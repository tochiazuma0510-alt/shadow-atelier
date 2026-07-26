# search/twincell-enum.g -- レベル 16 双子セル列挙機 v1(委嘱: 司令塔発注 2026-07-26)
#
# ── ツール仕様ヘッダ(2026-07-26 規約) ─────────────────────────────────────
# 入力:  なし(GAP 標準ライブラリのみ)。docs/manifest_twincell_v1.md が事前登録の正本。
# モード/触れてよいデータ範囲: 建造+アンカー較正(𝒞₈・𝒞₁₀)のみが無条件実行。
#        標的窓(𝒞₁₆・K^(8))の本走査は search/FIRE_twincell.auth の存在を機械的に検査し、
#        無ければ [LOCKED] を印字してスキップする(ドキュメント上の約束ではなく実行時ガード)。
# 出力スキーマ: gtsh-cert/twincell-v1(下記 WriteTwincellCert 参照) を
#        certificates/twincell/*.json へ書き出す。
# 検査する不変量: pb3_index(=|Q_L| または |G_n|)・n_ord・charming_set・
#        hexagon_free_certificate(candidate_total/h10_fail/h11_fail/generation_fail/shadow_total)・
#        (較正①のみ)marked factor map 全単射(x->x,y->y を送る具体的同型で GT shadow 集合を照合
#        -- 単なる |GT| 一致や部分群比較ではない。Sol 警告 6/罠 12 準拠)。
#
# 宇宙(事前登録・manifest_twincell_v1.md より, 変更しない):
#   C8  = pi^{-1}Gammabar(8)  = K^(4) (K-cong)  -- 較正①、既知 |GT|=4, F0=1
#   C10 = pi^{-1}Gammabar(10) = N_A (T-6)        -- 較正②、既知 |GT|=20 (=~F20)
#   C16 = pi^{-1}Gammabar(16)                    -- 標的(合同)、UNKNOWN、FIRE 封鎖
#   K8  = ker psi_8                              -- 標的(非合同)、既知飽和 |GT|=16、FIRE 封鎖
#
# 構成法(二系統、manifest sec. 構成法):
#   系統(a) 行列 mod L: Q_L := <Xbar,Ybar> <= SL(2,Z/L) / {+-I}、
#           Xbar=[[1,2],[0,1]], Ybar=[[1,0],[-2,1]] (Gamma(2) の標準自由生成元を mod L 還元)。
#   系統(b) D_n^3 埋め込み(既存 MakeGn, week3-battery-common.g -- K^(n) の正本構成、D1 (3.6)):
#           x=(r,s,s), y=(rs,r,rs) in D_n^3。C8 = K^(4) は n=4。K8 は MakeGn(8)。
#   較正①(manifest 特筆事項): C8 の二構成(mod-8 行列 vs D_4^3)の GT 集合が
#           marked factor map(x->x, y->y を送る具体的群同型)で全単射一致することを要求する。

SizeScreen([4096, 0]);;
startTime := Runtime();;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

# ================================================================================
# 系統(a): Q_L = <Xbar,Ybar> <= SL(2,Z/L)/{+-I} の直接構成
# 表現方式: 行列は [a,b,c,d] (mod L の整数4個, 行優先 [[a,b],[c,d]])。
# +-1 の同一視は「m と -m のうち整数キーが小さい方を代表元に取る」という正準化で実装する
# (Q8/Heis/P3 で使われている「自前で正準形を決めて BFS 閉包+左正則置換表現」パターンに
#  合わせた -- GAP の GF(q) 体演算は L が素数冪でない(8,10,16)場合に使えないための選択)。
MatModL := function(x, L) return ((x mod L) + L) mod L; end;;

MatMulL := function(m, n, L)
  local a,b,c,d,e,f,g,h;
  a:=m[1];; b:=m[2];; c:=m[3];; d:=m[4];;
  e:=n[1];; f:=n[2];; g:=n[3];; h:=n[4];;
  return [ MatModL(a*e+b*g, L), MatModL(a*f+b*h, L), MatModL(c*e+d*g, L), MatModL(c*f+d*h, L) ];
end;;

MatNegL := function(m, L) return [ MatModL(-m[1],L), MatModL(-m[2],L), MatModL(-m[3],L), MatModL(-m[4],L) ]; end;;

MatKeyInt := function(m, L) return ((m[1]*L + m[2])*L + m[3])*L + m[4]; end;;

# 罠(発見・修理 2026-07-26 事後デルタ対応中): 正準化は「入力を先に mod L で還元してから」
# 比較しないと、生の(未還元の)整数リテラル(例: 種生成元 Ym の -2)と、BFS 経由で既に
# 還元済みの同じ抽象元とで**異なる代表元**が選ばれる恐れがある(-2 と 14 は mod 16 で同じ値だが、
# 整数キー ((a*L+b)*L+c)*L+d は還元前後で異なる)。node 側の独立検算(kernel_certificate の
# generator_images 突合)がこれに依存するため、GAP・node 双方で「まず全エントリを mod L 還元
# してから比較する」に統一する(入力が既に還元済みでも冪等なので無害)。
MatCanonL := function(m, L)
  local mr, neg;
  mr := List(m, x -> MatModL(x, L));;
  neg := MatNegL(mr, L);
  if MatKeyInt(mr,L) <= MatKeyInt(neg,L) then return mr; else return neg; fi;
