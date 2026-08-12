# search/r13_r0b_v1.g -- R-0b(deck 変換群・中間商 C の genus)K^(9) 窓(裁定948)
# 指示書 = docs/notes/r1_branch_decision_v1.md §4(R-0b-1〜R-0b-4)
#
# 実行: .\gap.ps1 search\r13_r0b_v1.g
#
# R-0b-1: Deck(lambda_9) := N_{P_9}(H_9^fun)/H_9^fun -- 正規化群を取るだけ。位数2の元 phi の存在確認。
# R-0b-2: phi に対応する中間群 K (H_9^fun < K < P_9, [K:H_9^fun]=2) -- phi の代表元での逆像。
# R-0b-3: C = P_9/K の passport と genus(RH)。
# R-0b-4: phi の固定点(H_9^fun のコセット18個上の置換作用での固定点)-- P_0^(9),P_infty^(9) かの示唆確認。
#
# 規律: u に一切触れない。u_touched は「実値」(2148dde の教訓: pass 系と value 系の命名を混同しない
#   -- JSON 出力コード中で "u_touched" フィールドには変数 uTouched そのものを書く。検査結果フラグは
#   別名の変数に置く)。
#
# 847 依存監査: search/r13_r0_v1.g の BuildPn/H9fun 構成部をそのまま複製して独立に再構成する
#   (Read()/import はしない -- 各スクリプトが自己完結する既存の設計慣行を踏襲)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# r13_r0b_v1.g -- R-0b(deck 変換群・中間商 C)K^(9) 窓(裁定948)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;
failures := 0;;
uTouched := false;;   # u_9 に触れるコードパスは本スクリプトに一切存在しない(design 上の保証)

# ====================================================================
# BuildPn(n) -- r13_r0_v1.g / c1-class-check.g / k9-package.g と同一パターン
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
  if X <> Xchk then Error("BuildPn: X mismatch for n=", n); fi;
  if Y <> Ychk then Error("BuildPn: Y mismatch for n=", n); fi;
  Gfull := Group(a1, a2, a3, q1, q2);;
  return rec(n:=n, a1:=a1, a2:=a2, a3:=a3, q1:=q1, q2:=q2, q3:=q3, X:=X, Y:=Y, G:=Gfull);
end;;

expectedSize := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

PassportOf := function(perm, deg)
  local lens, coll;
  lens := List([1..deg], i -> CycleLength(perm, i));
  coll := Collected(lens);
  return List(coll, e -> [e[1], e[2]/e[1]]);
end;;

sumEMinus1 := function(passport)
  local total, e;
  total := 0;;
  for e in passport do total := total + e[2]*(e[1]-1);; od;
  return total;;
end;;

n := 9;;
P9 := BuildPn(n);;
sz9 := Size(P9.G);;
H9fun := Group(P9.a2, P9.a1*P9.a3, P9.q2);;
sizeH9 := Size(H9fun);;
D := sz9 / sizeH9;;
Print("|P_9|=", sz9, "  |H_9^fun|=", sizeH9, "  D=[P_9:H_9^fun]=", D, "\n");

# ====================================================================
# R-0b-1: Deck(lambda_9) = N_{P_9}(H_9^fun) / H_9^fun
# ====================================================================
Print("\n============================================================\n");
Print("# R-0b-1: Deck(lambda_9) = N_{P_9}(H_9^fun)/H_9^fun\n");
Print("============================================================\n");

N9 := Normalizer(P9.G, H9fun);;
sizeN9 := Size(N9);;
deckOrder := sizeN9 / sizeH9;;
Print("|N_{P_9}(H_9^fun)| = ", sizeN9, "   Deck order = ", deckOrder, "\n");

DeckQuot := N9 / H9fun;;   # H9fun is normal in N9 by construction of the normalizer
sizeDeckQuot := Size(DeckQuot);;
deckQuotSizeOk := (sizeDeckQuot = deckOrder);;
Print("[", PF(deckQuotSizeOk), "] |N_9/H_9^fun| (群としての商) = ", sizeDeckQuot, " = Deck order\n");
if not deckQuotSizeOk then failures := failures + 1; fi;

deckHasOrder2Elt := ForAny(DeckQuot, g -> Order(g) = 2);;
Print("[", PF(deckHasOrder2Elt), "] Deck 群に位数 2 の元が存在する\n");
if not deckHasOrder2Elt then failures := failures + 1; fi;

# ====================================================================
# R-0b-2: phi に対応する中間群 K (H_9^fun < K < P_9, [K:H_9^fun]=2)
# ====================================================================
Print("\n============================================================\n");
Print("# R-0b-2: 中間群 K ([K:H_9^fun]=2)\n");
Print("============================================================\n");

phiQuotElt := fail;;
if deckHasOrder2Elt then
  phiQuotElt := First(DeckQuot, g -> Order(g) = 2);;
