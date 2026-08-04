#!/bin/sh
# search/probe/hsp7_cond4_laneP/driver_step2_run_pq.sh
# Lane P, HS 発火条件4較正走. Run ANUPQ's pq standalone on the SetupFile
# produced by driver_step1 (付録B env note: one-way stdin redirect, no
# interactive iostream). New driver, not copied from stage3/4.
export PATH="/c/Program Files/GAP-4.16.0/runtime/bin:$PATH"
PQEXE="/c/Program Files/GAP-4.16.0/runtime/opt/gap-4.16.0/pkg/anupq/pq.exe"
SETUP="search/probe/hsp7_cond4_laneP/pq_setup_Q_laneP.txt"
LOG="search/probe/hsp7_cond4_laneP/pq_run_Q_laneP.log"
"$PQEXE" -i -k -g < "$SETUP" > "$LOG" 2>&1
echo "exit=$?"
