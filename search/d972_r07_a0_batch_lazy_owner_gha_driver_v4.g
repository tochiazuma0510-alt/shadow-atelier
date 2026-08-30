#############################################################################
## R07 A0 batch-lazy owner. ASCII only; controlled production slice.
#############################################################################
if not IsBound(D416Mode) then D416Mode:="PRODUCTION"; fi;
if D416Mode<>"PRODUCTION" then Error("task416 production-only mode"); fi;
D416Producer:="search/d972_r07_a0_batch_lazy_owner_v4.py";;
D416Checker:="crosscheck/check_d972_r07_a0_batch_lazy_owner_v4.py";;
D416ProducerBytes:=8505;; D416ProducerSHA:="fa7e4682fae6eadba43bc8121cae930f7a4f0bb5f4286afac8b81e2d3e10a1cd";;
D416CheckerBytes:=1765;; D416CheckerSHA:="38952af42673ec9e03d355dd8826db9973e2e19110b43d58ca7800e6fb67af8f";;
D416Receipt:="ci/out/d972_r07_a0_batch_lazy_owner_v4.json";;
D416Verdict:="ci/out/d972_r07_a0_batch_lazy_owner_v4.checker.ok";;
D416Log:="ci/out/d972_r07_a0_batch_lazy_owner_v4.log";;
D416Checkpoint:="ci/out/d972_r07_a0_batch_lazy_owner_v4.checkpoint";;
D416Script:="ci/out/d972_r07_a0_batch_lazy_owner_v4.sh";;
if IsExistingFile(D416Receipt) or IsExistingFile(D416Verdict) or IsExistingFile(D416Log) or IsExistingFile(D416Script) then Error("task416 stale output"); fi;
D416S:=OutputTextFile(D416Script,false);; if D416S=fail then Error("task416 script open"); fi;
SetPrintFormattingStatus(D416S,false);; PrintTo(D416S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D416S,"test \"$(wc -c < ",D416Producer,")\" = \"",String(D416ProducerBytes),"\"\n");;
PrintTo(D416S,"test \"$(sha256sum ",D416Producer," | awk '{print $1}')\" = \"",D416ProducerSHA,"\"\n");;
PrintTo(D416S,"test \"$(wc -c < ",D416Checker,")\" = \"",String(D416CheckerBytes),"\"\n");;
PrintTo(D416S,"test \"$(sha256sum ",D416Checker," | awk '{print $1}')\" = \"",D416CheckerSHA,"\"\n");;
PrintTo(D416S,"python3 -u -B ",D416Producer," --mode PRODUCTION --output ",D416Receipt," --checkpoint ",D416Checkpoint," --seconds 6000 --rounds 1000000 --batch-cap 128 2>&1 | tee ",D416Log,"\n");;
PrintTo(D416S,"cat ",D416Log,"\n");; PrintTo(D416S,"python3 -u -B ",D416Checker," --producer ",D416Receipt," 2>&1 | tee ",D416Verdict,"\n");;
CloseStream(D416S);; Exec(Concatenation("chmod +x ",D416Script));; Exec(D416Script);;
Print("R07_A0_BATCH_LAZY_OWNER_V4_GHA_DONE\n");
