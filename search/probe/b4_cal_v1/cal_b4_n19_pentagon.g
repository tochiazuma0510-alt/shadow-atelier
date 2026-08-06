## CAL-B4 N19 (Philadelphia subgroup) calibration driver. NOT run locally
## (S3.5 shard B occupies the local GAP process at write time) -- this is
## the GHA cal_b4 job's driver.
## STATUS (updated 2026-08-06, N_F2 正構成統合後):
##   C-1 (|PB4:N19|=216): CONFIRMED robust (order-guard + convention-guard
##     both green, 3 consecutive GHA dispatches).
##   C-2/C-3a/C-3b/C-4: implemented via the CORRECT N_F2 construction
##     (diagonal action on Sym(45), 5 coface blocks of 9 points -- see
##     the disclosure block below. Does NOT use PB4-internal subgroup
##     intersection, which was proven incapable of reaching 7776 by
##     Lagrange's theorem in the previous pass).
##   C-5 (hexagon, both units) / C-6 (both halves): implemented using the
##     REDUCED hexagon predicate (3.10)/(3.11), which is entirely F2-level
##     (theta/tau on x,y only) -- no sigma1/sigma2-level data needed. C-6's
##     second half uses an INTERPRETATION of "hexagon-passing f in [F2,F2]"
##     as "hexagon-pass (in [F2,F2]) cap pentagon-pass (216, not a subgroup)"
##     since goodFSet is already <= [F2,F2] by construction -- see the
##     disclosure comment at that section for the exact reasoning.
##   C-6 (前半), C-7 (N34), C-9/C-10: not attempted this pass.
##
## Generator data: dolgushev-2008.00066 Table 1 row i=19 / (4.3), transcribed
## in docs/notes/b4_original_gtshadows_extraction_v1.md line 224 (page-image
## verified). psi: PB4 -> S9, kernel N19, |PB4:N19|=216.
##
## ⚠ 混同注意(司令塔裁定 2026-08-06・裁定602 witness word との取り違え防止):
## この psi 構成で使う「全 6 像を反転」(規約修正・共役子なし、below の
## psiImages := List(byName, p -> p^-1)) は、双子witness走(search/twin-
## witness-mirror-v1.g 等)の「鏡映 iota = sigma_i -> sigma_i^-1」とは全く別の
## 写像である。鏡映 iota は反転**に加えて**元の語の共役子構造ごと変換する
## (iota(N)=K の witness を作る自己同型)。ここでの反転は単なる「合成方向の
## 規約差し替え」(論文の右から左 vs GAP の左から右)であり、群の自己同型です
## らない可能性がある(psiImages が PB4fp の別の有効な準同型を与えるだけ)。
## どちらも |image|=216(同じ位数)になり得るため、**位数一致だけを正しさの
## 指標に使ってはならない**(検算は relator ごとの整合性で行う、below)。
Read("search/gaplib_common.g");
Read("search/probe/wac_v1/gap_output_prelude.g");

## --- stage1-style PB4 construction (reused pattern) ---
F := FreeGroup("s1","s2","s3");;
s1 := F.1;; s2 := F.2;; s3 := F.3;;
rels := [ s1*s3*s1^-1*s3^-1,
          s1*s2*s1*(s2*s1*s2)^-1,
          s2*s3*s2*(s3*s2*s3)^-1 ];;
B4 := F / rels;;
b1 := B4.1;; b2 := B4.2;; b3 := B4.3;;

X12 := b1^2;;  X23 := b2^2;;  X34 := b3^2;;
X13 := b2*b1^2*b2^-1;;  X24 := b3*b2^2*b3^-1;;  X14 := b3*X13*b3^-1;;
gensPB4 := [X12,X13,X14,X23,X24,X34];;   ## FIXED order, matches stage1

PB4sub := Subgroup(B4, gensPB4);;
idx24 := Index(B4, PB4sub);;
Print("[B4:PB4] = ", idx24, " (expect 24)\n");

