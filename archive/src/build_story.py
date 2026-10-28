"""Build the story page from story/content.md and check it against the guide.

All visible text comes from story/content.md, which holds the group's text verbatim
(from docs/storyboard.md and docs/figure-text.md). This script only lays it out, copies
the figure files, and reports what the guide still needs.

Blocks in content.md (everything else is Markdown):
    ::: figure <file in figures/>      title: (finding title)  alt:  caption: (optional)  title_in_image: yes|no
    ::: discarded <file in figures/discarded/>   reason:  alt:
    ::: sources / ::: limitations / ::: box      Markdown body
    ::: easy                                     Markdown body shown only in "explain easier" mode
    ELI5 building blocks, shown only in "explain easier" mode (all values and words come from the group).
    A filled block is paired with the next figure: in "explain easier" mode it replaces that chart
    (docs/easy-version.md, rule 1 "swap, never add"); in normal mode only the chart shows.
    ::: easy-number    value: (shown huge, e.g. a number)   text: (one plain sentence)
    ::: easy-compare   before_label:  before_value:  after_label:  after_value:  text:  tone: strong|small|neutral
    ::: easy-dots      total: (default 100)  highlight: (how many)  text:  tone: strong|small|neutral

Usage (from the repo root):
    python -m src.build_story            # build + print compliance report
    python -m src.build_story --strict   # exit 1 if anything required is missing
"""
import argparse
import html
import os
import re
import shutil
import sys
from pathlib import Path
from string import Template

import markdown

ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / "story"
CONTENT = STORY / "content.md"
TEMPLATE = STORY / "template.html"
SITE = STORY / "site"
FIGURES = ROOT / "figures"
DISCARDED = FIGURES / "discarded"
MAX_FIGURES = 7  # guide §3, Tahap 3
IMAGE_EXT = {".png", ".svg", ".jpg", ".jpeg", ".webp", ".gif"}

FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
BLOCK_RE = re.compile(r"^:::[ \t]*(figure|discarded|sources|limitations|box|easy-number|easy-compare|easy-dots|easy)[ \t]*(\S*)[ \t]*\n(.*?)^:::[ \t]*$", re.S | re.M)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
MD_EXT = ["extra"]


def parse_fields(text: str) -> dict:
    """key: value lines; lines without a key continue the previous value."""
    fields, key = {}, None
    for line in text.splitlines():
        m = re.match(r"^([a-z_]+):\s?(.*)$", line)
        if m:
            key = m.group(1)
            fields[key] = m.group(2).strip()
        elif key and line.strip():
            fields[key] += " " + line.strip()
    return fields


def md_block(text: str) -> str:
    # Markdown needs a blank line before a list that follows a paragraph line; add it (layout only).
    text = re.sub(r"(?m)^(?!\s*$)(?!\s*\d+\.\s)(.+)\n(?=\d+\.\s)", r"\1\n\n", text)
    out = markdown.markdown(text, extensions=MD_EXT)
    return out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")


def md_inline(text: str) -> str:
    out = markdown.markdown(text)
    return out[3:-4] if out.startswith("<p>") and out.endswith("</p>") and out.count("<p>") == 1 else out


def is_missing(value: str | None) -> bool:
    return not value or "TODO" in value


# Tones map to the storyboard §2 palette so the simple visuals keep "orange = stronger quakes".
TONES = {"strong": "#C2410C", "small": "#B8BEC6", "neutral": "#475569"}
TEXT_TONES = {"small": "#6B7280"}  # storyboard §2: text for the grey category uses #6B7280


