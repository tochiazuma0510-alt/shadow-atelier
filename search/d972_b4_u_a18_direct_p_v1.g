#############################################################################
## d972_b4_u_a18_direct_p_v1.g
##
## Direct ambient p-quotient harness for the canonical raw A.18
## presentation.  Unlike the older Schreier-kernel lane, PQuotient is
## applied to F6/N_A itself.  Every emitted six-tuple is therefore a genuine
## finite image of the raw A.18 presentation; no unperformed core/normality
## step is hidden in the receipt.
##
## The two preregistered bad-characteristic campaigns are p=2, classes 1..4,
## and p=5, classes 1..3.  The prime and class list may be overridden for a
## bounded GHA run, but are always recorded in the receipt.  ALLPASS and
## UNKNOWN are nonterminal.  A nonidentity D-tilde is only a finite
## obstruction candidate for this presentation, not a global B4-A theorem.
##
## Controls:
##   D972_B4_A18_DIRECT_P, _CLASSES, _INPUT, _WORDS, _OUTPUT, _SELFTEST
#############################################################################

if LoadPackage("json")<>true then Error("A18 direct p: JSON package unavailable"); fi;;
if not IsBound(PQuotient) then Error("A18 direct p: PQuotient unavailable"); fi;;

D972A18DPInput:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972A18DPWords:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972A18DPOutput:="ci/out/d972_b4_u_a18_direct_p_v1.json";;
D972A18DPP:=2;;
D972A18DPClasses:=[1,2,3,4];;
if IsBound(D972_B4_A18_DIRECT_P) then D972A18DPP:=D972_B4_A18_DIRECT_P;; fi;;
if D972A18DPP=5 then D972A18DPClasses:=[1,2,3];; fi;;
if IsBound(D972_B4_A18_DIRECT_CLASSES) then
  D972A18DPClasses:=D972_B4_A18_DIRECT_CLASSES;
fi;;
if IsBound(D972_B4_A18_DIRECT_INPUT) then D972A18DPInput:=D972_B4_A18_DIRECT_INPUT;; fi;;
if IsBound(D972_B4_A18_DIRECT_WORDS) then D972A18DPWords:=D972_B4_A18_DIRECT_WORDS;; fi;;
if IsBound(D972_B4_A18_DIRECT_OUTPUT) then D972A18DPOutput:=D972_B4_A18_DIRECT_OUTPUT;; fi;;
D972A18DPSelf:=false;;
if IsBound(D972_B4_A18_DIRECT_SELFTEST) then
  D972A18DPSelf:=D972_B4_A18_DIRECT_SELFTEST=true or
    D972_B4_A18_DIRECT_SELFTEST=1;
fi;;
if not D972A18DPP in [2,5] then Error("A18 direct p: prime must be 2 or 5"); fi;;

D972A18DPSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972A18DPWordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972A18DPRelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972A18DPA18RowsSha:="1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722";;
D972A18DPPresentationSha:="783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305";;
D972A18DPDtildeSha:="32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef";;
D972A18DPRho:=[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]];;

D972A18DPJoin:=function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;
  out:=xs[1];;
  if Length(xs)>1 then
    for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  fi;
  return out;
end;;
D972A18DPJson:=function(x)
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
    parts:=List([1..Length(x)],i->D972A18DPJson(x[i]));;
    return Concatenation("[",D972A18DPJoin(parts,","),"]");
  fi;
  if IsRecord(x) then
    names:=SortedList(RecNames(x));; parts:=[];;
    for key in names do Add(parts,Concatenation(D972A18DPJson(key),":",
      D972A18DPJson(x.(key)))); od;
    return Concatenation("{",D972A18DPJoin(parts,","),"}");
  fi;
  Error("A18 direct p: JSON type drift");
end;;
D972A18DPWrite:=function(path,text)
  local f;
  f:=OutputTextFile(path,false);;
  SetPrintFormattingStatus(f,false);;
  PrintTo(f,text,"\n");;
  CloseStream(f);
end;;
D972A18DPReduce:=function(w)
  local out,x,n;
  out:=[];;
  for x in w do
    if not IsInt(x) or x=0 then Error("A18 direct p: signed word drift"); fi;
    n:=Length(out);;
    if n>0 and out[n]=-x then Remove(out,n); else Add(out,x); fi;
  od;
  return out;
end;;
D972A18DPInverse:=function(w)
  return List(Reversed(w),x->-x);
