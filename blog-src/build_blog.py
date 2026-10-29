#!/usr/bin/env python3
"""Builds the Rep Rot blog from blog-src/posts/*.html into the site.

Each source post is an HTML body fragment that starts with a metadata
comment:

    <!--
    title: How to Stop Doomscrolling on iPhone
    description: One or two sentences for search results and the card.
    date: 2026-10-29
    tags: Screen Time, Habits
    -->
    <p>First paragraph...</p>

Writes, from the repo root (the site GitHub Pages serves). blog-src/ is
served too, so robots.txt keeps crawlers out of it:
    blog/<slug>/index.html   one page per post (slug = file name)
    blog/index.html          the list of posts, newest first
    blog/feed.xml            RSS
    sitemap.xml, robots.txt

Posts dated in the future are skipped, so a post can be written ahead.
Run from anywhere: python3 blog-src/build_blog.py
"""

import datetime
import html
import json
import math
import re
from pathlib import Path

SITE = "https://reprotapp.com"
# Before launch the card asks for an early-access email; after launch,
# point it at the App Store (https://apps.apple.com/app/id6824360561).
EARLY_ACCESS = "mailto:help@reprotapp.com?subject=Rep%20Rot%20early%20access&body=Hi!%20I%27d%20like%20early%20access%20to%20Rep%20Rot.%20My%20iPhone%20model%3A%20"
ROOT = Path(__file__).resolve().parent.parent   # the repo root is the site (GitHub Pages)
POSTS = Path(__file__).resolve().parent / "posts"
BLOG = ROOT / "blog"
STATIC_PAGES = ["", "support/", "privacy/"]


def parse(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\s*<!--(.*?)-->\s*(.*)", text, re.S)
    if not match:
        raise SystemExit(f"{path.name}: missing the <!-- metadata --> header")
    meta = {}
    for line in match.group(1).strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip().lower()] = value.strip()
    for key in ("title", "description", "date", "tags"):
        if not meta.get(key):
            raise SystemExit(f"{path.name}: missing '{key}'")
    body = match.group(2).strip()
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    return {
        "slug": path.stem,
        "title": meta["title"],
        "description": meta["description"],
        "date": datetime.date.fromisoformat(meta["date"]),
        "tags": [t.strip() for t in meta["tags"].split(",") if t.strip()],
        "body": body,
        "minutes": max(1, math.ceil(words / 230)),
    }


def esc(text):
    return html.escape(text, quote=True)


def nice_date(date):
    return date.strftime("%B %-d, %Y")


def tags_html(post):
    return "".join(f'<span class="tag">{esc(t)}</span>' for t in post["tags"])


def meta_line(post):
    return f'<time datetime="{post["date"].isoformat()}">{nice_date(post["date"])}</time> · {post["minutes"]} min read'


def card(post, prefix):
    return f"""  <a class="post-card" href="{prefix}{post['slug']}/">
    <div class="tags">{tags_html(post)}</div>
    <h2>{esc(post['title'])}</h2>
    <p>{esc(post['description'])}</p>
    <div class="post-meta">{meta_line(post)}</div>
  </a>"""


def page(title, description, url, up, body, extra_head=""):
    """up = path back to the site root, e.g. "../../"."""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/logo.png">
<meta property="og:site_name" content="Rep Rot">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="application/rss+xml" title="Rep Rot Blog" href="{SITE}/blog/feed.xml">
<link rel="icon" href="{up}logo.png">
<link rel="stylesheet" href="{up}style.css">
{extra_head}</head>
<body>
<main>
  <header><a href="{up}"><img src="{up}logo.png" alt=""></a><a class="brand" href="{up}">Rep Rot</a></header>
{body}
  <nav><a href="{up}">Home</a><a href="{up}blog/">Blog</a><a href="{up}support/">Support</a><a href="{up}privacy/">Privacy</a></nav>
