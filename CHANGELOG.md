# Changelog

## 1.0.0 (2026-10-21)

First release.

- MQM-based review (7 categories, neutral/minor/major/critical, verdict PASS / FIX / FAIL) for Hebrew and en-US, en-GB, en-AU, en-NZ, en-CA, en-IE.
- `lqa/scripts/lqa_check.py`, a mechanical checker with no dependencies. It covers bidi, prefixes glued to or split from digits, dashes (banned everywhere, a major error), number ranges in TTS scripts, emoji, quotes, WhatsApp markers, SMS and WhatsApp length, ktiv spelling, calques, local English spelling, nikud-safe word checks, and source checks for placeholders, numbers, URLs and glossary terms.
- Hebrew pack with house rules, a checklist, and the vendored skills-il hebrew-content-writer rules (MIT).
- `references/research.md`, the sources behind the rules.
