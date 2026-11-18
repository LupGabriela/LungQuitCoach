"""PLCOm2012 6-year lung cancer risk model.

Source of every coefficient and centering value: Tammemägi M.C. et al.,
"Selection criteria for lung-cancer screening", N Engl J Med 2013;368:728-736,
Table 2 and its footnote (PMC3929969).

The model applies only to people who have EVER smoked. PLCO enrolled people aged
55-74 (Oken et al., JAMA 2011), so results outside that age range are flagged.

Implementation convention (not stated in the paper): current smokers use
quit_years = 0. This matches the open implementations listed in the thesis notes.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

CONSTANT = -4.532506
B_AGE, C_AGE = 0.0778868, 62.0
B_EDU, C_EDU = -0.0812744, 4.0
B_BMI, C_BMI = -0.0274194, 27.0
B_COPD = 0.3553063
B_CANCER_HIST = 0.4589971
B_FAMILY_HIST = 0.587185
B_CURRENT = 0.2597431
B_INTENSITY, C_INTENSITY = -1.822606, 0.4021541613
B_DURATION, C_DURATION = 0.0317321, 27.0
B_QUIT, C_QUIT = -0.0308572, 10.0

RACE_TERMS = {
    "white": 0.0,
    "black": 0.3944778,
    "hispanic": -0.7434744,
    "asian": -0.466585,
    "american_indian_alaska_native": 0.0,
    "native_hawaiian_pacific_islander": 1.027152,
}

VALIDATED_AGE_RANGE = (55, 74)
HORIZON_YEARS = 6


@dataclass(frozen=True)
class PlcoInputs:
    age: float
    race: str
    education: int  # 1..6, Table 2 footnote coding
    bmi: float
    copd: bool
    personal_cancer_history: bool
    family_history_lung_cancer: bool
    current_smoker: bool
    cigs_per_day: float
    smoking_years: float
    quit_years: float = 0.0  # 0 for current smokers (implementation convention)

    def validate(self) -> None:
        if self.race not in RACE_TERMS:
            raise ValueError(f"unknown race category: {self.race}")
        if not 1 <= self.education <= 6:
            raise ValueError("education must be an integer level from 1 to 6")
        if self.cigs_per_day <= 0:
            raise ValueError("PLCOm2012 applies to ever-smokers only (cigs_per_day > 0)")
        for name in ("age", "bmi", "smoking_years", "quit_years"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must not be negative")
        if self.bmi <= 0:
            raise ValueError("bmi must be positive")
        if self.current_smoker and self.quit_years != 0:
            raise ValueError("current smokers must have quit_years = 0")


def logit(x: PlcoInputs) -> float:
    """Linear predictor of PLCOm2012 (Table 2 footnote)."""
    x.validate()
    intensity = (x.cigs_per_day / 10.0) ** -1 - C_INTENSITY
    return (
        CONSTANT
        + B_AGE * (x.age - C_AGE)
        + RACE_TERMS[x.race]
        + B_EDU * (x.education - C_EDU)
        + B_BMI * (x.bmi - C_BMI)
        + B_COPD * int(x.copd)
        + B_CANCER_HIST * int(x.personal_cancer_history)
        + B_FAMILY_HIST * int(x.family_history_lung_cancer)
        + B_CURRENT * int(x.current_smoker)
        + B_INTENSITY * intensity
        + B_DURATION * (x.smoking_years - C_DURATION)
        + B_QUIT * (x.quit_years - C_QUIT)
    )


def risk_6y(x: PlcoInputs) -> float:
    """6-year probability of a lung cancer diagnosis: exp(l) / (1 + exp(l))."""
    lp = logit(x)
    return 1.0 / (1.0 + math.exp(-lp))


def in_validated_age_range(age: float) -> bool:
    lo, hi = VALIDATED_AGE_RANGE
    return lo <= age <= hi


def as_in_100(p: float) -> str:
    """Display a probability as 'x in 100' with one decimal (design choice)."""
    return f"{p * 100:.1f} in 100"
