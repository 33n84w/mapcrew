# QA Report

## Review Scope

- Project: U.S. county prevalence map of diagnosed coronary heart disease among adults.
- Review date: 2026-11-09.
- Selected estimates: CDC PLACES 2024 County Data, estimate year 2022.
- Boundaries: U.S. Census Bureau TIGERweb county layer 13, January 1, 2026 vintage.
- Validation: Build script checks, Python standard-library data/XML checks, and browser rendering of the interactive and static outputs.

## Dataset Inventory

| Dataset / layer | Format | Features / rows | Coverage | Notes |
|---|---|---:|---|---|
| CDC PLACES 2024 CHD estimates | CSV | 6,288 rows: 3,144 age-adjusted and 3,144 crude | All U.S. counties and county equivalents, including DC | All selected estimate values are for 2022. |
| TIGERweb counties, layer 13 | GeoJSON | 3,144 polygons | 50 states and DC | EPSG:4326; 0.001-degree generalization requested for display. |
| Derived county CHD layer | GeoJSON | 3,144 features | Exact one-to-one coverage with the selected health estimates and TIGERweb polygons | Contains both measures, confidence limits, population, and source year. |
| Interactive viewer | HTML | 3,144 mapped county features in each applicable view | Contiguous U.S., Alaska, and Hawaii | Leaflet and selected Esri tiles require internet access; county data and geometry are embedded. |
| Static map | SVG | 3,144 county paths | Contiguous U.S. plus Alaska and Hawaii insets | Hawaii inset focuses on the main islands; remote northwestern islands are outside the inset frame. |

## Checks

| Area | Check | Status | Result |
|---|---|---|---|
| Source estimates | Row keys, measure types, and years | PASS | 6,288 unique county/measure keys; 3,144 rows for each measure; every row is a 2022 estimate. |
| Source estimates | Values and confidence intervals | PASS | All prevalence values are within 0–100%; all reported confidence intervals contain their corresponding estimates. |
| Source estimates | Age-adjusted range and distribution | PASS | 4.1–11.7%; median 6.4%; quantile breaks 5.7%, 6.2%, 6.6%, and 7.2%; class counts 673, 701, 543, 608, and 619. |
| Source estimates | Crude range and distribution | PASS | 3.4–14.9%; median 8.4%; independent quantile breaks 7.0%, 8.0%, 8.8%, and 9.7%; class counts 638, 654, 643, 621, and 588. |
| TIGERweb geometry | Feature identity and basic structure | PASS | 3,144 unique GEOIDs; 3,093 Polygon and 51 MultiPolygon features; 51 state/DC codes; geometries have supported polygon types and valid coordinate ranges. |
| Join | Estimate and geometry key coverage | PASS | The three FIPS/GEOID sets match exactly; no duplicate, missing, or unmatched county keys. |
| Derived layer | Feature and estimate integrity | PASS | 3,144 unique county FIPS; all mapped values are present and within 0–100%; both measures and their confidence limits are retained. |
| Static SVG | XML structure and map paths | PASS | XML parses; 3,144 county paths are present. The inset frames clip remote geometry outside their display extents. |
| Static SVG | Visual layout | PASS | Browser preview confirms legible title, legend, contiguous-U.S. map, Alaska inset, and focused Hawaii inset without title overlap. |
| Interactive HTML | Local-file rendering and metric selector | PASS | Opens outside VS Code; county maps render; switching to crude prevalence updates both class breaks and range to 3.4–14.9%. |
| Interactive HTML | Basemap choices and attribution | PASS | Esri topographic tiles and attribution render; street, imagery, and no-basemap choices are present. Tile-backed options require internet access. |

## Findings and Limitations

- The 2025 CDC PLACES release was not used because it has no county CHD rows for all 120 Kentucky counties and all 67 Pennsylvania counties; Loving County, Texas is suppressed. The complete 2024 release avoids a mixed-vintage map and covers all 3,144 county/DC areas.
- TIGERweb geometry is generalized for national display, is not survey-grade, and uses a 2026 boundary vintage that may differ from boundaries applicable to the 2022 estimates.
- Topology and self-intersection validity were not tested. No geometry repair or silent omission is performed by the build script.
- PLACES estimates are modeled, not direct county surveys. They should not be interpreted as causal evidence, individual risk, case counts, or local intervention effects.
- The standalone interactive viewer embeds the county data but loads Leaflet and Esri tiles online. The static SVG is self-contained.

## Readiness

- Overall: `GO WITH LIMITATIONS` for local health-planning context and county-level comparison.
- Release conditions: Retain the estimate year, release, boundary vintage, attribution, and interpretation caveats in any reuse. Do not mix 2025 and 2024 estimates.
- No blocking data-coverage, join, or rendering issues remain.
