"""The reconcile (DB-D9): a valid design document against squadra's board, through the translation table, yields the Plan.

Pure: the Manager reads the snapshot and passes it in. The board checks are the
table's failure cells plus the parent (DB-D5), predecessor and claim-scope
(DB-D4) rules; every failure is collected (DB-D6). Each cell traces to a rule
owned by wayfinder, squadra or write safety; a cell needing any other rule
reopens WD14.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass

from contracts import (
    ABSENT,
    ACTIVE,
    DONE,
    QUEUED,
    WITHDRAWN,
    DesignDocument,
    Failure,
    Increment,
    IncrementRow,
    Plan,
    QueueStep,
    ReconcileResult,
    Snapshot,
    WithdrawStep,
)

ROW_LIVE = "live"
ROW_WITHDRAWN = "withdrawn"
ROW_STATES = (ROW_LIVE, ROW_WITHDRAWN)

QUEUE = "queue"
WITHDRAW = "withdraw"
NOTHING = "nothing"

BOARD = "board"
PARENT = "--parent"
REPAIR_BY_HAND = "repair the board by hand in squadra, then re-run design-to-board"
RESTORE_SCOPE = "restore the parent to squadra's claim scope (`parent_scope_ids`), then re-run design-to-board"


@dataclass(frozen=True, slots=True)
class Refusal:
    """A failure cell; `reason` and `fix` take {origin}, {item} and {row}."""

    reason: str
    fix: str

    def failure(self, row: IncrementRow, origin: str, item: Increment) -> Failure:
        values = {"origin": origin, "item": item.item_id, "row": row.id}
        return Failure(BOARD, row.id, self.reason.format(**values), self.fix.format(**values))


# Row state × item Lifecycle → action. ABSENT includes an Origin only a partial item carries (DB-D10).
TRANSLATION_TABLE: dict[tuple[str, str], str | Refusal] = {
    (ROW_LIVE, ABSENT): QUEUE,  # DB-D1; on a partial item the queue finishes it (DB-D10)
    (ROW_LIVE, QUEUED): NOTHING,  # DB-D1
    (ROW_LIVE, ACTIVE): NOTHING,  # DB-D1
    (ROW_LIVE, DONE): NOTHING,  # DB-D1
    (ROW_LIVE, WITHDRAWN): Refusal(  # squadra never reuses a withdrawn Origin (N6)
        "{origin} (item {item}) is withdrawn on the board, and squadra never reuses a withdrawn Origin",
        "revise the map in wayfinder: withdraw {row} and queue the work as a new increment",
    ),
    (ROW_WITHDRAWN, ABSENT): NOTHING,  # DB-D9
    (ROW_WITHDRAWN, QUEUED): WITHDRAW,  # DB-D1, DB-D2, DB-D10 (by Origin)
    (ROW_WITHDRAWN, ACTIVE): Refusal(  # DB-D2
        "{origin} (item {item}) is active; squadra withdraws only a queued increment",
        "wait for the run to finish or stop it in squadra, then re-run design-to-board",
    ),
    (ROW_WITHDRAWN, DONE): Refusal(  # DB-D2
        "{origin} (item {item}) is delivered; change delivered work with a new increment, not a withdrawal",
        "revise the map in wayfinder: a delivered increment can't be withdrawn",
    ),
    (ROW_WITHDRAWN, WITHDRAWN): NOTHING,  # DB-D2: a re-run is idempotent
}


class ReconcileEngine:
    def check_parent(self, map_name: str, snapshot: Snapshot, parent_arg: int | None) -> tuple[int | None, list[Failure]]:
        """DB-D5's `--parent` rules, which run even on an invalid document. Returns the map's parent, if one holds."""
        items = _map_items(map_name, snapshot)
        if not items:
            if parent_arg is None:
                return None, [Failure(
                    PARENT, f"map {map_name}",
                    f"--parent is required on the map's first run (no `{map_name}:` Origin is on the board)",
                    "re-run with --parent <the parent item ID>",
                )]
            return parent_arg, []
        parents: dict[int | None, list[str]] = {}
        for origin, item in items.items():
            parents.setdefault(item.parent, []).append(origin)
        if len(parents) > 1 or None in parents:
            carried = "; ".join(
                f"{'no parent' if parent is None else f'parent {parent}'} ({', '.join(origins)})"
                for parent, origins in sorted(parents.items(), key=lambda entry: (entry[0] is None, entry[0] or 0))
            )
            return None, [Failure(BOARD, f"map {map_name}", f"the map's items need one parent; they carry {carried}", REPAIR_BY_HAND)]
        (parent,) = parents
        if parent_arg is not None and parent_arg != parent:
            return None, [Failure(
                PARENT, f"map {map_name}",
                f"--parent {parent_arg} conflicts with parent {parent}, which the map's items carry",
                f"re-run without --parent, or with --parent {parent}",
            )]
        return parent, []

    def reconcile(self, document: DesignDocument, snapshot: Snapshot, parent_arg: int | None) -> ReconcileResult:
        """The document against the snapshot: the Plan, or every failure (parent checks, then rows in ID order)."""
        map_name = document.front_matter.map
        parent, failures = self.check_parent(map_name, snapshot, parent_arg)
        failures += _check_scope(map_name, snapshot)
        rows = sorted(document.increments, key=lambda row: row.number)
        to_withdraw: list[IncrementRow] = []
        to_queue: list[IncrementRow] = []
        for row in rows:
            origin = _origin(map_name, row.id)
            item = snapshot.get(origin)
            cell = TRANSLATION_TABLE[(ROW_LIVE if row.live else ROW_WITHDRAWN, item.lifecycle if item else ABSENT)]
            if isinstance(cell, Refusal):
                failures.append(cell.failure(row, origin, item))
            elif cell == WITHDRAW:
                to_withdraw.append(row)
            elif cell == QUEUE:
                to_queue.append(row)
            if row.live:
                failures += _check_predecessors(row, snapshot)
        failures += _check_unknown_origins(map_name, snapshot, {row.id for row in rows})
        if failures or parent is None:
            return ReconcileResult(None, tuple(failures))
        plan = Plan(
            map_name,
            document.front_matter.revision,
            parent,
            tuple(WithdrawStep(_origin(map_name, row.id)) for row in _kahn(to_withdraw)),
            tuple(_queue_step(map_name, row) for row in _kahn(to_queue)),
        )
        return ReconcileResult(plan, ())


def _origin(map_name: str, entry: str) -> str:
    """A row ID or `Depends on` entry as an Origin: `<map>:<ID>`, a cross-map entry as written."""
    return entry if ":" in entry else f"{map_name}:{entry}"


def _map_items(map_name: str, snapshot: Snapshot) -> dict[str, Increment]:
    """The map's Origins on the board, in row-number order."""
    prefix = f"{map_name}:"
    origins = [origin for origin in snapshot if origin.startswith(prefix)]
    return {origin: snapshot[origin] for origin in sorted(origins, key=_origin_order)}


