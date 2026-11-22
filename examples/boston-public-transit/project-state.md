# Project State

**Project:** Boston Public Transportation Routes
**Last updated:** 2026-11-22
**Current step:** Complete

## Progress

- [x] Brief confirmed
- [x] MBTA GTFS source documented
- [x] Route shape join and geometry QA
- [x] Categorized GeoJSON generated
- [x] Leaflet viewer created
- [x] Final review recorded

## Decisions

- 2026-11-22: Use official MBTA GTFS scheduled route geometry.
- 2026-11-22: Categorize with GTFS route types 0 through 4.
- 2026-11-22: Embed combined route data in `routes.js` for direct browser use.
- 2026-11-22: Label the result as overview/scheduled geometry, not live service.

## Open issues

- Redistribute rights: confirm applicable MBTA GTFS reuse terms before public redistribution.
- Route coverage: 31 route records have no usable shape in the bundled snapshot.
