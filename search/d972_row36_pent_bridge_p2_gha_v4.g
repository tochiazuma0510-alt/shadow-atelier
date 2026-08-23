#############################################################################
## P2 fixed-row36 bridge v4: fail-closed GHA launcher.
##
## The 64-row universe and every predicate are unchanged from v3.  The static
## GAP worker evaluates only the 32 frozen signed words directly in the
## immutable exported Q4 pc presentation, avoiding the Python rank-26 token
## collector cap.  It does not construct or rerun a quotient canary.
#############################################################################

P159OR36P2V4RequireSha := function(path, expected)
  local raw, actual;
  raw := StringFile(path);
  if raw = fail then
    Error("PENT159O_ROW36_P2_V4: missing immutable input ", path);
  fi;
  actual := HexSHA256(raw);
  if actual <> expected then
    Error("PENT159O_ROW36_P2_V4: immutable input hash mismatch ", path,
      " expected=", expected, " actual=", actual);
  fi;
  Print("PENT159O_ROW36_P2_V4_PIN_PASS path=", path,
    " bytes=", Length(raw), " sha256=", actual, "\n");
end;

P159OR36P2V4RequireSha(
  "search/d972_row36_pent_bridge_common_v1.py",
  "d3e27775b59baa150c255c15feb2ab5809bdc299265278772f0428d2f1de0a79");
P159OR36P2V4RequireSha(
  "search/d972_row36_pent_bridge_common_v2.py",
  "46ab60bf06e1bec03725a69349914e4bd9e786c41ce0946b0387f74493a55ecc");
P159OR36P2V4RequireSha(
  "search/d972_row36_pent_bridge_common_v3.py",
  "95ff60fe351aa0020aa5353d805cd8588c7d16cbfc45acdca862097d67cafcb5");
P159OR36P2V4RequireSha(
  "search/d972_row36_pent_bridge_common_p2_v4.py",
  "774952e40e3d0dee63a3c393283d278575730ea947f275c2d6000dd5264b12f2");
P159OR36P2V4RequireSha(
  "search/d972_row36_pent_bridge_p2_producer_v4.py",
  "57e8201471e438e1f6b597da51a495a13dc05e454cd5ae1a7a6ff08991baa3ef");
P159OR36P2V4RequireSha(
  "search/d972_row36_pent_bridge_p2_worker_generator_v4.py",
  "1f9bf0b7ce7b6c071324e32c92ea536f43f3e690a3894f70dea10b081e97c8e7");
P159OR36P2V4RequireSha(
  "search/d972_row36_pent_bridge_p2_dpap_worker_v4.g",
  "9fc4caa01a2696704fee32503377bd001f59a34bee7d405a8c39c15efbc00aba");
P159OR36P2V4RequireSha(
  "search/certs/d972_row36_pent_bridge_p2_prereg_v4_20260824.json",
  "7c86ed1d2b467af1baa9c1b90df271c5c81f5576b5a64f880bf21f898cee5665");

P159OR36P2V4ResultPath :=
  "ci/out/d972_row36_pent_bridge_p2_dpap_results_v4_20260824.json";
P159OR36P2V4ReceiptPath :=
  "ci/out/d972_row36_pent_bridge_p2_receipt_v4_20260824.json";
P159OR36P2V4ManifestPath :=
  "ci/out/d972_row36_pent_bridge_p2_manifest_v4_20260824.json";
P159OR36P2V4PythonLogPath :=
  "ci/out/d972_row36_pent_bridge_p2_python_v4.log";

if StringFile(P159OR36P2V4ResultPath) <> fail or
   StringFile(P159OR36P2V4ReceiptPath) <> fail or
   StringFile(P159OR36P2V4ManifestPath) <> fail or
   StringFile(P159OR36P2V4PythonLogPath) <> fail then
  Error("PENT159O_ROW36_P2_V4: pre-existing versioned output");
fi;

Print("PENT159O_ROW36_P2_V4_WORKER_START direct_same_word=true words=32 quotient_rerun=false\n");
Read("search/d972_row36_pent_bridge_p2_dpap_worker_v4.g");
P159OR36P2V4Result := StringFile(P159OR36P2V4ResultPath);
if P159OR36P2V4Result = fail then
  Error("PENT159O_ROW36_P2_V4: GAP direct same-word result absent");
