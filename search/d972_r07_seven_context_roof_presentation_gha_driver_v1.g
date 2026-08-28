#############################################################################
## Task198b generic fail-closed driver.  ASCII only; no workflow changes.
#############################################################################
if not IsBound(D972_R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_MODE) then
  Error("task198: MODE must be bound");
fi;
D198Mode:=D972_R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_MODE;;
if not IsString(D198Mode) or not D198Mode in ["SELFTEST","PRODUCTION"] then
  Error("task198: invalid MODE");
fi;
D198P:="search/d972_r07_seven_context_roof_presentation_v1.py";;
D198C:="crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py";;
D198F:="search/certs/d972_r07_seven_context_roof_presentation_selftest_v1_20260828.json";;
D198I:="ci/in/d972_r07_all_seven_extension_section_census_v1.json";;
D198M:="ci/in/d972_r07_all_seven_extension_section_census_v1.manifest.json";;
D198R:="ci/out/d972_r07_seven_context_roof_presentation_v1.json";;
D198V:="ci/out/d972_r07_seven_context_roof_presentation_crosscheck_v1.json";;
D198PL:="ci/out/d972_r07_seven_context_roof_presentation_producer.log";;
D198CL:="ci/out/d972_r07_seven_context_roof_presentation_checker.log";;
D198OK:="ci/out/d972_r07_seven_context_roof_presentation_v1.ok";;
D198T:="ci/out/d972_r07_seven_context_roof_presentation_terminal.txt";;
D198K:="ci/out/d972_r07_seven_context_roof_presentation_resume_v1.checkpoint.json";;
D198KM:="ci/out/d972_r07_seven_context_roof_presentation_resume_v1.manifest.json";;
D198RI:="ci/in/d972_r07_seven_context_roof_presentation_resume_v1.checkpoint.json";;
D198RM:="ci/in/d972_r07_seven_context_roof_presentation_resume_v1.manifest.json";;
D198SR:="ci/out/d972_r07_seven_context_roof_presentation_selftest.receipt.json";;
D198SV:="ci/out/d972_r07_seven_context_roof_presentation_selftest.verdict.json";;
D198SP:="ci/out/d972_r07_seven_context_roof_presentation_selftest";;
D198SPath:="ci/out/d972_r07_seven_context_roof_presentation_command.sh";;
# Conservative one-process GHA staging estimate, also used as the hard cap.
D198EstimatedWallSeconds:=14400;;
D198EstimatedPeakRSSBytes:=8000000000;;

D198Read:=function(path,label)
  local raw; raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task198: missing ",label); fi;
  return raw;
end;;
D198Pin:=function(row)
  local raw; raw:=D198Read(row[1],"pin");;
  if Length(raw)<>row[3] or HexSHA256(raw)<>row[2] then
    Error("task198: pin drift ",row[1]);
  fi;
end;;
D198Count:=function(raw,needle)
  local n,p; n:=0;; p:=PositionSublist(raw,needle);;
  while p<>fail do n:=n+1;; p:=PositionSublist(raw,needle,p+1);; od;
  return n;
end;;
D198Reject:=function(paths)
  local p;
  for p in paths do
    if IsExistingFile(p) then Error("task198: stale output ",p); fi;
  od;
end;;

