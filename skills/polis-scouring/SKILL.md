---
name: polis-scouring
description: >
  Assist with "polis scouring" -- a periodic review of ~90 tracked search links
  across GitHub, Hacker News, YouTube transcripts, Google Scholar, Reddit, Twitter,
  LinkedIn, Internet Archive, and more, all related to the Polis computational
  democracy platform. Trigger when the user says they want to do "polis scouring"
  or asks to check their Polis tracking spreadsheet. Reads a public Google
  Spreadsheet of search URLs, prioritizes which to check based on past fruitfulness
  and recency, programmatically checks those that are automatable, and presents
  findings as potential new leads. Read-only -- does not update the spreadsheet.
---

# Polis Scouring

## Overview

Periodic scan of ~90 tracked search links to find new mentions of Polis (the computational democracy platform) across the web. The tracking data lives in a public Google Spreadsheet with historical check counts.

Each cell in the spreadsheet records the **cumulative total result count** from that source at the time of a check — not the number of new results. A source is "fruitful" when its count grows significantly between checks (i.e. a large delta), indicating new content has appeared.

## Workflow

### Step 1: Fetch and parse the spreadsheet

Run the fetch script to get structured JSON data:

```bash
python3 scripts/fetch_spreadsheet.py
```

This outputs JSON with each row containing: `source_type`, `keyword`, `url`, `last_checked_date`, `last_count`, `previous_count`, `days_since_last_check`, `total_checks`, `has_ever_been_checked`, and per-date `checks` with `count` and `reviewed` fields.

### Step 2: Pick a source type to focus on

Rather than trying to check everything at once, work through **one source type per session**. Each source has its own quirks — how to read the result count, what the results mean, what counts as a real lead vs. noise, etc.

Present the user with the distinct source types from the spreadsheet, along with:
- How many rows of that type exist
- When they were last checked
- Whether a checking strategy exists in `references/source-strategies.md`

Let the user pick which source type to work on. If they don't have a preference, suggest one that is overdue or has never been checked.

### Step 3: Check that source type

For the chosen source type, work through all its rows:

1. Show the user the rows for this source type (keyword, URL, last count, last checked date)
2. Use the strategy from `references/source-strategies.md` if one exists
3. For each row, report what you find: the current count, the delta from the previous check, and any notable new results
4. If automated checking fails (API down, CAPTCHA, rate limit), present the URL for the user to check manually

### Step 4: Calibrate together

This is the most important step. After checking each row, discuss the results with the user:
- **What does the count mean?** Confirm you're reading the right number from the source.
- **What counts as a real lead?** The user may have context about which results are noise vs. genuinely new mentions of Polis.
- **What should be recorded?** The user decides whether the count and findings are ready to note.

The goal is to build up shared understanding of each source type so that future sessions can move faster. Record any source-specific learnings in `references/source-strategies.md`.

### Step 5: Summarize

After working through the chosen source type, present a summary:

```markdown
## [Source Type] — [DATE]

| Keyword | Previous | Current | Delta | Notes |
|---------|----------|---------|-------|-------|
| polis -polish | 66 | 92 | +26 | 26 new stories since last check |

### Notable finds
- [Any interesting new results worth investigating]

### Source-specific notes
- [Anything learned about how this source works]
```

## Resources

### scripts/
- `fetch_spreadsheet.py` — Fetches and parses the Google Spreadsheet CSV export into structured JSON.

### references/
- `source-strategies.md` — Per-source-type strategies for automated checking (API endpoints, parsing approaches, known limitations).
