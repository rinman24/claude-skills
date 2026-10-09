import sys
from collections.abc import Callable
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from contracts import ValidationResult  # noqa: E402
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
