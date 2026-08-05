#############################################################################
## search/probe/w6_bu_s1_s3/w6_bu_s1_s3_driver.g
## W6BU firing (裁定585/585補): v3 table S1(宇宙)-S2(位数)-S3(拡大類 H^2 全類)
## for the exact 17-row (V-cen) firing universe (manifest
## W6-BU-FREEZE2-EXACT17-F106), D+D row (p2_d4_a0b0c2) first.
##
## SCOPE (裁定585補で確定): S1/S2/S3 ONLY -- v3 table numbering, NOT the
## commander's original (erroneous) "S1=roof enum/S3.5=ISO-GATE" gloss.
## S3.5 (marked lift L1-L3) is explicitly NOT attempted here: it requires an
## explicit sigma1,sigma2 -> Ghat5 (order 3000, A-component included)
## embedding formula that is not yet available (mathematician order pending,
## bu_s35_embedding_v1.md). Guessing that embedding is forbidden (D-1/N-4
## danger flags; 裁定585補 explicit prohibition). No B3/Ghat5/P-hat group is
## constructed anywhere in this script -- only the F_p[S4]-module V itself
## (same construction as w6_bu_census_driver.g) and its H^2(S4,V) data.
##
## S1 (宇宙): re-derive V from module_id (independent of the census cert's
##   own in-memory state -- this is a fresh GAP process) and re-check it is
##   S4-well-defined (a^2=b^3=(ab)^4=I) and S3-inflate (true by construction:
##   built purely from triv/reg2/D blocks for p=2, or brute-force S3->GL(2,3)
##   homs for p=3 -- both factor through S4->S3).
## S2 (位数): window_order = 500*p^dim <= 8000 check (manifest gate).
## S3 (拡大類): dim H^2(S4,V) cross-checked against the census cert's own
##   recorded value (independent re-derivation via CHR/SecondCohomologyDimension
##   in this fresh process), then the FULL set of classes [eps] in H^2(S4,V)
##   is enumerated as F_p-coordinate vectors (F_p^dim, size p^dim) -- an
##   abstract enumeration of cohomology classes, NOT a construction of the
##   actual extension groups (that belongs to S3.5+, out of scope here).
##
## Non-contact: Im R untouched, d_N unevaluated, 3 sealed quantities
## untouched, no reading of prior certs' measurement values as ground truth
## without independent re-derivation (cross-check only). No
## kill/EMPTY/candidate/isolated=TRUE-FALSE word used anywhere.
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
LoadPackage("cohomolo");;

FAILS := [];;
Chk := function(name, got, want)
  local ok;
  ok := (got = want);
  if not ok then Add(FAILS, rec(name := name, got := String(got), want := String(want))); fi;
  Print("  [", PF(ok), "] ", name, ": got=", got, " want=", want, "\n");
  return ok;
end;;

#############################################################################
## Shared S4/S3 setup (verbatim from w6_bu_census_driver.g -- same convention)
#############################################################################
S4grp := Group((1,2),(1,3,4));;
theta := (1,2);; tau := (1,3,4);;
FS4 := FreeGroup(2);;
FqS4 := FS4 / [FS4.1^2, FS4.2^3, (FS4.1*FS4.2)^4];;

V4norm := Filtered(NormalSubgroups(S4grp), n -> Size(n) = 4)[1];;
quoS3 := NaturalHomomorphismByNormalSubgroup(S4grp, V4norm);;
S3q := Image(quoS3);;
gl22 := GL(2,2);;
isoS3toGL22 := IsomorphismGroups(S3q, gl22);;

triv_a := [[Z(2)^0]];; triv_b := [[Z(2)^0]];;
reg2_a := [[Z(2)^0,Z(2)^0],[0*Z(2),Z(2)^0]];;
reg2_b := IdentityMat(2,GF(2));;
D_a := Image(isoS3toGL22, Image(quoS3, theta));;
D_b := Image(isoS3toGL22, Image(quoS3, tau));;

