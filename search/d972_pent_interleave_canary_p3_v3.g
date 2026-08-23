#############################################################################
## D972 corrected pentagon-interleave canary, p=3 literal-A.18 repair v3.
##
## Authenticates the immutable producer-generated p3-v2 effective source from
## GHA run 32653488263 and two v3 overlays, generates one hash-pinned effective
## source, executes it, and fail-closes on receipt semantics.  No checker lane
## source, verdict, or report is read or imported.
#############################################################################

P159P3O3BasePath :=
  "ci/pent159n_p3_v2_artifacts_32653488263/d972_pent_interleave_canary_p3_math_effective_v2.g";
P159P3O3BaseBytes := 54203;
P159P3O3BaseSha :=
  "986533bf179e9352fe54471b082994f06981282b895edf16491c7f4c7891dabe";
P159P3O3A18Path :=
  "search/d972_pent_interleave_literal_a18_p3_overlay_v3.g";
P159P3O3A18Bytes := 5627;
P159P3O3A18Sha :=
  "ee165826581f15848cc06c94762a337909c40718eb1a1bf6dc8e02c156a66fab";
P159P3O3ControlPath :=
  "search/d972_pent_interleave_canary_p3_control_overlay_v3.g";
P159P3O3ControlBytes := 5342;
P159P3O3ControlSha :=
  "fc977883d147469b6c6ad56d6ef69cb8b1f5579a4c599378339077840a71d36c";
P159P3O3EffectivePath :=
  "ci/out/d972_pent_interleave_canary_p3_math_effective_v3.g";
P159P3O3EffectiveBytes := 56579;
P159P3O3EffectiveSha :=
  "5dbaa59b63a4280727f9da4f109b452d30de16d1bc46eaa225df7fc024c23b3e";
P159P3O3ReceiptPath :=
  "ci/out/d972_pent_interleave_canary_p3_receipt_v3_20260824.json";

P159P3O3CountSublist := function(s,needle)
  local count,pos,tail,offset,rel;
  if Length(needle)=0 then Error("PENT159N_P3_OUTER_V3: empty needle"); fi;
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

P159P3O3ReplaceExact := function(s,old,new,expected,label)
  local got;
  got:=P159P3O3CountSublist(s,old);
  if got<>expected then
    Error("PENT159N_P3_OUTER_V3: replacement count drift ",label,
      " expected=",expected," observed=",got);
  fi;
  return ReplacedString(s,old,new);
end;

P159P3O3ReplaceSpan := function(s,startMarker,endMarker,new,label)
  local p1,p2,tail,rel;
  if P159P3O3CountSublist(s,startMarker)<>1 or
     P159P3O3CountSublist(s,endMarker)<>1 then
    Error("PENT159N_P3_OUTER_V3: span marker count drift ",label);
  fi;
  p1:=PositionSublist(s,startMarker);
  tail:=s{[p1..Length(s)]}; rel:=PositionSublist(tail,endMarker);
  if rel=fail then Error("PENT159N_P3_OUTER_V3: span order drift ",label); fi;
  p2:=p1+rel-1;
  return Concatenation(s{[1..p1-1]},new,s{[p2..Length(s)]});
end;

P159P3O3CheckedWriteText := function(path,payload)
  local stream,readback;
  stream:=OutputTextFile(path,false);
  if stream=fail then Error("PENT159N_P3_OUTER_V3: cannot open effective source"); fi;
  SetPrintFormattingStatus(stream,false);
  PrintTo(stream,payload); CloseStream(stream);
  readback:=StringFile(path);
  if readback=fail or readback<>payload or
     HexSHA256(readback)<>HexSHA256(payload) then
    Error("PENT159N_P3_OUTER_V3: effective source closed-write/hash mismatch");
  fi;
  return rec(bytes:=Length(readback),sha256:=HexSHA256(readback));
end;

