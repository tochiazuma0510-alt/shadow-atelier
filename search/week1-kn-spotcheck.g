# Task #4 スポット照合: 2405.11725 の K^(n) に関する数値主張の独立検算
# 検算対象(抽出ノート §4 (A)(B)):
#   (1) |G_n| = |PB3 : K^(n)| = 4n^3 (n 奇数) / 4(n/2)^3 (n 偶数)
#   (2) K_ord = lcm(ord x̄, ord ȳ, ord c̄) = lcm(n, 2)   (c̄ = 1 なので lcm(|x̄|,|ȳ|))
#   (3) K^(n) = K^(2n) (n 奇数) — 生成元対応 x̄_n↦x̄_2n, ȳ_n↦ȳ_2n が同型を与えることで検証
# D_n の置換表現(論文 §5.3 の慣例): r(j) = j+1 mod n, s(j) = -j mod n

MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("D_n relations failed for n = ", n);
  fi;
  return [r, s];
end;;

# D_n^3 の元を「3n 点上の置換」(第 i 成分はブロック {(i-1)n+1..in} に作用)として実装
MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  # 置換 p([1..n] 上)を第 i ブロックへ移送
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do
      l[j + (i-1)*n] := (j^p) + (i-1)*n;
    od;
    return PermList(l);
  end;
  # x̄ = (r, s, s), ȳ = (rs, r, rs)   ※論文の積の順序: (rs)(j) = r(s(j)) に合わせ GAP では s*r
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y));
end;;

expectedSize := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

failures := 0;;
for n in [3..12] do
  gn := MakeGn(n);
  sz := Size(gn.G);
  ok1 := (sz = expectedSize(n));
  kord := Lcm(Order(gn.x), Order(gn.y));   # c̄ = 1 なので省略
  ok2 := (kord = Lcm(n, 2));
  Print("n=", n, "  |G_n|=", sz, " (期待 ", expectedSize(n), ") ",
        ok1, "   K_ord=", kord, " (期待 ", Lcm(n,2), ") ", ok2, "\n");
  if not (ok1 and ok2) then failures := failures + 1; fi;
od;

# (3) K^(n) = K^(2n) for odd n: F2 -> G_n と F2 -> G_2n の核の一致
#     ⟺ x̄_n↦x̄_2n, ȳ_n↦ȳ_2n が well-defined な同型
for n in [3, 5, 7, 9, 11] do
  gn := MakeGn(n);  g2n := MakeGn(2*n);
  hom := GroupHomomorphismByImages(gn.G, g2n.G, [gn.x, gn.y], [g2n.x, g2n.y]);
  ok := (hom <> fail) and IsBijective(hom);
  Print("n=", n, "  K^(n)=K^(2n) 検証(生成元対応が同型): ", ok, "\n");
  if not ok then failures := failures + 1; fi;
od;

if failures = 0 then
  Print("SPOTCHECK ALL PASSED\n");
else
  Print("SPOTCHECK FAILURES: ", failures, "\n");
fi;
QUIT;
