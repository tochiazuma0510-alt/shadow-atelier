#############################################################################
## B4 pure-2 p-central quotient lane.  Repository-relative, versioned.
## GAP errors intentionally occur before the final marker; the runner gates on
## the marker and on GAP's syntax/error diagnostics (especially selftest).
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
D972P2Json := LoadPackage("json");;
if D972P2SmallGrp <> true or D972P2Anupq <> true or D972P2Json <> true then
  Error("P2: required packages unavailable (smallgrp/anupq/json)");
fi;
Print("P2_PACKAGES_PASS smallgrp=true anupq=true json=true\n");
if IsBound(D972_P2_SELFTEST) and D972_P2_SELFTEST=true then
  P2RunMode:="selftest";;
  Print("P2_SELFTEST_PASS source_sha256=",P2SelfSha,
    " worker_sha256=",P2WorkerSha,"\n");;
else
  P2RunMode:="full";;
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

P2Roof := function(words, h0, rf, relsU)
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

## Keep the worker's base-order gate, but materialize the finite-image input
## from the independently pinned Magnus artifact.  Re-running
## IsomorphismFpGroupByGenerators here is not deterministic across GAP builds:
## RelatorsOfFpGroup can return a different (shortened/reordered) presentation.
B := D972BuildBase(false);;
if B.pure_size <> 1469664 then Error("P2: pure base order drift"); fi;

P2InputPath := "search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
P2InputSource := StringFile(P2InputPath);;
if P2InputSource=fail then Error("P2: pinned Magnus input missing"); fi;
P2InputFileSha := HexSHA256(P2InputSource);;
if P2InputFileSha<>"c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9" then
  Error("P2: pinned Magnus input file digest drift: ",P2InputFileSha);
fi;
P2Input := JsonStringToGap(P2InputSource);;
if P2Input=fail or not IsRecord(P2Input) or
   not IsBound(P2Input.schema) or
   P2Input.schema<>"d972-b4-p2-magnus-input/v2" or
   not IsBound(P2Input.rho_words_source) or
   P2Input.rho_words_source<>"universal_v2_canonical" then
  Error("P2: pinned Magnus input schema drift");
fi;
Print("P2_PINNED_INPUT_COUNTS relators=",Length(P2Input.all_relators),
  " rho_words=",Length(P2Input.rho_words),
  " target_keys=",Length(P2Input.target_keys),
  " roof_words=",Length(P2Input.roof_words),"\n");
if P2Input.relator_count<>158 or P2Input.roof_count<>972 or
   Length(P2Input.all_relators)<>158 or Length(P2Input.rho_words)<>6 or
   Length(P2Input.target_keys)<>972 or Length(P2Input.roof_words)<>972 then
  Error("P2: pinned Magnus input count drift");
fi;

F6:=FreeGroup(6);; F6g:=GeneratorsOfGroup(F6);;
P2WordFromSigned:=function(signed)
  local w,x;
  w:=One(F6);;
  for x in signed do
    if x=0 or AbsInt(x)>6 then Error("P2: signed word letter drift"); fi;
    if x>0 then w:=w*F6g[x]; else w:=w*F6g[-x]^-1; fi;
  od;
  return w;
end;;
P2RelWords:=List(P2Input.all_relators,ShallowCopy);;
P2RelDigest:=HexSHA256(P2Json(P2RelWords));;
if P2RelDigest<>P2Input.all_relators_sha256 or
   P2RelDigest<>"12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e" then
  Error("P2: pinned relator digest drift: ",P2RelDigest);
fi;
## The quotient presentation is now exactly the 158 signed rows above.
## Do not call RelatorsOfFpGroup to recover/rewrite these rows.
P2RelGroupWords:=List(P2RelWords,P2WordFromSigned);;
Ufree:=F6;; Ufp:=Ufree/P2RelGroupWords;;
UfpFree:=Ufree;; relsU:=P2RelGroupWords;;
Ugens:=GeneratorsOfGroup(Ufp);; Ufreen:=GeneratorsOfGroup(Ufree);;
P2RhoWords:=List(P2Input.rho_words,ShallowCopy);;
if P2RhoWords<>[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]] then
  Error("P2: canonical universal rho word drift");
fi;
rf:=List(P2RhoWords,P2WordFromSigned);;
if rf<>[(F6g[3]*F6g[5]*F6g[6])^-1,F6g[3],F6g[5],
       (F6g[1]*F6g[2]*F6g[3])^-1,
       (F6g[1]*F6g[4]*F6g[5])^-1,F6g[1]] then
  Error("P2: canonical universal rho reconstruction drift");
fi;

P2TargetKeys:=List(P2Input.target_keys,ShallowCopy);;
if Length(Set(P2TargetKeys))<>972 then
  Error("P2: pinned target-key enumeration is not unique");
fi;
P2TargetDigest:=HexSHA256(Concatenation(
  D972Join(Set(P2TargetKeys),"\n"),"\n"));;
if P2TargetDigest<>P2Input.target_key_digest or
   P2TargetDigest<>"9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62" then
  Error("P2: pinned target-key digest drift: ",P2TargetDigest);
