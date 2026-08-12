# search/crown_battery_v1.g -- crown バッテリー v1(裁定1041/1050の一手目・SB-1+SB-6)
#
# 正本: docs/notes/surg_boost_audit_v1.md §1(SB-1完備性・非正規検定の1ビット化)+§6(SB-6
#   較正)+§7(実装係への一手目) / docs/notes/surg_universality_audit_v1.md §4.1(U-6との
#   granularity弁別・S3⊇C3反例)。
#
# 器のみ: X/Phi(X) の極大部分群類を census し、各類 c について「部分群 A を与えると
#   1ビット(A が crown c の"maximal-class"検定を通すか)を返す判定器」を組む。まだ
#   何も算術的判定(実際のarithmetic subgroup A)はしない -- 較正モード(A=M_c を注入
#   して対角較正行列を assert)のみをここで実行する。
#
# 検定の定義(§1.1-1.2、一般形。S3の場合の「位数3の元を含むか」は導出される特殊形
#   であって、ハードコードしていない):
#   正規類 c(Core(M_c)=M_c): pass_c(A) := (A の Xbar/M_c での像が自明)
#   非正規類 c(Core(M_c)<M_c): pass_c(A) := (A の Xbar/Core(M_c) での像が、
#     M_c/Core(M_c) の剰余類作用(Xbar/Core(M_c) の自然な置換表現)で不動点を持つか)
#
# ⚠ granularity 注記(U-6監査 §4.1): 本バッテリーの検定は「maximal-class 検定」(A が
#   crown c を代表する極大類 M_c のいずれかの共役に含まれるか)であって、「crown-covering
#   検定」(A R_c = X)ではない。反例: Xbar=S_3 で A=C_3 は maximal-class 検定 PASS
#   (3点上に不動点なし=A**は**crownを覆う、の意でPASSは「不動点あり」の意 -- 要精査)
#   だが A≠Xbar なので crown-covering としては A は Xbar 自身を覆わない。両者を混同する
#   と fail-open になるため、本certの全testエントリに test_type:"maximal-class" を明記する。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ---- Aff(Z/n) x C2 構成(v4 と同一パターン) ----
BuildAff := function(n)
  local g, t, u, G;
  g := PrimitiveRootMod(n);;
  if g = fail then Error("BuildAff: no primitive root mod ", n); fi;
  t := PermList(List([0..n-1], x -> ((x+1) mod n) + 1));;
  u := PermList(List([0..n-1], x -> ((g*x) mod n) + 1));;
  G := Group(t, u);;
  return rec(n:=n, g:=g, t:=t, u:=u, G:=G);;
end;;

BuildGTKnViaAff := function(n)
  local aff, G;
  aff := BuildAff(n);;
  G := DirectProduct(aff.G, CyclicGroup(2));;
  return G;;
end;;

# ---- 972 屋根 M = K^(9) cap N_S4(v2 と同一パターン・ihnec_r4b_run.g 再利用) ----
Read("search/week3-psl-common.g");;

ScanRoofHexagon := function(qrec, charmingSet)
  local G, D, Delts, thetaHom, tauHom, zElt, h10Fail, h11Fail, genFail, shadows,
        m, u, f, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj,
        candidateTotal, i;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  D := DerivedSubgroup(G);
  Delts := Elements(D);
  h10Fail := 0;  h11Fail := 0;  genFail := 0;  shadows := [];
  candidateTotal := Length(Delts) * Length(charmingSet);
  for m in charmingSet do
    u := 2*m + 1;
    for i in [1 .. Length(Delts)] do
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
  od;
  return rec(candidate_total := candidateTotal, shadow_total := Length(shadows), shadows := shadows,
             derived_order := Length(Delts));
end;;

