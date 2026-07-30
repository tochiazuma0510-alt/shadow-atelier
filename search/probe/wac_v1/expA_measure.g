#############################################################################
## search/probe/wac_v1/expA_measure.g
##   実験 A(裁定 243 工程 1)工程 2・3:
##   (A) 訂正予言 P6 の検証 — n=10 λ=(9,1) の canonical 窓で
##       「hexagon+全射を満たす f」= 54 個 に対し「shadow(settled 込み)」が何個か。
##       C_Sn(v)-軌道ごとの内訳を出す。
##   (B) 予想 PASSPORT の判定 — n=10 λ=(7,3)(N_gen=3・既測窓の外の passport)の
##       3 軌道から 3 窓を作り、kerchi-judge の実物で GTSh を測って比較。
##
## 入力: なし(自己完結)。JUDGE は search/kerchi-judge.g を LIBRARY_ONLY で使用。
## **f_orientation: judge**(f_judge = a1 * g、訂正版定理 SURV の向き)。
##   手書き向き f_hand = g * a1 は本 probe では一切使わない(混用禁止・裁定ノート §4)。
## 出力: 標準出力 + search/certs/expA_passport_20260731.json
## 検査する不変量:
##   K1: (A) の 54 個のうち hexagon+全射は 54/54(定理 RED の再確認)
##   K2: (A) の基点軌道 9 個はすべて shadow(定理 SURV の再確認)
##   K3: (B) の 3 窓で |GTSh| / IdGroup / ker 構造 / Ξ 像が一致するか(PASSPORT の判定)
##   K4: (B) の Ξ 像は定理 CENT-0 により C_S10(w0)(位数 21)でなければならない
## Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
JUDGE_LIBRARY_ONLY := true;;
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g");
PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

MakePermFromType := function(lambda)
  local L, pos, part, i;
  L := [];  pos := 0;
  for part in lambda do
    for i in [1..part-1] do L[pos+i] := pos+i+1; od;
    L[pos+part] := pos+1;
    pos := pos + part;
  od;
  return PermList(L);
end;;

MakeInvol := function(n, k)
  local L, i;
  L := [1..n];
  for i in [1..k] do L[2*i-1] := 2*i;  L[2*i] := 2*i-1; od;
  return PermList(L);
end;;

BuildS1S2E := function(a1, b1, n)
  local Sn, S3, Dgrp, embA, embS, agen, bgen;
  Sn := SymmetricGroup(n);;  S3 := SymmetricGroup(3);;
  Dgrp := DirectProduct(Sn, S3);;
  embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
  agen := Image(embA, a1) * Image(embS, (1,3));;
  bgen := Image(embA, b1) * Image(embS, (1,3,2));;
  return rec(s1 := bgen^-1 * agen, s2 := agen^-1 * bgen^2,
             Dgrp := Dgrp, embA := embA, agen := agen, bgen := bgen);
end;;

## w-径数付け: b1^-1*a1 = w0 なる生成対をすべて集め、C_Sn(w0)-軌道に分ける
OrbitsOfWindows := function(n, w0)
  local Sn, half, F, k, cl, a1, b1, C, Cel, rem, r, orb, orbs;
  Sn := SymmetricGroup(n);  half := Factorial(n)/2;
  F := [];
  for k in [0 .. QuoInt(n,2)] do
    cl := Elements(ConjugacyClass(Sn, MakeInvol(n,k)));
    for a1 in cl do
      b1 := a1 * w0^-1;
      if b1^3 <> () then continue; fi;
      if Size(Group(a1,b1)) < half then continue; fi;
      Add(F, [a1,b1]);
    od;
  od;
  C := Centralizer(Sn, w0);  Cel := Elements(C);
  rem := Set(F);  orbs := [];
  while not IsEmpty(rem) do
    r := rem[1];
    orb := Set(List(Cel, z -> [r[1]^z, r[2]^z]));
    Add(orbs, rec(rep := r, size := Length(orb)));
    rem := Difference(rem, orb);
  od;
  return rec(F := F, orbs := orbs, C := C);
end;;

#############################################################################
## ==== (A) 訂正予言 P6: hexagon 解 54 個 vs shadow 何個か ====================
#############################################################################
Print("\n############ (A) n=10, lambda=(9,1): hexagon 解 vs shadow ############\n");
nA := 10;;  w0A := MakePermFromType([9,1]);;
oA := OrbitsOfWindows(nA, w0A);;
Print("  |F| (hexagon+全射の生成対) = ", Length(oA.F),
      "   |C_Sn(w0)| = ", Size(oA.C),
      "   N_gen (= C(w0)-軌道数) = ", Length(oA.orbs), "\n");

