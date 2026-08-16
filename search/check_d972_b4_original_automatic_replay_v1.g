#############################################################################
## Independent GAP replay for d972_b4_original_automatic_v1.g.
## It rebuilds the six-generator presentation and all exact norms from the
## pinned source/artifact, then attaches only the exported FSA files.
#############################################################################

if LoadPackage("json")<>true then Error("ORIGINAL replay: json unavailable"); fi;
D972ODReceipt:=Filename(DirectoryTemporary(),"d972_b4_original_automatic_v1.json");;
D972ODSource:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972ODWords:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972ODOutput:=Filename(DirectoryTemporary(),"d972_b4_original_automatic_replay_v1.json");;
if IsBound(D972_B4_ORIGINAL_REPLAY_RECEIPT) then D972ODReceipt:=D972_B4_ORIGINAL_REPLAY_RECEIPT; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_SOURCE) then D972ODSource:=D972_B4_ORIGINAL_REPLAY_SOURCE; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_WORDS) then D972ODWords:=D972_B4_ORIGINAL_REPLAY_WORDS; fi;
if IsBound(D972_B4_ORIGINAL_REPLAY_OUTPUT) then D972ODOutput:=D972_B4_ORIGINAL_REPLAY_OUTPUT; fi;
D972ODSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972ODWordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972ODRelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972ODRhoSha:="23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed";;
D972ODRoofSha:="3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8";;
D972ODNormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972ODTargetSha:="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972ODTupleSha:="32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91";;
D972ODExpectedSize:=111577100832;;
D972ODJoin:=function(xs,sep) local z,i; if Length(xs)=0 then return ""; fi; z:=xs[1]; for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od; return z; end;;
D972ODJson:=function(x) local p,i; if IsInt(x) then return String(x); fi; if IsList(x) and Length(x)=0 then return "[]"; fi; if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi; if x=true then return "true"; fi; if x=false then return "false"; fi; if x=fail then return "null"; fi; if not IsList(x) then Error("ORIGINAL replay JSON drift"); fi; p:=List([1..Length(x)],i->D972ODJson(x[i])); return Concatenation("[",D972ODJoin(p,","),"]"); end;;
D972ODFR:=function(row) local out,x,n; out:=[]; for x in row do n:=Length(out); if n>0 and out[n]=-x then Remove(out,n); else Add(out,x); fi; od; return out; end;;
D972ODRhoWord:=function(w,rho) local out,x,img; out:=[]; for x in w do img:=rho[AbsInt(x)]; if x<0 then img:=List(Reversed(img),y->-y); fi; out:=Concatenation(out,img); od; return D972ODFR(out); end;;
D972ODNorm:=function(row,rho) local j,x,v,orb,z,t; j:=[]; for x in row do if AbsInt(x)=1 then Add(j,SignInt(x)); elif AbsInt(x)=2 then Add(j,SignInt(x)*4); else Error("ORIGINAL replay F2 alphabet drift"); fi; od; j:=D972ODFR(j); v:=j; orb:=[]; for t in [1..5] do Add(orb,v); v:=D972ODRhoWord(v,rho); od; z:=[]; for t in Reversed([1..5]) do z:=D972ODFR(Concatenation(z,orb[t])); od; return z; end;;
D972ODSignedObj:=function(w) local e,o,i,g,n,j; e:=ExtRepOfObj(w); o:=[]; i:=1; while i<=Length(e) do g:=e[i]; n:=e[i+1]; if n>0 then for j in [1..n] do Add(o,g); od; else for j in [1..-n] do Add(o,-g); od; fi; i:=i+2; od; return o; end;;
D972ODSignedWord:=function(row,gens) local w,x; w:=One(gens[1]); for x in row do if x>0 then w:=w*gens[x]; else w:=w*gens[-x]^-1; fi; od; return w; end;;
D972ODReceiptRaw:=StringFile(D972ODReceipt);; if D972ODReceiptRaw=fail then Error("ORIGINAL replay receipt missing"); fi;
D972ODObj:=JsonStringToGap(D972ODReceiptRaw);;
if D972ODObj.schema<>"d972-b4-original-automatic/v1" or D972ODObj.status<>"B4_B_CANDIDATE_PENDING_REPLAY" or
   D972ODObj.automatic_success<>true or D972ODObj.automatic_axiom_checked<>true or
   D972ODObj.source_sha256<>D972ODSourceSha or D972ODObj.word_artifact_sha256<>D972ODWordsSha or
   D972ODObj.relator_sha256<>D972ODRelSha or D972ODObj.rho_words_sha256<>D972ODRhoSha or
   D972ODObj.roof_words_sha256<>D972ODRoofSha or D972ODObj.roof_norm_sha256<>D972ODNormSha or
   D972ODObj.rws_size_status<>"COMPUTED" or D972ODObj.expected_sq_order<>D972ODExpectedSize or
   D972ODObj.rws_size_matches_expected<>(IsInt(D972ODObj.rws_size) and D972ODObj.rws_size=D972ODExpectedSize) then
  Error("ORIGINAL replay receipt gate failed");
