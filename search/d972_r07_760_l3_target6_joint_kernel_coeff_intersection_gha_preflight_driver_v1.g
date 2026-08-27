#############################################################################
## Task-169b exact-transition GHA preflight bootstrap driver v1.
## ASCII only.  This driver creates a preflight only and refuses full mode.
## The two producers and the helper-nonshared checker are strictly serial.
#############################################################################

D972JKPB1Producer :=
  "search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py";;
D972JKPB1Checker :=
  "crosscheck/check_d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py";;
D972JKPB1TemporaryA :=
  "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_a_v1.json";;
D972JKPB1TemporaryB :=
  "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_b_v1.json";;
D972JKPB1Canonical :=
  "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_preflight_v1_20260827.json";;
D972JKPB1Verdict :=
  "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_preflight_check_v1.json";;
D972JKPB1ProducerLogA :=
  "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_producer_a_v1.log";;
D972JKPB1ProducerLogB :=
  "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_producer_b_v1.log";;
D972JKPB1CheckerLog :=
  "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_checker_v1.log";;
D972JKPB1Timing :=
  "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_timing_v1.txt";;
D972JKPB1Hashes :=
  "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_hashes_v1.txt";;
D972JKPB1StageOK :=
  "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_stage_v1.ok";;
D972JKPB1FinalOK :=
  "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_v1.ok";;
D972JKPB1DomainSeconds := 5400;;
D972JKPB1PerProcessOuterSeconds := 5700;;
D972JKPB1OuterTotalSeconds := 17900;;
D972JKPB1EnvelopeSeconds := 18000;;

## The controlling task, both final Python sources, and every immutable input
## inherited by task 169 are pinned.  The driver does not pin itself or the
## circular task-169 reply, and it does not require the missing preflight.
D972JKPB1Pins := [
  ["sol/luna_task_169b_r07_joint_kernel_gha_bootstrap.md",
   "c11712949a7f750ef5992309f1ea13ab5805d16dd223e08468690922c7d0f33c",7330],
  [D972JKPB1Producer,
   "f7d80db6197224b2096d8034e2bccc7f3f62956cc0454727156652131cfaf0c7",111249],
  [D972JKPB1Checker,
    "46623966a71d1c9f2aa0f86f6f1e5fdf74098b4ecd5a76b4c2713eb8a33bbc95",94904],
  ["sol/luna_task_169_r07_joint_kernel_coeff_intersection_v1.md",
   "6223245e9e3ec7476b5b0c55631d7bcea254c7890c5220f2b5866b9f31b22fa7",10445],
  ["sol/proof_r07_joint_kernel_coefficient_intersection_v107.md",
   "81f83d16abac3a8ffa59b6747b4b36e10796f353916ee4078c8c29c2ad2b07cd",9359],
  ["sol/proof_pb4_eleven_relator_presentation_equality_v108.md",
   "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f",6742],
  ["sol/proof_r07_full_e4_joint_orbit_selector_v109.md",
   "3224f0be545ac1ffe1d3c674087b30f55c0eb97fda0bd7702eb5f85b768255f0",11228],
  ["sol/luna_task_168_r07_jennings_legal_coefficients_v1.md",
   "4d85fd8f9ec69a618828c06498aa22922cf5372e21d10ed65280ca2468f5b7f1",7262],
  ["sol/luna_reply_168_r07_jennings_legal_coefficients_v1.md",
   "d22bed5ee8331fd5eb1d84256813699d0985df5a5bdf9a31152fdc448f847940",10692],
  ["search/d972_r07_760_l3_target6_legal_coefficients_v1.py",
   "7db4e174dec13e2f69f4011b09abcc52320699261b164b5eedb18a53fa64b962",57792],
  ["crosscheck/check_d972_r07_760_l3_target6_legal_coefficients_v1.py",
   "a54383185601e8251b7cbac87b6c57f89d3a8df8519cb93014b08a3893825e25",49633],
  ["search/d972_r07_760_l3_target6_legal_coefficients_gha_driver_v1.g",
   "bad7911b0958983aacd541bb682b0f14a2903de02cecfc01043b593b17ab1e16",19176],
  ["search/certs/d972_r07_760_l3_target6_legal_coefficients_preflight_v1_20260827.json",
   "f390f53e6fc840f41009eb31beab519e36b4989b49ac70f9c8f4df7b32776138",6833],
  ["sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md",
   "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4",11226],
  ["sol/luna_reply_157ee_b345_joint_kernel_qstar_closure.md",
   "53f20c2cb1395b8ff59ee961e1d5a14d55156a488eb6fa49edefed5dd7619eee",4118],
  ["sol/luna_task_157ef_b345_joint_kernel_checker_repair.md",
   "e626802b32e9577e35f5543b252830abdc4461b409972c9f5536ea29d8bb14ed",3235],
  ["sol/luna_reply_157ef_b345_joint_kernel_checker_repair.md",
   "71ba794479eea934c6ae06d94333f890983e53c909813dd17bab26039bce80e0",4541],
  ["search/d972_b345_joint_kernel_qstar_closure_v1.py",
   "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc",67945],
  ["search/check_d972_b345_joint_kernel_qstar_closure_v2.py",
   "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88",5942],
  ["search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g",
   "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7",3912],
  ["ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json",
   "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df",2166036],
  ["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json",
   "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72",231570]
];;