fi;
P2RoofWords:=List(P2Input.roof_words,ShallowCopy);;
P2RoofDigest:=HexSHA256(P2Json(P2RoofWords));;
if P2RoofDigest<>P2Input.roof_words_sha256 or
   P2RoofDigest<>"3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8" then
  Error("P2: pinned roof-word digest drift: ",P2RoofDigest);
fi;

## Independently authenticate the corrected word/key archive and bind its
## exact pairs to the pinned Magnus rows.  This replaces the old 972-shadow
## rescan while retaining the load-bearing correspondence gate.
P2ArtifactPath := "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
P2ArtifactSource := StringFile(P2ArtifactPath);;
if P2ArtifactSource=fail then Error("P2: word/key artifact missing"); fi;
P2Artifact:=JsonStringToGap(P2ArtifactSource);;
if P2Artifact=fail or not IsRecord(P2Artifact) or
   P2Artifact.schema<>"d972-b4-word-key-artifact/v1" or
   P2Artifact.count<>972 or Length(P2Artifact.rows)<>972 or
   P2Artifact.source_target_key_digest<>P2TargetDigest or
   P2Artifact.frozen_tuple_sha256<>"32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91" then
  Error("P2: word/key artifact metadata drift");
fi;
P2WordKeyRows:=P2Artifact.rows;;
P2WordKeyDigest:=HexSHA256(P2Json(P2WordKeyRows));;
if P2WordKeyDigest<>P2Artifact.canonical_bytes_sha256 or
   P2WordKeyDigest<>"283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930" then
  Error("P2: independently pinned word/key artifact digest drift: ",P2WordKeyDigest);
fi;
P2ArtifactFlatKey:=function(key)
  local can9,can9flat,can4;
  if not IsList(key) or Length(key)<>3 then Error("P2: artifact key shape drift"); fi;
  can9:=key[2];; can4:=key[3];;
  if not IsList(can9) or Length(can9)<>3 or
     not IsList(can4) or Length(can4)<>9 then
    Error("P2: artifact key coordinates drift");
  fi;
  can9flat:=Concatenation(can9[1],can9[2],can9[3]);;
  return Concatenation("(",String(key[1]),";",
    D972Join(List(can9flat,String),","),";",
    D972Join(List(can4,String),","),")");
end;;
P2ArtifactPairs:=Set(List(P2WordKeyRows,r->P2Json([
  P2ArtifactFlatKey(r[2]),r[3]])));;
P2InputPairs:=Set(List([1..972],i->P2Json([
  P2TargetKeys[i],P2RoofWords[i]])));;
if P2ArtifactPairs<>P2InputPairs then
  Error("P2: pinned Magnus rows do not match word/key artifact");
fi;
Print("P2_PRESENTATION_PASS relators=158 rel_digest=",P2RelDigest,
  " roof=972 roof_digest=",P2RoofDigest,
  " input_sha256=",P2InputFileSha,"\n");
Print("P2_WORD_KEY_BINDING_PASS digest=",P2WordKeyDigest,"\n");

if IsBound(D972_P2_MAGNUS_ONLY) and D972_P2_MAGNUS_ONLY=true then
  P2RunMode:="magnus";;
  Read("search/d972_b4_p2_magnus_export_v2.g");;
else
  P2RunMode:="full";;
fi;

if P2RunMode="full" then
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
    ",\"rho_words_source\":\"universal_v2_canonical\"",
    ",\"rho_words_sha256\":\"23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed\"",
    ",\"source_sha256\":",P2Json(P2InputFileSha),
    ",\"rho_words_legacy_json_mismatch\":false",
    ",\"p2_input_schema\":\"d972-b4-p2-magnus-input/v2\"",
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
    ",\"word_key_artifact_sha256\":",P2Json(P2WordKeyDigest),
    ",\"p2_input_file_sha256\":",P2Json(P2InputFileSha),"}");
end;;

## SmallGroup targets: Q8=(8,4), D8=(8,3), and every group of order 16.
if IdGroup(SmallGroup(8,4))<>[8,4] then Error("P2: Q8 SmallGroup id drift"); fi;
if IdGroup(SmallGroup(8,3))<>[8,3] then Error("P2: D8 SmallGroup id drift"); fi;
P2ScanTarget:=function(label,G)
  local qs, count, i, epi, h0, scan, row, id, out;
  id:=IdGroup(G);; Print("P2_SG_BEGIN label=",label," id=",id," order=",Size(G),"\n");
  qs:=GQuotients(Ufp,G:findall:=true);; count:=Length(qs);; i:=0;
  for epi in qs do i:=i+1;; h0:=List(Ugens,g->Image(epi,g));;
    scan:=P2Roof(P2RoofWords,h0,rf,relsU);;
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
  scan:=P2Roof(P2RoofWords,h0,rf,relsU);;
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
  ",\"p2_input_file_sha256\":",P2Json(P2InputFileSha),
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
fi;
if P2RunMode="selftest" then
  Print("P2_SELFTEST_FINAL_MARKER source_sha256=",P2SelfSha,
    " worker_sha256=",P2WorkerSha,"\n");
else
  Print("P2_FINAL_MARKER mode=",P2RunMode,"\n");
fi;
