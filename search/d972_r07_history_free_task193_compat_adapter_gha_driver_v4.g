#############################################################################
## Dedicated exact-pin A0-v20 to task193 adapter v4; production only, ASCII.
#############################################################################
if not IsBound(D359Mode) then Error("task359 MODE required"); fi;
if D359Mode<>"PRODUCTION" then Error("task359 production-only mode"); fi;
if not IsBound(D359A0Receipt) then Error("task359 A0 receipt path required"); fi;
if not IsBound(D359A0Verdict) then Error("task359 A0 verdict path required"); fi;

D359A0Producer:="search/d972_r07_history_free_positive_fast_resume_v20.py";;
D359A0ProducerBytes:=10739;;
D359A0ProducerSHA:="cf775975304a56cd3587470074e31d3a2000fba418fab5793fd25d6307150ed7";;
D359A0Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v20.py";;
D359A0CheckerBytes:=5327;;
D359A0CheckerSHA:="7c0a1c8b862f8dd62224e0f4ebc0d50ae7ea2de86c63ffb67e025cba98d7c077";;
D359A0Driver:="search/d972_r07_history_free_positive_fast_resume_gha_driver_v20.g";;
D359A0DriverBytes:=6907;;
D359A0DriverSHA:="f9cfffc8e38082a4ff4d24b608ccb0eab5d9a53ba36169264d440827ad6918d4";;
D359Producer:="search/d972_r07_history_free_task193_compat_adapter_v4.py";;
D359ProducerBytes:=2426;;
D359ProducerSHA:="0174b1508f50708352e8607edfb0a210508680e58a295763b2d287fda32889b9";;
D359Checker:="crosscheck/check_d972_r07_history_free_task193_compat_adapter_v4.py";;
D359CheckerBytes:=3105;;
D359CheckerSHA:="4269368c006e19fa0cc71da78d12927f8fbd4c85087f0e5b5ca11688a8f58d06";;
if not IsBound(D359AdapterReceipt) then D359AdapterReceipt:="ci/out/d972_r07_history_free_task193_compat_adapter_v4.json";; fi;
if not IsBound(D359Attestation) then D359Attestation:="ci/out/d972_r07_history_free_task193_compat_adapter_v4.attestation";; fi;
if not IsBound(D359CheckerVerdict) then D359CheckerVerdict:="ci/out/d972_r07_history_free_task193_compat_adapter_v4.checker.json";; fi;
D359OK:="ci/out/d972_r07_history_free_task193_compat_adapter_v4.ok";;
D359Log:="ci/out/d972_r07_history_free_task193_compat_adapter_v4.producer.log";;
D359CheckLog:="ci/out/d972_r07_history_free_task193_compat_adapter_v4.checker.log";;
D359Script:="ci/out/d972_r07_history_free_task193_compat_adapter_v4.sh";;

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

D359Read:=function(path)
  local x;
  x:=StringFile(path);
  if x=fail or Length(x)=0 then Error("task359 missing pinned source ",path); fi;
  return x;
end;;
D359Pin:=function(path,n,h)
  local x;
  x:=D359Read(path);
  if Length(x)<>n or HexSHA256(x)<>h then Error("task359 source pin drift ",path); fi;
end;;
D359Pin(D359A0Producer,D359A0ProducerBytes,D359A0ProducerSHA);
D359Pin(D359A0Checker,D359A0CheckerBytes,D359A0CheckerSHA);
D359Pin(D359A0Driver,D359A0DriverBytes,D359A0DriverSHA);
D359Pin(D359Producer,D359ProducerBytes,D359ProducerSHA);
D359Pin(D359Checker,D359CheckerBytes,D359CheckerSHA);

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
PrintTo(D359S,"p=$(sed -n 's/^R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V4_TERMINAL //p' ",D359Log,");\n");;
PrintTo(D359S,"c=$(sed -n 's/^R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V4_CHECKER terminal=//p' ",D359CheckLog,");\n");;
PrintTo(D359S,"test -n \"$p\" && test \"$p\" = \"$c\"\n");;
PrintTo(D359S,"case \"$p\" in R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V4_A0_REPLAY|UNKNOWN_INPUT:*) ;; *) echo terminal-not-allowed >&2; exit 1;; esac\n");;
PrintTo(D359S,"test -s ",D359AdapterReceipt," && test -s ",D359Attestation," && test -s ",D359CheckerVerdict,"\n");;
PrintTo(D359S,"printf '%s\\n' 'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V4_DRIVER_COMPLETE' > ",D359OK,"\n");
CloseStream(D359S);;
Exec(Concatenation("bash ",D359Script));;
if not IsExistingFile(D359OK) then Error("task359 missing success marker after Exec"); fi;
Print("R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V4_DRIVER_COMPLETE\n");;
