#############################################################################
## 157en: producer-only target-6 dual column-generation Stage-P driver v2.
#############################################################################

D972EMProducer := "search/d972_b345_target6_dual_colgen_v2.py";;
D972EMChecker := "search/check_d972_b345_target6_dual_colgen_v2.py";;
D972EMTask := "sol/luna_task_157en_b345_target6_dual_colgen_v2.md";;
D972EMArtifact := "ci/out/d972_b345_target6_dual_colgen_v2.json";;
D972EMQ3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972EMQ3ArtifactSHA :=
  "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;

# The mutable current reply is deliberately absent.  Its digest is reported
# out of band after freeze, avoiding a reply/driver pin cycle.
D972EMSourcePins := [
  [D972EMProducer,
   "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7",444497],
  [D972EMChecker,
   "9b135f22f8687532a10d42c2332b65239709a74df4b9d0de74b17da0430ec99f",275320],
  [D972EMTask,
   "0c650d358662d3d8e3eaf8fa67eac50ff8d64e35522348cfe634ead02f7c0ee8",16017],
  ["search/d972_b345_target6_dual_colgen_v1.py",
   "8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc",410757],
  ["search/check_d972_b345_target6_dual_colgen_v1.py",
   "08cee7be18128b1dcc1376012854a828695c19a97bd1495e4cb0d7f7ddea035e",228980],
  ["search/d972_b345_target6_dual_colgen_gha_driver_v1.g",
   "e67d6397fca2b7181710fe8baf5893f8273399dc43b6c4ec27caebe4f1a903dc",14634],
  ["sol/luna_task_157em_b345_target6_dual_colgen.md",
   "60df04261bfd9f30928ed51b26bd501518c05eae43b0bb8ca08507e3b6c4ca99",43511],
  ["sol/luna_reply_157em_b345_target6_dual_colgen.md",
   "70fc6a91a1e10316b5ef2c8ad497e4fc61479866de28b80e0402de92c1065b58",39427],
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

D972EMProducerLog := "ci/out/d972_b345_target6_dual_colgen_v2_producer.log";;
D972EMMathOk := "ci/out/d972_b345_target6_dual_colgen_v2_producer_stage.ok";;
D972EMTiming := "ci/out/d972_b345_target6_dual_colgen_v2_producer_timing.txt";;
D972EMQ3Child := "ci/out/d972_b345_target6_dual_colgen_v2_q3_child.g";;
D972EMQ3Log := "ci/out/d972_b345_target6_dual_colgen_v2_q3_child.log";;
D972EMQ3Ok := "ci/out/d972_b345_target6_dual_colgen_v2_q3_child.ok";;
D972EMProductionCommand := "bash -o pipefail -c 'set -e; SECONDS=0; python3 -u -B \"search/d972_b345_target6_dual_colgen_v2.py\" --q3 \"ci/out/d972_b345_q3_chief_v1.json\" --output \"ci/out/d972_b345_target6_dual_colgen_v2.json\" --seconds 18000 2>&1 | tee \"ci/out/d972_b345_target6_dual_colgen_v2_producer.log\"; producer_elapsed=$SECONDS; final_margin=$((18000-producer_elapsed)); printf \"producer_elapsed=%s\\nfinal_margin=%s\\ntarget6_v2_checker_processes=0\\nsoft_deadline_seconds=18000\\n\" $producer_elapsed $final_margin > \"ci/out/d972_b345_target6_dual_colgen_v2_producer_timing.txt\"; printf %s D972_B345_TARGET6_DUAL_COLGEN_V2_PRODUCER_STAGE_EXIT_ZERO > \"ci/out/d972_b345_target6_dual_colgen_v2_producer_stage.ok\"'";;

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

D972EMShellQuote := function(path)
  if not IsString(path) or Length(path)=0 or
     PositionSublist(path,"'")<>fail or PositionSublist(path,"\n")<>fail or
     PositionSublist(path,"\r")<>fail then
    Error("157en driver: unsafe selftest shell path");
  fi;
  return Concatenation("'",path,"'");
end;;

for D972EMSource in D972EMSourcePins do D972EMRequirePin(D972EMSource);; od;
if PositionSublist(D972EMProductionCommand,D972EMChecker)<>fail or
   PositionSublist(D972EMProductionCommand," --receipt ")<>fail or
   PositionSublist(D972EMProductionCommand,"exit 97")<>fail then
  Error("157en driver: producer-only command shape");
fi;

D972EMSelf:=IsBound(D972_B345_TARGET6_DUAL_COLGEN_V2_PRODUCER_SELFTEST) and
  D972_B345_TARGET6_DUAL_COLGEN_V2_PRODUCER_SELFTEST=true;;
D972EMRun:=IsBound(D972_B345_TARGET6_DUAL_COLGEN_V2_PRODUCER_RUN) and
  D972_B345_TARGET6_DUAL_COLGEN_V2_PRODUCER_RUN=true;;
if D972EMSelf=D972EMRun then
  Error("157em driver: select exactly one boolean mode");
fi;
if IsBound(D972_B345_TARGET6_DUAL_COLGEN_V2_OUTPUT) and
   D972_B345_TARGET6_DUAL_COLGEN_V2_OUTPUT<>D972EMArtifact then
  Error("157em driver: optional output differs from frozen artifact");
fi;

if D972EMSelf then
  # All five self-test artifacts live in one OS temporary directory outside
  # the repository.  Production paths and the literal Stage-P command above
  # remain unchanged.
  D972EMSelfDirectory:=DirectoryTemporary();;
  if D972EMSelfDirectory=fail then
    Error("157en driver: no absolute OS temporary directory");
  fi;
  D972EMSelfRoot:=Filename(D972EMSelfDirectory,"");;
  D972EMSelfArtifact:=Filename(D972EMSelfDirectory,
    "d972_b345_target6_dual_colgen_v2.json");;
  D972EMSelfProducerLog:=Filename(D972EMSelfDirectory,
    "d972_b345_target6_dual_colgen_v2_producer.log");;
  D972EMSelfMathOk:=Filename(D972EMSelfDirectory,
    "d972_b345_target6_dual_colgen_v2_producer_stage.ok");;
  D972EMSelfLog:=Filename(D972EMSelfDirectory,
    "d972_b345_target6_dual_colgen_v2_preP_selftest.log");;
  D972EMSelfOk:=Filename(D972EMSelfDirectory,
    "d972_b345_target6_dual_colgen_v2_preP_selftest.ok");;
  D972EMSelfPaths:=[D972EMSelfArtifact,D972EMSelfProducerLog,
    D972EMSelfMathOk,D972EMSelfLog,D972EMSelfOk];;
  D972EMRepoRoot:=Filename(DirectoryCurrent(),"");;
  if not IsString(D972EMSelfRoot) or Length(D972EMSelfRoot)=0 or
     Length(Set(D972EMSelfPaths))<>5 or
     ForAny(D972EMSelfPaths,x->not IsString(x) or
       PositionSublist(x,D972EMSelfRoot)<>1 or
       PositionSublist(x,D972EMRepoRoot)=1) then
    Error("157en driver: selftest paths not in one external temp directory");
  fi;
  D972EMWrite(D972EMSelfArtifact,"stale-receipt");;
  D972EMWrite(D972EMSelfProducerLog,"stale-log");;
  D972EMWrite(D972EMSelfMathOk,"stale-sentinel");;
  for D972EMSelfPath in D972EMSelfPaths do
    if IsExistingFile(D972EMSelfPath) then RemoveFile(D972EMSelfPath);; fi;
  od;
  if ForAny(D972EMSelfPaths,IsExistingFile) then
    Error("157en driver: stale Stage-P output survived cleanup");
  fi;
  # The combined source boundary intentionally runs P then C.  The production
  # command below is a separate literal and contains no v2 checker process.
  D972EMSelfCommand:=Concatenation(
    "python3 -u -B 'search/d972_b345_target6_dual_colgen_v2.py' --self-test > ",
    D972EMShellQuote(D972EMSelfLog)," 2>&1 && ",
    "python3 -u -B 'search/check_d972_b345_target6_dual_colgen_v2.py' --self-test >> ",
    D972EMShellQuote(D972EMSelfLog)," 2>&1 && printf '%s' ",
    "'D972_B345_TARGET6_DUAL_COLGEN_V2_PREP_SELFTEST_EXIT_ZERO' > ",
    D972EMShellQuote(D972EMSelfOk));;
  Exec(D972EMSelfCommand);;
  if not IsExistingFile(D972EMSelfOk) then
    if IsExistingFile(D972EMSelfLog) then
      Print(D972EMRead(D972EMSelfLog,"failed selftest log"),"\n");;
    fi;
    Error("157em driver: missing selftest sentinel");
  fi;
  if D972EMRead(D972EMSelfOk,"selftest sentinel")<>
       "D972_B345_TARGET6_DUAL_COLGEN_V2_PREP_SELFTEST_EXIT_ZERO" then
    Error("157em driver: selftest sentinel");
  fi;
  D972EMSelfRaw:=D972EMRead(D972EMSelfLog,"selftest log");;
  if D972EMCount(D972EMSelfRaw,"Traceback (most recent call last):")<>0 or
     D972EMCount(D972EMSelfRaw,
       "D972_B345_TARGET6_DUAL_COLGEN_V2_PRODUCER_SELFTEST_PASS")<>1 or
     D972EMCount(D972EMSelfRaw,
       "D972_B345_TARGET6_DUAL_COLGEN_V2_CHECKER_SELFTEST_PASS")<>1 or
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
     D972EMCount(D972EMSelfRaw,"prefix_provider=1")<>2 or
     D972EMCount(D972EMSelfRaw,"old_module_lifecycle=3")<>1 or
     D972EMCount(D972EMSelfRaw,
       "summary_key_modes=2 summary_key_mutations=4")<>1 or
     D972EMCount(D972EMSelfRaw,"reverse_lift=1 correlation=2")<>2 or
     D972EMCount(D972EMSelfRaw,"section_inverse=1")<>2 or
     D972EMCount(D972EMSelfRaw,
       "recovery=1 stage_batch=1 commit_batch=1 incremental109=1")<>2 or
     D972EMCount(D972EMSelfRaw,"incremental_order=1")<>2 or
     D972EMCount(D972EMSelfRaw,"transaction_rollback=1")<>2 or
     D972EMCount(D972EMSelfRaw,"positive_prefix_offset=1")<>2 or
     D972EMCount(D972EMSelfRaw,"fixture_blob_decoder=1")<>2 or
     D972EMCount(D972EMSelfRaw,"packed_225=1 terminals=4 checked_write=1")<>2 or
     D972EMCount(D972EMSelfRaw,"independent_reverse_lift=1")<>2 or
     D972EMCount(D972EMSelfRaw,"independent_correlation=1")<>2 or
     D972EMCount(D972EMSelfRaw,"incremental_all109=1")<>2 or
     D972EMCount(D972EMSelfRaw,"lifecycle_reuse=1")<>2 or
     D972EMCount(D972EMSelfRaw,"typed_stage_core=1")<>2 or
     D972EMCount(D972EMSelfRaw,"typed_stage_mutations=2")<>2 or
     D972EMCount(D972EMSelfRaw,"fixture_scope_repairs=3")<>2 then
    Error("157em driver: combined/inherited/production-core markers");
  fi;
  if D972EMCount(D972EMSelfRaw,"semantic_remainders=1")<>2 or
     D972EMCount(D972EMSelfRaw,"semantic_mutations=4")<>2 or
     D972EMCount(D972EMSelfRaw,"generation_13_resource=1")<>2 or
     D972EMCount(D972EMSelfRaw,"cap12_resource_envelope=1")<>2 or
     D972EMCount(D972EMSelfRaw,
       "completed_initial_resource_envelope=1")<>2 then
    Error("157en driver: semantic/cap repair markers");
  fi;
  Print(D972EMSelfRaw,
    "\nB345_TARGET6_DUAL_COLGEN_V2_PRODUCER_GHA_DRIVER_PASS mode=selftest target6_v2_checker_process_in_production=0 q3_checker_processes=1 stale_outputs_removed=3 selftest_temp_paths=5\n");;
else
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b345_lexfirst_block_target6_v2.json' 'ci/out/d972_b345_target6_dual_colgen_v2.json' 'ci/out/d972_b345_target6_dual_colgen_v2_q3_child.g' 'ci/out/d972_b345_target6_dual_colgen_v2_q3_child.log' 'ci/out/d972_b345_target6_dual_colgen_v2_q3_child.ok' 'ci/out/d972_b345_target6_dual_colgen_v2_producer.log' 'ci/out/d972_b345_target6_dual_colgen_v2_producer_stage.ok' 'ci/out/d972_b345_target6_dual_colgen_v2_producer_timing.txt'");;
  D972EMQ3Text:=Concatenation(
    "if GAPInfo.Version<>\"4.16.0\" then Error(\"GAP 4.16.0 required\"); fi;;\n",
    "if LoadPackage(\"smallgrp\")<>true then Error(\"smallgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"autpgrp\")<>true then Error(\"autpgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"anupq\")<>true then Error(\"anupq LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"json\")<>true then Error(\"json LoadPackage failed\"); fi;;\n",
    "D972_B345_Q3_RUN:=true;; D972_B345_Q3_OUTPUT:=\"ci/out/d972_b345_q3_chief_v1.json\";;\n",
    "Read(\"search/d972_b345_q3_gha_driver_v1.g\");; QUIT_GAP(0);;\n");;
  D972EMWrite(D972EMQ3Child,D972EMQ3Text);;
  Exec("bash -o pipefail -c 'gap -l \";/usr/share/gap;/usr/lib/gap;${GAP_P2_PACKAGE_ROOT:?}\" --quitonbreak -q -o 12g ci/out/d972_b345_target6_dual_colgen_v2_q3_child.g 2>&1 | tee ci/out/d972_b345_target6_dual_colgen_v2_q3_child.log' && printf '%s' 'D972_B345_TARGET6_DUAL_COLGEN_V2_Q3_EXIT_ZERO' > 'ci/out/d972_b345_target6_dual_colgen_v2_q3_child.ok'");;
  if D972EMRead(D972EMQ3Ok,"q3 sentinel")<>
       "D972_B345_TARGET6_DUAL_COLGEN_V2_Q3_EXIT_ZERO" then
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
  Exec(D972EMProductionCommand);;
  if D972EMRead(D972EMMathOk,"math sentinel")<>
       "D972_B345_TARGET6_DUAL_COLGEN_V2_PRODUCER_STAGE_EXIT_ZERO" then
    Error("157en driver: producer-only deadline/sentinel");
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
       "D972_B345_TARGET6_DUAL_COLGEN_V2_PRODUCER_PASS")<>1 or
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
  if D972EMCount(D972EMProducerRaw,
       "Traceback (most recent call last):")<>0 then
    Error("157en driver: producer traceback");
  fi;
  D972EMTimingRaw:=D972EMRead(D972EMTiming,"producer-only timing");;
  if D972EMCount(D972EMTimingRaw,"producer_elapsed=")<>1 or
     D972EMCount(D972EMTimingRaw,"final_margin=")<>1 or
     D972EMCount(D972EMTimingRaw,"target6_v2_checker_processes=0")<>1 or
     D972EMCount(D972EMTimingRaw,"soft_deadline_seconds=18000")<>1 then
    Error("157en driver: producer-only deadline ledger");
  fi;
  Print("B345_TARGET6_DUAL_COLGEN_V2_PRODUCER_GHA_DRIVER_PASS mode=full artifact_sha256=",
    D972EMReceiptSHA," bytes=",Length(D972EMReceiptRaw),
    " target6_v2_checker_processes=0 q3_checker_processes=1\n");;
fi;
