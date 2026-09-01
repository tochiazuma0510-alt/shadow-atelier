#############################################################################
## Task470 recovered rank99 checker-only replay driver v2. ASCII only.
## The checker source is authenticated by bash before its sole invocation.
#############################################################################
if not IsBound(D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_RUN) or
   D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_RUN<>true then
 Error("task470 driver: external preamble required"); fi;
D470Checker:="crosscheck/check_d972_r07_a0_dual_anchored_active_batch_recovered_v2.py";;
D470CheckerBytes:=14442;;
D470CheckerSHA:="1d1080cd3e130d987316feefd820215f495cd6320aa5eca764fd2f8997f0c424";;
D470ReleaseURL:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9808605601_gap-run-out.rank99.zip";;
D470Zip:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v2.zip";;
D470ZipBytes:=27959;; D470ZipSHA:="d707cf2553fae24863362d581ba4c09709c629a977ff772d95877dd18fdd5f48";;
D470Extract:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v2_archive";;
D470Work:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v2_work";;
D470Artifact:="d972_r07_a0_dual_anchored_active_batch_v1.json";;
D470Checkpoint:="d972_r07_a0_dual_anchored_active_batch_v1_output.checkpoint";;
D470CheckerHistoricalLog:="d972_r07_a0_dual_anchored_active_batch_v1_checker.log";;
D470ProducerLog:="d972_r07_a0_dual_anchored_active_batch_v1_producer.log";;
D470DriverHistorical:="driver.g";; D470RunLog:="run.log";;
D470CheckerLog:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v2_checker.log";;
D470Receipt:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v2_receipt.txt";;
D470Pass:="R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_V2_CHECKER_PASS";;
D470FinalPass:="TASK470_R07_RANK99_CHECKER_DRIVER_V2_PASS";;
D470RunID:="33512607989";; D470ArtifactID:="9808605601";; D470ArtifactName:="gap-run-out";;
D470HeadSHA:="3316809e483223ec571ca7d6976dc1317c892441";;
D470OriginalArtifactSHA:="fb6b6b776b8b288952196f400a0d32d57fd2a5ddb9780a7718e55cffee8bafe1";;
D470Files:=[[D470Artifact,173930,"5079ddfbffbfc00cac6b2672cbef80f7eb2cce069a2dba87aa04e7cbc420c29a"],[D470CheckerHistoricalLog,5595,"83378497196b198ef257c4918eedf103baa3532ec71675f2a15d4a5a65db3e91"],[D470Checkpoint,173082,"bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358"],[D470ProducerLog,3898,"ef366c147651cf011c16e676878a267dd5d85494d949ff02228f43c6004307af"],[D470DriverHistorical,125,"28802be0e11aad96494eaa266baed0c5b7aa9d85add29bf04a7d7d6db67f67c8"],[D470RunLog,9493,"075f3db302e3f7ee98d826cbe8b67fcbcf9355472b18322ccb29fb78a510af2a"]];;
D470Read:=function(path,label) local raw; raw:=StringFile(path); if raw=fail then Error("task470 missing ",label); fi; return raw; end;;
D470Pin:=function(path,bytes,digest,label) local raw; raw:=D470Read(path,label); if Length(raw)<>bytes or HexSHA256(raw)<>digest then Error("task470 pin drift ",label); fi; return raw; end;;
D470Quote:=function(path) if PositionSublist(path,"'")<>fail or PositionSublist(path,"\n")<>fail or PositionSublist(path,"\r")<>fail then Error("task470 unsafe path"); fi; return Concatenation("'",path,"'"); end;;
D470Member:=function(name) local path; if PositionSublist(name,"/")<>fail or PositionSublist(name,"\\")<>fail or PositionSublist(name,"..")<>fail or Length(name)=0 then Error("task470 unsafe archive member"); fi; path:=Concatenation(D470Extract,"/",name); if PositionSublist(path,Concatenation(D470Extract,"/"))<>1 then Error("task470 escaped extract root"); fi; return path; end;;
if Length(D470Files)<>6 then Error("task470 six-file manifest"); fi;
if D470RunID<>"33512607989" or D470ArtifactID<>"9808605601" or D470ArtifactName<>"gap-run-out" or
   D470HeadSHA<>"3316809e483223ec571ca7d6976dc1317c892441" or
   D470OriginalArtifactSHA<>"fb6b6b776b8b288952196f400a0d32d57fd2a5ddb9780a7718e55cffee8bafe1" then
 Error("task470 immutable binding drift"); fi;
