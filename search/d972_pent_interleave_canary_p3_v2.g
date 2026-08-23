#############################################################################
## D972 corrected pentagon-interleave canary, bounded p=3 producer v2.
##
## Authenticates the unpublished p3 v1 mathematical base and the independent
## v2 complete-control overlay, generates one hash-pinned effective source,
## executes it, and fail-closes on both receipt bytes and control semantics.
#############################################################################

P159P3O2BasePath := "search/d972_pent_interleave_canary_p3_math_v1.g";
P159P3O2BaseBytes := 52396;
P159P3O2BaseSha :=
  "ecc6a10befc8b37c627a90f29588b7ff4c992f31384642aa22a0fe4d76608c49";
P159P3O2OverlayPath :=
  "search/d972_pent_interleave_canary_p3_control_overlay_v2.g";
P159P3O2OverlayBytes := 5131;
P159P3O2OverlaySha :=
  "3accef86d2e20105eb767b8309d8dd1e6972f90294ecc63bb669cb3954e3c7f3";
P159P3O2EffectivePath :=
  "ci/out/d972_pent_interleave_canary_p3_math_effective_v2.g";
P159P3O2EffectiveBytes := 54203;
P159P3O2EffectiveSha :=
  "986533bf179e9352fe54471b082994f06981282b895edf16491c7f4c7891dabe";
P159P3O2ReceiptPath :=
  "ci/out/d972_pent_interleave_canary_p3_receipt_v2_20260824.json";
P159P3O2P2TriggerRun := 32652710118;
P159P3O2P2TriggerCommit :=
  "4e2de61961e167d058bcf963e6add5a0eb6edfe0";
P159P3O2P2TriggerReceiptBytes := 214729;
P159P3O2P2TriggerReceiptSha :=
  "79fc3b392f6e9c514c469c92e230c60d244472a15c252ccc482666943faf387e";
P159P3O2P2TriggerRunLogBytes := 7206;
P159P3O2P2TriggerRunLogSha :=
  "40c0b9845c012da41c516a9d994e57af407bb993dfa554d9acc2fa9bb54bc0a4";

P159P3O2CountSublist := function(s,needle)
  local count,pos,tail,offset,rel;
  if Length(needle)=0 then Error("PENT159N_P3_OUTER_V2: empty needle"); fi;
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

P159P3O2ReplaceExact := function(s,old,new,expected,label)
  local got;
  got:=P159P3O2CountSublist(s,old);
  if got<>expected then
    Error("PENT159N_P3_OUTER_V2: replacement count drift ",label,
      " expected=",expected," observed=",got);
  fi;
  return ReplacedString(s,old,new);
end;

P159P3O2CheckedWriteText := function(path,payload)
  local stream,readback;
  stream:=OutputTextFile(path,false);
  if stream=fail then Error("PENT159N_P3_OUTER_V2: cannot open effective source"); fi;
  SetPrintFormattingStatus(stream,false);
  PrintTo(stream,payload); CloseStream(stream);
  readback:=StringFile(path);
  if readback=fail or readback<>payload or
     HexSHA256(readback)<>HexSHA256(payload) then
    Error("PENT159N_P3_OUTER_V2: effective source closed-write/hash mismatch");
  fi;
  return rec(bytes:=Length(readback),sha256:=HexSHA256(readback));
end;

P159P3O2BaseRaw:=StringFile(P159P3O2BasePath);
if P159P3O2BaseRaw=fail or Length(P159P3O2BaseRaw)<>P159P3O2BaseBytes or
   HexSHA256(P159P3O2BaseRaw)<>P159P3O2BaseSha then
  Error("PENT159N_P3_OUTER_V2: p3 v1 mathematical base missing or pin drift");
fi;
P159P3O2OverlayRaw:=StringFile(P159P3O2OverlayPath);
if P159P3O2OverlayRaw=fail or
   Length(P159P3O2OverlayRaw)<>P159P3O2OverlayBytes or
   HexSHA256(P159P3O2OverlayRaw)<>P159P3O2OverlaySha then
  Error("PENT159N_P3_OUTER_V2: v2 control overlay missing or pin drift");