fi;
D972ODSourceRaw:=StringFile(D972ODSource);; if D972ODSourceRaw=fail or HexSHA256(D972ODSourceRaw)<>D972ODSourceSha then Error("ORIGINAL replay source SHA drift"); fi;
D972ODSourceObj:=JsonStringToGap(D972ODSourceRaw);; D972ODRho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;
if D972ODSourceObj.schema<>"d972-b4-p2-magnus-input/v2" or D972ODSourceObj.rho_words<>D972ODRho or D972ODSourceObj.rho_words_source<>"universal_v2_canonical" or D972ODSourceObj.all_relators_sha256<>D972ODRelSha or D972ODSourceObj.roof_words_sha256<>D972ODRoofSha then Error("ORIGINAL replay source gate failed"); fi;
D972ODWordsRaw:=StringFile(D972ODWords);; if D972ODWordsRaw=fail or HexSHA256(D972ODWordsRaw)<>D972ODWordsSha then Error("ORIGINAL replay words SHA drift"); fi;
D972ODWordsObj:=JsonStringToGap(D972ODWordsRaw);; if D972ODWordsObj.schema<>"d972-b4-word-key-artifact/v1" or D972ODWordsObj.count<>972 or D972ODWordsObj.source_target_key_digest<>D972ODTargetSha or D972ODWordsObj.frozen_tuple_sha256<>D972ODTupleSha then Error("ORIGINAL replay words gate failed"); fi;
D972ODRoof:=[];; for D972ODRow in D972ODWordsObj.rows do D972ODWord:=D972ODRow[3];; if D972ODWord="" then D972ODWord:=[]; fi; Add(D972ODRoof,D972ODWord); od;
if D972ODRoof<>D972ODSourceObj.roof_words or HexSHA256(D972ODJson(D972ODRoof))<>D972ODRoofSha then Error("ORIGINAL replay roof drift"); fi;
D972ODNorms:=List(D972ODRoof,w->D972ODNorm(w,D972ODRho));; if HexSHA256(D972ODJson(D972ODNorms))<>D972ODNormSha then Error("ORIGINAL replay norm drift"); fi;
D972ODNames:=D972ODObj.automaton_names;; D972ODBindings:=D972ODObj.automaton_bindings;; D972ODPaths:=D972ODObj.automaton_paths;; D972ODStates:=D972ODObj.automaton_states;; D972ODShas:=D972ODObj.automaton_sha256;;
if D972ODNames<>["wa","diff1","diff2"] and D972ODNames<>["wa","diff1","diff2","reduction"] then Error("ORIGINAL replay automaton names"); fi;
if Length(D972ODPaths)<>Length(D972ODNames) or Length(D972ODStates)<>Length(D972ODNames) or Length(D972ODShas)<>Length(D972ODNames) then Error("ORIGINAL replay automaton ledger"); fi;
for D972ODI in [1..Length(D972ODPaths)] do if HexSHA256(StringFile(D972ODPaths[D972ODI]))<>D972ODShas[D972ODI] then Error("ORIGINAL replay automaton SHA"); fi; Read(D972ODPaths[D972ODI]); od;
if not IsBound(D972OAWA) or not IsBound(D972OADiff1) or not IsBound(D972OADiff2) then Error("ORIGINAL replay FSA bindings"); fi;
if NumberOfStatesFSA(D972OAWA)<>D972ODStates[1] or NumberOfStatesFSA(D972OADiff1)<>D972ODStates[2] or NumberOfStatesFSA(D972OADiff2)<>D972ODStates[3] then Error("ORIGINAL replay FSA states"); fi;
if not IsDeterministicFSA(D972OAWA) or not IsDeterministicFSA(D972OADiff1) or not IsDeterministicFSA(D972OADiff2) then Error("ORIGINAL replay FSA deterministic"); fi;
D972ODF:=FreeGroup(6);; D972ODG:=GeneratorsOfGroup(D972ODF);; D972ODRels:=List(D972ODSourceObj.all_relators,w->D972ODSignedWord(w,D972ODG));; D972ODU:=D972ODF/D972ODRels;;
D972ODRws:=KBMAGRewritingSystem(D972ODU);; SetOrderingOfKBMAGRewritingSystem(D972ODRws,"shortlex");; D972ODRws!.wa:=D972OAWA;; D972ODRws!.diff1:=D972OADiff1;; D972ODRws!.diff2:=D972OADiff2;;
if Length(D972ODNames)=4 then if not IsBound(D972OAReduction) then Error("ORIGINAL replay reduction binding"); fi; D972ODRws!.reductionFSA:=D972OAReduction; fi;
D972ODReduced:=[];; for D972ODI in [1..972] do D972ODZ:=ReducedForm(D972ODRws,D972ODSignedWord(D972ODNorms[D972ODI],D972ODG));; Add(D972ODReduced,D972ODSignedObj(D972ODZ)); od;
if D972ODReduced<>D972ODObj.reduced_norm_words or Number(D972ODReduced,x->Length(x)=0)<>972 then Error("ORIGINAL replay reduced ledger/all-empty failure"); fi;
Print("B4_ORIGINAL_AUTOMATIC_REPLAY_PASS all_empty=972 automata=",D972ODNames,"\n");
D972ODOut:=Concatenation("{\"schema\":\"d972-b4-original-automatic-gap-replay/v1\",\"status\":\"B4_B_TERMINAL_CANDIDATE_REPLAYED\",\"automatic_receipt_sha256\":\"",HexSHA256(D972ODReceiptRaw),"\",\"norm_count\":972,\"all_empty\":true,\"automata_replayed\":true,\"rws_size_receipt_verified\":true,\"rws_size\":",D972ODJson(D972ODObj.rws_size),",\"expected_sq_order\":",String(D972ODExpectedSize),",\"rws_size_matches_expected\":",D972ODJson(D972ODObj.rws_size_matches_expected),",\"proof_level\":\"DIRECT_GPAxioms_RECEIPT_PLUS_FSA_REPLAY_PENDING_LEAN\"}");
D972ODFout:=OutputTextFile(D972ODOutput,false);; SetPrintFormattingStatus(D972ODFout,false); PrintTo(D972ODFout,Concatenation(D972ODOut,"\n"));; CloseStream(D972ODFout);
Print("B4_ORIGINAL_AUTOMATIC_REPLAY_FINAL_MARKER output=",D972ODOutput," status=B4_B_TERMINAL_CANDIDATE_REPLAYED\n");
