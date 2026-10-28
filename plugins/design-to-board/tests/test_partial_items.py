"""DB11 (DB-D13): a partial item the Plan's queue would refuse fails as board state before any write; DB12 (DB-D14):
the check is collected with the other board checks whenever a parent holds.

squadra gives the verdict (`squadra board partial-items`); design-to-board quotes its refusal, never words one.
"""

import json

import pytest

from contracts import FINISHES, QUEUED, REFUSES, BoardReadError, Failure, Increment, PartialItem, Plan, QueueStep, ReconcileResult
from design_to_board import main
from design_to_board_manager import BOARD_READ_FIXES
from reconcile_engine import BOARD, NOTE, REMOVE_PARTIAL, REPAIR_PARTIAL, ReconcileEngine
from squadra_board_access import SquadraBoardAccess

# make_document, make_fake_squadra, fake_board are provided by tests/conftest.py

I1_CREATE_WRITES = 3  # the fake's create of billing:I1, which has no predecessor: create, parent, commit (squadra N17)
REVISED = ("| I1 | Invoice store:", "| I1 | Invoice archive:")
PLAN = Plan("billing", 2, 1, (), (QueueStep("billing:I1", (), "Invoice store", "b"),))
DRAFTED = ReconcileResult(PLAN, (), draft=PLAN)


def _run(capsys, *args: str) -> tuple[int, list[str]]:
    exit_code = main(list(args))
    return exit_code, capsys.readouterr().out.splitlines()


def _writes(fake_board) -> int:
    return json.loads(fake_board.shim_config.read_text()).get("writes", 0)


def _partial(origin: str) -> dict[str, object]:
    return {"title": "t", "body": "b", "state": None, "parent": 1, "origin": origin, "predecessors": []}


@pytest.mark.parametrize("j", range(1, I1_CREATE_WRITES))
def test_probe_a_revised_title_on_a_partial_item_fails_before_any_write(j, make_document, fake_board, capsys) -> None:
    fake_board.seed({})
    fake_board.before_write(1, patch={"fail_create_after_step": j})
    assert _run(capsys, str(make_document()), "--parent", "1")[0] == 3
    (partial_id,) = fake_board.items()
    before = fake_board.bytes()
    revised = str(make_document(REVISED))

    for args in ((revised, "--parent", "1", "--dry-run"), (revised, "--parent", "1")):
        exit_code, lines = _run(capsys, *args)

        assert exit_code == 1  # before DB11: 3, and every re-run looped on WRITE_FIXES[3]
        (line,) = [line for line in lines if line.startswith(f"{BOARD} · I1 · ")]
        assert line.startswith(f"{BOARD} · I1 · billing:I1 is on partial item {partial_id}, and squadra would refuse its queue: ")
        assert f"origin 'billing:I1' is on partial item {partial_id}, which disagrees with this request: title" in line
        assert line.endswith(REPAIR_PARTIAL)
    assert _writes(fake_board) == 1  # `squadra board queue` never ran again
    assert fake_board.bytes() == before


def test_an_agreeing_partial_item_still_reads_as_a_queue_that_finishes_it(make_document, fake_board, capsys) -> None:
    fake_board.seed({})
    fake_board.before_write(1, patch={"fail_create_after_step": 2})
    path = str(make_document())
    _run(capsys, path, "--parent", "1")

    exit_code, lines = _run(capsys, path, "--parent", "1", "--dry-run")

    assert exit_code == 0
    assert "queue billing:I1 · Invoice store: invoices can be saved and read · predecessors: none" in lines
    assert not [line for line in lines if line.startswith(NOTE)]


def test_a_partial_item_no_queue_names_gets_a_note_and_blocks_nothing(make_document, fake_board, capsys) -> None:
    fake_board.seed({"1001": _partial("billing:I2"), "1002": _partial("billing:I9"), "1003": _partial("other:I1")})

    exit_code, lines = _run(capsys, str(make_document()), "--parent", "1")

    assert exit_code == 0
    assert [line for line in lines if line.startswith(NOTE)] == [
        f"{NOTE} · I2 · billing:I2 is on partial item 1001; no queue of this run finishes it, so it stays in no bucket "
        f"and nothing claims it · {REMOVE_PARTIAL}",
        f"{NOTE} · I9 · billing:I9 is on partial item 1002; no queue of this run finishes it, so it stays in no bucket "
        f"and nothing claims it · {REMOVE_PARTIAL}",
    ]
    assert lines[-1].startswith("Next: ")