fi;
Print("PENT159N_P3_V2_INPUT_PINS_PASS base_bytes=",P159P3O2BaseBytes,
  " base_sha256=",P159P3O2BaseSha," overlay_bytes=",P159P3O2OverlayBytes,
  " overlay_sha256=",P159P3O2OverlaySha,"\n");

P159P3O2Effective:=P159P3O2BaseRaw;
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "P159P3V1","P159P3V2",854,"mathematical namespace");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "PENT159N_P3_V1","PENT159N_P3_V2",75,"diagnostic namespace");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "finite p=3 stage v1","finite p=3 stage v2",1,"header version");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "search/d972_pent_interleave_canary_p3_math_v1.g",
  P159P3O2EffectivePath,1,"runtime source path");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "ci/out/d972_pent_interleave_canary_p3_receipt_v1_20260824.json",
  P159P3O2ReceiptPath,1,"receipt path");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "d972-pent-interleave-canary-p3/v1",
  "d972-pent-interleave-canary-p3/v2",1,"receipt schema");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "status:=\"MEASURED_P3_STAGE\"",
  "status:=\"MEASURED_P3_STAGE_CONTROL_AGGREGATE_V2\"",1,
  "receipt status");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "NOT_IN_P3_V1_BOUNDED_STAGE","NOT_IN_P3_V2_BOUNDED_STAGE",4,
  "deferred-version labels");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "p2_v1_through_v9_edited","p2_v1_through_v10_edited",1,
  "firewall version range");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "32651230906",String(P159P3O2P2TriggerRun),1,"p2 trigger run");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "211971",String(P159P3O2P2TriggerReceiptBytes),1,
  "p2 trigger receipt bytes");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "bc1e3e0e610f6043567017b220c4e7947da9c5541a2130dbd63116b28ea9c84e",
  P159P3O2P2TriggerReceiptSha,1,"p2 trigger receipt SHA");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "7855",String(P159P3O2P2TriggerRunLogBytes),1,
  "p2 trigger run-log bytes");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  "b93a3a082d15e50263e86be0268320fbd6b49b7de5428c59e53865d9ec8b0f91",
  P159P3O2P2TriggerRunLogSha,1,"p2 trigger run-log SHA");
P159P3O2OldTriggerStatus:=
  "    p2_trigger_receipt_sha256:=P159P3V2P2ReceiptSha,";
P159P3O2NewTriggerStatus:=Concatenation(P159P3O2OldTriggerStatus,"\n",
  "    p2_trigger_commit:=\"",P159P3O2P2TriggerCommit,"\",\n",
  "    p2_trigger_producer_grade_only:=true,\n",
  "    p2_trigger_crosscheck_closed:=false,");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  P159P3O2OldTriggerStatus,P159P3O2NewTriggerStatus,2,
  "p2 trigger status boundary");

P159P3O2OldOverlayAnchor:=Concatenation(
  "  \" external_S3_calibration_only=true\\n\");\n",
  "if P159P3V2InversionDiscriminator=fail then");
P159P3O2NewOverlayAnchor:=Concatenation(
  "  \" external_S3_calibration_only=true\\n\");\n",
  "P159P3V2RequireFileSha(\n",
  "  \"search/d972_pent_interleave_canary_p3_control_overlay_v2.g\",\n",
  "  \"",P159P3O2OverlaySha,"\",\n",
  "  \"p3 v2 complete actual-coface control overlay\");\n",
  "Read(\"search/d972_pent_interleave_canary_p3_control_overlay_v2.g\");\n",
  "if P159P3V2WrongOrderActualCofaceRowCount=0 then\n",
  "  Error(\"PENT159N_P3_V2: aggregate control overlay did not close\");\n",
  "fi;\n",
  "if P159P3V2InversionDiscriminator=fail then");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  P159P3O2OldOverlayAnchor,P159P3O2NewOverlayAnchor,1,
  "authenticated aggregate-overlay injection");

P159P3O2OldFactorReceipt:=Concatenation(
  "  destructive_controls:=rec(\n",
  "    wrong_order_mutant:=\"phi123*phi1_23_4*phi234*(phi12_3_4*phi1_2_34)^-1\",\n",
  "    wrong_order_noncommuting_discriminator:=P159P3V2WrongOrderDiscriminator,");
