#############################################################################
## d972_b4_u_metabelian_kbmag_v1.g -- raw K commutativity/finite-kernel lane.
##
## The frozen raw-161/5056 ordinary Reidemeister--Schreier construction is
## reused only as a source of exact words.  The old p-quotient block is
## disabled by an auditable one-occurrence splice; no GAP order or
## isomorphism result is used as a proof.  AutomaticStructure plus GpAxioms
## is required before any ReducedForm ledger is interpreted.
##
## All 12880 pairwise commutators of the raw K generators and all 972 exact
## norms are reduced.  Empty commutators are the required replayable K
## abelianity gate.  Only a nonempty norm after that gate (and the axiom
## gate) is a finite C9^10 B4-A candidate; an all-empty commutator and norm
## ledger is only a B4-B replay candidate.
#############################################################################

D972MCSourcePath := "search/d972_b4_u_anupq_kernel_v2.g";;
D972MCSourceSha :=
  "ae605e53f0a6823b6362ffe9e063cb9b4ea824ff1a28992c17da8706feb62576";;
D972MCRhoSha :=
  "23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed";;
D972MCInput := "search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972MCWords := "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972MCOutput := Filename(DirectoryTemporary(),
  "d972_b4_u_metabelian_kbmag_v1.json");;
D972MCAutoPrefix := Filename(DirectoryTemporary(),
  "d972_b4_u_metabelian_kbmag_automaton");;
D972MCReplayRequested:=false;;
if IsBound(D972_B4_METABELIAN_INPUT) then D972MCInput:=D972_B4_METABELIAN_INPUT; fi;
if IsBound(D972_B4_METABELIAN_WORDS) then D972MCWords:=D972_B4_METABELIAN_WORDS; fi;
if IsBound(D972_B4_METABELIAN_OUTPUT) then D972MCOutput:=D972_B4_METABELIAN_OUTPUT; fi;
if IsBound(D972_B4_METABELIAN_AUTOMATA_PREFIX) then
  D972MCAutoPrefix:=D972_B4_METABELIAN_AUTOMATA_PREFIX;
fi;
if IsBound(D972_B4_METABELIAN_POST_REPLAY) then
  D972MCReplayRequested:=D972_B4_METABELIAN_POST_REPLAY;
fi;
D972MCLarge:=false;; D972MCFilestore:=false;; D972MCDiff1:=false;;
D972MCMaxEqns:=250000;; D972MCMaxStates:=250000;; D972MCMaxWdiffs:=250000;;
D972MCMaxStored:=[4000,4000];;
if IsBound(D972_B4_METABELIAN_LARGE) then D972MCLarge:=D972_B4_METABELIAN_LARGE; fi;
if IsBound(D972_B4_METABELIAN_FILESTORE) then D972MCFilestore:=D972_B4_METABELIAN_FILESTORE; fi;
if IsBound(D972_B4_METABELIAN_DIFF1) then D972MCDiff1:=D972_B4_METABELIAN_DIFF1; fi;
if IsBound(D972_B4_METABELIAN_MAXEQNS) then D972MCMaxEqns:=D972_B4_METABELIAN_MAXEQNS; fi;
if IsBound(D972_B4_METABELIAN_MAXSTATES) then D972MCMaxStates:=D972_B4_METABELIAN_MAXSTATES; fi;
if IsBound(D972_B4_METABELIAN_MAXWDIFFS) then D972MCMaxWdiffs:=D972_B4_METABELIAN_MAXWDIFFS; fi;
if IsBound(D972_B4_METABELIAN_MAXSTOREDLEN) then D972MCMaxStored:=D972_B4_METABELIAN_MAXSTOREDLEN; fi;
if not IsBool(D972MCLarge) or not IsBool(D972MCFilestore) or
   not IsBool(D972MCDiff1) or not IsInt(D972MCMaxEqns) or
   not IsInt(D972MCMaxStates) or not IsInt(D972MCMaxWdiffs) or
   not IsString(D972MCOutput) or not IsString(D972MCAutoPrefix) or
   not IsBool(D972MCReplayRequested) or
   not IsList(D972MCMaxStored) or Length(D972MCMaxStored)<>2 or
   not ForAll(D972MCMaxStored,x->IsInt(x) and x>0) then
  Error("metabelian setting type drift");
fi;

