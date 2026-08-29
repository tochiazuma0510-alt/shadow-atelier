#############################################################################
## R07 zero-base A5/A6 production transport. ASCII only; no SELFTEST path.
#############################################################################
if not IsBound(DZeroBaseMode) then Error("zero-base MODE required"); fi;
if DZeroBaseMode<>"PRODUCTION" then Error("zero-base production only"); fi;
DManifest:="ci/in/d972_r07_zero_base_a5_a6_compiler_v1.manifest.json";;
DProducer:="search/d972_r07_zero_base_a5_a6_compiler_v1.py";;
DProducerBytes:=21903;;
DProducerSHA:="abd44b7182a13bb53595f562df3310b0d96fb61e5ed54391446e1bf265df4173";;
DChecker:="crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v1.py";;
DCheckerBytes:=14462;;
DCheckerSHA:="06055c2e9ea599d666711327b7ba75a9f02e6dae90bfe4c3cee3560f95651b72";;
DReceipt:="ci/out/d972_r07_zero_base_a5_a6_compiler_v1.json";;
DVerdict:="ci/out/d972_r07_zero_base_a5_a6_compiler_v1.verdict.json";;
DPLog:="ci/out/d972_r07_zero_base_a5_a6_compiler_v1.producer.log";;
DCLog:="ci/out/d972_r07_zero_base_a5_a6_compiler_v1.checker.log";;
DSh:="ci/out/d972_r07_zero_base_a5_a6_compiler_v1.sh";;
DOK:="ci/out/d972_r07_zero_base_a5_a6_compiler_v1.ok";;
DRead:=function(path) local x; x:=StringFile(path); if x=fail then Error("missing source ",path); fi; return x; end;;
DPin:=function(path,bytes,digest)
  local raw;
  raw:=DRead(path);;
  if Length(raw)<>bytes or HexSHA256(raw)<>digest then Error("source pin drift ",path); fi;
end;;
DPin(DProducer,DProducerBytes,DProducerSHA);;
DPin(DChecker,DCheckerBytes,DCheckerSHA);;
for DPath in [DReceipt,DVerdict,DPLog,DCLog,DSh,DOK] do
  if IsExistingFile(DPath) then Error("stale zero-base output ",DPath); fi;
od;
DStream:=OutputTextFile(DSh,false);; SetPrintFormattingStatus(DStream,false);;
PrintTo(DStream,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
PrintTo(DStream,"python3 -u -B ",DProducer," --manifest ",DManifest," --output ",DReceipt," > ",DPLog," 2>&1\n");
PrintTo(DStream,"cat ",DPLog,"\n");
PrintTo(DStream,"python3 -u -B ",DChecker," --manifest ",DManifest," --receipt ",DReceipt," --output ",DVerdict," > ",DCLog," 2>&1\n");
PrintTo(DStream,"cat ",DCLog,"\n");
PrintTo(DStream,"test -s ",DReceipt," -a -s ",DVerdict,"\n");
PrintTo(DStream,"test \"$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[\"terminal\"])' ",DReceipt,")\" = \"$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[\"terminal\"])' ",DVerdict,")\"\n");
PrintTo(DStream,"printf 'R07_ZERO_BASE_A5_A6_COMPILER_V1_DONE\\n' > ",DOK,"\n");
PrintTo(DStream,"test -s ",DOK,"\n");
CloseStream(DStream);;
Exec(Concatenation("bash ",DSh));;
if not IsExistingFile(DOK) then Error("zero-base missing completion"); fi;
Print("R07_ZERO_BASE_A5_A6_COMPILER_V1_DRIVER_DONE\n");
