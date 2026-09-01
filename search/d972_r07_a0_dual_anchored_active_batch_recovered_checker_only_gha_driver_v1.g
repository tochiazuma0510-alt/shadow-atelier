#############################################################################
## Task467 recovered Task451 checker-only replay. External preamble required.
## ASCII only. No producer is invoked or imported by this driver.
## Required preamble: D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_RUN:=true;;
#############################################################################

if not IsBound(D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_RUN) or
   D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_RUN<>true then
  Error("task467 driver: external preamble required");
fi;

D467Checker:="crosscheck/check_d972_r07_a0_dual_anchored_active_batch_recovered_v2.py";;
D467CheckerBytes:=14442;;
D467CheckerSHA:="1d1080cd3e130d987316feefd820215f495cd632aa5eca764fd2f8997f0c424";;
D467ReleaseURL:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9808605601_gap-run-out.rank99.zip";;
D467Zip:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v1.zip";;
D467ZipBytes:=27959;;
D467ZipSHA:="d707cf2553fae24863362d581ba4c09709c629a977ff772d95877dd18fdd5f48";;
D467Extract:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v1_archive";;
D467Work:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_rank99_v1_work";;
D467Artifact:="d972_r07_a0_dual_anchored_active_batch_v1.json";;
D467Checkpoint:="d972_r07_a0_dual_anchored_active_batch_v1_output.checkpoint";;
D467CheckerHistoricalLog:="d972_r07_a0_dual_anchored_active_batch_v1_checker.log";;
D467ProducerLog:="d972_r07_a0_dual_anchored_active_batch_v1_producer.log";;
D467DriverHistorical:="driver.g";;
D467RunLog:="run.log";;
D467CheckerLog:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v1_checker.log";;
D467Receipt:="ci/out/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v1_receipt.txt";;
D467Pass:="R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_V2_CHECKER_PASS";;
D467FinalPass:="R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_GHA_DRIVER_PASS";;
D467WallSeconds:=6600;;
D467RSSBytes:=4800000000;;
D467RSSKilobytes:=4687500;;
D467RunID:="33512607989";;
D467ArtifactID:="9808605601";;
D467ArtifactName:="gap-run-out";;
D467HeadSHA:="3316809e483223ec571ca7d6976dc1317c892441";;
D467OriginalArtifactSHA:="fb6b6b776b8b288952196f400a0d32d57fd2a5ddb9780a7718e55cffee8bafe1";;

D467Files:=[
  [D467Artifact,173930,"5079ddfbffbfc00cac6b2672cbef80f7eb2cce069a2dba87aa04e7cbc420c29a"],
  [D467CheckerHistoricalLog,5595,"83378497196b198ef257c4918eedf103baa3532ec71675f2a15d4a5a65db3e91"],
  [D467Checkpoint,173082,"bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358"],
  [D467ProducerLog,3898,"ef366c147651cf011c16e676878a267dd5d85494d949ff02228f43c6004307af"],
  [D467DriverHistorical,125,"28802be0e11aad96494eaa266baed0c5b7aa9d85add29bf04a7d7d6db67f67c8"],
  [D467RunLog,9493,"075f3db302e3f7ee98d826cbe8b67fcbcf9355472b18322ccb29fb78a510af2a"]
];;

D467Read:=function(path,label)
  local raw;
  raw:=StringFile(path);
  if raw=fail then Error("task467 driver: missing ",label," ",path); fi;
  return raw;
end;;
D467Pin:=function(path,bytes,digest,label)
  local raw;
  raw:=D467Read(path,label);
  if Length(raw)<>bytes or HexSHA256(raw)<>digest then
    Error("task467 driver: pin drift ",label);
  fi;
  return raw;
end;;
D467Count:=function(raw,needle)
  local at,count;
  count:=0;; at:=PositionSublist(raw,needle);
  while at<>fail do
    count:=count+1;; at:=PositionSublist(raw,needle,at+1);
  od;
  return count;
end;;
D467ShellQuote:=function(path)
  if PositionSublist(path,"'")<>fail or PositionSublist(path,"\n")<>fail or
     PositionSublist(path,"\r")<>fail then Error("task467 driver: unsafe path"); fi;
  return Concatenation("'",path,"'");
end;;
D467ExtractMember:=function(name)
  local path;
  if PositionSublist(name,"/")<>fail or PositionSublist(name,"\\")<>fail or
     PositionSublist(name,"..")<>fail or Length(name)=0 then
    Error("task467 driver: unsafe archive member");
  fi;
  path:=Concatenation(D467Extract,"/",name);
  if PositionSublist(path,Concatenation(D467Extract,"/"))<>1 then
    Error("task467 driver: archive member escaped extract root");
  fi;
  return path;
end;;

if Length(D467Files)<>6 then Error("task467 driver: six-file manifest required"); fi;
if D467RunID<>"33512607989" or D467ArtifactID<>"9808605601" or
   D467ArtifactName<>"gap-run-out" or
   D467HeadSHA<>"3316809e483223ec571ca7d6976dc1317c892441" then
  Error("task467 driver: production binding drift");
fi;
if D467OriginalArtifactSHA<>"fb6b6b776b8b288952196f400a0d32d57fd2a5ddb9780a7718e55cffee8bafe1" then
  Error("task467 driver: original artifact digest drift");
fi;
D467Pin(D467Checker,D467CheckerBytes,D467CheckerSHA,"recovered checker");;
if not IsDirectoryPath("ci/out") then
  if CreateDir("ci/out")=fail then Error("task467 driver: ci/out create failed"); fi;
