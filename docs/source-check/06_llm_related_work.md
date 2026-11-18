# 06 — Related work for the LLM explanation layer (verified sources only)

Thesis: *Lung Health & Quit Coach* (UBB, licență). Contribution under comparison:
(1) the LLM never writes numbers, it writes placeholders such as `{plco.display}` that code fills from a structured result;
(2) a rule-based verifier checks every text (no stray digits or number words, correct time horizon and units, correct direction such as "quitting never raises risk", no forbidden phrases such as "safe", "no risk" or "you have cancer", no findings missing from the input; English and Romanian);
(3) one retry, then a fixed template fallback.
Experiments: verifier precision/recall on injected errors; error rates of Qwen3-4B (Ollama) and API LLMs with vs without the verifier; a user comprehension study vs template + icon array.

**Verification rule used here.** Each entry below was checked on a page fetched on 2026-11-18 (URL given). Citation fields come from that page. Method and results are paraphrased from the fetched abstract or full text; any number given was read on the fetched page. Fields the page did not show are marked "not shown". Nothing was filled in from memory. Note: direct `api.crossref.org/works/<DOI>` lookups were blocked by this session's network allowlist except one (Reuland 2018, see "not confirmed"), so citation data comes from ACL Anthology, arXiv, NeurIPS proceedings, publisher or repository pages instead.

---

## A. Hallucination detection and verification

### A1. FActScore
- **Citation:** Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Koh, Mohit Iyyer, Luke Zettlemoyer, Hannaneh Hajishirzi. 2023. *FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation.* In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP 2023), pp. 12076–12100, Singapore. ACL. DOI: 10.18653/v1/2023.emnlp-main.741
- **URL fetched:** https://aclanthology.org/2023.emnlp-main.741
- **Method:** A generation is split into atomic facts, and the score is the share of those facts that a knowledge source (Wikipedia for biographies) supports. An automatic estimator uses retrieval plus a strong LM to approximate the human-annotated score.
- **Reported results:** In human evaluation, ChatGPT reached only 58% factual precision on biographies. The automatic estimator's error rate is below 2%. It was applied to 6,500 generations from 13 LMs, and the authors estimate the same human evaluation would have cost about $26K.
- **Similarity:** Breaks a text into checkable claims, as the thesis verifier checks each statement (direction, horizon, findings).
- **Difference:** FActScore checks open-world facts against a knowledge source and needs an LLM plus retrieval. The thesis checks a closed world (the structured result is the only truth) with deterministic rules and never lets the model produce numbers.
- **Comparable thesis metric:** % of unsupported content per output, i.e. "findings absent from input" rate with vs without verifier.

### A2. SelfCheckGPT
- **Citation:** Potsawee Manakul, Adian Liusie, Mark Gales. 2023. *SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models.* In Proceedings of EMNLP 2023, pp. 9004–9017, Singapore. ACL. DOI: 10.18653/v1/2023.emnlp-main.557
- **URLs fetched:** https://aclanthology.org/2023.emnlp-main.557 (citation, abstract); https://ar5iv.labs.arxiv.org/html/2303.08896 (Table 2 numbers)
- **Method:** Samples several responses to the same prompt and scores each sentence by how consistent it is with the other samples (BERTScore, QA, n-gram, NLI or prompting variants). Needs no external database and no access to token probabilities.
- **Reported results:** The dataset is 238 GPT-3 WikiBio passages (1,908 sentences). Sentence-level AUC-PR for non-factual sentences was 93.42 for the Prompt variant and 92.50 for NLI, vs 83.21 for the grey-box GPT-3 avg(−log p) baseline and 72.96 for random. Passage-level Pearson correlation was 78.32 (Prompt) vs 57.04 (grey-box baseline).
- **Similarity:** A post-hoc detector that flags bad sentences before they reach the user.
- **Difference:** Probabilistic, costs N extra LLM calls, and gives only a score, not a reason. The thesis verifier is deterministic, costs no LLM calls, works on one sample and returns a named violation (e.g. `DIRECTION_ERROR`) that drives the retry.
- **Comparable thesis metric:** Detection precision/recall (and AUC-PR if a score is produced) on the injected-error set. SelfCheckGPT could also serve as a baseline detector on the same set.

