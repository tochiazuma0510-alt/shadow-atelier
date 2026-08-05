## HS lane certificate JSON writer.
## This file deliberately implements only the small JSON fragment needed by
## the lane wrappers.  All string-valued provenance bindings are restricted
## to a conservative ASCII alphabet before they reach JsonQuote, so an
## unescaped quote/backslash can never turn a certificate into ambiguous JSON.

HSJsonSafeString := function(s)
  local ch;
  if not IsString(s) then
    Error("CERT_IO_STOP: expected a string, got ", s);
  fi;
  for ch in s do
    if not (ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._/:+-") then
      Error("CERT_IO_STOP: unsafe JSON string character in provenance value: ", ch);
    fi;
  od;
  return s;
end;;

HSJsonQuote := function(s)
  return Concatenation("\"", HSJsonSafeString(s), "\"");
end;;

HSJsonBool := function(b)
  if b then return "true"; else return "false"; fi;
end;;

HSJsonIntList := function(xs)
  local out, i;
  out := "[";
  for i in [1..Length(xs)] do
    if i > 1 then Append(out, ","); fi;
    Append(out, String(xs[i]));
  od;
  Append(out, "]");
  return out;
end;;

HSRequireBinding := function(name, value)
  if not IsString(value) or value = "" or value = "UNSET" then
    Error("CERT_BINDING_STOP: required binding ", name, " is absent/UNSET");
  fi;
  HSJsonSafeString(value);
end;;

HSOpenCert := function(path, lane, axis, universeTotal, evaluatedLo,
                       evaluatedHi, classId, runId, runAttempt, commitSha,
                       sourceBundleSha, wrapperSha, predicateSha, auxSha,
                       schemaSha, basisMaterialJson, basisFingerprint)
  local out;
  HSRequireBinding("CLASS_ID", classId);
  HSRequireBinding("RUN_ID", runId);
  HSRequireBinding("RUN_ATTEMPT", runAttempt);
  HSRequireBinding("COMMIT_SHA", commitSha);
  HSRequireBinding("SOURCE_BUNDLE_SHA256", sourceBundleSha);
  HSRequireBinding("WRAPPER_SHA256", wrapperSha);
  HSRequireBinding("PREDICATE_SHA256", predicateSha);
  HSRequireBinding("AUX_SHA256", auxSha);
  HSRequireBinding("SCHEMA_SHA256", schemaSha);
  HSRequireBinding("PCGS_BASIS_FINGERPRINT", basisFingerprint);
  if not IsString(basisMaterialJson) or basisMaterialJson = "" then
    Error("CERT_BINDING_STOP: pcgs_basis_material JSON is absent");
  fi;
  out := OutputTextFile(path, false);
  if out = fail then Error("CERT_IO_STOP: cannot open output path ", path); fi;
  SetPrintFormattingStatus(out, false);
  PrintTo(out,
    "{\n",
    "  \"schema\": \"hsp7-lane-cert/v3\",\n",
    "  \"lane\": ", HSJsonQuote(lane), ",\n",
    "  \"axis\": ", HSJsonQuote(axis), ",\n",
    "  \"class_id\": ", HSJsonQuote(classId), ",\n",
    "  \"run\": {\"run_id\":", HSJsonQuote(runId),
      ",\"run_attempt\":", HSJsonQuote(runAttempt),
      ",\"commit_sha\":", HSJsonQuote(commitSha), "},\n",
    "  \"source_bindings\": {\"source_bundle_sha256\":", HSJsonQuote(sourceBundleSha),
      ",\"wrapper_sha256\":", HSJsonQuote(wrapperSha),
      ",\"predicate_sha256\":", HSJsonQuote(predicateSha),
      ",\"aux_sha256\":", HSJsonQuote(auxSha),
      ",\"schema_sha256\":", HSJsonQuote(schemaSha), "},\n",
    "  \"pcgs_basis_material\": ", basisMaterialJson, ",\n",
    "  \"pcgs_basis_fingerprint\": ", HSJsonQuote(basisFingerprint), ",\n",
    "  \"universe_total\": ", String(universeTotal), ",\n",
    "  \"evaluated_range\": [", String(evaluatedLo), ",", String(evaluatedHi), "],\n",
    "  \"records\": [\n");
  return out;
end;;

HSCertWriteRecord := function(out, first, recordJson)
  if not first then PrintTo(out, ",\n"); fi;
  PrintTo(out, "    ", recordJson);
end;;

HSCloseCert := function(out, evaluatedCount, unknownCount, integrityOk,
                        driverDone)
  PrintTo(out,
    "\n  ],\n",
    "  \"summary\": {\"evaluated_count\":", String(evaluatedCount),
      ",\"unknown_count\":", String(unknownCount),
      ",\"integrity_ok\":", HSJsonBool(integrityOk), "},\n",
    "  \"driver_done\": ", HSJsonBool(driverDone), "\n",
    "}\n");
  CloseStream(out);
end;;
