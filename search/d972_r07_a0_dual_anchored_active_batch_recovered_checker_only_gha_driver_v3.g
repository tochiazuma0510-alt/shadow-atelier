#############################################################################
## Task471 recovered rank99 checker-only replay driver v3. ASCII only.
## The checker source is authenticated by bash before its sole invocation.
#############################################################################
if not IsBound(D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_RUN) or
   D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_RUN<>true then
 Error("task471 driver: external preamble required"); fi;
D471Checker:="crosscheck/check_d972_r07_a0_dual_anchored_active_batch_recovered_v2.py";;
D471CheckerBytes:=14442;;
D471CheckerSHA:="1d1080cd3e130d987316feefd820215f495cd6320aa5eca764fd2f8997f0c424";;
D471ReleaseURL:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9808605601_gap-run-out.rank99.zip";;
D471Zip:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v3.zip";;
D471ZipBytes:=27959;; D471ZipSHA:="d707cf2553fae24863362d581ba4c09709c629a977ff772d95877dd18fdd5f48";;
D471Extract:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v3_archive";;
D471Work:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v3_work";;
D471Artifact:="d972_r07_a0_dual_anchored_active_batch_v1.json";;
D471Checkpoint:="d972_r07_a0_dual_anchored_active_batch_v1_output.checkpoint";;
D471CheckerHistoricalLog:="d972_r07_a0_dual_anchored_active_batch_v1_checker.log";;
D471ProducerLog:="d972_r07_a0_dual_anchored_active_batch_v1_producer.log";;
D471DriverHistorical:="driver.g";; D471RunLog:="run.log";;
D471CheckerLog:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v3_checker.log";;
D471Receipt:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v3_receipt.txt";;
D471Pass:="R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_V2_CHECKER_PASS";;
D471FinalPass:="TASK471_R07_RANK99_CHECKER_DRIVER_V3_PASS";;
D471RunID:="33512607989";; D471ArtifactID:="9808605601";; D471ArtifactName:="gap-run-out";;
D471HeadSHA:="3316809e483223ec571ca7d6976dc1317c892441";;
D471OriginalArtifactSHA:="fb6b6b776b8b288952196f400a0d32d57fd2a5ddb9780a7718e55cffee8bafe1";;
D471Files:=[[D471Artifact,173930,"5079ddfbffbfc00cac6b2672cbef80f7eb2cce069a2dba87aa04e7cbc420c29a"],[D471CheckerHistoricalLog,5595,"83378497196b198ef257c4918eedf103baa3532ec71675f2a15d4a5a65db3e91"],[D471Checkpoint,173082,"bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358"],[D471ProducerLog,3898,"ef366c147651cf011c16e676878a267dd5d85494d949ff02228f43c6004307af"],[D471DriverHistorical,125,"28802be0e11aad96494eaa266baed0c5b7aa9d85add29bf04a7d7d6db67f67c8"],[D471RunLog,9493,"075f3db302e3f7ee98d826cbe8b67fcbcf9355472b18322ccb29fb78a510af2a"]];;
D471Read:=function(path,label) local raw; raw:=StringFile(path); if raw=fail then Error("task471 missing ",label); fi; return raw; end;;
D471Pin:=function(path,bytes,digest,label) local raw; raw:=D471Read(path,label); if Length(raw)<>bytes or HexSHA256(raw)<>digest then Error("task471 pin drift ",label); fi; return raw; end;;
D471Quote:=function(path) if PositionSublist(path,"'")<>fail or PositionSublist(path,"\n")<>fail or PositionSublist(path,"\r")<>fail then Error("task471 unsafe path"); fi; return Concatenation("'",path,"'"); end;;
D471Member:=function(name) local path; if PositionSublist(name,"/")<>fail or PositionSublist(name,"\\")<>fail or PositionSublist(name,"..")<>fail or Length(name)=0 then Error("task471 unsafe archive member"); fi; path:=Concatenation(D471Extract,"/",name); if PositionSublist(path,Concatenation(D471Extract,"/"))<>1 then Error("task471 escaped extract root"); fi; return path; end;;
if Length(D471Files)<>6 then Error("task471 six-file manifest"); fi;
if D471RunID<>"33512607989" or D471ArtifactID<>"9808605601" or D471ArtifactName<>"gap-run-out" or
   D471HeadSHA<>"3316809e483223ec571ca7d6976dc1317c892441" or
   D471OriginalArtifactSHA<>"fb6b6b776b8b288952196f400a0d32d57fd2a5ddb9780a7718e55cffee8bafe1" then
 Error("task471 immutable binding drift"); fi;
