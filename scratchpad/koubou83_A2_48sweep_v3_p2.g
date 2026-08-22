## scratchpad/koubou83_A2_48sweep_v3_p2.g -- A-2 v3, p=2 ONLY (2026-08-22, WARN-A2-1 / UNIT-2 fix)
##
## SUPERSESSION NOTICE: this file supersedes ONLY the p=2 half of
## search/certs/koubou83_A2_48sweep_v2_20260822.json. The p=3 half of that cert
## (48/48 both windows) is UNCHANGED and remains authoritative (theorem UNIT-INV:
## gcd(2,9)=gcd(2,3)=1, so the units bug below is invisible to any mod-3-power test).
##
## ROOT CAUSE (mathematician's ruling, scratchpad/c83_inn_lift_lemma_v1.md sec.8,
## theorem UNIT-2): koubou83_A2_48sweep_v2.g's ComputeLinking sums SIGNED CROSSING
## COUNTS without dividing by 2. For f in the free group F_2=<x,y> (x=sigma_1^2,
## y=sigma_2^2), the canonical abelianization is ab(f)=(deg_x f, deg_y f); the
## strand-linking formula (a,b,gamma)=(l12-l13,l23-l13,l13) reproduces this EXACTLY
## on F_2 only if l_jk is HALF the signed crossing count (since x=sigma_1^2 has
## crossing count 2, l12=1). v2 never divided by 2, so its ABGamma = 2x canonical.
## By theorem UNIT-INV, a scalar-2 error is INVISIBLE to any "M | linear-form" test
## with gcd(2,M)=1 (all the p=3,p=5 tests) but makes gcd(2,M)=2 tests (p=2's
## 2|a, 2|b, 2|gamma) VACUOUSLY TRUE -- p=2's charming/legal-gamma tests were never
## actually imposed nor checked, in v1 AND v2 alike. Verdict: p=2 full-48 result
## (v1: 48/48, v2: 24/48+17/48) is WITHDRAWN to UNKNOWN; this file re-derives it
## with the corrected (canonical, PIN-AB-1) units.
##
## PIN-AB-1 (scratchpad/c83_inn_lift_lemma_v1.md sec.8.7), implemented below:
##   ab(f) := (deg_x f, deg_y f) via l_jk := (signed crossing count)/2,
##   (a,b,gamma) := (l12-l13, l23-l13, l13). MANDATORY assert block (4 pins) at
##   top of file: (a,b,g)(sigma_1^2)=(1,0,0), (sigma_2^2)=(0,1,0), (Delta^2)=(0,0,1),
##   RAW (unhalved) crossing count of Delta^2 = (2,2,2). Plus a purity/evenness
##   runtime guard inside the corrected ABGamma itself (final permutation must be
##   identity, all three raw lk must be even) -- fires on EVERY call, not just the
##   4 pin words, per sec.8.7 item 4 ("assert evenness and final perm = identity").
##
## charming at K_p (PIN-AB-1 item 5): p|a and p|b and 3|((a+b)/p).
##   p=2: theorem A2-TAUT (independent of unit convention, gcd(2,3)=1) makes the
##   3rd condition TAUTOLOGICALLY TRUE given cond1 and cond2 -- so cond3 is set to
##   true directly for p=2, with a defensive assert that 3|(a_w+b_w) still holds
##   (raises ASSUMPTION-VIOLATED, does not silently pass, if that assumption ever
##   breaks). p=3 is NOT rerun here (commander: no rerun needed, theorem UNIT-INV
##   makes v2's p=3 result robust to the units bug).
##
## cond1/cond2/legal-gamma are BAKED into the same augmented linear system used in
## v1/v2 (TVecp/GVecp/AVecp/BVecp columns of augMat) -- this was ALREADY the
## architecture in v1 (not a v2-only feature); fixing ONLY the ABGamma units
## (AVecp/BVecp/GVecp values) is therefore sufficient: SolutionMat either finds a
## representative satisfying R1=R2=0 AND legal AND cond1/cond2 simultaneously (in
## which case ALL of those hold automatically for that witness, by construction of
## the augmented target -- not a partial search), or the system is UNSOLVABLE,
## which is an EXHAUSTIVE proof (over the full basis-word coset, not a sample) that
## no representative achieves charming/legal at p=2 for that shadow -- a genuine,
## fully-searched death, matching "解なしが尽くされて初めて死".
##
## Pre-registered predictions (fixed BEFORE running, per commander instruction):
##   P-A2-1: positive control [11,1] (idx43, both windows) survives at p=2.
##   P-A2-2: identity shadow (idx1, both windows) survives at p=2.
##   P-A2-3 (open, no bias toward any outcome): is the corrected p=2 survival count
##   48/48 or not? Report whatever is measured.

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/iso_census83_deep15_data.g");

