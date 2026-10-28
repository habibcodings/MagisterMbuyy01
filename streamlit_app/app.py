"""Streamlit version of the data story "Bukan Bumi yang Makin Gaduh, Telinga Kita yang Makin Tajam".

The same story as site/, without scroll animations: every visible string comes from teks.py (verbatim from the page copy)
and every number from site/data/*.json (written by notebooks/analisis.ipynb). The guesses, the per-section "Versi mudah"
toggles, the MLv switch, the spike cards and the "Cek judulmu" tool are Streamlit widgets.

Run from the repository root:  streamlit run streamlit_app/app.py
"""
import html
import json
from pathlib import Path

import streamlit as st

import charts
import teks as T

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "data"
REPO_URL = None        # TODO(kelompok): the public GitHub repository URL
AI_STATEMENT = None    # TODO(kelompok): the AI-use statement (course guide §6)

TOGGLED = ["hero", "g1", "g2", "g3", "g4", "g5", "g6"]    # sections with their own toggle; the bridge follows the global one
ORDER = ["hero", "g1", "g2", "g3", "g4", "g5", "g6", "tool"]
FIG_DATA = {"g1": "f1", "g2": "f2", "g3": "f3", "g4": "f4", "g5": "f5", "g6": "f6", "gx": "fx"}
TONE = {"strong": "#C2410C", "small": "#B8BEC6", "neutral": "#475569"}
TONE_TEXT = {"strong": "#C2410C", "small": "#6B7280", "neutral": "#475569"}
BLOCK_VALUES = {
    "m5_2020": lambda D: D["f1"]["m5_2020"], "m5_2025": lambda D: D["f1"]["m5_2025"],
    "at_3_0[0]": lambda D: D["f3"]["at_3_0"][0], "at_3_0[1]": lambda D: D["f3"]["at_3_0"][1],
    "median_A": lambda D: D["f4"]["median_A"], "median_B": lambda D: D["f4"]["median_B"],
    "median": lambda D: round(D["f5"]["median"]),
    "spike_2019_11": lambda D: next(s["value"] for s in D["f5"]["spikes"] if s["month"] == "2019-11"),
}

st.set_page_config(page_title=T.TITLE, layout="centered", initial_sidebar_state="collapsed")
ss = st.session_state


def fmt(v):
    return f"{int(round(v)):,}".replace(",", ".")


def dec1(v):
    return f"{v:.1f}".replace(".", ",")


def e(s):
    return html.escape(str(s), quote=False)


@st.cache_data
def load():
    return {n: json.loads((DATA / f"{n}.json").read_text()) for n in FIG_DATA.values()}


@st.cache_data(show_spinner=False)
def chart_png(fig_id, variant):
    return charts.png(charts.FIGURES[fig_id](load()[FIG_DATA[fig_id]], variant))


def month(ym):
    return f"{charts.MONTHS[int(ym[5:]) - 1]} {ym[:4]}"


# ---------- state and callbacks ----------

for s in TOGGLED:
    ss.setdefault(f"easy_{s}", False)
for k, v in {"easy_all": False, "g1": None, "g2": None, "g2_value": 50, "toast": None, "scroll_to": None,
             "tool_year_out": None, "tool_new_out": None}.items():
    ss.setdefault(k, v)


def passed(section):
    """Reaching a later section counts as scrolling past an unanswered guess: reveal it as skipped (guesses never block)."""
    i = ORDER.index(section)
    if i > ORDER.index("g1") and ss.g1 is None:
        ss.g1 = "skipped"
    if i > ORDER.index("g2") and ss.g2 is None:
        ss.g2 = "skipped"


def on_section_toggle(sec):
    ss.easy_all = all(ss[f"easy_{s}"] for s in TOGGLED)
    if sec in T.FIGS:
        ss.toast = (T.ANNOUNCE_EASY if ss[f"easy_{sec}"] else T.ANNOUNCE_CHART).format(n=T.FIGS[sec]["n"])
        ss.scroll_to = f"card_{sec}"   # keep the reader's place: the section changes height
    passed(sec)


