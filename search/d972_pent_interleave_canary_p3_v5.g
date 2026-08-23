#############################################################################
## D972 p=3 literal-A.18 identity-serialization repair v5 generator.
##
## Authenticates the unexecuted v3 generator template, emits a hash-pinned v5
## outer using versioned v5 overlays, executes it, and checks the closed receipt.
## No checker source, verdict, or report is read or imported.
#############################################################################

P159P3G4BasePath := "search/d972_pent_interleave_canary_p3_v3.g";
P159P3G4BaseBytes := 22050;
P159P3G4BaseSha :=
  "2d2e98dfe8662cc5ac41b28449cb218e8d715473c0ac25e43f44771b9128b8ce";
P159P3G4A18Path :=
  "search/d972_pent_interleave_literal_a18_p3_overlay_v5.g";
P159P3G4A18Bytes := 11501;
P159P3G4A18Sha :=
  "99d3b67d2fc7b0661505a37b8925ac60b88b6195059d3c2e6df1e41c6431b50f";
P159P3G4ControlPath :=
  "search/d972_pent_interleave_canary_p3_control_overlay_v5.g";
P159P3G4ControlBytes := 5342;
P159P3G4ControlSha :=
  "ed4f66247e7a13aedf2c782223cf5f5a4bbbe48554ba71e6f4b210da28599052";
P159P3G4GeneratedOuterPath :=
  "ci/out/d972_pent_interleave_canary_p3_outer_effective_v5.g";
P159P3G4GeneratedOuterBytes := 22325;
P159P3G4GeneratedOuterSha :=
  "c8c80e647a926ed33ac3795924f173bf162611a4f5d4325ac9441eeac84813ab";

P159P3G4Count := function(s,needle)
  local count,pos,tail,offset,rel;
  if Length(needle)=0 then Error("PENT159N_P3_V5_GENERATOR: empty needle"); fi;
  count:=0; pos:=PositionSublist(s,needle);
  while pos<>fail do
    count:=count+1; offset:=pos+Length(needle);
    if offset>Length(s) then pos:=fail;
    else
      tail:=s{[offset..Length(s)]}; rel:=PositionSublist(tail,needle);
      if rel=fail then pos:=fail; else pos:=offset+rel-1; fi;
    fi;
  od;
  return count;
end;

P159P3G4Replace := function(s,old,new,expected,label)
  local got;
  got:=P159P3G4Count(s,old);
  if got<>expected then
    Error("PENT159N_P3_V5_GENERATOR: replacement count drift ",label,
      " expected=",expected," observed=",got);
  fi;
  return ReplacedString(s,old,new);
end;

P159P3G4Write := function(path,payload)
  local stream,readback;
  stream:=OutputTextFile(path,false);
  if stream=fail then Error("PENT159N_P3_V5_GENERATOR: cannot open generated outer"); fi;
  SetPrintFormattingStatus(stream,false); PrintTo(stream,payload); CloseStream(stream);
  readback:=StringFile(path);
  if readback=fail or readback<>payload or
     HexSHA256(readback)<>HexSHA256(payload) then
    Error("PENT159N_P3_V5_GENERATOR: generated outer closed-write mismatch");
  fi;
  return rec(bytes:=Length(readback),sha256:=HexSHA256(readback));
end;

P159P3G4Raw:=StringFile(P159P3G4BasePath);
if P159P3G4Raw=fail or Length(P159P3G4Raw)<>P159P3G4BaseBytes or
   HexSHA256(P159P3G4Raw)<>P159P3G4BaseSha then
  Error("PENT159N_P3_V5_GENERATOR: unexecuted v3 template pin drift");
fi;
P159P3G4A18Raw:=StringFile(P159P3G4A18Path);
if P159P3G4A18Raw=fail or Length(P159P3G4A18Raw)<>P159P3G4A18Bytes or
   HexSHA256(P159P3G4A18Raw)<>P159P3G4A18Sha then
  Error("PENT159N_P3_V5_GENERATOR: v5 A.18 overlay pin drift");
fi;
P159P3G4ControlRaw:=StringFile(P159P3G4ControlPath);
if P159P3G4ControlRaw=fail or
   Length(P159P3G4ControlRaw)<>P159P3G4ControlBytes or
   HexSHA256(P159P3G4ControlRaw)<>P159P3G4ControlSha then
  Error("PENT159N_P3_V5_GENERATOR: v5 control overlay pin drift");
fi;

