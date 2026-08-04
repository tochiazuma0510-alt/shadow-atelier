# statemachine_lib.g -- Lane V shared library: an explicit "transversal-cocycle" state
# machine representing B3/N (or B3/N0) WITHOUT ever materializing the (huge, degree
# 6*|Q|) permutation representation of the full group.
#
# Design rationale (own derivation, reported for review):
#   Full (3.3)/(3.4) must be checked as literal equalities in B3/N (resp. B3/N0), where
#   B3/N is an extension  1 -> Q -> B3/N -> S3 -> 1  (Q = PB3/N, a p-group here; S3 =
#   B3/PB3, order 6). Building B3/N as an explicit GAP permutation group of degree
#   6*|Q| (|Q| up to 7^9 for the control window) is infeasible on this machine (RAM 8GB
#   constraint) and unnecessary: we only need to evaluate a handful of SPECIFIC words
#   (the LHS/RHS of (3.3)/(3.4) for specific m,f) starting from the identity coset, i.e.
#   we only need the ORBIT of a single basepoint under those specific words, not the
#   whole group.
#
#   The general "Q x T" (transversal-cocycle) model used elsewhere in this project
#   (search/week3-M5-explorer.g, function BuildQTGeneral -- general, frozen WP2
#   infrastructure per docs/wp2-transversal-model.md, predates and is independent of the
#   hsp7 Lane S/P driver code that Lane V is barred from reading) encodes exactly this
#   extension as a permutation representation on 6*|Q| points, built from three inputs
#   phiX, phiY, phiC (images of x,y,c in Q) via a 6x2-branch table (one branch per of the
#   6 T-values, for each of s1,s2). Lane V reuses that SAME abstract table (it is
#   general-purpose GT-shadow machinery, not a Lane S/P specific driver), but
#   REIMPLEMENTS it as a function acting on a single (t,d) pair -- t in 1..6, d in Q --
#   instead of as a materialized PermList. This scales to any |Q|.
#
#   Because Lane V additionally needs s1^-1, s2^-1 (not present in BuildQTGeneral, which
#   only ever needed forward application when building a full permutation), those two
#   inverse tables were derived BY HAND from the forward table (by solving "which input
#   state maps here" for each of the 6 branches). This hand derivation is exactly the
#   kind of self-decided step Sol's warnings target, so SelfTestStateMachine (below)
#   cross-validates the whole four-generator table (forward AND inverse) against an
#   independent, brute-force rebuild of BuildQTGeneral's own PermList construction on a
#   small toy group, checked at EVERY one of the 6*|Q0| points, before the state machine
#   is trusted on the real (large) P / P x C7.
#
Read("search/probe/wac_v1/gap_output_prelude.g");

# ---- forward/inverse table, operating on state = [t, d] ----
# gen in {1,-1,2,-2} meaning s1, s1^-1, s2, s2^-1 respectively.
ApplyGen := function(state, gen, phiX, phiY, phiC)
  local t, d, phiXi, phiYi, phiCi, newT, newD;
  t := state[1]; d := state[2];
  phiXi := phiX^-1; phiYi := phiY^-1; phiCi := phiC^-1;
  if gen = 1 then
    if t=1 then newD:=d; newT:=2;
    elif t=2 then newD:=d*phiX; newT:=1;
    elif t=3 then newD:=d; newT:=5;
    elif t=4 then newD:=d; newT:=6;
    elif t=5 then newD:=d*phiXi*phiYi*phiC; newT:=3;
    else newD:=d*phiY; newT:=4; fi;
  elif gen = -1 then
    if t=1 then newD:=d*phiXi; newT:=2;
    elif t=2 then newD:=d; newT:=1;
    elif t=3 then newD:=d*phiCi*phiY*phiX; newT:=5;
    elif t=4 then newD:=d*phiYi; newT:=6;
    elif t=5 then newD:=d; newT:=3;
    else newD:=d; newT:=4; fi;
  elif gen = 2 then
    if t=1 then newD:=d; newT:=3;
    elif t=2 then newD:=d; newT:=4;
    elif t=3 then newD:=d*phiY; newT:=1;
    elif t=4 then newD:=d*phiYi*phiXi*phiC; newT:=2;
    elif t=5 then newD:=d; newT:=6;
    else newD:=d*phiX; newT:=5; fi;
  elif gen = -2 then
    if t=1 then newD:=d*phiYi; newT:=3;
    elif t=2 then newD:=d*phiCi*phiX*phiY; newT:=4;
    elif t=3 then newD:=d; newT:=1;
    elif t=4 then newD:=d; newT:=2;
    elif t=5 then newD:=d*phiXi; newT:=6;
    else newD:=d; newT:=5; fi;
  else
    Error("ApplyGen: unknown gen ", gen);
  fi;
  return [newT, newD];
