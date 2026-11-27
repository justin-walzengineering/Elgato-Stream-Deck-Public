"""Builds the Word install and user guide that goes into the release zip.

Usage (from the repo root):   python tools/build_guide.py
Needs:                        pip install python-docx
Output:                       release-files/Install_and_User_Guide.docx

The text follows release-files/INSTALL.txt and adds screenshots from docs/images.
The button table is read from docs/shortcut-catalog.md, so it stays in step with the catalog.
Rebuild whenever the setup steps, screenshots or catalog change, then run release.ps1.
"""
import os
import re
import struct

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "docs", "images")
VERSION = open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip()
BLUE = RGBColor(0x1F, 0x4E, 0x79)
GREY = RGBColor(0x59, 0x59, 0x59)

doc = Document()

# ---------------------------------------------------------------- page and styles
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(sec, side, Inches(1))


def set_font(style, name, size, bold=None, color=None):
    style.font.name = name
    style.font.size = Pt(size)
    if bold is not None:
        style.font.bold = bold
    if color is not None:
        style.font.color.rgb = color
    rpr = style.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.append(fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(attr), name)


styles = doc.styles
set_font(styles["Normal"], "Arial", 10.5)
styles["Normal"].paragraph_format.space_after = Pt(6)
styles["Normal"].paragraph_format.line_spacing = 1.1
set_font(styles["Title"], "Arial", 26, True, BLUE)
set_font(styles["Heading 1"], "Arial", 16, True, BLUE)
styles["Heading 1"].paragraph_format.space_before = Pt(18)
styles["Heading 1"].paragraph_format.space_after = Pt(6)
styles["Heading 1"].paragraph_format.keep_with_next = True
set_font(styles["Heading 2"], "Arial", 12.5, True, BLUE)
styles["Heading 2"].paragraph_format.space_before = Pt(12)
styles["Heading 2"].paragraph_format.space_after = Pt(4)
styles["Heading 2"].paragraph_format.keep_with_next = True
set_font(styles["List Bullet"], "Arial", 10.5)


# ---------------------------------------------------------------- helpers
def para(text="", bold=False, italic=False, size=None, color=None, align=None, space_after=None, keep_next=False):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        if size:
            r.font.size = Pt(size)
        if color is not None:
            r.font.color.rgb = color
    if align:
        p.alignment = align
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = keep_next
    return p


def rich(parts, style=None, left=None, hanging=None, keep_next=False):
    """parts: list of (text, bold) tuples."""
    p = doc.add_paragraph(style=style)
    for text, bold in parts:
        r = p.add_run(text)
        r.bold = bold
    if left is not None:
        p.paragraph_format.left_indent = Inches(left)
    if hanging is not None:
        p.paragraph_format.first_line_indent = Inches(-hanging)
    p.paragraph_format.keep_with_next = keep_next
    return p


def bullet(parts):
    if isinstance(parts, str):
        parts = [(parts, False)]
    return rich(parts, style="List Bullet")


def step(n, parts, keep_next=False):
    if isinstance(parts, str):
        parts = [(parts, False)]
    p = rich([(f"{n}.\t", True)] + parts, left=0.35, hanging=0.35, keep_next=keep_next)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(0.35))
    return p


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


def picture(name, caption, max_in=6.0, folder=IMG):
    path = os.path.join(folder, name)
    w, h = png_size(path)
    width = min(max_in, w / 96.0)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(path, width=Inches(width))
    c = para(caption, italic=True, size=8.5, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    return c


def shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcpr.append(shd)


def cell_borders(cell, **edges):
    tcpr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        spec = edges.get(edge)
        el = OxmlElement("w:" + edge)
        if spec:
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(spec[0]))
            el.set(qn("w:color"), spec[1])
        else:
            el.set(qn("w:val"), "nil")
        borders.append(el)
    tcpr.append(borders)


def callout(title, text, fill="FFF4CE", edge="E0A800"):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.rows[0].cells[0]
    c.width = Inches(6.5)
    shade(c, fill)
    cell_borders(c, left=(24, edge))
    p = c.paragraphs[0]
    r = p.add_run(title)
    r.bold = True
    p.paragraph_format.space_after = Pt(2)
    p2 = c.add_paragraph(text)
    p2.paragraph_format.space_after = Pt(2)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def grid_table(header, rows, widths, font=9.5):
    t = doc.add_table(rows=1, cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]
        c.width = Inches(widths[i])
        shade(c, "1F4E79")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(font)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    # repeat header row on each page
    trpr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trpr.append(th)
    for n, row in enumerate(rows):
        cells = t.add_row().cells
        for i, text in enumerate(row):
            cells[i].width = Inches(widths[i])
            if n % 2:
                shade(cells[i], "F2F6FA")
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.size = Pt(font)
        cant = OxmlElement("w:cantSplit")
        cant.set(qn("w:val"), "true")
        t.rows[-1]._tr.get_or_add_trPr().append(cant)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def add_page_field(paragraph):
    run = paragraph.add_run()
    for kind, text in (("begin", None), (None, " PAGE "), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)


