# Rep Rot blog: how we write

One post a day on reprotapp.com/blog. The goal is search traffic from people
who have the problem Rep Rot solves, so every post has to be the best answer
on the page for its search. Thin, generic, padded posts hurt the whole site:
if a post wouldn't be worth reading without the Rep Rot plug, don't publish it.

## Who we write for

People who scroll more than they want to, can't get out of bed, or keep
meaning to "start working out." Mostly 18–35, iPhone users, not gym people.
They want something they can do today, not a lecture.

## Voice (modeled on liinks.co/blog)

- Second person, direct, a little contrarian. Open on a scene the reader
  recognizes, then name the real problem in one line.
  > You set a 30-minute limit on TikTok. You hit it at 9:40. You tapped
  > "Ignore Limit" at 9:40 and four seconds.
- Short paragraphs: one to three sentences. Short sentences. Plain words.
- Confident, warm, never preachy or shame-y. No "in today's fast-paced world",
  no "let's dive in", no "game-changer", no "unlock your potential", no emoji.
- Specific beats general: real settings paths, real numbers, real rep
  schemes, real examples ("the 11 p.m. Reels hole", "the snooze button at
  6:10").
- Two post shapes, alternate them:
  1. **How-to** ("How to …"): a precise, step-by-step answer to a search.
     Exact iPhone settings paths, what each option does, what goes wrong.
  2. **Point of view** (a claim as the title, e.g. "Willpower Isn't the
     Problem. Your Phone Is Designed That Way."): an argument with a
     practical takeaway.

## Structure

- Title: under ~65 characters, contains the main search phrase naturally.
- Description (meta): 140–160 characters, says what the reader gets.
- 1,000–2,000 words. Long enough to fully answer the search, no padding.
- Opening: 3–6 short paragraphs, no heading.
- 4–7 `<h2>` sections with plain, specific headings (sentence case). `<h3>`
  only if needed. Use `<hr>` between big shifts.
- At least one list, table or numbered routine the reader can use.
- A `<h2>TL;DR</h2>` with 4–6 bullets near the end.
- Close with a short section that ties the advice to Rep Rot, naturally and
  honestly (what the app actually does: app limits that lock until you do a
  set, an alarm that stops only after reps, camera rep counting on the phone,
  push-ups / sit-ups / squats / pull-ups / plank, free plan + 7-day Pro
  trial). One mention mid-post is fine if it genuinely fits. The page adds a
  "Get early access" card after the post automatically (an email to
  help@reprotapp.com while the app is in testing); don't add another button.
  Until launch, a closing line may invite readers to email
  help@reprotapp.com for early access. Never link to the App Store yet.
- Link 2–3 earlier posts where they genuinely help: `<a href="../slug/">`.
- End with `<p class="sources">Sources: …</p>` listing every study or
  official page cited, as links.

## Accuracy (non-negotiable)

- Research before writing (WebSearch / WebFetch). Every number, study and
  setting must be verified from a primary or reputable source and linked in
  Sources. If you can't verify it, leave it out.
- Describe studies honestly: sample size, observational vs. trial, "linked
  to" not "causes". No invented quotes, stats, users or testimonials.
- iPhone instructions must match current iOS. Check Apple's support pages.
- Fitness: safe, conservative advice for beginners; scale-downs for every
  exercise; no medical claims; suggest a doctor for pain, injury, pregnancy
  or heart conditions where relevant.
- Don't overclaim Rep Rot. It can't see which apps you block or your usage
  (Screen Time privacy), it doesn't record video, and Screen Time limits can
  be bypassed by someone determined. Say so when relevant; honesty sells.
- Never name or disparage competitor apps by name.

## SEO checklist

- One clear search intent per post; don't target a phrase an existing post
  already covers (check `topics.md` and `posts/`).
- Main phrase in the title, the first 100 words and one `<h2>`; variants
  elsewhere, never stuffed.
- Answer the question early (first section), then go deeper.
- Tags: 1–3 from: Screen Time, Habits, Focus, Sleep & Mornings,
  Bodyweight Training, Push-Ups, Squats, Plank, Pull-Ups, Sit-Ups,
  Beginners, iPhone Tips, Motivation.

## File format

`blog-src/posts/<slug>.html`, slug = lowercase-hyphenated title keywords (it
becomes the URL /blog/<slug>/). Body fragment only, starting with:

```
<!--
title: How to Stop Doomscrolling on iPhone (Without Deleting Your Apps)
description: 140–160 characters.
date: YYYY-MM-DD
tags: Screen Time, iPhone Tips
-->
```

Allowed markup: p, h2, h3, ul, ol, li, strong, em, a, blockquote, hr,
table/thead/tbody/tr/th/td, p class="sources". No inline styles, no images,
no scripts.

Then run `python3 blog-src/build_blog.py` and check it prints the new count.
