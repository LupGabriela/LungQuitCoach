# 07 - Sources checked for the "Mathematical model" chapter

Checked on 2026-11-18. Each fact below was confirmed on a page fetched today unless it is marked NOT CONFIRMED. Nothing comes from memory.

How the pages were reached: from the sandbox's command line, only raw.githubusercontent.com and api.github.com were reachable. The NCBI E-utilities, Europe PMC, Crossref API, nature.com, thorax.bmj.com and pubmed.ncbi.nlm.nih.gov were blocked (proxy 403, URL not on the allowlist, or a reCAPTCHA page). PMC article pages and the NHS England PDFs were read with a web-fetch tool. That tool returns a model-written summary with short verbatim quotes, not the raw page. **Crossref could not be used, so no DOI was checked against Crossref.** The web-search budget ran out partway through, which blocked items 8 and 9.

---

## 1. PLCOm2012 coefficients (Tammemägi et al., NEJM 2013;368:728-36): CONFIRMED, one wording note

Fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC3929969/ (the E-utilities efetch URL was blocked by the proxy).

| Item | Value in 05-risk-calculators.md | Value fetched today | Status |
|---|---|---|---|
| Age | 0.0778868, centred at 62 | 0.0778868, centred at 62 | OK |
| White | reference | "Reference group" | OK |
| Black | 0.3944778 | 0.3944778 | OK |
| Hispanic | -0.7434744 | -0.7434744 | OK |
| Asian | -0.466585 | -0.466585 | OK |
| American Indian / Alaskan Native | 0 | OR 1, beta 0, no CI or P | OK |
| Native Hawaiian / Pacific Islander | 1.027152 | 1.027152 | OK |
| Education | -0.0812744, centred at level 4 | -0.0812744, level 4 | OK |
| BMI | -0.0274194, centred at 27 | -0.0274194, 27 | OK |
| COPD | 0.3553063 | 0.3553063 | OK |
| Personal history of cancer | 0.4589971 | 0.4589971 | OK |
| Family history of lung cancer | 0.587185 | 0.587185 | OK |
| Smoking status (current vs former) | 0.2597431 | 0.2597431 | OK, see note (a) |
| Smoking intensity | -1.822606 | -1.822606 | OK |
| Intensity transform | (cpd/10)^-1 - 0.4021541613 | "dividing by 10, exponentiating by the power -1, centering by subtracting 0.4021541613" | OK |
| Intensity definition | average cigarettes per day | "the average number of cigarettes smoked per day" | OK |
| Duration | 0.0317321, centred at 27 | 0.0317321, 27 | OK |
| Quit time | -0.0308572, centred at 10 | -0.0308572, 10 | OK |
| Constant | -4.532506 | -4.532506 | OK |
| Link function | p = e^logit / (1 + e^logit), 6-year | same | OK |
| Education levels | 1 = less than high-school graduate ... 6 = postgraduate or professional degree | 1 = "less than high-school graduate", 2 = "high-school graduate", 3 = "some training after high school", 4 = "some college", 5 = "college graduate", 6 = "postgraduate or professional degree" | OK |
| Development cohort | 36,286 ever-smokers, PLCO control group | "36,286 Control Participants Who Had Ever Smoked" | OK |
| Validation AUC, PLCO intervention group | 0.797 | 0.797 (95% CI 0.782-0.813) | OK |
| Validation AUC, NLST | 0.701 | 0.701 (95% CI 0.689-0.712) | OK |
| 1.3455% threshold | Table 4 footnote | Table 4 footnote: "positivity was defined as a probability of lung cancer that was greater than 1.3455% over a period of 6 years"; Results: "persons with a lung-cancer risk higher than 1.3455% were eligible". Methods: the cutoff was chosen so that "the number of persons above this point was exactly the same" as those meeting the NLST criteria | OK |
| Pack-years not a predictor | quote | "pack-years were not included" (Discussion) | OK |
| Never-smokers excluded | quote | "PLCOm2012 excluded persons who had never smoked." | OK |
| Age 55-74 | "Table 1" | "In both the PLCO and the NLST, an age between 55 and 74 years was an entry criterion." | Value OK, see note (b) |

