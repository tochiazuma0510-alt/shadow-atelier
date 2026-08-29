#############################################################################
## Task395 C_rel occurrence closure v3. ASCII only; default undispatched.
#############################################################################

D395Producer:="search/d972_r07_crel_occurrence_closure_v3.py";;
D395ProducerBytes:=26765;;
D395ProducerSHA:="8d1ee5d06fd5dc760c2df1fa760cb64280903c2a10561b4340f93ed313deb817";;
D395Checker:="crosscheck/check_d972_r07_crel_occurrence_closure_v3.py";;
D395CheckerBytes:=35157;;
D395CheckerSHA:="7409847c42581631495cadae549e7cff019d4f9e30c6398b679fb9e5e50b829c";;
D395Base:="ci/out/d972_r07_crel_occurrence_closure_v3";;
D395Receipt:=Concatenation(D395Base,".json");;
D395Verdict:=Concatenation(D395Base,".verdict.json");;
D395Checkpoint:=Concatenation(D395Base,".checkpoint.json");;
D395ProducerLog:=Concatenation(D395Base,".producer.log");;
D395CheckerLog:=Concatenation(D395Base,".checker.log");;
D395ProducerTerminal:=Concatenation(D395Base,".producer.terminal");;
D395CheckerTerminal:=Concatenation(D395Base,".checker.terminal");;
D395Shell:=Concatenation(D395Base,".sh");;
D395OK:=Concatenation(D395Base,".ok");;
D395ProducerPrefix:="CREL_OCCURRENCE_CLOSURE_V3_PRODUCER_TERMINAL";;
D395CheckerPrefix:="CREL_OCCURRENCE_CLOSURE_V3_CHECKER_TERMINAL";;
D395Pass:="CREL_OCCURRENCE_CLOSURE_COMPLETE";;
D395Sentinel:="CREL_OCCURRENCE_CLOSURE_V3_DRIVER_PASS";;
if not IsBound(D395Dispatch) then D395Dispatch:=false;; fi;
if not IsBound(D395Task382ReceiptPath) then D395Task382ReceiptPath:="ci/in/FUTURE_TASK382_RECEIPT.json";; fi;
if not IsBound(D395Task382ReceiptBytes) then D395Task382ReceiptBytes:=0;; fi;
if not IsBound(D395Task382ReceiptSHA) then D395Task382ReceiptSHA:="";; fi;
if not IsBound(D395Task382VerdictPath) then D395Task382VerdictPath:="ci/in/FUTURE_TASK382_VERDICT.json";; fi;
if not IsBound(D395Task382VerdictBytes) then D395Task382VerdictBytes:=0;; fi;
if not IsBound(D395Task382VerdictSHA) then D395Task382VerdictSHA:="";; fi;

