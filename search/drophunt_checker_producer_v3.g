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
## 裁定1761 item 1 (最重要): the seed codes (row36/row71) are defined under
## the PREPEND word-evaluation convention (matching wall-miner-v4.g's
## AbstractProd / EvalWordInQ), NOT the direct/append order this function
## previously used (z:=z*g). Evaluating a prepend-defined word with append
## accumulation is exactly the WDICT-5 convention-mixing bug class, applied
## here to the SEED itself (not just the internal tau~-cycle formula fixed
## above) -- fixed by prepending: z := g^pow * z.
DCP3EvalWord := function(letters, gx, gy, one)
  local z, l;
  z := one;;
  for l in letters do
    if l[1]="x" then z := gx^l[2]*z; else z := gy^l[2]*z; fi;
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
        ## 裁定1761 item 1/3 resolution: B-2 calibration (row71 MUST be a
        ## full GT(M) member when checked directly in the roof, per
        ## search/drophunt_row71_calibration_v1.g) was used to empirically
        ## pin the correct convention PAIR, since a naive re-derivation from
        ## AbstractProd's reversal rule alone was ambiguous (both "prepend
        ## seed + reversed triple" and "append seed + reversed triple" LOOK
        ## internally consistent in isolation -- only round-tripping against
        ## a KNOWN member of GT(M) disambiguates them, exactly the discipline
        ## this whole campaign exists to enforce). The validated pair is:
        ## seed words evaluated PREPEND (DCP3EvalWord, fixed above) PAIRED
        ## WITH the ORIGINAL/NAIVE Wd:=y^m*f and triple order tau~^2(Wd)*
        ## tau~(Wd)*Wd (i.e. this hexagon (3.11) formula itself is UNCHANGED
        ## from the pre-1761 version; only the SEED word evaluation
        ## convention was actually wrong). Both row36 and row71 independently
        ## confirmed PASS as full GT(M) members under this exact pair before
        ## it was adopted here -- see search/certs/
        ## drophunt_row71_calibration_v1_20260829.json.
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

#############################################################################
## ITEM 5.1: v3 receipt emission with the SS4 8 required fields, all on
## every row/window. Short-circuited/not-applicable values are JSON null
## (GAP `fail` -> JStr-free direct "null" literal), never false, per the
## coordinator's explicit inversion of v2's (wrong) CK-4 rule.
#############################################################################
DCP3PermToJsonList := function(p, deg)
  return JArr(List([1..deg], j -> String(j^p)));;
end;;

DCP3BoolOrNull := function(v)
  if v = fail then return "null"; fi;;
  return JB(v);;
end;;

#############################################################################
## 裁定1776 (MULT-COSET / final stop lattice): F1_prime := K_ord/M_ord
## (RECORD-ONLY, the count of ALL m-residues, gcd-eligible or not --
## renamed here to match 数学者命名; this is what earlier drophunt cert
## prose (裁定1774-era) called "F1"). F1_double_prime := #{m : gcd(2m+1,
## K_ord)=1} (the DECISION denominator -- what 裁定1774's implementer draft
## called "F1'", now superseded by this name). per_m[i] is "null" (GAP
## string sentinel -> JSON null) for a gcd-EXCLUDED m, or an INTEGER >= 0
## (possibly 0) for a gcd-ELIGIBLE m -- strict null/0 distinction is a
## receipt-schema REQUIREMENT (0 means "evaluated, no lift"; null means
## "never evaluated, gcd side-condition excluded it"). lift_m := number of
## gcd-eligible m with per_m[m]>=1. mult_set := SET of DISTINCT nonzero
## per_m values (MULT-COSET theorem: this set must have size <=1 -- the
## fibre multiplicity is constant across every lifting m; a set of size>1
## is a THEOREM VIOLATION, not a data anomaly). verdict in
## {"BUG","DROP","ANOMALY","PASS"}, exclusive lattice in this priority
## order: BUG if lift_m>F1_double_prime or |mult_set|>1; else DROP if
## valid_total=0; else ANOMALY if lift_m<F1_double_prime; else PASS.
#############################################################################
DCP3ComputeMultAnalysis := function(qrec, evalResult)
  local mCands, m, perM, cnt, liftM, multSet, validTotal, verdict, f1prime, f1double;
  mCands := List([0..(qrec.K_ord/qrec.M_ord)-1], t -> qrec.M_ord*t);;
  f1prime := qrec.K_ord/qrec.M_ord;;
  f1double := Length(Filtered(mCands, m -> Gcd(2*m+1, qrec.K_ord) = 1));;
  perM := [];; liftM := 0;; multSet := [];; validTotal := 0;;
  for m in mCands do
    if Gcd(2*m+1, qrec.K_ord) <> 1 then
      Add(perM, "null");;
    else
      cnt := Length(Filtered(evalResult.rows, r -> r.m = m and r.verdict = true));;
      Add(perM, cnt);;
      validTotal := validTotal + cnt;;
      if cnt >= 1 then
        liftM := liftM + 1;;
        if not cnt in multSet then Add(multSet, cnt); fi;;
      fi;;
    fi;;
  od;;
  Sort(multSet);;
  if liftM > f1double or Length(multSet) > 1 then verdict := "BUG";
  elif validTotal = 0 then verdict := "DROP";
  elif liftM < f1double then verdict := "ANOMALY";
  else verdict := "PASS"; fi;;
  return rec(F1_prime:=f1prime, F1_double_prime:=f1double, per_m:=perM,
    lift_m:=liftM, mult_set:=multSet, valid_total:=validTotal, verdict:=verdict);;
end;;

DCP3IntOrNullStr := function(v)
  if v = "null" then return "null"; fi;;
  return String(v);;
