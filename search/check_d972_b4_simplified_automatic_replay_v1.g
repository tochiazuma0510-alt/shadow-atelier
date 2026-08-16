#############################################################################
## Independent GAP replay of an AutomaticStructure candidate receipt.
## This checker does not Read the producer.  It loads only the pinned receipt
## and exported FSA records, rebuilds the 5/141 presentation, attaches the
## exported automata, and replays all 972 ReducedForm words.
#############################################################################

if LoadPackage("json")<>true then Error("AUTOMATIC replay: json unavailable"); fi;
D972ABInput:="C:/Users/81905/AppData/Local/Temp/d972_b4_simplified_automatic_v1.json";;
D972ABTransportInput:="C:/Users/81905/AppData/Local/Temp/d972_b4_u_simplified_transport_v1_receipt.json";;
D972ABOutput:=Filename(DirectoryTemporary(),"d972_b4_simplified_automatic_replay_v1.json");;
if IsBound(D972_B4_SIMPLE_AUTOMATIC_REPLAY_INPUT) then D972ABInput:=D972_B4_SIMPLE_AUTOMATIC_REPLAY_INPUT; fi;
if IsBound(D972_B4_SIMPLE_AUTOMATIC_REPLAY_TRANSPORT) then D972ABTransportInput:=D972_B4_SIMPLE_AUTOMATIC_REPLAY_TRANSPORT; fi;
if IsBound(D972_B4_SIMPLE_AUTOMATIC_REPLAY_OUTPUT) then D972ABOutput:=D972_B4_SIMPLE_AUTOMATIC_REPLAY_OUTPUT; fi;
D972ABTransportSha:="535d033019140e76cb9d3d7452b3e551c156f50ce74728b76bf6238d81806323";;
D972ABSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972ABRelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972ABNormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972ABSimpleRelSha:="6d614c32365753d62477cad8803420ffa58bcca0b5d18b0e5eadaaf6bf81b35a";;
D972ABSimpleNormSha:="127f029a2bafc7f8adf249b8c5f37cda594b105d3e1b567ba00400771cdca63e";;
D972ABExpectedSize:=111577100832;;
D972ABJoin:=function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1]; for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972ABJson:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if x=true then return "true"; fi; if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("AUTOMATIC replay JSON drift"); fi;
  p:=List([1..Length(x)],i->D972ABJson(x[i]));
  return Concatenation("[",D972ABJoin(p,","),"]");
end;;
D972ABSignedObj:=function(w)
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
D972ABSignedWordObj:=function(row,gens)
  local w,x;
  w:=One(gens[1]);
  for x in row do
    if x>0 then w:=w*gens[x]; else w:=w*gens[-x]^-1; fi;
  od;
  return w;
end;;

D972ABRaw:=StringFile(D972ABInput);;
if D972ABRaw=fail then Error("AUTOMATIC replay receipt missing"); fi;
D972ABObj:=JsonStringToGap(D972ABRaw);;
if D972ABObj.schema<>"d972-b4-simplified-automatic/v1" or
   D972ABObj.status<>"B4_B_CANDIDATE_PENDING_REPLAY" or
   D972ABObj.automatic_success<>true or D972ABObj.automatic_axiom_checked<>true or
   D972ABObj.transport_receipt_sha256<>D972ABTransportSha or
   D972ABObj.source_sha256<>D972ABSourceSha or D972ABObj.relator_sha256<>D972ABRelSha or
   D972ABObj.roof_norm_sha256<>D972ABNormSha or D972ABObj.simple_relators_sha256<>D972ABSimpleRelSha or
   D972ABObj.simple_norms_sha256<>D972ABSimpleNormSha or
   D972ABObj.rws_size_status<>"COMPUTED" or D972ABObj.expected_sq_order<>D972ABExpectedSize or
   D972ABObj.rws_size_matches_expected<> (IsInt(D972ABObj.rws_size) and D972ABObj.rws_size=D972ABExpectedSize) or
   Length(D972ABObj.reduced_norm_words)<>972 then
  Error("AUTOMATIC replay receipt gate failed");
fi;
D972ABTransportRaw:=StringFile(D972ABTransportInput);;
if D972ABTransportRaw=fail or HexSHA256(D972ABTransportRaw)<>D972ABTransportSha then Error("AUTOMATIC replay transport missing/SHA drift"); fi;
D972ABTransportObj:=JsonStringToGap(D972ABTransportRaw);;
if D972ABTransportObj.schema<>"d972-b4-u-simplified-transport/v1" or
   D972ABTransportObj.source_sha256<>D972ABSourceSha or D972ABTransportObj.relator_sha256<>D972ABRelSha or
   D972ABTransportObj.roof_norm_sha256<>D972ABNormSha or
   D972ABTransportObj.simple_relators_sha256<>D972ABSimpleRelSha or
   D972ABTransportObj.simple_norms_sha256<>D972ABSimpleNormSha or
   Length(D972ABTransportObj.simple_relators)<>141 or Length(D972ABTransportObj.simple_norm_words)<>972 then
  Error("AUTOMATIC replay transport gate failed");
