#############################################################################
## D972 p=2 literal-A.18 finite-gate repair v12 generator.
##
## Authenticates frozen outer v11, mechanically generates a hash-pinned v12
## outer with the efficient Q4-coordinate relator gate, executes it, and checks
## the closed receipt state.  V11 remains untouched as a superseded resource
## trap.  No checker source, verdict, or report is read or imported.
#############################################################################

P159P2G12BaseOuterPath := "search/d972_pent_interleave_canary_p2_v11.g";
P159P2G12BaseOuterBytes := 19354;
P159P2G12BaseOuterSha :=
  "bb795216135b6b38e9257009f9c073a0085df1ec0e728207201a4145af0bab7b";
P159P2G12OverlayPath :=
  "search/d972_pent_interleave_literal_a18_p2_overlay_v12.g";
P159P2G12OverlayBytes := 5687;
P159P2G12OverlaySha :=
  "755e431a91478ee5ca3581ecb84b4be10b1c569983d4ebaca494857cd4adb28d";
P159P2G12GeneratedOuterPath :=
  "ci/out/d972_pent_interleave_canary_p2_outer_effective_v12.g";
P159P2G12GeneratedOuterBytes := 19737;
P159P2G12GeneratedOuterSha :=
  "15ca44dff4fa86c2d1a16af451804eeecc7fd93847db14332f251bf38f266ab4";

P159P2G12Count := function(s,needle)
  local count,pos,tail,offset,rel;
  if Length(needle)=0 then Error("PENT159N_P2_V12_GENERATOR: empty needle"); fi;
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

P159P2G12Replace := function(s,old,new,expected,label)
  local got;
  got:=P159P2G12Count(s,old);
  if got<>expected then
    Error("PENT159N_P2_V12_GENERATOR: replacement count drift ",label,
      " expected=",expected," observed=",got);
  fi;
  return ReplacedString(s,old,new);
end;

P159P2G12Write := function(path,payload)
  local stream,readback;
  stream:=OutputTextFile(path,false);
  if stream=fail then Error("PENT159N_P2_V12_GENERATOR: cannot open generated outer"); fi;
  SetPrintFormattingStatus(stream,false); PrintTo(stream,payload); CloseStream(stream);
  readback:=StringFile(path);
  if readback=fail or readback<>payload or
     HexSHA256(readback)<>HexSHA256(payload) then
    Error("PENT159N_P2_V12_GENERATOR: generated outer closed-write mismatch");
  fi;
  return rec(bytes:=Length(readback),sha256:=HexSHA256(readback));
end;

P159P2G12Raw:=StringFile(P159P2G12BaseOuterPath);
if P159P2G12Raw=fail or Length(P159P2G12Raw)<>P159P2G12BaseOuterBytes or
   HexSHA256(P159P2G12Raw)<>P159P2G12BaseOuterSha then
  Error("PENT159N_P2_V12_GENERATOR: frozen v11 outer pin drift");
fi;
P159P2G12OverlayRaw:=StringFile(P159P2G12OverlayPath);
if P159P2G12OverlayRaw=fail or
   Length(P159P2G12OverlayRaw)<>P159P2G12OverlayBytes or
   HexSHA256(P159P2G12OverlayRaw)<>P159P2G12OverlaySha then
  Error("PENT159N_P2_V12_GENERATOR: v12 finite-gate overlay pin drift");
fi;

P159P2G12Out:=P159P2G12Raw;
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "P159P2O11","P159P2O12",187,"outer namespace");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "P159P2V11","P159P2V12",97,"math namespace strings");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "PENT159N_P2_OUTER_V11","PENT159N_P2_OUTER_V12",16,
  "outer diagnostic namespace");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "PENT159N_P2_V11","PENT159N_P2_V12",13,
  "math diagnostic strings");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "p=2 literal-A.18 repair v11",
  "p=2 literal-A.18 finite-gate repair v12",1,"outer header");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "search/d972_pent_interleave_literal_a18_p2_overlay_v11.g",
  P159P2G12OverlayPath,4,"overlay paths");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "6048","5687",1,"overlay bytes");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "a20a3dc8e4847109ee7172040495421027678b4cb4167247f64b948df20c13a8",
  P159P2G12OverlaySha,3,"overlay SHA");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "ci/out/d972_pent_interleave_canary_p2_math_effective_v11.g",
  "ci/out/d972_pent_interleave_canary_p2_math_effective_v12.g",1,
  "math effective path");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "56314","56651",1,"math effective bytes");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "6f6f7b1a9adbc54882006865b29b77d8560fefbaa5e015c6d60511dc56a96404",
  "af9221aa753a5dbea60d88d7a6b0f459e02b52c78a0ba186bc56a6c277f8237a",
  1,"math effective SHA");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "ci/out/d972_pent_interleave_canary_p2_receipt_v11_20260824.json",
  "ci/out/d972_pent_interleave_canary_p2_receipt_v12_20260824.json",1,
  "receipt path");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "d972-pent-interleave-canary-p2/v11",
  "d972-pent-interleave-canary-p2/v12",2,"schema strings");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "finite p=2 literal-A.18 repair stage v11",
  "finite p=2 literal-A.18 finite-gate repair stage v12",1,
  "generated math header");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "MEASURED_P2_LITERAL_A18_REPAIR_V11",
  "MEASURED_P2_LITERAL_A18_FINITE_GATE_REPAIR_V12",1,
  "receipt status");

P159P2G12OldHeader:=JoinStringsWithSeparator([
  "## Producer-only literal-A.18 repair derived mechanically from frozen p2 v10.\",",
  "  \"## It reads no checker source, verdict, or report.  Before any quotient census,\",",
  "  \"## every printed A.18 coface is serialized once to native order and must preserve\",",
  "  \"## both frozen PB3 relators.  The prior direct-use reversal is mutant-only."],"\n");
