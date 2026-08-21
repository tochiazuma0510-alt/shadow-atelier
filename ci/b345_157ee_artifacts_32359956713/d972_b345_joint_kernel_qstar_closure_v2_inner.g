#############################################################################
## Thin fail-closed same-job driver for the 157ee joint-kernel certificate.
#############################################################################

D972JKQ3Driver := "search/d972_b345_q3_gha_driver_v1.g";;
D972JKQ3DriverSHA :=
  "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831";;
D972JKTask := "sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md";;
D972JKTaskSHA := "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4";;
D972JKProducer := "search/d972_b345_joint_kernel_qstar_closure_v1.py";;
D972JKProducerSHA := "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc";;
D972JKChecker := "search/check_d972_b345_joint_kernel_qstar_closure_v2.py";;
D972JKCheckerSHA := "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88";;
D972JKPrevProducer := "search/d972_b345_triple_cube_raw_lambda_census_v1.py";;
D972JKPrevProducerSHA := "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db";;
D972JKPrevChecker := "search/check_d972_b345_triple_cube_raw_lambda_census_v1.py";;
D972JKPrevCheckerSHA := "677aa1b69e4415da9629c34fcf0e469ad974cf3c888be7e768635bac50f672ce";;
D972JKPrevDriver := "search/d972_b345_triple_cube_raw_lambda_census_gha_driver_v1.g";;
D972JKPrevDriverSHA := "29a31752d42bd3f5a0e7f27ca38495bdd54c9cc694d12ddf9fe637e8749975e9";;
D972JKQ3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972JKQ3ArtifactSHA :=
  "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972JKArtifact := "ci/out/d972_b345_joint_kernel_qstar_closure_v1.json";;
D972JKSelfLog := "ci/out/d972_b345_joint_kernel_qstar_closure_v1_selftest.log";;
D972JKSelfOk := "ci/out/d972_b345_joint_kernel_qstar_closure_v1_selftest.ok";;
D972JKProducerLog := "ci/out/d972_b345_joint_kernel_qstar_closure_v1_producer.log";;
D972JKCheckerLog := "ci/out/d972_b345_joint_kernel_qstar_closure_v1_checker.log";;
D972JKMathOk := "ci/out/d972_b345_joint_kernel_qstar_closure_v1_math.ok";;
D972JKTiming := "ci/out/d972_b345_joint_kernel_qstar_closure_v1_timing.txt";;
D972JKQ3Child := "ci/out/d972_b345_joint_kernel_qstar_closure_v1_q3_child.g";;
D972JKQ3Log := "ci/out/d972_b345_joint_kernel_qstar_closure_v1_q3_child.log";;
D972JKQ3Ok := "ci/out/d972_b345_joint_kernel_qstar_closure_v1_q3_child.ok";;

D972JKRequireSHA := function(path,expected)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157ee driver: missing source ",path); fi;
  got:=HexSHA256(raw);;
  if got<>expected then Error("157ee driver: source SHA drift ",path," got=",got); fi;
  return true;
end;;

D972JKCount := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157ee driver: occurrence input");
  fi;
  n:=Length(text);;m:=Length(needle);;count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972JKRead := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("157ee driver: missing ",label); fi;
  return raw;
end;;

D972JKWrite := function(path,text)
  local stream,got;
  stream:=OutputTextFile(path,false);;
  if stream=fail then Error("157ee driver: child write open"); fi;
  SetPrintFormattingStatus(stream,false);;PrintTo(stream,text);;CloseStream(stream);;
  got:=StringFile(path);;
  if got=fail or got<>text then Error("157ee driver: child readback"); fi;
  return true;
end;;

D972JKRequireSHA(D972JKQ3Driver,D972JKQ3DriverSHA);;
D972JKRequireSHA(D972JKTask,D972JKTaskSHA);;
D972JKRequireSHA(D972JKProducer,D972JKProducerSHA);;
D972JKRequireSHA(D972JKChecker,D972JKCheckerSHA);;
D972JKRequireSHA(D972JKPrevProducer,D972JKPrevProducerSHA);;
D972JKRequireSHA(D972JKPrevChecker,D972JKPrevCheckerSHA);;
D972JKRequireSHA(D972JKPrevDriver,D972JKPrevDriverSHA);;
if Length(D972JKProducerSHA)<>64 or Length(D972JKCheckerSHA)<>64 then
  Error("157ee driver: producer/checker SHA constants not frozen");
