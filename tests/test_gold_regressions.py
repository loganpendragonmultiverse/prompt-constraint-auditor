import json
import re

import pytest

from prompt_constraint_auditor.cli import main
from prompt_constraint_auditor.core import analyze, render_markdown


@pytest.mark.parametrize(
    "data",
    [
        None,
        [],
        42,
        "text",
        {"prompt": None},
        {"prompt": 77},
        {"prompt": True},
        {"prompt": []},
        {"prompt": {}},
        {"prompt": ""},
        {"prompt": " \r\n\t"},
    ],
)
def test_malformed_shapes_fail_with_actionable_input_error(data):
    with pytest.raises((TypeError, ValueError)):
        analyze(data)


def test_invalid_cli_input_has_no_report_or_traceback(tmp_path, capsys):
    source = tmp_path / "source.json"
    source.write_text("[]", encoding="utf-8")
    report = tmp_path / "report.json"
    assert main([str(source), "--output", str(report)]) == 2
    assert not report.exists()
    assert source.read_text() == "[]"
    assert "input must be a JSON object" in capsys.readouterr().err


def test_unicode_source_evidence_and_authored_markdown_remain_literal():
    prompt = "  Café must publish clear reports.\r\nNever publish clear reports.\nMust include ```\n# Author text."
    original = {"prompt": prompt}
    report = analyze(original)
    assert original == {"prompt": prompt}
    assert [c["id"] for c in report["constraints"]] == [
        "constraint-000001",
        "constraint-000002",
        "constraint-000003",
    ]
    for constraint in report["constraints"]:
        span = constraint["span"]
        assert prompt[span["start"] : span["end"]] == constraint["text"]
        for cue in constraint["cues"]:
            span = cue["span"]
            assert prompt[span["start"] : span["end"]] == cue["text"]
    assert report["conflicts"][0]["left_id"] == "constraint-000001"
    payload = re.search(
        r"## Constraints\n\n```json\n(.*?)\n```", render_markdown(report), re.DOTALL
    )
    assert json.loads(payload.group(1)) == report["constraints"]
