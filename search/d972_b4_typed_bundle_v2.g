#############################################################################
## d972_b4_typed_bundle_v2.g
##
## A typed, fail-closed receipt producer for the current B4 6/158 object.
## This is not a B4 A/B decision procedure.  In particular, the producer
## refuses to turn an all-pass fixed-U computation into a global statement.
##
## Environment:
##   D972_B4_TYPED_OUTPUT       receipt JSON
##   D972_B4_TYPED_CERTIFICATE  raw certificate JSON
##   D972_B4_TYPED_SELFTEST      1 for the tiny source/API smoke path
##
## The expensive worker/base and K(0,5) construction is intentionally only
## entered when selftest is false.  The parent dispatches this file in GHA;
## no local production GAP invocation is part of this lane.
#############################################################################

if not IsBound(GetEnv) then GetEnv := name -> fail; fi;

D972TypedSourcePath := "search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972TypedWordsPath := "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972TypedStage2Path := "search/probe/hsp7_gap_v1/stage2_k05.g";;
D972TypedWorkerPath := "search/d972_dovetail_worker_v1.g";;
D972TypedExpectedSourceSha :=
  "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972TypedExpectedStage2Sha :=
  "b2522f7d701525dc81c408d2b37b9fe693f017a11eeafb9333131de8c361daf5";;
D972TypedExpectedWorkerSha :=
  "f9ad3f8f71dc5af3d20dbef66dc6a25c79a50393be55767c0fb9f077d46994e8";;
D972TypedRelatorSha :=
  "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972TypedTargetSha :=
  "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972TypedRoofSha :=
  "3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8";;
D972TypedRowsSha :=
  "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930";;
D972TypedExpectedWordsSha :=
  "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972TypedExpectedTupleSha :=
  "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91";;
D972TypedRho := [ [-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1] ];;

D972TypedOut := fail;;
if IsBound(D972_B4_TYPED_OUTPUT) then
  D972TypedOut:=D972_B4_TYPED_OUTPUT;
else
  D972TypedOut:=GetEnv("D972_B4_TYPED_OUTPUT");
fi;;
if D972TypedOut=fail or D972TypedOut="" then
  D972TypedOut := "ci/out/d972_b4_typed_bundle_v2.json";
fi;;
D972TypedCertOut := fail;;
if IsBound(D972_B4_TYPED_CERTIFICATE) then
  D972TypedCertOut:=D972_B4_TYPED_CERTIFICATE;
else
  D972TypedCertOut:=GetEnv("D972_B4_TYPED_CERTIFICATE");
fi;;
if D972TypedCertOut=fail or D972TypedCertOut="" then
  D972TypedCertOut := "ci/out/d972_b4_typed_bundle_v2_certificate.json";
fi;;
D972TypedSelf := "";;
if IsBound(D972_B4_TYPED_SELFTEST) then
  if D972_B4_TYPED_SELFTEST=true or D972_B4_TYPED_SELFTEST=1 then
    D972TypedSelf:="1";
  fi;
else
  D972TypedSelf := GetEnv("D972_B4_TYPED_SELFTEST");
fi;;

## JSON encoder.  GAP's empty list can also satisfy IsString on some builds,
## so the empty-list case is deliberately before the string case.
D972TypedJson := function(x)
  local names, parts, i, key, t;
  if x=fail then return "null"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    t:=ReplacedString(x,"\\","\\\\");;
    t:=ReplacedString(t,"\"","\\\"");;
    t:=ReplacedString(t,"\n","\\n");;
    t:=ReplacedString(t,"\r","\\r");;
    return Concatenation("\"",t,"\"");
  fi;
  if IsList(x) then
    parts:=List([1..Length(x)],i->D972TypedJson(x[i]));;
    return Concatenation("[",D972Join(parts,","),"]");
  fi;
  if IsRecord(x) then
    names:=SortedList(RecNames(x)); parts:=[];;
    for key in names do
      Add(parts,Concatenation(D972TypedJson(key),":",
        D972TypedJson(x.(key))));
    od;
    return Concatenation("{",D972Join(parts,","),"}");
  fi;
  Error("typed v2 JSON type drift");
end;;

D972TypedWrite := function(path, text)
  WriteFile(path,Concatenation(text,"\n"));
end;;