## 工房の既存窓表(strike-a13-ladder.g)の a1 と軌道の対応を照合
LADDER := [ rec(id:="W-E-A10-9t1",  a1:=( 1, 2)( 3, 5)( 4,10)( 6, 9)),
            rec(id:="W-E-A10-9t1-o2", a1:=( 3, 9)( 4, 6)( 5,10)( 7, 8)),
            rec(id:="W-E-A10-9t1-o3", a1:=( 2, 3)( 4, 9)( 6, 8)( 7,10)),
            rec(id:="W-E-A10-9t1-o4", a1:=( 2, 3)( 4, 9)( 5, 7)( 6,10)),
            rec(id:="W-E-A10-9t1-o5", a1:=( 2, 4)( 3,10)( 5, 9)( 6, 7)),
            rec(id:="W-E-A10-9t1-o6", a1:=( 2, 6)( 3, 4)( 7, 9)( 8,10)) ];;
Print("  -- 工房の既存 6 窓が本当に別軌道か(照合)--\n");
for L in LADDER do
  L.b1 := L.a1 * w0A^-1;
  L.orbidx := First([1..Length(oA.orbs)],
                    i -> [L.a1,L.b1] in Set(List(Elements(oA.C),
                          z -> [oA.orbs[i].rep[1]^z, oA.orbs[i].rep[2]^z])));
  Print("     ", L.id, " -> 軌道 #", L.orbidx, "\n");
od;
Print("  6 窓が 6 つの相異なる軌道か: ",
      PF(Size(Set(List(LADDER, L -> L.orbidx))) = 6), "\n");

## canonical 窓を基点にして、全 54 個の f_judge に judge の m=0 条件を当てる
baseA := LADDER[1];;
bltA := BuildS1S2E(baseA.a1, baseA.b1, nA);;
WA := MakeWindow(bltA.s1, bltA.s2);;
vA := baseA.a1 * baseA.b1^-1;;                 ## RED の固定元 v = a1 b1^-1
CvA := Centralizer(SymmetricGroup(nA), vA);;
Print("  基点窓 = ", baseA.id, "   N_ord = ", WA.Nord,
      "   c in N = ", WA.c = Identity(WA.Bq),
      "   |C_Sn(v)| = ", Size(CvA), "\n");

## v-径数付けで g を列挙(g^2=1, (g v)^3=1, 生成)
GsetA := [];;
for k in [0 .. QuoInt(nA,2)] do
  for g in Elements(ConjugacyClass(SymmetricGroup(nA), MakeInvol(nA,k))) do
    if (g*vA)^3 <> () then continue; fi;
    if Size(Group(g, g*vA)) < Factorial(nA)/2 then continue; fi;
    Add(GsetA, g);
  od;
od;
Print("  |F(v)| (v-径数付け) = ", Length(GsetA), "\n");

## C(v)-軌道分解(基点軌道 = a1 の軌道)
CvEl := Elements(CvA);;
remA := Set(GsetA);;  orbsV := [];;
while not IsEmpty(remA) do
  rr := remA[1];
  orb := Set(List(CvEl, z -> rr^z));
  Add(orbsV, orb);
  remA := Difference(remA, orb);
od;
baseOrbIdx := First([1..Length(orbsV)], i -> baseA.a1 in orbsV[i]);;
Print("  C(v)-軌道数 = ", Length(orbsV), "   基点 a1 が入る軌道 = #", baseOrbIdx, "\n");

Print("\n  軌道 | 大きさ | hexagon(3.10) | hexagon(3.11) | 全射 | settled | shadow\n");
totShadowA := 0;;
rowsA := [];;
for i in [1 .. Length(orbsV)] do
  c1 := 0;; c2 := 0;; c3 := 0;; c4 := 0;; cs := 0;;
  for g in orbsV[i] do
    fj := Image(bltA.embA, baseA.a1 * g);        ## f_orientation = judge
    t1 := AbstractProd([fj, TH(WA, fj)]) = Identity(WA.Bq);
    t2 := RtOf(WA, 0, fj) = WA.c^0;
    t3 := Size(Group(WA.x, AbstractProd([fj^-1, WA.y, fj]))) = Size(WA.PN);
    t4 := false;
    if t1 and t2 and t3 then
      t4 := GroupHomomorphismByImages(WA.Bq, WA.Bq, [WA.s1, WA.s2],
              [WA.s1, AbstractProd([fj^-1, WA.s2, fj])]) <> fail;
    fi;
    if t1 then c1 := c1+1; fi;
    if t2 then c2 := c2+1; fi;
    if t3 then c3 := c3+1; fi;
    if t4 then c4 := c4+1; fi;
    if t1 and t2 and t3 and t4 then cs := cs+1; fi;
  od;
  totShadowA := totShadowA + cs;
  Add(rowsA, rec(orb := i, size := Length(orbsV[i]), h1 := c1, h2 := c2,
                 surj := c3, settled := c4, shadow := cs));
  Print("   #", i, " | ", Length(orbsV[i]), " | ", c1, " | ", c2, " | ", c3,
        " | ", c4, " | ", cs);
  if i = baseOrbIdx then Print("   <= 基点軌道\n"); else Print("\n"); fi;