D972JKPB1Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then
    Error("task169b bootstrap: missing or empty ",label);
  fi;
  return raw;
end;;

D972JKPB1Count := function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("task169b bootstrap: count input");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972JKPB1ReplaceFirst := function(raw,old,new)
  local at,before,after;
  at:=PositionSublist(raw,old);;
  if at=fail then Error("task169b bootstrap: mutation needle"); fi;
  before:="";; after:="";;
  if at>1 then before:=raw{[1..at-1]};; fi;
  if at+Length(old)<=Length(raw) then
    after:=raw{[at+Length(old)..Length(raw)]};;
  fi;
  return Concatenation(before,new,after);
end;;

D972JKPB1Pin := function(row)
  local raw;
  if not IsList(row) or Length(row)<>3 or
     not IsString(row[1]) or not IsString(row[2]) or
     Length(row[2])<>64 or not IsInt(row[3]) or row[3]<=0 then
    Error("task169b bootstrap: malformed pin");
  fi;
  raw:=D972JKPB1Read(row[1],row[1]);;
  if Length(raw)<>row[3] or HexSHA256(raw)<>row[2] then
    Error("task169b bootstrap: pin drift ",row[1]);
  fi;
  return true;
end;;

D972JKPB1ShellQuote := function(path)
  if not IsString(path) or Length(path)=0 or
     PositionSublist(path,"\"")<>fail or
     PositionSublist(path,"\n")<>fail or
     PositionSublist(path,"\r")<>fail or
     PositionSublist(path,"$")<>fail or
     PositionSublist(path,"`")<>fail then
    Error("task169b bootstrap: unsafe shell path");
  fi;
  return Concatenation("\"",path,"\"");
end;;

D972JKPB1RejectPreexisting := function(paths)
  local path;
  if Length(Set(paths))<>Length(paths) then
    Error("task169b bootstrap: duplicate owned output");
  fi;
  for path in paths do
    if IsExistingFile(path) then
      Error("task169b bootstrap: refuse pre-existing owned output ",path);
    fi;
  od;
  return true;
end;;

D972JKPB1CleanLog := function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):", "SyntaxError",
                "RuntimeError", "ResourceStop", "Error,", " FAIL ",
                " failed"] do
    if D972JKPB1Count(raw,token)<>0 then
      Error("task169b bootstrap: forbidden log token ",label," ",token);
    fi;
  od;
  return true;
end;;

D972JKPB1NoForbiddenPositiveClaim := function(raw)
  local token;
  for token in [
    "\"full_E4_positive_class_reconstructed\":true",
    "\"true_PB4_D2_equality_used\":true",
    "\"literal_A18_replayed\":true",
    "\"two_hexagons_replayed_as_joint_system\":true",
    "\"HT1_HT5_all_edges_proved\":true",
    "\"cofinal_compatibility_proved\":true",
    "\"actual_A18_lift\":true", "\"fake\":true",
    "\"cofinal_lift\":true", "\"Ihara_witness\":true"] do
    if D972JKPB1Count(raw,token)<>0 then return false; fi;
  od;
  return true;
end;;

