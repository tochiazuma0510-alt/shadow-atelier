#############################################################################
## Task525 rank111 lazy compact-seed successor driver v12. External preamble required.
## The producer/checker and all computation semantics remain frozen from v9.
#############################################################################
if not IsBound(D972_R07_A0_LAZY_COMPACT_RANK111_RESUME_V12_RUN) or
   D972_R07_A0_LAZY_COMPACT_RANK111_RESUME_V12_RUN<>true then
 Error("task525 external preamble required"); fi;
D525Producer:="search/d972_r07_a0_actual_tau_free_lazy_compact_seed_v4.py";;
D525Checker:="crosscheck/check_d972_r07_a0_actual_tau_free_lazy_compact_seed_v8.py";;
D525ReleaseURL:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9826862037_gap-run-out.a0-rank111.zip";;
D525Run:="33564845217";; D525Job:="100045550767";;
D525Head:="c582f8d786012a668783790007b72c5c422c3db8";;
D525APIArtifactID:="9826862037";; D525APIArtifactName:="gap-run-out";; D525APIArtifactSize:=96198;;
D525Zip:="ci/out/d972_r07_a0_actual_tau_free_lazy_rank111_resume_v12.zip";;
D525Extract:="ci/out/d972_r07_a0_actual_tau_free_lazy_rank111_resume_v12_archive";;
D525ResumeMember:="d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint";;
D525Input:="ci/out/d972_r07_a0_actual_tau_free_lazy_rank111_resume_v12_input.checkpoint";;
D525Artifact:="ci/out/d972_r07_a0_actual_tau_free_lazy_compact_seed_v4.json";;
D525Checkpoint:="ci/out/d972_r07_a0_actual_tau_free_lazy_compact_seed_v4_output.checkpoint";;
D525PL:="ci/out/d972_r07_a0_actual_tau_free_lazy_compact_seed_v4_producer.log";;
D525CL:="ci/out/d972_r07_a0_actual_tau_free_lazy_compact_seed_v4_checker.log";;
D525DL:="ci/out/d972_r07_a0_actual_tau_free_lazy_rank111_resume_v12_preflight.log";;
D525ZipBytes:=37586;;
D525ZipSHA:="8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de";;
D525ProducerBytes:=4199;;
D525ProducerSHA:="8267edcc89b605fea5f3641c3547e05abf23d0e6370a18cc297c6803739b4e26";;
D525CheckerBytes:=1348;;
D525CheckerSHA:="36b9a6fa5de45aa94a30ad39a3dfa5db525213529d7ac19684883a02eaefe477";;
D525ResumeBytes:=85934;;
D525ResumeSHA:="69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93";;
D525MemberManifest:=[
 ["d972_r07_a0_actual_tau_free_rank98_resume_v10_input.checkpoint",69947,"c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f"],
 ["d972_r07_a0_actual_tau_free_rank98_resume_v10_preflight.log",38,"52f94358c40a2e6968927b4078a0bf00b6a40c32eb013367679e8d59b599240c"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10.json",86354,"39434b6a4c1a7851805c2deb3be8de4e7e919085a537b8d3913a15d341c19279"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10_checker.log",51,"aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint",85934,"69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v10_producer.log",4905,"271d05e70153cbceadf9d45478a4357bcd7899610b3857b3525644205b7e975c"],
 ["driver.g",128,"393794cf2188ac0a27abe472180ddabca42e7f88082248726e4ae664cd371978"],
 ["run.log",5004,"ac7fcf963237cc23d88774df9c85d82cb8b3acc09f24b0ee4dda5506e719bf15"]
];;
D525Quote:=function(s)
 if PositionSublist(s,"'")<>fail or PositionSublist(s,"\n")<>fail or
    PositionSublist(s,"\r")<>fail then Error("task525 unsafe shell text"); fi;
 return Concatenation("'",s,"'");
