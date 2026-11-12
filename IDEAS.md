# Ideas and future improvements

A running list. Add to it freely; move items to `TODO.md` when they are scheduled, and delete them when done.

## Shortcut import script (next)

Replace the manual import (Settings > right-click **User** > Import > tick **Shortcut keys** > pick file) with a small Eplan script.

- Run it from a ribbon button or Extras > Run script; show a themed window: what will be imported, a **Back up my current shortcuts first** check box (default on), a file picker defaulting to `eplan/ShortcutKeys_StreamDeck.xml`, and an Import button with a clear success or failure message.
- Uses Eplan's `XSettingsExport` / `XSettingsImport` actions. Parameter names are **not yet confirmed**: run a probe script in Eplan that lists the parameters of both actions, then write the real script.
- Must handle: Cancel, missing file, file for a different Eplan version, and a clear note that shortcuts are replaced.
- Match the GUI style of [Eplan-Scripting-GUI-Examples](https://github.com/justin-walzengineering/Eplan-Scripting-GUI-Examples): light/dark theme, centered on Eplan, themed message window instead of `MessageBox`, C# 5 only.
- Write it from scratch with generic data. Do not copy code from private or employer repos; only the concept travels.
- Candidate for the public examples repo idea list too (ask Justin first).

## Testing

- [ ] Import on a colleague's (clean) Eplan user account and confirm every button works.
- [ ] Confirm the Eplan version the import file works on (built from 2026.0.3).
- [ ] Re-test after each Eplan update.

## Profile and buttons

- [ ] Add the shortcuts from the catalog's "Ideas queue" as new buttons.
- [ ] Name Grid A to D after what they actually do (grid sizes).
- [ ] Use the free first column for page navigation and new Eplan commands.
- [ ] Profile variants for different Stream Deck sizes (15-key, 32-key).
- [ ] Optional: a second page for panel layout (Pro Panel) and one for reports/exports.

## Icons

- [ ] Animated or two-state icons for toggle commands.
- [ ] Dark/light icon variants.
- [ ] A small icon-maker guide (how `tools/make_icons.py` works) for readers who want their own.

## Docs, blog and video

- [ ] Screenshots of the import steps and the finished deck for the README.
- [ ] Blog series: overview, building shortcuts in Eplan, importing the profile, making icons.
- [ ] Video: from empty deck to working Eplan buttons.
- [ ] Short FAQ (shortcuts not firing, focus problems, multi-monitor, Eplan versions).

## Repo housekeeping

- [ ] GitHub issue templates (button request, profile contribution).
- [ ] CI check that no usernames or paths slip into committed profiles.
- [ ] Create the GitHub repo and publish (only with Justin's explicit OK).
