#############################################################################
## P3 fixed-row36 v13 warning-only outcome launcher.
##
## This wrapper authenticates frozen v11/v12, routes the v11 worker reference
## to the versioned v13 warning repair, adds the frozen v12 receipt aggregate
## digest as a fail-closed semantic gate, and otherwise delegates unchanged.
#############################################################################

P159OR36P3V13V11Driver:=
  "search/d972_row36_pent_bridge_p3_outcome_gha_v11.g";;
P159OR36P3V13V11DriverBytes:=14846;;
P159OR36P3V13V11DriverSha:=
  "03709a4dcb6e7c39765307c000a9fe62382615c25b3001d1d12465836f711139";;
P159OR36P3V13V12Launcher:=
  "search/d972_row36_pent_bridge_p3_outcome_gha_v12.g";;
P159OR36P3V13V12LauncherBytes:=5590;;
P159OR36P3V13V12LauncherSha:=
  "d42b704180d4726aef5fc2d677b226576c361dd1aeef2db8d0effabd2da8d326";;
P159OR36P3V13V12Manifest:=
  "search/certs/d972_row36_pent_bridge_p3_outcome_execution_manifest_v12_20260824.json";;
P159OR36P3V13V12ManifestBytes:=7347;;
P159OR36P3V13V12ManifestSha:=
  "a029d00ca86d7626afbe7e04195e6d4e3a07f2673250bdf73f1dd69bfc5cbc8e";;
P159OR36P3V13Worker:=
  "search/d972_row36_pent_bridge_p3_q4_outcome_worker_v13.g";;
P159OR36P3V13WorkerBytes:=4836;;
P159OR36P3V13WorkerSha:=
  "628ce68fecb6c7d08d4706a6482c9d8db0c2cc44bb1415e23a6f21ce5fb48d33";;
P159OR36P3V13DerivedDriver:=
  "ci/out/d972_row36_pent_bridge_p3_outcome_driver_worker_v13.g";;
P159OR36P3V13DerivedLauncher:=
  "ci/out/d972_row36_pent_bridge_p3_outcome_launcher_effective_v13.g";;

P159OR36P3V13OldWorkerPath:=
  "search/d972_row36_pent_bridge_p3_q4_outcome_worker_v11.g";;
P159OR36P3V13OldWorkerBytes:="3258958";;
P159OR36P3V13OldWorkerSha:=
  "3838da922ddd7117e2d134a5c773a6ed606b2e656f8ce6c70ee82e6f7b9e691c";;
P159OR36P3V13ReceiptTerminal:=
  "   \"\\\"terminal_token\\\":\\\"PENT159O_ROW36_P3_PRODUCER_V11_CANDIDATE__CHECKER_REQUIRED\\\"\"]);";;
P159OR36P3V13ReceiptAggregate:=Concatenation(
  "   \"\\\"aggregate_sha256\\\":\\\"8e9f3242463e83de53f65e636faec236abcd5431011a08f8969e0d3b095522b9\\\"\",\n",
  P159OR36P3V13ReceiptTerminal);;
P159OR36P3V13OldDriverPath:=
  "search/d972_row36_pent_bridge_p3_outcome_gha_v11.g";;
P159OR36P3V13OldDriverBytes:="14846";;
P159OR36P3V13OldDriverSha:=
  "03709a4dcb6e7c39765307c000a9fe62382615c25b3001d1d12465836f711139";;
P159OR36P3V13OldEffectiveBytes:="14788";;
P159OR36P3V13OldEffectiveSha:=
  "cb841608a845e3a35cbc17cdd97cb9cda8f3f7b5b2e90ecbe15b657024c049f3";;

P159OR36P3V13RequireSha:=function(path,expectedBytes,expectedSha)
  local raw,actual;
  raw:=StringFile(path);;
  if raw=fail then
    Error("PENT159O_ROW36_P3_V13: missing immutable input ",path);
  fi;
  actual:=HexSHA256(raw);;
  if Length(raw)<>expectedBytes or actual<>expectedSha then
    Error("PENT159O_ROW36_P3_V13: immutable pin mismatch ",path,
      " expected_bytes=",expectedBytes," actual_bytes=",Length(raw),
      " expected_sha256=",expectedSha," actual_sha256=",actual);
  fi;
  Print("PENT159O_ROW36_P3_V13_PIN_PASS path=",path,
    " bytes=",Length(raw)," sha256=",actual,"\n");
  return raw;
