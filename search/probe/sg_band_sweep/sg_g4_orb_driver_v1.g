#############################################################################
## search/probe/sg_band_sweep/sg_g4_orb_driver_v1.g
## G4 (ORB) execution over the 36 g3_records windows found by the G0-G3 SG
## band sweep. Authority: 裁定649 (司令塔), executing prereg
## docs/notes/sg_band_sweep_prereg_iffirst_v1.md SS7.2 (connection spec) +
## the established ORB methodology of
## docs/notes/theorem_check_mirrorall_l3vacuous_v1.md SSF.8/F.10 (verbatim
## reuse of the proven machinery, NOT a new design):
##   1. Input is search/certs/sg_band_sweep_20260806.json's g3_records[]
##      ONLY -- (order,id) pairs. G4 reconstructs SmallGroup(order,id)
##      independently (does not reuse any GAP object from the G0-G3 run,
##      which was a separate process anyway).
##   2. Entry gate: independently REDISCOVER some (r,s) with ord(r)=2,
##      ord(s)=3, <r,s>=Ghat, and confirm exists phi:Ghat->>S3 -- this is a
##      STRONGER form of "re-verify" than parsing the stored witness string
##      back into an element (which is fragile across GAP sessions); if no
##      such pair exists at all, HANDOFF_MISMATCH/STOP for that record
##      (should never happen since G3 already passed it).
##   3. M := FULL enumeration {(r,s): ord(r)=2, ord(s)=3, <r,s>=Ghat} -- r
##      ranges over ALL order-2 elements here, NOT just conjugacy class
##      reps (prereg SS7.2 item 3: "枝刈りを引き継がない" -- G2's pruning
##      would break the orbit accounting).
##   4. A := AutomorphismGroup(Ghat); partition M into A-orbits; per orbit,
##      reflexible test exists alpha in A: alpha(r)=r^-1(=r) and
##      alpha(s)=s^-1(=s^2) (theorem_check SSF.8 step 4, verbatim).
##   5. nu(r,s) := (r,s^2) [[since r^-1=r, s^-1=s^2]] is a PROVEN involution
##      on M commuting with the A-action (theorem_check SSF.10.2, a THEOREM
##      not re-derived here, only used and spot-checked): it therefore acts
##      as an involution on the set of ORBITS. reflexible(O) <=> nu(O)=O.
##      For each orbit, we record which orbit index nu(representative)
##      lands in -- this is the "cheap free canary" theorem_check SSF.10.2
##      itself recommends, and it is ALSO exactly what the independent
##      python lane (crosscheck/check_sg_g4_g5.py) verifies structurally.
##
## Window/twin classification (G5, same driver -- see PART 2), per the
## established vocabulary of theorem_check_mirrorall_l3vacuous_v1.md SSG.6:
##   - K=1 orbit, reflexible: "isolated_self_mirror" (no twin at all)
##   - a nu-pair of 2 chiral orbits: "mirror_pair" (NOT exotic -- explained
##     by iota, matches the 432/486 precedent exactly)
##   - 2 orbits BOTH reflexible (individually nu-fixed, i.e. NOT each
##     other's nu-image): "両固定 (both-fixed)" twin pair -- EXOTIC (type
##     E1), per Lemma BOTH-FIXED-EXOTIC (theorem_check SSG.6.a, proven, not
##     re-derived here)
##   - more generally, for K orbits sharing one Ghat: exotic pair count =
##     C(K,2) - t where t = number of nu-chiral-pairs (theorem_check
##     SSG.6.a fiber formula, used verbatim)
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;

INPUT_CERT_PATH := "search/certs/sg_band_sweep_20260806.json";;
S3grp := SymmetricGroup(3);;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_g4_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then Error("sha256 fail for ", relpath); fi;
  return line{[1 .. 64]};
end;;

#############################################################################
## PART 0 -- minimal JSON extraction of g3_records[] (order,id pairs only;
## the string witnesses are NOT reused -- entry gate rediscovers fresh).
#############################################################################
ReadWholeFile := function(path)
  local f, s;
  f := InputTextFile(path);
  if f = fail then Error("cannot open ", path); fi;
  s := ReadAll(f); CloseStream(f);
  return s;
end;;

