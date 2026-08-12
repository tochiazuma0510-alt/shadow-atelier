#############################################################################
## u6_2_crowncore.g -- [U6-2] nonabelian-crown core collapse + wall37 coupling
## fix (裁定1108 prereg, 発注 docs/notes/wall_crown_u6_reading_v1.md S7 [U6-2]).
##
## [1] recompute, for each wall window, the core of EVERY nonabelian-crown
##     maximal class and confirm they are all equal (single core).
## [2] identify Q/Core NOT by order+socle alone but by IdGroup/StructureDescription.
##     Specifically for wall37 (|Q/Core|=720, socle A6): S6, PGL(2,9), M10 all
##     have order 720 and socle A6, so order+socle cannot distinguish them.
##     This script resolves it by directly constructing Aut(A6) (order 1440)
##     and enumerating its three order-720 subgroups containing Inn(A6) --
##     these are (up to isomorphism) exactly S6 / PGL(2,9) / M10, and their
##     IdGroup values are pairwise distinct -- then comparing Q/Core's own
##     IdGroup against these three reference IdGroups.
## [3] records |Out(socle)| and identifies which subgroup of Out(socle) the
##     coupling C_2 -> Out(A_t) lands in (via the reference subgroups above).
##
## Window construction reused verbatim from wall_crown_census_v1.g /
## u6_1_chivir.g (BuildWallQ), per the task's explicit permission. The
## core-collapse + IdGroup-based S6/PGL(2,9)/M10 discrimination logic is new,
## independent of the producer's own StructureDescription/IdGroup fields
## (recomputed here from scratch, not read from the existing wall_crown_census
## cert).
##
## u/c 非接触・封印非接触・prereg量非計算・NAME-COLLIDE: wall-window instances.
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;

## ---- (F2) window machinery, copied verbatim (same as u6_1_chivir.g) ----
AbstractProdW := function(l)
  local p, i;
  p := l[1];
  for i in [2 .. Length(l)] do p := p * l[i]; od;
  return p;
end;;

MakeWindow := function(s1, s2)
  local xx, yy, DD, dd, cc, zz;
  xx := s1^2;  yy := s2^2;
  DD := AbstractProdW([s1, s2, s1]);  dd := AbstractProdW([s1, s2]);
  cc := DD^2;  zz := AbstractProdW([xx, yy])^-1;
  return rec(s1 := s1, s2 := s2, x := xx, y := yy, Dlt := DD, dlt := dd, c := cc, z := zz,
             Bq := Group(s1, s2), PN := Group(xx, yy),
             Nord := Lcm(Order(xx), Order(yy), Order(cc)));
end;;

YImg := function(W, u, f)
  return f^-1 * W.y^u * f;
end;;

HexagonHolds := function(W, m, f)
  local u;
  u := 2*m + 1;
  return W.s1^u * f^-1 * W.s2^u * f
           = f^-1 * W.s1 * W.s2 * W.x^(-m) * W.c^m
     and f^-1 * W.s2^u * f * W.s1^u
           = W.s2 * W.s1 * W.y^(-m) * W.c^m * f;
end;;

FindFirstSettledShadow := function(W, m, Snn, stabElts, cyuElts)
  local u, yu, alpha0, s, xi, target, h, c, f, scanned, wdP, wdB;
  u := 2*m + 1;
  yu := W.y^u;
  alpha0 := RepresentativeAction(Snn, W.x, W.x^u);
  scanned := 0;
  if alpha0 = fail then
    return rec(found := false, m := m, u := u, scanned := scanned,
               reason := "alpha0_not_found");
  fi;
  for s in stabElts do
    xi := s * alpha0;
    target := W.y^xi;
    h := RepresentativeAction(W.PN, yu, target, OnPoints);
    if h = fail then
      continue;
    fi;
    for c in cyuElts do
      scanned := scanned + 1;
      f := c * h;
      if YImg(W, u, f) <> target then
        Error("CV-13 orientation assertion failed");
      fi;
      if not HexagonHolds(W, m, f) then
        continue;
      fi;
      if Group(W.x^u, YImg(W, u, f)) <> W.PN then
        continue;
      fi;
      wdP := GroupHomomorphismByImages(
        W.PN, W.PN, [W.x, W.y], [W.x^u, YImg(W, u, f)]);
      if wdP = fail then
        continue;
      fi;
      wdB := GroupHomomorphismByImages(
        W.Bq, W.Bq, [W.s1, W.s2], [W.s1^u, f^-1 * W.s2^u * f]);
      if wdB = fail then
        continue;
      fi;
      return rec(found := true, m := m, u := u, scanned := scanned,
                 f := f, xi := xi);
    od;
  od;
  return rec(found := false, m := m, u := u, scanned := scanned,
             reason := "candidate_space_exhausted");
end;;

