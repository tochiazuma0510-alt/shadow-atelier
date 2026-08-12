#############################################################################
## wall_crown_census_v1.g -- wall-window GT/Phi maximal-class census.
##
## Universe (fixed by Sol task 114): n = 24, 28, 36, 37 only.  For every
## charming m this script finds ONE settled shadow.  It never enumerates a
## complete chi fibre: once a fibre is nonempty it is a coset of ker(chi).
## The already cross-checked wall certificates identify the Xi image of that
## kernel with C_Sn(x).  The representatives and the kernel therefore give a
## compact permutation model of the complete Xi image.
##
## The JSON contains raw group data and booleans.  It contains no arithmetic
## realizability verdict and touches no sealed/pre-registered quantity.
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;
JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");;

JBool := function(b)
  if b then return "true"; else return "false"; fi;
end;;
JStr := function(s)
  s := ReplacedString(s, "\\", "\\\\");
  s := ReplacedString(s, "\"", "\\\"");
  s := ReplacedString(s, "\n", "\\n");
  return Concatenation("\"", s, "\"");
end;;
JIntList := l -> Concatenation("[", JoinStringsWithSeparator(List(l, String), ","), "]");;

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

## Corrected literal orientation from wall_canary_24_20260801.g:
## h^-1*y^u*h=target and f=c*h with c in C_P(y^u).
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
                 f := f, xi := xi,
                 xi_maps_x := (W.x^xi = W.x^u),
                 xi_maps_y := (W.y^xi = YImg(W, u, f)),
                 p_hom_is_surjective := true,
                 bq_hom_is_defined := true);
    od;
  od;
  return rec(found := false, m := m, u := u, scanned := scanned,
             reason := "candidate_space_exhausted");
end;;

PrimitiveRow := function(G, cl)
  local M, core, hom, Q, soc, id;
  M := Representative(cl);
  core := Core(G, M);
  hom := NaturalHomomorphismByNormalSubgroup(G, core);
  Q := Image(hom);
  soc := Socle(Q);
  id := fail;
  if Size(Q) <= 2000 then
    id := IdGroup(Q);
  fi;
  return rec(
    index := Index(G, M),
    class_size := Size(cl),
    maximal_is_normal := IsNormal(G, M),
    maximal_order := Size(M),
    maximal_structure := StructureDescription(M),
    core_order := Size(core),
    primitive_order := Size(Q),
    primitive_structure := StructureDescription(Q),
    primitive_id := id,
    socle_order := Size(soc),
    socle_structure := StructureDescription(soc),
    crown_abelian := IsAbelian(soc));
end;;

CensusGroup := function(G)
  local phi, nat, Q, classes, rows;
  phi := FrattiniSubgroup(G);
  nat := NaturalHomomorphismByNormalSubgroup(G, phi);
  Q := Image(nat);
  classes := ConjugacyClassesMaximalSubgroups(Q);
  rows := List(classes, cl -> PrimitiveRow(Q, cl));
  return rec(
    group_order := Size(G),
    group_structure := StructureDescription(G),
    frattini_order := Size(phi),
    quotient_order := Size(Q),
    quotient_structure := StructureDescription(Q),
    maximal_class_count := Length(rows),
    abelian_crown_count := Number(rows, r -> r.crown_abelian),
    nonabelian_crown_count := Number(rows, r -> not r.crown_abelian),
    rows := rows);
end;;

RowJson := function(r)
  local idjson;
  if r.primitive_id = fail then
    idjson := "null";
  else
    idjson := JIntList(r.primitive_id);
  fi;
  return Concatenation(
    "{\"index\":", String(r.index),
    ",\"class_size\":", String(r.class_size),
    ",\"maximal_is_normal\":", JBool(r.maximal_is_normal),
    ",\"maximal_order\":", String(r.maximal_order),
    ",\"maximal_structure\":", JStr(r.maximal_structure),
    ",\"core_order\":", String(r.core_order),
    ",\"primitive_order\":", String(r.primitive_order),
    ",\"primitive_structure\":", JStr(r.primitive_structure),
    ",\"primitive_id\":", idjson,
    ",\"socle_order\":", String(r.socle_order),
    ",\"socle_structure\":", JStr(r.socle_structure),
    ",\"crown_abelian\":", JBool(r.crown_abelian), "}");
