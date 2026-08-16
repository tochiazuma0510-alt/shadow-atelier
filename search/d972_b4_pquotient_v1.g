#############################################################################
## B4 pure-2 p-central quotient lane.  Repository-relative, versioned.
## GAP errors intentionally occur before the final artifact marker; absence
## of P2_ARTIFACT_WRITTEN is therefore an explicit incomplete run.
#############################################################################

D972P2LoadPrefix := function(path, marker)
  local src, at, tmp;
  src := StringFile(path);
  if src = fail then Error("P2: missing worker source"); fi;
  at := PositionSublist(src, marker);
  if at = fail then Error("P2: worker marker drift"); fi;
  tmp := Filename(DirectoryTemporary(), "d972_b4_p2_worker.g");
  FileString(tmp, src{[1..at-1]});
  Read(tmp);
end;;
if not IsBound(GetEnv) then GetEnv := name -> fail; fi;
P2WorkerPath := "search/d972_dovetail_worker_v1.g";;
P2SourcePath := "search/d972_b4_pquotient_v1.g";;
P2WorkerExpectedSha :=
  "323d18de4fadcf4561222995f5b6590bb560cd617048d2e9b54049ae3eea9efd";;
P2WorkerSource := StringFile(P2WorkerPath);;
P2SelfSource := StringFile(P2SourcePath);;
if P2WorkerSource=fail or P2SelfSource=fail then
  Error("P2: pinned source input missing");
fi;
P2WorkerSha := HexSHA256(P2WorkerSource);;
P2SelfSha := HexSHA256(P2SelfSource);;
if P2WorkerSha<>P2WorkerExpectedSha then
  Error("P2: worker source digest drift: ",P2WorkerSha);
fi;
D972P2SmallGrp := LoadPackage("smallgrp");;
D972P2Anupq := LoadPackage("anupq");;
if D972P2SmallGrp <> true or D972P2Anupq <> true then
  Error("P2: required packages unavailable (smallgrp/anupq)");
fi;
Print("P2_PACKAGES_PASS smallgrp=true anupq=true\n");
if IsBound(D972_P2_SELFTEST) and D972_P2_SELFTEST=true then
  Print("P2_SELFTEST_PASS source_sha256=",P2SelfSha,
    " worker_sha256=",P2WorkerSha,"\n");;
else
  D972P2LoadPrefix("search/d972_dovetail_worker_v1.g",
    "\nif D972Mode = \"selftest\" then");;

P2Json := function(x)
  local i, parts;
  if IsInt(x) then return String(x); fi;
  ## GAP classifies [] as a string as well as a list.  Preserve the
  ## identity signed word as an array in every finite-image receipt.
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    return Concatenation("\"", ReplacedString(x,"\"","\\\""), "\"");
  fi;
  if x = true then return "true"; fi;
  if x = false then return "false"; fi;
  if IsList(x) then
    parts := List([1..Length(x)], i -> P2Json(x[i]));
    return Concatenation("[", D972Join(parts, ","), "]");
  fi;
  Error("P2 JSON type drift");
end;;

P2Signed := function(w)
  local e, out, i, g, n, j;
  e := ExtRepOfObj(w); out := []; i := 1;
  while i <= Length(e) do
    g := e[i]; n := e[i+1];
    if n > 0 then for j in [1..n] do Add(out,g); od;
    else for j in [1..-n] do Add(out,-g); od; fi;
    i := i+2;
  od;
  return out;
end;;

P2PermImages := function(h0)
  local H, iso, Hp, degree;
  H := Group(h0); iso := IsomorphismPermGroup(H);
  if iso = fail then Error("P2: permutation image conversion failed"); fi;
  Hp := Image(iso); degree := LargestMovedPoint(Hp);
  if degree < 1 then degree := 1; fi;
  return List(h0, g -> List([1..degree], i -> i^Image(iso,g)));
end;;

