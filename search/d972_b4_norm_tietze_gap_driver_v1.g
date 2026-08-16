#############################################################################
## d972_b4_norm_tietze_gap_driver_v1.g
##
## Single-job GAP driver for the fixed canonical Python/Tietze lane:
##   1. producer v2 (raw RS 161/5056 -> 34 elementary steps),
##   2. independent dense checker, and
##   3. explicit dense KBMAG consumer.
##
## The generic gap-run workflow reads this file.  Python commands and all
## repository paths are source constants; only the typed mode switches may
## be supplied by the dispatch preamble.  Shell paths are quoted and checked
## before Exec(), and every command writes an explicit exit-code file.
## There is deliberately no QUIT: this file is safe in Read() context.
#############################################################################

D972NTZTracePath := "ci/out/d972_b4_norm_tietze_trace_v2.json";;
D972NTZCheckPath := "ci/out/d972_b4_norm_tietze_dense_check_v1.json";;
D972NTZConsumerPath := "ci/out/d972_b4_norm_tietze_kbmag_v2.json";;
D972NTZDriverPath := "ci/out/d972_b4_norm_tietze_gap_driver_v1.json";;
D972NTZInputPath :=
  "search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972NTZWordsPath :=
  "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972NTZProducerPath := "search/d972_b4_norm_tietze_trace_v2.py";;
D972NTZCheckerPath :=
  "crosscheck/check_d972_b4_norm_tietze_dense_v1.py";;
D972NTZConsumerScript :=
  "search/d972_b4_norm_tietze_kbmag_consumer_v2.g";;

D972NTZSelftest := 0;;
if IsBound(D972_B4_NORM_TZ_SELFTEST) then
  D972NTZSelftest := D972_B4_NORM_TZ_SELFTEST;
fi;
if not IsInt(D972NTZSelftest) or not D972NTZSelftest in [0,1] then
  Error("norm Tietze gap driver: SELFTEST must be integer 0 or 1");
fi;
D972NTZBootstrap := 1;;
if IsBound(D972_B4_NORM_TZ_BOOTSTRAP) then
  D972NTZBootstrap := D972_B4_NORM_TZ_BOOTSTRAP;
fi;
if not IsInt(D972NTZBootstrap) or not D972NTZBootstrap in [0,1] then
  Error("norm Tietze gap driver: BOOTSTRAP must be integer 0 or 1");
fi;

## Do not permit a preamble to redirect the fixed consumer to an arbitrary
## file.  The generic workflow itself still controls the artifact directory,
## but this lane always writes under ci/out as required by the receipt gate.
if IsBound(D972_B4_NORM_TZ_ARTIFACT) and
   D972_B4_NORM_TZ_ARTIFACT<>D972NTZTracePath then
  Error("norm Tietze gap driver: artifact path override rejected");
fi;
if IsBound(D972_B4_NORM_TZ_KBMAG_OUTPUT) and
   D972_B4_NORM_TZ_KBMAG_OUTPUT<>D972NTZConsumerPath then
  Error("norm Tietze gap driver: KBMAG output override rejected");
fi;

D972NTZShellQuote := function(s)
  local c;
  if not IsString(s) then
    Error("norm Tietze gap driver: shell path is not a string");
  fi;
  ## These characters are not needed by any fixed path in this lane.  Reject
  ## them even though the result is single-quoted, so future edits cannot
  ## accidentally turn a path into shell syntax.
  for c in ["'","`","$","\\","\n","\r",";","|","&",
            ">","<","(",")"] do
    if Position(s,c)<>fail then
      Error("norm Tietze gap driver: unsafe shell path");
    fi;
  od;
  return Concatenation("'",s,"'");
end;;

D972NTZJoin := function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1];;
  for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972NTZJson := function(x)
  local p,i,names;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if IsInt(x) then return String(x); fi;
  ## GAP 4.16 also gives [] the string filter; test empty lists first.
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\"");
  fi;
  if IsRecord(x) then
    names:=SortedList(RecNames(x));;
    p:=List(names,i->Concatenation("\"",i,"\":",D972NTZJson(x.(i))));;
    return Concatenation("{",D972NTZJoin(p,","),"}");
  fi;
  if not IsList(x) then
    Error("norm Tietze gap driver: JSON type drift");
  fi;
  p:=List([1..Length(x)],i->D972NTZJson(x[i]));;
  return Concatenation("[",D972NTZJoin(p,","),"]");
end;;
D972NTZWriteJson := function(path,obj)
  local f;
  f:=OutputTextFile(path,false);;
  if f=fail then Error("norm Tietze gap driver: cannot open JSON output"); fi;
  SetPrintFormattingStatus(f,false);;
  PrintTo(f,Concatenation(D972NTZJson(obj),"\n"));;
  CloseStream(f);;
end;;

