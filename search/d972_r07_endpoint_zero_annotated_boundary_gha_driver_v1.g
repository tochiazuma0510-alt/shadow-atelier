#############################################################################
## Task378 annotated PB boundary compiler driver. ASCII only.
#############################################################################
if not IsBound(D378Mode) then Error("task378 MODE required"); fi;
if D378Mode<>"PRODUCTION" then Error("task378 production-only mode"); fi;
if not IsBound(D378ParentReceipt) then
  Error("task378 parent receipt required");
fi;
if not IsBound(D378ParentVerdict) then
  Error("task378 parent verdict required");
fi;
if not IsBound(D378ParentCheckpoint) then
  Error("task378 parent checkpoint required");
fi;
if not IsBound(D378ParentA5Sidecar) then
  Error("task378 parent A5 sidecar required");
fi;
if not IsBound(D378Cadence) then D378Cadence:=256; fi;
if not IsBound(D378Seconds) then D378Seconds:=14400; fi;
if not IsBound(D378RSSBytes) then D378RSSBytes:=5000000000; fi;
if not IsBound(D378Operations) then D378Operations:=2000000000; fi;
if not IsBound(D378CheckpointBytes) then
  D378CheckpointBytes:=2000000000;
fi;
if not IsInt(D378Cadence) or D378Cadence<=0 then
  Error("task378 bad cadence");
fi;
if not IsInt(D378Seconds) or D378Seconds<=0 then
  Error("task378 bad seconds");
fi;
if not IsInt(D378RSSBytes) or D378RSSBytes<=0 then
  Error("task378 bad RSS cap");
fi;
if not IsInt(D378Operations) or D378Operations<=0 then
  Error("task378 bad operation cap");
fi;
if not IsInt(D378CheckpointBytes) or D378CheckpointBytes<=0 then
  Error("task378 bad checkpoint cap");
fi;

D378Producer:="search/d972_r07_endpoint_zero_annotated_boundary_v1.py";;
D378Checker:="crosscheck/check_d972_r07_endpoint_zero_annotated_boundary_v1.py";;
D378ProducerBytes:=79194;;
D378ProducerSHA:="c6e4b0d99ed79f9eabedf225c964a598b2f21b3ab10758cb9d5f83a60ceb5d11";;
D378CheckerBytes:=45525;;
D378CheckerSHA:="719f1b97b793599a0a6013512636c346dc00fbd6f445ecb6b93ef1b0d685d717";;
D378Receipt:="ci/out/d972_r07_endpoint_zero_annotated_boundary_v1.json";;
D378Verdict:="ci/out/d972_r07_endpoint_zero_annotated_boundary_v1.checker.json";;
D378Checkpoint:="ci/out/d972_r07_endpoint_zero_annotated_boundary_v1.checkpoint.json";;
D378ProgressLog:="ci/out/d972_r07_endpoint_zero_annotated_boundary_v1.progress.log";;
D378CheckerLog:="ci/out/d972_r07_endpoint_zero_annotated_boundary_v1.checker.log";;
D378Script:="ci/out/d972_r07_endpoint_zero_annotated_boundary_v1.sh";;
D378OK:="ci/out/d972_r07_endpoint_zero_annotated_boundary_v1.ok";;

D378SafePath:=function(path,area)
  local bad;
  if not IsString(path) or Length(path)<=Length(area) or
     path{[1..Length(area)]}<>area then
    return false;
  fi;
  for bad in [" ","'","\"",";","&","|","$","(",")","<",">"] do
    if Position(path,bad[1])<>fail then return false; fi;
  od;
  if Position(path,CharInt(96))<>fail then return false; fi;
  return true;
end;;

D378SafeInput:=function(path)
  return D378SafePath(path,"ci/in/") or D378SafePath(path,"ci/out/");
end;;

for D378Path in [D378ParentReceipt,D378ParentVerdict,
                 D378ParentCheckpoint,D378ParentA5Sidecar] do
  if not D378SafeInput(D378Path) then
    Error("task378 bad parent path ",D378Path);
  fi;
od;

D378ResumeBound:=IsBound(D378ResumePath);;
if D378ResumeBound<>IsBound(D378ResumeBytes) or
   D378ResumeBound<>IsBound(D378ResumeSHA) then
  Error("task378 resume path/bytes/SHA must be all-or-none");
