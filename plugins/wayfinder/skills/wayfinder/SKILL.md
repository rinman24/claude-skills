---
name: wayfinder
description: Chart the way to one destination that is too big for a single session and whose route is still foggy. Keeps a committed map of tickets under .scratch/wayfinder/, resolves one decision ticket per session with grilling and domain-modeling, and publishes a design document of increments for design-to-board. Writes only the map and the design document; never builds.
disable-model-invocation: true
---

A loose idea has arrived, too big for one session, and the way from here to the **destination** is still in fog. Wayfinder charts that way as a **map** of **tickets**, resolves the **decision tickets** one session at a time, and publishes a **design document** that lists the **increments** squadra will build. Its vocabulary is in the plugin's [GLOSSARY.md](../../GLOSSARY.md); use those terms.

## What wayfinder writes

Wayfinder writes exactly two things: the map, under `.scratch/wayfinder/<map>/` ([MAP-FORMAT.md](./MAP-FORMAT.md)), and the design document, at `docs/design/<map>.md` ([DESIGN-FORMAT.md](./DESIGN-FORMAT.md)). Both are committed. Glossary files are written by domain-modeling when it is called, under its own rules.

Wayfinder never builds. No product code, scaffolds or migrations, at any point, whatever a map, a ticket or a resolution says; no map can grant itself an exception. It never touches squadra's board or any issue tracker either: `design-to-board` transcribes a cleared design document onto the board, and squadra builds from there. When the pull to just build something appears, that is the edge of the map: finish the ticket and stop.

## Refer by name

In everything the user reads, refer to a map or ticket by its name (its title), with the file as the link. Never a bare number like `03`.

## Ticket kinds

Every ticket's `Kind` line says how it is resolved. Read it; never infer the kind from the body. Grilling, research and prototype tickets are decision tickets. An errand is not.

- **grilling** (with the user, the default): call the Skill tool twice, for `grilling` and for `domain-modeling`, and check both loaded before the first question. The user answers for themselves; never answer a grilling question on the user's behalf, even when another skill or the ticket seems to invite it. Pass domain-modeling the ticket's ref (`scratch:wayfinder/<map>/<file>`) as the `ref` for any `Settle`.
- **research** (agent alone): dispatch one read-only subagent with the question. Tell it to use primary sources (official docs, the code, the spec) and cite a source for every finding. Its findings, with citations, become the Resolution.
- **prototype** (with the user): make cheap, rough variants to react to, shown in the conversation (outlines, mock-ups, sketched behaviour), not as files. The user picks the variant; never pick it yourself, and never close the ticket until the user has picked.
- **errand** (with the user): a manual step that unblocks a decision. Give the user a precise checklist; you may run read-only commands to help. The Resolution records what was done and any facts later tickets need. An errand that reads like a piece of the build is mis-kinded: say so, and don't do it.

## Keep the map small

Over-charting is the main failure: a map so detailed that later tickets stop making sense once early ones are resolved. Lead toward vertical increments:

- Every decision ticket carries `Unblocks: <increment>`. A ticket that unblocks no increment doesn't belong on the map yet.
- An increment that can't be named in settled terms is fog, not a row.
- More than about 6 increments: propose splitting the map per subsystem, one map each.
- An increment that changes more than 2 services (new or modified, counted from `Touches`): split it into predecessor increments.
- List increments in critical-path order.
- On that split, or when an increment introduces a new component, you may consult Juval Löwy: the Agent tool with `subagent_type: board-juval`. It is optional; if the agent isn't available, carry on without it. Juval advises; the user decides.

## Chart

One mode, four operations. Pick the operation from what the user asked:

- `/wayfinder <loose idea>`: **Begin**.
- `/wayfinder <map> [ticket]`: **Resolve**.
- "revise …" naming a closed ticket: **Revise**.
- "publish <map>": **Publish**.

One ticket in progress per map at a time, no exceptions. Separate maps may run in parallel.

### Begin

0. **Check the size first.** Before loading any skill or asking anything, judge the idea as stated. If it plainly fits in one session (one change you could make now, or a question you could answer now, with no decision that needs another session), stop: say a map isn't needed, in a line or two, and ask the user how to proceed. Don't grill, don't write anything, and don't start doing the work. When in doubt, go on to step 1; step 2 catches the rest.
1. **Name the destination.** Call the Skill tool for `grilling` and `domain-modeling` and settle what this map is finding its way to, including the behaviours `B1`, `B2`… observable once it is reached. The destination fixes the scope, so it comes first.
2. **Survey the frontier.** Grill again, breadth-first: across the whole space rather than deep on one thread, to surface the open decisions and the increments you can already name. If this turns up no fog (the whole route fits in one session), stop: say a map isn't needed and ask the user how to proceed.
3. **Write the map**: `map.md` with Destination, the increments you can name, an empty Decisions so far, and the rest sketched as Fog.
4. **Write the tickets you can state precisely now**, each with `Kind`, `Status: open` and `Unblocks:`. Then add `Blocked by` lines in a second pass, once every ticket has its number.
5. **Stop.** Begin resolves nothing, research included.

### Resolve

1. **Load the map**: `map.md` only, not every ticket body.
2. **Choose the ticket.** If the user named one, use it. Otherwise take the first ticket on the frontier ([MAP-FORMAT.md](./MAP-FORMAT.md)). If another ticket on this map is already `in progress`, stop and ask the user whether that session is still going.
3. **Mark it** `Status: in progress` before anything else.
4. **Resolve it** as its kind says. Open other tickets' bodies only when you need their detail.
5. **Record it**: write the Resolution, set `Status: closed`, and add its line to Decisions so far.
6. **Update the map**: write tickets for any fog the answer has made precise and delete those patches from Fog; add or edit unpublished increment rows. If a ticket turns out to sit beyond the destination, set it `closed` with a one-line Resolution saying so and add an out-of-scope line under Destination; it gets no Decisions line.
7. **Stop.** One ticket per session. If every decision ticket is closed and Fog is empty, say the map is ready to publish.

### Revise

Only when the user explicitly says a closed decision changed. Never revise on your own initiative, and don't design around a decision you think is wrong: put it to the user.

1. On the closed ticket: set `Status: revised` and add a `## Revised <date>` section saying what changed, linking the replacement.
2. Open the replacement ticket with `Replaces:` pointing back and the same `Unblocks:`; it is resolved in its own session.
3. Rewrite the old ticket's line in Decisions so far to point at the replacement, and repoint every `Blocked by` that named the old ticket.
4. Flag dependents: list every ticket whose Resolution relied on the old decision and every increment it decided, in the map and in your reply.
5. Settled terms: scan `GLOSSARY-SETTLED.md` for rows whose `Ref` is the revised ticket's ref (a text search, not a Lookup), and have domain-modeling `Reopen` each one, with the user's revision as the reason.
6. If the design document is published, set its `status: revising` and change nothing else. Publish rewrites it.

### Publish

1. Run every check in [DESIGN-FORMAT.md](./DESIGN-FORMAT.md). If any fails, name each failure and write nothing.
2. Write `docs/design/<map>.md`: the record and the contract built from the map, never a copy of `map.md`. Published rows already in the document keep their IDs; a changed row is withdrawn (`r1, withdrawn r2`) and replaced by a new ID.
3. Fill `Published` for every row new in this revision (`r<N>`), in the document and in the map.
4. Set `status: cleared`, set `revision` (1, or one more than before) and `changed` (the sections that changed; empty on revision 1).
5. Tell the user the document is cleared for `design-to-board`. Don't run it: it is a separate step the user starts.
