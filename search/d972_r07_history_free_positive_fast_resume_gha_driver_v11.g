#############################################################################
## Task353 R07 A0/v11 bootstrap driver.  ASCII only.
## It is intentionally blocked until exact deterministic R/V owners exist.
#############################################################################
D353Producer:="search/d972_r07_history_free_positive_fast_resume_v11.py";;
D353Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v11.py";;
D353Fixture:="search/certs/d972_r07_history_free_positive_fast_resume_selftest_v11_20260829.json";;
D353Preregi:="ci/in/d972_r07_history_free_positive_fast_resume_selftest_v11.preregistration.v1.json";;
D353Pins:=[
 [D353Producer,3803,"3fd358c9efb271d4839b4c493e93714552b0d051561d5d6a5c56d1d31089d48f"],
 [D353Checker,2830,"a368543b481d42abdaaaa9c4fb6edd62e17c48b752fe545d0d4852d411492b6d"],
 [D353Fixture,514,"2440b4e57a7dcf0572ae994bfbfc08bf539a65d5295587ed4368d12c4860bb46"],
 [D353Preregi,2179,"a47e082b15ed1b9b6ea9448404ec7f2127f85d352b13d65d8ff7b1a4ad9e3757"],
 ["ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.v2.json",2690,"67dd555f6e0f943d0161ef2f2c8124b4cc31c9167846b45b43fd2001f5fbba3f"],
 ["ci/in/d972_r07_all_seven_extension_section_census_v1.json",13649089,"715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41"],
 ["ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.json",757,"e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5"]
];;
D353ModeNames:=["SELFTEST","PRODUCTION"];;
D353ProducerSeconds:=10800;;
D353CheckerSeconds:=7200;;
D353ArtifactSeconds:=3600;;
D353TotalSeconds:=21600;;
D353SelftestTerminal:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V11_SELFTEST_PASS";;
D353CommonTerminal:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V11_COMMON_WORD";;
D353Blocker:="preregistration_exact_R_V_bytes_unresolved_before_execution";;

if not IsBoundGlobal("D972_R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V11_MODE") then
  Error("task353 mode is unbound");
fi;
if not D972_R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V11_MODE in D353ModeNames then
  Error("task353 unknown driver mode");
fi;
if D353ProducerSeconds + D353CheckerSeconds + D353ArtifactSeconds > D353TotalSeconds then
  Error("task353 deadline accounting");
fi;
Error("TASK353_BLOCKED ",D353Blocker);
