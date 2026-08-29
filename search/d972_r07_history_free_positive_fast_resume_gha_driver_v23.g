#############################################################################
## A0 v23 pre-heavy replacement-worker production driver. ASCII only; fail closed.
#############################################################################
D392Producer:="search/d972_r07_history_free_positive_fast_resume_v23.py";;
D392ProducerBytes:=3729;;
D392ProducerSHA:="0e7ad85d5328b86b57086ca4710520ce748e591e0a0e1cc93cedeba3850fb8f3";;
D392Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v23.py";;
D392CheckerBytes:=2066;;
D392CheckerSHA:="b0e6f447c92cf76f7735c56ce7dc71b2fa7c3a2247abab3962d50ba9e9bb926c";;
D392Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D392Manifest:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json";;
D392Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
# Keep the v20 source pathname exactly: restore_checkpoint binds source.path.
D392Raw:="ci/resume/d972_r07_history_free_positive_fast_resume_v20.raw.json";;
D392Base:="ci/out/d972_r07_history_free_positive_fast_resume_v23_production";;
D392Receipt:=Concatenation(D392Base,".json");;
D392Checkpoint:=Concatenation(D392Receipt,".checkpoint.json");;
D392Verdict:=Concatenation(D392Base,".verdict.json");;
D392ProducerLog:=Concatenation(D392Base,".producer.log");;
D392CheckerLog:=Concatenation(D392Base,".checker.log");;
D392ProducerTerminal:=Concatenation(D392Base,".producer.terminal");;
D392CheckerTerminal:=Concatenation(D392Base,".checker.terminal");;
D392Shell:=Concatenation(D392Base,".sh");;
D392OK:=Concatenation(D392Base,".ok");;
D392Common:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD";;
D392ProducerPrefix:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_PRODUCER_TERMINAL";;
D392CheckerPrefix:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_CHECKER_TERMINAL";;
D392Sentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V23_DRIVER_PASS";;

D392ResumeBindings:=[IsBound(D392ResumePath),IsBound(D392ResumeBytes),
                     IsBound(D392ResumeSHA)];;
D392ResumeCount:=Number(D392ResumeBindings,x->x=true);;
if D392ResumeCount=0 then
  D392ResumeEnabled:=false;;
elif D392ResumeCount=3 then
  D392ResumeEnabled:=true;;
else
  Error("task392 resume path/bytes/SHA must be all specified or all absent");
fi;

D392Safe:=function(path)
  local bad;
  if not IsString(path) or Length(path)<7 or path{[1..7]}<>"ci/in/" then
    return false;
  fi;
  for bad in [" ","'","\"",";","&","|","`","$","(",")","<",">"] do
    if Position(path,bad[1])<>fail then return false; fi;
  od;
  return true;
end;;
D392LowerHex:=function(value)
  local c;
  if not IsString(value) or Length(value)<>64 then return false; fi;
  for c in value do
    if Position("0123456789abcdef",c)=fail then return false; fi;
  od;
  return true;
end;;
if D392ResumeEnabled then
  if not D392Safe(D392ResumePath) or not IsInt(D392ResumeBytes) or
     D392ResumeBytes<=0 or not D392LowerHex(D392ResumeSHA) then
    Error("task392 invalid resume triple");
  fi;
fi;

for D392Path in [D392Receipt,D392Checkpoint,D392Verdict,D392ProducerLog,
                 D392CheckerLog,D392ProducerTerminal,D392CheckerTerminal,
                 D392Shell,D392OK,D392Raw] do
  if IsExistingFile(D392Path) then Error("task392 stale output ",D392Path); fi;
od;

Exec("mkdir -p ci/out ci/resume");;
D392Stream:=OutputTextFile(D392Shell,false);;
if D392Stream=fail then Error("task392 shell open"); fi;
SetPrintFormattingStatus(D392Stream,false);;
PrintTo(D392Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D392Stream,"for command in python3 timeout tee grep sed cmp wc sha256sum unzip; do command -v \"$command\" >/dev/null; done\n");
PrintTo(D392Stream,"test \"$(wc -c < ",D392Producer,
  ")\" = \"",String(D392ProducerBytes),"\"\n");
PrintTo(D392Stream,"test \"$(sha256sum ",D392Producer,
  " | awk '{print $1}')\" = \"",D392ProducerSHA,"\"\n");
PrintTo(D392Stream,"test \"$(wc -c < ",D392Checker,
  ")\" = \"",String(D392CheckerBytes),"\"\n");
PrintTo(D392Stream,"test \"$(sha256sum ",D392Checker,
  " | awk '{print $1}')\" = \"",D392CheckerSHA,"\"\n");
PrintTo(D392Stream,"test \"$(wc -c < ",D392Zip,")\" = \"5001811\"\n");
PrintTo(D392Stream,"test \"$(sha256sum ",D392Zip,
  " | awk '{print $1}')\" = \"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566\"\n");
PrintTo(D392Stream,"test \"$(wc -c < ",D392Manifest,")\" = \"1328\"\n");
PrintTo(D392Stream,"test \"$(sha256sum ",D392Manifest,
  " | awk '{print $1}')\" = \"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302\"\n");