def _origin_order(origin: str) -> tuple[int, str]:
    row_id = origin.rpartition(":")[2]
    return (int(row_id[1:]), origin) if row_id[1:].isdigit() else (0, origin)


def _check_scope(map_name: str, snapshot: Snapshot) -> list[Failure]:
    """Juval's case 5: the map's items out of claim scope are reported, never re-queued."""
    outside = [origin for origin, item in _map_items(map_name, snapshot).items() if not item.in_claim_scope]
    if not outside:
        return []
    reason = f"the map's items are outside squadra's claim scope: {', '.join(outside)}"
    return [Failure(BOARD, f"map {map_name}", reason, RESTORE_SCOPE)]


def _check_predecessors(row: IncrementRow, snapshot: Snapshot) -> list[Failure]:
    """DB-D4: a cross-map predecessor must be on the board, not withdrawn, and in claim scope."""
    failures: list[Failure] = []
    for entry in row.depends_on:
        if ":" not in entry:
            continue
        item = snapshot.get(entry)
        other_map = entry.partition(":")[0]
        if item is None:
            failures.append(Failure(
                BOARD, row.id, f"depends on {entry}, which is missing from the board",
                f"transcribe map {other_map} first, then re-run design-to-board",
            ))
        elif item.lifecycle == WITHDRAWN:
            failures.append(Failure(
                BOARD, row.id, f"depends on {entry} (item {item.item_id}), which is withdrawn",
                f"revise the map in wayfinder: depend on what replaced {entry}",
            ))
        elif not item.in_claim_scope:
            failures.append(Failure(
                BOARD, row.id, f"depends on {entry} (item {item.item_id}), which is outside squadra's claim scope",
                RESTORE_SCOPE,
            ))
    return failures


def _check_unknown_origins(map_name: str, snapshot: Snapshot, row_ids: set[str]) -> list[Failure]:
    """An Origin of this map with no row in the table: the table has no cell for it, so it fails loudly."""
    return [
        Failure(BOARD, origin.partition(":")[2], f"{origin} (item {item.item_id}) is on the board, but the table has no such row", REPAIR_BY_HAND)
        for origin, item in _map_items(map_name, snapshot).items()
        if origin.partition(":")[2] not in row_ids
    ]


def _kahn(rows: list[IncrementRow]) -> list[IncrementRow]:
    """Predecessors first among `rows`, ties broken by `(Order, numeric ID)` (DB-D6)."""
    by_id = {row.id: row for row in rows}
    waiting = {row.id: {d for d in row.same_map_depends_on if d in by_id} for row in rows}
    ready = [(row.order, row.number) for row in rows if not waiting[row.id]]
    heapq.heapify(ready)
    ordered: list[IncrementRow] = []
    while ready:
        _, number = heapq.heappop(ready)
        done = f"I{number}"
        ordered.append(by_id[done])
        for row_id in sorted(waiting, key=lambda r: by_id[r].number):
            if done in waiting[row_id]:
                waiting[row_id].discard(done)
                if not waiting[row_id]:
                    heapq.heappush(ready, (by_id[row_id].order, by_id[row_id].number))
    return ordered


def _queue_step(map_name: str, row: IncrementRow) -> QueueStep:
    origin = _origin(map_name, row.id)
    return QueueStep(origin, tuple(_origin(map_name, entry) for entry in row.depends_on), row.name, _body(origin, row))


def _body(origin: str, row: IncrementRow) -> str:
    """From row fields and the Origin only, never the revision (a retry that finishes a partial item must match)."""
    fields = [
        ("Origin", origin),
        ("Increment", row.name),
        ("Kind", row.kind),
        ("Touches", ", ".join(row.touches)),
        ("Depends on", ", ".join(row.depends_on)),
        ("Decided by", ", ".join(row.decided_by)),
    ]
    return "".join(f"{name}: {value}\n" for name, value in fields if value)
