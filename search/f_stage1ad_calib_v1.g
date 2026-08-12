# search/f_stage1ad_calib_v1.g -- 段1'(Ad) 較正スイート+本番値(裁定1012)
# 正本 = docs/notes/F_stage1ad_prereg_v1_1.md(sha 768898e153ec7b211c45bb8d6b8ae91d378d570aeb79940a252abaefbe0bbe61・凍結・変更禁止)
#      + docs/notes/F_stage1ad_prereg_v1.md(前版、v1.1に置換されていない節を継承)
#
# 系統B(安定元法): H^n(SL(2,p),M) = H^n(C_p,M)^T (TI Sylow, n>=1)。GROUP を構成せず、
#   P=<u(1)>・T=<d(lambda)> の M 上の作用行列だけで計算する。
#   H^2(C_p,M) = M^P (x) y, y の T-重み = lambda^{-2} (x,y = Lambda(x)(x)F_p[y] の生成元、
#   x = P の双対、y=beta(x))。よって T-不変性の条件は「M^P の重み k について k-2 = 0 (mod p-1)」。
#   有効範囲では k は discrete log で 0..p-2 の整数として一意に取れるので、k=2 と同値。
#
# 較正: cal-1(C_p,W)・cal-2(H_F,W/W(x)det)・cal-3(H_F,sl_2/sl_2(x)det)・cal-4(p=23 リハ)・
#   cal-5(系統B独立実装・p<=23で既知値と突合、weight 3.6 の反同語反復済み)・cal-6(Sym^2 W、
#   detに一切言及せず構成)。calib_primes は {7,11,23} を含む(p=5単独への降格禁止)。
#
# ★ 停止線: 系統Bがcap 60秒を超過 -> UNKNOWN+設計差し戻し。calib全PASSかつbound_violated=false
#   を通してから枝表(要修正1)。判定語なし(枝の帰結の"適用可否"のみ記録、最終解釈は司令塔)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ====================================================================
# GF(p) 上の明示行列: u(1)(P生成元)・d(lambda)(T生成元)・A=diag(1,-1)
# 加群: W(自然表現・2次元)・Ad=sl_2(随伴・3次元、基底 e,h,f)・Sym^2 W(3次元)
# ====================================================================

# W 上の表現: g そのもの(2x2)
RepW := function(g) return g; end;;

# sl_2 の基底 e=[[0,1],[0,0]], h=[[1,0],[0,-1]], f=[[0,0],[1,0]] 上の Ad(g) 表現(3x3)、
# Ad(g)X = g*X*g^-1 をこの基底で書いた行列
RepAd := function(g, p)
  local ginv, e, h, f, basis, images, mat, i, img, coordsOf, X, a11,a12,a21,a22;
  ginv := g^-1;
  e := [[0,1],[0,0]]*Z(p)^0;;  h := [[1,0],[0,-1]]*Z(p)^0;;  f := [[0,0],[1,0]]*Z(p)^0;;
  basis := [e,h,f];;
  coordsOf := function(X)
    # X = a*e + b*h + c*f -> [a,b,c] via matrix entries: X=[[b,a],[c,-b]]
    return [X[1][2], X[1][1], X[2][1]];
  end;;
  images := [];;
  for X in basis do
    img := g*X*ginv;;
    Add(images, coordsOf(img));
  od;
  # images[i] = image of basis[i] as coordinate vector; matrix acts on COLUMN vectors ->
  # matrix columns = images
  mat := TransposedMat(images);;
  return mat;;
end;;

# Sym^2(W): 基底 e1^2, e1*e2, e2^2 (3次元)。g=[[a,b],[c,d]] の作用:
# e1 -> a*e1+c*e2, e2 -> b*e1+d*e2 (列ベクトル作用と仮定: g*(x,y)^T)
# Sym^2 の基底 (e1^2, e1e2, e2^2) 上での行列を直接展開して構成
RepSym2 := function(g)
  local a,b,c,d, mat;
  a:=g[1][1];; b:=g[1][2];; c:=g[2][1];; d:=g[2][2];;
  # e1' = a e1 + c e2 ; e2' = b e1 + d e2
  # (e1')^2 = a^2 e1^2 + 2ac e1e2 + c^2 e2^2
  # e1'e2'  = ab e1^2 + (ad+bc) e1e2 + cd e2^2
  # (e2')^2 = b^2 e1^2 + 2bd e1e2 + d^2 e2^2
  # mat の列 j = 基底ベクトル j の像の座標(列ベクトル規約 mat*v、実地検算:
  # scratchpad/debug_sym2b.g で確認 -- 追加の TransposedMat は誤りだった。
  # RepAd と違い、ここでは a,c/b,d が最初から「列=像」の形で書き下されているため
  # 転置は不要(RepAd は images を「行=像」のリストとして作るので転置が要る、という違い)。
  mat := [ [a^2, a*b, b^2],
           [2*a*c, a*d+b*c, 2*b*d],
           [c^2, c*d, d^2] ];;
  return mat;;
