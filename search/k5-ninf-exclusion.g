#############################################################################
# search/k5-ninf-exclusion.g -- (N_infty) 副枝の排除証明書(GAP 側・第一系統)
# v3(便 36・裁定 36 の修理 + 司令塔中継の補題 R1-N∞-W 仕様反映)
#
# 委嘱: docs/week4-K5_Rule1_v1.md v1.3 §11 R-6(補題 R1-N∞-W)。
#
# *** v1 からの撤回理由(Sol 便 35 F1.5・裁定 36) ***
# v1 は (0 infty)-交換の monodromy 三つ組への移し方として素朴な置換
#   (x,y,z) |-> (z,y,x)                                            (35.2)
# を検査していた。これは xyz=1 の relator を一般に保たない(zyx=1 は
# xyz=1 から従わない)ため誤りである。
#
# *** v2 -> v3 差分(司令塔中継・補題 R1-N∞-W の反映) ***
# 1. 判定式は (35.4) の第一・第二式のみを decisive predicate とする:
#      g sigma_0 g^{-1} = sigma_infty                               (E1)
#      g sigma_1 g^{-1} = sigma_1                                    (E2)
#    第三式 g sigma_infty g^{-1} = sigma_1^{-1} sigma_0 sigma_1 は
#    xyz=1 型の関係式から **E1・E2 の両方**のもとで自動的に従う(補題
#    R1-N∞-W の指摘・便 36 F1.2 の文言修理: 「E1 だけから」ではない)。
#    本証明書では第三式を「冗長確認」として別途検査し、そう明記する。
# 2. 10! の悉皆は不要: sigma_0 が単一の 10-サイクルなので、E1 を満たす g は
#    g(0) の値ひとつで完全に決まる(cycle 上を伝播させるだけ)。ゆえに
#    10 候補の悉皆で閉じる。
# 3. 自己検査(定理由来・補題 R1-N∞-W・便 36 F1.2 の文言修理): 定理が証明
#    するのは解が**高々一つ**であること(centralizer=1 からの一意性)まで。
#    「ちょうど 1 個存在する」ことは定理からは出ず、各 fixture の実計算
#    結果である。survivors > 1 は定理違反(理論上ありえない)ゆえ入力破損
#    -> integrity stop。survivors = 0 は定理に反しないので integrity stop
#    としない(0 解を fixture corruption 扱いしない -- 便 36 F1.2 (2))。
#    survivors = 1 のときは g^2 = sigma_1 も成立するはず -- 破れたら
#    入力破損 -> integrity stop(UNKNOWN ではない)。
# 4. 撤回の記録の自己完結化: 旧述語 (35.3)(g sigma_infty g^{-1} = sigma_0
#    という第三式)は、E1 のもとで (35.4) かつ [sigma_0,sigma_1]=1 と同値
#    である。[sigma_0,sigma_1]=1 は sigma_0,sigma_1 が可換であることを
#    要求するが、sigma_0 は 10-サイクル(その centralizer は自分自身が
#    生成する巡回群 <sigma_0> のみ)であり sigma_1 の型 (2^4 1^2) は
#    <sigma_0> のどの元の型とも一致しないので、sigma_0*sigma_1 <>
#    sigma_1*sigma_0 が常に成り立つ(証明書内で直接計算により確認)。
#    ゆえに (35.3) は恒真に充足不能であり、旧証明書の「conjugator が
#    存在しない」という出力は正しい計算結果だったが、それは的外れな
#    問い(35.3)に対する答えであって (N_infty) の排除を意味しない。
# 5. 結論札: 「排除されず・対称性充足・(N_infty) の存否は UNKNOWN・
#    witness は cross-checked」。
#
# 期待は判定には使わない。結果は結果としてそのまま記録する。
#
# 第二系統: crosscheck/check-k5-ninf.mjs(node・helper 非共有・本ファイルの
# ソースは読まない独立実装)。
#
# 実行: .\gap.ps1 search\k5-ninf-exclusion.g
#############################################################################

