---
name: design-lab-prompts
description: Search, compare, recommend, and apply 77 curated frontend visual styles from the Design Lab prompt collection, including 174 Chinese and 144 English prompt entries, design tokens, CSS snippets, characteristics, and do/don't rules. Use when choosing a UI/web design direction, writing an implementation-ready vibe-coding prompt, comparing visual styles, extracting a named style such as Glassmorphism or Brutalism, or recommending styles for SaaS, portfolios, e-commerce, content, gaming, wellness, fintech, education, food, fashion, AI/tech, or culture projects.
---

# Design Lab Prompts

Use the local catalog to select a style, retrieve its original prompt, and turn it into a project-specific implementation brief without losing the source language.

## Workflow

1. Identify the project type, desired mood, light/dark preference, and acceptable visual risk from the request.
2. If the user names a style, inspect it directly. Otherwise run the recommender, then compare the top two or three candidates.
3. Retrieve the original basic, advanced, or keyword prompt for the selected style.
4. Keep the retrieved source prompt separate from project-specific additions in working notes. When implementing a website or app, do not render either the prompt or provenance labels as user-facing content.
5. Add a separate `Project-specific extension` containing content hierarchy, components, responsive behavior, accessibility, and technical constraints from the request.
6. Apply the catalog's colors, CSS, characteristics, do rules, and don't rules when implementing or reviewing the result.
7. Keep attribution in repository documentation or external delivery notes: retain `https://design-lab-yanliu.vercel.app/`, credit the source site as “Curated by Dreameryanyan,” and identify this skill project as unofficial.

Do not invent English translations for styles marked `zh-only`. The query tool explicitly falls back to Chinese for those ten styles.

## Query the catalog

Run commands from this skill directory:

```bash
python3 scripts/query_prompts.py stats
python3 scripts/query_prompts.py list --lang zh --filter trend
python3 scripts/query_prompts.py show glass --lang en
python3 scripts/query_prompts.py search "warm editorial SaaS" --lang all --limit 5
python3 scripts/query_prompts.py prompt luxury --lang zh --kind advanced
python3 scripts/query_prompts.py recommend "AI developer dashboard" --lang en --level 3
```

Use `--json` with `stats`, `show`, `search`, or `recommend` when another script will consume the result.

## Select references progressively

- Read [references/style-index.md](references/style-index.md) for a compact inventory and filter overview.
- Read [references/prompts-zh.md](references/prompts-zh.md) only when browsing the full Chinese prompt book.
- Read [references/prompts-en.md](references/prompts-en.md) only when browsing the full English prompt book.
- Read [references/catalog.json](references/catalog.json) for machine-readable metadata, exact CSS, design tokens, or recommendation mappings.
- Read [references/source-notes.md](references/source-notes.md) when reporting provenance, snapshot limits, translation coverage, or reuse rights.

Prefer `scripts/query_prompts.py` over loading the full catalog into context for ordinary lookups.

## Compose the final design prompt

Return these sections when the user asks for a reusable prompt:

1. `Selected style` — localized name, style ID, and one-sentence rationale.
2. `Source style instructions` — exact retrieved text.
3. `Project-specific extension` — concrete page structure, component states, responsive rules, motion, accessibility, and stack constraints.
4. `Design tokens` — the catalog palette and relevant CSS.
5. `Guardrails` — applicable do/don't rules.

When the user asks only to look up or copy a prompt, return the exact prompt without expanding it.
When the user asks to implement a website or app, use the prompt sections as internal planning material and deliver only the requested product interface.

## Keep provenance outside generated UI

Treat copied Design Lab prompts and metadata as upstream reference content, not as original project authorship. Never add source credit, attribution copy, unofficial-project disclaimers, or prompt labels to a generated website or app UI, including its footer, unless the user explicitly requests visible attribution. Put any required provenance in repository documentation or external delivery notes instead. Do not imply affiliation, endorsement, ownership, or a license to commercially redistribute the upstream dataset. The repository's MIT License covers original project code and original documentation only; consult the root `ATTRIBUTION.md` and `NOTICE.md` for the full statement.
