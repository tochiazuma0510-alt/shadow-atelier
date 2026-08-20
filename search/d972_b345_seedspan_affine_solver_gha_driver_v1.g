#############################################################################
## d972_b345_seedspan_affine_solver_gha_driver_v1.g
## Thin fail-closed same-job driver for the 157eb raw-Fox affine lane.
#############################################################################

D972AFFQ3Driver := "search/d972_b345_q3_gha_driver_v1.g";;
D972AFFQ3DriverSHA :=
  "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831";;
D972AFFProducer := "search/d972_b345_seedspan_affine_solver_v1.py";;
D972AFFProducerSHA := "804414e69155f2b8d9aa2a2412b0120d64eb373945a0fa6163f1214b4673e19a";;
D972AFFChecker := "search/check_d972_b345_seedspan_affine_solver_v1.py";;
D972AFFCheckerSHA := "67ad8d8227f1a8a60e481977fd2d07d819d532deb2651cd28667db997ec46081";;
D972AFFQ3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972AFFQ3ArtifactSHA :=
  "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972AFFArtifact := "ci/out/d972_b345_seedspan_affine_v1.json";;
D972AFFSelfLog := "ci/out/d972_b345_seedspan_affine_v1_selftest.log";;
D972AFFSelfOk := "ci/out/d972_b345_seedspan_affine_v1_selftest.ok";;
D972AFFProducerLog := "ci/out/d972_b345_seedspan_affine_v1_producer.log";;
D972AFFProducerOk := "ci/out/d972_b345_seedspan_affine_v1_producer.ok";;
D972AFFCheckerLog := "ci/out/d972_b345_seedspan_affine_v1_checker.log";;
D972AFFCheckerOk := "ci/out/d972_b345_seedspan_affine_v1_checker.ok";;
D972AFFQ3Child := "ci/out/d972_b345_seedspan_affine_v1_q3_child.g";;
D972AFFQ3Log := "ci/out/d972_b345_seedspan_affine_v1_q3_child.log";;
D972AFFQ3Ok := "ci/out/d972_b345_seedspan_affine_v1_q3_child.ok";;
D972AFFSelfSentinel := "D972_B345_SEEDSPAN_AFFINE_SELFTEST_EXIT_ZERO";;
D972AFFProducerSentinel := "D972_B345_SEEDSPAN_AFFINE_PRODUCER_EXIT_ZERO";;
D972AFFCheckerSentinel := "D972_B345_SEEDSPAN_AFFINE_CHECKER_EXIT_ZERO";;
D972AFFQ3Sentinel := "D972_B345_SEEDSPAN_AFFINE_Q3_CHILD_EXIT_ZERO";;

D972AFFRequireSHA := function(path,expected)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157eb driver: missing source ",path); fi;
  got:=HexSHA256(raw);;
  if got<>expected then Error("157eb driver: source SHA drift ",path," got=",got); fi;
  return true;
end;;

D972AFFCount := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157eb driver: occurrence input");
  fi;
  n:=Length(text);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972AFFRead := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("157eb driver: missing ",label); fi;
  return raw;
end;;

D972AFFWrite := function(path,text)
  local stream,got;
  stream:=OutputTextFile(path,false);;
  if stream=fail then Error("157eb driver: child write open"); fi;
  SetPrintFormattingStatus(stream,false);; PrintTo(stream,text);; CloseStream(stream);;
  got:=StringFile(path);;
  if got=fail or got<>text then Error("157eb driver: child readback"); fi;
  return true;
end;;

D972AFFRequireSHA(D972AFFQ3Driver,D972AFFQ3DriverSHA);;
D972AFFRequireSHA(D972AFFProducer,D972AFFProducerSHA);;
D972AFFRequireSHA(D972AFFChecker,D972AFFCheckerSHA);;
if Length(D972AFFProducerSHA)<>64 or Length(D972AFFCheckerSHA)<>64 then
  Error("157eb driver: producer/checker SHA constants not frozen");
fi;

