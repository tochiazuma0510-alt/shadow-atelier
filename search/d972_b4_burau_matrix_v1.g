#############################################################################
## D972 B4 faithful matrix-56 Burau producer.
##
## This version never constructs the old high-degree vector permutation action.
## The roof is represented by its faithful 36x36 permutation matrix over GF(q),
## followed by five natural 4x4 Burau blocks, giving GL(56,q).
#############################################################################

if not IsBound(GetEnv) then GetEnv:=name->fail; fi;;
if LoadPackage("json")<>true then Error("matrix56: JSON package unavailable"); fi;;

D972MInt:=function(name,default)
  local x; x:=GetEnv(name);; if x=fail or x="" then return default; fi;; return Int(x);
end;;
D972MQ:=D972MInt("D972_B4_BURAU_Q",5);;
D972MA:=D972MInt("D972_B4_BURAU_A",2);;
if IsBound(D972_B4_BURAU_Q) then D972MQ:=D972_B4_BURAU_Q; fi;;
if IsBound(D972_B4_BURAU_A) then D972MA:=D972_B4_BURAU_A; fi;;
if not ([D972MQ,D972MA] in [[3,-1],[4,2],[5,2],[5,4]]) then
  Error("matrix56: unsupported registered (q,a)"); fi;;
D972MMode:=GetEnv("D972_B4_BURAU_MODE");;
if IsBound(D972_B4_BURAU_MODE) then D972MMode:=D972_B4_BURAU_MODE; fi;;
if IsBound(D972_B4_BURAU_SELFTEST) and D972_B4_BURAU_SELFTEST=true then D972MMode:="selftest"; fi;;
if D972MMode=fail or D972MMode="" then D972MMode:="run"; fi;;
if not D972MMode in ["selftest","run","calibration"] then Error("matrix56: closed mode"); fi;;
D972MWordsPath:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972MOut:=GetEnv("D972_B4_BURAU_OUTPUT");;
if IsBound(D972_B4_BURAU_OUTPUT) then D972MOut:=D972_B4_BURAU_OUTPUT; fi;;
if D972MOut=fail or D972MOut="" then D972MOut:="ci/out/d972_b4_burau_matrix_v1.json"; fi;;
D972MWordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972MTargetSha:="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972MTupleSha:="32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91";;
D972MSemSha:="3a2168fc88c86c21eea4bff6fd2958bf18fe7bcee506e0c3cdf6c6f2a2cef729";;

## Load frozen roof/helper definitions, never the worker dispatch.
D972MWorkerRaw:=StringFile("search/d972_dovetail_worker_v1.g");;
D972MWorkerAt:=PositionSublist(D972MWorkerRaw,"\nif D972Mode = \"selftest\" then");;
if D972MWorkerAt=fail then Error("matrix56: worker marker drift"); fi;;
D972MWorkerTmp:=Filename(DirectoryTemporary(),"d972_matrix56_worker_prefix.g");;
FileString(D972MWorkerTmp,D972MWorkerRaw{[1..D972MWorkerAt-1]});; Read(D972MWorkerTmp);;
D972MSourcePath:="search/d972_b4_burau_matrix_v1.g";;
D972MSourceRaw:=StringFile(D972MSourcePath);;if D972MSourceRaw=fail then Error("matrix56: producer source unavailable");fi;;
D972MSourceSha:=HexSHA256(D972MSourceRaw);;

D972MJson:=function(x)
  local parts,i,k,names;
  if x=fail then return "null"; fi;; if x=true then return "true"; fi;; if x=false then return "false"; fi;;
  if IsInt(x) then return String(x); fi;; if x="" then return "[]"; fi;;
  if IsString(x) then return D972JsonString(x); fi;;
  if IsList(x) then parts:=List([1..Length(x)],i->D972MJson(x[i])); return Concatenation("[",D972Join(parts,","),"]"); fi;;
  if IsRecord(x) then names:=SortedList(RecNames(x)); parts:=List(names,k->Concatenation(D972JsonString(k),":",D972MJson(x.(k)))); return Concatenation("{",D972Join(parts,","),"}"); fi;;
  Error("matrix56: JSON type drift");
