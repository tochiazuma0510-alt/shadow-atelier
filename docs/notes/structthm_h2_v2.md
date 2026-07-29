# 構造定理 v2 — STR-1(内部分解型)・H2′ パッケージ・$H^2$ 判定

作成: 数学者(Opus 5)・2026-07-30(裁定 214 工程 1)
**本ノートが正本**。`docs/notes/structthm_h2_v1.md` は**凍結**(erratum 方式・上書きしない)。
入力: Sol 便 85(`sol/sol_reply_85_math12.md` §3)の FAIL 3 件 + 修理案 P85-2 / v1 の実測 / `docs/notes/a13_prediction_v1.md` §3.0.1(補題 H2′ の初出・**本 v2 で訂正して収蔵**)
凍結済み予言(41b8698・P-STR 系)には非接触。

---

## 0. v1 からの差分(erratum 一覧)

| # | v1 の記述 | 判定 | v2 での処置 |
|---|---|---|---|
| E-1 | STR-1(3)(a) $G\cong S\times(A\rtimes Q)$(抽象同型) | **FAIL**(F85-3.2) | **(a$_{\rm int}$) 内部分解型へ retype**。抽象同型版は (a$_{\rm abs}$) として「(a$_{\rm int}$) の帰結」に格下げ(逆は主張しない) |
| E-2 | STR-1(4) $\mathrm{dl}(G)=\max(\mathrm{dl}(S),2)$ | **FAIL**(F85-3.3) | 一般式 $\mathrm{dl}(G)=\max(\mathrm{dl}(S),\mathrm{dl}(A\rtimes Q))$ を本文へ。$2$ への特殊化は **Hol 型窓の系 STR-1.4c** に分離。反例 $D_8\times S_4$ を明記 |
| E-3 | 補題 H2′(a13_prediction §3.0.1)「$Q\ne1\Rightarrow A^Q=0$」 | **FAIL**(F85-3.6) | **偽**。反例 $Q=\langle4\rangle\cong C_3\le(\mathbb Z/9)^\times$、$A=C_3$($4\equiv1\bmod3$)。三分割(H2′-exist / H2′-uniq / Cyclic criterion)へ再編・適用欄を訂正 |
| E-4 | (H2′) を非アーベル $A$ へ | (v1 では未主張) | F85-3.7 を注記として収蔵:**通常の $H^2(Q;A)$ では移植不可**(pointed-set obstruction が要る) |
| — | 証明核(F85-3.1 の 1〜6)・$H^2$ 計算・実測・§5〜§9 | **PASS** | v1 のまま継承(下に再掲) |

> **Sol の総評に同意**: FAIL は**中心拡大の証明核の崩壊ではない**。(a) の型と dl 系の分離、H2′ の適用欄訂正で紙上 PASS にできる。**E-1〜E-3 はいずれも私(起草者)の責**である。

---

## 1. 設定と実測入力(v1 §1 から変更なし)

| 窓 | $N_{\rm ord}$ | $\lvert G\rvert$ | $K$ | $Q$ | $\gcd(N,\lvert Q\rvert)$ |
|---|---|---|---|---|---|
| A16-11a | 11 | 880 | $C_{11}\times D_8$ | $C_{10}$ | 1 |
| A18-13a | 13 | 1248 | $C_{13}\times D_8$ | $C_{12}$ | 1 |
| A20-15a | 15 | 960 | $C_{15}\times D_8$ | $C_4\times C_2$ | 1 |

$Q\cong\mathrm{Aut}(C_N)=(\mathbb Z/N)^\times$、$C_N$ 上の作用は忠実、$\tilde\chi$ は全射。
**KE-o の群論的正体**(v1 §1 のまま): 「$Q$ は $K^{\rm ab}$ の 2-部分を固定」$\iff$ **(H3) $G=S\cdot C_G(S)$**。$\ker(\mathrm{Aut}(D_8)\to\mathrm{Aut}(D_8^{\rm ab}))=\mathrm{Inn}(D_8)$ による。実測 $\lvert G/C_G(D_8)\rvert=4=\lvert\mathrm{Inn}(D_8)\rvert$(三窓)。

---

## 2. 【STR-1 v2】還元定理(内部分解型)

