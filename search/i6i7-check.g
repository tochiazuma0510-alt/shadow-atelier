# search/i6i7-check.g -- I6/I7 の安価 2 項の機械確認(裁定117・n=9 前件 C3)
#
# 実行: .\gap.ps1 search\i6i7-check.g
#
# 正本: docs/notes/c2c4_closure_v1.md I6/I7 節(§3 の inventory 表)。
#   I6: 正典 Thm 4.3 (4.12)(docs/notes/抽出_Kn定義_D1.md §4)が
#       chi~: (m,f) |-> 2m+1 を GT(K^(n)) 上の写像として与える。未確認点は
#       m |-> 2m+1 の mod 2n(= K_ord、n 奇)での多重度(2 対 1 の可能性)。
#   I7: docs/week4-BFC攻略_opus_v2.md (6.1)(行412-417)「F_0 ≅ C_n, e=n,
#       M/e=2」の n=9 転記(|F_0|=9, e=9, M=18)を GAP で直接照合する。
#
# 実装: search/k9-package.g のタスク1(BuildPn/GT(K^(9)) 較正)をそのまま
#   n in {3,5,7,9,11} へ一般化する(BuildPn は既に n を引数に取る一般実装
#   -- k9-package.g からの無変更コピー)。EnumerateReducedHexagon で GT(K^(n))
#   を実際に列挙し、各 shadow (m,f) について chi~(m,f) := (2m+1) mod 2n を
#   直接計算して分布を集計する(観測のみ・解釈しない)。
#
# 宇宙: n in {3,5,7,9,11}(発注書の事前登録どおり。既存の family survey
#   (search/family-window-survey.g)と同一宇宙 -- 拡大縮小しない)。
#
# 規律: u・c 平方類・c_mu には触れない。解釈しない(数値のみを記録する)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

PF := function(b)
  if b then return "PASS"; else return "FAIL"; fi;
end;;

Print("############################################################\n");
Print("# i6i7-check.g -- I6 (chi~ 分布・多重度) + I7 (|F_0|=e=n 照合)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;

# ====================================================================
# BuildPn(n) -- search/k9-package.g からの無変更コピー(座標辞書つき P_n)。
# ====================================================================
BuildPn := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, q3, X, Y, Xchk, Ychk, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("BuildPn: D_n relations failed for n = ", n);
  fi;
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do
      l[j + (i-1)*n] := (j^p) + (i-1)*n;
    od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2) * tr(s,3);;
  q2 := tr(s,1) * tr(s,3);;
  q3 := tr(s,1) * tr(s,2);;
  X := AbstractProd([a1, q1]);;
  Y := AbstractProd([a1, a2, a3, q2]);;
  Xchk := tr(r,1) * tr(s,2) * tr(s,3);;
  Ychk := tr(s*r,1) * tr(r,2) * tr(s*r,3);;
  if X <> Xchk then
    Error("BuildPn: X = AbstractProd([a1,q1]) does not match MakeGn convention for n=", n);
  fi;
  if Y <> Ychk then
    Error("BuildPn: Y = AbstractProd([a1,a2,a3,q2]) does not match MakeGn convention for n=", n);
  fi;
  Gfull := Group(a1, a2, a3, q1, q2);;
  return rec(n:=n, a1:=a1, a2:=a2, a3:=a3, q1:=q1, q2:=q2, q3:=q3, X:=X, Y:=Y, G:=Gfull);
end;;

expectedSize := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

universe := [3, 5, 7, 9, 11];;
Print("宇宙 (事前登録どおり固定): ", universe, "\n");

resultsPerN := [];;
failures := 0;;

for n in universe do
  Print("\n============================================================\n");
  Print("# n = ", n, "\n");
  Print("============================================================\n");

  Pn := BuildPn(n);;
  sz := Size(Pn.G);;
  okSize := (sz = expectedSize(n));;
  Print("[", PF(okSize), "] |P_", n, "| = ", sz, " (期待 ", expectedSize(n), ")\n");
  if not okSize then failures := failures + 1; fi;

  Nord := Lcm(Order(Pn.X), Order(Pn.Y));;
  twoN := 2*n;;
  okNord := (Nord = twoN);;
  Print("[", PF(okNord), "] N_ord = lcm(ord X, ord Y) = ", Nord, " (期待 2n=", twoN, ")\n");
  if not okNord then failures := failures + 1; fi;

  phin := Length(Filtered([1..n], k -> Gcd(k,n)=1));;
  theoreticalGT := 2 * n * phin;;
  Print("理論値(Thm 4.3, n0=n, alpha=0): 2*n*phi(n) = 2*", n, "*", phin, " = ", theoreticalGT, "\n");

  charmingSet := Filtered([0..Nord-1], m -> Gcd(2*m+1, Nord) = 1);;
  Print("|X_", n, "| = ", Length(charmingSet), "  charming set = ", charmingSet, "\n");

  qrec := rec(x:=Pn.X, y:=Pn.Y, G:=Pn.G);;
  gtResult := EnumerateReducedHexagon(qrec, charmingSet);;

  Print("実測 |GT(K^(", n, "))| = ", gtResult.shadow_total, "\n");
  gtCalibPass := (gtResult.shadow_total = theoreticalGT);;
  Print("[", PF(gtCalibPass), "] GT(K^(", n, ")) 較正: 実測 = 理論値\n");
  if not gtCalibPass then failures := failures + 1; fi;

  # ---- I6: chi~(m,f) := (2m+1) mod 2n の分布(全 shadow・観測のみ) ----
  chiValues := List(gtResult.shadows, sh -> (2*sh.m + 1) mod twoN);;
  chiCollected := Collected(chiValues);;   # [[value, multiplicity], ...] value 昇順
  imageOrder := Length(chiCollected);;
  kernelMult := 0;;
  for pr in chiCollected do
    if pr[1] = 1 then kernelMult := pr[1] * 0 + pr[2]; fi;
  od;
  # 上の for は kernelMult に値 1 の多重度を代入する(見つからなければ 0 のまま)
  multSet := Set(List(chiCollected, pr -> pr[2]));;
  allEqualMult := (Length(multSet) = 1);;

  Print("chi~ の像の位数(mod 2n=", twoN, " での相異なる値の個数) = ", imageOrder, "\n");
  Print("chi~ の値ごとの多重度(値順): ", chiCollected, "\n");
  Print("多重度が全値で一定か: ", allEqualMult, "  (一定なら値=", multSet, ")\n");
  Print("chi~=1 (mod 2n) の多重度(= 素朴な kernel カウント) = ", kernelMult, "\n");

  # ---- I7: 正典 (6.1) 予測(e=n)との照合(素朴カウントとして) ----
  i7ExpectedE := n;;
  i7Match := (kernelMult = i7ExpectedE);;
  Print("[", PF(i7Match), "] I7 照合: chi~=1 多重度(", kernelMult, ") vs (6.1) 予測 e=n=", i7ExpectedE, "\n");

  Add(resultsPerN, rec(
    n := n,
    pn_size := sz, pn_size_expected := expectedSize(n), pn_size_pass := okSize,
    n_ord := Nord, n_ord_expected := twoN, n_ord_pass := okNord,
    theoretical_gt_size := theoreticalGT,
    charming_set := charmingSet,
    observed_gt_size := gtResult.shadow_total,
    gt_calibration_pass := gtCalibPass,
    chi_image_order := imageOrder,
    chi_value_multiplicities := chiCollected,
    chi_mult_all_equal := allEqualMult,
    chi_mult_all_equal_value := multSet,
    chi_kernel_mult_at_1 := kernelMult,
    i7_expected_e := i7ExpectedE,
    i7_match := i7Match
  ));
