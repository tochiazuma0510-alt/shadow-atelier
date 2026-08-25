# 972 屋根の actual arithmetic image と非算術 named rows v76

作成日: 2026-08-25
Status: arithmetic paper audit / accepted-theorem-package-relative;
finite index-three census `cross_checked`; `verified=false`.

本稿では index-three census を再実行しない。v67 の有限分割と v75 Proposition 8.1
を固定入力とし、実際の標識付き算術像

\[
 A:=\operatorname{Im}
 \bigl(\operatorname{PR}_M\circ\operatorname{Ih}:G_{\mathbf Q}\to X\bigr)
 \tag{0.1}
\]

が v75 の五条件を満たすかだけを、受理済み算術体 package、provenance、原論文で
監査する。結論は次である。

```text
FINITE INDEX-3 CENSUS:                         CROSS_CHECKED (v67; not rerun)
|A|=324:                                      PASS*
A NONNORMAL IN X:                             PASS*
FIXED K9 PROJECTION SURJECTIVE:                PASS*
FIXED NS4 PROJECTION SURJECTIVE:               PASS*
EXACT COMPLEX-CONJUGATION ROW 891 IN A:        PASS*
A IN {IDX3-NN-09, IDX3-NN-12}:                PASS*
COMMON OUTSIDE 432 IS ACTUALLY NONARITHMETIC: PASS*
ZERO-BASED ROWS 9 AND 36 NONARITHMETIC:        PASS*
ORIENTATION NN-09 VERSUS NN-12:                BLOCKED_UNKNOWN
FIXED FULL 648-ROW ROSTER:                     NOT SELECTED
ARITHMETIC ROW PAYLOAD CROSS-CHECKED:          FALSE
LEAN VERIFIED:                                FALSE
```

ここで `PASS*` は

> paper-proof relative to the post-1145 / 157bt accepted marked arithmetic
> field-and-restriction package, combined with the cross-checked finite
> implication of v75 Proposition 8.1

を意味する。算術 membership bit 324 本の機械 cross-check や Lean `verified` を
意味しない。

---

## 1. 同じ標識付き対象であること

対象は

\[
 M=K^{(9)}\cap N_{S4},\qquad
 X=GT(M)
   =GT(K^{(9)})\times_U GT(N_{S4}),
 \qquad U=(\mathbf Z/18\mathbf Z)^\times,
 \tag{1.1}
\]

であり、\(|X|=108\cdot54/6=972\) である。これは抽象的に同型な order-972
群を後から当てたものではない。`sol/luna_reply_157bt_q5_premise_reconciliation.md`
§§2.1--3.2 は、自然な factor maps、Artin marking、凍結 972 row の underlying set
をこの同じ \(X\) に束縛している。

post-1145 / 157bt で受理済みの標識付き算術体 package を次の形で使う。

\[
 \begin{aligned}
 K&=\mathbf Q(\zeta_9),\\
 E&=K(\sqrt[9]{2^7})=K(\sqrt[9]{2}),\\
 L_1&=E(i),\qquad L_2=F,\\
 G_1&=\operatorname{Gal}(L_1/\mathbf Q)
       \overset{\rm marked}{\cong}GT(K^{(9)}),\qquad |G_1|=108,\\
 G_2&=\operatorname{Gal}(L_2/\mathbf Q)
       \overset{\rm marked}{\cong}GT(N_{S4}),\qquad |G_2|=54.
 \end{aligned}
 \tag{1.2}
\]

P5′ と rational RES-INJ-9 による受理済み交叉同定は

\[
 D=L_1\cap L_2=K(\sqrt[3]{2}),\qquad
 H=\operatorname{Gal}(D/\mathbf Q),\qquad |H|=18,
 \tag{1.3}
\]

であり、自然な restriction maps を通じて

\[
 \boxed{
 X=G_1\times_U G_2,\qquad
 A=G_1\times_H G_2\subset X.}
 \tag{1.4}
\]

