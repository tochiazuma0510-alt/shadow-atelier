# 実験 A(裁定 243 工程 1)— 予想 PASSPORT の判定と、剛性 N の**正体の訂正** v1

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- 委嘱: 司令塔「裁定 243 工程 1【実験 A】」— ①N_gen ≥ 2 の最小 passport 探索 ②別軌道 witness 2 個 ③GTSh 比較で PASSPORT を裁く ④余力で H2(SPIN)
- 入力正本: `docs/notes/sat_l1_v1.md`(定理 RED / SURV / SURV+ / SAT-RIG / CENT / CENT-0 / 計数機構 §10.6.2)、`docs/notes/hexagon_orientation_ruling_v1.md`(judge 規約)、`docs/notes/wac_reverse_design_v1.md`(補題 0.1・命題 0.3・命題 3.1)、`ideas/ideas_014_harvest_and_targets.md` H1/H2
- 既存実測との突合: `search/strike-a13-ladder.g`(窓表)、`search/certs/a13_ladder_W_E_A10_9t1*.json`(6 窓)、`search/certs/ladder_xi_recheck_*`
- **f_orientation: judge**(全 probe・全 cert。手書き向きは一切使っていない)
- 格の宣言: 本稿は **単系統(GAP 4.16.0)**。ただし計数は「指標和」と「直接悉皆」の**二経路が一致**している(§2.3)。Lean verified ではない。台帳請求権は発生していない。

---

## 0. 予言の凍結(測定**前**に書いた・prediction-first)

> **本節は測定を走らせる前に書き、以後一字も書き換えていない。**(§2 以降が測定。)

### 0.1 探索についての予言

- **(F1)** 我々の族(a₁ ∈ 2^k1^\*, b₁ ∈ 3^j1^\*, w₀ 固定)で **N_gen ≥ 2 は「稀な破れ」ではなく普通に起きる**と予想する。理由: 既測 11 窓はすべて $\bar x=(\ell^r,1^t)$ という**設計上の特殊形**に偏っており、母集団の代表ではない。
- **(F2)** 最小の n は **n = 10**。理由: 定理 TRI(ord(w₀) ≥ 7)+ Ree の二重ゲートで n ≤ 9 はほぼ全滅するはず。

### 0.2 λ=(7,3)(n=10)窓についての予言(§3 の測定対象)

$w_0$ が偶長巡回をもたない($p=s=0$)ので **定理 CENT-0 が適用できる**。よって:

- **(P1)** $N_{\rm ord}=\operatorname{ord}(\bar x)=\operatorname{ord}(w_0^2)=21$、charming 個数 $=\varphi(42)=\mathbf{12}$。
- **(P2)** $\Xi(\ker\widetilde\chi)=C_{S_{10}}(w_0)=C_7\times C_3=C_{21}$(**位数 21**)。定理 CENT-0 の挟み撃ちが閉じるので、これは**測定でなく定理**。
- **(P3)** $\lvert\ker\widetilde\chi\rvert=\mathbf{21}$、$\ker\widetilde\chi\cong C_{21}$。(Ξ 単射は UNKNOWN なので、これは (P2) + 単射性の予想。)
- **(P4)** $\lvert\mathrm{GTSh}\rvert = 21\times 12=\mathbf{252}$、$\varepsilon=0$($w_0$ 偶 ⟹ $a_1$ 偶 ⟹ $E=A_{10}\times S_3$)。
- **(P5・本命)** **3 つの軌道から作った 3 窓は、上記すべてが一致する** ⟹ **予想 PASSPORT を支持**。

### 0.3 【本稿の主予言】剛性 N の正体は「窓の個数」であって「核の大きさ」ではない

sat_l1_v1 §6.2 の **定理 SAT-RIG (a)**「$\ker\widetilde\chi\leftrightarrow\mathcal F(v)$」を、私は**誤り**と予言する。

> **(P6・訂正予言)** GT-shadow の定義には hexagon (3.10)(3.11) と全射性のほかに
> 「$T_{m,f}$ が**well-defined な自己準同型である**」(judge の settled 節)が入る。$m=0$ ではこれは
> $$\exists\,\alpha\in C_{S_n}(\bar x):\quad \bar y^{\,\alpha}=f\bar yf^{-1}$$
> と同値であり、hexagon からは従わない。したがって
> $$\ker\widetilde\chi\ \subsetneq\ \mathcal F(v)\quad(\text{一般には真の部分集合}),$$
> $$\boxed{\ \lvert\ker\widetilde\chi\rvert=\lvert C_{S_n}(w_0)\rvert\cdot N_{\rm shadow},\qquad N_{\rm shadow}\le N_{\rm gen}\ }$$
> で、**$N_{\rm shadow}=1$(基点軌道だけ)を予言**する。
> **系(予言)**: 「飽和 ⟺ 剛性 $N_{\rm gen}=1$」(SAT-RIG (d))は**偽**。$N_{\rm gen}\ge2$ でも CENT は成り立ちうる。
> **検証形**: n=10・λ=(9,1) の canonical 窓で、hexagon+全射を満たす $f$ は **54 個**(= $T_{\rm gen}$)あるが、shadow は **9 個**(= $\lvert C\rvert$)だけであることを示せ。
> **含意(予言)**: $N_{\rm gen}$ は「同じ passport をもつ**窓の個数**」を数えている。工房が既に作っていた sibling 窓 `-o2..-o6` は、まさにこの別軌道である。

---

## 1. 判定(先出し)

