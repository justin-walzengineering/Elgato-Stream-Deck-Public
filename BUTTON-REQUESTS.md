# Button requests

The working list for new Stream Deck buttons. Add a row, tell Claude (or open an issue if you are a reader), and the button is added to **both** profiles (public and private).

## How to fill in a row

| Column | What to write |
|--------|---------------|
| **Page / spot** | `Page 2` plus a position, or just a group ("with the 3D view buttons"). Positions are **column,row** counted from the top left: `1,1` is top left, `8,4` is bottom right. If you skip it, the next free spot is used. |
| **Button name** | Short label for the icon, two lines at most, for example `Placement Area`. |
| **What it does** | The command as you see it in Eplan, in plain words. |
| **Works in** | Where you use it: Layout space, Schematic editor, Macro project, Parts management, and so on. |
| **Shortcut** | The shortcut it already has in Eplan, or `needs one`. |
| **Notes** | Anything special: changes project data, needs something selected, only works in 3D. |

You do **not** need to know Eplan's internal action name. If the command has no shortcut yet, assign one in Eplan (the command is found by its normal name), export your shortcut keys, and the action is looked up from the export.

## Requests

| Page / spot | Button name | What it does | Works in | Shortcut | Notes |
|-------------|-------------|--------------|----------|----------|-------|
| Page 2, with Mounting Surface | Placement Area | Defines the placement area | Layout space | needs one | Example row |
| | | | | | |

## Done

Moved to [docs/shortcut-catalog.md](docs/shortcut-catalog.md) once the button exists in the profiles.
