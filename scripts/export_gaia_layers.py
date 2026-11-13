"""Export the commons registry as a Gaia synced source.

Gaia imports any source that publishes a manifest (`layers.json`) plus one
GeoJSON file per layer (see hub-culture/gaiaclub, gaia-api/src/sources.rs).
This writes that shape to `gaia/`, so Gaia can add the Global Commons with

    GAIA_SOURCES=...,commons=https://raw.githubusercontent.com/hub-culture/Commons/main/gaia/layers.json

and its layer appears as `commons.registry`.

Run:  python scripts/export_gaia_layers.py
"""
import json
import os

REPO = "https://github.com/hub-culture/Commons"
STEP_NAMES = {1: "No rules", 2: "Weak rules", 3: "Rules that don't pay out"}


def props(e):
    return {
        "slug": e["id"],
        "name": e["name"],
        "kind": e["kind"],
        "ladder_step": e["ladder_step"],
        "ladder_step_name": STEP_NAMES[e["ladder_step"]],
        "status": e["status"],
        "summary": e.get("summary", ""),
        "boundary_type": e["boundaries"]["type"],
        "boundary_notes": e["boundaries"].get("notes", ""),
        "rules": "; ".join(f'{r["name"]} ({r["status"]})' for r in e.get("rules", [])),
        "cloud_mirror_spoke": e.get("cloud_mirror_spoke") or "",
        "registry_url": f"{REPO}/blob/main/data/registry/seed.json",
    }


def main():
    entries = json.load(open(os.path.join("data", "registry", "seed.json")))
    placed, unplaced = [], []
    for e in entries:
        b = e["boundaries"]
        geometry = b.get("geojson") or (
            {"type": "Point", "coordinates": b["indicative_point"]}
            if b.get("indicative_point")
            else None
        )
        if geometry:
            p = props(e)
            p["location_precision"] = "boundary" if b.get("geojson") else "indicative"
            placed.append({"type": "Feature", "id": e["id"], "geometry": geometry, "properties": p})
        else:
            unplaced.append(e)
    os.makedirs("gaia", exist_ok=True)
    with open(os.path.join("gaia", "commons-registry.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": placed}, f, indent=2, ensure_ascii=False)
    # Global and network commons have no single place. They are listed in the
    # manifest's `unplaced` entry, not drawn, so the map never implies one.
    manifest = {
        "source": "commons",
        "name": "Global Commons",
        "homepage": REPO,
        "licence": "CC BY 4.0",
        "layers": [
            {
                "id": "registry",
                "file": "commons-registry.geojson",
                "name": "Global Commons registry",
                "description": "Commons in the Global Commons registry that have a place on the map, each with its step on the rules ladder (1 no rules, 2 weak rules, 3 rules that don't pay out). Points marked indicative are candidate areas, not boundaries or claims.",
                "h3_resolutions": [4],
                "attribution": ["Global Commons Initiative, Hub Culture and contributors (CC BY 4.0)"],
            }
        ],
        "unplaced": [
            {"slug": e["id"], "name": e["name"], "kind": e["kind"], "ladder_step": e["ladder_step"], "boundary_type": e["boundaries"]["type"]}
            for e in unplaced
        ],
    }
    with open(os.path.join("gaia", "layers.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"{len(placed)} placed, {len(unplaced)} unplaced")


if __name__ == "__main__":
    main()
