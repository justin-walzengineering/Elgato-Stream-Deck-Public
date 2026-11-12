"""Generate original Stream Deck button icons for the Eplan profile.

Usage (from the repo root):  python tools/make_icons.py
Needs:  pip install pillow

Every icon is drawn from scratch with simple shapes (no third-party artwork).
Output: icons/<id>.png (144x144) and _local/icon_preview.png (contact sheet, git-ignored).
Edit the BUTTONS list below to rename a button or change its glyph/colour.
"""
import os
from PIL import Image, ImageDraw, ImageFont

S = 4            # supersampling factor
N = 144 * S      # canvas size while drawing
BG = (24, 28, 36)
WHITE = (240, 244, 250)
DIM = (96, 106, 124)

# category accent colours
GRID, ORDER, FORM, LIB, TEXT, FMT, UPD, DESIGN = (
    (79, 156, 255), (255, 170, 64), (176, 132, 255), (72, 207, 140),
    (255, 107, 129), (255, 214, 79), (64, 214, 214), (150, 170, 200))

FONT_PATHS = [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def font(size):
    for p in FONT_PATHS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size * S)
    return ImageFont.load_default()


def line_w(d, pts, col, w=7):
    d.line([(x * S, y * S) for x, y in pts], fill=col, width=w * S, joint="curve")


def rect(d, box, col, w=7, fill=None, r=8):
    x0, y0, x1, y1 = [v * S for v in box]
    d.rounded_rectangle([x0, y0, x1, y1], radius=r * S, outline=col, width=w * S, fill=fill)


def dot(d, cx, cy, rad, col):
    d.ellipse([(cx - rad) * S, (cy - rad) * S, (cx + rad) * S, (cy + rad) * S], fill=col)


def text(d, xy, s, col, size, anchor="mm"):
    d.text((xy[0] * S, xy[1] * S), s, fill=col, font=font(size), anchor=anchor)


# ---------- glyphs (drawn inside roughly x 22..122, y 18..92) ----------
def g_grid(d, a, letter):
    for t in (46, 72):
        line_w(d, [(t, 22), (t, 90)], a, 6)
        line_w(d, [(24, t - 8), (96, t - 8)], a, 6)
    text(d, (110, 70), letter, WHITE, 40)


def g_front(d, a, _):
    rect(d, (30, 24, 86, 80), DIM, 6)
    rect(d, (52, 40, 110, 94), a, 7, fill=a)


def g_back(d, a, _):
    rect(d, (52, 40, 110, 94), DIM, 6)
    rect(d, (30, 24, 86, 80), a, 7, fill=a)


def g_form(d, a, mode):
    rect(d, (34, 20, 98, 92), WHITE, 6)
    line_w(d, [(46, 40), (86, 40)], a, 6)
    line_w(d, [(46, 56), (86, 56)], a, 6)
    line_w(d, [(46, 72), (70, 72)], a, 6)
    badge(d, mode, a)


def g_library(d, a, mode):
    for i, y in enumerate((26, 48, 70)):
        rect(d, (28, y, 100, y + 16), WHITE if i == 0 else DIM, 5, r=4)
    badge(d, mode, a)


def g_symbol(d, a, mode):
    # a coil-style electrical symbol: lead, box, lead
    line_w(d, [(66, 16), (66, 32)], WHITE, 6)
    rect(d, (46, 32, 86, 76), WHITE, 6, r=4)
    line_w(d, [(66, 76), (66, 92)], WHITE, 6)
    badge(d, mode, a)


def badge(d, mode, a):
    """+ / x badge in the lower right to show open vs close."""
    dot(d, 108, 76, 17, a)
    if mode == "open":
        line_w(d, [(108, 67), (108, 85)], BG, 5)
        line_w(d, [(99, 76), (117, 76)], BG, 5)
    else:
        line_w(d, [(100, 68), (116, 84)], BG, 5)
        line_w(d, [(116, 68), (100, 84)], BG, 5)


def g_text(d, a, pos):
    rect(d, (28, 20, 116, 92), DIM, 5)
    col, row = pos
    for r in range(3):
        for c in range(3):
            x, y = 44 + c * 28, 34 + r * 24
            if (c, r) == (col, row):
                dot(d, x, y, 10, a)
            else:
                dot(d, x, y, 4, WHITE)


def g_copyfmt(d, a, mode):
    text(d, (62, 56), "Aa", WHITE, 52)
    # arrow: out of the text (copy) or into it (paste)
    if mode == "copy":
        line_w(d, [(112, 78), (112, 34)], a, 7)
        line_w(d, [(98, 48), (112, 32), (126, 48)], a, 7)
    else:
        line_w(d, [(112, 32), (112, 78)], a, 7)
        line_w(d, [(98, 64), (112, 80), (126, 64)], a, 7)


def g_align(d, a, _):
    for x in (30, 66, 102):
        for y in (26, 58, 90):
            dot(d, x, y, 4, DIM)
    rect(d, (30, 26, 66, 58), a, 7, fill=None, r=3)
    dot(d, 30, 26, 8, a)


