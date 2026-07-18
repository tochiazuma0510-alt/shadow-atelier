# Detach a codex launch/wake via Start-Process so the caller's tool session
# ending cannot take down the Codex turn. (Ported from atelier_lean/ES7/ops.)
# Usage:
#   powershell -File launch_wake.ps1 new  "instruction..."   # first launch (pins session id)
#   powershell -File launch_wake.ps1 wake "reason..."        # wake pinned session
# Keep this file ASCII-only (PS 5.1 misparses UTF-8 without BOM).
param(
    [Parameter(Mandatory = $true)][ValidateSet("new", "wake")][string]$Mode,
    [string]$Message = ""
)
$node = (Get-Command node).Source
$dir = "C:\Users\81905\Desktop\shadow-atelier\ops\bin"
$mjs = if ($Mode -eq "new") { "$dir\launch_new.mjs" } else { "$dir\wake_codex.mjs" }
$list = @($mjs)
if ($Message) { $list += $Message }
Start-Process -FilePath $node -ArgumentList $list -WindowStyle Hidden
Write-Output "LAUNCHED-$Mode-VIA-STARTPROCESS"
