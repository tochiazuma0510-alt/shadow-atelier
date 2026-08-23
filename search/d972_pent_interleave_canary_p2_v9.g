#############################################################################
## D972 corrected pentagon-interleave canary, finite p=2 stage v9.
##
## Versioned receipt-syntax repair after GHA run 32650825593.  The v8 outer
## fail-closed gate exposed the second and final malformed frozen-v5 receipt
## field: `PB4_quotient:` was missing `=`.  V9 authenticates v8, preserves its
## exact identity-field repair, and adds only the remaining one-token repair
## `PB4_quotient:` to `PB4_quotient:=`, with exact-count and hash gates.
#############################################################################

P159V9OuterSource := "search/d972_pent_interleave_canary_p2_v9.g";
P159V9V8Outer := "search/d972_pent_interleave_canary_p2_v8.g";
P159V9V8OuterSha :=
  "7b00c22889511e94586550e7ba9068c5dcbd898da43c246492079108731d07da";
P159V9V7Outer := "search/d972_pent_interleave_canary_p2_v7.g";
P159V9V7OuterSha :=
  "d8599a670af5bb2909e03db31a537e209ef9472d8a96a7e42fa734bde7c0e5a9";
P159V9V7GeneratedWrapperSha :=
  "fc4fc99605ae135cefd52cb59f81aed2dc9d0dec4761fbdad9865fd77005bc14";
P159V9BootstrapSourcePath :=
  "ci/out/d972_pent_interleave_canary_p2_v7_bootstrap_source_v9.g";
P159V9BootstrapWrapperPath :=
  "ci/out/d972_pent_interleave_canary_p2_v7_bootstrap_wrapper_v9.g";
P159V9GeneratedWrapperPath :=
  "ci/out/d972_pent_interleave_canary_p2_wrapper_effective_v9.g";
P159V9ExpectedReceiptPath :=
  "ci/out/d972_pent_interleave_canary_p2_receipt_v9_20260824.json";
P159V9ExpectedMathEffectiveSha :=
  "1d020d26a7aedb34a6b2d5732b0d95e36cc13b7c2a5e0424209d012d1695643d";
P159V9ExpectedGeneratedWrapperSha :=
  "d36191bec066d26ac83bb488d78b122259a92dc529e4ea3cc187e9e916e1659e";

P159V9CountSublist := function(s,needle)
  local count,pos,tail,offset,rel;
  if Length(needle)=0 then Error("PENT159N_V9: empty replacement needle"); fi;
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

P159V9ReplaceExact := function(s,old,new,expected,label)
  local got;
  got:=P159V9CountSublist(s,old);
  if got<>expected then
    Error("PENT159N_V9: replacement count drift ",label,
      " expected=",expected," observed=",got);
  fi;
  return ReplacedString(s,old,new);
end;

P159V9CheckedWriteText := function(path,payload,label)
  local stream,readback;
  stream:=OutputTextFile(path,false);
  if stream=fail then Error("PENT159N_V9: cannot open ",label); fi;
  SetPrintFormattingStatus(stream,false);
  PrintTo(stream,payload);
  CloseStream(stream);
  readback:=StringFile(path);
  if readback=fail or readback<>payload or
     HexSHA256(readback)<>HexSHA256(payload) then
    Error("PENT159N_V9: closed-write/hash mismatch ",label);
  fi;
  return rec(bytes:=Length(readback),sha256:=HexSHA256(readback));
end;

P159V9V8Raw:=StringFile(P159V9V8Outer);
if P159V9V8Raw=fail or HexSHA256(P159V9V8Raw)<>P159V9V8OuterSha then
  Error("PENT159N_V9: frozen v8 outer source missing or SHA drift");
fi;

## Execute the frozen v7 outer generator only far enough to reproduce its
## authenticated generated wrapper.  Suppress its final Read so the invalid
## v7 receipt tail is never executed or promoted.
P159V9V7Raw:=StringFile(P159V9V7Outer);
if P159V9V7Raw=fail or HexSHA256(P159V9V7Raw)<>P159V9V7OuterSha then
  Error("PENT159N_V9: frozen v7 outer source missing or SHA drift");