def on_global_toggle():
    for s in TOGGLED:
        ss[f"easy_{s}"] = ss.easy_all


def answer_g1(kind):
    ss.g1 = kind


def answer_g2(kind):
    passed("g2")
    ss.g2 = kind
    ss.g2_value = ss.get("g2_guess", 50)


# ---------- "Cek judulmu" rules (copy §10) ----------

def decide(year, total, now, last, felt):
    t = T.TOOL
    out = dict(year=year, range=None, felt=None, extra=None)
    if now < last:
        out.update(case="A", finding=t["a_finding"].format(last=fmt(last), now=fmt(now)), advice=t["avoid"],
                   headline=t["a_headline"].format(total=fmt(total), tahun=year))
    elif now == last:
        out.update(case="B", finding=t["b_finding"].format(now=fmt(now)), advice=t["avoid"],
                   headline=t["b_headline"].format(total=fmt(total), tahun=year))
    else:
        pct = fmt(abs(now - last) / last * 100)
        out.update(case="C", finding=t["c_finding"].format(last=fmt(last), now=fmt(now), pct=pct),
                   range=t["c_in_range"] if now <= 244 else t["c_above_range"], advice=t["c_advice"],
                   headline=t["c_headline"].format(total=fmt(total), tahun=year, pct=pct))
    if felt is not None:
        out["felt"] = t["felt_line"].format(felt=fmt(felt))
    if year == 2024:
        out["extra"] = t["extra_2024"]
    return out


def from_year(year):
    rows = {r["year"]: r for r in load()["f1"]["years"]}
    r, prev = rows[year], rows[year - 1]
    return decide(year, r["total"], r["m5plus"], prev["m5plus"], r["felt"])


# ---------- page pieces ----------

