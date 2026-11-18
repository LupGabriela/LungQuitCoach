# 02 — Related work: similar existing applications

Thesis prototype: **Lung Health & Quit Coach**. It is a research prototype, not a medical device. It computes PLCOm2012 6-year risk, projects quit/continue/increase scenarios, can optionally run open chest X-ray models (TorchXRayVision, CXR-Lung-Risk), and adds LLM plain-language explanations. The LLM writes only placeholders, and a rule-based verifier checks every text, with a template fallback. It runs offline on a laptop.

**Sourcing rule.** Every statement below comes from a page fetched in this session (18 Nov 2026). If a page did not say something, the report says "not stated" or "not publicly documented". Where a technology detail comes from observable evidence (an FDA summary, an R manual, app-store metadata, page markup), the source is named. The "Lacks vs. prototype" lines compare only against features that were verified.

---

## Group 1 — Online / downloadable lung cancer risk calculators

### 1.1 PLCOm2012 family of spreadsheet calculators (Brock University)
- **Operator:** Hosted at brocku.ca. The page cites research by Tammemägi, Katki, Church, Berg and others. The page itself does not name an operating unit.
- **URL fetched:** https://brocku.ca/lung-cancer-risk-calculator
- **Target user:** Offered "for public non-profit use" to individuals, universities, research institutes and non-profit hospitals or practices. Users must fill in a registration form before downloading.
- **Features:**
  - **Models:** PLCOm2012 (6-year lung cancer risk in ever-smokers); PLCOall2014 (also covers never-smokers; correlation with PLCOm2012 >0.99); PLCOm2012noRace (race predictor removed; reported AUC 0.796 vs 0.797); PLCO2012results (updates the risk with screening results).
  - **Nodule malignancy calculators:** full and parsimonious versions (McWilliams et al. 2013).
  - **Output:** probability estimates.
  - **Not offered:** plain-language interpretation, quit-smoking scenarios, numeric eligibility thresholds.
- **Technology:** Downloadable spreadsheets only. The page mentions no web or mobile app, and nothing else about the implementation is documented.
- **Lacks vs. prototype:** No web UI, no scenario projection, no plain-language explanation or verification, no imaging input. Use is limited to non-profit purposes, and download requires registration.

### 1.2 shouldiscreen.com (University of Michigan)
- **Operator:** University of Michigan School of Public Health; lead developer Rafael Meza. The page describes it as "endorsed by the American College of Radiology" (Rogel Cancer Center page).
- **URLs fetched:**
  - https://www.rogelcancercenter.org/node/2266
  - https://www.rogelcancercenter.org/node/3432
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8175495 (Kates et al., *J Gen Intern Med* 2021;36(6):1543–1552)
  - Hung, Lau, Ackerman, Meza, "Designing a Web-based Decision Aid for Individuals to Consider Lung Cancer Screening", PervasiveHealth'19 (author-hosted PDF at peiyaoh.github.io)
  - shouldiscreen.com itself could **not** be fetched.
- **Target user:** Patients and the public (a patient-facing decision aid).
- **Features:**
  - Calculates a 6-year lung cancer risk from age, smoking history, weight, height and other information, and checks eligibility against USPSTF criteria (Rogel).
  - Explains why screening is suggested, what happens during a CT, and radiation exposure, and offers help with smoking cessation (Rogel).
  - Kates et al. list its model as **PLCO**, with output given as a 6-year percentage plus a screening recommendation.
  - Built in 2014 following the Ottawa Decision Support Framework; meets IPDASi and CMS criteria (Hung et al.).
  - Evaluated in a 60-participant study, which found improved knowledge (Rogel).
- **Technology:** Not publicly documented. Hung et al. do not state the stack.
- **Lacks vs. prototype:** The fetched sources describe no quit/continue/increase projection, no imaging input and no offline use. Its explanations are static, human-written content, so there is no generated text and no verification step. Its code is not documented as open source.