end;;
D972MWrite:=function(path,obj)local f;f:=OutputTextFile(path,false);;SetPrintFormattingStatus(f,false);PrintTo(f,D972MJson(obj),"\n");;CloseStream(f);end;;
D972MPP:=function(xs)local out,i;if Length(xs)=0 then Error("matrix56: PaperProd empty");fi;;out:=xs[1]^0;for i in [Length(xs),Length(xs)-1..1] do out:=out*xs[i];od;return out;end;;
D972MFieldElem:=function(F,x)
  if Size(F)=4 then if x<0 then x:=x mod 4;fi;;if x>3 then Error("matrix56: GF4 encoding");fi;;return [Zero(F),One(F),Z(4),Z(4)^2][x+1];fi;; return (x mod Size(F))*One(F);
end;;
D972MBurau:=function(q,a)
  local F,t,mats,m,i;
  F:=GF(q);;t:=D972MFieldElem(F,a);;if t=Zero(F) then Error("matrix56: zero Burau parameter");fi;;mats:=[];
  for i in [1..3] do m:=IdentityMat(4,F);;m[i][i]:=One(F)-t;;m[i][i+1]:=t;;m[i+1][i]:=One(F);;m[i+1][i+1]:=Zero(F);;Add(mats,m);od;;return mats;
end;;

## Row-action matrix: R(p)R(q)=R(p*q) for GAP's right action convention.
D972MPermMat:=function(p,n,F)
  local a,i,j;
  a:=List([1..n],i->List([1..n],j->Zero(F)));;
  for i in [1..n] do a[i][i^p]:=One(F); od;; return ImmutableMatrix(F,a);
end;;
D972MBlockDiag:=function(ms,F)
  local d,a,i,j,k,n,off;
  d:=Sum(List(ms,Length));;a:=List([1..d],i->List([1..d],j->Zero(F)));;off:=0;
  for k in [1..Length(ms)] do n:=Length(ms[k]);;for i in [1..n] do for j in [1..n] do a[off+i][off+j]:=ms[k][i][j]; od; od;;off:=off+n; od;;
  return ImmutableMatrix(F,a);
end;;
D972MExtract:=function(M,off,n,F)
  return ImmutableMatrix(F,List([1..n],i->List([1..n],j->M[off+i][off+j])));
end;;
D972MRoofPerm:=function(M,F)
  local p,i,j,hit;
  p:=[];;for i in [1..36] do hit:=fail;;for j in [1..36] do if M[i][j]=One(F) then if hit<>fail then Error("matrix56: non-permutation roof row");fi;;hit:=j;fi;;od;;if hit=fail then Error("matrix56: zero roof row");fi;;Add(p,hit);od;;return PermList(p);
end;;
D972MEntry:=function(F,x)
  if Size(F)=4 then if x=Zero(F) then return 0;fi;;if x=One(F) then return 1;fi;;if x=Z(4) then return 2;fi;;return 3;fi;;return IntFFE(x);
end;;
D972MEnc:=function(M,F)return List([1..Length(M)],i->List([1..Length(M)],j->D972MEntry(F,M[i][j])));end;;
D972MDefect:=function(parts)return D972MPP([D972MPP([parts[5],parts[3]])^-1,parts[2],parts[4],parts[1]]);end;;
D972MKey:=function(m,p)return [m,D972Can9(D972BlockRestrict(p,0,27)),D972Can4(D972BlockRestrict(p,27,9))];end;;
D972MWordEval:=function(w,gens)local z,x;z:=One(gens[1]);for x in w do if x>0 then z:=z*gens[x];else z:=z*gens[-x]^-1;fi;od;return z;end;;

