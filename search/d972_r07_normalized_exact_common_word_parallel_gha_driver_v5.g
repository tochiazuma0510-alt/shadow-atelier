#############################################################################
## Task303 v5 fixed-dual process-parallel boundary-kernel SELFTEST driver.
## ASCII only. Production remains a sealed fail-closed adapter stop.
#############################################################################
D303Producer:="search/d972_r07_normalized_exact_common_word_parallel_v5.py";;
D303Checker:="crosscheck/check_d972_r07_normalized_exact_common_word_parallel_v5.py";;
D303Fixture:="search/certs/d972_r07_normalized_exact_common_word_parallel_selftest_v5_20260828.json";;
D303SelfReceipt:="ci/out/d972_r07_normalized_exact_common_word_parallel_v5.selftest.json";;
D303SelfVerdict:="ci/out/d972_r07_normalized_exact_common_word_parallel_v5.selftest.verdict.json";;
D303SelfLog:="ci/out/d972_r07_normalized_exact_common_word_parallel_v5.selftest.log";;
D303ProductionReceipt:="ci/out/d972_r07_normalized_exact_common_word_parallel_v5.production.json";;
D303ProductionVerdict:="ci/out/d972_r07_normalized_exact_common_word_parallel_v5.production.verdict.json";;
D303ProductionLog:="ci/out/d972_r07_normalized_exact_common_word_parallel_v5.production.log";;
D303Shell:="ci/out/d972_r07_normalized_exact_common_word_parallel_v5.sh";;
D303OK:="ci/out/d972_r07_normalized_exact_common_word_parallel_v5.ok";;
D303Sentinel:="R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_DRIVER_PASS";;
D303ProducerTerminal:="R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_PRODUCER_TERMINAL";;
D303CheckerTerminal:="R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_CHECKER_TERMINAL";;
D303SelftestMarker:="R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_SELFTEST_PASS";;
D303CheckerMarker:="R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_CHECKER_PASS";;

D303Current:=[
 [D303Producer,39234,"19a2970fcf072c25c606d0305fd999c8481353e0be20879de4be2aa26f6fb90c"],
 [D303Checker,32486,"530d67c854017a538fa2185b8bc5c48834a785f5bd6db38452db3551695cf1df"],
 [D303Fixture,1195,"4d481ba84e3c452c79f344e66a0eea5322ec8b64c15a81f1a290c22ce18e3fc9"]
];;
D303V3:=[
 ["search/d972_r07_normalized_exact_common_word_cached_v3.py",193704,"f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37"],
 ["crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py",154009,"dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10"],
 ["search/d972_r07_normalized_exact_common_word_cached_gha_driver_v3.g",11548,"2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d"],
 ["search/certs/d972_r07_normalized_exact_common_word_cached_selftest_v3_20260827.json",276,"c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12"]
];;

D303Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task303 missing input ",path); fi;
  return raw;
end;;

D303Pin:=function(row)
  local raw;
  raw:=D303Read(row[1]);;
  if Length(raw)<>row[2] or HexSHA256(raw)<>row[3] then
    Error("task303 pin drift ",row[1]);
  fi;
end;;

D303RejectFresh:=function(paths)
  local path;
  if Length(paths)<>Length(Set(paths)) then
    Error("task303 duplicate output path");
  fi;
  for path in paths do
    if IsExistingFile(path) then Error("task303 stale output ",path); fi;
  od;
end;;

for D303Row in Concatenation(D303V3,D303Current) do D303Pin(D303Row);; od;
D303RejectFresh([
  D303SelfReceipt,D303SelfVerdict,D303SelfLog,
  D303ProductionReceipt,D303ProductionVerdict,D303ProductionLog,
  D303Shell,D303OK
]);;

D303Mode:="SELFTEST";;
if IsBoundGlobal("GetEnv") and GetEnv("D303_MODE")<>fail and
   GetEnv("D303_MODE")<>"" then
  D303Mode:=GetEnv("D303_MODE");
fi;
if D303Mode<>"SELFTEST" and D303Mode<>"PRODUCTION" then
  Error("task303 invalid mode");
fi;

D303Stream:=OutputTextFile(D303Shell,false);;
if D303Stream=fail then Error("task303 shell open"); fi;
SetPrintFormattingStatus(D303Stream,false);;
PrintTo(D303Stream,
  "#!/usr/bin/env bash\n",
  "set -euo pipefail\n",
  "mkdir -p ci/out\n",
  "nproc_count=$(nproc)\n",
  "workers=$(( nproc_count < 4 ? nproc_count : 4 ))\n",
  "test \"$workers\" -ge 2\n",
  "test \"$workers\" -le 4\n",
  "printf 'TASK303_BOUNDARY_WORKERS %s\\n' \"$workers\" > ",D303SelfLog,"\n");

## SELFTEST producer and independent checker always run first.
PrintTo(D303Stream,
  "if ! python3 -u -B ",D303Producer,
  " --mode SELFTEST --fixture ",D303Fixture,
  " --boundary-workers \"$workers\" --output ",D303SelfReceipt,
  " >> ",D303SelfLog," 2>&1; then cat ",D303SelfLog,"; exit 1; fi\n");
