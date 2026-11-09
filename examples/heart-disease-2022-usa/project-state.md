# Project State

**Project:** U.S. county coronary heart disease prevalence map

**Last updated:** 2026-11-09

**Status:** Complete; release review is GO WITH LIMITATIONS.

## Completed
- [x] Confirmed project brief, measure, geography, audience, timeframe, and outputs.
- [x] Selected the complete CDC PLACES 2024 release (2022 estimates) instead of the incomplete 2025 release.
- [x] Documented data sources, methods, map specification, and limitations.
- [x] Downloaded and validated CDC estimates and TIGERweb boundaries; matched all 3,144 county/DC areas.
- [x] Generated joined GeoJSON, map summary, static SVG, and interactive HTML viewer.
- [x] Validated value ranges, confidence intervals, key coverage, SVG structure, map rendering, and metric selector.
- [x] Completed QA report and release review.

## Decisions
- Use age-adjusted diagnosed coronary heart disease prevalence among adults as the primary comparison.
- Keep crude prevalence as a separately classified interactive alternate.
- Do not mix estimate years. Use the complete 2024 release consistently for the national map.

## Limitations
- PLACES estimates are modeled and cannot establish causation or individual risk.
- TIGERweb polygons are generalized for display and use a 2026 vintage.
- Topology/self-intersection checks were not run.
- The standalone HTML needs internet access for Leaflet and Esri tile basemaps; the SVG is self-contained.
