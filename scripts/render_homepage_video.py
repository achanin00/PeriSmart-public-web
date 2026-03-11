#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import io
import json
import math
import os
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import cairosvg
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "video"
TMP_DIR = ROOT / ".tmp_video_render"
FONT_DIR = ROOT / "assets" / "fonts"

DESIGN_WIDTH = 1920
DESIGN_HEIGHT = 1080
OUTPUT_WIDTH = 1280
OUTPUT_HEIGHT = 720
FPS = 24

BG = "#ffffff"
BG_SOFT = "#f5f7fa"
INK = "#1a1d21"
INK_SOFT = "#5f6770"
ACCENT = "#1e6beb"
ACCENT_HOVER = "#1558c9"
GREEN = "#12a05c"
NAVY = "#0f172a"
CORAL = "#ef866e"
GOLD = "#f0c65d"
CARD = "#ffffff"
LINE = "#e6ebef"

FADE_DURATION = 0.4  # seconds per fade-in / fade-out
FADE_FRAMES = max(1, int(FADE_DURATION * FPS))
PROGRESS_HEIGHT = 4

FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/plusjakartasans/PlusJakartaSans%5Bwght%5D.ttf"
FONT_VAR = FONT_DIR / "PlusJakartaSans-wght.ttf"
FONT_REG = FONT_DIR / "PlusJakartaSans-Regular.ttf"
FONT_BOLD = FONT_DIR / "PlusJakartaSans-Bold.ttf"
FONT_XBOLD = FONT_DIR / "PlusJakartaSans-ExtraBold.ttf"


@dataclass
class Scene:
    slug: str
    voiceover: str
    eyebrow: str
    title: str
    body: str
    renderer: str


SCENES = [
    Scene(
        slug="problem",
        eyebrow="The Problem",
        title="The schedule gets stale the moment the first case moves.",
        body="Phone calls and status chasing create delay before the board even shows it.",
        renderer="render_problem",
        voiceover=(
            "Every day, perioperative teams manage millions of dollars in O.R. time "
            "\u2014 with phone calls, gut instinct, and schedules that go stale the moment "
            "the first case starts. A room runs long, turnovers drag, and the cascade "
            "hits every patient down the line. What if you could see and analyze "
            "what\u2019s happening \u2014 in real time \u2014 before the delays pile up "
            "and use that data to improve turnovers, better allocate block time, "
            "and optimize room utilization?"
        ),
    ),
    Scene(
        slug="intro",
        eyebrow="PeriSmart",
        title="Real-time perioperative intelligence.",
        body="What's running. What's next. What's at risk.",
        renderer="render_intro",
        voiceover=(
            "PeriSmart gives your team a live picture of every operating room "
            "\u2014 what\u2019s running, what\u2019s next, and what\u2019s at risk "
            "\u2014 all without a single phone call. The actual case and turnover "
            "times are used to improve analysis and make better projections."
        ),
    ),
    Scene(
        slug="or-board",
        eyebrow="OR Board",
        title="One timeline for planned, actual, and predicted flow.",
        body="A shared view for charge nurses, periop leaders, anesthesia, pre-op, and PACU.",
        renderer="render_or_board",
        voiceover=(
            "The O.R. Board shows every room on a single timeline. Scheduled cases "
            "sit alongside real-time progress \u2014 so you can see at a glance which "
            "rooms are on track, which are running long, and exactly when the next "
            "turnover will begin. No more walking the halls or calling into rooms."
        ),
    ),
    Scene(
        slug="case-detail",
        eyebrow="Case Detail",
        title="Milestones and finish-time predictions in one panel.",
        body="PeriSmart turns room activity into a case-level timeline teams can trust.",
        renderer="render_case_detail",
        voiceover=(
            "Click any case to see the full picture \u2014 nine milestones tracked "
            "automatically from Patient In to Patient Out. PeriSmart detects each "
            "event using computer vision, predicts when the case will finish, and "
            "shows you the variance from the original schedule. You know exactly "
            "where every case stands."
        ),
    ),
    Scene(
        slug="analytics",
        eyebrow="Analytics",
        title="Turnover, idle time, room use, and block use.",
        body="",
        renderer="render_analytics",
        voiceover=(
            "Beyond the day-of board, PeriSmart gives your leadership team the "
            "analytics to drive lasting improvement. Turnover times broken down by "
            "phase \u2014 cleaning, idle, and setup \u2014 so you can pinpoint where "
            "minutes are lost. Room and block utilization trends, tracked daily, "
            "weekly, and monthly, with export to CSV for analysis."
        ),
    ),
    Scene(
        slug="privacy",
        eyebrow="Privacy-First",
        title="De-identification before the cloud.",
        body="Processing happens inside the hospital, so the operational signal moves upstream without moving raw video upstream.",
        renderer="render_privacy",
        voiceover=(
            "Privacy is core to our mission and is built in. PeriSmart processes "
            "all video on an edge device inside your hospital. Faces are always "
            "de-identified. Raw video is never retained. Monitor and TV screens "
            "are automatically obfuscated. It\u2019s designed for HIPAA compliance, "
            "and state biometric privacy laws from day one."
        ),
    ),
    Scene(
        slug="cta",
        eyebrow="Request a Demo",
        title="See what's really happening in your ORs.",
        body="Real-time visibility. Critical analysis. Improved utilization.",
        renderer="render_cta",
        voiceover=(
            "PeriSmart \u2014 real-time visibility, critical analysis, "
            "improved utilization, and privacy-first deployment. "
            "Make your O.R.s more efficient. Request a demo today."
        ),
    ),
]

