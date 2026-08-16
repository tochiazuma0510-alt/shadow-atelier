#############################################################################
## D972 k=9 relative C3 cell, v6: explicit full-BQ bridge.
##
## This is a GHA-only producer.  It loads only the finite prefix of the
## worker and never constructs an infinite fp group or calls an infinite
## presentation conversion.  Unlike v5, the candidate is a full marked
## B3 quotient P=<s1~,s2~> mapping to the fixed explicit BQ.  The C9 kernel
## is therefore tested at the right (full-B3) level, while its pure subgroup
## is used for the five-coface and 972-row finite cell.
##
## Important artifact shape: every frozen word row is [m,key,word].  The
## v5 [4] access was a runtime range error; v6 uses [1] and [3].
#############################################################################

V6LoadWorkerPrefix:=function(path,marker)
  local src,at,tmp;
  src:=StringFile(path);;
  if src=fail then Error("k9 v6: missing worker source"); fi;
  at:=PositionSublist(src,marker);;
  if at=fail then Error("k9 v6: worker marker drift"); fi;
  tmp:=Filename(DirectoryTemporary(),"d972_k9_v6_worker_prefix.g");;
  FileString(tmp,src{[1..at-1]});;
  Read(tmp);;
end;;

V6LoadWorkerPrefix("search/d972_dovetail_worker_v1.g",
  "\nif D972Mode = \"selftest\" then");;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

V6Json:=function(x)
  local a,i;
  if x=fail then return "null"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsInt(x) then return String(x); fi;
  if IsString(x) then return JStr(x); fi;
  if IsList(x) then
    a:=List([1..Length(x)],i->V6Json(x[i]));;
    return Concatenation("[",JoinC(a,","),"]");
  fi;
  Error("k9 v6: JSON value drift");
end;;

V6Eval:=function(w,imgs)
  local q,x,k;
  q:=One(imgs[1]);;
  for x in w do
    if x=0 or AbsInt(x)>Length(imgs) then Error("k9 v6: word alphabet drift"); fi;
    k:=AbsInt(x);;
    if x>0 then q:=q*imgs[k]; else q:=q*imgs[k]^-1; fi;
  od;
  return q;
end;;

V6Paper:=function(xs)
  local q,i;
  q:=One(xs[1]);;
  for i in [Length(xs),Length(xs)-1..1] do q:=q*xs[i]; od;
  return q;
end;;

V6PB3Pass:=function(imgs)
  local c;
  c:=imgs[1]*imgs[2]*imgs[3];;
  return ForAll(imgs,q->Comm(c,q)=One(q));
end;;

V6Cofaces:=[[[1],[2],[4]],[[4],[5],[6]],[[2,4],[3,5],[6]],
  [[1,2],[3],[5,6]],[[1],[2,3],[4,5]]];;

if IsBound(D972_B4_K9_RELATIVE_C3_V6_SELFTEST) and
   D972_B4_K9_RELATIVE_C3_V6_SELFTEST=true then
  if Length(V6Cofaces)<>5 or V6Cofaces[1]<>[[1],[2],[4]] then
    Error("k9 v6 coface canary drift");
  fi;
  Print("D972_B4_K9_RELATIVE_C3_V6_SELFTEST_PASS finite_BQ_bridge=true artifact_row_shape=[m,key,word] no_infinite_fp=true\n");
