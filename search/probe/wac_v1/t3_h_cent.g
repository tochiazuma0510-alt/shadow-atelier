#############################################################################
## search/probe/wac_v1/t3_h_cent.g   [T3 / 準 pure-cycle 剛性]
##
## 定理 CENT の証明鎖の最終検算(3 窓・eps=0 と eps=1 の両方):
##   各 shadow f (hexagon + 生成 + settled) について
##     (a) alpha := Xi(f) が存在(x^alpha=x, y^alpha=y^f)
##     (b) w^alpha = w            [settled => alpha in C(w)]
##     (c) v^alpha = v^f          [settled は v^2 でなく v のレベルで効く ★load-bearing]
##     (d) f |-> alpha 単射
##     (e) 像 = C_{S_n}(w) ちょうど
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

Run := function(n, vlist, wantEps)
  local v, sols, g, h, a1, b1, a, b, s1, s2, x, y, Bq, PN, w, Cw, f, fj, hom,
        ker, Xs, al, okb, okc, i;
  v := PermList(vlist);
  sols := [];
  for g in InvolutionsAll(n) do
    h := g*v; if h^3 = () then Add(sols, g); fi;
  od;
  if wantEps = 0 then
    a1 := First(sols, g -> Size(Group(g,g*v)) = Factorial(n)/2);
  else
    a1 := First(sols, g -> Size(Group(g,g*v)) = Factorial(n));
  fi;
  if a1 = fail then Print("  [窓なし n=",n," eps=",wantEps,"]\n"); return fail; fi;
  b1 := (a1*v)^-1;
  a := a1*(n+1,n+3); b := b1*(n+1,n+2,n+3);
  s1 := b^-1*a; s2 := a*b^2; x := s1^2; y := s2^2;
  Bq := Group(a,b); PN := Group(x,y); w := b1^-1*a1;
  Cw := Centralizer(SymmetricGroup(n), w);
  ker := []; Xs := [];
  for g in sols do
    f := g*a1;
    if not f in PN then continue; fi;
    if (f*a1)^2 <> () or (f*b1^-1)^3 <> () then continue; fi;
    if Size(Group(x, y^f)) <> Size(PN) then continue; fi;
    fj := f^-1;
    hom := GroupHomomorphismByImages(Bq, Bq, [s1,s2], [s1, fj*s2*fj^-1]);
    if hom = fail then continue; fi;
    al := RepresentativeAction(SymmetricGroup(n), [x,y], [x,y^f], OnTuples);
    Add(ker, f); Add(Xs, al);
  od;
  okb := ForAll(Xs, z -> z <> fail and w^z = w);
  okc := true;
  for i in [1..Length(ker)] do
    if v^(Xs[i]) <> v^(ker[i]) then okc := false; fi;
  od;
  Print("  n=", n, " eps=", wantEps, " v 型=", CycleTypeOf(v,n),
        " w 型=", CycleTypeOf(w,n), "  |P|=", Size(PN), "\n",
        "     |ker chi~| = ", Length(ker), "   |C(w)| = ", Size(Cw),
        "   等号(CENT)? ", Length(ker) = Size(Cw), "\n",
        "     (b) Xi 像 ⊆ C(w) : ", okb, "\n",
        "     (c) v^Xi(f) = v^f (★) : ", okc, "\n",
        "     (d) Xi 単射 : ", Length(Set(Xs)) = Length(Xs), "\n",
        "     (e) Xi 像 = C(w) ちょうど : ", Set(Xs) = Set(Elements(Cw)), "\n");
  return true;
end;;

Print("############ T3-H : 定理 CENT の証明鎖 最終検算 ############\n");
Run(10, Concatenation([2..9],[1],[10]), 0);;     ## v=(9,1)  p=s=0  eps=0
Run(10, Concatenation([2..10],[1]), 1);;         ## v=(10)   p=1    eps=1
Run(13, Concatenation([2..11],[1],[12,13]), 0);; ## v=(11,1,1) p=s=0 eps=0
Print("\nT3_H_DONE\n");
QUIT;
