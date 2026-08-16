#############################################################################
## d972_b4_original_automatic_v1.g -- direct 6/158 AutomaticStructure lane.
##
## This intentionally does not use IsomorphismSimplifiedFpGroup or the
## 5-generator transport.  It reads the pinned canonical source and word
## artifact, constructs the six-generator U presentation directly, forms all
## 972 exact rho^4(f)...f words, and asks KBMAG to axiom-check an automatic
## structure.  An all-empty result is a replay candidate only.
#############################################################################

if LoadPackage("json")<>true then Error("ORIGINAL automatic: json unavailable"); fi;
D972OAInput:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972OAWords:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972OAOutput:=Filename(DirectoryTemporary(),"d972_b4_original_automatic_v1.json");;
D972OAPrefix:=Filename(DirectoryTemporary(),"d972_b4_original_automatic_v1_automaton");;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_INPUT) then D972OAInput:=D972_B4_ORIGINAL_AUTOMATIC_INPUT; fi;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_WORDS) then D972OAWords:=D972_B4_ORIGINAL_AUTOMATIC_WORDS; fi;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_OUTPUT) then D972OAOutput:=D972_B4_ORIGINAL_AUTOMATIC_OUTPUT; fi;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_AUTOMATA_PREFIX) then D972OAPrefix:=D972_B4_ORIGINAL_AUTOMATIC_AUTOMATA_PREFIX; fi;
D972OAPrecheck:=0;;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_PRECHECK) then D972OAPrecheck:=D972_B4_ORIGINAL_AUTOMATIC_PRECHECK; fi;
D972OASelftest:=0;;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_SELFTEST) then D972OASelftest:=D972_B4_ORIGINAL_AUTOMATIC_SELFTEST; fi;
if not IsInt(D972OAPrecheck) or (D972OAPrecheck<>0 and D972OAPrecheck<>1) or
   not IsInt(D972OASelftest) or (D972OASelftest<>0 and D972OASelftest<>1) then
  Error("ORIGINAL automatic precheck/selftest flag drift");