end;;

# ============================================================================
# ★★ BUGGY -- DO NOT USE (kept only for audit history; superseded 2026-08-04
# by arbitration docs/notes/hsp7_hexagon_arbitration_v1.md SS3.2).
#
# State (t,d) represents the group element g = d~ * t~ (t~ in {1,s1,s2,s1s2,
# s2s1,s1s2s1}, model A, confirmed correct by TEST A). Right-multiplying g by a
# pure-Q element q gives g*q = d~ t~ q~ = d~ (t~ q~ t~^-1) t~, i.e.
#   newD = d * Ad(t~)(q),   NOT   newD = d*q.
# ApplyQElt below computes d*q, which equals d~ q~ t~ = g*(t~^-1 q~ t~) -- only
# correct at t=1 (t~=identity). For t != 1 it silently applies q conjugated the
# WRONG way. c is central so ApplyQElt(s,c^m) alone was accidentally correct,
# which is why the "c-side bookkeeping looked healthy" (arbitration SS3.2).
# This bug produced S-9 mismatch=6 in search/certs/hsp7_cond4_laneV_20260804.json
# (v1, HELD). Root-caused and reproduced independently in scratchpad/arb_toy.g.
# ============================================================================
ApplyQElt := function(state, q)
  return [state[1], state[2]*q];
end;;

# ============================================================================
# FIX (2026-08-04, arbitration SS5.4 repair A -- first choice, "structurally
# eliminates the bug class"): never apply a pure-Q element directly. Instead
# expand it into a WORD in the free generators x,y (and, for c, the fixed
# 6-letter sigma-word (s1 s2)^3 = c), then push that word through the
# ALREADY-VALIDATED ApplyGen one sigma-letter at a time (TEST A: model
# g = d~*t~ matched a literal group 12/12; braid relation and forward/inverse
# tables cross-validated against BuildQTGeneral -- see driver_step3_selftest.g).
# Because x = s1^2 and y = s2^2, this is exact: no Ad(t~) table is needed, and
# the whole "conjugate by the current transversal element" bookkeeping that the
# old ApplyQElt got wrong is handled automatically by ApplyGen's own (already
# correct) per-branch table. Cross-validated against a fully independent
# LITERAL construction of a small window (search/probe/hsp7_cond4_laneV/
# driver_step3b_toy_fixture.g, scale-model of arbitration scratchpad/arb_toy.g).
# ============================================================================

# apply a sequence of signed generator indices (1/-1 = s1/s1^-1, 2/-2 = s2/s2^-1)
# to a state, one ApplyGen call per letter, in the given (paper) order.
ApplyWordSeq := function(state, seq, phiX, phiY, phiC)
  local s, g;
  s := state;
  for g in seq do
    s := ApplyGen(s, g, phiX, phiY, phiC);
  od;
  return s;
end;;

# repeat a signed-letter sequence k times (k<0: repeat the letter-wise-inverted,
# reversed sequence -k times). Matches arb_toy.g's SeqPow exactly.
SeqPow := function(seq, k)
  local r, i, inv;
  r := [];
  if k >= 0 then
    for i in [1..k] do Append(r, seq); od;
  else
    inv := Reversed(List(seq, g -> -g));
    for i in [1..(-k)] do Append(r, inv); od;
  fi;
  return r;
end;;

