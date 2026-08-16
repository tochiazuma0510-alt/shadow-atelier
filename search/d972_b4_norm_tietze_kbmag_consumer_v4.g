#############################################################################
## d972_b4_norm_tietze_kbmag_consumer_v4.g
##
## Versioned KBMAG consumer for the independently checked 100-step/61-
## generator canonical Tietze receipt.  This is a candidate lane only:
## KBMAG has no ancestry back to the 158 source relators here.
## There is deliberately no QUIT; generic gap-run reads this file.
#############################################################################

if LoadPackage("json") <> true then
  Error("norm Tietze KBMAG v4: json package unavailable");
fi;
if LoadPackage("kbmag") <> true then
  Error("norm Tietze KBMAG v4: kbmag package unavailable");
fi;

D972NKBV4Input := "ci/out/d972_b4_norm_tietze_trace_v4.json";;
D972NKBV4Output := "ci/out/d972_b4_norm_tietze_kbmag_v4.json";;
if IsBound(D972_B4_NORM_TZ_ARTIFACT) then
  D972NKBV4Input := D972_B4_NORM_TZ_ARTIFACT;
fi;
if IsBound(D972_B4_NORM_TZ_KBMAG_OUTPUT) then
  D972NKBV4Output := D972_B4_NORM_TZ_KBMAG_OUTPUT;
fi;
D972NKBV4MaxEqns := 50000;;
D972NKBV4MaxStates := 50000;;
D972NKBV4MaxWdiffs := 50000;;
D972NKBV4MaxStored := [100,100];;
if IsBound(D972_B4_NORM_TZ_MAXEQNS) then D972NKBV4MaxEqns:=D972_B4_NORM_TZ_MAXEQNS; fi;
if IsBound(D972_B4_NORM_TZ_MAXSTATES) then D972NKBV4MaxStates:=D972_B4_NORM_TZ_MAXSTATES; fi;
if IsBound(D972_B4_NORM_TZ_MAXWDIFFS) then D972NKBV4MaxWdiffs:=D972_B4_NORM_TZ_MAXWDIFFS; fi;
if IsBound(D972_B4_NORM_TZ_MAXSTORED) then D972NKBV4MaxStored:=D972_B4_NORM_TZ_MAXSTORED; fi;
if not IsInt(D972NKBV4MaxEqns) or D972NKBV4MaxEqns<=0 or
   not IsInt(D972NKBV4MaxStates) or D972NKBV4MaxStates<=0 or
   not IsInt(D972NKBV4MaxWdiffs) or D972NKBV4MaxWdiffs<=0 or
   not IsList(D972NKBV4MaxStored) or Length(D972NKBV4MaxStored)<>2 then
  Error("norm Tietze KBMAG v4: numeric cap drift");
fi;

D972NKBV4SourceSha :=
  "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972NKBV4RelSha :=
  "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972NKBV4RowsSha :=
  "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930";;
D972NKBV4NormSha :=
  "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972NKBV4WordArtifactSha :=
  "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972NKBV4BasisId := "f2^5-positive-transversal-mask-order-v1";;
D972NKBV4PairSha :=
  "2be7ef40bbe19177a9777774e3685c4b5f564466a1f65fc55d5466b6dc34ca7e";;
D972NKBV4RawRsSha :=
  "29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e";;
D972NKBV4NormRsSha :=
  "f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8";;
D972NKBV4FinalRelSha :=
  "2327388540e9095b2c7ca9b6d0d1f9de2295e3400b0430bdf97b672d02ce745";;
D972NKBV4FinalNormSha :=
  "325aecb390f4c8107a92be3cca8ed16f396f1baec49b973488f8822b43bf4d70";;

