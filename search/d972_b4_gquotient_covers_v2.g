#############################################################################
## d972_b4_gquotient_covers_v2.g
##
## Exact-artifact finite-image lane for B4-A.  Unlike the exploratory v1
## driver, this version does not load a drifting worker/p-quotient prefix.
## It consumes a GAP data file generated from the pinned
## d972-b4-p2-magnus-input artifact and constructs exactly
##
##       U_M = F_6 / << 158 signed relators >>.
##
## All 972 roof words, target keys, and relator/norm digests are checked
## before GQuotients.  A defect receipt contains explicit permutation images
## and is independently replayed by check_d972_b4_finite_image_v2.py.
##
## Mode is supplied as a GAP global by a tiny wrapper:
##   D972_B4_GQ_MODE:="selftest";;  (default if absent)
##   D972_B4_GQ_MODE:="target";; D972_B4_GQ_TARGET:="SL2_3";;
##   D972_B4_GQ_TARGET_INDEX:=7;;  (closed 1..12 numeric table)
##   D972_B4_GQ_SELFTEST:=1;;     (numeric selftest override)
#############################################################################

if not IsBound(GetEnv) then GetEnv := name -> fail; fi;
D972GQ2JsonPackage:=LoadPackage("json");;
D972GQ2Mode:=fail;;
if IsBound(D972_B4_GQ_MODE) then D972GQ2Mode:=D972_B4_GQ_MODE; fi;
if D972GQ2Mode=fail then D972GQ2Mode:=GetEnv("D972_B4_GQ_MODE"); fi;
if D972GQ2Mode=fail or D972GQ2Mode="" then D972GQ2Mode:="selftest"; fi;
D972GQ2Target:=fail;;
D972GQ2StringTarget:=fail;;
D972GQ2StringTargetExplicit:=false;;
if IsBound(D972_B4_GQ_TARGET) then
  D972GQ2StringTarget:=D972_B4_GQ_TARGET;;
  D972GQ2StringTargetExplicit:=true;;
fi;
if D972GQ2StringTarget=fail then
  D972GQ2StringTarget:=GetEnv("D972_B4_GQ_TARGET");
  if D972GQ2StringTarget<>fail and D972GQ2StringTarget<>"" then
    D972GQ2StringTargetExplicit:=true;;
  fi;
fi;
D972GQ2StringTargetWasEmpty:=
  D972GQ2StringTarget=fail or D972GQ2StringTarget="";;
if D972GQ2StringTargetWasEmpty then D972GQ2StringTarget:="SL2_3"; fi;

## Numeric target selection is deliberately a closed table.  SL2(8)=PSL2(8)
## (because gcd(2,8-1)=1), so the redundant SL2_8 string target remains
## accepted for backwards compatibility but is not assigned a numeric shard.
D972GQ2NumericLabels:=[
  "SL2_3","GL2_3","SL2_4","GL2_4","SL2_5","GL2_5",
  "SL2_7","GL2_7","PSL2_7","PGL2_7","PSL2_8","PGL2_8"];;
D972GQ2TargetIndex:=fail;; D972GQ2NumericIndexSet:=false;;
if IsBound(D972_B4_GQ_TARGET_INDEX) then
  D972GQ2TargetIndex:=D972_B4_GQ_TARGET_INDEX;;
  D972GQ2NumericIndexSet:=true;;
else
  D972GQ2TargetIndexEnv:=GetEnv("D972_B4_GQ_TARGET_INDEX");;
  if D972GQ2TargetIndexEnv<>fail and D972GQ2TargetIndexEnv<>"" then
    D972GQ2TargetIndex:=Int(D972GQ2TargetIndexEnv);;
    D972GQ2NumericIndexSet:=true;;
  fi;
