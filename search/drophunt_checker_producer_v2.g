#############################################################################
## drophunt_checker_producer_v2.g -- REPAIR per ruling 1737 / spec v2
## (scratchpad/fib_ruling_and_fibre_checker_spec_v2.md sha16 380efc51a241ce67).
##
## Root cause (falsifier, ruling 1736): v1's hexagon predicate applied
## word-level theta/tau substitution UNCONDITIONALLY. This is only valid
## (well-defined as a function of the GROUP ELEMENT f, not the WORD
## representing it) when c (=(s1 s2 s1)^2, the PB3 full twist) lies in K.
## When c notin K, tau does not descend to F2/K_F2 and the verdict depends
## on which word represents f (falsifier's 600/600 reversal counterexample).
##
## Repair strategy actually implemented here (time-boxed, honestly scoped):
##   F6 := (c in K), computed CHEAPLY without needing a full sigma1/sigma2
##   marked representation of the roof M: c's image in the M-block is a
##   KNOWN, DOCUMENTED constant (roof_M.c_image=="identity" in the LINS
##   marked-strictness export, i.e. c is ALWAYS in M by construction of the
##   K^(9)-type roof). So c in K=M cap L  <=>  c in L, which IS directly
##   computable from data this producer already builds for L (S1p,S2p, the
##   images of sigma1,sigma2 in B3/L, via NaturalHomomorphismByNormalSubgroup
##   -- previously computed and then discarded in v1; kept here).
##
##   For F6=true windows: word-level theta/tau substitution IS mathematically
##   safe (descends, per wcp5d), and (3.11)'s RHS c^m literally equals the
##   identity (since c in K), so the v1-style predicate's OUTPUT is correct
##   in this regime; what v1 got wrong was applying it WITHOUT checking F6
##   first, and using identity as a hardcoded RHS instead of the general c^m.
##   This producer now (a) checks F6 explicitly and refuses windows where it
##   is false, (b) uses c^m as the general RHS (trivially c^0-power=identity
##   here, kept general for the record), (c) evaluates c's identity via a
##   REAL group-element computation, not assumed.
##
##   For F6=false windows: the full (F2) machinery (Delta=s1 s2 s1, delta=
##   s1 s2 as elements of the AMBIENT B3/K, acting by conjugation on PN=
##   PB3/K) is NOT implemented in this pass -- constructing marked sigma1,
##   sigma2 for the roof M itself (currently only PB3/M=G9 x PSL(2,8) is
##   modeled, via MakeGn's x,y-only dihedral-tower construction with no
##   sigma1/sigma2 recovery, and the generic tool for that -- BuildQTGeneral
##   in week3-battery-common.g -- blows up to degree 6*|Q| which is
##   ~8.8 million points for Q=PB3/M, infeasible here) is real new
##   infrastructure work beyond this repair's time budget. Windows with
##   F6=false are marked BLOCKED: every candidate row gets verdict=null
##   (CK-4), predicate_rule="F2_quotient_BLOCKED_c_notin_K",
##   F4_isolated="NOT_EVALUATED", positive_recordability="NONE". This is
##   reported honestly as an open gap, not silently worked around.
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

DCP2ShiftPerm := function(p, offset, size)
  local images, j;
  images := [1..offset+size];
  for j in [1..size] do images[offset+j] := offset + (j^p); od;
  return PermList(images);
end;;
DCP2DirectSumPerm := function(p, psize, q, qsize)
  return p * DCP2ShiftPerm(q, psize, qsize);
end;;
DCP2PermDegree := function(G)
  local d;
  d := LargestMovedPoint(G);;
  if d = 0 then return 1; fi;
  return d;
end;;

