#############################################################################
## Independent replay for configurable direct AutomaticStructure v2.
## It checks the producer's v2 settings, reconstructs the pinned 6/158 and
## 972 norm data, reattaches the exported FSAs, and independently runs the
## KBMAG multiplier/axiom checks before classifying every reduced norm.
#############################################################################

if LoadPackage("json")<>true then Error("ORIGINAL v2 replay: json unavailable"); fi;
D972OA2RReceipt:="ci/out/d972_b4_original_automatic_v1.json";;
D972OA2RSource:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972OA2RWords:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972OA2ROutput:="ci/out/d972_b4_original_automatic_replay_v2.json";;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_RECEIPT) then D972OA2RReceipt:=D972_B4_ORIGINAL_REPLAY_V2_RECEIPT; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_SOURCE) then D972OA2RSource:=D972_B4_ORIGINAL_REPLAY_V2_SOURCE; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_WORDS) then D972OA2RWords:=D972_B4_ORIGINAL_REPLAY_V2_WORDS; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_OUTPUT) then D972OA2ROutput:=D972_B4_ORIGINAL_REPLAY_V2_OUTPUT; fi;
D972OA2RLarge:=true;; D972OA2RFilestore:=true;; D972OA2RDiff1:=false;; D972OA2RComputeSize:=true;; D972OA2RPostReplay:=false;;
D972OA2RMaxEqns:=250000;; D972OA2RMaxStates:=250000;; D972OA2RMaxWdiffs:=250000;; D972OA2RMaxStored:=[4000,4000];;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_LARGE) then D972OA2RLarge:=D972_B4_ORIGINAL_REPLAY_V2_LARGE; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_FILESTORE) then D972OA2RFilestore:=D972_B4_ORIGINAL_REPLAY_V2_FILESTORE; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_DIFF1) then D972OA2RDiff1:=D972_B4_ORIGINAL_REPLAY_V2_DIFF1; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_COMPUTE_SIZE) then D972OA2RComputeSize:=D972_B4_ORIGINAL_REPLAY_V2_COMPUTE_SIZE; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_POST_REPLAY) then D972OA2RPostReplay:=D972_B4_ORIGINAL_REPLAY_V2_POST_REPLAY; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_MAXEQNS) then D972OA2RMaxEqns:=D972_B4_ORIGINAL_REPLAY_V2_MAXEQNS; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_MAXSTATES) then D972OA2RMaxStates:=D972_B4_ORIGINAL_REPLAY_V2_MAXSTATES; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_MAXWDIFFS) then D972OA2RMaxWdiffs:=D972_B4_ORIGINAL_REPLAY_V2_MAXWDIFFS; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_V2_MAXSTOREDLEN) then D972OA2RMaxStored:=D972_B4_ORIGINAL_REPLAY_V2_MAXSTOREDLEN; fi;
if not IsBool(D972OA2RLarge) or not IsBool(D972OA2RFilestore) or not IsBool(D972OA2RDiff1) or
   not IsBool(D972OA2RComputeSize) or not IsBool(D972OA2RPostReplay) or not IsInt(D972OA2RMaxEqns) or D972OA2RMaxEqns<=0 or
   not IsInt(D972OA2RMaxStates) or D972OA2RMaxStates<=0 or not IsInt(D972OA2RMaxWdiffs) or
   D972OA2RMaxWdiffs<=0 or not IsList(D972OA2RMaxStored) or Length(D972OA2RMaxStored)<>2 or
   not ForAll(D972OA2RMaxStored,x->IsInt(x) and x>0) then
  Error("ORIGINAL v2 replay: setting type drift");
fi;
D972OA2RRaw:=StringFile(D972OA2RReceipt);; if D972OA2RRaw=fail then Error("ORIGINAL v2 replay: receipt missing"); fi;
D972OA2RObj:=JsonStringToGap(D972OA2RRaw);;
D972OA2RLegacy:=not IsBound(D972OA2RObj.v2_settings);;
if D972OA2RLegacy then
  ## Frozen v1 receipts have no v2_settings field.  This compatibility mode
  ## is deliberately the exact v1 default and is used only by the separate
  ## legacy terminal wrapper; it still runs the full independent replay below.
  if D972OA2RLarge<>true or D972OA2RFilestore<>true or D972OA2RDiff1<>false or
     D972OA2RComputeSize<>true or D972OA2RMaxEqns<>250000 or D972OA2RMaxStates<>250000 or
     D972OA2RMaxWdiffs<>250000 or D972OA2RMaxStored<>[4000,4000] then
    Error("ORIGINAL v2 replay: legacy v1 settings drift");
  fi;
  D972OA2RS:=fail;;
