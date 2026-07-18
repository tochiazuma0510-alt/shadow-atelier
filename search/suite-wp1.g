# suite-wp1.g -- 較正スイート v2 / 作業パッケージ WP1
#
# 実行: .\gap.ps1 search\suite-wp1.g
#
# 出典: arXiv 2405.11725 (dihedral poset; Prop 3.1/3.4/3.5, Thm 4.3) +
#       arXiv 2401.06870 (GTSh 定義正本; hexagon (3.3)(3.4), Def 3.1, Prop 3.6)
# 正本ノート: docs/week1-定義ノート.md v2 §4(較正スイート v2、Sol 定義ゲート条件反映)
# 慣習: D_n^3 は 3n 点上の置換(左作用)。rs (論文の積、s のち r) は GAP 右作用で s*r。
#       (裁定: sol/裁定_01_definition_gate.md「rs の作用慣習」— 司令塔の読みが正本と一致と確認済み)
#
# 実装する 3 検査:
#   1. K^(n) 数値事実の完走 (n=3..16,18,36; 奇数 n=13,15 の doubling check)
#   2. Prop 3.5 の包含判定 (marked factor map と数論式 n|lcm(q,2) の一致)
#   3. N_5 control (c <> 1 の較正; S3xC5 内で full hexagon (3.3)(3.4) + T(c))
#
# 規律: 宇宙は事前登録どおり固定 (n in {3..16,18,36})。範囲は広げも絞りもしない。
# 全検査 PASS/FAIL 印字 + 最終総括行 "WP1 ALL PASSED" / "WP1 FAILURES: <数>"。

SizeScreen([4096, 0]);;   # 端末の 80 桁自動折返しを止める(出力を原文のまま報告するため)

failures := 0;;

PF := function(b)
  if b then return "PASS"; else return "FAIL"; fi;
end;;

# ------------------------------------------------------------------
# MakeDn / MakeGn -- search/week1-kn-spotcheck.g より再利用(無変更でコピー)
# D_n の置換表現(論文 2405 §5.3 の慣例): r(j) = j+1 mod n, s(j) = -j mod n
# ------------------------------------------------------------------
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
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do
      l[j + (i-1)*n] := (j^p) + (i-1)*n;
    od;
    return PermList(l);
  end;
  # x̄ = (r, s, s), ȳ = (rs, r, rs)  ※ rs は「s のち r」= GAP では s*r
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y));
end;;

expectedSize := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

# ####################################################################
# セクション 1: K^(n) 数値事実の完走
# ####################################################################
Print("############################################################\n");
Print("# セクション 1: K^(n) 数値事実の完走\n");
Print("############################################################\n");

universe1 := Concatenation([3..16], [18, 36]);;
Print("宇宙 (事前登録どおり): ", universe1, "\n");

cache := [];;   # cache[n] := MakeGn(n) の結果 rec(x,y,G)

for n in universe1 do
  gn := MakeGn(n);
  cache[n] := gn;
  sz := Size(gn.G);
  okSize := (sz = expectedSize(n));
  kord := Lcm(Order(gn.x), Order(gn.y));
  okKord := (kord = Lcm(n, 2));
  Print("[", PF(okSize), "] n=", n, "  |G_n|=", sz, " (期待 ", expectedSize(n), ")\n");
  Print("[", PF(okKord), "] n=", n, "  K_ord=", kord, " (期待 ", Lcm(n,2), ")\n");
  if not okSize then failures := failures + 1; fi;
  if not okKord then failures := failures + 1; fi;
od;

Print("--- 奇数 n=13,15: K^(n) = K^(2n) の doubling check ---\n");
Print("(注: 2n = 26,30 は宇宙 {3..16,18,36} の外の補助構成。\n");
Print(" week1-kn-spotcheck.g の n=3,5,7,9,11 と同じ前例パターンで、\n");
Print(" doubling 同型検査専用に一時的に構成するのみで新規対象として登録はしない)\n");
for n in [13, 15] do
  gn := cache[n];
  g2n := MakeGn(2*n);
  hom := GroupHomomorphismByImages(gn.G, g2n.G, [gn.x, gn.y], [g2n.x, g2n.y]);
  if hom = fail then
    ok := false;
  else
    ok := IsBijective(hom);
  fi;
  Print("[", PF(ok), "] K^(", n, ") = K^(", 2*n, ") (x_n->x_2n, y_n->y_2n が同型): ", ok, "\n");
  if not ok then failures := failures + 1; fi;