end;;

CensusJson := function(c)
  return Concatenation(
    "{\"group_order\":", String(c.group_order),
    ",\"group_structure\":", JStr(c.group_structure),
    ",\"frattini_order\":", String(c.frattini_order),
    ",\"quotient_order\":", String(c.quotient_order),
    ",\"quotient_structure\":", JStr(c.quotient_structure),
    ",\"maximal_class_count\":", String(c.maximal_class_count),
    ",\"abelian_crown_count\":", String(c.abelian_crown_count),
    ",\"nonabelian_crown_count\":", String(c.nonabelian_crown_count),
    ",\"classes\":[",
    JoinStringsWithSeparator(List(c.rows, RowJson), ","), "]}");
end;;

ShadowJson := function(r)
  if not r.found then
    return Concatenation("{\"m\":", String(r.m), ",\"u\":", String(r.u),
      ",\"found\":false,\"scanned\":", String(r.scanned),
      ",\"reason\":", JStr(r.reason), "}");
  fi;
  return Concatenation("{\"m\":", String(r.m), ",\"u\":", String(r.u),
    ",\"found\":true,\"scanned\":", String(r.scanned),
    ",\"xi\":", JStr(String(r.xi)),
    ",\"f\":", JStr(String(r.f)),
    ",\"xi_maps_x\":", JBool(r.xi_maps_x),
    ",\"xi_maps_y\":", JBool(r.xi_maps_y),
    ",\"p_hom_is_surjective\":", JBool(r.p_hom_is_surjective),
    ",\"bq_hom_is_defined\":", JBool(r.bq_hom_is_defined), "}");
end;;

RunWall := function(label, n, a1, b1, kernelCert)
  local Snn, Ann, aE, bE, s1, s2, W, ell, t, Kchi, stabElts,
        cyuElts, ms, reps, allFound, X, normalizer, census, elapsed;
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
    Print(label, ": searching m=", m, " u=", 2*m+1, "\n");
    Add(reps, FindFirstSettledShadow(W, m, Snn, stabElts, cyuElts));
    Print(label, ": m=", m, " found=", reps[Length(reps)].found,
          " scanned=", reps[Length(reps)].scanned, "\n");
  od;
  allFound := ForAll(reps, r -> r.found);
  if allFound then
    X := Group(Concatenation(GeneratorsOfGroup(Kchi), List(reps, r -> r.xi)));
  else
    X := Kchi;
  fi;
  normalizer := Normalizer(Snn, Group(W.x));
  census := CensusGroup(X);
  return rec(
    label := label, n := n, ell := ell, t := t,
    kernel_cert := kernelCert,
    pn_order := Size(W.PN),
    charming_m_count := Length(ms),
    settled_representatives_found := Number(reps, r -> r.found),
    all_charming_layers_represented := allFound,
    kernel_xi_order := Size(Kchi),
    kernel_xi_structure := StructureDescription(Kchi),
    xi_image_order := Size(X),
    normalizer_order := Size(normalizer),
    xi_image_equals_normalizer := (X = normalizer),
    normalizer_structure := StructureDescription(normalizer),
    representatives := reps,
    census := census,
    elapsed_ms := Runtime() - elapsed);
end;;

WallJson := function(w)
  return Concatenation(
    "{\"label\":", JStr(w.label),
    ",\"n\":", String(w.n), ",\"ell\":", String(w.ell),
    ",\"t\":", String(w.t),
    ",\"kernel_cert\":", JStr(w.kernel_cert),
    ",\"pn_order\":", String(w.pn_order),
    ",\"charming_m_count\":", String(w.charming_m_count),
    ",\"settled_representatives_found\":", String(w.settled_representatives_found),
    ",\"all_charming_layers_represented\":", JBool(w.all_charming_layers_represented),
    ",\"kernel_xi_order\":", String(w.kernel_xi_order),
    ",\"kernel_xi_structure\":", JStr(w.kernel_xi_structure),
    ",\"xi_image_order\":", String(w.xi_image_order),
    ",\"normalizer_order\":", String(w.normalizer_order),
    ",\"xi_image_equals_normalizer\":", JBool(w.xi_image_equals_normalizer),
    ",\"normalizer_structure\":", JStr(w.normalizer_structure),
    ",\"representatives\":[",
    JoinStringsWithSeparator(List(w.representatives, ShadowJson), ","), "],",
    "\"census\":", CensusJson(w.census),
    ",\"elapsed_ms\":", String(w.elapsed_ms), "}");
