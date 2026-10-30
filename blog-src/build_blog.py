#!/usr/bin/env python3
"""Builds the Rep Rot blog from blog-src/posts/*.html into the site.

Each source post is an HTML body fragment that starts with a metadata
comment:

    <!--
    title: How to Stop Doomscrolling on iPhone
    description: One or two sentences for search results and the card.
    date: 2026-10-29
    tags: Screen Time, Habits
    cover: app-one-set
    -->
    <p>First paragraph...</p>

`cover` is optional: an exercise (squat, pushup, plank, pullup, crunch)
whose photo goes behind the post's cover. Without it, exercise tags pick
their photo and other posts get a tally-mark cover over a photo picked from
the slug. The photos are the app's own, darkened and blurred (see
blog-src/prepare_images.py).

Writes, from the repo root (the site GitHub Pages serves). blog-src/ is
served too, so robots.txt keeps crawlers out of it:
    blog/<slug>/index.html     one page per post (slug = file name)
    blog/img/covers/<slug>.jpg the post's cover (card, header, social preview)
    blog/index.html            the landing page, newest first
    blog/feed.xml              RSS
    sitemap.xml, robots.txt

Posts dated in the future are skipped, so a post can be written ahead.
Needs Pillow (pip install pillow). Run: python3 blog-src/build_blog.py
"""

import datetime
import html
import json
import math
import re
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Pillow is missing: run  pip install pillow  and build again.")

SITE = "https://reprotapp.com"
# Before launch the buttons ask for an early-access email; after launch,
# point them at the App Store (https://apps.apple.com/app/id6824360561).
EARLY_ACCESS = "mailto:help@reprotapp.com?subject=Rep%20Rot%20early%20access&body=Hi!%20I%27d%20like%20early%20access%20to%20Rep%20Rot.%20My%20iPhone%20model%3A%20"
ROOT = Path(__file__).resolve().parent.parent   # the repo root is the site (GitHub Pages)
POSTS = Path(__file__).resolve().parent / "posts"
BLOG = ROOT / "blog"
LIB = BLOG / "img" / "lib"
COVERS = BLOG / "img" / "covers"
FONT = ROOT / "fonts" / "ArchivoExpanded-Black.ttf"
STATIC_PAGES = ["", "support/", "privacy/"]
KEEP = {"img"}   # folders in blog/ that aren't posts

# Exercise tags pick a photo for the cover when the post doesn't name one.
TAG_PHOTOS = {"Squats": "squat", "Push-Ups": "pushup", "Plank": "plank",
              "Pull-Ups": "pullup", "Sit-Ups": "crunch"}


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
    tags = [t.strip() for t in meta["tags"].split(",") if t.strip()]
    cover = meta.get("cover") or next((TAG_PHOTOS[t] for t in tags if t in TAG_PHOTOS), "")
    if cover and cover not in TAG_PHOTOS.values():
        raise SystemExit(f"{path.name}: cover must be one of {', '.join(TAG_PHOTOS.values())}")
    body = match.group(2).strip()
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    return {
        "slug": path.stem,
        "title": meta["title"],
        "description": meta["description"],
        "date": datetime.date.fromisoformat(meta["date"]),
        "tags": tags,
        "cover": cover,
        "body": body,
        "minutes": max(1, math.ceil(words / 230)),
    }


# MARK: - Covers

def font(size):
    return ImageFont.truetype(str(FONT), size)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def tracked(draw, xy, text, fnt, fill, spacing):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *img.size), radius, fill=255)
    out = Image.new("RGBA", img.size)
    out.paste(img, (0, 0), mask)
    return out