fi;

D972JKSelf:=IsBound(D972_B345_JOINT_KERNEL_QSTAR_SELFTEST) and
  D972_B345_JOINT_KERNEL_QSTAR_SELFTEST=true;;
D972JKRun:=IsBound(D972_B345_JOINT_KERNEL_QSTAR_RUN) and
  D972_B345_JOINT_KERNEL_QSTAR_RUN=true;;
if D972JKSelf=D972JKRun then Error("157ee driver: select exactly one mode"); fi;

Exec("bash -o pipefail -c 'python3 -c \"import sympy\" >/dev/null 2>&1 || python3 -m pip install --disable-pip-version-check --no-input sympy==1.14.0'");;

if D972JKSelf then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_selftest.log' 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_selftest.ok' && python3 -u -B search/d972_b345_joint_kernel_qstar_closure_v1.py --self-test > 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_selftest.log' 2>&1 && python3 -u -B search/check_d972_b345_joint_kernel_qstar_closure_v2.py --self-test >> 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_selftest.log' 2>&1 && printf '%s' 'D972_B345_JOINT_KERNEL_QSTAR_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_selftest.ok'");;
  if D972JKRead(D972JKSelfOk,"selftest sentinel")<>
     "D972_B345_JOINT_KERNEL_QSTAR_SELFTEST_EXIT_ZERO" then
    Error("157ee driver: selftest exit sentinel");
  fi;
  D972JKSelfRaw:=D972JKRead(D972JKSelfLog,"selftest log");;
  if D972JKCount(D972JKSelfRaw,
       "D972_B345_JOINT_KERNEL_QSTAR_PRODUCER_SELFTEST_PASS")<>1 or
     D972JKCount(D972JKSelfRaw,
       "D972_B345_JOINT_KERNEL_QSTAR_CHECKER_SELFTEST_PASS")<>1 then
    Error("157ee driver: combined selftest markers");
  fi;
  Print(D972JKSelfRaw,
    "\nB345_JOINT_KERNEL_QSTAR_GHA_DRIVER_PASS mode=selftest\n");;
