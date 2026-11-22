# Analysis Plan

## Question

Map the scheduled MBTA route network and classify each route feature by GTFS
`route_type`.

## Method

1. Download the official MBTA GTFS ZIP feed.
2. Read `routes.txt`, `trips.txt`, `shapes.txt`, and `feed_info.txt`.
3. Join each `shape_id` to its route(s) through `trips.txt`.
4. Join route names and types through `routes.txt`.
5. Sort shape points by `shape_pt_sequence`.
6. Simplify each line with Douglas-Peucker at epsilon 0.00025 decimal degrees.
7. Write combined and category-specific GeoJSON FeatureCollections.
8. Embed the combined data in `routes.js` for direct browser opening.

## CRS

GTFS coordinates are longitude/latitude on WGS 84. They remain EPSG:4326.
Leaflet transforms coordinates to its Web Mercator display projection.

No distance or area calculations are performed, so no projected CRS is required.

## Assumptions and Limitations

- Multiple trips can use the same shape.
- Bus networks include 371 route records in the inspected feed, but route records
  may have no usable shape geometry.
- Simplification changes line detail but preserves the route path at an overview
  scale.
- The feed is scheduled route geometry; it does not show disruptions, detours,
  or real-time vehicle movement.

## Reproducibility

The rebuild script downloads the live feed, so future output may differ from the
bundled snapshot. Record or retain the downloaded ZIP to preserve exact inputs.