BlockDiag := function(mats)
  local dim, res, offs, i, j, m;
  dim := Sum(mats, m -> Length(m));
  res := List([1..dim], i -> List([1..dim], j -> Zero(GF(2))));
  offs := 0;
  for m in mats do
    for i in [1..Length(m)] do
      for j in [1..Length(m)] do
        res[offs+i][offs+j] := m[i][j];
      od;
    od;
    offs := offs + Length(m);
  od;
  return res;
end;;

BuildVCenModuleP2 := function(a,b,c)
  local matsA, matsB, i, ma, mb;
  matsA := [];; matsB := [];;
  for i in [1..a] do Add(matsA, triv_a); Add(matsB, triv_b); od;
  for i in [1..b] do Add(matsA, reg2_a); Add(matsB, reg2_b); od;
  for i in [1..c] do Add(matsA, D_a); Add(matsB, D_b); od;
  ma := BlockDiag(matsA);; mb := BlockDiag(matsB);;
  return rec(ma := ma, mb := mb);
end;;

## p=3, dim=2: reproduce the IDENTICAL brute-force enumeration as
## w6_bu_census_driver.g (same GL(2,3) element order, same relation checks,
## same naive orbit-merge dedup) so that "p3_d2_bruteforce_N" indexes match.
gl23 := GL(2,3);;
eltsGL23 := Elements(gl23);;
homsP3 := [];;
for aElt in eltsGL23 do
  if aElt^2 = aElt^0 then
    for bElt in eltsGL23 do
      if bElt^3 = bElt^0 then
        if (aElt*bElt)^2 = (aElt*bElt)^0 then
          Add(homsP3, [aElt,bElt]);
        fi;
      fi;
    od;
  fi;
od;
repsP3 := [];;
for pr in homsP3 do
  found := false;;
  for g in eltsGL23 do
    for rp in repsP3 do
      if pr[1]^g = rp[1] and pr[2]^g = rp[2] then found := true; break; fi;
    od;
    if found then break; fi;
  od;
  if not found then Add(repsP3, pr); fi;
od;
Chk("p3 bruteforce reproduction: num conjugacy-class reps", Length(repsP3), 5);;

#############################################################################
## Load manifest / census cert (read-only cross-check source; census values
## are RE-DERIVED below, not trusted blindly -- match is asserted via Chk).
#############################################################################
ManifestPath := "search/certs/w6_bu_firing_gate_manifest_v1.json";;
CensusPath := "search/certs/h2_census_s4_20260805.json";;
SchemaPath := "search/certs/w6_bu_firing_cert_schema_v1.json";;

ReadWholeFile := function(path)
  local f, s;
  f := InputTextFile(path);
  if f = fail then Error("cannot open ", path); fi;
  s := ReadAll(f);
  CloseStream(f);
  return s;
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_w6bu_s1s3_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then
    Error("ComputeSha256File: sha256sum did not return a hash line for ", relpath);
  fi;
  return line{[1 .. 64]};
end;;

## Minimal hand-rolled JSON field extractor for the census cert's "rows"
## array (avoids depending on a general JSON parser inside GAP). We only
## need module_id -> dim_H2_S4 and window_order, both plain integers, and
## p/dim/s3_inflated -- all appear as simple "key":value tokens per row.
ExtractRowsBlock := function(content)
  local mk, pos, depth, i, c, startIdx;
  mk := "\"rows\":[";
  pos := PositionSublist(content, mk);
  if pos = fail then Error("ExtractRowsBlock: \"rows\":[ not found"); fi;
  startIdx := pos + Length(mk) - 1; ## points at first char after '['
  depth := 1; i := startIdx;
  while depth > 0 do
    i := i + 1;
    c := content[i];
    if c = '[' then depth := depth + 1; fi;
    if c = ']' then depth := depth - 1; fi;
  od;
  return content{[startIdx .. i-1]};
end;;