この標識付き二重 fibre-product は `docs/対話帳.md` T-37、特に
lines 1209--1264 に明記され、provenance の裁定 1210
(`provenance/rulings_1206_1657_snapshot_20260824.md`) が paper PASS として
受理している。P3/C1′ と P5′ の発効は provenance 裁定 1145、体・次数・roof
の式は `docs/notes/triad972_canonical_addendum_v2.md` (1)--(7) と
`sol/luna_reply_157bt_q5_premise_reconciliation.md` §4.3 に pin されている。

P4 の「\(A_{S4}\) が full pullback」という強い row-classifier 命題は現在も open
である。しかし (1.4) と以下の五条件には不要であり、本稿は P4 を閉じたとは
主張しない。

---

## 2. v75 の五条件の個別監査

### 2.1 条件 (i): \(|A|=324\)

(1.4) の restriction maps は全射であるから、有限 fibre product の位数公式より

\[
 |A|=\frac{|G_1||G_2|}{|H|}
     =\frac{108\cdot54}{18}=324.
 \tag{2.1}
\]

これは 972-row artifact に `arithmetic_count=324` と書いたことを根拠にしていない。
同じ値は canonical addendum の

\[
 |A|=\frac{12d_9d_{S4}}r
     =\frac{12\cdot9\cdot9}{3}=324
\]

とも一致する。従って条件 (i) は受理済み算術体 package 相対で paper PASS。

### 2.2 条件 (ii): \(A\not\trianglelefteq X\)

restriction による全射

\[
 q:X\twoheadrightarrow H\times_U H
 \tag{2.2}
\]

を取ると、(1.4) より

\[
 A=q^{-1}(\Delta H).
 \tag{2.3}
\]

一般に \(N=\ker(H\to U)\) とすると

\[
 \Delta H\trianglelefteq H\times_U H
 \quad\Longleftrightarrow\quad N\le Z(H).
 \tag{2.4}
\]

実際、\((a,b)\in H\times_U H\) による \((h,h)\) の共役が再び対角に入ることは
\(b^{-1}a\in Z(H)\) と同値であり、可能な \(b^{-1}a\) 全体が \(N\) である。

ここでは

\[
 N=\operatorname{Gal}(D/K)\cong C_3.
\]

\(\tau(\sqrt[3]{2})=\zeta_3\sqrt[3]{2}\) とし、複素共役を \(c\) とすると

\[
 c\tau c^{-1}=\tau^{-1}\ne\tau.
 \tag{2.5}
\]

従って \(N\not\le Z(H)\)、(2.4) により \(\Delta H\) は非正規、全射 (2.2) の
逆像 \(A\) も非正規である。これは T-37 の証明そのものであり、裁定 1210 が

\[
 A\not\trianglelefteq X,\qquad
 \operatorname{im}(X\curvearrowright X/A)\cong S_3,\qquad
 |\operatorname{core}_X(A)|=162
\]

を受理済みである。従って条件 (ii) は paper PASS。有限 index-three census から
「実際の \(A\) も非正規だろう」と逆推定してはいない。

### 2.3 条件 (iii): fixed K9 projection は全射

\(D/\mathbf Q\) は Galois で \(D\subset L_1\) だから、自然な restriction

\[
 r_1:G_1\twoheadrightarrow H
\]

は全射である。任意の \(g_1\in G_1\) に対し、\(r_2(g_2)=r_1(g_1)\) となる
\(g_2\in G_2\) を選べるので、\((g_1,g_2)\in A\)。従って

\[
 \operatorname{pr}_{K9}(A)=G_1=GT(K^{(9)}).
 \tag{2.6}
\]

ここで最後の等号は (1.2) の **fixed marked** factor identification である。
抽象同型だけから全射を言っていない。

原論文 `papers/2405.11725-nonabelian-quotients-gt-elementary.pdf` の印刷 p.6,
Remark 1.5, equation (1.14) も、細かい標的から粗い標的への reduction について

