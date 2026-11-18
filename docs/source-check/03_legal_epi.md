# 03 – Legal, regulatory and epidemiological background (verified 18 Nov 2026)

Scope: "Lung Health & Quit Coach", a research prototype (PLCOm2012 risk, quit scenarios, optional CXR AI score, LLM explanations with verifier). Not a medical device; fictional cases + public anonymised data + anonymous user study.

Method: every fact below was taken from a page fetched on 18 Nov 2026 (WebFetch). Nothing was filled in from memory. Quotes are short fragments; the rest is paraphrased. Where a source could not be fetched (robots block, allowlist, or search budget used up), the item is listed under "Not confirmed".

Access problems that affected this file:
- legislatie.just.ro, insp.gov.ro and one england.nhs.uk URL blocked automated fetching (robots_disallowed).
- iris.who.int PDF downloads failed (client error).
- The Eurobarometer and Eurostat data browser pages are JavaScript-only, so the fetcher saw no content.
- The web-search budget ran out before searches for UBB ethics, WHO LMM guidance, Law 349/2002 and the Beating Cancer Plan page. These can be repeated in a follow-up run.

---

## A. MDR – Regulation (EU) 2017/745

### Confirmed
- **Art. 2(1), definition of "medical device"**: "any instrument, apparatus, appliance, software, implant, reagent, material or other article" intended by the manufacturer for human beings for one or more specific medical purposes. The first listed purpose is "diagnosis, prevention, monitoring, prediction, prognosis, treatment or alleviation of disease". The device must not achieve its principal intended action by pharmacological, immunological or metabolic means.
  -> So software whose *intended purpose* is **prediction/prognosis of disease** for individuals falls within the definition.
- **Art. 2(27), making available on the market**: any supply of a device, other than an investigational device, "for distribution, consumption or use on the Union market in the course of a commercial activity, whether in return for payment or free of charge".
- **Art. 2(28), placing on the market**: "the first making available of a device, other than an investigational device, on the Union market".
- **Art. 2(29), putting into service**: the stage at which a device, other than an investigational device, "has been made available to the final user as being ready for use on the Union market for the first time for its intended purpose".
  -> MDR obligations attach to placing on the market and putting into service. These require supply in the course of a commercial activity, or availability to final users as ready for use. A university research prototype that is not supplied or made available to end users for a medical purpose does not meet these definitions. (This is an inference from the definitions, not an explicit statement in the text.)
- **Annex VIII, Chapter III (section 6.3), Rule 11** (paraphrased): software providing information used to take decisions for diagnosis or therapy is **Class IIa**. It is **Class III** if such decisions may cause death or irreversible deterioration of health, and **Class IIb** if they may cause serious deterioration or surgical intervention. Software monitoring physiological processes is IIa, or IIb for vital parameters where variations could cause immediate danger. "All other software is classified as class I."
  - URL (consolidated text 19.07.2026): https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A02017R0745-20260719
  - Note: EUR-Lex also lists a newer consolidated version dated 09.11.2026 (CELEX 02017R0745-20261109). It was not fetched; check whether it touches Art. 2 or Annex VIII.

- **MDCG 2019-11 rev.1 (June 2025)**, "Qualification and classification of software – Regulation (EU) 2017/745 and Regulation (EU) 2017/746". The original version was October 2019. The document is MDCG-endorsed and not legally binding. It is the current revision on the Commission's MDCG guidance page.
  - Guidance page: https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en
  - PDF: https://health.ec.europa.eu/document/download/b45335c5-1679-4c71-a91c-fc7a4d37f12b_en?filename=mdcg_2019_11_en.pdf
  - **Qualification decision steps (Section 3.3, Fig. 1)**:
    1. Is it software?
    2. Is it an Annex XVI product, an accessory, or software driving/influencing a device?
    3. Does it act on data beyond storage, archival, communication, simple search or lossless compression?
    4. Is it for the benefit of *individual* patients? Population-level aggregation, generic pathways, literature, epidemiological studies or registers are generally not.
    5. Does it have a medical purpose under Art. 2(1)?
  - Section 3.1: risk of harm is **not** a criterion for qualification.
  - Prediction/prognosis software can qualify. Examples of qualifying MDSW include software calculating prostate-cancer risk, trisomy-21 risk, an app giving 10-year cardiovascular risk from user input (p. 21), and ICU/readmission risk scores (Annex II, Example 2).
  - Wellness/fitness software with only non-medical purposes is not MDSW (Section 3.1).
  - **Intended purpose** is set by the manufacturer's label, IFU, promotional/sales material and clinical evaluation (Section 2). It must describe all medical functionality without ambiguity.
  - **Rule 11 interpretation (Section 4.2.1)**: classification depends on the significance of the information and the healthcare situation. An illustrative IMDRF-style table is in Annex III, Table 1.
