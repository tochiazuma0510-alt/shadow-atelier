#############################################################################
## A0 batch-64 v29 raw-row resume repair driver. ASCII; fail closed.
#############################################################################
D410Producer:="search/d972_r07_history_free_positive_fast_resume_batch64_v29.py";;
D410ProducerBytes:=4999;;
D410ProducerSHA:="e3cf997b8aae78599e693652cf576083ae518b7a3690099c83b12d6e83039434";;
D410Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_batch64_v29.py";;
D410CheckerBytes:=2332;;
D410CheckerSHA:="0df0b765f00553cec696606b334022fe5953fa79a05076454aed8f05e45ce7c2";;
D410Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D410Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
D410Source:="ci/resume/d972_r07_history_free_positive_fast_resume_v20.raw.json";;
D410Manifest:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json";;
D410Resume:="ci/in/prior/d972_r07_history_free_positive_fast_resume_v24_production.json.checkpoint.json";;
D410Base:="ci/out/d972_r07_history_free_positive_fast_resume_batch64_v29_production";;
D410Receipt:=Concatenation(D410Base,".json");;
D410Checkpoint:=Concatenation(D410Receipt,".checkpoint.json");;
D410Verdict:=Concatenation(D410Base,".verdict.json");;
D410ProducerLog:=Concatenation(D410Base,".producer.log");;
D410CheckerLog:=Concatenation(D410Base,".checker.log");;
D410ProducerTerminal:=Concatenation(D410Base,".producer.terminal");;
D410CheckerTerminal:=Concatenation(D410Base,".checker.terminal");;
D410Shell:=Concatenation(D410Base,".sh");;
D410OK:=Concatenation(D410Base,".ok");;
D410Sentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_BATCH64_V29_DRIVER_PASS";;

for D410Path in [D410Receipt,D410Checkpoint,D410Verdict,D410ProducerLog,
                 D410CheckerLog,D410ProducerTerminal,D410CheckerTerminal,
                 D410Shell,D410OK] do
  if IsExistingFile(D410Path) then Error("task408 stale output ",D410Path); fi;
od;
if not IsExistingFile(D410Zip) or not IsExistingFile(D410Manifest) or
   not IsExistingFile(D410Resume) then Error("task408 missing input"); fi;
D410Stream:=OutputTextFile(D410Shell,false);;
if D410Stream=fail then Error("task408 shell open"); fi;
SetPrintFormattingStatus(D410Stream,false);;
PrintTo(D410Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D410Stream,"for command in python3 timeout tee grep sed cmp wc sha256sum unzip; do command -v \"$command\" >/dev/null; done\n");
PrintTo(D410Stream,"test \"$(wc -c < ",D410Producer,")\" = \"",String(D410ProducerBytes),"\"\n");
PrintTo(D410Stream,"test \"$(sha256sum ",D410Producer," | awk '{print $1}')\" = \"",D410ProducerSHA,"\"\n");
PrintTo(D410Stream,"test \"$(wc -c < ",D410Checker,")\" = \"",String(D410CheckerBytes),"\"\n");
PrintTo(D410Stream,"test \"$(sha256sum ",D410Checker," | awk '{print $1}')\" = \"",D410CheckerSHA,"\"\n");
PrintTo(D410Stream,"test \"$(wc -c < ",D410Zip,")\" = \"5001811\"\n");
PrintTo(D410Stream,"test \"$(sha256sum ",D410Zip," | awk '{print $1}')\" = \"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566\"\n");
PrintTo(D410Stream,"test \"$(wc -c < ",D410Manifest,")\" = \"1328\"\n");
PrintTo(D410Stream,"test \"$(sha256sum ",D410Manifest," | awk '{print $1}')\" = \"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302\"\n");
PrintTo(D410Stream,"mkdir -p ci/resume\n");
PrintTo(D410Stream,"unzip -p ",D410Zip," ",D410Member," > ",D410Source,"\n");
PrintTo(D410Stream,"test \"$(wc -c < ",D410Source,")\" = \"86368039\"\n");
PrintTo(D410Stream,"test \"$(sha256sum ",D410Source," | awk '{print $1}')\" = \"c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab\"\n");
PrintTo(D410Stream,"test \"$(wc -c < ",D410Resume,")\" = \"1663424241\"\n");
PrintTo(D410Stream,"test \"$(sha256sum ",D410Resume," | awk '{print $1}')\" = \"55c463335e89fb7e67a04ec9c0405a8216f6f909b2ce67a0fe7a8a4afaf2014d\"\n");
PrintTo(D410Stream,"set +e\n");
PrintTo(D410Stream,"timeout --foreground 11100s python3 -u -B ",D410Producer,
  " --mode PRODUCTION --source ",D410Source," --manifest ",D410Manifest,
  " --output ",D410Receipt," --seconds 10800 --workers 2 --resume ",D410Resume,
  " 2>&1 | tee ",D410ProducerLog,"\n");
PrintTo(D410Stream,"producer_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D410Stream,"grep -E '^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_PRODUCER_TERMINAL ' ",D410ProducerLog,
  " | sed 's/^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_PRODUCER_TERMINAL //' > ",D410ProducerTerminal,"\n");
PrintTo(D410Stream,"timeout --foreground 1800s python3 -u -B ",D410Checker,
  " --receipt ",D410Receipt," --verdict ",D410Verdict," 2>&1 | tee ",D410CheckerLog,"\n");
PrintTo(D410Stream,"checker_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D410Stream,"grep -E '^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_CHECKER_TERMINAL ' ",D410CheckerLog,
  " | sed 's/^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_CHECKER_TERMINAL //' > ",D410CheckerTerminal,"\n");
PrintTo(D410Stream,"set -e\n");
PrintTo(D410Stream,"test \"$","{producer_status[0]}\" -eq 0 -a \"$","{producer_status[1]}\" -eq 0\n");
PrintTo(D410Stream,"test \"$","{checker_status[0]}\" -eq 0 -a \"$","{checker_status[1]}\" -eq 0\n");
PrintTo(D410Stream,"test -s ",D410Receipt," -a -s ",D410Verdict,"\n");
PrintTo(D410Stream,"test \"$(wc -l < ",D410ProducerTerminal,")\" -eq 1\n");
PrintTo(D410Stream,"test \"$(wc -l < ",D410CheckerTerminal,")\" -eq 1\n");
PrintTo(D410Stream,"cmp -s ",D410ProducerTerminal," ",D410CheckerTerminal,"\n");
PrintTo(D410Stream,"printf '%s' '",D410Sentinel,"' > ",D410OK,"\n");
CloseStream(D410Stream);;
Exec(Concatenation("bash ",D410Shell));;
D410Observed:=StringFile(D410OK);;
if D410Observed<>D410Sentinel then Error("task408 sentinel mismatch"); fi;
Print(D410Sentinel,"\n");;