fi;
if D972OASelftest=1 then D972OAPrecheck:=1; fi;
D972OASourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972OAWordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972OARelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972OARhoSha:="23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed";;
D972OARoofSha:="3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8";;
D972OANormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972OATargetSha:="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972OATupleSha:="32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91";;
D972OAExpectedSize:=111577100832;;
D972OAJoin:=function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1]; for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972OAJson:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if x=true then return "true"; fi; if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("ORIGINAL automatic JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972OAJson(x[i]));
  return Concatenation("[",D972OAJoin(p,","),"]");
end;;
D972OAFR:=function(row)
  local out,x,n;
  out:=[];
  for x in row do n:=Length(out);
    if n>0 and out[n]=-x then Remove(out,n); else Add(out,x); fi;
  od;
  return out;
end;;
D972OARhoWord:=function(w,rho)
  local out,x,img;
  out:=[];
  for x in w do
    img:=rho[AbsInt(x)];
    if x<0 then img:=List(Reversed(img),y->-y); fi;
    out:=Concatenation(out,img);
  od;
  return D972OAFR(out);
end;;
D972OANormF6:=function(row,rho)
  local j,x,v,orbit,z,t;
  j:=[];
  for x in row do
    if AbsInt(x)=1 then Add(j,SignInt(x)*1);
    elif AbsInt(x)=2 then Add(j,SignInt(x)*4);
    else Error("ORIGINAL automatic F2 alphabet drift"); fi;
  od;
  j:=D972OAFR(j);; v:=j;; orbit:=[];
  for t in [1..5] do Add(orbit,v); v:=D972OARhoWord(v,rho); od;
  z:=[];
  for t in Reversed([1..5]) do z:=D972OAFR(Concatenation(z,orbit[t])); od;
  return z;
end;;
D972OASignedObj:=function(w)
  local e,o,i,g,n,j;
  e:=ExtRepOfObj(w);; o:=[];; i:=1;
  while i<=Length(e) do
    g:=e[i];; n:=e[i+1];;
    if n>0 then for j in [1..n] do Add(o,g); od;
    else for j in [1..-n] do Add(o,-g); od; fi;
    i:=i+2;
  od;
  return o;
end;;
D972OASignedWordObj:=function(row,gens)
  local w,x;
  w:=One(gens[1]);
  for x in row do if x>0 then w:=w*gens[x]; else w:=w*gens[-x]^-1; fi; od;
  return w;
end;;

D972OARaw:=StringFile(D972OAInput);;
if D972OARaw=fail or HexSHA256(D972OARaw)<>D972OASourceSha then Error("ORIGINAL source SHA drift"); fi;
D972OAObj:=JsonStringToGap(D972OARaw);;
D972OARho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;
if D972OAObj.schema<>"d972-b4-p2-magnus-input/v2" or
   Length(D972OAObj.all_relators)<>158 or Length(D972OAObj.roof_words)<>972 or
   D972OAObj.rho_words<>D972OARho or D972OAObj.rho_words_source<>"universal_v2_canonical" or
   D972OAObj.all_relators_sha256<>D972OARelSha or D972OAObj.roof_words_sha256<>D972OARoofSha then
  Error("ORIGINAL source canonical gate failed");
fi;
D972OAWordsRaw:=StringFile(D972OAWords);;
if D972OAWordsRaw=fail or HexSHA256(D972OAWordsRaw)<>D972OAWordsSha then Error("ORIGINAL word SHA drift"); fi;
D972OAWordsObj:=JsonStringToGap(D972OAWordsRaw);;
if D972OAWordsObj.schema<>"d972-b4-word-key-artifact/v1" or D972OAWordsObj.count<>972 or
   D972OAWordsObj.source_target_key_digest<>D972OATargetSha or
   D972OAWordsObj.frozen_tuple_sha256<>D972OATupleSha then Error("ORIGINAL word artifact gate failed"); fi;
D972OARoofRows:=[];;
for D972OARow in D972OAWordsObj.rows do
  D972OAWord:=D972OARow[3];; if D972OAWord="" then D972OAWord:=[]; fi;
  Add(D972OARoofRows,D972OAWord);
od;
if D972OARoofRows<>D972OAObj.roof_words or
   HexSHA256(D972OAJson(D972OARoofRows))<>D972OARoofSha then Error("ORIGINAL roof artifact mismatch"); fi;
D972OANormRows:=List(D972OARoofRows,w->D972OANormF6(w,D972OARho));;
if HexSHA256(D972OAJson(D972OANormRows))<>D972OANormSha then Error("ORIGINAL norm digest drift"); fi;
Print("B4_ORIGINAL_AUTOMATIC_INPUT_PASS source_sha256=",D972OASourceSha,
  " relators=158 norms=972 norm_sha256=",D972OANormSha,"\n");
if D972OAPrecheck=1 then
  D972OAPreOut:=Concatenation(
    "{\"schema\":\"d972-b4-original-automatic-precheck/v1\",\"status\":\"INPUT_PRECHECK_PASS\",",
    "\"source_sha256\":\"",D972OASourceSha,"\",\"word_artifact_sha256\":\"",D972OAWordsSha,
    "\",\"relator_sha256\":\"",D972OARelSha,"\",\"rho_words_sha256\":\"",D972OARhoSha,
    "\",\"roof_words_sha256\":\"",D972OARoofSha,"\",\"roof_norm_sha256\":\"",D972OANormSha,
    "\",\"relator_count\":158,\"norm_count\":972,\"automatic_invoked\":false,\"selftest\":",
    D972OAJson(D972OASelftest=1),"}");
  D972OAPreF:=OutputTextFile(D972OAOutput,false);; SetPrintFormattingStatus(D972OAPreF,false);
  PrintTo(D972OAPreF,Concatenation(D972OAPreOut,"\n"));; CloseStream(D972OAPreF);
  Print("B4_ORIGINAL_AUTOMATIC_PRECHECK_FINAL_MARKER output=",D972OAOutput," status=INPUT_PRECHECK_PASS\n");
else

D972OAF:=FreeGroup(6);; D972OAG:=GeneratorsOfGroup(D972OAF);;
D972OARels:=List(D972OAObj.all_relators,w->D972OASignedWordObj(w,D972OAG));;
D972OAU:=D972OAF/D972OARels;; D972OAUG:=GeneratorsOfGroup(D972OAU);;
if LoadPackage("kbmag")<>true then Error("ORIGINAL automatic kbmag unavailable"); fi;
D972OARws:=KBMAGRewritingSystem(D972OAU);; SetOrderingOfKBMAGRewritingSystem(D972OARws,"shortlex");;
D972OAOpts:=OptionsRecordOfKBMAGRewritingSystem(D972OARws);;
D972OAOpts.maxeqns:=250000;; D972OAOpts.maxstates:=250000;; D972OAOpts.maxwdiffs:=250000;;
D972OAOpts.maxstoredlen:=[4000,4000];;
Print("B4_ORIGINAL_AUTOMATIC_BEGIN generators=6 relators=158 large=true filestore=true diff1=false\n");
D972OAResult:=AutomaticStructure(D972OARws,true,true,false);;
D972OASuccess:=(D972OAResult=true);; D972OAConfluent:=IsConfluent(D972OARws);;
D972OASizeStatus:="NOT_RUN";; D972OASizeValue:="not_computed";; D972OAComputeSize:=true;;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_COMPUTE_SIZE) then D972OAComputeSize:=D972_B4_ORIGINAL_AUTOMATIC_COMPUTE_SIZE; fi;
if D972OASuccess and D972OAComputeSize=true then
  D972OASizeRaw:=Size(D972OARws);; D972OASizeStatus:="COMPUTED";;
  if IsInt(D972OASizeRaw) then D972OASizeValue:=D972OASizeRaw;
  elif D972OASizeRaw=fail then D972OASizeValue:="unknown";
  else D972OASizeValue:="infinity"; fi;
