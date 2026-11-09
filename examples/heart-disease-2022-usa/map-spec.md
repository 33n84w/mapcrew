# Map Specification

## Audience and Purpose

- Primary audience: Local health planning.
- Map purpose / key message: Compare county-level estimates of diagnosed coronary heart disease prevalence among adults across the United States.
- Intended medium and display size: Static SVG national map plus responsive interactive HTML viewer.

## Extent and Projection

- AOI / initial extent: 50 states and the District of Columbia, with separate contiguous-U.S., Alaska, and Hawaii views. The static Hawaii inset focuses on the main islands; remote northwestern islands are outside that frame.
- Display CRS: Leaflet web maps use EPSG:3857; the source GeoJSON is EPSG:4326. Static SVG uses separate Albers equal-area projections for the contiguous U.S., Alaska, and Hawaii.
- Any analysis CRS and transformations to disclose: No distance or area analysis. Census TIGERweb polygons are requested in EPSG:4326 with 0.001-degree generalization for national display. Static panels clip polygons to their frames.

## Layers

| Order | Layer / source | Geometry | Role | Visibility default | Attribution |
|---:|---|---|---|---|---|
| 1 | CDC PLACES 2024 county CHD age-adjusted prevalence, joined to TIGERweb 2026 counties | Polygon | Main choropleth; age-adjusted prevalence percent, estimate year 2022 | Visible | CDC PLACES; U.S. Census Bureau TIGERweb |
| 2 | CDC PLACES 2024 county CHD crude prevalence, joined to the same TIGERweb counties | Polygon | Alternate choropleth for crude prevalence percent | Available from measure selector | CDC PLACES; U.S. Census Bureau TIGERweb |

## Symbology and Classification

| Layer / field | Data type | Encoding | Classification / breaks | Units / labels | Rationale |
|---|---|---|---|---|---|
| `age_adjusted_percent` | Continuous numeric | Sequential blue ramp from pale to dark | Five quantile classes; `≤5.7`, `>5.7–≤6.2`, `>6.2–≤6.6`, `>6.6–≤7.2`, `>7.2` | Percent of adults, 2022 estimate | Primary measure supports comparisons among counties with different age structures. |
| `crude_percent` | Continuous numeric | Same sequential blue ramp, recalculated using crude-rate quantiles | Five quantile classes; `≤7.0`, `>7.0–≤8.0`, `>8.0–≤8.8`, `>8.8–≤9.7`, `>9.7` | Percent of adults, 2022 estimate | Separate breaks avoid reusing age-adjusted classes for the crude measure. |

Colors, from lowest to highest: `#f7fbff`, `#c6dbef`, `#6baed6`, `#2171b5`, `#08306b`. County boundaries use thin white strokes, except the Hawaii static inset uses darker outlines for legibility. Missing estimates use light gray; there are no missing county values in the selected 2024 release.

## Legend and Interaction

- Legend title and entries: Age-adjusted or crude prevalence; five quantile classes with exact break labels and observed range.
- Popup fields and labels: County and state, age-adjusted estimate and 95% CI, crude estimate and 95% CI, adult population, estimate year.
- Layer toggles or filters: Select age-adjusted or crude prevalence; switch among Esri topographic, street, imagery, or no basemap. Alaska and Hawaii are separate map views.
- No-data and uncertainty treatment: Gray no-data style reserved for missing values; show CDC confidence intervals in popups. No county estimates are missing in the selected data.

## Basemap and Attribution

- Basemap/provider or none: Esri World Topographic Map by default; Esri World Street Map, Esri World Imagery, or no basemap are selectable.
- URL/service and terms checked: Esri ArcGIS tile endpoints and map terms links are included in `viewer.html`; requests require internet access.
- Required attribution text: Esri tile attribution appears in each map; Census Bureau and CDC sources are named in the viewer and static map.
- Dataset attribution text: Centers for Disease Control and Prevention, National Center for Chronic Disease Prevention and Health Promotion, Division of Population Health; U.S. Census Bureau TIGERweb.

## Limitations

- Data vintage and scale/resolution: CDC PLACES 2024 release, estimate year 2022; county-level model-based estimates. County boundaries are Census TIGERweb January 1, 2026 vintage and generalized for display.
- Known uncertainty or omissions: Values are model-based estimates with uncertainty; popups show confidence intervals. The selected dataset has all 3,144 county/DC values.
- Interpretation cautions: Age-adjusted prevalence is not a crude population share, case count, individual risk, or causal estimate. CDC cautions that the model cannot detect local-intervention effects.
- Sensitive-location handling: Only aggregate county data is mapped; no individual health records or precise case locations are included.
