#############################################################################
## d972_b4_norm_tietze_gap_driver_v3.g
##
## One generic gap-run job for the canonical 100-step/61-generator lane:
##   (1) Python producer v4, (2) independent Python checker v3,
##   (3) explicit KBMAG consumer v4.
##
## All paths and commands are source constants.  Only integer mode/cap
## switches may be supplied by a quote-free dispatch preamble.  There is no
## QUIT: this file is safe in GAP Read context.
#############################################################################

D972NTZV3TracePath := "ci/out/d972_b4_norm_tietze_trace_v4.json";;
D972NTZV3CheckPath := "ci/out/d972_b4_norm_tietze_dense_check_v3.json";;
D972NTZV3ConsumerPath := "ci/out/d972_b4_norm_tietze_kbmag_v4.json";;
D972NTZV3DriverPath := "ci/out/d972_b4_norm_tietze_gap_driver_v3.json";;
D972NTZV3InputPath :=
  "search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972NTZV3WordsPath :=
  "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972NTZV3ProducerPath := "search/d972_b4_norm_tietze_trace_v4.py";;
D972NTZV3CheckerPath :=
  "crosscheck/check_d972_b4_norm_tietze_dense_v3.py";;
D972NTZV3ConsumerScript :=
  "search/d972_b4_norm_tietze_kbmag_consumer_v4.g";;

D972NTZV3Selftest := 0;;
if IsBound(D972_B4_NORM_TZ_SELFTEST) then
  D972NTZV3Selftest := D972_B4_NORM_TZ_SELFTEST;
fi;
if not IsInt(D972NTZV3Selftest) or not D972NTZV3Selftest in [0,1] then
  Error("norm Tietze v3 driver: SELFTEST must be integer 0 or 1");
fi;
D972NTZV3Bootstrap := 1;;
if IsBound(D972_B4_NORM_TZ_BOOTSTRAP) then
  D972NTZV3Bootstrap := D972_B4_NORM_TZ_BOOTSTRAP;
fi;
if not IsInt(D972NTZV3Bootstrap) or not D972NTZV3Bootstrap in [0,1] then
  Error("norm Tietze v3 driver: BOOTSTRAP must be integer 0 or 1");
fi;

if IsBound(D972_B4_NORM_TZ_ARTIFACT) and
   D972_B4_NORM_TZ_ARTIFACT<>D972NTZV3TracePath then
  Error("norm Tietze v3 driver: artifact path override rejected");
fi;
if IsBound(D972_B4_NORM_TZ_KBMAG_OUTPUT) and
   D972_B4_NORM_TZ_KBMAG_OUTPUT<>D972NTZV3ConsumerPath then
  Error("norm Tietze v3 driver: KBMAG output override rejected");
fi;

D972NTZV3ShellQuote := function(s)
  local c;
  if not IsString(s) then
    Error("norm Tietze v3 driver: shell path is not a string");
  fi;
  for c in ["'",CharInt(96),"$","\\","\n","\r",";","|","&",
            ">","<","(",")"] do
    if Position(s,c)<>fail then
      Error("norm Tietze v3 driver: unsafe shell path");
    fi;
  od;
  return Concatenation("'",s,"'");
end;;
D972NTZV3Join := function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1];;
  for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972NTZV3Json := function(x)
  local p,i,names;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\"");
  fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if IsInt(x) then return String(x); fi;
  if IsRecord(x) then
    names:=SortedList(RecNames(x));;
    p:=List(names,i->Concatenation("\"",i,"\":",D972NTZV3Json(x.(i))));;
    return Concatenation("{",D972NTZV3Join(p,","),"}");
  fi;
  if not IsList(x) then
    Error("norm Tietze v3 driver: JSON type drift");
  fi;
  p:=List([1..Length(x)],i->D972NTZV3Json(x[i]));;
  return Concatenation("[",D972NTZV3Join(p,","),"]");
end;;
D972NTZV3WriteJson := function(path,obj)
  local f;
  f:=OutputTextFile(path,false);;
  if f=fail then Error("norm Tietze v3 driver: cannot open receipt"); fi;
  SetPrintFormattingStatus(f,false);;
  PrintTo(f,Concatenation(D972NTZV3Json(obj),"\n"));;
  CloseStream(f);;
end;;
D972NTZV3RunFixed := function(label,command,status_path,log_path)
  local full,raw;
  full:=Concatenation(
    "rm -f ",D972NTZV3ShellQuote(status_path),"; ",command,
    " > ",D972NTZV3ShellQuote(log_path)," 2>&1; ",
    "rc=$?; printf '%s' \"$rc\" > ",
    D972NTZV3ShellQuote(status_path));;
  Exec(full);;
  raw:=StringFile(status_path);;
  if raw=fail or raw<>"0" then
    Error(Concatenation("norm Tietze v3 driver: ",label,
      " exit status is not zero"));
  fi;
  return true;
end;;

