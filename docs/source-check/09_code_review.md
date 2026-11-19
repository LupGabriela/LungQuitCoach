# Code review, 19 Nov 2026

Each problem was reproduced with a test before it was fixed (see commits 17-19).

| Problem | Evidence | Fix |
|---|---|---|
| Finding names from the request were pasted into the text after the verifier ran | "you are safe and cancer-free, no need to see a doctor" appeared in the explanation | only the 18 TorchXRayVision labels accepted (422 otherwise) |
| Impossible smoking histories accepted | age 50, smoked 45 y, quit 20 y -> 0.5 in 100 | years smoked + years since quitting <= age |
| `/xray` blocked the server | /health during scoring: max 379 ms (n=4); after: max 27 ms, median 1 ms (n=44) | plain `def` endpoint |
| Romanian numbers in English format | "2.2 in 100" in a Romanian sentence | "2,2 din 100" |
| Verifier false alarms / misses ('quite', 'not safe', 'you have questions about lung disease', 'will not get a diagnosis', Romanian 'mie'/'una', 'cancerul') | reproduced in tests | verifier v3 (four planned changes, committed before coding) |

Sources checked on 19 Nov 2026:
- FastAPI, "Concurrency and async / await": plain `def` path operations run in an external threadpool; `async def` runs directly. https://fastapi.tiangolo.com/async/
- Ollama, "Thinking": thinking is enabled by default in the CLI and API for supported models (Qwen 3 listed); `think` can be set on generate requests. https://docs.ollama.com/capabilities/thinking.md
- Ollama OpenAPI spec: `options.seed` ("Random seed used for reproducible outputs") and `options.temperature`. https://docs.ollama.com/openapi.yaml
- actions/checkout v6: Dependabot "Bumps actions/checkout from 5 to 6" PRs from 24 Nov 2025 (e.g. https://github.com/p4lang/PI/pull/626).
