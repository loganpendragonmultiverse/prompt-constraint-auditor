from prompt_constraint_auditor.core import analyze, render_json


def test_repeats_are_distinct_and_conflicts_reference_occurrences():
    prompt = "Must publish clear reports. Must publish clear reports. Never publish clear reports."
    report = analyze({"prompt": prompt})
    constraints = report["constraints"]
    assert [x["id"] for x in constraints] == [
        "constraint-000001",
        "constraint-000002",
        "constraint-000003",
    ]
    assert constraints[0]["text"] == constraints[1]["text"]
    assert constraints[0]["span"]["start"] != constraints[1]["span"]["start"]
    assert [(x["left_id"], x["right_id"]) for x in report["conflicts"]] == [
        ("constraint-000001", "constraint-000003"),
        ("constraint-000002", "constraint-000003"),
    ]
    assert render_json(report) == render_json(analyze({"prompt": prompt}))


def test_exact_unicode_punctuation_crlf_and_cue_spans():
    prompt = "  Café must not leak données!\r\n\tYou SHOULD avoid logs?  Usually fine.\n"
    report = analyze({"prompt": prompt})
    first, second = report["constraints"]
    assert first["span"] == {
        "start": 2,
        "end": 29,
        "start_line": 1,
        "start_column": 3,
        "end_line": 1,
        "end_column": 30,
    }
    assert second["span"]["start_line"] == 2 and second["span"]["start_column"] == 2
    assert [c["text"] for c in first["cues"]] == ["must not"]
    assert first["strength"] == "hard" and first["negative"]
    assert second["strength"] == "soft" and second["negative"]
    for item in report["constraints"]:
        assert prompt[item["span"]["start"] : item["span"]["end"]] == item["text"]
        for cue in item["cues"]:
            assert prompt[cue["span"]["start"] : cue["span"]["end"]] == cue["text"]
    assert report["assumptions"] == ["Usually fine."]


def test_marker_boundaries_and_no_constraints():
    assert analyze({"prompt": "mustard shouldering ONLYish"})["constraints"] == []
    report = analyze({"prompt": "Only output JSON; do not explain.\nYou can't publish secrets."})
    assert len(report["constraints"]) == 2
    assert report["counts"] == {"hard": 2, "soft": 0}
    assert [x["text"] for x in report["constraints"][0]["cues"]] == ["Only", "do not"]