SplitTopLevelObjects := function(s)
  ## s is a comma-joined sequence of {...} objects (no nested arrays deeper
  ## than braces themselves contain, which holds for our row schema).
  local objs, depth, i, startIdx, c;
  objs := []; depth := 0; startIdx := fail;
  for i in [1..Length(s)] do
    c := s[i];
    if c = '{' then
      if depth = 0 then startIdx := i; fi;
      depth := depth + 1;
    elif c = '}' then
      depth := depth - 1;
      if depth = 0 then Add(objs, s{[startIdx..i]}); fi;
    fi;
  od;
  return objs;
end;;

ExtractIntField := function(obj, key)
  local mk, pos, j, digitStr;
  mk := Concatenation("\"", key, "\":");
  pos := PositionSublist(obj, mk);
  if pos = fail then Error("ExtractIntField: key not found: ", key); fi;
  j := pos + Length(mk);
  digitStr := "";
  while j <= Length(obj) and obj[j] in "0123456789" do
    Append(digitStr, [obj[j]]); j := j + 1;
  od;
  if Length(digitStr) = 0 then Error("ExtractIntField: empty int for key ", key); fi;
  return Int(digitStr);
end;;

ExtractStrField := function(obj, key)
  local mk, pos, j, k, out;
  mk := Concatenation("\"", key, "\":\"");
  pos := PositionSublist(obj, mk);
  if pos = fail then Error("ExtractStrField: key not found: ", key); fi;
  j := pos + Length(mk);
  k := j;
  while obj[k] <> '"' do k := k + 1; od;
  return obj{[j..k-1]};
end;;

censusContent := ReadWholeFile(CensusPath);;
censusRowsStr := ExtractRowsBlock(censusContent);;
censusRowObjs := SplitTopLevelObjects(censusRowsStr);;
CensusById := rec();;
for obj in censusRowObjs do
  CensusById.(ExtractStrField(obj,"module_id")) := rec(
    p := ExtractIntField(obj,"p"),
    dim := ExtractIntField(obj,"dim"),
    dim_H2_S4 := ExtractIntField(obj,"dim_H2_S4"),
    window_order := ExtractIntField(obj,"window_order")
  );;
od;;
Chk("census: rows extracted", Length(RecNames(CensusById)), 17);;

#############################################################################
## Exact 17-row order (manifest row_ids, verbatim)
#############################################################################
RowIds := [
  "p2_d2_a0b0c1", "p2_d2_a0b1c0", "p2_d2_a2b0c0",
  "p2_d3_a1b0c1", "p2_d3_a1b1c0", "p2_d3_a3b0c0",
  "p2_d4_a0b0c2", "p2_d4_a0b1c1", "p2_d4_a0b2c0",
  "p2_d4_a2b0c1", "p2_d4_a2b1c0", "p2_d4_a4b0c0",
  "p3_d2_bruteforce_1", "p3_d2_bruteforce_2", "p3_d2_bruteforce_3",
  "p3_d2_bruteforce_4", "p3_d2_bruteforce_5"
];;

## D+D (p2_d4_a0b0c2) first, per commander order; remaining 16 follow in
## manifest row order (S-BU order requirement: source order preserved in the
## emitted cert regardless of computation order).
ProcessOrder := Concatenation(["p2_d4_a0b0c2"],
    Filtered(RowIds, r -> r <> "p2_d4_a0b0c2"));;

ParseP2Triple := function(modId)
  ## "p2_d{dim}_a{a}b{b}c{c}" -> [a,b,c]
  local parts, aPos, bPos, cPos, aStr, bStr, cStr, j;
  aPos := PositionSublist(modId, "_a") + 2;
  bPos := PositionSublist(modId, "b");
  cPos := PositionSublist(modId, "c");
  aStr := modId{[aPos .. bPos-1]};
  bStr := modId{[bPos+1 .. cPos-1]};
  cStr := modId{[cPos+1 .. Length(modId)]};
  return [Int(aStr), Int(bStr), Int(cStr)];
end;;

ParseP3Index := function(modId)
  local parts;
  parts := SplitString(modId, "_");
  return Int(parts[Length(parts)]);
end;;

RowResults := rec();;
TraversalWitnesses := [];;
TotalTraversed := 0;;