CSS = """
.stApp { background: #FCF7FB; }
.block-container { padding-top: 1.2rem; max-width: 760px; }
/* the top bar's own wrapper is only as tall as the bar, so the wrapper is what sticks */
[data-testid="stLayoutWrapper"]:has(> .st-key-topbar) { position: sticky; top: 0; z-index: 99; }
.st-key-topbar { background: #FCF7FB; border-bottom: 1px solid #EBDDE7; padding: 6px 0 2px; }
.hdr { display: flex; flex-wrap: wrap; gap: 4px 14px; align-items: baseline; font-size: .9rem; }
.hdr b { font-weight: 800; }
.hdr a { color: #6B4A63; font-weight: 700; text-decoration: none; }
.hdr a:hover { color: #A8336F; text-decoration: underline; }
.stHtml [id] { scroll-margin-top: 64px; }   /* anchors land below the sticky top bar */
.skip { position: absolute; left: -9999px; }
.skip:focus { position: static; display: inline-block; margin-bottom: 4px; background: #3F1D38; color: #fff !important;
  padding: 6px 12px; border-radius: 999px; }
.st-key-hero { background: linear-gradient(120deg, #F7D9EE, #EAD6FA); border-radius: 24px; padding: 26px 24px 18px; }
.kicker { font-size: .78rem; font-weight: 800; letter-spacing: .12em; color: #A8336F; margin: 0; }
.st-key-hero .kicker { color: #6B4A63; }
h1.title { font-size: clamp(2.1rem, 6vw, 3.3rem); font-weight: 800; line-height: 1.12; margin: .3rem 0 1rem; color: #3F1D38; }
.main-message { font-size: 1.28rem; font-weight: 600; line-height: 1.45; margin: 0 0 .6rem; }
.byline { color: #6B4A63; font-size: .88rem; margin: .2rem 0 .3rem; }
.cue { color: #6B4A63; font-weight: 700; font-size: .88rem; margin: 0; }
.lede { font-size: 1.22rem; font-weight: 600; line-height: 1.55; margin: 1.6rem 0 1rem; }
.prose { font-size: 1.08rem; line-height: 1.6; margin: 1.4rem 0; }
.orbcard { position: relative; background: linear-gradient(135deg, #F9E9F4, #F1E9FB); border-radius: 22px;
  padding: 16px 20px 16px 62px; box-shadow: 0 2px 6px rgba(63,29,56,.06), 0 12px 28px rgba(63,29,56,.07); margin: .4rem 0; }
.orbcard::before { content: ""; position: absolute; left: 18px; top: 18px; width: 28px; height: 28px; border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #fff 0 18%, transparent 20%), linear-gradient(135deg, #F28CC3, #B58AF0); }
.orbcard p { margin: 0; font-weight: 700; }
.keycard p { font-size: 1.14rem; font-weight: 800; }
.steps { background: #fff; border-radius: 20px; padding: 14px 20px; box-shadow: 0 2px 6px rgba(63,29,56,.06); margin: .4rem 0; }
.steps p { margin: .35rem 0; font-size: 1.04rem; line-height: 1.55; }
[class*="st-key-card"] { scroll-margin-top: 72px; background: #fff; border-radius: 22px !important; box-shadow: 0 2px 6px rgba(63,29,56,.06), 0 12px 28px rgba(63,29,56,.07); }
.fig-num { font-size: .7rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; color: #6B4A63; }
.fig-title { font-size: 1.18rem; font-weight: 800; line-height: 1.25; margin: .15rem 0 .2rem; color: #3F1D38; }
.fig-sub { font-size: .92rem; font-weight: 600; color: #6B4A63; margin: 0; }
.fig-note, .fig-source { font-size: .76rem; line-height: 1.45; color: #6B4A63; margin: .2rem 0; }
.guess-kicker { color: #A8336F; font-weight: 800; margin: 0 0 .2rem; }
.guess-q { margin: 0 0 .2rem; font-size: 1.04rem; }
.feedback { font-weight: 800; margin: .2rem 0; font-size: 1.04rem; }
.spike-card { display: inline-block; border: 1.5px solid #3F1D38; border-radius: 14px; padding: 8px 14px; font-weight: 700;
  font-size: .92rem; background: #fff; }
.blk { padding: 18px 4px 10px; }
.cmp-row { margin: 0 0 18px; }
.cmp-label { font-weight: 700; font-size: .98rem; color: #374151; margin-bottom: 6px; }
.cmp-line { display: flex; align-items: center; gap: 12px; }
.cmp-track { flex: 1; height: 26px; border-radius: 999px; background: #F0F1F3; overflow: hidden; }
.cmp-bar { height: 100%; border-radius: 999px; animation: grow .6s cubic-bezier(.2,.7,.2,1); }
.cmp-val { font-size: 1.7rem; font-weight: 800; min-width: 3.2ch; text-align: right; }
.dots { display: grid; grid-template-columns: repeat(20, 1fr); gap: 5px; max-width: 520px; margin: 0 auto; }
.dots i { display: block; aspect-ratio: 1; border-radius: 50%; background: #B8BEC6; }
.dots-cap { text-align: center; font-weight: 800; font-size: 1.2rem; margin-top: 12px; }
.num { text-align: center; font-size: 6rem; font-weight: 800; line-height: 1; }
.num-dots { display: flex; justify-content: center; gap: 10px; margin-top: 12px; }
.num-dots i { width: 14px; height: 14px; border-radius: 50%; display: block; }
@keyframes grow { from { width: 0; } }
@media (prefers-reduced-motion: reduce) { .cmp-bar { animation: none; } }
.checklist { background: linear-gradient(135deg, #F9E9F4, #F1E9FB); border-radius: 22px; padding: 20px 24px; margin: 1.6rem 0 .8rem; }
.checklist h2, .endmatter h2 { font-size: 1.45rem; font-weight: 800; margin: 0 0 .6rem; }
.checklist li { font-weight: 600; margin-bottom: .45rem; }
.endmatter { margin: 2rem 0 .6rem; }
.endmatter li { margin-bottom: .45rem; }
.sources { list-style: none; padding: 0; font-size: .9rem; }
.sources li { overflow-wrap: anywhere; }
.endmatter a, .footer a { color: #A8336F; }
.todo { background: #FFF4D6; border-radius: 4px; padding: 0 3px; }
.footer { border-top: 1px solid #EBDDE7; margin-top: 2.4rem; padding-top: 1rem; font-size: .84rem; color: #6B4A63; }
.footer p { margin: 0 0 .3rem; }
.sr-only { position: absolute !important; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
"""


