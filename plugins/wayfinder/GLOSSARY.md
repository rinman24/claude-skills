# Wayfinder

Wayfinder charts the way to one destination: it clears the fog on a map and publishes a design document. It never builds.

## Language

**Map**:
Wayfinder's record of the way to one destination: `map.md` and the ticket files inside its boundary.
_Avoid_: local board

**Errand**:
A ticket for a manual step that unblocks a decision; it decides nothing itself.
_Avoid_: task, chore

**Subsystem**:
Löwy's architectural unit: up to three Managers with the Engines and ResourceAccess components behind them.
_Avoid_: slice, vertical slice

**Increment**:
squadra's unit of delivery, as wayfinder charts it in a map and lists it in the design document. Attributes as squadra defines them: _Vertical_, _Foundation_.
_Avoid_: infrastructure increment