# ---------------------------------------------------------------- catalog table
def read_catalog():
    """Returns [(section title, [(button, shortcut, command), ...]), ...] from docs/shortcut-catalog.md."""
    path = os.path.join(ROOT, "docs", "shortcut-catalog.md")
    out, title, rows, in_table, seen_sep = [], None, [], False, False
    for line in open(path, encoding="utf-8").read().splitlines() + [""]:
        if line.startswith("## "):
            if rows:
                out.append((title, rows))
            title, rows, in_table, seen_sep = line[3:].strip(), [], False, False
            continue
        if line.startswith("|"):
            cells = [c.strip().replace("`", "") for c in line.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                seen_sep = True
                continue
            if not in_table:
                in_table = True          # header row
                continue
            if seen_sep and len(cells) >= 3:
                button, shortcut, command = cells[0], cells[1], cells[2]
                if command.isdigit():
                    command = "Text justification " + command
                rows.append((button, shortcut, command))
        else:
            in_table = False if not line.startswith("|") else in_table
    if rows:
        out.append((title, rows))
    return [(t, r) for t, r in out if t and r and not t.startswith("Ideas")]


# ================================================================= CONTENT
# ---- title block
p = para("Eplan Shortcuts for the Elgato Stream Deck", space_after=2)
p.style = styles["Title"]
para("Install and User Guide", bold=True, size=15, color=GREY, space_after=2)
para(f"Version {VERSION}  |  Walz Engineering", size=10, color=GREY, space_after=14)
picture("streamdeck-eplan-profile.png", "The Eplan Shortcuts profile on a Stream Deck XL")

callout("Unofficial community project",
        "Not affiliated with, endorsed by, or supported by EPLAN or Elgato. \"EPLAN\", \"Elgato\" and \"Stream Deck\" are "
        "trademarks of their owners. Everything here is original work, released under the MIT license (see LICENSE.txt).",
        fill="EAF1F8", edge="1F4E79")

# ---- what you get
doc.add_heading("What you get", level=1)
para("This package puts 28 everyday Eplan Electric P8 commands on a Stream Deck XL. Each Stream Deck button sends a keyboard "
     "shortcut. Eplan must have the matching shortcut for a button to do anything, so setup has two parts:")
step(1, [("Part 1: ", True), ("put the shortcuts into Eplan (folder 1_Eplan).", False)])
step(2, [("Part 2: ", True), ("put the buttons on the Stream Deck (folder 2_StreamDeck).", False)])
para("What is in the package:", keep_next=True)
grid_table(
    ["File or folder", "What it is"],
    [
        ["1_Eplan\\ImportShortcutKeys.cs", "Script that imports the shortcuts into Eplan"],
        ["1_Eplan\\ShortcutKeys_StreamDeck.xml", "The shortcut keys the buttons use"],
        ["2_StreamDeck\\Eplan-Shortcuts-StreamDeck-XL.streamDeckProfile", "The Stream Deck buttons"],
        ["icons\\", "The button icons (optional)"],
        ["docs\\Shortcut-Catalog.md", "Every button and its Eplan command"],
        ["INSTALL.txt and this guide", "Setup instructions (same steps, this one with screenshots)"],
        ["CHANGELOG.md, LICENSE.txt", "What changed, and the license"],
    ],
    [3.6, 2.9],
)

doc.add_heading("What you need", level=2)
bullet("Eplan Electric P8 2026")
bullet("A Stream Deck XL (32 keys)")
bullet("The Elgato Stream Deck software for Windows")
para("The profile uses only the built-in Hotkey and Multi Action functions, so there are no plugins to install.")

doc.add_heading("Before you start", level=2)
callout("Part 1 replaces your Eplan shortcuts",
        "Importing replaces your Eplan user keyboard shortcuts with the set in the file. The script offers to back up your "
        "current shortcuts first. Leave that option on, and try everything on a copy of a project first.")

# ---- Part 1
doc.add_heading("Part 1: Shortcuts in Eplan (use the script)", level=1)
step(1, [("Copy the whole folder ", False), ("1_Eplan", True),
         (" to your computer, for example to C:\\EplanScripts\\. Keep the two files together.", False)])
step(2, [("In Eplan open ", False), ("File > Extras > Interfaces", True), (". Under ", False), ("Scripts", True),
         (" click ", False), ("Run", True), (".", False)], keep_next=True)
picture("run-script-menu.png", "File > Extras > Interfaces: Run, Load and Unload under Scripts", max_in=4.6)
step(3, [("Select ", False), ("ImportShortcutKeys.cs", True), (" and click Open.", False)])
step(4, [("In the window, click ", False), ("Browse", True), (" next to Shortcut file and choose ", False),
         ("ShortcutKeys_StreamDeck.xml", True),
         (" (the window fills this in if the file is in Documents, Downloads or the Desktop). Keep ", False),
         ("Back up my current shortcuts first", True), (" ticked and choose a backup folder.", False)], keep_next=True)
picture("script-window.png", "The Import shortcut keys window", max_in=4.8)
step(5, [("Click ", False), ("Import", True), (", then ", False), ("Yes", True), (" to confirm.", False)], keep_next=True)
picture("script-confirm.png", "The confirmation window", max_in=4.2)
step(6, [("Read the result message. It says whether Eplan now has the shortcuts from the file. If a shortcut does not "
          "respond, restart Eplan.", False)], keep_next=True)
picture("script-result.png", "The result: the shortcuts match the file, and the backup is saved", max_in=4.2)

doc.add_heading("To undo", level=2)
para("Run the script again and choose the backup file it saved (named ShortcutKeys_Backup_<date>_<time>.xml).")

doc.add_heading("Prefer to do it by hand?", level=2)
para("The same import can be done in Eplan's Settings dialog. Export your own shortcuts first as a backup, the same way.")
step(1, [("Open the Settings dialog and right-click ", False), ("User", True), (". Choose ", False), ("Export...", True),
         (" to make your backup, or ", False), ("Import...", True), (" to load the shortcut file.", False)], keep_next=True)
picture("settings-user-menu.png", "Right-click User in the Settings dialog", max_in=3.2)
step(2, [("Tick only ", False), ("Shortcut keys", True), (", choose the file, and click OK. The Import window looks the same "
                                                          "as this Export window.", False)], keep_next=True)
picture("export-settings-dialog.png", "Export settings with only Shortcut keys ticked", max_in=4.4)

# ---- Part 2
doc.add_heading("Part 2: Buttons on the Stream Deck", level=1)
step(1, "Install the Stream Deck software from Elgato and connect your Stream Deck XL.")
step(2, [("Double-click ", False), ("2_StreamDeck\\Eplan-Shortcuts-StreamDeck-XL.streamDeckProfile", True),
         (". Or, inside the Stream Deck app: click the gear icon, open the ", False), ("Profiles", True),
         (" tab, click the small arrow below the profile list, choose ", False), ("Import...", True),
         (" and pick the file.", False)], keep_next=True)
picture("streamdeck-import-profile.png", "Stream Deck Preferences, Profiles tab: Import is in the menu below the list", max_in=4.8)
step(3, [("A new profile named ", False), ("Eplan Shortcuts (XL)", True),
         (" appears. Your other profiles are not changed. Pick it with the profile drop-down under the device name.", False)])
step(4, "The first column is empty so you can add your own buttons.")

doc.add_heading("Try it", level=1)
para("Open an Eplan project (a copy) and press a button, for example one of the Grid buttons or the nine text-position buttons. "
     "The table below lists every button and the Eplan command it runs.")
picture("layout.png", "Button layout (first column left free)", max_in=5.6, folder=os.path.join(ROOT, "profiles"))

# ---- button table
doc.add_heading("Button reference", level=1)
para("Each button sends the shortcut shown. The Eplan command column is the internal name Eplan uses for the command.")
for title, rows in read_catalog():
    doc.add_heading(title, level=2)
    grid_table(["Button", "Shortcut", "Eplan command"], [list(r) for r in rows], [1.7, 1.9, 2.9])

# ---- troubleshooting
doc.add_heading("If something does not work", level=1)
bullet([("A button does nothing: ", True), ("the Eplan window must be in front, and Part 1 must be done. Restart Eplan after the "
                                           "import if needed.", False)])
bullet([("A different command runs: ", True), ("another command in your Eplan already uses that shortcut. Restore your backup "
                                              "with the script, or change the shortcut in Eplan.", False)])
bullet([("The script does not start: ", True), ("Eplan 2026 is required. Check that Windows has not blocked the file (right-click "
                                               "it, choose Properties, then Unblock).", False)])
bullet([("The profile does not import: ", True), ("check that the Stream Deck software is up to date and that the device is a "
                                                 "Stream Deck XL.", False)])

p = para("", space_after=0)
para("Maintained by Justin Walz, Walz Engineering. Questions and ideas are welcome, and if you would like help with a script of "
     "your own, feel free to get in touch.", size=9.5, color=GREY, space_after=2)
para("Project page: https://github.com/justin-walzengineering/Elgato-Stream-Deck-Public", size=9.5, color=GREY)

# ---------------------------------------------------------------- footer
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run(f"Eplan Shortcuts for the Elgato Stream Deck  |  Version {VERSION}  |  Walz Engineering  |  Page ")
r.font.size = Pt(8)
r.font.color.rgb = GREY
add_page_field(fp)
for run in fp.runs:
    run.font.size = Pt(8)
    run.font.color.rgb = GREY

core = doc.core_properties
core.title = "Eplan Shortcuts for the Elgato Stream Deck: Install and User Guide"
core.author = "Walz Engineering"
core.comments = f"Version {VERSION}"

out = os.path.join(ROOT, "release-files", "Install_and_User_Guide.docx")
doc.save(out)
print("wrote", out)
