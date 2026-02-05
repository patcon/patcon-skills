# Source Checking Strategies

## Tier 1: API-based (fully automatable)

### HN Search (Stories/Comments)

Use the Algolia API. Extract the query and type from the spreadsheet URL.

```bash
curl -sL 'https://hn.algolia.com/api/v1/search?query=KEYWORD&tags=TYPE&hitsPerPage=0'
```

- `tags` = `story` or `comment` (from source_type)
- Response: `{"nbHits": N}` — use `nbHits` as count
- The spreadsheet URLs contain `date<TIMESTAMP` filters — strip those for total count, or use `numericFilters=created_at_i>TIMESTAMP` to scope to a date range

### GitHub API: Forks

```bash
gh api repos/compdemocracy/polis -q .forks_count
```

### Internet Archive: CDX API

For each Internet Archive row, extract the URL pattern from the spreadsheet URL (the part after `*/`):

```bash
curl -sL 'https://web.archive.org/cdx/search/cdx?url=PATTERN&output=json&limit=0&showNumPages=true'
```

Returns a number — total snapshot pages. For exact count:

```bash
curl -sL 'https://web.archive.org/cdx/search/cdx?url=PATTERN&output=json&fl=timestamp' | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d)-1)"
```

Batch all ~30 Internet Archive rows together for efficiency.

## Tier 2: WebFetch-based (may work, may need fallback)

### YouTube Transcripts (filmot.com)

Use WebFetch on the filmot URL. Look for result count in page content.

### Google Scholar: Citations

Use WebFetch on the scholar.google.com URL. Look for result count. May be blocked by CAPTCHA — flag as manual if it fails.

### GitLab Search

Use WebFetch on the gitlab.com search URL. Parse result count from page.

### Reddit

Try WebFetch on the Reddit URL. Look for post/comment counts. May be rate-limited.

### Google Search

Use WebFetch on Google search URLs. Look for "About X results". Likely blocked — flag as manual if it fails.

## Tier 3: Manual only (requires authentication)

These cannot be automated. Present the URL for the user to open manually.

- **Twitter/X Search** — requires login
- **LinkedIn: Org / Search** — requires login
- **Facebook: Search posts** — requires login
- **Join.tw platform** — requires manual inspection