P159P3O2NewFactorReceipt:=Concatenation(
  "  destructive_controls:=rec(\n",
  "    wrong_order_mutant:=\"phi123*phi1_23_4*phi234*(phi12_3_4*phi1_2_34)^-1\",\n",
  "    wrong_order_correct_paper_factors:=[\"A^-1\",\"B^-1\",\"C\",\"E\",\"F\"],\n",
  "    wrong_order_correct_native_factors:=[\"F\",\"E\",\"C\",\"B^-1\",\"A^-1\"],\n",
  "    wrong_order_mutant_paper_factors:=[\"F\",\"E\",\"C\",\"B^-1\",\"A^-1\"],\n",
  "    wrong_order_mutant_native_factors:=[\"A^-1\",\"B^-1\",\"C\",\"E\",\"F\"],\n",
  "    wrong_order_control_contract:=\"actual complete-Q2 coface-derived row with distinct residuals and at least one noncommuting factor pair\",\n",
  "    wrong_order_noncommuting_discriminator:=P159P3V2WrongOrderDiscriminator,");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  P159P3O2OldFactorReceipt,P159P3O2NewFactorReceipt,1,
  "receipt factor-order contract");

P159P3O2OldAggregateReceipt:=Concatenation(
  "    wrong_order_external_S3_calibration_accepted_as_pass:=false,\n",
  "    wrong_order_full_Q2_universe_count:=Length(P159P3V2Bfs),");
P159P3O2NewAggregateReceipt:=Concatenation(
  "    wrong_order_external_S3_calibration_accepted_as_pass:=false,\n",
  "    wrong_order_factor_noncommuting_row_count:=P159P3V2WrongOrderFactorNoncommutingRowCount,\n",
  "    wrong_order_actual_distinct_and_factor_noncommuting_row_count:=P159P3V2WrongOrderActualCofaceRowCount,\n",
  "    wrong_order_noncommuting_factor_pair_total:=P159P3V2WrongOrderNoncommutingPairTotal,\n",
  "    wrong_order_full_Q2_universe_count:=Length(P159P3V2Bfs),");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  P159P3O2OldAggregateReceipt,P159P3O2NewAggregateReceipt,1,
  "receipt aggregate counts");

P159P3O2OldProvenance:=Concatenation(
  "    derivation_base_sha256:=\"1d020d26a7aedb34a6b2d5732b0d95e36cc13b7c2a5e0424209d012d1695643d\",\n",
  "    p2_trigger_run_id:=P159P3V2P2TriggerRun,");
P159P3O2NewProvenance:=Concatenation(
  "    derivation_base_sha256:=\"1d020d26a7aedb34a6b2d5732b0d95e36cc13b7c2a5e0424209d012d1695643d\",\n",
  "    v2_authenticated_base_path:=\"search/d972_pent_interleave_canary_p3_math_v1.g\",\n",
  "    v2_authenticated_base_sha256:=\"",P159P3O2BaseSha,"\",\n",
  "    v2_control_overlay_path:=\"search/d972_pent_interleave_canary_p3_control_overlay_v2.g\",\n",
  "    v2_control_overlay_sha256:=\"",P159P3O2OverlaySha,"\",\n",
  "    p2_trigger_run_id:=P159P3V2P2TriggerRun,");
P159P3O2Effective:=P159P3O2ReplaceExact(P159P3O2Effective,
  P159P3O2OldProvenance,P159P3O2NewProvenance,1,
  "v2 provenance pins");

if Length(P159P3O2Effective)<>P159P3O2EffectiveBytes or
   HexSHA256(P159P3O2Effective)<>P159P3O2EffectiveSha then
  Error("PENT159N_P3_OUTER_V2: generated effective source pin drift bytes=",
    Length(P159P3O2Effective)," sha256=",HexSHA256(P159P3O2Effective));
fi;
P159P3O2EffectiveWrite:=P159P3O2CheckedWriteText(P159P3O2EffectivePath,
  P159P3O2Effective);
Print("PENT159N_P3_V2_EFFECTIVE_SOURCE_WRITTEN path=",P159P3O2EffectivePath,
  " bytes=",P159P3O2EffectiveWrite.bytes," sha256=",
  P159P3O2EffectiveWrite.sha256,"\n");
