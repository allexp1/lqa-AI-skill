---
name: lqa
description: Use when writing, translating, editing or approving copy in Hebrew or any non-English language, or English for a specific country (en-US, en-GB, en-AU, en-NZ, en-CA, en-IE); when asked for LQA, proofreading, a translation review, a language check, or "is this ready to ship"; and before delivering any non-English draft, even unasked. Covers WhatsApp and SMS messages, app and website strings, store listings, emails, kids' learning content and narration scripts.
---

# LQA (linguistic quality assurance)

Two passes, then a verdict. A script catches what can be counted. A careful native-level read catches what matters: meaning, grammar, naturalness, register. Every finding gets an MQM category and a severity, so a typo and a wrong price never weigh the same.

Run it on every non-English draft before delivery, including my own drafts, and report the findings, not just the corrected text.

## 1. Scope (30 seconds, from context; ask only if it changes the verdict)

- **Language and locale:** `he`, `en-US`, `en-GB`... English copy needs an explicit locale.
- **Channel:** whatsapp / sms / app / web / email / store. This sets the length and bidi rules.
- **Audience:** age (kids: see the checklist), formality, and who is addressed (one person, a group, unknown gender).
- **Source text,** if this is a translation.
- **Project glossary:** look for `lqa/glossary.json` or `.lqa/glossary.json` in the project root. If the project has none and the same terms keep recurring, offer to start one (format in `references/glossary-format.md`).

## 2. Mechanical pass

```bash
python3 -I <skill-dir>/scripts/lqa_check.py DRAFT.txt --channel whatsapp [--source SRC.txt] [--lang en-GB] [--glossary G.json]
```

Use `-` to read from stdin. `--help` lists the flags (`--allow-emoji`, `--allow-dashes`, `--max-chars`, `--format json`, `--strict`). Read every finding and confirm or dismiss it. The script gives leads, not verdicts: `neutral` findings (`LG-REPEAT`, bidi in apps) need a look, and only you decide.

## 3. Linguistic pass

Load the language pack first:
- **Hebrew:** `references/he/checklist.md` (the review questions), `references/he/house-rules.md` (the owner's rules, and how conflicts between sources are settled), then `references/he/writing-rules.md` and `references/he/grammar-quick-ref.md` as needed.
- **English locales:** `references/en/locales.md`.

Walk the MQM categories in `references/typology.md` in order: accuracy, terminology, linguistic conventions, style, locale conventions, audience, design. Read the whole text once for sense before you hunt for errors.

**Translations:** back-translate each sentence literally into the source language and compare meaning, numbers, names, negation and modality (must / may / can). Back-translation is a signal, not proof: it hides awkward phrasing, so it never replaces the native read.

## 4. Filter (stops over-flagging, the known failure of AI reviewers)

For every candidate finding, write the fix. If a native reader would not clearly prefer the fix, it is `neutral` (a preference): list it, but it doesn't count. Never record taste as an error.

## 5. Fix, then re-read for sense

Apply the fixes. Re-read every changed sentence in full context: a grammar fix can break meaning (removing a pronoun once left "מותר לו לחרוג" with no object). Re-run the script on the final text.

## 6. Report

Use `references/report-template.md`: the verdict first, then the findings table (what was wrong, why, what was changed), then the final text. Deliver Hebrew chat copy as a file or an artifact, never in a terminal code block (the code block forces LTR direction).

**Verdict:** any critical → **FAIL**; any major → **FIX** (fixed in the final text, or listed as blocking); otherwise → **PASS**. Store listings, paid ads, legal text, prices and narration scripts are high-visibility copy and also get **needs native sign-off**: an AI pass is a revision, not the final authority.

## Common mistakes

| Mistake | Instead |
|---|---|
| Returning only the corrected text | The findings table first, then the text |
| Counting style preferences as errors | Pass each one through the fix test; preferences are `neutral` |
| Checking strings out of context | Read where they appear (button, message, story page); check truncation and gender agreement there |
| Trusting a clean script run | The script can't see meaning; the linguistic pass is the LQA |
| Fixing grammar and breaking sense | Re-read every changed sentence in its full context |