# Path-sorted normalized union of the complete final task175/176/179
# producer/checker dependency cone.  This is direct driver authentication.
D198Cone:=[
 ["ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json","1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df",2166036],
 ["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json","3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72",231570],
 ["crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py","4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695",84980],
 ["crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py","0b45c3daa1db6cad63d434170c65d0dbfa928efc51543b881dc0aa2e3a0f1fce",88503],
 ["crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py","e3917ec05b95b8996e3a5cec1cc2bfde51c3ed8c6972175fd9be9e1178205c23",12423],
 ["crosscheck/check_d972_r07_positive_common_word_colgen_v1.py","de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d",73780],
 ["search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json","86c6f3a72a3f852a1be7c5323bf72c7ad987377fd5483b6e32528fe263e290ff",45246709],
 ["search/check_d972_b345_joint_kernel_qstar_closure_v2.py","5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88",5942],
 ["search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py","f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f",33409],
 ["search/d972_b345_full_d2_dual_correlation_v1.py","6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52",78832],
 ["search/d972_b345_full_d2_dual_correlation_v2.py","6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f",42449],
 ["search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g","8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7",3912],
 ["search/d972_b345_joint_kernel_qstar_closure_v1.py","06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc",67945],
 ["search/d972_b345_seedspan_triple4_v1.py","fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29",535219],
 ["search/d972_b345_target6_dual_colgen_v2.py","b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7",444497],
 ["search/d972_b345_triple_cube_raw_lambda_census_v1.py","d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db",126942],
 ["search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g","1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995",15929],
 ["search/d972_r07_all_seven_extension_section_census_v1.py","878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b",66109],
 ["search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g","919e7a9efe7385444c480203dc51525873e770236777dd61e2f6fc1ef22de494",22052],
 ["search/d972_r07_all_seven_raw_bridge_preflight_v1.py","1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa",60306],
 ["search/d972_r07_full_e4_joint_orbit_preflight_v7.py","92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed",21918],
 ["search/d972_r07_positive_common_word_colgen_gha_driver_v1.g","48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b",12872],
 ["search/d972_r07_positive_common_word_colgen_v1.py","47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7",123870],
 ["sol/audit_r07_all_seven_bridge_checkpoint_v123.md","272aabc882599031c4da0472f8f2340043b32571e8e05ecaa58fc5ad1c6a31ac",5017],
 ["sol/luna_reply_157ee_b345_joint_kernel_qstar_closure.md","53f20c2cb1395b8ff59ee961e1d5a14d55156a488eb6fa49edefed5dd7619eee",4118],
 ["sol/luna_reply_173_r07_all_seven_raw_bridge_inventory_v1.md","189a642fc8654f163b0b7964b75043ea393cac31a0b56b84ae0fddf2f73c3695",24283],
 ["sol/luna_reply_174_r07_target6_context_image_census_v1.md","516d15d4ad73e9e2d8e564789e856224c35a30a235e46e87ad857cb20470b49f",13224],
 ["sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md","64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4",11226],
 ["sol/luna_task_175_r07_all_seven_raw_bridge_preflight_v1.md","5d0d8e006c6a752e5a525b188c9d95ba0c858aa69147432e639fe3e735ffefee",8584],
 ["sol/luna_task_175b_r07_all_seven_raw_bridge_implementation_repair.md","a41f2446fd1c9f0bd60a7189db682784f4e69e24e8958f7c4505cd1eb9741836",5136],
 ["sol/luna_task_176_r07_all_seven_extension_section_census_v1.md","a1778c17c33e42880a6dd0c2480303a13702cb38950cf836a4ca9d8cca6fa332",7054],
 ["sol/luna_task_179_r07_positive_common_word_colgen_v1.md","f97870ec0243b2c399928bcef4f89134f1cd41f15869cc88e3ba7d9dc6956a73",13105],
 ["sol/proof_pb3_two_relator_presentation_equality_v121.md","efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5",5762],
 ["sol/proof_pb4_eleven_relator_presentation_equality_v108.md","4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f",6742],
 ["sol/proof_r07_actual_singleton_coarse_inverse_selector_v142.md","5f0fffe64b729a8e44643ce86e9d588ef96cbe199ef8ca03741c712c2b162ee8",4942],
 ["sol/proof_r07_actual_weighted_support_hitting_selector_v143.md","aae57d5481d7e649d449b58d06ade2d9cbf90fa48d50a8ae43650da5243cf259",5253],
 ["sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md","b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3",8545],
 ["sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md","9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456",6371],
 ["sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md","daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348",7939],
 ["sol/proof_r07_full_e4_seven_evaluation_orbit_selector_v110.md","dd0b75d6dc85229405a3a95e3631a709aa40a0ad21f2c17b96106dae2c7989dc",12136],
 ["sol/proof_r07_positive_only_common_word_colgen_v140.md","6d388a74c75d55d215b0035496c451aa9de5bbc7a8248c277e76021092b8562b",10073],
 ["sol/proof_r07_q4_q0_noncontiguous_deletion_layout_v135.md","75c511a765ad88ec1aa72c63a0d1965ac85724695d743cbf00350572a884cf67",4539],
 ["sol/proof_r07_witness_first_fibre_dovetail_selector_v139.md","62e2160348db38eca1570b2ca6eb8934b885569f4e8cfb276a91b98c9b983920",8310]
];;
if Length(D198Cone)<>43 or Set(D198Cone)<>D198Cone then
  Error("task198: dependency cone is not normalized");
