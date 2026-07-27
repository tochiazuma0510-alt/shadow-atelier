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
# model レコードのフィールド(便 37 F3/裁定 38 で branch/P0_type を分離):
#   id            : 文字列ラベル
#   M             : 次数 (6 or 10)
#   branch        : 大域枝 "W" または "N_aff"(M0 の三値 {W,N_aff,N_infty}
#                   のうち、x0,y0 を持つこのスキーマでは N_infty は不正)
#   P0_type       : 局所 P0 の Weierstrass 性 "nonWeierstrass" または "Weierstrass"
#                   (branch='W' のときは 'nonWeierstrass' でなければならない --
#                   S5-W 補題 / Rule 1 SS4.1「v1.2 の絞り込み」)
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

#################### 厳密多項式演算(打ち切りなし・R-5 production 化) ####################
# べき級数(PSMul 等・seriesLen で打ち切り)とは別に、(N∞-1)-(N∞-4) の構造検査
# 自体は「打ち切りのない」正確な多項式演算でなければならない(seriesLen が
# 足りないと高次係数が消えて見えるだけの偽陰性があり得るため)。以下は昇冪係数
# リスト上の完全な(打ち切りなし)多項式演算。

ExactPolyMul := function(a, b)
  local r, i, j;
  r := List([1 .. Length(a) + Length(b) - 1], i -> 0);
  for i in [1 .. Length(a)] do
    if a[i] <> 0 then
      for j in [1 .. Length(b)] do
        if b[j] <> 0 then
          r[i + j - 1] := r[i + j - 1] + a[i] * b[j];
        fi;
      od;
    fi;
  od;
  return r;
end;;

ExactPolySub := function(a, b)
  local n, r, i;
  n := Maximum(Length(a), Length(b));
  r := [];
  for i in [1 .. n] do
    r[i] := 0;
    if i <= Length(a) then r[i] := r[i] + a[i]; fi;
    if i <= Length(b) then r[i] := r[i] - b[i]; fi;
  od;
  return r;
end;;

ExactPolyScale := function(a, c) return List(a, x -> x * c); end;;

# trim trailing (high-order) zero coefficients (ascending list)
ExactPolyTrim := function(a)
  local r;
  r := ShallowCopy(a);
  while Length(r) > 1 and r[Length(r)] = 0 do
    Remove(r, Length(r));
  od;
  return r;
end;;

# gcd(f, f') が定数(単元)かどうか -- f の平方非因子性の exact 検査。
# GAP の一変数多項式環上の Gcd を使う(PSMul/PSInverse とは独立の経路)。
PolyGcdIsUnit := function(coeffsAsc)
  local x, p, i, fprime, g, gdeg;
  x := Indeterminate(Rationals, "x_gcdcheck");
  p := Zero(Rationals);
  for i in [Length(coeffsAsc), Length(coeffsAsc) - 1 .. 1] do
    p := p * x + coeffsAsc[i];
  od;
  fprime := Derivative(p);
  g := Gcd(p, fprime);
  if IsZero(g) then
    return false; # f and f' both zero (degenerate) -- not a unit
  fi;
  gdeg := DegreeOfUnivariateLaurentPolynomial(g);
  return gdeg = 0;
end;;

