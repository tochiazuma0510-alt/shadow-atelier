# search/crown_battery_targets_v1.g -- crown バッテリー初実戦: 1152系2窓(裁定1041続き・
#   研究者指示起点)
#
# 対象: [1152,154161]/[1152,154163](search/iso_census83_deep15_data.g DEEP15、全settled=
#   isolated、既存cert search/certs/iso_census83_deep15_v1_20260812.json で確認済み:
#   両窓とも pn_order=192・n_ord=12・shadow_total=48・all_kernel_trivial=true・
#   c_is_identity=false)。
# 構成: search/iso_census83_deep15_v1.g の BuildWindowFromWords/MakeWindow/TH/TT/RtOf/
#   CorrectedShadows(wall-miner-v4.g からの逐語引用パターン)を再利用し、まず窓(Bq,PN)を
#   再構成 → CorrectedShadows で48個の(m,f)ペアを得る → crown_battery_v1.g と同一の
#   shadow-composition-table 手法で GT(N)(位数48)を具体置換群として構成 → Frattini表行
#   + crown類census + 各類の可換/非可換 + 1ビット判定器の適用可否を記録。
#
# 847依存監査: BuildWindowFromWords/MakeWindow/TH/TT/RtOf/CorrectedShadowsは
#   iso_census83_deep15_v1.g(裁定986・既に検収済み構成)と同一パターンを再利用(既存
#   確立済み計器の再実行であり、独自の代数的再導出ではない -- 発注が「census で全settled
#   =isolated」と既存資産を明示的に指定しているため、この場合は再利用が正しい選択)。

SizeScreen([4096, 0]);;
Read("search/probe/wac_v1/gap_output_prelude.g");;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ---- (F2) machinery, verbatim from wall-miner-v4.g / iso_census83_deep15_v1.g ----
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
  if not (idxOk and isNormal) then
    Error("BuildWindowFromWords: index/normality mismatch");
  fi;
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  Gimg := Image(hm);;
  isoQ := IsomorphismPermGroup(Gimg);;
  s1 := Image(isoQ, Image(hm, ga));;
  s2 := Image(isoQ, Image(hm, gb));;
  return MakeWindow(s1, s2);;
end;;

# ---- shadow-composition regular rep (v1/v2/v3 と同一パターン) ----
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

BuildShadowCompositionRegularRep := function(W, shadowPairs, Nord)
  local n, i1, i2, m1, f1, m2, f2, u1, Ehom, newm, newf, idx, t, tbl, closureFail, regGrp,
        idxDict, key, shadows;
  shadows := List(shadowPairs, p -> rec(m := p[1], f := p[2]));;
  n := Length(shadows);;
  tbl := [];;  closureFail := 0;;
  idxDict := NewDictionary([shadows[1].m, shadows[1].f], true);;
  for t in [1..n] do AddDictionary(idxDict, [shadows[t].m, shadows[t].f], t);; od;
  for i1 in [1..n] do
    m1 := shadows[i1].m;;  f1 := shadows[i1].f;;  u1 := 2*m1+1;;
    Ehom := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
              [W.x^u1, AbstractProd([f1^-1, W.y^u1, f1])]);;
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
  if closureFail > 0 then return rec(regGrp:=fail, closed_observed:=false, closure_fail_count:=closureFail);; fi;
  regGrp := BuildRegularPermGroupFromTable(tbl, n);;
  return rec(regGrp:=regGrp, closed_observed:=true, closure_fail_count:=0);;
end;;