_FONT_CACHE: dict[tuple[int, str], ImageFont.FreeTypeFont] = {}


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, **kwargs)


def ffprobe_duration(path: Path) -> float:
    result = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def ensure_fonts() -> None:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    if not FONT_VAR.exists():
        urllib.request.urlretrieve(FONT_URL, FONT_VAR)

    targets = {
        400: FONT_REG,
        700: FONT_BOLD,
        800: FONT_XBOLD,
    }
    missing = [weight for weight, path in targets.items() if not path.exists()]
    if not missing:
        return

    for weight, path in targets.items():
        if path.exists():
            continue
        font = TTFont(str(FONT_VAR))
        instance = instantiateVariableFont(font, {"wght": weight}, inplace=False)
        instance.save(str(path))


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    key = (size, weight)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]

    if weight == "xbold":
        path = FONT_XBOLD
    elif weight == "bold":
        path = FONT_BOLD
    else:
        path = FONT_REG

    _FONT_CACHE[key] = ImageFont.truetype(str(path), size)
    return _FONT_CACHE[key]


def ease_out_cubic(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def ease_in_out_quad(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 2 * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 2 / 2


def reveal(t: float, start: float, end: float) -> float:
    if t <= start:
        return 0.0
    if t >= end:
        return 1.0
    return ease_out_cubic((t - start) / (end - start))


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), candidate, font=fnt)[2] <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_lines: int,
    start_size: int,
    min_size: int,
    weight: str,
) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(start_size, min_size - 1, -2):
        fnt = font(size, weight)
        lines = wrap(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(min_size, weight)
    lines = wrap(draw, text, fnt, max_width)
    return fnt, lines[:max_lines]


def line_height(fnt: ImageFont.FreeTypeFont, factor: float = 1.22) -> int:
    ascent, descent = fnt.getmetrics()
    return int((ascent + descent) * factor)


def svg_or_image(path: Path) -> Image.Image:
    if path.suffix.lower() == ".svg":
        data = cairosvg.svg2png(url=str(path))
        return Image.open(io.BytesIO(data)).convert("RGBA")
    return Image.open(path).convert("RGBA")


def contain(im: Image.Image, max_w: int, max_h: int) -> Image.Image:
    copy = im.copy()
    copy.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    return copy


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def paste_round(base: Image.Image, im: Image.Image, box: tuple[int, int], radius: int) -> None:
    base.paste(im, box, rounded_mask(im.size, radius))


def make_bg() -> Image.Image:
    base = Image.new("RGBA", (DESIGN_WIDTH, DESIGN_HEIGHT), BG)

    # Subtle top-edge gradient tint
    grad = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(260):
        a = int(10 * (1 - y / 260))
        gd.line([(0, y), (DESIGN_WIDTH, y)], fill=(30, 107, 235, a))
    base.alpha_composite(grad)

    # Colour glow blobs – more visible than before
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.ellipse((20, -40, 540, 480), fill=(30, 107, 235, 38))
    d.ellipse((1400, -30, 1920, 420), fill=(240, 198, 93, 34))
    d.ellipse((1200, 600, 1960, 1200), fill=(18, 160, 92, 28))
    d.ellipse((1060, 500, 1860, 1220), fill=(30, 107, 235, 18))
    d.ellipse((700, 880, 1200, 1200), fill=(239, 134, 110, 16))
    glow = glow.filter(ImageFilter.GaussianBlur(42))
    base.alpha_composite(glow)

    # Decorative arcs
    lines = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lines)
    d.arc((40, 250, 1900, 1380), 210, 318, fill=(96, 111, 125, 80), width=2)
    d.arc((160, 420, 1840, 1460), 212, 315, fill=(96, 111, 125, 44), width=2)
    base.alpha_composite(lines)
    return base