end;;

# BuildMatQuotient: BFS closure of <Xbar,Ybar> under the +-1 identification, then a left-regular
# permutation representation (same recipe as MakeQ8/MakeHeis/MakeP3 -- self-contained, no GAP
# GF(q)/ring-of-integers-mod-n library calls needed since we only require BFS + group law here).
# xySign lets the fixture builder inject a deliberately WRONG generator (罠(3.10)/(3.11) 型の
# 合成負例を作るため; 正常系では常に 1 を渡す).
BuildMatQuotient := function(L, ySign)
  local idm, Xm, Ym, Xinv, Yinv, gens, dict, idxDict, queue, qi, cur, g, nv, key,
        elements, n, i, RegOf, xperm, yperm, G;
  idm  := MatCanonL([1,0,0,1], L);
  Xm   := MatCanonL([1,2,0,1], L);
  Ym   := MatCanonL([1,0, ySign*(-2), 1], L);
  Xinv := MatCanonL([1,-2,0,1], L);
  Yinv := MatCanonL([1,0, ySign*2, 1], L);
  gens := [Xm, Xinv, Ym, Yinv];
  dict := NewDictionary(1, true);
  AddDictionary(dict, MatKeyInt(idm,L), true);
  queue := [idm];  qi := 1;
  while qi <= Length(queue) do
    cur := queue[qi];  qi := qi+1;
    for g in gens do
      nv := MatCanonL(MatMulL(g, cur, L), L);
      key := MatKeyInt(nv, L);
      if LookupDictionary(dict, key) = fail then
        AddDictionary(dict, key, true);
        Add(queue, nv);
      fi;
    od;
  od;
  elements := queue;
  n := Length(elements);
  idxDict := NewDictionary(1, true);
  for i in [1..n] do AddDictionary(idxDict, MatKeyInt(elements[i], L), i); od;
  RegOf := function(g0)
    local l, i2, prod, k2, idx;
    l := [];
    for i2 in [1..n] do
      prod := MatCanonL(MatMulL(g0, elements[i2], L), L);
      k2 := MatKeyInt(prod, L);
      idx := LookupDictionary(idxDict, k2);
      if idx = fail then Error("BuildMatQuotient: closure failure (not a group?) L=", L); fi;
      l[i2] := idx;
    od;
    return PermList(l);
  end;
  xperm := RegOf(Xm);;  yperm := RegOf(Ym);;
  G := Group(xperm, yperm);;
  if Size(G) <> n then
    Error("BuildMatQuotient: |Group(x,y)|=", Size(G), " != BFS closure count ", n, " for L=", L);
  fi;
  return rec(L:=L, x:=xperm, y:=yperm, c:=Identity(G), G:=G, order:=n,
             elements:=elements, xMat:=Xm, yMat:=Ym, matOfIdx:=elements);
end;;

MatToStrL := function(m)
  return Concatenation("[[",String(m[1]),",",String(m[2]),"],[",String(m[3]),",",String(m[4]),"]]");
end;;

# DnTripleAEStr: encode a D_n^3 element (a permutation built via MakeGn's tr()) as
# "[[a1,e1],[a2,e2],[a3,e3]]" -- the abstract (a,e) triple per factor (r^a s^e), using the SAME
# encoding week3-battery-common.g's DnElemToAE already defines. This is n-independent as ABSTRACT
# data (x=(r,s,s)=[[1,0],[0,1],[0,1]], y=(rs,r,rs)=[[1,1],[1,0],[1,1]] for every n) -- machine
# parseable JSON, used as the generative "kernel_certificate.generator_images" for D_n^3 windows.
DnTripleAEStr := function(perm, r, s, n)
  local i, ae, parts;
  parts := [];;
  for i in [1..3] do
    ae := DnElemToAE(compOfFix(perm, i, n), r, s, n);;
    Add(parts, Concatenation("[", String(ae[1]), ",", String(ae[2]), "]"));
  od;
  return Concatenation("[", JoinC(parts, ","), "]");
end;;

# KernelCertJson(qrec, pb3Index, xImgStr, yImgStr): the GENERATIVE kernel_certificate
# (falsifier 監査「事後デルタ」重大指摘への対応 -- 数値の重複+文章だけでなく、N を定義する
# psi: F2 ->> Q の生成元像そのもの(xImgStr/yImgStr、machine-parseable)と、それが本当に
# claimed pb3_index の群を生成する(=部分群でないことを確認する)検証データを両方含める。
# node 側はこの xImgStr/yImgStr を自前で構築した (G,X,Y) と突き合わせて独立に再検証する。
KernelCertJson := function(qrec, pb3Index, xImgStr, yImgStr)
  local genVerified;
  genVerified := (Size(Group(qrec.x, qrec.y)) = pb3Index);;
  return Concatenation(
    "\"kernel_certificate\":{\"kernel_scope\":\"PB3\",",
    "\"definition\":\"N = ker(psi: F2 ->> Q), psi(x)|->generator_images.x, psi(y)|->generator_images.y (Q per the construction field)\",",
    "\"generator_images\":{\"x\":\"", xImgStr, "\",\"y\":\"", yImgStr, "\"},",
    "\"verification\":{\"method\":\"Size(Group(generator_images.x,generator_images.y)) equals the claimed pb3_index -- confirms the given images GENERATE the full claimed quotient (not a proper subgroup, which would mean N is strictly larger than claimed)\",",
    "\"generation_verified\":", JB(genVerified), "},",
    "\"pb3_kernel_index\":", String(pb3Index), ",\"b3_kernel_index\":", String(6*pb3Index), "},");
