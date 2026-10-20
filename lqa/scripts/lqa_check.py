#!/usr/bin/env python3
"""Mechanical LQA pass: finds what a script can find reliably, so the linguistic
pass can spend its attention on meaning, grammar and naturalness.

Usage:
  python3 lqa_check.py TARGET [--source SRC] [--lang he|en-US|en-GB|en-AU|en-NZ|en-CA|en-IE]
                      [--channel whatsapp|sms|app|web|email|store|tts] [--max-chars N]
                      [--glossary glossary.json] [--allow-emoji] [--format text|json] [--strict]

TARGET and SRC are file paths, or "-" for stdin. Every finding carries an MQM
category and a severity (critical / major / minor / neutral). The script never
edits text; it only reports. --strict exits 1 when anything critical or major is found.
"""
import argparse
import json
import re
import sys
from collections import Counter

HEB = "א-ת"
HEB_LETTER = re.compile(f"[{HEB}]")
LATIN_LETTER = re.compile(r"[A-Za-z]")
PREFIXES = "ובכלמשה"

PLACEHOLDER = re.compile(r"\{\{\s*[\w.]+\s*\}\}|\{[\w.]+\}|%\{\w+\}|%(?:\d+\$)?[sdif@]|</?[A-Za-z][^<>]*>")
URL = re.compile(r"https?://[^\s<>\"'״)]+")
NUMBER = re.compile(r"\d+(?:[.,:/]\d+)*")
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍]")
# Em dash, en dash, or a hyphen with spaces round it standing in for one.
# A spaced hyphen between numbers or brackets is a minus sign, not a dash.
DASHES = re.compile(r"[–—]|(?<![\d)]) -(?= )|(?<=[\d)]) -(?= (?![\d(]))")
TTS_RANGE = re.compile(r"(?<![\w.])\d+-\d+(?![\w.])")
CURLY_DOUBLE = re.compile("[“”„]")
DETACHED_PREFIX = re.compile(f"(?<![\\w־-])([{PREFIXES}]) (?=[0-9])")
GLUED_PREFIX = re.compile(f"(?<![\\w])([{PREFIXES}]{{1,3}})(?=[0-9A-Za-z])")

DEFAULT_MAX = {"whatsapp": 800}

# Older or defective spellings next to the full spelling (ktiv maleh) modern copy uses.
# Some are real words in another sense, so the message asks to verify.
KTIV = [
    ("תכנית", "תוכנית"), ("תכניות", "תוכניות"), ("תכנה", "תוכנה"),
    ("שרות", "שירות"), ("שרותים", "שירותים"), ("פרוט", "פירוט"),
]

# English calques and stiff phrasing (sources: skills-il hebrew-content-writer, Microsoft Hebrew style guide).
CALQUES = [
    (r"עושה\s+(?:שכל|סנס)", "זה הגיוני / זה נשמע הגיוני", "minor"),
    (r"על\s+בסיס\s+יומי", "מדי יום / כל יום", "minor"),
    (r"לוקח(?:ת|ים|ות)?\s+מקום", "מתקיים (if 'takes place')", "minor"),
    (r"לעשות\s+שימוש", "להשתמש", "minor"),
    (r"כמו\s+גם", "וגם", "minor"),
    (r"לבצע\s+גישה", "לגשת", "minor"),
    (r"מרגיש(?:ה|ים|ות)?\s+חופשי", "אל תהססו / אפשר תמיד", "minor"),
    (r"יש\s+לך\s+יום\s+(?:טוב|נפלא|נהדר)", "שיהיה לך יום טוב", "minor"),
    (r"(?<![\w])בכדי(?![\w])", "כדי", "neutral"),
    (r"בסוף\s+היום", "בסופו של דבר (if the idiom, not the evening)", "neutral"),
]

# (form, regex, locales that use this form). A finding is raised when the text's
# locale is not in the form's locale set and the pair has a form that the locale uses.
ALL_EN = {"en-US", "en-CA", "en-GB", "en-IE", "en-AU", "en-NZ"}
COMMONWEALTH = {"en-CA", "en-GB", "en-IE", "en-AU", "en-NZ"}
NON_NA = {"en-GB", "en-IE", "en-AU", "en-NZ"}