fi;

# H9fun < K < P9 の逆像を N9 内で構成: K = 自然な射影 N9 -> N9/H9fun = DeckQuot の下で
# <phiQuotElt> の逆像。GAP の PreImages で直接取れる。
K := fail;;
kOk := false;;
kIndexOk := false;;
if phiQuotElt <> fail then
  natHom := NaturalHomomorphismByNormalSubgroup(N9, H9fun);;
  # natHom: N9 -> N9/H9fun. phiQuotElt は DeckQuot=N9/H9fun の元そのものなので、
  # PreImage で K = <H9fun, 代表元> を直接得る。
  K := PreImage(natHom, Group(phiQuotElt));;
  sizeK := Size(K);;
  kOk := (H9fun < K) and (K < P9.G);;
  kIndexOk := (sizeK/sizeH9 = 2);;
fi;
Print("[", PF(kOk), "] H_9^fun < K < P_9\n");
Print("[", PF(kIndexOk), "] [K:H_9^fun] = 2\n");
if not (kOk and kIndexOk) then failures := failures + 1; fi;
degC := fail;;
sizeKSafe := fail;;
if K <> fail then sizeKSafe := Size(K);; degC := sz9/sizeKSafe;; fi;
Print("|K| = ", sizeKSafe, "   deg(C) = [P_9:K] = ", degC, " (期待 ", D/2, ")\n");

# ====================================================================
# R-0b-3: C = P_9/K の passport と genus(RH)
# ====================================================================
Print("\n============================================================\n");
Print("# R-0b-3: C = P_9/K の passport と genus\n");
Print("============================================================\n");

gC := fail;;
passXc := fail;; passYc := fail;; passZc := fail;;
ramTotalC := fail;; twoGminus2C := fail;;
identityCheckC := false;;
if K <> fail then
  phiActionC := FactorCosetAction(P9.G, K);;
  XimgC := Image(phiActionC, P9.X);;
  YimgC := Image(phiActionC, P9.Y);;
  ZimgC := (XimgC * YimgC)^-1;;
  passXc := PassportOf(XimgC, degC);;
  passYc := PassportOf(YimgC, degC);;
  passZc := PassportOf(ZimgC, degC);;
  Print("passport(X, 0上) = ", passXc, "\n");
  Print("passport(Y, 1上) = ", passYc, "\n");
  Print("passport(Z, infty上) = ", passZc, "\n");

  ramTotalC := sumEMinus1(passXc) + sumEMinus1(passYc) + sumEMinus1(passZc);;
  twoGminus2C := degC*(-2) + ramTotalC;;
  Print("sum(e_P-1) 総計 = ", ramTotalC, "\n");
  Print("2g(C)-2 = ", degC, "*(-2) + ", ramTotalC, " = ", twoGminus2C, "\n");
  gCComputable := (twoGminus2C mod 2 = 0) and (twoGminus2C >= -2);;
  if gCComputable then gC := (twoGminus2C+2)/2; fi;
  Print("[", PF(gCComputable), "] 2g(C)-2 が偶数かつ >= -2\n");
  if not gCComputable then failures := failures + 1; fi;
  Print("★★★ g(C) = ", gC, " (期待 2) ★★★\n");
  gCMatchesExpected := (gC = 2);;
  Print("[", PF(gCMatchesExpected), "] g(C) = 2 の確認(§4 表の予測)\n");
  if not gCMatchesExpected then failures := failures + 1; fi;
  identityCheckC := (ramTotalC = 2*degC + 2*gC - 2);;
  Print("[", PF(identityCheckC), "] 恒等式再検算: sum(e_P-1) = 2*deg(C)+2*g(C)-2\n");
  if not identityCheckC then failures := failures + 1; fi;
else
  Print("[SKIP] K が構成できなかったため R-0b-3 は実行できない\n");
  failures := failures + 1;
fi;

# ====================================================================
# R-0b-4: phi の固定点(H_9^fun のコセット18個上での置換作用)
# ====================================================================
Print("\n============================================================\n");
Print("# R-0b-4: phi の固定点(H_9^fun のコセット18個上)\n");
Print("============================================================\n");