def g_update_reports(d, a, _):
    d.arc([22 * S, 18 * S, 98 * S, 94 * S], 40, 330, fill=a, width=7 * S)
    line_w(d, [(88, 24), (92, 44), (74, 42)], a, 7)
    for y in (42, 56, 70):
        line_w(d, [(44, y), (76, y)], WHITE, 5)


def g_update_conn(d, a, _):
    d.arc([22 * S, 18 * S, 98 * S, 94 * S], 40, 330, fill=a, width=7 * S)
    line_w(d, [(88, 24), (92, 44), (74, 42)], a, 7)
    line_w(d, [(40, 56), (80, 56)], WHITE, 6)
    dot(d, 40, 56, 7, WHITE)
    dot(d, 80, 56, 7, WHITE)


def g_tabs(d, a, _):
    rect(d, (22, 34, 100, 90), DIM, 6, r=6)
    rect(d, (22, 20, 62, 44), a, 6, fill=a, r=6)
    rect(d, (66, 24, 104, 44), WHITE, 5, r=6)


def g_design(d, a, _):
    # drafting set-square
    d.polygon([(30 * S, 22 * S), (30 * S, 92 * S), (104 * S, 92 * S)], outline=a, width=7 * S)
    d.polygon([(46 * S, 54 * S), (46 * S, 76 * S), (68 * S, 76 * S)], outline=WHITE, width=5 * S)


# id, caption, accent, glyph, argument
BUTTONS = [
    ("grid-a", "Grid A", GRID, g_grid, "A"),
    ("grid-b", "Grid B", GRID, g_grid, "B"),
    ("grid-c", "Grid C", GRID, g_grid, "C"),
    ("grid-d", "Grid D", GRID, g_grid, "D"),
    ("to-front", "To Front", ORDER, g_front, None),
    ("to-back", "To Back", ORDER, g_back, None),
    ("form-open", "Open Form", FORM, g_form, "open"),
    ("form-close", "Close Form", FORM, g_form, "close"),
    ("library-open", "Open Library", LIB, g_library, "open"),
    ("library-close", "Close Library", LIB, g_library, "close"),
    ("symbol-open", "Open Symbol", LIB, g_symbol, "open"),
    ("symbol-close", "Close Symbol", LIB, g_symbol, "close"),
    ("align-grid", "Align to Grid", GRID, g_align, None),
    ("text-tl", "Top Left", TEXT, g_text, (0, 0)),
    ("text-t", "Top", TEXT, g_text, (1, 0)),
    ("text-tr", "Top Right", TEXT, g_text, (2, 0)),
    ("text-l", "Left", TEXT, g_text, (0, 1)),
    ("text-c", "Center", TEXT, g_text, (1, 1)),
    ("text-r", "Right", TEXT, g_text, (2, 1)),
    ("text-bl", "Bottom Left", TEXT, g_text, (0, 2)),
    ("text-b", "Bottom", TEXT, g_text, (1, 2)),
    ("text-br", "Bottom Right", TEXT, g_text, (2, 2)),
    ("copy-format", "Copy Format", FMT, g_copyfmt, "copy"),
    ("paste-format", "Paste Format", FMT, g_copyfmt, "paste"),
    ("update-reports", "Update Reports", UPD, g_update_reports, None),
    ("update-connections", "Update Connections", UPD, g_update_conn, None),
    ("switch-tabs", "Switch Tabs", DESIGN, g_tabs, None),
    ("design", "Design", DESIGN, g_design, None),
]


def make(bid, caption, accent, glyph, arg):
    im = Image.new("RGB", (N, N), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([4 * S, 4 * S, N - 4 * S, N - 4 * S], radius=18 * S, outline=accent, width=3 * S)
    glyph(d, accent, arg)
    # caption (split long captions on a space)
    words = caption.split(" ")
    lines = [caption] if len(caption) <= 11 else [" ".join(words[:-1]), words[-1]]
    size = 19 if len(lines) == 1 else 16
    y0 = 119 if len(lines) == 1 else 108
    for i, ln in enumerate(lines):
        text(d, (72, y0 + i * 17), ln, WHITE, size)
    return im.resize((144, 144), Image.LANCZOS)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "icons")
    os.makedirs(out, exist_ok=True)
    os.makedirs(os.path.join(root, "_local"), exist_ok=True)
    cols = 7
    rows = (len(BUTTONS) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 152 + 8, rows * 152 + 8), (60, 60, 60))
    for i, b in enumerate(BUTTONS):
        im = make(*b)
        im.save(os.path.join(out, b[0] + ".png"))
        sheet.paste(im, (8 + (i % cols) * 152, 8 + (i // cols) * 152))
    sheet.save(os.path.join(root, "_local", "icon_preview.png"))
    print("wrote", len(BUTTONS), "icons to", out)


if __name__ == "__main__":
    main()
