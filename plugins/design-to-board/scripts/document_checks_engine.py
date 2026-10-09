"""DESIGN-FORMAT's translator checks 6–15 on a read document. Pure; every failure is collected (DB-D6).

Checks 7–14 judge live rows, except where a check is about withdrawn rows.
Same-map `Depends on` edges only: a `<map>:<ID>` predecessor is a board check.
"Depends on" is the transitive relation: a row depends on every row it can
reach through `Depends on` edges.
"""

from __future__ import annotations

import re

from contracts import FORMAT, DesignDocument, Failure, FrontMatter, IncrementRow

MISSED_BY_PUBLISH = "wayfinder's Publish checks missed this"
VERTICAL = re.compile(r"vertical \((B[1-9]\d*)\)")
FOUNDATION = re.compile(r"foundation → (I[1-9]\d*(?:, I[1-9]\d*)*)")


def _fix(check: int) -> str:
    fix = "revise the map in wayfinder and Publish again"
    return f"{fix} ({MISSED_BY_PUBLISH})" if check <= 13 else fix


def _failure(check: int, row: str, reason: str, name: str | None = None) -> Failure:
    label = f"check {check}" + (f" ({name})" if name else "")
    return Failure(label, row, reason, _fix(check))


class DocumentChecksEngine:
    def check_front_matter(self, front_matter: FrontMatter) -> list[Failure]:
        """Check 6: `format` is known and `status` is `cleared`."""
        failures = []
        if front_matter.format != FORMAT:
            failures.append(_failure(6, "front matter", f"format `{front_matter.format}` is unknown; expected `{FORMAT}`"))
        if front_matter.status != "cleared":
            failures.append(_failure(6, "front matter", f"status is `{front_matter.status}`, not `cleared`"))
        return failures

    def check_document(self, document: DesignDocument) -> list[Failure]:
        """Checks 7–15, in check order, rows in table order."""
        rows = {row.id: row for row in document.increments}
        live = [row for row in document.increments if row.live]
        reach = _reachability(rows)
        failures: list[Failure] = []
        failures += self._check_7(document.increments)
        failures += self._check_8(document, live)
        failures += self._check_9(document, rows, live, reach)
        failures += self._check_10(live, reach)
        failures += self._check_11(document, live)
        failures += self._check_12(rows, live, reach)
        failures += self._check_13(rows, live)
        failures += self._check_14(rows, live)
        failures += self._check_15(document, rows)
        return failures

    def _check_7(self, increments: tuple[IncrementRow, ...]) -> list[Failure]:
        failures: list[Failure] = []
        seen: set[str] = set()
        for row in increments:
            if row.id in seen:
                failures.append(_failure(7, row.id, f"ID {row.id} appears more than once"))
            seen.add(row.id)
        numbers = {row.number for row in increments}
        for number in range(1, max(numbers, default=0) + 1):
            if number not in numbers:
                failures.append(_failure(7, f"I{number}", f"I{number} is missing; a withdrawn row stays in the table"))
        for row in increments:
            for target in row.same_map_depends_on:
                if target not in seen:
                    failures.append(_failure(7, row.id, f"Depends on names {target}, which isn't in the table"))
        return failures

    def _check_8(self, document: DesignDocument, live: list[IncrementRow]) -> list[Failure]:
        declared = {service.name for service in document.services}
        return [
            _failure(8, row.id, f"Touches names `{name}`, which Services doesn't declare")
            for row in live
            for name in row.touches
            if name not in declared
        ]

    def _check_9(self, document, rows, live, reach) -> list[Failure]:
        failures: list[Failure] = []
        for service in document.services:
            introducer = service.introduced_in
            if introducer is None:
                continue
            row = rows.get(introducer)
            if row is None or not row.live or service.name not in row.touches:
                failures.append(_failure(
                    9, introducer,
                    f"`{service.name}` is Introduced in {introducer}, which isn't a live row touching it",
                ))
                continue
            for other in live:
                if other.id != introducer and service.name in other.touches and introducer not in reach[other.id]:
                    failures.append(_failure(
                        9, other.id,
                        f"touches new service `{service.name}` but doesn't depend on {introducer}, which introduces it",
                    ))
        return failures

    def _check_10(self, live, reach) -> list[Failure]:
        failures: list[Failure] = []
        for i, first in enumerate(live):
            for second in live[i + 1:]:
                shared = sorted(set(first.touches) & set(second.touches))
                if shared and second.id not in reach[first.id] and first.id not in reach[second.id]:
                    failures.append(_failure(
                        10, f"{first.id}, {second.id}",
                        f"both touch `{shared[0]}` with no Depends on path between them",
                    ))
        return failures

    def _check_11(self, document: DesignDocument, live) -> list[Failure]:
        limit = document.max_changed_services
        return [
            _failure(11, row.id, f"touches {len(row.touches)} services; the rule allows at most {limit}")
            for row in live
            if len(row.touches) > limit
        ]

    def _check_12(self, rows, live, reach) -> list[Failure]:
        failures: list[Failure] = []
        for row in live:
            match = FOUNDATION.fullmatch(row.kind)
            if not match:
                continue
            for target in match.group(1).split(", "):
                named = rows.get(target)
                if named is not None and named.live and row.id not in reach[target]:
                    failures.append(_failure(12, row.id, f"is a foundation for {target}, which doesn't depend on it"))
        return failures

    def _check_13(self, rows, live) -> list[Failure]:
        failures: list[Failure] = []
        for row in live:
            for target in row.same_map_depends_on:
                dependency = rows.get(target)
                if dependency is not None and dependency.live and dependency.order >= row.order:
                    failures.append(_failure(
                        13, row.id,
                        f"Order {row.order} isn't after {target}'s Order {dependency.order}, which it depends on",
                    ))
        return failures

    def _check_14(self, rows, live) -> list[Failure]:
        return [
            _failure(14, row.id, f"depends on {target}, which is withdrawn")
            for row in live
            for target in row.same_map_depends_on
            if target in rows and not rows[target].live
        ]

    def _check_15(self, document: DesignDocument, rows) -> list[Failure]:
        """Every row's Kind; a withdrawn row's behaviour may have left Destination since it was published."""
        failures: list[Failure] = []
        for row in document.increments:
            kind = row.kind
            if not kind:
                continue
            vertical = VERTICAL.fullmatch(kind)
            foundation = FOUNDATION.fullmatch(kind)
            if vertical:
                if row.live and vertical.group(1) not in document.behaviours:
                    reason = f"`{kind}`: unknown behaviour {vertical.group(1)}; Destination doesn't list it"
                    failures.append(_failure(15, row.id, reason, "malformed Kind"))
            elif foundation:
                for target in foundation.group(1).split(", "):
                    if target not in rows:
                        reason = f"`{kind}`: unknown row {target}; the table doesn't list it"
                        failures.append(_failure(15, row.id, reason, "malformed Kind"))
            else:
                reason = f"`{kind}`: form isn't blank, `vertical (B<n>)` or `foundation → I<n>, …`"
                failures.append(_failure(15, row.id, reason, "malformed Kind"))
        return failures


def _reachability(rows: dict[str, IncrementRow]) -> dict[str, set[str]]:
    """For each row, every row it reaches through same-map `Depends on` edges."""
    reach: dict[str, set[str]] = {}
    for start in rows:
        seen: set[str] = set()
        stack = list(rows[start].same_map_depends_on)
        while stack:
            target = stack.pop()
            if target in seen or target not in rows:
                continue
            seen.add(target)
            stack.extend(rows[target].same_map_depends_on)
        reach[start] = seen
    return reach
