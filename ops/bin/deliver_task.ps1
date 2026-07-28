# deliver_task.ps1 - hardened Sol/Luna delivery (2026-07-28, researcher ruling).
# Builds the wake message deterministically from the task-file path, so there is
# no free-text relay step that can garble the instruction (root cause of the
# task-69 misdelivery: only the session ID reached Sol as the message).
# Usage (commander runs this directly; do NOT delegate delivery to a subagent):
#   deliver_task.ps1 -TaskFile ops/inbox_codex/sol_task_NN_x.txt -ReplyFile sol/sol_reply_NN_x.md [-Role sol]
# Keep this file ASCII-only (PS 5.1 misparses UTF-8 without BOM).
param(
    [Parameter(Mandatory = $true)][string]$TaskFile,
    [Parameter(Mandatory = $true)][string]$ReplyFile,
    [ValidateSet("sol", "sol2", "luna")][string]$Role = "sol"
)
$root = "C:\Users\81905\Desktop\shadow-atelier"
$tf = Join-Path $root $TaskFile
if (-not (Test-Path $tf)) { Write-Output "FAIL-NO-TASKFILE: $tf"; exit 1 }
if ($ReplyFile -match "\s") { Write-Output "FAIL-REPLYFILE-HAS-SPACE: $ReplyFile"; exit 1 }
$msg = "Read $TaskFile and process the FULL mail (all numbered sections, first to last). Reply to $ReplyFile."
& "$root\ops\bin\launch_wake.ps1" wake $msg -Role $Role -ReplyFile (Join-Path $root $ReplyFile)
