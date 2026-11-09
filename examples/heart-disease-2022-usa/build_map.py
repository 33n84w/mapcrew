import csv
import json
import math
import statistics
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
CDC_API = "https://data.cdc.gov/resource/fu4u-a9bh.json"
CENSUS_QUERY = (
    "https://tigerweb.geo.census.gov/arcgis/rest/services/"
    "TIGERweb/State_County/MapServer/13/query"
)
STATE_FIPS = [
    "01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13",
    "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
    "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36",
    "37", "38", "39", "40", "41", "42", "44", "45", "46", "47", "48",
    "49", "50", "51", "53", "54", "55", "56",
]
METRIC_COLORS = ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08306b"]
HEALTH_FIELDS = [
    "locationid",
    "locationname",
    "stateabbr",
    "statedesc",
    "year",
    "measure",
    "datavaluetypeid",
    "data_value",
    "low_confidence_limit",
    "high_confidence_limit",
    "totalpop18plus",
    "data_value_footnote",
]


def fetch_json(url, params=None):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url, headers={"User-Agent": "MapCrew heart-disease map/1.0"}
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def fetch_health_rows():
    return fetch_json(
        CDC_API,
        {
            "$select": ",".join(HEALTH_FIELDS),
            "$where": "measureid='CHD' AND stateabbr<>'US'",
            "$limit": "10000",
            "$order": "locationid,datavaluetypeid",
        },
    )


def fetch_counties():
    features = []
    for state in STATE_FIPS:
        response = fetch_json(
            CENSUS_QUERY,
            {
                "where": f"STATE='{state}'",
                "outFields": "GEOID,STATE,NAME",
                "returnGeometry": "true",
                "outSR": "4326",
                "geometryPrecision": "4",
                "maxAllowableOffset": "0.001",
                "resultRecordCount": "10000",
                "f": "geojson",
            },
        )
        features.extend(response.get("features", []))
    return {"type": "FeatureCollection", "features": features}


def save_health_csv(rows):
    path = DATA_DIR / "places_chd_2024.csv"
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=HEALTH_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return path


def save_json(path, data):
    path.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    return path


def validate_geometry(feature):
    geometry = feature.get("geometry") or {}
    if geometry.get("type") not in {"Polygon", "MultiPolygon"}:
        raise ValueError(f"Unexpected geometry type for {feature.get('properties')}")
    parts = geometry.get("coordinates")
    if not parts:
        raise ValueError(f"Empty geometry for {feature.get('properties')}")
    for polygon in parts if geometry["type"] == "MultiPolygon" else [parts]:
        if not polygon or len(polygon[0]) < 4:
            raise ValueError(f"Invalid polygon ring for {feature.get('properties')}")
        for ring in polygon:
            for point in ring:
                if (
                    len(point) < 2
                    or not math.isfinite(float(point[0]))
                    or not math.isfinite(float(point[1]))
                    or not -180 <= float(point[0]) <= 180
                    or not -90 <= float(point[1]) <= 90
                ):
                    raise ValueError(f"Invalid coordinate for {feature.get('properties')}")


def index_estimates(rows):
    indexed = {}
    for row in rows:
        fips = str(row.get("locationid", "")).zfill(5)
        value_type = row.get("datavaluetypeid")
        if value_type not in {"AgeAdjPrv", "CrdPrv"}:
            continue
        if fips in indexed and value_type in indexed[fips]:
            raise ValueError(f"Duplicate {value_type} estimate for county FIPS {fips}")
        estimate = row.get("data_value")
        if estimate in (None, ""):
            raise ValueError(f"Missing {value_type} estimate for county FIPS {fips}")
        value = float(estimate)
        if not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError(f"Out-of-range estimate for county FIPS {fips}: {estimate}")
        indexed.setdefault(fips, {})[value_type] = row
    return indexed


