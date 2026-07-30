#############################################################################
## search/probe/wac_v1/sat_l1_probe8.g
##  「計数してから構成する」機構(裁定 240 追記 2 の委嘱 1・2):
##   TAll(lambda)   := #{(g,h): g^2=1, h^3=1, gh=w0} , w0 の型 lambda
##                     (対称群指標表の class multiplication coefficient で厳密計算)
##   TTrans(lambda) := そのうち <g,h> が推移的なもの
##                     (w の巡回の集合分割上の Moebius 反転 = Hall の差引の実用形)
##   軌道数 = TTrans/|C_Sn(w)| (自由作用; 推移なら C_{S_n}(<g,h>)=1 とは限らないので
##            割り切れない場合は非自由軌道の存在を示す ==> 生値のまま報告)
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
TAllCache := NewDictionary([1,1], true);;

TAll := function(lambda)
  local n, tbl, cp, idx, kk, i, j, tot, part, invs, thr, key, v;
  key := SortedList(lambda);
  v := LookupDictionary(TAllCache, key);
  if v <> fail then return v; fi;
  n := Sum(lambda);
  if n = 0 then return 1; fi;
  if n = 1 then AddDictionary(TAllCache, key, 1); return 1; fi;
  tbl := CharacterTable("Symmetric", n);
  cp := ClassParameters(tbl);
  kk := First([1..Length(cp)], z -> SortedList(cp[z][2]) = key);
  if kk = fail then return fail; fi;
  invs := []; thr := [];
  for i in [1..Length(cp)] do
    part := cp[i][2];
    if ForAll(part, e -> e in [1,2]) then Add(invs, i); fi;
    if ForAll(part, e -> e in [1,3]) then Add(thr, i); fi;
  od;
  tot := 0;
  for i in invs do for j in thr do
    tot := tot + ClassMultiplicationCoefficient(tbl, j, i, kk);
  od; od;
  AddDictionary(TAllCache, key, tot);
  return tot;
end;;

## 集合 {1..m} の全分割
SetPartitions := function(m)
  local rec1;
  rec1 := function(i, blocks)
    local res, b, nb, k;
    if i > m then return [ List(blocks, ShallowCopy) ]; fi;
    res := [];
    for k in [1..Length(blocks)] do
      nb := List(blocks, ShallowCopy);
      Add(nb[k], i);
      Append(res, rec1(i+1, nb));
    od;
    nb := List(blocks, ShallowCopy); Add(nb, [i]);
    Append(res, rec1(i+1, nb));
    return res;
  end;
  return rec1(1, []);
end;;

TTransCache := NewDictionary([1,1], true);;

TTrans := function(lambda)
  local key, v, m, parts, tot, pi, prod, B, sub, ok;
  key := SortedList(lambda);
  v := LookupDictionary(TTransCache, key);
  if v <> fail then return v; fi;
  m := Length(lambda);
  if m = 1 then
    v := TAll(lambda);            ## 巡回 1 本 ==> 全分解が推移的
    AddDictionary(TTransCache, key, v); return v;
  fi;
  parts := SetPartitions(m);
  tot := 0;
  for pi in parts do
    if Length(pi) = 1 then continue; fi;   ## 自明分割 = 求めたい項
    prod := 1;
    for B in pi do
      sub := lambda{B};
      prod := prod * TTrans(sub);
    od;
    tot := tot + prod;
  od;
  v := TAll(lambda) - tot;
  AddDictionary(TTransCache, key, v);
  return v;
end;;

CentSize := function(lambda)
  local mult, s, L, c;
  mult := Collected(SortedList(lambda));
  s := 1;
  for c in mult do s := s * c[1]^c[2] * Factorial(c[2]); od;
  return s;
end;;

Report := function(lambda, label)
  local ta, tt, cw;
  ta := TAll(lambda); tt := TTrans(lambda); cw := CentSize(lambda);
  Print("  ", label, "\n     w=", lambda, "  n=", Sum(lambda),
        "   |C_Sn(w)|=", cw, "\n     T_all=", ta, "  T_trans=", tt,
        "   T_trans/|C| = ", tt/cw, "\n");
  return true;
end;;

Print("=== 較正(答を知っている窓)===\n");
Report([5,5],    "n=10 p=0  : 悉皆陰性(全て A5)・|ker|=0");;
Report([10],     "n=10 p=1  : 実在・|ker|=10");;
Report([5,5,2],  "n=12      : 悉皆陰性(全て 2^5:S5 = 3840・推移かつ非原始)・|ker|=0");;
Report([10,5],   "n=15      : 実在・|ker|=50");;
Report([9,1],    "n=10 梯子 : 実在・|ker|=9");;
Report([9,2],    "n=11 梯子 : 実在・|ker|=18");;
Report([9,2,1],  "n=12 梯子 : 実在・|ker|=18");;
Report([9,2,2],  "n=13 梯子 : 実在・|ker|=72");;
Report([11,2,2,1], "n=16 D族 : 実在・|ker|=88");;
Print("\n=== r=4 両枝(重い場合は途中で落ちてよい)===\n");
Report([10,10],  "n=20 C枝  : 実在・|ker|=200");;
Report([10,5,5], "n=20 B枝  : 実在・|ker|=500");;
Print("\nSAT_L1_PROBE8_DONE\n");
QUIT;