for modId in ProcessOrder do
  Print("\n=== S1-S3: ", modId, " ===\n");
  cinfo := CensusById.(modId);;
  if cinfo.p = 2 then
    trip := ParseP2Triple(modId);;
    a := trip[1];; b := trip[2];; c := trip[3];;
    Chk(Concatenation(modId, ": a+2b+2c = dim"), a+2*b+2*c, cinfo.dim);;
    built := BuildVCenModuleP2(a,b,c);;
    ma := built.ma;; mb := built.mb;;
    dim := cinfo.dim;;
    ## S1: re-check well-defined S4 relations (fresh re-derivation)
    Chk(Concatenation(modId, ": S1 a^2=I"), ma^2 = IdentityMat(dim,GF(2)), true);;
    Chk(Concatenation(modId, ": S1 b^3=I"), mb^3 = IdentityMat(dim,GF(2)), true);;
    Chk(Concatenation(modId, ": S1 (ab)^4=I"), (ma*mb)^4 = IdentityMat(dim,GF(2)), true);;
    ## S1: S3-inflate is true by construction (triv/reg2/D blocks all factor
    ## through S4 -> S3); recorded, not independently re-derived here.
    s3infl := true;;
    ## S2: window order
    windowOrder := 500 * 2^dim;;
    Chk(Concatenation(modId, ": S2 window_order matches census"), windowOrder, cinfo.window_order);;
    Chk(Concatenation(modId, ": S2 window_order <= 8000"), windowOrder <= 8000, true);;
    ## S3: dim H^2(S4,V), independently re-derived via CHR
    chr := CHR(S4grp, 2, FqS4, [ma, mb]);;
    h2 := SecondCohomologyDimension(chr);;
    Chk(Concatenation(modId, ": S3 dim H2(S4,V) cross-check vs census"), h2, cinfo.dim_H2_S4);;
    pPrime := 2;;
  else
    idx := ParseP3Index(modId);;
    rp := repsP3[idx];;
    dim := cinfo.dim;;
    ma3 := rp[1];; mb3 := rp[2];;
    Chk(Concatenation(modId, ": S1 a^2=I (p3)"), ma3^2 = ma3^0, true);;
    Chk(Concatenation(modId, ": S1 b^3=I (p3)"), mb3^3 = mb3^0, true);;
    Chk(Concatenation(modId, ": S1 (ab)^2=I (p3, prodOrdS3=2)"), (ma3*mb3)^2 = (ma3*mb3)^0, true);;
    s3infl := true;;
    windowOrder := 500 * 3^dim;;
    Chk(Concatenation(modId, ": S2 window_order matches census"), windowOrder, cinfo.window_order);;
    Chk(Concatenation(modId, ": S2 window_order <= 8000"), windowOrder <= 8000, true);;
    chr3 := CHR(S4grp, 3, FqS4, [ma3, mb3]);;
    h2 := SecondCohomologyDimension(chr3);;
    Chk(Concatenation(modId, ": S3 dim H2(S4,V) cross-check vs census"), h2, cinfo.dim_H2_S4);;
    pPrime := 3;;
  fi;

  ## S3: enumerate ALL classes [eps] in H^2(S4,V) as F_p-coordinate vectors
  ## (abstract enumeration only -- no extension group is constructed).
  numClasses := pPrime ^ h2;;
  classVectors := [];;
  if h2 = 0 then
    Add(classVectors, []);
  else
    classVectors := Cartesian(List([1..h2], ii -> [0..pPrime-1]));;
  fi;
  Chk(Concatenation(modId, ": S3 |H2(S4,V)| = p^dimH2 enumeration size"), Length(classVectors), numClasses);;

  RowResults.(modId) := rec(
    p := pPrime, dim := dim, s3_inflated := s3infl, window_order := windowOrder,
    dim_H2_S4 := h2, num_classes := numClasses
  );;

  for ci in [1..Length(classVectors)] do
    Add(TraversalWitnesses, rec(
      traversal_id := Concatenation(modId, "_class_", String(ci-1)),
      disposition := "ACCEPTED",
      source_tag := "S3_H2_ENUM"
    ));;
    TotalTraversed := TotalTraversed + 1;;
  od;
