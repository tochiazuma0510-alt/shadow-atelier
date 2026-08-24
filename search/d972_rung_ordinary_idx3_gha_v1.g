#############################################################################
## Ordinary idx-3 producer-v2 GHA launcher v1.
##
## This wrapper is inert until the parent publishes the fixed-path mode token
## and supplies its lowercase SHA-256 in the workflow preamble as
## D972_ORDINARY_IDX3_MODE_TOKEN_SHA256.  It neither creates nor names a rung.
#############################################################################

P159OOrdIdx3V1RequirePin:=function(path,expectedBytes,expectedSha)
  local raw,actual;
  raw:=StringFile(path);
  if raw=fail then
    Error("PENT159O_ORDINARY_IDX3_GHA_V1: missing immutable input ",path);
  fi;
  actual:=HexSHA256(raw);
  if Length(raw)<>expectedBytes or actual<>expectedSha then
    Error("PENT159O_ORDINARY_IDX3_GHA_V1: immutable input pin mismatch ",
      path," expected_bytes=",expectedBytes," actual_bytes=",Length(raw),
      " expected_sha256=",expectedSha," actual_sha256=",actual);
  fi;
  Print("PENT159O_ORDINARY_IDX3_GHA_V1_PIN_PASS path=",path,
    " bytes=",Length(raw)," sha256=",actual,"\n");
  return rec(path:=path,bytes:=Length(raw),sha256:=actual);
end;

## The complete producer-v2 EXPECTED map, in source order.
P159OOrdIdx3V1RequirePin(
  "ops/inbox_codex/sol_task_159o_ladder_launch.txt",2829,
  "aa234d0a4ce138aa3e8c8de24c37a601cc8169a9f75d7d04cfc7f0b6d4e16b84");
P159OOrdIdx3V1RequirePin(
  "sol/luna_task_159o_ladder_launch.md",12324,
  "08be5089fcedd8232b39feb3e7491a83b3dad001ca4c2be122491c5acc7dc85a");
P159OOrdIdx3V1RequirePin(
  "scratchpad/d972_idx3_arith_datum_independent_v1.md",96640,
  "a2fae0a0365a8f1587781c797120a25532b6d274dedc609bad11c0c22082e31a");
P159OOrdIdx3V1RequirePin(
  "papers/2401.06870-gt-shadows-gentle-version.pdf",500548,
  "4e0a29e19825810eb9db24ebda120a6805c42fee4eb51679d409c5437e0943ab");
P159OOrdIdx3V1RequirePin(
  "ci/lins_marked_artifacts_32626064970/lins_marked_export/lins_marked_strictness_export_v1_20260823.json",
  51546606,
  "9fa4fff101d641688b858550e77e3543d7461bc00d149470b81dfdce91fa8324");
P159OOrdIdx3V1RequirePin(
  "search/certs/lins_census_2000_v1_20260811.json",3395546,
  "d0832df8a4e61adff45c5c24c8eba32f5d388f55412907ed5ffdf714b2b4b958");
P159OOrdIdx3V1RequirePin(
  "search/lins_marked_strictness_export_v1.g",14064,
  "74924dd639470a48d94770578c9ae9b5e22657483461f2063632150948979ec1");
P159OOrdIdx3V1RequirePin(
  "certificates/K36.v1.json",727834,
  "feac2a0202e5b78a017272a972e105ac7daf7eb5ca0b4de102b6664b098d8719");
P159OOrdIdx3V1RequirePin(
  "crosscheck/verdicts/K36.v1.verdict.json",71093,
  "4436da2643a0577b06761cd310f0032d98fefe67bab10c16f74c534aabb1a92b");
P159OOrdIdx3V1RequirePin(
  "certificates/K9.v1.json",173224,
  "ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e");
P159OOrdIdx3V1RequirePin(
  "crosscheck/verdicts/K9.v1.verdict.json",20991,
  "9c299baba6cd3c49296621ecfe5efbc260d7971fa874f44465fa5e968cc065f9");
P159OOrdIdx3V1RequirePin(
  "certificates/S4.v2.json",287984,
  "c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d");
