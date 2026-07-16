# Internal Code Audit

Audit date: 2026-07-16
Reviewed version: 0.2.0 candidate
Scope: extractor, catalog generator, CLI, tests, generated references, licensing boundary, and public repository hygiene

## Executive summary

The review found one high-impact trust-boundary issue, one medium maintainability issue, two low correctness and reliability issues, and several open-source readiness gaps. The implementation changes documented below are covered by focused tests and the repository's full verification workflow.

## Findings

### DLPS-001 — Captured page literals were executed

Severity: High
Status: Remediated

The extractor previously used Node's `vm` module to evaluate JavaScript literals taken from a captured remote page. A VM context is not a security boundary for hostile input, and the maintenance workflow should never require executing source-page code.

Remediation:

- Replaced evaluation with a dependency-free parser for a restricted data-literal grammar.
- Required the expected literal to begin immediately after each known marker.
- Rejected functions, calls, unsupported identifiers, computed expressions, sparse arrays, duplicate object keys, and template interpolation.
- Added fixtures proving plain literals are accepted while executable expressions and interpolation are rejected.

### DLPS-002 — Snapshot validation was tied to one fixed dataset

Severity: Medium
Status: Remediated

The reference generator hard-coded 77 styles, language totals, four levels, three results per level, and 144 recommendation records. That protected the current snapshot but made the documented refresh workflow fail whenever the upstream collection legitimately changed.

Remediation:

- Validation now recomputes statistics from catalog contents and checks internal consistency.
- Provenance metadata, capture digest, style structure, palettes, translation status, and localized fields are validated before generation.
- Recommender categories and levels are validated against their metadata.
- Recommendation totals and translation counts are generated dynamically.
- Snapshot-specific expectations remain pinned in the test suite, where a source update can be reviewed explicitly.

### DLPS-003 — Short aliases matched inside unrelated words

Severity: Low
Status: Remediated

Category detection used substring matching for all aliases. The short alias `ai` therefore matched the word `retail` and could select the AI/tech category instead of e-commerce.

Remediation:

- Latin aliases now use token boundaries.
- CJK aliases retain substring matching.
- Added a focused retail classification test and retained the AI dashboard test.
- Localized the catalog-search fallback reason to the requested output language.

### DLPS-004 — Script selection and marker discovery were ambiguous

Severity: Low
Status: Remediated

For JSON captures, the extractor selected the longest script even when a shorter script contained the catalog. Marker discovery also used an unrestricted substring search, so marker-shaped text inside comments could be mistaken for a real assignment. English metadata IDs were checked only in the prompt map, leaving a second orphan path unchecked.

Remediation:

- JSON capture selection now requires the complete set of catalog markers and then chooses the longest matching script.
- Marker discovery skips quoted strings and comments and requires a statement boundary.
- Orphan checks cover both English metadata maps.
- Added focused fixtures for multi-script captures, comment decoys, and orphan metadata.

### DLPS-005 — Public repository onboarding was incomplete

Severity: Low
Status: Remediated

The original README read as a private handoff, and the repository lacked contribution guidance, a security-reporting path, continuous integration, and a durable audit record.

Remediation:

- Replaced the root README with a public English landing page and added a Chinese edition.
- Added contribution and security policies.
- Added GitHub Actions checks for supported Python versions, Node syntax, tests, and deterministic generation.
- Clarified the boundary between MIT-licensed original code and source-derived content.

## Residual risks and limitations

- The extractor depends on upstream marker names and will require a reviewed change if the source page structure changes.
- The project does not automatically fetch the source website; maintainers must provide a complete local capture.
- SHA-256 entries detect drift but do not authenticate the upstream publisher.
- Rights to upstream-derived prompts and metadata are not granted by this repository's MIT License. See [NOTICE.md](NOTICE.md).
- Heuristic search and recommendation are deterministic but not semantic models.

## Verification workflow

The repository defines these release checks:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q skill tools tests
node --check tools/extract_site_data.mjs
python3 tools/build_reference_files.py \
  skill/design-lab-prompts/references/catalog.json \
  skill/design-lab-prompts
git diff --exit-code
git diff --check
```

CI runs the test suite across the declared Python support range and separately checks deterministic generation. A release should not be tagged or pushed with failing checks.