def make_cover(post, path):
    """1200×675, in the App Store screenshots' style: black, wide caps."""
    W, H, pad = 1200, 675, 72
    img = Image.new("RGB", (W, H), (10, 10, 11))
    draw = ImageDraw.Draw(img)
    text_w = W - 2 * pad
    name = post["cover"]

    # Background: one of the app's exercise photos, blurred and darkened
    # (blog/img/lib/bg-*.jpg). Exercise posts get their own exercise; the
    # rest get one picked from the slug, with tally marks on top.
    bg = name or sorted(TAG_PHOTOS.values())[sum(map(ord, post["slug"])) % len(TAG_PHOTOS)]
    img.paste(Image.open(LIB / f"bg-{bg}.jpg").convert("RGB").resize((W, H)))
    shade = Image.linear_gradient("L").rotate(90).resize((W, H)).point(lambda v: 235 - int(v * 0.7))
    img.paste(Image.new("RGB", (W, H), (8, 8, 9)), (0, 0), shade)   # darker behind the title
    draw = ImageDraw.Draw(img)
    if not name:
        # Tally marks: the reps you'd count on a wall.
        mark = (58, 58, 62)
        for g in range(3):
            x0 = 700 + g * 170
            for i in range(4):
                draw.rounded_rectangle((x0 + i * 30, 170, x0 + i * 30 + 12, 470), 6, fill=mark)
            draw.line((x0 - 22, 420, x0 + 122, 220), fill=mark, width=13)
    text_w = 580

    tracked(draw, (pad, pad), post["tags"][0].upper(), font(19), (150, 156, 163), 3)

    title = post["title"].upper()
    for size in range(68, 30, -2):
        fnt = font(size)
        lines = wrap(draw, title, fnt, text_w)
        if len(lines) <= 5:
            break
    y = pad + 58
    for line in lines:
        draw.text((pad, y), line, font=fnt, fill=(245, 245, 246))
        y += int(size * 1.12)

    logo = Image.open(ROOT / "logo.png").convert("RGBA").resize((46, 46), Image.LANCZOS)
    img.paste(logo, (pad, H - pad - 46), logo)
    tracked(draw, (pad + 62, H - pad - 34), "REP ROT", font(20), (245, 245, 246), 2)
    img.save(path, quality=80, optimize=True)


# MARK: - HTML

def esc(text):
    return html.escape(text, quote=True)


def nice_date(date):
    return date.strftime("%b %-d, %Y")


def byline(post, up):
    return (f'<div class="byline"><img class="avatar" src="{up}logo.png" alt="">'
            f'<span>Rep Rot Team</span><span class="dot">·</span>'
            f'<time datetime="{post["date"].isoformat()}">{nice_date(post["date"])}</time>'
            f'<span class="dot">·</span><span>{post["minutes"]} min read</span></div>')


def card(post, to_blog, up):
    """to_blog = path to /blog/ from the page; up = path to the site root."""
    return f"""    <a class="post-card" href="{to_blog}{post['slug']}/">
      <div class="thumb"><img src="{to_blog}img/covers/{post['slug']}.jpg" alt="" loading="lazy" width="1200" height="675"></div>
      <div class="card-body">
        <h3>{esc(post['title'])}</h3>
        <p>{esc(post['description'])}</p>
        <div class="byline"><time datetime="{post['date'].isoformat()}">{nice_date(post['date'])}</time><span class="dot">·</span><span>{post['minutes']} min read</span></div>
      </div>
    </a>"""


def page(title, description, url, up, body, image, extra_head=""):
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
<meta property="og:image" content="{image}">
<meta property="og:site_name" content="Rep Rot">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="Rep Rot Blog" href="{SITE}/blog/feed.xml">
<link rel="icon" href="{up}logo.png">
<link rel="stylesheet" href="{up}style.css">
{extra_head}</head>
<body class="blog">
<header class="site-head">
  <div class="wrap head-row">
    <a class="logo" href="{up}"><img src="{up}logo.png" alt=""><span class="brand">Rep Rot</span></a>
    <nav class="head-nav"><a href="{up}blog/">Blog</a><a href="{up}support/">Support</a><a class="pill" href="{EARLY_ACCESS}">Early access</a></nav>
  </div>
</header>
<main class="wrap">
{body}
</main>
<footer class="site-foot">
  <div class="wrap foot-row">
    <span>© {datetime.date.today().year} Rep Rot. Don't rot. Rep instead.</span>
    <nav><a href="{up}">Home</a><a href="{up}blog/">Blog</a><a href="{up}support/">Support</a><a href="{up}privacy/">Privacy</a><a href="{SITE}/blog/feed.xml">RSS</a></nav>
  </div>
