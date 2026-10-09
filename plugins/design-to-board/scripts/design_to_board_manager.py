"""design-to-board's single entry point. Validation only, for now: the board steps come later (DB3, DB4)."""

from __future__ import annotations

from contracts import Failure, ValidationResult
from design_document_access import DesignDocumentAccess
from document_checks_engine import DocumentChecksEngine
from document_reader_engine import DocumentReaderEngine

INPUT_FIX = "pass the path of a design document (docs/design/<map>.md)"


class DesignToBoardManager:
    def __init__(
        self,
        document_access: DesignDocumentAccess,
        reader: DocumentReaderEngine,
        checks: DocumentChecksEngine,
    ) -> None:
        self._document_access = document_access
        self._reader = reader
        self._checks = checks

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
            return ValidationResult(None, tuple(failures))

        document, failures = self._reader.read_body(text, front_matter, body_start)
        if document is None:
            return ValidationResult(None, tuple(failures))
        return ValidationResult(document, tuple(self._checks.check_document(document)))


def build_manager() -> DesignToBoardManager:
    return DesignToBoardManager(DesignDocumentAccess(), DocumentReaderEngine(), DocumentChecksEngine())