Notes:
- (a) Table 2 labels the smoking-status row "current vs. former". The footnote does **not** say "current = 1, former = 0" in so many words. That coding follows from the row label and the positive beta, and the resplab code agrees (`smoking_status = 0` is used for a former smoker, item 2). In the thesis, write it as "indicator for current smoking (current vs. former, Table 2)".
- (b) The tool found the age criterion as a sentence in the text. It did not confirm that the sentence sits in Table 1. Cite "Methods, PMC3929969", not "Table 1".
- The paper gives **no quit-time value for current smokers**. Re-confirmed today. Setting quit time to 0 for current smokers is an implementation convention.

**No discrepancies in any coefficient, centring value or constant.**

## 2. Worked example 0.01750922 (resplab/PLCOm2012): CONFIRMED

Fetched: https://raw.githubusercontent.com/resplab/PLCOm2012/HEAD/README.md and https://raw.githubusercontent.com/resplab/PLCOm2012/HEAD/tests/testthat/test-plcom2012.R (the github.com HTML page returned 403).

- README: `plcom2012(age=62, race='White', education=4, bmi=27, copd=0, cancer_hist=0, family_hist_lung_cancer=0, smoking_status=0, smoking_intensity=80, duration_smoking=27, smoking_quit_time=10)` returns `$prob [1] 0.01750922`. The README text says "former smoker, smokes 80 cigarettes per day ... 1.75% probability ... over the next 6 years".
- Test file: at the centring values (intensity = 10/0.4021541613, age 62, education 4, BMI 27, duration 27, quit 10) the probability equals `exp(-4.532506)/(1+exp(-4.532506))`. The same holds with each race beta added for Black (+0.3944778), Hispanic (-0.7434744), Asian (-0.466585) and Pacific Islander (+1.027152).
- **Own check:** `/home/claude/research/plcom_check.py` is written from the item 1 coefficients only. No downloaded code was run. Output: `README example: 0.01750922` and all 5 centring tests passed (white 0.0106392819, black 0.0157037373, hispanic 0.0050869323, asian 0.0066988967, NHPI 0.0291602766).

## 3. The 1.51% threshold: CONFIRMED

### Tammemägi et al. 2014, PLoS Medicine
Fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC4251899/

- Citation: Tammemägi MC, Church TR, Hocking WG, Silvestri GA, Kvale PA, Riley TL, Commins J, Berg CD. "Evaluation of the Lung Cancer Risks at Which to Screen Ever- and Never-Smokers: Screening Rules Applied to the PLCO and NLST Cohorts." *PLoS Med.* 2014;11(12):e1001764. doi:10.1371/journal.pmed.1001764. PMID 25460915. A correction was published (PLoS Med 2015;12(1):e1001787).
- Threshold, from the abstract: "At PLCOm2012 risk ≥0.0151, the 65th percentile of risk, the NLST CT arm mortality rates are consistently below the CXR arm's rates." The 65th percentile was taken among PLCO control-arm smokers.
- Other abstract conclusions: "Smokers aged ≥65-80 y are a high-risk group who may benefit from screening." "Currently, never-smokers should not be screened." None of the 65,711 PLCO never-smokers had a PLCOm2012 risk of 0.0151 or more.

### NHS England standard protocol
Two versions were fetched. Both give the same thresholds and age range.

- **Version 2, 7 Nov 2022** (Targeted Lung Health Checks Programme, ref PR1646): https://www.england.nhs.uk/wp-content/uploads/2019/02/B1646-standard-protocol-targeted-lung-health-checks-programme-v2.pdf
  - Title: "Targeted screening for lung cancer with low radiation dose computed tomography". Subtitle: "Standard protocol prepared for the Targeted Lung Health Checks Programme".
  - §3.3.8: "PLCOM2012 risk of ≥1.51% over six years or LLPver2 five-year risk of ≥2.5%." "Age is from 55 years, to 74 years and 364 days."
- **Version 3, 3 Feb 2025** (Lung Cancer Screening Programme, ref PR1646): https://www.england.nhs.uk/wp-content/uploads/2019/02/2502-B1646-standard-protocol-prepared-for-the-lung-cancer-screening-programme.pdf
  - §3.3.4: "a risk threshold of ≥1.51% risk of lung cancer over six years is the minimum threshold for PLCOM2012". The same section mentions ≥2.00% over five years for LLPv2 from the evidence base, but says "a risk threshold for LLP of ≥2.5% is considered the minimum threshold".
  - §3.3.7: "PLCOM2012 risk of ≥1.51% over six years" or "LLPver2 five-year risk of ≥2.5%". "Age is from 55 years to 74 years and 364 days."
