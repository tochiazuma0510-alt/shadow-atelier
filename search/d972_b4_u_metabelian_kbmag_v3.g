#############################################################################
## d972_b4_u_metabelian_kbmag_v3.g -- replay-gated exact K terminal lane.
##
## This wrapper is intentionally separate from the mutable v1/v2 drafts.  It
## pins the current raw-RS producer, forces its same-job independent GAP
## replay, and emits a receipt only after the replay receipt and both complete
## ledgers agree.  A nonidentity norm is a sound A witness even if K is not
## abelian.  The B branch additionally requires every generator commutator to
## vanish and the independently reconstructed K_ab=C9^10.
#############################################################################

D972MCV3V1Path := "search/d972_b4_u_metabelian_kbmag_v1.g";;
D972MCV3V1Sha :=
  "a3972236122dac32e74c6c8527d8dec8c8adc61e7f4dabb107af7660bc039dac";;
D972MCV3Output := "ci/out/d972_b4_u_metabelian_kbmag_v3.json";;
D972MCV3ReplayPath := "ci/out/d972_b4_u_metabelian_kbmag_replay_v1.json";;
D972MCV3Reached := false;;
if IsBound(D972_B4_METABELIAN_V3_OUTPUT) then
  D972MCV3Output := D972_B4_METABELIAN_V3_OUTPUT;
fi;
if IsBound(D972_B4_METABELIAN_V3_REPLAY_OUTPUT) then
  D972MCV3ReplayPath := D972_B4_METABELIAN_V3_REPLAY_OUTPUT;
fi;
if not IsString(D972MCV3Output) or not IsString(D972MCV3ReplayPath) then
  Error("metabelian v3: output paths must be strings");
fi;

D972MCV3V1Raw := StringFile(D972MCV3V1Path);;
if D972MCV3V1Raw=fail or HexSHA256(D972MCV3V1Raw)<>D972MCV3V1Sha then
  Error("metabelian v3: pinned v1 source SHA drift");
fi;
if PositionSublist(D972MCV3V1Raw,Concatenation("QU","IT;"))<>fail then
  Error("metabelian v3: bare QUIT in v1 read context");
fi;

