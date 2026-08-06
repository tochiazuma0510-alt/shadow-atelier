#!/bin/bash
# scratchpad/run_chir1_v2.sh
# Orchestrator: runs sg_chir1_single_window_v2.g once per window, in a
# SEPARATE gap.ps1 process each time, with a hard 120s wall-clock cap
# enforced externally via GNU `timeout` (a single synchronous GAP process
# cannot preempt its own blocking calls -- 司令塔 intervention instruction
# ②). Chiral windows first (instruction③). Records TIMEOUT_SKIPPED with a
# reason (never silently dropped, instruction②).
#
# bugfix (this run, 2nd occurrence): a `while read -u 3 ... done 3< file`
# loop -- even with the order-list moved off stdin -- still corrupted
# repeated powershell.exe/gap.exe subprocess spawns under Git-Bash/MSYS on
# this machine (Resolve-Path failures on every iteration, though a direct
# standalone call of the exact same command outside any loop worked in
# 1.5s). Root-caused by switching to a plain array + for-loop (no open
# extra file descriptors, no `read` builtin involved at all) -- confirmed
# working.
set -u
cd /c/Users/81905/Desktop/shadow-atelier

LOGFILE="scratchpad/chir1_v2_orchestrator.log"
> "$LOGFILE"
STATUS_FILE="scratchpad/chir1_v2_status.txt"
> "$STATUS_FILE"

mapfile -t LINES < scratchpad/chir1_order_list.txt

for LINE in "${LINES[@]}"; do
  ORDER=$(echo "$LINE" | awk '{print $1}')
  ID=$(echo "$LINE" | awk '{print $2}')
  case "$ORDER" in
    ''|*[!0-9]*) continue ;;   # skip non-numeric junk lines (e.g. stray debug output)
  esac
  case "$ID" in
    ''|*[!0-9]*) continue ;;
  esac
  PRELUDE="scratchpad/chir1_prelude_${ORDER}_${ID}.g"
  cat > "$PRELUDE" <<EOF
CHIR1_ORDER := ${ORDER};;
CHIR1_ID := ${ID};;
Read("search/probe/sg_band_sweep/sg_chir1_single_window_v2.g");
EOF
  echo "=== window (${ORDER},${ID}) ===" | tee -a "$LOGFILE"
  timeout 120 powershell.exe -NoProfile -File ./gap.ps1 "$PRELUDE" < /dev/null >> "$LOGFILE" 2>&1
  RC=$?
  if [ "$RC" -eq 124 ]; then
    echo "TIMEOUT_SKIPPED ${ORDER} ${ID} wall_cap_120s_exceeded" | tee -a "$STATUS_FILE"
    taskkill //F //IM gap.exe > /dev/null 2>&1
  elif [ "$RC" -ne 0 ]; then
    echo "COMPUTE_FAILED ${ORDER} ${ID} exit_code_${RC}" | tee -a "$STATUS_FILE"
  else
    echo "COMPLETED ${ORDER} ${ID}" | tee -a "$STATUS_FILE"
  fi
  rm -f "$PRELUDE"
done

echo "=== orchestrator done ===" | tee -a "$LOGFILE"
