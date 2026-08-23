#############################################################################
## D972 p=2 literal-A.18 source-relator gate overlay v11.
##
## Read only after the frozen PB3/PB4 presentations have been built and before
## any finite quotient or census.  Printed A.18 words are paper products; this
## overlay performs their unique repository-native serialization exactly once.
#############################################################################

if not IsBoundGlobal("P159P2V11P3Pres") or
   not IsBoundGlobal("P159P2V11P4Pres") or
   not IsBoundGlobal("P159P2V11Cofaces") then
  Error("PENT159N_P2_V11_A18: source presentations/functions absent");
fi;
if P159P2V11P3Pres.relation_count<>2 or
   P159P2V11P4Pres.relation_count<>11 then
  Error("PENT159N_P2_V11_A18: frozen source relation counts drift");
fi;

P159P2V11A18SlotNames:=["phi234","phi12_3_4","phi1_23_4",
  "phi1_2_34","phi123"];
P159P2V11A18ExpectedPaperWords:=[
  [[4],[5],[6]],
  [[2,4],[3,5],[6]],
  [[1,2],[3],[5,6]],
  [[1],[2,3],[4,5]],
  [[1],[2],[4]]
];
P159P2V11A18PaperWords:=P159P2V11Cofaces(3);
if P159P2V11A18PaperWords<>P159P2V11A18ExpectedPaperWords then
  Error("PENT159N_P2_V11_A18: printed A.18 paper table drift");
fi;

## Repository bridge: paper g1*...*gk is native gk*...*g1.  Signs are
## preserved; this is word-order serialization, not group inversion.
P159P2V11A18SerializePaperWordToNative := w -> Reversed(w);
P159P2V11A18NativeWords:=List(P159P2V11A18PaperWords,
  m->List(m,P159P2V11A18SerializePaperWordToNative));
P159P2V11A18ExpectedNativeWords:=[
  [[4],[5],[6]],
  [[4,2],[5,3],[6]],
  [[2,1],[3],[6,5]],
  [[1],[3,2],[5,4]],
  [[1],[2],[4]]
];
if P159P2V11A18NativeWords<>P159P2V11A18ExpectedNativeWords then
  Error("PENT159N_P2_V11_A18: unique native serialization drift");
fi;

P159P2V11A18IdentityArtinImages:=List([1..4],i->[i]);
P159P2V11A18LiteralRelatorGateRows:=[];
P159P2V11Phase("LITERAL_A18_SOURCE_RELATOR_GATE_BEFORE_CENSUS");
for P159P2V11A18SlotIndex in [1..5] do
  for P159P2V11A18RelatorIndex in [1..2] do
    P159P2V11A18MappedWord:=P159P2V11SubWord(
      P159P2V11P3Pres.relations[P159P2V11A18RelatorIndex],
      P159P2V11A18NativeWords[P159P2V11A18SlotIndex]);
    P159P2V11A18ArtinImages:=P159P2V11ArtinImages(4,
      P159P2V11ExpandPure(4,P159P2V11A18MappedWord));
    P159P2V11A18Passed:=
      P159P2V11A18ArtinImages=P159P2V11A18IdentityArtinImages;
    Add(P159P2V11A18LiteralRelatorGateRows,rec(
      slot_index_zero_based:=P159P2V11A18SlotIndex-1,
      slot_name:=P159P2V11A18SlotNames[P159P2V11A18SlotIndex],
      source_relator_index:=P159P2V11A18RelatorIndex,
      source_relator_word:=P159P2V11P3Pres.relations[
        P159P2V11A18RelatorIndex],
      mapped_native_pure_word:=P159P2V11A18MappedWord,
      artin_image_digest:=P159P2V11Digest(P159P2V11A18ArtinImages),
      artin_image_word_lengths:=List(P159P2V11A18ArtinImages,Length),
      passed:=P159P2V11A18Passed));
    if not P159P2V11A18Passed then
      Error("PENT159N_P2_V11_A18: literal coface failed source relator slot=",
        P159P2V11A18SlotIndex-1," relator=",P159P2V11A18RelatorIndex);
    fi;
  od;