fi;
D378ResumeArgs:="";;
if D378ResumeBound then
  if not D378SafeInput(D378ResumePath) then
    Error("task378 bad resume path");
  fi;
  if not IsInt(D378ResumeBytes) or D378ResumeBytes<=0 then
    Error("task378 bad resume bytes");
  fi;
  if not IsString(D378ResumeSHA) or Length(D378ResumeSHA)<>64 then
    Error("task378 bad resume SHA");
  fi;
  D378ResumeArgs:=Concatenation(" --resume-path ",D378ResumePath,
    " --resume-bytes ",String(D378ResumeBytes),
    " --resume-sha256 ",D378ResumeSHA);
fi;

for D378Path in [D378Receipt,D378Verdict,D378Checkpoint,
                 D378ProgressLog,D378CheckerLog,D378Script,D378OK] do
  if IsExistingFile(D378Path) then Error("task378 stale output ",D378Path); fi;
od;
Exec("mkdir -p ci/out");;
D378S:=OutputTextFile(D378Script,false);;
if D378S=fail then Error("task378 script open"); fi;
SetPrintFormattingStatus(D378S,false);;
PrintTo(D378S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D378S,"test \"$(wc -c < ",D378Producer,")\" = \"",
  String(D378ProducerBytes),"\"\n");;
PrintTo(D378S,"test \"$(sha256sum ",D378Producer,
  " | awk '{print $1}')\" = \"",D378ProducerSHA,"\"\n");;
PrintTo(D378S,"test \"$(wc -c < ",D378Checker,")\" = \"",
  String(D378CheckerBytes),"\"\n");;
PrintTo(D378S,"test \"$(sha256sum ",D378Checker,
  " | awk '{print $1}')\" = \"",D378CheckerSHA,"\"\n");;
PrintTo(D378S,"python3 -u -B ",D378Producer,
  " --mode PRODUCTION --parent-receipt ",D378ParentReceipt,
  " --parent-verdict ",D378ParentVerdict,
  " --parent-checkpoint ",D378ParentCheckpoint,
  " --parent-a5-sidecar ",D378ParentA5Sidecar,
  " --output ",D378Receipt,
  " --checkpoint ",D378Checkpoint,
  " --cadence ",String(D378Cadence),
  " --seconds ",String(D378Seconds),
  " --rss-bytes ",String(D378RSSBytes),
  " --max-operations ",String(D378Operations),
  " --checkpoint-bytes ",String(D378CheckpointBytes),D378ResumeArgs,
  " > ",D378ProgressLog," 2>&1\n");;
PrintTo(D378S,"cat ",D378ProgressLog,"\n");;
PrintTo(D378S,"p=$(sed -n 's/^R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_V1_PRODUCER_TERMINAL //p' ",
  D378ProgressLog,")\n");;
PrintTo(D378S,"case \"$p\" in R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_MEMBER|UNKNOWN_INPUT:*|UNKNOWN_RESOURCE:*) ;; *) exit 1;; esac\n");;
PrintTo(D378S,"test -s ",D378Receipt," && test -s ",D378Checkpoint,"\n");;
PrintTo(D378S,"if test \"$p\" = R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_MEMBER; then\n");;
PrintTo(D378S,"  python3 -u -B ",D378Checker,
  " --mode PRODUCTION --parent-receipt ",D378ParentReceipt,
  " --parent-verdict ",D378ParentVerdict,
  " --parent-checkpoint ",D378ParentCheckpoint,
  " --parent-a5-sidecar ",D378ParentA5Sidecar,
  " --receipt ",D378Receipt,
  " --checkpoint ",D378Checkpoint,
  " --output ",D378Verdict,
  " > ",D378CheckerLog," 2>&1\n");;
PrintTo(D378S,"  cat ",D378CheckerLog,"\n");;
PrintTo(D378S,"  c=$(sed -n 's/^R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_V1_CHECKER terminal=//p' ",
  D378CheckerLog,")\n");;
PrintTo(D378S,"  test \"$c\" = \"$p\"\n");;
PrintTo(D378S,"  grep -Fq '\"status\":\"ACCEPTED\"' ",D378Verdict,"\n");;
PrintTo(D378S,"  grep -Fq '\"terminal\":\"R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_MEMBER\"' ",
  D378Verdict,"\n");;
PrintTo(D378S,"else\n");;
PrintTo(D378S,"  test ! -e ",D378Verdict," && test ! -e ",D378CheckerLog,"\n");;
PrintTo(D378S,"fi\n");;
PrintTo(D378S,"printf '%s\\n' \"R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_V1_DRIVER_COMPLETE terminal=$p\" > ",
  D378OK,"\n");;
CloseStream(D378S);;
Exec(Concatenation("bash ",D378Script));;
if not IsExistingFile(D378OK) then Error("task378 missing success marker"); fi;
Print("R07_ENDPOINT_ZERO_ANNOTATED_BOUNDARY_V1_DRIVER_COMPLETE\n");;
