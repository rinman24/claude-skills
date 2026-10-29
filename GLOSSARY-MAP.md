# Glossary Map

## Contexts

- [Wayfinder](./plugins/wayfinder/GLOSSARY.md): charts the way to one destination and publishes a design document
- design-to-board (`./plugins/design-to-board/`, no glossary yet): transcribes a cleared design document into increments on squadra's board and never designs; its language is the reconcile's translation table (row state × item Lifecycle → action) and the Origin format `<map>:<ID>`
- [Service decomposition](./docs/service-decomposition/GLOSSARY.md): Löwy's Method as target repos apply it: layers, contracts, type pairs and call edges, and the checks that hold a build to its design document
- plumb (`rinman24/plumb`, no glossary: it coins no terms): generates the import-linter config from cleared design documents and the service layout, and runs the config check and the conformance check

## Relationships

- **Wayfinder → squadra fleet**: Conformist on Increment (Vertical / Foundation); the design document is the Published Language that `design-to-board` reads ([squadra's glossary](https://github.com/rinman24/squadra/blob/main/GLOSSARY.md))
- **Wayfinder → design-to-board**: Published Language; the design document ([DESIGN-FORMAT.md](./plugins/wayfinder/skills/wayfinder/DESIGN-FORMAT.md)) is the only thing design-to-board reads from wayfinder, and the contract is its translator checks 6–15
- **design-to-board → squadra fleet**: Conformist downstream of squadra's board verbs (`queue_increment`, `withdraw_increment`, `increments_by_origin`) and Lifecycle. Translations: `Depends on` → predecessors; row ID → Origin (`<map>:<ID>`); withdrawn row → `withdraw_increment` at QUEUED, refused at ACTIVE, nothing at DONE (withdrawing a row never undoes delivered work, so a delivered increment never becomes Withdrawn; the withdrawing revision's run notes it); live row without its Origin on the board → `queue_increment`; `Published: rN` → nothing
- **Wayfinder → Service decomposition**: Conformist; the design document quotes its terms verbatim (`Layer`, `Calls`, contract operations and type pairs)
- **design-to-board → Service decomposition**: Conformist; it checks the design document against these rules and never extends them
- **plumb → Service decomposition**: Conformist; plumb coins no terms
- **Wayfinder → plumb**: Published Language; plumb reads cleared design documents' Services rows, as design-to-board does
- **plumb → import-linter**: Anticorruption Layer; plumb's config generator is the only place the translation lives, so import-linter's words ("contract", "layers", "forbidden", "protected") stay inside the generated config, and our Layer and Forbidden import never mean import-linter's
- One person (Rich) spans Wayfinder, design-to-board, Service decomposition, plumb and squadra fleet; the boundaries are in the artifacts, not the team.
