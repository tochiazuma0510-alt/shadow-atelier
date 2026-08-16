#############################################################################
## d972_b4_u_magnus4_a18_driver_v1.g
##
## Generic gap-run bridge for the raw-A.18 Magnus4 Python lane:
##   (1) producer, accepting only Python rc 0 or 2;
##   (2) independent checker, requiring rc 0 and a bound JSON receipt.
##
## The producer's rc=2 denotes UNKNOWN all-pass and is intentionally not
## treated as a driver failure.  A producer receipt is still parsed and
## pinned before the checker is started.  This file is ASCII and safe under
## GAP Read; it has no process-exit command.
#############################################################################

D972MAG4A18SourcePath :=
  "search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972MAG4A18WordsPath :=
  "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972MAG4A18ProducerPath :=
  "search/d972_b4_u_magnus4_a18_v1.py";;
D972MAG4A18CheckerPath :=
  "search/check_d972_b4_u_magnus4_a18_v1.py";;
D972MAG4A18ProducerReceiptPath :=
  "ci/out/d972_b4_u_magnus4_a18_v1.json";;
D972MAG4A18CheckerReceiptPath :=
  "ci/out/d972_b4_u_magnus4_a18_v1_check.json";;
D972MAG4A18ProducerLogPath :=
  "ci/out/d972_b4_u_magnus4_a18_v1_producer.log";;
D972MAG4A18CheckerLogPath :=
  "ci/out/d972_b4_u_magnus4_a18_v1_checker.log";;
D972MAG4A18ProducerStatusPath :=
  "/tmp/d972_b4_u_magnus4_a18_v1_producer.status";;
D972MAG4A18CheckerStatusPath :=
  "/tmp/d972_b4_u_magnus4_a18_v1_checker.status";;

D972MAG4A18Selftest := 0;;
if IsBound(D972_B4_MAGNUS4_A18_SELFTEST) then
  D972MAG4A18Selftest := D972_B4_MAGNUS4_A18_SELFTEST;
fi;
if not IsInt(D972MAG4A18Selftest) or
   not D972MAG4A18Selftest in [0,1] then
  Error("Magnus4 A18 driver: SELFTEST must be integer 0 or 1");
fi;

D972MAG4A18ShellQuote := function(s)
  local c;
  if not IsString(s) then
    Error("Magnus4 A18 driver: shell path is not a string");
  fi;
  for c in ["'",CharInt(96),"$","\\","\n","\r",";","|","&",
            ">","<","(",")"] do
    if Position(s,c)<>fail then
      Error("Magnus4 A18 driver: unsafe shell path");
    fi;
  od;
  return Concatenation("'",s,"'");
end;;

D972MAG4A18RunAllow02 := function(label,command,status_path,log_path)
  local full,raw;
  full:=Concatenation(
    "rm -f ",D972MAG4A18ShellQuote(status_path),"; ",command,
    " > ",D972MAG4A18ShellQuote(log_path)," 2>&1; ",
    "rc=$?; printf '%s' \"$rc\" > ",
    D972MAG4A18ShellQuote(status_path));
  Exec(full);
  raw:=StringFile(status_path);
  if raw=fail or not raw in ["0","2"] then
    Error(Concatenation("Magnus4 A18 driver: ",label,
      " exit code is neither 0 nor 2"));
  fi;
  return Int(raw);
end;;

D972MAG4A18RunZero := function(label,command,status_path,log_path)
  local full,raw;
  full:=Concatenation(
    "rm -f ",D972MAG4A18ShellQuote(status_path),"; ",command,
    " > ",D972MAG4A18ShellQuote(log_path)," 2>&1; ",
    "rc=$?; printf '%s' \"$rc\" > ",
    D972MAG4A18ShellQuote(status_path));
  Exec(full);
  raw:=StringFile(status_path);
  if raw=fail or raw<>"0" then
    Error(Concatenation("Magnus4 A18 driver: ",label,
      " did not exit zero"));
  fi;
  return 0;
end;;

if D972MAG4A18Selftest=1 then
  if D972MAG4A18SourcePath<>
       "search/certs/d972_b4_p2_magnus_input_v2_20260816.json" or
     D972MAG4A18WordsPath<>
       "search/certs/d972_b4_word_key_artifact_v1_20260816.json" or
     D972MAG4A18ProducerPath<>
       "search/d972_b4_u_magnus4_a18_v1.py" or
     D972MAG4A18CheckerPath<>
       "search/check_d972_b4_u_magnus4_a18_v1.py" or
     D972MAG4A18ProducerReceiptPath<>
       "ci/out/d972_b4_u_magnus4_a18_v1.json" or
     D972MAG4A18CheckerReceiptPath<>
       "ci/out/d972_b4_u_magnus4_a18_v1_check.json" then
    Error("Magnus4 A18 driver: fixed path selftest drift");
  fi;
  if StringFile(D972MAG4A18ProducerPath)=fail or
     StringFile(D972MAG4A18CheckerPath)=fail then
    Error("Magnus4 A18 driver: Python lane file missing");
  fi;
  Print("D972_B4_U_MAGNUS4_A18_DRIVER_SELFTEST_FINAL_MARKER\n");
