#############################################################################
## d972_b4_norm_tietze_kbmag_consumer_v2.g
##
## Consume the versioned pure-Python raw-RS/Tietze artifact.  This file does
## not construct a presentation from an opaque GAP isomorphism: it validates
## the pinned source/basis fields and the dense final relators/norm ledger,
## then gives KBMAG exactly that explicit <=127-generator presentation.
##
## The receipt remains a candidate until the independent Python replay checker
## accepts every primitive/map/norm event.  There is intentionally no QUIT;
## gap-run executes this script in Read context.
#############################################################################

if LoadPackage("json") <> true then
  Error("norm Tietze KBMAG v2: json package unavailable");
fi;
if LoadPackage("kbmag") <> true then
  Error("norm Tietze KBMAG v2: kbmag package unavailable");
fi;

D972NKBV2Input := "ci/out/d972_b4_norm_tietze_trace_v2.json";;
D972NKBV2Output := "ci/out/d972_b4_norm_tietze_kbmag_v2.json";;
if IsBound(D972_B4_NORM_TZ_ARTIFACT) then
  D972NKBV2Input := D972_B4_NORM_TZ_ARTIFACT;
fi;
if IsBound(D972_B4_NORM_TZ_KBMAG_OUTPUT) then
  D972NKBV2Output := D972_B4_NORM_TZ_KBMAG_OUTPUT;
fi;
D972NKBV2MaxEqns := 50000;;
D972NKBV2MaxStates := 50000;;
D972NKBV2MaxWdiffs := 50000;;
D972NKBV2MaxStored := [100,100];;
if IsBound(D972_B4_NORM_TZ_MAXEQNS) then D972NKBV2MaxEqns:=D972_B4_NORM_TZ_MAXEQNS; fi;
if IsBound(D972_B4_NORM_TZ_MAXSTATES) then D972NKBV2MaxStates:=D972_B4_NORM_TZ_MAXSTATES; fi;
if IsBound(D972_B4_NORM_TZ_MAXWDIFFS) then D972NKBV2MaxWdiffs:=D972_B4_NORM_TZ_MAXWDIFFS; fi;
if IsBound(D972_B4_NORM_TZ_MAXSTORED) then D972NKBV2MaxStored:=D972_B4_NORM_TZ_MAXSTORED; fi;

D972NKBV2SourceSha :=
  "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972NKBV2RelSha :=
  "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972NKBV2RowsSha :=
  "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930";;
D972NKBV2NormSha :=
  "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972NKBV2WordArtifactSha :=
  "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972NKBV2BasisId := "f2^5-positive-transversal-mask-order-v1";;
D972NKBV2PairSha :=
  "2be7ef40bbe19177a9777774e3685c4b5f564466a1f65fc55d5466b6dc34ca7e";;
D972NKBV2RawRsSha :=
  "29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e";;
D972NKBV2NormRsSha :=
  "f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8";;

