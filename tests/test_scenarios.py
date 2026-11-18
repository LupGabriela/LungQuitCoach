from app.risk.plcom2012 import PlcoInputs, risk_6y
from app.risk.scenarios import INCREASE_FACTOR, project, run_scenarios


def smoker(**kw):
    d = dict(age=60, race="white", education=3, bmi=26, copd=False, personal_cancer_history=False,
             family_history_lung_cancer=False, current_smoker=True, cigs_per_day=20,
             smoking_years=40, quit_years=0)
    d.update(kw)
    return PlcoInputs(**d)


def test_projection_moves_inputs_forward():
    x = smoker()
    c = project(x, "continue", 5)
    assert c.age == 65 and c.smoking_years == 45 and c.current_smoker
    q = project(x, "quit_now", 5)
    assert q.age == 65 and q.smoking_years == 40 and not q.current_smoker and q.quit_years == 5
    i = project(x, "increase", 5)
    expected = (20 * 40 + 20 * INCREASE_FACTOR * 5) / 45
    assert abs(i.cigs_per_day - expected) < 1e-9 and i.smoking_years == 45


def test_scenarios_are_not_identical():
    # Regression test for the bug found in the feasibility review:
    # all scenarios used to give identical values.
    out = run_scenarios(smoker())
    s = out["scenarios"]
    for i in range(3):
        q = s["quit_now"]["points"][i]["risk_6y"]
        c = s["continue"]["points"][i]["risk_6y"]
        inc = s["increase"]["points"][i]["risk_6y"]
        assert q < c < inc


def test_continue_rises_over_time():
    pts = run_scenarios(smoker())["scenarios"]["continue"]["points"]
    assert pts[0]["risk_6y"] < pts[1]["risk_6y"] < pts[2]["risk_6y"]
    assert pts[0]["risk_6y"] > risk_6y(smoker())


def test_former_smoker_has_no_increase_scenario():
    x = smoker(current_smoker=False, quit_years=8)
    out = run_scenarios(x)
    assert "increase" not in out["scenarios"]
    assert project(x, "increase", 3) is None


def test_age_outside_validated_range_is_flagged():
    pts = run_scenarios(smoker(age=70))["scenarios"]["continue"]["points"]
    # ages 73, 75, 77 -> only 75 and 77 are outside 55-74
    assert [p["outside_validated_age"] for p in pts] == [False, True, True]
