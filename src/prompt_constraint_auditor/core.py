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


def _prompt_constraints(data: dict[str, Any]) -> dict[str, Any]:
    prompt = str(_require(data, "prompt"))
    sentences = [item.strip() for item in re.split("(?<=[.!?])\\s+|\\n+", prompt) if item.strip()]
    markers = re.compile(
        "\\b(must|must not|should|should not|do not|never|always|only|avoid|required|cannot|can't)\\b",
        re.IGNORECASE,
    )
    constraints: list[dict[str, Any]] = [
        {
            "text": sentence,
            "strength": "hard"
            if re.search(
                "\\b(must|must not|do not|never|always|only|required|cannot|can't)\\b",
                sentence,
                re.IGNORECASE,
            )
            else "soft",
            "negative": bool(
                re.search("\\b(not|never|avoid|cannot|can't)\\b", sentence, re.IGNORECASE)
            ),
        }
        for sentence in sentences
        if markers.search(sentence)
    ]
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
                    "right": right["text"],
                    "shared_terms": sorted(left_terms & right_terms),
                }
            )
    assumptions = [
        sentence
        for sentence in sentences
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