od;;

Chk("grand total: traversed classes across 17 rows", TotalTraversed, 449);;

#############################################################################
## ==== JSON output (per w6-bu-firing-cert/v1 schema) ====
#############################################################################
Print("\n=== writing cert ===\n");

manifestSha := ComputeSha256File(ManifestPath);;
schemaSha := ComputeSha256File(SchemaPath);;
censusSha := ComputeSha256File(CensusPath);;
selfSha := ComputeSha256File("search/probe/w6_bu_s1_s3/w6_bu_s1_s3_driver.g");;

## NOTE: manifestSha is the CURRENT manifest file's own hash (used verbatim
## in the emitted cert's "manifest" field, per schema). It is NOT expected to
## equal the frozen "pre_authorization_manifest_sha256" field recorded
## inside the manifest itself (that field is a snapshot of an EARLIER,
## pre-amendment manifest state -- a different, historical artifact -- so no
## equality check against it belongs here).
Chk("census sha256 matches frozen source_map binding", censusSha,
    "4b8673209d55c46fe1bc01a1e2736df03f296cd7d775df6da98f8f582df73b30");;

## row_projection-style canonical row list, source order (manifest order)
RowsJson := JArr(List(RowIds, function(modId)
  local r;
  r := RowResults.(modId);
  return Concatenation(
    "{\"module_id\":", JStr(modId),
    ",\"p\":", String(r.p), ",\"dim\":", String(r.dim),
    ",\"s3_inflated\":", JB(r.s3_inflated),
    ",\"window_order\":", String(r.window_order),
    ",\"stage_status\":\"INVENTORY_ONLY\"",
    ",\"stop_or_unknown\":", JStr(Concatenation(
        "S1-S3 complete (universe/order/H2-class-count cross-checked vs census); ",
        "S3.5 marked-lift NOT attempted (sigma1,sigma2 -> Ghat5 embedding pending, ",
        "bu_s35_embedding_v1.md; guessing forbidden per 裁定585補/D-1/N-4)")),
    "}");
end));;

DenomRowIdsJson := JArr(List(RowIds, JStr));;

SourceMapEntriesJson := JArr(List([0..Length(RowIds)-1], function(i)
  return Concatenation("{\"module_id\":", JStr(RowIds[i+1]),
      ",\"source_pointer\":", JStr(Concatenation("/rows/", String(i))),
      ",\"stage_tag\":\"FIRING_UNIVERSE_SELECTION\"}");
end));;

## projection_sha256: recompute the exact same canonicalization the checker
## uses (row_projection keys module_id,p,dim,s3_inflated,window_order; UTF-8,
## ensure_ascii=false, sort_keys=true, separators=(',',':')) -- delegate to
## a tiny inline python-equivalent by shelling out, to guarantee byte-for-byte
## match with the Python checker's canonical_sha256(row_projection(rows)).
ProjectionPySrc := Concatenation(
  "import json,hashlib\n",
  "rows=json.load(open('search/certs/h2_census_s4_20260805.json',encoding='utf-8'))['rows']\n",
  "keys=('module_id','p','dim','s3_inflated','window_order')\n",
  "proj=[{k:r[k] for k in keys} for r in rows]\n",
  "blob=json.dumps(proj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')\n",
  "print(hashlib.sha256(blob).hexdigest())\n");;
WriteFile("search/.tmp_w6bu_s1s3_projection.py", ProjectionPySrc);;
Exec("python search/.tmp_w6bu_s1s3_projection.py > search/.tmp_w6bu_s1s3_projection.out");;
projFile := InputTextFile("search/.tmp_w6bu_s1s3_projection.out");;
projLine := ReadLine(projFile);; CloseStream(projFile);;
ProjectionSha := projLine{[1..64]};;
Exec("rm -f search/.tmp_w6bu_s1s3_projection.py search/.tmp_w6bu_s1s3_projection.out");;

