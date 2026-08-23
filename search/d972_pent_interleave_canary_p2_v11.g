#############################################################################
## D972 corrected pentagon-interleave canary, p=2 literal-A.18 repair v11.
##
## Authenticates frozen producer p2-v10 and the v11 pre-census A.18 gate,
## generates one hash-pinned effective source, executes it, and fail-closes on
## the receipt.  No checker source, verdict, or report is read or imported.
#############################################################################

P159P2O11BasePath := "search/d972_pent_interleave_canary_p2_math_v10.g";
P159P2O11BaseBytes := 54180;
P159P2O11BaseSha :=
  "c3df3d2ae54f7cfaf8f18e4f98e1f2bf4f9754b06902c6b5a2bfd134490f26d0";
P159P2O11OverlayPath :=
  "search/d972_pent_interleave_literal_a18_p2_overlay_v11.g";
P159P2O11OverlayBytes := 6048;
P159P2O11OverlaySha :=
  "a20a3dc8e4847109ee7172040495421027678b4cb4167247f64b948df20c13a8";
P159P2O11EffectivePath :=
  "ci/out/d972_pent_interleave_canary_p2_math_effective_v11.g";
P159P2O11EffectiveBytes := 56314;
P159P2O11EffectiveSha :=
  "6f6f7b1a9adbc54882006865b29b77d8560fefbaa5e015c6d60511dc56a96404";
P159P2O11ReceiptPath :=
  "ci/out/d972_pent_interleave_canary_p2_receipt_v11_20260824.json";

P159P2O11CountSublist := function(s,needle)
  local count,pos,tail,offset,rel;
  if Length(needle)=0 then Error("PENT159N_P2_OUTER_V11: empty needle"); fi;
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

P159P2O11ReplaceExact := function(s,old,new,expected,label)
  local got;
  got:=P159P2O11CountSublist(s,old);
  if got<>expected then
    Error("PENT159N_P2_OUTER_V11: replacement count drift ",label,
      " expected=",expected," observed=",got);
  fi;
  return ReplacedString(s,old,new);
end;

P159P2O11ReplaceSpan := function(s,startMarker,endMarker,new,label)
  local p1,p2,tail,rel;
  if P159P2O11CountSublist(s,startMarker)<>1 or
     P159P2O11CountSublist(s,endMarker)<>1 then
    Error("PENT159N_P2_OUTER_V11: span marker count drift ",label);
  fi;
  p1:=PositionSublist(s,startMarker);
  tail:=s{[p1..Length(s)]}; rel:=PositionSublist(tail,endMarker);
  if rel=fail then Error("PENT159N_P2_OUTER_V11: span order drift ",label); fi;
  p2:=p1+rel-1;
  return Concatenation(s{[1..p1-1]},new,s{[p2..Length(s)]});
end;

P159P2O11CheckedWriteText := function(path,payload)
  local stream,readback;
  stream:=OutputTextFile(path,false);
  if stream=fail then Error("PENT159N_P2_OUTER_V11: cannot open effective source"); fi;
  SetPrintFormattingStatus(stream,false);
  PrintTo(stream,payload); CloseStream(stream);
  readback:=StringFile(path);
  if readback=fail or readback<>payload or
     HexSHA256(readback)<>HexSHA256(payload) then
    Error("PENT159N_P2_OUTER_V11: effective source closed-write/hash mismatch");
  fi;
  return rec(bytes:=Length(readback),sha256:=HexSHA256(readback));
end;

P159P2O11BaseRaw:=StringFile(P159P2O11BasePath);
if P159P2O11BaseRaw=fail or Length(P159P2O11BaseRaw)<>P159P2O11BaseBytes or
   HexSHA256(P159P2O11BaseRaw)<>P159P2O11BaseSha then
  Error("PENT159N_P2_OUTER_V11: frozen p2-v10 producer base pin drift");
