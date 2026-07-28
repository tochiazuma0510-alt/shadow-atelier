#############################################################################
## search/kerchi-judge.g -- kerchi-judge v1 (裁定167・自動判定器)
##
## Packages the (F2) quotient-rule machinery (proven out on 17 real windows in
## search/wall-miner-v4.g, itself lifted from the coordinator-cross-checked
## search/wcp5d-verify.g / docs/notes/wcp5d_resolution_v1.md) into a single
## reusable script: given ONE window (however specified), decide whether
## ker(chi-tilde) (the m=0 layer of G_N=GTSh(N,N)) is ABELIAN or NONABELIAN,
## with every intermediate assert reported, fail-closed.
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
##      N5 = ker(B3 -> S3 x SL(2,F5)), same construction as wall-miner-v1/v4):
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
##   JUDGE_ID: "N5-SL2F5"
##
##   -- or, for the self-test:
##
##   preamble: JUDGE_SELFTEST:=true;;
##
## ---------------------------------------------------------------------
## OUTPUT: JUDGE_OUTFILE, a JSON record with fields:
##   verdict (one of "ABELIAN" | "NONABELIAN" | "UNSCREENED"), c_in_N,
##   abs_Bq, abs_PN, N_ord, charming_count, shadow_total, isotropy_order
##   (= |G_N| = |GTSh(N,N)|), ker_size, phi_2Nord, ta_predicted_ker,
##   ta_assert_holds, closure_353_holds, ker_commutes, witness (null unless
##   NONABELIAN), derived_series_orders, derived_length (or -1 if not
##   solvable), crosscheck_vs_EnumerateReducedHexagon (null unless c_in_N;
##   for c_in_N windows this cross-checks the (F2) shadow set against the
##   pre-existing quotient-shortcut enumerator in week3-battery-common.g,
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

CorrectedShadows := function(W, charmingSet)
  local out, f, m, u;
  out := [];
  for f in Elements(DerivedSubgroup(W.PN)) do
    if AbstractProd([f, TH(W, f)]) <> Identity(W.Bq) then continue; fi;
    for m in charmingSet do
      u := 2*m + 1;
      if RtOf(W, m, f) <> W.c^m then continue; fi;
      if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN) then continue; fi;
      Add(out, [m, f]);
    od;
  od;
  return Set(out);
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
  local s1, s2, Gtmp, iso, W, charmingSet, r, corr, kerList, gi, dseries,
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

  corr := CorrectedShadows(W, charmingSet);;
  r.shadow_total := Length(corr);
  kerList := Filtered(corr, k -> k[1] = 0);;
  r.ker_size := Length(kerList);

  if r.phi_2Nord = 0 then
    r.ta_predicted_ker := -1; r.ta_assert_holds := false;
  elif r.shadow_total mod r.phi_2Nord <> 0 then
    r.ta_predicted_ker := -1; r.ta_assert_holds := false;
  else
    r.ta_predicted_ker := r.shadow_total / r.phi_2Nord;
    r.ta_assert_holds := (r.ta_predicted_ker = r.ker_size);
  fi;

  gi := GroupOfShadows(W, corr);;
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

  # ---- c_in_N crosscheck against the pre-existing quotient-shortcut enumerator ----
  # (EnumerateReducedHexagon in week3-battery-common.g is valid precisely when c_in_N;
  # see that file's comments and docs/notes/wcp5d_resolution_v1.md S3a: "c in N no toki
  # tau ga F2/N_F2 ni oriru" -- 16/16 confirmed there). This is a genuine independent
  # RE-DERIVATION of the same shadow set via a different code path (quotient-shortcut
  # theta/tau homomorphisms, not Ad(Delta)/Ad(delta) conjugation), so a mismatch here
  # would be a real red flag, not a tautology -- both paths share only the ambient
  # group W.PN and AbstractProd, not the enumeration logic itself.
  r.crosscheck_vs_EnumerateReducedHexagon := fail;
  if r.c_in_N then
    qrecCk := rec(x := W.x, y := W.y, G := W.PN);
    hexres := fail;
    if GAPLIB_CheckCap(300.0, Concatenation(label, "-crosscheck")) then
      r.crosscheck_vs_EnumerateReducedHexagon := "SKIPPED (cap)";
    else
      hexres := EnumerateReducedHexagon(qrecCk, charmingSet);
      hexSet := Set(List(hexres.shadows, s -> [s.m, s.f]));
      r.crosscheck_vs_EnumerateReducedHexagon := (hexSet = corr);
    fi;
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
    "  \"isotropy_order\":", String(r.isotropy_order), ",\n",
    "  \"ker_size\":", String(r.ker_size), ",\n",
    "  \"phi_2Nord\":", String(r.phi_2Nord), ",\n",
    "  \"ta_predicted_ker\":", String(r.ta_predicted_ker), ",\n",
    "  \"ta_assert_holds\":", JB(r.ta_assert_holds), ",\n",
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
  Print("  shadow_total=", result.shadow_total, "  isotropy_order=", result.isotropy_order,
        "  ker_size=", result.ker_size, "\n");
  Print("  T-A assert holds=", result.ta_assert_holds, "  (3.53) closure=",
        result.closure_353_holds, "  ker_commutes=", result.ker_commutes, "\n");
  Print("  derived_series_orders=", result.derived_series_orders,
        "  derived_length=", result.derived_length, "\n");
  Print("  crosscheck_vs_EnumerateReducedHexagon=", result.crosscheck_vs_EnumerateReducedHexagon, "\n");
  WriteFile(outfile, ResultJson(result));
  Print("Wrote ", outfile, "\n");
end;;

#############################################################################
## ---------------------- self-test (JUDGE_SELFTEST := true) -----------------
#############################################################################
# Fixture 1: W-C-p5 = N5 = ker(B3 -> S3 x SL(2,F5)) (c NOT in N; known answer per
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
if IsBound(JUDGE_SELFTEST) and JUDGE_SELFTEST = true then
  Print("=== kerchi-judge.g SELF-TEST ===\n");
  SELFTEST_FAILS := 0;;

  Print("\n--- fixture 1: W-C-p5 (N5 = ker(B3 -> S3 x SL(2,F5))) ---\n");
  psi2 := IsomorphismPermGroup(Group([[1,1],[0,1]]*One(GF(2)), [[1,0],[1,1]]*One(GF(2))));;
  psi5 := IsomorphismPermGroup(Group([[1,1],[0,1]]*One(GF(5)), [[1,0],[4,1]]*One(GF(5))));;
  DP := DirectProduct(Image(psi2), Image(psi5));;
  s1p5 := Image(Embedding(DP,1), Image(psi2,[[1,1],[0,1]]*One(GF(2)))) *
          Image(Embedding(DP,2), Image(psi5,[[1,1],[0,1]]*One(GF(5))));;
  s2p5 := Image(Embedding(DP,1), Image(psi2,[[1,0],[1,1]]*One(GF(2)))) *
          Image(Embedding(DP,2), Image(psi5,[[1,0],[4,1]]*One(GF(5))));;
  resP5 := JudgeWindow(s1p5, s2p5, "W-C-p5-selftest");;
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
        "] fixture 1 (W-C-p5): verdict=", resP5.verdict, " |GTSh|=", resP5.isotropy_order, "\n");

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