BF3 := FreeGroup("a","b");;
brel := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;
B3 := BF3/[brel];;
aB3 := B3.1;; bB3 := B3.2;;
a := aB3;; b := bB3;;

targets := [154161, 154163];;
seen := [];; reps := [];;
for r1 in DEEP15 do
  if r1.id[1] = 1152 and (r1.id[2] in targets) and not (r1.id in seen) then
    Add(seen, r1.id); Add(reps, r1);
  fi;
od;;

FreeReduce := function(w)
  local out, l;
  out := [];
  for l in w do
    if Length(out) > 0 and out[Length(out)] = -l then Remove(out, Length(out)); else Add(out, l); fi;
  od;
  return out;
end;;
InvWord := function(w) return List(Reversed(w), l -> -l); end;;
RepWord := function(w, k)
  local out, i;
  out := [];
  if k >= 0 then for i in [1..k] do Append(out, w); od;
  else for i in [1..(-k)] do Append(out, InvWord(w)); od; fi;
  return out;
end;;

PB_next := [ [2,3], [1,4], [5,1], [6,2], [3,6], [4,5] ];;
PB_valw := [ [ [], [] ], [ [1], [] ], [ [], [2] ], [ [], [-2,-1] ], [ [-1,-2], [] ], [ [2], [1] ] ];;
PB_valk := [ [0,0], [0,0], [0,0], [0,1], [1,0], [0,0] ];;
PBcoords := function(W)
  local i, accW, acck, l, letter, nexti, val, kx;
  i := 1;;  accW := [];;  acck := 0;;
  for l in W do
    letter := AbsInt(l);;
    if l > 0 then
      nexti := PB_next[i][letter];;  val := PB_valw[i][letter];;  kx := PB_valk[i][letter];;
      Append(accW, val);;  acck := acck + kx;;  i := nexti;;
    else
      nexti := PB_next[i][letter];;  val := PB_valw[nexti][letter];;  kx := PB_valk[nexti][letter];;
      Append(accW, InvWord(val));;  acck := acck - kx;;  i := nexti;;
    fi;
  od;
  if i <> 1 then Error("PBcoords: not in PB3"); fi;
  return [FreeReduce(accW), acck];;
end;;

SubstXYtoSigma := function(xyword)
  local out, l;
  out := [];
  for l in xyword do
    if l = 1 then Append(out, [1,1]); elif l = -1 then Append(out, [-1,-1]);
    elif l = 2 then Append(out, [2,2]); elif l = -2 then Append(out, [-2,-2]);
    else Error("bad xy letter ", l); fi;
  od;
  return out;;
end;;

## ---- output files (row manifest jsonl + witness export jsonl) ----
rowsFile := "search/certs/koubou83_A2_48sweep_v3_p2_20260822_rows.jsonl";;
witFile := "search/certs/koubou83_A2_48sweep_v3_p2_20260822_witness.jsonl";;
PrintTo(rowsFile, "");;
PrintTo(witFile, "");;

JList := function(lst)
  return Concatenation("[", JoinStringsWithSeparator(List(lst, String), ","), "]");;
end;;
JBool := function(b)
  if b = true then return "true";
  elif b = false then return "false";
  else return "null";  ## covers GAP's 'fail' (used for the assumption-violated escape hatch)
  fi;
end;;

