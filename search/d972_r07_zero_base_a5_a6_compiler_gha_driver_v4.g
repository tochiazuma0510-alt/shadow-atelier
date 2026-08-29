#############################################################################
## R07 direct-relator A5/A6 v4 production driver. ASCII only.
#############################################################################
if not IsBound(D370Mode) then Error("task370 MODE required"); fi;
if D370Mode<>"PRODUCTION" then Error("task370 production-only mode"); fi;
if not IsBound(D370Task193Receipt) then Error("task370 task193 receipt required"); fi;
if not IsBound(D370Task193Verdict) then Error("task370 task193 verdict required"); fi;

D370Producer:="search/d972_r07_zero_base_a5_a6_compiler_v4.py";;
D370Checker:="crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v4.py";;
D370ProducerBytes:=59239;;
D370ProducerSHA:="3949c5b98432cabebef989304cb70201266d48b7bdd71a6301a955000a9755c7";;
D370CheckerBytes:=45942;;
D370CheckerSHA:="cc88aeed18c4f14481971595ab22070720f68ce3fbe48f1057ecd89b610178aa";;
D370Receipt:="ci/out/d972_r07_zero_base_a5_a6_compiler_v4.json";;
D370Verdict:="ci/out/d972_r07_zero_base_a5_a6_compiler_v4.checker.json";;
D370ProducerLog:="ci/out/d972_r07_zero_base_a5_a6_compiler_v4.producer.log";;
D370CheckerLog:="ci/out/d972_r07_zero_base_a5_a6_compiler_v4.checker.log";;
D370Script:="ci/out/d972_r07_zero_base_a5_a6_compiler_v4.sh";;
D370OK:="ci/out/d972_r07_zero_base_a5_a6_compiler_v4.ok";;

D370SafeInput:=function(path)
  local bad;
  if not IsString(path) or Length(path)<7 or path{[1..6]}<>"ci/in/" then
    return false;
  fi;
  for bad in [" ","'","\"",";","&","|","$","(",")","<",">"] do
    if Position(path,bad[1])<>fail then return false; fi;
  od;
  if Position(path,CharInt(96))<>fail then return false; fi;
  return true;
end;;
if not D370SafeInput(D370Task193Receipt) then Error("task370 bad task193 receipt path"); fi;
if not D370SafeInput(D370Task193Verdict) then Error("task370 bad task193 verdict path"); fi;

for D370Path in [D370Receipt,D370Verdict,D370ProducerLog,D370CheckerLog,
                 D370Script,D370OK] do
  if IsExistingFile(D370Path) then Error("task370 stale output ",D370Path); fi;
od;
Exec("mkdir -p ci/out");;
D370S:=OutputTextFile(D370Script,false);;
if D370S=fail then Error("task370 script open"); fi;
SetPrintFormattingStatus(D370S,false);;
PrintTo(D370S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D370S,"test \"$(wc -c < ",D370Producer,")\" = \"",
  String(D370ProducerBytes),"\"\n");;
PrintTo(D370S,"test \"$(sha256sum ",D370Producer,
  " | awk '{print $1}')\" = \"",D370ProducerSHA,"\"\n");;
PrintTo(D370S,"test \"$(wc -c < ",D370Checker,")\" = \"",
  String(D370CheckerBytes),"\"\n");;
PrintTo(D370S,"test \"$(sha256sum ",D370Checker,
  " | awk '{print $1}')\" = \"",D370CheckerSHA,"\"\n");;
PrintTo(D370S,"python3 -u -B ",D370Producer,
  " --mode PRODUCTION --task193-receipt ",D370Task193Receipt,
  " --task193-verdict ",D370Task193Verdict,
  " --output ",D370Receipt," > ",D370ProducerLog," 2>&1\n");;
PrintTo(D370S,"cat ",D370ProducerLog,"\n");;
PrintTo(D370S,"p=$(sed -n 's/^R07_ZERO_BASE_A5_A6_COMPILER_V4_PRODUCER_TERMINAL //p' ",
  D370ProducerLog,")\n");;
PrintTo(D370S,"case \"$p\" in R07_ZERO_BASE_A5_A6_MEMBER|R07_ZERO_BASE_A5_A6_NONMEMBER) ;; *) exit 1;; esac\n");;
PrintTo(D370S,"grep -q '\"status\":\"COMPLETE\"' ",D370Receipt,"\n");;
PrintTo(D370S,"python3 -u -B ",D370Checker,
  " --mode PRODUCTION --task193-receipt ",D370Task193Receipt,
  " --task193-verdict ",D370Task193Verdict,
  " --receipt ",D370Receipt," --output ",D370Verdict,
  " > ",D370CheckerLog," 2>&1\n");;
PrintTo(D370S,"cat ",D370CheckerLog,"\n");;
PrintTo(D370S,"c=$(sed -n 's/^R07_ZERO_BASE_A5_A6_COMPILER_V4_CHECKER terminal=//p' ",
  D370CheckerLog,")\n");;
PrintTo(D370S,"test \"$c\" = \"$p\"\n");;
PrintTo(D370S,"grep -q '\"status\":\"ACCEPTED\"' ",D370Verdict,"\n");;
PrintTo(D370S,"grep -q '\"terminal\":\"'\"$p\"'\"' ",D370Verdict,"\n");;
PrintTo(D370S,"test -s ",D370Receipt," && test -s ",D370Verdict,
  " && test -s ",D370ProducerLog," && test -s ",D370CheckerLog,"\n");;
PrintTo(D370S,"printf '%s\\n' 'R07_ZERO_BASE_A5_A6_COMPILER_V4_DRIVER_COMPLETE' > ",
  D370OK,"\n");;
CloseStream(D370S);;
Exec(Concatenation("bash ",D370Script));;
if not IsExistingFile(D370OK) then Error("task370 missing success marker"); fi;
Print("R07_ZERO_BASE_A5_A6_COMPILER_V4_DRIVER_COMPLETE\n");;
