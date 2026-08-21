#############################################################################
## 157em: bounded target-6 full-D2 dual column-generation driver v1.
#############################################################################

D972EMProducer := "search/d972_b345_target6_dual_colgen_v1.py";;
D972EMChecker := "search/check_d972_b345_target6_dual_colgen_v1.py";;
D972EMTask := "sol/luna_task_157em_b345_target6_dual_colgen.md";;
D972EMArtifact := "ci/out/d972_b345_target6_dual_colgen_v1.json";;
D972EMQ3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972EMQ3ArtifactSHA :=
  "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;

# The mutable current reply is deliberately absent.  Its digest is reported
# out of band after freeze, avoiding a reply/driver pin cycle.
D972EMSourcePins := [
  [D972EMProducer,
   "8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc",410757],
  [D972EMChecker,
   "08cee7be18128b1dcc1376012854a828695c19a97bd1495e4cb0d7f7ddea035e",228980],
  [D972EMTask,
   "60df04261bfd9f30928ed51b26bd501518c05eae43b0bb8ca08507e3b6c4ca99",43511],
  ["search/d972_b345_lexfirst_block_target6_v2.py",
   "ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a",148824],
  ["search/check_d972_b345_lexfirst_block_target6_v4.py",
   "f15a2beeaf1925c1ea4894ef5fae02de6973c36047a91915b7efd12f6d424533",21594],
  ["search/d972_b345_lexfirst_block_target6_gha_driver_v4.g",
   "fa288727c77dcbdd8061b066d4863babeaf160dbac8ca4f87ba602a6c7a58836",14899],
  ["sol/luna_task_157el_b345_lexfirst_block_checker_accounting_v4.md",
   "755861e724fbd66f88b59b9ad9808703f26e2c8016394cb49c0c9cb09ce1f88a",16945],
  ["sol/luna_reply_157el_b345_lexfirst_block_checker_accounting_v4.md",
   "af8b33dccc44881fae7533d633922899774738b7dd1c310afbfaeda967417cb6",16035],
  ["search/d972_b345_full_d2_dual_correlation_v2.py",
   "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f",42449],
  ["search/check_d972_b345_full_d2_dual_correlation_v2.py",
   "881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060",21933],
  ["search/d972_b345_full_d2_dual_correlation_gha_driver_v2.g",
   "5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde",13253],
  ["sol/luna_task_157eh_b345_full_d2_monitor_scope_repair.md",
   "5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e",15015],
  ["sol/luna_reply_157eh_b345_full_d2_monitor_scope_repair.md",
   "0b595d82e7fa84ce4ee59256e03ca813b55f36a5c0f90d012ad141554fc23bfa",10817],
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

D972EMSelfLog := "ci/out/d972_b345_target6_dual_colgen_v1_selftest.log";;
D972EMSelfOk := "ci/out/d972_b345_target6_dual_colgen_v1_selftest.ok";;
D972EMProducerLog := "ci/out/d972_b345_target6_dual_colgen_v1_producer.log";;
D972EMCheckerLog := "ci/out/d972_b345_target6_dual_colgen_v1_checker.log";;
D972EMMathOk := "ci/out/d972_b345_target6_dual_colgen_v1_math.ok";;
D972EMTiming := "ci/out/d972_b345_target6_dual_colgen_v1_timing.txt";;
D972EMQ3Child := "ci/out/d972_b345_target6_dual_colgen_v1_q3_child.g";;
D972EMQ3Log := "ci/out/d972_b345_target6_dual_colgen_v1_q3_child.log";;
D972EMQ3Ok := "ci/out/d972_b345_target6_dual_colgen_v1_q3_child.ok";;

D972EMRead := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("157em driver: missing ",label); fi;
  return raw;
end;;

D972EMRequirePin := function(row)
  local raw,got;
  if not IsList(row) or Length(row)<>3 or not IsString(row[1]) or
     not IsString(row[2]) or not IsInt(row[3]) or row[3]<=0 then
    Error("157em driver: malformed source pin");
  fi;
  raw:=D972EMRead(row[1],row[1]);; got:=HexSHA256(raw);;
  if Length(raw)<>row[3] or got<>row[2] then
    Error("157em driver: source pin drift ",row[1]," sha=",got,
          " bytes=",Length(raw));
  fi;
  return true;
end;;

D972EMCount := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157em driver: occurrence input");
  fi;
  n:=Length(text);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972EMWrite := function(path,text)
  local stream,got;
  stream:=OutputTextFile(path,false);;
  if stream=fail then Error("157em driver: child write open"); fi;
  SetPrintFormattingStatus(stream,false);; PrintTo(stream,text);;
  CloseStream(stream);; got:=StringFile(path);;
  if got=fail or got<>text then Error("157em driver: child readback"); fi;
  return true;
end;;

for D972EMSource in D972EMSourcePins do D972EMRequirePin(D972EMSource);; od;

D972EMSelf:=IsBound(D972_B345_TARGET6_DUAL_COLGEN_V1_SELFTEST) and
  D972_B345_TARGET6_DUAL_COLGEN_V1_SELFTEST=true;;
D972EMRun:=IsBound(D972_B345_TARGET6_DUAL_COLGEN_V1_RUN) and
  D972_B345_TARGET6_DUAL_COLGEN_V1_RUN=true;;
if D972EMSelf=D972EMRun then
  Error("157em driver: select exactly one boolean mode");
fi;
if IsBound(D972_B345_TARGET6_DUAL_COLGEN_V1_OUTPUT) and
   D972_B345_TARGET6_DUAL_COLGEN_V1_OUTPUT<>D972EMArtifact then
  Error("157em driver: optional output differs from frozen artifact");
fi;

if D972EMSelf then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_target6_dual_colgen_v1_selftest.log' 'ci/out/d972_b345_target6_dual_colgen_v1_selftest.ok' && python3 -u -B 'search/d972_b345_target6_dual_colgen_v1.py' --self-test > 'ci/out/d972_b345_target6_dual_colgen_v1_selftest.log' 2>&1 && python3 -u -B 'search/check_d972_b345_target6_dual_colgen_v1.py' --self-test >> 'ci/out/d972_b345_target6_dual_colgen_v1_selftest.log' 2>&1 && printf '%s' 'D972_B345_TARGET6_DUAL_COLGEN_V1_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b345_target6_dual_colgen_v1_selftest.ok'");;
  if D972EMRead(D972EMSelfOk,"selftest sentinel")<>
       "D972_B345_TARGET6_DUAL_COLGEN_V1_SELFTEST_EXIT_ZERO" then
    Error("157em driver: selftest sentinel");
  fi;
  D972EMSelfRaw:=D972EMRead(D972EMSelfLog,"selftest log");;
  if D972EMCount(D972EMSelfRaw,"Traceback (most recent call last):")<>0 or
     D972EMCount(D972EMSelfRaw,
       "D972_B345_TARGET6_DUAL_COLGEN_V1_PRODUCER_SELFTEST_PASS")<>1 or
     D972EMCount(D972EMSelfRaw,
       "D972_B345_TARGET6_DUAL_COLGEN_V1_CHECKER_SELFTEST_PASS")<>1 or
     D972EMCount(D972EMSelfRaw,
       "D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_SELFTEST_PASS")<>1 or
     D972EMCount(D972EMSelfRaw,
       "D972_B345_LEXBLOCK_TARGET6_V4_CHECKER_SELFTEST_PASS")<>1 or
     D972EMCount(D972EMSelfRaw,
       "D972_B345_FULL_D2_DUAL_CORRELATION_V2_PRODUCER_SELFTEST_PASS")<>1 or
     D972EMCount(D972EMSelfRaw,
       "D972_B345_FULL_D2_DUAL_CORRELATION_V2_CHECKER_SELFTEST_PASS")<>1 or
     D972EMCount(D972EMSelfRaw,"prefix_provider=1")<>1 or
     D972EMCount(D972EMSelfRaw,"reverse_lift=1 correlation=2")<>1 or
     D972EMCount(D972EMSelfRaw,"section_inverse=1")<>1 or
     D972EMCount(D972EMSelfRaw,
       "recovery=1 stage_batch=1 commit_batch=1 incremental109=1")<>1 or
     D972EMCount(D972EMSelfRaw,"incremental_order=1")<>1 or
     D972EMCount(D972EMSelfRaw,"transaction_rollback=1")<>1 or
     D972EMCount(D972EMSelfRaw,"positive_prefix_offset=1")<>1 or
     D972EMCount(D972EMSelfRaw,"fixture_blob_decoder=1")<>1 or
     D972EMCount(D972EMSelfRaw,"packed_225=1 terminals=4 checked_write=1")<>1 or
     D972EMCount(D972EMSelfRaw,"independent_reverse_lift=1")<>1 or
     D972EMCount(D972EMSelfRaw,"independent_correlation=1")<>1 or
     D972EMCount(D972EMSelfRaw,"incremental_all109=1")<>1 or
     D972EMCount(D972EMSelfRaw,"lifecycle_reuse=1")<>1 or
     D972EMCount(D972EMSelfRaw,"typed_stage_core=1")<>1 or
     D972EMCount(D972EMSelfRaw,"typed_stage_mutations=2")<>1 or
     D972EMCount(D972EMSelfRaw,"fixture_scope_repairs=3")<>1 then
    Error("157em driver: combined/inherited/production-core markers");
  fi;
  Print(D972EMSelfRaw,
    "\nB345_TARGET6_DUAL_COLGEN_V1_GHA_DRIVER_PASS mode=selftest\n");;
else
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b345_lexfirst_block_target6_v2.json' 'ci/out/d972_b345_target6_dual_colgen_v1.json' 'ci/out/d972_b345_target6_dual_colgen_v1_q3_child.g' 'ci/out/d972_b345_target6_dual_colgen_v1_q3_child.log' 'ci/out/d972_b345_target6_dual_colgen_v1_q3_child.ok' 'ci/out/d972_b345_target6_dual_colgen_v1_producer.log' 'ci/out/d972_b345_target6_dual_colgen_v1_checker.log' 'ci/out/d972_b345_target6_dual_colgen_v1_math.ok' 'ci/out/d972_b345_target6_dual_colgen_v1_timing.txt'");;
  D972EMQ3Text:=Concatenation(
    "if GAPInfo.Version<>\"4.16.0\" then Error(\"GAP 4.16.0 required\"); fi;;\n",
    "if LoadPackage(\"smallgrp\")<>true then Error(\"smallgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"autpgrp\")<>true then Error(\"autpgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"anupq\")<>true then Error(\"anupq LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"json\")<>true then Error(\"json LoadPackage failed\"); fi;;\n",
    "D972_B345_Q3_RUN:=true;; D972_B345_Q3_OUTPUT:=\"ci/out/d972_b345_q3_chief_v1.json\";;\n",
    "Read(\"search/d972_b345_q3_gha_driver_v1.g\");; QUIT_GAP(0);;\n");;
  D972EMWrite(D972EMQ3Child,D972EMQ3Text);;
  Exec("bash -o pipefail -c 'gap -l \";/usr/share/gap;/usr/lib/gap;${GAP_P2_PACKAGE_ROOT:?}\" --quitonbreak -q -o 12g ci/out/d972_b345_target6_dual_colgen_v1_q3_child.g 2>&1 | tee ci/out/d972_b345_target6_dual_colgen_v1_q3_child.log' && printf '%s' 'D972_B345_TARGET6_DUAL_COLGEN_V1_Q3_EXIT_ZERO' > 'ci/out/d972_b345_target6_dual_colgen_v1_q3_child.ok'");;
  if D972EMRead(D972EMQ3Ok,"q3 sentinel")<>
       "D972_B345_TARGET6_DUAL_COLGEN_V1_Q3_EXIT_ZERO" then
    Error("157em driver: q3 child");
  fi;
  D972EMQ3Raw:=D972EMRead(D972EMQ3Artifact,"q3 artifact");;
  if HexSHA256(D972EMQ3Raw)<>D972EMQ3ArtifactSHA then
    Error("157em driver: q3 artifact SHA");
  fi;
  Exec("bash -o pipefail -c 'python3 -u -B \"search/check_d972_b345_q3_chief_v1.py\" \"ci/out/d972_b345_q3_chief_v1.json\" > \"ci/out/d972_b345_q3_checker_full.log\" 2>&1 && printf %s D972_B345_Q3_CHECKER_FULL_EXIT_ZERO > \"ci/out/d972_b345_q3_checker_full.ok\"'");;
  D972EMQ3Check:=D972EMRead("ci/out/d972_b345_q3_checker_full.log",
                           "q3 checker");;
  if D972EMRead("ci/out/d972_b345_q3_checker_full.ok",
       "q3 checker sentinel")<>"D972_B345_Q3_CHECKER_FULL_EXIT_ZERO" or
     D972EMCount(D972EMQ3Check,"B345_Q3_CHECKER_PASS")<>1 then
    Error("157em driver: q3 independent checker");
  fi;
  Exec("bash -o pipefail -c 'set -e; SECONDS=0; python3 -u -B \"search/d972_b345_target6_dual_colgen_v1.py\" --q3 \"ci/out/d972_b345_q3_chief_v1.json\" --output \"ci/out/d972_b345_target6_dual_colgen_v1.json\" --seconds 18000 2>&1 | tee \"ci/out/d972_b345_target6_dual_colgen_v1_producer.log\"; producer_elapsed=$SECONDS; remaining=$((18000-SECONDS)); if [ $remaining -le 0 ]; then exit 97; fi; python3 -u -B \"search/check_d972_b345_target6_dual_colgen_v1.py\" --q3 \"ci/out/d972_b345_q3_chief_v1.json\" --receipt \"ci/out/d972_b345_target6_dual_colgen_v1.json\" --seconds $remaining 2>&1 | tee \"ci/out/d972_b345_target6_dual_colgen_v1_checker.log\"; final_elapsed=$SECONDS; final_remaining=$((18000-final_elapsed)); if [ $final_remaining -le 0 ]; then exit 98; fi; printf \"producer_elapsed=%s\\nchecker_initial_remaining=%s\\nfinal_elapsed=%s\\nfinal_margin=%s\\n\" $producer_elapsed $remaining $final_elapsed $final_remaining > \"ci/out/d972_b345_target6_dual_colgen_v1_timing.txt\"; printf %s D972_B345_TARGET6_DUAL_COLGEN_V1_MATH_EXIT_ZERO > \"ci/out/d972_b345_target6_dual_colgen_v1_math.ok\"'");;
  if D972EMRead(D972EMMathOk,"math sentinel")<>
       "D972_B345_TARGET6_DUAL_COLGEN_V1_MATH_EXIT_ZERO" then
    Error("157em driver: producer/checker common deadline");
  fi;
  D972EMProducerRaw:=D972EMRead(D972EMProducerLog,"producer log");;
  D972EMTerminalCount:=0;;
  for D972EMToken in [
      "B345_E4_D2_COLGEN_TARGET6_CONSISTENT",
      "B345_E4_D2_COLGEN_TARGET6_FULL_D2_OBSTRUCTION",
      "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_RESOURCE",
      "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_INPUT"] do
    D972EMTerminalCount:=D972EMTerminalCount+
      D972EMCount(D972EMProducerRaw,D972EMToken);;
  od;
  if D972EMTerminalCount<>1 or
     D972EMCount(D972EMProducerRaw,
       "D972_B345_TARGET6_DUAL_COLGEN_V1_PRODUCER_PASS")<>1 or
     D972EMCount(D972EMProducerRaw,"D972_B345_DUAL_COLGEN_PHASE ")<1 then
    Error("157em driver: producer terminal/progress/PASS markers");
  fi;
  D972EMReceiptRaw:=D972EMRead(D972EMArtifact,"final artifact");;
  D972EMReceiptSHA:=HexSHA256(D972EMReceiptRaw);;
  if D972EMCount(D972EMProducerRaw,
       Concatenation("sha256=",D972EMReceiptSHA))<>1 or
     D972EMCount(D972EMProducerRaw,
       Concatenation("bytes=",String(Length(D972EMReceiptRaw))))<>1 then
    Error("157em driver: producer/artifact hash or byte mismatch");
  fi;
  D972EMCheckerRaw:=D972EMRead(D972EMCheckerLog,"checker log");;
  if D972EMCount(D972EMProducerRaw,
       "Traceback (most recent call last):")<>0 or
     D972EMCount(D972EMCheckerRaw,
       "Traceback (most recent call last):")<>0 or
     D972EMCount(D972EMCheckerRaw,
       "D972_B345_TARGET6_DUAL_COLGEN_V1_CHECKER_PASS")<>1 then
    Error("157em driver: checker PASS marker");
  fi;
  D972EMTimingRaw:=D972EMRead(D972EMTiming,"common deadline timing");;
  if D972EMCount(D972EMTimingRaw,"producer_elapsed=")<>1 or
     D972EMCount(D972EMTimingRaw,"checker_initial_remaining=")<>1 or
     D972EMCount(D972EMTimingRaw,"final_elapsed=")<>1 or
     D972EMCount(D972EMTimingRaw,"final_margin=")<>1 then
    Error("157em driver: common deadline ledger");
  fi;
  Print("B345_TARGET6_DUAL_COLGEN_V1_GHA_DRIVER_PASS mode=full artifact_sha256=",
    D972EMReceiptSHA," bytes=",Length(D972EMReceiptRaw),"\n");;
fi;
