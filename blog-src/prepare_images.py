#!/usr/bin/env python3
"""Makes blog/img/lib/ from the app's own pictures (run on the Mac, once,
or again when the app's pictures change; the results are committed, so the
daily routine never needs the originals).

    python3 blog-src/prepare_images.py ~/Documents/FitnessDailies

- Exercise photos → darkened, desaturated and blurred to sit in the black
  theme:  <name>.jpg (inline, 960×540, soft blur) and bg-<name>.jpg (cover
  background, 1200×675, heavy blur).
- App Store screenshots → app-<name>.jpg, cropped to the phone (no caption).
"""

import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

LIB = Path(__file__).resolve().parent.parent / "blog" / "img" / "lib"

PHOTOS = {"squat": "Male_Squat.png", "pushup": "Male_push_up.png", "plank": "male_plank.png",
          "pullup": "Male_pull_up.png", "crunch": "Male_Crunch.png"}
SHOTS = {"app-dont-rot": "01-dont-rot", "app-home": "02-every-rep", "app-triggers": "03-triggers",
         "app-pick-trigger": "04-your-call", "app-one-set": "05-one-set",
         "app-rots-prevented": "06-rots-prevented"}


def theme(img, size, blur, brightness):
    """Crop to 16:9 (dropping the corner mark), then mute it into the theme."""
    w, h = img.size
    ch = int(h * 0.9)
    cw = int(ch * 16 / 9)
    img = img.crop((int(w * 0.015), 0, int(w * 0.015) + cw, ch)).resize(size, Image.LANCZOS)
    img = ImageEnhance.Color(img).enhance(0.2)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    # Vignette: darker towards the edges.
    vig = Image.radial_gradient("L").resize(size).point(lambda v: int(v * 0.75))
    return Image.composite(Image.new("RGB", size, (6, 6, 7)), img, vig)


def main(app_dir):
    app = Path(app_dir).expanduser()
    LIB.mkdir(parents=True, exist_ok=True)
    for name, file in PHOTOS.items():
        src = Image.open(app / file).convert("RGB")
        theme(src, (960, 540), 2.5, 0.55).save(LIB / f"{name}.jpg", quality=80, optimize=True)
        theme(src, (1200, 675), 9, 0.42).save(LIB / f"bg-{name}.jpg", quality=78, optimize=True)
    for name, file in SHOTS.items():
        shot = Image.open(app / "AppStore" / "Screenshots-6.9" / f"{file}.png").convert("RGB")
        w, h = shot.size
        shot = shot.crop((0, int(h * 0.19), w, h))
        shot = shot.resize((360, int(shot.height * 360 / w)), Image.LANCZOS)
        shot.save(LIB / f"{name}.jpg", quality=82, optimize=True)
    print("Wrote", 2 * len(PHOTOS) + len(SHOTS), "images to", LIB)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "~/Documents/FitnessDailies")
