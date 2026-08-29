#############################################################################
## R07 pre-A0 single-target actual A3 v1.
## Serial fail-closed GAP driver; no workflow edits and no local receipt.
#############################################################################
D359ModeVariable:="D972_R07_PRE_A0_SINGLE_TARGET_A3_MODE";;
if not IsBound(D972_R07_PRE_A0_SINGLE_TARGET_A3_MODE) then
  Error("task359: supply quoted mode"); fi;
D359Mode:=D972_R07_PRE_A0_SINGLE_TARGET_A3_MODE;;
if not IsString(D359Mode) or not D359Mode in ["PRODUCTION"] then
  Error("task359: mode must be PRODUCTION"); fi;
D359P0:="ci/in/d972_r07_pre_a0_single_target_a3_v1.prereg.v1.json";;
D359P:="search/d972_r07_pre_a0_single_target_a3_v1.py";;
D359C:="crosscheck/check_d972_r07_pre_a0_single_target_a3_v1.py";;
D359R:="ci/out/d972_r07_pre_a0_single_target_a3_v1.json";;
D359V:="ci/out/d972_r07_pre_a0_single_target_a3_v1.verdict.json";;
D359PL:="ci/out/d972_r07_pre_a0_single_target_a3_v1.producer.log";;
D359CL:="ci/out/d972_r07_pre_a0_single_target_a3_v1.checker.log";;
D359S:="ci/out/d972_r07_pre_a0_single_target_a3_v1.sh";;
D359OK:="ci/out/d972_r07_pre_a0_single_target_a3_v1.ok";;
D359Sentinel:="R07_PRE_A0_SINGLE_TARGET_A3_DRIVER_SENTINEL";;
D359ProducerMember:="R07_PRE_A0_A3_PROJECTED_MEMBER";;
D359ProducerDual:="R07_PRE_A0_A3_PROJECTED_NONMEMBER_DUAL";;
D359UnknownInput:="UNKNOWN_INPUT";;
D359UnknownResource:="UNKNOWN_RESOURCE";;
D359P0Bytes:=6691;;
D359P0SHA:="f8092796af77da3ea137908b1cca48db6563c412d937147bc341be29cc49489";;
D359Pins:=[
  [D359P0,D359P0SHA,D359P0Bytes],
  [D359P,"de69138d64a0324b45cd8327cb1425df88dcf54525c32d6127f0dbac251e94d6",45897],
  [D359C,"ba087b0e37fa15a7ff8dbb1a1d65509e0a3721b4d1b4a0f07789c40c3411ad7d",46751],
  ["ci/in/d972_r07_seven_context_roof_presentation_v1.json","82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5",31017244],
  ["ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json","cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4",2722],
  ["ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt","b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090",81],
  ["ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt","260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e",95],
  ["ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json","ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de",150],
  ["search/d972_r07_seven_context_roof_presentation_v1.py","6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c",137169],
  ["crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py","001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1",157253],
  ["search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g","6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068",20541],
  ["search/d972_r07_actual_two_word_endpoint_specializer_v2.py","a1532740a7343bd8166c17947f6bd95203a4abdaaafd8e0d9607d3cdf202e6fb",40556],
  ["crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py","e49e4ee24b56e35f8c8120bad7579865e497d94f57b2af51664d562f50ffaa44",35463],
  ["search/d972_r07_typed_single_seed_endpoint_consumer_v2.py","755ba97e55266bcdb51796cc1a89a562efa782db48475d0e3479e82e325cde8e",47135],
  ["crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py","028e615bd71276c22cea2180b8ff59e53d8e9ee745c84a1912c862f217f2bb95",34200],
  ["search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g","38352fd53e2aa2534e6b4d61c5a613c38fd65c4a6843fa5cb6dd2a04918cfe7d",5387],
  ["search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py","f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f",33409],
  ["search/d972_r07_760_l3_target6_v1.py","7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde",53284],
  ["sol/proof_r07_a18_area_invisibility_single_a3_target_v302.md","ba508bbe96f34967ebe456c51285ecbe774861a864c369699bbf1dce2b9fc6c3",7340],
  ["sol/proof_r07_pre_a0_computational_base_equivalence_v303.md","9868aa26d630138da9b8b963b0f3968e8c2ee698ba4461d596a2b6f155d25cf2",6739]
];;
D359Read:=function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task359: missing ",label); fi;
  return raw;
