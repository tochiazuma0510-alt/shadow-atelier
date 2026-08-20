#############################################################################
## Thin fail-closed same-job driver for the 157ed raw-lambda census.
#############################################################################

D972RLCQ3Driver := "search/d972_b345_q3_gha_driver_v1.g";;
D972RLCQ3DriverSHA :=
  "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831";;
D972RLCProducer := "search/d972_b345_triple_cube_raw_lambda_census_v1.py";;
D972RLCProducerSHA := "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db";;
D972RLCChecker := "search/check_d972_b345_triple_cube_raw_lambda_census_v1.py";;
D972RLCCheckerSHA := "677aa1b69e4415da9629c34fcf0e469ad974cf3c888be7e768635bac50f672ce";;
D972RLCQ3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972RLCQ3ArtifactSHA :=
  "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972RLCArtifact := "ci/out/d972_b345_triple_cube_raw_lambda_census_v1.json";;
D972RLCSelfLog := "ci/out/d972_b345_triple_cube_raw_lambda_census_v1_selftest.log";;
D972RLCSelfOk := "ci/out/d972_b345_triple_cube_raw_lambda_census_v1_selftest.ok";;
D972RLCProducerLog := "ci/out/d972_b345_triple_cube_raw_lambda_census_v1_producer.log";;
D972RLCCheckerLog := "ci/out/d972_b345_triple_cube_raw_lambda_census_v1_checker.log";;
D972RLCMathOk := "ci/out/d972_b345_triple_cube_raw_lambda_census_v1_math.ok";;
D972RLCTiming := "ci/out/d972_b345_triple_cube_raw_lambda_census_v1_timing.txt";;
D972RLCQ3Child := "ci/out/d972_b345_triple_cube_raw_lambda_census_v1_q3_child.g";;
D972RLCQ3Log := "ci/out/d972_b345_triple_cube_raw_lambda_census_v1_q3_child.log";;
D972RLCQ3Ok := "ci/out/d972_b345_triple_cube_raw_lambda_census_v1_q3_child.ok";;

D972RLCRequireSHA := function(path,expected)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157ed driver: missing source ",path); fi;
  got:=HexSHA256(raw);;
  if got<>expected then Error("157ed driver: source SHA drift ",path," got=",got); fi;
  return true;
end;;

D972RLCCount := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157ed driver: occurrence input");
  fi;
  n:=Length(text);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972RLCRead := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("157ed driver: missing ",label); fi;
  return raw;
end;;

D972RLCWrite := function(path,text)
  local stream,got;
  stream:=OutputTextFile(path,false);;
  if stream=fail then Error("157ed driver: child write open"); fi;
  SetPrintFormattingStatus(stream,false);; PrintTo(stream,text);; CloseStream(stream);;
  got:=StringFile(path);;
  if got=fail or got<>text then Error("157ed driver: child readback"); fi;
  return true;
end;;

D972RLCRequireSHA(D972RLCQ3Driver,D972RLCQ3DriverSHA);;
D972RLCRequireSHA(D972RLCProducer,D972RLCProducerSHA);;
D972RLCRequireSHA(D972RLCChecker,D972RLCCheckerSHA);;
if Length(D972RLCProducerSHA)<>64 or Length(D972RLCCheckerSHA)<>64 then
  Error("157ed driver: producer/checker SHA constants not frozen");
fi;

D972RLCSelf:=IsBound(D972_B345_TRIPLE_CUBE_RAW_LAMBDA_SELFTEST) and
  D972_B345_TRIPLE_CUBE_RAW_LAMBDA_SELFTEST=true;;
D972RLCRun:=IsBound(D972_B345_TRIPLE_CUBE_RAW_LAMBDA_RUN) and
  D972_B345_TRIPLE_CUBE_RAW_LAMBDA_RUN=true;;
if D972RLCSelf=D972RLCRun then
  Error("157ed driver: select exactly one mode");
fi;