ExtractArrayBlock := function(content, key)
  local mk, pos, depth, i, c, startIdx;
  mk := Concatenation("\"", key, "\":[");
  pos := PositionSublist(content, mk);
  if pos = fail then Error("array marker not found: ", key); fi;
  startIdx := pos + Length(mk) - 1;
  depth := 1; i := startIdx;
  while depth > 0 do
    i := i + 1; c := content[i];
    if c = '[' then depth := depth + 1; fi;
    if c = ']' then depth := depth - 1; fi;
  od;
  return content{[startIdx .. i-1]};
end;;

SplitTopLevelObjects := function(s)
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
  local mk, pos, j, digitStr, neg;
  mk := Concatenation("\"", key, "\":");
  pos := PositionSublist(obj, mk);
  if pos = fail then Error("key not found: ", key); fi;
  j := pos + Length(mk); digitStr := ""; neg := false;
  if obj[j] = '-' then neg := true; j := j + 1; fi;
  while j <= Length(obj) and obj[j] in "0123456789" do Append(digitStr,[obj[j]]); j:=j+1; od;
  if neg then return -Int(digitStr); fi;
  return Int(digitStr);
end;;

certContent := ReadWholeFile(INPUT_CERT_PATH);;
g3Block := ExtractArrayBlock(certContent, "g3_records");;
g3Objs := SplitTopLevelObjects(g3Block);;
ALL_WINDOWS := List(g3Objs, obj -> rec(order := ExtractIntField(obj,"order"), id := ExtractIntField(obj,"id")));;
Print("Loaded ", Length(ALL_WINDOWS), " g3_records windows from ", INPUT_CERT_PATH, "\n");

## Shard support (same convention as w6_bu_s35_driver_v2.g / gaplib_common.g
## 600s wall-clock discipline): set G4_WINDOW_RANGE=[startIdx,endIdx] (1-based,
## inclusive, into ALL_WINDOWS in file order) and G4_OUT_SUFFIX before
## Read()-ing this file to process only a slice.
if not IsBound(G4_WINDOW_RANGE) then G4_WINDOW_RANGE := [1, Length(ALL_WINDOWS)]; fi;
if not IsBound(G4_OUT_SUFFIX) then G4_OUT_SUFFIX := ""; fi;
WINDOWS := ALL_WINDOWS{[G4_WINDOW_RANGE[1] .. G4_WINDOW_RANGE[2]]};;
Print("Processing shard range ", G4_WINDOW_RANGE, " -> ", Length(WINDOWS), " windows\n");

#############################################################################
## PART 1 -- per-window ORB (G4)
#############################################################################
G1_Test := function(Ghat)
  local ab;
  ab := AbelianInvariants(Ghat);;
  return ab in [[2],[2,3],[6]];
end;;

FindOneG2G3Pair := function(Ghat)
  ## Entry gate rediscovery (NOT reusing the G2 pruning): scan ALL
  ## involutions x ALL order-3 elements for a single valid (r,s), plus a
  ## surjection to S3. Returns rec(ok:=bool, r,s,phi).
  local invs, ord3, r, s, sz, quots;
  invs := Filtered(Elements(Ghat), x -> Order(x) = 2);;
  ord3 := Filtered(Elements(Ghat), x -> Order(x) = 3);;
  sz := Size(Ghat);;
  for r in invs do
    for s in ord3 do
      if Size(Subgroup(Ghat,[r,s])) = sz then
        quots := GQuotients(Ghat, S3grp);;
        if Length(quots) > 0 then
          return rec(ok := true, r := r, s := s);
        else
          return rec(ok := false, r := fail, s := fail);
        fi;
      fi;
    od;
  od;
  return rec(ok := false, r := fail, s := fail);
end;;

G4_RESULTS := [];;
HANDOFF_MISMATCHES := [];;

