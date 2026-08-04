#!/bin/sh
export PATH="/c/Program Files/GAP-4.16.0/runtime/bin:$PATH"
PQBIN="/c/Program Files/GAP-4.16.0/runtime/opt/gap-4.16.0/pkg/anupq/bin/x86_64-pc-cygwin-default64-kv11/pq.exe"
"$PQBIN" -i -k -g < search/probe/hsp7_cond4_laneS/pqsetup_P.txt > search/probe/hsp7_cond4_laneS/driver_step2_pqrun_P.log 2>&1
echo "exit=$?"