fi;
if IsExistingFile(D467Zip) or IsDirectoryPath(D467Extract) or
   IsDirectoryPath(D467Work) or IsExistingFile(D467CheckerLog) or
   IsExistingFile(D467Receipt) then
  Error("task467 driver: owned output path is not fresh");
fi;
if PositionSublist(D467Extract,"ci/out/")<>1 or
   PositionSublist(D467Work,"ci/out/")<>1 or D467Extract=D467Work then
  Error("task467 driver: dedicated roots required");
fi;

D467Download:=Concatenation(
  "set -euo pipefail; command -v curl >/dev/null; command -v unzip >/dev/null; ",
  "command -v sha256sum >/dev/null; command -v timeout >/dev/null; ",
  "curl --fail --location --silent --show-error \"",D467ReleaseURL,
  "\" --output \"",D467Zip,"\"; ",
  "test \"$(wc -c < \"",D467Zip,"\" | tr -d [:space:])\" = \"",String(D467ZipBytes),"\"; ",
  "test \"$(sha256sum \"",D467Zip,"\" | cut -d \" \" -f1)\" = \"",D467ZipSHA,"\"; ",
  "mkdir \"",D467Extract,"\"; unzip -q \"",D467Zip,"\" -d \"",D467Extract,"\"; ",
  "mkdir -p \"",D467Work,"/ci/out\"; ",
  "test \"$(wc -c < \"",D467Extract,"/",D467Checkpoint,"\" | tr -d [:space:])\" = \"173082\"; ",
  "test \"$(sha256sum \"",D467Extract,"/",D467Checkpoint,"\" | cut -d \" \" -f1)\" = \"",
  "bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358\"; ",
  "cp \"",D467Extract,"/",D467Checkpoint,"\" \"",D467Work,"/ci/out/",D467Checkpoint,"\"; ",
  "test \"$(wc -c < \"",D467Work,"/ci/out/",D467Checkpoint,"\" | tr -d [:space:])\" = \"173082\"; ",
  "test \"$(sha256sum \"",D467Work,"/ci/out/",D467Checkpoint,"\" | cut -d \" \" -f1)\" = \"",
  "bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358\"; ",
  "cd \"",D467Work,"\"; ulimit -v ",String(D467RSSKilobytes),"; ",
  "timeout --foreground --signal=TERM --kill-after=60s ",String(D467WallSeconds),
  "s python3 -u -B ../../../",D467Checker," ../",D467Extract,"/",D467Artifact,
  " > ../d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_v1_checker.log 2>&1"
);;
Exec(Concatenation("bash -o pipefail -c ",D467ShellQuote(D467Download)));;

D467ZipRaw:=D467Pin(D467Zip,D467ZipBytes,D467ZipSHA,"release zip");;
for D467Row in D467Files do
  D467Pin(D467ExtractMember(D467Row[1]),D467Row[2],D467Row[3],D467Row[1]);
od;
D467Copied:=D467Pin(Concatenation(D467Work,"/ci/out/",D467Checkpoint),173082,
  "bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358",
  "working checkpoint copy");;
D467CheckerRaw:=D467Read(D467CheckerLog,"checker log");;
if Length(D467CheckerRaw)=0 then
  Error("task467 driver: checker log unreadable");
fi;
if D467Count(D467CheckerRaw,"Traceback (most recent call last):")<>0 or
   D467Count(D467CheckerRaw,D467Pass)<>1 or
   Length(D467CheckerRaw)<>Length(D467Pass)+1 or
   D467CheckerRaw<>Concatenation(D467Pass,"\n") then
  Error("task467 driver: exactly one recovered-v2 PASS required");
fi;

D467ReceiptText:=Concatenation(
  "schema=d972-r07-a0-dual-anchored-active-batch-recovered-checker-only/v1\n",
  "production_run_id=",D467RunID,"\nartifact_id=",D467ArtifactID,"\nartifact_name=",D467ArtifactName,"\nhead_sha=",D467HeadSHA,"\n",
  "original_artifact_sha256=",D467OriginalArtifactSHA,"\nrelease_url=",D467ReleaseURL,"\n",
  "release_bytes=",String(D467ZipBytes),"\nrelease_sha256=",D467ZipSHA,"\n",
  "checker_path=",D467Checker,"\nchecker_bytes=",String(D467CheckerBytes),"\nchecker_sha256=",D467CheckerSHA,"\n",
  "checker_log_bytes=",String(Length(D467CheckerRaw)),"\nchecker_log_sha256=",HexSHA256(D467CheckerRaw),"\n",
  "wall_seconds=",String(D467WallSeconds),"\nrss_bytes=",String(D467RSSBytes),"\n",
  "checker_exit_code=0\npass_marker=",D467Pass,"\npass_count=1\n",
  "archive_extract=",D467Extract,"\nworking_directory=",D467Work,"\n",
  "rank99_full_semantic_replay_pass=true\n");;
D467ReceiptStream:=OutputTextFile(D467Receipt,false);;
if D467ReceiptStream=fail then Error("task467 driver: receipt open failed"); fi;
SetPrintFormattingStatus(D467ReceiptStream,false);;PrintTo(D467ReceiptStream,D467ReceiptText);;CloseStream(D467ReceiptStream);;
if D467Read(D467Receipt,"receipt")<>D467ReceiptText then Error("task467 driver: receipt readback"); fi;
Print("",D467FinalPass," mode=checker-only process_count=1 checker_exit_code=0\n");
