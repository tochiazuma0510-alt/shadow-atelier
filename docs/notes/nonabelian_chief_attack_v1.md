# 非可換 chief factor $S^t$ における literal residual absorption — 一撃

**状態札: 数学者起草・司令塔検分前・Sol 未監査**
**一行裁定: 成果 2(有限な必要十分 obstruction)を与える。加えて成果 1 方向の「最初に使える正確な補題」を 2 本(NA-1 = literal 残差系の明示公式・NA-5 = Sylow-3 生成元持ち上げで十分)証明する。一般の型付き十分定理は出ない — 欠品データを D1–D6 に確定して返す。**

起草: Claude 数学者 / 2026-08-18 / 委嘱 = Sol(`ops/express/20260818_sol_fable_nonabelian_chief_attack.md`)経由・司令塔振り分け。T-36 の直接の続き。
格付け: 本書の全結果は **paper candidate**(紙上証明・Sol 監査前)。機械計算ゼロ。**cross-checked ではなく verified でもない。**
非接触: 封印 3 量・$u$ の値と平方類・$c$ の値・sealed $K^{(5)}$ に非接触($u=2m+1$ は形式変数)。
**未査読文献への非依存宣言**: [BBB26](Burau $n=4$ 忠実)には**一切荷重を載せていない**。本書の結果はどれも Burau を使わない。
NAME-COLLIDE 警告:
- $c$ は正典どおり $PB_3$ の中心元 $(\sigma_1\sigma_2)^3$。**補正元は $w$** と書く。
- $\Theta$ は T-35 の comparison map。本書の補正変換は $\mathcal T$ と書き、混同しない。
- $K(5)$ = Stasheff associahedron。sealed $K^{(5)}$ と別物。
- **数値の偶然**: $|\mathrm{core}_X(A)|=162$(T-37)と $|X^2\setminus A|=162$(T33-L4)は**値が一致するだけの別対象**。

---

## 0. 何を主張し、何を主張しないか

| 項目 | 裁定 |
|---|---|
| **NA-1** literal 残差系の明示公式(3 本)。$S^t$ 段の「全 literal residual を同時に吸収する」条件を、**Wells 抜き・comparison map 抜き**で正確な有限方程式系にする | **証明**(独立検算: 可換化すると T-30 §2 の $D_3=\sum(-1)^id^i$ と**逐語一致**) |
| **NA-2** 補正領域 $W=H_{PB_3}/K_{PB_3}$ の五 coface 埋め込み $W\hookrightarrow N^5$ と、そこに欠品が集中すること | **証明** |
| **NA-3** 勘定: 拘束 11 座標 vs 自由 5 座標 ⟹ **B5/K(5) syzygy は装飾ではなく load-bearing** | **証明**(不等式として) |
| **NA-4** 役者の取り直し: $X$ の作用は**一切不要**。作用するのは $\mathcal G_3=B_3/K_{PB_3}$ と $\mathcal G_4=PB_4/K$ の共役のみ ⟹ T33-L11 の循環も T-35 の $\Theta$ も**この定式化では発生しない** | **証明** |
| **NA-5** **Sylow-3 生成元持ち上げで十分**。しかも持ち上げる各元は outside roof を持たなくてよい | **証明**(最も実用的な成果) |
| **OBS-NA** 有限な必要十分 obstruction(探索器 + 独立 checker 契約つき) | **定式化**(成果 2) |
| 一般の型付き十分定理(成果 1) | **出ない**。欠品は D1–D6 |
| 非可換段で「$3\nmid[\mathrm{ML}(H):J]$ が $S^t$ の構造から自動」 | **否**。$J$ は $N$ だけでは決まらない(§6.3 で理由) |
| B4-B | **宣言しない** |

---

## 1. 固定入力と記号

### 1.1 追加された固定入力(T-37)

$$A\not\trianglelefteq X,\qquad \mathrm{im}(X\to\mathrm{Sym}(X/A))\cong S_3,\qquad |\mathrm{core}_X(A)|=162 .$$
以後これを使う。**$A$ の正規性は仮定しない**(禁止短路)。本書の議論はすべて $A$ 非正規で成立する。

### 1.2 既定の固定入力(T-33 §2、および T-36 で証明した補題)

$|X|=972=2^2\cdot3^5$, $|A|=324=2^2\cdot3^4$, $[X:A]=3$;$A\le I_K$ と $I_K$ の群性(2008 Prop. 3.7/3.11);one-outside;段ごとの seed 差は許容;q=3 段の typed positive。
T-36 から:
- **T33-L1(単調性)** $L\le K\Rightarrow I_L\le I_K$。
- **T33-L2(二値性)** $I_K\in\{A,X\}$($A$ の正規性不要)。
- **T33-L4** $X^2=\langle x^2\rangle$ は $X$ の**唯一の(正規)Sylow 3-部分群**、$|X^2|=243$、$|A\cap X^2|=81$、$|X^2\setminus A|=162$。$I_K=X\iff I_K\cap(X^2\setminus A)\ne\varnothing$。
- **T33-T2(SYL3)** $L\le K$ isolated, $I_K=X$, $J:=\mathrm{im}(R_{L,K})$ とすると $3\nmid[\mathrm{ML}(K):J]\Rightarrow I_L=X$。
- **T33-L8** shadow の持ち上げ障害は「3 本の残差」だけ。Wells の compatible pair 存在問題は生じない。
- **T33-L9** $H_{PB_3}/K_{PB_3}\hookrightarrow(H/K)^5$、$H_{PB_2}/K_{PB_2}\hookrightarrow(H_{PB_3}/K_{PB_3})^4$。

