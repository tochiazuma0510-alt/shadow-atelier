# Live viewer for ops/codex_activity.log (Sol/Luna turn output) - v3 liveness.
# Launch in Windows Terminal (preferred - user directive 2026-07-18):
#   Start-Process wt.exe -ArgumentList 'new-tab','--title','"shadow-atelier codex log"','powershell','-NoExit','-ExecutionPolicy','Bypass','-File','C:\Users\81905\Desktop\shadow-atelier\ops\bin\watch_log.ps1'
# v3 (2026-07-26 tool inspection, case 3: "is it running or stalled?" asked twice):
#   the WINDOW TITLE now shows liveness, refreshed every StatusSec (default 5s):
#     codex log (main) | upd 12s ago | codex.exe ALIVE x1 [4321] | 18:04:59
#   - "upd Ns ago"  = seconds since the log file was last written
#   - codex.exe ALIVE xN [pids] / GONE = process existence (all lanes - with two
#     lanes tasklist cannot attribute a pid to a lane; use the per-lane log age)
#   Implementation note: Get-Content -Wait blocks, so v3 polls the file itself
#   (FileShare ReadWrite + stateful UTF8 decoder; partial lines are buffered,
#   multi-byte chars split across reads are handled by the decoder state).
#   Initial tail may rarely duplicate a line that lands during startup (benign).
#   Writer compatibility: production writers are node (libuv share R|W) - tested
#   live. PowerShell Add-Content to the SAME log fails with a sharing violation
#   while ANY viewer (v2 Get-Content -Wait or v3) holds its read handle - do not
#   write the activity logs from PowerShell (ops rule already: node writes them).
# -MaxSeconds N: self-exit after N seconds (0 = run forever; test hook).
# Mojibake note: chcp 65001 + UTF8 OutputEncoding together (either alone breaks
# on a cp932 console). Log file is UTF-8 (BOM at creation by wake scripts).
# Keep this file ASCII-only (PS 5.1 encoding pitfall).
param(
    [int]$Tail = 60,
    [string]$Log = "",
    [int]$StatusSec = 5,
    [int]$MaxSeconds = 0
)
$log = if ($Log) { $Log } else { "C:\Users\81905\Desktop\shadow-atelier\ops\codex_activity.log" }
$lane = if ($Log -match "sol2") { "sol2" } else { "main" }
if (-not (Test-Path -LiteralPath $log)) { New-Item -ItemType File -Path $log | Out-Null }
chcp 65001 | Out-Null
try { [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false) } catch {}
function Set-Title([string]$t) { try { $host.UI.RawUI.WindowTitle = $t } catch {} }
Set-Title "shadow-atelier codex log ($lane, starting...)"

function Show-LogLine([string]$line) {
    switch -Regex ($line) {
        '^=====\s*(WAKE|NEW-SESSION)' {
            Write-Host ""
            Write-Host $line -ForegroundColor Black -BackgroundColor Cyan
            break
        }
        '^-----\s*turn end' {
            Write-Host $line -ForegroundColor Black -BackgroundColor DarkCyan
            Write-Host ""
            break
        }
        '(ERROR|Error\b|error:|failed|FAILED|FAIL\b|refuted|ZOMBIE)' {
            Write-Host $line -ForegroundColor Red
            break
        }
        '(ALL PASSED|VERIFIED|\bPASS\b|SUCCESS)' {
            Write-Host $line -ForegroundColor Green
            break
        }
        '^(reason:|instr:|target:)' {
            Write-Host $line -ForegroundColor Yellow
            break
        }
        '^\s*(thinking|tokens used|exec\b|bash -lc|codex\b)' {
            Write-Host $line -ForegroundColor DarkGray
            break
        }
        default {
            Write-Host $line -ForegroundColor Gray
        }
    }
}
function Update-Title {
    $age = "?"
    try { $age = [int]((Get-Date) - (Get-Item -LiteralPath $log).LastWriteTime).TotalSeconds } catch {}
    $procs = @(Get-Process codex -ErrorAction SilentlyContinue)
    if ($procs.Count -gt 0) {
        $pids = ($procs | ForEach-Object { $_.Id }) -join ","
        $alive = "codex.exe ALIVE x$($procs.Count) [$pids]"
    } else {
        $alive = "codex.exe GONE"
    }
    Set-Title ("codex log ($lane) | upd ${age}s ago | $alive | " + (Get-Date -Format HH:mm:ss))
}

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  shadow-atelier : codex activity (live tail)"  -ForegroundColor Cyan
Write-Host "  quit: Ctrl+C    liveness: window title (5s)" -ForegroundColor DarkCyan
Write-Host "  file: $log" -ForegroundColor DarkCyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# initial tail, then stream from the snapshot offset
$startLen = (Get-Item -LiteralPath $log).Length
Get-Content -LiteralPath $log -Tail $Tail -Encoding UTF8 | ForEach-Object { Show-LogLine $_ }
$fs = [System.IO.File]::Open($log, [System.IO.FileMode]::Open,
    [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
[void]$fs.Seek($startLen, [System.IO.SeekOrigin]::Begin)
$decoder = [System.Text.Encoding]::UTF8.GetDecoder()   # stateful: survives split multi-byte chars
$carry = ""
$lastStatus = Get-Date "2000-01-01"
$t0 = Get-Date
try {
    while ($true) {
        if ($fs.Length -gt $fs.Position) {
            $buf = New-Object byte[] ($fs.Length - $fs.Position)
            $n = $fs.Read($buf, 0, $buf.Length)
            if ($n -gt 0) {
                $chars = New-Object char[] ($decoder.GetCharCount($buf, 0, $n))
                [void]$decoder.GetChars($buf, 0, $n, $chars, 0)
                $text = $carry + (New-Object string (,$chars))
                $parts = $text -split "`n", -1
                for ($i = 0; $i -lt $parts.Count - 1; $i++) {
                    Show-LogLine ($parts[$i].TrimEnd("`r"))
                }
                $carry = $parts[$parts.Count - 1]
            }
        } else {
            Start-Sleep -Milliseconds 700
        }
        if (((Get-Date) - $lastStatus).TotalSeconds -ge $StatusSec) {
            $lastStatus = Get-Date
            Update-Title
        }
        if ($MaxSeconds -gt 0 -and ((Get-Date) - $t0).TotalSeconds -ge $MaxSeconds) { break }
    }
} finally {
    $fs.Close()
}
