# Map format

A map is committed markdown under `.scratch/wayfinder/<map>/`, where `<map>` is a short kebab-case name for the destination:

```
.scratch/wayfinder/<map>/
├── map.md                 # the aggregate root: the low-resolution view
├── 01-<ticket-slug>.md    # one file per ticket, inside the map's boundary
└── 02-<ticket-slug>.md
```

Ticket numbers are assigned in creation order and never reused. A ticket's ref, used everywhere outside the map (the design document's Decisions, `Ref` in `GLOSSARY-SETTLED.md`), is `scratch:wayfinder/<map>/<file>`, the path under `.scratch/`.

## map.md

`map.md` is an index, not a store. A decision lives in exactly one place, its ticket; the map gives the gist and the link. Open tickets are not listed here: they are found from the ticket files (see [The frontier](#the-frontier)).

```markdown
# <Map title>

## Destination

<One or two lines: what reaching the end of this map looks like.>

- B1: <a behaviour observable end to end once the destination is reached>
- B2: <…>

Out of scope:
- <gist>: <why it is beyond the destination> ([<ticket name>](<file>) if a ticket was closed for it)

## Increments

| ID | Increment | Kind | Touches | Depends on | Order | Decided by | Published |
|----|-----------|------|---------|------------|-------|------------|-----------|
| I1 | <name>: <one-line intent> | vertical (B1) | <service>, <service> | | 1 | 03 | |
| I2 | <name>: <one-line intent> | foundation → I3 | <service> | I1 | 2 | 04, 06 | |

## Decisions so far

- [<ticket name>](<file>): <one-line gist of the resolution>
- [<errand name>](<file>) (errand): <what was done, and any fact later tickets need>

## Fog

- <a question you can tell is coming but can't yet state precisely>
```

- **Destination** fixes the scope. Behaviours are numbered `B1`, `B2`… (usually two or three) and never renumbered. Out-of-scope lines live here because scope is the destination's business: anything ruled beyond it never graduates from Fog and never appears in Decisions so far.
- **Increments** uses the design document's columns ([DESIGN-FORMAT.md](./DESIGN-FORMAT.md)). Kind is `vertical (B<n>)`, `foundation → I<n>, …` or blank, as squadra defines them. `Decided by` lists ticket numbers here; Publish turns them into refs. `Published` stays blank until Publish fills it. IDs `I1`, `I2`… are never renumbered or reused. Before its first Publish a row may be edited freely; after it, a row changes only its `Published` status, and any other change means withdrawing it and adding a new ID. Withdrawn rows stay.
- **Decisions so far** has one line per closed ticket, in the order closed, errands marked `(errand)`. A revised ticket's line is rewritten to point at its replacement.
- **Fog** is in-scope and not yet sharp enough to ticket. The test is whether the question can be stated precisely now, not whether it can be answered. An increment that can't yet be named in settled terms is fog, not a row. When a patch graduates into tickets or rows, delete it here: nothing lives in two places.

## Ticket file

```markdown
# <Ticket name, phrased as the question or the step>

Kind: grilling | research | prototype | errand
Status: open | in progress | closed | revised
Unblocks: I3
Blocked by: 02, 05
Replaces: 04

## Question

<The decision this ticket resolves, sized to one session. For an errand: the manual step and the decision it unblocks.>

## Resolution

<Written when the ticket closes. The decision and why; for research, the findings with a source cited for each; for a prototype, the user's verdict in their own words and a link to the prototype (its `prototype/<name>` branch and path, or "not kept"); for an errand, what was done and the resulting facts.>
```

- **Kind** says how the ticket is resolved; read it, never infer the kind from the body. Grilling, research and prototype tickets are decision tickets; an errand decides nothing.
- **Status**: `open` until a session starts it; `in progress` while one session holds it (at most one ticket per map); `closed` with a Resolution; `revised` when a later decision replaced it.
- **Unblocks** names the increment(s) a decision ticket unblocks. An errand names the ticket it unblocks instead (`Unblocks: 07`).
- **Blocked by** lists ticket numbers; omit the line when nothing blocks it. **Replaces** appears only on a replacement opened by Revise.
- Assets made while resolving (a prototype, a research note too long for the Resolution) are linked from the Resolution, never pasted in.

A revised ticket keeps its Resolution and gains a section below it:

```markdown
## Revised <YYYY-MM-DD>

<What changed and why, in one or two lines.> Replaced by [<replacement name>](<file>).
```

## The frontier

A ticket is unblocked when every ticket in its `Blocked by` is `closed`. The frontier is the open, unblocked tickets, in number order. Find it from the files, not from memory:

```bash
grep -l '^Status: open' .scratch/wayfinder/<map>/[0-9]*.md
```

then drop any whose `Blocked by` names a ticket that isn't closed. A ticket whose blocker was revised is blocked by the replacement instead; Revise rewrites the line.
