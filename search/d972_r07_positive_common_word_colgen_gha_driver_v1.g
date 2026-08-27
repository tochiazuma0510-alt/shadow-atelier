#############################################################################
## Task179 positive-only R07 common-word column generation driver v1.
## ASCII only.  One producer, then one helper-nonshared checker, serially.
#############################################################################

if not IsBound(D972_R07_POSITIVE_COMMON_WORD_COLGEN_V1_MODE) then
  Error("task179 driver: MODE must be SELFTEST or PRODUCTION");
fi;
D179Mode:=D972_R07_POSITIVE_COMMON_WORD_COLGEN_V1_MODE;;
if D179Mode<>"SELFTEST" and D179Mode<>"PRODUCTION" then
  Error("task179 driver: invalid MODE");
fi;

D179Producer:="search/d972_r07_positive_common_word_colgen_v1.py";;
D179Checker:="crosscheck/check_d972_r07_positive_common_word_colgen_v1.py";;
D179Fixture:="search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json";;
D179Common:="R07_POSITIVE_COMMON_WORD_COLGEN_COMMON_WORD";;
D179Receipt:="ci/out/d972_r07_positive_common_word_colgen_v1.json";;
D179Checkpoint:="ci/out/d972_r07_positive_common_word_colgen_v1.json.checkpoint.json";;
D179Verdict:="ci/out/d972_r07_positive_common_word_colgen_verdict_v1.json";;
D179ProducerLog:="ci/out/d972_r07_positive_common_word_colgen_producer_v1.log";;
D179CheckerLog:="ci/out/d972_r07_positive_common_word_colgen_checker_v1.log";;
D179Timing:="ci/out/d972_r07_positive_common_word_colgen_timing_v1.txt";;
D179Hashes:="ci/out/d972_r07_positive_common_word_colgen_hashes_v1.txt";;
D179Shell:="ci/out/d972_r07_positive_common_word_colgen_command_v1.sh";;
D179OK:="ci/out/d972_r07_positive_common_word_colgen_v1.ok";;
D179ResumeInput:="ci/in/d972_r07_positive_common_word_colgen_checkpoint_v1.json";;
D179ResumeArg:="";;

D179ProducerBytes:=119396;;
D179ProducerSHA:="448123e3ccba4324f4d19a09eeb6a2ba217d611ef5053d4cfa27e61ac69a2512";;
D179CheckerBytes:=70020;;
D179CheckerSHA:="473bad89f9656dd67f4313398b5bdbb253a3495e1e20855d90781b4875309f2d";;
D179FixtureBytes:=407;;
D179FixtureSHA:="46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78";;

