# ADR Format (default convention)

Use this only when the repo has no ADR convention of its own (see "Follow the repo's convention" in [SKILL.md](./SKILL.md)).

## Location and numbering

ADRs live in `docs/adr/` with sequential numbering: `0001-slug.md`, `0002-slug.md`, and so on. The slug is the title in lowercase kebab-case.

Create `docs/adr/` lazily: only when the first ADR is written. To number a new one, scan `docs/adr/` for the highest existing number and add one.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording _that_ a decision was made and _why_, not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`): useful when decisions are revisited.
- **Considered Options**: only when the rejected alternatives are worth remembering.
- **Consequences**: only when non-obvious downstream effects need to be called out.

## Superseding

When a new ADR reverses an earlier one, say so in its paragraph ("Supersedes ADR-0003."). If the earlier ADR has `Status` frontmatter, set it to `superseded by ADR-NNNN`; otherwise leave the earlier file alone. Never delete an ADR.
