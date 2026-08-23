#############################################################################
## D972 corrected pentagon-interleave canary, finite p=2 stage v7.
##
## Versioned repair after v6 run 32649385042.  V6 passed the quotients, maps,
## independent order control, and complete commutator instrument (8 rows, 4
## nonzero).  It then exposed a convention error in the PB3 full twist.  This
## wrapper authenticates the frozen v6 wrapper and adds an exact Artin/A.5
## central-word repair without overwriting v5 or v6.
#############################################################################

P159V7OuterSource := "search/d972_pent_interleave_canary_p2_v7.g";
P159V7V6Wrapper := "search/d972_pent_interleave_canary_p2_v6.g";
P159V7V6WrapperSha :=
  "5806069bbacfff91e5abae1b4adaac1670967507a879bf8761cbbea41d49bb43";
P159V7GeneratedWrapperPath :=
  "ci/out/d972_pent_interleave_canary_p2_wrapper_effective_v7.g";
P159V7ExpectedMathEffectiveSha :=
  "a950d60f5bd456582e18dd5db59db5375d64ea371852d31e0de4ca8eb75f3072";
P159V7ExpectedGeneratedWrapperSha :=
  "fc4fc99605ae135cefd52cb59f81aed2dc9d0dec4761fbdad9865fd77005bc14";

P159V7CountSublist := function(s,needle)
  local count,pos,tail,offset,rel;
  if Length(needle)=0 then Error("PENT159N_V7: empty replacement needle"); fi;
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

P159V7ReplaceExact := function(s,old,new,expected,label)
  local got;
  got:=P159V7CountSublist(s,old);
  if got<>expected then
    Error("PENT159N_V7: wrapper patch count drift ",label,
      " expected=",expected," observed=",got);
  fi;
  return ReplacedString(s,old,new);
end;

P159V7V6Raw:=StringFile(P159V7V6Wrapper);
if P159V7V6Raw=fail or HexSHA256(P159V7V6Raw)<>P159V7V6WrapperSha then
  Error("PENT159N_V7: frozen v6 wrapper missing or SHA drift");
fi;
P159V7GeneratedWrapper:=P159V7V6Raw;

## Version the v6 wrapper itself.  The resulting generated wrapper still
## authenticates the frozen v5 mathematical producer and applies all v6
## warning/order-control repairs before the new central-word patch below.
P159V7GeneratedWrapper:=P159V7ReplaceExact(P159V7GeneratedWrapper,
  "P159V6","P159V7",132,"v6 wrapper symbol namespace");
P159V7GeneratedWrapper:=P159V7ReplaceExact(P159V7GeneratedWrapper,
  "PENT159N_V6","PENT159N_V7",8,"v6 diagnostic namespace");
P159V7GeneratedWrapper:=P159V7ReplaceExact(P159V7GeneratedWrapper,
  "PENT159N_P2_V6","PENT159N_P2_V7",2,"v7 semantic marker target");
P159V7GeneratedWrapper:=P159V7ReplaceExact(P159V7GeneratedWrapper,
  "search/d972_pent_interleave_canary_p2_v6.g",
  "search/d972_pent_interleave_canary_p2_v7.g",2,"v7 source path");
P159V7GeneratedWrapper:=P159V7ReplaceExact(P159V7GeneratedWrapper,
  "d972_pent_interleave_canary_p2_effective_v6.g",
  "d972_pent_interleave_canary_p2_effective_v7.g",1,
  "v7 effective source path");
P159V7GeneratedWrapper:=P159V7ReplaceExact(P159V7GeneratedWrapper,
  "d972_pent_interleave_canary_p2_receipt_v6_20260824.json",
  "d972_pent_interleave_canary_p2_receipt_v7_20260824.json",1,
  "v7 receipt path");
P159V7GeneratedWrapper:=P159V7ReplaceExact(P159V7GeneratedWrapper,
  "d972-pent-interleave-canary-p2/v6",
  "d972-pent-interleave-canary-p2/v7",1,"v7 receipt schema");
P159V7GeneratedWrapper:=P159V7ReplaceExact(P159V7GeneratedWrapper,
  "effective_v6_source","effective_v7_source",2,
  "v7 effective-source receipt field names");

