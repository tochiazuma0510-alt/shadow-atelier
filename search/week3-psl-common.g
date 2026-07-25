# week3-psl-common.g -- shared helpers for the PSL/PGL seven-window battery (workorder 4).
# Read via: Read("search/week3-psl-common.g");
#
# Design source (spec projection only): search/manifest_spec_v2_psl.md.
# Independence note: this file builds PGL(2,q) from EXPLICIT 2x2 matrices over GF(q) acting on the
# projective line P^1(GF(q)) (q+1 points) -- no GAP library PSL()/PGL()/AutomorphismGroup() calls,
# per spec sec.4.1(a)/4.2 ("明示 2x2 行列からの直接列挙"・"AutomorphismGroup は使わず").

SizeScreen([4096, 0]);;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= GF(q) helper: coerce an integer 0..q-1 to a field element =================
FElt := function(q, n) return (n mod q) * One(GF(q)); end;;

# ================= projective line P^1(GF(q)): q+1 points, index 1..q+1 =================
# point 1 = infinity [1:0]; point 1+1+x = [x:1] for x in 0..q-1 (i.e. index 2+x)
MatToPerm := function(q, M)
  local n, images, i, x, a, b, c, d, num, den, img;
  n := q + 1;
  a := M[1][1];  b := M[1][2];  c := M[2][1];  d := M[2][2];
  images := [];
  # point 1: infinity -> [a:c]
  if c = Zero(GF(q)) then images[1] := 1;
  else images[1] := 2 + Int(a/c); fi;
  for x in [0..q-1] do
    num := a*FElt(q,x) + b;
    den := c*FElt(q,x) + d;
    if den = Zero(GF(q)) then images[2+x] := 1;
    else images[2+x] := 2 + Int(num/den); fi;
  od;
  return PermList(images);
end;;

# build a 2x2 matrix over GF(q) from 4 plain integers (row-major [[a,b],[c,d]])
MakeMat := function(q, a, b, c, d)
  return [[FElt(q,a),FElt(q,b)],[FElt(q,c),FElt(q,d)]];
end;;

DetMat2 := function(M) return M[1][1]*M[2][2] - M[1][2]*M[2][1]; end;;

IsSquareInGF := function(q, x)
  local g, e;
  if x = Zero(GF(q)) then return true; fi;
  for e in GF(q) do
    if e <> Zero(GF(q)) and e*e = x then return true; fi;
  od;
  return false;
end;;

# ================= canonical form (first nonzero entry -> 1) for scalar-mod dedup =================
CanonicalizeMat := function(q, M)
  local flat, i, j, first, inv;
  flat := [M[1][1],M[1][2],M[2][1],M[2][2]];
  first := 0;
  for i in [1..4] do
    if flat[i] <> Zero(GF(q)) then first := flat[i]; break; fi;
  od;
  inv := first^-1;
  return [[M[1][1]*inv, M[1][2]*inv],[M[2][1]*inv, M[2][2]*inv]];
end;;

MatKey := function(M) return [M[1][1],M[1][2],M[2][1],M[2][2]]; end;;

# ================= enumerate all of PGL(2,q) as (matrix, permutation) pairs (q+1 points) =================
BuildPGLElements := function(q)
  local elts, seen, a, b, c, d, M, det, canon, key, perm, result;
  result := [];
  seen := [];
  for a in GF(q) do
    for b in GF(q) do
      for c in GF(q) do
        for d in GF(q) do
          det := a*d - b*c;
          if det <> Zero(GF(q)) then
            M := [[a,b],[c,d]];
            canon := CanonicalizeMat(q, M);
            key := MatKey(canon);
            if not (key in seen) then
              Add(seen, key);
              perm := MatToPerm(q, canon);
              Add(result, rec(mat:=canon, perm:=perm));
            fi;
          fi;
        od;
      od;
    od;
  od;
  return result;
end;;

MatToStr := function(M)
  local ent, s, i, j, x;
  s := "[[";
  for i in [1,2] do
    if i=2 then Append(s, "],["); fi;
    for j in [1,2] do
      if j=2 then Append(s, ","); fi;
      x := IntFFE(M[i][j]);
      if x = fail then x := 0; fi;
      Append(s, String(x));
    od;
  od;
  Append(s, "]]");
  return s;