if D972NTZV3Selftest=1 then
  if D972NTZV3TracePath<>
       "ci/out/d972_b4_norm_tietze_trace_v4.json" or
     D972NTZV3CheckPath<>
       "ci/out/d972_b4_norm_tietze_dense_check_v3.json" or
     D972NTZV3ConsumerPath<>
       "ci/out/d972_b4_norm_tietze_kbmag_v4.json" or
     D972NTZV3ProducerPath<>
       "search/d972_b4_norm_tietze_trace_v4.py" or
     D972NTZV3CheckerPath<>
       "crosscheck/check_d972_b4_norm_tietze_dense_v3.py" then
    Error("norm Tietze v3 driver: fixed path selftest drift");
  fi;
  Print("B4_NORM_TZ_GAP_DRIVER_V3_SELFTEST_FINAL_MARKER ",
    "producer=v4-step100 checker=v3-step100 consumer=v4\n");
else
  if D972NTZV3Bootstrap=1 then
    ## The subshell keeps the GAP working directory at the repository root.
    D972NTZV3BuildCommand:=Concatenation(
      "( mkdir -p ",D972NTZV3ShellQuote("/home/runner/gap/pkg/kbmag"),
      " && cd ",D972NTZV3ShellQuote("/home/runner/gap/pkg/kbmag"),
      " && ./configure ",D972NTZV3ShellQuote("/home/runner/gap"),
      " && make -j2 )");;
    D972NTZV3RunFixed("KBMAG bootstrap",D972NTZV3BuildCommand,
      "/tmp/d972_b4_norm_tietze_gap_driver_v3_bootstrap.status",
      "ci/out/d972_b4_norm_tietze_gap_driver_v3_bootstrap.log");
    Print("B4_NORM_TZ_GAP_DRIVER_V3_BOOTSTRAP_PASS\n");
  fi;
  if LoadPackage("json")<>true then
    Error("norm Tietze v3 driver: json package unavailable");
  fi;
  if LoadPackage("kbmag")<>true then
    Error("norm Tietze v3 driver: kbmag package unavailable");
  fi;
  Print("B4_NORM_TZ_GAP_DRIVER_V3_PACKAGE_PASS\n");

  D972NTZV3ProducerCommand:=Concatenation(
    "mkdir -p ",D972NTZV3ShellQuote("ci/out"),
    " && python3 -B ",D972NTZV3ShellQuote(D972NTZV3ProducerPath),
    " --input ",D972NTZV3ShellQuote(D972NTZV3InputPath),
    " --word-artifact ",D972NTZV3ShellQuote(D972NTZV3WordsPath),
    " --output ",D972NTZV3ShellQuote(D972NTZV3TracePath));;
  D972NTZV3RunFixed("producer",D972NTZV3ProducerCommand,
    "/tmp/d972_b4_norm_tietze_gap_driver_v3_producer.status",
    "ci/out/d972_b4_norm_tietze_gap_driver_v3_producer.log");
  D972NTZV3TraceRaw:=StringFile(D972NTZV3TracePath);;
  if D972NTZV3TraceRaw=fail then
    Error("norm Tietze v3 driver: producer receipt missing");
  fi;
  Print("B4_NORM_TZ_GAP_DRIVER_V3_PRODUCER_PASS sha256=",
    HexSHA256(D972NTZV3TraceRaw),"\n");

  D972NTZV3CheckerCommand:=Concatenation(
    "python3 -B ",D972NTZV3ShellQuote(D972NTZV3CheckerPath)," ",
    D972NTZV3ShellQuote(D972NTZV3TracePath)," --input ",
    D972NTZV3ShellQuote(D972NTZV3InputPath)," --word-artifact ",
    D972NTZV3ShellQuote(D972NTZV3WordsPath)," --output ",
    D972NTZV3ShellQuote(D972NTZV3CheckPath));;
  D972NTZV3RunFixed("independent checker",D972NTZV3CheckerCommand,
    "/tmp/d972_b4_norm_tietze_gap_driver_v3_checker.status",
    "ci/out/d972_b4_norm_tietze_gap_driver_v3_checker.log");
  D972NTZV3CheckRaw:=StringFile(D972NTZV3CheckPath);;
  if D972NTZV3CheckRaw=fail then
    Error("norm Tietze v3 driver: checker receipt missing");
  fi;
  D972NTZV3CheckObj:=JsonStringToGap(D972NTZV3CheckRaw);;
  if not IsRecord(D972NTZV3CheckObj) or
     D972NTZV3CheckObj.schema<>
       "d972-b4-norm-tietze-dense-check/v3" or
     D972NTZV3CheckObj.producer_receipt_sha256<>
       HexSHA256(D972NTZV3TraceRaw) or
     D972NTZV3CheckObj.source_sha256<>
       "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9" or
     D972NTZV3CheckObj.raw_rs_relators_sha256<>
       "29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e" or
     D972NTZV3CheckObj.norm_rs_words_sha256<>
       "f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8" or
     D972NTZV3CheckObj.status<>"UNKNOWN_STAGE_LIMIT" or
     D972NTZV3CheckObj.steps_replayed<>100 or
     D972NTZV3CheckObj.final_generator_count<>61 or
     D972NTZV3CheckObj.stock_kbmag_max_generators<>63 or
     D972NTZV3CheckObj.final_norm_empty_count<>2 or
     D972NTZV3CheckObj.all_norms_empty<>false or
     D972NTZV3CheckObj.final_relators_sha256<>
       "2327388540e9095b2c7ca9b6d0d1f9de2295e3400b0430bdf97b672d02ce745" or
     D972NTZV3CheckObj.final_norm_words_sha256<>
       "325aecb390f4c8107a92be3cca8ed16f396f1baec49b973488f8822b43bf4d70" or
     D972NTZV3CheckObj.independent_raw_rs_replay<>true or
     D972NTZV3CheckObj.independent_norm_replay<>true or
     D972NTZV3CheckObj.independent_tietze_replay<>true or
     D972NTZV3CheckObj.independent_dense_map_replay<>true or
     D972NTZV3CheckObj.terminal_claim<>
       "NONE; KBMAG/AutomaticStructure replay still required" then
    Error("norm Tietze v3 driver: independent checker gate failed");
  fi;
  Print("B4_NORM_TZ_GAP_DRIVER_V3_CHECK_PASS status=",
    D972NTZV3CheckObj.status," final_generators=",
    D972NTZV3CheckObj.final_generator_count," norm_empty=",
    D972NTZV3CheckObj.final_norm_empty_count,"/972\n");

  D972_B4_NORM_TZ_ARTIFACT:=D972NTZV3TracePath;;
  D972_B4_NORM_TZ_KBMAG_OUTPUT:=D972NTZV3ConsumerPath;;
  Read(D972NTZV3ConsumerScript);;
  D972NTZV3ConsumerRaw:=StringFile(D972NTZV3ConsumerPath);;
  if D972NTZV3ConsumerRaw=fail then
    Error("norm Tietze v3 driver: KBMAG receipt missing");
  fi;
  D972NTZV3ConsumerObj:=JsonStringToGap(D972NTZV3ConsumerRaw);;
  if not IsRecord(D972NTZV3ConsumerObj) or
     D972NTZV3ConsumerObj.schema<>
       "d972-b4-norm-tietze-kbmag/v4" or
     D972NTZV3ConsumerObj.artifact_sha256<>
       HexSHA256(D972NTZV3TraceRaw) or
     D972NTZV3ConsumerObj.final_generator_count<>61 or
     D972NTZV3ConsumerObj.stock_max_generators<>63 or
     D972NTZV3ConsumerObj.norm_count<>972 or
     not D972NTZV3ConsumerObj.status in [
       "ALL_972_EMPTY_CANDIDATE_NEEDS_REPLAY",
       "B4_A_SIDE_CANDIDATE_NEEDS_REPLAY",
       "UNKNOWN_NO_COMPLETE_REDUCTION"] or
     D972NTZV3ConsumerObj.proof_level<>
       "KBMAG_CANDIDATE_INDEPENDENT_TZ_REPLAY_REQUIRED" then
    Error("norm Tietze v3 driver: KBMAG receipt gate failed");
  fi;
  D972NTZV3WriteJson(D972NTZV3DriverPath,rec(
    schema:="d972-b4-norm-tietze-gap-driver/v3",
    status:="KBMAG_CANDIDATE_PENDING_REPLAY",
    lane:="step100-dense61",
    bootstrap_requested:=D972NTZV3Bootstrap,
    producer_exit_code:=0,checker_exit_code:=0,
    producer_receipt_sha256:=HexSHA256(D972NTZV3TraceRaw),
    checker_receipt_sha256:=HexSHA256(D972NTZV3CheckRaw),
    checker_status:=D972NTZV3CheckObj.status,
    checker_final_generator_count:=D972NTZV3CheckObj.final_generator_count,
    checker_final_norm_empty_count:=D972NTZV3CheckObj.final_norm_empty_count,
    checker_final_relators_sha256:=D972NTZV3CheckObj.final_relators_sha256,
    checker_final_norm_words_sha256:=D972NTZV3CheckObj.final_norm_words_sha256,
    consumer_receipt_sha256:=HexSHA256(D972NTZV3ConsumerRaw),
    consumer_status:=D972NTZV3ConsumerObj.status,
    consumer_proof_level:=D972NTZV3ConsumerObj.proof_level,
    producer_command:=D972NTZV3ProducerCommand,
    checker_command:=D972NTZV3CheckerCommand,
    consumer_script:=D972NTZV3ConsumerScript,
    terminal_claim:="NONE; independent rewrite ancestry is absent"));
  Print("B4_NORM_TZ_GAP_DRIVER_V3_FINAL_MARKER status=",
    D972NTZV3ConsumerObj.status," checker=PASS consumer=PASS output=",
    D972NTZV3DriverPath,"\n");
fi;
