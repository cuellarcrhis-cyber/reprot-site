You are writing today's post for the Rep Rot blog. Work in the root of
this repository (reprot-site). Follow every step; quality beats speed.
"Today" is the current date in America/Los_Angeles (run: TZ=America/Los_Angeles date +%F).

1. Read blog-src/WRITING.md (the rules) and blog-src/topics.md (the queue). Read
   2–3 existing posts in blog-src/posts/ to match the voice and avoid repeating
   them.
2. If a post in blog-src/posts/ already has today's date in its header, stop
   and print "Already posted today." Do nothing else.
3. Take the first unchecked topic in topics.md. If it overlaps an existing
   post, skip it (mark it "- [~] … (skipped: overlaps <slug>)") and take
   the next.
4. Size up the competition, then research. Write a short brief to
   blog-src/briefs/<slug>.md before drafting:
   a. Search the main phrase and 1–2 close variants (WebSearch). Open the
      top 5 organic results that are articles (skip ads, forums, videos)
      with WebFetch.
   b. For each, note: what kind of page it is (step-by-step, listicle,
      opinion, product page), its main headings, length, whether it cites
      sources, how current its details are (e.g. old iOS menu names), and
      what it gets wrong or leaves out.
   c. Search intent: in one line, what the searcher actually wants to walk
      away with. Our post must deliver that in its first section.
   d. Must-cover list: subtopics that most top results include. Readers
      (and Google) expect them; leaving one out makes the post look thin.
   e. Questions people ask: related searches and "how do I / why does /
      is it bad to" variants. Answer the best 2–3 inside the post, as h2/h3
      headings or a short FAQ near the end.
   f. Our edge: 2–4 specific things that will make ours the best result,
      e.g. current iOS 27 steps, real studies with honest caveats, a
      beginner scale-down, a printable routine or table, a better example.
      Never copy wording or structure from a competitor.
   Then verify every fact you'll use: studies from PubMed/journals/
   universities, Apple support pages for any iPhone steps (current iOS
   wording), official guidelines. At least 3 solid sources. If a fact
   can't be verified, leave it out.
5. Write blog-src/posts/<slug>.html in the exact format WRITING.md describes,
   dated today. Link 2–3 relevant earlier posts with ../<slug>/ (only slugs
   that exist in blog-src/posts/).
6. Review it against this list and fix anything that fails:
   - Opening is a specific scene, not a definition or a generality.
   - The main search phrase appears in the title, first 100 words and an h2.
   - Every number, study and setting is in the Sources line, and studies
     are described honestly (sample, observational vs trial).
   - Exercise advice includes easier versions and safety notes.
   - Rep Rot claims match what the app does (see WRITING.md). No overclaims.
   - No banned phrases, no emoji, no filler paragraphs, short paragraphs.
   - Description is 140–160 characters.
   - A header illustration plus 2–4 inline visuals (AI scene / app photo /
     app screenshot / stat card), spread out, with real alt text and
     captions. Never images from other sites.
6b. Make the illustrations (WRITING.md, "Images and visual rhythm"): a
   header and one or two inline scenes with blog-src/gen_image.py, then look
   at each one (Read the .jpg). Regenerate any that has text or numbers,
   brand logos, garbled hands/faces, a subject cut off at the edge, or doesn't
   fit the post. Up to 3 tries per image; keep the best. If gen_image.py says there's no API
   key or the API fails twice, skip the illustrations (the build falls back
   to the title cover) and say so in the final message.
7. Run: python3 blog-src/build_blog.py   It must print the new post count with
   no errors. If it says Pillow is missing, run  pip install pillow  first.
   Check the post has its cover in blog/img/covers/ and 2–4 inline visuals
   as WRITING.md describes.
8. In topics.md, check off the topic: "- [x] … (YYYY-MM-DD, <slug>)". If
   fewer than 10 unchecked topics remain, research and append 10 new ones
   people actually search for, in the same format, mixing how-to and point
   of view across screen time, mornings/sleep and bodyweight training.
9. Append one line to blog-src/logs/published.md:
   "YYYY-MM-DD  <slug>  <title>  (<word count> words)".

10. Commit and push to main:
    git add -A && git commit -m "Blog: <title>" && git push origin HEAD:main
    If the push is rejected, git pull --rebase origin main, rebuild, and
    push again.

Only change blog-src/ and the files the build script writes. Don't edit
Website/*.html by hand.