end;;

# ================================================================================
# 共通ランナー: 与えられた qrec(x,y,G) について reduced-hexagon 全列挙を実行し、
# 結果 rec を返す(certificate 化は呼び出し側)。
# ================================================================================
RunWindow := function(label, qrec)
  local nOrd, charmingSet, derivedOrder, candidateTotalExpected, result, shadowSumCheck, t0, t1;
  Print("\n===== window ", label, ": |G|=", Size(qrec.G), " =====\n");
  nOrd := Lcm(Order(qrec.x), Order(qrec.y));;
  charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);;
  derivedOrder := Size(DerivedSubgroup(qrec.G));;
  candidateTotalExpected := Length(charmingSet) * derivedOrder;;
  Print("n_ord=", nOrd, " charming_set=", charmingSet, " derived_order=", derivedOrder,
        " candidate_total_expected=", candidateTotalExpected, "\n");
  t0 := Runtime();;
  result := EnumerateReducedHexagon(qrec, charmingSet);;
  t1 := Runtime();;
  Print("reduced hexagon: time_ms=", t1-t0, " candidate_total=", result.candidate_total,
        " h10_fail=", result.h10_fail, " h11_fail=", result.h11_fail,
        " generation_fail=", result.generation_fail, " shadow_total=", result.shadow_total, "\n");
  shadowSumCheck := (result.candidate_total - result.h10_fail - result.h11_fail - result.generation_fail
                      = result.shadow_total);;
  Print("[", PF(shadowSumCheck), "] shadow_total 引き算整合性チェック\n");
  return rec(label:=label, qrec:=qrec, nOrd:=nOrd, charmingSet:=charmingSet, derivedOrder:=derivedOrder,
             candidateTotalExpected:=candidateTotalExpected, result:=result, shadowSumOk:=shadowSumCheck,
             pb3_index:=Size(qrec.G));
end;;

# WriteTwincellCertFull: writes a gtsh-cert/twincell-v1 certificate with an explicit isolatedJson
# value (a JSON scalar string, e.g. "\"UNKNOWN\"" or "true"/"false") -- used for target windows
# once settled/isolated has actually been computed (falsifier/司令塔 発射指示: settled/isolated・
# kernel 証明書 も本走査の観測量に含める).
WriteTwincellCertFull := function(path, label, construction, run, extra, isolatedJson)
  local genDetailJson, gd, gtShadowsJson, sh, s;
  genDetailJson := [];;
  for gd in run.result.generation_detail do
    Add(genDetailJson, Concatenation("{\"m\":", String(gd.m), ",\"f_word\":", WordToJson(gd.f_word),
        ",\"pass\":", JB(gd.pass), ",\"stage\":\"", gd.stage, "\"}"));
  od;
  gtShadowsJson := [];;
  for sh in run.result.shadows do
    Add(gtShadowsJson, Concatenation("{\"m\":", String(sh.m), ",\"f_word\":", WordToJson(sh.word), "}"));
  od;
  s := Concatenation(
    "{\"schema\":\"gtsh-cert/twincell-v1\",",
    "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/twincell-enum.g\",\"date\":\"2026-07-26\"},",
    "\"window_id\":\"", label, "\",",
    "\"construction\":\"", construction, "\",",
    "\"universe\":{\"pb3_index\":", String(run.pb3_index), ",\"b3_points\":", String(6*run.pb3_index),
    ",\"n_ord\":", String(run.nOrd), ",\"charming_set\":", JArr(List(run.charmingSet,String)),
    ",\"derived_order\":", String(run.derivedOrder), ",\"candidate_total\":", String(run.candidateTotalExpected), "},",
    "\"c_in_N\":true,\"evaluation_mode\":\"quotient_ok\",",
    "\"hexagon_free_certificate\":{\"candidate_total\":", String(run.result.candidate_total),
    ",\"h10_fail\":", String(run.result.h10_fail), ",\"h11_fail\":", String(run.result.h11_fail),
    ",\"generation_fail\":", String(run.result.generation_fail),
    ",\"shadow_total\":", String(run.result.shadow_total), "},",
    "\"shadow_sum_identity\":", JB(run.shadowSumOk), ",",
    "\"generation_detail\":", JArr(genDetailJson), ",",
    "\"gt_shadows_observed\":", JArr(gtShadowsJson), ",",
    extra, "\"isolated\":", isolatedJson, "}");;
  WriteFile(path, s);;
  Print("wrote ", path, "\n");
end;;

# WriteTwincellCert: thin wrapper, isolated always "UNKNOWN" (calibration windows -- settled/isolated
# not computed there, out of scope for this manifest's calibration windows).
WriteTwincellCert := function(path, label, construction, run, extra)
  WriteTwincellCertFull(path, label, construction, run, extra, "\"UNKNOWN\"");
end;;

