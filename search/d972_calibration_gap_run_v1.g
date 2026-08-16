#############################################################################
## d972_calibration_gap_run_v1.g
##
## Driver for the existing generic .github/workflows/gap-run.yml.
## It runs the committed Python v4 fresh diagnostic, then its independent
## receipt checker.  Every fixed output is below ci/out; no state run or
## artifact input is accepted.  The driver never emits A or B.
##
## The generic workflow prepends a dispatch preamble before Read().  The only
## accepted preamble binding is D972_CALIBRATION_GAP_SELFTEST:=0 or 1.  There
## is deliberately no QUIT, so this file is safe in a GAP Read context.
#############################################################################

D972CGRReceiptPath := "ci/out/d972_calibration_diagnostic_v4.json";;
D972CGRScriptPath := "ci/out/d972_calibration_generated_v4.g";;
D972CGRWorkerPath := "ci/out/d972_frozen_v2_base_presentation.json";;
D972CGRConsolePath := "ci/out/d972_calibration_helper.log";;
D972CGRCheckerLogPath := "ci/out/d972_calibration_checker.log";;
D972CGRDriverPath := "ci/out/d972_calibration_gap_run_v1.json";;
D972CGRHelperStatusPath := "ci/out/d972_calibration_helper.status";;
D972CGRCheckerStatusPath := "ci/out/d972_calibration_checker.status";;
D972CGRHelperPath := "search/d972_calibration_diagnostic_v4.py";;
D972CGRCheckerPath := "search/check_d972_calibration_diagnostic_v4.py";;

D972CGRSelftest := 0;;
if IsBound(D972_CALIBRATION_GAP_SELFTEST) then
  D972CGRSelftest := D972_CALIBRATION_GAP_SELFTEST;
fi;
if not IsInt(D972CGRSelftest) or not D972CGRSelftest in [0,1] then
  Error("D972 calibration gap driver: SELFTEST must be integer 0 or 1");
fi;

D972CGRShellQuote := function(s)
  local c;
  if not IsString(s) then
    Error("D972 calibration gap driver: shell path is not a string");
  fi;
  ## Fixed repository paths need none of these characters.  Reject them so
  ## future edits cannot turn a path into shell syntax.
  if Position(s,CharInt(96))<>fail then
    Error("D972 calibration gap driver: unsafe shell path");
  fi;
  for c in ["'","$","\\","\n","\r",";","|","&",
            ">","<","(",")"] do
    if PositionSublist(s,c)<>fail then
      Error("D972 calibration gap driver: unsafe shell path");
    fi;
  od;
  return Concatenation("'",s,"'");
end;;

D972CGRJoin := function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1];;
  for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;

D972CGRJson := function(x)
  local p,i,names;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if IsInt(x) then return String(x); fi;
  if IsString(x) then
    return Concatenation("\"",ReplacedString(
      ReplacedString(x,"\\","\\\\"),"\"","\\\""),"\"");
  fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsRecord(x) then
    names:=SortedList(RecNames(x));;
    p:=List(names,i->Concatenation("\"",i,"\":",
      D972CGRJson(x.(i))));;
    return Concatenation("{",D972CGRJoin(p,","),"}");
  fi;
  if not IsList(x) then
    Error("D972 calibration gap driver: JSON type drift");
  fi;
  p:=List([1..Length(x)],i->D972CGRJson(x[i]));;
  return Concatenation("[",D972CGRJoin(p,","),"]");
end;;

D972CGRWriteJson := function(path,obj)
  local f;
  f:=OutputTextFile(path,false);;
  if f=fail then
    Error("D972 calibration gap driver: cannot open driver receipt");
  fi;
  SetPrintFormattingStatus(f,false);;
  PrintTo(f,Concatenation(D972CGRJson(obj),"\n"));;
  CloseStream(f);
end;;

## Run one source-constant command.  Exec() does not expose a portable exit
## status in all GAP builds, so the shell writes an explicit status file.
D972CGRRunFixed := function(command,status_path,log_path)
  local full,raw;
  full:=Concatenation(
    "rm -f ",D972CGRShellQuote(status_path),"; ",command,
    " > ",D972CGRShellQuote(log_path)," 2>&1; ",
    "rc=$?; printf '%s' \"$rc\" > ",
    D972CGRShellQuote(status_path));;
  Exec(full);;
  raw:=StringFile(status_path);;
  if raw=fail then return "MISSING"; fi;
  return raw;
end;;

D972CGRRead := function(path)
  return StringFile(path);
end;;

