# Domain Docs

How the skills should consume this repo's domain documentation before exploring or writing.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root: the glossary (single context, no `CONTEXT-MAP.md`).
- **`docs/adr/`**: read ADRs that touch the area you're about to work in (plugin granularity, naming, description policy, model selection).

If any of these files are empty, **proceed silently**. Terms and decisions are added when they actually get resolved.

## File structure

```
/
├── CONTEXT.md
├── docs/adr/
│   └── NNNN-<slug>.md
└── skills/<plugin-name>/
```

## Use the glossary's vocabulary

When your output names a project concept (in a ticket title, a skill description, an ADR), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (define it in `CONTEXT.md` first, then use it).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0001 (one plugin per model family), but worth reopening because…_
