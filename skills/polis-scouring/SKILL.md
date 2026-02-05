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

### Step 2: Prioritize which links to check

Score each row:

```
score = 0.4 * fruitfulness + 0.6 * recency

fruitfulness = avg delta between consecutive checks (normalized 0-1 across all rows)
               (only include check pairs where both have a count; use absolute deltas)
recency      = days_since_last_check / max_days (higher = more overdue)
```

Fruitfulness measures how much a source's cumulative count tends to *grow* between checks — not how large the count is. A source that regularly gains new results scores higher than one with a large but static count.

Special cases:
- Never checked → bonus score of 0.8 (establish baseline)
- Zero delta on most recent check (count identical to previous) → penalty of -0.2

Group results:
1. **Automatable, high priority** — will check programmatically
2. **Manual-only, high priority** — recommend user check these
3. **Lower priority** — mention but don't insist

Present the prioritized list to the user and ask which groups to proceed with before checking.

### Step 3: Check automatable links

Use the strategies in `references/source-strategies.md` to check each source type. Work through automatable sources in priority order. Batch similar source types together (e.g. all Internet Archive rows via CDX API).

### Step 4: Present findings

Use this output format:

```markdown
# Polis Scouring Report — [DATE]

## Automated Checks

| Source | Keyword | Previous | Current | Delta | Notes |
|--------|---------|----------|---------|-------|-------|
| HN Stories | polis -polish | 66 | 72 | +6 | 6 new stories since 2025-02-19 |

## Significant New Leads (delta > 0)
- **HN Stories "polis -polish"**: 6 new stories. [Open search](URL) to review.

## Manual Checks Needed (sorted by priority)
1. **Twitter @UsePolis** (last checked 2025-03-22): [Open](URL)
2. **LinkedIn "pol.is"** (last checked 2025-04-17): [Open](URL)

## Already Up-to-Date (checked recently, low delta)
- GitHub: Ruby (last: 2025-05-26, stable at 10)

## Never Checked
- [Any rows with no historical data]
```

### Step 5: Manual checking round

Present manual-check URLs one at a time. For each, ask the user:
- The current count they see
- Whether they want to mark it as reviewed

Record their responses for inclusion in the final summary.

## Resources

### scripts/
- `fetch_spreadsheet.py` — Fetches and parses the Google Spreadsheet CSV export into structured JSON.

### references/
- `source-strategies.md` — Per-source-type strategies for automated checking (API endpoints, parsing approaches, known limitations).
