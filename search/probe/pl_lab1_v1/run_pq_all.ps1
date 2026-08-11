# run_pq_all.ps1 -- run ANUPQ's pq.exe for the remaining PL-LAB-1 targets
$ErrorActionPreference = "Stop"
$env:PATH = "C:\Program Files\GAP-4.16.0\runtime\bin;" + $env:PATH
$pq = "C:\Program Files\GAP-4.16.0\runtime\opt\gap-4.16.0\pkg\anupq\pq.exe"

$targets = @("p5c5", "p5c6", "p7c6", "p7c7")

foreach ($t in $targets) {
    $setupFile = "search\probe\pl_lab1_v1\pq_setup_$t.txt"
    $logFile = "search\probe\pl_lab1_v1\pq_run_$t.log"
    Write-Output "=== running $t ==="
    Get-Content $setupFile | & $pq -i -k -g > $logFile 2>&1
    Write-Output "exit=$LASTEXITCODE"
    if (Test-Path "PQ_OUTPUT") {
        Move-Item -Force "PQ_OUTPUT" "search\probe\pl_lab1_v1\PQ_OUTPUT_$t.g"
        Write-Output "moved -> PQ_OUTPUT_$t.g"
    } else {
        Write-Output "WARNING: PQ_OUTPUT not found for $t"
    }
}
