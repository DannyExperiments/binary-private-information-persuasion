#!/usr/bin/env python3
"""Render the exact one-variable test gadget and rotate its mass coordinates."""
from itertools import combinations, product
from math import cos, pi, sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 664, 432
COLORS = ["#101a28", "#17283a", "#30495f", "#f3f5fa", "#b6c9dc", "#7ce0cb", "#ffc378", "#60869d"]
VERTICES = list(product((0, 1), repeat=3))
EDGES = [(a, b) for a, b in combinations(VERTICES, 2) if sum(x != y for x, y in zip(a, b)) == 1]
ORIGIN = (0, 0, 0)
WITNESSES = [(.8, 1, .05), (.8, 1, .75)]


def font(size, bold=False):
    names = ("Arial Bold.ttf", "DejaVuSans-Bold.ttf") if bold else ("Arial.ttf", "DejaVuSans.ttf")
    for name in names:
        for root in (Path("/System/Library/Fonts/Supplemental"), Path("/usr/share/fonts/truetype/dejavu")):
            path = root / name
            if path.is_file():
                return ImageFont.truetype(str(path), size)
    raise RuntimeError("Arial or DejaVu Sans is required to render the GIF")


FONTS = [font(32, True), font(19), font(23, True), font(22, True), font(18), font(19, True)]


def project(point, angle):
    x, y, z = (u - .5 for u in point)
    x, z = x*cos(angle) + z*sin(angle), -x*sin(angle) + z*cos(angle)
    y, z = y*cos(.44) - z*sin(.44), y*sin(.44) + z*cos(.44)
    scale = 139*5/(5-z)
    return 189 + x*scale, 217 - y*scale, z


def frame(angle, unsat):
    image = Image.new("RGB", (W, H), COLORS[0])
    d = ImageDraw.Draw(image)
    d.text((24, 17), "Guard signals penalize imbalance", font=FONTS[0], fill=COLORS[3])
    d.text((24, 58), "Exact one-variable instance  ·  Anchor test scores", font=FONTS[1], fill=COLORS[4])
    d.rounded_rectangle((24, 103, 353, 350), radius=18, fill=COLORS[1], outline=COLORS[2])
    d.rounded_rectangle((366, 103, 640, 350), radius=18, fill=COLORS[1], outline=COLORS[2])
    v = {p: project(p, angle) for p in VERTICES}
    for a, b in sorted(EDGES, key=lambda e:v[e[0]][2]+v[e[1]][2]):
        col = COLORS[7 if v[a][2] + v[b][2] > 0 else 2]
        d.line((*v[a][:2], *v[b][:2]), fill=col, width=2)
    center = v[ORIGIN][:2]
    for i, point in enumerate(WITNESSES):
        x, y, _ = project(point, angle)
        color = COLORS[5 if i == 1 else 4]
        radius = 8 if i == 1 else 6
        d.line((*center, x, y), fill=color, width=3 if i else 1)
        d.ellipse((x-radius,y-radius,x+radius,y+radius), fill=color if i == 1 else COLORS[1], outline=color, width=2)
    d.text((41, 321), "Balanced masses  (t, x, z)", font=FONTS[4], fill=COLORS[4])

    color = COLORS[6 if unsat else 5]
    d.text((385, 121), "UNSAT example" if unsat else "SAT example", font=FONTS[2], fill=color)
    d.text((385, 159), "t = 32z, x = 30z", font=FONTS[4], fill=COLORS[3])
    d.text((385, 190), "3 of 5 tests pass" if unsat else "4 of 5 tests pass", font=FONTS[3], fill=COLORS[3])
    d.text((385, 229), "Guard ties favor action 1.", font=FONTS[4], fill=COLORS[4])
    d.text((385, 263), "Second clause score" if unsat else "Both clause scores", font=FONTS[4], fill=COLORS[4])
    d.text((385, 297), "−10z" if unsat else "74z each", font=FONTS[3], fill=color)
    d.text((24, 372), "Certified payoff after subtracting each baseline and scaling", font=FONTS[4], fill=COLORS[4])
    d.text((24, 399), "UNSAT ≤ 13/4    ·    Decision at 7/2    ·    SAT ≥ 4", font=FONTS[5], fill=COLORS[3])
    return image


def main():
    palette = Image.new("P", (1, 1))
    palette.putpalette([int(c[i:i+2],16) for c in COLORS for i in (1,3,5)] + [0,0,0]*(256-len(COLORS)))
    frames = [frame(tau*i/48 + pi/6, i>=24).quantize(palette=palette,dither=Image.Dither.NONE) for i in range(48)]
    target = Path(__file__).resolve().with_name("anchor-and-guards.gif")
    frames[0].save(target, save_all=True, append_images=frames[1:], loop=0, duration=130, optimize=True, disposal=1)


if __name__ == "__main__":
    main()
