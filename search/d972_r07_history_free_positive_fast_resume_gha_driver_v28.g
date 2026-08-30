#############################################################################
## A0 v28 two-phase low-memory resume driver. ASCII only; fail closed.
## V28 changes only the prior artifact member path to its uploaded basename.
#############################################################################
D407Producer:="search/d972_r07_history_free_positive_fast_resume_v26.py";;
D407ProducerBytes:=5950;;
D407ProducerSHA:="4ae9de2eaf0ae337d48309f107fe7aef94afe3783ee2bde63b7c839364e1098e";;
D407Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v27.py";;
D407CheckerBytes:=1964;;
D407CheckerSHA:="181553ce338d1ef65e9ca275a41b157c2e4f8f4a8ca8616a63f3b5a144a045a3";;
D407Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D407Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
D407Source:="ci/resume/d972_r07_history_free_positive_fast_resume_v20.raw.json";;
D407Manifest:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json";;
D407Resume:="ci/in/prior/d972_r07_history_free_positive_fast_resume_v24_production.json.checkpoint.json";;
D407Base:="ci/out/d972_r07_history_free_positive_fast_resume_v28_production";;
D407Receipt:=Concatenation(D407Base,".json");;
D407Checkpoint:=Concatenation(D407Receipt,".checkpoint.json");;
D407Verdict:=Concatenation(D407Base,".verdict.json");;
D407ProducerLog:=Concatenation(D407Base,".producer.log");;
D407CheckerLog:=Concatenation(D407Base,".checker.log");;
D407ProducerTerminal:=Concatenation(D407Base,".producer.terminal");;
D407CheckerTerminal:=Concatenation(D407Base,".checker.terminal");;
D407Shell:=Concatenation(D407Base,".sh");;
D407OK:=Concatenation(D407Base,".ok");;
D407Sentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V28_DRIVER_PASS";;

for D407Path in [D407Receipt,D407Checkpoint,D407Verdict,D407ProducerLog,
                 D407CheckerLog,D407ProducerTerminal,D407CheckerTerminal,
                 D407Shell,D407OK] do
  if IsExistingFile(D407Path) then Error("task408 stale output ",D407Path); fi;
od;
if not IsExistingFile(D407Zip) or not IsExistingFile(D407Manifest) or
   not IsExistingFile(D407Resume) then Error("task408 missing input"); fi;
D407Stream:=OutputTextFile(D407Shell,false);;
if D407Stream=fail then Error("task408 shell open"); fi;
SetPrintFormattingStatus(D407Stream,false);;
PrintTo(D407Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D407Stream,"for command in python3 timeout tee grep sed cmp wc sha256sum unzip; do command -v \"$command\" >/dev/null; done\n");
PrintTo(D407Stream,"test \"$(wc -c < ",D407Producer,")\" = \"",String(D407ProducerBytes),"\"\n");
PrintTo(D407Stream,"test \"$(sha256sum ",D407Producer," | awk '{print $1}')\" = \"",D407ProducerSHA,"\"\n");
PrintTo(D407Stream,"test \"$(wc -c < ",D407Checker,")\" = \"",String(D407CheckerBytes),"\"\n");
PrintTo(D407Stream,"test \"$(sha256sum ",D407Checker," | awk '{print $1}')\" = \"",D407CheckerSHA,"\"\n");
PrintTo(D407Stream,"test \"$(wc -c < ",D407Zip,")\" = \"5001811\"\n");
PrintTo(D407Stream,"test \"$(sha256sum ",D407Zip," | awk '{print $1}')\" = \"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566\"\n");
PrintTo(D407Stream,"test \"$(wc -c < ",D407Manifest,")\" = \"1328\"\n");
PrintTo(D407Stream,"test \"$(sha256sum ",D407Manifest," | awk '{print $1}')\" = \"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302\"\n");
PrintTo(D407Stream,"mkdir -p ci/resume\n");
PrintTo(D407Stream,"unzip -p ",D407Zip," ",D407Member," > ",D407Source,"\n");
PrintTo(D407Stream,"test \"$(wc -c < ",D407Source,")\" = \"86368039\"\n");
PrintTo(D407Stream,"test \"$(sha256sum ",D407Source," | awk '{print $1}')\" = \"c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab\"\n");
PrintTo(D407Stream,"test \"$(wc -c < ",D407Resume,")\" = \"1663424241\"\n");
PrintTo(D407Stream,"test \"$(sha256sum ",D407Resume," | awk '{print $1}')\" = \"55c463335e89fb7e67a04ec9c0405a8216f6f909b2ce67a0fe7a8a4afaf2014d\"\n");
PrintTo(D407Stream,"set +e\n");
PrintTo(D407Stream,"timeout --foreground 11100s python3 -u -B ",D407Producer,
  " --mode PRODUCTION --source ",D407Source," --manifest ",D407Manifest,
  " --output ",D407Receipt," --seconds 10800 --workers 2 --resume ",D407Resume,
  " 2>&1 | tee ",D407ProducerLog,"\n");
PrintTo(D407Stream,"producer_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D407Stream,"grep -E '^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_PRODUCER_TERMINAL ' ",D407ProducerLog,
  " | sed 's/^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_PRODUCER_TERMINAL //' > ",D407ProducerTerminal,"\n");
PrintTo(D407Stream,"timeout --foreground 1800s python3 -u -B ",D407Checker,
  " --receipt ",D407Receipt," --verdict ",D407Verdict," 2>&1 | tee ",D407CheckerLog,"\n");
PrintTo(D407Stream,"checker_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D407Stream,"grep -E '^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_CHECKER_TERMINAL ' ",D407CheckerLog,
  " | sed 's/^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_CHECKER_TERMINAL //' > ",D407CheckerTerminal,"\n");
PrintTo(D407Stream,"set -e\n");
PrintTo(D407Stream,"test \"$","{producer_status[0]}\" -eq 0 -a \"$","{producer_status[1]}\" -eq 0\n");
PrintTo(D407Stream,"test \"$","{checker_status[0]}\" -eq 0 -a \"$","{checker_status[1]}\" -eq 0\n");
PrintTo(D407Stream,"test -s ",D407Receipt," -a -s ",D407Verdict,"\n");
PrintTo(D407Stream,"test \"$(wc -l < ",D407ProducerTerminal,")\" -eq 1\n");
PrintTo(D407Stream,"test \"$(wc -l < ",D407CheckerTerminal,")\" -eq 1\n");
PrintTo(D407Stream,"cmp -s ",D407ProducerTerminal," ",D407CheckerTerminal,"\n");
PrintTo(D407Stream,"printf '%s' '",D407Sentinel,"' > ",D407OK,"\n");
CloseStream(D407Stream);;
Exec(Concatenation("bash ",D407Shell));;
D407Observed:=StringFile(D407OK);;
if D407Observed<>D407Sentinel then Error("task408 sentinel mismatch"); fi;
Print(D407Sentinel,"\n");;
