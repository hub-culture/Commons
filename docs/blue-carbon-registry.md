# The open blue carbon registry

*Version 0, 16 November 2026. In design and open for input.*

An open, public record of blue carbon ecosystems (mangroves, seagrass meadows, salt marshes and other coastal wetlands). For each site it records where it is and who keeps it, what is claimed about it and on what evidence, what was promised to its keepers and what reached them, and which credits other registries have issued for it.

**It records; it never issues, holds or sells credits.** Credits stay in the registries that issue them. This registry links to them, so anyone can see whether the money behind a credit reached the people who keep the place.

## What's here

| Path | What it is |
|---|---|
| [`schema/blue-carbon-site.schema.json`](../schema/blue-carbon-site.schema.json) | One site: ecosystems, location, area, tenure, keepers, claims, payments, credit links, consent, status |
| [`data/blue-carbon/sites.json`](../data/blue-carbon/sites.json) | The sites. The first is Mikoko Pamoja at Gazi Bay, Kenya, a community-led mangrove project, listed as a candidate until its keepers confirm it |
| [`connectors/cadtrust.py`](../connectors/cadtrust.py) | Reads credit records from the CAD Trust network, read-only, and proposes links to sites |
| [`scripts/link_cadtrust.py`](../scripts/link_cadtrust.py) | Command line for the connector |
| [`gaia/blue-carbon-sites.geojson`](../gaia/blue-carbon-sites.geojson) | The sites as a Gaia map layer (`commons.blue-carbon`) |

## The rules

- **Every claim carries its evidence.** Source, lineage, licence and consent, the same as the commons registry. A claim settles only when at least two independent lineages support it and none contradicts it. The validator enforces this on every change.
- **Keepers come first.** A site stays a `candidate` until the people who keep it confirm what is published about it. Boundaries are published only when the keepers agree.
- **Payments are tracked as promised or paid,** each with its source, so the gap between the two is visible.
- **Indigenous and community data stays theirs.** Nothing about people is published without consent, and traditional knowledge is recorded on its holders' terms.

## Linking to national registries through CAD Trust

Many countries run national carbon registries built on the [UNDP National Carbon Registry](https://github.com/undp/undp-national-carbon-registry), an open-source digital public good maintained by UNDP. Those registries publish each project, its location, issuances and retirements to the CAD Trust network (Data Model v2). Anyone can read that data through a read-only observer node.

So the connector reads CAD Trust, not each registry. One connector covers every connected registry, and no registry has to give us an account. It follows each unit back to its project (unit, issuance, verification or project methodology, project) to total what was issued and retired. It then proposes a link when a project reads as blue carbon and its location falls near a site.

CAD Trust's v2 picklists have no blue carbon sector or type yet, so blue carbon projects are filed under forestry or "Others". The connector recognises them by words in the project's name and description. Proposed links are **candidates**: a person who knows the site confirms them, and the link then goes into the site's `credit_links` with its source.

```
python scripts/link_cadtrust.py --node https://<cad-trust-observer-node>
python scripts/link_cadtrust.py --records tests/fixtures/cadtrust_sample.json   # synthetic test data
```

The connector only reads. It never writes to CAD Trust or to any registry. It is our own code under this repository's MIT licence; it uses CAD Trust's published data model and no code from the AGPL-licensed UNDP registry.

## Gaps this work could close upstream

Found while reading the UNDP registry's code (as of its 5 November 2026 commit):

1. **No blue carbon categories.** Neither the registry's sectors nor CAD Trust's picklists have mangrove, seagrass or salt-marsh types.
2. **One location per project.** Multi-site projects send a single location, and empty location fields can arrive as the placeholder "test".
3. **Locations as text and points.** Boundaries and map cells would let sites be compared with protected areas and ecosystem maps.
4. **No record of keepers or benefit flows.** Who keeps a site, and what reached them, sits outside the credit record.

## Next steps

1. Connect to a live CAD Trust observer node and run the connector against real data.
2. Confirm Mikoko Pamoja's entry with its keepers, and add sites with partners who keep them.
3. Work with Xeptagon and UNDP on the upstream gaps above.
4. Map sites against marine protected areas and the Ocean Data Initiative layers on Gaia.