### 1.3 NCI DCEG lung cancer risk models: lcrisks / LCmodels R packages and Excel tool
- **Operator:** U.S. National Cancer Institute, Division of Cancer Epidemiology and Genetics (Biostatistics Branch). Contact: Li Cheung.
- **URLs fetched:**
  - https://dceg.cancer.gov/tools/risk-assessment/lcrisks
  - https://dceg.cancer.gov/tools/risk-assessment/lcmodels
  - https://dceg.cancer.gov/tools/risk-assessment/lcrisks/Manual-lcrisk.pdf
  - https://dceg.cancer.gov/research/public-health-impact/lung-screening
- **Target user:** Researchers and analysts.
- **Features:**
  - **lcrisks models:** LCRAT (incidence), LCDRAT (lung cancer death), a model for deaths from other causes, overall mortality, and a polytomous model for false-positive CT screens.
  - **lcrisks outputs:** USPSTF eligibility; lung cancer deaths per 1,000 without screening; deaths averted per 1,000 with 3 annual screens; diagnoses per 1,000; extra diagnoses from screening; false positives per 1,000; life-expectancy gain and life-years gained (LYFS-CT); counterfactual-race versions of some outputs.
  - **Inputs:** age, sex, years smoked, years quit, cigarettes per day, race, COPD/emphysema, parental lung cancer, BMI and education, plus prior cancer, 11 comorbidities and year of assessment for LYFS-CT. Prediction horizon up to 10 years. Covers ages 40–98 (manual).
  - **LCmodels:** adds published models (Bach 2003, Spitz 2007, LLP 2008, Hoggart 2012, Tammemägi 2013, LLPi 2015, Pittsburgh 2015, Katki 2016/2018, LYFS-CT 2019).
  - DCEG also says the team "created an online lung-cancer screening risk-tool" at analysistools.nci.nih.gov/lungCancerScreening/. That tool could not be fetched.
- **Technology (documented):**
  - R package (Windows zip, Linux tar.gz) plus an Excel tool (lcrisk_tool.xlsx).
  - Manual for lcrisks v4.1.1 (2023-07-05): Depends R (>= 4.0); Imports survival, VGAM; **License GPL-2**; authors Cheung, Kovalchik, Katki.
  - The download pages also link to a separate License Agreement whose terms are not shown on the pages.
- **Lacks vs. prototype:** Not patient-facing and gives no plain-language explanation. Its scenarios are screening vs. no screening (and counterfactual race), not quit/continue/increase smoking. No imaging input. Its strength is that it covers many more validated models.

### 1.4 MSK "Is a Lung Screening Right for You?" (Memorial Sloan Kettering)
- **Operator:** Memorial Sloan Kettering Cancer Center.
- **URL fetched:** https://www.mskcc.org/cancer-care/types/lung/screening/lung-screening-decision-tool
- **Target user:** Patients (people who smoke or used to smoke).
- **Features:**
  - Short eligibility quiz: age, current or former smoking, amount per day and years smoked.
  - Follows "the recommendations of the National Lung Screening Trial and the United States Preventive Services Taskforce".
  - If the user is eligible, it directs them to book screening.
  - Shows no numeric risk, no benefit/harm display and no scenarios.
  - Note: Kates et al. (2021) listed mskcc.com as using the CARET model. The page as fetched today names no model.
- **Technology (observable in page markup, per fetch):** Drupal 10 site, JavaScript form, Google Tag Manager. The scoring method is not documented.
- **Lacks vs. prototype:** Criteria-based rather than a validated risk model, and gives no numeric risk. No scenarios, no imaging input, no generated explanations, no offline use.

### 1.5 Other web calculators catalogued in a peer-reviewed comparison (Kates et al., 2021)
- **URL fetched:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8175495
- **Content:** The study compared 10 web-based lung cancer risk calculators, including:
  - mylungrisk.org (LLP, 5-year %)
  - merckmanuals.com (PLCO, 6-year %)
  - aats.org (PLCO, Hoggart, LLP, Spitz)
  - analysistools.nci.nih.gov (PLCO, HUNT; 5-year)
  - siteman.wustl.edu (SEER; qualitative thermometer/risk ladder)
  - mycanceriq.ca (qualitative low/intermediate/high)
  - omnicalculator.com and mensxmachina.org (HUNT)