D972JKPB1AuditPreflight := function(raw)
  return
    D972JKPB1Count(raw,
      "\"schema\":\"d972-r07-760-l3-target6-joint-kernel-coeff-intersection/v1\"")=1 and
    D972JKPB1Count(raw,"\"mode\":\"preflight\"")=2 and
    D972JKPB1Count(raw,
      "\"preflight_state\":\"R07_760_JOINT_COEFF_INTERSECTION_V1_PREFLIGHT_READY\"")=1 and
    D972JKPB1Count(raw,
      "\"status\":\"R07_760_JOINT_COEFF_INTERSECTION_V1_PREFLIGHT_READY\"")=1 and
    D972JKPB1Count(raw,"\"mutation_tests_rejected\":19")=1 and
    D972JKPB1Count(raw,"\"all_31_context_ids\":31")=1 and
    D972JKPB1Count(raw,"\"all_46_named_aliases\":46")=1 and
    D972JKPB1Count(raw,"\"all_3_relation_layers\":3")=1 and
    D972JKPB1Count(raw,"\"all_27_transversals\":27")=1 and
    D972JKPB1Count(raw,"\"all_28_schreier_sign_rows\":28")=1 and
    D972JKPB1Count(raw,"\"all_56_exponent_entries\":56")=1 and
    D972JKPB1Count(raw,"\"relation_count\":6441")=1 and
    D972JKPB1Count(raw,"\"input_row_count\":173907")=1 and
    D972JKPB1Count(raw,"\"legacy_group_eval_canary_count\":31")=1 and
    D972JKPB1Count(raw,
      "\"legacy_group_eval_canary_global_ordinals\":[")=1 and
    D972JKPB1Count(raw,
      "\"legacy_group_eval_canary_digest_sha256\":\"")=1 and
    D972JKPB1Count(raw,
      "\"direct_full_Omega_relation_evaluation_digest_sha256\":\"")=1 and
    D972JKPB1Count(raw,"\"domain_seconds\":5400.0")=1 and
    D972JKPB1Count(raw,"\"default_local_domain_seconds\":600.0")=1 and
    D972JKPB1Count(raw,"\"maximum_GHA_domain_seconds\":5400.0")=1 and
    D972JKPB1Count(raw,
      "\"separate_from_task168_full_search_seconds\":true")=1 and
    D972JKPB1Count(raw,
      "\"not_part_of_mathematical_universe\":true")=1 and
    D972JKPB1Count(raw,"\"registered_wall_seconds_cap\":5400.0")=1 and
    D972JKPB1Count(raw,"\"full_j9_run_locally\":false")=2 and
    D972JKPB1Count(raw,"\"GHA_dispatched\":false")=2 and
    D972JKPB1Count(raw,"\"parallel_local_computation\":false")>=1 and
    D972JKPB1NoForbiddenPositiveClaim(raw);
end;;

D972JKPB1AuditVerdict := function(raw,targetsha)
  return
    D972JKPB1Count(raw,
      "\"schema\":\"d972-r07-760-l3-target6-joint-kernel-coeff-intersection-check/v1\"")=1 and
    D972JKPB1Count(raw,"\"status\":\"CROSSCHECK_PASS\"")=1 and
    D972JKPB1Count(raw,
      Concatenation("\"target_sha256\":\"",targetsha,"\""))=1 and
    D972JKPB1Count(raw,"\"mutation_tests_rejected\":23")=1 and
    D972JKPB1Count(raw,"\"word_count\":1365")=1 and
    D972JKPB1Count(raw,"\"mutation_tests_rejected\":4")=1 and
    D972JKPB1Count(raw,"\"relation_count\":6441")=1 and
    D972JKPB1Count(raw,"\"RS_row_count\":173907")=1 and
    D972JKPB1Count(raw,
      "\"exact_transition_cache_and_canaries_reproduced\":true")=1 and
    D972JKPB1Count(raw,"\"task169_domain_seconds\":5400.0")=1 and
    D972JKPB1Count(raw,
      "\"helper_shared_with_task169_producer\":false")=2 and
    D972JKPB1Count(raw,"\"imports_task169_producer\":false")=1 and
    D972JKPB1Count(raw,"\"full_j9_recomputed\":false")=1 and
    D972JKPB1NoForbiddenPositiveClaim(raw);
end;;

