#############################################################################
## Task504 rank-98 continuation runtime-envelope driver v10. External preamble required.
## The producer/checker and all computation semantics remain frozen from v9.
#############################################################################
if not IsBound(D972_R07_A0_RANK98_CHECKPOINT_RESUME_V10_RUN) or
   D972_R07_A0_RANK98_CHECKPOINT_RESUME_V10_RUN<>true then
 Error("task504 external preamble required"); fi;
D504Producer:="search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py";;
D504Checker:="crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py";;
D504ReleaseURL:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9821857621_gap-run-out.a0-rank98.zip";;
D504Run:="33548094849";; D504Job:="99990508106";;
D504Head:="3d5cac391076553fe68a83343376194dbd9efb6d";;
D504APIArtifactID:="9821857621";; D504APIArtifactName:="gap-run-out";; D504APIArtifactSize:=74814;;
D504Zip:="ci/out/d972_r07_a0_actual_tau_free_rank98_resume_v10.zip";;
D504Extract:="ci/out/d972_r07_a0_actual_tau_free_rank98_resume_v10_archive";;
D504ResumeMember:="d972_r07_a0_actual_tau_free_rank_ladder_v9_output.checkpoint";;
D504Input:="ci/out/d972_r07_a0_actual_tau_free_rank98_resume_v10_input.checkpoint";;
D504Artifact:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v10.json";;
D504Checkpoint:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint";;
D504PL:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v10_producer.log";;
D504CL:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v10_checker.log";;
D504DL:="ci/out/d972_r07_a0_actual_tau_free_rank98_resume_v10_preflight.log";;
D504ZipBytes:=30758;;
D504ZipSHA:="d0293cdd3bab98b792af17064ace21594966a5610e30219842347466e9ade9e4";;
D504ProducerBytes:=12215;;
D504ProducerSHA:="0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37";;
D504CheckerBytes:=3653;;
D504CheckerSHA:="e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1";;
D504ResumeBytes:=69947;;
D504ResumeSHA:="c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f";;
D504MemberManifest:=[
 ["d972_r07_a0_actual_tau_free_rank84_resume_v9_input.checkpoint",52707,"eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24f"],
 ["d972_r07_a0_actual_tau_free_rank84_resume_v9_preflight.log",35,"4d3dd0892debc756d57c12ab585ff63d473aad334bf25339c3fe3af6cef79139"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v9.json",70365,"2bbe05d8c5c2b97177854e7cd77944e9b89af70cea7f50e7565a6faec3a70b1d"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v9_checker.log",51,"aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v9_output.checkpoint",69947,"c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v9_producer.log",4989,"d585eec9c9b2f81a5689749ddc9fbe9d9e5e658651907ae95baf41d8827082fa"],
 ["driver.g",126,"ee8f36e711d719244b40b283f8d9debcdfd553b4ca0bee8dedcade6cd6ac8081"],
 ["run.log",5087,"d2c1cc146af7b1af3eddfbd213b29ee2b75e8b8030a77dcff2747dbb9ff2dc7c"]
];;
D504Quote:=function(s)
 if PositionSublist(s,"'")<>fail or PositionSublist(s,"\n")<>fail or
    PositionSublist(s,"\r")<>fail then Error("task504 unsafe shell text"); fi;
 return Concatenation("'",s,"'");
end;;
if Length(D504MemberManifest)<>8 then Error("task504 eight-member manifest"); fi;
if D504Run<>"33548094849" or D504Job<>"99990508106" or
   D504Head<>"3d5cac391076553fe68a83343376194dbd9efb6d" or
   D504APIArtifactID<>"9821857621" or D504APIArtifactName<>"gap-run-out" or
   D504APIArtifactSize<>74814 or
   D504ReleaseURL<>"https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9821857621_gap-run-out.a0-rank98.zip" or
   D504ZipBytes<>30758 or D504ZipSHA<>"d0293cdd3bab98b792af17064ace21594966a5610e30219842347466e9ade9e4" then
 Error("task504 immutable source binding drift"); fi;
if IsExistingFile(D504Zip) or IsDirectoryPath(D504Extract) or
   IsExistingFile(D504Input) or IsExistingFile(D504Artifact) or
   IsExistingFile(D504Checkpoint) or IsExistingFile(D504PL) or
   IsExistingFile(D504CL) or IsExistingFile(D504DL) then
 Error("task504 stale output"); fi;
if not IsDirectoryPath("ci/out") then
 if CreateDir("ci/out")=fail then Error("task504 ci/out"); fi; fi;
