#############################################################################
# search/kummer-decide.g -- Rule 1 SS8 exact Kummer 判定器
# 委嘱: 便 32 P6 後半 + 便 34 blocker 2/3/4 修理(Sol 便 34 P6-E1/K1/C3)。
# M パラメトリック(K^(3): M=6, K=Q(zeta_12) / K^(5): M=10, K=Q(zeta_20))。
# GAP の CF(n) 上多項式演算 (Factors) を用いて T^p - w (p | M, p 素数) の
# 一次因子の有無を厳密に判定する。
#
# 身分(便 34 P6-E1 以降): 本ファイルは **library** である(関数定義のみ・
# 入力パラメトリック・QUIT なし・トップレベル実行なし)。K3 較正の実行は
# search/kummer-decide-k3-driver.g(薄い driver)が担う。将来の K5 driver は
# 本ファイルを Read して IsMthPower/OrdModM/KummerCovariance3Check を呼ぶ
# だけでよい。
#
# SS8.2 (8.1): M が相異なる素数の積 (6=2*3, 10=2*5) のとき
#   w in K^{*M}  <=>  w in K^{*p} かつ w in K^{*q}  (p,q = M の素因数)
# 陽性証明書は Bezout 表示 (GcdRepresentation) による明示合成
#   e := c_p^a * c_q^b   (a*q + b*p = 1)   が e^M = w を満たすことで与える。
# 陰性証明書 (obstruction) は (O-b)/(O-c): T^p - w が K[T] で既約であること
# (イデアル分解 (O-a) は本実装では未実装 -- 8.3 の「いずれか一つで足りる」
# の要件は (O-b)/(O-c) で満たす)。
#
# 便 34 P6-K1 (blocker 3 後半 / F4.4): 従来の証明書は最終 witness と ord しか
# 保存せず、「位数がちょうど d である」ことの根拠(d の真の約数それぞれの
# 非 M 乗 obstruction)を artifact から失っていた。本版は OrdModM のループが
# 試した全ての(失敗した)約数について obstruction を収集し、JSON に
# minimality_obstructions として保存する。また witness が満たす式を
# 明示的に e^M = w^ord(誤って e^M=w としない)として記録する。
#
# 便 34 P6-C3 (blocker 4 / F4.5): manifest §較正三層 3「τ ↦ τ∘[d] と Kummer
# character の逆冪を同時に施し (5') 相当の整合が不変であること」の検査を
# KummerCovariance3Check として実装する。
#############################################################################

Read("search/gaplib_common.g");

# 罠(発見・便 32): GAP の CF(n) は「乗法群を含む Cyclotomics の緩い collection」
# であって、Indeterminate(CF(n),"T") 上の Factors は有理係数の範囲でしか
# 分解しない(非有理な根を見逃す)。実測: K=CF(12) 上 T^2+4 は明らかに
# 2*E(4) (=2i) を根に持つ (Value で確認済み) にもかかわらず Factors は
# 既約と誤答する。正しい構成は AlgebraicExtension(Rationals,
# CyclotomicPolynomial(Rationals, n)) で「体」として GAP に認識させること
# (実測: この構成では T^2+4 = (T-2a^3)(T+2a^3) と正しく分解される。
# a = 定義多項式の根、cyclotomic polynomial の根なので実質 zeta_n の役)。
# 本ファイルはこの構成(AlgebraicExtension 上の Factors)を正本として採用する。
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
#
# 便 34 P6-K1: 試した divisor のうち失敗したもの全てを minimalityObstructions
# として収集し返す(以前は最初に成功した d だけを返し、途中の失敗は捨てて
# いた -- artifact 単体からは「なぜ ord が 1 でなく 3 なのか」が読めなかった)。
OrdModM := function(K, M, w)
  local divs, d, wd, res, obstructions;
  divs := DivisorsInt(M);
  obstructions := [];
  for d in divs do
    wd := w^d;
    res := IsMthPower(K, M, wd);
    if not res.decided then
      return rec(decided := false, reason := res.reason, triedDivisor := d,
                  minimalityObstructions := obstructions);
    fi;
    if res.isPower then
      return rec(decided := true, ord := d, witness := res.witness, w := w, M := M,
                  minimalityObstructions := obstructions);
    fi;
    Add(obstructions, rec(divisor := d, obstructionPrime := res.obstructionPrime,
                           obstructionType := res.obstructionType));
  od;
  # 理論上 d=M で必ず isPower=true になるはずなので、ここに来ることはない
  return rec(decided := false, reason := "no divisor produced isPower=true (unexpected)",
             minimalityObstructions := obstructions);
end;;