def anchor(name):
    st.html(f'<div id="{name}"></div>')


def kicker(text):
    st.html(f'<p class="kicker">{e(text)}</p>')


def steps(lines):
    st.html('<div class="steps">' + "".join(f"<p>{e(x)}</p>" for x in lines) + "</div>")


def orbcard(text, cls=""):
    st.html(f'<div class="orbcard {cls}"><p>{e(text)}</p></div>')


def block_html(fid):
    b, D = T.FIGS[fid]["block"], load()
    color, text_color = TONE[b["tone"]], TONE_TEXT[b["tone"]]
    if b["type"] == "compare":
        rows = [(label, BLOCK_VALUES[ref](D)) for label, ref in b["rows"]]
        top = max(v for _, v in rows)
        inner = "".join(
            f'<div class="cmp-row"><div class="cmp-label">{e(label)}</div><div class="cmp-line"><div class="cmp-track">'
            f'<div class="cmp-bar" style="width:{v / top * 100:.1f}%;background:{color}"></div></div>'
            f'<div class="cmp-val" style="color:{text_color}">{fmt(v)}</div></div></div>' for label, v in rows)
        return f'<div class="blk">{inner}</div>'
    if b["type"] == "dots":
        dots = "".join(f'<i style="background:{color}"></i>' if i < b["highlight"] else "<i></i>" for i in range(100))
        return f'<div class="blk"><div class="dots">{dots}</div><div class="dots-cap" style="color:{text_color}">{e(b["caption"])}</div></div>'
    dots = "".join(f'<i style="background:{color}"></i>' for _ in range(b["value"]))
    return f'<div class="blk"><div class="num" style="color:{text_color}">{fmt(b["value"])}</div><div class="num-dots">{dots}</div></div>'


def figure_card(fid, variant, controls=None):
    f = T.FIGS[fid]
    with st.container(border=True, key=f"card_{fid}"):
        left, right = st.columns([4, 1.5], vertical_alignment="top")
        left.html(f'<div class="fig-num">{e(T.FIG_NUM.format(n=f["n"]))}</div><h2 class="fig-title">{e(f["title"])}</h2>'
                  f'<p class="fig-sub">{e(f["subtitle"])}</p>')
        right.toggle(T.SECTION_TOGGLE, key=f"easy_{fid}", help=T.SECTION_TOGGLE_ARIA.format(n=f["n"]),
                     on_change=on_section_toggle, args=(fid,))
        if ss[f"easy_{fid}"]:
            st.html(block_html(fid))
        else:
            if controls:
                controls()
            st.image(chart_png(fid, variant), alt=f["alt"], width="stretch")
        st.html(f'<p class="fig-note">{e(f["note"])}</p><p class="fig-source">{e(f["source"])}</p>')


def easy_section(fid):
    """Easy mode: the block replaces the chart, one plain card replaces the steps; the key card and the source stay."""
    f = T.FIGS[fid]
    figure_card(fid, None)
    orbcard(f["easy"])
    orbcard(f["key"], "keycard")


def copy_button(text):
    label, done = json.dumps(T.TOOL["copy"]), json.dumps(T.TOOL["copied"])
    # the headline is built from our own strings and integers only; set with textContent, never as HTML
    st.iframe(f"""
<button id="b" style="font:700 15px Nunito,'Segoe UI',system-ui,sans-serif;border:2px solid #3F1D38;background:#fff;color:#3F1D38;
 padding:9px 14px;border-radius:999px;cursor:pointer;min-height:42px"></button>
<script>
const b = document.getElementById('b'), text = {json.dumps(text)};
b.textContent = {label};
b.onclick = async () => {{
  let ok = false;
  try {{ await navigator.clipboard.writeText(text); ok = true; }} catch (err) {{
    const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select();
    try {{ ok = document.execCommand('copy'); }} catch (err2) {{ ok = false; }}
    ta.remove();
  }}
  if (ok) {{ b.textContent = {done}; setTimeout(() => {{ b.textContent = {label}; }}, 2000); }}
}};
</script>""", height=54)