D972MSelfTest:=function()
  local F,s,p,q,r,aa,bb,good,bad,parts;
  F:=GF(D972MQ);;s:=D972MBurau(D972MQ,D972MA);;
  if s[1]*s[2]*s[1]<>s[2]*s[1]*s[2] or s[2]*s[3]*s[2]<>s[3]*s[2]*s[3] or s[1]*s[3]<>s[3]*s[1] then Error("matrix56: Artin selftest");fi;;
  if ForAny(s,m->DeterminantMat(m)=Zero(F)) then Error("matrix56: determinant selftest");fi;;
  p:=(1,2,3);;q:=(1,3);;r:=D972MPermMat(p*q,36,F);;if r<>D972MPermMat(p,36,F)*D972MPermMat(q,36,F) then Error("matrix56: row orientation");fi;;
  aa:=D972MBlockDiag([D972MPermMat(p,36,F),s[1],s[2],s[3],s[1],s[2]],F);;if D972MRoofPerm(aa,F)<>p then Error("matrix56: faithful extraction");fi;;
  if D972MPP([s[2],s[1]^2,s[2]^-1])=D972MPP([s[2]^-1,s[1]^2,s[2]]) then Error("matrix56: reversed x13");fi;;
  if D972MPP([s[1],s[2]])=s[1]*s[2] then Error("matrix56: PaperProd reversal");fi;;
  parts:=[s[1],s[2],s[3],s[1],s[2]];;good:=D972MDefect(parts);;bad:=D972MPP([D972MPP([parts[3],parts[5]])^-1,parts[1],parts[2],parts[4]]);;if good=bad then Error("matrix56: swapped defect");fi;;
  return true;
end;;

if D972MMode="selftest" then
  D972MSelfTest();;Print("D972_B4_BURAU_MATRIX56_GAP_SELFTEST_PASS q=",D972MQ," a=",D972MA," dim=56\n");;
  Print("D972_B4_BURAU_MATRIX56_GAP_FINAL_MARKER status=PASS\n");
