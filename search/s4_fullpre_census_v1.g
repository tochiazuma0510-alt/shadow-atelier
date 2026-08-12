# search/s4_fullpre_census_v1.g -- S4-FULLPRE census(裁定955【1】・仕様=docs/notes/ideas_r3_s4order_v1.md 札②)
#
# 実行: .\gap.ps1 search\s4_fullpre_census_v1.g
#
# 標的群: Hol(Z/9) = Aff(Z/9) = Z/9 rtimes (Z/9)^x, 位数 54, IdGroup [54,6]
#   (docs/notes/ideas_r3_s4order_v1.md 冒頭 pin: "GT(N_S4) cong Hol(Z/9) -- PSL(2,8)は窓の商であって
#   標的群ではない")
#
# 目的(封印非接触・u 非接触・秒級・生値のみ):
#   ① 全部分群の一覧 + 各位数
#   ② chi 射影(G -> G/N cong (Z/9)^x cong Z/6, N=Z/9=平行移動部)との交わり
#      -- chi-全射部分群(H の chi(H) = 全 Z/6)をフラグ
#   ③ graph 型の有無 -- H が「標準の pullback 部分群」(N_d と標準complement Q0 の
#      order-|chi(H)| 部分群 K_std から生成される N_d*K_std)と一致するか否か。
#      不一致(同じ位数・同じ N-成分・同じ chi(H) だが実体が異なる)なら graph 型。
#      (定義の出所: docs/notes/k9_kummer_supp_v1.md 3.1「graph 型部分群(k が u の関数になるもの)」
#       -- K9-FULLPRE の n=9 版と同じ意味論を Hol(Z/9) の部分群全体に総当たりで適用する)

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# s4_fullpre_census_v1.g -- Hol(Z/9) 部分群 census(裁定955)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;
failures := 0;;

# ====================================================================
# G := Hol(Z/9) の構成(明示的半直積、GAP ライブラリの HolomorphismGroup 等は使わず、
#      本工房の convention どおり明示的な置換/行列構成で作る)
# ====================================================================
# N = Z/9 (加法的、平行移動)。Q = (Z/9)^x = {1,2,4,5,7,8} cong Z/6(乗法的)。
# G の元は (a,u), a in Z/9, u in (Z/9)^x。積: (a,u)*(b,v) = (a+u*b mod 9, u*v mod 9)。
# 置換表現: G は Z/9 上のアフィン変換 x -> u*x+a として作用(9 点上の置換)。

AffPerm := function(a, u)
  local images, x;
  images := [];
  for x in [0..8] do
    images[x+1] := ((u*x + a) mod 9) + 1;
  od;
  return PermList(images);
end;;

units9 := Filtered([1..8], u -> Gcd(u,9)=1);;   # (Z/9)^x = {1,2,4,5,7,8}, |units9|=6
Print("(Z/9)^x = ", units9, " (期待 6 元)\n");

genElts := [];;
for a in [0..8] do
  for u in units9 do
    Add(genElts, AffPerm(a,u));;
  od;
od;;
G := Group(genElts);;
sizeG := Size(G);;
Print("[", PF(sizeG = 54), "] |Hol(Z/9)| = ", sizeG, " (期待 54)\n");
if sizeG <> 54 then failures := failures + 1; fi;

idG := IdGroup(G);;
Print("IdGroup(G) = ", idG, " (期待 [54,6])\n");
idGroupOk := (idG = [54,6]);;
Print("[", PF(idGroupOk), "] IdGroup 一致\n");
if not idGroupOk then failures := failures + 1; fi;

# N = Z/9 の平行移動部分群(標準・正規)
N := Group(AffPerm(1,1));;   # a=1,u=1 の元、位数9の巡回群
sizeN := Size(N);;
Print("|N| (平行移動部) = ", sizeN, " (期待 9)\n");
# 陽性対照(裁定961の恒久規範): N.1 が恒等元でない(位数9)ことを明示的に較正する
Assert(0, Order(N.1) = 9);;
Print("[陽性対照] N.1 の位数 = ", Order(N.1), " (期待 9・恒等元でないことの較正)\n");
normalN := IsNormal(G, N);;
Print("[", PF(normalN), "] N は G で正規\n");
if not normalN then failures := failures + 1; fi;

# Q0 = 標準乗法complement (a=0 の元全体)
Q0 := Group(List(units9, u -> AffPerm(0,u)));;
sizeQ0 := Size(Q0);;
Print("|Q0| (標準 complement) = ", sizeQ0, " (期待 6)\n");

