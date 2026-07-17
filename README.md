# Design Lab Prompts Skill

[![CI](https://github.com/niceShare/design-lab-prompts-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/niceShare/design-lab-prompts-skill/actions/workflows/ci.yml)
[![License: MIT (code)](https://img.shields.io/badge/code%20license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![Source snapshot](https://img.shields.io/badge/source%20snapshot-2026--07--16-orange.svg)](ATTRIBUTION.md)

[简体中文](README.zh-CN.md)

An offline Codex skill and zero-dependency CLI for exploring, comparing, and applying 77 frontend visual styles from the public [Design Lab](https://design-lab-yanliu.vercel.app/) collection.

The repository turns a source snapshot into a structured catalog, searchable prompt books, a project-type recommender, and implementation-ready skill workflows. It includes 174 Chinese prompt entries, 144 English prompt entries, and 144 curated recommendation records.

> [!IMPORTANT]
> This is an **unofficial, independent open-source learning project** that references the public Design Lab website, credited there as “Curated by Dreameryanyan.” It is not affiliated with, sponsored by, or endorsed by Design Lab or its curator. Original repository code and documentation are MIT-licensed. Upstream-derived prompts, descriptions, and metadata are excluded from that license and are bundled solely for study, research, design analysis, and non-commercial exchange. See [Attribution](ATTRIBUTION.md) and [Notice](NOTICE.md) before reusing or redistributing the dataset.

## What it provides

- An installable Codex skill with progressive reference loading.
- A standard-library-only Python CLI for listing, searching, copying, and recommending styles.
- 77 normalized style records with descriptions, characteristics, palettes, CSS, prompts, do rules, and don't rules.
- Original Chinese coverage for all 77 styles and source-provided English coverage for 67 styles.
- The source site's 12-category, four-level recommendation matrix.
- Deterministic Markdown generation, file hashes, snapshot integrity tests, and four end-to-end examples.
- A non-evaluating data-literal parser for maintainers refreshing the source snapshot.

## Quick start

### Install the Codex skill

```bash
git clone https://github.com/niceShare/design-lab-prompts-skill.git
cd design-lab-prompts-skill
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skill/design-lab-prompts "${CODEX_HOME:-$HOME/.codex}/skills/design-lab-prompts"
```

Start a new Codex task and invoke the skill:

```text
$design-lab-prompts Recommend three visual directions for an AI developer dashboard at creativity level 3/4, then compose an implementation-ready prompt.
```

### Use the CLI directly

Python 3.10 or later is required. No third-party Python packages are used.

```bash
cd skill/design-lab-prompts

python3 scripts/query_prompts.py stats
python3 scripts/query_prompts.py list --lang en --filter trend
python3 scripts/query_prompts.py show glass --lang en
python3 scripts/query_prompts.py search "warm editorial SaaS" --lang all --limit 5
python3 scripts/query_prompts.py prompt luxury --lang zh --kind advanced
python3 scripts/query_prompts.py recommend "AI developer dashboard" --lang en --level 3
```

Add `--json` to `stats`, `show`, `search`, `prompt`, or `recommend` when another tool will consume the result.

## Example workflows

### Recommend styles for a project

```bash
python3 scripts/query_prompts.py recommend \
  "API debugging dashboard for developers" \
  --lang en \
  --level 3 \
  --json
```

The recommender first uses Design Lab's curated project-category matrix. When no category matches, it falls back to weighted catalog search.

### Retrieve an exact source prompt

```bash
python3 scripts/query_prompts.py prompt terminal --lang en --kind basic
```

The skill keeps retrieved source wording separate from project-specific requirements during planning. Generated websites and apps contain only the requested product interface; provenance remains in repository documentation or external delivery notes rather than visible UI.

### Handle missing translations

```bash
python3 scripts/query_prompts.py prompt editorialsaas --lang en --kind basic
```

Ten recently added styles are Chinese-only in the captured source. The CLI reports the fallback and returns the Chinese original instead of inventing a translation.

See [examples/cases.md](examples/cases.md) for complete AI dashboard, luxury commerce, editorial SaaS, and beauty campaign cases.

## Snapshot coverage

| Field | Count |
|---|---:|
| Styles | 77 |
| Bilingual styles | 67 |
| Chinese-only styles | 10 |
| Chinese prompt entries | 174 |
| English prompt entries | 144 |
| Recommendation categories | 12 |
| Creativity levels | 4 |
| Recommendation records | 144 |

The canonical snapshot is [`catalog.json`](skill/design-lab-prompts/references/catalog.json). Its source length and SHA-256 digest are recorded in the catalog and [`manifest.json`](skill/design-lab-prompts/references/manifest.json). For the collection analysis and coverage decisions, read [research/analysis.md](research/analysis.md).

## Repository layout

```text
skill/design-lab-prompts/
  SKILL.md                    Codex workflow and attribution rules
  agents/openai.yaml          Skill UI metadata
  scripts/query_prompts.py    Zero-dependency catalog CLI
  references/catalog.json     Canonical normalized snapshot
  references/style-index.md   Compact style inventory
  references/prompts-zh.md    Chinese source prompt book
  references/prompts-en.md    English source prompt book
  references/source-notes.md  Provenance and known gaps
  references/manifest.json    Version, counts, hashes, and sizes
examples/cases.md             Four end-to-end usage examples
research/analysis.md          Collection and prompt-system analysis
tools/                        Safe extraction and deterministic generation
tests/test_catalog.py         Integrity, security, documentation, and CLI tests
```

## Development

Requirements:

- Python 3.10+
- Node.js 20+ for extractor validation and snapshot maintenance

Run the complete local verification suite:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q skill tools tests
node --check tools/extract_site_data.mjs
python3 tools/build_reference_files.py \
  skill/design-lab-prompts/references/catalog.json \
  skill/design-lab-prompts
git diff --exit-code
```

The generator validates internal catalog consistency and produces deterministic references. Snapshot-specific counts remain pinned in the tests, so upstream changes require an intentional test review.

### Refreshing the source snapshot

Save the rendered page's complete inline script as a `.js` file, or save a JSON array of `{ "text": "..." }` script records. Then run:

```bash
node tools/extract_site_data.mjs \
  path/to/site-inline.js \
  work/catalog.json \
  --captured-at 2026-07-16T17:29:57+08:00

python3 tools/build_reference_files.py work/catalog.json skill/design-lab-prompts
python3 -m unittest discover -s tests -v
```

The extractor accepts data literals only. It does not execute code from the captured page and rejects functions, calls, computed expressions, and template interpolation. Marker names are still coupled to the current upstream page structure; review extraction failures instead of weakening the parser.

## Provenance and license boundary

This is a mixed-rights repository:

- Original tooling and original project documentation: [MIT License](LICENSE).
- Source-derived prompts, style descriptions, recommendations, and metadata: not covered by the MIT License.
- Upstream reference: [Design Lab](https://design-lab-yanliu.vercel.app/), credited on the source site as “Curated by Dreameryanyan.”
- Project status: unofficial and independent; no affiliation or endorsement is claimed.

The upstream-content snapshot does not grant commercial redistribution, resale, sublicensing, or derivative-dataset rights. Confirm permission with the relevant rights holder before public or commercial reuse. Read [ATTRIBUTION.md](ATTRIBUTION.md) and [NOTICE.md](NOTICE.md) for the full bilingual statement.

## Project status and limitations

- The catalog is a point-in-time snapshot captured on 2026-07-16; it does not update automatically.
- Ten styles have no source-provided English prompts.
- Search and category detection are deterministic heuristics, not semantic embeddings.
- Visual prompts are design direction, not a substitute for accessibility, information architecture, or device testing.
- The extraction workflow intentionally avoids network fetching and executable page code.

## Contributing and security

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Please report vulnerabilities privately as described in [SECURITY.md](SECURITY.md). The current internal review and remediation record is documented in [AUDIT.md](AUDIT.md).

## Acknowledgements

This project references the public [Design Lab / Design Style Laboratory](https://design-lab-yanliu.vercel.app/) collection, credited on the source site as “Curated by Dreameryanyan.” The structured CLI, skill workflow, validation, and repository documentation are independent community work.