if D972CGRSelftest=1 then
  if D972CGRReceiptPath<>"ci/out/d972_calibration_diagnostic_v4.json" or
     D972CGRScriptPath<>"ci/out/d972_calibration_generated_v4.g" or
     D972CGRWorkerPath<>"ci/out/d972_frozen_v2_base_presentation.json" or
     D972CGRHelperPath<>"search/d972_calibration_diagnostic_v4.py" or
     D972CGRCheckerPath<>"search/check_d972_calibration_diagnostic_v4.py" then
    Error("D972 calibration gap driver: fixed path selftest drift");
  fi;
  D972CGRWriteJson(D972CGRDriverPath,rec(
    schema:="d972-calibration-gap-run/v1",
    mode:="fresh", status:="SELFTEST_PASS",
    helper_exit_code:=0, checker_exit_code:=0,
    receipt_present:=false, generated_script_present:=false,
    worker_output_present:=false,
    terminal_claim:="NONE; diagnostic only"));
  Print("D972_CALIBRATION_GAP_RUN_FINAL_MARKER status=SELFTEST_PASS\n");
else
  D972CGRHelperCommand:=Concatenation(
    "mkdir -p ",D972CGRShellQuote("ci/out")," && python3 -B ",
    D972CGRShellQuote(D972CGRHelperPath)," --mode fresh --receipt ",
    D972CGRShellQuote(D972CGRReceiptPath)," --script-output ",
    D972CGRShellQuote(D972CGRScriptPath)," --worker-output ",
    D972CGRShellQuote(D972CGRWorkerPath));;
  D972CGRHelperRc:=D972CGRRunFixed(D972CGRHelperCommand,
    D972CGRHelperStatusPath,D972CGRConsolePath);;

  ## Run the independent checker even when helper status is nonzero.  This
  ## preserves a valid UNKNOWN receipt and rejects missing/tampered output.
  D972CGRCheckerCommand:=Concatenation(
    "python3 -B ",D972CGRShellQuote(D972CGRCheckerPath),
    " --receipt ",D972CGRShellQuote(D972CGRReceiptPath),
    " --script ",D972CGRShellQuote(D972CGRScriptPath),
    " --worker-output ",D972CGRShellQuote(D972CGRWorkerPath));;
  D972CGRCheckerRc:=D972CGRRunFixed(D972CGRCheckerCommand,
    D972CGRCheckerStatusPath,D972CGRCheckerLogPath);;

  D972CGRReceiptRaw:=D972CGRRead(D972CGRReceiptPath);;
  D972CGRScriptRaw:=D972CGRRead(D972CGRScriptPath);;
  D972CGRWorkerRaw:=D972CGRRead(D972CGRWorkerPath);;
  D972CGRReceiptPresent:=D972CGRReceiptRaw<>fail;
  D972CGRScriptPresent:=D972CGRScriptRaw<>fail;
  D972CGRWorkerPresent:=D972CGRWorkerRaw<>fail;
  D972CGRPass:=D972CGRHelperRc="0" and D972CGRCheckerRc="0" and
    D972CGRReceiptPresent and D972CGRScriptPresent and D972CGRWorkerPresent;
  if D972CGRPass then D972CGRStatus:="CALIBRATION_PASS_CANDIDATE";
  else D972CGRStatus:="FAIL_CLOSED_UNKNOWN"; fi;
  D972CGRReceiptSha:="";;
  if D972CGRReceiptPresent then
    D972CGRReceiptSha:=HexSHA256(D972CGRReceiptRaw);
  fi;

  D972CGRWriteJson(D972CGRDriverPath,rec(
    schema:="d972-calibration-gap-run/v1",
    mode:="fresh", status:=D972CGRStatus,
    helper_exit_code:=D972CGRHelperRc,
    checker_exit_code:=D972CGRCheckerRc,
    receipt_present:=D972CGRReceiptPresent,
    generated_script_present:=D972CGRScriptPresent,
    worker_output_present:=D972CGRWorkerPresent,
    receipt_sha256:=D972CGRReceiptSha,
    checker_log_path:=D972CGRCheckerLogPath,
    helper_log_path:=D972CGRConsolePath,
    terminal_claim:="NONE; diagnostic only"));
  Print("D972_CALIBRATION_GAP_RUN_FINAL_MARKER status=",D972CGRStatus,
    " helper_rc=",D972CGRHelperRc," checker_rc=",D972CGRCheckerRc,
    " receipt=",D972CGRReceiptPath,"\n");
  ## gap-run.yml uploads artifacts only after a successful GAP step.  Keep the
  ## process alive after this terminal marker so a failed helper/checker still
  ## has its fail-closed receipt/logs uploaded; the marker/receipt status is
  ## never upgraded to A or B.
fi;
