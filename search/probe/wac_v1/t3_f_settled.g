#############################################################################
## search/probe/wac_v1/t3_f_settled.g   [T3 / 準 pure-cycle 剛性]
##
## 目的: ker chi~ の受理条件を judge 実物どおり(hexagon + 生成 + settled)に適用し、
##       m=0 層の中で「Nielsen 軌道(T3 の N)」がどこまで生き残るかを実測する。
##       settled 節 (裁定169) = s1 |-> s1^u, s2 |-> f s2^u f^-1 が Bq=E の
##       自己準同型に延びること。これは (F2) の 3 条件から従わない。
##
## 窓は本 probe 内で自作(命題 0.3 型): n=10, v=(9,1), (k,j)=(4,3) 他。
## GAP 4.16.0 単系統。台帳請求権なし。
#############################################################################

InvolutionsAll := function(n)
  local res, img, free, rec1;
  res := []; img := List([1..n], x->x); free := List([1..n], x->true);
  rec1 := function()
    local i, q;
    i := First([1..n], x -> free[x]);
    if i = fail then Add(res, PermList(ShallowCopy(img))); return; fi;
    free[i] := false; rec1();                       ## i を不動点に
    for q in [i+1..n] do
      if free[q] then
        free[q] := false; img[i] := q; img[q] := i;
        rec1();
        img[i] := i; img[q] := q; free[q] := true;
      fi;
    od;
    free[i] := true;
    return;
  end;
  rec1();
  return res;
end;;
CycleTypeOf := function(p,n) return SortedList(CycleLengths(p,[1..n])); end;;

Study := function(ell, t, k, j)
  local n, v, sols, g, h, base_a1, b1, a, b, s1, s2, x, y, Bq, PN, dlt, Dlt,
        hexAll, cand, f, fj, res, nHex, nGen, nSet, C, cg, kerSet, orbs, alpha,
        Ximg, ok, hom, u, w, orbA1;
  n := ell + t;
  v := PermList(Concatenation(List([1..ell-1], x->x+1), [1], [ell+1..n]));
  ## 基点 (a1,b1): 生成する解を 1 つ選ぶ
  sols := [];
  for g in InvolutionsAll(n) do
    h := g*v;
    if h^3 = () then Add(sols, g); fi;
  od;
  Print("\n### n=", n, " v 型=", CycleTypeOf(v,n),
        "   hexagon 層(g^2=1 & (gv)^3=1 の全型)= ", Length(sols), " 個\n");
  Print("    型別内訳 = ", Collected(List(sols, g -> [Number(CycleLengths(g,[1..n]), z->z=2),
                              Number(CycleLengths(g*v,[1..n]), z->z=3)])), "\n");
  base_a1 := First(sols, g -> Size(Group(g,g*v)) >= Factorial(n)/2 and
                    Number(CycleLengths(g,[1..n]), z->z=2) = k);
  if base_a1 = fail then Print("    基点なし\n"); return fail; fi;
  b1 := (base_a1*v)^-1;
  Print("    基点 a1=", base_a1, "\n         b1=", b1, "\n");
  ## E の構成(命題 0.3 型窓)
  a := base_a1*(n+1,n+3);  b := b1*(n+1,n+2,n+3);
  s1 := b^-1*a;  s2 := a*b^2;
  x := s1^2; y := s2^2;
  Bq := Group(a,b); PN := Group(x,y);
  w := b1^-1*base_a1;
  Print("    |E|=", Size(Bq), "  |P|=", Size(PN), "  x 型=", CycleTypeOf(x,n+3),
        "  w=b1^-1 a1 型=", CycleTypeOf(w,n), "\n");
  Dlt := s1*s2*s1; dlt := s1*s2;
  Print("    Dlt=a? ", Dlt = a, "   dlt=b? ", dlt = b, "\n");
  u := 1;   ## m=0
  nHex := 0; nGen := 0; nSet := 0; kerSet := []; Ximg := [];
  for g in sols do
    ## f(手書き規約) = g*a1 ;  judge 規約 f_j = その逆元
    f := g*base_a1;
    if not f in PN then continue; fi;         ## f in P = [P,P]
    fj := f^-1;
    ## hexagon(手書き規約で確認: (f a1)^2=1 かつ (f b1^-1)^3=1)
    if (f*base_a1)^2 <> () then continue; fi;
    if (f*b1^-1)^3 <> () then continue; fi;
    nHex := nHex + 1;
    ## 生成条件(judge: <x^u, f_j x ... > ; ここでは <x, y^f> = P)
    if Size(Group(x, y^f)) <> Size(PN) then continue; fi;
    nGen := nGen + 1;
    ## settled 節: s1 |-> s1, s2 |-> fj*s2*fj^-1 (= y^f と整合する向き)
    hom := GroupHomomorphismByImages(Bq, Bq, [s1,s2], [s1, fj*s2*fj^-1]);
    if hom = fail then continue; fi;
    nSet := nSet + 1;
    Add(kerSet, g);
    alpha := RepresentativeAction(SymmetricGroup(n), [x, y], [x, y^f], OnTuples);
    Add(Ximg, alpha);
  od;
  cg := [v]; Append(cg, List([ell+1..n-1], z -> (z,z+1)));
  C := Group(cg);
  Print("    hexagon 通過 = ", nHex, " / 生成も通過 = ", nGen,
        " / settled も通過(= |ker chi~|) = ", nSet, "\n");
  Print("    |C_{S_n}(v)| = ", Size(C), "   |C_{S_n}(w)| = ",
        Size(Centralizer(SymmetricGroup(n), w)), "\n");
  if nSet > 0 then
    orbs := Orbits(C, kerSet, OnPoints);
    orbA1 := Orbit(C, base_a1, OnPoints);
    Print("    ker の C(v)-軌道数 = ", Length(orbs), "  軌道長=",
          Collected(List(orbs,Length)), "   ker = a1^{C(v)} ? ",
          Set(kerSet) = Set(orbA1), "\n");
    Print("    Xi 像が C_{S_n}(w) に入るか = ",
          ForAll(Ximg, al -> al <> fail and w^al = w), "\n");
  fi;
  return true;
end;;

Print("############ T3-F : judge 実物条件(hexagon+生成+settled)での ker ############\n");
Study(9,1,4,3);;
Study(7,2,4,3);;
Study(11,2,6,4);;

Print("\nT3_F_DONE\n");
QUIT;
