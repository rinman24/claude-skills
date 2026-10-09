# Lessons learned

Append-only. One entry per lesson: what happened, and how to apply it next
time. Newest at the bottom.

The wayfinder port's lessons (`docs/wayfinder-port/LESSONS-LEARNED.md`)
still apply; the ones that matter most here: push command (S1), merge
`origin/main` rather than rebasing a pushed branch (S1), absolute paths and
no `cd` into another repo (S6/S7), "read the consumer, not only the config"
(Q3), continue the same advisor agent with SendMessage (S8), `/ask-juval`
is typed by Rich (Q3), and the headless-check recipe (S14, S15).

## S0 · 2026-10-09

- **squadra has no create path.** Its `BoardAccess` only reads, moves state,
  tags and comments, and only ADO is wired. Apply: don't assume "publish to
  the board" means "call squadra"; DBQ1 decides where board writes live.
