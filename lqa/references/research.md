# LQA research (October 2026)

What exists beyond agent skills, and what this skill took from each. Sources were read during research on 2026-10-20/21; items marked *(background)* come from general knowledge and were not re-checked then.

## 1. Agent skills ecosystem

About 18 registry searches (LQA, MQM, translation QA, localization QA, transcreation, Hebrew, RTL, proofread and others). No published skill does real LQA, meaning error typology plus severity plus a verdict, for Hebrew or for locale English.

| Skill | Verdict |
|---|---|
| aniruddhaadak80/skills `linguistic-quality-lqa-review-cycle` | 1.7 KB checklist from a 500-skill bot-generated repo; thin |
| **skills-il/localization `hebrew-content-writer`** (MIT, 681 installs) | Best Hebrew writing rules found; **vendored here** as `he/writing-rules.md` |
| skills-il/localization `hebrew-rtl-best-practices` | Strong RTL/bidi engineering guidance (web code, not language) |
| kostja94/marketing-skills `translation` (2.3K installs) | Good process: source lock, glossary, in-context review, outdated state |
| indranilbanerjee `multilingual-score` | Composite publish/review/re-translate score; tied to its own brand system |
| devolutions/unigetui `translation-review` | Good mechanical method (parity, English-equal, wrong script); repo-specific |
| Others (Chuukese, en↔zh, en↔ja↔zh, NGO localise) | Off-target |

## 2. Quality frameworks and standards

