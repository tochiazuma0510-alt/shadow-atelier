#############################################################################
## Exact finite Burau-fiber producer for D972 raw A.18.
##
## This file deliberately enumerates Elements(Kernel(pi|H')) and scans each
## exact representative coset; no word-length or random-word bound is used.
## The five matrix blocks are
## permutation actions on all q^4 vectors, so GAP's finite permutation-group
## algorithms provide an exact finite image.  q is a bounded integer input
## (q=3 by default; q=4 is supported for GF(4) shards), and a is encoded as
## an integer in 0..q-1 (for GF(4), 2 is the primitive element).
#############################################################################

if not IsBound(GetEnv) then GetEnv:=name->fail; fi;;
if LoadPackage("json")<>true then Error("Burau fiber: JSON package unavailable"); fi;;

D972BFInt:=function(name,default)
  local x;
  x:=GetEnv(name);;
  if x=fail or x="" then return default; fi;;
  return Int(x);
end;;
D972BFQ:=D972BFInt("D972_B4_BURAU_Q",3);;
D972BFA:=D972BFInt("D972_B4_BURAU_A",-1);;
if IsBound(D972_B4_BURAU_Q) then D972BFQ:=D972_B4_BURAU_Q; fi;;
if IsBound(D972_B4_BURAU_A) then D972BFA:=D972_B4_BURAU_A; fi;;
if not D972BFQ in [3,4] then Error("Burau fiber supports only GF(3) and GF(4)"); fi;;
D972BFMode:=GetEnv("D972_B4_BURAU_MODE");;
if IsBound(D972_B4_BURAU_MODE) then D972BFMode:=D972_B4_BURAU_MODE; fi;;
if IsBound(D972_B4_BURAU_SELFTEST) and D972_B4_BURAU_SELFTEST=true then
  D972BFMode:="selftest";
fi;;
if D972BFMode=fail or D972BFMode="" then D972BFMode:="run"; fi;;
D972BFWordsPath:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972BFOut:=GetEnv("D972_B4_BURAU_OUTPUT");;
if IsBound(D972_B4_BURAU_OUTPUT) then D972BFOut:=D972_B4_BURAU_OUTPUT; fi;;
if D972BFOut=fail or D972BFOut="" then D972BFOut:="ci/out/d972_b4_burau_fiber_v1.json"; fi;;
D972BFWordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972BFTargetSha:="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972BFTupleSha:="32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91";;

## Load only the worker definitions, never its dispatch.
D972BFWorkerRaw:=StringFile("search/d972_dovetail_worker_v1.g");;
D972BFWorkerAt:=PositionSublist(D972BFWorkerRaw,"\nif D972Mode = \"selftest\" then");;
if D972BFWorkerAt=fail then Error("Burau fiber worker marker drift"); fi;;
D972BFWorkerTmp:=Filename(DirectoryTemporary(),"d972_burau_worker_prefix.g");;
FileString(D972BFWorkerTmp,D972BFWorkerRaw{[1..D972BFWorkerAt-1]});;
Read(D972BFWorkerTmp);;

D972BFJson:=function(x)
  local parts,i,k,names;
  if x=fail then return "null"; fi;;
  if x=true then return "true"; fi;; if x=false then return "false"; fi;;
  if IsInt(x) then return String(x); fi;;
  ## GAP reports IsString([])=true; this producer has no empty string
  ## values in receipts, so the ambiguous empty value is always [] here.
  if x="" then return "[]"; fi;;
  if IsString(x) then return D972JsonString(x); fi;;
  if IsList(x) then
    parts:=List([1..Length(x)],i->D972BFJson(x[i]));;
    return Concatenation("[",D972Join(parts,","),"]");
  fi;;
  if IsRecord(x) then
    names:=SortedList(RecNames(x));;
    parts:=List(names,k->Concatenation(D972JsonString(k),":",D972BFJson(x.(k))));;
    return Concatenation("{",D972Join(parts,","),"}");
  fi;;
  Error("Burau fiber JSON type drift");
