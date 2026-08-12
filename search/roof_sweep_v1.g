# search/roof_sweep_v1.g -- 異族屋根一括掃討(裁定1059)
#
# 正本: docs/notes/ideas_cex_structure_v1.md 札I-CEX-1 §3(空白の系統列挙)。
# 陽性対照(972屋根 M=K^(9) cap N_S4)を同一コード経路で再現してから、K(n)(n=3,9,15,21,27,
# 33,81)x{1152系2窓} + S4 x{1152系2窓} = 16本の異族屋根を掃討する。
# 各屋根: cap 600秒(超過はUNKNOWN記録・次へ)・構築後 shadow_total・Frattini行
#   (|X|・|Φ|・|X/Φ|)・crown類census(件数・正規/非正規内訳)を記録。checkpoint方式
#   (1本終わるごとにcert書き出し)。
#
# 847依存監査: MakeGn/ScanRoofHexagon/BuildShadowCompositionRegularRep/BuildOneClassTest等は
#   crown_battery_v1.g・crown_battery_targets_v1.g・ihnec_r4b_run.g(裁定376)と同一パターンの
#   再利用(既存確立済み計器)。BuildWindowFromWordsはiso_census83_deep15_v1.g(裁定986)から。

SizeScreen([4096, 0]);;
Read("search/probe/wac_v1/gap_output_prelude.g");;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ---- (F2) machinery, verbatim pattern (wall-miner-v4.g / iso_census83_deep15_v1.g) ----
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

BF3 := FreeGroup("a", "b");;
brelD := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;
B3 := BF3 / [brelD];;
ga := B3.1;;  gb := B3.2;;
a := ga;;  b := gb;;

BuildWindowFromWords := function(indexExpected, words)
  local genElts, N, idxOk, isNormal, hm, Gimg, isoQ, s1, s2;
  genElts := List(words, w -> EvalString(w));;
  N := Subgroup(B3, genElts);;
  idxOk := (Index(B3, N) = indexExpected);;
  isNormal := IsNormal(B3, N);;
  if not (idxOk and isNormal) then Error("BuildWindowFromWords: mismatch"); fi;
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  Gimg := Image(hm);;
  isoQ := IsomorphismPermGroup(Gimg);;
  s1 := Image(isoQ, Image(hm, ga));;
  s2 := Image(isoQ, Image(hm, gb));;
  return MakeWindow(s1, s2);;
end;;

# ---- ScanRoofHexagon with 600s per-roof budget (self-contained timer) ----
ScanRoofHexagonCapped := function(qrec, charmingSet, capSeconds)
  local G, D, Delts, thetaHom, tauHom, zElt, h10Fail, h11Fail, genFail, shadows,
        m, u, f, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj,
        candidateTotal, i, t0, capped, checkEvery, counter;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  # self-caught (roof_sweep_v1.g, 裁定1059中に発見・K(3) x 1152[b] roofで実際に発生):
  # theta(x<->y の入替)・tau(x->y,y->(xy)^-1)がこの特定の合成roof群G上で自己同型として
  # well-defined とは限らない(ihnec_r4b_run.gが検算済みの972屋根では通ったが、一般には
  # 保証されない)。fail のまま Image(thetaHom,...) を呼ぶと "<map> must be a general
  # mapping" でGAPがクラッシュする -- ここでガードし、このroofをtheta/tau非well-defined
  # として fail-closed に UNKNOWN 報告する(次のroofへ継続)。
  if thetaHom = fail or tauHom = fail then
    return rec(candidate_total := 0, shadow_total := 0, shadows := [],
               derived_order := 0, capped := false,
               theta_tau_not_well_defined := true,
               elapsed_seconds := 0.0);;
  fi;
  D := DerivedSubgroup(G);
  Delts := Elements(D);
  h10Fail := 0;  h11Fail := 0;  genFail := 0;  shadows := [];
  candidateTotal := Length(Delts) * Length(charmingSet);
  t0 := GAPLIB_WallElapsedMs();;
  capped := false;;
  checkEvery := 200;;  counter := 0;;
  for m in charmingSet do
    u := 2*m + 1;
    for i in [1 .. Length(Delts)] do
      counter := counter + 1;;
      if counter mod checkEvery = 0 then
        if (GAPLIB_WallElapsedMs() - t0) / 1000.0 > capSeconds then
          capped := true;;
          break;;
        fi;
      fi;
      f := Delts[i];
      thetaf := Image(thetaHom, f);
      hex310 := AbstractProd([f, thetaf]) = Identity(G);
      if not hex310 then h10Fail := h10Fail + 1; continue; fi;
      ymf := AbstractProd([qrec.y^m, f]);
      tauymf := Image(tauHom, ymf);
      tau2ymf := Image(tauHom, tauymf);
      hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(G);
      if not hex311 then h11Fail := h11Fail + 1; continue; fi;
      genA := qrec.x^u;
      genB := AbstractProd([f^-1, qrec.y^u, f]);
      surj := Size(Group(genA, genB)) = Size(G);
      if not surj then genFail := genFail + 1;
      else Add(shadows, rec(m := m, f := f)); fi;
    od;
    if capped then break; fi;
  od;
  return rec(candidate_total := candidateTotal, shadow_total := Length(shadows), shadows := shadows,
             derived_order := Length(Delts), capped := capped,
             theta_tau_not_well_defined := false,
             elapsed_seconds := (GAPLIB_WallElapsedMs() - t0)/1000.0);;
