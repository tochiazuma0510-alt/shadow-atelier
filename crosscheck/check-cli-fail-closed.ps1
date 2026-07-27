# crosscheck/check-cli-fail-closed.ps1
# ASCII-only comments/strings (PowerShell 5.1 encoding pitfall with non-ASCII
# in .ps1 files -- see CLAUDE.md rule 1). Japanese design rationale for this
# fallback harness lives in crosscheck/check-cli-fail-closed.mjs (F2.2).
#
# Purpose: outer harness that exercises the same attacks as
# check-cli-fail-closed.mjs, for use when nested spawnSync inside node
# cannot capture child stdout in this Windows session (EPERM-like symptom).
# This script calls node directly (single level, no nested node-spawns-node)
# and reads $LASTEXITCODE, so it is a genuinely independent code path, not
# just a copy of the node harness.
#
# Run: powershell -File crosscheck/check-cli-fail-closed.ps1

$ROOT = Split-Path -Parent $PSScriptRoot
Set-Location $ROOT

$pass = 0
$fail = 0

function Report {
  param([string]$name, [bool]$ok, [string]$extra = '')
  if ($ok) {
    $script:pass++
    Write-Host "[PASS] $name  $extra"
  } else {
    $script:fail++
    Write-Host "[FAIL] $name  $extra"
  }
}

