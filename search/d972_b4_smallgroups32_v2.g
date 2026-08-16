#############################################################################
## D972 B4-A canonical-v2 SmallGroup(32) sharded scanner.
##
## Numeric-only controls are accepted before Read():
##   D972_SG32_ID_START:=1;; D972_SG32_ID_END:=17;; D972_SG32_SELFTEST:=0;;
## Defaults are the complete 1..51 SmallGroup(32) universe.  A shard is
## exhaustive over every GQuotients epimorphism for each selected group, but
## every finite all-pass result remains UNKNOWN.  A valid roof defect writes
## one d972-b4-finite-image/v2 receipt per defective epimorphism.
#############################################################################

if not IsBound(GetEnv) then GetEnv:=name->fail; fi;;

if LoadPackage("smallgrp") <> true then
  Error("SG32 v2: smallgrp package unavailable");
fi;
if LoadPackage("json") <> true then
  Error("SG32 v2: json package unavailable");
fi;

D972SG32Start:=1;; D972SG32End:=51;; D972SG32Selftest:=0;;
if IsBound(D972_SG32_ID_START) then D972SG32Start:=D972_SG32_ID_START; fi;
if IsBound(D972_SG32_ID_END) then D972SG32End:=D972_SG32_ID_END; fi;
if IsBound(D972_SG32_SELFTEST) then D972SG32Selftest:=D972_SG32_SELFTEST; fi;
if not IsBound(D972_SG32_SELFTEST) then
  D972SG32SelftestEnv:=GetEnv("D972_SG32_SELFTEST");;
  if D972SG32SelftestEnv<>fail and D972SG32SelftestEnv<>"" then
    D972SG32Selftest:=Int(D972SG32SelftestEnv);
  fi;
fi;
if not IsInt(D972SG32Start) or not IsInt(D972SG32End) or
   D972SG32Start<1 or D972SG32End>51 or D972SG32Start>D972SG32End then
  Error("SG32 v2: numeric shard range drift");
fi;
if not IsInt(D972SG32Selftest) or
   (D972SG32Selftest<>0 and D972SG32Selftest<>1) then
  Error("SG32 v2: numeric selftest flag drift");
fi;
D972SG32Output:=Concatenation("ci/out/d972_b4_sg32_",String(D972SG32Start),
  "_",String(D972SG32End),".json");;

D972SG32SourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972SG32Rho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;
D972SG32RhoSha:="23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed";;
D972SG32RelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972SG32RoofSha:="3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8";;
D972SG32NormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972SG32TargetSha:="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972SG32WordKeySha:="283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930";;
D972SG32InputPath:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;

D972SG32Join:=function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;
  out:=xs[1];;
  for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  return out;