else
  if LoadPackage("json")<>true then
    Error("Magnus4 A18 driver: JSON package unavailable");
  fi;
  D972MAG4A18ProducerCommand:=Concatenation(
    "mkdir -p ",D972MAG4A18ShellQuote("ci/out")," && rm -f ",
    D972MAG4A18ShellQuote(D972MAG4A18ProducerReceiptPath)," && python3 -B ",
    D972MAG4A18ShellQuote(D972MAG4A18ProducerPath)," --source ",
    D972MAG4A18ShellQuote(D972MAG4A18SourcePath)," --word-artifact ",
    D972MAG4A18ShellQuote(D972MAG4A18WordsPath)," --output ",
    D972MAG4A18ShellQuote(D972MAG4A18ProducerReceiptPath));
  D972MAG4A18ProducerRc:=D972MAG4A18RunAllow02("producer",
    D972MAG4A18ProducerCommand,D972MAG4A18ProducerStatusPath,
    D972MAG4A18ProducerLogPath);;
  D972MAG4A18ProducerRaw:=StringFile(D972MAG4A18ProducerReceiptPath);;
  if D972MAG4A18ProducerRaw=fail then
    Error("Magnus4 A18 driver: producer receipt missing");
  fi;
  D972MAG4A18ProducerObj:=JsonStringToGap(D972MAG4A18ProducerRaw);;
  if not IsRecord(D972MAG4A18ProducerObj) or
     D972MAG4A18ProducerObj.schema<>"d972-b4-u-magnus4-a18/v1" or
     not D972MAG4A18ProducerObj.status in
       ["UNKNOWN_ALLPASS_MAGNUS4_A18",
        "B4_A_CANDIDATE_MAGNUS4_A18"] or
     D972MAG4A18ProducerObj.source_sha256<>
       "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9" or
     D972MAG4A18ProducerObj.word_artifact_sha256<>
       "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9" or
     D972MAG4A18ProducerObj.presentation_sha256<>
       "783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305" or
     D972MAG4A18ProducerObj.dtilde_sha256<>
       "32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef" or
     D972MAG4A18ProducerObj.raw_rs_sha256<>
       "db25c0268cdc774ef3205c9c1d1cf62cd013e6daaf73cf959e7972af5b3082bb" or
     D972MAG4A18ProducerObj.dtilde_rs_sha256<>
       "418e88934210e726de0e7e1f375bac2e6151f465be84f913884c58129217259c" or
     D972MAG4A18ProducerObj.presentation_relator_count<>158 or
     D972MAG4A18ProducerObj.a18_row_count<>140 or
     D972MAG4A18ProducerObj.norm_count<>972 or
     D972MAG4A18ProducerObj.rs_generator_count<>161 or
     D972MAG4A18ProducerObj.rs_relator_count<>5056 then
    Error("Magnus4 A18 driver: producer receipt gate failed");
  fi;
  Print("D972_B4_U_MAGNUS4_A18_PRODUCER_PASS rc=",D972MAG4A18ProducerRc,
    " status=",D972MAG4A18ProducerObj.status,"\n");

  D972MAG4A18CheckerCommand:=Concatenation(
    "rm -f ",D972MAG4A18ShellQuote(D972MAG4A18CheckerReceiptPath),
    " && python3 -B ",D972MAG4A18ShellQuote(D972MAG4A18CheckerPath),
    " --source ",D972MAG4A18ShellQuote(D972MAG4A18SourcePath),
    " --word-artifact ",D972MAG4A18ShellQuote(D972MAG4A18WordsPath),
    " --receipt ",D972MAG4A18ShellQuote(D972MAG4A18ProducerReceiptPath),
    " --output ",D972MAG4A18ShellQuote(D972MAG4A18CheckerReceiptPath));
  D972MAG4A18CheckerRc:=D972MAG4A18RunZero("independent checker",
    D972MAG4A18CheckerCommand,D972MAG4A18CheckerStatusPath,
    D972MAG4A18CheckerLogPath);;
  D972MAG4A18CheckerRaw:=StringFile(D972MAG4A18CheckerReceiptPath);;
  if D972MAG4A18CheckerRaw=fail then
    Error("Magnus4 A18 driver: checker receipt missing");
  fi;
  D972MAG4A18CheckerObj:=JsonStringToGap(D972MAG4A18CheckerRaw);;
  if not IsRecord(D972MAG4A18CheckerObj) or
     D972MAG4A18CheckerObj.schema<>
       "d972-b4-u-magnus4-a18-independent/v1" or
     D972MAG4A18CheckerObj.producer_status<>
       D972MAG4A18ProducerObj.status or
     not D972MAG4A18CheckerObj.status in
       ["UNKNOWN_ALLPASS_MAGNUS4_A18_CROSSCHECKED",
        "B4_A_CANDIDATE_MAGNUS4_A18_CROSSCHECKED"] or
     D972MAG4A18CheckerObj.rs_generator_count<>161 or
     D972MAG4A18CheckerObj.rs_relator_count<>5056 or
     D972MAG4A18CheckerObj.norm_count<>972 then
    Error("Magnus4 A18 driver: checker receipt gate failed");
  fi;
  Print("D972_B4_U_MAGNUS4_A18_CHECKER_PASS rc=",D972MAG4A18CheckerRc,
    " status=",D972MAG4A18CheckerObj.status,
    " producer_receipt_sha256=",HexSHA256(D972MAG4A18ProducerRaw),"\n");
  Print("D972_B4_U_MAGNUS4_A18_DRIVER_FINAL_MARKER status=",
    D972MAG4A18CheckerObj.status," producer_rc=",D972MAG4A18ProducerRc,
    " checker_rc=",D972MAG4A18CheckerRc,
    " producer=",D972MAG4A18ProducerReceiptPath,
    " checker=",D972MAG4A18CheckerReceiptPath,"\n");
fi;
