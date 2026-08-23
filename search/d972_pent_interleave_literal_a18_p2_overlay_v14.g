#############################################################################
## D972 p=2 literal-A.18 identity-serialization repair overlay v14.
##
## Internal V12 names are retained so this versioned overlay can be injected
## into the frozen v13 derivation without changing any mathematical universe.
## Formula (A.18), paper PDF page 49, gives group products in their literal
## written order.  The Paper() reversal remains solely the Dpap outer-factor
## bridge and is not applied to images of PB3 generators.
#############################################################################

if not IsBoundGlobal("P159P2V12P3Pres") or
   not IsBoundGlobal("P159P2V12P4Pres") or
   not IsBoundGlobal("P159P2V12Cofaces") then
  Error("PENT159N_P2_V14_A18: source presentations/functions absent");
fi;
if P159P2V12P3Pres.relation_count<>2 or
   P159P2V12P4Pres.relation_count<>11 then
  Error("PENT159N_P2_V14_A18: frozen source relation counts drift");
fi;
if P159P2V12P3Pres.relations<>[
    [-1,2,1,2,3,-2,-3,-2],[-1,3,1,2,-3,-2]] then
  Error("PENT159N_P2_V14_A18: PB3 source-relator word pin drift");
fi;

P159P2V12A18SlotNames:=["phi234","phi12_3_4","phi1_23_4",
  "phi1_2_34","phi123"];
P159P2V12A18ExpectedPaperWords:=[
  [[4],[5],[6]],
  [[2,4],[3,5],[6]],
  [[1,2],[3],[5,6]],
  [[1],[2,3],[4,5]],
  [[1],[2],[4]]
];
P159P2V12A18PaperWords:=P159P2V12Cofaces(3);
if P159P2V12A18PaperWords<>P159P2V12A18ExpectedPaperWords then
  Error("PENT159N_P2_V14_A18: printed page-49 A.18 table drift");
fi;

## A.18 is a list of group-homomorphism values.  Native group multiplication
## consumes each displayed product in exactly that order.  There is no Paper()
## call and no factor reversal at this bridge.
P159P2V12A18NativeWords:=List(P159P2V12A18PaperWords,
  row->List(row,ShallowCopy));
P159P2V12A18ExpectedNativeWords:=P159P2V12A18ExpectedPaperWords;
if P159P2V12A18NativeWords<>P159P2V12A18ExpectedNativeWords then
  Error("PENT159N_P2_V14_A18: literal native identity serialization drift");
fi;

## Superseded conversion, destructive mutant only.
P159P2V12A18OldReversalWords:=List(P159P2V12A18PaperWords,
  row->List(row,Reversed));
P159P2V12A18ExpectedOldReversalWords:=[
  [[4],[5],[6]],
  [[4,2],[5,3],[6]],
  [[2,1],[3],[6,5]],
  [[1],[3,2],[5,4]],
  [[1],[2],[4]]
];
if P159P2V12A18OldReversalWords<>
   P159P2V12A18ExpectedOldReversalWords then
  Error("PENT159N_P2_V14_A18: old reversal-mutant table drift");
fi;

## Exact phi12_3_4 / relator-1 word bridge, pinned before either canary.
P159P2V12A18LiteralPhi12Rel1:=P159P2V12SubWord(
  P159P2V12P3Pres.relations[1],P159P2V12A18NativeWords[2]);
P159P2V12A18OldReversalPhi12Rel1:=P159P2V12SubWord(
  P159P2V12P3Pres.relations[1],P159P2V12A18OldReversalWords[2]);
if P159P2V12A18LiteralPhi12Rel1<>
     [-4,-2,3,5,2,4,3,5,6,-5,-3,-6,-5,-3] or
   P159P2V12A18OldReversalPhi12Rel1<>
     [-2,-4,5,3,4,2,5,3,6,-3,-5,-6,-3,-5] then
  Error("PENT159N_P2_V14_A18: explicit phi12_3_4 relator-1 image drift");
fi;

#############################################################################
## Independent bounded canary: finite evaluation of the faithful Artin action.
#############################################################################

P159P2V12A18ArtinTupleAction := function(inputTuple,braidWord)
  local tuple,letter,index,a,b;
  tuple:=ShallowCopy(inputTuple);
  for letter in braidWord do
    index:=AbsInt(letter); a:=tuple[index]; b:=tuple[index+1];
    if letter>0 then
      tuple[index]:=a*b*a^-1; tuple[index+1]:=a;
    else
      tuple[index]:=b; tuple[index+1]:=b^-1*a*b;
    fi;
  od;
  return tuple;
end;

P159P2V12A18PermutationImages := tuple ->
  List(tuple,g->List([1..4],i->i^g));

