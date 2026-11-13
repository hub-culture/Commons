# What the Hub stack already gives the Global Commons

*Working note, 13 November 2026, written for the Global Commons Trust community workshop at COP31. It reviews pieces Hub Culture has already built (the QEM knowledge layer, the Bermuda Standard, Mandala agent Lineages, DIRT territories, Gaia and the off-grid mesh) and asks one question of each: what does it lend the commons? Proposals are marked as proposals; everything else describes what exists.*

## The short answer

Most of Elinor Ostrom's eight design principles already have a working part somewhere in the stack. Those parts were built for other jobs: verifying ocean data, holding AI agents to account, launching place-based tokens. The Global Commons doesn't need to invent them. It needs to connect them and let each community set its own rules for them through Propel.

| Ostrom's principle | What already does it | Where |
|---|---|---|
| 1. Clear boundaries | Places are addressed as H3 cells on one shared map. DIRT territories must sit inside one country, cover under a quarter of it and not overlap a registered territory. EEZ boundaries are kept as data with their source. | Gaia, DIRT, QEM |
| 2. Rules fit local conditions | Each community writes its own charter, with its own majorities, quorum and locks. A DIRT territory reserves a share for its local steward. | Cloud Mirror, DIRT |
| 3. Those affected make the rules | A new jurisdiction for agents is added only after members approve it through Propel. Community charter changes are designed to go through Propel votes. | Propel, Mandala |
| 4. Monitoring | A claim counts as settled only when independent sources agree, never because one source repeats it. Reviewers never review their own contributions. | QEM, Bermuda Standard |
| 5. Graduated sanctions | An agent's required stake starts at zero and rises one rung with each abuse flag, and never falls back. A refuted claim is snuffed, but kept on record rather than deleted. | Mandala, QEM |
| 6. Cheap conflict resolution | Every jurisdiction an agent can choose names its dispute forum. When two sources disagree, the disagreement is kept as evidence, not overwritten. | Mandala, QEM |
| 7. Right to organise is recognised | Another network's agent records count once that network joins as a connector or validator. Nothing else is needed. | Mandala |
| 8. Nested layers | The Bermuda Standard is the default charter. Cloud Mirrors adopt it and add their own rules. Communities sit inside them. Data shards merge into one picture without a central editor. | Bermuda Standard, Cloud Mirror, QEM |

## Each piece, and what it lends

### The QEM: monitoring by independent lineages

The QEM is Hub's knowledge layer. It stores each bit of data (a "speck") with its source, licence and consent. A speck starts unlit. It lights up only when **independent lineages** agree: a tide gauge and a satellite, say, or two different ocean models. One source repeating itself adds nothing. The design goes further for agents: a thousand AI agents built on the same model are to count as **one** voice, not a thousand (written into the design, not yet built). It already reads public ocean and climate sources and writes them out as Gaia layers, each with its licence.

**For the commons:**
- **Monitoring without a monitor.** Ostrom found that commons last when the users themselves can check one another cheaply. Triangulation by independent sources is that check, done in the open.
- **Stories as data.** A community's testimony is one lineage. A registry is another. Satellite data is a third. A claim about a commons (this reef recovered, this forest is being cleared) can be held to the same rule: it settles when separate lines of evidence agree, so local knowledge carries real weight without having to be taken on trust.
- **Truth over popularity.** Repetition and attention never light a claim. That protects a commons from being steered by whoever shouts loudest, or by swarms of agents.

**Proposal:** the rules on what counts as an independent lineage, and how certain is certain enough, should be set by each community through Propel, within a floor set by the Bermuda Standard. That makes the QEM's open question about thresholds a polycentric decision rather than a central one.

### The Bermuda Standard: a data charter of five rules

The Bermuda Standard sets five rules for a number to count: **provenance, lineage, agreement, licence and consent, and signature**. The Bermuda Climate Data Engine applies them to climate records, with Bermuda as its anchor station, and its site lists every source with its licence.

