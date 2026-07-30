#############################################################################
## search/probe/wac_v1/t3_d_brute.g   [T3 / 準 pure-cycle 剛性]
##
## 第 2 系統(指標を一切使わない直接列挙):
##   (A) w0=(ell,1^t) を固定し、型 2^k1^{f2} の対合 g を悉皆列挙、h:=g*w0 が
##       型 3^j1^{f3} かつ h^3=1 を検査 => F(w0) を直接構成。
##       C(w0)=<w0> x Sym(Delta) の軌道を明示計算 => N(実測)。
##   (B) P-WALL-2 の実物 witness から地図(cubic ribbon graph)を復元し、
##       「t 本のループを外すと平面木」という構造予言を直接検証。
##
## GAP 4.16.0 単系統(ただし T3-A/T3-B の指標計数とは独立)。台帳請求権なし。
#############################################################################

## 型 2^k 1^{n-2k} の対合を全列挙(img 配列で incremental に構成)
InvolutionsOfType := function(n, k)
  local res, img, free, rec1;
  res := [];
  img := List([1..n], x -> x);
  free := List([1..n], x -> true);
  rec1 := function(np, nf)
    local i, q;
    i := First([1..n], x -> free[x]);
    if i = fail then
      if np = k then Add(res, PermList(ShallowCopy(img))); fi;
      return;
    fi;
    if nf > 0 then
      free[i] := false;
      rec1(np, nf-1);
      free[i] := true;
    fi;
    if np < k then
      free[i] := false;
      for q in [i+1..n] do
        if free[q] then
          free[q] := false; img[i] := q; img[q] := i;
          rec1(np+1, nf);
          img[i] := i; img[q] := q; free[q] := true;
        fi;
      od;
      free[i] := true;
    fi;
    return;
  end;
  rec1(0, n-2*k);
  return res;
end;;

CycleTypeOf := function(p, n) return SortedList(CycleLengths(p, [1..n])); end;;

Analyse := function(ell, t, k, j)
  local n, w0, f2, f3, target3, sols, g, h, cnt, C, orbs, gens, solsGen, cgens;
  n := ell + t; f2 := n-2*k; f3 := n-3*j;
  w0 := PermList(Concatenation(List([1..ell-1], x -> x+1), [1], [ell+1..n]));
  Print("\n### 直接列挙: ell=", ell, " t=", t, " n=", n, " (k,j)=(", k, ",", j,
        ") f2=", f2, " f3=", f3, "\n");
  Print("    w0 型 = ", CycleTypeOf(w0,n), "\n");
  target3 := SortedList(Concatenation(ListWithIdenticalEntries(j,3),
                                      ListWithIdenticalEntries(f3,1)));
  sols := []; cnt := 0;
  for g in InvolutionsOfType(n,k) do
    cnt := cnt+1;
    h := g*w0;
    if h^3 = () and CycleTypeOf(h,n) = target3 then Add(sols, g); fi;
  od;
  Print("    列挙対合数 = ", cnt, "     T_all^{(k,j)} = |F(w0)| = ", Length(sols), "\n");
  gens := List(sols, g -> Size(Group(g, g*w0)));
  solsGen := Filtered(sols, g -> Size(Group(g, g*w0)) >= Factorial(n)/2);
  Print("    推移的なもの = ", Number(sols, g -> IsTransitive(Group(g,g*w0),[1..n])),
        "     <g,h> >= A_n なもの = ", Length(solsGen), "\n");
  Print("    <g,h> の位数の分布 = ", Collected(gens), "\n");
  cgens := [w0];
  Append(cgens, List([ell+1..n-1], x -> (x,x+1)));
  C := Group(cgens);
  Print("    |C_{S_n}(w0)| = ", Size(C), "  (ell*t! = ", ell*Factorial(t), ")\n");
  if Length(sols) > 0 then
    orbs := Orbits(C, sols, OnPoints);
    Print("    C(w0)-軌道数(F(w0) 全体)= ", Length(orbs),
          "  軌道長 = ", Collected(List(orbs,Length)), "\n");
  fi;
  if Length(solsGen) > 0 then
    orbs := Orbits(C, solsGen, OnPoints);
    Print("    ** C(w0)-軌道数(生成分)N = ", Length(orbs),
          "  軌道長 = ", Collected(List(orbs,Length)), "\n");
    Print("    C_{S_n}(<g,h>) の位数 = ",
          Collected(List(solsGen,
            g -> Size(Centralizer(SymmetricGroup(n), Group(g, g*w0))))), "\n");
  fi;
  return true;