- **Practical implication for the thesis** (reasoning from the above, not a legal opinion): an individual lung-cancer *risk prediction* tool with a medical intended purpose would likely qualify as MDSW if placed on the market (cf. the 10-year CVD risk app example), probably at Class IIa or higher under Rule 11a. The prototype's stated intended purpose (research/education, not for clinical decisions) and the fact that it is not placed on the market or put into service are therefore the key framing points. Phrase the disclaimers and UI carefully, because promotional wording can create an intended purpose.

### Not confirmed
- The text of the 09.11.2026 consolidated MDR version (not fetched).
- MDR Art. 5(5) (in-house exemption) wording: not fetched directly. It is mentioned only via MDCG 2025-6; see B.

---

## B. AI Act – Regulation (EU) 2024/1689 (as amended by Regulation (EU) 2026/1744)

### Confirmed
- **Consolidated text 27.07.2026**: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A02024R1689-20260727
- **Art. 6(1)**: an AI system is high-risk where (a) it is intended to be used as a safety component of a product, or is itself a product, covered by Annex I legislation, and (b) that product "is required to undergo a third-party conformity assessment" under the Annex I legislation.
- **Annex I, Section A**: entry 11 is Regulation (EU) 2017/745 (MDR) and entry 12 is Regulation (EU) 2017/746 (IVDR).
- **Art. 2(6)**: the Regulation does not apply to AI systems or models, including their output, "specifically developed and put into service for the sole purpose of scientific research and development."
- **Art. 2(8)**: the Regulation does not apply to "any research, testing or development activity regarding AI systems or AI models prior to their being placed on the market or put into service". Such activities must comply with applicable Union law. "Testing in real world conditions shall not be covered by that exclusion."
- **Art. 3(9)-(11)**: placing on the market is the first making available on the Union market. Making available is supply for distribution or use in the course of a commercial activity. Putting into service is supply for first use directly to the deployer or for own use.
- **Art. 50 (transparency)**:
  - 50(1): providers must design AI systems that interact directly with people so that those people are informed they are interacting with an AI system, unless this is obvious.
  - 50(2): providers of systems generating synthetic audio, image, video or text must mark outputs in a machine-readable, detectable way.
  - 50(5): the information must be given clearly and distinguishably at the latest at the first interaction, and must meet accessibility requirements.
- **Digital Omnibus on AI, current status (adopted)**:
  - Commission proposal **COM(2025) 836 of 19 Nov 2025** (procedure 2025/0359(COD)). It proposed tying the high-risk application date to a Commission decision confirming that standards and support tools are available (+6 months for Annex III, +12 months for Annex I), with long-stop dates of 2 Dec 2027 and 2 Aug 2028.
    URL: https://www.europarl.europa.eu/RegData/docs_autres_institutions/commission_europeenne/com/2025/0836/COM_COM(2025)0836_EN.pdf
  - **Adopted as Regulation (EU) 2026/1744 of 8 July 2026** (Digital Omnibus on AI), amending Regulations 2024/1689, 2018/1139 and 2023/1230. It was published in the OJ L series on 24 July 2026 and **entered into force 27 July 2026** (Art. 4: third day after publication).
    URL: https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ%3AL_202601744 (ELI: https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng)
- **Art. 113 as now consolidated**:
  - The Regulation entered into force on the 20th day after publication and applies generally from **2 August 2026**.
  - (a) Chapters I-II apply from 2 Feb 2025. The new Art. 5(1)(ba),(bb) and 5(1a),(1b) apply from 2 Dec 2026.
  - (b) Chapter III Section 4, Chapters V, VII and XII, and Art. 78 apply from 2 Aug 2025 (except Art. 101).
  - (c) Chapter III Sections 1-3 (high-risk requirements, except Art. 6(5)) apply from **2 December 2027 for Annex III / Art. 6(2) systems** and from **2 August 2028 for Art. 6(1) / Annex I systems (including MDR-regulated AI)**.
  - (d) Arts. 102-110 apply from 27 July 2026.
  - The final consolidated text states these as fixed dates. The proposal's decision-trigger mechanism does not appear in the consolidated Art. 113.
