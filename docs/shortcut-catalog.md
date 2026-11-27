# Shortcut catalog

Every Eplan command used by the Stream Deck profile. A button simply sends a keyboard shortcut, so **the shortcut must exist in Eplan first**. Import [`../eplan/ShortcutKeys_StreamDeck.xml`](../eplan/ShortcutKeys_StreamDeck.xml) (see [getting-started](getting-started.md)) or assign the keys yourself in Eplan.

Status: **Draft** = not yet individually checked; **Spot-checked** = used and working, not every button tested; **Verified** = run in Eplan 2026.

Shortcut import file: tested on the maintainer's own account and on a fresh account (Verified). The maintainer spot-checked the buttons after the import and they worked.

Action names come from matching the command ids in the exported shortcut file to the installed Eplan command table.

## Graphical editing

| Button | Shortcut | Eplan command | Status |
|--------|----------|---------------|--------|
| Grid A | Ctrl+Shift+Alt+S | XGedSetGridsizeAction /id:1 | Draft |
| Grid B | Ctrl+Shift+Alt+D | XGedSetGridsizeAction /id:2 | Draft |
| Grid C | Ctrl+Shift+Alt+F | XGedSetGridsizeAction /id:3 | Draft |
| Grid D | Ctrl+Shift+Alt+G | XGedSetGridsizeAction /id:4 | Draft |
| Align to Grid | Ctrl+Shift+Alt+A | XGedIaArrangeOnGrid | Draft |
| To Front | Ctrl+Shift+Alt+H | XGedIaToForeground | Draft |
| To Back | Ctrl+Shift+Alt+J | XGedIaToBackground | Draft |
| Copy Format | Ctrl+Alt+6 | XGedCopyGraphicalFormatAction (format painter) | Draft |
| Paste Format | Ctrl+Alt+0 | XGedAcceptGraphicalFormatAction (format painter) | Draft |

## Forms, symbols and libraries

| Button | Shortcut | Eplan command | Status |
|--------|----------|---------------|--------|
| Open Form | Ctrl+Alt+\ | XFOEActionFormOpen | Draft |
| Close Form | Ctrl+Alt+] | XFOEActionFormClose | Draft |
| Open Library | Ctrl+Alt+S | XSymLibOpenAction | Draft |
| Close Library | Ctrl+Alt+U | XSymLibCloseAction | Draft |
| Open Symbol | Ctrl+Alt+P | XSymbolOpenAction | Draft |
| Close Symbol | Ctrl+Alt+V | XSymbolCloseAction | Draft |

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

**Verified** in Eplan 2026: all nine buttons place text at the anchor shown on their icon.

## Updating and navigation

| Button | Shortcut | Eplan command | Status |
|--------|----------|---------------|--------|
| Update Reports | Ctrl+, | XFgUpdateEvaluationAction | Draft |
| Update Connections | Ctrl+Alt+[ | EsGenerateConnections | Draft |
| Switch Tabs | Ctrl+F6 | Windows-style window switch | Draft |
| Design | Ctrl+Alt+L then Ctrl+Alt+N (multi action) | XGedActionToggleConstructionMode, XGedToggleObjectSnapAction | Draft |

## Ideas queue (shortcuts already assigned in Eplan, not yet on the deck)

Ctrl+Alt+A (35036), Ctrl+Alt+D (35056), Ctrl+Alt+B (35295), Ctrl+Alt+E (35173), Ctrl+Alt+C (35191), Ctrl+Alt+I (37259), Ctrl+Alt+G (37127), Ctrl+Alt+T/R/F (36801/36804/36805), Ctrl+Alt+1-4 (36807-36810), Ctrl+Alt+5/7/8/9 (37313-37316). Work out what each does, then give it a button.
