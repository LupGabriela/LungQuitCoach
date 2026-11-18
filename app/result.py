"""Build the structured result from a questionnaire (and optional X-ray info)."""
from __future__ import annotations

from .risk.plcom2012 import HORIZON_YEARS, PlcoInputs, as_in_100, in_validated_age_range, risk_6y
from .risk.scenarios import YEARS, run_scenarios
from .schemas import Questionnaire, XrayInfo

SCHEMA_VERSION = "1.0"


def to_plco_inputs(q: Questionnaire) -> PlcoInputs:
    return PlcoInputs(
        age=q.age, race=q.race, education=q.education, bmi=q.bmi, copd=q.copd,
        personal_cancer_history=q.personal_cancer_history,
        family_history_lung_cancer=q.family_history_lung_cancer,
        current_smoker=q.smoking_status == "current",
        cigs_per_day=q.cigs_per_day, smoking_years=q.smoking_years,
        quit_years=0.0 if q.smoking_status == "current" else q.quit_years,
    )


def _direction(a: float, b: float, tol: float = 1e-4) -> str:
    if b < a - tol:
        return "lower"
    if b > a + tol:
        return "higher"
    return "similar"


def build_result(q: Questionnaire, xray: XrayInfo | None = None) -> dict:
    x = to_plco_inputs(q)
    p = risk_6y(x)
    sc = run_scenarios(x)
    scenarios: dict = {}
    for name, block in sc["scenarios"].items():
        scenarios[name] = {"label": block["label"]}
        for pt in block["points"]:
            scenarios[name][f"y{pt['year']}"] = {
                "risk_6y": pt["risk_6y"],
                "display": as_in_100(pt["risk_6y"]),
                "outside_validated_age": pt["outside_validated_age"],
            }
    # Directions are computed in code, never by the LLM. A choice (quit / increase)
    # is compared with "continue" at the same future year; "continue" itself is
    # compared with today. Comparing "quit now" with today would mix the effect
    # of quitting with the effect of getting older.
    last = f"y{YEARS[-1]}"
    directions = {}
    cont = scenarios.get("continue", {}).get(last)
    if cont:
        directions["continue"] = _direction(p, cont["risk_6y"])
        for name in ("quit_now", "increase"):
            if name in scenarios and last in scenarios[name]:
                directions[name] = _direction(cont["risk_6y"], scenarios[name][last]["risk_6y"])
    return {
        "schema_version": SCHEMA_VERSION,
        "language": q.language,
        "smoking_status": q.smoking_status,
        "plco": {
            "risk_6y": p,
            "display": as_in_100(p),
            "horizon_years": HORIZON_YEARS,
            "horizon_display": f"{HORIZON_YEARS} years" if q.language == "en" else f"{HORIZON_YEARS} ani",
            "outside_validated_age": not in_validated_age_range(q.age),
        },
        "scenarios": scenarios,
        "direction": directions,
        "xray": (xray or XrayInfo()).model_dump(),
    }


def allowed_markers(result: dict) -> dict[str, str]:
    """Map every marker the LLM may use to the text the program fills in."""
    m = {"plco.display": result["plco"]["display"],
         "plco.horizon": result["plco"]["horizon_display"]}
    for name, block in result["scenarios"].items():
        for key, val in block.items():
            if key.startswith("y"):
                m[f"scen.{name}.{key}"] = val["display"]
                yr = key[1:]
                m[f"scen.{name}.{key}.when"] = (f"in {yr} years" if result["language"] == "en"
                                                 else f"peste {yr} ani")
    xr = result["xray"]
    if xr["provided"] and xr["flagged"]:
        m["xray.flagged_list"] = ", ".join(xr["flagged"])
    return m