> **定理 STR-1(v2).** 有限群 $G$、$K\trianglelefteq G$、$Q=G/K$。
> - **(H1)** $K=A\times S$、$A$ 奇位数アーベル、$S=\mathrm{Syl}_2(K)$、$Z(S)=\langle z\rangle\cong C_2$。
> - **(H2)** $\gcd(\lvert A\rvert,\lvert Q\rvert)=1$。 【§3 で (H2′) に弱められる】
> - **(H3)** $G=S\cdot C_G(S)$。
>
> **(1)** $A,S\trianglelefteq G$、$z\in Z(G)$、$G=S\circ_{\langle z\rangle}C_G(S)$、$\lvert C_G(S)\rvert=2\lvert A\rvert\lvert Q\rvert$。
> **(2)** $\bar C:=C_G(S)/A$ は中心拡大 $1\to\langle z\rangle\to\bar C\to Q\to1$。その類を $\varepsilon\in H^2(Q;C_2)$ とおく。
> **(3)** 次は同値:
> - **(a$_{\rm int}$)**〔**v2 で retype**〕 **$X\le C_G(S)$ が存在して $A\trianglelefteq X$、$X/A\cong Q$、$G=S\times X$(内部直積)。さらに $X\cong A\rtimes Q$。**
> - **(b)** $K$ の補群を $C_G(S)$ の内部に取れる。
> - **(c)** $\varepsilon=0$。
> - **(d)** $z\notin\Phi(\mathrm{Syl}_2(\bar C))$。
>
> **(4)**〔**v2 で訂正**〕 (a$_{\rm int}$) の下で $\mathrm{Syl}_2(G)\cong S\times\mathrm{Syl}_2(Q)$ かつ
> $$\mathrm{dl}(G)=\max\bigl(\mathrm{dl}(S),\ \mathrm{dl}(A\rtimes Q)\bigr).$$
> **(5)** $H^2(Q;Z(K))\cong H^2(Q;C_2)$((H2) または $H^2(Q;A)=0$ による)。
> **(6)** $\mathrm{Syl}_2(Q)$ が巡回なら、$\varepsilon=0$ $\iff$ $\mathrm{Syl}_2(Q)$ の唯一の対合 $\iota$ の $C_G(S)$ における逆像が $A\langle z\rangle$ の外に位数 2 の元を含む。

### 2.1 (a$_{\rm int}$) と (a$_{\rm abs}$) の区別(F85-3.2 への対応)

$$\text{(a}_{\rm abs}\text{)}\quad G\cong S\times(A\rtimes Q)\ \text{(抽象同型)}$$

> **(a$_{\rm int}$) $\Rightarrow$ (a$_{\rm abs}$) は自明。逆は本定理では主張しない。**
> 理由(Sol の指摘そのもの): 証明の (a)$\Rightarrow$(c) は「$G=S\times X$ で $A\trianglelefteq X$、$X/A\cong Q$」という**定理データ $S,A,K$ を尊重する内部分解**を使う。抽象同型は、その同型が定理データの $S,A$ を各因子へ送ることを含意しない。よって v1 の (a) は**証明と逐語一致していなかった**。

### 2.2 証明(v1 から (a) の型のみ差し替え・他は F85-3.1 で PASS 済)

**(1)** (H1) より $K$ は冪零で $A$ は Hall $2'$、$S$ は Sylow 2、ともに $K$ の特性部分群ゆえ $G$ で正規。$Z(S)$ は特性・位数 2 で $G/C_G(z)\hookrightarrow\mathrm{Aut}(C_2)=1$ ゆえ $z\in Z(G)$。(H3) と $S\cap C_G(S)=Z(S)$ から中心積と位数。

**(2)** $A\le C_G(S)$、$C_G(S)\cap K=C_K(S)=A\times\langle z\rangle$、$C_G(S)K=G$ ゆえ $\bar C/\langle\bar z\rangle\cong Q$。$z\in Z(G)$ より中心的。

**(3)**
- **(c)$\Rightarrow$(b)**: $\varepsilon=0$ なら $\bar C=\langle\bar z\rangle\times\bar Q$。$\bar Q$ の $C_G(S)$ での逆像 $Y$ は位数 $\lvert A\rvert\lvert Q\rvert$、$Y\cap K=A$。(H2) と Schur–Zassenhaus で $A$ の補群 $H\cong Q$ が $Y\le C_G(S)$ 内に取れる。
- **(b)$\Rightarrow$(a$_{\rm int}$)**: $H\le C_G(S)$ を $K$ の補群とし $X:=AH$ とおく。$A\trianglelefteq G$ ゆえ $X\le G$、$\lvert X\rvert=\lvert A\rvert\lvert Q\rvert$、$A\trianglelefteq X$、$X/A\cong H\cong Q$。$X\le C_G(S)$($A,H$ ともに $S$ を中心化)。$S\cap X\le K\cap X=A(H\cap K)=A$ かつ $S\cap A=1$ ゆえ $S\cap X=1$。$S\cdot X=SAH=KH=G$。$[S,X]=1$。よって $G=S\times X$(内部直積)。$X$ は $A$ の $Q$ による拡大で Schur–Zassenhaus により分裂、$X\cong A\rtimes Q$。
- **(a$_{\rm int}$)$\Rightarrow$(c)**: $G=S\times X$、$X\le C_G(S)$ より $C_G(S)=Z(S)\times X$、ゆえに $\bar C=\langle\bar z\rangle\times(X/A)$、$X/A\cong Q$ ゆえ $\varepsilon=0$。
- **(c)$\Leftrightarrow$(d)**: $\langle\bar z\rangle$ はアーベル正規 2-部分群ゆえ Gaschütz で $\mathrm{Syl}_2(\bar C)$ 内の補群存在と同値。2-群 $T$ の中心の位数 2 部分群が直和因子 $\iff$ $z\notin\Phi(T)$。

