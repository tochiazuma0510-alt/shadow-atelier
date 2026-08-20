#############################################################################
## Thin fail-closed same-job driver for the 157eg full-D2 correlation lane.
#############################################################################

D972FDCProducer := "search/d972_b345_full_d2_dual_correlation_v1.py";;
D972FDCProducerSHA :=
  "6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52";;
D972FDCChecker := "search/check_d972_b345_full_d2_dual_correlation_v1.py";;
D972FDCCheckerSHA :=
  "311dc9413012542e489c9b2b7cd38e6008b81b6b8854e5e49d8d56285a457358";;
D972FDCTask := "sol/luna_task_157eg_b345_full_d2_dual_correlation.md";;
D972FDCTaskSHA :=
  "22b649c178ea1a821a5d67973b39c58f6a7395b6bc6a407a36a493f9ce19720e";;
D972FDCEDProducer := "search/d972_b345_triple_cube_raw_lambda_census_v1.py";;
D972FDCEDProducerSHA :=
  "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db";;
D972FDCEDChecker := "search/check_d972_b345_triple_cube_raw_lambda_census_v1.py";;
D972FDCEDCheckerSHA :=
  "677aa1b69e4415da9629c34fcf0e469ad974cf3c888be7e768635bac50f672ce";;
D972FDCEDDriver := "search/d972_b345_triple_cube_raw_lambda_census_gha_driver_v1.g";;
D972FDCEDDriverSHA :=
  "29a31752d42bd3f5a0e7f27ca38495bdd54c9cc694d12ddf9fe637e8749975e9";;
D972FDCEEProducer := "search/d972_b345_joint_kernel_qstar_closure_v1.py";;
D972FDCEEProducerSHA :=
  "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc";;
D972FDCEFChecker := "search/check_d972_b345_joint_kernel_qstar_closure_v2.py";;
D972FDCEFCheckerSHA :=
  "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88";;
D972FDCEFDriver := "search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g";;
D972FDCEFDriverSHA :=
  "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7";;
D972FDCPrefix := "search/d972_b345_seedspan_triple4_v1.py";;
D972FDCPrefixSHA :=
  "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29";;
D972FDCQ3Producer := "search/d972_b345_q3_chief_v1.g";;
D972FDCQ3ProducerSHA :=
  "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755";;
D972FDCQ3Checker := "search/check_d972_b345_q3_chief_v1.py";;
D972FDCQ3CheckerSHA :=
  "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73";;
D972FDCQ3Driver := "search/d972_b345_q3_gha_driver_v1.g";;
D972FDCQ3DriverSHA :=
  "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831";;

D972FDCQ3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972FDCQ3ArtifactSHA :=
  "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972FDCArtifact := "ci/out/d972_b345_full_d2_dual_correlation_v1.json";;
D972FDCSelfLog := "ci/out/d972_b345_full_d2_dual_correlation_v1_selftest.log";;
D972FDCSelfOk := "ci/out/d972_b345_full_d2_dual_correlation_v1_selftest.ok";;
D972FDCProducerLog := "ci/out/d972_b345_full_d2_dual_correlation_v1_producer.log";;
D972FDCCheckerLog := "ci/out/d972_b345_full_d2_dual_correlation_v1_checker.log";;
D972FDCMathOk := "ci/out/d972_b345_full_d2_dual_correlation_v1_math.ok";;
D972FDCTiming := "ci/out/d972_b345_full_d2_dual_correlation_v1_timing.txt";;
D972FDCQ3Child := "ci/out/d972_b345_full_d2_dual_correlation_v1_q3_child.g";;
D972FDCQ3Log := "ci/out/d972_b345_full_d2_dual_correlation_v1_q3_child.log";;
D972FDCQ3Ok := "ci/out/d972_b345_full_d2_dual_correlation_v1_q3_child.ok";;

D972FDCRead := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("157eg driver: missing ",label); fi;
  return raw;
end;;

D972FDCRequireSHA := function(path,expected)
  local raw,got;
  raw:=D972FDCRead(path,path);; got:=HexSHA256(raw);;
  if got<>expected then Error("157eg driver: SHA drift ",path," got=",got); fi;
  return true;
end;;

D972FDCCount := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157eg driver: occurrence input");
  fi;
  n:=Length(text);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972FDCWrite := function(path,text)
  local stream,got;
  stream:=OutputTextFile(path,false);;
  if stream=fail then Error("157eg driver: child write open"); fi;
  SetPrintFormattingStatus(stream,false);; PrintTo(stream,text);; CloseStream(stream);;
  got:=StringFile(path);;
  if got=fail or got<>text then Error("157eg driver: child readback"); fi;
  return true;
end;;