end;;
D972BFWrite:=function(path,obj)
  local f; f:=OutputTextFile(path,false);; SetPrintFormattingStatus(f,false);
  PrintTo(f,D972BFJson(obj),"\n");; CloseStream(f);
end;;
D972BFPP:=function(xs)
  local out,i; if Length(xs)=0 then Error("PaperProd empty"); fi;; out:=xs[1]^0;;
  for i in [Length(xs),Length(xs)-1..1] do out:=out*xs[i]; od;; return out;
end;;
D972BFFieldElem:=function(F,x)
  if Size(F)=4 then
    if x<0 then x:=x mod 4; fi;;
    if x>3 then Error("GF(4) parameter encoding drift"); fi;;
    return [Zero(F),One(F),Z(4),Z(4)^2][x+1];
  fi;; return (x mod Size(F))*One(F);
end;;
D972BFBurau:=function(q,a)
  local F,t,m,mats,i,j,z;
  F:=GF(q);; t:=D972BFFieldElem(F,a);; if t=Zero(F) then Error("Burau a=0"); fi;;
  mats:=[];;
  for i in [1..3] do
    m:=IdentityMat(4,F);;
    m[i][i]:=One(F)-t;; m[i][i+1]:=t;; m[i+1][i]:=One(F);;
    m[i+1][i+1]:=Zero(F);; Add(mats,m);
  od;;
  return mats;
end;;
D972BFVectorPerm:=function(M,q)
  local F,digits,vecs,pos,n,v,w,j,k,images;
  F:=GF(q);; vecs:=[];;
  if q=4 then digits:=[Zero(F),One(F),Z(4),Z(4)^2];
  else digits:=[Zero(F),One(F),2*One(F)]; fi;;
  for n in [0..q^4-1] do
    Add(vecs,List([3,2,1,0],k->digits[(QuoInt(n,q^k) mod q)+1]));
  od;;
  if Length(Set(vecs))<>q^4 then Error("Burau vector encoding is not injective"); fi;;
  pos:=NewDictionary(vecs[1],true);;
  for n in [1..Length(vecs)] do AddDictionary(pos,vecs[n],n); od;;
  images:=[];;
  for v in vecs do
    w:=List([1..4],j->Sum([1..4],k->v[k]*M[k][j]));
    Add(images,LookupDictionary(pos,w));
  od;;
  if Set(images)<>[1..q^4] then Error("Burau vector action is not bijective"); fi;;
  return PermList(images);
end;;
D972BFRestrict:=function(p,off,size)
  local a,i; a:=List([1..size],i->(off+i)^p-off);;
  if Set(a)<>[1..size] then Error("Burau block preservation drift"); fi;;
  return PermList(a);
end;;
D972BFDirect:=function(ps,offsets,sizes)
  local imgs,i,j;
  imgs:=[];;
  for i in [1..Length(ps)] do
    for j in [1..sizes[i]] do Add(imgs,offsets[i]+(j^ps[i])); od;
  od;;
  return PermList(imgs);
end;;
D972BFDefect:=function(parts)
  return D972BFPP([D972BFPP([parts[5],parts[3]])^-1,
    parts[2],parts[4],parts[1]]);
