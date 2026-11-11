"""Render docs/lineage-map.html from data/lineage/lineage.json."""
import json, os
here = os.path.dirname(__file__)
data = json.load(open(os.path.join("data", "lineage", "lineage.json")))
tpl = open(os.path.join(here, "lineage_template.html")).read()
os.makedirs("docs", exist_ok=True)
open(os.path.join("docs", "lineage-map.html"), "w").write(tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False)))
print("wrote docs/lineage-map.html")
