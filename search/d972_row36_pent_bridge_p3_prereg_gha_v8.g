#############################################################################
## P3 fixed-row36 outcome-free paper/native orientation prereg wrapper v8.
#############################################################################

P159OR36P3V8RequireSha:=function(path,expected)
  local raw,actual;
  raw:=StringFile(path);
  if raw=fail then
    Error("PENT159O_ROW36_P3_V8: missing immutable input ",path);
  fi;
  actual:=HexSHA256(raw);
  if actual<>expected then
    Error("PENT159O_ROW36_P3_V8: immutable input hash mismatch ",path,
      " expected=",expected," actual=",actual);
  fi;
  Print("PENT159O_ROW36_P3_V8_PIN_PASS path=",path," bytes=",Length(raw),
    " sha256=",actual,"\n");
end;

P159OR36P3V8RequireSha("search/d972_row36_pent_bridge_common_v1.py",
  "d3e27775b59baa150c255c15feb2ab5809bdc299265278772f0428d2f1de0a79");
P159OR36P3V8RequireSha("search/d972_row36_pent_bridge_common_v2.py",
  "46ab60bf06e1bec03725a69349914e4bd9e786c41ce0946b0387f74493a55ecc");
P159OR36P3V8RequireSha("search/d972_row36_pent_bridge_common_v3.py",
  "95ff60fe351aa0020aa5353d805cd8588c7d16cbfc45acdca862097d67cafcb5");
P159OR36P3V8RequireSha("search/d972_row36_pent_bridge_common_p3_v6.py",
  "f6ac99a0d55394d675cab43690631b528a8e95270b7abfe432a94b321c411ab1");
P159OR36P3V8RequireSha("search/d972_row36_pent_bridge_p3_producer_v6.py",
  "5d557a642e34274462750e466795650a608810e6555964736c5e92aac911e2a2");
P159OR36P3V8RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_v6.g",
  "0133616171025f250bdc2f89dab0b56c0af920dc88f5b396631b5fe5f05ba7d1");
P159OR36P3V8RequireSha("search/d972_row36_pent_bridge_common_p3_v7.py",
  "bcfafa18e646d9ac2ef4b5b3d8693a1547da761a34335f6f0c2643938baf270c");
P159OR36P3V8RequireSha("search/d972_row36_pent_bridge_p3_producer_v7.py",
  "b1fba6374d37608a0e1faef4ad7ed6087c25b84c2bde33a6903cb37926111acc");
P159OR36P3V8RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_generator_v7.py",
  "6ab35d7a2fd4d9c3b1a7a5ed4dc5c0597ff199b1cea1faa6fd3b5a652834fe36");
P159OR36P3V8RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_v7.g",
  "de654fc73fb3d69f7736c97b48b04619122bdca04c015817ff07c27a321f6768");
P159OR36P3V8RequireSha("search/d972_row36_pent_bridge_common_p3_v8.py",
  "46194661f3d80c5d95025a3e4efad3b0ba25a28d9f77657d554060cb070e3d9e");
P159OR36P3V8RequireSha("search/d972_row36_pent_bridge_p3_producer_v8.py",
  "bd1911b1b9f2a3665e81529694be8e6d421d93a713644c6355e9f360ed7b6a3b");
P159OR36P3V8RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_generator_v8.py",
  "2c56f5a77e5809f5976778739cab3487d30bb58074d171c74fd59ee6f9fcd27b");
P159OR36P3V8RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_v8.g",
  "dc87c6872a68141f30be15ebad05d9ea12f343347fdf953e944d335294559035");
P159OR36P3V8RequireSha(
  "ci/pent159n_p3_v5_artifacts_32661138818/d972_pent_interleave_canary_p3_receipt_v5_20260824.json",
  "8838dbfecbb8f487265801de860c91207de56e4acf5e98088e6d9cd161390530");
P159OR36P3V8RequireSha(
  "crosscheck/verdicts/d972_pent_interleave_canary_crosscheck_p3_v2_20260824.json",
  "73d4cb3f242d74f796021af922e1771c68f9256bcddedcbe2a277539f79c2781");

P159OR36P3V8ResultPath:=
  "ci/out/d972_row36_pent_bridge_p3_transition_results_v8_20260824.json";;
P159OR36P3V8RepoPreregPath:=
  "search/certs/d972_row36_pent_bridge_p3_prereg_v8_20260824.json";;
P159OR36P3V8ArtifactPreregPath:=
  "ci/out/d972_row36_pent_bridge_p3_prereg_v8_20260824.json";;
P159OR36P3V8PythonLogPath:=
  "ci/out/d972_row36_pent_bridge_p3_python_prepare_v8.log";;

if StringFile(P159OR36P3V8ResultPath)<>fail or
   StringFile(P159OR36P3V8RepoPreregPath)<>fail or
   StringFile(P159OR36P3V8ArtifactPreregPath)<>fail or
   StringFile(P159OR36P3V8PythonLogPath)<>fail then
  Error("PENT159O_ROW36_P3_V8: pre-existing versioned output");