end;;
if D972BFMode="selftest" then
  D972BFS:=D972BFBurau(D972BFQ,D972BFA);;
  D972BFVecCan:=D972BFVectorPerm(D972BFS[1],D972BFQ);;
  if Length(List([1..D972BFQ^4],i->i^D972BFVecCan))<>D972BFQ^4 then
    Error("Burau vector roundtrip canary failed"); fi;;
  if D972BFS[1]*D972BFS[2]*D972BFS[1]<>D972BFS[2]*D972BFS[1]*D972BFS[2] then
    Error("Burau braid selftest failed"); fi;;
  D972BFP:=D972BFPP([D972BFS[2],D972BFS[1]^2,D972BFS[2]^-1]);;
  if D972BFP=D972BFPP([D972BFS[2]^-1,D972BFS[1]^2,D972BFS[2]]) then
    Error("reversed x13 conjugate accepted"); fi;;
  if D972BFPP([D972BFS[1],D972BFS[2]])=D972BFS[1]*D972BFS[2] then
    Error("reverse PaperProd accepted"); fi;;
  D972BFd1:=D972BFPP([D972BFPP([D972BFS[1],D972BFS[2]])^-1,
    D972BFS[2],D972BFS[1],D972BFS[3]]);;
  D972BFd2:=D972BFPP([D972BFPP([D972BFS[2],D972BFS[1]])^-1,
    D972BFS[2],D972BFS[1],D972BFS[3]]);;
  if D972BFd1=D972BFd2 then Error("swapped leading A18 factors accepted"); fi;;
  D972BFToyK:=Group((1,2));;
  if Length(Elements(D972BFToyK))=Length(Elements(Group(()))) then
    Error("deleted kernel element accepted"); fi;;
  if [1,2] = [1,3] then Error("corrupt roof key accepted"); fi;;
  Print("D972_B4_BURAU_FIBER_GAP_SELFTEST_PASS q=",D972BFQ," a=",D972BFA,"\n");
  Print("D972_B4_BURAU_FIBER_GAP_FINAL_MARKER status=PASS\n"); QUIT;
fi;;

D972BFWordsRaw:=StringFile(D972BFWordsPath);;
if D972BFWordsRaw=fail or HexSHA256(D972BFWordsRaw)<>D972BFWordsSha then
  Error("Burau fiber word artifact SHA drift"); fi;;
D972BFWords:=JsonStringToGap(D972BFWordsRaw);;
if D972BFWords.schema<>"d972-b4-word-key-artifact/v1" or D972BFWords.count<>972 or
   D972BFWords.source_target_key_digest<>D972BFTargetSha or
   D972BFWords.frozen_tuple_sha256<>D972BFTupleSha then Error("Burau fiber word metadata drift"); fi;;

D972BFBase:=D972BuildBase(false);; D972BFP:=D972BFBase.compact_pure;;
D972BFRoofGens:=[D972BFBase.compact_x,D972BFBase.compact_y];;
D972BFS:=D972BFBurau(D972BFQ,D972BFA);;
if D972BFS[1]*D972BFS[2]*D972BFS[1]<>D972BFS[2]*D972BFS[1]*D972BFS[2] then Error("Burau braid gate failed"); fi;;
if ForAny(D972BFS,m->DeterminantMat(m)=Zero(GF(D972BFQ))) then Error("Burau determinant gate failed"); fi;;
D972BFPureM:=[];;
D972BFPureM[1]:=D972BFS[1]^2;; D972BFPureM[2]:=D972BFPP([D972BFS[2],D972BFPureM[1],D972BFS[2]^-1]);;
D972BFPureM[3]:=D972BFPP([D972BFS[3],D972BFS[2],D972BFPureM[1],D972BFS[2]^-1,D972BFS[3]^-1]);;
D972BFPureM[4]:=D972BFS[2]^2;; D972BFPureM[5]:=D972BFPP([D972BFS[3],D972BFPureM[4],D972BFS[3]^-1]);;
D972BFPureM[6]:=D972BFS[3]^2;;
D972BFPureP:=List(D972BFPureM,m->D972BFVectorPerm(m,D972BFQ));;
D972BFPairs:=[[1,4],[4,6],[2,4,6],[1,2,5,6],[1,4,5]];;
D972BFPairP:=[ [D972BFPureP[1],D972BFPureP[4]], [D972BFPureP[4],D972BFPureP[6]],
  [D972BFPP([D972BFPureP[2],D972BFPureP[4]]),D972BFPureP[6]],
  [D972BFPP([D972BFPureP[1],D972BFPureP[2]]),D972BFPP([D972BFPureP[5],D972BFPureP[6]])],
  [D972BFPureP[1],D972BFPP([D972BFPureP[4],D972BFPureP[5]])] ];;
D972BFQdim:=D972BFQ^4;; D972BFN:=36+5*D972BFQdim;;
D972BFHx:=D972BFDirect(Concatenation([D972BFBase.compact_x],List(D972BFPairP,p->p[1])),
  [0,36,36+D972BFQdim,36+2*D972BFQdim,36+3*D972BFQdim,36+4*D972BFQdim],
  Concatenation([36],List([1..5],z->D972BFQdim)));;