od;

# ####################################################################
# セクション 2: Prop 3.5 の包含判定 (marked factor map)
#   主張: K^(q) subseteq K^(n)  <=>  n | lcm(q,2)
#   判定法: x_q -> x_n, y_q -> y_n が well-defined な準同型 G_q -> G_n を
#           与えること (GroupHomomorphismByImages <> fail) と同値
# ####################################################################
Print("\n############################################################\n");
Print("# セクション 2: Prop 3.5 の包含判定 (marked factor map)\n");
Print("############################################################\n");

matNumeric := [];;
matFmap := [];;
mismatchCount := 0;;
nonIncludedChecked := 0;;
nonIncludedFmapFail := 0;;

for q in universe1 do
  matNumeric[q] := [];
  matFmap[q] := [];
  for n in universe1 do
    numeric := (Lcm(q,2) mod n) = 0;
    recQ := cache[q];
    recN := cache[n];
    hom := GroupHomomorphismByImages(recQ.G, recN.G, [recQ.x, recQ.y], [recN.x, recN.y]);
    fmap := (hom <> fail);
    matNumeric[q][n] := numeric;
    matFmap[q][n] := fmap;
    if numeric <> fmap then
      mismatchCount := mismatchCount + 1;
      Print("[FAIL] 不一致: (q,n)=(", q, ",", n, ")  数論式=", numeric, "  factormap=", fmap, "\n");
    fi;
    if not numeric then
      nonIncludedChecked := nonIncludedChecked + 1;
      if fmap = false then
        nonIncludedFmapFail := nonIncludedFmapFail + 1;
      fi;
    fi;
  od;
od;

Print("全 ", Length(universe1)*Length(universe1), " 順序対 (q,n) を検査。不一致: ", mismatchCount, " 件\n");
Print("[", PF(mismatchCount = 0), "] 数論式 n|lcm(q,2) <=> factor map、全順序対で一致\n");
if mismatchCount <> 0 then failures := failures + 1; fi;

Print("包含不成立(数論式で false)の対: ", nonIncludedChecked, " 件中、factor map も実際に fail: ", nonIncludedFmapFail, " 件\n");
Print("[", PF(nonIncludedChecked = nonIncludedFmapFail), "] 包含不成立の全対で factor map が実際に fail を返す\n");
if nonIncludedChecked <> nonIncludedFmapFail then failures := failures + 1; fi;

Print("--- reduction branch suite 5 対の個別 PASS 行 ---\n");
specialPairs := [[8,4],[36,12],[12,4],[18,3],[9,3]];;
for pr in specialPairs do
  q := pr[1];
  n := pr[2];
  numeric := matNumeric[q][n];
  fmap := matFmap[q][n];
  agree := (numeric = fmap) and numeric;
  Print("[", PF(agree), "] branch (q,n)=(", q, ",", n, "): K^(", q, ") included in K^(", n,
        ")?  numeric=", numeric, "  factormap=", fmap, "\n");
  if not agree then failures := failures + 1; fi;
od;

# ####################################################################
# セクション 3: N_5 control (c <> 1 の較正)
# ####################################################################
Print("\n############################################################\n");
Print("# セクション 3: N_5 control (c <> 1 の較正)\n");
Print("############################################################\n");

sigma1 := (1,2)(4,5,6,7,8);;
sigma2 := (2,3)(4,5,6,7,8);;
Bgrp := Group(sigma1, sigma2);;

ok := (Size(Bgrp) = 30);;
Print("[", PF(ok), "] |B| = ", Size(Bgrp), " (期待 30)\n");
if not ok then failures := failures + 1; fi;

xbar := sigma1^2;;
ybar := sigma2^2;;
Deltabar := sigma1*sigma2*sigma1;;
cbar := Deltabar^2;;

ok := (Order(xbar) = 5);;
Print("[", PF(ok), "] |xbar| = ", Order(xbar), " (期待 5)\n");
if not ok then failures := failures + 1; fi;

ok := (Order(cbar) = 5);;
Print("[", PF(ok), "] |cbar| = ", Order(cbar), " (期待 5)\n");
if not ok then failures := failures + 1; fi;

PB3img := Group(xbar, ybar, cbar);;
ok := (Size(PB3img) = 5);;
Print("[", PF(ok), "] |<xbar,ybar,cbar>| (PB3 の像) = ", Size(PB3img), " (期待 5)\n");
if not ok then failures := failures + 1; fi;

