# GAP script runner (Windows / direct Cygwin runtime invocation).
# Usage:  .\gap.ps1 search\smoke-test.g
# Note: gap.bat opens a separate interactive window - never use it for automation.
# Keep this file ASCII-only: PS 5.1 misparses UTF-8 (no BOM) non-ASCII comments.
param(
    [Parameter(Mandatory = $true)][string]$ScriptPath,
    [string[]]$ExtraArgs = @()
)
$gapRoot = "C:\Program Files\GAP-4.16.0"
$env:PATH = "$gapRoot\runtime\bin;" + $env:PATH
& "$gapRoot\runtime\opt\gap-4.16.0\gap.exe" -q --quitonbreak @ExtraArgs (Resolve-Path $ScriptPath).Path
exit $LASTEXITCODE
