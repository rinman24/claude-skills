"""DB10 (DB-D12): a map's first-run `--parent` outside squadra's claim scope fails under `--parent` before any write.

squadra answers the question (`squadra board scope`); design-to-board never reads its config (DB-D5).
"""

from pathlib import Path

import pytest

from design_to_board import main
from design_to_board_manager import WRITE_FIXES
from reconcile_engine import PARENT, PARENT_OUT_OF_SCOPE, ReconcileEngine
from squadra_board_access import SquadraBoardAccess

# default_document_text, make_document, read_document, make_increment, make_fake_squadra, fake_board
# are provided by tests/conftest.py

OUT_OF_SCOPE = (
    "--parent · map outscope · --parent 2 is outside squadra's claim scope · re-run with a `--parent` inside squadra's "
    "claim scope, or widen `[board].claim_scope` in squadra"
)


@pytest.fixture
def outscope(tmp_path: Path, default_document_text: str) -> str:
    """S5's probe map: a fresh map name, so no Origin of it is on the board (a first run)."""
    path = tmp_path / "outscope.md"
    path.write_text(default_document_text.replace("map: billing", "map: outscope", 1), encoding="utf-8")
    return str(path)


def _run(capsys, *args: str) -> tuple[int, list[str]]:
    exit_code = main(list(args))
    return exit_code, capsys.readouterr().out.splitlines()


def test_first_run_parent_out_of_scope_fails_under_parent(make_document, read_document) -> None:
    result = ReconcileEngine().reconcile(read_document(make_document()), {}, 2, False)

    assert result.plan is None
    assert [(f.check, f.row, f.fix) for f in result.failures] == [(PARENT, "map billing", PARENT_OUT_OF_SCOPE)]


def test_scope_answer_is_read_only_on_a_first_run(make_document, read_document, make_increment) -> None:
    engine = ReconcileEngine()
    snapshot = {"billing:I1": make_increment(101, parent=2)}

    assert engine.first_run_parent("billing", {}, 2) == 2
    assert engine.first_run_parent("billing", snapshot, 2) is None
    assert engine.check_parent("billing", snapshot, 2, False) == (2, [])


def test_access_reads_squadra_scope_answer(make_fake_squadra) -> None:
    make_fake_squadra(in_scope=False)

    assert SquadraBoardAccess().parent_in_claim_scope(2) is False


def test_probe_out_of_scope_parent_fails_the_dry_run_and_the_run_with_nothing_written(outscope, fake_board, capsys) -> None:
    fake_board.set_scope(1)

    for args in ((outscope, "--parent", "2", "--dry-run"), (outscope, "--parent", "2")):
        exit_code, lines = _run(capsys, *args)

        assert exit_code == 1
        assert OUT_OF_SCOPE in lines
    assert not fake_board.shim_config.exists()  # `squadra board queue` never ran
    assert fake_board.bytes() is None


def test_scope_narrowed_mid_run_stops_and_the_re_run_names_the_scope(outscope, fake_board, capsys) -> None:
    fake_board.before_write(1, scope=(1,))

    exit_code, lines = _run(capsys, outscope, "--parent", "2")

    assert exit_code == 3
    assert any(line.endswith(WRITE_FIXES[3]) for line in lines)
    assert fake_board.by_origin() == {}
    exit_code, lines = _run(capsys, outscope, "--parent", "2")  # before DB10 this passed and looped
    assert exit_code == 1
    assert OUT_OF_SCOPE in lines
