"""Scenario engine: "quit now", "continue", "increase".

Method: the inputs are moved forward by t years (age, years smoked, years since
quitting) and the SAME 6-year PLCOm2012 risk is recomputed "as if assessed at
year t". This follows the future-risk projection idea of Kumarasamy et al.,
Thorax 2025 (doi:10.1136/thorax-2024-222098).

These are projections from a prediction model, not causal effects of quitting
(van Geloven et al., Eur J Epidemiol 2020). The labels below say so.

Design choices of this thesis (not taken from a paper):
* INCREASE_FACTOR: "increase" means smoking 1.5x the current cigarettes per day.
* PLCOm2012 intensity is the average cigarettes per day over the smoking history,
  so under "increase" the average is updated as a duration-weighted mean.
* BMI, education, COPD and history variables are held fixed.
"""
from __future__ import annotations

from dataclasses import replace

from .plcom2012 import PlcoInputs, in_validated_age_range, risk_6y

YEARS = (3, 5, 7)
INCREASE_FACTOR = 1.5

LABELS = {
    "quit_now": "If you stop smoking now (best case, no relapse)",
    "continue": "If you keep smoking as now",
    "increase": "If you smoke more (least reliable projection)",
}


def project(x: PlcoInputs, scenario: str, t: int) -> PlcoInputs | None:
    """Return the inputs as they would be t years from now, or None if the
    scenario does not apply (e.g. 'increase' for a former smoker)."""
    if t < 0:
        raise ValueError("t must be >= 0")
    if scenario not in LABELS:
        raise ValueError(f"unknown scenario: {scenario}")
    aged = replace(x, age=x.age + t)
    if not x.current_smoker:
        # A former smoker stays quit under 'quit_now' and 'continue'.
        if scenario == "increase":
            return None
        return replace(aged, quit_years=x.quit_years + t)
    if scenario == "quit_now":
        if t == 0:
            return aged
        return replace(aged, current_smoker=False, quit_years=float(t))
    if scenario == "continue":
        return replace(aged, smoking_years=x.smoking_years + t)
    # increase
    new_years = x.smoking_years + t
    new_cpd = x.cigs_per_day * INCREASE_FACTOR
    avg_cpd = (x.cigs_per_day * x.smoking_years + new_cpd * t) / new_years if new_years else new_cpd
    return replace(aged, smoking_years=new_years, cigs_per_day=avg_cpd)


def run_scenarios(x: PlcoInputs, years: tuple[int, ...] = YEARS) -> dict:
    """Compute the 6-year risk at each future year for each scenario."""
    out: dict = {"scenarios": {}}
    for name in LABELS:
        points = []
        for t in years:
            px = project(x, name, t)
            if px is None:
                continue
            points.append({
                "year": t,
                "risk_6y": risk_6y(px),
                "outside_validated_age": not in_validated_age_range(px.age),
            })
        if points:
            out["scenarios"][name] = {"label": LABELS[name], "points": points}
    return out
