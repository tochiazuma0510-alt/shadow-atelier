#############################################################################
## search/kerchi-judge.g -- kerchi-judge v1.3 (version numbering unified per
## 裁定171: what was internally v1.2 -- the 裁定170 settled-certificate /
## chi_image_order / N5cong-rename pass -- is renumbered v1.3's predecessor;
## the mathematician's blocker report had only seen v1.1. 裁定167 原型・
## 裁定169 KJ-1 修理・裁定171 命題3.1 Xi-restriction 速達修理)
##
## v1.3 (裁定171・速達 blocker, 2026-07-29, spec: docs/notes/
## wac_reverse_design_v1.md S3.4 命題3.1): CorrectedShadows's
## "for f in Elements(DerivedSubgroup(P))" loop is infeasible for
## non-solvable P with |[P,P]| ~ 10^13 (window W-D-A16-11a: |[P,P]|=|A16|).
## Added CorrectedShadowsXi (the Prop 3.1 Xi-restricted scan: f ranges over
## C_P(ybar^u)-cosets of Stab_{Aut(P)}(xbar)-indexed representatives, NOT
## all of [P,P]) alongside the renamed CorrectedShadowsLegacy (unchanged
## exhaustive path), auto-selected by a CorrectedShadows dispatcher on
## |[P,P]|*|charmingSet| vs JUDGE_SCAN_THRESHOLD (overridable via
## JUDGE_FORCE_SCAN_MODE := "legacy" / "xi_restricted"). New output fields:
## scan_mode, scanned_count, legacy_candidate_count, compression. See
## search/kerchi-judge-v13-calibration.g for the required regression
## calibration (D1 p=5,7 congruence windows + N5cong: both scan modes must
## give IDENTICAL shadow sets, forced via JUDGE_FORCE_SCAN_MODE on each side).
##
## Packages the (F2) quotient-rule machinery (proven out on 17 real windows in
## search/wall-miner-v4.g, itself lifted from the coordinator-cross-checked
## search/wcp5d-verify.g / docs/notes/wcp5d_resolution_v1.md) into a single
## reusable script: given ONE window (however specified), decide whether
## ker(chi-tilde) (the m=0 layer of G_N=GTSh(N,N)) is ABELIAN or NONABELIAN,
## with every intermediate assert reported, fail-closed.
##
## v1.1 (KJ-1, 裁定169, 2026-07-29): added a settled/well-definedness clause
## to the (F2) predicate. Window W-A-B3idx126-s2 was found (while testing
## v1) to satisfy all three original (F2) conditions for a candidate that is
## NOT actually well-defined as a homomorphism (GroupHomomorphismByImages
## genuinely fails on it) -- so v1's shadow set could silently include
## ill-defined "shadows". The fix: for every candidate that passes the
## original three conditions, additionally require
##   GroupHomomorphismByImages(Bq, Bq, [s1,s2], [s1^u, f^-1*s2^u*f]) <> fail
## at the Bq=B3/N level (the same level theta~/tau~ already live on), not at
## the P_N level. Candidates failing this are dropped and counted in the new
## settled_fail_count output field. See search/kerchi-judge-v11-regression.g
## for the regression check against v1's/wall-miner-v4.g's recorded numbers.
##
## Policy unchanged throughout this campaign: rough is fine, no polish
## required, but the asserts stay -- this script's entire point is to be an
## honest judge, not a lead-generator. NOT a ledger claim by itself (it is
## infrastructure a ledger claim could later cite, together with an
## independent cross-check -- this script alone is still a single GAP
## implementation, not a two-system cross-check). No commit. No u (sealed
## symbol) anywhere.
##
## ---------------------------------------------------------------------
## INPUT (bind ONE of these two ways before Read()-ing this file):
##
##   (a) LINS node lookup (same window-id convention as wall-miner-v2/v3/v4):
##         JUDGE_INDEX_BOUND := 192;;              # LINS index bound (B3-index)
##         JUDGE_WINDOW_ID   := "W-A-B3idx144-s5";; # "W-A-B3idx<idx>-s<serial>"
##       (serial = the k-th LINS node found at that B3-index, in the same
##       iteration order used throughout this campaign: N normal in B3,
##       N <= PB3, idx > 1, ordered as ComputedNormalSubgroups(gr) yields them)
##
##   (b) Direct generator images (for congruence windows, WA-c reverse-design
##       windows, or anything not reachable via LINS/index alone) -- bind
##       permutations OR matrices satisfying the braid relation:
##         JUDGE_S1_IMG := <perm or matrix>;;   # image of sigma_1
##         JUDGE_S2_IMG := <perm or matrix>;;   # image of sigma_2
##         JUDGE_ID     := "my-window-label";;  # optional, for the outfile name
##       (matrices are auto-converted to a permutation representation via
##       IsomorphismPermGroup; if that conversion is not possible this fails
##       closed with an Error, it does not silently degrade)
##
##   Optional in both modes:
##         JUDGE_OUTFILE := "search/certs/kerchi_judge_myrun.json";;
##       (default: search/certs/kerchi_judge_<id>.json, id = JUDGE_WINDOW_ID
##       in mode (a) or JUDGE_ID (default "direct") in mode (b))
##
##   Self-test mode (no window input needed -- runs the two smoke fixtures
##   described below and asserts their known answers):
##         JUDGE_SELFTEST := true;;
##
## ---------------------------------------------------------------------
## CI USAGE EXAMPLE (.github/workflows/gap-run.yml "preamble" input, a
## semicolon-terminated GAP statement blob bound before Read(script)):
##
##   script:   search/kerchi-judge.g
##   preamble: JUDGE_INDEX_BOUND:=192;; JUDGE_WINDOW_ID:="W-A-B3idx144-s5";;
##   out_dir:  search/certs
##
##   -- or, for a congruence window built from explicit matrices (example:
##      N5cong (written N5^cong; renamed 裁定170 from "N5" to avoid collision with
##      week1-定義ノート.md's own N5 = ker(beta_5)) = ker(B3 -> S3 x SL(2,F5)),
##      same construction as wall-miner-v1/v4):
##
##   preamble: JUDGE_S1_IMG:=Image(Embedding(DirectProduct(
##               Image(IsomorphismPermGroup(Group([[1,1],[0,1]]*One(GF(2)),
##                 [[1,0],[1,1]]*One(GF(2))))),
##               Image(IsomorphismPermGroup(Group([[1,1],[0,1]]*One(GF(5)),
##                 [[1,0],[4,1]]*One(GF(5)))))),1),
##               Image(IsomorphismPermGroup(Group([[1,1],[0,1]]*One(GF(2)),
##                 [[1,0],[1,1]]*One(GF(2)))),[[1,1],[0,1]]*One(GF(2))))
##               * ... (see search/wall-miner-v1.g N5 construction for the
##               full expression; in practice it is easier to write a tiny
##               wrapper .g file that builds JUDGE_S1_IMG/JUDGE_S2_IMG with
##               ordinary multi-line GAP and then Read()s this file, rather
##               than inlining a one-line preamble for matrix windows)
##   JUDGE_ID: "N5cong-SL2F5"
##
##   -- or, for the self-test:
##
##   preamble: JUDGE_SELFTEST:=true;;
##
## ---------------------------------------------------------------------
## OUTPUT: JUDGE_OUTFILE, a JSON record with fields:
##   verdict (one of "ABELIAN" | "NONABELIAN" | "UNSCREENED"), c_in_N,
##   abs_Bq, abs_PN, N_ord, charming_count, shadow_total,
##   settled_fail_count / settled_total_evaluated / settled_all_pass /
##   settled_fail_witnesses (裁定170: per-candidate settled certificate --
##   settled_all_pass=true and settled_fail_count=0 together mean
##   "shadow_total/shadow_total settled", i.e. every hexagon-candidate that
##   passed the three original (F2) conditions was ALSO well-defined;
##   settled_fail_witnesses lists up to 20 of the rejected (m,f) candidates),
##   isotropy_order (= |G_N| = |GTSh(N,N)|), ker_size, chi_image_order
##   (= |Im chi~|, computed directly from the realized shadow set, NOT
##   assumed equal to phi_2Nord), phi_2Nord, ta_predicted_ker (legacy,
##   assumed-surjective reading), ta_assert_holds (裁定170: UNIVERSAL form
##   |ker chi~| * |Im chi~| = |G_N|, always meaningful once (3.53) closes),
##   chi_surjective_assert (null unless c_in_N -- see the code comment on why
##   c_in_N is used as a documented proxy for "isolated相当" rather than a
##   genuine isolated-ness check), closure_353_holds, ker_commutes, witness
##   (null unless NONABELIAN), derived_series_orders, derived_length (or -1
##   if not solvable), crosscheck_vs_EnumerateReducedHexagon (null unless
##   c_in_N; for c_in_N windows this cross-checks the (F2) shadow set against
##   the pre-existing quotient-shortcut enumerator in week3-battery-common.g,
##   which is valid precisely when c_in_N -- see that file's own comments).
#############################################################################

Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");   # AbstractProd, PF, EnumerateReducedHexagon
                                          # (the last one used ONLY for the c_in_N
                                          # crosscheck assert -- see WARNING comments
                                          # added to the word-level c_notin_N
                                          # enumerators in that same file, ruling 166)

