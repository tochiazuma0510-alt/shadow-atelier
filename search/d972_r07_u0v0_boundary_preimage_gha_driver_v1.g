#############################################################################
## Task187 u0/v0 boundary-preimage driver v1. ASCII only; serial execution.
#############################################################################
if not IsBound(D972_R07_U0V0_BOUNDARY_PREIMAGE_V1_MODE) then
  Error("task187 driver: MODE must be SELFTEST or PRODUCTION");
fi;
D187Mode:=D972_R07_U0V0_BOUNDARY_PREIMAGE_V1_MODE;;
if D187Mode<>"SELFTEST" and D187Mode<>"PRODUCTION" then Error("task187 driver: invalid MODE"); fi;
D187Producer:="search/d972_r07_u0v0_boundary_preimage_v1.py";;
D187Checker:="crosscheck/check_d972_r07_u0v0_boundary_preimage_v1.py";;
D187Fixture:="search/certs/d972_r07_u0v0_boundary_preimage_selftest_v1_20260827.json";;
D187Receipt:="ci/out/d972_r07_u0v0_boundary_preimage_v1.json";;
D187ProducerLog:="ci/out/d972_r07_u0v0_boundary_preimage_v1.producer.log";;
D187CheckerLog:="ci/out/d972_r07_u0v0_boundary_preimage_v1.checker.log";;
D187Shell:="ci/out/d972_r07_u0v0_boundary_preimage_v1.sh";;
D187OK:="ci/out/d972_r07_u0v0_boundary_preimage_v1.ok";;
D187Common:="R07_U0V0_BOUNDARY_PREIMAGE_V1";;
D187Current:=[
 [D187Producer,35173,"85c7aa86c2406f76e7a285b44fd01224a0357fb90b20b085b12e4621a2fdddb3"],
 [D187Checker,32537,"1ffa7b6b5f3a184b2956a36984d0cc8c58574ab43f80695bec918cef918ef566"],
 [D187Fixture,699,"de58b9ae79fbf9e12e70f9370e370345809367540682284699ed28f63fc175cd"]
];;
D187Live:=[
 ["search/d972_r07_positive_common_word_colgen_v1.py",123870,"47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"],
 ["crosscheck/check_d972_r07_positive_common_word_colgen_v1.py",73780,"de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"],
 ["search/d972_r07_positive_common_word_colgen_gha_driver_v1.g",12872,"48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b"],
 ["search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json",407,"46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"],
 ["sol/proof_r07_task179_exact_exponent_lattice_v156.md",10409,"2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d"],
 ["sol/proof_r07_all_rung_exact_charming_lattice_selector_v157.md",8367,"08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8"]
];;
D187Read:=function(path)
  local raw;
  raw:=StringFile(path); if raw=fail or Length(raw)=0 then Error("task187 driver: missing ",path); fi;
  return raw;
end;;
D187Pin:=function(row)
  local raw;
  raw:=D187Read(row[1]);
  if row[2]>0 and (Length(raw)<>row[2] or HexSHA256(raw)<>row[3]) then Error("task187 driver: pin drift ",row[1]); fi;
end;;
D187Reject:=function(paths)
  local p;
  if Length(paths)<>Length(Set(paths)) then Error("task187 driver: duplicate output"); fi;
  for p in paths do if IsExistingFile(p) then Error("task187 driver: stale output ",p); fi; od;