fi;

Print("PENT159O_ROW36_P3_V8_WORKER_START outcome_free=true states=2187 serialization=explicit_base3_lex transition_sides=native_right_and_paper_left quotient_rerun=false\n");
Read("search/d972_row36_pent_bridge_p3_transition_worker_v8.g");
P159OR36P3V8Result:=StringFile(P159OR36P3V8ResultPath);;
if P159OR36P3V8Result=fail then
  Error("PENT159O_ROW36_P3_V8: transition result absent");
fi;
Print("PENT159O_ROW36_P3_V8_TRANSITION_RESULT_PRESENT path=",
  P159OR36P3V8ResultPath," bytes=",Length(P159OR36P3V8Result),
  " sha256=",HexSHA256(P159OR36P3V8Result),"\n");

Print("PENT159O_ROW36_P3_V8_PYTHON_PREPARE_START raw_rows=34992 predicates=false\n");
Exec(Concatenation(
  "python3 search/d972_row36_pent_bridge_p3_producer_v8.py prepare > ",
  P159OR36P3V8PythonLogPath," 2>&1"));
P159OR36P3V8PythonLog:=StringFile(P159OR36P3V8PythonLogPath);;
if P159OR36P3V8PythonLog=fail then
  Error("PENT159O_ROW36_P3_V8: Python prepare log absent");
fi;
Print("PENT159O_ROW36_P3_V8_PYTHON_LOG_BEGIN\n");
Print(P159OR36P3V8PythonLog);
Print("PENT159O_ROW36_P3_V8_PYTHON_LOG_END\n");
for P159OR36P3V8Forbidden in
  ["Traceback","SyntaxError","MemoryError","Killed",
   "PENT159O_ROW36_P3_V1_STATE_STOP"] do
  if PositionSublist(P159OR36P3V8PythonLog,P159OR36P3V8Forbidden)<>fail then
    Error("PENT159O_ROW36_P3_V8: forbidden Python diagnostic ",
      P159OR36P3V8Forbidden);
  fi;
od;
if PositionSublist(P159OR36P3V8PythonLog,
     "PENT159O_ROW36_P3_V1_PREREG_WRITTEN")=fail or
   PositionSublist(P159OR36P3V8PythonLog,
     "PENT159O_ROW36_P3_V1_PREPARE_PASS")=fail then
  Error("PENT159O_ROW36_P3_V8: Python prepare terminal markers absent");
fi;

P159OR36P3V8Prereg:=StringFile(P159OR36P3V8RepoPreregPath);;
if P159OR36P3V8Prereg=fail then
  Error("PENT159O_ROW36_P3_V8: repository preregistration absent");
fi;
for P159OR36P3V8Required in
  ["\"schema\":\"d972-row36-pent-bridge-p3-prereg/v8\"",
   "\"raw_count\":34992",
   "\"expected_count\":34992",
   "\"canonical_section_derivation_serialized\":true",
   "\"predicate_outcomes_evaluated\":false",
   "\"paper_projection_signed_replay_count\":2187",
   "\"native_product_bridge_rows\":8748",
   "\"all_34992_rows_reference_the_frozen_section_word_for_their_kernel_coordinate\":true",
   "\"terminal_token\":\"PENT159O_ROW36_P3_PREREG_V8_FROZEN\""] do
  if PositionSublist(P159OR36P3V8Prereg,P159OR36P3V8Required)=fail then
    Error("PENT159O_ROW36_P3_V8: required preregistration token absent ",
      P159OR36P3V8Required);
  fi;
od;

P159OR36P3V8Out:=OutputTextFile(P159OR36P3V8ArtifactPreregPath,false);;
if P159OR36P3V8Out=fail then
  Error("PENT159O_ROW36_P3_V8: cannot open artifact preregistration");
fi;
SetPrintFormattingStatus(P159OR36P3V8Out,false);
PrintTo(P159OR36P3V8Out,P159OR36P3V8Prereg);
CloseStream(P159OR36P3V8Out);
P159OR36P3V8ArtifactPrereg:=StringFile(P159OR36P3V8ArtifactPreregPath);;
if P159OR36P3V8ArtifactPrereg=fail or
   P159OR36P3V8ArtifactPrereg<>P159OR36P3V8Prereg then
  Error("PENT159O_ROW36_P3_V8: artifact preregistration copy drift");
fi;

Print("PENT159O_ROW36_P3_V8_PREREG_WRITTEN path=",
  P159OR36P3V8ArtifactPreregPath," bytes=",Length(P159OR36P3V8ArtifactPrereg),
  " sha256=",HexSHA256(P159OR36P3V8ArtifactPrereg),"\n");
Print("PENT159O_ROW36_P3_V8_FINAL OUTCOME_FREE_PREREGISTRATION_FROZEN__PREDICATE_EXECUTION_NOT_RUN\n");
QUIT_GAP(0);
