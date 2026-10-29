# Service decomposition

Löwy's Method as target repos apply it: layers, contracts, type pairs and call edges, and the checks that hold a build to its design document.

## Language

### Services and calls

**Layer**:
A service's kind in Löwy's Method, as the design document's `Layer` column writes it: Manager, Engine, ResourceAccess, Client or Utility.

**Composition rule**:
A rule on which layer may call which; every service gets the composition rules, declared or not.

**Calls**:
The column on Services that holds a declaring row's complete set of direct callees after the map is delivered, or `none`; it is blank on a referenced service's row.
_Avoid_: uses, depends on

**Declaring row**:
A Services row for a service the map creates (`Introduced in`) or changes (named in an increment's `Touches`).

**Declaration**:
A declaring row's `Calls` cell in a cleared design document; for each service, the latest one holds.
_Avoid_: listing

**Referenced service**:
A service in Services only because a declaring row calls it; it has a Layer and no declaration.
_Avoid_: external, legacy

**Call edge**:
A→B, where B is in A's declaration: A's code may import B's contract module and nothing else of B's.
_Avoid_: dependency (unqualified)

**Queued call**:
A call delivered through a queue, written `<name> (queued)` in `Calls`; legal only Manager→Manager.
_Avoid_: async call, event

**Composition root**:
The one package that constructs and wires services, and so may import their implementation modules.

**Use case**:
Löwy's name for a behaviour B<n> in a design document; the two are one concept.

### Contracts

**Contract**:
A named set of a service's public operations; a service has one or two.
_Avoid_: interface, API

**Operation**:
One entry on a contract: a domain verb, an input type and an output type.
_Avoid_: method, endpoint

**Type pair**:
The input→output kinds an operation's layer requires: Manager Command→Result or Query→Result, Engine Facts→Plan, ResourceAccess Spec→Rows, or Spec alone for a write that returns nothing. Utilities and Clients have none.
_Avoid_: signature

**Contract change**:
Adding, removing or renaming an operation on an existing service, or changing one of its types.

**Operation count**:
The number of operations on one contract, not on one service.

### Enforcement on every PR

**Service layout**:
The target-owned file that places each service at its repo path, names the composition root, records exemptions, and gives the layer of each rules-only service.
_Avoid_: layer map

**Exemption**:
An import allowed against the rules, recorded in the service layout with its reason.
_Avoid_: baseline, ignore

**Generated config**:
The committed import-linter config that plumb generates from the declarations and the service layout.

**Import rule**:
One entry in the generated config, enforcing either a composition rule or one service's call edges.
_Avoid_: import-linter contract

**Rules-only / edge-enforced**:
A service in the service layout with no declaration is rules-only: it gets the composition rules only. From its first declaration it is edge-enforced.

**Import-direction check**:
The check that runs on every PR and fails on any import the generated config forbids.
_Avoid_: architecture test (unqualified)

**Forbidden import**:
An import that breaks a composition rule, a declared call edge, or the composition root's sole access to implementation modules.

**Config check**:
The check that runs on every PR and fails when the committed generated config differs from what plumb generates now.
_Avoid_: drift check, sync

**Stale config**:
The config check's finding: the committed generated config no longer matches the declarations and the service layout.

### Conformance once per delivered map

**Conformance check**:
The check that runs once per delivered map and compares the repo with the design document on three surfaces: modules against Services, import edges against declarations, public operations against declared operations.
_Avoid_: reconciliation, reconciliation diff, reconcile, as-built check

**Match**:
A conformance check finding: declared and built.
_Avoid_: convergence, conforms

**Surplus**:
A conformance check finding: built, not declared.
_Avoid_: divergence

**Shortfall**:
A conformance check finding: declared, not built.
_Avoid_: absence

### Tool

**plumb**:
The tool that generates the config and runs the config check and the conformance check; target repos pin one of its tags.
_Avoid_: reconciler

## Translation notes

- Command here is an operation's state-changing input; it is not Evans's Command, which returns no domain information.
- Spec matches Evans's Specification: a selection predicate, or a description of something to build to order.
- Facts→Plan and Spec→Rows are this context's words. design-to-board's Reconcile already yields a Plan, so design-to-board code qualifies them (`TypePair.FACTS_TO_PLAN`) and never uses a bare `Plan`.
