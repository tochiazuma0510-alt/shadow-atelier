# search/frattini_resolution_v3.g -- Frattini 解像度表 v3(裁定1046-1・族公式テスト)
#
# F(K^(n)) = GT(K^(n))/Phi を n = 3,9,15,21,27,33 で実測し、予言式
#   F(K^(n)) =? (Z/rad(n) x| (Z/n)^x) x C2   (docs/notes/ideas_surg_universality_v1.md U-2 (T2))
# の位数 2*rad(n)*phi(n) と突合する(n=27 が破れ候補と予言されている)。
# 構成は v1/v2 と同一の (3.53) shadow 合成則パターンの流用(BuildPn/EnumerateReducedHexagon)。
# 範囲の申告: 予言側の群を GAP で明示構成しての完全同型判定(IdGroup突合)は本ラウンドでは
# 行わず、位数の一致/不一致(生値)のみを報告する(拙速な半直積構成によるバグ混入回避)。

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
  idxDict := NewDictionary([shadows[1].m, shadows[1].f], true);;
  for t in [1..n] do AddDictionary(idxDict, [shadows[t].m, shadows[t].f], t);; od;
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

RadicalOf := function(n)
  local p, r;
  r := 1;;
  for p in Set(Factors(n)) do r := r * p; od;
  return r;;
end;;

FrattiniRow := function(name, defn, G, orderTheory, nVal, radVal, phiVal)
  local sizeX, phiX, sizePhi, sizeQuot, quotG, quotAbelian, quotAbInv, quotIdGroup, quotIdOk,
        predictedOrder, orderMatchesPredicted;
  sizeX := Size(G);;
  phiX := FrattiniSubgroup(G);;
  sizePhi := Size(phiX);;
  sizeQuot := sizeX / sizePhi;;
  quotG := G / phiX;;
  quotAbelian := IsAbelian(quotG);;
  quotAbInv := fail;;
  if quotAbelian then quotAbInv := AbelianInvariants(quotG);; fi;
  quotIdGroup := fail;;  quotIdOk := false;;
  if sizeQuot <= 4000 then
    quotIdGroup := IdGroup(quotG);;
    quotIdOk := true;;
  fi;
  predictedOrder := 2 * radVal * phiVal;;
  orderMatchesPredicted := (sizeQuot = predictedOrder);;
  return rec(name:=name, defn:=defn, orderTheory:=orderTheory,
             sizeX:=sizeX, sizeMatchesTheory:=(orderTheory=fail or sizeX=orderTheory),
             sizePhi:=sizePhi, sizeQuot:=sizeQuot,
             quotAbelian:=quotAbelian, quotAbInv:=quotAbInv,
             quotIdGroup:=quotIdGroup, quotIdOk:=quotIdOk,
             n:=nVal, rad:=radVal, phi_n:=phiVal, predictedOrder:=predictedOrder,
             orderMatchesPredicted:=orderMatchesPredicted);;
end;;

Print("############################################################\n");
Print("# frattini_resolution_v3.g -- 族公式テスト(裁定1046-1)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;
rows := [];;
targetNs := [3, 9, 15, 21, 27, 33];;

for nn in targetNs do
  Print("\n=== GT(K^(", nn, ")) 構成中 ===\n");
  tn0 := GAPLIB_WallElapsedMs();;
  gtkn := BuildGTKn(nn);;
  if not gtkn.reg.closed_observed then
    Print("[HALT] K(", nn, ") shadow composition not closed -- raw failure only.\n");
  else
    radn := RadicalOf(nn);;
    phin := Length(Filtered([1..nn], k -> Gcd(k,nn)=1));;
    rown := FrattiniRow(Concatenation("K(", String(nn), ")"),
                         Concatenation("GT(K^(", String(nn), "))"),
                         gtkn.reg.regGrp, gtkn.groupOrderTheory, nn, radn, phin);;
    Add(rows, rown);;
    tn1 := GAPLIB_WallElapsedMs();;
    Print("|X|=", rown.sizeX, " |Phi(X)|=", rown.sizePhi, " |X/Phi(X)|=", rown.sizeQuot,
          " rad(n)=", radn, " phi(n)=", phin, " predicted=2*rad*phi=", rown.predictedOrder,
          " match=", rown.orderMatchesPredicted, " elapsed_ms=", tn1-tn0, "\n");
  fi;
od;

Print("\n============================================================\n");
Print("# 一覧表\n");
Print("============================================================\n");
Print("n | |X| | |Phi(X)| | |X/Phi(X)| | rad(n) | phi(n) | predicted(2*rad*phi) | match | IdGroup\n");
for r in rows do
  Print(r.n, " | ", r.sizeX, " | ", r.sizePhi, " | ", r.sizeQuot, " | ", r.rad, " | ",
        r.phi_n, " | ", r.predictedOrder, " | ", r.orderMatchesPredicted, " | ", r.quotIdGroup, "\n");
od;

posControlRow := First(rows, r -> r.n = 9);;
posControlOk := (posControlRow <> fail and posControlRow.sizeQuot = 36);;
Print("\n[", PF(posControlOk), "] 陽性対照: K(9) |X/Phi(X)| = 36: ", posControlOk, "\n");

t1 := GAPLIB_WallElapsedMs();;
Print("\n総経過 = ", t1-t0, " ms\n");

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_frat3.txt";;
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
    ",\"n\":", String(r.n), ",\"rad_n\":", String(r.rad), ",\"phi_n\":", String(r.phi_n),
    ",\"order_theory\":", String(r.orderTheory), ",\"size_X\":", String(r.sizeX),
    ",\"size_matches_theory\":", JB(r.sizeMatchesTheory),
    ",\"size_Phi\":", String(r.sizePhi), ",\"size_X_mod_Phi\":", String(r.sizeQuot),
    ",\"predicted_order_2_rad_phi\":", String(r.predictedOrder),
    ",\"order_matches_predicted\":", JB(r.orderMatchesPredicted),
    ",\"quotient_abelian\":", JB(r.quotAbelian),
    ",\"quotient_abelian_invariants\":", abInvStr,
    ",\"quotient_IdGroup\":", idGroupStr,
    "}"
  );
end;;

scriptSha256 := ComputeSha256File("search/frattini_resolution_v3.g");;

cert := Concatenation(
  "{\"schema\":\"frattini-resolution/v3\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/frattini_resolution_v3.g\",\"order\":\"裁定1046-1(族公式テスト)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"family_formula_ref\":\"docs/notes/ideas_surg_universality_v1.md U-2 (T2): F(K^(n)) =? (Z/rad(n) x| (Z/n)^x) x C2\"",
  ",\"scope_note\":\"予言側の群のGAP明示構成・完全同型判定(IdGroup突合)は未実施。位数の一致/不一致(生値)のみ報告。\"",
  ",\"rows\":", JArr(List(rows, RowJson)),
  ",\"positive_control\":{\"name\":\"K(9)\",\"claim\":\"数学者手計算 |X/Phi(X)|=36\",",
    "\"observed\":", String(posControlRow.sizeQuot), ",\"matches\":", JB(posControlOk), "}",
  ",\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/frattini_resolution_v3_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
