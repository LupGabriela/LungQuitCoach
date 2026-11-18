# 05 – Evaluation methods: verified facts and citations

Verified on 2026-11-18. Every fact below comes from a page fetched in this session (URL given). Nothing is taken from memory.

**Access limits during verification**
- The Crossref API (api.crossref.org), PubMed, PMC and doi.org were all unreachable. Bash egress was blocked by policy, and PubMed/PMC/scinapse/dblp returned bot-check pages. So **no DOI was checked against Crossref**. DOIs were confirmed on publisher pages, library catalogues or indexing pages instead (listed per item).
- Kaggle could not be fetched.
- The web-search budget ran out before the last few lookups. Those are in the "Not confirmed" list at the end.

---

## 1. NIH ChestX-ray14 (NIH Clinical Center)

**NIH news release (official)**: https://nih.gov/news-events/news-releases/nih-clinical-center-provides-one-largest-publicly-available-chest-x-ray-datasets-scientific-community
- Dated Wednesday 27 September 2017.
- "over 100,000 anonymized chest x-ray images" from "more than 30,000 patients".
- The release says images are "available via Box", but the fetched text shows no URL. It says researchers can "freely access the datasets" and does not name a licence.
- It cites Wang X, Peng Y, Lu L, Lu Z, Bagheri M, Summers RM, "ChestX-ray8: Hospital-scale Chest X-ray Database and Benchmarks…", IEEE CVPR 2017.

**Google Cloud Healthcare API public-dataset page (re-hosts the NIH data)**: https://docs.cloud.google.com/healthcare-api/docs/resources/public-datasets/nih-chest
- Official NIH download site: **https://nihcc.app.box.com/v/ChestXray-NIHCC**
- "The images are in PNG format."
- Terms: **"There are no restrictions on the use of the NIH chest x-ray images."** Users must:
  1. provide a link to the NIH download site;
  2. cite the CVPR 2017 paper;
  3. acknowledge the NIH Clinical Center as the data provider.
