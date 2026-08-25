#############################################################################
## GHA-only launcher for the total ordinary K2 fibre-roster producer v1.
## ASCII only.  Run through .github/workflows/gap-run.yml with out_dir=ci/out.
#############################################################################

D972K2TotalSource :=
  "search/d972_k2_total_fibre_roster_producer_v1.py";;
D972K2TotalResult :=
  "ci/out/d972_k2_total_fibre_roster_v1_20260825.json";;
D972K2TotalSelftestLog :=
  "ci/out/d972_k2_total_fibre_roster_v1_selftest.log";;
D972K2TotalSelftestOK :=
  "ci/out/d972_k2_total_fibre_roster_v1_selftest.ok";;
D972K2TotalFullLog :=
  "ci/out/d972_k2_total_fibre_roster_v1_full.log";;
D972K2TotalFullOK :=
  "ci/out/d972_k2_total_fibre_roster_v1_full.ok";;
D972K2TotalPythonFinal :=
  "D972_K2_TOTAL_FIBRE_ROSTER_PRODUCER_V1_FINAL";;
D972K2TotalSelftestFinal :=
  "D972_K2_TOTAL_FIBRE_ROSTER_SELFTEST_PASS";;

D972K2TotalRequirePin := function(path, expectedBytes, expectedSha)
  local raw, actualSha;
  raw := StringFile(path);;
  if raw = fail then
    Error("D972_K2_TOTAL_FIBRE_GHA_STOP missing pinned file path=", path);
  fi;
  actualSha := HexSHA256(raw);;
  if Length(raw) <> expectedBytes or actualSha <> expectedSha then
    Error("D972_K2_TOTAL_FIBRE_GHA_STOP pin mismatch path=", path,
      " expected_bytes=", expectedBytes, " actual_bytes=", Length(raw),
      " expected_sha256=", expectedSha, " actual_sha256=", actualSha);
  fi;
  Print("D972_K2_TOTAL_FIBRE_PIN_PASS path=", path,
    " bytes=", Length(raw), " sha256=", actualSha, "\n");
  return raw;
end;;

D972K2TotalCount := function(raw, needle)
  local i, n, m, count;
  if not IsString(raw) or not IsString(needle) or Length(needle) = 0 then
    Error("D972_K2_TOTAL_FIBRE_GHA_STOP invalid occurrence inputs");
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

D972K2TotalRequireAbsent := function(path)
  if StringFile(path) <> fail then
    Error("D972_K2_TOTAL_FIBRE_GHA_STOP pre-existing output path=", path);
  fi;
end;;

D972K2TotalRequireExactFile := function(path, expected)
  local raw;
  raw := StringFile(path);;
  if raw = fail or raw <> expected then
    Error("D972_K2_TOTAL_FIBRE_GHA_STOP exit sentinel mismatch path=", path);
  fi;
end;;

D972K2TotalRequireCleanLog := function(path, requiredMarker)
  local raw, forbidden;
  raw := StringFile(path);;
  if raw = fail then
    Error("D972_K2_TOTAL_FIBRE_GHA_STOP missing log path=", path);
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
    Error("D972_K2_TOTAL_FIBRE_GHA_STOP forbidden diagnostic path=", path);
  fi;
  if D972K2TotalCount(raw, requiredMarker) <> 1 then
    Error("D972_K2_TOTAL_FIBRE_GHA_STOP terminal cardinality path=", path,
      " marker=", requiredMarker,
      " count=", D972K2TotalCount(raw, requiredMarker));
  fi;
  return raw;
end;;

Print("D972_K2_TOTAL_FIBRE_ROSTER_GHA_V1_START venue=GHA producer_side=true\n");
if GAPInfo.Version <> "4.16.0" then
  Error("D972_K2_TOTAL_FIBRE_GHA_STOP GAP 4.16.0 required observed=",
    GAPInfo.Version);
fi;

D972K2TotalRequirePin(D972K2TotalSource, 44829,
  "cc518377347988c5ad531d0d5c0c5410d2c050a91439ccb27db6414ffae9c499");;
D972K2TotalRequirePin(
  "search/d972_rung_ordinary_idx3_producer_v2.py", 54993,
  "b8dd453f7647dacc87356b13cb5428674a21bfabe6aa5af3850ac89129eb7211");;
D972K2TotalRequirePin(
  "search/certs/nf972_sourcemap_a_tuples_v2_20260804.json", 43751,
  "cfa1f3a917e2cd9d21ceaa7f77539633ccb22e8585da8b3248609008d0391801");;
D972K2TotalRequirePin(
  "search/certs/d972_b4_word_key_artifact_v1_20260816.json", 176474,
  "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9");;
D972K2TotalRequirePin(
  "search/certs/d972_rung_ordinary_idx3_prereg_v2_20260824.json", 46928,
  "1273f6050afaaba01f8dc137042ae191cecd91dea44a1618f665c2e3048e4656");;
