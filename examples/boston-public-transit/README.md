# Boston Public Transportation Routes

This MapCrew example maps scheduled MBTA public transportation routes and
categorizes them by GTFS route type.

## Open the Map

Open `viewer.html` directly in a modern browser. It embeds the route data in
`routes.js`, so no local server or API key is required. An internet connection
is required for Leaflet and the selected basemap tiles.

## Categories

- Subway
- Light rail
- Commuter rail
- Bus
- Ferry

The route display is based on scheduled GTFS shape geometry. It is not live
vehicle information and must not be used for real-time navigation or service
status decisions.

## Rebuild

Requires Python 3 and internet access. No third-party Python packages are needed.

```powershell
Set-Location C:\Users\zhana\mapcrew\examples\boston-public-transit
py .\build_routes.py
```

The script downloads the current official MBTA GTFS feed and rewrites the bundled
GeoJSON and `routes.js`.

## Files

- `build_routes.py` - download and rebuild script
- `data/MBTA_GTFS.zip` - bundled feed snapshot
- `data/boston-public-transit-routes.geojson` - combined route geometry
- `data/routes-*.geojson` - category-specific route geometry
- `routes.js` - browser-embedded combined data
- `viewer.html` - interactive categorized map
- `map-summary.json` - feed metadata and route/shape counts
- `project-brief.md`, `analysis-plan.md`, `data-sources.md` - project documentation
- `qa-report.md`, `review.md` - validation and release notes