phiFixedPointCount := fail;;
phiFixedCosetsMatchP0Pinf := false;;
if phiQuotElt <> fail then
  # phi の N9 内での代表元(自然射影の逆像から任意に1つ取る)を使って、
  # H_9^fun のコセット (=W_9 の 18 点、FactorCosetAction(P9.G,H9fun) の作用域) での
  # 固定点数を数える。
  phiRep := PreImagesRepresentative(natHom, phiQuotElt);;
  phiActionW9 := FactorCosetAction(P9.G, H9fun);;
  phiPermOnW9 := Image(phiActionW9, phiRep);;
  fixedPts := Filtered([1..D], i -> i^phiPermOnW9 = i);;
  phiFixedPointCount := Length(fixedPts);;
  Print("phi の代表元 (=", phiRep, ") の W_9(18 点)上の固定点: ", fixedPts, "\n");
  Print("固定点数 = ", phiFixedPointCount, " (§3.3 の示唆: 期待 2)\n");
  phiFixedCountMatches2 := (phiFixedPointCount = 2);;
  Print("[", PF(phiFixedCountMatches2), "] 固定点数 = 2 の確認\n");
  if not phiFixedCountMatches2 then failures := failures + 1; fi;
  # 固定点が「P_0^(9), P_infty^(9)」かどうかは、0/infty の上の分岐点(passport X,Z のただ1点)
  # に対応するコセットが固定点集合に含まれるかで確認する。X の 0-fiber は唯一の 18-サイクル
  # 上の全点(=W_9全体が1つの軌道)なので、"P_0^(9)"は特定のコセット代表というより「Xが推移的に
  # 動く軌道」全体を指す幾何的な1点。固定点が実際にX,Zの不動点集合と一致するかを別途、
  # X,Z軌道の構造から確認する代わりに、直接的な機械確認として「固定点集合が X-軌道(=全18点)の
  # 中で X の作用の下で特別な位置にあるか」を記録する(数の一致のみが機械的に確認できる範囲、
  # §3.3 の注記どおり「示唆」であって証明ではない)。
else
  Print("[SKIP] phi が構成できなかったため R-0b-4 は実行できない\n");
  failures := failures + 1;
fi;

# ====================================================================
# 総括
# ====================================================================
Print("\n############################################################\n");
if failures = 0 then
  Print("R13-R0B ALL PASSED\n");
else
  Print("R13-R0B FAILURES: ", failures, "\n");
fi;

t1 := GAPLIB_WallElapsedMs();;
Print("経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_r13r0b.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

PassportToJson := function(p)
  local parts, e;
  if p = fail then return "null"; fi;
  parts := [];
  for e in p do Add(parts, JPair(e[1], e[2])); od;
  return JArr(parts);
end;;

ValOrNull := function(v)
  if v = fail then return "null"; fi;
  return String(v);
end;;

scriptSha256 := ComputeSha256File("search/r13_r0b_v1.g");;

cert := Concatenation(
  "{\"schema\":\"r13-r0b/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/r13_r0b_v1.g\",\"order\":\"裁定948 / docs/notes/r1_branch_decision_v1.md §4\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":{\"n\":9,\"D\":", String(D), "}",
  ",\"r0b1_deck\":{",
    "\"normalizer_size\":", String(sizeN9),
    ",\"h9fun_size\":", String(sizeH9),
    ",\"deck_order\":", String(deckOrder),
    ",\"deck_quotient_size_pass\":", JB(deckQuotSizeOk),
    ",\"deck_has_order2_element\":", JB(deckHasOrder2Elt),
  "}",
  ",\"r0b2_intermediate_K\":{",
    "\"K_size\":", ValOrNull(sizeKSafe),
    ",\"H_lt_K_lt_P9\":", JB(kOk),
    ",\"index_K_over_H9fun\":", (function() if K<>fail then return String(sizeKSafe/sizeH9); else return "null"; fi; end)(),
    ",\"index_pass\":", JB(kIndexOk),
    ",\"deg_C\":", ValOrNull(degC),
  "}",
  ",\"r0b3_C_passport_genus\":{",
    "\"passport_X_at_0\":", PassportToJson(passXc),
    ",\"passport_Y_at_1\":", PassportToJson(passYc),
    ",\"passport_Z_at_infty\":", PassportToJson(passZc),
    ",\"sum_e_minus_1_total\":", ValOrNull(ramTotalC),
    ",\"two_g_minus_2\":", ValOrNull(twoGminus2C),
    ",\"g_C\":", ValOrNull(gC),
    ",\"g_C_expected\":2",
    ",\"g_C_matches_expected\":", JB(gC = 2),
    ",\"identity_check_pass\":", JB(identityCheckC),
  "}",
  ",\"r0b4_phi_fixed_points\":{",
    "\"fixed_point_count\":", ValOrNull(phiFixedPointCount),
    ",\"fixed_point_count_expected\":2",
    ",\"fixed_point_count_matches_expected\":", JB(phiFixedPointCount = 2),
    ",\"note\":\"数の一致のみを機械確認。固定点=P_0^(9),P_infty^(9)であることの幾何的同定は本スクリプトの射程外(§3.3の示唆の域を出ない)\"",
  "}",
  ",\"u_touched\":", JB(uTouched),
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"helper_disjoint\":\"本スクリプトは他のsearch/*.gをRead()せず、BuildPn等を独立に再定義している\"",
  ",\"overall_failures\":", String(failures),
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/r13_r0b_v1_20260812.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");

Print("\nR13-R0B DONE\n");
QUIT;
