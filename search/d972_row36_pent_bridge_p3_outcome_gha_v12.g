#############################################################################
## P3 fixed-row36 v12 launcher-only marker-contract repair.
##
## The frozen v11 outcome launcher reconstructed the exact v8 preregistration
## but expected two wrapper-only v8 log markers which the frozen Python entry
## does not emit.  This wrapper authenticates v11, changes only those two
## required log-token literals to the exact v1 markers actually emitted, and
## then delegates every mathematical and outcome gate to the patched copy.
#############################################################################

P159OR36P3V12V11Driver:=
  "search/d972_row36_pent_bridge_p3_outcome_gha_v11.g";;
P159OR36P3V12V11DriverBytes:=14846;;
P159OR36P3V12V11DriverSha:=
  "03709a4dcb6e7c39765307c000a9fe62382615c25b3001d1d12465836f711139";;
P159OR36P3V12V11Manifest:=
  "search/certs/d972_row36_pent_bridge_p3_outcome_execution_manifest_v11_20260824.json";;
P159OR36P3V12V11ManifestBytes:=10604;;
P159OR36P3V12V11ManifestSha:=
  "7970c4c84ec7ef27b253934980f3b3388730ad47319d09e5c13f2ab13877d253";;
P159OR36P3V12Effective:=
  "ci/out/d972_row36_pent_bridge_p3_outcome_effective_v12.g";;

P159OR36P3V12OldWritten:=
  "PENT159O_ROW36_P3_V8_PREREG_WRITTEN";;
P159OR36P3V12NewWritten:=
  "PENT159O_ROW36_P3_V1_PREREG_WRITTEN";;
P159OR36P3V12OldFinal:=
  "PENT159O_ROW36_P3_V8_FINAL OUTCOME_FREE_PREREGISTRATION_FROZEN__PREDICATE_EXECUTION_NOT_RUN";;
P159OR36P3V12NewFinal:=
  "PENT159O_ROW36_P3_V1_PREPARE_PASS";;

P159OR36P3V12RequireSha:=function(path,expectedBytes,expectedSha)
  local raw,actual;
  raw:=StringFile(path);;
  if raw=fail then
    Error("PENT159O_ROW36_P3_V12: missing immutable input ",path);
  fi;
  actual:=HexSHA256(raw);;
  if Length(raw)<>expectedBytes or actual<>expectedSha then
    Error("PENT159O_ROW36_P3_V12: immutable input pin mismatch ",path,
      " expected_bytes=",expectedBytes," actual_bytes=",Length(raw),
      " expected_sha256=",expectedSha," actual_sha256=",actual);
  fi;
  Print("PENT159O_ROW36_P3_V12_PIN_PASS path=",path,
    " bytes=",Length(raw)," sha256=",actual,"\n");
  return raw;
end;;

P159OR36P3V12Count:=function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("PENT159O_ROW36_P3_V12: occurrence-count input drift");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

P159OR36P3V12WriteExact:=function(path,raw,expectedBytes,expectedSha)
  local stream,readback,actual;
  if StringFile(path)<>fail then
    Error("PENT159O_ROW36_P3_V12: pre-existing versioned effective driver ",path);
  fi;
  stream:=OutputTextFile(path,false);;
  if stream=fail then
    Error("PENT159O_ROW36_P3_V12: cannot open effective driver ",path);
  fi;
  SetPrintFormattingStatus(stream,false);;
  PrintTo(stream,raw);;
  CloseStream(stream);
  readback:=StringFile(path);;
  if readback=fail or readback<>raw then
    Error("PENT159O_ROW36_P3_V12: effective driver readback drift");
  fi;
  actual:=HexSHA256(readback);;
  if Length(readback)<>expectedBytes or actual<>expectedSha then
    Error("PENT159O_ROW36_P3_V12: effective driver generated-pin drift",
      " expected_bytes=",expectedBytes," actual_bytes=",Length(readback),
      " expected_sha256=",expectedSha," actual_sha256=",actual);
  fi;
  Print("PENT159O_ROW36_P3_V12_EFFECTIVE_DRIVER_PIN path=",path,
    " bytes=",Length(readback)," sha256=",actual,"\n");
end;;

Print("PENT159O_ROW36_P3_V12_START launcher_only=true failed_run=32671573263 outcome_started=false\n");
P159OR36P3V12Raw:=P159OR36P3V12RequireSha(
  P159OR36P3V12V11Driver,P159OR36P3V12V11DriverBytes,
  P159OR36P3V12V11DriverSha);;
P159OR36P3V12ManifestRaw:=P159OR36P3V12RequireSha(
  P159OR36P3V12V11Manifest,P159OR36P3V12V11ManifestBytes,
  P159OR36P3V12V11ManifestSha);;
if PositionSublist(P159OR36P3V12ManifestRaw,
     "PENT159O_ROW36_P3_OUTCOME_EXECUTION_MANIFEST_V11_FROZEN")=fail or
   PositionSublist(P159OR36P3V12ManifestRaw,
     "DISPATCH_READY_NOT_RUN")=fail then
  Error("PENT159O_ROW36_P3_V12: frozen v11 manifest semantic pin drift");
fi;

if P159OR36P3V12Count(P159OR36P3V12Raw,P159OR36P3V12OldWritten)<>1 or
   P159OR36P3V12Count(P159OR36P3V12Raw,P159OR36P3V12OldFinal)<>1 or
   P159OR36P3V12Count(P159OR36P3V12Raw,P159OR36P3V12NewWritten)<>1 or
   P159OR36P3V12Count(P159OR36P3V12Raw,P159OR36P3V12NewFinal)<>1 then
  Error("PENT159O_ROW36_P3_V12: frozen marker substitution cardinality drift");
fi;
P159OR36P3V12Patched:=ReplacedString(
  P159OR36P3V12Raw,P159OR36P3V12OldWritten,P159OR36P3V12NewWritten);;
P159OR36P3V12Patched:=ReplacedString(
  P159OR36P3V12Patched,P159OR36P3V12OldFinal,P159OR36P3V12NewFinal);;
if P159OR36P3V12Count(P159OR36P3V12Patched,P159OR36P3V12OldWritten)<>0 or
   P159OR36P3V12Count(P159OR36P3V12Patched,P159OR36P3V12OldFinal)<>0 or
   P159OR36P3V12Count(P159OR36P3V12Patched,P159OR36P3V12NewWritten)<>2 or
   P159OR36P3V12Count(P159OR36P3V12Patched,P159OR36P3V12NewFinal)<>2 then
  Error("PENT159O_ROW36_P3_V12: effective marker substitution cardinality drift");
fi;

Exec("mkdir -p 'ci/out'");;
P159OR36P3V12WriteExact(P159OR36P3V12Effective,P159OR36P3V12Patched,
  14788,
  "cb841608a845e3a35cbc17cdd97cb9cda8f3f7b5b2e90ecbe15b657024c049f3");;
Print("PENT159O_ROW36_P3_V12_MARKER_REPAIR_PASS replacements=2 exact_v1_prepare_contract=true prereg_byte_sha_gate_preserved=true\n");
Print("PENT159O_ROW36_P3_V12_DELEGATE_START frozen_outcome_launcher=v11\n");
Read(P159OR36P3V12Effective);;
