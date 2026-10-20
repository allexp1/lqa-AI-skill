# LQA report: the shape

The output is always these parts, in this order. Keep it short: the reader wants the verdict and the fixes, not the method.

1. **Verdict line:** `LQA he · whatsapp · FIX → fixed (0 open)`. Add `· needs native sign-off` for high-visibility copy.
2. **Findings table,** most severe first. Neutral items go in a separate short list, or are left out when there are none worth mentioning.

   | # | Severity | Category | Was | Now | Why |
   |---|---|---|---|---|---|
   | 1 | major | grammar/agreement | הקבוצה הגיעו | הקבוצה הגיעה | the verb agrees with הקבוצה (feminine singular) |
   | 2 | minor | punctuation | ל100 | ל-100 | prefix before a digit takes a hyphen |

3. **Sense re-read:** one line confirming every changed sentence was re-read in context, or naming the one that needed a second fix.
4. **Final text,** delivered per channel: Hebrew chat copy as a file or artifact, never a terminal code block.
5. **Score,** only for texts of 250 words or more: `APT 12 · 2,400 words · NPT 5.0 per 1,000 (tolerance 10)`.

When the text is clean, say so in one line (`LQA he · app · PASS, 0 findings`) and give the text.
