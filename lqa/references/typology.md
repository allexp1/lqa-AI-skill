# Error typology and scoring

Based on MQM Core (themqm.org), the typology that the industry standards (ISO 5060:2024, the merged TAUS DQF-MQM) and the LLM evaluators (GEMBA-MQM) all build on. The script's `category` field uses these names.

## Categories (walk them in this order)

| Dimension | Subtypes to check | Typical question |
|---|---|---|
| **Accuracy** | mistranslation, omission, addition, untranslated, do-not-translate, over/undertranslation | Does it say exactly what the source says? Same numbers, names, negation, must/may/can? |
| **Terminology** | termbase, inconsistent use, wrong term | Glossary terms used? The same concept named the same way every time? |
| **Linguistic conventions** | grammar, spelling, punctuation, unintelligible, encoding | Agreement, prepositions, את, spelling standard, punctuation rules |
| **Style** | register, unidiomatic (calques), awkward, inconsistent, organization style (house rules) | Does it sound written in this language? One register all the way through? |
| **Locale conventions** | number, currency, date, time, measurement, phone, address formats; local spelling | 12/03 means 12 March here? ₪ placement? -ise or -ize? |
| **Audience appropriateness** | culture-specific reference, offensive; for kids: age fit | Will this reader get it? Could it offend or exclude? |
| **Design and markup** | layout, markup/placeholders, truncation/length, missing text, links | Placeholders intact? Fits the space? Bidi safe? WhatsApp markers paired? |

## Severities (MQM weights 0 / 1 / 5 / 25)

| Severity | Weight | Definition | Examples |
|---|---|---|---|
| **Critical** | 25 | Makes the content unfit for purpose: misleading, harmful, legally exposed, or functionally broken | Wrong price, date or amount; broken placeholder; meaning reversed (a negation lost); missing legal marker (an Israeli ad message without "פרסומת"); offensive; addresses a child inappropriately |
| **Major** | 5 | A native reader notices at once and trusts the text less, or meaning is unclear; or any error in a headline, CTA or button | Wrong gender agreement; wrong term; mistranslated sentence; brand name translated; WhatsApp marker shows as a literal `*`; over the length limit |
| **Minor** | 1 | Noticeable but meaning intact; polish | Ktiv chaser spelling, a missing maqaf, double space, calque in body text, wrong local spelling (colour/color) |
| **Neutral** | 0 | A preference, or a lead that checked out fine. Listed, never counted | Synonym choice; an intentional double (חצי חצי); a Latin brand word in app text that renders correctly |

**Visibility raises severity.** The same error is one step more severe in a headline, button, push notification, store title or price line.

**Fix test.** Write the fix for every finding. If a native reader would not clearly prefer it, the finding is neutral. This stops the documented failure of AI reviewers: too many false positives.

## Score (for longer texts)

- Penalty total `APT = minor×1 + major×5 + critical×25` (neutral = 0).
- Normed per 1,000 words: `NPT = APT / words × 1000`.
- The MQM example tolerance is 10 penalty points per 1,000 words (about 10 minors or 2 majors).
- Report NPT only when the text has 250 words or more. For short copy (a WhatsApp message, a button set), one error decides, so use the verdict alone.

## Verdict

1. Any critical → **FAIL**: do not ship until fixed and re-checked.
2. Otherwise, any major → **FIX**: fixed in the delivered text, or listed as blocking.
3. Otherwise → **PASS**, minors fixed in the delivered text.
4. Add **needs native sign-off** for high-visibility copy: store listings, paid ads, legal text, prices, narration scripts. ISO 17100 requires a second person to revise every translation. Treat this review as that revision, not as the last word.

Report the verdict for the draft as received, and confirm that the delivered text has no open findings ("after fixes: 0 open").
