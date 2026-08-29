#############################################################################
## A0 v22 terminal-checkpoint production driver. ASCII only; fail closed.
#############################################################################
D380Producer:="search/d972_r07_history_free_positive_fast_resume_v22.py";;
D380ProducerBytes:=3280;;
D380ProducerSHA:="1cc875afb05b7c3db189d7a77fd6d9d4e2604610a0af6a383895011ecbdd0d01";;
D380Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v22.py";;
D380CheckerBytes:=2066;;
D380CheckerSHA:="4c79b841b5ce003e4d2eefaf1320e878aab400c20ef1a23e4f2900ea61e5cf13";;
D380Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D380Manifest:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json";;
D380Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
# Keep the v20 source pathname exactly: restore_checkpoint binds source.path.
D380Raw:="ci/resume/d972_r07_history_free_positive_fast_resume_v20.raw.json";;
D380Base:="ci/out/d972_r07_history_free_positive_fast_resume_v22_production";;
D380Receipt:=Concatenation(D380Base,".json");;
D380Checkpoint:=Concatenation(D380Receipt,".checkpoint.json");;
D380Verdict:=Concatenation(D380Base,".verdict.json");;
D380ProducerLog:=Concatenation(D380Base,".producer.log");;
D380CheckerLog:=Concatenation(D380Base,".checker.log");;
D380ProducerTerminal:=Concatenation(D380Base,".producer.terminal");;
D380CheckerTerminal:=Concatenation(D380Base,".checker.terminal");;
D380Shell:=Concatenation(D380Base,".sh");;
D380OK:=Concatenation(D380Base,".ok");;
D380Common:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD";;
D380ProducerPrefix:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_PRODUCER_TERMINAL";;
D380CheckerPrefix:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_CHECKER_TERMINAL";;
D380Sentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V22_DRIVER_PASS";;

D380ResumeBindings:=[IsBound(D380ResumePath),IsBound(D380ResumeBytes),
                     IsBound(D380ResumeSHA)];;
D380ResumeCount:=Number(D380ResumeBindings,x->x=true);;
if D380ResumeCount=0 then
  D380ResumeEnabled:=false;;
elif D380ResumeCount=3 then
  D380ResumeEnabled:=true;;
else
  Error("task380 resume path/bytes/SHA must be all specified or all absent");
fi;

D380Safe:=function(path)
  local bad;
  if not IsString(path) or Length(path)<7 or path{[1..7]}<>"ci/in/" then
    return false;
  fi;
  for bad in [" ","'","\"",";","&","|","`","$","(",")","<",">"] do
    if Position(path,bad[1])<>fail then return false; fi;
  od;
  return true;
end;;
D380LowerHex:=function(value)
  local c;
  if not IsString(value) or Length(value)<>64 then return false; fi;
  for c in value do
    if Position("0123456789abcdef",c)=fail then return false; fi;
  od;
  return true;
end;;
if D380ResumeEnabled then
  if not D380Safe(D380ResumePath) or not IsInt(D380ResumeBytes) or
     D380ResumeBytes<=0 or not D380LowerHex(D380ResumeSHA) then
    Error("task380 invalid resume triple");
  fi;
fi;

for D380Path in [D380Receipt,D380Checkpoint,D380Verdict,D380ProducerLog,
                 D380CheckerLog,D380ProducerTerminal,D380CheckerTerminal,
                 D380Shell,D380OK,D380Raw] do
  if IsExistingFile(D380Path) then Error("task380 stale output ",D380Path); fi;
od;

Exec("mkdir -p ci/out ci/resume");;
D380Stream:=OutputTextFile(D380Shell,false);;
if D380Stream=fail then Error("task380 shell open"); fi;
SetPrintFormattingStatus(D380Stream,false);;
PrintTo(D380Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D380Stream,"for command in python3 timeout tee grep sed cmp wc sha256sum unzip; do command -v \"$command\" >/dev/null; done\n");
PrintTo(D380Stream,"test \"$(wc -c < ",D380Producer,
  ")\" = \"",String(D380ProducerBytes),"\"\n");
PrintTo(D380Stream,"test \"$(sha256sum ",D380Producer,
  " | awk '{print $1}')\" = \"",D380ProducerSHA,"\"\n");
PrintTo(D380Stream,"test \"$(wc -c < ",D380Checker,
  ")\" = \"",String(D380CheckerBytes),"\"\n");
PrintTo(D380Stream,"test \"$(sha256sum ",D380Checker,
  " | awk '{print $1}')\" = \"",D380CheckerSHA,"\"\n");
PrintTo(D380Stream,"test \"$(wc -c < ",D380Zip,")\" = \"5001811\"\n");
PrintTo(D380Stream,"test \"$(sha256sum ",D380Zip,
  " | awk '{print $1}')\" = \"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566\"\n");
PrintTo(D380Stream,"test \"$(wc -c < ",D380Manifest,")\" = \"1328\"\n");
PrintTo(D380Stream,"test \"$(sha256sum ",D380Manifest,
  " | awk '{print $1}')\" = \"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302\"\n");
