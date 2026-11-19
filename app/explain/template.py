"""Fixed fallback template. Built only from markers, so it always passes the
verifier (this is tested in tests/test_verifier.py)."""
from __future__ import annotations

# "quit_now" is compared with continuing to smoke (see app/result.py)
_DIR_EN = {"lower": "lower than if you keep smoking", "higher": "higher than if you keep smoking",
           "similar": "about the same as if you keep smoking"}
_DIR_RO = {"lower": "mai mic decât dacă ai continua", "higher": "mai mare decât dacă ai continua",
           "similar": "cam la fel ca dacă ai continua"}


def template_draft(result: dict) -> str:
    lang = result.get("language", "en")
    d = result.get("direction", {})
    sc = result["scenarios"]
    if lang == "ro":
        parts = ["Riscul estimat de cancer pulmonar în următorii {plco.horizon} este {plco.display}."]
        if "quit_now" in sc and "y5" in sc["quit_now"] and result.get("smoking_status") == "current":
            parts.append("Dacă renunți acum, riscul {plco.horizon_adj}, calculat din nou "
                         "{scen.quit_now.y5.when}, ar fi {scen.quit_now.y5}, adică "
                         + _DIR_RO[d.get("quit_now", "similar")] + ".")
        if "continue" in sc and "y5" in sc["continue"] and result.get("smoking_status") == "current":
            parts.append("Dacă continui, același risc {plco.horizon_adj}, calculat "
                         "{scen.continue.y5.when}, ar fi {scen.continue.y5}.")
        parts.append("Acestea sunt estimări ale unui model, nu un diagnostic.")
        return " ".join(parts)
    parts = ["Your estimated chance of lung cancer over the next {plco.horizon} is {plco.display}."]
    if "quit_now" in sc and "y5" in sc["quit_now"]:
        if result.get("smoking_status") == "current":
            parts.append("If you stop smoking now and your {plco.horizon_adj} chance is "
                         "calculated again {scen.quit_now.y5.when}, it would be {scen.quit_now.y5}, "
                         + _DIR_EN[d.get("quit_now", "similar")] + ".")
        else:
            parts.append("If you stay smoke-free and your {plco.horizon_adj} chance is "
                         "calculated again {scen.quit_now.y5.when}, it would be {scen.quit_now.y5}.")
    if "continue" in sc and "y5" in sc["continue"] and result.get("smoking_status") == "current":
        parts.append("If you keep smoking as now, that {plco.horizon_adj} chance, calculated "
                     "{scen.continue.y5.when}, would be {scen.continue.y5}.")
    if result["xray"].get("provided") and result["xray"].get("flagged"):
        parts.append("The computer model flagged these items on the X-ray: {xray.flagged_list}. "
                     "A doctor should look at the image.")
    parts.append("These are estimates from a model, not a diagnosis.")
    return " ".join(parts)