P159P2G12NewHeader:=JoinStringsWithSeparator([
  "## Producer-only finite-gate literal-A.18 repair derived from frozen p2 v10.\",",
  "  \"## It reads no checker source, verdict, or report.  V11's pre-quotient naive\",",
  "  \"## faithful-Artin replay is superseded as a resource trap.  V12 evaluates both\",",
  "  \"## frozen PB3 relators in marked Q4 before any marked map or Q2 census."],"\n");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  P159P2G12OldHeader,P159P2G12NewHeader,1,"generated header body");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "literal A.18 p2 v11 source-relator overlay",
  "literal A.18 p2 v12 finite source-relator overlay",1,"overlay label");

P159P2G12OldEarly:=JoinStringsWithSeparator([
  "  \"if not IsBoundGlobal(\\\"P159P2V12A18GateReceipt\\\") or\",",
  "  \"   P159P2V12A18GateReceipt.literal_all_relators_preserved<>true then\",",
  "  \"  Error(\\\"PENT159N_P2_V12: literal A.18 pre-census gate did not close\\\");\","],"\n");
P159P2G12NewEarly:=JoinStringsWithSeparator([
  "  \"if not IsBoundGlobal(\\\"P159P2V12A18RunFiniteRelatorGate\\\") then\",",
  "  \"  Error(\\\"PENT159N_P2_V12: literal A.18 finite relator-gate function absent\\\");\","],"\n");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  P159P2G12OldEarly,P159P2G12NewEarly,1,"deferred finite-gate check");

P159P2G12OldMapStart:=JoinStringsWithSeparator([
  "P159P2O12NewMap:=JoinStringsWithSeparator([",
  "  \"P159P2V12DelWords:=P159P2V12Deletions(4);\","],"\n");
P159P2G12NewMapStart:=JoinStringsWithSeparator([
  "P159P2O12NewMap:=JoinStringsWithSeparator([",
  "  \"P159P2V12A18GateReceipt:=P159P2V12A18RunFiniteRelatorGate(\",",
  "  \"  P159P2V12Q4,P159P2V12Q4Pc);\",",
  "  \"if P159P2V12A18GateReceipt.literal_all_relators_preserved<>true then\",",
  "  \"  Error(\\\"PENT159N_P2_V12: finite A.18 gate did not close before maps/census\\\");\",",
  "  \"fi;\",",
  "  \"P159P2V12DelWords:=P159P2V12Deletions(4);\","],"\n");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  P159P2G12OldMapStart,P159P2G12NewMapStart,1,"finite-gate call");

P159P2G12OldProv:=JoinStringsWithSeparator([
  "  \"    predecessor_p2_v10_semantic_status:=\\\"REJECTED_AT_A18_HOMOMORPHISM_BOUNDARY\\\",\",",
  "  \"    predecessor_run_id:=P159P2V12PredecessorRun,\"],\"\\n\");"],"\n");
P159P2G12NewProv:=JoinStringsWithSeparator([
  "  \"    predecessor_p2_v10_semantic_status:=\\\"REJECTED_AT_A18_HOMOMORPHISM_BOUNDARY\\\",\",",
  "  \"    superseded_p2_v11_run_id:=32656923609,\",",
  "  \"    superseded_p2_v11_status:=\\\"CANCELLED_RESOURCE_TRAP_NAIVE_FAITHFUL_ARTIN_REPLAY\\\",\",",
  "  \"    predecessor_run_id:=P159P2V12PredecessorRun,\"],\"\\n\");"],"\n");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  P159P2G12OldProv,P159P2G12NewProv,1,"v11 resource-trap provenance");
P159P2G12Out:=P159P2G12Replace(P159P2G12Out,
  "p2_v1_through_v10_edited:=false,v11_overwrote_prior_version:=false",
  "p2_v1_through_v11_edited:=false,v12_overwrote_prior_version:=false",1,
  "firewall version boundary");

if Length(P159P2G12Out)<>P159P2G12GeneratedOuterBytes or
   HexSHA256(P159P2G12Out)<>P159P2G12GeneratedOuterSha then
  Error("PENT159N_P2_V12_GENERATOR: generated outer pin drift bytes=",
    Length(P159P2G12Out)," sha256=",HexSHA256(P159P2G12Out));
fi;
P159P2G12WriteState:=P159P2G12Write(P159P2G12GeneratedOuterPath,
  P159P2G12Out);
Print("PENT159N_P2_V12_OUTER_GENERATED path=",P159P2G12GeneratedOuterPath,
  " bytes=",P159P2G12WriteState.bytes," sha256=",
  P159P2G12WriteState.sha256," v11_resource_trap_superseded=true\n");
Read(P159P2G12GeneratedOuterPath);

if not IsBoundGlobal("P159P2V12Receipt") or
   not IsBoundGlobal("P159P2V12Write") then
  Error("PENT159N_P2_V12_GENERATOR: generated outer returned without receipt");
fi;
P159P2G12Receipt:=ValueGlobal("P159P2V12Receipt");
P159P2G12Gate:=P159P2G12Receipt.marked_maps.a18_source_relator_gate;
if P159P2G12Receipt.schema<>"d972-pent-interleave-canary-p2/v12" or
   P159P2G12Gate.literal_all_relators_preserved<>true or
   P159P2G12Gate.required_reversal_mutant_failure.passed<>false then
  Error("PENT159N_P2_V12_GENERATOR: final finite-gate receipt check failed");
fi;
Print("PENT159N_P2_V12_GENERATOR_FINAL_PASS receipt_schema=",
  P159P2G12Receipt.schema," literal_relator_rows=",
  P159P2G12Gate.literal_relator_gate_row_count,"\n");
