#############################################################################
## P3 fixed-row36 outcome-free explicit-state preregistration wrapper v7.
#############################################################################

P159OR36P3V7RequireSha:=function(path,expected)
  local raw,actual;
  raw:=StringFile(path);
  if raw=fail then
    Error("PENT159O_ROW36_P3_V7: missing immutable input ",path);
  fi;
  actual:=HexSHA256(raw);
  if actual<>expected then
    Error("PENT159O_ROW36_P3_V7: immutable input hash mismatch ",path,
      " expected=",expected," actual=",actual);
  fi;
  Print("PENT159O_ROW36_P3_V7_PIN_PASS path=",path," bytes=",Length(raw),
    " sha256=",actual,"\n");
end;

P159OR36P3V7RequireSha("search/d972_row36_pent_bridge_common_v1.py",
  "d3e27775b59baa150c255c15feb2ab5809bdc299265278772f0428d2f1de0a79");
P159OR36P3V7RequireSha("search/d972_row36_pent_bridge_common_v2.py",
  "46ab60bf06e1bec03725a69349914e4bd9e786c41ce0946b0387f74493a55ecc");
P159OR36P3V7RequireSha("search/d972_row36_pent_bridge_common_v3.py",
  "95ff60fe351aa0020aa5353d805cd8588c7d16cbfc45acdca862097d67cafcb5");
P159OR36P3V7RequireSha("search/d972_row36_pent_bridge_common_p3_v6.py",
  "f6ac99a0d55394d675cab43690631b528a8e95270b7abfe432a94b321c411ab1");
P159OR36P3V7RequireSha("search/d972_row36_pent_bridge_p3_producer_v6.py",
  "5d557a642e34274462750e466795650a608810e6555964736c5e92aac911e2a2");
P159OR36P3V7RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_v6.g",
  "0133616171025f250bdc2f89dab0b56c0af920dc88f5b396631b5fe5f05ba7d1");
P159OR36P3V7RequireSha("search/d972_row36_pent_bridge_common_p3_v7.py",
  "bcfafa18e646d9ac2ef4b5b3d8693a1547da761a34335f6f0c2643938baf270c");
P159OR36P3V7RequireSha("search/d972_row36_pent_bridge_p3_producer_v7.py",
  "b1fba6374d37608a0e1faef4ad7ed6087c25b84c2bde33a6903cb37926111acc");
P159OR36P3V7RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_generator_v7.py",
  "6ab35d7a2fd4d9c3b1a7a5ed4dc5c0597ff199b1cea1faa6fd3b5a652834fe36");
P159OR36P3V7RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_v7.g",
  "de654fc73fb3d69f7736c97b48b04619122bdca04c015817ff07c27a321f6768");

P159OR36P3V7ResultPath:=
  "ci/out/d972_row36_pent_bridge_p3_transition_results_v7_20260824.json";;
P159OR36P3V7RepoPreregPath:=
  "search/certs/d972_row36_pent_bridge_p3_prereg_v7_20260824.json";;
P159OR36P3V7ArtifactPreregPath:=
  "ci/out/d972_row36_pent_bridge_p3_prereg_v7_20260824.json";;
P159OR36P3V7PythonLogPath:=
  "ci/out/d972_row36_pent_bridge_p3_python_prepare_v7.log";;

if StringFile(P159OR36P3V7ResultPath)<>fail or
   StringFile(P159OR36P3V7RepoPreregPath)<>fail or
   StringFile(P159OR36P3V7ArtifactPreregPath)<>fail or
   StringFile(P159OR36P3V7PythonLogPath)<>fail then
  Error("PENT159O_ROW36_P3_V7: pre-existing versioned output");
fi;

Print("PENT159O_ROW36_P3_V7_WORKER_START outcome_free=true states=2187 serialization=explicit_base3_lex quotient_rerun=false\n");
Read("search/d972_row36_pent_bridge_p3_transition_worker_v7.g");
P159OR36P3V7Result:=StringFile(P159OR36P3V7ResultPath);;
if P159OR36P3V7Result=fail then
  Error("PENT159O_ROW36_P3_V7: transition result absent");
