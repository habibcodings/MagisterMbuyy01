"""Rebuild the catalog from the author's archive at a pinned commit and verify it.

Follows the storyboard's reproducibility plan: fetch the raw archive and the author's
parser from github.com/kekavigi/repo-gempa at COMMIT, run the parser, and check every
file against the SHA-256 values in the author's MANIFEST.md for that commit.

Outputs (committed): data/raw/katalog_gempa_v2.tsv, data/raw/katalog_sensor.tsv,
data/raw/archive_days.csv, data/raw/MANIFEST.md.
Upstream files are cached in data/raw/upstream/ (not committed).

Usage (from the repo root):
    python -m src.download           # skip if the verified outputs are present
    python -m src.download --force   # re-fetch and rebuild
"""
import argparse
import csv
import hashlib
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
UPSTREAM = RAW / "upstream"

REPO = "kekavigi/repo-gempa"
COMMIT = "539ed6e461c409da1475781fd57bbc6deaef66ef"  # 2026-08-16, MANIFEST generated 2026-08-16T12:53:14Z
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}"

# Upstream inputs: path in repo -> expected SHA-256
# (archive value from the author's MANIFEST.md; parser value recorded on first fetch, 2026-10-28)
UPSTREAM_FILES = {
    "katalog_gempa_v2/bmkg_html.sqlite": "13c5333d0d4bf15648c4c0d114771e06e595958e910a0718b500bffe93689cf2",
    "katalog_gempa_v2/extract_tsv.py": "a87c11a3badf35f9e0e41bd894b410786b456c1be8c5d5661a08423caa18e469",
    "MANIFEST.md": None,
}
# Parser outputs -> expected SHA-256 from the author's MANIFEST.md.
# The catalog hash is reproduced with pandas 2.2.3; pandas 3 writes whole-second
# timestamps as ".000000" and changes the hash without changing the data.
OUTPUTS = {
    "katalog_gempa_v2.tsv": "7c92b9e9fba06a04b436c39956ba8ee7e7615fdbda9370d7a768e0f893dd77a7",
    "katalog_sensor.tsv": "5a4e57671c6b0ac718108987ad191c59a2870adf24f3ef101774bc145f66e466",
}
DAYS_FILE = "archive_days.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def http_get(url: str, attempts: int = 4) -> bytes:
    for i in range(1, attempts + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "vdl-midterm-download/1.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError) as exc:
            if i == attempts:
                raise
            print(f"  retry {i}/{attempts - 1} after: {exc}")
            time.sleep(5 * i)


def fetch(rel: str, expected: str | None) -> Path:
    target = UPSTREAM / Path(rel).name
    if not (target.exists() and (expected is None or sha256(target) == expected)):
        target.write_bytes(http_get(f"{RAW_BASE}/{rel}"))
    if expected and sha256(target) != expected:
        raise SystemExit(f"{rel}: SHA-256 {sha256(target)} does not match expected {expected}")
    return target


def export_days(db: Path, out: Path) -> int:
    """Day-level collection status from the archive: 'ok' or 'broken' (a gap, not zero activity)."""
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    rows = con.execute("SELECT date, status, event_count FROM days ORDER BY date").fetchall()
    con.close()
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "status", "event_count"])
        w.writerows(rows)
    return len(rows)


def outputs_verified() -> bool:
    return all((RAW / name).exists() and sha256(RAW / name) == h for name, h in OUTPUTS.items()) \
        and (RAW / DAYS_FILE).exists()


def write_manifest(when: str) -> None:
    lines = [
        "# Raw data manifest",
        "",
        "Written by `src/download.py`. Upstream files are fetched from the author's repository at a pinned commit; "
        "the catalog is rebuilt with the author's parser and checked against the author's MANIFEST.md.",
        "",
        f"- Repository: https://github.com/{REPO} at commit `{COMMIT}`",
        "- Dataset citation: Vigiliant, A. K. *Earthquakes in Indonesia*, Kaggle, DOI 10.34740/kaggle/ds/1934565",
        f"- Fetched / rebuilt (UTC): {when}",
        "",
        "| file | role | source | SHA-256 |",
        "|---|---|---|---|",
    ]
    for rel in UPSTREAM_FILES:
        p = UPSTREAM / Path(rel).name
        lines.append(f"| `upstream/{p.name}` | upstream input (not committed) | `{RAW_BASE}/{rel}` | `{sha256(p)}` |")
    for name in OUTPUTS:
        lines.append(f"| `{name}` | rebuilt by `extract_tsv.py`, matches author's MANIFEST | parser output | `{sha256(RAW / name)}` |")
    lines.append(f"| `{DAYS_FILE}` | `days` table of the archive (date, status, event_count) | exported from `bmkg_html.sqlite` | `{sha256(RAW / DAYS_FILE)}` |")
    (RAW / "MANIFEST.md").write_text("\n".join(lines) + "\n")


def main(force: bool = False) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    if outputs_verified() and not force:
        print("verified raw files already present; use --force to re-fetch and rebuild")
        return
    UPSTREAM.mkdir(parents=True, exist_ok=True)
    paths = {rel: fetch(rel, h) for rel, h in UPSTREAM_FILES.items()}
    db, parser = paths["katalog_gempa_v2/bmkg_html.sqlite"], paths["katalog_gempa_v2/extract_tsv.py"]

    # The parser only reads the archive and writes the two TSVs (reviewed 2026-10-28); run it isolated.
    subprocess.run([sys.executable, "-I", str(parser), "--db", str(db),
                    "--catalog-out", str(RAW / "katalog_gempa_v2.tsv"),
                    "--sensor-out", str(RAW / "katalog_sensor.tsv")], check=True, cwd=UPSTREAM)
    for name, expected in OUTPUTS.items():
        got = sha256(RAW / name)
        if got != expected:
            raise SystemExit(f"{name}: SHA-256 {got} does not match the author's MANIFEST ({expected}). "
                             "Check the pandas version (2.2.3 reproduces it).")
    n_days = export_days(db, RAW / DAYS_FILE)
    write_manifest(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))
    print(f"rebuilt and verified {', '.join(OUTPUTS)}; exported {n_days} archive days")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--force", action="store_true", help="re-fetch and rebuild even if verified outputs exist")
    main(force=p.parse_args().force)
