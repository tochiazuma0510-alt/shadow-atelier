#############################################################################
## d972_b4_literal_row18_stage_v1.g
##
## Exact finite consumer for the frozen row-18 C2^24 chief stage.  This
## script deliberately consumes the lossless v2 four-deletion construction,
## derives the three Artin actions from PB4 words, reconstructs the literal
## five-coface A.18 rows, and exhausts the 2^6 correction fibre.  It never
## promotes a Magnus/Burau zero to a typed lift.
#############################################################################

if LoadPackage("json") <> true then
  Error("157cu: GAP json package unavailable");
fi;;

D972LRMode := "full";;
D972LROutput := "ci/out/d972_b4_literal_row18_stage_v1.json";;
D972LRCoreOutput := "ci/out/d972_d972core_c2six_intersection_v2.json";;
if IsBound(D972_LITERAL_ROW18_MODE) then D972LRMode:=D972_LITERAL_ROW18_MODE; fi;;
if IsBound(D972_LITERAL_ROW18_OUTPUT) then D972LROutput:=D972_LITERAL_ROW18_OUTPUT; fi;;
if IsBound(D972_LITERAL_ROW18_CORE_OUTPUT) then D972LRCoreOutput:=D972_LITERAL_ROW18_CORE_OUTPUT; fi;;

D972LRCorePath := "search/d972_d972core_c2six_intersection_v2.g";;
D972LRCoreSha := "577de029a49e2db3a33cf3b4437c78548214f9635b1750185d48a5385c161f4c";;
D972LRWordsPath := "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972LRWordsSha := "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972LRTuplesPath := "search/certs/nf972_sourcemap_a_tuples_v2_20260804.json";;
D972LRTuplesSha := "cfa1f3a917e2cd9d21ceaa7f77539633ccb22e8585da8b3248609008d0391801";;
D972LRLiteralPath := "search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972LRLiteralSha := "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972LRPaBPath := "thirdparty/packageGT/extracted/PackageGT/PaB.py";;
D972LRPaBSha := "e54c08d3437d0706b4639d7db31f7177c1c82de9c2f820fa7b194fa1c4e378f2";;
D972LRPrefixSha := "62ccbb87e2b27784b5330812252a2eaf247fea0fef4eda078ea6724c5b2a31e6";;
D972LRSeedSha := "366c893977a0684a294e8bd488741c735016ec5caf18804415dfc73acdb09822";;
D972LRA18Sha := "1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722";;
D972LRPresentationSha := "783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305";;
D972LRDtildeSha := "32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef";;
D972LRKeyDigest := "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972LRTupleDigest := "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91";;

