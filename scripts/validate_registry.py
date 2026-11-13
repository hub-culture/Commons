"""Validate data/registry/*.json against schema/commons.schema.json, then apply the
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
# The projects board (data/projects.json): unique ids, a known status,
# something to ask for, and https links.
STATUSES = {"live", "seed", "in-design", "seeking-partners"}
seen = set()
for proj in json.load(open("data/projects.json")):
    pid = proj.get("id")
    if not pid or pid in seen:
        report("data/projects.json", proj, "missing or duplicate id")
    seen.add(pid)
    if proj.get("status") not in STATUSES:
        report("data/projects.json", proj, f"status must be one of {sorted(STATUSES)}")
    if not proj.get("summary") or not proj.get("input_wanted"):
        report("data/projects.json", proj, "needs a summary and at least one thing it wants input on")
    for link in proj.get("links", []):
        if not link.get("url", "").startswith("https://"):
            report("data/projects.json", proj, f"link {link.get('label')!r} must be https")

print("ok" if not errors else f"{errors} error(s)")
sys.exit(1 if errors else 0)
