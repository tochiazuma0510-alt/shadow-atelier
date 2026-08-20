#############################################################################
## Thin fail-closed same-job driver for the 157ej lex-first target-6 v2 lane.
#############################################################################

D972EIProducer := "search/d972_b345_lexfirst_block_target6_v2.py";;
D972EIProducerSHA :=
  "ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a";;
D972EIChecker := "search/check_d972_b345_lexfirst_block_target6_v2.py";;
D972EICheckerSHA :=
  "fb28b8b4c7b42f5d83dd1f5c762136812d36731c427a003aae8a8fb0c36a66ba";;
D972EITask := "sol/luna_task_157ej_b345_lexfirst_block_target6_v2.md";;
D972EITaskSHA :=
  "1d6f14ef9f799a43fc344daa38606281dbcf0b2fe47d86db0b44df382762f290";;
D972EIV1Producer := "search/d972_b345_lexfirst_block_target6_v1.py";;
D972EIV1ProducerSHA :=
  "f901cffd73069e78c9cc256e1a6c18c7e7ce6adef6d4de0c4fe68970571476bb";;
D972EIV1Checker := "search/check_d972_b345_lexfirst_block_target6_v1.py";;
D972EIV1CheckerSHA :=
  "d0601533131008002d09a6320ab643df865a2a86245ed23f399e4c469bd93c57";;
D972EIV1Driver := "search/d972_b345_lexfirst_block_target6_gha_driver_v1.g";;
D972EIV1DriverSHA :=
  "e0cb01bf119ae7834fa85da7910c6dd82048c8ae756e48f834fad055a7bc4c0a";;
D972EIV1Reply := "sol/luna_reply_157ei_b345_lexfirst_block_target6.md";;
D972EIV1ReplySHA :=
  "de6c22867a7a66cb28fdbbffae2f92632e8dfc382a5f7088a097d7518cef2ad2";;
D972EIV1Task := "sol/luna_task_157ei_b345_lexfirst_block_target6.md";;
D972EIV1TaskSHA :=
  "cfe0c50046a750e4169c473872c5770ce76c105267353e82c9ed19de01c043f4";;
D972EIEHProducer := "search/d972_b345_full_d2_dual_correlation_v2.py";;
D972EIEHProducerSHA :=
  "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f";;
D972EIEHChecker := "search/check_d972_b345_full_d2_dual_correlation_v2.py";;
D972EIEHCheckerSHA :=
  "881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060";;
D972EIEHDriver := "search/d972_b345_full_d2_dual_correlation_gha_driver_v2.g";;
D972EIEHDriverSHA :=
  "5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde";;
D972EIEHTask := "sol/luna_task_157eh_b345_full_d2_monitor_scope_repair.md";;
D972EIEHTaskSHA :=
  "5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e";;
D972EIECProducer := "search/d972_b345_seedspan_triple4_v1.py";;
D972EIECProducerSHA :=
  "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29";;
D972EIECChecker := "search/check_d972_b345_seedspan_triple4_v1.py";;
D972EIECCheckerSHA :=
  "ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981";;
D972EIECDriver := "search/d972_b345_seedspan_triple4_gha_driver_v1.g";;
D972EIECDriverSHA :=
  "a9c88540c1abdb21dc214d4d4e6461c1431dc407f93542c49e0e65a14788fca4";;
D972EIECTask := "sol/luna_task_157ec_b345_seedspan_triple4.md";;
D972EIECTaskSHA :=
  "1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2";;
D972EIQ3Producer := "search/d972_b345_q3_chief_v1.g";;
D972EIQ3ProducerSHA :=
  "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755";;
D972EIQ3Checker := "search/check_d972_b345_q3_chief_v1.py";;
D972EIQ3CheckerSHA :=
  "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73";;
D972EIQ3Driver := "search/d972_b345_q3_gha_driver_v1.g";;
D972EIQ3DriverSHA :=
  "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831";;

D972EIQ3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972EIQ3ArtifactSHA :=
  "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972EIArtifact := "ci/out/d972_b345_lexfirst_block_target6_v2.json";;
