#############################################################################
## Independent replay for d972_b4_u_metabelian_kbmag_v1.g.
##
## This file intentionally does not Read the metabelian producer or the raw
## RS source.  It reconstructs the canonical ordinary RS presentation from
## the pinned JSON, attaches only the exported FSAs named by the producer,
## reruns GpGenMult/GpCheckMult/GpAxioms, and then replays all 12880 pairwise
## commutators and all 972 exact norm rows.  Empty ledgers are still a GAP
## candidate pending the repository's proof-level review; a norm defect is
## promoted to the finite C9^10 route only when all K commutators also reduce
## to one.  No Size() result is used as a substitute for the relator and FSA
## replay.
#############################################################################

if LoadPackage("json")<>true then Error("metabelian replay: json unavailable"); fi;

D972MRInput:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972MRWords:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972MRReceipt:=Filename(DirectoryTemporary(),
  "d972_b4_u_metabelian_kbmag_v1.json");;
D972MROutput:=Filename(DirectoryTemporary(),
  "d972_b4_u_metabelian_kbmag_replay_v1.json");;
if IsBound(D972_B4_METABELIAN_REPLAY_INPUT) then
  D972MRInput:=D972_B4_METABELIAN_REPLAY_INPUT;
fi;
if IsBound(D972_B4_METABELIAN_REPLAY_WORDS) then
  D972MRWords:=D972_B4_METABELIAN_REPLAY_WORDS;
fi;
if IsBound(D972_B4_METABELIAN_REPLAY_RECEIPT) then
  D972MRReceipt:=D972_B4_METABELIAN_REPLAY_RECEIPT;
fi;
if IsBound(D972_B4_METABELIAN_REPLAY_OUTPUT) then
  D972MROutput:=D972_B4_METABELIAN_REPLAY_OUTPUT;
fi;

D972MRLarge:=false;; D972MRFilestore:=false;; D972MRDiff1:=false;;
D972MRMaxEqns:=250000;; D972MRMaxStates:=250000;; D972MRMaxWdiffs:=250000;;
D972MRMaxStored:=[4000,4000];;
if IsBound(D972_B4_METABELIAN_REPLAY_LARGE) then D972MRLarge:=D972_B4_METABELIAN_REPLAY_LARGE; fi;
if IsBound(D972_B4_METABELIAN_REPLAY_FILESTORE) then D972MRFilestore:=D972_B4_METABELIAN_REPLAY_FILESTORE; fi;
if IsBound(D972_B4_METABELIAN_REPLAY_DIFF1) then D972MRDiff1:=D972_B4_METABELIAN_REPLAY_DIFF1; fi;
if IsBound(D972_B4_METABELIAN_REPLAY_MAXEQNS) then D972MRMaxEqns:=D972_B4_METABELIAN_REPLAY_MAXEQNS; fi;
if IsBound(D972_B4_METABELIAN_REPLAY_MAXSTATES) then D972MRMaxStates:=D972_B4_METABELIAN_REPLAY_MAXSTATES; fi;
if IsBound(D972_B4_METABELIAN_REPLAY_MAXWDIFFS) then D972MRMaxWdiffs:=D972_B4_METABELIAN_REPLAY_MAXWDIFFS; fi;
if IsBound(D972_B4_METABELIAN_REPLAY_MAXSTOREDLEN) then D972MRMaxStored:=D972_B4_METABELIAN_REPLAY_MAXSTOREDLEN; fi;
if not IsString(D972MRInput) or not IsString(D972MRWords) or
   not IsString(D972MRReceipt) or not IsString(D972MROutput) or
   not IsBool(D972MRLarge) or not IsBool(D972MRFilestore) or
   not IsBool(D972MRDiff1) or not IsInt(D972MRMaxEqns) or
   not IsInt(D972MRMaxStates) or not IsInt(D972MRMaxWdiffs) or
   not IsList(D972MRMaxStored) or Length(D972MRMaxStored)<>2 or
   not ForAll(D972MRMaxStored,x->IsInt(x) and x>0) then
  Error("metabelian replay setting type drift");
