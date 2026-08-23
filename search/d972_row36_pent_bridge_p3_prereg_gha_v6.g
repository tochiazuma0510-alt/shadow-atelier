#############################################################################
## P3 fixed-row36 outcome-free transition/preregistration wrapper v6.
#############################################################################

P159OR36P3V6RequireSha:=function(path,expected)
  local raw,actual;
  raw:=StringFile(path);
  if raw=fail then
    Error("PENT159O_ROW36_P3_V6: missing immutable input ",path);
  fi;
  actual:=HexSHA256(raw);
  if actual<>expected then
    Error("PENT159O_ROW36_P3_V6: immutable input hash mismatch ",path,
      " expected=",expected," actual=",actual);
  fi;
  Print("PENT159O_ROW36_P3_V6_PIN_PASS path=",path," bytes=",Length(raw),
    " sha256=",actual,"\n");
end;

P159OR36P3V6RequireSha("search/d972_row36_pent_bridge_common_v1.py",
  "d3e27775b59baa150c255c15feb2ab5809bdc299265278772f0428d2f1de0a79");
P159OR36P3V6RequireSha("search/d972_row36_pent_bridge_common_v2.py",
  "46ab60bf06e1bec03725a69349914e4bd9e786c41ce0946b0387f74493a55ecc");
P159OR36P3V6RequireSha("search/d972_row36_pent_bridge_common_v3.py",
  "95ff60fe351aa0020aa5353d805cd8588c7d16cbfc45acdca862097d67cafcb5");
P159OR36P3V6RequireSha("search/d972_row36_pent_bridge_common_p3_v6.py",
  "f6ac99a0d55394d675cab43690631b528a8e95270b7abfe432a94b321c411ab1");
P159OR36P3V6RequireSha("search/d972_row36_pent_bridge_p3_producer_v6.py",
  "5d557a642e34274462750e466795650a608810e6555964736c5e92aac911e2a2");
P159OR36P3V6RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_generator_v6.py",
  "0dc5caaf529c127ffa86ac2aecf3c3fa031262c9fa6ded9d554ad78099861c5a");
P159OR36P3V6RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_v6.g",
  "0133616171025f250bdc2f89dab0b56c0af920dc88f5b396631b5fe5f05ba7d1");

P159OR36P3V6ResultPath:=
  "ci/out/d972_row36_pent_bridge_p3_transition_results_v6_20260824.json";;
P159OR36P3V6RepoPreregPath:=
  "search/certs/d972_row36_pent_bridge_p3_prereg_v6_20260824.json";;
P159OR36P3V6ArtifactPreregPath:=
  "ci/out/d972_row36_pent_bridge_p3_prereg_v6_20260824.json";;
P159OR36P3V6PythonLogPath:=
  "ci/out/d972_row36_pent_bridge_p3_python_prepare_v6.log";;

if StringFile(P159OR36P3V6ResultPath)<>fail or
   StringFile(P159OR36P3V6RepoPreregPath)<>fail or
   StringFile(P159OR36P3V6ArtifactPreregPath)<>fail or
   StringFile(P159OR36P3V6PythonLogPath)<>fail then
  Error("PENT159O_ROW36_P3_V6: pre-existing versioned output");
fi;

Print("PENT159O_ROW36_P3_V6_WORKER_START outcome_free=true states=2187 positive_generators=2 quotient_rerun=false\n");
Read("search/d972_row36_pent_bridge_p3_transition_worker_v6.g");
P159OR36P3V6Result:=StringFile(P159OR36P3V6ResultPath);;
if P159OR36P3V6Result=fail then
  Error("PENT159O_ROW36_P3_V6: transition result absent");
fi;
Print("PENT159O_ROW36_P3_V6_TRANSITION_RESULT_PRESENT path=",
  P159OR36P3V6ResultPath," bytes=",Length(P159OR36P3V6Result),
  " sha256=",HexSHA256(P159OR36P3V6Result),"\n");

