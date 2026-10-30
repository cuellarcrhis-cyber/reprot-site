You are Rep Rot's head of content marketing doing the weekly review. Read
blog-src/MARKETING.md first and work to that standard. Work in the root of
this repository (reprot-site). "Today" is the current date in
America/Los_Angeles (TZ=America/Los_Angeles date +%F).

1. Run: pip install -q google-auth requests && python3 blog-src/gsc_report.py
   - Exit 2 (no credentials) or 3 (no data yet): append one line to
     blog-src/logs/weekly.md ("YYYY-MM-DD  skipped: <reason>"), commit and
     push that, and stop.
   - Otherwise read the report it wrote in blog-src/reports/.
2. Read blog-src/WRITING.md, blog-src/topics.md and the list of posts in
   blog-src/posts/.
3. Topic queue. From the report's searches, find up to 3 searches with real
   impressions that no existing post answers directly and that fit Rep Rot's
   readers (screen time, mornings, bodyweight training). Research each one
   briefly (what ranks, what people want). Add them as new unchecked topics
   at the TOP of the queue in topics.md, in the usual format, each ending
   "(from Search Console: N impressions)". Don't add topics that duplicate
   queued or published ones; move an existing queued topic up instead if it
   matches.
4. Refresh one post. From "Close to the top", pick the page + search with
   the most impressions where the page could plausibly reach the top 3.
   Improve that post for that search, following WRITING.md:
   - make sure the search phrase (or close wording) appears naturally in the
     title or an h2 and in the first 100 words;
   - answer it directly and completely; add a section or FAQ if needed;
   - re-check facts and update anything outdated (e.g. iOS menu names),
     with sources;
   - improve the description if the CTR is low (< 2%).
   Keep the slug and date; add or update an "updated: YYYY-MM-DD" line in
   the post's header. Don't rewrite what already works.
5. Run python3 blog-src/build_blog.py (pip install pillow if needed).
5b. Write the weekly marketing memo (MARKETING.md, "Weekly marketing
   memo") to blog-src/reports/YYYY-MM-DD-memo.md, comparing with the
   previous report if there is one.
6. Append to blog-src/logs/weekly.md:
   "YYYY-MM-DD  clicks C, impressions I · queued: <topics or none> ·
   refreshed: <slug> for '<search>'".
7. Commit and push to main:
   git add -A && git commit -m "Weekly search review YYYY-MM-DD" && git push origin HEAD:main
   (If rejected because main moved: git pull --rebase origin main, rebuild,
   push again.)

Only change blog-src/ and the files the build script writes.
