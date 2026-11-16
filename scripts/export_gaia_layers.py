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
    # The open blue carbon registry: one point per site, with its keepers,
    # how many claims have settled, and any credits other registries issued.
    sites = json.load(open(os.path.join("data", "blue-carbon", "sites.json")))
    site_features = []
    for s in sites:
        settled = sum(1 for c in s["claims"] if c["status"] == "settled")
        site_features.append({
            "type": "Feature",
            "id": s["id"],
            "geometry": s["location"].get("boundary") or {"type": "Point", "coordinates": s["location"]["point"]},
            "properties": {
                "slug": s["id"],
                "name": s["name"],
                "ecosystems": ", ".join(s["ecosystems"]),
                "country": s["country"],
                "area_ha": s.get("area_ha"),
                "keepers": "; ".join(k["name"] for k in s["keepers"]),
                "claims_settled": settled,
                "claims_total": len(s["claims"]),
                "credit_registries": ", ".join(sorted({c["registry"] for c in s["credit_links"]})),
                "status": s["status"],
                "location_precision": s["location"]["precision"],
                "registry_url": f"{REPO}/blob/main/data/blue-carbon/sites.json",
            },
        })
    with open(os.path.join("gaia", "blue-carbon-sites.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": site_features}, f, indent=2, ensure_ascii=False)
    manifest["layers"].append({
        "id": "blue-carbon",
        "file": "blue-carbon-sites.geojson",
        "name": "Open blue carbon registry",
        "description": "Blue carbon sites (mangroves, seagrass, salt marsh): who keeps them, how many claims about them have settled on independent evidence, and which registries have issued credits for them. The registry records; it does not issue or sell credits.",
        "h3_resolutions": [6],
        "attribution": ["Global Commons Initiative and contributors (CC BY 4.0); sources listed per claim"],
    })
    with open(os.path.join("gaia", "layers.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"{len(placed)} placed, {len(unplaced)} unplaced, {len(site_features)} blue carbon sites")


if __name__ == "__main__":
    main()
