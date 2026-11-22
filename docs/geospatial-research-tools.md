# Geospatial Research and Analysis Reference

This reference lists GitHub repositories for tools that MapCrew agents can use
for geospatial research, data quality checks, spatial analysis, remote sensing,
and map delivery. It is a starting point, not a recommendation to install every
project or bypass source licensing, dataset terms, and reproducibility checks.

Last curated: 2026-11-22.

## Agent-to-tool map

| MapCrew agent | Useful repositories | Primary use |
|---|---|---|
| Scout | Awesome-Geospatial, PySTAC, pystac-client, OSMnx, geopy | Discover sources, search catalogs, and find places or networks |
| Sentinel | GeoPandas, Fiona, Shapely, Rasterio, GDAL, PostGIS, H3 | Inspect schemas, geometry validity, CRS, coverage, resolution, and storage |
| Analyst | GeoPandas, Shapely, PySAL, OSMnx, Rasterio, rioxarray, PySTAC, H3, PostGIS | Run vector, raster, statistical, network, and database analysis |
| Cartographer | MapLibre GL JS, Leaflet, OpenLayers, Turf, QGIS | Build static or interactive maps and derive presentation layers |
| Web Builder | MapLibre GL JS, Leaflet, OpenLayers, Turf | Add viewer controls, interactivity, drawing, and client-side analysis |
| Reviewer | QGIS, GDAL, PostGIS, Ruff or test-framework repositories used with scripts | Reproduce checks and confirm that outputs preserve the documented method |

## Discovery and catalogs

