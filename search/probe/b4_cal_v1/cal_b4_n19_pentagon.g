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

## --- C-5/C-6: FULL hexagon (3.3)/(3.4) via 3-generator Q3 (裁定664 修理・
## 数学者#2 の c5.g 方式、確定診断どおり忠実移植). 前回パスの2生成元reduced
## hexagon((3.10)/(3.11)をtheta/tau経由)は「c」に相当する第3座標
## (phi_k(x13))を一切使わず、正確に半分の値しか出なかった(pair=36/72,
## distinct-f=18/36 -- 診断: docs 便未記載だが 2026-08-06 報告参照)。
## c5.g は PB3 の全3生成元(Y12=s1^2, Y23=s2^2, Y13=s2*s1^2*s2^-1、c 相当)を
## 5余面それぞれの像として保持し(Av,Bv,Cv)、Q3:=Group(gX,gY,gZ) という
## 3生成元の target 群で T_{m,f} の full hexagon (3.3)/(3.4) を直接評価する。
Print("\n=== C-5/C-6: full hexagon (3.3)/(3.4) via 3-generator Q3 (c5.g method) ===\n");

## Av,Bv,Cv: 5余面(phi_123,phi_234,phi_{1,23,4}? -- c5.gの実際のk順序に忠実、
## 独自の再解釈はしない)。psiX_ij は既に h_ij=g_ij^-1 と一致確認済み(規約
## 修正済みのpsi構成、本ファイル上部)なのでそのまま使う。
Av := [ psiX12, psiX23, psiX13*psiX23, psiX12*psiX13, psiX12 ];;
Bv := [ psiX23, psiX34, psiX34,        psiX24*psiX34, psiX23*psiX24 ];;
Cv := [ psiX13, psiX24, psiX14*psiX24, psiX14,        psiX13*psiX14 ];;

## blk/diag: c5.g 逐語(9点ブロック5個・45点への配置)。既存の ShiftPerm と
## 数学的に同じ操作だが、c5.g の変数名/実装に忠実に独立して再定義する
## (既存コードとの暗黙の結合を避け、移植の対応関係を検査しやすくするため)。
blkC5 := function(p, k)
  local l, x;
  l := [1..45];;
  for x in [1..9] do l[9*k+x] := 9*k + x^p;; od;
  return PermList(l);;
end;;
diagC5 := function(v)
  local pr, k;
  pr := ();;
  for k in [0..4] do pr := pr * blkC5(v[k+1], k);; od;
  return pr;;
end;;

gXc5 := diagC5(Av);;  gYc5 := diagC5(Bv);;  gZc5 := diagC5(Cv);;
Gc5 := Group(gXc5, gYc5);;
Q3 := Group(gXc5, gYc5, gZc5);;

## C-4 cross-check via c5.g's own pentagon method (independent of the
## diagonal-Sym(45) construction used earlier in this file for the primary
## C-4 result -- both should give 216).
compC5 := function(p, k)
  local l, x;
  l := [];;
  for x in [1..9] do l[x] := (9*(k-1)+x)^p - 9*(k-1);; od;
  return PermList(l);;
end;;
passC5 := Filtered(Elements(Gc5), p -> compC5(p,2)*compC5(p,4)*compC5(p,1) = compC5(p,5)*compC5(p,3));;
Print("C-4 (c5.g method, cross-check) pentagon solutions = ", Length(passC5), " (expect 216)\n");
if Length(passC5) <> 216 then
  Error("STOP -- c5.g-method pentagon cross-check <> 216, Av/Bv/Cv or blk/diag mismatch");
fi;

## words for the pentagon-passing elements (as words in the free group on 2
## generators, for later re-evaluation as B3 elements via Y12,Y23).
epiC5 := EpimorphismFromFreeGroup(Gc5 : names := ["X","Y"]);;
FG2c5 := Source(epiC5);;
wordsC5 := List(passC5, p -> PreImagesRepresentative(epiC5, p));;

## B3 and PB3 -> Q3 (the FULL, 3-generator target for hexagon evaluation)
FBc5 := FreeGroup("s1","s2");;
B3c5 := FBc5 / [ FBc5.1*FBc5.2*FBc5.1*(FBc5.2*FBc5.1*FBc5.2)^-1 ];;
t1c5 := B3c5.1;;  t2c5 := B3c5.2;;
Y12c5 := t1c5^2;;  Y23c5 := t2c5^2;;  Y13c5 := t2c5*t1c5^2*t2c5^-1;;
PB3c5 := Subgroup(B3c5, [Y12c5,Y23c5,Y13c5]);;
idxB3PB3c5 := Index(B3c5, PB3c5);;
Print("[B3:PB3] = ", idxB3PB3c5, " (expect 6)\n");
if idxB3PB3c5 <> 6 then
  Error("STOP -- [B3:PB3] <> 6, PB3 construction wrong");