#############################################################################
## ---------------------- (F2) machinery (from wall-miner-v4.g) --------------
#############################################################################
MakeWindow := function(s1, s2)
  local xx, yy, DD, dd, cc, zz;
  xx := s1^2;  yy := s2^2;
  DD := AbstractProd([s1, s2, s1]);  dd := AbstractProd([s1, s2]);
  cc := DD^2;  zz := AbstractProd([xx, yy])^-1;
  return rec(s1 := s1, s2 := s2, x := xx, y := yy, Dlt := DD, dlt := dd, c := cc, z := zz,
             Bq := Group(s1, s2), PN := Group(xx, yy),
             Nord := Lcm(Order(xx), Order(yy), Order(cc)));
end;;

TT := function(W, g) return AbstractProd([W.dlt, g, W.dlt^-1]); end;;
TH := function(W, g) return AbstractProd([W.Dlt, g, W.Dlt^-1]); end;;
RtOf := function(W, m, f)
  local Wd;
  Wd := AbstractProd([W.y^m, f]);
  return AbstractProd([TT(W, TT(W, Wd)), TT(W, Wd), Wd]);
end;;

# *** KJ-1 FIX (裁定169, 2026-07-29): settled/well-definedness clause added ***
# docs/notes/ (KJ-1 audit, 札B): the three original (F2) conditions (f*theta~(f)=1,
# Rt=c^m, generation) do NOT by themselves guarantee that T_{m,f} (x->x^u,
# y->f^-1 y^u f) is an actual well-defined homomorphism -- window
# W-A-B3idx126-s2 is a concrete counterexample found while testing
# kerchi-judge v1 (m=2, f=identity there: all three old conditions passed,
## but GroupHomomorphismByImages on P_N genuinely failed). The fix is to test
# well-definedness explicitly, and to do it at the Bq=B3/N level (same
# ambient group theta~/tau~ already live in), not at the P_N level -- per the
# coordinator's ruling 169. A candidate that fails this settled check is
# dropped (not added to the shadow set), and counted in settled_fail_count.
# Return shape changed from v1 (a bare Set) to v1.1 (a record) precisely so
# this count can be reported without a second global/side-channel.
# v1.2 (裁定170・Sol F79-5.5/F79-2.1, 2026-07-29): per-candidate settled certificate.
# CorrectedShadows now also tracks EVERY candidate that passed the three original
# (F2) conditions (the "hexagon-candidate" set, before the settled filter), so
# that "N/N settled" can be reported honestly (e.g. W-C-N5cong's known 40
# candidates). Rather than dumping every candidate's settled=true trivially
# (which would bloat the certificate for windows with hundreds of candidates,
# e.g. W-C-N5cong has 960), only the FAILING candidates are kept as an explicit
# witness list (settled_fail_witnesses); the passing count is inferred from
# Length(shadows) (all of which are settled=true by construction) and the total
# hexagon-candidate count is Length(shadows) + settled_fail_count -- so
# "40/40 settled" is exactly the statement settled_fail_count = 0 with
# shadow_total = 40, reported without needing to enumerate 40 trivial passes.
# v1.3 (裁定171・速達blocker・docs/notes/wac_reverse_design_v1.md S3.4 命題3.1,
# 2026-07-29): this is now the SLOW/EXHAUSTIVE path only (renamed from
# "CorrectedShadows" to "CorrectedShadowsLegacy"). It literally calls
# Elements(DerivedSubgroup(W.PN)), which is infeasible for non-solvable P
# with |[P,P]| in the 10^13 range (W-D-A16-11a: |[P,P]|=|A16|~1.05e13 --
# "Elements の時点でメモリ死"). Kept verbatim (unchanged logic) as the
# ground-truth path for small/solvable-or-tractable P, and as the regression
# baseline that CorrectedShadowsXi below is calibrated against.
CorrectedShadowsLegacy := function(W, charmingSet)
  local out, f, m, u, settledFails, settledHom, failWitnesses;
  out := [];  settledFails := 0;  failWitnesses := [];
  for f in Elements(DerivedSubgroup(W.PN)) do
    if AbstractProd([f, TH(W, f)]) <> Identity(W.Bq) then continue; fi;
    for m in charmingSet do
      u := 2*m + 1;
      if RtOf(W, m, f) <> W.c^m then continue; fi;
      if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN) then continue; fi;
      # settled/well-definedness clause (Bq level, per ruling 169):
      settledHom := GroupHomomorphismByImages(W.Bq, W.Bq, [W.s1, W.s2],
                      [W.s1^u, AbstractProd([f^-1, W.s2^u, f])]);
      if settledHom = fail then
        settledFails := settledFails + 1;
        if Length(failWitnesses) < 20 then   # cap the witness list, not the count
          Add(failWitnesses, rec(m := m, f := f));
        fi;
        continue;
      fi;
      Add(out, [m, f]);
    od;
  od;
  return rec(shadows := Set(out), settled_fail_count := settledFails,
             settled_fail_witnesses := failWitnesses, scanned_count := -1);
             # scanned_count filled in by the CorrectedShadows dispatcher below
             # (legacy scan budget = |[P,P]| * |charmingSet|, computed there)