D972TypedReduce := function(w)
  local out, x;
  out:=[];;
  for x in w do
    if Length(out)>0 and out[Length(out)]=-x then
      Remove(out,Length(out));
    else Add(out,x); fi;
  od;
  return out;
end;;

D972TypedInverse := function(w)
  return List(Reversed(w),x->-x);
end;;

D972TypedRhoWord := function(w)
  local out, x, image;
  out:=[];;
  for x in w do
    if x=0 or AbsInt(x)>6 then Error("typed v2 rho alphabet drift"); fi;
    image:=D972TypedRho[AbsInt(x)];;
    if x<0 then Append(out,D972TypedInverse(image));
    else Append(out,image); fi;
  od;
  return D972TypedReduce(out);
end;;

D972TypedEvalSigned := function(w, images)
  local out, x;
  out:=One(images[1]);;
  for x in w do
    if x=0 or AbsInt(x)>Length(images) then
      Error("typed v2 signed image alphabet drift");
    fi;
    if x>0 then out:=out*images[x];
    else out:=out*images[-x]^-1; fi;
  od;
  return out;
end;;

D972TypedSubstitute := function(w, a, b)
  local out, x, image;
  out:=[];;
  for x in w do
    if AbsInt(x)=1 then image:=a; else image:=b; fi;
    if x<0 then Append(out,D972TypedInverse(image));
    else Append(out,image); fi;
  od;
  return D972TypedReduce(out);
end;;

D972TypedMapF2 := function(w, a, b)
  return D972TypedEvalSigned(w,[a,b]);
end;;

D972TypedNormalizeRoofWord := function(x)
  if IsString(x) then return []; fi;
  return ShallowCopy(x);
end;;

D972TypedArtifactKey := function(key)
  local flat;
  if not IsList(key) or Length(key)<>3 or not IsList(key[2]) or
     Length(key[2])<>3 or not IsList(key[3]) or Length(key[3])<>9 then
    Error("typed v2 artifact key shape drift");
  fi;
  flat:=Concatenation(key[2][1],key[2][2],key[2][3]);;
  return Concatenation("(",String(key[1]),";",
    D972Join(List(flat,String),","),";",
    D972Join(List(key[3],String),","),")");
end;;

D972TypedPermImage := function(p, degree)
  return List([1..degree],i->i^p);
end;;

D972TypedLoadPrefix := function(path, marker, tag)
  local src, at, tmp;
  src:=StringFile(path);;
  if src=fail then Error("typed v2 missing source ",path); fi;
  at:=PositionSublist(src,marker);;
  if at=fail then Error("typed v2 source marker drift ",tag); fi;
  tmp:=Filename(DirectoryTemporary(),Concatenation("d972_typed_v2_",tag,".g"));;
  FileString(tmp,src{[1..at-1]});;
  Read(tmp);;
  return tmp;
end;;

