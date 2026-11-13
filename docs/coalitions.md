# Coalitions, Cloud Mirror and the Global Commons: one structure

Design note v0.1, 13 November 2026.

Hub Culture already runs Coalitions: people create a **system**, launch **coalitions** inside it to raise money for a goal, invite others to join and donate in Ven, and apply for **stimulus**. The Global Commons and Cloud Mirror need exactly these parts: a community, its projects, its members, its money. This note makes them one structure, so there's one way to govern, fund and map a commons, and so Coalitions become its project layer instead of a parallel system.

## The structure

```
 Cloud Mirror ── the layer: charters, standing, ledger, stewardship
   │
   ├─ Community (a Cloud Mirror spoke)  ◀── was: a Coalition "system"
   │    charter + governance, written in Propel
   │    commons treasury (escrowed, steward quorum)
   │    boundary on Gaia
   │    │
   │    ├─ Coalition (a project)          ◀── was: a coalition
   │    │    goal, budget, milestones, place on Gaia
   │    │    funded from the treasury and by direct gifts, released in tranches
   │    │
   │    └─ Members: people (HubID) and, where the charter allows, agents (Mandala)
   │
   └─ The Global Commons community
        one sub-community per commons in its registry, each with its own coalitions
```

Communities nest. The Global Commons is itself a community, and each commons in its registry (a marine protected area, a land trust, the AI agent commons) can become a community of its own, with its own charter, treasury and coalitions. That is Ostrom's eighth principle, nested enterprises.

## How each part maps

| Part | Coalitions today | In the shared structure |
| --- | --- | --- |
| **System** | A creator names it, picks a currency, and sets a transaction and a redemption commission. | **A Cloud Mirror community.** Creating a system creates a community with a founding charter. The commissions become the charter's **commons share**, set and changed by members through Propel, not by the creator alone. |
| **Coalition** | A fundraising goal with a name, description, amount and currency. | **A project inside a community**, with a budget, milestones, a precept or purpose alignment statement, and a place on Gaia. |
| **Approval** | One "authority monitor" approves or unapproves. | **The community's own process:** a Propel vote under its charter's thresholds, then steward review. |
| **Joining** | Subscribe to a coalition. | Join the **community** by accepting its charter. Follow or back any **coalition** inside it. |
| **Donations** | Ven goes straight to the coalition creator's personal account. | Ven goes to the **community's escrowed treasury**, earmarked for that coalition, and is released to a verified project steward in **milestone tranches**, with evidence and a steward quorum. Unspent funds return to the commons. |
| **Stimulus** | A system applies for an amount; the only refusal is "already applied". | **An allocation proposal**: a request for treasury funds, voted on in Propel under the community's threshold for money, then steward review. |
| **Banking details** | Held by the coalition site. | Held only for verified project stewards, never shown publicly. |
| **Records** | Database rows. | **Ledger entries**, hash-chained and anchored, so every vote, release and refund can be checked. |

## One decision engine

Charter amendments, project approvals and allocation requests are the same act: a member proposes, the community votes in Propel, the stewards review, and the outcome is written to the ledger. So they share one pipeline with three kinds of proposal.

| Proposal kind | Example | Threshold (community's choice) | Steward review |
| --- | --- | --- | --- |
| `charter` | Add a rule, change a precept, set governance, lock or unlock | Per change kind, as in the charter | Alignment veto, legal check |
| `project` | Approve a coalition, its budget and milestones | The charter's majority for money | Feasibility, budget, alignment |
| `allocation` | Move treasury funds to a coalition (was: stimulus) | The charter's majority for money | Quorum and caps |

Tranche releases are not public votes. They're steward decisions against evidence, with a public notice period for large releases.

This adds one setting to every community's governance: `majorities.money`, the majority needed for projects and allocations. Recommended default: a simple majority, with steward review.

## Money

```
 member commons share ─┐
 agent levy ───────────┼──▶ community treasury ──allocation policy──▶ coalitions (tranches)
 direct gifts ─────────┤        (escrowed, steward quorum)        ├──▶ reserve (capped)
 virtual land or ocean ┘                                           └──▶ parent commons share
```

- **Inflows are kept separate**, so paying never buys standing.
- **A parent share.** A share of each sub-community's inflow can flow up to its parent. For example, a commons inside the Global Commons can send a set share to the Global Commons treasury. Set by the sub-community's charter.
- **Perpetual trusts.** A coalition can end in a permanent holding, such as critical ecosystem land bought and placed in a perpetual trust. Its final milestone is the transfer into trust, with the trust deed as evidence.

## On the map

Every community has a boundary on Gaia, and every coalition has a place: a point, a parcel or a polygon. So the map shows where money is going and what it protects, and Gaia's calculator view can rank which coalitions matter most for a commons.

## What changes in Coalitions

1. **Link systems to communities.** Every system gets a Cloud Mirror community. New systems create one; existing systems are offered the switch.
2. **Stop direct-to-creator donations.** Route all Ven to the community treasury, earmarked by coalition. This is the most important change.
3. **Add milestones, budgets and a place on Gaia** to every coalition.
4. **Replace single-person approval** with the community's Propel vote and steward review.
5. **Turn stimulus into allocation proposals.**
6. **Move the commissions into the charter** as the community's commons share.
7. **Keep thecoalition.world as the public face** for coalitions across every community, including the Global Commons, reading from Cloud Mirror's API. Existing coalitions and donation history are imported read-only.

## Build order

This slots into the charter build already under way:

1. ~~Per-community charters~~ (done).
2. **Proposals**, not just amendments: one engine with the three kinds above, validated before any vote.
3. Propel voting through the mock, then the live API.
4. **Treasuries and coalitions:** escrow, allocation policy, milestones, tranche releases, the steward quorum.
5. **Coalition front end** on Cloud Mirror's API; switch off the old donation path; import history.
6. **Gaia layers** for community boundaries and coalition places.
7. **The Global Commons community** and its first sub-community, with a first coalition.
