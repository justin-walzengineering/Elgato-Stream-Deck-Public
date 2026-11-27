# Builds the download package (zip) for the Eplan Stream Deck project.
#
# The repository keeps the working files (full history, notes, tools). This script copies
# only what a user needs into Releases\EplanStreamDeck_v<version>_<date>\ , checks that no
# personal or company data slipped in, and zips the folder.
#
# Usage (from the repository root):
#   powershell -NoProfile -ExecutionPolicy Bypass -File release.ps1
#   powershell -NoProfile -ExecutionPolicy Bypass -File release.ps1 -Date 2026-12-01
#   powershell -NoProfile -ExecutionPolicy Bypass -File release.ps1 -OutRoot "$env:TEMP\test-release"
#
# It never uploads or publishes anything. Publishing the zip (for example as a GitHub release)
# is a separate step that only happens when the maintainer says so.
param(
    [string]$Date = (Get-Date -Format "yyyy-MM-dd"),
    [string]$OutRoot = ""
)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
if ($OutRoot -eq "") { $OutRoot = Join-Path $root "Releases" }

# ---------------------------------------------------------------- version checks
$version = (Get-Content (Join-Path $root "VERSION") -Raw).Trim()
if ($version -notmatch '^\d+\.\d+\.\d+$') { throw "VERSION must look like 1.0.0 (found '$version')" }

$scriptPath = Join-Path $root "scripts\ImportShortcutKeys.cs"
$scriptText = [System.IO.File]::ReadAllText($scriptPath)
$headerVersion = [regex]::Match($scriptText, '//\s*Version\s*:\s*([0-9.]+)').Groups[1].Value
$constVersion = [regex]::Match($scriptText, 'const string Version = "([0-9.]+)"').Groups[1].Value
if ($headerVersion -ne $version) { throw "Script header version '$headerVersion' does not match VERSION '$version'" }
if ($constVersion -ne $version) { throw "Script Version constant '$constVersion' does not match VERSION '$version'" }

$changelog = Get-Content (Join-Path $root "CHANGELOG.md") -Raw
if ($changelog -notmatch ("(?m)^## " + [regex]::Escape($version))) { throw "CHANGELOG.md has no section for $version" }

# ---------------------------------------------------------------- build the folder
$name = "EplanStreamDeck_v${version}_$Date"
$out = Join-Path $OutRoot $name
if (Test-Path $out) { Remove-Item $out -Recurse -Force }
New-Item -ItemType Directory -Path $out | Out-Null
foreach ($d in @("1_Eplan", "2_StreamDeck", "icons", "docs")) { New-Item -ItemType Directory -Path (Join-Path $out $d) | Out-Null }

