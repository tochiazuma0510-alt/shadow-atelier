#############################################################################
## d972_b4_u_a18_anupq_v1.g
##
## Finite-obstruction lane for the raw A.18 presentation.  The presentation
## is F6/(18 K05 rows + the five literal A.18 images of the 28 marked rows).
## It evaluates the unconditional PENT-FORM' D-tilde rows in the index-32
## regular C2^5 Schreier kernel, followed by bounded p=3 PQuotient classes.
## A defect is a finite-quotient candidate only; no global B4 claim is made.
## This file is self-contained, ASCII, and safe under a generic GAP Read.
## It contains no process-exit command and performs no worker/base shadow scan;
## the only ledger is the exact 972 D-tilde rows named below.
##
## Controls:
##   D972_B4_A18_ANUPQ_INPUT, _WORDS, _OUTPUT, _SELFTEST, _CLASSES
#############################################################################

if LoadPackage("json")<>true then Error("A18 ANUPQ: JSON package unavailable"); fi;;
if not IsBound(PQuotient) then Error("A18 ANUPQ: PQuotient unavailable"); fi;;

D972A18ANInput:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972A18ANWords:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972A18ANOutput:="ci/out/d972_b4_u_a18_anupq_v1.json";;
if IsBound(D972_B4_A18_ANUPQ_INPUT) then D972A18ANInput:=D972_B4_A18_ANUPQ_INPUT; fi;;
if IsBound(D972_B4_A18_ANUPQ_WORDS) then D972A18ANWords:=D972_B4_A18_ANUPQ_WORDS; fi;;
if IsBound(D972_B4_A18_ANUPQ_OUTPUT) then D972A18ANOutput:=D972_B4_A18_ANUPQ_OUTPUT; fi;;
D972A18ANSelf:=false;;
if IsBound(D972_B4_A18_ANUPQ_SELFTEST) then
  D972A18ANSelf:=D972_B4_A18_ANUPQ_SELFTEST=true or
    D972_B4_A18_ANUPQ_SELFTEST=1;
fi;;
D972A18ANClasses:=[2,3];;
if IsBound(D972_B4_A18_ANUPQ_CLASSES) then D972A18ANClasses:=D972_B4_A18_ANUPQ_CLASSES; fi;;

D972A18ANSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972A18ANWordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972A18ANRelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972A18ANA18RowsSha:="1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722";;
D972A18ANPresentationSha:="783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305";;
D972A18ANDtildeSha:="32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef";;
D972A18ANRSSha:="418e88934210e726de0e7e1f375bac2e6151f465be84f913884c58129217259c";;
D972A18ANRelRSSha:="db25c0268cdc774ef3205c9c1d1cf62cd013e6daaf73cf959e7972af5b3082bb";;
D972A18ANRho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;
D972A18ANGenBits:=[1,2,4,8,16,31];;

D972A18ANJoin:=function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;
  out:=xs[1];;
  if Length(xs)>1 then
    for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  fi;
  return out;
end;;
D972A18ANJson:=function(x)
  local names,parts,i,key,t;
  if x=fail then return "null"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    t:=ReplacedString(x,"\\","\\\\");;
    t:=ReplacedString(t,"\"","\\\"");;
    t:=ReplacedString(t,"\n","\\n");;
    t:=ReplacedString(t,"\r","\\r");;
    return Concatenation("\"",t,"\"");
  fi;
  if IsList(x) then
    parts:=List([1..Length(x)],i->D972A18ANJson(x[i]));;
    return Concatenation("[",D972A18ANJoin(parts,","),"]");
  fi;
  if IsRecord(x) then
    names:=SortedList(RecNames(x));; parts:=[];;
    for key in names do Add(parts,Concatenation(D972A18ANJson(key),":",
      D972A18ANJson(x.(key)))); od;
    return Concatenation("{",D972A18ANJoin(parts,","),"}");
  fi;
  Error("A18 ANUPQ: JSON type drift");
end;;
D972A18ANWrite:=function(path,text)
  WriteFile(path,Concatenation(text,"\n"));
end;;
D972A18ANReduce:=function(w)
  local out,x,n;
  out:=[];;
  for x in w do
    if not IsInt(x) or x=0 then Error("A18 ANUPQ: signed word drift"); fi;
    n:=Length(out);;
    if n>0 and out[n]=-x then Remove(out,n); else Add(out,x); fi;
  od;
  return out;
end;;
D972A18ANInverse:=function(w)
  return List(Reversed(w),x->-x);
