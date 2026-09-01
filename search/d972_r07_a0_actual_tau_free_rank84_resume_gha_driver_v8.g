#############################################################################
## Task484 rank-84 single-row continuation v8. External preamble required.
## The UNKNOWN_RESOURCE terminal is transport state, not A0 completion.
## producer wall has a 300s margin; VM has a 524800000-byte margin.
#############################################################################
if not IsBound(D972_R07_A0_RANK84_CHECKPOINT_RESUME_V8_RUN) or
   D972_R07_A0_RANK84_CHECKPOINT_RESUME_V8_RUN<>true then
 Error("task484 external preamble required"); fi;
D484Producer:="search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py";;
D484Checker:="crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py";;
D484ReleaseURL:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9812928957_gap-run-out.rank84.zip";;
D484Run:="33524681526";; D484Job:="99912387760";;
D484Head:="dd67f12b0ee4f022061df27ed396ad3d3a37f264";;
D484APIZipSHA:="4b3239f35f6ec2a4859e6a81e2b49456702f0f22f695a7332089b407dbcb817d";;
D484Zip:="ci/out/d972_r07_a0_actual_tau_free_rank84_resume_v8.zip";;
D484Extract:="ci/out/d972_r07_a0_actual_tau_free_rank84_resume_v8_archive";;
D484ResumeMember:="d972_r07_a0_actual_tau_free_rank_ladder_v7_output.checkpoint";;
D484Input:="ci/out/d972_r07_a0_actual_tau_free_rank84_resume_v8_input.checkpoint";;
D484Artifact:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v8.json";;
D484Checkpoint:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v8_output.checkpoint";;
D484PL:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v8_producer.log";;
D484CL:="ci/out/d972_r07_a0_actual_tau_free_rank_ladder_v8_checker.log";;
D484ZipBytes:=23004;;
D484ZipSHA:="dde60bad768e20ead6ad08e8bd0a8e53fc97050a43f6c207552ba97d579c438a";;
D484ProducerBytes:=12215;;
D484ProducerSHA:="0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37";;
D484CheckerBytes:=3653;;
D484CheckerSHA:="e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1";;
D484ResumeBytes:=52707;;
D484ResumeSHA:="eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24";;
D484MemberManifest:=[
 ["d972_r07_a0_actual_tau_free_rank68_input_v1.checkpoint",33015,"73ad85624d079d01ecc824ab6adc699c51b0dabfddcc36c0f7d2bd4384f7d5a4"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v7.json",53125,"97dfa69864c95f1a3ec7dc5428fcceee50d9eaa1ea07f5cabb0fb8df8c27b59"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v7_checker.log",51,"aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v7_output.checkpoint",52707,"eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24"],
 ["d972_r07_a0_actual_tau_free_rank_ladder_v7_producer.log",5179,"475d51fa9af4a498ab92125ad7b59058ef372fafb890204530989970ff3e7513"],
 ["driver.g",124,"f521a63c21f940c7ebc44665606995acb45464ef9e7ca4606630875bda0eb01c"],
 ["run.log",5277,"11856023c568b25066b1604eb3fc8dc1879413bfd439bad5ef658f0f2571788f"]
];;
D484Quote:=function(s)
 if PositionSublist(s,"'")<>fail or PositionSublist(s,"\n")<>fail or
    PositionSublist(s,"\r")<>fail then Error("task484 unsafe shell text"); fi;
 return Concatenation("'",s,"'");
end;;
if Length(D484MemberManifest)<>7 then Error("task484 seven-member manifest"); fi;
if D484Run<>"33524681526" or D484Job<>"99912387760" or
   D484Head<>"dd67f12b0ee4f022061df27ed396ad3d3a37f264" or
   D484APIZipSHA<>"4b3239f35f6ec2a4859e6a81e2b49456702f0f22f695a7332089b407dbcb817d" then
 Error("task484 immutable source binding drift"); fi;
if IsExistingFile(D484Zip) or IsDirectoryPath(D484Extract) or
   IsExistingFile(D484Input) or IsExistingFile(D484Artifact) or
   IsExistingFile(D484Checkpoint) or IsExistingFile(D484PL) or
   IsExistingFile(D484CL) then Error("task484 stale output"); fi;
if not IsDirectoryPath("ci/out") then
 if CreateDir("ci/out")=fail then Error("task484 ci/out"); fi; fi;
