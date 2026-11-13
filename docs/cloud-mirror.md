# How the Global Commons links to Cloud Mirror

Draft v0.1, November 2026.

## In one line

**Cloud Mirror** is a jurisdictional cloud layer, in development, where a community writes its precepts and rules, and members (people, organisations and AI agents) choose to live under them. **The Global Commons becomes one spoke of Cloud Mirror**: its rules are written in Propel, its places are mapped in Gaia, its members carry Mandala and HubID identities, and its value flows in Ven.

```
                   ┌───────────────────────────────┐
                   │          CLOUD MIRROR         │
                   │  charter · tiers · ledger ·   │
                   │  stewardship · treasury       │
                   └──┬─────────────┬───────────┬──┘
                      │             │           │
             ┌────────▼───┐  ┌──────▼──────┐  ┌─▼─────────────┐
             │  GLOBAL    │  │ other cloud │  │ Hub Culture,  │
             │  COMMONS   │  │ jurisdictions│ │ Bermuda       │
             │  (spoke)   │  │ (spokes)    │  │ Standard ...  │
             └──┬───┬──┬──┘  └─────────────┘  └───────────────┘
                │   │  │
       Propel ◄─┘   │  └─► Ven (remuneration, anchoring)
     (rules, votes) │
                    ▼
        Gaia (place)  +  Mandala / HubID (identity)
```

Best practices migrate between spokes in both directions. A rule that works in one jurisdiction can be adopted by another.

## Cloud Mirror already implements Ostrom's design principles

The Cloud Mirror design maps almost one to one onto Ostrom's eight principles. That is why it is a natural base for the Global Commons.

| Ostrom principle | Cloud Mirror mechanism | In the Global Commons spoke |
| --- | --- | --- |
| 1. Clear boundaries | A public registry. Joining needs two signatures: the member accepts the charter, and an accountable human operator confirms. | Each commons is a Gaia polygon or network, and its members are registered identities. |
| 2. Rules fit local conditions | Each spoke has its own versioned charter and precepts, with a signable digest. | Each commons writes its own charter. The framework supplies a checklist, not a template. |
| 3. Collective choice | Rules and decisions go through Propel, with liquid (delegated) voting. | Users of a commons vote on its rules, delegating by topic to people they trust. |
| 4. Monitoring | An append-only, hash-chained ledger of every standing event, anchored on Ven. | Use, payouts and rule changes are on the ledger and visible on the map. |
| 5. Graduated sanctions | Standing tiers granted and revoked by a council, with written reasons. Treasury freezes. | Rights scale with responsibilities met. Breaches cost standing before they cost access. |
| 6. Conflict resolution | Incident disclosure and council review, recorded publicly. | Disputes are disclosed, reviewed and repaired in the open. |
| 7. Right to organise | A recognised cloud jurisdiction. | Communities organise their commons without waiting for a treaty. |
| 8. Nested enterprises | Hub-and-spoke: spokes under one Cloud Mirror layer. | Local commons nest inside regional and global ones. |

## The commons treasury

Cloud Mirror's treasury design carries over directly. It answers the "bankability" test and the main corruption risk in community funding.

- **Inflows are kept separate:** contributions, access fees and donations are recorded as different kinds. Paying fees never buys standing.
- **An allocation policy** splits each period's inflow among purposes. It is versioned and set by the stewards.
- **Escrow and tranches.** Money goes to an escrowed treasury and is released against milestones, with evidence. It never goes to a person's own account.
- **Steward quorum.** Releases need several stewards from different groups. Large releases get a public notice period. Any two stewards can freeze.
- **Everything on the ledger**, anchored and published, without exposing individuals.

For the Global Commons, the treasury is where remuneration lives: a codified share of revenue from commons-based assets (renewables, the Ocean Climate Fund's virtual ocean layer, benefit-sharing on genetic data) paid to the keepers of each commons, converted into what they value.

## Hub Culture Coalitions

Coalitions become the local project layer of the Global Commons: geo-linked on Gaia, funded from the commons treasury in milestone tranches, and governed by steward quorum. See [coalitions.md](coalitions.md) for the full mapping.

## AI agents: the most urgent spoke

Cloud Mirror was designed for AI agents as well as people. An agent joins by accepting a charter of precepts, such as peaceful nonviolence, and rises through tiers by demonstrated behaviour. With a billion or more agents expected within a year, a Global Commons spoke for agents may be the most urgent use of this framework:

- **Identity:** every agent is a Mandala identity with an accountable human operator.
- **Rules:** agents can propose rules in Propel, always labelled as agents, never mistaken for humans.
- **Monitoring:** agent incidents are disclosed and reviewed like anyone's.
- **Governing the shepherd:** where AI helps steward a commons, its own conduct sits under the same charter, ledger and override.

## What to build

1. **Registry API:** serve `data/registry/` entries as a Gaia layer, each linked to its Cloud Mirror charter.
2. **Charter template** for a commons spoke, with the six parts (boundaries, terms, rules, rights, responsibilities, remuneration).
3. **Propel binding:** rule proposals and delegated votes per commons.
4. **Treasury spoke:** allocation policy and tranche releases for one pilot commons.
5. **Agent-governance charter:** a first draft for agents, for public comment.