P159P3O3BaseRaw:=StringFile(P159P3O3BasePath);
if P159P3O3BaseRaw=fail or Length(P159P3O3BaseRaw)<>P159P3O3BaseBytes or
   HexSHA256(P159P3O3BaseRaw)<>P159P3O3BaseSha then
  Error("PENT159N_P3_OUTER_V3: immutable p3-v2 producer base pin drift");
fi;
P159P3O3A18Raw:=StringFile(P159P3O3A18Path);
if P159P3O3A18Raw=fail or Length(P159P3O3A18Raw)<>P159P3O3A18Bytes or
   HexSHA256(P159P3O3A18Raw)<>P159P3O3A18Sha then
  Error("PENT159N_P3_OUTER_V3: literal-A.18 overlay pin drift");
fi;
P159P3O3ControlRaw:=StringFile(P159P3O3ControlPath);
if P159P3O3ControlRaw=fail or
   Length(P159P3O3ControlRaw)<>P159P3O3ControlBytes or
   HexSHA256(P159P3O3ControlRaw)<>P159P3O3ControlSha then
  Error("PENT159N_P3_OUTER_V3: aggregate-control overlay pin drift");
fi;
Print("PENT159N_P3_V3_INPUT_PINS_PASS base_bytes=",P159P3O3BaseBytes,
  " base_sha256=",P159P3O3BaseSha," a18_bytes=",P159P3O3A18Bytes,
  " a18_sha256=",P159P3O3A18Sha," control_bytes=",P159P3O3ControlBytes,
  " control_sha256=",P159P3O3ControlSha,"\n");

P159P3O3Effective:=P159P3O3BaseRaw;
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "P159P3V2","P159P3V3",859,"mathematical namespace");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "PENT159N_P3_V2","PENT159N_P3_V3",76,"diagnostic namespace");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "finite p=3 stage v2","finite p=3 literal-A.18 repair stage v3",1,
  "header version");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "ci/out/d972_pent_interleave_canary_p3_math_effective_v2.g",
  P159P3O3EffectivePath,1,"runtime source path");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "ci/out/d972_pent_interleave_canary_p3_receipt_v2_20260824.json",
  P159P3O3ReceiptPath,1,"receipt path");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "d972-pent-interleave-canary-p3/v2",
  "d972-pent-interleave-canary-p3/v3",1,"receipt schema");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "MEASURED_P3_STAGE_CONTROL_AGGREGATE_V2",
  "MEASURED_P3_LITERAL_A18_REPAIR_V3",1,"receipt status");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "NOT_IN_P3_V2_BOUNDED_STAGE","NOT_IN_P3_V3_BOUNDED_STAGE",4,
  "deferred labels");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "p3_prior_versions_overwritten","p3_v1_through_v2_edited",1,
  "firewall version boundary");

P159P3O3OldHeader:=JoinStringsWithSeparator([
  "## Producer-only standalone mathematical source, derived mechanically from the",
  "## authenticated successful p=2 v9 effective source.  It reads no task checker,",
  "## checker verdict, or checker report.  It reuses only the frozen authenticated",
  "## NQ portability stage v4, then constructs the marked D4_3 quotients through",
  "## the same direct NQ record/collector API.  It never forms the fp source",
  "## subgroup used by NqEpimorphismByNqOutput."],"\n");