BuildRegularPermGroupFromTable := function(tbl, n)
  local prod, e, gens, a, images, b;
  prod := List([0..n-1], i -> List([0..n-1], j -> -1));;
  for e in tbl do prod[e[1]+1][e[2]+1] := e[3]; od;;
  gens := [];;
  for a in [0..n-1] do
    images := List([0..n-1], b -> prod[a+1][b+1] + 1);;
    Add(gens, PermList(images));;
  od;
  return Group(gens);;
end;;

BuildShadowCompositionRegularRep := function(qrec, shadows, Nord)
  local n, i1, i2, m1, f1, m2, f2, u1, Ehom, newm, newf, idx, t, tbl, closureFail, regGrp,
        idxDict, key;
  n := Length(shadows);;
  tbl := [];;  closureFail := 0;;
  idxDict := NewDictionary([shadows[1].m, shadows[1].f], true);;
  for t in [1..n] do AddDictionary(idxDict, [shadows[t].m, shadows[t].f], t);; od;
  for i1 in [1..n] do
    m1 := shadows[i1].m;;  f1 := shadows[i1].f;;  u1 := 2*m1+1;;
    Ehom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y],
              [qrec.x^u1, AbstractProd([f1^-1, qrec.y^u1, f1])]);;
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
  if closureFail > 0 then return rec(regGrp:=fail, closed_observed:=false);; fi;
  regGrp := BuildRegularPermGroupFromTable(tbl, n);;
  return rec(regGrp:=regGrp, closed_observed:=true);;
end;;

BuildRoof972 := function()
  local g9, Smat, Tmat, Sperm, Tperm, wPerm, Xperm, Yperm, Pgrp, ShiftPerm, DirectSumPerm,
        XM, YM, GM, Mord, Mcharm, qrecM, resM, regM;
  g9 := MakeGn(9);;
  CheckGF8();;
  Smat := MakeMatGF8(1,0,1,1);;  Tmat := MakeMatGF8(4,3,1,5);;
  Sperm := MatToPermGF8(Smat);;  Tperm := MatToPermGF8(Tmat);;
  wPerm := Sperm * Tperm^-1;;  Xperm := wPerm^2;;  Yperm := Sperm^-1 * Xperm * Sperm;;
  Pgrp := Group(Xperm, Yperm);;
  ShiftPerm := function(p, offset, size)
    local l, j;
    l := [1 .. offset+size];
    for j in [1 .. size] do l[offset+j] := offset + (j^p); od;
    return PermList(l);
  end;
  DirectSumPerm := function(p1, deg1, p2, deg2) return p1 * ShiftPerm(p2, deg1, deg2); end;
  XM := DirectSumPerm(g9.x, 27, Xperm, 9);;
  YM := DirectSumPerm(g9.y, 27, Yperm, 9);;
  GM := Group(XM, YM);;
  Mord := Lcm(Order(XM), Order(YM));;
  Mcharm := Filtered([0..Mord-1], mm -> Gcd(2*mm+1, Mord) = 1);;
  qrecM := rec(x := XM, y := YM, G := GM);;
  resM := ScanRoofHexagon(qrecM, Mcharm);;
  regM := BuildShadowCompositionRegularRep(qrecM, resM.shadows, Mord);;
  return regM.regGrp;;
end;;

