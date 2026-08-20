#############################################################################
## 157ek: fail-closed checker-projection repair driver (v3 orchestration).
#############################################################################

D972EKProducer := "search/d972_b345_lexfirst_block_target6_v2.py";;
D972EKChecker := "search/check_d972_b345_lexfirst_block_target6_v3.py";;
D972EKTask :=
  "sol/luna_task_157ek_b345_lexfirst_block_checker_projection_v3.md";;
D972EKArtifact := "ci/out/d972_b345_lexfirst_block_target6_v2.json";;
D972EKQ3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972EKQ3ArtifactSHA :=
  "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;

D972EKSourcePins := [
  [D972EKProducer,
   "ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a",148824],
  [D972EKChecker,
   "bc0c1c4dfe2e4bc6ea8fd6c18e3af245d20e0959408649dd61d23f969cba9845",14032],
  [D972EKTask,
   "af5bfe5182e66010fb8893a68ad9f02dda87389171ea425c4122c3fad8addb7c",13686],
  ["search/check_d972_b345_lexfirst_block_target6_v2.py",
   "fb28b8b4c7b42f5d83dd1f5c762136812d36731c427a003aae8a8fb0c36a66ba",130007],
  ["search/d972_b345_lexfirst_block_target6_gha_driver_v2.g",
   "48f5717b9be1d6f6087cdf2864d20d41df2475f5d0d87b43c2bd1deefab01394",13597],
  ["sol/luna_task_157ej_b345_lexfirst_block_target6_v2.md",
   "1d6f14ef9f799a43fc344daa38606281dbcf0b2fe47d86db0b44df382762f290",14667],
  ["sol/luna_reply_157ej_b345_lexfirst_block_target6_v2.md",
   "f00a3f56e140663002e85a488f78b37ade796126928d475f30bb57e951020428",8676],
  ["search/d972_b345_lexfirst_block_target6_v1.py",
   "f901cffd73069e78c9cc256e1a6c18c7e7ce6adef6d4de0c4fe68970571476bb",143075],
  ["search/check_d972_b345_lexfirst_block_target6_v1.py",
   "d0601533131008002d09a6320ab643df865a2a86245ed23f399e4c469bd93c57",128399],
  ["search/d972_b345_lexfirst_block_target6_gha_driver_v1.g",
   "e0cb01bf119ae7834fa85da7910c6dd82048c8ae756e48f834fad055a7bc4c0a",10516],
  ["sol/luna_reply_157ei_b345_lexfirst_block_target6.md",
   "de6c22867a7a66cb28fdbbffae2f92632e8dfc382a5f7088a097d7518cef2ad2",13277],
  ["sol/luna_task_157ei_b345_lexfirst_block_target6.md",
   "cfe0c50046a750e4169c473872c5770ce76c105267353e82c9ed19de01c043f4",24179],
  ["search/d972_b345_full_d2_dual_correlation_v2.py",
   "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f",42449],
  ["search/check_d972_b345_full_d2_dual_correlation_v2.py",
   "881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060",21933],
  ["search/d972_b345_full_d2_dual_correlation_gha_driver_v2.g",
   "5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde",13253],
  ["sol/luna_task_157eh_b345_full_d2_monitor_scope_repair.md",
   "5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e",15015],
  ["search/d972_b345_seedspan_triple4_v1.py",
   "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29",535219],
  ["search/check_d972_b345_seedspan_triple4_v1.py",
   "ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981",574347],
  ["search/d972_b345_seedspan_triple4_gha_driver_v1.g",
   "a9c88540c1abdb21dc214d4d4e6461c1431dc407f93542c49e0e65a14788fca4",9041],
  ["sol/luna_task_157ec_b345_seedspan_triple4.md",
   "1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2",14751],
  ["search/d972_b345_q3_chief_v1.g",
   "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755",76867],
  ["search/check_d972_b345_q3_chief_v1.py",
   "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73",89082],
  ["search/d972_b345_q3_gha_driver_v1.g",
   "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831",5488]
];;

D972EKSelfLog :=
  "ci/out/d972_b345_lexfirst_block_target6_v3_selftest.log";;
D972EKSelfOk :=
  "ci/out/d972_b345_lexfirst_block_target6_v3_selftest.ok";;
