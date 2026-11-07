# Data Sources: Natural Earth Continents Example

## Candidate

| Dataset | Source | License / attribution | CRS | Format | Coverage | Update frequency | Limitations |
|---|---|---|---|---|---|---|---|
| Admin 0 - Countries, 1:110m Cultural Vectors | [Official Natural Earth download page](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/) | Natural Earth's [terms of use](https://www.naturalearthdata.com/about/terms-of-use/) state Natural Earth raster and vector data are public domain. The terms note exceptions for some third-party contributions; inspect archive metadata/notices. Attribute Natural Earth and any component sources identified in the archive. | Expected WGS 84 geographic coordinates; verify the downloaded layer metadata before conversion. | Official download is a GIS archive; convert the country layer to GeoJSON for the viewer. | Global country coverage; verify the downloaded layer extent. | Irregular releases; no fixed update cadence stated here. Check the source page for the current release date. | Generalized for 1:110m scale; not suitable for local boundary detail. Boundaries and disputed areas reflect source conventions and may not represent legal positions. Country polygons crossing the antimeridian need viewer-aware handling. |

## Verification Notes

- License page checked: 2026-11-07. It states Natural Earth data are public domain and lists exceptions for particular third-party contributions; check the selected archive's notices before redistribution.
- Coverage and CRS must be verified against the downloaded archive before recommending it for any other AOI or measurement task.
- Attribution in this example: `Data: Natural Earth (public domain); see archive notices for third-party contributions.` Update this text if archive metadata requires additional attribution.