P159OOrdIdx3V1RequirePin(
  "crosscheck/verdicts/S4.psl.verdict.json",470,
  "8d9d98965e270c2130b56fd6240c3b7460fe906ef5523f5e90396280dd043b28");
P159OOrdIdx3V1RequirePin(
  "search/certs/b3_gentle_source_census_preflight_v1_20260823.json",887124,
  "c30077133305c07ca0e58c9eaa700d42a512a6bbbce96c9c27d161e921e1aaf2");
P159OOrdIdx3V1RequirePin(
  "crosscheck/verdicts/b3_gentle_source_census_v1_20260823.json",4931,
  "e308a71323dc429d771d7fb86f507b3c17936716505dd6ca3ee3fbfdeecf7f4e");
P159OOrdIdx3V1RequirePin(
  "search/certs/d972_b4_word_key_artifact_v1_20260816.json",176474,
  "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9");
P159OOrdIdx3V1RequirePin(
  "search/certs/d972_idx3_arithmetic_receipt_v2_20260823.json",249817,
  "1fca084f396605a8755534d19412a47f60af76406ca01a2ef99bc0c06f00e7d9");
P159OOrdIdx3V1RequirePin(
  "crosscheck/verdicts/d972_idx3_arithmetic_crosscheck_v2_20260823.json",8804,
  "6fd63e3453854a02f504695876e246f1f9fa388a0b3018db4a15c84ec35db525");

## Frozen producer, preregistration, launch manifest, and unchanged workflow.
P159OOrdIdx3V1RequirePin(
  "search/d972_rung_ordinary_idx3_producer_v2.py",54993,
  "b8dd453f7647dacc87356b13cb5428674a21bfabe6aa5af3850ac89129eb7211");
P159OOrdIdx3V1RequirePin(
  "search/certs/d972_rung_ordinary_idx3_prereg_v2_20260824.json",46928,
  "1273f6050afaaba01f8dc137042ae191cecd91dea44a1618f665c2e3048e4656");
P159OOrdIdx3V1RequirePin(
  "search/certs/d972_rung_ordinary_idx3_launch_manifest_v2_20260824.json",6175,
  "196220e7fd064967ff4b8f4b622ffec5d494d3099e73bc4b26efe8eaf88fd07b");
P159OOrdIdx3V1RequirePin(
  ".github/workflows/gap-run.yml",11346,
  "7e732a4edf49306e18067b1003b8495c858bfae79ade8855c49488bb7e4dd763");

P159OOrdIdx3V1ModeTokenPath:=
  "search/certs/d972_rung_mode_freeze_ordinary_idx3_v1_20260824.json";
if not IsBound(D972_ORDINARY_IDX3_MODE_TOKEN_SHA256) then
  Error("PENT159O_ORDINARY_IDX3_GHA_V1: MODE_TOKEN_REQUIRED parent SHA-256 preamble absent");
fi;
if not IsString(D972_ORDINARY_IDX3_MODE_TOKEN_SHA256) or
   Length(D972_ORDINARY_IDX3_MODE_TOKEN_SHA256)<>64 or
   not ForAll(D972_ORDINARY_IDX3_MODE_TOKEN_SHA256,
     c->c in "0123456789abcdef") then
  Error("PENT159O_ORDINARY_IDX3_GHA_V1: invalid parent mode-token SHA-256 preamble");
fi;
P159OOrdIdx3V1ModeToken:=StringFile(P159OOrdIdx3V1ModeTokenPath);
if P159OOrdIdx3V1ModeToken=fail then
  Error("PENT159O_ORDINARY_IDX3_GHA_V1: MODE_TOKEN_REQUIRED fixed token absent ",
    P159OOrdIdx3V1ModeTokenPath);
fi;
if HexSHA256(P159OOrdIdx3V1ModeToken)<>
   D972_ORDINARY_IDX3_MODE_TOKEN_SHA256 then
  Error("PENT159O_ORDINARY_IDX3_GHA_V1: parent mode-token pin mismatch path=",
    P159OOrdIdx3V1ModeTokenPath," expected=",
    D972_ORDINARY_IDX3_MODE_TOKEN_SHA256," actual=",
    HexSHA256(P159OOrdIdx3V1ModeToken));
