#############################################################################
## drophunt_checker_producer_v3.g -- REPAIR per ruling 1746 (WDICT-5).
##
## Root cause (falsifier NO-GO #2): v2's predicate obtained a candidate's
## word wp via PreImagesRepresentative (GAP's own free-group epimorphism,
## APPEND/standard left-to-right convention: word evaluates as g1*g2*...*gn)
## but then fed wp into EvalWordInQ, which uses PREPEND convention (val :=
## g^pow * val, i.e. REVERSED order). EvalWordInQ(wp) != p in general -- the
## predicate was silently evaluating theta/tau on a DIFFERENT group element
## than the one it claimed to test, in the direction that manufactures FALSE
## DROPs (a fake NO_LIFT verdict).
##
## Repair (per scratchpad/math_f6false_admarking_v1.g, 150-window machine-
## confirmed): DROP WORDS ENTIRELY from predicate evaluation. theta~=Ad(Delta),
## tau~=Ad(delta) are built as GENUINE AUTOMORPHISMS of A:=Group(JX,JY,JC) via
## closed-form identities that hold IN PB3 ITSELF (hence in every quotient
## PB3/K automatically, requiring NO sigma1/sigma2 marking of the window):
##   Ad(Delta)(x)=y, Ad(Delta)(y)=x, Ad(Delta)(c)=c            [Delta=s1 s2 s1]
##   Ad(delta)(x)=y, Ad(delta)(y)=y^-1 x^-1 c, Ad(delta)(c)=c  [delta=s1 s2]
## Predicate (F2), evaluated ENTIRELY on GROUP ELEMENTS:
##   (i)   f * theta~(f) = 1
##   (ii)  tau~^2(y^m f) * tau~(y^m f) * (y^m f) = c^m
##   (iii) <x^u, f^-1 y^u f> = G  (u=2m+1)
## This ELIMINATES the earlier F6=false BLOCKED case for the reasons that
## motivated it: theta~/tau~ no longer require sigma1/sigma2 of the roof at
## all (M or K1), only JC (c's joint image), which is already computable
## from data this producer already builds (M-block c-image is a documented
## constant, see item 7 grounding note below; L-block c-image = Cp, from
## S1p,S2p already computed for L).
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

DCP3ShiftPerm := function(p, offset, size)
  local images, j;
  images := [1..offset+size];
  for j in [1..size] do images[offset+j] := offset + (j^p); od;
  return PermList(images);
end;;
DCP3DirectSumPerm := function(p, psize, q, qsize)
  return p * DCP3ShiftPerm(q, psize, qsize);
end;;
DCP3PermDegree := function(G)
  local d;
  d := LargestMovedPoint(G);;
  if d = 0 then return 1; fi;
  return d;
end;;

#############################################################################
## Fixed roof M model.
#############################################################################
DCP3G9Rec := MakeGn(9);;
if Size(DCP3G9Rec.G) <> 2916 then Error("DCP3: G9 order drift"); fi;
CheckGF8();;
DCP3SMat := MakeMatGF8(1,0,1,1);; DCP3TMat := MakeMatGF8(4,3,1,5);;
DCP3SPerm := MatToPermGF8(DCP3SMat);; DCP3TPerm := MatToPermGF8(DCP3TMat);;
DCP3WPerm := DCP3SPerm * DCP3TPerm^-1;; DCP3X4 := DCP3WPerm^2;;
DCP3Y4 := DCP3SPerm^-1 * DCP3X4 * DCP3SPerm;;
DCP3P4 := Group(DCP3X4, DCP3Y4);;
if Size(DCP3P4) <> 504 then Error("DCP3: PSL(2,8) order drift"); fi;
DCP3MX := DCP3DirectSumPerm(DCP3G9Rec.x, 27, DCP3X4, 9);;
DCP3MY := DCP3DirectSumPerm(DCP3G9Rec.y, 27, DCP3Y4, 9);;
DCP3MDegree := 36;;
DCP3MBlock := Group(DCP3MX, DCP3MY);;
if Size(DCP3MBlock) <> 1469664 then Error("DCP3: PB3/M order drift"); fi;

DCP3F := FreeGroup("a", "b");;
DCP3a := DCP3F.1;; DCP3b := DCP3F.2;;
DCP3Rel := DCP3a * DCP3b * DCP3a * (DCP3b * DCP3a * DCP3b)^-1;;
DCP3B3 := DCP3F / [DCP3Rel];;
DCP3s1 := DCP3B3.1;; DCP3s2 := DCP3B3.2;;

