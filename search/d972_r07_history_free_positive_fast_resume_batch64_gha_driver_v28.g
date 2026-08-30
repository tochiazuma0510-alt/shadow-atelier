#############################################################################
## A0 v28 globally merged batch-64 resume driver. ASCII; fail closed.
#############################################################################
D408Producer:="search/d972_r07_history_free_positive_fast_resume_batch64_v28.py";;
D408ProducerBytes:=19149;;
D408ProducerSHA:="ff26d11c23b45b70a1fc93d481bfd4f3dd66e6c106fd0afae140af81ec01ddf9";;
D408Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_batch64_v28.py";;
D408CheckerBytes:=8219;;
D408CheckerSHA:="0491b3b7ff68a839811869079c7da33cae751f58936c6eef7a4e5ab8724baa99";;
D408Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D408Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
D408Source:="ci/resume/d972_r07_history_free_positive_fast_resume_v20.raw.json";;
D408Manifest:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json";;
D408Resume:="ci/in/prior/d972_r07_history_free_positive_fast_resume_v24_production.json.checkpoint.json";;
D408Base:="ci/out/d972_r07_history_free_positive_fast_resume_batch64_v28_production";;
D408Receipt:=Concatenation(D408Base,".json");;
D408Checkpoint:=Concatenation(D408Receipt,".checkpoint.json");;
D408Verdict:=Concatenation(D408Base,".verdict.json");;
D408ProducerLog:=Concatenation(D408Base,".producer.log");;
D408CheckerLog:=Concatenation(D408Base,".checker.log");;
D408ProducerTerminal:=Concatenation(D408Base,".producer.terminal");;
D408CheckerTerminal:=Concatenation(D408Base,".checker.terminal");;
D408Shell:=Concatenation(D408Base,".sh");;
D408OK:=Concatenation(D408Base,".ok");;
D408Sentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_BATCH64_V28_DRIVER_PASS";;

for D408Path in [D408Receipt,D408Checkpoint,D408Verdict,D408ProducerLog,
                 D408CheckerLog,D408ProducerTerminal,D408CheckerTerminal,
                 D408Shell,D408OK] do
  if IsExistingFile(D408Path) then Error("task408 stale output ",D408Path); fi;
od;
if not IsExistingFile(D408Zip) or not IsExistingFile(D408Manifest) or
   not IsExistingFile(D408Resume) then Error("task408 missing input"); fi;
D408Stream:=OutputTextFile(D408Shell,false);;
if D408Stream=fail then Error("task408 shell open"); fi;
SetPrintFormattingStatus(D408Stream,false);;
PrintTo(D408Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D408Stream,"for command in python3 timeout tee grep sed cmp wc sha256sum unzip; do command -v \"$command\" >/dev/null; done\n");
PrintTo(D408Stream,"test \"$(wc -c < ",D408Producer,")\" = \"",String(D408ProducerBytes),"\"\n");
PrintTo(D408Stream,"test \"$(sha256sum ",D408Producer," | awk '{print $1}')\" = \"",D408ProducerSHA,"\"\n");
PrintTo(D408Stream,"test \"$(wc -c < ",D408Checker,")\" = \"",String(D408CheckerBytes),"\"\n");
PrintTo(D408Stream,"test \"$(sha256sum ",D408Checker," | awk '{print $1}')\" = \"",D408CheckerSHA,"\"\n");
PrintTo(D408Stream,"test \"$(wc -c < ",D408Zip,")\" = \"5001811\"\n");
PrintTo(D408Stream,"test \"$(sha256sum ",D408Zip," | awk '{print $1}')\" = \"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566\"\n");
PrintTo(D408Stream,"test \"$(wc -c < ",D408Manifest,")\" = \"1328\"\n");
PrintTo(D408Stream,"test \"$(sha256sum ",D408Manifest," | awk '{print $1}')\" = \"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302\"\n");
PrintTo(D408Stream,"mkdir -p ci/resume\n");
PrintTo(D408Stream,"unzip -p ",D408Zip," ",D408Member," > ",D408Source,"\n");
PrintTo(D408Stream,"test \"$(wc -c < ",D408Source,")\" = \"86368039\"\n");
PrintTo(D408Stream,"test \"$(sha256sum ",D408Source," | awk '{print $1}')\" = \"c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab\"\n");
PrintTo(D408Stream,"test \"$(wc -c < ",D408Resume,")\" = \"1663424241\"\n");
PrintTo(D408Stream,"test \"$(sha256sum ",D408Resume," | awk '{print $1}')\" = \"55c463335e89fb7e67a04ec9c0405a8216f6f909b2ce67a0fe7a8a4afaf2014d\"\n");
PrintTo(D408Stream,"set +e\n");
PrintTo(D408Stream,"timeout --foreground 11100s python3 -u -B ",D408Producer,
  " --mode PRODUCTION --source ",D408Source," --manifest ",D408Manifest,
  " --output ",D408Receipt," --seconds 10800 --workers 2 --resume ",D408Resume,
  " 2>&1 | tee ",D408ProducerLog,"\n");
PrintTo(D408Stream,"producer_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D408Stream,"grep -E '^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_PRODUCER_TERMINAL ' ",D408ProducerLog,
  " | sed 's/^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_PRODUCER_TERMINAL //' > ",D408ProducerTerminal,"\n");
PrintTo(D408Stream,"timeout --foreground 1800s python3 -u -B ",D408Checker,
  " --receipt ",D408Receipt," --verdict ",D408Verdict," 2>&1 | tee ",D408CheckerLog,"\n");
PrintTo(D408Stream,"checker_status=(\"$","{PIPESTATUS[@]}\")\n");
PrintTo(D408Stream,"grep -E '^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_CHECKER_TERMINAL ' ",D408CheckerLog,
  " | sed 's/^R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_CHECKER_TERMINAL //' > ",D408CheckerTerminal,"\n");
PrintTo(D408Stream,"set -e\n");
PrintTo(D408Stream,"test \"$","{producer_status[0]}\" -eq 0 -a \"$","{producer_status[1]}\" -eq 0\n");
PrintTo(D408Stream,"test \"$","{checker_status[0]}\" -eq 0 -a \"$","{checker_status[1]}\" -eq 0\n");
PrintTo(D408Stream,"test -s ",D408Receipt," -a -s ",D408Verdict,"\n");
PrintTo(D408Stream,"test \"$(wc -l < ",D408ProducerTerminal,")\" -eq 1\n");
PrintTo(D408Stream,"test \"$(wc -l < ",D408CheckerTerminal,")\" -eq 1\n");
PrintTo(D408Stream,"cmp -s ",D408ProducerTerminal," ",D408CheckerTerminal,"\n");
PrintTo(D408Stream,"printf '%s' '",D408Sentinel,"' > ",D408OK,"\n");
CloseStream(D408Stream);;
Exec(Concatenation("bash ",D408Shell));;
D408Observed:=StringFile(D408OK);;
if D408Observed<>D408Sentinel then Error("task408 sentinel mismatch"); fi;
Print(D408Sentinel,"\n");;