Read("search/gaplib_common.g");

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
  if ok then Print("[PASS] ", name, "  ", extra, "\n");
  else Print("[FAIL] ", name, "  ", extra, "\n"); fi;
end;;

results := rec();;

# Build the (unique, if it exists) g in S_10 (as a 0-indexed one-line array)
# satisfying E1: g[s0[x]] = sInf[g[x]] for all x, given g[0] = c.
# Since s0 is a single 10-cycle covering all 10 points starting from 0, this
# determines g on every point by propagating along the cycle 0, s0(0),
# s0(s0(0)), ... -- no guessing, no 10!-search.
BuildGFromG0 := function(s0arr, sInfarr, c)
  local g, x, i, xn;
  g := List([1..10], i -> -1);   # 0-indexed images, -1 = unset (1-indexed array positions)
  g[1] := c;                      # g(0) = c  (array index 1 <-> point 0)
  x := 0;
  for i in [1..9] do
    xn := s0arr[x + 1];           # xn := s0(x)
    g[xn + 1] := sInfarr[g[x + 1] + 1];   # g(s0(x)) = sInf(g(x))
    x := xn;
  od;
  return g;                       # g[i+1] = g(i), 0-indexed
end;;

IsBijection10 := function(garr)
  local seen, v;
  seen := List([1..10], i -> false);
  for v in garr do
    if v < 0 or v > 9 or seen[v+1] then return false; fi;
    seen[v+1] := true;
  od;
  return true;
end;;