for w in WINDOWS do
  Print("\n=== G4 window (", w.order, ",", w.id, ") ===\n");
  Ghat := SmallGroup(w.order, w.id);;

  ## entry gate
  if not G1_Test(Ghat) then
    Print("  HANDOFF_MISMATCH: G1 fails on independent reconstruction\n");
    Add(HANDOFF_MISMATCHES, w);;
    continue;
  fi;
  entry := FindOneG2G3Pair(Ghat);;
  if not entry.ok then
    Print("  HANDOFF_MISMATCH: no (r,s) with G2+G3 found on independent reconstruction\n");
    Add(HANDOFF_MISMATCHES, w);;
    continue;
  fi;
  Print("  entry gate OK\n");

  ## M: FULL enumeration (no conjugacy-class pruning)
  invs := Filtered(Elements(Ghat), x -> Order(x) = 2);;
  ord3 := Filtered(Elements(Ghat), x -> Order(x) = 3);;
  sz := Size(Ghat);;
  M := [];;
  for r in invs do
    for s in ord3 do
      if Size(Subgroup(Ghat,[r,s])) = sz then
        Add(M, [r,s]);
      fi;
    od;
  od;
  Print("  |M| = ", Length(M), "\n");

  A := AutomorphismGroup(Ghat);;
  autOrder := Size(A);;
  Print("  |Aut(Ghat)| = ", autOrder, "\n");

  ## partition M into A-orbits (manual: OnPairs action via images under
  ## automorphisms represented as GroupHomomorphism objects -- use
  ## Image(alpha,x) per generator-driven orbit closure)
  autGens := GeneratorsOfGroup(A);;
  ApplyAutPair := function(alpha, pr) return [Image(alpha,pr[1]), Image(alpha,pr[2])]; end;;

  remaining := ShallowCopy(M);;
  orbits := [];;
  while Length(remaining) > 0 do
    seed := remaining[1];;
    orb := [seed];;
    frontier := [seed];;
    while Length(frontier) > 0 do
      cur := Remove(frontier);;
      for g in autGens do
        img := ApplyAutPair(g, cur);;
        if not (img in orb) then
          Add(orb, img);; Add(frontier, img);;
        fi;
      od;
    od;
    Add(orbits, orb);;
    remaining := Filtered(remaining, x -> not (x in orb));;
  od;
  Print("  num_orbits = ", Length(orbits), " (sizes: ", List(orbits,Length), ")\n");

  ## regularity self-check (theorem_check SSF.10.1: stabilizer of a
  ## generating pair under Aut is always trivial => every orbit size =
  ## |Aut|)
  regularOk := ForAll(orbits, o -> Length(o) = autOrder);;
  Print("  regularity check (all orbit sizes = |Aut|): ", regularOk, "\n");

  ## reflexible test + nu-mapping per orbit
  orbitRecs := [];;
  for oi in [1..Length(orbits)] do
    rep := orbits[oi][1];;
    r := rep[1];; s := rep[2];;
    reflexible := ForAny(A, alpha -> Image(alpha,r) = r^-1 and Image(alpha,s) = s^-1);;
    nuImg := [r, s^-1];;   ## nu(r,s) = (r^-1,s^-1) = (r,s^2) since r^2=1
    ## find which orbit nu(rep) belongs to
    nuOrbitIdx := fail;;
    for oj in [1..Length(orbits)] do
      if nuImg in orbits[oj] then nuOrbitIdx := oj; break; fi;
    od;
    Add(orbitRecs, rec(orbit_index := oi, size := Length(orbits[oi]),
        reflexible := reflexible, nu_maps_to_orbit_index := nuOrbitIdx,
        rep_r := String(r), rep_s := String(s)));;
    Print("    orbit ", oi, ": size=", Length(orbits[oi]), " reflexible=", reflexible,
          " nu->orbit ", nuOrbitIdx, "\n");
  od;

  Add(G4_RESULTS, rec(order := w.order, id := w.id, M_size := Length(M),
      aut_order := autOrder, num_orbits := Length(orbits), regular_ok := regularOk,
      orbits := orbitRecs));;
od;

Print("\n=== G4 summary ===\n");
Print("windows processed: ", Length(G4_RESULTS), " / ", Length(WINDOWS), "\n");
Print("HANDOFF_MISMATCHES: ", Length(HANDOFF_MISMATCHES), "\n");

#############################################################################
## PART 2 -- G5 (twin/mirror/exotic classification), verbatim vocabulary of
## theorem_check_mirrorall_l3vacuous_v1.md SSG.6 (Lemma BOTH-FIXED-EXOTIC,
## fiber formula #pairs = C(K,2)-t). GT predicates are NOT evaluated here
## ("window" is used only as the already-defined G3-pass predicate, per
## 司令塔's instruction) -- this is a WORD-LEVEL classification of the
## abstract (r,s)-labelled maps, exactly as F.8/F.10/G.6 already do for the
## 432/486 precedent.
#############################################################################
Print("\n=== G5 classification ===\n");
G5_RESULTS := [];;
NONREFLEXIBLE_TWIN_ALERTS := [];;   ## for the "1 件でも即報告" instruction

