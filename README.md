# Elgato Stream Deck for Eplan

Put your most-used Eplan Electric P8 commands, scripts and workflows on a physical button. This repo shares ready-to-import Stream Deck profiles, icons, and guides showing what you can trigger from a Stream Deck while you work in Eplan.

> ⚠️ **Unofficial community project.** Not affiliated with, endorsed by, or supported by EPLAN or Elgato. "EPLAN" and "Elgato" / "Stream Deck" are trademarks of their respective owners. Everything here is original work using only publicly available features.

## Why a Stream Deck?

Eplan is a powerful platform with a command for nearly everything. A Stream Deck is one more way to reach those commands quickly: one press to run a script, open a dialog, insert a macro, or send a keyboard shortcut. Buttons can show icons, change by profile, and group into folders, so each task (schematics, panel layout, reports, export) gets its own page.

## What's in this repo

| Folder | Contents |
|--------|----------|
| [`profiles/`](profiles/) | Stream Deck profile you can import (Stream Deck XL, Eplan buttons) |
| [`eplan/`](eplan/) | Eplan shortcut keys file that the buttons rely on |
| [`scripts/`](scripts/) | Eplan scripts, including a one-click shortcut import |
| [`icons/`](icons/) | Original button icons |
| [`tools/`](tools/) | The script that draws the icons |
| [`docs/`](docs/) | Setup guides and the catalog of Eplan commands |
| [`BUTTON-REQUESTS.md`](BUTTON-REQUESTS.md) | Request a new button |
| [`IDEAS.md`](IDEAS.md) and [`TODO.md`](TODO.md) | What is planned next |

## Quick start

Each button sends a keyboard shortcut, so Eplan needs the matching shortcuts first.

1. Install the Stream Deck software from Elgato.
2. Import the shortcuts into Eplan: use the [one-click script](scripts/README.md) or the manual steps in [`docs/getting-started.md`](docs/getting-started.md). Back up your own shortcuts first; the import replaces them.
3. Import the profile from [`profiles/`](profiles/) (double-click it, or Stream Deck > Preferences > Profiles > Import).
4. Press a button in Eplan. Try it on a copy of a project first.

## Ways to trigger Eplan from a button

See [`docs/shortcut-catalog.md`](docs/shortcut-catalog.md) for the growing list. Typical approaches:

- Keyboard shortcuts already assigned in Eplan (what the profile uses today)
- Eplan actions run through scripts
- Your own scripts loaded in Eplan (see the companion [Eplan Scripting GUI Examples](https://github.com/justin-walzengineering/Eplan-Scripting-GUI-Examples))
- Opening files, folders and websites

## Blog and videos

Walkthroughs, posts and videos are collected in [`docs/blog-and-videos.md`](docs/blog-and-videos.md).

## Contributing

Ideas, button requests and profile contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT, see [LICENSE](LICENSE).

---

Maintained by Justin Walz, [Walz Engineering](https://walzengineering.com). Need something custom built for your Eplan workflow? Get in touch.
