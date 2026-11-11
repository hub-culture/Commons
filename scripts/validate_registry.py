"""Validate data/registry/*.json against schema/commons.schema.json."""
import glob, json, sys
from jsonschema import Draft202012Validator

schema = json.load(open("schema/commons.schema.json"))
v = Draft202012Validator(schema)
errors = 0
for path in sorted(glob.glob("data/registry/*.json")):
    for entry in json.load(open(path)):
        for e in v.iter_errors(entry):
            errors += 1
            print(f"{path} [{entry.get('id')}] {'/'.join(map(str, e.path))}: {e.message}")
print("ok" if not errors else f"{errors} error(s)")
sys.exit(1 if errors else 0)