def shadow(base: Image.Image, box: tuple[int, int, int, int], radius: int = 34, blur_radius: int = 30) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    x1, y1, x2, y2 = box
    ImageDraw.Draw(overlay).rounded_rectangle(
        (x1 + 14, y1 + 20, x2 + 14, y2 + 20),
        radius=radius,
        fill=(15, 33, 55, 36),
    )
    overlay = overlay.filter(ImageFilter.GaussianBlur(blur_radius))
    base.alpha_composite(overlay)


def card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int = 34, fill: str = CARD) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=LINE, width=2)


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, active: bool = True) -> None:
    fnt = font(26, "bold")
    pad_x = 22
    h = 52
    w = draw.textbbox((0, 0), text, font=fnt)[2] + pad_x * 2
    x, y = xy
    fill = ACCENT if active else "#ffffff"
    ink = "#ffffff" if active else INK_SOFT
    draw.rounded_rectangle((x, y, x + w, y + h), radius=26, fill=fill)
    draw.text((x + pad_x, y + 12), text, font=fnt, fill=ink)


def button(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, primary: bool = True) -> None:
    fnt = font(28, "bold")
    x, y = xy
    pad_x = 30
    h = 62
    w = draw.textbbox((0, 0), text, font=fnt)[2] + pad_x * 2
    fill = ACCENT if primary else "#ffffff"
    ink = "#ffffff" if primary else INK
    outline = None if primary else LINE
    draw.rounded_rectangle((x, y, x + w, y + h), radius=31, fill=fill, outline=outline, width=2)
    draw.text((x + pad_x, y + 16), text, font=fnt, fill=ink)


def _alpha_text(
    base: Image.Image,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: str,
    alpha: float,
) -> None:
    """Draw text with variable opacity onto an RGBA *base*."""
    if alpha >= 1.0:
        ImageDraw.Draw(base).text(xy, text, font=fnt, fill=fill)
        return
    if alpha <= 0.0:
        return
    # Render text on a temporary layer and composite at reduced opacity
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(xy, text, font=fnt, fill=fill)
    # Scale the alpha channel
    r, g, b, a = layer.split()
    a = a.point(lambda v: int(v * alpha))
    layer = Image.merge("RGBA", (r, g, b, a))
    base.alpha_composite(layer)


def draw_copy(base: Image.Image, scene: Scene, x: int, y: int, max_w: int, t: float) -> int:
    d = ImageDraw.Draw(base)
    eyebrow_p = reveal(t, 0.0, 0.16)
    title_p = reveal(t, 0.08, 0.30)
    body_p = reveal(t, 0.18, 0.42)

    label(d, (x, int(y - 20 + (1 - eyebrow_p) * 16)), scene.eyebrow, True)
    title_font, title_lines = fit_lines(d, scene.title, max_w, 4, 76, 56, "xbold")
    body_font, body_lines = fit_lines(d, scene.body, max_w, 4, 30, 24, "regular")

    cy = y + 56 - int((1 - title_p) * 20)
    for line in title_lines:
        _alpha_text(base, (x, cy), line, title_font, INK, title_p)
        cy += line_height(title_font, 1.08)

    cy += 14
    for line in body_lines:
        _alpha_text(base, (x, cy), line, body_font, INK_SOFT, body_p)
        cy += line_height(body_font, 1.3)

    return cy


def draw_callout(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int],
    title: str,
    body: str,
    accent: str,
    body_size: int = 25,
) -> int:
    x, y, w = box
    tag_font = font(24, "bold")
    body_font, body_lines = fit_lines(draw, body, w - 44, 3, body_size, 20, "regular")
    tag_w = draw.textbbox((0, 0), title, font=tag_font)[2] + 34
    content_h = 20 + 34 + 18 + len(body_lines) * line_height(body_font, 1.14) + 18
    h = max(92, content_h)

    draw.rounded_rectangle((x, y, x + w, y + h), radius=28, fill="#ffffff", outline=LINE, width=2)
    draw.rounded_rectangle((x + 18, y + 18, x + 18 + tag_w, y + 18 + 36), radius=18, fill=accent)
    draw.text((x + 35, y + 23), title, font=tag_font, fill="#ffffff")

    cy = y + 68
    for line in body_lines:
        draw.text((x + 22, cy), line, font=body_font, fill=INK_SOFT)
        cy += line_height(body_font, 1.14)
    return h