end;;
for D187Row in D187Live do D187Pin(D187Row); od;;
for D187Row in D187Current do D187Pin(D187Row); od;;
D187Reject([D187Receipt,D187ProducerLog,D187CheckerLog,D187Shell,D187OK]);
D187Stream:=OutputTextFile(D187Shell,false);;
if D187Stream=fail then Error("task187 driver: shell open"); fi;
PrintTo(D187Stream,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D187Mode="SELFTEST" then
  PrintTo(D187Stream,"python3 -u -B ",D187Producer," --selftest --receipt ",D187Receipt," 2>&1 | tee ",D187ProducerLog,"\n");
  PrintTo(D187Stream,"test ${PIPESTATUS[0]} -eq 0\n");
  PrintTo(D187Stream,"grep -Fxc 'R07_U0V0_BOUNDARY_PREIMAGE_V1_PRODUCER_SELFTEST_PASS' ",D187ProducerLog," >/dev/null\n");
  PrintTo(D187Stream,"python3 -u -B ",D187Checker," ",D187Receipt," --selftest 2>&1 | tee ",D187CheckerLog,"\n");
  PrintTo(D187Stream,"test ${PIPESTATUS[0]} -eq 0\n");
  PrintTo(D187Stream,"grep -Fxc 'R07_U0V0_BOUNDARY_PREIMAGE_V1_CHECKER_PASS terminal=R07_U0V0_BOUNDARY_PREIMAGE_V1_SELFTEST_PASS' ",D187CheckerLog," >/dev/null\n");
else
  PrintTo(D187Stream,"python3 -u -B ",D187Producer," --mode PRODUCTION --output ",D187Receipt,
    " --seconds 19800 --boundary-pairs 8000000 --retained-columns 250000 --rss-bytes 5700000000 2>&1 | tee ",D187ProducerLog,"\n");
  PrintTo(D187Stream,"test ${PIPESTATUS[0]} -eq 0\n");
  PrintTo(D187Stream,"grep -Ec '^R07_U0V0_BOUNDARY_PREIMAGE_V1_PRODUCER_TERMINAL (R07_U0V0_BOUNDARY_PREIMAGE_V1|UNKNOWN_RESOURCE:(task175_reconstruction|fine_deletion|Q0_positive_shortlex_section|Q0_discovery|A_L_membership_scan|L_subgroup_closure|typed_singleton_equality|runtime_reconstruction):(wall_seconds|rss_bytes):[^[:cntrl:]]+|UNKNOWN_RESOURCE:complete_boundary_correlation:(wall_seconds|rss_bytes|boundary_pairs):[^[:cntrl:]]+|UNKNOWN_RESOURCE:boundary_echelon:(wall_seconds|rss_bytes|retained_columns):[^[:cntrl:]]+|UNKNOWN_INPUT:[^[:cntrl:]]+)$' ",D187ProducerLog," | grep -qx 1\n");
  PrintTo(D187Stream,"python3 -u -B ",D187Checker," ",D187Receipt," 2>&1 | tee ",D187CheckerLog,"\n");
  PrintTo(D187Stream,"test ${PIPESTATUS[0]} -eq 0\n");
  PrintTo(D187Stream,"grep -Ec '^R07_U0V0_BOUNDARY_PREIMAGE_V1_CHECKER_PASS terminal=(R07_U0V0_BOUNDARY_PREIMAGE_V1|UNKNOWN_RESOURCE:(task175_reconstruction|fine_deletion|Q0_positive_shortlex_section|Q0_discovery|A_L_membership_scan|L_subgroup_closure|typed_singleton_equality|runtime_reconstruction):(wall_seconds|rss_bytes):[^[:cntrl:]]+|UNKNOWN_RESOURCE:complete_boundary_correlation:(wall_seconds|rss_bytes|boundary_pairs):[^[:cntrl:]]+|UNKNOWN_RESOURCE:boundary_echelon:(wall_seconds|rss_bytes|retained_columns):[^[:cntrl:]]+|UNKNOWN_INPUT:[^[:cntrl:]]+)$' ",D187CheckerLog," | grep -qx 1\n");
  PrintTo(D187Stream,"producer_terminal=$(grep -E '^R07_U0V0_BOUNDARY_PREIMAGE_V1_PRODUCER_TERMINAL ' ",D187ProducerLog," | sed -E 's/^R07_U0V0_BOUNDARY_PREIMAGE_V1_PRODUCER_TERMINAL //'); test $(printf '%s\\n' \"$producer_terminal\" | wc -l) -eq 1\n");
  PrintTo(D187Stream,"checker_terminal=$(grep -E '^R07_U0V0_BOUNDARY_PREIMAGE_V1_CHECKER_PASS terminal=' ",D187CheckerLog," | sed -E 's/^R07_U0V0_BOUNDARY_PREIMAGE_V1_CHECKER_PASS terminal=//'); test $(printf '%s\\n' \"$checker_terminal\" | wc -l) -eq 1\n");
  PrintTo(D187Stream,"test \"$producer_terminal\" = \"$checker_terminal\"\n");
fi;
PrintTo(D187Stream,"touch ",D187OK,"\n"); CloseStream(D187Stream);;
Exec(Concatenation("bash ",D187Shell));
if not IsExistingFile(D187OK) then Error("task187 driver: missing completion sentinel"); fi;
if D187Mode="SELFTEST" then Print("R07_U0V0_BOUNDARY_PREIMAGE_V1_GHA_DRIVER_PASS mode=SELFTEST terminal=R07_U0V0_BOUNDARY_PREIMAGE_V1_SELFTEST_PASS\n");
else Print("R07_U0V0_BOUNDARY_PREIMAGE_V1_GHA_DRIVER_PASS mode=PRODUCTION terminal=AUTHENTICATED_CHECKER_TERMINAL\n"); fi;
