#############################################################################
## d972_b4_simplified_reduced_v1.g -- KBMAG reduced-form audit.
##
## This lane consumes the independently transported 5-generator receipt.
## KnuthBendix is allowed to return false: the KBMAG contract still supplies
## a reduction automaton after a normal (non-aborted) halt.  Every transported
## norm is then passed to ReducedForm, regardless of IsConfluent/reduced flags.
## A nonconfluent all-empty ledger is only a candidate until rule ancestry or
## independently replayable van Kampen certificates are supplied.
#############################################################################

if LoadPackage("json")<>true then Error("SIMPLE reduced: json unavailable"); fi;

D972SRInput:="C:/Users/81905/AppData/Local/Temp/d972_b4_u_simplified_transport_v1_receipt.json";;
D972SROutput:=Filename(DirectoryTemporary(),"d972_b4_simplified_reduced_v1.json");;
if IsBound(D972_B4_SIMPLE_REDUCED_INPUT) then D972SRInput:=D972_B4_SIMPLE_REDUCED_INPUT; fi;
if IsBound(D972_B4_SIMPLE_REDUCED_OUTPUT) then D972SROutput:=D972_B4_SIMPLE_REDUCED_OUTPUT; fi;
D972SRTransportSha:="535d033019140e76cb9d3d7452b3e551c156f50ce74728b76bf6238d81806323";;
D972SRSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972SRRelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972SRNormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972SRSimpleRelSha:="6d614c32365753d62477cad8803420ffa58bcca0b5d18b0e5eadaaf6bf81b35a";;
D972SRSimpleNormSha:="127f029a2bafc7f8adf249b8c5f37cda594b105d3e1b567ba00400771cdca63e";;

