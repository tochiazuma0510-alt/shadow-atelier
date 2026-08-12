#############################################################################
## u6_3_isolated.g -- [U6-3] wall-window isolated-ness / #C(N) measurement
## (裁定1108 prereg + 裁定1112 (A)+(B) 複合設計).
##
## Background (reported to the coordinator before this script was written,
## 裁定1112 response): applying the fixture's marked-factor-map method
## (search/set_surgery_fixture_v1.g) directly to the Xi-restricted shadow
## search (kerchi-judge.g's CorrectedShadowsXi / Prop 3.1, the ONLY feasible
## enumeration method at this scale -- legacy exhaustive enumeration over
## [PN,PN]=PN=A_n is astronomically infeasible) is STRUCTURALLY TAUTOLOGICAL:
## every candidate f found by the Xi search is, BY CONSTRUCTION, produced as
## f solving f*ybar^u*f^-1 = eta(ybar) for an ACTUAL automorphism
## eta=s*alpha0 in Aut(PN)=S_n with x^eta=x^u -- i.e. genA=eta(x), genB=eta(y)
## for an explicit eta in hand. That means the pair (genA,genB) is Aut(PN)-
## equivalent to (x,y) via eta ITSELF, with no computation needed to discover
## this (it is definitionally true of every candidate the search can ever
## produce). So "(A) marked-factor-map classification of the Xi-restricted
## set" can only ever return num_classes=1 -- not because the window is
## isolated, but because the search method cannot even in principle produce
## a witness of non-isolation. This is reported honestly below (weak/
## tautological grade), per coordinator's 裁定1112 instruction.
##
## (B) partially compensates by directly probing OUTSIDE the Xi-restricted
## search space: uniformly random candidates f in PN (=[PN,PN], A_n already
## perfect) crossed with the full charming-m set, run through the ORIGINAL
## (Aut(PN)-agnostic) hexagon+generation+settled filter chain
## (CorrectedShadowsLegacy's exact filters, copied verbatim from
## kerchi-judge.g), under a wall-clock budget. A hit here would be a genuine,
## non-tautological data point (and if its genB fell outside the Xi-search's
## reach, direct evidence against Prop 3.1's completeness / against #C(N)=1).
## The analytic detection power (P[a uniformly random (m,f) candidate is a
## genuine shadow] = |GT(N)| / (|PN| * charming_m_count), using the ALREADY
## machine-computed |GT(N)| and |PN|) is computed and reported alongside the
## empirical sample, per coordinator's instruction to record detection power
## numerically rather than report a silent negative.
##
## u/c 非接触・封印非接触・prereg量非計算・NAME-COLLIDE: wall-window instances.
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;

## ---- (F2) window machinery ----
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

TT := function(W, g) return AbstractProdW([W.dlt, g, W.dlt^-1]); end;;
TH := function(W, g) return AbstractProdW([W.Dlt, g, W.Dlt^-1]); end;;
RtOf := function(W, m, f)
  local Wd;
  Wd := AbstractProdW([W.y^m, f]);
  return AbstractProdW([TT(W, TT(W, Wd)), TT(W, Wd), Wd]);
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
  return rec(label := label, n := n, ell := ell, t := t, W := W, Snn := Snn,
             ms := ms, reps := reps, all_charming_layers_represented := allFound,
             kernel_xi_order := Size(Kchi), X := X, elapsed_ms := Runtime() - elapsed);
end;;

JBool := function(b) if b then return "true"; else return "false"; fi; end;;
JStrU := function(s)
  s := ReplacedString(s, "\\", "\\\\");
  s := ReplacedString(s, "\"", "\\\"");
  return Concatenation("\"", s, "\"");
end;;