# ================================================================================
# settled/isolated(week1-定義ノート.md §2, Thm 3.10 の定義に厳密に従う):
# settled: ker(T_{m,f}) = N -- 同値に、induced map T_{m,f}: x|->x^u, y|->f^-1 y^u f が
# G=Q/N 自身の自己同型(全単射)であること。これは GroupHomomorphismByImages(G,G,[x,y],
# [targetX,targetY]) を構成し IsBijective で判定すれば計算できる(Aut(G) の全列挙は不要 --
# 較正①②で使った marked-factor-map の仕組みと全く同じ機構の再利用)。
# isolated: 全 shadow が settled ⇒ GT(N) = GTSh(N,N) は有限群(Prop 3.14 系)。
# ================================================================================
ComputeSettledIsolated := function(qrec, result)
  local settledDetail, sh, isSettled, m, u, targetX, targetY, hom, settledCount;
  settledDetail := [];;  settledCount := 0;;
  for sh in result.shadows do
    m := sh.m;;  u := 2*m+1;;
    targetX := qrec.x^u;;
    targetY := AbstractProd([sh.f^-1, qrec.y^u, sh.f]);;   # paper "f^-1 y^u f" -> AbstractProd convention
    hom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y], [targetX, targetY]);;
    if hom = fail then isSettled := false;
    else isSettled := IsBijective(hom); fi;
    if isSettled then settledCount := settledCount + 1; fi;
    Add(settledDetail, rec(m:=m, f_word:=sh.word, settled:=isSettled));
  od;
  return rec(settled_detail:=settledDetail, settled_count:=settledCount,
             total:=Length(result.shadows),
             isolated:=(Length(result.shadows) > 0 and settledCount = Length(result.shadows)));
end;;

SettledDetailToJson := function(si)
  local items, sd;
  items := [];;
  for sd in si.settled_detail do
    Add(items, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
        ",\"settled\":", JB(sd.settled), "}"));
  od;
  return JArr(items);
end;;

# ================================================================================
# マーク付き因子写像による全単射照合(較正①・Sol 警告「部分群比較でなく marked factor map」)
# G1 の生成元 (x1,y1) から G2 の生成元 (x2,y2) への marked hom を構成し、全単射性と、
# 両側 GT-shadow 集合が (m, f) |-> (m, phi(f)) で完全一致することを検査する。
# 罠回避: これは指数の一致(|G1|=|G2|)や単なる |GT| の数値一致では代替できない
# (Sol 警告6件・罠12件 -- 指数一致を settled 証明に使わない、の類推)。
# ================================================================================
CheckMarkedBijection := function(run1, run2)
  local hom, bijective, phiShadows, matched, sh, phiF, foundIdx, i, allMatched,
        shadowSet2, mismatchDetail;
  hom := GroupHomomorphismByImages(run1.qrec.G, run2.qrec.G,
           [run1.qrec.x, run1.qrec.y], [run2.qrec.x, run2.qrec.y]);;
  if hom = fail then
    return rec(ok:=false, reason:="marked hom did not construct (images inconsistent with relations)");
  fi;
  bijective := IsBijective(hom);;
  if not bijective then
    return rec(ok:=false, reason:="marked hom constructed but NOT bijective", hom_exists:=true);
  fi;
  # each shadow (m,f) of run1 must map, under phi, to a shadow (m,phi(f)) actually present in run2
  matched := 0;;  mismatchDetail := [];;
  for sh in run1.result.shadows do
    phiF := Image(hom, sh.f);;
    foundIdx := fail;;
    for i in [1..Length(run2.result.shadows)] do
      if run2.result.shadows[i].m = sh.m and run2.result.shadows[i].f = phiF then foundIdx := i; break; fi;
    od;
    if foundIdx <> fail then matched := matched + 1;
    else Add(mismatchDetail, rec(m:=sh.m, f_word:=sh.word)); fi;
  od;
  allMatched := (matched = Length(run1.result.shadows)) and (matched = Length(run2.result.shadows))
                and (Length(run1.result.shadows) = Length(run2.result.shadows));
  return rec(ok:=allMatched, hom_exists:=true, bijective_group_hom:=bijective,
             shadow1_count:=Length(run1.result.shadows), shadow2_count:=Length(run2.result.shadows),
             matched:=matched, mismatch_count:=Length(mismatchDetail));
end;;

# ================================================================================
# 較正① 𝒞₈ = K^(4): 系統(a) 行列 mod 8 と 系統(b) D_4^3 埋め込み(MakeGn(4))
# ================================================================================
Print("\n########## CALIBRATION 1: C8 = K^(4), two constructions ##########\n");
c8mat := BuildMatQuotient(8, 1);;
Print("C8 matrix-mod-8: |Q_8| = ", c8mat.order, " (expect 32, per pb3_index in K4.v1.json)\n");
qrecC8mat := rec(x:=c8mat.x, y:=c8mat.y, c:=c8mat.c, G:=c8mat.G);;
runC8mat := RunWindow("C8_matrix_mod8", qrecC8mat);;

gn4 := MakeGn(4);;
Print("C8 D4^3 (MakeGn(4)): |G_4| = ", Size(gn4.G), " (expect 32)\n");
qrecC8d4 := rec(x:=gn4.x, y:=gn4.y, c:=Identity(gn4.G), G:=gn4.G);;
runC8d4 := RunWindow("C8_D4cubed", qrecC8d4);;

calib1 := CheckMarkedBijection(runC8mat, runC8d4);;
Print("\n[", PF(calib1.ok), "] CALIBRATION 1 (marked factor map bijection, matrix-mod-8 <-> D4^3): ",
      "shadow1=", calib1.shadow1_count, " shadow2=", calib1.shadow2_count, " matched=", calib1.matched, "\n");