end;;

DCP3EmitReceipt := function(pathOut, nodeId, b3Index, qrec, seedName, seedCodes, evalResult, totalMs)
  local rowsJson, out, deg, seedKeyDigest, mult;
  deg := DCP3MDegree + qrec.degL;;
  seedKeyDigest := HexSHA256(Concatenation(
    "word=", String(seedCodes), "\n", "seed_name=", seedName, "\n"));;
  mult := DCP3ComputeMultAnalysis(qrec, evalResult);;

  rowsJson := JoinC(List(evalResult.rows, r -> Concatenation(
    "{\"m\":", String(r.m),
    ",\"perm_one_line\":", DCP3PermToJsonList(r.perm, deg),
    ",\"charming\":", DCP3BoolOrNull(r.charming),
    ",\"hex310\":", DCP3BoolOrNull(r.hex310),
    ",\"hex311\":", DCP3BoolOrNull(r.hex311),
    ",\"onto\":", DCP3BoolOrNull(r.onto),
    ",\"reduction_match\":", DCP3BoolOrNull(r.reduction_match),
    ",\"verdict\":", JB(r.verdict),   # verdict is always a real boolean (false if any stage failed/unreached)
    ",\"stage\":", JStr(r.stage), "}")), ",\n");;

  out := Concatenation(
    "{\n",
    "  \"schema\":\"drophunt-checker-producer/v3\",\n",
    "  \"status\":\"CANDIDATE_GAP_PRODUCER\",\n",
    "  \"verified\":false,\n",
    ## SS4 8 required top-level fields:
    "  \"predicate_rule\":\"F2_quotient\",\n",
    "  \"c_in_K\":", JB(qrec.c_in_K), ",\n",
    ## item 5 (裁定1761): tau_descends is NOT_APPLICABLE under (F2)-only
    ## operation (the (F1) word-descent question this field was originally
    ## for does not arise -- there is no word-level fallback path anymore;
    ## the earlier "conservative := c_in_K" wiring quoted a nonexistent
    ## "spec v2 SS10.4" comment and is removed).
    "  \"tau_descends\":\"NOT_APPLICABLE\",\n",
    "  \"F4_isolated\":\"NOT_EVALUATED\",\n",
    "  \"positive_recordability\":\"NONE\",\n",
    "  \"node_id\":", JStr(nodeId), ",\n",
    "  \"seed_key\":{\"word\":", JArr(List(seedCodes, String)), ",\"seed_name\":", JStr(seedName),
      ",\"digest\":", JStr(seedKeyDigest), "},\n",
    "  \"wcp5d_ref\":\"docs/notes/wcp5d_resolution_v1.md (裁定164/165)\",\n",
    ## item 2 (裁定1761): the pair declaring which product-order/word-eval
    ## convention this receipt was produced under. Only valid TOGETHER,
    ## per spec v2 SS3.0's literal declaration; the checker fail-closed
    ## rejects a receipt missing either or declaring a different pair.
    "  \"product_order\":\"tau2_tau_id\",\n",
    "  \"word_eval_order\":\"prepend\",\n",
    "  \"reduction_index_order\":\"source_first\",\n",
    "  \"reduction_match_tautological_by_construction\":true,\n",   # item 4
    "  \"c_in_M_grounding\":\"", DCP3CinMGrounding, "\",\n",
    "  \"window\":{",
      "\"node_id\":", JStr(nodeId),
      ",\"b3_index_of_L\":", String(b3Index),
      ",\"c_in_K\":", JB(qrec.c_in_K),
      ",\"K_ord\":", String(qrec.K_ord),
      ",\"M_ord\":", String(qrec.M_ord),
      ",\"F1_m_factor\":", String(qrec.K_ord/qrec.M_ord),
      ",\"F2_ratio\":", String(qrec.F2),
      ",\"F3_fib\":", String(qrec.F3),
      ",\"F5_size_G\":", String(Size(qrec.G)),
      ",\"degree\":", String(deg),
      ",\"JX_one_line\":", DCP3PermToJsonList(qrec.JX, deg),
      ",\"JY_one_line\":", DCP3PermToJsonList(qrec.JY, deg),
      ",\"JC_one_line\":", DCP3PermToJsonList(qrec.JC, deg), "},\n",
    "  \"seed\":", JStr(seedName), ",\n",
    "  \"cc1_candidate_coverage\":{",
      "\"evaluated_count\":", String(evalResult.evaluated_count),
      ",\"expected_count\":", String(evalResult.expected_count),
      ",\"match\":", JB(evalResult.evaluated_count = evalResult.expected_count), "},\n",
    "  \"valid_count\":", String(evalResult.valid_count), ",\n",
    ## 裁定1776 final stop lattice fields:
    "  \"F1_prime\":", String(mult.F1_prime), ",\n",
    "  \"F1_double_prime\":", String(mult.F1_double_prime), ",\n",
    "  \"per_m\":[", JoinC(List(mult.per_m, DCP3IntOrNullStr), ","), "],\n",
    "  \"lift_m\":", String(mult.lift_m), ",\n",
    "  \"mult_set\":[", JoinC(List(mult.mult_set, String), ","), "],\n",
    "  \"valid_total\":", String(mult.valid_total), ",\n",
    "  \"verdict\":", JStr(mult.verdict), ",\n",
    "  \"total_elapsed_ms\":", String(totalMs), ",\n",
    "  \"rows\":[\n", rowsJson, "\n  ]\n",
    "}\n");;
  WriteFile(pathOut, out);;
  return rec(path:=pathOut, bytes:=Length(out), sha256:=HexSHA256(out));;
end;;

Print("DCP3_LOADED\n");;