od;
Print("  --> shadow 合計 = ", totShadowA, "   (|C(v)| = ", Size(CvA),
      ", |F(v)| = ", Length(GsetA), ")\n");
Print("  K1 (hexagon+全射が |F| 全部) = ",
      PF(ForAll(rowsA, r -> r.h1 = r.size and r.h2 = r.size and r.surj = r.size)), "\n");
Print("  K2 (基点軌道が全部 shadow) = ",
      PF(rowsA[baseOrbIdx].shadow = rowsA[baseOrbIdx].size), "\n");
Print("  P6 判定: N_shadow = ", Length(Filtered(rowsA, r -> r.shadow > 0)),
      "  vs  N_gen = ", Length(orbsV), "\n");

#############################################################################
## ==== (B) PASSPORT 判定: n=10, lambda=(7,3), 3 軌道 =========================
#############################################################################
Print("\n############ (B) n=10, lambda=(7,3): 3 窓の GTSh 比較 ############\n");
nB := 10;;  w0B := MakePermFromType([7,3]);;
oB := OrbitsOfWindows(nB, w0B);;
Print("  w0 = ", w0B, "   |C_Sn(w0)| = ", Size(oB.C),
      "   N_gen = ", Length(oB.orbs), "   |F| = ", Length(oB.F), "\n");

MeasureWindow := function(a1, b1, n, label)
  local blt, W, charming, res, gi, Sdeg, Stab, kerf, xis, al, r, kg, m0;
  blt := BuildS1S2E(a1, b1, n);
  W := MakeWindow(blt.s1, blt.s2);
  charming := Filtered([0 .. W.Nord-1], m -> Gcd(2*m+1, W.Nord) = 1);
  Print("\n  --- ", label, " ---\n");
  Print("    a1 = ", a1, "\n    b1 = ", b1, "\n");
  Print("    |E|=", Size(W.Bq), "  |P|=", Size(W.PN), "  c in N=", W.c = Identity(W.Bq),
        "  N_ord=", W.Nord, "  charming=", Length(charming),
        "  phi(2N)=", Phi(2*W.Nord), "\n");
  Print("    <a1,b1> = ", StructureDescription(Group(a1,b1)),
        "   sgn(a1) = ", SignPerm(a1), "  (eps=0 <=> +1)\n");
  res := CorrectedShadows(W, charming);
  gi := GroupOfShadows(W, res.shadows);
  if not gi.closed then
    Print("    !! (3.53) closure FAILED\n");
    return rec(label := label, closed := false);
  fi;
  m0 := Filtered(res.shadows, s -> s[1] = 0);
  ## Xi 像(m=0 層)
  Sdeg := SymmetricGroup(MovedPoints(W.PN));
  Stab := Centralizer(Sdeg, W.x);
  xis := [];
  for r in m0 do
    al := First(Elements(Stab), a -> W.y^a = r[2]*W.y*r[2]^-1);
    if al = fail then Print("    !! Xi undefined for a shadow -- fail closed\n"); fi;
    Add(xis, al);
  od;
  kg := Group(xis);
  Print("    shadow_total=", Length(res.shadows), " settled_fail=", res.settled_fail_count,
        " scan_mode=", res.scan_mode, " scanned=", res.scanned_count, "\n");
  Print("    |GTSh| = ", gi.order, "   IdGroup = ", IdGroup(gi.G),
        "   Struct = ", StructureDescription(gi.G), "\n");
  Print("    |ker chi~| = ", Length(m0), "   ker IdGroup = ", IdGroup(gi.ker),
        "   ker Struct = ", StructureDescription(gi.ker),
        "   abelian=", IsAbelian(gi.ker), "\n");
  Print("    |Stab(xbar)| = ", Size(Stab), "   |Xi(ker)| = ", Size(kg),
        "   Xi Struct = ", StructureDescription(kg),
        "   Xi injective = ", Size(kg) = Length(m0), "\n");
  Print("    derived_series = ", List(DerivedSeries(gi.G), Size),
        "   solvable=", IsSolvable(gi.G), "\n");
  return rec(label := label, closed := true, a1 := a1, b1 := b1,
             order := gi.order, idg := IdGroup(gi.G),
             struct := StructureDescription(gi.G),
             kersize := Length(m0), keridg := IdGroup(gi.ker),
             kerstruct := StructureDescription(gi.ker),
             xisize := Size(kg), xistruct := StructureDescription(kg),
             stabsize := Size(Stab), nord := W.Nord,
             charming := Length(charming), shadow_total := Length(res.shadows),
             settled_fail := res.settled_fail_count,
             sgn := SignPerm(a1), amb := StructureDescription(Group(a1,b1)));