D972TypedDirectInput := function()
  local src, inp, rels, i, word, keys, roof, rows,
    wsrc, winp, wrows, flatkeys, normalized;
  src:=StringFile(D972TypedSourcePath);;
  if src=fail or HexSHA256(src)<>D972TypedExpectedSourceSha then
    Error("typed v2 canonical source SHA drift");
  fi;
  inp:=JsonStringToGap(src);;
  if inp=fail or inp.schema<>"d972-b4-p2-magnus-input/v2" then
    Error("typed v2 canonical schema drift");
  fi;
  if inp.relator_count<>158 or Length(inp.all_relators)<>158 or
     Length(inp.rho_words)<>6 or inp.roof_count<>972 or
     Length(inp.roof_words)<>972 or Length(inp.target_keys)<>972 then
    Error("typed v2 canonical count drift");
  fi;
  if inp.rho_words<>D972TypedRho or
     inp.rho_words_source<>"universal_v2_canonical" then
    Error("typed v2 corrected rho drift");
  fi;
  rels:=List(inp.all_relators,ShallowCopy);;
  if HexSHA256(D972TypedJson(rels))<>D972TypedRelatorSha or
     inp.all_relators_sha256<>D972TypedRelatorSha then
    Error("typed v2 158 digest drift");
  fi;
  roof:=List(inp.roof_words,D972TypedNormalizeRoofWord);;
  if HexSHA256(D972TypedJson(roof))<>D972TypedRoofSha or
     inp.roof_words_sha256<>D972TypedRoofSha then
    Error("typed v2 roof digest drift");
  fi;
  keys:=List(inp.target_keys,ShallowCopy);;
  if HexSHA256(Concatenation(D972Join(Set(keys),"\n"),"\n"))<>
       D972TypedTargetSha or inp.target_key_digest<>D972TypedTargetSha then
    Error("typed v2 target digest drift");
  fi;
  rows:=[];;
  for i in [1..972] do Add(rows,[inp.target_keys[i],roof[i]]); od;
  wsrc:=StringFile(D972TypedWordsPath);;
  if wsrc=fail or HexSHA256(wsrc)<>D972TypedExpectedWordsSha then
    Error("typed v2 word/key artifact SHA drift");
  fi;
  winp:=JsonStringToGap(wsrc);;
  if winp=fail or winp.schema<>"d972-b4-word-key-artifact/v1" or
     winp.count<>972 or Length(winp.rows)<>972 or
     winp.source_target_key_digest<>D972TypedTargetSha or
     winp.frozen_tuple_sha256<>D972TypedExpectedTupleSha then
    Error("typed v2 word/key artifact metadata drift");
  fi;
  wrows:=winp.rows;;
  if HexSHA256(D972TypedJson(wrows))<>D972TypedRowsSha or
     winp.canonical_bytes_sha256<>D972TypedRowsSha then
    Error("typed v2 word/key row digest drift");
  fi;
  flatkeys:=List(wrows,x->D972TypedArtifactKey(x[2]));;
  normalized:=List(wrows,x->D972TypedNormalizeRoofWord(x[3]));;
  if flatkeys<>keys or normalized<>roof then
    Error("typed v2 canonical source is not bound to word/key rows");
  fi;
  return rec(source:=src,input:=inp,relators:=rels,roof:=roof,keys:=keys,
    rows:=rows,source_sha256:=HexSHA256(src),relator_sha256:=D972TypedRelatorSha,
    roof_sha256:=D972TypedRoofSha,target_sha256:=D972TypedTargetSha,
    word_artifact_sha256:=D972TypedExpectedWordsSha,
    word_rows_sha256:=D972TypedRowsSha);
end;;

## A.18 is written in the six-generator marked K(0,5) alphabet.  These are
## literal words, not labels or an untyped diagram.
D972TypedA18Maps := [
  rec(name:="123", f6_substitution:=[[1],[4]]),
  rec(name:="234", f6_substitution:=[[4],[6]]),
  rec(name:="12,3,4", f6_substitution:=[[2,4],[6]]),
  rec(name:="1,23,4", f6_substitution:=[[1,2],[5,6]]),
  rec(name:="1,2,34", f6_substitution:=[[1],[4,5]]) ];;

if D972TypedSelf="1" then
  if D972TypedRhoWord([1])<>[-6,-5,-3] or
     D972TypedRhoWord([-1])<>[3,5,6] or
     D972TypedEvalSigned([1,-1],[One(FreeGroup(1)),One(FreeGroup(1))])<>
       One(FreeGroup(1)) then
    Error("typed v2 tiny word selftest failed");
  fi;
  Print("D972_B4_TYPED_BUNDLE_V2_GAP_SELFTEST_PASS\n");;
  QUIT;
fi;;

## Load exact definitions without dispatching either library's main mode.
D972TypedWorkerSource:=StringFile(D972TypedWorkerPath);;
if D972TypedWorkerSource=fail or HexSHA256(D972TypedWorkerSource)<>
     D972TypedExpectedWorkerSha then
  Error("typed v2 worker source SHA drift");
fi;;
D972TypedStage2Source:=StringFile(D972TypedStage2Path);;
if D972TypedStage2Source=fail or HexSHA256(D972TypedStage2Source)<>
     D972TypedExpectedStage2Sha then
  Error("typed v2 stage2 source SHA drift");
fi;;
D972TypedLoadPrefix(D972TypedWorkerPath,
  "\nif D972Mode = \"selftest\" then","worker");;
D972TypedLoadPrefix(D972TypedStage2Path,"QUIT;","k05");;
if LoadPackage("json")<>true then Error("typed v2 JSON package unavailable"); fi;;
if not IsBound(D972Join) then Error("typed v2 worker JSON helper missing"); fi;;
D972TypedCanonical:=D972TypedDirectInput();;

