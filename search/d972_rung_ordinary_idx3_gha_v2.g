#############################################################################
## Ordinary idx-3 producer-v2 GHA launcher v2.
##
## This version authenticates frozen v1 and changes only its artifact-copy
## implementation: unformatted streams plus byte/string/SHA readback replace
## PrintTo(filename,long_string), which line-wrapped the one-line JSON.
#############################################################################

P159OOrdIdx3V2Base:=
  "search/d972_rung_ordinary_idx3_gha_v1.g";;
P159OOrdIdx3V2BaseBytes:=10789;;
P159OOrdIdx3V2BaseSha:=
  "8b78f5cef60b7f98671a7fa2bf5d2668d35d8d486187dc2494f712fa89d29a48";;
P159OOrdIdx3V2BaseManifest:=
  "search/certs/d972_rung_ordinary_idx3_gha_launcher_manifest_v1_20260824.json";;
P159OOrdIdx3V2BaseManifestBytes:=14235;;
P159OOrdIdx3V2BaseManifestSha:=
  "d26c123891be46bf3624cbd945db3ec51138620905c94663fc73e5e3ef440f52";;
P159OOrdIdx3V2Effective:=
  "ci/out/d972_rung_ordinary_idx3_gha_effective_v2.g";;
P159OOrdIdx3V2ModeTokenPath:=
  "search/certs/d972_rung_mode_freeze_ordinary_idx3_v1_20260824.json";;
P159OOrdIdx3V2ModeTokenBytes:=2531;;
P159OOrdIdx3V2ModeTokenSha:=
  "9102917bc105ba6dc586d4ba6b43ce9703d1d1d7a47d795860239f970b5c0672";;

P159OOrdIdx3V2OldCopy:=Concatenation(
  "PrintTo(P159OOrdIdx3V1ReceiptCopy,P159OOrdIdx3V1Receipt);\n",
  "PrintTo(P159OOrdIdx3V1ManifestCopy,P159OOrdIdx3V1ExecutionManifest);\n",
  "if StringFile(P159OOrdIdx3V1ReceiptCopy)=fail or\n",
  "   HexSHA256(StringFile(P159OOrdIdx3V1ReceiptCopy))<>\n",
  "     HexSHA256(P159OOrdIdx3V1Receipt) or\n",
  "   StringFile(P159OOrdIdx3V1ManifestCopy)=fail or\n",
  "   HexSHA256(StringFile(P159OOrdIdx3V1ManifestCopy))<>\n",
  "     HexSHA256(P159OOrdIdx3V1ExecutionManifest) then\n",
  "  Error(\"PENT159O_ORDINARY_IDX3_GHA_V1: artifact copy mismatch\");\n",
  "fi;");;
P159OOrdIdx3V2NewCopy:=Concatenation(
  "P159OOrdIdx3V2CopyExact:=function(path,raw,label)\n",
  "  local stream,readback,expectedSha,actualSha;\n",
  "  expectedSha:=HexSHA256(raw);\n",
  "  stream:=OutputTextFile(path,false);\n",
  "  if stream=fail then\n",
  "    Error(\"PENT159O_ORDINARY_IDX3_GHA_V2: artifact copy open failed label=\",label,\" path=\",path);\n",
  "  fi;\n",
  "  SetPrintFormattingStatus(stream,false);\n",
  "  PrintTo(stream,raw);\n",
  "  CloseStream(stream);\n",
  "  readback:=StringFile(path);\n",
  "  if readback=fail then\n",
  "    Error(\"PENT159O_ORDINARY_IDX3_GHA_V2: artifact copy readback absent label=\",label,\" path=\",path);\n",
  "  fi;\n",
  "  actualSha:=HexSHA256(readback);\n",
  "  if Length(readback)<>Length(raw) or readback<>raw or actualSha<>expectedSha then\n",
  "    Error(\"PENT159O_ORDINARY_IDX3_GHA_V2: artifact copy mismatch label=\",label,\n",
  "      \" path=\",path,\" expected_bytes=\",Length(raw),\" actual_bytes=\",Length(readback),\n",
  "      \" expected_sha256=\",expectedSha,\" actual_sha256=\",actualSha);\n",
  "  fi;\n",
  "  Print(\"PENT159O_ORDINARY_IDX3_GHA_V2_ARTIFACT_COPY_PASS label=\",label,\n",
  "    \" path=\",path,\" bytes=\",Length(readback),\" sha256=\",actualSha,\"\\n\");\n",
  "  return true;\n",
  "end;\n",
  "if Length(P159OOrdIdx3V1Receipt)<>62680 or\n",
  "   HexSHA256(P159OOrdIdx3V1Receipt)<>\"48512270d265753944ff9b86d19fa5e84095ffffd8ae78beba969088c31053e9\" then\n",
  "  Error(\"PENT159O_ORDINARY_IDX3_GHA_V2: deterministic source receipt drift\");\n",
  "fi;\n",
  "if Length(P159OOrdIdx3V1ExecutionManifest)<>1702 or\n",
  "   HexSHA256(P159OOrdIdx3V1ExecutionManifest)<>\"950f91d3e22f26970f31161503843b15e9543c0fd16371933e3543dd11ee0dab\" then\n",
  "  Error(\"PENT159O_ORDINARY_IDX3_GHA_V2: deterministic source execution-manifest drift\");\n",
  "fi;\n",
  "Print(\"PENT159O_ORDINARY_IDX3_GHA_V2_SOURCE_OUTPUT_PINS_PASS receipt=62680/48512270d265753944ff9b86d19fa5e84095ffffd8ae78beba969088c31053e9 manifest=1702/950f91d3e22f26970f31161503843b15e9543c0fd16371933e3543dd11ee0dab\\n\");\n",
  "P159OOrdIdx3V2CopyExact(P159OOrdIdx3V1ReceiptCopy,\n",
  "  P159OOrdIdx3V1Receipt,\"receipt\");\n",
  "P159OOrdIdx3V2CopyExact(P159OOrdIdx3V1ManifestCopy,\n",
  "  P159OOrdIdx3V1ExecutionManifest,\"execution_manifest\");");;