end;;

## Witnesses are copied literally from the four versioned wall drivers.
walls := [];;
if not IsBound(WALL_ONLY) or WALL_ONLY = "wall24" then
Add(walls, RunWall("wall24", 24,
  (1,13)(2,9)(3,5)(4,24)(6,8)(7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23),
  (1,12,9)(2,8,5)(3,4,24)(6,7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23),
  "search/certs/wall2_cert_judge_20260731.json"));;
fi;
if not IsBound(WALL_ONLY) or WALL_ONLY = "wall28" then
Add(walls, RunWall("wall28", 28,
  (1,8)(2,4)(3,24)(5,7)(6,27)(9,11)(10,25)(12,23)(13,14)(15,22)(16,18)(17,28)(19,21)(20,26),
  (1,7,4)(2,3,24)(5,6,27)(8,23,11)(9,10,25)(12,22,14)(15,21,18)(16,17,28)(19,20,26),
  "search/certs/wall28_cert_20260731.json"));;
fi;
if not IsBound(WALL_ONLY) or WALL_ONLY = "wall36" then
Add(walls, RunWall("wall36", 36,
  (1,3)(2,34)(4,29)(5,25)(6,16)(7,9)(8,35)(10,15)(11,12)(13,14)(17,24)(18,20)(19,32)(21,23)(22,33)(26,28)(27,36)(30,31),
  (1,2,34)(3,31,29)(4,28,25)(5,24,16)(6,15,9)(7,8,35)(10,14,12)(17,23,20)(18,19,32)(21,22,33)(26,27,36),
  "search/certs/wall36_cert_20260731_r2.json"));;
fi;
if not IsBound(WALL_ONLY) or WALL_ONLY = "wall37" then
Add(walls, RunWall("wall37", 37,
  (1,30)(2,11)(3,7)(4,5)(8,10)(9,35)(12,29)(13,15)(14,32)(16,28)(17,19)(18,36)(20,27)(21,23)(22,33)(24,26)(25,37)(31,34),
  (1,29,11)(2,10,7)(3,6,5)(8,9,35)(12,28,15)(13,14,32)(16,27,19)(17,18,36)(20,26,23)(21,22,33)(24,25,37)(30,31,34),
  "search/certs/wall37_cert_20260731_r2.json"));;
fi;

controls := [
  rec(label := "K9", small_group_id := [36,12], census := CensusGroup(SmallGroup(36,12))),
  rec(label := "roof972", small_group_id := [108,43], census := CensusGroup(SmallGroup(108,43)))
];;
ControlJson := c -> Concatenation(
  "{\"label\":", JStr(c.label),
  ",\"small_group_id\":", JIntList(c.small_group_id),
  ",\"census\":", CensusJson(c.census), "}");;

out := Concatenation(
  "{\n",
  "\"schema\":\"wall-crown-census/v1\",\n",
  "\"generated_by\":\"search/probe/wall_crown_census_v1/wall_crown_census_v1.g\",\n",
  "\"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "\"universe\":\"wall-window instances n=24,28,36,37 only\",\n",
  "\"method\":\"one settled representative per nonempty chi fibre; kernel-coset reconstruction; Xi permutation image; maximal classes of Xi/Phi\",\n",
  "\"quarantine\":{\"K9\":\"group-theory positive control only\",\"K5\":\"not accessed\",\"name_collide\":\"wall-window instance\",\"u_c\":\"not accessed\"},\n",
  "\"positive_controls\":[", JoinStringsWithSeparator(List(controls, ControlJson), ","), "],\n",
  "\"walls\":[", JoinStringsWithSeparator(List(walls, WallJson), ","), "]\n",
  "}\n");;
if IsBound(WALL_ONLY) then
  outName := Concatenation("search/certs/wall_crown_census_v1_", WALL_ONLY,
                           "_20260812.json");
else
  outName := "search/certs/wall_crown_census_v1_20260812.json";
fi;
PrintTo(outName, out);;
Print("WALL_CROWN_CENSUS_V1_DONE\n");
QUIT;
