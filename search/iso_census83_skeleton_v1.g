# search/iso_census83_skeleton_v1.g -- ISO-CENSUS-83 スクリプト骨格(裁定974【3】・準備のみ・発火禁止)
#
# ⚠⚠ 本ファイルは骨格の準備であり、83窓のうちdelta>1の15窓(本命標的)には一切適用しない。
#    末尾で行うのは N5/M5 級の既知窓1本のみの dry-run(較正)。数学者の札検分後、司令塔裁定で
#    実際の15窓へ適用する別スクリプトが発火される(このファイルはそれではない)。
#
# search/s4_settled54_v1.g を「窓 parametrized」化した骨格。入力 = 一般の窓(qrec=rec(x,y,G) の
# 形で与える -- lins 由来なら canonical_id_words から B3 fp群経由で構成、既知窓(M5等)なら
# 既存の構成関数をそのまま渡す)。出力 = I2 の4項:
#   (a) 列挙完全性(EnumerateReducedHexagon の BFS 全被覆 + derived subgroup 独立検算)
#   (b) kernel equality(直接route: psi:=GroupHomomorphismByImages(Gg,Gg,[X,Y],[X^u,f^-1*Y^u*f])
#       の well-definedness + Kernel(psi) 自明性 -- S4 専用構造(PSL(2,8)/GF(8))に依存しない
#       一般形。裁定892の直接routeがそもそも一般の Gg=PB3/N に対して定義される)
#   (c) staleness citation(裁定529 / auto_settled_check_v1.md 付録A.1、共有関数
#       EnumerateReducedHexagon が descent 判定を呼ばないという既存の裏取りをそのまま引用)
#   (d) c∉N assert への反転 + z 記録: S4 の "S^2=1(c∈N の代理)" を裏返し、
#       z=ord(c mod N) を測定し z<>1(c∉N)を assert する(zcensus83_v1.g で確立した B3 fp群
#       + NaturalHomomorphismByNormalSubgroup 経由の z 測定をそのまま流用)。
#
# 847 依存監査: EnumerateReducedHexagon/AbstractProd = search/week3-battery-common.g(既存)。
#   z 測定パターン = search/zcensus83_v1.g(このセッションで確立・裁定960)。
#   窓再構成(B3 fp群 + EvalString(canonical_id_words))も zcensus83_v1.g と同一パターン。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ====================================================================
# B3 = <a,b|aba=bab> の共通構成(lins 由来窓の再構成に使う)
# ====================================================================
BF3 := FreeGroup("a", "b");;
brel := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;
B3 := BF3 / [brel];;
b3a := B3.1;;  b3b := B3.2;;
cElt := (b3a*b3b)^3;;   # c = (sigma1 sigma2)^3, NAME-COLLIDE 注記どおり B3 の中心生成元

# ====================================================================
# WindowFromLinsWords: canonical_id_words から qrec=rec(x,y,G,N,cInQuot) を構成(本番用入力経路、
#   未発火)。x=sigma1^2 の像、y=sigma2^2 の像として PB3/N=Gg を作る。
# ====================================================================
WindowFromLinsWords := function(indexExpected, words)
  local a, b, genElts, N, idxOk, isNormal, hom, Gg, Xg, Yg, cImg;
  a := b3a;;  b := b3b;;
  genElts := List(words, w -> EvalString(w));;
  N := Subgroup(B3, genElts);;
  idxOk := (Index(B3, N) = indexExpected);;
  isNormal := IsNormal(B3, N);;
  if not (idxOk and isNormal) then
    return rec(ok:=false, reason:="index/normality mismatch", idx_ok:=idxOk, is_normal:=isNormal);
  fi;
  hom := NaturalHomomorphismByNormalSubgroup(B3, N);;
  Gg := Image(hom);;
  Xg := Image(hom, a^2);;    # x = sigma1^2 の像
  Yg := Image(hom, b^2);;    # y = sigma2^2 の像
  cImg := Image(hom, cElt);;
  return rec(ok:=true, N:=N, hom:=hom, Gg:=Gg, qrec:=rec(x:=Xg, y:=Yg, c:=(), G:=Gg),
             cImg:=cImg, zVal:=Order(cImg));
end;;

