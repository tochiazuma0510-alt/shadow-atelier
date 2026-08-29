#############################################################################
## Dedicated A0-v18 to task193 input adapter v3; production only, ASCII.
#############################################################################
if not IsBound(D359Mode) then Error("task359 MODE required"); fi;
if D359Mode<>"PRODUCTION" then Error("task359 production-only mode"); fi;
if not IsBound(D359A0Receipt) then Error("task359 A0 receipt path required"); fi;
if not IsBound(D359A0Verdict) then Error("task359 A0 verdict path required"); fi;

D359Producer:="search/d972_r07_history_free_task193_compat_adapter_v3.py";;
D359ProducerBytes:=14038;;
D359ProducerSHA:="7be27b31f0c6e4acf0948341dfaae9d9d880b204774d04660a77982c0546245c";;
D359Checker:="crosscheck/check_d972_r07_history_free_task193_compat_adapter_v3.py";;
D359CheckerBytes:=16804;;
D359CheckerSHA:="f123daeec769aff9254bf913514f0792f20a2f32725aa19bd0020dc84e4c0c6f";;
if not IsBound(D359AdapterReceipt) then D359AdapterReceipt:="ci/out/d972_r07_history_free_task193_compat_adapter_v3.json";; fi;
if not IsBound(D359Attestation) then D359Attestation:="ci/out/d972_r07_history_free_task193_compat_adapter_v3.attestation";; fi;
if not IsBound(D359CheckerVerdict) then D359CheckerVerdict:="ci/out/d972_r07_history_free_task193_compat_adapter_v3.checker.json";; fi;
D359OK:="ci/out/d972_r07_history_free_task193_compat_adapter_v3.ok";;
D359Log:="ci/out/d972_r07_history_free_task193_compat_adapter_v3.producer.log";;
D359CheckLog:="ci/out/d972_r07_history_free_task193_compat_adapter_v3.checker.log";;
D359Script:="ci/out/d972_r07_history_free_task193_compat_adapter_v3.sh";;

D359Safe:=function(path)
  local bad;
  if not IsString(path) or Length(path)=0 then return false; fi;
  if Length(path)<7 or path{[1..7]}<>"ci/in/" then return false; fi;
  for bad in [" ","'","\"",";","&","|","`","$","(",")","<",">"] do
    if Position(path,bad[1])<>fail then return false; fi;
  od;
  return true;
end;;
if not D359Safe(D359A0Receipt) or not D359Safe(D359A0Verdict) then
  Error("task359 A0 path outside fixed allowlist");
fi;
for D359Path in [D359AdapterReceipt,D359Attestation,D359CheckerVerdict,D359OK,D359Log,D359CheckLog,D359Script] do
  if IsExistingFile(D359Path) then Error("task359 stale output ",D359Path); fi;
od;

Exec("mkdir -p ci/out");;
D359S:=OutputTextFile(D359Script,false);;
if D359S=fail then Error("task359 script open"); fi;
SetPrintFormattingStatus(D359S,false);;
PrintTo(D359S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D359S,"python3 -u -B ",D359Producer,
  " --a0-receipt ",D359A0Receipt,
  " --a0-verdict ",D359A0Verdict,
  " --output ",D359AdapterReceipt,
  " --attestation-output ",D359Attestation,
  " > ",D359Log," 2>&1\n");;
PrintTo(D359S,"cat ",D359Log,"\n");;
PrintTo(D359S,"python3 -u -B ",D359Checker,
  " --a0-receipt ",D359A0Receipt,
  " --a0-verdict ",D359A0Verdict,
  " --adapter-receipt ",D359AdapterReceipt,
  " --attestation ",D359Attestation,
  " --output ",D359CheckerVerdict,
  " > ",D359CheckLog," 2>&1\n");;
PrintTo(D359S,"cat ",D359CheckLog,"\n");;
PrintTo(D359S,"p=$(sed -n 's/^R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_TERMINAL //p' ",D359Log,");\n");;
PrintTo(D359S,"c=$(sed -n 's/^R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_CHECKER terminal=//p' ",D359CheckLog,");\n");;
PrintTo(D359S,"test -n \"$p\" && test \"$p\" = \"$c\"\n");;
PrintTo(D359S,"case \"$p\" in R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_A0_REPLAY|UNKNOWN_INPUT:*) ;; *) echo terminal-not-allowed >&2; exit 1;; esac\n");;
PrintTo(D359S,"test -s ",D359AdapterReceipt," && test -s ",D359Attestation," && test -s ",D359CheckerVerdict,"\n");;
PrintTo(D359S,"printf '%s\\n' 'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_DRIVER_COMPLETE' > ",D359OK,"\n");
CloseStream(D359S);;
Exec(Concatenation("bash ",D359Script));;
if not IsExistingFile(D359OK) then Error("task359 missing success marker after Exec"); fi;
Print("R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_DRIVER_COMPLETE\n");;
