<p align="center">
  <img src="assets/banner-mapcrew-gis.svg" width="100%">
</p>
MapCrew is a small, staged workflow for turning a geospatial question into a documented, quality-checked analysis and a shareable map. A lead agent, Captain, plans the route, hands work to specialist agents, and checks each handoff.

MapCrew doesn't replace GIS software. It adds a documented, quality-checked workflow on top of open GIS tools, so AI-assisted spatial analysis is reproducible and reviewable.

## Repository Layout

- `agents/` - Captain (orchestrator) plus Scout, Sentinel, Analyst, Cartographer, Web Builder, and Reviewer persona definitions.
- `workflows/` - reusable orchestration guides for quick maps and site selection.
- `templates/` - starter files for project briefs, QA reports, and map specifications.
- `viewer/` - a no-build Leaflet viewer starter that can be opened as a local HTML file.
- `examples/` - a documented open-data example using Natural Earth country boundaries.

## The Crew

| Agent | Responsibility |
|---|---|
| **Captain** | Clarifies the goal, chooses the route, manages handoffs and checkpoints, reports to you |
| **Scout** | Finds and documents candidate datasets |
| **Sentinel** | Checks data quality |
| **Analyst** | Documents the method and runs the analysis |
| **Cartographer** | Designs the map and prepares viewer-ready layers |
| **Web Builder** | Builds the interactive viewer |
| **Reviewer** | Checks reproducibility, licensing, and gives the final go/no-go |

Captain is the first agent you talk to and the last one you hear from. Captain does not do the specialist work.

## Using in VS Code

1. Create a new folder for your project outside this repository, for example `C:\Users\username\my-map-project`.
2. In VS Code, choose **File > Add Folder to Workspace** and add both this MapCrew repository and your new project folder. This lets Copilot Chat read the MapCrew guides while keeping project files separate.
3. Open Copilot Chat and start with the Captain guide at `agents/captain.agent.md`. If Captain is available in the agent picker, select it; otherwise, attach or reference the guide in your chat and ask it to lead the workflow.
4. Tell Captain which folder is your project folder, then describe the map or analysis you want. Ask Captain to put all project outputs in that folder and leave the MapCrew repository unchanged.

## Typical Sequence

1. Start with Captain (`agents/captain.agent.md`). Captain clarifies your question and constraints using `templates/brief-template.md` and saves the result as `project-brief.md`.
2. Captain picks a route, such as `workflows/quick-map.md` or `workflows/site-selection.md`, and records the ordered steps and expected outputs in `workflow-plan.md`. Progress is tracked in `project-state.md` so work can be resumed later.
3. Scout documents candidate sources in `data-sources.md`; verify license, attribution, and coverage before selection.
4. Sentinel checks data quality and records results in `qa-report.md`.
5. Analyst documents the method and CRS in `analysis-plan.md`, then saves and runs the analysis script.
6. Cartographer documents the map in `map-spec.md` and prepares viewer-ready layers.
7. Web Builder creates `viewer.html`.
8. Reviewer records a final go/no-go in `review.md`.
9. Captain delivers the final outputs and a short project summary.

Captain may skip steps that are not needed (for example, Scout when you already have data) and records the reason in `workflow-plan.md`.

Do not skip a failed QA gate or present assumptions as verified facts. Keep source data unchanged; save derived outputs separately and document transformations.

## Checkpoints

Captain pauses to confirm with you after the brief, after data QA, after the analysis, and after the final review. If something unexpected comes up between checkpoints, such as unusable data, implausible results, or a change of scope, Captain stops and asks before continuing.

## Viewer Starter

Open `viewer/viewer.html` directly in a modern browser and choose one or more GeoJSON files. The starter needs no build step. Leaflet and Esri World Topographic Map, World Street Map, and World Imagery (satellite) tiles, plus OpenStreetMap Standard tiles, load from the internet. Attribution for the selected basemap is shown on the map. Follow [Esri's terms](https://goto.arcgisonline.com/maps/World_Topo_Map) or the [OpenStreetMap tile usage policy](https://operations.osmfoundation.org/policies/tiles/); OSM Standard is for normal interactive viewing only, not bulk downloading or offline use. The OSM tile service requires a valid HTTP referrer, which may not be sent when this page is opened directly as a `file://` URL, so host the viewer on a web server when using that option.

## Example

See [`examples/natural-earth-continents/`](examples/natural-earth-continents/) for source notes and a map specification for a categorical continent map. The dataset is not bundled; follow the source instructions there and inspect the downloaded archive metadata before use.
