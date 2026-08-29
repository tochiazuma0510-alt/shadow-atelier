#############################################################################
## Task382 A4 legal relative-source extractor v1. ASCII only; fail closed.
## Default is undispatched.  A dispatch without A4 pins materializes the
## task176-only canonical residual action and returns typed UNKNOWN_INPUT.
#############################################################################

D382Producer:="search/d972_r07_a4_legal_source_extractor_v1.py";;
D382ProducerBytes:=45551;;
D382ProducerSHA:="e0a70e81e8ebad95e95bd30784b3150b4e06608236d22d00569cde1c17a0a885";;
D382Checker:="crosscheck/check_d972_r07_a4_legal_source_extractor_v1.py";;
D382CheckerBytes:=49380;;
D382CheckerSHA:="35bf8d6c91770326efe46669287bdf39c72c951c14d0b5afe72820cc826802fc";;
D382Base:="ci/out/d972_r07_a4_legal_source_extractor_v1_production";;
D382Receipt:=Concatenation(D382Base,".json");;
D382Verdict:=Concatenation(D382Base,".verdict.json");;
D382ProducerLog:=Concatenation(D382Base,".producer.log");;
D382CheckerLog:=Concatenation(D382Base,".checker.log");;
D382ProducerTerminal:=Concatenation(D382Base,".producer.terminal");;
D382CheckerTerminal:=Concatenation(D382Base,".checker.terminal");;
D382Shell:=Concatenation(D382Base,".sh");;
D382OK:=Concatenation(D382Base,".ok");;
D382ProducerPrefix:="R07_A4_LEGAL_SOURCE_EXTRACTOR_V1_PRODUCER_TERMINAL";;
D382CheckerPrefix:="R07_A4_LEGAL_SOURCE_EXTRACTOR_V1_CHECKER_TERMINAL";;
D382Pass:="A4_LEGAL_RELATIVE_SOURCE_COMPLETE";;
D382Sentinel:="R07_A4_LEGAL_SOURCE_EXTRACTOR_V1_DRIVER_PASS";;

if not IsBound(D382Dispatch) then D382Dispatch:=false;; fi;