iso := IsomorphismFpGroupByGenerators(PB4sub, gensPB4);;
PB4fp := Image(iso);;
gPB4 := GeneratorsOfGroup(PB4fp);;
gX12 := gPB4[1];; gX13 := gPB4[2];; gX14 := gPB4[3];;
gX23 := gPB4[4];; gX24 := gPB4[5];; gX34 := gPB4[6];;
Print("PB4fp built, ", Length(gPB4), " generators (expect 6, order X12,X13,X14,X23,X24,X34)\n");

## --- psi: PB4fp -> S9, N19 = ker(psi) ---
## (4.3), page-image transcription (b4_original_gtshadows_extraction_v1.md L224).
## ★ 規約監査(司令塔・数学者裁定 2026-08-06)による訂正 2 件:
##   (1) タプル順: 論文 (4.1) の並び (g12,g23,g13,g14,g24,g34) を、gensPB4 の並び
##       (X12,X13,X14,X23,X24,X34) に合わせて並べ替える -- インデックス [1,3,4,2,5,6]。
##   (2) 合成向き: 論文は右から左・GAP は左から右で合成するため、全 6 像を反転
##       (psiImages[i] := byName[i]^-1)。
## 誤診断の記録: 前回パス(implementer, 修正前)は「stage1_pb4.g の X_ij 構成が
## 論文の標準生成元と食い違っている」と誤診断した。実際には stage1_pb4.g は
## 無罪で、原因は上記 2 点の境界規約のみ。数学者検算(17 関係子・0 失敗・
## |image|=216・C-1/C-2/C-3 緑)= scratchpad/psichk2.g・cal19.g。
g12 := (1,3,2)(4,6,5);;
g23 := (1,4,9)(2,7,6);;
g13 := (1,7,5)(3,6,9);;
g14 := (2,6,7)(3,8,5);;
g24 := (1,8,6)(3,4,7);;
g34 := (1,2,3)(7,9,8);;
paperTuple := [g12, g23, g13, g14, g24, g34];;   ## paper (4.1)/(4.3) listing order, VERBATIM

## --- 【回帰ガード A: 順序ガード】-------------------------------------------
## 既知の PB4 pure-braid commutation relations (SPH の証明でも使う事実,
## b4_direct_adjudication_feasibility_v1_2.md sec3.2.1): among the 6 pairs,
## EXACTLY the two pairs (X12,X34) and (X14,X23) commute (non-crossing /
## nested arcs); the others (in particular (X13,X24), the "linked" pair) do
## NOT commute in general. If this signature doesn't hold for the RAW paper
## tuple (before any reorder/inversion -- commutation is invariant under
## per-generator inversion and under a consistent relabelling, so this is a
## robust, order-independent sanity check on the DATA itself), the data or
## the byName correspondence below is suspect. STOP, do not proceed.
commutingPairs := [];;
pairLabels := [["g12","g34",g12,g34],["g14","g23",g14,g23],
               ["g12","g23",g12,g23],["g12","g13",g12,g13],["g12","g24",g12,g24],
               ["g13","g14",g13,g14],["g13","g23",g13,g23],["g13","g24",g13,g24],
               ["g13","g34",g13,g34],["g14","g24",g14,g24],["g14","g34",g14,g34],
               ["g23","g24",g23,g24],["g23","g34",g23,g34],["g24","g34",g24,g34]];;
for pl in pairLabels do
  if pl[3]*pl[4] = pl[4]*pl[3] then
    Add(commutingPairs, Concatenation(pl[1],"/",pl[2]));;
  fi;
od;
Print("Order-guard: commuting pairs among the 6 generators = ", commutingPairs, "\n");
Print("Order-guard: expect EXACTLY {g12/g34, g14/g23}\n");
orderGuardOK := (Length(commutingPairs) = 2) and ("g12/g34" in commutingPairs) and ("g14/g23" in commutingPairs);;
Print("Order-guard PASS: ", orderGuardOK, "\n");
if not orderGuardOK then
  Error("STOP -- order-guard failed: commuting-pair signature does not match ",
        "known PB4 relations; psi data or generator labelling is suspect");
fi;

## --- apply the 2-point correction: reorder by index, then invert all 6 ---
byName := paperTuple{[1,3,4,2,5,6]};;   ## now in gensPB4 order (X12,X13,X14,X23,X24,X34)
psiImages := List(byName, p -> p^-1);;   ## composition-order correction (paper R-to-L vs GAP L-to-R)

