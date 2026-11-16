"""Propose links between open blue carbon registry sites and projects on the CAD Trust network.

    python scripts/link_cadtrust.py --node https://<observer-node>      # read live, read-only
    python scripts/link_cadtrust.py --records tests/fixtures/cadtrust_sample.json

Prints candidate links as JSON. It never edits the registry: a person who knows
the site confirms a candidate and adds it to the site's credit_links with its source.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from connectors import cadtrust  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--node", help="Base URL of a CAD Trust v2 observer node")
    src.add_argument("--records", help="A JSON file of CAD Trust v2 records, keyed by resource")
    ap.add_argument("--sites", default="data/blue-carbon/sites.json")
    ap.add_argument("--radius-km", type=float, default=25.0)
    args = ap.parse_args()
    records = cadtrust.fetch(args.node) if args.node else json.load(open(args.records))
    sites = json.load(open(args.sites))
    print(json.dumps(cadtrust.candidates(records, sites, args.radius_km), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
