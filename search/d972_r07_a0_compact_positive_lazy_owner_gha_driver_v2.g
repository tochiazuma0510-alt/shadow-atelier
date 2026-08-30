#############################################################################
## R07 A0 compact positive-first lazy owner. ASCII only.
#############################################################################
if not IsBound(D413Mode) then D413Mode:="PRODUCTION"; fi;
if D413Mode<>"PRODUCTION" then Error("task413 production-only mode"); fi;
D413Producer:="search/d972_r07_a0_compact_positive_lazy_owner_v2.py";;
D413Checker:="crosscheck/check_d972_r07_a0_compact_positive_lazy_owner_v2.py";;
D413ProducerBytes:=26424;; D413ProducerSHA:="435f2a3e10dca0ce0ce9a2109c4ee34282105f52750dd4c68a63cb18b7ea15e4";;
D413CheckerBytes:=5117;; D413CheckerSHA:="9998192818fd8ba780e7329df552fd8a5df60c7a3da9e9ec8781abc708bb519c";;
D413Receipt:="ci/out/d972_r07_a0_compact_positive_lazy_owner_v2.json";;
D413Verdict:="ci/out/d972_r07_a0_compact_positive_lazy_owner_v2.checker.ok";;
D413Log:="ci/out/d972_r07_a0_compact_positive_lazy_owner_v2.log";;
D413Checkpoint:="ci/out/d972_r07_a0_compact_positive_lazy_owner_v2.checkpoint";;
D413Script:="ci/out/d972_r07_a0_compact_positive_lazy_owner_v2.sh";;
if IsExistingFile(D413Receipt) or IsExistingFile(D413Verdict) or IsExistingFile(D413Log) or IsExistingFile(D413Script) then Error("task413 stale output"); fi;
D413S:=OutputTextFile(D413Script,false);;
if D413S=fail then Error("task413 script open"); fi;
SetPrintFormattingStatus(D413S,false);;
PrintTo(D413S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D413S,"test \"$(wc -c < ",D413Producer,")\" = \"",String(D413ProducerBytes),"\"\n");;
PrintTo(D413S,"test \"$(sha256sum ",D413Producer," | awk '{print $1}')\" = \"",D413ProducerSHA,"\"\n");;
PrintTo(D413S,"test \"$(wc -c < ",D413Checker,")\" = \"",String(D413CheckerBytes),"\"\n");;
PrintTo(D413S,"test \"$(sha256sum ",D413Checker," | awk '{print $1}')\" = \"",D413CheckerSHA,"\"\n");;
PrintTo(D413S,"python3 -u -B ",D413Producer," --mode PRODUCTION --output ",D413Receipt," --checkpoint ",D413Checkpoint," --seconds 6000 2>&1 | tee ",D413Log,"\n");;
PrintTo(D413S,"cat ",D413Log,"\n");;
PrintTo(D413S,"python3 -u -B ",D413Checker," --producer ",D413Receipt," 2>&1 | tee ",D413Verdict,"\n");;
CloseStream(D413S);; Exec(Concatenation("chmod +x ",D413Script));; Exec(D413Script);;
Print("R07_A0_COMPACT_POSITIVE_LAZY_OWNER_V2_GHA_DONE\n");