- **Key finding:** Even calculators based on the same PLCO model gave inconsistent estimates for the same hypothetical patients. The authors call for standardization before such tools are used as decision aids.
- **Relevance to the thesis:** This supports the prototype's choice of one fixed, documented PLCOm2012 implementation that is unit-tested against the reference coefficients.
- **Note:** These calculators are listed for context only. Their sites were not fetched individually, and the myLungRisk paper page was not reachable.

---

## Group 2 — National screening programmes / recommendations that use these models

### 2.1 NHS England: Targeted Lung Health Check (TLHC), now the Lung Cancer Screening Programme
- **Operator:** NHS England (protocol prepared by the Lung Clinical Expert Advisory Group).
- **URLs fetched:**
  - https://www.england.nhs.uk/wp-content/uploads/2019/02/B1646-standard-protocol-targeted-lung-health-checks-programme-v2.pdf ("Standard protocol prepared for the Targeted Lung Health Checks Programme", v2, 7 Nov 2022, PR1646)
  - https://www.england.nhs.uk/wp-content/uploads/2019/02/2502-B1647-quality-assurance-standards-prepared-for-the-lung-cancer-screening-programme.pdf ("Quality assurance standards prepared for the Lung Cancer Screening Programme", v3, 3 Feb 2025, PR1647)
- **Target user:** People aged 55–74 who have ever smoked (a population programme run through nurse-led lung health checks).
- **Features (verified thresholds):**
  - The person is referred for LDCT if **PLCOm2012 ≥1.51% risk over six years** OR **LLPv2 ≥2.5% risk over five years**, provided they meet no exclusion criteria.
  - PLCOm2012 is used in a version adapted to UK ethnic groups.
  - A 2.0% LLP threshold was considered and rejected because it would mean substantially more LDCTs.
  - Current smokers get opt-out referral to smoking cessation services, including pharmacotherapy. Staff must complete Very Brief Advice training, and the target is that 100% of current smokers are offered an intervention.
  - Participant information must be in "plain English", with easy-read and video material, and the focus is on "informed choice".
- **Technology:**
  - The risk-calculation software or IT system is not named ("validated lung cancer risk assessment tools").
  - The QA standards require patient administration software that supports recall and audit, and CT reporting software with computer-aided detection and nodule volumetry. Brock nodule scores are computed automatically in commercial reporting software.
- **Lacks vs. prototype:** This is a clinical service, not a self-service app. Explanations come from nurses and printed material, and the documents describe no individual quit/continue scenario display. Imaging is LDCT, not chest X-ray. **Relevance:** It is the strongest evidence that PLCOm2012 with the 1.51% threshold is used operationally, which justifies the prototype's model choice.

### 2.2 USPSTF 2021 lung cancer screening recommendation (USA)
- **Operator:** U.S. Preventive Services Task Force.
- **URL fetched:** https://www.uspreventiveservicestaskforce.org/uspstf/sites/default/files/file/supporting_documents/lung-cancer-newsbulletin.pdf (official bulletin; the main recommendation page was not reachable)
- **Content (verified):**
  - Dated March 9, 2021; grade B.
  - Yearly LDCT for people aged **50–80** with **≥20 pack-years** who **currently smoke or quit within the last 15 years**.
  - The bulletin does not mention risk prediction models.
- **Relevance:** USPSTF uses criteria, not a risk model. Several tools (shouldiscreen.com, lcrisks, MSK) report USPSTF eligibility next to model-based risk. The prototype can show both.

