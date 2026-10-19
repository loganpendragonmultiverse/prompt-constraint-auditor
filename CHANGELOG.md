# Changelog

## 1.1.2 - 2026-10-19

- Reject malformed JSON input shapes instead of stringifying values or crashing.
- Create report files exclusively, refuse symlink destinations and return a clean error for closed stdout pipes.
- Include release handoff documents and their license with the installed package.

## 1.1.1 - 2026-10-16

- Correct release wording and include dated release history and development notes in source distributions.
- Preserve version 1.1.0 comparison/auditing behavior; update package and runtime version declarations only.

## 1.1.0 - 2026-10-15

- Attach deterministic IDs and exact Unicode source/cue spans to each constraint occurrence.
- Reference constraint IDs from conflict records, including repeated wording.

## 1.0.0 - 2026-07-26

- Released the first complete Prompt Constraint Auditor command-line workflow.
- Added deterministic reporting, representative examples, cross-platform tests, and explicit limitations.
