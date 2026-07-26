#############################################################################
# search/k5-ninf-exclusion.g -- (N_infty) 副枝の排除証明書(GAP 側・第一系統)
#
# 委嘱: docs/week4-K5_Rule1_v1.md v1.2 (S11 論点 7 / 補題 R1-N∞-S) の
# 「選択肢 1(組合せ的排除証明書)」を、凍結済み有限 fixture
# (certificates/k5fixture/K5-sq.json, K5-ns.json の perm_triple フィールド)
# だけを入力とする有限計算で実施する。launch blocker ではない任意の補強
# (v1.2 §11 論点 7 冒頭)。
#
# 補題 R1-N∞-S 3.: 副枝 (N_infty) が生じるなら、ordered dessin は底の
# Mobius 対合 lambda -> 1/lambda による (0 infty)-交換で不変でなければ
# ならない。この交換は monodromy 三つ組のレベルでは
#   sigma_0 <-> sigma_infty を交換し sigma_1 を保つ、simultaneous
#   conjugation を実現する g in S_10 の存在
# として現れる(委嘱書の指定: 「向き規約に依存しない保守形 -- sigma_0 <-> sigma_infty
# の交換を実現する S_10 の元の存在」)。したがって
#   その g が存在しない  =>  (0 infty)-交換不変性が破れる
#                        => 補題 R1-N∞-S 3. の対偶により (N_infty) はこの
#                           dessin について発火し得ない(排除)。
#   その g が存在する    =>  判定不能(排除できない。別途厳密な捻り三つ組の
#                           確定が必要 -- 論点7の記述どおり)。
#
# 期待(「対称性なし ⇒ 発火しない」)は判定には使わない。結果は結果として
# そのまま記録する。
#
# 接触禁止: 曲線・lambda・u・数値近似・database には一切触れない。M・lambda・u
# には一切触れない(perm_triple のみが入力)。
#
# 第二系統: crosscheck/check-k5-ninf.mjs(node・helper 非共有・本ファイルの
# ソースは読まない独立実装 -- 総当り brute force で同じ存在問題を解く)。
#
# 実行: .\gap.ps1 search\k5-ninf-exclusion.g
#############################################################################

Read("search/gaplib_common.g");

# ---------------------------------------------------------------- fixture data
# 出所: certificates/k5fixture/K5-sq.json / K5-ns.json の "perm_triple" フィールド
# (search/k5-blocks-check.g と同一の転記値・0-indexed one-line)。
Fixtures := rec(
  sq := rec(
    s0 := [1,2,3,4,5,6,7,8,9,0],
    s1 := [0,1,8,9,6,7,4,5,2,3],
    sInf := [3,0,1,8,9,6,7,4,5,2]
  ),
  ns := rec(
    s0 := [1,2,3,4,5,6,7,8,9,0],
    s1 := [4,7,2,5,0,3,8,1,6,9],
    sInf := [9,4,7,2,5,0,3,8,1,6]
  )
);;

# 0-indexed image list -> GAP PermList (1-indexed): i^p = list0[i-1] + 1
ToPerm := function(list0)
  return PermList(List(list0, x -> x + 1));
end;;

CycleTypeOn := function(g, dom)
  local lens;
  lens := ShallowCopy(CycleLengths(g, dom));
  Sort(lens, function(a,b) return a > b; end);
  return lens;
end;;

totalPass := 0;; totalFail := 0;;
Check := function(name, ok, extra)
  if ok then totalPass := totalPass + 1; else totalFail := totalFail + 1; fi;
  if ok then
    Print("[PASS] ", name, "  ", extra, "\n");
  else
    Print("[FAIL] ", name, "  ", extra, "\n");
  fi;
end;;

S10 := SymmetricGroup(10);;

results := rec();;