| # | 主張 | 格 |
|---|---|---|
| **①** | **最小の $N_{\rm gen}\ge2$ passport は $n=10$**。$n\le9$ では全 passport で $N_{\rm gen}\le1$(厳密)。$n=10$ には $N_{\rm gen}\ge2$ の passport が**一挙に 5 本**現れる: $(9,1)\!:\!6$、$(10)\!:\!5$、$(8,2)\!:\!3$、$(7,3)\!:\!3$、$(6,4)\!:\!3$ | **二経路一致**(指標和 × 直接悉皆) |
| **②** | **予言 (F1) 的中**: $N_{\rm gen}\ge2$ は例外でなく**常態**。既測 11 窓が全部 $N_{\rm gen}$ 由来の一意性をもつように見えたのは、$\bar x=(\ell^r,1^t)$ 設計への偏りではなく **§4 の測り違い**だった | **proof + 実データ** |
| **③** | **予想 PASSPORT は支持**(反証されず)。$n=10,11$ の **7 passport・計 24 窓**(うち 5 passport が $N_{\rm gen}\ge2$)で、$\lvert\mathrm{GTSh}\rvert$・IdGroup・$\ker\widetilde\chi$ の IdGroup・$\lvert\Xi(\ker)\rvert$・$N_{\rm ord}$・charming 数が**すべて passport ごとに完全一致**(24/24) | **窓 assert + 全数測定**(GAP 単系統) |
| **④** | **定理 SAT-RIG (a)(c)(d) は誤り**。$\ker\widetilde\chi\subsetneq\mathcal F(v)$。実測: $\lvert\mathcal F(v)\rvert=54$、うち hexagon(3.10)(3.11)+全射は **54/54**、shadow は **9/54**(= 基点軌道のみ)。よって $N_{\rm shadow}=1\ne N_{\rm gen}=6$ ⟵ **同日・別セッションの T3 稿(`t3_quasi_purecycle_rigidity_v1.md` ①)が別経路で同じ訂正に到達しており、本稿は独立な二重発見**(§7.4) | **反証(明示実データ)+ 機構の同定・独立二重取得** |
| **⑤** | **系(重要)**: 「**飽和 ⟺ 剛性**」は成立しない。$N_{\rm gen}=6$ の窓で CENT($\Xi(\ker)=C_{S_n}(w_0)$)は成り立つ。**剛性は CENT の必要条件ではない** — 委嘱が「発見」と呼んだ事象がそのまま起きた | **実データ 24/24**(+ T3 稿 ④ で **定理化済み**) |
| **⑥** | **系(工程への含意)**: 【GAP-C1】(剛性 $N=1$ の証明 = 本丸の後継)は**標的が誤っていた**。正しい標的は「settled 節($T$ が自己準同型)が基点軌道以外を殺すこと」で、§4.3 に紙の証明を書いた。**T3 稿の定理 XI-C + XI-INJ がこれを完成させており、予想 CENT は既に定理**(§7.4) | **proof(§4.3)+ T3 稿で完結** |
| **⑦** | **$N_{\rm gen}$ の値が T3 稿の閉形と完全一致**: $(13,1^3)_{n=16}\!\to\!2$、$(17,1^3)_{n=20}\!\to\!10$、$(19,1^5)_{n=24}\!\to\!1$。私は Frobenius 指標和 + 巡回集合分割 Möbius、T3 稿は**平面木の Catalan 計数** — **全く別の道具が 3 点で一致**(§7.3) | **cross-checked(二手法一致)** |
| **⑧** | **H2(予想 SPIN)は第一測定で否定的**。$2\cdot A_{10}$ で対合類 $2^41^2$ の原像は**割れない**(1 類)⟹ 標準的な持ち上げ不変量は well-defined ですらなく、Nielsen 類を分離しない | **機械確認**(ctbllib `2.A10`) |
| **⑨** | **Sol F88-2.6「窓の E-構造に追加情報」への名指し回答**: 追加情報は **Nielsen 類(= $C_{S_n}(w_0)$-軌道)そのもの**。$a_1,b_1$ の**音節長 6 の語の巡回型**で全 Nielsen 類が分離される(6→6, 5→5, 3→3 ×3)。**GTSh はこの情報を完全に忘れる** | **実データ** |

> **一行で**: 「$N\ge2$ の窓を探して PASSPORT を裁く」という委嘱を実行したところ、$N\ge2$ は最初の窓($n=10$)から常態であり、しかも**工房は既にその別軌道窓(`-o2..-o6`)を作って測っていた**。PASSPORT は 24/24 で支持された。そして副産物として、**剛性 $N$ と核の大きさを結ぶ SAT-RIG の等式が誤りだった**ことが確定した。

---

## 2. 工程 1 — $N_{\rm gen}$ の走査

### 2.1 何を数えるのか(定義の確定)

窓は命題 0.3 型: $a_1^2=b_1^3=1$、$\langle a_1,b_1\rangle\supseteq A_n$、$w_0:=b_1^{-1}a_1$、$\bar x=w_0^2$。
$$\mathcal F(w_0):=\{(a_1,b_1):a_1^2=1,\ b_1^3=1,\ b_1^{-1}a_1=w_0,\ \langle a_1,b_1\rangle\supseteq A_n\},$$
$$T_{\rm gen}:=\lvert\mathcal F(w_0)\rvert,\qquad N_{\rm gen}:=\#\bigl(\mathcal F(w_0)/C_{S_n}(w_0)\bigr).$$
$C_{S_n}(w_0)$ の同時共役作用は $\mathcal F(w_0)$ 上**自由**(安定化群 $=C_{S_n}(\langle a_1,b_1\rangle)=C_{S_n}(A_n)=1$)なので $T_{\rm gen}=\lvert C_{S_n}(w_0)\rvert\cdot N_{\rm gen}$。
なお $\operatorname{sgn}(a_1)=\operatorname{sgn}(w_0)$ は自動($b_1$ は常に偶)なので、$\varepsilon$ は passport が決める。

### 2.2 走査の道具と、**厳密に言えることの範囲**

`search/probe/wac_v1/expA_scan.g`(計数機構は sat_l1_v1 §10.6.2 と同一実装):

