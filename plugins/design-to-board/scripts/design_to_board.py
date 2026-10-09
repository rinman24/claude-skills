"""design-to-board's command line: a Client of DesignToBoardManager. Prints the report; never writes."""

from __future__ import annotations

import argparse
import sys

from contracts import EXIT_FAILED_NOTHING_WRITTEN, EXIT_VALID, ValidationResult
from design_to_board_manager import build_manager


def report(path: str, result: ValidationResult) -> str:
    if not result.valid:
        count = len(result.failures)
        lines = [f"design-to-board: failed, nothing written ({count} failure{'s' if count != 1 else ''} in {path})"]
        lines += [failure.line() for failure in result.failures]
        return "\n".join(lines)
    document = result.document
    live = sum(1 for row in document.increments if row.live)
    withdrawn = len(document.increments) - live
    front_matter = document.front_matter
    return (
        f"design-to-board: {path} is valid (map {front_matter.map}, revision {front_matter.revision}, "
        f"{live} live and {withdrawn} withdrawn increments). Nothing written: this version only validates."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="design-to-board",
        description="Validate a cleared wayfinder design document (DESIGN-FORMAT checks 6–15).",
    )
    parser.add_argument("document", help="path to the design document, docs/design/<map>.md")
    args = parser.parse_args(argv)
    result = build_manager().validate(args.document)
    print(report(args.document, result))
    return EXIT_VALID if result.valid else EXIT_FAILED_NOTHING_WRITTEN


if __name__ == "__main__":
    sys.exit(main())