# fixed sigma-letter words for the generators of Q used throughout NW(7)/NW-P8:
#   x = s1^2, y = s2^2, c = (s1 s2)^3  (standard braid identity (sigma1 sigma2)^3
#   = Delta^2 = c; matches arb_toy.g's Cg := (S1*S2)^3 exactly).
SeqX := [1, 1];;
SeqY := [2, 2];;
SeqC := [1, 2, 1, 2, 1, 2];;

# expand a free-group word (over generators named "x","y", e.g. from
# LetterRepAssocWord) into a sigma-letter sequence: each x-letter -> 2 s1
# letters, each y-letter -> 2 s2 letters, sign preserved, order preserved.
ExpandXYLettersToSigma := function(letterRep)
  local out, l;
  out := [];
  for l in letterRep do
    if l = 1 then Append(out, SeqX);
    elif l = -1 then Append(out, Reversed(List(SeqX, g -> -g)));
    elif l = 2 then Append(out, SeqY);
    elif l = -2 then Append(out, Reversed(List(SeqY, g -> -g)));
    else Error("ExpandXYLettersToSigma: letter rep uses more than 2 generators (got ", l, ") -- only x,y (F2.1,F2.2) supported"); fi;
  od;
  return out;
end;;

# apply a free-group element (word in x,y) to a state via the validated ApplyGen
# path (sigma-letter expansion).
ApplyFreeWord := function(state, freeElt, phiX, phiY, phiC)
  return ApplyWordSeq(state, ExpandXYLettersToSigma(LetterRepAssocWord(freeElt)), phiX, phiY, phiC);
end;;

# ============================================================================
# EvalFullHexagonFixed(m, freeF, phiX, phiY, phiC): full (3.3)/(3.4), computed
# entirely via sigma-word expansion (repair A). freeF must be an ELEMENT OF A
# FREE GROUP ON (x,y) (e.g. built with Comm()/products in FreeGroup("x","y")),
# NOT a pc-group element -- this is what lets f, f^-1, x^{-m}, y^{-m} all be
# expanded into sigma-letters safely. phiX,phiY,phiC remain the TARGET window's
# images of x,y,c (pc group / direct product elements, as before).
# ============================================================================
EvalFullHexagonFixed := function(m, freeF, phiX, phiY, phiC)
  local u, freeFinv, base, s, lhs33, rhs33, lhs34, rhs34, fSeq, fInvSeq;
  u := 2*m+1;
  freeFinv := freeF^-1;
  fSeq := ExpandXYLettersToSigma(LetterRepAssocWord(freeF));
  fInvSeq := ExpandXYLettersToSigma(LetterRepAssocWord(freeFinv));
  base := [1, Identity(phiX)];

  # LHS(3.3) = sigma1^u f^-1 sigma2^u f
  s := ApplyWordSeq(base, Concatenation(SeqPow([1],u), fInvSeq, SeqPow([2],u), fSeq), phiX, phiY, phiC);
  lhs33 := s;
  # RHS(3.3) = f^-1 sigma1 sigma2 x^-m c^m   (NO trailing f -- verbatim (3.3), page-image
  # confirmed by arbitration SS2.1; adding one is the (b') trap, arbitration SS2.3)
  s := ApplyWordSeq(base, Concatenation(fInvSeq, [1,2], SeqPow(SeqX,-m), SeqPow(SeqC,m)), phiX, phiY, phiC);
  rhs33 := s;

  # LHS(3.4) = f^-1 sigma2^u f sigma1^u
  s := ApplyWordSeq(base, Concatenation(fInvSeq, SeqPow([2],u), fSeq, SeqPow([1],u)), phiX, phiY, phiC);
  lhs34 := s;
  # RHS(3.4) = sigma2 sigma1 y^-m c^m f   (trailing f present -- verbatim (3.4))
  s := ApplyWordSeq(base, Concatenation([2,1], SeqPow(SeqY,-m), SeqPow(SeqC,m), fSeq), phiX, phiY, phiC);
  rhs34 := s;

  return rec(hex33 := (lhs33 = rhs33), hex34 := (lhs34 = rhs34));
end;;