calib1KnownValueOk := (runC8mat.result.shadow_total = 4) and (runC8d4.result.shadow_total = 4);;
Print("[", PF(calib1KnownValueOk), "] CALIBRATION 1 known value: both constructions give |GT|=4 (Thm 4.3)\n");

# ================================================================================
# 較正② 𝒞₁₀ = N_A: 系統(a) 行列 mod 10。既知値 |GT|=20 (≅F20, 裁定16) の再現に加え、
# falsifier 監査(docs/notes/反証前哨_双子セル.md §2)の要求により、既存 A5 置換構成
# (certificates/A1.v2.json のマーキング, week3-battery-A1.g 系統)との marked factor map
# 全単射を較正①と同水準で追加する(数値一致のみでは「kernel 主張」の証明にならない
# -- CLAUDE.md 鉄則3・Sol 警告6件・罠12件)。A5 の構成はここで独立に再構築する
# (search/week3-battery-A1.g を import せず、A1.v2.json 記載の marking を直に転記 -- これは
# spec-disclosed な既知データの再利用であり、探索器コードの import ではない)。
# ================================================================================
Print("\n########## CALIBRATION 2: C10 = N_A, matrix-mod-10 vs A5 permutation construction ##########\n");
c10mat := BuildMatQuotient(10, 1);;
Print("C10 matrix-mod-10: |Q_10| = ", c10mat.order, " (expect 60, matches |A5|)\n");
qrecC10mat := rec(x:=c10mat.x, y:=c10mat.y, c:=c10mat.c, G:=c10mat.G);;
runC10mat := RunWindow("C10_matrix_mod10", qrecC10mat);;
calib2KnownValueOk := (runC10mat.result.shadow_total = 20);;
Print("[", PF(calib2KnownValueOk), "] CALIBRATION 2 known value: matrix-mod-10 gives |GT|=", runC10mat.result.shadow_total, " (expect 20)\n");

# A5 permutation construction (marking verbatim from certificates/A1.v2.json / week3-battery-A1.g)
A5Xhat := (1,3,2,4,5);;  A5Yhat := (1,3,4,5,2);;
A5grp := Group(A5Xhat, A5Yhat);;
qrecA5 := rec(x:=A5Xhat, y:=A5Yhat, c:=(), G:=A5grp);;
runA5 := RunWindow("C10_A5_permutation", qrecA5);;

calib2Bij := CheckMarkedBijection(runC10mat, runA5);;
Print("\n[", PF(calib2Bij.ok), "] CALIBRATION 2 (marked factor map bijection, matrix-mod-10 <-> A5 permutation): ",
      "shadow1=", calib2Bij.shadow1_count, " shadow2=", calib2Bij.shadow2_count, " matched=", calib2Bij.matched, "\n");

# A5-CONV 適合テスト(docs/week1-定義ノート.md §1.5.4, PU-F11 と同一判定式)を twincell 固有の
# 行列 mod 10 構成に対して直接実行する(falsifier 軽微指摘6への対応 -- 既存 PSL 系列からの
# 流用ではなく、C10 matrix -> A5 の marked hom を経由した専用チェック)。
calib2ConvHom := GroupHomomorphismByImages(qrecC10mat.G, A5grp, [qrecC10mat.x, qrecC10mat.y], [A5Xhat, A5Yhat]);;
a5ConvOk := false;;
if calib2ConvHom <> fail then
  evYXinvMat := AbstractProd([qrecC10mat.y, qrecC10mat.x^-1]);;
  evYXinvA5 := Image(calib2ConvHom, evYXinvMat);;
  a5ConvOk := (evYXinvA5 = (1,2,4));;
fi;
Print("[", PF(a5ConvOk), "] A5-CONV (twincell 固有, C10 matrix-mod-10 経由): ev(y x^-1) mapped into A5 = ",
      evYXinvA5, " (expect (1 2 4))\n");

# ================================================================================
# 合成負例 fixture(manifest 発射条件: 既知値をわざと壊した証明書が FAIL すること)
#
# 第一案(Ybar の符号反転, ySign=-1)は不採用として記録する: 実行してみると |Q_8'|=32・
# shadow_total=4・D4^3 との marked bijection も成立し(下記 BONUS 参照)、これは
# 「壊れていない」正しい結果だった(符号反転は Gamma(2) の別の自由生成対を与えるだけで、
# K^(4) の別実現になっている -- 数学的には興味深い頑健性の観測だが、負例としては失格)。
# 正しい負例として、level を取り違えた場合(L=6, C8 のつもりで書き間違えた誤り)を採用する:
# |Q_6| は |Q_8|=32 と一致せず(BFS 閉包の位数が異なる)、marked bijection も group order の
# 時点で崩れる -- これは実際に「既知値(|GT(K^(4))|=4 との一致・D4^3 との同型)」を壊す。
# ================================================================================
Print("\n########## NEGATIVE FIXTURE: mistaken level L=6 in place of C8's L=8 ##########\n");
c8matBad := BuildMatQuotient(6, 1);;
Print("mistaken-level matrix (L=6): |Q_6| = ", c8matBad.order, " (should NOT equal |Q_8|=32)\n");
qrecC8matBad := rec(x:=c8matBad.x, y:=c8matBad.y, c:=c8matBad.c, G:=c8matBad.G);;
runC8matBad := RunWindow("C8_matrix_WRONG_LEVEL6_fixture", qrecC8matBad);;
calibBad := CheckMarkedBijection(runC8matBad, runC8d4);;
negFixtureDetectsCorruption := (not calibBad.ok) or (runC8matBad.result.shadow_total <> 4)
                                 or (runC8matBad.pb3_index <> runC8d4.pb3_index);;