#################### canonical model digest (便 34 P6-E2) ####################
# 罠回避: 一時ファイル名は id を含めて衝突を避ける(並行 driver 実行を想定)。
PathA_CanonicalModelString := function(model)
  local ratList, joinRat;
  joinRat := function(lst) return JoinC(List(lst, String), ","); end;;
  return Concatenation(
    "id=", model.id, ";",
    "M=", String(model.M), ";",
    "branch=", model.branch, ";",
    "P0_type=", model.P0_type, ";",
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
# model.P0_type = "nonWeierstrass": t = x - x0, x(t) = x0 + t (自明),
#   y(t) = PSSqrt(f(x(t)), y0, n).
# model.P0_type = "Weierstrass": t = y, x(t) を f(x(t)) = t^2 の
#   Hensel/Newton 持ち上げで解く(f(x0)=0, f'(x0) <> 0 が前提)。
#
# 便 37 F3/裁定 38(R-8 修理): model.branch(大域枝 {W,N_aff})と model.P0_type
# (局所 Weierstrass 性)を fail-closed に検査する。未知/欠落ラベルは既定値へ
# 丸めず即 Error(I-m)。branch='W' は P0_type='nonWeierstrass' を要求する
# (S5-W 補題)。

GLOBAL_BRANCH_ENUM := ["W", "N_aff"];;
P0_TYPE_ENUM := ["Weierstrass", "nonWeierstrass"];;

ExtractPathA := function(model)
  local n, xSeries, ySeries, fprimeAsc, tSquared, xcur, iter, nIter,
        fx, fpx, num, lambdaSeries, k, lowerZero, report, u, extras;

  if not IsBound(model.branch) or not (model.branch in GLOBAL_BRANCH_ENUM) then
    Error("ExtractPathA (I-m): model.branch must be one of ", GLOBAL_BRANCH_ENUM,
          ", got ", model.branch, " (N_infty must use ExtractPathA_Ninf, not this schema)");
  fi;
  if not IsBound(model.P0_type) or not (model.P0_type in P0_TYPE_ENUM) then
    Error("ExtractPathA (I-m): model.P0_type must be one of ", P0_TYPE_ENUM,
          ", got ", model.P0_type);
  fi;
  if model.branch = "W" and model.P0_type <> "nonWeierstrass" then
    Error("ExtractPathA (I-m): branch='W' requires P0_type='nonWeierstrass' (Lemma S5-W), got ",
          model.P0_type);
  fi;

  n := model.seriesLen;

  if model.P0_type = "nonWeierstrass" then
    xSeries := PSFromScalar(model.x0, n);
    xSeries[2] := xSeries[2] + 1;               # x(t) = x0 + t
    ySeries := PSSqrt(PSEvalPoly(model.f, xSeries, n), model.y0, n);

  elif model.P0_type = "Weierstrass" then
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
    Error("ExtractPathA: unknown P0_type ", model.P0_type);
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
    branch := model.branch,
    P0_type := model.P0_type,
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

#################### R-5(便 36・裁定 37): 副枝 (N_infty) 経路 A∞(production 化) ####################
# 委嘱: docs/week4-K5_Rule1_v1.md v1.2 S6.1 (b) / 補題 R1-B∞ + 便 36 F3.2/F6-1
# (Sol 提供の M=10, chat=1 exact synthetic fixture)。
#
# 身分: 本関数は M=3 の玩具(unit test)にも M=10 の production 較正
# (search/u-extract-pathA-ninf-production-driver.g)にも同じライブラリコードを
# 使う -- どちらも K^(5) の実 fixture ではない(K^(5) には (N_infty) 型の
# dessin がまだ無い)。単体試験(M=3)と production 較正(M=10・chat=1・
# (N∞-1)-(N∞-4) 完走)の位置づけの違いは呼び出し側 driver のコメントで区別する。
#
# schema v3(便 36 F3.2 (3) の修理・裁定40/便39 F2 で v2→v3 へ破壊的 version
# bump -- 必須 field P0Type/aM/bMm3 を欠く旧 v2 raw は retracted/ へ退避):
# 三値 branch label(model.branch は必ず
# "N_infty" 文字列)・model.M(旧 model.n を置換 -- Rule 1 の M と揃える)・
# model_digest・expected_model_digest を持つ。x0, y0 は存在しない(§6.3-6)。
#
# model_ninf レコードのフィールド:
#   id                    : 文字列ラベル
#   branch                : 文字列 "N_infty"(fail-closed 突合。§9.2 I-m)
#   M                     : 被覆の位数(div(lambda) = M P0 - M P_infty)
#   f                     : 昇冪係数リスト、次数 6(モニック、種数 2 の六次モデル)
#   A, B                  : 昇冪係数リスト(deg A = M、deg B = M-3 を要求)
#   seriesLen             : 保持する項数(>= 2M+4 を要求。不足は fail-closed)
#   expectedModelDigest   : 凍結 bundle が宣言する期待 digest(較正では driver が
#                           hand-transcribe した synthetic の期待値。実 K5 では
#                           Freeze 2 が注入する — 便 36 F3.2 (3)/R-7)
#
# (N∞-1)-(N∞-4) の構造検査(すべて exact 多項式演算・fail-closed。§6.2):
#   (N∞-1) deg A = M かつ deg B = M-3
#   (N∞-2) b_{M-3} = a_M かつ a_M <> 0
#   (N∞-3) A^2-B^2 f が定数 chat <> 0(次数 >= 1 の係数がすべて 0)
#   (N∞-4) chat = 1(補題 R1-N∞-S -- 本 campaign では sigma_1 <> id が自動)
# いずれかが破れたら Error で即停止する(§9.2 I-j)。加えて gcd(f,f') が単元
# (f の平方非因子性)・seriesLen >= 2M+4・model_digest = expectedModelDigest も
# fail-closed に検査する(便 36 F3.2 (2)(3)(5))。
#
# s := 1/x, w := y/x^3 のチャート(補題 R1-U∞ 1.)。F(s) := s^6 f(1/s) は
# f の係数列を逆順にしたもの(f モニックゆえ F(0)=1)。W は W^2=F、W(0)=1 の
# 冪級数(A∞-1)。Atilde(s):=s^M A(1/s)、Btilde(s):=s^{M-3} B(1/s) も係数列の
# 逆順(A∞-2)。P0=infty_- では w=-W ゆえ G_-(s):=Atilde(s)-W(s)*Btilde(s)、
# u^{(A)} := [s^{2M}] G_-(A∞-3、補題 R1-B∞ より [s^{M+M}]=[s^{2M}])。
ReverseCoeffs := function(c) return Reversed(c); end;;

PathA_CanonicalModelStringNinf := function(model)
  local joinRat;
  joinRat := function(lst) return JoinC(List(lst, String), ","); end;;
  return Concatenation(
    "id=", model.id, ";",
    "branch=N_infty;",
    "M=", String(model.M), ";",
    "f=[", joinRat(model.f), "];",
    "A=[", joinRat(model.A), "];",
    "B=[", joinRat(model.B), "]"
  );
end;;

PathA_ModelDigestNinf := function(model)
  local s, tmp, f, line;
  s := PathA_CanonicalModelStringNinf(model);
  tmp := Concatenation("search/.tmp_model_digest_pathA_ninf_", model.id, ".txt");
  WriteFile(tmp, s);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", tmp, ".out\""));
  f := InputTextFile(Concatenation(tmp, ".out"));
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", tmp, ".out\""));
  return line{[1..64]};