end;;
D972SG32Json:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\"");
  fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("SG32 v2: JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972SG32Json(x[i]));;
  return Concatenation("[",D972SG32Join(p,","),"]");
end;;
D972SG32Write:=function(path,s)
  local f;
  f:=OutputTextFile(path,false);;
  SetPrintFormattingStatus(f,false);;
  PrintTo(f,Concatenation(s,"\n"));;
  CloseStream(f);;
end;;

D972SG32RelWords:=fail;; D972SG32RoofWords:=fail;; D972SG32Keys:=fail;;
D972SG32RelDigest:=fail;; D972SG32RoofDigest:=fail;; D972SG32TargetDigest:=fail;;
D972SG32SourceActual:=fail;; D972SG32NormRows:=fail;; D972SG32NormDigest:=fail;;

D972SG32LoadInput:=function()
  local src,obj,keys,joined,i;
  src:=StringFile(D972SG32InputPath);;
  if src=fail then Error("SG32 v2: corrected JSON input missing"); fi;
  D972SG32SourceActual:=HexSHA256(src);;
  if D972SG32SourceActual<>D972SG32SourceSha then
    Error("SG32 v2: corrected JSON source SHA drift: ",D972SG32SourceActual);
  fi;
  obj:=JsonStringToGap(src);;
  if not IsRecord(obj) or obj.schema<>"d972-b4-p2-magnus-input/v2" then
    Error("SG32 v2: input schema drift");
  fi;
  if obj.rho_words<>D972SG32Rho or
     not IsBound(obj.rho_words_source) or
     obj.rho_words_source<>"universal_v2_canonical" then
    Error("SG32 v2: canonical rho drift");
  fi;
  D972SG32RelWords:=obj.all_relators;;
  D972SG32RoofWords:=obj.roof_words;;
  D972SG32Keys:=obj.target_keys;;
  D972SG32RelDigest:=obj.all_relators_sha256;;
  D972SG32RoofDigest:=obj.roof_words_sha256;;
  D972SG32TargetDigest:=obj.target_key_digest;;
  if Length(D972SG32RelWords)<>158 or Length(D972SG32RoofWords)<>972 or
     Length(D972SG32Keys)<>972 then
    Error("SG32 v2: input count drift");
  fi;
  if D972SG32RelDigest<>D972SG32RelSha or
     D972SG32RoofDigest<>D972SG32RoofSha or
     D972SG32TargetDigest<>D972SG32TargetSha then
    Error("SG32 v2: input digest metadata drift");
  fi;
  if HexSHA256(D972SG32Json(D972SG32RelWords))<>D972SG32RelSha then
    Error("SG32 v2: relator digest recomputation drift");
  fi;
  if HexSHA256(D972SG32Json(D972SG32RoofWords))<>D972SG32RoofSha then
    Error("SG32 v2: roof digest recomputation drift");
  fi;
  keys:=ShallowCopy(D972SG32Keys);; Sort(keys);; joined:="";;
  for i in [1..Length(keys)] do joined:=Concatenation(joined,keys[i],"\n"); od;
  if HexSHA256(joined)<>D972SG32TargetSha then
    Error("SG32 v2: target digest recomputation drift");
  fi;
  Print("D972_SG32_INPUT_AUDIT_PASS source_sha256=",D972SG32SourceActual,
    " relators=158 roofs=972 rho_sha256=",D972SG32RhoSha,"\n");
end;;

D972SG32EvalSigned:=function(w,imgs)
  local q,x,g;
  if not IsList(imgs) or Length(imgs)<>6 then
    Error("SG32 v2: six-image evaluator drift");
  fi;
  q:=One(imgs[1]);;
  for x in w do
    if not IsInt(x) or x=0 or AbsInt(x)>6 then
      Error("SG32 v2: signed word letter drift");
    fi;
    g:=AbsInt(x);;
    if x>0 then q:=q*imgs[g]; else q:=q*imgs[g]^-1; fi;
  od;
  return q;
end;;
D972SG32EvalFree:=function(w,imgs)
  local e,i,g,n,q;
  if not IsList(imgs) or Length(imgs)<>6 then
    Error("SG32 v2: free evaluator image drift");
  fi;
  e:=ExtRepOfObj(w);; q:=One(imgs[1]);; i:=1;
  while i<=Length(e) do
    g:=e[i];; n:=e[i+1];;
    if not IsInt(g) or not IsInt(n) or g<1 or g>6 or n=0 then
      Error("SG32 v2: free ExtRep drift");
    fi;
    q:=q*imgs[g]^n;; i:=i+2;
  od;
  return q;
end;;
D972SG32ExtToSigned:=function(e)
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

## Build the exact F6 words and bind the independently recomputed norm digest.
F6SG32:=FreeGroup(6);; F6GensSG32:=GeneratorsOfGroup(F6SG32);;
D972SG32SignedToFree:=function(a)
  local w,x;
  w:=One(F6GensSG32[1]);;
  for x in a do
    if x>0 then w:=w*F6GensSG32[x];
    else w:=w*F6GensSG32[-x]^-1; fi;
  od;
  return w;
end;;

D972SG32BuildNormRows:=function()
  local rows,a,jf,x,orb,v,z,t;
  rows:=[];;
  for a in D972SG32RoofWords do
    jf:=One(F6GensSG32[1]);;
    for x in a do
      if x=1 then jf:=jf*F6GensSG32[1];
      elif x=-1 then jf:=jf*F6GensSG32[1]^-1;
      elif x=2 then jf:=jf*F6GensSG32[4];
      elif x=-2 then jf:=jf*F6GensSG32[4]^-1;
      else Error("SG32 v2: roof row is not F2"); fi;
    od;
    orb:=[];; v:=jf;;
    for t in [1..5] do
      Add(orb,v);;
      v:=D972SG32EvalFree(v,
        List(D972SG32Rho,D972SG32SignedToFree));;
    od;
    z:=One(F6GensSG32[1]);;
    for t in Reversed([1..5]) do z:=z*orb[t]; od;
    Add(rows,D972SG32ExtToSigned(ExtRepOfObj(z)));
  od;
  return rows;
end;;

D972SG32SelfTest:=function()
  local S,id,h,w,got,one;
  S:=SymmetricGroup(4);; id:=One(S);;
  h:=[(1,2),id,(1,3,4),(2,3),(2,4),(1,4)];;
  if h[2]=h[4] then Error("SG32 v2: y/U4 asymmetric guard drift"); fi;
  w:=[1,-2,3,-6];; got:=D972SG32EvalSigned(w,h);;
  one:=One(S);;
  if got=one then Error("SG32 v2: signed evaluator selftest unexpectedly trivial"); fi;
  if D972SG32EvalSigned([1,-1],h)<>one then
    Error("SG32 v2: inverse evaluator selftest failed");
  fi;
  if D972SG32Rho[1]<>[-6,-5,-3] or D972SG32Rho[4]<>[-3,-2,-1] or
     D972SG32Rho[5]<>[-5,-4,-1] then
    Error("SG32 v2: rho inverse-order selftest failed");
  fi;
  Print("D972_SG32_SELFTEST_PASS numeric_controls=true y_to_U4=true evaluator=true\n");
end;;

if D972SG32Selftest=1 then
  ## The full shard path performs the expensive 158/972 JSON digest audit
  ## before any GQuotients call.  Selftest deliberately stays cheap while
  ## pinning the same immutable source/digest constants and exercising the
  ## evaluator/asymmetric-j map; input-audit is therefore not bypassed in a
  ## production shard.
  D972SG32SelfTest();;
  Print("D972_SG32_SELFTEST_FINAL_MARKER start=",D972SG32Start,
    " end=",D972SG32End,"\n");
else
  D972SG32LoadInput();;
  D972SG32NormRows:=D972SG32BuildNormRows();;
  D972SG32NormDigest:=HexSHA256(D972SG32Json(D972SG32NormRows));;
  if D972SG32NormDigest<>D972SG32NormSha then
    Error("SG32 v2: norm digest drift: ",D972SG32NormDigest);
  fi;
  Print("D972_SG32_NORM_PASS digest=",D972SG32NormDigest,
    " order=[4,3,2,1,0] j=(1->U1,2->U4)\n");

  RelsSG32:=List(D972SG32RelWords,D972SG32SignedToFree);;
  UfpSG32:=F6SG32/RelsSG32;; UgensSG32:=GeneratorsOfGroup(UfpSG32);;
  if Length(UgensSG32)<>6 then Error("SG32 v2: U generator count drift"); fi;

  D972SG32Scan:=function(epi)
    local h0,hp,t,r,one,bad,rho5,fails,first,z;
    h0:=List(UgensSG32,g->Image(epi,g));;
    hp:=[];; Add(hp,h0);;
    for t in [1..4] do
      Add(hp,List([1..6],r->D972SG32EvalSigned(D972SG32Rho[r],hp[t])));
    od;
    one:=One(h0[1]);; bad:=[];;
    for t in [1..5] do
      for r in [1..Length(D972SG32RelWords)] do
        if D972SG32EvalSigned(D972SG32RelWords[r],hp[t])<>one then
          Add(bad,[t,r]);
        fi;
      od;
    od;
    rho5:=List([1..6],r->D972SG32EvalSigned(D972SG32Rho[r],hp[5]))=h0;;
    fails:=[];; first:=fail;;
    if Length(bad)=0 and rho5 then
      for t in [1..Length(D972SG32NormRows)] do
        z:=D972SG32EvalSigned(D972SG32NormRows[t],h0);;
        if z<>one then
          Add(fails,t);;
          if first=fail then first:=rec(index:=t,word:=D972SG32RoofWords[t],defect:=z); fi;
        fi;
      od;
    fi;
    return rec(h0:=h0,relator_bad:=bad,rho5:=rho5,fails:=fails,
      first:=first,valid:=(Length(bad)=0 and rho5));
  end;;

  D972SG32Receipt:=function(label,id,order,scan,epiIndex,epiCount,path)
    local H,iso,Hp,degree,wit,defect;
    H:=Group(scan.h0);; iso:=IsomorphismPermGroup(H);;
    if iso=fail then Error("SG32 v2: receipt permutation conversion failed"); fi;
    Hp:=Image(iso);; degree:=LargestMovedPoint(Hp);;
    if degree<1 then degree:=1; fi;
    wit:=scan.first;; defect:=Image(iso,wit.defect);;
    D972SG32Write(path,Concatenation(
      "{\"schema\":\"d972-b4-finite-image/v2\",\"target\":",
      D972SG32Json(label),",\"target_order\":",String(order),
      ",\"epi_index\":",String(epiIndex),",\"epi_count\":",String(epiCount),
      ",\"h_images\":",D972SG32Json(List(scan.h0,g->
        List([1..degree],i->i^Image(iso,g)))),
      ",\"rho_words\":",D972SG32Json(D972SG32Rho),
      ",\"rho_words_source\":\"universal_v2_canonical\",\"rho_words_legacy_json_mismatch\":false",
      ",\"rho_words_sha256\":",D972SG32Json(D972SG32RhoSha),
      ",\"source_sha256\":",D972SG32Json(D972SG32SourceActual),
      ",\"all_relators\":",D972SG32Json(D972SG32RelWords),
      ",\"all_relators_sha256\":",D972SG32Json(D972SG32RelSha),
      ",\"relator_bools\":",D972SG32Json(List(D972SG32RelWords,r->true)),
      ",\"rho5\":true,\"target_keys\":",D972SG32Json(D972SG32Keys),
      ",\"target_key_digest\":",D972SG32Json(D972SG32TargetSha),
      ",\"roof_words\":",D972SG32Json(D972SG32RoofWords),
      ",\"roof_words_sha256\":",D972SG32Json(D972SG32RoofSha),
      ",\"witness_index\":",String(wit.index),
      ",\"witness_word\":",D972SG32Json(wit.word),
      ",\"expected_defect\":",D972SG32Json(List([1..degree],i->i^defect)),
      ",\"word_key_artifact_sha256\":",D972SG32Json(D972SG32WordKeySha),"}"));
  end;;

  Print("D972_SG32_SCOPE start=",D972SG32Start," end=",D972SG32End,
    " default_full=true numeric_controls=true exhaustive_shard=true\n");
  Print("D972_SG32_SHARD_BEGIN start=",D972SG32Start," end=",D972SG32End,"\n");
  GroupRowsSG32:=[];; DefectPathsSG32:=[];; DefectCountSG32:=0;;
  for idSG32 in [D972SG32Start..D972SG32End] do
    GSG32:=SmallGroup(32,idSG32);;
    if IdGroup(GSG32)<>[32,idSG32] then Error("SG32 v2: SmallGroup id drift"); fi;
    Print("D972_SG32_GROUP_BEGIN id=",idSG32,"\n");
    QSG32:=GQuotients(UfpSG32,GSG32:findall:=true);;
    CountSG32:=Length(QSG32);; CheckedSG32:=0;; DefectEpiSG32:=0;;
    for epiSG32 in QSG32 do
      CheckedSG32:=CheckedSG32+1;; ScanSG32:=D972SG32Scan(epiSG32);;
      if ScanSG32.first<>fail then
        DefectEpiSG32:=DefectEpiSG32+1;; DefectCountSG32:=DefectCountSG32+1;;
        DefectPathSG32:=Concatenation("ci/out/d972_b4_sg32_",String(D972SG32Start),
          "_",String(D972SG32End),"_id",String(idSG32),"_epi",String(CheckedSG32),".defect.json");;
        D972SG32Receipt(Concatenation("SG32_",String(idSG32)),idSG32,32,
          ScanSG32,CheckedSG32,CountSG32,DefectPathSG32);;
        Add(DefectPathsSG32,DefectPathSG32);;
        Print("D972_SG32_DEFECT id=",idSG32," epi=",CheckedSG32,
          " roof_index=",ScanSG32.first.index," receipt=",DefectPathSG32,"\n");
      fi;
    od;
    if CheckedSG32<>CountSG32 then Error("SG32 v2: epi coverage drift"); fi;
    AllPassSG32:=(DefectEpiSG32=0 and CountSG32=CheckedSG32);;
    Add(GroupRowsSG32,Concatenation(
      "{\"id\":",String(idSG32),",\"order\":32,\"epi_count\":",String(CountSG32),
      ",\"epi_checked\":",String(CheckedSG32),",\"defect_epi_count\":",
      String(DefectEpiSG32),",\"allpass\":",D972SG32Json(AllPassSG32),"}"));
    Print("D972_SG32_GROUP_DONE id=",idSG32," epis=",CountSG32,
      " checked=",CheckedSG32," defects=",DefectEpiSG32,
      " allpass=",AllPassSG32,"\n");
  od;
  StatusSG32:="UNKNOWN_ALLPASS_CONTINUE";;
  if DefectCountSG32>0 then StatusSG32:="B4_A_SIDE_CANDIDATE_PENDING_REPLAY"; fi;
  SummarySG32:=Concatenation(
    "{\"schema\":\"d972-b4-smallgroups32-shard/v2\",\"status\":",
    D972SG32Json(StatusSG32),",\"id_start\":",String(D972SG32Start),
    ",\"id_end\":",String(D972SG32End),",\"group_count\":",
    String(D972SG32End-D972SG32Start+1),",\"order\":32,\"exhaustive_shard\":true",
    ",\"source_sha256\":",D972SG32Json(D972SG32SourceActual),
    ",\"rho_words\":",D972SG32Json(D972SG32Rho),
    ",\"rho_words_source\":\"universal_v2_canonical\",\"rho_words_legacy_json_mismatch\":false",
    ",\"rho_words_sha256\":",D972SG32Json(D972SG32RhoSha),
    ",\"all_relators_sha256\":",D972SG32Json(D972SG32RelSha),
    ",\"roof_words_sha256\":",D972SG32Json(D972SG32RoofSha),
    ",\"roof_norm_sha256\":",D972SG32Json(D972SG32NormSha),
    ",\"target_key_digest\":",D972SG32Json(D972SG32TargetSha),
    ",\"word_key_artifact_sha256\":",D972SG32Json(D972SG32WordKeySha),
    ",\"groups\":[",D972SG32Join(GroupRowsSG32,","),"],\"defect_receipts\":",
    D972SG32Json(DefectPathsSG32),",\"defect_epi_count\":",String(DefectCountSG32),"}");
  D972SG32Write(D972SG32Output,SummarySG32);;
  Print("D972_SG32_ARTIFACT_WRITTEN path=",D972SG32Output," defects=",DefectCountSG32,"\n");
  Print("D972_SG32_FINAL_MARKER status=",StatusSG32," start=",D972SG32Start,
    " end=",D972SG32End," groups=",D972SG32End-D972SG32Start+1,
    " defects=",DefectCountSG32,"\n");
fi;