for D972FDCSource in [
  [D972FDCProducer,D972FDCProducerSHA],
  [D972FDCChecker,D972FDCCheckerSHA],
  [D972FDCTask,D972FDCTaskSHA],
  [D972FDCEDProducer,D972FDCEDProducerSHA],
  [D972FDCEDChecker,D972FDCEDCheckerSHA],
  [D972FDCEDDriver,D972FDCEDDriverSHA],
  [D972FDCEEProducer,D972FDCEEProducerSHA],
  [D972FDCEFChecker,D972FDCEFCheckerSHA],
  [D972FDCEFDriver,D972FDCEFDriverSHA],
  [D972FDCPrefix,D972FDCPrefixSHA],
  [D972FDCQ3Producer,D972FDCQ3ProducerSHA],
  [D972FDCQ3Checker,D972FDCQ3CheckerSHA],
  [D972FDCQ3Driver,D972FDCQ3DriverSHA]
] do
  D972FDCRequireSHA(D972FDCSource[1],D972FDCSource[2]);;
od;

D972FDCSelf:=IsBound(D972_B345_FULL_D2_DUAL_CORRELATION_SELFTEST) and
  D972_B345_FULL_D2_DUAL_CORRELATION_SELFTEST=true;;
D972FDCRun:=IsBound(D972_B345_FULL_D2_DUAL_CORRELATION_RUN) and
  D972_B345_FULL_D2_DUAL_CORRELATION_RUN=true;;
if D972FDCSelf=D972FDCRun then
  Error("157eg driver: select exactly one mode");
fi;

if D972FDCSelf then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_full_d2_dual_correlation_v1_selftest.log' 'ci/out/d972_b345_full_d2_dual_correlation_v1_selftest.ok' && python3 -u -B search/d972_b345_full_d2_dual_correlation_v1.py --self-test > 'ci/out/d972_b345_full_d2_dual_correlation_v1_selftest.log' 2>&1 && python3 -u -B search/check_d972_b345_full_d2_dual_correlation_v1.py --self-test >> 'ci/out/d972_b345_full_d2_dual_correlation_v1_selftest.log' 2>&1 && printf '%s' 'D972_B345_FULL_D2_DUAL_CORRELATION_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b345_full_d2_dual_correlation_v1_selftest.ok'");;
  if D972FDCRead(D972FDCSelfOk,"selftest sentinel")<>
       "D972_B345_FULL_D2_DUAL_CORRELATION_SELFTEST_EXIT_ZERO" then
    Error("157eg driver: selftest sentinel");
  fi;
  D972FDCSelfRaw:=D972FDCRead(D972FDCSelfLog,"selftest log");;
  if D972FDCCount(D972FDCSelfRaw,
       "D972_B345_FULL_D2_DUAL_CORRELATION_PRODUCER_SELFTEST_PASS")<>1 or
     D972FDCCount(D972FDCSelfRaw,
       "D972_B345_FULL_D2_DUAL_CORRELATION_CHECKER_SELFTEST_PASS")<>1 then
    Error("157eg driver: combined selftest markers");
  fi;
  Print(D972FDCSelfRaw,
    "\nB345_FULL_D2_DUAL_CORRELATION_GHA_DRIVER_PASS mode=selftest\n");;