### 2.3 Romania: what could be confirmed
- **National project "Screeningul Cancerului Pulmonar – Program Național de Detectare Precoce"** (SMIS 346295):
  - **Beneficiary:** Institutul de Pneumoftiziologie „Marius Nasta".
  - **Partners:** INSP, UMF „Carol Davila", Fundația Centrul pentru Politici și Servicii de Sănătate, Asociația Română Anti-SIDA.
  - **Funding:** Programul Sănătate (POS), Priority 1, co-financed by FSE+.
  - **Budget and duration:** total eligible value 82,032,595.75 lei; 50 months.
  - **Target:** screening at least 21,695 people from a vulnerable target group of 27,118.
  - **URL fetched:** https://umfcd.ro/wp-content/uploads/2025/12/Comunicat_presa_lansare-proiect_noiembrie2025.pdf (launch press release, Nov 2025)
- **National methodology** ("Metodologie screening cancer pulmonar", 2026; Marius Nasta Institute with the Ministry of Investments and European Projects and the Ministry of Health; reviewed by the CMR Pneumology Commission):
  - Eligibility: age 50–75, ≥20 pack-years, current smokers or quit within 15 years. Heated-tobacco and vape users count as smokers.
  - **No validated risk model (e.g., PLCOm2012) is named.** Recruitment uses a risk questionnaire (Annex A) and a mapping of administrative units by cumulative risk.
  - LDCT at 1–1.5 mSv; Lung-RADS reporting.
  - Participation is conditional on consent to an anti-tobacco intervention (Fagerström and Schneider tests, counselling, NRT).
  - A National Lung Screening Registry is planned at INSP. No app is mentioned.
  - **URLs fetched:** https://www.cmr.ro/wp-content/uploads/2026/03/Metodologie-screening-cancer-pulmonar_CMR.pdf, and the CMR press release of 1 Aug 2026 (https://agerpres.ro/comunicate/2026/08/01/comunicat-de-presa---colegiul-medicilor-din-romania--1581406). The press release says the first stage targets high-risk vulnerable groups.
- **EU SOLACE project** (EU4Health, GA 101101187, 1 Apr 2023 – 31 Mar 2026; coordinator EIBIR):
  - Romania is a participating country.
  - The Romanian partner is **UMF „Carol Davila" Bucharest**, responsible for WP2 (Knowledge Hub) and WP3 (Implementation Network); coordinator Dr. Rodica Anghel.
  - The DKFZ project map marks "an implementation plan project in Romania".
  - None of the fetched pages names a Romanian pilot site.
  - **URLs fetched:** https://health.ec.europa.eu/system/files/2023-08/fs_cancer_solace.pdf, https://old.umfcd.ro/en/?p=14460, https://www.dkfz.de/en/cancer-epidemiology/eu-solace-strengthening-the-screening-of-lung-cancer-in-europe
- **Relevance:** Romania's methodology uses USPSTF-like criteria plus a questionnaire, without an individual validated risk model. A PLCOm2012-based, Romanian-context explainer is therefore a real gap. This is a framing argument, not a clinical claim.

---

## Group 3 — Quit-smoking apps and services from health authorities

### 3.1 NHS Quit Smoking app (England)
- **Operator:** Department of Health and Social Care (Digital), the App Store seller. DHSC is also the data controller.
- **URLs fetched:**
  - https://apps.apple.com/gb/app/nhs-quit-smoking/id687298065
  - https://www.nhs.uk/better-health/quit-smoking/
  - https://www.nhs.uk/better-health/privacy-policy/privacy-policy-for-the-nhs-quit-smoking-app
- **Target user:** Adult smokers (App Store age rating 18+).
- **Features:**
  - 28-day quit programme with weekly guides, missions and "tailored clinical advice".
  - Home-screen focus on smokefree streak, money saved or daily health benefits; editable cigarette cost.
  - Badges; "and breathe!" craving tool; stories from other quitters.
  - The NHS page adds a separate online 8-step Personal Quit Plan.
- **Technology:**
  - Native iOS app (iOS 15+, 64.7 MB, version 5.6.1) and an Android version (Google Play, per the NHS page).
  - The release notes mention the **Branch.io SDK** (used for attribution).
  - Privacy policy: "All your progress and data are stored locally on your device", but anonymised activity and analytics data are collected, "encrypted at rest and in transit", and "stored and processed in the United Kingdom".
  - Nothing else is publicly documented.