P2Roof := function(rows, words, h0, rf, relsU)
  local F6, f6g, hp, rw, t, relok, rho5, eval, i, sw, z, k,
        fails, first;
  F6 := FreeGroup(6); f6g := GeneratorsOfGroup(F6);
  hp := []; rw := ShallowCopy(f6g);
  for t in [0..4] do
    Add(hp, List(rw, w -> MappedWord(w,f6g,h0)));
    rw := List(rw, w -> MappedWord(w,f6g,rf));
  od;
  rho5 := List(rw,w -> MappedWord(w,f6g,h0)) = h0;
  relok := List(relsU,r -> IsOne(MappedWord(r,
    GeneratorsOfGroup(UfpFree),h0)));
  eval := function(sw,a,b)
    local q,v;
    q := One(a);
    for v in sw do
      if v=1 then q:=q*a; elif v=2 then q:=q*b;
      elif v=-1 then q:=q*a^-1; elif v=-2 then q:=q*b^-1; fi;
    od;
    return q;
  end;
  fails := []; first := fail;
  for i in [1..Length(words)] do
    sw := words[i]; z := One(h0[1]);
    for t in Reversed([0..4]) do
      z := z * eval(sw,hp[t+1][1],hp[t+1][4]);
    od;
    if not IsOne(z) then
      Add(fails,i);
      if first=fail then first:=rec(index:=i,defect:=z); fi;
    fi;
  od;
  return rec(relok:=relok,rho5:=rho5,fails:=fails,first:=first);
end;;

P2RelWords := fail;; P2RhoWords := fail;; P2TargetKeys := fail;;
P2RoofWords := fail;; P2TargetDigest := fail;; P2RelDigest := fail;;
P2RoofDigest := fail;; P2WordKeyDigest := fail;; P2DefectReceipt := fail;;
P2ClassRows := [];;
P2SmallRows := [];;
Print("P2_ARTIFACT_PATH ci/out/d972_b4_pquotient_v1.json\n");
Print("P2_ARTIFACT_GATE final_marker_only\n");
Print("P2_BEGIN prime=2 class_bounds=1..5 collector_capacity=4096\n");

## Construct the exact U_M presentation (28 + 18*? rho closure = 158).
B := D972BuildBase(false);;
if B.pure_size <> 1469664 then Error("P2: pure base order drift"); fi;
Q0fp := Image(IsomorphismFpGroupByGenerators(
  B.compact_pure,[B.compact_x,B.compact_y],"p"));;
relsP := RelatorsOfFpGroup(Q0fp);;
Q0free:=FreeGroupOfFpGroup(Q0fp);;
F := FreeGroup("s1","s2","s3");;
B4 := F/[F.1*F.3*F.1^-1*F.3^-1,
  F.1*F.2*F.1*(F.2*F.1*F.2)^-1,
  F.2*F.3*F.2*(F.3*F.2*F.3)^-1];;
b1:=B4.1;; b2:=B4.2;; b3:=B4.3;;
X12:=b1^2;; X23:=b2^2;; X34:=b3^2;;
X13:=b2*b1^2*b2^-1;; X24:=b3*b2^2*b3^-1;; X14:=b3*X13*b3^-1;;
PB4sub:=Subgroup(B4,[X12,X13,X14,X23,X24,X34]);;
isoPB:=IsomorphismFpGroupByGenerators(PB4sub,
  [X12,X13,X14,X23,X24,X34],"x");;
PB4fp:=Image(isoPB);; Delta2img:=ImageElm(isoPB,(b1*b2*b3)^4);;
FPB:=FreeGroupOfFpGroup(PB4fp);;
K05:=FPB/Concatenation(RelatorsOfFpGroup(PB4fp),
  [UnderlyingElement(Delta2img)]);; gK:=GeneratorsOfGroup(K05);;
k12:=gK[1];; k13:=gK[2];; k14:=gK[3];;
k23:=gK[4];; k24:=gK[5];; k34:=gK[6];;
rhoImgs:=[(k14*k24*k34)^-1,k14,k24,
  (k12*k13*k14)^-1,(k12*k23*k24)^-1,k12];;
FK:=FreeGroupOfFpGroup(K05);; fgens:=GeneratorsOfGroup(FK);;
relsK:=RelatorsOfFpGroup(K05);;
if Number(relsK,r->not IsOne(MappedWord(r,fgens,rhoImgs)))<>0 then
  Error("P2: rho does not preserve K05 relators");
fi;
rhoHom:=GroupHomomorphismByImagesNC(K05,K05,gK,rhoImgs);;
fPure:=GeneratorsOfGroup(Q0free);;
baseJ:=List(relsP,r->MappedWord(r,fPure,[k12,k23]));;
allJ:=[];; cur:=baseJ;;
for j in [0..4] do Append(allJ,List(cur,UnderlyingElement));;
  cur:=List(cur,w->Image(rhoHom,w));;