end;;

BuildRegularPermGroupFromTable := function(tbl, n)
  local prod, e, gens, aa, images, bb;
  prod := List([0..n-1], i -> List([0..n-1], j -> -1));;
  for e in tbl do prod[e[1]+1][e[2]+1] := e[3]; od;;
  gens := [];;
  for aa in [0..n-1] do
    images := List([0..n-1], bb -> prod[aa+1][bb+1] + 1);;
    Add(gens, PermList(images));;
  od;
  return Group(gens);;
end;;

BuildShadowCompositionRegularRep := function(qrec, shadowPairsOrRecs, Nord)
  local n, i1, i2, m1, f1, m2, f2, u1, Ehom, newm, newf, idx, t, tbl, closureFail, regGrp,
        idxDict, key, shadows, notWellDefinedCount;
  if Length(shadowPairsOrRecs) > 0 and IsBound(shadowPairsOrRecs[1].m) then
    shadows := shadowPairsOrRecs;;
  else
    shadows := List(shadowPairsOrRecs, p -> rec(m := p[1], f := p[2]));;
  fi;
  n := Length(shadows);;
  tbl := [];;  closureFail := 0;;
  idxDict := NewDictionary([shadows[1].m, shadows[1].f], true);;
  for t in [1..n] do AddDictionary(idxDict, [shadows[t].m, shadows[t].f], t);; od;
  notWellDefinedCount := 0;;
  for i1 in [1..n] do
    m1 := shadows[i1].m;;  f1 := shadows[i1].f;;  u1 := 2*m1+1;;
    Ehom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y],
              [qrec.x^u1, AbstractProd([f1^-1, qrec.y^u1, f1])]);;
    if Ehom = fail then
      # self-caught (roof_sweep_v1.g, 裁定1059中に発見): ScanRoofHexagon/ScanRoofHexagonCapped
      # の3条件(hex310・hex311・generation)だけでは well-definedness を保証しない
      # (kerchi-judge.g KJ-1 修理・裁定169 と同型の穴)。ここで初めて GAP が実際に検出する
      # ケースが出た(K(3) x 1152[b] roof) -- crash させず「この shadow は非 well-defined」
      # として closure failure に計上し、そのroofはUNKNOWNとして報告(fail-closed継続)。
      notWellDefinedCount := notWellDefinedCount + 1;;
      closureFail := closureFail + 1;;
      for i2 in [1..n] do Add(tbl, [i1-1, i2-1, -1]);; od;
      continue;;
    fi;
    for i2 in [1..n] do
      m2 := shadows[i2].m;;  f2 := shadows[i2].f;;
      newm := (2*m1*m2 + m1 + m2) mod Nord;;
      newf := AbstractProd([f1, Image(Ehom, f2)]);;
      key := [newm, newf];;
      idx := LookupDictionary(idxDict, key);;
      if idx = fail then closureFail := closureFail + 1;; Add(tbl, [i1-1, i2-1, -1]);;
      else Add(tbl, [i1-1, i2-1, idx-1]);; fi;
    od;
  od;
  if closureFail > 0 then
    return rec(regGrp:=fail, closed_observed:=false, closure_fail_count:=closureFail,
               not_well_defined_count:=notWellDefinedCount);;
  fi;
  regGrp := BuildRegularPermGroupFromTable(tbl, n);;
  return rec(regGrp:=regGrp, closed_observed:=true, closure_fail_count:=0);;
end;;