def to_number(text: str | None) -> float | None:
    """Parse '1.820', '18.357', '2,5' or '42' (Indonesian format) into a float."""
    if not text:
        return None
    t = text.strip().replace(" ", "")
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", t):
        t = t.replace(".", "")
    t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def render_eli5(kind: str, f: dict) -> str | None:
    """Simple ELI5 visuals; returns None when a required field is missing (nothing is invented)."""
    tone_key = f.get("tone", "neutral").strip().lower() or "neutral"
    tone = TONES.get(tone_key, TONES["neutral"])
    text = f'<p class="eli5-text">{md_inline(f["text"])}</p>' if not is_missing(f.get("text")) else ""
    if kind == "easy-number":
        if is_missing(f.get("value")):
            return None
        return f'<div class="eli5 eli5-number"><div class="eli5-big" style="color:{TEXT_TONES.get(tone_key, tone)}">{html.escape(f["value"])}</div>{text}</div>'
    if kind == "easy-compare":
        need = ["before_label", "before_value", "after_label", "after_value"]
        vals = [to_number(f.get("before_value")), to_number(f.get("after_value"))]
        if any(is_missing(f.get(k)) for k in need) or None in vals or min(vals) < 0:
            return None
        top = max(vals) or 1
        rows = "".join(
            f'<div class="eli5-row"><span class="eli5-label">{html.escape(f[lab])}</span>'
            f'<span class="eli5-track"><span class="eli5-bar" style="width:{v / top * 100:.1f}%;background:{tone}"></span></span>'
            f'<span class="eli5-val">{html.escape(f[val])}</span></div>'
            for lab, val, v in [("before_label", "before_value", vals[0]), ("after_label", "after_value", vals[1])])
        return f'<div class="eli5 eli5-compare tone-{tone_key}">{rows}{text}</div>'
    if kind == "easy-dots":
        total, hit = to_number(f.get("total") or "100"), to_number(f.get("highlight"))
        if hit is None or total is None or not (0 <= hit <= total <= 400) or total != int(total) or hit != int(hit):
            return None
        dots = "".join(f'<i style="background:{tone}"></i>' if i < hit else "<i></i>" for i in range(int(total)))
        cols = 10 if total <= 50 else 20
        return f'<div class="eli5 eli5-dots"><div class="eli5-grid" style="grid-template-columns:repeat({cols},1fr)" role="img" aria-label="{int(hit)} / {int(total)}">{dots}</div>{text}</div>'
    return None


class Report:
    def __init__(self):
        self.items = []

    def add(self, ok: bool, msg: str, level: str = "MISSING"):
        self.items.append(("OK" if ok else level, msg))

    @property
    def missing(self) -> int:
        return sum(1 for s, _ in self.items if s == "MISSING")

    def text(self) -> str:
        width = max(len(s) for s, _ in self.items)
        return "\n".join(f"  [{s:<{width}}] {m}" for s, m in self.items)


def render_figure(file: str, f: dict, label: str | None, rel_dir: str, anchor: str | None = None, cls: str = "") -> str:
    parts = []
    if label:
        parts.append(f'  <p class="fig-num">{html.escape(label)}</p>')
    if f.get("title") and f.get("title_in_image", "no").lower() != "yes":
        parts.append(f'  <p class="fig-title">{html.escape(f["title"])}</p>')
    src = f"{rel_dir}/{html.escape(file)}"
    # the image links to itself so phone readers can open it full size and zoom
    parts.append(f'  <a href="{src}"><img src="{src}" alt="{html.escape(f.get("alt", ""))}"></a>')
    if f.get("caption"):
        parts.append(f'  <figcaption>{md_inline(f["caption"])}</figcaption>')
    attrs = (f' id="{anchor}" data-label="{html.escape(label or "")}"' if anchor else "") + (f' class="{cls}"' if cls else "")
    open_tag = f"<figure{attrs}>"
    return open_tag + "\n" + "\n".join(parts) + "\n</figure>"


