from pathlib import Path

import pytest

from contracts import WITHDRAWN, BoardReadError
from squadra_board_access import SquadraBoardAccess

# make_increment, make_fake_squadra
# are provided by tests/conftest.py


def test_reads_squadra_json_into_the_snapshot(make_fake_squadra, make_increment) -> None:
    snapshot = {"billing:I1": make_increment(101), "billing:I2": make_increment(102, WITHDRAWN, None, False)}
    make_fake_squadra(snapshot)

    assert SquadraBoardAccess().increments_by_origin() == snapshot


def test_squadra_refusal_carries_exit_code_and_last_stderr_line(make_fake_squadra) -> None:
    make_fake_squadra(exit_code=3, stderr="partial item 9 carries billing:I1\nsquadra board origins: duplicate Origin\n")

    with pytest.raises(BoardReadError) as raised:
        SquadraBoardAccess().increments_by_origin()

    assert (raised.value.exit_code, raised.value.message) == (3, "squadra board origins: duplicate Origin")


def test_no_squadra_on_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PATH", str(tmp_path))

    with pytest.raises(BoardReadError) as raised:
        SquadraBoardAccess().increments_by_origin()

    assert raised.value.exit_code is None


def test_unknown_lifecycle_is_refused(make_fake_squadra, make_increment) -> None:
    make_fake_squadra({"billing:I1": make_increment(101, "held")})

    with pytest.raises(BoardReadError, match="Lifecycle `held`"):
        SquadraBoardAccess().increments_by_origin()