end;;

P159OR36P3V13Count:=function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("PENT159O_ROW36_P3_V13: occurrence input drift");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

P159OR36P3V13WriteExact:=function(path,raw,expectedBytes,expectedSha)
  local stream,readback,actual;
  if StringFile(path)<>fail then
    Error("PENT159O_ROW36_P3_V13: pre-existing generated launcher ",path);
  fi;
  stream:=OutputTextFile(path,false);;
  if stream=fail then
    Error("PENT159O_ROW36_P3_V13: cannot open generated launcher ",path);
  fi;
  SetPrintFormattingStatus(stream,false);;
  PrintTo(stream,raw);;
  CloseStream(stream);
  readback:=StringFile(path);;
  if readback=fail or readback<>raw then
    Error("PENT159O_ROW36_P3_V13: generated launcher readback drift");
  fi;
  actual:=HexSHA256(readback);;
  if Length(readback)<>expectedBytes or actual<>expectedSha then
    Error("PENT159O_ROW36_P3_V13: generated launcher pin drift ",path,
      " expected_bytes=",expectedBytes," actual_bytes=",Length(readback),
      " expected_sha256=",expectedSha," actual_sha256=",actual);
  fi;
  Print("PENT159O_ROW36_P3_V13_GENERATED_PIN path=",path,
    " bytes=",Length(readback)," sha256=",actual,"\n");
end;;

Print("PENT159O_ROW36_P3_V13_START warning_only=true failed_warning_run=32672099635 math_change=false universe_change=false\n");
P159OR36P3V13Raw11:=P159OR36P3V13RequireSha(
  P159OR36P3V13V11Driver,P159OR36P3V13V11DriverBytes,
  P159OR36P3V13V11DriverSha);;
P159OR36P3V13Raw12:=P159OR36P3V13RequireSha(
  P159OR36P3V13V12Launcher,P159OR36P3V13V12LauncherBytes,
  P159OR36P3V13V12LauncherSha);;
P159OR36P3V13Manifest12:=P159OR36P3V13RequireSha(
  P159OR36P3V13V12Manifest,P159OR36P3V13V12ManifestBytes,
  P159OR36P3V13V12ManifestSha);;
P159OR36P3V13RequireSha(P159OR36P3V13Worker,
  P159OR36P3V13WorkerBytes,P159OR36P3V13WorkerSha);;
if PositionSublist(P159OR36P3V13Manifest12,
     "PENT159O_ROW36_P3_OUTCOME_EXECUTION_MANIFEST_V12_FROZEN")=fail then
  Error("PENT159O_ROW36_P3_V13: v12 execution manifest semantic drift");
fi;

if P159OR36P3V13Count(P159OR36P3V13Raw11,
     P159OR36P3V13OldWorkerPath)<>2 or
   P159OR36P3V13Count(P159OR36P3V13Raw11,
     P159OR36P3V13OldWorkerBytes)<>1 or
   P159OR36P3V13Count(P159OR36P3V13Raw11,
     P159OR36P3V13OldWorkerSha)<>1 or
   P159OR36P3V13Count(P159OR36P3V13Raw11,
     P159OR36P3V13ReceiptTerminal)<>1 or
   P159OR36P3V13Count(P159OR36P3V13Raw11,
     "8e9f3242463e83de53f65e636faec236abcd5431011a08f8969e0d3b095522b9")<>0 then
  Error("PENT159O_ROW36_P3_V13: v11 repair cardinality drift");
fi;
P159OR36P3V13Driver:=ReplacedString(P159OR36P3V13Raw11,
  P159OR36P3V13OldWorkerPath,P159OR36P3V13Worker);;
P159OR36P3V13Driver:=ReplacedString(P159OR36P3V13Driver,
  P159OR36P3V13OldWorkerBytes,String(P159OR36P3V13WorkerBytes));;
P159OR36P3V13Driver:=ReplacedString(P159OR36P3V13Driver,
  P159OR36P3V13OldWorkerSha,P159OR36P3V13WorkerSha);;
P159OR36P3V13Driver:=ReplacedString(P159OR36P3V13Driver,
  P159OR36P3V13ReceiptTerminal,P159OR36P3V13ReceiptAggregate);;
