# lqa — linguistic quality assurance skill

An agent skill for reviewing copy in Hebrew and in country-specific English (en-US, en-GB, en-AU, en-NZ, en-CA, en-IE): WhatsApp and SMS messages, app and web strings, store listings, emails, kids' learning content and narration scripts.

It works in two passes:

1. **Mechanical:** `lqa/scripts/lqa_check.py` (Python 3, no dependencies) checks bidi, prefixes glued to digits, dashes, emoji, quotes, WhatsApp markers, length, ktiv spelling, calques, local English spelling, and placeholders, numbers, URLs and glossary terms against the source.
2. **Linguistic:** an MQM-based review: accuracy, terminology, grammar, style, locale, audience, design. It uses Hebrew and English locale packs, a fix-test filter against over-flagging, and a re-read for sense after every fix.

The result is a verdict (PASS / FIX / FAIL, plus "needs native sign-off" for high-visibility copy), a findings table, and the corrected text.

## Install

```bash
./install.sh          # runs the tests, then copies lqa/ to ~/.claude/skills/lqa
```

## Use the checker on its own

```bash
python3 -I lqa/scripts/lqa_check.py draft.txt --channel whatsapp
python3 -I lqa/scripts/lqa_check.py he.txt --source en.txt --glossary lqa/glossary.json --format json
```

## Develop

`bash test.sh` runs the test suite. `lqa/references/research.md` has the sources behind the rules (MQM, ISO 5060, the Microsoft Hebrew style guide, the Academy of the Hebrew Language, Government of Canada and Australian style guidance, LLM-judge research).

## Credits

The Hebrew writing rules are vendored from [skills-il/localization](https://github.com/skills-il/localization) (MIT); see `NOTICE`.