D972EISelfLog := "ci/out/d972_b345_lexfirst_block_target6_v2_selftest.log";;
D972EISelfOk := "ci/out/d972_b345_lexfirst_block_target6_v2_selftest.ok";;
D972EIProducerLog := "ci/out/d972_b345_lexfirst_block_target6_v2_producer.log";;
D972EICheckerLog := "ci/out/d972_b345_lexfirst_block_target6_v2_checker.log";;
D972EIMathOk := "ci/out/d972_b345_lexfirst_block_target6_v2_math.ok";;
D972EITiming := "ci/out/d972_b345_lexfirst_block_target6_v2_timing.txt";;
D972EIQ3Child := "ci/out/d972_b345_lexfirst_block_target6_v2_q3_child.g";;
D972EIQ3Log := "ci/out/d972_b345_lexfirst_block_target6_v2_q3_child.log";;
D972EIQ3Ok := "ci/out/d972_b345_lexfirst_block_target6_v2_q3_child.ok";;

D972EIRead := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("157ei driver: missing ",label); fi;
  return raw;
end;;

D972EIRequireSHA := function(path,expected)
  local raw,got;
  raw:=D972EIRead(path,path);; got:=HexSHA256(raw);;
  if got<>expected then Error("157ei driver: SHA drift ",path," got=",got); fi;
  return true;
end;;

D972EICount := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157ei driver: occurrence input");
  fi;
  n:=Length(text);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972EIWrite := function(path,text)
  local stream,got;
  stream:=OutputTextFile(path,false);;
  if stream=fail then Error("157ei driver: child write open"); fi;
  SetPrintFormattingStatus(stream,false);; PrintTo(stream,text);;
  CloseStream(stream);; got:=StringFile(path);;
  if got=fail or got<>text then Error("157ei driver: child readback"); fi;
  return true;
end;;

for D972EISource in [
  [D972EIProducer,D972EIProducerSHA],
  [D972EIChecker,D972EICheckerSHA],
  [D972EITask,D972EITaskSHA],
  [D972EIV1Producer,D972EIV1ProducerSHA],
  [D972EIV1Checker,D972EIV1CheckerSHA],
  [D972EIV1Driver,D972EIV1DriverSHA],
  [D972EIV1Reply,D972EIV1ReplySHA],
  [D972EIV1Task,D972EIV1TaskSHA],
  [D972EIEHProducer,D972EIEHProducerSHA],
  [D972EIEHChecker,D972EIEHCheckerSHA],
  [D972EIEHDriver,D972EIEHDriverSHA],
  [D972EIEHTask,D972EIEHTaskSHA],
  [D972EIECProducer,D972EIECProducerSHA],
  [D972EIECChecker,D972EIECCheckerSHA],
  [D972EIECDriver,D972EIECDriverSHA],
  [D972EIECTask,D972EIECTaskSHA],
  [D972EIQ3Producer,D972EIQ3ProducerSHA],
  [D972EIQ3Checker,D972EIQ3CheckerSHA],
  [D972EIQ3Driver,D972EIQ3DriverSHA]
] do
  D972EIRequireSHA(D972EISource[1],D972EISource[2]);;
od;

D972EISelf:=IsBound(D972_B345_LEXBLOCK_TARGET6_V2_SELFTEST) and
  D972_B345_LEXBLOCK_TARGET6_V2_SELFTEST=true;;
D972EIRun:=IsBound(D972_B345_LEXBLOCK_TARGET6_V2_RUN) and
  D972_B345_LEXBLOCK_TARGET6_V2_RUN=true;;
if D972EISelf=D972EIRun then
  Error("157ei driver: select exactly one boolean mode");
fi;
if IsBound(D972_B345_LEXBLOCK_TARGET6_V2_OUTPUT) and
   D972_B345_LEXBLOCK_TARGET6_V2_OUTPUT<>D972EIArtifact then
  Error("157ei driver: optional output differs from fixed artifact");
fi;