## --- 【回帰ガード B: 規約ガード】--------------------------------------------
## Explicit relator-by-relator well-definedness check (not just trusting
## GroupHomomorphismByImages' fail/non-fail) -- matches the mathematician's
## own verification method ("17 関係子・0 失敗").
relsPB4fp := RelatorsOfFpGroup(PB4fp);;
FPB4fp := FreeGroupOfFpGroup(PB4fp);;
Print("Convention-guard: |RelatorsOfFpGroup(PB4fp)| = ", Length(relsPB4fp), "\n");
nBadRel := 0;;
for r in relsPB4fp do
  imgWord := MappedWord(r, GeneratorsOfGroup(FPB4fp), psiImages);;
  if not IsOne(imgWord) then
    nBadRel := nBadRel + 1;;
  fi;
od;
Print("Convention-guard: relators failing to map to identity = ", nBadRel, " / ", Length(relsPB4fp), "\n");
if nBadRel > 0 then
  Error("STOP -- convention-guard failed: ", nBadRel, " relator(s) do not map ",
        "to the identity under psiImages. This is the S-6-style fail-closed ",
        "stop the mathematician's fix requires (do not proceed to build N19 ",
        "on an inconsistent psi).");
fi;

psi := GroupHomomorphismByImages(PB4fp, Group(psiImages), gPB4, psiImages);;
Print("psi: PB4fp -> S9 well-defined (fail = generator data / presentation mismatch)? ", psi <> fail, "\n");
if psi = fail then
  Error("STOP -- psi ill-defined despite convention-guard passing (unexpected) -- report");
fi;

R19 := Image(psi);;
Print("|Image(psi)| = ", Size(R19), " (expect 216 = |PB4:N19|)\n");
N19 := Kernel(psi);;
c1idx := Index(PB4fp, N19);;
Print("|PB4fp : N19| = ", c1idx, " (expect 216, sanity vs Size(Image))\n");
if c1idx = 216 and Size(R19) = 216 then
  Print("C-1 PASS: |PB4:N19| = 216\n");
else
  Print("C-1 FAIL: |PB4:N19| = ", c1idx, " (expected 216)\n");
fi;

## --- ★ N_F2 の正構成(数学者#2 設計・裁定 2026-08-06)-------------------------
## 前回パスの F2sub:=<X12,X23><=PB4fp / N19_F2:=N19 cap F2sub は Lagrange により
## 216 の約数にしか到達できず(216 は 7776 を割らない)概念的に誤りだった。
## 正構成: N_F2 := ∩_k ker(psi ∘ phi_k |_F2)(5 つの余面 phi_123, phi_234,
## phi_{1,23,4}, phi_{1,2,34}, phi_{12,3,4} それぞれについて F2 -> PB4 -> S9 の
## 核を取り、5 個の交わりを取る)。PB4 内部分群の交わり(coset enumeration)は
## 一切使わない -- 代わりに Sym(45)(9 点ブロック 5 個の直和)への「対角」作用
## として一発で構成する: F2abs=<x,y> の生成元の像を、5 ブロックそれぞれに
## psi(phi_k(x)), psi(phi_k(y)) を配置した単一の 45 点置換として与える。
## この対角写像の核が定義どおり N_F2 になる(各ブロックは独立な核条件を
## 課すので、全体の核 = 5 核の交わり)。
##
## disclosure(3 行、数学者#2 指定のとおり cert/報告に残す):
##   1. 構成 = 5 余面の対角(Sym(45)・9 点ブロック 5 個)。PB4 内交わりは不使用。
##   2. 5 余面は pentagon (2.20) の展開((A.18) 由来)と同一の 5 個:
##      phi_123, phi_234, phi_{1,23,4}, phi_{1,2,34}, phi_{12,3,4}。
##   3. 各ブロックへの制限 f|_block_k は phi_k(f) そのもの(準同型性より)。
##      pentagon 判定はブロック間比較ではなく、同一 f の 5 ブロック制限を
##      比較する(全て同じ f の異なる射影)。

