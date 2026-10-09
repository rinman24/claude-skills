# Wayfinder

Wayfinder charts the way to one destination and publishes a design document. It never builds.

## Language

**Map**:
Wayfinder's record of the way to one destination: `map.md` and the ticket files inside its boundary.
_Avoid_: local board

**Ticket**:
One question or manual step on a map; its Kind is grilling, research, prototype or errand.
_Avoid_: issue, story, card

**Decision ticket**:
A ticket whose resolution is recorded as a decision on the map; any Kind except errand.
_Avoid_: work item, task

**Errand**:
A ticket for a manual step that unblocks a decision; it decides nothing itself.
_Avoid_: task, chore

**Design document**:
Wayfinder's published output for one map: the destination's behaviours, the decisions, and the increments that reach them; the Published Language `design-to-board` reads.
_Avoid_: spec, plan, deliverable

**Cleared**:
The design document's state in which `design-to-board` may read it; its opposite is revising.
_Avoid_: done, ready, final, approved

**Subsystem**:
Löwy's architectural unit: up to three Managers with the Engines and ResourceAccess components behind them.
_Avoid_: slice, vertical slice

**Increment**:
squadra's unit of delivery, as wayfinder charts it in a map and lists it in the design document. Attributes as squadra defines them: _Vertical_, _Foundation_.
_Avoid_: infrastructure increment
