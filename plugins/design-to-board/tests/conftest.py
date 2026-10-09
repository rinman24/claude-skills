import json
import os
import sys
from collections.abc import Callable, Mapping
from dataclasses import asdict
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from contracts import QUEUED, DesignDocument, Increment, ValidationResult  # noqa: E402
from design_to_board_manager import build_manager  # noqa: E402


@pytest.fixture
def default_document_text() -> str:
    return (FIXTURES / "valid.md").read_text(encoding="utf-8")


@pytest.fixture
def make_document(tmp_path: Path, default_document_text: str) -> Callable[..., Path]:
    """Write the valid document with each (old, new) replacement applied once; return its path."""

    def _factory(*replacements: tuple[str, str]) -> Path:
        text = default_document_text
        for old, new in replacements:
            assert text.count(old) == 1, f"fixture edit must match exactly once: {old!r}"
            text = text.replace(old, new)
        path = tmp_path / "billing.md"
        path.write_text(text, encoding="utf-8")
        return path

    return _factory


@pytest.fixture
def validate() -> Callable[[Path], ValidationResult]:
    manager = build_manager()
    return lambda path: manager.validate(str(path))


@pytest.fixture
def read_document(validate: Callable[[Path], ValidationResult]) -> Callable[[Path], DesignDocument]:
    """The read document at `path`, which must be valid."""

    def _read(path: Path) -> DesignDocument:
        result = validate(path)
        assert result.valid, [failure.line() for failure in result.failures]
        return result.document

    return _read


@pytest.fixture
def make_increment() -> Callable[..., Increment]:
    """One snapshot entry: QUEUED under parent 1, in claim scope, unless told otherwise."""

    def _factory(item_id: int, lifecycle: str = QUEUED, parent: int | None = 1, in_claim_scope: bool = True) -> Increment:
        return Increment(item_id, parent, lifecycle, in_claim_scope)

    return _factory


@pytest.fixture
def make_fake_squadra(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Callable[..., Path]:
    """Put a stub `squadra` first on PATH: `board origins` prints `snapshot` as squadra's JSON, or fails as told.

    Any other arguments exit 2, as squadra's argparse would. Returns the stub's directory.
    """

    def _factory(snapshot: Mapping[str, Increment] | None = None, exit_code: int = 0, stderr: str = "") -> Path:
        stdout = json.dumps({origin: asdict(item) for origin, item in (snapshot or {}).items()}) if exit_code == 0 else ""
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir(exist_ok=True)
        stub = bin_dir / "squadra"
        stub.write_text(
            f"#!{sys.executable}\n"
            "import sys\n"
            "if sys.argv[1:] != ['board', 'origins']:\n"
            "    sys.exit(2)\n"
            f"sys.stderr.write({stderr!r})\n"
            f"sys.stdout.write({stdout!r})\n"
            f"sys.exit({exit_code})\n",
            encoding="utf-8",
        )
        stub.chmod(0o755)
        monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
        return bin_dir

    return _factory
