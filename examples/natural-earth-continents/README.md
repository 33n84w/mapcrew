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

4. Open `../../viewer/viewer.html`, load `countries.geojson`, and set the data attribution as documented in `data-sources.md`.
5. Apply the categorical treatment in [map-spec.md](map-spec.md). Do not use the continent colors as an ordered scale.

The viewer starter does not automatically implement this example's category palette; customize its style using the map specification. The map is a generalized global overview, not a source for local boundaries or precise area measurements.