else
  D972OA2RS:=D972OA2RObj.v2_settings;;
  if D972OA2RS.producer<>"d972_b4_original_automatic_v2" or
     D972OA2RS.v1_source_sha256<>"fcb32175837412bbce9bf117fbe0eb8c4f8cc1b11f9fa921b46acf133ecc6874" or
     D972OA2RS.large<>D972OA2RLarge or D972OA2RS.filestore<>D972OA2RFilestore or
     D972OA2RS.diff1<>D972OA2RDiff1 or D972OA2RS.compute_size<>D972OA2RComputeSize or
     D972OA2RS.post_replay<>D972OA2RPostReplay or
     D972OA2RS.maxeqns<>D972OA2RMaxEqns or D972OA2RS.maxstates<>D972OA2RMaxStates or
     D972OA2RS.maxwdiffs<>D972OA2RMaxWdiffs or D972OA2RS.maxstoredlen<>D972OA2RMaxStored then
    Error("ORIGINAL v2 replay: settings binding failed");
  fi;
fi;
Print("B4_ORIGINAL_AUTOMATIC_V2_REPLAY_SETTINGS_PASS diff1=",D972OA2RDiff1,
  " legacy=",D972OA2RLegacy,"\n");

## Rebuild the pinned source and norm list here.  This body is intentionally
## independent of the v1 replay: in particular it accepts a producer receipt
## that skipped Size(rws), and it does not turn the producer's
## automatic_axiom_checked field into an independent axiom proof.
D972OA2RSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972OA2RWordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972OA2RRelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972OA2RRhoSha:="23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed";;
D972OA2RRoofSha:="3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f";;
D972OA2RNormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972OA2RTargetSha:="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972OA2RTupleSha:="32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91";;
D972OA2RJson:=function(x) local p,i; if IsInt(x) then return String(x); fi; if IsList(x) and Length(x)=0 then return "[]"; fi; if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi; if x=true then return "true"; fi; if x=false then return "false"; fi; if x=fail then return "null"; fi; if IsRecord(x) then return Concatenation("{\"producer\":",D972OA2RJson(x.producer),",\"large\":",D972OA2RJson(x.large),",\"filestore\":",D972OA2RJson(x.filestore),",\"diff1\":",D972OA2RJson(x.diff1),",\"compute_size\":",D972OA2RJson(x.compute_size),",\"maxeqns\":",D972OA2RJson(x.maxeqns),",\"maxstates\":",D972OA2RJson(x.maxstates),",\"maxwdiffs\":",D972OA2RJson(x.maxwdiffs),",\"maxstoredlen\":",D972OA2RJson(x.maxstoredlen),",\"post_replay\":",D972OA2RJson(x.post_replay),",\"v1_source_sha256\":",D972OA2RJson(x.v1_source_sha256),"}"); fi; if not IsList(x) then Error("ORIGINAL v2 replay JSON drift"); fi; p:=List([1..Length(x)],i->D972OA2RJson(x[i])); return Concatenation("[",JoinStringsWithSeparator(p,","),"]"); end;;
D972OA2RFR:=function(row) local out,x,n; out:=[]; for x in row do n:=Length(out); if n>0 and out[n]=-x then Remove(out,n); else Add(out,x); fi; od; return out; end;;
D972OA2RRhoWord:=function(w,rho) local out,x,img; out:=[]; for x in w do img:=rho[AbsInt(x)]; if x<0 then img:=List(Reversed(img),y->-y); fi; out:=Concatenation(out,img); od; return D972OA2RFR(out); end;;
D972OA2RNorm:=function(row,rho) local j,x,v,orb,z,t; j:=[]; for x in row do if AbsInt(x)=1 then Add(j,SignInt(x)); elif AbsInt(x)=2 then Add(j,SignInt(x)*4); else Error("ORIGINAL v2 replay F2 alphabet drift"); fi; od; j:=D972OA2RFR(j); v:=j; orb:=[]; for t in [1..5] do Add(orb,v); v:=D972OA2RRhoWord(v,rho); od; z:=[]; for t in Reversed([1..5]) do z:=D972OA2RFR(Concatenation(z,orb[t])); od; return z; end;;
D972OA2RSignedObj:=function(w) local e,o,i,g,n,j; e:=ExtRepOfObj(w); o:=[]; i:=1; while i<=Length(e) do g:=e[i]; n:=e[i+1]; if n>0 then for j in [1..n] do Add(o,g); od; else for j in [1..-n] do Add(o,-g); od; fi; i:=i+2; od; return o; end;;
D972OA2RSignedWord:=function(row,gens) local w,x; w:=One(gens[1]); for x in row do if x>0 then w:=w*gens[x]; else w:=w*gens[-x]^-1; fi; od; return w; end;;
if D972OA2RObj.schema<>"d972-b4-original-automatic/v1" or
   D972OA2RObj.automatic_success<>true or D972OA2RObj.automatic_axiom_checked<>true or
   D972OA2RObj.source_sha256<>D972OA2RSourceSha or D972OA2RObj.word_artifact_sha256<>D972OA2RWordsSha or
   D972OA2RObj.relator_sha256<>D972OA2RRelSha or D972OA2RObj.rho_words_sha256<>D972OA2RRhoSha or
   D972OA2RObj.roof_words_sha256<>D972OA2RRoofSha or D972OA2RObj.roof_norm_sha256<>D972OA2RNormSha or
   Length(D972OA2RObj.reduced_norm_words)<>972 or
   HexSHA256(D972OA2RJson(D972OA2RObj.reduced_norm_words))<>D972OA2RObj.reduced_norm_words_sha256 then
  Error("ORIGINAL v2 replay receipt/canonical gate failed");