## This code is inserted into the generated wrapper.  It adds two exact,
## counted replacements to that wrapper's transformation of the frozen v5
## mathematical source.
P159V7CentralPatchBlock:=Concatenation(
  "## V7: audit the A.5 full twist in the faithful Artin/native model.\n",
  "P159V7Effective:=P159V7ReplaceExact(P159V7Effective,\n",
  "  Concatenation(\n",
  "    \"P159V5Q3c:=P159V5Paper([P159V5Q3.marks[1],P159V5Q3.marks[2],\\n\",\n",
  "    \"  P159V5Q3.marks[3]]);\\n\",\n",
  "    \"if ForAny(P159V5Q3.marks,g->Comm(P159V5Q3c,g)<>One(P159V5Q3.group)) then\\n\",\n",
  "    \"  Error(\\\"PENT159N_V5: PB3 full-twist marking is not central\\\");\\n\",\n",
  "    \"fi;\"),\n",
  "  Concatenation(\n",
  "    \"P159V7A5PureWords:=[[1,2,3],[2,3,1],[3,1,2]];\\n\",\n",
  "    \"P159V7A5BraidWords:=List(P159V7A5PureWords,w->\\n\",\n",
  "    \"  P159V5ExpandPure(3,w));\\n\",\n",
  "    \"P159V7A5ArtinImages:=List(P159V7A5BraidWords,w->\\n\",\n",
  "    \"  P159V5ArtinImages(3,w));\\n\",\n",
  "    \"if Length(Set(P159V7A5ArtinImages))<>1 then\\n\",\n",
  "    \"  Error(\\\"PENT159N_V7: cyclic A.5 native forms differ in Artin action\\\");\\n\",\n",
  "    \"fi;\\n\",\n",
  "    \"P159V7SigmaFullTwist:=[1,2,1,2,1,2];\\n\",\n",
  "    \"if P159V5ArtinImages(3,P159V7SigmaFullTwist)<>P159V7A5ArtinImages[1] then\\n\",\n",
  "    \"  Error(\\\"PENT159N_V7: A.5 forms differ from (sigma1 sigma2)^3\\\");\\n\",\n",
  "    \"fi;\\n\",\n",
  "    \"for P159V5i in [1..3] do\\n\",\n",
  "    \"  P159V7A5CommPure:=P159V5Reduce(Concatenation(\\n\",\n",
  "    \"    P159V5InvWord(P159V7A5PureWords[1]),[-P159V5i],\\n\",\n",
  "    \"    P159V7A5PureWords[1],[P159V5i]));\\n\",\n",
  "    \"  if not P159V5ArtinIdentity(3,P159V5ExpandPure(3,P159V7A5CommPure)) then\\n\",\n",
  "    \"    Error(\\\"PENT159N_V7: A.5 native word is not source-central\\\");\\n\",\n",
  "    \"  fi;\\n\",\n",
  "    \"od;\\n\",\n",
  "    \"P159V7A5Q3Values:=List(P159V7A5PureWords,w->\\n\",\n",
  "    \"  P159V5NativeWordEval(w,P159V5Q3.marks));\\n\",\n",
  "    \"if Length(Set(P159V7A5Q3Values))<>1 then\\n\",\n",
  "    \"  Error(\\\"PENT159N_V7: A.5 native quotient forms differ\\\");\\n\",\n",
  "    \"fi;\\n\",\n",
  "    \"P159V5Q3c:=P159V7A5Q3Values[1];\\n\",\n",
  "    \"for P159V5i in [1..Length(P159V5Q3.marks)] do\\n\",\n",
  "    \"  if Comm(P159V5Q3c,P159V5Q3.marks[P159V5i])<>One(P159V5Q3.group) then\\n\",\n",
  "    \"    Error(\\\"PENT159N_V7: pinned A.5 quotient element is not central\\\");\\n\",\n",
  "    \"  fi;\\n\",\n",
  "    \"od;\\n\",\n",
  "    \"P159V7RejectedReversedWords:=[[3,2,1],[2,1,3]];\\n\",\n",
  "    \"P159V7RejectedReversedCentralBits:=[];\\n\",\n",
  "    \"for P159V7RejectedReversedWord in P159V7RejectedReversedWords do\\n\",\n",
  "    \"  P159V7RejectedReversedValue:=P159V5NativeWordEval(\\n\",\n",
  "    \"    P159V7RejectedReversedWord,P159V5Q3.marks);\\n\",\n",
  "    \"  P159V7RejectedReversedCentral:=true;\\n\",\n",
  "    \"  for P159V5i in [1..Length(P159V5Q3.marks)] do\\n\",\n",
  "    \"    if Comm(P159V7RejectedReversedValue,P159V5Q3.marks[P159V5i])<>\\n\",\n",
  "    \"       One(P159V5Q3.group) then P159V7RejectedReversedCentral:=false; fi;\\n\",\n",
  "    \"  od;\\n\",\n",
  "    \"  Add(P159V7RejectedReversedCentralBits,P159V7RejectedReversedCentral);\\n\",\n",
  "    \"od;\\n\",\n",
  "    \"if true in P159V7RejectedReversedCentralBits then\\n\",\n",
  "    \"  Error(\\\"PENT159N_V7: a reversed paper/native mutant was not rejected\\\");\\n\",\n",
  "    \"fi;\\n\",\n",
  "    \"Print(\\\"PENT159N_P2_V5_A5_CENTRAL_PASS displayed_native_forms=2 cyclic_native_forms=3 artin_equal=true sigma_full_twist_equal=true quotient_equal=true central=true reversed_forms=2 reversed_central_all=false\\\\n\\\");\"),\n",
  "  1,\"A.5 native full-twist repair\");\n",
  "P159V7Effective:=P159V7ReplaceExact(P159V7Effective,\n",
  "  Concatenation(\n",
  "    \"    rejected_tau_native_mutant:=\\\"(X*Y)^-1\\\"),\\n\",\n",
  "    \"  quotients:=rec(Q2:=P159V5PublicPcReceipt(P159V5Q2Receipt),\"),\n",
  "  Concatenation(\n",
  "    \"    rejected_tau_native_mutant:=\\\"(X*Y)^-1\\\"),\\n\",\n",
  "    \"  pb3_full_twist_A5:=rec(\\n\",\n",
  "    \"    multiplication_convention:=\\\"faithful Artin/native, not global Paper reversal\\\",\\n\",\n",
  "    \"    displayed_A5_native_forms:=[[3,1,2],[1,2,3]],\\n\",\n",
  "    \"    native_cyclic_forms:=[[1,2,3],[2,3,1],[3,1,2]],\\n\",\n",
  "    \"    sigma_word:=[1,2,1,2,1,2],artin_images_equal:=true,\\n\",\n",
  "    \"    source_central:=true,quotient_forms_equal:=true,quotient_central:=true,\\n\",\n",
  "    \"    quotient_coords:=P159V5Coords(P159V5Q3Pc,P159V5Q3c),\\n\",\n",
  "    \"    quotient_order:=Int(Order(P159V5Q3c)),\\n\",\n",
  "    \"    rejected_global_paper_reversals:=[[3,2,1],[2,1,3]],\\n\",\n",
  "    \"    rejected_reversal_central_bits:=P159V7RejectedReversedCentralBits),\\n\",\n",
  "    \"  quotients:=rec(Q2:=P159V5PublicPcReceipt(P159V5Q2Receipt),\"),\n",
  "  1,\"A.5 receipt fields\");\n\n");

