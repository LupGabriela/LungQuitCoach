"""Explanation pipeline: LLM draft -> verifier -> one retry -> fixed template."""
from __future__ import annotations

import json

from ..result import allowed_markers
from ..schemas import Explanation
from .llm_client import LLM
from .template import template_draft
from .verifier import fill, verify

MAX_ATTEMPTS = 2  # first try + one retry
SAFE_MINIMAL = ("Your estimated chance of lung cancer over the next {plco.horizon} is "
                "{plco.display}. This is an estimate from a model, not a diagnosis.")


def build_prompt(result: dict, feedback: list[str] | None = None) -> str:
    facts = {k: result[k] for k in ("language", "smoking_status", "direction", "xray")}
    prompt = ("RESULT:\n" + json.dumps(facts, ensure_ascii=False) +
              "\nMARKERS:\n" + "\n".join("{" + m + "}" for m in allowed_markers(result)))
    if feedback:
        prompt += "\nYour previous draft was rejected for: " + "; ".join(feedback[:10])
    return prompt


def explain(result: dict, llm: LLM | None) -> Explanation:
    attempts = 0
    last: list[str] = []
    if llm is not None:
        for _ in range(MAX_ATTEMPTS):
            attempts += 1
            try:
                draft = llm.generate(build_prompt(result, last or None))
            except Exception as exc:  # LLM down -> template
                last = [f"llm_error: {type(exc).__name__}"]
                break
            violations = verify(draft, result)
            if not violations:
                return Explanation(text=fill(draft, result), source="llm", attempts=attempts)
            last = [str(x) for x in violations]
    draft = template_draft(result)
    if verify(draft, result):  # fail closed: should never happen (tested on generated cases)
        draft = SAFE_MINIMAL
    return Explanation(text=fill(draft, result), source="template",
                       attempts=attempts, violations=last)