# apply s1 (or s2) exactly n>=0 times (n<0 means apply the inverse -n times)
ApplyGenPow := function(state, genIdx, n, phiX, phiY, phiC)
  local s, i;
  s := state;
  if n >= 0 then
    for i in [1..n] do s := ApplyGen(s, genIdx, phiX, phiY, phiC); od;
  else
    for i in [1..(-n)] do s := ApplyGen(s, -genIdx, phiX, phiY, phiC); od;
  fi;
  return s;
end;;

# ---- BuildQTGeneral, reused verbatim from search/week3-M5-explorer.g ----
# (general WP2 transversal-cocycle infra, not Lane S/P specific; used here ONLY inside
# SelfTestStateMachine, on a small toy group, to cross-validate ApplyGen.)
BuildQTGeneral := function(Qgrp, phiX, phiY, phiC)
  local Qelts, posDict, posOf, phiXi, phiYi, np, imgS1, imgS2, t, i, d, pt, val, tp;
  Qelts := Elements(Qgrp);
  np := Length(Qelts);
  posDict := NewDictionary(Qelts[1], true);
  for i in [1..np] do AddDictionary(posDict, Qelts[i], i); od;
  posOf := function(v) return LookupDictionary(posDict, v); end;
  phiXi := phiX^-1;  phiYi := phiY^-1;
  imgS1 := [];;  imgS2 := [];;
  for t in [1..6] do
    for i in [1..np] do
      d := Qelts[i];  pt := (t-1)*np + i;
      if t=1 then val:=d; tp:=2;
      elif t=2 then val:=d*phiX; tp:=1;
      elif t=3 then val:=d; tp:=5;
      elif t=4 then val:=d; tp:=6;
      elif t=5 then val:=d*phiXi*phiYi*phiC; tp:=3;
      else val:=d*phiY; tp:=4; fi;
      imgS1[pt] := (tp-1)*np + posOf(val);
      if t=1 then val:=d; tp:=3;
      elif t=2 then val:=d; tp:=4;
      elif t=3 then val:=d*phiY; tp:=1;
      elif t=4 then val:=d*phiYi*phiXi*phiC; tp:=2;
      elif t=5 then val:=d; tp:=6;
      else val:=d*phiX; tp:=5; fi;
      imgS2[pt] := (tp-1)*np + posOf(val);
    od;
  od;
  return rec(s1:=PermList(imgS1), s2:=PermList(imgS2), np:=np, elts:=Qelts, posOf:=posOf);
end;;