**(4)** (a$_{\rm int}$) より $G=S\times X$、$X\cong A\rtimes Q$、$A$ 奇位数ゆえ $\mathrm{Syl}_2(X)\cong\mathrm{Syl}_2(Q)$。導来長は直積で $\max$。

**(6)** $H^2(Q;C_2)$ は 2-torsion ゆえ $\mathrm{cor}\circ\mathrm{res}=[Q:Q_2]$(奇)で $\mathrm{res}$ 単射。$Q_2$ 巡回位数 $2^a$ のとき非自明類は $C_{2^{a+1}}\twoheadrightarrow C_{2^a}$ で、唯一の位数 2 部分群への制限は位数 4 巡回 = 非分裂ゆえ再制限も単射。$\square$

### 2.3 導来長の系(F85-3.3 への対応)

> **反例(Sol)**: $G=D_8\times S_4$、$K=D_8$、$A=1$、$Q=S_4$。(H1)(H2)(H3) と $\varepsilon=0$ が全て成立するが
> $$\mathrm{dl}(G)=3\ \ne\ \max(\mathrm{dl}(D_8),2)=2 .$$
> ゆえに **v1 の「$\mathrm{dl}(G)=\max(\mathrm{dl}(S),2)$」は STR-1 の系ではない**。

> **系 STR-1.4c(Hol 型窓へ限定した正しい形).** (a$_{\rm int}$) に加えて $A\rtimes Q\cong\mathrm{Hol}(C_N)$($A=C_N$ 巡回、$Q\le\mathrm{Aut}(C_N)$)が成り立つ窓では、$\mathrm{Hol}(C_N)'\le C_N$ アーベルゆえ $\mathrm{dl}(A\rtimes Q)\le2$、したがって
> $$\mathrm{dl}(G)=\max\bigl(\mathrm{dl}(S),\,2\bigr).$$
> **前件「$A\rtimes Q$ が Hol 型」は窓ごとに測る量である**(三窓では実測 = §4)。

> **尾部 8 への含意(v1 §8 の訂正版)**: $\mathrm{dl}(\mathrm{Syl}_2(S_{2^n}))=n$ ゆえ、**Hol 型かつ (a$_{\rm int}$)** の窓に限って $\mathrm{dl}(G)=3\iff t\ge8$。$A\rtimes Q$ が Hol 型でない窓では $\mathrm{dl}(A\rtimes Q)$ が独立に 3 以上になりうる($D_8\times S_4$ 型の汚染)ため、**dl-3 の観測を自動的に「$S$ 由来」と読んではならない** — これは v1 になかった警告である。

### 2.4 系 STR-1.6(維持)

$Q_2$ 巡回なら、$u=-1$ 層に「位数 2 かつ $S$ を中心化する shadow」が 1 つあれば $\varepsilon=0$。
**警告(維持・v2 で強調)**: $Q_2$ 巡回は $N$ が**素数冪**のときに保証される。$\pi(N)\ge2$ では $u=-1$ 層の判定は $\varepsilon$ の**一部のビットしか見ない**(epsilon v2 §1.5)。

---

## 3. 【H2′ パッケージ v2】(H2) を弱める(P85-2 の形をそのまま採用)

初出は `docs/notes/a13_prediction_v1.md` §3.0.1(起草者 = 私)。**その適用欄が偽であったため、ここで三分割して訂正収蔵する。**