Nord := Lcm(Order(xbar), Order(ybar), Order(cbar));;
ok := (Nord = 5);;
Print("[", PF(ok), "] N_ord = lcm(|xbar|,|ybar|,|cbar|) = ", Nord, " (期待 5)\n");
if not ok then failures := failures + 1; fi;

ok := (sigma1*sigma2*sigma1 = sigma2*sigma1*sigma2);;
Print("[", PF(ok), "] braid 関係 sigma1 sigma2 sigma1 = sigma2 sigma1 sigma2: ", ok, "\n");
if not ok then failures := failures + 1; fi;

# GT(N5) の全列挙: C5 可換ゆえ f = 1 のみ(charming の f 条件が自明)。
# m = 0..4 の各々で full hexagon (3.3)(3.4)(f=1 版)・単元条件・全射性を検査。
Print("\n--- GT(N_5) 列挙: f=1 固定、m=0..4 の hexagon/charming/全射 ---\n");
Print("m | u=2m+1 | hex(3.3) | hex(3.4) | unit(gcd(u,5)=1) | surj(<xbar^u>=<xbar>) | shadow候補\n");

passingM := [];;
consistencyFailCount := 0;;

for m in [0..4] do
  u := 2*m + 1;

  lhs33 := sigma1^u * sigma2^u;
  rhs33 := sigma1*sigma2 * xbar^(-m) * cbar^m;
  hex33 := (lhs33 = rhs33);

  lhs34 := sigma2^u * sigma1^u;
  rhs34 := sigma2*sigma1 * ybar^(-m) * cbar^m;
  hex34 := (lhs34 = rhs34);

  unitCond := (Gcd(u, 5) = 1);
  surjCond := (Group(xbar^u) = Group(xbar));

  # 内部整合性: |xbar|=5 は素数なので unitCond <=> surjCond は数学的に保証される
  # (真の較正チェック; 期待 m 集合の一致とは独立)
  consistencyOK := (unitCond = surjCond);
  if not consistencyOK then
    consistencyFailCount := consistencyFailCount + 1;
  fi;

  isShadow := hex33 and hex34 and unitCond and surjCond;
  if isShadow then Add(passingM, m); fi;

  Print(m, " | ", u, " | ", PF(hex33), " | ", PF(hex34), " | ", PF(unitCond), " | ",
        PF(surjCond), " | ", PF(isShadow), "\n");
od;

Print("[", PF(consistencyFailCount = 0), "] 全 m で unit条件 <=> 全射性 の内部整合 (不整合 ",
      consistencyFailCount, " 件)\n");
if consistencyFailCount <> 0 then failures := failures + 1; fi;

# 期待値との比較は「一級の計算結果」の報告であって、これに合わせて判定を書き換えない。
Print("\n実際に計算で通った m の集合(hex33 and hex34 and unit and surj): ", passingM, "\n");
expectedM := [0, 1, 3, 4];;
Print("外部監査の予想: ", expectedM, "\n");
if passingM = expectedM then
  Print("比較結果: 一致 (期待どおり)\n");
else
  Print("比較結果: 不一致 -- 重要な発見として報告する(期待に合わせて書き換えない)\n");
fi;

# T(c) の検査: 通った各 m について (sigma1^u sigma2^u sigma1^u)^2 = cbar^u
Print("\n--- T(c) 検査 (通った m のみ) ---\n");
tcFail := 0;;
for m in passingM do
  u := 2*m + 1;
  lhsTc := (sigma1^u * sigma2^u * sigma1^u)^2;
  rhsTc := cbar^u;
  ok := (lhsTc = rhsTc);
  Print("[", PF(ok), "] m=", m, "  T(c): (s1^u s2^u s1^u)^2 = c^u : ", ok, "\n");
  if not ok then tcFail := tcFail + 1; fi;
od;
if tcFail = 0 then
  Print("[", PF(true), "] T(c) 検査、通った全 m (", Length(passingM), " 個) で一致\n");
else
  Print("[", PF(false), "] T(c) 検査、不一致 ", tcFail, " 件\n");
  failures := failures + 1;
fi;

# ####################################################################
# 総括
# ####################################################################
Print("\n############################################################\n");
if failures = 0 then
  Print("WP1 ALL PASSED\n");
else
  Print("WP1 FAILURES: ", failures, "\n");
fi;
QUIT;
