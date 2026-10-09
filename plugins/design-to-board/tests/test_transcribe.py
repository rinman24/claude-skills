import pytest

from contracts import DONE, QUEUED, BoardWriteError, QueueStep, WithdrawStep
from design_document_access import DesignDocumentAccess
from design_to_board import main
from design_to_board_manager import WRITE_FIX, WRITE_FIXES, DesignToBoardManager, build_manager
from document_checks_engine import DocumentChecksEngine
from document_reader_engine import DocumentReaderEngine
from reconcile_engine import ReconcileEngine
from squadra_board_access import SquadraBoardAccess

# make_document, make_increment, fake_board
# are provided by tests/conftest.py

# Billing after revision 1 (as in test_report.py): I1 delivered, I2 queued. Revision 2's plan is three writes:
# withdraw billing:I2, queue billing:I4, queue billing:I3, each queue with one predecessor (item 101).
R1_ITEMS = {
    "101": {"title": "Invoice store", "body": "b", "state": "Done", "parent": 1, "origin": "billing:I1"},
    "102": {"title": "Raise on order", "body": "b", "state": "Backlog", "parent": 1, "origin": "billing:I2"},
}
WRITES = 3
CREATE_WRITES = 4  # the fake's create: create, parent, one predecessor, commit (squadra N17)


def _run(capsys, *args: str) -> tuple[int, list[str]]:
    exit_code = main(list(args))
    return exit_code, capsys.readouterr().out.splitlines()


def test_writes_land_on_the_board_as_the_plan_says(make_document, fake_board, capsys) -> None:
    fake_board.seed(R1_ITEMS)
    path = str(make_document())
    plan = build_manager().dry_run(path, None).plan

    exit_code, lines = _run(capsys, path)

    assert exit_code == 0
    board = fake_board.by_origin()
    assert board["billing:I2"]["state"] == "Dropped"
    queued = [board[step.origin] for step in plan.queues]
    for step, item in zip(plan.queues, queued):
        assert (item["title"], item["body"], item["parent"], item["state"]) == (step.title, step.body, 1, "Backlog")
        assert item["predecessors"] == [board[origin]["id"] for origin in step.predecessors]
    assert [item["id"] for item in queued] == sorted(item["id"] for item in queued)
    i4, i3 = (item["id"] for item in queued)
    assert lines == [
        "design-to-board: transcribed map billing, revision 2, under parent 1: 1 withdrawal, 2 queues.",
        "withdrew billing:I2 · item 102",
        f"queued billing:I4 · item {i4} · predecessors: 101",
        f"queued billing:I3 · item {i3} · predecessors: 101",
        "Next: `squadra tick --dry-run` shows what squadra would claim.",
    ]


def test_a_queue_resolves_a_predecessor_queued_earlier_in_the_run(make_document, fake_board, capsys) -> None:
    exit_code, _ = _run(capsys, str(make_document()), "--parent", "1")

    board = fake_board.by_origin()
    assert exit_code == 0
    assert board["billing:I3"]["predecessors"] == board["billing:I4"]["predecessors"] == [board["billing:I1"]["id"]]
    assert "billing:I2" not in board


def test_a_second_run_writes_nothing_and_says_so(make_document, fake_board, capsys) -> None:
    fake_board.seed(R1_ITEMS)
    path = str(make_document())
    _run(capsys, path)
    before = fake_board.bytes()

    exit_code, lines = _run(capsys, path)

    assert (exit_code, fake_board.bytes()) == (0, before)
    assert lines[0] == "design-to-board: map billing, revision 2, under parent 1: nothing to write; the board already matches the document."


CRASHES = [("before write", n, None) for n in range(1, WRITES + 1)] + [
    ("inside create", n, j) for n in (2, 3) for j in range(1, CREATE_WRITES + 1)
]


@pytest.mark.parametrize(("where", "n", "j"), CRASHES)
def test_a_run_stopped_at_any_write_converges_on_re_run(where, n, j, make_document, fake_board, capsys) -> None:
    path = str(make_document())
    fake_board.seed(R1_ITEMS)
    _run(capsys, path)
    reference = fake_board.items()
    fake_board.seed(R1_ITEMS)
    if j is None:
        fake_board.before_write(n, fail=(1, "ConnectionError: the provider dropped the call"))
    else:
        fake_board.before_write(n, patch={"fail_create_after_step": j})

    stopped, lines = _run(capsys, path)
    partial = [item for item in fake_board.items().values() if item["state"] is None]
    rerun, _ = _run(capsys, path)

    assert len(partial) == (1 if j is not None and j < CREATE_WRITES else 0)
    assert lines[0] == f"design-to-board: stopped partway, {n - 1} of {WRITES} writes done (map billing, revision 2, under parent 1)"
    assert lines[1].startswith("write · ") and lines[1].endswith(WRITE_FIXES[1])
    assert len([line for line in lines if line.startswith("remaining: ")]) == WRITES - n + 1
    assert (stopped, rerun) == (3, 0)
    assert fake_board.items() == reference


def test_a_refused_withdrawal_stops_the_run_before_any_queue(make_document, fake_board, capsys) -> None:
    fake_board.seed(R1_ITEMS)
    fake_board.before_write(1, patch={"items": {"102": {"state": "Doing"}}})  # a tick claims I2 after the read
    path = str(make_document())

    stopped, lines = _run(capsys, path)
    rerun, rerun_lines = _run(capsys, path)

    assert stopped == 3
    assert lines[:2] == [
        "design-to-board: stopped partway, 0 of 3 writes done (map billing, revision 2, under parent 1)",
        lines[1],
    ]
    assert lines[1].startswith("write · withdraw billing:I2 · squadra board withdraw: ") and lines[1].endswith(WRITE_FIXES[3])
    assert lines[2:] == ["remaining: withdraw billing:I2", "remaining: queue billing:I4", "remaining: queue billing:I3"]
    assert set(fake_board.by_origin()) == {"billing:I1", "billing:I2"}
    assert rerun == 1 and rerun_lines[1].startswith("board · I2 · ")


class _RefusingBoard(SquadraBoardAccess):
    def __init__(self, snapshot, exit_code) -> None:
        self._snapshot, self._exit_code = snapshot, exit_code

    def increments_by_origin(self):
        return self._snapshot

    def withdraw_increment(self, origin: str) -> int:
        raise BoardWriteError(self._exit_code, "squadra board withdraw: refused")


def test_every_squadra_exit_code_has_a_write_fix() -> None:
    assert set(WRITE_FIXES) == {None, 1, 2, 3}


@pytest.mark.parametrize(("exit_code", "fix"), [*WRITE_FIXES.items(), (7, WRITE_FIX)])
def test_a_stopped_write_is_routed_by_squadra_exit_code(exit_code, fix, make_document, make_increment) -> None:
    snapshot = {"billing:I1": make_increment(101, DONE), "billing:I2": make_increment(102, QUEUED)}
    manager = DesignToBoardManager(
        DesignDocumentAccess(), DocumentReaderEngine(), DocumentChecksEngine(), _RefusingBoard(snapshot, exit_code), ReconcileEngine()
    )

    result = manager.transcribe(str(make_document()), None)

    assert (result.done, result.stop.line()) == ((), f"write · withdraw billing:I2 · squadra board withdraw: refused · {fix}")
    assert [type(step) for step in result.remaining] == [WithdrawStep, QueueStep, QueueStep]