def build(strict: bool = False) -> Report:
    raw = CONTENT.read_text(encoding="utf-8")
    text = COMMENT_RE.sub("", raw)
    rep = Report()

    m = FRONT_RE.match(text)
    meta = parse_fields(m.group(1)) if m else {}
    body_src = text[m.end():] if m else text

    msg = meta.get("main_message")
    rep.add(not is_missing(msg), "main message present, printed at the top (front matter `main_message`)")
    if not is_missing(msg):
        sentences = len(re.findall(r"[.!?](?=\s|$)", msg))
        rep.add(sentences <= 1, f"main message is one sentence (found {sentences} sentence ending(s))", "WARN")
    rep.add(not is_missing(meta.get("title")), "title present")
    rep.add(not is_missing(meta.get("authors")), "authors present", "WARN")
    fig_word = meta.get("figure_label", "")

    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "figures" / "discarded").mkdir(parents=True)

    parts, pos, n_fig = [], 0, 0
    seen = {"sources": 0, "limitations": 0, "discarded": 0, "box": 0, "easy": 0}
    eli5 = {"filled": 0, "empty": 0, "paired": 0}
    pending_eli5 = None
    for b in BLOCK_RE.finditer(body_src):
        parts.append(md_block(body_src[pos:b.start()]))
        kind, arg, inner = b.group(1), b.group(2), b.group(3)
        if kind == "figure":
            n_fig += 1
            f = parse_fields(inner)
            src = FIGURES / arg
            rep.add(src.is_file(), f"figure {n_fig}: file figures/{arg} exists")
            rep.add(not is_missing(f.get("title")), f"figure {n_fig}: finding title present")
            rep.add(not is_missing(f.get("alt")), f"figure {n_fig}: alt text present", "WARN")
            if src.is_file():
                shutil.copy2(src, SITE / "figures" / arg)
            label = f"{fig_word} {n_fig}" if fig_word else ""
            fig_html = render_figure(arg, f, label or None, "figures", cls="has-easy" if pending_eli5 else "")
            easy_html = ""
            if pending_eli5:
                pill = f'<p class="fig-num">{html.escape(label)}</p>' if label else ""
                easy_html = f'<section class="easy eli5-wrap">\n{pill}\n{pending_eli5}\n</section>\n'
                eli5["paired"] += 1
                pending_eli5 = None
            parts.append(f'<div class="slot" id="gambar-{n_fig}" data-label="{html.escape(label)}">\n{easy_html}{fig_html}\n</div>')
        elif kind == "discarded":
            seen["discarded"] += 1
            f = parse_fields(inner)
            src = DISCARDED / arg
            rep.add(src.is_file(), f"discarded figure: file figures/discarded/{arg} exists")
            rep.add(not is_missing(f.get("reason")), "discarded figure: reason present")
            if src.is_file():
                shutil.copy2(src, SITE / "figures" / "discarded" / arg)
            fig = render_figure(arg, {"alt": f.get("alt", ""), "title_in_image": "yes"}, None, "figures/discarded")
            parts.append(f'<section class="discarded">\n{fig}\n{md_block(f.get("reason", ""))}\n</section>')
        elif kind.startswith("easy-"):
            f = parse_fields(inner)
            if not any(v.strip() for v in f.values()):
                eli5["empty"] += 1  # untouched scaffold: not shown, not a warning
            else:
                block = render_eli5(kind, f)
                if block:
                    eli5["filled"] += 1
                    if pending_eli5:  # two filled blocks before one figure: keep the first, report the second
                        rep.add(False, f"{kind} before {fig_word} {n_fig + 1}: a second block for the same figure is not shown", "WARN")
                    else:
                        pending_eli5 = block
                else:
                    blank = [k for k, v in f.items() if not v.strip()]
                    rep.add(False, f"{kind} near {fig_word} {n_fig + 1}: not shown, fill in {', '.join(blank) or 'valid numbers'}", "WARN")
        else:
            seen[kind] += 1
            content = inner.strip()
            if kind not in ("box", "easy"):
                rep.add(not is_missing(content), f"{kind} section filled in")
            if kind == "sources" and not is_missing(content):
                rep.add(bool(re.search(r"[Dd]iunduh|[Dd]ownloaded", content)), "sources: download date given", "WARN")
            parts.append(f'<section class="{kind}">\n{md_block(content)}\n</section>')
        pos = b.end()
    parts.append(md_block(body_src[pos:]))
    if pending_eli5:  # a filled block with no figure after it
        rep.add(False, "an explain-easier block after the last figure is not shown", "WARN")

    rep.add(n_fig <= MAX_FIGURES, f"story figures on the page: {n_fig} (max {MAX_FIGURES})")
    story_files = [p for p in FIGURES.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXT] if FIGURES.exists() else []
    rep.add(len(story_files) <= MAX_FIGURES, f"image files in figures/: {len(story_files)} (max {MAX_FIGURES})")
    rep.add(seen["sources"] == 1, "exactly one sources section")
    rep.add(seen["limitations"] == 1, "exactly one limitations section")
    rep.add(seen["discarded"] == 1, "exactly one discarded figure")
    rep.add(True, f"explain-easier blocks: {eli5['paired']} of {n_fig} figures swap to a block in easy mode; {eli5['empty']} empty blocks hidden", "INFO")
    leftover = len(re.findall(r"TODO", text))
    rep.add(leftover == 0, f"no TODO placeholders left (found {leftover})")

    page = Template(TEMPLATE.read_text(encoding="utf-8")).safe_substitute(
        lang=html.escape(meta.get("lang", "id")),
        title=html.escape(meta.get("title", "")),
        main_message=html.escape(msg or ""),
        authors=html.escape(meta.get("authors", "")),
        easy_label=html.escape(meta.get("easy_label", "")),
        easy_intro=html.escape(meta.get("easy_intro", "")),
        body="\n".join(p for p in parts if p.strip()),
    )
    (SITE / "index.html").write_text(page, encoding="utf-8")
    (SITE / ".nojekyll").write_text("")

    print(f"built {os.path.relpath(SITE / 'index.html', ROOT)}")
    print("compliance check (guide §3 Tahap 3 and §5):")
    print(rep.text())
    print(f"  -> {rep.missing} required item(s) missing")
    if strict and rep.missing:
        sys.exit(1)
    return rep


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--strict", action="store_true", help="exit 1 if a required item is missing")
    build(strict=p.parse_args().strict)