if D395Dispatch then
  if D395ProducerBytes<=0 or Length(D395ProducerSHA)<>64 or
     D395CheckerBytes<=0 or Length(D395CheckerSHA)<>64 then
    Error("task395 source pins are not bound");
  fi;
  D395Safe:=function(path)
    local bad;
    if not IsString(path) or Length(path)<7 or path{[1..6]}<>"ci/in/" then return false; fi;
    for bad in [" ","'","\"",";","&","|","`","$","(",")","<",">"] do
      if Position(path,bad[1])<>fail then return false; fi;
    od;
    return true;
  end;;
  D395Hex:=function(value)
    local c;
    if not IsString(value) or Length(value)<>64 then return false; fi;
    for c in value do if Position("0123456789abcdef",c)=fail then return false; fi; od;
    return true;
  end;;
  if not D395Safe(D395Task382ReceiptPath) or not D395Safe(D395Task382VerdictPath) or
     not IsInt(D395Task382ReceiptBytes) or D395Task382ReceiptBytes<=0 or
     not IsInt(D395Task382VerdictBytes) or D395Task382VerdictBytes<=0 or
     not D395Hex(D395Task382ReceiptSHA) or not D395Hex(D395Task382VerdictSHA) then
    Error("task395 future task382 pins are incomplete or unsafe");
  fi;
  for D395Path in [D395Receipt,D395Verdict,D395Checkpoint,D395ProducerLog,
                   D395CheckerLog,D395ProducerTerminal,D395CheckerTerminal,
                   D395Shell,D395OK] do
    if IsExistingFile(D395Path) then Error("task395 stale output ",D395Path); fi;
  od;
  Exec("mkdir -p ci/out");;
  D395Stream:=OutputTextFile(D395Shell,false);;
  if D395Stream=fail then Error("task395 shell open"); fi;
  SetPrintFormattingStatus(D395Stream,false);;
  PrintTo(D395Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
  PrintTo(D395Stream,"for command in python3 timeout tee grep sed wc sha256sum; do command -v \"$command\" >/dev/null; done\n");
  PrintTo(D395Stream,"test \"$(wc -c < ",D395Producer,")\" = \"",String(D395ProducerBytes),"\"\n");
  PrintTo(D395Stream,"test \"$(sha256sum ",D395Producer," | awk '{print $1}')\" = \"",D395ProducerSHA,"\"\n");
  PrintTo(D395Stream,"test \"$(wc -c < ",D395Checker,")\" = \"",String(D395CheckerBytes),"\"\n");
  PrintTo(D395Stream,"test \"$(sha256sum ",D395Checker," | awk '{print $1}')\" = \"",D395CheckerSHA,"\"\n");
  PrintTo(D395Stream,"test \"$(wc -c < ",D395Task382ReceiptPath,")\" = \"",String(D395Task382ReceiptBytes),"\"\n");
  PrintTo(D395Stream,"test \"$(sha256sum ",D395Task382ReceiptPath," | awk '{print $1}')\" = \"",D395Task382ReceiptSHA,"\"\n");
  PrintTo(D395Stream,"test \"$(wc -c < ",D395Task382VerdictPath,")\" = \"",String(D395Task382VerdictBytes),"\"\n");
  PrintTo(D395Stream,"test \"$(sha256sum ",D395Task382VerdictPath," | awk '{print $1}')\" = \"",D395Task382VerdictSHA,"\"\n");
  PrintTo(D395Stream,"set +e\n");
  PrintTo(D395Stream,"timeout --foreground 14700s python3 -u -B ",D395Producer,
    " --mode PRODUCTION --task382-receipt ",D395Task382ReceiptPath,
    " --task382-receipt-bytes ",String(D395Task382ReceiptBytes),
    " --task382-receipt-sha256 ",D395Task382ReceiptSHA,
    " --task382-verdict ",D395Task382VerdictPath,
    " --task382-verdict-bytes ",String(D395Task382VerdictBytes),
    " --task382-verdict-sha256 ",D395Task382VerdictSHA,
    " --output ",D395Receipt," --checkpoint ",D395Checkpoint,
    " 2>&1 | tee ",D395ProducerLog,"\n");
  PrintTo(D395Stream,"producer_pipeline_status=(\"$","{PIPESTATUS[@]}\")\nset -e\n");
  PrintTo(D395Stream,"test \"$","{producer_pipeline_status[0]}\" -eq 0 -a \"$","{producer_pipeline_status[1]}\" -eq 0\n");
  PrintTo(D395Stream,"test -s ",D395Receipt," -a -s ",D395ProducerLog,"\n");
  PrintTo(D395Stream,"test \"$(grep -c '^",D395ProducerPrefix," ' ",D395ProducerLog,")\" -eq 1\n");
  PrintTo(D395Stream,"grep -E '^",D395ProducerPrefix," ' ",D395ProducerLog," | sed 's/^",D395ProducerPrefix," //' > ",D395ProducerTerminal,"\n");
  PrintTo(D395Stream,"set +e\n");
  PrintTo(D395Stream,"timeout --foreground 14700s python3 -u -B ",D395Checker,
    " --mode CROSSCHECK --task382-receipt ",D395Task382ReceiptPath,
    " --task382-receipt-bytes ",String(D395Task382ReceiptBytes),
    " --task382-receipt-sha256 ",D395Task382ReceiptSHA,
    " --task382-verdict ",D395Task382VerdictPath,
    " --task382-verdict-bytes ",String(D395Task382VerdictBytes),
    " --task382-verdict-sha256 ",D395Task382VerdictSHA,
    " --producer-receipt ",D395Receipt," --producer-receipt-bytes $(wc -c < ",D395Receipt,")",
    " --producer-receipt-sha256 $(sha256sum ",D395Receipt," | awk '{print $1}')",
    " --output ",D395Verdict," --checkpoint ",D395Checkpoint,
    " 2>&1 | tee ",D395CheckerLog,"\n");
  PrintTo(D395Stream,"checker_pipeline_status=(\"$","{PIPESTATUS[@]}\")\nset -e\n");
  PrintTo(D395Stream,"test \"$","{checker_pipeline_status[0]}\" -eq 0 -a \"$","{checker_pipeline_status[1]}\" -eq 0\n");
  PrintTo(D395Stream,"test -s ",D395Verdict," -a -s ",D395CheckerLog,"\n");
  PrintTo(D395Stream,"test \"$(grep -c '^",D395CheckerPrefix," ' ",D395CheckerLog,")\" -eq 1\n");
  PrintTo(D395Stream,"grep -E '^",D395CheckerPrefix," ' ",D395CheckerLog," | sed 's/^",D395CheckerPrefix," //' > ",D395CheckerTerminal,"\n");
  PrintTo(D395Stream,"test \"$(wc -l < ",D395ProducerTerminal,")\" -eq 1 -a \"$(wc -l < ",D395CheckerTerminal,")\" -eq 1\n");
  PrintTo(D395Stream,"terminal=$(tr -d '\\n' < ",D395ProducerTerminal,")\ncase \"$terminal\" in ",D395Pass,") true ;; UNKNOWN_INPUT:*|UNKNOWN_RESOURCE:*) true ;; *) exit 1 ;; esac\n");
  PrintTo(D395Stream,"checker_terminal=$(tr -d '\\n' < ",D395CheckerTerminal,")\ncase \"$checker_terminal\" in ",D395Pass,") true ;; UNKNOWN_INPUT:*|UNKNOWN_RESOURCE:*) true ;; *) exit 1 ;; esac\n");
  PrintTo(D395Stream,"cmp -s ",D395ProducerTerminal," ",D395CheckerTerminal,"\n");
  PrintTo(D395Stream,"printf '%s' '",D395Sentinel,"' > ",D395OK,"\n");
  CloseStream(D395Stream);;
  Exec(Concatenation("bash ",D395Shell));;
  if StringFile(D395OK)<>D395Sentinel then Error("task395 sentinel mismatch"); fi;
  Print(D395Sentinel,"\n");
else
  Print("CREL_OCCURRENCE_CLOSURE_V3_UNDISPATCHED\n");
fi;