D504Cmd:=Concatenation(
 "set -euo pipefail; umask 077; ",
 "test ! -e \"",D504DL,"\"; test ! -L \"",D504DL,"\"; ",
 "exec 9>\"",D504DL,"\"; ",
 "printf \"TASK504_R07_A0_RANK98_PREFLIGHT_BEGIN\\n\" >&9; ",
 "task504_preflight_fail() { rc=$?; printf \"TASK504_R07_A0_RANK98_PREFLIGHT_FAIL rc=%s cmd=%s\\n\" \"$rc\" \"$BASH_COMMAND\" >&9; return \"$rc\"; }; ",
 "trap task504_preflight_fail ERR; ",
 "command -v curl >/dev/null; command -v unzip >/dev/null; command -v sha256sum >/dev/null; ",
 "command -v timeout >/dev/null; command -v tee >/dev/null; command -v grep >/dev/null; ",
 "test ! -e \"",D504Zip,"\"; test ! -L \"",D504Zip,"\"; ",
 "test ! -e \"",D504Extract,"\"; test ! -L \"",D504Extract,"\"; ",
 "test ! -e \"",D504Input,"\"; test ! -L \"",D504Input,"\"; ",
 "test ! -e \"",D504Artifact,"\"; test ! -L \"",D504Artifact,"\"; ",
 "test ! -e \"",D504Checkpoint,"\"; test ! -L \"",D504Checkpoint,"\"; ",
 "test ! -e \"",D504PL,"\"; test ! -L \"",D504PL,"\"; ",
 "test ! -e \"",D504CL,"\"; test ! -L \"",D504CL,"\"; ",
 "test -f \"",D504Producer,"\"; test ! -L \"",D504Producer,"\"; ",
 "test \"$(wc -c < \"",D504Producer,"\" | tr -d \"[:space:]\")\" = \"",String(D504ProducerBytes),"\"; ",
 "test \"$(sha256sum \"",D504Producer,"\" | cut -d \" \" -f1)\" = \"",D504ProducerSHA,"\"; ",
 "test -f \"",D504Checker,"\"; test ! -L \"",D504Checker,"\"; ",
 "test \"$(wc -c < \"",D504Checker,"\" | tr -d \"[:space:]\")\" = \"",String(D504CheckerBytes),"\"; ",
 "test \"$(sha256sum \"",D504Checker,"\" | cut -d \" \" -f1)\" = \"",D504CheckerSHA,"\"; ",
 "curl --fail --location --silent --show-error \"",D504ReleaseURL,"\" --output \"",D504Zip,"\"; ",
 "test \"$(wc -c < \"",D504Zip,"\" | tr -d \"[:space:]\")\" = \"",String(D504ZipBytes),"\"; ",
 "test \"$(sha256sum \"",D504Zip,"\" | cut -d \" \" -f1)\" = \"",D504ZipSHA,"\"; ",
 "mkdir \"",D504Extract,"\"; unzip -q \"",D504Zip,"\" -d \"",D504Extract,"\"; ",
 "test \"$(unzip -Z1 \"",D504Zip,"\" | wc -l | tr -d \"[:space:]\")\" = \"8\"; ");
for D504Row in D504MemberManifest do
 D504Path:=Concatenation(D504Extract,"/",D504Row[1]);
 D504Cmd:=Concatenation(D504Cmd,
  "test -f \"",D504Path,"\"; test \"$(wc -c < \"",D504Path,
  "\" | tr -d \"[:space:]\")\" = \"",String(D504Row[2]),"\"; ",
  "test \"$(sha256sum \"",D504Path,"\" | cut -d \" \" -f1)\" = \"",D504Row[3],"\"; ");
od;
D504ResumePath:=Concatenation(D504Extract,"/",D504ResumeMember);
D504Cmd:=Concatenation(D504Cmd,
 "cp \"",D504ResumePath,"\" \"",D504Input,"\"; ",
 "test \"$(wc -c < \"",D504Input,"\" | tr -d \"[:space:]\")\" = \"",String(D504ResumeBytes),"\"; ",
 "test \"$(sha256sum \"",D504Input,"\" | cut -d \" \" -f1)\" = \"",D504ResumeSHA,"\"; ",
 "ulimit -v 5200000; ",
 "timeout --foreground --signal=TERM --kill-after=60s 7500s python3 -u -B ",D504Producer,
 " --mode PRODUCTION --resume \"",D504Input,
 "\" --seconds 7200 --rss-bytes 4800000000 --max-rises 64 --output \"",D504Artifact,
 "\" --checkpoint \"",D504Checkpoint,"\" 2>&1 | tee \"",D504PL,"\"; ",
 "test -s \"",D504Artifact,"\"; test -s \"",D504Checkpoint,"\"; ",
 "test \"$(grep -Ec \"^R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V3 status=[A-Z_]+$\" \"",D504PL,"\")\" = \"1\"; ",
 "timeout --foreground --signal=TERM --kill-after=60s 3600s python3 -u -B ",D504Checker,
 " \"",D504Artifact,"\" 2>&1 | tee \"",D504CL,"\"; ",
 "test \"$(grep -Fc \"R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V7_CHECKER_PASS\" \"",D504CL,"\")\" = \"1\"; ",
 "test \"$(wc -l < \"",D504CL,"\" | tr -d \"[:space:]\")\" = \"1\"; ");
Exec(Concatenation("bash -o pipefail -c ",D504Quote(D504Cmd)));
if not IsExistingFile(D504DL) or Length(StringFile(D504DL))=0 then
 Error("task504 preflight diagnostic missing"); fi;
if not IsExistingFile(D504Artifact) or not IsExistingFile(D504Checkpoint) or
   not IsExistingFile(D504CL) then Error("task504 result/checker missing"); fi;
if Length(StringFile(D504Artifact))=0 or Length(StringFile(D504Checkpoint))=0 then
 Error("task504 result/checkpoint empty"); fi;
if PositionSublist(StringFile(D504PL),"R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V3 status=")=fail then
 Error("task504 producer marker"); fi;
if StringFile(D504CL)<>"R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V7_CHECKER_PASS\n" then
 Error("task504 checker marker"); fi;
Print("R07_A0_RANK98_CHECKPOINT_RESUME_V10_DRIVER_PASS\n");