- **Recommendation:** cite version 3 (Feb 2025), the current programme document. Note that the age range is 55 to 74 years and 364 days.

## 4. Kumarasamy et al., Thorax 2025: CONFIRMED, with abstract inconsistencies

Fetched: full text https://pmc.ncbi.nlm.nih.gov/articles/PMC12322426/; bibliographic record https://research-repository.uwa.edu.au/en/publications/future-risk-projection-to-engage-near-miss-individuals-in-lung-ca/; abstract https://publications.petermac.org/Publications/4628. thorax.bmj.com and doi.org were not on the allowlist.

- Citation: Kumarasamy C, Betts K, Norman R, McWilliams A, Stone E, Lam DCL, Manser R, Fogarty P, Marshall HM, Lam S, Tammemagi M, Fong KM, Atkar-Khattra S, Brims F. *Thorax* 2025;80:547-552. doi:10.1136/thorax-2024-222098. PMID 40274409. Epub 24 Apr 2025.
- Cohort: potential ILST participants aged 55-80 who were **ineligible** at baseline (PLCOm2012 below 1.5%). n = **4,451** (out of 10,146 assessed). Median age 61 (IQR 57-66). 965 current smokers (21.7%) and 3,486 former smokers (78.3%).
- How risk was projected: PLCOm2012 recomputed **every year from the first evaluation up to age 80**, using "annual increments of change in age, smoking duration and quit time". Duration rises for current smokers and quit time rises for former smokers. **Held constant:** BMI (to "minimise further assumption"), COPD, personal cancer history, family history, education, and cigarettes per day. Main scenario: smoking status unchanged ("no change in smoking status post evaluation"), because "predicting individual smoking behaviour was not feasible". Alternative scenario: "complete and successful smoking cessation after initial evaluation", with no relapse. The paper does not spell out the exact quit date or how quit time is coded in that scenario.
- Eligibility threshold during projection: PLCOm2012 ≥1.51%.
- Main finding, no change in smoking: 2,239 (50.3%) became eligible by age 80; 26.9% by age 70; 38.7% by age 75. Among those with baseline risk ≥0.6%, 1,518 (34.1%) became eligible within 10 years. With cessation: 1,963 (44.1%) by age 80, and 17.4% (n=775) by age 70 (Results).
- **Discrepancy inside the paper:** the abstract says cessation lowers the share eligible by age 70 "from 68.7% to 24.9%". Those numbers do not appear in the Results, which give 26.9% vs 17.4%, and the denominator for 68.7%/24.9% is not stated. Cite the Results figures, or flag the inconsistency.
- Limitation stated by the authors: "These assumptions of constancy are unlikely to hold true at an individual level."
- **Relevance to the thesis:** this is the same kind of input-advancing projection as in our model (age, duration and quit time move forward; everything else stays fixed). Kumarasamy used yearly steps up to age 80, not years 3, 5 and 7. Our "increase" scenario (higher average cpd) is **not** part of their method.

## 5. van Geloven et al. 2020, Eur J Epidemiol: CONFIRMED (key point is in the body, not the abstract)

Fetched: https://repub.eur.nl/pub/127452 (record), https://arxiv.org/abs/2004.06998v1 (abstract), https://arxiv.org/pdf/2004.06998 (full text). The PMC page (PMC7387325) showed a reCAPTCHA. The UCL PDF failed to load.

