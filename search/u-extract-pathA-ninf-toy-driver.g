#############################################################################
# search/u-extract-pathA-ninf-toy-driver.g -- R-5 ライブラリ unit test(M=3, synthetic)
# 委嘱: 便 36(裁定_36_ben35 起草・裁定_37_ben36 で production 化を要求・便 36 F3.2)。
# docs/week4-K5_Rule1_v1.md v1.2 S6.1(b)/補題 R1-B∞ の実装(search/u-extract-
# pathA.g の ExtractPathA_Ninf, schema v3(裁定40/便39 F2 で v2→v3 へ破壊的 version bump))を、Rule 1 S0.4-3 の精神に沿う
# M=3 の小さい合成 fixture で叩く unit test。
#
# *** 位置づけ(便 36 F3.2 の裁定を反映・重要) ***
# 本ファイルは **R-5 の production 較正ではない**。ExtractPathA_Ninf ライブラリ
# 関数(schema v3(裁定40/便39 F2 で v2→v3 へ破壊的 version bump) の配線・(N∞-1)-(N∞-4) の fail-closed 検査・gcd(f,f')=1・
# 必要級数長・model digest 束縛)が「M=3 という小さい入力でも production と
# 同じコードパスで正しく動く」ことを確認する library unit test である。
# R-5 の production 較正(M=10・(N∞-1)-(N∞-4) 完走・Sol 提供 exact synthetic
# fixture)は search/u-extract-pathA-ninf-production-driver.g が別途行う
# (二経路一致・第三 checker への feed も production driver 側)。
#
# *** SYNTHETIC(合成の玩具例)であることを明記 ***
# K^(5) の実 fixture(K5-sq/K5-ns)には (N_infty) 型の dessin が無いため、
# 較正は Rule 1/便 35/便 36 が許す範囲の合成例でのみ行う。以下の A, B, f は
# K^(5) の個別モデル・係数・数値近似では**ない**(種数 2 の一般的な六次モデル
# 玩具族)。
#
# *** 便 36 F3.2 の修理注記 ***
# 旧版(便 36 起草時点)の玩具は f6 の定数項を -1 とし chat=2 だった。
# schema v3(裁定40/便39 F2 で v2→v3 へ破壊的 version bump) の ExtractPathA_Ninf は (N∞-4)(chat=1)を fail-closed に要求する
# ため、chat=2 の入力はもはやこの共有ライブラリを正常に通らない(意図的:
# chat=1 は補題 R1-N∞-S による K5 campaign 固有の定理であり、production
# schema はこれを常時検査する)。以下は定数項を 0 に変えただけ(それ以外の
# 係数は不変)で chat=1 に修正した新しい unit test 用の値。旧 chat=2 入力を
# 与えると (N∞-4) で GAP Error が発生することは
# crosscheck/check-r5-ninf-fail-closed.mjs(node 側 adversarial 較正)で
# 自動確認している。
#
# 玩具構成: A(x) := x^3 + x + 1(モニック 3 次)、B(x) := 1(定数、
#   deg B = M-3 = 0)、f(x) := A(x)^2 - 1(モニック 6 次)。このとき
#   N(lambda) = A^2 - B^2 f = A^2 - f = 1 = chat(検算 N∞-3/N∞-4)、
#   deg A = 3 = M、deg B = 0 = M-3、b_0 = 1 = a_3(検算 N∞-1/N∞-2)。
# gcd(f,f') が単元であること(f の平方非因子性)は本 driver 実行時に
# PolyGcdIsUnit で exact 検査される(事前に scratchpad でも確認済み:
# gcd(f,f') は次数 0 の非零有理数)。
#
# expectedModelDigest は本 driver がハードコードせず、独立に生成された凍結
# bundle ファイル certificates/k5pipeline/toy-ninf-M3-bundle.json
# (crosscheck/build-frozen-bundles.mjs -- pathA/pathB のどちらのコードとも
# 独立な第三実装)から読み取る(裁定 38/便 37 F2 修理 1)。この unit test では
# 「凍結 bundle の期待 digest」を模する synthetic bundle として扱う。
#
# 実行: .\gap.ps1 search\u-extract-pathA-ninf-toy-driver.g
#############################################################################

Read("search/u-extract-pathA.g");

bundleExpectedDigest := ReadJsonStringField("certificates/k5pipeline/toy-ninf-M3-bundle.json", "expected_model_digest");;
Print("expected_model_digest read from bundle file = ", bundleExpectedDigest, "\n");

model := rec(
  id := "toy-ninf-M3",
  branch := "N_infty",
  P0_type := "nonWeierstrass",
  M := 3,
  f := [0, 2, 1, 2, 2, 0, 1],    # f = x^3+x+1)^2 - 1 = x^6+2x^4+2x^3+x^2+2x
  A := [1, 1, 0, 1],             # A(x) = x^3 + x + 1 (ascending: a0=1,a1=1,a2=0,a3=1)
  B := [1],                     # B(x) = 1 (constant, deg = M-3 = 0)
  seriesLen := 20,               # >= 2M+4 = 10; ample margin for exact rational arithmetic
  expectedModelDigest := bundleExpectedDigest
);;

report := ExtractPathA_Ninf(model);;

Print("=== u-extract-pathA-ninf unit test (M=3, synthetic, schema v3(裁定40/便39 F2 で v2→v3 へ破壊的 version bump)) ===\n");
Print("id = ", report.id, "\n");
Print("branch = ", report.branch, "\n");
Print("M = ", report.M, "\n");
Print("deg_A_equals_M (N∞-1a) = ", report.degAEqualsM, "\n");
Print("deg_B_equals_Mminus3 (N∞-1b) = ", report.degBEqualsMminus3, "\n");
Print("b_Mm3_equals_a_M (N∞-2) = ", report.bMm3EqualsAM, "\n");
Print("gcd_f_fprime_is_unit = ", report.gcdFFprimeIsUnit, "\n");
Print("chat (N∞-3) = ", report.chat, "\n");
Print("chat_equals_1 (N∞-4) = ", report.chatEquals1, "\n");
Print("W^2 = F check: ", report.W_mod_check, "\n");
Print("lower_order_vanish ([s^0..s^{2M-1}] of G_- all zero): ", report.lowerOrderVanish, "\n");
Print("u_pathA_ninf = [s^{2M}] G_- = ", report.u_pathA_ninf, "\n");
Print("higher_order_raw (next 3 terms) = ", report.higherOrderRaw, "\n");
Print("model_digest = ", report.modelDigest, "\n");
Print("expected_model_digest = ", report.expectedModelDigest, "\n");
Print("digest_match = ", report.modelDigest = report.expectedModelDigest, "\n");

if not report.W_mod_check then
  Print("*** FAIL: W^2 <> F ***\n");
fi;
if not report.lowerOrderVanish then
  Print("*** FAIL: lower-order terms do not vanish (ord_{P0}(lambda) <> M) ***\n");
fi;
if report.modelDigest <> report.expectedModelDigest then
  Print("*** FAIL: model_digest <> expectedModelDigest ***\n");
fi;

WriteFile("certificates/k5pipeline/toy-ninf-M3-pathA.json", ReportToJSON_Ninf(report));;
Print("wrote certificates/k5pipeline/toy-ninf-M3-pathA.json\n");

QUIT;
