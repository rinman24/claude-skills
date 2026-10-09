from collections.abc import Callable
from pathlib import Path

import pytest

from contracts import ValidationResult

# default_document_text, make_document, validate
# are provided by tests/conftest.py

I1_KIND = "| foundation → I2, I3 |"
I3_TOUCHES = "| InvoiceAccess, PortalClient |"
I3_DEPENDS = "PortalClient | I1 | 3 |"
I4_ROW = "| I4 | Raise on delivery"
I4_ORDER = "OrderAccess | I1 | 2 | scratch:wayfinder/billing/03-invoice-trigger.md | r2 |"
STATUS = "status: cleared"


def _checks(result: ValidationResult) -> set[str]:
    return {failure.check for failure in result.failures}


def test_valid_document_passes(make_document, validate) -> None:
    result = validate(make_document())

    assert result.valid
    assert [row.id for row in result.document.increments if row.live] == ["I1", "I3", "I4"]


# One failing document per check: each edit breaks that check and no other.
FAILING = {
    "check 6, unknown format": (("format: wayfinder-design/1", "format: wayfinder-design/2"),),
    "check 6, revising": ((STATUS, "status: revising"),),
    "check 7, duplicate ID": ((I4_ROW, "| I3 | Raise on delivery"),),
    "check 7, missing row": ((I4_ROW, "| I5 | Raise on delivery"),),
    "check 8": ((I3_TOUCHES, "| InvoiceAccess, MobileClient |"),),
    "check 9": (("| how an invoice is raised | I1 |", "| how an invoice is raised | I4 |"),),
    "check 10": ((I3_TOUCHES, "| OrderAccess, PortalClient |"),),
    "check 11": (("at most 2 changed services", "at most 1 changed services"),),
    "check 12": (("| vertical (B2) |", "| foundation → I4 |"),),
    "check 13": ((I4_ORDER, I4_ORDER.replace("| I1 | 2 |", "| I1 | 1 |")),),
    "check 14": ((I3_DEPENDS, "PortalClient | I1, I2 | 3 |"),),
    "check 15 (malformed Kind), form": (("| vertical (B2) |", "| vertical B2 |"),),
    "check 15 (malformed Kind), unknown behaviour": (("| vertical (B2) |", "| vertical (B9) |"),),
    "check 15 (malformed Kind), unknown row": ((I1_KIND, "| foundation → I2, I3, I9 |"),),
    "check 15 (malformed Kind), cross-map foundation": ((I1_KIND, "| foundation → I2, billing:I3 |"),),
}


@pytest.mark.parametrize("case", FAILING)
def test_each_check_fails_alone(case: str, make_document, validate) -> None:
    result = validate(make_document(*FAILING[case]))

    assert _checks(result) == {case.split(",")[0]}


def test_withdrawn_row_may_name_a_behaviour_no_longer_in_destination(make_document, validate) -> None:
    result = validate(make_document(("| vertical (B1) | InvoiceManager, OrderAccess | I1 | 2 | scratch:wayfinder/billing/03-invoice-trigger.md | r1, withdrawn r2 |",
                                     "| vertical (B7) | InvoiceManager, OrderAccess | I1 | 2 | scratch:wayfinder/billing/03-invoice-trigger.md | r1, withdrawn r2 |")))

    assert result.valid


def test_cross_map_dependency_is_left_to_the_board_checks(make_document, validate) -> None:
    result = validate(make_document((I3_DEPENDS, "PortalClient | I1, shipping:I2 | 3 |")))

    assert result.valid


def test_dependency_on_a_row_not_in_the_table_fails_check_7(make_document, validate) -> None:
    result = validate(make_document((I3_DEPENDS, "PortalClient | I1, I9 | 3 |")))

    assert [(f.check, f.row) for f in result.failures] == [("check 7", "I3")]


def test_several_defects_are_all_reported_in_check_order(make_document, validate) -> None:
    result = validate(make_document(
        (I3_DEPENDS, "PortalClient | I1, I2 | 3 |"),
        (I3_TOUCHES, "| InvoiceAccess, MobileClient |"),
        (I4_ORDER, I4_ORDER.replace("| I1 | 2 |", "| I1 | 1 |")),
        ("| vertical (B2) |", "| vertical (B9) |"),
    ))

    assert [(f.check, f.row) for f in result.failures] == [
        ("check 8", "I3"),
        ("check 13", "I4"),
        ("check 14", "I3"),
        ("check 15 (malformed Kind)", "I3"),
    ]


def test_check_6_stops_before_the_body_is_read(make_document, validate) -> None:
    result = validate(make_document((STATUS, "status: revising"), ("## Services", "## Servicez")))

    assert _checks(result) == {"check 6"}


def test_fix_routes_document_defects_to_wayfinder(make_document, validate) -> None:
    missed = validate(make_document((I3_TOUCHES, "| InvoiceAccess, MobileClient |"))).failures[0]
    new_check = validate(make_document((I3_DEPENDS, "PortalClient | I1, I2 | 3 |"))).failures[0]

    assert missed.fix == "revise the map in wayfinder and Publish again (wayfinder's Publish checks missed this)"
    assert new_check.fix == "revise the map in wayfinder and Publish again"
