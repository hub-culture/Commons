import json
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
from connectors import cadtrust  # noqa: E402

RECORDS = json.load(open(os.path.join(ROOT, "tests", "fixtures", "cadtrust_sample.json")))
SITES = json.load(open(os.path.join(ROOT, "data", "blue-carbon", "sites.json")))


class CadTrustTest(unittest.TestCase):
    def test_blue_carbon_words(self):
        names = {p["cadTrustProjectId"]: cadtrust.is_blue_carbon(p) for p in RECORDS["project"]}
        self.assertEqual(names, {"p-blue": True, "p-far": True, "p-solar": False, "p-noloc": True})

    def test_point_from_gis(self):
        self.assertEqual(cadtrust.point_of({"locationGis": '{"type":"Point","coordinates":[39.85,-4.43]}'}), (39.85, -4.43))
        lon, lat = cadtrust.point_of(RECORDS["location"][1])
        self.assertAlmostEqual(lon, 40.84, places=2)
        self.assertIsNone(cadtrust.point_of({"locationGis": "not json"}))
        self.assertIsNone(cadtrust.point_of({}))

    def test_credit_totals_follow_unit_to_project(self):
        t = cadtrust.credit_totals(RECORDS)["p-blue"]
        self.assertEqual((t["issued_tco2e"], t["retired_tco2e"], t["vintages"]), (1400.0, 400.0, [2024, 2025]))

    def test_candidates(self):
        found = {(c["site"], c["cadtrust_project_id"]): c for c in cadtrust.candidates(RECORDS, SITES, 25)}
        near = found[("mikoko-pamoja", "p-blue")]
        self.assertEqual(near["match"], "within-radius")
        self.assertLess(near["distance_km"], 5)
        self.assertEqual(near["retired_tco2e"], 400.0)
        # Too far away, not blue carbon, or matched by country only.
        self.assertNotIn(("mikoko-pamoja", "p-far"), found)
        self.assertNotIn(("mikoko-pamoja", "p-solar"), found)
        self.assertEqual(found[("mikoko-pamoja", "p-noloc")]["match"], "same-country-no-location")


if __name__ == "__main__":
    unittest.main()
