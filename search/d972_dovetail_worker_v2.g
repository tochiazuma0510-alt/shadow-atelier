#############################################################################
## d972_dovetail_worker_v2.g
##
## DMTCP-safe exact worker for the D972 relative-extension dovetail.
##
## The mathematical routines are the frozen v1 routines below the v1 dispatch
## boundary.  This file adds a v2 receipt envelope and a resumability contract.
## In particular, resumability is never inferred from an outer tuple cursor:
## GAP state inside canonical relabelling, Aut(H), MTC/fp-order, and the full
## 972-fibre scan is recoverable only when the workflow launches this process
## under DMTCP and independently seals the checkpoint-image manifest.
##
## Required for a resumable workflow receipt:
##   D972_DMTCP_ENABLED=1
##   D972_DMTCP_CONTRACT_SHA256=<64 lowercase hexadecimal characters>
## Optional provenance bindings:
##   D972_DMTCP_VERSION, D972_DMTCP_GENERATION,
##   D972_DMTCP_IMAGE_MANIFEST_SHA256, D972_UNIVERSE_ID,
##   D972_INPUT_DIGEST, D972_TASK_DIGEST, D972_HEARTBEAT
##
## D972_HEARTBEAT is an overwrite-only, non-authoritative diagnostic file.
## Only the final v2 result envelope has authority to complete/advance a cell.
#############################################################################

D972V2V1Path := "search/d972_dovetail_worker_v1.g";;
D972V2ExpectedV1SHA256 :=
  "f9ad3f8f71dc5af3d20dbef66dc6a25c79a50393be55767c0fb9f077d46994e8";;
D972V2CompatNeedle := "Size(Group(a1,a2))";;
D972V2CompatReplacement :=
  "D972V2MappingGroupOrder([a1,a2],G9)";;
D972V2CompatReplacementCount := 1;;
D972V2QtCompatNeedle := "Size(Group(qt9.s1,qt9.s2))";;
D972V2QtCompatReplacement :=
  "D972V2PointActionGroupOrder([qt9.s1,qt9.s2],6*Size(G9))";;
D972V2QtCompatReplacementCount := 1;;
D972V2Qt4CompatNeedle := "Size(Group(qt4.s1,qt4.s2))";;
D972V2Qt4CompatReplacement :=
  "D972V2PointActionGroupOrder([qt4.s1,qt4.s2],6*Size(P4))";;
D972V2Qt4CompatReplacementCount := 1;;
D972V2MtcNeedle := "PresentationSubgroupMtc(P, Hsub, \"h\", 0)";;
D972V2MtcReplacement := "PresentationSubgroupMtc(P, Hsub, \"h\")";;
D972V2MtcReplacementCount := 1;;

## GAP 4.12 can reject otherwise-valid permutation pairs passed through the
## two-argument Group(a,b) dispatcher.  These needles are restricted to the
## base-audit path, where every permutation degree/parent is exact and fixed.
## The v1 source remains immutable; D972V2LoadV1Library applies these rewrites
## only to its temporary in-memory library copy.
D972V2BaseQNeedle := "Q := Group(s1,s2);";;
D972V2BaseQReplacement :=
  "Q := D972V2PermutationGroup([s1,s2],6*2916+6*504,\"base_q\");";;
D972V2BaseQReplacementCount := 1;;
D972V2BasePureNeedle := "pureSize := Size(Group(s1^2,s2^2));";;
D972V2BasePureReplacement :=
  "pureSize := Size(D972V2PermutationGroup([s1^2,s2^2],6*2916+6*504,\"base_pure\"));";;
D972V2BasePureReplacementCount := 1;;
D972V2BaseCompactNeedle := "compactPure:=Group(compactX,compactY);";;
D972V2BaseCompactReplacement :=
  "compactPure:=D972V2PermutationGroup([compactX,compactY],27+9,\"base_compact_pure\");";;
D972V2BaseCompactReplacementCount := 1;;
D972V2BaseFullPureNeedle := "fullF2:=Group(x,y);";;
D972V2BaseFullPureReplacement :=
  "fullF2:=D972V2PermutationGroup([x,y],6*2916+6*504,\"base_full_pure\");";;
D972V2BaseFullPureReplacementCount := 1;;
D972V2BaseShortcutNeedle := Concatenation(
  "Size(Group(compactX^u,\n",
  "             AbstractProd([f^-1,compactY^u,f])))");;
D972V2BaseShortcutReplacement := Concatenation(
  "Size(D972V2PermutationGroup([compactX^u,\n",
  "             AbstractProd([f^-1,compactY^u,f])],27+9,\"base_shortcut_pure\"))");;
D972V2BaseShortcutReplacementCount := 1;;
D972V2BaseSurjNeedle := "if Size(Group(img1,img2))<>Size(P) then";;
D972V2BaseSurjReplacement :=
  "if Size(D972V2PermutationGroup([img1,img2],6*2916+6*504,\"base_scan_surjectivity\"))<>Size(P) then";;
D972V2BaseSurjReplacementCount := 1;;
D972V2SmallC2Needle := "S:=Group(qt.s1,qt.s2); degree:=6*Size(C2);";;
D972V2SmallC2Replacement :=
  "degree:=6*Size(C2); S:=D972V2PermutationGroup([qt.s1,qt.s2],degree,\"small_c2\");";;
D972V2SmallC2ReplacementCount := 1;;
D972V2SmallQ8Needle := "S:=Group(qt.s1,qt.s2); degree:=6*Size(q8.G);";;
D972V2SmallQ8Replacement :=
  "degree:=6*Size(q8.G); S:=D972V2PermutationGroup([qt.s1,qt.s2],degree,\"small_q8\");";;