fi;
D972OA2RSourceRaw:=StringFile(D972OA2RSource);; if D972OA2RSourceRaw=fail or HexSHA256(D972OA2RSourceRaw)<>D972OA2RSourceSha then Error("ORIGINAL v2 replay source SHA drift"); fi;
D972OA2RSourceObj:=JsonStringToGap(D972OA2RSourceRaw);; D972OA2RRho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;
if D972OA2RSourceObj.schema<>"d972-b4-p2-magnus-input/v2" or D972OA2RSourceObj.rho_words<>D972OA2RRho or
   D972OA2RSourceObj.rho_words_source<>"universal_v2_canonical" or D972OA2RSourceObj.all_relators_sha256<>D972OA2RRelSha or
   D972OA2RSourceObj.roof_words_sha256<>D972OA2RRoofSha then Error("ORIGINAL v2 replay source gate failed"); fi;
D972OA2RWordsRaw:=StringFile(D972OA2RWords);; if D972OA2RWordsRaw=fail or HexSHA256(D972OA2RWordsRaw)<>D972OA2RWordsSha then Error("ORIGINAL v2 replay words SHA drift"); fi;
D972OA2RWordsObj:=JsonStringToGap(D972OA2RWordsRaw);; if D972OA2RWordsObj.schema<>"d972-b4-word-key-artifact/v1" or D972OA2RWordsObj.count<>972 or
   D972OA2RWordsObj.source_target_key_digest<>D972OA2RTargetSha or D972OA2RWordsObj.frozen_tuple_sha256<>D972OA2RTupleSha then Error("ORIGINAL v2 replay words gate failed"); fi;