end;;

# v1.3 【修理仕様】命題3.1 (Xi-restriction), per docs/notes/wac_reverse_design_v1.md
# S3.4 exactly (the 4 numbered items there are the normative spec; this
# implementation follows them literally, not an independent re-derivation):
#   1. Replace "for f in Elements(DerivedSubgroup(P))" with a per-m loop that
#      constructs the candidate set C_m directly (below), instead of filtering
#      the whole derived subgroup.
#   2. Construct A_m WITHOUT building all of Aut(P): find one alpha0 in
#      Aut(P) with alpha0(xbar) = xbar^u via RepresentativeAction (this is
#      the general-purpose GAP analogue of "P=A_n の場合は S_n 内の共役元探索
#      で足りる" -- RepresentativeAction on AutomorphismGroup(P) does exactly
#      that search, not restricted to the A_n case specifically, since the
#      spec's A_n remark is given as an implementation NOTE about how cheap
#      that search is for A_n, not a restriction on which P this applies to).
#      A_m = alpha0 . Stab(xbar) (a coset of the once-per-window-computed
#      Stab_{Aut(P)}(xbar)).
#   3. For each alpha = alpha0∘s (s ranging over Stab), find f0 with
#      f0 * ybar^u * f0^-1 = alpha(ybar). This is computed as f0 := h^-1 where
#      h := RepresentativeAction(P, ybar^u, alpha(ybar), OnPoints) (GAP's
#      STANDARD pt^g=g^-1*pt*g action) -- i.e. h solves (ybar^u)^h=alpha(ybar)
#      the ordinary way, then f0=h^-1 solves f0*ybar^u*f0^-1=alpha(ybar).
#      IMPORTANT (found during calibration, 2026-07-29): calling
#      RepresentativeAction directly with a hand-written REVERSED action
#      function (pt,g)->g*pt*g^-1 instead of this h/inverse trick looked
#      plausible and sometimes returned a "solution", but that solution did
#      NOT always actually satisfy the requested equation (verified by direct
#      substitution) -- i.e. RepresentativeAction with a non-standard custom
#      action is not reliable here. Using GAP's own OnPoints (its
#      best-supported, most heavily optimized action) and inverting the
#      result algebraically is the robust fix, and is what is implemented
#      below. This codebase's settled/hexagon formulas are all written via
#      AbstractProd([f^-1, w, f]), which (per week3-battery-common.g's own
#      "reversal convention" comment on AbstractProd, and gaplib_common.g
#      trap (1)) actually EVALUATES to f*w*f^-1, not literally f^-1*w*f --
#      an inconsistency discovered and fixed here (2026-07-29) while
#      calibrating against CorrectedShadowsLegacy on the D1 p=5 fixture: an
#      earlier draft of this function used the literal (non-reversed)
#      f^-1*w*f convention and silently found only 1/5 of the true m=0 shadow
#      layer for that fixture (isotropy_order 8 instead of 40) -- caught
#      precisely by the required regression calibration, not left unnoticed.
#      f then ranges over f0 . C_P(ybar^u) (a RIGHT coset of the centralizer,
#      since (f0*c)*ybar^u*(f0*c)^-1 = f0*c*ybar^u*c^-1*f0^-1 =
#      f0*ybar^u*f0^-1 = alpha(ybar) exactly when c centralizes ybar^u). The
#      f in [P,P] test ("最後に置く" per the spec) is applied first among the
#      post-generation filters purely for cost ordering (cheapest test
#      first); mathematically it is still just one more filter, same as the
#      original three (F2) conditions and the settled clause, ALL of which
#      are still checked per-candidate exactly as in CorrectedShadowsLegacy
#      (the Xi-restriction narrows WHERE f is searched, it does not weaken or
#      replace any acceptance criterion).
#   4. Fail-closed budget check: the theoretical per-m bound
#      |Stab(xbar)| * |C_P(ybar^u)| is accumulated into
#      theoretical_upper_bound_xi (summed over charming m) and compared
#      against the actual scanned_count; Error() if scanned_count ever
#      exceeds it (should be structurally impossible given the loop nesting
#      below, but kept as an explicit assert per the spec, not silently
#      trusted).
# UNKNOWN / not invented here: the spec does not say what to do if
# RepresentativeAction fails to find alpha0 or f0 for some m/s (only that
# "A_m は空か... の剰余類" -- i.e. it MAY be empty). This implementation
# treats that as "zero candidates from this (m) or (m,s) branch, move on" --
# the natural reading, but it is an implementation choice where the spec
# itself is silent, not a claim that the spec forced this exact behavior.
CorrectedShadowsXi := function(W, charmingSet)
  local out, settledFails, failWitnesses, D, AutP, actFun, Stab, stabElts,
        m, u, alpha0, yu, Cyu, cElts, s, target, hRep, f0, c, f, scannedCount,
        theoreticalBound, settledHom, fastAutN;
  out := [];  settledFails := 0;  failWitnesses := [];  scannedCount := 0;
  theoreticalBound := 0;
  D := DerivedSubgroup(W.PN);

  # PERFORMANCE fast-path (裁定181・strike-a16 prep, 2026-07-29): for P = A_n
  # (n<>6), Aut(P) = S_n acting by ordinary conjugation -- this is explicitly
  # noted in docs/notes/wac_reverse_design_v1.md S3.4 item 2 ("P=A_n なら S_n
  # 内の共役元探索で足りる"). Using the GENERIC AutomorphismGroup(P) +
  # Stabilizer(AutP, xbar, actFun) path for W-D-A16-11a (|Aut(P)|=16!~2e13)
  # was found, while timing this window for the strike driver, to not
  # complete Stabilizer() even after 90+ seconds. Two separate performance
  # traps were found and fixed here, not just one:
  #  (a) AutomorphismGroup(P) itself returns instantly (GAP recognizes A_n
  #      and returns S_n's structure cheaply), but Stabilizer/
  #      RepresentativeAction called on that abstract automorphism-group
  #      OBJECT (even with a mathematically-correct custom action function)
  #      does not get GAP's fast permutation-conjugacy algorithms.
  #  (b) Even after switching AutP to a genuine permutation group
  #      (Sym(support)) with actFun(pt,g):=pt^g (ordinary conjugation),
  #      calling the GENERIC Stabilizer(AutP,xbar,actFun) /
  #      RepresentativeAction(AutP,xbar,xbar^u,actFun) 4-argument forms
  #      (custom action function supplied) was STILL too slow (still not
  #      done after 60+ seconds) -- GAP's fast conjugacy-class algorithms are
  #      only reliably invoked via the DEDICATED Centralizer(G,pt) /
  #      RepresentativeAction(G,d,e) forms (no custom action function; GAP
  #      then recognizes this is ordinary permutation conjugation and uses
  #      its optimized centralizer/conjugacy machinery), which is what is
  #      actually used below for the fastAutN branch -- confirmed instant
  #      (0ms) on W-D-A16-11a. This was NOT part of the calibration in
  #      search/kerchi-judge-v13-calibration.g (whose P's are SL(2,5)/
  #      SL(2,7), not alternating), so it does not touch that already-
  #      calibrated path (fastAutN = false there, generic branch unchanged).
  fastAutN := IsNaturalAlternatingGroup(W.PN) and NrMovedPoints(W.PN) <> 6;
  if fastAutN then
    AutP := SymmetricGroup(MovedPoints(W.PN));
    Stab := Centralizer(AutP, W.x);
  else
    AutP := AutomorphismGroup(W.PN);
    actFun := function(pt, g) return Image(g, pt); end;
    Stab := Stabilizer(AutP, W.x, actFun);
  fi;
  stabElts := Elements(Stab);   # |Stab(xbar)| -- expected small (e.g. 1320 for A16-11a)

  for m in charmingSet do
    u := 2*m + 1;
    Print("  [Xi] m=", m, " (u=", u, ") starting...\n");
    yu := W.y^u;
    Cyu := Centralizer(W.PN, yu);
    cElts := Elements(Cyu);     # |C_P(ybar^u)| -- expected small (e.g. 660 for A16-11a)
    theoreticalBound := theoreticalBound + Length(stabElts) * Length(cElts);

    if fastAutN then
      alpha0 := RepresentativeAction(AutP, W.x, W.x^u);   # dedicated conjugacy search, no action fn
    else
      alpha0 := RepresentativeAction(AutP, W.x, W.x^u, actFun);
    fi;
    if alpha0 = fail then
      Print("  [Xi] m=", m, ": A_m empty (alpha0 not found), 0 candidates, next m\n");
      continue;   # A_m empty for this m -- no candidates, per Prop 3.1
    fi;

    for s in stabElts do
      # alpha(ybar), alpha = alpha0 composed with s ("s first, then alpha0"):
      # fastAutN uses GAP's right-action convention pt^(g1*g2)=(pt^g1)^g2, so
      # "s first, then alpha0" is the product s*alpha0, NOT alpha0*s.
      if fastAutN then
        target := W.y ^ (s * alpha0);
      else
        target := Image(alpha0, Image(s, W.y));
      fi;
      # solve f0 * yu * f0^-1 = target via GAP's standard OnPoints action
      # (pt^g = g^-1*pt*g) applied to h with (yu)^h = target, then f0 := h^-1:
      hRep := RepresentativeAction(W.PN, yu, target, OnPoints);
      if hRep = fail then
        continue;   # this alpha contributes no f -- move to the next s
      fi;
      f0 := hRep^-1;
      for c in cElts do
        f := f0 * c;
        scannedCount := scannedCount + 1;
        if scannedCount > theoreticalBound then
          Error("kerchi-judge CorrectedShadowsXi: scanned_count exceeded the ",
                "theoretical Prop-3.1 upper bound -- this should be structurally ",
                "impossible given the loop nesting; fail-closed per the coordinator's ",
                "instruction rather than silently continuing");
        fi;
        if not (f in D) then continue; fi;   # [P,P] membership, checked first (cheapest)
        if AbstractProd([f, TH(W, f)]) <> Identity(W.Bq) then continue; fi;
        if RtOf(W, m, f) <> W.c^m then continue; fi;
        if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN) then continue; fi;
        settledHom := GroupHomomorphismByImages(W.Bq, W.Bq, [W.s1, W.s2],
                        [W.s1^u, AbstractProd([f^-1, W.s2^u, f])]);
        if settledHom = fail then
          settledFails := settledFails + 1;
          if Length(failWitnesses) < 20 then
            Add(failWitnesses, rec(m := m, f := f));
          fi;
          continue;
        fi;
        Add(out, [m, f]);
      od;
    od;
    Print("  [Xi] m=", m, " done. scanned_so_far=", scannedCount,
          " shadows_so_far=", Length(out), " settled_fail_so_far=", settledFails, "\n");
  od;
  return rec(shadows := Set(out), settled_fail_count := settledFails,
             settled_fail_witnesses := failWitnesses, scanned_count := scannedCount,
             theoretical_upper_bound_xi := theoreticalBound);
