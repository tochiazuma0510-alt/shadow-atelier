# watch_artifact.ps1 - generic artifact-completion watcher (PS 5.1 compatible)
# Usage: powershell -NoProfile -File watch_artifact.ps1 -Paths <path1,path2,...> [-IntervalSec 10] [-TimeoutSec 3600]
# Polls target files until all exist and their mtimes are stable across two consecutive checks;
# prints "ARTIFACT-READY: <paths>" and exits 0, or "ARTIFACT-TIMEOUT" and exits 1 on timeout.

param(
    [Parameter(Mandatory = $true)]
    [string[]]$Paths,

    [int]$IntervalSec = 10,

    [int]$TimeoutSec = 3600
)

$startTime = Get-Date
$prevWriteTimes = @{}
foreach ($p in $Paths) { $prevWriteTimes[$p] = $null }

while ($true) {
    $elapsed = (Get-Date) - $startTime
    if ($elapsed.TotalSeconds -gt $TimeoutSec) {
        Write-Output "ARTIFACT-TIMEOUT"
        exit 1
    }

    $allExist = $true
    $allStable = $true
    $currentWriteTimes = @{}

    foreach ($p in $Paths) {
        if (-not (Test-Path -LiteralPath $p)) {
            $allExist = $false
            continue
        }
        $item = Get-Item -LiteralPath $p
        $currentWriteTimes[$p] = $item.LastWriteTimeUtc

        if ($null -eq $prevWriteTimes[$p]) {
            $allStable = $false
        }
        elseif ($prevWriteTimes[$p] -ne $currentWriteTimes[$p]) {
            $allStable = $false
        }
    }

    if ($allExist -and $allStable) {
        $joined = [string]::Join(", ", $Paths)
        Write-Output "ARTIFACT-READY: $joined"
        exit 0
    }

    if ($allExist) {
        foreach ($p in $Paths) { $prevWriteTimes[$p] = $currentWriteTimes[$p] }
    }
    else {
        foreach ($p in $Paths) { $prevWriteTimes[$p] = $null }
    }

    Start-Sleep -Seconds $IntervalSec
}