end;;
D972A18DPMarkedSubstitute:=function(w,a,b)
  local out,x,img;
  out:=[];;
  for x in w do
    if not IsInt(x) or AbsInt(x)<>1 and AbsInt(x)<>4 then
      Error("A18 direct p: marked F2 alphabet drift");
    fi;
    if AbsInt(x)=1 then img:=a; else img:=b; fi;
    if x<0 then Append(out,D972A18DPInverse(img)); else Append(out,img); fi;
  od;
  return D972A18DPReduce(out);
end;;
D972A18DPMaps:=[
  rec(name:="123",substitution:=[[1],[4]]),
  rec(name:="234",substitution:=[[4],[6]]),
  rec(name:="12,3,4",substitution:=[[2,4],[6]]),
  rec(name:="1,23,4",substitution:=[[1,2],[5,6]]),
  rec(name:="1,2,34",substitution:=[[1],[4,5]]) ];;

D972A18DPLoad:=function()
  local src,inp,rels,wsrc,winp,seeds,a18,allA,row,map,norms,j,x;
  src:=StringFile(D972A18DPInput);;
  if src=fail or HexSHA256(src)<>D972A18DPSourceSha then
    Error("A18 direct p: input SHA drift");
  fi;
  inp:=JsonStringToGap(src);;
  if inp=fail or inp.schema<>"d972-b4-p2-magnus-input/v2" or
     inp.relator_count<>158 or Length(inp.all_relators)<>158 or
     inp.rho_words<>D972A18DPRho or inp.rho_words_source<>"universal_v2_canonical" or
     inp.all_relators_sha256<>D972A18DPRelSha then
    Error("A18 direct p: canonical input contract drift");
  fi;
  rels:=List(inp.all_relators,ShallowCopy);;
  if HexSHA256(D972A18DPJson(rels))<>D972A18DPRelSha then
    Error("A18 direct p: relator digest drift");
  fi;
  wsrc:=StringFile(D972A18DPWords);;
  if wsrc=fail or HexSHA256(wsrc)<>D972A18DPWordsSha then
    Error("A18 direct p: word artifact SHA drift");
  fi;
  winp:=JsonStringToGap(wsrc);;
  if winp=fail or winp.schema<>"d972-b4-word-key-artifact/v1" or
     winp.count<>972 or Length(winp.rows)<>972 then
    Error("A18 direct p: word artifact contract drift");
  fi;
  seeds:=List(rels{[19..46]},ShallowCopy);; a18:=[];;
  for map in D972A18DPMaps do
    Append(a18,List(seeds,x->D972A18DPMarkedSubstitute(x,
      map.substitution[1],map.substitution[2])));
  od;
  if HexSHA256(D972A18DPJson(a18))<>D972A18DPA18RowsSha then
    Error("A18 direct p: raw A18 digest drift");
  fi;
  allA:=Concatenation(rels{[1..18]},a18);;
  if HexSHA256(D972A18DPJson(allA))<>D972A18DPPresentationSha then
    Error("A18 direct p: presentation digest drift");
  fi;
  norms:=[];;
  for row in winp.rows do
    j:=[];;
    for x in row[3] do
      if AbsInt(x)=1 then Add(j,SignInt(x)*1);
      elif AbsInt(x)=2 then Add(j,SignInt(x)*4);
      else Error("A18 direct p: roof word alphabet drift"); fi;
    od;
    j:=D972A18DPReduce(j);;
    Add(norms,D972A18DPReduce(Concatenation(
      D972A18DPInverse(D972A18DPMarkedSubstitute(j,[-6,-5,-3],[6])),
      D972A18DPInverse(D972A18DPMarkedSubstitute(j,[1],[-3,-2,-1])),
      D972A18DPMarkedSubstitute(j,[4],[6]),
      D972A18DPMarkedSubstitute(j,[-6,-5,-3],[-3,-2,-1]),
      D972A18DPMarkedSubstitute(j,[1],[4]))));
  od;
  if HexSHA256(D972A18DPJson(norms))<>D972A18DPDtildeSha then
    Error("A18 direct p: Dtilde digest drift");
  fi;
  return rec(input:=inp,relators:=rels,a18_rows:=a18,presentation:=allA,
    norms:=norms,source_sha256:=D972A18DPSourceSha,
    word_artifact_sha256:=D972A18DPWordsSha,relator_sha256:=D972A18DPRelSha,
    a18_rows_sha256:=D972A18DPA18RowsSha,
    presentation_sha256:=D972A18DPPresentationSha,dtilde_sha256:=D972A18DPDtildeSha);
end;;

D972A18DPObj:=D972A18DPLoad();;