end;;

ExtractPathA_Ninf := function(model)
  local M, seriesLen, degA, degB, aM, bMm3, Nlambda, chat, gcdUnit,
        Fasc, W, Atilde, Btilde, GMinus, k, lowerZero,
        u, higherRaw, modelDigest, report;

  if not IsBound(model.branch) or model.branch <> "N_infty" then
    Error("ExtractPathA_Ninf (I-m): model.branch must be the literal string \"N_infty\", got ",
          model.branch);
  fi;
  if not IsBound(model.M) then
    Error("ExtractPathA_Ninf: model.M is required (Rule 1 M naming; the old model.n field name is retired)");
  fi;
  # 便 37 F3(R-8): P0_type は副枝 (N_infty) では常に "nonWeierstrass"
  # (補題 R1-M0 3.)。field があれば逐語一致を要求する(fail-closed)。
  if IsBound(model.P0_type) and model.P0_type <> "nonWeierstrass" then
    Error("ExtractPathA_Ninf (I-m): P0_type must be \"nonWeierstrass\" for branch=\"N_infty\" (Lemma R1-M0 3.), got ",
          model.P0_type);
  fi;

  M := model.M;
  seriesLen := model.seriesLen;

  if Length(model.f) <> 7 then
    Error("ExtractPathA_Ninf: f must have degree 6 (genus-2 sextic model), got length ", Length(model.f));
  fi;
  if model.f[7] <> 1 then
    Error("ExtractPathA_Ninf: f must be monic (leading coeff 1)");
  fi;

  # -- (N∞-1) --
  degA := Length(model.A) - 1;
  degB := Length(model.B) - 1;
  if degA <> M then
    Error("ExtractPathA_Ninf (N∞-1): deg A must equal M=", M, ", got ", degA);
  fi;
  if degB <> M - 3 then
    Error("ExtractPathA_Ninf (N∞-1): deg B must equal M-3=", M - 3, ", got ", degB);
  fi;

  # -- (N∞-2) --
  aM := model.A[M + 1];
  bMm3 := model.B[M - 3 + 1];
  if aM <> bMm3 then
    Error("ExtractPathA_Ninf (N∞-2): b_{M-3} (", bMm3, ") must equal a_M (", aM, ")");
  fi;
  if aM = 0 then
    Error("ExtractPathA_Ninf (N∞-2): a_M must be nonzero");
  fi;

  # -- (N∞-3)/(N∞-4): exact (untruncated) polynomial computation of N(lambda) = A^2 - B^2 f --
  Nlambda := ExactPolyTrim(ExactPolySub(ExactPolyMul(model.A, model.A),
                                        ExactPolyMul(ExactPolyMul(model.B, model.B), model.f)));
  if Length(Nlambda) <> 1 then
    Error("ExtractPathA_Ninf (N∞-3): A^2-B^2*f is not constant, degree ", Length(Nlambda) - 1);
  fi;
  chat := Nlambda[1];
  if chat = 0 then
    Error("ExtractPathA_Ninf (N∞-3): A^2-B^2*f is the zero constant");
  fi;
  if chat <> 1 then
    Error("ExtractPathA_Ninf (N∞-4): chat must equal 1 (Lemma R1-N∞-S; sigma_1<>id is automatic in this campaign), got ", chat);
  fi;

  # -- gcd(f,f') must be a unit (f squarefree) --
  gcdUnit := PolyGcdIsUnit(model.f);
  if not gcdUnit then
    Error("ExtractPathA_Ninf: gcd(f,f') is not a unit -- f is not squarefree (fixture corruption)");
  fi;

  # -- required series length (便 36 F3.2 (2)) --
  if seriesLen < 2 * M + 4 then
    Error("ExtractPathA_Ninf: seriesLen (", seriesLen, ") must be >= 2M+4 = ", 2 * M + 4);
  fi;

  # -- model digest binding to the frozen/expected value (R-7 mechanism, 便 36 F3.2 (3)) --
  modelDigest := PathA_ModelDigestNinf(model);
  if IsBound(model.expectedModelDigest) then
    if modelDigest <> model.expectedModelDigest then
      Error("ExtractPathA_Ninf (I-l): model_digest (", modelDigest,
            ") does not match expectedModelDigest (", model.expectedModelDigest, ")");
    fi;
  fi;

  # F(s) = s^6 f(1/s): reverse of f's ascending coeffs, then pad to seriesLen.
  Fasc := ShallowCopy(ReverseCoeffs(model.f));
  while Length(Fasc) < seriesLen do Add(Fasc, 0); od;
  if Fasc[1] <> 1 then
    Error("ExtractPathA_Ninf: F(0) must be 1 (monic f), got ", Fasc[1]);
  fi;

  W := PSSqrt(Fasc, 1, seriesLen);

  Atilde := ShallowCopy(ReverseCoeffs(model.A));
  while Length(Atilde) < seriesLen do Add(Atilde, 0); od;
  Btilde := ShallowCopy(ReverseCoeffs(model.B));
  while Length(Btilde) < seriesLen do Add(Btilde, 0); od;

  # P0 = infty_-: w = -W, so lambda = s^{-M}(Atilde + w*Btilde) = s^{-M}(Atilde - W*Btilde) =: s^{-M} G_-.
  GMinus := PSSub(Atilde, PSMul(W, Btilde));

  lowerZero := true;
  for k in [1 .. 2*M] do
    if GMinus[k] <> 0 then lowerZero := false; fi;
  od;

  u := GMinus[2*M + 1];
  higherRaw := List([2*M + 1 .. Minimum(seriesLen, 2*M + 4)], k -> GMinus[k]);

  report := rec(
    schema := "u-pathA-ninf/v3",
    id := model.id,
    branch := "N_infty",
    P0Type := "nonWeierstrass",
    M := M,
    f := model.f,
    A := model.A,
    B := model.B,
    seriesLen := seriesLen,
    degAEqualsM := (degA = M),
    degBEqualsMminus3 := (degB = M - 3),
    bMm3EqualsAM := (aM = bMm3),
    aM := aM,
    bMm3 := bMm3,
    gcdFFprimeIsUnit := gcdUnit,
    chat := chat,
    chatEquals1 := (chat = 1),
    lowerOrderVanish := lowerZero,
    u_pathA_ninf := u,
    higherOrderRaw := higherRaw,
    W_mod_check := ForAll(PSSub(PSMul(W, W), Fasc), c -> c = 0),
    modelDigest := modelDigest,
    expectedModelDigest := model.expectedModelDigest,
    modelCanonicalString := PathA_CanonicalModelStringNinf(model)
  );
  return report;