fi;
D972ABNames:=D972ABObj.automaton_names;; D972ABBindings:=D972ABObj.automaton_bindings;;
D972ABPaths:=D972ABObj.automaton_paths;; D972ABStates:=D972ABObj.automaton_states;; D972ABSHashes:=D972ABObj.automaton_sha256;;
if D972ABNames<>["wa","diff1","diff2"] and
   D972ABNames<>["wa","diff1","diff2","reduction"] then Error("AUTOMATIC replay automaton names drift"); fi;
if Length(D972ABBindings)<>Length(D972ABNames) or Length(D972ABPaths)<>Length(D972ABNames) or
   Length(D972ABStates)<>Length(D972ABNames) or Length(D972ABSHashes)<>Length(D972ABNames) then Error("AUTOMATIC replay automaton ledger drift"); fi;
Print("B4_SIMPLE_AUTOMATIC_REPLAY_INPUT_PASS receipt_sha256=",HexSHA256(D972ABRaw),
  " automata=",D972ABNames," norms=972\n");

## Load the FSA files emitted with assignment names by the producer.
for D972ABI in [1..Length(D972ABPaths)] do
  if HexSHA256(StringFile(D972ABPaths[D972ABI]))<>D972ABSHashes[D972ABI] then Error("AUTOMATIC replay FSA SHA drift"); fi;
  Read(D972ABPaths[D972ABI]);
od;
if not IsBound(D972SAWA) or not IsBound(D972SADiff1) or not IsBound(D972SADiff2) then Error("AUTOMATIC replay FSA bindings missing"); fi;
if NumberOfStatesFSA(D972SAWA)<>D972ABStates[1] or NumberOfStatesFSA(D972SADiff1)<>D972ABStates[2] or NumberOfStatesFSA(D972SADiff2)<>D972ABStates[3] then Error("AUTOMATIC replay FSA state drift"); fi;
if not IsDeterministicFSA(D972SAWA) or not IsDeterministicFSA(D972SADiff1) or not IsDeterministicFSA(D972SADiff2) then Error("AUTOMATIC replay nondeterministic FSA"); fi;

D972ABF:=FreeGroup(5);; D972ABG:=GeneratorsOfGroup(D972ABF);;
D972ABRels:=List(D972ABTransportObj.simple_relators,w->D972ABSignedWordObj(w,D972ABG));;
D972ABS:=D972ABF/D972ABRels;; D972ABSG:=GeneratorsOfGroup(D972ABS);;
D972ABRws:=KBMAGRewritingSystem(D972ABS);; SetOrderingOfKBMAGRewritingSystem(D972ABRws,"shortlex");;
D972ABRws!.wa:=D972SAWA;; D972ABRws!.diff1:=D972SADiff1;; D972ABRws!.diff2:=D972SADiff2;;
if Length(D972ABNames)=4 then
  if not IsBound(D972SAReduction) or NumberOfStatesFSA(D972SAReduction)<>D972ABStates[4] then Error("AUTOMATIC replay reduction FSA drift"); fi;
  D972ABRws!.reductionFSA:=D972SAReduction;
fi;
D972ABReduced:=[];;
for D972ABI in [1..Length(D972ABTransportObj.simple_norm_words)] do
  D972ABZ:=ReducedForm(D972ABRws,D972ABSignedWordObj(D972ABTransportObj.simple_norm_words[D972ABI],D972ABG));;
  Add(D972ABReduced,D972ABSignedObj(D972ABZ));
od;
if D972ABReduced<>D972ABObj.reduced_norm_words then Error("AUTOMATIC replay reduced words drift"); fi;
if Number(D972ABReduced,x->Length(x)=0)<>972 then Error("AUTOMATIC replay is not all-empty"); fi;
Print("B4_SIMPLE_AUTOMATIC_REPLAY_PASS all_empty=972 automata=",D972ABNames,"\n");
D972ABOut:=Concatenation(
  "{\"schema\":\"d972-b4-simplified-automatic-gap-replay/v1\",\"status\":\"B4_B_TERMINAL_CANDIDATE_REPLAYED\",",
  "\"automatic_receipt_sha256\":\"",HexSHA256(D972ABRaw),"\",\"transport_receipt_sha256\":\"",D972ABTransportSha,
  "\",\"norm_count\":972,\"all_empty\":true,\"automata_replayed\":true,\"rws_size_receipt_verified\":true,\"rws_size\":",
  D972ABJson(D972ABObj.rws_size),",\"expected_sq_order\":",String(D972ABExpectedSize),
  ",\"rws_size_matches_expected\":",D972ABJson(D972ABObj.rws_size_matches_expected),
  ",\"proof_level\":\"GPAxioms_RECEIPT_PLUS_FSA_REPLAY_PENDING_LEAN\"}");
D972ABFout:=OutputTextFile(D972ABOutput,false);; SetPrintFormattingStatus(D972ABFout,false); PrintTo(D972ABFout,Concatenation(D972ABOut,"\n"));; CloseStream(D972ABFout);
Print("B4_SIMPLE_AUTOMATIC_REPLAY_FINAL_MARKER output=",D972ABOutput," status=B4_B_TERMINAL_CANDIDATE_REPLAYED\n");