# 裁定961(falsifier CV-9 判読で確定): Q0.1 = AffPerm(0,1) = 恒等置換(units9 の先頭が 1)。
# GeneratorsOfGroup(Q0) の最初の元を無条件に「生成元」として使うと、生成元リストの先頭が
# たまたま恒等元の場合に (Q0.1)^k が常に恒等になる欠陥を生む(v1 の実際のバグ)。
# 修理: 位数6の元を明示的に探して使う + 陽性対照(非自明値を返すことの較正)を必ず入れる。
gen6 := First(GeneratorsOfGroup(Q0), g -> Order(g)=6);;
if gen6 = fail then gen6 := First(Q0, g -> Order(g)=6);; fi;
Assert(0, gen6 <> fail);;
Assert(0, Order(gen6) = 6);;
Print("[陽性対照] gen6 の位数 = ", Order(gen6), " (期待 6・恒等元でないことの較正)\n");

# chi: G -> G/N (自然な商写像、IsomorphismQuotientGroups あるいは FactorCosetAction 経由)
quotHom := NaturalHomomorphismByNormalSubgroup(G, N);;
QuotG := Image(quotHom);;
sizeQuotG := Size(QuotG);;
Print("|G/N| = ", sizeQuotG, " (期待 6)\n");

# ====================================================================
# 全部分群の列挙
# ====================================================================
Print("\n============================================================\n");
Print("# 全部分群の列挙\n");
Print("============================================================\n");

allSubs := AllSubgroups(G);;
Print("全部分群数 = ", Length(allSubs), "\n");

# 位数ごとの内訳
orderCounts := [];;
for H in allSubs do
  ord := Size(H);;
  found := First(orderCounts, e -> e.order = ord);;
  if found = fail then
    Add(orderCounts, rec(order:=ord, count:=1));
  else
    found.count := found.count + 1;;
  fi;
od;;
Sort(orderCounts, function(a,b) return a.order < b.order; end);;
Print("位数ごとの部分群数: ");
for e in orderCounts do Print("|H|=", e.order, ":", e.count, "  "); od;
Print("\n");

# ====================================================================
# 各部分群について: chi(H) の位数(chi-全射か)・N∩H の位数(=N_d)・graph型か
# ====================================================================
Print("\n============================================================\n");
Print("# 各部分群の分類(chi 射影・graph 型判定)\n");
Print("============================================================\n");

# 標準 pullback 部分群テーブル: 各 (d, k) (d | 9, k | 6) について N_d * K_std を事前構成
divisors9 := [1,3,9];;
divisors6 := DivisorsInt(6);;   # [1,2,3,6]
stdPullbackTable := [];;
for d in divisors9 do
  Nd := Subgroup(N, [ (N.1)^(9/d) ]);;   # N の位数 d の部分群(N=Z/9 巡回)
  for k in divisors6 do
    Kstd := Subgroup(Q0, [ gen6^(6/k) ]);;   # Q0 の位数 k の部分群(gen6 は位数6の陽性対照済み生成元)
    Pstd := ClosureGroup(Nd, Kstd);;
    Add(stdPullbackTable, rec(d:=d, k:=k, Nd:=Nd, Kstd:=Kstd, Pstd:=Pstd, size:=Size(Pstd)));
  od;
od;;

detail := [];;
chiSurjCount := 0;;
graphTypeCount := 0;;
fullPullbackCount := 0;;
for H in allSubs do
  ord := Size(H);;
  HcapN := Intersection(H, N);;
  dH := Size(HcapN);;
  chiH := Image(quotHom, H);;
  kH := Size(chiH);;
  isChiSurjective := (kH = sizeQuotG);;
  if isChiSurjective then chiSurjCount := chiSurjCount + 1; fi;

  # 標準 pullback との一致判定: 同じ (d,k) を持つ stdPullbackTable のエントリを探し、
  # H がそれと GAP 群として等しいか(同一部分群かどうか、共役でなく厳密な集合一致で判定
  # -- 「同じ不変量だが実体が違う」= graph 型 の定義そのもの)。
  stdEntry := First(stdPullbackTable, e -> e.d = dH and e.k = kH);;
  isFullPullback := false;;
  if stdEntry <> fail then
    isFullPullback := (H = stdEntry.Pstd);;
  fi;
  isGraphType := (not isFullPullback) and (ord = stdEntry.size);;  # 同じ位数で標準型と一致しない
  if isFullPullback then fullPullbackCount := fullPullbackCount + 1; fi;
  if isGraphType then graphTypeCount := graphTypeCount + 1; fi;

  Add(detail, rec(order:=ord, d_N_component:=dH, k_chi_image:=kH,
                   chi_surjective:=isChiSurjective, full_pullback:=isFullPullback,
                   graph_type:=isGraphType));
