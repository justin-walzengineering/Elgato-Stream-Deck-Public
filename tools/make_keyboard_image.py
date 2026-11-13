"""Draw the Eplan shortcuts-on-the-keyboard image from scratch.

Usage (from the repo root):  python tools/make_keyboard_image.py
Needs:  pip install pillow

Output: docs/images/eplan-shortcuts-keyboard.png
Two keyboards: keys pressed on their own (with the Shift / Alt versions in small print),
and keys pressed with Ctrl (with the Ctrl+Shift versions in small print).
Edit PLAIN or CTRL below to change a label, then run it again.
The script stops with an error if a label does not fit on its key.
All artwork is original (simple shapes and text only).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = 2400
MARGIN = 60
BG = (20, 24, 32)
KEY = (34, 40, 52)
KEY_DIM_TXT = (92, 102, 120)
WHITE = (240, 244, 250)
SOFT = (170, 180, 198)

DRAW, SYM, CONN, EDIT, VIEW, PAGES, SEARCH, REP, EVERY, PANEL = (
    (79, 156, 255), (176, 132, 255), (72, 207, 140), (64, 214, 214),
    (255, 214, 79), (255, 107, 129), (140, 160, 255), (255, 170, 64),
    (150, 165, 190), (214, 170, 120))

LEGEND = [("Draw", DRAW), ("Symbols and macros", SYM), ("Connections", CONN),
          ("Move and edit", EDIT), ("View and snap", VIEW), ("Pages", PAGES),
          ("Search and check", SEARCH), ("Reports and PLC", REP),
          ("Everyday", EVERY), ("Panel layout (3D)", PANEL)]

# key -> (main label, category, small print)   Use \n for a second line.
PLAIN = {
    "Esc": ("Cancel", EVERY, ""),
    "F3": ("Angle\ndown, right", CONN, "Shift:\nDevice pt"),
    "F4": ("Angle\ndown, left", CONN, "Shift:\nInterruption"),
    "F5": ("Redraw\nview", VIEW, "Shift:\nCable def."),
    "F6": ("Angle\nup, left", CONN, "Shift:\nShield"),
    "F7": ("T-node\ndown", CONN, "Shift:\nConn. def. pt"),
    "F8": ("T-node\nup", CONN, "Shift:\nJumper"),
    "F9": ("T-node\nright", CONN, ""),
    "F10": ("T-node\nleft", CONN, ""),
    "F11": ("", CONN, "Shift:\nBlack box"),
    "F12": ("Page\nnavigator", PAGES, ""),
    "Space": ("Selection window", EDIT, ""),
    "Tab": ("Jump to\nelement points", VIEW, ""),
    "Up": ("Jump in\ngrid", VIEW, "Shift: Pan"),
    "Down": ("Jump in\ngrid", VIEW, "Shift: Pan"),
    "Left": ("Jump in\ngrid", VIEW, "Shift: Pan"),
    "Right": ("Jump in\ngrid", VIEW, "Shift: Pan"),
    "3": ("", VIEW, "Alt:\nWhole page"),
    "Backspace": ("", EVERY, "Alt: Undo"),
    "Q": ("Quick snap\non / off", VIEW, ""),
    "E": ("Ellipse", DRAW, ""),
    "R": ("Rectangle", DRAW, "Shift:\nRel. coords"),
    "T": ("Text", DRAW, ""),
    "U": ("Show / hide\ninvisible", VIEW, ""),
    "I": ("Insertion\npoints", VIEW, ""),
    "O": ("Move base\npoint", EDIT, ""),
    "P": ("Coordinate\ninput", VIEW, ""),
    "A": ("Change\nhandle (3D)", PANEL, ""),
    "S": ("Set\nincrement", VIEW, ""),
    "D": ("Duplicate", EDIT, ""),
    "F": ("Go to\ncounterpart", PAGES, ""),
    "G": ("Group", EDIT, ""),
    "H": ("Rail: use\nlength", PANEL, ""),
    "J": ("Rail:\ncentered", PANEL, ""),
    "K": ("Circle", DRAW, ""),
    "L": ("Polyline", DRAW, ""),
    "Z": ("Zoom\nwindow", VIEW, ""),
    "B": ("Window\nmacro", SYM, ""),
    "M": ("Insert\nmacro", SYM, ""),
    "V": ("Move", EDIT, ""),
    "Ins": ("Insert\nsymbol", SYM, "Alt:\nInsert device"),
    "Del": ("Delete", EVERY, "Shift: Cut\nAlt: Delete\nplacement"),
    "PgUp": ("Previous\npage", PAGES, "Alt: Prev.\ncross-ref"),
    "PgDn": ("Next\npage", PAGES, "Alt: Next\ncross-ref"),
}

CTRL = {
    "Ctrl": ("Hold", WHITE, ""),
    "F1": ("Ribbon\nmin / max", EVERY, ""),
    "F2": ("Line", DRAW, ""),
    "F4": ("Close\neditor", EVERY, ""),
    "F5": ("Window\nmacro", SYM, ""),
    "F6": ("Docked\ntabs", EVERY, "+Shift:\nGrid on / off"),
    "F7": ("Stacked\ntabs", EVERY, ""),
    "F11": ("Add\nstructure box", SYM, ""),
    "F12": ("Switch\nwindows", EVERY, ""),
    "Space": ("Jump to counterpart", PAGES, ""),
    "Up": ("Next\ninsertion pt", VIEW, ""),
    "Down": ("Next\ninsertion pt", VIEW, ""),
    "Left": ("Next\ninsertion pt", VIEW, ""),
    "Right": ("Next\ninsertion pt", VIEW, ""),
    "U": ("", CONN, "+Shift:\nInterrupt conn."),
    "F10": ("Page\nmacro", SYM, ""),
    "Enter": ("Redraw", VIEW, ""),
    ",": ("Update\nreports", REP, "+Shift:\nProject reports"),
    "Ins": ("Insert\nmacro", SYM, ""),
    "N": ("New\npage", PAGES, ""),
    "M": ("Select\npage", PAGES, "+Shift:\n2D layout nav."),
    "J": ("Go to\ngraphic", PAGES, ""),
    "F": ("Find", SEARCH, "+Shift:\nNext entry"),
    "I": ("Add to\nsearch", SEARCH, ""),
    "S": ("Sync\nselection", SEARCH, ""),
    "V": ("Paste", EVERY, "+Shift:\nPrev. entry"),
    "P": ("Print", REP, "+Shift:\nCheck project"),
    "E": ("Generate\nreports", REP, "+Shift:\nMessages"),
    "W": ("Placement\noptions", PANEL, ""),
    "R": ("Rotate", EDIT, "+Shift:\n3D rotation"),
    "T": ("Path\ntext", DRAW, ""),
    "O": ("Address\nPLC", REP, ""),
    "L": ("PLC conn.\npoints", REP, ""),
    "A": ("Select all", EVERY, "+Shift:\nLinear dim."),
    "D": ("Properties", EDIT, ""),
    "G": ("Arc", DRAW, ""),
    "K": ("Generate\nmacros", SYM, ""),
    "Z": ("Undo", EVERY, ""),
    "X": ("Cut", EVERY, ""),
    "C": ("Copy", EVERY, ""),
    "B": ("Move\nprop. text", EDIT, ""),
    "Y": ("Redo", EVERY, ""),
}


D3 = {
    "T": ("Top\nview", PANEL, ""), "R": ("Right\nview", PANEL, ""), "F": ("Front\nview", PANEL, ""),
    "1": ("SW\nisometric", PANEL, ""), "2": ("SE\nisometric", PANEL, ""),
    "3": ("NE\nisometric", PANEL, ""), "4": ("NW\nisometric", PANEL, ""),
}


def layout():
    """Return [(label, x, y, w)] for a tenkeyless keyboard (units of one key)."""
    keys = []

    def row(y, items, x=0.0):
        for lab, w in items:
            if lab:
                keys.append((lab, x, y, w))
            x += w

    row(0, [("Esc", 1), ("", 1)] + [(f"F{i}", 1) for i in range(1, 5)] + [("", .5)]
        + [(f"F{i}", 1) for i in range(5, 9)] + [("", .5)] + [(f"F{i}", 1) for i in range(9, 13)])
    row(1.35, [(c, 1) for c in "`1234567890-="] + [("Backspace", 2)])
    row(2.35, [("Tab", 1.5)] + [(c, 1) for c in "QWERTYUIOP[]"] + [("\\", 1.5)])
    row(3.35, [("Caps", 1.75)] + [(c, 1) for c in "ASDFGHJKL;'"] + [("Enter", 2.25)])
    row(4.35, [("Shift", 2.25)] + [(c, 1) for c in "ZXCVBNM,./"] + [("Shift", 2.75)])
    row(5.35, [("Ctrl", 1.25), ("Win", 1.25), ("Alt", 1.25), ("Space", 6.25), ("Alt ", 1.25), ("Win ", 1.25), ("Menu", 1.25), ("Ctrl ", 1.25)])
    # navigation cluster and arrows
    nx = 15.35
    row(0, [("PrtSc", 1), ("ScrLk", 1), ("Pause", 1)], nx)
    row(1.35, [("Ins", 1), ("Home", 1), ("PgUp", 1)], nx)
    row(2.35, [("Del", 1), ("End", 1), ("PgDn", 1)], nx)
    row(4.35, [("", 1), ("Up", 1)], nx)
    row(5.35, [("Left", 1), ("Down", 1), ("Right", 1)], nx)
    return keys


def font(name, size):
    for p in (rf"C:\Windows\Fonts\{name}", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


F_TITLE = font("segoeuib.ttf", 76)
F_SUB = font("segoeui.ttf", 32)
F_BOARD = font("segoeuib.ttf", 40)
F_NOTE = font("segoeui.ttf", 26)
F_SMALL = font("segoeui.ttf", 24)
F_LEG = font("segoeui.ttf", 24)
F_CAP = font("segoeuib.ttf", 20)
F_MAIN = font("segoeuib.ttf", 19)
F_FINE = font("segoeui.ttf", 14)

U = 124           # one key unit in pixels
KG = 6            # gap between keys
BOARD_H = int(6.35 * U) + 10


def tint(c, k=0.26):
    return tuple(int(c[i] * k + KEY[i] * (1 - k)) for i in range(3))


PROBLEMS = []


def fit_lines(d, text, f, max_w, where):
    for line in text.split("\n"):
        if d.textlength(line, font=f) > max_w:
            PROBLEMS.append("%r (%s)" % (line, where))


def show_label(key):
    return {"Backspace": "Bksp", "Caps": "Caps", "Alt ": "Alt", "Win ": "Win", "Ctrl ": "Ctrl",
            "Up": "\u2191", "Down": "\u2193", "Left": "\u2190", "Right": "\u2192"}.get(key, key)


def draw_board(d, x0, y0, data, mod_keys=(), rows=None):
    for key, kx, ky, kw in layout():
        if rows is not None and (ky not in rows or kx >= 15):
            continue
        x = x0 + kx * U
        y = y0 + (ky - (min(rows) if rows else 0)) * U
        w = kw * U - KG
        h = U - KG
        info = data.get(key)
        mod = key.strip() in mod_keys
        if mod:
            d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(250, 250, 250), outline=WHITE, width=3)
            d.text((x + w / 2, y + h / 2), key.strip(), font=font("segoeuib.ttf", 26), fill=(20, 24, 32), anchor="mm")
            continue
        if not info:
            d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(28, 33, 44), outline=(44, 52, 68), width=2)
            d.text((x + 10, y + 7), show_label(key), font=F_CAP, fill=KEY_DIM_TXT)
            continue
        main, cat, fine = info
        d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=tint(cat), outline=cat, width=3)
        d.text((x + 10, y + 7), show_label(key), font=F_CAP, fill=cat)
        max_w = w - 14
        if main:
            fm = F_MAIN
            for size in (19, 18, 17, 16, 15):
                fm = font("segoeuib.ttf", size)
                if all(d.textlength(t, font=fm) <= max_w for t in main.split("\n")):
                    break
            fit_lines(d, main, fm, max_w, key)
            ty = y + 35
            for line in main.split("\n"):
                d.text((x + w / 2, ty), line, font=fm, fill=WHITE, anchor="mt")
                ty += 21
        if fine:
            fit_lines(d, fine, F_FINE, max_w, key + " small print")
            lines = fine.split("\n")
            ty = y + h - 4 - 16 * len(lines)
            for line in lines:
                d.text((x + w / 2, ty), line, font=F_FINE, fill=SOFT, anchor="mt")
                ty += 16


def main():
    board_w = int(18.35 * U)
    x0 = (W - board_w) // 2
    top = 215
    legend_h = 96
    H = top + legend_h + 2 * (BOARD_H + 110) + (int(3.4 * U) + 10 + 110) + 120
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.text((MARGIN, 40), "Eplan Electric P8 Shortcuts on the Keyboard", font=F_TITLE, fill=WHITE)
    d.text((MARGIN, 140), "Default keys in Eplan 2026. Each key shows what it does; the color shows the kind of job.", font=F_SUB, fill=SOFT)

    # legend
    lx, ly = MARGIN, top
    for name, col in LEGEND:
        wtxt = d.textlength(name, font=F_LEG)
        if lx + wtxt + 60 > W - MARGIN:
            lx, ly = MARGIN, ly + 44
        d.rounded_rectangle([lx, ly + 4, lx + 26, ly + 30], radius=6, fill=tint(col), outline=col, width=3)
        d.text((lx + 38, ly + 17), name, font=F_LEG, fill=SOFT, anchor="lm")
        lx += 38 + wtxt + 34

    y = top + legend_h
    for title, note, data, mods, rows in [
        ("1  Press the key on its own", "Small print: the Shift or Alt version of the same key.", PLAIN, (), None),
        ("2  Hold Ctrl and press the key", "Small print: add Shift as well.", CTRL, ("Ctrl",), None),
        ("3  Hold Ctrl and Alt together", "3D views for panel layout (number, QWERTY and home rows shown).", D3, (), (1.35, 2.35, 3.35)),
    ]:
        d.text((MARGIN, y), title, font=F_BOARD, fill=WHITE)
        d.text((MARGIN + d.textlength(title, font=F_BOARD) + 30, y + 14), note, font=F_NOTE, fill=SOFT)
        draw_board(d, x0, y + 66, data, mods, rows)
        y += (BOARD_H if rows is None else int(3.4 * U) + 10) + 110

    fy = H - 112
    d.line([(MARGIN, fy), (W - MARGIN, fy)], fill=(52, 60, 78), width=2)
    d.text((MARGIN, fy + 24), "Shortcut keys can be customized in Eplan, so yours may differ. Check a key on a copy of a project first.", font=F_SMALL, fill=SOFT)
    d.text((MARGIN, fy + 60), "Unofficial community guide by Walz Engineering. Not affiliated with or endorsed by EPLAN.", font=F_SMALL, fill=SOFT)
    d.text((W - MARGIN, fy + 60), "github.com/justin-walzengineering/Elgato-Stream-Deck-Public", font=F_SMALL, fill=SOFT, anchor="ra")

    if PROBLEMS:
        raise SystemExit("Too wide on key: " + "; ".join(PROBLEMS))
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "images", "eplan-shortcuts-keyboard.png")
    img.save(out, optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