fi;
Print("PENT159O_ORDINARY_IDX3_GHA_V1_MODE_TOKEN_PIN_PASS path=",
  P159OOrdIdx3V1ModeTokenPath," bytes=",Length(P159OOrdIdx3V1ModeToken),
  " sha256=",HexSHA256(P159OOrdIdx3V1ModeToken),
  " authority=parent semantic_validation=producer_before_predicate\n");

P159OOrdIdx3V1ReceiptRel:=
  "search/certs/d972_rung_ordinary_idx3_producer_receipt_v2_20260824.json";
P159OOrdIdx3V1ExecutionManifestRel:=
  "search/certs/d972_rung_ordinary_idx3_execution_manifest_v2_20260824.json";
P159OOrdIdx3V1ReceiptCopy:=
  "ci/out/d972_rung_ordinary_idx3_producer_receipt_v2_20260824.json";
P159OOrdIdx3V1ManifestCopy:=
  "ci/out/d972_rung_ordinary_idx3_execution_manifest_v2_20260824.json";
P159OOrdIdx3V1PythonLogPath:=
  "ci/out/d972_rung_ordinary_idx3_python_execute_v2_20260824.log";

for P159OOrdIdx3V1OutputPath in
  [P159OOrdIdx3V1ReceiptRel,P159OOrdIdx3V1ExecutionManifestRel,
   P159OOrdIdx3V1ReceiptCopy,P159OOrdIdx3V1ManifestCopy,
   P159OOrdIdx3V1PythonLogPath] do
  if StringFile(P159OOrdIdx3V1OutputPath)<>fail then
    Error("PENT159O_ORDINARY_IDX3_GHA_V1: pre-existing versioned output ",
      P159OOrdIdx3V1OutputPath);
  fi;
od;

Print("PENT159O_ORDINARY_IDX3_GHA_V1_EXECUTE_START producer=v2 raw_rows=48 mode_authority=parent output_version=v2\n");
Exec(Concatenation(
  "python3 -B search/d972_rung_ordinary_idx3_producer_v2.py --execute ",
  "--mode-token ",P159OOrdIdx3V1ModeTokenPath," ",
  "--mode-token-sha256 ",D972_ORDINARY_IDX3_MODE_TOKEN_SHA256," ",
  "--receipt-rel ",P159OOrdIdx3V1ReceiptRel," ",
  "--execution-manifest-rel ",P159OOrdIdx3V1ExecutionManifestRel,
  " > ",P159OOrdIdx3V1PythonLogPath," 2>&1"));

P159OOrdIdx3V1PythonLog:=StringFile(P159OOrdIdx3V1PythonLogPath);
if P159OOrdIdx3V1PythonLog=fail then
  Error("PENT159O_ORDINARY_IDX3_GHA_V1: Python execution log absent");
fi;
Print("PENT159O_ORDINARY_IDX3_GHA_V1_PYTHON_LOG_BEGIN\n");
Print(P159OOrdIdx3V1PythonLog);
Print("PENT159O_ORDINARY_IDX3_GHA_V1_PYTHON_LOG_END\n");
for P159OOrdIdx3V1Forbidden in
  ["Traceback","SyntaxError","MemoryError","Killed","STATE_STOP",
   "MODE_TOKEN_REQUIRED","PIN_MISMATCH","PREREG_INPUT_PIN_DRIFT",
   "IMMUTABLE_VERSIONED_OUTPUT_MISMATCH","No such file or directory"] do
  if PositionSublist(P159OOrdIdx3V1PythonLog,
       P159OOrdIdx3V1Forbidden)<>fail then
    Error("PENT159O_ORDINARY_IDX3_GHA_V1: forbidden Python diagnostic ",
      P159OOrdIdx3V1Forbidden);
  fi;
