# Detach a codex launch/wake via Start-Process so the caller's tool session
# ending cannot take down the Codex turn. (Ported from atelier_lean/ES7/ops.)
# Usage:
#   launch_wake.ps1 new  "instruction..."             # new Sol session (pins id)
#   launch_wake.ps1 new  "instruction..." -Role luna  # new Luna session (own pin)
#   launch_wake.ps1 new  "instruction..." -Renew      # new session for a new 便 (archives old pin)
#   launch_wake.ps1 wake "reason..." [-Role luna]     # wake pinned session (same-便 follow-up)
# Options added 2026-07-26 (tool inspection, case 2 - death watch standard kit):
#   -ReplyFile <path>  expected reply file for THIS turn; the monitor alerts if
#                      the process ends without creating it (no spaces in path).
#   -NoMonitor         skip starting turn_monitor.ps1 (tests / special ops).
# Every launch/wake now auto-starts ops/bin/turn_monitor.ps1 (hidden, per-turn):
#   process death without a turn-end marker (OOM etc.) or a missing ReplyFile
#   drops an express note into ops/express/ (picked up by the commander's
#   resident express watch). Verdicts go to ops/wake_dispatch.log.
# Keep this file ASCII-only (PS 5.1 misparses UTF-8 without BOM).
param(
    [Parameter(Mandatory = $true)][ValidateSet("new", "wake")][string]$Mode,
    [string]$Message = "",
    [ValidateSet("sol", "sol2", "luna")][string]$Role = "sol",
    [ValidateSet("", "medium", "high", "xhigh")][string]$Effort = "",
    [string]$ReplyFile = "",
    [switch]$NoMonitor,
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
# Snapshot the role log length BEFORE starting node, so the monitor's watch
# region is guaranteed to contain this turn's WAKE/NEW-SESSION marker.
if ($Role -eq "sol2") { $roleLog = "C:\Users\81905\Desktop\shadow-atelier\ops\codex_activity_sol2.log" }
else { $roleLog = "C:\Users\81905\Desktop\shadow-atelier\ops\codex_activity.log" }
$startLen = 0
if (Test-Path -LiteralPath $roleLog) { $startLen = (Get-Item -LiteralPath $roleLog).Length }
$p = Start-Process -FilePath $node -ArgumentList $list -WindowStyle Hidden -PassThru
$monInfo = "monitor=off"
if (-not $NoMonitor) {
    $monArgs = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "$dir\turn_monitor.ps1",
        "-NodePid", $p.Id, "-Role", $Role, "-Mode", $Mode, "-StartLen", $startLen)
    if ($ReplyFile) { $monArgs += @("-ReplyFile", ('"' + $ReplyFile + '"')) }
    Start-Process -FilePath "powershell.exe" -ArgumentList $monArgs -WindowStyle Hidden
    $monInfo = "monitor=on"
}
Write-Output "LAUNCHED-$Mode-$Role-VIA-STARTPROCESS pid=$($p.Id) $monInfo"
