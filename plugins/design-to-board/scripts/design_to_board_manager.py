"""design-to-board's single entry point: validation, the board read and the reconcile. The writes come later (DB4)."""

from __future__ import annotations

from contracts import BoardReadError, Failure, ReconcileResult, ValidationResult
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
        validation = self.validate(path)
        front_matter = validation.front_matter
        if front_matter is None:
            return ReconcileResult(None, validation.failures)
        try:
            snapshot = self._board.increments_by_origin()
        except BoardReadError as error:
            fix = BOARD_READ_FIXES.get(error.exit_code, BOARD_READ_FIX)
            return ReconcileResult(None, validation.failures + (Failure("board read", "squadra board origins", error.message, fix),))
        if not validation.valid:
            _, parent_failures = self._reconcile.check_parent(front_matter.map, snapshot, parent_arg)
            return ReconcileResult(None, validation.failures + tuple(parent_failures))
        return self._reconcile.reconcile(validation.document, snapshot, parent_arg)


def build_manager() -> DesignToBoardManager:
    return DesignToBoardManager(
        DesignDocumentAccess(), DocumentReaderEngine(), DocumentChecksEngine(), SquadraBoardAccess(), ReconcileEngine(),
    )
