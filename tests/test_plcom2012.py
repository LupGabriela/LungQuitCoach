import math

import pytest

from app.risk.plcom2012 import CONSTANT, PlcoInputs, as_in_100, in_validated_age_range, risk_6y


def base(**kw):
    d = dict(age=62, race="white", education=4, bmi=27, copd=False, personal_cancer_history=False,
             family_history_lung_cancer=False, current_smoker=False, cigs_per_day=80,
             smoking_years=27, quit_years=10)
    d.update(kw)
    return PlcoInputs(**d)


def test_worked_example_resplab():
    # Worked example of the resplab/PLCOm2012 package README:
    # 62-year-old white former smoker, education 4, BMI 27, 80 cig/day,
    # 27 years smoked, quit 10 years ago -> 0.01750922
    assert risk_6y(base()) == pytest.approx(0.01750922, abs=1e-8)


def test_all_centering_values_give_constant():
    x = base(cigs_per_day=10 / 0.4021541613)
    assert risk_6y(x) == pytest.approx(math.exp(CONSTANT) / (1 + math.exp(CONSTANT)), abs=1e-12)


def test_monotonic_directions():
    assert risk_6y(base(age=70)) > risk_6y(base(age=60))
    assert risk_6y(base(copd=True)) > risk_6y(base())
    assert risk_6y(base(family_history_lung_cancer=True)) > risk_6y(base())
    assert risk_6y(base(quit_years=20)) < risk_6y(base(quit_years=5))
    assert risk_6y(base(smoking_years=40)) > risk_6y(base(smoking_years=20))


def test_current_smoker_higher_than_former_same_history():
    cur = base(current_smoker=True, quit_years=0)
    former = base(current_smoker=False, quit_years=0)
    assert risk_6y(cur) > risk_6y(former)


@pytest.mark.parametrize("kw", [dict(cigs_per_day=0), dict(education=7), dict(race="martian"),
                                dict(age=-1), dict(current_smoker=True, quit_years=3)])
def test_invalid_inputs_rejected(kw):
    with pytest.raises(ValueError):
        risk_6y(base(**kw))


def test_age_range_and_display():
    assert in_validated_age_range(55) and in_validated_age_range(74)
    assert not in_validated_age_range(54) and not in_validated_age_range(75)
    assert as_in_100(0.01750922) == "1.8 in 100"
    assert as_in_100(0.01750922, "ro") == "1,8 din 100"