D972K2TotalRequirePin(
  "ci/ordinary_idx3_artifacts_32682548731/d972_rung_ordinary_idx3_producer_receipt_v2_20260824.json",
  62680,
  "48512270d265753944ff9b86d19fa5e84095ffffd8ae78beba969088c31053e9");;
D972K2TotalRequirePin(".github/workflows/gap-run.yml", 11346,
  "7e732a4edf49306e18067b1003b8495c858bfae79ade8855c49488bb7e4dd763");;

Exec("mkdir -p 'ci/out'");;
D972K2TotalRequireAbsent(D972K2TotalResult);;
D972K2TotalRequireAbsent(D972K2TotalSelftestLog);;
D972K2TotalRequireAbsent(D972K2TotalSelftestOK);;
D972K2TotalRequireAbsent(D972K2TotalFullLog);;
D972K2TotalRequireAbsent(D972K2TotalFullOK);;

Exec(Concatenation(
  "python3 -u -B '", D972K2TotalSource,
  "' --selftest > '", D972K2TotalSelftestLog,
  "' 2>&1 && printf '%s' 'D972_K2_TOTAL_FIBRE_SELFTEST_EXIT_ZERO' > '",
  D972K2TotalSelftestOK, "'"));;
D972K2TotalRequireExactFile(D972K2TotalSelftestOK,
  "D972_K2_TOTAL_FIBRE_SELFTEST_EXIT_ZERO");;
D972K2TotalSelftestRaw := D972K2TotalRequireCleanLog(
  D972K2TotalSelftestLog, D972K2TotalSelftestFinal);;
if PositionSublist(D972K2TotalSelftestRaw, "mutations=8") = fail or
   PositionSublist(D972K2TotalSelftestRaw, "small_component_cases=6") = fail then
  Error("D972_K2_TOTAL_FIBRE_GHA_STOP selftest semantic marker missing");
fi;
Print("D972_K2_TOTAL_FIBRE_ROSTER_GHA_V1_SELFTEST_PASS\n");

Exec(Concatenation(
  "python3 -u -B '", D972K2TotalSource,
  "' --execute --output '", D972K2TotalResult,
  "' > '", D972K2TotalFullLog,
  "' 2>&1 && printf '%s' 'D972_K2_TOTAL_FIBRE_FULL_EXIT_ZERO' > '",
  D972K2TotalFullOK, "'"));;
D972K2TotalRequireExactFile(D972K2TotalFullOK,
  "D972_K2_TOTAL_FIBRE_FULL_EXIT_ZERO");;
D972K2TotalFullRaw := D972K2TotalRequireCleanLog(
  D972K2TotalFullLog, D972K2TotalPythonFinal);;
D972K2TotalResultRaw := StringFile(D972K2TotalResult);;
if D972K2TotalResultRaw = fail or Length(D972K2TotalResultRaw) = 0 then
  Error("D972_K2_TOTAL_FIBRE_GHA_STOP result missing or empty");
fi;
if D972K2TotalCount(D972K2TotalResultRaw, D972K2TotalPythonFinal) <> 1 then
  Error("D972_K2_TOTAL_FIBRE_GHA_STOP result terminal cardinality");
fi;
if PositionSublist(D972K2TotalResultRaw,
     "\"schema\":\"d972-k2-total-fibre-roster-producer/v1\"") = fail or
   PositionSublist(D972K2TotalResultRaw,
     "\"status\":\"CANDIDATE_PYTHON_PRODUCER\"") = fail or
   PositionSublist(D972K2TotalResultRaw, "\"cross_checked\":false") = fail or
   PositionSublist(D972K2TotalResultRaw, "\"verified\":false") = fail or
   PositionSublist(D972K2TotalResultRaw, "\"complete\":true") = fail or
   PositionSublist(D972K2TotalResultRaw, "\"no_early_stop\":true") = fail or
   PositionSublist(D972K2TotalResultRaw,
     "\"acceptance_did_not_assume_1944_or_two_per_target\":true") = fail then
  Error("D972_K2_TOTAL_FIBRE_GHA_STOP result semantic gate");
fi;
if PositionSublist(D972K2TotalResultRaw, "STATE_STOP") <> fail or
   PositionSublist(D972K2TotalResultRaw, "Traceback") <> fail then
  Error("D972_K2_TOTAL_FIBRE_GHA_STOP result diagnostic contamination");
fi;

Print("D972_K2_TOTAL_FIBRE_RESULT_PIN path=", D972K2TotalResult,
  " bytes=", Length(D972K2TotalResultRaw),
  " sha256=", HexSHA256(D972K2TotalResultRaw), "\n");
Print("D972_K2_TOTAL_FIBRE_ROSTER_GHA_V1_FINAL result=",
  D972K2TotalResult, " python_terminal_count=1 result_terminal_count=1\n");
QUIT_GAP(0);