end;;

RESB := [];;
for i in [1 .. Length(oB.orbs)] do
  Add(RESB, MeasureWindow(oB.orbs[i].rep[1], oB.orbs[i].rep[2], nB,
                          Concatenation("W-P-A10-73-o", String(i))));
od;

Print("\n  === (B) 比較表 ===\n");
Print("  窓 | |GTSh| | IdGroup | ker | ker IdGroup | |Xi(ker)| | N_ord | charming | sgn(a1)\n");
for r in RESB do
  Print("  ", r.label, " | ", r.order, " | ", r.idg, " | ", r.kersize, " | ",
        r.keridg, " | ", r.xisize, " | ", r.nord, " | ", r.charming, " | ", r.sgn, "\n");
od;
allsame := Size(Set(List(RESB, r -> [r.order, r.idg, r.kersize, r.keridg, r.xisize]))) = 1;;
Print("\n  K3 (3 窓すべて一致 = PASSPORT 支持) = ", PF(allsame), "\n");
Print("  K4 (|Xi(ker)| = |C_Sn(w0)| = ", Size(oB.C), ") = ",
      PF(ForAll(RESB, r -> r.xisize = Size(oB.C))), "\n");

#############################################################################
## ---- cert ----------------------------------------------------------------
#############################################################################
JRow := function(r)
  return Concatenation("{\"label\":", JStr(r.label),
    ",\"a1\":", JStr(String(r.a1)), ",\"b1\":", JStr(String(r.b1)),
    ",\"gtsh_order\":", String(r.order),
    ",\"gtsh_idgroup\":", JPair(r.idg[1], r.idg[2]),
    ",\"gtsh_struct\":", JStr(r.struct),
    ",\"ker_size\":", String(r.kersize),
    ",\"ker_idgroup\":", JPair(r.keridg[1], r.keridg[2]),
    ",\"ker_struct\":", JStr(r.kerstruct),
    ",\"xi_image_order\":", String(r.xisize),
    ",\"xi_image_struct\":", JStr(r.xistruct),
    ",\"stab_xbar_order\":", String(r.stabsize),
    ",\"N_ord\":", String(r.nord),
    ",\"charming_count\":", String(r.charming),
    ",\"shadow_total\":", String(r.shadow_total),
    ",\"settled_fail_count\":", String(r.settled_fail),
    ",\"sgn_a1\":", String(r.sgn),
    ",\"ambient\":", JStr(r.amb), "}");
end;;
JRowA := function(r)
  return Concatenation("{\"orbit\":", String(r.orb), ",\"size\":", String(r.size),
    ",\"hex310\":", String(r.h1), ",\"hex311\":", String(r.h2),
    ",\"surjective\":", String(r.surj), ",\"settled\":", String(r.settled),
    ",\"shadow\":", String(r.shadow), "}");
end;;
cert := Concatenation("{\n",
  "  \"schema\": \"expA-passport/v1\",\n",
  "  \"f_orientation\": \"judge\",\n",
  "  \"generated_by\": {\"tool\":\"GAP 4.16.0\",\"script\":\"search/probe/wac_v1/expA_measure.g\",\"date\":\"2026-07-31\"},\n",
  "  \"note\": \"single lane (GAP only). NOT a ledger claim. NOT Lean-verified.\",\n",
  "  \"partA\": {\n",
  "    \"n\": 10, \"lambda\": [9,1],\n",
  "    \"base_window\": ", JStr(baseA.id), ",\n",
  "    \"C_v_order\": ", String(Size(CvA)), ",\n",
  "    \"F_v_size\": ", String(Length(GsetA)), ",\n",
  "    \"N_gen\": ", String(Length(orbsV)), ",\n",
  "    \"N_shadow\": ", String(Length(Filtered(rowsA, r -> r.shadow > 0))), ",\n",
  "    \"shadow_total_m0\": ", String(totShadowA), ",\n",
  "    \"per_orbit\": ", JArr(List(rowsA, JRowA)), "\n",
  "  },\n",
  "  \"partB\": {\n",
  "    \"n\": 10, \"lambda\": [7,3],\n",
  "    \"C_w0_order\": ", String(Size(oB.C)), ",\n",
  "    \"N_gen\": ", String(Length(oB.orbs)), ",\n",
  "    \"F_size\": ", String(Length(oB.F)), ",\n",
  "    \"windows\": ", JArr(List(RESB, JRow)), ",\n",
  "    \"all_windows_agree\": ", JB(allsame), "\n",
  "  }\n}\n");;
WriteFile("search/certs/expA_passport_20260731.json", cert);
Print("\nWrote search/certs/expA_passport_20260731.json\n");
Print("\nEXPA_MEASURE_DONE\n");
QUIT;