D972NKBV2Join := function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1];;
  for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972NKBV2Json := function(x)
  local p,i,names;
  if IsInt(x) then return String(x); fi;
  ## GAP 4.16 represents the empty list with the string filter too.  The
  ## empty-list case must precede IsString or [] would serialize as "".
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if IsRecord(x) then
    names:=SortedList(RecNames(x));;
    p:=List(names,i->Concatenation("\"",i,"\":",D972NKBV2Json(x.(i))));;
    return Concatenation("{",D972NKBV2Join(p,","),"}");
  fi;
  if not IsList(x) then Error("norm Tietze KBMAG v2: JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972NKBV2Json(x[i]));;
  return Concatenation("[",D972NKBV2Join(p,","),"]");
end;;
D972NKBV2Reduce := function(w)
  local out,x;
  out:=[];;
  for x in w do
    if Length(out)>0 and Last(out)=-x then Remove(out);
    else Add(out,x); fi;
  od;
  return out;
end;;
D972NKBV2Canonical := function(rows)
  local out,w;
  out:=[];;
  for w in rows do
    w:=D972NKBV2Reduce(w);;
    if Length(w)>0 then Add(out,w); fi;
  od;
  Sort(out);;
  return out;
end;;
D972NKBV2Digest := function(rows)
  return HexSHA256(D972NKBV2Json(D972NKBV2Canonical(rows)));
end;;
D972NKBV2DigestRows := function(rows)
  return HexSHA256(D972NKBV2Json(List(rows,D972NKBV2Reduce)));
end;;
D972NKBV2SignedWord := function(row,gens)
  local z,a;
  z:=One(gens[1]);;
  for a in row do
    if a>0 then z:=z*gens[a]; else z:=z*gens[-a]^-1; fi;
  od;
  return z;
end;;

D972NKBV2Raw := StringFile(D972NKBV2Input);;
if D972NKBV2Raw=fail then Error("norm Tietze KBMAG v2: artifact missing"); fi;
D972NKBV2Obj := JsonStringToGap(D972NKBV2Raw);;
if not IsRecord(D972NKBV2Obj) or
   D972NKBV2Obj.schema<>"d972-b4-norm-tietze-trace/v2" or
   D972NKBV2Obj.source_sha256<>D972NKBV2SourceSha or
   D972NKBV2Obj.relator_sha256<>D972NKBV2RelSha or
   D972NKBV2Obj.normalized_rows_sha256<>D972NKBV2RowsSha or
   D972NKBV2Obj.roof_norm_words_sha256<>D972NKBV2NormSha or
   D972NKBV2Obj.word_artifact_sha256<>D972NKBV2WordArtifactSha or
   D972NKBV2Obj.basis_id<>D972NKBV2BasisId or
   D972NKBV2Obj.gen_bits<>[1,2,4,8,16,31] or
   D972NKBV2Obj.rs_generator_count<>161 or
   D972NKBV2Obj.rs_relator_count<>5056 or D972NKBV2Obj.norm_count<>972 then
  Error("norm Tietze KBMAG v2: artifact pin/count gate failed");
fi;
if D972NKBV2Obj.rs_pair_words_sha256<>D972NKBV2PairSha or
   Length(D972NKBV2Obj.rs_pair_words)<>161 or
   D972NKBV2Obj.rs_relators_sha256<>D972NKBV2RawRsSha or
   D972NKBV2Obj.norm_rs_words_sha256<>D972NKBV2NormRsSha then
  Error("norm Tietze KBMAG v2: raw/norm RS basis digest drift");
fi;
if not IsInt(D972NKBV2Obj.final_generator_count) or
   D972NKBV2Obj.final_generator_count<=0 or
   D972NKBV2Obj.final_generator_count>127 or
   Length(D972NKBV2Obj.final_relators)=0 or
   Length(D972NKBV2Obj.final_norm_words)<>972 then
  Error("norm Tietze KBMAG v2: final dense artifact gate failed");
fi;
D972NKBV2N := D972NKBV2Obj.final_generator_count;;
for D972NKBV2W in D972NKBV2Obj.final_relators do
  if not IsList(D972NKBV2W) or
     ForAny(D972NKBV2W,x->x=0 or not IsInt(x) or AbsInt(x)>D972NKBV2N) then
    Error("norm Tietze KBMAG v2: final relator alphabet drift");
  fi;
od;
for D972NKBV2W in D972NKBV2Obj.final_norm_words do
  if not IsList(D972NKBV2W) or
     ForAny(D972NKBV2W,x->x=0 or not IsInt(x) or AbsInt(x)>D972NKBV2N) then
    Error("norm Tietze KBMAG v2: final norm alphabet drift");
  fi;
od;
if D972NKBV2Digest(D972NKBV2Obj.final_relators)<>
   D972NKBV2Obj.final_relators_sha256 or
   D972NKBV2DigestRows(D972NKBV2Obj.final_norm_words)<>
   D972NKBV2Obj.final_norm_words_sha256 then
  Error("norm Tietze KBMAG v2: final digest mismatch");
fi;
Print("B4_NORM_TZ_KBMAG_V2_INPUT_PASS raw_rs=161/5056 norm=972 final_generators=",
  D972NKBV2N," raw_rs_sha256=",D972NKBV2RawRsSha,
  " norm_rs_sha256=",D972NKBV2NormRsSha,"\n");

D972NKBV2F:=FreeGroup(D972NKBV2N);;
D972NKBV2FG:=GeneratorsOfGroup(D972NKBV2F);;
D972NKBV2Rels:=List(D972NKBV2Obj.final_relators,
  w->D972NKBV2SignedWord(w,D972NKBV2FG));;
D972NKBV2G:=D972NKBV2F/D972NKBV2Rels;;
D972NKBV2GG:=GeneratorsOfGroup(D972NKBV2G);;
D972NKBV2Rws:=KBMAGRewritingSystem(D972NKBV2G);;
SetOrderingOfKBMAGRewritingSystem(D972NKBV2Rws,"shortlex");;
D972NKBV2Opts:=OptionsRecordOfKBMAGRewritingSystem(D972NKBV2Rws);;
D972NKBV2Opts.maxeqns:=D972NKBV2MaxEqns;;
D972NKBV2Opts.maxstates:=D972NKBV2MaxStates;;
D972NKBV2Opts.maxwdiffs:=D972NKBV2MaxWdiffs;;
D972NKBV2Opts.maxstoredlen:=D972NKBV2MaxStored;;
Print("B4_NORM_TZ_KBMAG_V2_BEGIN maxeqns=",D972NKBV2MaxEqns,
  " maxstates=",D972NKBV2MaxStates," maxwdiffs=",D972NKBV2MaxWdiffs,"\n");
KnuthBendix(D972NKBV2Rws);;
D972NKBV2Reduced:=IsBound(D972NKBV2Rws!.reduced) and
  D972NKBV2Rws!.reduced=true;;
D972NKBV2Bits:=[];;
if D972NKBV2Reduced then
  for D972NKBV2I in [1..972] do
    D972NKBV2RW:=ReducedForm(D972NKBV2Rws,
      D972NKBV2SignedWord(D972NKBV2Obj.final_norm_words[D972NKBV2I],D972NKBV2GG));;
    Add(D972NKBV2Bits,IsOne(D972NKBV2RW));;
  od;
fi;
D972NKBV2Zero:=Number(D972NKBV2Bits,x->x=false);;
if Length(D972NKBV2Bits)=972 and D972NKBV2Zero=0 then
  D972NKBV2Status:="ALL_972_EMPTY_CANDIDATE_NEEDS_REPLAY";
elif Length(D972NKBV2Bits)=972 then
  D972NKBV2Status:="B4_A_SIDE_CANDIDATE_NEEDS_REPLAY";
else
  D972NKBV2Status:="UNKNOWN_NO_COMPLETE_REDUCTION";
fi;
D972NKBV2Receipt:=D972NKBV2Json(rec(
  schema:="d972-b4-norm-tietze-kbmag/v2",status:=D972NKBV2Status,
  artifact_sha256:=HexSHA256(D972NKBV2Raw),
  artifact_schema:=D972NKBV2Obj.schema,
  source_sha256:=D972NKBV2SourceSha,relator_sha256:=D972NKBV2RelSha,
  raw_rs_sha256:=D972NKBV2RawRsSha,norm_rs_sha256:=D972NKBV2NormRsSha,
  final_generator_count:=D972NKBV2N,norm_count:=972,
  reduced_available:=D972NKBV2Reduced,reduced_count:=Length(D972NKBV2Bits),
  roof_bits:=D972NKBV2Bits,roof_zero_count:=D972NKBV2Zero,
  maxeqns:=D972NKBV2MaxEqns,maxstates:=D972NKBV2MaxStates,
  maxwdiffs:=D972NKBV2MaxWdiffs,maxstored:=D972NKBV2MaxStored,
  proof_level:="KBMAG_CANDIDATE_INDEPENDENT_TZ_REPLAY_REQUIRED"));;
D972NKBV2Out:=OutputTextFile(D972NKBV2Output,false);;
SetPrintFormattingStatus(D972NKBV2Out,false);;
PrintTo(D972NKBV2Out,Concatenation(D972NKBV2Receipt,"\n"));;
CloseStream(D972NKBV2Out);;
Print("B4_NORM_TZ_KBMAG_V2_FINAL_MARKER status=",D972NKBV2Status,
  " reduced=",Length(D972NKBV2Bits)," zero=",D972NKBV2Zero,
  " output=",D972NKBV2Output,"\n");
