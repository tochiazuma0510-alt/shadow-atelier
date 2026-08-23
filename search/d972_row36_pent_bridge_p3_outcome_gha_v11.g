#############################################################################
## P3 fixed-row36 v11 outcome launcher over the frozen v8 preregistration.
## This is prime-local, does not rerun quotient canaries, and emits no mode/K2.
#############################################################################

P159OR36P3V11RequireSha:=function(path,expectedBytes,expectedSha)
  local raw,actual;
  raw:=StringFile(path);
  if raw=fail then
    Error("PENT159O_ROW36_P3_V11: missing immutable input ",path);
  fi;
  actual:=HexSHA256(raw);
  if Length(raw)<>expectedBytes or actual<>expectedSha then
    Error("PENT159O_ROW36_P3_V11: immutable input pin mismatch ",path,
      " expected_bytes=",expectedBytes," actual_bytes=",Length(raw),
      " expected_sha256=",expectedSha," actual_sha256=",actual);
  fi;
  Print("PENT159O_ROW36_P3_V11_PIN_PASS path=",path,
    " bytes=",Length(raw)," sha256=",actual,"\n");
  return raw;
end;

P159OR36P3V11RequireAbsent:=function(path)
  if StringFile(path)<>fail then
    Error("PENT159O_ROW36_P3_V11: pre-existing versioned output ",path);
  fi;
end;

P159OR36P3V11RequireTokens:=function(raw,label,tokens)
  local token;
  for token in tokens do
    if PositionSublist(raw,token)=fail then
      Error("PENT159O_ROW36_P3_V11: required ",label," token absent ",token);
    fi;
  od;
end;

P159OR36P3V11RejectTokens:=function(raw,label,tokens)
  local token;
  for token in tokens do
    if PositionSublist(raw,token)<>fail then
      Error("PENT159O_ROW36_P3_V11: forbidden ",label," diagnostic ",token);
    fi;
  od;
end;