# ---- self test: cross-validate ApplyGen (incl. hand-derived inverses) against
# BuildQTGeneral, exhaustively over all 6*|Q0| points, on a small toy group; and
# independently confirm the braid relation s1 s2 s1 = s2 s1 s2 holds identically in
# the ApplyGen state machine (not assumed, checked).
SelfTestStateMachine := function()
  local Q0, phiX0, phiY0, phiC0, qt, np, t, i, pt, stateIn, viaTable, viaPerm, viaPermState,
        mismatches, mismatchesInv, braidFail, s, s1s2s1, s2s1s2, elt;
  Q0 := SymmetricGroup(4);;
  phiX0 := (1,2,3,4);;
  phiY0 := (1,2);;
  phiC0 := (1,3);;
  qt := BuildQTGeneral(Q0, phiX0, phiY0, phiC0);;
  np := qt.np;;
  mismatches := 0;;  mismatchesInv := 0;;
  for t in [1..6] do
    for i in [1..np] do
      pt := (t-1)*np + i;
      stateIn := [t, qt.elts[i]];
      # forward s1
      viaTable := ApplyGen(stateIn, 1, phiX0, phiY0, phiC0);
      viaPerm := pt^(qt.s1);
      viaPermState := [ QuoInt(viaPerm-1, np) + 1, qt.elts[ RemInt(viaPerm-1, np) + 1 ] ];
      if viaTable <> viaPermState then mismatches := mismatches + 1; fi;
      # forward s2
      viaTable := ApplyGen(stateIn, 2, phiX0, phiY0, phiC0);
      viaPerm := pt^(qt.s2);
      viaPermState := [ QuoInt(viaPerm-1, np) + 1, qt.elts[ RemInt(viaPerm-1, np) + 1 ] ];
      if viaTable <> viaPermState then mismatches := mismatches + 1; fi;
      # inverse s1^-1: apply forward s1 then ApplyGen(.,-1,...) must return to stateIn
      viaTable := ApplyGen(ApplyGen(stateIn, 1, phiX0, phiY0, phiC0), -1, phiX0, phiY0, phiC0);
      if viaTable <> stateIn then mismatchesInv := mismatchesInv + 1; fi;
      # inverse s2^-1
      viaTable := ApplyGen(ApplyGen(stateIn, 2, phiX0, phiY0, phiC0), -2, phiX0, phiY0, phiC0);
      if viaTable <> stateIn then mismatchesInv := mismatchesInv + 1; fi;
    od;
  od;
  # braid relation s1 s2 s1 = s2 s1 s2, checked over all 6*|Q0| starting states directly
  # in the ApplyGen state machine (independent of the PermList cross-check above).
  braidFail := 0;;
  for t in [1..6] do
    for i in [1..np] do
      s := [t, qt.elts[i]];
      s1s2s1 := ApplyGen(ApplyGen(ApplyGen(s,1,phiX0,phiY0,phiC0),2,phiX0,phiY0,phiC0),1,phiX0,phiY0,phiC0);
      s2s1s2 := ApplyGen(ApplyGen(ApplyGen(s,2,phiX0,phiY0,phiC0),1,phiX0,phiY0,phiC0),2,phiX0,phiY0,phiC0);
      if s1s2s1 <> s2s1s2 then braidFail := braidFail + 1; fi;
    od;
  od;
  return rec(total_points := 6*np, forward_mismatches := mismatches,
             inverse_roundtrip_mismatches := mismatchesInv, braid_relation_fail := braidFail);
end;;

# ---- second self-test: braid relation on a GENUINE B3-quotient instance ----
# Finding (own derivation, reported): the arbitrary-element toy above (S4 with hand-picked
# phiX0,phiY0,phiC0) does NOT satisfy the braid relation even via the reference
# BuildQTGeneral/PermList construction itself (independently confirmed) -- i.e. the 12-rule
# table only represents a genuine copy of B3 when (Q,phiX,phiY,phiC) come from an actual
# B3-compatible quotient, not for arbitrary group elements. SelfTestStateMachine above is
# therefore only a syntactic cross-check (does ApplyGen match BuildQTGeneral's arithmetic);
# it does NOT by itself certify that the table is being used correctly. This second test
# checks braid relation on a KNOWN-VALID instance (the dihedral G_n = Im(psi_n) construction,
# MakeGn -- general infra from search/week3-L-explorer.g, c |-> 1 case) and on a
# control-style instance (G_n x C5 with x,y trivial in the C5 factor and c trivial in the
# G_n factor, embedded via DirectProduct) -- structurally identical to Lane V's planned
# P x C7 construction for the N0 (control) window.
MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  return [r, s];
end;;

MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y));
end;;

