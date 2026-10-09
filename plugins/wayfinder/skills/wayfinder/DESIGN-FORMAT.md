# Design document format

The design document is what Publish writes: one per map, at `docs/design/<map>.md`, outside `.scratch/`. It is the Published Language that `design-to-board` reads to put increments on squadra's board. It is never a copy of `map.md`: fog, ticket bodies and errands stay in the map.

It has two parts. The **contract** (front matter, Services, Increments, Rules and planning assumptions) is what `design-to-board` reads. The **record** (Destination, Decisions) is for people; the translator never reads it.

```markdown
---
format: wayfinder-design/1
map: <map>
status: cleared
revision: 1
changed: []
---

# <Map title>

## Destination

<One or two lines.>

- B1: <behaviour observable end to end>
- B2: <…>

## Decisions

- <one line per current decision> (scratch:wayfinder/<map>/03-<slug>.md)

## Services

| Service | Layer | Encapsulates | Introduced in |
|---------|-------|--------------|---------------|
| <name> | Manager / Engine / ResourceAccess / Client / Utility | <the volatility it hides; required for a new service> | I2 |
| <name> | ResourceAccess | | |

## Increments

| ID | Increment | Kind | Touches | Depends on | Order | Decided by | Published |
|----|-----------|------|---------|------------|-------|------------|-----------|
| I1 | <name>: <one-line intent> | vertical (B1) | <service>, <service> | | 1 | scratch:wayfinder/<map>/03-<slug>.md | r1 |
| I2 | <name>: <one-line intent> | foundation → I3 | <service> | I1 | 2 | scratch:wayfinder/<map>/04-<slug>.md | r1, withdrawn r2 |

## Rules and planning assumptions

- Rule: at most 2 changed services (new or modified) per increment.
- Assumption: at most 2 concurrent runners, one reviewer.
```

## Front matter

- `format`: always `wayfinder-design/1`.
- `map`: the map's directory name.
- `status`: `cleared` (the translator may read it) or `revising` (it may not).
- `revision`: starts at 1; each Publish after the first adds 1.
- `changed`: the sections whose content changed in this revision (`[Decisions, Increments]`); empty on revision 1.

## Sections

- **Destination**: copied from the map's Destination, without the out-of-scope lines. Behaviours `B1`, `B2`… keep their map numbers.
- **Decisions**: one line per current decision, each with its ticket's `scratch:` ref. A revised ticket appears only through its replacement. Errands never appear.
- **Services**: only the services this map creates or changes. `Introduced in` names the one increment that creates a new service and is blank for an existing one; it is the only place a service is called new. `Encapsulates` is required for a new service.
- **Increments**: the map's Increments table, with `Decided by` as `scratch:` refs. Kind is `vertical (B<n>)`, `foundation → I<n>, …`, or blank (an increment with neither attribute), as squadra's glossary defines them. A foundation names rows in this table only; a map enables another map's increment through that increment's `Depends on: <map>:<ID>`. `Touches` holds service names only, each declared in Services. `Depends on` holds increment IDs, or `<map>:<ID>` for an increment in another map. `Order` puts the critical path first.
- **Rules and planning assumptions**: rule lines (the integration rule above) apart from resource lines. A line belongs here only if changing it would make Rich revise the map.

## Increment identity

IDs `I1`, `I2`… are never renumbered or reused. A published row changes only its `Published` cell (`r1`, then `r1, withdrawn r2`); any other change to it is a withdrawal plus a new row with a new ID. Withdrawn rows stay in the table. The translator only ever creates and withdraws.

A live row never depends on a withdrawn row. When Publish withdraws a row, it also withdraws every live row that depends on it, directly or through other rows (the withdrawal cascade).

A published foundation's `Kind` cell is frozen: withdrawing an increment it names doesn't change it.

## Checks before `cleared`

Publish runs every check and sets `status: cleared` only when all pass. A failure is reported by name and the document is left as it was.

From the map:

1. No ticket on the map is `open` or `in progress`, and Fog is empty.
2. Every behaviour has a vertical increment, and every vertical increment names a behaviour.
3. Every `Decided by` ref appears in Decisions.
4. Every increment is named in settled terms: run domain-modeling's `Lookup` on the terms in each increment name and behaviour, in the context the destination belongs to (the `GLOSSARY-MAP.md` context whose description covers it). A `rejected-form` hit fails. A term with no row is a plain word and passes; only a `GLOSSARY-SETTLED.md` row can fail this check. If no listed context covers the destination, no row applies: say so and pass.
5. No more than about 6 live increments; past that, the map is split per subsystem instead of published.

The translator's validation list (it fails loudly back to wayfinder if any of these fails, so wayfinder checks them first):

6. `format` is known and `status` is `cleared`.
7. IDs are unique, and withdrawn rows are still present.
8. Every `Touches` entry is declared in Services.
9. A service with an `Introduced in` is introduced by exactly one increment, and every other increment touching it depends on that one.
10. Any two increments touching the same service have a path of `Depends on` edges between them.
11. Each increment's `Touches` count is within the rule (at most 2 changed services).
12. Each foundation increment's named increments depend on it.
13. Order is consistent with the edges.
14. A live row never depends on a withdrawn row.
15. Each Kind is blank, `vertical (B<n>)` naming a behaviour in Destination, or `foundation → I<n>, …` naming rows in the table, live or withdrawn. A failure is reported as malformed Kind, quoting the cell and naming the failed part (form, unknown behaviour or unknown row).
