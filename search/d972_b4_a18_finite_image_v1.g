#############################################################################
## d972_b4_a18_finite_image_v1.g
##
## Raw A.18 finite-image lane.  The presentation is exactly 18 original
## K(0,5) rows followed by the five literal images of the 28 marked rows:
## 18+5*28=158.  The 972 words are the unconditional D-tilde rows, rebuilt
## from the pinned word artifact.  No rho orbit or rho-tail is evaluated.
##
## GQuotients is run only against the fixed finite-group shelf below.  Every
## candidate receipt contains all six K(0,5) generator images in the order
## (x45,x14,x24,x15,x25,x12), and is independently replayed by
## check_d972_b4_a18_finite_image_v1.py.  All-pass and zero-epimorphism
## outcomes are UNKNOWN; a D-tilde defect is only a finite-image candidate.
##
## Controls (all optional, quote-free preamble friendly):
##   D972_B4_A18_FINITE_MODE:=selftest;;
##   D972_B4_A18_FINITE_TARGET_INDEX:=1;;
##   D972_B4_A18_FINITE_SHELF:="gquotients";;
##   D972_B4_A18_FINITE_INPUT:=...;;
##   D972_B4_A18_FINITE_WORDS:=...;;
##   D972_B4_A18_FINITE_OUTPUT:=...;;
#############################################################################

if not IsBound(GetEnv) then GetEnv:=name->fail; fi;
if LoadPackage("json")<>true then Error("A18 finite: JSON package unavailable"); fi;;

D972A18FMode:=fail;;
if IsBound(D972_B4_A18_FINITE_MODE) then D972A18FMode:=D972_B4_A18_FINITE_MODE; fi;;
if D972A18FMode=fail then D972A18FMode:=GetEnv("D972_B4_A18_FINITE_MODE"); fi;;
if D972A18FMode=fail or D972A18FMode="" then D972A18FMode:="selftest"; fi;;

D972A18FLabels:=["S3","S4","A4","A5","D10","D14","D18","D22",
  "D26","PSL2_7","PGL2_7","PSL2_8","PGL2_8","PSL2_11","SL2_11",
  "PGL2_11","PSL2_13","SL2_13","M11","PSL3_3"];;
D972A18FOrders:=[6,24,12,60,10,14,18,22,26,168,336,504,504,660,1320,
  1320,1092,2184,7920,5616];;
D972A18FTargetIndex:=fail;; D972A18FIndexSet:=false;;
if IsBound(D972_B4_A18_FINITE_TARGET_INDEX) then
  D972A18FTargetIndex:=D972_B4_A18_FINITE_TARGET_INDEX;;
  D972A18FIndexSet:=true;;
else
  D972A18FIndexEnv:=GetEnv("D972_B4_A18_FINITE_TARGET_INDEX");;
  if D972A18FIndexEnv<>fail and D972A18FIndexEnv<>"" then
    D972A18FTargetIndex:=Int(D972A18FIndexEnv);; D972A18FIndexSet:=true;;
  fi;
fi;
if D972A18FIndexSet then
  if not IsInt(D972A18FTargetIndex) or D972A18FTargetIndex<1 or
     D972A18FTargetIndex>Length(D972A18FLabels) then
    Error("A18 finite target index drift");
  fi;
  D972A18FTarget:=D972A18FLabels[D972A18FTargetIndex];;
  D972A18FMode:="target";;
else
  D972A18FTarget:="S3";;
fi;
D972A18FShelf:="gquotients";;
if IsBound(D972_B4_A18_FINITE_SHELF) then D972A18FShelf:=D972_B4_A18_FINITE_SHELF; fi;;
if D972A18FShelf=fail then D972A18FShelf:=GetEnv("D972_B4_A18_FINITE_SHELF"); fi;;
if D972A18FShelf=fail or D972A18FShelf="" then D972A18FShelf:="gquotients"; fi;;
D972A18FInput:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972A18FWords:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
if IsBound(D972_B4_A18_FINITE_INPUT) then D972A18FInput:=D972_B4_A18_FINITE_INPUT; fi;;
if IsBound(D972_B4_A18_FINITE_WORDS) then D972A18FWords:=D972_B4_A18_FINITE_WORDS; fi;;
D972A18FOutput:=fail;;
if IsBound(D972_B4_A18_FINITE_OUTPUT) then D972A18FOutput:=D972_B4_A18_FINITE_OUTPUT; fi;;
if D972A18FOutput=fail then D972A18FOutput:=GetEnv("D972_B4_A18_FINITE_OUTPUT"); fi;;
if D972A18FOutput=fail or D972A18FOutput="" then
  D972A18FOutput:=Concatenation("ci/out/d972_b4_a18_finite_image_",
    D972A18FTarget,".json");;
