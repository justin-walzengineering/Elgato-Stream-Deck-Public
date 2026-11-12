# Scripts

Small Eplan scripts that go with the Stream Deck profile. They are plain `.cs` files that you run from inside Eplan 2026.

New to running scripts? See [How to run a script](https://github.com/justin-walzengineering/Eplan-Scripting-GUI-Examples/blob/main/docs/running-scripts.md) in the companion Eplan Scripting GUI Examples repo.

## Import shortcut keys (the one most people want)

| | |
|---|---|
| **File** | [`ImportShortcutKeys.cs`](ImportShortcutKeys.cs) |
| **Level** | Intermediate |
| **Status** | Works. Run in Eplan 2026.0.3 on the maintainer's account. A fresh-account test is still to do. |

Imports a shortcut-keys XML file (for example [`../eplan/ShortcutKeys_StreamDeck.xml`](../eplan/ShortcutKeys_StreamDeck.xml)) into Eplan in one click, so the Stream Deck buttons have the shortcuts they send.

**What it changes:** your Eplan **user** keyboard shortcuts, and nothing else. It **replaces** your whole shortcut set with the one in the file.

**How to use it**

1. Copy `ImportShortcutKeys.cs` to a folder on your computer, for example `C:\EplanScripts\`.
2. In Eplan: File > Extras > Interfaces, then **Run** (under Scripts), and choose the file.
3. In the window, pick the shortcut file. Keep **Back up my current shortcuts first** ticked and pick a backup folder.
4. Click **Import**, then **Yes** to confirm.
5. Read the result message. It compares the shortcuts Eplan now has with the file and says whether they match.

**To undo:** run the script again and choose the backup file it saved (named `ShortcutKeys_Backup_<date>_<time>.xml`).

**What you learn from the code**

- Running Eplan's settings export and import actions with parameters
- Backing up before a risky change, and stopping if the backup fails
- Checking the result afterwards instead of trusting it
- A small window that follows Eplan's light or dark theme, centered on Eplan

## Probe scripts

Read-only helpers used to find out how Eplan's settings actions work. Most readers do not need them. They are kept as examples of how to explore the scripting interface before building something.

| Script | What it does |
|--------|--------------|
| [`ProbeSettingsActions.cs`](ProbeSettingsActions.cs) | Lists the parameters of the `XSettingsExport` and `XSettingsImport` actions in a window you can copy from. Found: export takes `node`, `XMLFile`, `prj`; import takes `XmlFile`, `src`, `Project`, `Node`. |
| [`ProbeSettingsExportNodes.cs`](ProbeSettingsExportNodes.cs) | Exports four settings nodes to your temp folder and reports which one holds the keyboard shortcuts. Found: `USER.SYSTEM.GUI.Shortcuts`. It never imports anything. |

Both ran in Eplan 2026.0.3.

## Notes

- Eplan 2026 compiles scripts with C# 5, so there is no string interpolation, `?.`, or `out var` in these files.
- Try scripts on a throwaway setup first, and keep the backup the import script offers.
- All scripts are MIT licensed and written from scratch for this repo.