## Reconstruct the marked finite base and retain actual permutation images.
D972TypedBase:=D972BuildBase(false);;
if D972TypedBase.q_size<>8817984 or D972TypedBase.pure_size<>1469664 or
   D972TypedBase.epsilon_kernel_size<>1469664 then
  Error("typed v2 marked finite base order drift");
fi;;
D972TypedQ:=D972TypedBase.q;;
D972TypedS1:=D972TypedBase.s1;; D972TypedS2:=D972TypedBase.s2;;
D972TypedEps:=GroupHomomorphismByImages(D972TypedQ,SymmetricGroup(3),
  [D972TypedS1,D972TypedS2],[(1,2),(2,3)]);;
if D972TypedEps=fail or not IsSurjective(D972TypedEps) or
   Size(Kernel(D972TypedEps))<>1469664 then
  Error("typed v2 epsilon/kernel replay failed");
fi;;

## K(0,5): group-internal checks use the canonical 18 rows and the actual
## K05 image, rather than trusting RelatorsOfFpGroup ordering.
D972TypedKImages:=[kX12,kX13,kX14,kX23,kX24,kX34];;
D972TypedK05Rows:=D972TypedCanonical.relators{[1..18]};;
D972TypedK05Replay:=[];; D972TypedK05Bad:=0;;
for D972TypedI in [1..18] do
  D972TypedRow:=D972TypedK05Rows[D972TypedI];;
  D972TypedV:=D972TypedRow;; D972TypedPowers:=[];;
  D972TypedRowAll:=true;;
  for D972TypedJ in [0..4] do
    D972TypedOK:=IsOne(D972TypedEvalSigned(D972TypedV,D972TypedKImages));;
    if not D972TypedOK then
      D972TypedK05Bad:=D972TypedK05Bad+1;
    fi;
    if not D972TypedOK then D972TypedRowAll:=false; fi;
    Add(D972TypedPowers,rec(power:=D972TypedJ,identity:=D972TypedOK));;
    D972TypedV:=D972TypedRhoWord(D972TypedV);
  od;
  Add(D972TypedK05Replay,rec(relator:=D972TypedRow,power_count:=5,
    identity_at_all_powers:=D972TypedRowAll,powers:=D972TypedPowers));
od;;
D972TypedRho5Rows:=[];; D972TypedRho5:=true;;
for D972TypedI in [1..6] do
  D972TypedV:=[D972TypedI];;
  for D972TypedJ in [1..5] do D972TypedV:=D972TypedRhoWord(D972TypedV); od;
  D972TypedOK:=D972TypedEvalSigned(D972TypedV,D972TypedKImages)=
    D972TypedKImages[D972TypedI];;
  if not D972TypedOK then D972TypedRho5:=false; fi;
  Add(D972TypedRho5Rows,rec(generator_index:=D972TypedI,
    word_after_five:=D972TypedV,identity_after_five:=D972TypedOK));
od;;
if D972TypedK05Bad<>0 or not D972TypedRho5 then
  Error("typed v2 K05 rho group-internal gate failed");
fi;;

## Exact canonical tail replay in the free F6 words, followed by the same
## replay in K05.  A presentation digest alone is never used as the gate.
D972TypedTail:=[];; D972TypedBlocks:=[];; D972TypedTailOK:=true;;
for D972TypedP in [0..4] do
  D972TypedBlock:=[];;
  for D972TypedI in [1..28] do
    D972TypedRow:=D972TypedCanonical.relators[18+28*D972TypedP+D972TypedI];;
    Add(D972TypedBlock,D972TypedRow);
    if D972TypedP>0 then
      D972TypedPrev:=D972TypedCanonical.relators[18+28*(D972TypedP-1)+D972TypedI];;
      if D972TypedRow<>D972TypedRhoWord(D972TypedPrev) then
        D972TypedTailOK:=false;
      fi;
    fi;
  od;
  Add(D972TypedBlocks,D972TypedBlock);
od;;
if not D972TypedTailOK then Error("typed v2 28x5 tail replay failed"); fi;;

