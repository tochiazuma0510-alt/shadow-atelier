# turn_monitor.ps1 - lightweight per-turn death watch for codex turns (v1).
# Added 2026-07-26 tool inspection (commander order, case 2: sol2 OOM death went
# unnoticed for ~40+ min until the researcher saw it on screen).
#
# ---- SPEC ------------------------------------------------------------------
# Launched by: launch_wake.ps1 (one hidden monitor per launch/wake, both modes).
#   Manual run is fine too. Keep this file ASCII-only (PS 5.1 encoding pitfall).
# Watches:  the node wrapper process (launch_new.mjs / wake_codex.mjs) by PID.
#   Per-lane death detection uses the WRAPPER pid, not tasklist codex.exe,
#   because with two lanes tasklist cannot tell which codex.exe is which lane.
# Verdicts (checked once the wrapper pid is gone, after GraceSec):
#   NOTURN  - no "===== WAKE/NEW-SESSION(" marker appeared in the log region
#             from StartLen: the wrapper exited before starting a turn
#             (ENQUEUED / QUEUE-DUP / BAD-ROLE / NO-PINNED-SESSION...).
#             No alert - the [wake] lines in ops/wake_dispatch.log explain it.
#   OK      - a "----- turn end" marker exists after our turn marker AND
#             (no ReplyFile given, or it exists). Kicks wake_queue_drain.mjs
#             (this is how launch_new-initiated turns drain the queue) and exits.
#   ALERT(turndeath) - wrapper gone, NO turn-end marker: the turn died
#             (OOM / kill / crash). Writes an express note to ops/express/.
#   ALERT(noreply)   - turn ended normally but ReplyFile still missing.
#             Writes an express note (the "process gone AND reply not created"
#             condition from the commander order).
#   TIMEOUT - turn still running after MaxHours: monitor gives up silently
#             (dispatch-logged; no alert - long turns are not deaths).
# On ALERT the queue is deliberately NOT drained (the freed lane is left for
#   the commander's recovery wake; noted inside the express note).
# Express notes are picked up by the commander's resident express watch
# (10s polling, see docs/taisei "express box" section), closing the gap.
# Output: all verdicts appended to ops/wake_dispatch.log ([monitor] tag).
# Overhead: one hidden powershell sleeping PollSec - negligible on 8GB.
# Test hooks: -LogPath/-ExpressDir/-DispatchLog overrides (defaults = production).
# ----------------------------------------------------------------------------
param(
    [Parameter(Mandatory = $true)][int]$NodePid,
    [string]$Role = "sol",
    [string]$Mode = "wake",
    [string]$ReplyFile = "",
    [long]$StartLen = -1,
    [string]$LogPath = "",
    [string]$ExpressDir = "",
    [string]$DispatchLog = "",
    [int]$PollSec = 15,
    [int]$GraceSec = 20,
    [double]$MaxHours = 6.0
)
$repo = "C:\Users\81905\Desktop\shadow-atelier"
if (-not $LogPath) {
    if ($Role -eq "sol2") { $LogPath = "$repo\ops\codex_activity_sol2.log" }
    else { $LogPath = "$repo\ops\codex_activity.log" }
}
if (-not $ExpressDir) { $ExpressDir = "$repo\ops\express" }
if (-not $DispatchLog) { $DispatchLog = "$repo\ops\wake_dispatch.log" }