if D972A18DPSelf then
  D972A18DPSelfReceipt:=rec(schema:="d972-b4-u-a18-direct-p/v1",
    status:="DIRECT_P_SELFTEST_PASS",terminal_claim:=false,
    final_marker:="D972_B4_U_A18_DIRECT_P_V1_FINAL",
    prime:=D972A18DPP,requested_classes:=D972A18DPClasses,
    source_sha256:=D972A18DPObj.source_sha256,
    word_artifact_sha256:=D972A18DPObj.word_artifact_sha256,
    relator_sha256:=D972A18DPObj.relator_sha256,
    a18_rows_sha256:=D972A18DPObj.a18_rows_sha256,
    presentation_sha256:=D972A18DPObj.presentation_sha256,
    dtilde_sha256:=D972A18DPObj.dtilde_sha256,
    raw_relator_count:=158,dtilde_count:=972,generator_order:=[1,2,3,4,5,6],
    ambient_presentation:=true,legitimacy:=
      "direct quotient of F6 by canonical raw A18 relators",
    normal_closure_status:="NOT_NEEDED_DIRECT_AMBIENT");;
  D972A18DPWrite(D972A18DPOutput,D972A18DPJson(D972A18DPSelfReceipt));;
  Print("D972_B4_U_A18_DIRECT_P_V1_FINAL status=DIRECT_P_SELFTEST_PASS output=",
    D972A18DPOutput,"\n");