fi;
D972A18FDefectOutput:=Concatenation(D972A18FOutput,".defect.json");;

D972A18FSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972A18FWordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972A18FRelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972A18FA18Sha:="1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722";;
D972A18FPresSha:="783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305";;
D972A18FDtildeSha:="32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef";;
D972A18FGeneratorOrder:=["x45","x14","x24","x15","x25","x12"];;

D972A18FJoin:=function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;; out:=xs[1];;
  for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;;
  return out;
end;;
D972A18FJson:=function(x)
  local names,parts,i,key,t;
  if x=fail then return "null"; fi;;
  if x=true then return "true"; fi;;
  if x=false then return "false"; fi;;
  if IsInt(x) then return String(x); fi;;
  if IsString(x) then
    t:=ReplacedString(x,"\\","\\\\");;
    t:=ReplacedString(t,"\"","\\\"");;
    t:=ReplacedString(t,"\n","\\n");;
    t:=ReplacedString(t,"\r","\\r");;
    return Concatenation("\"",t,"\"");
  fi;
  if IsList(x) then
    if Length(x)=0 then return "[]"; fi;;
    parts:=List([1..Length(x)],i->D972A18FJson(x[i]));;
    return Concatenation("[",D972A18FJoin(parts,","),"]");
  fi;
  if IsRecord(x) then
    names:=SortedList(RecNames(x));; parts:=[];;
    for key in names do Add(parts,Concatenation(D972A18FJson(key),":",
      D972A18FJson(x.(key)))); od;;
    return Concatenation("{",D972A18FJoin(parts,","),"}");
  fi;
  Error("A18 finite JSON type drift");
end;;
D972A18FWrite:=function(path,text)
  local f;
  f:=OutputTextFile(path,false);; SetPrintFormattingStatus(f,false);
  PrintTo(f,text,"\n");; CloseStream(f);
end;;
D972A18FReduce:=function(w)
  local out,x,n;
  out:=[];;
  for x in w do
    if not IsInt(x) or x=0 then Error("A18 finite signed word drift"); fi;;
    n:=Length(out);;
    if n>0 and out[n]=-x then Remove(out,n); else Add(out,x); fi;;
  od;;
  return out;
end;;
D972A18FInverse:=function(w)
  return List(Reversed(w),x->-x);
end;;
D972A18FMarked:=function(w,a,b)
  local out,x,img;
  out:=[];;
  for x in w do
    if AbsInt(x)<>1 and AbsInt(x)<>4 then Error("A18 finite marked alphabet drift"); fi;;
    if AbsInt(x)=1 then img:=a; else img:=b; fi;;
    if x<0 then Append(out,D972A18FInverse(img)); else Append(out,img); fi;;
  od;;
  return D972A18FReduce(out);
end;;
D972A18FMaps:=[
  rec(name:="123",first:=[1],second:=[4]),
  rec(name:="234",first:=[4],second:=[6]),
  rec(name:="12,3,4",first:=[2,4],second:=[6]),
  rec(name:="1,23,4",first:=[1,2],second:=[5,6]),
  rec(name:="1,2,34",first:=[1],second:=[4,5]) ];;

