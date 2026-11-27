"""Build the printable PDF of the Eplan shortcut sheets.

Usage (from the repo root):  python tools/build_pdf.py
Needs:  pip install pymupdf pillow
Run these first so the print images are current:
    python tools/make_cheatsheet.py --print
    python tools/make_keyboard_image.py --print

Output: docs/Eplan-Shortcuts-Printable.pdf  (US Letter, 2 pages: cheat sheet landscape, keyboard portrait)
Light theme so it prints without a page of dark ink.
"""
import os
import fitz  # pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "docs", "images")
OUT = os.path.join(ROOT, "docs", "Eplan-Shortcuts-Printable.pdf")
LETTER = (612, 792)
M = 24  # page margin in points


def add_page(doc, png, landscape):
    w, h = (LETTER[1], LETTER[0]) if landscape else LETTER
    page = doc.new_page(width=w, height=h)
    pic = fitz.Pixmap(png)
    box_w, box_h = w - 2 * M, h - 2 * M
    scale = min(box_w / pic.width, box_h / pic.height)
    iw, ih = pic.width * scale, pic.height * scale
    x, y = (w - iw) / 2, (h - ih) / 2
    page.insert_image(fitz.Rect(x, y, x + iw, y + ih), filename=png)


doc = fitz.open()
add_page(doc, os.path.join(IMG, "eplan-shortcut-cheat-sheet-print.png"), landscape=True)
add_page(doc, os.path.join(IMG, "eplan-shortcuts-keyboard-print.png"), landscape=False)
doc.set_metadata({"title": "Eplan Electric P8 Shortcuts - printable", "author": "Walz Engineering",
                  "subject": "Default keys in Eplan 2026. Unofficial community guide.", "creator": "", "producer": ""})
doc.save(OUT, deflate=True)
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
