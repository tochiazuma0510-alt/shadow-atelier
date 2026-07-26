#############################################################################
# search/u-extract-pathA-k3-driver.g -- 経路 A・K3 較正用の薄い driver
# 委嘱: 便 34 blocker 2 (Sol 便 34 P6-E1)。
#
# 身分: 本ファイルは driver である。アルゴリズム本体(ExtractPathA 等)は
# search/u-extract-pathA.g(library・凍結対象)から Read するだけで、model
# literal と実行・QUIT はすべてここに置く。将来の K5 driver は本ファイルと
# 同じ形(Read library -> model 定義 -> ExtractPathA 呼び出し -> WriteFile)
# を新しい driver ファイルとして追加すればよく、library 側の digest は
# 変更しない。
#
# 出力: certificates/k5pipeline/<id>-u-pathA.json
#############################################################################

Read("search/u-extract-pathA.g");

#################### モデル群(K3 較正専用) ####################
# K3-regression (certificates/k5fixture/K3-regression-model.json と手動照合済み)
K3Model := rec(
  id := "K3-regression",
  M := 6,
  branchP0 := "nonWeierstrass",
  x0 := 0,
  y0 := 1,
  f := [1, -12, 54, -116, 129, -72],
  A := [-1/2, 3, -9/2, 2],
  B := [1/2],
  seriesLen := 10
);;

# COV-1 (s -> cs 較正・M2 残余群作用 x -> k^2 x, y -> k^5 y, k=2 を適用した
# 派生モデル。u -> u*k^{-2M} となるはず -- SS5.4 観測 R1-C の実地検算)
K3Model_cov1_k2 := function()
  local k, f2, A2, B2, i;
  k := 2;
  f2 := List([1..Length(K3Model.f)], i -> K3Model.f[i] * k^(10 - 2*(i-1)));
  A2 := List([1..Length(K3Model.A)], i -> K3Model.A[i] / k^(2*(i-1)));
  B2 := List([1..Length(K3Model.B)], i -> K3Model.B[i] / k^(2*(i-1) + 5));
  return rec(
    id := "K3-regression-cov1-k2",
    M := 6,
    branchP0 := "nonWeierstrass",
    x0 := 0,
    y0 := k^5 * K3Model.y0,
    f := f2,
    A := A2,
    B := B2,
    seriesLen := 10
  );
end;;

MODELS := [ K3Model, K3Model_cov1_k2() ];;

#################### 実行 ####################
for m in MODELS do
  r := ExtractPathA(m);
  Print("== ", r.id, " ==\n");
  Print("  u_pathA = ", r.u_pathA, "  lowerOrderVanish=", r.lowerOrderVanish,
        "  curveResidualZero=", r.curveResidualZero, "\n");
  Print("  model_digest = ", r.modelDigest, "\n");
  WriteFile(Concatenation("certificates/k5pipeline/", r.id, "-u-pathA.json"), ReportToJSON(r));
od;

QUIT;