</main>
</body>
</html>
"""


def related(post, posts):
    """Three other posts: most shared tags first, then newest."""
    others = [p for p in posts if p["slug"] != post["slug"]]
    others.sort(key=lambda p: (-len(set(p["tags"]) & set(post["tags"])), -p["date"].toordinal()))
    return others[:3]


def post_page(post, posts):
    url = f"{SITE}/blog/{post['slug']}/"
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["description"],
        "datePublished": post["date"].isoformat(),
        "dateModified": post["date"].isoformat(),
        "mainEntityOfPage": url,
        "keywords": ", ".join(post["tags"]),
        "image": f"{SITE}/logo.png",
        "author": {"@type": "Organization", "name": "Rep Rot", "url": SITE},
        "publisher": {"@type": "Organization", "name": "Rep Rot",
                      "logo": {"@type": "ImageObject", "url": f"{SITE}/logo.png"}},
    }
    head = (f'<meta property="og:type" content="article">\n'
            f'<meta property="article:published_time" content="{post["date"].isoformat()}">\n'
            f'<script type="application/ld+json">{json.dumps(schema)}</script>\n')
    more = related(post, posts)
    more_html = ""
    if more:
        more_html = '\n  <h2 class="more-title">Keep reading</h2>\n  <div class="post-list">\n' + \
            "\n".join(card(p, "../") for p in more) + "\n  </div>"
    body = f"""
  <article class="post">
    <p class="crumb"><a href="../">Blog</a></p>
    <div class="tags">{tags_html(post)}</div>
    <h1>{esc(post['title'])}</h1>
    <div class="post-meta">{meta_line(post)}</div>

{post['body']}
  </article>

  <div class="card cta">
    <strong>Don't rot. Rep instead.</strong>
    <p>Rep Rot locks the apps you lose hours to, and wakes you with an alarm, until you do your reps. Your iPhone's camera counts them. It's in testing now: email us and we'll send you an early-access invite.</p>
    <a class="button" href="{EARLY_ACCESS}">Get early access</a>
  </div>
{more_html}"""
    return page(f"{post['title']} · Rep Rot", post["description"], url, "../../", body, head)


def index_page(posts):
    body = f"""
  <h1>The Rep Rot Blog</h1>
  <p class="lede">Practical guides for spending less time scrolling and more time moving: screen time, habits, bodyweight training and getting out of bed.</p>

  <div class="post-list">
{chr(10).join(card(p, "") for p in posts)}
  </div>"""
    return page("The Rep Rot Blog: Screen Time, Habits and Bodyweight Training",
                "Practical guides for spending less time scrolling and more time moving.",
                f"{SITE}/blog/", "../", body)


def feed(posts):
    items = "".join(f"""
  <item>
    <title>{esc(p['title'])}</title>
    <link>{SITE}/blog/{p['slug']}/</link>
    <guid>{SITE}/blog/{p['slug']}/</guid>
    <pubDate>{datetime.datetime.combine(p['date'], datetime.time(9)).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    <description>{esc(p['description'])}</description>
  </item>""" for p in posts[:30])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>The Rep Rot Blog</title>
  <link>{SITE}/blog/</link>
  <description>Practical guides for spending less time scrolling and more time moving.</description>{items}
</channel>
</rss>
"""


def sitemap(posts):
    today = datetime.date.today().isoformat()
    urls = [(f"{SITE}/{p}", today) for p in STATIC_PAGES]
    urls.append((f"{SITE}/blog/", posts[0]["date"].isoformat() if posts else today))
    urls += [(f"{SITE}/blog/{p['slug']}/", p["date"].isoformat()) for p in posts]
    rows = "".join(f"\n  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{rows}\n</urlset>\n'


def main():
    today = datetime.date.today()
    posts = [parse(p) for p in sorted(POSTS.glob("*.html"))]
    posts = [p for p in posts if p["date"] <= today]
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)

    # Remove pages for posts that were deleted or renamed.
    live = {p["slug"] for p in posts}
    for folder in BLOG.iterdir():
        if folder.is_dir() and folder.name not in live:
            (folder / "index.html").unlink(missing_ok=True)
            if not any(folder.iterdir()):
                folder.rmdir()

    for post in posts:
        out = BLOG / post["slug"]
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(post_page(post, posts), encoding="utf-8")
    (BLOG / "index.html").write_text(index_page(posts), encoding="utf-8")
    (BLOG / "feed.xml").write_text(feed(posts), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(posts), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nDisallow: /blog-src/\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(posts)} post(s).")


if __name__ == "__main__":
    main()