P159P3O3NewHeader:=JoinStringsWithSeparator([
  "## Producer-only literal-A.18 repair derived from the immutable p3-v2 GHA",
  "## effective producer source.  It reads no checker source, verdict, or report.",
  "## Before any quotient or census, each printed A.18 word is serialized exactly",
  "## once to native order and both frozen PB3 source relators must map to identity.",
  "## The old direct-use table and section 9.1 order are destructive mutants only."],"\n");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  P159P3O3OldHeader,P159P3O3NewHeader,1,"header contract");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "    p2_trigger_crosscheck_closed:=false,",
  Concatenation("    p2_trigger_crosscheck_closed:=false,\n",
    "    p2_trigger_literal_A18_semantic_status:=\"REJECTED\","),
  2,"rejected p2 trigger status");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "    p2_trigger_terminal:=\"PENT159N_P2_INSTRUMENT_SENSITIVE_ACTUAL_CHARMING_BLIND__P3_REQUIRED\",",
  "    p2_predecessor_terminal_semantically_rejected_at_A18_boundary:=true,",
  1,"rejected p2 terminal");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "    p3_executed_due_to_p2_actual_charming_blind:=true,",
  Concatenation("    p3_executed_due_to_p2_actual_charming_blind:=false,\n",
    "    p3_executed_by_bounded_literal_A18_repair_authorization:=true,"),
  1,"repair routing");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "search/d972_pent_interleave_canary_p3_control_overlay_v2.g",
  P159P3O3ControlPath,3,"aggregate overlay path");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "3accef86d2e20105eb767b8309d8dd1e6972f90294ecc63bb669cb3954e3c7f3",
  P159P3O3ControlSha,2,"aggregate overlay SHA");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "v2 complete actual-coface control overlay",
  "v3 literal-A.18 complete actual-coface control overlay",1,
  "aggregate overlay label");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "aggregate control overlay did not close",
  "literal-A.18 aggregate control overlay did not close",1,
  "aggregate closure diagnostic");

P159P3O3OldEarly:=JoinStringsWithSeparator([
  "if P159P3V3P3Pres.relation_count<>2 or P159P3V3P4Pres.relation_count<>11 then",
  "  Error(\"PENT159N_P3_V3: FN presentation relation-count drift\");",
  "fi;","","P159P3V3Phase(\"BUILD_Q2_D4_3\");"],"\n");
P159P3O3NewEarly:=JoinStringsWithSeparator([
  "if P159P3V3P3Pres.relation_count<>2 or P159P3V3P4Pres.relation_count<>11 then",
  "  Error(\"PENT159N_P3_V3: FN presentation relation-count drift\");",
  "fi;",
  "P159P3V3RequireFileSha(",
  "  \"search/d972_pent_interleave_literal_a18_p3_overlay_v3.g\",",
  "  \"ee165826581f15848cc06c94762a337909c40718eb1a1bf6dc8e02c156a66fab\",",
  "  \"literal A.18 p3 v3 source-relator overlay\");",
  "Read(\"search/d972_pent_interleave_literal_a18_p3_overlay_v3.g\");",
  "if not IsBoundGlobal(\"P159P3V3A18RunFiniteRelatorGate\") then",
  "  Error(\"PENT159N_P3_V3: literal A.18 finite relator-gate function absent\");",
  "fi;","","P159P3V3Phase(\"BUILD_Q2_D4_3\");"],"\n");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  P159P3O3OldEarly,P159P3O3NewEarly,1,"pre-census A.18 injection");

P159P3O3MapStart:="P159P3V3DelWords:=P159P3V3Deletions(4);";
P159P3O3MapEnd:=Concatenation("\n\n",
  "#############################################################################\n",
  "## Complete commutator instrument");
