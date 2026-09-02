#############################################################################
## Task527 actual rank111 lazy K=0 successor driver v13. External preamble required.
#############################################################################
if not IsBound(D972_R07_A0_LAZY_K0_RANK111_RESUME_V13_RUN) or
   D972_R07_A0_LAZY_K0_RANK111_RESUME_V13_RUN<>true then
 Error("task527 external preamble required"); fi;
D527Producer:="search/d972_r07_a0_actual_tau_free_lazy_k0_seed_v5.py";;
D527Checker:="crosscheck/check_d972_r07_a0_actual_tau_free_lazy_k0_seed_v9.py";;
D527ReleaseURL:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9826862037_gap-run-out.a0-rank111.zip";;
D527Run:="33564845217";; D527Job:="100045550767";;
D527Head:="c582f8d786012a668783790007b72c5c422c3db8";;
D527APIArtifactID:="9826862037";; D527APIArtifactName:="gap-run-out";; D527APIArtifactSize:=96198;;
D527Zip:="ci/out/d972_r07_a0_actual_tau_free_lazy_k0_rank111_resume_v13.zip";;
D527Extract:="ci/out/d972_r07_a0_actual_tau_free_lazy_k0_rank111_resume_v13_archive";;
D527ResumeMember:="d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint";;
D527Input:="ci/out/d972_r07_a0_actual_tau_free_lazy_k0_rank111_resume_v13_input.checkpoint";;
D527Artifact:="ci/out/d972_r07_a0_actual_tau_free_lazy_k0_seed_v5.json";;
D527Checkpoint:="ci/out/d972_r07_a0_actual_tau_free_lazy_k0_seed_v5_output.checkpoint";;
D527PL:="ci/out/d972_r07_a0_actual_tau_free_lazy_k0_seed_v5_producer.log";;
D527CL:="ci/out/d972_r07_a0_actual_tau_free_lazy_k0_seed_v5_checker.log";;
D527DL:="ci/out/d972_r07_a0_actual_tau_free_lazy_k0_rank111_resume_v13_preflight.log";;
D527ZipBytes:=37586;;
D527ZipSHA:="8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de";;
D527ProducerBytes:=34773;;
D527ProducerSHA:="94e9079c36592414d394f816d0d1190822157c017afecd9e75c9e19f8c7aa5aa";;
D527CheckerBytes:=27570;;
D527CheckerSHA:="9b9bfbf72a312ed759861c854f1f5513342c037c2eb74b89bee8e09caa2f29c0";;
D527ResumeBytes:=85934;;
D527ResumeSHA:="69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93";;
D527MemberManifest:=[
 ["d972_r07_a0_actual_tau_free_rank98_resume_v10_input.checkpoint",69947,"c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f"],
 ["d972_r07_a0_actual_tau_free_rank98_resume_v10_preflight.log",38,"52f94358c40a2e6968927b4078a0bf00b6a40c32eb013367679e8d59b599240c"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10.json",86354,"39434b6a4c1a7851805c2deb3be8de4e7e919085a537b8d3913a15d341c19279"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10_checker.log",51,"aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint",85934,"69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10_producer.log",4905,"271d05e70153cbceadf9d45478a4357bcd7899610b3857b3525644205b7e975c"],
 ["driver.g",128,"393794cf2188ac0a27abe472180ddabca42e7f88082248726e4ae664cd371978"],
 ["run.log",5004,"ac7fcf963237cc23d88774df9c85d82cb8b3acc09f24b0ee4dda5506e719bf15"]
];;
D527Quote:=function(s)
 if PositionSublist(s,"'")<>fail or PositionSublist(s,"\n")<>fail or
    PositionSublist(s,"\r")<>fail then Error("task527 unsafe shell text"); fi;
 return Concatenation("'",s,"'");