Print("[", PF(negFixtureDetectsCorruption), "] NEGATIVE FIXTURE correctly rejected (bijection ok=",
      calibBad.ok, ", shadow_total=", runC8matBad.result.shadow_total, " (expect <>4 or order mismatch vs D4^3, |Q_6|=",
      runC8matBad.pb3_index, " vs |G_4|=", runC8d4.pb3_index, ")\n");
if not negFixtureDetectsCorruption then
  Print("  [ANOMALY] negative fixture failed to be detected as wrong -- report to commander immediately\n");
fi;

# ---- BONUS(参考記録・要件外): Ybar 符号反転版は D4^3 と正しく bijection する(頑健性の観測) ----
Print("\n---- BONUS (not a fixture, informational): Ybar-sign-flip variant of C8 ----\n");
c8matSignFlip := BuildMatQuotient(8, -1);;
qrecC8matSignFlip := rec(x:=c8matSignFlip.x, y:=c8matSignFlip.y, c:=c8matSignFlip.c, G:=c8matSignFlip.G);;
runC8matSignFlip := RunWindow("C8_matrix_mod8_Ybar_signflip_BONUS", qrecC8matSignFlip);;
calibSignFlip := CheckMarkedBijection(runC8matSignFlip, runC8d4);;
Print("[INFO] Ybar-sign-flip variant: |Q_8|=", runC8matSignFlip.pb3_index, " shadow_total=",
      runC8matSignFlip.result.shadow_total, " marked-bijection-with-D4^3 ok=", calibSignFlip.ok,
      " (both constructions still realize K^(4) -- NOT used as the negative fixture)\n");

# ================================================================================
# FIRE LOCK: 標的窓(C16 行列 mod 16・K^(8) = MakeGn(8))の本走査は
# search/FIRE_twincell.auth の存在でのみ解錠する(mechanical guard、e2c6-sweep.g と同じ作法)。
# ================================================================================
fireLockPath := "search/FIRE_twincell.auth";;
fireUnlocked := IsExistingFile(fireLockPath);;
# 較正③(falsifier 監査 §3b・重大指摘への対応): K^(8) の既知値 |GT|=16 (Thm 4.3/5.3,
# 2^(2*alpha-2), alpha=3) を、印字コメントのみでなく pass/fail 判定変数として登録する。
# FIRE ロック中は「まだ判定できない(標的窓を走らせていない)」ことを明示するため
# calib3Status := "LOCKED" とし、calib3KnownValueOk は真偽値ではなく明示的に未定(fail)とする
# -- これにより calibJson・SUMMARY のどちらでも「ロック中は判定不能」と「判定して不一致」の
# 区別が機械的に付く(事前登録された既知値が実行コードから断線したまま発射されることを防ぐ)。
calib3Status := "LOCKED";;
calib3KnownValueOk := fail;;
calib3ObservedShadowTotal := fail;;
Print("\n########## TARGET WINDOWS (C16 matrix-mod-16, K^(8)=MakeGn(8)) ##########\n");
if not fireUnlocked then
  Print("[LOCKED] ", fireLockPath, " not found -- target window main sweep SKIPPED per manifest_twincell_v1.md.\n");
  Print("[LOCKED] Only calibration windows (C8, C10) and fixtures were executed this run.\n");
  Print("[LOCKED] CALIBRATION 3 (K^(8) known value |GT|=16) NOT YET RUN -- status=LOCKED, not a PASS.\n");