end;;

Print("############ T3-D : 直接列挙(第 2 系統)############\n");

Analyse(9,1,4,3);;     ## 予言: T_all=63, T_trans=54(N_trans=6)/ 生成分 9(N=1)
Analyse(7,2,4,3);;     ## 予言: T_all=T_trans=14, N=1
Analyse(11,2,6,4);;    ## 予言: T_all=154, T_trans=132, N_trans=6
Analyse(13,3,8,5);;    ## 予言: T_all=T_trans=156, N=2(Jordan 安全域)

Print("\n############ T3-D(B): P-WALL-2 witness の地図構造 ############\n");
DoWallMap := function()
  local a1, b1, g, h, w0, n, hc, gc, loops, nonloop, deg, i, findv,
        treeEdges, leaves, tri, conn;
  n := 24;
  a1 := ( 1,13)( 2, 9)( 3, 5)( 4,24)( 6, 8)( 7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23);
  b1 := ( 1,12, 9)( 2, 8, 5)( 3, 4,24)( 6, 7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23);
  g := a1; h := b1^-1; w0 := g*h;
  Print("  g 型 ", CycleTypeOf(g,n), " / h 型 ", CycleTypeOf(h,n),
        " / g*h 型 ", CycleTypeOf(w0,n), "\n");
  Print("  g^2=1? ", g^2 = (), "  h^3=1? ", h^3 = (),
        "  <g,h>=A_24? ", Size(Group(g,h)) = Factorial(24)/2, "\n");
  hc := Filtered(Cycles(h,[1..n]), c -> Length(c)=3);
  gc := Filtered(Cycles(g,[1..n]), c -> Length(c)=2);
  Print("  黒頂点(h の 3-巡回)= ", Length(hc), " / 辺(g の 2-巡回)= ", Length(gc), "\n");
  findv := function(d) return First([1..Length(hc)], i -> d in hc[i]); end;
  loops   := Filtered(gc, e -> findv(e[1]) = findv(e[2]));
  nonloop := Filtered(gc, e -> findv(e[1]) <> findv(e[2]));
  Print("  ループ辺 = ", Length(loops), " 本 [予言 t=5]、非ループ辺 = ",
        Length(nonloop), " 本 [予言 |V|-1=7]\n");
  treeEdges := List(nonloop, e -> Set([findv(e[1]), findv(e[2])]));
  deg := List([1..Length(hc)], i -> Number(treeEdges, e -> i in e));
  conn := Length(Orbits(Group(List(treeEdges, e -> (e[1],e[2]))), [1..Length(hc)])) = 1;
  Print("  ループ除去後の次数列 = ", SortedList(deg), " [予言 1^5 3^3]、連結(=木)? ", conn, "\n");
  leaves := Filtered([1..Length(hc)], i -> deg[i]=1);
  tri    := Filtered([1..Length(hc)], i -> deg[i]=3);
  Print("  葉 = ", leaves, " / 3 価 = ", tri, "\n");
  Print("  ループを持つ黒頂点 = ", SortedList(List(loops, e -> findv(e[1]))),
        " [予言: 葉集合と一致 -> ", SortedList(List(loops, e->findv(e[1]))) = leaves, "]\n");
  Print("  3 価どうしを結ぶ辺 = ", Filtered(treeEdges, e -> e[1] in tri and e[2] in tri),
        " [予言: 道 a-b-c = 2 本]\n");
  for i in tri do
    Print("    3 価頂点 ", i, " に付く葉の本数 = ",
          Number(treeEdges, e -> i in e and Length(Intersection(e, leaves)) > 0), "\n");
  od;
  return true;
end;;
DoWallMap();;

Print("\nT3_D_DONE\n");
QUIT;
