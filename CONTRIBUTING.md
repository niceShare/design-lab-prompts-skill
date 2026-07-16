# Contributing

Thank you for helping improve Design Lab Prompts Skill. Contributions to the original tooling, tests, documentation, and skill workflow are welcome.

This repository also contains source-derived reference data. Before changing that data, read [ATTRIBUTION.md](ATTRIBUTION.md) and [NOTICE.md](NOTICE.md). A contribution must not imply that upstream material is MIT-licensed or owned by this project.

## Development setup

Requirements:

- Python 3.10 or later
- Node.js 20 or later
- Git

Clone the repository and run the test suite:

```bash
git clone https://github.com/niceShare/design-lab-prompts-skill.git
cd design-lab-prompts-skill
python3 -m unittest discover -s tests -v
```

No third-party Python or Node packages are required.

## Types of contribution

- Fix CLI lookup, search, localization, or output behavior.
- Improve catalog validation and deterministic generation.
- Harden the extraction boundary without allowing captured code execution.
- Improve the Codex skill workflow or add a clearly documented case.
- Correct original project documentation.
- Report a source attribution, provenance, or removal concern.

For changes to copied upstream wording, open an issue first. Do not silently rewrite a source prompt or add a machine translation as though it came from Design Lab.

## Updating the source snapshot

Snapshot changes must be intentional and reviewable.

1. Capture the complete rendered inline script from the public source page.
2. Record the real capture time with `--captured-at`.
3. Run the safe extractor. Do not replace it with `eval`, `Function`, `node:vm`, or another executable parser.
4. Regenerate reference files.
5. Review source credit, translation coverage, counts, and rights notes.
6. Update the snapshot-specific tests and documentation in the same pull request.

```bash
node tools/extract_site_data.mjs \
  path/to/site-inline.js \
  work/catalog.json \
  --captured-at 2026-07-16T17:29:57+08:00

python3 tools/build_reference_files.py work/catalog.json skill/design-lab-prompts
```

The extractor intentionally rejects executable expressions and template interpolation. If the upstream structure changes, update the parser narrowly and add a failing fixture test before changing production code.

## Verification

Run all checks before submitting:

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

The generator command should not change tracked files unless the canonical catalog, version, or source notes changed intentionally.

## Pull request checklist

- [ ] The change has a focused purpose and no unrelated generated diff.
- [ ] Behavior changes include a test that failed before the implementation.
- [ ] The full verification suite passes locally.
- [ ] Generated files and `manifest.json` are current.
- [ ] Source-derived wording remains attributed and separate from original project authorship.
- [ ] Documentation reflects any user-visible or maintenance change.
- [ ] No secrets, private captures, or unrelated user data are included.

By contributing original code or documentation, you agree that it may be distributed under this repository's MIT License. This does not alter rights in upstream-derived content.
