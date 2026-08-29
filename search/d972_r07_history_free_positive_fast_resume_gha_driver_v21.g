#############################################################################
## A0 v21 actual-resume production driver. ASCII only; fail closed.
#############################################################################
D374Producer:="search/d972_r07_history_free_positive_fast_resume_v21.py";;
D374ProducerBytes:=3035;;
D374ProducerSHA:="18aef3a1619b076b32002a9083ba9763116d984b761b7f8d181059293dbdf1fd";;
D374Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v21.py";;
D374CheckerBytes:=2027;;
D374CheckerSHA:="a2d913328fef890477305ae5b2cec6978c0dc3882e7c47af35d3444ac16f7c22";;
D374Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D374Manifest:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json";;
D374Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
# Keep the v20 source pathname exactly: restore_checkpoint binds source.path.
D374Raw:="ci/resume/d972_r07_history_free_positive_fast_resume_v20.raw.json";;
D374Base:="ci/out/d972_r07_history_free_positive_fast_resume_v21_production";;
D374Receipt:=Concatenation(D374Base,".json");;
D374Checkpoint:=Concatenation(D374Receipt,".checkpoint.json");;
D374Verdict:=Concatenation(D374Base,".verdict.json");;
D374ProducerLog:=Concatenation(D374Base,".producer.log");;
D374CheckerLog:=Concatenation(D374Base,".checker.log");;
D374ProducerTerminal:=Concatenation(D374Base,".producer.terminal");;
D374CheckerTerminal:=Concatenation(D374Base,".checker.terminal");;
D374Shell:=Concatenation(D374Base,".sh");;
D374OK:=Concatenation(D374Base,".ok");;
D374Common:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD";;
D374ProducerPrefix:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_PRODUCER_TERMINAL";;
D374CheckerPrefix:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_CHECKER_TERMINAL";;
D374Sentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V21_DRIVER_PASS";;

D374ResumeBindings:=[IsBound(D374ResumePath),IsBound(D374ResumeBytes),
                     IsBound(D374ResumeSHA)];;
D374ResumeCount:=Number(D374ResumeBindings,x->x=true);;
if D374ResumeCount=0 then
  D374ResumeEnabled:=false;;
elif D374ResumeCount=3 then
  D374ResumeEnabled:=true;;
else
  Error("task374 resume path/bytes/SHA must be all specified or all absent");
fi;

D374Safe:=function(path)
  local bad;
  if not IsString(path) or Length(path)<7 or path{[1..7]}<>"ci/in/" then
    return false;
  fi;
  for bad in [" ","'","\"",";","&","|","`","$","(",")","<",">"] do
    if Position(path,bad[1])<>fail then return false; fi;
  od;
  return true;
end;;
D374LowerHex:=function(value)
  local c;
  if not IsString(value) or Length(value)<>64 then return false; fi;
  for c in value do
    if Position("0123456789abcdef",c)=fail then return false; fi;
  od;
  return true;
end;;
if D374ResumeEnabled then
  if not D374Safe(D374ResumePath) or not IsInt(D374ResumeBytes) or
     D374ResumeBytes<=0 or not D374LowerHex(D374ResumeSHA) then
    Error("task374 invalid resume triple");
  fi;
fi;

for D374Path in [D374Receipt,D374Checkpoint,D374Verdict,D374ProducerLog,
                 D374CheckerLog,D374ProducerTerminal,D374CheckerTerminal,
                 D374Shell,D374OK,D374Raw] do
  if IsExistingFile(D374Path) then Error("task374 stale output ",D374Path); fi;
od;

Exec("mkdir -p ci/out ci/resume");;
D374Stream:=OutputTextFile(D374Shell,false);;
if D374Stream=fail then Error("task374 shell open"); fi;
SetPrintFormattingStatus(D374Stream,false);;
PrintTo(D374Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D374Stream,"for command in python3 timeout tee grep sed cmp wc sha256sum unzip; do command -v \"$command\" >/dev/null; done\n");
PrintTo(D374Stream,"test \"$(wc -c < ",D374Producer,
  ")\" = \"",String(D374ProducerBytes),"\"\n");
PrintTo(D374Stream,"test \"$(sha256sum ",D374Producer,
  " | awk '{print $1}')\" = \"",D374ProducerSHA,"\"\n");
PrintTo(D374Stream,"test \"$(wc -c < ",D374Checker,
  ")\" = \"",String(D374CheckerBytes),"\"\n");
PrintTo(D374Stream,"test \"$(sha256sum ",D374Checker,
  " | awk '{print $1}')\" = \"",D374CheckerSHA,"\"\n");
PrintTo(D374Stream,"test \"$(wc -c < ",D374Zip,")\" = \"5001811\"\n");
PrintTo(D374Stream,"test \"$(sha256sum ",D374Zip,
  " | awk '{print $1}')\" = \"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566\"\n");
PrintTo(D374Stream,"test \"$(wc -c < ",D374Manifest,")\" = \"1328\"\n");
PrintTo(D374Stream,"test \"$(sha256sum ",D374Manifest,
  " | awk '{print $1}')\" = \"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302\"\n");