if D972EISelf then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_lexfirst_block_target6_v2_selftest.log' 'ci/out/d972_b345_lexfirst_block_target6_v2_selftest.ok' && python3 -u -B search/d972_b345_lexfirst_block_target6_v2.py --self-test > 'ci/out/d972_b345_lexfirst_block_target6_v2_selftest.log' 2>&1 && python3 -u -B search/check_d972_b345_lexfirst_block_target6_v2.py --self-test >> 'ci/out/d972_b345_lexfirst_block_target6_v2_selftest.log' 2>&1 && printf '%s' 'D972_B345_LEXBLOCK_TARGET6_V2_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b345_lexfirst_block_target6_v2_selftest.ok'");;
  if D972EIRead(D972EISelfOk,"selftest sentinel")<>
       "D972_B345_LEXBLOCK_TARGET6_V2_SELFTEST_EXIT_ZERO" then
    Error("157ei driver: selftest sentinel");
  fi;
  D972EISelfRaw:=D972EIRead(D972EISelfLog,"selftest log");;
  if D972EICount(D972EISelfRaw,"Traceback (most recent call last):")<>0 or
     D972EICount(D972EISelfRaw,
       "D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_SELFTEST_PASS")<>1 or
     D972EICount(D972EISelfRaw,
       "D972_B345_LEXBLOCK_TARGET6_V2_CHECKER_SELFTEST_PASS")<>1 or
     D972EICount(D972EISelfRaw,"value_root_union=1")<>1 or
     D972EICount(D972EISelfRaw,"source_omission_rejected=1")<>1 or
     D972EICount(D972EISelfRaw,
       "D972_B345_FULL_D2_DUAL_CORRELATION_V2_PRODUCER_SELFTEST_PASS")<>1 or
     D972EICount(D972EISelfRaw,
       "D972_B345_FULL_D2_DUAL_CORRELATION_V2_CHECKER_SELFTEST_PASS")<>1 then
    Error("157ei driver: combined/inherited selftest markers");
  fi;
  Print(D972EISelfRaw,
    "\nB345_LEXBLOCK_TARGET6_V2_GHA_DRIVER_PASS mode=selftest\n");;