> **H2′-exist.** $A$ を有限アーベル $Q$-加群とし $H^2(Q;A)=0$ とする。このとき STR-1(3) の **(c)$\Rightarrow$(b)** が成立する(拡大 $1\to A\to Y\to Q\to1$ の類が $H^2(Q;A)$ に住み、消滅 ⟹ 分裂)。
> **H2′-uniq.** さらに $H^1(Q;A)=0$ なら補群は $A$-共役を除いて一意。
> **Cyclic criterion.** $Q$ 巡回かつ $\boxed{A^Q=0}$ なら H2′-exist と H2′-uniq がともに成立。
> (証明: $Q=\langle\sigma\rangle$ 巡回で Tate 2 周期性 $H^2=A^Q/N_QA$、$H^1=\ker N_Q/(\sigma-1)A$。$A^Q=0$ なら $\ker(\sigma-1)=0$、$A$ 有限ゆえ $\sigma-1$ は全単射で $(\sigma-1)A=A$、また $N_Q(\sigma-1)=0$ から $N_Q=0$。よって $H^1=H^2=0$。)

> **STR-1 の TFAE 存在部分に必要なのは $H^2(Q;A)=0$ のみ**(F85-3.4)。$H^1=0$ は一意性用で**過剰**。v1 で (H2) と書いていた箇所は、存在だけが要るなら $H^2(Q;A)=0$ に置き換えてよい。

### 3.1 【訂正】「$Q\ne1\Rightarrow A^Q=0$」は偽(F85-3.6)

`a13_prediction_v1.md` §3.0.1 の
> 「$Q\le(\mathbb Z/9)^\times$ が非自明なら $A^Q=0$」

は**偽**である。**反例(Sol)**:
$$Q=\langle4\rangle\cong C_3\le(\mathbb Z/9)^\times,\qquad A=C_3,\qquad 4\equiv1\!\!\pmod 3 .$$
$Q$ は $A=C_3$ に**自明に作用**するので $A^Q=A\ne0$、$H^1(C_3;C_3)\cong H^2(C_3;C_3)\cong C_3\ne0$。

> **適用欄の訂正**: 「$\tilde\chi$ 全射、または少なくとも $Q\ne1$」→ **「$Q=C_6$(現梯子の実測)、または $A^Q=0$ を別途確認」**。
> 現梯子は $Q=C_6=\langle2\rangle$ が実測されているので、この訂正は梯子への STR-1 適用を**反転させない**(Sol も同旨)。ただし**根拠の書き方は差し替えが必要**。

### 3.2 非アーベル $A$ への移植(F85-3.7)

- **(H2) を維持するなら**: Schur–Zassenhaus は $A$ の可換性を要さない。$A$ を一般の奇位数群へ広げた STR-1 は、$Z(K)=Z(A)\times Z(S)$ 等の文言を直せば同じ方法で通る。
- **(H2′) を非アーベル $A$ へ移すことはできない**: 非アーベル核の拡大分類は通常の群値 $H^2(Q;A)$ ではない。移植するなら「関連する全ての $Y$ が分裂する」を直接前件にするか、outer action と pointed-set obstruction を明示する必要がある。**現時点では移植しない**。

---

## 4. $H^2$ の計算と判定(v1 §3 から変更なし・PASS)

$H^2(Q;Z(K))\cong H^2(Q;C_2)$(自明作用)。

| 窓 | $Q$ | $\dim Z^2$ | $\dim B^2$ | $\dim H^2(Q;C_2)$ | $\lvert H^2\rvert$ | HAP | 手計算 |
|---|---|---|---|---|---|---|---|
| A16 | $C_{10}$ | 2 | 1 | **1** | 2 | `[ 2 ]` | ✔ |
| A18 | $C_{12}$ | 3 | 2 | **1** | 2 | `[ 2 ]` | ✔ |
| A20 | $C_4\times C_2$ | 4 | 1 | **3** | 8 | `[ 2, 2, 2 ]` | ✔ |

> ### 判定 STR-3(維持):**必然ではない(NOT FORCED)**
> $H^2(Q;Z(K))\ne0$。$\varepsilon=0$ は 1+1+3 = **5 ビットの実質情報**。

**型の明記(維持)**: $K$ 非可換ゆえ $H^2(Q;K)$ は存在しない。$\varepsilon$ は **$K$-拡大の類ではなく**、中心拡大 $1\to Z(S)\to C_G(S)/A\to Q\to1$ の類。分裂拡大が複数ありうる(§6 の $D_8\circ C_4$)ため、$K$-拡大の分裂は $\varepsilon=0$ を含意しない。

---

## 5. 実測(v1 §4・§5 から変更なし)【STR-2:実測命題】