end;;

# v1.3 dispatcher: chooses legacy (exhaustive, ground truth) vs xi_restricted
# (Prop 3.1, for P too large to enumerate), auto-selected by |[P,P]|*|charmingSet|
# against JUDGE_SCAN_THRESHOLD, or forced via JUDGE_FORCE_SCAN_MODE (legacy
# strings "legacy" / "xi_restricted"). NOTE: the threshold VALUE below is an
# ENGINEERING choice (how large a GAP Elements() call is comfortable to run),
# not a mathematical spec point -- docs/notes/wac_reverse_design_v1.md does
# not fix one, so this is not "invented math", just a practical cutoff,
# clearly labeled as such and open to recalibration.
if not IsBound(JUDGE_SCAN_THRESHOLD) then
  JUDGE_SCAN_THRESHOLD := 100000;;   # |[P,P]| * |charmingSet| above this uses Xi-restriction
fi;

CorrectedShadows := function(W, charmingSet)
  local sizePP, legacyCount, mode, res;
  sizePP := Size(DerivedSubgroup(W.PN));
  legacyCount := sizePP * Length(charmingSet);

  if IsBound(JUDGE_FORCE_SCAN_MODE) then
    mode := JUDGE_FORCE_SCAN_MODE;
  elif legacyCount <= JUDGE_SCAN_THRESHOLD then
    mode := "legacy";
  else
    mode := "xi_restricted";
  fi;

  if mode = "legacy" then
    res := CorrectedShadowsLegacy(W, charmingSet);
    res.scanned_count := legacyCount;
  elif mode = "xi_restricted" then
    res := CorrectedShadowsXi(W, charmingSet);
  else
    Error("kerchi-judge: JUDGE_FORCE_SCAN_MODE must be \"legacy\" or \"xi_restricted\", got ",
          mode);
  fi;
  res.scan_mode := mode;
  res.legacy_candidate_count := legacyCount;
  if res.scanned_count > 0 then
    res.compression := Float(legacyCount) / Float(res.scanned_count);
  else
    res.compression := -1;   # sentinel: undefined (zero candidates scanned)
  fi;
  return res;
end;;