fi;
Print("PENT159O_ROW36_P3_V7_TRANSITION_RESULT_PRESENT path=",
  P159OR36P3V7ResultPath," bytes=",Length(P159OR36P3V7Result),
  " sha256=",HexSHA256(P159OR36P3V7Result),"\n");

Print("PENT159O_ROW36_P3_V7_PYTHON_PREPARE_START raw_rows=34992 predicates=false\n");
Exec(Concatenation(
  "python3 search/d972_row36_pent_bridge_p3_producer_v7.py prepare > ",
  P159OR36P3V7PythonLogPath," 2>&1"));
P159OR36P3V7PythonLog:=StringFile(P159OR36P3V7PythonLogPath);;
if P159OR36P3V7PythonLog=fail then
  Error("PENT159O_ROW36_P3_V7: Python prepare log absent");
fi;
Print("PENT159O_ROW36_P3_V7_PYTHON_LOG_BEGIN\n");
Print(P159OR36P3V7PythonLog);
Print("PENT159O_ROW36_P3_V7_PYTHON_LOG_END\n");
for P159OR36P3V7Forbidden in
  ["Traceback","SyntaxError","MemoryError","Killed",
   "PENT159O_ROW36_P3_V1_STATE_STOP"] do
  if PositionSublist(P159OR36P3V7PythonLog,P159OR36P3V7Forbidden)<>fail then
    Error("PENT159O_ROW36_P3_V7: forbidden Python diagnostic ",
      P159OR36P3V7Forbidden);
  fi;
od;
if PositionSublist(P159OR36P3V7PythonLog,
     "PENT159O_ROW36_P3_V1_PREREG_WRITTEN")=fail or
   PositionSublist(P159OR36P3V7PythonLog,
     "PENT159O_ROW36_P3_V1_PREPARE_PASS")=fail then
  Error("PENT159O_ROW36_P3_V7: Python prepare terminal markers absent");
fi;

P159OR36P3V7Prereg:=StringFile(P159OR36P3V7RepoPreregPath);;
if P159OR36P3V7Prereg=fail then
  Error("PENT159O_ROW36_P3_V7: repository preregistration absent");
fi;
for P159OR36P3V7Required in
  ["\"schema\":\"d972-row36-pent-bridge-p3-prereg/v7\"",
   "\"raw_count\":34992",
   "\"expected_count\":34992",
   "\"canonical_section_derivation_serialized\":true",
   "\"predicate_outcomes_evaluated\":false",
   "\"all_three_serializations_identical\":true",
   "\"all_34992_rows_reference_the_frozen_section_word_for_their_kernel_coordinate\":true",
   "\"terminal_token\":\"PENT159O_ROW36_P3_PREREG_V7_FROZEN\""] do
  if PositionSublist(P159OR36P3V7Prereg,P159OR36P3V7Required)=fail then
    Error("PENT159O_ROW36_P3_V7: required preregistration token absent ",
      P159OR36P3V7Required);
  fi;
od;

P159OR36P3V7Out:=OutputTextFile(P159OR36P3V7ArtifactPreregPath,false);;
if P159OR36P3V7Out=fail then
  Error("PENT159O_ROW36_P3_V7: cannot open artifact preregistration");
fi;
SetPrintFormattingStatus(P159OR36P3V7Out,false);
PrintTo(P159OR36P3V7Out,P159OR36P3V7Prereg);
CloseStream(P159OR36P3V7Out);
P159OR36P3V7ArtifactPrereg:=StringFile(P159OR36P3V7ArtifactPreregPath);;
if P159OR36P3V7ArtifactPrereg=fail or
   P159OR36P3V7ArtifactPrereg<>P159OR36P3V7Prereg then
  Error("PENT159O_ROW36_P3_V7: artifact preregistration copy drift");
fi;

Print("PENT159O_ROW36_P3_V7_PREREG_WRITTEN path=",
  P159OR36P3V7ArtifactPreregPath," bytes=",Length(P159OR36P3V7ArtifactPrereg),
  " sha256=",HexSHA256(P159OR36P3V7ArtifactPrereg),"\n");
Print("PENT159O_ROW36_P3_V7_FINAL OUTCOME_FREE_PREREGISTRATION_FROZEN__PREDICATE_EXECUTION_NOT_RUN\n");
QUIT_GAP(0);