od;
if PositionSublist(P159OOrdIdx3V1PythonLog,
     "\"terminal_token\": \"UNKNOWN_PENDING_INDEPENDENT_CHECKER_AND_PARENT_RUNG_ADJUDICATION\"")=fail then
  Error("PENT159O_ORDINARY_IDX3_GHA_V1: Python terminal marker absent");
fi;

P159OOrdIdx3V1Receipt:=StringFile(P159OOrdIdx3V1ReceiptRel);
P159OOrdIdx3V1ExecutionManifest:=
  StringFile(P159OOrdIdx3V1ExecutionManifestRel);
if P159OOrdIdx3V1Receipt=fail or
   P159OOrdIdx3V1ExecutionManifest=fail then
  Error("PENT159O_ORDINARY_IDX3_GHA_V1: receipt or execution manifest absent");
fi;
for P159OOrdIdx3V1Required in
  ["\"schema\":\"d972-rung-ordinary-idx3-producer-receipt/v2\"",
   "\"mode\":\"ORDINARY_FAIR_SHELL_FIRST\"",
   "\"rung_name_assigned\":false",
   "\"cross_checked\":false",
   "\"CLAIM-COVER-RUNG-1\"",
   "\"terminal_token\":\"UNKNOWN_PENDING_INDEPENDENT_CHECKER_AND_PARENT_RUNG_ADJUDICATION\""] do
  if PositionSublist(P159OOrdIdx3V1Receipt,P159OOrdIdx3V1Required)=fail then
    Error("PENT159O_ORDINARY_IDX3_GHA_V1: required receipt token absent ",
      P159OOrdIdx3V1Required);
  fi;
od;
for P159OOrdIdx3V1Required in
  ["\"schema\":\"d972-rung-ordinary-idx3-execution-manifest/v2\"",
   "\"mode\":\"ORDINARY_FAIR_SHELL_FIRST\"",
   "\"rung_name_assigned\":false",
   "\"terminal_token\":\"UNKNOWN_PENDING_INDEPENDENT_CHECKER_AND_PARENT_RUNG_ADJUDICATION\""] do
  if PositionSublist(P159OOrdIdx3V1ExecutionManifest,
       P159OOrdIdx3V1Required)=fail then
    Error("PENT159O_ORDINARY_IDX3_GHA_V1: required execution-manifest token absent ",
      P159OOrdIdx3V1Required);
  fi;
od;

PrintTo(P159OOrdIdx3V1ReceiptCopy,P159OOrdIdx3V1Receipt);
PrintTo(P159OOrdIdx3V1ManifestCopy,P159OOrdIdx3V1ExecutionManifest);
if StringFile(P159OOrdIdx3V1ReceiptCopy)=fail or
   HexSHA256(StringFile(P159OOrdIdx3V1ReceiptCopy))<>
     HexSHA256(P159OOrdIdx3V1Receipt) or
   StringFile(P159OOrdIdx3V1ManifestCopy)=fail or
   HexSHA256(StringFile(P159OOrdIdx3V1ManifestCopy))<>
     HexSHA256(P159OOrdIdx3V1ExecutionManifest) then
  Error("PENT159O_ORDINARY_IDX3_GHA_V1: artifact copy mismatch");
fi;

Print("PENT159O_ORDINARY_IDX3_GHA_V1_RECEIPT_PRESENT path=",
  P159OOrdIdx3V1ReceiptRel," bytes=",Length(P159OOrdIdx3V1Receipt),
  " sha256=",HexSHA256(P159OOrdIdx3V1Receipt),"\n");
Print("PENT159O_ORDINARY_IDX3_GHA_V1_EXECUTION_MANIFEST_PRESENT path=",
  P159OOrdIdx3V1ExecutionManifestRel," bytes=",
  Length(P159OOrdIdx3V1ExecutionManifest)," sha256=",
  HexSHA256(P159OOrdIdx3V1ExecutionManifest),"\n");
Print("PENT159O_ORDINARY_IDX3_GHA_V1_FINAL PRODUCER_V2_CANDIDATE_CHECKER_REQUIRED__RUNG_NAME_UNSET\n");
QUIT_GAP(0);
