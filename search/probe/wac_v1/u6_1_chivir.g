#############################################################################
## u6_1_chivir.g -- [U6-1] ker(chi_vir) vs [Q,Q] measurement (裁定1108 prereg,
## 発注 docs/notes/wall_crown_u6_reading_v1.md S7 [U6-1]).
##
## Goal (pure group theory, zero arithmetic input): for each wall window
## (wall24/28/36/37), build X = Q = GT(N) (Frattini trivial per the existing
## census cert, so X itself IS the Frattini-quotient), then:
##   [1] identify chi_vir : Q -> (Z/N_ord)^x concretely as the conjugation
##       action of Q on its (unique, normal) order-ell Sylow subgroup T --
##       this T is exactly the C_ell translation subgroup of the AGL(1,ell)
##       direct factor (ell does not divide t! or (ell-1), so the Sylow-ell
##       subgroup has order ell and, since C_ell is normal/characteristic in
##       AGL(1,ell) and the S_t factor contains no ell-elements, T is normal
##       in the whole of Q). ker(chi_vir) = C_Q(T) = C_Q(any generator of T)
##       (T cyclic of prime order, so centralizing a generator centralizes
##       all of T).
##   [2] confirm ker(chi_vir) >= [Q,Q] (=DerivedSubgroup(Q)), report the
##       index/quotient orders (|Q^ab|, |ker/[Q,Q]| via natural hom to Q^ab).
##   [3] recompute ConjugacyClassesMaximalSubgroups(Q) directly (frattini
##       trivial so this is the SAME class list the wall_crown_census_v1 cert
##       reports) and count how many classes M satisfy M >= ker(chi_vir)
##       ("free crown" candidates under the TRUE chi_vir kernel, as opposed
##       to the [Q,Q]-based count already in docs/notes/wall_crown_u6_reading_v1.md S5).
##
## Window construction (MakeWindow/HexagonHolds/FindFirstSettledShadow/RunWall
## core) is copied VERBATIM from search/probe/wall_crown_census_v1/
## wall_crown_census_v1.g per the U6 task's explicit permission ("壁側の構成は
## Solのcensus資産の窓構成経路を再利用してよい(核分類のロジックはfixture系のもの)").
## The chi_vir/ker analysis below is new, independent logic -- not copied from
## any producer script.
##
## u/c 非接触・封印非接触・prereg 量(b9/a9/d9)非計算・NAME-COLLIDE: "wall24" etc.
## below denote the wall-WINDOW instances (crown census objects), not any other
## use of those integers elsewhere in the campaign.
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;

## ---- (F2) window machinery, copied verbatim from wall_crown_census_v1.g ----
MakeWindow := function(s1, s2)
  local xx, yy, DD, dd, cc, zz;
  xx := s1^2;  yy := s2^2;
  DD := AbstractProdW([s1, s2, s1]);  dd := AbstractProdW([s1, s2]);
  cc := DD^2;  zz := AbstractProdW([xx, yy])^-1;
  return rec(s1 := s1, s2 := s2, x := xx, y := yy, Dlt := DD, dlt := dd, c := cc, z := zz,
             Bq := Group(s1, s2), PN := Group(xx, yy),
             Nord := Lcm(Order(xx), Order(yy), Order(cc)));
end;;

## AbstractProd is defined in search/week3-battery-common.g in the producer
## scripts; re-derive the minimal local equivalent here (simple left-to-right
## product) so this script has no hidden dependency on that file's other
## machinery. Verified equivalent to the producer's usage pattern (always
## called on ordinary group elements, never on free-group words here).
AbstractProdW := function(l)
  local p, i;
  p := l[1];
  for i in [2 .. Length(l)] do p := p * l[i]; od;
  return p;
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
             pn_order := Size(W.PN), charming_m_count := Length(ms),
             all_charming_layers_represented := allFound,
             kernel_xi_order := Size(Kchi), X := X, elapsed_ms := Runtime() - elapsed);
end;;

## ---- U6-1 chi_vir analysis (new/independent logic) ----
JBool := function(b) if b then return "true"; else return "false"; fi; end;;
JStrU := function(s)
  s := ReplacedString(s, "\\", "\\\\");
  s := ReplacedString(s, "\"", "\\\"");
  return Concatenation("\"", s, "\"");