if IsExistingFile(D471Zip) or IsDirectoryPath(D471Extract) or IsDirectoryPath(D471Work) or IsExistingFile(D471CheckerLog) or IsExistingFile(D471Receipt) then Error("task471 stale output"); fi;
if PositionSublist(D471Extract,"ci/out/")<>1 or PositionSublist(D471Work,"ci/out/")<>1 or D471Extract=D471Work then Error("task471 roots"); fi;
if not IsDirectoryPath("ci/out") then if CreateDir("ci/out")=fail then Error("task471 ci/out"); fi; fi;
D471Download:=Concatenation("set -euo pipefail; command -v curl >/dev/null; command -v unzip >/dev/null; command -v sha256sum >/dev/null; command -v timeout >/dev/null; ",
 "curl --fail --location --silent --show-error \"",D471ReleaseURL,"\" --output \"",D471Zip,"\"; ",
 "test \"$(wc -c < \"",D471Zip,"\" | tr -d [:space:])\" = \"",String(D471ZipBytes),"\"; test \"$(sha256sum \"",D471Zip,"\" | cut -d \" \" -f1)\" = \"",D471ZipSHA,"\"; ",
 "mkdir \"",D471Extract,"\"; unzip -q \"",D471Zip,"\" -d \"",D471Extract,"\"; mkdir -p \"",D471Work,"/ci/out\"; ",
 "test \"$(wc -c < \"",D471Checker,"\" | tr -d [:space:])\" = \"",String(D471CheckerBytes),"\"; test \"$(sha256sum \"",D471Checker,"\" | cut -d \" \" -f1)\" = \"",D471CheckerSHA,"\"; ",
 "test \"$(wc -c < \"",D471Extract,"/",D471Checkpoint,"\" | tr -d [:space:])\" = \"173082\"; test \"$(sha256sum \"",D471Extract,"/",D471Checkpoint,"\" | cut -d \" \" -f1)\" = \"bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358\"; ",
 "cp \"",D471Extract,"/",D471Checkpoint,"\" \"",D471Work,"/ci/out/",D471Checkpoint,"\"; cd \"",D471Work,"\"; ulimit -v 4687500; timeout --foreground --signal=TERM --kill-after=60s 6600s python3 -u -B ../../../",D471Checker," ../",D471Extract,"/",D471Artifact," > ../d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v3_checker.log 2>&1");;
Exec(Concatenation("bash -o pipefail -c ",D471Quote(D471Download)));;
for D471Row in D471Files do D471Pin(D471Member(D471Row[1]),D471Row[2],D471Row[3],D471Row[1]); od;;
D471Raw:=D471Read(D471CheckerLog,"checker log");;
if D471Raw<>Concatenation(D471Pass,"\n") then Error("task471 checker exact PASS"); fi;
D471ReceiptText:=Concatenation("schema=d972-r07-rank99-checker-driver/v3\nproduction_run_id=",D471RunID,"\nartifact_id=",D471ArtifactID,"\nartifact_name=",D471ArtifactName,"\nhead_sha=",D471HeadSHA,"\noriginal_artifact_sha256=",D471OriginalArtifactSHA,"\nchecker_path=",D471Checker,"\nchecker_bytes=",String(D471CheckerBytes),"\nchecker_sha256=",D471CheckerSHA,"\nrelease_bytes=",String(D471ZipBytes),"\nrelease_sha256=",D471ZipSHA,"\npass_marker=",D471Pass,"\npass_count=1\nworking_directory=",D471Work,"\n");;
D471Out:=OutputTextFile(D471Receipt,false);; if D471Out=fail then Error("task471 receipt"); fi; SetPrintFormattingStatus(D471Out,false);; PrintTo(D471Out,D471ReceiptText);; CloseStream(D471Out);;
Print(D471FinalPass," mode=checker-only process_count=1\n");