P159P2V12A18ArtinCanaryGroup:=SymmetricGroup(4);
P159P2V12A18ArtinCanaryInput:=[(1,3),(1,3,2,4),(1,2),(1,4,3)];
P159P2V12A18ArtinLiteralRows:=[];
P159P2V12A18ArtinMutantRows:=[];
for P159P2V12A18SlotIndex in [1..5] do
  for P159P2V12A18RelatorIndex in [1..2] do
    P159P2V12A18PureImage:=P159P2V12SubWord(
      P159P2V12P3Pres.relations[P159P2V12A18RelatorIndex],
      P159P2V12A18NativeWords[P159P2V12A18SlotIndex]);
    P159P2V12A18BraidImage:=P159P2V12ExpandPure(4,
      P159P2V12A18PureImage);
    P159P2V12A18ArtinOutput:=P159P2V12A18ArtinTupleAction(
      P159P2V12A18ArtinCanaryInput,P159P2V12A18BraidImage);
    Add(P159P2V12A18ArtinLiteralRows,rec(
      slot_index_zero_based:=P159P2V12A18SlotIndex-1,
      slot_name:=P159P2V12A18SlotNames[P159P2V12A18SlotIndex],
      source_relator_index:=P159P2V12A18RelatorIndex,
      source_relator_word:=P159P2V12P3Pres.relations[
        P159P2V12A18RelatorIndex],
      image_pure_word:=P159P2V12A18PureImage,
      image_braid_word:=P159P2V12A18BraidImage,
      output_tuple_images:=P159P2V12A18PermutationImages(
        P159P2V12A18ArtinOutput),
      passed:=P159P2V12A18ArtinOutput=P159P2V12A18ArtinCanaryInput));

    P159P2V12A18PureImage:=P159P2V12SubWord(
      P159P2V12P3Pres.relations[P159P2V12A18RelatorIndex],
      P159P2V12A18OldReversalWords[P159P2V12A18SlotIndex]);
    P159P2V12A18BraidImage:=P159P2V12ExpandPure(4,
      P159P2V12A18PureImage);
    P159P2V12A18ArtinOutput:=P159P2V12A18ArtinTupleAction(
      P159P2V12A18ArtinCanaryInput,P159P2V12A18BraidImage);
    Add(P159P2V12A18ArtinMutantRows,rec(
      slot_index_zero_based:=P159P2V12A18SlotIndex-1,
      slot_name:=P159P2V12A18SlotNames[P159P2V12A18SlotIndex],
      source_relator_index:=P159P2V12A18RelatorIndex,
      image_pure_word:=P159P2V12A18PureImage,
      image_braid_word:=P159P2V12A18BraidImage,
      output_tuple_images:=P159P2V12A18PermutationImages(
        P159P2V12A18ArtinOutput),
      passed:=P159P2V12A18ArtinOutput=P159P2V12A18ArtinCanaryInput));
  od;
od;
P159P2V12A18ArtinRequiredFailure:=Filtered(
  P159P2V12A18ArtinMutantRows,
  r->r.slot_index_zero_based=1 and r.source_relator_index=1);
if Length(P159P2V12A18ArtinLiteralRows)<>10 or
   ForAny(P159P2V12A18ArtinLiteralRows,r->r.passed<>true) or
   Length(P159P2V12A18ArtinRequiredFailure)<>1 or
   P159P2V12A18ArtinRequiredFailure[1].passed<>false then
  Error("PENT159N_P2_V14_A18: bounded faithful-Artin finite canary failed");
fi;
P159P2V12A18ArtinCanaryReceipt:=rec(
  model:="bounded S4 evaluation of the faithful Artin B4 action on F4 generators",
  finite_canary_not_standalone_proof:=true,
  group:="S4",input_tuple_images:=P159P2V12A18PermutationImages(
    P159P2V12A18ArtinCanaryInput),
  literal_rows:=P159P2V12A18ArtinLiteralRows,
  literal_row_count:=Length(P159P2V12A18ArtinLiteralRows),
  literal_all_identity:=true,
  old_reversal_mutant_rows:=P159P2V12A18ArtinMutantRows,
  required_old_reversal_failure:=P159P2V12A18ArtinRequiredFailure[1]);
Print("PENT159N_P2_V14_LITERAL_A18_ARTIN_FINITE_CANARY_PASS literal_rows=10 old_reversal_phi12_3_4_relator1_rejected=true input_sha256=",
  P159P2V12Digest(P159P2V12A18ArtinCanaryReceipt.input_tuple_images),"\n");

#############################################################################
## Authoritative producer finite gate in marked Q4=D4_2(PB4).
#############################################################################