fi;
P159P2O11OverlayRaw:=StringFile(P159P2O11OverlayPath);
if P159P2O11OverlayRaw=fail or
   Length(P159P2O11OverlayRaw)<>P159P2O11OverlayBytes or
   HexSHA256(P159P2O11OverlayRaw)<>P159P2O11OverlaySha then
  Error("PENT159N_P2_OUTER_V11: literal-A.18 overlay pin drift");
fi;
Print("PENT159N_P2_V11_INPUT_PINS_PASS base_bytes=",P159P2O11BaseBytes,
  " base_sha256=",P159P2O11BaseSha," overlay_bytes=",
  P159P2O11OverlayBytes," overlay_sha256=",P159P2O11OverlaySha,"\n");

P159P2O11Effective:=P159P2O11BaseRaw;
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "P159P2V10","P159P2V11",864,"mathematical namespace");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "PENT159N_P2_V10","PENT159N_P2_V11",74,"diagnostic namespace");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "finite p=2 stage v10","finite p=2 literal-A.18 repair stage v11",1,
  "header version");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "search/d972_pent_interleave_canary_p2_math_v10.g",
  P159P2O11EffectivePath,1,"runtime source path");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "ci/out/d972_pent_interleave_canary_p2_receipt_v10_20260824.json",
  P159P2O11ReceiptPath,1,"receipt path");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "d972-pent-interleave-canary-p2/v10",
  "d972-pent-interleave-canary-p2/v11",1,"receipt schema");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "MEASURED_P2_STAGE_CONTROL_REPAIR_V10",
  "MEASURED_P2_LITERAL_A18_REPAIR_V11",1,"receipt status");

P159P2O11OldHeader:=JoinStringsWithSeparator([
  "## Producer-only standalone control repair, derived mechanically from the",
  "## authenticated successful p=2 v9 effective source.  It reads no checker",
  "## source, verdict, or report.  Quotients, maps, literal Dpap order, instrument,",
  "## and actual-charming gate are unchanged.  V10 replaces only the insufficient",
  "## arbitrary-S3 wrong-order pass by a complete actual-coface-derived control."],"\n");
P159P2O11NewHeader:=JoinStringsWithSeparator([
  "## Producer-only literal-A.18 repair derived mechanically from frozen p2 v10.",
  "## It reads no checker source, verdict, or report.  Before any quotient census,",
  "## every printed A.18 coface is serialized once to native order and must preserve",
  "## both frozen PB3 relators.  The prior direct-use reversal is mutant-only."],"\n");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  P159P2O11OldHeader,P159P2O11NewHeader,1,"header contract");

P159P2O11OldEarly:=JoinStringsWithSeparator([
  "if P159P2V11P3Pres.relation_count<>2 or P159P2V11P4Pres.relation_count<>11 then",
  "  Error(\"PENT159N_P2_V11: FN presentation relation-count drift\");",
  "fi;","","P159P2V11Phase(\"BUILD_Q2_D4_2\");"],"\n");
P159P2O11NewEarly:=JoinStringsWithSeparator([
  "if P159P2V11P3Pres.relation_count<>2 or P159P2V11P4Pres.relation_count<>11 then",
  "  Error(\"PENT159N_P2_V11: FN presentation relation-count drift\");",
  "fi;",
  "P159P2V11RequireFileSha(",
  "  \"search/d972_pent_interleave_literal_a18_p2_overlay_v11.g\",",
  "  \"a20a3dc8e4847109ee7172040495421027678b4cb4167247f64b948df20c13a8\",",
  "  \"literal A.18 p2 v11 source-relator overlay\");",
  "Read(\"search/d972_pent_interleave_literal_a18_p2_overlay_v11.g\");",
  "if not IsBoundGlobal(\"P159P2V11A18GateReceipt\") or",
  "   P159P2V11A18GateReceipt.literal_all_relators_preserved<>true then",
  "  Error(\"PENT159N_P2_V11: literal A.18 pre-census gate did not close\");",
  "fi;","","P159P2V11Phase(\"BUILD_Q2_D4_2\");"],"\n");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  P159P2O11OldEarly,P159P2O11NewEarly,1,"pre-census overlay injection");