- **MQM (Multidimensional Quality Metrics)**, the de facto standard. 7 dimensions: terminology, accuracy, linguistic conventions, style, locale conventions, audience appropriateness, design and markup. 38 subtypes. Severity weights neutral 0 / minor 1 / major 5 / critical 25; one critical commonly fails the text. Scoring: APT (sum of penalties) → per-word → normed per 1,000 words; the example tolerance is 10 points per 1,000 words; a calibrated linear model maps scores to 0–100. → **adopted** as `typology.md`. [themqm.org typology](https://themqm.org/the-mqm-typology/), [scoring models](https://themqm.org/error-types-2/the-mqm-scoring-models/), [MQM scoring and statistical QC (AMTA 2024)](https://aclanthology.org/2024.amta-presentations.6.pdf)
- **ISO 5060:2024**, the first ISO standard for evaluating translation output: an analytic method with error categories and penalty points, giving an error score and a quality rating. It applies to human, post-edited and raw machine translation, and covers evaluator qualifications and sampling. The standard is paywalled. → confirms the approach. [iso.org/standard/80701](https://www.iso.org/standard/80701.html)
- **ISO 17100:2015** *(background)*: translation-service requirements. Every translation is revised by a second qualified person ("four eyes"). → the "needs native sign-off" rule for high-visibility copy.
- **TAUS DQF** *(background)*: merged with MQM as DQF-MQM (2015). **SAE J2450** *(background)*: an older automotive metric (7 categories, serious/minor). **LISA QA Model**: legacy. All superseded by MQM.

## 3. AI reviewers (LLM-as-judge) and their failure modes

- **GEMBA-MQM** (Kocmi & Federmann, WMT 2023): prompts an LLM to mark error spans with an MQM class and severity, without a reference translation; language-agnostic three-shot examples. [arXiv 2310.13988](https://arxiv.org/pdf/2310.13988)
- **Known failure: too many false positives.** MQM-MSC (2025) reports that GEMBA-style methods "still suffer from an excessive number of false positives" and adds a self-correction re-check. MQM-APE (2024) has the model post-edit each flagged error and drops errors whose fix doesn't improve the text. RUBRIC-MQM (ACL 2025) questions how dependable LLM judges are on high-quality text. [MQM-APE](https://arxiv.org/pdf/2409.14335), [MQM-MSC](https://aclanthology.org/2025.ccl-1.67.pdf), [RUBRIC-MQM](https://aclanthology.org/2025.acl-industry.12/)
- **GEMBA V2** (WMT 2025): ten judgments beat one; aggregating repeated judgments reduces variance. [ACL Anthology](https://aclanthology.org/2025.wmt-1.67.pdf)
- → **adopted:** the "fix test" filter (MQM-APE logic) and the neutral severity for preferences. Not adopted: repeated sampling (too expensive for every message; an option for store listings).
- *(background)* Reference-based metrics (BLEU, chrF, COMET, MetricX) need a human reference translation and score whole systems, not single messages. They are not useful for reviewing copy.

## 4. LQA practice (industry)

- LQA means reviewing **in context, inside the product**: in-context validation, functional checks, in-market testing, and automated checks layered together; a string freeze before release. [SimpleLocalize](https://simplelocalize.io/blog/posts/what-is-localization-qa/), [Lara](https://blog.laratranslate.com/localization-quality-assurance/), [Interpro](https://www.interproinc.com/linguistic-quality-assurance-internal-localization/), [Lingohub](https://lingohub.com/blog/what-is-linguistic-quality-assurance-lqa-)
- Mechanical QA tools (**Xbench**, **Verifika**, **QA Distiller**) check consistency, terminology, numbers, punctuation, whitespace, tags and placeholders, with known false-warning problems. → **adopted** as `scripts/lqa_check.py`, a small dependency-free version tuned for Hebrew and chat copy. [ProZ on Xbench](https://proz.com/forum/proofreading_editing_reviewing/352132-what_is_xbench_used_for.html)

## 5. Hebrew authorities

- **Microsoft Hebrew Localization Style Guide** (PDF, 52 pp.). Key rules: everyday words over formal ones (להשתמש, not לעשות שימוש); no word-for-word translation; gender: plural forms, pairs in education, slashes only as a last resort, verbal nouns on buttons; numbers under 10 in words except with units; על ידי + action vs באמצעות + means; punctuation outside quotes; product names in Latin script with no article. → `he/house-rules.md` conflict table and `he/checklist.md`. [download.microsoft.com](https://download.microsoft.com/download/a/2/f/a2ff07cc-afca-4db8-9ed7-fd1b706abf1c/heb-isr-StyleGuide.pdf)
- **Academy of the Hebrew Language punctuation rules** (read via HaMichlol's summary; the Academy site blocks automated reads): maqaf ־ joins words, no spaces, keyboard hyphen accepted; קו מפריד – with spaces (§15); ranges with no spaces (§18); **no em dash in Hebrew**; gershayim before the last letter of an acronym. → the `LG-EM-DASH` check. [HaMichlol: maqaf and dash](https://www.hamichlol.org.il/המכלול:מקף_וקו_מפריד), [he.wikipedia: gershayim](https://he.wikipedia.org/wiki/גרשיים), [Academy punctuation](https://hebrew-academy.org.il/topic/hahlatot/punctuation/)
- **Ministry of Education, nikud for young readers:** reading is assessed on pointed and unpointed text, with explicit teaching of the move to unpointed text around grade ב. No single official partial-nikud policy was found. → the kids' nikud item in the checklist. [MoE nikud guidance (PDF)](https://meyda.education.gov.il/files/Mazkirut_Pedagogit/HebrewPrimary/learning-teaching/books/nikod.pdf), [fluency assessment 2021](https://meyda.education.gov.il/files/Mazkirut_Pedagogit/HebrewPrimary/assessment/fluency-assessment-2021.pdf)

## 6. English locale authorities

- **Canada:** Government of Canada *Writing Tips Plus*: Canadian Oxford Dictionary; -ize; -our and -re; travelled; defence; practice (noun) / practise (verb). [our-languages.canada.ca](https://our-languages.canada.ca/writing-tips-plus/spelling-international-variations), [practice/practise](https://www.noslangues-ourlanguages.gc.ca/en/writing-tips-plus/practice-practise)
- **Australia:** *Australian Government Style Manual*: pick one dictionary (ACOD or Macquarie) and record exceptions in a style sheet; "program" throughout. [stylemanual.gov.au spelling](https://www.stylemanual.gov.au/grammar-punctuation-and-conventions/spelling)
- **New Zealand:** macrons on te reo Māori words per Te Aka / Te Taura Whiri; no English plural -s on Māori words. [DOC style guide](https://doc.govt.nz/about-us/science-publications/writing-style-guide), [NZ Law Foundation style guide](https://www.lawfoundation.org.nz/style-guide/chapter-1.html)
- **School year names:** age-aligned tables (Wikipedia mirrors, PowerSchool chart); mappings vary with cut-off dates, so project curriculum research wins. [Primary school (Wikipedia)](https://en.wikipedia.org/wiki/Primary_school)

## 7. Open gaps

- The Academy's full rulebook and ISO 5060's penalty table weren't read in full (site blocks automated reads / paywall).
- Not yet covered: Arabic (RTL) and other target languages. Add one pack per language under `references/<lang>/` when a project needs it.
