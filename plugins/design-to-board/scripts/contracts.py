"""Contracts between design-to-board's layers: the read design document, the board snapshot, the plan and the failure report."""

from __future__ import annotations

from collections.abc import Mapping
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
# 2 is usage (argparse). Any stop once writing began: some writes may have landed, a re-run completes the rest.
EXIT_STOPPED_PARTWAY = 3

# squadra's Lifecycle buckets as `squadra board origins` spells them; ABSENT is an Origin no Increment carries.
ABSENT = "absent"
QUEUED = "queued"
ACTIVE = "active"
DONE = "done"
WITHDRAWN = "withdrawn"
LIFECYCLES = (ABSENT, QUEUED, ACTIVE, DONE, WITHDRAWN)


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
    front_matter: FrontMatter | None = None

    @property
    def valid(self) -> bool:
        return not self.failures


@dataclass(frozen=True, slots=True)
class Increment:
    """One entry of squadra's `increments_by_origin()`; claim scope is reported, never filtered."""

    item_id: int
    parent: int | None
    lifecycle: str
    in_claim_scope: bool


# `increments_by_origin()` as a value: every Origin an Increment carries on the board, partial items left out.
Snapshot = Mapping[str, Increment]


@dataclass(frozen=True, slots=True)
class WithdrawStep:
    origin: str


@dataclass(frozen=True, slots=True)
class QueueStep:
    """A `queue_increment` call; predecessors are named by Origin, never item ID."""

    origin: str
    predecessors: tuple[str, ...]
    title: str
    body: str


@dataclass(frozen=True, slots=True)
class Plan:
    """The reconcile's writes: withdrawals first (predecessors first), then queues in Kahn order."""

    map: str
    revision: int
    parent: int
    withdrawals: tuple[WithdrawStep, ...]
    queues: tuple[QueueStep, ...]


@dataclass(frozen=True, slots=True)
class ReconcileResult:
    plan: Plan | None
    failures: tuple[Failure, ...]


@dataclass(frozen=True, slots=True)
class Write:
    """One plan step squadra carried out: the item it wrote and, for a queue, the predecessors' item IDs."""

    step: WithdrawStep | QueueStep
    item_id: int
    predecessor_ids: tuple[int, ...] = ()


@dataclass(frozen=True, slots=True)
class TranscribeResult:
    """The reconcile, then the writes done; `stop` is the refusal that ended the walk, `remaining` the steps not done."""

    reconcile: ReconcileResult
    done: tuple[Write, ...] = ()
    stop: Failure | None = None
    remaining: tuple[WithdrawStep | QueueStep, ...] = ()


class BoardReadError(Exception):
    """`squadra board origins` didn't give a snapshot: not found (exit_code None), or squadra's exit code and stderr."""

    def __init__(self, exit_code: int | None, message: str) -> None:
        super().__init__(message)
        self.exit_code = exit_code
        self.message = message


class BoardWriteError(Exception):
    """`squadra board queue` or `withdraw` didn't write: not found (exit_code None), or squadra's exit code and stderr."""

    def __init__(self, exit_code: int | None, message: str) -> None:
        super().__init__(message)
        self.exit_code = exit_code
        self.message = message
