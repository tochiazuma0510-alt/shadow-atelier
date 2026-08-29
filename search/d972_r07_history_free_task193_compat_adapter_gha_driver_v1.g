#############################################################################
## A0 v18 to task193 v1 compatibility adapter; production only.
## ASCII only.  No SELFTEST, fixture, retry, or task193 search is launched.
#############################################################################
if not IsBound(D357Mode) then Error("task357 MODE required"); fi;
if D357Mode<>"PRODUCTION" then Error("task357 production-only mode"); fi;
if not IsBound(D357A0Receipt) then Error("task357 A0 receipt path required"); fi;
if not IsBound(D357A0Verdict) then Error("task357 A0 verdict path required"); fi;

D357Producer:="search/d972_r07_history_free_task193_compat_adapter_v1.py";;
D357ProducerBytes:=17928;;
D357ProducerSHA:="2ebdc6890316160a3d2f71b1b03f0c12132171e0933031d50ddec3e3be912cf3";;
D357Checker:="crosscheck/check_d972_r07_history_free_task193_compat_adapter_v1.py";;
D357CheckerBytes:=17801;;
D357CheckerSHA:="dbf8894d681d4bd73cf698ce378c3a2ac9ba1162d382ec4b20d3df9a534b752a";;
if not IsBound(D357Output) then
  D357Output:="ci/out/d972_r07_history_free_task193_compat_adapter_v1.task186.json";;
fi;
if not IsBound(D357Attestation) then
  D357Attestation:="ci/out/d972_r07_history_free_task193_compat_adapter_v1.task186.attestation";;
fi;
D357Log:="ci/out/d972_r07_history_free_task193_compat_adapter_v1.producer.log";;
D357CheckLog:="ci/out/d972_r07_history_free_task193_compat_adapter_v1.checker.log";;
D357Script:="ci/out/d972_r07_history_free_task193_compat_adapter_v1.sh";;

D357Read:=function(path)
  local raw;
  raw:=StringFile(path);
  if raw=fail or Length(raw)=0 then Error("task357 missing owner ",path); fi;
  return raw;
end;;
D357Pin:=function(path,bytes,sha)
  local raw;
  raw:=D357Read(path);
  if Length(raw)<>bytes or HexSHA256(raw)<>sha then
    Error("task357 owner pin drift ",path);
  fi;
end;;
D357Pin(D357Producer,D357ProducerBytes,D357ProducerSHA);;
D357Pin(D357Checker,D357CheckerBytes,D357CheckerSHA);;

for D357Path in [D357Output,D357Attestation,D357Log,D357CheckLog,D357Script] do
  if IsExistingFile(D357Path) then Error("task357 stale output ",D357Path); fi;
od;

Exec("mkdir -p ci/out");;
D357S:=OutputTextFile(D357Script,false);;
if D357S=fail then Error("task357 script open"); fi;
SetPrintFormattingStatus(D357S,false);;
PrintTo(D357S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D357S,"python3 -u -B ",D357Producer,
  " --a0-receipt ",D357A0Receipt,
  " --a0-verdict ",D357A0Verdict,
  " --output ",D357Output,
  " --attestation-output ",D357Attestation,
  " > ",D357Log," 2>&1\n");;
PrintTo(D357S,"cat ",D357Log,"\n");;
PrintTo(D357S,"python3 -u -B ",D357Checker,
  " --a0-receipt ",D357A0Receipt,
  " --a0-verdict ",D357A0Verdict,
  " --task186-receipt ",D357Output,
  " --attestation ",D357Attestation,
  " > ",D357CheckLog," 2>&1\n");;
PrintTo(D357S,"cat ",D357CheckLog,"\n");;
PrintTo(D357S,"printf 'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V1_DRIVER_PASS\\n'\n");;
CloseStream(D357S);;
Exec(Concatenation("bash ",D357Script));;
Print("R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V1_DRIVER_PASS\n");;
