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

# apply a "pure Q" element (right multiplication, T-coordinate unaffected) -- used for
# f, f^-1, x^{-m}, y^{-m}, c^m factors of (3.3)/(3.4).
ApplyQElt := function(state, q)
  return [state[1], state[2]*q];
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
