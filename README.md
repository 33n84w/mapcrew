# Geopilot

Geopilot is a small, staged workflow for turning a geospatial question into a documented, quality-checked analysis and a shareable map.

## Repository Layout

- `agents/` - Scout, Sentinel, Analyst, Cartographer, Web Builder, and Reviewer persona definitions.
- `workflows/` - reusable orchestration guides for quick maps and site selection.
- `templates/` - starter files for project briefs, QA reports, and map specifications.
- `viewer/` - a no-build Leaflet viewer starter that can be opened as a local HTML file.
- `examples/` - a documented open-data example using Natural Earth country boundaries.

## Typical Sequence

1. Define the question and constraints with `templates/brief-template.md`.
2. Follow `workflows/quick-map.md` or `workflows/site-selection.md`.
3. Scout documents candidate sources in `data-sources.md`; verify license, attribution, and coverage before selection.
4. Sentinel checks data quality and records results in `qa-report.md`.
5. Analyst documents the method and CRS in `analysis-plan.md`, then saves and runs the analysis script.
6. Cartographer documents the map in `map-spec.md` and prepares viewer-ready layers.
7. Web Builder creates `viewer.html`; Reviewer records a final go/no-go in `review.md`.

Do not skip a failed QA gate or present assumptions as verified facts. Keep source data unchanged; save derived outputs separately and document transformations.

## Viewer Starter

Open `viewer/viewer.html` directly in a modern browser and choose one or more GeoJSON files. The starter needs no build step or API key. Leaflet and OpenStreetMap tiles are loaded from public internet services, so an internet connection is required for the map library and basemap. OpenStreetMap attribution is included; respect the tile service usage policy and use an appropriate provider for production or high-volume use.

## Example

See [`examples/natural-earth-continents/`](examples/natural-earth-continents/) for source notes and a map specification for a categorical continent map. The dataset is not bundled; follow the source instructions there and inspect the downloaded archive metadata before use.
