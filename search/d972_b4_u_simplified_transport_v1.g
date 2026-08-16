#############################################################################
## d972_b4_u_simplified_transport_v1.g -- exact 6-to-5 generator transport.
##
## IsomorphismSimplifiedFpGroup is used only to produce a pinned presentation
## and both word maps.  The receipt contains the complete 5-generator/141-
## relator presentation, the images of both generator sets, and every one of
## the 972 exact roof norms in the simplified alphabet.  Optional KBMAG work
## is explicitly candidate-only; a bounded all-pass remains UNKNOWN.
#############################################################################

if LoadPackage("json")<>true then Error("SIMPLE transport: json unavailable"); fi;

D972STInput:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972STWords:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972STOutput:=Filename(DirectoryTemporary(),"d972_b4_u_simplified_transport_v1.json");;
if IsBound(D972_B4_SIMPLE_INPUT) then D972STInput:=D972_B4_SIMPLE_INPUT; fi;
if IsBound(D972_B4_SIMPLE_WORDS) then D972STWords:=D972_B4_SIMPLE_WORDS; fi;
if IsBound(D972_B4_SIMPLE_OUTPUT) then D972STOutput:=D972_B4_SIMPLE_OUTPUT; fi;
D972STSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972STRelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972STRho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;
D972STNormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972STWordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972STTargetSha:="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972STTupleSha:="32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91";;

