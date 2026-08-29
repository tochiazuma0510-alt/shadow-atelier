#############################################################################
## Dedicated exact-pin A0-v22 to task193 adapter v5; production only, ASCII.
#############################################################################
if not IsBound(D391Mode) then Error("task391 MODE required"); fi;
if D391Mode<>"PRODUCTION" then Error("task391 production-only mode"); fi;
if not IsBound(D391A0Receipt) then Error("task391 A0 receipt path required"); fi;
if not IsBound(D391A0Verdict) then Error("task391 A0 verdict path required"); fi;

D391A0Producer:="search/d972_r07_history_free_positive_fast_resume_v22.py";;
D391A0ProducerBytes:=3280;;
D391A0ProducerSHA:="1cc875afb05b7c3db189d7a77fd6d9d4e2604610a0af6a383895011ecbdd0d01";;
D391A0Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v22.py";;
D391A0CheckerBytes:=2066;;
D391A0CheckerSHA:="4c79b841b5ce003e4d2eefaf1320e878aab400c20ef1a23e4f2900ea61e5cf13";;
D391A0Driver:="search/d972_r07_history_free_positive_fast_resume_gha_driver_v22.g";;
D391A0DriverBytes:=8266;;
D391A0DriverSHA:="8b8f2e9a1dc0b6a30e61ab8866c8d2393328a7038c22323873350d91d5b6531d";;
D391Producer:="search/d972_r07_history_free_task193_compat_adapter_v5.py";;
D391ProducerBytes:=2453;;
D391ProducerSHA:="024fe7c5d5ac23f248b30275f4f97d4bf512980a4dc17e249b981fd18649355f";;
D391Checker:="crosscheck/check_d972_r07_history_free_task193_compat_adapter_v5.py";;
D391CheckerBytes:=3145;;
D391CheckerSHA:="4c7d89fdc3f4a5399f3abef0d5380a26958bcb48d5caab95ec27fc0c23a89556";;
if not IsBound(D391AdapterReceipt) then D391AdapterReceipt:="ci/out/d972_r07_history_free_task193_compat_adapter_v5.json";; fi;
if not IsBound(D391Attestation) then D391Attestation:="ci/out/d972_r07_history_free_task193_compat_adapter_v5.attestation";; fi;
if not IsBound(D391CheckerVerdict) then D391CheckerVerdict:="ci/out/d972_r07_history_free_task193_compat_adapter_v5.checker.json";; fi;
D391OK:="ci/out/d972_r07_history_free_task193_compat_adapter_v5.ok";;
D391Log:="ci/out/d972_r07_history_free_task193_compat_adapter_v5.producer.log";;
D391CheckLog:="ci/out/d972_r07_history_free_task193_compat_adapter_v5.checker.log";;
D391Script:="ci/out/d972_r07_history_free_task193_compat_adapter_v5.sh";;

D391Safe:=function(path)
  local bad;
  if not IsString(path) or Length(path)=0 then return false; fi;
  if Length(path)<7 or path{[1..7]}<>"ci/in/" then return false; fi;
  for bad in [" ","'","\"",";","&","|","`","$","(",")","<",">"] do
    if Position(path,bad[1])<>fail then return false; fi;
  od;
  return true;
end;;
if not D391Safe(D391A0Receipt) or not D391Safe(D391A0Verdict) then
  Error("task391 A0 path outside fixed allowlist");
fi;

D391Read:=function(path)
  local x;
  x:=StringFile(path);
  if x=fail or Length(x)=0 then Error("task391 missing pinned source ",path); fi;
  return x;
end;;
D391Pin:=function(path,n,h)
  local x;
  x:=D391Read(path);
  if Length(x)<>n or HexSHA256(x)<>h then Error("task391 source pin drift ",path); fi;
end;;
D391Pin(D391A0Producer,D391A0ProducerBytes,D391A0ProducerSHA);
D391Pin(D391A0Checker,D391A0CheckerBytes,D391A0CheckerSHA);
D391Pin(D391A0Driver,D391A0DriverBytes,D391A0DriverSHA);
D391Pin(D391Producer,D391ProducerBytes,D391ProducerSHA);
D391Pin(D391Checker,D391CheckerBytes,D391CheckerSHA);

for D391Path in [D391AdapterReceipt,D391Attestation,D391CheckerVerdict,D391OK,D391Log,D391CheckLog,D391Script] do
  if IsExistingFile(D391Path) then Error("task391 stale output ",D391Path); fi;
od;

Exec("mkdir -p ci/out");;
D391S:=OutputTextFile(D391Script,false);;
if D391S=fail then Error("task391 script open"); fi;
SetPrintFormattingStatus(D391S,false);;
PrintTo(D391S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D391S,"python3 -u -B ",D391Producer,
  " --a0-receipt ",D391A0Receipt,
  " --a0-verdict ",D391A0Verdict,
  " --output ",D391AdapterReceipt,
  " --attestation-output ",D391Attestation,
  " > ",D391Log," 2>&1\n");;
PrintTo(D391S,"cat ",D391Log,"\n");;
PrintTo(D391S,"python3 -u -B ",D391Checker,
  " --a0-receipt ",D391A0Receipt,
  " --a0-verdict ",D391A0Verdict,
  " --adapter-receipt ",D391AdapterReceipt,
  " --attestation ",D391Attestation,
  " --output ",D391CheckerVerdict,
  " > ",D391CheckLog," 2>&1\n");;
PrintTo(D391S,"cat ",D391CheckLog,"\n");;
PrintTo(D391S,"p=$(sed -n 's/^R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V5_TERMINAL //p' ",D391Log,");\n");;
PrintTo(D391S,"c=$(sed -n 's/^R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V5_CHECKER terminal=//p' ",D391CheckLog,");\n");;
PrintTo(D391S,"test -n \"$p\" && test \"$p\" = \"$c\"\n");;
PrintTo(D391S,"case \"$p\" in R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V5_A0_REPLAY|UNKNOWN_INPUT:*) ;; *) echo terminal-not-allowed >&2; exit 1;; esac\n");;
PrintTo(D391S,"test -s ",D391AdapterReceipt," && test -s ",D391Attestation," && test -s ",D391CheckerVerdict,"\n");;
PrintTo(D391S,"printf '%s\\n' 'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V5_DRIVER_COMPLETE' > ",D391OK,"\n");
CloseStream(D391S);;
Exec(Concatenation("bash ",D391Script));;
if not IsExistingFile(D391OK) then Error("task391 missing success marker after Exec"); fi;
Print("R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V5_DRIVER_COMPLETE\n");;
