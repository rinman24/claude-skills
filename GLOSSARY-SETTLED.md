# Settled terms

Rulings domain-modeling must not reopen on its own initiative. Match Term or Rejected within the same Context, case-insensitive. Reopen only on explicit user instruction; a reopened row is superseded when the term is settled again. Never delete.

| Term | Rejected | Context | Ruling | Status | Settled | Ref |
|---|---|---|---|---|---|---|
| Subsystem | Slice, Vertical slice | Wayfinder | Use Subsystem for Löwy's architectural unit; the unit of delivery is Increment | settled | 2026-10-07 | session:2026-10-06-eric-squadra-unit-name |
| Map | Local board | Wayfinder | Use Map for wayfinder's charted record; wayfinder has no board | settled | 2026-10-07 | session:2026-10-06-eric-term-board |
| Errand | Task, Chore | Wayfinder | Use Errand for wayfinder's manual-step ticket kind | settled | 2026-10-07 | session:2026-10-06-eric-design-document-contract |
| Increment | Infrastructure increment | Wayfinder | Use Increment, conforming to squadra's definition | settled | 2026-10-07 | session:2026-10-06-eric-design-document-contract |
| Ticket | Issue, Story, Card | Wayfinder | Use Ticket for any entry on a map; decision ticket and errand are its two sorts | settled | 2026-10-07 | session:2026-10-07 |
| Decision ticket | Work item | Wayfinder | Use Decision ticket for every ticket except an errand, research included | settled | 2026-10-07 | session:2026-10-07 |
| Design document | Spec, Plan, Deliverable | Wayfinder | Use Design document for what publish writes; it is never a copy of the map | settled | 2026-10-07 | session:2026-10-07 |
| Cleared | Done, Ready, Final, Approved | Wayfinder | Use Cleared only for the design document's readable state, never for the map or a ticket | settled | 2026-10-07 | session:2026-10-07 |
| Transcribe | Publish, Sync | design-to-board | Use Transcribe for design-to-board's whole act, cleared design document to squadra's board; it never designs. Its comparison step is the reconcile | settled | 2026-10-09 | session:2026-10-09-eric-transcribe-vs-reconcile |
| Reconcile | Diff | design-to-board | Use Reconcile only for the step that compares a design document with `increments_by_origin()` through the translation table and yields the Plan; never for the whole act | settled | 2026-10-09 | session:2026-10-09-eric-transcribe-vs-reconcile |
| Calls | Uses, Depends on | Service decomposition | Use Calls for a declaring row's complete set of direct callees; `Depends on` stays increment order | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Declaration | Listing | Service decomposition | Use Declaration for a declaring row's `Calls` cell; a referenced row declares nothing | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Referenced service | External, Legacy | Service decomposition | Use Referenced service for a Services row present only because a declaring row calls it | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Call edge | Dependency | Service decomposition | Use Call edge for a declared A→B; never bare "dependency" | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Queued call | Async call, Event | Service decomposition | Use Queued call for a call delivered through a queue | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Contract | Interface, API | Service decomposition | Use Contract for a named set of a service's public operations; one import-linter entry is an Import rule | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Operation | Method, Endpoint | Service decomposition | Use Operation for one entry on a contract | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Type pair | Signature | Service decomposition | Use Type pair for the input→output kinds an operation's layer requires | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Service layout | Layer map | Service decomposition | Use Service layout for the target-owned file placing each service at its repo path; Map stays Wayfinder's | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Exemption | Baseline, Ignore | Service decomposition | Use Exemption for an import allowed against the rules, recorded with its reason | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Import rule | import-linter contract | Service decomposition | Use Import rule for one entry in the generated config; Contract stays a service's public operations | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Import-direction check | Architecture test | Service decomposition | Use Import-direction check for the every-PR check that reports forbidden imports | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Config check | Drift check, Sync | Service decomposition | Use Config check for the every-PR check that reports a stale config | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Conformance check | Reconciliation, Reconciliation diff, Reconcile, As-built check | Service decomposition | Use Conformance check for the once-per-delivered-map comparison of the repo with its design document; Reconcile stays design-to-board's | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Match | Convergence, Conforms | Service decomposition | Use Match for a conformance check finding that is declared and built | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Surplus | Divergence | Service decomposition | Use Surplus for a conformance check finding that is built, not declared | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Shortfall | Absence | Service decomposition | Use Shortfall for a conformance check finding that is declared, not built | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| plumb | Reconciler | Service decomposition | Use plumb for the tool that generates the config and runs the config and conformance checks | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Proving path | Spike, Pilot | Wayfinder | Use Proving path for the increments that prove a subsystem's decomposition ahead of the pulses; Vertical slice stays rejected under Subsystem | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Pulse | Phase, Wave, Sprint | Wayfinder | Use Pulse for one step of the build order, closed by a pulse milestone; a Layer is a service's kind, not a pulse | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
| Pulse milestone | Gate, Checkpoint, Milestone | Wayfinder | Use Pulse milestone for the increment that closes a pulse; never bare Milestone | settled | 2026-10-29 | session:2026-10-28-eric-decomposition-vocabulary-followup |