- $T_{\rm all}$ = 対称群指標表の class multiplication coefficient を(対合類 × 位数 3 類)全対で和(厳密)。
- $T_{\rm trans}$ = $w_0$ の巡回の集合分割上の Möbius 反転(厳密)。
- **$R:=T_{\rm trans}/\lvert C_{S_n}(w_0)\rvert$ は $N_{\rm gen}$ の上界**($T_{\rm gen}\le T_{\rm trans}$)。⟹ **$R<2$ なら $N_{\rm gen}\le1$ が全 λ で厳密に従う。**
- **補題 CLEAN(本稿)**: $\lambda$ が**素数の部分 $\ell$ で $n/2<\ell\le n-3$** をもてば、$T_{\rm gen}=T_{\rm trans}$、ゆえに **$N_{\rm gen}=R$ が厳密**。
 **証明.** $\ell>n/2$ ゆえ他の部分の総和 $n-\ell<\ell$、$\ell$ 素数ゆえ $\ell\nmid M:=\operatorname{lcm}(\text{他の部分})$。よって $w_0^M$ はちょうど 1 本の $\ell$-巡回($n-\ell\ge3$ 点を固定)。推移的とすると、ブロック長 $b\mid n$、$b\ge2$ ならブロック数 $n/b\le n/2<\ell$ ゆえ位数 $\ell$ の $w_0^M$ は各ブロックを保つ;$\ell$-巡回は台上推移的だからブロックは台を丸ごと含む ⟹ $b\ge\ell>n/2$ ⟹ $b=n$、矛盾。よって**原始的**。原始 + 素数長 $\ell\le n-3$ の巡回 ⟹ Jordan により $\supseteq A_n$。∎
 (この 3 段は sat_l1_v1 §10.6.5 の P-WALL-2 の論法と同一。本稿はそれを**判定条件として一般化**した。)
- 残り(non-clean かつ $R\ge2$)は本 probe では UNDETERMINED。§2.3 の直接悉皆で個別に決着させた。

**I1 較正**: probe8 の 9 窓の $(T_{\rm all},T_{\rm trans})$ を**全一致で再現**(CAL_FAILS = 0)。

### 2.3 二経路目 — 直接悉皆(`expA_verify.g`)

$S_n$ の**全対合**を共役類ごとに悉皆し、$b_1:=a_1w_0^{-1}$、$b_1^3=1$、$\lvert\langle a_1,b_1\rangle\rvert\ge n!/2$ で濾す。$n\le11$ で数秒。

| n | λ | \|C(w₀)\| | T_all 直接 / 指標 | T_trans 直接 / 指標 | **T_gen** | **N_gen** |
|---|---|---|---|---|---|---|
| 8 | (8) | 8 | 24 / 24 ✓ | 24 / 24 ✓ | **0** | 0 |
| 9 | (8,1) | 8 | 40 / 40 ✓ | 16 / 16 ✓ | **0** | 0 |
| 9 | (9) | 9 | 36 / 36 ✓ | 36 / 36 ✓ | **0** | 0 |
| 10 | (9,1) | 9 | 90 / 90 ✓ | 54 / 54 ✓ | **54** | **6** |
| 10 | (8,2) | 16 | 72 / 72 ✓ | 48 / 48 ✓ | **48** | **3** |
| 10 | (7,3) | 21 | 77 / 77 ✓ | 63 / 63 ✓ | **63** | **3** |
| 10 | (6,4) | 24 | 96 / 96 ✓ | 72 / 72 ✓ | **72** | **3** |
| 10 | (10) | 10 | 65 / 65 ✓ | 65 / 65 ✓ | **50** | **5** |
| 10 | (7,2,1) | 14 | 77 / 77 ✓ | 14 / 14 ✓ | **14** | **1** |

**J1(指標和と直接悉皆の一致)9/9 PASS。J2(全軌道長 = \|C(w₀)\|)PASS**(自由作用の再確認)。

### 2.4 結論 — 最小 passport

- **$n\le9$**: 各 λ は「$R<2$(⟹ $N_{\rm gen}\le1$)」か「$T_{\rm gen}=0$(窓なし)」のいずれか。⟹ **$N_{\rm gen}\ge2$ は存在しない(厳密)**。
- **$n=10$**: $N_{\rm gen}\ge2$ の passport が **5 本**(上表)。$N_{\rm gen}=1$ は $(7,2,1)$ ただ 1 本。
- ⟹ **最小 passport は $n=10$。最大の $N_{\rm gen}$ をもつのは $\lambda=(9,1)$、$N_{\rm gen}=6$。**

### 2.5 予言 (F1) の的中ぶり — $N_{\rm gen}\ge2$ は常態

`expA_scan.g` を $n=8..20$ で走らせると、clean と判定できた λ だけで **$N_{\rm gen}\ge2$ が 76 本**。例:

| n | λ | \|C(w₀)\| | T_gen | **N_gen** |
|---|---|---|---|---|
| 13 | (7,6) | 42 | 336 | **8** |
| 14 | (11,3) | 33 | 396 | **12** |
| 15 | (11,4) | 44 | 792 | **18** |
| **16** | **(13,1,1,1)** | 78 | 156 | **2** |
| 17 | (13,4) | 52 | 3120 | **60** |
| 19 | (13,6) | 78 | 10686 | **137** |
| **20** | **(17,1,1,1)** | 102 | 1020 | **10** |
| 20 | (17,3) | 51 | 15453 | **303** |

**太字の 2 本は $(\ell,1^t)$ 型** — すなわち **T3(準 pure-cycle 剛性定理)が「$N=1$」を主張しようとしている当の族**である(§7.3)。

---

## 3. 工程 2・3 — PASSPORT の判定(24 窓)

### 3.1 witness の構成

委嘱は「2-opt 山登りで別軌道 witness を 2 個」だったが、**$n=10,11$ では山登り不要**: 全対合の悉皆(数秒)で $\mathcal F(w_0)$ が丸ごと得られ、$C_{S_n}(w_0)$-軌道分解で**全軌道の代表**が取れる。よって 2 個ではなく**全 Nielsen 類**を測った。

### 3.2 測定(`expA_measure.g` / `expA_batch.g`・judge 実物)

各代表 $(a_1,b_1)$ から `BuildS1S2E`(工房の正本構成)で $s_1,s_2$ を作り、`search/kerchi-judge.g` の実物(`MakeWindow` / `CorrectedShadows` / `GroupOfShadows`)で GTSh を全数計算。$\Xi(\ker)$ は $\mathrm{Stab}(\bar x)=C_{S_n}(\bar x)$ の中で $\bar y^{\alpha}=f\bar yf^{-1}$ を解いて独立に再計算。

