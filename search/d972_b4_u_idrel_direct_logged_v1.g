#############################################################################
## d972_b4_u_idrel_direct_logged_v1.g
##
## Proof-producing, bounded IdRel lane for the frozen six-generator,
## 158-relator presentation U.  This file deliberately does not call the
## package's unbounded convenience completion helpers: each requested pass
## is explicit and is checked against externally supplied caps.
##
## A stage record contains, for each of the 486 unique exact norms, the
## reduced word and the IdRel log.  The log is converted from IdRel's monoid
## words to signed words in the original six generators.  The producer checks
## in the original free group that
##
##   product(rel_i^conjugator) * reduced = original norm.
##
## The Python checker repeats this equality without GAP.  A nonidentity
## reduced word is never an A witness: bounded rewriting is only UNKNOWN.
## B4_B_DIRECT_LOGGED_TERMINAL is emitted only when all 486 unique rows (and
## their complete 972-row duplicate map) reduce to the identity.
#############################################################################

if LoadPackage("json") <> true then
  Error("B4 IdRel direct: json package unavailable");
fi;
if LoadPackage("idrel") <> true then
  Error("B4 IdRel direct: idrel package unavailable");
fi;

D972IDLInput := "search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972IDLWords := "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972IDLOutput := Filename(DirectoryTemporary(),
  "d972_b4_u_idrel_direct_logged_v1.json");;
D972IDLMaxPasses := 1;;
D972IDLMaxRules := 20000;;
D972IDLMaxLogLength := 8192;;
D972IDLMaxConjugatorLength := 16384;;
D972IDLMaxLogLetters := 200000;;
D972IDLMaxReducedLength := 4096;;
D972IDLMaxWallMs := 1800000;;
if IsBound(D972_B4_IDREL_INPUT) then D972IDLInput := D972_B4_IDREL_INPUT; fi;
if IsBound(D972_B4_IDREL_WORDS) then D972IDLWords := D972_B4_IDREL_WORDS; fi;
if IsBound(D972_B4_IDREL_OUTPUT) then D972IDLOutput := D972_B4_IDREL_OUTPUT; fi;
if IsBound(D972_B4_IDREL_MAX_PASSES) then
  D972IDLMaxPasses := D972_B4_IDREL_MAX_PASSES;
fi;
if IsBound(D972_B4_IDREL_MAX_RULES) then
  D972IDLMaxRules := D972_B4_IDREL_MAX_RULES;
fi;
if IsBound(D972_B4_IDREL_MAX_LOG_LENGTH) then
  D972IDLMaxLogLength := D972_B4_IDREL_MAX_LOG_LENGTH;
fi;
if IsBound(D972_B4_IDREL_MAX_CONJUGATOR_LENGTH) then
  D972IDLMaxConjugatorLength := D972_B4_IDREL_MAX_CONJUGATOR_LENGTH;
fi;
if IsBound(D972_B4_IDREL_MAX_LOG_LETTERS) then
  D972IDLMaxLogLetters := D972_B4_IDREL_MAX_LOG_LETTERS;
fi;
if IsBound(D972_B4_IDREL_MAX_REDUCED_LENGTH) then
  D972IDLMaxReducedLength := D972_B4_IDREL_MAX_REDUCED_LENGTH;
fi;
if IsBound(D972_B4_IDREL_MAX_WALL_MS) then
  D972IDLMaxWallMs := D972_B4_IDREL_MAX_WALL_MS;
fi;

D972IDLSourceSha :=
  "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972IDLWordsSha :=
  "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972IDLRelSha :=
  "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972IDLRoofSha :=
  "3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8";;
D972IDLTargetSha :=
  "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
D972IDLNormSha :=
  "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e";;
D972IDLWordCanonicalSha :=
  "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930";;

D972IDLJoin := function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1];
  for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;