## The frozen source creates D972ANV2Raw, D972ANV2Kfp and D972ANV2NormRows
## before its p-quotient block.  Disable that block without editing the
## source file, then close both GAP if-statements explicitly.
D972MCRaw := StringFile(D972MCSourcePath);;
if D972MCRaw=fail or HexSHA256(D972MCRaw)<>D972MCSourceSha then
  Error("metabelian frozen source SHA drift");
fi;
if PositionSublist(D972MCRaw,Concatenation("QU","IT;"))<>fail then
  Error("metabelian source contains bare QUIT in Read context");
fi;
D972MCNeedle := "D972ANV2Classes:=[2,3];;";;
D972MCCut := PositionSublist(D972MCRaw,D972MCNeedle);;
if D972MCCut=fail then
  Error("metabelian source splice occurrence drift");
fi;
D972MCSecond:=PositionSublist(
  D972MCRaw{[D972MCCut+Length(D972MCNeedle)..Length(D972MCRaw)]},
  D972MCNeedle);;
if D972MCSecond<>fail then
  Error("metabelian source splice is not unique");
fi;
D972MCPatched := Concatenation(
  D972MCRaw{[1..D972MCCut-1]},D972MCNeedle," if false then\n",
  D972MCRaw{[D972MCCut+Length(D972MCNeedle)..Length(D972MCRaw)]},
  "\nfi;\n");;
D972MCTmp := Filename(DirectoryTemporary(),"d972_b4_u_metabelian_source.g");;
FileString(D972MCTmp,D972MCPatched);;
D972_B4_ANUPQ_INPUT:=D972MCInput;; D972_B4_ANUPQ_WORDS:=D972MCWords;;
D972_B4_ANUPQ_SELFTEST:=false;;
Read(D972MCTmp);;
if not IsBound(D972ANV2Kfp) or not IsBound(D972ANV2Raw) or
   not IsBound(D972ANV2NormRows) or Length(D972ANV2Raw.relators)<>5056 or
   Length(D972ANV2Raw.pair_words)<>161 or Length(D972ANV2NormRows)<>972 then
  Error("metabelian raw RS construction missing");
fi;
if HexSHA256(D972ANV2Json(D972ANV2Rho))<>D972MCRhoSha then
  Error("metabelian canonical rho digest drift");
fi;

if LoadPackage("kbmag")<>true then Error("metabelian kbmag unavailable"); fi;
D972MCRws:=KBMAGRewritingSystem(D972ANV2Kfp);;
SetOrderingOfKBMAGRewritingSystem(D972MCRws,"shortlex");;
D972MCOpts:=OptionsRecordOfKBMAGRewritingSystem(D972MCRws);;
D972MCOpts.maxeqns:=D972MCMaxEqns;; D972MCOpts.maxstates:=D972MCMaxStates;;
D972MCOpts.maxwdiffs:=D972MCMaxWdiffs;; D972MCOpts.maxstoredlen:=D972MCMaxStored;;
Print("B4_METABELIAN_BEGIN raw_generators=161 raw_relators=5056 norms=972",
  " large=",D972MCLarge," filestore=",D972MCFilestore,
  " diff1=",D972MCDiff1,"\n");
D972MCAuto:=AutomaticStructure(D972MCRws,D972MCLarge,D972MCFilestore,D972MCDiff1);;
D972MCGpGenMult:=false;; D972MCGpCheckMult:=false;;
D972MCAxioms:=false;;
if D972MCAuto=true then
  D972MCGpGenMult:=GpGenMult(D972MCRws,D972MCLarge,D972MCFilestore);;
  if D972MCGpGenMult=true then
    D972MCGpCheckMult:=GpCheckMult(D972MCRws,D972MCLarge,D972MCFilestore);;
  fi;
  if D972MCGpCheckMult=true then
    D972MCAxioms:=GpAxioms(D972MCRws,D972MCLarge,D972MCFilestore);;
  fi;
