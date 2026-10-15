# Prompt Constraint Auditor

[![CI](https://github.com/loganpendragonmultiverse/prompt-constraint-auditor/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/prompt-constraint-auditor/actions/workflows/ci.yml)

Extract prompt constraints, surface assumptions, and flag possible internal conflicts. The command uses explicit UTF-8 JSON input and produces reviewable JSON or Markdown output.

## Three-minute start

```bash
python -m pip install .
prompt-constraints examples/sample.json
prompt-constraints examples/sample.json --format json --output report.json
```

The example documents the v1 input shape. Existing report files are never overwritten. Source inputs are read-only except where the documented purpose explicitly creates a new output artifact.

## Privacy and platforms

The tool runs locally and does not upload input or include telemetry. Python 3.10 or newer is supported on Windows, macOS, and Linux.

## Interpretation boundary

The auditor uses deterministic wording cues and lexical overlap. It cannot reliably infer every implied constraint or prove that two instructions conflict.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Traceable constraint occurrences

Each constraint now has a deterministic occurrence ID such as `constraint-000001`, a `span`, and matched `cues` with their own spans. IDs follow constraint order within this report; they distinguish repeated text but are not stable identifiers across edited prompts. Span `start`/`end` are zero-based Unicode character offsets with an exclusive end, so `prompt[start:end]` reproduces the exact reported text. Lines and columns are one-based and the end column is exclusive; CRLF counts as one line break. Conflict records retain `left`/`right` text and add `left_id`/`right_id` references. Existing counts, assumptions, and lexical interpretation rules are preserved. A reference makes a possible conflict traceable; it does not prove a semantic contradiction.
