#############################################################################
## A0 v20 minimal RSS/checkpoint repair production driver. ASCII; fail closed.
#############################################################################
D371Producer:="search/d972_r07_history_free_positive_fast_resume_v20.py";;
D371ProducerBytes:=10739;;
D371ProducerSHA:="cf775975304a56cd3587470074e31d3a2000fba418fab5793fd25d6307150ed7";;
D371Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v20.py";;
D371CheckerBytes:=5327;;
D371CheckerSHA:="7c0a1c8b862f8dd62224e0f4ebc0d50ae7ea2de86c63ffb67e025cba98d7c077";;
D371Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D371Manifest:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json";;
D371Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
D371Raw:="ci/resume/d972_r07_history_free_positive_fast_resume_v20.raw.json";;
D371Base:="ci/out/d972_r07_history_free_positive_fast_resume_v20_production";;
D371Receipt:=Concatenation(D371Base,".json");;
D371Checkpoint:=Concatenation(D371Receipt,".checkpoint.json");;
D371Verdict:=Concatenation(D371Base,".verdict.json");;
D371ProducerLog:=Concatenation(D371Base,".producer.log");;
D371CheckerLog:=Concatenation(D371Base,".checker.log");;
D371ProducerTerminal:=Concatenation(D371Base,".producer.terminal");;
D371CheckerTerminal:=Concatenation(D371Base,".checker.terminal");;
D371Shell:=Concatenation(D371Base,".sh");;
D371OK:=Concatenation(D371Base,".ok");;
D371Common:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD";;
D371ProducerPrefix:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_PRODUCER_TERMINAL";;
D371CheckerPrefix:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_CHECKER_TERMINAL";;
D371Sentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V20_DRIVER_PASS";;

if D371ProducerBytes=0 or D371CheckerBytes=0 then
  Error("task371 final source pins required");
fi;
for D371Path in [D371Receipt,D371Checkpoint,D371Verdict,D371ProducerLog,
                 D371CheckerLog,D371ProducerTerminal,D371CheckerTerminal,
                 D371Shell,D371OK,D371Raw] do
  if IsExistingFile(D371Path) then Error("task371 stale output ",D371Path); fi;
od;

Exec("mkdir -p ci/out ci/resume");;
D371Stream:=OutputTextFile(D371Shell,false);;
if D371Stream=fail then Error("task371 shell open"); fi;
SetPrintFormattingStatus(D371Stream,false);;
PrintTo(D371Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D371Stream,"for command in python3 timeout tee grep sed cmp wc sha256sum unzip; do command -v \"$command\" >/dev/null; done\n");
PrintTo(D371Stream,"test \"$(wc -c < ",D371Producer,
  ")\" = \"",String(D371ProducerBytes),"\"\n");
PrintTo(D371Stream,"test \"$(sha256sum ",D371Producer,
  " | awk '{print $1}')\" = \"",D371ProducerSHA,"\"\n");
PrintTo(D371Stream,"test \"$(wc -c < ",D371Checker,
  ")\" = \"",String(D371CheckerBytes),"\"\n");
PrintTo(D371Stream,"test \"$(sha256sum ",D371Checker,
  " | awk '{print $1}')\" = \"",D371CheckerSHA,"\"\n");
PrintTo(D371Stream,"test \"$(wc -c < ",D371Zip,
  ")\" = \"5001811\"\n");
PrintTo(D371Stream,"test \"$(sha256sum ",D371Zip,
  " | awk '{print $1}')\" = \"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566\"\n");
PrintTo(D371Stream,"test \"$(wc -c < ",D371Manifest,
  ")\" = \"1328\"\n");
PrintTo(D371Stream,"test \"$(sha256sum ",D371Manifest,
  " | awk '{print $1}')\" = \"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302\"\n");
PrintTo(D371Stream,"unzip -p ",D371Zip," ",D371Member," > ",D371Raw,"\n");
PrintTo(D371Stream,"test \"$(wc -c < ",D371Raw,
  ")\" = \"86368039\"\n");
PrintTo(D371Stream,"test \"$(sha256sum ",D371Raw,
  " | awk '{print $1}')\" = \"c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab\"\n");