fi;
D972MCAb:=AbelianInvariants(D972ANV2Kfp);;
D972MCCommBits:=[];; D972MCCommBad:=[];; D972MCNormBits:=[];; D972MCNormBad:=[];;
D972MCKG:=GeneratorsOfGroup(D972ANV2Kfp);;
D972MCAutoNames:=[];; D972MCAutoBindings:=[];; D972MCAutoPaths:=[];;
D972MCAutoStates:=[];; D972MCAutoShas:=[];;
if D972MCAuto=true then
  D972MCAutoNames:=["wa","diff1","diff2"];;
  D972MCAutoBindings:=["D972MCWA","D972MCDiff1FSA","D972MCDiff2FSA"];;
  D972MCAutoFsa:=[WordAcceptor(D972MCRws),
    FirstWordDifferenceAutomaton(D972MCRws),
    SecondWordDifferenceAutomaton(D972MCRws)];;
  if IsBound(D972MCRws!.reductionFSA) then
    Add(D972MCAutoNames,"reduction");;
    Add(D972MCAutoBindings,"D972MCReductionFSA");;
    Add(D972MCAutoFsa,D972MCRws!.reductionFSA);;
  fi;
  for D972MCI in [1..Length(D972MCAutoFsa)] do
    D972MCP:=Concatenation(D972MCAutoPrefix,"_",D972MCAutoNames[D972MCI],".fsa");;
    WriteFSA(D972MCAutoFsa[D972MCI],D972MCAutoBindings[D972MCI],D972MCP,";");;
    Add(D972MCAutoPaths,D972MCP);;
    Add(D972MCAutoStates,NumberOfStatesFSA(D972MCAutoFsa[D972MCI]));;
    Add(D972MCAutoShas,HexSHA256(StringFile(D972MCP)));;
  od;
fi;
if D972MCAuto=true and D972MCAxioms=true then
  for D972MCI in [1..160] do
    for D972MCJ in [D972MCI+1..161] do
      D972MCZ:=ReducedForm(D972MCRws,D972MCKG[D972MCI]*D972MCKG[D972MCJ]*
        D972MCKG[D972MCI]^-1*D972MCKG[D972MCJ]^-1);;
      Add(D972MCCommBits,IsOne(D972MCZ));;
      if not IsOne(D972MCZ) then Add(D972MCCommBad,
        [D972MCI,D972MCJ,D972ANV2SignedWord(D972MCZ,D972MCKG)]); fi;
    od;
  od;
  for D972MCI in [1..972] do
    D972MCZ:=ReducedForm(D972MCRws,
      D972ANV2SignedWord(D972ANV2NormRows[D972MCI],D972MCKG));;
    Add(D972MCNormBits,IsOne(D972MCZ));;
    if not IsOne(D972MCZ) and Length(D972MCNormBad)=0 then
      Add(D972MCNormBad,[D972MCI,D972ANV2NormRows[D972MCI],
        D972ANV2SignedWord(D972MCZ,D972MCKG)]); fi;
  od;
fi;
D972MCCommEmpty:=Number(D972MCCommBits,x->x=true);;
D972MCNormEmpty:=Number(D972MCNormBits,x->x=true);;
D972MCStatus:="UNKNOWN_AUTOMATIC_OR_AXIOMS";;
if D972MCAuto=true and D972MCAxioms=true then
  if D972MCCommEmpty<>12880 then D972MCStatus:="UNKNOWN_K_NONABELIAN";
  elif Length(D972MCNormBad)>0 then D972MCStatus:="B4_A_CANDIDATE_K_C9";
  elif D972MCNormEmpty=972 then D972MCStatus:="B4_B_CANDIDATE_K_ABELIAN_PENDING_REPLAY";
  else D972MCStatus:="UNKNOWN_NORM_LEDGER"; fi;