fi;
if D972GQ2NumericIndexSet then
  if not IsInt(D972GQ2TargetIndex) or
     D972GQ2TargetIndex<1 or D972GQ2TargetIndex>Length(D972GQ2NumericLabels) then
    Error("GQ2 numeric target index drift (expected 1..12)");
  fi;
  D972GQ2Target:=D972GQ2NumericLabels[D972GQ2TargetIndex];;
  if D972GQ2StringTargetExplicit and
     D972GQ2StringTarget<>D972GQ2Target then
    Error("GQ2 numeric/string target disagreement");
  fi;
  ## A numeric selector is a complete target request; no quoted mode is
  ## needed in a workflow preamble.  An explicit selftest still wins below.
  D972GQ2Mode:="target";;
  Print("B4_GQ2_TARGET_INDEX_PASS index=",D972GQ2TargetIndex,
    " label=",D972GQ2Target," count=12\n");
fi;
D972GQ2SelftestNumeric:=0;;
if IsBound(D972_B4_GQ_SELFTEST) then D972GQ2SelftestNumeric:=D972_B4_GQ_SELFTEST; fi;
if not IsInt(D972GQ2SelftestNumeric) or
   (D972GQ2SelftestNumeric<>0 and D972GQ2SelftestNumeric<>1) then
  Error("GQ2 numeric selftest flag drift");
fi;
if D972GQ2SelftestNumeric=1 then D972GQ2Mode:="selftest"; fi;
if not D972GQ2NumericIndexSet then D972GQ2Target:=D972GQ2StringTarget; fi;
D972GQ2Input:=fail;;
if IsBound(D972_B4_GQ_INPUT) then D972GQ2Input:=D972_B4_GQ_INPUT; fi;
if D972GQ2Input=fail then D972GQ2Input:=GetEnv("D972_B4_GQ_INPUT"); fi;
D972GQ2Output:=fail;;
if IsBound(D972_B4_GQ_OUTPUT) then D972GQ2Output:=D972_B4_GQ_OUTPUT; fi;
if D972GQ2Output=fail then D972GQ2Output:=GetEnv("D972_B4_GQ_OUTPUT"); fi;
if D972GQ2Output=fail or D972GQ2Output="" then
  D972GQ2Output:=Filename(DirectoryTemporary(),"d972_b4_gquotient_v2.json");
fi;
D972GQ2ReceiptOutput:=Concatenation(D972GQ2Output,".defect.json");;
D972ExactRelWords:=fail;; D972ExactRoofWords:=fail;;
D972ExactTargetKeys:=fail;; D972ExactRelDigest:=fail;;
D972ExactRoofDigest:=fail;; D972ExactTargetDigest:=fail;;
D972ExactWordKeyDigest:=fail;; D972ExactSourceSha256:=fail;;
D972ExactLegacyRhoWords:=fail;;
D972GQ2CanonicalRho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;
D972GQ2LegacyRhoMismatch:=false;;
D972GQ2CanonicalRhoDigest:="23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed";;
D972GQ2CorrectedSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;

D972GQ2Join:=function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;
  out:=xs[1];;
  for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  return out;