$tmpDir = Join-Path ([System.IO.Path]::GetTempPath()) ("k5-cli-fail-closed-ps-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null

try {
  # PowerShell 5.1's -Encoding utf8 writes a BOM, which node's JSON.parse
  # rejects (BOM-as-first-char SyntaxError) -- write BOM-less UTF-8 directly.
  $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  function Write-TextNoBom {
    param([string]$path, [string]$text)
    [System.IO.File]::WriteAllText($path, $text, $Utf8NoBom)
  }

  $nonJsonFile = Join-Path $tmpDir "non-json.txt"
  Write-TextNoBom $nonJsonFile 'this is not JSON {{{ unstructured text'

  $validNinfA = Join-Path $ROOT "certificates/k5pipeline/toy-ninf-M3-pathA.json"
  $validNinfB = Join-Path $ROOT "certificates/k5pipeline/toy-ninf-M3-pathB.json"
  $validNinfBundle = Join-Path $ROOT "certificates/k5pipeline/toy-ninf-M3-bundle.json"
  $validMainA = Join-Path $ROOT "certificates/k5pipeline/K3-regression-u-pathA.json"
  $validMainB = Join-Path $ROOT "certificates/k5pipeline/K3-regression-u-pathB.json"
  $validMainBundle = Join-Path $ROOT "certificates/k5fixture/K3-regression-model.json"

  # Clone a valid raw and mutate exactly one field to a malformed rational
  # literal (strict-parser attack), instead of a hand-built object with a
  # mismatched id (that older bug tripped id-mismatch before ever reaching
  # the rational parser).
  $badRationalNinfFile = Join-Path $tmpDir "bad-rational-ninf.json"
  $ninfObj = Get-Content $validNinfA -Raw | ConvertFrom-Json
  $ninfObj.chat = 'not-a-number'
  Write-TextNoBom $badRationalNinfFile ($ninfObj | ConvertTo-Json -Depth 10 -Compress)

  $badRationalMainFile = Join-Path $tmpDir "bad-rational-main.json"
  $mainObj = Get-Content $validMainA -Raw | ConvertFrom-Json
  $mainObj.u_pathA = '1/0'
  Write-TextNoBom $badRationalMainFile ($mainObj | ConvertTo-Json -Depth 10 -Compress)

  function Invoke-Checker {
    param([string]$scriptName, [string[]]$scriptArgs)
    # Use Start-Process with redirected files instead of native-command
    # 2>&1 (which wraps stderr lines in NativeCommandError records and can
    # trip $ErrorActionPreference='Stop' even on a clean nonzero exit).
    $scriptPath = Join-Path $ROOT "crosscheck\$scriptName"
    $outFile = [System.IO.Path]::GetTempFileName()
    $errFile = [System.IO.Path]::GetTempFileName()
    try {
      $allArgs = @($scriptPath) + $scriptArgs
      $proc = Start-Process -FilePath 'node' -ArgumentList $allArgs -NoNewWindow -Wait -PassThru `
        -RedirectStandardOutput $outFile -RedirectStandardError $errFile
      $stdoutText = Get-Content -Raw -Path $outFile -ErrorAction SilentlyContinue
      $stderrText = Get-Content -Raw -Path $errFile -ErrorAction SilentlyContinue
      if ($null -eq $stdoutText) { $stdoutText = '' }
      if ($null -eq $stderrText) { $stderrText = '' }
      return [PSCustomObject]@{ ExitCode = $proc.ExitCode; Stdout = $stdoutText; Stderr = $stderrText }
    } finally {
      Remove-Item -Path $outFile, $errFile -ErrorAction SilentlyContinue
    }
  }

  $r1 = Invoke-Checker 'u-compare-ninf.mjs' @($nonJsonFile, $validNinfB, $validNinfBundle)
  Report "non-JSON arg1: u-compare-ninf.mjs exits nonzero" ($r1.ExitCode -ne 0) "exit=$($r1.ExitCode)"
  Report "non-JSON arg1: u-compare-ninf.mjs stdout is empty" ($r1.Stdout.Trim().Length -eq 0) "len=$($r1.Stdout.Trim().Length)"
  Report "non-JSON arg1: u-compare-ninf.mjs stderr has INTEGRITY_STOP" ($r1.Stderr -match 'INTEGRITY_STOP') ""

  $r2 = Invoke-Checker 'u-compare.mjs' @($nonJsonFile, $validMainB, $validMainBundle)
  Report "non-JSON arg1: u-compare.mjs exits nonzero" ($r2.ExitCode -ne 0) "exit=$($r2.ExitCode)"
  Report "non-JSON arg1: u-compare.mjs stdout is empty" ($r2.Stdout.Trim().Length -eq 0) "len=$($r2.Stdout.Trim().Length)"
  Report "non-JSON arg1: u-compare.mjs stderr has INTEGRITY_STOP" ($r2.Stderr -match 'INTEGRITY_STOP') ""

  $rNinf = Invoke-Checker 'u-compare-ninf.mjs' @($badRationalNinfFile, $validNinfB, $validNinfBundle)
  Report "malformed rational: u-compare-ninf.mjs (chat) exits nonzero" ($rNinf.ExitCode -ne 0) "exit=$($rNinf.ExitCode)"
  $reachedNinf = $false
  try {
    $parsed = $rNinf.Stdout | ConvertFrom-Json
    $reachedNinf = ($parsed.result -eq 'INTEGRITY_STOP') -and ($parsed.reason -match 'strict rational parser')
  } catch {}
  Report "malformed rational: u-compare-ninf.mjs stop reason is strict-rational-parser gate" $reachedNinf ""

  $rMain = Invoke-Checker 'u-compare.mjs' @($badRationalMainFile, $validMainB, $validMainBundle)
  Report "malformed rational: u-compare.mjs (u_pathA=1/0) exits nonzero" ($rMain.ExitCode -ne 0) "exit=$($rMain.ExitCode)"
  $reachedMain = $false
  try {
    $parsed = $rMain.Stdout | ConvertFrom-Json
    $reachedMain = ($parsed.result -eq 'INTEGRITY_STOP') -and ($parsed.reason -match 'strict rational parser')
  } catch {}
  Report "malformed rational: u-compare.mjs stop reason is strict-rational-parser gate" $reachedMain ""

  $rSanityNinf = Invoke-Checker 'u-compare-ninf.mjs' @($validNinfA, $validNinfB, $validNinfBundle)
  $sanityNinfOk = ($rSanityNinf.ExitCode -eq 0) -and ($rSanityNinf.Stdout -match '"result":\s*"ACCEPT"')
  Report "sanity: u-compare-ninf.mjs valid input exits 0 with ACCEPT" $sanityNinfOk "exit=$($rSanityNinf.ExitCode)"

  $rSanityMain = Invoke-Checker 'u-compare.mjs' @($validMainA, $validMainB, $validMainBundle)
  $sanityMainOk = ($rSanityMain.ExitCode -eq 0) -and ($rSanityMain.Stdout -match '"result":\s*"ACCEPT"')
  Report "sanity: u-compare.mjs valid input exits 0 with ACCEPT" $sanityMainOk "exit=$($rSanityMain.ExitCode)"

} finally {
  Remove-Item -Recurse -Force -Path $tmpDir -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "=== $pass/$($pass + $fail) PASS ==="
if ($fail -gt 0) { exit 1 } else { exit 0 }
