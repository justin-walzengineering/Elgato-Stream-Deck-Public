"""Draw the Eplan shortcut cheat sheet image from scratch.

Usage (from the repo root):  python tools/make_cheatsheet.py
Needs:  pip install pillow

Output: docs/images/eplan-shortcut-cheat-sheet.png
Edit the CARDS list to change a key, a description or a group, then run it again.
The same keys are explained in docs/eplan-shortcut-cheat-sheet.md.
All artwork is original (simple shapes and text only).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = 2400
MARGIN, GAP = 60, 30
COLS = 4
BG = (20, 24, 32)
CARD = (30, 36, 48)
CHIP = (44, 52, 68)
WHITE = (240, 244, 250)
SOFT = (170, 180, 198)
STAR = (255, 214, 79)

BLUE, GREEN, PURPLE, ORANGE, TEAL, PINK, YELLOW = (
    (79, 156, 255), (72, 207, 140), (176, 132, 255), (255, 170, 64),
    (64, 214, 214), (255, 107, 129), (255, 214, 79))

# Each card: (title, accent colour, rows). A row is (keys, description, star).
# `keys` is a list: several entries mean "either key".
CARDS = [
    # ---- column 1
    [("Draw", BLUE, [
        (["E"], "Ellipse", 0), (["K"], "Circle", 0), (["L"], "Polyline", 0),
        (["R"], "Rectangle", 0), (["T"], "Text", 0), (["Ctrl+F2"], "Line", 0),
        (["Ctrl+G"], "Arc", 0), (["Ctrl+T"], "Path function text", 0)]),
     ("Symbols and macros", PURPLE, [
        (["Insert"], "Insert symbol", 0), (["Alt+Insert"], "Insert device", 0),
        (["M", "Ctrl+Insert"], "Insert macro", 0),
        (["B", "Ctrl+F5"], "Create window macro", 0),
        (["Ctrl+F10"], "Create page macro", 0), (["Ctrl+K"], "Generate macros", 0)]),
     ("Everyday", ORANGE, [
        (["Ctrl+C"], "Copy", 0), (["Ctrl+X"], "Cut", 0), (["Ctrl+V"], "Paste", 0),
        (["Ctrl+Z"], "Undo", 0), (["Ctrl+Y"], "Redo", 0),
        (["Ctrl+A"], "Select all", 0), (["Esc"], "Cancel the action", 0)])],
    # ---- column 2
    [("Connections and schematic symbols", GREEN, [
        (["F3"], "Angle (down, right)", 0), (["F4"], "Angle (down, left)", 0),
        (["F6"], "Angle (up, left)", 0), (["F7"], "T-node (down)", 0),
        (["F8"], "T-node (up)", 0), (["F9"], "T-node (right)", 0),
        (["F10"], "T-node (left)", 0), (["Shift+F3"], "Device connection point", 0),
        (["Shift+F4"], "Interruption point", 0), (["Shift+F5"], "Cable definition", 0),
        (["Shift+F6"], "Shield", 0), (["Shift+F7"], "Connection def. point", 0),
        (["Shift+F8"], "Jumper", 0), (["Shift+F11"], "Black box", 0),
        (["Ctrl+Shift+U"], "Interrupt connections", 0)]),
     ("Panel layout and 3D views", TEAL, [
        (["A"], "Change handle", 0), (["H"], "Rail: use length", 0),
        (["J"], "Rail: centered", 0), (["Ctrl+W"], "Placement options", 0),
        (["Ctrl+Shift+R"], "Modify rotation angle", 0),
        (["Ctrl+Shift+M"], "2D layout navigator", 0),
        (["Ctrl+Alt+T/F/R"], "Top, front, right", 0),
        (["Ctrl+Alt+1 to 4"], "Isometric views", 0)])],
    # ---- column 3
    [("Move and edit", BLUE, [
        (["Space"], "Selection window", 0), (["V"], "Move", 0), (["D"], "Duplicate", 0), (["G"], "Group", 0),
        (["Ctrl+R"], "Rotate", 0), (["O"], "Move base point", 0),
        (["Ctrl+B"], "Move property text", 0), (["Ctrl+D"], "Edit properties", 0),
        (["Alt+Delete"], "Delete placement", 0)]),
     ("View, snap and position", YELLOW, [
        (["Tab"], "Jump to element points", 0),
        (["Z"], "Zoom window", 1), (["Alt+3"], "Show the whole page", 1),
        (["Q"], "Snap on / off", 1),
        (["I"], "Show insertion points", 0),
        (["U"], "Show / hide invisible", 1),
        (["F5"], "Redraw the view", 1), (["Ctrl+Shift+F6"], "Grid on / off", 1),
        (["S"], "Set increment", 0), (["P"], "Coordinate input", 0),
        (["Shift+R"], "Relative coordinates", 0)])],
    # ---- column 4
    [("Pages and navigation", PINK, [
        (["PgUp/PgDn"], "Previous / next page", 0), (["Ctrl+M"], "Select a page", 0),
        (["F12"], "Page navigator", 0), (["Ctrl+N"], "New page", 0),
        (["Ctrl+J"], "Go to graphic", 0), (["F"], "Go to counterpart", 1),
        (["Alt+PgUp/PgDn"], "Cross-reference jump", 0)]),
     ("Search and check", PURPLE, [
        (["Ctrl+F"], "Find", 0), (["Ctrl+Shift+F"], "Next entry", 0),
        (["Ctrl+Shift+V"], "Previous entry", 0), (["Ctrl+I"], "Add to search results", 0),
        (["Ctrl+S"], "Synchronize selection", 0), (["Ctrl+Shift+P"], "Check project", 1),
        (["Ctrl+Shift+E"], "Message management", 0)]),
     ("Reports, output and PLC", ORANGE, [
        (["Ctrl+E"], "Generate reports", 0), (["Ctrl+,"], "Update reports", 1),
        (["Ctrl+Shift+,"], "Generate project reports", 0), (["Ctrl+P"], "Print project", 0),
        (["Ctrl+O"], "Address PLC", 0), (["Ctrl+L"], "PLC connection points", 0)])],
]


def font(name, size):
    for p in (rf"C:\Windows\Fonts\{name}", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


F_TITLE = font("segoeuib.ttf", 76)
F_SUB = font("segoeui.ttf", 32)
F_HEAD = font("segoeuib.ttf", 30)
F_KEY = font("segoeuib.ttf", 24)
F_DESC = font("segoeui.ttf", 27)
F_SMALL = font("segoeui.ttf", 24)

ROW_H, HEAD_H, PAD, CARD_GAP = 46, 64, 22, 26
COL_W = (W - 2 * MARGIN - (COLS - 1) * GAP) // COLS
TOP = 205


def star(d, cx, cy, r):
    pts = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(a), cy - rr * math.sin(a)))
    d.polygon(pts, fill=STAR)


def tw(d, s, f):
    return d.textlength(s, font=f)


def chip_row_width(d, keys):
    return sum(tw(d, k, F_KEY) + 24 for k in keys) + 14 * (len(keys) - 1)


def card_height(rows):
    return HEAD_H + PAD // 2 + len(rows) * ROW_H + PAD


def main():
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    col_h = [sum(card_height(c[2]) for c in col) + CARD_GAP * (len(col) - 1) for col in CARDS]
    H = TOP + max(col_h) + 150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.text((MARGIN, 40), "Eplan Electric P8 Shortcut Cheat Sheet", font=F_TITLE, fill=WHITE)
    d.text((MARGIN, 140), "Default keys in Eplan 2026, grouped by what you are doing.", font=F_SUB, fill=SOFT)
    sx = W - MARGIN
    legend = "= a great Stream Deck button"
    d.text((sx, 152), legend, font=F_SUB, fill=SOFT, anchor="rm")
    star(d, sx - tw(d, legend, F_SUB) - 30, 152, 15)

    for ci, col in enumerate(CARDS):
        x0 = MARGIN + ci * (COL_W + GAP)
        y = TOP
        for title, acc, rows in col:
            h = card_height(rows)
            d.rounded_rectangle([x0, y, x0 + COL_W, y + h], radius=18, fill=CARD)
            d.rounded_rectangle([x0, y, x0 + COL_W, y + HEAD_H], radius=18, fill=tuple(int(c * 0.28 + CARD[i] * 0.72) for i, c in enumerate(acc)))
            d.rectangle([x0, y + HEAD_H - 18, x0 + COL_W, y + HEAD_H], fill=tuple(int(c * 0.28 + CARD[i] * 0.72) for i, c in enumerate(acc)))
            d.rounded_rectangle([x0, y, x0 + 9, y + h], radius=4, fill=acc)
            d.text((x0 + 30, y + HEAD_H // 2), title, font=F_HEAD, fill=WHITE, anchor="lm")
            key_w = max(chip_row_width(d, r[0]) for r in rows)
            ry = y + HEAD_H + PAD // 2
            for keys, desc, star_row in rows:
                cx = x0 + 30
                cy = ry + ROW_H // 2
                for ki, k in enumerate(keys):
                    w = tw(d, k, F_KEY) + 24
                    d.rounded_rectangle([cx, cy - 18, cx + w, cy + 18], radius=8, fill=CHIP, outline=acc, width=2)
                    d.text((cx + w / 2, cy), k, font=F_KEY, fill=WHITE, anchor="mm")
                    cx += w + 14
                dx = x0 + 30 + key_w + 26
                d.text((dx, cy), desc, font=F_DESC, fill=WHITE, anchor="lm")
                limit = x0 + COL_W - (58 if star_row else 16)
                if dx + tw(d, desc, F_DESC) > limit:
                    raise SystemExit("Too wide: %r in %r" % (desc, title))
                if star_row:
                    star(d, x0 + COL_W - 34, cy, 12)
                ry += ROW_H
            y += h + CARD_GAP

    fy = H - 112
    d.line([(MARGIN, fy), (W - MARGIN, fy)], fill=(52, 60, 78), width=2)
    d.text((MARGIN, fy + 24), "Shortcut keys can be customized in Eplan, so yours may differ. Check a key on a copy of a project first.", font=F_SMALL, fill=SOFT)
    d.text((MARGIN, fy + 60), "Unofficial community guide by Walz Engineering. Not affiliated with or endorsed by EPLAN.", font=F_SMALL, fill=SOFT)
    d.text((W - MARGIN, fy + 60), "github.com/justin-walzengineering/Elgato-Stream-Deck-Public", font=F_SMALL, fill=SOFT, anchor="ra")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "images", "eplan-shortcut-cheat-sheet.png")
    img.save(out, optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