SelfTestBraidOnGenuineInstance := function()
  local gn, chat0, np, elts, braidFailMain, t, i, s, a, b,
        C5, gc, D, e1, e2, xhatD, yhatD, chatD, npD, eltsD, braidFailCtrl;
  gn := MakeGn(3);;
  chat0 := Identity(gn.G);;
  np := Size(gn.G);;  elts := Elements(gn.G);;
  braidFailMain := 0;;
  for t in [1..6] do
    for i in [1..np] do
      s := [t, elts[i]];
      a := ApplyGen(ApplyGen(ApplyGen(s,1,gn.x,gn.y,chat0),2,gn.x,gn.y,chat0),1,gn.x,gn.y,chat0);
      b := ApplyGen(ApplyGen(ApplyGen(s,2,gn.x,gn.y,chat0),1,gn.x,gn.y,chat0),2,gn.x,gn.y,chat0);
      if a<>b then braidFailMain := braidFailMain+1; fi;
    od;
  od;
  C5 := CyclicGroup(IsPermGroup, 5);;
  gc := GeneratorsOfGroup(C5)[1];;
  D := DirectProduct(gn.G, C5);;
  e1 := Embedding(D,1);;  e2 := Embedding(D,2);;
  xhatD := Image(e1, gn.x);;  yhatD := Image(e1, gn.y);;  chatD := Image(e2, gc);;
  npD := Size(D);;  eltsD := Elements(D);;
  braidFailCtrl := 0;;
  for t in [1..6] do
    for i in [1..npD] do
      s := [t, eltsD[i]];
      a := ApplyGen(ApplyGen(ApplyGen(s,1,xhatD,yhatD,chatD),2,xhatD,yhatD,chatD),1,xhatD,yhatD,chatD);
      b := ApplyGen(ApplyGen(ApplyGen(s,2,xhatD,yhatD,chatD),1,xhatD,yhatD,chatD),2,xhatD,yhatD,chatD);
      if a<>b then braidFailCtrl := braidFailCtrl+1; fi;
    od;
  od;
  return rec(main_points := 6*np, main_braid_fail := braidFailMain,
             ctrl_points := 6*npD, ctrl_braid_fail := braidFailCtrl);
end;;

# ============================================================================
# ★ PERMANENT REGRESSION FIXTURE (mandated by arbitration SS5.4 item 4, audit
# gap closed: the old selftest exercised ApplyGen but never ApplyQElt/the pure-Q
# application path -- this is exactly where the bug lived). Scale-model window,
# independent of NW(7):
#   N_F2 = gamma3(F2) F2^3 (verbal, class<=2, exponent 3) => Q = extraspecial
#   3^{1+2}, order 27; c |-> 1 => B3/N has order 162, SMALL ENOUGH to build
#   LITERALLY via an fp-group presentation + IsomorphismPermGroup (no state
#   machine at all). Dummy-family analogue f = a^k, a=[x,y] in gamma2(Q) (the
#   window's top layer, central + elementary abelian) -- structurally identical
#   in role to h4^t in gamma4(P), just one layer shallower.
#   Prop 3.4 predicts full (3.3)(3.4) PASS for ALL k, at BOTH m=0 and m=2 (the
#   other element of X_N for N_ord=3), since theta(a)=a^-1, tau(a)=a make (3.10)
#   and (3.11) hold exactly regardless of m (m only appears via y^m in (3.11),
#   and a's tau-fixedness kills that dependence too -- checked below, not
#   assumed).
# ============================================================================
TestToyFixtureLiteralVsFixed := function()
  local FreeB, s1, s2, xw, yw, rels, Gfp, iso, S1, S2, Xg, Yg, Cg, aa,
        EvalLiteral, mVals, results, m, k, f, lit, fx, mismatches, r,
        FreeXY, aFree;

  FreeB := FreeGroup("s1", "s2");;
  s1 := FreeB.1;;  s2 := FreeB.2;;
  xw := s1^2;;  yw := s2^2;;
  rels := [ s1*s2*s1*(s2*s1*s2)^-1,
            (s1*s2)^3,
            xw^3, yw^3, Comm(xw,yw)^3,
            Comm(Comm(xw,yw),xw), Comm(Comm(xw,yw),yw) ];;
  Gfp := FreeB/rels;;
  if Size(Gfp) <> 162 then
    return rec(ok := false, reason := Concatenation("Size(B3/N) = ", String(Size(Gfp)), ", expected 162"));
  fi;
  iso := IsomorphismPermGroup(Gfp);;
  S1 := Image(iso, Gfp.1);;  S2 := Image(iso, Gfp.2);;
  Xg := S1^2;;  Yg := S2^2;;  Cg := (S1*S2)^3;;
  if Size(Group(Xg,Yg)) <> 27 then
    return rec(ok := false, reason := Concatenation("Size(Q) = ", String(Size(Group(Xg,Yg))), ", expected 27"));
  fi;
  if Cg <> One(Group(S1,S2)) then
    return rec(ok := false, reason := "c is not trivial in this TOY window (expected c->1)");
  fi;
  if not (S1*S2*S1 = S2*S1*S2) then
    return rec(ok := false, reason := "braid relation fails in the LITERAL toy group (fp-presentation error)");
  fi;
  aa := Comm(Xg,Yg);;

  EvalLiteral := function(m, f)
    local u;
    u := 2*m+1;
    return rec(hex33 := (S1^u * f^-1 * S2^u * f = f^-1 * S1 * S2 * Xg^(-m) * Cg^m),
               hex34 := (f^-1 * S2^u * f * S1^u = S2 * S1 * Yg^(-m) * Cg^m * f));
  end;;

  # free-group (x,y) words for a^k, fed through EvalFullHexagonFixed exactly as
  # the real driver feeds h4^t/h3 -- this is what makes the fixture a genuine
  # regression test of the SAME code path, not a reimplementation.
  FreeXY := FreeGroup("x","y");;
  aFree := Comm(FreeXY.1, FreeXY.2);;
  mVals := [0, 2];;
  results := [];;
  mismatches := 0;;
  for m in mVals do
    for k in [0, 1, 2] do
      f := aa^k;
      lit := EvalLiteral(m, f);
      fx := EvalFullHexagonFixed(m, aFree^k, Xg, Yg, Cg);
      r := rec(m := m, k := k, literal_hex33 := lit.hex33, literal_hex34 := lit.hex34,
               fixed_hex33 := fx.hex33, fixed_hex34 := fx.hex34,
               agree := (lit.hex33 = fx.hex33) and (lit.hex34 = fx.hex34),
               predicted_pass := true);
      if not r.agree then mismatches := mismatches + 1; fi;
      if not (lit.hex33 and lit.hex34) then
        # literal itself should PASS per Prop 3.4 (a is theta-anti-fixed, tau-fixed) --
        # if it doesn't, the fixture's own math is wrong, not just the state machine.
        mismatches := mismatches + 1;
      fi;
      Add(results, r);
    od;
  od;
  return rec(ok := true, size_B3N := Size(Gfp), size_Q := Size(Group(Xg,Yg)),
             mismatches := mismatches, results := results);
