#############################################################################
## P2 fixed-row36 bridge execution wrapper v6.
##
## Mathematical worker, preregistration, producer, result, receipt, and
## manifest schemas remain byte-identical v5.  V6 removes only the invalid
## raw-prefix assertion: the pinned Python producer semantically parses JSON
## and requires the exact ordered 32-word roster and every coordinate width.
#############################################################################

P159OR36P2V6RequireSha := function(path, expected)
  local raw, actual;
  raw := StringFile(path);
  if raw = fail then
    Error("PENT159O_ROW36_P2_V6: missing immutable input ", path);
  fi;
  actual := HexSHA256(raw);
  if actual <> expected then
    Error("PENT159O_ROW36_P2_V6: immutable input hash mismatch ", path,
      " expected=", expected, " actual=", actual);
  fi;
  Print("PENT159O_ROW36_P2_V6_PIN_PASS path=", path,
    " bytes=", Length(raw), " sha256=", actual, "\n");
end;

P159OR36P2V6RequireSha(
  "search/d972_row36_pent_bridge_common_v1.py",
  "d3e27775b59baa150c255c15feb2ab5809bdc299265278772f0428d2f1de0a79");
P159OR36P2V6RequireSha(
  "search/d972_row36_pent_bridge_common_v2.py",
  "46ab60bf06e1bec03725a69349914e4bd9e786c41ce0946b0387f74493a55ecc");
P159OR36P2V6RequireSha(
  "search/d972_row36_pent_bridge_common_v3.py",
  "95ff60fe351aa0020aa5353d805cd8588c7d16cbfc45acdca862097d67cafcb5");
P159OR36P2V6RequireSha(
  "search/d972_row36_pent_bridge_common_p2_v4.py",
  "774952e40e3d0dee63a3c393283d278575730ea947f275c2d6000dd5264b12f2");
P159OR36P2V6RequireSha(
  "search/d972_row36_pent_bridge_common_p2_v5.py",
  "6fd800c4ad0f8f949ff5cb53ed039d3e5454d5ac00386d51aac282b068269dd5");
P159OR36P2V6RequireSha(
  "search/d972_row36_pent_bridge_p2_producer_v5.py",
  "a021b300d46e340954579749d52e24101c5f3c0b665c01c04d257e6401bd0cd0");
P159OR36P2V6RequireSha(
  "search/d972_row36_pent_bridge_p2_worker_generator_v5.py",
  "0e11ade7b1de0a35d4adc02b26db807beeea65b15fbb176ebd9b3e0147c1ca71");
P159OR36P2V6RequireSha(
  "search/d972_row36_pent_bridge_p2_dpap_worker_v5.g",
  "7c64432d5199f9d35c785db002e9a2ec595cfda0d94674cb80f07110e375b242");
P159OR36P2V6RequireSha(
  "search/certs/d972_row36_pent_bridge_p2_prereg_v5_20260824.json",
  "bf58d269fa587c693dd3ab9872129fdc695fe141e37d5c2582b858227bf056d9");

P159OR36P2V6ResultPath :=
  "ci/out/d972_row36_pent_bridge_p2_dpap_results_v5_20260824.json";
P159OR36P2V6ReceiptPath :=
  "ci/out/d972_row36_pent_bridge_p2_receipt_v5_20260824.json";
P159OR36P2V6ManifestPath :=
  "ci/out/d972_row36_pent_bridge_p2_manifest_v5_20260824.json";
P159OR36P2V6PythonLogPath :=
  "ci/out/d972_row36_pent_bridge_p2_python_v5.log";

if StringFile(P159OR36P2V6ResultPath) <> fail or
   StringFile(P159OR36P2V6ReceiptPath) <> fail or
   StringFile(P159OR36P2V6ManifestPath) <> fail or
   StringFile(P159OR36P2V6PythonLogPath) <> fail then
  Error("PENT159O_ROW36_P2_V6: pre-existing versioned v5 semantic output");
fi;

Print("PENT159O_ROW36_P2_V6_WORKER_START worker_schema=v5 direct_same_word=true defining_coordinates=true words=32 quotient_rerun=false\n");
Read("search/d972_row36_pent_bridge_p2_dpap_worker_v5.g");
P159OR36P2V6Result := StringFile(P159OR36P2V6ResultPath);
if P159OR36P2V6Result = fail then
  Error("PENT159O_ROW36_P2_V6: GAP direct same-word result absent");
