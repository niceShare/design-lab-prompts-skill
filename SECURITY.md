# Security Policy

## Supported version

Security fixes are applied to the latest state of the `main` branch. Historical snapshots and forks are not maintained by this project.

## Report a vulnerability

Please report a suspected vulnerability privately through [GitHub Security Advisories](https://github.com/niceShare/design-lab-prompts-skill/security/advisories/new). Do not open a public issue for an unpatched vulnerability.

Include:

- The affected file, command, and environment.
- Reproduction steps or a minimal fixture.
- The expected and observed behavior.
- The security impact and any known workaround.

Do not include secrets, private website captures, or unrelated personal data. Maintainers will review good-faith reports and coordinate disclosure after a fix is available.

## Security model

- The query CLI reads a local JSON catalog and does not make network requests.
- The extractor operates on a maintainer-provided local page capture.
- Captured JavaScript is treated as untrusted input. The extractor parses a restricted data-literal grammar and does not evaluate page code.
- Functions, calls, computed expressions, duplicate object keys, sparse arrays, and template interpolation are rejected.
- Generated manifest hashes detect accidental file drift; they are integrity metadata, not signatures.

Legal, attribution, or content-removal concerns are not security vulnerabilities. They may be reported through the repository issue tracker without including sensitive information.