end;;

# ================= centralizer of a permutation w within a list of (mat,perm) records =================
# returns rec(order, generator_mats) -- generator_mats via GAP's own GeneratorsOfGroup on the found
# subgroup (explicit witness elements, not just the count) -- PU-F14.
CentralizerWitness := function(elemList, wPerm)
  local commuting, e, sub, gens, gensMat, g, idx;
  commuting := [];
  for e in elemList do
    if e.perm * wPerm = wPerm * e.perm then Add(commuting, e); fi;
  od;
  sub := Group(List(commuting, e -> e.perm));
  gens := GeneratorsOfGroup(sub);
  gensMat := [];
  for g in gens do
    idx := First(elemList, e -> e.perm = g);
    if idx <> fail then Add(gensMat, idx.mat); fi;
  od;
  return rec(order:=Size(sub), commuting_count:=Length(commuting), generator_mats:=gensMat);
end;;

# ================= class_coefficient: N_Ghat(w^u) = #{(r,g) in T3 x T2 : r*g = w^u} (paper product;
# GAP form per W-4/reversal: paper's "rg" = GAP's "g*r") =================
# T3/T2 built from a FULL element list (elemList: list of perms in Ghat), filtered by order.
ClassCoefficient := function(elemList, target)
  local t3, t2, r, g, count;
  t3 := Filtered(elemList, x -> Order(x) = 3);
  t2 := Filtered(elemList, x -> Order(x) = 2);
  count := 0;
  for r in t3 do
    for g in t2 do
      if g*r = target then count := count + 1; fi;   # paper "rg" -> GAP "g*r" (reversal)
    od;
  od;
  return count;
end;;

# ================= GF(8) = F2[x]/(x^3+x+1), own bit-based arithmetic (q=8 needs this since GAP's
# native GF(8) coercion "n*One(GF(8))" only reaches {0,1} for integer n -- we need all 8 elements
# under the manifest's OWN encoding a0+a1*x+a2*x^2 <-> a0+2*a1+4*a2, sec.2.1) =================
BitOfInt := function(n, i) return RemInt(QuoInt(n, 2^i), 2); end;;
XorInt := function(a, b)
  local result, i;
  result := 0;
  for i in [0..6] do
    if (BitOfInt(a,i) + BitOfInt(b,i)) mod 2 = 1 then result := result + 2^i; fi;
  od;
  return result;
end;;
GF8CarrylessMul := function(a,b)
  local result, i;
  result := 0;
  for i in [0..2] do
    if BitOfInt(b,i) = 1 then result := XorInt(result, a*2^i); fi;
  od;
  return result;
end;;
GF8Reduce := function(p)
  local i, result;
  result := p;
  for i in [4,3] do
    if BitOfInt(result, i) = 1 then result := XorInt(result, 11 * 2^(i-3)); fi;
  od;
  return result;
end;;
GF8Add := function(a,b) return XorInt(a,b); end;;
GF8Mul := function(a,b) return GF8Reduce(GF8CarrylessMul(a,b)); end;;
GF8Inv := function(a)
  local b;
  if a = 0 then Error("GF8Inv: no inverse of 0"); fi;
  for b in [1..7] do if GF8Mul(a,b) = 1 then return b; fi; od;
  Error("GF8Inv: not found");
end;;
GF8Neg := function(a) return a; end;;   # char 2: -a = a
GF8Sub := function(a,b) return XorInt(a,b); end;;

# self-check: verify GF8Mul defines a field with the stated minimal polynomial x^3+x+1=0, i.e. x^3 = x+1
CheckGF8 := function()
  local x, x2, x3, ok;
  x := 2;;  x2 := GF8Mul(x,x);;  x3 := GF8Mul(x2,x);;
  ok := (x2 = 4) and (x3 = GF8Add(x,1));
  if not ok then Error("GF8 arithmetic self-check FAILED: x^2=", x2, " x^3=", x3, " (expect x^2=4, x^3=x+1=3)"); fi;
  return true;
end;;