WitnessesJson := JArr(List(TraversalWitnesses, function(w)
  return Concatenation("{\"traversal_id\":", JStr(w.traversal_id),
      ",\"disposition\":\"", w.disposition, "\"",
      ",\"source_tag\":", JStr(w.source_tag), "}");
end));;

cert := Concatenation(
  "{\n",
  "\"schema\":\"w6-bu-firing-cert/v1\",\n",
  "\"schema_sha256\":", JStr(schemaSha), ",\n",
  "\"manifest\":{\"path\":\"search/certs/w6_bu_firing_gate_manifest_v1.json\",\"sha256\":", JStr(manifestSha), "},\n",
  "\"run_class\":\"S3\",\n",
  "\"execution_authorized\":true,\n",
  "\"universe\":{\"layer\":\"V-cen/S3-inflated\",\"dimension_by_prime\":{\"2\":[2,3,4],\"3\":[2]},\"window_order_lte\":8000,\"predicate_order\":[\"layer\",\"prime\",\"dimension_by_prime\",\"window_order_lte\"]},\n",
  "\"denominator\":{\"unit\":\"V-cen module isomorphism type keyed by module_id\",\"expected_count\":17,\"selected_row_count\":17,\"row_ids\":", DenomRowIdsJson, "},\n",
  "\"source_map\":{\"source_path\":\"search/certs/h2_census_s4_20260805.json\",\"source_sha256\":", JStr(censusSha),
  ",\"json_pointer\":\"/rows\",\"projection_sha256\":", JStr(ProjectionSha), ",\"entries\":", SourceMapEntriesJson, "},\n",
  "\"counts\":{\"traversed_count\":", String(TotalTraversed), ",\"accepted_count\":", String(TotalTraversed),
  ",\"rejected_count\":0",
  ",\"traversed_unit\":\"enumerated parameter/lift before acceptance filters; never H1-conjugacy classes\"",
  ",\"accepted_unit\":\"objects after all stage-local acceptance filters\"",
  ",\"relation\":\"traversed_count = accepted_count + rejected_count; fields are not aliases\"",
  ",\"witnesses\":", WitnessesJson, "},\n",
  "\"rows\":", RowsJson, ",\n",
  "\"iso_gate_contract_snapshot\":{\"m_iso8_real_verdict\":\"UNKNOWN(NONSHADOW_IN_DATUM)\",\"m_iso8_mutant_verdict\":\"UNKNOWN(NONSHADOW_IN_DATUM)\",\"m_iso8_detection_layer\":\"detail-element comparison only; verdict is insensitive\",\"real_witness_settled\":false,\"mutant_witness_settled\":true,\"isolated_false_witness_claim\":false},\n",
  "\"claims\":{\"isolated_verdict\":\"UNKNOWN\",\"kill_claim\":false,\"candidate_found\":false,\"empty_claim\":false,\"scope_of_any_coverage\":\"exact firing universe only; no statement about W \\\\ W_adm or supplemental inventory\"},\n",
  "\"status\":{\"coverage_status\":\"PARTIAL_INVENTORY\",\"stop_code\":null,\"unknown_reason\":\"S3.5 marked-lift pending sigma1,sigma2->Ghat5 embedding formula (mathematician order bu_s35_embedding_v1.md, 裁定585補); S3.6-S9 remain LOCKED per manifest always_forbidden_here\"},\n",
  "\"non_contact_declaration\":{\"exploration\":false,\"candidate_generation\":false,\"kill\":false,\"empty_theorem\":false,\"im_R\":false,\"d_N\":false,\"sealed_quantities\":false,\"S9\":false}\n",
  "}\n");;

OUT_PATH := "search/certs/w6_bu_s1_s3_firing_20260806.json";;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nFAILS = ", Length(FAILS), "\n");
for fitem in FAILS do
  Print("   ", fitem.name, " got=", fitem.got, " want=", fitem.want, "\n");
od;
Print("\nSELF_SHA=", selfSha, "\n");
Print("\nW6_BU_S1_S3_DRIVER_DONE\n");
QUIT;
