#!/bin/bash
set -u
cd /c/Users/81905/Desktop/shadow-atelier
LOGFILE="scratchpad/chir3_v1_orchestrator.log"
> "$LOGFILE"
STATUS_FILE="scratchpad/chir3_v1_status.txt"
> "$STATUS_FILE"

WINDOWS=(
  "1944 826"
  "1944 921"
)

for LINE in "${WINDOWS[@]}"; do
  ORDER=$(echo "$LINE" | awk '{print $1}')
  ID=$(echo "$LINE" | awk '{print $2}')
  PRELUDE="scratchpad/chir3_prelude_${ORDER}_${ID}.g"
  cat > "$PRELUDE" <<EOF
CHIR3_ORDER := ${ORDER};;
CHIR3_ID := ${ID};;
Read("search/probe/sg_band_sweep/sg_chir3_single_window_v1.g");
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
