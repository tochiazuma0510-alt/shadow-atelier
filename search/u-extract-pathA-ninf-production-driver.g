#############################################################################
# search/u-extract-pathA-ninf-production-driver.g -- R-5 production 較正(M=10, synthetic)
# 委嘱: 便 36 F3.2/F6-1(裁定_37_ben36 の最小条件 1)。Sol 提供の exact synthetic
# fixture で ExtractPathA_Ninf(search/u-extract-pathA.g・schema v2)を
# production-degree で叩き、(N∞-1)-(N∞-4)・deg A=10・gcd(f,f')=1・model digest
# 束縛のすべてを一つの走行で通す。
#
# *** SYNTHETIC(合成の較正例)であることを明記(便 36 F3.2 の言明) ***
# 「実 K5 の (N_infty) モデルがまだ無い」ことを延期の理由にしないため、Sol が
# 提示した候補へ**接触しない**合成 unit fixture でこの production 経路を
# 事前に固定する。以下の p, a, f, A, B は K^(5) の Belyi 候補・係数・数値近似
# では**ない**(封印前の合成 unit fixture)。
#
# 構成(便 36 F3.2 の式そのまま): p := x^2+1、a := 1+x(x^2+1)^2、
#   f := 2x+x^2(x^2+1)^2 = x^6+2x^4+x^2+2x。このとき a^2-fp^2 = 1(=: chat_mu、
#   mu の norm 定数)、gcd(f,f') = 1(f は平方非因子)。y^2=f、mu=a+p*y、
#   lambda = mu^2 = A+B*y とすると
#     A = 2a^2-1、B = 2ap、
#   deg A = 10、deg B = 7、b_7 = a_10 = 2、A^2-B^2 f = 1(=: chat)。
#
# A, B は本 driver が a, p, f から ExactPolyMul/ExactPolySub/ExactPolyScale で
# **その場で導出する**(手転記でなく計算で作る -- 手動転記による誤記の余地を
# 減らす。node 側の照合器・production driver も同じ p, a, f の定義から
# 独立に A, B を再計算する)。
#
# expectedModelDigest は本 driver がハードコードせず、独立に生成された凍結
# bundle ファイル certificates/k5pipeline/prod-ninf-M10-bundle.json
# (crosscheck/build-frozen-bundles.mjs -- pathA/pathB のどちらのコードとも
# 独立な第三実装)から読み取る(裁定 38/便 37 F2 修理 1: 「driver が凍結
# bundle の canonical model JSON を読むこと」)。実 K5 では Freeze 2 が注入
# する値のスタンドイン。
#
# 実行: .\gap.ps1 search\u-extract-pathA-ninf-production-driver.g
#############################################################################

Read("search/u-extract-pathA.g");

p := [1, 0, 1];;              # p(x) = 1 + x^2
a := [1, 1, 0, 2, 0, 1];;     # a(x) = 1 + x(x^2+1)^2 = 1 + x + 2x^3 + x^5
xpoly := [0, 1];;             # x, ascending

# f := 2x + x^2*(x^2+1)^2, computed exactly (not hand-transcribed) from p.
# (search/u-extract-pathA.g has no ExactPolyAdd -- reuse ExactPolySub with a
#  negated second argument, which is exactly as independent/exact.)
NegList := function(l) return List(l, x -> -x); end;;
ExactPolyAdd := function(u, v) return ExactPolySub(u, NegList(v)); end;;

f := ExactPolyTrim(ExactPolyAdd(
       ExactPolyScale(xpoly, 2),                       # 2x
       ExactPolyMul(ExactPolyMul(xpoly, xpoly), ExactPolyMul(p, p))  # x^2 * p^2
     ));;

# sanity check (mu-side norm constant, independent of the (N∞-3)/(N∞-4)
# check inside ExtractPathA_Ninf which is about A,B,f not a,p,mu):
chatMu := ExactPolyTrim(ExactPolySub(ExactPolyMul(a, a), ExactPolyMul(f, ExactPolyMul(p, p))));;
if Length(chatMu) <> 1 or chatMu[1] <> 1 then
  Error("production driver: a^2 - f*p^2 must be the constant 1 (mu-side norm), got ", chatMu);
fi;
Print("sanity check a^2-f*p^2 = ", chatMu, " (expect [1])\n");

# lambda = mu^2 = (a+p y)^2 = (a^2+p^2 f) + 2ap y =: A + B y
A := ExactPolyTrim(ExactPolySub(ExactPolyScale(ExactPolyMul(a, a), 2), [1]));;   # 2a^2-1
B := ExactPolyTrim(ExactPolyScale(ExactPolyMul(a, p), 2));;                      # 2ap

Print("derived A (ascending) = ", A, " deg = ", Length(A) - 1, "\n");
Print("derived B (ascending) = ", B, " deg = ", Length(B) - 1, "\n");
Print("f (ascending) = ", f, " deg = ", Length(f) - 1, "\n");

bundleExpectedDigest := ReadJsonStringField("certificates/k5pipeline/prod-ninf-M10-bundle.json", "expected_model_digest");;
Print("expected_model_digest read from bundle file = ", bundleExpectedDigest, "\n");

model := rec(
  id := "prod-ninf-M10",
  branch := "N_infty",
  P0_type := "nonWeierstrass",
  M := 10,
  f := f,
  A := A,
  B := B,
  seriesLen := 30,     # >= 2M+4 = 24; margin for exact rational arithmetic
  expectedModelDigest := bundleExpectedDigest
);;

report := ExtractPathA_Ninf(model);;

Print("\n=== u-extract-pathA-ninf PRODUCTION calibration (M=10, synthetic, schema v2) ===\n");
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

WriteFile("certificates/k5pipeline/prod-ninf-M10-pathA.json", ReportToJSON_Ninf(report));;
Print("wrote certificates/k5pipeline/prod-ninf-M10-pathA.json\n");

QUIT;
