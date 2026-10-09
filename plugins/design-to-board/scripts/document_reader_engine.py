"""The strict reader: DESIGN-FORMAT's grammar exactly; anything else is a document defect (DB-D7).

It reads the contract (front matter, Services, Increments, Rules and planning
assumptions) and the behaviour IDs in Destination, which check 15 needs.
Decisions is record only and is not read.
"""

from __future__ import annotations

import re

from contracts import (
    LAYERS,
    SECTIONS,
    DesignDocument,
    Failure,
    FrontMatter,
    IncrementRow,
    Service,
)

GRAMMAR = "grammar"
DOCUMENT_FIX = "revise the map in wayfinder and Publish again; don't edit the document by hand"

FRONT_MATTER_KEYS = ("format", "map", "status", "revision", "changed")
STATUSES = ("cleared", "revising")
SERVICES_HEADER = ("Service", "Layer", "Encapsulates", "Introduced in")
INCREMENTS_HEADER = (
    "ID", "Increment", "Kind", "Touches", "Depends on", "Order", "Decided by", "Published",
)

MAP_NAME = r"[a-z0-9][a-z0-9._-]*"
ROW_ID = re.compile(r"I[1-9]\d*")
DEPENDENCY = re.compile(rf"(?:{MAP_NAME}:)?I[1-9]\d*")
BEHAVIOUR_LINE = re.compile(r"- (B[1-9]\d*): \S.*")
POSITIVE_INT = re.compile(r"[1-9]\d*")
PUBLISHED = re.compile(r"r([1-9]\d*)(?:, withdrawn r([1-9]\d*))?")
INTEGRATION_RULE = re.compile(r"- Rule: at most (\d+) changed services\b.*")
RULES_LINE = re.compile(r"- (?:Rule|Assumption): \S.*")
SEPARATOR = re.compile(r"\|(?:\s*:?-+:?\s*\|)+")


def _failure(line: int | str, reason: str) -> Failure:
    row = f"line {line}" if isinstance(line, int) else line
    return Failure(GRAMMAR, row, reason, DOCUMENT_FIX)


def _cells(line: str) -> tuple[str, ...]:
    return tuple(cell.strip() for cell in line.strip()[1:-1].split("|"))


def _list(cell: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in cell.split(",")) if cell else ()