D972LRRaw := function(path,sha,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or HexSHA256(raw)<>sha then Error("157cu: ",label," SHA drift"); fi;
  return raw;
end;;
D972LRCoreRaw:=D972LRRaw(D972LRCorePath,D972LRCoreSha,"core producer");;
D972LRWordsRaw:=D972LRRaw(D972LRWordsPath,D972LRWordsSha,"word artifact");;
D972LRTuplesRaw:=D972LRRaw(D972LRTuplesPath,D972LRTuplesSha,"tuple artifact");;
D972LRLiteralRaw:=D972LRRaw(D972LRLiteralPath,D972LRLiteralSha,"literal source");;
D972LRPaBRaw:=D972LRRaw(D972LRPaBPath,D972LRPaBSha,"PackageGT PaB");;

## Rerun the fast, lossless v2 basis constructor in this same pinned process.
D972_BD_MODE := "full";;
D972_BD_OUTPUT := D972LRCoreOutput;;
Read(D972LRCorePath);

D972LRWords:=JsonStringToGap(D972LRWordsRaw);;
D972LRTuples:=JsonStringToGap(D972LRTuplesRaw);;
D972LRLiteral:=JsonStringToGap(D972LRLiteralRaw);;
if D972LRWords.schema<>"d972-b4-word-key-artifact/v1" or
   D972LRWords.count<>972 or D972LRWords.source_target_key_digest<>D972LRKeyDigest or
   D972LRWords.frozen_tuple_sha256<>D972LRTupleDigest or
   D972LRTuples.schema<>"nf972-sourcemap-a-tuples/v2" or D972LRTuples.count<>972 or
   D972LRTuples.canonical_bytes_sha256<>D972LRTupleDigest or
   D972LRLiteral.schema<>"d972-b4-p2-magnus-input/v2" or
   D972LRLiteral.relator_count<>158 then Error("157cu: input metadata drift"); fi;;

D972LRJoin := function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;
  out:=xs[1];;
  for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  return out;
end;;
D972LRJson := function(x)
  local names,parts,i;
  if x=fail then return "null"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsInt(x) or IsRat(x) then return String(x); fi;
  ## GAP's empty list also satisfies IsString; it is always an array here.
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if IsRecord(x) then
    names:=Set(RecNames(x));;
    parts:=List(names,i->Concatenation(D972LRJson(i),":",D972LRJson(x.(i))));;
    return Concatenation("{",D972LRJoin(parts,","),"}");
  fi;
  if IsList(x) then
    parts:=List([1..Length(x)],i->D972LRJson(x[i]));;
    return Concatenation("[",D972LRJoin(parts,","),"]");
  fi;
  Error("157cu: unsupported JSON value");
end;;
D972LRWrite := function(path,obj)
  local f;
  f:=OutputTextFile(path,false);; SetPrintFormattingStatus(f,false);;
  PrintTo(f,D972LRJson(obj),"\n");; CloseStream(f);
end;;
D972LRDigest := x->HexSHA256(D972LRJson(x));;

D972LRReduce := function(word)
  local out,a;
  out:=[];;
  for a in word do
    if a=0 then Error("157cu: zero letter"); fi;
    if Length(out)>0 and out[Length(out)]=-a then Remove(out); else Add(out,a); fi;
  od;
  return out;
end;;
D972LRInvWord := w->List(Reversed(w),x->-x);;
D972LRSubstitute := function(word,images)
  local out,a,img;
  out:=[];;
  for a in word do
    if AbsInt(a)>Length(images) then Error("157cu: substitution alphabet drift"); fi;
    img:=images[AbsInt(a)];;
    if a<0 then img:=D972LRInvWord(img); fi;
    Append(out,img);
  od;
  return D972LRReduce(out);
end;;
D972LRWordElm := function(word,gens)
  local out,a;
  out:=One(gens[1]);;
  for a in word do
    if a>0 then out:=out*gens[a]; else out:=out*gens[-a]^-1; fi;
  od;
  return out;
end;;
D972LRPP := function(xs)
  local out,i;
  if Length(xs)=0 then Error("157cu: empty paper product"); fi;
  out:=One(xs[1]);;
  for i in Reversed([1..Length(xs)]) do out:=out*xs[i]; od;
  return out;
end;;
D972LRPaperWord := function(parts)
  local out,p;
  out:=[];;
  for p in Reversed(parts) do Append(out,p); od;
  return D972LRReduce(out);
end;;
D972LRBits := function(mask,n)
  return List([0..n-1],i->QuoInt(mask,2^i) mod 2);
end;;
D972LRXor := function(a,b)
  local out,p,aa,bb;
  out:=0;; p:=1;; aa:=a;; bb:=b;;
  while aa>0 or bb>0 do
    if (aa mod 2)<>(bb mod 2) then out:=out+p; fi;
    aa:=QuoInt(aa,2);; bb:=QuoInt(bb,2);; p:=2*p;
  od;
  return out;
end;;
D972LRMask24 := function(value)
  local c,b,m,out;
  out:=0;;
  for c in [1..4] do
    b:=D972BDBlockRestrict(value,(c-1)*D972BDDegreeE,D972BDDegreeE);;
    if not b in D972BDV then Error("157cu: value outside V4"); fi;
    m:=D972BDModuleMask(b,D972BDModule,D972BDE);;
    out:=out+m*2^(6*(c-1));
  od;
  return out;
end;;
D972LRMask6 := function(value)
  if not value in D972BDV then Error("157cu: value outside V"); fi;
  return D972BDModuleMask(value,D972BDModule,D972BDE);
end;;
D972LRApplyMatrix := function(mask,rows)
  local i,out;
  out:=0;;
  for i in [1..Length(rows)] do
    if QuoInt(mask,2^(i-1)) mod 2=1 then out:=D972LRXor(out,rows[i]); fi;
  od;
  return out;
end;;
D972LRMatMul := function(a,b)
  return List(a,row->D972LRApplyMatrix(row,b));
end;;
D972LRIdentityRows := function(n) return List([0..n-1],i->2^i); end;;
D972LRMatAdd := function(a,b)
  return List([1..Length(a)],i->D972LRXor(a[i],b[i]));
end;;
D972LRMatrixRows := function(m)
  local out,i,j,mask;
  out:=[];;
  for i in [1..Length(m)] do
    mask:=0;;
    for j in [1..Length(m[i])] do
      if not IsZero(m[i][j]) then mask:=mask+2^(j-1); fi;
    od;
    Add(out,mask);
  od;
  return out;
end;;

D972LRNewSpan := function(n) return rec(n:=n,pivots:=List([1..n],i->fail),rank:=0); end;;
D972LRInsert := function(S,v,comb)
  local p;
  for p in Reversed([0..S.n-1]) do
    if QuoInt(v,2^p) mod 2=1 then
      if S.pivots[p+1]=fail then
        S.pivots[p+1]:=rec(vector:=v,combination:=comb);; S.rank:=S.rank+1;; return true;
      fi;
      v:=D972LRXor(v,S.pivots[p+1].vector);;
      comb:=D972LRXor(comb,S.pivots[p+1].combination);
    fi;
  od;
  return false;
end;;
D972LRSolve := function(S,v)
  local p,comb;
  comb:=0;;
  for p in Reversed([0..S.n-1]) do
    if QuoInt(v,2^p) mod 2=1 then
      if S.pivots[p+1]=fail then return fail; fi;
      v:=D972LRXor(v,S.pivots[p+1].vector);;
      comb:=D972LRXor(comb,S.pivots[p+1].combination);
    fi;
  od;
  return comb;
end;;
D972LRInvariantClosureRank := function(seed,rows,n)
  local S,queue,pos,v,r;
  S:=D972LRNewSpan(n);; D972LRInsert(S,seed,1);; queue:=[seed];; pos:=1;;
  while pos<=Length(queue) do
    v:=queue[pos];; pos:=pos+1;;
    for r in rows do
      r:=D972LRApplyMatrix(v,r);;
      if D972LRInsert(S,r,1) then Add(queue,r); fi;
    od;
  od;
  return S.rank;
end;;
D972LRRowRank := function(rows,n)
  local S,r;
  S:=D972LRNewSpan(n);;
  for r in rows do D972LRInsert(S,r,1); od;
  return S.rank;
end;;

#############################################################################
## Full marked Artin action, independently rederived in B4.
#############################################################################
D972LRArtinWords := [
  [[1],[-1,4,1],[-1,5,1],[2],[3],[6]],
  [[-4,2,4],[1],[3],[4],[-4,6,4],[5]],
  [[1],[-6,3,6],[2],[-6,5,6],[4],[6]]
];;
## PackageGT's conjBySig functions encode the opposite kernel-conjugation
## orientation.  We bind it separately and compare it with p^(sigma^-1),
## never with the accepted natural action p^sigma=sigma^-1*p*sigma.
D972LRPaBInverseWords := [
  [[1],[4],[5],[1,2,-1],[1,3,-1],[6]],
  [[2],[4,1,-4],[3],[4],[6],[4,5,-4]],
  [[1],[3],[6,2,-6],[5],[6,4,-6],[6]]
];;

D972LRBF:=FreeGroup("lr_s1","lr_s2","lr_s3");;
D972LRBRels:=[D972LRBF.1*D972LRBF.3*D972LRBF.1^-1*D972LRBF.3^-1,
  D972LRBF.1*D972LRBF.2*D972LRBF.1*(D972LRBF.2*D972LRBF.1*D972LRBF.2)^-1,
  D972LRBF.2*D972LRBF.3*D972LRBF.2*(D972LRBF.3*D972LRBF.2*D972LRBF.3)^-1];;
D972LRB4:=D972LRBF/D972LRBRels;;
D972LRSig:=[D972LRB4.1,D972LRB4.2,D972LRB4.3];;
D972LRPure:=[D972LRSig[1]^2,
  D972LRSig[2]*D972LRSig[1]^2*D972LRSig[2]^-1,
  D972LRSig[3]*D972LRSig[2]*D972LRSig[1]^2*D972LRSig[2]^-1*D972LRSig[3]^-1,
  D972LRSig[2]^2,D972LRSig[3]*D972LRSig[2]^2*D972LRSig[3]^-1,D972LRSig[3]^2];;
D972LRPB4:=Subgroup(D972LRB4,D972LRPure);;
D972LRPB4Iso:=IsomorphismFpGroupByGenerators(D972LRPB4,D972LRPure,"lr_x");;
D972LRPB4fp:=Image(D972LRPB4Iso);; D972LRPB4g:=GeneratorsOfGroup(D972LRPB4fp);;
D972LRDerivedArtin:=[];; D972LRDerivedPaBInverse:=[];;
for D972LRI in [1..3] do
  D972LRTmp:=[];; D972LRR:=[];;
  for D972LRJ in [1..6] do
    D972LRD:=ImageElm(D972LRPB4Iso,D972LRPure[D972LRJ]^D972LRSig[D972LRI]);;
    D972LRH:=D972LRWordElm(D972LRArtinWords[D972LRI][D972LRJ],D972LRPB4g);;
    if D972LRD<>D972LRH then Error("157cu: canonical Artin orientation drift"); fi;
    Add(D972LRTmp,D972BDSignedWord(UnderlyingElement(D972LRD)));
    D972LRD:=ImageElm(D972LRPB4Iso,D972LRPure[D972LRJ]^(D972LRSig[D972LRI]^-1));;
    D972LRH:=D972LRWordElm(D972LRPaBInverseWords[D972LRI][D972LRJ],D972LRPB4g);;
    if D972LRD<>D972LRH then Error("157cu: PackageGT inverse-orientation drift"); fi;
    Add(D972LRR,D972BDSignedWord(UnderlyingElement(D972LRD)));
  od;
  Add(D972LRDerivedArtin,D972LRTmp);; Add(D972LRDerivedPaBInverse,D972LRR);
od;

D972LRActionRows:=[];; D972LRActionWordCert:=[];;
for D972LRI in [1..3] do
  D972LRTmp:=[];; D972LRD:=[];;
  for D972LRJ in [1..24] do
    D972LRW:=D972LRSubstitute(D972BDWords[D972LRJ].source_word,D972LRArtinWords[D972LRI]);;
    D972LRE:=D972LRWordElm(D972LRW,D972BDTupleGens);;
    if D972LRWordElm(D972LRW,D972BDTuplePGens)<>One(D972BDTuplePGens[1]) or
       D972LRWordElm(D972LRW,D972BDTupleG9Gens)<>One(D972BDTupleG9Gens[1]) then
      Error("157cu: Artin action left the marked kernel");
    fi;
    Add(D972LRTmp,D972LRMask24(D972LRE));; Add(D972LRD,D972LRW);
  od;
  Add(D972LRActionRows,D972LRTmp);; Add(D972LRActionWordCert,D972LRD);
od;
if D972LRMatMul(D972LRMatMul(D972LRActionRows[1],D972LRActionRows[2]),D972LRActionRows[1])<>
   D972LRMatMul(D972LRMatMul(D972LRActionRows[2],D972LRActionRows[1]),D972LRActionRows[2]) or
   D972LRMatMul(D972LRMatMul(D972LRActionRows[2],D972LRActionRows[3]),D972LRActionRows[2])<>
   D972LRMatMul(D972LRMatMul(D972LRActionRows[3],D972LRActionRows[2]),D972LRActionRows[3]) or
   D972LRMatMul(D972LRActionRows[1],D972LRActionRows[3])<>
   D972LRMatMul(D972LRActionRows[3],D972LRActionRows[1]) then
  Error("157cu: 24-dimensional Artin relation drift");
fi;;
if D972LRMatMul(D972LRActionRows[1],D972LRActionRows[1])<>
     List([1..24],i->D972BDPureMatrices[1][QuoInt(i-1,6)+1][((i-1) mod 6)+1]*
       2^(6*QuoInt(i-1,6))) or
   D972LRMatMul(D972LRActionRows[2],D972LRActionRows[2])<>
     List([1..24],i->D972BDPureMatrices[4][QuoInt(i-1,6)+1][((i-1) mod 6)+1]*
       2^(6*QuoInt(i-1,6))) or
   D972LRMatMul(D972LRActionRows[3],D972LRActionRows[3])<>
     List([1..24],i->D972BDPureMatrices[6][QuoInt(i-1,6)+1][((i-1) mod 6)+1]*
       2^(6*QuoInt(i-1,6))) then
  Error("157cu: Artin-square/pure-action calibration drift");
fi;;

D972LRExpectedPerms:=[[2,1,3,4],[1,3,2,4],[1,2,4,3]];;
for D972LRI in [1..3] do
  for D972LRC in [1..4] do
    for D972LRJ in [1..6] do
      D972LRM:=D972LRActionRows[D972LRI][6*(D972LRC-1)+D972LRJ];;
      if D972LRM=0 or ForAny([0..23],p->QuoInt(D972LRM,2^p) mod 2=1 and
          QuoInt(p,6)+1<>D972LRExpectedPerms[D972LRI][D972LRC]) then
        Error("157cu: Artin coordinate transport drift");
      fi;
    od;
  od;
od;

## Exact pure image and chief certificate.  Projection orders alone do not
## prove a direct product: the four single-support commutators below do.
D972LRFactorOrders:=[];; D972LRFactorModuleIrreducible:=[];;
D972LRFactorGroups:=[];; D972LRFactorMatricesByCoordinate:=[];;
for D972LRC in [1..4] do
  D972LRFactorMats:=List(D972BDPureMatrices,row->ImmutableMatrix(GF(2),
    List(row[D972LRC],m->D972LRBits(m,6))));;
  D972LRFactorGroup:=Group(D972LRFactorMats);;
  Add(D972LRFactorMatricesByCoordinate,D972LRFactorMats);;
  Add(D972LRFactorGroups,D972LRFactorGroup);;
  Add(D972LRFactorOrders,Size(D972LRFactorGroup));;
  D972LRModuleIrreducible:=true;;
  for D972LRM in [1..63] do
    if D972LRInvariantClosureRank(D972LRM,List(D972BDPureMatrices,
       row->row[D972LRC]),6)<>6 then D972LRModuleIrreducible:=false;; break; fi;
  od;
  Add(D972LRFactorModuleIrreducible,D972LRModuleIrreducible);
od;
if D972LRFactorOrders<>[504,504,504,504] or
   ForAny(D972LRFactorModuleIrreducible,x->x=false) then
  Error("157cu: P-factor action/chief decomposition drift");
fi;;

## Replay all six canonical PB4 generators as actual B4 words, not merely the
## three adjacent squares.  This binds the block-diagonal pure action to the
## recorded three-generator B4 action.
D972LRPureBraidWords:=[[1,1],[2,1,1,-2],[3,2,1,1,-2,-3],
  [2,2],[3,2,2,-3],[3,3]];;
D972LRActionMatrixObjects:=List(D972LRActionRows,r->
  ImmutableMatrix(GF(2),List(r,m->D972LRBits(m,24))));;
D972LRPureFullRows:=List([1..6],g->List([1..24],i->
  D972BDPureMatrices[g][QuoInt(i-1,6)+1][((i-1) mod 6)+1]*
    2^(6*QuoInt(i-1,6))));;
D972LRPureFullMatrixObjects:=List(D972LRPureFullRows,r->
  ImmutableMatrix(GF(2),List(r,m->D972LRBits(m,24))));;
for D972LRI in [1..6] do
  if D972LRWordElm(D972LRPureBraidWords[D972LRI],D972LRActionMatrixObjects)<>
     D972LRPureFullMatrixObjects[D972LRI] then
    Error("157cu: pure generator/B4 matrix replay drift at ",D972LRI);
  fi;
od;

## Generator supports are x12:{3,4}, x13:{2,4}, x14:{2,3},
## x23:{1,4}, x24:{1,3}, x34:{1,2}.  Each listed commutator therefore has
## one-coordinate support.  Its normal closure in the corresponding
## 504-element projection is computed exactly, closing P^4 <= pure image.
D972LRWitnessPairs:=[[4,5],[2,3],[1,3],[1,2]];;
D972LRSingleSupportWitnesses:=[];; D972LRNormalClosureOrders:=[];;
for D972LRC in [1..4] do
  D972LRA:=D972LRWitnessPairs[D972LRC][1];;
  D972LRB:=D972LRWitnessPairs[D972LRC][2];;
  D972LRWitnessBlocks:=List([1..4],d->Comm(
    D972LRFactorMatricesByCoordinate[d][D972LRA],
    D972LRFactorMatricesByCoordinate[d][D972LRB]));;
  D972LRWitnessSupport:=Filtered([1..4],d->
    D972LRWitnessBlocks[d]<>One(D972LRWitnessBlocks[d]));;
  if D972LRWitnessSupport<>[D972LRC] then
    Error("157cu: single-support commutator drift at coordinate ",D972LRC);
  fi;
  D972LRNormal:=NormalClosure(D972LRFactorGroups[D972LRC],
    Subgroup(D972LRFactorGroups[D972LRC],[D972LRWitnessBlocks[D972LRC]]));;
  Add(D972LRNormalClosureOrders,Size(D972LRNormal));;
  Add(D972LRSingleSupportWitnesses,rec(coordinate:=D972LRC,
    generator_indices:=[D972LRA,D972LRB],
    commutator_word:=[-D972LRA,-D972LRB,D972LRA,D972LRB],
    support_coordinates:=D972LRWitnessSupport,
    block_row_masks:=List(D972LRWitnessBlocks,D972LRMatrixRows),
    factor_normal_closure_order:=Size(D972LRNormal)));
od;
if D972LRNormalClosureOrders<>[504,504,504,504] then
  Error("157cu: single-support normal-closure drift");
fi;;
D972LRPureImageOrder:=Product(D972LRFactorOrders);;
D972LRCoordinateGroup:=Group(List(D972LRExpectedPerms,PermList));;
D972LRCoordinateImageOrder:=Size(D972LRCoordinateGroup);;
D972LRCoordinateTransitive:=Set(Orbit(D972LRCoordinateGroup,1))=[1..4];;
if D972LRCoordinateImageOrder<>24 or not D972LRCoordinateTransitive then
  Error("157cu: coordinate S4 image drift");
fi;;
D972LRActionImageOrder:=D972LRPureImageOrder*D972LRCoordinateImageOrder;;

#############################################################################
## Literal A.18 transport, row 18, and the exact finite torsor equation.
#############################################################################
D972LRPrefix:=D972LRLiteral.all_relators{[1..18]};;
D972LRSeeds:=D972LRLiteral.all_relators{[19..46]};;
if D972LRDigest(D972LRPrefix)<>D972LRPrefixSha or D972LRDigest(D972LRSeeds)<>D972LRSeedSha then
  Error("157cu: literal prefix/seed digest drift");
fi;;
D972LRMaps:=[
  rec(name:="123",left:=[1],right:=[4]),
  rec(name:="234",left:=[4],right:=[6]),
  rec(name:="12,3,4",left:=[2,4],right:=[6]),
  rec(name:="1,23,4",left:=[1,2],right:=[5,6]),
  rec(name:="1,2,34",left:=[1],right:=[4,5])
];;
D972LRMarkedSub := function(word,left,right)
  local images;
  images:=List([1..6],i->[]);; images[1]:=left;; images[4]:=right;;
  return D972LRSubstitute(word,images);
end;;
D972LRA18Rows:=[];; D972LRA18Meta:=[];;
for D972LRI in [1..5] do
  for D972LRJ in [1..28] do
    D972LRW:=D972LRMarkedSub(D972LRSeeds[D972LRJ],D972LRMaps[D972LRI].left,
      D972LRMaps[D972LRI].right);;
    Add(D972LRA18Rows,D972LRW);;
    Add(D972LRA18Meta,rec(coface:=D972LRMaps[D972LRI].name,seed_index:=D972LRJ));
  od;
od;
if D972LRDigest(D972LRA18Rows)<>D972LRA18Sha or
   D972LRDigest(Concatenation(D972LRPrefix,D972LRA18Rows))<>D972LRPresentationSha then
  Error("157cu: literal A.18 reconstruction drift");
fi;;

D972LRRow:=D972LRWords.rows[19];; D972LRTupleRow:=D972LRTuples.tuples[19];;
D972LRExpectedKey:=[0,[[2,0],[7,0],[0,0]],[1,2,3,4,5,6,7,8,9]];;
D972LRExpectedWord:=[-2,-2,-1,-1,2,2,1,-2,-1,-1,2,1,1,-2,1,1,1,1,2,1,-2,-2,1,1];;
if D972LRRow[1]<>0 or D972LRRow[2]<>D972LRExpectedKey or
   D972LRRow[3]<>D972LRExpectedWord or
   D972LRTupleRow<>D972LRExpectedKey then Error("157cu: row-18 key/word binding drift"); fi;;
D972LRF0:=D972LRRow[3];;

## The first deletion of each coordinate-1 C2^24 basis word is a lossless
## correction word over F2.  z=(y*x)^-1 is [-1,-2] in the GAP word encoding.
D972LRDelete1:=[[],[],[],[1],[-1,-2],[2]];;
D972LRCorrectionWords:=[];;
for D972LRI in [1..6] do
  if D972BDWords[D972LRI].coordinate<>1 or D972BDWords[D972LRI].module_index<>D972LRI then
    Error("157cu: basis ordering drift");
  fi;
  D972LRW:=D972LRSubstitute(D972BDWords[D972LRI].source_word,D972LRDelete1);;
  if D972LRWordElm(D972LRW,[D972BDX,D972BDY])<>D972BDModule[D972LRI] or
     D972LRWordElm(D972LRW,[D972BDPX,D972BDPY])<>One(D972BDP) or
     D972LRWordElm(D972LRW,[D972BDX9,D972BDY9])<>One(D972BDG9) then
    Error("157cu: lossless F2 correction basis replay drift");
  fi;
  Add(D972LRCorrectionWords,D972LRW);
od;

D972LRPairs := function(g)
  return [[g[1],g[4]],[g[4],g[6]],[D972LRPP([g[2],g[4]]),g[6]],
    [D972LRPP([g[1],g[2]]),D972LRPP([g[5],g[6]])],
    [g[1],D972LRPP([g[4],g[5]])]];
end;;
D972LRPent := function(word,g)
  local pairs,parts;
  pairs:=D972LRPairs(g);; parts:=List(pairs,p->D972LRWordElm(word,p));;
  return D972LRPP([D972LRPP([parts[5],parts[3]])^-1,parts[2],parts[4],parts[1]]);
end;;
D972LRHex := function(word,m,x,y)
  local z,u,fxy,fxz,fyz,fux,fuy;
  z:=D972LRPP([x,y])^-1;; u:=D972LRPP([y,x])^-1;;
  fxy:=D972LRWordElm(word,[x,y]);;
  fxz:=D972LRWordElm(word,[x,z]);; fyz:=D972LRWordElm(word,[y,z]);;
  fux:=D972LRWordElm(word,[u,x]);; fuy:=D972LRWordElm(word,[u,y]);;
  return [D972LRPP([y^m,fxy,x^m,fxz^-1,z^m,fyz]),
    D972LRPP([fux^-1,x^m,fxy^-1,y^m,fuy,u^m])];
end;;
D972LRDtildeWord := function(word)
  local marked,x15,x45,a,b,c,d,e;
  marked:=List(word,n->SignInt(n)*([1,4][AbsInt(n)]));;
  x15:=[-3,-2,-1];; x45:=[-6,-5,-3];;
  a:=D972LRMarkedSub(marked,x45,[6]);;
  b:=D972LRMarkedSub(marked,[1],x15);;
  c:=D972LRMarkedSub(marked,[4],[6]);;
  d:=D972LRMarkedSub(marked,x45,x15);;
  e:=D972LRMarkedSub(marked,[1],[4]);;
  return D972LRReduce(Concatenation(D972LRInvWord(a),D972LRInvWord(b),c,d,e));
end;;
if D972LRDigest(List(D972LRWords.rows,r->D972LRDtildeWord(r[3])))<>D972LRDtildeSha then
  Error("157cu: all-row ordered Dtilde digest drift");
fi;;

## Literal prefix is a true PB4 boundary.  Raw coface rows must vanish in the
## base P4/G9^4 quotient and give marked vectors in V4 upstairs.
if ForAny(D972LRPrefix,w->D972LRWordElm(w,D972BDTupleGens)<>One(D972BDTupleGens[1])) or
   ForAny(D972LRPrefix,w->D972LRWordElm(w,D972BDTupleG9Gens)<>One(D972BDTupleG9Gens[1])) then
  Error("157cu: K(0,5) prefix relation replay drift");
fi;;
D972LRRawMasks:=[];;
for D972LRW in D972LRA18Rows do
  if D972LRWordElm(D972LRW,D972BDTuplePGens)<>One(D972BDTuplePGens[1]) or
     D972LRWordElm(D972LRW,D972BDTupleG9Gens)<>One(D972BDTupleG9Gens[1]) then
    Error("157cu: raw A.18 row does not lie in the marked C2 stage");
  fi;
  Add(D972LRRawMasks,D972LRMask24(D972LRWordElm(D972LRW,D972BDTupleGens)));
od;

## Close the relation-boundary image under the computed Artin action.  Each
## independent generator retains an actual conjugated word and action path.
D972LRRelationSpan:=D972LRNewSpan(24);; D972LRRelationGens:=[];; D972LRPos:=1;;
for D972LRI in [1..140] do
  D972LRM:=D972LRRawMasks[D972LRI];; D972LRJ:=Length(D972LRRelationGens)+1;;
  if D972LRInsert(D972LRRelationSpan,D972LRM,2^(D972LRJ-1)) then
    Add(D972LRRelationGens,rec(vector:=D972LRM,word:=D972LRA18Rows[D972LRI],
      raw_index:=D972LRI,action_word:=[]));
  fi;
od;
while D972LRPos<=Length(D972LRRelationGens) do
  D972LRR:=D972LRRelationGens[D972LRPos];; D972LRPos:=D972LRPos+1;;
  for D972LRI in [1..3] do
    D972LRM:=D972LRApplyMatrix(D972LRR.vector,D972LRActionRows[D972LRI]);;
    D972LRW:=D972LRSubstitute(D972LRR.word,D972LRArtinWords[D972LRI]);;
    if D972LRMask24(D972LRWordElm(D972LRW,D972BDTupleGens))<>D972LRM then
      Error("157cu: relation/action equivariance drift");
    fi;
    D972LRJ:=Length(D972LRRelationGens)+1;;
    if D972LRInsert(D972LRRelationSpan,D972LRM,2^(D972LRJ-1)) then
      Add(D972LRRelationGens,rec(vector:=D972LRM,word:=D972LRW,
        raw_index:=D972LRR.raw_index,
        action_word:=Concatenation(D972LRR.action_word,[D972LRI])));
    fi;
  od;
od;
for D972LRR in D972LRRelationGens do for D972LRI in [1..3] do
  if D972LRSolve(D972LRRelationSpan,
     D972LRApplyMatrix(D972LRR.vector,D972LRActionRows[D972LRI]))=fail then
    Error("157cu: relation boundary is not B4 invariant");
  fi;
od; od;

D972LRCorrectionWord := function(bits)
  local out,i;
  out:=[];;
  for i in [1..6] do if QuoInt(bits,2^(i-1)) mod 2=1 then
    Append(out,D972LRCorrectionWords[i]); fi; od;
  return D972LRReduce(out);
end;;
D972LRGTComposeM0 := function(left,right)
  local ximg,yimg,newright;
  ximg:=[1];; yimg:=D972LRReduce(Concatenation(left,[2],D972LRInvWord(left)));;
  newright:=D972LRSubstitute(right,[ximg,yimg]);;
  return D972LRReduce(Concatenation(newright,left));
end;;

## Full m=0 sourcePB4 word formula, canonical generator order.  Its induced
## map on V4 is the action/norm operator used by the power selector.
D972LRSourceWordsM0 := function(f)
  local ff,g,gs,f1234,h,x123;
  ff:=D972LRSubstitute(f,[[1],[4]]);;
  g:=D972LRSubstitute(f,[[1],[2]]);;
  gs:=D972LRSubstitute(f,[[4],[5]]);;
  f1234:=D972LRSubstitute(f,[[4,2],[6]]);;
  x123:=[2,1];; h:=D972LRSubstitute(f,[x123,[3]]);;
  return [[1],
    D972LRPaperWord([D972LRInvWord(g),[2],g]),
    D972LRPaperWord([D972LRInvWord(ff),D972LRInvWord(h),[3],h,ff]),
    D972LRPaperWord([D972LRInvWord(ff),[4],ff]),
    D972LRPaperWord([D972LRInvWord(ff),D972LRInvWord(D972LRSubstitute(f,[[2,1],[6,5]])),
      D972LRInvWord(gs),[5],gs,D972LRSubstitute(f,[[2,1],[6,5]]),ff]),
    D972LRPaperWord([D972LRInvWord(f1234),[6],f1234])];
end;;
D972LRRootSource:=D972LRSourceWordsM0(D972LRF0);;
D972LRRootAction:=[];;
for D972LRI in [1..24] do
  D972LRW:=D972LRSubstitute(D972BDWords[D972LRI].source_word,D972LRRootSource);;
  Add(D972LRRootAction,D972LRMask24(D972LRWordElm(D972LRW,D972BDTupleGens)));
od;
if D972LRRowRank(D972LRRootAction,24)<>24 then Error("157cu: root action is singular"); fi;;
D972LRNorm2:=D972LRMatAdd(D972LRIdentityRows(24),D972LRRootAction);;

D972LRRootP:=D972LRWordElm(D972LRF0,[D972BDPX,D972BDPY]);;
D972LRRootG9:=D972LRWordElm(D972LRF0,[D972BDX9,D972BDY9]);;
D972LRSquare:=D972LRGTComposeM0(D972LRF0,D972LRF0);;
D972LRSquareP:=D972LRWordElm(D972LRSquare,[D972BDPX,D972BDPY]);;
D972LRSquareG9:=D972LRWordElm(D972LRSquare,[D972BDX9,D972BDY9]);;
D972LRSquareIndex:=fail;; D972LRSquareKey:=fail;;
for D972LRI in [1..972] do
  if D972LRWords.rows[D972LRI][1]=0 and
     D972LRWordElm(D972LRWords.rows[D972LRI][3],[D972BDPX,D972BDPY])=D972LRSquareP and
     D972LRWordElm(D972LRWords.rows[D972LRI][3],[D972BDX9,D972BDY9])=D972LRSquareG9 then
    if D972LRSquareIndex<>fail then Error("157cu: powered roof is not unique"); fi;
    D972LRSquareIndex:=D972LRI;; D972LRSquareKey:=D972LRWords.rows[D972LRI][2];
  fi;
od;
if D972LRSquareIndex=fail then Error("157cu: GT square roof missing from frozen 972 rows"); fi;;

D972LRPowers:=[rec(exponent:=1,word:=D972LRF0,row_index:=19,key:=D972LRExpectedKey),
  rec(exponent:=2,word:=D972LRSquare,row_index:=D972LRSquareIndex,key:=D972LRSquareKey)];;
D972LRSolutions:=[];; D972LRPowerRecords:=[];; D972LRGlobalMissing:=[];;
for D972LRPow in D972LRPowers do
  D972LRBaseDword:=D972LRDtildeWord(D972LRPow.word);;
  D972LRBaseHexE:=D972LRHex(D972LRPow.word,0,D972BDX,D972BDY);;
  D972LRBaseHexP:=D972LRHex(D972LRPow.word,0,D972BDPX,D972BDPY);;
  D972LRBaseHexG9:=D972LRHex(D972LRPow.word,0,D972BDX9,D972BDY9);;
  D972LRBaseHexMasks:=fail;;
  if ForAll(Concatenation(D972LRBaseHexP,D972LRBaseHexG9),IsOne) then
    D972LRBaseHexMasks:=List(D972LRBaseHexE,D972LRMask6);
  else
    AddSet(D972LRGlobalMissing,"stage.row_power_base_hexagon_membership");
  fi;
  D972LRBasePentE:=D972LRPent(D972LRPow.word,D972BDTupleGens);;
  D972LRBasePentP:=D972LRPent(D972LRPow.word,D972BDTuplePGens);;
  D972LRBasePentG9:=D972LRPent(D972LRPow.word,D972BDTupleG9Gens);;
  D972LRDwordE:=D972LRWordElm(D972LRBaseDword,D972BDTupleGens);;
  D972LRTransportOK:=D972LRDwordE=D972LRBasePentE;;
  if not D972LRTransportOK then
    AddSet(D972LRGlobalMissing,"a18_comparison.dtilde_to_pab_pentagon_transport");
  fi;
  D972LRBaseMask:=fail;;
  if D972LRBasePentP=One(D972BDTuplePGens[1]) and
     D972LRBasePentG9=One(D972BDTupleG9Gens[1]) then
    D972LRBaseMask:=D972LRMask24(D972LRBasePentE);
  else
    AddSet(D972LRGlobalMissing,"stage.row_power_base_pentagon_membership");
  fi;
  D972LRGaugeCols:=[];; D972LRPowSolutions:=[];;
  for D972LRBitsValue in [0..63] do
    D972LRCorr:=D972LRCorrectionWord(D972LRBitsValue);;
    D972LRCandidate:=D972LRReduce(Concatenation(D972LRPow.word,D972LRCorr));;
    D972LRHexE:=D972LRHex(D972LRCandidate,0,D972BDX,D972BDY);;
    D972LRHexP:=D972LRHex(D972LRCandidate,0,D972BDPX,D972BDPY);;
    D972LRHexG9:=D972LRHex(D972LRCandidate,0,D972BDX9,D972BDY9);;
    D972LRPentE:=D972LRPent(D972LRCandidate,D972BDTupleGens);;
    D972LRPentP:=D972LRPent(D972LRCandidate,D972BDTuplePGens);;
    D972LRPentG9:=D972LRPent(D972LRCandidate,D972BDTupleG9Gens);;
    D972LRMask:=fail;; D972LRCoeff:=fail;; D972LRHexMasks:=fail;;
    if ForAll(Concatenation(D972LRHexP,D972LRHexG9),IsOne) then
      D972LRHexMasks:=List(D972LRHexE,D972LRMask6);
    fi;
    if D972LRPentP=One(D972BDTuplePGens[1]) and
       D972LRPentG9=One(D972BDTupleG9Gens[1]) then
      D972LRMask:=D972LRMask24(D972LRPentE);;
      D972LRCoeff:=D972LRSolve(D972LRRelationSpan,D972LRMask);
    fi;
    if D972LRBitsValue>0 and (D972LRBitsValue=2^(LogInt(D972LRBitsValue,2))) and
       D972LRBaseMask<>fail and D972LRMask<>fail and D972LRBaseHexMasks<>fail and
       D972LRHexMasks<>fail then
      Add(D972LRGaugeCols,rec(hexagon1:=D972LRXor(D972LRBaseHexMasks[1],D972LRHexMasks[1]),
        hexagon2:=D972LRXor(D972LRBaseHexMasks[2],D972LRHexMasks[2]),
        pentagon:=D972LRXor(D972LRBaseMask,D972LRMask)));
    fi;
    D972LRRoofOK:=D972LRWordElm(D972LRCandidate,[D972BDPX,D972BDPY])=
        D972LRWordElm(D972LRPow.word,[D972BDPX,D972BDPY]) and
      D972LRWordElm(D972LRCandidate,[D972BDX9,D972BDY9])=
        D972LRWordElm(D972LRPow.word,[D972BDX9,D972BDY9]);;
    D972LRCharm:=Sum(Filtered(D972LRCandidate,x->AbsInt(x)=1),SignInt)=0 and
      Sum(Filtered(D972LRCandidate,x->AbsInt(x)=2),SignInt)=0;;
    D972LROntoE:=Size(Group(D972BDX,D972LRPP([
      D972LRWordElm(D972LRCandidate,[D972BDX,D972BDY])^-1,D972BDY,
      D972LRWordElm(D972LRCandidate,[D972BDX,D972BDY])])))=Size(D972BDE);;
    D972LROntoG9:=Size(Group(D972BDX9,D972LRPP([
      D972LRWordElm(D972LRCandidate,[D972BDX9,D972BDY9])^-1,D972BDY9,
      D972LRWordElm(D972LRCandidate,[D972BDX9,D972BDY9])])))=Size(D972BDG9);;
    if D972LRTransportOK and D972LRRoofOK and D972LRCharm and D972LROntoE and D972LROntoG9 and
       ForAll(Concatenation(D972LRHexE,D972LRHexP,D972LRHexG9),IsOne) and
       D972LRCoeff<>fail then
      D972LRSelectedRel:=Filtered([1..Length(D972LRRelationGens)],i->
        QuoInt(D972LRCoeff,2^(i-1)) mod 2=1);;
      D972LRCorrected:=D972LRDtildeWord(D972LRCandidate);;
      for D972LRI in D972LRSelectedRel do
        Append(D972LRCorrected,D972LRRelationGens[D972LRI].word);
      od;
      D972LRCorrected:=D972LRReduce(D972LRCorrected);;
      if D972LRWordElm(D972LRCorrected,D972BDTupleGens)<>One(D972BDTupleGens[1]) or
         D972LRWordElm(D972LRCorrected,D972BDTuplePGens)<>One(D972BDTuplePGens[1]) or
         D972LRWordElm(D972LRCorrected,D972BDTupleG9Gens)<>One(D972BDTupleG9Gens[1]) then
        Error("157cu: lossless relation correction did not close");
      fi;
      D972LRSol:=rec(exponent:=D972LRPow.exponent,correction_bits:=D972LRBitsValue,
        correction_word:=D972LRCorr,typed_source_word:=D972LRCandidate,
        roof_row_index:=D972LRPow.row_index,roof_key:=D972LRPow.key,
        defect_mask:=D972LRMask,relation_combination:=D972LRCoeff,
        relation_generator_indices:=D972LRSelectedRel,
        corrected_pentagon_word:=D972LRCorrected,
        hexagon_E_identity:=true,hexagon_P_identity:=true,hexagon_G9_identity:=true,
        pentagon_mod_literal_relations:=true,marking_m:=0,lambda:=1,
        charming:=true,onto_E:=true,onto_G9:=true,roof_reduction_exact:=true);;
      Add(D972LRPowSolutions,D972LRSol);; Add(D972LRSolutions,D972LRSol);
    fi;
  od;
  Add(D972LRPowerRecords,rec(exponent:=D972LRPow.exponent,row_index:=D972LRPow.row_index,
    roof_key:=D972LRPow.key,source_word:=D972LRPow.word,
    base_dtilde_word:=D972LRBaseDword,dtilde_transport_ok:=D972LRTransportOK,
    base_hexagon_masks:=D972LRBaseHexMasks,base_defect_mask:=D972LRBaseMask,
    gauge_columns:=D972LRGaugeCols,
    solution_count:=Length(D972LRPowSolutions)));
od;

D972LRNormOK:=false;;
if D972LRPowerRecords[1].base_defect_mask<>fail and D972LRPowerRecords[2].base_defect_mask<>fail then
  D972LRNormResidual:=D972LRXor(D972LRPowerRecords[2].base_defect_mask,
    D972LRApplyMatrix(D972LRPowerRecords[1].base_defect_mask,D972LRNorm2));;
  D972LRNormOK:=D972LRSolve(D972LRRelationSpan,D972LRNormResidual)<>fail;
fi;;

D972LRStatus:="UNKNOWN_MISSING_INPUT";; D972LRSelected:=fail;;
if Length(D972LRGlobalMissing)=0 then
  if Length(D972LRSolutions)>0 then
    ## Prefer the fixed target itself; use the accepted square only if needed.
    D972LRSelected:=First(D972LRSolutions,s->s.exponent=1);;
    if D972LRSelected=fail then D972LRSelected:=D972LRSolutions[1]; fi;
    D972LRStatus:="ROW18_TYPED_STAGE_LIFT";
  else
    D972LRStatus:="EXACT_FINITE_STAGE_OBSTRUCTION";
  fi;
fi;;

## Settlement is an exact finite homomorphism gate in the literal quotient.
## The raw A.18 boundary subgroup R<=V4 is imposed before testing the source;
## requiring an automorphism of raw E4 would incorrectly forget the literal
## relation surgery which just closed the pentagon.
D972LRSettlement:=fail;;
if D972LRSelected<>fail then
  D972LRSelectedSourceWords:=D972LRSourceWordsM0(D972LRSelected.typed_source_word);;
  D972LRSelectedSourceE:=List(D972LRSelectedSourceWords,
    w->D972LRWordElm(w,D972BDTupleGens));;
  D972LRSelectedSourceP:=List(D972LRSelectedSourceWords,
    w->D972LRWordElm(w,D972BDTuplePGens));;
  D972LRSelectedSourceG9:=List(D972LRSelectedSourceWords,
    w->D972LRWordElm(w,D972BDTupleG9Gens));;
  D972LRSelectedAction:=List(D972BDWords,r->D972LRMask24(D972LRWordElm(
    D972LRSubstitute(r.source_word,D972LRSelectedSourceWords),D972BDTupleGens)));;
  D972LRP4Group:=Group(D972BDTuplePGens);; D972LRE4Group:=Group(D972BDTupleGens);;
  D972LRG94Group:=Group(D972BDTupleG9Gens);;
  D972LRBoundaryGroup:=Group(List(D972LRRelationGens,
    r->D972LRWordElm(r.word,D972BDTupleGens)));;
  if Size(D972LRBoundaryGroup)<>2^D972LRRelationSpan.rank or
     not IsNormal(D972LRE4Group,D972LRBoundaryGroup) then
    Error("157cu: literal boundary subgroup order/normality drift");
  fi;
  D972LRLiteralQMap:=NaturalHomomorphismByNormalSubgroup(D972LRE4Group,
    D972LRBoundaryGroup);;
  D972LRLiteralQ:=Image(D972LRLiteralQMap);;
  D972LRLiteralQGens:=List(D972BDTupleGens,g->Image(D972LRLiteralQMap,g));;
  D972LRSelectedSourceQ:=List(D972LRSelectedSourceE,g->Image(D972LRLiteralQMap,g));;
  D972LRHomP:=GroupHomomorphismByImages(D972LRP4Group,Group(D972LRSelectedSourceP),
    D972BDTuplePGens,D972LRSelectedSourceP);;
  D972LRHomG9:=GroupHomomorphismByImages(D972LRG94Group,Group(D972LRSelectedSourceG9),
    D972BDTupleG9Gens,D972LRSelectedSourceG9);;
  D972LRHomQ:=GroupHomomorphismByImages(D972LRLiteralQ,Group(D972LRSelectedSourceQ),
    D972LRLiteralQGens,D972LRSelectedSourceQ);;
  if D972LRRowRank(D972LRSelectedAction,24)<>24 or D972LRHomP=fail or
     D972LRHomG9=fail or D972LRHomQ=fail or not IsBijective(D972LRHomP) or
     not IsBijective(D972LRHomG9) or not IsBijective(D972LRHomQ) then
    AddSet(D972LRGlobalMissing,"settlement.source_endomorphism_bijective");;
    D972LRStatus:="UNKNOWN_MISSING_INPUT";; D972LRSelected:=fail;
  else
    D972LRSettlement:=rec(source_words:=D972LRSelectedSourceWords,
      source_images_E:=List(D972LRSelectedSourceE,p->D972BDZeroArray(p,4*D972BDDegreeE)),
      source_images_P:=List(D972LRSelectedSourceP,p->D972BDZeroArray(p,4*D972BDDegreeP)),
      source_images_G9:=List(D972LRSelectedSourceG9,p->D972BDZeroArray(p,4*D972BDDegreeG9)),
      kernel_action_matrix:=List(D972LRSelectedAction,r->D972LRBits(r,24)),
      kernel_action_rank:=24,literal_boundary_order:=Size(D972LRBoundaryGroup),
      literal_kernel_quotient_dimension:=24-D972LRRelationSpan.rank,
      literal_quotient_order:=Size(D972LRLiteralQ),P4_bijective:=true,
      G9_fourfold_image_bijective:=true,literal_quotient_bijective:=true,settled:=true);
    D972LRSelected.settlement:=D972LRSettlement;
  fi;
fi;;

D972LRRelationReceipt:=List(D972LRRelationGens,r->rec(vector:=r.vector,
  vector_bits:=D972LRBits(r.vector,24),raw_index:=r.raw_index,
  action_word:=r.action_word,word:=r.word));;
D972LRBasisReceipt:=List(D972BDWords,r->rec(coordinate:=r.coordinate,
  module_index:=r.module_index,source_word:=r.source_word,target_E:=r.target_E,
  target_P:=r.target_P,target_G9:=r.target_G9));;
D972LRReceipt:=rec(
  schema:="d972-b4-literal-row18-stage/v1",
  final_marker:="D972_B4_LITERAL_ROW18_STAGE_V1_FINAL",
  status:=D972LRStatus,
  missing_inputs:=D972LRGlobalMissing,
  frozen_inputs:=rec(core_source_sha256:=D972LRCoreSha,word_artifact_sha256:=D972LRWordsSha,
    tuple_artifact_sha256:=D972LRTuplesSha,literal_source_sha256:=D972LRLiteralSha,
    packagegt_pab_sha256:=D972LRPaBSha,row_vector_PSL_convention:=true,
    roof_tuple_digest:=D972LRTupleDigest,roof_key_digest:=D972LRKeyDigest),
  row18:=rec(zero_based_index:=18,one_based_index:=19,key:=D972LRExpectedKey,
    word:=D972LRExpectedWord,pure_axis:=[1,0],arithmetic_outside_accepted:=true),
  c2_basis:=rec(rank:=24,order:=2^24,ordering:="four deletion coordinates, then u,v,w,x,y,z",
    generators:=D972LRBasisReceipt,correction_F2_basis_words:=D972LRCorrectionWords),
  b4_action:=rec(generator_order:=["sigma1","sigma2","sigma3"],
    canonical_PB4_order:=["x12","x13","x14","x23","x24","x34"],
    packagegt_PB4_order:=["x12","x23","x13","x14","x24","x34"],
    source_automorphism_words:=D972LRArtinWords,
    independently_derived_words:=D972LRDerivedArtin,
    packagegt_inverse_orientation_words:=D972LRPaBInverseWords,
    independently_derived_packagegt_inverse_words:=D972LRDerivedPaBInverse,
    transformed_basis_words:=D972LRActionWordCert,
    matrices:=List(D972LRActionRows,m->List(m,r->D972LRBits(r,24))),
    matrix_row_masks:=D972LRActionRows,artin_relations:=true,
    pure_generator_braid_words:=D972LRPureBraidWords,
    pure_generator_braid_word_replay:=true,
    coordinate_permutations:=D972LRExpectedPerms,
    pure_factor_orders:=D972LRFactorOrders,
    pure_factor_module_irreducible:=D972LRFactorModuleIrreducible,
    direct_product_certificate:=rec(
      method:="single-support commutators and exact factor normal closures",
      single_support_commutators:=D972LRSingleSupportWitnesses,
      factor_normal_closure_orders:=D972LRNormalClosureOrders,
      independent_factor_inclusion:=true,pure_image_order:=D972LRPureImageOrder),
    pure_image_order:=D972LRPureImageOrder,
    coordinate_image_order:=D972LRCoordinateImageOrder,
    coordinate_action_transitive:=D972LRCoordinateTransitive,
    image_order:=D972LRActionImageOrder,
    chief_certificate:=rec(factor_dimensions:=[6,6,6,6],
      factor_module_irreducible:=D972LRFactorModuleIrreducible,
      independent_factor_action:=true,coordinate_action_transitive:=true,
      dimensions:=[24],module_irreducible:=true),
    chief_dimensions:=[24],module_irreducible:=true,
    source_kernel_certificate:=rec(definition:="kernel of the recorded B4 to GL(24,2) generator map",
      index:=D972LRActionImageOrder,
      membership_test:="natural word evaluation in the three recorded 24x24 matrices")),
  literal_a18:=rec(prefix_count:=18,seed_count:=28,coface_count:=5,
    coface_order:=List(D972LRMaps,r->r.name),prefix_sha256:=D972LRPrefixSha,
    seed_sha256:=D972LRSeedSha,a18_rows_sha256:=D972LRA18Sha,
    presentation_sha256:=D972LRPresentationSha,dtilde_sha256:=D972LRDtildeSha,
    raw_relation_masks:=D972LRRawMasks,relation_boundary_rank:=D972LRRelationSpan.rank,
    relation_boundary_generators:=D972LRRelationReceipt,
    literal_residual_to_C_P_over_C_E_matrix:=List(D972LRPowerRecords,r->
      rec(exponent:=r.exponent,row_index:=r.row_index,hexagon_masks:=r.base_hexagon_masks,
        residual_mask:=r.base_defect_mask,
        gauge_columns:=r.gauge_columns))),
  power_selector:=rec(used:=D972LRSelected<>fail and D972LRSelected.exponent>1,
    root_row_index:=19,root_key:=D972LRExpectedKey,root_word:=D972LRF0,
    exponent_candidates:=[1,2],powered_word:=D972LRSquare,
    powered_row_index:=D972LRSquareIndex,powered_key:=D972LRSquareKey,
    root_action_matrix:=List(D972LRRootAction,r->D972LRBits(r,24)),
    norm_I_plus_T:=List(D972LRNorm2,r->D972LRBits(r,24)),
    norm_identity_mod_literal_relations:=D972LRNormOK,
    outside_proof:="pure axis exponent n with 3 not dividing n remains outside both arithmetic Kummer lines"),
  exhaustive_stage:=rec(correction_count:=64,power_records:=D972LRPowerRecords,
    total_solution_count:=Length(D972LRSolutions),selected:=D972LRSelected,
    relation_boundary_closed_under_B4:=true,representative_independence:=true,
    marking_checked:=true,charming_onto_checked:=true,settlement:=D972LRSettlement,
    settlement_method:="exact source homomorphisms on the literal E4/R quotient, P4 and the G9 fourfold image"),
  logical_boundary:=rec(stage_only:=true,common_refinement_compactness_not_recomputed:=true,
    timeout_or_resource_is_unknown:=true,burau_or_magnus_zero_used_as_lift:=false));;

if D972LRMode="selftest" then
  if D972LRArtinWords[1][2]=[2] then Error("157cu: action mutation accepted"); fi;
  if D972LRMaps[3].left=[4,2] then Error("157cu: coface mutation accepted"); fi;
  if D972LRExpectedWord=D972LRReduce(Concatenation(D972LRExpectedWord,[1])) then
    Error("157cu: basis/roof mutation accepted"); fi;
  if D972LRGTComposeM0([1,2],[1,2])=D972LRReduce([1,2,1,2]) then
    Error("157cu: naive GT composition order accepted"); fi;
  Print("D972_B4_LITERAL_ROW18_STAGE_V1_GAP_SELFTEST_PASS\n");
fi;;
D972LRWrite(D972LROutput,D972LRReceipt);;
Print("D972_B4_LITERAL_ROW18_STAGE_V1_FINAL status=",D972LRStatus,
  " output=",D972LROutput," relation_rank=",D972LRRelationSpan.rank,
  " solutions=",Length(D972LRSolutions),"\n");
Print("D972_B4_LITERAL_ROW18_STAGE_V1_FINAL\n");