P159OR36P3V11Pins:=[
  ["search/d972_row36_pent_bridge_common_v1.py",72409,
   "d3e27775b59baa150c255c15feb2ab5809bdc299265278772f0428d2f1de0a79"],
  ["search/d972_row36_pent_bridge_common_v2.py",7891,
   "46ab60bf06e1bec03725a69349914e4bd9e786c41ce0946b0387f74493a55ecc"],
  ["search/d972_row36_pent_bridge_common_v3.py",14091,
   "95ff60fe351aa0020aa5353d805cd8588c7d16cbfc45acdca862097d67cafcb5"],
  ["search/d972_row36_pent_bridge_common_v4.py",8073,
   "1d7a4673c7fdd8c5aa72a8a0f0cb78d1e39d2983a9635f6ce0fe8d978fe43bea"],
  ["search/d972_row36_pent_bridge_common_p3_v5.py",19739,
   "274db1abd26f8beeae181b9d049a6955ed33a81b7b1f6b7971ca5f7207a977e9"],
  ["search/d972_row36_pent_bridge_common_p3_v6.py",27352,
   "f6ac99a0d55394d675cab43690631b528a8e95270b7abfe432a94b321c411ab1"],
  ["search/d972_row36_pent_bridge_common_p3_v7.py",4843,
   "bcfafa18e646d9ac2ef4b5b3d8693a1547da761a34335f6f0c2643938baf270c"],
  ["search/d972_row36_pent_bridge_common_p3_v8.py",15321,
   "46194661f3d80c5d95025a3e4efad3b0ba25a28d9f77657d554060cb070e3d9e"],
  ["search/d972_row36_pent_bridge_p3_producer_v1.py",210,
   "5313639b334dd88b302f154dc3d72dfdad0476e93ed12d79e808d4a2f74fc9e8"],
  ["search/d972_row36_pent_bridge_p3_producer_v2.py",199,
   "41cf6a9d7d580083c1e451a831dd10c53243bb44869494e6e5e97a922a3bab72"],
  ["search/d972_row36_pent_bridge_p3_producer_v3.py",189,
   "52cda6616a0c88ac59b02db8d4dc70f65cd8d66c9c44d97a72ea73e5d020c903"],
  ["search/d972_row36_pent_bridge_p3_producer_v4.py",189,
   "02ff8afc3d296a79d7039c615de0db5fa1178fa7aaca93ddba3146626089feaa"],
  ["search/d972_row36_pent_bridge_p3_producer_v5.py",192,
   "cad712f2362ef484665c266b0c184caefd8851bb2d40117dcab2f45a20c45aa3"],
  ["search/d972_row36_pent_bridge_p3_producer_v6.py",198,
   "5d557a642e34274462750e466795650a608810e6555964736c5e92aac911e2a2"],
  ["search/d972_row36_pent_bridge_p3_producer_v7.py",198,
   "b1fba6374d37608a0e1faef4ad7ed6087c25b84c2bde33a6903cb37926111acc"],
  ["search/d972_row36_pent_bridge_p3_producer_v8.py",198,
   "bd1911b1b9f2a3665e81529694be8e6d421d93a713644c6355e9f360ed7b6a3b"],
  ["search/d972_row36_pent_bridge_p3_transition_worker_generator_v7.py",2878,
   "6ab35d7a2fd4d9c3b1a7a5ed4dc5c0597ff199b1cea1faa6fd3b5a652834fe36"],
  ["search/d972_row36_pent_bridge_p3_transition_worker_v7.g",51254,
   "de654fc73fb3d69f7736c97b48b04619122bdca04c015817ff07c27a321f6768"],
  ["search/d972_row36_pent_bridge_p3_transition_worker_generator_v8.py",8962,
   "2c56f5a77e5809f5976778739cab3487d30bb58074d171c74fd59ee6f9fcd27b"],
  ["search/d972_row36_pent_bridge_p3_transition_worker_v8.g",54599,
   "dc87c6872a68141f30be15ebad05d9ea12f343347fdf953e944d335294559035"],
  ["search/d972_row36_pent_bridge_common_p3_v11.py",18451,
   "a72dfa6194a3a5490abd18dd3cfb17f79de3040b7930b8bc1cd3eb9bf802609b"],
  ["search/d972_row36_pent_bridge_p3_producer_v11.py",194,
   "c2ce7326bbd8e95ca6043d3a9cbeaf1d4979357da84d19e1ca4e830483a75ad6"],
  ["search/d972_row36_pent_bridge_p3_q4_worker_generator_v11.py",11418,
   "5c0663d75d12b9aee188f502a66819cec6c2d25a320ca5e28132362208aaab3a"],
  ["search/d972_row36_pent_bridge_p3_q4_outcome_worker_v11.g",3258958,
   "3838da922ddd7117e2d134a5c773a6ed606b2e656f8ce6c70ee82e6f7b9e691c"],
  ["sol/luna_reply_159o_row36_claim_cover_audit_v1.md",10967,
   "15e597396a63a5c92beec2e8b17abc3430cac6555f645ec1cb9b805d3a32ce23"],
  ["sol/luna_reply_159o_k2_preflight.md",34658,
   "461c5e60e13c4034dcb7f2fcef87e42d8b7dfd5b1f6148a944a4d8bae7d42e26"],
  ["sol/luna_task_159o_ladder_launch.md",12324,
   "08be5089fcedd8232b39feb3e7491a83b3dad001ca4c2be122491c5acc7dc85a"],
  ["search/certs/d972_b4_word_key_artifact_v1_20260816.json",176474,
   "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"],
  ["certificates/K36.v1.json",727834,
   "feac2a0202e5b78a017272a972e105ac7daf7eb5ca0b4de102b6664b098d8719"],
  ["crosscheck/verdicts/K36.v1.verdict.json",71093,
   "4436da2643a0577b06761cd310f0032d98fefe67bab10c16f74c534aabb1a92b"],
  ["certificates/K9.v1.json",173224,
   "ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e"],
  ["crosscheck/verdicts/K9.v1.verdict.json",20991,
   "9c299baba6cd3c49296621ecfe5efbc260d7971fa874f44465fa5e968cc065f9"],
  ["certificates/S4.v2.json",287984,
   "c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d"],
  ["crosscheck/verdicts/S4.psl.verdict.json",470,
   "8d9d98965e270c2130b56fd6240c3b7460fe906ef5523f5e90396280dd043b28"],
  ["search/certs/b3_gentle_source_census_preflight_v1_20260823.json",887124,
   "c30077133305c07ca0e58c9eaa700d42a512a6bbbce96c9c27d161e921e1aaf2"],
  ["crosscheck/verdicts/b3_gentle_source_census_v1_20260823.json",4931,
   "e308a71323dc429d771d7fb86f507b3c17936716505dd6ca3ee3fbfdeecf7f4e"],
  ["ci/pent159n_p3_v5_artifacts_32661138818/d972_pent_interleave_canary_p3_receipt_v5_20260824.json",5223102,
   "8838dbfecbb8f487265801de860c91207de56e4acf5e98088e6d9cd161390530"],
  ["search/certs/d972_pent_interleave_canary_p3_manifest_v5_20260824.json",9376,
   "0cb50bd91f65611f52643de082ba9f317b75716ee12545c7e4a285cde61cfe9e"],
  ["crosscheck/verdicts/d972_pent_interleave_canary_crosscheck_p3_v2_20260824.json",22901,
   "73d4cb3f242d74f796021af922e1771c68f9256bcddedcbe2a277539f79c2781"],
  ["search/d972_row36_pent_bridge_p3_prereg_gha_v10.g",4024,
   "1d6438eaa673d50fa9d9b29740b76b91646d09c8ef11a7fe79fbc3898f5a7e91"],
  ["search/certs/d972_row36_pent_bridge_p3_prereg_execution_manifest_v10_20260824.json",8205,
   "3da685d5274d60044ee3efe84e3b54057fe1b0d9195a3ae61e6dde7934152ac5"],
  [".github/workflows/gap-run.yml",11346,
   "7e732a4edf49306e18067b1003b8495c858bfae79ade8855c49488bb7e4dd763"]
];;