od;;
Ufree:=FK;;
Ufp:=Ufree/Concatenation(relsK,allJ);;
relsU:=RelatorsOfFpGroup(Ufp);;
if Length(relsU)<>158 then Error("P2: U relator count drift"); fi;
UfpFree:=FreeGroupOfFpGroup(Ufp);;
Ugens:=GeneratorsOfGroup(Ufp);; Ufreen:=GeneratorsOfGroup(Ufree);;
F6:=FreeGroup(6);; F6g:=GeneratorsOfGroup(F6);;
rf:=[(F6g[3]*F6g[5]*F6g[6])^-1,F6g[3],F6g[5],
  (F6g[1]*F6g[2]*F6g[3])^-1,
  (F6g[1]*F6g[4]*F6g[5])^-1,F6g[1]];;
P2RhoWords:=List(rf,P2Signed);; P2RelWords:=List(relsU,P2Signed);;
P2RelDigest:=HexSHA256(P2Json(P2RelWords));;
if P2RelDigest<>"12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e" then
  Error("P2: frozen relator digest drift");
fi;

## Exact 972 roof rows and independent key/word correspondence.
R:=D972ScanCalibrationBase(B);;
if R.shadow_count<>972 then Error("P2: roof count drift"); fi;
## R.target_keys is the sorted Set(keys), not the shadow enumeration order.
## Receipts zip target_keys with roof_words, so retain the per-shadow order
## here and independently recompute the frozen set digest.
P2TargetKeys:=List(R.shadows,sh->sh.key);;
if Length(Set(P2TargetKeys))<>972 then
  Error("P2: shadow target-key enumeration is not unique");
fi;
P2TargetDigest:=HexSHA256(Concatenation(
  D972Join(Set(P2TargetKeys),"\n"),"\n"));;
if P2TargetDigest<>R.target_key_set_sorted_sha256 or
   P2TargetDigest<>"9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62" then
  Error("P2: target-key set digest drift");
fi;
## D972ScanCalibrationBase stores sh.f in fullF2=Group(s1^2,s2^2).
## Pull it back through the explicit marked full->compact isomorphism before
## asking the compact F2 epimorphism for a word; direct PreImagesRepresentative
## on the foreign fullF2 element is not a valid round-trip gate.
P2FullF2:=Group(B.s1^2,B.s2^2);;
P2FromFull:=GroupHomomorphismByImages(P2FullF2,B.compact_pure,
  [B.s1^2,B.s2^2],[B.compact_x,B.compact_y]);;
if P2FromFull=fail or not IsBijective(P2FromFull) then
  Error("P2: fullF2 to compact_pure marked isomorphism failed");
fi;
## One stable F2 domain is used for every row; no factorwise words are joined.
P2F2:=FreeGroup("u","v");;
P2Epi:=GroupHomomorphismByImages(P2F2,B.compact_pure,
  [P2F2.1,P2F2.2],[B.compact_x,B.compact_y]);;
P2RoofWords:=[];;
for P2Sh in R.shadows do
  P2CompactF:=Image(P2FromFull,P2Sh.f);;
  P2Pre:=PreImagesRepresentative(P2Epi,P2CompactF);;
  if P2Pre=fail or Image(P2Epi,P2Pre)<>P2CompactF then
    Error("P2: compact F2 preimage round-trip failed");
  fi;
  Add(P2RoofWords,P2Signed(P2Pre));
od;
if Length(P2RoofWords)<>972 then Error("P2: roof words drift"); fi;
P2RoofDigest:=HexSHA256(P2Json(P2RoofWords));;

## Bind the P2 reconstruction to the independently checked word/key table.
## The archived artifact hashes canonical rows [m,nested_key,signed_word]
## after sorting by the nested key.  Rebuild precisely that row stream here;
## a producer-controlled roof-word list or target-key list alone is not enough
## for a finite-image receipt to pass the independent checker.
P2ListLess:=function(a,b)
  local i, av, bv;
  if IsInt(a) and IsInt(b) then return a<b; fi;
  if not (IsList(a) and IsList(b)) then Error("P2: key comparator type drift"); fi;
  for i in [1..Minimum(Length(a),Length(b))] do
    av:=a[i]; bv:=b[i];
    if av=bv then continue; fi;
    return P2ListLess(av,bv);
  od;
  return Length(a)<Length(b);
