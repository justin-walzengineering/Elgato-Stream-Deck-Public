# TODO

## Next up

- [x] Make a fresh Stream Deck backup.
- [x] Build the Eplan-only sanitized public profile (`profiles/`) and a private profile with personal buttons (`_local/private/`, git-ignored).
- [x] Import the public profile on a fresh account (worked).
- [x] Review the backup for private data (see [`docs/sanitizing-checklist.md`](docs/sanitizing-checklist.md)).
- [ ] **Page 2: macro-project editing page** (requests go in `BUTTON-REQUESTS.md`) (generate macros, etc.) for both profiles; replaces the copy of page 1, keeps only the previous-page button.
- [ ] **Add more Eplan commands to the Stream Deck**: work through Eplan actions and shortcuts together with Justin, set up buttons on the physical device, and record each in [`docs/shortcut-catalog.md`](docs/shortcut-catalog.md).
- [ ] Write a README for each profile listing pages, buttons, and Eplan commands.
- [x] Create original icons (`tools/make_icons.py`, `icons/`).
- [x] Export Eplan shortcuts and test the import (`eplan/ShortcutKeys_StreamDeck.xml`).
- [x] Probe Eplan's settings actions (now in `tools/probes/`).
- [x] Test `scripts/ImportShortcutKeys.cs` in Eplan on the maintainer's account (works).
- [x] Test the import script and shortcut file on a fresh account (worked).
- [ ] Add the import script to the docs (getting-started, screenshots) and a README for `scripts/`.

## Release package

- [x] `release.ps1`, install guide template, scrub check, `docs/releasing.md` (test build ok).
- [ ] When ready: run `release.ps1`, test the zip on a clean PC, then (with Justin's OK) attach it to a GitHub release.

## Blog and video

- [x] Draft the first blog post (private blog repo: `posts/sd01-eplan-on-a-stream-deck.md`, status draft, not committed there yet).
- [x] Repo published; fresh-account test done.
- [ ] Before the post goes out: add screenshots in Wix, update the post's tested line, set a release date.
- [ ] Plan the first video (screen capture of the deck driving Eplan).
- [ ] Keep post/video links in [`docs/blog-and-videos.md`](docs/blog-and-videos.md).

## Repo housekeeping

- [x] Local git repo, README, CLAUDE.md, LICENSE, .gitignore.
- [ ] Create the GitHub repo and push (**only with Justin's explicit OK**).
- [ ] Add issue templates for button/profile requests.
