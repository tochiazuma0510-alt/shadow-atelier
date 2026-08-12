# search/frattini_resolution_v2.g -- Frattini 解像度表 v2(裁定1037)
#
# v1(K(3)・K(9))に「合成もつれ屋根」X = GT(M)(M = K^(9) cap N_S4・|X|=972 予言)の行を追加。
#
# 構成: search/probe/wac_v1/ihnec_r4b_run.g の窓構成(MakeGn(9)・S4=GF(8)明示行列・
#   block-diagonal直和埋め込みでM=K9∩N_S4を作る)とScanRoofHexagon(同ファイル)を
#   再利用(このファイルは独立係数計算ではなく既存の確立済み群構成の再実行なので、
#   R4a/R4b の 847依存監査対象そのもの — 発注どおり「search/の該当scriptとcert」を
#   再利用する。ScanRoofHexagonは847監査上「唯一の判定式」として複数窓で共有される
#   設計そのものであり、再入力ではなく正しい再利用)。
# shadows(972個の(m,f)ペア)に (3.53) 合成則 [m1,f1]o[m2,f2] =
#   [(2m1m2+m1+m2) mod Mord, f1.E_{m1,f1}(f2)] を適用し、正則表現として X=GT(M) を
#   具体置換群として構成 -> FrattiniSubgroup(X) を実測。

SizeScreen([4096, 0]);;
Read("search/probe/wac_v1/gap_output_prelude.g");;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ---- v1 由来: K(3)/K(9) 再構成(独立再構成パターン、847監査) ----
BuildPn := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, q3, X, Y, Xchk, Ychk, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("BuildPn: D_n relations failed for n = ", n);
  fi;
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2) * tr(s,3);;  q2 := tr(s,1) * tr(s,3);;  q3 := tr(s,1) * tr(s,2);;
  X := AbstractProd([a1, q1]);;  Y := AbstractProd([a1, a2, a3, q2]);;
  Xchk := tr(r,1) * tr(s,2) * tr(s,3);;
  Ychk := tr(s*r,1) * tr(r,2) * tr(s*r,3);;
  if X <> Xchk or Y <> Ychk then Error("BuildPn: convention mismatch for n=", n); fi;
  Gfull := Group(a1, a2, a3, q1, q2);;
  return rec(n:=n, a1:=a1, a2:=a2, a3:=a3, q1:=q1, q2:=q2, q3:=q3, X:=X, Y:=Y, G:=Gfull);
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
  # dictionary keyed by [m,f] for O(1) lookup instead of O(n) linear scan (n=972 here,
  # O(n) scan per pair would give O(n^3) total -- too slow; O(n^2) with dict is fine)
  idxDict := NewDictionary([shadows[1].m, shadows[1].f], true);;
  for t in [1..n] do
    AddDictionary(idxDict, [shadows[t].m, shadows[t].f], t);;
  od;
  for i1 in [1..n] do
    m1 := shadows[i1].m;;  f1 := shadows[i1].f;;  u1 := 2*m1+1;;
    Ehom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y],
              [qrec.x^u1, AbstractProd([f1^-1, qrec.y^u1, f1])]);;
    if Ehom = fail then
      Error("BuildShadowCompositionRegularRep: E_{m1,f1} construction failed, i1=", i1);
    fi;
    for i2 in [1..n] do
      m2 := shadows[i2].m;;  f2 := shadows[i2].f;;
      newm := (2*m1*m2 + m1 + m2) mod Nord;;
      newf := AbstractProd([f1, Image(Ehom, f2)]);;
      key := [newm, newf];;
      idx := LookupDictionary(idxDict, key);;
      if idx = fail then
        closureFail := closureFail + 1;;
        Add(tbl, [i1-1, i2-1, -1]);;
      else
        Add(tbl, [i1-1, i2-1, idx-1]);;
      fi;
    od;
  od;
  if closureFail > 0 then
    return rec(regGrp:=fail, closed_observed:=false, closure_fail_count:=closureFail, shadow_total:=n);;
  fi;
  regGrp := BuildRegularPermGroupFromTable(tbl, n);;
  return rec(regGrp:=regGrp, closed_observed:=true, closure_fail_count:=0, shadow_total:=n);;
