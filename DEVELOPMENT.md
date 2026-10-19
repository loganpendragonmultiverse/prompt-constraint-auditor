# Development contract

Extract prompt constraints, surface assumptions, and flag possible internal conflicts.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, changelog, README claims, repository metadata, release assets, and the Forge catalog together.

## 1.1.0 - 2026-10-15

Attach deterministic IDs and exact Unicode source/cue spans to each constraint occurrence. Reference constraint IDs from conflict records, including repeated wording.

See README.md for interface details and TESTING.md for the verification gate.
Published on GitHub after independent review and passing PR, main, and tag checks.

## 1.1.1 - 2026-10-16

Documentation and version declarations only. Library implementation and tests are unchanged from 1.1.0.

## 1.1.2 maintenance

- Reject malformed JSON input shapes instead of stringifying values or crashing.
- Create report files exclusively, refuse symlink destinations and return a clean error for closed stdout pipes.
- Include release handoff documents and their license with the installed package.

Preserve exact source and cue spans, deterministic occurrence IDs and the documented lexical interpretation limits. Release through independent review, protected CI and exact tag-built installed-distribution acceptance.
