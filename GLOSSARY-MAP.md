# Glossary Map

## Contexts

- [Wayfinder](./plugins/wayfinder/GLOSSARY.md): charts the way to one destination and publishes a design document
- design-to-board (`./plugins/design-to-board/`, no glossary yet): transcribes a cleared design document into increments on squadra's board and never designs; its language is the reconcile's translation table (row state × item Lifecycle → action) and the Origin format `<map>:<ID>`

## Relationships

- **Wayfinder → squadra fleet**: Conformist on Increment (Vertical / Foundation); the design document is the Published Language that `design-to-board` (not yet built) will read ([squadra's glossary](https://github.com/rinman24/squadra/blob/main/GLOSSARY.md))
- **Wayfinder → design-to-board**: Published Language; the design document ([DESIGN-FORMAT.md](./plugins/wayfinder/skills/wayfinder/DESIGN-FORMAT.md)) is the only thing design-to-board reads from wayfinder, and the contract is its translator checks 6–15
- **design-to-board → squadra fleet**: Conformist downstream of squadra's board verbs (`queue_increment`, `withdraw_increment`, `increments_by_origin`) and Lifecycle. Translations: `Depends on` → predecessors; row ID → Origin (`<map>:<ID>`); withdrawn row → `withdraw_increment` (QUEUED only; refused at ACTIVE and DONE); live row without its Origin on the board → `queue_increment`; `Published: rN` → nothing
- One person (Rich) spans Wayfinder, design-to-board and squadra fleet; the boundaries are in the artifacts, not the team.
