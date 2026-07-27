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