else
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b345_lexfirst_block_target6_v2_q3_child.g' 'ci/out/d972_b345_lexfirst_block_target6_v2_q3_child.log' 'ci/out/d972_b345_lexfirst_block_target6_v2_q3_child.ok' 'ci/out/d972_b345_lexfirst_block_target6_v1.json' 'ci/out/d972_b345_lexfirst_block_target6_v2.json' 'ci/out/d972_b345_lexfirst_block_target6_v2_producer.log' 'ci/out/d972_b345_lexfirst_block_target6_v2_checker.log' 'ci/out/d972_b345_lexfirst_block_target6_v2_math.ok' 'ci/out/d972_b345_lexfirst_block_target6_v2_timing.txt'");;
  D972EIQ3Text:=Concatenation(
    "if GAPInfo.Version<>\"4.16.0\" then Error(\"GAP 4.16.0 required\"); fi;;\n",
    "if LoadPackage(\"smallgrp\")<>true then Error(\"smallgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"autpgrp\")<>true then Error(\"autpgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"anupq\")<>true then Error(\"anupq LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"json\")<>true then Error(\"json LoadPackage failed\"); fi;;\n",
    "D972_B345_Q3_RUN:=true;; D972_B345_Q3_OUTPUT:=\"ci/out/d972_b345_q3_chief_v1.json\";;\n",
    "Read(\"search/d972_b345_q3_gha_driver_v1.g\");; QUIT_GAP(0);;\n");;
  D972EIWrite(D972EIQ3Child,D972EIQ3Text);;
  Exec("bash -o pipefail -c 'gap -l \";/usr/share/gap;/usr/lib/gap;${GAP_P2_PACKAGE_ROOT:?}\" --quitonbreak -q -o 12g ci/out/d972_b345_lexfirst_block_target6_v2_q3_child.g 2>&1 | tee ci/out/d972_b345_lexfirst_block_target6_v2_q3_child.log' && printf '%s' 'D972_B345_LEXBLOCK_TARGET6_V2_Q3_EXIT_ZERO' > 'ci/out/d972_b345_lexfirst_block_target6_v2_q3_child.ok'");;
  if D972EIRead(D972EIQ3Ok,"q3 sentinel")<>
       "D972_B345_LEXBLOCK_TARGET6_V2_Q3_EXIT_ZERO" then
    Error("157ei driver: q3 child");
  fi;
  D972EIQ3Raw:=D972EIRead(D972EIQ3Artifact,"q3 artifact");;
  if HexSHA256(D972EIQ3Raw)<>D972EIQ3ArtifactSHA then
    Error("157ei driver: q3 artifact SHA");
  fi;
  Exec("bash -o pipefail -c 'python3 -u -B search/check_d972_b345_q3_chief_v1.py ci/out/d972_b345_q3_chief_v1.json > ci/out/d972_b345_q3_checker_full.log 2>&1 && printf %s D972_B345_Q3_CHECKER_FULL_EXIT_ZERO > ci/out/d972_b345_q3_checker_full.ok'");;
  D972EIQ3Check:=D972EIRead("ci/out/d972_b345_q3_checker_full.log",
                           "q3 checker");;
  if D972EIRead("ci/out/d972_b345_q3_checker_full.ok",
       "q3 checker sentinel")<>"D972_B345_Q3_CHECKER_FULL_EXIT_ZERO" or
     D972EICount(D972EIQ3Check,"B345_Q3_CHECKER_PASS")<>1 then
    Error("157ei driver: q3 independent checker");
  fi;
  Exec("bash -o pipefail -c 'set -e; SECONDS=0; python3 -u -B search/d972_b345_lexfirst_block_target6_v2.py --q3 ci/out/d972_b345_q3_chief_v1.json --output ci/out/d972_b345_lexfirst_block_target6_v2.json --seconds 18000 2>&1 | tee ci/out/d972_b345_lexfirst_block_target6_v2_producer.log; producer_elapsed=$SECONDS; remaining=$((18000-SECONDS)); if [ $remaining -le 0 ]; then exit 97; fi; python3 -u -B search/check_d972_b345_lexfirst_block_target6_v2.py --q3 ci/out/d972_b345_q3_chief_v1.json --receipt ci/out/d972_b345_lexfirst_block_target6_v2.json --seconds $remaining 2>&1 | tee ci/out/d972_b345_lexfirst_block_target6_v2_checker.log; final_elapsed=$SECONDS; final_remaining=$((18000-final_elapsed)); if [ $final_remaining -le 0 ]; then exit 98; fi; printf \"producer_elapsed=%s\\nchecker_initial_remaining=%s\\nfinal_elapsed=%s\\nfinal_margin=%s\\n\" $producer_elapsed $remaining $final_elapsed $final_remaining > ci/out/d972_b345_lexfirst_block_target6_v2_timing.txt; printf %s D972_B345_LEXBLOCK_TARGET6_V2_MATH_EXIT_ZERO > ci/out/d972_b345_lexfirst_block_target6_v2_math.ok'");;
  if D972EIRead(D972EIMathOk,"math sentinel")<>
       "D972_B345_LEXBLOCK_TARGET6_V2_MATH_EXIT_ZERO" then
    Error("157ei driver: producer/checker common deadline");
  fi;
  D972EIProducerRaw:=D972EIRead(D972EIProducerLog,"producer log");;
  D972EITerminalCount:=0;;
  for D972EIToken in [
      "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT",
      "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT",
      "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE",
      "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_INPUT"] do
    D972EITerminalCount:=D972EITerminalCount+
      D972EICount(D972EIProducerRaw,D972EIToken);;
  od;
  if D972EITerminalCount<>1 or
     D972EICount(D972EIProducerRaw,
       "D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_PASS")<>1 then
    Error("157ei driver: producer terminal/exit markers");
  fi;
  D972EICheckerRaw:=D972EIRead(D972EICheckerLog,"checker log");;
  if D972EICount(D972EIProducerRaw,
       "Traceback (most recent call last):")<>0 or
     D972EICount(D972EICheckerRaw,
       "Traceback (most recent call last):")<>0 or
     D972EICount(D972EICheckerRaw,
       "D972_B345_LEXBLOCK_TARGET6_V2_CHECKER_PASS")<>1 then
    Error("157ei driver: checker PASS marker");
  fi;
  D972EITimingRaw:=D972EIRead(D972EITiming,"common deadline timing");;
  if D972EICount(D972EITimingRaw,"producer_elapsed=")<>1 or
     D972EICount(D972EITimingRaw,"checker_initial_remaining=")<>1 or
     D972EICount(D972EITimingRaw,"final_margin=")<>1 then
    Error("157ei driver: common deadline ledger");
  fi;
  Print("B345_LEXBLOCK_TARGET6_V2_GHA_DRIVER_PASS mode=full artifact_sha256=",
    HexSHA256(D972EIRead(D972EIArtifact,"final artifact")),"\n");;
fi;