for P159OR36P3V11Pin in P159OR36P3V11Pins do
  P159OR36P3V11RequireSha(P159OR36P3V11Pin[1],P159OR36P3V11Pin[2],
    P159OR36P3V11Pin[3]);
od;
Print("PENT159O_ROW36_P3_V11_COMPLETE_PIN_CLOSURE_PASS pins=42 prereg_outcome_free=true quotient_canary_rerun=false\n");

P159OR36P3V11TransitionResult:=
  "ci/out/d972_row36_pent_bridge_p3_transition_results_v8_20260824.json";;
P159OR36P3V11PreregRepo:=
  "search/certs/d972_row36_pent_bridge_p3_prereg_v8_20260824.json";;
P159OR36P3V11PreregArtifact:=
  "ci/out/d972_row36_pent_bridge_p3_prereg_v8_20260824.json";;
P159OR36P3V11PrepareLog:=
  "ci/out/d972_row36_pent_bridge_p3_python_prepare_v11.log";;
P159OR36P3V11Q4Result:=
  "ci/out/d972_row36_pent_bridge_p3_q4_results_v11_20260824.json";;
P159OR36P3V11ExecuteLog:=
  "ci/out/d972_row36_pent_bridge_p3_python_execute_v11.log";;
P159OR36P3V11Receipt:=
  "ci/out/d972_row36_pent_bridge_p3_receipt_v11_20260824.json";;
P159OR36P3V11Manifest:=
  "ci/out/d972_row36_pent_bridge_p3_manifest_v11_20260824.json";;

for P159OR36P3V11Output in
  [P159OR36P3V11TransitionResult,P159OR36P3V11PreregRepo,
   P159OR36P3V11PreregArtifact,P159OR36P3V11PrepareLog,
   P159OR36P3V11Q4Result,P159OR36P3V11ExecuteLog,
   P159OR36P3V11Receipt,P159OR36P3V11Manifest] do
  P159OR36P3V11RequireAbsent(P159OR36P3V11Output);
od;

Print("PENT159O_ROW36_P3_V11_EXEC_START prime=3 frozen_prereg=v8 canonical_words=17496 raw_rows=34992 quotient_canary_rerun=false\n");
Print("PENT159O_ROW36_P3_V11_TRANSITION_WORKER_START outcome_free=true states=2187\n");
Read("search/d972_row36_pent_bridge_p3_transition_worker_v8.g");
P159OR36P3V11TransitionRaw:=P159OR36P3V11RequireSha(
  P159OR36P3V11TransitionResult,150826,
  "3dcb6493a536c2ff000e349bd29d81166430c067293ee6d43de950859a1d6faa");;
Print("PENT159O_ROW36_P3_V11_TRANSITION_RESULT_AUTHENTICATED states=2187 signed_tables=4 orientation=paper_left_native_left\n");