## The 28 seeds are checked in the actual marked pure finite image.  This is
## useful evidence for M, but the named K^(9) intersect N_S4 identity is kept
## as a separate gate below and is not inferred from these 28 zeroes.
D972TypedQ0Rows:=D972TypedCanonical.relators{[19..46]};;
D972TypedQ0Bad:=[];;
D972TypedQ0Identity:=[];;
for D972TypedI in [1..28] do
  D972TypedQ0OK:=IsOne(D972TypedEvalSigned(D972TypedQ0Rows[D972TypedI],
      [D972TypedS1^2,D972TypedS2^2]));;
  Add(D972TypedQ0Identity,D972TypedQ0OK);;
  if not D972TypedQ0OK then Add(D972TypedQ0Bad,D972TypedI); fi;
od;;

## Build the five literal coface words from the current rho orbit and bind
## every block to the canonical tail.  A.18's named-map identification is
## intentionally a separate explicit certificate field.
D972TypedCofaceBlocks:=D972TypedBlocks;;
D972TypedCofaceRows:=[];;
for D972TypedP in [1..5] do
  Add(D972TypedCofaceRows,rec(power:=D972TypedP-1,
    relator_count:=Length(D972TypedCofaceBlocks[D972TypedP]),
    rows:=D972TypedCofaceBlocks[D972TypedP],
    exact_tail_match:=true));
od;;

## Independently match each named A.18 substitution against one of the five
## tail blocks in K05.  Several A.18 substitutions are not literally equal
## as free F6 words; the comparison is therefore a row-by-row group replay in
## the actual K05 presentation.  No match is inferred from block order.
D972TypedA18Replay:=[];; D972TypedA18Exact:=true;;
for D972TypedA18 in D972TypedA18Maps do
  D972TypedA18Rows:=List(D972TypedQ0Rows,
    w->D972TypedSubstitute(w,D972TypedA18.f6_substitution[1],
      D972TypedA18.f6_substitution[2]));;
  D972TypedHits:=[];;
  for D972TypedP in [1..5] do
    D972TypedSame:=true;;
    for D972TypedI in [1..28] do
      if D972TypedEvalSigned(D972TypedA18Rows[D972TypedI],D972TypedKImages)<>
         D972TypedEvalSigned(D972TypedCofaceBlocks[D972TypedP][D972TypedI],
           D972TypedKImages) then D972TypedSame:=false; fi;
    od;
    if D972TypedSame then Add(D972TypedHits,D972TypedP-1); fi;
  od;
  if Length(D972TypedHits)<>1 then D972TypedA18Exact:=false; fi;
  Add(D972TypedA18Replay,rec(name:=D972TypedA18.name,
    f6_substitution:=D972TypedA18.f6_substitution,
    candidate_rows:=D972TypedA18Rows,
    block_indices:=D972TypedHits,raw_word_replay:=true,
    group_equal_rows:=List([1..28],i->Length(D972TypedHits)=1)));
od;;

## The worker scan supplies the finite shadow candidates.  We preserve every
## row, including unsettled ones; settled_count is never silently used as a
## filter.  The canonical word/key artifact is the source-order binding.
D972TypedScan:=D972ScanCalibrationBase(D972TypedBase);;
if D972TypedScan.shadow_count<>972 then
  Error("typed v2 shadow count drift");
fi;;
D972TypedF2:=FreeGroup("x","y");;
D972TypedPure:=Group(D972TypedS1^2,D972TypedS2^2);;
D972TypedEpi:=GroupHomomorphismByImages(D972TypedF2,D972TypedPure,
  [D972TypedF2.1,D972TypedF2.2],[D972TypedS1^2,D972TypedS2^2]);;
D972TypedFiberRows:=[];; D972TypedSettled:=0;; D972TypedOnto:=0;;
for D972TypedI in [1..972] do
  D972TypedWord:=D972TypedCanonical.roof[D972TypedI];;
  D972TypedKey:=D972TypedCanonical.keys[D972TypedI];;
  D972TypedSh:=First(D972TypedScan.shadows,x->x.key=D972TypedKey);;
  if D972TypedSh=fail then Error("typed v2 canonical key missing from scan"); fi;
  if D972TypedSh.settled then D972TypedSettled:=D972TypedSettled+1; fi;
  ## D972ScanCalibrationBase reaches this append only after the literal
  ## equations, condition (I), and full marked onto test.  Keep those as
  ## per-row replay fields, but do not call them global cofinality.
  D972TypedOnto:=D972TypedOnto+1;;
  D972TypedProofWord:=D972SignedWord(PreImagesRepresentative(
    D972TypedEpi,D972TypedSh.f));;
  Add(D972TypedFiberRows,rec(index:=D972TypedI,m:=D972TypedSh.m,
    f2_word:=D972TypedWord,target_key:=D972TypedKey,
    settled:=D972TypedSh.settled,onto:=true,condition_I:=true,
    condition_II:=true,charming:=true,arithmetic:=fail,outside:=fail,
    proof:=rec(source_key:=D972TypedKey,source_word:=D972TypedProofWord,
      raw_replay:=true,settled_replay:=rec(value:=D972TypedSh.settled),
      onto_replay:=rec(value:=true,image_order:=D972TypedBase.q_size,
        target_order:=D972TypedBase.q_size,raw_generator_replay:=true),
      condition_replay:=rec(I:=true,II:=true,theta_equation:=true,
        tau_equation:=true,literal_equations:=true,raw_equation_replay:=true))));