fi;
P159V9Bootstrap:=P159V9V7Raw;
P159V9Bootstrap:=P159V9ReplaceExact(P159V9Bootstrap,
  Concatenation(
    "P159V7GeneratedWrapperPath :=\n",
    "  \"ci/out/d972_pent_interleave_canary_p2_wrapper_effective_v7.g\";"),
  Concatenation(
    "P159V7GeneratedWrapperPath :=\n",
    "  \"ci/out/d972_pent_interleave_canary_p2_v7_bootstrap_wrapper_v9.g\";"),
  1,"v7 bootstrap wrapper path");
P159V9Bootstrap:=P159V9ReplaceExact(P159V9Bootstrap,
  "PENT159N_P2_V7_WRAPPER_SOURCE_WRITTEN",
  "PENT159N_P2_V9_V7_BOOTSTRAP_WRAPPER_WRITTEN",1,
  "bootstrap marker isolation");
P159V9Bootstrap:=P159V9ReplaceExact(P159V9Bootstrap,
  "Read(P159V7GeneratedWrapperPath);",
  Concatenation(
    "Print(\"PENT159N_P2_V9_V7_BOOTSTRAP_COMPLETE sha256=\",",
    "P159V7GeneratedWrapperSha,\"\\n\");"),
  1,"suppress invalid v7 execution");
P159V9BootstrapWrite:=P159V9CheckedWriteText(P159V9BootstrapSourcePath,
  P159V9Bootstrap,"v7 bootstrap source");
Print("PENT159N_P2_V9_V7_BOOTSTRAP_SOURCE_WRITTEN path=",
  P159V9BootstrapSourcePath," bytes=",P159V9BootstrapWrite.bytes,
  " sha256=",P159V9BootstrapWrite.sha256,"\n");
Read(P159V9BootstrapSourcePath);

if not IsBound(P159V7GeneratedWrapper) or
   HexSHA256(P159V7GeneratedWrapper)<>P159V9V7GeneratedWrapperSha then
  Error("PENT159N_V9: frozen v7 generated-wrapper reconstruction drift");
fi;

## Version the authenticated v7 generated wrapper.  All replacements below
## are deterministic metadata/namespace changes except the separately marked
## exact one-token receipt repair.
P159V9GeneratedWrapper:=P159V7GeneratedWrapper;
P159V9GeneratedWrapper:=P159V9ReplaceExact(P159V9GeneratedWrapper,
  "P159V7","P159V9",171,"v7 wrapper symbol namespace");
P159V9GeneratedWrapper:=P159V9ReplaceExact(P159V9GeneratedWrapper,
  "PENT159N_V7","PENT159N_V9",15,"v7 diagnostic namespace");
P159V9GeneratedWrapper:=P159V9ReplaceExact(P159V9GeneratedWrapper,
  "PENT159N_P2_V7","PENT159N_P2_V9",2,"v9 semantic marker target");
P159V9GeneratedWrapper:=P159V9ReplaceExact(P159V9GeneratedWrapper,
  "search/d972_pent_interleave_canary_p2_v7.g",
  "search/d972_pent_interleave_canary_p2_v9.g",2,"v9 source path");
P159V9GeneratedWrapper:=P159V9ReplaceExact(P159V9GeneratedWrapper,
  "d972_pent_interleave_canary_p2_effective_v7.g",
  "d972_pent_interleave_canary_p2_effective_v9.g",1,
  "v9 effective source path");
P159V9GeneratedWrapper:=P159V9ReplaceExact(P159V9GeneratedWrapper,
  "d972_pent_interleave_canary_p2_receipt_v7_20260824.json",
  "d972_pent_interleave_canary_p2_receipt_v9_20260824.json",1,
  "v9 receipt path");
P159V9GeneratedWrapper:=P159V9ReplaceExact(P159V9GeneratedWrapper,
  "d972-pent-interleave-canary-p2/v7",
  "d972-pent-interleave-canary-p2/v9",1,"v9 receipt schema");