end;;
D972A18ANRhoWord:=function(w)
  local out,x,img;
  out:=[];;
  for x in w do
    if AbsInt(x)<1 or AbsInt(x)>6 then Error("A18 ANUPQ: rho alphabet drift"); fi;
    img:=D972A18ANRho[AbsInt(x)];;
    if x<0 then Append(out,D972A18ANInverse(img)); else Append(out,img); fi;
  od;
  return D972A18ANReduce(out);
end;;
D972A18ANMarkedSubstitute:=function(w,a,b)
  local out,x,img;
  out:=[];;
  for x in w do
    if AbsInt(x)<>1 and AbsInt(x)<>4 then
      Error("A18 ANUPQ: marked F2 alphabet drift");
    fi;
    if AbsInt(x)=1 then img:=a; else img:=b; fi;
    if x<0 then Append(out,D972A18ANInverse(img)); else Append(out,img); fi;
  od;
  return D972A18ANReduce(out);
end;;
D972A18ANSubstituteF2:=function(w,a,b)
  local out,x,img;
  out:=[];;
  for x in w do
    if AbsInt(x)<>1 and AbsInt(x)<>2 then
      Error("A18 ANUPQ: roof F2 alphabet drift");
    fi;
    if AbsInt(x)=1 then img:=a; else img:=b; fi;
    if x<0 then Append(out,D972A18ANInverse(img)); else Append(out,img); fi;
  od;
  return D972A18ANReduce(out);
end;;
D972A18ANMaps:=[
  rec(name:="123",substitution:=[[1],[4]]),
  rec(name:="234",substitution:=[[4],[6]]),
  rec(name:="12,3,4",substitution:=[[2,4],[6]]),
  rec(name:="1,23,4",substitution:=[[1,2],[5,6]]),
  rec(name:="1,2,34",substitution:=[[1],[4,5]]) ];;

D972A18ANLoad:=function()
  local src,inp,rels,wsrc,winp,seeds,a18,one,allA,rows,raw,norms,
    row,map,p,expected,orbit,j,v,t,block,x,norm;
  src:=StringFile(D972A18ANInput);;
  if src=fail or HexSHA256(src)<>D972A18ANSourceSha then
    Error("A18 ANUPQ: input SHA drift");
  fi;
  inp:=JsonStringToGap(src);;
  if inp=fail or inp.schema<>"d972-b4-p2-magnus-input/v2" or
     inp.relator_count<>158 or Length(inp.all_relators)<>158 or
     inp.rho_words<>D972A18ANRho or
     inp.rho_words_source<>"universal_v2_canonical" or
     inp.all_relators_sha256<>D972A18ANRelSha then
    Error("A18 ANUPQ: canonical input contract drift");
  fi;
  rels:=List(inp.all_relators,ShallowCopy);;
  if HexSHA256(D972A18ANJson(rels))<>D972A18ANRelSha then
    Error("A18 ANUPQ: relator digest drift");
  fi;
  wsrc:=StringFile(D972A18ANWords);;
  if wsrc=fail or HexSHA256(wsrc)<>D972A18ANWordsSha then
    Error("A18 ANUPQ: word artifact SHA drift");
  fi;
  winp:=JsonStringToGap(wsrc);;
  if winp=fail or winp.schema<>"d972-b4-word-key-artifact/v1" or
     winp.count<>972 or Length(winp.rows)<>972 then
    Error("A18 ANUPQ: word artifact contract drift");
  fi;
  seeds:=List(rels{[19..46]},ShallowCopy);;
  a18:=[];;
  for map in D972A18ANMaps do
    Append(a18,List(seeds,x->D972A18ANMarkedSubstitute(x,
      map.substitution[1],map.substitution[2])));
  od;
  if HexSHA256(D972A18ANJson(a18))<>D972A18ANA18RowsSha then
    Error("A18 ANUPQ: raw A18 row digest drift");
  fi;
  allA:=Concatenation(rels{[1..18]},a18);;
  if HexSHA256(D972A18ANJson(allA))<>D972A18ANPresentationSha then
    Error("A18 ANUPQ: presentation digest drift");
  fi;
  norms:=[];;
  for row in winp.rows do
    j:=[];;
    for x in row[3] do
      if AbsInt(x)=1 then Add(j,SignInt(x)*1);
      elif AbsInt(x)=2 then Add(j,SignInt(x)*4);
      else Error("A18 ANUPQ: roof word alphabet drift"); fi;
    od;
    j:=D972A18ANReduce(j);;
    ## Unconditional PENT-FORM' D-tilde, with no condition-I shortcut.
    norm:=D972A18ANReduce(Concatenation(
      D972A18ANInverse(D972A18ANMarkedSubstitute(j,[-6,-5,-3],[6])),
      D972A18ANInverse(D972A18ANMarkedSubstitute(j,[1],[-3,-2,-1])),
      D972A18ANMarkedSubstitute(j,[4],[6]),
      D972A18ANMarkedSubstitute(j,[-6,-5,-3],[-3,-2,-1]),
      D972A18ANMarkedSubstitute(j,[1],[4])));
    Add(norms,norm);
  od;
  if HexSHA256(D972A18ANJson(norms))<>D972A18ANDtildeSha then
    Error("A18 ANUPQ: Dtilde digest drift");
  fi;
  return rec(source:=src,input:=inp,relators:=rels,seeds:=seeds,
    a18_rows:=a18,presentation:=allA,norms:=norms,
    source_sha256:=D972A18ANSourceSha,relator_sha256:=D972A18ANRelSha,
    a18_rows_sha256:=D972A18ANA18RowsSha,
    presentation_sha256:=D972A18ANPresentationSha,
    dtilde_sha256:=D972A18ANDtildeSha);