def tool_output(out):
    st.html(f'<p class="feedback">{e(out["finding"])}</p>' + (f'<p>{e(out["range"])}</p>' if out["range"] else "")
            + f'<p>{e(out["advice"])}</p>')
    orbcard(out["headline"], "keycard")
    copy_button(out["headline"])
    extra = [x for x in (out["felt"], out["extra"]) if x]
    if extra:
        st.html("".join(f"<p>{e(x)}</p>" for x in extra))


# ---------- sections ----------

def topbar():
    with st.container(key="topbar"):
        left, right = st.columns([3, 2], vertical_alignment="center")
        nav = " · ".join(f'<a href="#{target}">{e(label)}</a>' for label, target in T.PROGRESS)
        left.html(f'<a class="skip" href="#keterbatasan">{e(T.SKIP_LINK)}</a>'
                  f'<div class="hdr"><b>{e(T.HEADER_TITLE)}</b><span>{nav}</span></div>')
        right.toggle(T.GLOBAL_TOGGLE, key="easy_all", help=T.GLOBAL_TOGGLE_ARIA, on_change=on_global_toggle)


def hero():
    with st.container(key="hero"):
        anchor("hero")
        left, right = st.columns([3, 1.3], vertical_alignment="center")
        left.html(f'<p class="kicker">{e(T.HERO_KICKER)}</p>')
        right.toggle(T.SECTION_TOGGLE, key="easy_hero", on_change=on_section_toggle, args=("hero",))
        st.html(f'<h1 class="title">{e(T.TITLE)}</h1><p class="main-message">{e(T.MAIN_MESSAGE)}</p>')
        if ss.easy_hero:
            orbcard(T.PLAIN_CARD)
        st.html(f'<p class="byline">{e(T.BYLINE)}</p><p class="cue">{e(T.SCROLL_CUE)}</p>')
    st.html(f'<p class="lede">{e(T.LEDE)}</p>')


def section_g1():
    f = T.FIGS["g1"]
    anchor("g1")
    kicker(f["kicker"])
    if ss.easy_g1:
        anchor("konflik")
        easy_section("g1")
        return
    steps(f["steps"])
    revealed = ss.g1 is not None
    figure_card("g1", "final" if revealed else "guess")
    anchor("konflik")
    g = T.G1_GUESS
    with st.container(border=True, key="card_g1_guess"):
        st.html(f'<p class="guess-kicker">{e(g["kicker"])}</p><p class="guess-q">{e(g["question"])}</p>')
        for (k, label), col in zip(g["buttons"], st.columns(3)):
            col.button(label, key=f"g1_{k}", on_click=answer_g1, args=(k,), disabled=revealed, width="stretch")
        st.button(g["skip"], key="g1_skip", type="tertiary", on_click=answer_g1, args=("skipped",), disabled=revealed)
    if revealed:
        fb = g["turun"] if ss.g1 == "turun" else g["skipped"] if ss.g1 == "skipped" else g["other"]
        st.html(f'<div class="steps"><p class="feedback">{e(fb)} {e(g["always"])}</p></div>')
        orbcard(f["key"], "keycard")