end;;
if Length(D525MemberManifest)<>8 then Error("task525 eight-member manifest"); fi;
if D525Run<>"33564845217" or D525Job<>"100045550767" or
   D525Head<>"c582f8d786012a668783790007b72c5c422c3db8" or
   D525APIArtifactID<>"9826862037" or D525APIArtifactName<>"gap-run-out" or
   D525APIArtifactSize<>96198 or
   D525ReleaseURL<>"https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9826862037_gap-run-out.a0-rank111.zip" or
   D525ZipBytes<>37586 or D525ZipSHA<>"8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de" then
 Error("task525 immutable source binding drift"); fi;
if IsExistingFile(D525Zip) or IsDirectoryPath(D525Extract) or
   IsExistingFile(D525Input) or IsExistingFile(D525Artifact) or
   IsExistingFile(D525Checkpoint) or IsExistingFile(D525PL) or
   IsExistingFile(D525CL) or IsExistingFile(D525DL) then
 Error("task525 stale output"); fi;
if not IsDirectoryPath("ci/out") then
 if CreateDir("ci/out")=fail then Error("task525 ci/out"); fi; fi;
D525Cmd:=Concatenation(
 "set -euo pipefail; umask 077; ",
 "test ! -e \"",D525DL,"\"; test ! -L \"",D525DL,"\"; ",
 "exec 9>\"",D525DL,"\"; ",
 "printf \"TASK525_R07_A0_LAZY_RANK111_PREFLIGHT_BEGIN\\n\" >&9; ",
 "task525_preflight_fail() { rc=$?; printf \"TASK525_R07_A0_LAZY_RANK111_PREFLIGHT_FAIL rc=%s cmd=%s\\n\" \"$rc\" \"$BASH_COMMAND\" >&9; return \"$rc\"; }; ",
 "trap task525_preflight_fail ERR; ",
 "command -v curl >/dev/null; command -v unzip >/dev/null; command -v sha256sum >/dev/null; ",
 "command -v timeout >/dev/null; command -v tee >/dev/null; command -v grep >/dev/null; ",
 "test ! -e \"",D525Zip,"\"; test ! -L \"",D525Zip,"\"; ",
 "test ! -e \"",D525Extract,"\"; test ! -L \"",D525Extract,"\"; ",
 "test ! -e \"",D525Input,"\"; test ! -L \"",D525Input,"\"; ",
 "test ! -e \"",D525Artifact,"\"; test ! -L \"",D525Artifact,"\"; ",
 "test ! -e \"",D525Checkpoint,"\"; test ! -L \"",D525Checkpoint,"\"; ",
 "test ! -e \"",D525PL,"\"; test ! -L \"",D525PL,"\"; ",
 "test ! -e \"",D525CL,"\"; test ! -L \"",D525CL,"\"; ",
 "test -f \"",D525Producer,"\"; test ! -L \"",D525Producer,"\"; ",
 "test \"$(wc -c < \"",D525Producer,"\" | tr -d \"[:space:]\")\" = \"",String(D525ProducerBytes),"\"; ",
 "test \"$(sha256sum \"",D525Producer,"\" | cut -d \" \" -f1)\" = \"",D525ProducerSHA,"\"; ",
 "test -f \"",D525Checker,"\"; test ! -L \"",D525Checker,"\"; ",
 "test \"$(wc -c < \"",D525Checker,"\" | tr -d \"[:space:]\")\" = \"",String(D525CheckerBytes),"\"; ",
 "test \"$(sha256sum \"",D525Checker,"\" | cut -d \" \" -f1)\" = \"",D525CheckerSHA,"\"; ",
 "curl --fail --location --silent --show-error \"",D525ReleaseURL,"\" --output \"",D525Zip,"\"; ",
 "test \"$(wc -c < \"",D525Zip,"\" | tr -d \"[:space:]\")\" = \"",String(D525ZipBytes),"\"; ",
 "test \"$(sha256sum \"",D525Zip,"\" | cut -d \" \" -f1)\" = \"",D525ZipSHA,"\"; ",
 "mkdir \"",D525Extract,"\"; unzip -q \"",D525Zip,"\" -d \"",D525Extract,"\"; ",
 "test \"$(unzip -Z1 \"",D525Zip,"\" | wc -l | tr -d \"[:space:]\")\" = \"8\"; ");