end;;

D972A18ANToggle:=function(mask,bit)
  if bit=31 then return 31-mask; fi;
  if QuoInt(mask,bit) mod 2=1 then return mask-bit; fi;
  return mask+bit;
end;;
D972A18ANTransversal:=function(mask)
  local out,bit;
  out:=[];;
  for bit in [0..4] do if QuoInt(mask,2^bit) mod 2=1 then Add(out,bit+1); fi; od;
  return out;
end;;
D972A18ANBuildRS:=function(relators)
  local reps,pairId,pairWords,mask,gen,bit,raw,word,id,rs,start,rel,x;
  reps:=List([0..31],D972A18ANTransversal);;
  pairId:=List([1..32],i->List([1..6],j->0));; pairWords:=[];;
  for mask in [0..31] do
    for gen in [1..6] do
      bit:=D972A18ANGenBits[gen];;
      raw:=Concatenation(reps[mask+1],[gen],
        D972A18ANInverse(reps[D972A18ANToggle(mask,bit)+1]));;
      word:=D972A18ANReduce(raw);;
      if Length(word)>0 then Add(pairWords,word);;
        id:=Length(pairWords);; pairId[mask+1][gen]:=id;
      fi;
    od;
  od;
  if Length(pairWords)<>161 then Error("A18 ANUPQ: Schreier generator count drift"); fi;
  rs:=[];;
  for start in [0..31] do
    for rel in relators do
      mask:=start;; word:=[];;
      for x in rel do
        gen:=AbsInt(x);; bit:=D972A18ANGenBits[gen];;
        if x>0 then
          id:=pairId[mask+1][gen];; if id>0 then Add(word,id); fi;
          mask:=D972A18ANToggle(mask,bit);
        else
          mask:=D972A18ANToggle(mask,bit);; id:=pairId[mask+1][gen];;
          if id>0 then Add(word,-id); fi;
        fi;
      od;
      if mask<>start then Error("A18 ANUPQ: relator leaves C2^5"); fi;
      word:=D972A18ANReduce(word);; if Length(word)>0 then Add(rs,word); fi;
    od;
  od;
  if Length(rs)<>5056 then Error("A18 ANUPQ: Schreier relator count drift"); fi;
  return rec(pair_id:=pairId,pair_words:=pairWords,relators:=rs,
    transversal:=reps);
end;;
D972A18ANRewrite:=function(word,start,pairId)
  local mask,out,x,gen,bit,id;
  mask:=start;; out:=[];;
  for x in word do
    gen:=AbsInt(x);; bit:=D972A18ANGenBits[gen];;
    if x>0 then id:=pairId[mask+1][gen];; if id>0 then Add(out,id); fi;
      mask:=D972A18ANToggle(mask,bit);
    else mask:=D972A18ANToggle(mask,bit);; id:=pairId[mask+1][gen];;
      if id>0 then Add(out,-id); fi;
    fi;
  od;
  if mask<>start then Error("A18 ANUPQ: norm leaves C2^5"); fi;
  return D972A18ANReduce(out);
end;;