### A3. Chain-of-Verification (CoVe)
- **Citation:** Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu, Roberta Raileanu, Xian Li, Asli Celikyilmaz, Jason Weston. 2024. *Chain-of-Verification Reduces Hallucination in Large Language Models.* In Findings of the Association for Computational Linguistics: ACL 2024, pp. 3563–3578. ACL. DOI: 10.18653/v1/2024.findings-acl.212 — **venue confirmed as Findings of ACL 2024.**
- **URLs fetched:** https://aclanthology.org/2024.findings-acl.212 ; https://arxiv.org/pdf/2309.11495 (numbers)
- **Method:** The model (1) drafts an answer, (2) plans verification questions, (3) answers them independently so the draft does not bias the answers, and (4) writes a final verified answer.
- **Reported results (Llama 65B):** Precision on Wikidata list questions rose from 0.17 (few-shot) to 0.36 (two-step CoVe). Closed-book MultiSpanQA F1 rose from 0.39 to 0.48 (factored). FActScore on long-form biographies rose from 55.9 to 71.4 (factor+revise).
- **Similarity:** Verify, then revise. This matches the thesis "verify, then retry once" loop.
- **Difference:** In CoVe the verifier is the same LLM, so errors can be correlated. The thesis verifier is external and rule-based, and the fallback is a fixed template instead of more LLM revision.
- **Comparable thesis metric:** Relative reduction in % of outputs with errors (baseline vs with-verifier pipeline).

### A4. RARR
- **Citation:** Luyu Gao, Zhuyun Dai, Panupong Pasupat, Anthony Chen, Arun Tejasvi Chaganty, Yicheng Fan, Vincent Zhao, Ni Lao, Hongrae Lee, Da-Cheng Juan, Kelvin Guu. 2023. *RARR: Researching and Revising What Language Models Say, Using Language Models.* In Proceedings of the 61st Annual Meeting of the ACL (Volume 1: Long Papers), pp. 16477–16508, Toronto. ACL. DOI: 10.18653/v1/2023.acl-long.910 — **venue confirmed as ACL 2023 long.**
- **URL fetched:** https://aclanthology.org/2023.acl-long.910
- **Method:** Post-hoc system for any generator's output. It searches the web for evidence, then edits unsupported content while changing the original text as little as possible. Needs only a few examples, an LLM and web search.
- **Reported results (abstract):** Attribution improves significantly over several state-of-the-art LMs and tasks, and the original text is preserved much better than with earlier edit models. Exact figures were not extracted (not shown on the abstract page).
- **Similarity:** Post-generation repair aimed at grounding; keeps the original intent.
- **Difference:** Open-domain web evidence and LLM editing, vs the thesis's closed structured input, rule checks and deterministic template fallback.
- **Comparable thesis metric:** Error rate after repair; also the thesis "retry success rate" (share of failing outputs fixed by the single retry).

## B. Grounding

### B1. Retrieval-Augmented Generation (RAG)
- **Citation:** Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela. 2020. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* Advances in Neural Information Processing Systems 33 (NeurIPS 2020), pp. 9459–9474.
- **URL fetched:** https://papers.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html
- **Method:** Combines a pretrained seq2seq generator (parametric memory) with a dense Wikipedia index that a neural retriever searches (non-parametric memory). Two variants: the same passages for the whole output, or different passages per token.
- **Reported results (abstract):** State of the art on three open-domain QA tasks. Generated text is more specific, diverse and factual than a parametric-only seq2seq baseline.
- **Similarity:** The output is conditioned on external evidence instead of model memory.
- **Difference:** RAG grounds by putting text in the context, so the model can still copy numbers wrongly. The thesis grounds by construction: numbers never pass through the model (placeholders filled by code), and the "evidence" is one structured result, not retrieved passages.
- **Comparable thesis metric:** Conceptual baseline ("give the LLM the numbers in the prompt") vs the placeholder design: % of outputs with numeric errors.

## C. Guardrail frameworks