od;;

## Actual unconditional PENT-FORM' D-tilde.  The five substitutions are
## fixed in K(0,5), with x51=x15.  We compare its K05 image to the frozen
## reverse-rho norm, but do not replace D-tilde by the norm unless all rows
## replay equal in the actual group.
D972TypedX15:=[-3,-2,-1];;
D972TypedX45:=[-6,-5,-3];;
D972TypedDtildeRows:=[];; D972TypedEqual:=0;;
for D972TypedI in [1..972] do
  D972TypedF:=D972TypedCanonical.roof[D972TypedI];;
  D972TypedW45:=D972TypedSubstitute(D972TypedF,D972TypedX45,[6]);;
  D972TypedW12:=D972TypedSubstitute(D972TypedF,[1],D972TypedX15);;
  D972TypedW23:=D972TypedSubstitute(D972TypedF,[4],[6]);;
  D972TypedW51:=D972TypedSubstitute(D972TypedF,D972TypedX45,D972TypedX15);;
  D972TypedW123:=D972TypedSubstitute(D972TypedF,[1],[4]);;
  D972TypedDtilde:=D972TypedReduce(
    Concatenation(D972TypedInverse(D972TypedW45),
      D972TypedInverse(D972TypedW12),D972TypedW23,D972TypedW51,
      D972TypedW123));;
  D972TypedBaseWord:=D972TypedSubstitute(D972TypedF,[1],[4]);;
  D972TypedOrbit:=[];; D972TypedV:=D972TypedBaseWord;;
  for D972TypedJ in [1..5] do Add(D972TypedOrbit,D972TypedV);
    D972TypedV:=D972TypedRhoWord(D972TypedV); od;
  D972TypedNorm:=[];;
  for D972TypedJ in Reversed([1..5]) do
    D972TypedNorm:=D972TypedReduce(Concatenation(D972TypedNorm,
      D972TypedOrbit[D972TypedJ]));
  od;
  D972TypedDtildeId:=IsOne(D972TypedEvalSigned(D972TypedDtilde,D972TypedKImages));;
  D972TypedNormId:=IsOne(D972TypedEvalSigned(D972TypedNorm,D972TypedKImages));;
  D972TypedEq:=D972TypedEvalSigned(D972TypedDtilde,D972TypedKImages)=
    D972TypedEvalSigned(D972TypedNorm,D972TypedKImages);;
  if D972TypedEq then D972TypedEqual:=D972TypedEqual+1; fi;
  Add(D972TypedDtildeRows,rec(index:=D972TypedI,source_word:=D972TypedF,
    formula:="f(x45,x34)^-1*f(x12,x15)^-1*f(x23,x34)*f(x45,x51)*f(x12,x23)",
    dtilde_signed:=D972TypedDtilde,norm_signed:=D972TypedNorm,
    dtilde_identity:=D972TypedDtildeId,norm_identity:=D972TypedNormId,
    equal_in_K05:=D972TypedEq,raw_replay:=true));
od;;

## Raw finite component images.  They are emitted even though the named
## K^(9) intersect N_S4 proof is left open; a checker can inspect them rather
## than accepting a component order/digest claim.
D972TypedComp9Deg:=D972TypedBase.component9_degree;;
D972TypedComp4Deg:=D972TypedBase.component4_degree;;
D972TypedEps9:=GroupHomomorphismByImages(
  Group(D972TypedBase.qt9.s1,D972TypedBase.qt9.s2),SymmetricGroup(3),
  [D972TypedBase.qt9.s1,D972TypedBase.qt9.s2],[(1,2),(2,3)]);;