D972AFFSelf:=IsBound(D972_B345_SEEDSPAN_AFFINE_SELFTEST) and
  D972_B345_SEEDSPAN_AFFINE_SELFTEST=true;;
D972AFFRun:=IsBound(D972_B345_SEEDSPAN_AFFINE_RUN) and
  D972_B345_SEEDSPAN_AFFINE_RUN=true;;
if D972AFFSelf=D972AFFRun then
  Error("157eb driver: select exactly one of SELFTEST and RUN");
fi;

if D972AFFSelf then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_seedspan_affine_v1_selftest.log' 'ci/out/d972_b345_seedspan_affine_v1_selftest.ok' && python3 -u -B search/d972_b345_seedspan_affine_solver_v1.py --self-test > 'ci/out/d972_b345_seedspan_affine_v1_selftest.log' 2>&1 && python3 -u -B search/check_d972_b345_seedspan_affine_solver_v1.py --self-test >> 'ci/out/d972_b345_seedspan_affine_v1_selftest.log' 2>&1 && printf '%s' 'D972_B345_SEEDSPAN_AFFINE_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b345_seedspan_affine_v1_selftest.ok' ");;
  if D972AFFRead(D972AFFSelfOk,"selftest sentinel")<>D972AFFSelfSentinel then
    Error("157eb driver: selftest exit sentinel");
  fi;
  D972AFFSelfRaw:=D972AFFRead(D972AFFSelfLog,"selftest log");;
  if D972AFFCount(D972AFFSelfRaw,"D972_B345_SEEDSPAN_AFFINE_PRODUCER_SELFTEST_PASS")<>1 or
     D972AFFCount(D972AFFSelfRaw,"D972_B345_SEEDSPAN_AFFINE_CHECKER_SELFTEST_PASS")<>1 then
    Error("157eb driver: combined selftest markers");
  fi;
  Print(D972AFFSelfRaw,"\nB345_SEEDSPAN_AFFINE_GHA_DRIVER_PASS mode=selftest\n");;