P159P2V12A18RunFiniteRelatorGate := function(targetRec,targetPc)
  local literalRows,mutantRows,slotIndex,relatorIndex,images,value,coords,
    passed,requiredFailure,receipt;
  if not IsRecord(targetRec) or targetRec.name<>"Q4_PB4_D4_2" or
     Length(targetRec.marks)<>6 then
    Error("PENT159N_P2_V14_A18: finite gate target is not marked Q4 D4_2");
  fi;
  P159P2V12Phase("LITERAL_A18_SOURCE_RELATOR_GATE_BEFORE_CENSUS");
  literalRows:=[];
  for slotIndex in [1..5] do
    images:=List(P159P2V12A18NativeWords[slotIndex],
      w->P159P2V12NativeWordEval(w,targetRec.marks));
    for relatorIndex in [1..2] do
      value:=P159P2V12NativeWordEval(
        P159P2V12P3Pres.relations[relatorIndex],images);
      coords:=P159P2V12Coords(targetPc,value);
      passed:=value=One(targetRec.group);
      Add(literalRows,rec(slot_index_zero_based:=slotIndex-1,
        slot_name:=P159P2V12A18SlotNames[slotIndex],
        source_relator_index:=relatorIndex,
        source_relator_word:=P159P2V12P3Pres.relations[relatorIndex],
        coface_generator_image_words:=P159P2V12A18NativeWords[slotIndex],
        image_coords:=coords,image_coordinate_digest:=P159P2V12Digest(coords),
        passed:=passed));
      if not passed then
        Error("PENT159N_P2_V14_A18: literal coface failed finite source relator slot=",
          slotIndex-1," relator=",relatorIndex);
      fi;
    od;
  od;
  if Length(literalRows)<>10 or ForAny(literalRows,r->r.passed<>true) then
    Error("PENT159N_P2_V14_A18: incomplete literal finite relator gate");
  fi;

  mutantRows:=[];
  for slotIndex in [1..5] do
    images:=List(P159P2V12A18OldReversalWords[slotIndex],
      w->P159P2V12NativeWordEval(w,targetRec.marks));
    for relatorIndex in [1..2] do
      value:=P159P2V12NativeWordEval(
        P159P2V12P3Pres.relations[relatorIndex],images);
      coords:=P159P2V12Coords(targetPc,value);
      passed:=value=One(targetRec.group);
      Add(mutantRows,rec(slot_index_zero_based:=slotIndex-1,
        slot_name:=P159P2V12A18SlotNames[slotIndex],
        source_relator_index:=relatorIndex,
        coface_generator_image_words:=P159P2V12A18OldReversalWords[slotIndex],
        image_coords:=coords,image_coordinate_digest:=P159P2V12Digest(coords),
        passed:=passed));
    od;
  od;
  requiredFailure:=Filtered(mutantRows,
    r->r.slot_index_zero_based=1 and r.source_relator_index=1);
  if Length(requiredFailure)<>1 or requiredFailure[1].passed<>false then
    Error("PENT159N_P2_V14_A18: old reversal mutant was not rejected at phi12_3_4 relator 1");
  fi;
  receipt:=rec(
    source:="Dolgushev et al. Appendix A.18, original PDF page 49 image audit",
    gate_phase:="after marked Q4 construction and before marked maps or any Q2 census",
    target_quotient:=targetRec.name,
    a18_paper_to_native_rule:="identity: consume each displayed group product in literal written order",
    Dpap_outer_factor_bridge_separate:=true,
    slot_names:=P159P2V12A18SlotNames,
    printed_paper_words:=P159P2V12A18PaperWords,
    printed_paper_words_sha256:=P159P2V12Digest(P159P2V12A18PaperWords),
    serialized_native_words:=P159P2V12A18NativeWords,
    serialized_native_words_sha256:=P159P2V12Digest(P159P2V12A18NativeWords),
    old_reversal_mutant_words:=P159P2V12A18OldReversalWords,
    old_reversal_mutant_words_sha256:=P159P2V12Digest(
      P159P2V12A18OldReversalWords),
    explicit_phi12_3_4_relator1_literal_image:=P159P2V12A18LiteralPhi12Rel1,
    explicit_phi12_3_4_relator1_old_reversal_image:=
      P159P2V12A18OldReversalPhi12Rel1,
    artin_finite_canary:=P159P2V12A18ArtinCanaryReceipt,
    literal_relator_gate_row_count:=Length(literalRows),
    literal_relator_gate_rows:=literalRows,
    literal_all_relators_preserved:=true,
    old_reversal_mutant_accepted_as_coface:=false,
    reversal_mutant_accepted_as_coface:=false,
    old_reversal_mutant_rows:=mutantRows,
    reversal_mutant_rows:=mutantRows,
    required_old_reversal_mutant_failure:=requiredFailure[1],
    required_reversal_mutant_failure:=requiredFailure[1]);
  Print("PENT159N_P2_V14_LITERAL_A18_SOURCE_RELATORS_PASS cofaces=5 relators_per_coface=2 rows=10 target=Q4_D4_2 literal_order=true old_reversal_phi12_3_4_relator1_rejected=true runtime_ms=",
    Runtime(),"\n");
  return receipt;
end;

Print("PENT159N_P2_V14_LITERAL_A18_TABLE_PIN_PASS paper_page=49 a18_native_serialization=identity old_reversal_mutant_only=true paper_sha256=",
  P159P2V12Digest(P159P2V12A18PaperWords)," native_sha256=",
  P159P2V12Digest(P159P2V12A18NativeWords)," finite_gate_pending=true\n");