# ---- crown battery (self-caught closure-bug-fixed pattern) ----
BuildOneClassTest := function(Xbar, classId, cls)
  local Mc, coreC, indexC, normalC, quotHom, Qc, McImageInQc, cosetActHom, testFn;
  Mc := Representative(cls);;
  coreC := Core(Xbar, Mc);;
  indexC := Index(Xbar, Mc);;
  normalC := (coreC = Mc);;
  quotHom := NaturalHomomorphismByNormalSubgroup(Xbar, coreC);;
  Qc := Image(quotHom);;
  McImageInQc := Image(quotHom, Mc);;
  if normalC then
    testFn := function(A) return IsTrivial(Image(quotHom, A));; end;;
  else
    cosetActHom := FactorCosetAction(Qc, McImageInQc);;
    testFn := function(A)
      local Aimg, AimgPerm, deg;
      Aimg := Image(quotHom, A);;
      AimgPerm := Image(cosetActHom, Aimg);;
      deg := Index(Qc, McImageInQc);;
      return ForAny([1..deg], pt -> ForAll(GeneratorsOfGroup(AimgPerm), gg -> pt^gg = pt));;
    end;;
  fi;
  return rec(class_id := classId, index := indexC, normal := normalC,
             core_order := Size(coreC), quotient_order := Size(Qc),
             representative := Mc, quotient_abelian := IsAbelian(Qc),
             test_type := "maximal-class", test := testFn);;
end;;

BuildCrownBattery := function(Xbar)
  local classes, n;
  classes := ConjugacyClassesMaximalSubgroups(Xbar);;
  n := Length(classes);;
  return rec(Xbar := Xbar, n_classes := n,
             entries := List([1..n], i -> BuildOneClassTest(Xbar, i, classes[i])));;
end;;

CalibrateCrownBattery := function(battery)
  local n, matrix, i, j, Mc, val, allDiagOk, offDiagFail, calibOk;
  n := battery.n_classes;;
  matrix := List([1..n], i -> List([1..n], j -> fail));;
  offDiagFail := 0;;
  for i in [1..n] do
    Mc := battery.entries[i].representative;;
    for j in [1..n] do
      val := battery.entries[j].test(Mc);;
      matrix[i][j] := val;;
      if i <> j and val = true then offDiagFail := offDiagFail + 1;; fi;
    od;
  od;
  allDiagOk := ForAll([1..n], i -> matrix[i][i] = true);;
  calibOk := allDiagOk and (offDiagFail = 0);;
  return rec(diag_all_true := allDiagOk, off_diagonal_fail_count := offDiagFail, calibration_ok := calibOk);;
end;;

# ---- window builders ----
ShiftPerm := function(p, offset, size)
  local l, j;
  l := [1 .. offset+size];
  for j in [1 .. size] do l[offset+j] := offset + (j^p); od;
  return PermList(l);
end;;
DirectSumPerm := function(p1, deg1, p2, deg2) return p1 * ShiftPerm(p2, deg1, deg2); end;;

BuildKWindow := function(n)
  local g;
  g := MakeGn(n);;
  return rec(x := g.x, y := g.y, G := g.G, degree := 3*n, label := Concatenation("K(", String(n), ")"));;
end;;

s4cache := fail;;
BuildS4Window := function()
  local Smat, Tmat, Sperm, Tperm, wPerm, Xperm, Yperm, Pgrp;
  if s4cache <> fail then return s4cache; fi;
  CheckGF8();;
  Smat := MakeMatGF8(1,0,1,1);;  Tmat := MakeMatGF8(4,3,1,5);;
  Sperm := MatToPermGF8(Smat);;  Tperm := MatToPermGF8(Tmat);;
  wPerm := Sperm * Tperm^-1;;  Xperm := wPerm^2;;  Yperm := Sperm^-1 * Xperm * Sperm;;
  Pgrp := Group(Xperm, Yperm);;
  s4cache := rec(x := Xperm, y := Yperm, G := Pgrp, degree := 9, label := "S4(N_S4)");;
  return s4cache;;
end;;

