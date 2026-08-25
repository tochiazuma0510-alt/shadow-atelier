#############################################################################
## GHA launcher v2 for the convention-repaired total K2 roster producer.
## ASCII only. Failure logs are copied into the outer run.log before Error().
#############################################################################

D972K2V2Source :=
  "search/d972_k2_total_fibre_roster_producer_v2.py";;
D972K2V2Result :=
  "ci/out/d972_k2_total_fibre_roster_v2_20260825.json";;
D972K2V2SelftestLog :=
  "ci/out/d972_k2_total_fibre_roster_v2_selftest.log";;
D972K2V2SelftestOK :=
  "ci/out/d972_k2_total_fibre_roster_v2_selftest.ok";;
D972K2V2FullLog :=
  "ci/out/d972_k2_total_fibre_roster_v2_full.log";;
D972K2V2FullOK :=
  "ci/out/d972_k2_total_fibre_roster_v2_full.ok";;
D972K2V2PythonFinal :=
  "D972_K2_TOTAL_FIBRE_ROSTER_PRODUCER_V2_FINAL";;
D972K2V2SelftestFinal :=
  "D972_K2_TOTAL_FIBRE_ROSTER_V2_SELFTEST_PASS";;
D972K2V2CoreSelftestFinal :=
  "D972_K2_TOTAL_FIBRE_ROSTER_CORE_V1_SELFTEST_PASS";;

D972K2V2RequirePin := function(path, expectedBytes, expectedSha)
  local raw, actualSha;
  raw := StringFile(path);;
  if raw = fail then
    Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP missing pinned file path=", path);
  fi;
  actualSha := HexSHA256(raw);;
  if Length(raw) <> expectedBytes or actualSha <> expectedSha then
    Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP pin mismatch path=", path,
      " expected_bytes=", expectedBytes, " actual_bytes=", Length(raw),
      " expected_sha256=", expectedSha, " actual_sha256=", actualSha);
  fi;
  Print("D972_K2_TOTAL_FIBRE_V2_PIN_PASS path=", path,
    " bytes=", Length(raw), " sha256=", actualSha, "\n");
  return raw;
end;;

D972K2V2Count := function(raw, needle)
  local i, n, m, count;
  if not IsString(raw) or not IsString(needle) or Length(needle) = 0 then
    Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP invalid occurrence inputs");
  fi;
  n := Length(raw);;
  m := Length(needle);;
  count := 0;;
  if n < m then
    return 0;
  fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]} = needle then
      count := count + 1;;
    fi;
  od;
  return count;
end;;

D972K2V2RequireAbsent := function(path)
  if StringFile(path) <> fail then
    Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP pre-existing output path=", path);
  fi;
end;;

D972K2V2RequireExitOrEmit := function(okPath, expected, logPath, phase)
  local okRaw, logRaw;
  okRaw := StringFile(okPath);;
  if okRaw = fail or okRaw <> expected then
    logRaw := StringFile(logPath);;
    Print("D972_K2_TOTAL_FIBRE_GHA_V2_FAILURE_LOG_BEGIN phase=", phase,
      " path=", logPath, "\n");
    if logRaw = fail then
      Print("<failure log missing>\n");
    else
      Print(logRaw);
      if Length(logRaw) = 0 or logRaw[Length(logRaw)] <> '\n' then
        Print("\n");
      fi;
    fi;
    Print("D972_K2_TOTAL_FIBRE_GHA_V2_FAILURE_LOG_END phase=", phase, "\n");
    Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP subprocess exit sentinel phase=",
      phase);
  fi;
end;;

D972K2V2RequireCleanLog := function(path, requiredMarker)
  local raw, forbidden;
  raw := StringFile(path);;
  if raw = fail then
    Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP missing log path=", path);
  fi;
  forbidden := [
    "Traceback (most recent call last)",
    "SyntaxError",
    "MemoryError",
    "STATE_STOP",
    "Killed",
    "Error,",
    "Syntax error:"
  ];;
  if ForAny(forbidden, token -> PositionSublist(raw, token) <> fail) then
    Print("D972_K2_TOTAL_FIBRE_GHA_V2_FAILURE_LOG_BEGIN phase=diagnostic path=",
      path, "\n", raw);
    if Length(raw) = 0 or raw[Length(raw)] <> '\n' then
      Print("\n");
    fi;
    Print("D972_K2_TOTAL_FIBRE_GHA_V2_FAILURE_LOG_END phase=diagnostic\n");
    Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP forbidden diagnostic path=", path);
  fi;
  if D972K2V2Count(raw, requiredMarker) <> 1 then
    Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP terminal cardinality path=", path,
      " marker=", requiredMarker,
      " count=", D972K2V2Count(raw, requiredMarker));
  fi;
  return raw;