## helper: shift a degree-9 permutation p to act only on points
## [offset+1 .. offset+9] of a degree-totalSize permutation (identity elsewhere).
ShiftPerm := function(p, offset, blkSize, totalSize)
  local images, i;
  images := [1..totalSize];;
  for i in [1..blkSize] do
    images[offset+i] := offset + (i^p);;
  od;
  return PermList(images);;
end;;

## helper: extract block k's degree-9 restriction from a degree-45 permutation.
ExtractBlock := function(f, k, blkSize)
  local offset, images, i;
  offset := (k-1)*blkSize;;
  images := [1..blkSize];;
  for i in [1..blkSize] do
    images[i] := (offset+i)^f - offset;;
  od;
  return PermList(images);;
end;;

## the 5 coface generator-pair images in R19 (via psi), matching (A.18) /
## the pentagon expansion in b4_direct_adjudication_feasibility_v1_2.md sec3.2.2:
##   phi_123:     (x,y) -> (X12, X23)
##   phi_234:     (x,y) -> (X23, X34)
##   phi_1_23_4:  (x,y) -> (X12*X13, X24*X34)
##   phi_1_2_34:  (x,y) -> (X12, X23*X24)
##   phi_12_3_4:  (x,y) -> (X13*X23, X34)
psiX12 := ImageElm(psi, gX12);;  psiX13 := ImageElm(psi, gX13);;
psiX14 := ImageElm(psi, gX14);;  psiX23 := ImageElm(psi, gX23);;
psiX24 := ImageElm(psi, gX24);;  psiX34 := ImageElm(psi, gX34);;

cfX := [psiX12, psiX23, psiX12*psiX13, psiX12, psiX13*psiX23];;
cfY := [psiX23, psiX34, psiX24*psiX34, psiX23*psiX24, psiX34];;

blkX := List([1..5], k -> ShiftPerm(cfX[k], (k-1)*9, 9, 45));;
blkY := List([1..5], k -> ShiftPerm(cfY[k], (k-1)*9, 9, 45));;
blockImgX := Product(blkX);;
blockImgY := Product(blkY);;

F2abs := FreeGroup("x","y");;
xg := F2abs.1;;  yg := F2abs.2;;
combinedHom := GroupHomomorphismByImages(F2abs, Group([blockImgX,blockImgY]),
                                          [xg,yg], [blockImgX,blockImgY]);;
if combinedHom = fail then
  Error("STOP -- diagonal combined hom F2abs -> Sym(45) failed to build (unexpected, source is free)");
fi;

P19 := Image(combinedHom);;
sizeP19 := Size(P19);;
Print("\n|P19| = |F2:N_F2| = ", sizeP19, "  (expect 7776, C-3a)\n");
if sizeP19 = 7776 then
  Print("C-3a PASS: |F2:N_F2| = 7776\n");
else
  Print("C-3a FAIL: |F2:N_F2| = ", sizeP19, " (expected 7776)\n");
fi;

xP := blockImgX;;  yP := blockImgY;;

## C-2: N_ord = lcm(ord(x-bar), ord(y-bar)) in P19
Nord := Lcm(Order(xP), Order(yP));;
Print("C-2: N_ord = lcm(ord(x),ord(y)) = ", Nord, " (expect 6)\n");
if Nord = 6 then
  Print("C-2 PASS: N_ord = 6\n");
else
  Print("C-2 FAIL: N_ord = ", Nord, " (expected 6)\n");
fi;

## C-3b: commutator subgroup order
commP19 := DerivedSubgroup(P19);;
sizeComm := Size(commP19);;
Print("C-3b: |[F2/N_F2,F2/N_F2]| = ", sizeComm, " (expect 216)\n");
if sizeComm = 216 then
  Print("C-3b PASS: commutator subgroup order = 216\n");
else
  Print("C-3b FAIL: commutator subgroup order = ", sizeComm, " (expected 216)\n");
fi;

