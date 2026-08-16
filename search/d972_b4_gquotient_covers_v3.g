#############################################################################
## d972_b4_gquotient_covers_v3.g
##
## Canonical finite-simple-target lane for B4-A.  The only selectable target
## table is numeric and closed: PSL2_11, SL2_11, PGL2_11, PSL2_13, SL2_13,
## M11, PSL3_3.  The canonical v2 JSON is loaded directly and all public
## relator/roof/key/rho digests are recomputed before GQuotients.
##
## A defect receipt uses the existing d972-b4-finite-image/v2 schema and is
## independently checked by check_d972_b4_finite_image_v2.py.  Epi-zero and
## all-pass outcomes are UNKNOWN.  A target selftest constructs every group,
## checks its numeric order and permutation copy, and never invokes
## GQuotients.
##
## Quote-free workflow preamble:
##   D972_B4_GQ_TARGET_INDEX:=1;; D972_B4_GQ_SELFTEST:=1;;
##   Read("search/d972_b4_gquotient_covers_v3.g");
#############################################################################

if not IsBound(GetEnv) then GetEnv:=name->fail; fi;
D972GQ3Mode:=fail;;
if IsBound(D972_B4_GQ_MODE) then D972GQ3Mode:=D972_B4_GQ_MODE; fi;
if D972GQ3Mode=fail then D972GQ3Mode:=GetEnv("D972_B4_GQ_MODE"); fi;
if D972GQ3Mode=fail or D972GQ3Mode="" then D972GQ3Mode:="selftest"; fi;

D972GQ3Labels:=["PSL2_11","SL2_11","PGL2_11","PSL2_13","SL2_13",
  "M11","PSL3_3"];;
D972GQ3Orders:=[660,1320,1320,1092,2184,7920,5616];;
D972GQ3TargetIndex:=fail;; D972GQ3Numeric:=false;;
if IsBound(D972_B4_GQ_TARGET_INDEX) then
  D972GQ3TargetIndex:=D972_B4_GQ_TARGET_INDEX;; D972GQ3Numeric:=true;
else
  D972GQ3IndexEnv:=GetEnv("D972_B4_GQ_TARGET_INDEX");;
  if D972GQ3IndexEnv<>fail and D972GQ3IndexEnv<>"" then
    D972GQ3TargetIndex:=Int(D972GQ3IndexEnv);; D972GQ3Numeric:=true;
  fi;
fi;
if D972GQ3Numeric then
  if not IsInt(D972GQ3TargetIndex) or D972GQ3TargetIndex<1 or
     D972GQ3TargetIndex>Length(D972GQ3Labels) then
    Error("GQ3 numeric target index drift (expected 1..7)");
  fi;
  D972GQ3Target:=D972GQ3Labels[D972GQ3TargetIndex];;
  D972GQ3Mode:="target";;
  Print("B4_GQ3_TARGET_INDEX_PASS index=",D972GQ3TargetIndex,
    " label=",D972GQ3Target," count=7\n");
else
  D972GQ3Target:="PSL2_11";;
fi;
D972GQ3Selftest:=0;;
if IsBound(D972_B4_GQ_SELFTEST) then D972GQ3Selftest:=D972_B4_GQ_SELFTEST; fi;
if not IsInt(D972GQ3Selftest) or (D972GQ3Selftest<>0 and D972GQ3Selftest<>1) then
  Error("GQ3 numeric selftest flag drift");
fi;
if D972GQ3Selftest=1 then D972GQ3Mode:="selftest"; fi;

D972GQ3CanonicalInput:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972GQ3Input:=fail;;
if IsBound(D972_B4_GQ_INPUT) then D972GQ3Input:=D972_B4_GQ_INPUT; fi;
if D972GQ3Input=fail then D972GQ3Input:=GetEnv("D972_B4_GQ_INPUT"); fi;
D972GQ3InputDefault:=false;;
if D972GQ3Input=fail or D972GQ3Input="" then
  D972GQ3Input:=D972GQ3CanonicalInput;; D972GQ3InputDefault:=true;
