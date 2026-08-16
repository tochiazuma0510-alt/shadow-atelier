#############################################################################
## d972_b4_u_anupq_kernel_v2.g -- canonical raw Schreier ANUPQ lane.
##
## This is deliberately independent of the exploratory v1 Tietze path.  The
## kernel K=ker(U->C2^5) is presented directly in the canonical 161-generator
## ordinary Reidemeister--Schreier basis and its 5056 relators.  No
## GAP coset-table simplification or reduced presentation is used for either
## the relators or the norm words.
##
## A nonidentity norm image in a finite p-quotient of K is a B4-A candidate:
## take the core of the kernel in U.  A bounded all-pass is UNKNOWN, never a
## terminal result.  Every receipt exposes the basis recipe and all source
## digests needed to replay the raw presentation independently.
#############################################################################

if LoadPackage("json")<>true then Error("ANUPQ v2: json package unavailable"); fi;
if not IsBound(PQuotient) then Error("ANUPQ v2: PQuotient unavailable"); fi;

D972ANV2Input:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972ANV2Words:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972ANV2Output:=Filename(DirectoryTemporary(),"d972_b4_u_anupq_kernel_v2.json");;
if IsBound(D972_B4_ANUPQ_INPUT) then D972ANV2Input:=D972_B4_ANUPQ_INPUT; fi;
if IsBound(D972_B4_ANUPQ_WORDS) then D972ANV2Words:=D972_B4_ANUPQ_WORDS; fi;
if IsBound(D972_B4_ANUPQ_OUTPUT) then D972ANV2Output:=D972_B4_ANUPQ_OUTPUT; fi;
D972ANV2SourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972ANV2RelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972ANV2NormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972ANV2WordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972ANV2Rho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;
D972ANV2GenBits:=[1,2,4,8,16,31];;
D972ANV2ExpectedRSGenerators:=161;;
D972ANV2ExpectedRSRelators:=5056;;
D972ANV2ExpectedNorms:=972;;
D972ANV2ExpectedRawRelSha:="29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e";;
D972ANV2ExpectedNormRSSha:="f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8";;

D972ANV2Join:=function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1];
  for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972ANV2Json:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsString(x) then
    return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\"");
  fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("ANUPQ v2 JSON type drift"); fi;
  if Length(x)=0 then return "[]"; fi;
  p:=List([1..Length(x)],i->D972ANV2Json(x[i]));
  return Concatenation("[",D972ANV2Join(p,","),"]");
end;;
D972ANV2SignedWord:=function(row,gens)
  local w,x;
  w:=One(gens[1]);
  for x in row do
    if x>0 then w:=w*gens[x]; else w:=w*gens[-x]^-1; fi;
  od;
  return w;
end;;
D972ANV2FreeReduce:=function(word)
  local out,x,n;
  out:=[];
  for x in word do
    n:=Length(out);
    if n>0 and out[n]=-x then Remove(out,n); else Add(out,x); fi;
  od;
  return out;
end;;
D972ANV2InverseWord:=function(word)
  return List(Reversed(word),x->-x);
end;;
D972ANV2Toggle:=function(mask,bit)
  if QuoInt(mask,bit) mod 2=1 then return mask-bit; fi;
  return mask+bit;
end;;
D972ANV2TransversalWord:=function(mask)
  local out,bit;
  out:=[];
  for bit in [0..4] do
    if QuoInt(mask,2^bit) mod 2=1 then Add(out,bit+1); fi;
  od;
  return out;
end;;

## Rewrite a word in the original six generators through the canonical
## regular C2^5 transversal.  Pair IDs are assigned mask-major, generator-
## minor, with the identity Schreier pairs omitted.
D972ANV2RSRewrite:=function(word,start,pairId)
  local mask,out,letter,gen,bit,id;
  mask:=start; out:=[];
  for letter in word do
    gen:=AbsInt(letter); bit:=D972ANV2GenBits[gen];
    if letter>0 then
      id:=pairId[mask+1][gen];
      if id>0 then Add(out,id); fi;
      mask:=D972ANV2Toggle(mask,bit);
    else
      mask:=D972ANV2Toggle(mask,bit);
      id:=pairId[mask+1][gen];
      if id>0 then Add(out,-id); fi;
    fi;
  od;
  if mask<>start then Error("ANUPQ v2 Schreier word does not close"); fi;
  return D972ANV2FreeReduce(out);