### 1.3 本書の設定

$K\le H$ を isolated・開・$B_4$-normal・$\le PB_4$ とし、$N:=H/K\cong S^t$($S$ 非可換単純)を $B_4$-chief factor とする。$I_H=X$ は既知。置く:
$$\mathcal G_4:=PB_4/K,\quad \mathcal G_3:=B_3/K_{PB_3},\quad N=H/K\trianglelefteq B_4/K,\quad W:=H_{PB_3}/K_{PB_3}\trianglelefteq\mathcal G_3 .$$
五 coface $\varphi_{123},\varphi_{234},\varphi_{12,3,4},\varphi_{1,23,4},\varphi_{1,2,34}:PB_3\to PB_4$ は (2.4) より $K_{PB_3}\to K$, $H_{PB_3}\to H$ を満たすので、誘導準同型 $\bar\varphi_j:PB_3/K_{PB_3}\to\mathcal G_4$ とその制限 $\bar\varphi_j|_W:W\to N$ を得る。
共役記法: ${}^gz:=gzg^{-1}$、$z^g:=g^{-1}zg$。

---

## 2. NA-4 — 役者の取り直し(先に済ませる)

**補題 NA-4.** 以下の残差方程式系(§3)には、$X=\mathrm{ML}(M)$ の何物への作用も現れない。現れる作用は
$$\mathcal G_3\ \curvearrowright\ W\ (\text{共役}),\qquad \mathcal G_4\ \curvearrowright\ N\ (\text{共役})$$
の二つだけであり、いずれも有限群の literal な内部自己同型である。$X$ は **roof 写像 $\rho=R_{H,M}$ を通じて $g\in\mathrm{ML}(H)$ を選ぶときにだけ**現れる。
*証明.* §3 の公式を見れば、共役子はすべて $\mathcal G_3$ または $\mathcal G_4$ の元(literal な $H$ 段の語)であり、補正元は $W$ の元である。∎

**含意.**
1. **T33-L11(T-36)の循環はこの定式化では発生しない。** T33-L11 は「$X$ が $H_1(H_r;\mathbf F_3)$ に作用する」という前提が構成対象そのものに依存する、という指摘だった。$S^t$ 段の残差方程式は $X$-作用を必要としない。
2. **T-35 の comparison map $\Theta$ も不要。** $\Theta$ は「orbit/sign 情報を actual 窓の非零 residual へ送る」写像だったが、本定式化では residual は最初から literal に計算される量である。⟹ T-35 の `PB4-specific kappa + Theta comparison: OPEN` は、**$S^t$ 段の absorption を決めるためには迂回できる**(κ/Θ が要るのは orbit/sign 経由の間接論法の方であり、直接の残差計算には要らない)。
3. 従って禁止短路「centerless/Schreier だけからの自動 lift」「$K(5)$ 単連結性だけからの effectivity」に抵触する余地が構造的に無い — 本書はそれらの概念を一度も使わない。

---

## 3. NA-1 — literal 残差系の明示公式(**最初に使える正確な補題 I**)

### 3.1 残差の定義

$H$ 段の shadow $[(m,f)]\in\mathrm{ML}(H)$ の literal 代表 $(m,f)\in\mathbf Z\times F_2$($charming ゆえ $f\in[F_2,F_2]$ に取れる)を固定し、$\mathcal G_3$ の中で
$$A_1:=\sigma_1x_{12}^m,\quad B_1:=f^{-1}\sigma_2x_{23}^mf,\quad C_1:=f^{-1}\sigma_1\sigma_2(x_{13}x_{23})^m,\quad C_2:=\sigma_2\sigma_1(x_{12}x_{13})^mf$$
と置き、$\mathcal G_4$ の中で
$$a_1:=\varphi_{234}(f),\ a_2:=\varphi_{1,23,4}(f),\ a_3:=\varphi_{123}(f),\ a_4:=\varphi_{1,2,34}(f),\ a_5:=\varphi_{12,3,4}(f)$$
と置く。**残差**を
$$\rho_1:=(A_1B_1)C_1^{-1},\qquad \rho_2:=(B_1A_1)C_2^{-1},\qquad \rho_3:=(a_1a_2a_3)(a_4a_5)^{-1}$$
と定義する。$[(m,f)]$ が $H$ 段の shadow であることは、(2.18)(2.19)(2.20) がそれぞれ $H_{PB_3}, H_{PB_3}, H$ を法として成立することなので
$$\rho_1,\rho_2\in W,\qquad \rho_3\in N$$
であり、$K$ 段の shadow であることは $\rho_1=\rho_2=1$ in $W$、$\rho_3=1$ in $N$ と同値である(2008 Def 2.6)。

### 3.2 補正のもとでの変換公式

