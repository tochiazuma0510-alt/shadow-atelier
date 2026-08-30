#############################################################################
## R07 A0 compact PC owner driver. ASCII only; bounded checkpoint continuation.
#############################################################################
if not IsBound(D411Mode) then D411Mode:="PRODUCTION"; fi;
if D411Mode<>"PRODUCTION" then Error("task411 production-only mode"); fi;
D411Producer:="search/d972_r07_a0_compact_pc_invariant_owner_v1.py";;
D411Checker:="crosscheck/check_d972_r07_a0_compact_pc_invariant_owner_v1.py";;
D411ProducerBytes:=59733;; D411ProducerSHA:="0c5e364a3ba3946081ea2551f2cc75331f29d4d570ed8b0613ffeccd1928c55f";;
D411CheckerBytes:=44831;; D411CheckerSHA:="7c1aea086ce264ad6f51983554a3a371ac481d07a2ec5f5d9a96ee270af6dfcf";;
D411Receipt:="ci/out/d972_r07_a0_compact_pc_invariant_owner_v1.json";;
D411Verdict:="ci/out/d972_r07_a0_compact_pc_invariant_owner_v1.checker.ok";;
D411Log:="ci/out/d972_r07_a0_compact_pc_invariant_owner_v1.log";;
D411Checkpoint:="ci/out/d972_r07_a0_compact_pc_invariant_owner_v1.checkpoint.json";;
D411Script:="ci/out/d972_r07_a0_compact_pc_invariant_owner_v1.sh";;
if IsExistingFile(D411Receipt) or IsExistingFile(D411Verdict) or
   IsExistingFile(D411Log) or IsExistingFile(D411Script) or
   (not IsBound(D411Resume) and IsExistingFile(D411Checkpoint)) then
  Error("task411 stale output");
fi;
D411S:=OutputTextFile(D411Script,false);;
if D411S=fail then Error("task411 script open"); fi;
SetPrintFormattingStatus(D411S,false);;
PrintTo(D411S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D411S,"test \"$(wc -c < ",D411Producer,")\" = \"",String(D411ProducerBytes),"\"\n");;
PrintTo(D411S,"test \"$(sha256sum ",D411Producer," | awk '{print $1}')\" = \"",D411ProducerSHA,"\"\n");;
PrintTo(D411S,"test \"$(wc -c < ",D411Checker,")\" = \"",String(D411CheckerBytes),"\"\n");;
PrintTo(D411S,"test \"$(sha256sum ",D411Checker," | awk '{print $1}')\" = \"",D411CheckerSHA,"\"\n");;
if IsBound(D411Resume) then
  PrintTo(D411S,"D411CP=",D411Resume,"\n");;
  PrintTo(D411S,"python3 -u -B ",D411Producer,
    " --mode PRODUCTION --output ",D411Receipt," --resume ",D411Resume,
    " --checkpoint ",D411Resume," --seconds 6000",
    " 2>&1 | tee ",D411Log,"\n");;
else
  PrintTo(D411S,"D411CP=",D411Checkpoint,"\n");;
  PrintTo(D411S,"python3 -u -B ",D411Producer,
    " --mode PRODUCTION --output ",D411Receipt," --checkpoint ",D411Checkpoint," --seconds 6000",
    " 2>&1 | tee ",D411Log,"\n");;
fi;
PrintTo(D411S,"for attempt in 1 2; do\n");;
PrintTo(D411S,"  if test -f ",D411Receipt," && grep -q '\"status\":\"UNKNOWN_RESOURCE\"' ",D411Receipt," && test -f \"$D411CP\"; then\n");;
  PrintTo(D411S,"    python3 -u -B ",D411Producer,
  " --mode PRODUCTION --output ",D411Receipt," --resume \"$D411CP\"",
  " --checkpoint \"$D411CP\" --seconds 6000 2>&1 | tee -a ",D411Log,"\n");;
PrintTo(D411S,"  else break; fi\n");;
PrintTo(D411S,"done\n");;
PrintTo(D411S,"cat ",D411Log,"\n");;
PrintTo(D411S,"python3 -u -B ",D411Checker,
  " --producer ",D411Receipt,
  " 2>&1 | tee ",D411Verdict,"\n");;
CloseStream(D411S);;
Exec(Concatenation("chmod +x ",D411Script));;
Exec(D411Script);;
Print("R07_A0_COMPACT_PC_OWNER_GHA_DONE\n");
