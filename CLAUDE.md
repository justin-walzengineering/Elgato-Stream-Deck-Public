# CLAUDE.md

Guidance for Claude Code (and human contributors) working in this repository.

## What this repo is

A free, public collection of **original** Elgato Stream Deck profiles, icons and guides for working faster in Eplan Electric P8. Audience: Eplan users of all levels who want hardware shortcuts. Maintained by Justin Walz, Walz Engineering. It is a community resource, not self-promotion. Content also feeds Walz Engineering blog posts and videos.

## Hard rules

1. **Sanitize everything.** Raw Stream Deck backups (`.streamDeckProfilesBackup`) and exported profiles contain Windows usernames, local paths, machine names, project and customer names. Never commit one raw. Unpack copies in `_local/` (git-ignored), follow `docs/sanitizing-checklist.md`, and show Justin the findings before anything is added to `profiles/`.
2. **No customer or employer material.** No client names, project names, part numbers, drawings, or company data. Only the concept travels; use generic names and paths (for example `C:\EplanScripts\`).
3. **Original work only.** Never copy Eplan-owned or Elgato-owned documentation, training material, or icons. Write guides in our own words. Icons must be original or properly licensed (state the source).
4. **No Eplan files in the repo.** No DLLs, API docs, PDFs, zips, or project/template files.
5. **Unofficial.** Keep the disclaimer in the README. Do not imply Eplan or Elgato endorsement.
6. **Positive tone toward Eplan and Elgato.** Present Stream Deck as one more way to build on an already excellent product. Never suggest Eplan is lacking or frame content as fixing or replacing Eplan features.
7. **Low-key branding.** A short "Maintained by Justin Walz, Walz Engineering" footer with one line inviting contact about custom work, plus file headers where relevant. No other sales pitches.
8. **English only.**
9. **Never `git push`, create remotes, or publish** without Justin's explicit OK in that conversation.
10. **Blog is separate.** The `blog/` folder is a separate PRIVATE repo and is git-ignored. Never commit it here.

## Profiles: public and private stay in step

There are two profile files built from the same buttons: the public one in `profiles/` (Eplan buttons only) and a private one in `_local/private/` (same Eplan buttons plus personal ones such as Spotify, audio switch, applause). **Every edit to the Eplan buttons or pages applies to both.** Personal buttons go in the private profile only. Page 2 is a macro-project-editing page (planned); it is added to both. The build helper lives in `_local/build_profiles.py` (git-ignored).

## Target

- Eplan Electric P8 2026 (installed at `C:\Program Files\EPLAN\Platform\2026.0.3\Bin`). Anything documented must be verified on that version; other versions are not mentioned.
- Elgato Stream Deck software on Windows. Record the software version a profile was exported from.

## Layout

```
profiles/   sanitized, importable profiles (+ a README per profile: pages, buttons, what each does)
icons/      original button icons (PNG/SVG)
docs/       guides: getting-started, shortcut-catalog, sanitizing-checklist, blog-and-videos
_local/     git-ignored scratch: unpacked backups, raw exports
```

## Conventions

- Each profile gets a folder-level README listing every page and button, the Eplan command it triggers, and any prerequisites (scripts to load, paths to edit).
- Mark anything not yet run in Eplan as **Draft** in the catalog until Justin has verified it. Never publish a Draft without his OK.
- Buttons that change project data must say so in their description and recommend trying a copy first.
- Use relative links; keep tables aligned and readable.