### C1. NeMo Guardrails
- **Citation:** Traian Rebedea, Razvan Dinu, Makesh Narsimhan Sreedhar, Christopher Parisien, Jonathan Cohen. 2023. *NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails.* In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, pp. 431–445, Singapore. ACL. DOI: 10.18653/v1/2023.emnlp-demo.40 — **venue confirmed (EMNLP 2023 System Demonstrations).**
- **URLs fetched:** https://aclanthology.org/2023.emnlp-demo.40 ; https://arxiv.org/pdf/2310.10501 (details, numbers)
- **Method:** Open-source runtime, inspired by dialogue management, that applies programmable "rails" independently of the LLM. Rails are written in Colang, a language that mixes English with Python-like syntax. The paper describes topical rails (dialogue flow) and execution rails (Python actions) for fact-checking, hallucination checks (agreement across sampled answers) and input/output moderation.
- **Reported results (paper):** With input and output moderation, gpt-3.5-turbo blocked about 99% of harmful prompts and 2% of helpful ones (200-sample set). The fact-checking rail reached about 80% accuracy on MS MARCO. The hallucination rail caught 70% of 20 false-premise prompts for text-davinci-003; the gpt-3.5-turbo figure is reported inconsistently between main text and appendix.
- **Similarity:** An output-checking layer separate from the model, with block/redo behaviour.
- **Difference:** Its checks are mostly LLM-based (self-check prompts, sampling). The thesis checks are deterministic, specific to the domain (horizon, units, risk direction, banned medical claims) and bilingual EN/RO.
- **Comparable thesis metric:** Block rate on bad outputs (recall) vs false-block rate on good outputs (1 − precision). The thesis can report the same pair.

### C2. Guardrails AI (open-source framework)
- **Citation:** Guardrails AI. *guardrails* (Python framework), GitHub repository, Apache-2.0 licence. Accessed 2026-11-18.
- **URLs fetched:** https://github.com/guardrails-ai/guardrails ; https://guardrailsai.com/guardrails/docs/concepts/validators.md
- **Method:** A `Guard` combines validators that run on inputs or outputs. A validator returns `PassResult` or `FailResult`, and on failure applies a configurable `on_fail` policy (the README examples use `OnFailAction.EXCEPTION`; the full list is on a separate "On-Fail Policies" page that was not fetched). Validators come from the Guardrails Hub. Ones named on the fetched pages: `RegexMatch`, `CompetitorCheck`, `ToxicLanguage`, `ProvenanceLLM`, `DetectPII`, `ExtractedSummarySentencesMatch`. It also supports Pydantic-schema structured output (`Guard.for_pydantic`). The README says validators are moving to standard PyPI packages and hosted remote inference was planned to end on 25 Aug 2026.
- **Reported results:** None (software, no evaluation).
- **Similarity:** Closest engineering analogue. The thesis verifier is in effect a set of custom validators with a "reask once, then fallback" policy.
- **Difference:** Generic validators (regex, toxicity, PII). The thesis adds domain-specific semantic checks (risk direction under quitting, time horizon and unit consistency against the structured result, forbidden medical reassurance) and Romanian support, and is evaluated with injected-error precision/recall.
- **Comparable thesis metric:** None reported by the tool. Could serve as an implementation baseline (e.g. `RegexMatch` for digits only) to show what the domain rules add.

### C3. Llama Guard
- **Citation:** Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, Madian Khabsa. 2023. *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations.* arXiv:2312.06674 (v1, 7 Dec 2023). **No journal or conference listed on the arXiv page, so cite as an arXiv preprint (confirmed).**
- **URL fetched:** https://arxiv.org/abs/2312.06674v1
- **Method:** Llama2-7b instruction-tuned on a small dataset to classify both prompts and responses against a safety-risk taxonomy. The taxonomy can be changed through zero- or few-shot prompting.
- **Reported results (abstract):** Matches or beats existing moderation tools on the OpenAI Moderation Evaluation dataset and ToxicChat.
- **Similarity:** Classifies outputs before they are shown.
- **Difference:** Targets general harm categories (violence, etc.), not factual or numeric fidelity to a medical result. It is itself an LLM, whereas the thesis verifier is deterministic and explainable.
- **Comparable thesis metric:** Classifier precision/recall/F1 (same metric family as the verifier evaluation).

## D. Medical hallucination benchmarks and error rates in patient-facing text

### D1. Med-HALT
- **Citation:** Ankit Pal, Logesh Kumar Umapathi, Malaikannan Sankarasubbu. 2023. *Med-HALT: Medical Domain Hallucination Test for Large Language Models.* In Proceedings of the 27th Conference on Computational Natural Language Learning (CoNLL 2023), pp. 314–334, Singapore. ACL. DOI: 10.18653/v1/2023.conll-1.21 — **venue confirmed (CoNLL 2023).**
- **URLs fetched:** https://aclanthology.org/2023.conll-1.21 ; https://arxiv.org/abs/2307.15343
- **Method:** Benchmark built from medical exam questions from several countries, with reasoning-based hallucination tests and memory-based hallucination tests.
- **Reported results (abstract):** Text Davinci, GPT-3.5, LLaMA-2, MPT and Falcon show significant performance differences. Specific scores and sub-test names were not on the fetched pages.
- **Similarity:** Measures hallucination in the medical domain.
- **Difference:** Exam-style QA from model knowledge, vs the thesis's explanation of a given result where any added knowledge counts as an error.
- **Comparable thesis metric:** Motivation only (shows medical hallucination is measurable and differs by model). Supports the thesis's per-model error-rate comparison (Qwen3-4B vs API models).