D972JKPB1FixtureSelftest := function()
  local sha,raw,verdict,bad,rejected;
  sha:="0000000000000000000000000000000000000000000000000000000000000000";;
  raw:=Concatenation(
    "{\"GHA_dispatched\":false,",
    "\"embedded\":{\"GHA_dispatched\":false,\"full_j9_run_locally\":false,",
    "\"mode\":\"preflight\",\"mutation_tests_rejected\":11},",
    "\"full_j9_run_locally\":false,\"mode\":\"preflight\",",
    "\"mutation_tests_rejected\":19,\"parallel_local_computation\":false,",
    "\"preflight_state\":\"R07_760_JOINT_COEFF_INTERSECTION_V1_PREFLIGHT_READY\",",
    "\"registered_joint_domain\":{\"RS_abelianization\":{\"input_row_count\":173907},",
    "\"exact_transition_evaluator\":{\"legacy_group_eval_canary_count\":31,",
    "\"legacy_group_eval_canary_digest_sha256\":\"x\",",
    "\"legacy_group_eval_canary_global_ordinals\":[]},",
    "\"relation_count\":6441,",
    "\"direct_full_Omega_relation_evaluation_digest_sha256\":\"x\",",
    "\"resource_accounting\":{\"registered_wall_seconds_cap\":5400.0}},",
    "\"schema\":\"d972-r07-760-l3-target6-joint-kernel-coeff-intersection/v1\",",
    "\"status\":\"R07_760_JOINT_COEFF_INTERSECTION_V1_PREFLIGHT_READY\",",
    "\"structural_mutation_tests_rejected\":{\"all_27_transversals\":27,",
    "\"all_28_schreier_sign_rows\":28,\"all_31_context_ids\":31,",
    "\"all_3_relation_layers\":3,\"all_46_named_aliases\":46,",
    "\"all_56_exponent_entries\":56},",
    "\"task169_domain_resource_policy\":{\"default_local_domain_seconds\":600.0,",
    "\"domain_seconds\":5400.0,\"maximum_GHA_domain_seconds\":5400.0,",
    "\"not_part_of_mathematical_universe\":true,",
    "\"separate_from_task168_full_search_seconds\":true},",
    "\"claims\":{\"actual_A18_lift\":false,\"cofinal_lift\":false,",
    "\"fake\":false,\"Ihara_witness\":false}}\n");;
  verdict:=Concatenation(
    "{\"domain_crosscheck\":{\"RS_row_count\":173907,",
    "\"exact_transition_cache_and_canaries_reproduced\":true,",
    "\"helper_shared_with_task169_producer\":false,",
    "\"relation_count\":6441},",
    "\"exact_transition_cache_fixture\":{\"mutation_tests_rejected\":4,",
    "\"word_count\":1365},\"full_j9_recomputed\":false,",
    "\"helper_shared_with_task169_producer\":false,",
    "\"imports_task169_producer\":false,\"mutation_tests_rejected\":23,",
    "\"schema\":\"d972-r07-760-l3-target6-joint-kernel-coeff-intersection-check/v1\",",
    "\"status\":\"CROSSCHECK_PASS\",\"target_sha256\":\"",sha,"\",",
    "\"task169_domain_seconds\":5400.0}\n");;
  if not D972JKPB1AuditPreflight(raw) or
     not D972JKPB1AuditVerdict(verdict,sha) then
    Error("task169b bootstrap: static fixture rejected");
  fi;
  rejected:=0;;
  bad:=D972JKPB1ReplaceFirst(raw,"\"relation_count\":6441",
                                 "\"relation_count\":6440");;
  if not D972JKPB1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  bad:=D972JKPB1ReplaceFirst(raw,"\"input_row_count\":173907",
                                 "\"input_row_count\":173906");;
  if not D972JKPB1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  bad:=D972JKPB1ReplaceFirst(raw,
    "\"legacy_group_eval_canary_count\":31",
    "\"legacy_group_eval_canary_count\":30");;
  if not D972JKPB1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  bad:=D972JKPB1ReplaceFirst(raw,"\"domain_seconds\":5400.0",
                                 "\"domain_seconds\":600.0");;
  if not D972JKPB1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  bad:=D972JKPB1ReplaceFirst(raw,"\"fake\":false","\"fake\":true");;
  if not D972JKPB1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  bad:=D972JKPB1ReplaceFirst(raw,"\"mutation_tests_rejected\":19",
                                 "\"mutation_tests_rejected\":18");;
  if not D972JKPB1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  bad:=D972JKPB1ReplaceFirst(verdict,"\"status\":\"CROSSCHECK_PASS\"",
    "\"status\":\"CROSSCHECK_FAIL\"");;
  if not D972JKPB1AuditVerdict(bad,sha) then rejected:=rejected+1;; fi;
  bad:=D972JKPB1ReplaceFirst(verdict,
    Concatenation("\"target_sha256\":\"",sha,"\""),
    Concatenation("\"target_sha256\":\"1",sha{[2..64]},"\""));;
  if not D972JKPB1AuditVerdict(bad,sha) then rejected:=rejected+1;; fi;
  bad:=D972JKPB1ReplaceFirst(verdict,"\"mutation_tests_rejected\":23",
    "\"mutation_tests_rejected\":22");;
  if not D972JKPB1AuditVerdict(bad,sha) then rejected:=rejected+1;; fi;
  bad:=D972JKPB1ReplaceFirst(verdict,"\"mutation_tests_rejected\":4",
    "\"mutation_tests_rejected\":3");;
  if not D972JKPB1AuditVerdict(bad,sha) then rejected:=rejected+1;; fi;
  if rejected<>10 then
    Error("task169b bootstrap: static fixture mutations ",rejected);
  fi;
  return rejected;