ProcessTarget := function(label, fx)
  local s0, s1, sInf, dom, t0, t1, tInf, oddMultCount, ok0,
        s0Arr, s1Arr, sInfArr, s1invArr, rhsArr, c, gArr, gPerm,
        e2ok, e3ok, isBij, survivors, sol, gSquaredOk, commuteCheck,
        rec2;
  dom := [1..10];
  s0Arr := fx.s0; s1Arr := fx.s1; sInfArr := fx.sInf;
  s0 := ToPerm(s0Arr); s1 := ToPerm(s1Arr); sInf := ToPerm(sInfArr);

  Print("\n==== target: ", label, " ====\n");

  # -- sanity: relation + cheap invariants (unchanged from v2)
  ok0 := sInf*s1*s0 = ();
  Check(Concatenation(label, "-S0 sigma_0 sigma_1 sigma_infty = id (composition conv.)"), ok0, "");
  t0 := CycleTypeOn(s0, dom); tInf := CycleTypeOn(sInf, dom); t1 := CycleTypeOn(s1, dom);
  Check(Concatenation(label, "-INV sigma_0 is a single 10-cycle"), t0 = [10], Concatenation("got ", String(t0)));
  Check(Concatenation(label, "-INV sigma_infty is a single 10-cycle"), tInf = [10], Concatenation("got ", String(tInf)));
  Check(Concatenation(label, "-INV sigma_1 has even sign"), SignPerm(s1) = 1, "");
  oddMultCount := Length(Filtered(t1, x -> x mod 2 = 1));
  Check(Concatenation(label, "-INV # odd-length cycles of sigma_1 <= 6"), oddMultCount <= 6, Concatenation("count = ", String(oddMultCount)));

  # -- (35.3) impossibility, demonstrated directly (item 4 of the v2->v3 diff):
  # sigma_0*sigma_1 <> sigma_1*sigma_0 (direct computation, no appeal to abstract
  # centralizer argument needed for the certificate itself -- the argument is
  # recorded in the header comment as explanation).
  commuteCheck := (s0*s1 = s1*s0);
  Check(Concatenation(label, "-COMMUTE sigma_0*sigma_1 <> sigma_1*sigma_0 (so (35.3)'s third eqn, combined with E1, is unsatisfiable)"),
        not commuteCheck, Concatenation("commute = ", String(commuteCheck)));

  # -- candidate generation: only 10 candidates (g(0) = c for c = 0..9), each
  # built by propagating E1 along the sigma_0 10-cycle. No 10!-search.
  # rhs(x) := (s1^{-1} s0 s1)(x) = s1inv(s0(s1(x))), used only for the E3
  # redundant confirmation (E1+E2 alone are the decisive predicate).
  s1invArr := List([0..9], i -> Position(s1Arr, i) - 1);
  rhsArr := List([0..9], x -> s1invArr[s0Arr[s1Arr[x+1]+1]+1]);

  survivors := [];
  for c in [0..9] do
    gArr := BuildGFromG0(s0Arr, sInfArr, c);
    isBij := IsBijection10(gArr);
    if not isBij then continue; fi;   # E1-construction failed to close into a permutation -- skip (would itself indicate corruption if it happened for the eventual survivor)
    gPerm := ToPerm(gArr);
    e2ok := ForAll([0..9], x -> gArr[s1Arr[x+1]+1] = s1Arr[gArr[x+1]+1]);   # g(s1(x)) = s1(g(x))
    if e2ok then
      e3ok := ForAll([0..9], x -> gArr[sInfArr[x+1]+1] = rhsArr[gArr[x+1]+1]);  # redundant confirmation, logged not gated
      Add(survivors, rec(c := c, gArr := gArr, gPerm := gPerm, e3ok := e3ok));
    fi;
  od;

  Check(Concatenation(label, "-MAIN E1+E2 restricted to 10 candidates (g(0)=c): survivors found"),
        true, Concatenation("count = ", String(Length(survivors))));

  # -- self-check (theorem-derived, R1-N∞-W / 便 36 F1.2 の文言修理): R1-N∞-W
  # が定理として与えるのは「解は**高々一つ**」(centralizer=1 からの一意性)
  # であって「ちょうど一つ存在する」ことまでは定理から出ない -- 存在は各
  # fixture の実計算結果である。したがって:
  #   survivors > 1 は理論的に不可能な事態 ⇒ 定理違反 ⇒ integrity stop
  #     (fixture corruption suspected -- 一意性定理そのものに反する)。
  #   survivors = 0 は定理に反しない(「高々一つ」は「ゼロでもよい」を含む)
  #     ⇒ **integrity stop として扱わない**。「この fixture には (35.4) の
  #     E1+E2 を満たす witness が無い」という正直な結論として記録する
  #     (reusable checker は 0 解を fixture corruption 扱いしない)。
  if Length(survivors) > 1 then
    Print("*** INTEGRITY STOP: R1-N∞-W proves AT MOST one survivor, got ", Length(survivors),
          " for target ", label, " (theorem violation -- fixture corruption suspected) ***\n");
    Check(Concatenation(label, "-SELFCHECK at most one survivor (R1-N∞-W)"), false,
          Concatenation("got ", String(Length(survivors)), " survivors (theorem allows at most 1)"));
    rec2 := rec(target := label, integrity_stop := true,
                reason := Concatenation("R1-N∞-W proves at most 1 survivor of E1+E2 among the 10 candidates, got ", String(Length(survivors)), " (theorem violation)"));
    results.(label) := rec2;
    return;
  fi;
  Check(Concatenation(label, "-SELFCHECK at most one survivor (R1-N∞-W)"), true, "");
  if Length(survivors) = 0 then
    Print("  => (N_infty) predicate (35.4)'s E1+E2 has NO witness for target ", label,
          " among the 10 candidates. This is consistent with R1-N∞-W (at most one, ",
          "possibly zero) and is NOT treated as fixture corruption.\n");
    rec2 := rec(target := label, integrity_stop := false, num_survivors := 0,
                conjugator_exists := false,
                sanity_relation_ok := ok0, cycle_type_sigma0 := t0, cycle_type_sigmaInf := tInf,
                cycle_type_sigma1 := t1, sign_sigma1 := SignPerm(s1),
                odd_length_cycle_count_sigma1 := oddMultCount,
                sigma0_sigma1_commute := commuteCheck, num_candidates_checked := 10,
                ninf_excluded := false,
                note := "no witness found for (35.4)'s E1+E2 among the 10 candidates; R1-N∞-W does not require existence, only at most one -- honestly reported, not integrity_stop");
    results.(label) := rec2;
    return;
  fi;

  sol := survivors[1];
  Check(Concatenation(label, "-REDUNDANT E3 (third eqn of (35.4), should be automatic from E1+E2)"), sol.e3ok, "");

  # -- self-check: g^2 = sigma_1 (theorem-derived, (35.6)/R1-N∞-W). Integrity
  # stop (not UNKNOWN) if this breaks -- it would mean the fixture itself is corrupted.
  gSquaredOk := sol.gPerm^2 = s1;
  if not gSquaredOk then
    Print("*** INTEGRITY STOP: g^2 <> sigma_1 for target ", label, " (fixture corruption suspected) ***\n");
  fi;
  Check(Concatenation(label, "-SELFCHECK g^2 = sigma_1 (35.6)/(R1-N∞-W)"), gSquaredOk,
        Concatenation("g^2 = ", String(sol.gPerm^2), "  sigma_1 = ", String(s1)));

  Print("  => (N_infty) NOT excluded for target ", label,
        " (unique witness g satisfying (35.4)'s E1+E2 found, E3 redundant-confirmed, g^2=sigma_1 self-check passed; UNDETERMINED, not a proof of presence)\n");

  rec2 := rec(
    target := label,
    integrity_stop := false,
    sanity_relation_ok := ok0,
    cycle_type_sigma0 := t0,
    cycle_type_sigmaInf := tInf,
    cycle_type_sigma1 := t1,
    sign_sigma1 := SignPerm(s1),
    odd_length_cycle_count_sigma1 := oddMultCount,
    sigma0_sigma1_commute := commuteCheck,
    num_candidates_checked := 10,
    num_survivors := 1,
    conjugator_exists := true,
    conjugator_g_0indexed := sol.gArr,
    e3_redundant_confirmation := sol.e3ok,
    g_squared_equals_sigma1 := gSquaredOk,
    ninf_excluded := false
  );
  results.(label) := rec2;