# ====================================================================
# crown バッテリー本体
# ====================================================================
# 与えられた Xbar(=X/Phi(X))上に、各極大共役類 c の判定器を構成する。
# ★ self-caught バグ(裁定1041/1050発火中に発見): 当初 BuildCrownBattery 内の for ループで
#   quotHom/coreC/Qc/McImageInQc/cosetActHom を「1つのローカル変数」として反復ごとに
#   再代入していたところ、GAP の function-local変数はループ全体で共有される(反復ごとの
#   フレッシュスコープではない)ため、各 testFn クロージャが同じ変数を参照してしまい、
#   全ての class の test が「最後の反復(=最後の class)」のデータだけを見る、という
#   典型的な「ループ変数のクロージャ捕捉」バグを生んだ。較正モード(SB-6)を回した時点で
#   対角成分が真にならない(off-diagonal は 0 だが diag_all_true=false)という形で
#   実際に検出された -- まさに設計ノートが「off-diagonal 発火 = バグ検出器」と述べた
#   較正の趣旨どおり、バグが対角側の異常として捕捉された。
# 修正: 各 class の構成を BuildOneClassTest という別関数呼び出しに切り出し、呼び出し
#   ごとに新しいローカルスコープ(quotHom等)を持たせることでクロージャ捕捉を断つ。
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
    # Qc = Xbar/Mc, regular action -- pass iff image of A is trivial
    testFn := function(A)
      local Aimg;
      Aimg := Image(quotHom, A);;
      return IsTrivial(Aimg);;
    end;;
  else
    # generic fixed-point test via the natural coset action of Qc on Qc/McImageInQc
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
             test_type := "maximal-class", test := testFn);;
end;;

BuildCrownBattery := function(Xbar)
  local classes, n, entries, i;
  classes := ConjugacyClassesMaximalSubgroups(Xbar);;
  n := Length(classes);;
  entries := List([1..n], i -> BuildOneClassTest(Xbar, i, classes[i]));;
  return rec(Xbar := Xbar, n_classes := n, entries := entries);;
end;;

# 較正モード(SB-6): A=M_c を各類について注入し n x n 較正行列を作る。期待=単位行列。
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
# 実行: K(3)/K(9)/K(27)/K(81)/972屋根
# ====================================================================
Print("############################################################\n");
Print("# crown_battery_v1.g -- 裁定1041/1050 一手目(SB-1+SB-6)\n");
Print("############################################################\n");
t0 := GAPLIB_WallElapsedMs();;

results := [];;

RunOne := function(label, X)
  local phiX, Xbar, battery, calib, res;
  Print("\n=== ", label, " ===\n");
  phiX := FrattiniSubgroup(X);;
  Xbar := X/phiX;;
  Print("|X|=", Size(X), " |Phi(X)|=", Size(phiX), " |Xbar|=", Size(Xbar), "\n");
  battery := BuildCrownBattery(Xbar);;
  Print("極大共役類数 = ", battery.n_classes, "\n");
  for e in battery.entries do
    Print("  class ", e.class_id, ": index=", e.index, " normal=", e.normal,
          " |Xbar/Core|=", e.quotient_order, "\n");
  od;
  calib := CalibrateCrownBattery(battery);;
  Print("[", PF(calib.calibration_ok), "] 較正行列(", battery.n_classes, "x", battery.n_classes,
        ") = 単位行列: ", calib.calibration_ok, " (off-diagonal fail count=",
        calib.off_diagonal_fail_count, ")\n");
  res := rec(label := label, size_X := Size(X), size_Phi := Size(phiX), size_Xbar := Size(Xbar),
             n_classes := battery.n_classes,
             classes := List(battery.entries, e -> rec(class_id:=e.class_id, index:=e.index,
                              normal:=e.normal, quotient_order:=e.quotient_order)),
             calibration_ok := calib.calibration_ok,
             off_diagonal_fail_count := calib.off_diagonal_fail_count,
             normal_count := Length(Filtered(battery.entries, e -> e.normal)),
             nonnormal_count := Length(Filtered(battery.entries, e -> not e.normal)));;
  Add(results, res);;
  return res;;
end;;

