#############################################################################
## search/probe/wac_v1/sat_l1_probe10.g
##  P-WALL-2 (n=24, w0=(19-cycle)+5 fixed) の witness を **乱択でなく局所探索**で構成。
##   探索空間: 24 点上の完全マッチング a1 (12 互換・不動点なし)
##   目的関数: defect(a1) := NrMovedPoints( (a1*w0^-1)^3 )   (0 が解)
##   手順: 2-opt(2 辺の張り替え)の山登り + ランダム再出発
##  分解数は 2280(probe9・指標計算)= 1 自由軌道ゆえ解は必ず存在する。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
n := 24;;
MakeCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;
w0 := MakeCyc([1..19]);;
Print("w0 = ", w0, "  型 ", CycleStructurePerm(w0), "  ord ", Order(w0), "\n");

MatchToPerm := function(m)          ## m = list of 12 pairs
  local l, p;
  l := [];
  for p in m do Add(l, p[1]); Add(l, p[2]); od;
  return Product(List(m, p -> (p[1], p[2])));
end;;

RandMatch := function()
  local pts, m, i, a, b;
  pts := Shuffle(ShallowCopy([1..n]));
  m := [];
  for i in [1..n/2] do Add(m, [pts[2*i-1], pts[2*i]]); od;
  return m;
end;;

Defect := function(m)
  local a;
  a := MatchToPerm(m);
  return NrMovedPoints((a*w0^-1)^3);
end;;

Hunt := function(maxRestart, maxStep)
  local rs, m, d, step, i, j, m2, d2, best, which;
  for rs in [1..maxRestart] do
    m := RandMatch(); d := Defect(m);
    for step in [1..maxStep] do
      if d = 0 then
        Print("  *** HIT ***  restart ", rs, " step ", step, "\n");
        return m;
      fi;
      ## 2-opt: 2 辺を選び 2 通りの張り替えを試す
      i := Random([1..n/2]); j := Random([1..n/2]);
      if i = j then continue; fi;
      m2 := List(m, ShallowCopy);
      if Random([1,2]) = 1 then
        m2[i] := [m[i][1], m[j][1]]; m2[j] := [m[i][2], m[j][2]];
      else
        m2[i] := [m[i][1], m[j][2]]; m2[j] := [m[i][2], m[j][1]];
      fi;
      d2 := Defect(m2);
      if d2 <= d then m := m2; d := d2; fi;
    od;
  od;
  return fail;
end;;

res := Hunt(400, 4000);;
if res = fail then
  Print("NO HIT (局所探索の予算内)\n");
else
  a1 := MatchToPerm(res);;
  b1 := a1*w0^-1;;
  Print("  a1 = ", a1, "\n  b1 = ", b1, "\n");
  Print("  a1^2=1 ? ", a1^2=(), "   b1^3=1 ? ", b1^3=(), "\n");
  Print("  a1 型 ", CycleStructurePerm(a1), "   b1 型 ", CycleStructurePerm(b1), "\n");
  Print("  b1^-1*a1 = w0 ? ", b1^-1*a1 = w0, "\n");
  G := Group(a1,b1);;
  Print("  <a1,b1> 推移的? ", IsTransitive(G,[1..n]),
        "   = A_24 ? ", G = AlternatingGroup(n),
        "   = S_24 ? ", G = SymmetricGroup(n), "\n");
  Print("  sign(a1) = ", SignPerm(a1), "\n");
  Print("  |C_S24(w0)| = ", Size(Centralizer(SymmetricGroup(n), w0)),
        "   構造 ", StructureDescription(Centralizer(SymmetricGroup(n), w0)), "\n");
  Print("  C_S24(w0) 可解? ", IsSolvable(Centralizer(SymmetricGroup(n), w0)), "\n");
fi;
Print("\nSAT_L1_PROBE10_DONE\n");
QUIT;