PrintTo(D303Stream,
  "grep -Fxc '",D303SelftestMarker,"' ",D303SelfLog," | grep -qx 1\n",
  "test \"$(grep -c '^",D303ProducerTerminal," ' ",D303SelfLog,
  ")\" -eq 1\n",
  "grep -Fxc '",D303ProducerTerminal," PASS' ",D303SelfLog,
  " | grep -qx 1\n");
PrintTo(D303Stream,
  "if ! python3 -u -B ",D303Checker,
  " --mode SELFTEST --fixture ",D303Fixture,
  " --receipt ",D303SelfReceipt," --output ",D303SelfVerdict,
  " >> ",D303SelfLog," 2>&1; then cat ",D303SelfLog,"; exit 1; fi\n");
PrintTo(D303Stream,
  "grep -Fxc '",D303CheckerMarker,"' ",D303SelfLog," | grep -qx 1\n",
  "test \"$(grep -c '^",D303CheckerTerminal," ' ",D303SelfLog,
  ")\" -eq 1\n",
  "grep -Fxc '",D303CheckerTerminal," PASS' ",D303SelfLog,
  " | grep -qx 1\n",
  "self_producer_terminal=$(grep -E '^",D303ProducerTerminal,
  " ' ",D303SelfLog," | sed -E 's/^",D303ProducerTerminal," //')\n",
  "self_checker_terminal=$(grep -E '^",D303CheckerTerminal,
  " ' ",D303SelfLog," | sed -E 's/^",D303CheckerTerminal," //')\n",
  "test \"$self_producer_terminal\" = \"$self_checker_terminal\"\n",
  "test -s ",D303SelfReceipt," -a -s ",D303SelfVerdict,
  " -a -s ",D303SelfLog,"\n");

if D303Mode="PRODUCTION" then
  PrintTo(D303Stream,
    "test -n \"${D303_RESUME:-}\"\n",
    "case \"$D303_RESUME\" in ci/in/*) ;; *) exit 1 ;; esac\n",
    "case \"/$D303_RESUME/\" in */../*) exit 1 ;; esac\n",
    "test -f \"$D303_RESUME\"\n",
    "printf 'TASK303_BOUNDARY_WORKERS %s\\n' \"$workers\" > ",
    D303ProductionLog,"\n");
  PrintTo(D303Stream,
    "if ! python3 -u -B ",D303Producer,
    " --mode PRODUCTION --boundary-workers \"$workers\"",
    " --resume \"$D303_RESUME\" --output ",D303ProductionReceipt,
    " --seconds 19800 --boundary-pairs 8000000 --fibre-scans 80000000",
    " --candidate-words 2000000 --retained-columns 250000",
    " --checkpoint-bytes 4000000000 --rss-bytes 5700000000",
    " --oracle-rounds 1 >> ",D303ProductionLog,
    " 2>&1; then cat ",D303ProductionLog,"; exit 1; fi\n");
  PrintTo(D303Stream,
    "test \"$(grep -c '^",D303ProducerTerminal," ' ",D303ProductionLog,
    ")\" -eq 1\n",
    "grep -Fxc '",D303ProducerTerminal,
    " UNKNOWN_INPUT:resume_adapter_not_commissioned' ",
    D303ProductionLog," | grep -qx 1\n");
  PrintTo(D303Stream,
    "if ! python3 -u -B ",D303Checker,
    " --mode PRODUCTION --receipt ",D303ProductionReceipt,
    " --output ",D303ProductionVerdict," >> ",D303ProductionLog,
    " 2>&1; then cat ",D303ProductionLog,"; exit 1; fi\n");
  PrintTo(D303Stream,
    "test \"$(grep -c '^",D303CheckerTerminal," ' ",D303ProductionLog,
    ")\" -eq 1\n",
    "grep -Fxc '",D303CheckerTerminal,
    " UNKNOWN_INPUT:resume_adapter_not_commissioned' ",
    D303ProductionLog," | grep -qx 1\n",
    "production_producer_terminal=$(grep -E '^",D303ProducerTerminal,
    " ' ",D303ProductionLog," | sed -E 's/^",D303ProducerTerminal," //')\n",
    "production_checker_terminal=$(grep -E '^",D303CheckerTerminal,
    " ' ",D303ProductionLog," | sed -E 's/^",D303CheckerTerminal," //')\n",
    "test \"$production_producer_terminal\" = \"$production_checker_terminal\"\n",
    "test -s ",D303ProductionReceipt," -a -s ",D303ProductionVerdict,
    " -a -s ",D303ProductionLog,"\n");
fi;

PrintTo(D303Stream,
  "printf '%s' '",D303Sentinel,"' > ",D303OK,"\n",
  "test -s ",D303OK,"\n");
CloseStream(D303Stream);;

Exec(Concatenation("bash ",D303Shell));;
D303Observed:=D303Read(D303OK);;
if D303Observed<>D303Sentinel then
  Error("task303 sentinel mismatch");
fi;
Print(D303Sentinel," mode=",D303Mode,"\n");