- **Lacks vs. prototype:** No lung cancer risk model, no risk projection for quit vs. continue, no imaging input, no generated or verified explanations. English only.

### 3.2 quitSTART (NCI Smokefree.gov)
- **Operator:** Smokefree.gov, created by the NCI Tobacco Control Research Branch together with the U.S. FDA. The App Store seller is **ICF International, Inc.**
- **URLs fetched:** https://www.smokefree.gov/apps/, https://apps.apple.com/us/app/quitstart-quit-smoking/id494552000
- **Target user:** Adult smokers.
- **Features:** Preparation tips; progress tracking and badges; help after a slip; managing cravings and moods; games and challenges; a "Quit Kit"; social sharing. The App Store listing says it "takes the information you provide about your smoking history and gives you tailored tips".
- **Status:** Listed as available (App Store v2.48). No discontinuation notice on smokefree.gov.
- **Technology:** iOS 11+ (also listed for Apple-silicon Mac and visionOS). Data collected but not linked to identity: identifiers, usage data, crash data. Nothing else is publicly documented.
- **Lacks vs. prototype:** No risk model, no scenario projection, no imaging input, no LLM explanation.

### 3.3 QuitGuide (NCI Smokefree.gov)
- **Operator:** NCI Tobacco Control Research Branch.
- **URL fetched:** https://smokefree.gov/apps-quitguide
- **Features:** Logs cravings, moods and slips with their triggers; reasons for quitting; tips and distractions; milestone tracking; journal. The page notes: "Advanced functionality currently only available for Apple users."
- **Status:** The page offers iOS and Android download links and shows no discontinuation notice. Current availability in the stores was not checked.
- **Technology:** iOS and Android. Nothing else is publicly documented.
- **Lacks vs. prototype:** Same gaps as quitSTART.

### 3.4 WHO QuitTobacco app (WHO South-East Asia Regional Office)
- **Operator:** World Health Organization – SEARO. Launched 15 Feb 2022 in New Delhi.
- **URLs fetched:** https://www.who.int/southeastasia/news/detail/15-02-2022-who-launches-quit-tobacco-app, https://apps.apple.com/us/app/who-quittobacco/id1609277771
- **Target user:** Users of any form of tobacco, including smokeless and newer products.
- **Features:** Health Improvement Tracker; cost-savings calculator; personal quit plan (triggers, strategies); motivation journal; linking supporters; craving diary and craving-management view; personal challenges.
- **Technology:** Free on iOS and Android, v1.4 on iOS. The listing says Health & Fitness data and identifiers may be "collected and linked to your identity". Languages, offline capability and stack are not documented.
- **Lacks vs. prototype:** No lung cancer risk model or scenario projection, no imaging input, no LLM explanation.

### 3.5 Romania: national quitline (TelVerde) and stopfumat.eu
- **Operator:** Not confirmed. The leaflet was produced under the Ministry of Health's health evaluation and promotion subprogramme ("subprogramului de evaluare și promovare a sănătății").
- **URLs fetched:**
  - https://www.who.int/campaigns/world-no-tobacco-day/2021/quitting-toolkit/toll-free-quitlines
  - https://dsp-gorj.centruldecalcul.ro/wp-content/uploads/2022/11/6.-Pliant-ZNT.pdf (public-health leaflet)
- **Verified facts:**
  - WHO lists Romania's "National quit line: 0800 878 673" and the cessation website stopfumat.eu.
  - The leaflet says "Apelează Telverde gratuit: 0800878673" and "Accesează: www.stopfumat.eu".
  - **Note:** the number 0800 878 **778** was not confirmed anywhere. The verified number is **0800 878 673**.
- **Features:** Phone counselling line and a website. The site itself could not be fetched, so its features are not verified.
- **Technology:** Not publicly documented.
- **Lacks vs. prototype:** No app was found, no risk estimate, no scenarios.

---

## Group 4 — Patient-facing AI/LLM explanation tools for medical results

