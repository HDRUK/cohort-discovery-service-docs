"""
Build OMOP LOCATION tables for the whole UK from the uk-postcode-mapper database.

The companion project https://github.com/HDRUK/uk-postcode-mapper builds a SQLite
database (``data/postcode.db``) with two tables:

  * ``postcode_lookup``  — every UK postcode → LSOA / Data Zone / Super Data Zone code
  * ``lsoa_centroids``   — LSOA/DZ/SDZ code → population-weighted centroid (lat, lon)

This script exports an OMOP CDM ``LOCATION`` table (one row per small-area code)
covering only the codes that a real postcode can actually resolve to, joined to
their centroid. That guarantees the ``location_source_value`` column matches exactly
what the mapper returns, so a custodian who blurs a postcode to its LSOA can look the
row up directly.

Codes are split by nation using their prefix:

  * ``E01`` → England (LSOA 2021)
  * ``W01`` → Wales (LSOA 2021)
  * ``S01`` → Scotland (Data Zone 2022)
  * ``N21`` → Northern Ireland (Super Data Zone 2021)

Non-geographic ONS pseudocodes (``L99999999``, ``M99999999`` …) are skipped.

Usage:
    python scripts/build_uk_location.py \
        --db ../uk-postcode-mapper/data/postcode.db \
        --out-dir locations
"""

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

# location_source_value prefix → (nation slug, human label)
NATIONS = {
    "E01": ("england", "England (LSOA 2021)"),
    "W01": ("wales", "Wales (LSOA 2021)"),
    "S01": ("scotland", "Scotland (Data Zone 2022)"),
    "N21": ("northern-ireland", "Northern Ireland (Super Data Zone 2021)"),
}

OMOP_FIELDS = [
    "location_id",
    "address_1",
    "address_2",
    "city",
    "state",
    "zip",
    "county",
    "location_source_value",
    "country_concept_id",
    "country_source_value",
    "latitude",
    "longitude",
]


def load_rows(db_path: Path):
    """Return {nation_slug: [(code, lat, lon), ...]} sorted by code, for codes a
    postcode can reach that also have a centroid."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    rows = cur.execute(
        """
        SELECT DISTINCT p.lsoa_code, c.latitude, c.longitude
        FROM postcode_lookup p
        JOIN lsoa_centroids c ON c.lsoa_code = p.lsoa_code
        WHERE p.lsoa_code IS NOT NULL
          AND c.latitude IS NOT NULL
          AND c.longitude IS NOT NULL
        """
    ).fetchall()
    con.close()

    by_nation: dict[str, list] = {slug: [] for slug, _ in NATIONS.values()}
    skipped = 0
    for code, lat, lon in rows:
        entry = NATIONS.get(code[:3])
        if entry is None:
            skipped += 1
            continue
        by_nation[entry[0]].append((code, lat, lon))
    for slug in by_nation:
        by_nation[slug].sort(key=lambda r: r[0])
    return by_nation, skipped


def write_location(rows, out_path: Path):
    """Write an OMOP LOCATION table (tab-separated) with sequential location_id."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OMOP_FIELDS, delimiter="\t")
        writer.writeheader()
        for location_id, (code, lat, lon) in enumerate(rows, start=1):
            writer.writerow(
                {
                    "location_id": location_id,
                    "address_1": "",
                    "address_2": "",
                    "city": "",
                    "state": "",
                    "zip": "",
                    "county": "",
                    "location_source_value": code,
                    "country_concept_id": "",
                    "country_source_value": "",
                    "latitude": lat,
                    "longitude": lon,
                }
            )
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build OMOP LOCATION tables (full UK + per-nation) from uk-postcode-mapper"
    )
    parser.add_argument(
        "--db",
        default="../uk-postcode-mapper/data/postcode.db",
        help="Path to the uk-postcode-mapper SQLite database (data/postcode.db)",
    )
    parser.add_argument(
        "--out-dir",
        default="locations",
        help="Directory to write the LOCATION tables into",
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        sys.exit(
            f"Database not found: {db_path}\n"
            "Build it first in the uk-postcode-mapper repo:\n"
            "    python scripts/build_db.py \\\n"
            "        --postcodes data/PCD_OA21_LSOA21_MSOA21_LAD_MAY26_UK_LU.csv \\\n"
            "        --england-wales data/lsoa_latlong.csv \\\n"
            "        --scotland data/scotland_locations.csv \\\n"
            "        --northern-ireland data/ni_locations.csv"
        )

    out_dir = Path(args.out_dir)
    print(f"Reading postcode-reachable centroids from {db_path}…")
    by_nation, skipped = load_rows(db_path)

    # Per-nation files.
    all_rows: list = []
    for prefix, (slug, label) in NATIONS.items():
        rows = by_nation[slug]
        n = write_location(rows, out_dir / slug / "LOCATION.csv")
        all_rows.extend(rows)
        print(f"  {label:<40} {n:>6} rows → {out_dir / slug / 'LOCATION.csv'}")

    # Full UK file: nations concatenated in E, W, S, N order (already per-nation sorted).
    n_uk = write_location(all_rows, out_dir / "uk" / "LOCATION.csv")
    print(f"  {'United Kingdom (all nations)':<40} {n_uk:>6} rows → {out_dir / 'uk' / 'LOCATION.csv'}")
    if skipped:
        print(f"  (skipped {skipped} non-geographic / pseudo codes)")


if __name__ == "__main__":
    main()
