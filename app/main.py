"""FastAPI application (research prototype, not a medical device)."""
from __future__ import annotations

import io
import os
import time

from fastapi import FastAPI, File, HTTPException, UploadFile

from .explain.llm_client import OllamaLLM
from .explain.pipeline import explain
from .imaging import xray
from .result import build_result
from .schemas import ExplainRequest, Questionnaire, XrayInfo

AI_NOTICE = ("This explanation was written by an AI system from your numbers and checked "
             "automatically. It is not a diagnosis.")

app = FastAPI(title="Lung Health & Quit Coach (research prototype)", version="0.1.0")


def _llm():
    """Use a local Ollama model only if LLM_BACKEND=ollama; otherwise template only."""
    if os.environ.get("LLM_BACKEND") == "ollama":
        return OllamaLLM(model=os.environ.get("OLLAMA_MODEL", "qwen3:4b"))
    return None


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "xray_available": xray.available(),
            "llm_backend": os.environ.get("LLM_BACKEND", "template")}


@app.post("/risk")
def risk(q: Questionnaire) -> dict:
    return build_result(q)


@app.post("/explain")
def explain_endpoint(req: ExplainRequest) -> dict:
    t0 = time.perf_counter()
    result = build_result(req.questionnaire, req.xray)
    exp = explain(result, _llm())
    body = {"result": result, "explanation": exp.model_dump(),
            "notice": "Research prototype. Illustration and estimates only, not a diagnosis.",
            "elapsed_ms": round((time.perf_counter() - t0) * 1000, 1)}
    # AI Act Art. 50: tell the reader when a text was written by an AI system
    if exp.source == "llm":
        body["ai_notice"] = AI_NOTICE
    return body


@app.post("/xray")
async def xray_endpoint(file: UploadFile = File(...)) -> dict:
    if not xray.available():
        raise HTTPException(status_code=503, detail="TorchXRayVision is not installed")
    from PIL import Image
    import numpy as np
    data = await file.read()
    try:
        img = np.array(Image.open(io.BytesIO(data)).convert("L"))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="not a readable image") from exc
    sc = xray.scores(img)
    yes, no = xray.flagged(sc)
    return {"scores": sc, "xray": XrayInfo(provided=True, flagged=yes, not_flagged=no).model_dump(),
            "note": "Scores, not probabilities. Not a diagnosis."}