D972A18ANObj:=D972A18ANLoad();;
D972A18ANRaw:=D972A18ANBuildRS(D972A18ANObj.presentation);;
D972A18ANRawSha:=HexSHA256(D972A18ANJson(D972A18ANRaw.relators));;
D972A18ANNormRows:=List(D972A18ANObj.norms,x->D972A18ANRewrite(x,0,
  D972A18ANRaw.pair_id));;
D972A18ANNormSha:=HexSHA256(D972A18ANJson(D972A18ANNormRows));;
if D972A18ANRawSha<>D972A18ANRelRSSha or D972A18ANNormSha<>D972A18ANRSSha then
  Error("A18 ANUPQ: Schreier digest drift");
fi;;

D972A18ANBase:=rec(
  basis_id:="regular_c2^5_mask_transversal_v1",coset_count:=32,
  original_generator_count:=6,rs_generator_count:=161,rs_relator_count:=5056,
  gen_bits:=D972A18ANGenBits,transversal:=D972A18ANRaw.transversal);;

if D972A18ANSelf then
  D972A18ANSelfReceipt:=rec(schema:="d972-b4-u-a18-anupq/v1",
    status:="A18_ANUPQ_SELFTEST_PASS",terminal_claim:=false,
    final_marker:="D972_B4_U_A18_ANUPQ_V1_FINAL",
    source_sha256:=D972A18ANSourceSha,relator_sha256:=D972A18ANRelSha,
    word_artifact_sha256:=D972A18ANWordsSha,
    a18_rows_sha256:=D972A18ANA18RowsSha,
    presentation_sha256:=D972A18ANPresentationSha,
    dtilde_sha256:=D972A18ANDtildeSha,raw_rs_sha256:=D972A18ANRawSha,
    dtilde_rs_sha256:=D972A18ANNormSha,normal_closure_status:="NOT_RUN_BOUNDED",
    quotient_prime:=3,p_quotient_bound:=4096,
    a18_map_count:=5,a18_row_count:=140,norm_count:=972,
    basis_contract:=D972A18ANBase);;
  D972A18ANWrite(D972A18ANOutput,D972A18ANJson(D972A18ANSelfReceipt));;
  Print("D972_B4_U_A18_ANUPQ_V1_FINAL status=A18_ANUPQ_SELFTEST_PASS output=",
    D972A18ANOutput,"\n");