P159OOrdIdx3V2OldFinal:=Concatenation(
  "Print(\"PENT159O_ORDINARY_IDX3_GHA_V1_FINAL PRODUCER_V2_CANDIDATE_CHECKER_REQUIRED__RUNG_NAME_UNSET\\n\");\n",
  "QUIT_GAP(0);");;
P159OOrdIdx3V2NewFinal:=Concatenation(
  "Print(\"PENT159O_ORDINARY_IDX3_GHA_V1_FINAL PRODUCER_V2_CANDIDATE_CHECKER_REQUIRED__RUNG_NAME_UNSET\\n\");\n",
  "Print(\"PENT159O_ORDINARY_IDX3_GHA_V2_FINAL PRODUCER_V2_CANDIDATE_CHECKER_REQUIRED__RUNG_NAME_UNSET copy_exact=true\\n\");\n",
  "QUIT_GAP(0);");;

P159OOrdIdx3V2RequireSha:=function(path,expectedBytes,expectedSha)
  local raw,actual;
  raw:=StringFile(path);;
  if raw=fail then
    Error("PENT159O_ORDINARY_IDX3_GHA_V2: missing immutable input ",path);
  fi;
  actual:=HexSHA256(raw);;
  if Length(raw)<>expectedBytes or actual<>expectedSha then
    Error("PENT159O_ORDINARY_IDX3_GHA_V2: immutable input pin mismatch ",path,
      " expected_bytes=",expectedBytes," actual_bytes=",Length(raw),
      " expected_sha256=",expectedSha," actual_sha256=",actual);
  fi;
  Print("PENT159O_ORDINARY_IDX3_GHA_V2_PIN_PASS path=",path,
    " bytes=",Length(raw)," sha256=",actual,"\n");
  return raw;
end;;

P159OOrdIdx3V2Count:=function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("PENT159O_ORDINARY_IDX3_GHA_V2: occurrence input drift");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

P159OOrdIdx3V2WriteExact:=function(path,raw,expectedBytes,expectedSha)
  local stream,readback,actual;
  if StringFile(path)<>fail then
    Error("PENT159O_ORDINARY_IDX3_GHA_V2: pre-existing effective launcher ",path);
  fi;
  stream:=OutputTextFile(path,false);;
  if stream=fail then
    Error("PENT159O_ORDINARY_IDX3_GHA_V2: cannot open effective launcher ",path);
  fi;
  SetPrintFormattingStatus(stream,false);;
  PrintTo(stream,raw);;
  CloseStream(stream);
  readback:=StringFile(path);;
  if readback=fail or readback<>raw then
    Error("PENT159O_ORDINARY_IDX3_GHA_V2: effective launcher readback drift");
  fi;
  actual:=HexSHA256(readback);;
  if Length(readback)<>expectedBytes or actual<>expectedSha then
    Error("PENT159O_ORDINARY_IDX3_GHA_V2: effective launcher generated-pin drift",
      " expected_bytes=",expectedBytes," actual_bytes=",Length(readback),
      " expected_sha256=",expectedSha," actual_sha256=",actual);
  fi;
  Print("PENT159O_ORDINARY_IDX3_GHA_V2_EFFECTIVE_PIN path=",path,
    " bytes=",Length(readback)," sha256=",actual,"\n");
end;;

