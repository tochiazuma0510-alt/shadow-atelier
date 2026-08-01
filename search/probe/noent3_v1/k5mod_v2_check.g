# k5mod_v2_check.g -- 定理 K5-MOD-v2 が使う構造事実の独立検算(数学者 Opus 5 / 2026-08-02)
# 便 99 W99-4.1(非半単純 F_5[G_5] の穴)の修理で使う前件だけを機械確認する:
#   (i)   |G_5| = 500, G_5^ab = C_2^2, [G_5,G_5] = A = C_5^3
#   (ii)  Q = G_5/A の 3 個の非自明指標(= 指数 2 部分群)が座標巡回で 1 軌道
#   (iii) NO-CENTRAL(n=5)の独立確認材料: Schur 乗数の 5-部分が無いこと
#         (=> H^2(G_5, F_5) = Hom(M(G_5),F_5) (+) Ext(C_2^2,C_5) = 0)
#   (iv)  模型 Ghat = <G_5, 座標 S_3> について A = O_5(Ghat), |Ghat| = 3000,
#         Ghat/A の位数 24・IdGroup(= S_4 か)
# (iv) は「模型」の確認であって B_3/K^{(5)} そのものの同定ではない(証明は
# 補題 D0^n と (4.8) の構造事実のみを使う)。shadow の値には一切触れない。

MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("D_n relations failed for n = ", n);
  fi;
  return [r, s];
end;;

MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y), r := r, s := s, tr := tr);
end;;

fails := 0;;
Chk := function(name, got, want)
  local ok;
  ok := (got = want);
  if not ok then fails := fails + 1; fi;
  Print("[", ok, "] ", name, " got=", got, " want=", want, "\n");
end;;

n := 5;;
gn := MakeGn(n);;
G5 := gn.G;;  xg := gn.x;;  yg := gn.y;;  zg := (xg*yg)^-1;;

Chk("B1  |G_5|", Size(G5), 500);
Chk("B2  AbelianInvariants(G_5)", AbelianInvariants(G5), [2,2]);
A := DerivedSubgroup(G5);;
Chk("B3  |A| = |[G_5,G_5]|", Size(A), 125);
Chk("B4  AbelianInvariants(A)", AbelianInvariants(A), [5,5,5]);

cyc := PermList(List([1..3*n], k -> ((k + (2*n-1)) mod (3*n)) + 1));;
Chk("B5  cyc^3 = ()", cyc^3, ());
Chk("B6  cyc が G_5 を正規化", ForAll(GeneratorsOfGroup(G5), g -> g^cyc in G5), true);

subs := Filtered(NormalSubgroups(G5), H -> Index(G5, H) = 2);;
Chk("B7  指数 2 部分群の個数", Length(subs), 3);
perm := List(subs, H -> Position(subs, ConjugateSubgroup(H, cyc)));;
Print("     cyc の誘導する置換 = ", perm, "\n");
Chk("B8  cyc は 3 個を巡回置換(1 軌道)", Set(perm) = [1,2,3] and perm <> [1,2,3], true);
Chk("B9  cyc-固定の非自明指標は 0 個", Length(Filtered([1..3], i -> perm[i] = i)), 0);

ab := NaturalHomomorphismByNormalSubgroup(G5, A);;
Chk("B10 x,y,z の abel 化像は相異なる 3 元",
    Length(Set([Image(ab,xg), Image(ab,yg), Image(ab,zg)])), 3);

mult := AbelianInvariantsMultiplier(G5);;
Print("     AbelianInvariantsMultiplier(G_5) = ", mult, "\n");
Chk("B11 Schur 乗数に 5-部分なし", ForAll(mult, m -> m mod 5 <> 0), true);

# --- 模型 Ghat = <G_5, cyc, 転置> の構造(B_3/K^{(5)} そのものではない) ---
# 座標 (1 2) の入替: block1 <-> block2
swap := PermList(Concatenation([n+1..2*n], [1..n], [2*n+1..3*n]));;
Ghat := Group(Concatenation(GeneratorsOfGroup(G5), [cyc, swap]));;
Print("     |Ghat model| = ", Size(Ghat), "\n");
Chk("B12 |Ghat| = 3000", Size(Ghat), 3000);
O5 := PCore(Ghat, 5);;
Chk("B13 O_5(Ghat) = A", O5 = A, true);
Q24 := Image(NaturalHomomorphismByNormalSubgroup(Ghat, O5));;
Chk("B14 |Ghat/A| = 24", Size(Q24), 24);
Print("     IdGroup(Ghat/A) = ", IdGroup(Q24), "  (S_4 = [24,12])\n");
Chk("B15 Ghat/A = S_4", IdGroup(Q24), [24,12]);

Print("\nFAILS = ", fails, "\n");
if fails > 0 then Error("k5mod_v2_check FAILED"); fi;
QUIT_GAP(0);
