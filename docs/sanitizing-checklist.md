# Sanitizing checklist

Run this before **any** Stream Deck profile or backup is added to the repo.

## Workflow

1. Copy the backup or export to `_local/` (git-ignored). Never work inside `profiles/` on a raw file.
2. A `.streamDeckProfilesBackup` / `.streamDeckProfile` file is a zip archive. Unpack the copy in `_local/`.
3. Search every JSON manifest and text file for the items below.
4. Replace findings with generic placeholders, repack, and re-import into Stream Deck to confirm the profile still loads.
5. Review the result with Justin before it goes into `profiles/`.

## Search for

- Windows username and user-profile paths (`C:\Users\...`)
- Machine, domain and server names, UNC paths (`\\server\share`)
- Project, customer and company names; part numbers; drawing names
- Script paths and file names that reveal a client
- Email addresses, URLs with tokens, API keys, license info
- Button titles and icons (images) that show customer names or drawing content
- Plugin settings that store account data

## Placeholders

| Real | Use instead |
|------|-------------|
| User profile path | `C:\EplanScripts\` or `%USERPROFILE%` |
| Network paths | `C:\EplanShared\` |
| Project names | `ExampleProject` |

## Final check

- [ ] No `Users\<name>` strings remain
- [ ] No customer/project names remain (text and images)
- [ ] Profile imports and opens cleanly
- [ ] Profile README written; Draft/Verified status set