### D2. Zaretsky et al. 2024 — LLM patient-friendly discharge summaries (peer-reviewed error measurement)
- **Citation:** Zaretsky J, Kim JM, Baskharoun S, Zhao Y, Austrian J, Aphinyanaphongs Y, Gupta R, Blecker SB, Feldman J. *Generative artificial intelligence to transform inpatient discharge summaries to patient-friendly language and format.* JAMA Network Open. 2024;7(3):e240357. doi:10.1001/jamanetworkopen.2024.0357
- **URL fetched:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10928500
- **Method:** Cross-sectional study. GPT-4 (HIPAA-compliant Azure) rewrote 50 discharge summaries into a one-page Q&A patient version. Physicians rated accuracy, completeness and safety, and readability and understandability were measured.
- **Reported results:** Flesch-Kincaid grade 6.2 vs 11.0 for the originals. PEMAT understandability 81% vs 13%. 54/100 reviews gave the top accuracy rating. Omissions appeared in about 24% of all reviews and hallucinations in about 4%. 18/100 reviews raised safety concerns. The authors conclude physician review is needed.
- **Similarity:** Patient-facing LLM rewriting of clinical content; error types (omission, hallucination, safety) overlap with the verifier's rules.
- **Difference:** Human review afterwards, no automatic safeguard. The thesis automates the safeguard, removes numeric errors by construction, and falls back to a template.
- **Comparable thesis metric:** % outputs with hallucinated content (4%) and with safety concerns (18%) as reference rates for the "without verifier" condition. Readability grade (FKGL) and an understandability score.

## E. LLMs explaining medical results to patients

### E1. Jeblick et al. 2024 (already cited — confirmed)
- **Citation:** Jeblick K, Schachtner B, Dexl J, Mittermeier A, Stüber AT, Topalis J, Weber T, Wesp P, Sabel BO, Ricke J, Ingrisch M. *ChatGPT makes medicine easy to swallow: an exploratory case study on simplified radiology reports.* European Radiology. 2024;34:2817–2825 (published online 5 Oct 2023). DOI: 10.1007/s00330-023-10213-1 (issue number not shown).
- **URL fetched:** https://epub.ub.uni-muenchen.de/116334/1/s00330-023-10213-1.pdf (open-access copy, LMU repository)
- **Method:** ChatGPT (Dec 2022) simplified 3 fictitious reports, 15 times each (45 outputs), with the prompt "Explain this medical report to a child using simple language". 15 radiologists rated factual correctness, completeness and potential harm (5-point Likert) and listed errors.
- **Main finding (confirmed):** Median ratings were "agree" for correct and complete and "disagree" for harmful. But incorrect passages were flagged in 23/45 outputs (51%), missing key information in 10/45 (22%), and potentially harmful conclusions in 16/45 (36%). The authors conclude medical adaptation and expert oversight are needed.
- **Similarity:** Same task family (plain-language explanation of a medical result).
- **Difference:** No safeguard. The thesis adds placeholders, a verifier and a fallback.
- **Comparable thesis metric:** % outputs with incorrect statements (51%) and with potentially harmful statements (36%), compared with the thesis's raw-LLM vs verified-pipeline error rates.

### E2. Lyu et al. 2023
- **Citation:** Lyu Q, Tan J, Zapadka ME, Ponnatapura J, Niu C, Myers KJ, Wang G, Whitlow CT. *Translating radiology reports into plain language using ChatGPT and GPT-4 with prompt learning: results, limitations, and potential.* Visual Computing for Industry, Biomedicine, and Art. 2023;6(1). DOI: 10.1186/s42492-023-00136-5 (article number not shown; DOAJ lists pages 1–10).
- **URL fetched:** https://doaj.org/article/1e44174129ea4addbffdc7a3bb715612
- **Method:** ChatGPT translated 138 reports (62 low-dose chest CT lung cancer screening, 76 brain MRI metastasis screening) into plain language; radiologists rated quality. Prompt variants were compared, and GPT-4 was also tested.
- **Reported results:** Mean quality 4.27/5. On average 0.08 places of missing information and 0.07 places of misinformation per report. 37% of cases included specific recommendations. Responses varied between runs and sometimes oversimplified. A more detailed prompt helped, and GPT-4 improved quality significantly.
- **Similarity:** Directly relevant domain (lung cancer screening CT reports for patients).
- **Difference:** Free-text input and output, quality judged by radiologists, no automatic check. Run-to-run variability is exactly what the thesis's deterministic fallback addresses.
- **Comparable thesis metric:** Misinformation and omission per output; Likert quality.