else
  if not IsBound(D972_B345_SEEDSPAN_AFFINE_OUTPUT) or
     D972_B345_SEEDSPAN_AFFINE_OUTPUT<>D972AFFArtifact then
    Error("157eb driver: fixed affine output path required");
  fi;
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b345_seedspan_affine_v1_q3_child.g' 'ci/out/d972_b345_seedspan_affine_v1_q3_child.log' 'ci/out/d972_b345_seedspan_affine_v1_q3_child.ok' 'ci/out/d972_b345_seedspan_affine_v1.json' 'ci/out/d972_b345_seedspan_affine_v1_producer.log' 'ci/out/d972_b345_seedspan_affine_v1_producer.ok' 'ci/out/d972_b345_seedspan_affine_v1_checker.log' 'ci/out/d972_b345_seedspan_affine_v1_checker.ok'");;
  D972AFFQ3Text:=Concatenation(
    "if GAPInfo.Version<>\"4.16.0\" then Error(\"GAP 4.16.0 required\"); fi;;\n",
    "if LoadPackage(\"smallgrp\")<>true then Error(\"smallgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"autpgrp\")<>true then Error(\"autpgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"anupq\")<>true then Error(\"anupq LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"json\")<>true then Error(\"json LoadPackage failed\"); fi;;\n",
    "D972_B345_Q3_RUN:=true;; D972_B345_Q3_OUTPUT:=\"ci/out/d972_b345_q3_chief_v1.json\";;\n",
    "Read(\"search/d972_b345_q3_gha_driver_v1.g\");; QUIT_GAP(0);;\n");;
  D972AFFWrite(D972AFFQ3Child,D972AFFQ3Text);;
  Exec("bash -o pipefail -c 'gap -l \";/usr/share/gap;/usr/lib/gap;${GAP_P2_PACKAGE_ROOT:?}\" --quitonbreak -q -o 12g ci/out/d972_b345_seedspan_affine_v1_q3_child.g 2>&1 | tee ci/out/d972_b345_seedspan_affine_v1_q3_child.log' && printf '%s' 'D972_B345_SEEDSPAN_AFFINE_Q3_CHILD_EXIT_ZERO' > 'ci/out/d972_b345_seedspan_affine_v1_q3_child.ok'");;
  if D972AFFRead(D972AFFQ3Ok,"q3 sentinel")<>D972AFFQ3Sentinel then Error("157eb driver: q3 child"); fi;
  D972AFFQ3Raw:=D972AFFRead(D972AFFQ3Artifact,"q3 artifact");;
  if HexSHA256(D972AFFQ3Raw)<>D972AFFQ3ArtifactSHA then Error("157eb driver: q3 artifact SHA"); fi;
  Exec("bash -o pipefail -c 'python3 -u -B search/check_d972_b345_q3_chief_v1.py ci/out/d972_b345_q3_chief_v1.json > ci/out/d972_b345_q3_checker_full.log 2>&1 && printf '%s' 'D972_B345_Q3_CHECKER_FULL_EXIT_ZERO' > ci/out/d972_b345_q3_checker_full.ok'");;
  D972AFFQ3Check:=D972AFFRead("ci/out/d972_b345_q3_checker_full.log","q3 checker log");;
  if StringFile("ci/out/d972_b345_q3_checker_full.ok")<>"D972_B345_Q3_CHECKER_FULL_EXIT_ZERO" or
     D972AFFCount(D972AFFQ3Check,"B345_Q3_CHECKER_PASS")<>1 then Error("157eb driver: q3 checker"); fi;
  Exec("bash -o pipefail -c 'python3 -u -B search/d972_b345_seedspan_affine_solver_v1.py ci/out/d972_b345_q3_chief_v1.json ci/out/d972_b345_seedspan_affine_v1.json 2>&1 | tee ci/out/d972_b345_seedspan_affine_v1_producer.log' && printf '%s' 'D972_B345_SEEDSPAN_AFFINE_PRODUCER_EXIT_ZERO' > 'ci/out/d972_b345_seedspan_affine_v1_producer.ok'");;
  D972AFFProducerRaw:=D972AFFRead(D972AFFProducerLog,"producer log");;
  if D972AFFRead(D972AFFProducerOk,"producer sentinel")<>D972AFFProducerSentinel then Error("157eb driver: producer"); fi;
  D972AFFTerminalCount:=0;;
  for token in ["B345_SEEDSPAN_AFFINE_POSITIVE","B345_SEEDSPAN_AFFINE_SEARCH_INCOMPLETE","B345_SEEDSPAN_AFFINE_UNKNOWN_RESOURCE","B345_SEEDSPAN_AFFINE_UNKNOWN_INPUT"] do
    D972AFFTerminalCount:=D972AFFTerminalCount+D972AFFCount(D972AFFProducerRaw,token);;
  od;
  if D972AFFTerminalCount<>1 then Error("157eb driver: terminal marker count"); fi;
  Exec("bash -o pipefail -c 'python3 -u -B search/check_d972_b345_seedspan_affine_solver_v1.py ci/out/d972_b345_q3_chief_v1.json ci/out/d972_b345_seedspan_affine_v1.json 2>&1 | tee ci/out/d972_b345_seedspan_affine_v1_checker.log' && printf '%s' 'D972_B345_SEEDSPAN_AFFINE_CHECKER_EXIT_ZERO' > 'ci/out/d972_b345_seedspan_affine_v1_checker.ok'");;
  D972AFFCheckerRaw:=D972AFFRead(D972AFFCheckerLog,"checker log");;
  if D972AFFRead(D972AFFCheckerOk,"checker sentinel")<>D972AFFCheckerSentinel or
     D972AFFCount(D972AFFCheckerRaw,"D972_B345_SEEDSPAN_AFFINE_CHECK_PASS")<>1 then Error("157eb driver: checker"); fi;
  Print("B345_SEEDSPAN_AFFINE_GHA_DRIVER_PASS mode=full artifact_sha256=",HexSHA256(StringFile(D972AFFArtifact)),"\n");;
fi;