### 4.1 RadGPT (Stanford Medicine, Department of Radiology)
- **Operator:** Stanford radiology with Stanford HAI. Lead author Sanna E. Herwald; senior author Curtis Langlotz.
- **URLs fetched:** https://hai.stanford.edu/news/new-large-language-model-helps-patients-understand-their-radiology-reports, https://radiologybusiness.com/topics/health-it/enterprise-imaging/radgpt-system-improves-radiology-report-readability-and-ready-immediate-use
- **Publication:** *Journal of the American College of Radiology*, June 2025 (per Stanford HAI). The paper itself was not fetched.
- **Target user:** Patients reading radiology reports (X-ray, CT, MRI, ultrasound, PET, angiography).
- **Features:**
  - Extracts key concepts from the radiologist's report impression and explains each in plain language.
  - Generates concept-based and report-based Q&A pairs and suggested follow-up questions.
  - Works only on an existing radiologist report, not on raw images.
- **Verification:** Human only. Five radiologists (one radiologist and four residents, per Radiology Business) rated the outputs with a rubric and reported no answers that could be misconstrued. **No automated verifier is described.**
- **Status:** Research stage; "still has to be tested in a clinical setting".
- **Technology:** LLM-based. The base model is not named in the fetched sources, so it is treated as not publicly documented here.
- **Lacks vs. prototype:** No risk model, no scenarios, no image input. Its safety relies on human review rather than a run-time rule-based check with a template fallback.

### 4.2 Stanford EHR-integrated generative AI for drafting test-result explanations
- **Operator:** Stanford Health Care. Study in *JAMA Network Open* (lead author Shreya J. Shah), reported 8 Sep 2025.
- **URL fetched:** https://appliedradiology.com/articles/stanford-tests-ai-tool-to-help-clinicians-explain-imaging-and-lab-results
- **Target user:** Primary care clinicians. Patients receive the edited message through the portal.
- **Features:**
  - Drafts plain-language explanations of lab, imaging and pathology results.
  - The physician reviews and edits each draft before sending.
  - Of 93 surveyed clinicians, about 85% found it easy to use, 71% reported efficiency gains and 72% reported better explanations.
- **Technology:** **Claude 3.5 Sonnet (Anthropic)**, integrated into the electronic health record. The EHR vendor is not named.
- **Verification:** Human (the physician) in the loop. Accuracy and completeness were the most common concerns. No automated checker is described.
- **Lacks vs. prototype:** Not directly patient-facing, cloud LLM rather than offline, no automated verification, no risk model or scenarios.

---

## Group 5 — Regulated chest X-ray AI (clinician-facing)

### 5.1 Lunit INSIGHT CXR / Lunit INSIGHT CXR Triage (Lunit, South Korea)
- **URLs fetched:**
  - https://www.lunit.io/en/?p=824 (CE mark press release, 20 Nov 2019)
  - https://www.lunit.io/en/?p=906 (RCT press release, 13 Feb 2023)
  - https://www.lunit.io/en/?p=861 (FDA press release, 15 Nov 2021)
  - FDA K230899 summary (below), which cites Lunit INSIGHT CXR Triage as **K211733**
- **Regulatory status:**
  - INSIGHT CXR (v3) is **CE-marked** (2019; class and MDD/MDR route not stated on the fetched pages).
  - INSIGHT CXR Triage has **FDA 510(k)** clearance (2021) for triage of pleural effusion and pneumothorax.
- **Target user:** Radiologists and healthcare institutions (clinician-facing).
- **Features:**
  - Detects 10 common chest abnormalities, including nodule, calcification, pneumothorax, consolidation and fibrosis, plus TB screening.
  - Shows lesion location with an abnormality score and a case report.
  - Lunit reports an RCT showing higher actionable-nodule detection with AI (0.59% vs 0.25%).
- **Technology:** "Deep learning" (general company description). Architecture and deployment details are not publicly documented on the fetched pages.
- **Lacks vs. prototype:** Not patient-facing, no smoking-risk model, no quit scenarios, no plain-language patient explanation. It is a commercial closed product. On the other hand, it is regulated and clinically validated, which the prototype is not.