def percentile(values, proportion):
    ordered = sorted(values)
    position = (len(ordered) - 1) * proportion
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def build_derived_geojson(counties, estimates):
    features = []
    seen = set()
    for source in counties["features"]:
        properties = source.get("properties") or {}
        fips = str(properties.get("GEOID", "")).zfill(5)
        state = str(properties.get("STATE", ""))
        if len(fips) != 5 or state not in STATE_FIPS:
            raise ValueError(f"Invalid county FIPS/state: {fips}, {state}")
        if fips in seen:
            raise ValueError(f"Duplicate Census county GEOID: {fips}")
        seen.add(fips)
        validate_geometry(source)
        if fips not in estimates:
            raise ValueError(f"No CDC estimate for Census county GEOID {fips}")
        county_estimates = estimates[fips]
        if set(county_estimates) != {"AgeAdjPrv", "CrdPrv"}:
            raise ValueError(f"Incomplete estimate types for county FIPS {fips}")
        adjusted = county_estimates["AgeAdjPrv"]
        crude = county_estimates["CrdPrv"]
        if adjusted["year"] != "2022" or crude["year"] != "2022":
            raise ValueError(f"Unexpected estimate year for county FIPS {fips}")
        output_properties = {
            "fips": fips,
            "name": properties.get("NAME", ""),
            "state": state,
            "state_name": adjusted.get("statedesc", ""),
            "measure": adjusted.get("measure", ""),
            "estimate_year": int(adjusted["year"]),
            "age_adjusted_percent": float(adjusted["data_value"]),
            "age_adjusted_ci_low": float(adjusted["low_confidence_limit"]),
            "age_adjusted_ci_high": float(adjusted["high_confidence_limit"]),
            "crude_percent": float(crude["data_value"]),
            "crude_ci_low": float(crude["low_confidence_limit"]),
            "crude_ci_high": float(crude["high_confidence_limit"]),
            "adult_population": int(adjusted["totalpop18plus"]),
            "data_source": "CDC PLACES 2024",
        }
        features.append(
            {
                "type": "Feature",
                "geometry": source["geometry"],
                "properties": output_properties,
            }
        )
    if len(features) != 3144 or len(estimates) != 3144 or seen != set(estimates):
        raise ValueError(
            f"County join coverage mismatch: {len(features)} shapes, "
            f"{len(estimates)} estimates"
        )
    return {"type": "FeatureCollection", "features": features}


def flatten_rings(geometry):
    coordinates = geometry["coordinates"]
    polygons = coordinates if geometry["type"] == "MultiPolygon" else [coordinates]
    for polygon in polygons:
        for ring in polygon:
            yield ring


def albers(lon, lat, center_lon, center_lat, parallel_1, parallel_2):
    phi1 = math.radians(parallel_1)
    phi2 = math.radians(parallel_2)
    phi0 = math.radians(center_lat)
    n = 0.5 * (math.sin(phi1) + math.sin(phi2))
    c = math.cos(phi1) ** 2 + 2 * n * math.sin(phi1)
    phi = math.radians(lat)
    rho = math.sqrt(max(0, c - 2 * n * math.sin(phi))) / n
    rho0 = math.sqrt(max(0, c - 2 * n * math.sin(phi0))) / n
    lon_delta = math.radians(lon - center_lon)
    theta = n * lon_delta
    return rho * math.sin(theta), rho0 - rho * math.cos(theta)


def project_for_region(point, region):
    lon, lat = float(point[0]), float(point[1])
    center_lon = region["center_lon"]
    if region["key"] == "ak":
        if lon - center_lon > 180:
            lon -= 360
        elif lon - center_lon < -180:
            lon += 360
    return albers(
        lon,
        lat,
        center_lon,
        region["center_lat"],
        region["parallel_1"],
        region["parallel_2"],
    )