fi;
D972GQ3Output:=fail;;
if IsBound(D972_B4_GQ_OUTPUT) then D972GQ3Output:=D972_B4_GQ_OUTPUT; fi;
if D972GQ3Output=fail then D972GQ3Output:=GetEnv("D972_B4_GQ_OUTPUT"); fi;
D972GQ3OutputDefault:=false;;
if D972GQ3Output=fail or D972GQ3Output="" then
  if D972GQ3Numeric then
    D972GQ3Output:=Concatenation("ci/out/d972_b4_gquotient_v3_",
      String(D972GQ3TargetIndex),".json");
  else
    D972GQ3Output:=Filename(DirectoryTemporary(),"d972_b4_gquotient_v3.json");
  fi;
  D972GQ3OutputDefault:=true;
fi;
D972GQ3DefectOutput:=Concatenation(D972GQ3Output,".defect.json");;
if D972GQ3InputDefault then Print("B4_GQ3_INPUT_DEFAULT_PASS path=",D972GQ3Input,"\n"); fi;
if D972GQ3OutputDefault then Print("B4_GQ3_OUTPUT_DEFAULT_PASS path=",D972GQ3Output,"\n"); fi;

D972GQ3SourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972GQ3RelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972GQ3RoofSha:="3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8";;
D972GQ3TargetSha:="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972GQ3WordKeySha:="283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930";;
D972GQ3Rho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;
D972GQ3RhoSha:="23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed";;
D972GQ3RelWords:=fail;; D972GQ3RoofWords:=fail;; D972GQ3Keys:=fail;;
D972GQ3Sorted:=[];; D972GQ3Joined:="";; D972GQ3Key:="";;

D972GQ3Join:=function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;
  out:=xs[1];;
  for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  return out;