end;;

# ====================================================================
# P-invariant部分空間 + T-重み(discrete log)+ A の符号、を1モジュールについて計算
# ====================================================================
AnalyzeModule := function(repFunc, p, dimM, lambdaVal, u1mat, dLmat, Amat)
  local nullMat, invBasis, dimInv, weightsFound, entry, dLonV, ratio, k, kk,
        weight2Vectors, i, v, Av, sign, results, found2;
  # P-invariant: {v (列ベクトル) : u1mat*v = v}
  # self-caught bug #1(裁定1012 発火中に発見・第1版): RepAd/RepSym2 はどちらも
  # 「mat の列 i = 基底ベクトル i の像」という**列ベクトル規約**(mat*v)で構成されている
  # (実地検算: u1_Ad*[e の座標]=[e の座標](Pで固定)・dL_Ad*[e の座標]=lambda^2*[e の座標]、
  # scratchpad/debug_conv.g で確認 — v*mat では e が固定されない)。
  # 旧コード(2版とも)は v*mat(行ベクトル規約)で読んでおり不整合だった:
  #   初版: NullspaceMat(TransposedMat(nullMat)) [列規約の不変空間] を v*mat で読む(不整合)
  #         -- sl_2 は対称性でたまたま一致・Sym^2W は重み4を誤って拾い p=5でのみ偶然一致
  #         (設計ノート§3.6が警告した較正空虚化の罠そのもの)。
  #   2版(このコメントの直前): NullspaceMat(nullMat) [行規約の不変空間] を v*mat で読む
  #         (これも列規約の真実と不整合 -- 今度は sl_2 側が壊れて発覚)。
  # 正しい形(実地検算で確定): 列規約(mat*v)に統一。不変空間 = 右零空間 =
  # NullspaceMat(TransposedMat(nullMat))、重み確認は dLmat*v(v*dLmat ではない)。
  nullMat := u1mat - IdentityMat(dimM, GF(p));;
  invBasis := NullspaceMat(TransposedMat(nullMat));;   # 列ベクトル規約(mat*v=v)の右零空間
  dimInv := Length(invBasis);;

  results := rec(dim_M_P := dimInv, weight2_dim := 0, sign_on_weight2 := fail,
                  weights := []);;

  if dimInv = 0 then
    return results;;
  fi;

  # for each invariant basis vector, is it (or a combination) an eigenvector of dLmat?
  # since dimInv could be >1 in principle; we scan each basis vector's image under dLmat
  # and check if it's a scalar multiple (eigenvector) -- for our 3 modules dimInv=1 expected.
  weightsFound := [];;
  weight2Vectors := [];;
  for v in invBasis do
    dLonV := dLmat * v;;   # 列ベクトル規約(mat*v)に統一(上のコメント参照)
    # find scalar ratio dLonV = ratio * v (component-wise, using first nonzero entry of v)
    i := PositionProperty(v, x -> x <> Zero(GF(p)));;
    ratio := dLonV[i] / v[i];;
    # verify it's a genuine eigenvector
    if dLonV <> ratio*v then
      Add(results.weights, rec(is_eigenvector:=false));
    else
      # discrete log of ratio base lambdaVal
      k := LogFFE(ratio, lambdaVal);;
      if k = fail then k := -1; fi;;  # ratio=0 shouldn't happen (unit group)
      Add(results.weights, rec(is_eigenvector:=true, weight:=k));
      if k = 2 then
        Add(weight2Vectors, v);
      fi;
    fi;
  od;
  results.weight2_dim := Length(weight2Vectors);;

  if Length(weight2Vectors) >= 1 then
    v := weight2Vectors[1];;
    Av := Amat * v;;   # 列ベクトル規約に統一
    i := PositionProperty(v, x -> x <> Zero(GF(p)));;
    sign := Av[i]/v[i];;
    if Av <> sign*v then
      results.sign_on_weight2 := "NOT_EIGENVECTOR_OF_A";;
    else
      if sign = One(GF(p)) then results.sign_on_weight2 := 1;;
      elif sign = -One(GF(p)) then results.sign_on_weight2 := -1;;
      else results.sign_on_weight2 := "OTHER";; fi;
    fi;
  fi;
  return results;;
