"""Rule-based verifier for LLM explanation drafts.

The LLM writes a DRAFT that contains markers such as {plco.display}; it must not
write numbers itself. The verifier checks the draft against the structured
result BEFORE the markers are filled in. Each rule maps to one error type of the
thesis error taxonomy:

  R0 unknown_marker     marker that does not exist in the structured result
  R1 number             a digit or number word written by the LLM
  R2 period             wrong or missing time period for the risk
  R3 unit               wrong unit (percent, per thousand, odds, "times")
  R4 direction          change described in the wrong direction
  R5 reassurance        false reassurance ("safe", "no risk", ...)
  R6 diagnosis          statement that sounds like a diagnosis
  R7 finding            X-ray finding that is not in the structured result

Known limits (reported in the thesis): synonyms that are not in the lists are
missed; negation is handled only by the direction and finding rules; meaning
errors that use none of the listed words are not caught.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from ..result import allowed_markers

MARKER_RE = re.compile(r"\{([a-z0-9_.]+)\}")
DIGIT_RE = re.compile(r"\d")

NUMBER_WORDS = {
    "en": ["zero", "two", "three", "four", "five", "six", "seven", "eight", "nine",
           "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
           "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty",
           "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
           "half", "twice", "double", "triple", "quarter", "third"],
    "ro": ["zero", "unu", "una", "doi", "două", "trei", "patru", "cinci", "șase", "sase",
           "șapte", "sapte", "opt", "nouă", "noua", "zece", "douăzeci", "sută", "suta",
           "sute", "mie", "mii", "jumătate", "jumatate", "dublu", "triplu", "sfert"],
}
# v2: "one" is common in normal English ("one person", "no one"), so it counts as
# a number only when used as a quantity ("one in fifty", "one out of", "one percent").
ONE_AS_NUMBER = re.compile(r"(?<![\w-])one(?=\s+(?:in|out|per|of every|hundred|thousand|percent)\b|\s*%)")

PERIOD_PHRASES = {
    "en": ["lifetime", "per year", "each year", "every year", "annual", "annually",
           "next year", "this year", "a decade", "the decade", "per month", "rest of your life",
           "within a year", "one year", "in a year"],
    "ro": ["toată viața", "pe an", "în fiecare an", "anual", "anul viitor", "deceniu"],
}

UNIT_PHRASES = {
    "en": ["%", "percent", "per cent", "percentage", "per thousand", "per mille", "odds",
           "times higher", "times more", "times as", "fold"],
    "ro": ["%", "procent", "la mie", "de ori"],
}

UP_WORDS = {"en": ["increase", "increases", "raise", "raises", "higher", "rise", "rises",
                   "worse", "grow", "grows", "go up", "goes up", "greater"],
            "ro": ["crește", "creste", "mai mare", "mai ridicat"]}
DOWN_WORDS = {"en": ["lower", "decrease", "decreases", "reduce", "reduces", "drop", "drops",
                     "fall", "falls", "smaller", "go down", "goes down", "less"],
              "ro": ["scade", "mai mic", "mai scăzut", "reduce"]}
NEGATIONS = {"en": ["not", "never", "no longer"], "ro": ["nu", "niciodată"]}

SCENARIO_CUES = {
    "quit_now": {"en": ["stop smoking", "quit", "quitting", "stopping", "give up", "giving up",
                        "scen.quit_now"],
                 "ro": ["renunți", "renunta", "te oprești", "scen.quit_now"]},
    "continue": {"en": ["keep smoking", "continue", "continuing", "carry on", "scen.continue"],
                 "ro": ["continui", "scen.continue"]},
    "increase": {"en": ["smoke more", "smoking more", "scen.increase"],
                 "ro": ["fumezi mai mult", "scen.increase"]},
}

REASSURANCE = {
    "en": ["safe", "no risk", "zero risk", "risk-free", "nothing to worry", "no need to worry",
           "you are fine", "you're fine", "guaranteed", "will not get", "won't get",
           "perfectly healthy", "all clear"],
    "ro": ["în siguranță", "fără risc", "niciun risc", "nu aveți de ce", "nu ai de ce",
           "sigur nu", "garantat"],
}

DIAGNOSIS_RE = {
    "en": [r"\byou (?:have|'ve got|have got|do not have|don't have|are free of)\b[^.;]*?"
           r"\b(?:cancer|tumou?r|disease|copd|emphysema)\b",
           r"\bdiagnosed with\b", r"\byou are diagnosed\b", r"\bcancer-free\b",
           r"\byour lungs are (?:healthy|damaged|diseased)\b"],
    "ro": [r"\b(?:ai|aveți|aveti|nu ai|nu aveți)\b[^.;]*?\b(?:cancer|tumoră|tumora|boală|boala)\b",
           r"\bdiagnosticat\w*\b"],
}

SINGULAR = {"nodules": "nodule", "masses": "mass", "lesions": "lesion", "opacities": "opacity",
            "tumour": "tumor", "oedema": "edema"}
FINDING_TERMS = ["nodule", "nodules", "mass", "masses", "tumour", "tumor", "emphysema",
                 "fibrosis", "pneumonia", "effusion", "pneumothorax", "cardiomegaly",
                 "atelectasis", "consolidation", "edema", "oedema", "infiltration", "hernia",
                 "lesion", "lesions", "opacity", "opacities"]


@dataclass(frozen=True)
class Violation:
    rule: str
    detail: str

    def __str__(self) -> str:
        return f"{self.rule}: {self.detail}"


def _has_phrase(text: str, phrase: str) -> bool:
    if phrase.isalpha() or " " in phrase or "-" in phrase or "'" in phrase:
        return re.search(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", text) is not None
    return phrase in text


def _clauses(text: str) -> list[str]:
    # split on sentence ends followed by a space (markers contain dots) and on
    # contrast words
    return [c for c in re.split(r"[.;!?](?=\s|$)|\bbut\b|\bwhile\b|\bwhereas\b", text)
            if c and c.strip()]


def verify(draft: str, result: dict) -> list[Violation]:
    lang = result.get("language", "en")
    v: list[Violation] = []
    allowed = allowed_markers(result)

    # R0: markers must exist in the structured result
    for m in MARKER_RE.findall(draft):
        if m not in allowed:
            v.append(Violation("R0_unknown_marker", m))

    low = MARKER_RE.sub(lambda mm: f" mk:{mm.group(1)} ", draft).lower()
    low_words = MARKER_RE.sub(" ", draft).lower()

    # R1: no digits, no number words
    if DIGIT_RE.search(MARKER_RE.sub(" ", draft)):
        v.append(Violation("R1_number", "digit written by the model"))
    scrub = low_words
    if lang == "en" and ONE_AS_NUMBER.search(scrub):
        v.append(Violation("R1_number", "number word 'one'"))
    for w in NUMBER_WORDS[lang]:
        if any(x.rule == "R1_number" and "word" in x.detail for x in v):
            break
        if re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", scrub):
            v.append(Violation("R1_number", f"number word '{w}'"))
            break

    # R2: time period
    for ph in PERIOD_PHRASES[lang]:
        if _has_phrase(low_words, ph):
            v.append(Violation("R2_period", f"wrong period '{ph}'"))
            break
    for sent in re.split(r"[.!?](?=\s|$)", draft):
        if "{plco.display}" in sent and "{plco.horizon}" not in sent:
            v.append(Violation("R2_period", "risk given without its time period"))
            break

    # R3: unit
    for ph in UNIT_PHRASES[lang]:
        if _has_phrase(low_words, ph):
            v.append(Violation("R3_unit", f"wrong unit '{ph}'"))
            break

    # R4: direction, checked per clause; a clause belongs to the scenario whose
    # cue appears first in it
    directions = result.get("direction", {})
    for clause in _clauses(low):
        positions = {}
        for scen, cues in SCENARIO_CUES.items():
            hits = [clause.find(c) for c in cues[lang] if c in clause]
            if hits:
                positions[scen] = min(hits)
        if not positions:
            continue
        scen = min(positions, key=positions.get)
        if scen not in directions:
            continue
        negated = any(_has_phrase(clause, n) for n in NEGATIONS[lang]) or "n't" in clause
        said_up = any(_has_phrase(clause, w) for w in UP_WORDS[lang])
        said_down = any(_has_phrase(clause, w) for w in DOWN_WORDS[lang])
        if negated:
            said_up, said_down = said_down, said_up
        truth = directions[scen]
        # v2: "similar" also makes up/down words wrong
        if (said_up and truth != "higher") or (said_down and truth != "lower"):
            v.append(Violation("R4_direction", f"'{scen}' described in the wrong direction"))
            break

    # R5: false reassurance
    for ph in REASSURANCE[lang]:
        if _has_phrase(low_words, ph):
            v.append(Violation("R5_reassurance", f"'{ph}'"))
            break

    # R6: diagnosis-like statements
    for pat in DIAGNOSIS_RE[lang]:
        if re.search(pat, low_words):
            v.append(Violation("R6_diagnosis", pat))
            break

    # R7: findings must be in the structured result. v2: a term that the model
    # did NOT flag may only appear in a negated sentence ("the model did not flag ...").
    xr = result.get("xray") or {}
    flagged = " ".join(xr.get("flagged", [])).lower()
    not_flagged = " ".join(xr.get("not_flagged", [])).lower()
    for sent in re.split(r"[.!?](?=\s|$)", low_words):
        negated = any(_has_phrase(sent, n) for n in NEGATIONS[lang]) or "n't" in sent \
            or _has_phrase(sent, "no")
        hit = None
        for term in FINDING_TERMS:
            if not _has_phrase(sent, term):
                continue
            stem = SINGULAR.get(term, term)
            if _has_phrase(flagged, stem):
                continue
            if _has_phrase(not_flagged, stem) and negated:
                continue
            hit = term
            break
        if hit:
            v.append(Violation("R7_finding", f"'{hit}' not flagged in the result"))
            break
    return v


def fill(draft: str, result: dict) -> str:
    allowed = allowed_markers(result)
    return MARKER_RE.sub(lambda m: allowed.get(m.group(1), m.group(0)), draft)