## ---- (A) tautology check: verify, for every charming m, that the Xi-search
## witness (genA,genB) is Aut(PN)-equivalent to (x,y) -- exhibiting the SAME
## eta used to construct it as the witness (RepresentativeAction is also run
## as an independent double-check that eta really works, not trusted blindly).
PartA_XiTautologyCheck := function(w)
  local W, x, y, allSameClass, mismatches, r, eta, xu, genB, witnessOk, elapsed;
  elapsed := Runtime();
  W := w.W;  x := W.x;  y := W.y;
  allSameClass := true;
  mismatches := [];
  for r in w.reps do
    eta := r.xi;
    xu := x^r.u;
    genB := y^eta;   ## = YImg(W,u,f) by construction; recomputed here via eta directly
    ## sanity: eta really achieves x->x^u (definitional, from FindFirstSettledShadow)
    if x^eta <> xu then
      Add(mismatches, rec(m := r.m, reason := "eta_does_not_map_x_to_xu"));
      allSameClass := false;
      continue;
    fi;
    ## independent re-verification via RepresentativeAction on the pair (not
    ## just trusting eta): does SOME automorphism send (x,y) to (xu,genB)?
    witnessOk := RepresentativeAction(w.Snn, [x, y], [xu, genB], OnTuples);
    if witnessOk = fail then
      Add(mismatches, rec(m := r.m, reason := "RepresentativeAction_found_no_witness"));
      allSameClass := false;
    fi;
  od;
  return rec(
    label := w.label,
    charming_m_tested := Length(w.reps),
    all_charming_layers_same_class_as_base := allSameClass,
    mismatches := mismatches,
    ## 裁定1114 (数学者・docs/notes/u63_iset4_p2_reading_v1.md 第I部): Xi is only
    ## defined on the SETTLED layer (Sol's X ~= GT^settled(N)), so this value is
    ## #C_settled, NOT a measurement of #C(N) itself -- do not report it as #C(N).
    c_settled_value := 1,
    c_settled_definition := "num classes of the Aut(PN)-diagonal-orbit marked-factor-map classification, restricted to the Xi/settled-reachable shadow candidates only -- NOT #C(N)",
    tautology_grade := "WEAK_TAUTOLOGICAL",
    elapsed_ms := Runtime() - elapsed);
end;;

## ---- (B) legacy-type random probe outside the Xi search space ----
PartB_RandomLegacyProbe := function(w, budgetSeconds)
  local W, Snn, elapsed, t0, samplesF, hitsFound, domainHits, f, m, u,
        domainOk, hexOk, genOk, wdP, wdB, hitRec, pnOrder, gtOrder,
        charmingCount, analyticProbPerCandidate, analyticExpectedHits,
        totalCandidatesConsidered, budgetMs;
  W := w.W;  Snn := w.Snn;
  elapsed := Runtime();
  t0 := Runtime();
  budgetMs := budgetSeconds * 1000;
  samplesF := 0;  hitsFound := [];  domainHits := 0;  totalCandidatesConsidered := 0;
  while Runtime() - t0 < budgetMs do
    f := PseudoRandom(W.PN);
    samplesF := samplesF + 1;
    ## domain condition (m-independent, cheapest -- test once per f)
    domainOk := (AbstractProdW([f, TH(W, f)]) = Identity(W.Bq));
    if domainOk then
      domainHits := domainHits + 1;
      for m in w.ms do
        totalCandidatesConsidered := totalCandidatesConsidered + 1;
        u := 2*m + 1;
        hexOk := (RtOf(W, m, f) = W.c^m);
        if not hexOk then continue; fi;
        genOk := (Size(Group(W.x^u, YImg(W, u, f))) = Size(W.PN));
        if not genOk then continue; fi;
        wdP := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y], [W.x^u, YImg(W, u, f)]);
        if wdP = fail then continue; fi;
        wdB := GroupHomomorphismByImages(W.Bq, W.Bq, [W.s1, W.s2],
                 [W.s1^u, f^-1 * W.s2^u * f]);
        if wdB = fail then continue; fi;
        ## genuine hit (extraordinarily unlikely per the analytic bound below)
        Add(hitsFound, rec(m := m, f_string := String(f)));
      od;
    else
      totalCandidatesConsidered := totalCandidatesConsidered + Length(w.ms);
    fi;
  od;

  pnOrder := Size(W.PN);
  gtOrder := Size(w.X);   ## = |GT(N)|, already machine-computed and cross-checked
  charmingCount := Length(w.ms);
  analyticProbPerCandidate := Float(gtOrder) / (Float(pnOrder) * Float(charmingCount));
  analyticExpectedHits := analyticProbPerCandidate * Float(totalCandidatesConsidered);

  return rec(
    label := w.label,
    budget_seconds := budgetSeconds,
    wall_time_ms := Runtime() - t0,
    samples_f_drawn := samplesF,
    domain_condition_hits := domainHits,
    total_mf_candidates_considered := totalCandidatesConsidered,
    genuine_shadow_hits_found := Length(hitsFound),
    hits := hitsFound,
    pn_order := pnOrder,
    gt_order := gtOrder,
    charming_m_count := charmingCount,
    analytic_prob_per_candidate := analyticProbPerCandidate,
    analytic_expected_hits_this_run := analyticExpectedHits,
    elapsed_ms := Runtime() - elapsed);
end;;

FloatOrNullJson := function(v)
  local s;
  s := String(v);
  if Length(s) > 0 and s[Length(s)] = '.' then s := Concatenation(s, "0"); fi;
  return s;
end;;