fi;
D972MCJson:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if x=true then return "true"; fi; if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("metabelian JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972MCJson(x[i]));;
  return Concatenation("[",JoinStringsWithSeparator(p,","),"]");
end;;
D972MCOut:=Concatenation(
  "{\"schema\":\"d972-b4-u-metabelian-kbmag/v1\",",
  "\"status\":",D972MCJson(D972MCStatus),",
  "\"source_sha256\":",D972MCJson(D972ANV2SourceSha),",
  "\"rs_constructor_sha256\":",D972MCJson(D972MCSourceSha),",
  "\"rho_words_sha256\":",D972MCJson(D972MCRhoSha),",
  "\"relator_sha256\":",D972MCJson(D972ANV2RelSha),",
  "\"norm_original_sha256\":",D972MCJson(D972ANV2NormSha),",
  "\"word_artifact_sha256\":",D972MCJson(D972ANV2WordsSha),",
  "\"raw_rs_relators_sha256\":",D972MCJson(HexSHA256(D972ANV2Json(D972ANV2Raw.relators))),",
  "\"norm_rs_sha256\":",D972MCJson(HexSHA256(D972ANV2Json(D972ANV2NormRows))),",
  "\"raw_rs_generator_count\":161,\"raw_rs_relator_count\":5056,\"norm_count\":972,",
  "\"commutator_count\":12880,\"commutator_empty_count\":",String(D972MCCommEmpty),",
  "\"commutator_ledger_sha256\":",D972MCJson(HexSHA256(D972MCJson(D972MCCommBits))),",
  "\"norm_empty_count\":",String(D972MCNormEmpty),",
  "\"norm_ledger_sha256\":",D972MCJson(HexSHA256(D972MCJson(D972MCNormBits))),",
  "\"automatic_success\":",D972MCJson(D972MCAuto),",
  "\"gpgenmult_rechecked\":",D972MCJson(D972MCGpGenMult),",
  "\"gpcheckmult_rechecked\":",D972MCJson(D972MCGpCheckMult),",
  "\"gpaxioms_rechecked\":",D972MCJson(D972MCAxioms),",
  "\"large\":",D972MCJson(D972MCLarge),",\"filestore\":",D972MCJson(D972MCFilestore),
  ",\"diff1\":",D972MCJson(D972MCDiff1),",
  "\"automaton_names\":",D972MCJson(D972MCAutoNames),",
  "\"automaton_bindings\":",D972MCJson(D972MCAutoBindings),",
  "\"automaton_paths\":",D972MCJson(D972MCAutoPaths),",
  "\"automaton_states\":",D972MCJson(D972MCAutoStates),",
  "\"automaton_sha256\":",D972MCJson(D972MCAutoShas),",
  "\"commutator_ledger\":",D972MCJson(D972MCCommBits),",
  "\"norm_ledger\":",D972MCJson(D972MCNormBits),",
  "\"post_replay_requested\":",D972MCJson(D972MCReplayRequested),",
  "\"abelian_invariants\":",D972MCJson(D972MCAb),",
  "\"first_commutator_defect\":",D972MCJson(ShallowCopy(D972MCCommBad)),",
  "\"first_norm_defect\":",D972MCJson(ShallowCopy(D972MCNormBad)),",
  "\"proof_level\":\"RAW_RS_AUTOMATIC_GPAXIOMS_REPLAY_REQUIRED\"}");;
D972MCF:=OutputTextFile(D972MCOutput,false);; SetPrintFormattingStatus(D972MCF,false);
PrintTo(D972MCF,Concatenation(D972MCOut,"\n"));; CloseStream(D972MCF);
Print("B4_METABELIAN_FINAL_MARKER output=",D972MCOutput," status=",D972MCStatus,
  " comm_empty=",D972MCCommEmpty,"/12880 norm_empty=",D972MCNormEmpty,"/972\n");
if D972MCReplayRequested=true then
  D972_B4_METABELIAN_REPLAY_RECEIPT:=D972MCOutput;;
  D972_B4_METABELIAN_REPLAY_INPUT:=D972MCInput;;
  D972_B4_METABELIAN_REPLAY_WORDS:=D972MCWords;;
  D972_B4_METABELIAN_REPLAY_OUTPUT:="ci/out/d972_b4_u_metabelian_kbmag_replay_v1.json";;
  D972_B4_METABELIAN_REPLAY_LARGE:=D972MCLarge;;
  D972_B4_METABELIAN_REPLAY_FILESTORE:=D972MCFilestore;;
  D972_B4_METABELIAN_REPLAY_DIFF1:=D972MCDiff1;;
  D972_B4_METABELIAN_REPLAY_MAXEQNS:=D972MCMaxEqns;;
  D972_B4_METABELIAN_REPLAY_MAXSTATES:=D972MCMaxStates;;
  D972_B4_METABELIAN_REPLAY_MAXWDIFFS:=D972MCMaxWdiffs;;
  D972_B4_METABELIAN_REPLAY_MAXSTOREDLEN:=D972MCMaxStored;;
  Read("search/check_d972_b4_u_metabelian_kbmag_replay_v1.g");;
  if StringFile(D972_B4_METABELIAN_REPLAY_OUTPUT)=fail then
    Error("metabelian post-replay receipt missing");
  fi;
  Print("B4_METABELIAN_POST_REPLAY_PASS output=",
    D972_B4_METABELIAN_REPLAY_OUTPUT,"\n");
fi;