P159V7GeneratedWrapper:=P159V7ReplaceExact(P159V7GeneratedWrapper,
  "## Rename every semantic marker last, including the newly inserted control",
  Concatenation(P159V7CentralPatchBlock,
    "## Rename every semantic marker last, including the newly inserted control"),
  1,"insert A.5 repair before marker rename");
P159V7GeneratedWrapper:=P159V7ReplaceExact(P159V7GeneratedWrapper,
  "14,\"semantic marker version\"",
  "15,\"semantic marker version\"",1,"semantic marker count");
P159V7GeneratedWrapper:=P159V7ReplaceExact(P159V7GeneratedWrapper,
  "P159V7EffectiveSha:=HexSHA256(P159V7Effective);",
  Concatenation(
    "P159V7EffectiveSha:=HexSHA256(P159V7Effective);\n",
    "if P159V7EffectiveSha<>P159V7ExpectedMathEffectiveSha then\n",
    "  Error(\"PENT159N_V7: mathematical effective-source SHA drift \",",
    "P159V7EffectiveSha);\n",
    "fi;"),
  1,"mathematical effective-source SHA gate");

P159V7GeneratedWrapperSha:=HexSHA256(P159V7GeneratedWrapper);
if P159V7GeneratedWrapperSha<>P159V7ExpectedGeneratedWrapperSha then
  Error("PENT159N_V7: generated-wrapper SHA drift ",
    P159V7GeneratedWrapperSha);
fi;
P159V7GeneratedWrapperFile:=OutputTextFile(P159V7GeneratedWrapperPath,false);
if P159V7GeneratedWrapperFile=fail then
  Error("PENT159N_V7: cannot open generated wrapper path");
fi;
SetPrintFormattingStatus(P159V7GeneratedWrapperFile,false);
PrintTo(P159V7GeneratedWrapperFile,P159V7GeneratedWrapper);
CloseStream(P159V7GeneratedWrapperFile);
P159V7GeneratedWrapperReadback:=StringFile(P159V7GeneratedWrapperPath);
if P159V7GeneratedWrapperReadback=fail or
   P159V7GeneratedWrapperReadback<>P159V7GeneratedWrapper or
   HexSHA256(P159V7GeneratedWrapperReadback)<>P159V7GeneratedWrapperSha then
  Error("PENT159N_V7: generated wrapper closed-write/hash mismatch");
fi;
Print("PENT159N_P2_V7_WRAPPER_SOURCE_WRITTEN path=",
  P159V7GeneratedWrapperPath," bytes=",Length(P159V7GeneratedWrapper),
  " sha256=",P159V7GeneratedWrapperSha,
  " v6_wrapper_sha256=",P159V7V6WrapperSha,"\n");
Read(P159V7GeneratedWrapperPath);
