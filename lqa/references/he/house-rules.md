# Hebrew house rules (the owner's), and how source conflicts are settled

These override everything else in this folder. They come from real corrections: each rule exists because a draft failed in practice.

## Owner rules

1. **LQA every Hebrew draft before delivery, unasked,** and report the findings, not just the fixed text.
2. **No Latin on a Hebrew line in chat copy** (WhatsApp, SMS). Bidi flips the line and copy/paste breaks. Translate or transliterate English terms; anything that must stay Latin (a URL, a product label) goes on its own line, with blank lines around it.
3. **Deliver chat copy as a file or an artifact with a copy button,** never as a terminal code block (it forces LTR).
4. **No em or en dashes. No emoji.** Use commas, full stops, or a new sentence.
5. **Hyphen after a prefix before a number or a Latin word in chat copy:** `ל-100`, `ב-2026`. The Hebrew maqaf `־` is correct too (the Academy prefers it), but a plain hyphen survives every keyboard and app. Never glue (`ל100`).
6. **WhatsApp `*bold*` markers paired on the same line.**
7. **No decimals in chat messages** when a round number will do: the decimal point can shift visually.
8. **Length:** the owner cuts hard. Aim well under 800 characters for WhatsApp. Facts over hooks; drop any idea that needs a paragraph to explain.
9. **No trailing whitespace.** Straight and curly quotes never mixed.
10. **Re-read for sense after every fix.** A grammar fix once removed a dangling pronoun and left "מותר לו לחרוג" with no object. The sentence became unparseable.
11. **Resumptive pronouns in relative clauses:** required after a preposition (האיש שדיברתי איתו, not האיש שדיברתי); optional for a direct object (הספר שקניתי and הספר שקניתי אותו are both correct). When a fix removes one, check that the clause still reads complete.

## Where the sources disagree, and what we do

| Topic | Microsoft Hebrew style guide | skills-il writing rules | Academy of the Hebrew Language | **House decision** |
|---|---|---|---|---|
| Numbers 1–9 in running text | Spell out in words; digits with units | Prefer digits in body copy | (no binding rule found) | Chat, UI, math content: digits. Stories and narration: words. One choice per text, never mixed |
| Instructions to the reader | Informal plural imperative (לחצו, בחרו); infinitive not for instructions | Impersonal infinitive (יש ללחוץ) | — | Follow the project's existing address form. Default: plural imperative for instructions, יש/אפשר + infinitive for general statements |
| Button labels | Verbal noun (שמירה, הדפסה) | Imperative, ultra-short | — | Verbal noun |
| Em dash — | Allowed for an isolated element | Not covered | Doesn't exist in Hebrew; use the en dash – with spaces; ranges with no spaces (1–12) | Chat copy: no dashes at all (rule 4). Other content: en dash with spaces, never an em dash |
| Maqaf | Hyphen joins words, no spaces | Maqaf ־ between a prefix and a number/Latin word | Hebrew ־ preferred, keyboard hyphen accepted | Chat: hyphen (rule 5). Web and app: either, one per text |
| Gender | Plural forms; in education "תלמידים ותלמידות"; slash forms (ה/) only as a last resort | Ask; neutral rewording for UX | (no binding rule) | Plural or neutral wording; full pairs in education copy where they read well; no slashes in kids' content |
| Formal words | Avoid לעשות שימוש, כמו גם, כעת, ניתן (use להשתמש, וגם, עכשיו, אפשר) | Dugri register; avoid padding | — | Agree: everyday words |
| Quotation marks | Straight quotes common; punctuation outside the quote | Geresh/gershayim not to be confused with quotes | ״ for acronyms (צה״ל), ׳ for abbreviations (עמ׳) | Either style, consistent; gershayim placed before the last letter of an acronym |
| Emoji | Not covered | "Emoji-compatible" for social posts | — | None, unless the brief allows (`--allow-emoji`) |

## Product names and articles

- Brand and product names stay in Latin script and take no Hebrew article (Microsoft): "ב-Kixplo", not "בקיקספלו" or "הקיקספלו". In chat copy, rule 2 still applies: rephrase so the name sits on its own line, or use the established Hebrew transliteration if the brand has one.
- A company name takes feminine verbs (Kixplo מציעה) and an app name takes masculine verbs (Word שומר), per Microsoft. The noun itself decides when it is used: האפליקציה שומרת.
