"""Analysis table and valid-day calendar from the verified raw files.

- data/processed/gempa_box.csv: events inside the analysis box (storyboard §5):
  latitude -11..6, longitude 94..142 (inclusive).
- data/processed/valid_days.csv: one row per archive day with its status ('ok' / 'broken').

Counting rules for the story follow docs/storyboard.md §2 (see the functions below
`round_mag` … `monthly_counts`). `rate()` is the earlier draft's method (events ÷ ok days
× 365.25), kept for the profiling tables.

Usage (from the repo root):
    python -m src.clean
"""
import calendar
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
CATALOG = RAW / "katalog_gempa_v2.tsv"
DAYS = RAW / "archive_days.csv"

BOX = {"lat_min": -11.0, "lat_max": 6.0, "lon_min": 94.0, "lon_max": 142.0}
DAYS_PER_YEAR = 365.25
NUMERIC = ["latitude", "longitude", "magnitude", "depth", "phasecount", "azimuth_gap"]
KEEP = ["eventID", "datetime_utc", "date", "year", "month", "latitude", "longitude", "depth",
        "magnitude", "mag_type", "phasecount", "azimuth_gap", "location", "agency"]


def read_catalog() -> pd.DataFrame:
    df = pd.read_csv(CATALOG, sep="\t", dtype=str, keep_default_na=False)
    for col in NUMERIC:
        df[col] = pd.to_numeric(df[col].replace("", None), errors="coerce")
    # Most timestamps carry microseconds; a few whole-second ones do not, so parse as ISO 8601.
    dt = pd.to_datetime(df["datetime"], utc=True, format="ISO8601")
    df["datetime_utc"] = dt
    df["date"] = dt.dt.strftime("%Y-%m-%d")
    df["year"] = dt.dt.year
    df["month"] = dt.dt.month
    df["mag_type"] = df["mag_type"].replace("", None)
    return df


def in_box(df: pd.DataFrame) -> pd.Series:
    b = BOX
    return df.latitude.between(b["lat_min"], b["lat_max"]) & df.longitude.between(b["lon_min"], b["lon_max"])


def read_days() -> pd.DataFrame:
    days = pd.read_csv(DAYS, dtype={"date": str, "status": str})
    days["year"] = days.date.str[:4].astype(int)
    days["month"] = days.date.str[5:7].astype(int)
    return days


def valid_days(days: pd.DataFrame, by: str | list[str] = "year") -> pd.Series:
    return days[days.status == "ok"].groupby(by).size()


def rate(events: pd.DataFrame, days: pd.DataFrame, years: range | list[int]) -> float:
    """Events per year of valid data, pooled over `years`."""
    years = list(years)
    n = int(events.year.isin(years).sum())
    v = int(days[(days.status == "ok") & days.year.isin(years)].shape[0])
    return n / v * DAYS_PER_YEAR


# ---------------------------------------------------------------------------
# Counting rules from docs/storyboard.md §2 (final, 2026-10-28)
# ---------------------------------------------------------------------------
MIN_DAYS_PER_MONTH = 15  # months with fewer days of data are gaps


def round_mag(m: pd.Series) -> pd.Series:
    """Magnitude rounded to one decimal, half up (as BMKG publishes)."""
    return np.floor(m * 10 + 0.5) / 10


def analysis_events() -> pd.DataFrame:
    """Events in the box that have a magnitude, with the rounded magnitude in `mag1`."""
    cat = read_catalog()
    ev = cat[in_box(cat) & cat.magnitude.notna()].copy()
    ev["mag1"] = round_mag(ev.magnitude)
    ev["ym"] = ev.datetime_utc.dt.tz_convert(None).dt.to_period("M")
    return ev


def days_in_year(y: int) -> int:
    return 366 if calendar.isleap(y) else 365


def yearly_counts(ev: pd.DataFrame, days: pd.DataFrame, years: range) -> pd.Series:
    """Events per calendar year; incomplete years scaled by (days in year ÷ days with data)."""
    ok = valid_days(days)
    counts = ev.groupby("year").size()
    out = {}
    for y in years:
        n, v, full = counts.get(y, 0), int(ok.get(y, 0)), days_in_year(y)
        out[y] = n * full / v if 0 < v < full else float(n)
    return pd.Series(out, dtype=float)


def pace(ev: pd.DataFrame, days: pd.DataFrame, year: int) -> float:
    """Partial-year pace scaled to the full calendar year."""
    ok = valid_days(days)
    return ev[ev.year == year].shape[0] * days_in_year(year) / int(ok[year])


def monthly_counts(ev: pd.DataFrame, days: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """Events per month from `start` to `end` (YYYY-MM): raw, scaled, and a gap flag.

    Months with fewer than MIN_DAYS_PER_MONTH days of data are gaps (scaled = NaN);
    other incomplete months are scaled by (days in month ÷ days with data)."""
    months = pd.period_range(start, end, freq="M")
    okm = days[days.status == "ok"].assign(ym=lambda d: pd.PeriodIndex(d.date, freq="M")).groupby("ym").size()
    raw = ev.groupby("ym").size()
    rows = []
    for m in months:
        n, v, full = int(raw.get(m, 0)), int(okm.get(m, 0)), m.days_in_month
        gap = v < MIN_DAYS_PER_MONTH
        scaled = np.nan if gap else (n * full / v if v < full else float(n))
        rows.append({"month": m, "raw": n, "days_with_data": v, "days_in_month": full,
                     "partial": (not gap) and v < full, "gap": gap, "count": scaled})
    return pd.DataFrame(rows).set_index("month")


def build() -> tuple[pd.DataFrame, pd.DataFrame]:
    cat = read_catalog()
    box = cat[in_box(cat)].copy()
    box["datetime_utc"] = box["datetime_utc"].dt.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    return box[KEEP].reset_index(drop=True), read_days()[["date", "status"]]


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    box, days = build()
    box.to_csv(PROCESSED / "gempa_box.csv", index=False)
    days.to_csv(PROCESSED / "valid_days.csv", index=False)
    print(f"gempa_box.csv: {len(box):,} events in box | valid_days.csv: {len(days):,} days "
          f"({int((days.status == 'ok').sum()):,} ok, {int((days.status == 'broken').sum())} broken)")


if __name__ == "__main__":
    main()