elif D972OASuccess then D972OASizeStatus:="SKIPPED";; fi;
D972OASizeMatches:=(D972OASizeStatus="COMPUTED" and IsInt(D972OASizeValue) and D972OASizeValue=D972OAExpectedSize);;
D972OAPkgInfo:=PackageInfo("kbmag");; D972OAKBVersion:="unknown";;
if Length(D972OAPkgInfo)>0 and IsBound(D972OAPkgInfo[1].Version) then D972OAKBVersion:=D972OAPkgInfo[1].Version; fi;
D972OANames:=["wa","diff1","diff2"];; D972OABindings:=["D972OAWA","D972OADiff1","D972OADiff2"];;
D972OAStates:=[];; D972OAShas:=[];; D972OAPaths:=[];;
if D972OASuccess then
  D972OAFsa:=[WordAcceptor(D972OARws),FirstWordDifferenceAutomaton(D972OARws),SecondWordDifferenceAutomaton(D972OARws)];;
  if IsBound(D972OARws!.reductionFSA) then Add(D972OANames,"reduction"); Add(D972OABindings,"D972OAReduction"); Add(D972OAFsa,D972OARws!.reductionFSA); fi;
  for D972OAI in [1..Length(D972OAFsa)] do
    D972OAPath:=Concatenation(D972OAPrefix,"_",D972OANames[D972OAI],".fsa");;
    WriteFSA(D972OAFsa[D972OAI],D972OABindings[D972OAI],D972OAPath,";");;
    Add(D972OAPaths,D972OAPath); Add(D972OAStates,NumberOfStatesFSA(D972OAFsa[D972OAI])); Add(D972OAShas,HexSHA256(StringFile(D972OAPath)));
  od;
