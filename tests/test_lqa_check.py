"""Tests for lqa/scripts/lqa_check.py. Run with: bash test.sh"""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPT = os.path.join(ROOT, "lqa", "scripts", "lqa_check.py")
FIX = os.path.join(HERE, "fixtures")
sys.path.insert(0, os.path.join(ROOT, "lqa", "scripts"))

import lqa_check  # noqa: E402


def read(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as f:
        return f.read()


def codes(findings):
    return [f["code"] for f in findings]


def serious(findings):
    return [f for f in findings if f["severity"] in ("critical", "major")]


class HebrewWhatsApp(unittest.TestCase):
    def setUp(self):
        self.bad = lqa_check.check(read("he_whatsapp_bad.txt"), channel="whatsapp")
        self.good = lqa_check.check(read("he_whatsapp_good.txt"), channel="whatsapp")

    def test_detects_language(self):
        self.assertEqual(lqa_check.detect_lang(read("he_whatsapp_bad.txt")), "he")

    def test_bad_catches_every_planted_error(self):
        c = codes(self.bad)
        for expected in [
            "MK-WA-MARKER",     # unbalanced *bold
            "MK-TRAIL-WS",      # trailing space on line 1
            "MK-PREFIX-GLUE",   # ל100 and בAPI
            "MK-DASH",          # em dash
            "MK-EMOJI",         # party emoji
            "MK-BIDI-MIX",      # API on a Hebrew line
            "MK-DECIMAL",       # 2.5 in a WhatsApp message
            "LG-KTIV",          # תכנית
            "MK-QUOTE-MIX",     # straight and curly quotes
            "MK-DOUBLE-SPACE",  # double space
            "LG-CALQUE",        # עושה שכל
        ]:
            self.assertIn(expected, c, f"missing {expected}; got {c}")
        self.assertEqual(c.count("MK-PREFIX-GLUE"), 2)

    def test_bidi_mix_is_major_on_whatsapp(self):
        mix = [f for f in self.bad if f["code"] == "MK-BIDI-MIX"]
        self.assertTrue(all(f["severity"] == "major" for f in mix))

    def test_findings_have_positions(self):
        glue = [f for f in self.bad if f["code"] == "MK-PREFIX-GLUE"]
        self.assertEqual([f["line"] for f in glue], [2, 3])

    def test_good_message_is_clean(self):
        self.assertEqual(self.good, [], f"false positives: {self.good}")

    def test_detached_prefix_before_digit(self):
        f = lqa_check.check("השיעור מתחיל ב 17:00 ונגמר ב-18:00", channel="whatsapp")
        hits = [x for x in f if x["code"] == "MK-PREFIX-DETACHED"]
        self.assertEqual(len(hits), 1, f)
        self.assertEqual(hits[0]["text"], "ב 17:00")

    def test_gershayim_is_not_a_quote(self):
        out = lqa_check.check('צה"ל ו“מירכאות”', channel="app")
        self.assertNotIn("MK-QUOTE-MIX", codes(out))

    def test_length_limit(self):
        long_text = "שלום " * 200
        out = lqa_check.check(long_text, channel="whatsapp")
        self.assertIn("MK-LENGTH", codes(out))
        out = lqa_check.check("שלום", channel="whatsapp", max_chars=2)
        self.assertIn("MK-LENGTH", codes(out))

    def test_emoji_allowed_flag(self):
        out = lqa_check.check("שלום 🎉", channel="app", allow_emoji=True)
        self.assertNotIn("MK-EMOJI", codes(out))

    def test_nikud_does_not_split_words(self):
        pointed = "כָּל תְּמוּנָה הִיא אֶחָד. מַנִּיחִים אֶצְבַּע עַל רֹאשׁ הָעַמּוּדָה."
        self.assertEqual(lqa_check.check(pointed, channel="web"), [])

    def test_nikud_word_checks_still_work(self):
        out = lqa_check.check("הַתָּכְנִית אֶת אֶת הַיְּלָדִים", channel="web")
        c = codes(out)
        self.assertIn("LG-REPEAT", c)
        self.assertIn("LG-KTIV", c)

    def test_allow_dashes_keeps_hebrew_em_dash_rule(self):
        out = lqa_check.check("5 או יותר — למעלה", channel="web", allow_dashes=True)
        self.assertEqual([(f["code"], f["category"]) for f in out],
                         [("LG-EM-DASH", "linguistic/punctuation")])
        out = lqa_check.check("5 או יותר – למעלה", channel="web", allow_dashes=True)
        self.assertEqual(out, [])

    def test_bidi_mix_is_neutral_in_app(self):
        out = lqa_check.check("ברוכים הבאים ל-Kixplo", channel="app")
        mix = [f for f in out if f["code"] == "MK-BIDI-MIX"]
        self.assertEqual([f["severity"] for f in mix], ["neutral"])


class SourceComparison(unittest.TestCase):
    def setUp(self):
        self.glossary = json.loads(read("glossary.json"))
        self.bad = lqa_check.check(read("tgt_he_bad.txt"), source=read("src_en.txt"),
                                   glossary=self.glossary, channel="app")
        self.good = lqa_check.check(read("tgt_he_good.txt"), source=read("src_en.txt"),
                                    glossary=self.glossary, channel="app")

    def test_missing_placeholder_is_critical(self):
        ph = [f for f in self.bad if f["code"] == "AC-PLACEHOLDER"]
        self.assertTrue(ph)
        self.assertEqual(ph[0]["severity"], "critical")
        self.assertIn("{name}", ph[0]["message"])

    def test_number_mismatch(self):
        nums = [f for f in self.bad if f["code"] == "AC-NUMBER"]
        self.assertTrue(any("9.99" in f["message"] for f in nums), nums)

    def test_missing_url(self):
        self.assertIn("AC-URL", codes(self.bad))

    def test_brand_translated(self):
        keep = [f for f in self.bad if f["code"] == "TM-KEEP"]
        self.assertTrue(keep and "Kixplo" in keep[0]["message"])

    def test_good_target_has_no_serious_findings(self):
        self.assertEqual(serious(self.good), [], self.good)

    def test_glossary_required_and_forbidden(self):
        g = self.glossary
        out = lqa_check.check("הורידו את הוורקשיט", source="Download the worksheet", glossary=g)
        c = codes(out)
        self.assertIn("TM-GLOSSARY", c)
        self.assertIn("TM-FORBIDDEN", c)
        ok = lqa_check.check("הורידו את דף העבודה", source="Download the worksheet", glossary=g)
        self.assertNotIn("TM-GLOSSARY", codes(ok))

    def test_glossary_term_with_hebrew_prefix_counts(self):
        out = lqa_check.check("בתוכנית החדשה", source="In the new plan", glossary=self.glossary)
        self.assertNotIn("TM-GLOSSARY", codes(out))

    def test_small_number_may_be_spelled_out(self):
        out = lqa_check.check("שלושה ימים", source="3 days")
        nums = [f for f in out if f["code"] == "AC-NUMBER"]
        self.assertEqual([f["severity"] for f in nums], ["minor"])


class EnglishLocales(unittest.TestCase):
    def variants(self, name, lang):
        out = lqa_check.check(read(name), lang=lang)
        return sorted(f["text"].lower() for f in out if f["code"] == "LC-SPELL-VARIANT")

    def test_gb_flags_us_spellings(self):
        self.assertEqual(self.variants("en_gb_mixed.txt", "en-GB"), ["center", "color", "favorite"])

    def test_us_flags_gb_spellings(self):
        self.assertEqual(self.variants("en_us_mixed.txt", "en-US"),
                         ["centre", "colour", "favourite", "organise"])

    def test_us_clean(self):
        self.assertEqual(lqa_check.check(read("en_us_good.txt"), lang="en-US"), [])

    def test_canada_mix(self):
        out = lqa_check.check("My favourite colour is grey. We organize math clubs.", lang="en-CA")
        self.assertEqual([f for f in out if f["code"] == "LC-SPELL-VARIANT"], [])
        out = lqa_check.check("We organise clubs.", lang="en-CA")
        self.assertIn("LC-SPELL-VARIANT", codes(out))

    def test_australia_prefers_ise_and_program(self):
        out = lqa_check.check("We organize a programme.", lang="en-AU")
        self.assertEqual(sorted(f["text"].lower() for f in out if f["code"] == "LC-SPELL-VARIANT"),
                         ["organize", "programme"])

    def test_uk_accepts_ize_but_not_mixing(self):
        self.assertEqual(lqa_check.check("We organize and recognize.", lang="en-GB"), [])
        out = lqa_check.check("We organize and recognise.", lang="en-GB")
        self.assertIn("LC-ISE-IZE-MIX", codes(out))


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-I", SCRIPT, *args],
                              capture_output=True, text=True, encoding="utf-8")

    def test_json_output_and_strict_exit(self):
        p = self.run_cli(os.path.join(FIX, "tgt_he_bad.txt"), "--source", os.path.join(FIX, "src_en.txt"),
                         "--glossary", os.path.join(FIX, "glossary.json"), "--format", "json", "--strict")
        self.assertEqual(p.returncode, 1, p.stderr)
        data = json.loads(p.stdout)
        self.assertGreaterEqual(data["summary"]["critical"], 1)
        self.assertEqual(data["summary"]["lang"], "he")

    def test_text_output_clean_exit(self):
        p = self.run_cli(os.path.join(FIX, "he_whatsapp_good.txt"), "--channel", "whatsapp", "--strict")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("0 findings", p.stdout)

    def test_stdin(self):
        p = subprocess.run([sys.executable, "-I", SCRIPT, "-", "--channel", "whatsapp"],
                           input="שלום 🎉\n", capture_output=True, text=True, encoding="utf-8")
        self.assertIn("MK-EMOJI", p.stdout)


if __name__ == "__main__":
    unittest.main()
