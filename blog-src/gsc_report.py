#!/usr/bin/env python3
"""Pulls the last 28 days of Google Search Console data for reprotapp.com and
writes a report the weekly routine reads.

    pip install google-auth requests
    python3 blog-src/gsc_report.py            # writes blog-src/reports/YYYY-MM-DD.md

Credentials: a Google Cloud service account with read access to the
Search Console property (added under Settings → Users and permissions).
Its JSON key goes in the environment variable GSC_SERVICE_ACCOUNT_JSON
(the whole JSON text), or in ~/.config/reprot/gsc_service_account.json.
GSC_SITE overrides the property (default: sc-domain:reprotapp.com).
Exit code 2 = no credentials, 3 = no data yet; both print why.
"""

import datetime
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
SITE = os.environ.get("GSC_SITE", "sc-domain:reprotapp.com")
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"


def credentials():
    raw = os.environ.get("GSC_SERVICE_ACCOUNT_JSON")
    path = Path.home() / ".config" / "reprot" / "gsc_service_account.json"
    if not raw and path.exists():
        raw = path.read_text()
    if not raw:
        print("No Search Console credentials (GSC_SERVICE_ACCOUNT_JSON). Skipping.")
        sys.exit(2)
    from google.oauth2 import service_account
    return service_account.Credentials.from_service_account_info(json.loads(raw), scopes=[SCOPE])


def query(session, body):
    from urllib.parse import quote
    url = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{quote(SITE, safe='')}/searchAnalytics/query"
    res = session.post(url, json=body, timeout=60)
    if res.status_code != 200:
        print(f"Search Console error {res.status_code}: {res.text[:400]}")
        sys.exit(1)
    return res.json().get("rows", [])


def table(rows, keys):
    lines = ["| " + " | ".join(keys) + " | clicks | impressions | CTR | position |",
             "|" + "---|" * (len(keys) + 4)]
    for r in rows:
        lines.append("| " + " | ".join(r["keys"]) + f" | {r['clicks']:.0f} | {r['impressions']:.0f} | "
                     f"{r['ctr'] * 100:.1f}% | {r['position']:.1f} |")
    return "\n".join(lines)


def main():
    from google.auth.transport.requests import AuthorizedSession
    session = AuthorizedSession(credentials())
    end = datetime.date.today() - datetime.timedelta(days=3)    # GSC data lags ~2-3 days
    start = end - datetime.timedelta(days=27)
    span = {"startDate": start.isoformat(), "endDate": end.isoformat()}

    pages = query(session, {**span, "dimensions": ["page"], "rowLimit": 100})
    queries = query(session, {**span, "dimensions": ["query"], "rowLimit": 200})
    pairs = query(session, {**span, "dimensions": ["page", "query"], "rowLimit": 500})
    if not pages and not queries:
        print(f"No Search Console data yet for {start}..{end}.")
        sys.exit(3)

    near = [r for r in pairs if 5 <= r["position"] <= 20 and r["impressions"] >= 5]
    near.sort(key=lambda r: -r["impressions"])
    total_clicks = sum(r["clicks"] for r in pages)
    total_impr = sum(r["impressions"] for r in pages)

    REPORTS.mkdir(exist_ok=True)
    out = REPORTS / f"{datetime.date.today().isoformat()}.md"
    out.write_text(f"""# Search Console: {start} to {end}

Property {SITE}. {total_clicks:.0f} clicks, {total_impr:.0f} impressions.

## Pages
{table(sorted(pages, key=lambda r: -r['impressions']), ['page'])}

## Searches (top 200 by impressions)
{table(sorted(queries, key=lambda r: -r['impressions']), ['query'])}

## Close to the top: page + search at position 5-20 (refresh candidates)
{table(near[:40], ['page', 'query'])}
""", encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT.parent)}: {len(pages)} pages, {len(queries)} searches, {len(near)} near-top pairs.")


if __name__ == "__main__":
    main()