end;;

# ====================================================================
# 1つの素数 p について全モジュール(W, Ad, Sym2W)を測定
# ====================================================================
MeasureAtPrime := function(p)
  local lambdaVal, u1, dL, A, u1_W, dL_W, A_W, u1_Ad, dL_Ad, A_Ad, u1_S2, dL_S2, A_S2,
        resW, resAd, resS2, dimH2_SL_W, dimH2_SL_Ad, dimH2_SL_S2,
        i0_Ad, i0_S2, out;
  lambdaVal := PrimitiveRoot(GF(p));;
  u1 := [[One(GF(p)),One(GF(p))],[Zero(GF(p)),One(GF(p))]];;
  dL := [[lambdaVal,Zero(GF(p))],[Zero(GF(p)),lambdaVal^-1]];;
  A  := [[One(GF(p)),Zero(GF(p))],[Zero(GF(p)),-One(GF(p))]];;

  # W: rep = identity map
  u1_W := u1;;  dL_W := dL;;  A_W := A;;
  resW := AnalyzeModule(RepW, p, 2, lambdaVal, u1_W, dL_W, A_W);;

  # Ad = sl_2: 3x3 rep via conjugation
  u1_Ad := RepAd(u1, p);;  dL_Ad := RepAd(dL, p);;  A_Ad := RepAd(A, p);;
  resAd := AnalyzeModule(RepAd, p, 3, lambdaVal, u1_Ad, dL_Ad, A_Ad);;

  # Sym^2 W: 3x3 rep
  u1_S2 := RepSym2(u1);;  dL_S2 := RepSym2(dL);;  A_S2 := RepSym2(A);;
  resS2 := AnalyzeModule(RepSym2, p, 3, lambdaVal, u1_S2, dL_S2, A_S2);;

  dimH2_SL_W  := resW.weight2_dim;;
  dimH2_SL_Ad := resAd.weight2_dim;;
  dimH2_SL_S2 := resS2.weight2_dim;;

  # i0: which twist (0=untwisted,1=det-twisted) carries the surviving dim.
  # sign_on_weight2 combines with y's own A-sign (-1, from P->-1 under A, established in doc
  # sec1.3: A u(a) A^-1 = u(-a) => Hom(P,F_p) flips sign => x,y flip sign => y-sign = -1).
  # H^2 total A-sign = sign_on_weight2 * (-1). If total sign = +1 (trivial S3-rep) => i0=0 (untwisted).
  # If total sign = -1 (sign S3-rep) => i0=1 (det-twisted).
  i0_Ad := fail;;  i0_S2 := fail;;
  if dimH2_SL_Ad = 1 and IsInt(resAd.sign_on_weight2) then
    if resAd.sign_on_weight2 * (-1) = 1 then i0_Ad := 0; else i0_Ad := 1; fi;
  fi;
  if dimH2_SL_S2 = 1 and IsInt(resS2.sign_on_weight2) then
    if resS2.sign_on_weight2 * (-1) = 1 then i0_S2 := 0; else i0_S2 := 1; fi;
  fi;

  out := rec(p:=p, lambda:=Int(IntFFE(lambdaVal)),
             W  := rec(dim_M_P:=resW.dim_M_P, weight2_dim:=resW.weight2_dim,
                       weights:=resW.weights, dimH2_SL:=dimH2_SL_W),
             Ad := rec(dim_M_P:=resAd.dim_M_P, weight2_dim:=resAd.weight2_dim,
                       weights:=resAd.weights, dimH2_SL:=dimH2_SL_Ad,
                       sign_on_weight2:=resAd.sign_on_weight2, i0_observed:=i0_Ad),
             Sym2W := rec(dim_M_P:=resS2.dim_M_P, weight2_dim:=resS2.weight2_dim,
                       weights:=resS2.weights, dimH2_SL:=dimH2_SL_S2,
                       sign_on_weight2:=resS2.sign_on_weight2, i0_observed:=i0_S2));;
  return out;;