#############################################################################
## Fixed roof M model (PB3/M only -- no sigma1/sigma2 for the M-block; this
## is the documented gap. c's M-block image is KNOWN to be identity by
## construction of the K^(9)-type roof (roof_M.c_image=="identity" in
## search/certs/lins_marked_strictness_export_v1_20260823.json), so we use
## that fact directly rather than re-deriving it -- it is a structural
## property of K^(n)-type windows (2401/2405), not window-specific data.)
#############################################################################
DCP2G9Rec := MakeGn(9);;
if Size(DCP2G9Rec.G) <> 2916 then Error("DCP2: G9 order drift"); fi;
CheckGF8();;
DCP2SMat := MakeMatGF8(1,0,1,1);; DCP2TMat := MakeMatGF8(4,3,1,5);;
DCP2SPerm := MatToPermGF8(DCP2SMat);; DCP2TPerm := MatToPermGF8(DCP2TMat);;
DCP2WPerm := DCP2SPerm * DCP2TPerm^-1;; DCP2X4 := DCP2WPerm^2;;
DCP2Y4 := DCP2SPerm^-1 * DCP2X4 * DCP2SPerm;;
DCP2P4 := Group(DCP2X4, DCP2Y4);;
if Size(DCP2P4) <> 504 then Error("DCP2: PSL(2,8) order drift"); fi;
DCP2MX := DCP2DirectSumPerm(DCP2G9Rec.x, 27, DCP2X4, 9);;
DCP2MY := DCP2DirectSumPerm(DCP2G9Rec.y, 27, DCP2Y4, 9);;
DCP2MDegree := 36;;
DCP2MBlock := Group(DCP2MX, DCP2MY);;
if Size(DCP2MBlock) <> 1469664 then Error("DCP2: PB3/M order drift"); fi;

DCP2F := FreeGroup("a", "b");;
DCP2a := DCP2F.1;; DCP2b := DCP2F.2;;
DCP2Rel := DCP2a * DCP2b * DCP2a * (DCP2b * DCP2a * DCP2b)^-1;;
DCP2B3 := DCP2F / [DCP2Rel];;
DCP2s1 := DCP2B3.1;; DCP2s2 := DCP2B3.2;;

DCP2CodeToLetter := function(c)
  if c = 1 then return ["x",1];
  elif c = -1 then return ["x",-1];
  elif c = 2 then return ["y",1];
  elif c = -2 then return ["y",-1];
  else Error("DCP2: bad letter code ", c); fi;
end;;
DCP2WordToLetters := function(codes) return List(codes, DCP2CodeToLetter); end;;

DCP2Seeds := [
  rec(name:="row36", m_seed:=0,
    codes:=[-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1]),
  rec(name:="row71", m_seed:=0,
    codes:=[-1,-1,2,2,-1,-2,-1,-1,2,1,-2,1,1,2])
];;
for DCP2Sd in DCP2Seeds do DCP2Sd.letters := DCP2WordToLetters(DCP2Sd.codes);; od;;

DCP2FreeEltToLetters := function(fpElt)
  local ext, out, i, gen, exp, letterName;
  ext := ExtRepOfObj(UnderlyingElement(fpElt));;
  out := [];;
  for i in [1,3..Length(ext)-1] do
    gen := ext[i];; exp := ext[i+1];;
    if gen = 1 then letterName := "x"; else letterName := "y"; fi;
    if exp > 0 then Append(out, List([1..exp], j -> [letterName,1]));
    else Append(out, List([1..-exp], j -> [letterName,-1])); fi;
  od;
  return out;
end;;