P159P3O3NewMap:=JoinStringsWithSeparator([
  "P159P3V3A18GateReceipt:=P159P3V3A18RunFiniteRelatorGate(",
  "  P159P3V3Q4,P159P3V3Q4Pc);",
  "if P159P3V3A18GateReceipt.literal_all_relators_preserved<>true then",
  "  Error(\"PENT159N_P3_V3: finite A.18 gate did not close before maps/census\");",
  "fi;",
  "P159P3V3DelWords:=P159P3V3Deletions(4);",
  "P159P3V3CofWordsPaper:=P159P3V3A18PaperWords;",
  "P159P3V3CofWordsNative:=P159P3V3A18NativeWords;",
  "## Every finite map consumes only the once-serialized native table.",
  "P159P3V3CofWords:=P159P3V3CofWordsNative;",
  "P159P3V3ExpectedDelWords:=[",
  "  [[],[],[],[1],[2],[3]],",
  "  [[],[1],[2],[],[],[3]],",
  "  [[1],[],[2],[],[3],[]],",
  "  [[1],[2],[],[3],[],[]]",
  "];",
  "if P159P3V3DelWords<>P159P3V3ExpectedDelWords then",
  "  Error(\"PENT159N_P3_V3: deletion strand/renumbering table drift\");",
  "fi;",
  "P159P3V3DeletionMaps:=List([1..4],i->P159P3V3MapCertificate(",
  "  Concatenation(\"delete_strand_\",String(i)),\"ordinary_pure_braid_deletion\",",
  "  P159P3V3Q4,P159P3V3Q4Pc,P159P3V3Q3,P159P3V3Q3Pc,P159P3V3DelWords[i]));",
  "P159P3V3CofaceMaps:=List([1..5],i->P159P3V3MapCertificate(",
  "  Concatenation(\"coface_slot_\",String(i-1)),\"literal_A18_once_serialized_native\",",
  "  P159P3V3Q3,P159P3V3Q3Pc,P159P3V3Q4,P159P3V3Q4Pc,",
  "  P159P3V3CofWordsNative[i]));",
  "P159P3V3IotaMap:=P159P3V3MapCertificate(\"F2_to_PB3_x12_x23\",",
  "  \"marked_F2_inclusion\",P159P3V3Q2,P159P3V3Q2Pc,P159P3V3Q3,P159P3V3Q3Pc,",
  "  [[1],[3]]);",
  "if Size(Image(P159P3V3IotaMap.hom_internal))<>Size(P159P3V3Q2.group) then",
  "  Error(\"PENT159N_P3_V3: marked Q2 to Q3 map is not injective\");",
  "fi;",
  "## Contexts use the exact same native words admitted by both homomorphism gates.",
  "P159P3V3Contexts:=List(P159P3V3CofWordsNative,m->[",
  "  P159P3V3NativeWordEval(m[1],P159P3V3Q4.marks),",
  "  P159P3V3NativeWordEval(m[3],P159P3V3Q4.marks)]);",
  "P159P3V3ContextWordsPaper:=List(P159P3V3CofWordsPaper,m->[m[1],m[3]]);",
  "P159P3V3ContextWordsNative:=List(P159P3V3CofWordsNative,m->[m[1],m[3]]);",
  "P159P3V3ExpectedContextWordsPaper:=[",
  "  [[4],[6]],",
  "  [[2,4],[6]],",
  "  [[1,2],[5,6]],",
  "  [[1],[4,5]],",
  "  [[1],[4]]",
  "];",
  "P159P3V3ExpectedContextWordsNative:=[",
  "  [[4],[6]],",
  "  [[4,2],[6]],",
  "  [[2,1],[6,5]],",
  "  [[1],[5,4]],",
  "  [[1],[4]]",
  "];",
  "if P159P3V3ContextWordsPaper<>P159P3V3ExpectedContextWordsPaper or",
  "   P159P3V3ContextWordsNative<>P159P3V3ExpectedContextWordsNative then",
  "  Error(\"PENT159N_P3_V3: literal A.18 context serialization drift\");",
  "fi;",
  "Print(\"PENT159N_P3_V3_MAPS_PASS deletions=4 cofaces=5\",",
  "  \" iota_image_order=\",Size(Image(P159P3V3IotaMap.hom_internal)),",
  "  \" deletion_table_sha256=\",P159P3V3Digest(P159P3V3DelWords),",
  "  \" a18_paper_table_sha256=\",P159P3V3Digest(P159P3V3CofWordsPaper),",
  "  \" a18_native_table_sha256=\",P159P3V3Digest(P159P3V3CofWordsNative),\"\\n\");"],"\n");
P159P3O3Effective:=P159P3O3ReplaceSpan(P159P3O3Effective,
  P159P3O3MapStart,P159P3O3MapEnd,P159P3O3NewMap,"marked-map block");