fi;
Print("PENT159O_ROW36_P2_V6_WORKER_RESULT_PRESENT path=", P159OR36P2V6ResultPath,
  " bytes=", Length(P159OR36P2V6Result),
  " sha256=", HexSHA256(P159OR36P2V6Result),
  " raw_prefix_not_interpreted=true\n");

Print("PENT159O_ROW36_P2_V6_SEMANTIC_JSON_PARSE_START parser=pinned_python_v5 rows=32 exact_word_order=true\n");
Exec(Concatenation(
  "python3 search/d972_row36_pent_bridge_p2_producer_v5.py execute ",
  "--out-dir ci/out > ", P159OR36P2V6PythonLogPath, " 2>&1"));

P159OR36P2V6PythonLog := StringFile(P159OR36P2V6PythonLogPath);
if P159OR36P2V6PythonLog = fail then
  Error("PENT159O_ROW36_P2_V6: Python execution log absent");
fi;
Print("PENT159O_ROW36_P2_V6_PYTHON_LOG_BEGIN\n");
Print(P159OR36P2V6PythonLog);
Print("PENT159O_ROW36_P2_V6_PYTHON_LOG_END\n");
for P159OR36P2V6Forbidden in
  ["Traceback", "SyntaxError", "MemoryError", "Killed",
   "PENT159O_ROW36_P2_V1_STATE_STOP"] do
  if PositionSublist(P159OR36P2V6PythonLog, P159OR36P2V6Forbidden) <> fail then
    Error("PENT159O_ROW36_P2_V6: forbidden Python diagnostic ",
      P159OR36P2V6Forbidden);
  fi;
od;
if PositionSublist(P159OR36P2V6PythonLog,
     "PENT159O_ROW36_P2_V1_FINAL PRODUCER_CANDIDATE_CHECKER_REQUIRED") = fail then
  Error("PENT159O_ROW36_P2_V6: Python final marker absent");
fi;

P159OR36P2V6Receipt := StringFile(P159OR36P2V6ReceiptPath);
P159OR36P2V6Manifest := StringFile(P159OR36P2V6ManifestPath);
if P159OR36P2V6Receipt = fail or P159OR36P2V6Manifest = fail then
  Error("PENT159O_ROW36_P2_V6: receipt or manifest absent");
fi;
for P159OR36P2V6Required in
  ["\"schema\":\"d972-row36-pent-bridge-p2-receipt/v5\"",
   "\"raw_equals_evaluated_equals_expected\":true",
   "\"onto_evaluated_for_every_materialized_row\":true",
   "\"GAP_static_Q4_worker_invoked\":true",
   "\"basis\":\"reconstructed defining collector basis\"",
   "\"word_count\":32",
   "\"terminal_token\":\"PENT159O_ROW36_P2_PRODUCER_V5_CANDIDATE__CHECKER_REQUIRED\""] do
  if PositionSublist(P159OR36P2V6Receipt, P159OR36P2V6Required) = fail then
    Error("PENT159O_ROW36_P2_V6: required receipt token absent ",
      P159OR36P2V6Required);
  fi;
od;
if PositionSublist(P159OR36P2V6Manifest,
     "\"schema\":\"d972-row36-pent-bridge-p2-manifest/v5\"") = fail then
  Error("PENT159O_ROW36_P2_V6: generated manifest schema absent");
fi;

Print("PENT159O_ROW36_P2_V6_SEMANTIC_JSON_PARSE_PASS rows=32 exact_word_order=true coordinate_width=26\n");
Print("PENT159O_ROW36_P2_V6_RECEIPT_WRITTEN path=", P159OR36P2V6ReceiptPath,
  " bytes=", Length(P159OR36P2V6Receipt),
  " sha256=", HexSHA256(P159OR36P2V6Receipt), "\n");
Print("PENT159O_ROW36_P2_V6_MANIFEST_WRITTEN path=", P159OR36P2V6ManifestPath,
  " bytes=", Length(P159OR36P2V6Manifest),
  " sha256=", HexSHA256(P159OR36P2V6Manifest), "\n");
Print("PENT159O_ROW36_P2_V6_FINAL PRODUCER_V5_CANDIDATE_CHECKER_REQUIRED\n");
QUIT_GAP(0);