GroupOfShadows := function(W, S)
  local n, i, j, m1, f1, u1, Eh, nm, nf, p, closed, regs, GT, kerIdx;
  n := Length(S);  closed := true;  regs := [];
  for i in [1 .. n] do
    m1 := S[i][1];  f1 := S[i][2];  u1 := 2*m1 + 1;
    Eh := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
            [W.x^u1, AbstractProd([f1^-1, W.y^u1, f1])]);
    if Eh = fail then return rec(closed := false, note := "E hom fail"); fi;
    regs[i] := [];
    for j in [1 .. n] do
      nm := (2*m1*S[j][1] + m1 + S[j][1]) mod W.Nord;
      nf := AbstractProd([f1, Image(Eh, S[j][2])]);
      p := Position(S, [nm, nf]);
      if p = fail then closed := false; regs[i][j] := 1; else regs[i][j] := p; fi;
    od;
  od;
  if not closed then return rec(closed := false); fi;
  regs := List(regs, PermList);
  GT := Group(regs);
  kerIdx := Filtered([1 .. n], i -> S[i][1] = 0);
  return rec(closed := true, G := GT, order := Size(GT), regs := regs,
             ker := Group(List(kerIdx, i -> regs[i])), ker_idx := kerIdx);
end;;

FindKerWitness := function(S, regs, kerIdx)
  local i, j;
  for i in [1 .. Length(kerIdx)] do
    for j in [i+1 .. Length(kerIdx)] do
      if regs[kerIdx[i]] * regs[kerIdx[j]] <> regs[kerIdx[j]] * regs[kerIdx[i]] then
        return rec(m1 := S[kerIdx[i]][1], f1 := S[kerIdx[i]][2],
                    m2 := S[kerIdx[j]][1], f2 := S[kerIdx[j]][2]);
      fi;
    od;
  od;
  return fail;
end;;