if D382Dispatch then
  D382A4Bindings:=[IsBound(D382A4ReceiptPath),IsBound(D382A4ReceiptBytes),
                   IsBound(D382A4ReceiptSHA),IsBound(D382A4VerdictPath),
                   IsBound(D382A4VerdictBytes),IsBound(D382A4VerdictSHA)];;
  D382A4Count:=Number(D382A4Bindings,x->x=true);;
  if D382A4Count=0 then
    D382HasA4:=false;;
  elif D382A4Count=6 then
    D382HasA4:=true;;
  else
    Error("task382 A4 receipt/verdict path/bytes/SHA must be all present or all absent");
  fi;

  D382SafeInput:=function(path)
    local bad;
    if not IsString(path) or Length(path)<7 or path{[1..6]}<>"ci/in/" then
      return false;
    fi;
    for bad in [" ","'","\"",";","&","|","`","$","(",")","<",">"] do
      if Position(path,bad[1])<>fail then return false; fi;
    od;
    return true;
  end;;
  D382LowerHex:=function(value)
    local c;
    if not IsString(value) or Length(value)<>64 then return false; fi;
    for c in value do
      if Position("0123456789abcdef",c)=fail then return false; fi;
    od;
    return true;
  end;;
  if D382HasA4 then
    if not D382SafeInput(D382A4ReceiptPath) or
       not D382SafeInput(D382A4VerdictPath) or
       not IsInt(D382A4ReceiptBytes) or D382A4ReceiptBytes<=0 or
       not IsInt(D382A4VerdictBytes) or D382A4VerdictBytes<=0 or
       not D382LowerHex(D382A4ReceiptSHA) or
       not D382LowerHex(D382A4VerdictSHA) then
      Error("task382 invalid future A4 pins");
    fi;
  fi;

  for D382Path in [D382Receipt,D382Verdict,D382ProducerLog,D382CheckerLog,
                   D382ProducerTerminal,D382CheckerTerminal,D382Shell,D382OK] do
    if IsExistingFile(D382Path) then Error("task382 stale output ",D382Path); fi;
  od;

  Exec("mkdir -p ci/out");;
  D382Stream:=OutputTextFile(D382Shell,false);;
  if D382Stream=fail then Error("task382 shell open"); fi;
  SetPrintFormattingStatus(D382Stream,false);;
  PrintTo(D382Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
  PrintTo(D382Stream,"for command in python3 timeout tee grep sed cmp wc sha256sum; do command -v \"$command\" >/dev/null; done\n");
  PrintTo(D382Stream,"test \"$(wc -c < ",D382Producer,")\" = \"",
    String(D382ProducerBytes),"\"\n");
  PrintTo(D382Stream,"test \"$(sha256sum ",D382Producer,
    " | awk '{print $1}')\" = \"",D382ProducerSHA,"\"\n");
  PrintTo(D382Stream,"test \"$(wc -c < ",D382Checker,")\" = \"",
    String(D382CheckerBytes),"\"\n");
  PrintTo(D382Stream,"test \"$(sha256sum ",D382Checker,
    " | awk '{print $1}')\" = \"",D382CheckerSHA,"\"\n");
  if D382HasA4 then
    PrintTo(D382Stream,"test \"$(wc -c < ",D382A4ReceiptPath,")\" = \"",
      String(D382A4ReceiptBytes),"\"\n");
    PrintTo(D382Stream,"test \"$(sha256sum ",D382A4ReceiptPath,
      " | awk '{print $1}')\" = \"",D382A4ReceiptSHA,"\"\n");
    PrintTo(D382Stream,"test \"$(wc -c < ",D382A4VerdictPath,")\" = \"",
      String(D382A4VerdictBytes),"\"\n");
    PrintTo(D382Stream,"test \"$(sha256sum ",D382A4VerdictPath,
      " | awk '{print $1}')\" = \"",D382A4VerdictSHA,"\"\n");
  fi;
  PrintTo(D382Stream,"set +e\n");
  PrintTo(D382Stream,"timeout --foreground 14700s python3 -u -B ",D382Producer,
    " --mode PRODUCTION --output ",D382Receipt);
  if D382HasA4 then
    PrintTo(D382Stream," --a4-receipt ",D382A4ReceiptPath,
      " --a4-receipt-bytes ",String(D382A4ReceiptBytes),
      " --a4-receipt-sha256 ",D382A4ReceiptSHA,
      " --a4-verdict ",D382A4VerdictPath,
      " --a4-verdict-bytes ",String(D382A4VerdictBytes),
      " --a4-verdict-sha256 ",D382A4VerdictSHA);
  fi;
  PrintTo(D382Stream," 2>&1 | tee ",D382ProducerLog,"\n");
  PrintTo(D382Stream,"producer_pipeline_status=(\"$","{PIPESTATUS[@]}\")\n");
  PrintTo(D382Stream,"set -e\n");
  PrintTo(D382Stream,"if [ \"$","{producer_pipeline_status[0]}\" -ne 0 ]; then exit \"$",
    "{producer_pipeline_status[0]}\"; fi\n");
  PrintTo(D382Stream,"if [ \"$","{producer_pipeline_status[1]}\" -ne 0 ]; then exit \"$",
    "{producer_pipeline_status[1]}\"; fi\n");
  PrintTo(D382Stream,"test -s ",D382Receipt," -a -s ",D382ProducerLog,"\n");
  PrintTo(D382Stream,"test \"$(grep -c '^",D382ProducerPrefix," ' ",D382ProducerLog,
    ")\" -eq 1\n");
  PrintTo(D382Stream,"grep -E '^",D382ProducerPrefix," ' ",D382ProducerLog,
    " | sed 's/^",D382ProducerPrefix," //' > ",D382ProducerTerminal,"\n");
  PrintTo(D382Stream,"set +e\n");
  PrintTo(D382Stream,"timeout --foreground 14700s python3 -u -B ",D382Checker,
    " --mode PRODUCTION --producer ",D382Receipt," --output ",D382Verdict);
  if D382HasA4 then
    PrintTo(D382Stream," --a4-receipt ",D382A4ReceiptPath,
      " --a4-receipt-bytes ",String(D382A4ReceiptBytes),
      " --a4-receipt-sha256 ",D382A4ReceiptSHA,
      " --a4-verdict ",D382A4VerdictPath,
      " --a4-verdict-bytes ",String(D382A4VerdictBytes),
      " --a4-verdict-sha256 ",D382A4VerdictSHA);
  fi;
  PrintTo(D382Stream," 2>&1 | tee ",D382CheckerLog,"\n");
  PrintTo(D382Stream,"checker_pipeline_status=(\"$","{PIPESTATUS[@]}\")\n");
  PrintTo(D382Stream,"set -e\n");
  PrintTo(D382Stream,"if [ \"$","{checker_pipeline_status[0]}\" -ne 0 ]; then exit \"$",
    "{checker_pipeline_status[0]}\"; fi\n");
  PrintTo(D382Stream,"if [ \"$","{checker_pipeline_status[1]}\" -ne 0 ]; then exit \"$",
    "{checker_pipeline_status[1]}\"; fi\n");
  PrintTo(D382Stream,"test -s ",D382Verdict," -a -s ",D382CheckerLog,"\n");
  PrintTo(D382Stream,"test \"$(grep -c '^",D382CheckerPrefix," ' ",D382CheckerLog,
    ")\" -eq 1\n");
  PrintTo(D382Stream,"grep -E '^",D382CheckerPrefix," ' ",D382CheckerLog,
    " | sed 's/^",D382CheckerPrefix," //' > ",D382CheckerTerminal,"\n");
  PrintTo(D382Stream,"test \"$(wc -l < ",D382ProducerTerminal,")\" -eq 1\n");
  PrintTo(D382Stream,"test \"$(wc -l < ",D382CheckerTerminal,")\" -eq 1\n");
  PrintTo(D382Stream,"cmp -s ",D382ProducerTerminal," ",D382CheckerTerminal,"\n");
  PrintTo(D382Stream,"terminal=$(tr -d '\\n' < ",D382ProducerTerminal,")\n");
  PrintTo(D382Stream,"case \"$terminal\" in\n");
  PrintTo(D382Stream,"  ",D382Pass,") true ;;\n");
  PrintTo(D382Stream,"  UNKNOWN_INPUT) true ;;\n");
  PrintTo(D382Stream,"  UNKNOWN_RESOURCE) true ;;\n");
  PrintTo(D382Stream,"  *) exit 1 ;;\n");
  PrintTo(D382Stream,"esac\n");
  if not D382HasA4 then
    PrintTo(D382Stream,"test \"$terminal\" = \"UNKNOWN_INPUT\"\n");
  fi;
  PrintTo(D382Stream,"printf '%s' '",D382Sentinel,"' > ",D382OK,"\n");
  CloseStream(D382Stream);;
  Exec(Concatenation("bash ",D382Shell));;
  D382Observed:=StringFile(D382OK);;
  if D382Observed<>D382Sentinel then Error("task382 sentinel mismatch"); fi;
  Print(D382Sentinel,"\n");
else
  Print("R07_A4_LEGAL_SOURCE_EXTRACTOR_V1_UNDISPATCHED\n");
fi;
