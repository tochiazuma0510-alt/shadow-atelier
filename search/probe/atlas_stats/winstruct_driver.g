# winstruct_driver.g -- atlas 統計調査 穴(1)(3) 用の窓構造 cert バッチ(探索器側)
#
# 実行: .\gap.ps1 search\probe\atlas_stats\winstruct_driver.g
#
# 対象窓: 穴(1) n=15 / 穴(3) mixed-2-and-odd n in {6,10,12,14,18} (K^(20) は既済で除外)
# 各窓は K^(n) = ker(psi_n: PB3 -> G_n) の"直接"構成のみを使う。K^(5) への還元・Im R・
# d_N・u 値・封印3量には一切触れない(委嘱の禁止列)。K^(10)/K^(15) は K^(5) の倍数窓
# だが、還元写像は構成しない -- 各窓を MakeGn(n) で独立に構成し、GT(K^(n)) を hexagon
# 走査で自窓のみから直接列挙する。
#
# 出典: docs/week1-定義ノート.md 数値事実行 + Thm 4.3 行(GT(K^(n)) の閉じた式)。
# 助変数(MakeGn/AbstractProd/EnumerateReducedHexagon/JSON helper)は
# search/week3-battery-common.g から無変更で流用(既存検証済みインフラ)。
#
# 出力: 窓ごとに search/certs/winstruct_K{n}_20260805.json (探索器の生出力のみ;
# Thm 4.3 との照合判定はここではしない -- 別系統の crosscheck スクリプトの仕事)。

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/week3-battery-common.g");

TargetNs := [15, 6, 10, 12, 14, 18];;

ExpectedGOrder := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

# FindRPower: find e in [0,n-1] with r^e = elt, or fail if elt is not a power of r.
FindRPower := function(r, elt, n)
  local e;
  for e in [0..n-1] do
    if r^e = elt then return e; fi;
  od;
  return fail;
end;;

# 2-part / odd-part split of a positive integer
TwoOddSplit := function(k)
  local two, odd;
  two := 1;  odd := k;
  while odd mod 2 = 0 do
    two := two * 2;  odd := odd / 2;
  od;
  return [two, odd];
end;;

JNum := function(x) return String(x); end;;

