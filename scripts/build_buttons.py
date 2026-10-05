"""Generate the README link buttons as self-contained SVGs (icon embedded as base64)."""
import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"

WIDTH, HEIGHT = 280, 52
ICON_SIZE, ICON_X = 26, 22
FONT_FAMILY = "Segoe UI, -apple-system, Helvetica, Arial, sans-serif"

BUTTONS = [
    ("Portfolio.webp", "Portfolio Site", "button-portfolio.svg", "#1f6feb"),
    ("YouTube.webp", "YouTube Channel", "button-youtube.svg", "#24292f"),
    ("LinkedIn.webp", "LinkedIn", "button-linkedin.svg", "#24292f"),
    ("HaloDialogueArchive.webp", "Halo Dialogue Archive", "button-halo.svg", "#24292f"),
]


def icon_data(path):
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    im.thumbnail((96, 96), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", lossless=True)
    return base64.b64encode(buf.getvalue()).decode(), im.size


def build(icon, label, out, bg):
    b64, (iw, ih) = icon_data(IMAGES / icon)
    scale = ICON_SIZE / max(iw, ih)
    sw, sh = iw * scale, ih * scale
    ix, iy = ICON_X + (ICON_SIZE - sw) / 2, (HEIGHT - sh) / 2
    text_cx = (ICON_X + ICON_SIZE + 12 + WIDTH - 18) / 2
    href = f"data:image/webp;base64,{b64}"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="10" fill="{bg}" stroke="#ffffff" stroke-opacity="0.15"/>
  <image x="{ix:.1f}" y="{iy:.1f}" width="{sw:.1f}" height="{sh:.1f}" href="{href}" xlink:href="{href}"/>
  <text x="{text_cx:.1f}" y="{HEIGHT / 2}" dominant-baseline="central" text-anchor="middle" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="17" font-weight="600">{label}</text>
</svg>
"""
    (IMAGES / out).write_text(svg, encoding="utf-8", newline="\n")
    print(f"{out}: {len(svg)} bytes")


if __name__ == "__main__":
    for b in BUTTONS:
        build(*b)