- Citation: van Geloven N, Swanson SA, Ramspek CL, Luijken K, van Diepen M, Morris TP, Groenwold RHH, van Houwelingen HC, Putter H, le Cessie S. "Prediction meets causal inference: the role of treatment in clinical prediction models." *Eur J Epidemiol* 2020. doi:10.1007/s10654-020-00636-1. Published online 12 May 2020. **Volume, issue and pages: NOT CONFIRMED** (not on the fetched record; Crossref was blocked).
- The **abstract** does **not** say outright that hypothetical-intervention predictions need causal assumptions. It proposes a framework for questions about risk prediction when treatment starts after baseline, which the authors compare to the estimand framework used in trials. It says "clearly defining the estimand is equally important in prediction research as in causal inference" and discusses "appropriate estimators including their assumptions".
- The key point is in the **full text, §4.4 ("Hypothetical" strategy)**: "the strategy implicitly imposes a counterfactual or potential outcome version of A into the estimand of interest"; "Three key assumptions are required: exchangeability, consistency and positivity"; "These assumptions are similar to those that are needed for identifying the causal treatment effect of A". From §6: "The 'hypothetical' prediction estimand could be classified as a type of counterfactual prediction"; "Several untestable assumptions are needed here".
- Wording note: these quotes are from the arXiv preprint. Check them against the published version before quoting them word for word.

## 6. PLCO age range 55-74: CONFIRMED

Fetched: https://cdas.cancer.gov/publications/103 (NCI Cancer Data Access System record of Oken et al.).

- Oken MM, Hocking WG, Kvale PA, et al. *JAMA* 2011;306(17):1865-73. PMID 22031728.
- Abstract: "Randomized controlled trial that involved 154,901 participants aged 55 through 74 years", enrolled "between November 1993 and July 2001".
- This matches the NEJM 2013 sentence in item 1.

## 7. TorchXRayVision: CONFIRMED (calibration wording needs care)

Fetched: https://raw.githubusercontent.com/mlmed/torchxrayvision/HEAD/README.md, `.../torchxrayvision/models.py`, `.../datasets.py`, `.../utils.py`, and the paper https://arxiv.org/pdf/2111.00595 (Cohen JP, Viviano JD, Bertin P, et al. "TorchXRayVision: A library of chest X-ray datasets and models", arXiv:2111.00595, 2021).

- **"all" model (`densenet121-res224-all`):** a DenseNet-121 trained on "nih-pc-chex-mimic_ch-google-openi-rsna" (models.py description field), `input_resolution: 224`. It has **18 outputs**, in this order: Atelectasis, Consolidation, Infiltration, Pneumothorax, Edema, Emphysema, Fibrosis, Effusion, Pneumonia, Pleural_Thickening, Cardiomegaly, Nodule, Mass, Hernia, Lung Lesion, Fracture, Lung Opacity, Enlarged Cardiomediastinum. README: "Each pretrained model has 18 outputs. The `all` model has every output trained." For the other weights, untrained targets "will predict randomly".
- **What the outputs are:** in `forward()`, when `op_threshs` is set (it is set by default for "all"), the code applies `sigmoid` and then `op_norm`. `op_norm` is a piecewise-linear rescaling that maps each pathology's operating-point threshold to 0.5. Docstring: "outputs are re-scaled so that the threshold maps to 0.5". Paper §2.5: the operating point maximises TPR - FPR on the held-out test split of the *training* datasets. "The goal is to make a prediction of 0.5 the estimated decision boundary"; it "doesn't change the AUC"; "it is just for a nice calibrated probability output so you can use pred > 0.5 to get a prediction". To switch it off: `model.op_threshs = None`.
  - **Note for the thesis:** the authors do call this "calibrated", but only in the sense of re-centring the decision threshold. The README and paper **do not say** the scores are calibrated probabilities on new datasets or sites, and they do not say the opposite in those words either. The paper does stress that differences in dataset processing "can significantly impact the results". So the thesis should say: "the scores are threshold-normalised (0.5 = operating point chosen on the training data), not probabilities calibrated to a new population". That sentence is a correct reading of the code, but it is **our wording, not a quote**.
- **Input preprocessing:** README: `xrv.datasets.normalize(img, 255) # convert 8-bit image to [-1024, 1024] range`; single channel `img.mean(2)[None, ...]`; `XRayCenterCrop()` then `XRayResizer(224)`. utils.py: `img = (2 * (img / maxval) - 1.0) * 1024`. Paper §3.1: "Both models and datasets expect the image pixel values to be between [-1024,1024]"; input shape `[1,RES,RES]`; "All models will automatically resize input images to match the specified size they were trained on". `warn_normalization` warns if the input range looks wrong.

