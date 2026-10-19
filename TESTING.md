# Testing

Use an isolated Python environment and install `python -m pip install -e ".[dev]"`.
Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`.
The repository CI matrix covers Python 3.10 and 3.14 on Linux, Windows, and macOS.
New regressions live alongside the existing core/CLI tests.

## 1.1.2 acceptance

Exercise malformed root and field shapes, the README examples, existing report files, dangling report symlinks, racing output creation and a real consumer-closed stdout pipe. Check unchanged source bytes and lexical evidence. Install the actual tag-built wheel and source distribution in isolation; run their CLI entrypoints away from the checkout and verify bundled handoff documents and examples. Retain all protected platform checks, CodeQL and the existing coverage floor.