if D392ResumeEnabled then
  PrintTo(D392Stream,"test \"$(wc -c < ",D392ResumePath,")\" = \"",
    String(D392ResumeBytes),"\"\n");
  PrintTo(D392Stream,"test \"$(sha256sum ",D392ResumePath,
    " | awk '{print $1}')\" = \"",D392ResumeSHA,"\"\n");
fi;
PrintTo(D392Stream,"unzip -p ",D392Zip," ",D392Member," > ",D392Raw,"\n");
PrintTo(D392Stream,"test \"$(wc -c < ",D392Raw,")\" = \"86368039\"\n");
PrintTo(D392Stream,"test \"$(sha256sum ",D392Raw,
  " | awk '{print $1}')\" = \"c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab\"\n");
PrintTo(D392Stream,"set +e\n");
PrintTo(D392Stream,"timeout --foreground 11100s python3 -u -B ",D392Producer,
  " --mode PRODUCTION --source ",D392Raw,
  " --manifest ",D392Manifest," --output ",D392Receipt,
  " --seconds 10800 --workers 2");
if D392ResumeEnabled then PrintTo(D392Stream," --resume ",D392ResumePath); fi;
PrintTo(D392Stream," 2>&1 | tee ",D392ProducerLog,"\n");
PrintTo(D392Stream,"producer_pipeline_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D392Stream,"set -e\n");
PrintTo(D392Stream,"if [ \"$","{producer_pipeline_status[0]}\" -ne 0 ]; then exit \"$","{producer_pipeline_status[0]}\"; fi\n");
PrintTo(D392Stream,"if [ \"$","{producer_pipeline_status[1]}\" -ne 0 ]; then exit \"$","{producer_pipeline_status[1]}\"; fi\n");
PrintTo(D392Stream,"test -s ",D392Receipt," -a -s ",D392ProducerLog,"\n");
PrintTo(D392Stream,"test \"$(grep -c '^",D392ProducerPrefix," ' ",D392ProducerLog,")\" -eq 1\n");
PrintTo(D392Stream,"grep -E '^",D392ProducerPrefix," ' ",D392ProducerLog,
  " | sed 's/^",D392ProducerPrefix," //' > ",D392ProducerTerminal,"\n");
PrintTo(D392Stream,"set +e\n");
PrintTo(D392Stream,"timeout --foreground 7500s python3 -u -B ",D392Checker,
  " --receipt ",D392Receipt," --verdict ",D392Verdict,
  " 2>&1 | tee ",D392CheckerLog,"\n");
PrintTo(D392Stream,"checker_pipeline_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D392Stream,"set -e\n");
PrintTo(D392Stream,"if [ \"$","{checker_pipeline_status[0]}\" -ne 0 ]; then exit \"$","{checker_pipeline_status[0]}\"; fi\n");
PrintTo(D392Stream,"if [ \"$","{checker_pipeline_status[1]}\" -ne 0 ]; then exit \"$","{checker_pipeline_status[1]}\"; fi\n");
PrintTo(D392Stream,"test -s ",D392Verdict," -a -s ",D392CheckerLog,"\n");
PrintTo(D392Stream,"test \"$(grep -c '^",D392CheckerPrefix," ' ",D392CheckerLog,")\" -eq 1\n");
PrintTo(D392Stream,"grep -E '^",D392CheckerPrefix," ' ",D392CheckerLog,
  " | sed 's/^",D392CheckerPrefix," //' > ",D392CheckerTerminal,"\n");
PrintTo(D392Stream,"test \"$(wc -l < ",D392ProducerTerminal,")\" -eq 1\n");
PrintTo(D392Stream,"test \"$(wc -l < ",D392CheckerTerminal,")\" -eq 1\n");
PrintTo(D392Stream,"cmp -s ",D392ProducerTerminal," ",D392CheckerTerminal,"\n");
PrintTo(D392Stream,"terminal=$(tr -d '\\n' < ",D392ProducerTerminal,")\n");
PrintTo(D392Stream,"case \"$terminal\" in\n");
PrintTo(D392Stream,"  ",D392Common,") test ! -e ",D392Checkpoint," ;;\n");
PrintTo(D392Stream,"  UNKNOWN_INPUT:*) [[ \"$terminal\" =~ ^UNKNOWN_INPUT:[-A-Za-z0-9_.=,+:]+$ ]] && test ! -e ",D392Checkpoint," ;;\n");
PrintTo(D392Stream,"  UNKNOWN_RESOURCE:phase=*) [[ \"$terminal\" =~ ^UNKNOWN_RESOURCE:phase=[A-Za-z0-9_]+:cap=[A-Za-z0-9_]+:value=[0-9]+([.][0-9]+)?:limit=[0-9]+([.][0-9]+)?$ ]] && ( test -s ",D392Checkpoint," || grep -Fq '\"checkpoint_required\":false' ",D392Receipt," ) ;;\n");
PrintTo(D392Stream,"  *) exit 1 ;;\n");
PrintTo(D392Stream,"esac\n");
PrintTo(D392Stream,"printf '%s' '",D392Sentinel,"' > ",D392OK,"\n");
CloseStream(D392Stream);;
Exec(Concatenation("bash ",D392Shell));;
D392Observed:=StringFile(D392OK);;
if D392Observed<>D392Sentinel then Error("task392 sentinel mismatch"); fi;
Print(D392Sentinel,"\n");;
