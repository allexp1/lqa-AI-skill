# Hebrew linguistic pass: the questions

Read the whole text once for sense. Then go through these. Each item names the MQM category it scores under. Details and examples live in `writing-rules.md` (vendored skills-il) and `grammar-quick-ref.md`.

## Accuracy (translations)
- Literal back-translation of each sentence matches the source: numbers, names, dates, negation (לא / אל / אין), modality (חייבים / אפשר / כדאי).
- Nothing was dropped or added to "smooth" the text. Possessives may go (המחשב instead of המחשב שלך) when the meaning stays clear; that is style, not omission.

## Grammar (linguistic conventions)
- **Agreement:** each verb and adjective agrees with its noun in gender and number. Watch subjects separated from their verbs, and English loanwords: give each one a gender and keep it (הדשבורד נטען).
- **Numbers and gender:** 1–2 agree (יום אחד, שתי שנים); 3–10 take the "opposite-looking" form (שלושה ימים, שלוש שנים). Dual forms: יומיים, שבועיים, חודשיים, שנתיים, שעתיים.
- **את** before every definite direct object, never before an indefinite one.
- **Smichut:** the article goes only on the last noun (בית הספר); pluralize the first noun (בתי ספר).
- **Preposition government:** verbs keep their own preposition (לחכות ל-, להתחבר ל-, לחבר את). A hitpa'el verb with את is a calque (להתחבר את החשבון ✗).
- **Relative clauses:** a resumptive pronoun is required after a preposition (שדיברתי איתו).
- **על ידי vs באמצעות:** על ידי + an action; באמצעות + a means or tool.
- **Pronoun referents:** every הוא / היא / זה / אותו points at one clear noun.

## Spelling and punctuation
- Ktiv maleh throughout, one spelling per word (תוכנית, שירות, תוכנה).
- Maqaf or hyphen between a prefix and a digit or Latin word (house rule: hyphen in chat).
- Gershayim before the last letter of an acronym (צה״ל, בי״ס); geresh after an abbreviation (עמ׳).
- No comma before ו unless it joins two complete sentences. A period ends every sentence.
- Quotation marks: one style; punctuation that isn't quoted goes outside.
- Dashes: see house rules (none in chat; never an em dash in Hebrew).

## Style
- **Register:** chosen once (dugri / business / formal) and held to the end. Dugri means short and direct, still with תודה.
- **Calques:** anything that reads as translated (זה עושה שכל, על בסיס יומי, לוקח מקום, בסוף היום, מרגיש חופשי). Translate the meaning; drop an idiom that adds nothing.
- **Stiff words:** לעשות שימוש → להשתמש; כמו גם → וגם; כעת → עכשיו; יש אפשרות → אפשר.
- **Generic "you":** אתה צריך ללחוץ → לחצו / יש ללחוץ (house rules decide which).
- **Ask:** would an Israeli native write this sentence? If it is grammatical but no one would say it, it is `style/unidiomatic`.

## Audience
- **Address form** consistent all the way through (plural, neutral, or the known gender of a named person). In education copy, full pairs where they read well (תלמידים ותלמידות); no slash forms (ה/) in kids' content.
- **Kids' content:**
  - Vocabulary and sentence length fit the age. One idea per sentence for early grades.
  - **Nikud:** grades א to early ב read pointed text; the Ministry of Education moves children to unpointed text during grade ב. Pointed text must be pointed *correctly*: wrong nikud is a spelling error. Unpointed text for older grades can still point one ambiguous word.
  - **Narration and TTS:** homographs a voice can misread (ספר / סַפָּר / סִפֵּר, חלב / חֵלֶב) need nikud on that word or a rewrite. Check numbers too: a TTS voice must read the right gender form (שלושה / שלוש).
  - Nothing frightening, shaming or gendered by default (no "the girls cook, the boys build").
- **Advertising law (WhatsApp, SMS, email ads):** "פרסומת" at the start or in the subject, sender details, and a simple way to opt out. Missing = critical. See `writing-rules.md`, Step 5.

## Design
- Placeholders ({name}, %s) untouched, and the sentence around them still agrees for any value. A placeholder name can be any gender: rephrase so no gendered word depends on it.
- Fits the space: Hebrew often runs shorter than English, but buttons and push notifications still truncate.
- Chat: no Latin on Hebrew lines; WhatsApp markers paired; length limit.
- Web and app: Latin runs, numbers with signs, and phone numbers render correctly in RTL (wrap in `<bdi>` or `dir="ltr"`).
