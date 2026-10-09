import json
import os
import shutil
import subprocess
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


SQUADRA_TOML = (
    '[board]\nprovider = "fake"\nclaim_scope = "parents"\nparent_scope_ids = [{scope}]\n'
    '[board.states]\nqueued = ["Backlog"]\nactive = ["Doing"]\ndone = ["Done"]\nwithdrawn = ["Dropped"]\n'
)
WRITE_SHIM = """#!{python}
import json, os, sys
from pathlib import Path
REAL, CONFIG, BOARD = {real!r}, Path({config!r}), Path({board!r})
if sys.argv[1:3] in (["board", "queue"], ["board", "withdraw"]):
    config = json.loads(CONFIG.read_text()) if CONFIG.exists() else {{}}
    config["writes"] = write = config.get("writes", 0) + 1
    CONFIG.write_text(json.dumps(config))
    hook = config.get("before", {{}}).get(str(write), {{}})
    if "patch" in hook:
        board = json.loads(BOARD.read_text()) if BOARD.exists() else {{"version": 1}}
        for item_id, fields in hook["patch"].pop("items", {{}}).items():
            board.setdefault("items", {{}}).setdefault(item_id, {{}}).update(fields)
        board.update(hook["patch"])
        BOARD.write_text(json.dumps(board))
    if "fail" in hook:
        code, message = hook["fail"]
        sys.stderr.write(f"squadra board {{sys.argv[2]}}: {{message}}\\n")
        sys.exit(code)
os.execv(REAL, [REAL, *sys.argv[1:]])
"""


def real_squadra() -> str:
    """The `squadra` on PATH, which must have `squadra board` (squadra SQ4); the test is skipped otherwise."""
    path = shutil.which("squadra")
    if path is None:
        pytest.skip("no `squadra` on PATH: install squadra (SQ4 or later) to run design-to-board against its fake board")
    if subprocess.run([path, "board", "--help"], capture_output=True).returncode != 0:
        pytest.skip(f"the `squadra` at {path} has no `squadra board` (squadra SQ4)")
    return path


class FakeBoard:
    """squadra's fake provider in a temporary target repo, reached through a shim that counts writes and can act
    before write `n` (one-based, across runs): fail it with an exit code, or patch the board file first."""

    def __init__(self, home: Path) -> None:
        self.home = home
        self.path = home / ".squadra" / "fake-board.json"
        self.shim_config = home / "shim.json"

    def set_scope(self, *parents: int) -> None:
        (self.home / "squadra.toml").write_text(SQUADRA_TOML.format(scope=", ".join(map(str, parents))), encoding="utf-8")

    def seed(self, items: Mapping[str, Mapping[str, object]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({"version": 1, "items": items}), encoding="utf-8")
        self.shim_config.unlink(missing_ok=True)

    def items(self) -> dict[str, dict[str, object]]:
        return json.loads(self.path.read_text(encoding="utf-8"))["items"] if self.path.exists() else {}

    def by_origin(self) -> dict[str, dict[str, object]]:
        return {item["origin"]: {"id": int(item_id), **item} for item_id, item in self.items().items()}

    def bytes(self) -> bytes | None:
        return self.path.read_bytes() if self.path.exists() else None

    def before_write(self, n: int, fail: tuple[int, str] | None = None, patch: Mapping[str, object] | None = None) -> None:
        config = json.loads(self.shim_config.read_text()) if self.shim_config.exists() else {}
        hook = config.setdefault("before", {}).setdefault(str(n), {})
        if fail is not None:
            hook["fail"] = list(fail)
        if patch is not None:
            hook["patch"] = dict(patch)
        self.shim_config.write_text(json.dumps(config))


@pytest.fixture
def fake_board(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> FakeBoard:
    """A target repo whose `squadra.toml` names `provider = "fake"`, claim scope parents 1 and 2, behind the shim."""
    real = real_squadra()
    home = tmp_path / "target"
    home.mkdir()
    board = FakeBoard(home)
    board.set_scope(1, 2)
    for name in [name for name in os.environ if name.startswith("FLEET_")]:
        monkeypatch.delenv(name)
    monkeypatch.setenv("FLEET_HOME", str(home))
    shim_dir = tmp_path / "shim"
    shim_dir.mkdir()
    shim = shim_dir / "squadra"
    shim.write_text(
        WRITE_SHIM.format(python=sys.executable, real=real, config=str(board.shim_config), board=str(board.path)),
        encoding="utf-8",
    )
    shim.chmod(0o755)
    monkeypatch.setenv("PATH", f"{shim_dir}{os.pathsep}{os.environ['PATH']}")
    return board