words1152a := [ "(a^-3*b*a^-1)^2", "(a^-2*b*a^-2)^2", "(a^-1*b*a^-3)^2", "(b*a^-4)^2", "(b^4*a^-1)^2", "(b^-1*a^4)^2", "(b^-1*a*b^-3)^2", "(b^-2*a*b^-2)^2", "(b^-3*a*b^-1)^2", "(b^-4*a)^2", "a*(b*a^-4)^2*a^-1", "a*(b^4*a^-1)^2*a^-1", "a*(b^-1*a*b^-3)^2*a^-1", "a*(b^-2*a*b^-2)^2*a^-1", "a*(b^-3*a*b^-1)^2*a^-1", "a^-5*b^6*a^-1", "a^-3*b^6*a^-3", "a^-3*(b^-1*a^-2*b^-1)^2*a^-1", "a^-2*b^6*a^-4", "a^-1*(b^-1*a*b^-3)^2*a", "a^-1*(b^-2*a*b^-2)^2*a", "a^-1*(b^-3*a*b^-1)^2*a", "b^5*a^-2*b^-1*a^4", "b^6*a^-6", "b^-3*a^6*b^-3", "a^2*(b^-1*a*b^-3)^2*a^-2", "a^2*(b^-2*a*b^-2)^2*a^-2", "a^2*(b^-3*a*b^-1)^2*a^-2", "a*b^-3*a^6*b^-3*a^-1", "(a^-3*b^2*a^-2)^2", "a^-1*(a^-1*b)^2*b^3*(b*a^-1)^2*a^-2", "(a^-2*b^2*a^-3)^2", "a^-2*(b^-1*a*b^-3)^2*a^2", "a^-2*(b^-2*a*b^-2)^2*a^2", "a^-1*b^-3*a^6*b^-3*a", "(b*a^-1)^2*b^2*(b^2*a^-1)^2*b*a", "(b*a^-1*b)^2*b^2*(b*a^-1)^2*b*a", "(b^-1*a)^2*b^-2*(b^-2*a)^2*b^-1*a^-1", "(b^-1*a*b^-1)^2*b^-2*(b^-1*a)^2*b^-1*a^-1", "(b^-2*a^2*b^-3)^2", "(b^-3*a^2*b^-2)^2", "a^3*(b^-2*a*b^-2)^2*a^-3", "a^2*b^-3*a^6*b^-3*a^-2", "(a*b^-1)^3*b^-1*(b^-2*a)^2*b^-1*a^-2", "a*(b^-1*a*b^-1)^2*b^-2*(b^-1*a)^2*b^-1*a^-2", "a*(b^-2*a^2*b^-3)^2*a^-1", "a*(b^-3*a^2*b^-2)^2*a^-1", "a^-2*(a^-1*b^2)^2*b^2*(b*a^-2)^2", "a^-2*b^3*a^-4*(a^-1*b)^2*a^-3", "a^-1*((b*a^-1)^3*b)^2*a^-1", "(a^-1*b)^3*b*(b^2*a^-1)^2*b*a^2", "a^-1*b*a^-1*b*(b*a^-2*b^2*a^-1)^2", "(a^-1*(b*a^-1*b)^2*a^-1)^2", "a^-1*(b*a^-1*b)^2*b^2*(b*a^-1)^2*b*a^2", "a^-1*b*(b*a^-2)^2*a^-3*b^-1*(b^-1*a)^2", "(a^-1*b^2*a^-2*b)^2*b*a^-1*b*a^-1", "a^-1*(b^-2*a^2*b^-3)^2*a", "a^-1*(b^-3*a^2*b^-2)^2*a", "b*a^-2*b^2*a^-6*b^-1*a*b^-2*a", "b*a^-1*(a^-1*b^2*a^-2*b)^2*b*a^-1", "b*a^-1*(a^-1*b^2)^2*b*(b*a^-1)^2*b^2*a", "(b*a^-1)^3*a^-4*b^-3*a^2*b^-1", "b*((a^-1*b)^2*a^-1)^2*b*a^-1*b^2*a^-1", "((b*a^-1)^3*b)^2*a^-2", "((b*a^-1)^2*b)^2*a^-1*b*a^-2*b*a^-1", "b*a^-1*b*(b*a^-2*b^2*a^-1)^2*a^-1", "((b*a^-1*b)^2*a^-2)^2", "b*a^-1*b^2*a^-1*b*((a^-1*b)^2*a^-1)^2", "b*(b*a^-2*b^2*a^-1)^2*a^-1*b*a^-1", "b^2*((a^-1*b)^3*a^-1)^2", "b*(b*a^-1)^2*b^2*(b^2*a^-1)^2*a^-1*b*a", "b^2*(b*a^-2)^2*a^-3*b^-2*a*b^-2", "(b^-1*a^2*b^-2*a)^2*a*b^-1*a*b^-1", "b^-1*a*(a*b^-2)^2*b^-1*(b^-1*a)^2*b^-2*a^-1", "b^-1*((a*b^-1)^3*a)^2*b^-1", "((b^-1*a)^3*b^-1)^2*a^2", "((b^-1*a)^2*b^-1)^2*a*b^-1*a^2*b^-1*a", "b^-1*a*b^-1*(b^-1*a^2*b^-2*a)^2*a", "((b^-1*a*b^-1)^2*a^2)^2", "b^-1*a*b^-2*a*b^-1*((a*b^-1)^2*a)^2", "b^-2*a^2*b^-1*(a*b^-2*a)^2*b^-1*a^2", "b^-1*(b^-1*a^2*b^-2*a)^2*a*b^-1*a", "b^-2*((a*b^-1)^3*a)^2", "b^-1*(b^-1*a)^2*b^-2*(b^-2*a)^2*a*b^-1*a^-1", "a*(a*b^-1)^3*b^-1*(b^-2*a)^2*b^-1*a^-3", "a^2*b^-1*(b^-1*a^2)^2*a^3*b*(b*a^-1)^2*a^-1", "a^2*(b^-2*a^2*b^-3)^2*a^-2", "a^2*(b^-3*a^2*b^-2)^2*a^-2", "a*b*a^-1*(a^-1*b^2*a^-2*b)^2*b*a^-2", "a*b*((a^-1*b)^2*a^-1)^2*b*a^-1*b^2*a^-2", "a*((b*a^-1)^3*b)^2*a^-3", "a*b*a^-1*b*(b*a^-2*b^2*a^-1)^2*a^-2", "a*(b*a^-1*b)^2*((a^-1*b)^2*a^-1)^2*a^-1", "a*b*(b*a^-2*b^2*a^-1)^2*a^-1*b*a^-2", "(a*b^-1*a^2*b^-2)^2*a*(a*b^-1)^2*a^-1", "a*b^-1*a*(a*b^-2)^2*b^-1*(b^-1*a)^2*b^-2*a^-2", "a*b^-1*(b^-1*a)^2*b^-2*(b^-2*a)^2*a*b^-1*a^-2", "(a^-3*b*(b*a^-1)^2*a^-1)^2", "a^-2*b*(b^2*a^-2)^2*b*(b*a^-1)^3", "a^-1*b*(b*a^-1)^2*b^2*(b^2*a^-1)^2*a^-1*b*a^2", "a^-1*b^2*(b*a^-2)^2*a^-3*(b^-2*a)^2", "a^-1*(b^-1*a^2*b^-2*a)^2*(a*b^-1)^2*a", "a^2*b*((a^-1*b)^2*a^-1)^2*b*a^-1*b^2*a^-3", "a^2*b^-1*(b^-1*a)^2*b^-2*(b^-2*a)^2*a*b^-1*a^-3", "a^-3*b*(b*a^-1)^2*b^5*a^-1*(a^-1*b)^2*a^-2", "a^-1*(a^-1*b)^2*a^-2*b^4*(b*a^-1)^2*b^2*a^-3", "a^-1*(a^-1*b^2*a^-1*b)^2*a^-1*b*a^-2*b^3*a^-2", "a^-2*b*(b*a^-1)^2*b^5*a^-1*(a^-1*b)^2*a^-3", "a^-2*(b^-1*a^2*b^-2*a)^2*(a*b^-1)^2*a^2" ];;
words1152b := [ "a^-1*(b*a^2*b)^2*a^-1", "a^-1*b^-1*a^2*b^-1*a^-2*b^-2*a^-1", "b*a^-2*b*a^2*b^2*a^2", "b^-1*a^2*b^-1*a^-2*b^-2*a^-2", "a*b^-1*a^2*b^-1*a^-2*b^-2*a^-3", "a^-12", "a^-3*b^6*a^-3", "a^-2*b^6*a^-4", "b^2*a^-3*b*a^2*b^3*a", "(b^3*a^-1)^3", "(b^-1*a*b^-2)^3", "a*(b^3*a^-1)^3*a^-1", "a*(b^-1*a*b^-2)^3*a^-1", "(a^-2*(a^-1*b)^2*a^-1)^2", "a^-2*(a^-1*b)^2*b^3*(b*a^-1)^2*a^-1", "(a^-1*(a^-1*b)^2*a^-2)^2", "a^-1*(a^-1*b)^2*b^3*(b*a^-1)^2*a^-2", "((a^-1*b)^2*a^-3)^2", "(a^-1*b)^2*b^3*(b*a^-1)^2*a^-3", "a^-1*(b^-1*a*b^-2)^3*a", "((b^-1*a)^2*b^-3)^2", "(b^-1*a*b^-1)^2*b^-3*a^2*b^-3", "(b^-1*(b^-1*a)^2*b^-2)^2", "(b^-2*a)^2*b^-4*a^2*b^-2", "(b^-2*(b^-1*a)^2*b^-1)^2", "a*((b^-1*a)^2*b^-3)^2*a^-1", "a*(b^-1*a*b^-1)^2*b^-3*a^2*b^-3*a^-1", "a*(b^-1*(b^-1*a)^2*b^-2)^2*a^-1", "a^-1*((b*a^-1)^3*b)^2*a^-1", "a^-1*b*a^-1*b*(b*a^-2*b^2*a^-1)^2", "(a^-1*(b*a^-1*b)^2*a^-1)^2", "a^-1*b^2*a^-1*(b*a^-2*b)^2*a^-1*b^2*a^-1", "a^-1*(b^-1*(b^-1*a)^2*b^-2)^2*a", "a^-1*b^-2*(b^-1*a)^2*a^3*(a*b^-1)^2*b^-1*a", "a^-1*(b^-2*(b^-1*a)^2*b^-1)^2*a", "(b*a^-1)^3*a^-4*(b^-2*a)^2", "b*((a^-1*b)^2*a^-1)^2*b*a^-1*b^2*a^-1", "((b*a^-1)^3*b)^2*a^-2", "((b*a^-1)^2*b)^2*a^-1*b*a^-2*b*a^-1", "((b*a^-1*b)^2*a^-2)^2", "b*a^-1*b^2*a^-1*b*((a^-1*b)^2*a^-1)^2", "(b^2*(a^-1*b*a^-1)^2)^2", "b^2*a^-1*(b*a^-2*b)^2*a^-1*b^2*a^-2", "b^2*((a^-1*b)^3*a^-1)^2", "b^-1*((a*b^-1)^3*a)^2*b^-1", "((b^-1*a)^3*b^-1)^2*a^2", "((b^-1*a)^2*b^-1)^2*a*b^-1*a^2*b^-1*a", "b^-1*a*b^-1*(b^-1*a^2*b^-2*a)^2*a", "((b^-1*a*b^-1)^2*a^2)^2", "b^-1*a*b^-2*a*b^-1*((a*b^-1)^2*a)^2", "b^-2*a^2*b^-1*(a*b^-2*a)^2*b^-1*a^2", "b^-2*((a*b^-1)^3*a)^2", "(b^-2*a)^2*a^2*(a^2*b^-1)^2*b^-2", "b^-2*(b^-1*a^2)^2*a^2*(a*b^-2)^2", "a^2*((b^-1*a)^2*b^-3)^2*a^-2", "a^2*(b^-1*(b^-1*a)^2*b^-2)^2*a^-2", "a*b*((a^-1*b)^2*a^-1)^2*b*a^-1*b^2*a^-2", "a*((b*a^-1)^3*b)^2*a^-3", "a*(b*a^-1*b)^2*((a^-1*b)^2*a^-1)^2*a^-1" ];;

