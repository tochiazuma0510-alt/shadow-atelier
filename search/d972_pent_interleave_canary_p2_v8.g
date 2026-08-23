#############################################################################
## D972 corrected pentagon-interleave canary, finite p=2 stage v8.
##
## Versioned receipt-syntax repair after GHA run 32650001325.  That run
## passed every v7 mathematical gate through the complete actual-charming
## gate, then GAP reported a syntax error in the frozen v5 receipt constructor:
## `identity:` was missing the assignment `=`.  The existing runner did not
## propagate the GAP syntax diagnostic and therefore exited zero without a
## receipt.  V8 authenticates the complete frozen v7 generation chain and
## applies exactly that one-token repair, with exact-count and hash gates.
#############################################################################

P159V8OuterSource := "search/d972_pent_interleave_canary_p2_v8.g";
P159V8V7Outer := "search/d972_pent_interleave_canary_p2_v7.g";
P159V8V7OuterSha :=
  "d8599a670af5bb2909e03db31a537e209ef9472d8a96a7e42fa734bde7c0e5a9";
P159V8V7GeneratedWrapperSha :=
  "fc4fc99605ae135cefd52cb59f81aed2dc9d0dec4761fbdad9865fd77005bc14";
P159V8BootstrapSourcePath :=
  "ci/out/d972_pent_interleave_canary_p2_v7_bootstrap_source_v8.g";
P159V8BootstrapWrapperPath :=
  "ci/out/d972_pent_interleave_canary_p2_v7_bootstrap_wrapper_v8.g";
P159V8GeneratedWrapperPath :=
  "ci/out/d972_pent_interleave_canary_p2_wrapper_effective_v8.g";
P159V8ExpectedReceiptPath :=
  "ci/out/d972_pent_interleave_canary_p2_receipt_v8_20260824.json";
P159V8ExpectedMathEffectiveSha :=
  "8be94c1ea3bb1524201a69348b28333ddfcd1435cf8cb7aa62a28195b49537ec";
P159V8ExpectedGeneratedWrapperSha :=
  "f15999b5d7249cfe84b69a0dc4e51ad1e16244a6144ace64e8efc9c88d0f3141";

P159V8CountSublist := function(s,needle)
  local count,pos,tail,offset,rel;
  if Length(needle)=0 then Error("PENT159N_V8: empty replacement needle"); fi;
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

P159V8ReplaceExact := function(s,old,new,expected,label)
  local got;
  got:=P159V8CountSublist(s,old);
  if got<>expected then
    Error("PENT159N_V8: replacement count drift ",label,
      " expected=",expected," observed=",got);
  fi;
  return ReplacedString(s,old,new);
end;

P159V8CheckedWriteText := function(path,payload,label)
  local stream,readback;
  stream:=OutputTextFile(path,false);
  if stream=fail then Error("PENT159N_V8: cannot open ",label); fi;
  SetPrintFormattingStatus(stream,false);
  PrintTo(stream,payload);
  CloseStream(stream);
  readback:=StringFile(path);
  if readback=fail or readback<>payload or
     HexSHA256(readback)<>HexSHA256(payload) then
    Error("PENT159N_V8: closed-write/hash mismatch ",label);
  fi;
  return rec(bytes:=Length(readback),sha256:=HexSHA256(readback));
end;

## Execute the frozen v7 outer generator only far enough to reproduce its
## authenticated generated wrapper.  Suppress its final Read so the invalid
## v7 receipt tail is never executed or promoted.
P159V8V7Raw:=StringFile(P159V8V7Outer);
if P159V8V7Raw=fail or HexSHA256(P159V8V7Raw)<>P159V8V7OuterSha then
  Error("PENT159N_V8: frozen v7 outer source missing or SHA drift");
fi;
P159V8Bootstrap:=P159V8V7Raw;
P159V8Bootstrap:=P159V8ReplaceExact(P159V8Bootstrap,
  Concatenation(
    "P159V7GeneratedWrapperPath :=\n",
    "  \"ci/out/d972_pent_interleave_canary_p2_wrapper_effective_v7.g\";"),
  Concatenation(
    "P159V7GeneratedWrapperPath :=\n",
    "  \"ci/out/d972_pent_interleave_canary_p2_v7_bootstrap_wrapper_v8.g\";"),
  1,"v7 bootstrap wrapper path");
P159V8Bootstrap:=P159V8ReplaceExact(P159V8Bootstrap,
  "PENT159N_P2_V7_WRAPPER_SOURCE_WRITTEN",
  "PENT159N_P2_V8_V7_BOOTSTRAP_WRAPPER_WRITTEN",1,
  "bootstrap marker isolation");
P159V8Bootstrap:=P159V8ReplaceExact(P159V8Bootstrap,
  "Read(P159V7GeneratedWrapperPath);",
  Concatenation(
    "Print(\"PENT159N_P2_V8_V7_BOOTSTRAP_COMPLETE sha256=\",",
    "P159V7GeneratedWrapperSha,\"\\n\");"),
  1,"suppress invalid v7 execution");
P159V8BootstrapWrite:=P159V8CheckedWriteText(P159V8BootstrapSourcePath,
  P159V8Bootstrap,"v7 bootstrap source");
Print("PENT159N_P2_V8_V7_BOOTSTRAP_SOURCE_WRITTEN path=",
  P159V8BootstrapSourcePath," bytes=",P159V8BootstrapWrite.bytes,
  " sha256=",P159V8BootstrapWrite.sha256,"\n");
Read(P159V8BootstrapSourcePath);

if not IsBound(P159V7GeneratedWrapper) or
   HexSHA256(P159V7GeneratedWrapper)<>P159V8V7GeneratedWrapperSha then
  Error("PENT159N_V8: frozen v7 generated-wrapper reconstruction drift");