def draw_stat(draw: ImageDraw.ImageDraw, x: int, y: int, label_text: str, value: str, accent: str) -> None:
    draw.rounded_rectangle((x, y, x + 238, y + 126), radius=28, fill="#ffffff", outline=LINE, width=2)
    draw.text((x + 22, y + 22), label_text, font=font(22, "regular"), fill=INK_SOFT)
    value_font, value_lines = fit_lines(draw, value, 190, 2, 28, 21, "bold")
    cy = y + 56
    for line in value_lines:
        draw.text((x + 22, cy), line, font=value_font, fill=accent)
        cy += line_height(value_font, 1.04)


def render_problem(base: Image.Image, t: float, duration: float, assets: dict[str, Image.Image], scene: Scene) -> Image.Image:
    d = ImageDraw.Draw(base)
    draw_copy(base, scene, 120, 72, 620, t / duration)

    # Board illustration – right side
    board = contain(assets["hero_board"], 820, 500)
    panel_x = int(980 - (1 - reveal(t / duration, 0.12, 0.34)) * 72)
    panel_y = 110
    shadow(base, (panel_x, panel_y, panel_x + 810, panel_y + 520))
    card(d, (panel_x, panel_y, panel_x + 810, panel_y + 520))
    paste_round(base, board, (panel_x + 36, panel_y + 28), 28)
    d.rounded_rectangle((panel_x + 410, panel_y - 12, panel_x + 780, panel_y + 50), radius=28, fill=ACCENT_HOVER)
    d.text((panel_x + 446, panel_y + 6), "Accurate OR time", font=font(24, "bold"), fill="#ffffff")

    # Three outcome cards in a horizontal row at the bottom
    questions = [
        ("Reduce Turnovers", "Actual phase data cuts avg turnover time.", ACCENT),
        ("Allocate Block Time", "Real utilization drives smarter scheduling.", GREEN),
        ("Optimize Utilization", "Room efficiency improves with real-time tracking.", CORAL),
    ]
    card_w = 520
    card_gap = 30
    start_x = 120
    card_y = 740
    for idx, (title, body, accent) in enumerate(questions):
        q_p = reveal(t / duration, 0.20 + idx * 0.08, 0.38 + idx * 0.08)
        x = start_x + idx * (card_w + card_gap)
        y = card_y + int((1 - q_p) * 20)
        if q_p > 0.01:
            draw_callout(d, (x, y, card_w), title, body, accent, 22)
    return base


