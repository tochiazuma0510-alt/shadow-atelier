# run_pq_p5c4.ps1 -- run ANUPQ's pq.exe against the setup file (one-way stdin redirect)
$ErrorActionPreference = "Stop"
$env:PATH = "C:\Program Files\GAP-4.16.0\runtime\bin;" + $env:PATH
$pq = "C:\Program Files\GAP-4.16.0\runtime\opt\gap-4.16.0\pkg\anupq\pq.exe"
$setupFile = "search\probe\pl_lab1_v1\pq_setup_p5c4.txt"
$logFile = "search\probe\pl_lab1_v1\pq_run_p5c4.log"

Get-Content $setupFile | & $pq -i -k -g > $logFile 2>&1
Write-Output "exit=$LASTEXITCODE"

if (Test-Path "PQ_OUTPUT") {
    Move-Item -Force "PQ_OUTPUT" "search\probe\pl_lab1_v1\PQ_OUTPUT_p5c4.g"
    Write-Output "moved PQ_OUTPUT -> search\probe\pl_lab1_v1\PQ_OUTPUT_p5c4.g"
} else {
    Write-Output "WARNING: PQ_OUTPUT not found in cwd after pq.exe run"
}