### E3. Ayers et al. 2023
- **Citation:** Ayers JW, Poliak A, Dredze M, Leas EC, Zhu Z, Kelley JB, Faix DJ, Goodman AM, Longhurst CA, Hogarth M, Smith DM. *Comparing Physician and Artificial Intelligence Chatbot Responses to Patient Questions Posted to a Public Social Media Forum.* JAMA Internal Medicine. 2023;183(6):589. DOI: 10.1001/jamainternmed.2023.1838
- **URLs fetched:** https://kstp.com/wp-content/uploads/2023/05/jamainternal_ayers_2023_oi_230030_1681999216.70842.pdf (article PDF copy, for content); https://cir.nii.ac.jp/crid/1360299770892246016.csv (volume/issue/page: 183(6):589; end page not shown)
- **Method:** 195 r/AskDocs questions with verified-physician answers vs ChatGPT (GPT-3.5) answers. Three licensed clinicians blindly rated preference, quality and empathy (585 evaluations).
- **Reported results:** The chatbot was preferred in 78.6% of evaluations. Good/very good quality was 78.5% vs 22.1%, and empathetic/very empathetic 45.1% vs 4.6%. Chatbot answers were longer (211 vs 52 words). The authors note accuracy and fabrication were not assessed.
- **Similarity:** Shows LLM patient-facing text is well received, which motivates using an LLM rather than only templates.
- **Difference:** No error measurement at all. The thesis measures errors explicitly and constrains them.
- **Comparable thesis metric:** Perceived quality and preference in the user study (LLM+verifier vs template + icon array).

### E4. He et al. 2024 — LLMs interpreting lab test results for lay patients
- **Citation:** He Z, Bhasuran B, Jin Q, Tian S, Hanna K, Shavor C, Arguello LG, Murray P, Lu Z. *Quality of Answers of Generative Large Language Models Versus Peer Users for Interpreting Laboratory Test Results for Lay Patients: Evaluation Study.* Journal of Medical Internet Research. 2024;26:e56655. DOI: 10.2196/56655. PMID 38630520. (Title assembled from the JMIR RIS export, which showed the start and end verbatim, and the arXiv title; volume/e-number/DOI from the JMIR BibTeX export.)
- **URLs fetched:** https://jmir.org/article/export/bib/jmir_v26i1e56655 ; https://jmir.org/article/export/ris/jmir_v26i1e56655 ; https://arxiv.org/abs/2402.01693v1
- **Method:** 53 lab-test question–answer pairs from Yahoo! Answers. Responses came from GPT-4, GPT-3.5, LLaMA 2, MedAlpaca and ORCA_mini, compared with ROUGE/BLEU/METEOR/BERTScore, an LLM-judge win rate on relevance, correctness, helpfulness and safety, and medical experts on 7 questions.
- **Reported results (abstract):** GPT-4 beat the other LLMs and the human answers on all four aspects. The authors note LLM answers sometimes lacked patient context, contained incorrect statements and lacked references. Specific win rates were not on the abstract pages.
- **Similarity:** Patient-facing interpretation of a quantitative test result, closest analogue to explaining a PLCO risk value.
- **Difference:** Free generation; correctness judged afterwards. The thesis prevents number errors by construction and checks direction and horizon.
- **Comparable thesis metric:** Correctness and safety rates per model; model comparison (small local vs large API).

