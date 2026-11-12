# Tools

## make_icons.py

Draws the original button icons in [`../icons/`](../icons/) from scratch (no third-party artwork).

```bash
pip install pillow
python tools/make_icons.py
```

To rename a button or change its glyph or color, edit the `BUTTONS` list at the top of the script and run it again. Icons are 144 x 144 PNG files named after the button (`grid-a.png`, `to-front.png`, ...).