P159V9GeneratedWrapper:=P159V9ReplaceExact(P159V9GeneratedWrapper,
  "effective_v7_source","effective_v9_source",2,
  "v9 effective-source receipt field names");

P159V9ReceiptSyntaxPatchBlock:=Concatenation(
  "## V9: preserve the v8 identity repair and add the remaining exact field patch.\n",
  "P159V9Effective:=P159V9ReplaceExact(P159V9Effective,\n",
  "  \"      identity:\\\"gamma4(G) G^2 = G^2 because gamma2(G) <= G^2\\\",\",\n",
  "  \"      identity:=\\\"gamma4(G) G^2 = G^2 because gamma2(G) <= G^2\\\",\",\n",
  "  1,\"receipt original W2 identity assignment\");\n",
  "P159V9Effective:=P159V9ReplaceExact(P159V9Effective,\n",
  "  \"      PB4_quotient:\\\"(C2)^6\\\",\",\n",
  "  \"      PB4_quotient:=\\\"(C2)^6\\\",\",\n",
  "  1,\"receipt original W2 PB4 quotient assignment\");\n\n");
P159V9GeneratedWrapper:=P159V9ReplaceExact(P159V9GeneratedWrapper,
  "## Rename every semantic marker last, including the newly inserted control",
  Concatenation(P159V9ReceiptSyntaxPatchBlock,
    "## Rename every semantic marker last, including the newly inserted control"),
  1,"insert exact receipt syntax repair");

P159V9GeneratedWrapperSha:=HexSHA256(P159V9GeneratedWrapper);
if P159V9GeneratedWrapperSha<>P159V9ExpectedGeneratedWrapperSha then
  Error("PENT159N_V9: generated-wrapper SHA drift ",
    P159V9GeneratedWrapperSha);
fi;
P159V9GeneratedWrapperWrite:=P159V9CheckedWriteText(
  P159V9GeneratedWrapperPath,P159V9GeneratedWrapper,"v9 generated wrapper");
Print("PENT159N_P2_V9_WRAPPER_SOURCE_WRITTEN path=",
  P159V9GeneratedWrapperPath," bytes=",P159V9GeneratedWrapperWrite.bytes,
  " sha256=",P159V9GeneratedWrapperWrite.sha256,
  " v7_generated_wrapper_sha256=",P159V9V7GeneratedWrapperSha,
  " receipt_syntax_patch_count=2\n");
Read(P159V9GeneratedWrapperPath);

## A nested Read containing a GAP syntax diagnostic can return to its caller
## without making the workflow process fail.  Require the closed receipt state
## after Read, so the v7 masked-success mode cannot recur unnoticed.
if not IsBoundGlobal("P159V5Write") or
   not IsBoundGlobal("P159V5Receipt") or
   not IsBoundGlobal("P159V5Output") then
  Error("PENT159N_V9: effective source returned without closed receipt state");
fi;
P159V9ReceiptWriteState:=ValueGlobal("P159V5Write");
P159V9ReceiptState:=ValueGlobal("P159V5Receipt");
P159V9ReceiptOutputState:=ValueGlobal("P159V5Output");
if not IsRecord(P159V9ReceiptWriteState) or
   not IsRecord(P159V9ReceiptState) or
   P159V9ReceiptOutputState<>P159V9ExpectedReceiptPath then
  Error("PENT159N_V9: effective source returned invalid receipt state");
fi;
P159V9ReceiptReadback:=StringFile(P159V9ExpectedReceiptPath);
if P159V9ReceiptReadback=fail or
   Length(P159V9ReceiptReadback)<>P159V9ReceiptWriteState.bytes or
   HexSHA256(P159V9ReceiptReadback)<>P159V9ReceiptWriteState.sha256 then
  Error("PENT159N_V9: outer receipt readback/hash gate failed");
fi;
Print("PENT159N_P2_V9_OUTER_FINAL_PASS receipt_path=",
  P159V9ExpectedReceiptPath," bytes=",P159V9ReceiptWriteState.bytes,
  " sha256=",P159V9ReceiptWriteState.sha256," terminal=",
  P159V9ReceiptState.terminal_token,"\n");