D972OA2RRoof:=[];; for D972OA2RRow in D972OA2RWordsObj.rows do D972OA2RWord:=D972OA2RRow[3];; if D972OA2RWord="" then D972OA2RWord:=[]; fi; Add(D972OA2RRoof,D972OA2RWord); od;
if D972OA2RRoof<>D972OA2RSourceObj.roof_words or HexSHA256(D972OA2RJson(D972OA2RRoof))<>D972OA2RRoofSha then Error("ORIGINAL v2 replay roof drift"); fi;
D972OA2RNorms:=List(D972OA2RRoof,w->D972OA2RNorm(w,D972OA2RRho));; if HexSHA256(D972OA2RJson(D972OA2RNorms))<>D972OA2RNormSha then Error("ORIGINAL v2 replay norm drift"); fi;
D972OA2RNames:=D972OA2RObj.automaton_names;; D972OA2RBindings:=D972OA2RObj.automaton_bindings;; D972OA2RPaths:=D972OA2RObj.automaton_paths;; D972OA2RStates:=D972OA2RObj.automaton_states;; D972OA2RShas:=D972OA2RObj.automaton_sha256;;
if D972OA2RNames<>["wa","diff1","diff2"] and D972OA2RNames<>["wa","diff1","diff2","reduction"] then Error("ORIGINAL v2 replay automaton names"); fi;
if Length(D972OA2RPaths)<>Length(D972OA2RNames) or Length(D972OA2RStates)<>Length(D972OA2RNames) or Length(D972OA2RShas)<>Length(D972OA2RNames) then Error("ORIGINAL v2 replay automaton ledger"); fi;
for D972OA2RI in [1..Length(D972OA2RPaths)] do if StringFile(D972OA2RPaths[D972OA2RI])=fail or HexSHA256(StringFile(D972OA2RPaths[D972OA2RI]))<>D972OA2RShas[D972OA2RI] then Error("ORIGINAL v2 replay FSA SHA"); fi; Read(D972OA2RPaths[D972OA2RI]); od;
if not IsBound(D972OAWA) or not IsBound(D972OADiff1) or not IsBound(D972OADiff2) then Error("ORIGINAL v2 replay FSA bindings"); fi;
if NumberOfStatesFSA(D972OAWA)<>D972OA2RStates[1] or NumberOfStatesFSA(D972OADiff1)<>D972OA2RStates[2] or NumberOfStatesFSA(D972OADiff2)<>D972OA2RStates[3] then Error("ORIGINAL v2 replay FSA states"); fi;
if not IsDeterministicFSA(D972OAWA) or not IsDeterministicFSA(D972OADiff1) or not IsDeterministicFSA(D972OADiff2) then Error("ORIGINAL v2 replay nondeterministic FSA"); fi;
D972OA2RF:=FreeGroup(6);; D972OA2RG:=GeneratorsOfGroup(D972OA2RF);; D972OA2RRels:=List(D972OA2RSourceObj.all_relators,w->D972OA2RSignedWord(w,D972OA2RG));; D972OA2RU:=D972OA2RF/D972OA2RRels;; D972OA2RRws:=KBMAGRewritingSystem(D972OA2RU);; SetOrderingOfKBMAGRewritingSystem(D972OA2RRws,"shortlex");;
D972OA2RRws!.wa:=D972OAWA;; D972OA2RRws!.diff1:=D972OADiff1;; D972OA2RRws!.diff2:=D972OADiff2;;
if Length(D972OA2RNames)=4 then if not IsBound(D972OAReduction) or NumberOfStatesFSA(D972OAReduction)<>D972OA2RStates[4] or not IsDeterministicFSA(D972OAReduction) then Error("ORIGINAL v2 replay reduction FSA"); fi; D972OA2RRws!.reductionFSA:=D972OAReduction; fi;
D972OA2ROpts:=OptionsRecordOfKBMAGRewritingSystem(D972OA2RRws);; D972OA2ROpts.maxeqns:=D972OA2RMaxEqns;; D972OA2ROpts.maxstates:=D972OA2RMaxStates;; D972OA2ROpts.maxwdiffs:=D972OA2RMaxWdiffs;; D972OA2ROpts.maxstoredlen:=D972OA2RMaxStored;;
## GpAxioms is not a synonym for AutomaticStructure's return value.  Its
## documented prerequisites are regenerated from the attached wa/diff FSAs,
## then the external axiom checker is run independently on this RWS.
D972OA2RGpGenMult:=GpGenMult(D972OA2RRws,D972OA2RLarge,D972OA2RFilestore);; if D972OA2RGpGenMult<>true or not IsBound(D972OA2RRws!.gm) then Error("ORIGINAL v2 replay GpGenMult failed"); fi;
D972OA2RGpCheckMult:=GpCheckMult(D972OA2RRws,D972OA2RLarge,D972OA2RFilestore);; if D972OA2RGpCheckMult<>true then Error("ORIGINAL v2 replay GpCheckMult failed"); fi;
D972OA2RGpAxiomsResult:=GpAxioms(D972OA2RRws,D972OA2RLarge,D972OA2RFilestore);; if D972OA2RGpAxiomsResult<>true then Error("ORIGINAL v2 replay GpAxioms failed"); fi;
Print("B4_ORIGINAL_AUTOMATIC_V2_REPLAY_GPAXIOMS_PASS gpgenmult=true gpcheckmult=true gpaxioms=true\n");
D972OA2RReduced:=[];; for D972OA2RI in [1..972] do D972OA2RZ:=ReducedForm(D972OA2RRws,D972OA2RSignedWord(D972OA2RNorms[D972OA2RI],D972OA2RG));; Add(D972OA2RReduced,D972OA2RSignedObj(D972OA2RZ)); od;
if D972OA2RReduced<>D972OA2RObj.reduced_norm_words then Error("ORIGINAL v2 replay reduced ledger drift"); fi;
D972OA2REmpty:=Number(D972OA2RReduced,x->Length(x)=0);; D972OA2RNonzero:=Filtered(List(D972OA2RReduced,Length),x->x>0);; D972OA2RMin:=-1;; if Length(D972OA2RNonzero)>0 then D972OA2RMin:=Minimum(D972OA2RNonzero); fi;
D972OA2RAllEmpty:=(D972OA2REmpty=972);; if D972OA2RAllEmpty then D972OA2RStatus:="B4_B_TERMINAL_CANDIDATE_REPLAYED"; else D972OA2RStatus:="B4_A_CANDIDATE_REPLAYED"; fi;
D972OA2RProof:="DIRECT_GPAxioms_RECHECK_PLUS_FSA_REPLAY_PENDING_LEAN";;
D972OA2RLegacyFields:="";; if D972OA2RLegacy then D972OA2RLegacyFields:=",\"legacy_v1\":true,\"post_replay\":true"; fi;
D972OA2ROut:=Concatenation("{\"schema\":\"d972-b4-original-automatic-gap-replay/v2\",\"status\":\"",D972OA2RStatus,
  "\",\"automatic_receipt_sha256\":\"",HexSHA256(D972OA2RRaw),"\",\"source_sha256\":\"",D972OA2RSourceSha,
  "\",\"word_artifact_sha256\":\"",D972OA2RWordsSha,"\",\"relator_sha256\":\"",D972OA2RRelSha,
  "\",\"rho_words_sha256\":\"",D972OA2RRhoSha,"\",\"roof_words_sha256\":\"",D972OA2RRoofSha,
  "\",\"roof_norm_sha256\":\"",D972OA2RNormSha,"\",\"norm_count\":972,\"empty_count\":",String(D972OA2REmpty),
  ",\"nonempty_count\":",String(972-D972OA2REmpty),",\"min_nonzero_length\":",String(D972OA2RMin),
  ",\"all_empty\":",D972OA2RJson(D972OA2RAllEmpty),",\"automata_replayed\":true,\"gpgenmult_rechecked\":true,\"gpcheckmult_rechecked\":true,\"gpaxioms_rechecked\":true,\"gpaxioms_result\":true,\"v2_settings\":",D972OA2RJson(D972OA2RS),D972OA2RLegacyFields,",\"proof_level\":\"",D972OA2RProof,"\"}");
D972OA2RFout:=OutputTextFile(D972OA2ROutput,false);; SetPrintFormattingStatus(D972OA2RFout,false); PrintTo(D972OA2RFout,Concatenation(D972OA2ROut,"\n"));; CloseStream(D972OA2RFout);
Print("B4_ORIGINAL_AUTOMATIC_V2_REPLAY_FINAL_MARKER output=",D972OA2ROutput," status=",D972OA2RStatus,
  " empty=",D972OA2REmpty,"/972 gpaxioms=true\n");