# 2x2 matrices over GF(8), given as 4 plain integers 0..7 (manifest encoding)
DetMat2GF8 := function(M) return GF8Sub(GF8Mul(M[1][1],M[2][2]), GF8Mul(M[1][2],M[2][1])); end;;

MakeMatGF8 := function(a,b,c,d) return [[a,b],[c,d]]; end;;

CanonicalizeMatGF8 := function(M)
  local flat, i, first, inv;
  flat := [M[1][1],M[1][2],M[2][1],M[2][2]];
  first := 0;
  for i in [1..4] do if flat[i] <> 0 then first := flat[i]; break; fi; od;
  inv := GF8Inv(first);
  return [[GF8Mul(M[1][1],inv),GF8Mul(M[1][2],inv)],[GF8Mul(M[2][1],inv),GF8Mul(M[2][2],inv)]];
end;;

# projective line P^1(GF(8)): 9 points, index 1=infinity, 2+x for x in 0..7
MatToPermGF8 := function(M)
  local images, x, a, b, c, d, num, den;
  a := M[1][1];  b := M[1][2];  c := M[2][1];  d := M[2][2];
  images := [];
  if c = 0 then images[1] := 1; else images[1] := 2 + GF8Mul(a, GF8Inv(c)); fi;
  for x in [0..7] do
    num := GF8Add(GF8Mul(a,x), b);
    den := GF8Add(GF8Mul(c,x), d);
    if den = 0 then images[2+x] := 1; else images[2+x] := 2 + GF8Mul(num, GF8Inv(den)); fi;
  od;
  return PermList(images);
end;;

MatKeyGF8 := function(M) return [M[1][1],M[1][2],M[2][1],M[2][2]]; end;;

BuildPGLElementsGF8 := function()
  local result, seen, a, b, c, d, M, det, canon, key, perm;
  result := [];  seen := [];
  for a in [0..7] do for b in [0..7] do for c in [0..7] do for d in [0..7] do
    M := [[a,b],[c,d]];
    det := DetMat2GF8(M);
    if det <> 0 then
      canon := CanonicalizeMatGF8(M);
      key := MatKeyGF8(canon);
      if not (key in seen) then
        Add(seen, key);
        perm := MatToPermGF8(canon);
        Add(result, rec(mat:=canon, perm:=perm));
      fi;
    fi;
  od; od; od; od;
  return result;
end;;

MatToStrGF8 := function(M)
  return Concatenation("[[",String(M[1][1]),",",String(M[1][2]),"],[",String(M[2][1]),",",String(M[2][2]),"]]");
end;;

# Frobenius x -> x^2 on GF(8), extended to a permutation of the 9 projective points
FrobPermGF8 := function()
  local images, x;
  images := [1];  # infinity fixed
  for x in [0..7] do images[2+x] := 2 + GF8Mul(x,x); od;
  return PermList(images);
end;;