D972NKBV4Join := function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1];;
  for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972NKBV4Json := function(x)
  local p,i,names;
  ## In GAP 4.16 [] also satisfies IsString; empty lists must come first.
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if IsInt(x) then return String(x); fi;
  if IsRecord(x) then
    names:=SortedList(RecNames(x));;
    p:=List(names,i->Concatenation("\"",i,"\":",D972NKBV4Json(x.(i))));;
    return Concatenation("{",D972NKBV4Join(p,","),"}");
  fi;
  if not IsList(x) then Error("norm Tietze KBMAG v4: JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972NKBV4Json(x[i]));;
  return Concatenation("[",D972NKBV4Join(p,","),"]");
end;;
D972NKBV4Reduce := function(w)
  local out,x;
  out:=[];;
  for x in w do
    if Length(out)>0 and Last(out)=-x then Remove(out);
    else Add(out,x); fi;
  od;
  return out;
end;;
D972NKBV4Canonical := function(rows)
  local out,w;
  out:=[];;
  for w in rows do
    w:=D972NKBV4Reduce(w);;
    if Length(w)>0 then Add(out,w); fi;
  od;
  Sort(out);;
  return out;
end;;
D972NKBV4Digest := function(rows)
  return HexSHA256(D972NKBV4Json(D972NKBV4Canonical(rows)));
end;;
D972NKBV4DigestRows := function(rows)
  return HexSHA256(D972NKBV4Json(List(rows,D972NKBV4Reduce)));
end;;
D972NKBV4SignedWord := function(row,gens)
  local z,a;
  z:=One(gens[1]);;
  for a in row do
    if a>0 then z:=z*gens[a]; else z:=z*gens[-a]^-1; fi;
  od;
  return z;
end;;

D972NKBV4Raw := StringFile(D972NKBV4Input);;
if D972NKBV4Raw=fail then Error("norm Tietze KBMAG v4: artifact missing"); fi;
D972NKBV4Obj := JsonStringToGap(D972NKBV4Raw);;
if not IsRecord(D972NKBV4Obj) or
   D972NKBV4Obj.schema<>"d972-b4-norm-tietze-trace/v4" or
   D972NKBV4Obj.trace_base_schema<>"d972-b4-norm-tietze-trace/v2" or
   D972NKBV4Obj.source_sha256<>D972NKBV4SourceSha or
   D972NKBV4Obj.relator_sha256<>D972NKBV4RelSha or
   D972NKBV4Obj.normalized_rows_sha256<>D972NKBV4RowsSha or
   D972NKBV4Obj.roof_norm_words_sha256<>D972NKBV4NormSha or
   D972NKBV4Obj.word_artifact_sha256<>D972NKBV4WordArtifactSha or
   D972NKBV4Obj.basis_id<>D972NKBV4BasisId or
   D972NKBV4Obj.gen_bits<>[1,2,4,8,16,31] or
   D972NKBV4Obj.rs_generator_count<>161 or
   D972NKBV4Obj.rs_relator_count<>5056 or D972NKBV4Obj.norm_count<>972 or
   D972NKBV4Obj.max_steps<>100 or
   D972NKBV4Obj.dense_target_max_generators<>61 or
   Length(D972NKBV4Obj.events)<>100 or
   D972NKBV4Obj.final_generator_count<>61 or
   D972NKBV4Obj.final_generator_count>63 or
   D972NKBV4Obj.final_relators_sha256<>D972NKBV4FinalRelSha or
   D972NKBV4Obj.final_norm_words_sha256<>D972NKBV4FinalNormSha then
  Error("norm Tietze KBMAG v4: source/trace pin failed");
fi;
if D972NKBV4Obj.rs_pair_words_sha256<>D972NKBV4PairSha or
   Length(D972NKBV4Obj.rs_pair_words)<>161 or
   D972NKBV4Obj.rs_relators_sha256<>D972NKBV4RawRsSha or
   D972NKBV4Obj.norm_rs_words_sha256<>D972NKBV4NormRsSha then
  Error("norm Tietze KBMAG v4: raw/norm RS basis digest drift");
fi;
if Length(D972NKBV4Obj.final_relators)=0 or
   Length(D972NKBV4Obj.final_norm_words)<>972 then
  Error("norm Tietze KBMAG v4: final dense artifact count drift");
fi;
D972NKBV4N := D972NKBV4Obj.final_generator_count;;
for D972NKBV4W in D972NKBV4Obj.final_relators do
  if not IsList(D972NKBV4W) or
     ForAny(D972NKBV4W,x->x=0 or not IsInt(x) or AbsInt(x)>D972NKBV4N) then
    Error("norm Tietze KBMAG v4: final relator alphabet drift");
  fi;
od;
for D972NKBV4W in D972NKBV4Obj.final_norm_words do
  if not IsList(D972NKBV4W) or
     ForAny(D972NKBV4W,x->x=0 or not IsInt(x) or AbsInt(x)>D972NKBV4N) then
    Error("norm Tietze KBMAG v4: final norm alphabet drift");
  fi;
od;
if D972NKBV4Digest(D972NKBV4Obj.final_relators)<>D972NKBV4FinalRelSha or
   D972NKBV4DigestRows(D972NKBV4Obj.final_norm_words)<>D972NKBV4FinalNormSha then
  Error("norm Tietze KBMAG v4: final digest mismatch");
fi;
Print("B4_NORM_TZ_KBMAG_V4_INPUT_PASS raw_rs=161/5056 norm=972 final_generators=",
  D972NKBV4N,"\n");

D972NKBV4F:=FreeGroup(D972NKBV4N);;
D972NKBV4FG:=GeneratorsOfGroup(D972NKBV4F);;
D972NKBV4Rels:=List(D972NKBV4Obj.final_relators,
  w->D972NKBV4SignedWord(w,D972NKBV4FG));;
D972NKBV4G:=D972NKBV4F/D972NKBV4Rels;;
D972NKBV4GG:=GeneratorsOfGroup(D972NKBV4G);;
D972NKBV4Rws:=KBMAGRewritingSystem(D972NKBV4G);;
SetOrderingOfKBMAGRewritingSystem(D972NKBV4Rws,"shortlex");;
D972NKBV4Opts:=OptionsRecordOfKBMAGRewritingSystem(D972NKBV4Rws);;
D972NKBV4Opts.maxeqns:=D972NKBV4MaxEqns;;
D972NKBV4Opts.maxstates:=D972NKBV4MaxStates;;
D972NKBV4Opts.maxwdiffs:=D972NKBV4MaxWdiffs;;
D972NKBV4Opts.maxstoredlen:=D972NKBV4MaxStored;;
Print("B4_NORM_TZ_KBMAG_V4_BEGIN maxeqns=",D972NKBV4MaxEqns,
  " maxstates=",D972NKBV4MaxStates," maxwdiffs=",D972NKBV4MaxWdiffs,"\n");
KnuthBendix(D972NKBV4Rws);;
D972NKBV4Reduced:=IsBound(D972NKBV4Rws!.reduced) and
  D972NKBV4Rws!.reduced=true;;
D972NKBV4Bits:=[];;
if D972NKBV4Reduced then
  for D972NKBV4I in [1..972] do
    D972NKBV4RW:=ReducedForm(D972NKBV4Rws,
      D972NKBV4SignedWord(D972NKBV4Obj.final_norm_words[D972NKBV4I],D972NKBV4GG));;
    Add(D972NKBV4Bits,IsOne(D972NKBV4RW));;
  od;
fi;
D972NKBV4Zero:=Number(D972NKBV4Bits,x->x=false);;
if Length(D972NKBV4Bits)=972 and D972NKBV4Zero=0 then
  D972NKBV4Status:="ALL_972_EMPTY_CANDIDATE_NEEDS_REPLAY";
elif Length(D972NKBV4Bits)=972 then
  D972NKBV4Status:="B4_A_SIDE_CANDIDATE_NEEDS_REPLAY";
else
  D972NKBV4Status:="UNKNOWN_NO_COMPLETE_REDUCTION";
fi;
D972NKBV4Receipt:=D972NKBV4Json(rec(
  schema:="d972-b4-norm-tietze-kbmag/v4",status:=D972NKBV4Status,
  artifact_sha256:=HexSHA256(D972NKBV4Raw),
  artifact_schema:=D972NKBV4Obj.schema,
  source_sha256:=D972NKBV4SourceSha,relator_sha256:=D972NKBV4RelSha,
  raw_rs_sha256:=D972NKBV4RawRsSha,norm_rs_sha256:=D972NKBV4NormRsSha,
  final_relators_sha256:=D972NKBV4FinalRelSha,
  final_norm_words_sha256:=D972NKBV4FinalNormSha,
  final_generator_count:=D972NKBV4N,stock_max_generators:=63,norm_count:=972,
  reduced_available:=D972NKBV4Reduced,reduced_count:=Length(D972NKBV4Bits),
  roof_bits:=D972NKBV4Bits,roof_zero_count:=D972NKBV4Zero,
  maxeqns:=D972NKBV4MaxEqns,maxstates:=D972NKBV4MaxStates,
  maxwdiffs:=D972NKBV4MaxWdiffs,maxstored:=D972NKBV4MaxStored,
  proof_level:="KBMAG_CANDIDATE_INDEPENDENT_TZ_REPLAY_REQUIRED"));;
D972NKBV4Out:=OutputTextFile(D972NKBV4Output,false);;
SetPrintFormattingStatus(D972NKBV4Out,false);;
PrintTo(D972NKBV4Out,Concatenation(D972NKBV4Receipt,"\n"));;
CloseStream(D972NKBV4Out);;
Print("B4_NORM_TZ_KBMAG_V4_FINAL_MARKER status=",D972NKBV4Status,
  " reduced=",Length(D972NKBV4Bits)," zero=",D972NKBV4Zero,
  " output=",D972NKBV4Output,"\n");