MismatchJson := function(m)
  return Concatenation("{\"m\":", String(m.m), ",\"reason\":", JStrU(m.reason), "}");
end;;

HitJson := function(h)
  return Concatenation("{\"m\":", String(h.m), ",\"f_perm_string\":", JStrU(h.f_string), "}");
end;;

PartAJson := function(r)
  return Concatenation(
    "{\"label\":", JStrU(r.label),
    ",\"charming_m_tested\":", String(r.charming_m_tested),
    ",\"all_charming_layers_same_class_as_base\":", JBool(r.all_charming_layers_same_class_as_base),
    ",\"mismatches\":[", JoinStringsWithSeparator(List(r.mismatches, MismatchJson), ","), "]",
    ",\"c_settled_value\":", String(r.c_settled_value),
    ",\"c_settled_definition\":", JStrU(r.c_settled_definition),
    ",\"tautology_grade\":", JStrU(r.tautology_grade),
    ",\"elapsed_ms\":", String(r.elapsed_ms), "}");
end;;

PartBJson := function(r)
  return Concatenation(
    "{\"label\":", JStrU(r.label),
    ",\"budget_seconds\":", String(r.budget_seconds),
    ",\"wall_time_ms\":", String(r.wall_time_ms),
    ",\"samples_f_drawn\":", String(r.samples_f_drawn),
    ",\"domain_condition_hits\":", String(r.domain_condition_hits),
    ",\"total_mf_candidates_considered\":", String(r.total_mf_candidates_considered),
    ",\"genuine_shadow_hits_found\":", String(r.genuine_shadow_hits_found),
    ",\"hits\":[", JoinStringsWithSeparator(List(r.hits, HitJson), ","), "]",
    ",\"pn_order\":", String(r.pn_order),
    ",\"gt_order\":", String(r.gt_order),
    ",\"charming_m_count\":", String(r.charming_m_count),
    ",\"analytic_prob_per_candidate\":", FloatOrNullJson(r.analytic_prob_per_candidate),
    ",\"analytic_expected_hits_this_run\":", FloatOrNullJson(r.analytic_expected_hits_this_run),
    ",\"elapsed_ms\":", String(r.elapsed_ms), "}");
end;;

## ---- driver ----
Print("############################################################\n");
Print("# u6_3_isolated.g -- [U6-3] isolated-ness / #C(N), (A)+(B) 裁定1112\n");
Print("############################################################\n");

if IsBound(U6_3_BUDGET_SECONDS) then
  BUDGET := U6_3_BUDGET_SECONDS;
else
  BUDGET := 20;   ## per-window random-probe wall-clock budget (seconds); override via preamble
fi;

t0Global := Runtime();;

walls := [];;
Add(walls, BuildWallQ("wall24", 24,
  (1,13)(2,9)(3,5)(4,24)(6,8)(7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23),
  (1,12,9)(2,8,5)(3,4,24)(6,7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23)));;
Print("wall24 built. |GT(N)|=", Size(walls[1].X), "\n");

Add(walls, BuildWallQ("wall28", 28,
  (1,8)(2,4)(3,24)(5,7)(6,27)(9,11)(10,25)(12,23)(13,14)(15,22)(16,18)(17,28)(19,21)(20,26),
  (1,7,4)(2,3,24)(5,6,27)(8,23,11)(9,10,25)(12,22,14)(15,21,18)(16,17,28)(19,20,26)));;
Print("wall28 built. |GT(N)|=", Size(walls[2].X), "\n");

Add(walls, BuildWallQ("wall36", 36,
  (1,3)(2,34)(4,29)(5,25)(6,16)(7,9)(8,35)(10,15)(11,12)(13,14)(17,24)(18,20)(19,32)(21,23)(22,33)(26,28)(27,36)(30,31),
  (1,2,34)(3,31,29)(4,28,25)(5,24,16)(6,15,9)(7,8,35)(10,14,12)(17,23,20)(18,19,32)(21,22,33)(26,27,36)));;
Print("wall36 built. |GT(N)|=", Size(walls[3].X), "\n");

Add(walls, BuildWallQ("wall37", 37,
  (1,30)(2,11)(3,7)(4,5)(8,10)(9,35)(12,29)(13,15)(14,32)(16,28)(17,19)(18,36)(20,27)(21,23)(22,33)(24,26)(25,37)(31,34),
  (1,29,11)(2,10,7)(3,6,5)(8,9,35)(12,28,15)(13,14,32)(16,27,19)(17,18,36)(20,26,23)(21,22,33)(24,25,37)(30,31,34)));;
Print("wall37 built. |GT(N)|=", Size(walls[4].X), "\n");

