#############################################################################
# search/kummer-decide.g -- Rule 1 SS8 exact Kummer 判定器
# 委嘱: 便 32 P6 後半。M パラメトリック(K^(3): M=6, K=Q(zeta_12) /
# K^(5): M=10, K=Q(zeta_20))。GAP の CF(n) 上多項式演算 (Factors) を用いて
# T^p - w (p | M, p 素数) の一次因子の有無を厳密に判定する。
#
# SS8.2 (8.1): M が相異なる素数の積 (6=2*3, 10=2*5) のとき
#   w in K^{*M}  <=>  w in K^{*p} かつ w in K^{*q}  (p,q = M の素因数)
# 陽性証明書は Bezout 表示 (GcdRepresentation) による明示合成
#   e := c_p^a * c_q^b   (a*q + b*p = 1)   が e^M = w を満たすことで与える。
# 陰性証明書 (obstruction) は (O-b)/(O-c): T^p - w が K[T] で既約であること
# (イデアル分解 (O-a) は本実装では未実装 -- 8.3 の「いずれか一つで足りる」
# の要件は (O-b)/(O-c) で満たす)。
#############################################################################

Read("search/gaplib_common.g");

# 罠(発見・本便): GAP の CF(n) は「乗法群を含む Cyclotomics の緩い collection」
# であって、Indeterminate(CF(n),"T") 上の Factors は有理係数の範囲でしか
# 分解しない(非有理な根を見逃す)。実測: K=CF(12) 上 T^2+4 は明らかに
# 2*E(4) (=2i) を根に持つ (Value で確認済み) にもかかわらず Factors は
# 既約と誤答する。正しい構成は AlgebraicExtension(Rationals,
# CyclotomicPolynomial(Rationals,n)) で「体」として GAP に認識させること
# (実測: この構成では T^2+4 = (T-2a^3)(T+2a^3) と正しく分解される。
# a = 定義多項式の根、cyclotomic polynomial の根なので実質 zeta_n の役)。
# 本ファイルはこの構成を正本とする。
CyclotomicFieldForFactoring := function(n)
  return AlgebraicExtension(Rationals, CyclotomicPolynomial(Rationals, n));
end;;

# T^p - w over K (= CyclotomicFieldForFactoring(n) の出力) の一次因子を探す。
# 見つかれば根 c (c^p = w) を返し、見つからなければ fail を返す
# (= T^p-w が K 上既約、つまり obstruction (O-b)/(O-c))。
FindLinearFactor := function(K, p, w)
  local x, poly, facs, fac, coeffs, c;
  x := Indeterminate(K, "T");
  poly := x^p - w;
  facs := Factors(poly);
  for fac in facs do
    coeffs := CoefficientsOfUnivariatePolynomial(fac);
    if Length(coeffs) = 2 then
      # fac = coeffs[1] + coeffs[2]*T (monic normalisation: coeffs[2] should be 1,
      # but divide defensively in case GAP returns non-monic linear factor)
      c := -coeffs[1] / coeffs[2];
      if c^p <> w then Error("FindLinearFactor: candidate root fails c^p=w check"); fi;
      return c;
    fi;
  od;
  return fail;
end;;

# w が K^{*M} に入るかどうかを SS8.2 (8.1) に従って判定する。
# M は相異なる素数の積であることを要求 (それ以外は UNKNOWN として Error で止める
# -- 本実装の対象宇宙 M in {6,10} はこの仮定を満たす)。
IsMthPower := function(K, M, w)
  local primes, roots, p, q, c, a, b, rep, e;
  primes := PrimeDivisors(M);
  if Product(primes) <> M then
    return rec(decided := false, reason := Concatenation("M=", String(M), " is not a squarefree product of distinct primes -- UNKNOWN (SS8.2 の枠外)"));
  fi;
  roots := rec();
  for p in primes do
    c := FindLinearFactor(K, p, w);
    if c = fail then
      return rec(decided := true, isPower := false, obstructionPrime := p,
                  obstructionType := "irreducible T^p-w (O-b/O-c)", w := w, M := M);
    fi;
    roots.(String(p)) := c;
  od;
  if Length(primes) = 1 then
    e := roots.(String(primes[1]));
  elif Length(primes) = 2 then
    # w = c_p^p = c_q^q (両方 M 乗根の候補)。Bezout a*q+b*p=1 のとき
    # e := c_p^a * c_q^b は e^M = w を満たす (下記検算で確認する):
    #  e^{pq} = c_p^{a p q} * c_q^{b p q} = (c_p^p)^{aq} * (c_q^q)^{bp}
    #         = w^{aq} * w^{bp} = w^{aq+bp} = w^1
    p := primes[1]; q := primes[2];
    rep := GcdRepresentation(q, p);   # a*q + b*p = 1
    a := rep[1]; b := rep[2];
    e := roots.(String(p))^a * roots.(String(q))^b;
  else
    return rec(decided := false, reason := "more than 2 distinct prime factors not implemented");
  fi;
  if e^M <> w then Error("IsMthPower: witness verification failed (e^M <> w)"); fi;
  return rec(decided := true, isPower := true, witness := e, M := M, w := w);