P159P3G4Out:=P159P3G4Raw;
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "P159P3O3","P159P3O4",224,"outer namespace");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "P159P3V3","P159P3V4",103,"math namespace strings");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "PENT159N_P3_OUTER_V3","PENT159N_P3_OUTER_V5",17,
  "outer diagnostics");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "PENT159N_P3_V3","PENT159N_P3_V5",12,"math diagnostics");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "p=3 literal-A.18 repair v3",
  "p=3 literal-A.18 identity-serialization repair v5",1,"header");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "search/d972_pent_interleave_literal_a18_p3_overlay_v3.g",
  P159P3G4A18Path,4,"A.18 overlay paths");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "ee165826581f15848cc06c94762a337909c40718eb1a1bf6dc8e02c156a66fab",
  P159P3G4A18Sha,3,"A.18 overlay SHA");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "search/d972_pent_interleave_canary_p3_control_overlay_v3.g",
  P159P3G4ControlPath,3,"control overlay paths");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "fc977883d147469b6c6ad56d6ef69cb8b1f5579a4c599378339077840a71d36c",
  P159P3G4ControlSha,3,"control overlay SHA");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "ci/out/d972_pent_interleave_canary_p3_math_effective_v3.g",
  "ci/out/d972_pent_interleave_canary_p3_math_effective_v5.g",1,
  "math effective path");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "56579","56816",1,"math effective bytes");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "5dbaa59b63a4280727f9da4f109b452d30de16d1bc46eaa225df7fc024c23b3e",
  "bf7c81cf593309ea63f0e411174e1bb04f1e075455a08b3e7a06e091d017936a",
  1,"math effective SHA");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "ci/out/d972_pent_interleave_canary_p3_receipt_v3_20260824.json",
  "ci/out/d972_pent_interleave_canary_p3_receipt_v5_20260824.json",1,
  "receipt path");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "d972-pent-interleave-canary-p3/v3",
  "d972-pent-interleave-canary-p3/v5",2,"schema strings");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "MEASURED_P3_LITERAL_A18_REPAIR_V3",
  "MEASURED_P3_LITERAL_A18_IDENTITY_SERIALIZATION_REPAIR_V5",1,"receipt status");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "v3 literal-A.18 complete actual-coface control overlay",
  "v5 literal-A.18 complete actual-coface control overlay",1,
  "control label");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "NOT_IN_P3_V3_BOUNDED_STAGE","NOT_IN_P3_V5_BOUNDED_STAGE",1,
  "deferred version string");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "p3_v1_through_v2_edited","p3_v1_through_v4_edited",1,
  "firewall version boundary");

P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "P159P3O4A18Bytes := 5627;",
  "P159P3O4A18Bytes := 11501;",1,"A.18 overlay bytes");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "finite p=3 literal-A.18 repair stage v3",
  "finite p=3 literal-A.18 identity-serialization repair stage v5",1,
  "effective stage header");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "## Before any quotient or census, each printed A.18 word is serialized exactly",
  "## After marked Q4 exists and before maps/census, every printed A.18 group",1,
  "header gate placement line 1");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "## once to native order and both frozen PB3 source relators must map to identity.",
  "## product is consumed literally and both frozen PB3 relators must map to identity.",1,
  "header gate placement line 2");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "literal A.18 p3 v3 source-relator overlay",
  "literal A.18 p3 v5 identity-serialization overlay",1,
  "A.18 overlay label");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "[[4,2],[6]]","[[2,4],[6]]",1,"slot1 native context");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "[[2,1],[6,5]]","[[1,2],[5,6]]",1,"slot2 native context");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "[[1],[5,4]]","[[1],[4,5]]",1,"slot3 native context");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  "literal printed A.18 paper words reversed exactly once to native order",
  "literal printed A.18 group products consumed unchanged in native multiplication order",
  1,"receipt A.18 serialization");

P159P3G4OldProv:=JoinStringsWithSeparator([
  "  \"    rejected_p3_v2_receipt_sha256:=\\\"51d1bd649182b951fb7bed363f11eb854ad8d4ab824b87b1cc670c90ab253e56\\\",\",",
  "  \"    p2_trigger_run_id:=P159P3V4P2TriggerRun,\"],\"\\n\");"],"\n");
P159P3G4NewProv:=JoinStringsWithSeparator([
  "  \"    rejected_p3_v2_receipt_sha256:=\\\"51d1bd649182b951fb7bed363f11eb854ad8d4ab824b87b1cc670c90ab253e56\\\",\",",
  "  \"    superseded_p3_v3_status:=\\\"UNEXECUTED_DRAFT_REPLACED_BY_VERSIONED_V4_FINITE_GATE\\\",\",",
  "  \"    superseded_p3_v4_status:=\\\"HELD_UNEXECUTED_AFTER_SHARED_A18_REVERSAL_REJECTION\\\",\",",
  "  \"    p2_trigger_run_id:=P159P3V4P2TriggerRun,\"],\"\\n\");"],"\n");
P159P3G4Out:=P159P3G4Replace(P159P3G4Out,
  P159P3G4OldProv,P159P3G4NewProv,1,"v3 supersession provenance");

if Length(P159P3G4Out)<>P159P3G4GeneratedOuterBytes or
   HexSHA256(P159P3G4Out)<>P159P3G4GeneratedOuterSha then
  Error("PENT159N_P3_V5_GENERATOR: generated outer pin drift bytes=",
    Length(P159P3G4Out)," sha256=",HexSHA256(P159P3G4Out));
fi;
P159P3G4WriteState:=P159P3G4Write(P159P3G4GeneratedOuterPath,P159P3G4Out);
Print("PENT159N_P3_V5_OUTER_GENERATED path=",P159P3G4GeneratedOuterPath,
  " bytes=",P159P3G4WriteState.bytes," sha256=",P159P3G4WriteState.sha256,
  " v3_unexecuted_draft_superseded=true\n");
Read(P159P3G4GeneratedOuterPath);

if not IsBoundGlobal("P159P3V4Receipt") or
   not IsBoundGlobal("P159P3V4Write") then
  Error("PENT159N_P3_V5_GENERATOR: generated outer returned without receipt");
fi;
P159P3G4Receipt:=ValueGlobal("P159P3V4Receipt");
P159P3G4Gate:=P159P3G4Receipt.marked_maps.a18_source_relator_gate;
if P159P3G4Receipt.schema<>"d972-pent-interleave-canary-p3/v5" or
   P159P3G4Gate.literal_all_relators_preserved<>true or
   P159P3G4Gate.required_reversal_mutant_failure.passed<>false then
  Error("PENT159N_P3_V5_GENERATOR: final finite-gate receipt check failed");
fi;
Print("PENT159N_P3_V5_GENERATOR_FINAL_PASS receipt_schema=",
  P159P3G4Receipt.schema," literal_relator_rows=",
  P159P3G4Gate.literal_relator_gate_row_count,"\n");
