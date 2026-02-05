#!/usr/bin/env python3
"""Fetch and parse the Polis scouring tracking spreadsheet into structured JSON.

Each cell in the spreadsheet records the cumulative total result count from that
source at the time of a check. A growing count between checks indicates new
content has appeared — the delta between consecutive checks is what matters for
prioritization, not the absolute count.
"""

import csv
import io
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone

SPREADSHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1OukDM_FQYt_0_TFHdJmr-aror5YcIR2515mT_3_D0JA"
    "/gviz/tq?tqx=out:csv&sheet=search"
)


def parse_cell(raw):
    """Parse a cell value into (count, reviewed).

    Each cell holds a cumulative total result count (not a delta). Counts grow
    over time as new results appear in that source.

    Formats:
      ""          -> (None, False)
      "564"       -> (564, False)       # cumulative total
      "1,919"     -> (1919, False)      # cumulative total with comma separator
      "✅ 59"     -> (59, True)         # reviewed; count is cumulative total
      "320/1338"  -> (1338, False)      # two numbers; take second as total
    """
    val = raw.strip()
    if not val:
        return None, False

    # Checkmark: "✅ 59"
    m = re.match(r"[✅]\s*(\d[\d,]*)", val)
    if m:
        return int(m.group(1).replace(",", "")), True

    # Slash: "320/1338"
    m = re.match(r"(\d[\d,]*)\s*/\s*(\d[\d,]*)", val)
    if m:
        return int(m.group(2).replace(",", "")), False

    # Plain or comma number: "564", "1,919"
    m = re.match(r"^(\d[\d,]*)$", val)
    if m:
        return int(m.group(1).replace(",", "")), False

    return None, False


def fetch_and_parse():
    resp = urllib.request.urlopen(SPREADSHEET_URL)
    text = resp.read().decode("utf-8")
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)

    # Row 0: headers — date columns start at index 5
    headers = rows[0]
    # Row 1: unix timestamps for each date column
    timestamps = rows[1]

    # Build date column info (skip empty trailing columns)
    date_columns = []
    for i in range(5, len(headers)):
        date_str = headers[i].strip()
        ts_str = timestamps[i].strip() if i < len(timestamps) else ""
        if not date_str:
            continue
        ts = int(ts_str) if ts_str else None
        date_columns.append({"index": i, "date": date_str, "timestamp": ts})

    today = datetime.now(timezone.utc)
    results = []

    for row in rows[2:]:
        source_type = row[0].strip() if len(row) > 0 else ""
        keyword = row[1].strip() if len(row) > 1 else ""
        url = row[2].strip() if len(row) > 2 else ""

        # Skip empty rows
        if not source_type and not url:
            continue

        checks = []
        last_checked_date = None
        last_count = None
        previous_count = None
        total_checks = 0

        for dc in date_columns:
            raw = row[dc["index"]].strip() if dc["index"] < len(row) else ""
            count, reviewed = parse_cell(raw)
            if raw:
                total_checks += 1
                previous_count = last_count
                last_count = count
                last_checked_date = dc["date"]
            checks.append({
                "date": dc["date"],
                "raw_value": raw if raw else None,
                "count": count,
                "reviewed": reviewed,
            })

        days_since = None
        if last_checked_date:
            last_dt = datetime.strptime(last_checked_date, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
            days_since = (today - last_dt).days

        results.append({
            "source_type": source_type,
            "keyword": keyword,
            "url": url,
            "last_checked_date": last_checked_date,
            "last_count": last_count,
            "previous_count": previous_count,
            "days_since_last_check": days_since,
            "total_checks": total_checks,
            "has_ever_been_checked": total_checks > 0,
            "checks": checks,
        })

    return results


if __name__ == "__main__":
    data = fetch_and_parse()
    json.dump(data, sys.stdout, indent=2, ensure_ascii=False)
    print()