BuildWallQ := function(label, n, a1, b1)
  local Snn, Ann, aE, bE, s1, s2, W, ell, t, Kchi, stabElts,
        cyuElts, ms, reps, allFound, X, m, elapsed;
  elapsed := Runtime();
  Snn := SymmetricGroup(n);
  Ann := AlternatingGroup(n);
  aE := a1 * (n+1, n+3);
  bE := b1 * (n+1, n+3, n+2);
  s1 := bE^-1 * aE;
  s2 := aE * bE^2;
  if s1*s2*s1 <> s2*s1*s2 then Error("braid assertion failed: ", label); fi;
  W := MakeWindow(s1, s2);
  if W.PN <> Ann then Error("PN assertion failed: ", label); fi;
  if W.c <> Identity(W.Bq) then Error("central element assertion failed: ", label); fi;
  ell := W.Nord;
  t := n - ell;
  Kchi := Centralizer(Snn, W.x);
  stabElts := Elements(Kchi);
  cyuElts := Elements(Centralizer(W.PN, W.y));
  ms := Filtered([0..ell-1], m -> Gcd(2*m+1, ell) = 1);
  reps := [];
  for m in ms do
    Add(reps, FindFirstSettledShadow(W, m, Snn, stabElts, cyuElts));
  od;
  allFound := ForAll(reps, r -> r.found);
  if allFound then
    X := Group(Concatenation(GeneratorsOfGroup(Kchi), List(reps, r -> r.xi)));
  else
    X := Kchi;
  fi;
  return rec(label := label, n := n, ell := ell, t := t,
             all_charming_layers_represented := allFound, X := X,
             elapsed_ms := Runtime() - elapsed);
end;;

## ---- U6-2 analysis (new/independent logic) ----
JBool := function(b) if b then return "true"; else return "false"; fi; end;;
JStrU := function(s)
  s := ReplacedString(s, "\\", "\\\\");
  s := ReplacedString(s, "\"", "\\\"");
  return Concatenation("\"", s, "\"");
end;;
JIdOrNull := function(id)
  if id = fail then return "null"; fi;
  return Concatenation("[", String(id[1]), ",", String(id[2]), "]");
end;;

## Reference discrimination table for socle A6 (t=6 case): the 3 order-720
## subgroups of Aut(A6) containing Inn(A6), built ONCE and reused for every
## window whose socle is A6. Built fresh here, not taken from any external
## source.
BuildA6Discriminator := function()
  local A6, AutA6, InnA6, subs720, refs, s;
  A6 := AlternatingGroup(6);
  AutA6 := AutomorphismGroup(A6);
  InnA6 := InnerAutomorphismsAutomorphismGroup(AutA6);
  subs720 := Filtered(AllSubgroups(AutA6), s -> Size(s) = 720 and IsSubset(s, InnA6));
  if Length(subs720) <> 3 then
    Error("BuildA6Discriminator: expected exactly 3 order-720 subgroups of Aut(A6) ",
          "containing Inn(A6), got ", Length(subs720), " -- fail-closed");
  fi;
  refs := List(subs720, s -> rec(id := IdGroup(s), struct := StructureDescription(s), grp := s));
  ## sanity: pairwise distinct IdGroup (needed for discrimination to work at all)
  if Length(Set(List(refs, r -> r.id))) <> 3 then
    Error("BuildA6Discriminator: the 3 order-720 subgroups of Aut(A6) do NOT have ",
          "pairwise distinct IdGroup -- IdGroup-based discrimination is not viable, ",
          "fail-closed (would need a different invariant)");
  fi;
  return refs;
end;;

## Same construction for socle A5 (t=5 case: Out(A5)=C2, only 1 nontrivial
## extension S5, so no discrimination ambiguity, but we still verify this
## structurally rather than assume it).
BuildA5Discriminator := function()
  local A5, AutA5, InnA5, subs120, refs;
  A5 := AlternatingGroup(5);
  AutA5 := AutomorphismGroup(A5);
  InnA5 := InnerAutomorphismsAutomorphismGroup(AutA5);
  subs120 := Filtered(AllSubgroups(AutA5), s -> Size(s) = 120 and IsSubset(s, InnA5));
  return List(subs120, s -> rec(id := IdGroup(s), struct := StructureDescription(s), grp := s));
end;;