ProcessTarget := function(label, fx)
  local s0, s1, sInf, ok0, dom, t0, t1, tInf, oddMultCount, lens, cnt,
        conj, exists, gList, exclusion, rec2;
  dom := [1..10];
  s0 := ToPerm(fx.s0); s1 := ToPerm(fx.s1); sInf := ToPerm(fx.sInf);

  Print("\n==== target: ", label, " ====\n");

  # -- sanity: sigma_0 sigma_1 sigma_infty = id, convention (p o q)(i) = p(q(i))
  # i.e. apply sigma_infty first, then sigma_1, then sigma_0.
  ok0 := sInf*s1*s0 = ();
  Check(Concatenation(label, "-S0 sigma_0 sigma_1 sigma_infty = id (composition conv.)"), ok0, "");

  # -- cheap invariants (informational only -- doc notes these are "powerless"
  # as exclusion tools in this campaign because they hold automatically)
  t0 := CycleTypeOn(s0, dom);
  tInf := CycleTypeOn(sInf, dom);
  t1 := CycleTypeOn(s1, dom);
  Check(Concatenation(label, "-INV sigma_0 is a single 10-cycle"), t0 = [10], Concatenation("got ", String(t0)));
  Check(Concatenation(label, "-INV sigma_infty is a single 10-cycle"), tInf = [10], Concatenation("got ", String(tInf)));
  Check(Concatenation(label, "-INV sigma_1 has even sign (product relation forces this)"), SignPerm(s1) = 1, "");
  oddMultCount := Length(Filtered(t1, x -> x mod 2 = 1));
  Check(Concatenation(label, "-INV # odd-length cycles of sigma_1 <= 6 (R1-N-infty-S pt.4 necessary cond.)"),
        oddMultCount <= 6, Concatenation("count = ", String(oddMultCount)));

  # -- the actual test: does there exist g in S_10 realizing the (0 infty)
  # exchange, i.e. simultaneous conjugation
  #   s0 -> sInf,  s1 -> s1,  sInf -> s0 ?
  # GAP convention x^g = g^-1 * x * g; existence is convention-independent.
  conj := RepresentativeAction(S10, [s0, s1, sInf], [sInf, s1, s0], OnTuples);
  exists := conj <> fail;
  if exists then
    gList := List(dom, i -> i^conj - 1);   # back to 0-indexed one-line for the record
  else
    gList := fail;
  fi;
  exclusion := not exists;
  Check(Concatenation(label, "-MAIN (0,infty)-exchange conjugator g in S_10: exists?"), true,
        Concatenation("exists = ", String(exists)));
  if exclusion then
    Print("  => (N_infty) EXCLUDED for target ", label, " (no such g; contrapositive of R1-N-infty-S 3.)\n");
  else
    Print("  => (N_infty) NOT excluded by this certificate for target ", label,
          " (a conjugator g exists; UNDETERMINED, not a proof of presence)\n");
  fi;

  rec2 := rec(
    target := label,
    sanity_relation_ok := ok0,
    cycle_type_sigma0 := t0,
    cycle_type_sigmaInf := tInf,
    cycle_type_sigma1 := t1,
    sign_sigma1 := SignPerm(s1),
    odd_length_cycle_count_sigma1 := oddMultCount,
    conjugator_exists := exists,
    conjugator_g_0indexed := gList,
    ninf_excluded := exclusion
  );
  results.(label) := rec2;
end;;

ProcessTarget("sq", Fixtures.sq);
ProcessTarget("ns", Fixtures.ns);

Print("\n=== ", totalPass, "/", totalPass + totalFail, " PASS (structural sanity/invariant checks) ===\n");

# ---------------------------------------------------------------- certificate
GStr := function(g)
  if g = fail then
    return "null";
  else
    return JArr(List(g, String));
  fi;
end;;

certJson := Concatenation(
  "{",
  "\"schema\":\"k5pipeline/ninf-exclusion-gap/v1\",",
  "\"pass\":", String(totalPass), ",",
  "\"fail\":", String(totalFail), ",",
  "\"method\":\"RepresentativeAction(SymmetricGroup(10), [s0,s1,sInf], [sInf,s1,s0], OnTuples)\",",
  "\"targets\":{",
  "\"sq\":{",
    "\"sanity_relation_ok\":", JB(results.sq.sanity_relation_ok), ",",
    "\"cycle_type_sigma0\":", JArr(List(results.sq.cycle_type_sigma0, String)), ",",
    "\"cycle_type_sigmaInf\":", JArr(List(results.sq.cycle_type_sigmaInf, String)), ",",
    "\"cycle_type_sigma1\":", JArr(List(results.sq.cycle_type_sigma1, String)), ",",
    "\"sign_sigma1\":", String(results.sq.sign_sigma1), ",",
    "\"odd_length_cycle_count_sigma1\":", String(results.sq.odd_length_cycle_count_sigma1), ",",
    "\"conjugator_exists\":", JB(results.sq.conjugator_exists), ",",
    "\"conjugator_g_0indexed\":", GStr(results.sq.conjugator_g_0indexed), ",",
    "\"ninf_excluded\":", JB(results.sq.ninf_excluded),
  "},",
  "\"ns\":{",
    "\"sanity_relation_ok\":", JB(results.ns.sanity_relation_ok), ",",
    "\"cycle_type_sigma0\":", JArr(List(results.ns.cycle_type_sigma0, String)), ",",
    "\"cycle_type_sigmaInf\":", JArr(List(results.ns.cycle_type_sigmaInf, String)), ",",
    "\"cycle_type_sigma1\":", JArr(List(results.ns.cycle_type_sigma1, String)), ",",
    "\"sign_sigma1\":", String(results.ns.sign_sigma1), ",",
    "\"odd_length_cycle_count_sigma1\":", String(results.ns.odd_length_cycle_count_sigma1), ",",
    "\"conjugator_exists\":", JB(results.ns.conjugator_exists), ",",
    "\"conjugator_g_0indexed\":", GStr(results.ns.conjugator_g_0indexed), ",",
    "\"ninf_excluded\":", JB(results.ns.ninf_excluded),
  "}",
  "}",
  "}"
);;

WriteFile("certificates/k5pipeline/ninf-exclusion.gap.json", certJson);;
Print("wrote certificates/k5pipeline/ninf-exclusion.gap.json\n");

if totalFail > 0 then
  Print("*** THERE ARE FAILURES ***\n");
fi;

QUIT;
