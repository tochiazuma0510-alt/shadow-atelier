# Live viewer for ops/codex_activity.log (Sol/Luna turn output).
# Usage:  ops\bin\watch_log.ps1            (opens in current console, Ctrl+C to quit)
# The commander opens it in a visible window via:
#   Start-Process powershell -ArgumentList '-NoExit','-ExecutionPolicy','Bypass','-File','ops\bin\watch_log.ps1'
# Keep this file ASCII-only (PS 5.1 encoding pitfall).
param([int]$Tail = 40)
$log = "C:\Users\81905\Desktop\shadow-atelier\ops\codex_activity.log"
if (-not (Test-Path $log)) { New-Item -ItemType File -Path $log | Out-Null }
try { [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false) } catch {}
$host.UI.RawUI.WindowTitle = "shadow-atelier codex log (live)"
Write-Host "=== watching ops/codex_activity.log (Ctrl+C de owari) ===" -ForegroundColor Cyan
Get-Content -LiteralPath $log -Wait -Tail $Tail -Encoding UTF8