r1152acache := fail;;
BuildR1152Window := function(which)
  local w, idg, Wwin;
  if which = "a" then
    if r1152acache <> fail then return r1152acache; fi;
    w := words1152a;; idg := [1152,154161];;
  else
    w := words1152b;; idg := [1152,154163];;
  fi;
  Wwin := BuildWindowFromWords(1152, w);;
  if IdGroup(Wwin.Bq) <> idg then Error("BuildR1152Window: IdGroup mismatch"); fi;
  Wwin.degree := LargestMovedPoint(Group(Wwin.x, Wwin.y));;
  Wwin.label := Concatenation("1152[", String(idg[2]), "]");;
  if which = "a" then r1152acache := Wwin; fi;
  return Wwin;;
end;;

# ---- one roof: build + shadow + Frattini + crown census ----
RunRoof := function(leftW, rightW, capSeconds)
  local XM, YM, GM, Mord, Mcharm, qrecM, resM, reg, out, phiXX, Xbar, battery, calib;
  out := rec(left := leftW.label, right := rightW.label, status := "UNKNOWN");;
  XM := DirectSumPerm(leftW.x, leftW.degree, rightW.x, rightW.degree);;
  YM := DirectSumPerm(leftW.y, leftW.degree, rightW.y, rightW.degree);;
  GM := Group(XM, YM);;
  out.PB3_over_M := Size(GM);;
  Mord := Lcm(Order(XM), Order(YM));;
  out.M_ord := Mord;;
  Mcharm := Filtered([0..Mord-1], mm -> Gcd(2*mm+1, Mord) = 1);;
  out.charming_set_size := Length(Mcharm);;
  qrecM := rec(x := XM, y := YM, G := GM);;
  resM := ScanRoofHexagonCapped(qrecM, Mcharm, capSeconds);;
  out.derived_order := resM.derived_order;;
  out.candidate_total := resM.candidate_total;;
  out.shadow_total := resM.shadow_total;;
  out.scan_capped := resM.capped;;
  out.scan_elapsed_seconds := resM.elapsed_seconds;;
  if resM.theta_tau_not_well_defined then
    out.status := "UNKNOWN_THETA_TAU_NOT_WELL_DEFINED";;
    return out;;
  fi;
  if resM.capped then
    out.status := "UNKNOWN_CAP_EXCEEDED_AT_SCAN";;
    return out;;
  fi;
  if resM.shadow_total = 0 then
    out.status := "UNKNOWN_ZERO_SHADOWS";;
    return out;;
  fi;
  reg := BuildShadowCompositionRegularRep(qrecM, resM.shadows, Mord);;
  out.closed_observed := reg.closed_observed;;
  if not reg.closed_observed then
    out.status := "UNKNOWN_COMPOSITION_NOT_CLOSED";;
    return out;;
  fi;
  out.size_X := Size(reg.regGrp);;
  phiXX := FrattiniSubgroup(reg.regGrp);;
  out.size_Phi := Size(phiXX);;
  Xbar := reg.regGrp / phiXX;;
  out.size_Xbar := Size(Xbar);;
  battery := BuildCrownBattery(Xbar);;
  out.n_classes := battery.n_classes;;
  out.classes := List(battery.entries, e -> rec(index:=e.index, normal:=e.normal,
                       quotient_order:=e.quotient_order, quotient_abelian:=e.quotient_abelian));;
  out.normal_count := Length(Filtered(battery.entries, e -> e.normal));;
  out.nonnormal_count := Length(Filtered(battery.entries, e -> not e.normal));;
  calib := CalibrateCrownBattery(battery);;
  out.calibration_ok := calib.calibration_ok;;
  out.status := "COMPLETE";;
  return out;;
