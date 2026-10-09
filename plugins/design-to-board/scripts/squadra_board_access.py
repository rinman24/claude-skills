"""ResourceAccess for squadra's board: runs `squadra board {origins,queue,withdraw}` in the current directory.

squadra resolves its own `squadra.toml`; design-to-board never reads it (DB-D5).
"""

from __future__ import annotations

import json
import subprocess
from collections.abc import Sequence

from contracts import ABSENT, LIFECYCLES, BoardReadError, BoardWriteError, Increment, Snapshot


class SquadraBoardAccess:
    def increments_by_origin(self) -> Snapshot:
        """Every Origin an Increment carries, any Lifecycle; raises BoardReadError if squadra gives none."""
        entries = _run(["origins"], BoardReadError)
        try:
            snapshot = {
                origin: Increment(entry["item_id"], entry["parent"], entry["lifecycle"], entry["in_claim_scope"])
                for origin, entry in entries.items()
            }
        except (KeyError, TypeError, AttributeError) as error:
            raise BoardReadError(0, f"`squadra board origins` printed something other than its JSON ({error})") from None
        for origin, item in snapshot.items():
            if item.lifecycle not in LIFECYCLES or item.lifecycle == ABSENT:
                raise BoardReadError(0, f"{origin} has Lifecycle `{item.lifecycle}`, which design-to-board doesn't know")
        return snapshot

    def queue_increment(self, origin: str, parent: int, predecessors: Sequence[int], title: str, body: str) -> int:
        """`queue_increment` through the CLI, the body on stdin; returns the item ID or raises BoardWriteError."""
        args = ["queue", "--origin", origin, "--parent", str(parent)]
        for item_id in predecessors:
            args += ["--predecessor", str(item_id)]
        args += ["--title", title, "--body-file", "-"]
        return _item_id(_run(args, BoardWriteError, body), "queue")

    def withdraw_increment(self, origin: str) -> int:
        """`withdraw_increment` by Origin through the CLI; returns the item ID or raises BoardWriteError."""
        return _item_id(_run(["withdraw", "--origin", origin], BoardWriteError), "withdraw")


def _run(args: list[str], error: type[BoardReadError] | type[BoardWriteError], stdin: str = "") -> dict:
    """Run `squadra board <args>` and return its JSON; squadra's exit code and last stderr line go into `error`."""
    try:
        completed = subprocess.run(["squadra", "board", *args], input=stdin, capture_output=True, text=True)
    except FileNotFoundError:
        raise error(None, "no `squadra` command on PATH") from None
    if completed.returncode != 0:
        message = completed.stderr.strip().splitlines()
        raise error(completed.returncode, message[-1] if message else "no message")
    try:
        document = json.loads(completed.stdout)
    except ValueError as parse_error:
        raise error(0, f"`squadra board {args[0]}` printed something other than its JSON ({parse_error})") from None
    if not isinstance(document, dict):
        raise error(0, f"`squadra board {args[0]}` printed something other than its JSON")
    return document


def _item_id(document: dict, verb: str) -> int:
    item_id = document.get("item_id")
    if not isinstance(item_id, int):
        raise BoardWriteError(0, f"`squadra board {verb}` printed no item_id: {json.dumps(document)}")
    return item_id