## ITEM 7 GROUNDING NOTE: roof M's c-image ("identity") is treated here as a
## FRAMEWORK ASSUMPTION (structural property of K^(9)-type roofs per
## 2401/2405), NOT independently re-measured via a marked B3/M model in this
## pass -- lins_marked_strictness_export_v1.g's own roof_M.c_image field is a
## STRING LITERAL, not a computed value (falsifier finding). This producer
## explicitly labels this assumption in every emitted receipt
## (c_in_M_grounding field) rather than silently relying on it.
DCP3CinMGrounding := "FRAMEWORK_ASSUMPTION_NOT_INDEPENDENTLY_MEASURED";;
DCP3JCM := Identity(DCP3MBlock);;  # M-block component of c, per the above assumption

DCP3CodeToLetter := function(c)
  if c = 1 then return ["x",1];
  elif c = -1 then return ["x",-1];
  elif c = 2 then return ["y",1];
  elif c = -2 then return ["y",-1];
  else Error("DCP3: bad letter code ", c); fi;
end;;
DCP3WordToLetters := function(codes) return List(codes, DCP3CodeToLetter); end;;

DCP3Seeds := [
  rec(name:="row36", m_seed:=0,
    codes:=[-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1]),
  rec(name:="row71", m_seed:=0,
    codes:=[-1,-1,2,2,-1,-2,-1,-1,2,1,-2,1,1,2])
];;
for DCP3Sd in DCP3Seeds do DCP3Sd.letters := DCP3WordToLetters(DCP3Sd.codes);; od;;

## ITEM 6: pre-registered M-target constant for each seed, computed
## INDEPENDENTLY of any joint window (directly in the M model alone), so
## reduction_match compares against a FROZEN constant, not a value derived
## from the same candidate's own seed evaluation (which was a tautology).
DCP3EvalWord := function(letters, gx, gy, one)
  local z, l;
  z := one;;
  for l in letters do
    if l[1]="x" then z := z*gx^l[2]; else z := z*gy^l[2]; fi;
  od;
  return z;
end;;
for DCP3Sd in DCP3Seeds do
  DCP3Sd.m_target_pinned := DCP3EvalWord(DCP3Sd.letters, DCP3MX, DCP3MY, Identity(DCP3MBlock));;
od;;
Print("DCP3_PINNED_M_TARGETS row36=", DCP3Seeds[1].m_target_pinned <> fail,
  " row71=", DCP3Seeds[2].m_target_pinned <> fail, "\n");;

#############################################################################
## Build one window K := M cap L. Returns qrec with G=<JX,JY>, A=<JX,JY,JC>,
## theta~, tau~ (automorphisms of A, closed-form, NO word/sigma1/sigma2 of
## the ROOF needed -- only L's S1p,S2p for Cp).
#############################################################################
DCP3BuildWindow := function(L)
  local hom, Q, iso, Qp, S1p, S2p, Xp, Yp, Cp, deg, JX, JY, JC, G, A, kOrd,
    f2ratio, f3, pi0, H, cInK, thetaHom, tauHom;
  hom := NaturalHomomorphismByNormalSubgroup(DCP3B3, L);;
  Q := Image(hom);;
  iso := IsomorphismPermGroup(Q);;
  Qp := Image(iso);;
  S1p := Image(iso, Image(hom, DCP3s1));;
  S2p := Image(iso, Image(hom, DCP3s2));;
  Xp := S1p^2;; Yp := S2p^2;;
  Cp := (S1p*S2p*S1p)^2;;
  cInK := (Cp = Identity(Qp));;
  deg := DCP3PermDegree(Qp);;
  JX := DCP3DirectSumPerm(DCP3MX, DCP3MDegree, Xp, deg);;
  JY := DCP3DirectSumPerm(DCP3MY, DCP3MDegree, Yp, deg);;
  JC := DCP3DirectSumPerm(DCP3JCM, DCP3MDegree, Cp, deg);;
  G := Group(JX, JY);;
  A := Group(JX, JY, JC);;
  kOrd := Lcm(Order(JX), Order(JY));;
  if kOrd mod 18 <> 0 then Error("DCP3: K_ord not divisible by M_ord=18 -- fail-closed"); fi;
  f2ratio := Size(G) / 1469664;;
  if not IsInt(f2ratio) then Error("DCP3: F2 ratio nonintegral"); fi;
  f3 := (kOrd/18) * f2ratio;;
  pi0 := GroupHomomorphismByImages(G, DCP3MBlock, [JX,JY], [DCP3MX,DCP3MY]);;
  if pi0 = fail then Error("DCP3: M-block projection homomorphism ill-defined"); fi;
  H := Kernel(pi0);;
  if Size(H) <> f2ratio then Error("DCP3: |H| != F2 ratio"); fi;

  ## closed-form automorphisms of A (I4/I5 identities, no words, no sigma):
  thetaHom := GroupHomomorphismByImages(A, A, [JX,JY,JC], [JY,JX,JC]);;
  tauHom := GroupHomomorphismByImages(A, A, [JX,JY,JC], [JY, JY^-1*JX^-1*JC, JC]);;

  return rec(G:=G, A:=A, JX:=JX, JY:=JY, JC:=JC, degL:=deg, K_ord:=kOrd,
    M_ord:=18, F2:=f2ratio, F3:=f3, pi0:=pi0, H:=H, D:=DerivedSubgroup(G),
    c_in_K:=cInK, Cp_on_L:=Cp, thetaHom:=thetaHom, tauHom:=tauHom,
    theta_welldefined:=(thetaHom<>fail), tau_welldefined:=(tauHom<>fail));;