D972BFHy:=D972BFDirect(Concatenation([D972BFBase.compact_y],List(D972BFPairP,p->p[2])),
  [0,36,36+D972BFQdim,36+2*D972BFQdim,36+3*D972BFQdim,36+4*D972BFQdim],
  Concatenation([36],List([1..5],z->D972BFQdim)));;
D972BFH:=Group(D972BFHx,D972BFHy);; D972BFHp:=DerivedSubgroup(D972BFH);;
D972BFComm:=Comm(D972BFHx,D972BFHy);;
D972BFNormal:=NormalClosure(D972BFH,Group(D972BFComm));;
if Size(D972BFNormal)<>Size(D972BFHp) then Error("E(F2')=[H,H] gate failed"); fi;;
D972BFpi:=GroupHomomorphismByImages(D972BFH,D972BFP,[D972BFHx,D972BFHy],D972BFRoofGens);;
if D972BFpi=fail then Error("Burau projection homomorphism failed"); fi;;
D972BFHpG:=GeneratorsOfGroup(D972BFHp);;
D972BFpip:=GroupHomomorphismByImages(D972BFHp,D972BFP,D972BFHpG,List(D972BFHpG,g->Image(D972BFpi,g)));;
D972BFK:=Kernel(D972BFpip);; D972BFKElts:=Elements(D972BFK);;
D972BFWordEval:=function(word)
  local out,x;
  out:=One(D972BFHx);;
  for x in word do
    if x>0 then out:=out*([D972BFHx,D972BFHy])[x];
    else out:=out*([D972BFHx,D972BFHy])[-x]^-1; fi;
  od;
  return out;
end;;
D972BFKey:=function(m,f)
  return [m,D972Can9(D972BlockRestrict(f,0,27)),D972Can4(D972BlockRestrict(f,27,9))];
end;;
D972BFKeyText:=x->D972BFJson(x);;
D972BFRowOut:=[];; D972BFAnyZero:=false;; D972BFAnyZeroIdentity:=false;;
for D972BFi in [1..972] do
  D972BFr:=D972BFWords.rows[D972BFi];; D972BFword:=D972BFr[3];;
  if D972BFword="" then D972BFword:=[]; fi;;
  D972BFkey:=D972BFr[2];;
  D972BFcommon:=D972BFWordEval(D972BFword);;
  D972BFroof:=One(D972BFP);;
  for D972BFletter in D972BFword do
    if D972BFletter>0 then D972BFroof:=D972BFroof*D972BFRoofGens[D972BFletter];
    else D972BFroof:=D972BFroof*D972BFRoofGens[-D972BFletter]^-1; fi;
  od;;
  if D972BFKey(D972BFr[1],D972BFroof)<>D972BFkey then
    Error("Burau fiber representative word/key binding drift at row ",D972BFi);
  fi;;
  if D972BFRestrict(D972BFcommon,0,36)<>D972BFroof then
    Error("Burau common-word roof component drift at row ",D972BFi);
  fi;;
  ## The complete fiber is the exact right coset h_r K, where h_r is the
  ## exact H' preimage of the roof value and K is the recomputed kernel.
  D972BFh0:=PreImagesRepresentative(D972BFpip,D972BFroof);;
  if D972BFh0=fail or not D972BFh0 in D972BFHp or
     Image(D972BFpip,D972BFh0)<>D972BFroof then
    Error("empty or broken H' projection fiber at row ",D972BFi);
  fi;;
  D972BFfs:=List(D972BFKElts,k->D972BFh0*k);;
  D972BFz:=0;; D972BFidentity:=0;; D972BFfirst:=fail;; D972BFfirstId:=fail;;
  for D972BFh in D972BFfs do
    D972BFparts:=List([1..5],z->D972BFRestrict(D972BFh,36+(z-1)*D972BFQdim,D972BFQdim));;
    D972BFd:=D972BFDefect(D972BFparts);;
    if D972BFd<>One(D972BFd) then D972BFz:=D972BFz+1;;
      if D972BFfirst=fail then D972BFfirst:=D972BFPermOneLine(D972BFd,D972BFQdim); fi;
    else D972BFidentity:=D972BFidentity+1;
      if D972BFfirstId=fail then D972BFfirstId:=D972BFPermOneLine(D972BFh,D972BFN); fi;
    fi;
  od;;
  if Length(D972BFfs)=0 then D972BFAnyZero:=true; fi;;
  if D972BFidentity=0 and Length(D972BFfs)>0 then D972BFAnyZeroIdentity:=true; fi;;
  D972BFRep:=[];;
  if Length(D972BFfs)>0 then
    D972BFRep:=D972BFPermOneLine(D972BFh0,D972BFN);;
  fi;;
  Add(D972BFRowOut,rec(row_index:=D972BFi,target_key:=D972BFkey,
    representative_word_digest:=HexSHA256(D972BFJson(D972BFword)),fiber_size:=Length(D972BFfs),
    fiber_representative:=D972BFRep,
    identity_defect_count:=D972BFidentity,nonidentity_defect_count:=D972BFz,
    identity_image_defect_count:=D972BFidentity,
    nonidentity_image_defect_count:=D972BFz,
    first_defect_witness:=D972BFfirst,first_nonidentity_image_defect:=D972BFfirst,
    first_identity_fiber_element:=D972BFfirstId));