else
  D972A18DPF:=FreeGroup(6,"a18");;
  D972A18DPGens:=GeneratorsOfGroup(D972A18DPF);;
  D972A18DPRelWords:=List(D972A18DPObj.presentation,function(w)
    local z,y;
    z:=One(D972A18DPGens[1]);;
    for y in w do
      if y>0 then z:=z*D972A18DPGens[y];
      else z:=z*D972A18DPGens[-y]^-1; fi;
    od;
    return z;
  end);;
  D972A18DPKfp:=D972A18DPF/D972A18DPRelWords;;
  D972A18DPKgens:=GeneratorsOfGroup(D972A18DPKfp);;
  if Length(D972A18DPKgens)<>6 then
    Error("A18 direct p: quotient generator count drift");
  fi;;
  D972A18DPRows:=[];; D972A18DPDefect:=false;;
  for D972A18DPClass in D972A18DPClasses do
    Print("D972_B4_U_A18_DIRECT_P_CLASS_BEGIN p=",D972A18DPP,
      " class=",D972A18DPClass,"\n");
    D972A18DPQ:=PQuotient(D972A18DPKfp,D972A18DPP,D972A18DPClass,4096,
      "combinatorial":noninteractive);;
    if D972A18DPQ=fail then
      Add(D972A18DPRows,rec(class:=D972A18DPClass,status:="UNKNOWN_RESOURCE"));;
    else
      D972A18DPMap:=EpimorphismQuotientSystem(D972A18DPQ);;
      D972A18DPH:=Image(D972A18DPMap);;
      D972A18DPImagesG:=List(D972A18DPKgens,g->Image(D972A18DPMap,g));;
      D972A18DPPcgs:=Pcgs(D972A18DPH);;
      D972A18DPOrders:=List(RelativeOrders(D972A18DPPcgs),Int);;
      D972A18DPImages:=List(D972A18DPImagesG,
        g->List(ExponentsOfPcElement(D972A18DPPcgs,g),Int));;
      D972A18DPPower:=List([1..Length(D972A18DPPcgs)],i->
        List(ExponentsOfPcElement(D972A18DPPcgs,
          D972A18DPPcgs[i]^D972A18DPOrders[i]),Int));
      D972A18DPConj:=[];;
      if Length(D972A18DPPcgs)>1 then
        for i in [2..Length(D972A18DPPcgs)] do
          for j in [1..i-1] do Add(D972A18DPConj,[i,j,
            List(ExponentsOfPcElement(D972A18DPPcgs,
              D972A18DPPcgs[i]^D972A18DPPcgs[j]),Int)]); od;
        od;
      fi;
      D972A18DPBadRaw:=0;; D972A18DPBad:=0;; D972A18DPFirst:=fail;;
      for i in [1..158] do
        z:=One(D972A18DPH);;
        for x in D972A18DPObj.presentation[i] do
          if x>0 then z:=z*D972A18DPImagesG[x];
          else z:=z*D972A18DPImagesG[-x]^-1; fi;
        od;
        if not IsOne(z) then D972A18DPBadRaw:=D972A18DPBadRaw+1; fi;
      od;
      for i in [1..972] do
        z:=One(D972A18DPH);;
        for x in D972A18DPObj.norms[i] do
          if x>0 then z:=z*D972A18DPImagesG[x];
          else z:=z*D972A18DPImagesG[-x]^-1; fi;
        od;
        if not IsOne(z) then
          D972A18DPBad:=D972A18DPBad+1;;
          if D972A18DPFirst=fail then
            D972A18DPFirst:=rec(index:=i,word:=D972A18DPObj.norms[i],
              image:=List(ExponentsOfPcElement(D972A18DPPcgs,z),Int));
          fi;
        fi;
      od;
      if D972A18DPBadRaw>0 then Error("A18 direct p: quotient fails raw relator"); fi;;
      if D972A18DPBad>0 then D972A18DPDefect:=true; fi;;
      D972A18DPClassStatus:="ALLPASS";;
      if D972A18DPBad>0 then D972A18DPClassStatus:="DEFECT"; fi;;
      Add(D972A18DPRows,rec(class:=D972A18DPClass,status:=D972A18DPClassStatus,
        order:=Size(D972A18DPH),pcgs_relative_orders:=D972A18DPOrders,
        pcgs_power_relations:=D972A18DPPower,
        pcgs_conjugate_relations:=D972A18DPConj,
        quotient_generator_images:=D972A18DPImages,
        raw_relator_bad_count:=D972A18DPBadRaw,dtilde_bad_count:=D972A18DPBad,
        first_defect:=D972A18DPFirst));
      Print("D972_B4_U_A18_DIRECT_P_CLASS_DONE p=",D972A18DPP,
        " class=",D972A18DPClass," order=",Size(D972A18DPH),
        " raw_bad=",D972A18DPBadRaw," dtilde_bad=",D972A18DPBad,"\n");
    fi;
  od;
  D972A18DPStatus:="UNKNOWN_DIRECT_P_BOUNDED";;
  if D972A18DPDefect then D972A18DPStatus:="DIRECT_FINITE_OBSTRUCTION_CANDIDATE"; fi;;
  D972A18DPClassJson:=function(c)
    if c.status="UNKNOWN_RESOURCE" then return Concatenation(
      "{\"class\":",String(c.class),",\"status\":\"UNKNOWN_RESOURCE\"}"); fi;
    return Concatenation("{\"class\":",String(c.class),",\"status\":",
      D972A18DPJson(c.status),",\"order\":",String(c.order),
      ",\"pcgs_relative_orders\":",D972A18DPJson(c.pcgs_relative_orders),
      ",\"pcgs_power_relations\":",D972A18DPJson(c.pcgs_power_relations),
      ",\"pcgs_conjugate_relations\":",D972A18DPJson(c.pcgs_conjugate_relations),
      ",\"quotient_generator_images\":",D972A18DPJson(c.quotient_generator_images),
      ",\"raw_relator_bad_count\":",String(c.raw_relator_bad_count),
      ",\"dtilde_bad_count\":",String(c.dtilde_bad_count),
      ",\"first_defect\":",D972A18DPJson(c.first_defect),"}");
  end;;
  D972A18DPReceipt:=rec(schema:="d972-b4-u-a18-direct-p/v1",
    status:=D972A18DPStatus,terminal_claim:=false,
    final_marker:="D972_B4_U_A18_DIRECT_P_V1_FINAL",prime:=D972A18DPP,
    requested_classes:=D972A18DPClasses,
    completed_classes:=List(D972A18DPRows,x->x.class),
    source_sha256:=D972A18DPObj.source_sha256,
    word_artifact_sha256:=D972A18DPObj.word_artifact_sha256,
    relator_sha256:=D972A18DPObj.relator_sha256,
    a18_rows_sha256:=D972A18DPObj.a18_rows_sha256,
    presentation_sha256:=D972A18DPObj.presentation_sha256,
    dtilde_sha256:=D972A18DPObj.dtilde_sha256,
    raw_relators:=D972A18DPObj.presentation,dtilde_words:=D972A18DPObj.norms,
    raw_relator_count:=158,dtilde_count:=972,generator_order:=[1,2,3,4,5,6],
    ambient_presentation:=true,
    legitimacy:="direct quotient of F6 by canonical raw A18 relators",
    normal_closure_status:="NOT_NEEDED_DIRECT_AMBIENT",classes:=D972A18DPRows);;
  D972A18DPWrite(D972A18DPOutput,D972A18DPJson(D972A18DPReceipt));;
  Print("D972_B4_U_A18_DIRECT_P_V1_FINAL status=",D972A18DPStatus,
    " p=",D972A18DPP," output=",D972A18DPOutput,"\n");
fi;