P159P3O3OldProvenance:=JoinStringsWithSeparator([
  "    derivation_base:=\"authenticated GHA p2 v9 effective source\",",
  "    derivation_base_sha256:=\"1d020d26a7aedb34a6b2d5732b0d95e36cc13b7c2a5e0424209d012d1695643d\",",
  "    v2_authenticated_base_path:=\"search/d972_pent_interleave_canary_p3_math_v1.g\",",
  "    v2_authenticated_base_sha256:=\"ecc6a10befc8b37c627a90f29588b7ff4c992f31384642aa22a0fe4d76608c49\",",
  "    v2_control_overlay_path:=\"search/d972_pent_interleave_canary_p3_control_overlay_v3.g\",",
  "    v2_control_overlay_sha256:=\"fc977883d147469b6c6ad56d6ef69cb8b1f5579a4c599378339077840a71d36c\",",
  "    p2_trigger_run_id:=P159P3V3P2TriggerRun,"],"\n");
P159P3O3NewProvenance:=JoinStringsWithSeparator([
  "    derivation_base:=\"immutable producer-generated p3 v2 effective source from GHA run 32653488263; v2 semantic token rejected at A.18 boundary\",",
  "    derivation_base_path:=\"ci/pent159n_p3_v2_artifacts_32653488263/d972_pent_interleave_canary_p3_math_effective_v2.g\",",
  "    derivation_base_sha256:=\"986533bf179e9352fe54471b082994f06981282b895edf16491c7f4c7891dabe\",",
  "    literal_a18_overlay_path:=\"search/d972_pent_interleave_literal_a18_p3_overlay_v3.g\",",
  "    literal_a18_overlay_sha256:=\"ee165826581f15848cc06c94762a337909c40718eb1a1bf6dc8e02c156a66fab\",",
  "    aggregate_control_overlay_path:=\"search/d972_pent_interleave_canary_p3_control_overlay_v3.g\",",
  "    aggregate_control_overlay_sha256:=\"fc977883d147469b6c6ad56d6ef69cb8b1f5579a4c599378339077840a71d36c\",",
  "    rejected_p3_v2_receipt_sha256:=\"51d1bd649182b951fb7bed363f11eb854ad8d4ab824b87b1cc670c90ab253e56\",",
  "    p2_trigger_run_id:=P159P3V3P2TriggerRun,"],"\n");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  P159P3O3OldProvenance,P159P3O3NewProvenance,1,"provenance");

P159P3O3OldMarked:=JoinStringsWithSeparator([
  "    coface_table:=P159P3V3CofWords,",
  "    coface_table_sha256:=P159P3V3Digest(P159P3V3CofWords),",
  "    a18_F2_context_words_by_slot_0_to_4:=P159P3V3ContextWords,",
  "    deletions:=List(P159P3V3DeletionMaps,P159P3V3PublicMap),"],"\n");
P159P3O3NewMarked:=JoinStringsWithSeparator([
  "    coface_table:=P159P3V3CofWordsNative,",
  "    coface_table_sha256:=P159P3V3Digest(P159P3V3CofWordsNative),",
  "    coface_table_serialization:=\"literal printed A.18 paper words reversed exactly once to native order\",",
  "    a18_printed_paper_table:=P159P3V3CofWordsPaper,",
  "    a18_printed_paper_table_sha256:=P159P3V3Digest(P159P3V3CofWordsPaper),",
  "    a18_serialized_native_table:=P159P3V3CofWordsNative,",
  "    a18_serialized_native_table_sha256:=P159P3V3Digest(P159P3V3CofWordsNative),",
  "    a18_F2_context_paper_words_by_slot_0_to_4:=P159P3V3ContextWordsPaper,",
  "    a18_F2_context_native_words_by_slot_0_to_4:=P159P3V3ContextWordsNative,",
  "    a18_source_relator_gate:=P159P3V3A18GateReceipt,",
  "    deletions:=List(P159P3V3DeletionMaps,P159P3V3PublicMap),"],"\n");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  P159P3O3OldMarked,P159P3O3NewMarked,1,"marked-map receipt");