if D374ResumeEnabled then
  PrintTo(D374Stream,"test \"$(wc -c < ",D374ResumePath,")\" = \"",
    String(D374ResumeBytes),"\"\n");
  PrintTo(D374Stream,"test \"$(sha256sum ",D374ResumePath,
    " | awk '{print $1}')\" = \"",D374ResumeSHA,"\"\n");
fi;
PrintTo(D374Stream,"unzip -p ",D374Zip," ",D374Member," > ",D374Raw,"\n");
PrintTo(D374Stream,"test \"$(wc -c < ",D374Raw,")\" = \"86368039\"\n");
PrintTo(D374Stream,"test \"$(sha256sum ",D374Raw,
  " | awk '{print $1}')\" = \"c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab\"\n");
PrintTo(D374Stream,"set +e\n");
PrintTo(D374Stream,"timeout --foreground 11100s python3 -u -B ",D374Producer,
  " --mode PRODUCTION --source ",D374Raw,
  " --manifest ",D374Manifest," --output ",D374Receipt,
  " --seconds 10800 --workers 2");
if D374ResumeEnabled then PrintTo(D374Stream," --resume ",D374ResumePath); fi;
PrintTo(D374Stream," 2>&1 | tee ",D374ProducerLog,"\n");
PrintTo(D374Stream,"producer_pipeline_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D374Stream,"set -e\n");
PrintTo(D374Stream,"if [ \"$","{producer_pipeline_status[0]}\" -ne 0 ]; then exit \"$","{producer_pipeline_status[0]}\"; fi\n");
PrintTo(D374Stream,"if [ \"$","{producer_pipeline_status[1]}\" -ne 0 ]; then exit \"$","{producer_pipeline_status[1]}\"; fi\n");
PrintTo(D374Stream,"test -s ",D374Receipt," -a -s ",D374ProducerLog,"\n");
PrintTo(D374Stream,"test \"$(grep -c '^",D374ProducerPrefix," ' ",D374ProducerLog,")\" -eq 1\n");
PrintTo(D374Stream,"grep -E '^",D374ProducerPrefix," ' ",D374ProducerLog,
  " | sed 's/^",D374ProducerPrefix," //' > ",D374ProducerTerminal,"\n");
PrintTo(D374Stream,"set +e\n");
PrintTo(D374Stream,"timeout --foreground 7500s python3 -u -B ",D374Checker,
  " --receipt ",D374Receipt," --verdict ",D374Verdict,
  " 2>&1 | tee ",D374CheckerLog,"\n");
PrintTo(D374Stream,"checker_pipeline_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D374Stream,"set -e\n");
PrintTo(D374Stream,"if [ \"$","{checker_pipeline_status[0]}\" -ne 0 ]; then exit \"$","{checker_pipeline_status[0]}\"; fi\n");
PrintTo(D374Stream,"if [ \"$","{checker_pipeline_status[1]}\" -ne 0 ]; then exit \"$","{checker_pipeline_status[1]}\"; fi\n");
PrintTo(D374Stream,"test -s ",D374Verdict," -a -s ",D374CheckerLog,"\n");
PrintTo(D374Stream,"test \"$(grep -c '^",D374CheckerPrefix," ' ",D374CheckerLog,")\" -eq 1\n");
PrintTo(D374Stream,"grep -E '^",D374CheckerPrefix," ' ",D374CheckerLog,
  " | sed 's/^",D374CheckerPrefix," //' > ",D374CheckerTerminal,"\n");
PrintTo(D374Stream,"test \"$(wc -l < ",D374ProducerTerminal,")\" -eq 1\n");
PrintTo(D374Stream,"test \"$(wc -l < ",D374CheckerTerminal,")\" -eq 1\n");
PrintTo(D374Stream,"cmp -s ",D374ProducerTerminal," ",D374CheckerTerminal,"\n");
PrintTo(D374Stream,"terminal=$(tr -d '\\n' < ",D374ProducerTerminal,")\n");
PrintTo(D374Stream,"case \"$terminal\" in\n");
PrintTo(D374Stream,"  ",D374Common,") test ! -e ",D374Checkpoint," ;;\n");
PrintTo(D374Stream,"  UNKNOWN_INPUT:*) [[ \"$terminal\" =~ ^UNKNOWN_INPUT:[-A-Za-z0-9_.=,+:]+$ ]] && test ! -e ",D374Checkpoint," ;;\n");
PrintTo(D374Stream,"  UNKNOWN_RESOURCE:phase=*) [[ \"$terminal\" =~ ^UNKNOWN_RESOURCE:phase=[A-Za-z0-9_]+:cap=[A-Za-z0-9_]+:value=[0-9]+([.][0-9]+)?:limit=[0-9]+([.][0-9]+)?$ ]] && ( test -s ",D374Checkpoint," || grep -Fq '\"checkpoint_required\":false' ",D374Receipt," ) ;;\n");
PrintTo(D374Stream,"  *) exit 1 ;;\n");
PrintTo(D374Stream,"esac\n");
PrintTo(D374Stream,"printf '%s' '",D374Sentinel,"' > ",D374OK,"\n");
CloseStream(D374Stream);;
Exec(Concatenation("bash ",D374Shell));;
D374Observed:=StringFile(D374OK);;
if D374Observed<>D374Sentinel then Error("task374 sentinel mismatch"); fi;
Print(D374Sentinel,"\n");;