Read(P159P3O2EffectivePath);

if not IsBoundGlobal("P159P3V2Write") or
   not IsBoundGlobal("P159P3V2Receipt") or
   not IsBoundGlobal("P159P3V2Output") then
  Error("PENT159N_P3_OUTER_V2: effective source returned without receipt state");
fi;
P159P3O2WriteState:=ValueGlobal("P159P3V2Write");
P159P3O2ReceiptState:=ValueGlobal("P159P3V2Receipt");
P159P3O2OutputState:=ValueGlobal("P159P3V2Output");
if not IsRecord(P159P3O2WriteState) or
   not IsRecord(P159P3O2ReceiptState) or
   P159P3O2OutputState<>P159P3O2ReceiptPath or
   P159P3O2ReceiptState.schema<>"d972-pent-interleave-canary-p3/v2" then
  Error("PENT159N_P3_OUTER_V2: invalid receipt state/path/schema");
fi;
P159P3O2ReceiptRaw:=StringFile(P159P3O2ReceiptPath);
if P159P3O2ReceiptRaw=fail or
   Length(P159P3O2ReceiptRaw)<>P159P3O2WriteState.bytes or
   HexSHA256(P159P3O2ReceiptRaw)<>P159P3O2WriteState.sha256 then
  Error("PENT159N_P3_OUTER_V2: receipt closed-write/readback hash mismatch");
fi;
P159P3O2Control:=P159P3O2ReceiptState.destructive_controls;
if P159P3O2ReceiptState.quotients.Q2.prime<>3 or
   P159P3O2ReceiptState.quotients.Q2.order_decimal<>"2187" or
   P159P3O2ReceiptState.commutator_instrument.enumerated_count<>
     P159P3O2ReceiptState.commutator_instrument.derived_order or
   P159P3O2ReceiptState.actual_charming_onto_gate.raw_pair_count<>
     P159P3O2ReceiptState.actual_charming_onto_gate.evaluated_count or
   P159P3O2Control.wrong_order_full_Q2_universe_count<>2187 or
   P159P3O2Control.wrong_order_control_requires_actual_coface_row<>true or
   P159P3O2Control.wrong_order_external_S3_calibration_accepted_as_pass<>
     false or
   P159P3O2Control.wrong_order_actual_distinct_and_factor_noncommuting_row_count<=0 or
   P159P3O2Control.wrong_order_factor_noncommuting_row_count<=0 or
   P159P3O2Control.wrong_order_noncommuting_factor_pair_total<=0 then
  Error("PENT159N_P3_OUTER_V2: prime/coverage/aggregate control gate failed");
fi;
P159P3O2Witness:=P159P3O2Control.wrong_order_noncommuting_discriminator;
if P159P3O2Witness=fail or P159P3O2Witness.actual_coface_Dpap_row<>true or
   P159P3O2Witness.residuals_distinct<>true or
   P159P3O2Witness.relevant_factor_noncommutation<>true or
   Length(P159P3O2Witness.factor_labels)<>5 or
   Length(P159P3O2Witness.factor_coords)<>5 or
   Length(P159P3O2Witness.noncommuting_factor_pairs)=0 then
  Error("PENT159N_P3_OUTER_V2: actual-coface witness gate failed");
fi;
if not (P159P3O2ReceiptState.terminal_token in [
    "PENT159N_P3_ACTUAL_CHARMING_SENSITIVE__P3_COMPLETE",
    "PENT159N_P3_INSTRUMENT_SENSITIVE_ACTUAL_CHARMING_BLIND__P3_COMPLETE",
    "PENT159N_P3_INSTRUMENT_AND_ACTUAL_CHARMING_BLIND__P3_COMPLETE"]) then
  Error("PENT159N_P3_OUTER_V2: unrecognized terminal token");
fi;
Print("PENT159N_P3_V2_OUTER_FINAL_PASS receipt_path=",P159P3O2ReceiptPath,
  " bytes=",P159P3O2WriteState.bytes," sha256=",P159P3O2WriteState.sha256,
  " actual_control_rows=",
  P159P3O2Control.wrong_order_actual_distinct_and_factor_noncommuting_row_count,
  " terminal=",P159P3O2ReceiptState.terminal_token,"\n");