| 窓 | $\lvert C_G(D_8)\rvert$ | $G=D_8\!\cdot\!C_G(D_8)$ | $\bar C$ | $\varepsilon=0$ | $\mathrm{Syl}_2(G)$ | (a$_{\rm int}$) | $X$ |
|---|---|---|---|---|---|---|---|
| A16 | 220 | true | $C_{10}\times C_2$ | **true** | $C_2\times D_8$ | **true** | $C_{11}\!:\!C_{10}$ |
| A18 | 312 | true | $C_{12}\times C_2$ | **true** | $C_4\times D_8$ | **true** | $C_{13}\!:\!C_{12}$ |
| A20 | 240 | true | $C_4\times C_2\times C_2$ | **true** | $C_2\times C_4\times D_8$ | **true** | $(C_5\!:\!C_4)\times S_3$ |

明示同型 $G\cong D_8\times\mathrm{Hol}(\mathbb Z/N_{\rm ord})$ を三窓で構成(GAP `IsomorphismGroups`)。
**注**: 表の $X$ 欄は (a$_{\rm int}$) の $X$(= $C_G(D_8)$ 内に取った内部因子)であり、抽象同型のみの主張ではない。$X\cong\mathrm{Hol}(C_N)$ ゆえ**系 STR-1.4c の前件が三窓で成立**し、$\mathrm{dl}(G)=\max(\mathrm{dl}(D_8),2)=2$(実測 `G_derived_length = 2` と一致)。

**司令塔 I7-1 / Sol P84-1 への回答(維持)**: 作用は内部を経由($\lvert G/C_G(D_8)\rvert=4=\lvert\mathrm{Inn}(D_8)\rvert$)。補群の $C_G(D_8)$ 内取り直しは三窓とも可能(2/4・2/5・4/18 クラス)。**裁定 205 の witness 自身は三窓とも $D_8$ を中心化しない**(A16 $m=3$: false / A18 $m=2$: false, $m=1$: true / A20 $m=3$: true, $m=5$: false)。

---

## 6. 裁定 205 の推論の訂正(維持)

「分裂 + KE-o ⟹ 直積」は**偽**。反例 $\Gamma=D_8\rtimes_{\mathrm{conj}_r}C_2\cong D_8\circ C_4$(機械確認: 正規な補群 0 個、$\Gamma\not\cong D_8\times C_2$、$C_\Gamma(D_8)\cong C_4$、$\varepsilon\ne0$)。数学者・発案係 I7-1・Sol 便 84 の三者独立同着。

---

## 7. 残るギャップ

- **【GAP-1】** $\varepsilon=0$ の機構が不明(→ `epsilon_mechanism_v2.md`)。
- **【GAP-2】** $Q\cong\mathrm{Aut}(C_N)$ と $S=D_8$ は実測であり証明されていない。
- **【GAP-3(v2 で更新)】** (H2) は $N=9$ で破れる($\gcd(9,6)=3$)。**§3 の H2′-exist で回避しうる**が、その前件は「$Q$ 巡回 かつ $A^Q=0$」であり、**$Q\ne1$ では足りない**(§3.1)。$N=9$ 梯子では $Q=C_6$ 実測により回避が成立する。
- **【GAP-4(新)】** (4) の一般式に伴い、$\mathrm{dl}$ の観測から $S$ の情報を読むには $\mathrm{dl}(A\rtimes Q)$ を独立に押さえる必要がある(§2.3)。

---

## 8. 定理 candidate(Sol 再ゲート用)

> **【STR-1 v2】** §2(証明つき)。**変更点は (a$_{\rm int}$) への retype と (4) の一般式のみ**。証明核(F85-3.1 の 1〜6)は Sol PASS 済。
> **【H2′ パッケージ v2】** §3(三分割・適用欄訂正済)。
> **【STR-2】** §5(GAP 単系統の実測・cross-checked ではない)。
> **【判定 STR-3】** §4(維持)。
> **監査してほしい点**: (b)$\Rightarrow$(a$_{\rm int}$) の $X=AH$ の取り方(v1 から実質同じだが結論の型が変わった)、系 STR-1.4c の前件の書き方、§3.2 の非アーベル $A$ 注記の過不足。

---

## 9. 出所

- v1(凍結): `docs/notes/structthm_h2_v1.md`
- スクリプト: `search/_probe_structthm_h2.g`・`_witness.g`・`_counterex.g`・`_w205*.g`
- 証明書: `search/certs/.structthm_*.json`・`.structthm_wit_*.json`
- 監査: `sol/sol_reply_85_math12.md` §3(F85-3.1〜3.7・P85-2)
- H2′ 初出と訂正対象: `docs/notes/a13_prediction_v1.md` §3.0.1