end;;

## Canonical raw ordinary RS construction.  This is the source of truth for
## both the p-quotient presentation and the norm coordinates.
D972ANV2BuildRawRS:=function(relators)
  local reps,pairId,pairWords,mask,gen,bit,raw,word,id,rs,start,rel;
  reps:=List([0..31],D972ANV2TransversalWord);
  pairId:=List([1..32],i->List([1..6],j->0));
  pairWords:=[];
  for mask in [0..31] do
    for gen in [1..6] do
      bit:=D972ANV2GenBits[gen];
      raw:=Concatenation(reps[mask+1],[gen],
        D972ANV2InverseWord(reps[D972ANV2Toggle(mask,bit)+1]));
      word:=D972ANV2FreeReduce(raw);
      if Length(word)>0 then
        Add(pairWords,word); id:=Length(pairWords);
        pairId[mask+1][gen]:=id;
      fi;
    od;
  od;
  if Length(pairWords)<>D972ANV2ExpectedRSGenerators then
    Error("ANUPQ v2 raw Schreier generator count drift");
  fi;
  rs:=[];
  for start in [0..31] do
    for rel in relators do
      word:=D972ANV2RSRewrite(rel,start,pairId);
      if Length(word)>0 then Add(rs,word); fi;
    od;
  od;
  if Length(rs)<>D972ANV2ExpectedRSRelators then
    Error("ANUPQ v2 raw Schreier relator count drift");
  fi;
  return rec(pair_id:=pairId,pair_words:=pairWords,relators:=rs,
    transversal:=reps);
end;;

D972ANV2RhoMapWord:=function(word,rho)
  local out,letter,img;
  out:=[];
  for letter in word do
    img:=rho[AbsInt(letter)];
    if letter<0 then img:=D972ANV2InverseWord(img); fi;
    out:=Concatenation(out,img);
  od;
  return D972ANV2FreeReduce(out);
end;;
D972ANV2ExactNorm:=function(f2word,rho)
  local j,letter,orbit,v,t,z;
  j:=[];
  for letter in f2word do
    if AbsInt(letter)=1 then
      Add(j,SignInt(letter)*1);
    elif AbsInt(letter)=2 then
      Add(j,SignInt(letter)*4);
    else Error("ANUPQ v2 F2 alphabet drift"); fi;
  od;
  j:=D972ANV2FreeReduce(j); orbit:=[]; v:=j;
  for t in [1..5] do Add(orbit,v); v:=D972ANV2RhoMapWord(v,rho); od;
  z:=[];
  for t in Reversed([1..5]) do z:=D972ANV2FreeReduce(Concatenation(z,orbit[t])); od;
  return z;
end;;

D972ANV2Source:=StringFile(D972ANV2Input);;
if D972ANV2Source=fail or HexSHA256(D972ANV2Source)<>D972ANV2SourceSha then
  Error("ANUPQ v2 canonical source SHA drift");
fi;
D972ANV2Obj:=JsonStringToGap(D972ANV2Source);;
if D972ANV2Obj.schema<>"d972-b4-p2-magnus-input/v2" or
   Length(D972ANV2Obj.all_relators)<>158 or
   D972ANV2Obj.rho_words<>D972ANV2Rho or
   D972ANV2Obj.all_relators_sha256<>D972ANV2RelSha or
   HexSHA256(D972ANV2Json(D972ANV2Obj.all_relators))<>D972ANV2RelSha then
  Error("ANUPQ v2 canonical source gate failed");
fi;
D972ANV2WordSource:=StringFile(D972ANV2Words);;
if D972ANV2WordSource=fail or HexSHA256(D972ANV2WordSource)<>D972ANV2WordsSha then
  Error("ANUPQ v2 word artifact SHA drift");