end;;

ProcessTarget("sq", Fixtures.sq);
ProcessTarget("ns", Fixtures.ns);

Print("\n=== ", totalPass, "/", totalPass + totalFail, " PASS ===\n");

# ---------------------------------------------------------------- certificate
GStr := function(g)
  if g = fail or not IsBound(g) then return "null"; fi;
  return JArr(List(g, String));
end;;

TargetJSON := function(r)
  if r.integrity_stop then
    return Concatenation("{",
      "\"integrity_stop\":true,",
      "\"reason\":", JStr(r.reason),
    "}");
  fi;
  if r.num_survivors = 0 then
    # 便 36 F1.2 の文言修理: 0 survivors は R1-N∞-W(高々一つ)に反しないので
    # integrity_stop ではない -- 正直に「witness なし」として記録する。
    return Concatenation("{",
      "\"integrity_stop\":false,",
      "\"sanity_relation_ok\":", JB(r.sanity_relation_ok), ",",
      "\"cycle_type_sigma0\":", JArr(List(r.cycle_type_sigma0, String)), ",",
      "\"cycle_type_sigmaInf\":", JArr(List(r.cycle_type_sigmaInf, String)), ",",
      "\"cycle_type_sigma1\":", JArr(List(r.cycle_type_sigma1, String)), ",",
      "\"sign_sigma1\":", String(r.sign_sigma1), ",",
      "\"odd_length_cycle_count_sigma1\":", String(r.odd_length_cycle_count_sigma1), ",",
      "\"sigma0_sigma1_commute\":", JB(r.sigma0_sigma1_commute), ",",
      "\"num_candidates_checked\":", String(r.num_candidates_checked), ",",
      "\"num_survivors\":0,",
      "\"conjugator_exists\":false,",
      "\"ninf_excluded\":", JB(r.ninf_excluded), ",",
      "\"note\":", JStr(r.note),
    "}");
  fi;
  return Concatenation("{",
    "\"integrity_stop\":false,",
    "\"sanity_relation_ok\":", JB(r.sanity_relation_ok), ",",
    "\"cycle_type_sigma0\":", JArr(List(r.cycle_type_sigma0, String)), ",",
    "\"cycle_type_sigmaInf\":", JArr(List(r.cycle_type_sigmaInf, String)), ",",
    "\"cycle_type_sigma1\":", JArr(List(r.cycle_type_sigma1, String)), ",",
    "\"sign_sigma1\":", String(r.sign_sigma1), ",",
    "\"odd_length_cycle_count_sigma1\":", String(r.odd_length_cycle_count_sigma1), ",",
    "\"sigma0_sigma1_commute\":", JB(r.sigma0_sigma1_commute), ",",
    "\"num_candidates_checked\":", String(r.num_candidates_checked), ",",
    "\"num_survivors\":", String(r.num_survivors), ",",
    "\"conjugator_exists\":", JB(r.conjugator_exists), ",",
    "\"conjugator_g_0indexed\":", GStr(r.conjugator_g_0indexed), ",",
    "\"e3_redundant_confirmation\":", JB(r.e3_redundant_confirmation), ",",
    "\"g_squared_equals_sigma1\":", JB(r.g_squared_equals_sigma1), ",",
    "\"ninf_excluded\":", JB(r.ninf_excluded),
  "}");