D972MCV3Json := function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\"");
  fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("metabelian v3: JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972MCV3Json(x[i]));;
  return Concatenation("[",JoinStringsWithSeparator(p,","),"]");
end;;

## Convert a GAP group element to the signed generator-row convention used by
## the receipt.  The frozen v1 producer accidentally sends a group object to
## D972ANV2SignedWord on its two nonidentity diagnostic paths.  Keep the
## source hash frozen and repair those two calls in the TEMP copy below.
D972MCV3SignedObj := function(w)
  local e,out,i,g,n,j;
  e:=ExtRepOfObj(w);;
  out:=[];; i:=1;;
  while i<=Length(e) do
    g:=e[i];; n:=e[i+1];;
    if n>0 then
      for j in [1..n] do Add(out,g); od;
    else
      for j in [1..-n] do Add(out,-g); od;
    fi;
    i:=i+2;;
  od;
  return out;
end;;

D972MCV3Selftest := IsBound(D972_B4_METABELIAN_V3_SELFTEST) and
  D972_B4_METABELIAN_V3_SELFTEST=true;;

## This construction is deliberately outside the heavy branch: the numeric
## selftest must execute the same GAP string operations that patch the v1
## producer, including both line-ending variants.
D972MCV3CountSub:=function(text,needle)
  local i,last,n;
  n:=0;; last:=Length(text)-Length(needle)+1;;
  if last<1 then return 0; fi;
  for i in [1..last] do
    if text{[i..i+Length(needle)-1]}=needle then n:=n+1; fi;
  od;
  return n;
end;;
D972MCV3BadCRLF:=Concatenation(")",List([44,34,44,13,10],CharInt));;
D972MCV3GoodCRLF:=Concatenation(")",List([44,34,44,34,44,13,10],CharInt));;
D972MCV3BadLF:=Concatenation(")",List([44,34,44,10],CharInt));;
D972MCV3GoodLF:=Concatenation(")",List([44,34,44,34,44,10],CharInt));;
D972MCV3ExpectedCommaFields:=29;;
D972MCV3BadCount:=D972MCV3CountSub(D972MCV3V1Raw,D972MCV3BadCRLF)+
  D972MCV3CountSub(D972MCV3V1Raw,D972MCV3BadLF);;
D972MCV3GoodBefore:=D972MCV3CountSub(D972MCV3V1Raw,D972MCV3GoodCRLF)+
  D972MCV3CountSub(D972MCV3V1Raw,D972MCV3GoodLF);;
D972MCV3ObjNeedle:="D972ANV2SignedWord(D972MCZ,D972MCKG)";;
D972MCV3ObjReplacement:="D972MCV3SignedObj(D972MCZ)";;
D972MCV3SnfField:=",\"snf_rank\":161";;
D972MCV3ObjCount:=D972MCV3CountSub(D972MCV3V1Raw,D972MCV3ObjNeedle);;
if D972MCV3BadCount<>D972MCV3ExpectedCommaFields or
   D972MCV3GoodBefore<>0 or D972MCV3ObjCount<>2 then
  Error("metabelian v3: frozen v1 patch occurrence drift");
fi;

if D972MCV3Selftest then
  D972MCV3Patched := ReplacedString(D972MCV3V1Raw,
    D972MCV3BadCRLF,D972MCV3GoodCRLF);;
  D972MCV3Patched := ReplacedString(D972MCV3Patched,
    D972MCV3BadLF,D972MCV3GoodLF);;
  D972MCV3Patched := ReplacedString(D972MCV3Patched,
    D972MCV3ObjNeedle,D972MCV3ObjReplacement);;
  if D972MCV3BadCount<>29 or D972MCV3GoodBefore<>0 or
     D972MCV3ObjCount<>2 or
     D972MCV3CountSub(D972MCV3Patched,D972MCV3BadCRLF)+
       D972MCV3CountSub(D972MCV3Patched,D972MCV3BadLF)<>0 or
     D972MCV3CountSub(D972MCV3Patched,D972MCV3GoodCRLF)+
       D972MCV3CountSub(D972MCV3Patched,D972MCV3GoodLF)<>29 or
     D972MCV3CountSub(D972MCV3Patched,D972MCV3ObjNeedle)<>0 or
     D972MCV3CountSub(D972MCV3Patched,D972MCV3ObjReplacement)<>2 then
    Error("metabelian v3 selftest: patched occurrence gate failed");
  fi;
  D972MCV3TestF:=FreeGroup(2,"d972_v3_obj_test");;
  D972MCV3TestG:=GeneratorsOfGroup(D972MCV3TestF);;
  if D972MCV3SignedObj(D972MCV3TestG[1]*D972MCV3TestG[2]^-1)<>[1,-2] then
    Error("metabelian v3 selftest: ExtRep signed-row conversion failed");
  fi;
  if LoadPackage("json")<>true then
    Error("metabelian v3 selftest: json package unavailable");
  fi;
  D972MCV3MetaProbe:=Concatenation(
    "{\"post_replay_requested\":true",D972MCV3SnfField,
    ",\"kernel_index\":32,\"kernel_order\":1}");;
  if PositionSublist(D972MCV3MetaProbe,",,")<>fail then
    Error("metabelian v3 selftest: metadata double comma");
  fi;
  D972MCV3MetaProbeObj:=JsonStringToGap(D972MCV3MetaProbe);;
  if not IsRecord(D972MCV3MetaProbeObj) or
     D972MCV3MetaProbeObj.post_replay_requested<>true or
     D972MCV3MetaProbeObj.snf_rank<>161 or
     D972MCV3MetaProbeObj.kernel_index<>32 then
    Error("metabelian v3 selftest: metadata JSON parse failed");
  fi;
  D972MCV3Reached := true;;
  Print("B4_U_METABELIAN_V3_SELFTEST_PASS source_sha256=",D972MCV3V1Sha,
    " replay_forced=true comma_bad=29 comma_good=29 object_calls=2\n");
else
  ## The v1 producer writes its private receipt and automata to TEMP.  The
  ## replay then reads those exact paths in the same GAP process and writes
  ## the fixed ci/out receipt consumed below.
  D972_B4_METABELIAN_OUTPUT :=
    Filename(DirectoryTemporary(),"d972_b4_u_metabelian_kbmag_v1_v3_inner.json");;
  D972_B4_METABELIAN_POST_REPLAY := true;;
  ## The current v1 draft had a GAP-4.16 parser trap in its JSON builder:
  ## `),",` at an expression boundary is missing the closing quote of the
  ## comma string.  Insert that quote in TEMP; preserve the JSON comma.
  ## Count both line-ending variants exactly, and reject any pre-existing
  ## corrected occurrence or any dangling occurrence after replacement.
  if D972MCV3BadCount<>D972MCV3ExpectedCommaFields or
     D972MCV3GoodBefore<>0 or D972MCV3ObjCount<>2 then
    Error("metabelian v3: v1 JSON comma occurrence drift");
  fi;
  D972MCV3Patched := ReplacedString(D972MCV3V1Raw,
    D972MCV3BadCRLF,D972MCV3GoodCRLF);;
  D972MCV3Patched := ReplacedString(D972MCV3Patched,
    D972MCV3BadLF,D972MCV3GoodLF);;
  D972MCV3Patched := ReplacedString(D972MCV3Patched,
    D972MCV3ObjNeedle,D972MCV3ObjReplacement);;
  if D972MCV3CountSub(D972MCV3Patched,D972MCV3BadCRLF)+
     D972MCV3CountSub(D972MCV3Patched,D972MCV3BadLF)<>0 or
     D972MCV3CountSub(D972MCV3Patched,D972MCV3GoodCRLF)+
     D972MCV3CountSub(D972MCV3Patched,D972MCV3GoodLF)<>
        D972MCV3ExpectedCommaFields or
     D972MCV3CountSub(D972MCV3Patched,D972MCV3ObjNeedle)<>0 or
     D972MCV3CountSub(D972MCV3Patched,D972MCV3ObjReplacement)<>2 then
    Error("metabelian v3: patched JSON comma gate failed");
  fi;
  D972MCV3V1Temp := Filename(DirectoryTemporary(),
    "d972_b4_u_metabelian_kbmag_v3_v1_patched.g");;
  FileString(D972MCV3V1Temp,D972MCV3Patched);;
  Read(D972MCV3V1Temp);;
  if not IsBound(D972MCStatus) or not IsBound(D972MCAuto) or
     not IsBound(D972MCGpGenMult) or not IsBound(D972MCGpCheckMult) or
     not IsBound(D972MCAxioms) or not IsBound(D972MCCommBits) or
     not IsBound(D972MCNormBits) or not IsBound(D972MCAb) or
     not IsBound(D972ANV2WordObj) then
    Error("metabelian v3: producer bindings missing");
  fi;
  if Length(D972MCCommBits)<>12880 or Length(D972MCNormBits)<>972 then
    Error("metabelian v3: incomplete producer ledger");
  fi;
  if D972MCAuto<>true or D972MCGpGenMult<>true or
     D972MCGpCheckMult<>true or D972MCAxioms<>true then
    D972MCV3Status := "UNKNOWN_AUTOMATIC_OR_AXIOMS";;
  elif Length(D972MCNormBad)>0 then
    D972MCV3Status := "B4_A_TERMINAL";;
  elif Number(D972MCCommBits,x->x=true)<>12880 then
    D972MCV3Status := "UNKNOWN_K_NONABELIAN";;
  elif Number(D972MCNormBits,x->x=true)<>972 then
    D972MCV3Status := "UNKNOWN_NORM_LEDGER";;
  elif SortedList(D972MCAb)<>List([1..10],x->9) then
    D972MCV3Status := "UNKNOWN_K_AB_INVARIANTS";;
  else
    D972MCV3Status := "B4_B_FINITE_ORDER_TERMINAL";;
  fi;

  ## The producer must have written the private receipt before invoking the
  ## replay.  Binding its hash into the replay receipt prevents a stale FSA
  ## ledger from being paired with a new raw presentation.
  D972MCV3InnerRaw := StringFile(D972_B4_METABELIAN_OUTPUT);;
  D972MCV3ReplayRaw := StringFile(D972MCV3ReplayPath);;
  if D972MCV3InnerRaw=fail or D972MCV3ReplayRaw=fail then
    Error("metabelian v3: same-job replay receipt missing");
  fi;
  D972MCV3ReplayObj := JsonStringToGap(D972MCV3ReplayRaw);;
  if not IsRecord(D972MCV3ReplayObj) or
     D972MCV3ReplayObj.schema<>"d972-b4-u-metabelian-kbmag-replay/v1" or
     D972MCV3ReplayObj.producer_receipt_sha256<>HexSHA256(D972MCV3InnerRaw) or
     D972MCV3ReplayObj.source_sha256<>D972ANV2SourceSha or
     D972MCV3ReplayObj.rs_constructor_sha256<>D972MCSourceSha or
     D972MCV3ReplayObj.rho_words_sha256<>D972MCRhoSha or
     D972MCV3ReplayObj.relator_sha256<>D972ANV2RelSha or
     D972MCV3ReplayObj.norm_original_sha256<>D972ANV2NormSha or
     D972MCV3ReplayObj.norm_count<>972 or
     D972MCV3ReplayObj.commutator_count<>12880 or
     D972MCV3ReplayObj.gpgenmult_rechecked<>true or
     D972MCV3ReplayObj.gpcheckmult_rechecked<>true or
     D972MCV3ReplayObj.gpaxioms_rechecked<>true or
     D972MCV3ReplayObj.automata_replayed<>true or
     D972MCV3ReplayObj.commutator_ledger_sha256<>
       HexSHA256(D972MCV3Json(D972MCCommBits)) or
     D972MCV3ReplayObj.norm_ledger_sha256<>
       HexSHA256(D972MCV3Json(D972MCNormBits)) or
     D972MCV3ReplayObj.commutator_empty_count<>
       Number(D972MCCommBits,x->x=true) or
     D972MCV3ReplayObj.norm_empty_count<>
       Number(D972MCNormBits,x->x=true) then
    Error("metabelian v3: independent replay mismatch");
  fi;

  D972MCV3AbSorted := SortedList(D972MCAb);;
  D972MCV3AbOrder := Product(D972MCV3AbSorted);;
  D972MCV3NormFirst := [];;
  if Length(D972MCNormBad)>0 then
    D972MCV3NormFirst := ShallowCopy(D972MCNormBad[1]);
  fi;
  ## Keep the v2 receipt schema so the already independent v2 checker can
  ## consume this stronger v3 producer without importing it.
  D972MCV3Out := Concatenation(
    "{\"schema\":\"d972-b4-u-metabelian-kbmag/v2\",\"status\":",
    D972MCV3Json(D972MCV3Status),
    ",\"producer_v1_sha256\":",D972MCV3Json(D972MCV3V1Sha),
    ",\"replay_receipt_sha256\":",D972MCV3Json(HexSHA256(D972MCV3ReplayRaw)),
    ",\"inner_receipt_sha256\":",D972MCV3Json(HexSHA256(D972MCV3InnerRaw)),
    ",\"source_sha256\":",D972MCV3Json(D972ANV2SourceSha),
    ",\"rs_constructor_sha256\":",D972MCV3Json(D972MCSourceSha),
    ",\"rho_words_sha256\":",D972MCV3Json(D972MCRhoSha),
    ",\"relator_sha256\":",D972MCV3Json(D972ANV2RelSha),
    ",\"norm_original_sha256\":",D972MCV3Json(D972ANV2NormSha),
    ",\"word_artifact_sha256\":",D972MCV3Json(D972ANV2WordsSha),
    ",\"word_artifact_canonical_sha256\":",
      D972MCV3Json(D972ANV2WordObj.canonical_bytes_sha256),
    ",\"raw_rs_relators_sha256\":",
      D972MCV3Json(HexSHA256(D972ANV2Json(D972ANV2Raw.relators))),
    ",\"norm_rs_sha256\":",
      D972MCV3Json(HexSHA256(D972ANV2Json(D972ANV2NormRows))),
    ",\"raw_rs_generator_count\":161,\"raw_rs_relator_count\":5056,",
    "\"norm_count\":972,\"commutator_count\":12880,",
    "\"commutator_empty_count\":",String(Number(D972MCCommBits,x->x=true)),
    ",\"norm_empty_count\":",String(Number(D972MCNormBits,x->x=true)),
    ",\"commutator_ledger\":",D972MCV3Json(D972MCCommBits),
    ",\"norm_ledger\":",D972MCV3Json(D972MCNormBits),
    ",\"commutator_ledger_sha256\":",
      D972MCV3Json(HexSHA256(D972MCV3Json(D972MCCommBits))),
    ",\"norm_ledger_sha256\":",
      D972MCV3Json(HexSHA256(D972MCV3Json(D972MCNormBits))),
    ",\"automatic_success\":",D972MCV3Json(D972MCAuto),
    ",\"gpgenmult_rechecked\":",D972MCV3Json(D972MCGpGenMult),
    ",\"gpcheckmult_rechecked\":",D972MCV3Json(D972MCGpCheckMult),
    ",\"gpaxioms_rechecked\":",D972MCV3Json(D972MCAxioms),
    ",\"large\":",D972MCV3Json(D972MCLarge),
    ",\"filestore\":",D972MCV3Json(D972MCFilestore),
    ",\"diff1\":",D972MCV3Json(D972MCDiff1),
    ",\"abelian_invariants\":",D972MCV3Json(D972MCV3AbSorted),
    D972MCV3SnfField,
    ",\"kernel_index\":32,\"kernel_order\":",String(D972MCV3AbOrder),
    ",\"u_order\":",String(32*D972MCV3AbOrder),
    ",\"first_norm_defect\":",D972MCV3Json(D972MCV3NormFirst),
    ",\"post_replay_requested\":true,",
    "\"proof_level\":\"RAW_RS_AUTOMATIC_GPAXIOMS_AND_SAME_JOB_GAP_REPLAY\"}");;
  D972MCV3F := OutputTextFile(D972MCV3Output,false);;
  SetPrintFormattingStatus(D972MCV3F,false);;
  PrintTo(D972MCV3F,Concatenation(D972MCV3Out,"\n"));;
  CloseStream(D972MCV3F);;
  D972MCV3Reached := true;;
  if D972MCV3Status="B4_A_TERMINAL" or
     D972MCV3Status="B4_B_FINITE_ORDER_TERMINAL" then
    Print("B4_U_METABELIAN_V3_TERMINAL_MARKER status=",D972MCV3Status,
      " output=",D972MCV3Output," comm_empty=",
      Number(D972MCCommBits,x->x=true),"/12880 norm_empty=",
      Number(D972MCNormBits,x->x=true),"/972 u_order=",32*D972MCV3AbOrder,
      " replay=PASS\n");
  else
    Print("B4_U_METABELIAN_V3_FINAL_MARKER status=",D972MCV3Status,
      " output=",D972MCV3Output," replay=PASS\n");
  fi;
fi;