end;;

# ord(w) := 最小の d | M で w^d in K^{*M} となるもの (常に d=M で成立するので
# 停止性は保証される: w^M = w^M は自明に M 乗)。
OrdModM := function(K, M, w)
  local divs, d, wd, res;
  divs := DivisorsInt(M);
  for d in divs do
    wd := w^d;
    res := IsMthPower(K, M, wd);
    if not res.decided then
      return rec(decided := false, reason := res.reason, triedDivisor := d);
    fi;
    if res.isPower then
      return rec(decided := true, ord := d, witness := res.witness, w := w, M := M);
    fi;
  od;
  # 理論上 d=M で必ず isPower=true になるはずなので、ここに来ることはない
  return rec(decided := false, reason := "no divisor produced isPower=true (unexpected)");
end;;

#################### JSON 出力 ####################
JCyc := function(c)
  # 代数拡大元の直列化。JSON の数値リテラルは分数を許さないので有理数も
  # 含め常に文字列として引用符付きで出力する(呼び出し側で parseRat する)。
  return JStr(String(c));
end;;

KummerCertToJSON := function(label, K, n, M, w, ordRes)
  local witnessStr;
  witnessStr := "null";
  if ordRes.decided and IsBound(ordRes.witness) then witnessStr := JCyc(ordRes.witness); fi;
  return Concatenation("{",
    JStr("schema"), ":", JStr("kummer-decide/v1"), ",",
    JStr("label"), ":", JStr(label), ",",
    JStr("field_n"), ":", String(n), ",",
    JStr("M"), ":", String(M), ",",
    JStr("w"), ":", JCyc(w), ",",
    JStr("decided"), ":", JB(ordRes.decided), ",",
    JStr("ord"), ":", (function() if ordRes.decided then return String(ordRes.ord); else return "null"; fi; end)(), ",",
    JStr("witness"), ":", witnessStr,
  "}");
end;;

#################### K3 較正ケース ####################
# u = -4 (K3-regression の pathA/pathB 一致値), v := u^{-1} = -1/4.
# COV-2 (X -> X^{-1} / class 反転) 較正: ord(u) と ord(v)=ord(u^{-1}) が
# 一致すること (逆元は群の中で常に同じ位数を持つ -- 位数不変の直接検算)。

K12 := CyclotomicFieldForFactoring(12);;

RunK3Calibration := function()
  local u, v, ordU, ordV, out;
  u := -4;
  v := u^-1;   # -1/4
  Print("=== kummer-decide K3 calibration (K=Q(zeta_12), M=6) ===\n");
  ordU := OrdModM(K12, 6, u);
  Print("ord(u=-4)      = ", ordU.ord, "  witness = ", ordU.witness, "\n");
  ordV := OrdModM(K12, 6, v);
  Print("ord(v=u^-1=-1/4) = ", ordV.ord, "  witness = ", ordV.witness, "\n");
  Print("COV-2 class-reversal check: ord(u) = ord(v)? ", ordU.ord = ordV.ord, "\n");
  WriteFile("certificates/k5fixture/K3-regression-kummer-u.json", KummerCertToJSON("K3-regression-u", K12, 12, 6, u, ordU));
  WriteFile("certificates/k5fixture/K3-regression-kummer-uinv.json", KummerCertToJSON("K3-regression-uinv", K12, 12, 6, v, ordV));
end;;

if not IsBoundGlobal("KUMMER_DECIDE_ONLY_LOAD") then
  RunK3Calibration();
fi;

QUIT;