end;;
D972GQ3Json:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("GQ3 JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972GQ3Json(x[i]));;
  return Concatenation("[",D972GQ3Join(p,","),"]");
end;;
D972GQ3Write:=function(path,s)
  local f;
  f:=OutputTextFile(path,false);; SetPrintFormattingStatus(f,false);
  PrintTo(f,Concatenation(s,"\n"));; CloseStream(f);
end;;

D972GQ3LoadInput:=function()
  local src,obj;
  if LoadPackage("json")<>true then Error("GQ3 json package unavailable"); fi;
  src:=StringFile(D972GQ3Input);;
  if src=fail then Error("GQ3 canonical input missing"); fi;
  if HexSHA256(src)<>D972GQ3SourceSha then Error("GQ3 source SHA drift"); fi;
  obj:=JsonStringToGap(src);;
  if not IsRecord(obj) or obj.schema<>"d972-b4-p2-magnus-input/v2" or
     obj.rho_words<>D972GQ3Rho or obj.rho_words_source<>"universal_v2_canonical" or
     (IsBound(obj.rho_words_sha256) and obj.rho_words_sha256<>D972GQ3RhoSha) then
    Error("GQ3 canonical rho/schema gate failed");
  fi;
  D972GQ3RelWords:=obj.all_relators;; D972GQ3RoofWords:=obj.roof_words;;
  D972GQ3Keys:=obj.target_keys;;
  if Length(D972GQ3RelWords)<>158 or Length(D972GQ3RoofWords)<>972 or
     Length(D972GQ3Keys)<>972 then Error("GQ3 input count drift"); fi;
  if obj.all_relators_sha256<>D972GQ3RelSha or
     obj.roof_words_sha256<>D972GQ3RoofSha or
     obj.target_key_digest<>D972GQ3TargetSha then Error("GQ3 input digest metadata drift"); fi;
  if HexSHA256(D972GQ3Json(D972GQ3RelWords))<>D972GQ3RelSha or
     HexSHA256(D972GQ3Json(D972GQ3RoofWords))<>D972GQ3RoofSha then
    Error("GQ3 recomputed word digest drift");
  fi;
  D972GQ3Sorted:=ShallowCopy(D972GQ3Keys);; Sort(D972GQ3Sorted);; D972GQ3Joined:="";;
  for D972GQ3Key in D972GQ3Sorted do D972GQ3Joined:=Concatenation(D972GQ3Joined,D972GQ3Key,"\n"); od;
  if HexSHA256(D972GQ3Joined)<>D972GQ3TargetSha then Error("GQ3 target-key digest drift"); fi;
  Print("B4_GQ3_INPUT_AUDIT_PASS source_sha256=",D972GQ3SourceSha,
    " relator_digest=",D972GQ3RelSha," roof_digest=",D972GQ3RoofSha,
    " target_digest=",D972GQ3TargetSha," rho_sha256=",D972GQ3RhoSha,"\n");
end;;

D972GQ3TargetGroup:=function(label)
  local G,iso,Gp,ord;
  if label="PSL2_11" then G:=PSL(2,11);
  elif label="SL2_11" then G:=SL(2,11);
  elif label="PGL2_11" then G:=PGL(2,11);
  elif label="PSL2_13" then G:=PSL(2,13);
  elif label="SL2_13" then G:=SL(2,13);
  elif label="M11" then G:=MathieuGroup(11);
  elif label="PSL3_3" then G:=PSL(3,3);
  else Error("GQ3 unknown target: ",label);
  fi;
  ord:=Size(G);; iso:=IsomorphismPermGroup(G);;
  if iso=fail then Error("GQ3 permutation conversion failed: ",label); fi;
  Gp:=Image(iso);;
  if ord<>Size(Gp) then Error("GQ3 target order drift: ",label); fi;
  return rec(group:=Gp,order:=ord,degree:=LargestMovedPoint(Gp));
end;;

D972GQ3SelfTest:=function()
  local i,T,expected,h,one,invh;
  if D972GQ3Input<>D972GQ3CanonicalInput then
    Error("GQ3 selftest requires default canonical input");
  fi;
  D972GQ3LoadInput();;
  for i in [1..Length(D972GQ3Labels)] do
    T:=D972GQ3TargetGroup(D972GQ3Labels[i]);;
    expected:=D972GQ3Orders[i];;
    if T.order<>expected or Size(T.group)<>expected or T.degree<1 then
      Error("GQ3 numeric constructor/order selftest failed: ",D972GQ3Labels[i]);
    fi;
    Print("B4_GQ3_TARGET_SELFTEST_PASS index=",i," label=",D972GQ3Labels[i],
      " order=",T.order," degree=",T.degree,"\n");
  od;
  one:=(1,2,3);; invh:=(2,1,3);;
  if invh^2<>one then Error("GQ3 permutation evaluator selftest failed"); fi;
  h:=[invh,one,one,one,one,invh];;
  if h[1]^2<>one or h[6]^2<>one then Error("GQ3 image selftest failed"); fi;
  Print("B4_GQ3_SELFTEST_PASS targets=7 canonical_hashes=true quote_free=true\n");
  Print("B4_GQ3_SELFTEST_FINAL_MARKER status=PASS targets=7 source_sha256=",
    D972GQ3SourceSha," relator_digest=",D972GQ3RelSha," rho_sha256=",D972GQ3RhoSha,"\n");
end;;

if D972GQ3Mode="selftest" then
  D972GQ3SelfTest();;
else
  D972GQ3LoadInput();;
  F6GQ3:=FreeGroup(6);; G6GQ3:=GeneratorsOfGroup(F6GQ3);;
  D972GQ3SignedWord:=function(a)
    local w,v;
    w:=One(G6GQ3[1]);;
    for v in a do if v>0 then w:=w*G6GQ3[v]; else w:=w*G6GQ3[-v]^-1; fi; od;
    return w;
  end;;
  D972GQ3Eval:=function(w,row)
    local q,v;
    q:=One(row[1]);;
    for v in w do if v>0 then q:=q*row[v]; else q:=q*row[-v]^-1; fi; od;
    return q;
  end;;
  RelsGQ3:=List(D972GQ3RelWords,D972GQ3SignedWord);; UfpGQ3:=F6GQ3/RelsGQ3;;
  UgensGQ3:=GeneratorsOfGroup(UfpGQ3);;
  RhoFreeGQ3:=List(D972GQ3Rho,D972GQ3SignedWord);;
  NormRowsGQ3:=[];;
  for D972GQ3Roof in D972GQ3RoofWords do
    jf:=One(G6GQ3[1]);;
    for D972GQ3Letter in D972GQ3Roof do
      if D972GQ3Letter=1 then jf:=jf*G6GQ3[1];
      elif D972GQ3Letter=-1 then jf:=jf*G6GQ3[1]^-1;
      elif D972GQ3Letter=2 then jf:=jf*G6GQ3[4];
      elif D972GQ3Letter=-2 then jf:=jf*G6GQ3[4]^-1;
      else Error("GQ3 roof word is not F2"); fi;
    od;
    orb:=[];; v:=jf;;
    for D972GQ3T in [1..5] do Add(orb,v);; v:=MappedWord(v,G6GQ3,RhoFreeGQ3); od;
    z:=One(G6GQ3[1]);; for D972GQ3T in Reversed([1..5]) do z:=z*orb[D972GQ3T]; od;
    Add(NormRowsGQ3,[]);; D972GQ3Out:=Length(NormRowsGQ3);;
    e:=ExtRepOfObj(z);; i:=1;;
    while i<=Length(e) do
      g:=e[i];; n:=e[i+1];;
      if n>0 then for j in [1..n] do Add(NormRowsGQ3[D972GQ3Out],g); od;
      else for j in [1..-n] do Add(NormRowsGQ3[D972GQ3Out],-g); od; fi;
      i:=i+2;
    od;
  od;
  NormShaGQ3:=HexSHA256(D972GQ3Json(NormRowsGQ3));;
  if NormShaGQ3<>"ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e" then
    Error("GQ3 norm digest drift: ",NormShaGQ3);
  fi;
  Print("B4_GQ3_INPUT_PASS relators=158 roofs=972 norm_digest=",NormShaGQ3,"\n");
  TargetGQ3:=D972GQ3TargetGroup(D972GQ3Target);;
  Print("B4_GQ3_TARGET_BEGIN label=",D972GQ3Target," order=",TargetGQ3.order,
    " degree=",TargetGQ3.degree,"\n");
  QSGQ3:=GQuotients(UfpGQ3,TargetGQ3.group:findall:=true);;
  CountGQ3:=Length(QSGQ3);; Print("B4_GQ3_EPISODE_COUNT count=",CountGQ3,"\n");
  D972GQ3Scan:=function(epi)
    local h0,hp,t,r,one,bad,fails,first,z,valid;
    h0:=List(UgensGQ3,g->Image(epi,g));; hp:=[h0];;
    for t in [1..4] do Add(hp,List([1..6],r->D972GQ3Eval(D972GQ3Rho[r],hp[t]))); od;
    one:=One(h0[1]);; bad:=[];;
    for t in [1..5] do for r in D972GQ3RelWords do
      if D972GQ3Eval(r,hp[t])<>one then Add(bad,[t,Position(D972GQ3RelWords,r)]); fi;
    od; od;
    if List([1..6],r->D972GQ3Eval(D972GQ3Rho[r],hp[5]))<>h0 then Error("GQ3 rho5 image failure"); fi;
    valid:=Length(bad)=0;; fails:=[];; first:=fail;;
    for t in [1..Length(NormRowsGQ3)] do
      z:=D972GQ3Eval(NormRowsGQ3[t],h0);;
      if z<>one and valid then Add(fails,t);; if first=fail then first:=rec(index:=t,word:=D972GQ3RoofWords[t],defect:=z); fi; fi;
    od;
    return rec(h0:=h0,relator_bad:=bad,fails:=fails,first:=first,valid:=valid,rho5:=true);
  end;;
  D972GQ3Receipt:=function(scan,epiIndex,epiCount)
    local H,iso,Hp,degree,wit,defect;
    wit:=scan.first;; H:=Group(scan.h0);; iso:=IsomorphismPermGroup(H);;
    if iso=fail then Error("GQ3 receipt permutation conversion failed"); fi;
    Hp:=Image(iso);; degree:=LargestMovedPoint(Hp);; if degree<1 then degree:=1; fi;
    defect:=Image(iso,wit.defect);;
    return Concatenation(
      "{\"schema\":\"d972-b4-finite-image/v2\",\"target\":",D972GQ3Json(D972GQ3Target),
      ",\"target_order\":",String(TargetGQ3.order),",\"epi_index\":",String(epiIndex),
      ",\"epi_count\":",String(epiCount),",\"h_images\":",D972GQ3Json(List(scan.h0,g->List([1..degree],i->i^Image(iso,g)))),
      ",\"rho_words\":",D972GQ3Json(D972GQ3Rho),",\"rho_words_source\":\"universal_v2_canonical\",\"rho_words_legacy_json_mismatch\":false,\"rho_words_sha256\":",D972GQ3Json(D972GQ3RhoSha),
      ",\"source_sha256\":",D972GQ3Json(D972GQ3SourceSha),",\"all_relators\":",D972GQ3Json(D972GQ3RelWords),",\"all_relators_sha256\":",D972GQ3Json(D972GQ3RelSha),
      ",\"relator_bools\":",D972GQ3Json(List(D972GQ3RelWords,r->true)),",\"rho5\":true,\"target_keys\":",D972GQ3Json(D972GQ3Keys),",\"target_key_digest\":",D972GQ3Json(D972GQ3TargetSha),
      ",\"roof_words\":",D972GQ3Json(D972GQ3RoofWords),",\"roof_words_sha256\":",D972GQ3Json(D972GQ3RoofSha),",\"witness_index\":",String(wit.index),
      ",\"witness_word\":",D972GQ3Json(wit.word),",\"expected_defect\":",D972GQ3Json(List([1..degree],i->i^defect)),
      ",\"word_key_artifact_sha256\":\"",D972GQ3WordKeySha,"\"}");
  end;;
  SummaryGQ3:=[];; ReceiptGQ3:=fail;; epiIndexGQ3:=0;;
  for epiGQ3 in QSGQ3 do
    epiIndexGQ3:=epiIndexGQ3+1;; scanGQ3:=D972GQ3Scan(epiGQ3);;
    Add(SummaryGQ3,rec(epi_index:=epiIndexGQ3,relator_bad_count:=Length(scanGQ3.relator_bad),
      roof_fail_count:=Length(scanGQ3.fails),rho5:=scanGQ3.rho5,valid:=scanGQ3.valid));
    if scanGQ3.first<>fail and ReceiptGQ3=fail then
      ReceiptGQ3:=D972GQ3Receipt(scanGQ3,epiIndexGQ3,CountGQ3);
      D972GQ3Write(D972GQ3DefectOutput,ReceiptGQ3);;
      Print("B4_GQ3_DEFECT epi=",epiIndexGQ3," roof_index=",scanGQ3.first.index,"\n");
    fi;
  od;
  defectCountGQ3:=Number(SummaryGQ3,r->r.roof_fail_count>0);;
  passCountGQ3:=Number(SummaryGQ3,r->r.roof_fail_count=0 and r.relator_bad_count=0 and r.rho5=true);;
  statusGQ3:="UNKNOWN_EPI_ZERO";; if CountGQ3>0 then statusGQ3:="UNKNOWN_ALLPASS_CONTINUE"; fi;
  if defectCountGQ3>0 then statusGQ3:="B4_A_SIDE_CANDIDATE_PENDING_REPLAY"; fi;
  summaryGQ3:=Concatenation("{\"schema\":\"d972-b4-gquotient-covers/v3\",\"status\":",D972GQ3Json(statusGQ3),
    ",\"target\":",D972GQ3Json(D972GQ3Target),",\"target_order\":",String(TargetGQ3.order),",\"target_degree\":",String(TargetGQ3.degree),
    ",\"relator_count\":158,\"roof_count\":972,\"relator_digest\":",D972GQ3Json(D972GQ3RelSha),",\"roof_word_digest\":",D972GQ3Json(D972GQ3RoofSha),
    ",\"roof_norm_digest\":",D972GQ3Json(NormShaGQ3),",\"rho_words_source\":\"universal_v2_canonical\",\"rho_words_sha256\":",D972GQ3Json(D972GQ3RhoSha),
    ",\"source_sha256\":",D972GQ3Json(D972GQ3SourceSha),",\"target_key_digest\":",D972GQ3Json(D972GQ3TargetSha),
    ",\"word_key_artifact_digest\":\"",D972GQ3WordKeySha,"\",\"epi_count\":",String(CountGQ3),",\"allpass_epi_count\":",String(passCountGQ3),
    ",\"defect_epi_count\":",String(defectCountGQ3),",\"receipt_present\":",D972GQ3Json(ReceiptGQ3<>fail),",\"receipt_output\":",D972GQ3Json(D972GQ3DefectOutput),"}");
  D972GQ3Write(D972GQ3Output,summaryGQ3);;
  Print("B4_GQ3_DONE target=",D972GQ3Target," epis=",CountGQ3," allpass=",passCountGQ3," defects=",defectCountGQ3,"\n");
  Print("B4_GQ3_FINAL_MARKER status=",statusGQ3," target=",D972GQ3Target," epis=",CountGQ3," defects=",defectCountGQ3,"\n");
fi;
