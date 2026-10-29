"""Example artwork for the blog, drawn with Pillow: no photos.

- Exercise figures (squat, pushup, plank, pullup, crunch): bold line
  figures, used on covers and as inline pictures.
- Phone mockups (app-*): a simplified Rep Rot screen.

`python3 blog-src/art.py` (re)writes blog/img/lib/. These are stand-ins:
to use real pictures later, replace a file in blog/img/lib/ with one of the
same name and size (960×540 .jpg for exercises, 360×720 .png for phones).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "blog" / "img" / "lib"
FONT = ROOT / "fonts" / "ArchivoExpanded-Black.ttf"

INK = (17, 18, 20)
PAPER = (238, 240, 243)
WHITE = (245, 245, 246)
GREEN = (52, 199, 89)

# Joints on a 960×540 canvas, floor at y=440. Each figure is a list of
# limbs (polylines) plus the head's centre.
FIGURES = {
    "squat": {"head": (548, 168), "limbs": [
        [(530, 212), (452, 318), (566, 330), (548, 440), (590, 440)],   # back, thigh, shin, foot
        [(526, 222), (630, 250)]]},                                     # arms forward
    "pushup": {"head": (300, 292), "limbs": [
        [(340, 318), (560, 352), (790, 404), (812, 440)],                # body line to toes
        [(352, 322), (352, 440)]]},                                     # straight arm
    "plank": {"head": (292, 340), "limbs": [
        [(334, 362), (560, 384), (790, 414), (812, 440)],
        [(342, 372), (342, 440), (420, 440)]]},                         # forearm on the floor
    "pullup": {"head": (480, 150), "limbs": [
        [(480, 196), (480, 330), (456, 404), (500, 462)],               # body, bent knees
        [(480, 200), (420, 196), (424, 104)],                           # left arm to bar
        [(480, 200), (540, 196), (536, 104)]]},                         # right arm to bar
    "crunch": {"head": (352, 336), "limbs": [
        [(392, 366), (478, 430), (590, 350), (660, 440), (700, 440)],   # back, thigh, shin, foot
        [(402, 380), (456, 360)]]},                                     # arms across chest
}


def font(size):
    return ImageFont.truetype(str(FONT), size)


def draw_figure(draw, name, color, scale=1.0, offset=(0, 0), floor=True):
    fig = FIGURES[name]
    ox, oy = offset
    p = lambda pt: (ox + pt[0] * scale, oy + pt[1] * scale)
    w = max(4, int(26 * scale))
    if floor and name != "pullup":
        draw.rounded_rectangle((p((170, 446))[0], p((0, 446))[1], p((880, 0))[0], p((0, 454))[1]), int(4 * scale), fill=color)
    if name == "pullup":
        draw.rounded_rectangle((p((360, 92))[0], p((0, 92))[1], p((600, 0))[0], p((0, 106))[1]), int(7 * scale), fill=color)
    for limb in fig["limbs"]:
        pts = [p(pt) for pt in limb]
        draw.line(pts, fill=color, width=w, joint="curve")
        for x, y in pts:
            draw.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=color)
    hx, hy = p(fig["head"])
    r = 30 * scale
    draw.ellipse((hx - r, hy - r, hx + r, hy + r), fill=color)


def exercise(name):
    img = Image.new("RGB", (960, 540), PAPER)
    draw = ImageDraw.Draw(img)
    draw_figure(draw, name, INK)
    return img


# MARK: - Phone mockups

def bar(d, x, y, w, h=14, fill=(58, 60, 66)):
    d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=fill)


def toggle(d, x, y, on=True):
    d.rounded_rectangle((x, y, x + 46, y + 28), 14, fill=GREEN if on else (72, 74, 80))
    cx = x + 32 if on else x + 14
    d.ellipse((cx - 11, y + 3, cx + 11, y + 25), fill=WHITE)


def centred(d, y, text, size, fill=WHITE, width=360):
    f = font(size)
    d.text(((width - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)


def phone(name):
    W, H = 360, 720
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # transparent corners
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, H - 1), 52, fill=INK)
    d.rounded_rectangle((12, 12, W - 13, H - 13), 42, fill=(6, 6, 7))
    d.rounded_rectangle((W / 2 - 50, 26, W / 2 + 50, 54), 14, fill=INK)   # dynamic island
    card = (24, 25, 28)

    if name == "app-dont-rot":
        d.rounded_rectangle((152, 250, 208, 306), 14, fill=WHITE)
        centred(d, 266, "RR", 22, INK)
        centred(d, 340, "DON'T ROT.", 26)
        centred(d, 376, "REP INSTEAD.", 26)
        bar(d, 110, 430, 140, 10)
    elif name == "app-home":
        d.text((36, 84), "REP ROT", font=font(18), fill=WHITE)
        d.rounded_rectangle((28, 124, W - 28, 196), 18, fill=card)
        for i in range(7):
            x = 52 + i * 40
            d.ellipse((x - 14, 146, x + 14, 174), outline=WHITE, width=3)
            if i < 5:
                d.line([(x - 6, 160), (x - 1, 166), (x + 7, 154)], fill=WHITE, width=3)
        d.rounded_rectangle((28, 214, W - 28, 470), 22, fill=(32, 38, 52))
        draw_figure(d, "pushup", (120, 132, 156), scale=0.3, offset=(12, 196))
        d.text((48, 392), "PUSH-UPS", font=font(24), fill=WHITE)
        bar(d, 48, 428, 120, 10, (120, 132, 156))
        d.rounded_rectangle((28, 490, W - 28, 560), 18, fill=card)
        bar(d, 48, 512, 90, 10, (110, 112, 118)); bar(d, 48, 532, 170, 12)
    elif name == "app-triggers":
        d.text((36, 84), "ALARMS", font=font(14), fill=(140, 144, 150))
        for i, on in enumerate([True, True, False]):
            y = 112 + i * 70
            d.rounded_rectangle((28, y, W - 28, y + 60), 16, fill=card)
            d.text((48, y + 14), ["7:00 AM", "9:30 AM", "9:00 PM"][i], font=font(20), fill=WHITE if on else (110, 112, 118))
            toggle(d, W - 90, y + 16, on)
        d.text((36, 336), "APP LIMITS", font=font(14), fill=(140, 144, 150))
        for i in range(2):
            y = 364 + i * 70
            d.rounded_rectangle((28, y, W - 28, y + 60), 16, fill=card)
            d.rounded_rectangle((46, y + 14, 78, y + 46), 9, fill=[(10, 132, 255), (255, 69, 58)][i])
            bar(d, 92, y + 16, 90, 12, WHITE); bar(d, 92, y + 36, 120, 9)
            toggle(d, W - 90, y + 16)
    elif name == "app-pick-trigger":
        d.text((36, 96), "WHEN SHOULD", font=font(22), fill=WHITE)
        d.text((36, 126), "WE MAKE YOU REP?", font=font(22), fill=WHITE)
        for i, chosen in enumerate([True, False]):
            y = 196 + i * 100
            d.rounded_rectangle((28, y, W - 28, y + 84), 18, fill=card, outline=WHITE if chosen else card, width=2)
            bar(d, 52, y + 24, [130, 150][i], 14, WHITE); bar(d, 52, y + 50, 170, 10)
            if chosen:
                d.ellipse((W - 76, y + 26, W - 44, y + 58), fill=WHITE)
                d.line([(W - 68, y + 42), (W - 62, y + 49), (W - 51, y + 35)], fill=INK, width=4)
            else:
                d.ellipse((W - 76, y + 26, W - 44, y + 58), outline=(110, 112, 118), width=3)
        d.rounded_rectangle((28, 620, W - 28, 668), 14, fill=WHITE)
        centred(d, 636, "CONTINUE", 14, INK)
    elif name == "app-one-set":
        d.rounded_rectangle((40, 220, W - 40, 470), 26, fill=(200, 203, 208))
        d.ellipse((140, 248, 220, 328), fill=GREEN)
        d.line([(160, 290), (175, 305), (202, 272)], fill=WHITE, width=9, joint="curve")
        centred(d, 352, "20 PUSH-UPS.", 20, INK)
        centred(d, 380, "DONE.", 20, INK)
        d.rounded_rectangle((146, 420, 214, 450), 15, fill=(255, 149, 0))
    elif name == "app-rots-prevented":
        d.text((36, 84), "REP ROT", font=font(18), fill=WHITE)
        d.rounded_rectangle((28, 130, W - 28, 230), 20, fill=WHITE)
        d.rounded_rectangle((48, 162, 72, 192), 5, fill=INK)                    # lock body
        d.arc((50, 146, 70, 174), 180, 360, fill=INK, width=4)                   # shackle
        d.text((88, 152), "APP BLOCKED", font=font(15), fill=INK)
        bar(d, 88, 180, 120, 9, (150, 152, 158))
        d.rounded_rectangle((W - 120, 160, W - 44, 196), 18, fill=INK)
        d.text((W - 108, 171), "REP NOW", font=font(11), fill=WHITE)
        d.rounded_rectangle((28, 250, W - 28, 320), 18, fill=card)
        d.rounded_rectangle((46, 266, 84, 304), 10, fill=(225, 48, 108))
        bar(d, 100, 272, 110, 12, WHITE); bar(d, 100, 292, 80, 9)
        d.rounded_rectangle((28, 340, W - 28, 560), 22, fill=(32, 38, 52))
        draw_figure(d, "squat", (120, 132, 156), scale=0.3, offset=(40, 330))
        d.text((48, 494), "SQUATS", font=font(22), fill=WHITE)
    else:
        raise ValueError(name)
    return img


PHONES = ["app-dont-rot", "app-home", "app-triggers", "app-pick-trigger", "app-one-set", "app-rots-prevented"]


def main():
    LIB.mkdir(parents=True, exist_ok=True)
    for name in FIGURES:
        exercise(name).save(LIB / f"{name}.jpg", quality=78, optimize=True)
    for name in PHONES:
        phone(name).save(LIB / f"{name}.png", optimize=True)
    print("Wrote", len(FIGURES) + len(PHONES), "images to", LIB)


if __name__ == "__main__":
    main()