end;;
D359Pin:=function(row)
  local raw;
  raw:=D359Read(row[1],"pinned owner");;
  if Length(raw)<>row[3] or HexSHA256(raw)<>row[2] then
    Error("task359: pin drift ",row[1]); fi;
end;;
for D359PinRow in D359Pins do D359Pin(D359PinRow);; od;
for D359Path in [D359R,D359V,D359PL,D359CL,D359S,D359OK] do
  if IsExistingFile(D359Path) then Error("task359: stale output ",D359Path); fi;
od;
if not IsDirectoryPath("ci/out") then
  if CreateDir("ci/out")=fail then Error("task359: cannot create ci/out"); fi;
fi;
if not IsDirectoryPath("ci/out") then Error("task359: ci/out is not a directory"); fi;
D359Stream:=OutputTextFile(D359S,false);;
if D359Stream=fail then Error("task359: cannot open command script"); fi;
SetPrintFormattingStatus(D359Stream,false);
PrintTo(D359Stream,"set -euo pipefail\n");
PrintTo(D359Stream,"printf 'D359_GHA_ESTIMATE producer_wall_seconds=21600 checker_wall_seconds=21600 serial_wall_seconds=43200 rss_bytes=6442450944 output_bytes=2000000000\\n'\n");
PrintTo(D359Stream,"timeout 21600s python -u -B ",D359P," --output ",D359R,
  " > ",D359PL," 2>&1 || { cat ",D359PL,"; exit 1; }\n");
PrintTo(D359Stream,"grep -Ec '^D359_PRODUCER_TERMINAL (",D359ProducerMember,
  "|",D359ProducerDual,"|",D359UnknownInput,"|",D359UnknownResource,
  ")$' ",D359PL," | grep -qx 1 || { cat ",D359PL,"; exit 1; }\n");
PrintTo(D359Stream,"test -s ",D359R," || { cat ",D359PL,"; exit 1; }\n");
PrintTo(D359Stream,"timeout 21600s python -u -B ",D359C," ",D359R,
  " --verdict ",D359V," > ",D359CL," 2>&1 || { cat ",D359CL,"; exit 1; }\n");
PrintTo(D359Stream,"grep -Ec '^D359_CHECKER_TERMINAL (",D359ProducerMember,
  "|",D359ProducerDual,"|",D359UnknownInput,"|",D359UnknownResource,
  ")$' ",D359CL," | grep -qx 1 || { cat ",D359CL,"; exit 1; }\n");
PrintTo(D359Stream,"test -s ",D359V," || { cat ",D359CL,"; exit 1; }\n");
PrintTo(D359Stream,"rsha=$(sha256sum ",D359R," | awk '{print $1}')\n");
PrintTo(D359Stream,"grep -Fq -- '\"receipt_sha256\":\"'${rsha}'\"' ",D359V,
  " || { cat ",D359PL,"; cat ",D359CL,"; exit 1; }\n");
PrintTo(D359Stream,"p=$(sed -n 's/^D359_PRODUCER_TERMINAL //p' ",D359PL," | head -n 1)\n");
PrintTo(D359Stream,"c=$(sed -n 's/^D359_CHECKER_TERMINAL //p' ",D359CL," | head -n 1)\n");
PrintTo(D359Stream,"test \"$p\" = \"$c\" || { cat ",D359PL,"; cat ",D359CL,"; exit 1; }\n");
PrintTo(D359Stream,"grep -Fq '\"receipt_sha256\"' ",D359V," || { cat ",D359CL,"; exit 1; }\n");
PrintTo(D359Stream,"printf '%s' '",D359Sentinel,"_',D359Mode,"' > ",D359OK,"\n");
CloseStream(D359Stream);;
Exec(Concatenation("bash ",D359S));
if StringFile(D359OK)<>Concatenation(D359Sentinel,"_",D359Mode) then
  Error("task359: explicit sentinel"); fi;
Print("D359_DRIVER_PASS mode=",D359Mode,"\n");