end;;

for D972JKPB1PinRow in D972JKPB1Pins do
  D972JKPB1Pin(D972JKPB1PinRow);;
od;

if D972JKPB1PerProcessOuterSeconds<=D972JKPB1DomainSeconds or
   D972JKPB1OuterTotalSeconds>D972JKPB1EnvelopeSeconds or
   3*D972JKPB1PerProcessOuterSeconds>D972JKPB1EnvelopeSeconds then
  Error("task169b bootstrap: resource envelope constants");
fi;

## Refuse every known full lane flag.  This driver is preflight-only.
if IsBound(D972_R07_JOINT_COEFF_INTERSECTION_V1_RUN) and
   D972_R07_JOINT_COEFF_INTERSECTION_V1_RUN=true then
  Error("task169b bootstrap: refuses task169 full mode");
fi;
if IsBound(D972_R07_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_FULL) and
   D972_R07_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_FULL=true then
  Error("task169b bootstrap: refuses bootstrap full mode");
fi;

D972JKPB1Self :=
  IsBound(D972_R07_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_SELFTEST) and
  D972_R07_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_SELFTEST=true;;
D972JKPB1Run :=
  IsBound(D972_R07_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_RUN) and
  D972_R07_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_RUN=true;;
if D972JKPB1Self=D972JKPB1Run then
  Error("task169b bootstrap: select exactly one explicit bootstrap mode");
fi;

if D972JKPB1Self then
  D972JKPB1FixtureMutations:=D972JKPB1FixtureSelftest();;
  Print("R07_760_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_DRIVER_STATIC_SELFTEST_PASS ",
        "fixture_mutations=",D972JKPB1FixtureMutations,
        " python_processes=0 full=false grade=CANDIDATE\n");;
