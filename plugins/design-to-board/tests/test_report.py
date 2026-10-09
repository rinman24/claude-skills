import os
import subprocess
import sys
from pathlib import Path

import pytest

from contracts import DONE, Failure

# make_document, make_increment, make_fake_squadra
# are provided by tests/conftest.py

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "design_to_board.py"
GOLDEN = Path(__file__).resolve().parent / "fixtures" / "billing-r2.plan"


def _run(*args: str, env: dict[str, str] | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=env, cwd=cwd)


@pytest.fixture
def default_r2_board(make_increment) -> dict:
    """Billing after revision 1, I3's create lost to a crash (a partial item reads as absent): I1 delivered, I2 queued."""
    return {"billing:I1": make_increment(101, DONE), "billing:I2": make_increment(102)}


def test_report_line_is_check_row_reason_fix() -> None:
    failure = Failure("check 8", "I3", "Touches names `X`, which Services doesn't declare", "revise the map")

    assert failure.line() == "check 8 · I3 · Touches names `X`, which Services doesn't declare · revise the map"


def test_dry_run_prints_the_golden_plan_and_exits_0(make_document, make_fake_squadra, default_r2_board) -> None:
    """T1."""
    make_fake_squadra(default_r2_board)

    completed = _run(str(make_document()), "--dry-run")

    assert completed.returncode == 0
    assert completed.stdout == GOLDEN.read_text(encoding="utf-8")


def test_dry_run_output_is_byte_identical_across_environments(make_document, make_fake_squadra, default_r2_board, tmp_path: Path) -> None:
    """T3: hash seed, time zone, locale and working directory don't reach the plan."""
    make_fake_squadra(default_r2_board)
    path = str(make_document())
    outputs = []
    for seed, tz, locale, cwd in (("1", "UTC", "C", "a"), ("4242", "Asia/Kolkata", "en_US.UTF-8", "b")):
        (tmp_path / cwd).mkdir()
        env = {**os.environ, "PYTHONHASHSEED": seed, "TZ": tz, "LC_ALL": locale}
        outputs.append(_run(path, "--dry-run", env=env, cwd=tmp_path / cwd).stdout)

    assert outputs[0] == outputs[1] != ""


def test_board_already_matching_says_nothing_to_write(make_document, make_fake_squadra, make_increment) -> None:
    make_fake_squadra({f"billing:I{n}": make_increment(100 + n) for n in (1, 3, 4)})

    completed = _run(str(make_document()), "--dry-run")

    assert completed.stdout == (
        "design-to-board: dry run for map billing, revision 2, under parent 1: "
        "nothing to write; the board already matches the document.\n"
    )


def test_failing_document_reports_document_and_parent_failures_and_exits_1(make_document, make_fake_squadra) -> None:
    make_fake_squadra({})
    path = make_document(("PortalClient | I1 | 3 |", "PortalClient | I1, I2 | 3 |"))

    completed = _run(str(path), "--dry-run")

    assert completed.returncode == 1
    assert completed.stdout.splitlines() == [
        f"design-to-board: failed, nothing written (2 failures in {path})",
        "check 14 · I3 · depends on I2, which is withdrawn · revise the map in wayfinder and Publish again",
        "--parent · map billing · --parent is required on the map's first run (no `billing:` Origin is on the board) "
        "· re-run with --parent <the parent item ID>",
    ]


@pytest.mark.parametrize(
    ("exit_code", "fix"),
    [
        (2, "fix squadra's configuration in the target repo (`squadra init --check`), then re-run design-to-board"),
        (3, "repair the board by hand in squadra, then re-run design-to-board"),
        (1, "check squadra's board provider, then re-run design-to-board"),
    ],
)
def test_board_read_failure_is_routed_by_squadra_exit_code(exit_code: int, fix: str, make_document, make_fake_squadra) -> None:
    make_fake_squadra(exit_code=exit_code, stderr="squadra board origins: it went wrong\n")

    completed = _run(str(make_document()), "--dry-run")

    assert completed.returncode == 1
    assert completed.stdout.splitlines()[1] == f"board read · squadra board origins · squadra board origins: it went wrong · {fix}"


def test_missing_file_fails_and_writes_nothing(tmp_path: Path) -> None:
    completed = _run(str(tmp_path / "nope.md"))

    assert completed.returncode == 1
    assert "input · " in completed.stdout
