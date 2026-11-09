# U.S. County Heart Disease Prevalence: 2022

This MapCrew example maps modeled prevalence of diagnosed coronary heart disease among adults across all 3,144 U.S. counties and county-equivalent areas in the 50 states and District of Columbia. It supports county-level comparison and local health-planning context.

The estimates represent **2022**, from the **CDC PLACES 2024 release**. The complete 2024 release was selected because the newer 2025 release lacked CHD estimates for Kentucky and Pennsylvania and suppressed one Texas county value. Estimates from different releases are not mixed.

## Open the Maps

- **[Interactive viewer](./viewer.html):** Download or clone this example, then open `viewer.html` in a web browser outside VS Code. Select age-adjusted or crude prevalence, click counties for estimates and 95% confidence intervals, and choose Esri topographic, street, imagery, or no basemap. Alaska and Hawaii have separate views.
- **[Static map](./heart_disease_map.svg):** Open the SVG in a browser or compatible image application. It shows age-adjusted prevalence with Alaska and Hawaii insets and is self-contained.

The interactive viewer embeds county geometry and estimates, so no local server is required. Internet access is still required to load Leaflet and any selected Esri tiles; choosing no basemap does not make the viewer fully offline.

## Data and Map Design

| Component | Source / method |
|---|---|
| Health estimates | CDC PLACES 2024 County Data; CHD measure; 2022 age-adjusted and crude prevalence percentages |
| County boundaries | U.S. Census Bureau TIGERweb, January 1, 2026 vintage; EPSG:4326; generalized for national display |
| Join | Five-character county FIPS / GEOID; all 3,144 areas matched |
| Classification | Five quantile classes, calculated separately for age-adjusted and crude prevalence |
| Primary comparison | Age-adjusted prevalence, to compare counties with different age structures |

Age-adjusted estimates range from **4.1% to 11.7%**; crude estimates range from **3.4% to 14.9%**. Darker blue indicates higher prevalence within the selected measure's classes. Switching measures also changes the class breaks.

See [data sources](./data-sources.md) for source links and attribution, and the [map specification](./map-spec.md) for styling, class breaks, and interactions.

## Rebuild

Requires Python 3 and internet access. No third-party Python packages are needed.

From the repository root in PowerShell:

```powershell
Set-Location .\examples\heart-disease-2022-usa
python .\build_map.py
```

The script downloads CDC estimates and TIGERweb boundaries, validates coverage and the join, and overwrites the bundled source data and generated outputs. Live upstream services may change; retain the bundled files when the exact reviewed snapshot is needed.

## Project Files

| File | Purpose |
|---|---|
| [build_map.py](./build_map.py) | Download, validation, join, classification, and map generation |
| [data/places_chd_2024.csv](./data/places_chd_2024.csv) | Downloaded age-adjusted and crude CHD estimates |
| [data/us_counties_tigerweb_2026.geojson](./data/us_counties_tigerweb_2026.geojson) | Downloaded generalized county polygons |
| [data/county_chd_prevalence.geojson](./data/county_chd_prevalence.geojson) | Joined county geometry and health estimates |
| [map-summary.json](./map-summary.json) | Counts, ranges, class breaks, and source metadata |
| [project-brief.md](./project-brief.md) | Scope, audience, and acceptance criteria |
| [analysis-plan.md](./analysis-plan.md) | Preparation method and projection rationale |
| [workflow-plan.md](./workflow-plan.md) | MapCrew workflow |
| [qa-report.md](./qa-report.md) | Completed validation checks and limitations |
| [review.md](./review.md) | Release decision and interpretation requirements |
| [project-state.md](./project-state.md) | Completion status |

## Limitations

- PLACES estimates are modeled, not direct county surveys. They do not establish individual risk, case counts, causation, or local intervention effectiveness.
- Age-adjusted prevalence is a standardized comparison measure, not the crude share of adults with the condition. Confidence intervals are available in county popups.
- The generalized 2026 county boundaries differ in vintage from the 2022 estimates and are not survey-grade. Topology and self-intersection checks were not performed.
- Static insets use different scales. The Hawaii inset focuses on the main islands and crops remote northwestern islands.
- Preserve CDC, Census Bureau, and applicable Esri attribution when reusing the outputs.