# K(3)
RunOne("K(3)", BuildGTKnViaAff(3));;
# K(9)(陽性対照候補: census予言=5類・4正規+1非正規)
resK9 := RunOne("K(9)", BuildGTKnViaAff(9));;
k9ClassCountOk := (resK9.n_classes = 5);;
Print("[", PF(k9ClassCountOk), "] K(9) 極大共役類数=5(design doc census予言): ", k9ClassCountOk, "\n");
# K(27)
RunOne("K(27)", BuildGTKnViaAff(27));;
# K(81)
RunOne("K(81)", BuildGTKnViaAff(81));;
# 972屋根(陽性対照候補: census予言=8類・4正規+4非正規)
Print("\n972屋根 M=K^(9) cap N_S4 構成中(ihnec_r4b_run.gパターン再利用・~2分)...\n");
roofG := BuildRoof972();;
resRoof := RunOne("roof-972(M=K(9) cap N_S4)", roofG);;
roofClassCountOk := (resRoof.n_classes = 8);;
Print("[", PF(roofClassCountOk), "] 屋根 極大共役類数=8(design doc census予言): ", roofClassCountOk, "\n");
roofNonNormalOk := (resRoof.nonnormal_count = 4);;
Print("[", PF(roofNonNormalOk), "] 屋根 非正規類数=4(design doc census予言): ", roofNonNormalOk, "\n");

Print("\n============================================================\n");
Print("# 一覧表\n");
Print("============================================================\n");
Print("label | |X| | |Phi| | |Xbar| | n_classes | normal | nonnormal | calib_ok\n");
for r in results do
  Print(r.label, " | ", r.size_X, " | ", r.size_Phi, " | ", r.size_Xbar, " | ", r.n_classes,
        " | ", r.normal_count, " | ", r.nonnormal_count, " | ", r.calibration_ok, "\n");
od;

t1 := GAPLIB_WallElapsedMs();;
Print("\n総経過 = ", t1-t0, " ms\n");

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_crownbat.txt";;
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
    ",\"test_type\":\"maximal-class\"}");
end;;

ResultJson := function(r)
  return Concatenation(
    "{\"label\":\"", r.label, "\",\"size_X\":", String(r.size_X),
    ",\"size_Phi\":", String(r.size_Phi), ",\"size_Xbar\":", String(r.size_Xbar),
    ",\"n_classes\":", String(r.n_classes),
    ",\"normal_count\":", String(r.normal_count), ",\"nonnormal_count\":", String(r.nonnormal_count),
    ",\"classes\":", JArr(List(r.classes, ClassJson)),
    ",\"calibration_ok\":", JB(r.calibration_ok),
    ",\"off_diagonal_fail_count\":", String(r.off_diagonal_fail_count),
    "}"
  );
end;;

scriptSha256 := ComputeSha256File("search/crown_battery_v1.g");;

granularityNote := "本certの全testはtest_type=「maximal-class」(Aがcrown cを代表する極大類M_cのいずれかの共役に含まれるか、の判定)であり、U-6のcrown-covering検定(A*R_c=X)とは異なる述語(surg_universality_audit_v1.md 4.1)。反例: Xbar=S_3でA=C_3はmaximal-class検定PASS(非正規類の不動点あり)だがcrown-coveringはA<>Xbarゆえ被覆しない。混同するとfail-open。";;

cert := Concatenation(
  "{\"schema\":\"crown-battery/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/crown_battery_v1.g\",\"order\":\"裁定1041/1050一手目(SB-1完備性+SB-6較正・器のみ・算術入力なし)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"granularity_note\":\"", granularityNote, "\"",
  ",\"scope_note\":\"検定関数(器)の構築と較正のみ。実際の算術部分群Aによる判定はまだ行っていない。\"",
  ",\"results\":", JArr(List(results, ResultJson)),
  ",\"positive_control\":{",
    "\"K9_n_classes_5\":", JB(k9ClassCountOk),
    ",\"roof972_n_classes_8\":", JB(roofClassCountOk),
    ",\"roof972_nonnormal_4\":", JB(roofNonNormalOk),
    ",\"note\":\"design doc(surg_boost_audit_v1.md 1.4)のcensus予言(K9=5類・屋根=8類・屋根非正規4類)との突合\"",
  "}",
  ",\"u_touched\":false,\"c_touched\":false,\"prereg_value_computed\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/crown_battery_v1_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
