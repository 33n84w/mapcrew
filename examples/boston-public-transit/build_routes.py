import csv
import io
import json
import math
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
GTFS_URL = "https://cdn.mbta.com/MBTA_GTFS.zip"
GTFS_PATH = DATA_DIR / "MBTA_GTFS.zip"

CATEGORIES = {
    "0": ("Light rail", "#00A6A6"),
    "1": ("Subway", "#1F78B4"),
    "2": ("Commuter rail", "#6A3D9A"),
    "3": ("Bus", "#E31A1C"),
    "4": ("Ferry", "#00A67E"),
}


def download_feed():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        GTFS_URL,
        headers={"User-Agent": "MapCrew Boston public transit map/1.0"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        GTFS_PATH.write_bytes(response.read())


def read_feed_csv(feed, name):
    with feed.open(name) as file:
        text = io.TextIOWrapper(file, encoding="utf-8-sig")
        return list(csv.DictReader(text))


def read_feed_info(feed):
    for item in read_feed_csv(feed, "feed_info.txt"):
        return item
    return {}


def rdp(points, epsilon):
    if len(points) <= 2:
        return points

    start = points[0]
    end = points[-1]
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    scale_sq = dx * dx + dy * dy

    def distance(point):
        if scale_sq == 0:
            return math.hypot(point[0] - start[0], point[1] - start[1])
        t = ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / scale_sq
        t = max(0.0, min(1.0, t))
        projection = (start[0] + t * dx, start[1] + t * dy)
        return math.hypot(point[0] - projection[0], point[1] - projection[1])

    keep_index = max(range(1, len(points) - 1), key=lambda i: distance(points[i]))
    keep_distance = distance(points[keep_index])
    if keep_distance > epsilon:
        left = rdp(points[: keep_index + 1], epsilon)
        right = rdp(points[keep_index:], epsilon)
        return left[:-1] + right
    return [start, end]


def save_json(path, data):
    path.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


def build():
    download_feed()

    with zipfile.ZipFile(GTFS_PATH) as feed:
        routes = read_feed_csv(feed, "routes.txt")
        trips = read_feed_csv(feed, "trips.txt")
        shapes = read_feed_csv(feed, "shapes.txt")
        feed_info = read_feed_info(feed)

    route_by_id = {row["route_id"]: row for row in routes}

    shape_routes = {}
    for trip in trips:
        shape_id = trip.get("shape_id", "").strip()
        route_id = trip.get("route_id", "").strip()
        if shape_id and route_id:
            shape_routes.setdefault(shape_id, set()).add(route_id)

    shape_points = {}
    for row in shapes:
        shape_id = row["shape_id"].strip()
        point = (float(row["shape_pt_lon"]), float(row["shape_pt_lat"]))
        sequence = int(row["shape_pt_sequence"])
        shape_points.setdefault(shape_id, []).append((sequence, point))

    category_features = {key: [] for key in CATEGORIES}
    all_features = []
    route_shape_counts = {}

    for shape_id, indexed_points in shape_points.items():
        route_ids = sorted(shape_routes.get(shape_id, []))
        if not route_ids:
            continue
        points = [point for _, point in sorted(indexed_points)]
        if len(points) < 2:
            continue
        simplified = rdp(points, 0.00025)
        if len(simplified) < 2:
            continue

        for route_id in route_ids:
            route = route_by_id.get(route_id)
            if not route:
                continue
            route_type = route["route_type"].strip()
            category = CATEGORIES.get(route_type)
            if not category:
                continue
            category_name, category_color = category
            short_name = route.get("route_short_name", "").strip()
            long_name = route.get("route_long_name", "").strip()
            display_name = short_name or long_name or route_id
            properties = {
                "route_id": route_id,
                "route_name": display_name,
                "route_long_name": long_name,
                "route_type": route_type,
                "route_type_name": category_name,
                "category_color": category_color,
                "route_color": "#" + route.get("route_color", "").strip().lstrip("#")
                if route.get("route_color", "").strip()
                else category_color,
                "shape_id": shape_id,
            }
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": simplified,
                },
                "properties": properties,
            }
            category_features[route_type].append(feature)
            all_features.append(feature)
            route_shape_counts[route_id] = route_shape_counts.get(route_id, 0) + 1

    for route_type, (category_name, _) in CATEGORIES.items():
        save_json(
            DATA_DIR / ("routes-" + category_name.lower().replace(" ", "-") + ".geojson"),
            {"type": "FeatureCollection", "features": category_features[route_type]},
        )

    combined = {"type": "FeatureCollection", "features": all_features}
    save_json(DATA_DIR / "boston-public-transit-routes.geojson", combined)

    (ROOT / "routes.js").write_text(
        "window.BOSTON_TRANSIT_ROUTES = "
        + json.dumps(combined, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )

    type_counts = {
        CATEGORIES[key][0]: len(category_features[key])
        for key in CATEGORIES
    }
    summary = {
        "feed_url": GTFS_URL,
        "feed_publisher": feed_info.get("feed_publisher_name", "Massachusetts Bay Transportation Authority"),
        "feed_start_date": feed_info.get("feed_start_date", ""),
        "feed_end_date": feed_info.get("feed_end_date", ""),
        "feed_version": feed_info.get("feed_version", ""),
        "route_count": len(route_by_id),
        "shape_feature_count": len(all_features),
        "features_by_type": type_counts,
        "routes_with_shapes": len(route_shape_counts),
        "routes_without_shapes": sorted(
            route_id for route_id in route_by_id if route_id not in route_shape_counts
        ),
        "source_format": "GTFS",
        "coordinate_reference_system": "EPSG:4326",
    }
    save_json(ROOT / "map-summary.json", summary)


if __name__ == "__main__":
    build()
