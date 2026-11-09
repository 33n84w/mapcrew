# Analysis Plan

## Objective

Map the 2022 age-adjusted prevalence of diagnosed coronary heart disease among adults for all U.S. counties and county-equivalent areas using the complete CDC PLACES 2024 release.

## Inputs

- CDC PLACES 2024 County Data, measure `CHD`, data-value types `AgeAdjPrv` and `CrdPrv`.
- U.S. Census Bureau TIGERweb county polygons, layer 13, January 1, 2026 boundary vintage.

## Method

1. Download CDC rows for the CHD measure, including county FIPS, year, age-adjusted and crude prevalence, confidence limits, adult population, and suppression footnotes.
2. Download Census TIGERweb county polygons in WGS 84 and retain the 50 states and DC. Request a 0.001-degree generalization tolerance for a national viewer; this is display geometry, not survey-grade boundary data.
3. Validate schema, unique FIPS, estimate values, polygon geometry, expected coverage, and the one-to-one FIPS join. Fail rather than repair or silently omit unmatched records.
4. Preserve selected raw source rows and raw boundary GeoJSON under `data/`.
5. Write a derived county GeoJSON with age-adjusted and crude percentages and confidence limits in feature properties.
6. Classify the age-adjusted rates into five quantile classes. Compute exact breaks and class counts from the downloaded data; do not hard-code assumed values.
7. Produce a static SVG map and an interactive HTML map with the same class breaks. The interactive map includes county popups, a crude/age-adjusted selector, Esri basemap choices, and contiguous-U.S., Alaska, and Hawaii views.

## CRS Rationale

- Source health data is tabular and joined using five-character county FIPS/GEOID.
- County polygons are requested in EPSG:4326 for the Leaflet web map.
- The static SVG uses separate Albers equal-area projections for the contiguous U.S., Alaska, and Hawaii inset panels. Insets have separate scales and are labeled as such; the Hawaii frame focuses on the main islands, cropping remote northwestern islands for legibility.
- No distance or area analysis is performed.

## Assumptions and Limitations

- CDC PLACES values are modeled estimates of adult diagnosed coronary heart disease prevalence, not direct county surveys.
- Age-adjusted prevalence supports comparison among counties with different age structures; crude prevalence is included in popups for context.
- The 2024 release is the latest complete nationwide release selected by the user; its estimates represent 2022, not 2024 or 2025 observations.
- Census geometry is a 2026 vintage and may differ from boundaries applicable to the 2022 estimates. The FIPS join will be checked and the vintage disclosed.
- Do not infer causes, individual risk, case counts, or local intervention effectiveness from the map.

## Reproduction

Run `python .\build_map.py` from this project directory with Python 3 and internet access. The script uses only the Python standard library and writes downloaded sources, derived data, map summary, static SVG, and interactive HTML to this directory.
