#############################################################################
## d972_b4_simplified_automatic_v1.g -- AutomaticStructure audit.
##
## This is a separate lane from the nonconfluent KBMAG reduction audit.  It
## asks KBMAG's automatic-groups program to construct and axiom-check the
## automatic structure for the pinned 5/141 presentation.  ReducedForm is
## used only after a successful AutomaticStructure return; an all-empty
## ledger is still emitted as a proof candidate for independent review.
#############################################################################

if LoadPackage("json")<>true then Error("SIMPLE automatic: json unavailable"); fi;
D972SAInput:="C:/Users/81905/AppData/Local/Temp/d972_b4_u_simplified_transport_v1_receipt.json";;
D972SAOutput:=Filename(DirectoryTemporary(),"d972_b4_simplified_automatic_v1.json");;
if IsBound(D972_B4_SIMPLE_AUTOMATIC_INPUT) then D972SAInput:=D972_B4_SIMPLE_AUTOMATIC_INPUT; fi;
if IsBound(D972_B4_SIMPLE_AUTOMATIC_OUTPUT) then D972SAOutput:=D972_B4_SIMPLE_AUTOMATIC_OUTPUT; fi;
D972SAAutoPrefix:=Filename(DirectoryTemporary(),"d972_b4_simplified_automatic_v1_automaton");;
if IsBound(D972_B4_SIMPLE_AUTOMATIC_AUTOMATA_PREFIX) then D972SAAutoPrefix:=D972_B4_SIMPLE_AUTOMATIC_AUTOMATA_PREFIX; fi;
D972SATransportSha:="535d033019140e76cb9d3d7452b3e551c156f50ce74728b76bf6238d81806323";;
D972SASourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972SARelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972SANormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972SASimpleRelSha:="6d614c32365753d62477cad8803420ffa58bcca0b5d18b0e5eadaaf6bf81b35a";;
D972SASimpleNormSha:="127f029a2bafc7f8adf249b8c5f37cda594b105d3e1b567ba00400771cdca63e";;
D972SAJoin:=function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1]; for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972SAJson:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if x=true then return "true"; fi; if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("SIMPLE automatic JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972SAJson(x[i]));
  return Concatenation("[",D972SAJoin(p,","),"]");
end;;
D972SASignedObj:=function(w)
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
D972SASignedWordObj:=function(row,gens)
  local w,x;
  w:=One(gens[1]);
  for x in row do
    if x>0 then w:=w*gens[x]; else w:=w*gens[-x]^-1; fi;
  od;
  return w;
end;;

D972SARaw:=StringFile(D972SAInput);;
if D972SARaw=fail or HexSHA256(D972SARaw)<>D972SATransportSha then
  Error("SIMPLE automatic transport SHA drift");
fi;
D972SAObj:=JsonStringToGap(D972SARaw);;
if D972SAObj.schema<>"d972-b4-u-simplified-transport/v1" or
   D972SAObj.source_sha256<>D972SASourceSha or D972SAObj.relator_sha256<>D972SARelSha or
   D972SAObj.roof_norm_sha256<>D972SANormSha or D972SAObj.simple_relators_sha256<>D972SASimpleRelSha or
   D972SAObj.simple_norms_sha256<>D972SASimpleNormSha or
   Length(D972SAObj.simple_relators)<>141 or Length(D972SAObj.simple_norm_words)<>972 then
  Error("SIMPLE automatic transport gate failed");
fi;
Print("B4_SIMPLE_AUTOMATIC_INPUT_PASS transport_sha256=",D972SATransportSha,
  " simple_rel_sha256=",D972SASimpleRelSha," simple_norm_sha256=",D972SASimpleNormSha," norms=972\n");
D972SAF:=FreeGroup(5);; D972SAG:=GeneratorsOfGroup(D972SAF);;
D972SARels:=List(D972SAObj.simple_relators,w->D972SASignedWordObj(w,D972SAG));;
D972SAS:=D972SAF/D972SARels;; D972SASG:=GeneratorsOfGroup(D972SAS);;
D972SANorms:=D972SAObj.simple_norm_words;;
if LoadPackage("kbmag")<>true then Error("SIMPLE automatic kbmag unavailable"); fi;
D972SARws:=KBMAGRewritingSystem(D972SAS);; SetOrderingOfKBMAGRewritingSystem(D972SARws,"shortlex");;
D972SAOpts:=OptionsRecordOfKBMAGRewritingSystem(D972SARws);;
D972SAOpts.maxeqns:=250000;; D972SAOpts.maxstates:=250000;; D972SAOpts.maxwdiffs:=250000;;
D972SAOpts.maxstoredlen:=[4000,4000];;
Print("B4_SIMPLE_AUTOMATIC_BEGIN large=true filestore=true diff1=false\n");
D972SAAutoResult:=AutomaticStructure(D972SARws,true,true,false);;
D972SAAutoSuccess:=(D972SAAutoResult=true);;
D972SAConfluent:=IsConfluent(D972SARws);;
D972SAExpectedSize:=111577100832;;
D972SAComputeSize:=true;;
if IsBound(D972_B4_SIMPLE_AUTOMATIC_COMPUTE_SIZE) then
  D972SAComputeSize:=D972_B4_SIMPLE_AUTOMATIC_COMPUTE_SIZE;
fi;
D972SASizeStatus:="NOT_RUN";; D972SASizeValue:="not_computed";;
if D972SAAutoSuccess and D972SAComputeSize=true then
  D972SASizeRaw:=Size(D972SARws);;
  D972SASizeStatus:="COMPUTED";;
  if IsInt(D972SASizeRaw) then
    D972SASizeValue:=D972SASizeRaw;
  elif D972SASizeRaw=fail then
    D972SASizeValue:="unknown";
  else
    D972SASizeValue:="infinity";
  fi;
elif D972SAAutoSuccess then
  D972SASizeStatus:="SKIPPED";;
  D972SASizeValue:="not_computed";
fi;
D972SASizeMatches:=(D972SASizeStatus="COMPUTED" and IsInt(D972SASizeValue) and
  D972SASizeValue=D972SAExpectedSize);;
D972SAPkgInfo:=PackageInfo("kbmag");; D972SAKBVersion:="unknown";;
if Length(D972SAPkgInfo)>0 and IsBound(D972SAPkgInfo[1].Version) then D972SAKBVersion:=D972SAPkgInfo[1].Version; fi;
D972SAAutomatonNames:=["wa","diff1","diff2"];;
D972SAAutomatonBindings:=["D972SAWA","D972SADiff1","D972SADiff2"];;
D972SAAutomatonStates:=[];; D972SAAutomatonSha:=[];;
D972SAAutomatonPaths:=[];;
if D972SAAutoSuccess then
  D972SAFsaList:=[WordAcceptor(D972SARws),FirstWordDifferenceAutomaton(D972SARws),SecondWordDifferenceAutomaton(D972SARws)];;
  if IsBound(D972SARws!.reductionFSA) then
    Add(D972SAAutomatonNames,"reduction"); Add(D972SAAutomatonBindings,"D972SAReduction");
    Add(D972SAFsaList,D972SARws!.reductionFSA);
  fi;
  for D972SAI in [1..Length(D972SAFsaList)] do
    D972SAPath:=Concatenation(D972SAAutoPrefix,"_",D972SAAutomatonNames[D972SAI],".fsa");;
    WriteFSA(D972SAFsaList[D972SAI],D972SAAutomatonBindings[D972SAI],D972SAPath,";");;
    D972SARawFsa:=StringFile(D972SAPath);;
    Add(D972SAAutomatonPaths,D972SAPath); Add(D972SAAutomatonStates,NumberOfStatesFSA(D972SAFsaList[D972SAI]));
    Add(D972SAAutomatonSha,HexSHA256(D972SARawFsa));
  od;
fi;
D972SAReduced:=[];; D972SABits:=[];;
if D972SAAutoSuccess then
  for D972SAI in [1..Length(D972SANorms)] do
    D972SAZ:=ReducedForm(D972SARws,D972SASignedWordObj(D972SANorms[D972SAI],D972SAG));;
    D972SARow:=D972SASignedObj(D972SAZ);;
    Add(D972SAReduced,D972SARow); Add(D972SABits,Length(D972SARow)=0);
  od;
fi;
D972SAEmpty:=Number(D972SABits,x->x=true);; D972SAMinNonzero:=-1;;
D972SANonzero:=List([1..Length(D972SAReduced)],i->Length(D972SAReduced[i]));;
D972SANonzero:=Filtered(D972SANonzero,x->x>0);;
if Length(D972SANonzero)>0 then D972SAMinNonzero:=Minimum(D972SANonzero); fi;
D972SAStatus:="AUTOMATIC_STRUCTURE_FAILED";;
if D972SAAutoSuccess then
  if D972SAEmpty=972 and D972SASizeStatus="COMPUTED" then D972SAStatus:="B4_B_CANDIDATE_PENDING_REPLAY";
  elif D972SAEmpty=972 then D972SAStatus:="AUTOMATIC_ALL_EMPTY_SIZE_NOT_COMPUTED";
  else D972SAStatus:="AUTOMATIC_NONZERO_REDUCED_WORDS"; fi;
fi;
Print("B4_SIMPLE_AUTOMATIC_DONE success=",D972SAAutoSuccess," confluent=",D972SAConfluent,
  " size_status=",D972SASizeStatus," size=",D972SASizeValue," empty=",D972SAEmpty,
  "/972 min_nonzero=",D972SAMinNonzero," status=",D972SAStatus,"\n");
D972SAOut:=Concatenation(
  "{\"schema\":\"d972-b4-simplified-automatic/v1\",\"status\":\"",D972SAStatus,
  "\",\"transport_receipt_sha256\":\"",D972SATransportSha,"\",\"source_sha256\":\"",D972SASourceSha,
  "\",\"relator_sha256\":\"",D972SARelSha,"\",\"roof_norm_sha256\":\"",D972SANormSha,
  "\",\"simple_relators_sha256\":\"",D972SASimpleRelSha,"\",\"simple_norms_sha256\":\"",D972SASimpleNormSha,
  "\",\"kbmag_package_version\":\"",D972SAKBVersion,
  "\",\"rws_size_status\":\"",D972SASizeStatus,"\",\"rws_size\":",D972SAJson(D972SASizeValue),
  ",\"expected_sq_order\":",String(D972SAExpectedSize),
  ",\"rws_size_matches_expected\":",D972SAJson(D972SASizeMatches),
  ",\"norm_count\":972,\"automatic_success\":",D972SAJson(D972SAAutoSuccess),
  ",\"automatic_confluent\":",D972SAJson(D972SAConfluent),",\"automatic_axiom_checked\":",D972SAJson(D972SAAutoSuccess),
  ",\"automaton_names\":",D972SAJson(D972SAAutomatonNames),",\"automaton_bindings\":",D972SAJson(D972SAAutomatonBindings),",\"automaton_states\":",D972SAJson(D972SAAutomatonStates),
  ",\"automaton_sha256\":",D972SAJson(D972SAAutomatonSha),",\"automaton_paths\":",D972SAJson(D972SAAutomatonPaths),
  ",\"empty_count\":",String(D972SAEmpty),
  ",\"min_nonzero_length\":",String(D972SAMinNonzero),",\"reduced_norm_words_sha256\":\"",
  HexSHA256(D972SAJson(D972SAReduced)),"\",\"reduced_norm_words\":",D972SAJson(D972SAReduced),
  ",\"proof_level\":\"AUTOMATIC_AXIOM_CHECK_CANDIDATE\"}");
D972SAFout:=OutputTextFile(D972SAOutput,false);; SetPrintFormattingStatus(D972SAFout,false);
PrintTo(D972SAFout,Concatenation(D972SAOut,"\n"));; CloseStream(D972SAFout);
Print("B4_SIMPLE_AUTOMATIC_FINAL_MARKER output=",D972SAOutput," status=",D972SAStatus,
  " size_status=",D972SASizeStatus," size=",D972SASizeValue,
  " empty=",D972SAEmpty,"/972 min_nonzero=",D972SAMinNonzero,"\n");