</footer>
</body>
</html>
"""


def related(post, posts):
    """Three other posts: most shared tags first, then newest."""
    others = [p for p in posts if p["slug"] != post["slug"]]
    others.sort(key=lambda p: (-len(set(p["tags"]) & set(post["tags"])), -p["date"].toordinal()))
    return others[:3]


def prose(body):
    """Moves the TL;DR section to the top of the post, boxed as a summary
    card, wherever the writer put it."""
    match = re.search(r"<h2>TL;DR</h2>\s*(<ul>.*?</ul>)", body, flags=re.S)
    if not match:
        return body
    rest = (body[:match.start()] + body[match.end():]).strip()
    return f'<div class="tldr"><h2>TL;DR</h2>{match.group(1)}</div>\n\n{rest}'



CTA = f"""  <aside class="cta-card">
    <div>
      <p class="cta-kicker">Rep Rot · in testing</p>
      <h2>Don't rot. Rep instead.</h2>
      <p>Rep Rot locks the apps you lose hours to, and wakes you with an alarm, until you do your reps. Your iPhone's camera counts them. Email us and we'll send you an early-access invite.</p>
    </div>
    <a class="button" href="{EARLY_ACCESS}">Get early access</a>
  </aside>"""


def post_page(post, posts):
    url = f"{SITE}/blog/{post['slug']}/"
    image = f"{SITE}/blog/img/covers/{post['slug']}.jpg"
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["description"],
        "datePublished": post["date"].isoformat(),
        "dateModified": post["date"].isoformat(),
        "mainEntityOfPage": url,
        "keywords": ", ".join(post["tags"]),
        "image": image,
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
        more_html = ('\n  <section class="more">\n    <h2>Keep reading</h2>\n    <div class="grid">\n'
                     + "\n".join(card(p, "../", "../../") for p in more) + "\n    </div>\n  </section>")
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in post["tags"])
    body = f"""  <article class="post">
    <div class="post-head">
      <a class="crumb" href="../">← All posts</a>
      <div class="tags">{tags}</div>
      <h1>{esc(post['title'])}</h1>
      <p class="dek">{esc(post['description'])}</p>
      {byline(post, "../../")}
    </div>
    <figure class="post-cover"><img src="../img/covers/{post['slug']}.jpg" alt="" width="1200" height="675"></figure>
    <div class="prose">
{prose(post['body'])}
    </div>
  </article>
{CTA}
{more_html}"""
    return page(f"{post['title']} · Rep Rot", post["description"], url, "../../", body, image, head)


def index_page(posts):
    featured, rest = (posts[0], posts[1:]) if posts else (None, [])
    feat_html = ""
    if featured:
        tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in featured["tags"])
        feat_html = f"""  <a class="featured" href="{featured['slug']}/">
    <div class="thumb"><img src="img/covers/{featured['slug']}.jpg" alt="" width="1200" height="675"></div>
    <div class="featured-body">
      <div class="tags">{tags}</div>
      <h2>{esc(featured['title'])}</h2>
      <p>{esc(featured['description'])}</p>
      {byline(featured, "../")}
    </div>
  </a>"""
    grid = ""
    if rest:
        grid = '\n  <div class="grid">\n' + "\n".join(card(p, "", "../") for p in rest) + "\n  </div>"
    body = f"""  <section class="blog-hero">
    <h1>The Rep Rot Blog</h1>
    <p class="lede">Practical guides for spending less time scrolling and more time moving: screen time, habits, bodyweight training and getting out of bed.</p>
  </section>
{feat_html}{grid}
{CTA}"""
    image = f"{SITE}/blog/img/covers/{featured['slug']}.jpg" if featured else f"{SITE}/logo.png"
    return page("The Rep Rot Blog: Screen Time, Habits and Bodyweight Training",
                "Practical guides for spending less time scrolling and more time moving.",
                f"{SITE}/blog/", "../", body, image)


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

    # Remove pages and covers for posts that were deleted or renamed.
    live = {p["slug"] for p in posts}
    for folder in BLOG.iterdir():
        if folder.is_dir() and folder.name not in live | KEEP:
            (folder / "index.html").unlink(missing_ok=True)
            if not any(folder.iterdir()):
                folder.rmdir()
    COVERS.mkdir(parents=True, exist_ok=True)
    for cover in COVERS.glob("*.jpg"):
        if cover.stem not in live:
            cover.unlink()

    for post in posts:
        # An AI header illustration (blog-src/gen_image.py) is the cover when
        # the post has one; otherwise the generated title cover.
        header = BLOG / "img" / "posts" / f"{post['slug']}-header.jpg"
        if header.exists():
            Image.open(header).convert("RGB").resize((1200, 675)).save(COVERS / f"{post['slug']}.jpg", quality=82, optimize=True)
        else:
            make_cover(post, COVERS / f"{post['slug']}.jpg")
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