fi;

D972MRSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972MRConstructorSha:="ae605e53f0a6823b6362ffe9e063cb9b4ea824ff1a28992c17da8706feb62576";;
D972MRRhoSha:="23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed";;
D972MRRelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972MRNormSha:="ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972MRWordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972MRRawRelSha:="29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e";;
D972MRNormRSSha:="f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8";;
D972MRRho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;
D972MRGenBits:=[1,2,4,8,16,31];;

D972MRJoin:=function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1]; for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;
D972MRJson:=function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\""); fi;
  if x=true then return "true"; fi; if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if not IsList(x) then Error("metabelian replay JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972MRJson(x[i]));
  return Concatenation("[",D972MRJoin(p,","),"]");
end;;
D972MRFreeReduce:=function(word)
  local out,x,n;
  out:=[];
  for x in word do
    n:=Length(out);
    if n>0 and out[n]=-x then Remove(out,n); else Add(out,x); fi;
  od;
  return out;
end;;
D972MRInverse:=function(word) return List(Reversed(word),x->-x); end;;
D972MRToggle:=function(mask,bit)
  if bit=31 then return 31-mask; fi;
  if QuoInt(mask,bit) mod 2=1 then return mask-bit; fi;
  return mask+bit;
end;;
D972MRTransversal:=function(mask)
  local out,bit;
  out:=[];
  for bit in [0..4] do
    if QuoInt(mask,2^bit) mod 2=1 then Add(out,bit+1); fi;
  od;
  return out;
end;;
D972MRSignedWord:=function(row,gens)
  local w,x;
  w:=One(gens[1]);
  for x in row do
    if x>0 then w:=w*gens[x]; else w:=w*gens[-x]^-1; fi;
  od;
  return w;
end;;
D972MRSignedObj:=function(w)
  local e,out,i,g,n,j;
  e:=ExtRepOfObj(w); out:=[]; i:=1;
  while i<=Length(e) do
    g:=e[i]; n:=e[i+1];
    if n>0 then for j in [1..n] do Add(out,g); od;
    else for j in [1..-n] do Add(out,-g); od; fi;
    i:=i+2;
  od;
  return out;
end;;
D972MRRhoMap:=function(word)
  local out,letter,img;
  out:=[];
  for letter in word do
    img:=D972MRRho[AbsInt(letter)];
    if letter<0 then img:=D972MRInverse(img); fi;
    out:=Concatenation(out,img);
  od;
  return D972MRFreeReduce(out);
end;;
D972MRExactNorm:=function(f2word)
  local j,letter,orbit,v,z,t;
  j:=[];
  for letter in f2word do
    if AbsInt(letter)=1 then Add(j,SignInt(letter)*1);
    elif AbsInt(letter)=2 then Add(j,SignInt(letter)*4);
    else Error("metabelian replay F2 alphabet drift"); fi;
  od;
  j:=D972MRFreeReduce(j); orbit:=[]; v:=j;
  for t in [1..5] do Add(orbit,v); v:=D972MRRhoMap(v); od;
  z:=[];
  for t in Reversed([1..5]) do z:=D972MRFreeReduce(Concatenation(z,orbit[t])); od;
  return z;
end;;
D972MRBuildRaw:=function(relators)
  local reps,pairId,pairWords,mask,gen,bit,raw,word,id,rs,start,rel;
  reps:=List([0..31],D972MRTransversal);
  pairId:=List([1..32],i->List([1..6],j->0));; pairWords:=[];
  for mask in [0..31] do
    for gen in [1..6] do
      bit:=D972MRGenBits[gen];
      raw:=Concatenation(reps[mask+1],[gen],
        D972MRInverse(reps[D972MRToggle(mask,bit)+1]));
      word:=D972MRFreeReduce(raw);
      if Length(word)>0 then Add(pairWords,word); id:=Length(pairWords);
        pairId[mask+1][gen]:=id; fi;
    od;
  od;
  rs:=[];
  for start in [0..31] do
    for rel in relators do
      word:=[];; mask:=start;
      for gen in rel do
        bit:=D972MRGenBits[AbsInt(gen)];
        if gen>0 then id:=pairId[mask+1][AbsInt(gen)]; if id>0 then Add(word,id); fi;
          mask:=D972MRToggle(mask,bit);
        else mask:=D972MRToggle(mask,bit); id:=pairId[mask+1][AbsInt(gen)];
          if id>0 then Add(word,-id); fi;
        fi;
      od;
      if mask<>start then Error("metabelian replay RS relator does not close"); fi;
      word:=D972MRFreeReduce(word); if Length(word)>0 then Add(rs,word); fi;
    od;
  od;
  return rec(pair_words:=pairWords,relators:=rs,transversal:=reps);
end;;

D972MRInputRaw:=StringFile(D972MRInput);;
if D972MRInputRaw=fail or HexSHA256(D972MRInputRaw)<>D972MRSourceSha then
  Error("metabelian replay canonical input SHA drift");
fi;
D972MRInputObj:=JsonStringToGap(D972MRInputRaw);;
if D972MRInputObj.schema<>"d972-b4-p2-magnus-input/v2" or
   D972MRInputObj.rho_words<>D972MRRho or Length(D972MRInputObj.all_relators)<>158 or
   D972MRInputObj.all_relators_sha256<>D972MRRelSha or
   HexSHA256(D972MRJson(D972MRInputObj.all_relators))<>D972MRRelSha then
   Error("metabelian replay canonical relator gate failed");
fi;
if HexSHA256(D972MRJson(D972MRRho))<>D972MRRhoSha then
  Error("metabelian replay rho digest drift");
fi;
D972MRWordsRaw:=StringFile(D972MRWords);;
if D972MRWordsRaw=fail or HexSHA256(D972MRWordsRaw)<>D972MRWordsSha then
  Error("metabelian replay word artifact SHA drift");
fi;
D972MRWordsObj:=JsonStringToGap(D972MRWordsRaw);;
if D972MRWordsObj.schema<>"d972-b4-word-key-artifact/v1" or
   D972MRWordsObj.count<>972 then
  Error("metabelian replay word artifact gate failed");
fi;
D972MRCanonicalRows:=[];;
for D972MRI in [1..972] do
  D972MRRawRow:=D972MRWordsObj.rows[D972MRI];;
  if not IsList(D972MRRawRow) or Length(D972MRRawRow)<>3 then
    Error("metabelian replay word artifact row shape drift");
  fi;
  D972MRWord:=D972MRRawRow[3];;
  ## [] is classified as a string by some GAP 4.16 predicates; test the
  ## empty list first, then accept legacy "" only at the two registered rows.
  if IsList(D972MRWord) and Length(D972MRWord)=0 and
     not IsStringRep(D972MRWord) then
    D972MRWord:=[];
  elif IsStringRep(D972MRWord) then
    if D972MRWord<>"" or (D972MRI<>1 and D972MRI<>892) then
      Error("metabelian replay unexpected legacy empty row");
    fi;
    D972MRWord:=[];
  elif not IsList(D972MRWord) then
    Error("metabelian replay word type drift");
  fi;
  Add(D972MRCanonicalRows,[D972MRRawRow[1],D972MRRawRow[2],D972MRWord]);
od;
if HexSHA256(D972MRJson(D972MRCanonicalRows))<>
   D972MRWordsObj.canonical_bytes_sha256 then
  Error("metabelian replay word artifact canonical digest drift");
fi;
D972MRNormOriginal:=[];;
for D972MRI in [1..972] do
  D972MRRow:=D972MRCanonicalRows[D972MRI][3];;
  Add(D972MRNormOriginal,D972MRExactNorm(D972MRRow));
od;
if HexSHA256(D972MRJson(D972MRNormOriginal))<>D972MRNormSha then
  Error("metabelian replay exact norm digest drift");
fi;
D972MRRaw:=D972MRBuildRaw(D972MRInputObj.all_relators);;
if Length(D972MRRaw.pair_words)<>161 or Length(D972MRRaw.relators)<>5056 or
   HexSHA256(D972MRJson(D972MRRaw.relators))<>D972MRRawRelSha then
  Error("metabelian replay raw RS digest drift");
fi;
## Build the pair-id table independently, then rewrite the exact F6 norms.
D972MRPairId:=List([1..32],i->List([1..6],j->0));; D972MRPairWords:=[];;
for D972MRMask in [0..31] do
  for D972MRGen in [1..6] do
    D972MRBit:=D972MRGenBits[D972MRGen];;
    D972MRWord:=D972MRFreeReduce(Concatenation(
      D972MRRaw.transversal[D972MRMask+1],[D972MRGen],
      D972MRInverse(D972MRRaw.transversal[D972MRToggle(D972MRMask,D972MRBit)+1])));;
    if Length(D972MRWord)>0 then Add(D972MRPairWords,D972MRWord);
      D972MRPairId[D972MRMask+1][D972MRGen]:=Length(D972MRPairWords); fi;
  od;
od;
D972MRRewrite:=function(word)
  local out,mask,letter,bit,id;
  out:=[];; mask:=0;
  for letter in word do
    bit:=D972MRGenBits[AbsInt(letter)];;
    if letter>0 then id:=D972MRPairId[mask+1][AbsInt(letter)];;
      if id>0 then Add(out,id); fi; mask:=D972MRToggle(mask,bit);
    else mask:=D972MRToggle(mask,bit); id:=D972MRPairId[mask+1][AbsInt(letter)];;
      if id>0 then Add(out,-id); fi;
    fi;
  od;
  if mask<>0 then Error("metabelian replay norm does not close"); fi;
  return D972MRFreeReduce(out);
end;;
D972MRNormRows:=List(D972MRNormOriginal,D972MRRewrite);;
if HexSHA256(D972MRJson(D972MRNormRows))<>D972MRNormRSSha then
  Error("metabelian replay norm RS digest drift");
fi;

D972MRReceiptRaw:=StringFile(D972MRReceipt);;
if D972MRReceiptRaw=fail then Error("metabelian replay producer receipt missing"); fi;
D972MRObj:=JsonStringToGap(D972MRReceiptRaw);;
if D972MRObj.schema<>"d972-b4-u-metabelian-kbmag/v1" or
   D972MRObj.source_sha256<>D972MRSourceSha or D972MRObj.rs_constructor_sha256<>D972MRConstructorSha or
   D972MRObj.rho_words_sha256<>D972MRRhoSha or D972MRObj.relator_sha256<>D972MRRelSha or
   D972MRObj.word_artifact_sha256<>D972MRWordsSha or
   D972MRObj.norm_original_sha256<>D972MRNormSha or
   D972MRObj.raw_rs_relators_sha256<>D972MRRawRelSha or
   D972MRObj.norm_rs_sha256<>D972MRNormRSSha or
   D972MRObj.raw_rs_generator_count<>161 or D972MRObj.raw_rs_relator_count<>5056 or
   D972MRObj.norm_count<>972 or D972MRObj.automatic_success<>true or
   D972MRObj.gpgenmult_rechecked<>true or D972MRObj.gpcheckmult_rechecked<>true or
   D972MRObj.gpaxioms_rechecked<>true or
   D972MRObj.large<>D972MRLarge or D972MRObj.filestore<>D972MRFilestore or
   D972MRObj.diff1<>D972MRDiff1 then
  Error("metabelian replay producer receipt gate failed");
fi;
if Length(D972MRObj.automaton_paths)<>Length(D972MRObj.automaton_names) or
   Length(D972MRObj.automaton_paths)<>Length(D972MRObj.automaton_states) or
   Length(D972MRObj.automaton_paths)<>Length(D972MRObj.automaton_sha256) or
   D972MRObj.automaton_names<>["wa","diff1","diff2"] and
   D972MRObj.automaton_names<>["wa","diff1","diff2","reduction"] then
  Error("metabelian replay automaton ledger drift");
fi;
if Length(D972MRObj.automaton_names)=3 and
   D972MRObj.automaton_bindings<>["D972MCWA","D972MCDiff1FSA","D972MCDiff2FSA"] then
  Error("metabelian replay automaton bindings drift");
fi;
if Length(D972MRObj.automaton_names)=4 and
   D972MRObj.automaton_bindings<>["D972MCWA","D972MCDiff1FSA",
     "D972MCDiff2FSA","D972MCReductionFSA"] then
  Error("metabelian replay reduction binding drift");
fi;
for D972MRI in [1..Length(D972MRObj.automaton_paths)] do
  D972MRFsaRaw:=StringFile(D972MRObj.automaton_paths[D972MRI]);;
  if D972MRFsaRaw=fail or HexSHA256(D972MRFsaRaw)<>D972MRObj.automaton_sha256[D972MRI] then
    Error("metabelian replay FSA SHA drift");
  fi;
  Read(D972MRObj.automaton_paths[D972MRI]);;
od;
if not IsBound(D972MCWA) or not IsBound(D972MCDiff1FSA) or
   not IsBound(D972MCDiff2FSA) then Error("metabelian replay FSA bindings missing"); fi;

D972MRF:=FreeGroup(161,"kraw_replay");; D972MRG:=GeneratorsOfGroup(D972MRF);;
D972MRRelWords:=List(D972MRRaw.relators,w->D972MRSignedWord(w,D972MRG));;
D972MRK:=D972MRF/D972MRRelWords;; D972MRKG:=GeneratorsOfGroup(D972MRK);;
if D972MRObj.abelian_invariants<>List([1..10],x->9) then
  Error("metabelian replay receipt is not pinned to C9^10");
fi;
if AbelianInvariants(D972MRK)<>D972MRObj.abelian_invariants then
  Error("metabelian replay abelian invariant drift");
fi;
D972MRRws:=KBMAGRewritingSystem(D972MRK);; SetOrderingOfKBMAGRewritingSystem(D972MRRws,"shortlex");;
D972MRRws!.wa:=D972MCWA;; D972MRRws!.diff1:=D972MCDiff1FSA;; D972MRRws!.diff2:=D972MCDiff2FSA;;
if Length(D972MRObj.automaton_names)=4 then
  if not IsBound(D972MCReductionFSA) then Error("metabelian replay reduction FSA missing"); fi;
  D972MRRws!.reductionFSA:=D972MCReductionFSA;
fi;
D972MROpts:=OptionsRecordOfKBMAGRewritingSystem(D972MRRws);;
D972MROpts.maxeqns:=D972MRMaxEqns;; D972MROpts.maxstates:=D972MRMaxStates;;
D972MROpts.maxwdiffs:=D972MRMaxWdiffs;; D972MROpts.maxstoredlen:=D972MRMaxStored;;
D972MRGpGen:=GpGenMult(D972MRRws,D972MRLarge,D972MRFilestore);;
D972MRGpCheck:=GpCheckMult(D972MRRws,D972MRLarge,D972MRFilestore);;
D972MRAxioms:=GpAxioms(D972MRRws,D972MRLarge,D972MRFilestore);;
if D972MRGpGen<>true or D972MRGpCheck<>true or D972MRAxioms<>true then
  Error("metabelian replay GpAxioms gate failed");
fi;
Print("B4_METABELIAN_REPLAY_GPAXIOMS_PASS gpgenmult=true gpcheckmult=true gpaxioms=true\n");

D972MRCommBits:=[];; D972MRNormBits:=[];; D972MRCommBad:=[];; D972MRNormBad:=[];;
for D972MRI in [1..160] do
  for D972MRJ in [D972MRI+1..161] do
    D972MRZ:=ReducedForm(D972MRRws,D972MRKG[D972MRI]*D972MRKG[D972MRJ]*
      D972MRKG[D972MRI]^-1*D972MRKG[D972MRJ]^-1);;
    Add(D972MRCommBits,IsOne(D972MRZ));;
    if not IsOne(D972MRZ) and Length(D972MRCommBad)=0 then
      Add(D972MRCommBad,[D972MRI,D972MRJ,D972MRSignedObj(D972MRZ)]); fi;
  od;
od;
for D972MRI in [1..972] do
  D972MRZ:=ReducedForm(D972MRRws,D972MRSignedWord(D972MRNormRows[D972MRI],D972MRKG));;
  Add(D972MRNormBits,IsOne(D972MRZ));;
  if not IsOne(D972MRZ) and Length(D972MRNormBad)=0 then
    Add(D972MRNormBad,[D972MRI,D972MRNormRows[D972MRI],D972MRSignedObj(D972MRZ)]); fi;
od;
if D972MRObj.commutator_ledger<>D972MRCommBits or D972MRObj.norm_ledger<>D972MRNormBits then
  Error("metabelian replay ledgers differ from producer");
fi;
D972MRCommEmpty:=Number(D972MRCommBits,x->x=true);;
D972MRNormEmpty:=Number(D972MRNormBits,x->x=true);;
if D972MRCommEmpty<>12880 then D972MRStatus:="UNKNOWN_K_NONABELIAN_REPLAYED";
elif D972MRNormEmpty<972 then D972MRStatus:="B4_A_CANDIDATE_METABELIAN_REPLAYED";
else D972MRStatus:="B4_B_TERMINAL_CANDIDATE_METABELIAN_REPLAYED"; fi;
D972MROut:=Concatenation(
  "{\"schema\":\"d972-b4-u-metabelian-kbmag-replay/v1\",\"status\":\"",
  D972MRStatus,"\",\"producer_receipt_sha256\":\"",HexSHA256(D972MRReceiptRaw),
  "\",\"source_sha256\":\"",D972MRSourceSha,"\",\"rs_constructor_sha256\":\"",D972MRConstructorSha,
  "\",\"rho_words_sha256\":\"",D972MRRhoSha,"\",\"relator_sha256\":\"",D972MRRelSha,
  "\",\"norm_original_sha256\":\"",D972MRNormSha,"\",\"norm_count\":972,",
  "\"commutator_count\":12880,\"commutator_empty_count\":",String(D972MRCommEmpty),
  ",\"norm_empty_count\":",String(D972MRNormEmpty),
  ",\"commutator_ledger_sha256\":\"",HexSHA256(D972MRJson(D972MRCommBits)),
  "\",\"norm_ledger_sha256\":\"",HexSHA256(D972MRJson(D972MRNormBits)),
  "\",\"gpgenmult_rechecked\":true,\"gpcheckmult_rechecked\":true,",
  "\"gpaxioms_rechecked\":true,\"automata_replayed\":true,",
  "\"proof_level\":\"DIRECT_GPAxioms_FSA_REPLAY_PENDING_LEAN\"}");;
D972MRFout:=OutputTextFile(D972MROutput,false);; SetPrintFormattingStatus(D972MRFout,false);
PrintTo(D972MRFout,Concatenation(D972MROut,"\n"));; CloseStream(D972MRFout);
Print("B4_METABELIAN_REPLAY_FINAL_MARKER output=",D972MROutput,
  " status=",D972MRStatus," comm_empty=",D972MRCommEmpty,
  "/12880 norm_empty=",D972MRNormEmpty,"/972\n");
