#############################################################################
## d972_b4_literal_row18_stage_v2.g
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
D972LRPhaseBegin := function(label)
  local now;
  now:=Runtime();;
  WriteLine(OutputTextUser(),Concatenation("D972_ROW18_PHASE name=",label,
    " state=begin runtime_ms=",String(now)));;
  return now;
end;;
D972LRPhaseEnd := function(label,start)
  local now;
  now:=Runtime();;
  WriteLine(OutputTextUser(),Concatenation("D972_ROW18_PHASE name=",label,
    " state=end runtime_ms=",String(now)," elapsed_ms=",String(now-start)));;
end;;
D972LRCoreRaw:=D972LRRaw(D972LRCorePath,D972LRCoreSha,"core producer");;
D972LRWordsRaw:=D972LRRaw(D972LRWordsPath,D972LRWordsSha,"word artifact");;
D972LRTuplesRaw:=D972LRRaw(D972LRTuplesPath,D972LRTuplesSha,"tuple artifact");;
D972LRLiteralRaw:=D972LRRaw(D972LRLiteralPath,D972LRLiteralSha,"literal source");;
D972LRPaBRaw:=D972LRRaw(D972LRPaBPath,D972LRPaBSha,"PackageGT PaB");;

## Rerun the fast, lossless v2 basis constructor in this same pinned process.
D972LRPhaseStart:=D972LRPhaseBegin("core_reconstruction");;
D972_BD_MODE := "full";;
D972_BD_OUTPUT := D972LRCoreOutput;;
Read(D972LRCorePath);
D972LRPhaseEnd("core_reconstruction",D972LRPhaseStart);;

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
D972LRValueInV4 := function(value)
  local c,b;
  for c in [1..4] do
    b:=D972BDBlockRestrict(value,(c-1)*D972BDDegreeE,D972BDDegreeE);;
    if not b in D972BDV then return false; fi;
  od;
  return true;
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
D972LRMatrixPerm := function(rows,n)
  local images;
  images:=List([1..2^n-1],v->D972LRApplyMatrix(v,rows));;
  if Set(images)<>[1..2^n-1] then
    Error("157cx2: singular finite matrix action");
  fi;
  return PermList(images);
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
  local S,queue,pos,v,row,image;
  S:=D972LRNewSpan(n);; D972LRInsert(S,seed,1);; queue:=[seed];; pos:=1;;
  while pos<=Length(queue) do
    v:=queue[pos];; pos:=pos+1;;
    for row in rows do
      image:=D972LRApplyMatrix(v,row);;
      if D972LRInsert(S,image,1) then Add(queue,image); fi;
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
D972LRInverseMatrixRows := function(rows,n)
  local S,i,answer;
  S:=D972LRNewSpan(n);;
  for i in [1..n] do D972LRInsert(S,rows[i],2^(i-1)); od;
  if S.rank<>n then Error("157cx2: singular F2 matrix"); fi;
  answer:=List([1..n],i->D972LRSolve(S,2^(i-1)));;
  if D972LRMatMul(rows,answer)<>D972LRIdentityRows(n) or
     D972LRMatMul(answer,rows)<>D972LRIdentityRows(n) then
    Error("157cx2: F2 matrix inverse replay drift");
  fi;
  return answer;
end;;
D972LRMatrixWordRows := function(word,gens,n)
  local inverses,out,a,step;
  inverses:=List(gens,g->D972LRInverseMatrixRows(g,n));;
  out:=D972LRIdentityRows(n);;
  for a in word do
    if a>0 then step:=gens[a];; else step:=inverses[-a]; fi;
    out:=D972LRMatMul(out,step);
  od;
  return out;
end;;

#############################################################################
## Full marked Artin action, independently rederived in B4.
#############################################################################
D972LRPhaseStart:=D972LRPhaseBegin("fp_artin_action");;
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

## Use the faithful Artin representation B4 -> Aut(F4), avoiding a generic
## Reidemeister--Schreier conversion of PB4.  Free words are reduced signed
## integer lists.  The positive generator sends
##   t_i |-> t_i t_{i+1} t_i^-1,  t_{i+1} |-> t_i,
## and the negative formula below is its literal inverse.
D972LRBraidLetterAut := function(letter)
  local images,i;
  images:=List([1..4],j->[j]);; i:=AbsInt(letter);;
  if i<1 or i>3 then Error("157cx2: braid letter out of range"); fi;
  if letter>0 then
    images[i]:=[i,i+1,-i];; images[i+1]:=[i];
  else
    images[i]:=[i+1];; images[i+1]:=[-(i+1),i,i+1];
  fi;
  return images;
end;;
D972LRBraidAut := function(word)
  local images,letter,step;
  images:=List([1..4],j->[j]);;
  for letter in word do
    step:=D972LRBraidLetterAut(letter);;
    images:=List(images,w->D972LRSubstitute(w,step));
  od;
  return images;
end;;
D972LRPureBraidWords:=[[1,1],[2,1,1,-2],[3,2,1,1,-2,-3],
  [2,2],[3,2,2,-3],[3,3]];;
D972LRFreeIdentity:=List([1..4],j->[j]);;
if ForAny([1..3],i->D972LRBraidAut([i,-i])<>D972LRFreeIdentity or
     D972LRBraidAut([-i,i])<>D972LRFreeIdentity or
     D972LRSubstitute([1,2,3,4],D972LRBraidAut([i]))<>[1,2,3,4] or
     D972LRSubstitute([1,2,3,4],D972LRBraidAut([-i]))<>[1,2,3,4]) or
   D972LRBraidAut([1,2,1])<>D972LRBraidAut([2,1,2]) or
   D972LRBraidAut([2,3,2])<>D972LRBraidAut([3,2,3]) or
   D972LRBraidAut([1,3])<>D972LRBraidAut([3,1]) then
  Error("157cx2: faithful Artin representation calibration drift");
fi;;
D972LRDerivedArtin:=[];; D972LRDerivedPaBInverse:=[];;
for D972LRI in [1..3] do
  D972LRTmp:=[];; D972LRR:=[];;
  for D972LRJ in [1..6] do
    D972LRD:=D972LRReduce(Concatenation([-D972LRI],
      D972LRPureBraidWords[D972LRJ],[D972LRI]));;
    D972LRH:=D972LRSubstitute(D972LRArtinWords[D972LRI][D972LRJ],
      D972LRPureBraidWords);;
    if D972LRBraidAut(D972LRD)<>D972LRBraidAut(D972LRH) then
      Error("157cx2: faithful canonical Artin orientation drift");
    fi;
    Add(D972LRTmp,D972LRArtinWords[D972LRI][D972LRJ]);
    D972LRD:=D972LRReduce(Concatenation([D972LRI],
      D972LRPureBraidWords[D972LRJ],[-D972LRI]));;
    D972LRH:=D972LRSubstitute(D972LRPaBInverseWords[D972LRI][D972LRJ],
      D972LRPureBraidWords);;
    if D972LRBraidAut(D972LRD)<>D972LRBraidAut(D972LRH) then
      Error("157cx2: faithful PackageGT inverse-orientation drift");
    fi;
    Add(D972LRR,D972LRPaBInverseWords[D972LRI][D972LRJ]);
  od;
  Add(D972LRDerivedArtin,D972LRTmp);; Add(D972LRDerivedPaBInverse,D972LRR);
od;

D972LRActionRows:=[];; D972LRActionWordCert:=[];;
for D972LRI in [1..3] do
  D972LRTmp:=[];; D972LRD:=[];;
  D972LRAutoE:=List(D972LRArtinWords[D972LRI],w->D972LRWordElm(w,D972BDTupleGens));;
  D972LRAutoP:=List(D972LRArtinWords[D972LRI],w->D972LRWordElm(w,D972BDTuplePGens));;
  D972LRAutoG9:=List(D972LRArtinWords[D972LRI],w->D972LRWordElm(w,D972BDTupleG9Gens));;
  for D972LRJ in [1..24] do
    D972LRW:=D972LRSubstitute(D972BDWords[D972LRJ].source_word,D972LRArtinWords[D972LRI]);;
    D972LRE:=D972LRWordElm(D972BDWords[D972LRJ].source_word,D972LRAutoE);;
    if D972LRJ=1 and (D972LRWordElm(D972LRW,D972BDTupleGens)<>D972LRE or
       D972LRWordElm(D972LRW,D972BDTuplePGens)<>
         D972LRWordElm(D972BDWords[D972LRJ].source_word,D972LRAutoP) or
       D972LRWordElm(D972LRW,D972BDTupleG9Gens)<>
         D972LRWordElm(D972BDWords[D972LRJ].source_word,D972LRAutoG9)) then
      Error("157cx2: substitution/evaluation composition drift");
    fi;
    if D972LRWordElm(D972BDWords[D972LRJ].source_word,D972LRAutoP)<>
         One(D972BDTuplePGens[1]) or
       D972LRWordElm(D972BDWords[D972LRJ].source_word,D972LRAutoG9)<>
         One(D972BDTupleG9Gens[1]) then
      Error("157cx2: Artin action left the marked kernel");
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
D972LRFactorPermutationsByCoordinate:=[];;
for D972LRC in [1..4] do
  D972LRFactorMats:=List(D972BDPureMatrices,row->row[D972LRC]);;
  D972LRFactorPerms:=List(D972BDPureMatrices,row->
    D972LRMatrixPerm(row[D972LRC],6));;
  D972LRFactorGroup:=Group(D972LRFactorPerms);;
  Add(D972LRFactorMatricesByCoordinate,D972LRFactorMats);;
  Add(D972LRFactorPermutationsByCoordinate,D972LRFactorPerms);;
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
  Error("157cu: P-factor action/chief decomposition drift: orders=",
    D972LRFactorOrders," irreducible=",D972LRFactorModuleIrreducible);