else
  if not IsBound(D972_B345_FULL_D2_DUAL_CORRELATION_OUTPUT) or
     D972_B345_FULL_D2_DUAL_CORRELATION_OUTPUT<>D972FDCArtifact then
    Error("157eg driver: fixed output path required");
  fi;
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b345_full_d2_dual_correlation_v1_q3_child.g' 'ci/out/d972_b345_full_d2_dual_correlation_v1_q3_child.log' 'ci/out/d972_b345_full_d2_dual_correlation_v1_q3_child.ok' 'ci/out/d972_b345_full_d2_dual_correlation_v1.json' 'ci/out/d972_b345_full_d2_dual_correlation_v1_producer.log' 'ci/out/d972_b345_full_d2_dual_correlation_v1_checker.log' 'ci/out/d972_b345_full_d2_dual_correlation_v1_math.ok' 'ci/out/d972_b345_full_d2_dual_correlation_v1_timing.txt'");;
  D972FDCQ3Text:=Concatenation(
    "if GAPInfo.Version<>\"4.16.0\" then Error(\"GAP 4.16.0 required\"); fi;;\n",
    "if LoadPackage(\"smallgrp\")<>true then Error(\"smallgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"autpgrp\")<>true then Error(\"autpgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"anupq\")<>true then Error(\"anupq LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"json\")<>true then Error(\"json LoadPackage failed\"); fi;;\n",
    "D972_B345_Q3_RUN:=true;; D972_B345_Q3_OUTPUT:=\"ci/out/d972_b345_q3_chief_v1.json\";;\n",
    "Read(\"search/d972_b345_q3_gha_driver_v1.g\");; QUIT_GAP(0);;\n");;
  D972FDCWrite(D972FDCQ3Child,D972FDCQ3Text);;
  Exec("bash -o pipefail -c 'gap -l \";/usr/share/gap;/usr/lib/gap;${GAP_P2_PACKAGE_ROOT:?}\" --quitonbreak -q -o 12g ci/out/d972_b345_full_d2_dual_correlation_v1_q3_child.g 2>&1 | tee ci/out/d972_b345_full_d2_dual_correlation_v1_q3_child.log' && printf '%s' 'D972_B345_FULL_D2_DUAL_CORRELATION_Q3_EXIT_ZERO' > 'ci/out/d972_b345_full_d2_dual_correlation_v1_q3_child.ok'");;
  if D972FDCRead(D972FDCQ3Ok,"q3 sentinel")<>
       "D972_B345_FULL_D2_DUAL_CORRELATION_Q3_EXIT_ZERO" then
    Error("157eg driver: q3 child");
  fi;
  D972FDCQ3Raw:=D972FDCRead(D972FDCQ3Artifact,"q3 artifact");;
  if HexSHA256(D972FDCQ3Raw)<>D972FDCQ3ArtifactSHA then
    Error("157eg driver: q3 artifact SHA");
  fi;
  Exec("bash -o pipefail -c 'python3 -u -B search/check_d972_b345_q3_chief_v1.py ci/out/d972_b345_q3_chief_v1.json > ci/out/d972_b345_q3_checker_full.log 2>&1 && printf %s D972_B345_Q3_CHECKER_FULL_EXIT_ZERO > ci/out/d972_b345_q3_checker_full.ok'");;
  D972FDCQ3Check:=D972FDCRead("ci/out/d972_b345_q3_checker_full.log","q3 checker");;
  if D972FDCRead("ci/out/d972_b345_q3_checker_full.ok","q3 checker sentinel")<>
       "D972_B345_Q3_CHECKER_FULL_EXIT_ZERO" or
     D972FDCCount(D972FDCQ3Check,"B345_Q3_CHECKER_PASS")<>1 then
    Error("157eg driver: q3 independent checker");
  fi;
  Exec("bash -o pipefail -c 'set -e; SECONDS=0; python3 -u -B search/d972_b345_full_d2_dual_correlation_v1.py --q3 ci/out/d972_b345_q3_chief_v1.json --output ci/out/d972_b345_full_d2_dual_correlation_v1.json --seconds 18000 2>&1 | tee ci/out/d972_b345_full_d2_dual_correlation_v1_producer.log; producer_elapsed=$SECONDS; remaining=$((18000-SECONDS)); if [ $remaining -le 0 ]; then exit 97; fi; python3 -u -B search/check_d972_b345_full_d2_dual_correlation_v1.py --q3 ci/out/d972_b345_q3_chief_v1.json --receipt ci/out/d972_b345_full_d2_dual_correlation_v1.json --seconds $remaining 2>&1 | tee ci/out/d972_b345_full_d2_dual_correlation_v1_checker.log; final_elapsed=$SECONDS; final_remaining=$((18000-final_elapsed)); if [ $final_remaining -le 0 ]; then exit 98; fi; printf \"producer_elapsed=%s\\nchecker_initial_remaining=%s\\nfinal_elapsed=%s\\nfinal_margin=%s\\n\" $producer_elapsed $remaining $final_elapsed $final_remaining > ci/out/d972_b345_full_d2_dual_correlation_v1_timing.txt; printf %s D972_B345_FULL_D2_DUAL_CORRELATION_MATH_EXIT_ZERO > ci/out/d972_b345_full_d2_dual_correlation_v1_math.ok'");;
  if D972FDCRead(D972FDCMathOk,"math sentinel")<>
       "D972_B345_FULL_D2_DUAL_CORRELATION_MATH_EXIT_ZERO" then
    Error("157eg driver: producer/checker common process");
  fi;
  D972FDCProducerRaw:=D972FDCRead(D972FDCProducerLog,"producer log");;
  D972FDCTerminalCount:=0;;
  for D972FDCToken in ["B345_E4_FULL_D2_QSTAR_SEPARATOR",
      "B345_E4_FULL_D2_ACTIVE_TRANSLATION",
      "B345_E4_FULL_D2_UNKNOWN_RESOURCE",
      "B345_E4_FULL_D2_UNKNOWN_INPUT"] do
    D972FDCTerminalCount:=D972FDCTerminalCount+
      D972FDCCount(D972FDCProducerRaw,D972FDCToken);;
  od;
  if D972FDCTerminalCount<>1 or
     D972FDCCount(D972FDCProducerRaw,
       "D972_B345_FULL_D2_DUAL_CORRELATION_PRODUCER_PASS")<>1 then
    Error("157eg driver: producer terminal/exit markers");
  fi;
  D972FDCCheckerRaw:=D972FDCRead(D972FDCCheckerLog,"checker log");;
  if D972FDCCount(D972FDCCheckerRaw,
       "D972_B345_FULL_D2_DUAL_CORRELATION_CHECKER_PASS")<>1 then
    Error("157eg driver: checker PASS marker");
  fi;
  D972FDCTimingRaw:=D972FDCRead(D972FDCTiming,"common deadline timing");;
  if D972FDCCount(D972FDCTimingRaw,"producer_elapsed=")<>1 or
     D972FDCCount(D972FDCTimingRaw,"checker_initial_remaining=")<>1 or
     D972FDCCount(D972FDCTimingRaw,"final_margin=")<>1 then
    Error("157eg driver: common deadline ledger");
  fi;
  Print("B345_FULL_D2_DUAL_CORRELATION_GHA_DRIVER_PASS mode=full artifact_sha256=",
    HexSHA256(D972FDCRead(D972FDCArtifact,"final artifact")),"\n");;
fi;