else
  Print("[UNLOCKED] ", fireLockPath, " found -- running target window main sweep.\n");
  c16mat := BuildMatQuotient(16, 1);;
  Print("C16 matrix-mod-16: |Q_16| = ", c16mat.order, "\n");
  qrecC16mat := rec(x:=c16mat.x, y:=c16mat.y, c:=c16mat.c, G:=c16mat.G);;
  runC16mat := RunWindow("C16_matrix_mod16", qrecC16mat);;
  c16Settled := ComputeSettledIsolated(qrecC16mat, runC16mat.result);;
  Print("C16 settled: ", c16Settled.settled_count, "/", c16Settled.total,
        " shadows settled; isolated=", c16Settled.isolated, "\n");
  WriteTwincellCertFull("certificates/twincell/C16.matrix.v1.json", "C16_matrix_mod16",
    Concatenation("Q_16 = <Xbar,Ybar> <= SL(2,Z/16)/{+-I}, Xbar=", MatToStrL(c16mat.xMat),
                  ", Ybar=", MatToStrL(c16mat.yMat)),
    runC16mat,
    Concatenation(
      KernelCertJson(qrecC16mat, runC16mat.pb3_index, MatToStrL(c16mat.xMat), MatToStrL(c16mat.yMat)),
      "\"settled_count\":", String(c16Settled.settled_count),
      ",\"settled_total\":", String(c16Settled.total),
      ",\"settled_detail\":", SettledDetailToJson(c16Settled), ","),
    JB(c16Settled.isolated));

  gn8 := MakeGn(8);;
  Print("K^(8) (MakeGn(8)): |G_8| = ", Size(gn8.G), " (expect saturated |GT|=16 per Thm 5.3)\n");
  qrecK8 := rec(x:=gn8.x, y:=gn8.y, c:=Identity(gn8.G), G:=gn8.G);;
  runK8 := RunWindow("K8_MakeGn8", qrecK8);;

  # ---- CALIBRATION 3: K^(8) known value |GT|=16 (Thm 4.3/5.3, alpha=3, 2^(2*3-2)=16) ----
  calib3Status := "RAN";;
  calib3ObservedShadowTotal := runK8.result.shadow_total;;
  calib3KnownValueOk := (calib3ObservedShadowTotal = 16);;
  Print("[", PF(calib3KnownValueOk), "] CALIBRATION 3 known value: K^(8) gives |GT|=",
        calib3ObservedShadowTotal, " (expect 16, Thm 4.3/5.3 alpha=3)\n");
  if not calib3KnownValueOk then
    Print("  [ANOMALY] CALIBRATION 3 MISMATCH -- K^(8) observed shadow_total != 16, report to commander immediately\n");
  fi;

  k8Settled := ComputeSettledIsolated(qrecK8, runK8.result);;
  Print("K8 settled: ", k8Settled.settled_count, "/", k8Settled.total,
        " shadows settled; isolated=", k8Settled.isolated, "\n");
  WriteTwincellCertFull("certificates/twincell/K8.dncubed.v1.json", "K8_MakeGn8",
    "K^(8) = Im(psi_8) <= D_8^3, x=(r,s,s), y=(rs,r,rs) (D1 (3.1)/(3.6))",
    runK8,
    Concatenation(
      KernelCertJson(qrecK8, runK8.pb3_index,
        DnTripleAEStr(gn8.x, gn8.r, gn8.s, 8), DnTripleAEStr(gn8.y, gn8.r, gn8.s, 8)),
      "\"settled_count\":", String(k8Settled.settled_count),
      ",\"settled_total\":", String(k8Settled.total),
      ",\"settled_detail\":", SettledDetailToJson(k8Settled), ","),
    JB(k8Settled.isolated));
fi;

# ================================================================================
# 証明書書き出し(較正分)
# ================================================================================
WriteTwincellCert("certificates/twincell/C8.matrix.v1.json", "C8_matrix_mod8",
  Concatenation("Q_8 = <Xbar,Ybar> <= SL(2,Z/8)/{+-I}, Xbar=", MatToStrL(c8mat.xMat),
                ", Ybar=", MatToStrL(c8mat.yMat)),
  runC8mat, KernelCertJson(qrecC8mat, runC8mat.pb3_index, MatToStrL(c8mat.xMat), MatToStrL(c8mat.yMat)));

WriteTwincellCert("certificates/twincell/C8.d4cubed.v1.json", "C8_D4cubed",
  "K^(4) = Im(psi_4) <= D_4^3, x=(r,s,s), y=(rs,r,rs) (D1 (3.1)/(3.6))",
  runC8d4, KernelCertJson(qrecC8d4, runC8d4.pb3_index,
    DnTripleAEStr(gn4.x, gn4.r, gn4.s, 4), DnTripleAEStr(gn4.y, gn4.r, gn4.s, 4)));

WriteTwincellCert("certificates/twincell/C10.matrix.v1.json", "C10_matrix_mod10",
  Concatenation("Q_10 = <Xbar,Ybar> <= SL(2,Z/10)/{+-I}, Xbar=", MatToStrL(c10mat.xMat),
                ", Ybar=", MatToStrL(c10mat.yMat)),
  runC10mat, KernelCertJson(qrecC10mat, runC10mat.pb3_index, MatToStrL(c10mat.xMat), MatToStrL(c10mat.yMat)));

WriteTwincellCert("certificates/twincell/C10.a5permutation.v1.json", "C10_A5_permutation",
  "N_A = pi^{-1}(ker(F2 ->> A5)), marking verbatim from certificates/A1.v2.json / week3-battery-A1.g: X=(1,3,2,4,5), Y=(1,3,4,5,2)",
  runA5, KernelCertJson(qrecA5, runA5.pb3_index, String(A5Xhat), String(A5Yhat)));

WriteTwincellCert("certificates/twincell/C8.matrix.v1.WRONG_LEVEL6_fixture.json", "C8_matrix_WRONG_LEVEL6_fixture",
  Concatenation("(NEGATIVE FIXTURE -- mistaken level L=6 in place of C8's L=8) Xbar=", MatToStrL(c8matBad.xMat),
                ", Ybar=", MatToStrL(c8matBad.yMat)),
  runC8matBad, KernelCertJson(qrecC8matBad, runC8matBad.pb3_index, MatToStrL(c8matBad.xMat), MatToStrL(c8matBad.yMat)));

WriteTwincellCert("certificates/twincell/C8.matrix.v1.Ybar_signflip_BONUS.json", "C8_matrix_mod8_Ybar_signflip_BONUS",
  Concatenation("(参考記録・要件外 -- 負例ではない) Xbar=", MatToStrL(c8matSignFlip.xMat),
                ", Ybar(sign flipped)=", MatToStrL(c8matSignFlip.yMat)),
  runC8matSignFlip, KernelCertJson(qrecC8matSignFlip, runC8matSignFlip.pb3_index,
    MatToStrL(c8matSignFlip.xMat), MatToStrL(c8matSignFlip.yMat)));

