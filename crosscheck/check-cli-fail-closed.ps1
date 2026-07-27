# crosscheck/check-cli-fail-closed.ps1
# ASCII-only comments/strings (PowerShell 5.1 encoding pitfall with non-ASCII
# in .ps1 files -- see CLAUDE.md rule 1). Japanese design rationale for this
# fallback harness lives in crosscheck/check-cli-fail-closed.mjs (F2.2).
#
# Purpose: outer harness that exercises the same attacks as
# check-cli-fail-closed.mjs, for use when nested spawnSync inside node
# cannot capture child stdout in this Windows session (EPERM-like symptom).
#
# Sol 42/ben41 F4.3 (launch blocker): the previous version used
# Start-Process with -RedirectStandardOutput/-RedirectStandardError. In the
# audited environment this threw a non-terminating error
# ("Start-Process: Item has already been added. Key in dictionary: 'Path'
# Key being added: 'PATH'") that was never caught, so Invoke-Checker's
# result object was never populated, Report() was never called for any of
# the 12 cases, and the script fell through to "=== 0/0 PASS ===" / exit 0.
# That is a false green: nothing was measured, yet the script reported
# success.
#
# Fix in this version:
#   1. Invoke-Checker no longer uses Start-Process. It calls node directly
#      via the call operator (&) with $LASTEXITCODE, wrapped in a
#      try/catch so ANY failure to launch the process (missing node, PATH
#      collisions, etc.) is caught and surfaces as a checker-level
#      ENV_FAIL for that case instead of silently producing an empty
#      result object.
#   2. At the end, the script asserts that exactly 12 cases were actually
#      classified (Pass + Fail). 0, 11, or 13 are all treated as ENV_FAIL
#      with a nonzero exit and a structured status line -- never silently
#      accepted as "nothing to report".
#   3. If node itself cannot be invoked at all in this session, the script
#      still reports ENV_FAIL with nonzero exit rather than 0/0 PASS.
#
# Run: powershell -File crosscheck/check-cli-fail-closed.ps1

$ROOT = Split-Path -Parent $PSScriptRoot
Set-Location $ROOT

# Expected number of classified (Pass+Fail) cases. See EXPECTED_CASES in
# check-cli-fail-closed.mjs -- kept in lockstep with that file's 12 cases.
$ExpectedCases = 12

$pass = 0
$fail = 0
$envFailCases = 0

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

