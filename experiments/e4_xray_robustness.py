"""Experiment E4 (case study, small scale): how much do TorchXRayVision scores
change when the image quality is lowered?

Images: chest X-rays given on the command line (the case study uses the two
NIH ChestX-ray14 images shipped in the TorchXRayVision test folder).
Degradations follow the idea of common-corruption benchmarks (several types,
several strengths); the exact list and strengths are design choices.

Run: python -m experiments.e4_xray_robustness IMG1 IMG2 ...
Writes experiments/results/e4_scores.csv and e4_summary.json
"""
from __future__ import annotations

import io
import json
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

from app.imaging import xray

OUT = Path(__file__).parent / "results"
THRESHOLD = xray.FLAG_THRESHOLD


def jpeg(img: Image.Image, q: int) -> Image.Image:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=q)
    return Image.open(io.BytesIO(buf.getvalue())).convert("L")


def crop(img: Image.Image, keep: float) -> Image.Image:
    w, h = img.size
    cw, ch = int(w * keep), int(h * keep)
    left, top = (w - cw) // 2, (h - ch) // 2
    return img.crop((left, top, left + cw, top + ch))


def downup(img: Image.Image, f: float) -> Image.Image:
    w, h = img.size
    return img.resize((max(1, int(w * f)), max(1, int(h * f))), Image.BILINEAR).resize((w, h),
                                                                                       Image.BILINEAR)


DEGRADATIONS = {
    "jpeg_q75": lambda im: jpeg(im, 75), "jpeg_q50": lambda im: jpeg(im, 50),
    "jpeg_q25": lambda im: jpeg(im, 25), "jpeg_q10": lambda im: jpeg(im, 10),
    "rotate_5": lambda im: im.rotate(5, fillcolor=0), "rotate_10": lambda im: im.rotate(10, fillcolor=0),
    "rotate_15": lambda im: im.rotate(15, fillcolor=0),
    "crop_90": lambda im: crop(im, 0.9), "crop_80": lambda im: crop(im, 0.8),
    "bright_0.7": lambda im: ImageEnhance.Brightness(im).enhance(0.7),
    "bright_1.3": lambda im: ImageEnhance.Brightness(im).enhance(1.3),
    "contrast_0.7": lambda im: ImageEnhance.Contrast(im).enhance(0.7),
    "contrast_1.3": lambda im: ImageEnhance.Contrast(im).enhance(1.3),
    "blur_1": lambda im: im.filter(ImageFilter.GaussianBlur(1)),
    "blur_2": lambda im: im.filter(ImageFilter.GaussianBlur(2)),
    "blur_3": lambda im: im.filter(ImageFilter.GaussianBlur(3)),
    "downup_0.5": lambda im: downup(im, 0.5), "downup_0.25": lambda im: downup(im, 0.25),
}


def main(paths: list[str]) -> dict:
    rows, times = [], []
    summary: dict = {"images": [Path(p).name for p in paths], "threshold": THRESHOLD,
                     "per_degradation": {}}
    for p in paths:
        base_img = Image.open(p).convert("L")
        t0 = time.perf_counter()
        base = xray.scores(np.array(base_img))
        times.append(time.perf_counter() - t0)
        for name, fn in {"original": lambda im: im, **DEGRADATIONS}.items():
            img = fn(base_img)
            t0 = time.perf_counter()
            sc = xray.scores(np.array(img))
            times.append(time.perf_counter() - t0)
            for k, s in sc.items():
                rows.append({"image": Path(p).name, "degradation": name, "pathology": k,
                             "score": s, "base": base[k], "abs_change": abs(s - base[k]),
                             "crossed": int((s >= THRESHOLD) != (base[k] >= THRESHOLD))})
    for name in DEGRADATIONS:
        sub = [r for r in rows if r["degradation"] == name]
        summary["per_degradation"][name] = {
            "mean_abs_change": round(float(np.mean([r["abs_change"] for r in sub])), 4),
            "max_abs_change": round(float(np.max([r["abs_change"] for r in sub])), 4),
            "threshold_crossings": int(sum(r["crossed"] for r in sub)),
            "n_scores": len(sub),
        }
    orig = [r for r in rows if r["degradation"] == "original"]
    summary["original_identical"] = all(r["abs_change"] == 0 for r in orig)
    t = np.array(times[1:])  # first call includes model loading
    summary["timing_s"] = {"first_call_incl_load": round(times[0], 3),
                           "median": round(float(np.median(t)), 4),
                           "p95": round(float(np.percentile(t, 95)), 4), "n": int(t.size)}
    OUT.mkdir(exist_ok=True)
    import csv
    with open(OUT / "e4_scores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    (OUT / "e4_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    s = main(sys.argv[1:])
    print(json.dumps(s, indent=2))
