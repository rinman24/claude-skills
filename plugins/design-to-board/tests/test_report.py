import subprocess
import sys
from pathlib import Path

from contracts import Failure

# make_document
# is provided by tests/conftest.py

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "design_to_board.py"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


def test_report_line_is_check_row_reason_fix() -> None:
    failure = Failure("check 8", "I3", "Touches names `X`, which Services doesn't declare", "revise the map")

    assert failure.line() == "check 8 · I3 · Touches names `X`, which Services doesn't declare · revise the map"


def test_valid_document_says_so_and_exits_0(make_document) -> None:
    path = make_document()

    completed = _run(str(path))

    assert completed.returncode == 0
    assert completed.stdout == (
        f"design-to-board: {path} is valid (map billing, revision 2, 3 live and 1 withdrawn increments). "
        "Nothing written: this version only validates.\n"
    )


def test_failing_document_reports_every_line_and_exits_1(make_document) -> None:
    path = make_document(("PortalClient | I1 | 3 |", "PortalClient | I1, I2 | 3 |"))

    completed = _run(str(path))

    assert completed.returncode == 1
    assert completed.stdout.splitlines() == [
        f"design-to-board: failed, nothing written (1 failure in {path})",
        "check 14 · I3 · depends on I2, which is withdrawn · revise the map in wayfinder and Publish again",
    ]


def test_missing_file_fails_and_writes_nothing(tmp_path: Path) -> None:
    completed = _run(str(tmp_path / "nope.md"))

    assert completed.returncode == 1
    assert "input · " in completed.stdout