D179Pins:=[
  [D179Producer,D179ProducerBytes,D179ProducerSHA],
  [D179Checker,D179CheckerBytes,D179CheckerSHA],
  [D179Fixture,D179FixtureBytes,D179FixtureSHA],
  ["sol/luna_task_179_r07_positive_common_word_colgen_v1.md",13105,"f97870ec0243b2c399928bcef4f89134f1cd41f15869cc88e3ba7d9dc6956a73"],
  ["sol/proof_r07_actual_singleton_coarse_inverse_selector_v142.md",4942,"5f0fffe64b729a8e44643ce86e9d588ef96cbe199ef8ca03741c712c2b162ee8"],
  ["sol/proof_r07_actual_weighted_support_hitting_selector_v143.md",5253,"aae57d5481d7e649d449b58d06ade2d9cbf90fa48d50a8ae43650da5243cf259"],
  ["sol/proof_r07_witness_first_fibre_dovetail_selector_v139.md",8310,"62e2160348db38eca1570b2ca6eb8934b885569f4e8cfb276a91b98c9b983920"],
  ["sol/proof_r07_positive_only_common_word_colgen_v140.md",10073,"6d388a74c75d55d215b0035496c451aa9de5bbc7a8248c277e76021092b8562b"],
  ["sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md",6371,"9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456"],
  ["sol/proof_r07_full_e4_seven_evaluation_orbit_selector_v110.md",12136,"dd0b75d6dc85229405a3a95e3631a709aa40a0ad21f2c17b96106dae2c7989dc"],
  ["sol/proof_pb4_eleven_relator_presentation_equality_v108.md",6742,"4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f"],
  ["sol/proof_pb3_two_relator_presentation_equality_v121.md",5762,"efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5"],
  ["sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md",7939,"daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348"],
  ["sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md",8545,"b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3"],
  ["sol/proof_r07_q4_q0_noncontiguous_deletion_layout_v135.md",4539,"75c511a765ad88ec1aa72c63a0d1965ac85724695d743cbf00350572a884cf67"],
  ["search/d972_r07_all_seven_raw_bridge_preflight_v1.py",60306,"1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"],
  ["crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py",85848,"c55ec99a9a920cd5d0ef92db7d5f2ad841dda7b0f1dcc59a5dc45e469ed6f7cc"],
  ["search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g",21580,"dbe147f98774fde50dee86de7306f9e18243ac1becef0ec7516765bcb2e08765"],
  ["search/d972_r07_all_seven_extension_section_census_v1.py",66109,"878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"],
  ["crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py",84980,"4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"],
  ["search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g",15929,"1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995"],
  ["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json",231570,"3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"],
  ["ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json",2166036,"1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"],
  ["search/d972_b345_seedspan_triple4_v1.py",535219,"fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"],
  ["search/d972_b345_triple_cube_raw_lambda_census_v1.py",126942,"d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"],
  ["search/d972_b345_joint_kernel_qstar_closure_v1.py",67945,"06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"],
  ["search/d972_r07_full_e4_joint_orbit_preflight_v7.py",21918,"92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"],
  ["search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py",33409,"f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"],
  ["search/d972_b345_target6_dual_colgen_v2.py",444497,"b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"],
  ["search/d972_b345_full_d2_dual_correlation_v1.py",78832,"6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52"],
  ["search/d972_b345_full_d2_dual_correlation_v2.py",42449,"6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f"]
];;

D179Read:=function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task179 driver: missing ",label," ",path); fi;
  return raw;
end;;

D179Count:=function(raw,needle)
  local count,position;
  if Length(needle)=0 then Error("task179 driver: empty needle"); fi;
  count:=0;; position:=PositionSublist(raw,needle);;
  while position<>fail do
    count:=count+1;; position:=PositionSublist(raw,needle,position);;
  od;
  return count;
end;;

D179Pin:=function(row)
  local raw;
  raw:=D179Read(row[1],"pin");;
  if Length(raw)<>row[2] or HexSHA256(raw)<>row[3] then
    Error("task179 driver: pin drift ",row[1]);
  fi;
end;;

D179RejectOwned:=function(paths)
  local path;
  if Length(paths)<>Length(Set(paths)) then Error("task179 driver: duplicate output"); fi;
  for path in paths do
    if IsExistingFile(path) then Error("task179 driver: stale output ",path); fi;
  od;
end;;

D179Clean:=function(raw,label)
  local bad;
  for bad in ["Traceback (most recent call last):","SyntaxError","AssertionError",
              "PRODUCER_STOP","CHECKER_STOP","Killed"] do
    if D179Count(raw,bad)<>0 then Error("task179 driver: bad log ",label," ",bad); fi;
  od;
end;;

for D179Row in D179Pins do D179Pin(D179Row);; od;
if IsBound(D972_R07_POSITIVE_COMMON_WORD_COLGEN_V1_RESUME_SHA256) then
  if not IsExistingFile(D179ResumeInput) or
     HexSHA256(D179Read(D179ResumeInput,"resume checkpoint"))<>
       D972_R07_POSITIVE_COMMON_WORD_COLGEN_V1_RESUME_SHA256 then
    Error("task179 driver: resume checkpoint pin drift");
  fi;
  D179ResumeArg:=Concatenation(" --resume ",D179ResumeInput);;
