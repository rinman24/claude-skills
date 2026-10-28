"""ResourceAccess for squadra's board: runs `squadra board {origins,scope,partial-items,queue,withdraw}` in the current
directory.

squadra resolves its own `squadra.toml`; design-to-board never reads it (DB-D5).
"""

from __future__ import annotations

import json
import subprocess
from collections.abc import Sequence

from contracts import (
    ABSENT, FINISHES, LIFECYCLES, REFUSES, BoardReadError, BoardWriteError, Increment, PartialItem, QueueStep, Snapshot,
)


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

    def parent_in_claim_scope(self, parent: int) -> bool:
        """`squadra board scope`: whether an item under `parent` is inside squadra's claim scope (squadra's rule, never
        read here, DB-D12); raises BoardReadError if squadra gives no answer."""
        answer = _run(["scope", "--parent", str(parent)], BoardReadError).get("in_claim_scope")
        if not isinstance(answer, bool):
            raise BoardReadError(0, "`squadra board scope` printed no in_claim_scope")
        return answer

    def partial_items(self, parent: int, steps: Sequence[QueueStep]) -> tuple[PartialItem, ...]:
        """`squadra board partial-items`: every partial item on the board, each with squadra's verdict on the queue step
        naming its Origin (requests on stdin, one per step under `parent`); raises BoardReadError if squadra gives none."""
        requests = [
            {"origin": step.origin, "parent": parent, "predecessor_origins": list(step.predecessors),
             "title": step.title, "body": step.body}
            for step in steps
        ]
        entries = _run(["partial-items", "--requests-file", "-"], BoardReadError, json.dumps(requests)).get("partial_items")
        try:
            reports = tuple(
                PartialItem(entry["item_id"], entry["origin"], entry["queue"], entry["refusal"]) for entry in entries
            )
        except (KeyError, TypeError) as error:
            raise BoardReadError(0, f"`squadra board partial-items` printed something other than its JSON ({error})") from None
        for report in reports:
            if report.queue not in (REFUSES, FINISHES, None) or (report.queue == REFUSES) != isinstance(report.refusal, str):
                raise BoardReadError(0, f"partial item {report.item_id} has verdict `{report.queue}`, which design-to-board doesn't know")
        return reports

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