if D380ResumeEnabled then
  PrintTo(D380Stream,"test \"$(wc -c < ",D380ResumePath,")\" = \"",
    String(D380ResumeBytes),"\"\n");
  PrintTo(D380Stream,"test \"$(sha256sum ",D380ResumePath,
    " | awk '{print $1}')\" = \"",D380ResumeSHA,"\"\n");
fi;
PrintTo(D380Stream,"unzip -p ",D380Zip," ",D380Member," > ",D380Raw,"\n");
PrintTo(D380Stream,"test \"$(wc -c < ",D380Raw,")\" = \"86368039\"\n");
PrintTo(D380Stream,"test \"$(sha256sum ",D380Raw,
  " | awk '{print $1}')\" = \"c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab\"\n");
PrintTo(D380Stream,"set +e\n");
PrintTo(D380Stream,"timeout --foreground 11100s python3 -u -B ",D380Producer,
  " --mode PRODUCTION --source ",D380Raw,
  " --manifest ",D380Manifest," --output ",D380Receipt,
  " --seconds 10800 --workers 2");
if D380ResumeEnabled then PrintTo(D380Stream," --resume ",D380ResumePath); fi;
PrintTo(D380Stream," 2>&1 | tee ",D380ProducerLog,"\n");
PrintTo(D380Stream,"producer_pipeline_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D380Stream,"set -e\n");
PrintTo(D380Stream,"if [ \"$","{producer_pipeline_status[0]}\" -ne 0 ]; then exit \"$","{producer_pipeline_status[0]}\"; fi\n");
PrintTo(D380Stream,"if [ \"$","{producer_pipeline_status[1]}\" -ne 0 ]; then exit \"$","{producer_pipeline_status[1]}\"; fi\n");
PrintTo(D380Stream,"test -s ",D380Receipt," -a -s ",D380ProducerLog,"\n");
PrintTo(D380Stream,"test \"$(grep -c '^",D380ProducerPrefix," ' ",D380ProducerLog,")\" -eq 1\n");
PrintTo(D380Stream,"grep -E '^",D380ProducerPrefix," ' ",D380ProducerLog,
  " | sed 's/^",D380ProducerPrefix," //' > ",D380ProducerTerminal,"\n");
PrintTo(D380Stream,"set +e\n");
PrintTo(D380Stream,"timeout --foreground 7500s python3 -u -B ",D380Checker,
  " --receipt ",D380Receipt," --verdict ",D380Verdict,
  " 2>&1 | tee ",D380CheckerLog,"\n");
PrintTo(D380Stream,"checker_pipeline_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D380Stream,"set -e\n");
PrintTo(D380Stream,"if [ \"$","{checker_pipeline_status[0]}\" -ne 0 ]; then exit \"$","{checker_pipeline_status[0]}\"; fi\n");
PrintTo(D380Stream,"if [ \"$","{checker_pipeline_status[1]}\" -ne 0 ]; then exit \"$","{checker_pipeline_status[1]}\"; fi\n");
PrintTo(D380Stream,"test -s ",D380Verdict," -a -s ",D380CheckerLog,"\n");
PrintTo(D380Stream,"test \"$(grep -c '^",D380CheckerPrefix," ' ",D380CheckerLog,")\" -eq 1\n");
PrintTo(D380Stream,"grep -E '^",D380CheckerPrefix," ' ",D380CheckerLog,
  " | sed 's/^",D380CheckerPrefix," //' > ",D380CheckerTerminal,"\n");
PrintTo(D380Stream,"test \"$(wc -l < ",D380ProducerTerminal,")\" -eq 1\n");
PrintTo(D380Stream,"test \"$(wc -l < ",D380CheckerTerminal,")\" -eq 1\n");
PrintTo(D380Stream,"cmp -s ",D380ProducerTerminal," ",D380CheckerTerminal,"\n");
PrintTo(D380Stream,"terminal=$(tr -d '\\n' < ",D380ProducerTerminal,")\n");
PrintTo(D380Stream,"case \"$terminal\" in\n");
PrintTo(D380Stream,"  ",D380Common,") test ! -e ",D380Checkpoint," ;;\n");
PrintTo(D380Stream,"  UNKNOWN_INPUT:*) [[ \"$terminal\" =~ ^UNKNOWN_INPUT:[-A-Za-z0-9_.=,+:]+$ ]] && test ! -e ",D380Checkpoint," ;;\n");
PrintTo(D380Stream,"  UNKNOWN_RESOURCE:phase=*) [[ \"$terminal\" =~ ^UNKNOWN_RESOURCE:phase=[A-Za-z0-9_]+:cap=[A-Za-z0-9_]+:value=[0-9]+([.][0-9]+)?:limit=[0-9]+([.][0-9]+)?$ ]] && ( test -s ",D380Checkpoint," || grep -Fq '\"checkpoint_required\":false' ",D380Receipt," ) ;;\n");
PrintTo(D380Stream,"  *) exit 1 ;;\n");
PrintTo(D380Stream,"esac\n");
PrintTo(D380Stream,"printf '%s' '",D380Sentinel,"' > ",D380OK,"\n");
CloseStream(D380Stream);;
Exec(Concatenation("bash ",D380Shell));;
D380Observed:=StringFile(D380OK);;
if D380Observed<>D380Sentinel then Error("task380 sentinel mismatch"); fi;
Print(D380Sentinel,"\n");;
