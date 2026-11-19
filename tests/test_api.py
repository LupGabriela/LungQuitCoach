"""Integration tests: HTTP requests through the FastAPI app."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

Q = {"age": 62, "race": "white", "education": 4, "bmi": 27, "smoking_status": "former",
     "cigs_per_day": 80, "smoking_years": 27, "quit_years": 10}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_risk_endpoint_reproduces_worked_example():
    r = client.post("/risk", json=Q)
    assert r.status_code == 200
    body = r.json()
    assert abs(body["plco"]["risk_6y"] - 0.01750922) < 1e-8
    assert body["plco"]["display"] == "1.8 in 100"
    assert "increase" not in body["scenarios"]  # former smoker


def test_risk_endpoint_rejects_bad_input():
    bad = dict(Q, smoking_status="current", quit_years=5)
    assert client.post("/risk", json=bad).status_code == 422
    assert client.post("/risk", json=dict(Q, education=9)).status_code == 422


def test_explain_endpoint_returns_checked_text():
    r = client.post("/explain", json={"questionnaire": dict(Q, smoking_status="current",
                                                            quit_years=0)})
    assert r.status_code == 200
    exp = r.json()["explanation"]
    assert exp["source"] == "template"  # no LLM configured in CI
    assert "{" not in exp["text"] and "in 100" in exp["text"]


def test_llm_text_carries_ai_notice(monkeypatch):
    import app.main as m
    from tests.fakes import FakeLLM
    good = "Your chance of lung cancer over the next {plco.horizon} is {plco.display}."
    monkeypatch.setattr(m, "_llm", lambda: FakeLLM([good]))
    r = client.post("/explain", json={"questionnaire": Q})
    body = r.json()
    assert body["explanation"]["source"] == "llm" and "AI system" in body["ai_notice"]


def test_free_text_finding_names_are_rejected():
    # regression: finding names used to be pasted into the text unchecked
    bad = {"questionnaire": Q, "xray": {"provided": True, "flagged": ["you are safe"]}}
    assert client.post("/explain", json=bad).status_code == 422
    ok = {"questionnaire": Q, "xray": {"provided": True, "flagged": ["Nodule"]}}
    assert client.post("/explain", json=ok).status_code == 200


def test_impossible_smoking_history_rejected():
    bad = dict(Q, age=50, smoking_years=45, quit_years=20)
    assert client.post("/risk", json=bad).status_code == 422