for w in walls do
  if not w.all_charming_layers_represented then
    Error("u6_3_isolated.g: window ", w.label, " did not find a settled shadow for every ",
          "charming layer -- refusing to proceed");
  fi;
od;

resultsA := [];;
resultsB := [];;
gtSettled := [];;
for w in walls do
  Print("[A] tautology check for ", w.label, "...\n");
  rA := PartA_XiTautologyCheck(w);;
  Add(resultsA, rA);
  Print("  ", w.label, ": all_charming_layers_same_class_as_base=",
        rA.all_charming_layers_same_class_as_base, " elapsed_ms=", rA.elapsed_ms, "\n");

  Print("[B] random legacy probe for ", w.label, " (budget=", BUDGET, "s)...\n");
  rB := PartB_RandomLegacyProbe(w, BUDGET);;
  Add(resultsB, rB);
  Print("  ", w.label, ": samples_f=", rB.samples_f_drawn,
        " domain_hits=", rB.domain_condition_hits,
        " candidates_considered=", rB.total_mf_candidates_considered,
        " genuine_hits=", rB.genuine_shadow_hits_found,
        " analytic_prob_per_candidate=", rB.analytic_prob_per_candidate,
        " analytic_expected_hits=", rB.analytic_expected_hits_this_run,
        " elapsed_ms=", rB.elapsed_ms, "\n");
od;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/u6_isolated_v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/probe/wac_v1/u6_3_isolated.g\",",
  "\"order\":\"裁定1108(U-6 prereg測定・[U6-3])+裁定1112((A)+(B)複合設計)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/wall_crown_u6_reading_v1.md S7 [U6-3]\"",
  ",\"method_note_a\":\"(A) marked-factor-map classification applied to the Xi-restricted ",
  "(kerchi-judge.g CorrectedShadowsXi / Prop 3.1) shadow search is STRUCTURALLY TAUTOLOGICAL: ",
  "every candidate the Xi search can produce is, by construction, (eta(x),eta(y)) for an actual ",
  "eta in Aut(PN)=S_n already in hand, so it is automatically Aut(PN)-equivalent to (x,y). ",
  "裁定1114 (数学者裁定, docs/notes/u63_iset4_p2_reading_v1.md 第I部) confirmed this circularity: ",
  "Xi is only defined on the SETTLED layer (Sol's census group X is isomorphic to GT^settled(N), ",
  "not necessarily all of GT(N)), so the value below is c_settled_value=1 -- this is #C_settled, ",
  "NOT a measurement of #C(N) itself, and is reported at WEAK_TAUTOLOGICAL grade: it certifies the ",
  "internal consistency of the Xi search (every charming-m witness really is eta(x,y) for its own ",
  "eta, re-verified here via an independent RepresentativeAction call, not just trusted), NOT that ",
  "the window is isolated -- it cannot distinguish isolated from non-isolated, by construction.\",",
  "\"method_note_b\":\"(B) probes OUTSIDE the Xi search space: uniformly random f in PN (=[PN,PN], ",
  "A_n already perfect) crossed with the full charming-m set, filtered through the ORIGINAL ",
  "(automorphism-agnostic) hexagon+generation+settled chain (CorrectedShadowsLegacy's exact ",
  "filters). A hit would be non-tautological evidence. Detection power is reported both ",
  "analytically (P[random (m,f) candidate genuine] = |GT(N)|/(|PN|*charming_m_count), using the ",
  "already machine-computed |GT(N)|=|X| and |PN|) and empirically (samples actually drawn under a ",
  "wall-clock budget). At this scale (|PN| up to |A_37|) the analytic probability is astronomically ",
  "small (see per-window analytic_prob_per_candidate) -- zero empirical hits are the EXPECTED ",
  "outcome under that analytic bound, not evidence of isolated-ness; the analytic bound itself is ",
  "the honest measure of what (B) actually establishes (near-total absence of detection power at ",
  "this scale via uniform sampling), per coordinator's 裁定1112 instruction to record detection ",
  "power numerically rather than report a silent negative.\",",
  "\"part_a_xi_tautology\":[", JoinStringsWithSeparator(List(resultsA, PartAJson), ","), "],",
  "\"part_b_random_legacy_probe\":[", JoinStringsWithSeparator(List(resultsB, PartBJson), ","), "],",
  "\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(Runtime() - t0Global),
  "}"
);;

outPath := "search/certs/u6_3_isolated_v1_20260813.json";;
outStream := OutputTextFile(outPath, false);;
SetPrintFormattingStatus(outStream, false);;
PrintTo(outStream, cert);;
CloseStream(outStream);;
Print("\nwrote ", outPath, "\n");
Print("U6_3_ISOLATED_DONE\n");
QUIT;