def _pair(us, other, us_locales, suffix=r"(?:s|es|ed|ing|ful|ite|ites)?"):
    return [
        (re.compile(rf"\b{us}{suffix}\b", re.I), us_locales),
        (re.compile(rf"\b{other}{suffix}\b", re.I), ALL_EN - us_locales),
    ]


SPELLING = []
for us, other in [("color", "colour"), ("favorite", "favourite"), ("behavior", "behaviour"),
                  ("honor", "honour"), ("neighbor", "neighbour"), ("center", "centre"),
                  ("theater", "theatre"), ("gray", "grey"), ("traveled", "travelled"),
                  ("canceled", "cancelled"), ("catalog", "catalogue"), ("defense", "defence"),
                  ("pajamas", "pyjamas"), ("jewelry", "jewellery")]:
    SPELLING += _pair(us, other, {"en-US"})
SPELLING += _pair("math", "maths", {"en-US", "en-CA"}, suffix="")
SPELLING += _pair("mom", "mum", {"en-US", "en-CA"}, suffix=r"(?:s|my|mies)?")
SPELLING += _pair("analyz", "analys", {"en-US", "en-CA"}, suffix=r"(?:e|es|ed|ing)")
SPELLING += _pair("aluminum", "aluminium", {"en-US", "en-CA"})
# "program" is right everywhere for software, so only "programme" is ever flagged.
SPELLING.append((re.compile(r"\bprogrammes?\b", re.I), {"en-GB", "en-IE", "en-NZ"}))

ISE_IZE = re.compile(r"\b(organi|reali|recogni|apologi|memori|categori|prioriti|personali|customi|"
                     r"summari|minimi|maximi|finali|visuali|speciali|authori|critici)([sz])"
                     r"(e|es|ed|ing|ation|ations|er|ers)\b", re.I)
IZE_LOCALES = {"en-US", "en-CA"}
ISE_LOCALES = {"en-AU"}


def detect_lang(text):
    heb = len(HEB_LETTER.findall(text))
    lat = len(LATIN_LETTER.findall(text))
    return "he" if heb >= lat and heb > 0 else "en"


NIKUD = re.compile("[\u0591-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7]")


def _strip_nikud(line):
    """Remove vowel points and cantillation; return the plain line and a map to original columns."""
    plain, idx = [], []
    for i, ch in enumerate(line):
        if not NIKUD.match(ch):
            plain.append(ch)
            idx.append(i)
    return "".join(plain), idx


def _mask(line):
    """Blank out placeholders and URLs, keeping column positions."""
    for rx in (URL, PLACEHOLDER):
        line = rx.sub(lambda m: " " * len(m.group()), line)
    return line


def _find(code, category, severity, line, col, text, message, suggestion=""):
    return {"code": code, "category": category, "severity": severity, "line": line, "col": col,
            "text": text, "message": message, "suggestion": suggestion}


def _strip_for_compare(text):
    return URL.sub(" ", PLACEHOLDER.sub(" ", text))


def _hebrew_term_regex(term):
    words = term.split()
    parts = [f"[{PREFIXES}]{{0,3}}" + re.escape(w) for w in words]
    return re.compile(r"\s+".join(parts))


def _contains(text, term, lang):
    if HEB_LETTER.search(term):
        return bool(_hebrew_term_regex(term).search(text))
    return bool(re.search(rf"\b{re.escape(term)}\b", text, re.I))


def _line_col(text, index):
    line = text.count("\n", 0, index) + 1
    col = index - (text.rfind("\n", 0, index) + 1) + 1
    return line, col