| Repository | Best for | Notes |
|---|---|---|
| [sacridini/Awesome-Geospatial](https://github.com/sacridini/Awesome-Geospatial) | Broad geospatial catalog | Use as a research index, then verify every source and project before recommending it. |
| [stac-utils/pystac](https://github.com/stac-utils/pystac) | Reading and constructing STAC catalogs | Useful for satellite and Earth-observation asset metadata. |
| [stac-utils/pystac-client](https://github.com/stac-utils/pystac-client) | Searching STAC APIs | Good for finding imagery by location, date, collection, and cloud cover. |
| [gboeing/osmnx](https://github.com/gboeing/osmnx) | OpenStreetMap features and street networks | Supports network modeling, routing context, and urban geography. Check the Overpass/OpenStreetMap usage policy. |
| [geopy/geopy](https://github.com/geopy/geopy) | Geocoding interfaces | Compare providers and record terms, attribution, quotas, cache behavior, and result quality. |
| [jltobias/JupyterLite-Population-Data-Comparison](https://github.com/jltobias/JupyterLite-Population-Data-Comparison) | Browser-based population data comparison | Example of combining JupyterLite, demographic data, and geographic comparison workflows. Review source data, methodology, and licensing before reuse. |
| [jltobias/JupyterLite-Sea-Level-Rise](https://github.com/jltobias/JupyterLite-Sea-Level-Rise) | Browser-based sea-level-rise analysis | Example of geospatial coastal-risk and scenario analysis in JupyterLite. Verify sea-level, elevation, shoreline, and projection sources before reuse. |
| [PHI-Case-Studies/1854-Cholera-Outbreak-London-Advanced-1](https://github.com/PHI-Case-Studies/1854-Cholera-Outbreak-London-Advanced-1) | Historical cholera outbreak analysis | Advanced Jupyter Notebook case study of the 1854 London cholera outbreak. Useful for spatial epidemiology, point-pattern analysis, and historical public-health map examples; verify source data and case-study assumptions before reuse. |
| [PHI-Case-Studies/1854-Cholera-Outbreak-London-Advanced-2](https://github.com/PHI-Case-Studies/1854-Cholera-Outbreak-London-Advanced-2) | Historical cholera outbreak analysis | Advanced Jupyter Notebook case study of the 1854 London cholera outbreak. Useful for spatial epidemiology, public-health analysis, and historical map examples; verify source data and case-study assumptions before reuse. |
| [PHI-Case-Studies/1854-Cholera-Outbreak-London-Basic](https://github.com/PHI-Case-Studies/1854-Cholera-Outbreak-London-Basic) | Historical cholera outbreak analysis | Basic Jupyter Notebook case study of the 1854 London cholera outbreak. Useful for introductory spatial epidemiology and historical public-health mapping; verify source data and case-study assumptions before reuse. |

## Vector data and geometry

| Repository | Best for | Notes |
|---|---|---|
| [geopandas/geopandas](https://github.com/geopandas/geopandas) | Vector analysis in Python | Combines pandas-style data handling with spatial operations. A strong default for tabular/vector workflows. |
| [Toblerity/Fiona](https://github.com/Toblerity/Fiona) | Reading and writing vector formats | Useful for format support and lower-level I/O; GeoPandas may provide the higher-level workflow. |
| [shapely/shapely](https://github.com/shapely/shapely) | Geometry creation and predicates | Use for buffers, intersections, unions, validity, distances, and area operations. |
| [geopandas/dask-geopandas](https://github.com/geopandas/dask-geopandas) | Parallel GeoPandas workloads | Consider only when datasets or operations genuinely benefit from distributed or partitioned processing. |
| [uber/h3-py](https://github.com/uber/h3-py) | Hexagonal spatial indexes | Useful for consistent grids, aggregation, and cross-region joins. Document resolution and boundary assumptions. |

## Raster, imagery, and remote sensing

| Repository | Best for | Notes |
|---|---|---|
| [rasterio/rasterio](https://github.com/rasterio/rasterio) | Raster I/O and processing | Read/write rasters, inspect metadata, reproject, mask, and perform windowed operations. |
| [vylor/rioxarray](https://github.com/vylor/rioxarray) | Raster analysis with xarray | Useful for labeled arrays, multidimensional datasets, and metadata-aware raster workflows. |
| [cogeotiff/rio-tiler](https://github.com/cogeotiff/rio-tiler) | Cloud-optimized GeoTIFF and tiles | Useful for serverless or web tile workflows. |
| [OSGeo/gdal](https://github.com/OSGeo/gdal) | Universal geospatial format and transform layer | Essential underlying infrastructure; prefer recorded CLI or API commands over undocumented GUI work. |
| [pydata/xarray](https://github.com/pydata/xarray) | Multidimensional labeled arrays | Useful for time series of imagery and climate or environmental rasters. |
| [opengeos/geoai](https://github.com/opengeos/geoai) | GeoAI and remote-sensing experiments | Evaluate model provenance, licensing, spatial leakage, and uncertainty before operational use. |

## Spatial statistics and network analysis

| Repository | Best for | Notes |
|---|---|---|
| [pysal/pysal](https://github.com/pysal/pysal) | Spatial statistics and exploratory analysis | Covers spatial weights, clustering, autocorrelation, and regression workflows. |
| [pysal/libpysal](https://github.com/pysal/libpysal) | Core spatial-analysis components | Use for spatial weights and common supporting structures. |
| [pysal/mgwr](https://github.com/pysal/mgwr) | Multiscale geographically weighted regression | Suitable for spatially varying relationships after checking scale, collinearity, and dependence. |
| [networkx/networkx](https://github.com/networkx/networkx) | General graph analysis | Foundation for custom network analysis; OSMnx adds street-network-specific behavior. |
| [gboeing/osmnx](https://github.com/gboeing/osmnx) | Street-network extraction and metrics | Useful for connectivity, accessibility, isochrones, and travel-network analysis. |

## Databases and reproducible spatial SQL

| Repository | Best for | Notes |
|---|---|---|
| [postgis/postgis](https://github.com/postgis/postgis) | Spatial PostgreSQL engine | Use when data is relational, large, shared, or queried repeatedly. |
| [postgis/docker-postgis](https://github.com/postgis/docker-postgis) | Local PostGIS environments | Pin versions and record initialization scripts for reproducible projects. |
| [pyproj4/pyproj](https://github.com/pyproj4/pyproj) | Coordinate transforms and CRS operations | Critical for selecting and validating projected coordinate systems. |

## Mapping and web viewing

| Repository | Best for | Notes |
|---|---|---|
| [Leaflet/Leaflet](https://github.com/Leaflet/Leaflet) | Lightweight interactive maps | Good for a no-build or simple browser viewer. |
| [maplibre/maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js) | Vector/raster web maps | Good for MapLibre styles, vector tiles, 3D terrain, and richer interactions. |
| [openlayers/openlayers](https://github.com/openlayers/openlayers) | Feature-rich web mapping | Suitable for GIS-heavy browser applications and a wide range of data sources. |
| [Turfjs/turf](https://github.com/Turfjs/turf) | Browser-side geospatial operations | Useful for measurement, joins, buffers, classification support, and simple geometry tasks. |
| [python-visualization/folium](https://github.com/python-visualization/folium) | Python-generated Leaflet maps | Builds interactive Leaflet maps from Python notebooks and scripts; useful for rapid visualization and exploratory mapping. |
| [qgis/QGIS](https://github.com/qgis/QGIS) | Desktop GIS and processing | Useful for visual QA, complex geoprocessing, and reviewing map outputs. |
| [qgis/QGIS-Documentation](https://github.com/qgis/QGIS-Documentation) | QGIS documentation | Use for authoritative processing-tool and expression behavior. |

## Desktop GIS and R alternatives

| Repository | Best for | Notes |
|---|---|---|
| [r-spatial/sf](https://github.com/r-spatial/sf) | Simple Features in R | Strong choice for R-based vector processing and analysis. |
| [r-spatial/terra](https://github.com/r-spatial/terra) | Raster and vector processing in R | Useful for spatial prediction, raster stacks, zonal operations, and transformations. |

## Suggested selection rules

1. **Prefer maintained, well-documented projects.** Inspect release status, issue
   activity, license, and supported platforms before adopting a dependency.
2. **Choose the smallest tool that solves the question.** GeoPandas or Turf may
   be enough when no spatial database or distributed system is required.
3. **Record versions and commands.** Add package or container versions, CRS,
   parameters, input paths, output paths, and rerun instructions to
   `analysis-plan.md`.
4. **Prefer open, authoritative data sources.** Treat GitHub projects as tools
   or examples unless they are themselves established data publishers.
5. **Keep source data immutable.** Write derived datasets separately and save
   original source metadata and license information.
6. **Verify before automation.** A library may exist even if it does not support
   the required CRS, geometry, scale, API quota, license, or network environment.
7. **Do not hide uncertainty.** Record confidence, missingness, temporal
   mismatch, simplification, reprojection, and validation failures.

## Reproducibility template

Each analysis script or workflow should identify:

- Dataset and source URL
- License and attribution
- Dataset vintage and update frequency
- Input and output paths
- Geometry type and feature count
- Source CRS and target CRS
- Spatial and temporal coverage
- Software and library versions
- Method and key parameters
- Validation checks and known limitations

For a new project, copy the relevant tool choices into `analysis-plan.md` and
add the Scout findings to `data-sources.md` before analysis begins.
