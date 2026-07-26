#############################################################################
# search/u-extract-pathA.g -- Rule 1 (docs/week4-K5_Rule1_v1.md) SS6.1 経路 A
# 委嘱: 便 32 P6 後半(司令塔発注)。M パラメトリック実装 --
#   K^(3) (M=6, K=Q(zeta_12)) と K^(5) (M=10, K=Q(zeta_20)) の両方をこの
#   1 本の関数 ExtractPathA(model) が処理する(model レコードを変えるだけ)。
#
# 入力: model レコード (このファイル下部の MODELS 一覧・GAP 内リテラル。
#   JSON パーサに依存しない -- 数値は certificates/k5fixture/*-model.json
#   の値を手動転記し、出力 JSON にモデル係数を echo するので突合器
#   (crosscheck/u-compare.mjs) が JSON 側の値と一致するか検査できる)。
#
# model レコードのフィールド:
#   id            : 文字列ラベル
#   M             : 次数 (6 or 10)
#   branchP0      : "nonWeierstrass" または "Weierstrass"
#   x0, y0        : P0 の座標(有理数)
#   f, A, B       : 昇冪係数リスト (f(x)=sum f[i+1]*x^i, 等)
#   seriesLen     : 保持する項数 (= M+4 を推奨。[t^{M+3}] まで検算可能)
#
# 出力: 呼び出し元が WriteFile で certificates/k5fixture/<id>-u-pathA.json
#   へ書く(このファイル自身は実行時に対象 model 群を回して書き出す)。
#
# 中間表現: K[[t]] (切断冪級数、GAP の有理数/CF(n) 元のリストとして表現)。
# SS6.3 の非共有 helper 要件: 本ファイルはべき級数演算のみを実装し、
# crosscheck/u-extract-pathB.mjs (多項式係数評価・Taylor 係数のみ) とは
# 関数・データ構造を一切共有しない。
#############################################################################

Read("search/gaplib_common.g");

#################### べき級数(切断)ヘルパー ####################
# 表現: length n のリスト、インデックス i (1-indexed) が t^{i-1} の係数。

PSZero := function(n) return List([1..n], i -> 0); end;;

PSFromScalar := function(c, n)
  local r;
  r := PSZero(n);
  r[1] := c;
  return r;
end;;

PSAdd := function(a, b)
  return List([1..Length(a)], i -> a[i] + b[i]);
end;;

PSSub := function(a, b)
  return List([1..Length(a)], i -> a[i] - b[i]);
end;;

PSScale := function(a, c)
  return List(a, x -> x * c);
end;;

# 畳み込み(切断)
PSMul := function(a, b)
  local n, r, i, j;
  n := Length(a);
  r := PSZero(n);
  for i in [1..n] do
    if a[i] <> 0 then
      for j in [1..n - i + 1] do
        if b[j] <> 0 then
          r[i + j - 1] := r[i + j - 1] + a[i] * b[j];
        fi;
      od;
    fi;
  od;
  return r;
end;;

# 形式的逆元(a[1] <> 0 が必須)
PSInverse := function(a)
  local n, b, k, s, j;
  n := Length(a);
  if a[1] = 0 then
    Error("PSInverse: constant term is zero");
  fi;
  b := PSZero(n);
  b[1] := 1 / a[1];
  for k in [2..n] do
    s := 0;
    for j in [2..k] do
      s := s + a[j] * b[k - j + 1];
    od;
    b[k] := -s / a[1];
  od;
  return b;
end;;

# Horner 法によるべき級数への多項式代入: coeffsAsc(昇冪) を xSeries に代入
PSEvalPoly := function(coeffsAsc, xSeries, n)
  local deg, result, i;
  deg := Length(coeffsAsc) - 1;
  result := PSFromScalar(coeffsAsc[deg + 1], n);
  for i in [deg, deg - 1 .. 1] do
    result := PSAdd(PSMul(result, xSeries), PSFromScalar(coeffsAsc[i], n));
  od;
  return result;
end;;

# 多項式の(昇冪係数リストでの)形式微分
PolyDeriv := function(coeffsAsc)
  local deg, r, i;
  deg := Length(coeffsAsc) - 1;
  if deg = 0 then return [0]; fi;
  r := [];
  for i in [1..deg] do
    r[i] := i * coeffsAsc[i + 1];
  od;
  return r;
end;;

# Newton 法による形式冪級数の平方根: g[1] <> 0, 初期値 y0 (符号は g[1]=y0^2 と
# 整合するものを呼び出し側が渡す)
PSSqrt := function(g, y0, n)
  local y, iter, nIter;
  y := PSFromScalar(y0, n);
  nIter := 0;
  while 2^nIter < n do nIter := nIter + 1; od;
  for iter in [1 .. nIter + 3] do
    y := PSScale(PSAdd(y, PSMul(g, PSInverse(y))), 1/2);
  od;
  return y;
end;;

