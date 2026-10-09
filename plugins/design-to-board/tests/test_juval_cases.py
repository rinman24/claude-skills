"""Juval's seven board cases (DB-D4) end to end: design-to-board's CLI through `squadra board` on the fake provider.

Setup: map billing (I1, I3, I4 live) under parent P; map portal's I3 also depends on `billing:I3`, under parent Q;
both in claim scope. Cases 2 and 7 are only possible here; the rest are also plan tests in test_reconcile.py.
"""

from collections.abc import Callable
from pathlib import Path

import pytest

from design_to_board import main

# default_document_text, fake_board
# are provided by tests/conftest.py

P, Q = "1", "2"
PORTAL = (("map: billing", "map: portal"), ("PortalClient | I1 | 3 |", "PortalClient | I1, billing:I3 | 3 |"))
WITHDRAW_BILLING_I3 = (("04-portal.md | r1 |", "04-portal.md | r1, withdrawn r2 |"),)


@pytest.fixture
def write_map(tmp_path: Path, default_document_text: str) -> Callable[..., str]:
    def _write(name: str, *replacements: tuple[str, str]) -> str:
        text = default_document_text
        for old, new in replacements:
            assert text.count(old) == 1, f"fixture edit must match exactly once: {old!r}"
            text = text.replace(old, new)
        path = tmp_path / f"{name}.md"
        path.write_text(text, encoding="utf-8")
        return str(path)

    return _write


@pytest.fixture
def billing(write_map) -> str:
    return write_map("billing")


@pytest.fixture
def portal(write_map) -> str:
    return write_map("portal", *PORTAL)


def _run(capsys, *args: str) -> tuple[int, list[str]]:
    exit_code = main(list(args))
    return exit_code, capsys.readouterr().out.splitlines()


def _both_transcribed(capsys, billing: str, portal: str) -> None:
    assert _run(capsys, billing, "--parent", P)[0] == 0
    assert _run(capsys, portal, "--parent", Q)[0] == 0


def test_case_1_map_run_before_its_predecessor_map_fails(portal, fake_board, capsys) -> None:
    exit_code, lines = _run(capsys, portal, "--parent", Q)

    assert exit_code == 1
    assert lines[1] == "board · I3 · depends on billing:I3, which is missing from the board · transcribe map billing first, then re-run design-to-board"
    assert fake_board.bytes() is None


def test_case_2_cross_map_predecessor_resolves_to_its_item_id(billing, portal, fake_board, capsys) -> None:
    _both_transcribed(capsys, billing, portal)

    board = fake_board.by_origin()
    assert board["billing:I3"]["id"] in board["portal:I3"]["predecessors"]
    assert {origin: item["parent"] for origin, item in board.items()} == {
        "billing:I1": 1, "billing:I3": 1, "billing:I4": 1, "portal:I1": 2, "portal:I3": 2, "portal:I4": 2,
    }


def test_case_3_re_run_without_parent_writes_nothing(billing, portal, fake_board, capsys) -> None:
    _both_transcribed(capsys, billing, portal)
    before = fake_board.bytes()

    exit_code, lines = _run(capsys, portal)

    assert (exit_code, fake_board.bytes()) == (0, before)
    assert "nothing to write" in lines[0]


def test_case_4_conflicting_parent_is_refused(billing, portal, fake_board, capsys) -> None:
    _both_transcribed(capsys, billing, portal)
    before = fake_board.bytes()

    exit_code, lines = _run(capsys, portal, "--parent", P)

    assert (exit_code, fake_board.bytes()) == (1, before)
    assert lines[1].startswith("--parent · map portal · --parent 1 conflicts with parent 2")


def test_case_5_items_out_of_scope_are_reported_not_requeued(billing, portal, fake_board, capsys) -> None:
    _both_transcribed(capsys, billing, portal)
    fake_board.set_scope(1)
    before = fake_board.bytes()

    exit_code, lines = _run(capsys, portal)

    assert (exit_code, fake_board.bytes()) == (1, before)
    assert "the map's items are outside squadra's claim scope: portal:I1, portal:I3, portal:I4" in lines[1]


def test_case_6_withdrawn_cross_map_predecessor_fails(billing, portal, write_map, fake_board, capsys) -> None:
    _both_transcribed(capsys, billing, portal)
    assert _run(capsys, write_map("billing", *WITHDRAW_BILLING_I3))[0] == 0
    item = fake_board.by_origin()["billing:I3"]
    before = fake_board.bytes()

    exit_code, lines = _run(capsys, portal)

    assert (exit_code, fake_board.bytes(), item["state"]) == (1, before, "Dropped")
    assert lines[1].startswith(f"board · I3 · depends on billing:I3 (item {item['id']}), which is withdrawn")


def test_case_7_duplicate_origin_names_both_items(billing, fake_board, capsys) -> None:
    assert _run(capsys, billing, "--parent", P)[0] == 0
    first = fake_board.by_origin()["billing:I1"]["id"]
    fake_board.seed({**fake_board.items(), "999": {"title": "copy", "body": "b", "state": "Backlog", "parent": 1, "origin": "billing:I1"}})

    exit_code, lines = _run(capsys, billing)

    assert exit_code == 1
    assert lines[1].startswith("board read · squadra board origins · ")
    assert lines[1].endswith("repair the board by hand in squadra, then re-run design-to-board")
    assert "999" in lines[1] and str(first) in lines[1]