#############################################################################
## ---------------------- the judge itself -----------------------------------
#############################################################################
# JudgeWindow(s1, s2, label): the whole pipeline for one window given B3-generator
# images s1,s2 (already permutations, or matrices -- normalized below). Returns a
# result record; never Errors on a bad/degenerate window (records UNSCREENED
# instead) except for genuinely-broken input (e.g. braid relation not satisfied).
JudgeWindow := function(s1in, s2in, label)
  local s1, s2, Gtmp, iso, W, charmingSet, r, corr, corrRes, kerList, gi, dseries,
        crosscheck, qrecCk, hexres, hexSet;
  r := rec(label := label);

  # normalize input to a permutation representation
  if IsPerm(s1in) and IsPerm(s2in) then
    s1 := s1in;  s2 := s2in;
  else
    Gtmp := Group(s1in, s2in);
    if IsPermGroup(Gtmp) then
      s1 := s1in;  s2 := s2in;
    else
      iso := IsomorphismPermGroup(Gtmp);
      if iso = fail then
        Error("kerchi-judge: JudgeWindow could not build a permutation representation for '",
              label, "' -- fail-closed, not attempting a degraded computation");
      fi;
      s1 := Image(iso, s1in);  s2 := Image(iso, s2in);
    fi;
  fi;

  if AbstractProd([s1, s2, s1]) <> AbstractProd([s2, s1, s2]) then
    Error("kerchi-judge: JudgeWindow('", label,
          "'): braid relation s1 s2 s1 = s2 s1 s2 FAILS for the supplied images -- ",
          "this is not a valid B3 marking, refusing to judge it");
  fi;

  W := MakeWindow(s1, s2);
  r.abs_Bq := Size(W.Bq);
  r.abs_PN := Size(W.PN);
  r.c_in_N := (W.c = Identity(W.Bq));
  r.N_ord := W.Nord;
  charmingSet := Filtered([0 .. W.Nord - 1], m -> Gcd(2*m+1, W.Nord) = 1);;
  r.charming_count := Length(charmingSet);
  r.phi_2Nord := Phi(2 * W.Nord);

  Print("[judge] ", label, ": phase=CorrectedShadows starting (|Bq|=", Size(W.Bq),
        " |PN|=", Size(W.PN), " N_ord=", W.Nord, " charming_count=",
        Length(charmingSet), ")\n");
  corrRes := CorrectedShadows(W, charmingSet);;
  Print("[judge] ", label, ": phase=CorrectedShadows done (scan_mode=",
        corrRes.scan_mode, " shadow_total=", Length(corrRes.shadows),
        " settled_fail_count=", corrRes.settled_fail_count, ")\n");
  corr := corrRes.shadows;
  r.settled_fail_count := corrRes.settled_fail_count;
  r.settled_fail_witnesses := corrRes.settled_fail_witnesses;
  r.scan_mode := corrRes.scan_mode;
  r.scanned_count := corrRes.scanned_count;
  r.legacy_candidate_count := corrRes.legacy_candidate_count;
  r.compression := corrRes.compression;
  r.shadow_total := Length(corr);
  kerList := Filtered(corr, k -> k[1] = 0);;
  r.ker_size := Length(kerList);
  # "N/N settled" reporting (裁定170): every candidate that passed the three
  # original (F2) conditions is either in the final shadow set (settled=true,
  # implicitly -- shadow_total of them) or in settled_fail_witnesses/counted
  # in settled_fail_count (settled=false). Total hexagon-candidates evaluated
  # = shadow_total + settled_fail_count.
  r.settled_total_evaluated := r.shadow_total + r.settled_fail_count;
  r.settled_all_pass := (r.settled_fail_count = 0);

  # chi_image_order (裁定170 F79-2.1): |Im chi~| computed directly as the number
  # of DISTINCT u=2m+1 (mod 2*N_ord) values realized among the actual shadow
  # set corr (post-settled-filter) -- not assumed to be phi(2*N_ord).
  r.chi_image_order := Length(Set(List(corr, k -> (2*k[1] + 1) mod (2*W.Nord))));

  Print("[judge] ", label, ": phase=GroupOfShadows starting (n_shadows=", Length(corr), ")\n");
  gi := GroupOfShadows(W, corr);;
  Print("[judge] ", label, ": phase=GroupOfShadows done (closed=", gi.closed, ")\n");
  r.closure_353_holds := gi.closed;

  if gi.closed then
    r.isotropy_order := gi.order;
    r.ker_commutes := IsAbelian(gi.ker);
    if r.ker_commutes then
      r.witness := fail;
    else
      r.witness := FindKerWitness(corr, gi.regs, gi.ker_idx);
    fi;
    dseries := DerivedSeries(gi.G);
    r.derived_series_orders := List(dseries, Size);
    if IsSolvable(gi.G) then
      r.derived_length := DerivedLength(gi.G);
    else
      r.derived_length := -1;   # sentinel: not solvable, dl undefined
    fi;
    if r.ker_commutes then
      r.verdict := "ABELIAN";
    else
      r.verdict := "NONABELIAN";
    fi;
  else
    r.isotropy_order := -1;
    r.ker_commutes := false;
    r.witness := fail;
    r.derived_series_orders := [];
    r.derived_length := -1;
    r.verdict := "UNSCREENED";
    r.unscreened_reason := "(3.53) closure FAILED (E hom fail or shadow set not closed)";
  fi;

  # ---- T-A assert, universal form (裁定170 F79-2.1) ----
  # |ker chi~| * |Im chi~| = |G_N| (isotropy_order), checked against the ACTUAL
  # image order (chi_image_order), not an assumed-surjective phi(2*N_ord). This
  # is the form that should ALWAYS hold when (3.53) closes (it is just
  # |G_N| = |ker| * |image| for a homomorphism G_N -> (Z/2N_ord)^x), independent
  # of whether chi~ happens to be surjective onto its full nominal codomain.
  if gi.closed then
    r.ta_assert_holds := (r.ker_size * r.chi_image_order = r.isotropy_order);
  else
    r.ta_assert_holds := false;   # isotropy_order undefined (-1), assert can't be evaluated
  fi;
  # legacy field, kept for backward compatibility with v1/v1.1 certs/callers
  # (predicted ker under the ASSUMED-surjective-onto-phi(2N_ord) reading):
  if r.phi_2Nord = 0 or r.shadow_total mod r.phi_2Nord <> 0 then
    r.ta_predicted_ker := -1;
  else
    r.ta_predicted_ker := r.shadow_total / r.phi_2Nord;
  fi;

  # ---- chi~ surjectivity assert (裁定170): |Im chi~| =?= phi(2*N_ord) ----
  # Only "fires" (is evaluated/reported as non-null) for c_in_N windows, which
  # is the readily-available proxy this campaign has used throughout for
  # "isolated相当" -- genuine isolated-ness (ker(T_{m,f})=N for every shadow)
  # has never been independently verified anywhere in this campaign (see
  # docs/notes/wcp5d_resolution_v1.md GAP-4: "GTSh no 2 hyohon ha isolated-sei
  # wo dokuritsu kensho shite inai"), so this is a DELIBERATE, documented
  # simplification, not a claim that c_in_N literally implies isolated.
  if r.c_in_N then
    r.chi_surjective_assert := (r.chi_image_order = r.phi_2Nord);
  else
    r.chi_surjective_assert := fail;   # not applicable / not evaluated -- null in JSON
  fi;

  # ---- c_in_N crosscheck against the pre-existing quotient-shortcut enumerator ----
  # (EnumerateReducedHexagon in week3-battery-common.g is valid precisely when c_in_N;
  # see that file's comments and docs/notes/wcp5d_resolution_v1.md S3a: "c in N no toki
  # tau ga F2/N_F2 ni oriru" -- 16/16 confirmed there). This is a genuine independent
  # RE-DERIVATION of the same shadow set via a different code path (quotient-shortcut
  # theta/tau homomorphisms, not Ad(Delta)/Ad(delta) conjugation), so a mismatch here
  # would be a real red flag, not a tautology -- both paths share only the ambient
  # group W.PN and AbstractProd, not the enumeration logic itself.
  # v1.2 opt-out (裁定171・LID-1 processed alongside): bind
  # JUDGE_SKIP_LEGACY_CROSSCHECK := true;; before Read()-ing this file to
  # disable this block entirely (e.g. search/wall-miner-v5.g does this --
  # the coordinator's instruction there is explicit that EnumerateReducedHexagon
  # should not be relied on at all for the all-66-windows consolidation pass,
  # since KJ-1 raised the possibility that its own hex310/hex311 conditions
  # have the same missing-settled-check gap on the c_in_N side too). Default
  # (flag unbound) is unchanged from v1/v1.1: the crosscheck still runs.
  r.crosscheck_vs_EnumerateReducedHexagon := fail;
  if r.c_in_N and not (IsBound(JUDGE_SKIP_LEGACY_CROSSCHECK) and JUDGE_SKIP_LEGACY_CROSSCHECK = true) then
    Print("[judge] ", label, ": phase=crosscheck_vs_EnumerateReducedHexagon starting ",
          "(WARNING: this calls BFSWords over the WHOLE of P_N -- |PN|=", Size(W.PN),
          " -- infeasible if P_N is large; set JUDGE_SKIP_LEGACY_CROSSCHECK:=true;; ",
          "to skip this block for large-P windows)\n");
    qrecCk := rec(x := W.x, y := W.y, G := W.PN);
    hexres := fail;
    if GAPLIB_CheckCap(300.0, Concatenation(label, "-crosscheck")) then
      r.crosscheck_vs_EnumerateReducedHexagon := "SKIPPED (cap)";
    else
      hexres := EnumerateReducedHexagon(qrecCk, charmingSet);
      hexSet := Set(List(hexres.shadows, s -> [s.m, s.f]));
      r.crosscheck_vs_EnumerateReducedHexagon := (hexSet = corr);
    fi;
    Print("[judge] ", label, ": phase=crosscheck_vs_EnumerateReducedHexagon done (result=",
          r.crosscheck_vs_EnumerateReducedHexagon, ")\n");
  else
    Print("[judge] ", label, ": phase=crosscheck_vs_EnumerateReducedHexagon SKIPPED ",
          "(c_in_N=", r.c_in_N, ", JUDGE_SKIP_LEGACY_CROSSCHECK=",
          IsBound(JUDGE_SKIP_LEGACY_CROSSCHECK) and JUDGE_SKIP_LEGACY_CROSSCHECK, ")\n");
  fi;

  r.status := "computed";
  return r;
end;;

#############################################################################
## ---------------------- JSON serialization ---------------------------------
#############################################################################
WitnessJson := function(w)
  if w = fail then return "null"; fi;
  return Concatenation("{\"m1\":", String(w.m1), ",\"f1_perm\":", JStr(String(w.f1)),
                        ",\"m2\":", String(w.m2), ",\"f2_perm\":", JStr(String(w.f2)), "}");
end;;

CrosscheckJson := function(v)
  if v = fail then return "null"; fi;
  if v = "SKIPPED (cap)" then return JStr(v); fi;
  return JB(v);
end;;

BoolOrNullJson := function(v)
  if v = fail then return "null"; fi;
  return JB(v);
end;;

# compression is a GAP float (or -1 sentinel = undefined, e.g. scanned_count=0);
# GAP's String() on a float already yields a JSON-legal decimal literal.
FloatOrNullJson := function(v)
  local s;
  if IsInt(v) and v = -1 then return "null"; fi;   # sentinel (int -1); floats can't compare to -1 directly in GAP
  s := String(v);
  # GAP prints Float(1.0) as "1." (trailing dot, no digits) -- invalid JSON.
  if Length(s) > 0 and s[Length(s)] = '.' then s := Concatenation(s, "0"); fi;
  return s;
end;;

SettledFailWitnessesJson := function(ws)
  local items;
  items := List(ws, w -> Concatenation("{\"m\":", String(w.m),
                                        ",\"f_perm\":", JStr(String(w.f)), "}"));
  return JArr(items);