for D525Row in D525MemberManifest do
 D525Path:=Concatenation(D525Extract,"/",D525Row[1]);
 D525Cmd:=Concatenation(D525Cmd,
  "test -f \"",D525Path,"\"; test \"$(wc -c < \"",D525Path,
  "\" | tr -d \"[:space:]\")\" = \"",String(D525Row[2]),"\"; ",
  "test \"$(sha256sum \"",D525Path,"\" | cut -d \" \" -f1)\" = \"",D525Row[3],"\"; ");
od;
D525ResumePath:=Concatenation(D525Extract,"/",D525ResumeMember);
D525Cmd:=Concatenation(D525Cmd,
 "cp \"",D525ResumePath,"\" \"",D525Input,"\"; ",
 "test \"$(wc -c < \"",D525Input,"\" | tr -d \"[:space:]\")\" = \"",String(D525ResumeBytes),"\"; ",
 "test \"$(sha256sum \"",D525Input,"\" | cut -d \" \" -f1)\" = \"",D525ResumeSHA,"\"; ",
 "ulimit -v 5200000; ",
 "timeout --foreground --signal=TERM --kill-after=60s 7500s python3 -u -B ",D525Producer,
 " --mode PRODUCTION --resume \"",D525Input,
 "\" --seconds 7200 --rss-bytes 4800000000 --max-rises 64 --output \"",D525Artifact,
 "\" --checkpoint \"",D525Checkpoint,"\" 2>&1 | tee \"",D525PL,"\"; ",
 "test -s \"",D525Artifact,"\"; test -s \"",D525Checkpoint,"\"; ",
 "test \"$(grep -Ec \"^R07_A0_ACTUAL_TAU_FREE_LAZY_COMPACT_SEED_V4 (FIXTURE|UNKNOWN|UNKNOWN_RESOURCE)$\" \"",D525PL,"\")\" = \"1\"; ",
 "timeout --foreground --signal=TERM --kill-after=60s 3600s python3 -u -B ",D525Checker,
 " \"",D525Artifact,"\" 2>&1 | tee \"",D525CL,"\"; ",
 "test \"$(grep -Fc \"R07_A0_ACTUAL_TAU_FREE_LAZY_COMPACT_SEED_V8_CHECKER_PASS\" \"",D525CL,"\")\" = \"1\"; ",
 "test \"$(wc -l < \"",D525CL,"\" | tr -d \"[:space:]\")\" = \"1\"; ");
Exec(Concatenation("bash -o pipefail -c ",D525Quote(D525Cmd)));
if not IsExistingFile(D525DL) or Length(StringFile(D525DL))=0 then
 Error("task525 preflight diagnostic missing"); fi;
if not IsExistingFile(D525Artifact) or not IsExistingFile(D525Checkpoint) or
   not IsExistingFile(D525CL) then Error("task525 result/checker missing"); fi;
if Length(StringFile(D525Artifact))=0 or Length(StringFile(D525Checkpoint))=0 then
 Error("task525 result/checkpoint empty"); fi;
if PositionSublist(StringFile(D525PL),"R07_A0_ACTUAL_TAU_FREE_LAZY_COMPACT_SEED_V4 ")=fail then
 Error("task525 producer marker"); fi;
if StringFile(D525CL)<>"R07_A0_ACTUAL_TAU_FREE_LAZY_COMPACT_SEED_V8_CHECKER_PASS status=UNKNOWN_RESOURCE\n" then
 Error("task525 checker marker"); fi;
Print("R07_A0_LAZY_RANK111_RESUME_V12_DRIVER_PASS\n");