#################### 経路 A 本体 ####################
# model.branchP0 = "nonWeierstrass": t = x - x0, x(t) = x0 + t (自明),
#   y(t) = PSSqrt(f(x(t)), y0, n).
# model.branchP0 = "Weierstrass": t = y, x(t) を f(x(t)) = t^2 の
#   Hensel/Newton 持ち上げで解く(f(x0)=0, f'(x0) <> 0 が前提)。

ExtractPathA := function(model)
  local n, xSeries, ySeries, fprimeAsc, tSquared, xcur, iter, nIter,
        fx, fpx, num, lambdaSeries, k, lowerZero, report, u, extras;

  n := model.seriesLen;

  if model.branchP0 = "nonWeierstrass" then
    xSeries := PSFromScalar(model.x0, n);
    xSeries[2] := xSeries[2] + 1;               # x(t) = x0 + t
    ySeries := PSSqrt(PSEvalPoly(model.f, xSeries, n), model.y0, n);

  elif model.branchP0 = "Weierstrass" then
    fprimeAsc := PolyDeriv(model.f);
    xcur := PSFromScalar(model.x0, n);
    nIter := 0;
    while 2^nIter < n do nIter := nIter + 1; od;
    tSquared := PSZero(n);
    tSquared[3] := 1;                            # t^2 項 (index 3 = t^{2})
    for iter in [1 .. nIter + 3] do
      fx := PSEvalPoly(model.f, xcur, n);
      fpx := PSEvalPoly(fprimeAsc, xcur, n);
      num := PSSub(fx, tSquared);                # f(x) - t^2
      xcur := PSSub(xcur, PSMul(num, PSInverse(fpx)));
    od;
    xSeries := xcur;
    ySeries := PSZero(n);
    ySeries[2] := 1;                              # y(t) = t (自明恒等)

  else
    Error("ExtractPathA: unknown branchP0 ", model.branchP0);
  fi;

  # 曲線方程式 y^2 = f(x) の切断検算(モデル整合性)
  lambdaSeries := PSSub(PSMul(ySeries, ySeries), PSEvalPoly(model.f, xSeries, n));
  extras := rec(curveResidualZero := ForAll(lambdaSeries, c -> c = 0));

  # lambda = A(x) + B(x) y
  lambdaSeries := PSAdd(PSEvalPoly(model.A, xSeries, n), PSMul(PSEvalPoly(model.B, xSeries, n), ySeries));

  lowerZero := true;
  for k in [1 .. model.M] do
    if lambdaSeries[k] <> 0 then lowerZero := false; fi;
  od;

  u := lambdaSeries[model.M + 1];

  report := rec(
    id := model.id,
    M := model.M,
    branchP0 := model.branchP0,
    x0 := model.x0,
    y0 := model.y0,
    f := model.f,
    A := model.A,
    B := model.B,
    seriesLen := n,
    curveResidualZero := extras.curveResidualZero,
    lowerOrderVanish := lowerZero,
    u_pathA := u,
    higherOrderRaw := List([model.M + 1 .. Minimum(n, model.M + 4)], k -> lambdaSeries[k])
  );
  return report;
end;;

#################### JSON 直列化(有理数専用。cyclotomic は将来拡張) ####################
JRat := function(q)
  if not IsRat(q) then
    Error("JRat: non-rational value encountered (K5 実データでは CF(n) 直列化を別途拡張すること)");
  fi;
  return JStr(String(q));
end;;

JRatList := function(lst) return JArr(List(lst, JRat)); end;;

ReportToJSON := function(r)
  return Concatenation("{",
    JStr("schema"), ":", JStr("u-pathA/v1"), ",",
    JStr("id"), ":", JStr(r.id), ",",
    JStr("M"), ":", String(r.M), ",",
    JStr("branchP0"), ":", JStr(r.branchP0), ",",
    JStr("x0"), ":", JRat(r.x0), ",",
    JStr("y0"), ":", JRat(r.y0), ",",
    JStr("f_coeffs_ascending"), ":", JRatList(r.f), ",",
    JStr("A_coeffs_ascending"), ":", JRatList(r.A), ",",
    JStr("B_coeffs_ascending"), ":", JRatList(r.B), ",",
    JStr("series_length"), ":", String(r.seriesLen), ",",
    JStr("curve_residual_zero"), ":", JB(r.curveResidualZero), ",",
    JStr("lower_order_vanish"), ":", JB(r.lowerOrderVanish), ",",
    JStr("u_pathA"), ":", JRat(r.u_pathA), ",",
    JStr("higher_order_raw"), ":", JRatList(r.higherOrderRaw),
  "}");
end;;

#################### モデル群 ####################
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
if not IsBoundGlobal("U_PATHA_ONLY_LOAD") then
  for m in MODELS do
    r := ExtractPathA(m);
    Print("== ", r.id, " ==\n");
    Print("  u_pathA = ", r.u_pathA, "  lowerOrderVanish=", r.lowerOrderVanish,
          "  curveResidualZero=", r.curveResidualZero, "\n");
    WriteFile(Concatenation("certificates/k5fixture/", r.id, "-u-pathA.json"), ReportToJSON(r));
  od;
fi;

QUIT;