**補題 NA-1.** 補正 $f\mapsto f\,w$($w\in H_{PB_3}$、像も $w\in W$)に対し、$\mathcal G_3,\mathcal G_4$ の中で厳密に
$$\boxed{\ \rho_1(fw)\;=\;\rho_1\cdot{}^{C_1}\!\bigl[B_1,w\bigr]\cdot w\ }\qquad\bigl([B_1,w]:=B_1^{-1}w^{-1}B_1w\bigr)$$
$$\boxed{\ \rho_2(fw)\;=\;w^{-1}\cdot\rho_2\cdot{}^{C_2}\!\bigl(w^{A_1^{-1}}\,w^{-1}\bigr)\ }$$
$$\boxed{\ \rho_3(fw)\;=\;\rho_3\cdot{}^{(a_4a_5)}\!\bigl(P(w)\,Q(w)^{-1}\bigr)\ }$$
ここで
$$P(w):=\varphi_{234}(w)^{\,a_2a_3}\cdot\varphi_{1,23,4}(w)^{\,a_3}\cdot\varphi_{123}(w),\qquad Q(w):=\varphi_{1,2,34}(w)^{\,a_5}\cdot\varphi_{12,3,4}(w).$$
すべての因子は $W$(resp. $N$)に属する。

*証明.* $\rho_1$: $f\mapsto fw$ で $A_1B_1\mapsto A_1w^{-1}B_1w=A_1B_1\cdot[B_1,w]$、$C_1\mapsto w^{-1}C_1$。よって
$\rho_1(fw)=A_1B_1[B_1,w]\cdot C_1^{-1}w=(A_1B_1C_1^{-1})\cdot(C_1[B_1,w]C_1^{-1})\cdot w$。
$\rho_2$: $B_1A_1\mapsto w^{-1}B_1wA_1$、$C_2\mapsto C_2w$。よって
$\rho_2(fw)=w^{-1}B_1wA_1w^{-1}C_2^{-1}=w^{-1}\cdot(B_1A_1)\cdot(A_1^{-1}wA_1w^{-1})\cdot C_2^{-1}
=w^{-1}\cdot(B_1A_1C_2^{-1})\cdot C_2(w^{A_1^{-1}}w^{-1})C_2^{-1}$。
$\rho_3$: $\varphi_j(fw)=\varphi_j(f)\varphi_j(w)=a_jb_j$($b_j:=\varphi_j(w)\in N$)。
$a_1b_1a_2b_2a_3b_3=(a_1a_2a_3)\cdot b_1^{a_2a_3}b_2^{a_3}b_3=(a_1a_2a_3)P(w)$、
$a_4b_4a_5b_5=(a_4a_5)\cdot b_4^{a_5}b_5=(a_4a_5)Q(w)$。よって
$\rho_3(fw)=(a_1a_2a_3)P(w)Q(w)^{-1}(a_4a_5)^{-1}=\rho_3\cdot{}^{(a_4a_5)}(P(w)Q(w)^{-1})$。∎

**$m$ 側の補正.** $m\mapsto m+H_{\rm ord}s$ では、$\xi:=x_{12}^{H_{\rm ord}}$, $\eta:=x_{23}^{H_{\rm ord}}$, $\gamma:=c^{H_{\rm ord}}$ がいずれも $H_{PB_3}$ に属する(2008 Prop 2.3 の $H_{\rm ord}=\mathrm{lcm}(\mathrm{ord}\,x_{12},\mathrm{ord}\,x_{23},\mathrm{ord}\,c)$ と $x_{13}x_{23}=x_{12}^{-1}c$、$c$ 中心)ので、$A_1,B_1,C_1,C_2$ の各出現位置に $\xi^s,\eta^s,\xi^{-s}\gamma^s$ が literal に挿入され、同型の変換公式を与える。**これは定型の帳簿作業で、本書では書き下していない(欠品 D6)。**

### 3.3 独立検算(可換化)

$N$ が可換のとき $P(w)Q(w)^{-1}$ は
$$\varphi_{234}(w)+\varphi_{1,23,4}(w)+\varphi_{123}(w)-\varphi_{1,2,34}(w)-\varphi_{12,3,4}(w)$$
となり、T-30 §2 の順序 $d^0=\varphi_{234},d^1=\varphi_{12,3,4},d^2=\varphi_{1,23,4},d^3=\varphi_{1,2,34},d^4=\varphi_{123}$ のもとで
$$D_3=\sum_{i=0}^4(-1)^id^i$$
と**逐語一致する**。⟹ **NA-1 は T-30 §2/157cz の可換 $D_3$ の非可換持ち上げ**である。可換段で証明済みの split exactness は、この公式の可換化における像の完全性に他ならない。

### 3.4 帰結 — 「同時吸収」の正確な意味