for gr in G4_RESULTS do
  K := gr.num_orbits;;
  reflexibleIdx := Filtered([1..K], i -> gr.orbits[i].reflexible);;
  f := Length(reflexibleIdx);;   ## number of self-nu-fixed (reflexible) orbits
  ## verify involution structure: every non-reflexible orbit's nu-image is
  ## itself non-reflexible and the mapping is a fixed-point-free involution
  ## on the non-reflexible subset (sanity, should always hold per SSF.10.2)
  nonReflIdx := Filtered([1..K], i -> not gr.orbits[i].reflexible);;
  involutionOk := true;;
  for i in nonReflIdx do
    j := gr.orbits[i].nu_maps_to_orbit_index;;
    if j = fail or j = i or gr.orbits[j].nu_maps_to_orbit_index <> i then
      involutionOk := false;;
    fi;
  od;
  t := (K - f) / 2;;   ## number of chiral nu-pairs (mirror pairs)

  classification := "";;
  if K = 1 and f = 1 then
    classification := "isolated_self_mirror_no_twin";;
  elif K = 2 and f = 0 and t = 1 then
    classification := "single_mirror_pair_non_exotic";;
  elif K = 2 and f = 2 then
    classification := "both_fixed_twin_exotic";;
    Add(NONREFLEXIBLE_TWIN_ALERTS, rec(order:=gr.order, id:=gr.id, note:="both_fixed_twin_exotic (2 reflexible orbits, distinct windows, EXOTIC per Lemma BOTH-FIXED-EXOTIC)"));;
  else
    classification := "multi_orbit_mixed_structure";;
    if f > 0 or t > 1 then
      Add(NONREFLEXIBLE_TWIN_ALERTS, rec(order:=gr.order, id:=gr.id,
          note:=Concatenation("multi_orbit_mixed_structure K=",String(K)," f=",String(f)," t=",String(t)," -- needs case-by-case review")));;
    fi;
  fi;

  ## exotic pair count (fiber formula, SSG.6.a): C(K,2) - t
  exoticPairs := (K*(K-1))/2 - t;;

  Print("  (", gr.order, ",", gr.id, "): K=", K, " reflexible=", f, " chiral_pairs=", t,
        " involution_ok=", involutionOk, " class=", classification, " exotic_pairs=", exoticPairs, "\n");

  Add(G5_RESULTS, rec(order := gr.order, id := gr.id, num_orbits := K,
      num_reflexible := f, num_chiral_pairs := t, involution_ok := involutionOk,
      classification := classification, exotic_pair_count := exoticPairs));;
od;;

Print("\n=== G5 alerts (non-standard structure) ===\n");
Print("count: ", Length(NONREFLEXIBLE_TWIN_ALERTS), "\n");
for al in NONREFLEXIBLE_TWIN_ALERTS do
  Print("  (", al.order, ",", al.id, "): ", al.note, "\n");
od;

#############################################################################
## PART 3 -- cert output
#############################################################################
G4RecordsJson := JArr(List(G4_RESULTS, function(gr)
  return Concatenation(
    "{\"order\":", String(gr.order), ",\"id\":", String(gr.id),
    ",\"M_size\":", String(gr.M_size), ",\"aut_order\":", String(gr.aut_order),
    ",\"num_orbits\":", String(gr.num_orbits), ",\"regular_ok\":", JB(gr.regular_ok),
    ",\"orbits\":", JArr(List(gr.orbits, o -> Concatenation(
        "{\"orbit_index\":", String(o.orbit_index), ",\"size\":", String(o.size),
        ",\"reflexible\":", JB(o.reflexible),
        ",\"nu_maps_to_orbit_index\":", (function() if o.nu_maps_to_orbit_index=fail then return "null"; else return String(o.nu_maps_to_orbit_index); fi; end)(),
        ",\"rep_r\":", JStr(o.rep_r), ",\"rep_s\":", JStr(o.rep_s), "}"))),
    "}");
end));;

G5RecordsJson := JArr(List(G5_RESULTS, function(g5)
  return Concatenation(
    "{\"order\":", String(g5.order), ",\"id\":", String(g5.id),
    ",\"num_orbits\":", String(g5.num_orbits), ",\"num_reflexible\":", String(g5.num_reflexible),
    ",\"num_chiral_pairs\":", String(g5.num_chiral_pairs), ",\"involution_ok\":", JB(g5.involution_ok),
    ",\"classification\":", JStr(g5.classification), ",\"exotic_pair_count\":", String(g5.exotic_pair_count),
    "}");
end));;

