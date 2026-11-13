# The Open Blue Carbon Registry

Draft v0.1, 13 November 2026. Open for comment: file an issue or a pull request.

The ocean is the Global Commons' first test case, and blue carbon is its first working module: an open-source registry of coastal carbon sites, the evidence for each, and who keeps them. It is a commons-first public good, onboarded through the [Ocean Climate Fund](https://oceanclimatefund.com) and checked by the open data of the [Ocean Data Initiative](https://github.com/hub-culture/Ocean).

## In one paragraph

Mangroves, tidal marshes and seagrass meadows hold some of the densest carbon on Earth and are still being lost. Money for them is held back by three things: nobody can see which sites exist and who keeps them, the evidence behind a site's carbon is locked inside each project's documents, and the people who keep the sites are rarely the ones paid. The registry answers all three in the open. Any community, scientist or developer can register a site. Every claim about it (its area, its carbon, its condition) is checked against independent public data and gets brighter as more independent sources agree. And each site names its keepers and how they are paid. **The registry does not issue carbon credits.** It is the open layer underneath: when a site is ready for credits, it hands its evidence to a standard (Verra's VM0033, through Hedera Guardian, is the natural first) instead of competing with one.

## Why the ocean first, and why blue carbon

The [framework](../framework/README.md) places each commons on the rules ladder. Coastal blue carbon is at **step 2, weak rules**: national laws and voluntary standards exist, but sites keep disappearing, and payouts rarely reach the people who keep them. It is a good first test because:

- **It is mapped.** Global Mangrove Watch maps mangroves at 30 m every year from 1985 to 2025, and the Coastal Carbon Network has published about 15,000 soil cores. A registry can check claims from day one.
- **It is bankable.** Buyers already pay for blue carbon, and a [digital version of VM0033](https://docs.hedera.com/guardian/guardian/demo-guide/carbon-offsets/vm0033-methodology-for-tidal-wetland-and-seagrass-restoration) already runs on Hedera Guardian, the platform the QEM is linked to.
- **It is local.** Every site has fishers, families and councils who decide whether it survives. That is the commons method in miniature.
- **It is the OCF's own category.** "Blue living carbon" is one of the Ocean Climate Fund's three investment categories, chosen by its member community.

## What counts as blue carbon here

Only **mangroves, tidal marshes and seagrass meadows** are blue carbon ecosystems in the IPCC's national inventory guidance (the 2013 Wetlands Supplement) and in today's carbon markets. The registry follows that line, and keeps a separate, clearly labelled class for everything else.

| Class | Ecosystems | In the registry |
| --- | --- | --- |
| `established` | Mangroves, tidal marshes, seagrass meadows | Full verification ladder, can reach `credit-ready` |
| `emerging` | Tidal forests other than mangroves, macroalgae and kelp, phytoplankton-based and other open-ocean approaches, shellfish reefs | Registered and evidenced, never `credit-ready` here until a recognised methodology exists. Marked as emerging on every view. |

This matters for the Fund's own pipeline: open-ocean and phytoplankton approaches have no recognised carbon methodology yet, and the science on how much carbon they store, and for how long, is unsettled. The registry can carry their evidence openly, which is exactly what they need, without implying they are equivalent to a restored mangrove.

## How a site moves through the registry

Each step is a status a site earns. Each one is visible on the Gaia map and is a [Cloud Mirror](cloud-mirror.md) ledger event.

| Status | What it takes | Who checks |
| --- | --- | --- |
| `registered` | A name, an ecosystem class, a rough location, a contact, and the keepers' consent to be listed (free, prior and informed consent where communities are involved) | The registry's validator |
| `mapped` | A boundary on Gaia (GeoJSON and H3 cells). The claimed area is checked against Global Mangrove Watch (mangroves) or the best available habitat map | The QEM, against public maps |
| `evidenced` | Carbon stock and condition claims, each lit by **at least two independent lineages** (for example: the site's own soil cores and the Coastal Carbon Network's regional cores; the site's own survey and satellite extent) | The QEM |
| `verified` | **Three or more lineages**, including field measurements and an independent reviewer (a validation/verification body or an accredited scientist) | The QEM, plus a named reviewer |
| `credit-ready` | Evidence packaged for a standard (VM0033 via Guardian first); the site's registry ID is recorded in the standard's registry, and vice versa | The standard |

A claim that independent sources contradict dims, as every QEM speck does. A site never loses its history: if a mangrove is cleared, its status steps back and the loss stays on the record.

## What the registry checks against

Every claim becomes a QEM speck with its source, licence and consent attached. The QEM triangulates it against independent lineages: the same rule it already applies to sea temperature and CO₂. These are the public sources each kind of claim is checked against. Global Mangrove Watch, the Coastal Carbon Library, BATS and SOCAT were added to the QEM's source registry (`hub-culture/qem` `sources/registry.json`) as candidates on 13 November 2026; Coral Reef Watch, OBIS and the ODI's sea temperature already run; Sentinel-2, WDPA, MPAtlas and the standards' project lists are still to add.

| Claim | Independent lineages |
| --- | --- |
| Area and change | Global Mangrove Watch v4.1 (30 m, 1985-2025); the site's own survey; Sentinel-2 imagery |
| Soil carbon stock | Coastal Carbon Network Data Library (≈15,000 cores); the site's own cores; IPCC Tier 1 defaults as the floor, never the answer |
| Condition and stress | NOAA Coral Reef Watch heat stress (adjacent reefs), sea temperature from the Ocean Data Initiative, OBIS species records |
| Protection status | Protected Planet (WDPA) and MPAtlas, cross-checked with national designations |
| Ocean context | BIOS BATS and SOCAT for the carbon chemistry of adjacent water (relevant to seagrass and to any open-ocean claim) |
| Not counted twice | The site's boundary against the public project lists of Verra, Gold Standard and Plan Vivo; overlapping H3 cells are flagged |

## The records

Two record types, both JSON, both open (CC BY 4.0 unless a source's own terms say otherwise).

**A site** ([`schema/blue-carbon-site.schema.json`](../schema/blue-carbon-site.schema.json)): identity, ecosystem and class, boundary, status, keepers, rights, claims with their evidence, external registrations, and remuneration. Seeds are in [`data/blue-carbon/sites.json`](../data/blue-carbon/sites.json).

**A practice** ([`schema/practice.schema.json`](../schema/practice.schema.json)): a reusable way of doing something well in a commons (how to set MPA protection levels, how to measure soil carbon, how to share benefits with keepers), with where it has worked and the evidence. Seeds are in [`data/practices/seed.json`](../data/practices/seed.json).

Practices are how the Global Commons becomes a wider ingestion point. Every commons, starting with the ocean, contributes the practices that worked for it; the next commons starts from them. Blue carbon MRV and MPA governance are the first two families. The MPA best-practices plan the Ocean Climate Fund is preparing with Oceano Azul for the BBNJ process can enter here practice by practice.

## Onboarding from the Ocean Climate Fund

The registry is how a site enters the Fund's pipeline, and how the Fund's community sees it.

```
 oceanclimatefund.com/portfolio ── "Blue carbon registry"
            │
            ▼
   Register a site  (form → registry entry, status: registered)
            │
            ▼
   Gaia blue carbon layer  (boundary, GMW extent, ODI layers beneath)
            │
            ▼
   QEM checks each claim  ──►  status: mapped → evidenced
            │
            ▼
   OCF community sees the pipeline as deal flow; members vote
            │
            ▼
   OCF micro-funding pays for the missing evidence
   (soil cores, a survey, a reviewer)  ──►  status: verified
            │
            ▼
   Standard (VM0033 via Guardian)  ──►  credit-ready / credits issued elsewhere
            │
            ▼
   A share of every payout reaches the keepers, recorded on the ledger
```

Two things make this work for the Fund. First, micro-funding has a precise use: paying for the evidence a promising site lacks, which is cheap compared with the value it unlocks. Second, the Fund's 50+ member organisations get a single, open view of blue carbon sites around the Atlantic Rim, with the evidence attached, instead of pitch decks.

## Keepers and remuneration

The framework's rule applies: rights come with responsibilities, and payouts convert into what the keepers value. Each site records:

- **Keepers:** the community, cooperative, agency or owner who looks after it, by role, never by personal name unless they ask to be named.
- **Rights and responsibilities:** tenure, access and use, paired with monitoring and protection duties.
- **Remuneration:** the mechanism (OCF grant, credit revenue, the Gaia virtual ocean layer), the keepers' share, and what it converts into locally.

A default keepers' share, and how it is enforced through the Cloud Mirror treasury (escrow, milestone tranches, steward quorum), is an open question for the first pilot community to decide, not for this document.

## Integrity rules (proposed)

1. **Open by default.** Every claim, source and status change is public. Personal data is never stored; community details appear only with consent.
2. **Independent lineages only.** A claim repeated by many copies of one source counts once. A project's own consultants are one lineage.
3. **No double counting.** One site, one boundary. Overlaps with other registries are flagged and must be resolved before `credit-ready`.
4. **Permanence is a claim too.** Sea-level rise, erosion and grazing risks are recorded and checked (VM0033 uses Verra's AFOLU non-permanence tool for sea-level rise; the registry carries the same assessment). Bermuda's seagrass, where green turtle overgrazing has driven widespread loss, shows why condition must be watched, not assumed.
5. **The registry doesn't sell.** It never issues, holds or trades credits. Value flows through standards and the commons treasury.
6. **Govern the shepherd.** Where the QEM or Zeke scores a claim, the reasons are shown and a human reviewer can override, with the override on the ledger.

## Build plan

| When | What |
| --- | --- |
| Now | This design, the two schemas, seed sites and practices, validation in CI |
| By end of November | QEM readers for Global Mangrove Watch and the Coastal Carbon Library; first `mapped` checks on the seed sites |
| December | Gaia blue carbon layer; a "Register a site" form on oceanclimatefund.com writing registry entries; OCF Portfolio page link |
| Davos 2027 | First pilot site with its keepers, taken to `evidenced`; a Guardian export of its evidence in VM0033 shape |
| After | The `emerging` class's evidence model (with the open-ocean pipeline), the practices library opened to other commons |

## Open questions

- **Which pilot?** The seeds are candidates, not endorsements. The pilot is chosen with its community.
- **Who reviews?** For `verified`, an accredited verification body, a named scientist, or either?
- **Keepers' share.** A default, or set per site by its keepers?
- **Lineages.** Who decides when two sources are really one (the same question open in the QEM)?
- **Practices.** Who may add one, and what evidence lights it?