Print("PENT159O_ROW36_P3_V11_PREREG_RECONSTRUCTION_START predicates=false raw_rows=34992\n");
Exec(Concatenation(
  "python3 search/d972_row36_pent_bridge_p3_producer_v8.py prepare > ",
  P159OR36P3V11PrepareLog," 2>&1"));
P159OR36P3V11PrepareRaw:=StringFile(P159OR36P3V11PrepareLog);;
if P159OR36P3V11PrepareRaw=fail then
  Error("PENT159O_ROW36_P3_V11: Python preregistration log absent");
fi;
Print("PENT159O_ROW36_P3_V11_PREPARE_LOG_BEGIN\n");
Print(P159OR36P3V11PrepareRaw);
Print("PENT159O_ROW36_P3_V11_PREPARE_LOG_END\n");
P159OR36P3V11RejectTokens(P159OR36P3V11PrepareRaw,"preregistration Python",
  ["Traceback","SyntaxError","MemoryError","Killed","STATE_STOP","PIN_MISSING"]);
P159OR36P3V11RequireTokens(P159OR36P3V11PrepareRaw,"preregistration Python",
  ["PENT159O_ROW36_P3_V1_PREPARE_GATE RESIDUAL_PATHS_PASS count=1102248",
   "PENT159O_ROW36_P3_V1_PREREG_WRITTEN",
   "PENT159O_ROW36_P3_V1_PREPARE_PASS",
   "PENT159O_ROW36_P3_V8_PREREG_WRITTEN",
   "PENT159O_ROW36_P3_V8_FINAL OUTCOME_FREE_PREREGISTRATION_FROZEN__PREDICATE_EXECUTION_NOT_RUN"]);
P159OR36P3V11PreregRaw:=P159OR36P3V11RequireSha(
  P159OR36P3V11PreregRepo,66337660,
  "2d33542ba797440ec96d16e02f9f8d7ea537048eb84d02b2ce57153d147faea4");;
P159OR36P3V11RequireTokens(P159OR36P3V11PreregRaw,"preregistration",
  ["\"schema\":\"d972-row36-pent-bridge-p3-prereg/v8\"",
   "\"status\":\"PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME\"",
   "\"canonical_word_roster_sha256\":\"25a1192cb60321035feb5f36045c4417eb0a92a07e1be7918cbabadff19a04a1\"",
   "\"raw_roster_sha256\":\"644e254535d210c2cf16778ee2d09b762358fb80ea0a82c839f5a8e1c01561ee\"",
   "\"predicate_outcomes_evaluated\":false",
   "\"terminal_token\":\"PENT159O_ROW36_P3_PREREG_V8_FROZEN\""]);
P159OR36P3V11Out:=OutputTextFile(P159OR36P3V11PreregArtifact,false);;
if P159OR36P3V11Out=fail then
  Error("PENT159O_ROW36_P3_V11: cannot open preregistration artifact copy");
fi;
SetPrintFormattingStatus(P159OR36P3V11Out,false);
PrintTo(P159OR36P3V11Out,P159OR36P3V11PreregRaw);
CloseStream(P159OR36P3V11Out);
P159OR36P3V11RequireSha(P159OR36P3V11PreregArtifact,66337660,
  "2d33542ba797440ec96d16e02f9f8d7ea537048eb84d02b2ce57153d147faea4");
Print("PENT159O_ROW36_P3_V11_PREREG_AUTHENTICATED_BEFORE_OUTCOME words=17496 raw_rows=34992\n");

Print("PENT159O_ROW36_P3_V11_Q4_WORKER_START words=17496 direct_same_signed_word=true literal_A18=true\n");
Read("search/d972_row36_pent_bridge_p3_q4_outcome_worker_v11.g");
P159OR36P3V11Q4Raw:=StringFile(P159OR36P3V11Q4Result);;
if P159OR36P3V11Q4Raw=fail or Length(P159OR36P3V11Q4Raw)<1000000 then
  Error("PENT159O_ROW36_P3_V11: Q4 direct result absent or truncated");
fi;
Print("PENT159O_ROW36_P3_V11_Q4_RESULT_PRESENT path=",P159OR36P3V11Q4Result,
  " bytes=",Length(P159OR36P3V11Q4Raw)," sha256=",
  HexSHA256(P159OR36P3V11Q4Raw),"\n");