### E5. Doshi, Amin et al. 2023 — readability of LLM-simplified radiology reports (preprint)
- **Citation:** Doshi R, Amin K, Khosla P, Bajaj S, Chheang S, Forman HP. *Utilizing Large Language Models to Simplify Radiology Reports: a comparative analysis of ChatGPT3.5, ChatGPT4.0, Google Bard, and Microsoft Bing.* medRxiv preprint, 2023. DOI: 10.1101/2023.06.04.23290786. **Not peer-reviewed (the preprint says so).**
- **URLs fetched:** https://medrxiv.org/highwire/citation/660784/refworks-tagged ; https://medrxiv.org/content/10.1101/2023.06.04.23290786v2.full.pdf
- **Method:** 254 reports, 3 prompts, 4 LLMs. Readability was the average of Gunning Fog, Flesch-Kincaid, ARI and Coleman-Liau (aRGL).
- **Reported results:** Original reports had median aRGL 17.2. ChatGPT-3.5 reached 10.5 / 7.6 / 6.7 across prompts 1–3 (more context, e.g. "I am a patient" or "7th-grade level", helped). Bard and Bing were about 8–9 (the text reports these inconsistently). Accuracy was not assessed by clinicians.
- **Similarity:** Readability as an outcome; prompt specification matters.
- **Difference:** No accuracy check. The thesis pairs readability with verified correctness.
- **Comparable thesis metric:** Readability grade of verified outputs (EN; a Romanian readability measure would need a separate justification).

## F. Data-to-text, delexicalisation and numeric accuracy

### F1. Wen et al. 2015 — SC-LSTM with delexicalisation
- **Citation:** Tsung-Hsien Wen, Milica Gašić, Nikola Mrkšić, Pei-Hao Su, David Vandyke, Steve Young. 2015. *Semantically Conditioned LSTM-based Natural Language Generation for Spoken Dialogue Systems.* In Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing, pp. 1711–1721, Lisbon. ACL. DOI: 10.18653/v1/D15-1199
- **URLs fetched:** https://aclanthology.org/D15-1199/ ; https://preview.aclanthology.org/fix_video/D15-1199.pdf (full text)
- **Method:** An LSTM generator conditioned on a dialogue act. Slot values are replaced by slot tokens before training ("delexicalisation") and the real values are put back after generation ("lexicalisation"). The paper notes binary and "don't care" slots cannot be delexicalised.
- **Reported results:** SF Restaurant BLEU 0.731 with slot error rate 0.46%; SF Hotel BLEU 0.832 with ERR 0.41%. The handcrafted generator had ERR 0.0% but much lower BLEU (0.451/0.560). Human judges preferred SC-LSTM over a class-based LM 62.3% of the time.
- **Similarity:** **Direct ancestor of the placeholder design.** The model writes tokens and code fills in the values. The results also show the trade-off the thesis uses: templates give 0% slot errors, learned generators are more natural but make small slot errors.
- **Difference:** Task-specific trained model on restaurant/hotel dialogue acts, vs a prompted general LLM on medical risk, with an extra semantic verifier for errors that delexicalisation alone cannot prevent (wrong direction, banned phrases, stray number words).
- **Comparable thesis metric:** Slot error rate ↔ thesis rate of placeholder errors (missing, duplicated or invented placeholders) and stray numbers.

### F2. Thomson & Reiter 2020 — accuracy evaluation in data-to-text
- **Citation:** Craig Thomson, Ehud Reiter. 2020. *A Gold Standard Methodology for Evaluating Accuracy in Data-To-Text Systems.* In Proceedings of the 13th International Conference on Natural Language Generation (INLG 2020), pp. 158–168, Dublin. ACL. DOI: 10.18653/v1/2020.inlg-1.22
- **URLs fetched:** https://aclanthology.org/2020.inlg-1.22 ; https://aclanthology.org/2020.inlg-1.22.pdf
- **Method:** Human protocol for annotating factual errors at token/phrase level against the source data, with categories incorrect number, named entity, word, context, not checkable and other. Proposed as a gold standard for validating automatic accuracy metrics.
- **Reported results:** 21 neural basketball summaries had 418 errors (about 20 per text). **Incorrect number was the most common category (184, about 44%)**, followed by named entity (105) and word (80).
- **Similarity:** Its error taxonomy maps onto the thesis's injected-error categories. It provides empirical evidence that numbers are the main failure point of neural generators, which justifies keeping numbers out of the LLM.
- **Difference:** Human annotation of sports summaries; the thesis automates checking for a narrow medical schema.
- **Comparable thesis metric:** Errors per text by category; the verifier's per-category recall on injected errors (number / direction / horizon / unsupported finding / forbidden phrase).

## G. Structured output (one line each)