end;;

ResultJson := function(r)
  return Concatenation("{\n",
    "  \"label\":", JStr(r.label), ",\n",
    "  \"verdict\":", JStr(r.verdict), ",\n",
    "  \"c_in_N\":", JB(r.c_in_N), ",\n",
    "  \"abs_Bq\":", String(r.abs_Bq), ",\n",
    "  \"abs_PN\":", String(r.abs_PN), ",\n",
    "  \"N_ord\":", String(r.N_ord), ",\n",
    "  \"charming_count\":", String(r.charming_count), ",\n",
    "  \"shadow_total\":", String(r.shadow_total), ",\n",
    "  \"settled_fail_count\":", String(r.settled_fail_count), ",\n",
    "  \"settled_total_evaluated\":", String(r.settled_total_evaluated), ",\n",
    "  \"settled_all_pass\":", JB(r.settled_all_pass), ",\n",
    "  \"settled_fail_witnesses\":", SettledFailWitnessesJson(r.settled_fail_witnesses), ",\n",
    "  \"scan_mode\":", JStr(r.scan_mode), ",\n",
    "  \"scanned_count\":", String(r.scanned_count), ",\n",
    "  \"legacy_candidate_count\":", String(r.legacy_candidate_count), ",\n",
    "  \"compression\":", FloatOrNullJson(r.compression), ",\n",
    "  \"isotropy_order\":", String(r.isotropy_order), ",\n",
    "  \"ker_size\":", String(r.ker_size), ",\n",
    "  \"chi_image_order\":", String(r.chi_image_order), ",\n",
    "  \"phi_2Nord\":", String(r.phi_2Nord), ",\n",
    "  \"ta_predicted_ker\":", String(r.ta_predicted_ker), ",\n",
    "  \"ta_assert_holds\":", JB(r.ta_assert_holds), ",\n",
    "  \"chi_surjective_assert\":", BoolOrNullJson(r.chi_surjective_assert), ",\n",
    "  \"closure_353_holds\":", JB(r.closure_353_holds), ",\n",
    "  \"ker_commutes\":", JB(r.ker_commutes), ",\n",
    "  \"witness\":", WitnessJson(r.witness), ",\n",
    "  \"derived_series_orders\":", JArr(List(r.derived_series_orders, String)), ",\n",
    "  \"derived_length\":", String(r.derived_length), ",\n",
    "  \"crosscheck_vs_EnumerateReducedHexagon\":", CrosscheckJson(r.crosscheck_vs_EnumerateReducedHexagon), "\n",
    "}\n");
end;;

#############################################################################
## ---------------------- mode dispatch ---------------------------------------
#############################################################################
JudgeFromLinsNode := function(indexBound, windowId)
  local BF3, aa, bb, brel, B3, ga, gb, S3can, phiCan, PB3, gr, nodes, serialByIdx,
        nd, N, idx, wid, hm, isoQ, s1, s2;
  BF3 := FreeGroup("a", "b");;
  aa := BF3.1;;  bb := BF3.2;;
  brel := aa * bb * aa * (bb * aa * bb)^-1;;
  B3 := BF3 / [brel];;
  ga := B3.1;;  gb := B3.2;;
  S3can := SymmetricGroup(3);;
  phiCan := GroupHomomorphismByImages(B3, S3can, [ga, gb], [(1,2), (2,3)]);;
  if phiCan = fail then Error("canonical B3 -> S3 map failed sanity check"); fi;
  PB3 := Kernel(phiCan);;

  if LoadPackage("lins") <> true then
    Error("Failed to load GAP package LINS.");
  fi;
  gr := LowIndexNormalSubgroupsSearch(B3, indexBound);;
  nodes := ComputedNormalSubgroups(gr);;
  serialByIdx := rec();;
  for nd in nodes do
    N := Grp(nd);
    idx := Index(nd);
    if idx = 1 then continue; fi;
    if not IsSubset(PB3, N) then continue; fi;
    if IsBound(serialByIdx.(String(idx))) then
      serialByIdx.(String(idx)) := serialByIdx.(String(idx)) + 1;
    else
      serialByIdx.(String(idx)) := 1;
    fi;
    wid := Concatenation("W-A-B3idx", String(idx), "-s", String(serialByIdx.(String(idx))));
    if wid = windowId then
      hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
      isoQ := IsomorphismPermGroup(Image(hm));;
      s1 := Image(isoQ, Image(hm, ga));;
      s2 := Image(isoQ, Image(hm, gb));;
      return JudgeWindow(s1, s2, windowId);
    fi;
  od;
  Error("kerchi-judge: window_id '", windowId, "' not found among LINS nodes with index <= ",
        indexBound, " (N normal in B3, N <= PB3) -- check the id / index bound");
end;;

RunAndWrite := function(result, outfile)
  Print("\n=== VERDICT: ", result.verdict, " (", result.label, ") ===\n");
  Print("  c_in_N=", result.c_in_N, "  |B3/N|=", result.abs_Bq, " |P_N|=", result.abs_PN,
        "  N_ord=", result.N_ord, "\n");
  Print("  scan_mode=", result.scan_mode, "  scanned_count=", result.scanned_count,
        "  legacy_candidate_count=", result.legacy_candidate_count,
        "  compression=", result.compression, "\n");
  Print("  shadow_total=", result.shadow_total, "  settled_fail_count=", result.settled_fail_count,
        " (", result.settled_total_evaluated - result.settled_fail_count, "/",
        result.settled_total_evaluated, " settled)",
        "  isotropy_order=", result.isotropy_order, "  ker_size=", result.ker_size,
        "  chi_image_order=", result.chi_image_order, "\n");
  Print("  T-A assert (|ker|*|Im chi~|=|G_N|) holds=", result.ta_assert_holds,
        "  chi~ surjective onto phi(2N_ord) (c_in_N gate)=", result.chi_surjective_assert,
        "  (3.53) closure=", result.closure_353_holds,
        "  ker_commutes=", result.ker_commutes, "\n");
  Print("  derived_series_orders=", result.derived_series_orders,
        "  derived_length=", result.derived_length, "\n");
  Print("  crosscheck_vs_EnumerateReducedHexagon=", result.crosscheck_vs_EnumerateReducedHexagon, "\n");
  WriteFile(outfile, ResultJson(result));
  Print("Wrote ", outfile, "\n");
end;;

