#############################################################################
## R07 compact direct-relator positive-only owner. ASCII only.
#############################################################################
if not IsBound(D460Mode) then D460Mode:="PRODUCTION"; fi;
if D460Mode<>"PRODUCTION" then Error("task460 production-only mode"); fi;
D460Producer:="search/d972_r07_compact_direct_relator_a5_a6_positive_v1.py";;
D460Checker:="crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v1.py";;
D460ProducerBytes:=17452;; D460ProducerSHA:="0a3c2473448ecade6cd4a313c21b09359756214dd36933725fbb11700e1c121c";;
D460CheckerBytes:=12062;; D460CheckerSHA:="3c455dbfbb914fb89498be7249c1230042d432145e3680b391c09ada7a658ab7";;
D460Receipt:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v1.json";;
D460Checkpoint:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v1.checkpoint";;
D460Verdict:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v1.checker.ok";;
D460Log:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v1.log";;
D460Script:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v1.sh";;
if IsExistingFile(D460Receipt) or IsExistingFile(D460Checkpoint) or
   IsExistingFile(D460Verdict) or IsExistingFile(D460Log) or
   IsExistingFile(D460Script) then Error("task460 stale output"); fi;
D460S:=OutputTextFile(D460Script,false);;
if D460S=fail then Error("task460 script open"); fi;
SetPrintFormattingStatus(D460S,false);;
PrintTo(D460S,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D460S,"test \"$(wc -c < ",D460Producer,")\" = \"",String(D460ProducerBytes),"\"\n");
PrintTo(D460S,"test \"$(sha256sum ",D460Producer," | awk '{print $1}')\" = \"",D460ProducerSHA,"\"\n");
PrintTo(D460S,"test \"$(wc -c < ",D460Checker,")\" = \"",String(D460CheckerBytes),"\"\n");
PrintTo(D460S,"test \"$(sha256sum ",D460Checker," | awk '{print $1}')\" = \"",D460CheckerSHA,"\"\n");
PrintTo(D460S,"python3 -u -B ",D460Producer," --mode PRODUCTION --output ",D460Receipt," --checkpoint ",D460Checkpoint," 2>&1 | tee ",D460Log,"\n");
PrintTo(D460S,"if python3 -c \"import json; s=json.load(open('",D460Receipt,"'))['status']; raise SystemExit(0 if s=='MEMBER' else 2 if s=='UNKNOWN_INCOMPLETE' else 1)\"; then python3 -u -B ",D460Checker," --producer ",D460Receipt," 2>&1 | tee ",D460Verdict,"; else test $? -eq 2; fi\n");
CloseStream(D460S);;
Print("R07_COMPACT_DIRECT_RELATOR_POSITIVE_OWNER_V1_DRIVER_READY\n");