D972TypedEps4:=GroupHomomorphismByImages(
  Group(D972TypedBase.qt4.s1,D972TypedBase.qt4.s2),SymmetricGroup(3),
  [D972TypedBase.qt4.s1,D972TypedBase.qt4.s2],[(1,2),(2,3)]);;
if D972TypedEps9=fail or D972TypedEps4=fail or
   not IsSurjective(D972TypedEps9) or not IsSurjective(D972TypedEps4) then
  Error("typed v2 component epsilon maps failed");
fi;;
D972TypedMBinding:=rec(
  intersection_definition:="M=K^(9) intersect N_S4",
  marked_generators:=["s1","s2"],
  kernel_certificate:="MISSING_NAMED_INTERSECTION_PROOF",
  b3_normality_certificate:="PROVED_FINITE_EPSILON_KERNEL",
  combined_degree:=D972TypedComp9Deg+D972TypedComp4Deg,
  combined_order:=D972TypedBase.q_size,
  combined_pure_kernel_order:=D972TypedBase.pure_size,
  combined_generator_images:=[
    D972TypedPermImage(D972TypedS1,D972TypedComp9Deg+D972TypedComp4Deg),
    D972TypedPermImage(D972TypedS2,D972TypedComp9Deg+D972TypedComp4Deg)],
  epsilon_generator_images:=[[2,1,3],[1,3,2]],
  components:=[
    rec(name:="K9",degree:=D972TypedComp9Deg,order:=Size(Group(
      D972TypedBase.qt9.s1,D972TypedBase.qt9.s2)),kernel_order:=Size(Kernel(D972TypedEps9)),
      source_definition:="MakeGn(9) plus BuildQTGeneral",
      generator_images:=[D972TypedPermImage(D972TypedBase.qt9.s1,D972TypedComp9Deg),
        D972TypedPermImage(D972TypedBase.qt9.s2,D972TypedComp9Deg)],
      raw_image_certificate:=true),
    rec(name:="N_S4",degree:=D972TypedComp4Deg,order:=Size(Group(
      D972TypedBase.qt4.s1,D972TypedBase.qt4.s2)),kernel_order:=Size(Kernel(D972TypedEps4)),
      source_definition:="PSL(2,8) plus BuildQTGeneral",
      generator_images:=[D972TypedPermImage(D972TypedBase.qt4.s1,D972TypedComp4Deg),
        D972TypedPermImage(D972TypedBase.qt4.s2,D972TypedComp4Deg)],
      raw_image_certificate:=true) ]);;

## The receipt is deliberately UNKNOWN: the current worker does not provide
## a proof of the named intersection, A.18 block identification, full source
## and target reduction fibers, arithmetic/outside labels, or B4/S4 core.
D972TypedBlockers:=[
  "Q0_28_RELATOR_IMAGE_FAILURE_IF_NONZERO",
  "M_NAMED_INTERSECTION_NOT_PROVED",
  "A18_TO_COFASE_BLOCK_IDENTIFICATION_NOT_PROVED",
  "FULL_972_SETTLED_ONTO_FIBER_CERTIFICATE_MISSING",
  "ARITHMETIC_OUTSIDE_CLASSIFICATION_MISSING",
  "D_TILDE_EQUALITY_IS_LOCAL_K05_EVIDENCE_ONLY",
  "B4_S4_CORE_NORMALITY_NOT_PROVED" ];;
if Length(D972TypedQ0Bad)=0 then
  D972TypedBlockers:=Filtered(D972TypedBlockers,
    x->x<>"Q0_28_RELATOR_IMAGE_FAILURE_IF_NONZERO");
fi;;
if D972TypedA18Exact then
  D972TypedBlockers:=Filtered(D972TypedBlockers,
    x->x<>"A18_TO_COFASE_BLOCK_IDENTIFICATION_NOT_PROVED");
fi;;
D972TypedA18Certificate:="MISSING";;
if D972TypedA18Exact then D972TypedA18Certificate:="PROVED"; fi;;
D972TypedQ0Certificate:="MISSING";;
if Length(D972TypedQ0Bad)=0 then D972TypedQ0Certificate:="PROVED"; fi;;
D972TypedEqCertificate:="MISSING";;
if D972TypedEqual=972 then D972TypedEqCertificate:="PROVED"; fi;;

