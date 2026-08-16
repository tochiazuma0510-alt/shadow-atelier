#############################################################################
## D972 B4-A low-index max-7 scanner, canonical-v2 input.
##
## Numeric-only preamble controls:
##   D972_B4_LI_V2_MAX_INDEX:=7;; D972_B4_LI_V2_SELFTEST:=0;;
## The bound is fixed at 7; any other value fails closed.  Full mode builds
## F6/<158 exact relators> from the corrected c61b2 JSON, enumerates every
## LowIndexSubgroupsFpGroup subgroup through index 7, and checks every exact
## rho^4...rho^0 roof norm.  All-pass is UNKNOWN.  A valid first roof defect
## is emitted as a d972-b4-finite-image/v2 receipt for the independent checker.
#############################################################################

if not IsBound(GetEnv) then GetEnv:=name->fail; fi;;
if LoadPackage("json")<>true then Error("LI v2: json package unavailable"); fi;
D972LIV2Max:=7;; D972LIV2Selftest:=0;;
if IsBound(D972_B4_LI_V2_MAX_INDEX) then
  D972LIV2Max:=D972_B4_LI_V2_MAX_INDEX;
fi;
if IsBound(D972_B4_LI_V2_SELFTEST) then
  D972LIV2Selftest:=D972_B4_LI_V2_SELFTEST;
fi;
if not IsInt(D972LIV2Max) or D972LIV2Max<>7 then
  Error("LI v2: max-index must be numeric 7");
fi;
if not IsInt(D972LIV2Selftest) or
   (D972LIV2Selftest<>0 and D972LIV2Selftest<>1) then
  Error("LI v2: numeric selftest flag drift");
fi;

D972LIV2SourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972LIV2Rho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;
D972LIV2RhoSha:="23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed";;
D972LIV2RelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972LIV2RoofSha:="3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8";;
D972LIV2NormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972LIV2TargetSha:="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972LIV2WordKeySha:="283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930";;
D972LIV2InputPath:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972LIV2InputSchema:="d972-b4-p2-magnus-input/v2";;
D972LIV2Out:="ci/out/d972_b4_lowindex_v2.json";;
D972LIV2DefectOut:="ci/out/d972_b4_lowindex_v2.defect.json";;

D972LIV2Join:=function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;
  out:=xs[1];;
  for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  return out;
