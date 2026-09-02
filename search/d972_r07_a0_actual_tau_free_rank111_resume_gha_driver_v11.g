#############################################################################
## Task521 rank-111 continuation runtime-envelope driver v11. External preamble required.
## The producer/checker and all computation semantics remain frozen from v9.
#############################################################################
if not IsBound(D972_R07_A0_RANK111_CHECKPOINT_RESUME_V11_RUN) or
   D972_R07_A0_RANK111_CHECKPOINT_RESUME_V11_RUN<>true then
 Error("task521 external preamble required"); fi;
D521Producer:="search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py";;
D521Checker:="crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py";;
D521ReleaseURL:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9826862037_gap-run-out.a0-rank111.zip";;
D521Run:="33564845217";; D521Job:="100045550767";;
D521Head:="c582f8d786012a668783790007b72c5c422c3db8";;
D521APIArtifactID:="9826862037";; D521APIArtifactName:="gap-run-out";; D521APIArtifactSize:=96198;;
D521Zip:="ci/out/d972_r07_a0_actual_tau_free_rank111_resume_v11.zip";;
D521Extract:="ci/out/d972_r07_a0_actual_tau_free_rank111_resume_v11_archive";;
D521ResumeMember:="d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint";;
D521Input:="ci/out/d972_r07_a0_actual_tau_free_rank111_resume_v11_input.checkpoint";;
D521Artifact:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v11.json";;
D521Checkpoint:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v11_output.checkpoint";;
D521PL:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v11_producer.log";;
D521CL:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v11_checker.log";;
D521DL:="ci/out/d972_r07_a0_actual_tau_free_rank111_resume_v11_preflight.log";;
D521ZipBytes:=37586;;
D521ZipSHA:="8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de";;
D521ProducerBytes:=12215;;
D521ProducerSHA:="0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37";;
D521CheckerBytes:=3653;;
D521CheckerSHA:="e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1";;
D521ResumeBytes:=85934;;
D521ResumeSHA:="69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93";;
D521MemberManifest:=[
 ["d972_r07_a0_actual_tau_free_rank98_resume_v10_input.checkpoint",69947,"c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f"],
 ["d972_r07_a0_actual_tau_free_rank98_resume_v10_preflight.log",38,"52f94358c40a2e6968927b4078a0bf00b6a40c32eb013367679e8d59b599240c"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10.json",86354,"39434b6a4c1a7851805c2deb3be8de4e7e919085a537b8d3913a15d341c19279"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10_checker.log",51,"aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint",85934,"69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10_producer.log",4905,"271d05e70153cbceadf9d45478a4357bcd7899610b3857b3525644205b7e975c"],
 ["driver.g",128,"393794cf2188ac0a27abe472180ddabca42e7f88082248726e4ae664cd371978"],
 ["run.log",5004,"ac7fcf963237cc23d88774df9c85d82cb8b3acc09f24b0ee4dda5506e719bf15"]
];;
D521Quote:=function(s)
 if PositionSublist(s,"'")<>fail or PositionSublist(s,"\n")<>fail or
    PositionSublist(s,"\r")<>fail then Error("task521 unsafe shell text"); fi;
 return Concatenation("'",s,"'");
end;;
if Length(D521MemberManifest)<>8 then Error("task521 eight-member manifest"); fi;
if D521Run<>"33564845217" or D521Job<>"100045550767" or
   D521Head<>"c582f8d786012a668783790007b72c5c422c3db8" or
   D521APIArtifactID<>"9826862037" or D521APIArtifactName<>"gap-run-out" or
   D521APIArtifactSize<>96198 or
   D521ReleaseURL<>"https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9826862037_gap-run-out.a0-rank111.zip" or
   D521ZipBytes<>37586 or D521ZipSHA<>"8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de" then
 Error("task521 immutable source binding drift"); fi;
if IsExistingFile(D521Zip) or IsDirectoryPath(D521Extract) or
   IsExistingFile(D521Input) or IsExistingFile(D521Artifact) or
   IsExistingFile(D521Checkpoint) or IsExistingFile(D521PL) or
   IsExistingFile(D521CL) or IsExistingFile(D521DL) then
 Error("task521 stale output"); fi;
if not IsDirectoryPath("ci/out") then
 if CreateDir("ci/out")=fail then Error("task521 ci/out"); fi; fi;