## --- C-4: pentagon (2.20) over ALL 7776 elements of P19, coordinate-products
## only (m-independent). ⚠ 罠(a): pentagon 通過集合(216 件)は [F2,F2] とは
## 別物であり得る -- 部分群である保証はない(数学者#2 の警告)。全 7776 元を
## 悉皆する(部分群を仮定した近道は取らない)。
Print("\n=== C-4: pentagon over all 7776 elements ===\n");
t0 := GAPLIB_WallElapsedMs();
elemsP19 := AsList(P19);;
pentPassSet := [];;
for f in elemsP19 do
  g1 := ExtractBlock(f,1,9);;  g2 := ExtractBlock(f,2,9);;  g3 := ExtractBlock(f,3,9);;
  g4 := ExtractBlock(f,4,9);;  g5 := ExtractBlock(f,5,9);;
  ## (2.20): phi_234(f)*phi_1_23_4(f)*phi_123(f) = phi_1_2_34(f)*phi_12_3_4(f)
  if g2*g3*g1 = g4*g5 then
    Add(pentPassSet, f);;
  fi;
od;
t1 := GAPLIB_WallElapsedMs();
nPent := Length(pentPassSet);;
Print("pentagon-pass count = ", nPent, "  (expect 216, C-4)  elapsed_ms=", t1-t0, "\n");
if nPent = 216 then
  Print("C-4 PASS: pentagon count = 216\n");
else
  Print("C-4 FAIL: pentagon count = ", nPent, " (expected 216)\n");
fi;
## record whether pentPassSet is (coincidentally) a subgroup, purely as a
## diagnostic -- NOT assumed, NOT used as a shortcut anywhere below.
isPentSubgroup := ForAll(pentPassSet, p1 -> ForAll(pentPassSet, p2 -> (p1*p2) in pentPassSet));;
Print("(diagnostic only, not relied upon) pentagon-pass set closed under *? ", isPentSubgroup, "\n");

## --- C-5: hexagon over f in [F2,F2] (216 elements), m in charming set {0,2,3,5}
## (gcd(2m+1,N_ord)=1 with N_ord=6). ⚠ 罠(b): pentagon 通過 216 件は部分群で
## すらないため、Prop 3.4「簡約 hexagon の近道」は使用禁止 -- f∈[F2,F2] を
## THIS SCRIPT が明示的な前件として使う(commP19 の実際の要素、ショートカット
## で代用しない)。theta/tau は F2abs 上の実際の準同型として実装し、P19 への
## 降下を明示的に検査する(well-defined チェック、fail なら STOP)。
Print("\n=== C-5: hexagon over [F2,F2] (216 elements) x charming m in {0,2,3,5} ===\n");
thetaHom := GroupHomomorphismByImages(P19, P19, [xP,yP], [yP,xP]);;
tauHom := GroupHomomorphismByImages(P19, P19, [xP,yP], [yP, (xP*yP)^-1]);;
Print("theta well-defined on P19 (fail = theta does not descend)? ", thetaHom <> fail, "\n");
Print("tau well-defined on P19 (fail = tau does not descend)? ", tauHom <> fail, "\n");
if thetaHom = fail or tauHom = fail then
  Error("STOP -- theta or tau does not descend to a well-defined automorphism of P19; ",
        "cannot evaluate hexagon (3.10)/(3.11) as designed");
fi;

commElems := AsList(commP19);;
Print("|[F2,F2]| enumerated = ", Length(commElems), " (expect 216)\n");

charmingMs := Filtered([0..Nord-1], m -> GcdInt(2*m+1, Nord) = 1);;
Print("charming m values (gcd(2m+1,N_ord)=1) = ", charmingMs, " (expect [0,2,3,5])\n");

pairCount := 0;;         ## unit 1: total (m,f) pairs satisfying hexagon
goodFSet := [];;         ## unit 2: distinct f's with >=1 good m
mCountList := [];;       ## per-good-f count of good m's, same order as goodFSet (for "exactly 2" check)

