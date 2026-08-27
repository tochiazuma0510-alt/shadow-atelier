#############################################################################
## Task186 normalized exact-common-word column-generation driver v2.
## ASCII only; producer and helper-nonshared checker are serial.
#############################################################################
if not IsBound(D972_R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_MODE) then
  Error("task186 driver: MODE must be SELFTEST or PRODUCTION");
fi;
D186Mode:=D972_R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_MODE;;
if D186Mode<>"SELFTEST" and D186Mode<>"PRODUCTION" then
  Error("task186 driver: invalid MODE");
fi;
D186Producer:="search/d972_r07_normalized_exact_common_word_colgen_v2.py";;
D186Checker:="crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py";;
D186Fixture:="search/certs/d972_r07_normalized_exact_common_word_colgen_selftest_v2_20260827.json";;
D186Receipt:="ci/out/d972_r07_normalized_exact_common_word_colgen_v2.json";;
D186Verdict:="ci/out/d972_r07_normalized_exact_common_word_colgen_v2.verdict";;
D186ProducerLog:="ci/out/d972_r07_normalized_exact_common_word_colgen_v2.producer.log";;
D186CheckerLog:="ci/out/d972_r07_normalized_exact_common_word_colgen_v2.checker.log";;
D186Shell:="ci/out/d972_r07_normalized_exact_common_word_colgen_v2.sh";;
D186OK:="ci/out/d972_r07_normalized_exact_common_word_colgen_v2.ok";;
D186Sentinel:="R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_SENTINEL";;
D186Common:="R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD";;
D186UnknownInput:="UNKNOWN_INPUT";;
D186ProducerBytes:=0;; D186ProducerSHA:="";;
D186CheckerBytes:=0;; D186CheckerSHA:="";;
D186FixtureBytes:=0;; D186FixtureSHA:="";;
D186Current:=[
 [D186Producer,63053,"ec73db0a474b3b52d69e19862e8185ae22423b2406f3922b5669d9a4e85fafab"],
 [D186Checker,54982,"8898798d0d6a9e0b6cd67402e74ba0dc5048b4797a0f7a9657e58d70d553c488"],
 [D186Fixture,234,"34dd389d9a3aff50486e57137f8dafea7b14825baec13e3288ed595046940963"]
];;
D186Proofs:=[
 ["sol/proof_r07_task179_exact_exponent_lattice_v156.md",10409,"2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d"],
 ["sol/proof_r07_all_rung_exact_charming_lattice_selector_v157.md",8367,"08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8"]
];;
D186Live:=[
 ["search/d972_r07_positive_common_word_colgen_v1.py",123870,"47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"],
 ["crosscheck/check_d972_r07_positive_common_word_colgen_v1.py",73780,"de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"],
 ["search/d972_r07_positive_common_word_colgen_gha_driver_v1.g",12872,"48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b"],
 ["search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json",407,"46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"]
];;
D186Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task186 driver: missing ",path); fi;
  return raw;
end;;
D186Pin:=function(row)
  local raw;
  raw:=D186Read(row[1]);;
  if Length(raw)<>row[2] or HexSHA256(raw)<>row[3] then
    Error("task186 driver: pin drift ",row[1]);
  fi;
end;;
D186Reject:=function(paths)
  local p;
  if Length(paths)<>Length(Set(paths)) then Error("task186 driver: duplicate output"); fi;
  for p in paths do if IsExistingFile(p) then Error("task186 driver: stale output ",p); fi; od;