D972V2SmallQ8ReplacementCount := 1;;
D972V2CombinedPNeedle := "P:=Group(s1,s2);";;
D972V2CombinedPReplacement :=
  "P:=D972V2PermutationGroup([s1,s2],baseDegree+M.degree,\"combined_full\");";;
D972V2CombinedPReplacementCount := 1;;
D972V2CombinedSizeNeedle := "Size(Group(s1,s2))<>Size(P) or";;
D972V2CombinedSizeReplacement :=
  "Size(D972V2PermutationGroup([s1,s2],baseDegree+M.degree,\"combined_full_gate\"))<>Size(P) or";;
D972V2CombinedSizeReplacementCount := 1;;
D972V2CombinedF2Needle := "F2bar:=Group(s1^2,s2^2); cInF2:=c in F2bar;";;
D972V2CombinedF2Replacement :=
  "F2bar:=D972V2PermutationGroup([s1^2,s2^2],baseDegree+M.degree,\"combined_pure\"); cInF2:=c in F2bar;";;
D972V2CombinedF2ReplacementCount := 1;;
D972V2CombinedPureCNeedle := "Size(Group(s1^2,s2^2,c))<>Size(pure) or";;
D972V2CombinedPureCReplacement :=
  "Size(D972V2PermutationGroup([s1^2,s2^2,c],baseDegree+M.degree,\"combined_pure_with_c\"))<>Size(pure) or";;
D972V2CombinedPureCReplacementCount := 1;;
D972V2OrbitF2Needle := Concatenation(
  "C:=D972CalibrationCombinedModel(B,M);\n",
  "  P:=C.group; s1:=C.s1; s2:=C.s2; rho:=C.rho;\n",
  "  x:=s1^2; y:=s2^2; c:=C.c;\n",
  "  F2bar:=Group(x,y); D:=DerivedSubgroup(F2bar);");;
D972V2OrbitF2Replacement := Concatenation(
  "C:=D972CalibrationCombinedModel(B,M);\n",
  "  P:=C.group; s1:=C.s1; s2:=C.s2; rho:=C.rho;\n",
  "  x:=s1^2; y:=s2^2; c:=C.c;\n",
  "  F2bar:=D972V2PermutationGroup([x,y],B.component9_degree+\n",
  "    B.component4_degree+M.degree,\"orbit_pure\"); D:=DerivedSubgroup(F2bar);");;
D972V2OrbitF2ReplacementCount := 1;;
D972V2BaseDNeedle := "baseD:=DerivedSubgroup(Group(B.s1^2,B.s2^2));";;
D972V2BaseDReplacement :=
  "baseD:=DerivedSubgroup(D972V2PermutationGroup([B.s1^2,B.s2^2],B.component9_degree+B.component4_degree,\"base_derived\"));";;
D972V2BaseDReplacementCount := 1;;
D972V2OrbitSurjNeedle := "if Size(Group(img1,img2))=Size(P) then";;
D972V2OrbitSurjReplacement :=
  "if Size(D972V2PermutationGroup([img1,img2],B.component9_degree+B.component4_degree+M.degree,\"orbit_surjectivity\"))=Size(P) then";;
D972V2OrbitSurjReplacementCount := 1;;
D972V2BaseRewriteTotalCount := 15;;

D972V2PermutationGroup := function(generators, degree, stage)
  local imageOf, imageRows, perms, row, G;
  if not IsList(generators) or Length(generators) < 1 or degree < 1 then
    Error("D972 v2: permutation group needs generators and positive degree");
  fi;
  Print("D972V2_PERM_GROUP materialize_begin stage=",stage,
    " degree=",degree," generators=",Length(generators),"\n");
  imageOf := function(g, point)
    if IsPerm(g) then return point^g; fi;
    return Image(g,point);
  end;
  imageRows := List(generators, g -> List([1..degree],
    i -> imageOf(g,i)));
  if ForAny(imageRows, row -> Set(row) <> [1..degree]) then
    Error("D972 v2: permutation group generator left its finite point set");
  fi;
  perms := List(imageRows, row -> PermList(row));
  if ForAny(perms, p -> p=fail) then
    Error("D972 v2: permutation group materialization failed");
  fi;
  Print("D972V2_PERM_GROUP perms_constructed stage=",stage,
    " degree=",degree," generators=",Length(perms),"\n");
  G := Subgroup(SymmetricGroup(degree),perms);
  Print("D972V2_PERM_GROUP subgroup_done stage=",stage,
    " degree=",degree," order=",Size(G),"\n");
  return G;
end;;

D972V2CountNeedle := function(source, needle)
  local i, n;
  n := 0;
  for i in [1..Length(source)-Length(needle)+1] do
    if source{[i..i+Length(needle)-1]} = needle then n:=n+1; fi;
  od;
  return n;
end;;

D972V2Rewrite := function(source, needle, replacement, expected, label)
  local observed;
  observed := D972V2CountNeedle(source,needle);
  if observed <> expected then
    Error("D972 v2: GAP4.12 rewrite count drift label=",label,
      " observed=",observed," expected=",expected);
  fi;
  Print("D972V2_REWRITE label=",label," count=",observed,"\n");
  return ReplacedString(source,needle,replacement);
end;;

## Load all frozen v1 definitions without executing its mode dispatcher/QUIT.
## A temporary copy is used because the source is intentionally kept versioned
## and immutable.  The digest gate makes this dependency explicit.
## GAP 4.13 has no GetEnv global (GAP 4.14+ may provide one).  The frozen
## v1 library below calls GetEnv at load time, so install a compatibility
## accessor before reading it.  GAPInfo.SystemEnvironment is core GAP state;
## missing names intentionally return fail and are handled by the callers.
if not IsBound(GetEnv) then
  GetEnv := function(name)
    if IsBound(GAPInfo.SystemEnvironment) and
       IsBound(GAPInfo.SystemEnvironment.(name)) then
      return GAPInfo.SystemEnvironment.(name);
    fi;
    return fail;
  end;