end;;
D972LIV2Json:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",x,"\""); fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("LI v2: JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972LIV2Json(x[i]));;
  return Concatenation("[",D972LIV2Join(p,","),"]");
end;;
D972LIV2Write:=function(path,s)
  local f;
  f:=OutputTextFile(path,false);; SetPrintFormattingStatus(f,false);
  PrintTo(f,Concatenation(s,"\n"));; CloseStream(f);
end;;

D972LIV2RelWords:=fail;; D972LIV2RoofWords:=fail;; D972LIV2Keys:=fail;;
D972LIV2SourceActual:=fail;; D972LIV2RelDigest:=fail;;
D972LIV2RoofDigest:=fail;; D972LIV2TargetDigest:=fail;;
D972LIV2NormRows:=fail;; D972LIV2NormDigest:=fail;;

D972LIV2LoadInput:=function()
  local src,obj,keys,joined,i;
  src:=StringFile(D972LIV2InputPath);;
  if src=fail then Error("LI v2: corrected JSON input missing"); fi;
  D972LIV2SourceActual:=HexSHA256(src);;
  if D972LIV2SourceActual<>D972LIV2SourceSha then
    Error("LI v2: corrected JSON source SHA drift: ",D972LIV2SourceActual);
  fi;
  obj:=JsonStringToGap(src);;
  if not IsRecord(obj) or obj.schema<>D972LIV2InputSchema then
    Error("LI v2: corrected input schema drift");
  fi;
  if obj.rho_words<>D972LIV2Rho or
     not IsBound(obj.rho_words_source) or
     obj.rho_words_source<>"universal_v2_canonical" then
    Error("LI v2: canonical rho drift");
  fi;
  D972LIV2RelWords:=obj.all_relators;; D972LIV2RoofWords:=obj.roof_words;;
  D972LIV2Keys:=obj.target_keys;; D972LIV2RelDigest:=obj.all_relators_sha256;;
  D972LIV2RoofDigest:=obj.roof_words_sha256;; D972LIV2TargetDigest:=obj.target_key_digest;;
  if Length(D972LIV2RelWords)<>158 or Length(D972LIV2RoofWords)<>972 or
     Length(D972LIV2Keys)<>972 then Error("LI v2: input count drift"); fi;
  if D972LIV2RelDigest<>D972LIV2RelSha or
     D972LIV2RoofDigest<>D972LIV2RoofSha or
     D972LIV2TargetDigest<>D972LIV2TargetSha then
    Error("LI v2: input digest metadata drift");
  fi;
  if HexSHA256(D972LIV2Json(D972LIV2RelWords))<>D972LIV2RelSha then
    Error("LI v2: relator digest recomputation drift");
  fi;
  if HexSHA256(D972LIV2Json(D972LIV2RoofWords))<>D972LIV2RoofSha then
    Error("LI v2: roof digest recomputation drift");
  fi;
  keys:=ShallowCopy(D972LIV2Keys);; Sort(keys);; joined:="";;
  for i in [1..Length(keys)] do joined:=Concatenation(joined,keys[i],"\n"); od;
  if HexSHA256(joined)<>D972LIV2TargetSha then
    Error("LI v2: target digest recomputation drift");
  fi;
  Print("B4_LI_V2_INPUT_AUDIT_PASS source_sha256=",D972LIV2SourceActual,
    " relators=158 roofs=972 rho_sha256=",D972LIV2RhoSha,"\n");
end;;

D972LIV2EvalSigned:=function(w,imgs)
  local q,x,g;
  if not IsList(imgs) or Length(imgs)<>6 then Error("LI v2: image list drift"); fi;
  q:=One(imgs[1]);;
  for x in w do
    if not IsInt(x) or x=0 or AbsInt(x)>6 then Error("LI v2: signed letter drift"); fi;
    g:=AbsInt(x);; if x>0 then q:=q*imgs[g]; else q:=q*imgs[g]^-1; fi;
  od;
  return q;
end;;
D972LIV2EvalFree:=function(w,imgs)
  local e,i,g,n,q;
  e:=ExtRepOfObj(w);; q:=One(imgs[1]);; i:=1;
  while i<=Length(e) do
    g:=e[i];; n:=e[i+1];;
    if not IsInt(g) or not IsInt(n) or g<1 or g>6 or n=0 then
      Error("LI v2: free ExtRep drift");
    fi;
    q:=q*imgs[g]^n;; i:=i+2;
  od;
  return q;
end;;
D972LIV2ExtToSigned:=function(e)
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

F6LIV2:=FreeGroup(6);; F6LIV2Gens:=GeneratorsOfGroup(F6LIV2);;
D972LIV2SignedToFree:=function(a)
  local w,x;
  w:=One(F6LIV2Gens[1]);;
  for x in a do
    if x>0 then w:=w*F6LIV2Gens[x]; else w:=w*F6LIV2Gens[-x]^-1; fi;
  od;
  return w;
end;;
D972LIV2BuildNormRows:=function()
  local rows,a,jf,x,orb,v,z,t,rhofree;
  rhofree:=List(D972LIV2Rho,D972LIV2SignedToFree);; rows:=[];;
  for a in D972LIV2RoofWords do
    jf:=One(F6LIV2Gens[1]);;
    for x in a do
      if x=1 then jf:=jf*F6LIV2Gens[1];
      elif x=-1 then jf:=jf*F6LIV2Gens[1]^-1;
      elif x=2 then jf:=jf*F6LIV2Gens[4];
      elif x=-2 then jf:=jf*F6LIV2Gens[4]^-1;
      else Error("LI v2: roof row is not F2"); fi;
    od;
    orb:=[];; v:=jf;;
    for t in [1..5] do Add(orb,v);; v:=D972LIV2EvalFree(v,rhofree); od;
    z:=One(F6LIV2Gens[1]);;
    for t in Reversed([1..5]) do z:=z*orb[t]; od;
    Add(rows,D972LIV2ExtToSigned(ExtRepOfObj(z)));
  od;
  return rows;
end;;

D972LIV2SelfTest:=function()
  local S,id,h,one;
  S:=SymmetricGroup(4);; id:=One(S);;
  h:=[(1,2),id,(1,3,4),(2,3),(2,4),(1,4)];; one:=One(S);
  if h[2]=h[4] then Error("LI v2: y/U4 guard drift"); fi;
  if D972LIV2EvalSigned([1,-1],h)<>one then
    Error("LI v2: inverse evaluator selftest failed");
  fi;
  if D972LIV2Rho[1]<>[-6,-5,-3] or D972LIV2Rho[4]<>[-3,-2,-1] or
     D972LIV2Rho[5]<>[-5,-4,-1] then
    Error("LI v2: canonical rho selftest failed");
  fi;
  Print("B4_LI_V2_SELFTEST_PASS max_index=7 numeric_controls=true y_to_U4=true\n");
end;;

if D972LIV2Selftest=1 then
  D972LIV2SelfTest();;
  Print("B4_LI_V2_SELFTEST_FINAL_MARKER max_index=7\n");
else
  D972LIV2LoadInput();;
  D972LIV2NormRows:=D972LIV2BuildNormRows();;
  D972LIV2NormDigest:=HexSHA256(D972LIV2Json(D972LIV2NormRows));;
  if D972LIV2NormDigest<>D972LIV2NormSha then
    Error("LI v2: norm digest drift: ",D972LIV2NormDigest);
  fi;
  Print("B4_LI_V2_NORM_PASS digest=",D972LIV2NormDigest,
    " order=[4,3,2,1,0] j=(1->U1,2->U4)\n");

  RelsLIV2:=List(D972LIV2RelWords,D972LIV2SignedToFree);;
  UfpLIV2:=F6LIV2/RelsLIV2;; UgensLIV2:=GeneratorsOfGroup(UfpLIV2);;
  if Length(UgensLIV2)<>6 then Error("LI v2: U generator count drift"); fi;
  relsU_LIV2:=RelsLIV2;;

  D972LIV2Scan:=function(qh)
    local h0,hp,t,r,one,bad,relok,rho5,fails,first,z;
    h0:=List(UgensLIV2,g->Image(qh,g));;
    hp:=[];; Add(hp,h0);;
    for t in [1..4] do
      Add(hp,List([1..6],r->D972LIV2EvalSigned(D972LIV2Rho[r],hp[t])));
    od;
    one:=One(h0[1]);; bad:=[];; relok:=[];;
    for r in [1..Length(relsU_LIV2)] do
      Add(relok,IsOne(D972LIV2EvalSigned(D972LIV2RelWords[r],h0)));
    od;
    for t in [1..5] do
      for r in [1..Length(D972LIV2RelWords)] do
        if D972LIV2EvalSigned(D972LIV2RelWords[r],hp[t])<>one then Add(bad,[t,r]); fi;
      od;
    od;
    rho5:=List([1..6],r->D972LIV2EvalSigned(D972LIV2Rho[r],hp[5]))=h0;;
    fails:=[];; first:=fail;;
    if Length(bad)=0 and rho5 then
      for t in [1..Length(D972LIV2NormRows)] do
        z:=D972LIV2EvalSigned(D972LIV2NormRows[t],h0);;
        if z<>one then
          Add(fails,t);;
          if first=fail then first:=rec(index:=t,word:=D972LIV2RoofWords[t],defect:=z); fi;
        fi;
      od;
    fi;
    return rec(h0:=h0,relok:=relok,bad:=bad,rho5:=rho5,fails:=fails,first:=first);
  end;;

  D972LIV2Receipt:=function(scan,qi,qcount,qindex,qorder)
    local degree,wit,defect;
    degree:=qindex;; wit:=scan.first;; defect:=wit.defect;;
    D972LIV2Write(D972LIV2DefectOut,Concatenation(
      "{\"schema\":\"d972-b4-finite-image/v2\",\"target\":\"LI7\",",
      "\"target_order\":",String(qorder),",\"epi_index\":",String(qi),
      ",\"epi_count\":",String(qcount),",\"h_images\":",D972LIV2Json(
        List(scan.h0,g->List([1..degree],i->i^g))),
      ",\"rho_words\":",D972LIV2Json(D972LIV2Rho),
      ",\"rho_words_source\":\"universal_v2_canonical\",\"rho_words_legacy_json_mismatch\":false",
      ",\"rho_words_sha256\":",D972LIV2Json(D972LIV2RhoSha),
      ",\"source_sha256\":",D972LIV2Json(D972LIV2SourceActual),
      ",\"p2_input_schema\":",D972LIV2Json(D972LIV2InputSchema),
      ",\"p2_input_file_sha256\":",D972LIV2Json(D972LIV2SourceActual),
      ",\"all_relators\":",D972LIV2Json(D972LIV2RelWords),
      ",\"all_relators_sha256\":",D972LIV2Json(D972LIV2RelSha),
      ",\"relator_bools\":",D972LIV2Json(scan.relok),",\"rho5\":true",
      ",\"target_keys\":",D972LIV2Json(D972LIV2Keys),
      ",\"target_key_digest\":",D972LIV2Json(D972LIV2TargetSha),
      ",\"roof_words\":",D972LIV2Json(D972LIV2RoofWords),
      ",\"roof_words_sha256\":",D972LIV2Json(D972LIV2RoofSha),
      ",\"witness_index\":",String(wit.index),",\"witness_word\":",
      D972LIV2Json(wit.word),",\"expected_defect\":",D972LIV2Json(
        List([1..degree],i->i^defect)),
      ",\"word_key_artifact_sha256\":",D972LIV2Json(D972LIV2WordKeySha),"}"));
  end;;

  Print("B4_LI_V2_LOW_INDEX_BEGIN max_index=7 exhaustive=true\n");
  liLIV2:=LowIndexSubgroupsFpGroup(UfpLIV2,7);;
  qRowsLIV2:=[];; firstLIV2:=fail;; qiLIV2:=0;;
  for HqLIV2 in liLIV2 do
    qiLIV2:=qiLIV2+1;; mLIV2:=Index(UfpLIV2,HqLIV2);;
    qhLIV2:=FactorCosetAction(UfpLIV2,HqLIV2);;
    scanLIV2:=D972LIV2Scan(qhLIV2);;
    if scanLIV2.first<>fail and firstLIV2=fail then
      firstLIV2:=rec(scan:=scanLIV2,qi:=qiLIV2,index:=mLIV2,
        order:=Size(Image(qhLIV2)));
    fi;
    Add(qRowsLIV2,Concatenation(
      "{\"index\":",String(mLIV2),",\"order\":",String(Size(Image(qhLIV2))),
      ",\"relator_bad\":",String(Number(scanLIV2.relok,x->not x)),
      ",\"rho5\":",D972LIV2Json(scanLIV2.rho5),
      ",\"roof_fail_count\":",String(Length(scanLIV2.fails)),"}"));
    Print("B4_LI_V2_Q qi=",qiLIV2," index=",mLIV2," order=",Size(Image(qhLIV2)),
      " rel_bad=",Number(scanLIV2.relok,x->not x)," rho5=",scanLIV2.rho5,
      " roof_fails=",Length(scanLIV2.fails),"\n");
  od;
  if firstLIV2<>fail then
    D972LIV2Receipt(firstLIV2.scan,firstLIV2.qi,Length(liLIV2),
      firstLIV2.index,firstLIV2.order);;
  fi;
  StatusLIV2:="UNKNOWN_ALLPASS_CONTINUE";;
  if firstLIV2<>fail then StatusLIV2:="DEFECT_CANDIDATE_PENDING_REPLAY"; fi;
  D972LIV2ReceiptField:="null";;
  if firstLIV2<>fail then D972LIV2ReceiptField:=D972LIV2Json(D972LIV2DefectOut); fi;
  SummaryLIV2:=Concatenation(
    "{\"schema\":\"d972-b4-lowindex/v2\",\"status\":",
    D972LIV2Json(StatusLIV2),",\"max_index\":7,\"exhaustive\":true,",
    "\"quotient_count\":",String(Length(liLIV2)),",\"relator_count\":158,\"roof_count\":972,",
    "\"source_sha256\":",D972LIV2Json(D972LIV2SourceActual),
    ",\"p2_input_schema\":",D972LIV2Json(D972LIV2InputSchema),
    ",\"p2_input_file_sha256\":",D972LIV2Json(D972LIV2SourceActual),
    ",\"rho_words_source\":\"universal_v2_canonical\",\"rho_words_legacy_json_mismatch\":false",
    ",\"rho_words_sha256\":",D972LIV2Json(D972LIV2RhoSha),
    ",\"all_relators_sha256\":",D972LIV2Json(D972LIV2RelSha),
    ",\"roof_words_sha256\":",D972LIV2Json(D972LIV2RoofSha),
    ",\"roof_norm_sha256\":",D972LIV2Json(D972LIV2NormSha),
    ",\"target_key_digest\":",D972LIV2Json(D972LIV2TargetSha),
    ",\"word_key_artifact_sha256\":",D972LIV2Json(D972LIV2WordKeySha),
    ",\"quotients\":[",D972LIV2Join(qRowsLIV2,","),
    "],\"defect_receipt\":",D972LIV2ReceiptField,"}");
  D972LIV2Write(D972LIV2Out,SummaryLIV2);;
  Print("B4_LI_V2_ARTIFACT_WRITTEN path=",D972LIV2Out,"\n");
  if firstLIV2<>fail then Print("B4_LI_V2_DEFECT_RECEIPT path=",D972LIV2DefectOut,"\n"); fi;
  Print("B4_LI_V2_FINAL_MARKER status=",StatusLIV2,
    " max_index=7 quotients=",Length(liLIV2),"\n");
fi;