# calibration_3 JSON scalars (LOCKED vs RAN -- computed explicitly, not via a ternary idiom,
# since GAP string concatenation needs plain string values here)
if calib3Status = "LOCKED" then
  calib3KnownValueOkJson := "\"N/A_LOCKED\"";;
  calib3ObservedShadowTotalJson := "null";;
  calib3OkJson := "\"LOCKED\"";;
else
  calib3KnownValueOkJson := JB(calib3KnownValueOk);;
  calib3ObservedShadowTotalJson := String(calib3ObservedShadowTotal);;
  calib3OkJson := JB(calib3KnownValueOk);;
fi;

calibJson := Concatenation(
  "{\"schema\":\"gtsh-cert/twincell-calib-v1\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/twincell-enum.g\",\"date\":\"2026-07-26\"},",
  "\"calibration_1\":{\"ok\":", JB(calib1.ok),
  ",\"known_value_ok\":", JB(calib1KnownValueOk),
  ",\"shadow1_count\":", String(calib1.shadow1_count),
  ",\"shadow2_count\":", String(calib1.shadow2_count),
  ",\"matched\":", String(calib1.matched),
  ",\"method\":\"marked_factor_map (GroupHomomorphismByImages x->x,y->y; IsBijective; per-shadow image match)\"},",
  "\"calibration_2\":{\"known_value_ok\":", JB(calib2KnownValueOk),
  ",\"observed_shadow_total\":", String(runC10mat.result.shadow_total),
  ",\"expected\":20",
  ",\"bijection_ok\":", JB(calib2Bij.ok),
  ",\"bijection_shadow1_count\":", String(calib2Bij.shadow1_count),
  ",\"bijection_shadow2_count\":", String(calib2Bij.shadow2_count),
  ",\"bijection_matched\":", String(calib2Bij.matched),
  ",\"bijection_method\":\"marked_factor_map (GroupHomomorphismByImages x->x,y->y vs A5 permutation construction, certificates/A1.v2.json marking); IsBijective; per-shadow image match\"",
  ",\"a5_conv_ok\":", JB(a5ConvOk),
  ",\"a5_conv_note\":\"ev(y x^-1) transported via the C10-matrix->A5 marked hom, checked = (1 2 4) per docs/week1-定義ノート.md §1.5.4\"",
  ",\"ok\":", JB(calib2KnownValueOk and calib2Bij.ok and a5ConvOk), "},",
  "\"calibration_3\":{\"status\":\"", calib3Status, "\"",
  ",\"known_value_ok\":", calib3KnownValueOkJson,
  ",\"observed_shadow_total\":", calib3ObservedShadowTotalJson,
  ",\"expected\":16,\"note\":\"K^(8)=MakeGn(8), Thm 4.3/5.3 alpha=3, 2^(2*alpha-2)=16; LOCKED until search/FIRE_twincell.auth is issued by the commander\"",
  ",\"ok\":", calib3OkJson, "},",
  "\"negative_fixture\":{\"description\":\"mistaken level L=6 in place of C8's L=8 (self-consistency of THIS certificate is not the same as passing the negative-fixture check -- see calibration_summary/negative_fixture.correctly_rejected)\",",
  "\"correctly_rejected\":", JB(negFixtureDetectsCorruption),
  ",\"bad_bijection_ok\":", JB(calibBad.ok),
  ",\"bad_pb3_index\":", String(runC8matBad.pb3_index),
  ",\"bad_shadow_total\":", String(runC8matBad.result.shadow_total), "},",
  "\"bonus_ybar_signflip_not_a_fixture\":{\"pb3_index\":", String(runC8matSignFlip.pb3_index),
  ",\"shadow_total\":", String(runC8matSignFlip.result.shadow_total),
  ",\"marked_bijection_with_d4cubed_ok\":", JB(calibSignFlip.ok), "},",
  "\"fire_lock\":{\"path\":\"", fireLockPath, "\",\"unlocked\":", JB(fireUnlocked), "}",
  "}");;
WriteFile("certificates/twincell/calibration_summary.v1.json", calibJson);;
Print("\nwrote certificates/twincell/calibration_summary.v1.json\n");

Print("\n===== SUMMARY =====\n");
Print("[", PF(calib1.ok and calib1KnownValueOk), "] CALIBRATION 1 (C8=K^(4)) overall (marked bijection + known value)\n");
Print("[", PF(calib2KnownValueOk and calib2Bij.ok and a5ConvOk),
      "] CALIBRATION 2 (C10=N_A) overall (known value + marked bijection vs A5 + A5-CONV)\n");
if calib3Status = "LOCKED" then
  Print("[LOCKED] CALIBRATION 3 (K^(8) known value |GT|=16) -- NOT a PASS, target window not yet run\n");
else
  Print("[", PF(calib3KnownValueOk), "] CALIBRATION 3 (K^(8) known value |GT|=16) overall\n");
fi;
Print("[", PF(negFixtureDetectsCorruption), "] NEGATIVE FIXTURE correctly rejected\n");
Print("fire_lock unlocked = ", fireUnlocked, "\n");

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