# ---- crown battery (crown_battery_v1.g と同一パターン、self-caught closure バグ修正済み) ----
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
    testFn := function(A)
      local Aimg;
      Aimg := Image(quotHom, A);;
      return IsTrivial(Aimg);;
    end;;
  else
    cosetActHom := FactorCosetAction(Qc, McImageInQc);;
    testFn := function(A)
      local Aimg, AimgPerm, deg;
      Aimg := Image(quotHom, A);;
      AimgPerm := Image(cosetActHom, Aimg);;
      deg := Index(Qc, McImageInQc);;
      return ForAny([1..deg], pt -> ForAll(GeneratorsOfGroup(AimgPerm), g -> pt^g = pt));;
    end;;
  fi;
  return rec(class_id := classId, index := indexC, normal := normalC,
             core_order := Size(coreC), quotient_order := Size(Qc),
             representative := Mc, core := coreC, quotHom := quotHom,
             quotient_abelian := IsAbelian(Qc),
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
  return rec(matrix := matrix, diag_all_true := allDiagOk, off_diagonal_fail_count := offDiagFail,
             calibration_ok := calibOk);;
end;;

# ====================================================================
# 実行
# ====================================================================
Print("############################################################\n");
Print("# crown_battery_targets_v1.g -- 初実戦: 1152系2窓\n");
Print("############################################################\n");
t0 := GAPLIB_WallElapsedMs();;

targets := [
  rec(idg := [1152,154161], words := [ "(a^-3*b*a^-1)^2", "(a^-2*b*a^-2)^2", "(a^-1*b*a^-3)^2", "(b*a^-4)^2", "(b^4*a^-1)^2", "(b^-1*a^4)^2", "(b^-1*a*b^-3)^2", "(b^-2*a*b^-2)^2", "(b^-3*a*b^-1)^2", "(b^-4*a)^2", "a*(b*a^-4)^2*a^-1", "a*(b^4*a^-1)^2*a^-1", "a*(b^-1*a*b^-3)^2*a^-1", "a*(b^-2*a*b^-2)^2*a^-1", "a*(b^-3*a*b^-1)^2*a^-1", "a^-5*b^6*a^-1", "a^-3*b^6*a^-3", "a^-3*(b^-1*a^-2*b^-1)^2*a^-1", "a^-2*b^6*a^-4", "a^-1*(b^-1*a*b^-3)^2*a", "a^-1*(b^-2*a*b^-2)^2*a", "a^-1*(b^-3*a*b^-1)^2*a", "b^5*a^-2*b^-1*a^4", "b^6*a^-6", "b^-3*a^6*b^-3", "a^2*(b^-1*a*b^-3)^2*a^-2", "a^2*(b^-2*a*b^-2)^2*a^-2", "a^2*(b^-3*a*b^-1)^2*a^-2", "a*b^-3*a^6*b^-3*a^-1", "(a^-3*b^2*a^-2)^2", "a^-1*(a^-1*b)^2*b^3*(b*a^-1)^2*a^-2", "(a^-2*b^2*a^-3)^2", "a^-2*(b^-1*a*b^-3)^2*a^2", "a^-2*(b^-2*a*b^-2)^2*a^2", "a^-1*b^-3*a^6*b^-3*a", "(b*a^-1)^2*b^2*(b^2*a^-1)^2*b*a", "(b*a^-1*b)^2*b^2*(b*a^-1)^2*b*a", "(b^-1*a)^2*b^-2*(b^-2*a)^2*b^-1*a^-1", "(b^-1*a*b^-1)^2*b^-2*(b^-1*a)^2*b^-1*a^-1", "(b^-2*a^2*b^-3)^2", "(b^-3*a^2*b^-2)^2", "a^3*(b^-2*a*b^-2)^2*a^-3", "a^2*b^-3*a^6*b^-3*a^-2", "(a*b^-1)^3*b^-1*(b^-2*a)^2*b^-1*a^-2", "a*(b^-1*a*b^-1)^2*b^-2*(b^-1*a)^2*b^-1*a^-2", "a*(b^-2*a^2*b^-3)^2*a^-1", "a*(b^-3*a^2*b^-2)^2*a^-1", "a^-2*(a^-1*b^2)^2*b^2*(b*a^-2)^2", "a^-2*b^3*a^-4*(a^-1*b)^2*a^-3", "a^-1*((b*a^-1)^3*b)^2*a^-1", "(a^-1*b)^3*b*(b^2*a^-1)^2*b*a^2", "a^-1*b*a^-1*b*(b*a^-2*b^2*a^-1)^2", "(a^-1*(b*a^-1*b)^2*a^-1)^2", "a^-1*(b*a^-1*b)^2*b^2*(b*a^-1)^2*b*a^2", "a^-1*b*(b*a^-2)^2*a^-3*b^-1*(b^-1*a)^2", "(a^-1*b^2*a^-2*b)^2*b*a^-1*b*a^-1", "a^-1*(b^-2*a^2*b^-3)^2*a", "a^-1*(b^-3*a^2*b^-2)^2*a", "b*a^-2*b^2*a^-6*b^-1*a*b^-2*a", "b*a^-1*(a^-1*b^2*a^-2*b)^2*b*a^-1", "b*a^-1*(a^-1*b^2)^2*b*(b*a^-1)^2*b^2*a", "(b*a^-1)^3*a^-4*b^-3*a^2*b^-1", "b*((a^-1*b)^2*a^-1)^2*b*a^-1*b^2*a^-1", "((b*a^-1)^3*b)^2*a^-2", "((b*a^-1)^2*b)^2*a^-1*b*a^-2*b*a^-1", "b*a^-1*b*(b*a^-2*b^2*a^-1)^2*a^-1", "((b*a^-1*b)^2*a^-2)^2", "b*a^-1*b^2*a^-1*b*((a^-1*b)^2*a^-1)^2", "b*(b*a^-2*b^2*a^-1)^2*a^-1*b*a^-1", "b^2*((a^-1*b)^3*a^-1)^2", "b*(b*a^-1)^2*b^2*(b^2*a^-1)^2*a^-1*b*a", "b^2*(b*a^-2)^2*a^-3*b^-2*a*b^-2", "(b^-1*a^2*b^-2*a)^2*a*b^-1*a*b^-1", "b^-1*a*(a*b^-2)^2*b^-1*(b^-1*a)^2*b^-2*a^-1", "b^-1*((a*b^-1)^3*a)^2*b^-1", "((b^-1*a)^3*b^-1)^2*a^2", "((b^-1*a)^2*b^-1)^2*a*b^-1*a^2*b^-1*a", "b^-1*a*b^-1*(b^-1*a^2*b^-2*a)^2*a", "((b^-1*a*b^-1)^2*a^2)^2", "b^-1*a*b^-2*a*b^-1*((a*b^-1)^2*a)^2", "b^-2*a^2*b^-1*(a*b^-2*a)^2*b^-1*a^2", "b^-1*(b^-1*a^2*b^-2*a)^2*a*b^-1*a", "b^-2*((a*b^-1)^3*a)^2", "b^-1*(b^-1*a)^2*b^-2*(b^-2*a)^2*a*b^-1*a^-1", "a*(a*b^-1)^3*b^-1*(b^-2*a)^2*b^-1*a^-3", "a^2*b^-1*(b^-1*a^2)^2*a^3*b*(b*a^-1)^2*a^-1", "a^2*(b^-2*a^2*b^-3)^2*a^-2", "a^2*(b^-3*a^2*b^-2)^2*a^-2", "a*b*a^-1*(a^-1*b^2*a^-2*b)^2*b*a^-2", "a*b*((a^-1*b)^2*a^-1)^2*b*a^-1*b^2*a^-2", "a*((b*a^-1)^3*b)^2*a^-3", "a*b*a^-1*b*(b*a^-2*b^2*a^-1)^2*a^-2", "a*(b*a^-1*b)^2*((a^-1*b)^2*a^-1)^2*a^-1", "a*b*(b*a^-2*b^2*a^-1)^2*a^-1*b*a^-2", "(a*b^-1*a^2*b^-2)^2*a*(a*b^-1)^2*a^-1", "a*b^-1*a*(a*b^-2)^2*b^-1*(b^-1*a)^2*b^-2*a^-2", "a*b^-1*(b^-1*a)^2*b^-2*(b^-2*a)^2*a*b^-1*a^-2", "(a^-3*b*(b*a^-1)^2*a^-1)^2", "a^-2*b*(b^2*a^-2)^2*b*(b*a^-1)^3", "a^-1*b*(b*a^-1)^2*b^2*(b^2*a^-1)^2*a^-1*b*a^2", "a^-1*b^2*(b*a^-2)^2*a^-3*(b^-2*a)^2", "a^-1*(b^-1*a^2*b^-2*a)^2*(a*b^-1)^2*a", "a^2*b*((a^-1*b)^2*a^-1)^2*b*a^-1*b^2*a^-3", "a^2*b^-1*(b^-1*a)^2*b^-2*(b^-2*a)^2*a*b^-1*a^-3", "a^-3*b*(b*a^-1)^2*b^5*a^-1*(a^-1*b)^2*a^-2", "a^-1*(a^-1*b)^2*a^-2*b^4*(b*a^-1)^2*b^2*a^-3", "a^-1*(a^-1*b^2*a^-1*b)^2*a^-1*b*a^-2*b^3*a^-2", "a^-2*b*(b*a^-1)^2*b^5*a^-1*(a^-1*b)^2*a^-3", "a^-2*(b^-1*a^2*b^-2*a)^2*(a*b^-1)^2*a^2" ] ),
  rec(idg := [1152,154163], words := [ "a^-1*(b*a^2*b)^2*a^-1", "a^-1*b^-1*a^2*b^-1*a^-2*b^-2*a^-1", "b*a^-2*b*a^2*b^2*a^2", "b^-1*a^2*b^-1*a^-2*b^-2*a^-2", "a*b^-1*a^2*b^-1*a^-2*b^-2*a^-3", "a^-12", "a^-3*b^6*a^-3", "a^-2*b^6*a^-4", "b^2*a^-3*b*a^2*b^3*a", "(b^3*a^-1)^3", "(b^-1*a*b^-2)^3", "a*(b^3*a^-1)^3*a^-1", "a*(b^-1*a*b^-2)^3*a^-1", "(a^-2*(a^-1*b)^2*a^-1)^2", "a^-2*(a^-1*b)^2*b^3*(b*a^-1)^2*a^-1", "(a^-1*(a^-1*b)^2*a^-2)^2", "a^-1*(a^-1*b)^2*b^3*(b*a^-1)^2*a^-2", "((a^-1*b)^2*a^-3)^2", "(a^-1*b)^2*b^3*(b*a^-1)^2*a^-3", "a^-1*(b^-1*a*b^-2)^3*a", "((b^-1*a)^2*b^-3)^2", "(b^-1*a*b^-1)^2*b^-3*a^2*b^-3", "(b^-1*(b^-1*a)^2*b^-2)^2", "(b^-2*a)^2*b^-4*a^2*b^-2", "(b^-2*(b^-1*a)^2*b^-1)^2", "a*((b^-1*a)^2*b^-3)^2*a^-1", "a*(b^-1*a*b^-1)^2*b^-3*a^2*b^-3*a^-1", "a*(b^-1*(b^-1*a)^2*b^-2)^2*a^-1", "a^-1*((b*a^-1)^3*b)^2*a^-1", "a^-1*b*a^-1*b*(b*a^-2*b^2*a^-1)^2", "(a^-1*(b*a^-1*b)^2*a^-1)^2", "a^-1*b^2*a^-1*(b*a^-2*b)^2*a^-1*b^2*a^-1", "a^-1*(b^-1*(b^-1*a)^2*b^-2)^2*a", "a^-1*b^-2*(b^-1*a)^2*a^3*(a*b^-1)^2*b^-1*a", "a^-1*(b^-2*(b^-1*a)^2*b^-1)^2*a", "(b*a^-1)^3*a^-4*(b^-2*a)^2", "b*((a^-1*b)^2*a^-1)^2*b*a^-1*b^2*a^-1", "((b*a^-1)^3*b)^2*a^-2", "((b*a^-1)^2*b)^2*a^-1*b*a^-2*b*a^-1", "((b*a^-1*b)^2*a^-2)^2", "b*a^-1*b^2*a^-1*b*((a^-1*b)^2*a^-1)^2", "(b^2*(a^-1*b*a^-1)^2)^2", "b^2*a^-1*(b*a^-2*b)^2*a^-1*b^2*a^-2", "b^2*((a^-1*b)^3*a^-1)^2", "b^-1*((a*b^-1)^3*a)^2*b^-1", "((b^-1*a)^3*b^-1)^2*a^2", "((b^-1*a)^2*b^-1)^2*a*b^-1*a^2*b^-1*a", "b^-1*a*b^-1*(b^-1*a^2*b^-2*a)^2*a", "((b^-1*a*b^-1)^2*a^2)^2", "b^-1*a*b^-2*a*b^-1*((a*b^-1)^2*a)^2", "b^-2*a^2*b^-1*(a*b^-2*a)^2*b^-1*a^2", "b^-2*((a*b^-1)^3*a)^2", "(b^-2*a)^2*a^2*(a^2*b^-1)^2*b^-2", "b^-2*(b^-1*a^2)^2*a^2*(a*b^-2)^2", "a^2*((b^-1*a)^2*b^-3)^2*a^-2", "a^2*(b^-1*(b^-1*a)^2*b^-2)^2*a^-2", "a*b*((a^-1*b)^2*a^-1)^2*b*a^-1*b^2*a^-2", "a*((b*a^-1)^3*b)^2*a^-3", "a*(b*a^-1*b)^2*((a^-1*b)^2*a^-1)^2*a^-1" ] ),
];;

results := [];;

for target in targets do
  Print("\n=== 窓 IdGroup=", target.idg, " 構成中 ===\n");
  Wwin := BuildWindowFromWords(1152, target.words);;
  Print("Bq order=", Size(Wwin.Bq), " PN order=", Size(Wwin.PN), " Nord=", Wwin.Nord, "\n");
  wIdCheck := IdGroup(Wwin.Bq);;
  wIdOk := (wIdCheck = target.idg);;
  Print("[", PF(wIdOk), "] IdGroup(Bq) = ", wIdCheck, " (期待 ", target.idg, "): ", wIdOk, "\n");

  charmingSet := Filtered([0 .. Wwin.Nord - 1], mm -> Gcd(2*mm+1, Wwin.Nord) = 1);;
  Print("charming_set size = ", Length(charmingSet), " (期待 8)\n");
  tShadow0 := GAPLIB_WallElapsedMs();;
  corr := CorrectedShadows(Wwin, charmingSet);;
  tShadow1 := GAPLIB_WallElapsedMs();;
  Print("shadow_total = ", Length(corr), " (期待 48)  elapsed_ms=", tShadow1-tShadow0, "\n");
  shadowOk := (Length(corr) = 48);;
  Print("[", PF(shadowOk), "] shadow_total=48: ", shadowOk, "\n");

  reg := BuildShadowCompositionRegularRep(Wwin, corr, Wwin.Nord);;
  Print("closed_observed = ", reg.closed_observed, "\n");

  if not reg.closed_observed then
    Print("[HALT] shadow composition not closed for ", target.idg, " -- raw failure only.\n");
    Add(results, rec(idg := target.idg, closed_observed := false));;
  else
    XX := reg.regGrp;;
    Print("|GT(N)| = ", Size(XX), "\n");
    phiXX := FrattiniSubgroup(XX);;
    Xbar := XX/phiXX;;
    Print("|Phi(GT(N))| = ", Size(phiXX), " |Xbar| = ", Size(Xbar), "\n");
    battery := BuildCrownBattery(Xbar);;
    Print("極大共役類数 = ", battery.n_classes, "\n");
    for e in battery.entries do
      Print("  class ", e.class_id, ": index=", e.index, " normal=", e.normal,
            " |Xbar/Core|=", e.quotient_order, " quotient_abelian=", e.quotient_abelian, "\n");
    od;
    calib := CalibrateCrownBattery(battery);;
    Print("[", PF(calib.calibration_ok), "] 較正行列(", battery.n_classes, "x", battery.n_classes,
          ") = 単位行列: ", calib.calibration_ok, "\n");
    Add(results, rec(idg := target.idg, bq_idgroup_ok := wIdOk, shadow_total := Length(corr),
                      shadow_total_ok := shadowOk, closed_observed := true,
                      size_GT_N := Size(XX), size_Phi := Size(phiXX), size_Xbar := Size(Xbar),
                      n_classes := battery.n_classes,
                      classes := List(battery.entries, e -> rec(class_id:=e.class_id, index:=e.index,
                                       normal:=e.normal, quotient_order:=e.quotient_order,
                                       quotient_abelian:=e.quotient_abelian)),
                      normal_count := Length(Filtered(battery.entries, e -> e.normal)),
                      nonnormal_count := Length(Filtered(battery.entries, e -> not e.normal)),
                      calibration_ok := calib.calibration_ok));;
  fi;
od;

Print("\n============================================================\n");
Print("# 一覧表\n");
Print("============================================================\n");
Print("idg | |GT(N)| | |Phi| | |Xbar| | n_classes | normal | nonnormal | calib_ok\n");
for r in results do
  if r.closed_observed then
    Print(r.idg, " | ", r.size_GT_N, " | ", r.size_Phi, " | ", r.size_Xbar, " | ", r.n_classes,
          " | ", r.normal_count, " | ", r.nonnormal_count, " | ", r.calibration_ok, "\n");
  else
    Print(r.idg, " | CLOSURE FAILED\n");
  fi;
od;

t1 := GAPLIB_WallElapsedMs();;
Print("\n総経過 = ", t1-t0, " ms\n");

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_crowntgt.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

ClassJson := function(c)
  return Concatenation("{\"class_id\":", String(c.class_id), ",\"index\":", String(c.index),
    ",\"normal\":", JB(c.normal), ",\"quotient_order\":", String(c.quotient_order),
    ",\"quotient_abelian\":", JB(c.quotient_abelian), ",\"test_type\":\"maximal-class\"}");
end;;

ResultJson := function(r)
  if not r.closed_observed then
    return Concatenation("{\"idg\":", JArr(List(r.idg,String)), ",\"closed_observed\":false}");
  fi;
  return Concatenation(
    "{\"idg\":", JArr(List(r.idg,String)), ",\"bq_idgroup_ok\":", JB(r.bq_idgroup_ok),
    ",\"shadow_total\":", String(r.shadow_total), ",\"shadow_total_ok\":", JB(r.shadow_total_ok),
    ",\"closed_observed\":true",
    ",\"size_GT_N\":", String(r.size_GT_N), ",\"size_Phi\":", String(r.size_Phi),
    ",\"size_Xbar\":", String(r.size_Xbar), ",\"n_classes\":", String(r.n_classes),
    ",\"normal_count\":", String(r.normal_count), ",\"nonnormal_count\":", String(r.nonnormal_count),
    ",\"classes\":", JArr(List(r.classes, ClassJson)),
    ",\"calibration_ok\":", JB(r.calibration_ok),
    "}"
  );
end;;

scriptSha256 := ComputeSha256File("search/crown_battery_targets_v1.g");;

granularityNote := "全testはtest_type=「maximal-class」(U-6のcrown-covering検定とは別述語、surg_universality_audit_v1.md 4.1参照)。";;

cert := Concatenation(
  "{\"schema\":\"crown-battery-targets/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/crown_battery_targets_v1.g\",\"order\":\"研究者指示起点(crownバッテリー初実戦・1152系2窓)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"source_reuse_note\":\"BuildWindowFromWords/MakeWindow/TH/TT/RtOf/CorrectedShadowsはsearch/iso_census83_deep15_v1.g(裁定986・既存確立済み計器)と同一パターンを再利用\"",
  ",\"granularity_note\":\"", granularityNote, "\"",
  ",\"results\":", JArr(List(results, ResultJson)),
  ",\"u_touched\":false,\"c_touched\":false,\"prereg_value_computed\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/crown_battery_targets_v1_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
