# Lung Health & Quit Coach — research prototype (Lab 5–8 subset)

Bachelor thesis prototype, Babeș-Bolyai University, Faculty of Mathematics and Computer Science.
**Research prototype, not a medical device. It gives no diagnosis.** It is tested only on
fictional cases and public, de-identified images.

## What this subset does

| Module | File | Status |
|---|---|---|
| PLCOm2012 6-year lung cancer risk (Tammemägi et al., NEJM 2013) | `app/risk/plcom2012.py` | done, unit-tested against the published worked example |
| Scenario engine: quit now / continue / increase at 3, 5, 7 years | `app/risk/scenarios.py` | done |
| Structured result (data contract) | `app/schemas.py`, `app/result.py` | done |
| Explanation pipeline: markers → verifier → one retry → fixed template | `app/explain/` | done (LLM client for Ollama included; not run in CI) |
| Chest X-ray scores (TorchXRayVision DenseNet-121 "all") | `app/imaging/xray.py` | done, optional dependency |
| REST API (`/health`, `/risk`, `/explain`, `/xray`) | `app/main.py` | done |
| Case-study experiments E1, E4, E5 | `experiments/` | done on initial data |

## Run locally (Windows + WSL2, Linux or macOS)

```bash
python -m venv .venv && source .venv/bin/activate      # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m pytest                                         # 56 tests
uvicorn app.main:app --reload                            # open http://localhost:8000/docs
```

Optional X-ray module (CPU only):

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements-xray.txt
```

Optional local LLM: install Ollama, run `ollama pull qwen3:4b`, then start the API with
`LLM_BACKEND=ollama`. Without it the API always uses the checked template.

## Experiments (case study)

```bash
python -m experiments.e1_verifier --n 100 --seed 2026 --tag run4b_v3  # verifier vs baseline
python -m experiments.e4_xray_robustness IMG1.png IMG2.png # score change under 18 degradations
python -m experiments.e5_timing --n 100                    # run time + template readability
```

Results are written to `experiments/results/`. All E1 runs are kept on purpose: run 1 used
verifier v1, runs 2–3 v2 / v2.1, run 4a v2.1 on the new unseen sets (test_c, correct_b), and
run 4b verifier v3 (see the git log for what changed and why).

The two X-ray images used in E4 are NIH ChestX-ray14 images shipped in the TorchXRayVision
repository's `tests/` folder (`00000001_000.png`, `00027426_000.png`). Copy them into
`experiments/data/` (this folder is not committed).

## Docker

```bash
docker build -t lung-quit-coach .
docker run -p 8000:8000 lung-quit-coach
# or
docker compose up --build
```

## Continuous integration

`.github/workflows/ci.yml` runs the tests and a small E1 experiment on every push, then builds the
Docker image and smoke-tests the container.

## Deployment plan (summary)

1. **Local install** (main mode, also for the defence demo): clone, create the venv, run
   `uvicorn`, or run the Docker image. Works offline.
2. **Public demo server**: a small Linux VM (for example from the Azure for Students credit) with
   Docker Compose; a reverse proxy with automatic HTTPS (Caddy) in front of port 8000; a DNS name
   pointing at the VM. Only fictional demo cases; no data is stored.

## Licences of reused material

- TorchXRayVision: Apache-2.0 (main library; model weights have their own terms).
- BodyParts3D (planned 3D lung model): CC BY 4.0, credit "BodyParts3D, © The Database Center for
  Life Science licensed under CC Attribution 4.0 International".