else
  V6Input:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
  V6Output:="ci/out/d972_b4_k9_relative_c3_v6.json";;
  if IsBound(D972_B4_K9_RELATIVE_C3_V6_INPUT) then V6Input:=D972_B4_K9_RELATIVE_C3_V6_INPUT; fi;
  if IsBound(D972_B4_K9_RELATIVE_C3_V6_OUTPUT) then V6Output:=D972_B4_K9_RELATIVE_C3_V6_OUTPUT; fi;
  wordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
  canonPath:="search/certs/ihnec_r4b_run_20260801.json";;
  canonSha:="fdf5fd367cdd00e4aafde4d1ac4ef3708e6f3efd338f7b7945646879e0002fd2";;
  canonRowSha:="e9e1cb711dc700b3588902b7b05f83ae0ca1967983d70d46fc22825b96b0136c";;
  targetKeySha:="9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62";;
  tupleSha:="32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91";;
  artifactCanonicalSha:="283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930";;
  src:=StringFile(V6Input);; if src=fail or HexSHA256(src)<>wordsSha then Error("k9 v6 word SHA drift"); fi;
  obj:=JsonStringToGap(src);;
  if obj=fail or obj.schema<>"d972-b4-word-key-artifact/v1" or obj.count<>972 or Length(obj.rows)<>972 then
    Error("k9 v6 word artifact drift");
  fi;
  rows:=obj.rows;;
  if ForAny(rows,r->not IsList(r) or Length(r)<>3 or not IsInt(r[1]) or not IsList(r[3])) then
    Error("k9 v6 artifact row shape drift: expected [m,key,word]");
  fi;
  canon:=StringFile(canonPath);; if canon=fail or HexSHA256(canon)<>canonSha then Error("k9 v6 canonical SHA drift"); fi;
  if obj.source_target_key_digest<>targetKeySha or obj.frozen_tuple_sha256<>tupleSha or
     obj.canonical_bytes_sha256<>artifactCanonicalSha then Error("k9 v6 artifact digest drift"); fi;

  ## Build the same explicit finite BQ as the worker; withPresentation=false
  ## is deliberate and prevents the known infinite fp conversion stall.
  B:=D972BuildBase(false);; BQ:=B.q;; bs1:=B.s1;; bs2:=B.s2;;
  if Size(BQ)<>8817984 or B.pure_size<>1469664 then Error("k9 v6 BQ order drift"); fi;
  GM:=B.compact_pure;; XM:=B.compact_x;; YM:=B.compact_y;;
  C9:=CyclicGroup(IsPermGroup,9);; radix:=[1,2,4,5,7,8];; resultJsons:=[];;
  totalZero:=0;; computedCells:=0;;
  for z9 in radix do
    E:=DirectProduct(BQ,C9);; eq:=Embedding(E,1);; ec:=Embedding(E,2);;
    c9:=Image(ec,GeneratorsOfGroup(C9)[1]);;
    ps1:=Image(eq,bs1)*c9^z9;; ps2:=Image(eq,bs2)*c9^z9;;
    P:=Group(ps1,ps2);;
    pToBQ:=GroupHomomorphismByImages(P,BQ,[ps1,ps2],[bs1,bs2]);;
    braidPass:=ps1*ps2*ps1=ps2*ps1*ps2;;
    pOnto:=pToBQ<>fail and Size(Image(pToBQ))=Size(BQ);;
    pKer:=fail;; if pToBQ<>fail then pKer:=Size(Kernel(pToBQ)); fi;
    markedPass:=pToBQ<>fail and Image(pToBQ,ps1)=bs1 and Image(pToBQ,ps2)=bs2;;
    ## The pure part is the source of the five A.18 cofaces and the rows.
    lx:=ps1^2;; ly:=ps2^2;; l13:=ps2*lx*ps2^-1;; PP:=Group(lx,l13,ly);;
    pPureToM:=GroupHomomorphismByImages(PP,GM,[lx,l13,ly],[XM,XM^-1*YM^-1,YM]);;
    pureOnto:=pPureToM<>fail and Size(Image(pPureToM))=Size(GM);;
    pureKer:=fail;; if pPureToM<>fail then pureKer:=Size(Kernel(pPureToM)); fi;
    ## A finite B3 presentation map plus the explicit factor map proves the
    ## kernel inclusion N<=M.  B4-normality remains a separately typed gate.
    nLeM:=braidPass and pOnto and markedPass and pKer=9 and pureOnto and pureKer=9;;

    ## Five finite coface images in GM^4 x C9.  zPure=2*z9 is the induced
    ## pure character of sigma_i^2; unlike v5 this is derived from full B3.
    zPure:=(2*z9) mod 9;;
    delRows:=[ [[],[],[],[1],[2],[3]], [[],[1],[2],[],[],[3]],
      [[1],[],[2],[],[3],[]], [[1],[2],[],[3],[],[]] ];;
    baseImgs:=[XM,XM^-1*YM^-1,YM];;
    delImgs:=List(delRows,r->List(r,w->V6Eval(w,baseImgs)));;
    D4:=DirectProduct(GM,GM,GM,GM,C9);; de:=List([1..5],i->Embedding(D4,i));;
    edgeImgs:=List([1..6],j->Product(Concatenation(
      List([1..4],i->Image(de[i],delImgs[i][j])),[Image(de[5],c9^zPure)])));;
    cofaceImgs:=List(V6Cofaces,t->List(t,w->V6Eval(w,edgeImgs)));;
    cofaceRelPass:=ForAll(cofaceImgs,V6PB3Pass);;
    pRelPass:=V6PB3Pass([lx,l13,ly]);;
    D5:=DirectProduct(D4,D4,D4,D4,D4);; d5:=List([1..5],i->Embedding(D5,i));;
    jointImgs:=List([1..3],j->Product(List([1..5],k->Image(d5[k],cofaceImgs[k][j]))));;
    J:=Group(jointImgs);;
    pToJ:=GroupHomomorphismByImages(PP,J,[lx,l13,ly],jointImgs);;
    jToP:=GroupHomomorphismByImages(J,PP,jointImgs,[lx,l13,ly]);;
    pJPass:=pToJ<>fail and jToP<>fail and
      ForAll([lx,l13,ly],q->Image(jToP,Image(pToJ,q))=q) and
      ForAll(GeneratorsOfGroup(J),q->Image(pToJ,Image(jToP,q))=q);;
    cofaceFactors:=ForAll(cofaceImgs,t->GroupHomomorphismByImages(J,Group(t),jointImgs,t)<>fail);;
    nExact:=pRelPass and cofaceRelPass and cofaceFactors and pJPass;;
    center:=lx*l13*ly;; centerCentral:=ForAll([lx,l13,ly],q->Comm(center,q)=One(PP));;
    finiteCell:=nLeM and nExact and centerCentral and Order(center)=3;;
    rowBits:=[];; fails:=[];; zeroCount:=fail;; rowStatus:="NOT_COMPUTED_BRIDGE_GATE";;
    if finiteCell then
      th:=GroupHomomorphismByImages(PP,PP,[lx,ly],[ly,lx]);;
      tau:=GroupHomomorphismByImages(PP,PP,[lx,ly],[ly,lx^-1*ly^-1]);;
      if th<>fail and tau<>fail then
        for ri in [1..Length(rows)] do
          ## Frozen row shape is [m,key,word], not a four-field record.
          m:=rows[ri][1];; ff:=V6Eval(rows[ri][3],[lx,ly]);; u:=2*m+1;;
          h10:=V6Paper([ff,Image(th,ff)])=One(PP);;
          ymf:=V6Paper([ly^m,ff]);; ty:=Image(tau,ymf);;
          h11:=V6Paper([Image(tau,ty),ty,ymf])=One(PP);;
          ga:=lx^u;; gb:=V6Paper([ff^-1,ly^u,ff]);;
          good:=h10 and h11 and Size(Group(ga,gb))=Size(PP);;
          Add(rowBits,good);; if not good then Add(fails,ri); fi;
        od;
        rowStatus:="FINITE_C9_ROW_SCAN_NONTERMINAL";; zeroCount:=Length(fails);; computedCells:=computedCells+1;; totalZero:=totalZero+zeroCount;
      fi;
    fi;
    if Length(rowBits)<>Length(rows) then rowBits:=fail;; fails:=fail; fi;
    if finiteCell and rowStatus<>"FINITE_C9_ROW_SCAN_NONTERMINAL" then finiteCell:=false; fi;
    one:=Concatenation(
      "{\"radix\":",String(z9),",\"pure_radix\":",String(zPure),",\"status\":\"FINITE_C9_BQ_CELL\",",
      "\"action\":\"trivial\",\"BQ_order\":",String(Size(BQ)),",\"M_order\":",String(Size(GM)),",
      "\"B3_braid_pass\":",V6Json(braidPass),",\"P_order\":",String(Size(P)),",
      "\"P_to_BQ_onto\":",V6Json(pOnto),",\"P_to_BQ_kernel_order\":",V6Json(pKer),",
      "\"marked_images_pass\":",V6Json(markedPass),",\"pure_P_order\":",String(Size(PP)),",
      "\"pure_to_M_onto\":",V6Json(pureOnto),",\"pure_to_M_kernel_order\":",V6Json(pureKer),",
      "\"N_le_M\":",V6Json(nLeM),",\"N_le_M_proof\":\"kernel composition B3_to_P_to_BQ\",",
      "\"coface_count\":5,\"coface_relation_pass\":",V6Json(cofaceRelPass),",
      "\"pb3_candidate_relation_pass\":",V6Json(pRelPass),",\"finite_factor_inverse_pass\":",V6Json(pJPass),",
      "\"coface_inverse_kernel_inclusion\":",V6Json(cofaceFactors),",\"N_PB3_intersection_exact\":",V6Json(nExact),",
      "\"center_order\":",String(Order(center)),",\"center_central\":",V6Json(centerCentral),",
      "\"finite_cell_gate\":",V6Json(finiteCell),",\"row_status\":",JStr(rowStatus),",
      "\"row_bits\":",V6Json(rowBits),",\"fail_indices\":",V6Json(fails),",
      "\"zero_fiber_count\":",V6Json(zeroCount),",
      "\"b4_normality\":\"UNKNOWN\",\"isolated\":\"UNKNOWN\",\"all_shadows_settled\":\"UNKNOWN\",",
      "\"semantic_M_name\":\"M=K^(9) intersect N_S4\",\"semantic_M_binding_exact\":false,",
      "\"canonical_cert\":{\"path\":",JStr(canonPath),",\"sha256\":",JStr(canonSha),",\"rows_sha256\":",JStr(canonRowSha),\"row_count\":972,\"outside_648_identified\":false},",
      "\"source_word_artifact\":{\"path\":",JStr(V6Input),",\"sha256\":",JStr(wordsSha),\"row_count\":972,\"row_shape\":\"[m,key,word]\"},",
      "\"bridge\":{\"explicit_BQ\":true,\"kernel_C9\":",V6Json(pKer=9),",\"N_le_M\":",V6Json(nLeM),",\"b4_normality\":\"UNKNOWN\",\"isolated\":\"UNKNOWN\",\"settled\":\"UNKNOWN\",\"arithmetic_label\":\"UNAVAILABLE_TYPED_ARITHMETIC_BRIDGE\",\"outside_label\":\"UNAVAILABLE_TYPED_OUTSIDE_LABEL\",\"terminal_allowed\":false},",
      "\"provenance\":{\"gap_version\":",JStr(GAPInfo.Version),",\"infinite_fp_api_used\":false,\"producer\":\"d972_b4_k9_relative_c3_v6.g\"}}");
    Add(resultJsons,one);;
  od;
  out:=Concatenation(
    "{\"schema\":\"d972-b4-k9-relative-c3/v6\",\"status\":\"FINITE_C9_BQ_BRIDGE\",",
    "\"cell\":\"d972-k3-c3-exponent-v6\",\"BQ_order\":8817984,\"M_order\":1469664,",
    "\"radix\":",V6Json(radix),",\"results\":[",JoinC(resultJsons,","),"],",
    "\"frozen_972\":{\"row_count\":972,\"canonical_sha256\":",JStr(canonSha),",\"canonical_rows_sha256\":",JStr(canonRowSha),\"outside_648_identified\":false,\"word_sha256\":",JStr(wordsSha),",\"row_shape\":\"[m,key,word]\"},",
    "\"semantic_M_name\":\"M=K^(9) intersect N_S4\",\"semantic_M_binding_exact\":false,",
    "\"zero_fiber_count_total\":",String(totalZero),",\"computed_cells\":",String(computedCells),",
    "\"bridge\":{\"explicit_BQ\":true,\"kernel_C9_required\":true,\"N_le_M_required\":true,\"b4_normality\":\"UNKNOWN\",\"isolated\":\"UNKNOWN\",\"settled\":\"UNKNOWN\",\"outside_648_identified\":false,\"arithmetic_label\":\"UNAVAILABLE_TYPED_ARITHMETIC_BRIDGE\",\"outside_label\":\"UNAVAILABLE_TYPED_OUTSIDE_LABEL\",\"terminal_allowed\":false},",
    "\"provenance\":{\"gap_version\":",JStr(GAPInfo.Version),",\"infinite_fp_api_used\":false,\"producer\":\"d972_b4_k9_relative_c3_v6.g\"}}\n");
  WriteFile(V6Output,out);;
  Print("D972_B4_K9_RELATIVE_C3_V6_WRITTEN ",V6Output," cells=",Length(radix)," computed=",computedCells," zero=",totalZero,"\n");
fi;