AlertsJson := JArr(List(NONREFLEXIBLE_TWIN_ALERTS, al -> Concatenation(
    "{\"order\":", String(al.order), ",\"id\":", String(al.id), ",\"note\":", JStr(al.note), "}")));;

HandoffJson := JArr(List(HANDOFF_MISMATCHES, w -> Concatenation(
    "{\"order\":", String(w.order), ",\"id\":", String(w.id), "}")));;

selfSha := ComputeSha256File("search/probe/sg_band_sweep/sg_g4_orb_driver_v1.g");;
inputCertSha := ComputeSha256File(INPUT_CERT_PATH);;

classCounts := rec();;
for g5 in G5_RESULTS do
  key := g5.classification;;
  if IsBound(classCounts.(key)) then classCounts.(key) := classCounts.(key)+1; else classCounts.(key):=1; fi;
od;;
ClassCountsJson := Concatenation("{", JoinC(List(RecNames(classCounts), k -> Concatenation(JStr(k),":",String(classCounts.(k)))), ","), "}");;

cert := Concatenation(
"{\n",
"\"schema\":\"shadow-atelier/sg-g4-g5-orb/v1\",\n",
"\"driver_self_sha256\":", JStr(selfSha), ",\n",
"\"authority\":\"裁定649 (司令塔), executing prereg SS7.2 connection spec + theorem_check_mirrorall_l3vacuous_v1.md SSF.8/F.10/G.6 methodology (verbatim reuse, not new design)\",\n",
"\"input_cert\":{\"path\":", JStr(INPUT_CERT_PATH), ",\"sha256\":", JStr(inputCertSha), "},\n",
"\"windows_total\":", String(Length(ALL_WINDOWS)), ",\n",
"\"windows_in_this_shard\":", String(Length(WINDOWS)), ",\n",
"\"shard_range\":", JArr(List(G4_WINDOW_RANGE,String)), ",\n",
"\"windows_processed\":", String(Length(G4_RESULTS)), ",\n",
"\"handoff_mismatches\":", HandoffJson, ",\n",
"\"entry_gate_note\":\"per window, (r,s) was INDEPENDENTLY rediscovered (full scan of all involutions x all order-3 elements, not the stored witness string) plus a fresh GQuotients(Ghat,S3) check -- a stronger re-verification than parsing the original witness back into an element\",\n",
"\"pruning_note\":\"M enumerated WITHOUT the G2 conjugacy-class pruning (prereg SS7.2 item 3, verbatim warning honored) -- r ranges over ALL order-2 elements, not class reps\",\n",
"\"g4_orb_records\":", G4RecordsJson, ",\n",
"\"g5_classification\":", G5RecordsJson, ",\n",
"\"g5_classification_counts\":", ClassCountsJson, ",\n",
"\"g5_alerts_nonstandard_structure\":", AlertsJson, ",\n",
"\"vocabulary_note\":\"classification labels follow theorem_check_mirrorall_l3vacuous_v1.md SSG.6 verbatim: mirror_pair(鏡映対)=2 chiral orbits that are each other's nu-image, NOT exotic (explained by iota, matches 432/486 precedent); both_fixed(両固定)=2+ reflexible orbits for the same Ghat, EXOTIC (Lemma BOTH-FIXED-EXOTIC); isolated_self_mirror=a single reflexible orbit, no twin partner at all. GT predicates (hexagon/charming/SURJ/settled/isolated) are NOT evaluated anywhere here -- 'window' is used only as the pre-defined G3-pass predicate from the G0-G3 sweep, per instruction.\",\n",
"\"claims\":{\"exotic_verdict\":\"UNKNOWN\",\"grading_and_novelty\":\"out of scope for implementer per prereg SS10 item 4 -- classification counts above are raw measurements, not a settled/isolated/GTSh claim\"},\n",
"\"non_contact_declaration\":{\"im_R\":false,\"d_N\":false,\"sealed_quantities\":false,\"n5_series\":false}\n",
"}\n");;

OUT_PATH := Concatenation("search/certs/sg_g4_g5_orb_20260806", G4_OUT_SUFFIX, ".json");;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nW6_SG_G4_G5_DONE\n");
QUIT;