- **G1. Ollama structured outputs** — https://docs.ollama.com/capabilities/structured-outputs (fetched). The `format` parameter takes `"json"` or a JSON-schema object (e.g. a Pydantic `model_json_schema()`) and constrains the reply to that schema. The docs also advise putting the schema in the prompt and using temperature 0, and say Ollama's cloud does not support it yet.
- **G2. OpenAI Structured Outputs** — https://developers.openai.com/api/docs/guides/structured-outputs.md (fetched). With `json_schema` and `"strict": true` (Responses API `text.format`), a completed non-refusal reply conforms to the supplied JSON Schema. JSON mode only guarantees valid JSON. Refusals and incomplete responses must still be handled, and business rules the schema cannot express must still be checked.
- **Relevance:** Schema constraints guarantee *shape* (fields, enums), not *content truth*. The thesis's semantic verifier covers the gap the OpenAI doc itself points out ("business rules").

## H. Lung cancer screening risk communication

### H1. Lau et al. 2015 — shouldiscreen.com evaluation
- **Citation:** Lau YK, Caverly TJ, Cao P, Cherng ST, West M, Gaber C, Arenberg D, Meza R. *Evaluation of a Personalized, Web-Based Decision Aid for Lung Cancer Screening.* American Journal of Preventive Medicine. 2015;49(6):e125–e129. DOI: 10.1016/j.amepre.2015.07.027. PMID 26456873; PMCID PMC5544524.
- **URLs fetched:** https://www.pubmed.gov/26456873/ (abstract); https://buscaintegrada.ufrj.br/Record/pubmed-5544524 (authors, DOI); https://pesquisa.bvsalud.org/nicaragua/resource/es/mdl-26456873 (vol/issue/pages); https://medicalxpress.com/news/2015-10-tool-patients-lung-cancer-screening.pdf (DOI)
- **Method:** Before–after study (Aug–Dec 2014) of 60 current or former smokers using shouldiscreen.com, which computes personal lung cancer risk and the chance of benefit and harm from LDCT screening.
- **Reported results:** Knowledge rose and decisional conflict fell after use (both p<0.001; scores not shown in the fetched abstract). Agreement between preference and USPSTF eligibility improved (p<0.001). 97% found the aid likely useful.
- **Related protocol (fetched, https://pmc.ncbi.nlm.nih.gov/articles/PMC4376198):** Lau YK, Caverly TJ, Cherng ST, Cao P, West M, Arenberg D, Meza R. *Development and Validation of a Personalized, Web-Based Decision Aid for Lung Cancer Screening Using Mixed Methods: A Study Protocol.* JMIR Research Protocols. 2014;3(4):e78. doi:10.2196/resprot.4039. Risk is shown as an absolute percentage and benefits as **icon arrays**. The risk model is described as "an established risk model" and cited to Tammemägi et al. 2013 (NEJM). The model is not named in the protocol text.
- **Similarity:** Same clinical decision (LDCT eligibility from personal risk) and the same comparison format the thesis uses as its control (number + icon array).
- **Difference:** Static, expert-written explanations, no generated text. The thesis tests whether verified LLM text adds comprehension over this standard.
- **Comparable thesis metric:** Knowledge/comprehension score pre→post and acceptability (%). Possibly decisional conflict if the user study includes it.

---

## Summary table

| # | Work | Venue (confirmed) | Approach | Key reported metric | Thesis metric to compare |
|---|---|---|---|---|---|
| A1 | FActScore (Min et al.) | EMNLP 2023 | atomic-fact support vs KB | ChatGPT 58% factual precision; estimator <2% error | % unsupported content |
| A2 | SelfCheckGPT (Manakul et al.) | EMNLP 2023 | sampling consistency | AUC-PR 93.42 (NonFact) | verifier precision/recall, AUC-PR |
| A3 | CoVe (Dhuliawala et al.) | Findings ACL 2024 | self-verification questions | FActScore 55.9→71.4 | relative error reduction |
| A4 | RARR (Gao et al.) | ACL 2023 (long) | retrieve + minimal edit | attribution ↑ (abstract) | retry success / post-repair error rate |
| B1 | RAG (Lewis et al.) | NeurIPS 2020 | retrieval grounding | SOTA on 3 open QA tasks | numbers-in-prompt baseline vs placeholders |
| C1 | NeMo Guardrails (Rebedea et al.) | EMNLP 2023 Demos | programmable rails (Colang) | ~99% harmful blocked / 2% helpful blocked | block rate vs false-block rate |
| C2 | Guardrails AI | GitHub (Apache-2.0) | validators + on_fail | none | implementation baseline |
| C3 | Llama Guard (Inan et al.) | arXiv 2023 | LLM safety classifier | ≥ moderation tools on OpenAI Mod / ToxicChat | classifier P/R/F1 |
| D1 | Med-HALT (Pal et al.) | CoNLL 2023 | medical hallucination benchmark | significant model differences | per-model error rates |
| D2 | Zaretsky et al. | JAMA Netw Open 2024 | GPT-4 patient discharge summaries | FKGL 11.0→6.2; hallucination ~4%, safety concerns 18% | % errors without verifier; FKGL |
| E1 | Jeblick et al. | Eur Radiol 2024 | ChatGPT simplified reports | 51% incorrect, 36% harmful | % outputs with errors/harm |
| E2 | Lyu et al. | VCIBA 2023 | ChatGPT/GPT-4 plain-language reports (incl. LDCT) | 4.27/5; 0.07 misinformation per report | misinformation per output |
| E3 | Ayers et al. | JAMA Intern Med 2023 | chatbot vs physician answers | preferred 78.6% | user preference/quality |
| E4 | He et al. | JMIR 2024 | LLMs interpret lab results | GPT-4 best on 4 aspects | correctness/safety per model |
| E5 | Doshi, Amin et al. | medRxiv 2023 (preprint) | LLM readability | aRGL 17.2→6.7 | readability grade |
| F1 | Wen et al. (SC-LSTM) | EMNLP 2015 | delexicalised generation | ERR 0.41–0.46%; template 0% | placeholder/slot error rate |
| F2 | Thomson & Reiter | INLG 2020 | accuracy error taxonomy | 20 errors/text; 44% numbers | per-category error recall |
| G1 | Ollama structured outputs | official docs | JSON-schema constrained decoding | n/a | output well-formedness rate |
| G2 | OpenAI Structured Outputs | official docs | strict JSON Schema | n/a | output well-formedness rate |
| H1 | Lau et al. (shouldiscreen.com) | Am J Prev Med 2015 | personalised decision aid + icon arrays | knowledge ↑, conflict ↓ (p<0.001); 97% useful | comprehension vs template + icon array |

**Positioning in one line:** The detectors (A1–A3, C1, C3) are LLM-based and probabilistic. The patient-facing studies (D2, E1–E5) find 4–51% problematic outputs but add no automatic safeguard. Delexicalisation (F1) removes slot errors but not semantic ones. The thesis combines delexicalised generation, deterministic domain checks (EN+RO) and a template fallback, and evaluates them with injected-error P/R, per-model error rates and comprehension against the icon-array standard (H1).

## Not confirmed / caveats

- **Amin KS et al., Radiology (peer-reviewed version of the Doshi/Amin readability study):** A title "Accuracy of ChatGPT, Google Bard, and Microsoft Bing for Simplifying Radiology Reports" appears in search results (aminer), but no fetched page showed its journal, volume or DOI. **Unconfirmed; cite only the medRxiv preprint (E5) or verify on pubs.rsna.org first.**
- **Ollama structured-outputs blog post** (ollama.com/blog/structured-outputs): not fetched (blocked); the docs page was used instead. Release date/version not confirmed.
- **Guardrails AI full list of `on_fail` actions** (reask, fix, filter, etc.): only `exception` was shown on fetched pages; the On-Fail Policies page was not fetched.
- **RARR, Med-HALT, He et al., Lau et al.:** exact numeric results beyond those listed were not on fetched pages (abstract-level only).
- **Ayers et al.:** end page not shown (cite as 183(6):589–596 only after checking).
- **Jeblick et al.:** issue number not shown.
- **Lyu et al.:** article number not shown (DOAJ shows 6(1):1–10).
- **Lau 2014 protocol risk model:** the protocol cites Tammemägi 2013 but does not name PLCOm2012 in its text; do not claim shouldiscreen.com uses PLCOm2012 on the basis of this page alone.
- **Reuland et al. 2018** (BMC Med Inform Decis Mak 18:5, DOI 10.1186/s12911-018-0582-1, *A pre-post study testing a lung cancer screening decision aid in primary care*): citation confirmed via Crossref API, but no abstract was retrieved, so it is not summarised above. It could be added as a second H entry after reading its abstract.
- No peer-reviewed study specifically on **numerical** hallucination in LLM **table-to-text** was confirmed in this pass. Thomson & Reiter 2020 (neural, pre-LLM) is the confirmed evidence that numbers dominate data-to-text errors.
