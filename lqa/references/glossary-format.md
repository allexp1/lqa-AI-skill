# Project glossary

Keep one per project at `lqa/glossary.json` (or `.lqa/glossary.json`) in the project root, and pass it with `--glossary`. One file per target language when a project has several (`lqa/glossary.he.json`, `lqa/glossary.en-GB.json`).

```json
{
  "keep": ["Kixplo", "Grandpa Benny"],
  "terms": [
    {"source": "worksheet", "target": "דף עבודה", "forbidden": ["וורקשיט"], "note": "printable PDF page"},
    {"source": "test mode", "target": "מצב מבחן"}
  ],
  "forbidden": ["משתמש יקר"]
}
```

- `keep`: brand and product names that must appear exactly as in the source.
- `terms`: approved renderings. A Hebrew target matches with prefixes and an article on any word (`דף עבודה` also matches `בדף העבודה`). `forbidden` lists known wrong renderings of that term.
- `forbidden`: phrases the target must never contain, whatever the source says.
- `note` is for people; the script ignores it.

Add a term as soon as a choice is made twice. That is when inconsistency starts.