## ===== PIN-AB-1: canonical abelianization, halved-linking convention =====
## RAW (unhalved) signed-crossing-count linking, plus purity data (final perm,
## evenness). Does NOT depend on any window state -- defined once, globally.
ComputeLinkingRaw := function(sigmaWord)
  local perm, lk12, lk13, lk23, l, k, s, sA, sB, pr, tmp;
  perm := [1,2,3];;
  lk12 := 0;; lk13 := 0;; lk23 := 0;;
  for l in sigmaWord do
    k := AbsInt(l);;  s := SignInt(l);;
    sA := perm[k];;  sB := perm[k+1];;
    pr := Set([sA, sB]);;
    if pr = [1,2] then lk12 := lk12 + s;
    elif pr = [1,3] then lk13 := lk13 + s;
    elif pr = [2,3] then lk23 := lk23 + s;
    else Error("bad strand pair ", pr); fi;
    tmp := perm[k];;  perm[k] := perm[k+1];;  perm[k+1] := tmp;;
  od;
  return rec(lk12:=lk12, lk13:=lk13, lk23:=lk23, finalPerm:=perm);;
end;;
## Corrected ABGamma: canonical units (l_jk = raw_crossing_count/2), with a
## MANDATORY purity/evenness runtime guard on EVERY call (sec.8.7 item 4):
## final permutation must be identity, all three raw lk must be even. This is
## NOT limited to the 4 pin words below -- it fires on every basis word, every
## shadow generator, every witness built during the real sweep.
ABGamma := function(sigmaWord)
  local raw;
  raw := ComputeLinkingRaw(sigmaWord);;
  if raw.finalPerm <> [1,2,3] then
    Error("PIN-AB-1 PURITY VIOLATION: word does not induce identity permutation: ", sigmaWord);;
  fi;
  if raw.lk12 mod 2 <> 0 or raw.lk13 mod 2 <> 0 or raw.lk23 mod 2 <> 0 then
    Error("PIN-AB-1 EVENNESS VIOLATION: odd raw crossing count for word: ", sigmaWord,
          "  raw=", [raw.lk12,raw.lk13,raw.lk23]);;
  fi;
  return [ (raw.lk12-raw.lk13)/2, (raw.lk23-raw.lk13)/2, raw.lk13/2 ];;
end;;

## ===== MANDATORY assert block (4 pins, sec.8.7 item 3) -- stop and report if any fails =====
PinSigma1Sq := [1,1];;         ## x = sigma_1^2
PinSigma2Sq := [2,2];;         ## y = sigma_2^2
PinDeltaSq  := [1,2,1,1,2,1];; ## Delta^2 = c = (sigma_1 sigma_2 sigma_1)^2 (6 letters)

pinRawDelta := ComputeLinkingRaw(PinDeltaSq);;
if [pinRawDelta.lk12, pinRawDelta.lk13, pinRawDelta.lk23] <> [2,2,2] then
  Error("PIN-AB-1 ASSERT FAILED: raw crossing count of Delta^2 expected [2,2,2], got ",
        [pinRawDelta.lk12, pinRawDelta.lk13, pinRawDelta.lk23]);;
fi;
pinS1 := ABGamma(PinSigma1Sq);;
if pinS1 <> [1,0,0] then
  Error("PIN-AB-1 ASSERT FAILED: (a,b,gamma)(sigma_1^2) expected [1,0,0], got ", pinS1);;
fi;
pinS2 := ABGamma(PinSigma2Sq);;
if pinS2 <> [0,1,0] then
  Error("PIN-AB-1 ASSERT FAILED: (a,b,gamma)(sigma_2^2) expected [0,1,0], got ", pinS2);;
fi;
pinD := ABGamma(PinDeltaSq);;
if pinD <> [0,0,1] then
  Error("PIN-AB-1 ASSERT FAILED: (a,b,gamma)(Delta^2) expected [0,0,1], got ", pinD);;
fi;
Print("PIN-AB-1 ASSERT BLOCK: ALL 4 PINS PASSED  (sigma_1^2)->", pinS1, "  (sigma_2^2)->", pinS2,
      "  (Delta^2)->", pinD, "  raw-crossing(Delta^2)=", [pinRawDelta.lk12,pinRawDelta.lk13,pinRawDelta.lk23], "\n");

