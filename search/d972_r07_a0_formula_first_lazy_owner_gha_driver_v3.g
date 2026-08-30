#############################################################################
## R07 A0 formula-first lazy owner. ASCII only; controlled production slice.
#############################################################################
if not IsBound(D415Mode) then D415Mode:="PRODUCTION"; fi;
if D415Mode<>"PRODUCTION" then Error("task415 production-only mode"); fi;
D415Producer:="search/d972_r07_a0_formula_first_lazy_owner_v3.py";;
D415Checker:="crosscheck/check_d972_r07_a0_formula_first_lazy_owner_v3.py";;
D415ProducerBytes:=6254;; D415ProducerSHA:="657f12e4c7f52dd8012e55a7e775a518c532f1d2b0e4735f88a9adfd7fb9e01c";;
D415CheckerBytes:=2227;; D415CheckerSHA:="efbbfafad0aa156b9b2d7d9cfafaba775597d24269760fe93aee4f8cace4c91a";;
D415Receipt:="ci/out/d972_r07_a0_formula_first_lazy_owner_v3.json";;
D415Verdict:="ci/out/d972_r07_a0_formula_first_lazy_owner_v3.checker.ok";;
D415Log:="ci/out/d972_r07_a0_formula_first_lazy_owner_v3.log";;
D415Checkpoint:="ci/out/d972_r07_a0_formula_first_lazy_owner_v3.checkpoint";;
D415Script:="ci/out/d972_r07_a0_formula_first_lazy_owner_v3.sh";;
if IsExistingFile(D415Receipt) or IsExistingFile(D415Verdict) or IsExistingFile(D415Log) or IsExistingFile(D415Script) then Error("task415 stale output"); fi;
D415S:=OutputTextFile(D415Script,false);; if D415S=fail then Error("task415 script open"); fi;
SetPrintFormattingStatus(D415S,false);;
PrintTo(D415S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D415S,"test \"$(wc -c < ",D415Producer,")\" = \"",String(D415ProducerBytes),"\"\n");;
PrintTo(D415S,"test \"$(sha256sum ",D415Producer," | awk '{print $1}')\" = \"",D415ProducerSHA,"\"\n");;
PrintTo(D415S,"test \"$(wc -c < ",D415Checker,")\" = \"",String(D415CheckerBytes),"\"\n");;
PrintTo(D415S,"test \"$(sha256sum ",D415Checker," | awk '{print $1}')\" = \"",D415CheckerSHA,"\"\n");;
PrintTo(D415S,"python3 -u -B ",D415Producer," --mode PRODUCTION --output ",D415Receipt," --checkpoint ",D415Checkpoint," --seconds 6000 2>&1 | tee ",D415Log,"\n");;
PrintTo(D415S,"cat ",D415Log,"\n");;
PrintTo(D415S,"python3 -u -B ",D415Checker," --producer ",D415Receipt," 2>&1 | tee ",D415Verdict,"\n");;
CloseStream(D415S);; Exec(Concatenation("chmod +x ",D415Script));; Exec(D415Script);;
Print("R07_A0_FORMULA_FIRST_LAZY_OWNER_V3_GHA_DONE\n");