else
  if not IsBound(D972_B345_JOINT_KERNEL_QSTAR_OUTPUT) or
     D972_B345_JOINT_KERNEL_QSTAR_OUTPUT<>D972JKArtifact then
    Error("157ee driver: fixed output path required");
  fi;
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_q3_child.g' 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_q3_child.log' 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_q3_child.ok' 'ci/out/d972_b345_joint_kernel_qstar_closure_v1.json' 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_producer.log' 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_checker.log' 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_math.ok' 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_timing.txt'");;
  D972JKQ3Text:=Concatenation(
    "if GAPInfo.Version<>\"4.16.0\" then Error(\"GAP 4.16.0 required\"); fi;;\n",
    "if LoadPackage(\"smallgrp\")<>true then Error(\"smallgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"autpgrp\")<>true then Error(\"autpgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"anupq\")<>true then Error(\"anupq LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"json\")<>true then Error(\"json LoadPackage failed\"); fi;;\n",
    "D972_B345_Q3_RUN:=true;; D972_B345_Q3_OUTPUT:=\"ci/out/d972_b345_q3_chief_v1.json\";;\n",
    "Read(\"search/d972_b345_q3_gha_driver_v1.g\");; QUIT_GAP(0);;\n");;
  D972JKWrite(D972JKQ3Child,D972JKQ3Text);;
  Exec("bash -o pipefail -c 'gap -l \";/usr/share/gap;/usr/lib/gap;${GAP_P2_PACKAGE_ROOT:?}\" --quitonbreak -q -o 12g ci/out/d972_b345_joint_kernel_qstar_closure_v1_q3_child.g 2>&1 | tee ci/out/d972_b345_joint_kernel_qstar_closure_v1_q3_child.log' && printf '%s' 'D972_B345_JOINT_KERNEL_QSTAR_Q3_EXIT_ZERO' > 'ci/out/d972_b345_joint_kernel_qstar_closure_v1_q3_child.ok'");;
  if D972JKRead(D972JKQ3Ok,"q3 sentinel")<>
     "D972_B345_JOINT_KERNEL_QSTAR_Q3_EXIT_ZERO" then Error("157ee driver: q3 child"); fi;
  D972JKQ3Raw:=D972JKRead(D972JKQ3Artifact,"q3 artifact");;
  if HexSHA256(D972JKQ3Raw)<>D972JKQ3ArtifactSHA then Error("157ee driver: q3 artifact SHA"); fi;
  Exec("bash -o pipefail -c 'python3 -u -B search/check_d972_b345_q3_chief_v1.py ci/out/d972_b345_q3_chief_v1.json > ci/out/d972_b345_q3_checker_full.log 2>&1 && printf %s D972_B345_Q3_CHECKER_FULL_EXIT_ZERO > ci/out/d972_b345_q3_checker_full.ok'");;
  D972JKQ3Check:=D972JKRead("ci/out/d972_b345_q3_checker_full.log","q3 checker");;
  if D972JKRead("ci/out/d972_b345_q3_checker_full.ok","q3 checker sentinel")<>
       "D972_B345_Q3_CHECKER_FULL_EXIT_ZERO" or
     D972JKCount(D972JKQ3Check,"B345_Q3_CHECKER_PASS")<>1 then
    Error("157ee driver: q3 independent checker");
  fi;
  Exec("bash -o pipefail -c 'set -e; SECONDS=0; python3 -u -B search/d972_b345_joint_kernel_qstar_closure_v1.py ci/out/d972_b345_q3_chief_v1.json ci/out/d972_b345_joint_kernel_qstar_closure_v1.json 18000 2>&1 | tee ci/out/d972_b345_joint_kernel_qstar_closure_v1_producer.log; producer_elapsed=$SECONDS; remaining=$((18000-SECONDS)); if [ $remaining -le 0 ]; then exit 97; fi; python3 -u -B search/check_d972_b345_joint_kernel_qstar_closure_v2.py ci/out/d972_b345_q3_chief_v1.json ci/out/d972_b345_joint_kernel_qstar_closure_v1.json $remaining 2>&1 | tee ci/out/d972_b345_joint_kernel_qstar_closure_v1_checker.log; final_elapsed=$SECONDS; final_remaining=$((18000-final_elapsed)); if [ $final_remaining -le 0 ]; then exit 98; fi; printf \"producer_elapsed=%s\\nchecker_initial_remaining=%s\\nfinal_elapsed=%s\\nfinal_margin=%s\\n\" $producer_elapsed $remaining $final_elapsed $final_remaining > ci/out/d972_b345_joint_kernel_qstar_closure_v1_timing.txt; printf %s D972_B345_JOINT_KERNEL_QSTAR_MATH_EXIT_ZERO > ci/out/d972_b345_joint_kernel_qstar_closure_v1_math.ok'");;
  if D972JKRead(D972JKMathOk,"math sentinel")<>
     "D972_B345_JOINT_KERNEL_QSTAR_MATH_EXIT_ZERO" then Error("157ee driver: math process"); fi;
  D972JKProducerRaw:=D972JKRead(D972JKProducerLog,"producer log");;
  D972JKTerminalCount:=0;;
  for token in ["B345_JOINT_KERNEL_QSTAR_CLOSED","B345_JOINT_KERNEL_QSTAR_ACTIVE",
                "B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE",
                "B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT"] do
    D972JKTerminalCount:=D972JKTerminalCount+D972JKCount(D972JKProducerRaw,token);;
  od;
  if D972JKTerminalCount<>1 or D972JKCount(D972JKProducerRaw,
       "D972_B345_JOINT_KERNEL_QSTAR_PRODUCER_EXIT_ZERO")<>1 then
    Error("157ee driver: producer terminal/exit markers");
  fi;
  D972JKCheckerRaw:=D972JKRead(D972JKCheckerLog,"checker log");;
  if D972JKCount(D972JKCheckerRaw,"D972_B345_JOINT_KERNEL_QSTAR_CHECKER_PASS")<>1 then
    Error("157ee driver: checker PASS marker");
  fi;
  D972JKTimingRaw:=D972JKRead(D972JKTiming,"common deadline timing");;
  if D972JKCount(D972JKTimingRaw,"producer_elapsed=")<>1 or
     D972JKCount(D972JKTimingRaw,"checker_initial_remaining=")<>1 or
     D972JKCount(D972JKTimingRaw,"final_margin=")<>1 then Error("157ee driver: timing ledger"); fi;
  Print("B345_JOINT_KERNEL_QSTAR_GHA_DRIVER_PASS mode=full artifact_sha256=",
        HexSHA256(D972JKRead(D972JKArtifact,"final artifact")),"\n");;
fi;
