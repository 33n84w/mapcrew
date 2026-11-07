# Quick Map Workflow

Use this workflow for a focused question that can be answered with a small number of established datasets and one clear map.

## Inputs

- A project brief with question, area of interest (AOI), time range, required resolution, intended audience, and constraints
- Available data, if any

## Steps and Gates

1. **Define the task.** Complete `templates/brief-template.md`. Resolve material ambiguity in the question, AOI, dates, units, or audience before choosing data.
2. **Scout sources.** Compare at least two suitable candidates when possible. Record source URLs, licenses, attribution, CRS, format, coverage, update frequency, and limitations in `data-sources.md`. Do not recommend candidates with unverified license or AOI coverage.
3. **Review data quality.** Inspect the selected layers and write `qa-report.md` using `templates/qa-report-template.md`. Record counts and examples. Block analysis when a failure makes the result unreliable; document any approved exception.
4. **Plan analysis.** Write `analysis-plan.md` with method, assumptions, CRS rationale, inputs, parameters, and limitations before running the analysis. Use a suitable projected CRS for distance or area.
5. **Run reproducibly.** Save and run a script; keep source data unchanged and write derived layers separately. Record dependencies, versions, commands, and output paths.
6. **Design the map.** Write `map-spec.md` using `templates/map-spec-template.md`. Match symbology and classification to the data and audience; include legend, units, sources, attribution, and limitations.
7. **Build the viewer.** Produce `viewer.html`, with layer toggles, useful popups, a basemap option, and complete attribution. Ensure file-open limitations and network requirements are clear.
8. **Review before sharing.** Reviewer checks reproducibility, rights, sensitive locations, claims, QA failures, and viewer behavior; record `GO` or `NO-GO` in `review.md`.

## Expected Handoff Chain

`Brief -> Scout -> Sentinel -> Analyst -> Cartographer -> Web Builder -> Reviewer -> User`

At each handoff, pass the artifact paths, assumptions, unresolved questions, and limitations. A handoff is not evidence that the next stage has completed its work.

## Minimum Deliverables

- `data-sources.md`
- `qa-report.md`
- `analysis-plan.md` and runnable analysis script(s)
- Result layer(s)
- `map-spec.md`, viewer-ready GeoJSON/style configuration, and `viewer.html`
- `review.md` with an explicit release decision