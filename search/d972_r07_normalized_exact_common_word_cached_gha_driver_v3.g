#############################################################################
## Task192 normalized exact cached column-generation driver v3.
## ASCII only; producer and helper-nonshared checker are serial.
## Launchers must evaluate the quoted MODE preamble before Read(...); a bare
## SELFTEST token is an unbound GAP identifier and fails before this file runs.
#############################################################################
D192ModeVariable:="D972_R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_MODE";;
D192CanonicalModePreamble:=function(mode)
  if not IsString(mode) or not mode in ["SELFTEST","PRODUCTION"] then
    Error("task192 driver: cannot construct MODE preamble");
  fi;
  return Concatenation(D192ModeVariable,":=\"",mode,"\";;");
end;;
D192SelftestModePreamble:=D192CanonicalModePreamble("SELFTEST");;
D192ProductionModePreamble:=D192CanonicalModePreamble("PRODUCTION");;
if D192SelftestModePreamble<>"D972_R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_MODE:=\"SELFTEST\";;" or
   D192ProductionModePreamble<>"D972_R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_MODE:=\"PRODUCTION\";;" then
  Error("task192 driver: canonical MODE preamble regression");
fi;
if not IsBound(D972_R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_MODE) then
  Error("task192 driver: MODE must be a quoted SELFTEST/PRODUCTION string; use ",
    D192SelftestModePreamble," or ",D192ProductionModePreamble);
fi;
D192Mode:=D972_R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_MODE;;
if not IsString(D192Mode) or
   (D192Mode<>"SELFTEST" and D192Mode<>"PRODUCTION") then
  Error("task192 driver: invalid MODE");
fi;
D192Producer:="search/d972_r07_normalized_exact_common_word_cached_v3.py";;
D192Checker:="crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py";;
D192Fixture:="search/certs/d972_r07_normalized_exact_common_word_cached_selftest_v3_20260827.json";;
D192Receipt:="ci/out/d972_r07_normalized_exact_common_word_cached_v3.json";;
D192Verdict:="ci/out/d972_r07_normalized_exact_common_word_cached_v3.verdict";;
D192ProducerLog:="ci/out/d972_r07_normalized_exact_common_word_cached_v3.producer.log";;
D192CheckerLog:="ci/out/d972_r07_normalized_exact_common_word_cached_v3.checker.log";;
D192Shell:="ci/out/d972_r07_normalized_exact_common_word_cached_v3.sh";;
D192OK:="ci/out/d972_r07_normalized_exact_common_word_cached_v3.ok";;
D192Sentinel:="R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_SENTINEL";;
D192Common:="R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD";;
D192Selftest:="R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_SELFTEST_PASS";;
D192ProducerTerminal:="R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_PRODUCER_TERMINAL";;
D192CheckerPass:="R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_CHECKER_PASS";;
D192Current:=[
 [D192Producer,164649,"d394056420baed19a7692eee6efd0c05ff2dc642254226d81aace482ada21199"],
 [D192Checker,134845,"438242367187ab98d7c0ccf6cee22c00a3a21d416c891c8322789c9ce9f5b705"],
 [D192Fixture,276,"c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12"]
];;
D192Proofs:=[
 ["sol/proof_r07_task179_exact_exponent_lattice_v156.md",10409,"2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d"],
 ["sol/proof_r07_all_rung_exact_charming_lattice_selector_v157.md",8367,"08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8"]
];;
D192History:=[
 ["sol/luna_task_186_r07_normalized_exact_common_word_colgen_v2.md",6093,"aaae31643bdb0e25171e7a8dfef49b4a008e3b08a175c2e1337a5c11f13a3645"],
 ["sol/luna_reply_186_r07_normalized_exact_common_word_colgen_v2.md",11868,"31325a2845e1e51f6535aae3c0a9942b11c2fb553a1bb4cb0c1eff88dab4fdeb"],
 ["sol/luna_task_190_r07_exact_colgen_speed_audit.md",3699,"36502b0151e036c0df76de3e77722c1b9a9eb9ae0242fbdb6faba887d4510d29"],
 ["sol/luna_reply_190_r07_exact_colgen_speed_audit.md",22022,"6fe8ee264e33b75012b23a71c695282958882a1b1eadcc459cfff991184dfe3f"],
 ["search/d972_r07_normalized_exact_common_word_colgen_v2.py",63053,"ec73db0a474b3b52d69e19862e8185ae22423b2406f3922b5669d9a4e85fafab"],
 ["crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py",54982,"8898798d0d6a9e0b6cd67402e74ba0dc5048b4797a0f7a9657e58d70d553c488"],
 ["search/d972_r07_normalized_exact_common_word_colgen_gha_driver_v2.g",9630,"a1c0fc034b127174e5c5795347648db0629314262b9e59689705e887371a7e4e"],
 ["search/certs/d972_r07_normalized_exact_common_word_colgen_selftest_v2_20260827.json",234,"34dd389d9a3aff50486e57137f8dafea7b14825baec13e3288ed595046940963"]
];;
D192Live:=[
 ["search/d972_r07_positive_common_word_colgen_v1.py",123870,"47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"],
 ["crosscheck/check_d972_r07_positive_common_word_colgen_v1.py",73780,"de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"],
 ["search/d972_r07_positive_common_word_colgen_gha_driver_v1.g",12872,"48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b"],
 ["search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json",407,"46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"]
];;
D192Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task192 driver: missing ",path); fi;
  return raw;
