#!/usr/bin/env python3
"""Procedural velocity-profile vessel plate (no AI, no manual registration).

Shared geometry with 02c_velocity_profile.svg:
  image placed at (20, 90), size 400×400
  CX=200, CY=200, R=150 in image pixels → page (220, 290), R=150

Usage:
  python3 illustration-prompts/build_velocity_profile_vessel.py
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

SIZE = 400
CX = 200
CY = 200
R = 150
WALL = 32

ROOT = Path(__file__).resolve().parent.parent
OUT_VESSEL = ROOT / "velocity_profile_vessel.png"
OUT_BASE = ROOT / "velocity_profile_vessel_base.png"

CREAM = (242, 239, 227)
LUMEN = (248, 245, 236)
GRAPHITE = (72, 70, 66)
GRAPHITE_MID = (130, 126, 118)
RBC = (180, 72, 68)
RBC_DARK = (140, 48, 46)
RBC_LIGHT = (210, 110, 100)


def clamp(v: int) -> int:
    return max(0, min(255, v))


def paper_grain(img: Image.Image, seed: int = 7, amp: int = 6) -> Image.Image:
    rng = random.Random(seed)
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            n = rng.randint(-amp, amp)
            px[x, y] = (clamp(r + n), clamp(g + n), clamp(b + n))
    return img


def in_annulus(x: float, y: float, r_in: float, r_out: float) -> bool:
    d = math.hypot(x - CX, y - CY)
    return r_in <= d <= r_out


def hatch_wall(draw: ImageDraw.ImageDraw, rng: random.Random) -> None:
    """Loose graphite strokes in the wall annulus only."""
    for _ in range(900):
        ang = rng.uniform(0, 2 * math.pi)
        rad = rng.uniform(R + 2, R + WALL - 2)
        x0 = CX + rad * math.cos(ang)
        y0 = CY + rad * math.sin(ang)
        # stroke roughly tangential
        tang = ang + math.pi / 2 + rng.uniform(-0.35, 0.35)
        length = rng.uniform(4, 14)
        x1 = x0 + length * math.cos(tang)
        y1 = y0 + length * math.sin(tang)
        if not (in_annulus(x0, y0, R + 1, R + WALL) and in_annulus(x1, y1, R + 1, R + WALL)):
            continue
        tone = rng.choice([GRAPHITE, GRAPHITE_MID, (95, 92, 88)])
        draw.line((x0, y0, x1, y1), fill=tone, width=rng.choice([1, 1, 2]))


def draw_rbc(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    a: float,
    b: float,
    rot_deg: float,
) -> None:
    """Cartoon biconcave disc: ellipse + dimple."""
    rot = math.radians(rot_deg)
    pts = []
    for i in range(24):
        t = 2 * math.pi * i / 24
        px = a * math.cos(t)
        py = b * math.sin(t)
        rx = x + px * math.cos(rot) - py * math.sin(rot)
        ry = y + px * math.sin(rot) + py * math.cos(rot)
        pts.append((rx, ry))
    draw.polygon(pts, fill=RBC, outline=RBC_DARK)

    da, db = a * 0.35, b * 0.28
    dim = []
    for i in range(16):
        t = 2 * math.pi * i / 16
        px = da * math.cos(t)
        py = db * math.sin(t)
        rx = x + px * math.cos(rot) - py * math.sin(rot)
        ry = y + px * math.sin(rot) + py * math.cos(rot)
        dim.append((rx, ry))
    draw.polygon(dim, fill=RBC_LIGHT)


def place_rbcs(draw: ImageDraw.ImageDraw, rng: random.Random, n: int = 28) -> None:
    """Natural scatter inside lumen — whole cells only, clear of the wall."""
    placed: list[tuple[float, float, float]] = []
    margin = 6.0  # pixels between cell tip and lumen rim
    tries = 0
    while len(placed) < n and tries < n * 60:
        tries += 1
        a = rng.uniform(R / 7.2, R / 5.8)  # semi-major (~cell size)
        b = a * rng.uniform(0.55, 0.85)
        # Keep center far enough that the longest axis cannot cross the wall
        max_center_r = R - a - margin
        if max_center_r <= 4:
            continue
        rad = max_center_r * math.sqrt(rng.uniform(0.0, 1.0))
        ang = rng.uniform(0, 2 * math.pi)
        x = CX + rad * math.cos(ang)
        y = CY + rad * math.sin(ang)
        if math.hypot(x - CX, y - CY) + a > R - margin:
            continue
        if any(math.hypot(x - px, y - py) < 0.9 * (a + pr) for px, py, pr in placed):
            continue
        placed.append((x, y, a))
        draw_rbc(draw, x, y, a, b, rng.uniform(0, 180))


def build_vessel(seed: int = 42) -> Image.Image:
    rng = random.Random(seed)
    img = Image.new("RGB", (SIZE, SIZE), CREAM)
    draw = ImageDraw.Draw(img)

    # Wall fill
    draw.ellipse(
        (CX - R - WALL, CY - R - WALL, CX + R + WALL, CY + R + WALL),
        fill=(205, 200, 190),
    )
    hatch_wall(draw, rng)

    # Exact lumen (geometry lock)
    draw.ellipse((CX - R, CY - R, CX + R, CY + R), fill=LUMEN)
    draw.ellipse((CX - R, CY - R, CX + R, CY + R), outline=GRAPHITE, width=2)

    # Outer wall edge, slightly imperfect pencil
    for _ in range(3):
        jitter = rng.uniform(-1.2, 1.2)
        draw.ellipse(
            (
                CX - R - WALL + jitter,
                CY - R - WALL + jitter,
                CX + R + WALL - jitter,
                CY + R + WALL - jitter,
            ),
            outline=GRAPHITE_MID,
            width=1,
        )

    place_rbcs(draw, rng)

    img = paper_grain(img, seed=seed, amp=5)
    # Re-assert exact lumen rim after grain (keep cells; only redraw stroke)
    draw = ImageDraw.Draw(img)
    draw.ellipse((CX - R, CY - R, CX + R, CY + R), outline=GRAPHITE, width=2)
    return img


def build_base() -> Image.Image:
    """Empty locked lumen for inspection / optional AI experiments."""
    img = Image.new("RGB", (SIZE, SIZE), CREAM)
    draw = ImageDraw.Draw(img)
    draw.ellipse(
        (CX - R - WALL, CY - R - WALL, CX + R + WALL, CY + R + WALL),
        fill=(210, 205, 194),
    )
    draw.ellipse((CX - R, CY - R, CX + R, CY + R), fill=LUMEN)
    draw.ellipse((CX - R, CY - R, CX + R, CY + R), outline=GRAPHITE, width=2)
    return paper_grain(img, seed=7, amp=4)


def main() -> None:
    base = build_base()
    base.save(OUT_BASE, "PNG")
    vessel = build_vessel()
    vessel.save(OUT_VESSEL, "PNG")
    print(f"wrote {OUT_VESSEL}")
    print(f"wrote {OUT_BASE}")
    print(f"locked: CX={CX} CY={CY} R={R} → page ({20 + CX}, {90 + CY}), R={R}")


if __name__ == "__main__":
    main()