- The RSNA ATLAS card (https://atlas.rsna.org/cards/66962171-1dcb-431d-89b0-08a561f1c8ed) gives the same Box folder (`…/ChestXray-NIHCC/folder/36938765345`). It says the labels were first 8 diseases and later 14, but gives no counts.

**Original paper (CVF open access)**: https://openaccess.thecvf.com/content_cvpr_2017/papers/Wang_ChestX-ray8_Hospital-Scale_Chest_CVPR_2017_paper
- Citation: Wang X, Peng Y, Lu L, Lu Z, Bagheri M, Summers RM. ChestX-ray8: Hospital-scale chest X-ray database and benchmarks on weakly-supervised classification and localization of common thorax diseases. *Proc. IEEE CVPR* 2017, pp. 2097–2106.
- This paper describes the **ChestX-ray8** version, not ChestX-ray14:
  - 108,948 frontal-view images from 32,717 patients (collected 1992–2015);
  - 8 text-mined labels (DNorm/MetaMap NLP), plus "Normal";
  - images resized to **1024×1024**;
  - NLP label accuracy on an OpenI gold subset: P 0.90 / R 0.91 / F1 0.90.
- The arXiv v5 abstract (https://arxiv.org/abs/1705.02315v5, 14 Dec 2017) still gives 108,948 / 32,717 / 8 labels.

**ChestX-ray14 figures (112,120 images / 30,805 patients / 14 labels)**
- These appear **only in a third-party Hugging Face card**: https://huggingface.co/datasets/alkzar90/NIH-Chest-X-ray-dataset/raw/main/README.md
- That card says: "112,120 frontal-view X-ray images of 30,805 unique patients"; 14 pathologies plus "No Finding"; sample image is PNG 1024×1024.
- The figures were not found on an NIH page fetched here, because the NIH Box README was not reachable. **Before citing them, check the README_CHESTXRAY.pdf in the Box folder.**

**Kaggle "Random Sample of NIH Chest X-ray Dataset"**: **NOT CONFIRMED.**
- kaggle.com could not be fetched.
- The only indirect source is a TIB catalogue entry (https://service.tib.eu/ldmservice/dataset/975e0259-5921-4908-aaf0-5b5183a021fa). It gives the homepage as https://www.kaggle.com/nih-chest-xrays/sample.
- That entry states no image count (5,606 / 5% is unconfirmed) and no licence.

## 2. CheXphoto

**Stanford AIMI dataset page**: https://aimi.stanford.edu/datasets/chexphoto-chest-x-rays

| Split | X-rays | Patients | Source |
|---|---|---|---|
| Training (natural photos + synthetic transformations) | 10,507 | 3,000 | random sample of CheXpert training set |
| Validation | 234 | 200 | CheXpert validation set |
| Test | 668 | 500 | CheXpert test set |

- Download: via Redivis, https://stanford.redivis.com/datasets/2qwg-aav2k243j
- Dataset DOI to cite: https://doi.org/10.71718/n3nj-2c03
- The page has "Terms & Conditions" and "License" headings, but **no text appeared under them**.

**Competition page**: https://stanfordmlgroup.github.io/competitions/chexphoto
- Validation also includes 250 VinBrain film photos; the test set has 250 withheld film images.
- The competition is closed. Code is at https://github.com/stanfordmlgroup/cheXphoto
- No licence is stated.

**AIMI shared-datasets policy**: https://aimi.stanford.edu/shared-datasets
- Datasets are free for **non-commercial research**, "subject to the applicable data use terms".
- Commercial use needs a separate licence.
- Users should acknowledge Stanford AIMI.
- Access is through Redivis (stanford.redivis.com/AIMI).

**Paper (PMLR)**: https://proceedings.mlr.press/v136/phillips20a.html
- Phillips NA, Rajpurkar P, Sabini M, Krishnan R, Zhou S, Pareek A, Phu NM, Wang C, Jain M, Du ND, Truong SQ, Ng AY, Lungren MP. CheXphoto: 10,000+ Photos and Transformations of Chest X-rays for Benchmarking Deep Learning Robustness. *Proc. Machine Learning for Health NeurIPS Workshop*, PMLR 136:318–327, 2020.
- arXiv: 2007.06199

## 3. VinDr-CXR and PadChest

**VinDr-CXR (PhysioNet)**: https://physionet.org/content/vindr-cxr/
- Version 1.0.0.
- 18,000 images released (15,000 train / 3,000 test), out of more than 100,000 raw scans.
- 17 radiologists; 22 local (bounding-box) labels and 6 global labels.
- **DICOM** format.
- **Credentialed access**: "Only credentialed users who sign the DUA can access the files", plus CITI training.
- Licence: PhysioNet Credentialed Health Data License 1.5.0. DUA: PhysioNet Credentialed Health Data Use Agreement 1.5.0.
- Dataset DOI 10.13026/3akn-b287. Original paper: Nguyen HQ et al., arXiv:2012.15029 (2020).

**PadChest**

arXiv abstract: https://arxiv.org/abs/1901.07441
- More than 160,000 images from 67,000 patients.
- Labels: 174 radiographic findings, 19 differential diagnoses, 104 anatomic locations.
- Download location: http://bimcv.cipf.es/bimcv-projects/padchest/
- Authors: Bustos A, Pertusa A, Salinas J-M, de la Iglesia-Vayá M.
- Journal DOI 10.1016/j.media.2020.101797 (the journal name is not shown on the page).

BIMCV PadChest Research Use Agreement: https://bimcv.cipf.es/?p=4923
- It is a custom agreement; **no CC licence is named**.
- "Permission is granted to view and use the PadChest Dataset without charge for research purposes only."
- Sale is prohibited.
- Non-academic use is assessed case by case and needs BIMCV approval.
- Users must cite the PadChest article and must not share the download link outside their organisation.

## 4. Corruption benchmarking: ImageNet-C

**Pages fetched**
- arXiv: https://arxiv.org/abs/1903.12261
- Full text (ar5iv): https://ar5iv.labs.arxiv.org/html/1903.12261
- Venue: https://mlanthology.org/iclr/2019/hendrycks2019iclr-benchmarking

**Citation**: Hendrycks D, Dietterich T. Benchmarking Neural Network Robustness to Common Corruptions and Perturbations. *International Conference on Learning Representations (ICLR)*, 2019. arXiv:1903.12261.

**Corruption types**: 15 types in 4 categories (Table 1).

| Category | Corruptions |
|---|---|
| Noise | Gaussian, shot, impulse |
| Blur | defocus, glass, motion, zoom |
| Weather | snow, frost, fog, brightness |
| Digital | contrast, elastic transform, pixelate, JPEG |

**Severity levels**: "Each corruption type has five levels of severity", giving 75 corruptions in total.

**Extra held-out corruptions** (for validation): speckle noise, Gaussian blur, spatter, saturate.

**Metrics**
- CE<sub>c</sub> is the error summed over the 5 severities, divided by AlexNet's summed error for the same corruption.
- mCE is the mean CE over the 15 corruptions.
- Relative CE/mCE subtract clean error first.
- The paper notes that "any baseline will do".

**Relevance to E4**: brightness, JPEG and contrast/pixelate map directly onto the planned degradations. Using 5 severity levels per degradation follows this convention.

## 5. ICC

**Koo & Li 2016**
- Citation: Koo TK, Li MY. A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research. *J Chiropr Med*. 2016;15(2):155–163. doi:10.1016/j.jcm.2016.02.012. PMID 27330520; PMCID PMC4913118.
- Where each part of the citation was confirmed:
  - journal, volume, issue, pages, DOI and date (31 Mar 2016): Scilit, https://www.scilit.net/publications/8913fe0a6407c75c88e4ade94dcb2a9e
  - authors: https://papers.mewayz.com/paper/oa_W2327037637
  - PMID/PMCID: https://buscaintegrada.ufrj.br/Record/pubmed-4913118
- **Thresholds**: <0.50 poor, 0.50–0.75 moderate, 0.75–0.90 good, >0.90 excellent, judged on the 95% CI. These were **confirmed only on secondary pages**, because the PMC full text (https://pmc.ncbi.nlm.nih.gov/articles/4913118) returned a reCAPTCHA page:
  - CASRAI guide (https://casrai.org/guides/intraclass-correlation-coefficient-icc): "below 0.50 is poor, 0.50 to 0.75 moderate, 0.75 to 0.90 good, and above 0.90 excellent". It adds that "Koo & Li's own guideline recommends basing the reliability judgment on the 95% confidence interval".
  - A Hrčak paper (https://hrcak.srce.hr/file/294894), Table 4, has the same bands (it labels 0.50–0.75 "Fair") and cites Koo & Li J Chiropr Med 2016;15(2):155-63.
- **Action**: open PMC4913118 in a browser and quote the abstract sentence before submission.

**Shrout & Fleiss 1979**
- Citation: Shrout PE, Fleiss JL. Intraclass correlations: uses in assessing rater reliability. *Psychological Bulletin*. 1979;86(2):420–428. doi:10.1037/0033-2909.86.2.420
- ScienceOpen (https://scienceopen.com/document/vid/9429399b-566e-4c60-9385-8745643be589) confirms the title, journal, year (March 1979), volume 86, issue 2, publisher APA and DOI 10.1037//0033-2909.86.2.420 (start page 420).
- **Not confirmed on a fetched page**: author names and end page 428. PubMed 18839484 returned a bot-check page.

**Recommendation for E4**: report the ICC form explicitly. Measurements are of the same images under different degradations, so the likely form is two-way, absolute agreement, single measurement (ICC(A,1) / ICC(2,1)). Give the 95% CI and interpret it with the Koo & Li bands.

## 6. Power, within-subject design, counterbalancing

**G\*Power (official HHU page)**: https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower
- Recommended citations (cite one or both):
  - Faul F, Erdfelder E, Lang A-G, Buchner A (2007). G\*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences. *Behavior Research Methods*, 39, 175–191.
  - Faul F, Erdfelder E, Buchner A, Lang A-G (2009). Statistical power analyses using G\*Power 3.1: Tests for correlation and regression analyses. *Behavior Research Methods*, 41, 1149–1160.
- Latest versions: 3.1.9.7 for Windows (17 Mar 2020) and 3.1.9.6 for macOS (21 Feb 2020).
- Free for everyone; commercial redistribution is prohibited.
- The 2007 citation is also confirmed on Uni Mannheim's page: https://www.sowi.uni-mannheim.de/en/erdfelder/research/software/gpower-3/
- DOIs not confirmed (Crossref unreachable).

**Cohen 1988 (Routledge page)**: https://www.routledge.com/Statistical-Power-Analysisfor-the-Behavioral-Sciences/Cohen/p/book/9780805802832
- Cohen J. *Statistical Power Analysis for the Behavioral Sciences*. 2nd ed. 1988. ISBN 9780805802832.
- The current publisher is Routledge. The page does not name the original publisher (Lawrence Erlbaum), and it gives the page count as both 567 and 590.

**Latin square counterbalancing**
- Reference: Acheson A. Sequence Effects. In: *Encyclopedia of Research Design*. SAGE Publications; 2010:1341. doi:10.4135/9781412961288.n411 (book doi:10.4135/9781412961288).
- Page: https://methods.sagepub.com/ency/edvol/embed/encyc-of-research-design/chpt/sequence-effects
- What it says:
  - Full within-subject counterbalancing "is only practical when there are relatively few experimental conditions".
  - Otherwise, "control for sequence effects using a balanced Latin square". "In a balanced Latin square, each condition is immediately preceded once by all other conditions."
  - Trade-off: "A balanced Latin square cannot control for sequence effects as completely as counterbalancing."
- The editor is not shown on the page.
- **Note for E3**: with 4 cases, a 4×4 balanced (Williams) Latin square needs N to be a multiple of 4. N = 34 is not; 32 or 36 would be.

## 7. Paired-comparison tests (official docs)

**Wilcoxon signed-rank**: https://docs.scipy.org/doc/scipy-1.18.0/reference/generated/scipy.stats.wilcoxon.html (SciPy 1.18.0)
- Signature: `wilcoxon(x, y=None, zero_method='wilcox', correction=False, alternative='two-sided', method='auto', *, axis=0, nan_policy='propagate', keepdims=False)`
- Tests whether paired differences are symmetric about zero.
- `zero_method` options: `wilcox` (drop zeros), `pratt`, `zsplit`.
- With `method='auto'`, the exact test is used when len(d) ≤ 50. With ties or zeros present, a permutation test is used when len(d) ≤ 13.

**McNemar**: https://statsmodels.org/dev/generated/statsmodels.stats.contingency_tables.mcnemar.html
- Signature: `mcnemar(table, exact=True, correction=True)`, taking a 2×2 table.
- `exact=True` uses the binomial distribution, with statistic min(n1, n2).
- `exact=False` uses chi-square; the continuity correction applies only in that case, and not when the off-diagonal counts are equal (changed in 0.15.1).

**Bootstrap CI**: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html (SciPy 1.18.0)
- Defaults: `n_resamples=9999`, `confidence_level=0.95`, `method='BCa'`. Other methods: 'percentile', 'basic'.
- `paired=True` resamples one shared set of indices across all samples, which is what a within-subject design needs.

**Holm correction**: https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html (statsmodels 0.15.0)
- Signature: `multipletests(pvals, alpha=0.05, method='hs', …)`
- `'holm'` is the "step-down method using Bonferroni adjustments".
- **The default is 'hs' (Holm–Šidák), so pass `method='holm'` explicitly.**
- Returns reject, pvals_corrected, alphacSidak, alphacBonf.

## 8. Precision / recall / F1 (scikit-learn 1.9.1)

**`precision_recall_fscore_support`**: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html
- Precision = tp/(tp+fp); recall = tp/(tp+fn). F-beta is the weighted harmonic mean, and beta = 1 weighs both equally. Support is the number of occurrences of each class in y_true.
- `average` options: None (per class), 'binary', 'micro', 'macro', 'weighted', 'samples'.
- `zero_division` accepts "warn", 0.0, 1.0 or np.nan (np.nan added in 1.3).

**Classification-metrics API list**: https://scikit-learn.org/stable/api/sklearn.metrics.html
- Includes `classification_report`, `multilabel_confusion_matrix`, `f1_score`, and others.
- User guide: https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics (linked from the API page, not fetched itself).

**For E1**: per-error-type P/R/F1 can use `average=None` with one label per error type. False alarms on error-free cases are the FP count of the "error present" class.

## 9. Readability

**Flesch Reading Ease formula**
- Formula: 206.835 − 1.015 × (words/sentence) − 84.6 × (syllables/word).
- Confirmed on https://readabilityformulas.com/learn-about-the-flesch-reading-ease-formula/ and in textstat's source code (English constants 206.835 / 1.015 / 84.6, `textstat/backend/utils/constants.py`).
- Citation: Flesch R. A new readability yardstick. *Journal of Applied Psychology*. 1948. Author, title, journal and year are confirmed. **Volume 32(3) and pages 221–233 are not confirmed**: PubMed 18867058 and Scilit were not reachable.

**Flesch–Kincaid Grade Level (DTIC PDF)**: https://apps.dtic.mil/sti/pdfs/ADA006655.pdf
- Citation: Kincaid JP, Fishburne RP Jr, Rogers RL, Chissom BS. *Derivation of New Readability Formulas (Automated Readability Index, Fog Count and Flesch Reading Ease Formula) for Navy Enlisted Personnel*. Research Branch Report 8-75. Millington, TN: Chief of Naval Technical Training, Naval Air Station Memphis; February 1975.
- Formula (Table 3): **GL = 0.39 × (words/sentence) + 11.8 × (syllables/word) − 15.59**
- Caveat: the text extracted from this PDF printed the original reading-ease syllable term as ".836 (syllables/100 words)". That conflicts with 84.6/word (= .846 per 100 words) in the other two sources and is probably an OCR error. Check the PDF visually.

**textstat (PyPI JSON + installed package)**: https://pypi.org/pypi/textstat/json
- Latest stable release: 0.7.13 (uploaded 2026-02-18), MIT licence; 1.0.0a1 is a pre-release. Repository: https://github.com/textstat/textstat
- The README language table covers en, de, es, fr, it, nl, pl, ru. The source code also has hu.
- **Romanian is NOT supported with its own formula.**
  - `set_lang('ro')` runs: syllables then come from Pyphen's Romanian hyphenation dictionary ('ro' and 'ro_RO' are available).
  - Unknown languages fall back to the **English** Flesch coefficients (`get_lang_cfg` in the source).
  - So Romanian scores are not validated. Tested: a Romanian two-sentence text gave FRE 36.6.
  - Note also that the English mode needs NLTK cmudict downloaded.
- **Thesis implication**: report readability on the English outputs only. For Romanian, either use a validated Romanian measure or say plainly that this is a limitation.

**Recommended reading levels for patient materials**

| Source | Recommendation | URL / notes |
|---|---|---|
| NLM MedlinePlus, "How to Write Easy-to-Read Health Materials" | "Keep within a range of about a 7th or 8th grade reading level". Recommends testing with readability tools and names New Dale-Chall, SMOG, Gunning FOG and Flesch-Kincaid Grade Level. | https://medlineplus.awsqa.nlm.nih.gov/etr.html. "Page last updated on 28 June 2017". The fetched host is an NLM "awsqa" mirror; the public URL (expected medlineplus.gov/etr.html) was not fetched. |
| AHRQ Health Literacy Universal Precautions Toolkit | "Even if your materials are written at the 4th or 6th grade level as recommended, some adults will not be able to read them." | https://www.ahrq.gov/health-literacy/improve/precautions/tool11.html |
| CDC Clear Communication Index | Scores out of 100: "Although 100 is an ideal score, 90 or higher is passing". 20 items, each scored 0/1. **Recommends no grade level.** | https://www.cdc.gov/ccindex/tool/faq.html |

## 10. Numeracy / comprehension / risk-communication guidance

**Objective numeracy**
- Lipkus IM, Samsa G, Rimer BK. General Performance on a Numeracy Scale among Highly Educated Samples. *Med Decis Making*. 2001;21(1):37–44. doi:10.1177/0272989X0102100105
- Page: https://ideas.repec.org/a/sae/medema/v21y2001i1p37-44.html
- The study tested 463 adults with a 3-item general scale and a 7-item expanded scale.

**Subjective Numeracy Scale**
- Fagerlin A, Zikmund-Fisher BJ, Ubel PA, Jankovic A, Derry HA, Smith DM. Measuring numeracy without a math test: Development of the Subjective Numeracy Scale. *Med Decis Making*. 2007;27(5):672–680. doi:10.1177/0272989X07304449
- Page: https://ideas.repec.org/a/sae/medema/v27y2007i5p672-680.html
- 8 items in 2 subscales of 4 (ability and preference). Correlation with the Lipkus scale was 0.63–0.68.

**Graph literacy**
- Galesic M, Garcia-Retamero R. Graph literacy. *Med Decis Making*. 2011;31(3):444–457. doi:10.1177/0272989X10373805
- Page: https://econpapers.repec.org/RePEc:sae:medema:v:31:y:2011:i:3:p:444-457

**Berlin Numeracy Test**
- Cokely ET, Galesic M, Schulz E, Ghazal S, Garcia-Retamero R. Measuring risk literacy: The Berlin Numeracy Test. *Judgment and Decision Making*. 2012;7(1):25–47. doi:10.1017/S1930297500001819
- Page: https://www.cambridge.org/core/journals/judgment-and-decision-making/article/measuring-risk-literacy-the-berlin-numeracy-test/A9B26516D12D48EFA4BD3560E2001E8E
- About 3 minutes. The adaptive version uses 2–3 of 4 items; there is also a 1-item version.

**IPDAS risk-communication primer**
- Trevena LJ, Zikmund-Fisher BJ, Edwards A, Gaissmaier W, Galesic M, Han PKJ, King J, Lawson ML, Linder SK, Lipkus I, Ozanne E, Peters E, Timmermans D, Woloshin S. Presenting quantitative information about decision outcomes: a risk communication primer for patient decision aid developers. *BMC Med Inform Decis Mak*. 2013;13(Suppl 2):S7. doi:10.1186/1472-6947-13-S2-S7
- Pages: full text https://orca.cardiff.ac.uk/110573/1/1472-6947-13-S2-S7.pdf; metadata/DOI https://deepblue.lib.umich.edu/handle/2027.42/116070?show=full
- Recommendations quoted from the full text:
  - "absolute risks should be given either in percentages or simple frequencies". Relative-risk formats "tend to magnify risk perceptions and decrease understanding".
  - "Consistent denominators should always be used."
  - "visual aids are most effective for comprehension when the entire population at risk is shown". This supports a full icon array, e.g. 100 icons.
  - "all visual aids should be pilot tested for understanding (not simply preferences)".
  - Framing effects (gain vs loss) "tend to vary across situations".
- The text extraction read only the first ~100k characters of the PDF. No sentence naming "icon array" explicitly was returned, but the population-shown recommendation was.

## 11. SUS

**Bangor 2008**
- Bangor A, Kortum PT, Miller JT. An Empirical Evaluation of the System Usability Scale. *Int J Hum–Comput Interact*. 2008;24(6):574–594. doi:10.1080/10447310802205776
- Page: https://bibbase.org/network/publication/aaronbangor-miller-anempiricalevaluationofthesystemusabilityscale-2008

**Bangor 2009 (adjective scale)**: https://uxpajournal.org/wp-content/uploads/sites/7/pdf/JUS_Bangor_May2009.pdf
- Citation: Bangor A, Kortum P, Miller J. Determining what individual SUS scores mean: Adding an adjective rating scale. *J Usability Stud*. 2009;4(3):114–123.
- Mean SUS by adjective (Table 3, n = 959):

| Adjective | Mean SUS |
|---|---|
| Worst Imaginable | 12.5 |
| Awful | 20.3 |
| Poor | 35.7 |
| OK | 50.9 |
| Good | 71.4 |
| Excellent | 85.5 |
| Best Imaginable | 90.9 |

- Overall mean across surveys: 69.5 ("about 70").

**Lewis 2018 (IJHCI)**
- Lewis JR. The System Usability Scale: Past, Present, and Future. *Int J Hum–Comput Interact*. 2018;34(7):577–590. doi:10.1080/10447318.2018.1455307
- Confirmed via a library catalogue record: https://vufind-test.katalog.k.utb.cz/SummonRecord/FETCH-LOGICAL-c281t-cde89825959c462eb591958b5b82d8c3abf75bdcbcce11851923df9eaf608c4d3
- The abstract shown there did not mention 68.

**Mean SUS ≈ 68 benchmark**: https://uxpajournal.org/wp-content/uploads/sites/7/pdf/JUS_Lewis_May2018.pdf
- Citation: Lewis JR, Sauro J. Item benchmarks for the System Usability Scale. *J Usability Stud*. 2018;13(3):158–167.
- "a SUS score of 68 (an average overall system score)" (p. 163). 68 is at the centre of the "C" band on the Sauro–Lewis curved grading scale (C = 65.0–71.0; A = 80.8–84.0; F < 51.7), based on 241 industrial studies.
- An SUS of 80 is "a common industrial goal".

## 12. Reporting guidelines

**TRIPOD+AI**: https://epub.ub.uni-muenchen.de/116670/1/bmj-2023-078378.full.pdf (author-accepted PDF of the BMJ article; "Cite this as" line)
- Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ* 2024;385:e078378. doi:10.1136/bmj-2023-078378
- Published online 16 April 2024.
- 27 main items (52 subitems); a separate 13-item checklist covers abstracts.
- The words of the title after "clinical prediction models" were not confirmed; check them on bmj.com.

**CLAIM 2024**: https://escholarship.org/content/qt9zf6q2rb/qt9zf6q2rb.pdf
- Tejani AS, Klontzas ME, Gatti AA, Mongan JT, Moy L, Park SH, Kahn CE Jr; CLAIM 2024 Update Panel. Checklist for Artificial Intelligence in Medical Imaging (CLAIM): 2024 Update. *Radiol Artif Intell* 2024;6(4):e240300. doi:10.1148/ryai.240300
- 44 items; published 1 July 2024.

## 13. Accuracy evaluation in data-to-text

**ACL Anthology page**: https://aclanthology.org/2020.inlg-1.22
- Thomson C, Reiter E. A Gold Standard Methodology for Evaluating Accuracy in Data-To-Text Systems. In: *Proceedings of the 13th International Conference on Natural Language Generation*, pp. 158–168. Dublin, Ireland: ACL; December 2020. doi:10.18653/v1/2020.inlg-1.22
- The authors "propose a methodology for high-quality human evaluation of the accuracy of generated texts".
- **For E2**: use their error-annotation approach (classify each factual error, e.g. incorrect number) to count hallucinated numbers per output.

---

## NOT CONFIRMED (verify before citing)

**ChestX-ray14 and Kaggle**
1. 112,120 images / 30,805 patients / 14 labels: found only on a third-party Hugging Face card. Check README_CHESTXRAY.pdf at https://nihcc.app.box.com/v/ChestXray-NIHCC
2. Kaggle sample (5,606 images, 5%, licence): kaggle.com could not be fetched.

**Thresholds and citation details**
3. Koo & Li ICC thresholds: confirmed only via secondary sources. The PMC full text was blocked by a reCAPTCHA page.
4. Shrout & Fleiss: author names and end page 428.
5. Flesch 1948: volume, issue and pages (32(3):221–233).
6. The DTIC extraction of the original Flesch syllable coefficient (".836"): probably OCR; check visually.
7. Cohen 1988: original publisher (Lawrence Erlbaum) and page count.
8. TRIPOD+AI: full subtitle wording.
9. The Lewis 2018 IJHCI paper's own statement of mean 68. The 68 figure is confirmed from Lewis & Sauro 2018 JUS instead.

**Not checked against official sources**
10. All DOIs were confirmed on publisher, catalogue or indexing pages, **not via the Crossref API** (blocked). G\*Power 2007/2009 DOIs were not confirmed at all.
11. Licence text for CheXphoto on Redivis: the AIMI dataset page's "License" section was empty. The AIMI policy states only "non-commercial research, subject to applicable data use terms".
12. PadChest journal name (only DOI 10.1016/j.media.2020.101797 was shown).
13. Public MedlinePlus URL (fetched from an NLM "awsqa" mirror).
14. Editor of the SAGE *Encyclopedia of Research Design*.