D972STJoin:=function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1]; for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972STJson:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if x=true then return "true"; fi; if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("SIMPLE transport JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972STJson(x[i]));
  return Concatenation("[",D972STJoin(p,","),"]");
end;;
D972STSignedObj:=function(w)
  local e,o,i,g,n,j;
  e:=ExtRepOfObj(w); o:=[]; i:=1;
  while i<=Length(e) do
    g:=e[i]; n:=e[i+1];
    if n>0 then for j in [1..n] do Add(o,g); od;
    else for j in [1..-n] do Add(o,-g); od; fi;
    i:=i+2;
  od;
  return o;
end;;
D972STSignedWordObj:=function(row,gens)
  local w,x;
  w:=One(gens[1]);
  for x in row do
    if x>0 then w:=w*gens[x]; else w:=w*gens[-x]^-1; fi;
  od;
  return w;
end;;
D972STFreeReduce:=function(row)
  local out,x,n;
  out:=[];
  for x in row do n:=Length(out);
    if n>0 and out[n]=-x then Remove(out,n); else Add(out,x); fi;
  od;
  return out;
end;;
D972STMapWord:=function(row,map)
  local out,x,img;
  out:=[];
  for x in row do
    img:=map[AbsInt(x)];
    if x<0 then img:=List(Reversed(img),y->-y); fi;
    out:=D972STFreeReduce(Concatenation(out,img));
  od;
  return out;
end;;
D972STRhoWord:=function(w,rho)
  local out,x,img;
  out:=[];
  for x in w do img:=rho[AbsInt(x)];
    if x<0 then img:=List(Reversed(img),y->-y); fi;
    out:=Concatenation(out,img);
  od;
  return D972STFreeReduce(out);
end;;
D972STNormF6:=function(row,fg,rho)
  local j,x,orbit,v,z,t;
  j:=[];
  for x in row do
    if AbsInt(x)=1 then Add(j,SignInt(x)*1);
    elif AbsInt(x)=2 then Add(j,SignInt(x)*4);
    else Error("SIMPLE transport F2 alphabet drift"); fi;
  od;
  j:=D972STFreeReduce(j); orbit:=[]; v:=j;
  for t in [1..5] do Add(orbit,v); v:=D972STRhoWord(v,rho); od;
  z:=[]; for t in Reversed([1..5]) do z:=D972STFreeReduce(Concatenation(z,orbit[t])); od;
  return D972STSignedWordObj(z,fg);
end;;
D972STKey:=function(key)
  local flat,pair;
  flat:=[];
  for pair in key[2] do Append(flat,pair); od;
  return Concatenation("(",String(key[1]),";",D972STJoin(List(flat,String),","),";",
    D972STJoin(List(key[3],String),","),")");
end;;

D972STSource:=StringFile(D972STInput);;
if D972STSource=fail or HexSHA256(D972STSource)<>D972STSourceSha then Error("SIMPLE transport source SHA drift"); fi;
D972STObj:=JsonStringToGap(D972STSource);;
if D972STObj.schema<>"d972-b4-p2-magnus-input/v2" or
   Length(D972STObj.all_relators)<>158 or D972STObj.rho_words<>D972STRho or
   D972STObj.all_relators_sha256<>D972STRelSha then Error("SIMPLE transport source gate failed"); fi;
D972STWordSource:=StringFile(D972STWords);;
if D972STWordSource=fail or HexSHA256(D972STWordSource)<>D972STWordsSha then Error("SIMPLE transport words SHA drift"); fi;
D972STWordObj:=JsonStringToGap(D972STWordSource);;
if D972STWordObj.schema<>"d972-b4-word-key-artifact/v1" or D972STWordObj.count<>972 or
   D972STWordObj.source_target_key_digest<>D972STTargetSha or
   D972STWordObj.frozen_tuple_sha256<>D972STTupleSha then Error("SIMPLE transport word gate failed"); fi;

D972STF:=FreeGroup(6);; D972STFG:=GeneratorsOfGroup(D972STF);;
D972STRels:=List(D972STObj.all_relators,w->D972STSignedWordObj(w,D972STFG));;
D972STU:=D972STF/D972STRels;; D972STUG:=GeneratorsOfGroup(D972STU);;
D972STRhoFree:=[(D972STFG[3]*D972STFG[5]*D972STFG[6])^-1,D972STFG[3],D972STFG[5],
  (D972STFG[1]*D972STFG[2]*D972STFG[3])^-1,
  (D972STFG[1]*D972STFG[4]*D972STFG[5])^-1,D972STFG[1]];;
D972STNormF6Words:=[];; D972STNormUWords:=[];; D972STKeys:=[];;
for D972STRow in D972STWordObj.rows do
  D972STWord:=D972STRow[3];;
  if Length(D972STWord)=0 then D972STWord:=[]; fi;
  D972STF6Word:=D972STNormF6(D972STWord,D972STFG,D972STRho);;
  Add(D972STNormF6Words,D972STSignedObj(D972STF6Word));;
  Add(D972STNormUWords,D972STSignedObj(D972STF6Word));;
  Add(D972STKeys,D972STKey(D972STRow[2]));;
od;
if HexSHA256(D972STJson(D972STNormUWords))<>D972STNormSha then Error("SIMPLE transport norm digest drift"); fi;
Print("B4_SIMPLE_TRANSPORT_INPUT_PASS source_sha256=",D972STSourceSha,
  " relators=158 norms=972 norm_sha256=",D972STNormSha,"\n");

## GAP's simplifier supplies a genuine isomorphism U -> S.  Preserve both
## directions as words, so a later checker can bind the exact presentation.
D972STIso:=IsomorphismSimplifiedFpGroup(D972STU);;
D972STCheckMaps:=false;;
if IsBound(D972_B4_SIMPLE_CHECK_MAPS) then D972STCheckMaps:=D972_B4_SIMPLE_CHECK_MAPS; fi;
Print("B4_SIMPLE_TRANSPORT_ISO_RETURN\n");
D972STS:=Range(D972STIso);; D972STSG:=GeneratorsOfGroup(D972STS);;
D972STSimpleRels:=List(RelatorsOfFpGroup(D972STS),D972STSignedObj);;
if Length(D972STSG)<>5 or Length(D972STSimpleRels)<>141 then
  Error("SIMPLE transport expected 5/141 shape drift"); fi;
D972STInv:=InverseGeneralMapping(D972STIso);;
D972STUToS:=List(D972STUG,g->D972STSignedObj(Image(D972STIso,g)));;
D972STSgToU:=List(D972STSG,g->D972STSignedObj(Image(D972STInv,g)));;
D972STSimpleNorms:=List(D972STNormF6Words,w->D972STMapWord(w,D972STUToS));;
Print("B4_SIMPLE_TRANSPORT_WORDS_PASS\n");
D972STSimpleRelSha:=HexSHA256(D972STJson(D972STSimpleRels));;
D972STSimpleNormSha:=HexSHA256(D972STJson(D972STSimpleNorms));;
D972STMapSha:=HexSHA256(D972STJson([D972STUToS,D972STSgToU]));;
if D972STCheckMaps=true then
  D972STURelU:=List(D972STObj.all_relators,w->D972STSignedWordObj(w,D972STUG));;
  D972STSimpleRelS:=List(D972STSimpleRels,w->D972STSignedWordObj(w,D972STSG));;
  if ForAny(D972STURelU,r->not IsOne(Image(D972STIso,r))) then Error("SIMPLE transport relator map failure"); fi;
  if ForAny(D972STSimpleRelS,r->not IsOne(Image(D972STInv,r))) then Error("SIMPLE transport inverse relator map failure"); fi;
fi;
Print("B4_SIMPLE_TRANSPORT_ISO_PASS generators=5 relators=141 simple_rel_sha256=",
  D972STSimpleRelSha," simple_norm_sha256=",D972STSimpleNormSha,"\n");

D972STKB:=false;;
if IsBound(D972_B4_SIMPLE_KBMAG) then D972STKB:=D972_B4_SIMPLE_KBMAG; fi;
D972STKBMaxEqns:=50000;; D972STKBMaxStates:=50000;; D972STKBMaxWdiffs:=50000;;
D972STKBMaxStored:=[1000,1000];;
if IsBound(D972_B4_SIMPLE_MAXEQNS) then D972STKBMaxEqns:=D972_B4_SIMPLE_MAXEQNS; fi;
if IsBound(D972_B4_SIMPLE_MAXSTATES) then D972STKBMaxStates:=D972_B4_SIMPLE_MAXSTATES; fi;
if IsBound(D972_B4_SIMPLE_MAXWDIFFS) then D972STKBMaxWdiffs:=D972_B4_SIMPLE_MAXWDIFFS; fi;
if IsBound(D972_B4_SIMPLE_MAXSTORED) then D972STKBMaxStored:=D972_B4_SIMPLE_MAXSTORED; fi;
D972STKBStatus:="NOT_RUN";; D972STKBBits:=[];; D972STKBConfluent:=fail;;
if D972STKB=true then
  if LoadPackage("kbmag")<>true then Error("SIMPLE transport KBMAG unavailable"); fi;
  D972STRws:=KBMAGRewritingSystem(D972STS);; SetOrderingOfKBMAGRewritingSystem(D972STRws,"shortlex");;
  D972STOpts:=OptionsRecordOfKBMAGRewritingSystem(D972STRws);;
  D972STOpts.maxeqns:=D972STKBMaxEqns;; D972STOpts.maxstates:=D972STKBMaxStates;;
  D972STOpts.maxwdiffs:=D972STKBMaxWdiffs;; D972STOpts.maxstoredlen:=D972STKBMaxStored;;
  Print("B4_SIMPLE_KBMAG_BEGIN maxeqns=",D972STKBMaxEqns," maxstates=",D972STKBMaxStates,
    " maxwdiffs=",D972STKBMaxWdiffs," maxstoredlen=",D972STKBMaxStored,"\n");
  KnuthBendix(D972STRws);; D972STKBConfluent:=IsConfluent(D972STRws);;
  if IsBound(D972STRws!.reduced) and D972STRws!.reduced=true then
    for D972STI in [1..Length(D972STSimpleNorms)] do
      D972STZ:=ReducedForm(D972STRws,D972STSignedWordObj(D972STSimpleNorms[D972STI],D972STSG));;
      Add(D972STKBBits,IsOne(D972STZ));
    od;
  fi;
  if Length(D972STKBBits)=972 and D972STKBConfluent=true then
    if Number(D972STKBBits,x->x=false)=0 then D972STKBStatus:="CONFLUENT_ALLPASS_CANDIDATE";
    else D972STKBStatus:="B4_A_SIDE_CANDIDATE_NEEDS_REPLAY"; fi;
  else D972STKBStatus:="NO_TERMINAL_KBMAG_RESULT"; fi;
  Print("B4_SIMPLE_KBMAG_DONE status=",D972STKBStatus,"\n");
fi;
D972STCheckStatus:="NOT_RUN";;
if D972STCheckMaps=true then D972STCheckStatus:="GAP_ISONE_REPLAYED"; fi;

D972STOut:=Concatenation(
  "{\"schema\":\"d972-b4-u-simplified-transport/v1\",",
  "\"status\":\"",D972STKBStatus,"\",\"source_sha256\":\"",D972STSourceSha,
  "\",\"relator_sha256\":\"",D972STRelSha,"\",\"word_artifact_sha256\":\"",
  D972STWordsSha,"\",\"roof_norm_sha256\":\"",D972STNormSha,
  "\",\"simple_generator_count\":5,\"simple_relator_count\":141,",
  "\"simple_relators_sha256\":\"",D972STSimpleRelSha,"\",\"simple_norms_sha256\":\"",
  D972STSimpleNormSha,"\",\"transport_maps_sha256\":\"",D972STMapSha,
  "\",\"simple_relators\":",D972STJson(D972STSimpleRels),
  ",\"simple_norm_words\":",D972STJson(D972STSimpleNorms),
  ",\"original_to_simple_words\":",D972STJson(D972STUToS),
  ",\"simple_to_original_words\":",D972STJson(D972STSgToU),
  ",\"roof_count\":972,\"transport_relator_checks\":\"",
  D972STCheckStatus,
  "\",\"kbmag_confluent\":",D972STJson(D972STKBConfluent),
  ",\"kbmag_roof_bits\":",D972STJson(D972STKBBits),
  ",\"proof_level\":\"TRANSPORTED_PRESENTATION_REPLAY_REQUIRED\"}");
D972STFout:=OutputTextFile(D972STOutput,false);; SetPrintFormattingStatus(D972STFout,false);
PrintTo(D972STFout,Concatenation(D972STOut,"\n"));; CloseStream(D972STFout);
Print("B4_SIMPLE_TRANSPORT_FINAL_MARKER output=",D972STOutput,
  " status=",D972STKBStatus," simple_rel_sha256=",D972STSimpleRelSha,"\n");