- **Art. 111(4) (new)**: providers of generative systems placed on the market before 2 Aug 2026 must comply with Art. 50(2) by 2 Dec 2026. Art. 50 itself was not amended. For new systems, Art. 50 applies under the general 2 Aug 2026 date.
- **Art. 4 (AI literacy), replaced**: providers and deployers must "take measures to support the development of AI literacy". It does not require guaranteeing any specific level.
- **Art. 2(6) and 2(8) were not changed** by 2026/1744. A new Art. 2(13) allows delegated acts to limit certain requirements for some Art. 6(1) systems.
- **MDCG 2025-6 / AIB 2025-1 (June 2025)**, FAQ on the interplay between MDR/IVDR and the AI Act:
  - An MDAI is high-risk only if it is a medical device (or safety component) **and** requires notified-body conformity assessment.
  - MDR Class IIa/IIb/III software therefore counts as high-risk. Class I (non-sterile, non-measuring) does not, and in-house Art. 5(5) devices do not.
  - The MDR class drives the AI Act status, not the other way round (Q2, Q4, Table 1).
  - A clinical investigation of a high-risk MDAI counts as real-world testing under Art. 60 (Q25).
  - Art. 50 obligations apply independently of the MDR class (Q4, Q14).
  - URL: https://health.ec.europa.eu/document/download/b78a17d7-e3cd-4943-851d-e02a2f22bbb4_en?filename=mdcg_2025-6_en.pdf
- **Implication** (reasoning, not legal advice): the prototype falls under Art. 2(6)/(8), as research that is not placed on the market or put into service. If commercialised as MDSW of Class IIa or higher, it would be high-risk via Art. 6(1)/Annex I, with obligations from 2 Aug 2028. Art. 50(1) disclosure ("you are interacting with an AI") is good practice to mirror in the UI anyway. An anonymous user study with real participants could raise the question of whether it is "testing in real world conditions" (excluded from Art. 2(8)). Frame it as usability testing on fictional cases, with no real-world medical use.

### Not confirmed
- Whether any further act after 2026/1744 changed these dates (none found, but the search budget ran out before a final sweep).

---

## C. GDPR and Romanian Law 190/2018

### Confirmed (GDPR, https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679)
- **Art. 4(1)**: personal data is "any information relating to an identified or identifiable natural person".
- **Art. 4(5)**: pseudonymisation means data can no longer be attributed to a specific data subject without additional information that is kept separately.
- **Art. 4(15)**: data concerning health is "personal data related to the physical or mental health of a natural person".
- **Recital 26**:
  - Pseudonymised data remain personal data.
  - Identifiability is judged by "means reasonably likely to be used" (cost, time, technology).
  - The principles do not apply to anonymous information, and the Regulation does not concern its processing "including for statistical or research purposes".
- **Art. 9(1)**: processing of health data (a special category) is prohibited unless an Art. 9(2) exception applies, e.g. (a) explicit consent for specified purposes, or (j) processing necessary for scientific research based on Union/Member State law with suitable safeguards.
- **Art. 89(1)**:
  - Research processing needs safeguards, meaning technical and organisational measures, in particular for data minimisation.
  - Pseudonymisation may be used.
  - If the purposes can be fulfilled with data that no longer permit identification, they must be fulfilled that way.
- **Art. 89(2)**: Union/Member State law may derogate from Arts. 15, 16, 18 and 21 for research, subject to these safeguards.

### Confirmed (Law 190/2018 – ANSPDCP official English translation, https://www.dataprotection.ro/servlet/ViewDocument?id=1685)
- Title: Law no. 190/2018 on implementing measures to Regulation (EU) 2016/679.
- **Art. 3**: genetic, biometric or health data may be processed for automated decision-making or profiling only with explicit consent, or under explicit legal provisions, with appropriate safeguards. Health data processed for public-health purposes cannot later be used by third entities for other purposes.
- **Art. 8**:
  - For scientific or historical research, GDPR Arts. 15, 16, 18 and 21 do not apply where exercising them would make the research impossible or seriously impair it (para. 1). Para. 2 is the archiving equivalent.
  - Only applies with Art. 89(1) safeguards (para. 3).
  - Only covers the research purpose where processing serves mixed purposes (para. 4).
- The law enters into force 5 days after publication in Monitorul Oficial, Part I (Art. 16).
- The EUR-Lex/legislatie search listing shows the act as "LEGE 190 18/07/2018". The legislatie.just.ro page itself could not be fetched.