end;;

ReportToJSON_Ninf := function(r)
  return Concatenation("{",
    JStr("schema"), ":", JStr(r.schema), ",",
    JStr("id"), ":", JStr(r.id), ",",
    JStr("branch"), ":", JStr(r.branch), ",",
    JStr("P0_type"), ":", JStr(r.P0Type), ",",
    JStr("M"), ":", String(r.M), ",",
    JStr("f_coeffs_ascending"), ":", JRatList(r.f), ",",
    JStr("A_coeffs_ascending"), ":", JRatList(r.A), ",",
    JStr("B_coeffs_ascending"), ":", JRatList(r.B), ",",
    JStr("series_length"), ":", String(r.seriesLen), ",",
    JStr("deg_A_equals_M"), ":", JB(r.degAEqualsM), ",",
    JStr("deg_B_equals_Mminus3"), ":", JB(r.degBEqualsMminus3), ",",
    JStr("b_Mm3_equals_a_M"), ":", JB(r.bMm3EqualsAM), ",",
    JStr("a_M"), ":", JRat(r.aM), ",",
    JStr("b_Mm3"), ":", JRat(r.bMm3), ",",
    JStr("gcd_f_fprime_is_unit"), ":", JB(r.gcdFFprimeIsUnit), ",",
    JStr("chat"), ":", JRat(r.chat), ",",
    JStr("chat_equals_1"), ":", JB(r.chatEquals1), ",",
    JStr("W_squared_equals_F"), ":", JB(r.W_mod_check), ",",
    JStr("lower_order_vanish"), ":", JB(r.lowerOrderVanish), ",",
    JStr("u_pathA_ninf"), ":", JRat(r.u_pathA_ninf), ",",
    JStr("higher_order_raw"), ":", JRatList(r.higherOrderRaw), ",",
    JStr("model_digest"), ":", JStr(r.modelDigest), ",",
    JStr("model_digest_algo"), ":", JStr("sha256(canonical_model_string_ninf)"), ",",
    JStr("expected_model_digest"), ":", JStr(r.expectedModelDigest), ",",
    JStr("canonical_model_string"), ":", JStr(r.modelCanonicalString),
  "}");
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
    JStr("schema"), ":", JStr("u-pathA/v3"), ",",
    JStr("id"), ":", JStr(r.id), ",",
    JStr("M"), ":", String(r.M), ",",
    JStr("branch"), ":", JStr(r.branch), ",",
    JStr("P0_type"), ":", JStr(r.P0_type), ",",
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