if IsExistingFile(D470Zip) or IsDirectoryPath(D470Extract) or IsDirectoryPath(D470Work) or IsExistingFile(D470CheckerLog) or IsExistingFile(D470Receipt) then Error("task470 stale output"); fi;
if PositionSublist(D470Extract,"ci/out/")<>1 or PositionSublist(D470Work,"ci/out/")<>1 or D470Extract=D470Work then Error("task470 roots"); fi;
if not IsDirectoryPath("ci/out") then if CreateDir("ci/out")=fail then Error("task470 ci/out"); fi; fi;
D470Download:=Concatenation("set -euo pipefail; command -v curl >/dev/null; command -v unzip >/dev/null; command -v sha256sum >/dev/null; command -v timeout >/dev/null; ",
 "curl --fail --location --silent --show-error \"",D470ReleaseURL,"\" --output ",D470Quote(D470Zip),"; ",
 "test \"$(wc -c < ",D470Quote(D470Zip)," | tr -d '[:space:]')\" = \"",String(D470ZipBytes),"\"; test \"$(sha256sum ",D470Quote(D470Zip)," | cut -d ' ' -f1)\" = \"",D470ZipSHA,"\"; ",
 "mkdir ",D470Quote(D470Extract),"; unzip -q ",D470Quote(D470Zip)," -d ",D470Quote(D470Extract),"; mkdir -p ",D470Quote(D470Work),"/ci/out; ",
 "test \"$(wc -c < ",D470Quote(D470Checker)," | tr -d '[:space:]')\" = \"",String(D470CheckerBytes),"\"; test \"$(sha256sum ",D470Quote(D470Checker)," | cut -d ' ' -f1)\" = \"",D470CheckerSHA,"\"; ",
 "test \"$(wc -c < ",D470Extract,"/",D470Checkpoint," | tr -d '[:space:]')\" = \"173082\"; test \"$(sha256sum ",D470Extract,"/",D470Checkpoint," | cut -d ' ' -f1)\" = \"bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358\"; ",
 "cp ",D470Extract,"/",D470Checkpoint," ",D470Work,"/ci/out/",D470Checkpoint,"; cd ",D470Work,"; ulimit -v 4687500; timeout --foreground --signal=TERM --kill-after=60s 6600s python3 -u -B ../../../",D470Checker," ../",D470Extract,"/",D470Artifact," > ../d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v2_checker.log 2>&1");;
Exec(Concatenation("bash -o pipefail -c ",D470Quote(D470Download)));;
for D470Row in D470Files do D470Pin(D470Member(D470Row[1]),D470Row[2],D470Row[3],D470Row[1]); od;;
D470Raw:=D470Read(D470CheckerLog,"checker log");;
if D470Raw<>Concatenation(D470Pass,"\n") then Error("task470 checker exact PASS"); fi;
D470ReceiptText:=Concatenation("schema=d972-r07-rank99-checker-driver/v2\nproduction_run_id=",D470RunID,"\nartifact_id=",D470ArtifactID,"\nartifact_name=",D470ArtifactName,"\nhead_sha=",D470HeadSHA,"\noriginal_artifact_sha256=",D470OriginalArtifactSHA,"\nchecker_path=",D470Checker,"\nchecker_bytes=",String(D470CheckerBytes),"\nchecker_sha256=",D470CheckerSHA,"\nrelease_bytes=",String(D470ZipBytes),"\nrelease_sha256=",D470ZipSHA,"\npass_marker=",D470Pass,"\npass_count=1\nworking_directory=",D470Work,"\n");;
D470Out:=OutputTextFile(D470Receipt,false);; if D470Out=fail then Error("task470 receipt"); fi; SetPrintFormattingStatus(D470Out,false);; PrintTo(D470Out,D470ReceiptText);; CloseStream(D470Out);;
Print(D470FinalPass," mode=checker-only process_count=1\n");
