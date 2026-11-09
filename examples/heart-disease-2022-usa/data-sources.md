# Data Sources

Checked 2026-11-09 for a national county map of adult diagnosed coronary heart disease prevalence. The primary comparison field is age-adjusted prevalence (percent), which is more appropriate for comparing counties with different age structures than crude prevalence.

## Candidate health estimates

| Candidate | Source and URL | License / attribution | CRS / format | Coverage and time | Fit and limitations |
|---|---|---|---|---|---|
| CDC PLACES, County Data, 2025 release | [Dataset](https://data.cdc.gov/d/swc5-untb); [Socrata API](https://data.cdc.gov/resource/swc5-untb.json) | CDC catalog identifies `PUBLIC_DOMAIN`. Dataset attribution: Centers for Disease Control and Prevention, National Center for Chronic Disease Prevention and Health Promotion, Division of Population Health. | Tabular JSON/CSV; `LocationID` is the county FIPS identifier; no polygon geometry. | 50 states and DC; the release uses 2023 BRFSS for this measure. The dataset metadata describes model-based estimates at county, place, tract, and ZCTA levels. | Latest release and exact measure match. QA found no county rows for Kentucky (120 counties) or Pennsylvania (67 counties); Loving County, Texas is present with its estimate suppressed because population is under 50. Only 2,956 of 3,144 county estimates have values, so this release cannot provide complete national coverage. |
| CDC PLACES, County Data, 2024 release | [Dataset](https://data.cdc.gov/d/fu4u-a9bh); [Socrata API](https://data.cdc.gov/resource/fu4u-a9bh.json) | CDC catalog identifies `PUBLIC_DOMAIN`. Same CDC attribution as the 2025 release. | Tabular JSON/CSV; `LocationID` is the county FIPS identifier; no polygon geometry. | 50 states and DC; CHD estimate year is 2022, based on the 2024 release. | Same measure and county geography. Query returned 3,144 county estimates, all with values. Complete national coverage, but one release older than the 2025 dataset. Recommended if complete, same-vintage county comparison is required. |

Both PLACES releases contain model-based local estimates, not direct county surveys. The CDC dataset description warns that the small-area model cannot detect local-intervention effects and cautions against program or policy evaluation. Treat differences as estimated prevalence patterns, not causal evidence or individual risk.

## Supporting geography

| Dataset | Source and URL | License / attribution | CRS / format | Coverage and time | Limitations |
|---|---|---|---|---|---|
| U.S. Census Bureau TIGERweb, States and Counties, Counties layer (layer 13) | [TIGERweb county layer](https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/13) | U.S. Census Bureau source; retain Census Bureau attribution in derived map materials. | Polygon features; downloaded as GeoJSON in EPSG:4326. Join on five-character `GEOID` / county FIPS. | Service layer reports a January 1, 2026 boundary vintage. Contains 3,144 state/DC county-equivalent features when territories are excluded. | Used only as boundaries, not as health data. Requested 0.001-degree generalization for national display; not survey-grade boundary geometry. Boundary vintage differs from the PLACES estimate year. |

## Selection status

The user selected the complete 2024 PLACES release. Use its 2022 estimates consistently for all counties; do not fill gaps in the 2025 release from another vintage. The 2024 release is one release older but provides values for all 3,144 county/DC geographies. The derived layer was validated against all 3,144 TIGERweb county/DC GEOIDs.