for r1 in reps do
  Print("\n\n################ WINDOW ", r1.id, " ################\n");
  gens := List(r1.words, w -> EvalString(w));;
  N := Subgroup(B3, gens);;
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  iso := IsomorphismPermGroup(Image(hm));;
  s1 := Image(iso, Image(hm, aB3));;  s2 := Image(iso, Image(hm, bB3));;
  Bq := Group(s1,s2);;
  x := s1^2;;  y := s2^2;;  c := (s1*s2*s1)^2;;
  PN := Group(x,y);;
  Els := Elements(PN);;  nn := Length(Els);;
  posOf := function(g) return Position(Els, g); end;;
  kappa := Order(c);;

  if r1.id[2] = 154161 then m0xy := [-1,-1,-1,-1,-1,-1];;
  else m0xy := RepWord([-1,-2], 3);; fi;

  evXY := function(w, xelt, yelt)
    local acc, l;
    acc := xelt^0;;
    for l in w do
      if l=1 then acc := acc*xelt; elif l=-1 then acc := acc*xelt^-1;
      elif l=2 then acc := acc*yelt; elif l=-2 then acc := acc*yelt^-1;
      else Error("bad xy letter ", l); fi;
    od;
    return acc;;
  end;;
  if evXY(m0xy, x, y) <> c^-1 then Error("m0 pin failed"); fi;

  ## ===== generic prime-p machinery (mirrors koubou83_leg1_h2_w2_v1.g's BuildPrimeMachinery) =====
  BuildPrimeMachinery := function(p)
    local onep, zerop, negonep, Foxp, Dmat, i, KDp, cinv, Pmat, imgUp, rankUp, dimVp,
          PhiMapp, RankTrackerAddp, pivotsUp, uv, RedVecp, pivotsFullp, basisWordsp, basisVecsp,
          wstr, sw, fw, phiv, fullvec, before, dBasisp, redBasisCachep, ExpressInBasisp;
    onep := One(GF(p));;  zerop := Zero(GF(p));;  negonep := -onep;;
    Foxp := function(w)
      local Dx, Dy, pre, l;
      Dx := List([1..nn], ii->zerop);;  Dy := List([1..nn], ii->zerop);;
      pre := Identity(PN);;
      for l in w do
        if l = 1 then Dx[posOf(pre)] := Dx[posOf(pre)] + onep;  pre := pre*x;
        elif l = -1 then pre := pre*x^-1;  Dx[posOf(pre)] := Dx[posOf(pre)] + negonep;
        elif l = 2 then Dy[posOf(pre)] := Dy[posOf(pre)] + onep;  pre := pre*y;
        elif l = -2 then pre := pre*y^-1;  Dy[posOf(pre)] := Dy[posOf(pre)] + negonep;
        else Error("bad xy letter ", l); fi;
      od;
      return Concatenation(Dx, Dy);;
    end;;
    Dmat := NullMat(2*nn, nn, GF(p));;
    for i in [1..nn] do
      Dmat[i][posOf(Els[i]*x)] := Dmat[i][posOf(Els[i]*x)] + onep;
      Dmat[i][i] := Dmat[i][i] + negonep;
      Dmat[nn+i][posOf(Els[i]*y)] := Dmat[nn+i][posOf(Els[i]*y)] + onep;
      Dmat[nn+i][i] := Dmat[nn+i][i] + negonep;
    od;;
    KDp := NullspaceMat(Dmat);;
    cinv := c^-1;;
    Pmat := NullMat(2*nn, 2*nn, GF(p));;
    for i in [1..nn] do
      Pmat[i][posOf(cinv*Els[i])] := onep;;
      Pmat[nn+i][nn+posOf(cinv*Els[i])] := onep;;
    od;;
    imgUp := List(KDp, v -> v*Pmat - v);;
    rankUp := RankMat(imgUp);;
    dimVp := Length(KDp) - rankUp + 1;;
    PhiMapp := function(sigmaWord)
      local coords, w, k, mword, ev;
      coords := PBcoords(sigmaWord);;
      w := coords[1];;  k := coords[2];;
      mword := FreeReduce(Concatenation(w, RepWord(m0xy, -k)));;
      ev := evXY(mword, x, y);;
      if ev <> Identity(PN) then Error("PhiMapP BOOKKEEPING-FAIL"); fi;
      return [Foxp(mword), k mod p];;
    end;;
    RankTrackerAddp := function(pivots, vec)
      local v, col, pp;
      v := ShallowCopy(vec);;
      for pp in pivots do
        col := pp[1];;
        if v[col] <> zerop then v := v - v[col]/pp[2][col] * pp[2]; fi;
      od;
      col := PositionNonZero(v);;
      if col <= Length(v) then Add(pivots, [col, v]); fi;
      return pivots;;
    end;;
    pivotsUp := [];;
    for uv in imgUp do pivotsUp := RankTrackerAddp(pivotsUp, Concatenation(uv, [zerop])); od;;
    RedVecp := function(vec)
      local v, pp, col;
      v := ShallowCopy(vec);;
      for pp in pivotsUp do
        col := pp[1];;
        if v[col] <> zerop then v := v - v[col]/pp[2][col] * pp[2]; fi;
      od;
      return v;;
    end;;
    pivotsFullp := ShallowCopy(pivotsUp);;
    basisWordsp := [];;  basisVecsp := [];;
    for wstr in r1.words do
      sw := EvalString(wstr);;
      fw := LetterRepAssocWord(UnderlyingElement(PreImagesRepresentative(
              EpimorphismFromFreeGroup(B3 : names:=["a","b"]), sw)));;
      phiv := PhiMapp(fw);;
      fullvec := Concatenation(phiv[1], [phiv[2]*onep]);;
      before := Length(pivotsFullp);;
      pivotsFullp := RankTrackerAddp(pivotsFullp, fullvec);;
      if Length(pivotsFullp) > before then Add(basisWordsp, fw);; Add(basisVecsp, fullvec);; fi;
    od;;
    dBasisp := Length(basisWordsp);;
    redBasisCachep := List(basisVecsp, RedVecp);;
    ExpressInBasisp := function(fullvec)
      return SolutionMat(redBasisCachep, RedVecp(fullvec));;
    end;;
    return rec(p:=p, onep:=onep, zerop:=zerop, negonep:=negonep, dimVp:=dimVp, dBasisp:=dBasisp,
               PhiMapp:=PhiMapp, RedVecp:=RedVecp, ExpressInBasisp:=ExpressInBasisp,
               basisWordsp:=basisWordsp);;
  end;;

  BuildRword := function(Fsigma, wword, m, u)
    local candWord, xm, ym, cm, lhs1, rhs1, R1w, lhs2, rhs2, R2w;
    candWord := FreeReduce(Concatenation(Fsigma, wword));;
    if m = 0 then xm := []; else xm := ListWithIdenticalEntries(2*AbsInt(m), SignInt(-m)); fi;
    cm := RepWord([1,2,1,1,2,1], m);;
    lhs1 := Concatenation(ListWithIdenticalEntries(u,1), InvWord(candWord),
                          ListWithIdenticalEntries(u,2), candWord);;
    rhs1 := Concatenation(InvWord(candWord), [1,2], xm, cm);;
    R1w := FreeReduce(Concatenation(lhs1, InvWord(rhs1)));;
    lhs2 := Concatenation(InvWord(candWord), ListWithIdenticalEntries(u,2), candWord,
                          ListWithIdenticalEntries(u,1));;
    if m = 0 then ym := []; else
      if m > 0 then ym := ListWithIdenticalEntries(2*m, -2); else ym := ListWithIdenticalEntries(2*(-m), 2); fi;
    fi;
    rhs2 := Concatenation([2,1], ym, cm, candWord);;
    R2w := FreeReduce(Concatenation(lhs2, InvWord(rhs2)));;
    return [R1w, R2w];;
  end;;

  ## builds A-differential + charming/legal machinery for one prime p, returns a solver closure
  BuildSolverForPrime := function(mach, p)
    local TVecp, GVecp, AVecp, BVecp, WfullVecp, j, abgj, WitnessFromXip, EvalWitnessAt, SolveAug;
    TVecp := [];;  GVecp := [];;  AVecp := [];;  BVecp := [];;  WfullVecp := [];;
    for j in [1..mach.dBasisp] do
      abgj := ABGamma(mach.basisWordsp[j]);;
      Add(AVecp, (abgj[1] mod p)*mach.onep);;
      Add(BVecp, (abgj[2] mod p)*mach.onep);;
      Add(GVecp, (abgj[3] mod p)*mach.onep);;
      Add(TVecp, (mach.PhiMapp(mach.basisWordsp[j])[2] mod p)*mach.onep);;
      Add(WfullVecp, abgj[1]+abgj[2]);;  ## EXACT integer, independent of p reduction
    od;;
    WitnessFromXip := function(xic)
      local supp, i, cnt, r, ww;
      supp := Filtered([1..mach.dBasisp], i -> xic[i] <> mach.zerop);;
      ww := [];;
      for i in supp do
        cnt := IntFFE(xic[i]);;
        for r in [1..cnt] do Append(ww, mach.basisWordsp[i]); od;;
      od;
      return ww;;
    end;;
    ## computes (legalOk,cond1,cond2,directOk,abgW,Wsum) for a GIVEN xic vector (used both
    ## for the baseline xiAug and for any constructed kappa-shifted candidate)
    EvalWitnessAt := function(Fsigma, m, u, xic, abgF0)
      local ww, phiW, tCoordW, abgW, legalOk2, cond1x, cond2x, RRw, phi1w, phi2w, v1w, v2w, directOk2;
      ww := WitnessFromXip(xic);;
      phiW := mach.PhiMapp(ww);;  tCoordW := phiW[2] mod p;;
      abgW := ABGamma(ww);;
      legalOk2 := (tCoordW = 0) and (abgW[3] mod p = 0);;
      cond1x := (abgF0[1]+abgW[1]) mod p = 0;;
      cond2x := (abgF0[2]+abgW[2]) mod p = 0;;
      RRw := BuildRword(Fsigma, ww, m, u);;
      phi1w := mach.PhiMapp(RRw[1]);;  phi2w := mach.PhiMapp(RRw[2]);;
      v1w := mach.RedVecp(Concatenation(phi1w[1],[phi1w[2]*mach.onep]));;
      v2w := mach.RedVecp(Concatenation(phi2w[1],[phi2w[2]*mach.onep]));;
      directOk2 := IsZero(v1w) and IsZero(v2w);;
      return rec(ww:=ww, legalOk:=legalOk2, cond1:=cond1x, cond2:=cond2x, directOk:=directOk2, abgW:=abgW);;
    end;;
    SolveAug := function(Fsigma, m)
      local u, RR0, phi10, phi20, r1coeffs, r2coeffs, cols1, cols2, j2, RRj, phi1j, phi2j,
            c1j, c2j, Amat1, Amat2, Mstack, target, abgF0, augMat, augTarget, xiAug,
            base, KerAug, kerDim, S, Wsum0, assumptionViolated, cond3, cond3method, wwFinalRec;
      u := 2*m+1;;
      RR0 := BuildRword(Fsigma, [], m, u);;
      phi10 := mach.PhiMapp(RR0[1]);;  phi20 := mach.PhiMapp(RR0[2]);;
      r1coeffs := mach.ExpressInBasisp(Concatenation(phi10[1],[phi10[2]*mach.onep]));;
      r2coeffs := mach.ExpressInBasisp(Concatenation(phi20[1],[phi20[2]*mach.onep]));;
      cols1 := [];;  cols2 := [];;
      for j2 in [1..mach.dBasisp] do
        RRj := BuildRword(Fsigma, mach.basisWordsp[j2], m, u);;
        phi1j := mach.PhiMapp(RRj[1]);;  phi2j := mach.PhiMapp(RRj[2]);;
        c1j := mach.ExpressInBasisp(Concatenation(phi1j[1],[phi1j[2]*mach.onep])) - r1coeffs;;
        c2j := mach.ExpressInBasisp(Concatenation(phi2j[1],[phi2j[2]*mach.onep])) - r2coeffs;;
        Add(cols1, c1j);;  Add(cols2, c2j);;
      od;
      Amat1 := TransposedMat(cols1);;  Amat2 := TransposedMat(cols2);;
      Mstack := Concatenation(Amat1, Amat2);;
      target := Concatenation(-r1coeffs, -r2coeffs);;
      abgF0 := ABGamma(Fsigma);;
      augMat := List([1..mach.dBasisp], j2 -> Concatenation(TransposedMat(Mstack)[j2],
                [ TVecp[j2], GVecp[j2], AVecp[j2], BVecp[j2] ]));;
      augTarget := Concatenation(target,
                [ mach.zerop, mach.zerop, (((-abgF0[1]) mod p)*mach.onep), (((-abgF0[2]) mod p)*mach.onep) ]);;
      xiAug := SolutionMat(augMat, augTarget);;
      if xiAug = fail then
        return rec(solvable:=false, legalOk:=false, cond1:=false, cond2:=false, cond3:=false,
                   cond3method:="NOT-SOLVABLE", charmOk:=false, directOk:=false, kerDim:=-1,
                   assumptionViolated:=false, wwFinal:=[], survives:=false);;
      fi;
      KerAug := NullspaceMat(augMat);;
      kerDim := Length(KerAug);;

      base := EvalWitnessAt(Fsigma, m, u, xiAug, abgF0);;
      S := abgF0[1]+abgF0[2];;
      Wsum0 := base.abgW[1]+base.abgW[2];;
      assumptionViolated := false;;
      if Wsum0 mod 3 <> 0 then assumptionViolated := true;; fi;
      if not (base.cond1 and base.cond2) then
        ## cond1/cond2 failing at baseline is itself anomalous per the "always baked
        ## into augMat" argument -- flag but do not crash the sweep.
        assumptionViolated := true;;
      fi;
      if assumptionViolated then
        ## fall back to the plain (pre-fix) two-condition semantics for this row and
        ## flag it loudly; do not silently apply the cond3 machinery to an anomalous row.
        return rec(solvable:=true, legalOk:=base.legalOk, cond1:=base.cond1, cond2:=base.cond2,
                   cond3:=fail, charmOk:=fail, directOk:=base.directOk,
                   survives := fail, kerDim:=kerDim, cond3method:="ASSUMPTION-VIOLATED-see-row",
                   assumptionViolated:=true, wwFinal:=base.ww);;
      fi;
      ## p=2 ONLY in this file. Theorem A2-TAUT (mathematician, sec.7.2/8.6): given
      ## cond1(2|a) and cond2(2|b) hold, the 3rd charming condition 3|((a+b)/2) is
      ## TAUTOLOGICALLY TRUE (uses only mod-3 facts, gcd(2,3)=1, robust to the units
      ## bug either way). We do NOT search for it. Its precondition (3 | Wsum0) was
      ## ALREADY checked above (the assumptionViolated guard returned early if it
      ## failed) -- reaching this point means it holds, so cond3 is tautologically true.
      cond3 := true;;
      cond3method := "tautological-A2-TAUT-p-neq-3";;
      wwFinalRec := base;;

      return rec(solvable:=true, legalOk:=wwFinalRec.legalOk, cond1:=wwFinalRec.cond1,
                 cond2:=wwFinalRec.cond2, cond3:=cond3, cond3method:=cond3method,
                 charmOk:=(wwFinalRec.cond1 and wwFinalRec.cond2 and cond3),
                 directOk:=wwFinalRec.directOk, kerDim:=kerDim, assumptionViolated:=false,
                 wwFinal:=wwFinalRec.ww,
                 survives := (wwFinalRec.legalOk and wwFinalRec.cond1 and wwFinalRec.cond2
                              and cond3 and wwFinalRec.directOk));;
    end;;
    return SolveAug;;
  end;;

  mach2 := BuildPrimeMachinery(2);;
  Print("dimV2=", mach2.dimVp, " dBasis2=", mach2.dBasisp, "\n");
  Solve2 := BuildSolverForPrime(mach2, 2);;

  ## ===== enumerate the FULL 48-shadow corr list =====
  Nord := Lcm(Order(x), Order(y), Order(c));;
  charmingSet := Filtered([0..Nord-1], mm -> Gcd(2*mm+1,Nord)=1);;
  Dlt := s1*s2*s1;;  dlt := s1*s2;;
  TTfn := function(g) return dlt*g*dlt^-1; end;;
  THfn := function(g) return Dlt*g*Dlt^-1; end;;
  RtOfFn := function(m,f) local Wd; Wd := y^m*f; return TTfn(TTfn(Wd))*TTfn(Wd)*Wd; end;;
  corr := [];;
  for f in Elements(DerivedSubgroup(PN)) do
    if f*THfn(f) <> Identity(Bq) then continue; fi;
    for m in charmingSet do
      u := 2*m+1;;
      if RtOfFn(m,f) <> c^m then continue; fi;
      if Size(Group(x^u, f^-1*y^u*f)) <> Size(PN) then continue; fi;
      Add(corr, [m,f]);;
    od;
  od;;
  corr := Set(corr);;
  Print("|corr| (48-shadow set) = ", Length(corr), "\n");

  ## comparison baseline = v2's (units-broken) p=2 result for this window, indexed
  ## 1..48 in the SAME corr enumeration order (from
  ## search/certs/koubou83_A2_48sweep_v2_20260822_rows.jsonl, sorted by shadow_idx).
  if r1.id[2] = 154161 then
    v2p2broken := [true,true,true,false,false,false,false,false,true,false,true,false,true,false,
      true,true,true,false,true,false,false,true,true,false,true,false,false,true,true,false,
      true,false,true,true,true,false,false,false,true,false,true,false,true,true,true,false,
      false,false];;
  else
    v2p2broken := [true,true,true,false,false,false,true,true,true,false,true,false,false,false,
      false,false,false,false,false,false,false,true,true,false,true,true,true,false,false,true,
      false,true,false,false,true,false,false,false,false,true,false,false,false,false,false,
      false,true,false];;
  fi;

  survives2count := 0;;
  idx := 0;;
  for sh in corr do
    idx := idx + 1;;
    mm := sh[1];;  fval := sh[2];;
    fxy := LetterRepAssocWord(UnderlyingElement(PreImagesRepresentative(
             EpimorphismFromFreeGroup(PN : names:=["x","y"]), fval)));;
    Fsigma := SubstXYtoSigma(fxy);;
    res2 := Solve2(Fsigma, mm);;
    if res2.solvable and res2.survives=true then survives2count := survives2count+1;; fi;
    Print("[shadow ", idx, "/48] m=", mm,
          "  p2: solvable=", res2.solvable, " survives=", res2.survives,
          " cond3method=", res2.cond3method, " kerDim=", res2.kerDim, "\n");

    ## ---- row manifest (jsonl) ----
    AppendTo(rowsFile,
      "{\"window\":", JList(r1.id), ",\"shadow_idx\":", idx, ",\"m\":", mm,
      ",\"f_xyword\":", JList(fxy), ",\"p\":2",
      ",\"solvable\":", JBool(res2.solvable),
      ",\"legalOk\":", JBool(res2.legalOk),
      ",\"cond1\":", JBool(res2.cond1), ",\"cond2\":", JBool(res2.cond2),
      ",\"cond3\":", JBool(res2.cond3), ",\"cond3_method\":\"", res2.cond3method, "\"",
      ",\"kerDim\":", res2.kerDim,
      ",\"directOk\":", JBool(res2.directOk),
      ",\"assumption_violated\":", JBool(res2.assumptionViolated),
      ",\"survives_v3\":", JBool(res2.survives),
      ",\"survives_v2_units_broken\":", JBool(v2p2broken[idx]),
      ",\"changed_v2_to_v3\":", JBool(res2.survives <> v2p2broken[idx]),
      "}\n");
    AppendTo(witFile,
      "{\"window\":", JList(r1.id), ",\"shadow_idx\":", idx, ",\"m\":", mm,
      ",\"f_xyword\":", JList(fxy), ",\"p\":2",
      ",\"witness_sigma_word\":", JList(res2.wwFinal),
      "}\n");
  od;

  Print("\nWINDOW ", r1.id, " A-3(p=2) SUMMARY: survives-p2=", survives2count, "/48\n");
od;;

Print("\nA2_48SWEEP_V3_P2_DONE\n");