D972A18FLoad:=function()
  local src,inp,rels,wsrc,winp,seeds,a18,m,allA,norms,row,j,x,norm;
  src:=StringFile(D972A18FInput);;
  if src=fail or HexSHA256(src)<>D972A18FSourceSha then Error("A18 finite source SHA drift"); fi;;
  inp:=JsonStringToGap(src);;
  if inp=fail or inp.schema<>"d972-b4-p2-magnus-input/v2" or
     inp.relator_count<>158 or Length(inp.all_relators)<>158 or
     inp.all_relators_sha256<>D972A18FRelSha then
    Error("A18 finite raw source contract drift");
  fi;;
  rels:=List(inp.all_relators,ShallowCopy);;
  if HexSHA256(D972A18FJson(rels))<>D972A18FRelSha then Error("A18 finite raw relator digest drift"); fi;;
  wsrc:=StringFile(D972A18FWords);;
  if wsrc=fail or HexSHA256(wsrc)<>D972A18FWordsSha then Error("A18 finite word SHA drift"); fi;;
  winp:=JsonStringToGap(wsrc);;
  if winp=fail or winp.schema<>"d972-b4-word-key-artifact/v1" or
     winp.count<>972 or Length(winp.rows)<>972 then Error("A18 finite word contract drift"); fi;;
  seeds:=List(rels{[19..46]},ShallowCopy);; a18:=[];;
  for m in D972A18FMaps do
    Append(a18,List(seeds,x->D972A18FMarked(x,m.first,m.second)));
  od;;
  if HexSHA256(D972A18FJson(a18))<>D972A18FA18Sha then Error("A18 finite rows digest drift"); fi;;
  allA:=Concatenation(rels{[1..18]},a18);;
  if HexSHA256(D972A18FJson(allA))<>D972A18FPresSha then Error("A18 finite presentation digest drift"); fi;;
  norms:=[];;
  for row in winp.rows do
    j:=[];;
    if row[3]="" then row[3]:=[]; fi;;
    for x in row[3] do
      if AbsInt(x)=1 then Add(j,SignInt(x)*1);
      elif AbsInt(x)=2 then Add(j,SignInt(x)*4);
      else Error("A18 finite roof alphabet drift"); fi;
    od;;
    j:=D972A18FReduce(j);;
    norm:=D972A18FReduce(Concatenation(
      D972A18FInverse(D972A18FMarked(j,[-6,-5,-3],[6])),
      D972A18FInverse(D972A18FMarked(j,[1],[-3,-2,-1])),
      D972A18FMarked(j,[4],[6]),
      D972A18FMarked(j,[-6,-5,-3],[-3,-2,-1]),
      D972A18FMarked(j,[1],[4])));
    Add(norms,norm);
  od;;
  if Length(norms)<>972 or HexSHA256(D972A18FJson(norms))<>D972A18FDtildeSha then
    Error("A18 finite D-tilde digest drift");
  fi;;
  return rec(relators:=rels,presentation:=allA,norms:=norms,
    source_sha256:=D972A18FSourceSha,word_artifact_sha256:=D972A18FWordsSha,
    relator_sha256:=D972A18FRelSha,a18_rows_sha256:=D972A18FA18Sha,
    presentation_sha256:=D972A18FPresSha,dtilde_sha256:=D972A18FDtildeSha);
end;;

D972A18FTargetGroup:=function(label)
  local G,iso,Gp,ord;
  if label="S3" then G:=SymmetricGroup(3);
  elif label="S4" then G:=SymmetricGroup(4);
  elif label="A4" then G:=AlternatingGroup(4);
  elif label="A5" then G:=AlternatingGroup(5);
  ## GAP's IsPermGroup form takes the group order (not the polygon
  ## parameter n).  Thus D10 is DihedralGroup(IsPermGroup,10), etc.
  elif label="D10" then G:=DihedralGroup(IsPermGroup,10);
  elif label="D14" then G:=DihedralGroup(IsPermGroup,14);
  elif label="D18" then G:=DihedralGroup(IsPermGroup,18);
  elif label="D22" then G:=DihedralGroup(IsPermGroup,22);
  elif label="D26" then G:=DihedralGroup(IsPermGroup,26);
  elif label="PSL2_7" then G:=PSL(2,7);
  elif label="PGL2_7" then G:=PGL(2,7);
  elif label="PSL2_8" then G:=PSL(2,8);
  elif label="PGL2_8" then G:=PGL(2,8);
  elif label="PSL2_11" then G:=PSL(2,11);
  elif label="SL2_11" then G:=SL(2,11);
  elif label="PGL2_11" then G:=PGL(2,11);
  elif label="PSL2_13" then G:=PSL(2,13);
  elif label="SL2_13" then G:=SL(2,13);
  elif label="M11" then G:=MathieuGroup(11);
  elif label="PSL3_3" then G:=PSL(3,3);
  else Error("A18 finite unknown target: ",label);
  fi;
  ord:=Size(G);; iso:=IsomorphismPermGroup(G);;
  if iso=fail then Error("A18 finite permutation conversion failed: ",label); fi;;
  Gp:=Image(iso);;
  if Size(Gp)<>ord then Error("A18 finite target order drift: ",label); fi;;
  return rec(group:=Gp,order:=ord,degree:=LargestMovedPoint(Gp));
end;;

D972A18FPermVector:=function(p,d)
  return List([1..d],i->i^p);
end;;
D972A18FSigned:=function(w,F)
  local out,x;
  out:=One(F[1]);;
  for x in w do
    if x>0 then out:=out*F[x]; else out:=out*F[-x]^-1; fi;
  od;;
  return out;
end;;
D972A18FEval:=function(w,row)
  local out,x;
  out:=One(row[1]);;
  for x in w do
    if x>0 then out:=out*row[x]; else out:=out*row[-x]^-1; fi;
  od;;
  return out;
