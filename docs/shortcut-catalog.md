# Shortcut catalog

Every Eplan command used by the Stream Deck profile. A button simply sends a keyboard shortcut, so **the shortcut must exist in Eplan first**. Import [`../eplan/ShortcutKeys_StreamDeck.xml`](../eplan/ShortcutKeys_StreamDeck.xml) (see [getting-started](getting-started.md)) or assign the keys yourself in Eplan.

Status: **Draft** = not yet individually checked; **Spot-checked** = used and working, not every button tested; **Verified** = run in Eplan 2026.0.3.

Shortcut import file: tested on the maintainer's own account (Verified). The maintainer spot-checked the buttons after the import and they worked.

Eplan stores each shortcut as `command id ; modifier ; key code ; text`. The command ids below come from the exported shortcut file.

## Graphical editing

| Button | Shortcut | Eplan command | Status |
|--------|----------|---------------|--------|
| Grid A | Ctrl+Shift+Alt+S | id 37218 | Draft |
| Grid B | Ctrl+Shift+Alt+D | id 37219 | Draft |
| Grid C | Ctrl+Shift+Alt+F | id 37220 | Draft |
| Grid D | Ctrl+Shift+Alt+G | id 37221 | Draft |
| Align to Grid | Ctrl+Shift+Alt+A | id 37017 | Draft |
| To Front | Ctrl+Shift+Alt+H | id 37021 | Draft |
| To Back | Ctrl+Shift+Alt+J | id 37022 | Draft |
| Copy Format | Ctrl+Alt+6 | id 35366 | Draft |
| Paste Format | Ctrl+Alt+0 | id 35365 | Draft |

## Forms, symbols and libraries

| Button | Shortcut | Eplan command | Status |
|--------|----------|---------------|--------|
| Open Form | Ctrl+Alt+\ | id 35217 | Draft |
| Close Form | Ctrl+Alt+] | id 35343 | Draft |
| Open Library | Ctrl+Alt+S | id 35151 | Draft |
| Close Library | Ctrl+Alt+U | id 35152 | Draft |
| Open Symbol | Ctrl+Alt+P | id 35147 | Draft |
| Close Symbol | Ctrl+Alt+V | id 35339 | Draft |

## Text alignment (nine anchor positions)

All nine use `XGedStartInteractionAction /Name:XGedIaFormatText /justification:N`.

| Button | Shortcut | justification |
|--------|----------|---------------|
| Top Left | Ctrl+Alt+O | 1 |
| Top | Ctrl+Alt+; | 2 |
| Top Right | Ctrl+Alt+X | 3 |
| Left | Ctrl+Alt+' | 4 |
| Center | Ctrl+Alt+/ | 5 |
| Right | Ctrl+Alt+. | 6 |
| Bottom Left | Ctrl+Alt+Q | 7 |
| Bottom | Ctrl+Alt+, | 8 |
| Bottom Right | Ctrl+Alt+Z | 9 |

**Verified** in Eplan 2026.0.3: all nine buttons place text at the anchor shown on their icon.

## Updating and navigation

| Button | Shortcut | Eplan command | Status |
|--------|----------|---------------|--------|
| Update Reports | Ctrl+, | id 35175 | Draft |
| Update Connections | Ctrl+Alt+[ | id 35183 | Draft |
| Switch Tabs | Ctrl+F6 | Windows-style window switch | Draft |
| Design | Ctrl+Alt+L then Ctrl+Alt+N (multi action) | ids 37180, 37088 | Draft |

## Ideas queue (shortcuts already assigned in Eplan, not yet on the deck)

Ctrl+Alt+A (35036), Ctrl+Alt+D (35056), Ctrl+Alt+B (35295), Ctrl+Alt+E (35173), Ctrl+Alt+C (35191), Ctrl+Alt+I (37259), Ctrl+Alt+G (37127), Ctrl+Alt+T/R/F (36801/36804/36805), Ctrl+Alt+1-4 (36807-36810), Ctrl+Alt+5/7/8/9 (37313-37316). Work out what each does, then give it a button.