od;;

Print("chi-全射部分群の数 = ", chiSurjCount, " / ", Length(allSubs), "\n");
Print("標準 full-pullback 型の部分群数 = ", fullPullbackCount, "\n");
Print("graph 型(標準型と不一致・同位数)の部分群数 = ", graphTypeCount, "\n");
Print("[", PF(fullPullbackCount + graphTypeCount <= Length(allSubs)), "] 内訳の整合性(参考)\n");

# chi-全射部分群のみの共役類数(K9-FULLPRE の n=9 版で言及される「ちょうど3共役型」との比較用)
chiSurjSubs := Filtered(allSubs, H -> Size(Image(quotHom,H)) = sizeQuotG);;
chiSurjConjClasses := [];;
for H in chiSurjSubs do
  already := ForAny(chiSurjConjClasses, cls -> IsConjugate(G, cls[1], H));;
  if not already then Add(chiSurjConjClasses, [H]); fi;
od;;
Print("chi-全射部分群の G-共役類数 = ", Length(chiSurjConjClasses), "\n");

# graph 型部分群の一覧(位数・(d,k))詳細
graphDetail := Filtered(detail, e -> e.graph_type);;
Print("\ngraph 型部分群の詳細一覧:\n");
for e in graphDetail do
  Print("  |H|=", e.order, "  N-成分位数(d)=", e.d_N_component, "  chi(H)位数(k)=", e.k_chi_image, "\n");
od;;

# ====================================================================
# 総括
# ====================================================================
Print("\n############################################################\n");
if failures = 0 then
  Print("S4-FULLPRE-CENSUS ALL PASSED\n");
else
  Print("S4-FULLPRE-CENSUS FAILURES: ", failures, "\n");
fi;

t1 := GAPLIB_WallElapsedMs();;
Print("経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_s4fp.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

OrderCountsJson := function(lst)
  local parts, e;
  parts := [];
  for e in lst do
    Add(parts, Concatenation("{\"order\":", String(e.order), ",\"count\":", String(e.count), "}"));
  od;
  return JArr(parts);
end;;

DetailJson := function(lst)
  local parts, e;
  parts := [];
  for e in lst do
    Add(parts, Concatenation(
      "{\"order\":", String(e.order),
      ",\"d_N_component\":", String(e.d_N_component),
      ",\"k_chi_image\":", String(e.k_chi_image),
      ",\"chi_surjective\":", JB(e.chi_surjective),
      ",\"full_pullback\":", JB(e.full_pullback),
      ",\"graph_type\":", JB(e.graph_type), "}"));
  od;
  return JArr(parts);
end;;

scriptSha256 := ComputeSha256File("search/s4_fullpre_census_v1.g");;

cert := Concatenation(
  "{\"schema\":\"s4-fullpre-census/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/s4_fullpre_census_v1.g\",\"order\":\"裁定955 / docs/notes/ideas_r3_s4order_v1.md 札2\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"target_group\":{\"name\":\"Hol(Z/9)\",\"size\":", String(sizeG), ",\"idgroup\":", JArr([String(idG[1]),String(idG[2])]), "}",
  ",\"structure_check\":{\"normal_N_size\":", String(sizeN), ",\"N_is_normal\":", JB(normalN),
    ",\"quotient_size\":", String(sizeQuotG), ",\"idgroup_pass\":", JB(idGroupOk), "}",
  ",\"positive_control\":{\"note\":\"裁定961恒久規範: 陰性値(0件)を返し得る計器の較正 -- N.1/gen6 が恒等元でないことを明示検査\",",
    "\"N1_order\":", String(Order(N.1)), ",\"N1_order_expected\":9,",
    "\"gen6_order\":", String(Order(gen6)), ",\"gen6_order_expected\":6}",
  ",\"total_subgroup_count\":", String(Length(allSubs)),
  ",\"order_counts\":", OrderCountsJson(orderCounts),
  ",\"chi_surjective_count\":", String(chiSurjCount),
  ",\"chi_surjective_conjugacy_class_count\":", String(Length(chiSurjConjClasses)),
  ",\"full_pullback_count\":", String(fullPullbackCount),
  ",\"graph_type_count\":", String(graphTypeCount),
  ",\"detail\":", DetailJson(detail),
  ",\"u_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"overall_failures\":", String(failures),
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/s4_fullpre_census_v2_20260812.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");

Print("\nS4-FULLPRE-CENSUS DONE\n");
QUIT;
