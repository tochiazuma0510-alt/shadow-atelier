#!/bin/bash
set -u
cd /c/Users/81905/Desktop/shadow-atelier
LOGFILE="scratchpad/chir2_v1_orchestrator.log"
STATUS_FILE="scratchpad/chir2_v1_status.txt"

WINDOWS=(
  "1944 826"
  "1944 921"
)

for LINE in "${WINDOWS[@]}"; do
  ORDER=$(echo "$LINE" | awk '{print $1}')
  ID=$(echo "$LINE" | awk '{print $2}')
  PRELUDE="scratchpad/chir2_prelude_${ORDER}_${ID}.g"
  cat > "$PRELUDE" <<EOF
CHIR2_ORDER := ${ORDER};;
CHIR2_ID := ${ID};;
Read("search/probe/sg_band_sweep/sg_chir2_single_window_v1.g");
EOF
  echo "=== RETRY window (${ORDER},${ID}) ===" | tee -a "$LOGFILE"
  timeout 120 powershell.exe -NoProfile -File ./gap.ps1 "$PRELUDE" < /dev/null >> "$LOGFILE" 2>&1
  RC=$?
  if [ "$RC" -eq 124 ]; then
    echo "TIMEOUT_SKIPPED ${ORDER} ${ID} wall_cap_120s_exceeded_retry2" | tee -a "$STATUS_FILE"
    taskkill //F //IM gap.exe > /dev/null 2>&1
  elif [ "$RC" -ne 0 ]; then
    echo "COMPUTE_FAILED ${ORDER} ${ID} exit_code_${RC}_retry2" | tee -a "$STATUS_FILE"
  else
    echo "COMPLETED ${ORDER} ${ID}_retry2" | tee -a "$STATUS_FILE"
  fi
  rm -f "$PRELUDE"
done
echo "=== retry done ===" | tee -a "$LOGFILE"