Print("PENT159O_ORDINARY_IDX3_GHA_V2_START repair=artifact_copy_only failed_run=32681824334 outcome_not_consumed=true\n");
if not IsBound(D972_ORDINARY_IDX3_MODE_TOKEN_SHA256) or
   not IsString(D972_ORDINARY_IDX3_MODE_TOKEN_SHA256) or
   Length(D972_ORDINARY_IDX3_MODE_TOKEN_SHA256)<>64 or
   D972_ORDINARY_IDX3_MODE_TOKEN_SHA256<>P159OOrdIdx3V2ModeTokenSha or
   not ForAll(D972_ORDINARY_IDX3_MODE_TOKEN_SHA256,
     c->c in "0123456789abcdef") then
  Error("PENT159O_ORDINARY_IDX3_GHA_V2: MODE_TOKEN_REQUIRED valid parent SHA-256 preamble absent");
fi;
P159OOrdIdx3V2ModeToken:=StringFile(P159OOrdIdx3V2ModeTokenPath);;
if P159OOrdIdx3V2ModeToken=fail or
   Length(P159OOrdIdx3V2ModeToken)<>P159OOrdIdx3V2ModeTokenBytes or
   HexSHA256(P159OOrdIdx3V2ModeToken)<>D972_ORDINARY_IDX3_MODE_TOKEN_SHA256 then
  Error("PENT159O_ORDINARY_IDX3_GHA_V2: parent mode-token pin mismatch");
fi;
Print("PENT159O_ORDINARY_IDX3_GHA_V2_MODE_TOKEN_PIN_PASS path=",
  P159OOrdIdx3V2ModeTokenPath," bytes=",Length(P159OOrdIdx3V2ModeToken),
  " sha256=",HexSHA256(P159OOrdIdx3V2ModeToken),"\n");

P159OOrdIdx3V2Raw:=P159OOrdIdx3V2RequireSha(
  P159OOrdIdx3V2Base,P159OOrdIdx3V2BaseBytes,P159OOrdIdx3V2BaseSha);;
P159OOrdIdx3V2BaseManifestRaw:=P159OOrdIdx3V2RequireSha(
  P159OOrdIdx3V2BaseManifest,P159OOrdIdx3V2BaseManifestBytes,
  P159OOrdIdx3V2BaseManifestSha);;
if PositionSublist(P159OOrdIdx3V2BaseManifestRaw,
     "PENT159O_ORDINARY_IDX3_GHA_LAUNCHER_MANIFEST_V1_FROZEN__MODE_TOKEN_REQUIRED__NOT_RUN")=fail then
  Error("PENT159O_ORDINARY_IDX3_GHA_V2: frozen v1 launcher manifest semantic drift");
fi;
if P159OOrdIdx3V2Count(P159OOrdIdx3V2Raw,P159OOrdIdx3V2OldCopy)<>1 or
   P159OOrdIdx3V2Count(P159OOrdIdx3V2Raw,P159OOrdIdx3V2NewCopy)<>0 or
   P159OOrdIdx3V2Count(P159OOrdIdx3V2Raw,P159OOrdIdx3V2OldFinal)<>1 then
  Error("PENT159O_ORDINARY_IDX3_GHA_V2: frozen v1 patch cardinality drift");
fi;
P159OOrdIdx3V2Patched:=ReplacedString(
  P159OOrdIdx3V2Raw,P159OOrdIdx3V2OldCopy,P159OOrdIdx3V2NewCopy);;
P159OOrdIdx3V2Patched:=ReplacedString(
  P159OOrdIdx3V2Patched,P159OOrdIdx3V2OldFinal,P159OOrdIdx3V2NewFinal);;
if P159OOrdIdx3V2Count(P159OOrdIdx3V2Patched,P159OOrdIdx3V2OldCopy)<>0 or
   P159OOrdIdx3V2Count(P159OOrdIdx3V2Patched,P159OOrdIdx3V2NewCopy)<>1 or
   P159OOrdIdx3V2Count(P159OOrdIdx3V2Patched,P159OOrdIdx3V2OldFinal)<>0 or
   P159OOrdIdx3V2Count(P159OOrdIdx3V2Patched,P159OOrdIdx3V2NewFinal)<>1 then
  Error("PENT159O_ORDINARY_IDX3_GHA_V2: effective v2 patch drift");
fi;

Exec("mkdir -p 'ci/out'");;
P159OOrdIdx3V2WriteExact(P159OOrdIdx3V2Effective,P159OOrdIdx3V2Patched,
  12393,"6c5ccc976a6f789d5e8ccbd471d4205289030cf46d637009222151d48837ec31");;
Print("PENT159O_ORDINARY_IDX3_GHA_V2_PATCH_PASS copy_gate_only=true producer_prereg_token_outputs_unchanged=true dependencies_delegated_to_authenticated_v1=true\n");
Read(P159OOrdIdx3V2Effective);;