| passport (n, λ) | $N_{\rm gen}$ | $\lvert C(w_0)\rvert$ | $\lvert C(\bar x)\rvert$ | CENT-0 | $N_{\rm ord}$ | charm | $\lvert\ker\rvert$ | $\ker$ | $\lvert\Xi(\ker)\rvert$ | $\lvert\mathrm{GTSh}\rvert$ | IdGroup |
|---|---|---|---|---|---|---|---|---|---|---|---|
| (10, (9,1)) | **6** | 9 | 9 | 適用可 | 9 | 6 | 9 | $C_9$ | 9 | 54 | [54,6] |
| (10, (8,2)) | **3** | 16 | **64** | 不可 | 4 | 4 | 16 | $C_8\times C_2$ | 16 | 64 | [64,254] |
| (10, (7,3)) | **3** | 21 | 21 | 適用可 | 21 | 12 | 21 | $C_{21}$ | 21 | 252 | [252,26] |
| (10, (6,4)) | **3** | 24 | **144** | 不可 | 6 | 4 | 24 | $C_{12}\times C_2$ | 24 | 96 | [96,209] |
| (10, (10)) | **5** | 10 | **50** | 不可 | 5 | 4 | 10 | $C_{10}$ | 10 | 40 | [40,12] |
| (10, (7,2,1)) | 1 | 14 | **42** | 不可 | 7 | 6 | 14 | $C_{14}$ | 14 | 84 | [84,7] |
| (11, (7,4)) | **3** | 28 | **56** | 不可 | 14 | 12 | 28 | $C_{28}$ | 28 | 336 | [336,125] |

**各行の全窓(合計 24 窓)で、右 6 列がすべて同一。**`settled_fail_count = 0`、`(3.53) closure` 成立、$\lvert\mathrm{GTSh}\rvert=\lvert\ker\rvert\times\varphi(2N_{\rm ord})$(χ̃ 全射)も 24/24。

### 3.3 判定

> ### **予想 PASSPORT: 支持(反証されず)**【24 窓 machine-measured・GAP 単系統】
> $N_{\rm gen}$ が 3,5,6 の passport でも、**別 Nielsen 類から作った窓の GTSh は完全に一致する**。
> しかも「別の窓」は名ばかりではない: **§3.4 により、相異なる $C_{S_n}(w_0)$-軌道は $B_3$ の相異なる正規部分群 $N$ を与える。**

### 3.4 補題(軌道 ⟹ 相異なる窓)【proof・$\varepsilon=0$ の場合】