\[
 \mathcal R_{H,N}(GT_{\rm arith}(H))=GT_{\rm arith}(N)
 \tag{2.7}
\]

を与えており、同じ全射性を Ihara-map 側から確認する。従って条件 (iii) は
paper PASS。

### 2.4 条件 (iv): fixed NS4 projection は全射

同様に自然な restriction \(r_2:G_2\twoheadrightarrow H\) は全射である。
任意の \(g_2\in G_2\) に対して \(r_1(g_1)=r_2(g_2)\) となる \(g_1\) を選べるから

\[
 \operatorname{pr}_{NS4}(A)=G_2=GT(N_{S4}).
 \tag{2.8}
\]

これも fixed marked factor についての文であり、原論文 (1.14) と整合する。
従って条件 (iv) は paper PASS。

### 2.5 条件 (v): exact complex-conjugation row を含む

同原論文の印刷 pp.4--5, equations (1.5), (1.11), (1.12) は

\[
 \operatorname{Ih}(g)=((\chi(g)-1)/2,f_g),\qquad
 \operatorname{Ih}_N=\mathcal{PR}_N\circ\operatorname{Ih},\qquad
 GT_{\rm arith}(N)=\operatorname{Ih}_N(G_{\mathbf Q})
 \tag{2.9}
\]

を定義する。さらに印刷 p.7, Remark 1.10 は、複素共役 \(c\) について全ての
標的 \(N\) で

\[
 \operatorname{Ih}_N(c)=(-1,1)
 \tag{2.10}
\]

と明記する。従って \(N=M\) とすれば、この元は定義により \(A\) に入る。

凍結 972 座標では \(N_{\rm ord}=18\) なので第一成分は

\[
 m=-1\equiv17\pmod {18},
\]

第二成分 \(f=1\) は空語である。`sol/luna_reply_159i_idx3_producer.md` §1.2 と
v2 finite receipt は、\(m=17\) の唯一の空語行を **zero-based row 891** と束縛する。
従って

\[
 \boxed{c_\infty=\operatorname{row}891\in A.}
 \tag{2.11}
\]

算術的 inclusion は原論文 (2.10)、row number は凍結座標 binding から来る。
有限候補が row 891 を含むことから算術性を逆推定してはいない。条件 (v) は PASS。

---

## 3. unordered pair の確定

v75 Proposition 8.1 は、同じ fixed K9/NS4 component maps と同じ
\(c_\infty=\operatorname{row}891\) に対して次を述べる。

