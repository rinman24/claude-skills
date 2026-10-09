---
format: wayfinder-design/1
map: billing
status: cleared
revision: 2
changed: [Increments]
---

# Billing

## Destination

Invoices go out on delivery, and customers can see them.

- B1: A delivered order produces an invoice
- B2: A customer can list their invoices

## Decisions

- An invoice is raised on delivery, not on order (scratch:wayfinder/billing/03-invoice-trigger.md)
- Customers read invoices through the portal (scratch:wayfinder/billing/04-portal.md)

## Services

| Service | Layer | Encapsulates | Introduced in |
|---------|-------|--------------|---------------|
| InvoiceManager | Manager | how an invoice is raised | I1 |
| InvoiceAccess | ResourceAccess | where invoices are stored | I1 |
| OrderAccess | ResourceAccess | | |
| PortalClient | Client | | |

## Increments

| ID | Increment | Kind | Touches | Depends on | Order | Decided by | Published |
|----|-----------|------|---------|------------|-------|------------|-----------|
| I1 | Invoice store: invoices can be saved and read | foundation → I2, I3 | InvoiceManager, InvoiceAccess | | 1 | scratch:wayfinder/billing/03-invoice-trigger.md | r1 |
| I2 | Raise on order: an order raises an invoice | vertical (B1) | InvoiceManager, OrderAccess | I1 | 2 | scratch:wayfinder/billing/03-invoice-trigger.md | r1, withdrawn r2 |
| I3 | Invoice list: customers list their invoices | vertical (B2) | InvoiceAccess, PortalClient | I1 | 3 | scratch:wayfinder/billing/04-portal.md | r1 |
| I4 | Raise on delivery: a delivery raises an invoice | vertical (B1) | InvoiceManager, OrderAccess | I1 | 2 | scratch:wayfinder/billing/03-invoice-trigger.md | r2 |

## Rules and planning assumptions

- Rule: at most 2 changed services (new or modified) per increment.
- Assumption: at most 2 concurrent runners, one reviewer.
