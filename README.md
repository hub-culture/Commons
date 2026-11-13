# Commons

An open initiative to map, strengthen and fund the global commons, started by Hub Culture at the COP31 Climate Campus in Antalya (November 2026).

The global commons already exists. Oceans, the atmosphere, genetic resources, the savannah, outer space and now the networks where AI agents meet are all shared, and most already run on some rules. What's missing is rules that are strong enough, local enough, and that pay back the people who keep them. This repository is where we build that: open data, an open framework, and open code.

## What's here now

| Path | What it is |
| --- | --- |
| [`framework/`](framework/) | The working framework: the rules ladder, the parts of commons infrastructure, the method, and design principles from Elinor Ostrom's work and the COP31 sessions. |
| [`data/lineage/`](data/lineage/) | **Library of the Commons, first pass.** 149 scholars in Elinor Ostrom's lineage (Workshop PhDs and affiliated faculty), tiered and themed, as CSV and JSON. |
| [`docs/lineage-map.html`](docs/lineage-map.html) | An interactive map of that lineage. Open it in any browser. |
| [`data/registry/`](data/registry/) | A seed registry of commons, each placed on the rules ladder, in the format Gaia map layers will use. |
| [`schema/`](schema/) | JSON Schema for registry entries. |
| [`gaia/`](gaia/) | The registry as a **Gaia synced source** (manifest plus GeoJSON). Add `commons=https://raw.githubusercontent.com/hub-culture/Commons/main/gaia/layers.json` to Gaia's `GAIA_SOURCES` and it appears as the `commons.registry` layer. Rebuild with `python scripts/export_gaia_layers.py`. |
| [`docs/cloud-mirror.md`](docs/cloud-mirror.md) | How the Global Commons connects to Cloud Mirror, Propel, Gaia, Mandala and Ven. |
| [`docs/coalitions.md`](docs/coalitions.md) | How Coalitions, Cloud Mirror communities and the Global Commons fit one structure: communities, projects, treasuries and one decision engine. |
| [`docs/case-studies.md`](docs/case-studies.md) | Cases from the COP31 sessions: Sharm el-Sheikh vs Cancún, Maine lobster, the Cali Fund, planetary protection and more. |
| [`docs/hub-stack-and-the-commons.md`](docs/hub-stack-and-the-commons.md) | What Hub's existing pieces (QEM, Bermuda Standard, Mandala, DIRT, Gaia, Ultra, the edge mesh) lend the commons, mapped to Ostrom's eight principles. |
| [`docs/roadmap.md`](docs/roadmap.md) | What we're building next and how to help. |

## The idea in one paragraph

Commons fail at one of three steps: **no rules**, **weak rules**, or **rules that don't pay out**. The best rules are contracts written by the people who use a commons, and they are almost always local. So the work is to convene everyone who uses a commons, including the people who don't want one; map it, across all its seasons; write its rules, rights and responsibilities as contracts; pay its keepers in what they value; and scale what works into regulation. AI now makes it possible to read the whole literature on the commons and still give place-specific answers. We think the same framework is urgently needed for AI agents, which will soon number in the billions.

## Getting started

```bash
git clone https://github.com/hub-culture/Commons.git
cd Commons

# Rebuild the lineage data and map
python scripts/build_lineage.py
python scripts/render_lineage_map.py

# Check the registry against its schema
pip install jsonschema
python scripts/validate_registry.py

# Export the registry as a Gaia layer
python scripts/export_gaia_layers.py
```

## Contributing

We especially want:

- **Scholars of the commons**, above all the Ostrom lineage, to correct and extend the map.
- **Communities that keep a commons**, to add their commons to the registry, in their own terms.
- **Developers**, to build the Gaia layer, the registry API and the agent-governance spoke.

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), then open an issue or a pull request.

## License

Code is under the [MIT License](LICENSE). Data and documents are under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless a file says otherwise. Sources keep their own terms; each dataset names its source.

## Learn more

- [Hub Culture](https://hubculture.com)
- [Ocean Climate Fund](https://oceanclimatefund.com) and its open [Ocean](https://github.com/hub-culture/Ocean) data repository
- [The Vincent and Elinor Ostrom Workshop](https://ostromworkshop.indiana.edu), Indiana University