fi;
if PositionSublist(P159OR36P2V4Result, "[[") <> 1 then
  Error("PENT159O_ROW36_P2_V4: GAP direct same-word result schema prefix");
fi;
Print("PENT159O_ROW36_P2_V4_WORKER_RESULT_PASS path=", P159OR36P2V4ResultPath,
  " bytes=", Length(P159OR36P2V4Result),
  " sha256=", HexSHA256(P159OR36P2V4Result), "\n");

Print("PENT159O_ROW36_P2_V4_EXEC_START rows=64 direct_same_word=true quotient_rerun=false\n");
Exec(Concatenation(
  "python3 search/d972_row36_pent_bridge_p2_producer_v4.py execute ",
  "--out-dir ci/out > ", P159OR36P2V4PythonLogPath, " 2>&1"));

P159OR36P2V4PythonLog := StringFile(P159OR36P2V4PythonLogPath);
if P159OR36P2V4PythonLog = fail then
  Error("PENT159O_ROW36_P2_V4: Python execution log absent");
fi;
## Deliberately surface the complete inner diagnostic before any outer error.
Print("PENT159O_ROW36_P2_V4_PYTHON_LOG_BEGIN\n");
Print(P159OR36P2V4PythonLog);
Print("PENT159O_ROW36_P2_V4_PYTHON_LOG_END\n");
for P159OR36P2V4Forbidden in
  ["Traceback", "SyntaxError", "MemoryError", "Killed",
   "PENT159O_ROW36_P2_V1_STATE_STOP"] do
  if PositionSublist(P159OR36P2V4PythonLog, P159OR36P2V4Forbidden) <> fail then
    Error("PENT159O_ROW36_P2_V4: forbidden Python diagnostic ",
      P159OR36P2V4Forbidden);
  fi;
od;
if PositionSublist(P159OR36P2V4PythonLog,
     "PENT159O_ROW36_P2_V1_FINAL PRODUCER_CANDIDATE_CHECKER_REQUIRED") = fail then
  Error("PENT159O_ROW36_P2_V4: Python final marker absent");
fi;

P159OR36P2V4Receipt := StringFile(P159OR36P2V4ReceiptPath);
P159OR36P2V4Manifest := StringFile(P159OR36P2V4ManifestPath);
if P159OR36P2V4Receipt = fail or P159OR36P2V4Manifest = fail then
  Error("PENT159O_ROW36_P2_V4: receipt or manifest absent");
fi;
for P159OR36P2V4Required in
  ["\"schema\":\"d972-row36-pent-bridge-p2-receipt/v4\"",
   "\"raw_equals_evaluated_equals_expected\":true",
   "\"onto_evaluated_for_every_materialized_row\":true",
   "\"GAP_static_Q4_worker_invoked\":true",
   "\"word_count\":32",
   "\"terminal_token\":\"PENT159O_ROW36_P2_PRODUCER_V4_CANDIDATE__CHECKER_REQUIRED\""] do
  if PositionSublist(P159OR36P2V4Receipt, P159OR36P2V4Required) = fail then
    Error("PENT159O_ROW36_P2_V4: required receipt token absent ",
      P159OR36P2V4Required);
  fi;
od;
if PositionSublist(P159OR36P2V4Manifest,
     "\"schema\":\"d972-row36-pent-bridge-p2-manifest/v4\"") = fail then
  Error("PENT159O_ROW36_P2_V4: generated manifest schema absent");
fi;

Print("PENT159O_ROW36_P2_V4_RECEIPT_WRITTEN path=", P159OR36P2V4ReceiptPath,
  " bytes=", Length(P159OR36P2V4Receipt),
  " sha256=", HexSHA256(P159OR36P2V4Receipt), "\n");
Print("PENT159O_ROW36_P2_V4_MANIFEST_WRITTEN path=", P159OR36P2V4ManifestPath,
  " bytes=", Length(P159OR36P2V4Manifest),
  " sha256=", HexSHA256(P159OR36P2V4Manifest), "\n");
Print("PENT159O_ROW36_P2_V4_FINAL PRODUCER_CANDIDATE_CHECKER_REQUIRED\n");
QUIT_GAP(0);