fi;
D179RejectOwned([D179Receipt,D179Checkpoint,D179Verdict,D179ProducerLog,
                 D179CheckerLog,D179Timing,D179Hashes,D179Shell,D179OK]);;

D179Stream:=OutputTextFile(D179Shell,false);;
if D179Stream=fail then Error("task179 driver: shell open"); fi;
SetPrintFormattingStatus(D179Stream,false);;
PrintTo(D179Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D179Stream,"command -v python3 >/dev/null\ncommand -v timeout >/dev/null\nmkdir -p ci/out\n");;
PrintTo(D179Stream,"p0=$(date +%s)\n");;
if D179Mode="SELFTEST" then
  PrintTo(D179Stream,"timeout --signal=TERM --kill-after=60s 900s python3 -u -B ",
    D179Producer," --mode SELFTEST --output ",D179Receipt," 2>&1 | tee ",D179ProducerLog,"\n");;
  PrintTo(D179Stream,"test ${PIPESTATUS[0]} -eq 0\n");;
  PrintTo(D179Stream,"test \"$(grep -Fxc 'R07_POSITIVE_COMMON_WORD_COLGEN_V1_PRODUCER_SELFTEST_PASS mutation_attempted=15 mutation_rejected=15 coarse_inverse_checks=4 weighted_mutation_attempted=8 weighted_mutation_rejected=8' ",D179ProducerLog,")\" -eq 1\n");;
  PrintTo(D179Stream,"p1=$(date +%s)\n");;
  PrintTo(D179Stream,"timeout --signal=TERM --kill-after=60s 900s python3 -u -B ",
    D179Checker," --mode SELFTEST --receipt ",D179Receipt," --verdict ",D179Verdict,
    " 2>&1 | tee ",D179CheckerLog,"\n");;
  PrintTo(D179Stream,"test ${PIPESTATUS[0]} -eq 0\n");;
  PrintTo(D179Stream,"test \"$(grep -Fxc 'R07_POSITIVE_COMMON_WORD_COLGEN_V1_CHECKER_SELFTEST_PASS mutation_attempted=15 mutation_rejected=15 coarse_inverse_checks=4 weighted_mutation_attempted=8 weighted_mutation_rejected=8' ",D179CheckerLog,")\" -eq 1\n");;
else
  PrintTo(D179Stream,"timeout --signal=TERM --kill-after=60s 19500s python3 -u -B ",
    D179Producer," --mode PRODUCTION --seconds 19200 --output ",D179Receipt,
    D179ResumeArg," 2>&1 | tee ",D179ProducerLog,"\n");;
  PrintTo(D179Stream,"test ${PIPESTATUS[0]} -eq 0\n");;
  PrintTo(D179Stream,"test \"$(grep -Ec '^R07_POSITIVE_COMMON_WORD_COLGEN_V1_PRODUCER_TERMINAL (R07_POSITIVE_COMMON_WORD_COLGEN_COMMON_WORD|UNKNOWN_RESOURCE:[^[:cntrl:]]+|UNKNOWN_INPUT:[^[:cntrl:]]+)$' ",D179ProducerLog,")\" -eq 1\n");;
  PrintTo(D179Stream,"p1=$(date +%s)\n");;
  PrintTo(D179Stream,"timeout --signal=TERM --kill-after=60s 1500s python3 -u -B ",
    D179Checker," --mode PRODUCTION --receipt ",D179Receipt," --verdict ",D179Verdict,
    " 2>&1 | tee ",D179CheckerLog,"\n");;
  PrintTo(D179Stream,"test ${PIPESTATUS[0]} -eq 0\n");;
  PrintTo(D179Stream,"test \"$(grep -Ec '^R07_POSITIVE_COMMON_WORD_COLGEN_V1_CHECKER_PRODUCTION_PASS terminal=(R07_POSITIVE_COMMON_WORD_COLGEN_COMMON_WORD|UNKNOWN_RESOURCE:[^[:cntrl:]]+|UNKNOWN_INPUT:[^[:cntrl:]]+)$' ",D179CheckerLog,")\" -eq 1\n");;