else
  D972JKPB1OwnedOutputs := [
    D972JKPB1TemporaryA,D972JKPB1TemporaryB,D972JKPB1Canonical,
    D972JKPB1Verdict,D972JKPB1ProducerLogA,D972JKPB1ProducerLogB,
    D972JKPB1CheckerLog,D972JKPB1Timing,D972JKPB1Hashes,
    D972JKPB1StageOK,D972JKPB1FinalOK,
    Concatenation(D972JKPB1TemporaryA,".tmp"),
    Concatenation(D972JKPB1TemporaryB,".tmp"),
    Concatenation(D972JKPB1Verdict,".tmp")
  ];;
  D972JKPB1RejectPreexisting(D972JKPB1OwnedOutputs);;
  Exec("mkdir -p ci/out");;
  D972JKPB1RunCommand:=Concatenation(
    "timeout --signal=TERM 17900s bash -o pipefail -c '",
    "set -euo pipefail; SECONDS=0; ",
    "timeout --signal=TERM 5700s python3 -u -B ",
      D972JKPB1ShellQuote(D972JKPB1Producer),
      " --preflight --domain-seconds 5400 --output ",
      D972JKPB1ShellQuote(D972JKPB1TemporaryA),
      " 2>&1 | tee ",D972JKPB1ShellQuote(D972JKPB1ProducerLogA),"; ",
    "producer_a_elapsed=$SECONDS; producer_b_started=$SECONDS; ",
    "timeout --signal=TERM 5700s python3 -u -B ",
      D972JKPB1ShellQuote(D972JKPB1Producer),
      " --preflight --domain-seconds 5400 --output ",
      D972JKPB1ShellQuote(D972JKPB1TemporaryB),
      " 2>&1 | tee ",D972JKPB1ShellQuote(D972JKPB1ProducerLogB),"; ",
    "producer_b_elapsed=$((SECONDS-producer_b_started)); ",
    "cmp -s ",D972JKPB1ShellQuote(D972JKPB1TemporaryA)," ",
      D972JKPB1ShellQuote(D972JKPB1TemporaryB),"; ",
    "test $(grep -F -c R07_760_JOINT_COEFF_INTERSECTION_V1_PRODUCER_PASS ",
      D972JKPB1ShellQuote(D972JKPB1ProducerLogA),") -eq 1; ",
    "test $(grep -F -c R07_760_JOINT_COEFF_INTERSECTION_V1_PRODUCER_PASS ",
      D972JKPB1ShellQuote(D972JKPB1ProducerLogB),") -eq 1; ",
    "grep -F -q R07_760_JOINT_COEFF_INTERSECTION_V1_PREFLIGHT_READY ",
      D972JKPB1ShellQuote(D972JKPB1TemporaryA),"; ",
    "grep -F -q R07_760_JOINT_COEFF_INTERSECTION_V1_PREFLIGHT_READY ",
      D972JKPB1ShellQuote(D972JKPB1TemporaryB),"; ",
    "checker_started=$SECONDS; ",
    "timeout --signal=TERM 5700s python3 -u -B ",
      D972JKPB1ShellQuote(D972JKPB1Checker),
      " --check --domain-seconds 5400 --receipt ",
      D972JKPB1ShellQuote(D972JKPB1TemporaryA),
      " --output ",D972JKPB1ShellQuote(D972JKPB1Verdict),
      " 2>&1 | tee ",D972JKPB1ShellQuote(D972JKPB1CheckerLog),"; ",
    "checker_elapsed=$((SECONDS-checker_started)); total_elapsed=$SECONDS; ",
    "if [ $total_elapsed -gt 18000 ]; then exit 98; fi; ",
    "printf \"producer_a_elapsed=%s\\nproducer_b_elapsed=%s\\n",
      "checker_elapsed=%s\\ntotal_elapsed=%s\\ndomain_seconds=5400\\n",
      "per_process_outer_seconds=5700\\nouter_total_seconds=17900\\n",
      "envelope_seconds=18000\\nproducer_processes=2\\nchecker_processes=1\\n",
      "byte_equal_before_checker=true\\nfull=false\\n\" ",
      "$producer_a_elapsed $producer_b_elapsed $checker_elapsed ",
      "$total_elapsed > ",D972JKPB1ShellQuote(D972JKPB1Timing),"; ",
    "printf %s R07_760_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_STAGE_EXIT_ZERO > ",
      D972JKPB1ShellQuote(D972JKPB1StageOK),"'");;
  if D972JKPB1Count(D972JKPB1RunCommand,
       Concatenation("python3 -u -B ",
         D972JKPB1ShellQuote(D972JKPB1Producer)))<>2 or
     D972JKPB1Count(D972JKPB1RunCommand,
       Concatenation("python3 -u -B ",
         D972JKPB1ShellQuote(D972JKPB1Checker)))<>1 or
     D972JKPB1Count(D972JKPB1RunCommand," --preflight ")<>2 or
     D972JKPB1Count(D972JKPB1RunCommand," --check ")<>1 or
     D972JKPB1Count(D972JKPB1RunCommand,"--domain-seconds 5400")<>3 or
     D972JKPB1Count(D972JKPB1RunCommand,"timeout --signal=TERM 5700s")<>3 or
     D972JKPB1Count(D972JKPB1RunCommand,"bash -o pipefail")<>1 or
     D972JKPB1Count(D972JKPB1RunCommand,"set -euo pipefail")<>1 or
     D972JKPB1Count(D972JKPB1RunCommand," --full ")<>0 then
    Error("task169b bootstrap: serial preflight command shape");
  fi;
  Exec(D972JKPB1RunCommand);;
  if D972JKPB1Read(D972JKPB1StageOK,"stage sentinel")<>
       "R07_760_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_STAGE_EXIT_ZERO" then
    Error("task169b bootstrap: producer/checker process failure");
  fi;
  D972JKPB1LogA:=D972JKPB1Read(D972JKPB1ProducerLogA,"producer log A");;
  D972JKPB1LogB:=D972JKPB1Read(D972JKPB1ProducerLogB,"producer log B");;
  D972JKPB1CheckerRaw:=D972JKPB1Read(D972JKPB1CheckerLog,"checker log");;
  D972JKPB1CleanLog(D972JKPB1LogA,"producer A");;
  D972JKPB1CleanLog(D972JKPB1LogB,"producer B");;
  D972JKPB1CleanLog(D972JKPB1CheckerRaw,"checker");;
  if D972JKPB1Count(D972JKPB1LogA,
       "R07_760_JOINT_COEFF_INTERSECTION_V1_PRODUCER_PASS")<>1 or
     D972JKPB1Count(D972JKPB1LogB,
       "R07_760_JOINT_COEFF_INTERSECTION_V1_PRODUCER_PASS")<>1 or
     D972JKPB1Count(D972JKPB1LogA,
       "state=R07_760_JOINT_COEFF_INTERSECTION_V1_PREFLIGHT_READY")<>1 or
     D972JKPB1Count(D972JKPB1LogB,
       "state=R07_760_JOINT_COEFF_INTERSECTION_V1_PREFLIGHT_READY")<>1 or
     D972JKPB1Count(D972JKPB1LogA,"canaries=31")<>1 or
     D972JKPB1Count(D972JKPB1LogB,"canaries=31")<>1 or
     D972JKPB1Count(D972JKPB1LogA,"domain_seconds=5400")<>1 or
     D972JKPB1Count(D972JKPB1LogB,"domain_seconds=5400")<>1 or
     D972JKPB1Count(D972JKPB1CheckerRaw,
       "R07_760_JOINT_COEFF_INTERSECTION_V1_CHECKER_PASS")<>1 or
     D972JKPB1Count(D972JKPB1CheckerRaw,"mutations=23")<>1 or
     D972JKPB1Count(D972JKPB1CheckerRaw,"cache_fixture_words=1365")<>1 or
      D972JKPB1Count(D972JKPB1CheckerRaw,
         "cache_fixture_mutations=4")<>1 or
      D972JKPB1Count(D972JKPB1CheckerRaw,
         "gamma_schema_mutations=5")<>1 or
      D972JKPB1Count(D972JKPB1CheckerRaw,
        "empty_affine_inconsistent=true")<>1 or
     D972JKPB1Count(D972JKPB1CheckerRaw,"canaries=31")<>1 or
     D972JKPB1Count(D972JKPB1CheckerRaw,"domain_seconds=5400")<>1 then
    Error("task169b bootstrap: exact process markers");
  fi;
  D972JKPB1RawA:=D972JKPB1Read(D972JKPB1TemporaryA,"temporary A");;
  D972JKPB1RawB:=D972JKPB1Read(D972JKPB1TemporaryB,"temporary B");;
  if D972JKPB1RawA<>D972JKPB1RawB or
     not D972JKPB1AuditPreflight(D972JKPB1RawA) then
    Error("task169b bootstrap: twice-identical preflight audit");
  fi;
  D972JKPB1ASHA:=HexSHA256(D972JKPB1RawA);;
  D972JKPB1VerdictRaw:=D972JKPB1Read(D972JKPB1Verdict,"checker verdict");;
  if D972JKPB1Count(D972JKPB1CheckerRaw,
       Concatenation("target_sha256=",D972JKPB1ASHA))<>1 or
     not D972JKPB1AuditVerdict(D972JKPB1VerdictRaw,D972JKPB1ASHA) then
    Error("task169b bootstrap: checker target binding");
  fi;
  D972JKPB1TimingRaw:=D972JKPB1Read(D972JKPB1Timing,"timing");;
  if D972JKPB1Count(D972JKPB1TimingRaw,"domain_seconds=5400")<>1 or
     D972JKPB1Count(D972JKPB1TimingRaw,
       "per_process_outer_seconds=5700")<>1 or
     D972JKPB1Count(D972JKPB1TimingRaw,"outer_total_seconds=17900")<>1 or
     D972JKPB1Count(D972JKPB1TimingRaw,"envelope_seconds=18000")<>1 or
     D972JKPB1Count(D972JKPB1TimingRaw,"producer_processes=2")<>1 or
     D972JKPB1Count(D972JKPB1TimingRaw,"checker_processes=1")<>1 or
     D972JKPB1Count(D972JKPB1TimingRaw,
       "byte_equal_before_checker=true")<>1 or
     D972JKPB1Count(D972JKPB1TimingRaw,"full=false")<>1 then
    Error("task169b bootstrap: timing/process audit");
  fi;
  ## Publication is deliberately a second serial shell command.  It occurs
  ## only after every GAP-side marker, receipt, verdict, claim, and SHA gate.
  D972JKPB1PublishCommand:=Concatenation(
    "bash -o pipefail -c 'set -euo pipefail; cmp -s ",
      D972JKPB1ShellQuote(D972JKPB1TemporaryA)," ",
      D972JKPB1ShellQuote(D972JKPB1TemporaryB),"; cp -- ",
      D972JKPB1ShellQuote(D972JKPB1TemporaryA)," ",
      D972JKPB1ShellQuote(D972JKPB1Canonical),"; sha256sum ",
      D972JKPB1ShellQuote(D972JKPB1TemporaryA)," ",
      D972JKPB1ShellQuote(D972JKPB1TemporaryB)," ",
      D972JKPB1ShellQuote(D972JKPB1Canonical)," ",
      D972JKPB1ShellQuote(D972JKPB1Verdict)," ",
      D972JKPB1ShellQuote(D972JKPB1ProducerLogA)," ",
      D972JKPB1ShellQuote(D972JKPB1ProducerLogB)," ",
      D972JKPB1ShellQuote(D972JKPB1CheckerLog)," ",
      D972JKPB1ShellQuote(D972JKPB1Timing)," ",
      D972JKPB1ShellQuote(D972JKPB1StageOK)," > ",
      D972JKPB1ShellQuote(D972JKPB1Hashes),"; printf %s ",
      "R07_760_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_EXIT_ZERO > ",
      D972JKPB1ShellQuote(D972JKPB1FinalOK),"'");;
  Exec(D972JKPB1PublishCommand);;
  if D972JKPB1Read(D972JKPB1Canonical,"canonical preflight")<>
       D972JKPB1RawA or
     D972JKPB1Read(D972JKPB1FinalOK,"final sentinel")<>
       "R07_760_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_EXIT_ZERO" then
    Error("task169b bootstrap: publication failure");
  fi;
  D972JKPB1HashesRaw:=D972JKPB1Read(D972JKPB1Hashes,"hash manifest");;
  if D972JKPB1Count(D972JKPB1HashesRaw,D972JKPB1ASHA)<3 or
     ForAny([D972JKPB1TemporaryA,D972JKPB1TemporaryB,
             D972JKPB1Canonical,D972JKPB1Verdict,
             D972JKPB1ProducerLogA,D972JKPB1ProducerLogB,
             D972JKPB1CheckerLog,D972JKPB1Timing,D972JKPB1StageOK],
       path->D972JKPB1Count(D972JKPB1HashesRaw,path)<>1) then
    Error("task169b bootstrap: hash manifest audit");
  fi;
  Print("R07_760_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_DRIVER_PASS ",
        "mode=preflight bootstrap=true grade=CROSS_CHECKED ",
        "producer_processes=2 checker_processes=1 byte_identical=true ",
        "domain_seconds=5400 full=false receipt_sha256=",D972JKPB1ASHA,
        " verdict_sha256=",HexSHA256(D972JKPB1VerdictRaw),
        " timing_sha256=",HexSHA256(D972JKPB1TimingRaw),"\n");;
fi;
