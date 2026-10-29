---
format: wayfinder-design/1
map: done4
status: cleared
revision: 3
changed: [Increments]
---

# Done4

## Destination

The CLI greets a user and remembers its greetings.

- B1: The CLI greets a user
- B2: A user can list past greetings

## Decisions

- Greetings are stored before any behaviour uses them (scratch:wayfinder/done4/03-store.md)
- The CLI is the only client (scratch:wayfinder/done4/04-cli.md)

## Services

| Service | Layer | Encapsulates | Introduced in |
|---------|-------|--------------|---------------|
| GreetingManager | Manager | how a greeting is composed | I1 |
| GreetingAccess | ResourceAccess | where greetings are stored | I1 |
| CliClient | Client | | |

## Increments

| ID | Increment | Kind | Touches | Depends on | Order | Decided by | Published |
|----|-----------|------|---------|------------|-------|------------|-----------|
| I1 | Greeting store: greetings can be saved and read | foundation → I2 | GreetingManager, GreetingAccess | | 1 | scratch:wayfinder/done4/03-store.md | r1 |
| I2 | Greet by name: the CLI greets a user by name | vertical (B1) | GreetingManager, CliClient | I1 | 2 | scratch:wayfinder/done4/04-cli.md | r1, withdrawn r2 |
| I3 | Greeting history: the CLI lists past greetings | vertical (B2) | GreetingAccess, CliClient | I2 | 3 | scratch:wayfinder/done4/04-cli.md | r1, withdrawn r2 |
| I4 | Greet by nickname: the CLI greets a user by nickname | vertical (B1) | GreetingManager, CliClient | I1 | 2 | scratch:wayfinder/done4/04-cli.md | r2 |

## Rules and planning assumptions

- Rule: at most 2 changed services (new or modified) per increment.
- Assumption: at most 1 concurrent runner, one reviewer.
