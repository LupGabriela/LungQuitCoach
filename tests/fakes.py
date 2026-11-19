"""Test double for the LLM: returns pre-set drafts in order."""


class FakeLLM:
    def __init__(self, drafts: list[str]):
        self._drafts = list(drafts)

    def generate(self, prompt: str) -> str:
        return self._drafts.pop(0) if self._drafts else ""
