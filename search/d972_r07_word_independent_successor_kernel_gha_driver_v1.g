#############################################################################
## R07 task232 serial driver. ASCII only; no workflow edit is required.
#############################################################################
if not IsBound(D232Mode) then Error("task232 MODE required"); fi;
if D232Mode<>"SELFTEST" and D232Mode<>"PRODUCTION" then Error("task232 MODE"); fi;
D232Producer:="search/d972_r07_word_independent_successor_kernel_v1.py";;
D232Checker:="crosscheck/check_d972_r07_word_independent_successor_kernel_v1.py";;
D232Fixture:="search/certs/d972_r07_word_independent_successor_kernel_selftest_v1_20260828.json";;
D232Receipt:="ci/out/d972_r07_word_independent_successor_kernel_v1.json";;
D232OK:="ci/out/d972_r07_word_independent_successor_kernel_v1.ok";;
D232PLog:="ci/out/d972_r07_word_independent_successor_kernel_v1.producer.log";;
D232CLog:="ci/out/d972_r07_word_independent_successor_kernel_v1.checker.log";;
D232Sh:="ci/out/d972_r07_word_independent_successor_kernel_v1.sh";;
D232Pins:=[[D232Producer,89086,"b2e9187f1efba6c55621ba3bacd24d4918701af289ce1037974135f7019165b0"],[D232Checker,55032,"68e86ac49c9a1adf76c26d046ab2bbd52376130ccdc007b8295d89c35cc32020"],[D232Fixture,720,"302c31244a43a86dd46d4a54e41756f067044f251db78b749c7bf70025fc85e7"]];;
D232Read:=function(path) local x; x:=StringFile(path); if x=fail or Length(x)=0 then Error("task232 missing ",path); fi; return x; end;;
D232Pin:=function(row) local x; x:=D232Read(row[1]); if Length(x)<>row[2] or HexSHA256(x)<>row[3] then Error("task232 pin drift ",row[1]); fi; end;;
for D232PinRow in D232Pins do D232Pin(D232PinRow); od;
if IsExistingFile(D232Receipt) or IsExistingFile(D232OK) or IsExistingFile(D232PLog) or IsExistingFile(D232CLog) or IsExistingFile(D232Sh) then Error("task232 stale output"); fi;
D232S:=OutputTextFile(D232Sh,false);; SetPrintFormattingStatus(D232S,false);;
PrintTo(D232S,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D232Mode="SELFTEST" then
  PrintTo(D232S,"if ! python3 -u -B ",D232Producer," --selftest --fixture ",D232Fixture," --output ",D232Receipt," > ",D232PLog," 2>&1; then cat ",D232PLog,"; exit 1; fi\ncat ",D232PLog,"\n");
  PrintTo(D232S,"test \"$(grep -Fxc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PRODUCER_SELFTEST_PASS' ",D232PLog,")\" -eq 1\n");
  PrintTo(D232S,"if ! python3 -u -B ",D232Checker," --selftest --fixture ",D232Fixture," --producer-receipt ",D232Receipt," > ",D232CLog," 2>&1; then cat ",D232CLog,"; exit 1; fi\ncat ",D232CLog,"\n");
  PrintTo(D232S,"grep -Fxc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_CHECKER_PASS terminal=SELFTEST_COMPLETE mutation_attempted=57 mutation_rejected=57' ",D232CLog," >/dev/null\n");
else
  PrintTo(D232S,"if ! python3 -u -B ",D232Producer," --output ",D232Receipt," > ",D232PLog," 2>&1; then cat ",D232PLog,"; exit 1; fi\ncat ",D232PLog,"\n");
  PrintTo(D232S,"if ! python3 -u -B ",D232Checker," --producer-receipt ",D232Receipt," > ",D232CLog," 2>&1; then cat ",D232CLog,"; exit 1; fi\ncat ",D232CLog,"\n");
  PrintTo(D232S,"D232_PRODUCER_TERMINAL=\"$(grep -E '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PRODUCER_TERMINAL (UNKNOWN_INPUT|UNKNOWN_RESOURCE|R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PASS)$' ",D232PLog," | tail -n 1 | sed 's/^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PRODUCER_TERMINAL //')\"\n");
  PrintTo(D232S,"D232_CHECKER_TERMINAL=\"$(grep -E '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_CHECKER_PASS terminal=(UNKNOWN_INPUT|UNKNOWN_RESOURCE|R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PASS)$' ",D232CLog," | tail -n 1 | sed 's/^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_CHECKER_PASS terminal=//')\"\n");
  PrintTo(D232S,"test -n \"$D232_PRODUCER_TERMINAL\" -a -n \"$D232_CHECKER_TERMINAL\"\n");
  PrintTo(D232S,"test \"$D232_PRODUCER_TERMINAL\" = \"$D232_CHECKER_TERMINAL\"\n");
fi;
PrintTo(D232S,"printf 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_OK\\n' > ",D232OK,"\ntest -s ",D232OK,"\n"); CloseStream(D232S);;
Exec("bash ci/out/d972_r07_word_independent_successor_kernel_v1.sh");
if not IsExistingFile(D232OK) then Error("task232 missing completion"); fi;
if D232Mode="SELFTEST" then Print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_DRIVER_PASS\\n"); else Print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_DRIVER_PASS\\n"); fi;