## Run a source-constant shell command and fail closed unless its explicit
## status file contains exactly zero.  Exec()'s own return value is not used.
D972NTZRunFixed := function(label,command,status_path,log_path)
  local full,raw;
  full:=Concatenation(
    "rm -f ",D972NTZShellQuote(status_path),"; ",command,
    " > ",D972NTZShellQuote(log_path)," 2>&1; ",
    "rc=$?; printf '%s' \"$rc\" > ",D972NTZShellQuote(status_path));;
  Exec(full);;
  raw:=StringFile(status_path);;
  if raw=fail or raw<>"0" then
    Error(Concatenation("norm Tietze gap driver: ",label,
      " exit status is not zero"));
  fi;
  return true;
end;;

if D972NTZSelftest=1 then
  ## This branch performs no package load, Exec, or Python work.  It is a
  ## quote-free generic-run preflight and still emits an explicit marker.
  if D972NTZTracePath<>"ci/out/d972_b4_norm_tietze_trace_v2.json" or
     D972NTZCheckPath<>"ci/out/d972_b4_norm_tietze_dense_check_v1.json" or
     D972NTZConsumerPath<>"ci/out/d972_b4_norm_tietze_kbmag_v2.json" then
    Error("norm Tietze gap driver: fixed path selftest drift");
  fi;
  Print("B4_NORM_TZ_GAP_DRIVER_SELFTEST_FINAL_MARKER producer=FIXED checker=FIXED consumer=FIXED\n");