Print("PENT159O_ROW36_P3_V11_PYTHON_OUTCOME_START words=17496 raw_rows=34992\n");
Exec(Concatenation(
  "python3 search/d972_row36_pent_bridge_p3_producer_v11.py execute --out-dir ci/out > ",
  P159OR36P3V11ExecuteLog," 2>&1"));
P159OR36P3V11ExecuteRaw:=StringFile(P159OR36P3V11ExecuteLog);;
if P159OR36P3V11ExecuteRaw=fail then
  Error("PENT159O_ROW36_P3_V11: Python outcome log absent");
fi;
Print("PENT159O_ROW36_P3_V11_EXECUTE_LOG_BEGIN\n");
Print(P159OR36P3V11ExecuteRaw);
Print("PENT159O_ROW36_P3_V11_EXECUTE_LOG_END\n");
P159OR36P3V11RejectTokens(P159OR36P3V11ExecuteRaw,"outcome Python",
  ["Traceback","SyntaxError","MemoryError","Killed","STATE_STOP","PIN_MISSING"]);
P159OR36P3V11RequireTokens(P159OR36P3V11ExecuteRaw,"outcome Python",
  ["PENT159O_ROW36_P3_V11_RECEIPT_WRITTEN",
   "PENT159O_ROW36_P3_V11_MANIFEST_WRITTEN",
   "PENT159O_ROW36_P3_V11_FINAL PRODUCER_CANDIDATE_CHECKER_REQUIRED"]);

P159OR36P3V11ReceiptRaw:=StringFile(P159OR36P3V11Receipt);;
P159OR36P3V11ManifestRaw:=StringFile(P159OR36P3V11Manifest);;
if P159OR36P3V11ReceiptRaw=fail or P159OR36P3V11ManifestRaw=fail then
  Error("PENT159O_ROW36_P3_V11: receipt or manifest absent");
fi;
P159OR36P3V11RequireTokens(P159OR36P3V11ReceiptRaw,"receipt",
  ["\"schema\":\"d972-row36-pent-bridge-p3-receipt/v11\"",
   "\"status\":\"CANDIDATE_P3_FIXED_ROW36_FULL_OUTCOME__CHECKER_REQUIRED\"",
   "\"token\":\"CLAIM-COVER-PENT-CANARY-2\"",
   "\"raw_count\":34992","\"evaluated_count\":34992",
   "\"expected_count\":34992","\"raw_equals_evaluated_equals_expected\":true",
   "\"no_omission\":true","\"no_duplicate\":true",
   "\"all_rows_reduce_to_frozen_key\":true",
   "\"checker_source_opened_or_imported\":false",
   "\"quotient_canary_rerun\":false","\"NQ_invoked\":false",
   "\"mode_token\":null","\"K2_name\":null",
   "\"all_prime_promotion\":false",
   "\"terminal_token\":\"PENT159O_ROW36_P3_PRODUCER_V11_CANDIDATE__CHECKER_REQUIRED\""]);
P159OR36P3V11RequireTokens(P159OR36P3V11ManifestRaw,"manifest",
  ["\"schema\":\"d972-row36-pent-bridge-p3-manifest/v11\"",
   "\"canonical_words\":17496","\"raw_rows\":34992",
   "\"central_m_lifts_in_order\":[0,18]",
   "\"same_word_Dpap_for_every_canonical_word\":true",
   "\"onto_evaluated_for_every_materialized_row\":true",
   "\"CLAIM_COVER_token\":\"CLAIM-COVER-PENT-CANARY-2\"",
   "\"independent_checker_required\":true",
   "\"all_prime_inference\":false",
   "\"terminal_token\":\"PENT159O_ROW36_P3_MANIFEST_V11_FROZEN\""]);

Print("PENT159O_ROW36_P3_V11_RECEIPT_PIN path=",P159OR36P3V11Receipt,
  " bytes=",Length(P159OR36P3V11ReceiptRaw)," sha256=",
  HexSHA256(P159OR36P3V11ReceiptRaw),"\n");
Print("PENT159O_ROW36_P3_V11_MANIFEST_PIN path=",P159OR36P3V11Manifest,
  " bytes=",Length(P159OR36P3V11ManifestRaw)," sha256=",
  HexSHA256(P159OR36P3V11ManifestRaw),"\n");
Print("PENT159O_ROW36_P3_V11_FINAL PRODUCER_CANDIDATE_CHECKER_REQUIRED raw=evaluated=expected=34992 no_mode_no_K2=true\n");
QUIT_GAP(0);