def render_intro(base: Image.Image, t: float, duration: float, assets: dict[str, Image.Image], scene: Scene) -> Image.Image:
    d = ImageDraw.Draw(base)
    p = t / duration

    # Logo with fade-in
    logo_p = reveal(p, 0.0, 0.18)
    logo = contain(assets["logo"], 520, 210)
    if logo_p < 1.0:
        logo_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        logo_layer.paste(logo, ((DESIGN_WIDTH - logo.width) // 2, 160), logo)
        r, g, b, a = logo_layer.split()
        a = a.point(lambda v, lp=logo_p: int(v * lp))
        logo_layer = Image.merge("RGBA", (r, g, b, a))
        base.alpha_composite(logo_layer)
    else:
        base.alpha_composite(logo, ((DESIGN_WIDTH - logo.width) // 2, 160))

    # Title with staggered reveal
    title_p = reveal(p, 0.10, 0.30)
    body_p_val = reveal(p, 0.22, 0.40)
    title_font, title_lines = fit_lines(d, scene.title, 900, 2, 52, 40, "xbold")
    body_font, body_lines = fit_lines(d, scene.body, 860, 2, 30, 24, "regular")
    cy = 326 - int((1 - title_p) * 16)
    for line in title_lines:
        bbox = d.textbbox((0, 0), line, font=title_font)
        _alpha_text(base, ((DESIGN_WIDTH - bbox[2]) // 2, cy), line, title_font, INK, title_p)
        cy += line_height(title_font, 1.08)
    cy += 12
    for line in body_lines:
        bbox = d.textbbox((0, 0), line, font=body_font)
        _alpha_text(base, ((DESIGN_WIDTH - bbox[2]) // 2, cy), line, body_font, INK_SOFT, body_p_val)
        cy += line_height(body_font, 1.2)

    board = contain(assets["hero_board"], 740, 340)
    board_p = reveal(p, 0.20, 0.54)
    offset = int((1 - board_p) * 72)
    shadow(base, (590, 480 - offset, 1330, 780 - offset))
    card(d, (590, 480 - offset, 1330, 780 - offset))
    paste_round(base, board, (620, 500 - offset), 28)

    # Data-flow strip: Actual Times → Better Analysis → Improved Utilization
    flow_p = reveal(p, 0.40, 0.65)
    if flow_p > 0.01:
        steps = [
            ("Actual Times", ACCENT),
            ("Better Analysis", GREEN),
            ("Improved Utilization", NAVY),
        ]
        box_w = 300
        box_gap = 48
        total_w = len(steps) * box_w + (len(steps) - 1) * box_gap
        fx = (DESIGN_WIDTH - total_w) // 2
        fy = 850 + int((1 - flow_p) * 16)
        for idx, (step_text, accent) in enumerate(steps):
            sx = fx + idx * (box_w + box_gap)
            d.rounded_rectangle((sx, fy, sx + box_w, fy + 56), radius=28, fill=accent)
            sf = font(24, "bold")
            tw = d.textbbox((0, 0), step_text, font=sf)[2]
            d.text((sx + (box_w - tw) // 2, fy + 14), step_text, font=sf, fill="#ffffff")
            if idx < len(steps) - 1:
                ax = sx + box_w + 6
                d.line((ax, fy + 28, ax + box_gap - 16, fy + 28), fill=accent, width=4)
                d.polygon([
                    (ax + box_gap - 12, fy + 28),
                    (ax + box_gap - 22, fy + 18),
                    (ax + box_gap - 22, fy + 38),
                ], fill=accent)
    return base


def render_or_board(base: Image.Image, t: float, duration: float, assets: dict[str, Image.Image], scene: Scene) -> Image.Image:
    d = ImageDraw.Draw(base)
    draw_copy(base, scene, 110, 86, 640, t / duration)

    board = contain(assets["hero_board"], 980, 620)
    bx, by = 770, 210
    shadow(base, (bx, by, bx + 1000, by + 640))
    card(d, (bx, by, bx + 1000, by + 640))
    paste_round(base, board, (bx + 20, by + 18), 28)

    now_x = int(1305 + math.sin(t * 1.4) * 4)
    d.line((now_x, by + 86, now_x, by + 560), fill=NAVY, width=6)
    d.rounded_rectangle((now_x - 46, by + 42, now_x + 46, by + 88), radius=20, fill=ACCENT)
    d.text((now_x - 28, by + 54), "NOW", font=font(22, "bold"), fill="#ffffff")

    info = [
        (780, 860, 268, "Live position", "Current timeline anchor", ACCENT),
        (1076, 860, 250, "On Track", "Green rooms stay visible", GREEN),
        (1354, 860, 300, "At Risk", "44m over projected plan", CORAL),
    ]
    for idx, (x, y, w, title, body, accent) in enumerate(info):
        p = reveal(t / duration, 0.20 + idx * 0.07, 0.36 + idx * 0.07)
        draw_callout(d, (x, y - int((1 - p) * 16), w), title, body, accent, 22)
    return base


def render_case_detail(base: Image.Image, t: float, duration: float, assets: dict[str, Image.Image], scene: Scene) -> Image.Image:
    d = ImageDraw.Draw(base)
    draw_copy(base, scene, 118, 118, 680, t / duration)

    case = contain(assets["case_detail"], 690, 560)
    cx, cy = 980, 160
    shadow(base, (cx, cy, cx + 720, cy + 600))
    card(d, (cx, cy, cx + 720, cy + 600))
    paste_round(base, case, (cx + 18, cy + 20), 28)

    stats = [
        ("Predicted End", "8:45 AM", ACCENT),
        ("Variance", "40 min ahead", GREEN),
        ("Milestones", "auto-detected", CORAL),
    ]
    for idx, (label_text, value, accent) in enumerate(stats):
        p = reveal(t / duration, 0.22 + idx * 0.07, 0.40 + idx * 0.07)
        draw_stat(d, 124 + idx * 255, 760 - int((1 - p) * 16), label_text, value, accent)
    return base


def render_analytics(base: Image.Image, t: float, duration: float, assets: dict[str, Image.Image], scene: Scene) -> Image.Image:
    d = ImageDraw.Draw(base)
    label(d, (108, 66), scene.eyebrow, True)
    title_font, title_lines = fit_lines(d, scene.title, 520, 4, 66, 50, "xbold")
    body_font, body_lines = fit_lines(d, scene.body, 520, 3, 28, 22, "regular")
    cy = 148
    for line in title_lines:
        d.text((108, cy), line, font=title_font, fill=INK)
        cy += line_height(title_font, 1.06)
    cy += 12
    for line in body_lines:
        d.text((108, cy), line, font=body_font, fill=INK_SOFT)
        cy += line_height(body_font, 1.18)

    main = contain(assets["turnover"], 640, 400)
    shadow(base, (108, 440, 786, 860))
    card(d, (108, 440, 786, 860))
    paste_round(base, main, (128, 460), 28)

    mini = [("block", 860), ("room", 1220)]
    for key, x in mini:
        shadow(base, (x, 420, x + 310, 630))
        card(d, (x, 420, x + 310, 630))
        paste_round(base, contain(assets[key], 270, 150), (x + 20, 440), 24)

    panels = [
        ("Turnover trend", "Daily vs target"),
        ("Clean / Idle / Setup", "Phase breakdown"),
        ("CSV export", "Board reporting ready"),
    ]
    for idx, (title, body) in enumerate(panels):
        x = 860 + idx * 320
        d.rounded_rectangle((x, 720, x + 280, 840), radius=28, fill="#ffffff", outline=LINE, width=2)
        t_font = font(23, "bold")
        b_font = font(21, "regular")
        d.text((x + 22, 744), title, font=t_font, fill=INK)
        d.text((x + 22, 744 + line_height(t_font, 1.08) + 6), body, font=b_font, fill=ACCENT)
    return base


def render_privacy(base: Image.Image, t: float, duration: float, assets: dict[str, Image.Image], scene: Scene) -> Image.Image:
    d = ImageDraw.Draw(base)
    draw_copy(base, scene, 110, 96, 680, t / duration)

    privacy = contain(assets["privacy"], 710, 540)
    px, py = 1000, 150
    shadow(base, (px, py, px + 720, py + 560))
    card(d, (px, py, px + 720, py + 560))
    paste_round(base, privacy, (px + 18, py + 18), 28)

    stages = [("Camera", ACCENT), ("Edge Device", GREEN), ("Cloud Insights", NAVY)]
    box_w = 240
    box_gap = 36
    start_x = 120
    for idx, (name, accent) in enumerate(stages):
        x = start_x + idx * (box_w + box_gap)
        d.rounded_rectangle((x, 720, x + box_w, 804), radius=26, fill="#ffffff", outline=LINE, width=2)
        lbl_font = font(26, "bold")
        tw = d.textbbox((0, 0), name, font=lbl_font)[2]
        d.text((x + (box_w - tw) // 2, 742), name, font=lbl_font, fill=accent)
        if idx < len(stages) - 1:
            ax = x + box_w
            d.line((ax + 4, 762, ax + box_gap - 10, 762), fill=accent, width=5)
            d.polygon([(ax + box_gap - 6, 762), (ax + box_gap - 18, 752), (ax + box_gap - 18, 772)], fill=accent)

    d.text((178, 880), "Raw video is never retained", font=font(34, "bold"), fill=ACCENT)
    return base


def render_cta(base: Image.Image, t: float, duration: float, assets: dict[str, Image.Image], scene: Scene) -> Image.Image:
    d = ImageDraw.Draw(base)
    p = t / duration

    # Logo fade-in
    logo_p = reveal(p, 0.0, 0.16)
    logo = contain(assets["logo"], 540, 220)
    if logo_p < 1.0:
        logo_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        logo_layer.paste(logo, ((DESIGN_WIDTH - logo.width) // 2, 90), logo)
        r, g, b, a = logo_layer.split()
        a = a.point(lambda v, lp=logo_p: int(v * lp))
        logo_layer = Image.merge("RGBA", (r, g, b, a))
        base.alpha_composite(logo_layer)
    else:
        base.alpha_composite(logo, ((DESIGN_WIDTH - logo.width) // 2, 90))

    title_p = reveal(p, 0.08, 0.26)
    body_p_val = reveal(p, 0.16, 0.34)

    title_font, title_lines = fit_lines(d, scene.title, 1040, 2, 68, 52, "xbold")
    body_font, body_lines = fit_lines(d, scene.body, 1000, 2, 30, 24, "regular")
    cy = 284 - int((1 - title_p) * 14)
    for line in title_lines:
        bbox = d.textbbox((0, 0), line, font=title_font)
        _alpha_text(base, ((DESIGN_WIDTH - bbox[2]) // 2, cy), line, title_font, NAVY, title_p)
        cy += line_height(title_font, 1.08)
    cy += 18
    for line in body_lines:
        bbox = d.textbbox((0, 0), line, font=body_font)
        _alpha_text(base, ((DESIGN_WIDTH - bbox[2]) // 2, cy), line, body_font, INK_SOFT, body_p_val)
        cy += line_height(body_font, 1.2)

    # Schedule illustration – centered, larger
    hero = contain(assets["schedule"], 780, 280)
    hero_p = reveal(p, 0.22, 0.48)
    hx = (DESIGN_WIDTH - hero.width) // 2 - 20
    hy = int(560 + (1 - hero_p) * 20)
    card_w = hero.width + 60
    card_h = hero.height + 40
    shadow(base, (hx - 10, hy - 10, hx + card_w - 10, hy + card_h - 10))
    card(d, (hx - 10, hy - 10, hx + card_w - 10, hy + card_h - 10))
    paste_round(base, hero, (hx + 20, hy + 10), 22)

    url_p = reveal(p, 0.38, 0.54)
    url_font = font(30, "bold")
    url_text = "peri-smart.com"
    url_w = d.textbbox((0, 0), url_text, font=url_font)[2]
    _alpha_text(base, ((DESIGN_WIDTH - url_w) // 2, hy + card_h + 30), url_text, url_font, ACCENT, url_p)
    return base


def load_assets() -> dict[str, Image.Image]:
    return {
        "logo": svg_or_image(ROOT / "assets" / "logo" / "perismart-logo.png"),
        "hero_board": svg_or_image(ROOT / "assets" / "illustrations" / "hero-or-board-illustration.svg"),
        "case_detail": svg_or_image(ROOT / "assets" / "illustrations" / "case-detail-illustration.svg"),
        "turnover": svg_or_image(ROOT / "assets" / "illustrations" / "turnover-analytics-illustration.svg"),
        "block": svg_or_image(ROOT / "assets" / "illustrations" / "block-utilization-illustration.svg"),
        "room": svg_or_image(ROOT / "assets" / "illustrations" / "room-utilization-illustration.svg"),
        "privacy": svg_or_image(ROOT / "assets" / "illustrations" / "privacy-illustration.png"),
        "schedule": svg_or_image(ROOT / "assets" / "illustrations" / "schedule-context-integration.png"),
    }


def _load_env() -> None:
    """Read .env from repository root into os.environ (no dependencies)."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


ELEVENLABS_VOICE_ID = "pFZP5JQG7iQjIQuC4Bku"  # Lily – warm British female
ELEVENLABS_MODEL = "eleven_multilingual_v2"


def _elevenlabs_tts(text: str, out_path: Path) -> None:
    """Call ElevenLabs TTS and write the MP3 result to *out_path*."""
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not set — add it to .env")
    payload = json.dumps({
        "text": text,
        "model_id": ELEVENLABS_MODEL,
        "voice_settings": {
            "stability": 0.65,
            "similarity_boost": 0.75,
            "style": 0.35,
            "use_speaker_boost": True,
        },
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
        data=payload,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
    )
    with urllib.request.urlopen(req) as resp:
        out_path.write_bytes(resp.read())


def synthesize_scenes(audio_dir: Path) -> list[float]:
    _load_env()

    audio_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = audio_dir / "raw"
    cooked_dir = audio_dir / "cooked"
    raw_dir.mkdir(parents=True, exist_ok=True)
    cooked_dir.mkdir(parents=True, exist_ok=True)

    durations: list[float] = []

    for idx, scene in enumerate(SCENES, start=1):
        raw_out = raw_dir / f"{idx:02d}-{scene.slug}.mp3"
        cooked_out = cooked_dir / f"{idx:02d}-{scene.slug}.wav"
        print(f"  TTS [{idx}/{len(SCENES)}] {scene.slug} ...")
        _elevenlabs_tts(scene.voiceover, raw_out)
        # Light post-processing: normalize loudness, stereo, 48 kHz
        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(raw_out),
                "-af",
                (
                    "highpass=f=55,"
                    "loudnorm=I=-16:TP=-1.5:LRA=11,"
                    "volume=1.05,"
                    "pan=stereo|c0=c0|c1=c0,"
                    "aresample=48000"
                ),
                "-ar",
                "48000",
                str(cooked_out),
            ]
        )
        durations.append(ffprobe_duration(cooked_out))
    return durations


def concat_audio(audio_dir: Path, output: Path) -> None:
    cooked_dir = audio_dir / "cooked"
    listing = audio_dir / "concat.txt"
    with listing.open("w", encoding="utf-8") as handle:
        for idx, scene in enumerate(SCENES, start=1):
            handle.write(f"file '{cooked_dir / f'{idx:02d}-{scene.slug}.wav'}'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(output)])


def _apply_fade(frame: Image.Image, alpha: float) -> Image.Image:
    """Blend *frame* toward white by *alpha* (1.0 = fully visible)."""
    if alpha >= 1.0:
        return frame
    white = Image.new("RGB", frame.size, (255, 255, 255))
    return Image.blend(white, frame, ease_in_out_quad(max(0.0, alpha)))


def _draw_progress_bar(frame: Image.Image, progress: float) -> Image.Image:
    """Draw a thin accent progress bar at the very bottom of *frame*."""
    d = ImageDraw.Draw(frame)
    bar_w = int(frame.width * max(0.0, min(1.0, progress)))
    if bar_w > 0:
        d.rectangle((0, frame.height - PROGRESS_HEIGHT, bar_w, frame.height), fill=ACCENT)
    return frame


def render_video(assets: dict[str, Image.Image], durations: list[float], video_path: Path) -> None:
    ffmpeg = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{OUTPUT_WIDTH}x{OUTPUT_HEIGHT}",
            "-r",
            str(FPS),
            "-i",
            "-",
            "-an",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "18",
            "-preset",
            "medium",
            str(video_path),
        ],
        stdin=subprocess.PIPE,
    )
    assert ffmpeg.stdin is not None

    total_frames = sum(max(1, math.ceil(d * FPS)) for d in durations)
    global_frame = 0

    for scene_idx, (scene, duration) in enumerate(zip(SCENES, durations)):
        frame_count = max(1, math.ceil(duration * FPS))
        renderer = globals()[scene.renderer]
        is_first = scene_idx == 0
        is_last = scene_idx == len(SCENES) - 1

        for frame_idx in range(frame_count):
            t = frame_idx / FPS
            canvas = make_bg()
            frame = renderer(canvas, t, duration, assets, scene).convert("RGB")
            if frame.size != (OUTPUT_WIDTH, OUTPUT_HEIGHT):
                frame = frame.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT), Image.Resampling.LANCZOS)

            # Fade-through-white transitions between scenes
            if not is_first and frame_idx < FADE_FRAMES:
                frame = _apply_fade(frame, frame_idx / FADE_FRAMES)
            elif not is_last and frame_idx >= frame_count - FADE_FRAMES:
                remaining = frame_count - 1 - frame_idx
                frame = _apply_fade(frame, remaining / FADE_FRAMES)
            # Extra: fade in from white at very start of video
            elif is_first and frame_idx < FADE_FRAMES:
                frame = _apply_fade(frame, frame_idx / FADE_FRAMES)
            # Extra: fade out to white at very end of video
            elif is_last and frame_idx >= frame_count - FADE_FRAMES:
                remaining = frame_count - 1 - frame_idx
                frame = _apply_fade(frame, remaining / FADE_FRAMES)

            # Progress bar
            _draw_progress_bar(frame, global_frame / max(1, total_frames - 1))
            global_frame += 1

            ffmpeg.stdin.write(frame.tobytes())

    ffmpeg.stdin.close()
    if ffmpeg.wait() != 0:
        raise RuntimeError("ffmpeg video render failed")


def mux(video_path: Path, audio_path: Path, output: Path) -> None:
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(audio_path),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "256k",
            "-shortest",
            str(output),
        ]
    )


def poster(video_path: Path, output: Path) -> None:
    run(["ffmpeg", "-y", "-i", str(video_path), "-ss", "00:00:18", "-frames:v", "1", str(output)])


def main() -> None:
    ensure_fonts()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    audio_dir = TMP_DIR / "audio"
    silent_video = TMP_DIR / "perismart-homepage-explainer-silent.mp4"
    voiceover = TMP_DIR / "perismart-homepage-explainer-voiceover.wav"
    final = OUT_DIR / "perismart-homepage-explainer.mp4"
    poster_path = OUT_DIR / "perismart-homepage-explainer-poster.jpg"

    assets = load_assets()
    durations = synthesize_scenes(audio_dir)
    concat_audio(audio_dir, voiceover)
    render_video(assets, durations, silent_video)
    mux(silent_video, voiceover, final)
    poster(final, poster_path)

    print(f"Rendered {final}")
    print(f"Poster {poster_path}")
    print(f"Runtime {sum(durations):.2f}s")


if __name__ == "__main__":
    main()