else
  D972A18ANF:=FreeGroup(161,"ka18");;
  D972A18ANG:=GeneratorsOfGroup(D972A18ANF);;
  D972A18ANRelWords:=List(D972A18ANRaw.relators,function(x)
    local z,y;
    z:=One(D972A18ANG[1]);;
    for y in x do if y>0 then z:=z*D972A18ANG[y];
      else z:=z*D972A18ANG[-y]^-1; fi; od;
    return z;
  end);;
  D972A18ANKfp:=D972A18ANF/D972A18ANRelWords;;
  D972A18ANKgens:=GeneratorsOfGroup(D972A18ANKfp);;
  D972A18ANRows:=[];; D972A18ANTerminal:=false;;
  for D972A18ANClass in D972A18ANClasses do
    Print("D972_B4_U_A18_ANUPQ_CLASS_BEGIN class=",D972A18ANClass,"\n");
    D972A18ANQ:=PQuotient(D972A18ANKfp,3,D972A18ANClass,4096,
      "combinatorial":noninteractive);;
    if D972A18ANQ=fail then
      Add(D972A18ANRows,rec(class:=D972A18ANClass,status:="UNKNOWN_RESOURCE"));;
    else
      D972A18ANMap:=EpimorphismQuotientSystem(D972A18ANQ);;
      D972A18ANH:=Image(D972A18ANMap);;
      D972A18ANQG:=List(D972A18ANKgens,g->Image(D972A18ANMap,g));;
      D972A18ANPcgs:=Pcgs(D972A18ANH);;
      D972A18ANOrders:=List(RelativeOrders(D972A18ANPcgs),Int);;
      D972A18ANImages:=List(D972A18ANQG,
        g->List(ExponentsOfPcElement(D972A18ANPcgs,g),Int));;
      D972A18ANPower:=List([1..Length(D972A18ANPcgs)],i->
        List(ExponentsOfPcElement(D972A18ANPcgs,
          D972A18ANPcgs[i]^D972A18ANOrders[i]),Int));;
      D972A18ANConj:=[];;
      if Length(D972A18ANPcgs)>1 then
        for i in [2..Length(D972A18ANPcgs)] do
          for j in [1..i-1] do Add(D972A18ANConj,[i,j,
            List(ExponentsOfPcElement(D972A18ANPcgs,
              D972A18ANPcgs[i]^D972A18ANPcgs[j]),Int)]); od;
        od;
      fi;
      D972A18ANBad:=0;; D972A18ANFirst:=fail;;
      for i in [1..972] do
        z:=One(D972A18ANH);;
        for x in D972A18ANNormRows[i] do
          if x>0 then z:=z*D972A18ANQG[x];
          else z:=z*D972A18ANQG[-x]^-1; fi;
        od;
        if not IsOne(z) then
          D972A18ANBad:=D972A18ANBad+1;;
          if D972A18ANFirst=fail then
            D972A18ANFirst:=rec(index:=i,norm_rs:=D972A18ANNormRows[i],
              image:=List(ExponentsOfPcElement(D972A18ANPcgs,z),Int));
          fi;
        fi;
      od;
      if D972A18ANBad>0 then D972A18ANTerminal:=true; fi;
      D972A18ANClassStatus:="ALLPASS";;
      if D972A18ANBad>0 then D972A18ANClassStatus:="DEFECT"; fi;
      Add(D972A18ANRows,rec(class:=D972A18ANClass,
        status:=D972A18ANClassStatus,order:=Size(D972A18ANH),
        pcgs_relative_orders:=D972A18ANOrders,
        pcgs_power_relations:=D972A18ANPower,
        pcgs_conjugate_relations:=D972A18ANConj,
        quotient_generator_images:=D972A18ANImages,bad_count:=D972A18ANBad,
        first_defect:=D972A18ANFirst));
      Print("D972_B4_U_A18_ANUPQ_CLASS_DONE class=",D972A18ANClass,
        " order=",Size(D972A18ANH)," bad_count=",D972A18ANBad,"\n");
    fi;
    if D972A18ANTerminal then break; fi;
  od;
  D972A18ANStatus:="UNKNOWN_P3_BOUNDED";;
  if D972A18ANTerminal then D972A18ANStatus:="B4_A_CANDIDATE_P3"; fi;
  D972A18ANClassJson:=function(c)
    if c.status="UNKNOWN_RESOURCE" then return Concatenation(
      "{\"class\":",String(c.class),",\"status\":\"UNKNOWN_RESOURCE\"}"); fi;
    return Concatenation("{\"class\":",String(c.class),",\"status\":",
      D972A18ANJson(c.status),",\"order\":",String(c.order),
      ",\"pcgs_relative_orders\":",D972A18ANJson(c.pcgs_relative_orders),
      ",\"pcgs_power_relations\":",D972A18ANJson(c.pcgs_power_relations),
      ",\"pcgs_conjugate_relations\":",D972A18ANJson(c.pcgs_conjugate_relations),
      ",\"quotient_generator_images\":",D972A18ANJson(c.quotient_generator_images),
      ",\"bad_count\":",String(c.bad_count),",\"first_defect\":",
      D972A18ANJson(c.first_defect),"}");
  end;;
  D972A18ANClassStrings:=List(D972A18ANRows,D972A18ANClassJson);;
  D972A18ANReceipt:=rec(schema:="d972-b4-u-a18-anupq/v1",
    status:=D972A18ANStatus,terminal_claim:=false,
    final_marker:="D972_B4_U_A18_ANUPQ_V1_FINAL",
    source_sha256:=D972A18ANSourceSha,relator_sha256:=D972A18ANRelSha,
    a18_rows_sha256:=D972A18ANA18RowsSha,
    presentation_sha256:=D972A18ANPresentationSha,
    dtilde_sha256:=D972A18ANDtildeSha,raw_rs_sha256:=D972A18ANRawSha,
    dtilde_rs_sha256:=D972A18ANNormSha,word_artifact_sha256:=D972A18ANWordsSha,
    quotient_prime:=3,p_quotient_bound:=4096,requested_classes:=D972A18ANClasses,
    completed_classes:=List(D972A18ANRows,x->x.class),basis_contract:=D972A18ANBase,
    a18_map_count:=5,a18_row_count:=140,norm_count:=972,
    classes:=D972A18ANRows,normal_closure_status:="NOT_RUN_BOUNDED",
    global_semantic_claim:="PENDING_A18_CLOSURE_BRIDGE");;
  D972A18ANWrite(D972A18ANOutput,D972A18ANJson(D972A18ANReceipt));;
  Print("D972_B4_U_A18_ANUPQ_V1_FINAL status=",D972A18ANStatus,
    " output=",D972A18ANOutput,"\n");
fi;