## JSON serializer for the scalar/list data used by the receipt.  Check the
## empty-list case before IsString: GAP 4.16 regards [] as IsString.
D972IDLJson := function(x)
  local p,i,t;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if IsInt(x) then return String(x); fi;
  if IsString(x) then
    t:=ReplacedString(x,"\\","\\\\");
    t:=ReplacedString(t,"\"","\\\"");
    return Concatenation("\"",t,"\"");
  fi;
  if not IsList(x) then Error("B4 IdRel JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972IDLJson(x[i]));
  return Concatenation("[",D972IDLJoin(p,","),"]");
end;;

D972IDLWrite := function(path,text)
  local out;
  out:=OutputTextFile(path,false);
  SetPrintFormattingStatus(out,false);
  PrintTo(out,text);
  CloseStream(out);
end;;

D972IDLFreeReduce := function(word)
  local out,x,n;
  out:=[];
  for x in word do
    n:=Length(out);
    if n>0 and out[n]=-x then Remove(out,n); else Add(out,x); fi;
  od;
  return out;
end;;
D972IDLInverse := function(word)
  return List(Reversed(word),x->-x);
end;;
D972IDLWord := function(row,gens)
  local w,x;
  w:=One(gens[1]);
  for x in row do
    if x>0 then w:=w*gens[x]; else w:=w*gens[-x]^-1; fi;
  od;
  return w;
end;;
D972IDLToggleFree := function(word,gens)
  local w,x;
  w:=[];
  for x in word do
    if x>0 then Add(w,gens[x]); else Add(w,-gens[-x]); fi;
  od;
  return D972IDLFreeReduce(w);
end;;

D972IDLRhoWord := function(word,rho)
  local out,x,v;
  out:=[];
  for x in word do
    v:=rho[AbsInt(x)];
    if x<0 then v:=D972IDLInverse(v); fi;
    out:=D972IDLFreeReduce(Concatenation(out,v));
  od;
  return out;
end;;
D972IDLExactNorm := function(f2,rho)
  local j,x,v,orbit,t,out;
  j:=[];
  for x in f2 do
    if AbsInt(x)=1 then Add(j,SignInt(x)*1);
    elif AbsInt(x)=2 then Add(j,SignInt(x)*4);
    else Error("B4 IdRel F2 norm alphabet drift"); fi;
  od;
  j:=D972IDLFreeReduce(j);
  orbit:=[]; v:=j;
  for t in [1..5] do Add(orbit,v); v:=D972IDLRhoWord(v,rho); od;
  out:=[];
  for t in Reversed([1..5]) do
    out:=D972IDLFreeReduce(Concatenation(out,orbit[t]));
  od;
  return out;
end;;

## Signed words in the original alphabet are represented by positive monoid
## generators according to ArrangementOfMonoidGenerators.  This avoids any
## dependence on GAP's printed names or on ExtRep's inverse convention.
D972IDLMonWord := function(row,monGens,arrangement)
  local w,x,p;
  w:=One(monGens[1]);
  for x in row do
    p:=Position(arrangement,x);
    if p=fail then Error("B4 IdRel monoid arrangement drift"); fi;
    w:=w*monGens[p];
  od;
  return w;
end;;
D972IDLMonSigned := function(word,arrangement)
  local ext,out,i,g,n,j,base;
  ext:=ExtRepOfObj(word); out:=[]; i:=1;
  while i<=Length(ext) do
    g:=ext[i]; n:=ext[i+1];
    base:=arrangement[AbsInt(g)];
    if g<0 then base:=-base; fi;
    if n>0 then
      for j in [1..n] do Add(out,base); od;
    else
      for j in [1..-n] do Add(out,-base); od;
    fi;
    i:=i+2;
  od;
  return D972IDLFreeReduce(out);
end;;

D972IDLInputText:=StringFile(D972IDLInput);;
if D972IDLInputText=fail or HexSHA256(D972IDLInputText)<>D972IDLSourceSha then
  Error("B4 IdRel canonical input source SHA drift");
fi;
D972IDLObj:=JsonStringToGap(D972IDLInputText);;
if not IsRecord(D972IDLObj) or D972IDLObj.schema<>"d972-b4-p2-magnus-input/v2" or
   D972IDLObj.relator_count<>158 or D972IDLObj.roof_count<>972 or
   Length(D972IDLObj.all_relators)<>158 or Length(D972IDLObj.roof_words)<>972 or
   D972IDLObj.all_relators_sha256<>D972IDLRelSha or
   D972IDLObj.roof_words_sha256<>D972IDLRoofSha or
   D972IDLObj.target_key_digest<>D972IDLTargetSha or
   HexSHA256(D972IDLJson(D972IDLObj.all_relators))<>D972IDLRelSha or
   HexSHA256(D972IDLJson(D972IDLObj.roof_words))<>D972IDLRoofSha then
  Error("B4 IdRel canonical input gate failed");
fi;
D972IDLWordText:=StringFile(D972IDLWords);;
if D972IDLWordText=fail or HexSHA256(D972IDLWordText)<>D972IDLWordsSha then
  Error("B4 IdRel word artifact SHA drift");
fi;
D972IDLWordObj:=JsonStringToGap(D972IDLWordText);;
if not IsRecord(D972IDLWordObj) or
   D972IDLWordObj.schema<>"d972-b4-word-key-artifact/v1" or
   D972IDLWordObj.count<>972 or Length(D972IDLWordObj.rows)<>972 or
   D972IDLWordObj.source_target_key_digest<>D972IDLTargetSha or
   D972IDLWordObj.canonical_bytes_sha256<>D972IDLWordCanonicalSha then
  Error("B4 IdRel word artifact gate failed");
fi;
for D972IDLI in [1..972] do
  ## In GAP's 1-based indexing row[3] is the third JSON component: f2 word.
  if not IsList(D972IDLWordObj.rows[D972IDLI]) or
     Length(D972IDLWordObj.rows[D972IDLI])<>3 or
     D972IDLWordObj.rows[D972IDLI][3]<>D972IDLObj.roof_words[D972IDLI] then
    Error("B4 IdRel word/roof row drift at ",D972IDLI);
  fi;
od;

for D972IDLR in D972IDLObj.all_relators do
  if ForAny(D972IDLR,x->not IsInt(x) or x=0 or AbsInt(x)>6) then
    Error("B4 IdRel relator alphabet drift");
  fi;
od;

D972IDLNormAll:=List(D972IDLObj.roof_words,
  w->D972IDLExactNorm(w,D972IDLObj.rho_words));;
if HexSHA256(D972IDLJson(D972IDLNormAll))<>D972IDLNormSha then
  Error("B4 IdRel exact norm digest drift");
fi;
D972IDLNormUnique:=[]; D972IDLNormMap:=[];
for D972IDLI in [1..Length(D972IDLNormAll)] do
  D972IDLPos:=Position(D972IDLNormUnique,D972IDLNormAll[D972IDLI]);
  if D972IDLPos=fail then
    Add(D972IDLNormUnique,D972IDLNormAll[D972IDLI]);
    D972IDLPos:=Length(D972IDLNormUnique);
  fi;
  Add(D972IDLNormMap,D972IDLPos);
od;
if Length(D972IDLNormUnique)<>486 or Length(D972IDLNormMap)<>972 then
  Error("B4 IdRel unique norm count drift");
fi;

## Construct exactly U=<F_6 | the 158 frozen relators>.
D972IDLFreeF:=FreeGroup(6,"u");;
D972IDLFreeG:=GeneratorsOfGroup(D972IDLFreeF);;
D972IDLRelFree:=List(D972IDLObj.all_relators,
  w->D972IDLWord(w,D972IDLFreeG));;
D972IDLU:=D972IDLFreeF/D972IDLRelFree;;
D972IDLMon:=MonoidPresentationFpGroup(D972IDLU);;
D972IDLMonF:=FreeGroupOfPresentation(D972IDLMon);;
D972IDLMonG:=GeneratorsOfGroup(D972IDLMonF);;
D972IDLArrangement:=ArrangementOfMonoidGenerators(D972IDLU);;
if D972IDLArrangement<>Concatenation([1..6],[-1,-2,-3,-4,-5,-6]) or
   Length(D972IDLMonG)<>12 then
  Error("B4 IdRel monoid arrangement is not canonical");
fi;
D972IDLMonNorms:=List(D972IDLNormUnique,
  w->D972IDLMonWord(w,D972IDLMonG,D972IDLArrangement));;
D972IDLFreeNorms:=List(D972IDLNormUnique,w->D972IDLWord(w,D972IDLFreeG));;

D972IDLRuleCapOK:=function(rules)
  local r,e,total;
  if Length(rules)>D972IDLMaxRules then return false; fi;
  for r in rules do
    if not IsList(r) or Length(r)<>3 then return false; fi;
    total:=0;
    for e in r[2] do
      if Length(e)<>2 or Length(e[2])>D972IDLMaxConjugatorLength then
        return false;
      fi;
      total:=total+Length(e[2]);
    od;
    if total>D972IDLMaxLogLetters then return false; fi;
    if Length(r[1])>D972IDLMaxReducedLength or
       Length(r[3])>D972IDLMaxReducedLength or
       Length(r[2])>D972IDLMaxLogLength then return false; fi;
  od;
  return true;
end;;
D972IDLLogBudgetOK:=function(log)
  local e,total;
  if Length(log)>D972IDLMaxLogLength then return false; fi;
  total:=0;
  for e in log do
    if Length(e)<>2 or Length(e[2])>D972IDLMaxConjugatorLength then
      return false;
    fi;
    total:=total+Length(e[2]);
  od;
  return total<=D972IDLMaxLogLetters;
end;;
D972IDLLogSigned:=function(log)
  local out,e,idx;
  out:=[];
  for e in log do
    if not IsList(e) or Length(e)<>2 or not IsInt(e[1]) or
       e[1]=0 or AbsInt(e[1])>158 then
      Error("B4 IdRel unexpected log relator index");
    fi;
    idx:=e[1];
    Add(out,[idx,D972IDLMonSigned(e[2],D972IDLArrangement)]);
  od;
  return out;
end;;
D972IDLCheckProof:=function(original,red,log)
  local lhs,e,idx,rel,conj;
  lhs:=One(D972IDLFreeF);
  for e in log do
    idx:=e[1]; rel:=D972IDLRelFree[AbsInt(idx)];
    if idx<0 then rel:=rel^-1; fi;
    conj:=D972IDLWord(e[2],D972IDLFreeG);
    lhs:=lhs*(rel^conj);
  od;
  lhs:=lhs*D972IDLWord(red,D972IDLFreeG);
  return lhs=D972IDLWord(original,D972IDLFreeG);
end;;

## IdRel 2.49's type-1 construction has a documented log-invariant risk.  Do
## not pass a rule to the next API (or use it for a norm reduction) until its
## actual monoid words have been replayed in F6.  Invalid rules are filtered,
## never repaired or silently counted as proofs.  The audit records only their
## indices and a digest, so a malformed/oversized rule is not serialized.
D972IDLRuleFreeValid:=function(r)
  local signedLhs,signedRhs,signedLog,e;
  if not IsList(r) or Length(r)<>3 then return false; fi;
  if not IsList(r[2]) then return false; fi;
  if Length(r[2])>D972IDLMaxLogLength then return false; fi;
  for e in r[2] do
    if not IsList(e) or Length(e)<>2 or not IsInt(e[1]) or e[1]=0 or
       AbsInt(e[1])>158 or Length(e[2])>D972IDLMaxConjugatorLength then
      return false;
    fi;
  od;
  signedLhs:=D972IDLMonSigned(r[1],D972IDLArrangement);
  signedRhs:=D972IDLMonSigned(r[3],D972IDLArrangement);
  signedLog:=D972IDLLogSigned(r[2]);
  return D972IDLCheckProof(signedLhs,signedRhs,signedLog);
end;;
D972IDLFilterAudit:=[];;
D972IDLFilterRules:=function(stage,phase,rules)
  local good,bad,i,digest;
  good:=[]; bad:=[];
  for i in [1..Length(rules)] do
    if D972IDLRuleFreeValid(rules[i]) then Add(good,rules[i]);
    else Add(bad,i);
    fi;
  od;
  digest:=HexSHA256(D972IDLJson(bad));
  Add(D972IDLFilterAudit,rec(stage:=stage,phase:=phase,
    invalid_count:=Length(bad),invalid_digest:=digest));
  return good;
end;;
D972IDLFilterAuditJson:=function()
  local out,a;
  out:=[];
  for a in D972IDLFilterAudit do
    Add(out,Concatenation(
      "{\"stage\":",String(a.stage),
      ",\"phase\":",D972IDLJson(a.phase),
      ",\"invalid_count\":",String(a.invalid_count),
      ",\"invalid_digest\":",D972IDLJson(a.invalid_digest),"}"));
  od;
  return Concatenation("[",D972IDLJoin(out,","),"]");
end;;

D972IDLStartRuntime:=Runtime();;
D972IDLStageFailure:="";;
D972IDLStageRowJson:=function(R)
  return Concatenation(
    "{\"unique_index\":",String(R.unique_index),
    ",\"original\":",D972IDLJson(R.original),
    ",\"reduced\":",D972IDLJson(R.reduced),
    ",\"log\":",D972IDLJson(R.log),
    ",\"log_length\":",String(R.log_length),
    ",\"total_log_letters\":",String(R.total_log_letters),
    ",\"identity\":",D972IDLJson(R.identity),"}");
end;;
D972IDLStageJson:=function(stage,status,rules,rows,elapsed)
  local rr;
  rr:=List(rows,D972IDLStageRowJson);
  return Concatenation(
    "{\"schema\":\"d972-b4-u-idrel-direct-logged-stage/v1\"",
    ",\"stage\":",String(stage),",\"status\":",D972IDLJson(status),
    ",\"source_sha256\":",D972IDLJson(D972IDLSourceSha),
    ",\"relator_sha256\":",D972IDLJson(D972IDLRelSha),
    ",\"norm_sha256\":",D972IDLJson(D972IDLNormSha),
    ",\"generator_count\":6,\"relator_count\":158",
    ",\"rule_count\":",String(Length(rules)),
    ",\"max_rules\":",String(D972IDLMaxRules),
    ",\"max_log_length\":",String(D972IDLMaxLogLength),
    ",\"max_conjugator_length\":",String(D972IDLMaxConjugatorLength),
    ",\"max_log_letters\":",String(D972IDLMaxLogLetters),
    ",\"max_reduced_length\":",String(D972IDLMaxReducedLength),
    ",\"elapsed_ms\":",String(elapsed),
    ",\"filter_audit\":",D972IDLFilterAuditJson(),
    ",\"completed_unique_count\":",String(Length(rows)),
    ",\"rows\":[",D972IDLJoin(rr,","),"]}");
end;;

D972IDLReduceStage:=function(stage,rules)
  local rows,u,ans,log,red,redSigned,signedLog,ok,elapsed,R,status;
  rows:=[]; D972IDLStageFailure:="";;
  for u in [1..Length(D972IDLNormUnique)] do
    if Runtime()-D972IDLStartRuntime>D972IDLMaxWallMs then
      D972IDLStageFailure:="UNKNOWN_INTERNAL_WALL_CAP"; break;
    fi;
    ans:=LoggedReduceWordKB(D972IDLMonNorms[u],rules);;
    log:=ans[1]; red:=ans[2];
    if not D972IDLLogBudgetOK(log) then
      D972IDLStageFailure:="UNKNOWN_LOG_BUDGET_CAP"; break;
    fi;
    redSigned:=D972IDLMonSigned(red,D972IDLArrangement);
    if Length(redSigned)>D972IDLMaxReducedLength then
      D972IDLStageFailure:="UNKNOWN_REDUCED_LENGTH_CAP"; break;
    fi;
    signedLog:=D972IDLLogSigned(log);;
    ok:=D972IDLCheckProof(D972IDLNormUnique[u],redSigned,signedLog);
    if not ok then D972IDLStageFailure:="UNKNOWN_LOG_PROOF_MISMATCH"; break; fi;
    R:=rec(unique_index:=u,original:=D972IDLNormUnique[u],reduced:=redSigned,
      log:=signedLog,log_length:=Length(signedLog),
      total_log_letters:=Sum(List(signedLog,e->Length(e[2]))),
      identity:=Length(redSigned)=0);
    Add(rows,R);
  od;
  elapsed:=Runtime()-D972IDLStartRuntime;
  if D972IDLStageFailure="" and Length(rows)=Length(D972IDLNormUnique) then
    status:="COMPLETE";
  else
    if D972IDLStageFailure="" then D972IDLStageFailure:="UNKNOWN_STAGE_PARTIAL"; fi;
    status:=D972IDLStageFailure;
  fi;
  D972IDLWrite(Concatenation(D972IDLOutput,".stage",String(stage),".json"),
    D972IDLStageJson(stage,status,rules,rows,elapsed));
  return rec(rows:=rows,status:=status,elapsed_ms:=elapsed,
    rule_count:=Length(rules));
end;;

## Stage zero is always recorded.  Subsequent stages are explicit bounded
## calls, never the unbounded convenience attribute.
D972IDLStagePaths:=[]; D972IDLStageResults:=[];
D972IDLRules:=InitialLoggedRulesOfPresentation(D972IDLMon);;
if not D972IDLRuleCapOK(D972IDLRules) then
  D972IDLStageFailure:="UNKNOWN_INITIAL_RULE_CAP";
  D972IDLStage0:=rec(rows:=[],status:=D972IDLStageFailure,elapsed_ms:=0,
    rule_count:=Length(D972IDLRules));
  D972IDLWrite(Concatenation(D972IDLOutput,".stage0.json"),
     D972IDLStageJson(0,D972IDLStageFailure,D972IDLRules,[],0));
else
  D972IDLRules:=D972IDLFilterRules(0,"initial",D972IDLRules);;
  D972IDLStage0:=D972IDLReduceStage(0,D972IDLRules);
fi;
Add(D972IDLStagePaths,Concatenation(D972IDLOutput,".stage0.json"));
Add(D972IDLStageResults,D972IDLStage0);

D972IDLTerminal:=false; D972IDLLast:=D972IDLStage0;;
if D972IDLStage0.status="COMPLETE" and
   ForAll(D972IDLStage0.rows,R->R.identity) then D972IDLTerminal:=true; fi;

for D972IDLPass in [1..D972IDLMaxPasses] do
  if D972IDLTerminal or D972IDLLast.status<>"COMPLETE" then break; fi;
  if Runtime()-D972IDLStartRuntime>D972IDLMaxWallMs then break; fi;
  ## This is the bounded pass call requested by the lane contract.
  D972IDLNext:=LoggedOnePassKB(D972IDLMon,D972IDLRules);;
  if not D972IDLRuleCapOK(D972IDLNext) then
    D972IDLLast:=rec(rows:=[],status:="UNKNOWN_RULE_CAP",elapsed_ms:=
      Runtime()-D972IDLStartRuntime,rule_count:=Length(D972IDLNext));
    D972IDLWrite(Concatenation(D972IDLOutput,".stage",String(D972IDLPass),".json"),
      D972IDLStageJson(D972IDLPass,D972IDLLast.status,D972IDLNext,[],
        D972IDLLast.elapsed_ms));
    Add(D972IDLStagePaths,Concatenation(D972IDLOutput,".stage",String(D972IDLPass),".json"));
    Add(D972IDLStageResults,D972IDLLast); break;
  fi;
  D972IDLNext:=D972IDLFilterRules(D972IDLPass,"onepass",D972IDLNext);;
  ## Rewrite reduction is separately bounded; no completion wrapper.
  D972IDLNext:=LoggedRewriteReduce(D972IDLMon,D972IDLNext);;
  if not D972IDLRuleCapOK(D972IDLNext) then
    D972IDLLast:=rec(rows:=[],status:="UNKNOWN_RULE_CAP_AFTER_REWRITE",elapsed_ms:=
      Runtime()-D972IDLStartRuntime,rule_count:=Length(D972IDLNext));
    D972IDLWrite(Concatenation(D972IDLOutput,".stage",String(D972IDLPass),".json"),
      D972IDLStageJson(D972IDLPass,D972IDLLast.status,D972IDLNext,[],
        D972IDLLast.elapsed_ms));
    Add(D972IDLStagePaths,Concatenation(D972IDLOutput,".stage",String(D972IDLPass),".json"));
    Add(D972IDLStageResults,D972IDLLast); break;
  fi;
  D972IDLNext:=D972IDLFilterRules(D972IDLPass,"rewrite",D972IDLNext);;
  D972IDLRules:=D972IDLNext;;
  D972IDLLast:=D972IDLReduceStage(D972IDLPass,D972IDLRules);
  Add(D972IDLStagePaths,Concatenation(D972IDLOutput,".stage",String(D972IDLPass),".json"));
  Add(D972IDLStageResults,D972IDLLast);
  if D972IDLLast.status="COMPLETE" and
     ForAll(D972IDLLast.rows,R->R.identity) then D972IDLTerminal:=true; fi;
od;

D972IDLStatus:="UNKNOWN_IDREL_BOUNDED";;
if D972IDLTerminal then
  D972IDLStatus:="B4_B_DIRECT_LOGGED_TERMINAL";
elif D972IDLLast.status<>"COMPLETE" then
  D972IDLStatus:=D972IDLLast.status;
elif D972IDLMaxPasses=0 then
  D972IDLStatus:="UNKNOWN_PASS_CAP";
fi;
D972IDLStageMeta:=[];
for D972IDLJ in [1..Length(D972IDLStageResults)] do
  Add(D972IDLStageMeta,Concatenation(
    "{\"stage\":",String(D972IDLJ-1),
    ",\"artifact\":",D972IDLJson(D972IDLStagePaths[D972IDLJ]),
    ",\"status\":",D972IDLJson(D972IDLStageResults[D972IDLJ].status),
    ",\"rule_count\":",String(D972IDLStageResults[D972IDLJ].rule_count),
    ",\"elapsed_ms\":",String(D972IDLStageResults[D972IDLJ].elapsed_ms),"}"));
od;
D972IDLFinal:=Concatenation(
  "{\"schema\":\"d972-b4-u-idrel-direct-logged/v1\"",
  ",\"status\":",D972IDLJson(D972IDLStatus),
  ",\"proof_level\":\"F6_FREE_GROUP_LOG_REPLAY_CANDIDATE\"",
  ",\"source_sha256\":",D972IDLJson(D972IDLSourceSha),
  ",\"word_artifact_sha256\":",D972IDLJson(D972IDLWordsSha),
  ",\"relator_sha256\":",D972IDLJson(D972IDLRelSha),
  ",\"roof_word_sha256\":",D972IDLJson(D972IDLRoofSha),
  ",\"target_key_sha256\":",D972IDLJson(D972IDLTargetSha),
  ",\"norm_sha256\":",D972IDLJson(D972IDLNormSha),
  ",\"generator_count\":6,\"relator_count\":158",
  ",\"norm_count\":972,\"unique_norm_count\":486",
  ",\"duplicate_map\":",D972IDLJson(D972IDLNormMap),
  ",\"caps\":{\"max_passes\":",String(D972IDLMaxPasses),
    ",\"max_rules\":",String(D972IDLMaxRules),
    ",\"max_log_length\":",String(D972IDLMaxLogLength),
    ",\"max_conjugator_length\":",String(D972IDLMaxConjugatorLength),
     ",\"max_log_letters\":",String(D972IDLMaxLogLetters),
     ",\"max_reduced_length\":",String(D972IDLMaxReducedLength),
     ",\"max_wall_ms\":",String(D972IDLMaxWallMs),
     "},\"filter_audit\":",D972IDLFilterAuditJson(),
     ",\"stage_artifacts\":[",D972IDLJoin(D972IDLStageMeta,","),
  "]}");
D972IDLWrite(D972IDLOutput,Concatenation(D972IDLFinal,"\n"));
Print("B4_IDREL_DIRECT_LOGGED_FINAL_MARKER output=",D972IDLOutput,
  " status=",D972IDLStatus," stages=",Length(D972IDLStageResults),
  " unique=486 exact=972\n");