#################### 便 34 P6-C3: 第三 covariance (tau∘[d] + character 逆冪) ####################
# *** 撤回(便 36・裁定 36・Sol 便 35 F3 = blocker 4) ***
# 以下の KummerCovariance3Check / KummerCovariance3ToJSON は、witness
# e in K に対する GaloisCyc(e,d)(= Gal(K/Q) の K 内自己同型)の作用を検査
# するものであり、要求された Kummer character
#   kappa_w(gamma) = gamma(w^{1/M})/w^{1/M}   (gamma in G_K)
# ではない(e in K は定義により G_K に固定されるので GaloisCyc(e,d)/e の
# 非自明値はこの character と無関係)。また出力に b_i・tau_i・rho_0・j_i・
# formal a のいずれも現れず、便 34 F4.5 が要求した較正を実行し得ない
# (Sol 便 35 F3 全文)。両関数は**もう呼び出さない**(kummer-decide-k3-driver.g
# 参照)。後継は search/kummer-cov3-actual.g(rho_0/tau/j の実値 covariance
# を扱う・射程限定を明記)。旧証明書は certificates/k5pipeline/retracted/ へ
# 退避済み(NOTE.md 参照)。コードは history として残すが dead code である。
#
# manifest §較正三層 3: tau -> tau∘[d] (mu_M の生成元の取り替え) と Kummer
# character kappa の逆冪 kappa -> d^{-1}*kappa を**同時に**施しても (5')
# 相当の等式 sigma(e)/e = zeta_M^{kappa(sigma)} が(取り替えた生成元の下で)
# 引き続き成り立つことを確認する。
#
# 実装方針: witness e (AlgebraicExtension(Rationals, CyclotomicPolynomial(n))
# の元、n は w の属する体の位数 -- K3 較正では n=12) を、GAP 組み込みの
# native Cyclotomics (E(n)) へ座標変換し(a と E(n) は同じ定義多項式の根な
# ので基底表現がそのまま対応する)、native Cyclotomics 上でのみ定義されて
# 正しく動く GaloisCyc(x,d) (= Galois 作用 zeta_n -> zeta_n^d) を使う。
# Factors の罠(CF(n) 上の根の見逃し)は根探索にのみ関わるので、根 e が
# 既知の今回は影響しない(GaloisCyc は Factors を経由しない別の GAP 組み込み
# 機能)。
KummerCovariance3Check := function(n, M, w, ord, witnessAE)
  local coeffs, i, eNative, galoisUnits, zetaM, kappaTable, d, sigE, ratio, k,
        found, unitsModM, dprime, dprimeInv, reparamResults, expectedKNew, kNew,
        allMatch;

  coeffs := ExtRepOfObj(witnessAE);
  eNative := Sum([1 .. Length(coeffs)], i -> coeffs[i] * E(n)^(i - 1));
  if eNative^M <> w^ord then
    Error("KummerCovariance3Check: native reconstruction of witness fails e^M=w^ord");
  fi;

  zetaM := E(M);
  galoisUnits := Filtered([1 .. n - 1], d -> Gcd(d, n) = 1);

  kappaTable := rec();
  for d in galoisUnits do
    sigE := GaloisCyc(eNative, d);
    ratio := sigE / eNative;
    found := fail;
    for k in [0 .. M - 1] do
      if zetaM^k = ratio then found := k; break; fi;
    od;
    if found = fail then
      Error("KummerCovariance3Check: sigma_d(e)/e is not a power of zeta_M (unexpected)");
    fi;
    kappaTable.(String(d)) := found;
  od;

  unitsModM := Filtered([1 .. M - 1], x -> Gcd(x, M) = 1);
  reparamResults := [];
  for dprime in unitsModM do
    dprimeInv := First([0 .. M - 1], x -> (x * dprime) mod M = 1);
    for d in galoisUnits do
      sigE := GaloisCyc(eNative, d);
      ratio := sigE / eNative;
      kNew := First([0 .. M - 1], x -> (zetaM^dprime)^x = ratio);
      if kNew = fail then
        Error("KummerCovariance3Check: reparametrised exponent not found (unexpected)");
      fi;
      expectedKNew := (dprimeInv * kappaTable.(String(d))) mod M;
      Add(reparamResults, rec(d := d, dprime := dprime, kNew := kNew,
                              expectedKNew := expectedKNew, match := (kNew = expectedKNew)));
    od;
  od;
  allMatch := ForAll(reparamResults, r -> r.match);

  return rec(n := n, M := M, w := w, ord := ord, galoisUnits := galoisUnits,
             kappaTable := kappaTable, unitsModM := unitsModM,
             reparamResults := reparamResults, allMatch := allMatch,
             witnessNativeCoeffs := coeffs);
end;;

