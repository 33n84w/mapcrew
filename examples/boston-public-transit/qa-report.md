# QA Report

## Scope

Review the bundled MBTA GTFS snapshot, generated category-specific GeoJSON,
combined route GeoJSON, and embedded browser data.

## Dataset Inventory

| Output | Count |
|---|---:|
| Combined route shape features | 1,150 |
| Subway shape features | 30 |
| Light rail shape features | 37 |
| Commuter rail shape features | 79 |
| Bus shape features | 967 |
| Ferry shape features | 37 |

## Checks

| Check | Status | Evidence |
|---|---|---|
| Source feed readable | PASS | 402 routes and 1,150 route shape features rebuilt from the downloaded GTFS ZIP |
| Category coverage | PASS | All five GTFS route categories used by the feed are represented |
| EPSG/longitude-latitude range | PASS | Route coordinates are WGS 84 and pass longitude/latitude bounds |
| Line geometry | PASS | Combined output has no empty or invalid line coordinates |
| Shape join | PASS | 371 route records have at least one shape; 31 route records have no usable shape |
| Viewer data embedding | PASS | `routes.js` contains the same 1,150 combined features |
| Live schedule accuracy | WARN | GTFS is scheduled geometry; it is not live vehicle location or service-status data |
| Redistribution rights | WARN | MBTA feed terms should be confirmed before public redistribution |
| Route detail | WARN | Lines are simplified at 0.00025 degrees for browser performance |

## Remaining Gaps

- Some route records have no shape geometry and cannot appear on the map.
- The 31 route records without shapes include generic shuttle and elevator
  routes plus route `195`; these are not silently represented as empty lines.
- The bundled snapshot is valid for the documented feed dates and may become
  stale.