P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "wrong_order_correct_paper_factors","literal_Dpap_paper_factors",1,
  "literal paper factors");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "wrong_order_correct_native_factors","literal_Dpap_native_factors",1,
  "literal native factors");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "wrong_order_mutant_paper_factors","section_9_1_mutant_paper_factors",1,
  "mutant paper factors");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "wrong_order_mutant_native_factors","section_9_1_mutant_native_factors",1,
  "mutant native factors");
P159P3O3OldControl:=JoinStringsWithSeparator([
  "    wrong_order_control_contract:=\"actual complete-Q2 coface-derived row with distinct residuals and at least one noncommuting factor pair\",",
  "    wrong_order_noncommuting_discriminator:=P159P3V3WrongOrderDiscriminator,"],"\n");
P159P3O3NewControl:=JoinStringsWithSeparator([
  "    wrong_order_control_contract:=\"actual complete-Q2 literal-A.18 homomorphism-gated row with distinct residuals and at least one noncommuting factor pair\",",
  "    literal_A18_source_relator_gate_pass:=P159P3V3A18GateReceipt.literal_all_relators_preserved,",
  "    literal_A18_source_relator_gate_before_census:=true,",
  "    direct_use_count_fitting_reversal_accepted_as_coface:=false,",
  "    section_9_1_order_mutant_only:=true,",
  "    wrong_order_noncommuting_discriminator:=P159P3V3WrongOrderDiscriminator,"],"\n");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  P159P3O3OldControl,P159P3O3NewControl,1,"literal A.18 control gate");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "source:=\"actual complete-Q2 coface-derived Dpap row\"",
  "source:=\"actual complete-Q2 literal-A.18 homomorphism-gated Dpap row\"",
  1,"witness provenance");
P159P3O3Effective:=P159P3O3ReplaceExact(P159P3O3Effective,
  "main_sol_reply_edited:=false,p2_v1_through_v10_edited:=false",
  "main_sol_reply_edited:=false,class4_row36_mode_K2_work_performed:=false,p2_v1_through_v10_edited:=false",
  1,"bounded-scope firewall");

if Length(P159P3O3Effective)<>P159P3O3EffectiveBytes or
   HexSHA256(P159P3O3Effective)<>P159P3O3EffectiveSha then
  Error("PENT159N_P3_OUTER_V3: generated effective source pin drift bytes=",
    Length(P159P3O3Effective)," sha256=",HexSHA256(P159P3O3Effective));
fi;
P159P3O3EffectiveWrite:=P159P3O3CheckedWriteText(P159P3O3EffectivePath,
  P159P3O3Effective);
Print("PENT159N_P3_V3_EFFECTIVE_SOURCE_WRITTEN path=",P159P3O3EffectivePath,
  " bytes=",P159P3O3EffectiveWrite.bytes," sha256=",
  P159P3O3EffectiveWrite.sha256,"\n");
Read(P159P3O3EffectivePath);

if not IsBoundGlobal("P159P3V3Write") or
   not IsBoundGlobal("P159P3V3Receipt") or
   not IsBoundGlobal("P159P3V3Output") then
  Error("PENT159N_P3_OUTER_V3: effective source returned without receipt state");
fi;
P159P3O3WriteState:=ValueGlobal("P159P3V3Write");
P159P3O3ReceiptState:=ValueGlobal("P159P3V3Receipt");
P159P3O3OutputState:=ValueGlobal("P159P3V3Output");
if not IsRecord(P159P3O3WriteState) or
   not IsRecord(P159P3O3ReceiptState) or
   P159P3O3OutputState<>P159P3O3ReceiptPath or
   P159P3O3ReceiptState.schema<>"d972-pent-interleave-canary-p3/v3" then
  Error("PENT159N_P3_OUTER_V3: invalid receipt state/path/schema");
