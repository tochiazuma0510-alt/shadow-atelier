#############################################################################
## Task475 recovered rank99 checker-only replay driver v4. ASCII only.
## Repair: the checker receives the artifact from its post-cd ci/out cone.
#############################################################################
if not IsBound(D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_RUN) or
   D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_RUN<>true then
 Error("task475 driver: external preamble required"); fi;
D475Checker:="crosscheck/check_d972_r07_a0_dual_anchored_active_batch_recovered_v2.py";;
D475CheckerBytes:=14442;;
D475CheckerSHA:="1d1080cd3e130d987316feefd820215f495cd6320aa5eca764fd2f8997f0c424";;
D475ReleaseURL:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9808605601_gap-run-out.rank99.zip";;
D475Zip:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v4.zip";;
D475ZipBytes:=27959;; D475ZipSHA:="d707cf2553fae24863362d581ba4c09709c629a977ff772d95877dd18fdd5f48";;
D475Extract:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v4_archive";;
D475Work:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v4_work";;
D475Artifact:="d972_r07_a0_dual_anchored_active_batch_v1.json";;
D475Checkpoint:="d972_r07_a0_dual_anchored_active_batch_v1_output.checkpoint";;
D475CheckerHistoricalLog:="d972_r07_a0_dual_anchored_active_batch_v1_checker.log";;
D475ProducerLog:="d972_r07_a0_dual_anchored_active_batch_v1_producer.log";;
D475DriverHistorical:="driver.g";; D475RunLog:="run.log";;
D475CheckerLog:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v4_checker.log";;
D475Receipt:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v4_receipt.txt";;
D475Pass:="R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_V2_CHECKER_PASS";;
D475FinalPass:="TASK475_R07_RANK99_CHECKER_DRIVER_V4_PASS";;
D475RunID:="33512607989";; D475ArtifactID:="9808605601";; D475ArtifactName:="gap-run-out";;
D475HeadSHA:="3316809e483223ec571ca7d6976dc1317c892441";;
D475OriginalArtifactSHA:="fb6b6b776b8b288952196f400a0d32d57fd2a5ddb9780a7718e55cffee8bafe1";;
D475Files:=[[D475Artifact,173930,"5079ddfbffbfc00cac6b2672cbef80f7eb2cce069a2dba87aa04e7cbc420c29a"],[D475CheckerHistoricalLog,5595,"83378497196b198ef257c4918eedf103baa3532ec71675f2a15d4a5a65db3e91"],[D475Checkpoint,173082,"bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358"],[D475ProducerLog,3898,"ef366c147651cf011c16e676878a267dd5d85494d949ff02228f43c6004307af"],[D475DriverHistorical,125,"28802be0e11aad96494eaa266baed0c5b7aa9d85add29bf04a7d7d6db67f67c8"],[D475RunLog,9493,"075f3db302e3f7ee98d826cbe8b67fcbcf9355472b18322ccb29fb78a510af2a"]];;
D475Read:=function(path,label) local raw; raw:=StringFile(path); if raw=fail then Error("task475 missing ",label); fi; return raw; end;;
D475Pin:=function(path,bytes,digest,label) local raw; raw:=D475Read(path,label); if Length(raw)<>bytes or HexSHA256(raw)<>digest then Error("task475 pin drift ",label); fi; return raw; end;;
D475Quote:=function(path) if PositionSublist(path,"'")<>fail or PositionSublist(path,"\n")<>fail or PositionSublist(path,"\r")<>fail then Error("task475 unsafe path"); fi; return Concatenation("'",path,"'"); end;;
D475Member:=function(name) local path; if PositionSublist(name,"/")<>fail or PositionSublist(name,"\\")<>fail or PositionSublist(name,"..")<>fail or Length(name)=0 then Error("task475 unsafe archive member"); fi; path:=Concatenation(D475Extract,"/",name); if PositionSublist(path,Concatenation(D475Extract,"/"))<>1 then Error("task475 escaped extract root"); fi; return path; end;;
if Length(D475Files)<>6 then Error("task475 six-file manifest"); fi;
if D475RunID<>"33512607989" or D475ArtifactID<>"9808605601" or D475ArtifactName<>"gap-run-out" or
   D475HeadSHA<>"3316809e483223ec571ca7d6976dc1317c892441" or
   D475OriginalArtifactSHA<>"fb6b6b776b8b288952196f400a0d32d57fd2a5ddb9780a7718e55cffee8bafe1" then
 Error("task475 immutable binding drift"); fi;
if IsExistingFile(D475Zip) or IsDirectoryPath(D475Extract) or IsDirectoryPath(D475Work) or IsExistingFile(D475CheckerLog) or IsExistingFile(D475Receipt) then Error("task475 stale output"); fi;
if PositionSublist(D475Extract,"ci/out/")<>1 or PositionSublist(D475Work,"ci/out/")<>1 or D475Extract=D475Work then Error("task475 roots"); fi;
D475PostCDArtifact:=Concatenation(D475Work,"/ci/out/",D475Artifact);;
D475PostCDCheckpoint:=Concatenation(D475Work,"/ci/out/",D475Checkpoint);;
if PositionSublist(D475PostCDArtifact,Concatenation(D475Work,"/ci/out/"))<>1 or
   PositionSublist(D475PostCDCheckpoint,Concatenation(D475Work,"/ci/out/"))<>1 or
   D475PostCDArtifact=D475PostCDCheckpoint then Error("task475 post-cd paths"); fi;