### 5.2 qXR (Qure.ai, India)
- **URLs fetched:** https://qure.ai/regulatory-and-privacy, https://www.accessdata.fda.gov/cdrh_docs/pdf23/K230899.pdf
- **Regulatory status:**
  - qXR v4.0: **Class IIb CE under EU MDR**. qXR v3.1: Class IIa under MDD.
  - FDA 510(k) clearances: qXR-LN (pulmonary nodules; K-number not given on the page), qXR-BT (K212690), **qXR-PTX-PE (K230899, 22 Aug 2023; product code QFM; 21 CFR 892.2080; Class II)**, qXR-CTR (K231149).
  - Company certifications: ISO 13485 (MDSAP), IEC 62304, ISO 27001.
- **Target user:** "Radiologists, clinicians, and other appropriately trained medical specialists" (K230899). qXR-LN is designed "to aid radiologists, pulmonologists and ER physicians" as a second reader.
- **Features:** Nodule marking (qXR-LN), breathing-tube position, pneumothorax and pleural-effusion triage, cardiothoracic ratio.
- **Technology (from the FDA 510(k) summary):**
  - "Artificial intelligence algorithm" on adult frontal (AP/PA) chest X-rays in **DICOM**; vendor-agnostic.
  - Runs automatically after acquisition through PACS and places output in the PACS worklist.
  - Training data about 74% India, 20% EU, 3.9% US.
  - Not for stand-alone clinical decisions.
- **Lacks vs. prototype:** Same as Lunit: clinician-facing, no risk model or scenarios, no patient explanations, closed source.

---

## Comparison matrix

Legend: **Y** = verified yes; **N** = verified no, or not offered on the fetched pages; **P** = partial; **?** = not publicly documented or not verified; **n/a** = not applicable.

| Tool | Validated risk model | Scenarios | X-ray input | Plain-language explanation | Explanation verification | Offline | Open source | Patient-facing |
|---|---|---|---|---|---|---|---|---|
| **Lung Health & Quit Coach (thesis)** | Y (PLCOm2012) | Y (quit / continue / increase) | Y (optional, open models) | Y (LLM, placeholders only) | Y (rule-based verifier + template fallback) | Y | Uses open models; own licence ? | Y (research prototype) |
| Brock PLCOm2012 spreadsheets | Y (PLCOm2012, PLCOall2014, noRace, results) | N | N | N | n/a | Y (download) | N (non-profit use, registration) | P (individuals allowed; no lay UI) |
| shouldiscreen.com (U. Michigan) | Y (PLCO, per Kates 2021) | ? | N | Y (static, human-written) | n/a (human-authored) | N (web) | ? | Y |
| NCI lcrisks / LCmodels | Y (LCRAT, LCDRAT, LYFS-CT, Bach, LLP, …) | P (screening vs. none) | N | N | n/a | Y (R / Excel) | Y (GPL-2 per manual; separate licence agreement) | N |
| MSK lung screening quiz | N (NLST/USPSTF criteria) | N | N | P | n/a | N | ? | Y |
| NHS England TLHC / LCSP | Y (PLCOm2012 ≥1.51%/6y; LLPv2 ≥2.5%/5y) | N | N (LDCT) | Y (plain English, nurse-led) | Human (clinician) | n/a | n/a | Y (service) |
| USPSTF 2021 | N (age/pack-year criteria) | N | N (LDCT) | P (bulletin) | n/a | n/a | n/a | P |
| Romania national LC screening (SMIS 346295) | N (criteria + questionnaire) | N | N (LDCT) | ? | n/a | n/a | n/a | Y (service) |
| NHS Quit Smoking app | N | P (money saved / streak) | N | Y (static advice) | n/a | P (progress stored on device) | ? | Y |
| quitSTART (NCI) | N | N | N | Y (static tailored tips) | n/a | ? | ? | Y |
| QuitGuide (NCI) | N | N | N | Y (static tips) | n/a | ? | ? | Y |
| WHO QuitTobacco | N | P (cost savings / health tracker) | N | Y (static) | n/a | ? | ? | Y |
| Romania TelVerde 0800 878 673 / stopfumat.eu | N | N | N | Y (phone counselling) | Human | n/a | n/a | Y |
| RadGPT (Stanford) | N | N | N (report text only) | Y (LLM) | Human evaluation only | ? | ? | Y (research) |
| Stanford EHR result-explanation drafts | N | N | N | Y (LLM, Claude 3.5 Sonnet) | Human (physician edits) | N (cloud LLM) | N | P (via clinician) |
| Lunit INSIGHT CXR | N | N | Y (CE; Triage FDA K211733) | N | n/a | ? | N | N |
| qXR (Qure.ai) | N | N | Y (CE MDR IIb; several FDA 510(k)s) | N | n/a | ? | N | N |