fi;;

## Replay all six canonical PB4 generators as actual B4 words, not merely the
## three adjacent squares.  This binds the block-diagonal pure action to the
## recorded three-generator B4 action.
D972LRPureFullRows:=List([1..6],g->List([1..24],i->
  D972BDPureMatrices[g][QuoInt(i-1,6)+1][((i-1) mod 6)+1]*
    2^(6*QuoInt(i-1,6))));;
for D972LRI in [1..6] do
  if D972LRMatrixWordRows(D972LRPureBraidWords[D972LRI],
     D972LRActionRows,24)<>D972LRPureFullRows[D972LRI] then
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
  D972LRWitnessBlocks:=List([1..4],d->D972LRMatrixWordRows(
    [-1,-2,1,2],[D972LRFactorMatricesByCoordinate[d][D972LRA],
      D972LRFactorMatricesByCoordinate[d][D972LRB]],6));;
  D972LRWitnessSupport:=Filtered([1..4],d->
    D972LRWitnessBlocks[d]<>D972LRIdentityRows(6));;
  if D972LRWitnessSupport<>[D972LRC] then
    Error("157cu: single-support commutator drift at coordinate ",D972LRC);
  fi;
  D972LRWitnessPermutation:=Comm(
    D972LRFactorPermutationsByCoordinate[D972LRC][D972LRA],
    D972LRFactorPermutationsByCoordinate[D972LRC][D972LRB]);;
  if D972LRMatrixPerm(D972LRWitnessBlocks[D972LRC],6)<>
     D972LRWitnessPermutation then
    Error("157cx2: matrix/permutation commutator orientation drift");
  fi;
  D972LRNormal:=NormalClosure(D972LRFactorGroups[D972LRC],
    Subgroup(D972LRFactorGroups[D972LRC],[D972LRWitnessPermutation]));;
  Add(D972LRNormalClosureOrders,Size(D972LRNormal));;
  Add(D972LRSingleSupportWitnesses,rec(coordinate:=D972LRC,
    generator_indices:=[D972LRA,D972LRB],
    commutator_word:=[-D972LRA,-D972LRB,D972LRA,D972LRB],
    support_coordinates:=D972LRWitnessSupport,
    block_row_masks:=D972LRWitnessBlocks,
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
D972LRPhaseEnd("fp_artin_action",D972LRPhaseStart);;

#############################################################################
## Literal A.18 transport, row 18, and the exact finite torsor equation.
#############################################################################
D972LRPhaseStart:=D972LRPhaseBegin("literal_a18_reconstruction");;
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
D972LRHexCached := function(word,m,x,y,fxy)
  local z,u,fxz,fyz,fux,fuy;
  z:=D972LRPP([x,y])^-1;; u:=D972LRPP([y,x])^-1;;
  fxz:=D972LRWordElm(word,[x,z]);; fyz:=D972LRWordElm(word,[y,z]);;
  fux:=D972LRWordElm(word,[u,x]);; fuy:=D972LRWordElm(word,[u,y]);;
  return [D972LRPP([y^m,fxy,x^m,fxz^-1,z^m,fyz]),
    D972LRPP([fux^-1,x^m,fxy^-1,y^m,fuy,u^m])];
end;;
D972LRHex := function(word,m,x,y)
  return D972LRHexCached(word,m,x,y,D972LRWordElm(word,[x,y]));
end;;
## The 64 corrections are ordered concatenations of six fixed words.  At a
## fixed marked pair, evaluation is therefore the base value followed by the
## ordered product of the selected six correction values.  Precompute those
## fixed values once; this is an exact evaluation identity, not a filter.
D972LRHexPairs := function(x,y)
  local z,u;
  z:=D972LRPP([x,y])^-1;; u:=D972LRPP([y,x])^-1;;
  return [[x,y],[x,z],[y,z],[u,x],[u,y]];
end;;
D972LRContextTable := function(pairs)
  return rec(pairs:=pairs,correction_values:=List(pairs,p->
    List(D972LRCorrectionWords,w->D972LRWordElm(w,p))));
end;;
D972LRContextBase := function(word,table)
  return List(table.pairs,p->D972LRWordElm(word,p));
end;;
D972LRContextValues := function(base,table,bits)
  local out,j,i;
  out:=ShallowCopy(base);;
  for j in [1..Length(out)] do
    for i in [1..6] do
      if QuoInt(bits,2^(i-1)) mod 2=1 then
        out[j]:=out[j]*table.correction_values[j][i];
      fi;
    od;
  od;
  return out;
end;;
D972LRHexFromValues := function(values,m,x,y)
  local z,u,fxy,fxz,fyz,fux,fuy;
  if Length(values)<>5 then Error("157cx2: hex context arity drift"); fi;
  z:=D972LRPP([x,y])^-1;; u:=D972LRPP([y,x])^-1;;
  fxy:=values[1];; fxz:=values[2];; fyz:=values[3];;
  fux:=values[4];; fuy:=values[5];;
  return [D972LRPP([y^m,fxy,x^m,fxz^-1,z^m,fyz]),
    D972LRPP([fux^-1,x^m,fxy^-1,y^m,fuy,u^m])];
end;;
D972LRPentFromValues := function(parts)
  if Length(parts)<>5 then Error("157cx2: pentagon context arity drift"); fi;
  return D972LRPP([D972LRPP([parts[5],parts[3]])^-1,
    parts[2],parts[4],parts[1]]);
end;;
D972LROntoCached := function(value,x,y,targetSize,keys,values)
  local pos,result;
  pos:=Position(keys,value);;
  if pos<>fail then return values[pos]; fi;
  result:=Size(Group(x,D972LRPP([value^-1,y,value])))=targetSize;;
  Add(keys,value);; Add(values,result);;
  return result;
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

## Literal prefix is a true PB4 boundary.  The 140 individual coface rows need
## not lie in the marked kernel: the literal boundary is obtained only after
## taking their normal closure jointly with the 18 prefix relators.
if ForAny(D972LRPrefix,w->D972LRWordElm(w,D972BDTupleGens)<>One(D972BDTupleGens[1])) or
   ForAny(D972LRPrefix,w->D972LRWordElm(w,D972BDTupleG9Gens)<>One(D972BDTupleG9Gens[1])) then
  Error("157cu: K(0,5) prefix relation replay drift");
fi;;

D972LRPhaseEnd("literal_a18_reconstruction",D972LRPhaseStart);;

## Search only for a positive certificate C <= <<literal relators>>.  The
## subgroup grows monotonically by independent literal-relator conjugates;
## targets are tested in one batch at the end of each breadth-first round and
## the search stops as soon as all 24 marked basis elements are present.
D972LRPhaseStart:=D972LRPhaseBegin("literal_normal_membership_search");;
D972LRLiteralRelators:=Concatenation(D972LRPrefix,D972LRA18Rows);;
D972LRJointGens:=List([1..6],i->
  D972BDJoint(D972BDTupleRows[i],D972BDTupleG9Rows[i]));;
D972LRJointOne:=One(D972LRJointGens[1]);;
D972LRLiteralJointValues:=List(D972LRLiteralRelators,w->
  D972LRWordElm(w,D972LRJointGens));;
D972LRTargetJoint:=List(D972BDWords,r->
  D972LRWordElm(r.source_word,D972LRJointGens));;
D972LRNormalRecords:=[];; D972LRNormalValues:=[];;
D972LRNormalGroup:=Group(D972LRJointOne);;
## J <= E^4 x G9^4, so every strict subgroup enlargement at least doubles
## order and there are at most floor(log2((32256*2916)^4))=105 of them.
## Each retained generator is conjugated by the six actors and their inverses.
D972LRNormalGeneratorBound:=105;; D972LRAttemptBound:=1260;;
for D972LRI in [1..Length(D972LRLiteralRelators)] do
  D972LRValue:=D972LRLiteralJointValues[D972LRI];;
  if not D972LRValue in D972LRNormalGroup then
    Add(D972LRNormalRecords,rec(base_relator_index:=D972LRI,
      conjugator_word:=[],word:=D972LRLiteralRelators[D972LRI],
      element:=D972LRValue));;
    Add(D972LRNormalValues,D972LRValue);;
    D972LRNormalGroup:=ClosureGroup(D972LRNormalGroup,D972LRValue);;
    if Length(D972LRNormalRecords)>D972LRNormalGeneratorBound then
      Error("157cu: literal normal generator bound exceeded during raw insertion");
    fi;
  fi;
od;
D972LRUnresolved:=Filtered([1..24],i->
  not D972LRTargetJoint[i] in D972LRNormalGroup);;
D972LRActorLetters:=Concatenation([1..6],List([1..6],i->-i));;
D972LRPos:=1;; D972LRRound:=0;; D972LRAttempts:=0;;
WriteLine(OutputTextUser(),Concatenation(
  "D972_ROW18_NORMAL_SEARCH round=0 additions=",
  String(Length(D972LRNormalRecords))," generators=",
  String(Length(D972LRNormalRecords))," unresolved=",
  String(D972LRUnresolved)," runtime_ms=",String(Runtime())));;
while Length(D972LRUnresolved)>0 and D972LRPos<=Length(D972LRNormalRecords) do
  D972LRRound:=D972LRRound+1;;
  D972LRRoundEnd:=Length(D972LRNormalRecords);;
  D972LRRoundAdded:=0;;
  while D972LRPos<=D972LRRoundEnd do
    D972LRR:=D972LRNormalRecords[D972LRPos];;
    D972LRPos:=D972LRPos+1;;
    for D972LRLetter in D972LRActorLetters do
      D972LRAttempts:=D972LRAttempts+1;;
      if D972LRAttempts>D972LRAttemptBound then
        Error("157cu: literal normal conjugation-attempt bound exceeded");
      fi;
      if D972LRLetter>0 then
        D972LRActor:=D972LRJointGens[D972LRLetter];;
      else
        D972LRActor:=D972LRJointGens[-D972LRLetter]^-1;;
      fi;
      D972LRValue:=D972LRR.element^D972LRActor;;
      if not D972LRValue in D972LRNormalGroup then
        D972LRConjugator:=D972LRReduce(Concatenation(
          D972LRR.conjugator_word,[D972LRLetter]));;
        D972LRW:=D972LRReduce(Concatenation(D972LRInvWord(D972LRConjugator),
          D972LRLiteralRelators[D972LRR.base_relator_index],D972LRConjugator));;
        if D972LRWordElm(D972LRW,D972LRJointGens)<>D972LRValue then
          Error("157cu: tracked literal conjugate replay drift");
        fi;
        Add(D972LRNormalRecords,rec(
          base_relator_index:=D972LRR.base_relator_index,
          conjugator_word:=D972LRConjugator,word:=D972LRW,
          element:=D972LRValue));;
        Add(D972LRNormalValues,D972LRValue);;
        D972LRNormalGroup:=ClosureGroup(D972LRNormalGroup,D972LRValue);;
        if Length(D972LRNormalRecords)>D972LRNormalGeneratorBound then
          Error("157cu: literal normal generator bound exceeded during closure");
        fi;
        D972LRRoundAdded:=D972LRRoundAdded+1;;
      fi;
    od;
  od;
  D972LRUnresolved:=Filtered(D972LRUnresolved,i->
    not D972LRTargetJoint[i] in D972LRNormalGroup);;
  WriteLine(OutputTextUser(),Concatenation(
    "D972_ROW18_NORMAL_SEARCH round=",String(D972LRRound),
    " additions=",String(D972LRRoundAdded),
    " generators=",String(Length(D972LRNormalRecords)),
    " unresolved=",String(D972LRUnresolved),
    " runtime_ms=",String(Runtime())));;
  if D972LRRoundAdded=0 and Length(D972LRUnresolved)>0 then break; fi;
od;
if Length(D972LRUnresolved)>0 then
  Error("157cu: literal normal closure misses marked C basis indices=",
    D972LRUnresolved," tracked_generators=",Length(D972LRNormalRecords),
    " conjugation_attempts=",D972LRAttempts);
fi;;
D972LRNormalSearchGeneratorCount:=Length(D972LRNormalRecords);;
D972LRPhaseEnd("literal_normal_membership_search",D972LRPhaseStart);;

## Extract 24 actual words in literal conjugates, expand them back to F6, and
## compact the receipt to the normal generators used by those preimages.
D972LRPhaseStart:=D972LRPhaseBegin("literal_normal_certificate_expansion");;
D972LRNormalFree:=FreeGroup(Length(D972LRNormalRecords),"lr_literal_normal");;
D972LRNormalFreeGens:=GeneratorsOfGroup(D972LRNormalFree);;
D972LRNormalEpi:=GroupHomomorphismByImages(D972LRNormalFree,D972LRNormalGroup,
  D972LRNormalFreeGens,D972LRNormalValues);;
if D972LRNormalEpi=fail then Error("157cu: literal normal epimorphism failed"); fi;;
D972LRBasisCombinations:=[];;
for D972LRI in [1..24] do
  D972LRPre:=PreImagesRepresentative(D972LRNormalEpi,D972LRTargetJoint[D972LRI]);;
  if D972LRPre=fail then
    Error("157cu: marked C basis preimage failed at index=",D972LRI);
  fi;
  D972LRCombination:=D972LRReduce(D972BDSignedWord(D972LRPre));;
  D972LRW:=D972LRSubstitute(D972LRCombination,
    List(D972LRNormalRecords,r->r.word));;
  D972LRE:=D972LRWordElm(D972LRW,D972BDTupleGens);;
  D972LRP:=D972LRWordElm(D972LRW,D972BDTuplePGens);;
  D972LRG9:=D972LRWordElm(D972LRW,D972BDTupleG9Gens);;
  D972LRM:=D972LRMask24(D972LRE);;
  if D972LRP<>One(D972BDTuplePGens[1]) or
     D972LRG9<>One(D972BDTupleG9Gens[1]) or D972LRM<>2^(D972LRI-1) then
    Error("157cu: literal normal C-basis replay failed at index=",D972LRI,
      " mask=",D972LRM," P_order=",Order(D972LRP),
      " G9_order=",Order(D972LRG9));
  fi;
  Add(D972LRBasisCombinations,rec(basis_index:=D972LRI,
    target_source_word:=D972BDWords[D972LRI].source_word,
    normal_generator_word:=D972LRCombination,expanded_word:=D972LRW,
    E_mask:=D972LRM,E_value:=D972LRE,P_value:=D972LRP,G9_value:=D972LRG9));
od;
D972LRUsedNormal:=Set(Concatenation(List(D972LRBasisCombinations,r->
  List(r.normal_generator_word,AbsInt))));;
if Length(D972LRUsedNormal)=0 then Error("157cu: empty literal normal certificate"); fi;;
D972LRCompactNormal:=D972LRNormalRecords{D972LRUsedNormal};;
for D972LRR in D972LRBasisCombinations do
  D972LRCombination:=List(D972LRR.normal_generator_word,a->
    SignInt(a)*Position(D972LRUsedNormal,AbsInt(a)));;
  D972LRW:=D972LRSubstitute(D972LRCombination,
    List(D972LRCompactNormal,r->r.word));;
  if D972LRW<>D972LRR.expanded_word then
    Error("157cu: compressed literal normal word drift");
  fi;
  D972LRR.normal_generator_word:=D972LRCombination;;
od;
D972LRNormalRecords:=D972LRCompactNormal;;
D972LRNormalReceipt:=List([1..Length(D972LRNormalRecords)],i->rec(
  index:=i,
  base_relator_index:=D972LRNormalRecords[i].base_relator_index,
  conjugator_word:=D972LRNormalRecords[i].conjugator_word,
  word:=D972LRNormalRecords[i].word,
  image_E:=D972BDZeroArray(D972LRWordElm(D972LRNormalRecords[i].word,
    D972BDTupleGens),4*D972BDDegreeE),
  image_P:=D972BDZeroArray(D972LRWordElm(D972LRNormalRecords[i].word,
    D972BDTuplePGens),4*D972BDDegreeP),
  image_G9:=D972BDZeroArray(D972LRWordElm(D972LRNormalRecords[i].word,
    D972BDTupleG9Gens),4*D972BDDegreeG9)));;
D972LRBasisCombinationReceipt:=List(D972LRBasisCombinations,r->rec(
  basis_index:=r.basis_index,target_source_word:=r.target_source_word,
  normal_generator_word:=r.normal_generator_word,expanded_word:=r.expanded_word,
  E_mask:=r.E_mask,
  image_E:=D972BDZeroArray(r.E_value,4*D972BDDegreeE),
  image_P:=D972BDZeroArray(r.P_value,4*D972BDDegreeP),
  image_G9:=D972BDZeroArray(r.G9_value,4*D972BDDegreeG9)));;
WriteLine(OutputTextUser(),Concatenation(
  "D972_ROW18_NORMAL_CERT search_generators=",
  String(D972LRNormalSearchGeneratorCount)," certificate_generators=",
  String(Length(D972LRNormalRecords))," combinations=24 attempts=",
  String(D972LRAttempts)," runtime_ms=",String(Runtime())));;
D972LRPhaseEnd("literal_normal_certificate_expansion",D972LRPhaseStart);;

## These 24 actual literal-normal words are the standard marked C basis, so
## D contains C; the accepted stage inclusion D<=C gives D=C.  Initialize the
## relation span from exactly these words, not from the 140 raw coface rows.
D972LRPhaseStart:=D972LRPhaseBegin("literal_relation_basis");;
D972LRRelationSpan:=D972LRNewSpan(24);; D972LRRelationGens:=[];;
for D972LRI in [1..24] do
  D972LRM:=2^(D972LRI-1);;
  if not D972LRInsert(D972LRRelationSpan,D972LRM,D972LRM) then
    Error("157cu: standard literal relation basis dependence");
  fi;
  Add(D972LRRelationGens,rec(vector:=D972LRM,
    word:=D972LRBasisCombinations[D972LRI].expanded_word,
    basis_index:=D972LRI,
    normal_generator_word:=D972LRBasisCombinations[D972LRI].normal_generator_word,
    action_word:=[]));
od;
if D972LRRelationSpan.rank<>24 then Error("157cu: literal relation rank drift"); fi;;
for D972LRR in D972LRRelationGens do for D972LRI in [1..3] do
  if D972LRSolve(D972LRRelationSpan,
     D972LRApplyMatrix(D972LRR.vector,D972LRActionRows[D972LRI]))=fail then
    Error("157cu: relation boundary is not B4 invariant");
  fi;
od; od;
D972LRPhaseEnd("literal_relation_basis",D972LRPhaseStart);;

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

## Full m=0 sourcePB4 word formula, canonical generator order.  If the
## uncorrected root preserves the joint marked kernel C, its induced map on
## V4 supplies an action/norm diagnostic.  The diagnostic is not acceptance
## evidence: the exponent-1 word and its explicit GT square are independently
## enumerated below and accepted only by direct typed replay plus settlement.
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
D972LRRootSourceE:=List(D972LRRootSource,w->D972LRWordElm(w,D972BDTupleGens));;
D972LRRootSourceP:=List(D972LRRootSource,w->D972LRWordElm(w,D972BDTuplePGens));;
D972LRRootSourceG9:=List(D972LRRootSource,w->D972LRWordElm(w,D972BDTupleG9Gens));;
D972LRRootActionRows:=[];; D972LRRootActionUndefinedBasis:=[];;
D972LRRootEOutsideBasis:=[];; D972LRRootPNonidentityBasis:=[];;
D972LRRootG9NonidentityBasis:=[];;
for D972LRI in [1..24] do
  D972LRE:=D972LRWordElm(D972BDWords[D972LRI].source_word,D972LRRootSourceE);;
  D972LRP:=D972LRWordElm(D972BDWords[D972LRI].source_word,D972LRRootSourceP);;
  D972LRG9:=D972LRWordElm(D972BDWords[D972LRI].source_word,D972LRRootSourceG9);;
  D972LREInV4:=D972LRValueInV4(D972LRE);;
  if D972LRI=1 then
    D972LRW:=D972LRSubstitute(D972BDWords[D972LRI].source_word,D972LRRootSource);;
    if D972LRWordElm(D972LRW,D972BDTupleGens)<>D972LRE then
      Error("157cx2: root substitution/evaluation drift");
    fi;
  fi;
  if not D972LREInV4 then Add(D972LRRootEOutsideBasis,D972LRI); fi;
  if D972LRP<>One(D972BDTuplePGens[1]) then
    Add(D972LRRootPNonidentityBasis,D972LRI);
  fi;
  if D972LRG9<>One(D972BDTupleG9Gens[1]) then
    Add(D972LRRootG9NonidentityBasis,D972LRI);
  fi;
  if D972LREInV4 and D972LRP=One(D972BDTuplePGens[1]) and
     D972LRG9=One(D972BDTupleG9Gens[1]) then
    Add(D972LRRootActionRows,D972LRMask24(D972LRE));
  else
    Add(D972LRRootActionUndefinedBasis,D972LRI);
  fi;
od;
D972LRRootActionDefined:=Length(D972LRRootActionUndefinedBasis)=0;;
D972LRRootAction:=fail;; D972LRNorm2:=fail;;
D972LRRootActionReceipt:=fail;; D972LRNorm2Receipt:=fail;;
D972LRRootActionRank:=fail;; D972LRRootActionBijective:=fail;;
if D972LRRootActionDefined then
  D972LRRootAction:=D972LRRootActionRows;;
  D972LRRootActionRank:=D972LRRowRank(D972LRRootAction,24);;
  D972LRRootActionBijective:=D972LRRootActionRank=24;;
  D972LRNorm2:=D972LRMatAdd(D972LRIdentityRows(24),D972LRRootAction);;
  D972LRRootActionReceipt:=List(D972LRRootAction,r->D972LRBits(r,24));;
  D972LRNorm2Receipt:=List(D972LRNorm2,r->D972LRBits(r,24));;
fi;;

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
    D972LRSquareIndex:=D972LRI;; D972LRSquareKey:=D972LRWords.rows[D972LRI][2];;
  fi;
od;
if D972LRSquareIndex=fail then Error("157cu: GT square roof missing from frozen 972 rows"); fi;;

D972LRPowers:=[rec(exponent:=1,word:=D972LRF0,row_index:=19,key:=D972LRExpectedKey),
  rec(exponent:=2,word:=D972LRSquare,row_index:=D972LRSquareIndex,key:=D972LRSquareKey)];;
D972LRSolutions:=[];; D972LRPowerRecords:=[];; D972LRGlobalMissing:=[];;
D972LROntoECacheKeys:=[];; D972LROntoECacheValues:=[];;
D972LROntoG9CacheKeys:=[];; D972LROntoG9CacheValues:=[];;
D972LRETargetSize:=Size(D972BDE);; D972LRG9TargetSize:=Size(D972BDG9);;

## This is original B4 charmingness (2008.00066, Definition 2.19), not a
## silent replacement by the B3-gentle terminology.  Its first condition says
## that the coset has a representative in [F2,F2], equivalently that its
## image belongs to the derived subgroup of the actual finite F2 quotient;
## it never asks that this particular raw free representative have zero
## exponent sums.  The second condition is T^F2 onto and remains the existing
## onto_E/onto_G9 gate below.  See the pinned comparison
## docs/notes/gtpi_v1_addendum_upb4.md:14-18,30-34.
##
## At this fine stage the marked quotient is E x G9.  The two marked
## projections are onto by construction; E is perfect and G9 is solvable, so
## Goursat gives the direct product.  Pin that primary Phase-2b typing and
## replay both derived subgroups here.
D972LRFineG3:=D972BDS.G3_receipt;;
if D972LRFineG3.source_pure_quotient<>"G9 direct-product E" or
   D972LRFineG3.source_pure_quotient_order<>94058496 or
   D972LRFineG3.E_perfect<>true or D972LRFineG3.G9_solvable<>true or
   D972LRFineG3.nontrivial_common_quotient_exists<>false then
  Error("157cu: pinned fine F2 quotient typing drift");
fi;;
D972LRFineDerivedE:=DerivedSubgroup(D972BDE);;
D972LRFineDerivedG9:=DerivedSubgroup(D972BDG9);;
if Size(D972LRFineDerivedE)<>32256 or
   Size(D972LRFineDerivedE)<>Size(D972BDE) or
   Size(D972LRFineDerivedG9)<>729 or not IsSolvableGroup(D972BDG9) or
   Size(D972BDE)*Size(D972BDG9)<>94058496 then
  Error("157cu: fine charming quotient replay drift");
fi;;
D972LRFineCharmingReceipt:=rec(
  definition:="f N_F2 lies in [F2/N_F2,F2/N_F2]",
  definition_source:="2008.00066 Definition 2.19; docs/notes/gtpi_v1_addendum_upb4.md:14-18,30-34",
  original_B4_charming_not_B3_gentle_substitution:=true,
  marking_m:=0,lambda:=1,lambda_unit_precondition:=true,
  GT_shadow_equation_preconditions:="existing roof, hexagon, and pentagon gates; unchanged",
  condition_i:="coset has a representative in [F2,F2], equivalently fine derived membership",
  condition_i_equivalence:="under F2 onto Q, the preimage of Q' is [F2,F2] N_F2",
  condition_i_repaired_here:=true,
  condition_ii:="T^F2 is surjective",
  condition_ii_existing_gate:="onto_E and onto_G9; unchanged",
  condition_ii_candidate_fields:=["onto_E","onto_G9"],
  fine_F2_quotient:="E direct-product G9",
  marked_generators:="(X_E,X_G9),(Y_E,Y_G9)",
  quotient_order:=Size(D972BDE)*Size(D972BDG9),
  goursat_direct_product:=true,nontrivial_common_quotient_exists:=false,
  E_order:=Size(D972BDE),E_derived_order:=Size(D972LRFineDerivedE),
  E_perfect:=true,G9_order:=Size(D972BDG9),
  G9_derived_order:=Size(D972LRFineDerivedG9),G9_solvable:=true,
  derived_order:=Size(D972LRFineDerivedE)*Size(D972LRFineDerivedG9),
  membership_test:="candidate_E in DerivedSubgroup(E) and candidate_G9 in DerivedSubgroup(G9)",
  coarse_P_not_defining:=true,raw_free_exponent_sums_used:=false);;
## Thirty fixed marked contexts: five hexagon contexts and five pentagon
## contexts in each of E, P and G9.  The six correction words are evaluated
## once per context, rather than once per one of the 128 candidates.
D972LRHexTableE:=D972LRContextTable(D972LRHexPairs(D972BDX,D972BDY));;
D972LRHexTableP:=D972LRContextTable(D972LRHexPairs(D972BDPX,D972BDPY));;
D972LRHexTableG9:=D972LRContextTable(D972LRHexPairs(D972BDX9,D972BDY9));;
D972LRPentTableE:=D972LRContextTable(D972LRPairs(D972BDTupleGens));;
D972LRPentTableP:=D972LRContextTable(D972LRPairs(D972BDTuplePGens));;
D972LRPentTableG9:=D972LRContextTable(D972LRPairs(D972BDTupleG9Gens));;
for D972LRPow in D972LRPowers do
  D972LRPowerPhaseName:=Concatenation("power_",String(D972LRPow.exponent),
    "_correction_fibre");;
  D972LRPowerPhaseStart:=D972LRPhaseBegin(D972LRPowerPhaseName);;
  D972LRPowE:=D972LRWordElm(D972LRPow.word,[D972BDX,D972BDY]);;
  D972LRPowP:=D972LRWordElm(D972LRPow.word,[D972BDPX,D972BDPY]);;
  D972LRPowG9:=D972LRWordElm(D972LRPow.word,[D972BDX9,D972BDY9]);;
  D972LRBaseDword:=D972LRDtildeWord(D972LRPow.word);;
  D972LRBaseHexContextE:=D972LRContextBase(D972LRPow.word,D972LRHexTableE);;
  D972LRBaseHexContextP:=D972LRContextBase(D972LRPow.word,D972LRHexTableP);;
  D972LRBaseHexContextG9:=D972LRContextBase(D972LRPow.word,D972LRHexTableG9);;
  D972LRBasePentContextE:=D972LRContextBase(D972LRPow.word,D972LRPentTableE);;
  D972LRBasePentContextP:=D972LRContextBase(D972LRPow.word,D972LRPentTableP);;
  D972LRBasePentContextG9:=D972LRContextBase(D972LRPow.word,D972LRPentTableG9);;
  if D972LRBaseHexContextE[1]<>D972LRPowE or
     D972LRBaseHexContextP[1]<>D972LRPowP or
     D972LRBaseHexContextG9[1]<>D972LRPowG9 then
    Error("157cx2: fixed hex context base drift");
  fi;;
  D972LRBaseHexE:=D972LRHexFromValues(D972LRBaseHexContextE,0,D972BDX,D972BDY);;
  D972LRBaseHexP:=D972LRHexFromValues(D972LRBaseHexContextP,0,D972BDPX,D972BDPY);;
  D972LRBaseHexG9:=D972LRHexFromValues(D972LRBaseHexContextG9,0,D972BDX9,D972BDY9);;
  D972LRBaseHexMasks:=fail;;
  if ForAll(Concatenation(D972LRBaseHexP,D972LRBaseHexG9),IsOne) and
     ForAll(D972LRBaseHexE,e->e in D972BDV) then
    D972LRBaseHexMasks:=List(D972LRBaseHexE,D972LRMask6);;
  fi;
  D972LRBasePentE:=D972LRPentFromValues(D972LRBasePentContextE);;
  D972LRBasePentP:=D972LRPentFromValues(D972LRBasePentContextP);;
  D972LRBasePentG9:=D972LRPentFromValues(D972LRBasePentContextG9);;
  D972LRDwordE:=D972LRWordElm(D972LRBaseDword,D972BDTupleGens);;
  D972LRDwordP:=D972LRWordElm(D972LRBaseDword,D972BDTuplePGens);;
  D972LRDwordG9:=D972LRWordElm(D972LRBaseDword,D972BDTupleG9Gens);;
  D972LRTransportOK:=D972LRDwordE=D972LRBasePentE and
    D972LRDwordP=D972LRBasePentP and D972LRDwordG9=D972LRBasePentG9;;
  D972LRBaseMask:=fail;;
  if D972LRBasePentP=One(D972BDTuplePGens[1]) and
     D972LRBasePentG9=One(D972BDTupleG9Gens[1]) and
     D972LRValueInV4(D972LRBasePentE) then
    D972LRBaseMask:=D972LRMask24(D972LRBasePentE);;
  fi;
  D972LRGaugeCols:=[];; D972LRPowSolutions:=[];;
  D972LRCandidateTransportEvaluatedCount:=0;;
  D972LRCandidateTransportPassCount:=0;;
  ## Lossless diagnostics only.  These lists record the exact correction-bit
  ## fibres of each already-existing cheap gate; they do not alter candidate
  ## acceptance or the terminal classification.
  D972LRCheapGateBits:=rec(
    roof:=[],charming_E_derived:=[],charming_G9_derived:=[],charming:=[],
    hexagon_E_1_identity:=[],hexagon_E_2_identity:=[],hexagon_E_identity:=[],
    hexagon_P_1_identity:=[],hexagon_P_2_identity:=[],hexagon_P_identity:=[],
    hexagon_G9_1_identity:=[],hexagon_G9_2_identity:=[],hexagon_G9_identity:=[],
    pentagon_P_identity:=[],pentagon_G9_identity:=[],pentagon_E_in_C:=[],
    literal_coefficient_available:=[]);;
  D972LRProgressiveGateBits:=rec(
    roof:=[],roof_charming:=[],roof_charming_hexagon_E:=[],
    roof_charming_hexagon_E_P:=[],roof_charming_hexagon_E_P_G9:=[],
    through_pentagon_P:=[],through_pentagon_P_G9:=[],
    through_pentagon_P_G9_E_in_C:=[],through_literal_coefficient:=[]);;
  for D972LRBitsValue in [0..63] do
    D972LRCorr:=D972LRCorrectionWord(D972LRBitsValue);;
    D972LRCandidate:=D972LRReduce(Concatenation(D972LRPow.word,D972LRCorr));;
    D972LRHexContextE:=D972LRContextValues(D972LRBaseHexContextE,
      D972LRHexTableE,D972LRBitsValue);;
    D972LRHexContextP:=D972LRContextValues(D972LRBaseHexContextP,
      D972LRHexTableP,D972LRBitsValue);;
    D972LRHexContextG9:=D972LRContextValues(D972LRBaseHexContextG9,
      D972LRHexTableG9,D972LRBitsValue);;
    D972LRPentContextE:=D972LRContextValues(D972LRBasePentContextE,
      D972LRPentTableE,D972LRBitsValue);;
    D972LRPentContextP:=D972LRContextValues(D972LRBasePentContextP,
      D972LRPentTableP,D972LRBitsValue);;
    D972LRPentContextG9:=D972LRContextValues(D972LRBasePentContextG9,
      D972LRPentTableG9,D972LRBitsValue);;
    D972LRCandidateE:=D972LRHexContextE[1];;
    D972LRCandidateP:=D972LRHexContextP[1];;
    D972LRCandidateG9:=D972LRHexContextG9[1];;
    D972LRRoofOK:=D972LRCandidateP=D972LRPowP and
      D972LRCandidateG9=D972LRPowG9;;
    D972LRCharmE:=D972LRCandidateE in D972LRFineDerivedE;;
    D972LRCharmG9:=D972LRCandidateG9 in D972LRFineDerivedG9;;
    D972LRCharm:=D972LRCharmE and D972LRCharmG9;;
    D972LRHexE:=D972LRHexFromValues(D972LRHexContextE,0,D972BDX,D972BDY);;
    D972LRHexP:=D972LRHexFromValues(D972LRHexContextP,0,D972BDPX,D972BDPY);;
    D972LRHexG9:=D972LRHexFromValues(D972LRHexContextG9,0,D972BDX9,D972BDY9);;
    D972LRPentE:=D972LRPentFromValues(D972LRPentContextE);;
    D972LRPentP:=D972LRPentFromValues(D972LRPentContextP);;
    D972LRPentG9:=D972LRPentFromValues(D972LRPentContextG9);;
    D972LRHexEOK:=ForAll(D972LRHexE,IsOne);;
    D972LRHexPOK:=ForAll(D972LRHexP,IsOne);;
    D972LRHexG9OK:=ForAll(D972LRHexG9,IsOne);;
    D972LRPentPOK:=IsOne(D972LRPentP);;
    D972LRPentG9OK:=IsOne(D972LRPentG9);;
    D972LRPentEInC:=D972LRValueInV4(D972LRPentE);;
    D972LRMask:=fail;; D972LRCoeff:=fail;; D972LRHexMasks:=fail;;
    if ForAll(Concatenation(D972LRHexP,D972LRHexG9),IsOne) and
       ForAll(D972LRHexE,e->e in D972BDV) then
      D972LRHexMasks:=List(D972LRHexE,D972LRMask6);;
    fi;
    if D972LRPentPOK and D972LRPentG9OK and D972LRPentEInC then
      D972LRMask:=D972LRMask24(D972LRPentE);;
      D972LRCoeff:=D972LRSolve(D972LRRelationSpan,D972LRMask);;
    fi;
    if D972LRBitsValue>0 and (D972LRBitsValue=2^(LogInt(D972LRBitsValue,2))) and
       D972LRBaseMask<>fail and D972LRMask<>fail and D972LRBaseHexMasks<>fail and
       D972LRHexMasks<>fail then
      Add(D972LRGaugeCols,rec(hexagon1:=D972LRXor(D972LRBaseHexMasks[1],D972LRHexMasks[1]),
        hexagon2:=D972LRXor(D972LRBaseHexMasks[2],D972LRHexMasks[2]),
        pentagon:=D972LRXor(D972LRBaseMask,D972LRMask)));
    fi;
    if D972LRRoofOK then Add(D972LRCheapGateBits.roof,D972LRBitsValue); fi;
    if D972LRCharmE then Add(D972LRCheapGateBits.charming_E_derived,D972LRBitsValue); fi;
    if D972LRCharmG9 then Add(D972LRCheapGateBits.charming_G9_derived,D972LRBitsValue); fi;
    if D972LRCharm then Add(D972LRCheapGateBits.charming,D972LRBitsValue); fi;
    if IsOne(D972LRHexE[1]) then Add(D972LRCheapGateBits.hexagon_E_1_identity,D972LRBitsValue); fi;
    if IsOne(D972LRHexE[2]) then Add(D972LRCheapGateBits.hexagon_E_2_identity,D972LRBitsValue); fi;
    if D972LRHexEOK then Add(D972LRCheapGateBits.hexagon_E_identity,D972LRBitsValue); fi;
    if IsOne(D972LRHexP[1]) then Add(D972LRCheapGateBits.hexagon_P_1_identity,D972LRBitsValue); fi;
    if IsOne(D972LRHexP[2]) then Add(D972LRCheapGateBits.hexagon_P_2_identity,D972LRBitsValue); fi;
    if D972LRHexPOK then Add(D972LRCheapGateBits.hexagon_P_identity,D972LRBitsValue); fi;
    if IsOne(D972LRHexG9[1]) then Add(D972LRCheapGateBits.hexagon_G9_1_identity,D972LRBitsValue); fi;
    if IsOne(D972LRHexG9[2]) then Add(D972LRCheapGateBits.hexagon_G9_2_identity,D972LRBitsValue); fi;
    if D972LRHexG9OK then Add(D972LRCheapGateBits.hexagon_G9_identity,D972LRBitsValue); fi;
    if D972LRPentPOK then Add(D972LRCheapGateBits.pentagon_P_identity,D972LRBitsValue); fi;
    if D972LRPentG9OK then Add(D972LRCheapGateBits.pentagon_G9_identity,D972LRBitsValue); fi;
    if D972LRPentEInC then Add(D972LRCheapGateBits.pentagon_E_in_C,D972LRBitsValue); fi;
    if D972LRCoeff<>fail then
      Add(D972LRCheapGateBits.literal_coefficient_available,D972LRBitsValue);
    fi;
    D972LRProgRoofOK:=D972LRRoofOK;;
    D972LRProgCharmOK:=D972LRProgRoofOK and D972LRCharm;;
    D972LRProgHexEOK:=D972LRProgCharmOK and D972LRHexEOK;;
    D972LRProgHexPOK:=D972LRProgHexEOK and D972LRHexPOK;;
    D972LRProgHexG9OK:=D972LRProgHexPOK and D972LRHexG9OK;;
    D972LRProgPentPOK:=D972LRProgHexG9OK and D972LRPentPOK;;
    D972LRProgPentG9OK:=D972LRProgPentPOK and D972LRPentG9OK;;
    D972LRProgPentEOK:=D972LRProgPentG9OK and D972LRPentEInC;;
    D972LRProgCoeffOK:=D972LRProgPentEOK and D972LRCoeff<>fail;;
    if D972LRProgRoofOK then Add(D972LRProgressiveGateBits.roof,D972LRBitsValue); fi;
    if D972LRProgCharmOK then Add(D972LRProgressiveGateBits.roof_charming,D972LRBitsValue); fi;
    if D972LRProgHexEOK then Add(D972LRProgressiveGateBits.roof_charming_hexagon_E,D972LRBitsValue); fi;
    if D972LRProgHexPOK then Add(D972LRProgressiveGateBits.roof_charming_hexagon_E_P,D972LRBitsValue); fi;
    if D972LRProgHexG9OK then Add(D972LRProgressiveGateBits.roof_charming_hexagon_E_P_G9,D972LRBitsValue); fi;
    if D972LRProgPentPOK then Add(D972LRProgressiveGateBits.through_pentagon_P,D972LRBitsValue); fi;
    if D972LRProgPentG9OK then Add(D972LRProgressiveGateBits.through_pentagon_P_G9,D972LRBitsValue); fi;
    if D972LRProgPentEOK then Add(D972LRProgressiveGateBits.through_pentagon_P_G9_E_in_C,D972LRBitsValue); fi;
    if D972LRProgCoeffOK then Add(D972LRProgressiveGateBits.through_literal_coefficient,D972LRBitsValue); fi;
    D972LRHexOK:=D972LRHexEOK and D972LRHexPOK and D972LRHexG9OK;;
    D972LRCheapPreOntoOK:=D972LRRoofOK and D972LRCharm and D972LRHexOK and
      D972LRCoeff<>fail;;
    if D972LRCheapPreOntoOK<>D972LRProgCoeffOK then
      Error("157cu: diagnostic progressive gate changed acceptance");
    fi;
    D972LRCandidateDword:=fail;; D972LRCandidateTransportOK:=false;;
    if D972LRCheapPreOntoOK then
      D972LRCandidateTransportEvaluatedCount:=
        D972LRCandidateTransportEvaluatedCount+1;;
      D972LRCandidateDword:=D972LRDtildeWord(D972LRCandidate);;
      D972LRCandidateDwordE:=D972LRWordElm(D972LRCandidateDword,D972BDTupleGens);;
      D972LRCandidateDwordP:=D972LRWordElm(D972LRCandidateDword,D972BDTuplePGens);;
      D972LRCandidateDwordG9:=D972LRWordElm(D972LRCandidateDword,D972BDTupleG9Gens);;
      D972LRCandidateTransportOK:=D972LRCandidateDwordE=D972LRPentE and
        D972LRCandidateDwordP=D972LRPentP and
        D972LRCandidateDwordG9=D972LRPentG9;;
      if D972LRCandidateTransportOK then
        D972LRCandidateTransportPassCount:=D972LRCandidateTransportPassCount+1;;
      fi;
    fi;
    D972LRPreOntoOK:=D972LRCheapPreOntoOK and D972LRCandidateTransportOK;;
    D972LROntoE:=false;; D972LROntoG9:=false;;
    if D972LRPreOntoOK then
      D972LROntoE:=D972LROntoCached(D972LRCandidateE,D972BDX,D972BDY,
        D972LRETargetSize,D972LROntoECacheKeys,D972LROntoECacheValues);;
      D972LROntoG9:=D972LROntoCached(D972LRCandidateG9,D972BDX9,D972BDY9,
        D972LRG9TargetSize,D972LROntoG9CacheKeys,D972LROntoG9CacheValues);;
    fi;;
    if D972LRPreOntoOK and D972LROntoE and D972LROntoG9 then
      D972LRSelectedRel:=Filtered([1..Length(D972LRRelationGens)],i->
        QuoInt(D972LRCoeff,2^(i-1)) mod 2=1);;
      D972LRCorrected:=ShallowCopy(D972LRCandidateDword);;
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
        dtilde_word:=D972LRCandidateDword,dtilde_transport_ok:=true,
        corrected_pentagon_word:=D972LRCorrected,
        hexagon_E_identity:=true,hexagon_P_identity:=true,hexagon_G9_identity:=true,
        pentagon_mod_literal_relations:=true,marking_m:=0,lambda:=1,
        charming:=true,charming_E_derived:=true,charming_G9_derived:=true,
        onto_E:=true,onto_G9:=true,roof_reduction_exact:=true);;
      Add(D972LRPowSolutions,D972LRSol);; Add(D972LRSolutions,D972LRSol);
    fi;
  od;
  D972LRCheapGateCounts:=rec(
    roof:=Length(D972LRCheapGateBits.roof),
    charming_E_derived:=Length(D972LRCheapGateBits.charming_E_derived),
    charming_G9_derived:=Length(D972LRCheapGateBits.charming_G9_derived),
    charming:=Length(D972LRCheapGateBits.charming),
    hexagon_E_1_identity:=Length(D972LRCheapGateBits.hexagon_E_1_identity),
    hexagon_E_2_identity:=Length(D972LRCheapGateBits.hexagon_E_2_identity),
    hexagon_E_identity:=Length(D972LRCheapGateBits.hexagon_E_identity),
    hexagon_P_1_identity:=Length(D972LRCheapGateBits.hexagon_P_1_identity),
    hexagon_P_2_identity:=Length(D972LRCheapGateBits.hexagon_P_2_identity),
    hexagon_P_identity:=Length(D972LRCheapGateBits.hexagon_P_identity),
    hexagon_G9_1_identity:=Length(D972LRCheapGateBits.hexagon_G9_1_identity),
    hexagon_G9_2_identity:=Length(D972LRCheapGateBits.hexagon_G9_2_identity),
    hexagon_G9_identity:=Length(D972LRCheapGateBits.hexagon_G9_identity),
    pentagon_P_identity:=Length(D972LRCheapGateBits.pentagon_P_identity),
    pentagon_G9_identity:=Length(D972LRCheapGateBits.pentagon_G9_identity),
    pentagon_E_in_C:=Length(D972LRCheapGateBits.pentagon_E_in_C),
    literal_coefficient_available:=Length(D972LRCheapGateBits.literal_coefficient_available));;
  D972LRProgressiveGateCounts:=rec(
    roof:=Length(D972LRProgressiveGateBits.roof),
    roof_charming:=Length(D972LRProgressiveGateBits.roof_charming),
    roof_charming_hexagon_E:=Length(D972LRProgressiveGateBits.roof_charming_hexagon_E),
    roof_charming_hexagon_E_P:=Length(D972LRProgressiveGateBits.roof_charming_hexagon_E_P),
    roof_charming_hexagon_E_P_G9:=Length(D972LRProgressiveGateBits.roof_charming_hexagon_E_P_G9),
    through_pentagon_P:=Length(D972LRProgressiveGateBits.through_pentagon_P),
    through_pentagon_P_G9:=Length(D972LRProgressiveGateBits.through_pentagon_P_G9),
    through_pentagon_P_G9_E_in_C:=Length(D972LRProgressiveGateBits.through_pentagon_P_G9_E_in_C),
    through_literal_coefficient:=Length(D972LRProgressiveGateBits.through_literal_coefficient));;
  Add(D972LRPowerRecords,rec(exponent:=D972LRPow.exponent,row_index:=D972LRPow.row_index,
    roof_key:=D972LRPow.key,source_word:=D972LRPow.word,
    base_dtilde_word:=D972LRBaseDword,dtilde_transport_ok:=D972LRTransportOK,
    base_hexagon_masks:=D972LRBaseHexMasks,base_defect_mask:=D972LRBaseMask,
    gauge_columns:=D972LRGaugeCols,
    cheap_gate_passing_bits:=D972LRCheapGateBits,
    cheap_gate_counts:=D972LRCheapGateCounts,
    progressive_gate_passing_bits:=D972LRProgressiveGateBits,
    progressive_gate_counts:=D972LRProgressiveGateCounts,
    candidate_transport_evaluated_count:=D972LRCandidateTransportEvaluatedCount,
    candidate_transport_pass_count:=D972LRCandidateTransportPassCount,
    solution_count:=Length(D972LRPowSolutions)));
  D972LRPhaseEnd(D972LRPowerPhaseName,D972LRPowerPhaseStart);;
od;

D972LRNormOK:=fail;;
if D972LRRootActionDefined then
  D972LRNormOK:=false;;
fi;;
if D972LRRootActionDefined and D972LRPowerRecords[1].base_defect_mask<>fail and
   D972LRPowerRecords[2].base_defect_mask<>fail then
  D972LRNormResidual:=D972LRXor(D972LRPowerRecords[2].base_defect_mask,
    D972LRApplyMatrix(D972LRPowerRecords[1].base_defect_mask,D972LRNorm2));;
  D972LRNormOK:=D972LRSolve(D972LRRelationSpan,D972LRNormResidual)<>fail;;
fi;;

## Settlement is an exact finite homomorphism gate in the literal quotient.
## The imposed chief boundary is D=R intersect C=C, not the raw normal image
## R (which can have components outside C).
D972LRFactorXYRows:=[[4,6],[2,6],[1,5],[1,4]];;
D972LRFactorAutoCertificate := function(label,G,x,y,tupleRows,selectedImages,degree)
  local homs,receipt,c,xrow,yrow,hx,hy,H,hom,j,sourceBlock,targetBlock;
  homs:=[];; receipt:=[];;
  for c in [1..4] do
    xrow:=D972LRFactorXYRows[c][1];; yrow:=D972LRFactorXYRows[c][2];;
    hx:=D972BDBlockRestrict(selectedImages[xrow],(c-1)*degree,degree);;
    hy:=D972BDBlockRestrict(selectedImages[yrow],(c-1)*degree,degree);;
    H:=Group(hx,hy);;
    hom:=GroupHomomorphismByImages(G,H,[x,y],[hx,hy]);;
    if hom=fail then return fail; fi;
    if not IsBijective(hom) then return fail; fi;
    for j in [1..6] do
      sourceBlock:=tupleRows[j][c];;
      targetBlock:=D972BDBlockRestrict(selectedImages[j],(c-1)*degree,degree);;
      if Image(hom,sourceBlock)<>targetBlock then return fail; fi;
    od;
    Add(homs,hom);;
    Add(receipt,rec(family:=label,coordinate:=c,x_source_row:=xrow,
      y_source_row:=yrow,factor_order:=Size(G),bijective:=true,
      all_six_tuple_rows_bound:=true));
  od;
  return rec(homomorphisms:=homs,receipt:=receipt);
end;;
D972LRAbstractToP:=GroupHomomorphismByImages(D972BDAbstractP,D972BDP,
  [D972BDAbstractPX,D972BDAbstractPY],[D972BDPX,D972BDPY]);;
if D972LRAbstractToP=fail then Error("157cu: E/V to canonical P map drift"); fi;;
if not IsBijective(D972LRAbstractToP) then
  Error("157cu: E/V to canonical P isomorphism drift");
fi;;
D972LRBoundaryOrder:=2^D972LRRelationSpan.rank;;
D972LRLiteralQuotientOrder:=Size(D972BDE)^4/D972LRBoundaryOrder;;
D972LRSettlementMethod:="factor_automorphisms_and_exact_kernel_diagram";;

## A local hexagon/pentagon solution is only a candidate.  Settlement is
## tested for every candidate in the already deterministic order
## (exponent 1, bits 0..63; then exponent 2, bits 0..63).  Candidate failure
## is a finite negative, not a missing input.  Only the source-word/evaluation
## composition canary and the frozen quotient model remain hard errors.
D972LRTrySettlement := function(sol)
  local sourceWords,sourceE,sourceP,sourceG9,w,action,r,evalue,pvalue,gvalue,
    relationPreserved,factorE,factorP,factorG9,quotientOK,factorReceipt;
  sourceWords:=D972LRSourceWordsM0(sol.typed_source_word);;
  sourceE:=List(sourceWords,w->D972LRWordElm(w,D972BDTupleGens));;
  sourceP:=List(sourceWords,w->D972LRWordElm(w,D972BDTuplePGens));;
  sourceG9:=List(sourceWords,w->D972LRWordElm(w,D972BDTupleG9Gens));;
  w:=D972LRSubstitute(D972BDWords[1].source_word,sourceWords);;
  if D972LRWordElm(w,D972BDTupleGens)<>
       D972LRWordElm(D972BDWords[1].source_word,sourceE) or
     D972LRWordElm(w,D972BDTuplePGens)<>
       D972LRWordElm(D972BDWords[1].source_word,sourceP) or
     D972LRWordElm(w,D972BDTupleG9Gens)<>
       D972LRWordElm(D972BDWords[1].source_word,sourceG9) then
    Error("157cx2: settlement substitution/evaluation drift");
  fi;
  action:=[];;
  for r in D972BDWords do
    evalue:=D972LRWordElm(r.source_word,sourceE);;
    pvalue:=D972LRWordElm(r.source_word,sourceP);;
    gvalue:=D972LRWordElm(r.source_word,sourceG9);;
    if not D972LRValueInV4(evalue) or
       pvalue<>One(D972BDTuplePGens[1]) or
       gvalue<>One(D972BDTupleG9Gens[1]) then return fail; fi;
    Add(action,D972LRMask24(evalue));
  od;
  relationPreserved:=ForAll(D972LRRelationGens,r->
    D972LRSolve(D972LRRelationSpan,
      D972LRApplyMatrix(r.vector,action))<>fail);;
  if D972LRRowRank(action,24)<>24 or not relationPreserved or
     D972LRRelationSpan.rank<>24 then return fail; fi;
  factorE:=D972LRFactorAutoCertificate("E",D972BDE,D972BDX,D972BDY,
    D972BDTupleRows,sourceE,D972BDDegreeE);;
  if factorE=fail then return fail; fi;
  factorP:=D972LRFactorAutoCertificate("P",D972BDP,D972BDPX,D972BDPY,
    D972BDTuplePRows,sourceP,D972BDDegreeP);;
  if factorP=fail then return fail; fi;
  factorG9:=D972LRFactorAutoCertificate("G9",D972BDG9,D972BDX9,D972BDY9,
    D972BDTupleG9Rows,sourceG9,D972BDDegreeG9);;
  if factorG9=fail then return fail; fi;
  quotientOK:=ForAll([1..6],j->ForAll([1..4],c->
    Image(D972LRAbstractToP,Image(D972BDQMap,D972BDBlockRestrict(
      sourceE[j],(c-1)*D972BDDegreeE,D972BDDegreeE)))=
    D972BDBlockRestrict(sourceP[j],(c-1)*D972BDDegreeP,D972BDDegreeP)));;
  if not quotientOK then return fail; fi;
  factorReceipt:=rec(coordinate_map:=[1,2,3,4],
    E:=factorE.receipt,P:=factorP.receipt,G9:=factorG9.receipt,
    relation_boundary_preserved:=true,literal_boundary_equals_marked_kernel:=true,
    quotient_diagram_commutes:=true,
    quotient_kernel_lemma:="D=C=ker(E4->P4); commuting E/P automorphisms descend bijectively to E4/D",
    kernel_action_bijective:=true,ambient_E4_automorphism:=true,
    P4_automorphism:=true,G9_fourfold_image_automorphism:=true,
    quotient_automorphism:=true);;
  return rec(source_words:=sourceWords,
    source_images_E:=List(sourceE,p->D972BDZeroArray(p,4*D972BDDegreeE)),
    source_images_P:=List(sourceP,p->D972BDZeroArray(p,4*D972BDDegreeP)),
    source_images_G9:=List(sourceG9,p->D972BDZeroArray(p,4*D972BDDegreeG9)),
    kernel_action_matrix:=List(action,r->D972LRBits(r,24)),
    kernel_action_rank:=24,literal_boundary_order:=D972LRBoundaryOrder,
    literal_kernel_quotient_dimension:=24-D972LRRelationSpan.rank,
    literal_quotient_order:=D972LRLiteralQuotientOrder,P4_bijective:=true,
    G9_fourfold_image_bijective:=true,literal_quotient_bijective:=true,
    settlement_method:=D972LRSettlementMethod,
    factor_automorphism_certificate:=factorReceipt,settled:=true);
end;;

D972LRPhaseStart:=D972LRPhaseBegin("settlement");;
D972LRStatus:="EXACT_FINITE_STAGE_OBSTRUCTION";; D972LRSelected:=fail;;
D972LRSettlement:=fail;; D972LRSettlementAttempts:=0;;
D972LRSettlementRejected:=0;;
if Length(D972LRGlobalMissing)<>0 then
  Error("157cx2: diagnostic data entered terminal missing-input gate");
fi;;
for D972LRSol in D972LRSolutions do
  D972LRSettlementAttempts:=D972LRSettlementAttempts+1;;
  D972LRTry:=D972LRTrySettlement(D972LRSol);;
  if D972LRTry<>fail then
    D972LRSelected:=D972LRSol;;
    D972LRSettlement:=D972LRTry;;
    D972LRSelected.settlement:=D972LRSettlement;;
    D972LRStatus:="ROW18_TYPED_STAGE_LIFT";;
    break;
  fi;
  D972LRSettlementRejected:=D972LRSettlementRejected+1;;
od;
D972LRPhaseEnd("settlement",D972LRPhaseStart);;

D972LRRelationReceipt:=List(D972LRRelationGens,r->rec(vector:=r.vector,
  vector_bits:=D972LRBits(r.vector,24),basis_index:=r.basis_index,
  normal_generator_word:=r.normal_generator_word,
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
    faithful_artin_F4_replay:=true,
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
    literal_normal_certificate:=rec(
      method:="incremental subgroup of tracked literal-relator conjugates; stop after all 24 marked basis targets enter",
      boundary_definition:="D=normal closure of the 158 literal relators in the joint image, intersected with C",
      literal_relator_count:=Length(D972LRLiteralRelators),
      normal_generator_count:=Length(D972LRNormalReceipt),
      normal_generators:=D972LRNormalReceipt,
      C_basis_combination_count:=Length(D972LRBasisCombinationReceipt),
      C_basis_combinations:=D972LRBasisCombinationReceipt,
      C_basis_masks:=List([0..23],i->2^i),C_basis_rank:=24,
      certificate_compressed:=true,all_C_basis_membership:=true,
      C_subset_kernel_boundary_D:=true,kernel_boundary_D_subset_C:=true,
      raw_normal_not_used_as_chief_quotient:=true,
      kernel_combinations_P_G9_trivial:=true,
      conclusion:="literal boundary D equals marked kernel C"),
    relation_boundary_rank:=D972LRRelationSpan.rank,
    relation_boundary_generators:=D972LRRelationReceipt,
    literal_residual_to_C_P_over_C_E_matrix:=List(D972LRPowerRecords,r->
      rec(exponent:=r.exponent,row_index:=r.row_index,hexagon_masks:=r.base_hexagon_masks,
        residual_mask:=r.base_defect_mask,
        gauge_columns:=r.gauge_columns))),
  power_selector:=rec(used:=D972LRSelected<>fail and D972LRSelected.exponent>1,
    root_row_index:=19,root_key:=D972LRExpectedKey,root_word:=D972LRF0,
    exponent_candidates:=[1,2],powered_word:=D972LRSquare,
    powered_row_index:=D972LRSquareIndex,powered_key:=D972LRSquareKey,
    root_basis_images_in_C:=D972LRRootActionDefined,
    root_basis_E_outside_indices:=D972LRRootEOutsideBasis,
    root_basis_P_nonidentity_indices:=D972LRRootPNonidentityBasis,
    root_basis_G9_nonidentity_indices:=D972LRRootG9NonidentityBasis,
    root_action_defined:=D972LRRootActionDefined,
    root_action_undefined_basis_indices:=D972LRRootActionUndefinedBasis,
    root_action_rank:=D972LRRootActionRank,
    root_action_bijective:=D972LRRootActionBijective,
    root_action_matrix:=D972LRRootActionReceipt,
    norm_I_plus_T:=D972LRNorm2Receipt,
    norm_identity_mod_literal_relations:=D972LRNormOK,
    norm_role:="diagnostic_only; terminal acceptance uses direct candidate replay and settlement",
    outside_proof:="pure axis exponent n with 3 not dividing n remains outside both arithmetic Kummer lines"),
  charming_gate:=D972LRFineCharmingReceipt,
  exhaustive_stage:=rec(correction_count:=64,power_records:=D972LRPowerRecords,
    total_solution_count:=Length(D972LRSolutions),selected:=D972LRSelected,
    settlement_attempt_count:=D972LRSettlementAttempts,
    settlement_rejected_count:=D972LRSettlementRejected,
    settlement_candidate_order:="exponent_1_bits_0_to_63_then_exponent_2_bits_0_to_63",
    relation_boundary_closed_under_B4:=true,representative_independence:=true,
    marking_checked:=true,charming_onto_checked:=true,settlement:=D972LRSettlement,
    settlement_method:="exact factor automorphisms plus D=C kernel diagram; no generic fallback"),
  logical_boundary:=rec(stage_only:=true,common_refinement_compactness_not_recomputed:=true,
    timeout_or_resource_is_unknown:=true,burau_or_magnus_zero_used_as_lift:=false));;

if D972LRMode="selftest" then
  if D972LRArtinWords[1][2]=[2] then Error("157cu: action mutation accepted"); fi;
  if D972LRMaps[3].left=[4,2] then Error("157cu: coface mutation accepted"); fi;
  if D972LRExpectedWord=D972LRReduce(Concatenation(D972LRExpectedWord,[1])) then
    Error("157cu: basis/roof mutation accepted"); fi;
  if D972LRGTComposeM0([1,2],[1,2])=D972LRReduce([1,2,1,2]) then
    Error("157cu: naive GT composition order accepted"); fi;
  if Sum(Filtered(D972LRF0,x->AbsInt(x)=1),SignInt)=0 and
     Sum(Filtered(D972LRF0,x->AbsInt(x)=2),SignInt)=0 then
    Error("157cu: raw-free charming negative control drift");
  fi;
  Print("D972_B4_LITERAL_ROW18_STAGE_V1_GAP_SELFTEST_PASS\n");
fi;;
D972LRWrite(D972LROutput,D972LRReceipt);;
Print("D972_B4_LITERAL_ROW18_STAGE_V1_FINAL status=",D972LRStatus,
  " output=",D972LROutput," relation_rank=",D972LRRelationSpan.rank,
  " solutions=",Length(D972LRSolutions),"\n");
Print("D972_B4_LITERAL_ROW18_STAGE_V1_FINAL\n");
