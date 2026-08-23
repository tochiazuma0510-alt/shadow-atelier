#############################################################################
## D972 p=2 literal-A.18 finite-gate wrapper repair v13.
##
## Authenticates the frozen v12 generator, repairs only its stale inner
## bounded-scope firewall needle, writes a hash-pinned effective v13 generator,
## and executes it.  Mathematical formulas, universes, finite gates, internal
## V12 symbols, and the v12 literal-A.18 overlay are unchanged.  V12 remains
## immutable; only output paths/schema/diagnostics/firewall tokens are versioned.
#############################################################################

P159P2W13BasePath := "search/d972_pent_interleave_canary_p2_v12.g";
P159P2W13BaseBytes := 9940;
P159P2W13BaseSha :=
  "6b0bb30824053a3214d006b31fc9c0446f96d5207c818e479fcc5ad5a90b2d27";
P159P2W13EffectiveGeneratorPath :=
  "ci/out/d972_pent_interleave_canary_p2_generator_effective_v13.g";
P159P2W13EffectiveGeneratorBytes := 10146;
P159P2W13EffectiveGeneratorSha :=
  "a0521b49339fcd76bea3d6d943f27dca75a76052180c36ed85788b2521c7da8d";

P159P2W13Count := function(s,needle)
  local count,pos,tail,offset,rel;
  if Length(needle)=0 then Error("PENT159N_P2_V13_WRAPPER: empty needle"); fi;
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

P159P2W13Replace := function(s,old,new,expected,label)
  local got;
  got:=P159P2W13Count(s,old);
  if got<>expected then
    Error("PENT159N_P2_V13_WRAPPER: replacement count drift ",label,
      " expected=",expected," observed=",got);
  fi;
  return ReplacedString(s,old,new);
end;

P159P2W13Write := function(path,payload)
  local stream,readback;
  stream:=OutputTextFile(path,false);
  if stream=fail then
    Error("PENT159N_P2_V13_WRAPPER: cannot open effective generator");
  fi;
  SetPrintFormattingStatus(stream,false); PrintTo(stream,payload);
  CloseStream(stream); readback:=StringFile(path);
  if readback=fail or readback<>payload or
     HexSHA256(readback)<>HexSHA256(payload) then
    Error("PENT159N_P2_V13_WRAPPER: effective generator write mismatch");
  fi;
  return rec(bytes:=Length(readback),sha256:=HexSHA256(readback));
end;

P159P2W13Raw:=StringFile(P159P2W13BasePath);
if P159P2W13Raw=fail or Length(P159P2W13Raw)<>P159P2W13BaseBytes or
   HexSHA256(P159P2W13Raw)<>P159P2W13BaseSha then
  Error("PENT159N_P2_V13_WRAPPER: frozen v12 generator pin drift");
fi;

P159P2W13Out:=P159P2W13Raw;
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "PENT159N_P2_OUTER_V12","PENT159N_P2_OUTER_V13",1,
  "outer diagnostic namespace");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "PENT159N_P2_V12","PENT159N_P2_V13",15,
  "math diagnostic namespace");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "ci/out/d972_pent_interleave_canary_p2_outer_effective_v12.g",
  "ci/out/d972_pent_interleave_canary_p2_outer_effective_v13.g",1,
  "outer effective path");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "19737","19760",1,"outer effective bytes");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "15ca44dff4fa86c2d1a16af451804eeecc7fd93847db14332f251bf38f266ab4",
  "5c0b51fdb12f502ca492bae94c72f12e1c4564aaeccfc621a10fd809822e8f95",
  1,"outer effective SHA");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "ci/out/d972_pent_interleave_canary_p2_math_effective_v12.g",
  "ci/out/d972_pent_interleave_canary_p2_math_effective_v13.g",1,
  "math effective path");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "56651","56666",1,"math effective bytes");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "af9221aa753a5dbea60d88d7a6b0f459e02b52c78a0ba186bc56a6c277f8237a",
  "aeacb7e1c344f9a22b9abab5d580a20c367885ca339817f3b9475db91364323a",
  1,"math effective SHA");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "ci/out/d972_pent_interleave_canary_p2_receipt_v12_20260824.json",
  "ci/out/d972_pent_interleave_canary_p2_receipt_v13_20260824.json",1,
  "receipt path");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "d972-pent-interleave-canary-p2/v12",
  "d972-pent-interleave-canary-p2/v13",2,"schema strings");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "finite p=2 literal-A.18 finite-gate repair stage v12",
  "finite p=2 literal-A.18 finite-gate wrapper repair stage v13",1,
  "math header target");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "MEASURED_P2_LITERAL_A18_FINITE_GATE_REPAIR_V12",
  "MEASURED_P2_LITERAL_A18_FINITE_GATE_WRAPPER_REPAIR_V13",1,
  "receipt status target");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "p=2 literal-A.18 finite-gate repair v12 generator",
  "p=2 literal-A.18 finite-gate wrapper repair v13 effective generator",1,
  "generator header");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "mechanically generates a hash-pinned v12",
  "mechanically generates a hash-pinned v13",1,
  "generator contract header");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "p=2 literal-A.18 finite-gate repair v12",
  "p=2 literal-A.18 finite-gate wrapper repair v13",1,
  "outer header target");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "V12 evaluates both","V13 executes both",1,
  "generated math prose");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  "p2_v1_through_v11_edited:=false,v12_overwrote_prior_version:=false",
  "p2_v1_through_v12_edited:=false,v13_overwrote_prior_version:=false",1,
  "version boundary result");