end;;

# ScanRoofHexagon: 逐語 search/probe/wac_v1/ihnec_r4b_run.g(裁定376)と数学的に同一
# (theta/tau・hex310・hex311・生成条件。列挙戦略= Elements(DerivedSubgroup(G)) 直接列挙)。
ScanRoofHexagon := function(qrec, charmingSet)
  local G, D, Delts, thetaHom, tauHom, zElt, h10Fail, h11Fail, genFail, shadows,
        m, u, f, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj,
        candidateTotal, i;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  if thetaHom = fail or tauHom = fail then
    Error("ScanRoofHexagon: theta/tau homomorphism construction failed");
  fi;
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
      if not surj then
        genFail := genFail + 1;
      else
        Add(shadows, rec(m := m, f := f));
      fi;
    od;
  od;
  return rec(candidate_total := candidateTotal, h10_fail := h10Fail, h11_fail := h11Fail,
             generation_fail := genFail, shadow_total := Length(shadows), shadows := shadows,
             derived_order := Length(Delts));
end;;

BuildGTKn := function(n)
  local Pn, qrec, Nord, charmingSet, gtResult, phi_n, groupOrderTheory, reg;
  Pn := BuildPn(n);;
  qrec := rec(x:=Pn.X, y:=Pn.Y, c:=One(Pn.G), G:=Pn.G);;
  Nord := Lcm(Order(Pn.X), Order(Pn.Y));;
  charmingSet := Filtered([0..Nord-1], mm -> Gcd(2*mm+1, Nord) = 1);;
  gtResult := EnumerateReducedHexagon(qrec, charmingSet);;
  phi_n := Length(Filtered([1..n], k -> Gcd(k,n)=1));;
  groupOrderTheory := 2 * n * phi_n;;
  reg := BuildShadowCompositionRegularRep(qrec, gtResult.shadows, Nord);;
  return rec(n:=n, groupOrderTheory:=groupOrderTheory, reg:=reg);;
end;;

FrattiniRow := function(name, defn, G, orderTheory)
  local sizeX, phiX, sizePhi, sizeQuot, quotG, quotAbelian, quotAbInv, quotIdGroup, quotIdOk;
  sizeX := Size(G);;
  phiX := FrattiniSubgroup(G);;
  sizePhi := Size(phiX);;
  sizeQuot := sizeX / sizePhi;;
  quotG := G / phiX;;
  quotAbelian := IsAbelian(quotG);;
  quotAbInv := fail;;
  if quotAbelian then quotAbInv := AbelianInvariants(quotG);; fi;
  quotIdGroup := fail;;  quotIdOk := false;;
  if sizeQuot <= 2000 then
    quotIdGroup := IdGroup(quotG);;
    quotIdOk := true;;
  fi;
  return rec(name:=name, defn:=defn, orderTheory:=orderTheory,
             sizeX:=sizeX, sizeMatchesTheory:=(orderTheory=fail or sizeX=orderTheory),
             sizePhi:=sizePhi, sizeQuot:=sizeQuot,
             quotAbelian:=quotAbelian, quotAbInv:=quotAbInv,
             quotIdGroup:=quotIdGroup, quotIdOk:=quotIdOk);;
end;;

