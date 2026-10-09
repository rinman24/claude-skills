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

## S1 · 2026-10-09

- **An advisor who proposes names needs Eric before the ruling is final.**
  Juval's structure was right, but his verb `publish_increment` collided with
  wayfinder's settled Publish/`Published`, and his cascade placement would
  have had the translator invent IDs. Apply: when Juval's answer introduces
  verbs, states or identities, route the vocabulary through `/ask-eric`
  before recording the decision.
- **Two advisor consultations cost about 60K of a session.** Each answer is
  relayed verbatim and written verbatim to its session file, so it lands in
  context twice (~25–30K each). Apply: plan at most one consultation per
  session alongside other rulings, or a session that is only consultations.
- **One ruling can settle several questions.** DB-D1 answered most of DBQ2
  and DBQ4 and half of DBQ3. Apply: after each ruling, re-annotate the open
  questions before asking the next one, so Rich rules only what is left.