class DocumentReaderEngine:
    def read_front_matter(self, text: str) -> tuple[FrontMatter | None, list[Failure], int]:
        """Front matter, its failures, and the index of the first body line."""
        lines = text.splitlines()
        if not lines or lines[0] != "---":
            return None, [_failure(1, "the document doesn't open with front matter (`---`)")], 0
        try:
            end = lines.index("---", 1)
        except ValueError:
            return None, [_failure(1, "front matter is never closed (`---`)")], 0

        failures: list[Failure] = []
        values: dict[str, str] = {}
        for number, line in enumerate(lines[1:end], start=2):
            key, sep, value = line.partition(":")
            if not sep or key not in FRONT_MATTER_KEYS:
                failures.append(_failure(number, f"front matter line `{line}` isn't one of {', '.join(FRONT_MATTER_KEYS)}"))
            elif key in values:
                failures.append(_failure(number, f"front matter repeats `{key}`"))
            else:
                values[key] = value.strip()
        for key in FRONT_MATTER_KEYS:
            if key not in values:
                failures.append(_failure("front matter", f"`{key}` is missing"))
        if failures:
            return None, failures, end + 1

        if not values["format"]:
            failures.append(_failure("front matter", "`format` is empty"))
        if not re.fullmatch(MAP_NAME, values["map"]):
            failures.append(_failure("front matter", f"`map: {values['map']}` isn't a map directory name"))
        if values["status"] not in STATUSES:
            failures.append(_failure("front matter", f"`status: {values['status']}` isn't cleared or revising"))
        if not POSITIVE_INT.fullmatch(values["revision"]):
            failures.append(_failure("front matter", f"`revision: {values['revision']}` isn't a positive integer"))
        changed = re.fullmatch(r"\[(.*)\]", values["changed"])
        names = _list(changed.group(1).strip()) if changed else ()
        if not changed or any(name not in SECTIONS for name in names):
            failures.append(_failure("front matter", f"`changed: {values['changed']}` isn't a list of section names"))
        elif values["revision"] == "1" and names:
            failures.append(_failure("front matter", "`changed` must be empty on revision 1"))
        if failures:
            return None, failures, end + 1

        front_matter = FrontMatter(
            values["format"], values["map"], values["status"], int(values["revision"]), names
        )
        return front_matter, [], end + 1

    def read_body(
        self, text: str, front_matter: FrontMatter, start: int
    ) -> tuple[DesignDocument | None, list[Failure]]:
        lines = text.splitlines()
        failures: list[Failure] = []
        sections = self._split_sections(lines, start, failures)

        behaviours = self._read_behaviours(sections.get("Destination", []), failures)
        services = self._read_services(sections.get("Services", []), failures)
        increments = self._read_increments(sections.get("Increments", []), front_matter, failures)
        max_changed = self._read_rules(sections.get("Rules and planning assumptions", []), failures)

        if failures:
            return None, failures
        return DesignDocument(front_matter, behaviours, services, increments, max_changed), []

    def _split_sections(
        self, lines: list[str], start: int, failures: list[Failure]
    ) -> dict[str, list[tuple[int, str]]]:
        sections: dict[str, list[tuple[int, str]]] = {}
        current: str | None = None
        title_seen = False
        for index in range(start, len(lines)):
            number, line = index + 1, lines[index]
            if line.startswith("## "):
                name = line[3:].strip()
                if name not in SECTIONS:
                    failures.append(_failure(number, f"unknown section `{line}`"))
                    current = None
                elif name in sections:
                    failures.append(_failure(number, f"section `{name}` appears twice"))
                    current = None
                else:
                    expected = SECTIONS[len(sections)] if len(sections) < len(SECTIONS) else None
                    if name != expected:
                        failures.append(_failure(number, f"section `{name}` is out of order; expected `{expected}`"))
                    sections[name] = []
                    current = name
            elif current is not None:
                sections[current].append((number, line))
            elif line.startswith("# ") and not title_seen and not sections:
                title_seen = True
            elif line.strip():
                failures.append(_failure(number, f"`{line}` is outside any section"))
        if not title_seen:
            failures.append(_failure("document", "the `# <Map title>` heading is missing"))
        for name in SECTIONS:
            if name not in sections:
                failures.append(_failure("document", f"section `{name}` is missing"))
        return sections

    def _read_behaviours(self, lines: list[tuple[int, str]], failures: list[Failure]) -> tuple[str, ...]:
        behaviours: list[str] = []
        for number, line in lines:
            if not line.startswith("- "):
                continue
            match = BEHAVIOUR_LINE.fullmatch(line)
            if not match:
                failures.append(_failure(number, f"Destination line `{line}` isn't `- B<n>: <behaviour>`"))
            elif match.group(1) in behaviours:
                failures.append(_failure(number, f"behaviour {match.group(1)} appears twice"))
            else:
                behaviours.append(match.group(1))
        return tuple(behaviours)

    def _read_table(
        self, name: str, header: tuple[str, ...], lines: list[tuple[int, str]], failures: list[Failure]
    ) -> list[tuple[int, tuple[str, ...]]]:
        content = [(number, line) for number, line in lines if line.strip()]
        if len(content) < 2 or _cells(content[0][1]) != header or not SEPARATOR.fullmatch(content[1][1].strip()):
            at = content[0][0] if content else name
            failures.append(_failure(at, f"{name} must be one table with the header `| {' | '.join(header)} |`"))
            return []
        rows: list[tuple[int, tuple[str, ...]]] = []
        for number, line in content[2:]:
            stripped = line.strip()
            if not (stripped.startswith("|") and stripped.endswith("|")):
                failures.append(_failure(number, f"`{line}` isn't a row of the {name} table"))
                continue
            cells = _cells(stripped)
            if len(cells) != len(header):
                failures.append(_failure(number, f"{name} row has {len(cells)} cells; expected {len(header)}"))
                continue
            rows.append((number, cells))
        return rows

    def _read_services(self, lines: list[tuple[int, str]], failures: list[Failure]) -> tuple[Service, ...]:
        services: list[Service] = []
        names: set[str] = set()
        for number, (name, layer, encapsulates, introduced_in) in self._read_table(
            "Services", SERVICES_HEADER, lines, failures
        ):
            row_failures = len(failures)
            if not name:
                failures.append(_failure(number, "a service has no name"))
            elif name in names:
                failures.append(_failure(number, f"service `{name}` is declared twice"))
            if layer not in LAYERS:
                failures.append(_failure(number, f"`{name}` has layer `{layer}`; expected one of {', '.join(LAYERS)}"))
            if introduced_in and not ROW_ID.fullmatch(introduced_in):
                failures.append(_failure(number, f"`{name}` Introduced in `{introduced_in}` isn't an increment ID"))
            if introduced_in and not encapsulates:
                failures.append(_failure(number, f"`{name}` is new (Introduced in {introduced_in}) but Encapsulates is blank"))
            if len(failures) == row_failures:
                names.add(name)
                services.append(Service(name, layer, encapsulates, introduced_in or None, number))
        return tuple(services)

    def _read_increments(
        self, lines: list[tuple[int, str]], front_matter: FrontMatter, failures: list[Failure]
    ) -> tuple[IncrementRow, ...]:
        rows: list[IncrementRow] = []
        for number, cells in self._read_table("Increments", INCREMENTS_HEADER, lines, failures):
            row = self._read_increment(number, cells, front_matter, failures)
            if row is not None:
                rows.append(row)
        return tuple(rows)

    def _read_increment(
        self, number: int, cells: tuple[str, ...], front_matter: FrontMatter, failures: list[Failure]
    ) -> IncrementRow | None:
        row_id, name, kind, touches, depends_on, order, decided_by, published = cells
        before = len(failures)
        if not ROW_ID.fullmatch(row_id):
            failures.append(_failure(number, f"ID `{row_id}` isn't `I<n>`"))
        if not re.fullmatch(r"\S.*?: \S.*", name):
            failures.append(_failure(number, f"Increment `{name}` isn't `<name>: <one-line intent>`"))
        touches_list = _list(touches)
        if any(not entry for entry in touches_list):
            failures.append(_failure(number, f"Touches `{touches}` has an empty entry"))
        depends_list = _list(depends_on)
        for entry in depends_list:
            if not DEPENDENCY.fullmatch(entry):
                failures.append(_failure(number, f"Depends on entry `{entry}` isn't `I<n>` or `<map>:I<n>`"))
        if not POSITIVE_INT.fullmatch(order):
            failures.append(_failure(number, f"Order `{order}` isn't a positive integer"))
        decided_list = _list(decided_by)
        for entry in decided_list:
            if not re.fullmatch(r"scratch:\S+", entry):
                failures.append(_failure(number, f"Decided by entry `{entry}` isn't a `scratch:` ref"))
        match = PUBLISHED.fullmatch(published)
        if not match:
            failures.append(_failure(number, f"Published `{published}` isn't `r<N>` or `r<N>, withdrawn r<M>`"))
        else:
            published_in = int(match.group(1))
            withdrawn_in = int(match.group(2)) if match.group(2) else None
            revision = front_matter.revision
            if published_in > revision or (withdrawn_in is not None and not published_in < withdrawn_in <= revision):
                failures.append(_failure(number, f"Published `{published}` doesn't fit revision {revision}"))
        if len(failures) > before:
            return None
        return IncrementRow(
            row_id, name, kind, touches_list, depends_list, int(order), decided_list,
            published_in, withdrawn_in, number,
        )

    def _read_rules(self, lines: list[tuple[int, str]], failures: list[Failure]) -> int:
        limits: list[int] = []
        for number, line in lines:
            if not line.strip():
                continue
            if not RULES_LINE.fullmatch(line):
                failures.append(_failure(number, f"`{line}` isn't `- Rule: …` or `- Assumption: …`"))
                continue
            match = INTEGRATION_RULE.fullmatch(line)
            if match:
                limits.append(int(match.group(1)))
        if len(limits) != 1:
            failures.append(_failure(
                "Rules and planning assumptions",
                "exactly one integration rule `- Rule: at most <n> changed services …` is required",
            ))
            return 0
        return limits[0]