if D972RLCSelf then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_selftest.log' 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_selftest.ok' && python3 -u -B search/d972_b345_triple_cube_raw_lambda_census_v1.py --self-test > 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_selftest.log' 2>&1 && python3 -u -B search/check_d972_b345_triple_cube_raw_lambda_census_v1.py --self-test >> 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_selftest.log' 2>&1 && printf '%s' 'D972_B345_TRIPLE_CUBE_RAW_LAMBDA_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_selftest.ok'");;
  if D972RLCRead(D972RLCSelfOk,"selftest sentinel")<>
     "D972_B345_TRIPLE_CUBE_RAW_LAMBDA_SELFTEST_EXIT_ZERO" then
    Error("157ed driver: selftest exit sentinel");
  fi;
  D972RLCSelfRaw:=D972RLCRead(D972RLCSelfLog,"selftest log");;
  if D972RLCCount(D972RLCSelfRaw,
       "D972_B345_TRIPLE_CUBE_RAW_LAMBDA_PRODUCER_SELFTEST_PASS")<>1 or
     D972RLCCount(D972RLCSelfRaw,
       "D972_B345_TRIPLE_CUBE_RAW_LAMBDA_CHECKER_SELFTEST_PASS")<>1 then
    Error("157ed driver: combined selftest markers");
  fi;
  Print(D972RLCSelfRaw,
    "\nB345_TRIPLE_CUBE_RAW_LAMBDA_GHA_DRIVER_PASS mode=selftest\n");;