end;;

# ==== cert writer (checkpoint after each roof) ====
ClassJson := function(c)
  return Concatenation("{\"index\":", String(c.index), ",\"normal\":", JB(c.normal),
    ",\"quotient_order\":", String(c.quotient_order), ",\"quotient_abelian\":", JB(c.quotient_abelian),
    ",\"test_type\":\"maximal-class\"}");
end;;

RowJson := function(r)
  local base;
  base := Concatenation(
    "{\"left\":\"", r.left, "\",\"right\":\"", r.right, "\",\"status\":\"", r.status, "\"",
    ",\"PB3_over_M\":", String(r.PB3_over_M), ",\"M_ord\":", String(r.M_ord),
    ",\"charming_set_size\":", String(r.charming_set_size),
    ",\"derived_order\":", String(r.derived_order),
    ",\"candidate_total\":", String(r.candidate_total),
    ",\"shadow_total\":", String(r.shadow_total),
    ",\"scan_capped\":", JB(r.scan_capped),
    ",\"scan_elapsed_seconds\":", String(r.scan_elapsed_seconds)
  );;
  if r.status = "COMPLETE" then
    base := Concatenation(base,
      ",\"size_X\":", String(r.size_X), ",\"size_Phi\":", String(r.size_Phi),
      ",\"size_Xbar\":", String(r.size_Xbar), ",\"n_classes\":", String(r.n_classes),
      ",\"normal_count\":", String(r.normal_count), ",\"nonnormal_count\":", String(r.nonnormal_count),
      ",\"classes\":", JArr(List(r.classes, ClassJson)),
      ",\"calibration_ok\":", JB(r.calibration_ok));;
  fi;
  base := Concatenation(base, "}");;
  return base;;
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_roofsweep.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