P159P2W13Needle:=JoinStringsWithSeparator([
  "P159P2G12Out:=P159P2G12Replace(P159P2G12Out,",
  "  \"p2_v1_through_v10_edited:=false,v11_overwrote_prior_version:=false\",",
  "  \"p2_v1_through_v12_edited:=false,v13_overwrote_prior_version:=false\",1,",
  "  \"firewall version boundary\");"],"\n");
P159P2W13Insertion:=JoinStringsWithSeparator([
  P159P2W13Needle,
  "P159P2G12Out:=P159P2G12Replace(P159P2G12Out,",
  "  \"p2_v1_through_v10_edited:=false\",",
  "  \"p2_v1_through_v12_edited:=false\",2,",
  "  \"bounded-scope firewall wrapper repair\");"],"\n");
P159P2W13Out:=P159P2W13Replace(P159P2W13Out,
  P159P2W13Needle,P159P2W13Insertion,1,"bounded-scope patch insertion");

if Length(P159P2W13Out)<>P159P2W13EffectiveGeneratorBytes or
   HexSHA256(P159P2W13Out)<>P159P2W13EffectiveGeneratorSha then
  Error("PENT159N_P2_V13_WRAPPER: effective generator pin drift bytes=",
    Length(P159P2W13Out)," sha256=",HexSHA256(P159P2W13Out));
fi;
P159P2W13WriteState:=P159P2W13Write(P159P2W13EffectiveGeneratorPath,
  P159P2W13Out);
Print("PENT159N_P2_V13_EFFECTIVE_GENERATOR_WRITTEN path=",
  P159P2W13EffectiveGeneratorPath," bytes=",P159P2W13WriteState.bytes,
  " sha256=",P159P2W13WriteState.sha256,
  " repair=stale_bounded_scope_firewall_tokens_only\n");
Read(P159P2W13EffectiveGeneratorPath);

if not IsBoundGlobal("P159P2V12Receipt") or
   not IsBoundGlobal("P159P2V12Write") then
  Error("PENT159N_P2_V13_WRAPPER: effective generator returned without receipt");
fi;
P159P2W13Receipt:=ValueGlobal("P159P2V12Receipt");
P159P2W13Gate:=P159P2W13Receipt.marked_maps.a18_source_relator_gate;
if P159P2W13Receipt.schema<>"d972-pent-interleave-canary-p2/v13" or
   P159P2W13Gate.literal_all_relators_preserved<>true or
   P159P2W13Gate.required_reversal_mutant_failure.passed<>false or
   P159P2W13Receipt.firewall.class4_row36_mode_K2_work_performed<>false or
   P159P2W13Receipt.firewall.p2_v1_through_v12_edited<>false or
   P159P2W13Receipt.firewall.v13_overwrote_prior_version<>false then
  Error("PENT159N_P2_V13_WRAPPER: final receipt/firewall check failed");
fi;
Print("PENT159N_P2_V13_WRAPPER_FINAL_PASS receipt_schema=",
  P159P2W13Receipt.schema," literal_relator_rows=",
  P159P2W13Gate.literal_relator_gate_row_count,
  " math_universe_change=false\n");