for n in TargetNs do
  Print("=== n = ", n, " ===\n");
  gn := MakeGn(n);
  G := gn.G;  x := gn.x;  y := gn.y;  r := gn.r;  s := gn.s;

  Gorder := Size(G);
  expected := ExpectedGOrder(n);
  okOrder := (Gorder = expected);
  Print("|G_", n, "| = ", Gorder, " (expected ", expected, ") ", PF(okOrder), "\n");

  Nord := Lcm(n, 2);
  NordCheck := Lcm(Order(x), Order(y));
  okNord := (Nord = NordCheck);
  Print("N_ord = ", Nord, " (elt-order cross-check ", NordCheck, ") ", PF(okNord), "\n");

  # n1 = ord(r^2) in D_n: n/2 if n even, n if n odd
  if n mod 2 = 0 then n1 := n/2; else n1 := n; fi;
  okOrderR2 := (Order(r^2) = n1);
  Print("n1 = ord(r^2) = ", n1, " (Order(r^2)=", Order(r^2), ") ", PF(okOrderR2), "\n");

  # charming set X_n = {m in 0..Nord-1 : gcd(2m+1,Nord)=1}
  charmingSet := Filtered([0..Nord-1], m -> Gcd(2*m+1, Nord) = 1);
  Print("|X_", n, "| = ", Length(charmingSet), "\n");

  # derived subgroup D = [G,G] (the finite "kernel"-type structure quantity for this window --
  # the charming condition's target subgroup f in D = F2/N_F2 derived subgroup)
  D := DerivedSubgroup(G);
  Dorder := Size(D);
  Dstruct := StructureDescription(D);
  Dabelian := IsAbelian(D);
  Dsolvable := IsSolvable(D);
  if Dsolvable then Ddl := DerivedLength(D); else Ddl := -1; fi;
  Dsplit := TwoOddSplit(Dorder);

  Gsolvable := IsSolvable(G);
  if Gsolvable then Gdl := DerivedLength(G); else Gdl := -1; fi;
  Gsplit := TwoOddSplit(Gorder);

  Print("|D|=|[G,G]| = ", Dorder, "  struct=", Dstruct, "  abelian=", Dabelian,
        "  solvable=", Dsolvable, "  dl=", Ddl, "\n");
  Print("G solvable=", Gsolvable, "  dl=", Gdl, "\n");

  # hexagon scan: full GT(K^(n)) via reduced hexagon (quotient shortcut; c_in_N = true
  # for all Dih windows -- K^(m) subset K^(m) contains c always, cf. week1 note (3.1)).
  t0 := Runtime();
  res := EnumerateReducedHexagon(gn, charmingSet);
  t1 := Runtime();
  Print("hexagon scan: candidate_total=", res.candidate_total, " shadow_total=", res.shadow_total,
        " h10_fail=", res.h10_fail, " h11_fail=", res.h11_fail, " generation_fail=", res.generation_fail,
        " (", (t1-t0), " ms)\n");

  # decode each shadow (m,f) -> (m,k) via component 1 of f = r^{2k} mod n.
  # n even: e must be even, k := (e/2) mod n1 (n1=n/2).
  # n odd: 2 is invertible mod n (gcd(2,n)=1), k := e * inv2 mod n (n1=n).
  if n mod 2 = 1 then
    inv2 := (n+1)/2;  # integer; 2*inv2 = n+1 = 1 mod n
  fi;
  decoded := [];
  decodeFailCount := 0;
  for sh in res.shadows do
    comp1 := compOfBlock(sh.f, 0, n);
    e := FindRPower(r, comp1, n);
    if e = fail then
      decodeFailCount := decodeFailCount + 1;
      Add(decoded, rec(m := sh.m, k := fail, e := fail));
    elif n mod 2 = 0 and e mod 2 <> 0 then
      decodeFailCount := decodeFailCount + 1;
      Add(decoded, rec(m := sh.m, k := fail, e := e));
    else
      if n mod 2 = 0 then
        kval := (e/2) mod n1;
      else
        kval := (e * inv2) mod n;
      fi;
      Add(decoded, rec(m := sh.m, k := kval, e := e));
    fi;
  od;

  Print("decode: ", Length(decoded), " shadows decoded, ", decodeFailCount, " decode failures\n");

  # ---------------- JSON assembly ----------------
  shadowItems := [];
  for d in decoded do
    if d.k = fail then
      Add(shadowItems, Concatenation("{\"m\":", String(d.m), ",\"k\":null,\"e\":null,\"decode_ok\":false}"));
    else
      Add(shadowItems, Concatenation("{\"m\":", String(d.m), ",\"k\":", String(d.k), ",\"e\":", String(d.e), ",\"decode_ok\":true}"));
    fi;
  od;

  certObj := Concatenation(
    "{",
    "\"cert_version\":\"winstruct_v1\",",
    "\"window\":\"K(", String(n), ")\",",
    "\"n\":", String(n), ",",
    "\"generated\":\"20260805\",",
    "\"tier\":\"calibration\",",
    "\"scope_note\":\"direct construction of K(n) only; no reduction to K(5); no Im R / d_N / u-values / sealed quantities touched\",",
    "\"G_order\":", String(Gorder), ",",
    "\"G_order_expected\":", String(expected), ",",
    "\"G_order_ok\":", JB(okOrder), ",",
    "\"N_ord\":", String(Nord), ",",
    "\"N_ord_elt_order_crosscheck\":", String(NordCheck), ",",
    "\"N_ord_ok\":", JB(okNord), ",",
    "\"n1_ord_r2\":", String(n1), ",",
    "\"n1_ok\":", JB(okOrderR2), ",",
    "\"charming_set\":", JArr(List(charmingSet, String)), ",",
    "\"charming_set_size\":", String(Length(charmingSet)), ",",
    "\"derived_subgroup_order\":", String(Dorder), ",",
    "\"derived_subgroup_struct\":", JStr(Dstruct), ",",
    "\"derived_subgroup_abelian\":", JB(Dabelian), ",",
    "\"derived_subgroup_solvable\":", JB(Dsolvable), ",",
    "\"derived_subgroup_derived_length\":", String(Ddl), ",",
    "\"derived_subgroup_2part\":", String(Dsplit[1]), ",",
    "\"derived_subgroup_oddpart\":", String(Dsplit[2]), ",",
    "\"G_solvable\":", JB(Gsolvable), ",",
    "\"G_derived_length\":", String(Gdl), ",",
    "\"G_2part\":", String(Gsplit[1]), ",",
    "\"G_oddpart\":", String(Gsplit[2]), ",",
    "\"hexagon_scan\":{",
      "\"candidate_total\":", String(res.candidate_total), ",",
      "\"dwords_count\":", String(res.dwords_count), ",",
      "\"h10_fail\":", String(res.h10_fail), ",",
      "\"h11_fail\":", String(res.h11_fail), ",",
      "\"generation_fail\":", String(res.generation_fail), ",",
      "\"shadow_total\":", String(res.shadow_total),
    "},",
    "\"decode_fail_count\":", String(decodeFailCount), ",",
    "\"shadows_mk\":[", JoinC(shadowItems, ","), "]",
    "}"
  );

  outPath := Concatenation("search/certs/winstruct_K", String(n), "_20260805.json");
  WriteFile(outPath, certObj);
  Print("wrote ", outPath, "\n\n");
od;

Print("winstruct_driver.g done.\n");
QUIT;