#################### JSON 出力 ####################
JCyc := function(c)
  # 代数拡大元の直列化。JSON の数値リテラルは分数を許さないので有理数も
  # 含め常に文字列として引用符付きで出力する(呼び出し側で parseRat する)。
  return JStr(String(c));
end;;

# obstructions リスト(OrdModM.minimalityObstructions)を JSON 配列に直列化
JObstructions := function(obs)
  local parts, o;
  parts := [];
  for o in obs do
    Add(parts, Concatenation("{",
      JStr("divisor"), ":", String(o.divisor), ",",
      JStr("obstruction_prime"), ":", String(o.obstructionPrime), ",",
      JStr("obstruction_type"), ":", JStr(o.obstructionType),
    "}"));
  od;
  return JArr(parts);
end;;

KummerCertToJSON := function(label, K, n, M, w, ordRes)
  local witnessStr, witnessCoeffsStr;
  witnessStr := "null";
  witnessCoeffsStr := "null";
  if ordRes.decided and IsBound(ordRes.witness) then
    witnessStr := JCyc(ordRes.witness);
    witnessCoeffsStr := JArr(List(ExtRepOfObj(ordRes.witness), x -> JStr(String(x))));
  fi;
  return Concatenation("{",
    JStr("schema"), ":", JStr("kummer-decide/v2"), ",",
    JStr("label"), ":", JStr(label), ",",
    JStr("field_n"), ":", String(n), ",",
    JStr("M"), ":", String(M), ",",
    JStr("w"), ":", JCyc(w), ",",
    JStr("decided"), ":", JB(ordRes.decided), ",",
    JStr("ord"), ":", (function() if ordRes.decided then return String(ordRes.ord); else return "null"; fi; end)(), ",",
    JStr("witness"), ":", witnessStr, ",",
    JStr("witness_coeffs_basis_powers_of_root"), ":", witnessCoeffsStr, ",",
    JStr("witness_equation"), ":", JStr("witness^M = w^ord"), ",",
    JStr("minimality_obstructions"), ":",
      (function()
        if IsBound(ordRes.minimalityObstructions) then
          return JObstructions(ordRes.minimalityObstructions);
        else
          return "[]";
        fi;
      end)(),
  "}");
end;;

# cov3 結果 (KummerCovariance3Check の戻り値) の JSON 直列化
JIntList := function(lst) return JArr(List(lst, String)); end;;

JKappaTable := function(tbl, units)
  local parts, d;
  parts := [];
  for d in units do
    Add(parts, Concatenation(JStr(String(d)), ":", String(tbl.(String(d)))));
  od;
  return Concatenation("{", JoinC(parts, ","), "}");
end;;

JReparamResults := function(results)
  local parts, r;
  parts := [];
  for r in results do
    Add(parts, Concatenation("{",
      JStr("d"), ":", String(r.d), ",",
      JStr("dprime"), ":", String(r.dprime), ",",
      JStr("kNew"), ":", String(r.kNew), ",",
      JStr("expectedKNew"), ":", String(r.expectedKNew), ",",
      JStr("match"), ":", JB(r.match),
    "}"));
  od;
  return JArr(parts);
end;;

KummerCovariance3ToJSON := function(cov3)
  return Concatenation("{",
    JStr("schema"), ":", JStr("kummer-cov3/v1"), ",",
    JStr("field_n"), ":", String(cov3.n), ",",
    JStr("M"), ":", String(cov3.M), ",",
    JStr("w"), ":", JCyc(cov3.w), ",",
    JStr("ord"), ":", String(cov3.ord), ",",
    JStr("witness_coeffs_basis_powers_of_root"), ":", JArr(List(cov3.witnessNativeCoeffs, x -> JStr(String(x)))), ",",
    JStr("galois_units_mod_n"), ":", JIntList(cov3.galoisUnits), ",",
    JStr("units_mod_M"), ":", JIntList(cov3.unitsModM), ",",
    JStr("kappa_table_wrt_zetaM"), ":", JKappaTable(cov3.kappaTable, cov3.galoisUnits), ",",
    JStr("reparam_results"), ":", JReparamResults(cov3.reparamResults), ",",
    JStr("all_match"), ":", JB(cov3.allMatch), ",",
    JStr("claim"), ":", JStr("tau -> tau∘[dprime] (zeta_M -> zeta_M^dprime を新生成元に取り替え) と kappa -> dprime^{-1}*kappa (Kummer character 逆冪) を同時に施しても sigma_d(e)/e = (新生成元)^kappa'(d) が引き続き成り立つ"),
  "}");
end;;

# 本ファイルは library。実行(K3 較正・driver・QUIT)は
# search/kummer-decide-k3-driver.g が担う。