**系 NA-1'.** $\mathcal T:=(\mathcal T_1,\mathcal T_2,\mathcal T_3):\Lambda\to W\times W\times N$ を上記の補正変換($\Lambda:=(\mathbf Z/(K_{\rm ord}/H_{\rm ord}))\times W$)とすると、
$$[(m,f)]\ \text{が}\ K\ \text{へ持ち上がる}\iff \exists\lambda\in\Lambda:\ \mathcal T(\lambda)\ \text{が}\ (\rho_1,\rho_2,\rho_3)\ \text{を}\ (1,1,1)\ \text{へ送り、かつ side gate}\ \Sigma(\lambda)\ \text{が成立}.$$
これが Sol の「許容 PB3 correction/torsor が全 literal residual を同時に吸収する」の逐語形である。**トーサーではない**: $\mathcal T$ は準同型でないので解集合は一般にトーサーではなく、$\rho_3$ については $\mathrm{Stab}$ の右剰余類、$\rho_1,\rho_2$ については twisted な集合になる(T-29 閉 3.1 の「torsor は空を非空にしない」がここでも効く)。

---

## 4. NA-2 — 欠品は補正領域 $W\hookrightarrow N^5$ に集中する

**補題 NA-2.** 写像
$$\iota:W\longrightarrow N^5,\qquad \iota(w)=\bigl(\bar\varphi_{123}(w),\bar\varphi_{234}(w),\bar\varphi_{12,3,4}(w),\bar\varphi_{1,23,4}(w),\bar\varphi_{1,2,34}(w)\bigr)$$
は**単射**である。
*証明.* $\ker\iota=\{w\in H_{PB_3}:\varphi_j(w)\in K\ \forall j\}/K_{PB_3}=\bigl(H_{PB_3}\cap\bigcap_j\varphi_j^{-1}(K)\bigr)/K_{PB_3}=K_{PB_3}/K_{PB_3}=1$。ここで (2.4) の $K_{PB_3}=\bigcap_j\varphi_j^{-1}(K)$ を使った。∎

**含意.** $\rho_3$ の補正 $P(w)Q(w)^{-1}$ は $\iota(w)$ の 5 座標だけの関数である。従って:
- $\iota(W)=N^5$(**full**)なら、$\rho_3$ の方程式単独は常に可解(例えば $\varphi_{123}$ 座標だけ動かす)。
- $\iota(W)\subsetneq N^5$ なら、その**どの部分群であるか**が可解性を決める。
⟹ **$S^t$ 段の欠品の第一項は「$\iota(W)\le N^5$ の literal 決定」である**。これが Sol の言う「PB4 固有の literal A.18 coupling」の中身の一つである(もう一つは §3 の共役子 $a_i,C_1,C_2,A_1,B_1$)。

**注意(座標の非独立性).** $\iota(W)$ は一般に部分直積ですらない可能性がある。特に各射影 $\bar\varphi_j(W)\le N$ が全射かどうかも未知である。**「$\varphi_{123}$ は strand 4 の削除で分裂するから全射」は成り立たない**:削除 $s_4$ は $s_4(H)\subseteq H_{PB_3}$ を満たすとは限らず、また $\varphi_{123}\circ s_4\ne\mathrm{id}_{PB_4}$($x_{i4}$ を殺す)なので、この短絡は使えない。⟹ 各 $\bar\varphi_j(W)$ の決定も欠品(D1)。

---

## 5. NA-3 — 勘定: 拘束 11 座標 vs 自由 5 座標、B5/K(5) の正確な役割

**補題 NA-3.** $|\mathcal T(\Lambda)|\le|\Lambda|=(K_{\rm ord}/H_{\rm ord})\cdot|W|\le(K_{\rm ord}/H_{\rm ord})\cdot|N|^5$ であるのに対し、残差の住む空間は $W\times W\times N$ で位数 $\le|N|^{11}$。従って
$$\text{「任意の $H$-shadow の残差が吸収される」}\Longrightarrow \bigl|\{\mathcal R(g):g\in\mathrm{ML}(H)\}\bigr|\le|\Lambda| .$$
*証明.* 吸収可能な残差の集合は $\mathcal T$ の像に含まれる集合の $\mathcal R$-逆像で、その濃度は $|\mathcal T(\Lambda)|\le|\Lambda|$ で抑えられる。∎

**含意(B5/K(5) の正確な役割).** 実際に現れる残差三つ組 $\mathcal R(g)$ は $W\times W\times N$ の一般の元ではなく、**arity 5 の coherence(B5/K(5) の 6 pentagon + 3 square faces)が課す syzygy** を満たす。可換段ではこの syzygy が $\ker D_2=\mathrm{im}\,D_1$(157cz の `B345_UNTWISTED_SPLIT_EXACT`)として、残差を $\mathrm{im}\,\mathcal T$ の大きさに切り詰めた。**非可換段では、この切り詰めが起きることは形式的には従わない。**
⟹ **B5/K(5) は装飾ではなく、$S^t$ 段の可解性の必要条件を作る当の装置である。** ただし本書は「K(5) が単連結だから correction が effective」とは**言わない**(禁止短路);言うのは「syzygy が残差集合を $\mathcal Z\subseteq W\times W\times N$ に制限し、absorption $\iff\mathcal Z\subseteq$(吸収可能集合)」という同値だけである。

**⟹ 非可換版の正確な missing theorem.**
> **(NA-EX)** 実際に現れる残差集合 $\mathcal Z=\mathcal R(\mathrm{ML}(H))$ が $\mathcal T(\Lambda)$ による吸収可能集合に含まれること。
これは 157cz の `B345_UNTWISTED_SPLIT_EXACT` の非可換・捻れ版であり、**可換版からは従わない**(非可換群には完全列も分裂もないため)。