fi;

## Version the authenticated v7 generated wrapper.  All replacements below
## are deterministic metadata/namespace changes except the separately marked
## exact one-token receipt repair.
P159V8GeneratedWrapper:=P159V7GeneratedWrapper;
P159V8GeneratedWrapper:=P159V8ReplaceExact(P159V8GeneratedWrapper,
  "P159V7","P159V8",171,"v7 wrapper symbol namespace");
P159V8GeneratedWrapper:=P159V8ReplaceExact(P159V8GeneratedWrapper,
  "PENT159N_V7","PENT159N_V8",15,"v7 diagnostic namespace");
P159V8GeneratedWrapper:=P159V8ReplaceExact(P159V8GeneratedWrapper,
  "PENT159N_P2_V7","PENT159N_P2_V8",2,"v8 semantic marker target");
P159V8GeneratedWrapper:=P159V8ReplaceExact(P159V8GeneratedWrapper,
  "search/d972_pent_interleave_canary_p2_v7.g",
  "search/d972_pent_interleave_canary_p2_v8.g",2,"v8 source path");
P159V8GeneratedWrapper:=P159V8ReplaceExact(P159V8GeneratedWrapper,
  "d972_pent_interleave_canary_p2_effective_v7.g",
  "d972_pent_interleave_canary_p2_effective_v8.g",1,
  "v8 effective source path");
P159V8GeneratedWrapper:=P159V8ReplaceExact(P159V8GeneratedWrapper,
  "d972_pent_interleave_canary_p2_receipt_v7_20260824.json",
  "d972_pent_interleave_canary_p2_receipt_v8_20260824.json",1,
  "v8 receipt path");
P159V8GeneratedWrapper:=P159V8ReplaceExact(P159V8GeneratedWrapper,
  "d972-pent-interleave-canary-p2/v7",
  "d972-pent-interleave-canary-p2/v8",1,"v8 receipt schema");
P159V8GeneratedWrapper:=P159V8ReplaceExact(P159V8GeneratedWrapper,
  "effective_v7_source","effective_v8_source",2,
  "v8 effective-source receipt field names");

P159V8ReceiptSyntaxPatchBlock:=Concatenation(
  "## V8: repair the frozen v5 receipt field syntax by an exact one-token patch.\n",
  "P159V8Effective:=P159V8ReplaceExact(P159V8Effective,\n",
  "  \"      identity:\\\"gamma4(G) G^2 = G^2 because gamma2(G) <= G^2\\\",\",\n",
  "  \"      identity:=\\\"gamma4(G) G^2 = G^2 because gamma2(G) <= G^2\\\",\",\n",
  "  1,\"receipt original W2 identity assignment\");\n\n");
P159V8GeneratedWrapper:=P159V8ReplaceExact(P159V8GeneratedWrapper,
  "## Rename every semantic marker last, including the newly inserted control",
  Concatenation(P159V8ReceiptSyntaxPatchBlock,
    "## Rename every semantic marker last, including the newly inserted control"),
  1,"insert exact receipt syntax repair");

P159V8GeneratedWrapperSha:=HexSHA256(P159V8GeneratedWrapper);
if P159V8GeneratedWrapperSha<>P159V8ExpectedGeneratedWrapperSha then
  Error("PENT159N_V8: generated-wrapper SHA drift ",
    P159V8GeneratedWrapperSha);
fi;
P159V8GeneratedWrapperWrite:=P159V8CheckedWriteText(
  P159V8GeneratedWrapperPath,P159V8GeneratedWrapper,"v8 generated wrapper");
Print("PENT159N_P2_V8_WRAPPER_SOURCE_WRITTEN path=",
  P159V8GeneratedWrapperPath," bytes=",P159V8GeneratedWrapperWrite.bytes,
  " sha256=",P159V8GeneratedWrapperWrite.sha256,
  " v7_generated_wrapper_sha256=",P159V8V7GeneratedWrapperSha,
  " receipt_syntax_patch_count=1\n");
Read(P159V8GeneratedWrapperPath);

## A nested Read containing a GAP syntax diagnostic can return to its caller
## without making the workflow process fail.  Require the closed receipt state
## after Read, so the v7 masked-success mode cannot recur unnoticed.
if not IsBoundGlobal("P159V5Write") or
   not IsBoundGlobal("P159V5Receipt") or
   not IsBoundGlobal("P159V5Output") then
  Error("PENT159N_V8: effective source returned without closed receipt state");
fi;
P159V8ReceiptWriteState:=ValueGlobal("P159V5Write");
P159V8ReceiptState:=ValueGlobal("P159V5Receipt");
P159V8ReceiptOutputState:=ValueGlobal("P159V5Output");
if not IsRecord(P159V8ReceiptWriteState) or
   not IsRecord(P159V8ReceiptState) or
   P159V8ReceiptOutputState<>P159V8ExpectedReceiptPath then
  Error("PENT159N_V8: effective source returned invalid receipt state");
fi;
P159V8ReceiptReadback:=StringFile(P159V8ExpectedReceiptPath);
if P159V8ReceiptReadback=fail or
   Length(P159V8ReceiptReadback)<>P159V8ReceiptWriteState.bytes or
   HexSHA256(P159V8ReceiptReadback)<>P159V8ReceiptWriteState.sha256 then
  Error("PENT159N_V8: outer receipt readback/hash gate failed");
fi;
Print("PENT159N_P2_V8_OUTER_FINAL_PASS receipt_path=",
  P159V8ExpectedReceiptPath," bytes=",P159V8ReceiptWriteState.bytes,
  " sha256=",P159V8ReceiptWriteState.sha256," terminal=",
  P159V8ReceiptState.terminal_token,"\n");