def section_g2():
    f = T.FIGS["g2"]
    anchor("g2")
    kicker(f["kicker"])
    if ss.easy_g2:
        easy_section("g2")
        return
    g = T.G2_GUESS
    revealed = ss.g2 is not None
    with st.container(border=True, key="card_g2_guess"):
        st.html(f'<p class="guess-kicker">{e(g["kicker"])}</p><p class="guess-q">{e(g["question"])}</p>')
        if revealed:
            fb = g["answered"].format(x=fmt(ss.g2_value)) if ss.g2 == "answered" else g["skipped"]
            st.html(f'<p class="feedback">{e(fb)}</p>')
        else:
            st.slider(g["slider"].format(x=fmt(ss.get("g2_guess", 50))), 0, 100, 50, 1, key="g2_guess",
                      on_change=passed, args=("g2",))
            a, b = st.columns([1, 1])
            a.button(g["button"], key="g2_answer", on_click=answer_g2, args=("answered",), width="stretch")
            b.button(g["skip"], key="g2_skip", type="tertiary", on_click=answer_g2, args=("skipped",))
    figure_card("g2", "final" if revealed else "guess")
    if revealed:
        steps(f["steps"][1:])
        orbcard(f["key"], "keycard")


def bridge():
    anchor("jembatan")
    if ss.easy_all:
        orbcard(T.BRIDGE_EASY)
    else:
        st.html(f'<p class="prose">{e(T.BRIDGE)}</p>')


def section_simple(fid, controls=None, after=None, variant=lambda: "final"):
    f = T.FIGS[fid]
    anchor(fid)
    kicker(f["kicker"])
    if ss[f"easy_{fid}"]:
        easy_section(fid)
        return
    steps(f["steps"] if not after else f["steps"][:-1])
    figure_card(fid, variant(), controls)
    if after:
        after()
    orbcard(f["key"], "keycard")


def g3_controls():
    modes = T.FIGS["g3"]["modes"]
    st.segmented_control(T.FIGS["g3"]["title"], modes, default=modes[0], key="g3_mode", required=True,
                         label_visibility="collapsed", on_change=passed, args=("g3",))


def g3_variant():
    return "mlv" if ss.get("g3_mode") == T.FIGS["g3"]["modes"][1] else "all"


def g5_spikes():
    d = load()["f5"]
    options = {f"{s['label']} · {month(s['month'])}": s for s in d["spikes"]}
    with st.container(border=True, key="card_g5_spikes"):
        choice = st.pills(T.FIGS["g5"]["steps"][-1], list(options), key="g5_spike", on_change=passed, args=("g5",))
        if choice:
            s = options[choice]
            card = T.FIGS["g5"]["card"].format(nama=s["label"], bulan=month(s["month"]), nilai=fmt(s["value"]),
                                               kelipatan=dec1(s["value"] / round(d["median"])))
            st.html(f'<div class="spike-card">{e(card)}</div>')


def on_tool_year():
    passed("tool")
    ss.tool_year_out = None   # a new year needs a new check


def tool():
    t = T.TOOL
    anchor("cek-judul")
    st.html(f'<div class="endmatter"><h2>{e(t["heading"])}</h2><p>{e(t["intro"])}</p></div>')
    with st.container(border=True, key="card_tool"):
        tab_year, tab_new = st.tabs(t["tabs"])
        with tab_year:
            year = st.selectbox(t["year"], [2021, 2022, 2023, 2024, 2025], index=4, key="tool_year",
                                on_change=on_tool_year)
            if st.button(t["button"], key="tool_year_btn"):
                passed("tool")
                ss.tool_year_out = from_year(year)
            if ss.tool_year_out:
                tool_output(ss.tool_year_out)
        with tab_new:
            i = t["inputs"]
            vals = dict(
                year=st.number_input(i["year"], min_value=1000, max_value=9999, value=None, step=1, format="%d", key="n_year"),
                total=st.number_input(i["total"], min_value=0, value=None, step=1, format="%d", key="n_total"),
                now=st.number_input(i["now"], min_value=0, value=None, step=1, format="%d", key="n_now"),
                last=st.number_input(i["last"], min_value=1, value=None, step=1, format="%d", key="n_last"),
                felt=st.number_input(i["felt"], min_value=0, value=None, step=1, format="%d", key="n_felt"))
            ready = all(vals[k] is not None for k in ("year", "total", "now", "last"))
            if st.button(t["button"], key="tool_new_btn", disabled=not ready):
                passed("tool")
                ss.tool_new_out = decide(int(vals["year"]), int(vals["total"]), int(vals["now"]), int(vals["last"]),
                                         None if vals["felt"] is None else int(vals["felt"]))
            if ss.tool_new_out:
                tool_output(ss.tool_new_out)
    st.html(f'<p class="fig-note">{e(t["footnote"])}</p>')


