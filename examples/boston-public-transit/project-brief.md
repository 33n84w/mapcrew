# Boston Public Transportation Routes

## Question

Create a public map of scheduled Boston-area MBTA public transportation routes,
categorized by GTFS route type.

## Area of Interest

- Greater Boston and MBTA service area
- EPSG:4326 / WGS 84 route geometries

## Time

- Use the current MBTA GTFS feed available when rebuilt
- The feed validity dates and version should be recorded in `map-summary.json`

## Resolution and Units

- Route-level LineStrings derived from GTFS shapes
- Coordinates are decimal degrees

## Audience and Purpose

- Public audiences seeking to compare major public transportation modes
- Intended for overview and exploration, not real-time navigation

## Data and Constraints

- Official MBTA GTFS feed
- Scheduled geometry, not live vehicle locations
- Do not present the map as a real-time service-status tool
- Confirm current redistribution terms before a public data redistribution

## Method Preferences

- GTFS `route_type` categories:
  - Tram/light rail
  - Subway
  - Commuter rail
  - Bus
  - Ferry
- Douglas-Peucker simplification for browser performance

## Deliverables

- Categorized GeoJSON route layers
- A no-build Leaflet viewer
- Rebuild script and source metadata
- A summary of route and shape coverage
