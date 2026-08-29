#############################################################################
## Task193 v2 adapter-fed affine-prefix compiler; production-only ASCII.
#############################################################################
if not IsBound(D193Mode) then Error("task193 MODE required"); fi;
if D193Mode<>"PRODUCTION" then Error("task193 production-only mode"); fi;
if not IsBound(D193AdapterReceipt) then Error("task193 adapter receipt path required"); fi;
if not IsBound(D193AdapterVerdict) then Error("task193 adapter verdict path required"); fi;

D193Producer:="search/d972_r07_second_frattini_affine_prefix_compiler_v2.py";;
D193ProducerBytes:=22937;;
D193ProducerSHA:="65a45189e120ae58f99310a9189fd4f88802e269d3c1a61bf5e68e879eebde88";;
D193Checker:="crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v2.py";;
D193CheckerBytes:=32933;;
D193CheckerSHA:="fdb80b02030a82d4d6cfccc6246c915c14b896e91e126b2b7ba5c22a6dc99ea5";;
D193Receipt:="ci/out/d972_r07_second_frattini_affine_prefix_compiler_v2.json";;
D193CheckerVerdict:="ci/out/d972_r07_second_frattini_affine_prefix_compiler_v2.checker.json";;
D193OK:="ci/out/d972_r07_second_frattini_affine_prefix_compiler_v2.ok";;
D193ProducerLog:="ci/out/d972_r07_second_frattini_affine_prefix_compiler_v2.producer.log";;
D193CheckerLog:="ci/out/d972_r07_second_frattini_affine_prefix_compiler_v2.checker.log";;
D193Script:="ci/out/d972_r07_second_frattini_affine_prefix_compiler_v2.sh";;
if not IsBound(D193Resume) then D193Resume:=""; fi;
D193ResumePath:="ci/in/d972_r07_second_frattini_affine_prefix_compiler_v2.checkpoint.json";;

D193Safe:=function(path)
  local bad;
  if not IsString(path) or Length(path)=0 then return false; fi;
  if Length(path)<7 or path{[1..7]}<>"ci/in/" then return false; fi;
  for bad in [" ","'","\"",";","&","|","`","$","(",")","<",">"] do
    if Position(path,bad[1])<>fail then return false; fi;
  od;
  return true;
end;;
if not D193Safe(D193AdapterReceipt) or not D193Safe(D193AdapterVerdict) then
  Error("task193 adapter path outside fixed allowlist");
fi;
if D193Resume<>"" and D193Resume<>D193ResumePath then Error("task193 unsafe resume path"); fi;

D193Read:=function(path) local x; x:=StringFile(path); if x=fail or Length(x)=0 then Error("task193 missing pinned source ",path); fi; return x; end;;
D193Pin:=function(path,n,h) local x; x:=D193Read(path); if Length(x)<>n or HexSHA256(x)<>h then Error("task193 source pin drift ",path); fi; end;;
D193Pin(D193Producer,D193ProducerBytes,D193ProducerSHA);
D193Pin(D193Checker,D193CheckerBytes,D193CheckerSHA);
if D193Resume<>"" then D193Read(D193ResumePath); fi;
for D193Path in [D193Receipt,D193CheckerVerdict,D193OK,D193ProducerLog,D193CheckerLog,D193Script] do
  if IsExistingFile(D193Path) then Error("task193 stale output ",D193Path); fi;
od;

Exec("mkdir -p ci/out");;
D193S:=OutputTextFile(D193Script,false);;
if D193S=fail then Error("task193 script open"); fi;
SetPrintFormattingStatus(D193S,false);;
PrintTo(D193S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D193S,"python3 -u -B ",D193Producer,
  " --adapter-receipt ",D193AdapterReceipt,
  " --adapter-verdict ",D193AdapterVerdict,
  " --output ",D193Receipt);
if D193Resume<>"" then PrintTo(D193S," --resume ",D193ResumePath); fi;
PrintTo(D193S," > ",D193ProducerLog," 2>&1\n");;
PrintTo(D193S,"cat ",D193ProducerLog,"\n");;
PrintTo(D193S,"p=$(sed -n 's/^R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2_PRODUCER_TERMINAL //p' ",D193ProducerLog,");\n");;
PrintTo(D193S,"test \"$(grep -Ec '^R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2_PRODUCER_TERMINAL (R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2|UNKNOWN_INPUT:[^[:cntrl:]]+|UNKNOWN_RESOURCE:phase=[^:]+:cap=[^:]+:value=[0-9]+:limit=[0-9]+)$' ",D193ProducerLog,\")\" -eq 1\n");;
PrintTo(D193S,"python3 -u -B ",D193Checker,
  " --adapter-receipt ",D193AdapterReceipt,
  " --adapter-verdict ",D193AdapterVerdict,
  " --receipt ",D193Receipt,
  " --output ",D193CheckerVerdict,
  " > ",D193CheckerLog," 2>&1\n");;
PrintTo(D193S,"cat ",D193CheckerLog,"\n");;
PrintTo(D193S,"c=$(sed -n 's/^R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2_CHECKER_PASS terminal=//p' ",D193CheckerLog,");\n");;
PrintTo(D193S,"test \"$(grep -Ec '^R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2_CHECKER_PASS terminal=(R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2|UNKNOWN_INPUT:[^[:cntrl:]]+|UNKNOWN_RESOURCE:phase=[^:]+:cap=[^:]+:value=[0-9]+:limit=[0-9]+)$' ",D193CheckerLog,\")\" -eq 1\n");;
PrintTo(D193S,"test -n \"$p\" && test \"$p\" = \"$c\"\n");;
PrintTo(D193S,"test -s ",D193Receipt," && test -s ",D193CheckerVerdict,"\n");;
PrintTo(D193S,"printf '%s\\n' 'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2_DRIVER_COMPLETE' > ",D193OK,"\n");
CloseStream(D193S);;
Exec(Concatenation("bash ",D193Script));
if not IsExistingFile(D193OK) then Error("task193 missing success marker after Exec"); fi;
Print("R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2_DRIVER_COMPLETE\n");