end;;
D972GQ2Json:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\"");
  fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("GQ2 JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972GQ2Json(x[i]));;
  return Concatenation("[",D972GQ2Join(p,","),"]");
end;;
D972GQ2Write:=function(path,s)
  local f;
  f:=OutputTextFile(path,false);;
  SetPrintFormattingStatus(f,false);;
  PrintTo(f,Concatenation(s,"\n"));;
  CloseStream(f);;
end;;

## The terminal input is the corrected, versioned JSON artifact.  The old
## generated GAP bridge and v1 JSON are intentionally rejected here; they are
## retained only as historical exploratory inputs outside this terminal lane.
D972GQ2LoadInput:=function()
  local src,obj,sourceSha;
  if D972GQ2Input=fail or D972GQ2Input="" then
    Error("GQ2 exact input path is required");
  fi;
  if PositionSublist(D972GQ2Input,".json")=fail then
    Error("GQ2 terminal requires corrected JSON input, not GAP bridge");
  fi;
  if LoadPackage("json")<>true then
    Error("GQ2 json package unavailable for direct input");
  fi;
  src:=StringFile(D972GQ2Input);;
  if src=fail then Error("GQ2 direct JSON input missing"); fi;
  sourceSha:=HexSHA256(src);;
  if sourceSha<>D972GQ2CorrectedSourceSha then
    Error("GQ2 corrected JSON source SHA drift: ",sourceSha);
  fi;
  obj:=JsonStringToGap(src);;
  if not IsRecord(obj) or obj.schema<>"d972-b4-p2-magnus-input/v2" then
    Error("GQ2 corrected JSON schema drift");
  fi;
  if obj.rho_words<>D972GQ2CanonicalRho or
     (IsBound(obj.rho_words_sha256) and
      obj.rho_words_sha256<>D972GQ2CanonicalRhoDigest) or
     not IsBound(obj.rho_words_source) or
     obj.rho_words_source<>"universal_v2_canonical" then
    Error("GQ2 corrected JSON canonical rho drift");
  fi;
  D972ExactRelWords:=obj.all_relators;;
  D972ExactRoofWords:=obj.roof_words;;
  D972ExactTargetKeys:=obj.target_keys;;
  D972ExactRelDigest:=obj.all_relators_sha256;;
  D972ExactRoofDigest:=obj.roof_words_sha256;;
  D972ExactTargetDigest:=obj.target_key_digest;;
  D972ExactLegacyRhoWords:=obj.rho_words;;
  D972ExactWordKeyDigest:="283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930";;
  D972ExactSourceSha256:=sourceSha;;
end;;

## Read the pinned data file and recompute its three public digests.  This
## inexpensive lane is intentionally separate from GQuotients: it catches a
## stale/generated GAP bridge before any target enumeration is attempted.
D972GQ2InputAudit:=function()
  local keys,sorted,joined,i;
  if D972GQ2Input=fail or D972GQ2Input="" then
    Error("GQ2 input-audit exact input GAP data path is required");
  fi;
  D972GQ2LoadInput();;
  if not IsBound(D972ExactRelWords) or not IsBound(D972ExactRoofWords) or
     not IsBound(D972ExactTargetKeys) then
    Error("GQ2 input-audit variables missing");
  fi;
  if Length(D972ExactRelWords)<>158 or Length(D972ExactRoofWords)<>972 or
     Length(D972ExactTargetKeys)<>972 then
    Error("GQ2 input-audit count drift");
  fi;
  if not IsBound(D972ExactSourceSha256) or
     D972ExactSourceSha256<>D972GQ2CorrectedSourceSha then
    Error("GQ2 source JSON SHA drift");
  fi;
  if D972ExactRelDigest<>"12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e" or
     D972ExactRoofDigest<>"3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8" or
     D972ExactTargetDigest<>"9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62" or
     D972ExactWordKeyDigest<>"283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930" then
    Error("GQ2 input-audit digest metadata drift");
  fi;
  if D972ExactLegacyRhoWords<>fail then
    if D972ExactLegacyRhoWords=D972GQ2CanonicalRho then
      D972GQ2LegacyRhoMismatch:=false;;
      Print("B4_GQ2_RHO_FIELD_NOTE legacy_json_rho_mismatch=false canonical_json_rho=true\n");
    else
      Error("GQ2 JSON rho field is not the canonical universal_v2 map");
    fi;
  fi;
  if HexSHA256(D972GQ2Json(D972ExactRelWords))<>D972ExactRelDigest then
    Error("GQ2 recomputed relator digest drift: ",
      HexSHA256(D972GQ2Json(D972ExactRelWords)));
  fi;
  if HexSHA256(D972GQ2Json(D972ExactRoofWords))<>D972ExactRoofDigest then
    Error("GQ2 recomputed roof digest drift: ",
      HexSHA256(D972GQ2Json(D972ExactRoofWords)));
  fi;
  keys:=ShallowCopy(D972ExactTargetKeys);; Sort(keys);; joined:="";;
  for i in [1..Length(keys)] do joined:=Concatenation(joined,keys[i],"\n"); od;
  if HexSHA256(joined)<>D972ExactTargetDigest then
    Error("GQ2 recomputed target-key digest drift: ",HexSHA256(joined));
  fi;
  Print("B4_GQ2_INPUT_AUDIT_PASS source_sha256=",D972ExactSourceSha256,
    " relator_digest=",HexSHA256(D972GQ2Json(D972ExactRelWords)),
    " roof_digest=",HexSHA256(D972GQ2Json(D972ExactRoofWords)),
    " target_digest=",HexSHA256(joined),"\n");
end;;

## Six-generator signed-word evaluator.  This is deliberately independent
## from P2Roof and is used for both rho images and exact norm defects.
D972GQ2Eval:=function(w,row)
  local q,v;
  q:=One(row[1]);;
  for v in w do
    if v>0 then q:=q*row[v]; else q:=q*row[-v]^-1; fi;
  od;
  return q;
end;;
D972GQ2SelfTest:=function()
  local h,w,good,bad;
  h:=[(1,2),Identity(SymmetricGroup(3)),
    Identity(SymmetricGroup(3)),(1,2,3),
    Identity(SymmetricGroup(3)),Identity(SymmetricGroup(3))];;
  ## The canonical F2 y image is slot 4; slot 2 is deliberately different.
  good:=h[4];;
  bad:=h[2];;
  if good=bad then Error("GQ2 asymmetric y/U4 canary failed"); fi;
  Print("B4_GQ2_SELFTEST_PASS asymmetric_y_U4=true\n");
end;;

if D972GQ2Mode="selftest" then
  D972GQ2SelfTest();;
  if D972GQ2NumericIndexSet then
    Print("B4_GQ2_SELFTEST_FINAL_MARKER index=",D972GQ2TargetIndex,
      " label=",D972GQ2Target," numeric=true\n");
  else
    Print("B4_GQ2_SELFTEST_FINAL_MARKER index=none label=",D972GQ2Target,
      " numeric=false\n");
  fi;
elif D972GQ2Mode="input_audit" then
  D972GQ2InputAudit();;
  if D972GQ2NumericIndexSet then
    Print("B4_GQ2_INPUT_AUDIT_FINAL_MARKER index=",D972GQ2TargetIndex,
      " label=",D972GQ2Target," numeric=true\n");
  else
    Print("B4_GQ2_INPUT_AUDIT_FINAL_MARKER index=none label=",D972GQ2Target,
      " numeric=false\n");
  fi;
else

D972GQ2InputAudit();;

## Target constructors.  Matrix groups are converted to permutation groups
## so GQuotients and the independent JSON checker use one concrete model.
D972GQ2TargetGroup:=function(label)
  local G,iso,Gp,ord;
  if label="SL2_3" then G:=SL(2,3);
  elif label="GL2_3" then G:=GL(2,3);
  elif label="SL2_4" then G:=SL(2,4);
  elif label="GL2_4" then G:=GL(2,4);
  elif label="SL2_5" then G:=SL(2,5);
  elif label="GL2_5" then G:=GL(2,5);
  elif label="SL2_7" then G:=SL(2,7);
  elif label="GL2_7" then G:=GL(2,7);
  elif label="SL2_8" then G:=SL(2,8);
  elif label="PSL2_7" then G:=PSL(2,7);
  elif label="PGL2_7" then G:=PGL(2,7);
  elif label="PSL2_8" then G:=PSL(2,8);
  elif label="PGL2_8" then G:=PGL(2,8);
  else Error("GQ2 unknown target: ",label);
  fi;
  ord:=Size(G);;
  iso:=IsomorphismPermGroup(G);;
  if iso=fail then Error("GQ2 target permutation conversion failed"); fi;
  Gp:=Image(iso);;
  if Size(Gp)<>ord then Error("GQ2 target order drift"); fi;
  return rec(group:=Gp,order:=ord,degree:=LargestMovedPoint(Gp));
end;;

D972GQ2LoadInput();;
if not IsBound(D972ExactRelWords) or not IsBound(D972ExactRoofWords) then
  Error("GQ2 exact input variables missing");
fi;
if Length(D972ExactRelWords)<>158 or Length(D972ExactRoofWords)<>972 then
  Error("GQ2 exact input counts drift");
fi;
if D972ExactRelDigest<>"12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e" then
  Error("GQ2 relator digest metadata drift");
fi;
if D972ExactRoofDigest<>"3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8" then
  Error("GQ2 roof-word digest metadata drift");
fi;
if D972ExactTargetDigest<>"9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62" then
  Error("GQ2 target digest metadata drift");
fi;

F6GQ2:=FreeGroup(6);; G6GQ2:=GeneratorsOfGroup(F6GQ2);;
D972GQ2SignedWord:=function(a)
  local w,v;
  w:=One(G6GQ2[1]);;
  for v in a do
    if v>0 then w:=w*G6GQ2[v]; else w:=w*G6GQ2[-v]^-1; fi;
  od;
  return w;
end;;
RelsGQ2:=List(D972ExactRelWords,D972GQ2SignedWord);;
UfpGQ2:=F6GQ2/RelsGQ2;; UgensGQ2:=GeneratorsOfGroup(UfpGQ2);;
if Length(UgensGQ2)<>6 then Error("GQ2 U generator count drift"); fi;
RhoGQ2:=D972GQ2CanonicalRho;;
RhoFreeGQ2:=List(RhoGQ2,D972GQ2SignedWord);;
## Rebuild exact norm rows as signed integers for digest/evaluation.
NormRowsGQ2:=[];;
for D972RoofWord in D972ExactRoofWords do
  jf:=One(G6GQ2[1]);;
  for D972Letter in D972RoofWord do
    if D972Letter=1 then jf:=jf*G6GQ2[1];
    elif D972Letter=-1 then jf:=jf*G6GQ2[1]^-1;
    elif D972Letter=2 then jf:=jf*G6GQ2[4];
    elif D972Letter=-2 then jf:=jf*G6GQ2[4]^-1;
    else Error("GQ2 roof word is not F2"); fi;
  od;
  orb:=[];; v:=jf;;
  for D972T in [1..5] do Add(orb,v);; v:=MappedWord(v,G6GQ2,RhoFreeGQ2); od;
  z:=One(G6GQ2[1]);;
  for D972T in Reversed([1..5]) do z:=z*orb[D972T]; od;
  Add(NormRowsGQ2,ExtRepOfObj(z));;
od;
## Convert ExtRep rows deterministically to signed lists.
D972GQ2ExtToSigned:=function(e)
  local out,i,g,n,j;
  out:=[];; i:=1;;
  while i<=Length(e) do
    g:=e[i];; n:=e[i+1];;
    if n>0 then for j in [1..n] do Add(out,g); od;
    else for j in [1..-n] do Add(out,-g); od; fi;
    i:=i+2;
  od;
  return out;
end;;
NormRowsGQ2:=List(NormRowsGQ2,D972GQ2ExtToSigned);;
NormDigestGQ2:=HexSHA256(D972GQ2Json(NormRowsGQ2));;
if NormDigestGQ2<>"ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e" then
  Error("GQ2 exact norm digest drift: ",NormDigestGQ2);
fi;
Print("B4_GQ2_INPUT_PASS relators=158 roof=972 norm_digest=",NormDigestGQ2,
  " relator_digest=",D972ExactRelDigest," target_digest=",D972ExactTargetDigest,"\n");

D972GQ2Scan:=function(epi)
  local h0,hp,t,r,one,bad,fails,first,z,valid;
  h0:=List(UgensGQ2,g->Image(epi,g));;
  hp:=[];; Add(hp,h0);;
  for t in [1..4] do Add(hp,List([1..6],r->D972GQ2Eval(RhoGQ2[r],hp[t]))); od;
  one:=One(h0[1]);; bad:=[];;
  for t in [1..5] do for r in D972ExactRelWords do
    if D972GQ2Eval(r,hp[t])<>one then Add(bad,[t,Position(D972ExactRelWords,r)]); fi;
  od; od;
  if List([1..6],r->D972GQ2Eval(RhoGQ2[r],hp[5]))<>h0 then
    Error("GQ2 rho^5 image failure");
  fi;
  valid:=Length(bad)=0;;
  fails:=[];; first:=fail;;
  for t in [1..Length(NormRowsGQ2)] do
    z:=D972GQ2Eval(NormRowsGQ2[t],h0);;
    if z<>one and valid then
      Add(fails,t);;
      if first=fail then first:=rec(index:=t,word:=D972ExactRoofWords[t],defect:=z); fi;
    fi;
  od;
  return rec(h0:=h0,relator_bad:=bad,fails:=fails,first:=first,rho5:=true,
    valid:=valid);
end;;

D972GQ2Receipt:=function(label,order,scan,epiIndex,epiCount)
  local H,iso,Hp,degree,wit,defect;
  H:=Group(scan.h0);; iso:=IsomorphismPermGroup(H);;
  if iso=fail then Error("GQ2 receipt permutation conversion failed"); fi;
  Hp:=Image(iso);; degree:=LargestMovedPoint(Hp);; if degree<1 then degree:=1; fi;
  wit:=scan.first;; defect:=Image(iso,wit.defect);;
  return Concatenation(
    "{\"schema\":\"d972-b4-finite-image/v2\",",
    "\"target\":",D972GQ2Json(label),",\"target_order\":",String(order),
    ",\"epi_index\":",String(epiIndex),",\"epi_count\":",String(epiCount),
    ",\"h_images\":",D972GQ2Json(List(scan.h0,g->List([1..degree],i->i^Image(iso,g)))),
    ",\"rho_words\":",D972GQ2Json(RhoGQ2),
    ",\"rho_words_source\":\"universal_v2_canonical\",\"rho_words_legacy_json_mismatch\":",
    D972GQ2Json(D972GQ2LegacyRhoMismatch),",\"rho_words_sha256\":",
    D972GQ2Json(D972GQ2CanonicalRhoDigest),
    ",\"source_sha256\":",D972GQ2Json(D972ExactSourceSha256),
    ",\"all_relators\":",D972GQ2Json(D972ExactRelWords),
    ",\"all_relators_sha256\":",D972GQ2Json(D972ExactRelDigest),
    ",\"relator_bools\":",D972GQ2Json(List(D972ExactRelWords,r->true)),
    ",\"rho5\":true,\"target_keys\":",D972GQ2Json(D972ExactTargetKeys),
    ",\"target_key_digest\":",D972GQ2Json(D972ExactTargetDigest),
    ",\"roof_words\":",D972GQ2Json(D972ExactRoofWords),
    ",\"roof_words_sha256\":",D972GQ2Json(D972ExactRoofDigest),
    ",\"witness_index\":",String(wit.index),
    ",\"witness_word\":",D972GQ2Json(wit.word),
    ",\"expected_defect\":",D972GQ2Json(List([1..degree],i->i^defect)),
    ",\"word_key_artifact_sha256\":\"283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930\"}");
end;;

TargetGQ2:=D972GQ2TargetGroup(D972GQ2Target);;
Print("B4_GQ2_TARGET_BEGIN label=",D972GQ2Target," order=",TargetGQ2.order,
  " degree=",TargetGQ2.degree,"\n");
QSGQ2:=GQuotients(UfpGQ2,TargetGQ2.group:findall:=true);;
CountGQ2:=Length(QSGQ2);; Print("B4_GQ2_EPISODE_COUNT count=",CountGQ2,"\n");
SummaryGQ2:=[];; ReceiptGQ2:=fail;; D972EpiIndex:=0;;
for D972Epi in QSGQ2 do
  D972EpiIndex:=D972EpiIndex+1;; ScanGQ2:=D972GQ2Scan(D972Epi);;
  Add(SummaryGQ2,rec(epi_index:=D972EpiIndex,
    relator_bad_count:=Length(ScanGQ2.relator_bad),
    roof_fail_count:=Length(ScanGQ2.fails),rho5:=ScanGQ2.rho5,
    valid:=ScanGQ2.valid));
  if ScanGQ2.first<>fail and ReceiptGQ2=fail then
    ReceiptGQ2:=D972GQ2Receipt(D972GQ2Target,TargetGQ2.order,ScanGQ2,
      D972EpiIndex,CountGQ2);
    Print("B4_GQ2_DEFECT epi=",D972EpiIndex," roof_index=",ScanGQ2.first.index,"\n");
  fi;
od;
if ReceiptGQ2<>fail then D972GQ2Write(D972GQ2ReceiptOutput,ReceiptGQ2); fi;
DefectCountGQ2:=Number(SummaryGQ2,r->r.roof_fail_count>0);;
PassCountGQ2:=Number(SummaryGQ2,r->r.roof_fail_count=0 and
  r.relator_bad_count=0 and r.rho5=true);;
StatusGQ2:="UNKNOWN_ALLPASS_CONTINUE";;
if DefectCountGQ2>0 then StatusGQ2:="B4_A_SIDE_CANDIDATE_PENDING_REPLAY"; fi;
SummaryTextGQ2:=Concatenation(
  "{\"schema\":\"d972-b4-gquotient-covers/v2\",\"status\":",
  D972GQ2Json(StatusGQ2),",\"target\":",D972GQ2Json(D972GQ2Target),
  ",\"target_order\":",String(TargetGQ2.order),
  ",\"target_degree\":",String(TargetGQ2.degree),
  ",\"relator_count\":158,\"roof_count\":972,",
  "\"relator_digest\":",D972GQ2Json(D972ExactRelDigest),
  ",\"roof_word_digest\":",D972GQ2Json(D972ExactRoofDigest),
  ",\"roof_norm_digest\":",D972GQ2Json(NormDigestGQ2),
  ",\"rho_words_source\":\"universal_v2_canonical\",\"rho_words_legacy_json_mismatch\":",
  D972GQ2Json(D972GQ2LegacyRhoMismatch),",\"rho_words_sha256\":",
  D972GQ2Json(D972GQ2CanonicalRhoDigest),
  ",\"source_sha256\":",D972GQ2Json(D972ExactSourceSha256),
  ",\"target_key_digest\":",D972GQ2Json(D972ExactTargetDigest),
  ",\"word_key_artifact_digest\":\"283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930\"",
  ",\"epi_count\":",String(CountGQ2),",\"allpass_epi_count\":",String(PassCountGQ2),
  ",\"defect_epi_count\":",String(DefectCountGQ2),
  ",\"receipt_present\":",D972GQ2Json(ReceiptGQ2<>fail),
  ",\"receipt_output\":",D972GQ2Json(D972GQ2ReceiptOutput),"}");
D972GQ2Write(D972GQ2Output,SummaryTextGQ2);;
Print("B4_GQ2_DONE target=",D972GQ2Target," epis=",CountGQ2,
  " allpass=",PassCountGQ2," defects=",DefectCountGQ2,"\n");
Print("B4_GQ2_FINAL_MARKER status=",StatusGQ2," target=",D972GQ2Target,
  " epis=",CountGQ2," defects=",DefectCountGQ2,"\n");
fi;