> \(B\le X\) が order 324、nonnormal、両 fixed component へ全射、かつ
> \(c_\infty\in B\) なら、cross-checked exhaustive index-three census により
> \(B\in\{\mathrm{IDX3\mbox{-}NN\mbox{-}09,
>          \mathrm{IDX3\mbox{-}NN\mbox{-}12\}\)。

§2 がこの五前件を実際の \(A\) について全て認証したので、直ちに

\[
 \boxed{
 A\in\{A_9,A_{12}\},\qquad
 A_9:=\mathrm{IDX3\mbox{-}NN\mbox{-}09},\quad
 A_{12}:=\mathrm{IDX3\mbox{-}NN\mbox{-}12}.}
 \tag{3.1}
\]

を得る。従って v67 の \((H_{\rm pair})\) は、**accepted-theorem-package-relative
paper proof + cross-checked finite census** という格で閉じる。

これは v67 の有限 receipt を arithmetic payload へ読み替えたものではない。
receipt の

```text
cross_checked_arithmetic_payload = false
selected_candidate = null
```

はそのまま正しい。新しく使ったものは、finite roster 内部のデータではなく、T-37 の
標識付き算術 fibre-product と原論文の複素共役である。

---

## 4. 名指しできる非算術行と、まだ名指しできない 216 行

v67 の cross-checked 分割を再掲する。

\[
 \begin{aligned}
 C&=A_9\cap A_{12},& |C|&=108,\\
 D_9&=A_9\setminus A_{12},& |D_9|&=216,\\
 D_{12}&=A_{12}\setminus A_9,& |D_{12}|&=216,\\
 O&=X\setminus(A_9\cup A_{12}),& |O|&=432.
 \end{aligned}
 \tag{4.1}
\]

(3.1) より

\[
 \boxed{O\cap A=\varnothing.}
 \tag{4.2}
\]

したがって \(O\) の全 432 行は actual arithmetic image の外にある。
この集合の既存 compact pin は

```text
zero-based row-index-list SHA256:
99acd3ce41ff6e2d1a6430abea3de0bfb7ee1e82fa825da9118cbd0714339d36

canonical-key-list SHA256:
ab3c1867a11b5f425b55c40d2582ca586b8774f4b282a69addd763a26abd105b
```

である (`sol/sol_reply_159_iv.md` §21.4)。特に v67 の有限 membership

\[
 \operatorname{row}9,\operatorname{row}36\in O
 \tag{4.3}
\]

と合わせて

\[
 \boxed{
 \operatorname{row}9\notin A,\qquad
 \operatorname{row}36\notin A.}
 \tag{4.4}
\]

すなわち zero-based row 9 と row 36 は、受理済み theorem framework 相対で
**実際に非算術**である。orientation は不要である。

一方、完全な非算術 648-row roster はまだ二択である。

\[
 X\setminus A=
 \begin{cases}
  \Omega_9=D_{12}\sqcup O,& A=A_9,\\
  \Omega_{12}=D_9\sqcup O,& A=A_{12}.
 \end{cases}
 \tag{4.5}
\]

従って現時点で名指しできるのは common outside 432 と、その中の row 9/36。
残る actual nonarithmetic 216 行は \(D_9,D_{12}\) のどちらか一方だが、どちらかは
未選択である。

---

## 5. orientation の第一欠品

凍結有限作用

\[
 T_\varepsilon(m,k,\pi)=(m,\varepsilon k,\pi),\qquad
 \varepsilon\in(\mathbf Z/9\mathbf Z)^\times
 \tag{5.1}
\]

は

\[
 \begin{array}{c|c}
 \varepsilon\in\{1,4,7\}&A_9,A_{12}\text{ を個別に固定},\\
 \varepsilon\in\{2,5,8\}&A_9\leftrightarrow A_{12}
 \end{array}
 \tag{5.2}
\]

と作用する。従って unordered pair (3.1) は unit ambiguity に不変だが、個別候補の
選択は unit orientation に依存する。

既閉の P5′ は

\[
 \langle[u_0^{-1}]_9\rangle
 =\langle[u_{S4}^{-1}]_9\rangle
 \tag{5.3}
\]

という **巡回部分群** の一致だけを与える。`sol/luna_reply_159k_p5_math_audit.md`
が記録する通り、向き付き generator を frozen K9/NS4 marking に結ぶ

\[
 \text{marked }\mathbf Q\text{-isomorphism }\iota_W,qquad
 \text{cotangent scalar }\gamma,qquad
 \text{loop unit exponent }\varepsilon
 \tag{5.4}
\]

は未収蔵である。個別候補を交換する最終有限 bit は

\[
 [\varepsilon]\in
 (\mathbf Z/9\mathbf Z)^\times/
 \{1,4,7\}
 \cong C_2
 \tag{5.5}
\]

である。しかし現状では、その bit を読むための baseline である marked restriction、
conjugator、代表規約自体が未 pin なので、(5.5) だけを無標識に宣言してはならない。

従って orientation の **第一欠品** は正確には

```text
P5-REP-STOP-MISSING-IOTA-GAMMA-EPSILON:
labelled index-9 cusp と frozen loop/generator marking を保つ explicit marked
Q-isomorphism を与え、local parameter/tangent scalar gamma と loop exponent
epsilon（少なくともその square/nonsquare class）を、K9/NS4 restriction、
conjugator、D972 normalization と同じ typed record に束縛すること。
```

同値な供給方法は、これら全規約を含む authenticated joint marked Frobenius row
を一行与え、その row の \(A_9/A_{12}\) membership を canonical key で照合することである。
現在の Frobenius inventory は observed rows 0、P5′ は representative equality を主張せず、
`selected_A_cand=null` である。従って orientation と完全 648 roster は
`BLOCKED_UNKNOWN` のままである。

---

## 6. v67 に対する versioned 差分

v67 は「finite census や v2 arithmetic receipt だけから \((H_{\rm pair})\) を出しては
ならない」とした点で正しい。本稿はその禁止を破らず、v67 が別証拠線として利用して
いなかった T-37 / 裁定 1210 の算術体 fibre-product と原論文 Remark 1.10 を v75
Proposition 8.1 に入力した。

従って v67 を次の一点だけ supersede する。

```text
v67: H_pair = BLOCKED_UNKNOWN
v76: H_pair = PASS*
     (accepted marked arithmetic-field package relative
      + paper proof
      + cross-checked exhaustive finite implication)
```

次は supersede しない。

- \(A=A_9\) か \(A=A_{12}\) かという orientation は未選択。
- fixed full 648-row roster は未発行。
- arithmetic 324-row membership payload は machine cross-check されていない。
- P4 full-pullback は open。
- Lean `verified` ではない。
- 本稿だけから B3/B4 lift、genuine/fake、Ihara 非全射証人を宣言しない。

最終札は

```text
ACTUAL_ARITHMETIC_IMAGE_IN_UNORDERED_PAIR_PAPER_PASS_RELATIVE
COMMON_OUTSIDE_432_ACTUALLY_NONARITHMETIC_RELATIVE
ROWS_9_AND_36_ACTUALLY_NONARITHMETIC_RELATIVE
FULL_648_ROSTER_ORIENTATION_BLOCKED_UNKNOWN
NO_FINITE_CENSUS_RERUN
NO_ARITHMETIC_PAYLOAD_CROSSCHECK_CLAIM
VERIFIED_FALSE
```

である。

---

## 7. load-bearing pins

1. `sol/proof_r07_arithmetic_648_typing_erratum_v67.md` §§1--3, 8:
   cross-checked finite partition、row 9/36 membership、証拠格の分離。
2. `sol/proof_r07_arithmetic_double_orbit_dihedral_absorber_v75.md` §8,
   Proposition 8.1: 五条件から unordered pair への有限完全 implication。
3. `docs/対話帳.md` T-37 (lines 1205--1303): marked double fibre-product、
   nonnormality proof、格と射程。
4. `provenance/rulings_1206_1657_snapshot_20260824.md`, 裁定 1210:
   T-37 の paper PASS 受理。
5. `provenance/LEDGER.md`, 裁定 1145: C1′/P5′ 発効。
6. `sol/luna_reply_157bt_q5_premise_reconciliation.md` §§2--4:
   fixed roof/row binding、\(|A|=324\)、P4 非依存。
7. `docs/notes/triad972_canonical_addendum_v2.md` equations (1)--(7):
   Kummer field degree、roof fibre product、算術 compositum。
8. `docs/notes/c1prime_s4_p5prime_closure_v2.md` §4:
   P5′ の正確な subgroup-level 境界。
9. `papers/2405.11725-nonabelian-quotients-gt-elementary.pdf`, printed
   pp.4--7: equations (1.5), (1.11), (1.12), (1.14), Remark 1.10。
   本監査では PDF ページ画像を直接照合した。
10. `sol/luna_reply_159i_idx3_producer.md` §1.2:
    \((-1,1)\leftrightarrow(m=17,f=1)\leftrightarrow\) zero-based row 891。
11. `sol/luna_reply_159k_p5_math_audit.md` §§1--5 と
    `sol/luna_reply_159j_frobenius_design.md` §§3--5:
    orientation の representative-level 欠品と observed rows 0。

新規 GAP、有限 census、GHA、git、Lean は実行していない。