### Not confirmed
- Official Romanian text on legislatie.just.ro (https://legislatie.just.ro/Public/DetaliiDocument/203151): blocked by robots. Monitorul Oficial number and date not confirmed.
- Later amendments to Law 190/2018 not verified.

---

## D. Epidemiology

### Confirmed
- **IARC GCO Romania fact sheet**: the file currently served is **GLOBOCAN 2024** (Cancer Today, 2024 estimates, v1.0), *not* 2022.
  URL: https://gco.iarc.who.int/media/globocan/factsheets/populations/642-romania-fact-sheet.pdf
  - Population: 19,015,093. All cancers: 98,829 new cases and 53,326 deaths.
  - **Lung, both sexes**: 12,407 new cases (12.6%, **rank 2**) and **10,486 deaths (19.7%, rank 1)**.
  - Males: lung is incidence rank 1 (9,410 cases, 17.6%) and mortality rank 1.
  - Females: incidence rank 4 (2,997 cases, 6.6%) and mortality rank 3.
  - ASR (World) lung incidence of about 32.9 and mortality of about 26.5 per 100,000 were read from a bar chart. **Treat as approximate.**
- **ECIS EU-27, 2022 estimates** (factsheet published Sept 2023): https://ecis.jrc.ec.europa.eu/sites/default/files/2024-01/jrc_CancerEstimates2022_factsheet.pdf
  - 2.7 million new cancer cases and 1.3 million cancer deaths in the EU-27 in 2022.
  - Lung cancer: 11.6% of new cases (4th most diagnosed) and **19.5% of cancer deaths, the leading cause of cancer death**.
- **EC / OECD "Romania: Country Health Profile 2023"** (State of Health in the EU): https://health.ec.europa.eu/system/files/2023-12/2023_chp_ro_english.pdf
  - Lung cancer is the most frequent cause of cancer death in Romania (p. 4).
  - Lung is the 2nd most common cancer site in men (15%) and the 4th in women (7%) in the 2022 estimates (p. 7).
  - About 1 in 5 adults smoked daily in 2019 (EHIS), on a par with the EU average: men 30.6%, women 7.5% (p. 8).
  - No lung cancer screening programme is mentioned. Only breast, cervical and colorectal screening are reported (p. 12).
- **Eurostat, Tobacco consumption statistics** (EHIS wave 3, 2019): https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Tobacco_consumption_statistics
  - EU daily smokers: 18.4% of people aged 15+.
  - Romania has the **largest gender gap**: men 23.1 percentage points above women. The share of women smoking daily in Romania is below 10%.
  - The article does not give Romania's overall percentage. Next update planned for July 2027.
- **Romanian National Cancer Control Plan (PNCC) 2023** (ms.ro): https://ms.ro/media/documents/Planul_Na%C8%9Bional_de_Combatere_%C8%99i_Control_al_Cancerului_RIQiTXG.pdf
  - Adult cigarette smoking was 18.7% in 2019 (men 30.6%, women 7.6%; Eurostat EHIS 2019, p. 12).
  - GATS 2019: 30.2% current use of any tobacco product (men 39.2%, women 21.5%).
  - Lung cancer mortality rate fell from 52.7 (2011) to 51.1 (2019), a 3% relative decrease vs 9% in the EU (Table 1, Eurostat; unit not stated).
- **WHO global report on trends in prevalence of tobacco use 2000–2024 and projections 2025–2030** (6th ed., 6 Oct 2025): https://www.who.int/publications/i/item/9789240116276
  - News release: https://www.who.int/news/item/06-10-2025-who-tobacco-trends-report-1-in-5-adults-still-addicted-to-tobacco
  - 1.2 billion tobacco users globally in 2024, about 1 in 5 adults.
  - The WHO European Region has the highest prevalence (24.1% of adults), and women in Europe have the highest female prevalence of any region (17.4%).
- **Special Eurobarometer 539** "Attitudes of Europeans towards tobacco and related products":
  - The JRC report *Trends and patterns of use of tobacco and nicotine products in the EU* (JRC143862, 2026) states that SE 539 fieldwork was May–June 2023 and that its report was published in 2024.
  - **24%** of EU respondents aged 15+ currently smoked traditional tobacco products, and about 21% smoked daily (p. 10).
  - Daily smoking across countries ranged from 6% (Sweden) to 35% (Bulgaria).
  - URL: https://publications.jrc.ec.europa.eu/repository/bitstream/JRC143862/JRC143862_01.pdf
- **Older Eurobarometer (SE 458, 2017)** via the EC Knowledge4Policy page: Romania had 28% active smokers vs 26% for the EU-28.
  URL: https://knowledge4policy.ec.europa.eu/health-promotion-knowledge-gateway/tobacco-smoking-smokers-4_en

### Not confirmed
- **GLOBOCAN 2022 Romania figures**: the GCO URL now serves the 2024 edition. If the thesis must cite 2022, re-fetch the 2022 archived fact sheet. Otherwise cite 2024.
- **ECIS 2022 Romania-specific lung numbers**: these are only in the ECIS data explorer (JavaScript, not fetchable).
- **Romania's figure in SE 539 (2024)**: the Eurobarometer pages are JavaScript-only, and the JRC report's country chart values could not be extracted.
- **WHO 2025 report, Romania country estimate**: the IRIS PDF download failed.
- Absolute EU-27 lung cancer case and death counts (the ECIS factsheet gives only percentages).

---

## E. Screening policy

### Confirmed
- **Council Recommendation of 9 December 2022** on strengthening prevention through early detection: a new EU approach on cancer screening, replacing Council Recommendation 2003/878/EC (**2022/C 473/01**), OJ C 473, 13 Dec 2022.
  URL: https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32022H1213(01)
  - **Lung cancer (Annex)**:
    - Member States should "explore the feasibility and effectiveness" of LDCT screening, e.g. via implementation studies.
    - Screening should "start with high risk individuals", beginning with heavy and former heavy smokers.
    - Member States should research how to identify and invite this group, since there is no systematic data on smoking behaviour.
    - The Annex does not explicitly mention integration with smoking cessation.
  - **Point 1**: offer evidence-based screening per the Annex. **Point 2**: stepwise implementation. **Recital 27**: lung screening can be implemented in a stepwise approach (planning, piloting, roll-out).
  - Annex, other cancers:
    - Breast: mammography at 50–69 (45–74 suggested).
    - Cervical: HPV test at 30–65, every 5 years or more.
    - Colorectal: quantitative FIT at 50–74.
    - Prostate: stepwise PSA + MRI piloting.
    - Gastric: H. pylori screen-and-treat in high-incidence areas.
  - **Point 20**: new tests should enter routine care only after RCT evidence.
  - **Point 25**: report within 3 years, then every 4 years.
- **Europe's Beating Cancer Plan** (as cited in recital 39 of the Council Recommendation): Commission Communication of 3 Feb 2021, **COM(2021) 44 final**. Target: ensure 90% of the EU population who qualify for breast, cervical and colorectal screening are offered it by 2025.
- **Romania**:
  - **PNCC 2023** (ms.ro, version 31.05.2023), Section 3, p. 28:
    - Recommends implementing lung cancer screening with annual low-dose CT for smokers and ex-smokers over 50.
    - New lung and prostate programmes should be introduced cautiously, after feasibility testing.
    - Indicator under O.S. 3.2: "Programe pilot pentru depistarea precoce a cancerului pulmonar" (pilot programmes or feasibility reports).
    - The PNCC also lists Europe's Beating Cancer Plan as a basis.
    - URL: https://ms.ro/media/documents/Planul_Na%C8%9Bional_de_Combatere_%C8%99i_Control_al_Cancerului_RIQiTXG.pdf
  - **Ministry of Health press release, 17 Oct 2023**: the bronchopulmonary cancer screening methodology ("cancerul bronhopulmonar") is listed among acts still being finalised. It is not adopted.
    URL: https://www.ms.ro/ro/centrul-de-presa/noi-progrese-%C3%AEn-implementarea-planului-na%C8%9Bional-de-combatere-%C8%99i-control-al-cancerului/
  - **No adopted, operational national lung cancer screening programme in Romania was found** on the pages fetched. The Country Health Profile 2023 reports only breast, cervical and colorectal screening.
- **SOLACE** ("Strengthening the screening of Lung Cancer in Europe"):
  - EU4Health (call EU4H-2022-PJ-01), 1 Apr 2023 – 31 Mar 2026.
  - Budget €12,134,209, of which the EU contributes €9,707,367.
  - Coordinator: EIBIR (Vienna). Romania is among the 15 project countries.
  - EC page: https://health.ec.europa.eu/non-communicable-diseases/cancer/europes-beating-cancer-plan-eu4health-financed-projects/projects/solace_en
  - The Romanian partner is **UMF "Carol Davila" Bucharest** (team coordinator Dr. Rodica Anghel; WP2 Knowledge Hub, WP3 Implementation Network). This comes from the partner's own page, which is outside the listed source set: https://old.umfcd.ro/en/research-and-development/international-projects/solace-strengthening-the-screening-of-lung-cancer-in-europe/
- **4-IN-THE-LUNG-RUN**: H2020, grant 848294, 1 Jan 2020 – 31 Dec 2025, coordinated by Erasmus MC Rotterdam (CORDIS: https://cordis.europa.eu/project/id/848294/results). **A Romanian participant was not confirmed**, because the participant list was not shown.
- **USPSTF (final, 9 March 2021), Grade B**:
  - Annual LDCT for adults **aged 50–80** with a **20 pack-year** history who currently smoke or quit within the past 15 years.
  - Stop once a person has not smoked for 15 years, or if a health problem substantially limits life expectancy or the ability/willingness to have curative lung surgery.
  - URL: https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/lung-cancer-screening
- **NHS England**, "Targeted screening for lung cancer with low radiation dose computed tomography", standard protocol for the Lung Cancer Screening Programme, **version 3, 3 Feb 2025** (PR1646):
  - Eligibility: age 55 to 74 years 364 days, ever-smokers (s. 3.1.1, 3.3.7).
  - Thresholds: **PLCOm2012 ≥1.51% over six years** and/or **LLPv2 five-year risk ≥2.5%** (s. 3.3.4, 3.3.7). Meeting **either** model makes a person LDCT-eligible, subject to the inclusion and exclusion criteria (s. 3.3.6).
  - The scan should be offered within 56 days of risk assessment (s. 3.2.5).
  - URL: https://www.england.nhs.uk/wp-content/uploads/2019/02/2502-B1646-standard-protocol-prepared-for-the-lung-cancer-screening-programme.pdf

### Not confirmed
- Europe's Beating Cancer Plan text itself was not fetched (only as cited in the Council Recommendation and the PNCC). Its lung-specific content (e.g. the SOLACE link and the screening scheme update) was not confirmed from the Plan itself.
- Any PNRR / "Programul Sănătate" funded lung screening pilot in Romania.
- INSP "Profil de țară privind cancerul 2023" (blocked by robots).

---

## F. Romanian tobacco law

### Confirmed
- The PNCC 2023 (ms.ro) states that **Law no. 15/2016** "interzice fumatul în toate locurile publice închise" (bans smoking in all enclosed public places). It also notes that enforcement is only partly respected.

### Not confirmed
- **Law 349/2002** itself: legislatie.just.ro was blocked and the search budget ran out. The fetched PNCC chunks do not mention 349/2002 by number. That Law 15/2016 amends Law 349/2002 is **not confirmed** from an official page here.

---

## G. UBB research ethics (aviz de etică)

### Not confirmed
- The UBB research ethics committee page, its name, the procedure and the forms. The guessed URL was rejected by the fetch allowlist and the search budget ran out. **Action**: ask the supervisor, or find the page on ubbcluj.ro (Research / "Etică și integritate academică") manually or in a follow-up run.

---

## H. WHO guidance on large multi-modal models (2024)

### Not confirmed
- The title, year and recommendations of "Ethics and governance of artificial intelligence for health: Guidance on large multi-modal models". The who.int URL was not on the allowlist and the search budget ran out. **Action**: re-run a search in a follow-up and fetch the WHO publication page before citing.

---

## Consolidated "not confirmed" list
1. MDR consolidated version 09.11.2026 (content not checked); MDR Art. 5(5) wording.
2. Any act after Reg. 2026/1744 further changing AI Act dates (final sweep not done).
3. Law 190/2018 official Romanian text, Monitorul Oficial number/date and later amendments.
4. GLOBOCAN **2022** Romania figures (the GCO now serves 2024); ECIS 2022 Romania-specific lung numbers.
5. Romania's smoking prevalence in SE 539 (2024); the WHO 2025 report's Romania estimate.
6. Text of Europe's Beating Cancer Plan; any PNRR/Programul Sănătate lung pilot; INSP cancer country profile.
7. A Romanian participant in 4-IN-THE-LUNG-RUN.
8. Law 349/2002 (what it regulates, from an official page).
9. UBB ethics committee page and aviz procedure.
10. WHO LMM guidance (2024): title, year, recommendations.