P159P2O11MapStart:="P159P2V11DelWords:=P159P2V11Deletions(4);";
P159P2O11MapEnd:=Concatenation("\n\n",
  "#############################################################################\n",
  "## Complete commutator instrument");
P159P2O11NewMap:=JoinStringsWithSeparator([
  "P159P2V11DelWords:=P159P2V11Deletions(4);",
  "P159P2V11CofWordsPaper:=P159P2V11A18PaperWords;",
  "P159P2V11CofWordsNative:=P159P2V11A18NativeWords;",
  "## Every finite map consumes only the once-serialized native table.",
  "P159P2V11CofWords:=P159P2V11CofWordsNative;",
  "P159P2V11ExpectedDelWords:=[",
  "  [[],[],[],[1],[2],[3]],",
  "  [[],[1],[2],[],[],[3]],",
  "  [[1],[],[2],[],[3],[]],",
  "  [[1],[2],[],[3],[],[]]",
  "];",
  "if P159P2V11DelWords<>P159P2V11ExpectedDelWords then",
  "  Error(\"PENT159N_P2_V11: deletion strand/renumbering table drift\");",
  "fi;",
  "P159P2V11DeletionMaps:=List([1..4],i->P159P2V11MapCertificate(",
  "  Concatenation(\"delete_strand_\",String(i)),\"ordinary_pure_braid_deletion\",",
  "  P159P2V11Q4,P159P2V11Q4Pc,P159P2V11Q3,P159P2V11Q3Pc,P159P2V11DelWords[i]));",
  "P159P2V11CofaceMaps:=List([1..5],i->P159P2V11MapCertificate(",
  "  Concatenation(\"coface_slot_\",String(i-1)),\"literal_A18_once_serialized_native\",",
  "  P159P2V11Q3,P159P2V11Q3Pc,P159P2V11Q4,P159P2V11Q4Pc,",
  "  P159P2V11CofWordsNative[i]));",
  "P159P2V11IotaMap:=P159P2V11MapCertificate(\"F2_to_PB3_x12_x23\",",
  "  \"marked_F2_inclusion\",P159P2V11Q2,P159P2V11Q2Pc,P159P2V11Q3,P159P2V11Q3Pc,",
  "  [[1],[3]]);",
  "if Size(Image(P159P2V11IotaMap.hom_internal))<>Size(P159P2V11Q2.group) then",
  "  Error(\"PENT159N_P2_V11: marked Q2 to Q3 map is not injective\");",
  "fi;",
  "## Contexts use the exact same native words already admitted by the source-",
  "## relator gate and finite homomorphisms.  There is no second reversal here.",
  "P159P2V11Contexts:=List(P159P2V11CofWordsNative,m->[",
  "  P159P2V11NativeWordEval(m[1],P159P2V11Q4.marks),",
  "  P159P2V11NativeWordEval(m[3],P159P2V11Q4.marks)]);",
  "P159P2V11ContextWordsPaper:=List(P159P2V11CofWordsPaper,m->[m[1],m[3]]);",
  "P159P2V11ContextWordsNative:=List(P159P2V11CofWordsNative,m->[m[1],m[3]]);",
  "P159P2V11ExpectedContextWordsPaper:=[",
  "  [[4],[6]],",
  "  [[2,4],[6]],",
  "  [[1,2],[5,6]],",
  "  [[1],[4,5]],",
  "  [[1],[4]]",
  "];",
  "P159P2V11ExpectedContextWordsNative:=[",
  "  [[4],[6]],",
  "  [[4,2],[6]],",
  "  [[2,1],[6,5]],",
  "  [[1],[5,4]],",
  "  [[1],[4]]",
  "];",
  "if P159P2V11ContextWordsPaper<>P159P2V11ExpectedContextWordsPaper or",
  "   P159P2V11ContextWordsNative<>P159P2V11ExpectedContextWordsNative then",
  "  Error(\"PENT159N_P2_V11: literal A.18 context serialization drift\");",
  "fi;",
  "Print(\"PENT159N_P2_V11_MAPS_PASS deletions=4 cofaces=5\",",
  "  \" iota_image_order=\",Size(Image(P159P2V11IotaMap.hom_internal)),",
  "  \" deletion_table_sha256=\",P159P2V11Digest(P159P2V11DelWords),",
  "  \" a18_paper_table_sha256=\",P159P2V11Digest(P159P2V11CofWordsPaper),",
  "  \" a18_native_table_sha256=\",P159P2V11Digest(P159P2V11CofWordsNative),\"\\n\");"],"\n");