end;;

Print("D972_K2_TOTAL_FIBRE_ROSTER_GHA_V2_START venue=GHA producer_side=true repair=roof_word_replay_only\n");
if GAPInfo.Version <> "4.16.0" then
  Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP GAP 4.16.0 required observed=",
    GAPInfo.Version);
fi;

D972K2V2RequirePin(D972K2V2Source, 9776,
  "a6af98f3f2707e4812a66568c8679b3c5fad4671e764f9c33d194743c0a41411");;
D972K2V2RequirePin(
  "search/d972_k2_total_fibre_roster_producer_v1.py", 44829,
  "cc518377347988c5ad531d0d5c0c5410d2c050a91439ccb27db6414ffae9c499");;
D972K2V2RequirePin(
  "search/d972_rung_ordinary_idx3_producer_v2.py", 54993,
  "b8dd453f7647dacc87356b13cb5428674a21bfabe6aa5af3850ac89129eb7211");;
D972K2V2RequirePin(
  "search/certs/nf972_sourcemap_a_tuples_v2_20260804.json", 43751,
  "cfa1f3a917e2cd9d21ceaa7f77539633ccb22e8585da8b3248609008d0391801");;
D972K2V2RequirePin(
  "search/certs/d972_b4_word_key_artifact_v1_20260816.json", 176474,
  "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9");;
D972K2V2RequirePin(
  "search/certs/d972_rung_ordinary_idx3_prereg_v2_20260824.json", 46928,
  "1273f6050afaaba01f8dc137042ae191cecd91dea44a1618f665c2e3048e4656");;
D972K2V2RequirePin(
  "ci/ordinary_idx3_artifacts_32682548731/d972_rung_ordinary_idx3_producer_receipt_v2_20260824.json",
  62680,
  "48512270d265753944ff9b86d19fa5e84095ffffd8ae78beba969088c31053e9");;
D972K2V2RequirePin(
  "search/certs/b3_gentle_source_census_preflight_v1_20260823.json", 887124,
  "c30077133305c07ca0e58c9eaa700d42a512a6bbbce96c9c27d161e921e1aaf2");;
D972K2V2RequirePin(
  "crosscheck/verdicts/b3_gentle_source_census_v1_20260823.json", 4931,
  "e308a71323dc429d771d7fb86f507b3c17936716505dd6ca3ee3fbfdeecf7f4e");;
D972K2V2RequirePin("certificates/K36.v1.json", 727834,
  "feac2a0202e5b78a017272a972e105ac7daf7eb5ca0b4de102b6664b098d8719");;
D972K2V2RequirePin("crosscheck/verdicts/K36.v1.verdict.json", 71093,
  "4436da2643a0577b06761cd310f0032d98fefe67bab10c16f74c534aabb1a92b");;
D972K2V2RequirePin("certificates/K9.v1.json", 173224,
  "ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e");;
D972K2V2RequirePin("crosscheck/verdicts/K9.v1.verdict.json", 20991,
  "9c299baba6cd3c49296621ecfe5efbc260d7971fa874f44465fa5e968cc065f9");;
D972K2V2RequirePin("certificates/S4.v2.json", 287984,
  "c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d");;
D972K2V2RequirePin("crosscheck/verdicts/S4.psl.verdict.json", 470,
  "8d9d98965e270c2130b56fd6240c3b7460fe906ef5523f5e90396280dd043b28");;
D972K2V2RequirePin(".github/workflows/gap-run.yml", 11346,
  "7e732a4edf49306e18067b1003b8495c858bfae79ade8855c49488bb7e4dd763");;

Exec("mkdir -p 'ci/out'");;
D972K2V2RequireAbsent(D972K2V2Result);;
D972K2V2RequireAbsent(D972K2V2SelftestLog);;
D972K2V2RequireAbsent(D972K2V2SelftestOK);;
D972K2V2RequireAbsent(D972K2V2FullLog);;
D972K2V2RequireAbsent(D972K2V2FullOK);;

