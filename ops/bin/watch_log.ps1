# Live viewer for ops/codex_activity.log (Sol/Luna turn output) - v2 readable.
# Launch in Windows Terminal (preferred - user directive 2026-07-18):
#   Start-Process wt.exe -ArgumentList 'new-tab','--title','"shadow-atelier codex log"','powershell','-NoExit','-ExecutionPolicy','Bypass','-File','C:\Users\81905\Desktop\shadow-atelier\ops\bin\watch_log.ps1'
# Mojibake note: chcp 65001 + UTF8 OutputEncoding together (either alone breaks
# on a cp932 console). Log file is UTF-8 (BOM at creation by wake scripts).
# Keep this file ASCII-only (PS 5.1 encoding pitfall).
param([int]$Tail = 60)
$log = "C:\Users\81905\Desktop\shadow-atelier\ops\codex_activity.log"
if (-not (Test-Path $log)) { New-Item -ItemType File -Path $log | Out-Null }
chcp 65001 | Out-Null
try { [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false) } catch {}
$host.UI.RawUI.WindowTitle = "shadow-atelier codex log (live)"
Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  shadow-atelier : codex activity (live tail)"  -ForegroundColor Cyan
Write-Host "  quit: Ctrl+C    file: ops/codex_activity.log" -ForegroundColor DarkCyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""
Get-Content -LiteralPath $log -Wait -Tail $Tail -Encoding UTF8 | ForEach-Object {
    $line = $_
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