Print("PENT159O_ROW36_P3_V6_PYTHON_PREPARE_START raw_rows=34992 predicates=false\n");
Exec(Concatenation(
  "python3 search/d972_row36_pent_bridge_p3_producer_v6.py prepare > ",
  P159OR36P3V6PythonLogPath," 2>&1"));
P159OR36P3V6PythonLog:=StringFile(P159OR36P3V6PythonLogPath);;
if P159OR36P3V6PythonLog=fail then
  Error("PENT159O_ROW36_P3_V6: Python prepare log absent");
fi;
Print("PENT159O_ROW36_P3_V6_PYTHON_LOG_BEGIN\n");
Print(P159OR36P3V6PythonLog);
Print("PENT159O_ROW36_P3_V6_PYTHON_LOG_END\n");
for P159OR36P3V6Forbidden in
  ["Traceback","SyntaxError","MemoryError","Killed",
   "PENT159O_ROW36_P3_V1_STATE_STOP"] do
  if PositionSublist(P159OR36P3V6PythonLog,P159OR36P3V6Forbidden)<>fail then
    Error("PENT159O_ROW36_P3_V6: forbidden Python diagnostic ",
      P159OR36P3V6Forbidden);
  fi;
od;
if PositionSublist(P159OR36P3V6PythonLog,
     "PENT159O_ROW36_P3_V1_PREREG_WRITTEN")=fail or
   PositionSublist(P159OR36P3V6PythonLog,
     "PENT159O_ROW36_P3_V1_PREPARE_PASS")=fail then
  Error("PENT159O_ROW36_P3_V6: Python prepare terminal markers absent");
fi;

P159OR36P3V6Prereg:=StringFile(P159OR36P3V6RepoPreregPath);;
if P159OR36P3V6Prereg=fail then
  Error("PENT159O_ROW36_P3_V6: repository preregistration absent");
fi;
for P159OR36P3V6Required in
  ["\"schema\":\"d972-row36-pent-bridge-p3-prereg/v6\"",
   "\"raw_count\":34992",
   "\"expected_count\":34992",
   "\"canonical_section_derivation_serialized\":true",
   "\"predicate_outcomes_evaluated\":false",
   "\"all_34992_rows_reference_the_frozen_section_word_for_their_kernel_coordinate\":true",
   "\"terminal_token\":\"PENT159O_ROW36_P3_PREREG_V6_FROZEN\""] do
  if PositionSublist(P159OR36P3V6Prereg,P159OR36P3V6Required)=fail then
    Error("PENT159O_ROW36_P3_V6: required preregistration token absent ",
      P159OR36P3V6Required);
  fi;
od;

P159OR36P3V6Out:=OutputTextFile(P159OR36P3V6ArtifactPreregPath,false);;
if P159OR36P3V6Out=fail then
  Error("PENT159O_ROW36_P3_V6: cannot open artifact preregistration");
fi;
SetPrintFormattingStatus(P159OR36P3V6Out,false);
PrintTo(P159OR36P3V6Out,P159OR36P3V6Prereg);
CloseStream(P159OR36P3V6Out);
P159OR36P3V6ArtifactPrereg:=StringFile(P159OR36P3V6ArtifactPreregPath);;
if P159OR36P3V6ArtifactPrereg=fail or
   P159OR36P3V6ArtifactPrereg<>P159OR36P3V6Prereg then
  Error("PENT159O_ROW36_P3_V6: artifact preregistration copy drift");
fi;

Print("PENT159O_ROW36_P3_V6_PREREG_WRITTEN path=",
  P159OR36P3V6ArtifactPreregPath," bytes=",Length(P159OR36P3V6ArtifactPrereg),
  " sha256=",HexSHA256(P159OR36P3V6ArtifactPrereg),"\n");
Print("PENT159O_ROW36_P3_V6_FINAL OUTCOME_FREE_PREREGISTRATION_FROZEN__PREDICATE_EXECUTION_NOT_RUN\n");
QUIT_GAP(0);