else
  if not IsBound(D972_B345_TRIPLE_CUBE_RAW_LAMBDA_OUTPUT) or
     D972_B345_TRIPLE_CUBE_RAW_LAMBDA_OUTPUT<>D972RLCArtifact then
    Error("157ed driver: fixed output path required");
  fi;
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_q3_child.g' 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_q3_child.log' 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_q3_child.ok' 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1.json' 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_producer.log' 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_checker.log' 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_math.ok' 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_timing.txt'");;
  D972RLCQ3Text:=Concatenation(
    "if GAPInfo.Version<>\"4.16.0\" then Error(\"GAP 4.16.0 required\"); fi;;\n",
    "if LoadPackage(\"smallgrp\")<>true then Error(\"smallgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"autpgrp\")<>true then Error(\"autpgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"anupq\")<>true then Error(\"anupq LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"json\")<>true then Error(\"json LoadPackage failed\"); fi;;\n",
    "D972_B345_Q3_RUN:=true;; D972_B345_Q3_OUTPUT:=\"ci/out/d972_b345_q3_chief_v1.json\";;\n",
    "Read(\"search/d972_b345_q3_gha_driver_v1.g\");; QUIT_GAP(0);;\n");;
  D972RLCWrite(D972RLCQ3Child,D972RLCQ3Text);;
  Exec("bash -o pipefail -c 'gap -l \";/usr/share/gap;/usr/lib/gap;${GAP_P2_PACKAGE_ROOT:?}\" --quitonbreak -q -o 12g ci/out/d972_b345_triple_cube_raw_lambda_census_v1_q3_child.g 2>&1 | tee ci/out/d972_b345_triple_cube_raw_lambda_census_v1_q3_child.log' && printf '%s' 'D972_B345_TRIPLE_CUBE_RAW_LAMBDA_Q3_EXIT_ZERO' > 'ci/out/d972_b345_triple_cube_raw_lambda_census_v1_q3_child.ok'");;
  if D972RLCRead(D972RLCQ3Ok,"q3 sentinel")<>
     "D972_B345_TRIPLE_CUBE_RAW_LAMBDA_Q3_EXIT_ZERO" then
    Error("157ed driver: q3 child");
  fi;
  D972RLCQ3Raw:=D972RLCRead(D972RLCQ3Artifact,"q3 artifact");;
  if HexSHA256(D972RLCQ3Raw)<>D972RLCQ3ArtifactSHA then
    Error("157ed driver: q3 artifact SHA");
  fi;
  Exec("bash -o pipefail -c 'python3 -u -B search/check_d972_b345_q3_chief_v1.py ci/out/d972_b345_q3_chief_v1.json > ci/out/d972_b345_q3_checker_full.log 2>&1 && printf %s D972_B345_Q3_CHECKER_FULL_EXIT_ZERO > ci/out/d972_b345_q3_checker_full.ok'");;
  D972RLCQ3Check:=D972RLCRead("ci/out/d972_b345_q3_checker_full.log","q3 checker");;
  if D972RLCRead("ci/out/d972_b345_q3_checker_full.ok","q3 checker sentinel")<>
       "D972_B345_Q3_CHECKER_FULL_EXIT_ZERO" or
     D972RLCCount(D972RLCQ3Check,"B345_Q3_CHECKER_PASS")<>1 then
    Error("157ed driver: q3 independent checker");
  fi;
  Exec("bash -o pipefail -c 'set -e; SECONDS=0; python3 -u -B search/d972_b345_triple_cube_raw_lambda_census_v1.py ci/out/d972_b345_q3_chief_v1.json ci/out/d972_b345_triple_cube_raw_lambda_census_v1.json 18000 2>&1 | tee ci/out/d972_b345_triple_cube_raw_lambda_census_v1_producer.log; producer_elapsed=$SECONDS; remaining=$((18000-SECONDS)); if [ $remaining -le 0 ]; then exit 97; fi; python3 -u -B search/check_d972_b345_triple_cube_raw_lambda_census_v1.py ci/out/d972_b345_q3_chief_v1.json ci/out/d972_b345_triple_cube_raw_lambda_census_v1.json $remaining 2>&1 | tee ci/out/d972_b345_triple_cube_raw_lambda_census_v1_checker.log; final_elapsed=$SECONDS; final_remaining=$((18000-final_elapsed)); if [ $final_remaining -le 0 ]; then exit 98; fi; printf \"producer_elapsed=%s\\nchecker_initial_remaining=%s\\nfinal_elapsed=%s\\nfinal_margin=%s\\n\" $producer_elapsed $remaining $final_elapsed $final_remaining > ci/out/d972_b345_triple_cube_raw_lambda_census_v1_timing.txt; printf %s D972_B345_TRIPLE_CUBE_RAW_LAMBDA_MATH_EXIT_ZERO > ci/out/d972_b345_triple_cube_raw_lambda_census_v1_math.ok'");;
  if D972RLCRead(D972RLCMathOk,"math sentinel")<>
     "D972_B345_TRIPLE_CUBE_RAW_LAMBDA_MATH_EXIT_ZERO" then
    Error("157ed driver: producer/checker common process");
  fi;
  D972RLCProducerRaw:=D972RLCRead(D972RLCProducerLog,"producer log");;
  D972RLCTerminalCount:=0;;
  for token in ["B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE",
                "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT",
                "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE",
                "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT"] do
    D972RLCTerminalCount:=D972RLCTerminalCount+
      D972RLCCount(D972RLCProducerRaw,token);;
  od;
  if D972RLCTerminalCount<>1 or
     D972RLCCount(D972RLCProducerRaw,
       "D972_B345_TRIPLE_CUBE_RAW_LAMBDA_PRODUCER_EXIT_ZERO")<>1 then
    Error("157ed driver: producer terminal/exit markers");
  fi;
  D972RLCCheckerRaw:=D972RLCRead(D972RLCCheckerLog,"checker log");;
  if D972RLCCount(D972RLCCheckerRaw,
       "D972_B345_TRIPLE_CUBE_RAW_LAMBDA_CHECKER_PASS")<>1 then
    Error("157ed driver: checker PASS marker");
  fi;
  D972RLCTimingRaw:=D972RLCRead(D972RLCTiming,"common deadline timing");;
  if D972RLCCount(D972RLCTimingRaw,"producer_elapsed=")<>1 or
     D972RLCCount(D972RLCTimingRaw,"checker_initial_remaining=")<>1 or
     D972RLCCount(D972RLCTimingRaw,"final_margin=")<>1 then
    Error("157ed driver: common deadline ledger");
  fi;
  Print("B345_TRIPLE_CUBE_RAW_LAMBDA_GHA_DRIVER_PASS mode=full artifact_sha256=",
        HexSHA256(D972RLCRead(D972RLCArtifact,"final artifact")),"\n");;
fi;