fi;;

## GAP 4.13 does not necessarily autoload the small-groups library.  The
## frozen v1 kernel-catalog path requires these declarations; load it before
## reading v1 and fail closed if the pinned runtime lacks the package.
if LoadPackage("smallgrp") <> true then
  Error("D972 v2: required smallgrp package unavailable");
fi;;
if not IsBound(SmallGroupsAvailable) or not IsBound(AllSmallGroups) then
  Error("D972 v2: smallgrp API globals unavailable");
fi;;

D972V2LoadV1Library := function()
  local source, actual, marker, cut, dir, path, prefix;
  source := StringFile(D972V2V1Path);
  if source = fail then Error("D972 v2: could not read frozen v1 worker"); fi;
  actual := HexSHA256(source);
  if actual <> D972V2ExpectedV1SHA256 then
    Error("D972 v2: frozen v1 worker digest drift: ",actual);
  fi;
  source := ReplacedString(source,"\r\n","\n");
  marker := Concatenation("\nif D972Mode = ","\"selftest\" then");
  cut := PositionSublist(source,marker);
  if cut = fail then Error("D972 v2: v1 dispatch boundary not found"); fi;
  prefix := source{[1..cut-1]};
  ## GAP 4.12 compatibility-only materialization rewrites.  Every replacement
  ## is count-gated before it touches the temporary library copy.
  prefix := D972V2Rewrite(prefix,D972V2CompatNeedle,
    D972V2CompatReplacement,D972V2CompatReplacementCount,"mapping_group");
  prefix := D972V2Rewrite(prefix,D972V2QtCompatNeedle,
    D972V2QtCompatReplacement,D972V2QtCompatReplacementCount,"qt9_group");
  prefix := D972V2Rewrite(prefix,D972V2Qt4CompatNeedle,
    D972V2Qt4CompatReplacement,D972V2Qt4CompatReplacementCount,"qt4_group");
  prefix := D972V2Rewrite(prefix,D972V2MtcNeedle,
    D972V2MtcReplacement,D972V2MtcReplacementCount,"mtc_group");
  prefix := D972V2Rewrite(prefix,D972V2BaseQNeedle,
    D972V2BaseQReplacement,D972V2BaseQReplacementCount,"base_q");
  prefix := D972V2Rewrite(prefix,D972V2BasePureNeedle,
    D972V2BasePureReplacement,D972V2BasePureReplacementCount,"base_pure");
  prefix := D972V2Rewrite(prefix,D972V2BaseCompactNeedle,
    D972V2BaseCompactReplacement,D972V2BaseCompactReplacementCount,
    "base_compact_pure");
  prefix := D972V2Rewrite(prefix,D972V2BaseFullPureNeedle,
    D972V2BaseFullPureReplacement,D972V2BaseFullPureReplacementCount,
    "base_full_pure");
  prefix := D972V2Rewrite(prefix,D972V2BaseShortcutNeedle,
    D972V2BaseShortcutReplacement,D972V2BaseShortcutReplacementCount,
    "base_shortcut_pure");
  prefix := D972V2Rewrite(prefix,D972V2BaseSurjNeedle,
    D972V2BaseSurjReplacement,D972V2BaseSurjReplacementCount,
    "base_scan_surjectivity");
  prefix := D972V2Rewrite(prefix,D972V2SmallC2Needle,
    D972V2SmallC2Replacement,D972V2SmallC2ReplacementCount,"small_c2");
  prefix := D972V2Rewrite(prefix,D972V2SmallQ8Needle,
    D972V2SmallQ8Replacement,D972V2SmallQ8ReplacementCount,"small_q8");
  prefix := D972V2Rewrite(prefix,D972V2CombinedPNeedle,
    D972V2CombinedPReplacement,D972V2CombinedPReplacementCount,
    "combined_full");
  prefix := D972V2Rewrite(prefix,D972V2CombinedSizeNeedle,
    D972V2CombinedSizeReplacement,D972V2CombinedSizeReplacementCount,
    "combined_size");
  prefix := D972V2Rewrite(prefix,D972V2CombinedF2Needle,
    D972V2CombinedF2Replacement,D972V2CombinedF2ReplacementCount,
    "combined_pure");
  prefix := D972V2Rewrite(prefix,D972V2CombinedPureCNeedle,
    D972V2CombinedPureCReplacement,D972V2CombinedPureCReplacementCount,
    "combined_pure_with_c");
  prefix := D972V2Rewrite(prefix,D972V2OrbitF2Needle,
    D972V2OrbitF2Replacement,D972V2OrbitF2ReplacementCount,"orbit_pure");
  prefix := D972V2Rewrite(prefix,D972V2BaseDNeedle,
    D972V2BaseDReplacement,D972V2BaseDReplacementCount,"base_derived");
  prefix := D972V2Rewrite(prefix,D972V2OrbitSurjNeedle,
    D972V2OrbitSurjReplacement,D972V2OrbitSurjReplacementCount,
    "orbit_surjectivity");
  dir := DirectoryTemporary();
  if dir = fail then Error("D972 v2: no temporary directory"); fi;
  path := Filename(dir,"d972_dovetail_worker_v1_library.g");
  ## FileString is the byte-faithful writer on GAP 4.13.  PrintTo is
  ## stream/printing oriented and can abbreviate a large string, which
  ## corrupts the generated v1 prefix at a token boundary.
  FileString(path,prefix);
  actual := StringFile(path);
  if actual <> prefix then
    Error("D972 v2: generated v1 library is not byte-faithful");
  fi;
  Read(path);
end;;

D972V2LoadV1Library();;

