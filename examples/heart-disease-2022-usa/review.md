# Release Review

## Decision

**GO WITH LIMITATIONS** for a local health-planning comparison of modeled county-level prevalence. The selected CDC PLACES 2024 release provides complete 2022 estimates for all 3,144 U.S. county and county-equivalent areas, and the health-data keys match the TIGERweb polygons exactly.

## Verified Outputs

- [Static map](./heart_disease_map.svg): 3,144 county paths; the contiguous U.S. is shown with separate Alaska and focused main-Hawaii insets.
- [Interactive viewer](./viewer.html): county maps, age-adjusted/crude selector with separate quantile breaks, county popups, and Esri basemap choices.
- [Derived data](./data/county_chd_prevalence.geojson): 3,144 joined county features.
- [Build script](./build_map.py): reproduces the downloaded sources, derived layer, summary, SVG, and HTML viewer.

The static SVG passed XML parsing and visual browser review. The standalone HTML opened outside VS Code, and browser checks confirmed that changing the metric updates its legend and observed range. Esri tiles and Leaflet are loaded online; selecting no basemap leaves the embedded county data available.

## Required Interpretation

- State the release and estimate year separately: CDC PLACES 2024 release; 2022 estimates.
- The measure is adult diagnosed coronary heart disease prevalence. Age-adjusted rates are the primary comparison; crude rates are included as an alternate view.
- Estimates are model-based and are not direct county surveys. Do not interpret them as individual risk, case counts, causal evidence, or intervention effectiveness.
- County boundaries are generalized TIGERweb 2026 polygons, not survey-grade geometry. The static Hawaii inset focuses on the main islands; remote northwestern islands are cropped from that frame.
- Preserve source attribution and the 95% confidence intervals shown in interactive county popups.

## Remaining Limitation

The workflow checks polygon structure, coordinates, feature counts, and joins, but does not test topology or self-intersections. The selected release is one vintage older than the incomplete 2025 release; do not fill its values from another year.
