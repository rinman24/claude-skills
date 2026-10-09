import pytest

# make_document, validate
# are provided by tests/conftest.py

# Each edit takes the document outside DESIGN-FORMAT's grammar.
GRAMMAR = {
    "no front matter": (("---\nformat", "format"),),
    "unknown front matter key": (("revision: 2", "revision: 2\nowner: rich"),),
    "missing front matter key": (("changed: [Increments]\n", ""),),
    "unknown status": (("status: cleared", "status: done"),),
    "changed names an unknown section": (("changed: [Increments]", "changed: [Tickets]"),),
    "changed on revision 1": (("revision: 2", "revision: 1"), ("| r1, withdrawn r2 |", "| r1 |"), ("| r2 |", "| r1 |")),
    "missing section": (("## Decisions", "## Notes"),),
    "sections out of order": (("## Services", "## Rulez"),),
    "text outside a section": (("# Billing", "# Billing\nstray text"),),
    "bad behaviour line": (("- B2: A customer", "- Behaviour 2: A customer"),),
    "unknown column": (("| ID | Increment | Kind |", "| ID | Increment | Type |"),),
    "row with too few cells": (("PortalClient | Client | | |", "PortalClient | Client | |"),),
    "unknown layer": (("| OrderAccess | ResourceAccess |", "| OrderAccess | Repository |"),),
    "new service without Encapsulates": (("| where invoices are stored | I1 |", "| | I1 |"),),
    "bad row ID": (("| I3 | Invoice list", "| 3 | Invoice list"),),
    "increment without intent": (("| Invoice list: customers list their invoices |", "| Invoice list |"),),
    "bad Depends on entry": (("PortalClient | I1 | 3 |", "PortalClient | step 1 | 3 |"),),
    "bad Order": (("PortalClient | I1 | 3 |", "PortalClient | I1 | third |"),),
    "Decided by not a scratch ref": (("| 3 | scratch:wayfinder/billing/04-portal.md |", "| 3 | 04-portal.md |"),),
    "blank Published": (("| scratch:wayfinder/billing/04-portal.md | r1 |", "| scratch:wayfinder/billing/04-portal.md | |"),),
    "Published after the revision": (("| scratch:wayfinder/billing/04-portal.md | r1 |", "| scratch:wayfinder/billing/04-portal.md | r3 |"),),
    "no integration rule": (("- Rule: at most 2 changed services (new or modified) per increment.\n", ""),),
    "rules line that is neither": (("- Assumption: at most 2", "- at most 2"),),
}


@pytest.mark.parametrize("case", GRAMMAR)
def test_reader_rejects_anything_outside_the_grammar(case: str, make_document, validate) -> None:
    result = validate(make_document(*GRAMMAR[case]))

    assert result.failures
    assert {failure.check for failure in result.failures} == {"grammar"}


def test_grammar_failures_are_all_collected(make_document, validate) -> None:
    result = validate(make_document(*GRAMMAR["unknown layer"], *GRAMMAR["bad Order"], *GRAMMAR["blank Published"]))

    assert [f.row for f in result.failures] == ["line 29", "line 38", "line 38"]