> $n\ge7$、$n\ne6$、$\varepsilon=0$($E=A_n\times S_3$)とする。$(a_1,b_1)$ と $(a_1',b_1')$ が同じ $w_0$ をもつとき、
> $$\ker(B_3\to E)=\ker(B_3\to E')\iff (a_1',b_1')=(a_1^x,b_1^x)\ \exists x\in C_{S_n}(w_0).$$
> すなわち **Nielsen 類 = 窓 $N\trianglelefteq B_3$**。
> **証明.** 二つの全射 $B_3\twoheadrightarrow E$ の核が一致 $\iff$ 両者が $\varphi\in\operatorname{Aut}(E)$ で移り合う。$Z(A_n\times S_3)=1$、$A_n$ も $S_3$ も直既約、$A_n\not\cong S_3$ ゆえ Krull–Remak–Schmidt から $\operatorname{Aut}(A_n\times S_3)=\operatorname{Aut}(A_n)\times\operatorname{Aut}(S_3)=S_n\times S_3$。$\varphi=(\text{conj}_x,\text{conj}_y)$ が $a\mapsto a'$、$b\mapsto b'$ を満たすには第 2 成分で $(1\,3)^y=(1\,3)$ かつ $(1\,3\,2)^y=(1\,3\,2)$、ゆえに $y\in\langle(1\,3)\rangle\cap\langle(1\,3\,2)\rangle=1$。残る $x\in S_n$ が $a_1^x=a_1'$、$b_1^x=b_1'$ を与え、$w_0^x=w_0$ より $x\in C_{S_n}(w_0)$。逆は明らか。∎
> **⟹ $\lambda=(9,1)$、$n=10$ には $B_3$ の相異なる正規部分群が 6 本あり、その 6 本の $\mathrm{GTSh}(N,N)$ がすべて $[54,6]$ に同型である。**($\varepsilon=1$ の $E=S_n\times_{C_2}S_3$ では $\operatorname{Aut}(E)$ を確認していない — **UNKNOWN**。)

### 3.5 部分的には**定理**である(PASSPORT の核部分)

> ### 命題 A【定理・SURV+ から 2 行】
> 同じ $n$・同じ $w_0$ の巡回型をもつ任意の窓に対し
> $$C_{S_n}(w_0)\ \subseteq\ \Xi(\ker\widetilde\chi)\ \subseteq\ C_{S_n}(w_0^2)$$
> で、**両端は passport だけで決まる**。とくに $w_0$ が偶長巡回をもたない($p=s=0$)なら両端が一致し、
> $$\Xi(\ker\widetilde\chi)=C_{S_n}(w_0)\quad\text{は passport だけの関数}$$
> — **この族では予想 PASSPORT の「核方向」は定理である**(定理 CENT-0 の窓非依存性の言い換え)。
> 残る未知は (i) $\Xi$ の単射性、(ii) $m\ne0$ 層、(iii) 拡大類。実測 24/24 ではこの 3 つも passport だけで決まっている。
>
> **【後刻の強化・§7.4】** 同日・別セッションの T3 稿(定理 XI-C + XI-INJ)により $\ker\widetilde\chi\cong C_{S_n}(w_0)$ が **$p,s$ の制限なしで定理**となった。ゆえに命題 A の $p=s=0$ 制限は外れ、**予想 PASSPORT の「核方向」は全族で定理**。残る未知は (ii)(iii) の 2 つだけ(【GAP-P1】【GAP-P2】・§8.2)。上の (i) は T3 稿 XI-INJ で解決済み。

---

## 4. 【本稿の主結果】剛性 $N$ の正体 — SAT-RIG の訂正

### 4.1 実験(`expA_measure.g` Part A)

$n=10$、$\lambda=(9,1)$、基点 = 工房 canonical 窓 `W-E-A10-9t1`。$v:=a_1b_1^{-1}$ を固定し、$\mathcal F(v)$ の **54 個すべて**に、judge 実物の $m=0$ 条件を当てた($f_{\rm judge}=a_1\cdot g$、訂正版 SURV の向き)。

| 軌道 | 大きさ | (3.10) | (3.11) | 全射 | **settled** | **shadow** |
|---|---|---|---|---|---|---|
| #1 | 9 | 9 | 9 | 9 | **0** | **0** |
| **#2(基点)** | 9 | 9 | 9 | 9 | **9** | **9** |
| #3 | 9 | 9 | 9 | 9 | **0** | **0** |
| #4 | 9 | 9 | 9 | 9 | **0** | **0** |
| #5 | 9 | 9 | 9 | 9 | **0** | **0** |
| #6 | 9 | 9 | 9 | 9 | **0** | **0** |
| 計 | **54** | 54 | 54 | 54 | **9** | **9** |

**⟹ $N_{\rm shadow}=1$、$N_{\rm gen}=6$。予言 (P6) は完全に的中。**

### 4.2 何が誤りだったか

> ### 訂正【反証・実データ + 機構】
> `sat_l1_v1` §6.2 定理 SAT-RIG の
> - **(a)**「定理 RED により $\ker\widetilde\chi\leftrightarrow\mathcal F(v)$」 — **偽**。正しくは $\ker\widetilde\chi\hookrightarrow\mathcal F(v)$(基点軌道への埋め込み)。
> - **(c)**「$\lvert\ker\rvert=\lvert C_{S_n}(v)\rvert\cdot N$、$N$ = Nielsen 類の個数」 — **偽**。$N$ は $N_{\rm shadow}$ でなければならない。
> - **(d)**「飽和 $\iff N=1\iff$ 剛性」 — **偽**。$\lambda=(9,1)$ は $N_{\rm gen}=6$ でありながら飽和($\lvert\ker\rvert=\lvert C\rvert$)している。
>
> 同ノート §10.6.2「教訓 2」の「**剛性 $N_{\rm gen}=1$ が計数機構でも追認された**」は**誤った推論**である。計数機構自身の表の比 $T_{\rm trans}/\lvert C\rvert$ は $6,\,3,\,3,\,13/2,\,71/5,\,108,\,23$ … と **1 から遠い**値ばかりで、$N_{\rm gen}=1$ を一度も支持していなかった。

### 4.3 正しい機構(紙・2 行)

> ### 補題 SET(settled 節の $m=0$ 形)【proof】
> $f\in P$ が $m=0$ の GT-shadow であるためには、$T_{0,f}:\bar x\mapsto\bar x,\ \bar y\mapsto f\bar yf^{-1}$ が $P=\langle\bar x,\bar y\rangle$ の**自己準同型**であることが必要(定義)。全射条件と併せると $T_{0,f}\in\operatorname{Aut}(A_n)=S_n$、すなわち
> $$\exists\,\alpha\in S_n:\quad \bar x^{\alpha}=\bar x,\quad \bar y^{\alpha}=f\bar yf^{-1}.$$
> ゆえに $\boxed{\ f\in C_{S_n}(\bar y)\cdot C_{S_n}(\bar x)\ }$ が **hexagon とは独立な必要条件**であり、この $\alpha$ こそ $\Xi(f)$ である。
> **証明.** $T_{0,f}$ が自己準同型かつ像が $P$ を生成 ⟹ 全射自己準同型 ⟹(有限群)自己同型。$\operatorname{Aut}(A_n)=S_n$($n\ne6$)は共役で実現される。$\bar x$ が固定されるので $\alpha\in C_{S_n}(\bar x)$。∎

**これが judge の Ξ-制限走査(命題 3.1)の正当化そのものであり、同時に「なぜ基点軌道以外が全滅するか」の説明である**: 別の Nielsen 類の $(g,h)$ から作った $f$ は hexagon を満たすが、$\bar y^{f}$ を実現する $\alpha$ が $C_{S_n}(\bar x)$ の外に出る。

### 4.4 工程への含意

- **【GAP-C1】(剛性 $N=1$ の証明 = 「本丸の後継」)は標的が誤っていた。** 予想 CENT の $\subseteq$ を「Frobenius 指標和で $N=1$ を出す」経路で証明しようとするのは、**証明できない命題を証明しようとしている**(反例 $n=10$)。正しい経路は補題 SET(定義側)+「$\Xi$ が基点軌道の外に出ない」ことの直接論証 — **これは T3 稿の定理 XI-C + XI-INJ で完了しており、予想 CENT は定理**(§7.4・§8.2)。
- **`sat_l1_v1` §9.2 の文献要請(剛性 $N=1$ の判定条件)は失効**: 求めていた「$N=1$ の判定条件」は CENT には不要になった(困難そのものが消えた)。$N$ 自体の閉形は T3 稿が平面木で与えている。
- **壁 P4(P-WALL-2)は無傷**: 結論 WALL は SURV+ の**下限のみ**を使っており、$N_{\rm gen}$ に一切依存しない。しかも SURV の $f_z$ が settled 節を通ることは**紙で言える**: 定理 SURV(iii) より $T_{0,f_z}$ は $E$ 全体の共役 $\operatorname{conj}_z$ に延びるので、$B_3/N$ 水準で well-defined な自己同型である(実測でも基点軌道 9/9 が settled を通過・§4.1)。今回の訂正は壁に触れない。
- **CENT の実データはむしろ強化された**: 剛性が破れている窓 21 本を含む 24 窓で $\Xi(\ker)=C_{S_n}(w_0)$ が成立。**CENT は剛性より弱い仮定で立つ**。

---

## 5. H2(予想 SPIN)の第一測定 — **否定的**

`expA_spin.g`(ctbllib `2.A10`・`A10`・factor fusion)。

| $A_{10}$ の型 | $2\cdot A_{10}$ での原像 | 位数 |
|---|---|---|
| $2^41^2$(= $a_1$ の型) | **1 類**(割れない) | [2] |
| $3^31$(= $b_1$ の型) | 2 類 | [3, 6] |
| $(7,3)$(= $w_0$ の型) | 2 類 | [21, 42] |

$v$ の 4 つの持ち上げ類すべてで、類乗法係数 $\#\{(\tilde h,\tilde g):\tilde h\tilde g=\tilde v\}$ は **126 で一定**。

> ### 判定(H2)【否定・機構つき】
> **対合類 $2^k1^*$ の原像が $2\cdot A_n$ で割れない**ため、$\tilde g$ と $z\tilde g$ が共役になり、$g$ の「標準的持ち上げ」が存在しない。ゆえに Fried–Serre 型の持ち上げ不変量は**この族では well-defined ですらない**(相対版 $\tilde g_i:=\tilde g_1^{\tilde x_i}$ も $x_i$ の取り方に依存してしまう)。
> ⟹ **予想 SPIN(「N≥2 の最小例で不変量が 2 値に割れる」)は、少なくとも $n=10,\lambda=(7,3)$ では成立しない**。発案係自身が挙げた「破綻しそうな点」(不変量が無情報)が実際に起きた。
> **格**: これは「持ち上げ不変量が Nielsen 類を分離しない」の**否定的確定**であって、「別の spin 型不変量が存在しない」の証明ではない。

---

## 6. Sol F88-2.6 への回答 — 「窓の E-構造の追加情報」の正体

$C_{S_n}(w_0)$-軌道(Nielsen 類)は、passport の**外**にある情報である。それが**何によって見えるか**を実測した(`expA_spin.g` (i))。$a_1,b_1$ の語 $(a_1b_1^{e_1})(a_1b_1^{e_2})\cdots$($e_i\in\{1,2\}$、音節長 $L$)の巡回型の一覧を軌道の署名とする:

| passport | $N_{\rm gen}$ | $L\le3$ | $L\le4$ | $L\le5$ | $L\le6$ | $L\le7$ |
|---|---|---|---|---|---|---|
| (9,1) | 6 | 3 | 3 | 3 | **6** | 6 |
| (8,2) | 3 | 2 | 2 | 2 | **3** | 3 |
| (7,3) | 3 | 2 | 2 | 2 | **3** | 3 |
| (6,4) | 3 | 2 | 2 | 2 | **3** | 3 |
| (10) | 5 | 3 | 3 | 3 | **5** | 5 |

> ### 回答(名指し)
> **追加情報 = Nielsen 類**。それは「$w$ の巡回型」(= passport)**ではない**(発案係 H1 の名指しはここを外している)。実体は**音節長 6 の語の巡回型**という初等的な量で完全に分離される。
> そして **GTSh はこの情報を完全に忘れる**(§3 の 24/24 一致)。すなわち $\mathrm{GTSh}$ 構成は「$B_3$ の窓 $N$」から「passport」への**忘却写像を経由する**、というのが実測から見える像である(candidate)。

---

## 7. 既存台帳との突合(新規性 grep — 誇張回避)

### 7.1 **工房は既にこの実験の半分を実行していた**

`search/strike-a13-ladder.g` の sibling 窓 `W-E-A10-9t1-o2 … -o6` の $a_1$ は、**本稿の軌道 #2〜#6 の代表と permutation として完全一致**(機械照合済み・`expA_measure.g` が「6 窓が 6 つの相異なる軌道か: PASS」を出力)。canonical `W-E-A10-9t1` は軌道 #1。
したがって:

- **「同じ passport・別 Nielsen 類の 6 窓が同じ GTSh を与える」という事実は、2026-07-30 の梯子キャンペーンで既に取得されていた**(`a13_ladder_W_E_A10_9t1*_20260730.json`: 6 窓すべて `1_group_order=54`, `2_ker_size=9`, `6_K_struct=C9`, `9_Q_struct_description=C6`)。さらに $(9,2)$ に 3 窓、$(9,2,1)$ に 3 窓の同種データがある。
- **本稿の新規部分**は次の 4 点に限る:
 1. その 6 窓が **$C_{S_{10}}(w_0)$-軌道の完全代表系**であること(= $N_{\rm gen}=6$ でそれ以上ないこと)の**証明つき同定**。
 2. **CENT-0 の外**の passport ((8,2)/(6,4)/(10)/(7,4))への拡張 — 核が定理で決まらない場所での PASSPORT 検証。
 3. **§4 の訂正**(SAT-RIG の反証)— これは既存台帳にない。
 4. **§2.4 の最小性**(n ≤ 9 で $N_{\rm gen}\ge2$ が存在しないことの厳密な排除)。
- 「初」「未解決」の断定はしない。梯子キャンペーンの 6 窓が先行実例である。

### 7.2 予想 CENT との関係

11 窓表(sat_l1_v1 §6.1)+ 本稿 24 窓 = **CENT は 35 窓で無反証**。本稿の寄与は「**剛性が破れている 21 窓でも CENT が立つ**」という質的に新しい型のデータ。

### 7.3 T3 稿との**二手法一致**(cross-check)

同日・別セッションの `docs/notes/t3_quasi_purecycle_rigidity_v1.md` は、同じ $N$ を**平面木の Catalan 計数**(定理 T3-N0)で閉評価している:
$$N=\mathrm{Cat}(m-1)\cdot\frac{m!}{t!\,f_2!\,f_3!},\qquad m=t+f_2+f_3-1=j-t+1 .$$
本稿の値は Frobenius 指標和 + 巡回集合分割 Möbius(補題 CLEAN で $T_{\rm gen}=T_{\rm trans}$ が厳密)から出ており、**道具が完全に別**である。突合:

| n | λ | $(k,j)$ | $(f_2,f_3)$ | 本稿(指標和) | T3 稿(平面木) |
|---|---|---|---|---|---|
| 16 | $(13,1^3)$ | (8,5) | (0,1) | **2** | **2** ✓ |
| 20 | $(17,1^3)$ | (10,6) | (0,2) | **10** | **10** ✓ |
| 24 | $(19,1^5)$ | (12,8) | (0,0) | **1** | **1** ✓ |

**3 点で完全一致(検算: `search/probe/wac_v1/expA_treecheck.py`)。** これは単系統の値ではなく **cross-checked** と呼んでよい型の一致である(片方は指標理論、片方は組合せ論)。
T3 稿はさらに「$N=1$ となるのは $\{t,f_2,f_3\}\in\{\{1,1,0\},\{2,1,0\},\{5,0,0\}\}$ に限る」まで進めており、Jordan 安全域での唯一例が **P-WALL-2($n=24$)**であることを示している。**したがって「この族で $N=1$」という T3 の当初標的が偽であることは、本稿の 2 例だけでなく T3 稿の分類で完全に決着している。**

### 7.4 §4(SAT-RIG の訂正)は**独立な二重発見**である — 誇張回避のための明記

T3 稿 ①②③④ は、本稿 §4 と**同じ訂正に別経路で到達している**:

| | 本稿 §4 | T3 稿 |
|---|---|---|
| 発見経路 | passport 走査 → $N_{\rm gen}=6$ の窓で $\mathcal F(v)$ 54 個に judge 条件を全数適用 | `kerchi-judge.g` 146–215 行の受理条件を直接読解 → 同じ $n=10$ 窓で $90\to54\to9$ |
| settled 節の同定 | 補題 SET($f\in C(\bar y)C(\bar x)$) | 定理 XI-C($\Xi(\ker)\subseteq C_{S_n}(w)$・$\varepsilon$ 不問) |
| $\Xi$ 単射 | **UNKNOWN と申告**(§8.2 で「新しい急所」と書いた) | **定理 XI-INJ(5 行)で証明済** |
| 予想 CENT | 「剛性より弱い仮定で立つ」と実データで主張 | **定理**(XI-C + XI-INJ + SURV+ の 3 段) |

**⟹ 本稿の §4 は「初」ではない**(同日・同工房内の並行成果)。ただし発見経路が独立なので、**訂正そのものの信頼度は二重取得で上がった**と読むのが正しい。
**⟹ 本稿 §3.5 の命題 A($p=s=0$ での核方向 passport 不変性)は、T3 稿 ④ により $p,s$ の制限なしに強化される**: $\ker\widetilde\chi\cong C_{S_n}(w_0)$ が定理なら、**予想 PASSPORT の「核方向」は全族で定理**である。残る未知は **$m\ne0$ 層と拡大類の 2 つだけ**になり、§3 の 24 窓一致はまさにその 2 つに対する実データである。

---

## 8. 残ギャップ・格付け・要請

### 8.1 格付け表

| 主張 | 格 |
|---|---|
| 補題 CLEAN(素数 $\ell$、$n/2<\ell\le n-3$ ⟹ 推移 ⟹ 原始 ⟹ $\supseteq A_n$) | **proof**(古典 Jordan に依拠。T3 稿 補題 J と同一) |
| 最小 $N_{\rm gen}\ge2$ passport = $n=10$、$n\le9$ で不存在 | **厳密**(上界 $R$ + 直接悉皆) |
| $N_{\rm gen}$ の値(表 §2.3・§2.5) | **二経路一致**($n\le11$: 指標和 × 直接悉皆)/ **cross-checked**(§7.3: 指標和 × 平面木閉形、3 点) |
| **予想 PASSPORT** | **candidate・24 窓 machine-measured で無反証**(GAP 単系統)。**核方向は T3 稿 ④ により定理**、残るは 【GAP-P1】【GAP-P2】 |
| 補題(軌道 ⟺ 相異なる $N\trianglelefteq B_3$)§3.4 | **proof**($\varepsilon=0$)/ $\varepsilon=1$ は **UNKNOWN** |
| 命題 A(核方向の passport 不変性、$p=s=0$) | **定理**。ただし T3 稿 ④($p,s$ 制限なし)に**吸収される** |
| **SAT-RIG (a)(c)(d) の反証** §4 | **反証(明示実データ)+ 機構 proof(補題 SET)**。**「初」ではない — T3 稿と独立二重発見**(§7.4) |
| $N_{\rm shadow}=1$ が**常に**成り立つか | 本稿では **UNKNOWN と申告**。**T3 稿 XI-C + XI-INJ で定理**(§7.4) |
| H2(予想 SPIN) | **否定的**(持ち上げ不変量が well-defined でない・機構同定済) |
| 語署名が Nielsen 類を分離($L\le6$) | **実データ**(5 passport・20 軌道) |

### 8.2 【GAP-C1】の差し替え — **既に閉じている**

私が「新しい急所」と書いた
> **【GAP-C2】** $N_{\rm shadow}=1$、すなわち「$f\in\mathcal F(v)$ かつ $\exists\alpha\in C_{S_n}(\bar x):\bar y^\alpha=f\bar yf^{-1}$」$\Rightarrow$「$(fa_1,fb_1^{-1})$ は基点の $C_{S_n}(v)$-軌道に入る」

は、**T3 稿の定理 XI-C(settled ⟹ $\Xi(\ker)\subseteq C_{S_n}(w)$)+ 定理 XI-INJ($\Xi$ 単射・5 行)で既に証明されている**(§7.4)。私が UNKNOWN と申告した「$\Xi$ 単射」がまさにその 5 行である。
**⟹ 予想 CENT は定理に昇格済み。$\ker\widetilde\chi\cong C_{S_n}(w_0)$。** 本稿はこの結論を 24 窓で独立に追認した位置づけになる。

**したがって PASSPORT について残る真の未知は 2 つだけ**:
> **【GAP-P1】** $m\ne0$ 層の個数 $N_m$ が passport だけで決まるか(【GAP-M】の $u_m=a_1\bar y^mb_1^{-1}$ 公式が正しければ、$u_m$ の巡回型が窓に依らないことを示せばよい)。実測 24/24 で $\lvert\mathrm{GTSh}\rvert=\lvert\ker\rvert\cdot\varphi(2N_{\rm ord})$。
> **【GAP-P2】** 拡大類 $1\to\ker\widetilde\chi\to\mathrm{GTSh}\to Q\to1$ が passport だけで決まるか。実測 24/24 で IdGroup 一致(例: $(7,3)$ で $[252,26]=S_3\times(C_7{:}C_6)$)。
> この 2 つが立てば **予想 PASSPORT は定理**になる。

### 8.3 【文献要請】

**(a)(旧要請・撤回)** 「$(\ell,1^t)$ 型での $N_{\rm gen}$ の閉形」は **T3 稿の定理 T3-N0 が種数 0 で与えている**ので取り下げる(種数 $\ge1$ の要請は T3 稿 §8 に既出)。

**(b)(本稿からの新規要請・1 件)**
> **困難**: 同じ passport をもつ複数の Nielsen 類($(2^k1^{f_2},3^j1^{f_3},\lambda)$、$G=A_n$ or $S_n$、3 分岐点)から作った有限商 $E=G\times S_3$ の**族としての比較**をしたい。本稿の実測では、Nielsen 類が違っても $\mathrm{GTSh}(N,N)$ が同型になる(24/24)。
> **欲しい結果の型**: (i) 「passport は同じだが $S_n$-共役でない 3 点分岐データ(= 別 Nielsen 類)から作った有限商が、**それでも同型な GT 型不変量を与える**」ことを説明する定理。Hurwitz 空間の言葉なら「同一 passport の異なる連結成分の**モノドロミー的不変量が一致する**」型。 (ii) Nielsen 類を分ける不変量の一覧で、**持ち上げ不変量(§5 で無効と判定済)以外**に何があるか。
> **注**: 正典外なので自分では漁っていない(文献ゲート遵守)。これが降りれば 【GAP-P1】【GAP-P2】(= 予想 PASSPORT の定理化)に直結する。

**融合説の排除(自前で済んだ)**: 「6 軌道は $S_{10}$-共役では 1 つに融合するのでは(だから同型なのは当たり前)」という説明は**成り立たない**。$(a_1',b_1')=(a_1^x,b_1^x)$ なら $w_0^x=w_0$ すなわち $x\in C_{S_{10}}(w_0)$ で同一軌道に戻るからである(§3.4 の証明の一部)。**実データでも裏が取れている**: §6 の語署名は $S_n$-共役不変量であり、$L\le6$ で **6 軌道に 6 個の相異なる署名**を与えた ⟹ 6 対は互いに $S_{10}$-共役でない。**⟹ PASSPORT の一致は自明な同一視の産物ではない。**

### 8.4 訂正が必要な既存文書(司令塔裁定事項)

1. `docs/notes/sat_l1_v1.md` §6.2 定理 SAT-RIG (a)(c)(d) — **反証**(本稿 §4 と T3 稿 ① の二重取得)。§10.6.2「教訓 2」— **誤推論**。§9.1【GAP-C1】— **失効**(T3 稿 XI-C/XI-INJ で CENT が定理化されたため)。§9.2 文献要請 — **撤回**。
2. `provenance/CLAIMS.md` に「剛性 $N=1$」系の主張が登録されていれば **格下げ**。逆に **予想 CENT は candidate → 定理へ格上げ**(根拠は T3 稿。本稿は 24 窓の独立追認)。
3. `ideas/ideas_014` H1 の「追加情報の正体は w の巡回型」— **外れ**(正体は Nielsen 類・§6)。H1 本体(PASSPORT)は**支持**(24/24・核方向は定理)。H2(SPIN)は **否定的**(§5)。H1 の「検証の一手目 ①」は本稿で実行完了。
4. **本稿と T3 稿は同日・同工房の並行成果**であり、SAT-RIG 訂正の「初」は**どちらにも帰属させない**(§7.4)。司令塔の統合時に、$N$ の閉形は T3 稿、passport 比較の実データは本稿、と役割分担して引用されたい。

---

## 9. 検算(GAP 4.16.0・`gap.ps1`・単系統)

| スクリプト | 内容 | 結果 |
|---|---|---|
| `search/probe/wac_v1/expA_scan.g` | $n=8..20$ 全 λ の $T_{\rm all}/T_{\rm trans}$、clean 判定、$N_{\rm gen}$ | I1 較正 9/9 PASS・I2 違反 0・clean で $N_{\rm gen}\ge2$ が 76 本 |
| `search/probe/wac_v1/expA_verify.g` | $n\le11$ の直接悉皆(第二経路)+ 軌道代表抽出 | J1 9/9 PASS・J2 PASS・$n\le9$ で $T_{\rm gen}=0$ or $N\le1$ |
| `search/probe/wac_v1/expA_measure.g` | (A) $\mathcal F(v)$ 54 個への judge 実物条件 / (B) $(7,3)$ 3 窓の GTSh | K1〜K4 全 PASS・$N_{\rm shadow}=1$ vs $N_{\rm gen}=6$ |
| `search/probe/wac_v1/expA_batch.g` | 7 passport × 全 Nielsen 類 = 24 窓の GTSh | L1 全 PASS(passport ごと完全一致)・L2 全 PASS(CENT) |
| `search/probe/wac_v1/expA_spin.g` | 語署名の分離 + $2\cdot A_{10}$ 持ち上げ不変量 | $L\le6$ で全分離・対合類の原像は割れない |

証明書: `search/certs/expA_passport_20260731.json`(schema `expA-passport/v1`)、`search/certs/expA_passport_batch_20260731.json`(schema `expA-passport-batch/v1`)。両者とも **`f_orientation: "judge"`** 欄あり。

**単系統(GAP のみ)。cross-checked ではない**(ただし §2.3 の指標和 × 直接悉皆の一致、および §7.1 の梯子 cert(python 独立実装)との突合は独立性の高い一致)。**Lean verified ではない。**
