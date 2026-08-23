#############################################################################
## D972 p=3 literal-A.18 destructive-control aggregate overlay v5.
##
## Injected after the first repaired actual-coface witness and before receipt
## construction.  It scans every Q2 element using only the homomorphism-gated
## literal A.18 contexts.  The old section 9.1 ordering is mutant-only.
#############################################################################

if not IsBoundGlobal("P159P3V4Bfs") or
   not IsBoundGlobal("P159P3V4Contexts") or
   not IsBoundGlobal("P159P3V4Q4") or
   not IsBoundGlobal("P159P3V4Q4Pc") or
   not IsBoundGlobal("P159P3V4WrongOrderDiscriminator") or
   not IsBoundGlobal("P159P3V4A18GateReceipt") then
  Error("PENT159N_P3_V5_CONTROL: repaired authenticated producer state absent");
fi;
if P159P3V4A18GateReceipt.literal_all_relators_preserved<>true then
  Error("PENT159N_P3_V5_CONTROL: A.18 source-relator gate did not close");
fi;

P159P3V4WrongOrderFactorLabels:=["phi12_3_4^-1","phi1_2_34^-1",
  "phi234","phi1_23_4","phi123"];
P159P3V4WrongOrderFactorNoncommutingRowCount:=0;
P159P3V4WrongOrderActualCofaceRowCount:=0;
P159P3V4WrongOrderNoncommutingPairTotal:=0;
P159P3V4WrongOrderAggregateFirst:=fail;
Print("PENT159N_P3_V5_LITERAL_DPAP_FORMULA_PIN_PASS literal_paper=A^-1*B^-1*C*E*F literal_native=F*E*C*B^-1*A^-1 section_9_1_mutant_paper=F*E*C*B^-1*A^-1 section_9_1_mutant_native=A^-1*B^-1*C*E*F\n");

for P159P3V4ControlRow in P159P3V4Bfs do
  P159P3V4ControlDrec:=P159P3V4Dpap(P159P3V4ControlRow.word,
    P159P3V4Contexts);
  P159P3V4ControlFactors:=[P159P3V4ControlDrec.factor_values[2]^-1,
    P159P3V4ControlDrec.factor_values[4]^-1,
    P159P3V4ControlDrec.factor_values[1],
    P159P3V4ControlDrec.factor_values[3],
    P159P3V4ControlDrec.factor_values[5]];
  P159P3V4ControlNoncommutingPairs:=[];
  for P159P3V4ControlI in [1..4] do
    for P159P3V4ControlJ in [P159P3V4ControlI+1..5] do
      P159P3V4ControlComm:=Comm(
        P159P3V4ControlFactors[P159P3V4ControlI],
        P159P3V4ControlFactors[P159P3V4ControlJ]);
      if P159P3V4ControlComm<>One(P159P3V4Q4.group) then
        Add(P159P3V4ControlNoncommutingPairs,rec(
          positions:=[P159P3V4ControlI,P159P3V4ControlJ],
          labels:=[P159P3V4WrongOrderFactorLabels[P159P3V4ControlI],
            P159P3V4WrongOrderFactorLabels[P159P3V4ControlJ]],
          commutator_coords:=P159P3V4Coords(P159P3V4Q4Pc,
            P159P3V4ControlComm),noncommuting:=true));
      fi;
    od;
  od;
  P159P3V4WrongOrderNoncommutingPairTotal:=
    P159P3V4WrongOrderNoncommutingPairTotal+
      Length(P159P3V4ControlNoncommutingPairs);
  if Length(P159P3V4ControlNoncommutingPairs)>0 then
    P159P3V4WrongOrderFactorNoncommutingRowCount:=
      P159P3V4WrongOrderFactorNoncommutingRowCount+1;
  fi;
  if P159P3V4ControlDrec.correct<>
       P159P3V4ControlDrec.wrong_order_mutant and
     Length(P159P3V4ControlNoncommutingPairs)>0 then
    P159P3V4WrongOrderActualCofaceRowCount:=
      P159P3V4WrongOrderActualCofaceRowCount+1;
    if P159P3V4WrongOrderAggregateFirst=fail then
      P159P3V4WrongOrderAggregateFirst:=rec(
        source:="actual complete-Q2 literal-A.18 coface-derived Dpap row",
        f_coords:=P159P3V4ControlRow.coords,
        f_word:=P159P3V4ControlRow.word,
        factor_labels:=P159P3V4WrongOrderFactorLabels,
        factor_coords:=List(P159P3V4ControlFactors,
          g->P159P3V4Coords(P159P3V4Q4Pc,g)),
        noncommuting_factor_pairs:=P159P3V4ControlNoncommutingPairs,
        correct_coords:=P159P3V4Coords(P159P3V4Q4Pc,
          P159P3V4ControlDrec.correct),
        mutant_coords:=P159P3V4Coords(P159P3V4Q4Pc,
          P159P3V4ControlDrec.wrong_order_mutant),
        residual_commutator_coords:=P159P3V4Coords(P159P3V4Q4Pc,
          Comm(P159P3V4ControlDrec.correct,
            P159P3V4ControlDrec.wrong_order_mutant)),
        residuals_distinct:=true,actual_coface_Dpap_row:=true,
        literal_A18_homomorphism_gated:=true,
        relevant_factor_noncommutation:=true);
    fi;
  fi;
od;

if P159P3V4WrongOrderAggregateFirst=fail or
   P159P3V4WrongOrderActualCofaceRowCount=0 or
   P159P3V4WrongOrderFactorNoncommutingRowCount=0 or
   P159P3V4WrongOrderNoncommutingPairTotal=0 then
  Error("PENT159N_P3_V5_CONTROL: repaired actual-coface aggregate has no admissible same-row witness");
fi;
if P159P3V4WrongOrderDiscriminator=fail or
   P159P3V4WrongOrderDiscriminator.f_coords<>
     P159P3V4WrongOrderAggregateFirst.f_coords or
   P159P3V4WrongOrderDiscriminator.f_word<>
     P159P3V4WrongOrderAggregateFirst.f_word then
  Error("PENT159N_P3_V5_CONTROL: first-witness replay drift");
fi;
P159P3V4WrongOrderDiscriminator:=P159P3V4WrongOrderAggregateFirst;
Print("PENT159N_P3_V5_LITERAL_A18_WRONG_ORDER_AGGREGATE_PASS q2_universe=",
  Length(P159P3V4Bfs)," residual_distinct_rows=",
  P159P3V4CWrongOrderQ2DistinctCount," residual_noncommuting_rows=",
  P159P3V4CWrongOrderQ2NoncommutingCount,
  " factor_noncommuting_rows=",
  P159P3V4WrongOrderFactorNoncommutingRowCount,
  " actual_distinct_and_factor_noncommuting_rows=",
  P159P3V4WrongOrderActualCofaceRowCount,
  " factor_noncommuting_pair_total=",
  P159P3V4WrongOrderNoncommutingPairTotal,
  " first_f_word=",P159P3V4WrongOrderDiscriminator.f_word,
  " section_9_1_order_mutant_only=true external_S3_calibration_only=true\n");
