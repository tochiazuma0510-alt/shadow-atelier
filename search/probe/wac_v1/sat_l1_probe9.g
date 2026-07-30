#############################################################################
## search/probe/wac_v1/sat_l1_probe9.g
##  設計 v3: 候補窓の分解数を「走査前に」厳密計数する(probe8 の機構を再掲)。
##   候補 A(判別): ell=7,  r=2, t=0, p=0, n=14, w=(7,7)     TRI: ord=7 OK
##   候補 B(判別): ell=9,  r=2, t=0, p=0, n=18, w=(9,9)     TRI: ord=9 OK
##   候補 C(判別): ell=7,  r=3, t=0, p=0, n=21, w=(7,7,7)
##   候補 W(壁)  : ell=19, r=1, t=5, p=s=0, n=24, w=(19,1^5)
##     C_S24(w)=C19 x S5 ⊇ S5 非可解。(k,j)=(12,8) は両者不動点なし
##     ==> 全軌道長 ≡ 0 mod 6 ==> 19+a≡0(6) は a=5 のみ ==> 推移性が自動。
##     19 は素数かつ >n/2 ==> 原始的 ==> Jordan ==> A_24 ⊆ <a1,b1>。
##     ゆえに **その 1 個の class multiplication coefficient > 0 ⟺ 窓が存在**。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
TAllCache := NewDictionary([1,1], true);;
TAll := function(lambda)
  local n, tbl, cp, kk, i, j, tot, part, invs, thr, key, v;
  key := SortedList(lambda);
  v := LookupDictionary(TAllCache, key); if v <> fail then return v; fi;
  n := Sum(lambda);
  if n <= 1 then AddDictionary(TAllCache, key, 1); return 1; fi;
  tbl := CharacterTable("Symmetric", n); cp := ClassParameters(tbl);
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
  AddDictionary(TAllCache, key, tot); return tot;
end;;
SetPartitions := function(m)
  local rec1;
  rec1 := function(i, blocks)
    local res, nb, k;
    if i > m then return [ List(blocks, ShallowCopy) ]; fi;
    res := [];
    for k in [1..Length(blocks)] do
      nb := List(blocks, ShallowCopy); Add(nb[k], i);
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
  local key, v, m, parts, tot, pi, prod, B;
  key := SortedList(lambda);
  v := LookupDictionary(TTransCache, key); if v <> fail then return v; fi;
  m := Length(lambda);
  if m = 1 then v := TAll(lambda); AddDictionary(TTransCache,key,v); return v; fi;
  parts := SetPartitions(m); tot := 0;
  for pi in parts do
    if Length(pi) = 1 then continue; fi;
    prod := 1;
    for B in pi do prod := prod * TTrans(lambda{B}); od;
    tot := tot + prod;
  od;
  v := TAll(lambda) - tot; AddDictionary(TTransCache,key,v); return v;
end;;
CentSize := function(lambda)
  local s, c;
  s := 1;
  for c in Collected(SortedList(lambda)) do s := s*c[1]^c[2]*Factorial(c[2]); od;
  return s;
end;;
Report := function(lambda, label)
  local ta, tt, cw;
  ta := TAll(lambda); tt := TTrans(lambda); cw := CentSize(lambda);
  Print("  ", label, "\n     w=", lambda, " n=", Sum(lambda), " |C|=", cw,
        "   T_all=", ta, "  T_trans=", tt, "   T_trans/|C|=", tt/cw, "\n");
  return true;
end;;

Print("=== 判別窓の候補 ===\n");
Report([7,7],   "候補 A: n=14 w=(7,7)   CENT |ker|=98 vs PRUNE 14 (7 倍差)");;
Report([9,9],   "候補 B: n=18 w=(9,9)   CENT |ker|=162 vs PRUNE 18 (9 倍差)");;
Report([7,7,7], "候補 C: n=21 w=(7,7,7) CENT |ker|=2058 vs PRUNE 98 (21 倍差)");;

Print("\n=== 壁窓 W: n=24, w=(19,1^5) の単一係数 ===\n");
DoWall := function()
  local n, tbl, cp, kk, ii, jj, c;
  n := 24;
  tbl := CharacterTable("Symmetric", n);
  cp := ClassParameters(tbl);
  kk := First([1..Length(cp)], z -> SortedList(cp[z][2]) = SortedList([19,1,1,1,1,1]));
  ii := First([1..Length(cp)], z -> SortedList(cp[z][2]) = SortedList(ListWithIdenticalEntries(12,2)));
  jj := First([1..Length(cp)], z -> SortedList(cp[z][2]) = SortedList(ListWithIdenticalEntries(8,3)));
  Print("  class idx: w=(19,1^5) -> ", kk, "   a1=2^12 -> ", ii,
        "   b1=3^8 -> ", jj, "\n");
  c := ClassMultiplicationCoefficient(tbl, jj, ii, kk);
  Print("  #{(a1,b1) : a1 型 2^12, b1 型 3^8, b1^-1*a1 = w0} = ", c, "\n");
  Print("  |C_S24(w0)| = ", 19*120, "   軌道数 = ", c/(19*120), "\n");
  return true;
end;;
DoWall();;
Print("\nSAT_L1_PROBE9_DONE\n");
QUIT;
