# Detach a codex launch/wake via Start-Process so the caller's tool session
# ending cannot take down the Codex turn. (Ported from atelier_lean/ES7/ops.)
# Usage:
#   launch_wake.ps1 new  "instruction..."             # new Sol session (pins id)
#   launch_wake.ps1 new  "instruction..." -Role luna  # new Luna session (own pin)
#   launch_wake.ps1 new  "instruction..." -Renew      # new session for a new 便 (archives old pin)
#   launch_wake.ps1 wake "reason..." [-Role luna]     # wake pinned session (same-便 follow-up)
# Keep this file ASCII-only (PS 5.1 misparses UTF-8 without BOM).
param(
    [Parameter(Mandatory = $true)][ValidateSet("new", "wake")][string]$Mode,
    [string]$Message = "",
    [ValidateSet("sol", "sol2", "luna")][string]$Role = "sol",
    [ValidateSet("", "medium", "high", "xhigh")][string]$Effort = "",
    [switch]$Renew
)
# Reasoning-effort policy (user directive 2026-07-18): sol is pinned to max
# (no override); luna defaults to high, or medium (routine) / xhigh (Lean shards).
$node = (Get-Command node).Source
$dir = "C:\Users\81905\Desktop\shadow-atelier\ops\bin"
$mjs = if ($Mode -eq "new") { "$dir\launch_new.mjs" } else { "$dir\wake_codex.mjs" }
$list = @($mjs)
if ($Mode -eq "new" -and $Renew) { $list += "--renew" }
$list += @("--role", $Role)
if ($Effort) { $list += @("--effort", $Effort) }
if ($Message) { $list += $Message }
Start-Process -FilePath $node -ArgumentList $list -WindowStyle Hidden
Write-Output "LAUNCHED-$Mode-$Role-VIA-STARTPROCESS"
