# Boston Public Transportation Data Sources

| Source | URL | Use | Coverage | Format | License / terms |
|---|---|---|---|---|---|
| Massachusetts Bay Transportation Authority (MBTA) GTFS | https://cdn.mbta.com/MBTA_GTFS.zip | Scheduled routes, route names, route types, shape geometries, and feed validity | Greater Boston MBTA service area | GTFS ZIP | Official MBTA feed. Confirm current data redistribution terms before public redistribution. |
| Esri World Street Map, World Topographic Map, or World Imagery | https://www.arcgis.com/home/item.html?id=3b93337983e9436f8db950e38a8629af | Optional basemap | Global, subject to Esri terms | Web tiles | Esri terms and attribution are required |

## Snapshot

The bundled feed was downloaded on 2026-11-22. It reports:

- Publisher: MBTA
- Feed start: 2026-11-12
- Feed end: 2026-12-12
- Feed version: Fall 2026, 2026-11-19T01:01:13+00:00, version D

The downloaded archive is retained at `data/MBTA_GTFS.zip`. The live rebuild
script downloads the current feed, so exact route geometry can change after the
bundled snapshot was created.