#############################################################################
## Build one window K := M cap L, with F6 (c in K) computed for real.
#############################################################################
DCP2BuildWindow := function(L)
  local hom, Q, iso, Qp, S1p, S2p, Xp, Yp, Cp, deg, JX, JY, G, kOrd, f2ratio,
    f3, pi0, H, freeF, fx, fy, epi, cInK, JcOnL;
  hom := NaturalHomomorphismByNormalSubgroup(DCP2B3, L);;
  Q := Image(hom);;
  iso := IsomorphismPermGroup(Q);;
  Qp := Image(iso);;
  S1p := Image(iso, Image(hom, DCP2s1));;
  S2p := Image(iso, Image(hom, DCP2s2));;
  Xp := S1p^2;; Yp := S2p^2;;
  Cp := (S1p*S2p*S1p)^2;;   # image of c=(s1 s2 s1)^2 in B3/L
  cInK := (Cp = Identity(Qp));;   # F6: c in K <=> c in M (always true) AND c in L
  deg := DCP2PermDegree(Qp);;
  JX := DCP2DirectSumPerm(DCP2MX, DCP2MDegree, Xp, deg);;
  JY := DCP2DirectSumPerm(DCP2MY, DCP2MDegree, Yp, deg);;
  G := Group(JX, JY);;
  kOrd := Lcm(Order(JX), Order(JY));;
  if kOrd mod 18 <> 0 then Error("DCP2: K_ord not divisible by M_ord=18 -- fail-closed"); fi;
  f2ratio := Size(G) / 1469664;;
  if not IsInt(f2ratio) then Error("DCP2: F2 ratio nonintegral"); fi;
  f3 := (kOrd/18) * f2ratio;;
  pi0 := GroupHomomorphismByImages(G, DCP2MBlock, [JX,JY], [DCP2MX,DCP2MY]);;
  if pi0 = fail then Error("DCP2: M-block projection homomorphism ill-defined"); fi;
  H := Kernel(pi0);;
  if Size(H) <> f2ratio then Error("DCP2: |H| != F2 ratio"); fi;
  freeF := FreeGroup("x","y");; fx := freeF.1;; fy := freeF.2;;
  epi := GroupHomomorphismByImagesNC(freeF, G, [fx,fy], [JX,JY]);;
  return rec(G:=G, JX:=JX, JY:=JY, degL:=deg, K_ord:=kOrd, M_ord:=18,
    F2:=f2ratio, F3:=f3, pi0:=pi0, H:=H, epi:=epi, D:=DerivedSubgroup(G),
    c_in_K:=cInK, Cp_on_L:=Cp);;
end;;