function ReportEnvFailCase {
  param([string]$name, [string]$reason)
  $script:envFailCases++
  Write-Host "[ENV_FAIL] $name -- node could not be invoked in this session: $reason (this case is not counted as Pass or Fail -- unable to execute)"
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

  # Sol 42/ben41 F4.3 fix: no Start-Process. Call node directly via the call
  # operator inside a redirected-output block, and wrap the whole thing in
  # try/catch so a launch failure (missing node, PATH collision, etc.)
  # cannot silently fall through with an unpopulated result object -- it is
  # caught and returned as an explicit Ok=$false / EnvFail=$true record.
  function Invoke-Checker {
    param([string]$scriptName, [string[]]$scriptArgs)
    $scriptPath = Join-Path $ROOT "crosscheck\$scriptName"
    try {
      $stdoutLines = & node $scriptPath @scriptArgs 2>$null
      $exitCode = $LASTEXITCODE
      $stdoutText = if ($null -eq $stdoutLines) { '' } else { ($stdoutLines -join "`n") }
      # stderr is not separately captured here (native 2>&1 redirection in
      # PS 5.1 wraps stderr lines in NativeCommandError and can trip
      # $ErrorActionPreference -- see CLAUDE.md/tool notes). Re-invoke once
      # more with stderr captured via a temp file only when needed (below,
      # for the INTEGRITY_STOP-message checks) to avoid that pitfall on the
      # common path.
      return [PSCustomObject]@{ EnvFail = $false; ExitCode = $exitCode; Stdout = $stdoutText }
    } catch {
      # Stdout/Stderr are still present (empty string, not $null) on the
      # EnvFail branch so that callers building a diagnostic "extra" string
      # (e.g. "$($r.Stdout.Trim().Length)") do not themselves crash with a
      # null-reference error before ReportCheckerResult gets a chance to see
      # EnvFail=$true and skip the assertion. PowerShell evaluates all
      # argument expressions before a function call runs, so this matters.
      return [PSCustomObject]@{ EnvFail = $true; Reason = $_.Exception.Message; ExitCode = $null; Stdout = ''; Stderr = '' }
    }
  }

  # Separate helper that also captures stderr via redirected temp files (used
  # only for the cases that need to inspect stderr content), still avoiding
  # Start-Process.
  function Invoke-CheckerWithStderr {
    param([string]$scriptName, [string[]]$scriptArgs)
    $scriptPath = Join-Path $ROOT "crosscheck\$scriptName"
    $errFile = [System.IO.Path]::GetTempFileName()
    try {
      $stdoutLines = & node $scriptPath @scriptArgs 2>$errFile
      $exitCode = $LASTEXITCODE
      $stdoutText = if ($null -eq $stdoutLines) { '' } else { ($stdoutLines -join "`n") }
      $stderrText = Get-Content -Raw -Path $errFile -ErrorAction SilentlyContinue
      if ($null -eq $stderrText) { $stderrText = '' }
      return [PSCustomObject]@{ EnvFail = $false; ExitCode = $exitCode; Stdout = $stdoutText; Stderr = $stderrText }
    } catch {
      return [PSCustomObject]@{ EnvFail = $true; Reason = $_.Exception.Message; ExitCode = $null; Stdout = ''; Stderr = '' }
    } finally {
      Remove-Item -Path $errFile -ErrorAction SilentlyContinue
    }
  }

  function ReportCheckerResult {
    param([string]$name, [PSCustomObject]$r, [bool]$ok, [string]$extra = '')
    if ($r.EnvFail) {
      ReportEnvFailCase $name $r.Reason
    } else {
      Report $name $ok $extra
    }
  }

  $r1 = Invoke-CheckerWithStderr 'u-compare-ninf.mjs' @($nonJsonFile, $validNinfB, $validNinfBundle)
  ReportCheckerResult "non-JSON arg1: u-compare-ninf.mjs exits nonzero" $r1 ($r1.EnvFail -or $r1.ExitCode -ne 0) "exit=$($r1.ExitCode)"
  ReportCheckerResult "non-JSON arg1: u-compare-ninf.mjs stdout is empty" $r1 ($r1.EnvFail -or $r1.Stdout.Trim().Length -eq 0) "len=$($r1.Stdout.Trim().Length)"
  ReportCheckerResult "non-JSON arg1: u-compare-ninf.mjs stderr has INTEGRITY_STOP" $r1 ($r1.EnvFail -or $r1.Stderr -match 'INTEGRITY_STOP') ""

  $r2 = Invoke-CheckerWithStderr 'u-compare.mjs' @($nonJsonFile, $validMainB, $validMainBundle)
  ReportCheckerResult "non-JSON arg1: u-compare.mjs exits nonzero" $r2 ($r2.EnvFail -or $r2.ExitCode -ne 0) "exit=$($r2.ExitCode)"
  ReportCheckerResult "non-JSON arg1: u-compare.mjs stdout is empty" $r2 ($r2.EnvFail -or $r2.Stdout.Trim().Length -eq 0) "len=$($r2.Stdout.Trim().Length)"
  ReportCheckerResult "non-JSON arg1: u-compare.mjs stderr has INTEGRITY_STOP" $r2 ($r2.EnvFail -or $r2.Stderr -match 'INTEGRITY_STOP') ""

  $rNinf = Invoke-Checker 'u-compare-ninf.mjs' @($badRationalNinfFile, $validNinfB, $validNinfBundle)
  ReportCheckerResult "malformed rational: u-compare-ninf.mjs (chat) exits nonzero" $rNinf ($rNinf.EnvFail -or $rNinf.ExitCode -ne 0) "exit=$($rNinf.ExitCode)"
  $reachedNinf = $false
  if (-not $rNinf.EnvFail) {
    try {
      $parsed = $rNinf.Stdout | ConvertFrom-Json
      $reachedNinf = ($parsed.result -eq 'INTEGRITY_STOP') -and ($parsed.reason -match 'strict rational parser')
    } catch {}
  }
  ReportCheckerResult "malformed rational: u-compare-ninf.mjs stop reason is strict-rational-parser gate" $rNinf $reachedNinf ""

  $rMain = Invoke-Checker 'u-compare.mjs' @($badRationalMainFile, $validMainB, $validMainBundle)
  ReportCheckerResult "malformed rational: u-compare.mjs (u_pathA=1/0) exits nonzero" $rMain ($rMain.EnvFail -or $rMain.ExitCode -ne 0) "exit=$($rMain.ExitCode)"
  $reachedMain = $false
  if (-not $rMain.EnvFail) {
    try {
      $parsed = $rMain.Stdout | ConvertFrom-Json
      $reachedMain = ($parsed.result -eq 'INTEGRITY_STOP') -and ($parsed.reason -match 'strict rational parser')
    } catch {}
  }
  ReportCheckerResult "malformed rational: u-compare.mjs stop reason is strict-rational-parser gate" $rMain $reachedMain ""

  $rSanityNinf = Invoke-Checker 'u-compare-ninf.mjs' @($validNinfA, $validNinfB, $validNinfBundle)
  $sanityNinfOk = (-not $rSanityNinf.EnvFail) -and ($rSanityNinf.ExitCode -eq 0) -and ($rSanityNinf.Stdout -match '"result":\s*"ACCEPT"')
  ReportCheckerResult "sanity: u-compare-ninf.mjs valid input exits 0 with ACCEPT" $rSanityNinf $sanityNinfOk "exit=$($rSanityNinf.ExitCode)"

  $rSanityMain = Invoke-Checker 'u-compare.mjs' @($validMainA, $validMainB, $validMainBundle)
  $sanityMainOk = (-not $rSanityMain.EnvFail) -and ($rSanityMain.ExitCode -eq 0) -and ($rSanityMain.Stdout -match '"result":\s*"ACCEPT"')
  ReportCheckerResult "sanity: u-compare.mjs valid input exits 0 with ACCEPT" $rSanityMain $sanityMainOk "exit=$($rSanityMain.ExitCode)"

} finally {
  Remove-Item -Recurse -Force -Path $tmpDir -ErrorAction SilentlyContinue
}

Write-Host ""
$executed = $pass + $fail
Write-Host "=== $pass/$executed PASS ===$(if ($envFailCases -gt 0) { " ($envFailCases case(s) were ENV_FAIL -- node could not be invoked, not counted as Pass/Fail)" } else { '' })"

# Sol 42/ben41 F5.1: assert the executed (Pass+Fail) count is exactly the
# expected number of cases. 0, 11, 13, etc. are all false-green risks and
# must produce a structured ENV_FAIL with nonzero exit, not a silent
# "nothing to report" success.
if ($executed -ne $ExpectedCases) {
  $envFailJson = "{`"status`":`"ENV_FAIL`",`"reason`":`"executed case count ($executed) does not equal expected ($ExpectedCases) -- this harness measured nothing or an unexpected subset, and must not be reported as a passing calibration`",`"executed`":$executed,`"expected`":$ExpectedCases,`"pass`":$pass,`"fail`":$fail,`"envFailCases`":$envFailCases}"
  Write-Host $envFailJson
  exit 1
}
if ($fail -gt 0) { exit 1 } else { exit 0 }