## GAP 4.12.1 does not classify general bijective mappings as
## IsGeneratorsOfMagmaWithInverses, so even the list-plus-identity Group form
## is rejected.  Materialize the finite action on the source group as a
## permutation group before taking its order.  Use the explicit Subgroup
## parent/generator-list form: GAP 4.12's Group(list) and Group(p,q)
## dispatches are both version-sensitive here.  This is only the K9
## B3-action compatibility gate; the frozen v1 mappings and all mathematical
## data stay unchanged.
D972V2MappingGroupOrder := function(maps, source)
  local elements, imageRows, perms, order;
  elements := AsSSortedList(source);
  Print("D972V2_MAPPING_STAGE materialize_begin n=",Length(elements),"\n");
  if Length(elements) <> Size(source) or
     not ForAll(maps, map -> IsBijective(map) and
       Image(map,One(source))=One(source)) then
    Error("D972 v2: mapping action is not a finite automorphism action");
  fi;
  Print("D972V2_MAPPING_STAGE source_gate_pass n=",Length(elements),"\n");
  imageRows := List(maps, map ->
    List(elements, g -> PositionSorted(elements, Image(map,g))));
  Print("D972V2_MAPPING_STAGE images_materialized generators=",
    Length(imageRows),"\n");
  if ForAny(imageRows, row -> ForAny(row, i -> i=fail)) then
    Error("D972 v2: mapping action left its finite source group");
  fi;
  perms := List(imageRows, row -> PermList(row));
  Print("D972V2_MAPPING_STAGE perms_constructed generators=",Length(perms),"\n");
  if ForAny(perms, p -> p=fail) or Length(Set(perms))<>Length(maps) then
    Error("D972 v2: mapping action permutation materialization drift");
  fi;
  if Length(perms) <> 2 then
    Error("D972 v2: K9 mapping action must have exactly two generators");
  fi;
  Print("D972V2_MAPPING_STAGE subgroup_begin degree=",Length(elements),"\n");
  order := Size(Subgroup(SymmetricGroup(Length(elements)),perms));
  Print("D972V2_MAPPING_STAGE subgroup_done order=",order,"\n");
  return order;
end;;

## GAP 4.12 can also reject the six-coset transversal action returned by
## BuildQTGeneral when it is represented as a general bijective mapping.
## Materialize that action on its finite point set, then use the explicit
## parent/generator-list Subgroup form.  This is a representation bridge only:
## the point images, degree, and resulting generated subgroup are unchanged.
D972V2PointActionGroupOrder := function(maps, degree)
  local imageRows, perms, row, i, order, imageOf;
  if Length(maps) <> 2 or degree < 1 then
    Error("D972 v2: point action needs two generators and positive degree");
  fi;
  imageOf := function(map, point)
    if IsPerm(map) then return point^map; fi;
    return Image(map,point);
  end;
  imageRows := List(maps, map -> List([1..degree],
    i -> imageOf(map,i)));
  if ForAny(imageRows, row -> Set(row) <> [1..degree]) then
    Error("D972 v2: point action is not a permutation of its finite set");
  fi;
  perms := List(imageRows, row -> PermList(row));
  if ForAny(perms, p -> p=fail) then
    Error("D972 v2: point action permutation materialization failed");
  fi;
  Print("D972V2_POINT_ACTION materialized degree=",degree," generators=",
    Length(perms),"\n");
  order := Size(Subgroup(SymmetricGroup(degree),perms));
  Print("D972V2_POINT_ACTION subgroup_done order=",order,"\n");
  return order;
end;;

D972V2CompatibilitySelfTest := function()
  local p,q,expected,got;
  p := (1,2,3,4); q := (1,3)(2,4);
  expected := Size(Group(p,q));;
  got := D972V2PointActionGroupOrder([p,q],4);;
  if got <> expected then
    Error("D972 v2: point-action compatibility selftest drift");
  fi;
  Print("D972V2_COMPAT_SELFTEST_PASS point_action_order=",got,
    " qt9_rewrite_count=",D972V2QtCompatReplacementCount,
    " qt4_rewrite_count=",D972V2Qt4CompatReplacementCount,"\n");
end;;

D972V2GetEnv := function(name, fallback)
  local value;
  value := GetEnv(name);
  if value = fail or value = "" then return fallback; fi;
  return value;
end;;

D972V2IsLowerHex64 := function(value)
  return IsString(value) and Length(value)=64 and
    ForAll(value,c->c in "0123456789abcdef");
end;;

D972V2DmtcpEnabled := D972V2GetEnv("D972_DMTCP_ENABLED","0")="1";;
D972V2DmtcpContract :=
  D972V2GetEnv("D972_DMTCP_CONTRACT_SHA256","");;
D972V2DmtcpReady := D972V2DmtcpEnabled and
  D972V2IsLowerHex64(D972V2DmtcpContract);;
D972V2DmtcpVersion := D972V2GetEnv("D972_DMTCP_VERSION","unknown");;
D972V2DmtcpGeneration :=
  D972V2GetEnv("D972_DMTCP_GENERATION","0");;
D972V2DmtcpImageManifest :=
  D972V2GetEnv("D972_DMTCP_IMAGE_MANIFEST_SHA256","");;
D972V2HeartbeatPath := D972V2GetEnv("D972_HEARTBEAT","");;
D972V2UniverseId := D972V2GetEnv("D972_UNIVERSE_ID","unbound");;
D972V2InputDigest := D972V2GetEnv("D972_INPUT_DIGEST","unbound");;
D972V2TaskDigestClaim := D972V2GetEnv("D972_TASK_DIGEST","");;
D972V2TaskPath := D972V2GetEnv("D972_TASK_G","");;
if D972V2TaskPath=fail or D972V2TaskPath="" then
  D972V2TaskPath:=D972V2GetEnv("D972_TASK","");
