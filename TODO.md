# TODO

## Next up

- [x] Make a fresh Stream Deck backup.
- [ ] **Build the Eplan-only sanitized profile** (backup unpacked in `_local/`; Eplan buttons identified; personal buttons removed)
- [x] Review the backup for private data (see [`docs/sanitizing-checklist.md`](docs/sanitizing-checklist.md)).
- [ ] **Add more Eplan commands to the Stream Deck**: work through Eplan actions and shortcuts together with Justin, set up buttons on the physical device, and record each in [`docs/shortcut-catalog.md`](docs/shortcut-catalog.md).
- [ ] Write a README for each profile listing pages, buttons, and Eplan commands.
- [x] Create original icons (`tools/make_icons.py`, `icons/`).
- [x] Export Eplan shortcuts and test the import (`eplan/ShortcutKeys_StreamDeck.xml`).
- [x] Probe Eplan's settings actions (`scripts/ProbeSettingsActions.cs`, `ProbeSettingsExportNodes.cs`).
- [ ] Test `scripts/ImportShortcutKeys.cs` in Eplan (change one shortcut first, run the script, confirm it is restored), then on a colleague's account.

## Blog and video

- [ ] Draft the first blog post (overview: "Eplan on a Stream Deck").
- [ ] Plan the first video (screen capture of the deck driving Eplan).
- [ ] Keep post/video links in [`docs/blog-and-videos.md`](docs/blog-and-videos.md).

## Repo housekeeping

- [x] Local git repo, README, CLAUDE.md, LICENSE, .gitignore.
- [ ] Create the GitHub repo and push (**only with Justin's explicit OK**).
- [ ] Add issue templates for button/profile requests.