Exec(Concatenation(
  "python3 -u -B '", D972K2V2Source,
  "' --selftest > '", D972K2V2SelftestLog,
  "' 2>&1 && printf '%s' 'D972_K2_TOTAL_FIBRE_V2_SELFTEST_EXIT_ZERO' > '",
  D972K2V2SelftestOK, "'"));;
D972K2V2RequireExitOrEmit(D972K2V2SelftestOK,
  "D972_K2_TOTAL_FIBRE_V2_SELFTEST_EXIT_ZERO",
  D972K2V2SelftestLog, "selftest");;
D972K2V2SelftestRaw := D972K2V2RequireCleanLog(
  D972K2V2SelftestLog, D972K2V2SelftestFinal);;
if D972K2V2Count(D972K2V2SelftestRaw, D972K2V2CoreSelftestFinal) <> 1 or
   PositionSublist(D972K2V2SelftestRaw, "v1_g9_mismatches=810") = fail or
   PositionSublist(D972K2V2SelftestRaw, "first_v1_mismatch=81") = fail or
   PositionSublist(D972K2V2SelftestRaw, "v2_roof_g9_mismatches=0") = fail or
   PositionSublist(D972K2V2SelftestRaw, "psl_mismatches=0") = fail or
   PositionSublist(D972K2V2SelftestRaw,
     "convention_mutant_rejected=true") = fail then
  Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP selftest semantic gate");
fi;
Print("D972_K2_TOTAL_FIBRE_ROSTER_GHA_V2_SELFTEST_PASS\n");

Exec(Concatenation(
  "python3 -u -B '", D972K2V2Source,
  "' --execute --output '", D972K2V2Result,
  "' > '", D972K2V2FullLog,
  "' 2>&1 && printf '%s' 'D972_K2_TOTAL_FIBRE_V2_FULL_EXIT_ZERO' > '",
  D972K2V2FullOK, "'"));;
D972K2V2RequireExitOrEmit(D972K2V2FullOK,
  "D972_K2_TOTAL_FIBRE_V2_FULL_EXIT_ZERO",
  D972K2V2FullLog, "full");;
D972K2V2FullRaw := D972K2V2RequireCleanLog(
  D972K2V2FullLog, D972K2V2PythonFinal);;
D972K2V2ResultRaw := StringFile(D972K2V2Result);;
if D972K2V2ResultRaw = fail or Length(D972K2V2ResultRaw) = 0 then
  Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP result missing or empty");
fi;
if D972K2V2Count(D972K2V2ResultRaw, D972K2V2PythonFinal) <> 1 then
  Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP result terminal cardinality");
fi;
if PositionSublist(D972K2V2ResultRaw,
     "\"schema\":\"d972-k2-total-fibre-roster-producer/v2\"") = fail or
   PositionSublist(D972K2V2ResultRaw,
     "\"status\":\"CANDIDATE_PYTHON_PRODUCER\"") = fail or
   PositionSublist(D972K2V2ResultRaw, "\"cross_checked\":false") = fail or
   PositionSublist(D972K2V2ResultRaw, "\"verified\":false") = fail or
   PositionSublist(D972K2V2ResultRaw, "\"complete\":true") = fail or
   PositionSublist(D972K2V2ResultRaw, "\"no_early_stop\":true") = fail or
   PositionSublist(D972K2V2ResultRaw,
     "\"K2_predicate_or_reduction_law_changed\":false") = fail or
   PositionSublist(D972K2V2ResultRaw,
     "\"v2_roof_word_mismatch_count_over_972\":0") = fail or
   PositionSublist(D972K2V2ResultRaw,
     "\"acceptance_did_not_assume_1944_or_two_per_target\":true") = fail then
  Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP result semantic gate");
fi;
if PositionSublist(D972K2V2ResultRaw, "STATE_STOP") <> fail or
   PositionSublist(D972K2V2ResultRaw, "Traceback") <> fail then
  Error("D972_K2_TOTAL_FIBRE_GHA_V2_STOP result diagnostic contamination");
fi;

Print("D972_K2_TOTAL_FIBRE_V2_RESULT_PIN path=", D972K2V2Result,
  " bytes=", Length(D972K2V2ResultRaw),
  " sha256=", HexSHA256(D972K2V2ResultRaw), "\n");
Print("D972_K2_TOTAL_FIBRE_ROSTER_GHA_V2_FINAL result=",
  D972K2V2Result, " python_terminal_count=1 result_terminal_count=1\n");
QUIT_GAP(0);