def check(text, source=None, lang=None, channel="app", max_chars=None, glossary=None, allow_emoji=False):
    lang = lang or detect_lang(text)
    out = []
    lines = text.split("\n")
    is_he = lang == "he"
    chat = channel in ("whatsapp", "sms")
    curly_seen, straight_seen = None, None

    for n, raw in enumerate(lines, 1):
        line, idx = _strip_nikud(_mask(raw))
        pos = lambda i, idx=idx, raw=raw: (idx[i] if i < len(idx) else len(raw)) + 1
        has_heb = bool(HEB_LETTER.search(line))

        if raw != raw.rstrip(" \t"):
            out.append(_find("MK-TRAIL-WS", "linguistic/punctuation", "minor", n, len(raw.rstrip(" \t")) + 1,
                             "", "Trailing whitespace.", "Remove it."))
        m = re.search(r"\S( {2,})\S", line)
        if m:
            out.append(_find("MK-DOUBLE-SPACE", "linguistic/punctuation", "minor", n, pos(m.start(1)),
                             "", "Double space inside a line.", "Use one space."))
        for m in DASHES.finditer(line):
            out.append(_find("MK-DASH", "style/organization", "major", n, pos(m.start() + (m.group() == " -")),
                             m.group().strip(),
                             "No dashes, in any text: TTS voices skip them, pause wrongly or read them as "
                             "'minus', and Hebrew has no em dash.",
                             "Rewrite: a comma, a full stop, a new sentence, or parentheses; for a range write "
                             "'עד' / 'to'."))
        if channel == "tts":
            for m in TTS_RANGE.finditer(line):
                out.append(_find("MK-TTS-RANGE", "design/markup", "major", n, pos(m.start()), m.group(),
                                 "A number range with a hyphen: TTS voices read it as 'minus' or as one number.",
                                 "Write it out: 3 עד 5 / 3 to 5."))
        if not allow_emoji:
            for m in EMOJI.finditer(line):
                if m.group() in ("️", "‍"):
                    continue
                out.append(_find("MK-EMOJI", "style/organization", "minor", n, pos(m.start()), m.group(),
                                 "House style: no emoji.", "Remove it, or pass --allow-emoji if the brief allows."))
        for m in CURLY_DOUBLE.finditer(line):
            curly_seen = curly_seen or (n, pos(m.start()))
        for m in re.finditer('"', line):
            i = m.start()
            gershayim = i > 0 and i + 1 < len(line) and HEB_LETTER.match(line[i - 1]) and HEB_LETTER.match(line[i + 1])
            if not gershayim:
                straight_seen = straight_seen or (n, pos(i))

        if is_he or has_heb:
            for m in GLUED_PREFIX.finditer(line):
                out.append(_find("MK-PREFIX-GLUE", "linguistic/punctuation", "minor", n, pos(m.start()),
                                 re.match(r"\S+", line[m.start():]).group(),
                                 "Hebrew prefix glued to a digit or Latin word.",
                                 f"Join with a maqaf or hyphen: {m.group(1)}־… (WhatsApp house style: {m.group(1)}-…)."))
            for m in DETACHED_PREFIX.finditer(line):
                out.append(_find("MK-PREFIX-DETACHED", "linguistic/punctuation", "minor", n, pos(m.start()),
                                 m.group(1) + " " + re.match(r"\S+", line[m.end():]).group(),
                                 "Hebrew prefix separated from its number by a space.",
                                 f"Join with a maqaf or hyphen: {m.group(1)}־… (WhatsApp house style: {m.group(1)}-…)."))
            if has_heb and LATIN_LETTER.search(line):
                sev = "major" if chat else "neutral"
                word = LATIN_LETTER.search(line)
                out.append(_find("MK-BIDI-MIX", "design/layout", sev, n, pos(word.start()),
                                 re.search(r"[A-Za-z][\w.-]*", line[word.start():]).group(),
                                 "Latin text on a Hebrew line; bidi can reorder the line." +
                                 (" In chat apps this breaks copy/paste." if chat else
                                  " Check it renders in an RTL context (wrap in <bdi> / dir=ltr if needed)."),
                                 "Translate or transliterate, or move the Latin part to its own line." if chat else ""))
            if channel == "whatsapp" and has_heb:
                for m in re.finditer(r"\d+\.\d+", line):
                    out.append(_find("MK-DECIMAL", "design/layout", "minor", n, pos(m.start()), m.group(),
                                     "Decimal point in a Hebrew chat message can shift visually.",
                                     "Prefer a round number if the meaning allows."))
            for wrong, right in KTIV:
                rx = re.compile(f"(?<![{HEB}])([{PREFIXES}]{{0,3}}){wrong}(?![{HEB}])")
                for m in rx.finditer(line):
                    out.append(_find("LG-KTIV", "linguistic/spelling", "minor", n, pos(m.start()), m.group(),
                                     f"Defective spelling (ktiv chaser); modern copy uses '{right}'. Verify it is not a different word.",
                                     m.group(1) + right))
            for pattern, suggestion, sev in CALQUES:
                for m in re.finditer(pattern, line):
                    out.append(_find("LG-CALQUE", "style/unidiomatic", sev, n, pos(m.start()), m.group(),
                                     "Calque or stiff phrasing.", suggestion))

        if channel == "whatsapp":
            for marker in "*_~":
                if line.count(marker) % 2:
                    out.append(_find("MK-WA-MARKER", "design/markup", "major", n, pos(line.index(marker)), marker,
                                     f"Unbalanced WhatsApp '{marker}' marker; it will show as a literal character.",
                                     f"Close the {marker}…{marker} pair on the same line."))
        m = re.search(r"\b(\w+)\s+\1\b", line)
        if m and not m.group(1).isdigit():
            out.append(_find("LG-REPEAT", "linguistic/grammar", "neutral", n, pos(m.start()), m.group(),
                             "Repeated word (intentional doubles such as חצי חצי are fine).", m.group(1)))

    if curly_seen and straight_seen:
        out.append(_find("MK-QUOTE-MIX", "style/inconsistent", "minor", straight_seen[0], straight_seen[1], '"',
                         "Straight and curly quotation marks are mixed.", "Pick one style for the whole text."))

    body = _mask(text)
    for o, c in ("()", "[]"):
        if body.count(o) != body.count(c):
            out.append(_find("LG-UNBALANCED", "linguistic/punctuation", "minor", 0, 0, o + c,
                             f"Unbalanced {o}{c}.", "Close every bracket."))

    limit = max_chars or DEFAULT_MAX.get(channel)
    length = len(text.strip())
    if limit and length > limit:
        out.append(_find("MK-LENGTH", "design/truncation", "major", 0, 0, "",
                         f"{length} characters; limit for this channel is {limit}.", "Cut it."))
    if channel == "sms":
        ucs2 = any(ord(ch) > 127 for ch in text)
        per, single = (67, 70) if ucs2 else (153, 160)
        segments = 1 if length <= single else -(-length // per)
        if segments > 1:
            out.append(_find("MK-LENGTH", "design/truncation", "minor", 0, 0, "",
                             f"{length} characters = {segments} SMS segments ({'UCS-2' if ucs2 else 'GSM'}).",
                             "Shorten to one segment if cost or splitting matters."))

    if lang.startswith("en-"):
        out += _english_locale(text, lang)

    if source is not None:
        out += _compare(source, text, lang)
    if glossary:
        out += _glossary(source, text, glossary, lang)

    order = {"critical": 0, "major": 1, "minor": 2, "neutral": 3}
    out.sort(key=lambda f: (order[f["severity"]], f["line"], f["col"]))
    return out


def _english_locale(text, lang):
    out = []
    for rx, locales in SPELLING:
        if lang in locales:
            continue
        for m in rx.finditer(text):
            line, col = _line_col(text, m.start())
            out.append(_find("LC-SPELL-VARIANT", "locale/spelling", "minor", line, col, m.group(),
                             f"Spelling variant not used in {lang}.", "Use the local spelling (see references/en/locales.md)."))
    hits = list(ISE_IZE.finditer(text))
    kinds = {m.group(2).lower() for m in hits}
    for m in hits:
        k = m.group(2).lower()
        wrong = (lang in IZE_LOCALES and k == "s") or (lang in ISE_LOCALES and k == "z")
        if wrong:
            line, col = _line_col(text, m.start())
            out.append(_find("LC-SPELL-VARIANT", "locale/spelling", "minor", line, col, m.group(),
                             f"{lang} uses -i{'z' if lang in IZE_LOCALES else 's'}e.", ""))
    if lang not in IZE_LOCALES | ISE_LOCALES and kinds == {"s", "z"}:
        line, col = _line_col(text, hits[0].start())
        out.append(_find("LC-ISE-IZE-MIX", "style/inconsistent", "minor", line, col, "",
                         "Both -ise and -ize spellings appear.", "Pick one for the whole text (-ise is the common default)."))
    return out


def _compare(source, target, lang):
    out = []
    sp, tp = Counter(PLACEHOLDER.findall(source)), Counter(PLACEHOLDER.findall(target))
    for ph in sp - tp:
        out.append(_find("AC-PLACEHOLDER", "accuracy/omission", "critical", 0, 0, ph,
                         f"Placeholder {ph} from the source is missing in the target.", "Restore it exactly."))
    for ph in tp - sp:
        out.append(_find("AC-PLACEHOLDER", "accuracy/addition", "major", 0, 0, ph,
                         f"Placeholder {ph} is not in the source.", "Remove it or check the source."))
    su = Counter(u.rstrip(".,;:!?") for u in URL.findall(source))
    tu = Counter(u.rstrip(".,;:!?") for u in URL.findall(target))
    for u in su - tu:
        out.append(_find("AC-URL", "design/link", "major", 0, 0, u,
                         f"URL {u} from the source is missing or changed.", "Keep the link exactly."))
    sn = Counter(NUMBER.findall(_strip_for_compare(source)))
    tn = Counter(NUMBER.findall(_strip_for_compare(target)))
    for num in sn - tn:
        small = num.isdigit() and int(num) <= 10
        sev = "minor" if small else "major"
        out.append(_find("AC-NUMBER", "accuracy/mistranslation", sev, 0, 0, num,
                         f"Number {num} from the source does not appear in the target"
                         + (" (fine if spelled out in words)." if small else ". Critical if it is a price, date or legal figure."),
                         "Check the figure."))
    for num in tn - sn:
        out.append(_find("AC-NUMBER", "accuracy/addition", "minor", 0, 0, num,
                         f"Number {num} is in the target but not in the source.", "Check the figure."))
    return out


def _glossary(source, target, glossary, lang):
    out = []
    src = _strip_for_compare(source) if source else None
    for term in glossary.get("keep", []):
        if src is not None and term in src and term not in target:
            out.append(_find("TM-KEEP", "terminology/do-not-translate", "major", 0, 0, term,
                             f"'{term}' must stay as written but is missing from the target.", term))
    for t in glossary.get("terms", []):
        if src is not None and _contains(src, t["source"], "en") and not _contains(target, t["target"], lang):
            out.append(_find("TM-GLOSSARY", "terminology/termbase", "major", 0, 0, t["source"],
                             f"Source term '{t['source']}' should be rendered as '{t['target']}'.", t["target"]))
        for bad in t.get("forbidden", []):
            if _contains(target, bad, lang):
                out.append(_find("TM-FORBIDDEN", "terminology/termbase", "major", 0, 0, bad,
                                 f"Forbidden rendering '{bad}'.", t["target"]))
    for bad in glossary.get("forbidden", []):
        if _contains(target, bad, lang):
            out.append(_find("TM-FORBIDDEN", "terminology/termbase", "major", 0, 0, bad,
                             f"Forbidden term '{bad}'.", ""))
    return out


def _read(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as f:
        return f.read()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("target")
    p.add_argument("--source")
    p.add_argument("--lang")
    p.add_argument("--channel", default="app", choices=["whatsapp", "sms", "app", "web", "email", "store", "tts"])
    p.add_argument("--max-chars", type=int)
    p.add_argument("--glossary")
    p.add_argument("--allow-emoji", action="store_true")
    p.add_argument("--format", default="text", choices=["text", "json"])
    p.add_argument("--strict", action="store_true")
    a = p.parse_args(argv)

    text = _read(a.target)
    source = _read(a.source) if a.source else None
    glossary = json.loads(_read(a.glossary)) if a.glossary else None
    lang = a.lang or detect_lang(text)
    findings = check(text, source, lang, a.channel, a.max_chars, glossary, a.allow_emoji)
    counts = Counter(f["severity"] for f in findings)
    summary = {"lang": lang, "channel": a.channel, "chars": len(text.strip()), "words": len(text.split()),
               **{s: counts.get(s, 0) for s in ("critical", "major", "minor", "neutral")}}

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if a.format == "json":
        print(json.dumps({"summary": summary, "findings": findings}, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            tail = f"  -> {f['suggestion']}" if f["suggestion"] else ""
            shown = f"  «{f['text']}»" if f["text"] else ""
            pos = f"L{f['line']}:C{f['col']}" if f["line"] else "whole"
            print(f"{pos:<8} {f['severity']:<8} {f['code']:<16} [{f['category']}] {f['message']}{shown}{tail}")
        print(f"{len(findings)} findings  (critical {summary['critical']}, major {summary['major']}, "
              f"minor {summary['minor']}, neutral {summary['neutral']})  lang={lang} channel={a.channel} "
              f"chars={summary['chars']} words={summary['words']}")
    return 1 if a.strict and (counts.get("critical") or counts.get("major")) else 0


if __name__ == "__main__":
    sys.exit(main())