if P159OR36P3V13Count(P159OR36P3V13Driver,P159OR36P3V13OldWorkerPath)<>0 or
   P159OR36P3V13Count(P159OR36P3V13Driver,P159OR36P3V13Worker)<>2 or
   P159OR36P3V13Count(P159OR36P3V13Driver,P159OR36P3V13WorkerSha)<>1 or
   P159OR36P3V13Count(P159OR36P3V13Driver,
     "8e9f3242463e83de53f65e636faec236abcd5431011a08f8969e0d3b095522b9")<>1 then
  Error("PENT159O_ROW36_P3_V13: derived v11 driver drift");
fi;

Exec("mkdir -p 'ci/out'");;
P159OR36P3V13WriteExact(P159OR36P3V13DerivedDriver,P159OR36P3V13Driver,
  14939,"df5f385cccde2cb4393de1d215dbc6572768171f4c1f789b633227bc9bf01bf1");;

if P159OR36P3V13Count(P159OR36P3V13Raw12,
     P159OR36P3V13OldDriverPath)<>1 or
   P159OR36P3V13Count(P159OR36P3V13Raw12,
     P159OR36P3V13OldDriverBytes)<>1 or
   P159OR36P3V13Count(P159OR36P3V13Raw12,
     P159OR36P3V13OldDriverSha)<>1 or
   P159OR36P3V13Count(P159OR36P3V13Raw12,
     P159OR36P3V13OldEffectiveBytes)<>1 or
   P159OR36P3V13Count(P159OR36P3V13Raw12,
     P159OR36P3V13OldEffectiveSha)<>1 then
  Error("PENT159O_ROW36_P3_V13: v12 delegation cardinality drift");
fi;
P159OR36P3V13Launcher:=ReplacedString(P159OR36P3V13Raw12,
  P159OR36P3V13OldDriverPath,P159OR36P3V13DerivedDriver);;
P159OR36P3V13Launcher:=ReplacedString(P159OR36P3V13Launcher,
  P159OR36P3V13OldDriverBytes,"14939");;
P159OR36P3V13Launcher:=ReplacedString(P159OR36P3V13Launcher,
  P159OR36P3V13OldDriverSha,
  "df5f385cccde2cb4393de1d215dbc6572768171f4c1f789b633227bc9bf01bf1");;
P159OR36P3V13Launcher:=ReplacedString(P159OR36P3V13Launcher,
  P159OR36P3V13OldEffectiveBytes,"14881");;
P159OR36P3V13Launcher:=ReplacedString(P159OR36P3V13Launcher,
  P159OR36P3V13OldEffectiveSha,
  "48c0d021556f2245790835b01f727b34f48d12be8650bfaf900992771a07c3b8");;
if P159OR36P3V13Count(P159OR36P3V13Launcher,
     P159OR36P3V13OldDriverPath)<>0 or
   P159OR36P3V13Count(P159OR36P3V13Launcher,
     P159OR36P3V13DerivedDriver)<>1 or
   P159OR36P3V13Count(P159OR36P3V13Launcher,
     "df5f385cccde2cb4393de1d215dbc6572768171f4c1f789b633227bc9bf01bf1")<>1 or
   P159OR36P3V13Count(P159OR36P3V13Launcher,
     "48c0d021556f2245790835b01f727b34f48d12be8650bfaf900992771a07c3b8")<>1 then
  Error("PENT159O_ROW36_P3_V13: derived v12 launcher drift");
fi;
P159OR36P3V13WriteExact(P159OR36P3V13DerivedLauncher,P159OR36P3V13Launcher,
  5600,"0e0f4e27dcf068027eabf2fbd081298138b66a847258cc0a76e855ca04d4536d");;
Print("PENT159O_ROW36_P3_V13_REPAIR_PASS warning_only=true Q4_expected_sha256=ce7951c374c1dad4fe36e240dd6289e1e5f410c3111ceb892891b1521eac1480 receipt_aggregate_expected=8e9f3242463e83de53f65e636faec236abcd5431011a08f8969e0d3b095522b9\n");
Print("PENT159O_ROW36_P3_V13_DELEGATE_START frozen_marker_repair=v12 frozen_outcome=v11 worker_repair=v13\n");
Read(P159OR36P3V13DerivedLauncher);;