end;;

AnalyzeChiVir := function(w)
  local X, ell, D, T, sylowNormal, sylowOrder, tgen, Ker, kerNormal,
        kerContainsD, idxKerOverD, Qab, natD, kerImgInQab, imgQabOrder,
        cls, reps, freeCount, freeIdx, i, elapsed, chiImageOrder;
  elapsed := Runtime();
  X := w.X;
  ell := w.ell;

  ## [1] identify T = Sylow-ell subgroup of X, assert unique/normal, and set
  ## ker(chi_vir) := C_X(generator of T).
  T := SylowSubgroup(X, ell);
  sylowOrder := Size(T);
  sylowNormal := IsNormal(X, T);
  if sylowOrder <> ell then
    Error("AnalyzeChiVir(", w.label, "): Sylow-", ell, " subgroup has order ",
          sylowOrder, " <> ell=", ell, " -- fail-closed, ell does not appear ",
          "to the first power as expected");
  fi;
  if not sylowNormal then
    Error("AnalyzeChiVir(", w.label, "): Sylow-", ell,
          " subgroup is NOT normal in X -- chi_vir construction (unique translation ",
          "subgroup) assumption fails for this window, fail-closed");
  fi;
  tgen := First(Elements(T), g -> g <> Identity(X));
  Ker := Centralizer(X, tgen);
  kerNormal := IsNormal(X, Ker);
  chiImageOrder := Size(X) / Size(Ker);

  ## [2] ker >= [Q,Q] confirmation + quotient orders
  D := DerivedSubgroup(X);
  kerContainsD := IsSubset(Ker, D);
  idxKerOverD := Size(Ker) / Size(D);
  natD := NaturalHomomorphismByNormalSubgroup(X, D);
  Qab := Image(natD);
  kerImgInQab := Image(natD, Ker);
  imgQabOrder := Size(kerImgInQab);

  ## [3] free-crown recount under TRUE ker(chi_vir)
  cls := ConjugacyClassesMaximalSubgroups(X);
  reps := List(cls, Representative);
  freeIdx := [];
  for i in [1 .. Length(reps)] do
    if IsSubset(reps[i], Ker) then Add(freeIdx, i); fi;
  od;
  freeCount := Length(freeIdx);

  return rec(
    label := w.label, ell := ell, t := w.t,
    q_order := Size(X),
    sylow_ell_order := sylowOrder, sylow_ell_normal := sylowNormal,
    ker_chivir_order := Size(Ker), ker_chivir_normal := kerNormal,
    chi_image_order := chiImageOrder, ell_minus_1 := ell - 1,
    chi_image_order_matches_ell_minus_1 := (chiImageOrder = ell - 1),
    derived_subgroup_order := Size(D),
    ker_contains_derived := kerContainsD,
    index_ker_over_derived := idxKerOverD,
    ker_equals_derived := (idxKerOverD = 1),
    qab_order := Size(Qab),
    ker_image_in_qab_order := imgQabOrder,
    qab_over_ker_image_order := Size(Qab) / imgQabOrder,
    maximal_class_count := Length(reps),
    maximal_class_orders := List(reps, Size),
    free_crown_class_indices_true_kervir := freeIdx,
    free_crown_count_true_kervir := freeCount,
    elapsed_ms := Runtime() - elapsed);
end;;