Copy-Item $scriptPath (Join-Path $out "1_Eplan\ImportShortcutKeys.cs")
Copy-Item (Join-Path $root "eplan\ShortcutKeys_StreamDeck.xml") (Join-Path $out "1_Eplan\ShortcutKeys_StreamDeck.xml")
Copy-Item (Join-Path $root "profiles\Eplan-Shortcuts-StreamDeck-XL.streamDeckProfile") (Join-Path $out "2_StreamDeck\")
Copy-Item (Join-Path $root "icons\*.png") (Join-Path $out "icons\")
Copy-Item (Join-Path $root "LICENSE") (Join-Path $out "LICENSE.txt")
Copy-Item (Join-Path $root "CHANGELOG.md") (Join-Path $out "CHANGELOG.md")

# Word guide: built by tools\build_guide.py. It must carry the same version as VERSION.
$guide = Join-Path $root "release-files\Install_and_User_Guide.docx"
if (-not (Test-Path $guide)) { throw "release-files\Install_and_User_Guide.docx is missing. Run: python tools/build_guide.py" }
Add-Type -AssemblyName System.IO.Compression.FileSystem
$gz = [System.IO.Compression.ZipFile]::OpenRead($guide)
try {
    $footer = ($gz.Entries | Where-Object { $_.FullName -like "word/footer*.xml" } | ForEach-Object {
        $sr = New-Object System.IO.StreamReader($_.Open()); try { $sr.ReadToEnd() } finally { $sr.Dispose() } }) -join " "
} finally { $gz.Dispose() }
if ($footer -notmatch [regex]::Escape("Version $version")) { throw "Install_and_User_Guide.docx is for another version. Run: python tools/build_guide.py" }
Copy-Item $guide (Join-Path $out "Install_and_User_Guide.docx")

# Catalog: links to other repository files do not work inside the zip, so keep only the link text.
$catalog = [System.IO.File]::ReadAllText((Join-Path $root "docs\shortcut-catalog.md"))
$catalog = [regex]::Replace($catalog, '\[([^\]]+)\]\((?!https?:)[^)]+\)', '$1')
[System.IO.File]::WriteAllText((Join-Path $out "docs\Shortcut-Catalog.md"), $catalog, (New-Object System.Text.UTF8Encoding($true)))

$install = [System.IO.File]::ReadAllText((Join-Path $root "release-files\INSTALL.txt"))
$install = $install.Replace("{VERSION}", $version).Replace("{DATE}", $Date)
[System.IO.File]::WriteAllText((Join-Path $out "INSTALL.txt"), $install, (New-Object System.Text.UTF8Encoding($true)))

# ---------------------------------------------------------------- scrub check
# Anything that could identify a person, a company or a customer must not be in the package.
# Generic patterns live here. Personal names, company names and device serials live in the
# git-ignored file _local\scrub-patterns.txt (one regular expression per line, # for comments),
# so they never end up in the public repository.
$patterns = @(
    'C:\\Users\\(?!Public)',                    # a user profile path
    '\\\\[A-Za-z0-9_-]+\\[A-Za-z0-9$_-]+',      # a network share path
    'OneDrive',
    '[A-Za-z0-9._%+-]+@(?!walzengineering\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}'   # any e-mail address except the project one
)
$localList = Join-Path $root "_local\scrub-patterns.txt"
if (Test-Path $localList) {
    foreach ($line in Get-Content $localList) {
        $t = $line.Trim()
        if ($t -ne "" -and -not $t.StartsWith("#")) { $patterns += $t }
    }
    Write-Host ("Scrub check: " + $patterns.Count + " patterns (including your personal list).")
} else {
    Write-Host "WARNING: _local\scrub-patterns.txt not found. Only the generic patterns are checked; personal names are NOT." -ForegroundColor Yellow
}
$problems = @()
$textExt = @(".cs", ".xml", ".txt", ".md", ".json", ".ps1")
foreach ($f in Get-ChildItem $out -Recurse -File) {
    $ext = $f.Extension.ToLower()
    $blobs = @()
    if ($textExt -contains $ext) {
        $blobs += ,@($f.FullName, [System.IO.File]::ReadAllText($f.FullName))
    } elseif ($ext -eq ".streamdeckprofile") {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $zip = [System.IO.Compression.ZipFile]::OpenRead($f.FullName)
        try {
            foreach ($e in $zip.Entries) {
                if ($e.Length -eq 0) { continue }
                $sr = New-Object System.IO.StreamReader($e.Open(), [System.Text.Encoding]::UTF8)
                try { $blobs += ,@(($f.Name + " :: " + $e.FullName), $sr.ReadToEnd()) } finally { $sr.Dispose() }
            }
        } finally { $zip.Dispose() }
    } elseif ($ext -eq ".docx") {
        # A Word file is a zip: scan its XML parts as text and its pictures as bytes.
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $zip = [System.IO.Compression.ZipFile]::OpenRead($f.FullName)
        try {
            foreach ($e in $zip.Entries) {
                if ($e.Length -eq 0) { continue }
                $enc = if ($e.FullName -like "*.xml" -or $e.FullName -like "*.rels") { [System.Text.Encoding]::UTF8 } else { [System.Text.Encoding]::GetEncoding(28591) }
                $sr = New-Object System.IO.StreamReader($e.Open(), $enc)
                try { $blobs += ,@(($f.Name + " :: " + $e.FullName), $sr.ReadToEnd()) } finally { $sr.Dispose() }
            }
        } finally { $zip.Dispose() }
    } elseif ($ext -eq ".png") {
        # PNG files can carry text chunks; read the bytes as Latin-1 text and search them too.
        $blobs += ,@($f.FullName, [System.Text.Encoding]::GetEncoding(28591).GetString([System.IO.File]::ReadAllBytes($f.FullName)))
    }
    foreach ($b in $blobs) {
        foreach ($p in $patterns) {
            if ($b[1] -match $p) { $problems += ("LEFTOVER '" + $p + "' in " + $b[0]) }
        }
    }
}
# Nothing from the working folders may be in the package.
foreach ($bad in @("_local", ".git", "tools", "blog")) {
    if (Get-ChildItem $out -Recurse -Force | Where-Object { $_.FullName -like "*\$bad\*" -or $_.Name -eq $bad }) { $problems += "Working folder '$bad' is in the package" }
}
if ($problems.Count -gt 0) {
    $problems | ForEach-Object { Write-Host $_ -ForegroundColor Red }
    throw "Scrub check failed: $($problems.Count) problem(s). Nothing was zipped."
}
Write-Host "Scrub check passed." -ForegroundColor Green

# ---------------------------------------------------------------- zip
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zipPath = "$out.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
[System.IO.Compression.ZipFile]::CreateFromDirectory($out, $zipPath, [System.IO.Compression.CompressionLevel]::Optimal, $true)

Write-Host ""
Write-Host "Package folder: $out"
Write-Host "Zip file:       $zipPath"
Write-Host ("Size:           {0:N0} KB" -f ((Get-Item $zipPath).Length / 1KB))
Write-Host ("SHA-256:        " + (Get-FileHash $zipPath -Algorithm SHA256).Hash)
Write-Host ""
$outFull = (Get-Item $out).FullName
Get-ChildItem $out -Recurse -File | ForEach-Object { "  " + $_.FullName.Substring($outFull.Length + 1) }