fi;

D198Pins:=[
 [D198P,"292473d5f9d01827bb6971352a82b8f238be1b1a19a98002c575c8ebf39760ee",136938],
 [D198C,"fe645cdc94919b20942aa1d0497b29ec954feeb3054b959d666ebe6db84cb920",153337],
 [D198F,"fb31f6a0be2f2f5b530c6fe99796476ea16edb72fe7ddc192323995f2ae55ce7",1605],
 ["ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json","1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df",2166036],
 ["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json","3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72",231570],
 ["search/d972_b345_joint_kernel_qstar_closure_v1.py","06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc",67945],
 ["search/check_d972_b345_joint_kernel_qstar_closure_v2.py","5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88",5942],
 ["search/check_d972_b345_joint_kernel_qstar_closure_v1.py","9e721634d1f16be806e315eec263ec272bc023587f862703c094b7dd37c0111f",47661],
 ["search/d972_b345_seedspan_triple4_v1.py","fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29",535219],
 ["search/d972_r07_positive_common_word_colgen_v1.py","47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7",123870],
 ["search/d972_r07_all_seven_extension_section_census_v1.py","878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b",66109],
 ["search/d972_r07_full_e4_joint_orbit_preflight_v7.py","92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed",21918],
 ["crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py","e3917ec05b95b8996e3a5cec1cc2bfde51c3ed8c6972175fd9be9e1178205c23",12423],
 ["search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json","86c6f3a72a3f852a1be7c5323bf72c7ad987377fd5483b6e32528fe263e290ff",45246709],
 ["crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py","4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695",84980],
 ["sol/proof_r07_ten_occurrence_seven_block_action_bridge_v189.md","f3d2fdf9f1fec28c1f308fe7ee74e796cec465fd40dbd73f5e7dc478327da302",8814],
 ["sol/proof_r07_existing_6441_roof_presentation_v190.md","562a1ac9db7c1b0a460a5383deff5858de073704f648d524566bd7d18a05e5e1",9793],
 ["sol/proof_r07_compressed_diagonal_successor_relation_module_v188.md","6512e810011105f83f845e9a41f63ee51fe278371f2cee6cc241e8022a41e822",11314],
 ["sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md","b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3",8545],
 ["sol/proof_r07_task179_relative_frattini_successor_v145.md","b08f140838b78424cafa9528eafbcab9442f94cf92ce2cb42e15fc88ed489a51",13819],
 ["sol/proof_r07_recursive_relative_magnus_frattini_compiler_v168.md","0f491cf9a4a43ac165eb70c60d37142053bde47eac965b2497d1d6abaa370cb3",13829],
 ["sol/proof_r07_diagonal_context_cyclic_contraction_v173.md","7eed6ad7b00482e245e46226db3fb6985f59c6aa078d7705a92a793593f556f2",11471],
 ["sol/proof_r07_pointed_pair_obstruction_hensel_v184.md","7cabb1801b1a844f5f5d63267dda9a4a18e5eeec8a7ec296456e8e60501a88bd",11018],
 ["sol/luna_task_176_r07_all_seven_extension_section_census_v1.md","a1778c17c33e42880a6dd0c2480303a13702cb38950cf836a4ca9d8cca6fa332",7054],
 ["sol/luna_reply_176_r07_all_seven_extension_section_census_v1.md","aa173122310e33910d546bd3e02a98a6bf16aea9d3aad066b7d49976098ebb0c",47164],
 ["sol/luna_task_198_r07_seven_context_roof_presentation_v1.md","208bdac9fb5a1b257745d74f02878e1a3d033602fa20a5dc57a378a835a80dcc",11267],
 ["sol/luna_task_198b_r07_existing_6441_roof_presentation_repair.md","425b9dc64c0a19bac6af6992944fafbba4207ff5569f275fdbc08ee94441d2ae",4546]
];;
for D198PinRow in D198Pins do D198Pin(D198PinRow);; od;
for D198PinRow in D198Cone do D198Pin(D198PinRow);; od;
if D198Mode="PRODUCTION" then
  D198Pin([D198I,"715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41",13649089]);;
  D198Manifest:=D198Read(D198M,"task176 artifact manifest");;
  for D198ManifestNeedle in [
    "9635036013","250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912",
    "33044121344","0533e42019c9f67f6cec3d1566152db17b903836",
    "d972_r07_all_seven_extension_section_census_v1.json",
    "715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41",
    "13649089"] do
    if PositionSublist(D198Manifest,D198ManifestNeedle)=fail then
      Error("task198: task176 manifest field");
    fi;
  od;