D484Cmd:=Concatenation(
 "set -euo pipefail; umask 077; ",
 "command -v curl >/dev/null; command -v unzip >/dev/null; command -v sha256sum >/dev/null; ",
 "command -v timeout >/dev/null; command -v tee >/dev/null; command -v grep >/dev/null; ",
 "test ! -e \"",D484Zip,"\"; test ! -L \"",D484Zip,"\"; ",
 "test ! -e \"",D484Extract,"\"; test ! -L \"",D484Extract,"\"; ",
 "test ! -e \"",D484Input,"\"; test ! -L \"",D484Input,"\"; ",
 "test ! -e \"",D484Artifact,"\"; test ! -L \"",D484Artifact,"\"; ",
 "test ! -e \"",D484Checkpoint,"\"; test ! -L \"",D484Checkpoint,"\"; ",
 "test ! -e \"",D484PL,"\"; test ! -L \"",D484PL,"\"; ",
 "test ! -e \"",D484CL,"\"; test ! -L \"",D484CL,"\"; ",
 "test -f \"",D484Producer,"\"; test ! -L \"",D484Producer,"\"; ",
 "test \"$(wc -c < \"",D484Producer,"\" | tr -d \"[:space:]\")\" = \"",String(D484ProducerBytes),"\"; ",
 "test \"$(sha256sum \"",D484Producer,"\" | cut -d \" \" -f1)\" = \"",D484ProducerSHA,"\"; ",
 "test -f \"",D484Checker,"\"; test ! -L \"",D484Checker,"\"; ",
 "test \"$(wc -c < \"",D484Checker,"\" | tr -d \"[:space:]\")\" = \"",String(D484CheckerBytes),"\"; ",
 "test \"$(sha256sum \"",D484Checker,"\" | cut -d \" \" -f1)\" = \"",D484CheckerSHA,"\"; ",
 "curl --fail --location --silent --show-error \"",D484ReleaseURL,"\" --output \"",D484Zip,"\"; ",
 "test \"$(wc -c < \"",D484Zip,"\" | tr -d \"[:space:]\")\" = \"",String(D484ZipBytes),"\"; ",
 "test \"$(sha256sum \"",D484Zip,"\" | cut -d \" \" -f1)\" = \"",D484ZipSHA,"\"; ",
 "mkdir \"",D484Extract,"\"; unzip -q \"",D484Zip,"\" -d \"",D484Extract,"\"; ",
 "test \"$(unzip -Z1 \"",D484Zip,"\" | wc -l | tr -d \"[:space:]\")\" = \"7\"; ");
for D484Row in D484MemberManifest do
 D484Path:=Concatenation(D484Extract,"/",D484Row[1]);
 D484Cmd:=Concatenation(D484Cmd,
  "test -f \"",D484Path,"\"; test \"$(wc -c < \"",D484Path,
  "\" | tr -d \"[:space:]\")\" = \"",String(D484Row[2]),"\"; ",
  "test \"$(sha256sum \"",D484Path,"\" | cut -d \" \" -f1)\" = \"",D484Row[3],"\"; ");
od;
D484ResumePath:=Concatenation(D484Extract,"/",D484ResumeMember);
D484Cmd:=Concatenation(D484Cmd,
 "cp \"",D484ResumePath,"\" \"",D484Input,"\"; ",
 "test \"$(wc -c < \"",D484Input,"\" | tr -d \"[:space:]\")\" = \"",String(D484ResumeBytes),"\"; ",
 "test \"$(sha256sum \"",D484Input,"\" | cut -d \" \" -f1)\" = \"",D484ResumeSHA,"\"; ",
 "ulimit -v 5200000; ",
 "timeout --foreground --signal=TERM --kill-after=60s 7500s python3 -u -B ",D484Producer,
 " --mode PRODUCTION --resume \"",D484Input,
 "\" --seconds 7200 --rss-bytes 4800000000 --max-rises 64 --output \"",D484Artifact,
 "\" --checkpoint \"",D484Checkpoint,"\" 2>&1 | tee \"",D484PL,"\"; ",
 "test -s \"",D484Artifact,"\"; test -s \"",D484Checkpoint,"\"; ",
 "test \"$(grep -Ec \"^R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V3 status=[A-Z_]+$\" \"",D484PL,"\")\" = \"1\"; ",
 "timeout --foreground --signal=TERM --kill-after=60s 3600s python3 -u -B ",D484Checker,
 " \"",D484Artifact,"\" 2>&1 | tee \"",D484CL,"\"; ",
 "test \"$(grep -Fc \"R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V7_CHECKER_PASS\" \"",D484CL,"\")\" = \"1\"; ",
 "test \"$(wc -l < \"",D484CL,"\" | tr -d \"[:space:]\")\" = \"1\"; ");
Exec(Concatenation("bash -o pipefail -c ",D484Quote(D484Cmd)));
if not IsExistingFile(D484Artifact) or not IsExistingFile(D484Checkpoint) or
   not IsExistingFile(D484CL) then Error("task484 result/checker missing"); fi;
if Length(StringFile(D484Artifact))=0 or Length(StringFile(D484Checkpoint))=0 then
 Error("task484 result/checkpoint empty"); fi;
if PositionSublist(StringFile(D484PL),"R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V3 status=")=fail then
 Error("task484 producer marker"); fi;
if StringFile(D484CL)<>"R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V7_CHECKER_PASS\n" then
 Error("task484 checker marker"); fi;
Print("R07_A0_RANK84_CHECKPOINT_RESUME_V8_DRIVER_PASS\n");
