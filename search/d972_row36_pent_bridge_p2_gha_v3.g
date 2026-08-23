#############################################################################
## P2 fixed-row36 bridge v3: fail-closed GHA launcher.
##
## The mathematical producer is Python because it consumes the immutable
## exported pc tables directly.  GAP is only the existing gap-run workflow's
## authenticated launcher and terminal gate.  No optional package is needed.
#############################################################################

P159OR36P2V3RequireSha := function(path, expected)
  local raw, actual;
  raw := StringFile(path);
  if raw = fail then
    Error("PENT159O_ROW36_P2_V3: missing immutable input ", path);
  fi;
  actual := HexSHA256(raw);
  if actual <> expected then
    Error("PENT159O_ROW36_P2_V3: immutable input hash mismatch ", path,
      " expected=", expected, " actual=", actual);
  fi;
  Print("PENT159O_ROW36_P2_V3_PIN_PASS path=", path,
    " bytes=", Length(raw), " sha256=", actual, "\n");
end;

P159OR36P2V3RequireSha(
  "search/d972_row36_pent_bridge_common_v1.py",
  "d3e27775b59baa150c255c15feb2ab5809bdc299265278772f0428d2f1de0a79");
P159OR36P2V3RequireSha(
  "search/d972_row36_pent_bridge_common_v2.py",
  "46ab60bf06e1bec03725a69349914e4bd9e786c41ce0946b0387f74493a55ecc");
P159OR36P2V3RequireSha(
  "search/d972_row36_pent_bridge_common_v3.py",
  "95ff60fe351aa0020aa5353d805cd8588c7d16cbfc45acdca862097d67cafcb5");
P159OR36P2V3RequireSha(
  "search/d972_row36_pent_bridge_p2_producer_v3.py",
  "8e9eb2cbbe06a687a0f66f75b2f6efcdc136ddac75b5a6d0edd3950b29ee9098");
P159OR36P2V3RequireSha(
  "search/certs/d972_row36_pent_bridge_p2_prereg_v3_20260824.json",
  "a88fac834e6a5238b95b8d364af4fd7ec4fa343386a75577f29bdb5647ce71ea");

P159OR36P2V3ReceiptPath :=
  "ci/out/d972_row36_pent_bridge_p2_receipt_v3_20260824.json";
P159OR36P2V3ManifestPath :=
  "ci/out/d972_row36_pent_bridge_p2_manifest_v3_20260824.json";
P159OR36P2V3PythonLogPath :=
  "ci/out/d972_row36_pent_bridge_p2_python_v3.log";

if StringFile(P159OR36P2V3ReceiptPath) <> fail or
   StringFile(P159OR36P2V3ManifestPath) <> fail or
   StringFile(P159OR36P2V3PythonLogPath) <> fail then
  Error("PENT159O_ROW36_P2_V3: pre-existing versioned output");
fi;

Print("PENT159O_ROW36_P2_V3_EXEC_START direct_same_word=true quotient_rerun=false\n");
Exec(Concatenation(
  "python3 search/d972_row36_pent_bridge_p2_producer_v3.py execute ",
  "--out-dir ci/out > ", P159OR36P2V3PythonLogPath, " 2>&1"));

P159OR36P2V3PythonLog := StringFile(P159OR36P2V3PythonLogPath);
if P159OR36P2V3PythonLog = fail then
  Error("PENT159O_ROW36_P2_V3: Python execution log absent");
fi;
for P159OR36P2V3Forbidden in
  ["Traceback", "SyntaxError", "MemoryError", "Killed",
   "PENT159O_ROW36_P2_V1_STATE_STOP"] do
  if PositionSublist(P159OR36P2V3PythonLog, P159OR36P2V3Forbidden) <> fail then
    Error("PENT159O_ROW36_P2_V3: forbidden Python diagnostic ",
      P159OR36P2V3Forbidden);
  fi;
od;
if PositionSublist(P159OR36P2V3PythonLog,
     "PENT159O_ROW36_P2_V1_FINAL PRODUCER_CANDIDATE_CHECKER_REQUIRED") = fail then
  Error("PENT159O_ROW36_P2_V3: Python final marker absent");
fi;

P159OR36P2V3Receipt := StringFile(P159OR36P2V3ReceiptPath);
P159OR36P2V3Manifest := StringFile(P159OR36P2V3ManifestPath);
if P159OR36P2V3Receipt = fail or P159OR36P2V3Manifest = fail then
  Error("PENT159O_ROW36_P2_V3: receipt or manifest absent");
fi;
for P159OR36P2V3Required in
  ["\"schema\":\"d972-row36-pent-bridge-p2-receipt/v3\"",
   "\"raw_equals_evaluated_equals_expected\":true",
   "\"onto_evaluated_for_every_materialized_row\":true",
   "\"terminal_token\":\"PENT159O_ROW36_P2_PRODUCER_V3_CANDIDATE__CHECKER_REQUIRED\""] do
  if PositionSublist(P159OR36P2V3Receipt, P159OR36P2V3Required) = fail then
    Error("PENT159O_ROW36_P2_V3: required receipt token absent ",
      P159OR36P2V3Required);
  fi;
od;
if PositionSublist(P159OR36P2V3Manifest,
     "\"schema\":\"d972-row36-pent-bridge-p2-manifest/v3\"") = fail then
  Error("PENT159O_ROW36_P2_V3: generated manifest schema absent");
fi;

Print(P159OR36P2V3PythonLog);
Print("PENT159O_ROW36_P2_V3_RECEIPT_WRITTEN path=", P159OR36P2V3ReceiptPath,
  " bytes=", Length(P159OR36P2V3Receipt),
  " sha256=", HexSHA256(P159OR36P2V3Receipt), "\n");
Print("PENT159O_ROW36_P2_V3_MANIFEST_WRITTEN path=", P159OR36P2V3ManifestPath,
  " bytes=", Length(P159OR36P2V3Manifest),
  " sha256=", HexSHA256(P159OR36P2V3Manifest), "\n");
Print("PENT159O_ROW36_P2_V3_FINAL PRODUCER_CANDIDATE_CHECKER_REQUIRED\n");
QUIT_GAP(0);

