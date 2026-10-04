$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    New-Item -ItemType Directory -Force '.build' | Out-Null
    foreach ($entry in @('main_en', 'main_zh')) {
        1..3 | ForEach-Object {
            & xelatex '-interaction=nonstopmode' '-halt-on-error' '-output-directory=.build' "$entry.tex"
            if ($LASTEXITCODE -ne 0) { throw "XeLaTeX failed: $entry" }
        }
        Copy-Item -LiteralPath ".build/$entry.pdf" -Destination "$entry.pdf"
    }
} finally { Pop-Location }