#############################################################################
## ---------------------- self-test (JUDGE_SELFTEST := true) -----------------
#############################################################################
# Fixture 1: W-C-N5cong (N5cong = ker(B3 -> S3 x SL(2,F5)); renamed 裁定170 from
#            "N5" to avoid collision with week1-定義ノート.md's own N5=ker(beta_5))
#            (c NOT in N; known answer per
#            docs/notes/wcp5d_resolution_v1.md S4: GTSh = C2 x Aff(F5), order 40,
#            ABELIAN ker chi~ (= C5)).
# Fixture 2: a K(3)-style c IN N control. NOTE (honesty over convenience): the
#            literal K^(3) := ker(psi_3: PB3 -> D3^3) is NOT built here -- this
#            repo has only ever constructed the PB3-restricted picture of K^(n)
#            (search/week1-kn-spotcheck.g's MakeGn: |PB3/K^(3)|=108, so
#            |B3/K^(3)|=648), never a full B3-marking (sigma1,sigma2 with the
#            wreath/S3 action needed for Delta,delta conjugation) -- building
#            that is flagged as open, nontrivial work elsewhere in this
#            campaign (docs/notes/wall_design_audit_v1.md SS7.3/8.2, item
#            [WA-c]: "B3-window lift" of a P). Substituting a fake construction
#            here would risk a silently-wrong self-test PASS, so instead this
#            fixture reuses W-A-B3idx144-s5 -- a c IN N window already
#            cross-validated three times over (wall-miner-v1/v3/v4: SL(2,3),
#            N_ord=6, all (F2) asserts held in v4) -- as the c-in-N control,
#            clearly labeled as a substitution, not literally "K(3)".
if IsBound(JUDGE_LIBRARY_ONLY) and JUDGE_LIBRARY_ONLY = true then
  # KJ-1 (裁定169) addition: define MakeWindow/JudgeWindow/JudgeFromLinsNode/etc.
  # and return control to the caller without running any single-window or
  # self-test dispatch. Intended for driver scripts (e.g.
  # search/kerchi-judge-v11-regression.g) that want to call JudgeWindow /
  # JudgeFromLinsNode directly, many times, with their own comparison logic,
  # rather than going through the "process exactly one window and write one
  # outfile" path below.
  Print("kerchi-judge.g loaded in JUDGE_LIBRARY_ONLY mode (no window processed here).\n");

elif IsBound(JUDGE_SELFTEST) and JUDGE_SELFTEST = true then
  Print("=== kerchi-judge.g SELF-TEST ===\n");
  SELFTEST_FAILS := 0;;

  Print("\n--- fixture 1: W-C-N5cong (N5cong = ker(B3 -> S3 x SL(2,F5))) ---\n");
  psi2 := IsomorphismPermGroup(Group([[1,1],[0,1]]*One(GF(2)), [[1,0],[1,1]]*One(GF(2))));;
  psi5 := IsomorphismPermGroup(Group([[1,1],[0,1]]*One(GF(5)), [[1,0],[4,1]]*One(GF(5))));;
  DP := DirectProduct(Image(psi2), Image(psi5));;
  s1p5 := Image(Embedding(DP,1), Image(psi2,[[1,1],[0,1]]*One(GF(2)))) *
          Image(Embedding(DP,2), Image(psi5,[[1,1],[0,1]]*One(GF(5))));;
  s2p5 := Image(Embedding(DP,1), Image(psi2,[[1,0],[1,1]]*One(GF(2)))) *
          Image(Embedding(DP,2), Image(psi5,[[1,0],[4,1]]*One(GF(5))));;
  resP5 := JudgeWindow(s1p5, s2p5, "W-C-N5cong-selftest");;
  RunAndWrite(resP5, "search/certs/kerchi_judge_selftest_p5.json");
  if resP5.verdict <> "ABELIAN" then
    SELFTEST_FAILS := SELFTEST_FAILS + 1;
    Print("  [FAIL] expected verdict ABELIAN, got ", resP5.verdict, "\n");
  fi;
  if resP5.isotropy_order <> 40 then
    SELFTEST_FAILS := SELFTEST_FAILS + 1;
    Print("  [FAIL] expected |GTSh|=40, got ", resP5.isotropy_order, "\n");
  fi;
  Print("  [", PF(resP5.verdict = "ABELIAN" and resP5.isotropy_order = 40),
        "] fixture 1 (W-C-N5cong): verdict=", resP5.verdict, " |GTSh|=", resP5.isotropy_order, "\n");

  Print("\n--- fixture 2: c-in-N control (W-A-B3idx144-s5, substituting for K(3) -- see comment above) ---\n");
  resK3 := JudgeFromLinsNode(192, "W-A-B3idx144-s5");;
  RunAndWrite(resK3, "search/certs/kerchi_judge_selftest_cinN_control.json");
  if resK3.crosscheck_vs_EnumerateReducedHexagon <> true then
    SELFTEST_FAILS := SELFTEST_FAILS + 1;
    Print("  [FAIL] c_in_N crosscheck vs EnumerateReducedHexagon did not hold: ",
          resK3.crosscheck_vs_EnumerateReducedHexagon, "\n");
  fi;
  if resK3.verdict <> "ABELIAN" then
    SELFTEST_FAILS := SELFTEST_FAILS + 1;
    Print("  [FAIL] expected verdict ABELIAN (per wall-miner-v4 result for this window), got ",
          resK3.verdict, "\n");
  fi;
  Print("  [", PF(resK3.verdict = "ABELIAN" and resK3.crosscheck_vs_EnumerateReducedHexagon = true),
        "] fixture 2 (c-in-N control): verdict=", resK3.verdict,
        " crosscheck=", resK3.crosscheck_vs_EnumerateReducedHexagon, "\n");

  Print("\n============================================================\n");
  Print("SELF-TEST FAILS = ", SELFTEST_FAILS, "\n");
  Print("============================================================\n");
  Print("KERCHI_JUDGE_SELFTEST_DONE\n");

elif IsBound(JUDGE_WINDOW_ID) and IsBound(JUDGE_INDEX_BOUND) then
  outfile := "";;
  if IsBound(JUDGE_OUTFILE) then outfile := JUDGE_OUTFILE;
  else outfile := Concatenation("search/certs/kerchi_judge_", JUDGE_WINDOW_ID, ".json"); fi;
  result := JudgeFromLinsNode(JUDGE_INDEX_BOUND, JUDGE_WINDOW_ID);;
  RunAndWrite(result, outfile);
  Print("KERCHI_JUDGE_DONE\n");

elif IsBound(JUDGE_S1_IMG) and IsBound(JUDGE_S2_IMG) then
  idLabel := "";;
  if IsBound(JUDGE_ID) then idLabel := JUDGE_ID; else idLabel := "direct"; fi;
  outfile := "";;
  if IsBound(JUDGE_OUTFILE) then outfile := JUDGE_OUTFILE;
  else outfile := Concatenation("search/certs/kerchi_judge_", idLabel, ".json"); fi;
  result := JudgeWindow(JUDGE_S1_IMG, JUDGE_S2_IMG, idLabel);;
  RunAndWrite(result, outfile);
  Print("KERCHI_JUDGE_DONE\n");

else
  Error("kerchi-judge.g: no valid input bound. Bind either ",
        "(JUDGE_INDEX_BOUND + JUDGE_WINDOW_ID), or (JUDGE_S1_IMG + JUDGE_S2_IMG), ",
        "or (JUDGE_SELFTEST := true) before Read()-ing this file.");
fi;