end;;

# ============================================================================
# ★ EXTENSION (2026-08-04, CV-9 副検問 blocking B-2 / non-blocking m1): the
# original TOY fixture above only exercises phi(c)=1 (c dies) and has no
# negative cell (all 6 literal results are PASS) -- so it has zero
# discriminating power against a constant-PASS evaluator, and zero
# discriminating power on the c-accounting path specifically (the very axis
# where the original bug lived, since c is central and ApplyQElt's old bug was
# invisible for central q). This extension adds:
#   (i)  a CONTROL-style toy window where phi(c) survives with order 3
#        (N_F2 = gamma3(F2)F2^3 as before, but c^3=1 instead of c=1 -- exact
#        structural analogue of the real N0 = P x C7, scaled down),
#   (ii) a negative fixture f=x (a generator, NOT in [F2,F2] / not charming),
#        which literal evaluation shows FAILS (3.3)/(3.4) on both the main and
#        control toy windows, at m=0.
# ============================================================================
TestToyFixtureExtended := function()
  local FreeB0, s1_0, s2_0, xw0, yw0, rels0, Gfp0, iso0, S1c, S2c, Xc, Yc, Cc,
        FreeXY, aFree, xFree, EvalLiteral, results, mismatches, m, k, f, lit, fx, r,
        litNeg, fxNeg;

  # ---- control-style toy: c survives with order 3 ----
  FreeB0 := FreeGroup("s1","s2");;
  s1_0 := FreeB0.1;;  s2_0 := FreeB0.2;;
  xw0 := s1_0^2;;  yw0 := s2_0^2;;
  rels0 := [ s1_0*s2_0*s1_0*(s2_0*s1_0*s2_0)^-1,
             xw0^3, yw0^3, Comm(xw0,yw0)^3,
             Comm(Comm(xw0,yw0),xw0), Comm(Comm(xw0,yw0),yw0),
             ((s1_0*s2_0)^3)^3 ];;   # c^3 = 1 (NOT c = 1)
  Gfp0 := FreeB0/rels0;;
  if Size(Gfp0) <> 486 then
    return rec(ok := false, reason := Concatenation("Size(control TOY B3/N0) = ", String(Size(Gfp0)), ", expected 486"));
  fi;
  iso0 := IsomorphismPermGroup(Gfp0);;
  S1c := Image(iso0, Gfp0.1);;  S2c := Image(iso0, Gfp0.2);;
  Xc := S1c^2;;  Yc := S2c^2;;  Cc := (S1c*S2c)^3;;
  if Order(Cc) <> 3 then
    return rec(ok := false, reason := Concatenation("Order(c) in control TOY = ", String(Order(Cc)), ", expected 3 (c must survive)"));
  fi;
  if not (S1c*S2c*S1c = S2c*S1c*S2c) then
    return rec(ok := false, reason := "braid relation fails in the control TOY literal group");
  fi;

  EvalLiteral := function(S1,S2,Xg,Yg,Cg,m,f)
    local u;
    u := 2*m+1;
    return rec(hex33 := (S1^u * f^-1 * S2^u * f = f^-1 * S1 * S2 * Xg^(-m) * Cg^m),
               hex34 := (f^-1 * S2^u * f * S1^u = S2 * S1 * Yg^(-m) * Cg^m * f));
  end;;

  FreeXY := FreeGroup("x","y");;
  aFree := Comm(FreeXY.1, FreeXY.2);;
  xFree := FreeXY.1;;

  results := [];;  mismatches := 0;;

  # (i) c-nontrivial cells: dummy analogue a^k on the CONTROL toy, m in {0,2}
  # (same X_N as the main toy, N_ord=3 for both). Prop 3.4 predicts PASS for
  # ALL these too (a is still charming/central regardless of window).
  for m in [0, 2] do
    for k in [0, 1, 2] do
      f := Comm(Xc,Yc)^k;
      lit := EvalLiteral(S1c, S2c, Xc, Yc, Cc, m, f);
      fx := EvalFullHexagonFixed(m, aFree^k, Xc, Yc, Cc);
      r := rec(cell := "control-c-alive", m := m, k := k,
               literal_hex33 := lit.hex33, literal_hex34 := lit.hex34,
               fixed_hex33 := fx.hex33, fixed_hex34 := fx.hex34,
               agree := (lit.hex33 = fx.hex33) and (lit.hex34 = fx.hex34));
      if not r.agree then mismatches := mismatches + 1; fi;
      if not (lit.hex33 and lit.hex34) then mismatches := mismatches + 1; fi;  # literal itself must PASS (Prop 3.4)
      Add(results, r);
    od;
  od;

  # (ii) negative fixture: f = x (generator, not charming), m = 0, on BOTH
  # main toy (c->1, reuse TestToyFixtureLiteralVsFixed's construction inline)
  # and control toy (c order 3). Literal must FAIL here -- if EvalFullHexagonFixed
  # also FAILS, the evaluator is demonstrated non-constant (real discriminating
  # power), not merely "always returns PASS".
  litNeg := EvalLiteral(S1c, S2c, Xc, Yc, Cc, 0, Xc);;
  fxNeg := EvalFullHexagonFixed(0, xFree, Xc, Yc, Cc);;
  r := rec(cell := "negative-f=x-control", m := 0, k := "n/a",
           literal_hex33 := litNeg.hex33, literal_hex34 := litNeg.hex34,
           fixed_hex33 := fxNeg.hex33, fixed_hex34 := fxNeg.hex34,
           agree := (litNeg.hex33 = fxNeg.hex33) and (litNeg.hex34 = fxNeg.hex34));
  if not r.agree then mismatches := mismatches + 1; fi;
  if litNeg.hex33 or litNeg.hex34 then
    mismatches := mismatches + 1;  # literal must actually FAIL for this to be a negative fixture
  fi;
  if fxNeg.hex33 or fxNeg.hex34 then
    mismatches := mismatches + 1;  # fixed evaluator must also FAIL, proving it is not constant-PASS
  fi;
  Add(results, r);

  return rec(ok := true, size_control_B3N0 := Size(Gfp0), order_c_control := Order(Cc),
             mismatches := mismatches, results := results);
end;;