**For the commons:** these five rules are a ready-made charter for any data commons, including the open ocean data and blue carbon registries feeding Gaia. A community can adopt them as written and add its own.

### Mandala: holding AI agents to account

Every agent on HubID has a **Lineage**: the line it traces back to an accountable person or entity.
- An agent can bond to a beneficial owner, or stay unbound. An unbound agent is reviewed by general administration at a set interval.
- Its required stake rises with each abuse flag and never falls.
- Its Lineage names a jurisdiction: the Bermuda Standard charter by default, or a City or Stewarded Cloud Mirror that members have approved through Propel. Each jurisdiction names a dispute forum.
- Large payments wait for human approval.

**For the commons:** this is the "governing the AI shepherd" principle, already working. It answers Laura Stein's worry about the agent levy too. Access points (registration, payments, jurisdiction) are gated, so the rules apply to every agent that uses them, rather than relying on agents opting in.

**Proposal:** a share of agent stakes, or a small fee on verification work metered in Ven, flows to the commons treasury, as the agent levy discussed in the sessions.

### DIRT and Gaia: boundaries and bankability

DIRT ties a value layer to a mapped polygon on Gaia: an island, old town, valley or gathering ground. The rules are strict:
- It is never a nation.
- It is never in a place that issues its own currency.
- It never overlaps another registered territory.
- A fixed share goes to the local steward and to the community.

Every territory is addressed by H3 cells and exported as a Gaia layer, in the same shape as the commons registry layer.

**For the commons:** DIRT shows how a bounded place can carry value back to its stewards, which is the bankability principle. Gaia's shared cell addresses mean a commons, a DIRT territory, a Cloud Mirror community and a Coalition project can all be shown on one map, so overlaps are visible.

**Proposal:** a DIRT territory that falls inside a registered commons should need that commons' consent, recorded through Propel, before it launches.

### Ultra and Ven: tokenised assets

Ultra has just been rebuilt for tokenised assets inside Hub's own system. A status page for six blockchains is ready for further work. Bringing Ven and tokenised assets to other chains is on hold while Gaia comes first.

**For the commons:** when the perpetual trusts discussed with Laura Stein hold land or ecosystem assets, Ultra is the natural place to represent shares in them. The commons should adopt it only after the API and security hardening now under way are complete.

### The off-grid mesh: local-first

Hub's edge mesh is off-grid messaging over Bluetooth and Wi-Fi, compatible with Bitchat. It is tied to HubID, can settle Ven transfers, and has a gateway into Hub threads through edge pods.

**For the commons:** commons are often where connectivity is weakest. A mesh lets a fishing community or a forest guard post take part (reporting, voting, receiving payment) and sync when a gateway is in reach. That is local-first in practice, and it carries the "edge to centre" idea from the Laura Stein session.

*Naming note:* this repo is called `mesh`, while the workshop calls the whole structure "the mesh". Name the edge network "the edge mesh" so the two don't get confused. Similarly, `data/lineage` in this repo means Ostrom's academic lineage, not data lineage in the QEM sense.

## What this changes in the plan

1. **Registry claims go through triangulation.** Each commons entry in `data/registry` should name the sources behind its claims and how many independent lineages agree, following the Bermuda Standard's five rules.
2. **Communities set their own verification rules** in their Cloud Mirror charter, within the Bermuda Standard floor.
3. **Agent rules come from Mandala.** The commons uses Lineage, stakes and jurisdictions as they are, and adds the levy proposal.
4. **One map.** Commons, DIRT territories, Cloud Mirror communities and Coalition projects all appear as Gaia layers on shared H3 cells.
5. **Edge participation.** Pilot the edge mesh with one commons that has poor connectivity.

See also [cloud-mirror.md](cloud-mirror.md), [coalitions.md](coalitions.md) and [roadmap.md](roadmap.md).
