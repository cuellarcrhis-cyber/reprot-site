# Product signals from blog research

The daily research (briefs/) studies what people search for, what they
struggle with and what the evidence says. Most of it only shapes the post.
When a finding should change the Rep Rot app, it's logged here. The owner
decides what reaches the app's roadmap (it lives in the private app repo);
the routines never edit it.

This repo is public: write research findings with their evidence, never
unreleased plans, prices, metrics or user data.

## Verdicts

Every brief ends with a "Product signal" section and one of these verdicts:

- **none**: nothing for the app. The usual answer; most posts end here.
- **note**: interesting, but it fails a must-pass test below. Log one line
  here only if it adds to an existing signal or is likely to recur.
- **candidate**: passes every must-pass test. Log a full entry.
- **claim gap**: the post wanted to say Rep Rot does something it doesn't,
  or the app says something the evidence contradicts. Always log it; these
  keep marketing honest and often point at the cheapest fixes.

## Must-pass tests for a candidate (all five)

1. **Core loop.** It makes "move to unlock your apps / stop your alarm"
   work better for real users. A new product, a new audience or a
   nice-to-have extra is out.
2. **Evidence.** A primary source verified in the brief (trial,
   meta-analysis, large study, Apple documentation), or the same user pain
   showing up in at least 3 of the top results and the questions people
   ask. One blogger's opinion, or facts known only from search summaries,
   make it a note until checked.
3. **Moves something that matters now:** activation (first set done),
   retention (streaks kept), trust (the block holds, counts are fair),
   safety, or rep-count accuracy.
4. **Small and specific.** It names the screen, setting, default or copy
   to change, and one developer could ship it in about a week, or it's a
   test case or detail for an item already planned.
5. **New.** Not already built, planned or logged. If it sharpens an
   existing item, say which one instead of proposing a new one.

Safety findings (a default that could hurt someone) skip tests 3 and 4.

## Entry format

    ### YYYY-MM-DD · <short title> · candidate | claim gap | note
    - **From:** <post slug> (brief: briefs/<slug>.md)
    - **Finding:** one or two sentences, with the number.
    - **Evidence:** source(s), type and size, and caveats.
    - **For Rep Rot:** the specific change, or the existing item it sharpens.
    - **Tests:** which tests pass (1–5); for a note, the one that failed.

Mark an entry `→ roadmap YYYY-MM-DD` or `→ declined YYYY-MM-DD (<reason>)`
once the owner decides.

---

## Log

### 2026-11-05 · Beginners scale push-ups down; count those variants · candidate
- **From:** how-to-do-your-first-push-up, how-many-push-ups-a-day
- **Finding:** People who can't do a floor push-up start on a wall, counter
  or knees, and every top result tells them to. Hands on a ~61 cm box take
  about 41% of body mass vs about 64% for a floor push-up; on the knees,
  about 49%.
- **Evidence:** Ebben et al. 2011 (force plate, 23 recreationally fit
  people), Suprak et al. 2011; scale-downs are in all top-5 results.
- **For Rep Rot:** sharpens the planned camera-accuracy work. Include
  incline and knee push-ups in the accuracy test set and in what the
  counter is checked against, so a beginner who follows our posts isn't
  locked out by a counter that only knows the floor version.
- **Tests:** 1, 2, 3 (activation, accuracy), 4 (test cases for an existing
  item), 5. → roadmap 2026-11-05 (folded into camera-accuracy feedback)
- 2026-11-06 note (how-long-to-hold-a-plank): same pattern for planks; every top
  result starts beginners on knees or an incline. Add a knee plank to the
  camera test set alongside incline and knee push-ups.

### 2026-11-05 · Set size: about half your max, never to failure · note
- **From:** how-many-push-ups-a-day, grease-the-groove
- **Finding:** Practice sets at roughly half of an honest max, stopped well
  short of failure, build strength about as well as sets to failure, and
  are easy to repeat through the day.
- **Evidence:** Grgic et al. 2022 meta-analysis (15 studies, failure vs
  non-failure: no significant strength difference; mostly young adults);
  Grgic et al. 2018 (frequency); top results agree on 40–80% of max.
- **For Rep Rot:** an optional "test your max" step that suggests the daily
  goal (about half), instead of a fixed number for everyone.
- **Tests:** 1, 2, 4, 5 pass; 3 unproven until there's data on whether goal
  size drives drop-off. → roadmap 2026-11-05 (Later)

### 2026-11-05 · An easy way out makes friction work · note
- **From:** how-to-set-app-limits-on-iphone
- **Finding:** In a field study of an app that adds a pause before social
  apps open, 36% of opens were abandoned and attempts were 37% lower by
  week 6; the option to back out was what mattered most.
- **Evidence:** 2023 PNAS friction study, as summarized in the brief
  (verified from search summaries only).
- **For Rep Rot:** the block screen deliberately has no button, and iOS
  always lets people leave it, so no change. Revisit if the block screen
  is redesigned.
- **Tests:** 5 fails (current behavior already covers it).

### 2026-11-07 · In-bed use is the moment that matters · note
- **From:** your-phone-before-bed (brief: briefs/your-phone-before-bed.md)
- **Finding:** Phone use once in bed, not evening screen use in general, is
  most clearly linked to less sleep (each extra 10 min of interactive in-bed
  use ≈ 9 min less sleep in 11–14-year-olds; in-bed use linked to longer
  sleep latency in 75 adults, use outside bed not).
- **Evidence:** Brosnan et al. 2024 JAMA Pediatrics (79 analysed, cameras +
  actigraphy, observational); Kheirinejad et al. (75 adults, app logs + ring);
  Exelmans & Van den Bulck 2016 (844 adults, survey). Checked via search
  summaries only.
- **For Rep Rot:** limits are daily budgets, so the post couldn't promise a
  bedtime lock and didn't. A time-of-day trigger would fit the core loop.
- **Tests:** 1, 2, 5 pass; 4 fails (a new trigger type, not a week's change)
  and 3 is unproven. Likely to recur with the Downtime and phone-in-bed topics.
