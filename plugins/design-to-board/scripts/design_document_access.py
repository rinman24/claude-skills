"""ResourceAccess for the design document file: reads its text, nothing more."""

from __future__ import annotations

from pathlib import Path


class DesignDocumentAccess:
    def read_text(self, path: str) -> str | None:
        """The document's text, or None if there is no readable file at `path`."""
        try:
            return Path(path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None
