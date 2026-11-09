# Workflow Plan

## Goal

Map the latest complete nationwide county-level adult diagnosed coronary heart disease prevalence available to this project, for local health planning.

## Route

| Step | Role | Work | Expected output | Gate |
|---:|---|---|---|---|
| 1 | Captain | Confirm brief and document the selected release and scope | `project-brief.md`, `workflow-plan.md` | User approved the brief and chose 2024 release |
| 2 | Scout | Compare 2025 and 2024 CDC PLACES releases and Census county boundaries | `data-sources.md` | Sources, coverage, license, attribution, and data years documented |
| 3 | Sentinel | Validate estimate coverage, missing values, FIPS keys, geometry, and data/geometry join | `qa-report.md` | Stop on a failed check; do not silently repair or substitute values |
| 4 | Analyst | Fetch source data; calculate and save the county choropleth inputs reproducibly | `analysis-plan.md`, `build_map.py`, `data/` | Preserve raw inputs; log transformations and output paths |
| 5 | Cartographer | Specify a readable national county choropleth with a suitable classification and uncertainty disclosures | `map-spec.md` | Legend, units, data vintage, no-data handling, and attribution are explicit |
| 6 | Web Builder | Build static and interactive map deliverables | `heart_disease_map.svg`, `viewer.html` | Verify direct local-file opening, route-independent basemap behavior, and interactions |
| 7 | Reviewer | Review data claims, attribution, reproducibility, privacy, and rendered outputs | `review.md` | Explicit `GO` or `NO-GO` |

## Decisions

- Use CDC PLACES 2024 county data because it contains values for all 3,144 U.S. county-equivalent areas; the newer 2025 release omits all 120 Kentucky and 67 Pennsylvania counties and suppresses Loving County, Texas.
- The mapped measure is age-adjusted diagnosed coronary heart disease prevalence among adults, in percent. Keep crude prevalence and confidence intervals in the source data for popups and interpretation.
- Use only aggregate county-level data; do not use patient-level records.
- Join CDC county FIPS identifiers to Census county GEOIDs. Census TIGERweb layer 13 currently provides January 1, 2026 county geometry; retain and disclose that geography vintage.
- Produce a static SVG and an interactive HTML viewer. Use Esri World Topographic Map tiles for the interactive viewer, with attribution; the viewer requires internet access.
- Do not blend estimates from different PLACES releases.

## Known Risks and Limitations

- PLACES estimates are modeled, not direct county surveys. They should not be used to infer causes, individual risk, or local intervention effectiveness.
- Age-adjusted prevalence is for comparison across age structures; it is not the observed crude share or an estimate of case counts.
- The selected 2024 release represents 2022 estimates, not data measured in 2025.
- The boundary vintage (2026) differs from the estimate vintage (2022); verify all FIPS joins and disclose this difference.
