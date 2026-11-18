"""Generator of FICTIONAL cases (no real people). Seeded, so runs are reproducible.

Value ranges are design choices for testing; they cover people inside and outside
the 55-74 age range in which PLCOm2012 was developed.
"""
from __future__ import annotations

import random

from app.schemas import Questionnaire, XrayInfo

# TorchXRayVision pathology names used for fictional X-ray results
XRAY_LABELS = ["Atelectasis", "Consolidation", "Infiltration", "Pneumothorax", "Edema",
               "Emphysema", "Fibrosis", "Effusion", "Pneumonia", "Cardiomegaly", "Nodule",
               "Mass", "Lung Opacity"]


def make_case(rng: random.Random, language: str = "en") -> tuple[Questionnaire, XrayInfo]:
    age = rng.randint(50, 80)
    current = rng.random() < 0.6
    start_age = rng.randint(14, 25)
    if current:
        smoking_years = max(1, age - start_age)
        quit_years = 0
    else:
        quit_years = rng.randint(1, min(25, max(1, age - start_age - 1)))
        smoking_years = max(1, age - start_age - quit_years)
    q = Questionnaire(
        age=age,
        race=rng.choices(["white", "black", "hispanic", "asian"], weights=[85, 5, 5, 5])[0],
        education=rng.randint(1, 6),
        bmi=round(rng.uniform(18.5, 38.0), 1),
        copd=rng.random() < 0.2,
        personal_cancer_history=rng.random() < 0.08,
        family_history_lung_cancer=rng.random() < 0.15,
        smoking_status="current" if current else "former",
        cigs_per_day=rng.choice([5, 10, 15, 20, 25, 30, 40]),
        smoking_years=smoking_years,
        quit_years=quit_years,
        language=language,
    )
    if rng.random() < 0.5:
        labels = rng.sample(XRAY_LABELS, k=rng.randint(0, 2))
        xr = XrayInfo(provided=True, flagged=labels,
                      not_flagged=[x for x in XRAY_LABELS if x not in labels])
    else:
        xr = XrayInfo(provided=False)
    return q, xr


def make_cases(n: int, seed: int = 2026, language: str = "en"):
    rng = random.Random(seed)
    return [make_case(rng, language) for _ in range(n)]