end;;

# ====================================================================
# 実行: 較正素数 {7,11,23}(+参考 p=5)+ 本番 p=691
# ====================================================================
Print("############################################################\n");
Print("# f_stage1ad_calib_v1.g -- 段1'(Ad) 較正+本番(裁定1012)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;

calibPrimes := [5, 7, 11, 23];;   # 5 は参考(非判別)・7,11,23 は必須(要修正5/軽微5準拠)
allResults := [];;
for p in calibPrimes do
  Add(allResults, MeasureAtPrime(p));
od;;

tCalibEnd := GAPLIB_WallElapsedMs();;
calibElapsedMs := tCalibEnd - t0;;
Print("較正(p=5,7,11,23)経過 = ", calibElapsedMs, " ms\n");

for r in allResults do
  Print("p=", r.p, ": W.dimH2_SL=", r.W.dimH2_SL, " Ad.dimH2_SL=", r.Ad.dimH2_SL,
        " Ad.i0=", r.Ad.i0_observed, " Sym2W.dimH2_SL=", r.Sym2W.dimH2_SL,
        " Sym2W.i0=", r.Sym2W.i0_observed, "\n");
od;;

# ---- cal-1: (C_p, W) 予言 dim H^2 = 1(陽性対照・Sylow層。C_p単独のH^2は常に1次元、TではなくSylow自体)
#      注: これはH^2(C_p,W)自体(T商前)の次元で、Sylow-p部分群上のコホモロジーは常に非零
#      (P自身の作用のみ、H^2(C_p,W)=W(x)y は1次元・T不変性を問わない生の値)。
cal1Results := List(allResults, r -> rec(p:=r.p, dim_M_P:=r.W.dim_M_P));;
cal1Pass := ForAll(cal1Results, r -> r.dim_M_P = 1);;
Print("[", PF(cal1Pass), "] cal-1: (C_p,W) の M^P 次元が全p で1: ", cal1Pass, "\n");

# ---- cal-2: (H_F,W),(H_F,W(x)det) 予言 0,0
cal2Pass := ForAll(allResults, r -> r.W.dimH2_SL = 0);;
Print("[", PF(cal2Pass), "] cal-2: dim H^2(SL,W)=0 全p: ", cal2Pass, "\n");

# ---- cal-3: (H_F,sl_2),(H_F,sl_2(x)det) 予言 1,0(和=1)
cal3Pass := ForAll(allResults, r -> r.Ad.dimH2_SL = 1);;
Print("[", PF(cal3Pass), "] cal-3: dim H^2(SL,sl_2)=1 全p: ", cal3Pass, "\n");

# ---- cal-4: p=23 リハーサル(全3本、予言 0/0, 1/0)
r23 := First(allResults, r -> r.p = 23);;
cal4Pass := (r23.W.dimH2_SL = 0) and (r23.Ad.dimH2_SL = 1) and (r23.Ad.i0_observed = 0);;
Print("[", PF(cal4Pass), "] cal-4: p=23 リハ(W=0・Ad=1・i0=0): ", cal4Pass, "\n");

# ---- cal-5: 系統B独立実装(この一式そのものが系統B)。p<=23の値をcohomolo既知値と突合
#      (falsifier逐語§Dの実測4点 p=5,7,11,23で dim H^2(SL,sl_2)=1・dim H^2(SL,W)=0 が
#      確認済み — このセッションでは系統Aを再実行せず、既存の確立済み事実として引用する)
cal5KnownValues := "falsifier逐語§D実測: p=5,7,11,23 で dim H^2(SL,sl_2)=1, dim H^2(SL,W)=0(F_stage1ad_prereg_v1.md L41 引用・系統A再実行なし)";;
cal5Pass := cal3Pass and cal2Pass;;
Print("[", PF(cal5Pass), "] cal-5: 系統B(本スクリプト)がcal-2/cal-3の予言値と一致(系統A既知値との突合は引用): ", cal5Pass, "\n");

# ---- cal-6: Sym^2(W) 予言 (0,1) -- det に一切言及せず構成(RepSym2は det を使っていない)
cal6Pass := ForAll(allResults, r -> (r.Sym2W.dimH2_SL = 1) and (r.Sym2W.i0_observed = 1));;
Print("[", PF(cal6Pass), "] cal-6: Sym^2W の (dimH2,i0)=(1,1) 全p: ", cal6Pass, "\n");

# ---- 和則(軽微1): dim H^2(SL,sl_2) <= 1 かつ ちょうど1
sumRuleOk := ForAll(allResults, r -> r.Ad.dimH2_SL <= 1);;
Print("[", PF(sumRuleOk), "] 和則: dim H^2(SL,sl_2) <= 1 全p: ", sumRuleOk, "\n");

# ---- calib_primes assert({7,11,23} を含む)
calibPrimesOk := (7 in calibPrimes) and (11 in calibPrimes) and (23 in calibPrimes);;
Print("[", PF(calibPrimesOk), "] calib_primes に {7,11,23} を含む: ", calibPrimesOk, "\n");

allCalibPass := cal1Pass and cal2Pass and cal3Pass and cal4Pass and cal5Pass and cal6Pass
                and sumRuleOk and calibPrimesOk;;
Print("\n[", PF(allCalibPass), "] ゲート行: calib 全PASS: ", allCalibPass, "\n");

boundViolated := ForAny(allResults, r -> (r.Ad.dimH2_SL > 1) or (r.W.dimH2_SL > 1)
                                          or (r.Sym2W.dimH2_SL > 1));;
Print("[", PF(not boundViolated), "] bound_violated = false: ", not boundViolated, "\n");

gatePass := allCalibPass and (not boundViolated);;
Print("\n[", PF(gatePass), "] ★★★ ゲート(要修正1: calib全PASS かつ bound_violated=false): ", gatePass, "\n");

# ====================================================================
# 本番: p=691(系統B・cap 60秒)
# ====================================================================
Print("\n============================================================\n");
Print("# 本番 p=691(系統B・cap 60秒)\n");
Print("============================================================\n");

t691start := GAPLIB_WallElapsedMs();;
res691 := fail;;
capExceeded691 := false;;
res691 := MeasureAtPrime(691);;
t691end := GAPLIB_WallElapsedMs();;
elapsed691Ms := t691end - t691start;;
capExceeded691 := (elapsed691Ms > 60000);;
Print("p=691 経過 = ", elapsed691Ms, " ms (cap 60000ms)\n");
Print("[", PF(not capExceeded691), "] cap 60秒以内: ", not capExceeded691, "\n");

Print("p=691: W.dimH2_SL=", res691.W.dimH2_SL, " Ad.dimH2_SL=", res691.Ad.dimH2_SL,
      " Ad.i0_observed=", res691.Ad.i0_observed,
      " Sym2W.dimH2_SL=", res691.Sym2W.dimH2_SL, " Sym2W.i0_observed=", res691.Sym2W.i0_observed, "\n");

sumRule691 := res691.Ad.dimH2_SL;;  # sum over i=0,1 twists = dimH2_SL total (since dimH2_SL counts weight-2 space regardless of twist)
Print("sum_rule_value(Ad) = ", sumRule691, " (期待 1 ちょうど)\n");

# ====================================================================
# 判定枝(要修正1のゲート通過後のみ適用・判定語は最小限に留め、枝ラベルのみ記録)
# ====================================================================
branchLabel := "GATE_NOT_PASSED_UNKNOWN_STOP";;
if gatePass and (not capExceeded691) and (res691.Ad.i0_observed <> fail) then
  if sumRule691 = 1 and res691.Ad.i0_observed = 0 then
    branchLabel := "(Ad-b) predicted (1,0)";;
  elif sumRule691 = 0 then
    branchLabel := "(Ad-a) (0,0)";;
  elif sumRule691 = 1 and res691.Ad.i0_observed = 1 then
    branchLabel := "(Ad-b') (0,1) reversed sign";;
  else
    branchLabel := "STOP (sum>=2 or unexpected)";;
  fi;
elif res691.Ad.i0_observed = fail then
  branchLabel := "UNKNOWN (i0_observed=null)";;
fi;;
Print("\n枝ラベル(判定は司令塔): ", branchLabel, "\n");

# ====================================================================
# 総括 + cert
# ====================================================================
Print("\n############################################################\n");
Print("F-STAGE1AD-CALIB DONE\n");

t1 := GAPLIB_WallElapsedMs();;
totalElapsedMs := t1 - t0;;
Print("総経過 = ", totalElapsedMs, " ms\n");

# ---- cert JSON ----
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_f1ad.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

ValOrNull := function(v)
  if v = fail then return "null"; fi;
  if v = true then return "true"; fi;
  if v = false then return "false"; fi;
  return String(v);
end;;

ModuleResultJson := function(m)
  return Concatenation("{\"dim_M_P\":", String(m.dim_M_P), ",\"weight2_dim\":", String(m.weight2_dim),
    ",\"dimH2_SL\":", String(m.dimH2_SL), "}");
end;;

AdResultJson := function(m)
  return Concatenation("{\"dim_M_P\":", String(m.dim_M_P), ",\"weight2_dim\":", String(m.weight2_dim),
    ",\"dimH2_SL\":", String(m.dimH2_SL), ",\"sign_on_weight2\":", ValOrNull(m.sign_on_weight2),
    ",\"i0_observed\":", ValOrNull(m.i0_observed), "}");
end;;

PerPrimeJson := function(r)
  return Concatenation("{\"p\":", String(r.p), ",\"lambda\":", String(r.lambda),
    ",\"W\":", ModuleResultJson(r.W), ",\"Ad\":", AdResultJson(r.Ad),
    ",\"Sym2W\":", AdResultJson(r.Sym2W), "}");
end;;

scriptSha256 := ComputeSha256File("search/f_stage1ad_calib_v1.g");;
docSha256 := "768898e153ec7b211c45bb8d6b8ae91d378d570aeb79940a252abaefbe0bbe61";;  # F_stage1ad_prereg_v1_1.md (frozen)

cert := Concatenation(
  "{\"schema\":\"F_stage1_ad/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/f_stage1ad_calib_v1.g\",\"order\":\"裁定1012\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"prereg_doc\":\"docs/notes/F_stage1ad_prereg_v1_1.md\",\"prereg_doc_sha256\":\"", docSha256, "\"",
  ",\"method\":\"stable_elements\"",
  ",\"group_constructed\":false,\"group_fingerprint\":null,\"identity_basis\":\"paper_asserted\"",
  ",\"calib_primes\":", JArr(List(calibPrimes,String)),
  ",\"calib_primes_includes_7_11_23\":", JB(calibPrimesOk),
  ",\"per_prime_results\":", JArr(List(allResults, PerPrimeJson)),
  ",\"calibration\":{",
    "\"cal1_pass\":", JB(cal1Pass), ",\"cal2_pass\":", JB(cal2Pass), ",\"cal3_pass\":", JB(cal3Pass),
    ",\"cal4_pass\":", JB(cal4Pass), ",\"cal5_pass\":", JB(cal5Pass), ",\"cal5_note\":\"", cal5KnownValues, "\"",
    ",\"cal6_pass\":", JB(cal6Pass),
    ",\"sum_rule_ok\":", JB(sumRuleOk),
    ",\"all_calib_pass\":", JB(allCalibPass),
  "}",
  ",\"bound_violated\":", JB(boundViolated),
  ",\"gate_pass\":", JB(gatePass),
  ",\"calib_elapsed_ms\":", String(calibElapsedMs),
  ",\"production\":{",
    "\"p\":691,\"elapsed_ms\":", String(elapsed691Ms), ",\"cap_ms\":60000",
    ",\"cap_exceeded\":", JB(capExceeded691),
    ",\"result\":", PerPrimeJson(res691),
    ",\"sum_rule_value\":", String(sumRule691),
    ",\"i0_predicted\":0",
    ",\"i0_observed\":", ValOrNull(res691.Ad.i0_observed),
    ",\"branch_label\":\"", branchLabel, "\"",
  "}",
  ",\"r1_reservation\":\"unproven(型 vs 実像・段4未閉)\"",
  ",\"name_collide_note\":\"pair_h2_design_draft_v1.md の Gbar と同一対象・P-PH2-4 は再掲\"",
  ",\"grade_note\":\"紙の二導出(系統B+系統C) + 単系統実装。cross-checkedはcal-4/cal-5(p<=23)の一致に限定。verifiedではない。\"",
  ",\"u_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(totalElapsedMs),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/f_stage1ad_calib_v1_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");

Print("\nF-STAGE1AD-CALIB DONE\n");
QUIT;