fi;;
D972V2TaskDigest := "unbound";;
D972V2TaskMeta := fail;;
D972V2LastAutCount := fail;;
if D972V2TaskPath<>fail and D972V2TaskPath<>"" then
  D972V2TaskDigest:=HexSHA256(StringFile(D972V2TaskPath));
  if D972V2TaskDigestClaim<>"" and
     D972V2TaskDigestClaim<>D972V2TaskDigest then
    Error("D972 v2: task digest claim mismatch");
  fi;
  Read(D972V2TaskPath);
  if IsBound(D972_TASK) then D972V2TaskMeta:=D972_TASK; fi;
fi;;

if D972V2TaskMeta<>fail then
  if IsBound(D972V2TaskMeta.universe_id) then
    if D972V2UniverseId<>"unbound" and
       D972V2UniverseId<>D972V2TaskMeta.universe_id then
      Error("D972 v2: universe id environment/task mismatch");
    fi;
    D972V2UniverseId:=D972V2TaskMeta.universe_id;
  fi;
  if IsBound(D972V2TaskMeta.input_digest) then
    if D972V2InputDigest<>"unbound" and
       D972V2InputDigest<>D972V2TaskMeta.input_digest then
      Error("D972 v2: input digest environment/task mismatch");
    fi;
    D972V2InputDigest:=D972V2TaskMeta.input_digest;
  fi;
fi;;

D972V2CursorField := function(T, primary, alternate)
  if T=fail then return fail; fi;
  if IsBound(T.(primary)) then return T.(primary); fi;
  if alternate<>"" and IsBound(T.(alternate)) then return T.(alternate); fi;
  return fail;
end;;

D972V2OuterCursorJson := function(T)
  local a,d,l;
  a:=D972V2CursorField(T,"aut_pair_index","automorphism_pair_index");
  d:=D972V2CursorField(T,"defect_index","relator_defect_index");
  l:=D972V2CursorField(T,"lift_pair_index","marked_lift_index");
  if a=fail or d=fail or l=fail then return "null"; fi;
  return Concatenation("{\"aut_pair_index\":",String(a),
    ",\"defect_index\":",String(d),
    ",\"lift_pair_index\":",String(l),"}");
end;;

D972V2Radices := function(T)
  local k,r,acount;
  if T=fail or not IsBound(T.kernel_table) then return fail; fi;
  k:=Length(T.kernel_table);
  if IsBound(T.q_relators) then r:=Length(T.q_relators);
  elif IsBound(T.base_relators) then r:=Length(T.base_relators);
  else return fail; fi;
  if IsBound(T.aut_count) then acount:=T.aut_count;
  elif IsBound(T.automorphism_count) then acount:=T.automorphism_count;
  elif D972V2LastAutCount<>fail then acount:=D972V2LastAutCount;
  else
    ## This exact fallback is potentially expensive, but it is itself covered
    ## by DMTCP.  Candidate/shadow modes normally populate the cache while
    ## doing their mathematically required Aut(H) enumeration, so no second
    ## enumeration is performed in the normal path.
    acount:=Length(D972TableAutomorphisms(T.kernel_table));
    D972V2LastAutCount:=acount;
  fi;
  return rec(k:=k,relator_count:=r,aut_count:=acount,
    automorphism_pair_count:=acount^2,
    defect_count:=k^r,
    extension_class_count:=acount^2*k^r,
    marked_orbit_count:=k^2);
end;;

D972V2RadicesJson := function(R)
  if R=fail then return "null"; fi;
  return Concatenation("{\"automorphism_count\":",String(R.aut_count),
    ",\"automorphism_pair_count\":",String(R.automorphism_pair_count),
    ",\"defect_count\":",String(R.defect_count),
    ",\"extension_class_count\":",String(R.extension_class_count),
    ",\"marked_orbit_count\":",String(R.marked_orbit_count),"}");
end;;

D972V2NextOuterCursorJson := function(T,R)
  local a,d,l;
  if R=fail then return "null"; fi;
  a:=D972V2CursorField(T,"aut_pair_index","automorphism_pair_index");
  d:=D972V2CursorField(T,"defect_index","relator_defect_index");
  l:=D972V2CursorField(T,"lift_pair_index","marked_lift_index");
  if a=fail or d=fail or l=fail then return "null"; fi;
  l:=l+1;
  if l=R.marked_orbit_count then
    l:=0; d:=d+1;
    if d=R.defect_count then
      d:=0; a:=a+1;
      if a=R.automorphism_pair_count then return "null"; fi;
    fi;
  fi;
  return Concatenation("{\"aut_pair_index\":",String(a),
    ",\"defect_index\":",String(d),
    ",\"lift_pair_index\":",String(l),"}");
end;;

D972V2Heartbeat := function(stage, phase, cursorJson)
  local body;
  if D972V2HeartbeatPath="" then return; fi;
  body:=Concatenation(
    "{\"schema\":\"d972_dovetail_heartbeat/v2\"",
    ",\"authoritative\":false",
    ",\"stage\":",D972JsonString(stage),
    ",\"phase\":",D972JsonString(phase),
    ",\"logical_outer_cursor\":",cursorJson,
    ",\"opaque_inner_cursor_storage\":\"DMTCP process image\"",
    ",\"dmtcp_generation\":",D972JsonString(D972V2DmtcpGeneration),
    ",\"task_digest\":",D972JsonString(D972V2TaskDigest),"}");
  WriteFile(D972V2HeartbeatPath,Concatenation(body,"\n"));
end;;