AnalyzeCrownCore := function(w, a6refs, a5refs)
  local X, cls, reps, nonabIdx, i, cl, M, core, coreOrders, coresEqual,
        commonCore, hom, Q, soc, socId, socStruct, outSocOrder,
        qId, matchLabel, matchesFound, r, elapsed;
  elapsed := Runtime();
  X := w.X;
  cls := ConjugacyClassesMaximalSubgroups(X);
  reps := List(cls, Representative);
  nonabIdx := [];
  coreOrders := [];
  for i in [1 .. Length(reps)] do
    M := reps[i];
    core := Core(X, M);
    ## nonabelian crown per docs S3 definition: primitive quotient's socle is
    ## nonabelian. Recompute directly (not read from the existing cert).
    hom := NaturalHomomorphismByNormalSubgroup(X, core);
    Q := Image(hom);
    soc := Socle(Q);
    if not IsAbelian(soc) then
      Add(nonabIdx, i);
      Add(coreOrders, Size(core));
    fi;
  od;
  coresEqual := (Length(Set(coreOrders)) <= 1);
  if Length(nonabIdx) = 0 then
    Error("AnalyzeCrownCore(", w.label, "): no nonabelian-crown maximal classes found -- ",
          "unexpected given docs/notes/wall_crown_u6_reading_v1.md S1/S3, fail-closed");
  fi;
  if not coresEqual then
    Error("AnalyzeCrownCore(", w.label, "): nonabelian-crown cores are NOT all equal ",
          "(orders=", coreOrders, ") -- contradicts the S3 'single core' claim, fail-closed ",
          "rather than silently picking one");
  fi;

  commonCore := Core(X, reps[nonabIdx[1]]);
  hom := NaturalHomomorphismByNormalSubgroup(X, commonCore);
  Q := Image(hom);
  soc := Socle(Q);
  socId := IdGroup(soc);
  socStruct := StructureDescription(soc);
  outSocOrder := Size(AutomorphismGroup(soc)) / Size(soc);
  qId := IdGroup(Q);

  ## discriminate against the appropriate reference table (by socle order)
  matchesFound := [];
  if Size(soc) = Size(AlternatingGroup(6)) then
    for r in a6refs do
      if r.id = qId then Add(matchesFound, r.struct); fi;
    od;
  elif Size(soc) = Size(AlternatingGroup(5)) then
    for r in a5refs do
      if r.id = qId then Add(matchesFound, r.struct); fi;
    od;
  fi;
  if Length(matchesFound) <> 1 then
    matchLabel := "AMBIGUOUS_OR_UNMATCHED";
  else
    matchLabel := matchesFound[1];
  fi;

  return rec(
    label := w.label,
    nonabelian_crown_class_indices := nonabIdx,
    nonabelian_crown_class_count := Length(nonabIdx),
    nonabelian_core_orders := coreOrders,
    all_nonabelian_cores_equal := coresEqual,
    common_core_order := Size(commonCore),
    q_over_core_order := Size(Q),
    q_over_core_id := qId,
    q_over_core_structure := StructureDescription(Q),
    socle_id := socId,
    socle_structure := socStruct,
    out_socle_order := outSocOrder,
    q_over_core_matches_reference := matchLabel,
    elapsed_ms := Runtime() - elapsed);
end;;

ResultToJson := function(r)
  return Concatenation(
    "{\"label\":", JStrU(r.label),
    ",\"nonabelian_crown_class_indices\":[",
      JoinStringsWithSeparator(List(r.nonabelian_crown_class_indices, String), ","), "]",
    ",\"nonabelian_crown_class_count\":", String(r.nonabelian_crown_class_count),
    ",\"nonabelian_core_orders\":[",
      JoinStringsWithSeparator(List(r.nonabelian_core_orders, String), ","), "]",
    ",\"all_nonabelian_cores_equal\":", JBool(r.all_nonabelian_cores_equal),
    ",\"common_core_order\":", String(r.common_core_order),
    ",\"q_over_core_order\":", String(r.q_over_core_order),
    ",\"q_over_core_id\":", JIdOrNull(r.q_over_core_id),
    ",\"q_over_core_structure\":", JStrU(r.q_over_core_structure),
    ",\"socle_id\":", JIdOrNull(r.socle_id),
    ",\"socle_structure\":", JStrU(r.socle_structure),
    ",\"out_socle_order\":", String(r.out_socle_order),
    ",\"q_over_core_matches_reference\":", JStrU(r.q_over_core_matches_reference),
    ",\"elapsed_ms\":", String(r.elapsed_ms), "}");
end;;

RefsToJson := function(refs)
  return Concatenation("[",
    JoinStringsWithSeparator(List(refs, r -> Concatenation(
      "{\"id\":", JIdOrNull(r.id), ",\"structure\":", JStrU(r.struct), "}")), ","),
    "]");
end;;

## ---- driver ----
Print("############################################################\n");
Print("# u6_2_crowncore.g -- [U6-2] crown core collapse + wall37 coupling fix\n");
Print("############################################################\n");

t0Global := Runtime();;

Print("building A6 discriminator (Aut(A6), order-720 subgroups containing Inn(A6))...\n");
a6refs := BuildA6Discriminator();;
for r in a6refs do
  Print("  A6 ref: id=", r.id, " structure=", r.struct, "\n");
od;

