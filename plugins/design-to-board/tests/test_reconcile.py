import dataclasses
import itertools
from collections.abc import Callable
from pathlib import Path

import pytest

from contracts import ABSENT, ACTIVE, DONE, LIFECYCLES, QUEUED, WITHDRAWN, DesignDocument, Increment
from reconcile_engine import (
    NOTHING,
    QUEUE,
    ROW_LIVE,
    ROW_STATES,
    TRANSLATION_TABLE,
    WITHDRAW,
    ReconcileEngine,
    Refusal,
)

# make_document, read_document, make_increment
# are provided by tests/conftest.py

P, Q = 1, 2
# Juval's setup (DB-D4) on the fixture: map billing under P; map portal's I3 also depends on billing:I3, under Q.
PORTAL = (("map: billing", "map: portal"), ("PortalClient | I1 | 3 |", "PortalClient | I1, billing:I3 | 3 |"))


def _reconcile(document: DesignDocument, snapshot: dict[str, Increment], parent_arg: int | None = None):
    return ReconcileEngine().reconcile(document, snapshot, parent_arg)


def _transcribed(map_name: str, parent: int, make_increment, **lifecycles: str) -> dict[str, Increment]:
    """The map after its first run of revision 2: I1, I3 and I4 queued; I2 never on the board."""
    base = 100 if map_name == "billing" else 200
    states = {"I1": QUEUED, "I3": QUEUED, "I4": QUEUED, **lifecycles}
    return {
        f"{map_name}:{row}": make_increment(base + int(row[1:]), state, parent)
        for row, state in states.items()
        if state != ABSENT
    }


def test_translation_table_has_every_cell_and_only_known_actions() -> None:
    assert set(TRANSLATION_TABLE) == set(itertools.product(ROW_STATES, LIFECYCLES))
    for cell in TRANSLATION_TABLE.values():
        assert isinstance(cell, Refusal) or cell in (QUEUE, WITHDRAW, NOTHING)


@pytest.mark.parametrize("cell", list(itertools.product(ROW_STATES, LIFECYCLES)))
def test_reconcile_acts_on_each_cell_as_the_table_says(cell, make_document, read_document, make_increment) -> None:
    row_state, lifecycle = cell
    row = "I1" if row_state == ROW_LIVE else "I2"
    snapshot = _transcribed("billing", P, make_increment, **{row: lifecycle})

    result = _reconcile(read_document(make_document()), snapshot)

    action = TRANSLATION_TABLE[cell]
    if isinstance(action, Refusal):
        assert result.plan is None
        assert [(f.check, f.row) for f in result.failures] == [("board", row)]
        return
    assert result.failures == ()
    queued = {step.origin for step in result.plan.queues}
    withdrawn = {step.origin for step in result.plan.withdrawals}
    assert (f"billing:{row}" in queued, f"billing:{row}" in withdrawn) == (action == QUEUE, action == WITHDRAW)


def test_first_run_queues_live_rows_in_kahn_order_and_skips_a_withdrawn_row(make_document, read_document) -> None:
    plan = _reconcile(read_document(make_document()), {}, P).plan

    assert plan.withdrawals == ()
    assert [(step.origin, step.predecessors) for step in plan.queues] == [
        ("billing:I1", ()),
        ("billing:I4", ("billing:I1",)),
        ("billing:I3", ("billing:I1",)),
    ]


def test_withdrawals_go_predecessors_first_before_order(make_document, read_document, make_increment) -> None:
    path = make_document(
        ("| I1 | 3 | scratch:wayfinder/billing/04-portal.md | r1 |", "| I1 | 3 | scratch:wayfinder/billing/04-portal.md | r1, withdrawn r2 |"),
        ("| I1 | 2 | scratch:wayfinder/billing/03-invoice-trigger.md | r2 |", "| I1, I3 | 2 | scratch:wayfinder/billing/03-invoice-trigger.md | r1, withdrawn r2 |"),
    )
    snapshot = _transcribed("billing", P, make_increment, I2=QUEUED)

    plan = _reconcile(read_document(path), snapshot).plan

    assert [step.origin for step in plan.withdrawals] == ["billing:I2", "billing:I3", "billing:I4"]
    assert plan.queues == ()


def test_queue_step_title_and_body_come_from_row_fields_and_origin(make_document, read_document) -> None:
    step = _reconcile(read_document(make_document()), {}, P).plan.queues[0]

    assert step.title == "Invoice store: invoices can be saved and read"
    assert step.body == (
        "Origin: billing:I1\n"
        "Increment: Invoice store: invoices can be saved and read\n"
        "Kind: foundation → I2, I3\n"
        "Touches: InvoiceManager, InvoiceAccess\n"
        "Decided by: scratch:wayfinder/billing/03-invoice-trigger.md\n"
    )