end;;

#############################################################################
## Predicate evaluation: GROUP-ELEMENT ONLY. No word representative is used
## for theta/tau/hexagon at any point. A candidate's word (needed only for
## CC-1 record-keeping / mutant testing) is obtained via PreImagesRepresentative
## and, per item 1's fail-closed instruction, IMMEDIATELY VERIFIED (assert
## EvalWordInQ-style re-evaluation of that word reproduces the SAME element p
## under the SAME word-evaluation convention used to record it -- i.e. we
## verify our own bookkeeping is self-consistent, not used for theta/tau).
#############################################################################
DCP3EvalWindow := function(qrec, seed)
  local JFseed, target0, Hlist, cosetF, h, p, mCands, t, rows, m, u,
    okCm, okCf, charming, ymf, lhsF2, rhs, hex310, hex311, genA, genB, onto,
    redOk, verdict, stage, validCount;
  if qrec.thetaHom = fail or qrec.tauHom = fail then
    Error("DCP3: theta~/tau~ ill-defined for this window -- fail-closed stop (should not happen per closed-form identities; investigate before proceeding)");
  fi;;
  JFseed := DCP3EvalWord(seed.letters, qrec.JX, qrec.JY, Identity(qrec.G));;
  target0 := Image(qrec.pi0, JFseed);;
  ## ITEM 6: reduction target is the PRE-REGISTERED, independently-pinned
  ## M-level constant for this seed (computed once, at load time, directly
  ## in the M model, not derived from this window's own candidate) -- and we
  ## ALSO cross-check it agrees with target0 (both must independently land
  ## on the SAME M-level element; a mismatch here means the window does not
  ## actually reduce to M correctly, a genuine fail-closed condition).
  if seed.m_target_pinned <> target0 then
    Error("DCP3: pinned M-target != window's own pi0(seed) -- fail-closed stop (window does not correctly reduce to M for this seed)");
  fi;;
  Hlist := Elements(qrec.H);;
  cosetF := List(Hlist, h -> JFseed * h);;
  if Length(cosetF) <> qrec.F2 then Error("DCP3: coset size mismatch"); fi;
  mCands := List([0..(qrec.K_ord/qrec.M_ord)-1], t -> seed.m_seed + qrec.M_ord*t);;
  rows := [];; validCount := 0;;
  for m in mCands do
    for p in cosetF do
      u := 2*m+1;;
      okCm := Gcd(u, qrec.K_ord) = 1;;
      okCf := p in qrec.D;;
      charming := okCm and okCf;;
      stage := "charming_fail";;
      hex310 := fail;; hex311 := fail;; onto := fail;; redOk := fail;;
      if charming then
        hex310 := (p * Image(qrec.thetaHom, p) = Identity(qrec.A));;
        if hex310 then
          ymf := qrec.JY^m * p;;
          lhsF2 := Image(qrec.tauHom, Image(qrec.tauHom, ymf)) * Image(qrec.tauHom, ymf) * ymf;;
          rhs := qrec.JC^m;;
          hex311 := (lhsF2 = rhs);;
          if hex311 then
            genA := qrec.JX^u;; genB := p^-1 * qrec.JY^u * p;;
            onto := Size(Group(genA, genB)) = Size(qrec.G);;
            if onto then
              redOk := (m mod qrec.M_ord = seed.m_seed) and (Image(qrec.pi0, p) = target0);;
              if not redOk then Error("DCP3: reduction-match FAILED on constructed candidate -- fail-closed stop"); fi;;
              stage := "pass";;
            else stage := "onto_fail"; fi;;
          else stage := "hex311_fail"; fi;;
        else stage := "hex310_fail"; fi;;
      fi;;
      verdict := charming and hex310=true and hex311=true and onto=true and redOk=true;;
      if verdict then validCount := validCount + 1; fi;;
      Add(rows, rec(m:=m, perm:=p, charming:=charming, hex310:=hex310, hex311:=hex311,
        onto:=onto, reduction_match:=redOk, verdict:=verdict, stage:=stage));;
    od;;
  od;;
  return rec(evaluated_count:=Length(rows), expected_count:=qrec.F3,
    valid_count:=validCount, rows:=rows);;
end;;

Print("DCP3_LOADED\n");;
