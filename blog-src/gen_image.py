#!/usr/bin/env python3
"""Generates one blog illustration with an AI image model.

    python3 blog-src/gen_image.py <name> "<what the picture shows>"

Writes blog/img/posts/<name>.jpg (1200×675). Name it <slug>-header for the
post's header (it also becomes the post's cover and social image), and
<slug>-1, <slug>-2 for pictures inside the post.

Describe only the scene; the house style below is added to every prompt so
all posts look like one set. Images must not contain text.

Needs one API key, from the environment or a file:
    GEMINI_API_KEY   (Google, default model gemini-2.5-flash-image), or
    OPENAI_API_KEY   (OpenAI, model gpt-image-1)
    file: ~/.config/reprot/image_api_key  ("gemini:<key>" or "openai:<key>")
Override the model with IMAGE_MODEL. Standard library only.
"""

import base64
import io
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "blog" / "img" / "posts"

STYLE = (
    "Editorial illustration for a fitness and screen-time blog. Moody, premium, "
    "modern: a near-black and charcoal palette with soft grays, and exactly one "
    "accent color, warm orange (#FF9500), used sparingly. Clean semi-flat 3D "
    "illustration style with soft studio lighting, gentle shadows and plenty of "
    "negative space; minimal props; calm composition, centered subject. If people "
    "appear, show them stylized and athletic, faces simple. Wide 16:9 frame. "
    "Absolutely no text, letters, numbers, logos, watermarks or UI labels anywhere."
)


def key():
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini", os.environ["GEMINI_API_KEY"]
    if os.environ.get("OPENAI_API_KEY"):
        return "openai", os.environ["OPENAI_API_KEY"]
    path = Path.home() / ".config" / "reprot" / "image_api_key"
    if path.exists():
        provider, _, value = path.read_text().strip().partition(":")
        if provider in ("gemini", "openai") and value:
            return provider, value
    raise SystemExit("No image API key: set GEMINI_API_KEY or OPENAI_API_KEY (see this file's header).")


def post(url, body, headers):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=180) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Image API error {e.code}: {e.read().decode()[:500]}")


def gemini(api_key, prompt):
    model = os.environ.get("IMAGE_MODEL", "gemini-2.5-flash-image")
    data = post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                {"contents": [{"parts": [{"text": prompt}]}],
                 "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9"}}},
                {"x-goog-api-key": api_key})
    for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        inline = part.get("inlineData") or part.get("inline_data")
        if inline:
            return base64.b64decode(inline["data"])
    raise SystemExit(f"No image in the response: {json.dumps(data)[:500]}")


def openai(api_key, prompt):
    model = os.environ.get("IMAGE_MODEL", "gpt-image-1")
    data = post("https://api.openai.com/v1/images/generations",
                {"model": model, "prompt": prompt, "size": "1536x1024", "quality": "medium", "n": 1},
                {"Authorization": f"Bearer {api_key}"})
    return base64.b64decode(data["data"][0]["b64_json"])


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    name, scene = sys.argv[1], sys.argv[2]
    provider, api_key = key()
    raw = (gemini if provider == "gemini" else openai)(api_key, f"{scene}\n\n{STYLE}")

    from PIL import Image   # resize to 16:9, 1200 wide, small JPEG
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = img.size
    target = w * 9 / 16
    if h > target:
        top = int((h - target) / 2)
        img = img.crop((0, top, w, top + int(target)))
    else:
        cw = int(h * 16 / 9)
        img = img.crop(((w - cw) // 2, 0, (w - cw) // 2 + cw, h))
    img = img.resize((1200, 675), Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.jpg"
    img.save(path, quality=80, optimize=True)
    print(f"Wrote {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB) with {provider}")


if __name__ == "__main__":
    main()