P159P2O11Effective:=P159P2O11ReplaceSpan(P159P2O11Effective,
  P159P2O11MapStart,P159P2O11MapEnd,P159P2O11NewMap,"marked-map block");

P159P2O11OldProvenance:=JoinStringsWithSeparator([
  "    derivation_base:=\"authenticated GHA p2 v9 effective source\",",
  "    derivation_base_sha256:=\"1d020d26a7aedb34a6b2d5732b0d95e36cc13b7c2a5e0424209d012d1695643d\",",
  "    predecessor_run_id:=P159P2V11PredecessorRun,"],"\n");
P159P2O11NewProvenance:=JoinStringsWithSeparator([
  "    derivation_base:=\"frozen producer p2 v10 mathematical source; v10 semantic output rejected at A.18 homomorphism boundary\",",
  "    derivation_base_sha256:=\"c3df3d2ae54f7cfaf8f18e4f98e1f2bf4f9754b06902c6b5a2bfd134490f26d0\",",
  "    literal_a18_overlay_path:=\"search/d972_pent_interleave_literal_a18_p2_overlay_v11.g\",",
  "    literal_a18_overlay_sha256:=\"a20a3dc8e4847109ee7172040495421027678b4cb4167247f64b948df20c13a8\",",
  "    predecessor_p2_v10_semantic_status:=\"REJECTED_AT_A18_HOMOMORPHISM_BOUNDARY\",",
  "    predecessor_run_id:=P159P2V11PredecessorRun,"],"\n");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  P159P2O11OldProvenance,P159P2O11NewProvenance,1,"provenance");

P159P2O11OldMarked:=JoinStringsWithSeparator([
  "    coface_table:=P159P2V11CofWords,",
  "    coface_table_sha256:=P159P2V11Digest(P159P2V11CofWords),",
  "    a18_F2_context_words_by_slot_0_to_4:=P159P2V11ContextWords,",
  "    deletions:=List(P159P2V11DeletionMaps,P159P2V11PublicMap),"],"\n");
P159P2O11NewMarked:=JoinStringsWithSeparator([
  "    coface_table:=P159P2V11CofWordsNative,",
  "    coface_table_sha256:=P159P2V11Digest(P159P2V11CofWordsNative),",
  "    coface_table_serialization:=\"literal printed A.18 paper words reversed exactly once to native order\",",
  "    a18_printed_paper_table:=P159P2V11CofWordsPaper,",
  "    a18_printed_paper_table_sha256:=P159P2V11Digest(P159P2V11CofWordsPaper),",
  "    a18_serialized_native_table:=P159P2V11CofWordsNative,",
  "    a18_serialized_native_table_sha256:=P159P2V11Digest(P159P2V11CofWordsNative),",
  "    a18_F2_context_paper_words_by_slot_0_to_4:=P159P2V11ContextWordsPaper,",
  "    a18_F2_context_native_words_by_slot_0_to_4:=P159P2V11ContextWordsNative,",
  "    a18_source_relator_gate:=P159P2V11A18GateReceipt,",
  "    deletions:=List(P159P2V11DeletionMaps,P159P2V11PublicMap),"],"\n");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  P159P2O11OldMarked,P159P2O11NewMarked,1,"marked-map receipt");

