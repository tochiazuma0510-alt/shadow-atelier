#############################################################################
# search/u-extract-pathA.g -- Rule 1 (docs/week4-K5_Rule1_v1.md) SS6.1 経路 A
# 委嘱: 便 32 P6 後半(司令塔発注)+ 便 34 blocker 2/3 修理(Sol 便 34 P6-E1/E2)。
#
# 身分(便 34 P6-E1 以降): 本ファイルは **library** である(関数定義のみ・
# 入力パラメトリック・QUIT なし・トップレベルの MODELS 実行なし)。
# K3 較正の実行は search/u-extract-pathA-k3-driver.g(薄い driver)が担う。
# 将来の K5 driver は本ファイルを Read して ExtractPathA(model) を呼ぶだけで
# よく、この library の凍結 digest は変わらない(model literal はすべて
# driver 側に置く)。
#
# 入力: model レコード (呼び出し元 driver が渡す。JSON パーサに依存しない --
#   数値は certificates/k5fixture/*-model.json の値を手動転記し、出力 JSON に
#   モデル係数を echo するので突合器 (crosscheck/u-compare.mjs) が JSON 側の
#   値と一致するか検査できる)。
#
# model レコードのフィールド:
#   id            : 文字列ラベル
#   M             : 次数 (6 or 10)
#   branchP0      : "nonWeierstrass" または "Weierstrass"
#   x0, y0        : P0 の座標(有理数)
#   f, A, B       : 昇冪係数リスト (f(x)=sum f[i+1]*x^i, 等)
#   seriesLen     : 保持する項数 (= M+4 を推奨。[t^{M+3}] まで検算可能)
#
# 出力: ExtractPathA(model) が report レコードを返す。driver が
#   ReportToJSON(report) で JSON 化し WriteFile で書き出す。
#
# 中間表現: K[[t]] (切断冪級数、GAP の有理数/CF(n) 元のリストとして表現)。
# SS6.3 の非共有 helper 要件: 本ファイルはべき級数演算のみを実装し、
# crosscheck/u-extract-pathB-lib.mjs (多項式係数評価・Taylor 係数のみ) とは
# 関数・データ構造を一切共有しない。
#
# 便 34 P6-E2 (blocker 3 前半): report に「入力モデルの canonical digest」を
# 埋め込む(model_digest フィールド)。canonical 化・sha256 の算出方法は
# crosscheck/u-extract-pathB-lib.mjs 側と**独立に**実装する(既存の
# search/e2c6-sweep.g ComputeSha256File と同じ Exec+sha256sum 方式を流用)。
# 突合(二 raw が同一モデル由来か)は crosscheck/u-compare.mjs が
# 埋め込み digest だけでなく全フィールドの再突合でも fail-closed に行う
# (blocker 3 前半の本体はそちら)。
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

#################### canonical model digest (便 34 P6-E2) ####################
# 罠回避: 一時ファイル名は id を含めて衝突を避ける(並行 driver 実行を想定)。
PathA_CanonicalModelString := function(model)
  local ratList, joinRat;
  joinRat := function(lst) return JoinC(List(lst, String), ","); end;;
  return Concatenation(
    "id=", model.id, ";",
    "M=", String(model.M), ";",
    "branchP0=", model.branchP0, ";",
    "x0=", String(model.x0), ";",
    "y0=", String(model.y0), ";",
    "f=[", joinRat(model.f), "];",
    "A=[", joinRat(model.A), "];",
    "B=[", joinRat(model.B), "]"
  );
end;;

PathA_ModelDigest := function(model)
  local s, tmp, f, line;
  s := PathA_CanonicalModelString(model);
  tmp := Concatenation("search/.tmp_model_digest_pathA_", model.id, ".txt");
  WriteFile(tmp, s);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", tmp, ".out\""));
  f := InputTextFile(Concatenation(tmp, ".out"));
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", tmp, ".out\""));
  return line{[1..64]};
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
    higherOrderRaw := List([model.M + 1 .. Minimum(n, model.M + 4)], k -> lambdaSeries[k]),
    modelDigest := PathA_ModelDigest(model),
    modelCanonicalString := PathA_CanonicalModelString(model)
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
    JStr("schema"), ":", JStr("u-pathA/v2"), ",",
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
    JStr("higher_order_raw"), ":", JRatList(r.higherOrderRaw), ",",
    JStr("model_digest"), ":", JStr(r.modelDigest), ",",
    JStr("model_digest_algo"), ":", JStr("sha256(canonical_model_string)"), ",",
    JStr("canonical_model_string"), ":", JStr(r.modelCanonicalString),
  "}");
end;;

# 本ファイルは library。実行(model 定義・driver・QUIT)は
# search/u-extract-pathA-k3-driver.g(K3 較正)/ 将来の K5 driver が担う。