else
  ## Build the setup-gap KBMAG tree in the Linux runner when requested.  The
  ## paths are literal constants, not preamble data, so this command has no
  ## shell-injection surface.  Dispatch uses BOOTSTRAP=1.
  if D972NTZBootstrap=1 then
    D972NTZBuildCommand:=Concatenation(
      "mkdir -p ",D972NTZShellQuote("/home/runner/gap/pkg/kbmag"),
      " && cd ",D972NTZShellQuote("/home/runner/gap/pkg/kbmag"),
      " && ./configure ",D972NTZShellQuote("/home/runner/gap"),
      " && make -j2");;
    D972NTZRunFixed("KBMAG bootstrap",D972NTZBuildCommand,
      "/tmp/d972_b4_norm_tietze_gap_driver_v1_bootstrap.status",
      "ci/out/d972_b4_norm_tietze_gap_driver_v1_bootstrap.log");
    Print("B4_NORM_TZ_GAP_DRIVER_BOOTSTRAP_PASS\n");
  fi;

  if LoadPackage("json")<>true then
    Error("norm Tietze gap driver: json package unavailable");
  fi;
  if LoadPackage("kbmag")<>true then
    Error("norm Tietze gap driver: kbmag package unavailable");
  fi;
  Print("B4_NORM_TZ_GAP_DRIVER_PACKAGE_PASS\n");

  D972NTZProducerCommand:=Concatenation(
    "mkdir -p ",D972NTZShellQuote("ci/out")," && python3 -B ",
    D972NTZShellQuote(D972NTZProducerPath)," --input ",
    D972NTZShellQuote(D972NTZInputPath)," --word-artifact ",
    D972NTZShellQuote(D972NTZWordsPath)," --max-steps 34 --output ",
    D972NTZShellQuote(D972NTZTracePath));;
  D972NTZRunFixed("producer",D972NTZProducerCommand,
    "/tmp/d972_b4_norm_tietze_gap_driver_v1_producer.status",
    "ci/out/d972_b4_norm_tietze_gap_driver_v1_producer.log");
  D972NTZTraceRaw:=StringFile(D972NTZTracePath);;
  if D972NTZTraceRaw=fail then
    Error("norm Tietze gap driver: producer receipt missing");
  fi;
  Print("B4_NORM_TZ_GAP_DRIVER_PRODUCER_PASS sha256=",
    HexSHA256(D972NTZTraceRaw),"\n");

  D972NTZCheckerCommand:=Concatenation(
    "python3 -B ",D972NTZShellQuote(D972NTZCheckerPath)," ",
    D972NTZShellQuote(D972NTZTracePath)," --input ",
    D972NTZShellQuote(D972NTZInputPath)," --word-artifact ",
    D972NTZShellQuote(D972NTZWordsPath)," --output ",
    D972NTZShellQuote(D972NTZCheckPath));;
  D972NTZRunFixed("independent checker",D972NTZCheckerCommand,
    "/tmp/d972_b4_norm_tietze_gap_driver_v1_checker.status",
    "ci/out/d972_b4_norm_tietze_gap_driver_v1_checker.log");
  D972NTZCheckRaw:=StringFile(D972NTZCheckPath);;
  if D972NTZCheckRaw=fail then
    Error("norm Tietze gap driver: checker receipt missing");
  fi;
  D972NTZCheckObj:=JsonStringToGap(D972NTZCheckRaw);;
  if not IsRecord(D972NTZCheckObj) or
     D972NTZCheckObj.schema<>"d972-b4-norm-tietze-dense-check/v1" or
     D972NTZCheckObj.producer_receipt_sha256<>HexSHA256(D972NTZTraceRaw) or
     D972NTZCheckObj.source_sha256<>
       "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9" or
     D972NTZCheckObj.raw_rs_relators_sha256<>
       "29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e" or
     D972NTZCheckObj.norm_rs_words_sha256<>
       "f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8" or
     D972NTZCheckObj.status<>"UNKNOWN_STAGE_LIMIT" or
     D972NTZCheckObj.steps_replayed<>34 or
     D972NTZCheckObj.final_generator_count<>127 or
     D972NTZCheckObj.final_norm_empty_count<>2 or
     D972NTZCheckObj.all_norms_empty<>false or
     D972NTZCheckObj.final_relators_sha256<>
       "1b4e1e86405dd348d633e706f0a66210df243dc2cbb4a04ed176bb452e2b2439" or
     D972NTZCheckObj.final_norm_words_sha256<>
       "49b90fb6215f425703cd59dc405048edd2db6e7ca24d062e8833473ccaf6042e" or
     D972NTZCheckObj.independent_raw_rs_replay<>true or
     D972NTZCheckObj.independent_norm_replay<>true or
     D972NTZCheckObj.independent_tietze_replay<>true or
     D972NTZCheckObj.independent_dense_map_replay<>true or
     D972NTZCheckObj.terminal_claim<>
       "NONE; KBMAG/AutomaticStructure replay still required" then
    Error("norm Tietze gap driver: independent checker gate failed");
  fi;
  Print("B4_NORM_TZ_GAP_DRIVER_CHECK_PASS status=",
    D972NTZCheckObj.status," final_generators=",
    D972NTZCheckObj.final_generator_count," norm_empty=",
    D972NTZCheckObj.final_norm_empty_count,"/972\n");

  ## The consumer sees exactly the receipt just checked.  Its own status is
  ## intentionally candidate-only; this driver never upgrades an all-empty
  ## ledger to B because no rewrite ancestry is present here.
  D972_B4_NORM_TZ_ARTIFACT:=D972NTZTracePath;;
  D972_B4_NORM_TZ_KBMAG_OUTPUT:=D972NTZConsumerPath;;
  Read(D972NTZConsumerScript);;
  D972NTZConsumerRaw:=StringFile(D972NTZConsumerPath);;
  if D972NTZConsumerRaw=fail then
    Error("norm Tietze gap driver: KBMAG receipt missing");
  fi;
  D972NTZConsumerObj:=JsonStringToGap(D972NTZConsumerRaw);;
  if not IsRecord(D972NTZConsumerObj) or
     D972NTZConsumerObj.schema<>"d972-b4-norm-tietze-kbmag/v2" or
     D972NTZConsumerObj.artifact_sha256<>HexSHA256(D972NTZTraceRaw) or
     D972NTZConsumerObj.norm_count<>972 or
     not D972NTZConsumerObj.status in [
       "ALL_972_EMPTY_CANDIDATE_NEEDS_REPLAY",
       "B4_A_SIDE_CANDIDATE_NEEDS_REPLAY",
       "UNKNOWN_NO_COMPLETE_REDUCTION"] or
     D972NTZConsumerObj.proof_level<>
       "KBMAG_CANDIDATE_INDEPENDENT_TZ_REPLAY_REQUIRED" then
    Error("norm Tietze gap driver: KBMAG candidate receipt gate failed");
  fi;

  D972NTZWriteJson(D972NTZDriverPath,rec(
    schema:="d972-b4-norm-tietze-gap-driver/v1",
    status:="KBMAG_CANDIDATE_PENDING_REPLAY",
    bootstrap_requested:=D972NTZBootstrap,
    producer_exit_code:=0,checker_exit_code:=0,
    producer_receipt_sha256:=HexSHA256(D972NTZTraceRaw),
    checker_receipt_sha256:=HexSHA256(D972NTZCheckRaw),
    checker_status:=D972NTZCheckObj.status,
    checker_final_generator_count:=D972NTZCheckObj.final_generator_count,
    checker_final_norm_empty_count:=D972NTZCheckObj.final_norm_empty_count,
    checker_final_relators_sha256:=D972NTZCheckObj.final_relators_sha256,
    checker_final_norm_words_sha256:=D972NTZCheckObj.final_norm_words_sha256,
    consumer_receipt_sha256:=HexSHA256(D972NTZConsumerRaw),
    consumer_status:=D972NTZConsumerObj.status,
    consumer_proof_level:=D972NTZConsumerObj.proof_level,
    producer_command:=D972NTZProducerCommand,
    checker_command:=D972NTZCheckerCommand,
    consumer_script:=D972NTZConsumerScript,
    terminal_claim:="NONE; independent rewrite ancestry is absent"));
  Print("B4_NORM_TZ_GAP_DRIVER_FINAL_MARKER status=",
    D972NTZConsumerObj.status," checker=PASS consumer=PASS output=",
    D972NTZDriverPath,"\n");
fi;