fi;
D972ANV2WordObj:=JsonStringToGap(D972ANV2WordSource);;
if D972ANV2WordObj.schema<>"d972-b4-word-key-artifact/v1" or
   D972ANV2WordObj.count<>D972ANV2ExpectedNorms or
   D972ANV2WordObj.canonical_bytes_sha256<>HexSHA256(
     D972ANV2Json(D972ANV2WordObj.rows)) then
  Error("ANUPQ v2 word artifact gate failed");
fi;
Print("B4_ANUPQ_V2_INPUT_PASS source_sha256=",D972ANV2SourceSha,
  " relator_sha256=",D972ANV2RelSha," word_artifact_sha256=",D972ANV2WordsSha,
  " basis=raw161 relators=5056 index=32\n");

D972ANV2Raw:=D972ANV2BuildRawRS(D972ANV2Obj.all_relators);;
D972ANV2RawRelSha:=HexSHA256(D972ANV2Json(D972ANV2Raw.relators));;
D972ANV2NormRows:=[]; D972ANV2NormOriginal:=[];
for D972ANV2Row in D972ANV2WordObj.rows do
  D972ANV2Norm:=D972ANV2ExactNorm(D972ANV2Row[3],D972ANV2Rho);;
  Add(D972ANV2NormOriginal,D972ANV2Norm);
  Add(D972ANV2NormRows,
    D972ANV2RSRewrite(D972ANV2Norm,0,D972ANV2Raw.pair_id));
od;
if Length(D972ANV2NormRows)<>D972ANV2ExpectedNorms or
   HexSHA256(D972ANV2Json(D972ANV2NormOriginal))<>D972ANV2NormSha then
  Error("ANUPQ v2 norm source/digest drift");
fi;
D972ANV2NormRSSha:=HexSHA256(D972ANV2Json(D972ANV2NormRows));;
if D972ANV2RawRelSha<>D972ANV2ExpectedRawRelSha or
   D972ANV2NormRSSha<>D972ANV2ExpectedNormRSSha then
  Error("ANUPQ v2 canonical raw RS digest drift");
fi;
if ForAny(D972ANV2NormRows,w->ForAny(w,x->AbsInt(x)>D972ANV2ExpectedRSGenerators)) then
  Error("ANUPQ v2 norm RS basis drift");
fi;
Print("B4_ANUPQ_V2_RAW_RS_PASS generators=",Length(D972ANV2Raw.pair_words),
  " relators=",Length(D972ANV2Raw.relators)," raw_relators_sha256=",D972ANV2RawRelSha,
  " norm_rs_sha256=",D972ANV2NormRSSha," norms=972\n");
if IsBound(D972_B4_ANUPQ_SELFTEST) and D972_B4_ANUPQ_SELFTEST=true then
  Print("B4_ANUPQ_V2_SELFTEST_PASS basis=raw161 relators=5056 norms=972\n");
  Print("B4_ANUPQ_V2_SELFTEST_FINAL_MARKER source_sha256=",D972ANV2SourceSha,
    " raw_rs_sha256=",D972ANV2ExpectedRawRelSha," norm_rs_sha256=",
    D972ANV2ExpectedNormRSSha,"\n");
  QUIT;
fi;

## Build the exact raw presentation.  This is intentionally 161-generator;
## no transported images or reduced presentation enters the quotient map.
D972ANV2RawF:=FreeGroup(D972ANV2ExpectedRSGenerators,"kraw");;
D972ANV2RawG:=GeneratorsOfGroup(D972ANV2RawF);;
D972ANV2RawRelWords:=List(D972ANV2Raw.relators,
  w->D972ANV2SignedWord(w,D972ANV2RawG));;
D972ANV2Kfp:=D972ANV2RawF/D972ANV2RawRelWords;;
D972ANV2Kgens:=GeneratorsOfGroup(D972ANV2Kfp);;
if Length(D972ANV2Kgens)<>D972ANV2ExpectedRSGenerators then
  Error("ANUPQ v2 raw fp generator count drift");
fi;