fi;
P159P3O3ReceiptRaw:=StringFile(P159P3O3ReceiptPath);
if P159P3O3ReceiptRaw=fail or
   Length(P159P3O3ReceiptRaw)<>P159P3O3WriteState.bytes or
   HexSHA256(P159P3O3ReceiptRaw)<>P159P3O3WriteState.sha256 then
  Error("PENT159N_P3_OUTER_V3: receipt closed-write/readback hash mismatch");
fi;
P159P3O3Gate:=P159P3O3ReceiptState.marked_maps.a18_source_relator_gate;
P159P3O3Control:=P159P3O3ReceiptState.destructive_controls;
if P159P3O3ReceiptState.quotients.Q2.prime<>3 or
   P159P3O3ReceiptState.quotients.Q2.order_decimal<>"2187" or
   P159P3O3ReceiptState.commutator_instrument.enumerated_count<>
     P159P3O3ReceiptState.commutator_instrument.derived_order or
   P159P3O3ReceiptState.actual_charming_onto_gate.raw_pair_count<>
     P159P3O3ReceiptState.actual_charming_onto_gate.evaluated_count then
  Error("PENT159N_P3_OUTER_V3: prime or coverage gate failed");
fi;
if P159P3O3Gate.literal_relator_gate_row_count<>10 or
   P159P3O3Gate.literal_all_relators_preserved<>true or
   ForAny(P159P3O3Gate.literal_relator_gate_rows,r->r.passed<>true) or
   P159P3O3Gate.reversal_mutant_accepted_as_coface<>false or
   P159P3O3Gate.required_reversal_mutant_failure.slot_index_zero_based<>1 or
   P159P3O3Gate.required_reversal_mutant_failure.source_relator_index<>1 or
   P159P3O3Gate.required_reversal_mutant_failure.passed<>false then
  Error("PENT159N_P3_OUTER_V3: literal A.18 source-relator gate failed");
fi;
if P159P3O3Control.literal_A18_source_relator_gate_pass<>true or
   P159P3O3Control.literal_A18_source_relator_gate_before_census<>true or
   P159P3O3Control.direct_use_count_fitting_reversal_accepted_as_coface<>false or
   P159P3O3Control.section_9_1_order_mutant_only<>true or
   P159P3O3Control.wrong_order_control_requires_actual_coface_row<>true or
   P159P3O3Control.wrong_order_external_S3_calibration_accepted_as_pass<>false or
   P159P3O3Control.wrong_order_actual_distinct_and_factor_noncommuting_row_count<=0 or
   P159P3O3Control.wrong_order_factor_noncommuting_row_count<=0 or
   P159P3O3Control.wrong_order_noncommuting_factor_pair_total<=0 then
  Error("PENT159N_P3_OUTER_V3: repaired Dpap/control semantics failed");
fi;
if not (P159P3O3ReceiptState.terminal_token in [
    "PENT159N_P3_ACTUAL_CHARMING_SENSITIVE__P3_COMPLETE",
    "PENT159N_P3_INSTRUMENT_SENSITIVE_ACTUAL_CHARMING_BLIND__P3_COMPLETE",
    "PENT159N_P3_INSTRUMENT_AND_ACTUAL_CHARMING_BLIND__P3_COMPLETE"]) then
  Error("PENT159N_P3_OUTER_V3: unrecognized prime-local terminal token");
fi;
Print("PENT159N_P3_V3_OUTER_FINAL_PASS receipt_path=",P159P3O3ReceiptPath,
  " bytes=",P159P3O3WriteState.bytes," sha256=",P159P3O3WriteState.sha256,
  " literal_relator_rows=",P159P3O3Gate.literal_relator_gate_row_count,
  " terminal=",P159P3O3ReceiptState.terminal_token,"\n");
