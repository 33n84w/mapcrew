import glob
import json
import math
import os


ROOT = os.path.dirname(__file__)


def load(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


combined = load(os.path.join(ROOT, "data", "boston-public-transit-routes.geojson"))
summary = load(os.path.join(ROOT, "map-summary.json"))

type_counts = {}
invalid = []
for feature in combined["features"]:
    properties = feature["properties"]
    name = properties["route_type_name"]
    type_counts[name] = type_counts.get(name, 0) + 1
    coordinates = feature["geometry"]["coordinates"]
    if len(coordinates) < 2:
        invalid.append(properties["route_id"])
        continue
    for longitude, latitude in coordinates:
        if (
            not math.isfinite(longitude)
            or not math.isfinite(latitude)
            or not -180 <= longitude <= 180
            or not -90 <= latitude <= 90
        ):
            invalid.append(properties["route_id"])
            break

category_files = {}
for path in glob.glob(os.path.join(ROOT, "data", "routes-*.geojson")):
    data = load(path)
    category_files[os.path.basename(path)] = len(data["features"])

print(
    json.dumps(
        {
            "features": len(combined["features"]),
            "types": type_counts,
            "invalid_geometry": len(invalid),
            "routes_without_shapes": len(summary["routes_without_shapes"]),
            "category_files": category_files,
        },
        indent=2,
        sort_keys=True,
    )
)

if invalid:
    raise SystemExit("Invalid route geometry detected")
