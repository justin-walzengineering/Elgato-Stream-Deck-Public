# Tools

## make_icons.py

Draws the original button icons in [`../icons/`](../icons/) from scratch (no third-party artwork).

```bash
pip install pillow
python tools/make_icons.py
```

To rename a button or change its glyph or color, edit the `BUTTONS` list at the top of the script and run it again. Icons are 144 x 144 PNG files named after the button (`grid-a.png`, `to-front.png`, ...).

## build_guide.py

Builds the Word install and user guide for the release zip (`release-files/Install_and_User_Guide.docx`) from the screenshots in `docs/images` and the button tables in `docs/shortcut-catalog.md`.

```bash
pip install python-docx
python tools/build_guide.py
```

Run it again whenever the setup steps, screenshots, catalog or `VERSION` change, then run `release.ps1`.

## probes/

Two read-only Eplan scripts that were used to find out how Eplan's settings actions work. You do not need them to use the profile; they are kept as examples of exploring the scripting interface before building something. Both ran in Eplan 2026.0.3.

| Script | What it does |
|--------|--------------|
| [`probes/ProbeSettingsActions.cs`](probes/ProbeSettingsActions.cs) | Lists the parameters of the `XSettingsExport` and `XSettingsImport` actions. Found: export takes `node`, `XMLFile`, `prj`; import takes `XmlFile`, `src`, `Project`, `Node`. |
| [`probes/ProbeSettingsExportNodes.cs`](probes/ProbeSettingsExportNodes.cs) | Exports four settings nodes to your temp folder and reports which one holds the keyboard shortcuts. Found: `USER.SYSTEM.GUI.Shortcuts`. It never imports anything. |