function Write-Dispatch([string]$msg) {
    $line = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ") + " [monitor] " + $msg
    try { Add-Content -LiteralPath $DispatchLog -Value $line -Encoding UTF8 } catch {}
}
function Read-LogRegion([string]$Path, [long]$FromByte) {
    if (-not (Test-Path -LiteralPath $Path)) { return "" }
    $fs = [System.IO.File]::Open($Path, [System.IO.FileMode]::Open,
        [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
    try {
        if ($FromByte -ge $fs.Length) { return "" }
        [void]$fs.Seek($FromByte, [System.IO.SeekOrigin]::Begin)
        $buf = New-Object byte[] ($fs.Length - $FromByte)
        $n = $fs.Read($buf, 0, $buf.Length)
        return [System.Text.Encoding]::UTF8.GetString($buf, 0, $n)
    } finally { $fs.Close() }
}
function Test-NodeAlive([int]$ProcId) {
    $p = Get-Process -Id $ProcId -ErrorAction SilentlyContinue
    if ($null -eq $p) { return $false }
    return ($p.ProcessName -eq "node")   # PID reuse defence
}

if ($StartLen -lt 0) {
    if (Test-Path -LiteralPath $LogPath) { $StartLen = (Get-Item -LiteralPath $LogPath).Length }
    else { $StartLen = 0 }
}
$t0 = Get-Date
Write-Dispatch "START role=$Role mode=$Mode nodePid=$NodePid startLen=$StartLen reply=$ReplyFile"

while ($true) {
    Start-Sleep -Seconds $PollSec
    if (((Get-Date) - $t0).TotalHours -ge $MaxHours) {
        Write-Dispatch "TIMEOUT role=$Role nodePid=$NodePid after ${MaxHours}h - monitor exits without verdict"
        exit 0
    }
    if (-not (Test-NodeAlive $NodePid)) { break }
}
Start-Sleep -Seconds $GraceSec

$region = Read-LogRegion $LogPath $StartLen
$region = $region.TrimStart([char]0xFEFF)   # BOM guard: a region starting at byte 0 begins with U+FEFF, which would defeat (?m)^
$m = [regex]::Match($region, '(?m)^===== (WAKE|NEW-SESSION)\(')
if (-not $m.Success) {
    Write-Dispatch "NOTURN role=$Role nodePid=$NodePid - wrapper exited without starting a turn (see [wake] lines) - no alert"
    exit 0
}
$after = $region.Substring($m.Index)
$turnEnded = [regex]::IsMatch($after, '(?m)^----- turn end')
$replyMissing = $false
if ($ReplyFile) { $replyMissing = -not (Test-Path -LiteralPath $ReplyFile) }

if ($turnEnded -and -not $replyMissing) {
    $rState = "n/a"
    if ($ReplyFile) { $rState = "present" }
    Write-Dispatch "OK role=$Role nodePid=$NodePid - turn ended normally (reply=$rState)"
    # turn-end hook for the wake queue (covers launch_new-initiated turns too)
    $drain = "$repo\ops\bin\wake_queue_drain.mjs"
    $queue = "$repo\ops\bin\wake_queue.jsonl"
    if ((Test-Path -LiteralPath $drain) -and (Test-Path -LiteralPath $queue)) {
        try {
            $nodeExe = (Get-Command node -ErrorAction Stop).Source
            Start-Process -FilePath $nodeExe -ArgumentList @($drain, "--from", "monitor($Role)") -WindowStyle Hidden
            Write-Dispatch "DRAIN-HOOK role=$Role - queue file exists, drain spawned"
        } catch { Write-Dispatch "DRAIN-HOOK-ERROR role=$Role - $($_.Exception.Message)" }
    }
    exit 0
}

# ---- ALERT path ----
$kind = "turndeath"
if ($turnEnded) { $kind = "noreply" }
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$note = Join-Path $ExpressDir ($stamp + "_monitor_" + $Role + "_" + $kind + ".md")
$lastWrite = "unknown"
if (Test-Path -LiteralPath $LogPath) {
    $lastWrite = (Get-Item -LiteralPath $LogPath).LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
}
$markerLine = ($after -split "`n")[0].TrimEnd("`r")
$replyState = "not specified"
if ($ReplyFile) {
    if ($replyMissing) { $replyState = "MISSING: $ReplyFile" } else { $replyState = "present: $ReplyFile" }
}
$verdictText = "turn DIED without a turn-end marker (OOM / kill / crash suspected)"
if ($kind -eq "noreply") { $verdictText = "turn ended normally but the expected reply file was NOT created" }
$detectedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$lines = @(
    "# express: turn monitor ALERT ($kind)",
    "",
    "- To: commander",
    "- Urgency: now",
    "- Lane/role: $Role (mode=$Mode, node wrapper pid=$NodePid)",
    "- Verdict: $verdictText",
    "- Turn marker: $markerLine",
    "- turn-end marker present: $turnEnded",
    "- Reply file: $replyState",
    "- Log last write: $lastWrite (log=$LogPath)",
    "- Detected: $detectedAt (grace ${GraceSec}s after wrapper exit)",
    "",
    "Suggested action: the session transcript survives - re-wake the pinned session",
    "with an explicit resume instruction (LEDGER 2026-07-26 sol2 OOM precedent).",
    "Wake queue was NOT auto-drained (lane left free for your recovery wake)."
)
try { $lines | Out-File -LiteralPath $note -Encoding utf8 } catch {}
Write-Dispatch "ALERT($kind) role=$Role nodePid=$NodePid note=$note"
exit 0