def test_the_check_reads_only_the_maps_partial_items() -> None:
    reports = (
        PartialItem(1001, "billing:I1", REFUSES, "origin 'billing:I1' is on partial item 1001, which disagrees"),
        PartialItem(1002, "billing:I3", FINISHES, None),
        PartialItem(1003, "billing:I2", None, None),
        PartialItem(1004, "other:I1", REFUSES, "origin 'other:I1' is on partial item 1004, which disagrees"),
    )

    result = ReconcileEngine().check_partial_items(DRAFTED, reports)

    assert result.plan is None
    assert [(f.check, f.row, f.fix) for f in result.failures] == [(BOARD, "I1", REPAIR_PARTIAL)]
    assert result.failures[0].reason.endswith(": origin 'billing:I1' is on partial item 1001, which disagrees")
    assert [note.split(" · ")[:2] for note in result.notes] == [[NOTE, "I2"]]
    assert ReconcileEngine().check_partial_items(DRAFTED, reports[1:2]) == DRAFTED


def test_the_check_merges_the_reconciles_failures_and_withholds_the_plan_while_any_stand() -> None:
    other = Failure(BOARD, "I3", "r", "f")
    reports = (PartialItem(1001, "billing:I1", REFUSES, "x"), PartialItem(1003, "billing:I2", None, None))

    result = ReconcileEngine().check_partial_items(ReconcileResult(None, (other,), draft=PLAN), reports)

    assert result.plan is None
    assert [(f.row, f.fix) for f in result.failures] == [("I3", "f"), ("I1", REPAIR_PARTIAL)]
    assert [note.split(" · ")[:2] for note in result.notes] == [[NOTE, "I2"]]
    assert ReconcileEngine().check_partial_items(ReconcileResult(None, (other,), draft=PLAN), reports[1:]).plan is None


def test_access_sends_the_queue_steps_as_requests_and_reads_the_verdicts(make_fake_squadra) -> None:
    bin_dir = make_fake_squadra(partial_items=[
        {"item_id": 1005, "origin": "A:I1", "queue": "refuses", "disagrees_on": ["title"], "refusal": "r"},
        {"item_id": 1007, "origin": "B:I9", "queue": None, "disagrees_on": [], "refusal": None},
    ])
    steps = (QueueStep("A:I1", (), "New", "b\n"), QueueStep("A:I2", ("A:I1", "B:I3"), "Two", "c\n"))

    reports = SquadraBoardAccess().partial_items(7, steps)

    assert json.loads((bin_dir / "requests.json").read_text()) == [
        {"origin": "A:I1", "parent": 7, "predecessor_origins": [], "title": "New", "body": "b\n"},
        {"origin": "A:I2", "parent": 7, "predecessor_origins": ["A:I1", "B:I3"], "title": "Two", "body": "c\n"},
    ]
    assert reports == (PartialItem(1005, "A:I1", REFUSES, "r"), PartialItem(1007, "B:I9", None, None))


@pytest.mark.parametrize("partial_items", [None, [{"item_id": 1}], [{"item_id": 1, "origin": "A:I1", "queue": "maybe", "refusal": None}]])
def test_access_refuses_output_it_cant_read(partial_items, make_fake_squadra) -> None:
    make_fake_squadra(partial_items=partial_items)

    with pytest.raises(BoardReadError) as error:
        SquadraBoardAccess().partial_items(1, ())

    assert error.value.exit_code == 0


@pytest.mark.parametrize("exit_code", [2, 3, 1])
def test_a_partial_items_failure_routes_as_a_board_read(exit_code, make_document, make_fake_squadra, capsys) -> None:
    make_fake_squadra(partial_exit=exit_code)

    for args in ((str(make_document()), "--parent", "1", "--dry-run"), (str(make_document()), "--parent", "1")):
        code, lines = _run(capsys, *args)

        assert code == 1
        assert lines[1:] == [
            f"board read · squadra board partial-items · squadra board partial-items: failed · "
            f"{BOARD_READ_FIXES.get(exit_code, 'check squadra' + chr(39) + 's board provider, then re-run design-to-board')}"
        ]


