#############################################################################
## R07 A0 batch-v4 exact resume transport. ASCII only.
#############################################################################
D417Producer:="search/d972_r07_a0_batch_lazy_owner_v4.py";;
D417Checker:="crosscheck/check_d972_r07_a0_batch_lazy_owner_v4.py";;
D417Prior:="ci/in/prior/d972_r07_a0_batch_lazy_owner_v4.checkpoint";;
D417PriorBytes:=129119626;;
D417PriorSHA:="1deed5488a8051102a3fbc80d65432b6f461fdf35c7db46e51261610b7e4a3d5";;
D417ProducerBytes:=8505;;
D417ProducerSHA:="fa7e4682fae6eadba43bc8121cae930f7a4f0bb5f4286afac8b81e2d3e10a1cd";;
D417CheckerBytes:=1765;;
D417CheckerSHA:="38952af42673ec9e03d355dd8826db9973e2e19110b43d58ca7800e6fb67af8f";;
D417Receipt:="ci/out/d972_r07_a0_batch_lazy_owner_v4_resume.json";;
D417Verdict:="ci/out/d972_r07_a0_batch_lazy_owner_v4_resume.checker.ok";;
D417Log:="ci/out/d972_r07_a0_batch_lazy_owner_v4_resume.log";;
D417Checkpoint:="ci/out/d972_r07_a0_batch_lazy_owner_v4_resume.checkpoint";;
D417Script:="ci/out/d972_r07_a0_batch_lazy_owner_v4_resume.sh";;
if IsExistingFile(D417Receipt) or IsExistingFile(D417Verdict) or
   IsExistingFile(D417Log) or IsExistingFile(D417Checkpoint) or
   IsExistingFile(D417Script) then Error("task417 stale output"); fi;
if not IsExistingFile(D417Prior) then Error("task417 prior checkpoint missing"); fi;
D417Raw:=StringFile(D417Prior);;
if D417Raw=fail or Length(D417Raw)<>D417PriorBytes or
   HexSHA256(D417Raw)<>D417PriorSHA then Error("task417 prior checkpoint pin"); fi;
D417S:=OutputTextFile(D417Script,false);;
if D417S=fail then Error("task417 script open"); fi;
SetPrintFormattingStatus(D417S,false);;
PrintTo(D417S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D417S,"test \"$(wc -c < ",D417Producer,")\" = \"",String(D417ProducerBytes),"\"\n");;
PrintTo(D417S,"test \"$(sha256sum ",D417Producer," | awk '{print $1}')\" = \"",D417ProducerSHA,"\"\n");;
PrintTo(D417S,"test \"$(wc -c < ",D417Checker,")\" = \"",String(D417CheckerBytes),"\"\n");;
PrintTo(D417S,"test \"$(sha256sum ",D417Checker," | awk '{print $1}')\" = \"",D417CheckerSHA,"\"\n");;
PrintTo(D417S,"python3 -u -B ",D417Producer," --mode PRODUCTION --output ",D417Receipt," --resume ",D417Prior," --checkpoint ",D417Checkpoint," --seconds 18000 --rounds 1000000 --batch-cap 128 --rss-bytes 5700000000 2>&1 | tee ",D417Log,"\n");;
PrintTo(D417S,"test -f ",D417Receipt,"\n");;
PrintTo(D417S,"if grep -q '\"status\":\"UNKNOWN_RESOURCE\"' ",D417Receipt,"; then test -f ",D417Checkpoint,"; fi\n");;
PrintTo(D417S,"python3 -u -B ",D417Checker," --producer ",D417Receipt," 2>&1 | tee ",D417Verdict,"\n");;
PrintTo(D417S,"echo R07_A0_BATCH_V4_RESUME_TRANSPORT_DONE\n");;
CloseStream(D417S);; Exec(Concatenation("chmod +x ",D417Script));; Exec(D417Script);;
Print("R07_A0_BATCH_V4_RESUME_TRANSPORT_GHA_DONE\n");