od;

# ====================================================================
# 総括表
# ====================================================================
Print("\n############################################################\n");
Print("# 総括表 (I6: chi~ 分布・I7: |F_0| 照合)\n");
Print("############################################################\n");
Print("n | |GT(K^n)| | chi~像位数 | 多重度一定? | chi~=1多重度 | (6.1)e=n | 一致\n");
for r in resultsPerN do
  Print(r.n, " | ", r.observed_gt_size, " | ", r.chi_image_order, " | ",
        r.chi_mult_all_equal, " | ", r.chi_kernel_mult_at_1, " | ",
        r.i7_expected_e, " | ", PF(r.i7_match), "\n");
od;

Print("\n############################################################\n");
if failures = 0 then
  Print("I6I7-CHECK ALL CALIBRATION GATES PASSED (I6/I7 自体は観測記録であり pass/fail 判定ではない)\n");
else
  Print("I6I7-CHECK CALIBRATION FAILURES: ", failures, "\n");
fi;

t1 := GAPLIB_WallElapsedMs();;
Print("経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_i6i7.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

MultsToJson := function(collected)
  local parts, pr;
  parts := [];
  for pr in collected do
    Add(parts, Concatenation("{\"value\":", String(pr[1]), ",\"mult\":", String(pr[2]), "}"));
  od;
  return JArr(parts);
end;;

PerNToJson := function(r)
  return Concatenation(
    "{\"n\":", String(r.n),
    ",\"pn_size\":", String(r.pn_size), ",\"pn_size_expected\":", String(r.pn_size_expected),
    ",\"pn_size_pass\":", JB(r.pn_size_pass),
    ",\"n_ord\":", String(r.n_ord), ",\"n_ord_expected\":", String(r.n_ord_expected),
    ",\"n_ord_pass\":", JB(r.n_ord_pass),
    ",\"theoretical_gt_size\":", String(r.theoretical_gt_size),
    ",\"charming_set\":", JArr(List(r.charming_set, String)),
    ",\"observed_gt_size\":", String(r.observed_gt_size),
    ",\"gt_calibration_pass\":", JB(r.gt_calibration_pass),
    ",\"chi_image_order\":", String(r.chi_image_order),
    ",\"chi_value_multiplicities\":", MultsToJson(r.chi_value_multiplicities),
    ",\"chi_mult_all_equal\":", JB(r.chi_mult_all_equal),
    ",\"chi_mult_all_equal_value\":", JArr(List(r.chi_mult_all_equal_value, String)),
    ",\"chi_kernel_mult_at_1\":", String(r.chi_kernel_mult_at_1),
    ",\"i7_expected_e\":", String(r.i7_expected_e),
    ",\"i7_match\":", JB(r.i7_match),
    "}"
  );
end;;

perNParts := [];;
for r in resultsPerN do
  Add(perNParts, PerNToJson(r));
od;

scriptSha256 := ComputeSha256File("search/i6i7-check.g");;

cert := Concatenation(
  "{\"schema\":\"i6i7-check/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/i6i7-check.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":[3,5,7,9,11]",
  ",\"note\":\"I6: chi~(m,f):=(2m+1) mod 2n の全 shadow に対する分布を観測(解釈しない)。",
   " I7: chi~=1 mod 2n の素朴カウントを docs/week4-BFC攻略_opus_v2.md (6.1) の e=n 予測と照合。",
   " chi~ 値は m のみに依存し f には依存しない(定義どおり)。\"",
  ",\"results\":[", JoinC(perNParts, ","), "]",
  ",\"overall_calibration_failures\":", String(failures),
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/i6i7_check_20260728.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");

Print("\nI6I7-CHECK DONE\n");
QUIT;
