from __future__ import annotations

import json
import re
from itertools import combinations
from typing import Any

PROJECT = "prompt-constraint-auditor"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _span(prompt: str, start: int, end: int) -> dict[str, int]:
    """Zero-based Unicode offsets; one-based line/columns; end is exclusive."""
    return {
        "start": start,
        "end": end,
        "start_line": prompt.count("\n", 0, start) + 1,
        "start_column": start - prompt.rfind("\n", 0, start),
        "end_line": prompt.count("\n", 0, end) + 1,
        "end_column": end - prompt.rfind("\n", 0, end),
    }


def _prompt_constraints(data: dict[str, Any]) -> dict[str, Any]:
    prompt = str(_require(data, "prompt"))
    # Split by the existing punctuation/newline rules, retaining source offsets.
    sentences = []
    cursor = 0
    for boundary in re.finditer(r"(?<=[.!?])\s+|\n+|\Z", prompt):
        raw = prompt[cursor : boundary.start()]
        sentence = raw.strip()
        if sentence:
            offset = cursor + len(raw) - len(raw.lstrip())
            sentences.append((sentence, offset, offset + len(sentence)))
        cursor = boundary.end()
    markers = re.compile(
        r"\b(must not|should not|do not|must|should|never|always|only|avoid|required|cannot|can't)\b",
        re.IGNORECASE,
    )
    constraints: list[dict[str, Any]] = []
    for sentence, start, end in sentences:
        cues = list(markers.finditer(sentence))
        if not cues:
            continue
        constraints.append(
            {
                "id": f"constraint-{len(constraints) + 1:06d}",
                "text": sentence,
                "span": _span(prompt, start, end),
                "cues": [
                    {
                        "text": cue.group(),
                        "span": _span(prompt, start + cue.start(), start + cue.end()),
                    }
                    for cue in cues
                ],
                "strength": "hard"
                if re.search(
                    r"\b(must|do not|never|always|only|required|cannot|can't)\b",
                    sentence,
                    re.IGNORECASE,
                )
                else "soft",
                "negative": bool(
                    re.search(
                        r"\b(not|never|avoid|cannot|can't)\b",
                        sentence,
                        re.IGNORECASE,
                    )
                ),
            }
        )
    conflicts = []
    for left, right in combinations(constraints, 2):
        left_terms = set(re.findall("[a-z]{4,}", str(left["text"]).casefold())) - {
            "must",
            "should",
            "never",
            "always",
            "only",
            "avoid",
        }
        right_terms = set(re.findall("[a-z]{4,}", str(right["text"]).casefold())) - {
            "must",
            "should",
            "never",
            "always",
            "only",
            "avoid",
        }
        if left["negative"] != right["negative"] and len(left_terms & right_terms) >= 2:
            conflicts.append(
                {
                    "left": left["text"],
                    "left_id": left["id"],
                    "right": right["text"],
                    "right_id": right["id"],
                    "shared_terms": sorted(left_terms & right_terms),
                }
            )
    assumptions = [
        sentence
        for sentence, _, _ in sentences
        if re.search("\\b(assume|probably|likely|usually|by default)\\b", sentence, re.IGNORECASE)
    ]
    return {
        "constraints": constraints,
        "conflicts": conflicts,
        "assumptions": assumptions,
        "counts": {
            "hard": sum(item["strength"] == "hard" for item in constraints),
            "soft": sum(item["strength"] == "soft" for item in constraints),
        },
    }


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": 1, "project": PROJECT, **_prompt_constraints(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.extend(
                [
                    f"## {key.replace('_', ' ').title()}",
                    "",
                    f"```json\n{json.dumps(value, indent=2, ensure_ascii=False, default=str)}\n```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"
