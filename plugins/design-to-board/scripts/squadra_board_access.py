"""ResourceAccess for squadra's board: runs `squadra board origins` in the current directory and reads its JSON.

squadra resolves its own `squadra.toml`; design-to-board never reads it (DB-D5).
"""

from __future__ import annotations

import json
import subprocess

from contracts import ABSENT, LIFECYCLES, BoardReadError, Increment, Snapshot


class SquadraBoardAccess:
    def increments_by_origin(self) -> Snapshot:
        """Every Origin an Increment carries, any Lifecycle; raises BoardReadError if squadra gives none."""
        try:
            completed = subprocess.run(["squadra", "board", "origins"], capture_output=True, text=True)
        except FileNotFoundError:
            raise BoardReadError(None, "no `squadra` command on PATH") from None
        if completed.returncode != 0:
            message = completed.stderr.strip().splitlines()
            raise BoardReadError(completed.returncode, message[-1] if message else "no message")
        try:
            entries = json.loads(completed.stdout)
            snapshot = {
                origin: Increment(entry["item_id"], entry["parent"], entry["lifecycle"], entry["in_claim_scope"])
                for origin, entry in entries.items()
            }
        except (ValueError, KeyError, TypeError, AttributeError) as error:
            raise BoardReadError(0, f"`squadra board origins` printed something other than its JSON ({error})") from None
        for origin, item in snapshot.items():
            if item.lifecycle not in LIFECYCLES or item.lifecycle == ABSENT:
                raise BoardReadError(0, f"{origin} has Lifecycle `{item.lifecycle}`, which design-to-board doesn't know")
        return snapshot