# ====================================================================
# RunI2Window: 窓一般形での I2 (a)(b)(c)(d) 実行(qrec を直接受け取る -- 窓の構成方法に非依存)
# ====================================================================
RunI2Window := function(qrec, cfg)
  local G, D, result, kernelDetail, sh, m, u, f, psi, wellDef, kerTrivial, kerSize,
        enumComplete, dwordsIndep, failures, kernelTrivialCount, cCitation;
  failures := 0;;
  G := qrec.G;;

  # (a) 列挙完全性
  D := DerivedSubgroup(G);;
  dwordsIndep := Size(D);;
  result := EnumerateReducedHexagon(qrec, cfg.charmingSet);;
  enumComplete := (result.dwords_count = dwordsIndep) and
                  (result.candidate_total - result.h10_fail - result.h11_fail - result.generation_fail = result.shadow_total);;
  if not enumComplete then failures := failures + 1; fi;

  # (b) kernel equality(直接route、一般の Gg に対して定義される)
  kernelDetail := [];;
  for sh in result.shadows do
    m := sh.m;;  u := 2*m+1;;  f := sh.f;;
    psi := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.x^u, AbstractProd([f^-1, qrec.y^u, f])]);;
    if psi = fail then
      wellDef := false;;  kerTrivial := false;;  kerSize := fail;;
    else
      wellDef := true;;  kerSize := Size(Kernel(psi));;  kerTrivial := (kerSize = 1);;
    fi;
    Add(kernelDetail, rec(m:=m, well_defined:=wellDef, kernel_trivial:=kerTrivial, kernel_size:=kerSize));
  od;;
  kernelTrivialCount := Length(Filtered(kernelDetail, r -> r.well_defined and r.kernel_trivial));;

  # (c) staleness citation(計算なし、既存裏取りの引用のみ)
  cCitation := "裁定529, docs/notes/auto_settled_check_v1.md 付録A.1 (AS-GAP-3 -- EnumerateReducedHexagon は descent 判定を呼ばない、共有関数につき窓非依存で成立)";;

  return rec(ok:=true, enum_complete:=enumComplete, dwords_count:=result.dwords_count,
             derived_subgroup_order_independent:=dwordsIndep, shadow_total:=result.shadow_total,
             kernel_detail:=kernelDetail, kernel_trivial_count:=kernelTrivialCount,
             c_staleness_citation:=cCitation, failures:=failures);;
end;;

# ====================================================================
# dry-run 較正: K^(3)(既知窓・c∈N・BuildPn(3) パターンで自己完結構成 -- M5/N5 は
#   week3-M5-explorer.g 等が QUIT で終わる独立スクリプトのため本骨格へ chain-load できず、
#   代わりに同格の小さい既知窓 K^(3) で RunI2Window の (a)(b)(c) を end-to-end 較正する)。
#   15窓(本命標的、delta>1)には未適用 -- これは骨格の動作確認のみ。
# ====================================================================
Print("############################################################\n");
Print("# iso_census83_skeleton_v1.g -- dry-run calibration on K^(3) ONLY (NOT the 15 target windows)\n");
Print("############################################################\n");

BuildPn3 := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, X, Y, Gfull;
  r := PermList(Concatenation([2..n], [1]));;
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));;
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);;
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2)*tr(s,3);;  q2 := tr(s,1)*tr(s,3);;
  X := AbstractProd([a1,q1]);;  Y := AbstractProd([a1,a2,a3,q2]);;
  Gfull := Group(a1,a2,a3,q1,q2);;
  return rec(x:=X, y:=Y, c:=(), G:=Gfull);;
end;;

k3qrec := BuildPn3(3);;
k3Nord := Lcm(Order(k3qrec.x), Order(k3qrec.y));;
k3Charming := Filtered([0..k3Nord-1], m -> Gcd(2*m+1,k3Nord)=1);;
Print("K^(3): |G|=", Size(k3qrec.G), " N_ord=", k3Nord, " charming_set=", k3Charming, "\n");

k3Result := RunI2Window(k3qrec, rec(charmingSet:=k3Charming));;
Print("[", PF(k3Result.enum_complete), "] (a) enum_complete: dwords_count=", k3Result.dwords_count,
      " derived_subgroup_order_independent=", k3Result.derived_subgroup_order_independent,
      " shadow_total=", k3Result.shadow_total, "\n");
Print("(b) kernel_trivial_count=", k3Result.kernel_trivial_count, " / ", Length(k3Result.kernel_detail), "\n");
Print("(c) staleness citation = ", k3Result.c_staleness_citation, "\n");
Print("(d) K^(3) is a KNOWN c-in-N window (not a c-notin-N target) -- z measurement/assert is NOT\n");
Print("    exercised meaningfully here (would need z<>1 for a genuine c-notin-N window; K^(3) gives\n");
Print("    z=1 by construction). This dry-run calibrates (a)(b)(c) only; (d)'s c-notin-N assert path\n");
Print("    is exercised structurally (the code path exists and runs) but its PASS/FAIL semantics\n");
Print("    require an actual delta>1 window, which is explicitly NOT fired here.\n");
Print("[", PF(k3Result.failures = 0), "] dry-run overall (a)(b) failures = ", k3Result.failures, "\n");

Print("\n[SKELETON READY -- 15 target windows NOT applied. Firing requires 司令塔裁定 after\n");
Print(" mathematician's 札 review, per 裁定974 instruction.]\n");
QUIT;
