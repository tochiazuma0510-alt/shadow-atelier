## CAL-B4 N19 (Philadelphia subgroup) identification (C-1 of docs/notes/
## b4_direct_adjudication_feasibility_v1_2.md sec6.2 ONLY, plus 2 regression
## guards -- see below). NOT run locally (S3.5 shard B occupies the local
## GAP process at write time) -- this is the GHA cal_b4 job's driver.
## STATUS (updated 2026-08-06 after 3 GHA dispatch rounds):
##   C-1 (|PB4:N19|=216): CONFIRMED, robust (order-guard + convention-guard
##     both green, matches the mathematician's own independent verification
##     "17 relators / 0 failures / |image|=216").
##   C-3/C-4/C-5 (pentagon count over |F2:N_F2|=7776, hexagon lift): BLOCKED
##     -- the naive "F2sub=<X12,X23><=PB4fp, N19_F2:=N19 cap F2sub" construction
##     is PROVABLY incapable of reaching 7776 (bounded by 216 via Lagrange /
##     second isomorphism theorem, see the comment at the bottom of this file
##     for the full argument). This is a conceptual error in what "F2"/"N_F2"
##     mean relative to N19, not a resource/coset-limit issue -- reported,
##     not routed around by throwing more compute at it.
##   C-2, C-6, C-7 (N34), C-8 (separate python job), C-9/C-10: not attempted
##     this pass, explicitly deferred.
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

## --- C-3/C-4 BLOCKED (discovered 2026-08-06, GHA run 31066781376/31066781376-2):
## the naive construction "F2sub := <X12,X23> <= PB4fp; N19_F2 := N19 /\ F2sub;
## P19 := F2sub/N19_F2" is PROVABLY INCAPABLE of reaching the paper's stated
## |F2:N_F2| = 7776, REGARDLESS of coset-enumeration resources. Proof (second
## isomorphism / diamond theorem): for H:=F2sub <= G:=PB4fp and N:=N19 <| G,
## H/(H cap N) = HN/N, which is a SUBGROUP of G/N = R19 (order 216) by the
## correspondence theorem -- hence |H/(H cap N)| DIVIDES 216 by Lagrange.
## 7776 does not divide 216 (7776/216 = 36, i.e. 216 divides 7776, not the
## reverse) -- so this P19 can NEVER have order 7776. This is a CONCEPTUAL
## bug (wrong definition of "F2"/"N_F2" relative to N19), not a resource
## bug -- raising CosetTableDefaultMaxLimit / GAP memory (-o 6g) only made
## the doomed enumeration run longer before hitting "reached the pre-set
## memory limit". STOPPING here rather than retrying with more resources.
## C-3 (|F2:N_F2|=7776), C-4 (pentagon count over that domain), and C-5
## (hexagon lift) all depend on the CORRECT F2/N_F2 construction and are
## BLOCKED pending the mathematician's exact recipe (very likely: N_F2 is
## NOT literally N19 intersected with a PB4-embedded copy of <x12,x23> --
## some other map/construction is needed, matching how Table 1's "F2" column
## relates to N via the operad coface structure, not a raw subgroup
## intersection inside PB4 itself).
Print("\nC-3/C-4/C-5: BLOCKED (conceptual construction error found this run, ",
      "not a resource limit -- see comment above this line in the script). ",
      "|F2sub:(N19 cap F2sub)| divides 216 by Lagrange and can never equal ",
      "7776. Reporting, not retrying.\n");

Print("ALL_DONE\n");
