# Natural Earth Continents: Quick-Map Example

This example maps world country boundaries using Natural Earth's 1:110m Admin 0 Countries data, categorized by continent. It demonstrates source checks, GeoJSON preparation, and the map specification. The source dataset is not bundled in this repository.

## Source Check

See [data-sources.md](data-sources.md) before downloading. Natural Earth's terms state that its raster and vector map data are public domain, but the terms also describe exceptions for some third-party contributions. Inspect the downloaded archive's metadata and notices before reuse.

## Prepare the Layer

1. Download the 1:110m Admin 0 Countries dataset from the official Natural Earth source linked in `data-sources.md`.
2. Inspect the archive and confirm it is the expected countries layer. Check its CRS, fields, coverage, and any included license or source notices.
3. Convert the shapefile to RFC 7946-style GeoJSON in WGS 84 longitude/latitude with GDAL/OGR:

   ```sh
   ogr2ogr -f GeoJSON countries.geojson ne_110m_admin_0_countries.shp -t_srs EPSG:4326
   ```

4. Open `viewer.html` in this folder. It auto-loads `data/countries.geojson`, applies the continent palette from [map-spec.md](map-spec.md), and includes legend, popup, layer toggle, and global extent controls.
5. If you use a different countries file, verify field names for country and continent and keep attribution aligned with `data-sources.md`.

The viewer starter does not automatically implement this example's category palette; customize its style using the map specification. The map is a generalized global overview, not a source for local boundaries or precise area measurements.