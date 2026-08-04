# driver_step2_run_pq.ps1 -- run ANUPQ's pq.exe against the setup file (one-way stdin
# redirect, per docs/notes/hsp7_cond4_lanespec_v1.md Appendix B environment note).
# ASCII-only comments (PS 5.1 encoding trap).
$ErrorActionPreference = "Stop"
$env:PATH = "C:\Program Files\GAP-4.16.0\runtime\bin;" + $env:PATH
$pq = "C:\Program Files\GAP-4.16.0\runtime\opt\gap-4.16.0\pkg\anupq\pq.exe"
$setupFile = "search\probe\hsp7_cond4_laneV\pqsetup_P.txt"
$logFile = "search\probe\hsp7_cond4_laneV\pq_run_P.log"

Get-Content $setupFile | & $pq -i -k -g > $logFile 2>&1
Write-Output "exit=$LASTEXITCODE"

# ANUPQ writes PQ_OUTPUT to the current working directory (per the setup file's own
# "output file" command, filename PQ_OUTPUT, not path-qualified there).
if (Test-Path "PQ_OUTPUT") {
    Move-Item -Force "PQ_OUTPUT" "search\probe\hsp7_cond4_laneV\PQ_OUTPUT_P.g"
    Write-Output "moved PQ_OUTPUT -> search\probe\hsp7_cond4_laneV\PQ_OUTPUT_P.g"
} else {
    Write-Output "WARNING: PQ_OUTPUT not found in cwd after pq.exe run"
}
