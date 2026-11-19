"""Baseline for experiment E1 (not used by the application)."""
from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Baseline used for comparison in experiment E1: a simple number-matching check
# on the FILLED text (every number must appear in the structured result), in the
# style of the validator first drafted in the thesis plan (Chapter 7.4).
NUM_RE = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)?")


def baseline_check(filled_text: str, result: dict) -> list[str]:
    allowed: set[str] = {"100"}

    def walk(o):
        if isinstance(o, dict):
            for val in o.values():
                walk(val)
        elif isinstance(o, list):
            for val in o:
                walk(val)
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            for x in (o, o * 100):
                allowed.update({f"{x:g}", str(round(x)), f"{x:.1f}".rstrip("0").rstrip(".")})
        elif isinstance(o, str):
            allowed.update(NUM_RE.findall(o))

    walk(result)
    # v2: the scenario years (keys "y3", "y5", "y7") are legitimate numbers too
    for block in result.get("scenarios", {}).values():
        allowed.update(k[1:] for k in block if re.fullmatch(r"y\d+", k))
    return [f"number not in result: {n}" for n in NUM_RE.findall(filled_text)
            if n.replace(",", ".") not in allowed]
