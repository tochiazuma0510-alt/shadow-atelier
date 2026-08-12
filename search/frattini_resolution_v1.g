# search/frattini_resolution_v1.g -- Frattini 解像度表(裁定1033・SURG 第一計器)
#
# 目的: 主要窓群 GT(N) について |X|・|Phi(X)|・|X/Phi(X)|・X/Phi(X) の構造(IdGroup/
#   アーベル不変量)を一覧化する。全射検定は Frattini 商に帰着する(裁定1032【事実FRAT】)
#   ので、その解像度(Frattini 商がどれだけ小さく/大きくなるか)を実測する。
#   純群論・算術入力ゼロ・判定語なし・記述統計級。
#
# 対象: K^(3)・K^(9)(裁定1023の窓、Thm4.3 の陽性対照 |X/Phi|=36 予言つき)。
# 構成: search/derived-census-v2.g の (3.53) shadow 合成則パターンを踏襲(BuildPn +
#   EnumerateReducedHexagon(共通ヘルパー week3-battery-common.g)+ shadow 合成表の正則表現)。
# 847依存監査: BuildPn/BuildShadowCompositionRegularRep は derived-census-v2.g と同一の
#   確立済みパターンを独立再構成(Read() しない)。EnumerateReducedHexagon のみ共通ヘルパー
#   (week3-battery-common.g、多数のscriptがReadする標準インフラ)を利用。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

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
    for j in [1..n] do
      l[j + (i-1)*n] := (j^p) + (i-1)*n;
    od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2) * tr(s,3);;
  q2 := tr(s,1) * tr(s,3);;
  q3 := tr(s,1) * tr(s,2);;
  X := AbstractProd([a1, q1]);;
  Y := AbstractProd([a1, a2, a3, q2]);;
  Xchk := tr(r,1) * tr(s,2) * tr(s,3);;
  Ychk := tr(s*r,1) * tr(r,2) * tr(s*r,3);;
  if X <> Xchk or Y <> Ychk then
    Error("BuildPn: convention mismatch for n=", n);
  fi;
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

# (3.53) [m1,f1] o [m2,f2] = [(2 m1 m2 + m1 + m2) mod Nord, f1 . E_{m1,f1}(f2)]
BuildShadowCompositionRegularRep := function(qrec, shadows, Nord)
  local n, i1, i2, m1, f1, m2, f2, u1, Ehom, newm, newf, idx, t, tbl, closureFail, regGrp;
  n := Length(shadows);;
  tbl := [];;  closureFail := 0;;
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
      idx := fail;;
      for t in [1..n] do
        if shadows[t].m = newm and shadows[t].f = newf then idx := t; break; fi;
      od;
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

# ===================================================================
# Frattini 解像度 1本の計算
# ===================================================================
FrattiniRow := function(name, defn, G, orderTheory)
  local sizeX, phiX, sizePhi, sizeQuot, quotG, quotAbelian, quotAbInv, quotIdGroup, quotIdOk;
  sizeX := Size(G);;
  phiX := FrattiniSubgroup(G);;
  sizePhi := Size(phiX);;
  sizeQuot := sizeX / sizePhi;;
  quotG := G / phiX;;
  quotAbelian := IsAbelian(quotG);;
  quotAbInv := fail;;
  if quotAbelian then
    quotAbInv := AbelianInvariants(quotG);;
  fi;
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
Print("# frattini_resolution_v1.g -- Frattini 解像度表(裁定1033・SURG)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;
rows := [];;

# ---- K(3) ----
Print("\n=== GT(K^(3)) 構成中 ===\n");
gtk3 := BuildGTKn(3);;
if gtk3.reg.closed_observed then
  row3 := FrattiniRow("K(3)", "GT(K^(3))", gtk3.reg.regGrp, gtk3.groupOrderTheory);;
  Add(rows, row3);;
  Print("|X|=", row3.sizeX, " |Phi(X)|=", row3.sizePhi, " |X/Phi(X)|=", row3.sizeQuot,
        " abelian=", row3.quotAbelian, " AbInv=", row3.quotAbInv, "\n");
else
  Print("[HALT] K(3) shadow composition not closed -- reporting raw failure only.\n");
fi;

# ---- K(9)(陽性対照: 数学者手計算 |X/Phi|=36) ----
Print("\n=== GT(K^(9)) 構成中 ===\n");
gtk9 := BuildGTKn(9);;
if gtk9.reg.closed_observed then
  row9 := FrattiniRow("K(9)", "GT(K^(9))", gtk9.reg.regGrp, gtk9.groupOrderTheory);;
  Add(rows, row9);;
  Print("|X|=", row9.sizeX, " |Phi(X)|=", row9.sizePhi, " |X/Phi(X)|=", row9.sizeQuot,
        " abelian=", row9.quotAbelian, " AbInv=", row9.quotAbInv, "\n");
  posControlOk := (row9.sizeQuot = 36);;
  Print("[", PF(posControlOk), "] 陽性対照(数学者手計算): |X/Phi(X)| = 36: ", posControlOk, "\n");
else
  Print("[HALT] K(9) shadow composition not closed -- reporting raw failure only.\n");
fi;

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
  tmp := "search/.tmp_sha256_out_frat.txt";;
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

scriptSha256 := ComputeSha256File("search/frattini_resolution_v1.g");;

cert := Concatenation(
  "{\"schema\":\"frattini-resolution/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/frattini_resolution_v1.g\",\"order\":\"裁定1033(SURG第一計器)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"fact_FRAT_ref\":\"裁定1032【事実FRAT】全射検定はFrattini商に帰着\"",
  ",\"rows\":", JArr(List(rows, RowJson)),
  ",\"positive_control\":{\"name\":\"K(9)\",\"claim\":\"数学者手計算 |X/Phi(X)|=36\",",
    "\"observed\":", String(row9.sizeQuot), ",\"matches\":", JB(row9.sizeQuot = 36), "}",
  ",\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/frattini_resolution_v1_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