end;;
D192Pin:=function(row)
  local raw;
  if row[2]=0 then return; fi;
  raw:=D192Read(row[1]);;
  if Length(raw)<>row[2] or HexSHA256(raw)<>row[3] then
    Error("task192 driver: pin drift ",row[1]);
  fi;
end;;
D192Reject:=function(paths)
  local p;
  if Length(paths)<>Length(Set(paths)) then Error("task192 driver: duplicate output"); fi;
  for p in paths do if IsExistingFile(p) then Error("task192 driver: stale output ",p); fi; od;
end;;
for D192Row in Concatenation(D192Proofs,D192History,D192Live,D192Current) do D192Pin(D192Row);; od;
D192Reject([D192Receipt,D192Verdict,D192ProducerLog,D192CheckerLog,D192Shell,D192OK]);;
D192Stream:=OutputTextFile(D192Shell,false);;
if D192Stream=fail then Error("task192 driver: shell open"); fi;
PrintTo(D192Stream,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D192Mode="SELFTEST" then
  PrintTo(D192Stream,"echo TASK192_STAGE=PRODUCER_START\n");
  PrintTo(D192Stream,"if ! python3 -u -B ",D192Producer," --selftest --receipt ",D192Receipt,
    " > ",D192ProducerLog," 2>&1; then cat ",D192ProducerLog,"; exit 1; fi\n");
  PrintTo(D192Stream,"cat ",D192ProducerLog,"\n");
  PrintTo(D192Stream,"grep -Fxc '",D192Selftest,"' ",D192ProducerLog," | grep -qx 1\n");
  PrintTo(D192Stream,"echo TASK192_STAGE=PRODUCER_PASS\n");
  PrintTo(D192Stream,"echo TASK192_STAGE=CHECKER_START\n");
  PrintTo(D192Stream,"if ! python3 -u -B ",D192Checker," ",D192Receipt," --selftest > ",
    D192CheckerLog," 2>&1; then cat ",D192CheckerLog,"; exit 1; fi\n");
  PrintTo(D192Stream,"cat ",D192CheckerLog,"\n");
  PrintTo(D192Stream,"grep -Fxc '",D192CheckerPass,"' ",D192CheckerLog," | grep -qx 1\n");
  PrintTo(D192Stream,"echo TASK192_STAGE=CHECKER_PASS\n");
else
  PrintTo(D192Stream,"echo TASK192_STAGE=PRODUCER_START\n");
  PrintTo(D192Stream,"if ! python3 -u -B ",D192Producer," --mode PRODUCTION --output ",D192Receipt,
    " --seconds 19800 --boundary-pairs 8000000 --fibre-scans 80000000 --candidate-words 2000000",
    " --retained-columns 250000 --checkpoint-bytes 4000000000 --rss-bytes 5700000000",
    " --oracle-rounds 1 > ",D192ProducerLog," 2>&1; then cat ",D192ProducerLog,"; exit 1; fi\n");
  PrintTo(D192Stream,"cat ",D192ProducerLog,"\n");
  PrintTo(D192Stream,"grep -Ec '^",D192ProducerTerminal," (",D192Common,"|UNKNOWN_RESOURCE:(phase=(task175_reconstruction|fine_deletion|Q0_discovery|A_L_membership_scan|L_subgroup_closure|typed_singleton_equality|Q0_positive_shortlex_section):cap=(wall_seconds|rss_bytes)|phase=resume_rebuild:cap=(boundary_pairs|fibre_scans|candidate_words|retained_columns|global_roster|oracle_rounds)|phase=coarse_inverse_build:cap=(fibre_scans|wall_seconds|rss_bytes)|phase=positive_boundary_correlation:cap=(boundary_pairs|wall_seconds|rss_bytes)|phase=rank_increase:cap=(retained_columns|wall_seconds|rss_bytes)|phase=positive_correction_candidate:cap=(candidate_words|wall_seconds|rss_bytes)|phase=(weighted_eleven_occurrence_formula|weighted_support_fibre):cap=(wall_seconds|rss_bytes)|phase=weighted_global_prefix:cap=(global_roster|wall_seconds|rss_bytes)|phase=checkpoint_serialization:cap=checkpoint_bytes|phase=positive_global_fallback:cap=global_roster|phase=positive_correction_dovetail:cap=oracle_rounds):value=[0-9.]+:limit=[0-9.]+|UNKNOWN_INPUT:(module_not_uniquely_pinned|module_missing|module_pin|module_loader|missing|pin|task175:not_READY|resume:input_identity|resume:target|resume:normalized_semantics|resume:monitor_limits)(:[^[:cntrl:]]*)?)$' ",D192ProducerLog," | grep -qx 1\n");
  PrintTo(D192Stream,"echo TASK192_STAGE=PRODUCER_PASS\n");
  PrintTo(D192Stream,"echo TASK192_STAGE=CHECKER_START\n");
  PrintTo(D192Stream,"if ! python3 -u -B ",D192Checker," ",D192Receipt," > ",D192CheckerLog,
    " 2>&1; then cat ",D192CheckerLog,"; exit 1; fi\n");
  PrintTo(D192Stream,"cat ",D192CheckerLog,"\n");
  PrintTo(D192Stream,"grep -Ec '^",D192CheckerPass," terminal=",D192Common,"$' ",D192CheckerLog," | grep -qx 1 || grep -Ec '^",D192CheckerPass," terminal=(UNKNOWN_RESOURCE:(phase=(task175_reconstruction|fine_deletion|Q0_discovery|A_L_membership_scan|L_subgroup_closure|typed_singleton_equality|Q0_positive_shortlex_section):cap=(wall_seconds|rss_bytes)|phase=resume_rebuild:cap=(boundary_pairs|fibre_scans|candidate_words|retained_columns|global_roster|oracle_rounds)|phase=coarse_inverse_build:cap=(fibre_scans|wall_seconds|rss_bytes)|phase=positive_boundary_correlation:cap=(boundary_pairs|wall_seconds|rss_bytes)|phase=rank_increase:cap=(retained_columns|wall_seconds|rss_bytes)|phase=positive_correction_candidate:cap=(candidate_words|wall_seconds|rss_bytes)|phase=(weighted_eleven_occurrence_formula|weighted_support_fibre):cap=(wall_seconds|rss_bytes)|phase=weighted_global_prefix:cap=(global_roster|wall_seconds|rss_bytes)|phase=checkpoint_serialization:cap=checkpoint_bytes|phase=positive_global_fallback:cap=global_roster|phase=positive_correction_dovetail:cap=oracle_rounds):value=[0-9.]+:limit=[0-9.]+|UNKNOWN_INPUT:(module_not_uniquely_pinned|module_missing|module_pin|module_loader|missing|pin|task175:not_READY|resume:input_identity|resume:target|resume:normalized_semantics|resume:monitor_limits)(:[^[:cntrl:]]*)?)$' ",D192CheckerLog," | grep -qx 1\n");
  PrintTo(D192Stream,"producer_terminal=$(grep -E '^",D192ProducerTerminal," ' ",D192ProducerLog," | sed -E 's/^",D192ProducerTerminal," //'); test $(printf '%s\\n' \"$producer_terminal\" | wc -l) -eq 1\n");
  PrintTo(D192Stream,"checker_terminal=$(grep -E '^",D192CheckerPass," terminal=' ",D192CheckerLog," | sed -E 's/^",D192CheckerPass," terminal=//'); test $(printf '%s\\n' \"$checker_terminal\" | wc -l) -eq 1\n");
  PrintTo(D192Stream,"test \"$producer_terminal\" = \"$checker_terminal\"\n");
  PrintTo(D192Stream,"echo TASK192_STAGE=TERMINAL_EQUAL\n");
fi;
PrintTo(D192Stream,"printf '%s' '",D192Sentinel,"' > ",D192OK,"\n");
CloseStream(D192Stream);;
Exec(Concatenation("bash ",D192Shell));;
D192SentinelRead:=D192Read(D192OK);;
if D192SentinelRead<>D192Sentinel then
  Error("task192 driver: sentinel payload mismatch");
fi;
if D192Mode="SELFTEST" then
  Print("R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_GHA_DRIVER_PASS mode=SELFTEST terminal=",D192Selftest,"\n");
else
  Print("R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_GHA_DRIVER_PASS mode=PRODUCTION terminal=AUTHENTICATED_CHECKER_TERMINAL\n");
fi;