D972ANV2Classes:=[2,3];;
if IsBound(D972_B4_ANUPQ_CLASSES) then D972ANV2Classes:=D972_B4_ANUPQ_CLASSES; fi;
D972ANV2ClassRows:=[];; D972ANV2Terminal:=false;;
for D972ANV2Class in D972ANV2Classes do
  Print("B4_ANUPQ_V2_CLASS_BEGIN class=",D972ANV2Class,"\n");
  D972ANV2Q:=PQuotient(D972ANV2Kfp,3,D972ANV2Class,4096,
    "combinatorial":noninteractive);;
  if D972ANV2Q=fail then
    Add(D972ANV2ClassRows,rec(class:=D972ANV2Class,status:="UNKNOWN_RESOURCE"));
    Print("B4_ANUPQ_V2_CLASS_UNKNOWN class=",D972ANV2Class,"\n");
    continue;
  fi;
  D972ANV2Map:=EpimorphismQuotientSystem(D972ANV2Q);;
  D972ANV2H:=Image(D972ANV2Map);;
  D972ANV2QG:=List(D972ANV2Kgens,g->Image(D972ANV2Map,g));;
  D972ANV2Pcgs:=Pcgs(D972ANV2H);;
  D972ANV2QImages:=List(D972ANV2QG,
    g->List(ExponentsOfPcElement(D972ANV2Pcgs,g),Int));
  D972ANV2PcgsOrders:=List(RelativeOrders(D972ANV2Pcgs),Int);
  D972ANV2PowerRelations:=List([1..Length(D972ANV2Pcgs)],
    i->List(ExponentsOfPcElement(D972ANV2Pcgs,
      D972ANV2Pcgs[i]^D972ANV2PcgsOrders[i]),Int));
  D972ANV2ConjugateRelations:=[];
  if Length(D972ANV2Pcgs)>1 then
    for D972ANV2I in [2..Length(D972ANV2Pcgs)] do
      for D972ANV2J in [1..D972ANV2I-1] do
        Add(D972ANV2ConjugateRelations,
          [D972ANV2I,D972ANV2J,
           List(ExponentsOfPcElement(D972ANV2Pcgs,
             D972ANV2Pcgs[D972ANV2I]^D972ANV2Pcgs[D972ANV2J]),Int)]);
      od;
    od;
  fi;
  D972ANV2BadCount:=0; D972ANV2First:=fail;
  for D972ANV2I in [1..D972ANV2ExpectedNorms] do
    D972ANV2Z:=One(D972ANV2H);
    for D972ANV2Letter in D972ANV2NormRows[D972ANV2I] do
      if D972ANV2Letter>0 then
        D972ANV2Z:=D972ANV2Z*D972ANV2QG[D972ANV2Letter];
      else
        D972ANV2Z:=D972ANV2Z*D972ANV2QG[-D972ANV2Letter]^-1;
      fi;
    od;
    if not IsOne(D972ANV2Z) then
      D972ANV2BadCount:=D972ANV2BadCount+1;
      if D972ANV2First=fail then
        D972ANV2First:=rec(index:=D972ANV2I,
          norm_rs:=D972ANV2NormRows[D972ANV2I],
          image:=List(ExponentsOfPcElement(D972ANV2Pcgs,D972ANV2Z),Int));
      fi;
    fi;
  od;
  if D972ANV2First<>fail then D972ANV2Terminal:=true; fi;
  if D972ANV2BadCount>0 then D972ANV2ClassStatus:="DEFECT";
  else D972ANV2ClassStatus:="ALLPASS"; fi;
  Add(D972ANV2ClassRows,rec(class:=D972ANV2Class,status:=
    D972ANV2ClassStatus,order:=Size(D972ANV2H),
    pcgs_relative_orders:=D972ANV2PcgsOrders,
    pcgs_power_relations:=D972ANV2PowerRelations,
    pcgs_conjugate_relations:=D972ANV2ConjugateRelations,
    quotient_generator_images:=D972ANV2QImages,bad_count:=D972ANV2BadCount,
    first_defect:=D972ANV2First));
  Print("B4_ANUPQ_V2_CLASS_DONE class=",D972ANV2Class,
    " order=",Size(D972ANV2H)," bad_count=",D972ANV2BadCount,"\n");
  if D972ANV2Terminal then
    Print("B4_ANUPQ_V2_FIRST_DEFECT class=",D972ANV2Class,
      " index=",D972ANV2First.index,"\n");
    break;
  fi;