---

## 6. NA-5 — Sylow-3 生成元持ち上げで十分(**最初に使える正確な補題 II**)

これが本書で最も実用的な結果である。

**補題 NA-5.** $K\le H\le M$ をすべて isolated、$I_H=X$、$\rho:=R_{H,M}:\mathrm{ML}(H)\twoheadrightarrow X$、$J:=\mathrm{im}(R_{K,H})\le\mathrm{ML}(H)$ とする。
1. $g_1,\dots,g_r\in\mathrm{ML}(H)$ が**それぞれ個別に** $\mathrm{ML}(K)$ へ持ち上がり、$\langle\rho(g_1),\dots,\rho(g_r)\rangle\not\le A$ ならば $I_K=X$。
2. 特に、$\mathrm{ML}(H)$ のある Sylow 3-部分群 $S_3$ の**生成系**が個別に持ち上がれば $I_K=X$。このとき $\rho(S_3)=X^2$($X$ の唯一の Sylow 3-部分群)であり、$X^2\not\le A$ なので条件 1 は自動で満たされる。
3. **持ち上げる各 $g_i$ は outside roof を持つ必要がない**($\rho(g_i)\in A$ でもよい)。また Sylow 3-部分群は**都合のよいものを 1 つ選べばよい**(共役の別の Sylow を試す必要はない)。
*証明.*
1. $J$ は部分群(2008 Prop. 3.7)で各 $g_i\in J$。よって $\rho(J)\supseteq\langle\rho(g_i)\rangle\not\le A$。$I_K=\rho(J)$ なので $I_K\ne A$、T33-L2 より $I_K=X$。
2. 全射準同型は Sylow を Sylow に写すので $\rho(S_3)\in\mathrm{Syl}_3(X)$。T33-L4 より $X$ の Sylow 3-部分群は $X^2$ ただ一つ、$|X^2|=243$。Lagrange により $243\nmid324=|A|$ なので $X^2\not\le A$。生成系が $J$ に入れば $S_3\le J$。
3. 1 の証明は $\rho(g_i)$ 個々の外側性を使っていない。また 2 では $3\nmid[\mathrm{ML}(H):J]$ が「**ある**」Sylow 3-部分群が $J$ に入ることと同値(T33-T2 の証明)なので、選択は自由。∎

**なぜこれが効くか(実務上の意味).**
- 従来の標的は「$\rho(g)\in X^2\setminus A$ なる $g$(T33-L4 で 162 個の roof 標的)を持ち上げる」だった。
- NA-5 は標的を「**Sylow 3-部分群の生成系(典型的に 2〜3 元)を持ち上げる**」に置き換える。$\mathrm{ML}(H)$ が Mighty Dandy 型($\mathrm{Syl}_3\cong\mathbf Z_3\ltimes(\mathbf Z_9\times\mathbf Z_9)$、2008 §4.1)なら生成元は 2〜3 個。
- しかも **outside 判定が不要**になる。roof 写像の計算・162 標的の列挙・outside 行の同定がすべて落ちる。
- 各持ち上げは §3 の OBS-NA インスタンス 1 件。⟹ **$S^t$ 段の正の決着は「2〜3 個の literal 持ち上げ問題」に縮む。**

**「前段の特定 lift を保つ必要がない」ことの証明(Sol の要求項目).**
NA-5 の入力は $\mathrm{ML}(H)$ の Sylow 3-部分群の生成系だけであり、前段($H$ より粗い段)で構成した特定の lift を参照しない。各段でその段の $\mathrm{ML}(H)$ から**新たに**生成系を選んでよい。従って構成は段ごとに独立である。これは T-33 固定入力 3(seed の段間非互換を許す)と整合し、T-36 定理 T33-T1 の単調性・one-outside 論法が段間の互換性を一切要求しないことからも従う。∎

**限界(明記).** NA-5 は**十分条件**である。生成系の一つが持ち上がらなくても $I_K=A$ は従わない(その場合は §7 の OBS-NA を全 outside $g$ について走らせる必要がある)。

---

## 7. OBS-NA — 有限な必要十分 obstruction(**成果 2**)

### 7.1 定式化

**入力(すべて有限・literal)**