D972EKProducerLog :=
  "ci/out/d972_b345_lexfirst_block_target6_v3_producer.log";;
D972EKCheckerLog :=
  "ci/out/d972_b345_lexfirst_block_target6_v3_checker.log";;
D972EKMathOk := "ci/out/d972_b345_lexfirst_block_target6_v3_math.ok";;
D972EKTiming := "ci/out/d972_b345_lexfirst_block_target6_v3_timing.txt";;
D972EKQ3Child := "ci/out/d972_b345_lexfirst_block_target6_v3_q3_child.g";;
D972EKQ3Log := "ci/out/d972_b345_lexfirst_block_target6_v3_q3_child.log";;
D972EKQ3Ok := "ci/out/d972_b345_lexfirst_block_target6_v3_q3_child.ok";;

D972EKRead := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("157ek driver: missing ",label); fi;
  return raw;
end;;

D972EKRequirePin := function(row)
  local raw,got;
  if not IsList(row) or Length(row)<>3 or not IsString(row[1]) or
     not IsString(row[2]) or not IsInt(row[3]) or row[3]<=0 then
    Error("157ek driver: malformed source pin");
  fi;
  raw:=D972EKRead(row[1],row[1]);;
  got:=HexSHA256(raw);;
  if Length(raw)<>row[3] or got<>row[2] then
    Error("157ek driver: source pin drift ",row[1]," sha=",got,
          " bytes=",Length(raw));
  fi;
  return true;
end;;

D972EKCount := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157ek driver: occurrence input");
  fi;
  n:=Length(text);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972EKWrite := function(path,text)
  local stream,got;
  stream:=OutputTextFile(path,false);;
  if stream=fail then Error("157ek driver: child write open"); fi;
  SetPrintFormattingStatus(stream,false);; PrintTo(stream,text);;
  CloseStream(stream);; got:=StringFile(path);;
  if got=fail or got<>text then Error("157ek driver: child readback"); fi;
  return true;
end;;

for D972EKSource in D972EKSourcePins do D972EKRequirePin(D972EKSource);; od;

D972EKSelf:=IsBound(D972_B345_LEXBLOCK_TARGET6_V3_SELFTEST) and
  D972_B345_LEXBLOCK_TARGET6_V3_SELFTEST=true;;
D972EKRun:=IsBound(D972_B345_LEXBLOCK_TARGET6_V3_RUN) and
  D972_B345_LEXBLOCK_TARGET6_V3_RUN=true;;
if D972EKSelf=D972EKRun then
  Error("157ek driver: select exactly one boolean mode");
fi;
if IsBound(D972_B345_LEXBLOCK_TARGET6_V3_OUTPUT) and
   D972_B345_LEXBLOCK_TARGET6_V3_OUTPUT<>D972EKArtifact then
  Error("157ek driver: optional output differs from frozen v2 artifact");
fi;

