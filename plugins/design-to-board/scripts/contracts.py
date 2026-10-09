"""Contracts between design-to-board's layers: the read design document and the failure report."""

from __future__ import annotations

from dataclasses import dataclass

FORMAT = "wayfinder-design/1"
SECTIONS = (
    "Destination",
    "Decisions",
    "Services",
    "Increments",
    "Rules and planning assumptions",
)
LAYERS = ("Manager", "Engine", "ResourceAccess", "Client", "Utility")

EXIT_VALID = 0
EXIT_FAILED_NOTHING_WRITTEN = 1


@dataclass(frozen=True, slots=True)
class FrontMatter:
    format: str
    map: str
    status: str
    revision: int
    changed: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Service:
    name: str
    layer: str
    encapsulates: str
    introduced_in: str | None
    line: int


@dataclass(frozen=True, slots=True)
class IncrementRow:
    id: str
    name: str
    kind: str
    touches: tuple[str, ...]
    depends_on: tuple[str, ...]
    order: int
    decided_by: tuple[str, ...]
    published_in: int
    withdrawn_in: int | None
    line: int

    @property
    def number(self) -> int:
        return int(self.id[1:])

    @property
    def live(self) -> bool:
        return self.withdrawn_in is None

    @property
    def same_map_depends_on(self) -> tuple[str, ...]:
        """`Depends on` entries in this map; `<map>:<ID>` entries are board checks, not document checks."""
        return tuple(d for d in self.depends_on if ":" not in d)


@dataclass(frozen=True, slots=True)
class DesignDocument:
    front_matter: FrontMatter
    behaviours: tuple[str, ...]
    services: tuple[Service, ...]
    increments: tuple[IncrementRow, ...]
    max_changed_services: int


@dataclass(frozen=True, slots=True)
class Failure:
    """One report line: `check · row · reason · fix`."""

    check: str
    row: str
    reason: str
    fix: str

    def line(self) -> str:
        return f"{self.check} · {self.row} · {self.reason} · {self.fix}"


@dataclass(frozen=True, slots=True)
class ValidationResult:
    document: DesignDocument | None
    failures: tuple[Failure, ...]

    @property
    def valid(self) -> bool:
        return not self.failures