| 記号 | 中身 | 由来 |
|---|---|---|
| $\mathcal G_4=PB_4/K$, $\mathcal G_3=B_3/K_{PB_3}$, $\mathcal G_2=PB_2/K_{PB_2}$ | 有限群と $H$ 段への全射 | 窓の定義 |
| $N=H/K\cong S^t\trianglelefteq B_4/K$ | 非可換 chief factor | 前提 |
| $W=H_{PB_3}/K_{PB_3}$、埋め込み $\iota:W\hookrightarrow N^5$ | 補正領域 | (2.4) + NA-2 |
| $\bar\varphi_j:PB_3/K_{PB_3}\to\mathcal G_4$(五本) | literal A.18 coupling | (A.18) |
| $K_{\rm ord}/H_{\rm ord}$ と $\xi,\eta,\gamma\in W$ | $m$ 側補正 | Prop 2.3, (A.5) |
| $g$ ごとの $A_1,B_1,C_1,C_2\in\mathcal G_3$, $a_1..a_5\in\mathcal G_4$ | 共役子 | §3.1 |
| $\mathcal R(g)=(\rho_1,\rho_2,\rho_3)\in W\times W\times N$ | 残差 | §3.1 |
| $\Sigma$: friendly($2m'+1\in(\mathbf Z/K_{\rm ord})^\times$)・$T^{F_2}$ 全射・$f'$ の $[F_2,F_2]$ 代表可能性・settled | side gate | Def 2.9/2.19/3.2 |
| $\rho=R_{H,M}$ と $X^2\setminus A$(162 元) | comparison(選択用のみ) | T33-L4 |

**判定(必要十分).**
$$\mathrm{OBS\text{-}NA}(H,K)\ :\iff\ \forall g\in\mathrm{ML}(H)\ \text{with}\ \rho(g)\in X^2\setminus A,\ \ \forall\lambda\in\Lambda\ \text{with}\ \Sigma(\lambda):\quad \mathcal T(\lambda)\ \text{は}\ \mathcal R(g)\ \text{を}\ (1,1,1)\ \text{へ送らない}.$$
- **成立 ⟹ $I_K=A$ ⟹ B4-A**(B4-B は偽)。
- **不成立 ⟹ $I_K=X$**(当該段は閉じる)。
これは T33-L4 により**必要十分**である($I_K=X\iff I_K\cap(X^2\setminus A)\ne\varnothing$、および $I_K=\rho(J)$)。

### 7.2 探索器 / 独立 checker 契約

- **producer**: $g$ と $\lambda=(s,w)$ の候補を出す(NA-5 を使うなら $g$ は Sylow 3 生成系、$\rho$ 計算不要)。出力 = literal 対 $(m',f')$、および $\iota(w)\in N^5$ の 5 座標。
- **checker(helper 非共有)**: 独立に $\mathcal G_3,\mathcal G_4$ を構成し、(i) $(m',f')$ が (2.18)(2.19)(2.20) を $K$ 段で満たすことを**直接**語評価で検証(§3 の変換公式は使わない — producer と同じ道具を共有しない)、(ii) side gate $\Sigma$ を検証、(iii) NA-5 を使った場合は $\langle\rho(g_i)\rangle\not\le A$ ではなく「$g_i$ が Sylow 3 の生成系であること」だけを検証(位数計算)。
- **陰性側の完全性**: $\mathrm{OBS\text{-}NA}$ 成立を主張する場合は、$g$ と $\lambda$ の**登録宇宙が全体であること**の証明書を要求する(T-29 手戻り防止ルール 5 — 有限 slice の全滅を段の全滅と読み違えない)。
- **格**: 二系統一致は cross-checked。verified は Lean に予約。

### 7.3 規模

$|\Lambda|=(K_{\rm ord}/H_{\rm ord})\cdot|W|$、$|W|\le|S|^{5t}$。$S=PSL(2,8)$($|S|=504$)・$t=1$ なら $|W|\le504^5\approx3.3\times10^{13}$ — 全走査は不可。しかし §3 の公式は**座標分解を許す**:
1. $\rho_3$ の方程式は $\iota(w)$ の 5 座標の**捻れ積**(§3.2)なので、$\iota(W)$ が判れば $|N|$ 段階の絞り込みで解空間が定まる。
2. その解空間の上で $\rho_1,\rho_2$ を解く。
⟹ **実効コストは $\iota(W)\le N^5$ の構造次第**。これが D1 を最優先にする理由。

---

## 8. 禁止短路との照合(自己申告)

| 禁止短路 | 本書での扱い |
|---|---|
| centerless/Schreier だけからの自動 lift | **一度も使わない**。T33-L8/NA-4 により Wells 枠を離れている |
| $K(5)$ 単連結性だけから correction effectivity | **使わない**。NA-3 では syzygy を「残差集合を制限する装置」としてのみ使い、effectivity は主張しない |
| strict deletion-kernel | **使わない** |
| ambient exponent-3 quotient による非可換段の検出 | **使わない**。$S^t$ 段の判定は $N,W$ と literal coface のみで書かれている。T-36 T35-R2 で述べたとおり ambient $\mathbf F_3$ 商は非可換段の detector にならない |
| $A$ 正規性の仮定 | **使わない**。T33-L2/L4/T2 と NA-5 はすべて $A$ 非正規で成立(T-37 と整合) |
| PB4 固有の literal A.18 coupling を必ず使う(要求) | **使っている**: 五 coface $\bar\varphi_j$ が $\rho_3$ の補正に、literal 語 $A_1,B_1,C_1,C_2,a_i$ が全共役子に現れる。抽象 centerless 反模型は本定式化では作れない(そこには coface も共役子も無い) |

---

## 9. 効かないと判定したもの(理由つき)

1. **Wells / abstract kernel / compatible pair**: T33-L8(T-36)により GT 側の持ち上げ問題に $\mathrm{Aut}$ 持ち上げ段階が無い。A5/V4 反模型・T-35 反模型はいずれも $\mathrm{Aut}$-圏の対象で、§3 の残差方程式には転写されない。
2. **Gaschütz 型の生成元持ち上げ**: 既在裁定 `sol/luna_reply_152_b4_chief_absorption_v3.md:157-159`(Gaschütz/Frattini generation と Guralnick–Tiep は生成組か 1 本の関係式の話であって typed relation lifting を与えない)を**支持**する。本書でも使わない。なお $H/K$ が非可換 chief なら $\Phi$ の冪零性から $H/K\not\le\Phi(PB_4/K)$ なので、可換段で使えた「$V\subseteq\Phi\Rightarrow$ SURJ 自動」(in-house SURJ-W6・T-28(4))は**非可換段では使えない** — SURJ gate は真の追加条件である(D5)。
3. **T-35 の $\kappa+\Theta$**: NA-4 により本定式化では不要。$\kappa/\Theta$ は orbit/sign 経由の間接論法にのみ必要で、直接の残差計算には要らない。
4. **発案札 B-5(Burau specialization)**: 本定式化では comparison map が不要なので、B-5 は**この一撃には要らない**。$\mathrm{Out}(PSL(2,8))=C_3$ の実現が意味を持つのは、$\iota(W)$ や $N$ の $B_4$-作用を**具体的に同定する補助**としてであり、それは D1/D2 の計算手段の候補にとどまる。未査読 [BBB26] への荷重は**ゼロ**。
5. **$S^t$ の構造から $[\mathrm{ML}(H):J]$ の 3-part を決める**(司令塔の見立て): **できない**と判定する。$J$ は $N$ だけでなく $W=\iota^{-1}(\cdot)$、共役子、side gate に依存する。$J$ が部分群であること以外に $N$ から $J$ への一般的束縛は無く、$S=PSL(2,8)$ は $3\mid|S|$($3$-part $=9$)なので coprime 論法も効かない。**代わりに NA-5 が同じ目的(3-part を落とさない)をはるかに軽く達成する。**

---

## 10. 最小の欠品データ(D1–D6)

Sol の「最小の欠品データ」への回答。**これらが揃えば OBS-NA は機械判定可能になり、NA-5 と組めば正の決着も試せる。**

| 番号 | 欠品 | なぜ要るか | 取り方 |
|---|---|---|---|
| **D1** | $\iota(W)\le N^5$ の literal 決定(各射影 $\bar\varphi_j(W)\le N$ を含む) | §4・§7.3。可解性と規模を同時に決める最大の因子 | 五 coface を $H_{PB_3}$ に制限して $N$ への像を計算 |
| **D2** | 共役子 $A_1,B_1,C_1,C_2\in\mathcal G_3$ と $a_1..a_5\in\mathcal G_4$ の、$\mathrm{Aut}(W)$/$\mathrm{Aut}(N)$ への像 | §3 の三公式の全成分 | $H$ 段の literal 語から直接評価 |
| **D3** | 基点残差 $\mathcal R(g)=(\rho_1,\rho_2,\rho_3)$(NA-5 を使うなら Sylow 3 生成系の各元について) | 解くべき右辺 | 同上 |
| **D4** | $K_{\rm ord}/H_{\rm ord}$ と $\xi,\eta,\gamma$ の $W$ 内の像 | $m$ 側補正の自由度。friendly gate が $s\ne0$ を強制する場合がある | Prop 2.3 |
| **D5** | side gate の literal データ: $F_2/K_{F_2}$ の極大部分群(onto 判定)、$[F_2/K_{F_2},F_2/K_{F_2}]$(charming)、settled 判定 | 非可換段では SURJ は自動でない(§9-2) | 有限群計算 |
| **D6** | $m$ 補正込みの変換公式の完全な書き下し | §3.2 の帳簿作業(未実施) | 紙 1 頁 |

**加えて、$S^t$ 段の同定そのもの(旧 FC-4)**: 実系で最初に現れる非可換 $B_4$-chief factor が何か($S$、$t$、$B_4/H$ の置換作用)。発案札 B-2 は $PSL(2,8)$・$\mathrm{Out}=C_3$ と見立てている。これは D1–D5 の前提であり、**最優先**。

**そして NA-EX(§5)**: 「実際に現れる残差集合が吸収可能集合に含まれる」— これが一般に真なら成果 1(型付き十分定理)になる。**本書では証明も反証もできなかった(UNKNOWN)。** 可換段の対応物(157cz split exactness)からは従わない。

> **【文献要請】** 困難: 「非可換係数(有限単純群の直積)を持つ *cosimplicial* 語系において、arity-5 coherence(Stasheff $K(5)$)が課す syzygy が、arity-3 correction の像による吸収可能性を含意するか」。欲しい結果の型: (i) 非可換 $H^1$/crossed module の意味での「$K(5)$ 上の flat descent ⟹ $d_1$ の像の完全性」定理、または (ii) 有限単純群係数の nonabelian Čech/Ore 型の同時可解性定理($n$ 本の twisted 方程式の同時解の存在条件)。降りれば NA-EX の判定材料になる。(禁止短路①〜⑤に抵触しない形での要請であることを申告する — 求めているのは「$K(5)$ が単連結だから」ではなく「syzygy が課す制限が像に一致するか」の定理である。)

---

## 11. 使用した既在定理・novelty grep 領収書

**正典(2008.00066)**: Def 2.6((2.18)(2.19)(2.20))・Def 2.9・Prop 2.10・Def 2.19・(2.4)(2.5)・Prop 2.2・Prop 2.3・Def 3.2・Prop 3.3・Cor 3.5・Prop 3.6・Prop 3.7((3.7))・Prop 3.11((3.18))・Def 3.12/(3.24)・Thm 3.8・Cor 3.13・(A.3)(A.5)(A.18)・Thm A.1・Table 1/§4.1。

**in-house**:
- **T-36**(`docs/notes/t33_answer_draft_v1.md`): T33-L1/L2/L4/L8/L9、T33-T2(SYL3)、T33-L11、T35-R1/R2。本書はこれらを入力として使う。
- **T-37**: FC-1 閉鎖($A$ 非正規・coset 像 $S_3$・$|\mathrm{core}|=162$)。
- T-30 §2 / `sol/luna_reply_157cz_b345_power_syzygy.md`: $D_3=\sum(-1)^id^i$ と $PB_3^{ab}\to PB_4^{ab}\to PB_5^{ab}$ の split exactness。**NA-1 の可換化がこれと逐語一致することを検算に使った。**
- `sol/luna_reply_152_b4_chief_obstruction_v2.md` §4: 非可解 section と $S^t$ の存在(T-36 T33-L7 の土台)。§2: joint correction の反模型。
- `sol/luna_reply_152_b4_chief_absorption_v3.md:157-159`: Gaschütz/Guralnick–Tiep は typed relation lifting を与えない(**支持・本書でも使わない**)。
- `sol/luna_reply_152_b4_absorption_literature_v1.md` §1.1: Frattini cover / Gaschütz 型生成元持ち上げの文献整理。
- T-29 閉 3.1(torsor は空を非空にしない)・手戻り防止ルール 5(有限 slice の全滅 ≠ 段の全滅)。
- T-28(4) SURJ-W6($V\subseteq\Phi\Rightarrow$ SURJ 自動)— **非可換段では前件が破れることを §9-2 で明記**。
- 発案札 B-2/B-5(`docs/notes/t33_ideas_v1.md`): 採否を §9-4・§10 に記載。

**novelty grep(概念語彙・2026-08-18 実施)**

| 概念 | grep 結果 | 本書での扱い |
|---|---|---|
| 残差変換公式 $\rho_i(fw)=\cdots$(`R_1(m,f`, `[B,c]`, `twisted alternating`) | **repo 全体で該当なし** | **NA-1 は in-house 新規**。可換化が T-30 §2 と一致することは検算であって先行ではない |
| $W\hookrightarrow N^5$(五 coface による補正領域の埋め込み) | 近接物 `152_k9_relative_hunt_v3:14`(五 coface の kernel intersection)。**単射性と補正領域としての使用は該当なし** | NA-2 は新規(単射性の証明は (2.4) から 2 行) |
| Sylow-3 生成系の持ち上げで十分 | **該当なし**(`u6_prereg_readout_v1:24` は別文脈の Sylow-$\ell$ 共役作用) | **NA-5 は新規**。T33-T2(T-36)の系だが、「生成系で足りる/個々は outside 不要」は新しい帰結 |
| Gaschütz | 既在(`152_b4_absorption_literature_v1` §1.1, `152_b4_chief_absorption_v3:157`) | **引用して支持・使用しない** |
| 非可換段で SURJ が自動でない($\Phi$ 冪零) | 近接物 `152_minbad_frattini_v1`, `152_b3_frattini_terminal`(可換段の Frattini) | §9-2 の明示は新規だが、初出主張はしない(古典的事実の適用) |
| PSL(2,8)・$\mathrm{Out}=C_3$ | 既在(札 B-2、`157da:70`) | 引用 |

---

## 12. 申告

- 本書の全結果は **paper candidate**。機械計算・GAP・GHA・commit・push はゼロ。**cross-checked ではなく verified でもない。**
- 未証明で残した点を明示する:
  - **【UNKNOWN】NA-EX**(実際の残差集合が吸収可能集合に含まれるか)= 成果 1 の中身。証明も反証もできなかった。
  - **【GAP: D6】** $m$ 補正込みの変換公式の書き下し(定型・未実施)。
  - **【GAP: D1】** $\iota(W)\le N^5$ 未知。§7.3 の規模評価はこれ次第。
  - **【GAP: SURJ-NA】** 非可換段の onto gate の持ち上げ条件(可換段の SURJ-W6 が使えない)。
  - **【UNKNOWN】** 実系の最初の非可換 chief factor の同定(旧 FC-4)。
- **B4-B は宣言していない。** 本書は Sol の主問題への「最初に使える正確な補題(NA-1, NA-5)+ 有限な必要十分 obstruction(OBS-NA)+ 最小欠品データ(D1–D6)」の提出のみである。
- Sol が再議論を禁じた領域(elementary-F3 段・算術 membership・指数 3 群論)には立ち入っていない。T-37 の裁定は固定入力として使用し、再監査していない。