end;;
P2WordKeyRows:=List([1..Length(R.shadows)],i->[
  R.shadows[i].m,
  [R.shadows[i].m,
   D972Can9(D972BlockRestrict(R.shadows[i].f,0,27)),
   D972Can4(D972BlockRestrict(R.shadows[i].f,27,9))],
  P2RoofWords[i]]);;
Sort(P2WordKeyRows,function(a,b) return P2ListLess(a[2],b[2]); end);;
if Length(Set(List(P2WordKeyRows,r->P2Json(r[2]))))<>972 then
  Error("P2: duplicate reconstructed word/key target");
fi;
P2WordKeyDigest:=HexSHA256(P2Json(P2WordKeyRows));;
if P2WordKeyDigest<>"283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930" then
  Error("P2: independently pinned word/key artifact digest drift: ",P2WordKeyDigest);
fi;
Print("P2_PRESENTATION_PASS relators=158 roof=972 target_digest=",P2TargetDigest,"\n");
Print("P2_WORD_KEY_BINDING_PASS digest=",P2WordKeyDigest,"\n");

if IsBound(D972_P2_MAGNUS_ONLY) and D972_P2_MAGNUS_ONLY=true then
  Read("search/d972_b4_p2_magnus_export_v1.g");;
  QUIT;
fi;

P2MakeReceipt:=function(label,order,h0,scan,epiIndex,epiCount)
  local H,iso,Hp,degree,wit,defect;
  H:=Group(h0);; iso:=IsomorphismPermGroup(H);;
  if iso=fail then Error("P2: finite image is not permutationizable"); fi;
  Hp:=Image(iso);; degree:=LargestMovedPoint(Hp);; if degree<1 then degree:=1; fi;
  wit:=scan.first;; defect:=Image(iso,wit.defect);
  return Concatenation(
    "{\"schema\":\"d972-b4-finite-image/v2\",\"target\":",P2Json(label),
    ",\"target_order\":",String(order),",\"epi_index\":",String(epiIndex),
    ",\"epi_count\":",String(epiCount),",\"h_images\":",
    P2Json(List(h0,g->List([1..degree],i->i^Image(iso,g)))),
    ",\"rho_words\":",P2Json(P2RhoWords),
    ",\"all_relators\":",P2Json(P2RelWords),
    ",\"all_relators_sha256\":",P2Json(P2RelDigest),
    ",\"relator_bools\":",P2Json(scan.relok),",\"rho5\":",P2Json(scan.rho5),
    ",\"target_keys\":",P2Json(P2TargetKeys),
    ",\"target_key_digest\":",P2Json(P2TargetDigest),
    ",\"roof_words\":",P2Json(P2RoofWords),
    ",\"roof_words_sha256\":",P2Json(P2RoofDigest),
    ",\"witness_index\":",String(wit.index),
    ",\"witness_word\":",P2Json(P2RoofWords[wit.index]),
    ",\"expected_defect\":",P2Json(List([1..degree],i->i^defect)),
    ",\"word_key_artifact_sha256\":",P2Json(P2WordKeyDigest),"}");
end;;

## SmallGroup targets: Q8=(8,4), D8=(8,3), and every group of order 16.
if IdGroup(SmallGroup(8,4))<>[8,4] then Error("P2: Q8 SmallGroup id drift"); fi;
if IdGroup(SmallGroup(8,3))<>[8,3] then Error("P2: D8 SmallGroup id drift"); fi;
P2ScanTarget:=function(label,G)
  local qs, count, i, epi, h0, scan, row, id, out;
  id:=IdGroup(G);; Print("P2_SG_BEGIN label=",label," id=",id," order=",Size(G),"\n");
  qs:=GQuotients(Ufp,G:findall:=true);; count:=Length(qs);; i:=0;
  for epi in qs do i:=i+1;; h0:=List(Ugens,g->Image(epi,g));;
    scan:=P2Roof(R.shadows,P2RoofWords,h0,rf,relsU);;
    row:=Concatenation("{\"label\":",P2Json(label),",\"id\":",P2Json(id),
      ",\"order\":",String(Size(G)),",\"epi_index\":",String(i),
      ",\"epi_count\":",String(count),",\"relator_bad\":",String(Number(scan.relok,x->not x)),
      ",\"rho5\":",P2Json(scan.rho5),",\"roof_fail_count\":",String(Length(scan.fails)),"}");
    Add(P2SmallRows,row);
    if scan.first<>fail and P2DefectReceipt=fail then
      P2DefectReceipt:=P2MakeReceipt(label,Size(G),h0,scan,i,count);
    fi;
  od;;
  Print("P2_SG_DONE label=",label," epis=",count,"\n");