def endmatter():
    st.html(f'<div class="checklist" id="daftar-periksa"><h2>{e(T.CHECKLIST_TITLE)}</h2><ol>'
            + "".join(f"<li>{e(x)}</li>" for x in T.CHECKLIST) + "</ol></div>")

    def italic(text, words):
        out = e(text)
        return out.replace(e(words), f"<em>{e(words)}</em>") if words else out
    st.html(f'<div class="endmatter" id="keterbatasan"><h2>{e(T.LIMITS_TITLE)}</h2><ol>'
            + "".join(f"<li>{italic(text, words)}</li>" for text, words in T.LIMITS) + "</ol></div>")

    repo = f'<a href="{e(REPO_URL)}">{e(REPO_URL)}</a>' if REPO_URL else f'<span class="todo">{e(T.REPO_PLACEHOLDER)}</span>'
    items = "".join(f'<li><strong>{lab}</strong> {before} <a href="{url}">{e(text)}</a>{after}</li>'
                    for lab, before, text, url, after in T.SOURCES)
    st.html(f'<div class="endmatter" id="sumber"><h2>{e(T.SOURCES_TITLE)}</h2><ul class="sources">{items}</ul>'
            f'<p>{e(T.REPO_LINE).replace("{link}", repo)}</p></div>')

    g = T.GX
    st.html(f'<div class="endmatter" id="gambar-dibuang"><h2>{e(g["heading"])}</h2></div>')
    with st.container(border=True, key="card_gx"):
        st.html(f'<h3 class="fig-title">{e(g["title"])}</h3><p class="fig-sub">{e(g["subtitle"])}</p>')
        st.image(chart_png("gx", "final"), alt=f'{g["title"]}. {g["subtitle"]}', width="stretch")
        st.html(f'<p class="fig-note">{e(g["note"])}</p><p class="fig-source">{e(g["source"])}</p>')
    st.html(f'<p class="prose">{e(g["reason"])}</p>')

    repo_f = f'<a href="{e(REPO_URL)}">{e(REPO_URL)}</a>' if REPO_URL else f'<span class="todo">{e(T.FOOTER_REPRO_PLACEHOLDER)}</span>'
    ai = e(AI_STATEMENT) if AI_STATEMENT else f'<span class="todo">{e(T.FOOTER_AI_PLACEHOLDER)}</span>'
    st.html(f'<div class="footer"><p>{e(T.FOOTER_REPRO).replace("{link}", repo_f)}</p>'
            f'<p>{e(T.FOOTER_AI).replace("{isi}", ai)}</p><p>{e(T.FOOTER_COPYRIGHT)}</p></div>')


# ---------- page ----------

st.html(f"<style>{CSS}</style>")
if ss.toast:
    st.toast(ss.toast)
    ss.toast = None
topbar()
hero()
section_g1()
section_g2()
bridge()
section_simple("g3", controls=g3_controls, variant=g3_variant)
section_simple("g4")
section_simple("g5", after=g5_spikes)
section_simple("g6")
tool()
endmatter()
if ss.scroll_to:
    # after a section toggle, bring the same figure card back under the top bar (the section got shorter or longer)
    st.iframe(f"""<script>
const target = {json.dumps(ss.scroll_to)};
let tries = 0;
(function go() {{
  const el = window.parent.document.querySelector('.st-key-' + target);
  if (el) el.scrollIntoView({{block: 'start'}});
  else if (tries++ < 20) setTimeout(go, 100);
}})();
</script>""", height=1)
    ss.scroll_to = None