D972SRJoin:=function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1]; for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972SRJson:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if x=true then return "true"; fi; if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("SIMPLE reduced JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972SRJson(x[i]));
  return Concatenation("[",D972SRJoin(p,","),"]");
end;;
D972SRSignedObj:=function(w)
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
D972SRSignedWordObj:=function(row,gens)
  local w,x;
  w:=One(gens[1]);
  for x in row do
    if x>0 then w:=w*gens[x]; else w:=w*gens[-x]^-1; fi;
  od;
  return w;
end;;
D972SRRuleWord:=function(w)
  local z;
  if IsList(w) then return w; fi;
  z:=InternalWordToExternalWordOfRewritingSystem(D972SRRws,w);
  if IsList(z) then return z; fi;
  return D972SRSignedObj(z);
end;;

D972SRRaw:=StringFile(D972SRInput);;
if D972SRRaw=fail or HexSHA256(D972SRRaw)<>D972SRTransportSha then
  Error("SIMPLE reduced transport receipt SHA drift");
fi;
D972SRObj:=JsonStringToGap(D972SRRaw);;
if D972SRObj.schema<>"d972-b4-u-simplified-transport/v1" or
   D972SRObj.source_sha256<>D972SRSourceSha or
   D972SRObj.relator_sha256<>D972SRRelSha or
   D972SRObj.roof_norm_sha256<>D972SRNormSha or
   D972SRObj.simple_generator_count<>5 or D972SRObj.simple_relator_count<>141 or
   D972SRObj.simple_relators_sha256<>D972SRSimpleRelSha or
   D972SRObj.simple_norms_sha256<>D972SRSimpleNormSha or
   Length(D972SRObj.simple_relators)<>141 or Length(D972SRObj.simple_norm_words)<>972 then
  Error("SIMPLE reduced transport gate failed");
fi;
Print("B4_SIMPLE_REDUCED_INPUT_PASS transport_sha256=",D972SRTransportSha,
  " simple_rel_sha256=",D972SRSimpleRelSha," simple_norm_sha256=",D972SRSimpleNormSha,
  " norms=972\n");

D972SRF:=FreeGroup(5);; D972SRG:=GeneratorsOfGroup(D972SRF);;
D972SRRels:=List(D972SRObj.simple_relators,w->D972SRSignedWordObj(w,D972SRG));;
D972SRS:=D972SRF/D972SRRels;; D972SRSG:=GeneratorsOfGroup(D972SRS);;
D972SRNorms:=D972SRObj.simple_norm_words;;
D972SRUnique:=Set(D972SRNorms);;
if LoadPackage("kbmag")<>true then Error("SIMPLE reduced: kbmag unavailable"); fi;
D972SRRws:=KBMAGRewritingSystem(D972SRS);;
SetOrderingOfKBMAGRewritingSystem(D972SRRws,"shortlex");;
D972SROpts:=OptionsRecordOfKBMAGRewritingSystem(D972SRRws);;
D972SRMaxEqns:=250000;; D972SRMaxStates:=250000;; D972SRMaxWdiffs:=250000;;
D972SRMaxStored:=[4000,4000];;
if IsBound(D972_B4_SIMPLE_REDUCED_MAXEQNS) then D972SRMaxEqns:=D972_B4_SIMPLE_REDUCED_MAXEQNS; fi;
if IsBound(D972_B4_SIMPLE_REDUCED_MAXSTATES) then D972SRMaxStates:=D972_B4_SIMPLE_REDUCED_MAXSTATES; fi;
if IsBound(D972_B4_SIMPLE_REDUCED_MAXWDIFFS) then D972SRMaxWdiffs:=D972_B4_SIMPLE_REDUCED_MAXWDIFFS; fi;
if IsBound(D972_B4_SIMPLE_REDUCED_MAXSTORED) then D972SRMaxStored:=D972_B4_SIMPLE_REDUCED_MAXSTORED; fi;
D972SROpts.maxeqns:=D972SRMaxEqns;; D972SROpts.maxstates:=D972SRMaxStates;;
D972SROpts.maxwdiffs:=D972SRMaxWdiffs;; D972SROpts.maxstoredlen:=D972SRMaxStored;;
Print("B4_SIMPLE_REDUCED_KBMAG_BEGIN maxeqns=",D972SRMaxEqns,
  " maxstates=",D972SRMaxStates," maxwdiffs=",D972SRMaxWdiffs,
  " maxstoredlen=",D972SRMaxStored," unique_norms=",Length(D972SRUnique),"\n");
D972SRKBResult:=KnuthBendix(D972SRRws);;
D972SRNormalStop:=(D972SRKBResult=true or D972SRKBResult=false);;
D972SRConfluent:=IsConfluent(D972SRRws);;
D972SRRules:=[];; D972SRRuleSha:="";;
if D972SRNormalStop then
  ## Rules are included as a raw GAP word ledger for later replay.  KBMAG
  ## exposes no derivation ancestry for these completed rules.
  D972SRRules:=List(Rules(D972SRRws),r->List(r,D972SRRuleWord));;
  D972SRRuleSha:=HexSHA256(D972SRJson(D972SRRules));;
fi;
D972SRReduced:=[];; D972SRBits:=[];; D972SRReducedUnique:=[];;
if D972SRNormalStop then
  ## Do not gate this on IsConfluent or the private .reduced flag: a normal
  ## nonconfluent halt still installs ReductionAutomaton/ReducedForm.
  D972SRRA:=ReductionAutomaton(D972SRRws);;
  for D972SRI in [1..Length(D972SRNorms)] do
    D972SRZ:=ReducedForm(D972SRRws,D972SRSignedWordObj(D972SRNorms[D972SRI],D972SRG));;
    D972SRRow:=D972SRSignedObj(D972SRZ);;
    Add(D972SRReduced,D972SRRow); Add(D972SRBits,Length(D972SRRow)=0);
  od;
  for D972SRI in [1..Length(D972SRUnique)] do
    D972SRZ:=ReducedForm(D972SRRws,D972SRSignedWordObj(D972SRUnique[D972SRI],D972SRG));;
    Add(D972SRReducedUnique,D972SRSignedObj(D972SRZ));
  od;
fi;
D972SREmpty:=Number(D972SRBits,x->x=true);;
D972SRNonzero:=List([1..Length(D972SRReduced)],i->Length(D972SRReduced[i]));;
D972SRNonzero:=Filtered(D972SRNonzero,x->x>0);;
D972SRMinNonzero:=-1;; if Length(D972SRNonzero)>0 then D972SRMinNonzero:=Minimum(D972SRNonzero); fi;
D972SRStatus:="KBMAG_NOT_NORMAL_STOP";;
if D972SRNormalStop then
  if D972SREmpty=972 then D972SRStatus:="ALL_EMPTY_REWRITE_CANDIDATE";
  else D972SRStatus:="NONZERO_REDUCED_WORDS"; fi;
fi;
Print("B4_SIMPLE_REDUCED_KBMAG_DONE normal_stop=",D972SRNormalStop,
  " confluent=",D972SRConfluent," empty=",D972SREmpty,"/972 min_nonzero=",D972SRMinNonzero,
  " status=",D972SRStatus," rule_count=",Length(D972SRRules),"\n");

D972SROut:=Concatenation(
  "{\"schema\":\"d972-b4-simplified-reduced/v1\",\"status\":\"",D972SRStatus,
  "\",\"transport_receipt_sha256\":\"",D972SRTransportSha,
  "\",\"source_sha256\":\"",D972SRSourceSha,"\",\"relator_sha256\":\"",D972SRRelSha,
  "\",\"roof_norm_sha256\":\"",D972SRNormSha,"\",\"simple_relators_sha256\":\"",
  D972SRSimpleRelSha,"\",\"simple_norms_sha256\":\"",D972SRSimpleNormSha,
  "\",\"simple_generator_count\":5,\"simple_relator_count\":141,\"norm_count\":972,",
  "\"unique_norm_count\":",String(Length(D972SRUnique)),
  ",\"kbmag_return\":",D972SRJson(D972SRKBResult),
  ",\"kbmag_normal_stop\":",D972SRJson(D972SRNormalStop),
  ",\"kbmag_confluent\":",D972SRJson(D972SRConfluent),
  ",\"empty_count\":",String(D972SREmpty),",\"min_nonzero_length\":",String(D972SRMinNonzero),
  ",\"reduced_norm_words_sha256\":\"",HexSHA256(D972SRJson(D972SRReduced)),
  "\",\"reduced_norm_words\":",D972SRJson(D972SRReduced),
  ",\"reduced_unique_words_sha256\":\"",HexSHA256(D972SRJson(D972SRReducedUnique)),
  "\",\"reduced_unique_words\":",D972SRJson(D972SRReducedUnique),
  ",\"rule_count\":",String(Length(D972SRRules)),",\"rules_sha256\":\"",D972SRRuleSha,
  "\",\"rules\":",D972SRJson(D972SRRules),
  ",\"proof_level\":\"KBMAG_RULES_NO_ANCESTRY_UNKNOWN\"}");
D972SRFout:=OutputTextFile(D972SROutput,false);; SetPrintFormattingStatus(D972SRFout,false);
PrintTo(D972SRFout,Concatenation(D972SROut,"\n"));; CloseStream(D972SRFout);
Print("B4_SIMPLE_REDUCED_FINAL_MARKER output=",D972SROutput," status=",D972SRStatus,
  " empty=",D972SREmpty,"/972 min_nonzero=",D972SRMinNonzero,"\n");