if not IsDirectoryPath("ci/out") then if CreateDir("ci/out")=fail then Error("task475 ci/out"); fi; fi;
D475Download:=Concatenation("set -euo pipefail; command -v curl >/dev/null; command -v unzip >/dev/null; command -v sha256sum >/dev/null; command -v timeout >/dev/null; ",
 "curl --fail --location --silent --show-error \"",D475ReleaseURL,"\" --output \"",D475Zip,"\"; ",
 "test \"$(wc -c < \"",D475Zip,"\" | tr -d [:space:])\" = \"",String(D475ZipBytes),"\"; test \"$(sha256sum \"",D475Zip,"\" | cut -d \" \" -f1)\" = \"",D475ZipSHA,"\"; ",
 "mkdir \"",D475Extract,"\"; unzip -q \"",D475Zip,"\" -d \"",D475Extract,"\"; mkdir -p \"",D475Work,"/ci/out\"; ",
 "test \"$(wc -c < \"",D475Checker,"\" | tr -d [:space:])\" = \"",String(D475CheckerBytes),"\"; test \"$(sha256sum \"",D475Checker,"\" | cut -d \" \" -f1)\" = \"",D475CheckerSHA,"\"; ",
 "test \"$(wc -c < \"",D475Extract,"/",D475Artifact,"\" | tr -d [:space:])\" = \"173930\"; test \"$(sha256sum \"",D475Extract,"/",D475Artifact,"\" | cut -d \" \" -f1)\" = \"5079ddfbffbfc00cac6b2672cbef80f7eb2cce069a2dba87aa04e7cbc420c29a\"; ",
 "test \"$(wc -c < \"",D475Extract,"/",D475Checkpoint,"\" | tr -d [:space:])\" = \"173082\"; test \"$(sha256sum \"",D475Extract,"/",D475Checkpoint,"\" | cut -d \" \" -f1)\" = \"bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358\"; ",
 "cp \"",D475Extract,"/",D475Artifact,"\" \"",D475PostCDArtifact,"\"; cp \"",D475Extract,"/",D475Checkpoint,"\" \"",D475PostCDCheckpoint,"\"; ",
 "test \"$(wc -c < \"",D475PostCDArtifact,"\" | tr -d [:space:])\" = \"173930\"; test \"$(sha256sum \"",D475PostCDArtifact,"\" | cut -d \" \" -f1)\" = \"5079ddfbffbfc00cac6b2672cbef80f7eb2cce069a2dba87aa04e7cbc420c29a\"; ",
 "test \"$(wc -c < \"",D475PostCDCheckpoint,"\" | tr -d [:space:])\" = \"173082\"; test \"$(sha256sum \"",D475PostCDCheckpoint,"\" | cut -d \" \" -f1)\" = \"bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358\"; ",
 "cd \"",D475Work,"\"; test -f \"ci/out/",D475Artifact,"\"; test -f \"ci/out/",D475Checkpoint,"\"; ulimit -v 4687500; timeout --foreground --signal=TERM --kill-after=60s 6600s python3 -u -B ../../../",D475Checker," ci/out/",D475Artifact," > ../d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v4_checker.log 2>&1");;
Exec(Concatenation("bash -o pipefail -c ",D475Quote(D475Download)));;
for D475Row in D475Files do D475Pin(D475Member(D475Row[1]),D475Row[2],D475Row[3],D475Row[1]); od;;
D475Raw:=D475Read(D475CheckerLog,"checker log");;
if D475Raw<>Concatenation(D475Pass,"\n") then Error("task475 checker exact PASS"); fi;
D475ReceiptText:=Concatenation("schema=d972-r07-rank99-checker-driver/v4\nproduction_run_id=",D475RunID,"\nartifact_id=",D475ArtifactID,"\nartifact_name=",D475ArtifactName,"\nhead_sha=",D475HeadSHA,"\noriginal_artifact_sha256=",D475OriginalArtifactSHA,"\nchecker_path=",D475Checker,"\nchecker_bytes=",String(D475CheckerBytes),"\nchecker_sha256=",D475CheckerSHA,"\nrelease_bytes=",String(D475ZipBytes),"\nrelease_sha256=",D475ZipSHA,"\npass_marker=",D475Pass,"\npass_count=1\nworking_directory=",D475Work,"\npost_cd_artifact=ci/out/",D475Artifact,"\npost_cd_checkpoint=ci/out/",D475Checkpoint,"\n");;
D475Out:=OutputTextFile(D475Receipt,false);; if D475Out=fail then Error("task475 receipt"); fi; SetPrintFormattingStatus(D475Out,false);; PrintTo(D475Out,D475ReceiptText);; CloseStream(D475Out);;
Print(D475FinalPass," mode=checker-only process_count=1\n");