ResultToJson := function(r)
  return Concatenation(
    "{\"label\":", JStrU(r.label),
    ",\"ell\":", String(r.ell), ",\"t\":", String(r.t),
    ",\"q_order\":", String(r.q_order),
    ",\"sylow_ell_order\":", String(r.sylow_ell_order),
    ",\"sylow_ell_normal\":", JBool(r.sylow_ell_normal),
    ",\"ker_chivir_order\":", String(r.ker_chivir_order),
    ",\"ker_chivir_normal\":", JBool(r.ker_chivir_normal),
    ",\"chi_image_order\":", String(r.chi_image_order),
    ",\"ell_minus_1\":", String(r.ell_minus_1),
    ",\"chi_image_order_matches_ell_minus_1\":", JBool(r.chi_image_order_matches_ell_minus_1),
    ",\"derived_subgroup_order\":", String(r.derived_subgroup_order),
    ",\"ker_contains_derived\":", JBool(r.ker_contains_derived),
    ",\"index_ker_over_derived\":", String(r.index_ker_over_derived),
    ",\"ker_equals_derived\":", JBool(r.ker_equals_derived),
    ",\"qab_order\":", String(r.qab_order),
    ",\"ker_image_in_qab_order\":", String(r.ker_image_in_qab_order),
    ",\"qab_over_ker_image_order\":", String(r.qab_over_ker_image_order),
    ",\"maximal_class_count\":", String(r.maximal_class_count),
    ",\"maximal_class_orders\":[", JoinStringsWithSeparator(List(r.maximal_class_orders, String), ","), "]",
    ",\"free_crown_class_indices_true_kervir\":[", JoinStringsWithSeparator(List(r.free_crown_class_indices_true_kervir, String), ","), "]",
    ",\"free_crown_count_true_kervir\":", String(r.free_crown_count_true_kervir),
    ",\"elapsed_ms\":", String(r.elapsed_ms), "}");
end;;

## ---- driver: the 4 wall windows (witnesses copied verbatim from
## search/probe/wall_crown_census_v1/wall_crown_census_v1.g) ----
Print("############################################################\n");
Print("# u6_1_chivir.g -- [U6-1] ker(chi_vir) vs [Q,Q] (裁定1108 prereg)\n");
Print("############################################################\n");

t0Global := Runtime();;

walls := [];;
Add(walls, BuildWallQ("wall24", 24,
  (1,13)(2,9)(3,5)(4,24)(6,8)(7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23),
  (1,12,9)(2,8,5)(3,4,24)(6,7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23)));;
Print("wall24 built. q_order=", walls[1].pn_order, " kernel_xi_order=", walls[1].kernel_xi_order, "\n");

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
    Error("u6_1_chivir.g: window ", w.label, " did not find a settled shadow for every ",
          "charming layer -- X is not the full Q, refusing to analyze chi_vir on an ",
          "incomplete group");
  fi;
od;

results := [];;
for w in walls do
  Print("analyzing chi_vir for ", w.label, " (|X|=", Size(w.X), ")...\n");
  r := AnalyzeChiVir(w);;
  Add(results, r);
  Print("  ", w.label, ": ker_chivir_order=", r.ker_chivir_order,
        " derived_subgroup_order=", r.derived_subgroup_order,
        " index_ker_over_derived=", r.index_ker_over_derived,
        " ker_equals_derived=", r.ker_equals_derived,
        " free_crown_count_true_kervir=", r.free_crown_count_true_kervir,
        " elapsed_ms=", r.elapsed_ms, "\n");
od;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/u6_chivir_v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/probe/wac_v1/u6_1_chivir.g\",\"order\":\"裁定1108(U-6 prereg測定・[U6-1])\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/wall_crown_u6_reading_v1.md S7 [U6-1]\"",
  ",\"method_note\":\"chi_vir : Q -> (Z/N_ord)^x identified concretely as the conjugation ",
  "action of Q on its unique normal Sylow-ell subgroup T (=the C_ell translation factor of ",
  "AGL(1,ell)); ker(chi_vir) := C_Q(generator of T) (T cyclic prime order, so centralizing a ",
  "generator centralizes all of T). This is derived, not assumed: normality of the Sylow-ell ",
  "subgroup is asserted (fail-closed Error if it does not hold) rather than taken on faith. ",
  "Window construction (MakeWindow/HexagonHolds/FindFirstSettledShadow/witness permutations) ",
  "is reused verbatim from search/probe/wall_crown_census_v1/wall_crown_census_v1.g per the ",
  "task's explicit permission; the chi_vir/ker analysis itself is independent new logic.\",",
  "\"walls\":[", JoinStringsWithSeparator(List(results, ResultToJson), ","), "],",
  "\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(Runtime() - t0Global),
  "}"
);;

outPath := "search/certs/u6_1_chivir_v1_20260813.json";;
outStream := OutputTextFile(outPath, false);;
SetPrintFormattingStatus(outStream, false);;
PrintTo(outStream, cert);;
CloseStream(outStream);;
Print("\nwrote ", outPath, "\n");
Print("U6_1_CHIVIR_DONE\n");
QUIT;
