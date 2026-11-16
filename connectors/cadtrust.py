"""Read carbon credit records from the CAD Trust network, read-only, and link them
to sites in the open blue carbon registry.

Why CAD Trust: registries built on the UNDP National Carbon Registry (and other
connected registries) publish their projects, locations, issuances and unit
retirements to the CAD Trust network under its Data Model v2. Anyone can read
that data through a read-only observer node. Reading it there means one
connector covers every connected registry, and no registry has to give us an
account.

This module never writes to CAD Trust or to any registry.

Data model v2, as used here (resource paths are under /v2):
    project               cadTrustProjectId, projectName, projectDescription, projectSector[], projectType[], projectStatus, projectRegistryName, projectLink
    location              cadTrustLocationId, cadTrustProjectId, locationCountry, locationRegion, locationGis
    verification          cadTrustVerificationId, cadTrustProjectId
    project-methodology   cadTrustProjectMethodologyId, cadTrustProjectId
    issuance              cadTrustIssuanceId, cadTrustVerificationId, cadTrustProjectMethodologyId
    unit                  cadTrustUnitId, cadTrustIssuanceId, unitCount, unitStatus, unitVintageYear, unitSerialId
List endpoints take ?page=&limit= (limit 1-1000) and return {"data": [...], "pageCount": n}.
"""
from __future__ import annotations

import json
import math
import urllib.parse
import urllib.request
from collections import defaultdict
from typing import Iterable

RESOURCES = {
    "project": "/project",
    "location": "/location",
    "verification": "/verification",
    "project_methodology": "/project-methodology",
    "issuance": "/issuance",
    "unit": "/unit",
}

# CAD Trust's v2 picklists have no blue carbon sector or type yet, so blue
# carbon projects arrive filed under forestry or "Others". These words in a
# project's name, description or subtype mark it as a candidate.
BLUE_CARBON_WORDS = (
    "mangrove", "seagrass", "sea grass", "salt marsh", "saltmarsh", "tidal marsh",
    "tidal wetland", "coastal wetland", "blue carbon", "kelp", "mikoko",
)

RETIRED_STATUSES = {"retired", "cancelled"}


def fetch(node_url: str, limit: int = 1000, timeout: int = 30) -> dict[str, list[dict]]:
    """Read every record of each resource from a CAD Trust v2 node, page by page."""
    out: dict[str, list[dict]] = {}
    base = node_url.rstrip("/")
    for name, path in RESOURCES.items():
        rows: list[dict] = []
        page, page_count = 1, 1
        while page <= page_count:
            query = urllib.parse.urlencode({"page": page, "limit": limit})
            with urllib.request.urlopen(f"{base}/v2{path}?{query}", timeout=timeout) as resp:
                body = json.load(resp)
            data = body.get("data") or []
            if not data:
                break
            rows.extend(data)
            page_count = body.get("pageCount") or 1
            page += 1
        out[name] = rows
    return out


def is_blue_carbon(project: dict) -> bool:
    text = " ".join(
        str(project.get(k) or "") for k in ("projectName", "projectDescription", "projectSubtype")
    ).lower()
    return any(word in text for word in BLUE_CARBON_WORDS)


def point_of(location: dict) -> tuple[float, float] | None:
    """[lon, lat] from a location's locationGis (GeoJSON, as a string or object), if it has one."""
    gis = location.get("locationGis")
    if not gis:
        return None
    try:
        geo = json.loads(gis) if isinstance(gis, str) else gis
    except (TypeError, ValueError):
        return None
    coords = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "Feature":
                walk(node.get("geometry"))
            elif node.get("type") == "FeatureCollection":
                for f in node.get("features", []):
                    walk(f)
            else:
                walk(node.get("coordinates"))
        elif isinstance(node, list):
            if len(node) >= 2 and all(isinstance(v, (int, float)) for v in node[:2]):
                coords.append((float(node[0]), float(node[1])))
            else:
                for item in node:
                    walk(item)

    walk(geo)
    if not coords:
        return None
    return (sum(c[0] for c in coords) / len(coords), sum(c[1] for c in coords) / len(coords))


def distance_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    lon1, lat1, lon2, lat2 = map(math.radians, (*a, *b))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(h))


def credit_totals(records: dict[str, list[dict]]) -> dict[str, dict]:
    """Issued, retired and held tCO2e for each project, following unit -> issuance -> project."""
    project_of_verification = {v["cadTrustVerificationId"]: v["cadTrustProjectId"] for v in records.get("verification", [])}
    project_of_pm = {m["cadTrustProjectMethodologyId"]: m["cadTrustProjectId"] for m in records.get("project_methodology", [])}
    project_of_issuance = {}
    for i in records.get("issuance", []):
        pid = project_of_verification.get(i.get("cadTrustVerificationId")) or project_of_pm.get(i.get("cadTrustProjectMethodologyId"))
        if pid:
            project_of_issuance[i["cadTrustIssuanceId"]] = pid
    totals: dict[str, dict] = defaultdict(lambda: {"issued_tco2e": 0.0, "retired_tco2e": 0.0, "vintages": set()})
    for u in records.get("unit", []):
        pid = project_of_issuance.get(u.get("cadTrustIssuanceId"))
        if not pid:
            continue
        count = float(u.get("unitCount") or 0)
        t = totals[pid]
        t["issued_tco2e"] += count
        if str(u.get("unitStatus", "")).lower() in RETIRED_STATUSES:
            t["retired_tco2e"] += count
        if u.get("unitVintageYear"):
            t["vintages"].add(int(u["unitVintageYear"]))
    return {pid: {**t, "vintages": sorted(t["vintages"])} for pid, t in totals.items()}


def candidates(records: dict[str, list[dict]], sites: Iterable[dict], radius_km: float = 25.0) -> list[dict]:
    """Projects on the network that may belong to a registry site.

    A project is proposed for a site when it reads as blue carbon and its
    location lies within radius_km of the site, or when it reads as blue carbon
    in the same country and has no usable location. These are candidates only:
    a person who knows the site confirms a link, and the link then carries its
    sources like any other claim.
    """
    sites = list(sites)
    locations: dict[str, list[dict]] = defaultdict(list)
    for loc in records.get("location", []):
        locations[loc.get("cadTrustProjectId")].append(loc)
    totals = credit_totals(records)
    out = []
    for project in records.get("project", []):
        if not is_blue_carbon(project):
            continue
        pid = project["cadTrustProjectId"]
        points = [p for p in (point_of(l) for l in locations.get(pid, [])) if p]
        countries = {str(l.get("locationCountry") or "").lower() for l in locations.get(pid, [])}
        for site in sites:
            site_point = tuple(site["location"]["point"])
            match, dist = None, None
            if points:
                dist = min(distance_km(site_point, p) for p in points)
                if dist <= radius_km:
                    match = "within-radius"
            elif site.get("country_name", "").lower() in countries:
                match = "same-country-no-location"
            if match:
                t = totals.get(pid, {"issued_tco2e": 0.0, "retired_tco2e": 0.0, "vintages": []})
                out.append({
                    "site": site["id"],
                    "cadtrust_project_id": pid,
                    "project_name": project.get("projectName"),
                    "registry": project.get("projectRegistryName"),
                    "registry_project_id": project.get("projectId"),
                    "project_link": project.get("projectLink"),
                    "match": match,
                    "distance_km": round(dist, 1) if dist is not None else None,
                    "issued_tco2e": t["issued_tco2e"],
                    "retired_tco2e": t["retired_tco2e"],
                    "vintages": t["vintages"],
                })
    return out