PrintTo(D371Stream,"workers=2\n");
PrintTo(D371Stream,"set +e\n");
PrintTo(D371Stream,"timeout --foreground 11100s python3 -u -B ",D371Producer,
  " --mode PRODUCTION --source ",D371Raw,
  " --manifest ",D371Manifest," --output ",D371Receipt,
  " --seconds 10800 --workers \"$workers\" 2>&1 | tee ",D371ProducerLog,"\n");
PrintTo(D371Stream,"producer_pipeline_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D371Stream,"set -e\n");
PrintTo(D371Stream,"if [ \"$","{producer_pipeline_status[0]}\" -ne 0 ]; then exit \"$","{producer_pipeline_status[0]}\"; fi\n");
PrintTo(D371Stream,"if [ \"$","{producer_pipeline_status[1]}\" -ne 0 ]; then exit \"$","{producer_pipeline_status[1]}\"; fi\n");
PrintTo(D371Stream,"test -s ",D371Receipt," -a -s ",D371ProducerLog,"\n");
PrintTo(D371Stream,"test \"$(grep -c '^",D371ProducerPrefix," ' ",
  D371ProducerLog,")\" -eq 1\n");
PrintTo(D371Stream,"grep -E '^",D371ProducerPrefix," ' ",D371ProducerLog,
  " | sed 's/^",D371ProducerPrefix," //' > ",D371ProducerTerminal,"\n");
PrintTo(D371Stream,"set +e\n");
PrintTo(D371Stream,"timeout --foreground 7500s python3 -u -B ",D371Checker,
  " --receipt ",D371Receipt," --verdict ",D371Verdict,
  " 2>&1 | tee ",D371CheckerLog,"\n");
PrintTo(D371Stream,"checker_pipeline_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D371Stream,"set -e\n");
PrintTo(D371Stream,"if [ \"$","{checker_pipeline_status[0]}\" -ne 0 ]; then exit \"$","{checker_pipeline_status[0]}\"; fi\n");
PrintTo(D371Stream,"if [ \"$","{checker_pipeline_status[1]}\" -ne 0 ]; then exit \"$","{checker_pipeline_status[1]}\"; fi\n");
PrintTo(D371Stream,"test -s ",D371Verdict," -a -s ",D371CheckerLog,"\n");
PrintTo(D371Stream,"test \"$(grep -c '^",D371CheckerPrefix," ' ",
  D371CheckerLog,")\" -eq 1\n");
PrintTo(D371Stream,"grep -E '^",D371CheckerPrefix," ' ",D371CheckerLog,
  " | sed 's/^",D371CheckerPrefix," //' > ",D371CheckerTerminal,"\n");
PrintTo(D371Stream,"test \"$(wc -l < ",D371ProducerTerminal,")\" -eq 1\n");
PrintTo(D371Stream,"test \"$(wc -l < ",D371CheckerTerminal,")\" -eq 1\n");
PrintTo(D371Stream,"cmp -s ",D371ProducerTerminal," ",D371CheckerTerminal,"\n");
PrintTo(D371Stream,"terminal=$(tr -d '\\n' < ",D371ProducerTerminal,")\n");
PrintTo(D371Stream,"case \"$terminal\" in\n");
PrintTo(D371Stream,"  ",D371Common,") test ! -e ",D371Checkpoint," ;;\n");
PrintTo(D371Stream,"  UNKNOWN_INPUT:*) [[ \"$terminal\" =~ ^UNKNOWN_INPUT:[-A-Za-z0-9_.=,+:]+$ ]] && test ! -e ",D371Checkpoint," ;;\n");
PrintTo(D371Stream,"  UNKNOWN_RESOURCE:phase=*) [[ \"$terminal\" =~ ^UNKNOWN_RESOURCE:phase=[A-Za-z0-9_]+:cap=[A-Za-z0-9_]+:value=[0-9]+([.][0-9]+)?:limit=[0-9]+([.][0-9]+)?$ ]] && ( test -s ",D371Checkpoint," || grep -Fq '\"checkpoint_required\":false' ",D371Receipt," ) ;;\n");
PrintTo(D371Stream,"  *) exit 1 ;;\n");
PrintTo(D371Stream,"esac\n");
PrintTo(D371Stream,"printf '%s' '",D371Sentinel,"' > ",D371OK,"\n");
CloseStream(D371Stream);;
Exec(Concatenation("bash ",D371Shell));;
D371Observed:=StringFile(D371OK);;
if D371Observed<>D371Sentinel then Error("task371 sentinel mismatch"); fi;
Print(D371Sentinel,"\n");;
