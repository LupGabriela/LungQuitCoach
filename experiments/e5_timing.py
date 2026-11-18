"""Experiment E5 (case study): run time of the non-image pipeline, and readability
of the fallback template texts (English only; textstat has no validated
Romanian formula).

Run: python -m experiments.e5_timing --n 100
"""
from __future__ import annotations

import argparse
import json
import time
import tracemalloc
from pathlib import Path

import numpy as np
import textstat
from fastapi.testclient import TestClient

from app.explain.pipeline import explain
from app.explain.verifier import verify
from app.explain.template import template_draft
from app.main import app
from app.result import build_result
from experiments.cases import make_cases

OUT = Path(__file__).parent / "results"


def stats(xs):
    a = np.array(xs) * 1000
    return {"median_ms": round(float(np.median(a)), 3), "p95_ms": round(float(np.percentile(a, 95)), 3),
            "n": int(a.size)}


def main(n: int) -> dict:
    cases = make_cases(n, seed=7)
    t_core, t_api, fk, fre, words, verified = [], [], [], [], [], 0
    tracemalloc.start()
    for q, xr in cases:
        t0 = time.perf_counter()
        res = build_result(q, xr)
        exp = explain(res, None)  # template path (no LLM in the case study)
        t_core.append(time.perf_counter() - t0)
        verified += int(verify(template_draft(res), res) == [])
        fk.append(textstat.flesch_kincaid_grade(exp.text))
        fre.append(textstat.flesch_reading_ease(exp.text))
        words.append(len(exp.text.split()))
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    client = TestClient(app)
    for q, xr in cases:
        body = {"questionnaire": q.model_dump(), "xray": xr.model_dump()}
        t0 = time.perf_counter()
        r = client.post("/explain", json=body)
        t_api.append(time.perf_counter() - t0)
        assert r.status_code == 200
    s = {"n_cases": n,
         "core_pipeline": stats(t_core), "api_round_trip": stats(t_api),
         "peak_python_memory_mb": round(peak / 1e6, 2),
         "template_passes_verifier": f"{verified}/{n}",
         "template_readability_en": {
             "flesch_kincaid_grade_median": round(float(np.median(fk)), 1),
             "flesch_kincaid_grade_range": [round(min(fk), 1), round(max(fk), 1)],
             "flesch_reading_ease_median": round(float(np.median(fre)), 1),
             "words_median": int(np.median(words))}}
    OUT.mkdir(exist_ok=True)
    (OUT / "e5_summary.json").write_text(json.dumps(s, indent=2))
    return s


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    print(json.dumps(main(ap.parse_args().n), indent=2))
