"""design-to-board's single entry point: validation, the board read, the reconcile and the walk of the plan's writes."""

from __future__ import annotations

from contracts import (
    BoardReadError,
    BoardWriteError,
    Failure,
    QueueStep,
    ReconcileResult,
    Snapshot,
    TranscribeResult,
    ValidationResult,
    WithdrawStep,
    Write,
)
from design_document_access import DesignDocumentAccess
from document_checks_engine import DocumentChecksEngine
from document_reader_engine import DocumentReaderEngine
from reconcile_engine import ReconcileEngine
from squadra_board_access import SquadraBoardAccess

INPUT_FIX = "pass the path of a design document (docs/design/<map>.md)"
BOARD_READ_FIXES = {
    None: "install squadra, and run design-to-board in the target repo",
    2: "fix squadra's configuration in the target repo (`squadra init --check`), then re-run design-to-board",
    3: "repair the board by hand in squadra, then re-run design-to-board",
}
BOARD_READ_FIX = "check squadra's board provider, then re-run design-to-board"
# A write squadra refused or failed, by squadra's exit code (verb-contract.md); the run stops there (DB-D6).
WRITE = "write"
WRITE_FIXES = {
    None: "install squadra, then re-run design-to-board to finish the remaining writes",
    1: "squadra's provider failed, so the item may be partial; check the provider, then re-run design-to-board, "
    "which finishes it and the remaining writes",
    2: "fix squadra's configuration in the target repo (`squadra init --check`), then re-run design-to-board "
    "to finish the remaining writes",
    3: "the board changed after design-to-board read it; re-run design-to-board, whose checks name what to do",
}
WRITE_FIX = "squadra failed in a way design-to-board doesn't know; check squadra, then re-run design-to-board"


class DesignToBoardManager:
    def __init__(
        self,
        document_access: DesignDocumentAccess,
        reader: DocumentReaderEngine,
        checks: DocumentChecksEngine,
        board: SquadraBoardAccess,
        reconcile: ReconcileEngine,
    ) -> None:
        self._document_access = document_access
        self._reader = reader
        self._checks = checks
        self._board = board
        self._reconcile = reconcile

    def validate(self, path: str) -> ValidationResult:
        """Read the document at `path` and run checks 6–15; every failure is collected."""
        text = self._document_access.read_text(path)
        if text is None:
            return ValidationResult(None, (Failure("input", path, "no readable file at this path", INPUT_FIX),))

        front_matter, failures, body_start = self._reader.read_front_matter(text)
        if front_matter is None:
            return ValidationResult(None, tuple(failures))
        failures = self._checks.check_front_matter(front_matter)
        if failures:
            return ValidationResult(None, tuple(failures), front_matter)

        document, failures = self._reader.read_body(text, front_matter, body_start)
        if document is None:
            return ValidationResult(None, tuple(failures), front_matter)
        return ValidationResult(document, tuple(self._checks.check_document(document)), front_matter)

    def dry_run(self, path: str, parent_arg: int | None) -> ReconcileResult:
        """Validate, read the board and reconcile; writes nothing. Board checks only on a valid document;
        the `--parent` checks whenever the map is known (DB-D6)."""
        return self._reconcile_board(path, parent_arg)[0]

    def transcribe(self, path: str, parent_arg: int | None) -> TranscribeResult:
        """The dry run, then the plan's writes in its order: withdrawals, then queues. Each queue's predecessor
        Origins resolve to item IDs from the snapshot or an earlier queue of this run; the plan is never
        recomputed. The first refusal stops the walk, so a refused withdrawal stops it before any queue (DB-D6)."""
        result, snapshot = self._reconcile_board(path, parent_arg)
        if result.failures:
            return TranscribeResult(result)
        plan = result.plan
        item_ids = {origin: item.item_id for origin, item in snapshot.items()}
        steps = (*plan.withdrawals, *plan.queues)
        done: list[Write] = []
        for index, step in enumerate(steps):
            try:
                if isinstance(step, WithdrawStep):
                    write = Write(step, self._board.withdraw_increment(step.origin))
                else:
                    predecessor_ids = tuple(item_ids[origin] for origin in step.predecessors)
                    item_id = self._board.queue_increment(step.origin, plan.parent, predecessor_ids, step.title, step.body)
                    write = Write(step, item_id, predecessor_ids)
                    item_ids[step.origin] = item_id
            except BoardWriteError as error:
                stop = Failure(WRITE, step_name(step), error.message, WRITE_FIXES.get(error.exit_code, WRITE_FIX))
                return TranscribeResult(result, tuple(done), stop, steps[index:])
            done.append(write)
        return TranscribeResult(result, tuple(done))

    def _reconcile_board(self, path: str, parent_arg: int | None) -> tuple[ReconcileResult, Snapshot]:
        validation = self.validate(path)
        front_matter = validation.front_matter
        if front_matter is None:
            return ReconcileResult(None, validation.failures), {}
        try:
            snapshot = self._board.increments_by_origin()
        except BoardReadError as error:
            fix = BOARD_READ_FIXES.get(error.exit_code, BOARD_READ_FIX)
            failure = Failure("board read", "squadra board origins", error.message, fix)
            return ReconcileResult(None, validation.failures + (failure,)), {}
        if not validation.valid:
            _, parent_failures = self._reconcile.check_parent(front_matter.map, snapshot, parent_arg)
            return ReconcileResult(None, validation.failures + tuple(parent_failures)), snapshot
        return self._reconcile.reconcile(validation.document, snapshot, parent_arg), snapshot


def step_name(step: WithdrawStep | QueueStep) -> str:
    return f"{'withdraw' if isinstance(step, WithdrawStep) else 'queue'} {step.origin}"


def build_manager() -> DesignToBoardManager:
    return DesignToBoardManager(
        DesignDocumentAccess(), DocumentReaderEngine(), DocumentChecksEngine(), SquadraBoardAccess(), ReconcileEngine(),
    )
