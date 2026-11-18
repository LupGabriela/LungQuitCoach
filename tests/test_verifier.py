import pytest

from app.explain.pipeline import explain
from app.explain.llm_client import FakeLLM
from app.explain.template import template_draft
from app.explain.verifier import baseline_check, fill, verify
from app.result import build_result
from app.schemas import Questionnaire, XrayInfo


@pytest.fixture
def result():
    q = Questionnaire(age=60, education=3, bmi=26, smoking_status="current", cigs_per_day=20,
                      smoking_years=40)
    return build_result(q)


@pytest.fixture
def result_xray():
    q = Questionnaire(age=60, education=3, bmi=26, smoking_status="current", cigs_per_day=20,
                      smoking_years=40)
    return build_result(q, XrayInfo(provided=True, flagged=["Emphysema"], not_flagged=["Mass"]))


GOOD = ("Your chance of lung cancer over the next {plco.horizon} is {plco.display}. "
        "If you stop smoking now, the chance {scen.quit_now.y5.when} would be lower: "
        "{scen.quit_now.y5}. If you keep smoking, it would rise to {scen.continue.y5} "
        "{scen.continue.y5.when}. This is an estimate, not a diagnosis.")


def rules(draft, res):
    return {v.rule for v in verify(draft, res)}


def test_good_draft_passes(result):
    assert verify(GOOD, result) == []


@pytest.mark.parametrize("draft,rule", [
    ("Your chance over the next {plco.horizon} is 2%.", "R1_number"),
    ("Your chance over the next {plco.horizon} is about two in a hundred.", "R1_number"),
    ("Your lifetime chance is {plco.display}, over {plco.horizon}.", "R2_period"),
    ("Your chance is {plco.display}.", "R2_period"),
    ("Your chance over the next {plco.horizon} is {plco.display} percent.", "R3_unit"),
    ("If you stop smoking now, your risk will go up.", "R4_direction"),
    ("If you keep smoking, your risk will drop.", "R4_direction"),
    ("You are safe.", "R5_reassurance"),
    ("There is no risk for you.", "R5_reassurance"),
    ("You have lung cancer.", "R6_diagnosis"),
    ("The X-ray also shows a nodule.", "R7_finding"),
    ("See {plco.lifetime}.", "R0_unknown_marker"),
])
def test_each_rule_fires(result, draft, rule):
    assert rule in rules(draft, result)


def test_negation_flips_direction(result):
    assert "R4_direction" not in rules("If you stop smoking, your risk will not go up.", result)


def test_finding_allowed_when_flagged(result_xray):
    assert "R7_finding" not in rules("The model flagged emphysema on the X-ray.", result_xray)


def test_template_always_passes(result, result_xray):
    assert verify(template_draft(result), result) == []
    assert verify(template_draft(result_xray), result_xray) == []


def test_fill_replaces_markers(result):
    text = fill(GOOD, result)
    assert "{" not in text and result["plco"]["display"] in text


def test_baseline_catches_wrong_number_but_not_reassurance(result):
    assert baseline_check("Your risk is 37 in 100.", result)
    assert baseline_check(fill("You are safe. Risk: {plco.display}.", result), result) == []


def test_pipeline_retry_then_success(result):
    llm = FakeLLM(["You are safe.", GOOD])
    exp = explain(result, llm)
    assert exp.source == "llm" and exp.attempts == 2


def test_pipeline_falls_back_to_template(result):
    llm = FakeLLM(["You are safe.", "You have lung cancer."])
    exp = explain(result, llm)
    assert exp.source == "template" and exp.attempts == 2 and exp.violations


def test_pipeline_without_llm_uses_template(result):
    exp = explain(result, None)
    assert exp.source == "template" and exp.attempts == 0


def test_romanian_rules():
    q = Questionnaire(age=60, education=3, bmi=26, smoking_status="current", cigs_per_day=20,
                      smoking_years=40, language="ro")
    res = build_result(q)
    assert verify(template_draft(res), res) == []
    assert "R5_reassurance" in rules("Sunteți în siguranță.", res)
    assert "R1_number" in rules("Riscul este de doi la sută în {plco.horizon}.", res)