def render_svg(geojson, breaks, summary):
    regions = [
        {
            "key": "conus",
            "title": "Contiguous United States",
            "features": [f for f in geojson["features"] if f["properties"]["state"] not in {"02", "15"}],
            "panel": (270, 125, 1180, 640),
            "center_lon": -96,
            "center_lat": 23,
            "parallel_1": 29.5,
            "parallel_2": 45.5,
        },
        {
            "key": "ak",
            "title": "Alaska",
            "features": [f for f in geojson["features"] if f["properties"]["state"] == "02"],
            "panel": (25, 600, 270, 220),
            "center_lon": -154,
            "center_lat": 55,
            "parallel_1": 55,
            "parallel_2": 65,
        },
        {
            "key": "hi",
            "title": "Hawaii",
            "features": [f for f in geojson["features"] if f["properties"]["state"] == "15"],
            "panel": (320, 680, 300, 140),
            "center_lon": -157,
            "center_lat": 20,
            "parallel_1": 18,
            "parallel_2": 22,
            "focus_bounds": (-161.5, -153.8, 18, 23),
        },
    ]
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="920" viewBox="0 0 1500 920" role="img" aria-labelledby="title description">',
        '<title id="title">County-level coronary heart disease prevalence</title>',
        '<desc id="description">2022 age-adjusted prevalence estimates by county in the United States.</desc>',
        '<rect width="1500" height="920" fill="#ffffff"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#1d2927}.county{stroke:#fff;stroke-width:.35;stroke-linejoin:round}.county-hi{stroke:#374151;stroke-width:2}</style>',
        '<text x="35" y="46" font-size="29" font-weight="700">Diagnosed coronary heart disease prevalence</text>',
        '<text x="35" y="76" font-size="16">2022 age-adjusted estimate • Percent of adults • CDC PLACES 2024</text>',
    ]
    for region in regions:
        extent_points = []
        projected_features = []
        for feature in region["features"]:
            rings = []
            for ring in flatten_rings(feature["geometry"]):
                points = []
                for point in ring:
                    projected_point = project_for_region(point, region)
                    points.append(projected_point)
                    bounds = region.get("focus_bounds")
                    if bounds is None or (
                        bounds[0] <= float(point[0]) <= bounds[1]
                        and bounds[2] <= float(point[1]) <= bounds[3]
                    ):
                        extent_points.append(projected_point)
                rings.append(points)
            projected_features.append((feature, rings))
        if not extent_points:
            raise ValueError(f"No geometries found for map panel {region['key']}")
        min_x = min(point[0] for point in extent_points)
        max_x = max(point[0] for point in extent_points)
        min_y = min(point[1] for point in extent_points)
        max_y = max(point[1] for point in extent_points)
        panel_x, panel_y, panel_w, panel_h = region["panel"]
        scale = min(panel_w / (max_x - min_x), panel_h / (max_y - min_y))
        width = (max_x - min_x) * scale
        height = (max_y - min_y) * scale
        offset_x = panel_x + (panel_w - width) / 2
        offset_y = panel_y + (panel_h - height) / 2
        clip_id = f'clip-{region["key"]}'
        svg.append(
            f'<defs><clipPath id="{clip_id}"><rect x="{panel_x}" y="{panel_y}" width="{panel_w}" height="{panel_h}"/></clipPath></defs>'
        )
        svg.append(
            f'<text x="{panel_x}" y="{panel_y - 10}" font-size="16" font-weight="700">{region["title"]}</text>'
        )
        svg.append(f'<g clip-path="url(#{clip_id})">')
        for feature, rings in projected_features:
            path_segments = []
            for ring in rings:
                if len(ring) < 4:
                    continue
                coords = [
                    (
                        offset_x + (x - min_x) * scale,
                        offset_y + (max_y - y) * scale,
                    )
                    for x, y in ring
                ]
                path_segments.append(
                    "M"
                    + " L".join(f"{x:.2f},{y:.2f}" for x, y in coords)
                    + " Z"
                )
            rate = feature["properties"]["age_adjusted_percent"]
            fill = color_for_value(rate, breaks)
            if path_segments:
                county_class = "county county-hi" if region["key"] == "hi" else "county"
                svg.append(
                    f'<path class="{county_class}" d="{" ".join(path_segments)}" fill="{fill}"><title>{escape_xml(feature["properties"]["name"] + ", " + feature["properties"]["state_name"] + ": " + format(rate, ".1f") + "%")}</title></path>'
                )
        svg.append("</g>")
    legend_y = 150
    svg.append(f'<text x="35" y="{legend_y}" font-size="16" font-weight="700">Age-adjusted prevalence</text>')
    labels = [f"≤ {breaks[0]:.1f}%"] + [
        f"> {breaks[index - 1]:.1f}–≤ {breaks[index]:.1f}%"
        for index in range(1, len(breaks))
    ] + [f"> {breaks[-1]:.1f}%"]
    for index, color in enumerate(METRIC_COLORS):
        y = legend_y + 28 + index * 36
        svg.append(f'<rect x="35" y="{y - 16}" width="22" height="22" fill="{color}" stroke="#777"/>')
        svg.append(f'<text x="67" y="{y}" font-size="14">{labels[index]}</text>')
    svg.append('<rect x="35" y="387" width="22" height="22" fill="#d9dde1" stroke="#777"/>')
    svg.append('<text x="67" y="403" font-size="14">No estimate</text>')
    svg.append(
        f'<text x="35" y="445" font-size="13">Counties mapped: {summary["county_count"]:,}</text>'
    )
    svg.append(
        f'<text x="35" y="468" font-size="13">Range: {summary["min"]:.1f}–{summary["max"]:.1f}%</text>'
    )
    svg.append('<text x="25" y="846" font-size="12">Alaska and Hawaii are shown in separate insets at different scales; the Hawaii inset focuses on the main islands.</text>')
    svg.append('<text x="25" y="870" font-size="12">Source: CDC PLACES 2024, 2022 model-based estimates; U.S. Census Bureau TIGERweb county boundaries (2026).</text>')
    svg.append('<text x="25" y="892" font-size="12">Estimates are for diagnosed coronary heart disease among adults; not individual risk or evidence of causation. See data-sources.md and qa-report.md.</text>')
    svg.append("</svg>")
    return "\n".join(svg)