def test_plan_is_invariant_under_row_and_snapshot_order(make_document, read_document, make_increment) -> None:
    """T2: every order of the table's rows and of the snapshot gives one plan."""
    document = read_document(make_document())
    snapshot = _transcribed("billing", P, make_increment, I2=QUEUED, I4=ABSENT)
    expected = _reconcile(document, snapshot)
    assert expected.plan is not None

    for rows in itertools.permutations(document.increments):
        for entries in (snapshot.items(), reversed(snapshot.items())):
            permuted = dataclasses.replace(document, increments=rows)
            assert _reconcile(permuted, dict(entries)) == expected


def test_first_run_without_parent_is_refused(make_document, read_document) -> None:
    result = _reconcile(read_document(make_document()), {})

    assert [failure.check for failure in result.failures] == ["--parent"]
    assert "first run" in result.failures[0].reason


def test_items_under_more_than_one_parent_fail(make_document, read_document, make_increment) -> None:
    snapshot = _transcribed("billing", P, make_increment)
    snapshot["billing:I4"] = make_increment(104, parent=Q)

    result = _reconcile(read_document(make_document()), snapshot)

    assert [f.line() for f in result.failures] == [
        "board · map billing · the map's items need one parent; they carry parent 1 (billing:I1, billing:I3); "
        "parent 2 (billing:I4) · repair the board by hand in squadra, then re-run design-to-board"
    ]


def test_an_origin_with_no_row_in_the_table_fails(make_document, read_document, make_increment) -> None:
    snapshot = {**_transcribed("billing", P, make_increment), "billing:I9": make_increment(109)}

    result = _reconcile(read_document(make_document()), snapshot)

    assert [(f.row, f.reason) for f in result.failures] == [
        ("I9", "billing:I9 (item 109) is on the board, but the table has no such row")
    ]


def test_juval_case_1_map_run_before_its_predecessor_map_fails(make_document, read_document) -> None:
    result = _reconcile(read_document(make_document(*PORTAL)), {}, Q)

    assert [(f.row, f.reason) for f in result.failures] == [("I3", "depends on billing:I3, which is missing from the board")]
    assert result.failures[0].fix == "transcribe map billing first, then re-run design-to-board"


def test_juval_case_3_re_run_without_parent_writes_nothing(make_document, read_document, make_increment) -> None:
    snapshot = {**_transcribed("billing", P, make_increment), **_transcribed("portal", Q, make_increment)}

    result = _reconcile(read_document(make_document(*PORTAL)), snapshot)

    assert result.failures == ()
    assert (result.plan.parent, result.plan.withdrawals, result.plan.queues) == (Q, (), ())


def test_juval_case_4_conflicting_parent_is_refused(make_document, read_document, make_increment) -> None:
    snapshot = {**_transcribed("billing", P, make_increment), **_transcribed("portal", Q, make_increment)}

    result = _reconcile(read_document(make_document(*PORTAL)), snapshot, P)

    assert [f.line() for f in result.failures] == [
        "--parent · map portal · --parent 1 conflicts with parent 2, which the map's items carry · "
        "re-run without --parent, or with --parent 2"
    ]


def test_juval_case_5_items_out_of_scope_are_reported_not_requeued(make_document, read_document, make_increment) -> None:
    portal = {origin: dataclasses.replace(item, in_claim_scope=False) for origin, item in _transcribed("portal", Q, make_increment).items()}
    snapshot = {**_transcribed("billing", P, make_increment), **portal}

    result = _reconcile(read_document(make_document(*PORTAL)), snapshot)

    assert result.plan is None
    assert [(f.row, f.reason) for f in result.failures] == [
        ("map portal", "the map's items are outside squadra's claim scope: portal:I1, portal:I3, portal:I4")
    ]


def test_juval_case_6_withdrawn_cross_map_predecessor_fails(make_document, read_document, make_increment) -> None:
    snapshot = {**_transcribed("billing", P, make_increment, I3=WITHDRAWN), **_transcribed("portal", Q, make_increment)}

    result = _reconcile(read_document(make_document(*PORTAL)), snapshot)

    assert [(f.row, f.reason) for f in result.failures] == [("I3", "depends on billing:I3 (item 103), which is withdrawn")]


def test_board_failures_are_all_collected(make_document, read_document, make_increment) -> None:
    snapshot = _transcribed("billing", P, make_increment, I1=WITHDRAWN, I2=ACTIVE, I3=DONE)

    result = _reconcile(read_document(make_document()), snapshot, Q)

    assert [(f.check, f.row) for f in result.failures] == [("--parent", "map billing"), ("board", "I1"), ("board", "I2")]


def test_check_parent_reads_the_parent_off_the_map_items(make_increment) -> None:
    parent, failures = ReconcileEngine().check_parent("billing", {"billing:I1": make_increment(101, parent=7)}, None)

    assert (parent, failures) == (7, [])