Print("############################################################\n");
Print("# frattini_resolution_v2.g -- Frattini 解像度表 v2(裁定1037)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;
rows := [];;

# ---- K(3) ----
Print("\n=== GT(K^(3)) 構成中 ===\n");
gtk3 := BuildGTKn(3);;
row3 := FrattiniRow("K(3)", "GT(K^(3))", gtk3.reg.regGrp, gtk3.groupOrderTheory);;
Add(rows, row3);;
Print("|X|=", row3.sizeX, " |Phi(X)|=", row3.sizePhi, " |X/Phi(X)|=", row3.sizeQuot, "\n");

# ---- K(9)(陽性対照) ----
Print("\n=== GT(K^(9)) 構成中 ===\n");
gtk9 := BuildGTKn(9);;
row9 := FrattiniRow("K(9)", "GT(K^(9))", gtk9.reg.regGrp, gtk9.groupOrderTheory);;
Add(rows, row9);;
Print("|X|=", row9.sizeX, " |Phi(X)|=", row9.sizePhi, " |X/Phi(X)|=", row9.sizeQuot, "\n");
posControlOk := (row9.sizeQuot = 36);;
Print("[", PF(posControlOk), "] 陽性対照: K(9) |X/Phi(X)| = 36: ", posControlOk, "\n");

# ---- M = K^(9) cap N_S4(合成もつれ屋根、|X|予言=972) ----
Print("\n=== 窓 M := K^(9) cap N_S4(ihnec_r4b_run.g パターン再利用)構成中 ===\n");
tM0 := GAPLIB_WallElapsedMs();;

g9 := MakeGn(9);;
if Size(g9.G) <> 2916 or Lcm(Order(g9.x), Order(g9.y)) <> 18 then
  Error("frattini_resolution_v2: K9 window construction mismatch -- refusing to proceed");
fi;

CheckGF8();;
Smat := MakeMatGF8(1,0,1,1);;
Tmat := MakeMatGF8(4,3,1,5);;
Sperm := MatToPermGF8(Smat);;
Tperm := MatToPermGF8(Tmat);;
wPerm := Sperm * Tperm^-1;;
Xperm := wPerm^2;;
Yperm := Sperm^-1 * Xperm * Sperm;;
Pgrp := Group(Xperm, Yperm);;
if Size(Pgrp) <> 504 or Lcm(Order(Xperm), Order(Yperm)) <> 9 then
  Error("frattini_resolution_v2: S4 window construction mismatch -- refusing to proceed");
fi;

ShiftPerm := function(p, offset, size)
  local l, j;
  l := [1 .. offset+size];
  for j in [1 .. size] do l[offset+j] := offset + (j^p); od;
  return PermList(l);
end;;
DirectSumPerm := function(p1, deg1, p2, deg2)
  return p1 * ShiftPerm(p2, deg1, deg2);
end;;
XM := DirectSumPerm(g9.x, 27, Xperm, 9);;
YM := DirectSumPerm(g9.y, 27, Yperm, 9);;
GM := Group(XM, YM);;
Mord := Lcm(Order(XM), Order(YM));;
if Size(GM) <> 2916*504 or Mord <> 18 then
  Error("frattini_resolution_v2: M window construction mismatch (|PB3/M| or M_ord) -- refusing to proceed");
fi;
Mcharm := Filtered([0..Mord-1], mm -> Gcd(2*mm+1, Mord) = 1);;
Print("  |PB3/M|=", Size(GM), " M_ord=", Mord, " charming_set_M=", Mcharm, " (|.|=", Length(Mcharm), ")\n");

qrecM := rec(x := XM, y := YM, G := GM);;
Print("  ScanRoofHexagon(M, 全charming) 実行中(derived_order 予言=367416)...\n");
tScan0 := GAPLIB_WallElapsedMs();;
resM := ScanRoofHexagon(qrecM, Mcharm);;
tScan1 := GAPLIB_WallElapsedMs();;
Print("  derived_order=", resM.derived_order, " candidate_total=", resM.candidate_total,
      " shadow_total=", resM.shadow_total, " (期待 972)  elapsed_ms=", tScan1-tScan0, "\n");
shadowTotalOk := (resM.shadow_total = 972);;
Print("[", PF(shadowTotalOk), "] shadow_total = 972: ", shadowTotalOk, "\n");
if not shadowTotalOk then
  Error("frattini_resolution_v2: shadow_total <> 972 -- refusing to build X=GT(M) on an "
        , "unexpected shadow set (fail-closed).");
fi;

Print("  BuildShadowCompositionRegularRep(M, 972 shadows) 実行中...\n");
tReg0 := GAPLIB_WallElapsedMs();;
regM := BuildShadowCompositionRegularRep(qrecM, resM.shadows, Mord);;
tReg1 := GAPLIB_WallElapsedMs();;
Print("  closed_observed=", regM.closed_observed, " closure_fail_count=", regM.closure_fail_count,
      " elapsed_ms=", tReg1-tReg0, "\n");

if not regM.closed_observed then
  Print("[HALT] X=GT(M) の shadow 合成則が閉じていない -- 生の失敗のみ報告、Frattini計算に進まない。\n");
else
  rowM := FrattiniRow("M(=K(9) cap N_S4)", "GT(M), M = K^(9) cap N_S4(合成もつれ屋根)",
                       regM.regGrp, 972);;
  Add(rows, rowM);;
  Print("|X|=", rowM.sizeX, " |Phi(X)|=", rowM.sizePhi, " |X/Phi(X)|=", rowM.sizeQuot,
        " abelian=", rowM.quotAbelian, " AbInv=", rowM.quotAbInv, " IdGroup=", rowM.quotIdGroup, "\n");
fi;
tM1 := GAPLIB_WallElapsedMs();;
Print("  M 全体所要 = ", tM1-tM0, " ms\n");

Print("\n============================================================\n");
Print("# 一覧表\n");
Print("============================================================\n");
Print("name | |X| | |Phi(X)| | |X/Phi(X)| | abelian | AbInv | IdGroup\n");
for r in rows do
  Print(r.name, " | ", r.sizeX, " | ", r.sizePhi, " | ", r.sizeQuot, " | ",
        r.quotAbelian, " | ", r.quotAbInv, " | ", r.quotIdGroup, "\n");
od;

t1 := GAPLIB_WallElapsedMs();;
Print("\n総経過 = ", t1-t0, " ms\n");

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_frat2.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

RowJson := function(r)
  local abInvStr, idGroupStr;
  if r.quotAbInv = fail then abInvStr := "null"; else abInvStr := JArr(List(r.quotAbInv,String)); fi;
  if r.quotIdOk then idGroupStr := JArr(List(r.quotIdGroup, String)); else idGroupStr := "null"; fi;
  return Concatenation(
    "{\"name\":\"", r.name, "\",\"definition\":\"", r.defn, "\"",
    ",\"order_theory\":", String(r.orderTheory), ",\"size_X\":", String(r.sizeX),
    ",\"size_matches_theory\":", JB(r.sizeMatchesTheory),
    ",\"size_Phi\":", String(r.sizePhi), ",\"size_X_mod_Phi\":", String(r.sizeQuot),
    ",\"quotient_abelian\":", JB(r.quotAbelian),
    ",\"quotient_abelian_invariants\":", abInvStr,
    ",\"quotient_IdGroup\":", idGroupStr,
    "}"
  );
end;;

scriptSha256 := ComputeSha256File("search/frattini_resolution_v2.g");;

cert := Concatenation(
  "{\"schema\":\"frattini-resolution/v2\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/frattini_resolution_v2.g\",\"order\":\"裁定1037(SURG joint適用第一データ)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"fact_FRAT_ref\":\"裁定1032【事実FRAT】全射検定はFrattini商に帰着\"",
  ",\"source_reuse_note\":\"M窓の構成・ScanRoofHexagonはsearch/probe/wac_v1/ihnec_r4b_run.g(裁定376)のパターンを再利用(847監査対象・発注どおり既存資産の再利用)\"",
  ",\"rows\":", JArr(List(rows, RowJson)),
  ",\"positive_control\":{\"name\":\"K(9)\",\"claim\":\"数学者手計算 |X/Phi(X)|=36\",",
    "\"observed\":", String(row9.sizeQuot), ",\"matches\":", JB(row9.sizeQuot = 36), "}",
  ",\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/frattini_resolution_v2_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