od;

D972ANV2TopStatus:="UNKNOWN_P3_BOUNDED";;
if D972ANV2Terminal then D972ANV2TopStatus:="B4_A_CANDIDATE_P3"; fi;
## GAP's JSON package is intentionally not used for output so receipt bytes
## are deterministic across package versions.
D972ANV2ClassJson:=function(C)
  local first;
  if C.status="UNKNOWN_RESOURCE" then
    return Concatenation("{\"class\":",String(C.class),
      ",\"status\":\"UNKNOWN_RESOURCE\"}");
  fi;
  if C.first_defect=fail then first:="null";
  else first:=Concatenation("{\"index\":",String(C.first_defect.index),
    ",\"norm_rs\":",D972ANV2Json(C.first_defect.norm_rs),
    ",\"image\":",D972ANV2Json(C.first_defect.image),"}"); fi;
  return Concatenation("{\"class\":",String(C.class),
    ",\"status\":",D972ANV2Json(C.status),",\"order\":",String(C.order),
    ",\"pcgs_relative_orders\":",D972ANV2Json(C.pcgs_relative_orders),
    ",\"pcgs_power_relations\":",D972ANV2Json(C.pcgs_power_relations),
    ",\"pcgs_conjugate_relations\":",D972ANV2Json(C.pcgs_conjugate_relations),
    ",\"quotient_generator_images\":",D972ANV2Json(C.quotient_generator_images),
    ",\"bad_count\":",String(C.bad_count),",\"first_defect\":",first,"}");
end;;
D972ANV2ClassStrings:=List(D972ANV2ClassRows,D972ANV2ClassJson);;
D972ANV2Out:=Concatenation(
  "{\"schema\":\"d972-b4-u-anupq-kernel/v2\",\"status\":",
  D972ANV2Json(D972ANV2TopStatus),
  ",\"source_sha256\":",D972ANV2Json(D972ANV2SourceSha),
  ",\"relator_sha256\":",D972ANV2Json(D972ANV2RelSha),
  ",\"word_artifact_sha256\":",D972ANV2Json(D972ANV2WordsSha),
  ",\"norm_original_sha256\":",D972ANV2Json(D972ANV2NormSha),
  ",\"raw_rs_relators_sha256\":",D972ANV2Json(D972ANV2RawRelSha),
  ",\"norm_rs_sha256\":",D972ANV2Json(D972ANV2NormRSSha),
  ",\"quotient_prime\":3,\"p_quotient_bound\":4096,\"requested_classes\":",
  D972ANV2Json(D972ANV2Classes),
  ",\"completed_classes\":",D972ANV2Json(List(D972ANV2ClassRows,C->C.class)),
  ",\"basis_contract\":{\"basis_id\":\"regular_c2^5_mask_transversal_v1\",",
  "\"coset_count\":32,\"original_generator_count\":6,\"rs_generator_count\":161,",
  "\"rs_relator_count\":5056,\"gen_bits\":",D972ANV2Json(D972ANV2GenBits),
  ",\"transversal\":",D972ANV2Json(D972ANV2Raw.transversal),"},",
  "\"norm_count\":972,\"classes\":[",D972ANV2Join(D972ANV2ClassStrings,","),"]}");
D972ANV2Fout:=OutputTextFile(D972ANV2Output,false);;
SetPrintFormattingStatus(D972ANV2Fout,false);
PrintTo(D972ANV2Fout,Concatenation(D972ANV2Out,"\n"));;
CloseStream(D972ANV2Fout);
Print("B4_ANUPQ_V2_FINAL_MARKER output=",D972ANV2Output,
  " status=",D972ANV2TopStatus,"\n");
QUIT;