end;;
D972A18FScan:=function(data,h,d)
  local one,bad,defects,i,z,first;
  one:=One(h[1]);; bad:=[];; defects:=[];; first:=fail;;
  for i in [1..Length(data.presentation)] do
    z:=D972A18FEval(data.presentation[i],h);;
    if z<>one then Add(bad,[i,D972A18FPermVector(z,d)]); fi;
  od;;
  if Length(bad)>0 then return rec(h:=h,raw_bad:=bad,defects:=defects,first:=first); fi;;
  for i in [1..Length(data.norms)] do
    z:=D972A18FEval(data.norms[i],h);;
    if z<>one then
      Add(defects,i);;
      if first=fail then first:=rec(index:=i,word:=data.norms[i],image:=z); fi;;
    fi;
  od;;
  return rec(h:=h,raw_bad:=bad,defects:=defects,first:=first);
end;;

## The N19 shelf is PB4, not K(0,5).  Check the central element explicitly
## and stop; this prevents a type-confused PackageGT tuple becoming a raw
## A.18 finite image.
D972A18FPackageGTN19:=function()
  local g12,g23,g13,g14,g24,g34,c;
  g12:=(1,3,2)(4,6,5);; g23:=(1,4,9)(2,7,6);;
  g13:=(1,7,5)(3,6,9);; g14:=(2,6,7)(3,8,5);;
  g24:=(1,8,6)(3,4,7);; g34:=(1,2,3)(7,9,8);;
  c:=g14*g24*g34*g12*g13*g23;;
  if c=One(c) then Error("A18 finite PackageGT N19 centre gate unexpectedly trivial"); fi;;
  return rec(schema:="d972-b4-a18-finite-image/v1",
    status:="REJECTED_PACKAGEGT_PB4_CENTER_NOT_K05", shelf:="packageGT_N19",
    presentation_semantics:="raw_a18_18_plus_140", rho_tail_used:=false,
    reason:="PB4 centre is nontrivial; no K(0,5) generator image",
    center_image:=D972A18FPermVector(c,9),
    generator_order:=D972A18FGeneratorOrder);
end;;

D972A18FSelftest:=function()
  local data,i,T,c;
  data:=D972A18FLoad();;
  if Length(data.presentation)<>158 or Length(data.norms)<>972 then
    Error("A18 finite selftest count drift");
  fi;;
  for i in [1..Length(D972A18FLabels)] do
    T:=D972A18FTargetGroup(D972A18FLabels[i]);;
    if T.order<>D972A18FOrders[i] or Size(T.group)<>D972A18FOrders[i] or T.degree<1 then
      Error("A18 finite target selftest failed: ",D972A18FLabels[i]);
    fi;;
  od;;
  c:=D972A18FPackageGTN19();;
  if c.status<>"REJECTED_PACKAGEGT_PB4_CENTER_NOT_K05" then Error("A18 finite shelf gate drift"); fi;;
  Print("D972_B4_A18_FINITE_IMAGE_V1_SELFTEST_PASS targets=",Length(D972A18FLabels),
    " presentation=158 dtilde=972 packageGT_N19=rejected_center\n");
  Print("D972_B4_A18_FINITE_IMAGE_V1_FINAL_MARKER status=PASS presentation_sha256=",
    D972A18FPresSha," dtilde_sha256=",D972A18FDtildeSha,"\n");
end;;

if D972A18FShelf="packageGT_N19" then
  D972A18FData:=D972A18FLoad();;
  D972A18FWrite(D972A18FOutput,D972A18FJson(D972A18FPackageGTN19()));;
  Print("D972_B4_A18_FINITE_IMAGE_V1_FINAL_MARKER status=REJECTED_PACKAGEGT_PB4_CENTER_NOT_K05\n");
elif D972A18FMode="selftest" then
  D972A18FSelftest();;