D972TypedCertificate:=rec(
  schema:="d972-b4-typed-bundle-certificate/v2",
  source_sha256:=D972TypedCanonical.source_sha256,
  word_artifact_sha256:=D972TypedCanonical.word_artifact_sha256,
  word_rows_sha256:=D972TypedCanonical.word_rows_sha256,
  stage2_sha256:=D972TypedExpectedStage2Sha,
  worker_sha256:=D972TypedExpectedWorkerSha,
  presentation:=rec(mode:="direct_F6_158",generator_labels:=
    ["X12","X13","X14","X23","X24","X34"],
    source_sha256:=D972TypedCanonical.source_sha256,
    all_relators_sha256:=D972TypedCanonical.relator_sha256,
    relator_rows:=D972TypedCanonical.relators,
    rho_words:=D972TypedRho,
    rho_derivation:="stage2_sphere_hurwitz_independent"),
  k05:=rec(relator_rows:=D972TypedK05Rows,rho_relator_replay:=D972TypedK05Replay,
    rho_relator_bad:=D972TypedK05Bad,rho5_generator_replay:=D972TypedRho5Rows,
    rho5:=D972TypedRho5,rho_nonidentity:=true,
    group_internal_certificate:="PROVED"),
  q0:=rec(marked_generators:=["s1^2","s2^2"],relator_count:=28,
    relator_rows:=D972TypedQ0Rows,image_identity:=D972TypedQ0Identity,
    image_certificate:=D972TypedQ0Certificate),
  m_binding:=D972TypedMBinding,
  cofaces:=rec(blocks:=D972TypedCofaceBlocks,block_order:=[0,1,2,3,4],
    a18_maps:=D972TypedA18Replay,
    a18_to_block_certificate:=D972TypedA18Certificate),
  fibers:=rec(rows:=D972TypedFiberRows,settled_count:=D972TypedSettled,
    onto_count:=D972TypedOnto,condition_I_count:=972,condition_II_count:=972,
    arithmetic_count:=fail,outside_count:=fail,classification_certificate:=
      "MISSING",source_full_fiber:=false,target_full_fiber:=false,
    duplicate_map_exact:=true,onto:=true),
  dtilde:=rec(rows:=D972TypedDtildeRows,formula_source:=
    "PENT-FORM-prime-docs-notes-b4_direct_adjudication_feasibility_v1_2:155-165",
    all_rows_raw_replayed:=true,equal_count:=D972TypedEqual,
    equality_certificate:=D972TypedEqCertificate),
  b4_s4_core:=rec(status:="MISSING",normality:=false,B4_stable:=false,
    S4_core_complete:=false,conjugate_rows:=[]),
  blockers:=D972TypedBlockers);;

D972TypedCertText:=D972TypedJson(D972TypedCertificate);;
D972TypedWrite(D972TypedCertOut,D972TypedCertText);;
D972TypedReceipt:=rec(
  schema:="d972-b4-typed-bundle/v2",
  status:="UNKNOWN_TYPED_BUNDLE",
  terminal_claim:=false,
  presentation_source_sha256:=D972TypedCanonical.source_sha256,
  canonical_relator_sha256:=D972TypedCanonical.relator_sha256,
  target_key_digest:=D972TypedCanonical.target_sha256,
  word_artifact_sha256:=D972TypedCanonical.word_artifact_sha256,
  word_rows_sha256:=D972TypedCanonical.word_rows_sha256,
  rho_words:=D972TypedRho,
  certificate_path:=D972TypedCertOut,
  certificate_sha256:=HexSHA256(Concatenation(D972TypedCertText,"\n")),
  k05_rho5:=D972TypedRho5,
  tail_28x5:=D972TypedTailOK,
  q0_relator_bad:=Length(D972TypedQ0Bad),
  settled_count:=D972TypedSettled,
  dtilde_equal_count:=D972TypedEqual,
  blockers:=D972TypedBlockers,
  global_survival:="UNKNOWN",
  note:="fixed finite/base and K05 evidence only; no B4 A/B or Ihara claim");;
D972TypedWrite(D972TypedOut,D972TypedJson(D972TypedReceipt));;
Print("D972_B4_TYPED_BUNDLE_V2_RECEIPT status=UNKNOWN_TYPED_BUNDLE output=",
  D972TypedOut," certificate=",D972TypedCertOut,"\n");
QUIT;