fi;
D972OAReduced:=[];; D972OABits:=[];;
if D972OASuccess then
  for D972OAI in [1..Length(D972OANormRows)] do
    D972OAZ:=ReducedForm(D972OARws,D972OASignedWordObj(D972OANormRows[D972OAI],D972OAG));;
    D972OARow:=D972OASignedObj(D972OAZ);; Add(D972OAReduced,D972OARow); Add(D972OABits,Length(D972OARow)=0);
  od;
fi;
D972OAEmpty:=Number(D972OABits,x->x=true);; D972OAMin:=-1;; D972OANonzero:=Filtered(List(D972OAReduced,Length),x->x>0);;
if Length(D972OANonzero)>0 then D972OAMin:=Minimum(D972OANonzero); fi;
D972OAStatus:="AUTOMATIC_STRUCTURE_FAILED";;
if D972OASuccess then
  if D972OAEmpty=972 and D972OASizeStatus="COMPUTED" then D972OAStatus:="B4_B_CANDIDATE_PENDING_REPLAY";
  elif D972OAEmpty=972 then D972OAStatus:="AUTOMATIC_ALL_EMPTY_SIZE_NOT_COMPUTED";
  else D972OAStatus:="AUTOMATIC_NONZERO_REDUCED_WORDS"; fi;
fi;
Print("B4_ORIGINAL_AUTOMATIC_DONE success=",D972OASuccess," confluent=",D972OAConfluent,
  " size_status=",D972OASizeStatus," size=",D972OASizeValue," empty=",D972OAEmpty,
  "/972 min_nonzero=",D972OAMin," status=",D972OAStatus,"\n");
D972OAOut:=Concatenation(
  "{\"schema\":\"d972-b4-original-automatic/v1\",\"status\":\"",D972OAStatus,
  "\",\"source_sha256\":\"",D972OASourceSha,"\",\"word_artifact_sha256\":\"",D972OAWordsSha,
  "\",\"relator_sha256\":\"",D972OARelSha,"\",\"rho_words_sha256\":\"",D972OARhoSha,
  "\",\"roof_words_sha256\":\"",D972OARoofSha,"\",\"roof_norm_sha256\":\"",D972OANormSha,
  "\",\"kbmag_package_version\":\"",D972OAKBVersion,"\",\"rws_size_status\":\"",D972OASizeStatus,
  "\",\"rws_size\":",D972OAJson(D972OASizeValue),",\"expected_sq_order\":",String(D972OAExpectedSize),
  ",\"rws_size_matches_expected\":",D972OAJson(D972OASizeMatches),
  ",\"norm_count\":972,\"automatic_success\":",D972OAJson(D972OASuccess),",\"automatic_confluent\":",D972OAJson(D972OAConfluent),
  ",\"automatic_axiom_checked\":",D972OAJson(D972OASuccess),",\"automaton_names\":",D972OAJson(D972OANames),
  ",\"automaton_bindings\":",D972OAJson(D972OABindings),",\"automaton_states\":",D972OAJson(D972OAStates),
  ",\"automaton_sha256\":",D972OAJson(D972OAShas),",\"automaton_paths\":",D972OAJson(D972OAPaths),
  ",\"empty_count\":",String(D972OAEmpty),",\"min_nonzero_length\":",String(D972OAMin),
  ",\"reduced_norm_words_sha256\":\"",HexSHA256(D972OAJson(D972OAReduced)),"\",\"reduced_norm_words\":",D972OAJson(D972OAReduced),
  ",\"proof_level\":\"DIRECT_AUTOMATIC_AXIOM_CHECK_CANDIDATE\"}");
D972OAFout:=OutputTextFile(D972OAOutput,false);; SetPrintFormattingStatus(D972OAFout,false); PrintTo(D972OAFout,Concatenation(D972OAOut,"\n"));; CloseStream(D972OAFout);
Print("B4_ORIGINAL_AUTOMATIC_FINAL_MARKER output=",D972OAOutput," status=",D972OAStatus,
  " size_status=",D972OASizeStatus," empty=",D972OAEmpty,"/972\n");
fi;