## Preserve the original algorithms, adding diagnostic safe-boundary markers.
## DMTCP, not these heartbeats, serializes a loop or library call mid-flight.
D972V1CanonicalTable := D972CanonicalTable;;
D972CanonicalTable := function(tbl)
  local answer;
  D972V2Heartbeat("canonical_table_relabel","entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  answer:=D972V1CanonicalTable(tbl);
  D972V2Heartbeat("canonical_table_relabel","completed",
    D972V2OuterCursorJson(D972V2TaskMeta));
  return answer;
end;;

D972V1TableAutomorphisms := D972TableAutomorphisms;;
D972TableAutomorphisms := function(tbl)
  local answer;
  D972V2Heartbeat("automorphism_enumeration","entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  answer:=D972V1TableAutomorphisms(tbl);
  D972V2LastAutCount:=Length(answer);
  D972V2Heartbeat("automorphism_enumeration","completed",
    D972V2OuterCursorJson(D972V2TaskMeta));
  return answer;
end;;

D972V1BuildDefectPresentation := D972BuildDefectPresentation;;
D972BuildDefectPresentation := function(Hrec,qRelators,autLabels,defects)
  local answer;
  D972V2Heartbeat("extension_class","presentation_build_entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  answer:=D972V1BuildDefectPresentation(Hrec,qRelators,autLabels,defects);
  D972V2Heartbeat("extension_class","presentation_build_completed",
    D972V2OuterCursorJson(D972V2TaskMeta));
  return answer;
end;;

## This is the v1 exact gate with explicit phase markers around the opaque GAP
## calls.  A DMTCP image taken in either call contains its actual internal
## enumerator state; the phase marker alone is never resume authority.
D972ExactEmbeddingGate := function(Pdata, expectedH, expectedQ)
  local P,Hsub,pres,Hfp,hsize,psize,normal,cursor;
  cursor:=D972V2OuterCursorJson(D972V2TaskMeta);
  P:=Pdata.fp;
  Hsub:=Subgroup(P,Pdata.h_words{[2..Length(Pdata.h_words)]});
  normal:=IsNormal(P,Hsub);
  D972V2Heartbeat("fp_order","presentation_subgroup_mtc_entered",cursor);
  pres:=PresentationSubgroupMtc(P,Hsub,"h");
  D972V2Heartbeat("fp_order","presentation_subgroup_mtc_completed",cursor);
  Hfp:=FpGroupPresentation(pres);
  D972V2Heartbeat("fp_order","kernel_size_entered",cursor);
  hsize:=Size(Hfp);
  D972V2Heartbeat("fp_order","kernel_size_completed",cursor);
  D972V2Heartbeat("fp_order","extension_size_entered",cursor);
  psize:=Size(P);
  D972V2Heartbeat("fp_order","extension_size_completed",cursor);
  return rec(normal:=normal,h_size:=hsize,p_size:=psize,
    h_embeds:=hsize=expectedH,exact_order:=psize=expectedH*expectedQ);
end;;

D972V1CandidateMode := D972CandidateMode;;
D972CandidateMode := function()
  D972V2Heartbeat("marked_orbit","candidate_cell_entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  D972V1CandidateMode();
end;;

D972V1ShadowFiberMode := D972ShadowFiberMode;;
D972ShadowFiberMode := function()
  D972V2Heartbeat("972_fiber_scan","full_scan_entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  D972V1ShadowFiberMode();
end;;

## Replace v1's honest blocked receipt by an equally honest conditional one.
## A worker result alone does not prove that a DMTCP image exists: the external
## producer/checker must bind and verify the image-manifest receipt.
D972CompletenessReceiptJson := function()
  local live;
  if D972V2DmtcpReady then live:="READY_DMTCP_EXTERNAL_IMAGE_RECEIPT_REQUIRED";
  else live:="BLOCKED_DMTCP_CONTRACT_NOT_ENABLED"; fi;
  return Concatenation(
    "{\"scope\":\"fixed labelled H and fixed marked finite presentation of Qbar\"",
    ",\"b3_stable_encoding\":\"enumerate full P=B3/L over B3/M; E=ker(P to S3) is gated to order k|PB3/M|\"",
    ",\"nonabelian_h_supported\":true",
    ",\"automorphism_pairs_exhaustive\":true",
    ",\"relator_defect_tuples_exhaustive\":true",
    ",\"marked_lift_pairs_exhaustive\":true",
    ",\"outer_buckets_prune_nothing\":true",
    ",\"exactness_gate\":\"H embeds and |P|=|H||Qbar|; factor kernel has size |H|\"",
    ",\"argument\":\"chosen lifts induce two automorphisms of H and one H-valued defect for every base relator; conversely the Cayley, conjugation and defect presentation with the exactness gate is precisely an extension; every marked lift lies in one enumerated H-coset\"",
    ",\"workflow_resumable\":",D972Bool(D972V2DmtcpReady),
    ",\"worker_alone_resume_authority\":false",
    ",\"liveness_status\":",D972JsonString(live),
    ",\"checkpoint_transport\":\"DMTCP full-process image plus independently sealed workflow manifest\"",
    ",\"checkpointed_internal_cursors\":{",
      "\"canonical_table_relabel\":\"GAP loop locals in DMTCP image\",",
      "\"Aut(H)\":\"GAP loop locals in DMTCP image\",",
      "\"extension_class\":\"logical outer coordinate plus GAP presentation state in DMTCP image\",",
      "\"marked_orbit\":\"logical outer coordinate plus GAP locals in DMTCP image\",",
      "\"fp_order\":\"MTC/Size call stack and heap in DMTCP image\",",
      "\"972_fiber_scan\":\"m/f loop locals, accumulators, and group objects in DMTCP image\"}",
    ",\"heartbeat_authoritative\":false",
    ",\"completed_cell_authority\":\"final d972_dovetail_worker/v2 envelope only\"",
    ",\"terminal_A_condition\":\"completed exact isolated shadow-fibre classification with first eligible zero fibre\"",
    ",\"finite_cap_or_nontermination_is_terminal_B\":false",
    ",\"dmtcp_contract_sha256\":",
      D972JsonString(D972V2DmtcpContract),"}"
  );
end;;

## Authority-receipt digest recipe (no terminal LF):
##
##   schema=d972_dovetail_worker/v2
##   |mode=<mode>|status=<status>|universe_id=<universe_id>
##   |input_digest=<input_digest>|task_digest=<task_digest>
##   |payload_sha256=<payload_sha256>
##   |cursor_before=<canonical compact JSON>
##   |cursor_after=<canonical compact JSON>
##   |radices=<canonical compact JSON>
##   |completed_range=<canonical compact JSON>
##   |cell_complete=<lowercase JSON boolean>
##   |classification_complete=<lowercase JSON boolean>
##   |outer_advance_authorized=<lowercase JSON boolean>
##   |exhausted=<lowercase JSON boolean>
##   |h_exhausted=<lowercase JSON boolean>
##   |terminal_A_eligible=<lowercase JSON boolean>
##   |workflow_resumable=<lowercase JSON boolean>
##   |dmtcp_contract_sha256=<digest>
##   |dmtcp_generation=<generation>
##
## Cursor, radices and completed-range objects below are emitted in sorted-key
## order.  An independent implementation may reproduce them with
## json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).
D972V2AuthorityMaterial := function(mode,status,universeId,inputDigest,
    taskDigest,payloadDigest,before,after,radicesJson,completedJson,
    cellComplete,classificationComplete,outerAdvanceAuthorized,exhausted,
    hExhausted,terminalA,workflowResumable,contract,generation)
  return Concatenation(
    "schema=d972_dovetail_worker/v2",
    "|mode=",mode,
    "|status=",status,
    "|universe_id=",universeId,
    "|input_digest=",inputDigest,
    "|task_digest=",taskDigest,
    "|payload_sha256=",payloadDigest,
    "|cursor_before=",before,
    "|cursor_after=",after,
    "|radices=",radicesJson,
    "|completed_range=",completedJson,
    "|cell_complete=",D972Bool(cellComplete),
    "|classification_complete=",D972Bool(classificationComplete),
    "|outer_advance_authorized=",D972Bool(outerAdvanceAuthorized),
    "|exhausted=",D972Bool(exhausted),
    "|h_exhausted=",D972Bool(hExhausted),
    "|terminal_A_eligible=",D972Bool(terminalA),
    "|workflow_resumable=",D972Bool(workflowResumable),
    "|dmtcp_contract_sha256=",contract,
    "|dmtcp_generation=",generation
  );
end;;

## Wrap every frozen v1 result in a restart-idempotent v2 envelope.  The result
## path is overwritten once; workflow code must ingest it only after clean GAP
## exit.  Restarting an image before/after the write therefore cannot append a
## duplicate ledger row.
D972V1Emit := D972Emit;;
D972Emit := function(payload)
  local payloadDigest,R,before,next,accepted,cellComplete,hExhausted,
        classificationComplete,outerAdvanceAuthorized,terminalA,status,
        completed,radicesJson,material,result,imageManifest;
  payloadDigest:=HexSHA256(payload);
  R:=D972V2Radices(D972V2TaskMeta);
  radicesJson:=D972V2RadicesJson(R);
  before:=D972V2OuterCursorJson(D972V2TaskMeta);
  next:=D972V2NextOuterCursorJson(D972V2TaskMeta,R);
  accepted:=PositionSublist(payload,"\"accepted_count\":1")<>fail;
  terminalA:=PositionSublist(payload,
    "\"campaign_stop_first_empty_fiber\":true")<>fail;
  if PositionSublist(payload,"\"status\":\"INCONSISTENT_STOP\"")<>fail then
    status:="INCONSISTENT_STOP";
  else status:="PASS"; fi;
  if D972Mode="candidate" or
     (D972Mode="checkpoint" and D972V2TaskMeta<>fail and
      IsBound(D972V2TaskMeta.operation) and
      D972V2TaskMeta.operation="candidate") then
    ## The relative-extension candidate cell has completed even when it is
    ## accepted.  In that case its shadow classification is the next stage and
    ## the outer cursor is deliberately held until that stage completes.
    cellComplete:=true;
    classificationComplete:=not accepted;
    outerAdvanceAuthorized:=not accepted;
    if accepted then next:=before; fi;
    completed:=Concatenation(
      "{\"relative_extension_complete\":true",
      ",\"shadow_classification_complete\":",
      D972Bool(classificationComplete),
      ",\"stage\":\"marked_orbit\",\"start\":",before,
      ",\"stop\":",next,"}");
  elif D972Mode="shadow-fiber" or
       (D972Mode="checkpoint" and D972V2TaskMeta<>fail and
        IsBound(D972V2TaskMeta.operation) and
        D972V2TaskMeta.operation="shadow-fiber") then
    cellComplete:=true;
    classificationComplete:=true;
    outerAdvanceAuthorized:=true;
    completed:=Concatenation(
      "{\"complete\":true,\"stage\":\"972_fiber_scan\",",
      "\"start\":0,",
      "\"stop_source\":\"payload.charming_pair_universe\"}");
  else
    cellComplete:=true;
    classificationComplete:=true;
    outerAdvanceAuthorized:=true;
    completed:=Concatenation("{\"complete\":true,\"stage\":",
      D972JsonString(D972Mode),"}");
  fi;
  hExhausted:=outerAdvanceAuthorized and next="null" and before<>"null";
  if D972V2IsLowerHex64(D972V2DmtcpImageManifest) then
    imageManifest:=D972JsonString(D972V2DmtcpImageManifest);
  else imageManifest:="null"; fi;
  material:=D972V2AuthorityMaterial(
    D972Mode,status,D972V2UniverseId,D972V2InputDigest,D972V2TaskDigest,
    payloadDigest,before,next,radicesJson,completed,cellComplete,
    classificationComplete,outerAdvanceAuthorized,hExhausted,hExhausted,
    terminalA,D972V2DmtcpReady,D972V2DmtcpContract,
    D972V2DmtcpGeneration);
  result:=Concatenation(
    "{\"schema\":\"d972_dovetail_worker/v2\"",
    ",\"mode\":",D972JsonString(D972Mode),
    ",\"status\":",D972JsonString(status),
    ",\"universe_id\":",D972JsonString(D972V2UniverseId),
    ",\"input_digest\":",D972JsonString(D972V2InputDigest),
    ",\"task_digest\":",D972JsonString(D972V2TaskDigest),
    ",\"payload_sha256\":",D972JsonString(payloadDigest),
    ",\"cursor_before\":",before,
    ",\"cursor_after\":",next,
    ",\"outer_cursor_before\":",before,
    ",\"outer_cursor_after\":",next,
    ",\"radices\":",radicesJson,
    ",\"completed_range\":",completed,
    ",\"cell_complete\":",D972Bool(cellComplete),
    ",\"classification_complete\":",D972Bool(classificationComplete),
    ",\"outer_advance_authorized\":",D972Bool(outerAdvanceAuthorized),
    ",\"exhausted\":",D972Bool(hExhausted),
    ",\"h_exhausted\":",D972Bool(hExhausted),
    ",\"terminal_A_eligible\":",D972Bool(terminalA),
    ",\"terminal_A_requires_independent_checker\":true",
    ",\"gap412_compat_rewrite\":{\"needle\":",D972JsonString(D972V2CompatNeedle),
      ",\"replacement\":",D972JsonString(D972V2CompatReplacement),
      ",\"count\":",String(D972V2CompatReplacementCount),"}",
    ",\"gap412_qt_group_rewrite\":{\"needle\":",D972JsonString(D972V2QtCompatNeedle),
      ",\"replacement\":",D972JsonString(D972V2QtCompatReplacement),
      ",\"count\":",String(D972V2QtCompatReplacementCount),"}",
    ",\"gap412_qt4_group_rewrite\":{\"needle\":",D972JsonString(D972V2Qt4CompatNeedle),
      ",\"replacement\":",D972JsonString(D972V2Qt4CompatReplacement),
      ",\"count\":",String(D972V2Qt4CompatReplacementCount),"}",
     ",\"gap412_mtc_rewrite\":{\"needle\":",D972JsonString(D972V2MtcNeedle),
       ",\"replacement\":",D972JsonString(D972V2MtcReplacement),
       ",\"count\":",String(D972V2MtcReplacementCount),"}",
     ",\"gap412_base_permutation_group_rewrites\":{\"helper\":\"D972V2PermutationGroup\"",
       ",\"replacement_count\":",String(D972V2BaseRewriteTotalCount),
       ",\"frozen_v1_sha256\":",D972JsonString(D972V2ExpectedV1SHA256),"}",
     ",\"workflow_resumable\":",D972Bool(D972V2DmtcpReady),
    ",\"opaque_internal_state_checkpointed_by\":\"DMTCP process image; authority is external image manifest\"",
    ",\"dmtcp\":{\"enabled\":",D972Bool(D972V2DmtcpEnabled),
      ",\"contract_ready\":",D972Bool(D972V2DmtcpReady),
      ",\"version\":",D972JsonString(D972V2DmtcpVersion),
      ",\"generation\":",D972JsonString(D972V2DmtcpGeneration),
      ",\"contract_sha256\":",D972JsonString(D972V2DmtcpContract),
      ",\"image_manifest_sha256\":",imageManifest,"}",
    ",\"checkpoint\":{\"logical_outer_cursor\":",before,
      ",\"internal_cursor_storage\":\"DMTCP process image\",",
      "\"heartbeat_authoritative\":false}",
    ",\"checkpoint_sha256\":",D972JsonString(HexSHA256(material)),
    ",\"relative_extension_completeness_receipt\":",
      D972CompletenessReceiptJson(),
    ",\"payload\":",payload,"}"
  );
  D972V2Heartbeat("result","cell_result_committed",next);
  if D972Output="" then Print(result,"\n");
  else WriteFile(D972Output,Concatenation(result,"\n")); fi;
end;;

D972V2Dispatch := function()
  local operation;
  D972V2Heartbeat("dispatch","entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  if D972Mode="checkpoint" then
    if D972V2TaskMeta=fail or not IsBound(D972V2TaskMeta.operation) then
      Error("checkpoint mode needs D972_TASK.operation");
    fi;
    operation:=D972V2TaskMeta.operation;
    if operation="candidate" then D972CandidateMode();
    elif operation="shadow-fiber" then D972ShadowFiberMode();
    elif operation="compare" then D972CompareMode();
    else Error("checkpoint operation not implemented: ",operation); fi;
  elif D972Mode="selftest" then D972SelfTest();
  elif D972Mode="base-audit" then D972BaseMode(true);
  elif D972Mode="preflight" then D972BaseMode(false);
  elif D972Mode="base-presentation" then D972BaseMode(true);
  elif D972Mode="kernel-catalog" then D972KernelCatalogMode();
  elif D972Mode="candidate" or D972Mode="slice" then D972CandidateMode();
  elif D972Mode="shadow-fiber" then D972ShadowFiberMode();
  elif D972Mode="compare" then D972CompareMode();
  else Error("mode not implemented yet: ",D972Mode); fi;
end;;

D972V2V1SelfTest := D972SelfTest;;
D972SelfTest := function()
  D972V2CompatibilitySelfTest();;
  D972V2V1SelfTest();;
end;;

D972V2Dispatch();
QUIT;