end;;
if Length(D527MemberManifest)<>8 then Error("task527 eight-member manifest"); fi;
if D527Run<>"33564845217" or D527Job<>"100045550767" or
   D527Head<>"c582f8d786012a668783790007b72c5c422c3db8" or
   D527APIArtifactID<>"9826862037" or D527APIArtifactName<>"gap-run-out" or
   D527APIArtifactSize<>96198 or
   D527ReleaseURL<>"https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9826862037_gap-run-out.a0-rank111.zip" or
   D527ZipBytes<>37586 or D527ZipSHA<>"8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de" then
 Error("task527 immutable source binding drift"); fi;
if IsExistingFile(D527Zip) or IsDirectoryPath(D527Extract) or
   IsExistingFile(D527Input) or IsExistingFile(D527Artifact) or
   IsExistingFile(D527Checkpoint) or IsExistingFile(D527PL) or
   IsExistingFile(D527CL) or IsExistingFile(D527DL) then
 Error("task527 stale output"); fi;
if not IsDirectoryPath("ci/out") then
 if CreateDir("ci/out")=fail then Error("task527 ci/out"); fi; fi;
D527Cmd:=Concatenation(
 "set -euo pipefail; umask 077; ",
 "test ! -e \"",D527DL,"\"; test ! -L \"",D527DL,"\"; ",
 "exec 9>\"",D527DL,"\"; ",
 "printf \"TASK527_R07_A0_LAZY_K0_RANK111_PREFLIGHT_BEGIN\\n\" >&9; ",
 "task527_preflight_fail() { rc=$?; printf \"TASK527_R07_A0_LAZY_K0_RANK111_PREFLIGHT_FAIL rc=%s cmd=%s\\n\" \"$rc\" \"$BASH_COMMAND\" >&9; return \"$rc\"; }; ",
 "trap task527_preflight_fail ERR; ",
 "command -v curl >/dev/null; command -v unzip >/dev/null; command -v sha256sum >/dev/null; ",
 "command -v timeout >/dev/null; command -v tee >/dev/null; command -v grep >/dev/null; ",
 "test ! -e \"",D527Zip,"\"; test ! -L \"",D527Zip,"\"; ",
 "test ! -e \"",D527Extract,"\"; test ! -L \"",D527Extract,"\"; ",
 "test ! -e \"",D527Input,"\"; test ! -L \"",D527Input,"\"; ",
 "test ! -e \"",D527Artifact,"\"; test ! -L \"",D527Artifact,"\"; ",
 "test ! -e \"",D527Checkpoint,"\"; test ! -L \"",D527Checkpoint,"\"; ",
 "test ! -e \"",D527PL,"\"; test ! -L \"",D527PL,"\"; ",
 "test ! -e \"",D527CL,"\"; test ! -L \"",D527CL,"\"; ",
 "test -f \"",D527Producer,"\"; test ! -L \"",D527Producer,"\"; ",
 "test \"$(wc -c < \"",D527Producer,"\" | tr -d \"[:space:]\")\" = \"",String(D527ProducerBytes),"\"; ",
 "test \"$(sha256sum \"",D527Producer,"\" | cut -d \" \" -f1)\" = \"",D527ProducerSHA,"\"; ",
 "test -f \"",D527Checker,"\"; test ! -L \"",D527Checker,"\"; ",
 "test \"$(wc -c < \"",D527Checker,"\" | tr -d \"[:space:]\")\" = \"",String(D527CheckerBytes),"\"; ",
 "test \"$(sha256sum \"",D527Checker,"\" | cut -d \" \" -f1)\" = \"",D527CheckerSHA,"\"; ",
 "curl --fail --location --silent --show-error \"",D527ReleaseURL,"\" --output \"",D527Zip,"\"; ",
 "test \"$(wc -c < \"",D527Zip,"\" | tr -d \"[:space:]\")\" = \"",String(D527ZipBytes),"\"; ",
 "test \"$(sha256sum \"",D527Zip,"\" | cut -d \" \" -f1)\" = \"",D527ZipSHA,"\"; ",
 "mkdir \"",D527Extract,"\"; unzip -q \"",D527Zip,"\" -d \"",D527Extract,"\"; ",
 "test \"$(unzip -Z1 \"",D527Zip,"\" | wc -l | tr -d \"[:space:]\")\" = \"8\"; ");