MISSING_PREDECESSOR = ("PortalClient | I1 | 3 |", "PortalClient | I1, ledger:I3 | 3 |")
MISSING_LINE = "board · I3 · depends on ledger:I3, which is missing from the board · transcribe map ledger first, then re-run design-to-board"


def test_the_flip_a_partial_item_is_collected_with_another_failure(make_document, fake_board, capsys) -> None:
    fake_board.seed({})
    fake_board.before_write(1, patch={"fail_create_after_step": 2})
    assert _run(capsys, str(make_document()), "--parent", "1")[0] == 3
    (partial_id,) = fake_board.items()
    before = fake_board.bytes()
    revised = str(make_document(REVISED, MISSING_PREDECESSOR))

    for args in ((revised, "--parent", "1", "--dry-run"), (revised, "--parent", "1")):
        exit_code, lines = _run(capsys, *args)

        assert exit_code == 1
        assert lines[1] == MISSING_LINE
        assert lines[2].startswith(f"{BOARD} · I1 · billing:I1 is on partial item {partial_id}, and squadra would refuse its queue: ")
        assert len(lines) == 3  # before DB12: only MISSING_LINE, as `partial-items` was never asked
    assert _writes(fake_board) == 1  # no `queue` or `withdraw` after the first run's
    assert fake_board.bytes() == before


def test_a_partial_items_failure_is_collected_with_another_failure(make_document, make_fake_squadra, capsys) -> None:
    make_fake_squadra(partial_exit=3)

    for args in ((str(make_document(MISSING_PREDECESSOR)), "--parent", "1", "--dry-run"), (str(make_document(MISSING_PREDECESSOR)), "--parent", "1")):
        code, lines = _run(capsys, *args)

        assert code == 1
        assert lines[1:] == [
            MISSING_LINE,
            f"board read · squadra board partial-items · squadra board partial-items: failed · {BOARD_READ_FIXES[3]}",
        ]


REFUSED_I1 = [{"item_id": 1001, "origin": "billing:I1", "queue": "refuses", "disagrees_on": ["title"], "refusal": "r"}]
LATER = {"billing:I3": Increment(101, 1, QUEUED, True), "billing:I4": Increment(102, 1, QUEUED, True)}


@pytest.mark.parametrize(("snapshot", "args", "in_scope", "blocking"), [
    ({}, (), True, "--parent · map billing · --parent is required on the map's first run"),
    ({}, ("--parent", "2"), False, "--parent · map billing · --parent 2 is outside squadra's claim scope"),
    ({**LATER, "billing:I4": Increment(102, 2, QUEUED, True)}, (), True, "board · map billing · the map's items need one parent"),
    (LATER, ("--parent", "2"), True, "--parent · map billing · --parent 2 conflicts with parent 1"),
], ids=["first-run-no-parent", "first-run-out-of-scope", "two-parents", "conflicting-parent"])
def test_the_fence_partial_items_is_never_asked_without_a_parent(
    snapshot, args, in_scope, blocking, make_document, make_fake_squadra, capsys,
) -> None:
    bin_dir = make_fake_squadra(snapshot, in_scope=in_scope, partial_items=REFUSED_I1)

    for extra in (("--dry-run",), ()):
        code, lines = _run(capsys, str(make_document()), *args, *extra)

        assert code == 1
        assert len(lines) == 2 and lines[1].startswith(blocking)
    assert not (bin_dir / "requests.json").exists()


def test_the_fence_holds_on_an_invalid_document(make_document, make_fake_squadra, capsys) -> None:
    bin_dir = make_fake_squadra(partial_items=REFUSED_I1)

    code, lines = _run(capsys, str(make_document(("| I1 | Invoice store:", "| I1 | :"))), "--parent", "1")

    assert code == 1
    assert not [line for line in lines if " · I1 · billing:I1 is on partial item" in line]
    assert not (bin_dir / "requests.json").exists()
