# reprotapp.com

The Rep Rot website, served by GitHub Pages from `main` (custom domain in
`CNAME`). Every push to `main` goes live.

- Site pages: `index.html`, `style.css`. Support and Privacy are generated from `blog-src/pages/` (edit those).
- Generated, don't edit by hand: `blog/`, `sitemap.xml`, `robots.txt`.
- `blog-src/`: blog sources. `posts/` (one HTML fragment per post), `WRITING.md`
  (rules), `topics.md` (queue), `daily-prompt.md` (the daily routine's
  instructions), `logs/published.md`.
- Build: `python3 blog-src/build_blog.py`

A daily Claude routine writes one post, builds, and pushes to `main`.