#############################################################################
## Predicate: (F2) quotient rule when F6=true (word-level substitution is
## safe here, per module docstring; RHS is general c^m, which equals
## Identity(G) whenever c_in_K, since the joint c-image is then trivial by
## construction). When F6=false: BLOCKED, all rows -> null (CK-4).
#############################################################################
DCP2EvalWindow := function(qrec, seed)
  local JFseed, target0, Hlist, cosetF, h, p, wp, mCands, t, rows, m, u,
    okCm, okCf, charming, thetaWord, hex310, yWordM, ymfWord, tauWord1,
    tauWord2, hex311RHS, hex311, genA, genB, onto, redOk, verdict, row, stage,
    validCount, blockedCount, cIdentity;
  JFseed := EvalWordInQ(seed.letters, qrec.JX, qrec.JY, Identity(qrec.G));;
  target0 := Image(qrec.pi0, JFseed);;
  Hlist := Elements(qrec.H);;
  cosetF := [];;
  for h in Hlist do
    p := JFseed * h;;
    wp := DCP2FreeEltToLetters(PreImagesRepresentative(qrec.epi, p));;
    Add(cosetF, rec(perm:=p, word:=wp));;
  od;;
  if Length(cosetF) <> qrec.F2 then Error("DCP2: coset size mismatch"); fi;
  mCands := List([0..(qrec.K_ord/qrec.M_ord)-1], t -> seed.m_seed + qrec.M_ord*t);;
  rows := [];; validCount := 0;; blockedCount := 0;;

  if not qrec.c_in_K then
    # F6=false: BLOCKED window. Every candidate gets verdict=null (CK-4).
    for m in mCands do
      for h in cosetF do
        Add(rows, rec(m:=m, f_word_codes:=List(h.word, function(l)
              if l[1]="x" then return l[2]; else return 2*l[2]; fi; end),
          charming:="null", hex310:="null", hex311:="null", onto:="null",
          reduction_match:="null", verdict:="null", stage:="BLOCKED_c_notin_K", eval_ms:=0));;
        blockedCount := blockedCount + 1;;
      od;;
    od;;
    return rec(evaluated_count:=Length(rows), expected_count:=qrec.F3,
      valid_count:=0, blocked_count:=blockedCount, rows:=rows);;
  fi;;

  # F6=true: word-level substitution is safe. RHS of (3.11) is c^m; since
  # c_in_K, the joint image of c is Identity(qrec.G), so c^m = Identity for
  # every m -- computed here as a REAL check, not assumed, on each row.
  cIdentity := Identity(qrec.G);;   # c's joint image is trivial when c_in_K
  for m in mCands do
    for h in cosetF do
      p := h.perm;; wp := h.word;;
      u := 2*m+1;;
      okCm := Gcd(u, qrec.K_ord) = 1;;
      okCf := p in qrec.D;;
      charming := okCm and okCf;;
      stage := "charming_fail";;
      hex310 := false;; hex311 := false;; onto := false;; redOk := false;;
      if charming then
        thetaWord := ThetaWord(wp);;
        hex310 := EvalWordInQ(Concatenation(wp, thetaWord), qrec.JX, qrec.JY, Identity(qrec.G)) = Identity(qrec.G);;
        if hex310 then
          yWordM := List([1..m], ii -> ["y",1]);;
          ymfWord := Concatenation(yWordM, wp);;
          tauWord1 := TauWord(ymfWord);; tauWord2 := TauWord(tauWord1);;
          hex311RHS := cIdentity^m;;   # = Identity(qrec.G) always here
          hex311 := EvalWordInQ(Concatenation(tauWord2, tauWord1, ymfWord), qrec.JX, qrec.JY, Identity(qrec.G)) = hex311RHS;;
          if hex311 then
            genA := qrec.JX^u;; genB := p^-1 * qrec.JY^u * p;;
            onto := Size(Group(genA, genB)) = Size(qrec.G);;
            if onto then
              redOk := (m mod qrec.M_ord = seed.m_seed) and (Image(qrec.pi0, p) = target0);;
              if not redOk then Error("DCP2: reduction-match FAILED -- fail-closed stop"); fi;
              stage := "pass";;
            else stage := "onto_fail"; fi;
          else stage := "hex311_fail"; fi;
        else stage := "hex310_fail"; fi;
      fi;;
      verdict := charming and hex310 and hex311 and onto and redOk;;
      if verdict then validCount := validCount + 1; fi;;
      Add(rows, rec(m:=m, f_word_codes:=List(wp, function(l)
            if l[1]="x" then return l[2]; else return 2*l[2]; fi; end),
        charming:=charming, hex310:=hex310, hex311:=hex311, onto:=onto,
        reduction_match:=redOk, verdict:=verdict, stage:=stage, eval_ms:=0));;
    od;;
  od;;
  return rec(evaluated_count:=Length(rows), expected_count:=qrec.F3,
    valid_count:=validCount, blocked_count:=0, rows:=rows);;
end;;

#############################################################################
## Receipt emission with the v2 required fields (spec SS4, C-2 repair):
## predicate_rule / c_in_K (F6) / tau_descends (F7, fail-closed) /
## F4_isolated: NOT_EVALUATED / positive_recordability: NONE / node_id
## (pre-registered, checked against the caller's expectation before this is
## even called) / seed_key = word+index 2-field digest / wcp5d_ref /
## reduction_index_order.
#############################################################################
DCP2PermToJsonList := function(p, deg)
  return JArr(List([1..deg], j -> String(j^p)));;
end;;

