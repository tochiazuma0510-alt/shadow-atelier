#############################################################################
## d972_b4_simplified_orderings_v1.g -- numeric KBMAG ordering/permutation
## scanner.  The two selectors are numeric so workflow quote stripping cannot
## silently change the target:
##   D972_B4_SIMPLE_ORDERING_INDEX = 1..8
##   D972_B4_SIMPLE_PERM_INDEX     = 1..10
## A finite all-pass is UNKNOWN; only a replayable defect can be B4-A.
#############################################################################

if LoadPackage("json")<>true then Error("SIMPLE orderings: json unavailable"); fi;
D972SOInput:="C:/Users/81905/AppData/Local/Temp/d972_b4_u_simplified_transport_v1_receipt.json";;
D972SOOutput:=Filename(DirectoryTemporary(),"d972_b4_simplified_orderings_v1.json");;
if IsBound(D972_B4_SIMPLE_ORDERINGS_INPUT) then D972SOInput:=D972_B4_SIMPLE_ORDERINGS_INPUT; fi;
if IsBound(D972_B4_SIMPLE_ORDERINGS_OUTPUT) then D972SOOutput:=D972_B4_SIMPLE_ORDERINGS_OUTPUT; fi;
D972SOOrderIndex:=1;; D972SOPermIndex:=1;;
if IsBound(D972_B4_SIMPLE_ORDERING_INDEX) then D972SOOrderIndex:=D972_B4_SIMPLE_ORDERING_INDEX; fi;
if IsBound(D972_B4_SIMPLE_PERM_INDEX) then D972SOPermIndex:=D972_B4_SIMPLE_PERM_INDEX; fi;
if not IsInt(D972SOOrderIndex) or D972SOOrderIndex<1 or D972SOOrderIndex>8 then Error("SIMPLE ordering index drift"); fi;
if not IsInt(D972SOPermIndex) or D972SOPermIndex<1 or D972SOPermIndex>10 then Error("SIMPLE permutation index drift"); fi;
D972SOTransportSha:="535d033019140e76cb9d3d7452b3e551c156f50ce74728b76bf6238d81806323";;
D972SOSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972SORelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972SONormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972SOSimpleRelSha:="6d614c32365753d62477cad8803420ffa58bcca0b5d18b0e5eadaaf6bf81b35a";;
D972SOSimpleNormSha:="127f029a2bafc7f8adf249b8c5f37cda594b105d3e1b567ba00400771cdca63e";;
D972SOJoin:=function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1]; for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972SOJson:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if x=true then return "true"; fi; if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("SIMPLE orderings JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972SOJson(x[i]));
  return Concatenation("[",D972SOJoin(p,","),"]");
end;;
D972SOSignedObj:=function(w)
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
D972SOSignedWordObj:=function(row,gens)
  local w,x;
  w:=One(gens[1]);
  for x in row do
    if x>0 then w:=w*gens[x]; else w:=w*gens[-x]^-1; fi;
  od;
  return w;
end;;

## Permutations act on the five positive generator labels.  The alphabet
## permutation below preserves the current signed-letter pattern and moves
## each old alphabet position to the position of its relabeled letter.
D972SOPerms:=[
  [1,2,3,4,5],[2,1,3,4,5],[3,2,1,4,5],[4,2,3,1,5],[5,2,3,4,1],
  [2,3,4,5,1],[5,1,2,3,4],[2,1,4,3,5],[3,4,5,1,2],[5,4,3,2,1]
];;
D972SOOrderNames:=["shortlex","recursive","rt_recursive","wreathprod",
  "wreathprod_reverse","wtlex","wtlex_reverse","recursive_reverse"];;
D972SOOrderName:=D972SOOrderNames[D972SOOrderIndex];;
D972SOPerm:=D972SOPerms[D972SOPermIndex];;

D972SORaw:=StringFile(D972SOInput);;
if D972SORaw=fail or HexSHA256(D972SORaw)<>D972SOTransportSha then Error("SIMPLE orderings transport SHA drift"); fi;
D972SOObj:=JsonStringToGap(D972SORaw);;
if D972SOObj.schema<>"d972-b4-u-simplified-transport/v1" or
   D972SOObj.source_sha256<>D972SOSourceSha or D972SOObj.relator_sha256<>D972SORelSha or
   D972SOObj.roof_norm_sha256<>D972SONormSha or D972SOObj.simple_relators_sha256<>D972SOSimpleRelSha or
   D972SOObj.simple_norms_sha256<>D972SOSimpleNormSha or
   Length(D972SOObj.simple_relators)<>141 or Length(D972SOObj.simple_norm_words)<>972 then
  Error("SIMPLE orderings transport gate failed");
fi;
Print("B4_SIMPLE_ORDERINGS_INPUT_PASS order_index=",D972SOOrderIndex," order=",D972SOOrderName,
  " perm_index=",D972SOPermIndex," norms=972\n");

D972SOF:=FreeGroup(5);; D972SOG:=GeneratorsOfGroup(D972SOF);;
D972SORels:=List(D972SOObj.simple_relators,w->D972SOSignedWordObj(w,D972SOG));;
D972SOS:=D972SOF/D972SORels;; D972SOSG:=GeneratorsOfGroup(D972SOS);;
D972SONorms:=D972SOObj.simple_norm_words;;
D972SORws:=KBMAGRewritingSystem(D972SOS);;
D972SOAlpha:=Alphabet(D972SORws);; D972SOAlphaSigned:=List(D972SOAlpha,D972SOSignedObj);;
D972SOTarget:=List(D972SOAlphaSigned,x->SignInt(x)*D972SOPerm[AbsInt(x)]);;
D972SOPList:=List(D972SOAlphaSigned,x->Position(D972SOTarget,x));;
if Length(Set(D972SOPList))<>Length(D972SOPList) then Error("SIMPLE alphabet permutation drift"); fi;
ReorderAlphabetOfKBMAGRewritingSystem(D972SORws,PermList(D972SOPList));;
if D972SOOrderIndex=1 then
  SetOrderingOfKBMAGRewritingSystem(D972SORws,"shortlex");
elif D972SOOrderIndex=2 then
  SetOrderingOfKBMAGRewritingSystem(D972SORws,"recursive");
elif D972SOOrderIndex=3 then
  SetOrderingOfKBMAGRewritingSystem(D972SORws,"rt_recursive");
elif D972SOOrderIndex=4 then
  SetOrderingOfKBMAGRewritingSystem(D972SORws,"wreathprod",List(Alphabet(D972SORws),x->AbsInt(D972SOSignedObj(x))));
elif D972SOOrderIndex=5 then
  SetOrderingOfKBMAGRewritingSystem(D972SORws,"wreathprod",List(Alphabet(D972SORws),x->6-AbsInt(D972SOSignedObj(x))));
elif D972SOOrderIndex=6 then
  SetOrderingOfKBMAGRewritingSystem(D972SORws,"wtlex",List(Alphabet(D972SORws),x->AbsInt(D972SOSignedObj(x))));
elif D972SOOrderIndex=7 then
  SetOrderingOfKBMAGRewritingSystem(D972SORws,"wtlex",List(Alphabet(D972SORws),x->6-AbsInt(D972SOSignedObj(x))));
else
  SetOrderingOfKBMAGRewritingSystem(D972SORws,"recursive");
fi;
D972SOOpts:=OptionsRecordOfKBMAGRewritingSystem(D972SORws);;
D972SOOpts.maxeqns:=250000;; D972SOOpts.maxstates:=250000;; D972SOOpts.maxwdiffs:=250000;;
D972SOOpts.maxstoredlen:=[4000,4000];;
Print("B4_SIMPLE_ORDERINGS_BEGIN order=",D972SOOrderName," permutation=",D972SOPerm,
  " alphabet=",List(Alphabet(D972SORws),D972SOSignedObj),"\n");
D972SOKBResult:=KnuthBendix(D972SORws);;
D972SONormalStop:=(D972SOKBResult=true or D972SOKBResult=false);;
D972SOConfluent:=IsConfluent(D972SORws);; D972SOReduced:=[];; D972SOBits:=[];;
if D972SONormalStop then
  D972SORA:=ReductionAutomaton(D972SORws);;
  for D972SOI in [1..Length(D972SONorms)] do
    D972SOZ:=ReducedForm(D972SORws,D972SOSignedWordObj(D972SONorms[D972SOI],D972SOG));;
    D972SORow:=D972SOSignedObj(D972SOZ);; Add(D972SOReduced,D972SORow); Add(D972SOBits,Length(D972SORow)=0);
  od;
fi;
D972SOEmpty:=Number(D972SOBits,x->x=true);; D972SOStatus:="KBMAG_NOT_NORMAL_STOP";;
D972SOMinNonzero:=-1;; D972SONonzero:=List(D972SOReduced,Length);; D972SONonzero:=Filtered(D972SONonzero,x->x>0);
if Length(D972SONonzero)>0 then D972SOMinNonzero:=Minimum(D972SONonzero); fi;
if D972SONormalStop then if D972SOEmpty=972 then D972SOStatus:="ALL_EMPTY_REWRITE_CANDIDATE"; else D972SOStatus:="NONZERO_REDUCED_WORDS"; fi; fi;
Print("B4_SIMPLE_ORDERINGS_DONE normal_stop=",D972SONormalStop," confluent=",D972SOConfluent,
  " empty=",D972SOEmpty,"/972 min_nonzero=",D972SOMinNonzero," status=",D972SOStatus,"\n");
D972SOOut:=Concatenation(
  "{\"schema\":\"d972-b4-simplified-orderings/v1\",\"status\":\"",D972SOStatus,
  "\",\"transport_receipt_sha256\":\"",D972SOTransportSha,"\",\"source_sha256\":\"",D972SOSourceSha,
  "\",\"relator_sha256\":\"",D972SORelSha,"\",\"roof_norm_sha256\":\"",D972SONormSha,
  "\",\"simple_relators_sha256\":\"",D972SOSimpleRelSha,"\",\"simple_norms_sha256\":\"",D972SOSimpleNormSha,
  "\",\"ordering_index\":",String(D972SOOrderIndex),",\"ordering\":\"",D972SOOrderName,
  "\",\"permutation_index\":",String(D972SOPermIndex),",\"permutation\":",D972SOJson(D972SOPerm),
  ",\"norm_count\":972,\"kbmag_return\":",D972SOJson(D972SOKBResult),
  ",\"kbmag_normal_stop\":",D972SOJson(D972SONormalStop),",\"kbmag_confluent\":",D972SOJson(D972SOConfluent),
  ",\"empty_count\":",String(D972SOEmpty),",\"min_nonzero_length\":",String(D972SOMinNonzero),
  ",\"reduced_norm_words_sha256\":\"",HexSHA256(D972SOJson(D972SOReduced)),"\",\"reduced_norm_words\":",D972SOJson(D972SOReduced),
  ",\"proof_level\":\"ORDERING_SCAN_UNKNOWN_UNLESS_REPLAYED\"}");
D972SOFout:=OutputTextFile(D972SOOutput,false);; SetPrintFormattingStatus(D972SOFout,false); PrintTo(D972SOFout,Concatenation(D972SOOut,"\n"));; CloseStream(D972SOFout);
Print("B4_SIMPLE_ORDERINGS_FINAL_MARKER output=",D972SOOutput," status=",D972SOStatus,
  " ordering_index=",D972SOOrderIndex," permutation_index=",D972SOPermIndex," empty=",D972SOEmpty,"/972\n");
