#############################################################################
## search/probe/wac_v1/t3_g_xiinj.g   [T3 / 準 pure-cycle 剛性]
##
## 補題 XI-INJ(本稿 §5)の機械検算と、p>0(ε=1)窓での settled 節の挙動確認。
##
## 補題 XI-INJ: g^2=1, h^3=1, v:=g^-1 h, C_{S_n}(<g,h>)=1, c in C_{S_n}(v),
##              (cg)^2=1  ==>  c=1.
##   (証明: (cg)^2=1 => c^g=c^-1 => cg=gc^-1;  c in C(v)=C(gh) => c^h=c^-1;
##          h^3=1 => c=c^{h^3}=c^-1 => c^2=1 => c は g,h と可換 => c=1)
##
## GAP 4.16.0 単系統。台帳請求権なし。
#############################################################################

InvolutionsAll := function(n)
  local res, img, free, rec1;
  res := []; img := List([1..n], x->x); free := List([1..n], x->true);
  rec1 := function()
    local i, q;
    i := First([1..n], x -> free[x]);
    if i = fail then Add(res, PermList(ShallowCopy(img))); return; fi;
    free[i] := false; rec1();
    for q in [i+1..n] do
      if free[q] then
        free[q] := false; img[i] := q; img[q] := i; rec1();
        img[i] := i; img[q] := q; free[q] := true;
      fi;
    od;
    free[i] := true; return;
  end;
  rec1(); return res;
end;;
CycleTypeOf := function(p,n) return SortedList(CycleLengths(p,[1..n])); end;;

## ---- (1) 補題 XI-INJ の悉皆検算 ------------------------------------------
Print("############ T3-G(1): 補題 XI-INJ の悉皆検算 ############\n");
CheckLemma := function(n, vtype)
  local v, sols, g, h, Cv, Cv2, bad2, bad, cnt, c;
  v := PermList(vtype);
  Cv  := Centralizer(SymmetricGroup(n), v);
  Cv2 := Centralizer(SymmetricGroup(n), v^2);
  sols := [];
  for g in InvolutionsAll(n) do
    h := g*v;
    if h^3 = () and Size(Group(g,h)) >= Factorial(n)/2 then Add(sols, g); fi;
  od;
  bad := 0; bad2 := 0;
  for g in sols do
    h := g*v;
    for c in Cv do
      if c <> () and (c*g)^2 = () then bad := bad+1; fi;
    od;
    for c in Cv2 do
      if c <> () and (c*g)^2 = () and (c*h)^3 = () then bad2 := bad2+1; fi;
    od;
  od;
  Print("  n=", n, " v 型=", CycleTypeOf(v,n), "  生成解 ", Length(sols), " 個 : ",
        "  |C(v)|=", Size(Cv), " |C(v^2)|=", Size(Cv2), "\n",
        "     c in C(v)\\1 で (cg)^2=1 となる例: ", bad, " 件  [補題 => 0]\n",
        "     c in C(v^2)\\1 で (cg)^2=1 かつ (ch)^3=1 となる例: ", bad2,
        " 件  [p=s=0 なら 0・一般は未証明]\n");
  return true;
end;;
CheckLemma(10, Concatenation([2..9],[1],[10]));       ## v=(9,1)   p=s=0
CheckLemma(9,  Concatenation([2..7],[1],[8,9]));      ## v=(7,1,1) p=s=0
CheckLemma(10, Concatenation([2..10],[1]));           ## v=(10)    p=1  <-- 反例の有無
CheckLemma(12, Concatenation([2..10],[1],[11,12]));   ## v=(9,1,1) p=s=0

## ---- (2) p=1 (eps=1) 窓での settled 節 -----------------------------------
Print("\n############ T3-G(2): p=1 窓 (v=(10), n=10) の judge 実物条件 ############\n");
DoP1 := function()
  local n, v, sols, g, h, a1, b1, a, b, s1, s2, x, y, Bq, PN, f, fj, hom,
        nHex, nGen, nSet, kerSet, Cv, w, Cw, Ximg, alpha, orbs;
  n := 10; v := PermList(Concatenation([2..10],[1]));
  sols := [];
  for g in InvolutionsAll(n) do
    h := g*v; if h^3 = () then Add(sols, g); fi;
  od;
  Print("  hexagon 層 = ", Length(sols), " [工房 probe16 の 65 と一致すべき]\n");
  a1 := First(sols, g -> Size(Group(g,g*v)) = Factorial(n));   ## eps=1 => S_10
  if a1 = fail then Print("  S_10 生成の基点なし\n"); return fail; fi;
  b1 := (a1*v)^-1;
  a := a1*(n+1,n+3); b := b1*(n+1,n+2,n+3);
  s1 := b^-1*a; s2 := a*b^2; x := s1^2; y := s2^2;
  Bq := Group(a,b); PN := Group(x,y);
  w := b1^-1*a1; Cv := Centralizer(SymmetricGroup(n), v);
  Cw := Centralizer(SymmetricGroup(n), w);
  Print("  |E|=", Size(Bq), " |P|=", Size(PN), " (P=A_10? ", Size(PN)=Factorial(10)/2, ")\n");
  Print("  w 型=", CycleTypeOf(w,n), " |C(v)|=", Size(Cv), " |C(w)|=", Size(Cw),
        " |C(xbar)|=", Size(Centralizer(SymmetricGroup(n), x^1)), "\n");
  nHex := 0; nGen := 0; nSet := 0; kerSet := []; Ximg := [];
  for g in sols do
    f := g*a1;
    if not f in PN then continue; fi;
    if (f*a1)^2 <> () or (f*b1^-1)^3 <> () then continue; fi;
    nHex := nHex+1;
    if Size(Group(x, y^f)) <> Size(PN) then continue; fi;
    nGen := nGen+1;
    fj := f^-1;
    hom := GroupHomomorphismByImages(Bq, Bq, [s1,s2], [s1, fj*s2*fj^-1]);
    if hom = fail then continue; fi;
    nSet := nSet+1; Add(kerSet, g);
    alpha := RepresentativeAction(SymmetricGroup(n), [x,y], [x,y^f], OnTuples);
    Add(Ximg, alpha);
  od;
  Print("  hexagon=", nHex, "  +生成=", nGen, "  +settled= |ker| =", nSet,
        "   [工房実測 |ker|=10]\n");
  Print("  Xi 像がすべて C_{S_n}(w) に入るか = ",
        ForAll(Ximg, al -> al <> fail and w^al = w), "\n");
  if nSet > 0 then
    orbs := Orbits(Cv, kerSet, OnPoints);
    Print("  ker の C(v)-軌道数 = ", Length(orbs), " 軌道長=",
          Collected(List(orbs,Length)), "\n");
  fi;
  return true;
end;;
DoP1();;

Print("\nT3_G_DONE\n");
QUIT;
