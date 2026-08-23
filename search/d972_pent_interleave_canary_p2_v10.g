#############################################################################
## D972 corrected pentagon-interleave canary, finite p=2 control repair v10.
##
## This outer driver authenticates the standalone producer source before it is
## read and then fail-closes on the closed receipt and the repaired destructive
## control.  It never reads a checker source, verdict, or report.
#############################################################################

P159P2V10OuterSource := "search/d972_pent_interleave_canary_p2_v10.g";
P159P2V10MathSource := "search/d972_pent_interleave_canary_p2_math_v10.g";
P159P2V10MathSourceBytes := 54180;
P159P2V10MathSourceSha :=
  "c3df3d2ae54f7cfaf8f18e4f98e1f2bf4f9754b06902c6b5a2bfd134490f26d0";
P159P2V10ExpectedReceiptPath :=
  "ci/out/d972_pent_interleave_canary_p2_receipt_v10_20260824.json";

P159P2V10OuterRaw:=StringFile(P159P2V10MathSource);
if P159P2V10OuterRaw=fail or Length(P159P2V10OuterRaw)<>
   P159P2V10MathSourceBytes or
   HexSHA256(P159P2V10OuterRaw)<>P159P2V10MathSourceSha then
  Error("PENT159N_P2_V10_OUTER: standalone math source missing or SHA/byte drift");
fi;
if PositionSublist(P159P2V10OuterRaw,
     "wrong_order_external_S3_calibration_accepted_as_pass:=false")=fail or
   PositionSublist(P159P2V10OuterRaw,
     "wrong_order_actual_distinct_and_factor_noncommuting_row_count")=fail or
   PositionSublist(P159P2V10OuterRaw,
     "PENT159N_P2_V10_WRONG_ORDER_FORMULA_PIN_PASS")=fail then
  Error("PENT159N_P2_V10_OUTER: repaired control source fragments absent");
fi;
Print("PENT159N_P2_V10_MATH_SOURCE_PIN_PASS path=",P159P2V10MathSource,
  " bytes=",P159P2V10MathSourceBytes," sha256=",P159P2V10MathSourceSha,"\n");

Read(P159P2V10MathSource);

## Nested Read syntax diagnostics need not force a nonzero GAP exit in every
## runner.  Require the closed in-memory state and independently re-read the
## exact receipt bytes before accepting the run.
if not IsBoundGlobal("P159P2V10Write") or
   not IsBoundGlobal("P159P2V10Receipt") or
   not IsBoundGlobal("P159P2V10Output") then
  Error("PENT159N_P2_V10_OUTER: math source returned without closed receipt state");
fi;
P159P2V10OuterWrite:=ValueGlobal("P159P2V10Write");
P159P2V10OuterReceipt:=ValueGlobal("P159P2V10Receipt");
P159P2V10OuterOutput:=ValueGlobal("P159P2V10Output");
if not IsRecord(P159P2V10OuterWrite) or
   not IsRecord(P159P2V10OuterReceipt) or
   P159P2V10OuterOutput<>P159P2V10ExpectedReceiptPath then
  Error("PENT159N_P2_V10_OUTER: invalid receipt state or path");
fi;
P159P2V10OuterReadback:=StringFile(P159P2V10ExpectedReceiptPath);
if P159P2V10OuterReadback=fail or
   Length(P159P2V10OuterReadback)<>P159P2V10OuterWrite.bytes or
   HexSHA256(P159P2V10OuterReadback)<>P159P2V10OuterWrite.sha256 then
  Error("PENT159N_P2_V10_OUTER: receipt closed-write/readback hash gate failed");
fi;

P159P2V10OuterControl:=P159P2V10OuterReceipt.destructive_controls;
if P159P2V10OuterReceipt.schema<>"d972-pent-interleave-canary-p2/v10" or
   P159P2V10OuterReceipt.quotients.Q2.prime<>2 or
   P159P2V10OuterReceipt.quotients.Q2.order_decimal<>"128" or
   P159P2V10OuterReceipt.commutator_instrument.enumerated_count<>
     P159P2V10OuterReceipt.commutator_instrument.derived_order or
   P159P2V10OuterReceipt.actual_charming_onto_gate.raw_pair_count<>
     P159P2V10OuterReceipt.actual_charming_onto_gate.evaluated_count then
  Error("PENT159N_P2_V10_OUTER: core receipt semantic gate failed");
fi;
if P159P2V10OuterControl.wrong_order_control_requires_actual_coface_row<>true or
   P159P2V10OuterControl.wrong_order_external_S3_calibration_accepted_as_pass<>
     false or
   P159P2V10OuterControl.wrong_order_full_Q2_universe_count<>128 or
   P159P2V10OuterControl.wrong_order_actual_distinct_and_factor_noncommuting_row_count<=0 or
   P159P2V10OuterControl.wrong_order_factor_noncommuting_row_count<=0 or
   P159P2V10OuterControl.wrong_order_noncommuting_factor_pair_total<=0 then
  Error("PENT159N_P2_V10_OUTER: repaired aggregate wrong-order control failed");
fi;
P159P2V10OuterWitness:=
  P159P2V10OuterControl.wrong_order_noncommuting_discriminator;
if P159P2V10OuterWitness=fail or
   P159P2V10OuterWitness.actual_coface_Dpap_row<>true or
   P159P2V10OuterWitness.residuals_distinct<>true or
   P159P2V10OuterWitness.relevant_factor_noncommutation<>true or
   Length(P159P2V10OuterWitness.factor_labels)<>5 or
   Length(P159P2V10OuterWitness.factor_coords)<>5 or
   Length(P159P2V10OuterWitness.noncommuting_factor_pairs)=0 then
  Error("PENT159N_P2_V10_OUTER: first actual-coface witness gate failed");
fi;
P159P2V10OuterAllowedTerminals:=[
  "PENT159N_P2_ACTUAL_CHARMING_SENSITIVE",
  "PENT159N_P2_INSTRUMENT_SENSITIVE_ACTUAL_CHARMING_BLIND__P3_REQUIRED",
  "PENT159N_P2_INSTRUMENT_AND_ACTUAL_CHARMING_BLIND__P3_REQUIRED"
];
if not P159P2V10OuterReceipt.terminal_token in
   P159P2V10OuterAllowedTerminals then
  Error("PENT159N_P2_V10_OUTER: unrecognized terminal token");
fi;
Print("PENT159N_P2_V10_OUTER_FINAL_PASS receipt_path=",
  P159P2V10ExpectedReceiptPath," bytes=",P159P2V10OuterWrite.bytes,
  " sha256=",P159P2V10OuterWrite.sha256," actual_control_rows=",
  P159P2V10OuterControl.wrong_order_actual_distinct_and_factor_noncommuting_row_count,
  " terminal=",P159P2V10OuterReceipt.terminal_token,"\n");