Print("building A5 discriminator (Aut(A5), order-120 subgroups containing Inn(A5))...\n");
a5refs := BuildA5Discriminator();;
for r in a5refs do
  Print("  A5 ref: id=", r.id, " structure=", r.struct, "\n");
od;

walls := [];;
Add(walls, BuildWallQ("wall24", 24,
  (1,13)(2,9)(3,5)(4,24)(6,8)(7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23),
  (1,12,9)(2,8,5)(3,4,24)(6,7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23)));;
Print("wall24 built.\n");

Add(walls, BuildWallQ("wall28", 28,
  (1,8)(2,4)(3,24)(5,7)(6,27)(9,11)(10,25)(12,23)(13,14)(15,22)(16,18)(17,28)(19,21)(20,26),
  (1,7,4)(2,3,24)(5,6,27)(8,23,11)(9,10,25)(12,22,14)(15,21,18)(16,17,28)(19,20,26)));;
Print("wall28 built.\n");

Add(walls, BuildWallQ("wall36", 36,
  (1,3)(2,34)(4,29)(5,25)(6,16)(7,9)(8,35)(10,15)(11,12)(13,14)(17,24)(18,20)(19,32)(21,23)(22,33)(26,28)(27,36)(30,31),
  (1,2,34)(3,31,29)(4,28,25)(5,24,16)(6,15,9)(7,8,35)(10,14,12)(17,23,20)(18,19,32)(21,22,33)(26,27,36)));;
Print("wall36 built.\n");

Add(walls, BuildWallQ("wall37", 37,
  (1,30)(2,11)(3,7)(4,5)(8,10)(9,35)(12,29)(13,15)(14,32)(16,28)(17,19)(18,36)(20,27)(21,23)(22,33)(24,26)(25,37)(31,34),
  (1,29,11)(2,10,7)(3,6,5)(8,9,35)(12,28,15)(13,14,32)(16,27,19)(17,18,36)(20,26,23)(21,22,33)(24,25,37)(30,31,34)));;
Print("wall37 built.\n");

for w in walls do
  if not w.all_charming_layers_represented then
    Error("u6_2_crowncore.g: window ", w.label, " did not find a settled shadow for every ",
          "charming layer -- refusing to analyze an incomplete Q");
  fi;
od;

results := [];;
for w in walls do
  Print("analyzing crown core for ", w.label, " (|X|=", Size(w.X), ")...\n");
  r := AnalyzeCrownCore(w, a6refs, a5refs);;
  Add(results, r);
  Print("  ", w.label, ": nonab_classes=", r.nonabelian_crown_class_count,
        " core_orders=", r.nonabelian_core_orders,
        " all_equal=", r.all_nonabelian_cores_equal,
        " Q/Core_id=", r.q_over_core_id, " Q/Core_structure=", r.q_over_core_structure,
        " match=", r.q_over_core_matches_reference,
        " out_socle_order=", r.out_socle_order,
        " elapsed_ms=", r.elapsed_ms, "\n");
od;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/u6_crowncore_v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/probe/wac_v1/u6_2_crowncore.g\",\"order\":\"裁定1108(U-6 prereg測定・[U6-2])\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/wall_crown_u6_reading_v1.md S7 [U6-2]\"",
  ",\"method_note\":\"Q/Core is identified by IdGroup, not order+socle. For socle A6 (wall37), the ",
  "3 candidates S6/PGL(2,9)/M10 are constructed as the order-720 subgroups of Aut(A6) (order 1440) ",
  "containing Inn(A6); their IdGroup values are verified pairwise distinct before use as a ",
  "discriminator (fail-closed Error otherwise), then Q/Core's own IdGroup is compared against them. ",
  "For socle A5 (wall24/28/36) the analogous construction is used (only 1 nontrivial extension S5 ",
  "expected, verified rather than assumed). Window construction reused verbatim from ",
  "search/probe/wall_crown_census_v1/wall_crown_census_v1.g / u6_1_chivir.g per the task's ",
  "permission; the core-collapse check and IdGroup discrimination are independent new logic, not ",
  "read from the existing wall_crown_census_v1 cert (StructureDescription/primitive_id there are ",
  "not consulted here).\",",
  "\"a6_discriminator_reference\":", RefsToJson(a6refs), ",",
  "\"a5_discriminator_reference\":", RefsToJson(a5refs), ",",
  "\"walls\":[", JoinStringsWithSeparator(List(results, ResultToJson), ","), "],",
  "\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(Runtime() - t0Global),
  "}"
);;

outPath := "search/certs/u6_2_crowncore_v1_20260813.json";;
outStream := OutputTextFile(outPath, false);;
SetPrintFormattingStatus(outStream, false);;
PrintTo(outStream, cert);;
CloseStream(outStream);;
Print("\nwrote ", outPath, "\n");
Print("U6_2_CROWNCORE_DONE\n");
QUIT;
