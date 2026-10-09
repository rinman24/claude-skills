"""design-to-board's command line: a Client of DesignToBoardManager. Prints the report or the plan; never writes."""

from __future__ import annotations

import argparse
import sys

from contracts import EXIT_FAILED_NOTHING_WRITTEN, EXIT_VALID, Plan, ReconcileResult
from design_to_board_manager import build_manager

NO_EXECUTOR = "Nothing written: this version stops at the plan; the writes come in a later version."


def report(path: str, result: ReconcileResult, dry_run: bool) -> str:
    if result.failures:
        count = len(result.failures)
        lines = [f"design-to-board: failed, nothing written ({count} failure{'s' if count != 1 else ''} in {path})"]
        lines += [failure.line() for failure in result.failures]
        return "\n".join(lines)
    lines = render_plan(result.plan)
    if not dry_run:
        lines.append(NO_EXECUTOR)
    return "\n".join(lines)


def render_plan(plan: Plan) -> list[str]:
    """The plan as the dry run prints it: one line per step, each queue's body indented under it."""
    withdrawals, queues = len(plan.withdrawals), len(plan.queues)
    header = f"design-to-board: dry run for map {plan.map}, revision {plan.revision}, under parent {plan.parent}"
    if not withdrawals and not queues:
        return [f"{header}: nothing to write; the board already matches the document."]
    lines = [
        f"{header}: {withdrawals} withdrawal{'s' if withdrawals != 1 else ''}, "
        f"{queues} queue{'s' if queues != 1 else ''}. Nothing written."
    ]
    lines += [f"withdraw {step.origin}" for step in plan.withdrawals]
    for step in plan.queues:
        predecessors = ", ".join(step.predecessors) or "none"
        lines.append(f"queue {step.origin} · {step.title} · predecessors: {predecessors}")
        lines += [f"    {line}" for line in step.body.splitlines()]
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="design-to-board",
        description="Transcribe a cleared wayfinder design document into increments on squadra's board. "
        "This version validates the document, reads the board and prints the plan; it writes nothing.",
    )
    parser.add_argument("document", help="path to the design document, docs/design/<map>.md")
    parser.add_argument("--parent", type=int, help="the parent item ID; required on the map's first run")
    parser.add_argument("--dry-run", action="store_true", help="print the plan and write nothing")
    args = parser.parse_args(argv)
    result = build_manager().dry_run(args.document, args.parent)
    print(report(args.document, result, args.dry_run))
    return EXIT_FAILED_NOTHING_WRITTEN if result.failures else EXIT_VALID


if __name__ == "__main__":
    sys.exit(main())