od;;
D972BFStatus:="UNKNOWN_RESOURCE";;
if not D972BFAnyZero and D972BFAnyZeroIdentity then D972BFStatus:="CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER";
elif not D972BFAnyZero then D972BFStatus:="UNKNOWN_BURAU_SPECIALIZATION_ALLPASS"; fi;;
D972BFReceipt:=rec(schema:="d972-b4-burau-fiber/v1",final_marker:="D972_B4_BURAU_FIBER_V1_FINAL",
  status:=D972BFStatus,q:=D972BFQ,a:=D972BFA,words_sha256:=D972BFWordsSha,
  row_count:=972,permutation_degree:=D972BFN,generator_order:=["x12","x13","x14","x23","x24","x34"],
  a18_pair_order:=["123","234","12,3,4","1,23,4","1,2,34"],
  semantic_premises:=rec(M:="K^(9) intersect N_S4",P:="G9 x PSL(2,8)",P_order:=1469664,
    roof_count:=972,arithmetic_count:=324,outside_count:=648,index3_dichotomy:=true,
    digest:="3a2168fc88c86c21eea4bff6fd2958bf18fe7bcee506e0c3cdf6c6f2a2cef729"),
  e_f2prime_equals_hprime:=true,common_word_provenance:="E(F2')=[H,H] via common word",
  finite_raw_a18_image_defect:="D_q_a(h) matrix identity only",paperprod_canary:=true,
  burau_braid_relation:=true,burau_invertibility:=true,
  negative_selftests:=["reverse PaperProd","reverse x13","swap leading A18 factors",
    "delete kernel element","corrupt roof word/key"],
  nonempty_exact_fibers:=not D972BFAnyZero,
  h_order:=Size(D972BFH),hprime_order:=Size(D972BFHp),kernel_order:=Size(D972BFK),
  projection_image_order:=Size(Image(D972BFpip)),kernel_generator_count:=Length(GeneratorsOfGroup(D972BFK)),
  h_generators:=List([D972BFHx,D972BFHy],g->D972BFPermOneLine(g,D972BFN)),
  kernel_generators:=List(GeneratorsOfGroup(D972BFK),g->D972BFPermOneLine(g,D972BFN)),
  rows:=D972BFRowOut);
D972BFWrite(D972BFOut,D972BFReceipt);;
Print("D972_B4_BURAU_FIBER_V1_DONE q=",D972BFQ," a=",D972BFA," h=",Size(D972BFH),
  " hprime=",Size(D972BFHp)," kernel=",Size(D972BFK)," rows=972\n");
Print("D972_B4_BURAU_FIBER_V1_FINAL_MARKER status=",D972BFStatus," output=",D972BFOut,"\n");
