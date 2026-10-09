"""design-to-board's command line: a Client of DesignToBoardManager. Transcribes and prints what it wrote, or with
`--dry-run` prints the plan and writes nothing; either way, a failure prints the report."""

from __future__ import annotations

import argparse
import sys

from contracts import (
    EXIT_FAILED_NOTHING_WRITTEN,
    EXIT_STOPPED_PARTWAY,
    EXIT_VALID,
    Plan,
    ReconcileResult,
    TranscribeResult,
    WithdrawStep,
    Write,
)
from design_to_board_manager import build_manager, step_name

NEXT = "Next: `squadra tick --dry-run` shows what squadra would claim."


def report(path: str, result: ReconcileResult) -> str:
    """The dry run's report: the failures, or the plan."""
    if result.failures:
        return "\n".join(failure_report(path, result))
    return "\n".join(render_plan(result.plan))


def transcribe_report(path: str, result: TranscribeResult) -> tuple[str, int]:
    """The run's report and exit code: failures (nothing written), stopped partway, or the writes done."""
    if result.reconcile.failures:
        return "\n".join(failure_report(path, result.reconcile)), EXIT_FAILED_NOTHING_WRITTEN
    plan = result.reconcile.plan
    where = f"map {plan.map}, revision {plan.revision}, under parent {plan.parent}"
    done = [render_write(write) for write in result.done]
    if result.stop is not None:
        total = len(result.done) + len(result.remaining)
        lines = [f"design-to-board: stopped partway, {len(result.done)} of {total} writes done ({where})", result.stop.line()]
        lines += [f"done: {line}" for line in done]
        lines += [f"remaining: {step_name(step)}" for step in result.remaining]
        return "\n".join(lines), EXIT_STOPPED_PARTWAY
    if not done:
        return "\n".join([f"design-to-board: {where}: nothing to write; the board already matches the document.", NEXT]), EXIT_VALID
    withdrawals, queues = len(plan.withdrawals), len(plan.queues)
    header = (
        f"design-to-board: transcribed {where}: {withdrawals} withdrawal{'s' if withdrawals != 1 else ''}, "
        f"{queues} queue{'s' if queues != 1 else ''}."
    )
    return "\n".join([header, *done, NEXT]), EXIT_VALID


def failure_report(path: str, result: ReconcileResult) -> list[str]:
    count = len(result.failures)
    lines = [f"design-to-board: failed, nothing written ({count} failure{'s' if count != 1 else ''} in {path})"]
    return lines + [failure.line() for failure in result.failures]


def render_write(write: Write) -> str:
    if isinstance(write.step, WithdrawStep):
        return f"withdrew {write.step.origin} · item {write.item_id}"
    predecessors = ", ".join(str(item_id) for item_id in write.predecessor_ids) or "none"
    return f"queued {write.step.origin} · item {write.item_id} · predecessors: {predecessors}"


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
        "It validates the document, reads the board, reconciles the two and writes the plan through `squadra board`.",
    )
    parser.add_argument("document", help="path to the design document, docs/design/<map>.md")
    parser.add_argument("--parent", type=int, help="the parent item ID; required on the map's first run")
    parser.add_argument("--dry-run", action="store_true", help="print the plan and write nothing")
    args = parser.parse_args(argv)
    manager = build_manager()
    if args.dry_run:
        result = manager.dry_run(args.document, args.parent)
        print(report(args.document, result))
        return EXIT_FAILED_NOTHING_WRITTEN if result.failures else EXIT_VALID
    text, exit_code = transcribe_report(args.document, manager.transcribe(args.document, args.parent))
    print(text)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
