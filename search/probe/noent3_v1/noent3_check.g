# noent3_check.g -- NO-ENT(3) の数値前件の独立検算(数学者 Opus 5 / 2026-08-02)
# 目的: Sol 起草 P99-NO-ENT(3)(便 99 F99-3.5)の 3 段証明のうち、
#   (i) G_3^ab = C_2^2   (=> 作用指標の候補は自明 + 非自明 3 個)
#   (ii) 3 個の非自明指標(= 指数 2 部分群 3 個)が座標巡回で 1 軌道
#   (iii) H^2(G_3, F_3) = 0 の独立確認材料(Schur 乗数の 3-部分)
# を機械で確認する。証明の代用ではない(紙の証明は docs/notes/no_ent3_v1.md)。
# K^{(5)} 非接触(n=3 のみ)。整数・有限群演算のみ。
#
# MakeDn / MakeGn は search/bfc-antecedents-check.g と同一実装(移送規約込み)。

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

gn := MakeGn(3);;
G3 := gn.G;;  xg := gn.x;;  yg := gn.y;;  zg := (xg*yg)^-1;;
r := gn.r;;  s := gn.s;;  tr := gn.tr;;

Chk("A1  |G_3|", Size(G3), 108);
Chk("A2  AbelianInvariants(G_3)", AbelianInvariants(G3), [2,2]);
Chk("A3  |[G_3,G_3]|", Size(DerivedSubgroup(G3)), 27);
Chk("A4  AbelianInvariants([G_3,G_3])", AbelianInvariants(DerivedSubgroup(G3)), [3,3,3]);

# 周囲の D_3^3 と偶部分群としての G_3
D33 := Group(tr(r,1), tr(s,1), tr(r,2), tr(s,2), tr(r,3), tr(s,3));;
Chk("A5  |D_3^3|", Size(D33), 216);
Chk("A6  [D_3^3 : G_3]", Index(D33, G3), 2);

# 座標巡回 cyc: block1 -> block2 -> block3 -> block1
cyc := PermList(List([1..9], k -> ((k+2) mod 9) + 1));;
Chk("A7  cyc^3 = ()", cyc^3, ());
Chk("A8  cyc が G_3 を正規化", ForAll(GeneratorsOfGroup(G3), g -> g^cyc in G3), true);
Chk("A9  cyc が D_3^3 を正規化", ForAll(GeneratorsOfGroup(D33), g -> g^cyc in D33), true);

# 指数 2 部分群(= 非自明な指標 G_3 -> C_2)の個数と cyc-軌道
subs := Filtered(NormalSubgroups(G3), H -> Index(G3, H) = 2);;
Chk("A10 指数 2 部分群の個数", Length(subs), 3);
perm := List(subs, H -> Position(subs, ConjugateSubgroup(H, cyc)));;
Print("     cyc の誘導する置換 = ", perm, "\n");
Chk("A11 cyc は 3 個を巡回置換(1 軌道)", Set(perm) = [1,2,3] and perm <> [1,2,3], true);
Chk("A12 cyc-固定の非自明指標は 0 個",
    Length(Filtered([1..3], i -> perm[i] = i)), 0);

# x,y,z の abel 化像が C_2^2 の 3 個の非自明元(= 3 座標のパリティ)であること
ab := NaturalHomomorphismByNormalSubgroup(G3, DerivedSubgroup(G3));;
imgs := Set([Image(ab,xg), Image(ab,yg), Image(ab,zg)]);;
Chk("A13 x,y,z の abel 化像は相異なる 3 元", Length(imgs), 3);
Chk("A14 その 3 元はすべて非自明", ForAll(imgs, u -> u <> One(Image(ab))), true);
Chk("A15 積 = 1(x y z = 中心元 ゆえ abel 化で和が 0)",
    Image(ab,xg)*Image(ab,yg)*Image(ab,zg) = One(Image(ab)), true);

# NO-CENTRAL(n=3)の独立確認材料:
#   H^2(G_3, C_3) (自明係数) = Hom(M(G_3), C_3) (+) Ext(G_3^ab, C_3);
#   G_3^ab = C_2^2 ゆえ Ext 項は 0。よって 3 | |M(G_3)| でなければ H^2 = 0。
mult := AbelianInvariantsMultiplier(G3);;
Print("     AbelianInvariantsMultiplier(G_3) = ", mult, "\n");
Chk("A16 Schur 乗数に 3-部分なし",
    ForAll(mult, m -> m mod 3 <> 0), true);

Print("\nFAILS = ", fails, "\n");
if fails > 0 then Error("noent3_check FAILED"); fi;
QUIT_GAP(0);