else
  D972A18FData:=D972A18FLoad();;
  D972A18FF6:=FreeGroup(6);; D972A18F6:=GeneratorsOfGroup(D972A18FF6);;
  D972A18FRels:=List(D972A18FData.presentation,w->D972A18FSigned(w,D972A18F6));;
  D972A18FU:=D972A18FF6/D972A18FRels;; D972A18FUgens:=GeneratorsOfGroup(D972A18FU);;
  if Length(D972A18FUgens)<>6 then Error("A18 finite U generator count drift"); fi;;
  D972A18FT:=D972A18FTargetGroup(D972A18FTarget);;
  Print("D972_B4_A18_FINITE_TARGET_BEGIN label=",D972A18FTarget,
    " order=",D972A18FT.order," degree=",D972A18FT.degree,"\n");
  D972A18FQ:=GQuotients(D972A18FU,D972A18FT.group:findall:=true);;
  D972A18FCount:=Length(D972A18FQ);; D972A18FDefectCount:=0;;
  D972A18FAllPass:=0;; D972A18FReceipt:=fail;; D972A18FIndex:=0;;
  for D972A18FEpi in D972A18FQ do
    D972A18FIndex:=D972A18FIndex+1;;
    D972A18FH:=List(D972A18FUgens,g->Image(D972A18FEpi,g));;
    if Size(Group(D972A18FH))<>D972A18FT.order then
      Error("A18 finite non-surjective quotient returned by GQuotients");
    fi;;
    D972A18FS:=D972A18FScan(D972A18FData,D972A18FH,D972A18FT.degree);;
    if Length(D972A18FS.raw_bad)=0 and Length(D972A18FS.defects)=0 then
      D972A18FAllPass:=D972A18FAllPass+1;;
    fi;;
    if Length(D972A18FS.defects)>0 then
      D972A18FDefectCount:=D972A18FDefectCount+1;;
      if D972A18FReceipt=fail then
        D972A18FFirst:=D972A18FS.first;;
        D972A18FReceipt:=rec(schema:="d972-b4-a18-finite-image/v1",
          status:="B4_A_CANDIDATE_RAW_A18_FINITE_IMAGE",
          presentation_semantics:="raw_a18_18_plus_140",rho_tail_used:=false,
          source_sha256:=D972A18FSourceSha,word_artifact_sha256:=D972A18FWordsSha,
          relator_sha256:=D972A18FRelSha,a18_rows_sha256:=D972A18FA18Sha,
          presentation_sha256:=D972A18FPresSha,dtilde_sha256:=D972A18FDtildeSha,
          target_label:=D972A18FTarget,target_order:=D972A18FT.order,
          target_degree:=D972A18FT.degree,generator_order:=D972A18FGeneratorOrder,
          generator_images:=List(D972A18FH,g->D972A18FPermVector(g,D972A18FT.degree)),
          surjective:=true,epi_index:=D972A18FIndex,epi_count:=D972A18FCount,
          raw_relator_count:=158,raw_relator_bad_count:=Length(D972A18FS.raw_bad),
          dtilde_count:=972,dtilde_defect_count:=Length(D972A18FS.defects),
          first_defect:=rec(index:=D972A18FFirst.index,word:=D972A18FFirst.word,
            image:=D972A18FPermVector(D972A18FFirst.image,D972A18FT.degree)));
        D972A18FWrite(D972A18FDefectOutput,D972A18FJson(D972A18FReceipt));;
      fi;;
    fi;;
  od;;
  if D972A18FCount=0 then D972A18FStatus:="UNKNOWN_RAW_A18_FINITE_IMAGE_NO_EPIMORPHISM";
  elif D972A18FDefectCount>0 then D972A18FStatus:="B4_A_CANDIDATE_RAW_A18_FINITE_IMAGE";
  else D972A18FStatus:="UNKNOWN_RAW_A18_FINITE_IMAGE_ALLPASS"; fi;;
  D972A18FSummary:=rec(schema:="d972-b4-a18-finite-image/v1-summary",
    status:=D972A18FStatus,presentation_semantics:="raw_a18_18_plus_140",
    rho_tail_used:=false,target_label:=D972A18FTarget,target_order:=D972A18FT.order,
    target_degree:=D972A18FT.degree,source_sha256:=D972A18FSourceSha,
    word_artifact_sha256:=D972A18FWordsSha,relator_sha256:=D972A18FRelSha,
    a18_rows_sha256:=D972A18FA18Sha,presentation_sha256:=D972A18FPresSha,
    dtilde_sha256:=D972A18FDtildeSha,raw_relator_count:=158,dtilde_count:=972,
    epi_count:=D972A18FCount,allpass_epi_count:=D972A18FAllPass,
    defect_epi_count:=D972A18FDefectCount,receipt_present:=D972A18FReceipt<>fail,
    receipt_output:=D972A18FDefectOutput);
  D972A18FWrite(D972A18FOutput,D972A18FJson(D972A18FSummary));;
  Print("D972_B4_A18_FINITE_IMAGE_V1_DONE target=",D972A18FTarget,
    " epis=",D972A18FCount," allpass=",D972A18FAllPass,
    " defects=",D972A18FDefectCount,"\n");
  Print("D972_B4_A18_FINITE_IMAGE_V1_FINAL_MARKER status=",D972A18FStatus,
    " target=",D972A18FTarget," epis=",D972A18FCount,"\n");
fi;