**Synthesis.** No verified tool combines a validated individual risk model, quit/continue scenarios, optional imaging input, and LLM explanations protected by automated verification.
- **Risk tools:** either research-grade without a lay UI (Brock, NCI) or patient-facing with static content (shouldiscreen.com).
- **Quit apps:** have no risk model.
- **LLM explanation tools:** rely on human review (RadGPT, Stanford).
- **Regulated CXR AI:** clinician-only.

The prototype's distinctive contribution is the **automated, rule-based verification of LLM output with a template fallback, running offline**. Its main limitation relative to Group 5 and Group 2 is the absence of regulatory approval and clinical validation.

---

## Could not verify

- **shouldiscreen.com:**
  - The site itself and the PMC article PMC5544524 could not be fetched (allowlist / captcha).
  - The model is given only as "PLCO" by Kates et al. (2021); whether this is PLCOm2012 specifically was not confirmed.
  - Scenario features and Spanish-language availability were not confirmed.
- **myLungRisk / Liverpool Lung Project calculator:** The paper page (XJTLU repository) and mylungrisk.org were not reachable. Only Kates et al.'s listing (LLP, 5-year %) was verified.
- **NCI online tool** (analysistools.nci.nih.gov/lungCancerScreening/): not fetchable. Its existence is stated by the DCEG page only.
- **USPSTF main recommendation page:** not fetchable. Criteria were verified from the official USPSTF bulletin PDF on the same domain.
- **NHS England LCSP rollout timeline:** The national rollout dates and current programme pages were not fetched.
- **Romania:**
  - Whether screening under SMIS 346295 has actually started, and in which regions.
  - The SOLACE Romanian pilot site, if any.
  - **4-IN-THE-LUNG-RUN** Romanian involvement (not researched before the search budget ran out).
  - The ADR Centru call PDF (fetch failed).
- **Romanian quitline operator:** The operator of the TelVerde line 0800 878 673 and of stopfumat.eu (stopfumat.eu was not fetchable). The program name "Stop fumatul" as an official title was not confirmed. The number 0800 878 778 given in the brief was not found.
- **QuitGuide:** current App Store / Google Play availability was not checked.
- **RadGPT:** the base LLM and the JACR paper's methods section were not fetched.
- **Lunit INSIGHT CXR:** the CE class and MDR (vs. MDD) status were not stated on the fetched official pages.
- **qXR-LN:** FDA K-number not given on the fetched page.
- **Technology stacks** of the NHS Quit Smoking app (beyond the Branch.io SDK), quitSTART, QuitGuide, the WHO QuitTobacco app and shouldiscreen.com are not publicly documented in any fetched source.
- **Patient-facing LLM explanation tools:** The WebSearch budget for this session ran out, so other such tools (e.g., for lab results) were not searched further.

## Addendum (main session, 18 Nov 2026)
- Kates et al. 2021 (PMC8175495, fetched): title "A Comparison of Web-Based Cancer Risk Calculators That Inform Shared Decision-making for Lung Cancer Screening", J Gen Intern Med 36(6):1543–1552, doi 10.1007/s11606-021-06754-0. Main finding: for one hypothetical patient, estimates ranged from 2.69% to 29.49% across calculators.