for D527Row in D527MemberManifest do
 D527Path:=Concatenation(D527Extract,"/",D527Row[1]);
 D527Cmd:=Concatenation(D527Cmd,
  "test -f \"",D527Path,"\"; test \"$(wc -c < \"",D527Path,
  "\" | tr -d \"[:space:]\")\" = \"",String(D527Row[2]),"\"; ",
  "test \"$(sha256sum \"",D527Path,"\" | cut -d \" \" -f1)\" = \"",D527Row[3],"\"; ");
od;
D527ResumePath:=Concatenation(D527Extract,"/",D527ResumeMember);
D527Cmd:=Concatenation(D527Cmd,
 "cp \"",D527ResumePath,"\" \"",D527Input,"\"; ",
 "test \"$(wc -c < \"",D527Input,"\" | tr -d \"[:space:]\")\" = \"",String(D527ResumeBytes),"\"; ",
 "test \"$(sha256sum \"",D527Input,"\" | cut -d \" \" -f1)\" = \"",D527ResumeSHA,"\"; ",
 "ulimit -v 5200000; ",
 "timeout --foreground --signal=TERM --kill-after=60s 7500s python3 -u -B ",D527Producer,
 " --mode PRODUCTION --resume \"",D527Input,
 "\" --seconds 7200 --rss-bytes 4800000000 --max-rises 64 --output \"",D527Artifact,
 "\" --checkpoint \"",D527Checkpoint,"\" 2>&1 | tee \"",D527PL,"\"; ",
 "test -s \"",D527Artifact,"\"; test -s \"",D527Checkpoint,"\"; ",
 "test \"$(grep -Ec \"^R07_A0_ACTUAL_TAU_FREE_LAZY_K0_SEED_V5 status=(UNKNOWN_RESOURCE|UNKNOWN|COMMON_CANDIDATE)$\" \"",D527PL,"\")\" = \"1\"; ",
 "timeout --foreground --signal=TERM --kill-after=60s 3600s python3 -u -B ",D527Checker,
 " \"",D527Artifact,"\" 2>&1 | tee \"",D527CL,"\"; ",
 "test \"$(grep -Fc \"R07_A0_ACTUAL_TAU_FREE_LAZY_K0_SEED_V9_CHECKER_PASS\" \"",D527CL,"\")\" = \"1\"; ",
 "test \"$(wc -l < \"",D527CL,"\" | tr -d \"[:space:]\")\" = \"1\"; ");
Exec(Concatenation("bash -o pipefail -c ",D527Quote(D527Cmd)));
if not IsExistingFile(D527DL) or Length(StringFile(D527DL))=0 then
 Error("task527 preflight diagnostic missing"); fi;
if not IsExistingFile(D527Artifact) or not IsExistingFile(D527Checkpoint) or
   not IsExistingFile(D527CL) then Error("task527 result/checker missing"); fi;
if Length(StringFile(D527Artifact))=0 or Length(StringFile(D527Checkpoint))=0 then
 Error("task527 result/checkpoint empty"); fi;
if PositionSublist(StringFile(D527PL),"R07_A0_ACTUAL_TAU_FREE_LAZY_K0_SEED_V5 status=")=fail then
 Error("task527 producer marker"); fi;
if StringFile(D527CL)<>"R07_A0_ACTUAL_TAU_FREE_LAZY_K0_SEED_V9_CHECKER_PASS\n" then
 Error("task527 checker marker"); fi;
Print("R07_A0_LAZY_K0_RANK111_RESUME_V13_DRIVER_PASS\n");
