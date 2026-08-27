#############################################################################
## Task193 serial SELFTEST/PRODUCTION/FIXTURE_GEN driver; ASCII only.
#############################################################################
if not IsBound(D193Mode) then Error("task193 MODE required"); fi;
if D193Mode<>"SELFTEST" and D193Mode<>"PRODUCTION" and D193Mode<>"FIXTURE_GEN" then Error("task193 MODE"); fi;
D193Producer:="search/d972_r07_second_frattini_affine_prefix_compiler_v1.py";;
D193Checker:="crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v1.py";;
D193Fixture:="search/certs/d972_r07_second_frattini_affine_prefix_compiler_selftest_v1_20260827.json";;
D193FixtureCandidate:="ci/out/d972_r07_second_frattini_affine_prefix_compiler_selftest_v1_candidate.json";;
D193Receipt:="ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.json";;
D193OK:="ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.ok";;
D193Task186Receipt:="ci/in/d972_r07_normalized_exact_common_word_colgen_v2.json";;
D193Task186Attestation:="ci/out/d972_r07_normalized_exact_common_word_colgen_v2.attestation";;
D193Task186Checker:="crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py";;
if not IsBound(D193Resume) then D193Resume:=""; fi;
D193ResumePath:="ci/in/d972_r07_second_frattini_affine_prefix_compiler_v1.checkpoint.json";;
D193ResumeArg:="";;
if D193Resume<>"" then if D193Resume<>D193ResumePath then Error("task193 unsafe resume path"); fi; D193ResumeArg:=Concatenation("--resume '",D193ResumePath,"'"); fi;
D193Pins:=[[D193Producer,37956,"7ec85fe5b359a371e7c7c6b701426c5521d2a9651f560cba0193fa9c34aa2530"],[D193Checker,33149,"278903c62c8f742cb985f44267f5f428c12dac9c514117f91eb6ae0daea17940"],[D193Fixture,545,"81bba2b13ecdb29b755a9d9b4e422955896ba66168a794d8c5b6a859fb328244"],[D193Task186Checker,54982,"8898798d0d6a9e0b6cd67402e74ba0dc5048b4797a0f7a9657e58d70d553c488"]];;
D193Read:=function(path) local x; x:=StringFile(path); if x=fail or Length(x)=0 then Error("task193 missing artifact ",path); fi; return x; end;;
D193Pin:=function(row) local x; x:=D193Read(row[1]); if Length(x)<>row[2] or HexSHA256(x)<>row[3] then Error("task193 pin drift ",row[1]); fi; end;;
D193CheckPins:=function() local row; for row in D193Pins do if D193Mode="FIXTURE_GEN" and row[1]=D193Fixture then continue; fi; D193Pin(row); od; end;;
D193CheckPins();
if D193Resume<>"" then D193Read(D193ResumePath); fi;
D193Reject:=function() local p; for p in [D193Receipt,D193OK,D193FixtureCandidate,D193Task186Attestation,"ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.sh","ci/out/d972_second_frattini_override.sh","ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log","ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log","ci/out/d972_r07_second_frattini_affine_prefix_compiler_fixture_gen.log"] do if IsExistingFile(p) then Error("task193 stale output ",p); fi; od; end;;
D193Reject();
D193S:=OutputTextFile("ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.sh",false);;
SetPrintFormattingStatus(D193S,false);;
PrintTo(D193S,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D193Mode="FIXTURE_GEN" then
  PrintTo(D193S,"task193_fixture_gen=1\n");
  PrintTo(D193S,"if ! python3 -u -B ",D193Producer," --selftest --fixture-output ",D193FixtureCandidate," --output ",D193Receipt," > ci/out/d972_r07_second_frattini_affine_prefix_compiler_fixture_gen.log 2>&1; then cat ci/out/d972_r07_second_frattini_affine_prefix_compiler_fixture_gen.log; exit 1; fi\ncat ci/out/d972_r07_second_frattini_affine_prefix_compiler_fixture_gen.log\ntest \"$(grep -Fxc 'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_PRODUCER_SELFTEST_PASS' ci/out/d972_r07_second_frattini_affine_prefix_compiler_fixture_gen.log)\" -eq 1\ntest -s ",D193FixtureCandidate,"\nprintf 'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_FIXTURE_GEN_PASS\\n' > ",D193OK,"\ntest \"$(cat ",D193OK,")\" = 'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_FIXTURE_GEN_PASS'\nexit 0\n");
elif D193Mode="SELFTEST" then
  PrintTo(D193S,"task193_selftest=1\n");
  PrintTo(D193S,"if ! python3 -u -B ",D193Producer," --selftest --output ",D193Receipt," > ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log 2>&1; then cat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log; exit 1; fi\ncat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log\n");
  PrintTo(D193S,"grep -Fxc 'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_PRODUCER_SELFTEST_PASS' ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log >/dev/null\n");
  PrintTo(D193S,"if ! python3 -u -B ",D193Checker," ",D193Receipt," --selftest > ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log 2>&1; then cat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log; exit 1; fi\ncat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log\n");
  PrintTo(D193S,"grep -Fxc 'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_CHECKER_PASS terminal=R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_SELFTEST_PASS' ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log >/dev/null\n");
else
  PrintTo(D193S,"task193_selftest=0\n");
  PrintTo(D193S,"if ! python3 -u -B ",D193Task186Checker," ",D193Task186Receipt," > ci/out/d972_r07_normalized_exact_common_word_colgen_v2.checker.log 2>&1; then cat ci/out/d972_r07_normalized_exact_common_word_colgen_v2.checker.log; exit 1; fi\ncat ci/out/d972_r07_normalized_exact_common_word_colgen_v2.checker.log\ntest \"$(wc -l < ci/out/d972_r07_normalized_exact_common_word_colgen_v2.checker.log)\" -eq 1\nIFS= read -r task186_line < ci/out/d972_r07_normalized_exact_common_word_colgen_v2.checker.log\ntest \"$task186_line\" = 'R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD'\nprintf '%s\\n' \"$task186_line\" > ",D193Task186Attestation,"\n");
  PrintTo(D193S,"if ! python3 -u -B ",D193Producer," --task186-receipt ",D193Task186Receipt," --task186-attestation ",D193Task186Attestation," --output ",D193Receipt," ",D193ResumeArg," > ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log 2>&1; then cat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log; exit 1; fi\ncat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log\ntest \"$(grep -Ec '^R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_PRODUCER_TERMINAL (R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1|UNKNOWN_INPUT:[^[:cntrl:]]+|UNKNOWN_RESOURCE:phase=[^:]+:cap=[^:]+:value=[0-9]+:limit=[0-9]+)$' ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log)\" -eq 1\n");
  PrintTo(D193S,"if ! python3 -u -B ",D193Checker," ",D193Receipt," > ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log 2>&1; then cat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log; exit 1; fi\ncat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log\ntest \"$(grep -Ec '^R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_CHECKER_PASS terminal=(R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1|UNKNOWN_INPUT:[^[:cntrl:]]+|UNKNOWN_RESOURCE:phase=[^:]+:cap=[^:]+:value=[0-9]+:limit=[0-9]+)$' ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log)\" -eq 1\n");
fi;
PrintTo(D193S,"producer_terminal=$(sed -n 's/^R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_PRODUCER_TERMINAL //p' ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log); checker_terminal=$(sed -n 's/^R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_CHECKER_PASS terminal=//p' ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log); test \"$producer_terminal\" = \"$checker_terminal\"\nprintf 'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_OK\\n' > ",D193OK,"\ntest \"$(cat ",D193OK,")\" = 'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_OK'\n"); CloseStream(D193S);;
if D193Mode="FIXTURE_GEN" then
  Exec("bash ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.sh");
elif D193Mode="SELFTEST" then
  D193S2:=OutputTextFile("ci/out/d972_second_frattini_override.sh",false);;
  SetPrintFormattingStatus(D193S2,false);;
  PrintTo(D193S2,"#!/usr/bin/env bash\nset -euo pipefail\n");
  PrintTo(D193S2,"if ! python3 -u -B ",D193Producer," --selftest --output ",D193Receipt," > ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log 2>&1; then cat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log; exit 1; fi\ncat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log\ngrep -Fxc 'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_PRODUCER_SELFTEST_PASS' ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.producer.log >/dev/null\nif ! python3 -u -B ",D193Checker," ",D193Receipt," --selftest > ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log 2>&1; then cat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log; exit 1; fi\ncat ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log\ngrep -Fxc 'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_CHECKER_PASS terminal=R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_SELFTEST_PASS' ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.checker.log >/dev/null\nprintf 'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_OK\\n' > ",D193OK,"\ntest -s ",D193OK,"\n"); CloseStream(D193S2);;
  Exec("bash ci/out/d972_second_frattini_override.sh");
else
  Exec("bash ci/out/d972_r07_second_frattini_affine_prefix_compiler_v1.sh");
fi;
if not IsExistingFile(D193OK) then Error("task193 missing completion"); fi;
if D193Mode="FIXTURE_GEN" then Print("R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_FIXTURE_GEN_DRIVER_PASS\n"); else Print("R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1_DRIVER_PASS\n"); fi;