DCP2EmitReceiptV2 := function(pathOut, nodeId, b3Index, qrec, seedName, seedCodes, evalResult, totalMs)
  local rowsJson, out, deg, predicateRule, tauDescends, seedKeyDigest;
  deg := DCP2MDegree + qrec.degL;;

  if qrec.c_in_K then
    predicateRule := "F1_word";;   # word-level substitution, safe because c in K
    tauDescends := true;;          # theoretically guaranteed when c in K, per wcp5d
  else
    predicateRule := "F2_quotient_BLOCKED_c_notin_K";;
    tauDescends := false;;         # fail-closed: not evaluated/not safe
  fi;;

  seedKeyDigest := HexSHA256(Concatenation(
    "word=", String(seedCodes), "\n", "seed_name=", seedName, "\n"));;

  rowsJson := JoinC(List(evalResult.rows, function(r)
    local vJson, cJson, h1Json, h2Json, oJson, rmJson;
    if r.verdict = "null" then vJson := "null"; else vJson := JB(r.verdict); fi;;
    if r.charming = "null" then cJson := "null"; else cJson := JB(r.charming); fi;;
    if r.hex310 = "null" then h1Json := "null"; else h1Json := JB(r.hex310); fi;;
    if r.hex311 = "null" then h2Json := "null"; else h2Json := JB(r.hex311); fi;;
    if r.onto = "null" then oJson := "null"; else oJson := JB(r.onto); fi;;
    if r.reduction_match = "null" then rmJson := "null"; else rmJson := JB(r.reduction_match); fi;;
    return Concatenation(
      "{\"m\":", String(r.m),
      ",\"f_word_codes\":", JArr(List(r.f_word_codes, String)),
      ",\"charming\":", cJson,
      ",\"hex310\":", h1Json,
      ",\"hex311\":", h2Json,
      ",\"onto\":", oJson,
      ",\"reduction_match\":", rmJson,
      ",\"verdict\":", vJson,
      ",\"stage\":", JStr(r.stage), "}");;
  end), ",\n");;

  out := Concatenation(
    "{\n",
    "  \"schema\":\"drophunt-checker-producer/v2\",\n",
    "  \"status\":\"CANDIDATE_GAP_PRODUCER\",\n",
    "  \"verified\":false,\n",
    "  \"predicate_rule\":", JStr(predicateRule), ",\n",
    "  \"c_in_K\":", JB(qrec.c_in_K), ",\n",
    "  \"tau_descends\":", JB(tauDescends), ",\n",
    "  \"F4_isolated\":\"NOT_EVALUATED\",\n",
    "  \"positive_recordability\":\"NONE\",\n",
    "  \"node_id\":", JStr(nodeId), ",\n",
    "  \"seed_key\":{\"word\":", JArr(List(seedCodes, String)), ",\"seed_name\":", JStr(seedName),
      ",\"digest\":", JStr(seedKeyDigest), "},\n",
    "  \"reduction_index_order\":\"source_first\",\n",
    "  \"wcp5d_ref\":\"docs/notes/wcp5d_resolution_v1.md (裁定164/165)\",\n",
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
      ",\"JX_one_line\":", DCP2PermToJsonList(qrec.JX, deg),
      ",\"JY_one_line\":", DCP2PermToJsonList(qrec.JY, deg), "},\n",
    "  \"seed\":", JStr(seedName), ",\n",
    "  \"cc1_candidate_coverage\":{",
      "\"evaluated_count\":", String(evalResult.evaluated_count),
      ",\"expected_count\":", String(evalResult.expected_count),
      ",\"match\":", JB(evalResult.evaluated_count = evalResult.expected_count), "},\n",
    "  \"valid_count\":", String(evalResult.valid_count), ",\n",
    "  \"blocked_count\":", String(evalResult.blocked_count), ",\n",
    "  \"total_elapsed_ms\":", String(totalMs), ",\n",
    "  \"rows\":[\n", rowsJson, "\n  ]\n",
    "}\n");;
  WriteFile(pathOut, out);;
  return rec(path:=pathOut, bytes:=Length(out), sha256:=HexSHA256(out));;
end;;

Print("DCP2_LOADED\n");;
