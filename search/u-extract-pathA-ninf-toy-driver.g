#############################################################################
# search/u-extract-pathA-ninf-toy-driver.g -- R-5 (N_infty) 経路 A∞ 玩具較正・driver
# 委嘱: 便 36(裁定 36_ben35)。docs/week4-K5_Rule1_v1.md v1.2 S6.1(b)/補題 R1-B∞
# の実装拡張(search/u-extract-pathA.g の ExtractPathA_Ninf)を、Rule 1 S0.4-3
# が挙げる M=n=3 の玩具族で較正する。
#
# *** SYNTHETIC(合成の玩具例)であることを明記 ***
# K^(5) の実 fixture(K5-sq/K5-ns)には (N_infty) 型の dessin が無いため、
# 二経路一致の較正は Rule 1/便 35 が許す範囲の合成例でのみ行う。以下の
# A3, chat, f6, A, B は K^(5) の個別モデル・係数・数値近似では**ない**
# (種数 2 の一般的な六次モデル玩具族)。
#
# 玩具構成: A3(x) := x^3 + x + 1(モニック 3 次)、chat := 2、
#   f6 := A3(x)^2 - chat、B(x) := 1(定数、deg B = n-3 = 0)、
#   lambda := A3(x) + y。このとき N(lambda) = A3^2 - B^2 f6
#           = A3^2 - (A3^2 - chat) = chat = 2(定数、検算 N∞-3)、
#   deg A3 = n = 3、deg B = 0 = n-3、b_0 = 1 = a_3(検算 N∞-1/N∞-2)。
# f6 の平方非因子性(6 根が相異なる)は本便で Durand-Kerner 数値根探索により
# 事前確認済み(最小根間距離 ~0.80、scratchpad 確認・非公式)。
#
# 実行: .\gap.ps1 search\u-extract-pathA-ninf-toy-driver.g
#############################################################################

Read("search/u-extract-pathA.g");

# f6 = -1 + 2x + x^2 + 2x^3 + 2x^4 + 0x^5 + x^6 (ascending)
model := rec(
  id := "toy-ninf-M3",
  n := 3,
  f := [-1, 2, 1, 2, 2, 0, 1],
  A := [1, 1, 0, 1],     # A3(x) = x^3 + x + 1 (ascending: a0=1,a1=1,a2=0,a3=1)
  B := [1],              # B(x) = 1 (constant, deg = n-3 = 0)
  seriesLen := 20        # >= 2n+4 = 10; ample margin for exact rational arithmetic
);;

report := ExtractPathA_Ninf(model);;

Print("=== u-extract-pathA-ninf toy calibration (M=n=3, synthetic) ===\n");
Print("id = ", report.id, "\n");
Print("n = ", report.n, "\n");
Print("W^2 = F check: ", report.W_mod_check, "\n");
Print("lower_order_vanish ([s^0..s^{2n-1}] of G_- all zero): ", report.lowerOrderVanish, "\n");
Print("u_pathA_ninf = [s^{2n}] G_- = ", report.u_pathA_ninf, "\n");
Print("higher_order_raw (next 3 terms) = ", report.higherOrderRaw, "\n");

if not report.W_mod_check then
  Print("*** FAIL: W^2 <> F ***\n");
fi;
if not report.lowerOrderVanish then
  Print("*** FAIL: lower-order terms do not vanish (ord_{P0}(lambda) <> n) ***\n");
fi;

WriteFile("certificates/k5pipeline/toy-ninf-M3-pathA.json", ReportToJSON_Ninf(report));;
Print("wrote certificates/k5pipeline/toy-ninf-M3-pathA.json\n");

QUIT;