else
  D972MRaw:=StringFile(D972MWordsPath);;if D972MRaw=fail or HexSHA256(D972MRaw)<>D972MWordsSha then Error("matrix56: word artifact SHA drift");fi;;
  D972MWords:=JsonStringToGap(D972MRaw);;if D972MWords.schema<>"d972-b4-word-key-artifact/v1" or D972MWords.count<>972 or D972MWords.source_target_key_digest<>D972MTargetSha or D972MWords.frozen_tuple_sha256<>D972MTupleSha then Error("matrix56: word metadata drift");fi;;
  D972MBase:=D972BuildBase(false);;D972MP:=D972MBase.compact_pure;;
  D972MRoofGens:=[D972MBase.compact_x,D972MBase.compact_y];;
  D972MF:=GF(D972MQ);;D972MS:=D972MBurau(D972MQ,D972MA);;
  if D972MS[1]*D972MS[2]*D972MS[1]<>D972MS[2]*D972MS[1]*D972MS[2] or
     D972MS[2]*D972MS[3]*D972MS[2]<>D972MS[3]*D972MS[2]*D972MS[3] or
     D972MS[1]*D972MS[3]<>D972MS[3]*D972MS[1] then Error("matrix56: Artin relation gate");fi;;
  if ForAny(D972MS,m->DeterminantMat(m)=Zero(D972MF)) then Error("matrix56: determinant gate");fi;;
  D972MPureM:=[];;D972MPureM[1]:=D972MS[1]^2;;D972MPureM[2]:=D972MPP([D972MS[2],D972MPureM[1],D972MS[2]^-1]);;
  D972MPureM[3]:=D972MPP([D972MS[3],D972MS[2],D972MPureM[1],D972MS[2]^-1,D972MS[3]^-1]);;
  D972MPureM[4]:=D972MS[2]^2;;D972MPureM[5]:=D972MPP([D972MS[3],D972MPureM[4],D972MS[3]^-1]);;D972MPureM[6]:=D972MS[3]^2;;
  D972MPairsM:=[[D972MPureM[1],D972MPureM[4]],[D972MPureM[4],D972MPureM[6]],
    [D972MPP([D972MPureM[2],D972MPureM[4]]),D972MPureM[6]],
    [D972MPP([D972MPureM[1],D972MPureM[2]]),D972MPP([D972MPureM[5],D972MPureM[6]])],
    [D972MPureM[1],D972MPP([D972MPureM[4],D972MPureM[5]])]];;
  D972MHx:=D972MBlockDiag(Concatenation([D972MPermMat(D972MBase.compact_x,36,D972MF)],List(D972MPairsM,p->p[1])),D972MF);;
  D972MHy:=D972MBlockDiag(Concatenation([D972MPermMat(D972MBase.compact_y,36,D972MF)],List(D972MPairsM,p->p[2])),D972MF);;
  if Length(D972MHx)<>56 or Length(D972MHy)<>56 then Error("matrix56: dimension drift");fi;;
  D972MH:=Group(D972MHx,D972MHy);;Print("D972_B4_BURAU_MATRIX56_PROGRESS stage=H q=",D972MQ," a=",D972MA," h=",Size(D972MH)," dim=56\n");;
  D972MFaithfulFullRoofModule:=Length(D972MHx)=56 and Length(D972MHy)=56;;
  if not D972MFaithfulFullRoofModule then Error("matrix56: faithful roof module gate");fi;;
  D972MMatrixGroupHExact:=Size(D972MH)>0;;if not D972MMatrixGroupHExact then Error("matrix56: exact H gate");fi;;
  D972MHP:=DerivedSubgroup(D972MH);;Print("D972_B4_BURAU_MATRIX56_PROGRESS stage=Hp q=",D972MQ," hp=",Size(D972MHP),"\n");;
  D972MDerivedSubgroupExact:=Size(D972MHP)>0;;if not D972MDerivedSubgroupExact then Error("matrix56: exact H' gate");fi;;
  D972MP:=Group(D972MBase.compact_x,D972MBase.compact_y);;D972MPPGrp:=DerivedSubgroup(D972MP);;
  if Size(D972MP)<>1469664 or Size(D972MPPGrp)<>367416 then Error("matrix56: roof order drift");fi;;
  D972Mpi:=GroupHomomorphismByImages(D972MH,D972MP,[D972MHx,D972MHy],D972MRoofGens);;if D972Mpi=fail or Image(D972Mpi,D972MHx)<>D972MRoofGens[1] or Image(D972Mpi,D972MHy)<>D972MRoofGens[2] then Error("matrix56: roof homomorphism failed");fi;;
  D972MHPG:=GeneratorsOfGroup(D972MHP);;D972Mpip:=GroupHomomorphismByImages(D972MHP,D972MPPGrp,D972MHPG,List(D972MHPG,g->Image(D972Mpi,g)));;if D972Mpip=fail then Error("matrix56: derived projection failed");fi;;
  D972MProjectionSurjective:=Size(Image(D972Mpip))=Size(D972MPPGrp);;if not D972MProjectionSurjective then Error("matrix56: derived projection image drift");fi;;
  D972MComm:=Comm(D972MHx,D972MHy);;D972MNormal:=NormalClosure(D972MH,Group(D972MComm));;D972MNormalClosureEqualsHPrime:=Size(D972MNormal)=Size(D972MHP);;if not D972MNormalClosureEqualsHPrime then Error("matrix56: E(F2')=[H,H] drift");fi;;
  D972MK:=Kernel(D972Mpip);;D972MKElts:=Elements(D972MK);;D972MKSet:=Set(D972MKElts);;
  D972MKernelDistinct:=Length(D972MKSet)=Length(D972MKElts);;D972MKernelRoofIdentity:=not ForAny(D972MKElts,k->D972MExtract(k,0,36,D972MF)<>IdentityMat(36,D972MF));;
  D972MKernelComplete:=Length(D972MKElts)=Size(D972MK) and D972MKernelDistinct and D972MKernelRoofIdentity;;if not D972MKernelComplete then Error("matrix56: incomplete kernel");fi;;
  D972MKernelGens:=GeneratorsOfGroup(D972MK);;D972MKernelGenCount:=Length(D972MKernelGens);;
  D972MKernelDeleted:=ShallowCopy(D972MKElts);;Remove(D972MKernelDeleted,1);;
  D972MKernelDeletionIncomplete:=Length(D972MKernelDeleted)=Size(D972MK)-1 and Length(Set(D972MKernelDeleted))=Size(D972MK)-1;
  if not D972MKernelDeletionIncomplete then Error("matrix56: deletion-negative kernel canary failed");fi;;
  Print("D972_B4_BURAU_MATRIX56_PROGRESS stage=K q=",D972MQ," k=",Size(D972MK),"\n");;
  D972MWords:=D972MWords.rows;;if Length(D972MWords)<>972 or Length(Set(List(D972MWords,r->D972MJson(r[2]))))<>972 then Error("matrix56: row/key completeness drift");fi;;
  D972MRows:=[];;D972MAnyEmpty:=false;;D972MAnyZero:=false;;D972MSignedWordReplay:=false;;D972MAllCommonWordsInHPrime:=false;;
  for D972Mi in [1..Length(D972MWords)] do
    D972Mr:=D972MWords[D972Mi];;D972Mw:=D972Mr[3];;if D972Mw="" then D972Mw:=[];fi;;
    D972Mcommon:=D972MWordEval(D972Mw,[D972MHx,D972MHy]);;D972Mroof:=D972MRoofPerm(D972MExtract(D972Mcommon,0,36,D972MF),D972MF);;
    if D972MKey(D972Mr[1],D972Mroof)<>D972Mr[2] then Error("matrix56: word/key drift row ",D972Mi);fi;;
    if not D972Mcommon in D972MHP then Error("matrix56: common word outside H' row ",D972Mi);fi;;
    D972Mh0:=PreImagesRepresentative(D972Mpip,D972Mroof);;if D972Mh0=fail or not D972Mh0 in D972MHP or Image(D972Mpip,D972Mh0)<>D972Mroof then Error("matrix56: broken H' preimage row ",D972Mi);fi;;
    D972Mcos:=List(D972MKElts,k->D972Mh0*k);;D972Mz:=0;;D972Mid:=0;;D972MFirst:=fail;;D972MFirstId:=fail;;
    for D972Mh in D972Mcos do
      D972Mparts:=List([1..5],j->D972MExtract(D972Mh,36+4*(j-1),4,D972MF));;D972Md:=D972MDefect(D972Mparts);;
      if D972Md=IdentityMat(4,D972MF) then D972Mid:=D972Mid+1;;if D972MFirstId=fail then D972MFirstId:=D972MEnc(D972Mh,D972MF);fi;;
      else D972Mz:=D972Mz+1;;if D972MFirst=fail then D972MFirst:=D972MEnc(D972Md,D972MF);fi;;fi;;
    od;;
    if Length(D972Mcos)=0 then D972MAnyEmpty:=true;fi;;if Length(D972Mcos)>0 and D972Mid=0 then D972MAnyZero:=true;fi;;
    Add(D972MRows,rec(row_index:=D972Mi,target_key:=D972Mr[2],representative_word_digest:=HexSHA256(D972MJson(D972Mw)),
      fiber_size:=Length(D972Mcos),fiber_representative_matrix:=D972MEnc(D972Mh0,D972MF),
      identity_image_defect_count:=D972Mid,nonidentity_image_defect_count:=D972Mz,
      first_defect_matrix:=D972MFirst,first_identity_fiber_element_matrix:=D972MFirstId));
    if D972Mi mod 81=0 then Print("D972_B4_BURAU_MATRIX56_PROGRESS stage=rows q=",D972MQ," done=",D972Mi,"/972 k=",Size(D972MK),"\n");fi;;
  od;;
  D972MSignedWordReplay:=true;;D972MAllCommonWordsInHPrime:=true;;
  D972MStatus:="UNKNOWN_RESOURCE";;if not D972MAnyEmpty and D972MAnyZero then D972MStatus:="CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER";elif not D972MAnyEmpty then D972MStatus:="UNKNOWN_BURAU_SPECIALIZATION_ALLPASS";fi;;
  if D972MMode="calibration" then
    if [D972MQ,D972MA] in [[3,-1],[4,2]] then
      if Size(D972MH)<>105815808 or Size(D972MHP)<>2939328 or Size(D972MK)<>8 or ForAny(D972MRows,r->r.fiber_size<>8 or r.identity_image_defect_count<>1) then Error("matrix56: calibration mismatch");fi;;
      D972MStatus:="CALIBRATION_PASS";
    else Error("matrix56: invalid calibration pair");fi;;
  fi;;
  D972MExactKernelCanary:=rec(complete:=D972MKernelComplete,order:=Size(D972MK),distinct_complete:=D972MKernelDistinct,fixes_roof_block:=D972MKernelRoofIdentity,deleted_element_incomplete:=D972MKernelDeletionIncomplete);;
  D972MKernelExact:=D972MKernelComplete and D972MProjectionSurjective;;if not D972MKernelExact then Error("matrix56: exact kernel evidence gate");fi;;
  D972MAlgorithmEvidence:=rec(faithful_full_roof_module:=D972MFaithfulFullRoofModule,matrix_group_h_exact:=D972MMatrixGroupHExact,derived_subgroup_exact:=D972MDerivedSubgroupExact,normal_closure_equals_hprime:=D972MNormalClosureEqualsHPrime,projection_surjective_to_pprime:=D972MProjectionSurjective,kernel_exact:=D972MKernelExact,kernel_elements_complete:=D972MKernelComplete,signed_word_replay:=D972MSignedWordReplay,all_common_words_in_hprime:=D972MAllCommonWordsInHPrime,no_word_bound_or_sampling:=true);;
  D972MReceipt:=rec(schema:="d972-b4-burau-matrix56/v1",final_marker:="D972_B4_BURAU_MATRIX56_FINAL",status:=D972MStatus,q:=D972MQ,a:=D972MA,producer_source_sha256:=D972MSourceSha,matrix_dimension:=56,block_layout:=[36,4,4,4,4,4],field_encoding:="GF(q) canonical; GF(4) 0,1,Z(4),Z(4)^2",words_sha256:=D972MWordsSha,source_target_key_digest:=D972MTargetSha,target_key_sha256:=D972MTargetSha,tuple_sha256:=D972MTupleSha,row_count:=972,generator_order:=["x12","x13","x14","x23","x24","x34"],a18_pair_order:=["123","234","12,3,4","1,23,4","1,2,34"],kernel_generator_count:=D972MKernelGenCount,exact_kernel_canary:=D972MExactKernelCanary,algorithm_evidence:=D972MAlgorithmEvidence,semantic_premises:=rec(P_order:=1469664,Pprime_order:=367416,roof_count:=972,arithmetic_count:=324,outside_count:=648,index3_dichotomy:=true,digest:=D972MSemSha),common_word_provenance:="E(F2')=[H,H] via common word",fiber_reconstruction:="h0 matrix times enumerated kernel_generators",finite_raw_a18_image_defect:="D_q_a(h) matrix identity only",h_order:=Size(D972MH),hprime_order:=Size(D972MHP),kernel_order:=Size(D972MK),projection_image_order:=Size(Image(D972Mpip)),h_generators:=List([D972MHx,D972MHy],g->D972MEnc(g,D972MF)),kernel_generators:=List(D972MKernelGens,g->D972MEnc(g,D972MF)),rows:=D972MRows);;
  D972MWrite(D972MOut,D972MReceipt);;if D972MMode="calibration" then Print("D972_B4_BURAU_MATRIX56_CALIBRATION_PASS q=",D972MQ," a=",D972MA," h=",Size(D972MH)," hp=",Size(D972MHP)," kernel=",Size(D972MK)," rows=972\n");fi;;Print("D972_B4_BURAU_MATRIX56_DONE q=",D972MQ," a=",D972MA," h=",Size(D972MH)," hprime=",Size(D972MHP)," kernel=",Size(D972MK)," rows=972\n");;Print("D972_B4_BURAU_MATRIX56_FINAL_MARKER status=",D972MStatus," output=",D972MOut,"\n");
fi;;