WriteCheckpoint := function(rows, doneCount, totalCount)
  local cert;
  cert := Concatenation(
    "{\"schema\":\"roof-sweep/v1\"",
    ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/roof_sweep_v1.g\",\"order\":\"裁定1059(異族屋根一括掃討)\"}",
    ",\"gap_version\":\"", GAPInfo.Version, "\"",
    ",\"per_roof_cap_seconds\":600",
    ",\"progress\":{\"done\":", String(doneCount), ",\"total\":", String(totalCount), "}",
    ",\"rows\":", JArr(List(rows, RowJson)),
    ",\"u_touched\":false,\"c_touched\":false,\"prereg_value_computed\":false",
    ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
    "}"
  );;
  WriteFile("search/certs/roof_sweep_v1_20260812.json", cert);;
end;;

# ====================================================================
# 実行: 陽性対照(K9 x S4 = 972屋根) + 16異族屋根
# ====================================================================
Print("############################################################\n");
Print("# roof_sweep_v1.g -- 異族屋根一括掃討(裁定1059)\n");
Print("############################################################\n");
t0 := GAPLIB_WallElapsedMs();;

kNs := [3, 9, 15, 21, 27, 33, 81];;
r1152vals := ["a", "b"];;

rows := [];;
totalCount := 1 + Length(kNs)*2 + 2;;   # positive control + 14 K-1152 + 2 S4-1152

