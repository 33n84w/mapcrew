# Site Selection Workflow

Use this workflow when comparing candidate locations against multiple spatial criteria. Treat the result as decision support, not as an automatic site recommendation.

## Inputs

- Decision question and intended decision-maker
- AOI and candidate-site definition
- Mandatory constraints and exclusion zones
- Criteria, units, relative importance, and acceptable thresholds
- Time range, resolution, audience, and legal or ethical constraints

If the user has not supplied criterion definitions or weights, do not invent authoritative preferences. Offer transparent alternatives and ask which to use.

## Steps

1. **Define the decision.** Use `templates/brief-template.md`. Separate hard constraints from preferences; identify affected communities, protected areas, and sensitive locations.
2. **Source the inputs.** Scout documents and compares datasets in `data-sources.md`. Verify license, attribution, AOI and temporal coverage, scale/resolution, update frequency, and limitations.
3. **Check quality.** Sentinel records CRS, geometry, nulls, duplicates, topology, and outliers in `qa-report.md`. Resolve failures that could change suitability rankings before proceeding.
4. **Specify the model.** Analyst documents criteria, units, thresholds, normalization, weights, constraints, missing-data treatment, resolution, and a suitable projected CRS in `analysis-plan.md` before execution.
5. **Run a reproducible analysis.** Script each transformation and scoring step. Preserve input data and write intermediate and final layers to separate outputs. Record software versions and parameters.
6. **Test sensitivity.** Compare reasonable alternative weights, thresholds, or input datasets. Report whether candidate rankings change and identify criteria driving instability.
7. **Map responsibly.** Cartographer distinguishes excluded, eligible, and ranked areas without implying more precision than the inputs support. Show criteria, units, breaks, source dates, uncertainty, and limitations.
8. **Build and review.** Web Builder packages the viewer. Reviewer checks reproducibility, licenses, attribution, sensitive-location risks, unsupported claims, QA failures, and whether uncertainty is visible.

## Required Outputs

- `data-sources.md`, `qa-report.md`, and `analysis-plan.md`
- Re-runnable scripts and intermediate/final result layers
- A sensitivity summary alongside the suitability result
- `map-spec.md`, `viewer.html`, and `review.md`

## Interpretation Guardrails

- A high score is relative to the chosen criteria and weights; it is not proof that a site is safe, feasible, equitable, or legally available.
- Report exclusions and missing data as well as preferred candidates.
- Do not publish exact sensitive locations unless sharing is authorized and risks have been assessed.