fi;
PrintTo(D179Stream,"p2=$(date +%s)\nprintf 'mode=",D179Mode,
  " producer_seconds=%s checker_seconds=%s\\n' \"$((p1-p0))\" \"$((p2-p1))\" > ",D179Timing,"\n");;
PrintTo(D179Stream,"sha256sum ",D179Receipt," ",D179Verdict," > ",D179Hashes,"\n");;
PrintTo(D179Stream,"touch ",D179OK,"\n");;
CloseStream(D179Stream);;

D179ShellRaw:=D179Read(D179Shell,"generated shell");;
if D179Count(D179ShellRaw,"\\\n")<>0 then
  Error("task179 driver: generated shell contains formatting continuation");
fi;
Exec(Concatenation("bash ",D179Shell));;
if not IsExistingFile(D179OK) then Error("task179 driver: shell sentinel missing"); fi;

D179ProducerRaw:=D179Read(D179ProducerLog,"producer log");;
D179CheckerRaw:=D179Read(D179CheckerLog,"checker log");;
D179Clean(D179ProducerRaw,"producer");; D179Clean(D179CheckerRaw,"checker");;
D179ReceiptRaw:=D179Read(D179Receipt,"receipt");;
D179VerdictRaw:=D179Read(D179Verdict,"verdict");;
if D179Count(D179ReceiptRaw,"\"self_digest\":\"")<1 or
   D179Count(D179VerdictRaw,"\"self_digest\":\"")<>1 then
  Error("task179 driver: digest cardinality");
fi;
if D179Mode="SELFTEST" then
  if D179Count(D179ProducerRaw,"PRODUCER_SELFTEST_PASS mutation_attempted=15 mutation_rejected=15 coarse_inverse_checks=4 weighted_mutation_attempted=8 weighted_mutation_rejected=8")<>1 or
     D179Count(D179CheckerRaw,"CHECKER_SELFTEST_PASS mutation_attempted=15 mutation_rejected=15 coarse_inverse_checks=4 weighted_mutation_attempted=8 weighted_mutation_rejected=8")<>1 then
    Error("task179 driver: SELFTEST marker");
  fi;
  D179Terminal:="SELFTEST";;
else
  if D179Count(D179ReceiptRaw,"\"negative_claim\":false")<1 or
     D179Count(D179ReceiptRaw,"\"separator\":false")<1 or
     D179Count(D179ReceiptRaw,"\"negative_claim\":true")<>0 or
     D179Count(D179ReceiptRaw,"\"separator\":true")<>0 then
    Error("task179 driver: positive-only claim gate");
  fi;
  if D179Count(D179ReceiptRaw,Concatenation("\"terminal\":\"",D179Common,"\""))=1 then
    D179Terminal:=D179Common;;
  elif D179Count(D179ReceiptRaw,"\"terminal\":\"UNKNOWN_RESOURCE:")=1 then
    D179Terminal:="UNKNOWN_RESOURCE";;
  elif D179Count(D179ReceiptRaw,"\"terminal\":\"UNKNOWN_INPUT:")=1 then
    D179Terminal:="UNKNOWN_INPUT";;
  else
    Error("task179 driver: no unique typed terminal");
  fi;
fi;

# Print the external sentinel through GAP's supported user stream API.
WriteLine(OutputTextUser(),Concatenation(
  "R07_POSITIVE_COMMON_WORD_COLGEN_V1_GHA_DRIVER_PASS mode=",D179Mode,
  " terminal=",D179Terminal));;
