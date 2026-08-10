# Pre-built UK LOCATION tables

Ready-to-use OMOP CDM `LOCATION` tables covering the whole UK, so custodians don't have
to build a location table themselves. Each row is one small-area statistical geography
(LSOA / Data Zone / Super Data Zone) with its **population-weighted centroid**
(`latitude`, `longitude`). The area code is stored in `location_source_value`.

For the full picture — why location matters, how BUNNY uses these coordinates, and the
privacy rationale for blurring postcodes to an area centroid — see the
[Location & Geo-radius Filtering](https://hdruk.github.io/cohort-discovery-service-docs/omop/location/)
page.

| File | Coverage | Code type | Rows |
|------|----------|-----------|-----:|
| `uk/LOCATION.csv` | United Kingdom (all four nations) | mixed | 43,914 |
| `england/LOCATION.csv` | England | LSOA 2021 (`E01…`) | 33,755 |
| `wales/LOCATION.csv` | Wales | LSOA 2021 (`W01…`) | 1,917 |
| `scotland/LOCATION.csv` | Scotland | Data Zone 2022 (`S01…`) | 7,392 |
| `northern-ireland/LOCATION.csv` | Northern Ireland | Super Data Zone 2021 (`N21…`) | 850 |

Files are tab-separated with the OMOP CDM 5.4 `LOCATION` columns. Only the four
nations' codes and their centroids are populated; address fields and country columns
are left blank. `location_id` is a sequential 1-based key, unique **within each file**.

## How to use them

### To add location to real OMOP data

These are the same centroids that [`uk-postcode-mapper`](https://github.com/HDRUK/uk-postcode-mapper)
returns. To attach a location to a real person **without storing their postcode**:

1. Blur the person's postcode to its LSOA / Data Zone / Super Data Zone code with
   `uk-postcode-mapper` (postcode → `lsoa_code`), inside your secure environment.
2. Find the row in the relevant `LOCATION.csv` where `location_source_value` equals
   that code, and read its `location_id`.
3. Set `person.location_id` to that value.

Because the `location_source_value` codes here are exactly the codes the mapper emits,
the join is guaranteed to resolve. BUNNY then answers distance queries using the
centroid's `latitude`/`longitude`.

### As synthetic test data (somop)

[`somop`](https://github.com/HDRUK/somop) can point a config's `location.prebuilt_file`
at one of these tables, assigning each synthetic person a random `location_id`:

```yaml
location:
  enabled: true
  prebuilt_file: scotland/LOCATION.csv   # path to a downloaded LOCATION.csv
```

## Provenance

A UK location is resolved in two joins, both implemented by `uk-postcode-mapper`:

```
Postcode → LSOA / Data Zone / Super Data Zone code → population-weighted centroid (lat, lon)
```

| Step | Source |
|------|--------|
| Postcode → area code | ONS Postcode Directory (`PCD_OA21_LSOA21_MSOA21_LAD_MAY26_UK_LU.csv`, ~2.7M postcodes) |
| England & Wales centroids | ONS LSOA population-weighted centroids (Open Geography Portal) |
| Scotland centroids | Scottish Government `DataZoneCent2022` ArcGIS layer (WGS84) |
| NI centroids | NI Super Data Zone centroids (via `drkane/geo-lookups`) |

All coordinates are WGS84 (EPSG:4326). Centroids are **population-weighted** — the point
representative of where residents actually live, not the geometric centre.

## Regenerating

Produced from the `uk-postcode-mapper` SQLite database, which combines the sources above:

```bash
# 1. Build the mapper database (in the uk-postcode-mapper repo)
python scripts/build_db.py \
  --postcodes data/PCD_OA21_LSOA21_MSOA21_LAD_MAY26_UK_LU.csv \
  --england-wales data/lsoa_latlong.csv \
  --scotland data/scotland_locations.csv \
  --northern-ireland data/ni_locations.csv

# 2. Export the LOCATION tables (from this repo's root)
python scripts/build_uk_location.py \
  --db ../uk-postcode-mapper/data/postcode.db \
  --out-dir locations
```

The export keeps only codes that a real postcode actually resolves to (dropping unused
legacy geographies and the ONS pseudocodes `L99999999` / `M99999999`), and joins each to
its centroid. See `scripts/build_uk_location.py`.

## Licence

Derived from the ONS Postcode Directory, ONS LSOA centroids (England & Wales), the
Scottish Government `DataZoneCent2022` layer, and NI Super Data Zone centroids — all
published under the [Open Government Licence v3](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/),
which permits reuse with attribution.
