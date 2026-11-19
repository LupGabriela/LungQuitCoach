"""Experiment E1 (case study, small scale): how well does the verifier detect
deliberate errors, compared with a simple number-matching check?

Run:  python -m experiments.e1_verifier --n 100 --seed 2026 --tag run3_v21
Writes experiments/results/e1_<tag>_texts.csv and e1_<tag>_summary.json
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
from pathlib import Path

import numpy as np
from scipy.stats import bootstrap

from app.explain.verifier import fill, verify
from experiments.baseline import baseline_check
from app.result import build_result
from experiments.cases import make_cases
from experiments.texts import DEV, ERROR_TYPES, TEST, TEST_B, correct_draft, inject

SPLITS = (("dev", DEV), ("test", TEST), ("test_b", TEST_B))

OUT = Path(__file__).parent / "results"
EXPECTED_RULE = {"number": "R1_number", "period": "R2_period", "unit": "R3_unit",
                 "direction": "R4_direction", "reassurance": "R5_reassurance",
                 "diagnosis": "R6_diagnosis", "finding": "R7_finding"}


def _finding_ok(op, result) -> bool:
    """Skip a finding injection whose term IS in the flagged list (then it is no error)."""
    if op[0] != "append":
        return True
    flagged = " ".join(result["xray"]["flagged"]).lower()
    words = set(re.findall(r"[a-z]+", op[1].lower()))
    return not any(w in flagged.split() for w in words if len(w) > 3)


def ci(x: list[int]) -> list[float]:
    arr = np.array(x, dtype=float)
    if arr.min() == arr.max():
        return [float(arr.mean()), float(arr.mean())]
    r = bootstrap((arr,), np.mean, n_resamples=2000, method="percentile",
                  random_state=np.random.default_rng(0))
    return [round(float(r.confidence_interval.low), 3), round(float(r.confidence_interval.high), 3)]


def main(n: int, seed: int, tag: str = "latest") -> dict:
    rng = random.Random(seed)
    rows = []
    for i, (q, xr) in enumerate(make_cases(n, seed)):
        res = build_result(q, xr)
        good = correct_draft(res, rng)
        rows.append(dict(case=i, split="correct", error_type="none", op="", draft=good, result=res))
        for et in ERROR_TYPES:
            for split, pool in SPLITS:
                ops = [op for op in pool[et] if et != "finding" or _finding_ok(op, res)]
                op = rng.choice(ops)
                rows.append(dict(case=i, split=split, error_type=et, op=" / ".join(op[1:]) or op[0],
                                 draft=inject(good, op), result=res))

    for r in rows:
        v = verify(r["draft"], r["result"])
        r["verifier_rules"] = sorted({x.rule for x in v})
        r["verifier_flag"] = int(bool(v))
        r["baseline_flag"] = int(bool(baseline_check(fill(r["draft"], r["result"]), r["result"])))
        r["expected_rule_hit"] = (int(EXPECTED_RULE[r["error_type"]] in r["verifier_rules"])
                                  if r["error_type"] != "none" else None)

    summary: dict = {"n_cases": n, "seed": seed, "n_texts": len(rows), "per_type": {}}
    correct = [r for r in rows if r["split"] == "correct"]
    summary["false_alarm_rate"] = {
        "verifier": round(sum(r["verifier_flag"] for r in correct) / len(correct), 3),
        "baseline": round(sum(r["baseline_flag"] for r in correct) / len(correct), 3)}
    summary["false_alarm_examples"] = [
        {"draft": r["draft"], "rules": r["verifier_rules"]} for r in correct if r["verifier_flag"]][:5]
    for split, _ in SPLITS:
        for et in ERROR_TYPES:
            sub = [r for r in rows if r["split"] == split and r["error_type"] == et]
            vf = [r["verifier_flag"] for r in sub]
            bf = [r["baseline_flag"] for r in sub]
            summary["per_type"][f"{split}:{et}"] = {
                "n": len(sub),
                "verifier_recall": round(float(np.mean(vf)), 3), "verifier_ci95": ci(vf),
                "expected_rule_hit": round(float(np.mean([r["expected_rule_hit"] for r in sub])), 3),
                "baseline_recall": round(float(np.mean(bf)), 3), "baseline_ci95": ci(bf),
                "missed_by_variant": {o: sum(1 for r in sub if r["op"] == o and not r["verifier_flag"])
                                      for o in sorted({r["op"] for r in sub})
                                      if any(r["op"] == o and not r["verifier_flag"] for r in sub)},
            }
    for split, _ in SPLITS:
        err = [r for r in rows if r["split"] == split]
        for who in ("verifier", "baseline"):
            tp = sum(r[f"{who}_flag"] for r in err)
            fp = sum(r[f"{who}_flag"] for r in correct)
            fn = len(err) - tp
            prec = tp / (tp + fp) if tp + fp else 0.0
            rec = tp / len(err)
            f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
            summary[f"overall_{split}_{who}"] = {"tp": tp, "fp": fp, "fn": fn,
                                                 "precision": round(prec, 3),
                                                 "recall": round(rec, 3), "f1": round(f1, 3)}
    OUT.mkdir(exist_ok=True)
    with open(OUT / f"e1_{tag}_texts.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case", "split", "error_type", "injected", "verifier_flag", "verifier_rules",
                    "baseline_flag", "draft"])
        for r in rows:
            w.writerow([r["case"], r["split"], r["error_type"], r["op"], r["verifier_flag"],
                        "|".join(r["verifier_rules"]), r["baseline_flag"], r["draft"]])
    (OUT / f"e1_{tag}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--tag", default="latest")
    a = ap.parse_args()
    s = main(a.n, a.seed, a.tag)
    print(json.dumps({k: v for k, v in s.items() if k != "per_type"}, indent=2))
    for k, v in s["per_type"].items():
        print(f"{k:22s} verifier={v['verifier_recall']:.2f} {v['verifier_ci95']} "
              f"rule={v['expected_rule_hit']:.2f} baseline={v['baseline_recall']:.2f}")