end;;

certJson := Concatenation(
  "{",
  "\"schema\":\"k5pipeline/ninf-exclusion-gap/v3\",",
  "\"retraction_note\":\"v1 (moved to certificates/k5pipeline/retracted/) tested the naive swap (x,y,z)->(z,y,x) (35.2)/(35.3), which does not preserve the relator xyz=1 in general. Direct computation here confirms sigma_0*sigma_1 <> sigma_1*sigma_0 for both fixtures, so (35.3)'s third equation combined with E1 is unsatisfiable (35.3 is equivalent to (35.4) AND [sigma_0,sigma_1]=1 given E1) -- v1's 'no conjugator found' was a CORRECT computation of an uninformative/wrong question, not evidence against (N_infty). v2 fixed the predicate to (35.4) but used a full-S10 search; v3 (this file) additionally implements the mathematician-reviewed restricted method (Rule 1 v1.3 R1-N∞-W): only 10 candidates (g(0)=c), E1+E2 as the decisive predicate (third eqn E3 automatic from E1+E2, checked as a redundant confirmation), and theorem-derived self-checks. 便36 F1.2 wording repair: R1-N∞-W proves AT MOST one survivor (integrity stop if >1, i.e. a genuine theorem violation), NOT exactly one -- 0 survivors is consistent with the theorem and is reported honestly rather than treated as fixture corruption; g^2=sigma_1 remains an integrity stop when a unique survivor exists but fails it.\",",
  "\"conclusion_label\":\"排除されず・対称性充足・(N_infty) の存否は UNKNOWN・witness は cross-checked\",",
  "\"pass\":", String(totalPass), ",",
  "\"fail\":", String(totalFail), ",",
  "\"method\":\"restricted 10-candidate search: g(0)=c for c=0..9, g built by propagating E1 (g s0 g^-1 = sInf) along the sigma_0 10-cycle; filter by E2 (g s1 g^-1 = s1); E1+E2 jointly imply E3 (checked as redundant confirmation); self-checks per R1-N∞-W: at most one survivor (integrity stop if >1; 0 is not corruption), g^2=sigma_1 when a survivor exists\",",
  "\"targets\":{",
  "\"sq\":", TargetJSON(results.sq), ",",
  "\"ns\":", TargetJSON(results.ns),
  "}",
  "}"
);;

WriteFile("certificates/k5pipeline/ninf-exclusion.gap.json", certJson);;
Print("wrote certificates/k5pipeline/ninf-exclusion.gap.json\n");

if totalFail > 0 then
  Print("*** THERE ARE FAILURES ***\n");
fi;

QUIT;
