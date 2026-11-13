"""Validate data/registry/*.json against schema/commons.schema.json (and the blue carbon
sites and practices against theirs), then apply the
Bermuda Standard lineage rule: a claim marked settled needs at least min_lineages
(default 2) distinct supporting lineages, and none contradicting it."""
import glob, json, sys
from jsonschema import Draft202012Validator

FLOOR = 2
schema = json.load(open("schema/commons.schema.json"))
v = Draft202012Validator(schema)
errors = 0


def report(path, entry, msg):
    global errors
    errors += 1
    print(f"{path} [{entry.get('id')}] {msg}")


def check_claims(path, entry):
    for i, c in enumerate(entry.get("claims", [])):
        need = max(FLOOR, c.get("min_lineages", FLOOR))
        ev = c.get("evidence", [])
        pro = {e["lineage"].strip().lower() for e in ev if e.get("supports")}
        con = {e["lineage"].strip().lower() for e in ev if e.get("supports") is False}
        status = c.get("status")
        if status == "settled" and (len(pro) < need or con):
            report(path, entry, f"claims/{i}: settled needs {need} independent supporting lineages and none against; has {len(pro)} for, {len(con)} against")
        if status == "contested" and not (pro and con):
            report(path, entry, f"claims/{i}: contested needs evidence on both sides")


for path in sorted(glob.glob("data/registry/*.json")):
    for entry in json.load(open(path)):
        for e in v.iter_errors(entry):
            report(path, entry, f"{'/'.join(map(str, e.path))}: {e.message}")
        check_claims(path, entry)

# Blue carbon sites and practices (docs/blue-carbon-registry.md).
commons_ids = {e.get("id") for p in glob.glob("data/registry/*.json") for e in json.load(open(p))}
for pattern, schema_path in [("data/blue-carbon/*.json", "schema/blue-carbon-site.schema.json"),
                             ("data/practices/*.json", "schema/practice.schema.json")]:
    sv = Draft202012Validator(json.load(open(schema_path)))
    seen = set()
    for path in sorted(glob.glob(pattern)):
        for entry in json.load(open(path)):
            for e in sv.iter_errors(entry):
                report(path, entry, f"{'/'.join(map(str, e.path))}: {e.message}")
            if entry.get("id") in seen:
                report(path, entry, "duplicate id")
            seen.add(entry.get("id"))
            if "commons" in entry and entry["commons"] not in commons_ids:
                report(path, entry, f"commons {entry['commons']!r} is not in data/registry")

print("ok" if not errors else f"{errors} error(s)")
sys.exit(1 if errors else 0)