if D972EKSelf then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_lexfirst_block_target6_v3_selftest.log' 'ci/out/d972_b345_lexfirst_block_target6_v3_selftest.ok' && python3 -u -B search/d972_b345_lexfirst_block_target6_v2.py --self-test > 'ci/out/d972_b345_lexfirst_block_target6_v3_selftest.log' 2>&1 && python3 -u -B search/check_d972_b345_lexfirst_block_target6_v3.py --self-test >> 'ci/out/d972_b345_lexfirst_block_target6_v3_selftest.log' 2>&1 && printf '%s' 'D972_B345_LEXBLOCK_TARGET6_V3_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b345_lexfirst_block_target6_v3_selftest.ok'");;
  if D972EKRead(D972EKSelfOk,"selftest sentinel")<>
       "D972_B345_LEXBLOCK_TARGET6_V3_SELFTEST_EXIT_ZERO" then
    Error("157ek driver: selftest sentinel");
  fi;
  D972EKSelfRaw:=D972EKRead(D972EKSelfLog,"selftest log");;
  if D972EKCount(D972EKSelfRaw,"Traceback (most recent call last):")<>0 or
     D972EKCount(D972EKSelfRaw,
       "D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_SELFTEST_PASS")<>1 or
     D972EKCount(D972EKSelfRaw,
       "D972_B345_LEXBLOCK_TARGET6_V2_CHECKER_SELFTEST_PASS")<>1 or
     D972EKCount(D972EKSelfRaw,
       "D972_B345_LEXBLOCK_TARGET6_V3_CHECKER_SELFTEST_PASS")<>1 or
     D972EKCount(D972EKSelfRaw,"prefix_projection_three_keys=1")<>1 or
     D972EKCount(D972EKSelfRaw,"directed_base_support_consumed=1")<>1 or
     D972EKCount(D972EKSelfRaw,
       "prefix_projection_omissions_rejected=3")<>1 or
     D972EKCount(D972EKSelfRaw,"prefix_projection_extra_rejected=1")<>1 or
     D972EKCount(D972EKSelfRaw,"production_wrapper_entry=1")<>1 or
     D972EKCount(D972EKSelfRaw,"source_shape_recurrence=1")<>1 or
     D972EKCount(D972EKSelfRaw,"value_root_union=1")<>1 or
     D972EKCount(D972EKSelfRaw,"source_omission_rejected=1")<>1 or
     D972EKCount(D972EKSelfRaw,
       "D972_B345_FULL_D2_DUAL_CORRELATION_V2_PRODUCER_SELFTEST_PASS")<>1 or
     D972EKCount(D972EKSelfRaw,
       "D972_B345_FULL_D2_DUAL_CORRELATION_V2_CHECKER_SELFTEST_PASS")<>1 then
    Error("157ek driver: combined/inherited/projection selftest markers");
  fi;
  Print(D972EKSelfRaw,
    "\nB345_LEXBLOCK_TARGET6_V3_GHA_DRIVER_PASS mode=selftest\n");;