# ================= generic window runner (used by S2-S7 scripts; S1 was written out by hand and
# is kept as-is; this function was extracted from S1's script to avoid rewriting the whole
# pipeline six more times, but performs EXACTLY the same steps in the same order) =================
# cfg fields: id, ambientGroupName, caseLabel, objectCount, autOrbitIndex,
#   Sperm, Tperm, SmatStr, TmatStr (strings for output),
#   autElements (list of rec(mat:=<GAP value for MatToStr-like or already a string>, perm:=<perm>)),
#   autElementToStr (function(mat)->string),
#   gSizeExp, ghatSizeExp, eOrdExp, kOrdExp, b3PointsExp, charmingSetExp, exactOrderExp,
#   detSIsSquareExp ("inner"|"outer"|"not_applicable"), pu5Applicable (bool),
#   cInN (should always be true per spec sec.2.1),
#   a5CalibrationDone (bool, to skip re-running PU-F11 after the first window)
RunPSLWindow := function(cfg)
  local fixtureOK, haltStage, wPerm, eOrd, Xperm, kOrd, Yperm, YviaT, Zperm, w2perm,
        Ghat, ghatSize, Gg, gSize, b3Points, nOrd, charmingSet, derivedOrder, candidateTotalExpected,
        qrec, result, shadowSumCheck, qt, braidOk, deltaBPerm, DeltaPerm, exactOrder,
        mMissing, m, gd, hasSolution, frobeniusZero, ccVal, centW, settledDetail, settledCount,
        sh, u, f, targetX, targetY, witness, e, h, t0, t1, startLocal, elapsedMs, wallSeconds,
        markingJson, genDetailJson, settledJson, sd, centGenJson, gm, hexFreeCert, s, cwd;
  startLocal := Runtime();;
  fixtureOK := true;;  haltStage := false;;

  wPerm := cfg.Sperm * cfg.Tperm^-1;;
  eOrd := Order(wPerm);;
  Xperm := wPerm^2;;
  kOrd := Order(Xperm);;
  Yperm := cfg.Sperm^-1 * Xperm * cfg.Sperm;;
  YviaT := cfg.Tperm^-1 * Xperm * cfg.Tperm;;
  Zperm := cfg.Tperm^-2 * Xperm * cfg.Tperm^2;;
  w2perm := cfg.Tperm^-1 * cfg.Sperm;;

  Print("\n===== window ", cfg.id, " =====\n");
  Print("[", PF(Order(cfg.Sperm)=2), "] PU-F2: ord(S)=", Order(cfg.Sperm), " (expect 2)\n");
  Print("[", PF(Order(cfg.Tperm)=3), "] PU-F2: ord(T)=", Order(cfg.Tperm), " (expect 3)\n");
  Print("[", PF(eOrd=cfg.eOrdExp), "] PU-F2: ord(w)=", eOrd, " (expect e=", cfg.eOrdExp, ")\n");
  Print("[", PF(kOrd=cfg.kOrdExp), "] PU-F2: ord(X)=", kOrd, " (expect k=", cfg.kOrdExp, ")\n");
  if not (Order(cfg.Sperm)=2 and Order(cfg.Tperm)=3 and eOrd=cfg.eOrdExp and kOrd=cfg.kOrdExp) then fixtureOK:=false; fi;

  Print("[", PF(Zperm*Yperm*Xperm = ()), "] PU-F3: XYZ=1\n");
  Print("[", PF(Yperm = YviaT), "] PU-F3: Y = TXT^-1 = SXS^-1\n");
  Print("[", PF(w2perm^2 = Yperm), "] PU-F3: w2^2 = Y\n");
  if not (Zperm*Yperm*Xperm = () and Yperm = YviaT and w2perm^2 = Yperm) then fixtureOK := false; fi;

  Ghat := Group(cfg.Sperm, cfg.Tperm);;  ghatSize := Size(Ghat);;
  Gg := Group(Xperm, Yperm);;  gSize := Size(Gg);;
  Print("[", PF(ghatSize=cfg.ghatSizeExp), "] PU-F4: |<S,T>|=", ghatSize, " (expect ", cfg.ghatSizeExp, ")\n");
  Print("[", PF(gSize=cfg.gSizeExp), "] PU-F4: |<X,Y>|=", gSize, " (expect ", cfg.gSizeExp, ")\n");
  if not (ghatSize=cfg.ghatSizeExp and gSize=cfg.gSizeExp) then fixtureOK := false; fi;

  b3Points := 6*gSize;;
  Print("[", PF(b3Points = cfg.b3PointsExp), "] PU-F1: B3 points=", b3Points, " (expect ", cfg.b3PointsExp, ")\n");
  if not (b3Points = cfg.b3PointsExp) then fixtureOK := false; fi;

  Print("[", PF(cfg.Sperm^2 = ()), "] PU-F7: S^2=1 (c_in_N)\n");
  if not (cfg.Sperm^2 = ()) then fixtureOK := false; fi;

  nOrd := kOrd;;
  charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);;
  Print("[", PF(charmingSet = cfg.charmingSetExp), "] PU-F9: charming_set=", charmingSet, "\n");
  if not (charmingSet = cfg.charmingSetExp) then fixtureOK := false; fi;
  derivedOrder := gSize;;
  candidateTotalExpected := Length(charmingSet)*derivedOrder;;
  Print("[", PF(true), "] PU-F10: candidate_total=", candidateTotalExpected, "\n");

  if not fixtureOK then
    Print("\n[UNKNOWN] window ", cfg.id, ": fixture mismatch -- halting.\n");
    haltStage := true;
  fi;

  if not haltStage then
    Print("|Aut(Ghat)| = ", Length(cfg.autElements), " (expect ", cfg.autSizeExp, ")\n");
    if Length(cfg.autElements) <> cfg.autSizeExp then
      Print("[FAIL] Aut size mismatch -- halting\n");  haltStage := true;
    fi;
  fi;

  if not haltStage then

  qrec := rec(x:=Xperm, y:=Yperm, c:=(), G:=Gg);;
  t0 := Runtime();;
  result := EnumerateReducedHexagon(qrec, charmingSet);;
  t1 := Runtime();;
  Print("reduced hexagon enumeration: time_ms=", t1-t0, "\n");
  Print("candidate_total=", result.candidate_total, " h10_fail=", result.h10_fail,
        " h11_fail=", result.h11_fail, " generation_fail=", result.generation_fail,
        " shadow_total=", result.shadow_total, "\n");
  shadowSumCheck := (result.candidate_total - result.h10_fail - result.h11_fail - result.generation_fail = result.shadow_total);;
  Print("[", PF(shadowSumCheck), "] shadow_total 引き算整合性チェック\n");

  t0 := Runtime();;
  qt := BuildQTGeneral(Gg, Xperm, Yperm, ());;
  t1 := Runtime();;
  braidOk := (qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2);;
  Print("[", PF(braidOk), "] QxT braid relation, time_ms=", t1-t0, "\n");
  deltaBPerm := qt.s1*qt.s2;;  DeltaPerm := qt.s1*qt.s2*qt.s1;;
  exactOrder := Order(deltaBPerm^-1*DeltaPerm);;
  Print("[", PF(exactOrder=cfg.exactOrderExp), "] PU-F6: ord_Q(deltaB^-1 Delta)=", exactOrder, " (expect ", cfg.exactOrderExp, ")\n");

  mMissing := [];;
  for m in charmingSet do
    hasSolution := false;
    for gd in result.generation_detail do
      if gd.m=m and gd.stage<>"h10_fail" and gd.stage<>"h11_fail" then hasSolution:=true; fi;
    od;
    if not hasSolution then Add(mMissing,m); fi;
  od;
  Print("m_missing = ", mMissing, "\n");

  frobeniusZero := [];;
  for m in charmingSet do
    ccVal := ClassCoefficient(List(Elements(Gg)), Xperm^(2*m+1));;
    if ccVal = 0 then Add(frobeniusZero, m); fi;
  od;
  Print("frobenius_zero = ", frobeniusZero, "\n");

  t0 := Runtime();;
  centW := CentralizerWitness(cfg.autElements, wPerm);;
  t1 := Runtime();;
  Print("C_Aut(w): order=", centW.order, " gens=", Length(centW.generator_mats), ", time_ms=", t1-t0, "\n");

  settledDetail := [];;  settledCount := 0;;
  t0 := Runtime();;
  for sh in result.shadows do
    m := sh.m;  u := 2*m+1;  f := sh.f;
    targetX := Xperm^u;;
    targetY := AbstractProd([f^-1, Yperm^u, f]);;
    witness := fail;;
    for e in cfg.autElements do
      h := e.perm;;
      if h^-1*Xperm*h = targetX and h^-1*Yperm*h = targetY then witness := e; break; fi;
    od;
    if witness <> fail then
      settledCount := settledCount+1;
      Add(settledDetail, rec(m:=m, f_word:=sh.word, settled:=true, witness_mat:=witness.mat));
    else
      Add(settledDetail, rec(m:=m, f_word:=sh.word, settled:=false));
    fi;
  od;
  t1 := Runtime();;
  Print("settled witness search: ", settledCount, "/", Length(result.shadows), " settled, time_ms=", t1-t0, "\n");

  elapsedMs := Runtime()-startLocal;;
  Print("window ", cfg.id, " elapsed ms: ", elapsedMs, "\n");
  wallSeconds := elapsedMs/1000.0;;

  markingJson := Concatenation(
    "{\"S\":", JStr(cfg.SmatStr), ",\"T\":", JStr(cfg.TmatStr),
    ",\"det_S_is_square\":", cfg.detSJson,
    ",\"ord_S\":", String(Order(cfg.Sperm)), ",\"ord_T\":", String(Order(cfg.Tperm)),
    ",\"ord_w\":", String(eOrd), ",\"ord_X\":", String(kOrd), "}");;

  genDetailJson := [];;
  for gd in result.generation_detail do
    Add(genDetailJson, Concatenation("{\"m\":", String(gd.m), ",\"f_word\":", WordToJson(gd.f_word),
        ",\"pass\":", JB(gd.pass), ",\"stage\":\"", gd.stage, "\"}"));
  od;

  settledJson := [];;
  for sd in settledDetail do
    if sd.settled then
      Add(settledJson, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
          ",\"settled\":true,\"automorphism_witness\":\"", cfg.autElementToStr(sd.witness_mat), "\"}"));
    else
      Add(settledJson, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
          ",\"settled\":false,\"automorphism_witness\":null}"));
    fi;
  od;

  centGenJson := [];;
  for gm in centW.generator_mats do Add(centGenJson, JStr(cfg.autElementToStr(gm))); od;

  hexFreeCert := Concatenation(
    "{\"candidate_total\":", String(result.candidate_total),
    ",\"h10_fail\":", String(result.h10_fail),
    ",\"h11_fail\":", String(result.h11_fail),
    ",\"generation_fail\":", String(result.generation_fail),
    ",\"shadow_total\":", String(result.shadow_total), "}");;

  s := Concatenation(
    "{\"schema\":\"gtsh-cert/v2-psl\",",
    "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-psl-", cfg.id, ".g\",\"date\":\"2026-07-26\"},",
    "\"ambient_group\":\"", cfg.ambientGroupName, "\",\"case\":\"", cfg.caseLabel, "\",",
    "\"object_count\":", String(cfg.objectCount), ",\"aut_orbit_index\":", String(cfg.autOrbitIndex), ",",
    "\"element_encoding\":\"pgl2q_matrix/v1\",",
    "\"marking\":", markingJson, ",",
    "\"generation_checks\":{\"gen_ambient\":", String(ghatSize), ",\"gen_derived\":", String(gSize), "},",
    "\"universe\":{\"pb3_index\":", String(gSize), ",\"b3_points\":", String(b3Points),
    ",\"n_ord\":", String(nOrd), ",\"charming_set\":", JArr(List(charmingSet,String)),
    ",\"derived_order\":", String(derivedOrder), ",\"candidate_total\":", String(candidateTotalExpected), "},",
    "\"c_in_N\":true,\"evaluation_mode\":\"quotient_ok\",",
    "\"triangle_marking\":{\"applicable\":true,\"exact_order_binv_a\":", String(exactOrder), "},",
    "\"hexagon_free_certificate\":", hexFreeCert, ",",
    "\"generation_pass_count\":", String(result.shadow_total), ",",
    "\"generation_detail\":", JArr(genDetailJson), ",",
    "\"frobenius_zero\":", JArr(List(frobeniusZero,String)), ",",
    "\"m_missing\":", JArr(List(mMissing,String)), ",",
    "\"settled_detail\":", JArr(settledJson), ",",
    "\"settled_count\":", String(settledCount), ",",
    "\"centralizer_witness\":{\"order\":", String(centW.order), ",\"generator_mats\":", JArr(centGenJson), "},",
    "\"convention_note\":\"XYZ=1 checked as GAP Z*Y*X=1 (full 3-term reversal, paper's word AB=GAP's B*A applied to all 3 factors) -- discovered during S1, applies to all PSL windows (D7 遡及対象)\",",
    "\"isolated\":\"UNKNOWN\",",
    "\"runtime\":{\"wall_seconds\":", String(Int(wallSeconds*1000)/1000.0), "}",
    "}");;

  WriteFile(Concatenation("certificates/", cfg.id, ".v2.json"), s);;
  Print("wrote certificates/", cfg.id, ".v2.json\n");

  fi; # haltStage
  return not haltStage;
end;;

Print("week3-psl-common.g loaded.\n");