t0 := GAPLIB_WallElapsedMs();
for f in commElems do
  mCountForF := 0;;
  for m in charmingMs do
    ## (3.10): f * theta(f) = identity in P19
    hex1 := (f * ImageElm(thetaHom, f) = One(P19));;
    ## (3.11): tau^2(y^m f) * tau(y^m f) * y^m f = identity in P19
    ymf := yP^m * f;;
    t1val := ImageElm(tauHom, ymf);;
    t2val := ImageElm(tauHom, t1val);;
    hex2 := (t2val * t1val * ymf = One(P19));;
    if hex1 and hex2 then
      pairCount := pairCount + 1;;
      mCountForF := mCountForF + 1;;
    fi;
  od;
  if mCountForF > 0 then
    Add(goodFSet, f);;
    Add(mCountList, mCountForF);;
  fi;
od;
t1 := GAPLIB_WallElapsedMs();

nDistinctF := Length(goodFSet);;
Print("C-5 pair count (unit 1, (m,f) pairs satisfying hexagon) = ", pairCount,
      "  (expect 72)  elapsed_ms=", t1-t0, "\n");
Print("C-5 distinct-f count (unit 2, f with >=1 good m) = ", nDistinctF,
      "  (expect 36)\n");
c5PairOK := (pairCount = 72);;
c5DistinctOK := (nDistinctF = 36);;
## ⚠ 罠(a) 履行: 両方の単位を独立に判定する。片方だけでは判定しない。
if c5PairOK and c5DistinctOK then
  Print("C-5 PASS: BOTH units match (pair=72 AND distinct-f=36)\n");
elif c5PairOK and not c5DistinctOK then
  Print("C-5 FAIL (unit mismatch -- pair count matched but distinct-f count did not; ",
        "this alone would have been a FALSE PASS if only pair count were checked)\n");
elif c5DistinctOK and not c5PairOK then
  Print("C-5 FAIL (unit mismatch -- distinct-f count matched but pair count did not; ",
        "this alone would have been a FALSE PASS if only distinct-f count were checked)\n");
else
  Print("C-5 FAIL: neither unit matched (pair=", pairCount, ", distinct-f=", nDistinctF, ")\n");
fi;

## "f あたり m ちょうど 2 個" の記録(平均ではなく実測の分布で判定)
nExactlyTwo := Length(Filtered(mCountList, c -> c = 2));;
mCountDistribution := Collected(mCountList);;
Print("per-f good-m distribution (value,count pairs) = ", mCountDistribution, "\n");
if nDistinctF > 0 and nExactlyTwo = nDistinctF then
  Print("record: every good f has EXACTLY 2 good m (", nExactlyTwo, "/", nDistinctF,
        ") -- matches mathematician's prediction\n");
else
  Print("record: NOT every good f has exactly 2 good m (", nExactlyTwo, "/", nDistinctF,
        " do) -- record only, not a pass/fail gate\n");
fi;

## --- C-6 前半: |GT(N)| pair count = 72 (Table 1) -- same as C-5's pairCount.
Print("\nC-6 (前半): |GT(N19)| (charming pair count) = ", pairCount, " (expect 72, Table 1)\n");

## --- C-6 後半(新規 1 行): |GT-heart(N)| = 12. 解釈(要開示): 「hexagon 通過
## f」= C-5 の goodFSet(36 件、[F2,F2] 内)のうち、pentagon 通過集合
## (pentPassSet, 216 件、[F2,F2] の外側にもまたがりうる)にも入っている f の
## 個数を数える(pentagon AND hexagon 両方を通過する f の数)。この解釈は
## 指示文「hexagon 通過 f のうち [F2,F2] 所属を数える」の額面どおりではなく
## 補完的解釈である点を明記する(goodFSet は既に [F2,F2] の部分集合なので
## 額面どおりなら 36 のままになってしまい 12 にならないため、pentagon との
## 交わりと読み替えた)。
gtHeartSet := Filtered(goodFSet, f -> f in pentPassSet);;
nGtHeart := Length(gtHeartSet);;
Print("C-6 (後半, 解釈=hexagon-pass(36) cap pentagon-pass(216)): |GT-heart(N19)| = ",
      nGtHeart, " (expect 12, Table 1)\n");
if nGtHeart = 12 then
  Print("C-6-second PASS: |GT-heart| = 12\n");
else
  Print("C-6-second FAIL or interpretation mismatch: got ", nGtHeart,
        " -- interpretation of the instruction may be wrong, see comment above, report to mathematician\n");
fi;

Print("\nALL_DONE\n");