fi;

D198ResumeArgs:="";;
if D198Mode="PRODUCTION" then
  if IsExistingFile(D198RI)<>IsExistingFile(D198RM) then
    Error("task198: staged resume checkpoint/manifest pair incomplete");
  fi;
  if IsExistingFile(D198RI) then
    D198ResumeRaw:=D198Read(D198RI,"staged resume checkpoint");;
    D198ResumeManifest:=D198Read(D198RM,"staged resume manifest");;
    for D198ResumeNeedle in [
      "d972-r07-seven-context-roof-presentation/v1/resume-manifest/v2",
      D198RI,HexSHA256(D198ResumeRaw),String(Length(D198ResumeRaw)),
      "checkpoint_seal_sha256","cursor","bridge_cursor",
      "self_digest_sha256"] do
      if PositionSublist(D198ResumeManifest,D198ResumeNeedle)=fail then
        Error("task198: staged resume manifest binding");
      fi;
    od;
    D198ResumeArgs:=Concatenation(" --resume ",D198RI,
      " --resume-manifest ",D198RM);;
  fi;
fi;

D198Reject([D198R,D198V,D198PL,D198CL,D198OK,D198T,D198K,D198KM,D198SPath,
 D198SR,D198SV,
 Concatenation(D198SP,".presentation.output.checkpoint.json"),
 Concatenation(D198SP,".presentation.output.manifest.json"),
 Concatenation(D198SP,".presentation.staged.checkpoint.json"),
 Concatenation(D198SP,".presentation.staged.manifest.json"),
 Concatenation(D198SP,".bridge.output.checkpoint.json"),
 Concatenation(D198SP,".bridge.output.manifest.json"),
 Concatenation(D198SP,".bridge.staged.checkpoint.json"),
 Concatenation(D198SP,".bridge.staged.manifest.json"),
 Concatenation(D198SP,".preflight-zero.output.checkpoint.json"),
 Concatenation(D198SP,".preflight-zero.output.manifest.json"),
 Concatenation(D198SP,".preflight-zero.staged.checkpoint.json"),
 Concatenation(D198SP,".preflight-four.output.checkpoint.json"),
 Concatenation(D198SP,".preflight-four.output.manifest.json"),
 Concatenation(D198SP,".preflight-four.staged.checkpoint.json")]);;
D198Fixture:=D198Read(D198F,"fixture");;
if D198Count(D198Fixture,"d972-r07-seven-context-roof-presentation-selftest-fixture/v4")<>1 or
   D198Count(D198Fixture,"\"mutation_count\": 44")<>1 then
  Error("task198: fixture schema/count");
fi;
if not IsDirectoryPath("ci/out") then
  if CreateDir("ci/out")=fail then Error("task198: cannot create ci/out"); fi;