od;
if Length(P159P2V11A18LiteralRelatorGateRows)<>10 or
   ForAny(P159P2V11A18LiteralRelatorGateRows,r->r.passed<>true) then
  Error("PENT159N_P2_V11_A18: incomplete literal per-coface relator gate");
fi;

## Destructive control: the former count-fitting implementation consumed the
## printed word lists directly as native lists.  It is never accepted as A.18.
P159P2V11A18ReversalMutantRelatorRows:=[];
for P159P2V11A18SlotIndex in [1..5] do
  for P159P2V11A18RelatorIndex in [1..2] do
    P159P2V11A18MappedWord:=P159P2V11SubWord(
      P159P2V11P3Pres.relations[P159P2V11A18RelatorIndex],
      P159P2V11A18PaperWords[P159P2V11A18SlotIndex]);
    P159P2V11A18ArtinImages:=P159P2V11ArtinImages(4,
      P159P2V11ExpandPure(4,P159P2V11A18MappedWord));
    P159P2V11A18Passed:=
      P159P2V11A18ArtinImages=P159P2V11A18IdentityArtinImages;
    Add(P159P2V11A18ReversalMutantRelatorRows,rec(
      slot_index_zero_based:=P159P2V11A18SlotIndex-1,
      slot_name:=P159P2V11A18SlotNames[P159P2V11A18SlotIndex],
      source_relator_index:=P159P2V11A18RelatorIndex,
      mapped_native_pure_word:=P159P2V11A18MappedWord,
      artin_image_digest:=P159P2V11Digest(P159P2V11A18ArtinImages),
      artin_image_word_lengths:=List(P159P2V11A18ArtinImages,Length),
      passed:=P159P2V11A18Passed));
  od;
od;
P159P2V11A18RequiredMutantFailure:=Filtered(
  P159P2V11A18ReversalMutantRelatorRows,
  r->r.slot_index_zero_based=1 and r.source_relator_index=1);
if Length(P159P2V11A18RequiredMutantFailure)<>1 or
   P159P2V11A18RequiredMutantFailure[1].passed<>false then
  Error("PENT159N_P2_V11_A18: reversal mutant was not rejected at phi12_3_4 relator 1");
fi;

P159P2V11A18GateReceipt:=rec(
  source:="Dolgushev et al. Appendix A.18, PDF page 49 image audit",
  gate_phase:="after frozen source presentations and before Q2/Q3/Q4 construction or any census",
  paper_to_native_rule:="reverse factor order once; preserve signed letters; do not invert",
  slot_names:=P159P2V11A18SlotNames,
  printed_paper_words:=P159P2V11A18PaperWords,
  printed_paper_words_sha256:=P159P2V11Digest(P159P2V11A18PaperWords),
  serialized_native_words:=P159P2V11A18NativeWords,
  serialized_native_words_sha256:=P159P2V11Digest(P159P2V11A18NativeWords),
  literal_relator_gate_row_count:=Length(
    P159P2V11A18LiteralRelatorGateRows),
  literal_relator_gate_rows:=P159P2V11A18LiteralRelatorGateRows,
  literal_all_relators_preserved:=true,
  reversal_mutant_accepted_as_coface:=false,
  reversal_mutant_rows:=P159P2V11A18ReversalMutantRelatorRows,
  required_reversal_mutant_failure:=P159P2V11A18RequiredMutantFailure[1]);
Print("PENT159N_P2_V11_LITERAL_A18_SOURCE_RELATORS_PASS cofaces=5 relators_per_coface=2 rows=10 paper_sha256=",
  P159P2V11A18GateReceipt.printed_paper_words_sha256,
  " native_sha256=",P159P2V11A18GateReceipt.serialized_native_words_sha256,
  " reversal_mutant_phi12_3_4_relator1_rejected=true runtime_ms=",Runtime(),"\n");