def escape_xml(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def color_for_value(value, breaks):
    for index, limit in enumerate(breaks):
        if value <= limit:
            return METRIC_COLORS[index]
    return METRIC_COLORS[-1]


def render_html(geojson, breaks, summary):
    template = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>County Heart Disease Prevalence | MapCrew</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <style>
    :root { color-scheme: light; --ink: #1d2927; --muted: #64716e; --line: #d7dfdc; --paper: #f5f7f4; --panel: #fff; --forest: #174e43; }
    * { box-sizing: border-box; }
    body { margin: 0; color: var(--ink); background: var(--paper); font: 14px/1.45 "Segoe UI", sans-serif; }
    .app { display: grid; grid-template-columns: minmax(260px, 320px) minmax(0, 1fr); min-height: 100vh; }
    aside { display: flex; flex-direction: column; gap: 16px; padding: 20px; background: var(--panel); border-right: 1px solid var(--line); }
    h1 { margin: 0; font-size: 19px; line-height: 1.25; }
    h2 { margin: 0 0 7px; color: var(--muted); font-size: 11px; letter-spacing: .04em; text-transform: uppercase; }
    p { margin: 0; }
    .muted, .hint { color: var(--muted); font-size: 12px; }
    .field { display: grid; gap: 7px; }
    select, button { width: 100%; min-height: 38px; padding: 7px 9px; color: var(--ink); background: #fff; border: 1px solid var(--line); border-radius: 5px; font: inherit; }
    button { cursor: pointer; }
    :focus-visible { outline: 3px solid #68ad96; outline-offset: 2px; }
    .legend { display: grid; gap: 5px; font-size: 12px; }
    .legend-row { display: flex; align-items: center; gap: 8px; }
    .swatch { width: 18px; height: 15px; border: 1px solid #87918e; }
    .maps { display: grid; grid-template-columns: minmax(0, 1fr) 260px; grid-template-rows: minmax(450px, 1fr) 260px; gap: 8px; min-width: 0; padding: 8px; }
    .map-panel { position: relative; min-width: 0; overflow: hidden; border: 1px solid var(--line); border-radius: 5px; background: #e8eeeb; }
    #map-conus { grid-row: 1 / span 2; }
    .panel-title { position: absolute; z-index: 500; top: 8px; left: 50px; padding: 4px 8px; background: rgba(255,255,255,.92); border: 1px solid var(--line); border-radius: 4px; font-size: 12px; font-weight: 700; pointer-events: none; }
    .map { width: 100%; height: 100%; min-height: 220px; }
    .footer { margin-top: auto; padding-top: 12px; border-top: 1px solid var(--line); }
    .leaflet-popup-content { line-height: 1.55; }
    @media (max-width: 850px) {
      .app { grid-template-columns: minmax(0, 1fr); }
      aside { border-right: 0; border-bottom: 1px solid var(--line); }
      .maps { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); grid-template-rows: minmax(55vh, 1fr) 240px; }
      #map-conus { grid-column: 1 / span 2; grid-row: auto; }
    }
    @media (max-width: 540px) { .maps { grid-template-columns: minmax(0, 1fr); grid-template-rows: minmax(55vh, 1fr) 220px 220px; } #map-conus { grid-column: auto; } }
  </style>
</head>
<body>
  <div class="app">
    <aside aria-label="Map controls and information">
      <header>
        <h1>Coronary Heart Disease by County</h1>
        <p class="muted">United States · CDC PLACES 2024 · estimate year 2022</p>
      </header>
      <section class="field">
        <label for="metric"><strong>Measure</strong></label>
        <select id="metric">
          <option value="age_adjusted_percent">Age-adjusted prevalence</option>
          <option value="crude_percent">Crude prevalence</option>
        </select>
        <p class="hint">Percent of adults with diagnosed coronary heart disease. Age-adjusted values are best for comparing counties with different age structures.</p>
      </section>
      <section class="field">
        <label for="basemap"><strong>Basemap</strong></label>
        <select id="basemap">
          <option value="topo">Esri World Topographic Map</option>
          <option value="street">Esri World Street Map</option>
          <option value="imagery">Esri World Imagery</option>
          <option value="none">No basemap</option>
        </select>
      </section>
      <section>
        <h2>Legend</h2>
        <div id="legend" class="legend" aria-live="polite"></div>
      </section>
      <section>
        <h2>How to read</h2>
        <p class="hint">Select a county for age-adjusted and crude estimates, 95% confidence intervals, and adult population. Alaska and Hawaii are separate views. County values are modeled estimates, not direct surveys.</p>
      </section>
      <div class="footer">
        <p class="hint">Source: CDC PLACES 2024; 2022 estimates. County boundaries: U.S. Census Bureau TIGERweb, 2026 vintage.</p>
        <p class="hint">Do not interpret the map as causal evidence, an intervention evaluation, or individual risk. Esri tiles require internet. County geometry and estimates are embedded in this file.</p>
      </div>
    </aside>
    <main class="maps" aria-label="U.S. county maps">
      <section class="map-panel" aria-label="Contiguous United States">
        <span class="panel-title">Contiguous United States</span>
        <div id="map-conus" class="map" role="application" aria-label="Interactive county map of the contiguous United States"></div>
      </section>
      <section class="map-panel" aria-label="Alaska">
        <span class="panel-title">Alaska</span>
        <div id="map-ak" class="map" role="application" aria-label="Interactive county map of Alaska"></div>
      </section>
      <section class="map-panel" aria-label="Hawaii">
        <span class="panel-title">Hawaii</span>
        <div id="map-hi" class="map" role="application" aria-label="Interactive county map of Hawaii"></div>
      </section>
    </main>
  </div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const countyData = __COUNTY_DATA__;
    const classBreaksByMetric = __CLASS_BREAKS__;
    const metricStats = __METRIC_STATS__;
    const colors = __COLORS__;
    const maps = [
      { id: "map-conus", include: (state) => state !== "02" && state !== "15", center: [39, -98], zoom: 4 },
      { id: "map-ak", include: (state) => state === "02", center: [62, -153], zoom: 3 },
      { id: "map-hi", include: (state) => state === "15", center: [20.8, -156.5], zoom: 6 }
    ];
    const tileOptions = {
      topo: {
        url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        maxZoom: 19,
        attribution: "Tiles &copy; Esri — Sources: Esri, HERE, Garmin, Intermap, increment P Corp., GEBCO, USGS, FAO, NPS, NRCAN, GeoBase, IGN, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), &copy; OpenStreetMap contributors, and the GIS User Community. <a href=\"https://goto.arcgisonline.com/maps/World_Topo_Map\">Terms and details</a>."
      },
      street: {
        url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        maxZoom: 19,
        attribution: "Tiles &copy; Esri — Sources: Esri, HERE, Garmin, USGS, Intermap, INCREMENT P, NRCan, Esri Japan, METI, Esri China (Hong Kong), Esri Korea, Esri (Thailand), NGCC, &copy; OpenStreetMap contributors, and the GIS User Community. <a href=\"https://goto.arcgisonline.com/maps/World_Street_Map\">Terms and details</a>."
      },
      imagery: {
        url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        maxZoom: 23,
        attribution: "Source: Esri, Vantor, Earthstar Geographics, and the GIS User Community. <a href=\"https://goto.arcgisonline.com/maps/World_Imagery\">Terms and details</a>."
      }
    };
    let metric = "age_adjusted_percent";
    let activeTiles = "topo";
    const mapStates = [];

    function formatPercent(value) {
      return Number(value).toFixed(1) + "%";
    }

    function metricValue(properties) {
      return properties[metric];
    }

    function colorFor(value) {
      if (value == null || !Number.isFinite(Number(value))) return "#d9dde1";
      const breaks = classBreaksByMetric[metric];
      for (let index = 0; index < breaks.length; index += 1) {
        if (Number(value) <= breaks[index]) return colors[index];
      }
      return colors[colors.length - 1];
    }

    function updateLegend() {
      const legend = document.getElementById("legend");
      const label = metric === "age_adjusted_percent" ? "Age-adjusted" : "Crude";
      const breaks = classBreaksByMetric[metric];
      const stats = metricStats[metric];
      const labels = [`≤ ${breaks[0].toFixed(1)}%`];
      for (let index = 1; index < breaks.length; index += 1) {
        labels.push(`> ${breaks[index - 1].toFixed(1)}–≤ ${breaks[index].toFixed(1)}%`);
      }
      labels.push(`> ${breaks[breaks.length - 1].toFixed(1)}%`);
      legend.replaceChildren();
      colors.forEach((color, index) => {
        const row = document.createElement("div");
        row.className = "legend-row";
        const swatch = document.createElement("span");
        swatch.className = "swatch";
        swatch.style.backgroundColor = color;
        const text = document.createElement("span");
        text.textContent = labels[index];
        row.append(swatch, text);
        legend.appendChild(row);
      });
      const note = document.createElement("p");
      note.className = "hint";
      note.textContent = `${label} prevalence · five quantile classes · data range ${stats.min.toFixed(1)}–${stats.max.toFixed(1)}%`;
      legend.appendChild(note);
    }

    function popupNode(properties) {
      const container = document.createElement("div");
      const title = document.createElement("strong");
      title.textContent = `${properties.name}, ${properties.state_name}`;
      container.appendChild(title);
      const rows = [
        ["Age-adjusted prevalence", formatPercent(properties.age_adjusted_percent)],
        ["95% CI", `${formatPercent(properties.age_adjusted_ci_low)}–${formatPercent(properties.age_adjusted_ci_high)}`],
        ["Crude prevalence", formatPercent(properties.crude_percent)],
        ["Crude 95% CI", `${formatPercent(properties.crude_ci_low)}–${formatPercent(properties.crude_ci_high)}`],
        ["Adult population", Number(properties.adult_population).toLocaleString()],
        ["Estimate year", String(properties.estimate_year)]
      ];
      rows.forEach(([label, value]) => {
        const row = document.createElement("div");
        row.textContent = `${label}: ${value}`;
        container.appendChild(row);
      });
      return container;
    }

    function createMaps() {
      maps.forEach((region) => {
        const map = L.map(region.id, { preferCanvas: true, minZoom: 2 }).setView(region.center, region.zoom);
        const tile = L.tileLayer(tileOptions.topo.url, {
          maxZoom: tileOptions.topo.maxZoom,
          attribution: tileOptions.topo.attribution
        }).addTo(map);
        const layer = L.geoJSON(countyData, {
          filter: (feature) => region.include(feature.properties.state),
          style: (feature) => ({
            color: "#fff",
            weight: 0.45,
            opacity: 0.9,
            fillColor: colorFor(metricValue(feature.properties)),
            fillOpacity: 0.78
          }),
          onEachFeature: (feature, featureLayer) => {
            featureLayer.bindPopup(() => popupNode(feature.properties));
          }
        }).addTo(map);
        mapStates.push({ map, tile, layer });
      });
      requestAnimationFrame(() => mapStates.forEach(({ map }) => map.invalidateSize()));
    }

    document.getElementById("metric").addEventListener("change", (event) => {
      metric = event.target.value;
      mapStates.forEach(({ layer }) => layer.setStyle((feature) => ({
        fillColor: colorFor(metricValue(feature.properties))
      })));
      updateLegend();
    });

    document.getElementById("basemap").addEventListener("change", (event) => {
      activeTiles = event.target.value;
      mapStates.forEach(({ map, tile }) => map.removeLayer(tile));
      if (activeTiles === "none") return;
      mapStates.forEach((state) => {
        const options = tileOptions[activeTiles];
        state.tile = L.tileLayer(options.url, {
          maxZoom: options.maxZoom,
          attribution: options.attribution
        }).addTo(state.map);
      });
    });

    updateLegend();
    createMaps();
  </script>
</body>
</html>"""
    return (
        template.replace("__COUNTY_DATA__", json.dumps(geojson, separators=(",", ":")))
        .replace(
            "__CLASS_BREAKS__",
            json.dumps(
                {
                    "age_adjusted_percent": breaks,
                    "crude_percent": summary["crude_quantile_breaks"],
                }
            ),
        )
        .replace(
            "__METRIC_STATS__",
            json.dumps(
                {
                    "age_adjusted_percent": {
                        "min": summary["min"],
                        "max": summary["max"],
                    },
                    "crude_percent": {
                        "min": summary["crude_min"],
                        "max": summary["crude_max"],
                    },
                }
            ),
        )
        .replace("__COLORS__", json.dumps(METRIC_COLORS))
    )


def main():
    DATA_DIR.mkdir(exist_ok=True)
    health_rows = fetch_health_rows()
    save_health_csv(health_rows)
    estimates = index_estimates(health_rows)
    if len(estimates) != 3144:
        raise ValueError(f"Expected 3,144 county estimates; received {len(estimates)}")

    counties = fetch_counties()
    save_json(DATA_DIR / "us_counties_tigerweb_2026.geojson", counties)
    geojson = build_derived_geojson(counties, estimates)
    save_json(DATA_DIR / "county_chd_prevalence.geojson", geojson)

    rates = [feature["properties"]["age_adjusted_percent"] for feature in geojson["features"]]
    crude_rates = [feature["properties"]["crude_percent"] for feature in geojson["features"]]
    breaks = [percentile(rates, quantile / 5) for quantile in range(1, 5)]
    crude_breaks = [percentile(crude_rates, quantile / 5) for quantile in range(1, 5)]

    def class_counts(values, limits):
        counts = [0] * len(METRIC_COLORS)
        for value in values:
            for index, limit in enumerate(limits):
                if value <= limit:
                    counts[index] += 1
                    break
            else:
                counts[-1] += 1
        return counts

    adjusted_counts = class_counts(rates, breaks)
    crude_counts = class_counts(crude_rates, crude_breaks)
    summary = {
        "health_data_release": "CDC PLACES 2024 County Data",
        "estimate_year": 2022,
        "measure": "Coronary heart disease among adults",
        "mapped_value": "Age-adjusted prevalence (percent)",
        "county_count": len(rates),
        "crude_county_values": sum(
            1 for feature in geojson["features"] if feature["properties"]["crude_percent"] is not None
        ),
        "min": min(rates),
        "max": max(rates),
        "median": statistics.median(rates),
        "quantile_breaks": breaks,
        "quantile_class_counts": adjusted_counts,
        "crude_min": min(crude_rates),
        "crude_max": max(crude_rates),
        "crude_median": statistics.median(crude_rates),
        "crude_quantile_breaks": crude_breaks,
        "crude_quantile_class_counts": crude_counts,
        "boundary_vintage": "January 1, 2026",
        "sources": [
            "https://data.cdc.gov/d/fu4u-a9bh",
            "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer",
        ],
    }
    save_json(ROOT / "map-summary.json", summary)
    (ROOT / "heart_disease_map.svg").write_text(
        render_svg(geojson, breaks, summary), encoding="utf-8"
    )
    (ROOT / "viewer.html").write_text(
        render_html(geojson, breaks, summary), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    print(f"Raw health data: {DATA_DIR / 'places_chd_2024.csv'}")
    print(f"Raw county boundaries: {DATA_DIR / 'us_counties_tigerweb_2026.geojson'}")
    print(f"Derived county data: {DATA_DIR / 'county_chd_prevalence.geojson'}")
    print(f"Static map: {ROOT / 'heart_disease_map.svg'}")
    print(f"Interactive map: {ROOT / 'viewer.html'}")


if __name__ == "__main__":
    main()