D521Cmd:=Concatenation(
 "set -euo pipefail; umask 077; ",
 "test ! -e \"",D521DL,"\"; test ! -L \"",D521DL,"\"; ",
 "exec 9>\"",D521DL,"\"; ",
 "printf \"TASK521_R07_A0_RANK111_PREFLIGHT_BEGIN\\n\" >&9; ",
 "task521_preflight_fail() { rc=$?; printf \"TASK521_R07_A0_RANK111_PREFLIGHT_FAIL rc=%s cmd=%s\\n\" \"$rc\" \"$BASH_COMMAND\" >&9; return \"$rc\"; }; ",
 "trap task521_preflight_fail ERR; ",
 "command -v curl >/dev/null; command -v unzip >/dev/null; command -v sha256sum >/dev/null; ",
 "command -v timeout >/dev/null; command -v tee >/dev/null; command -v grep >/dev/null; ",
 "test ! -e \"",D521Zip,"\"; test ! -L \"",D521Zip,"\"; ",
 "test ! -e \"",D521Extract,"\"; test ! -L \"",D521Extract,"\"; ",
 "test ! -e \"",D521Input,"\"; test ! -L \"",D521Input,"\"; ",
 "test ! -e \"",D521Artifact,"\"; test ! -L \"",D521Artifact,"\"; ",
 "test ! -e \"",D521Checkpoint,"\"; test ! -L \"",D521Checkpoint,"\"; ",
 "test ! -e \"",D521PL,"\"; test ! -L \"",D521PL,"\"; ",
 "test ! -e \"",D521CL,"\"; test ! -L \"",D521CL,"\"; ",
 "test -f \"",D521Producer,"\"; test ! -L \"",D521Producer,"\"; ",
 "test \"$(wc -c < \"",D521Producer,"\" | tr -d \"[:space:]\")\" = \"",String(D521ProducerBytes),"\"; ",
 "test \"$(sha256sum \"",D521Producer,"\" | cut -d \" \" -f1)\" = \"",D521ProducerSHA,"\"; ",
 "test -f \"",D521Checker,"\"; test ! -L \"",D521Checker,"\"; ",
 "test \"$(wc -c < \"",D521Checker,"\" | tr -d \"[:space:]\")\" = \"",String(D521CheckerBytes),"\"; ",
 "test \"$(sha256sum \"",D521Checker,"\" | cut -d \" \" -f1)\" = \"",D521CheckerSHA,"\"; ",
 "curl --fail --location --silent --show-error \"",D521ReleaseURL,"\" --output \"",D521Zip,"\"; ",
 "test \"$(wc -c < \"",D521Zip,"\" | tr -d \"[:space:]\")\" = \"",String(D521ZipBytes),"\"; ",
 "test \"$(sha256sum \"",D521Zip,"\" | cut -d \" \" -f1)\" = \"",D521ZipSHA,"\"; ",
 "mkdir \"",D521Extract,"\"; unzip -q \"",D521Zip,"\" -d \"",D521Extract,"\"; ",
 "test \"$(unzip -Z1 \"",D521Zip,"\" | wc -l | tr -d \"[:space:]\")\" = \"8\"; ");
for D521Row in D521MemberManifest do
 D521Path:=Concatenation(D521Extract,"/",D521Row[1]);
 D521Cmd:=Concatenation(D521Cmd,
  "test -f \"",D521Path,"\"; test \"$(wc -c < \"",D521Path,
  "\" | tr -d \"[:space:]\")\" = \"",String(D521Row[2]),"\"; ",
  "test \"$(sha256sum \"",D521Path,"\" | cut -d \" \" -f1)\" = \"",D521Row[3],"\"; ");
od;
D521ResumePath:=Concatenation(D521Extract,"/",D521ResumeMember);
D521Cmd:=Concatenation(D521Cmd,
 "cp \"",D521ResumePath,"\" \"",D521Input,"\"; ",
 "test \"$(wc -c < \"",D521Input,"\" | tr -d \"[:space:]\")\" = \"",String(D521ResumeBytes),"\"; ",
 "test \"$(sha256sum \"",D521Input,"\" | cut -d \" \" -f1)\" = \"",D521ResumeSHA,"\"; ",
 "ulimit -v 5200000; ",
 "timeout --foreground --signal=TERM --kill-after=60s 7500s python3 -u -B ",D521Producer,
 " --mode PRODUCTION --resume \"",D521Input,
 "\" --seconds 7200 --rss-bytes 4800000000 --max-rises 64 --output \"",D521Artifact,
 "\" --checkpoint \"",D521Checkpoint,"\" 2>&1 | tee \"",D521PL,"\"; ",
 "test -s \"",D521Artifact,"\"; test -s \"",D521Checkpoint,"\"; ",
 "test \"$(grep -Ec \"^R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V3 status=[A-Z_]+$\" \"",D521PL,"\")\" = \"1\"; ",
 "timeout --foreground --signal=TERM --kill-after=60s 3600s python3 -u -B ",D521Checker,
 " \"",D521Artifact,"\" 2>&1 | tee \"",D521CL,"\"; ",
 "test \"$(grep -Fc \"R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V7_CHECKER_PASS\" \"",D521CL,"\")\" = \"1\"; ",
 "test \"$(wc -l < \"",D521CL,"\" | tr -d \"[:space:]\")\" = \"1\"; ");
Exec(Concatenation("bash -o pipefail -c ",D521Quote(D521Cmd)));
if not IsExistingFile(D521DL) or Length(StringFile(D521DL))=0 then
 Error("task521 preflight diagnostic missing"); fi;
if not IsExistingFile(D521Artifact) or not IsExistingFile(D521Checkpoint) or
   not IsExistingFile(D521CL) then Error("task521 result/checker missing"); fi;
if Length(StringFile(D521Artifact))=0 or Length(StringFile(D521Checkpoint))=0 then
 Error("task521 result/checkpoint empty"); fi;
if PositionSublist(StringFile(D521PL),"R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V3 status=")=fail then
 Error("task521 producer marker"); fi;
if StringFile(D521CL)<>"R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V7_CHECKER_PASS\n" then
 Error("task521 checker marker"); fi;
Print("R07_A0_RANK111_CHECKPOINT_RESUME_V11_DRIVER_PASS\n");