end;;
P2ScanTarget("Q8_8_4",SmallGroup(8,4));;
P2ScanTarget("D8_8_3",SmallGroup(8,3));;
for i in [1..NumberSmallGroups(16)] do
  P2ScanTarget(Concatenation("SG16_",String(i)),SmallGroup(16,i));
od;;

## p=2 lower exponent-2 / p-central quotients, class 1..5.
for cls in [1..5] do
  Print("P2_CLASS_BEGIN class=",cls,"\n");;
  qs:=PQuotient(Ufp,2,cls,4096,"combinatorial":noninteractive);;
  if qs=fail then
    Add(P2ClassRows,Concatenation("{\"class_bound\":",String(cls),
      ",\"status\":\"UNKNOWN_RESOURCE\"}"));
    Print("P2_CLASS_UNKNOWN class=",cls," reason=collector_capacity\n");;
    continue;
  fi;
  phi:=EpimorphismQuotientSystem(qs);; H:=Image(phi);;
  h0:=List(Ugens,g->Image(phi,g));;
  scan:=P2Roof(R.shadows,P2RoofWords,h0,rf,relsU);;
  status:="ALLPASS";; if Length(scan.fails)>0 then status:="DEFECT"; fi;
  Add(P2ClassRows,Concatenation("{\"class_bound\":",String(cls),
    ",\"status\":",P2Json(status),",\"order\":",String(Size(H)),
    ",\"relator_bad\":",String(Number(scan.relok,x->not x)),
    ",\"rho5\":",P2Json(scan.rho5),",\"roof_count\":972,\"roof_fail_count\":",
    String(Length(scan.fails)),"}"));
  Print("P2_CLASS_DONE class=",cls," order=",Size(H),
    " relator_bad=",Number(scan.relok,x->not x)," rho5=",scan.rho5,
    " roof_fails=",Length(scan.fails),"\n");
  if Length(scan.fails)>0 and P2DefectReceipt=fail then
    P2DefectReceipt:=P2MakeReceipt(Concatenation("p2_class_",String(cls)),
      Size(H),h0,scan,1,1);
  fi;
od;;

if P2DefectReceipt=fail then P2DefectReceipt:="null"; fi;
P2ClassesJson:=Concatenation("[",D972Join(P2ClassRows,","),"]");;
P2SmallJson:=Concatenation("[",D972Join(P2SmallRows,","),"]");;
P2Status:="UNKNOWN";;
if ForAny(P2ClassRows,x->PositionSublist(x,"DEFECT")<>fail) then
  P2Status:="DEFECT";
fi;
if P2DefectReceipt<>"null" then P2Status:="DEFECT"; fi;
P2Out:=Concatenation(
  "{\"schema\":\"d972-b4-pquotient/v1\",\"status\":",
  P2Json(P2Status),
  ",\"source_sha256\":",P2Json(P2SelfSha),
  ",\"worker_sha256\":",P2Json(P2WorkerSha),
  ",\"prime\":2,\"collector\":\"combinatorial\",\"collector_capacity\":4096",
  ",\"class_bounds\":[1,2,3,4,5],\"relator_count\":158,\"roof_count\":972",
  ",\"all_relators_sha256\":",P2Json(P2RelDigest),
  ",\"target_key_digest\":",P2Json(P2TargetDigest),
  ",\"roof_words_sha256\":",P2Json(P2RoofDigest),
  ",\"word_key_artifact_sha256\":",P2Json(P2WordKeyDigest),
  ",\"classes\":",P2ClassesJson,",\"smallgroup_scans\":",P2SmallJson,
  ",\"defect_receipt\":",P2DefectReceipt,"}");
WriteFile("ci/out/d972_b4_pquotient_v1.json",Concatenation(P2Out,"\n"));;
Print("P2_ARTIFACT_WRITTEN ci/out/d972_b4_pquotient_v1.json\n");
fi;
QUIT;
