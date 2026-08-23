#############################################################################
## D972 p=2 literal-A.18 finite source-relator gate overlay v12.
##
## Read after the frozen PB3/PB4 presentations.  It pins the printed table and
## defines a p-specific Q4 source-relator gate.  The caller must execute that
## gate after Q4 exists and before any marked-map or element census.
#############################################################################

if not IsBoundGlobal("P159P2V12P3Pres") or
   not IsBoundGlobal("P159P2V12P4Pres") or
   not IsBoundGlobal("P159P2V12Cofaces") then
  Error("PENT159N_P2_V12_A18: source presentations/functions absent");
fi;
if P159P2V12P3Pres.relation_count<>2 or
   P159P2V12P4Pres.relation_count<>11 then
  Error("PENT159N_P2_V12_A18: frozen source relation counts drift");
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
  Error("PENT159N_P2_V12_A18: printed A.18 paper table drift");
fi;

## Repository bridge: paper g1*...*gk is native gk*...*g1.  Signs are
## preserved; this is word-order serialization, not group inversion.
P159P2V12A18SerializePaperWordToNative := w -> Reversed(w);
P159P2V12A18NativeWords:=List(P159P2V12A18PaperWords,
  m->List(m,P159P2V12A18SerializePaperWordToNative));
P159P2V12A18ExpectedNativeWords:=[
  [[4],[5],[6]],
  [[4,2],[5,3],[6]],
  [[2,1],[3],[6,5]],
  [[1],[3,2],[5,4]],
  [[1],[2],[4]]
];
if P159P2V12A18NativeWords<>P159P2V12A18ExpectedNativeWords then
  Error("PENT159N_P2_V12_A18: unique native serialization drift");
fi;

P159P2V12A18RunFiniteRelatorGate := function(targetRec,targetPc)
  local literalRows,mutantRows,slotIndex,relatorIndex,images,value,coords,
    passed,requiredFailure,receipt;
  if not IsRecord(targetRec) or targetRec.name<>"Q4_PB4_D4_2" or
     Length(targetRec.marks)<>6 then
    Error("PENT159N_P2_V12_A18: finite gate target is not marked Q4 D4_2");
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
        image_coords:=coords,image_coordinate_digest:=P159P2V12Digest(coords),
        passed:=passed));
      if not passed then
        Error("PENT159N_P2_V12_A18: literal coface failed finite source relator slot=",
          slotIndex-1," relator=",relatorIndex);
      fi;
    od;
  od;
  if Length(literalRows)<>10 or ForAny(literalRows,r->r.passed<>true) then
    Error("PENT159N_P2_V12_A18: incomplete literal finite relator gate");
  fi;

  ## Destructive control: consume printed paper words directly as native words.
  mutantRows:=[];
  for slotIndex in [1..5] do
    images:=List(P159P2V12A18PaperWords[slotIndex],
      w->P159P2V12NativeWordEval(w,targetRec.marks));
    for relatorIndex in [1..2] do
      value:=P159P2V12NativeWordEval(
        P159P2V12P3Pres.relations[relatorIndex],images);
      coords:=P159P2V12Coords(targetPc,value);
      passed:=value=One(targetRec.group);
      Add(mutantRows,rec(slot_index_zero_based:=slotIndex-1,
        slot_name:=P159P2V12A18SlotNames[slotIndex],
        source_relator_index:=relatorIndex,image_coords:=coords,
        image_coordinate_digest:=P159P2V12Digest(coords),passed:=passed));
    od;
  od;
  requiredFailure:=Filtered(mutantRows,
    r->r.slot_index_zero_based=1 and r.source_relator_index=1);
  if Length(requiredFailure)<>1 or requiredFailure[1].passed<>false then
    Error("PENT159N_P2_V12_A18: p2 reversal mutant was not rejected at phi12_3_4 relator 1");
  fi;
  receipt:=rec(
    source:="Dolgushev et al. Appendix A.18, PDF page 49 image audit",
    gate_phase:="after marked Q4 construction and before marked maps or any Q2 census",
    target_quotient:=targetRec.name,
    paper_to_native_rule:="reverse factor order once; preserve signed letters; do not invert",
    slot_names:=P159P2V12A18SlotNames,
    printed_paper_words:=P159P2V12A18PaperWords,
    printed_paper_words_sha256:=P159P2V12Digest(P159P2V12A18PaperWords),
    serialized_native_words:=P159P2V12A18NativeWords,
    serialized_native_words_sha256:=P159P2V12Digest(P159P2V12A18NativeWords),
    literal_relator_gate_row_count:=Length(literalRows),
    literal_relator_gate_rows:=literalRows,
    literal_all_relators_preserved:=true,
    reversal_mutant_accepted_as_coface:=false,
    reversal_mutant_rows:=mutantRows,
    required_reversal_mutant_failure:=requiredFailure[1]);
  Print("PENT159N_P2_V12_LITERAL_A18_SOURCE_RELATORS_PASS cofaces=5 relators_per_coface=2 rows=10 target=Q4_D4_2 paper_sha256=",
    receipt.printed_paper_words_sha256," native_sha256=",
    receipt.serialized_native_words_sha256,
    " reversal_mutant_phi12_3_4_relator1_rejected=true runtime_ms=",Runtime(),"\n");
  return receipt;
end;

Print("PENT159N_P2_V12_LITERAL_A18_TABLE_PIN_PASS paper_sha256=",
  P159P2V12Digest(P159P2V12A18PaperWords)," native_sha256=",
  P159P2V12Digest(P159P2V12A18NativeWords)," finite_gate_pending=true\n");