## 8. CXR-Lung-Risk (Weiss et al., Nat Commun 2023;14:2797): PARTLY CONFIRMED (official repo only; paper abstract NOT fetched)

Fetched: https://raw.githubusercontent.com/AIM-Harvard/CXR-Lung-Risk/HEAD/README.md and `.../notebooks/cxr_lung_risk_mwe.ipynb`. nature.com and Europe PMC were not on the allowlist, and the search budget ran out before the PMC ID could be found.

- Citation as given in the official repo: Weiss J, Raghu VK, Bontempi D, et al. "Deep learning to estimate lung disease mortality from chest radiographs." *Nat Commun* 14, 2797 (2023). doi:10.1038/s41467-023-37758-5.
- From the official notebook introduction, which is the authors' summary text: developed on "147,497 CXRs of 40,643 asymptomatic participants" from PLCO to predict lung-related mortality (COPD, interstitial lung disease, emphysema, lung cancer) from one CXR. "In three independent testing datasets comprising 15,976 individuals ... graded association with lung disease mortality ... robust after adjustment for known risk factors, including chronological age, smoking, and radiologic findings (adjusted hazard ratio for highest risk group vs. reference up to 12.15 [8.85-16.68]; p < 0.001). Adding CXR Lung-Risk to a multivariable model improved estimates of lung disease mortality (for all p ≤ 0.004)."
- README: test cohorts are "an independent cohort of 10.5k individuals from PLCO", "5.5k heavy smokers from the National Lung Screening Trial (NLST)" and "1k patients in the Boston Lung Cancer Study". It estimates "a person's risk of lung-related mortality within 18 years".
- **Output scale is unclear:** README: "CXR-Lung-Risk outputs a number (in years) reflecting lung-related mortality risk". The notebook computes the score as a LASSO-weighted sum of 20 CNN outputs plus an intercept of 49.8484258. **It is NOT CONFIRMED how the score is scaled or which risk groups the paper uses** (cut-points, the reference group for HR 12.15, cohort-specific HRs and C-statistics). These need the paper itself (nature.com or PMC), which could not be fetched today. Do not describe the score as a probability.

## 9. Lung Health Study (Scanlon et al., AJRCCM 2000;161:381-390): NOT CONFIRMED today

PubMed (https://pubmed.ncbi.nlm.nih.gov/10673175/) and the Europe PMC REST URL were both blocked (not on the allowlist), and the search budget was used up. The figures in 05-risk-calculators.md were **not** re-checked today: 3,926 smokers, mean age 48.5, 5-year follow-up, about +47 mL (2%) in the year after quitting, then a decline of 31 ± 48 mL/yr in sustained quitters vs 62 ± 55 mL/yr in continuing smokers. They rest only on the earlier Europe PMC fetch. Re-check them in a follow-up session before using them in the chapter.

---

## Summary of status

| # | Item | Status |
|---|---|---|
| 1 | PLCOm2012 coefficients, centring, transform, constant, education, n, AUCs, 1.3455% | CONFIRMED (no coefficient discrepancy; two wording notes) |
| 2 | 0.01750922 worked example and test file | CONFIRMED, reproduced by plcom_check.py |
| 3 | 1.51% (PLoS Med 2014, 65th percentile) and NHS England PLCOm2012 ≥1.51% / LLPv2 ≥2.5%, ages 55 to 74y364d | CONFIRMED (v2 2022 and v3 2025) |
| 4 | Kumarasamy 2025 projection method, n = 4,451, findings | CONFIRMED; abstract's 68.7%/24.9% does not match Results |
| 5 | van Geloven 2020 causal assumptions | CONFIRMED in full text §4.4 (not stated in abstract); vol/pages NOT CONFIRMED |
| 6 | PLCO ages 55-74 | CONFIRMED |
| 7 | TorchXRayVision outputs, op_norm, 224, [-1024, 1024] | CONFIRMED; "not calibrated across datasets" is our reading, not a quote |
| 8 | CXR-Lung-Risk | PARTLY CONFIRMED from official repo; score scale and risk groups NOT CONFIRMED |
| 9 | Lung Health Study FEV1 numbers | NOT CONFIRMED today |
| - | Crossref DOI checks | NOT DONE (api.crossref.org blocked) |