Print("\n=== 陽性対照: K(9) x S4 (972屋根) ===\n");
tR0 := GAPLIB_WallElapsedMs();;
rowPC := RunRoof(BuildKWindow(9), BuildS4Window(), 600.0);;
tR1 := GAPLIB_WallElapsedMs();;
Print("status=", rowPC.status, " shadow_total=", rowPC.shadow_total, "\n");
if rowPC.status = "COMPLETE" then
  Print("  |X|=", rowPC.size_X, " |Phi|=", rowPC.size_Phi, " |X/Phi|=", rowPC.size_Xbar,
        " n_classes=", rowPC.n_classes, " normal=", rowPC.normal_count,
        " nonnormal=", rowPC.nonnormal_count, " calib_ok=", rowPC.calibration_ok,
        " (期待: shadow=972 Phi=9 Xbar=108 classes=8 normal=4 nonnormal=4)\n");
fi;
Print("  elapsed_ms=", tR1-tR0, "\n");
Add(rows, rowPC);;
WriteCheckpoint(rows, 1, totalCount);;

doneCount := 1;;
for n in kNs do
  for rv in r1152vals do
    doneCount := doneCount + 1;;
    Print("\n=== K(", n, ") x 1152[", rv, "] (", doneCount, "/", totalCount, ") ===\n");
    tR0 := GAPLIB_WallElapsedMs();;
    row := RunRoof(BuildKWindow(n), BuildR1152Window(rv), 600.0);;
    tR1 := GAPLIB_WallElapsedMs();;
    Print("status=", row.status, " shadow_total=", row.shadow_total, " elapsed_ms=", tR1-tR0, "\n");
    if row.status = "COMPLETE" then
      Print("  |X|=", row.size_X, " |Phi|=", row.size_Phi, " |X/Phi|=", row.size_Xbar,
            " n_classes=", row.n_classes, " normal=", row.normal_count,
            " nonnormal=", row.nonnormal_count, " calib_ok=", row.calibration_ok, "\n");
    fi;
    Add(rows, row);;
    WriteCheckpoint(rows, doneCount, totalCount);;
  od;
od;

for rv in r1152vals do
  doneCount := doneCount + 1;;
  Print("\n=== S4 x 1152[", rv, "] (", doneCount, "/", totalCount, ") ===\n");
  tR0 := GAPLIB_WallElapsedMs();;
  row := RunRoof(BuildS4Window(), BuildR1152Window(rv), 600.0);;
  tR1 := GAPLIB_WallElapsedMs();;
  Print("status=", row.status, " shadow_total=", row.shadow_total, " elapsed_ms=", tR1-tR0, "\n");
  if row.status = "COMPLETE" then
    Print("  |X|=", row.size_X, " |Phi|=", row.size_Phi, " |X/Phi|=", row.size_Xbar,
          " n_classes=", row.n_classes, " normal=", row.normal_count,
          " nonnormal=", row.nonnormal_count, " calib_ok=", row.calibration_ok, "\n");
  fi;
  Add(rows, row);;
  WriteCheckpoint(rows, doneCount, totalCount);;
od;

t1 := GAPLIB_WallElapsedMs();;
Print("\n============================================================\n");
Print("# 一覧表\n");
Print("============================================================\n");
Print("left | right | status | shadow_total | |X| | |Phi| | |X/Phi| | classes(n/nn) | calib_ok\n");
for r in rows do
  if r.status = "COMPLETE" then
    Print(r.left, " x ", r.right, " | ", r.status, " | ", r.shadow_total, " | ", r.size_X, " | ",
          r.size_Phi, " | ", r.size_Xbar, " | ", r.normal_count, "/", r.nonnormal_count,
          " | ", r.calibration_ok, "\n");
  else
    Print(r.left, " x ", r.right, " | ", r.status, " | ", r.shadow_total, "\n");
  fi;
od;

Print("\n総経過 = ", t1-t0, " ms\n");

scriptSha256 := ComputeSha256File("search/roof_sweep_v1.g");;
Print("script sha256 = ", scriptSha256, "\n");

# final cert with sha256 included
finalCert := Concatenation(
  "{\"schema\":\"roof-sweep/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/roof_sweep_v1.g\",\"order\":\"裁定1059(異族屋根一括掃討)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"per_roof_cap_seconds\":600",
  ",\"progress\":{\"done\":", String(doneCount), ",\"total\":", String(totalCount), "}",
  ",\"rows\":", JArr(List(rows, RowJson)),
  ",\"u_touched\":false,\"c_touched\":false,\"prereg_value_computed\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;
WriteFile("search/certs/roof_sweep_v1_20260812.json", finalCert);;
Print("\nwrote search/certs/roof_sweep_v1_20260812.json\n");
QUIT;