end;;
for D186Row in Concatenation(D186Proofs,D186Live,D186Current) do D186Pin(D186Row);; od;
D186Reject([D186Receipt,D186Verdict,D186ProducerLog,D186CheckerLog,D186Shell,D186OK]);;
D186Stream:=OutputTextFile(D186Shell,false);;
if D186Stream=fail then Error("task186 driver: shell open"); fi;
PrintTo(D186Stream,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D186Mode="SELFTEST" then
  PrintTo(D186Stream,"echo TASK186_STAGE=PRODUCER_START\n");
  PrintTo(D186Stream,"if python3 -u -B ",D186Producer," --selftest --receipt ",D186Receipt," > ",D186ProducerLog," 2>&1; then producer_status=0; else producer_status=$?; fi\n");
  PrintTo(D186Stream,"cat ",D186ProducerLog,"\n");
  PrintTo(D186Stream,"test \"$producer_status\" -eq 0\n");
  PrintTo(D186Stream,"grep -Fxc 'R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_SELFTEST_PASS' ",D186ProducerLog," | grep -qx 1\n");
  PrintTo(D186Stream,"echo TASK186_STAGE=PRODUCER_PASS\n");
  PrintTo(D186Stream,"echo TASK186_STAGE=CHECKER_START\n");
  PrintTo(D186Stream,"if python3 -u -B ",D186Checker," ",D186Receipt," --selftest > ",D186CheckerLog," 2>&1; then checker_status=0; else checker_status=$?; fi\n");
  PrintTo(D186Stream,"cat ",D186CheckerLog,"\n");
  PrintTo(D186Stream,"test \"$checker_status\" -eq 0\n");
  PrintTo(D186Stream,"grep -Fxc 'R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS' ",D186CheckerLog," | grep -qx 1\n");
  PrintTo(D186Stream,"echo TASK186_STAGE=CHECKER_PASS\n");
else
  PrintTo(D186Stream,"echo TASK186_STAGE=PRODUCER_START\n");
  PrintTo(D186Stream,"if python3 -u -B ",D186Producer," --mode PRODUCTION --output ",D186Receipt,
    " --seconds 19800 --boundary-pairs 8000000 --fibre-scans 80000000 --candidate-words 2000000",
    " --retained-columns 250000 --checkpoint-bytes 4000000000 --rss-bytes 5700000000",
    " --oracle-rounds 1 > ",D186ProducerLog," 2>&1; then producer_status=0; else producer_status=$?; fi\n");
  PrintTo(D186Stream,"cat ",D186ProducerLog,"\n");
  PrintTo(D186Stream,"test \"$producer_status\" -eq 0\n");
  PrintTo(D186Stream,"grep -Ec '^R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_PRODUCER_TERMINAL (R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD|UNKNOWN_RESOURCE:(phase=(task175_reconstruction|fine_deletion|Q0_discovery|A_L_membership_scan|L_subgroup_closure|typed_singleton_equality|Q0_positive_shortlex_section):cap=(wall_seconds|rss_bytes)|phase=coarse_inverse_build:cap=(fibre_scans|wall_seconds|rss_bytes)|phase=positive_boundary_correlation:cap=(boundary_pairs|wall_seconds|rss_bytes)|phase=rank_increase:cap=(retained_columns|wall_seconds|rss_bytes)|phase=positive_correction_candidate:cap=(candidate_words|wall_seconds|rss_bytes)|phase=(weighted_eleven_occurrence_formula|weighted_support_fibre):cap=(wall_seconds|rss_bytes)|phase=weighted_global_prefix:cap=(global_roster|wall_seconds|rss_bytes)|phase=checkpoint_serialization:cap=checkpoint_bytes|phase=positive_global_fallback:cap=global_roster|phase=positive_correction_dovetail:cap=oracle_rounds):value=[0-9.]+:limit=[0-9.]+|UNKNOWN_INPUT:(module_not_uniquely_pinned|module_missing|module_pin|module_loader|missing|pin|task175:not_READY|resume:input_identity|resume:target|resume:normalized_semantics)(:[^[:cntrl:]]*)?)$' ",D186ProducerLog," | grep -qx 1\n");
  PrintTo(D186Stream,"echo TASK186_STAGE=PRODUCER_PASS\n");
  PrintTo(D186Stream,"echo TASK186_STAGE=CHECKER_START\n");
  PrintTo(D186Stream,"if python3 -u -B ",D186Checker," ",D186Receipt," > ",D186CheckerLog," 2>&1; then checker_status=0; else checker_status=$?; fi\n");
  PrintTo(D186Stream,"cat ",D186CheckerLog,"\n");
  PrintTo(D186Stream,"test \"$checker_status\" -eq 0\n");
  PrintTo(D186Stream,"grep -Ec '^R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=(R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD|UNKNOWN_RESOURCE:(phase=(task175_reconstruction|fine_deletion|Q0_discovery|A_L_membership_scan|L_subgroup_closure|typed_singleton_equality|Q0_positive_shortlex_section):cap=(wall_seconds|rss_bytes)|phase=coarse_inverse_build:cap=(fibre_scans|wall_seconds|rss_bytes)|phase=positive_boundary_correlation:cap=(boundary_pairs|wall_seconds|rss_bytes)|phase=rank_increase:cap=(retained_columns|wall_seconds|rss_bytes)|phase=positive_correction_candidate:cap=(candidate_words|wall_seconds|rss_bytes)|phase=(weighted_eleven_occurrence_formula|weighted_support_fibre):cap=(wall_seconds|rss_bytes)|phase=weighted_global_prefix:cap=(global_roster|wall_seconds|rss_bytes)|phase=checkpoint_serialization:cap=checkpoint_bytes|phase=positive_global_fallback:cap=global_roster|phase=positive_correction_dovetail:cap=oracle_rounds):value=[0-9.]+:limit=[0-9.]+|UNKNOWN_INPUT:(module_not_uniquely_pinned|module_missing|module_pin|module_loader|missing|pin|task175:not_READY|resume:input_identity|resume:target|resume:normalized_semantics)(:[^[:cntrl:]]*)?)$' ",D186CheckerLog," | grep -qx 1\n");
  PrintTo(D186Stream,"echo TASK186_STAGE=CHECKER_PASS\n");
  PrintTo(D186Stream,"producer_terminal=$(grep -E '^R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_PRODUCER_TERMINAL ' ",D186ProducerLog," | sed -E 's/^R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_PRODUCER_TERMINAL //'); test $(printf '%s\\n' \"$producer_terminal\" | wc -l) -eq 1\n");
  PrintTo(D186Stream,"checker_terminal=$(grep -E '^R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=' ",D186CheckerLog," | sed -E 's/^R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=//'); test $(printf '%s\\n' \"$checker_terminal\" | wc -l) -eq 1\n");
  PrintTo(D186Stream,"test \"$producer_terminal\" = \"$checker_terminal\"\n");
  PrintTo(D186Stream,"echo TASK186_STAGE=TERMINAL_EQUAL\n");
fi;
PrintTo(D186Stream,"printf '%s' '",D186Sentinel,"' > ",D186OK,"\n");
CloseStream(D186Stream);;
Exec(Concatenation("bash ",D186Shell));;
D186SentinelRead:=D186Read(D186OK);;
if D186SentinelRead<>D186Sentinel then
  Error("task186 driver: sentinel payload mismatch");
fi;
if D186Mode="SELFTEST" then
  Print("R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_GHA_DRIVER_PASS mode=SELFTEST terminal=R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_SELFTEST_PASS\n");
else
  Print("R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_GHA_DRIVER_PASS mode=PRODUCTION terminal=AUTHENTICATED_CHECKER_TERMINAL\n");
fi;
