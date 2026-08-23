#############################################################################
## D972 p=3 destructive-control aggregate overlay v2.
##
## This producer-only overlay is injected into the authenticated p3 v1 base
## after its first actual-coface witness has been found and before receipt
## construction.  It independently scans every marked Q2 element, evaluates
## all five literal coface factors, and records the full aggregate required by
## the corrected p2/p3 wrong-factor-order contract.
#############################################################################

if not IsBoundGlobal("P159P3V2Bfs") or
   not IsBoundGlobal("P159P3V2Contexts") or
   not IsBoundGlobal("P159P3V2Q4") or
   not IsBoundGlobal("P159P3V2Q4Pc") or
   not IsBoundGlobal("P159P3V2WrongOrderDiscriminator") then
  Error("PENT159N_P3_V2_CONTROL: required authenticated producer state absent");
fi;

P159P3V2WrongOrderFactorLabels:=["phi12_3_4^-1","phi1_2_34^-1",
  "phi234","phi1_23_4","phi123"];
P159P3V2WrongOrderFactorNoncommutingRowCount:=0;
P159P3V2WrongOrderActualCofaceRowCount:=0;
P159P3V2WrongOrderNoncommutingPairTotal:=0;
P159P3V2WrongOrderAggregateFirst:=fail;
Print("PENT159N_P3_V2_WRONG_ORDER_FORMULA_PIN_PASS correct_paper=A^-1*B^-1*C*E*F correct_native=F*E*C*B^-1*A^-1 mutant_paper=F*E*C*B^-1*A^-1 mutant_native=A^-1*B^-1*C*E*F\n");

for P159P3V2ControlRow in P159P3V2Bfs do
  P159P3V2ControlDrec:=P159P3V2Dpap(P159P3V2ControlRow.word,
    P159P3V2Contexts);
  P159P3V2ControlFactors:=[P159P3V2ControlDrec.factor_values[2]^-1,
    P159P3V2ControlDrec.factor_values[4]^-1,
    P159P3V2ControlDrec.factor_values[1],
    P159P3V2ControlDrec.factor_values[3],
    P159P3V2ControlDrec.factor_values[5]];
  P159P3V2ControlNoncommutingPairs:=[];
  for P159P3V2ControlI in [1..4] do
    for P159P3V2ControlJ in [P159P3V2ControlI+1..5] do
      P159P3V2ControlComm:=Comm(
        P159P3V2ControlFactors[P159P3V2ControlI],
        P159P3V2ControlFactors[P159P3V2ControlJ]);
      if P159P3V2ControlComm<>One(P159P3V2Q4.group) then
        Add(P159P3V2ControlNoncommutingPairs,rec(
          positions:=[P159P3V2ControlI,P159P3V2ControlJ],
          labels:=[P159P3V2WrongOrderFactorLabels[P159P3V2ControlI],
            P159P3V2WrongOrderFactorLabels[P159P3V2ControlJ]],
          commutator_coords:=P159P3V2Coords(P159P3V2Q4Pc,
            P159P3V2ControlComm),noncommuting:=true));
      fi;
    od;
  od;
  P159P3V2WrongOrderNoncommutingPairTotal:=
    P159P3V2WrongOrderNoncommutingPairTotal+
      Length(P159P3V2ControlNoncommutingPairs);
  if Length(P159P3V2ControlNoncommutingPairs)>0 then
    P159P3V2WrongOrderFactorNoncommutingRowCount:=
      P159P3V2WrongOrderFactorNoncommutingRowCount+1;
  fi;
  if P159P3V2ControlDrec.correct<>
       P159P3V2ControlDrec.wrong_order_mutant and
     Length(P159P3V2ControlNoncommutingPairs)>0 then
    P159P3V2WrongOrderActualCofaceRowCount:=
      P159P3V2WrongOrderActualCofaceRowCount+1;
    if P159P3V2WrongOrderAggregateFirst=fail then
      P159P3V2WrongOrderAggregateFirst:=rec(
        source:="actual complete-Q2 coface-derived Dpap row",
        f_coords:=P159P3V2ControlRow.coords,
        f_word:=P159P3V2ControlRow.word,
        factor_labels:=P159P3V2WrongOrderFactorLabels,
        factor_coords:=List(P159P3V2ControlFactors,
          g->P159P3V2Coords(P159P3V2Q4Pc,g)),
        noncommuting_factor_pairs:=P159P3V2ControlNoncommutingPairs,
        correct_coords:=P159P3V2Coords(P159P3V2Q4Pc,
          P159P3V2ControlDrec.correct),
        mutant_coords:=P159P3V2Coords(P159P3V2Q4Pc,
          P159P3V2ControlDrec.wrong_order_mutant),
        residual_commutator_coords:=P159P3V2Coords(P159P3V2Q4Pc,
          Comm(P159P3V2ControlDrec.correct,
            P159P3V2ControlDrec.wrong_order_mutant)),
        residuals_distinct:=true,actual_coface_Dpap_row:=true,
        relevant_factor_noncommutation:=true);
    fi;
  fi;
od;

if P159P3V2WrongOrderAggregateFirst=fail or
   P159P3V2WrongOrderActualCofaceRowCount=0 or
   P159P3V2WrongOrderFactorNoncommutingRowCount=0 or
   P159P3V2WrongOrderNoncommutingPairTotal=0 then
  Error("PENT159N_P3_V2_CONTROL: complete actual-coface aggregate has no admissible same-row witness");
fi;
if P159P3V2WrongOrderDiscriminator=fail or
   P159P3V2WrongOrderDiscriminator.f_coords<>
     P159P3V2WrongOrderAggregateFirst.f_coords or
   P159P3V2WrongOrderDiscriminator.f_word<>
     P159P3V2WrongOrderAggregateFirst.f_word then
  Error("PENT159N_P3_V2_CONTROL: first-witness replay drift");
fi;
P159P3V2WrongOrderDiscriminator:=P159P3V2WrongOrderAggregateFirst;
Print("PENT159N_P3_V2_WRONG_ORDER_AGGREGATE_PASS q2_universe=",
  Length(P159P3V2Bfs)," residual_distinct_rows=",
  P159P3V2CWrongOrderQ2DistinctCount," residual_noncommuting_rows=",
  P159P3V2CWrongOrderQ2NoncommutingCount,
  " factor_noncommuting_rows=",
  P159P3V2WrongOrderFactorNoncommutingRowCount,
  " actual_distinct_and_factor_noncommuting_rows=",
  P159P3V2WrongOrderActualCofaceRowCount,
  " factor_noncommuting_pair_total=",
  P159P3V2WrongOrderNoncommutingPairTotal,
  " first_f_word=",P159P3V2WrongOrderDiscriminator.f_word,
  " external_S3_calibration_only=true\n");