P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "wrong_order_correct_paper_factors","literal_Dpap_paper_factors",1,
  "literal paper factors");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "wrong_order_correct_native_factors","literal_Dpap_native_factors",1,
  "literal native factors");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "wrong_order_mutant_paper_factors","section_9_1_mutant_paper_factors",1,
  "mutant paper factors");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "wrong_order_mutant_native_factors","section_9_1_mutant_native_factors",1,
  "mutant native factors");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "PENT159N_P2_V11_WRONG_ORDER_FORMULA_PIN_PASS correct_paper=A^-1*B^-1*C*E*F correct_native=F*E*C*B^-1*A^-1 mutant_paper=F*E*C*B^-1*A^-1 mutant_native=A^-1*B^-1*C*E*F",
  "PENT159N_P2_V11_LITERAL_DPAP_FORMULA_PIN_PASS literal_paper=A^-1*B^-1*C*E*F literal_native=F*E*C*B^-1*A^-1 section_9_1_mutant_paper=F*E*C*B^-1*A^-1 section_9_1_mutant_native=A^-1*B^-1*C*E*F",
  1,"literal versus section-9.1 marker");
P159P2O11OldControl:=JoinStringsWithSeparator([
  "    wrong_order_control_contract:=\"actual complete-Q2 coface-derived row with distinct residuals and at least one noncommuting factor pair\",",
  "    wrong_order_control_requires_actual_coface_row:=true,"],"\n");
P159P2O11NewControl:=JoinStringsWithSeparator([
  "    wrong_order_control_contract:=\"actual complete-Q2 literal-A.18 homomorphism-gated row with distinct residuals and at least one noncommuting factor pair\",",
  "    literal_A18_source_relator_gate_pass:=P159P2V11A18GateReceipt.literal_all_relators_preserved,",
  "    literal_A18_source_relator_gate_before_census:=true,",
  "    direct_use_count_fitting_reversal_accepted_as_coface:=false,",
  "    section_9_1_order_mutant_only:=true,",
  "    wrong_order_control_requires_actual_coface_row:=true,"],"\n");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  P159P2O11OldControl,P159P2O11NewControl,1,"literal A.18 control gate");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "source:=\"actual complete-Q2 coface-derived Dpap row\"",
  "source:=\"actual complete-Q2 literal-A.18 homomorphism-gated Dpap row\"",
  1,"witness provenance");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "p2_v1_through_v9_edited:=false,v10_prior_version_overwritten:=false",
  "p2_v1_through_v10_edited:=false,v11_overwrote_prior_version:=false",1,
  "firewall version boundary");
P159P2O11Effective:=P159P2O11ReplaceExact(P159P2O11Effective,
  "main_sol_reply_edited:=false,p2_v1_through_v10_edited:=false",
  "main_sol_reply_edited:=false,class4_row36_mode_K2_work_performed:=false,p2_v1_through_v10_edited:=false",
  1,"bounded-scope firewall");

if Length(P159P2O11Effective)<>P159P2O11EffectiveBytes or
   HexSHA256(P159P2O11Effective)<>P159P2O11EffectiveSha then
  Error("PENT159N_P2_OUTER_V11: generated effective source pin drift bytes=",
    Length(P159P2O11Effective)," sha256=",HexSHA256(P159P2O11Effective));
fi;
P159P2O11EffectiveWrite:=P159P2O11CheckedWriteText(P159P2O11EffectivePath,
  P159P2O11Effective);
Print("PENT159N_P2_V11_EFFECTIVE_SOURCE_WRITTEN path=",
  P159P2O11EffectivePath," bytes=",P159P2O11EffectiveWrite.bytes,
  " sha256=",P159P2O11EffectiveWrite.sha256,"\n");
Read(P159P2O11EffectivePath);

if not IsBoundGlobal("P159P2V11Write") or
   not IsBoundGlobal("P159P2V11Receipt") or
   not IsBoundGlobal("P159P2V11Output") then
  Error("PENT159N_P2_OUTER_V11: effective source returned without receipt state");