fi;
if not IsDirectoryPath("ci/out") then Error("task198: ci/out is not a directory"); fi;
D198S:=OutputTextFile(D198SPath,false);;
if D198S=fail then Error("task198: cannot open generated shell after ci/out creation"); fi;
SetPrintFormattingStatus(D198S,false);;
PrintTo(D198S,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
PrintTo(D198S,"printf 'TASK198_RESOURCE_ESTIMATE wall_seconds=",D198EstimatedWallSeconds,
  " peak_rss_bytes=",D198EstimatedPeakRSSBytes," process_count=1\\n'\n");
if D198Mode="SELFTEST" then
  PrintTo(D198S,"python3 -u -B ",D198P," --selftest --fixture ",D198F,
    " --output ",D198SR," > ",D198PL," 2>&1 || { rc=$?; cat ",D198PL,"; exit $rc; }\n");
  PrintTo(D198S,"cat ",D198PL,"\n");
  PrintTo(D198S,"grep -Fxc 'R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_SELFTEST_PASS q0_order=6 gamma_order=2 D_order=12 presentation_rows=9 receipt=",D198SR,"' ",D198PL," | grep -qx 1\n");
  PrintTo(D198S,"python3 -u -B ",D198C," --selftest --fixture ",D198F,
    " --receipt ",D198SR," --verdict ",D198SV,
    " > ",D198CL," 2>&1 || { rc=$?; cat ",D198CL,"; exit $rc; }\n");
  PrintTo(D198S,"cat ",D198CL,"\n");
  PrintTo(D198S,"grep -Fxc 'R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_SELFTEST_PASS q0_order=6 gamma_order=2 D_order=12 presentation_rows=9 mutation_attempted=44 mutation_rejected=44' ",D198CL," | grep -qx 1\n");
  PrintTo(D198S,"test -s ",D198SR," -a -s ",D198SV,"\n");
  PrintTo(D198S,"printf 'SELFTEST\n' > ",D198T,"\n");
else
  PrintTo(D198S,"python3 -u -B ",D198P," --task176-receipt ",D198I," --output ",D198R," --checkpoint ",D198K," --checkpoint-manifest-output ",D198KM," --future-resume-checkpoint ",D198RI,D198ResumeArgs," --seconds ",D198EstimatedWallSeconds," --rss-bytes ",D198EstimatedPeakRSSBytes," --q0-states 1469664 --q0-edges 2939328 --presentation-rows 6441 --gamma-operations 5000000 --dag-nodes 10000000 --serialized-bytes 2000000000 --checkpoint-bytes 100000000 > ",D198PL," 2>&1 || { rc=$?; cat ",D198PL,"; exit $rc; }\n");
  PrintTo(D198S,"cat ",D198PL,"\n");
  PrintTo(D198S,"grep -Ec '^R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL (ROOF_BRIDGE_ISOMORPHISM|UNKNOWN_RESOURCE|UNKNOWN_INPUT)$' ",D198PL," | grep -qx 1\n");
  PrintTo(D198S,"python3 -u -B ",D198C," --receipt ",D198R," --verdict ",D198V," --task176-receipt ",D198I,D198ResumeArgs," --seconds ",D198EstimatedWallSeconds," --rss-bytes ",D198EstimatedPeakRSSBytes," --q0-states 1469664 --q0-edges 2939328 --presentation-rows 6441 --gamma-operations 10000000 --dag-nodes 10000000 --serialized-bytes 2000000000 --checkpoint-bytes 100000000 > ",D198CL," 2>&1 || { rc=$?; cat ",D198CL,"; exit $rc; }\n");
  PrintTo(D198S,"cat ",D198CL,"\n");
  PrintTo(D198S,"grep -Fxc 'R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441' ",D198CL," | grep -qx 1\n");
  PrintTo(D198S,"grep -Fxc 'R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM' ",D198PL," | grep -qx 1\n");
  PrintTo(D198S,"printf 'ROOF_BRIDGE_ISOMORPHISM\n' > ",D198T,"\n");
fi;
PrintTo(D198S,"printf 'R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_DRIVER_SENTINEL\n' > ",D198OK,"\n");
CloseStream(D198S);;
Exec("bash ci/out/d972_r07_seven_context_roof_presentation_command.sh");;
D198Sent:=D198Read(D198OK,"sentinel");;
if D198Sent<>"R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_DRIVER_SENTINEL\n" then
  Error("task198: bad sentinel");
fi;
D198Terminal:=D198Read(D198T,"terminal");;
if D198Mode="SELFTEST" and D198Terminal<>"SELFTEST\n" then
  Error("task198: selftest terminal");
fi;
if D198Mode="PRODUCTION" and D198Terminal<>"ROOF_BRIDGE_ISOMORPHISM\n" then
  Error("task198: nonpositive production terminal");
fi;
Print("R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_GHA_DRIVER_PASS mode=",
      D198Mode," terminal=",Chomp(D198Terminal),"\n");
