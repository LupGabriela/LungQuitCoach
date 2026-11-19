"""LLM clients. The local client talks to an Ollama server over its REST API
(POST /api/generate on port 11434 by default). Tests use a fake model
(tests/fakes.py), so no model is needed to run the test suite."""
from __future__ import annotations

import json
import os
import urllib.request
from typing import Protocol

SYSTEM_PROMPT = """You write short, kind, plain-language explanations of lung cancer risk results
for adults without medical training. You receive ONE JSON object called RESULT and a
list of MARKERS. RESULT is the only source of facts.
Rules:
1. Never write a number, digit or number word. Where a number or time period is
   needed, write the marker exactly, for example {plco.display} or {plco.horizon}.
2. Every sentence that gives the risk {plco.display} must also contain {plco.horizon}.
3. Use only markers from the MARKERS list.
4. Never say the person has or does not have a disease. Never say they are safe.
5. Describe each scenario in the direction given in RESULT.direction: "quit_now" and
   "increase" are compared with continuing to smoke; "continue" is compared with today.
6. Mention X-ray findings only if they are in RESULT.xray.flagged.
7. Use short sentences and everyday words. At most 120 words.
"""


class LLM(Protocol):
    def generate(self, prompt: str) -> str: ...


class OllamaLLM:
    def __init__(self, model: str = "qwen3:4b", host: str | None = None, timeout: int = 300,
                 temperature: float | None = None, seed: int = 2026):
        self.model = model
        self.temperature = temperature  # None = the model's default
        self.seed = seed
        self.host = host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        options: dict = {"seed": self.seed}
        if self.temperature is not None:
            options["temperature"] = self.temperature
        # think=False: Qwen 3 thinks by default, which would make a CPU-only
        # laptop write a long hidden reasoning trace before every explanation
        body = json.dumps({"model": self.model, "system": SYSTEM_PROMPT, "prompt": prompt,
                           "stream": False, "think": False, "options": options}).encode()
        req = urllib.request.Request(f"{self.host}/api/generate", data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.loads(r.read())["response"]
