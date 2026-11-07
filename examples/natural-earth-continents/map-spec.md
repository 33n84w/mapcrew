# Map Specification: Countries by Continent

## Audience and Purpose

- Audience: general audience and classroom users
- Purpose: show the global distribution of country polygons by continent
- This map is descriptive; it makes no claim about population, area, sovereignty, or geopolitical status.

## Extent and Projection

- Extent: global
- Display CRS: WGS 84 longitude/latitude (GeoJSON / EPSG:4326)
- Use a world view; do not compute area or distance in this CRS.

## Layer

| Order | Layer / source | Geometry | Role | Visibility default | Attribution |
|---:|---|---|---|---|---|
| 1 | Natural Earth Admin 0 Countries, 1:110m | Polygon / MultiPolygon | Country outlines categorized by `CONTINENT` | On | Natural Earth; inspect archive notices for third-party sources |

## Symbology and Classification

- Field: `CONTINENT` (nominal categorical data)
- Use a distinct categorical palette, not a sequential or diverging ramp.
- Suggested palette: Africa `#D55E00`, Antarctica `#56B4E9`, Asia `#009E73`, Europe `#CC79A7`, North America `#E69F00`, Oceania `#0072B2`, South America `#F0E442`.
- Thin neutral country borders; avoid outlines that overwhelm the fills.
- Treat any missing or unrecognized continent value as `No data` in a neutral gray and include it in the legend.

## Legend and Interaction

- Legend title: `Continent`
- Include one entry per observed category and an entry for missing values if present.
- Popup: country name and continent, using the downloaded layer's verified property names.
- Include layer visibility toggle and a global extent button.

## Basemap and Attribution

- Basemap: optional OpenStreetMap tiles with visible provider attribution; allow a no-basemap view.
- Data attribution: `Data: Natural Earth (public domain); see archive notices for third-party contributions.`
- Keep the basemap subordinate to the country fills. Observe the basemap provider's terms and tile usage policy.

## Limitations

- 1:110m data are generalized and intended for small-scale global views.
- Political boundaries and disputed areas represent the dataset's conventions, not a legal determination.
- CRS and archive attribution must be confirmed from the actual downloaded file and notices.