else
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b345_lexfirst_block_target6_v2.json' 'ci/out/d972_b345_lexfirst_block_target6_v3_q3_child.g' 'ci/out/d972_b345_lexfirst_block_target6_v3_q3_child.log' 'ci/out/d972_b345_lexfirst_block_target6_v3_q3_child.ok' 'ci/out/d972_b345_lexfirst_block_target6_v3_producer.log' 'ci/out/d972_b345_lexfirst_block_target6_v3_checker.log' 'ci/out/d972_b345_lexfirst_block_target6_v3_math.ok' 'ci/out/d972_b345_lexfirst_block_target6_v3_timing.txt'");;
  D972EKQ3Text:=Concatenation(
    "if GAPInfo.Version<>\"4.16.0\" then Error(\"GAP 4.16.0 required\"); fi;;\n",
    "if LoadPackage(\"smallgrp\")<>true then Error(\"smallgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"autpgrp\")<>true then Error(\"autpgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"anupq\")<>true then Error(\"anupq LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"json\")<>true then Error(\"json LoadPackage failed\"); fi;;\n",
    "D972_B345_Q3_RUN:=true;; D972_B345_Q3_OUTPUT:=\"ci/out/d972_b345_q3_chief_v1.json\";;\n",
    "Read(\"search/d972_b345_q3_gha_driver_v1.g\");; QUIT_GAP(0);;\n");;
  D972EKWrite(D972EKQ3Child,D972EKQ3Text);;
  Exec("bash -o pipefail -c 'gap -l \";/usr/share/gap;/usr/lib/gap;${GAP_P2_PACKAGE_ROOT:?}\" --quitonbreak -q -o 12g ci/out/d972_b345_lexfirst_block_target6_v3_q3_child.g 2>&1 | tee ci/out/d972_b345_lexfirst_block_target6_v3_q3_child.log' && printf '%s' 'D972_B345_LEXBLOCK_TARGET6_V3_Q3_EXIT_ZERO' > 'ci/out/d972_b345_lexfirst_block_target6_v3_q3_child.ok'");;
  if D972EKRead(D972EKQ3Ok,"q3 sentinel")<>
       "D972_B345_LEXBLOCK_TARGET6_V3_Q3_EXIT_ZERO" then
    Error("157ek driver: q3 child");
  fi;
  D972EKQ3Raw:=D972EKRead(D972EKQ3Artifact,"q3 artifact");;
  if HexSHA256(D972EKQ3Raw)<>D972EKQ3ArtifactSHA then
    Error("157ek driver: q3 artifact SHA");
  fi;
  Exec("bash -o pipefail -c 'python3 -u -B search/check_d972_b345_q3_chief_v1.py ci/out/d972_b345_q3_chief_v1.json > ci/out/d972_b345_q3_checker_full.log 2>&1 && printf %s D972_B345_Q3_CHECKER_FULL_EXIT_ZERO > ci/out/d972_b345_q3_checker_full.ok'");;
  D972EKQ3Check:=D972EKRead("ci/out/d972_b345_q3_checker_full.log",
                           "q3 checker");;
  if D972EKRead("ci/out/d972_b345_q3_checker_full.ok",
       "q3 checker sentinel")<>"D972_B345_Q3_CHECKER_FULL_EXIT_ZERO" or
     D972EKCount(D972EKQ3Check,"B345_Q3_CHECKER_PASS")<>1 then
    Error("157ek driver: q3 independent checker");
  fi;
  Exec("bash -o pipefail -c 'set -e; SECONDS=0; python3 -u -B search/d972_b345_lexfirst_block_target6_v2.py --q3 ci/out/d972_b345_q3_chief_v1.json --output ci/out/d972_b345_lexfirst_block_target6_v2.json --seconds 18000 2>&1 | tee ci/out/d972_b345_lexfirst_block_target6_v3_producer.log; producer_elapsed=$SECONDS; remaining=$((18000-SECONDS)); if [ $remaining -le 0 ]; then exit 97; fi; python3 -u -B search/check_d972_b345_lexfirst_block_target6_v3.py --q3 ci/out/d972_b345_q3_chief_v1.json --receipt ci/out/d972_b345_lexfirst_block_target6_v2.json --seconds $remaining 2>&1 | tee ci/out/d972_b345_lexfirst_block_target6_v3_checker.log; final_elapsed=$SECONDS; final_remaining=$((18000-final_elapsed)); if [ $final_remaining -le 0 ]; then exit 98; fi; printf \"producer_elapsed=%s\\nchecker_initial_remaining=%s\\nfinal_elapsed=%s\\nfinal_margin=%s\\n\" $producer_elapsed $remaining $final_elapsed $final_remaining > ci/out/d972_b345_lexfirst_block_target6_v3_timing.txt; printf %s D972_B345_LEXBLOCK_TARGET6_V3_MATH_EXIT_ZERO > ci/out/d972_b345_lexfirst_block_target6_v3_math.ok'");;
  if D972EKRead(D972EKMathOk,"math sentinel")<>
       "D972_B345_LEXBLOCK_TARGET6_V3_MATH_EXIT_ZERO" then
    Error("157ek driver: producer/checker common deadline");
  fi;
  D972EKProducerRaw:=D972EKRead(D972EKProducerLog,"producer log");;
  D972EKTerminalCount:=0;;
  for D972EKToken in [
      "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT",
      "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT",
      "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE",
      "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_INPUT"] do
    D972EKTerminalCount:=D972EKTerminalCount+
      D972EKCount(D972EKProducerRaw,D972EKToken);;
  od;
  if D972EKTerminalCount<>1 or
     D972EKCount(D972EKProducerRaw,
       "D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_PASS")<>1 then
    Error("157ek driver: producer terminal/exit markers");
  fi;
  D972EKCheckerRaw:=D972EKRead(D972EKCheckerLog,"checker log");;
  if D972EKCount(D972EKProducerRaw,
       "Traceback (most recent call last):")<>0 or
     D972EKCount(D972EKCheckerRaw,
       "Traceback (most recent call last):")<>0 or
     D972EKCount(D972EKCheckerRaw,
       "D972_B345_LEXBLOCK_TARGET6_V3_CHECKER_PASS")<>1 then
    Error("157ek driver: checker PASS marker");
  fi;
  D972EKTimingRaw:=D972EKRead(D972EKTiming,"common deadline timing");;
  if D972EKCount(D972EKTimingRaw,"producer_elapsed=")<>1 or
     D972EKCount(D972EKTimingRaw,"checker_initial_remaining=")<>1 or
     D972EKCount(D972EKTimingRaw,"final_elapsed=")<>1 or
     D972EKCount(D972EKTimingRaw,"final_margin=")<>1 then
    Error("157ek driver: common deadline ledger");
  fi;
  Print("B345_LEXBLOCK_TARGET6_V3_GHA_DRIVER_PASS mode=full artifact_sha256=",
    HexSHA256(D972EKRead(D972EKArtifact,"final artifact")),"\n");;
fi;