fi;
P159P2O11WriteState:=ValueGlobal("P159P2V11Write");
P159P2O11ReceiptState:=ValueGlobal("P159P2V11Receipt");
P159P2O11OutputState:=ValueGlobal("P159P2V11Output");
if not IsRecord(P159P2O11WriteState) or
   not IsRecord(P159P2O11ReceiptState) or
   P159P2O11OutputState<>P159P2O11ReceiptPath or
   P159P2O11ReceiptState.schema<>"d972-pent-interleave-canary-p2/v11" then
  Error("PENT159N_P2_OUTER_V11: invalid receipt state/path/schema");
fi;
P159P2O11ReceiptRaw:=StringFile(P159P2O11ReceiptPath);
if P159P2O11ReceiptRaw=fail or
   Length(P159P2O11ReceiptRaw)<>P159P2O11WriteState.bytes or
   HexSHA256(P159P2O11ReceiptRaw)<>P159P2O11WriteState.sha256 then
  Error("PENT159N_P2_OUTER_V11: receipt closed-write/readback hash mismatch");
fi;
P159P2O11Gate:=P159P2O11ReceiptState.marked_maps.a18_source_relator_gate;
P159P2O11Control:=P159P2O11ReceiptState.destructive_controls;
if P159P2O11ReceiptState.quotients.Q2.prime<>2 or
   P159P2O11ReceiptState.quotients.Q2.order_decimal<>"128" or
   P159P2O11ReceiptState.commutator_instrument.enumerated_count<>
     P159P2O11ReceiptState.commutator_instrument.derived_order or
   P159P2O11ReceiptState.actual_charming_onto_gate.raw_pair_count<>
     P159P2O11ReceiptState.actual_charming_onto_gate.evaluated_count then
  Error("PENT159N_P2_OUTER_V11: prime or coverage gate failed");
fi;
if P159P2O11Gate.literal_relator_gate_row_count<>10 or
   P159P2O11Gate.literal_all_relators_preserved<>true or
   ForAny(P159P2O11Gate.literal_relator_gate_rows,r->r.passed<>true) or
   P159P2O11Gate.reversal_mutant_accepted_as_coface<>false or
   P159P2O11Gate.required_reversal_mutant_failure.slot_index_zero_based<>1 or
   P159P2O11Gate.required_reversal_mutant_failure.source_relator_index<>1 or
   P159P2O11Gate.required_reversal_mutant_failure.passed<>false then
  Error("PENT159N_P2_OUTER_V11: literal A.18 source-relator gate failed");
fi;
if P159P2O11Control.literal_A18_source_relator_gate_pass<>true or
   P159P2O11Control.literal_A18_source_relator_gate_before_census<>true or
   P159P2O11Control.direct_use_count_fitting_reversal_accepted_as_coface<>false or
   P159P2O11Control.section_9_1_order_mutant_only<>true or
   P159P2O11Control.wrong_order_control_requires_actual_coface_row<>true or
   P159P2O11Control.wrong_order_external_S3_calibration_accepted_as_pass<>false or
   P159P2O11Control.wrong_order_actual_distinct_and_factor_noncommuting_row_count<=0 then
  Error("PENT159N_P2_OUTER_V11: repaired Dpap/control semantics failed");
fi;
if not (P159P2O11ReceiptState.terminal_token in [
    "PENT159N_P2_ACTUAL_CHARMING_SENSITIVE",
    "PENT159N_P2_INSTRUMENT_SENSITIVE_ACTUAL_CHARMING_BLIND__P3_REQUIRED",
    "PENT159N_P2_INSTRUMENT_AND_ACTUAL_CHARMING_BLIND__P3_REQUIRED"]) then
  Error("PENT159N_P2_OUTER_V11: unrecognized prime-local terminal token");
fi;
Print("PENT159N_P2_V11_OUTER_FINAL_PASS receipt_path=",P159P2O11ReceiptPath,
  " bytes=",P159P2O11WriteState.bytes," sha256=",P159P2O11WriteState.sha256,
  " literal_relator_rows=",P159P2O11Gate.literal_relator_gate_row_count,
  " terminal=",P159P2O11ReceiptState.terminal_token,"\n");