fi;
isoC5 := IsomorphismFpGroupByGenerators(PB3c5, [Y12c5,Y23c5,Y13c5]);;
P3fpC5 := Image(isoC5);;
homC5 := GroupHomomorphismByImages(P3fpC5, Q3, GeneratorsOfGroup(P3fpC5), [gXc5,gYc5,gZc5]);;
Print("hom PB3 -> Q3 built (fail = full-hexagon target ill-defined): ", homC5 <> fail, "\n");
if homC5 = fail then
  Error("STOP -- hom PB3->Q3 is ill-defined, cannot evaluate full hexagon (3.3)/(3.4)");
fi;
evC5 := function(g) return Image(homC5, Image(isoC5, g));; end;;

## C-5: full hexagon (3.3)/(3.4) at T_{m,f}, m in {0,2,3,5}, f ranging over
## the 216 pentagon-passing words (c5.g's own domain -- pentagon-pass, NOT
## [F2,F2] -- per 罠(b) this is deliberate: c5.g tests hexagon on the SAME
## 216 pentagon-solutions used for C-4, not on the abstractly-different
## commutator subgroup).
cntC5 := 0;;  hexpassC5 := [];;
t0 := GAPLIB_WallElapsedMs();
for i in [1..Length(wordsC5)] do
  fC5 := MappedWord(wordsC5[i], GeneratorsOfGroup(FG2c5), [Y12c5,Y23c5]);;
  for m in [0,2,3,5] do
    d1 := (fC5^-1*t1c5*t2c5*(Y13c5*Y23c5)^m)^-1 * (t1c5*Y12c5^m*fC5^-1*t2c5*Y23c5^m*fC5);;
    d2 := (t2c5*t1c5*(Y12c5*Y13c5)^m*fC5)^-1 * (fC5^-1*t2c5*Y23c5^m*fC5*t1c5*Y12c5^m);;
    if evC5(d1) = One(Q3) and evC5(d2) = One(Q3) then
      cntC5 := cntC5 + 1;;
      Add(hexpassC5, [i,m]);;
    fi;
  od;
od;
t1 := GAPLIB_WallElapsedMs();

distinctFC5 := Length(Set(List(hexpassC5, z -> z[1])));;
Print("C-5 (full hexagon) pair count (m,f) = ", cntC5, "  (target: pair=72)  elapsed_ms=", t1-t0, "\n");
Print("C-5 (full hexagon) distinct f = ", distinctFC5, "  (target: distinct-f=36)\n");
c5PairOK := (cntC5 = 72);;
c5DistinctOK := (distinctFC5 = 36);;
if c5PairOK and c5DistinctOK then
  Print("C-5 PASS: BOTH units match (pair=72 AND distinct-f=36)\n");
elif c5PairOK and not c5DistinctOK then
  Print("C-5 FAIL (unit mismatch -- pair matched, distinct-f did not: ", distinctFC5, ")\n");
elif c5DistinctOK and not c5PairOK then
  Print("C-5 FAIL (unit mismatch -- distinct-f matched, pair did not: ", cntC5, ")\n");
else
  Print("C-5 FAIL: neither unit matched (pair=", cntC5, ", distinct-f=", distinctFC5, ")\n");
fi;

## "f あたり m の個数" 分布(平均でなく実測)
mCountPerF := List(Set(List(hexpassC5, z -> z[1])),
                    fIdx -> Length(Filtered(hexpassC5, z -> z[1] = fIdx)));;
mCountDistribution := Collected(mCountPerF);;
Print("per-f good-m distribution (value,count pairs) = ", mCountDistribution, "\n");

## --- C-6 前半: |GT(N19)| pair count = 72 (Table 1) -- same as C-5's cntC5.
Print("\nC-6 (前半): |GT(N19)| (charming pair count) = ", cntC5, " (expect 72, Table 1)\n");
c6FirstOK := (cntC5 = 72);;

## --- C-6 後半: |GT-heart(N19)| = 12. ★ 注意(誤り訂正): distinctFC5(目標36、
## C-5の"distinct f"ユニット)と |GT-heart|=12 は Table 1 上で**別の量**
## (前者は hexagon 通過 f の異なり数、後者は GT(N19) それ自体が位数72の群を
## なすときの GT-heart 部分群の位数=12・D6構造)であり、混同していた前回の
## 実装(nGtHeart:=distinctFC5)を撤回する。c5.g はこの値を計算していない
## (pair数とdistinct-fの列挙で止まっている)。GT♡=12 の算出には GT(N19)=72
## 個の(m,f)ペアが実際に「群」として閉じる構造(合成則)を構築し、その中の
## charming(=[F2,F2]所属+practical等)部分集合を特定する追加実装が必要 --
## 本パスでは実装しない(サイレント省略ではなく明記)。
Print("\nC-6 (後半): |GT-heart(N19)| -- NOT COMPUTED this pass (see comment above; ",
      "distinct-f(=", distinctFC5, ") is a DIFFERENT quantity from GT-heart=12, ",
      "conflating them was an error in an earlier draft and has been withdrawn). ",
      "Requires additional structure (GT(N) group composition + charming subgroup ",
      "identification) not implemented here.\n");
c6SecondOK := fail;;   ## explicitly UNKNOWN, not silently true/false

Print("\nALL_DONE\n");
