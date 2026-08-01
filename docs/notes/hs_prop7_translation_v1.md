# HS Prop 7 の有限商翻訳 — 層 (b) の cross-frame 検出器の設計ノート(v1)

- 起草: 影工房 数学者(Claude / Opus 5)・2026-08-02
- 委嘱: 司令塔 **札 C 起動・裁定 419**(文献ゲート配達 HS-1)
- 入力: `docs/scout/覚書_hs1_prop7_20260802.md`(司令塔覚書・翻訳指針 5 点)/ `papers/harbater-schneps-2000-fund-groups-moduli-GT.pdf`(現物)
- 正典: `docs/week1-定義ノート.md`(§2 groupoid GTSh・規約 W-1〜W-4)/ arXiv 2401.06870 / 2405.11725
- 既存資産: `docs/notes/c2q_finite_def_v1.md`(+ 追記 A)/ `docs/notes/gtpi_v1.md`(+ 追記 A)/ `docs/notes/k5_genuine_campaign_v1.md` §3.6 / `docs/notes/ihnec_v1.md` / `docs/notes/fake_void_v1.md` / `docs/week3-比較写像_guillot_v2.md`(**定理 G3** — 本稿の最重要の対照)
- **本稿は設計ノート。実装は含まない。** 値はすべて機械生成(手写しなし)。**commit しない。**
- **読んだ範囲の申告(HS 2000)**: §0.1(条件 (I)(II)(III) の定義・Main Theorem)・§1.1(K(0,n) の構造・p_i・S̃_n)・§1.3(Prop 3 / Prop 4 とその証明・Thm 2)・§2.2(**Lemma 1** とその証明・q_i・(10))・§2.3 冒頭〜(Prop 5・Prop 6・j の定義・M(0,5))・**§2.3 の Prop 7 とその証明・直後の Remark・Theorem 4**。それ以外(§3・Appendix)は未読。

---

## 0. 判定(先に 8 行)

| # | 問い | 判定 | 格 |
|---|---|---|---|
| **①** | HS Prop 7 の機構は何か | **(I)(II)(III) は「位数 2・3・5 の自己同型に対するノルム条件」の同一族**。Prop 3/4/7 + Lemma 1 がこれを与える(§1.1) | **紙上証明**(HS の原文 + 3 行) |
| **②** | (III) の有限版はどう書くか | $\boxed{N_{\bar\rho}(\bar f):=\bar\rho^4(\bar f)\bar\rho^3(\bar f)\bar\rho^2(\bar f)\bar\rho(\bar f)\,\bar f=1}$ — **量化子なしの等式**。HS の「lift の存在」形は使わない(§1.2) | **紙上証明**(定理 PENT-NORM・(III) と厳密同値) |
| **③** | 深さ 2 の検出力 | **厳密ゼロ**。pentagon の深さ 2 主要項 $P$ は $\mathrm{gr}_2(K(0,5))$ で**恒等的に消える**(整数係数証明書つき)。⟹ **C2-Q の R3 の cross-frame 側からの独立証明**(§2.1) | **定理 + 独立検算 2 実装** |
| **④** | 深さ 3 の検出力 | **厳密ゼロ**。$\ker\nu_3=\{a=b\}$ が**hexagon (3.10) の解集合とちょうど一致**(§2.2) | **定理 + 検算** |
| **⑤** | 深さ 4 の検出力 | ★ **1 次元・非ゼロ**。hexagon の深さ 4 解空間は 1 次元 $\mathbb Q\mathfrak h_4$、$\nu_4$ はそこに単射 ⟹ **pentagon は hexagon にない情報を厳密に 1 次元もつ**(§2.3) | **定理 + 検算 2 素数** |
| **⑥** | dummy は特定できたか | ★ **できた**。$\mathfrak h_4=[[[x,y],x],x]+4[[[x,y],x],y]+[[[x,y],y],y]$ — **hexagon を満たし pentagon を破る明示元**(§2.3) | **定理 + 検算** |
| **⑦** | 委嘱指定の第一標的 $K_\pi$ は適切か | ★ **不適**。$\bar\rho$ は位数 5 ゆえノルムは**標数 5 で退化**し、$K_\pi$ 系は 5-torsion 漬け($N_{\rm ord}=5$・$C_5^3$)。実測 20/20 PASS の構造的説明でもある(§3.1) | **計算(p=5 で $\nu_4(\mathfrak h_4)=0$)+ 状況証拠** |
| **⑧** | 壁窓(n=24/28/36/37)へ移送できるか | ★ **裁定 386 の再開トリガーは充足しない**。壁窓は $d(N)=1$(A_n 完全)ゆえ命題 HSP-COLLAPSE の射程・非冪零 $Q$ では**検出力の事前見積りが原理的に立たない** = DUM-G3 規律に反する(§4) | **命題 + 正直な UNKNOWN** |

> **一行で**: **HS Prop 7 の有限版は書ける・恒真ではない・検出力は深さ 4 に厳密に 1 次元。ただしその 1 次元が見える窓は「$d(N)\ge2$ かつ類 $\ge4$ の冪零窓」に限られ、dihedral 予想の open 標的族(奇・混合)と壁窓は命題 HSP-COLLAPSE で構造的に外れる。**

> **司令塔向けの実務結論**: 起票してよい。ただし **標的を委嘱の $K_\pi$ から「類 4 冪零窓 $p\ge7$」へ差し替える**判断を求める(§3.2・速達で先行照会済)。

---

## 1. 機構の有限版の定式化

### 1.0 記号

$K(0,n)=\pi_1(\mathcal M_{0,n})$、生成元 $x_{ij}$。**HS §1.1**: $K(0,4)=F_2$($x=x_{12},y=x_{23}$)、
$$1\to F_{n-2}\to K(0,n)\xrightarrow{\ p_i\ }K(0,n-1)\to1\quad(\text{分裂}),$$
$K(0,5)\cong F_3\rtimes F_2$。$K(0,5)$ は **5 個の元 $x_{i,i+1}$($i\bmod5$)で生成される**(HS §2.3 Lemma 4 の証明)。$j:K(0,4)\hookrightarrow K(0,5)$, $x\mapsto x_{12},\ y\mapsto x_{23}$(HS §2.3)。

$$\rho\in\mathrm{Aut}(K(0,5)),\qquad \rho(x_{i,j})=x_{i+3,j+3}\ (\text{添字}\bmod5)$$
は置換 $(1\,4\,2\,5\,3)\in S_5$ の上のリフト(HS §2.3 冒頭)。生成元上 $\rho^5=\mathrm{id}$ ゆえ **$\rho$ の位数はちょうど 5**。

### 1.1 定理 NORM — HS の三条件は「有限位数自己同型のノルム」の同一族である

> **定理 NORM**(HS Prop 3 / Prop 4 / Prop 7 + §2.2 Lemma 1 の読み替え)。
> $\sigma\in\widetilde S_n\subseteq\mathrm{Aut}(K(0,n))$ を位数 $d$ の元、$F$ を $[\sigma,F]=\mathrm{inn}(h)$ を満たす自己同型とすると **Lemma 1**:
> $$\sigma^{d-1}(h)\cdot\sigma^{d-2}(h)\cdots\sigma(h)\cdot h=1 .$$
> HS の三条件はこの「$\langle\sigma\rangle$-ノルムの消滅」の $d=2,3,5$ の場合である:
>
> | 条件 | 自己同型 | 位数 | ノルム形 | 工房の対応物 |
> |---|---|---|---|---|
> | **(I)** | $\omega:x\leftrightarrow y$(= 工房の $\theta$) | 2 | $\theta(f)\cdot f=1$ | **(3.10)** $f\theta(f)\in N_{F_2}$ |
> | **(II)** | $\varphi:x\mapsto y\mapsto z\mapsto x$(= 工房の $\tau$) | 3 | $\tau^2(g)\tau(g)g=1$, $g=y^mf$ | **(3.11)** $\tau^2(y^mf)\tau(y^mf)y^mf\in N_{F_2}$ |
> | **(III)** | $\rho$(**$K(0,5)$ 上**) | 5 | $\rho^4(f)\cdots\rho(f)f=1$ | **本稿の新設** |

**この表が本稿の骨格である。** (I)(II) は $F_2=K(0,4)$ の自己同型のノルム、(III) は**より大きい群 $K(0,5)$ の自己同型のノルム**。gentle 枠は $K(0,4)$ しか持たない — **これが「cross-frame でなければ書けない」ことの正確な理由**である(C2-Q 追記 A の P99-C2-BLIND が「gentle 公理から全称的に出る不変量では不可能」と言ったことの、こちら側からの説明)。

**証明.** Lemma 1 は HS §2.2 の 2 行(帰納法 $\sigma^iF\sigma^{-i}=\sigma^{i-1}(h)\cdots h\,F$ に $i=d$)。(I)(II) の同値は HS Prop 3 (i)⟺(iii)・Prop 4 (i)⟺(iii)、(III) は次項。∎

### 1.2 定理 PENT-NORM — (III) は $\rho$-ノルムそのもの(量化子なし)

HS の (III)(原文 §0.1)は $K(0,5)$ の中の
$$f(x_{12},x_{23})\,f(x_{34},x_{45})\,f(x_{51},x_{12})\,f(x_{23},x_{34})\,f(x_{45},x_{51})=1 .$$

$\rho(x_{12})=x_{45},\ \rho(x_{23})=x_{51}$ より
$$\rho(f)=f(x_{45},x_{51}),\quad\rho^2(f)=f(x_{23},x_{34}),\quad\rho^3(f)=f(x_{51},x_{12}),\quad\rho^4(f)=f(x_{34},x_{45}).$$

> **定理 PENT-NORM.** $f\in F_2\subseteq K(0,5)$($j$ で埋め込む)に対し
> $$\textbf{(III)}\iff N_\rho(f):=\rho^4(f)\rho^3(f)\rho^2(f)\rho(f)\,f=1 .$$

**証明.** $W_1:=f(x_{12},x_{23})$、$A:=f(x_{34},x_{45})f(x_{51},x_{12})f(x_{23},x_{34})f(x_{45},x_{51})$ と置くと (III) は $W_1A=1$、$N_\rho(f)=AW_1$。$W_1A=1\iff A=W_1^{-1}\iff AW_1=1$。∎

> **★ 設計上の意味(3 点)**
> 1. **量化子がない。** HS Prop 7 の (ii)(iii) は「$\rho$ と可換な lift $\tilde F$ **が存在する**」という存在命題で、有限版にすると「どの lift か」「well-defined か」という委嘱 §1 の危険がそのまま入る。**ノルム形はこれを完全に回避する** — 語を 5 通りの生成元対で評価して掛けるだけ。
> 2. **HS Prop 7 の付加価値は「検出」ではなく「構成」**である。ノルム形が通ったとき、Prop 7 (iii) は **$[\rho,\tilde F]=\mathrm{inn}\,f$ を満たす $\tilde F\in\mathcal A_5$ を明示的に与える**(証明中の $\tilde F(x_{i,i+1})$ の 5 個の式)。検出器としては (III) 直接、構造(Out♯₅ 側の対象を作る)としては Prop 7 — **役割を分ける**。
> 3. **$\rho$-同変性(=$\langle\rho\rangle$ の 1-コサイクル条件)が見えるようになる**。これが §2 の深さ解析を可能にした唯一の道具である。**これが「手法の移送」の実体**であって、pentagon の語を書き下すこと自体は 2008.00066 (2.20) で既に可能だった(`docs/notes/litgate_pentagon_v1.md` §2.1)。

### 1.3 有限版の定義(窓・well-definedness・量化)

> ### 定義 HSP-W(**許容窓**)
> $W\trianglelefteq K(0,5)$ が**許容窓**であるとは:
> - **(W-a)** $[K(0,5):W]<\infty$;
> - **(W-b)** $\rho(W)=W$(⟹ $\bar\rho\in\mathrm{Aut}(Q)$、$Q:=K(0,5)/W$、$\mathrm{ord}(\bar\rho)\mid5$);
> - **(W-c)** **(WD)** $j(N_{F_2})\subseteq W$。

> ### 定義 HSP-T(**有限 pentagon 検査**)
> 窓 $N\in\mathrm{NFI}_{PB_3}(B_3)$ の GT-shadow $[m,\bar f]$($\bar f\in F_2/N_{F_2}$)と許容窓 $W$ に対し
> $$\mathrm{PENT}_W([m,\bar f])\ :\iff\ \bar\rho^4(\bar f)\bar\rho^3(\bar f)\bar\rho^2(\bar f)\bar\rho(\bar f)\,\bar f=1\ \text{ in }Q,$$
> ただし $\bar f:=j(f)W\in Q$($f$ は任意の代表)。

> ### 補題 HSP-WD(**well-defined 性**)
> (W-b)+(W-c) の下で $\mathrm{PENT}_W$ は代表 $f$ の取り方に依らない。
> **証明.** $n\in N_{F_2}$ に対し $j(fn)=j(f)j(n)$ で $j(n)\in W$。また $\rho^i(j(n))\in\rho^i(W)=W$((W-b))。ゆえに $\rho^i(j(fn))W=\rho^i(j(f))W$ が全 $i$ で成立し、5 項の積も不変。∎
> **注**: $m$ は使わない。$\mathrm{PENT}_W$ は **$\bar f$ のみの関数**である(hexagon と違い $m$ 依存性を持たない — §2.3 で $m$ は $c_2$ 経由で間接的に入る)。

> ### 命題 HSP-SOUND(**片側健全性** — これが検査の論理的性格)
> $\mathrm{PENT}_W([m,\bar f])$ が**偽**なら、$[m,\bar f]$ を持ち上げる $(\lambda,\hat f)\in\widehat{GT}$ は存在しない(= **pentagon-fake の有限証明書**)。**真の場合は何も結論しない**(有限深度)。
> **証明.** $(\lambda,\hat f)\in\widehat{GT}$ なら (III) が $\widehat{K(0,5)}$ で成立、$W$ への射影で $Q$ でも成立、$\hat f\mapsto\bar f$。対偶。∎

### 1.4 (I)(II) 前件の有限版 = 工房の hexagon + charming(逐語辞書)

**HS §0.1 の (I)(II) は、工房の gentle 系の条件そのものである**(定義ノート §2 末: 「$\widehat{GT}_{gen}$ = Harbater–Schneps の $\widehat{GT}_0$」、HS Thm 2: $\mathrm{Out}^\sharp_4\cong\widehat{GT}_0$)。

| HS | 工房(定義ノート §2) | 注 |
|---|---|---|
| $\lambda\in\widehat{\mathbb Z}$ | $u=2m+1$ | $m=(\lambda-1)/2$ |
| (I) $f(y,x)f(x,y)=1$ | **(3.10)** $f\theta(f)\in N_{F_2}$ | HS の $\omega$ = 工房の $\theta$ |
| (II) $f(z,x)z^mf(y,z)y^mf(x,y)x^m=1$ | **(3.11)** $\tau^2(y^mf)\tau(y^mf)y^mf\in N_{F_2}$ | 巡回回転で同値(§1.1 表) |
| $f\in\widehat{F_2}'$ | **charming** $\bar f\in[F_2/N_{F_2},F_2/N_{F_2}]$ | 有限版 |
| $F$ が $F_2$ の自己同型 | **全射性**(Def 3.7・Prop 3.6) | 有限版 |
| (III) | **本稿 $\mathrm{PENT}_W$** | 新設 |

> ⚠ **区別すべき一点(委嘱 §5 の水準混同の核心)**: **元の水準では辞書は完全一致**(上表)。**同名別物なのは窓の圏**であって条件式ではない — HS は $\mathrm{Out}^\sharp_n$($\mathcal M_{0,4}/\mathcal M_{0,5}$ の副有限 $\pi_1$ 全体)で、工房は $\mathrm{NFI}_{PB_3}(B_3)$ の有限窓。**本稿がやっているのは「HS の元の条件を工房の窓に載せる」ことであって、HS の定理($\mathrm{Out}^\sharp_5\cong\widehat{GT}$)を移送することではない。** 覚書 §12-3 の警告はこの形で精密化される。

### 1.5 補題 CENT-FREE — $K(0,5)$ 窓は $PB_4$ 窓の代用になる(【GAP-GTPI-2】/【文献要請 U-PB4】への部分回答)

$K(0,5)\cong PB_4/Z(PB_4)$(HS §1.1 の $K(0,n)\cong F_{n-2}\rtimes K(0,n-1)$ と $PB_4\cong F_3\rtimes PB_3$、$PB_3\cong F_2\times\langle c\rangle$ から)。

> **補題 CENT-FREE.** $f\in[PB_4,PB_4]$(charming なら成立)に対し、
> **$PB_4$ 水準の pentagon(2008.00066 (2.20))$\iff$ $K(0,5)=PB_4/Z(PB_4)$ 水準の pentagon(HS (III))。**
> **証明.** $\Rightarrow$ は商への射影。$\Leftarrow$: 二つの条件の差は $Z(PB_4)$ の元。pentagon の defect は 5 個の余面像 $\partial_\bullet(f)$ の積で、各 $\partial_\bullet$ は準同型ゆえ defect $\in[PB_4,PB_4]$。一方 $Z(PB_4)=\langle\text{full twist}\rangle\cong\widehat{\mathbb Z}$ は abelian 化 $PB_4^{ab}\cong\widehat{\mathbb Z}^6$ に**単射**に写る(full twist $=\prod_{i<j}x_{ij}$)ゆえ $Z(PB_4)\cap[PB_4,PB_4]=1$。∎

> **★ 含意**: 【GAP-GTPI-2】(「現行構成に $PB_4$ 水準の窓が存在しない」)と【文献要請 U-PB4】は、**pentagon の判定に関しては迂回できる** — $B_4$ の窓 $\tilde K\trianglelefteq B_4$ を構成しなくても、**$K(0,5)$ の $\rho$-安定窓**があれば $PB_4$ 水準の pentagon が判定できる。$K(0,5)$ は **5 生成・明示的 $\mathbb Z/5$ 対称つき**で、$PB_4$(6 生成・余面 5 本の簿記)より扱いやすい。
> ただし **これは pentagon 判定に限る** — 2008.00066 の GT-shadow の圏($\mathrm{NFI}_{PB_4}(B_4)$)そのものを代用するものではない(settled/isolated/reduction は別の話)。**U-PB4 の (α)(β)(γ) は依然 open。**

---

## 2. 検出力の事前見積り(**最重要** — C2-Q の轍を踏まない)

**方針**: 委嘱と K5 戦役 §3.6 F-4 の規律に従い、**走らせる前に紙(+ 独立検算)で見積る**。道具は $K(0,5)$ の下中心列(LCS)に沿う次数分解。

**枠組み**: $\mathfrak t:=\mathrm{gr}(K(0,5))\otimes\mathbb Q$(Drinfeld–Kohno 型の二次代数)。$V:=\mathfrak t_1$、基底 $T_i:=t_{i,i+1}$($i=1..5$)。$\rho$ は $V$ 上 $T_1\to T_4\to T_2\to T_5\to T_3\to T_1$(**5-巡回**)。
$f=\exp(F)$、$F=F_2+F_3+F_4+\cdots$($F_k\in\mathrm{Lie}_k$)。BCH より
$$\log N_\rho(f)=\underbrace{\textstyle\sum_i\rho^i(F)}_{\nu(F)}+\tfrac12\!\!\sum_{k<l}[(L_k)_2,(L_l)_2]+(\deg\ge5),\qquad L=(\rho^4f,\rho^3f,\rho^2f,\rho f,f).$$
次数別に:
$$\Omega_2=c_2\!\cdot\!P,\qquad \Omega_3=\nu_3(F_3),\qquad \Omega_4=\nu_4(F_4)+c_2^2\,\Theta,$$
$$P:=\textstyle\sum_i\rho^i([T_1,T_2])=[T_1,T_2]+[T_2,T_3]+[T_3,T_4]+[T_4,T_5]+[T_5,T_1],\qquad
\Theta:=\tfrac12\!\!\sum_{i>j}[\rho^iw,\rho^jw],\ w=[T_1,T_2].$$

### 2.1 ★ 定理 D2-BLIND(深さ 2 の検出力は**厳密ゼロ**)

> **定理 D2-BLIND.** $P=0$ in $\mathrm{gr}_2(K(0,5))$。ゆえに任意の charming $f$ に対し $N_\rho(f)\in\gamma_3(K(0,5))$ で、**pentagon の深さ 2 の情報量は恒等的にゼロ**である。

**証明(整数係数の明示証明書)**: 独立検算(§6)が
$$P=-3\,[t_{12},t_{34}]-2\,[t_{12},t_{35}]-[t_{13},t_{24}]-2\,[t_{13},t_{25}]+[t_{14},t_{23}]$$
を出力した — 右辺はすべて **添字が交わらない対の交換子 = $\mathfrak t$ の関係式 (R1)**、係数はすべて**整数**。ゆえに $P$ は $\Lambda^2(\mathbb Z^5)\to\mathrm{gr}_2$ の核に**整数的に**属する。∎

**構造検算**(同 script、独立に一致): $\dim V=5$・$\dim\mathrm{Lie}_2(V)=10$・関係式空間 6 次元・$\dim\mathfrak t_2=4$。**$4=\mathrm{Witt}(3,2)+\mathrm{Witt}(2,2)=3+1$** で $K(0,5)\cong F_3\rtimes F_2$ の予測と一致。対照: $[T_1,T_2]$ 単独は関係式空間に**入らない**(= $c_2$ 自身は死んでいない)。

> ### ★★ 系 D2-C2(**C2-Q の R3 の、cross-frame 側からの独立証明**)
> `c2q_finite_def_v1.md` R3 は「$c_2$ は pentagon の独立 detector ではない」を **gentle 公理側**(定理 C2-FIN)から示した。定理 D2-BLIND は**同じ結論を pentagon 側から**示す: **pentagon が深さ 2 に持っている情報そのものがゼロ**だから、どんな深さ 2 不変量($c_2$ を含む)も pentagon を検出できない。
> **二つは独立**である(前者は hexagon の帰結、後者は $K(0,5)$ の構造)。**追記 A の限定命題 P99-C2-BLIND が「factorization theorem が別途必要」と留保した部分を、この方向については埋める。**
>
> ⚠ **精確化(過剰主張の防止)**: 「$c_2$ が pentagon と無関係」ではない。**pentagon は $c_2$ に何の条件も課さない**(深さ 2 の成分が空虚だから)が、**逆に $c_2$ は深さ 4 の pentagon 条件に $c_2^2\Theta$ という形で入る**(定理 D4-POWER (d))。すなわち $c_2$ は **detector ではないが parameter ではある**。この 2 つを混同しない。

### 2.2 ★ 定理 D3-BLIND(深さ 3 の検出力も**厳密ゼロ** — hexagon が丸ごと食う)

$\mathrm{gr}_3(F_2)\cong\mathbb Z^2$、基底 $u_1=[[x,y],x]$、$u_2=[[x,y],y]$。$F_3=a\,u_1+b\,u_2$。

> **定理 D3-BLIND.**
> **(a)** $\ker\bigl(\nu_3|_{\mathrm{gr}_3(F_2)}\bigr)=\mathbb Q\,(u_1+u_2)$($\nu_3$ の像は 1 次元)。
> **(b)** hexagon (3.10) は深さ 3 で **$a=b$** と同値。
> **(c)** ゆえに **hexagon を満たす $f$ は自動的に $\Omega_3=0$**。深さ 3 の検出力はゼロ。

**証明.** (a) 検算(§6・2 実装 + 2 素数)。(b) $\theta(u_1)=[[y,x],y]=-u_2$、$\theta(u_2)=-u_1$、$F_3+\theta F_3=(a-b)(u_1-u_2)$、$\mathrm{gr}_3(F_2)$ は $u_1,u_2$ を基底とする自由加群ゆえ $=0\iff a=b$。((3.10) の深さ 3 は $F_3+\theta F_3=0$ — 深さ 2 の $\theta F_2=-F_2$ より $[F_2,\theta F_2]=0$ で BCH 補正が消えるため。)(c) (a)+(b)。∎

> **注(教材)**: (b) の $u_1+u_2$ は古典の $\mathfrak h_3$ に対応する方向である。**hexagon が許す唯一の深さ 3 方向を、pentagon がちょうど許す** — 偶然ではなく、両者が同じ $\mathfrak h_3$ を含むことの現れ。**検算でも $\mathfrak h_3$ は全標数で pentagon を通る**(§6)。

### 2.3 ★★ 定理 D4-POWER(深さ 4 の検出力は**厳密に 1 次元** — dummy の明示)

$\mathrm{gr}_4(F_2)\cong\mathbb Z^3$、基底 $v_1=[[[x,y],x],x]$、$v_2=[[[x,y],x],y]$、$v_3=[[[x,y],y],y]$(Hall 関係 $[[[x,y],y],x]=v_2$ を検算で確認)。

> **定理 D4-POWER.**
> **(a)** hexagon((3.10)+(3.11))の深さ 4 の**斉次解空間**は **1 次元**で、生成元は
> $$\boxed{\ \mathfrak h_4\ :=\ v_1+4v_2+v_3\ =\ [[[x,y],x],x]+4[[[x,y],x],y]+[[[x,y],y],y]\ }$$
> (この空間は $m$ に依らない — $F_4$ に効く線型作用素は $1+\theta$ と $1+\tau_0+\tau_0^2$ で、$y^m$ 共役は深さ 5 以上にしか効かない)。
> **(b)** $\nu_4|_{\mathrm{gr}_4(F_2)}$ は **単射**(3 次元の像)。とくに $\nu_4(\mathfrak h_4)\ne0$。
> **(c)** ゆえに **$\mathfrak h_4$ は hexagon を満たし pentagon を破る** ⟹ **★ 検出力は厳密に 1 次元、dummy は明示的に存在する。**
> **(d)** $\Theta\ne0$ in $\mathfrak t_4$。すなわち深さ 4 の障害は $c_2^2$ を通じて **$m$ に依存する**: $\Omega_4=\nu_4(F_4)+c_2^2\Theta$、$c_2=m(m+1)/6$(C2-FIN)。

**証明.** (a) 独立実装の厳密有理計算(§6・`hs_prop7_hexagon_vs_pentagon.py`): 深さ 2 で $c_2=0$ が強制($\lambda=1$)、深さ 3 で $\{a=b\}$(1 次元・$\mathfrak h_3$)、深さ 4 で $\{(\alpha,\beta,\gamma)=t(1,4,1)\}$。手計算とも一致 — (3.10) が $\alpha=\gamma$、(3.11) が $(4\alpha-\beta)(v_1+v_2+v_3)=0$($1+\tau_0+\tau_0^2$ の像は $\mathbb Q(v_1+v_2+v_3)$ で階数 1)。
(b)(d) 検算(§6・2 素数一致 + 小素数走査)。$\dim\mathfrak t_4=21=\mathrm{Witt}(3,4)+\mathrm{Witt}(2,4)=18+3$ で構造予測と一致。∎

> ### ★ 系 D4-DUM(**DUM-G3 規律の充足** — 委嘱 §2 への直接回答)
> **dummy fixture**: $f_{\rm dum}:=\exp(t\,\mathfrak h_4)$($t\ne0$)。
> - **hexagon**: 深さ $\le4$ で PASS(定理 D4-POWER (a))。
> - **charming**: $\mathfrak h_4\in\gamma_4(F_2)\subseteq[F_2,F_2]$ ゆえ PASS。
> - **pentagon**: **FAIL**($\nu_4(\mathfrak h_4)\ne0$)。
> ⟹ **「全 GT-shadow が自動的に通る恒真検査」ではないことが、実装前に確定した。** これが C2-Q との決定的な差である。

> ### ★ 系 D4-PRED(検出比の予言)
> 窓 $Q$ の深さ 4 層が $\mathbb Z/p$ 型なら、hexagon を満たす候補は $\mathfrak h_4$-座標について $p$ 通り、pentagon を通るのは**ちょうど 1 通り** ⟹ **検出比 $(p-1)/p$**。

### 2.4 ★ 悪い標数 = **$p=5$**(ノルムの退化)

$\nu=\sum_{i=0}^4\rho^i$ は $\mathrm{ord}(\rho)=5$ のノルム写像であり、標数 5 では $\nu=(\rho-1)^4$ に退化する。検算(§6・`hs_prop7_dummy_and_primes.py`):

| $p$ | 2 | 3 | 5 | 7 | 11 | 13 | $10^9{+}7$ |
|---|---|---|---|---|---|---|---|
| $\nu_4(\mathfrak h_4)=0$?(= **検出器の死**) | 否 | 否 | ★ **是** | 否 | 否 | 否 | 否 |
| $\mathfrak h_3$ が pentagon を通るか | 通る | 通る | 通る | 通る | 通る | 通る | 通る |
| $\Theta=0$? | 否 | 否 | 否 | 否 | 否 | 否 | 否 |

> **⟹ 篩条件: 窓の関与する標数から 5 を排除せよ。**

### 2.5 ★ 命題 HSP-COLLAPSE(**$d(N)=1$ の窓は冪零窓越しに完全に盲目**)

C2-Q の $d(N):=\lvert\gamma_2(P)/\gamma_3(P)\rvert$($P=F_2/N_{F_2}$)をそのまま使う。

> **命題 HSP-COLLAPSE.** $d(N)=1$(すなわち $\gamma_2(P)=\gamma_3(P)$)で、$W$ が許容窓かつ **$Q=K(0,5)/W$ が冪零**なら、**すべての charming $\bar f$ について $Q$ での像は $1$**。ゆえに $\mathrm{PENT}_W$ は恒真 — **検出力は厳密にゼロ**。
> **証明.** (W-c) より $j(F_2)$ の $Q$ での像 $\bar P$ は $P$ の商。$\gamma_2(P)=\gamma_3(P)$ は商に遺伝するので $\gamma_2(\bar P)=\gamma_k(\bar P)$ が全 $k\ge2$ で成立。charming より $\bar f\in\gamma_2(\bar P)=\gamma_k(\bar P)\subseteq\gamma_k(Q)$(部分群の LCS は全体の LCS に含まれる)が全 $k$ で成立 ⟹ $\bar f\in\gamma_\infty(Q)=1$($Q$ 冪零)。∎

> ### ★★ 系 HSP-ODD(**dihedral 予想の open 標的族は構造的に外れる**)
> **命題 D-ODD**(`c2q_finite_def_v1.md` R6: $4\nmid n\Rightarrow d(K^{(n)})=1$)と合わせて:
> **奇・混合 dihedral 窓 $K^{(n)}$($4\nmid n$)では、冪零 $K(0,5)$-窓を通した pentagon 検査の検出力はゼロ。**
> ⟹ $c_2$ が盲目だった族と**同じ族**で pentagon 検査も(この経路では)盲目。**これは偶然ではなく、両者が同じ量 $d(N)$ に律速されている。**

> ### 系 HSP-WALL(壁窓)
> 壁 4 窓は $P\cong A_n$(完全)ゆえ $\gamma_2(P)=\gamma_3(P)=P$、$d(N)=1$。⟹ 冪零 $Q$ を通す限り検出力ゼロ。**非冪零 $Q$ については本解析は沈黙**(§4)。

### 2.6 ★ 篩 HSP-F(**発注前に通す 6 段** — K5 戦役 §3.6 の型)

| 段 | 検査 | 落ちる例 |
|---|---|---|
| **F-1** | $d(N)\ge2$(C2-Q §5 の $d$ センサスをそのまま流用) | **全奇・混合 dihedral 窓**($d=1$)・**壁 4 窓**($d=1$)・$K_\pi$/$N_A$($P=A_5$ 完全ゆえ $d=1$) |
| **F-2** | 窓の関与標数に **$5$ を含まない** | $K_\pi$($N_{\rm ord}=5$・$C_5^3$)・$K^{(5)}$・$K^{(25)}$ |
| **F-3** | $F_2/N_{F_2}$ の**冪零類 $\ge4$**、かつ $\mathfrak h_4$ の像が $\gamma_4/\gamma_5$ で非ゼロ | 類 $\le3$ の窓すべて(深さ 2,3 は定理 D2/D3-BLIND で盲目) |
| **F-4** | $N_{F_2}\cap\gamma_4(F_2)$ が $\mathfrak h_4$ 方向を**含まない**(でないと $\bar f$ が検出座標を持てない) | 窓が浅すぎる場合 |
| **F-5** | 許容窓 $W$ が実際に構成でき、$[K(0,5):W]$ が 8GB 内 | §3.2 で見積り |
| **F-6** ★ | **dummy $f_{\rm dum}=\exp(t\mathfrak h_4)$ をその窓で走らせ、実際に FAIL することを本走前に確認**(系 D4-DUM の実効化) | 上記のいずれかを見落とした窓 |

> **F-1〜F-4 は紙で判定できる**(実装ゼロ)。**F-1 で落ちる窓は起票しない。**

### 2.7 ★★ 危険な対照 — 定理 G3(hexagon 側の可換性検査は**自動**)

`docs/week3-比較写像_guillot_v2.md` §3.3 **定理 G3**: 許容対象($c\in N$)の settled shadow について、$\alpha_{m,f}$ は $\mathrm{Out}(P)$ 内で $\theta$ とも $d_G$ とも**自動的に可換**。証明は「$T_{m,f}$ が $B_3$ の準同型で $S_3$ 上恒等」の一行。

> **⟹ HS Prop 3/4 型(hexagon 側・$\theta$/$\omega$ との可換性)を有限窓に載せても検出力はゼロである。** これは既に工房で証明済みの事実であり、**「可換性検査」という形だけを真似ると必ず C2-Q の轍を踏む。**

> **★ ではなぜ pentagon 側は自動でないのか(本稿の答)**:
> G3 の証明は「**$B_3/N$ の準同型 $T_{m,f}$ が既に存在し、$S_3$ 上恒等**」を使う。$\theta,\tau$ は $\mathrm{Ad}(\bar\Delta),\mathrm{Ad}(\bar\delta)$(定理 T2(ii))で、**$S_3$ 対称性は $T_{m,f}$ の存在に既に織り込まれている**。
> pentagon 側には**対応する $M(0,5)$ 水準の準同型が a priori 存在しない** — HS Prop 7 (i)⟹(iii) が構成する $\tilde F$ は **(III) を仮定して初めて作れる**([LS, Lemma 7] 経由)。**「$B_3$ 水準の shadow が $M(0,5)$ 水準に延びるか」こそが pentagon の内容**であり、それが自動でないことを定理 D4-POWER が定量的に示した(1 次元ぶん延びない候補がある)。
> **この対比を設計文書に明記すること**(Sol 監査点 A・§7)。

---

## 3. 第一標的

### 3.1 委嘱指定の $K_\pi$ 型窓 — 評価: **不適**(理由を数で)

| 篩 | $K_\pi$ / $N_A$ | 判定 |
|---|---|---|
| **F-1** $d(N)\ge2$ | $P=A_5$ 完全 ⟹ $\gamma_2=\gamma_3=A_5$ ⟹ $d=1$ | ✗ |
| **F-2** 標数 5 排除 | $N_{\rm ord}=5$、$\bar x,\bar y$ の位数 5、$Q_P=A\times V$ の $V\cong C_5^3$、$\lvert Q_P\rvert=7500=2^2\!\cdot\!3\!\cdot\!5^4$ | ✗(**$\rho$ の位数 5 とちょうど衝突**) |
| **F-3** 冪零類 $\ge4$ | $A_5$ は冪零でない(類は定義されない) | ✗ |

> ### ★ 系 KPI-RETRO(**既測 20/20 PASS の構造的説明**)
> `gtpi_v1.md` の窓では `Chk6` の $c_3$(pentagon)が **20/20 で真**だった。定理 D2/D3-BLIND(深さ $\le3$ は恒等的に盲目)+ F-2($p=5$ でノルムが退化)+ F-1($d=1$)は、**この 20/20 が「測定結果」ではなく構造の帰結であった可能性が高い**ことを示す。
> **格: 状況証拠**(3 本)。厳密な証明ではない — $A_5$ は完全群ゆえ LCS 論法が直接は効かない(§7【HSP-GAP-2】)。
> **⟹ $K_\pi$ で pentagon を測り直しても新しい情報は出ない公算が大きい。**

**それでも $K_\pi$ 上で書くなら**(委嘱 §3 への形式的回答):
- 対象: $\mathcal G$ = `Chk6` を満たす $(m,q)$ の 20 元(既在・再測定不要)。
- 窓: $W:=\bigcap_{i=0}^{4}\rho^i\bigl(\ker(\varphi\circ p_5)\bigr)$、$\varphi:K(0,4)=F_2\twoheadrightarrow A_5$。$Q\hookrightarrow A_5^5$($\lvert Q\rvert\le60^5=7.8\times10^8$、置換次数 25 — GAP で扱える)。$\bar\rho$ は座標の巡回置換(§3.3 の (M) 参照)。
- 期待値: **20/20 PASS**(= 新情報ゼロ)。**この予言は IF-FIRST として凍結する価値がある**(P-HSP-2・§6)。
- 費用: 小。**較正としてのみ価値がある**(既存 $c_3$ 判定との二経路一致)。

### 3.2 ★ 代替第一標的 — **類 4 冪零窓 $N^{(4,p)}$($p\ge7$)**

> ### 定義 HSP-NW(**冪零窓対**)
> 素数 $p\ge7$、$e\ge1$。$\mathcal V_{4,p^e}$ を「類 $\le4$ かつ指数 $\mid p^e$」の群の多様体とする。
> - $F_2$ 側: $N_{F_2}:=\gamma_5(F_2)\,F_2^{p^e}\,[\ldots]$ = $\mathcal V_{4,p^e}$ の verbal 部分群。
> - $B_3$ 側: $N:=$ $PB_3$ の対応する verbal 部分群の $B_3$ 内での適合化(§5 補題 NW-1)。
> - $K(0,5)$ 側: $W:=$ $K(0,5)$ の同じ verbal 部分群。
>
> **利点(設計上決定的)**: verbal ⟹ **完全不変** ⟹
> (i) $W$ は $\rho$-安定・$S_5$-安定(**(W-b) 自動**);
> (ii) $j(N_{F_2})\subseteq W$(同じ法則で定義されているから)(**(W-c) 自動**);
> (iii) **marking(どの $p_i$ を使うか・$K(0,4)$ の同一視)の自由度がゼロ** ⟹ 罠 #3/#12 と CV-9 規約事故の温床を構造的に消す。

**規模**: $\mathrm{gr}_k(K(0,5))$ の階数は $5,4,10,21$(§2 の検算)⟹ $\lvert Q\rvert=p^{40}$($e=1$)。**置換群では不可能・pc 群(polycyclic)なら 40 生成で軽い。** $F_2$ 側は階数 $2,1,2,3$ ⟹ $\lvert P\rvert=p^8$($p=7$ で $5.7\times10^6$ — GAP で余裕)。

**探索宇宙(事前登録の型)**:
- $m\in\mathcal X_N$($\gcd(2m+1,N_{\rm ord})=1$)。
- $\bar f\in[P,P]$($\lvert[P,P]\rvert=p^6$)。
- hexagon 判定 → GT-shadow 集合 → **その上で $\mathrm{PENT}_W$**。
- **予言**: 各 $m$ について hexagon 解の $\mathfrak h_4$-座標は $\mathbb Z/p^e$ の torsor、pentagon を通るのはそのうち $1/p^e$(系 D4-PRED)。

**なぜこれが層 (b) に効くか**: $\mathrm{PENT}_W$ を通らない gentle GT-shadow が 1 個でも出れば、それは
$$\mathrm{GT}_{\rm arith}(N)\subseteq\mathrm{GT}^{\rm pent}(N)\subsetneq\mathrm{GT}(N)$$
の実証であり、**$\mathrm{GT}(N)$ の新しい上界装置**である(工房が現在持つのは SURV 型の**下界**のみ)。飽和の証明が「下から積み上げる」しかなかった窓で、**上から削る**道具が初めて入る。

### 3.3 (M)$\bar\rho$ の具体形(実装仕様の核)

$W$ が verbal なら $Q=K(0,5)/W$ の生成元は $\bar T_1,\ldots,\bar T_5$ で、
$$\bar\rho:\ \bar T_1\mapsto\bar T_4\mapsto\bar T_2\mapsto\bar T_5\mapsto\bar T_3\mapsto\bar T_1$$
は**生成元の置換**として定義され、$\mathcal V_{4,p^e}$ の相対自由群では自動的に自己同型に延びる(自由性)。**$\bar\rho$ の構成に選択の余地がない** — これが定義ゲートの「後から変えない」規律に最も適合する形である。
そして $\bar f:=$「$f$ の語を $x\mapsto\bar T_1,\ y\mapsto\bar T_2$ で評価」。検査は
$$\bar f(\bar T_3,\bar T_4)\cdot\bar f(\bar T_5,\bar T_1)\cdot\bar f(\bar T_2,\bar T_3)\cdot\bar f(\bar T_4,\bar T_5)\cdot\bar f(\bar T_1,\bar T_2)\ \overset{?}{=}\ 1 .$$
**5 回の語評価と 4 回の積のみ。** 深い機構は不要。

---

## 4. 壁窓(非可解 4 窓 $n=24/28/36/37$)への適用可能性 — **判定: 再開トリガー不充足**

裁定 386 の再開トリガーは「**非可解窓の算術像を読む道具の獲得**(例: HS Prop 7 有限商翻訳の壁窓適用)」である。本設計の結論:

| # | 論点 | 判定 |
|---|---|---|
| **W-1** | 壁窓は $P\cong A_n$(完全)ゆえ $d(N)=1$ ⟹ 篩 **F-1 で落ちる** | 冪零 $W$ を通す経路は**命題 HSP-COLLAPSE で完全に閉じる**(検出力厳密ゼロ) |
| **W-2** | 非冪零 $W$(例: 5 重 packing $Q\hookrightarrow A_n^5$)なら? | **検出力の事前見積りが立たない**。LCS 論法は完全群で沈黙。**DUM-G3 規律(検出力を先に見積る)を満たせない** ⟹ 起票不可 |
| **W-3** | hexagon 側の可換性検査(HS Prop 3/4 型)を壁に載せる案 | **定理 G3 で自動 = 情報ゼロ**(§2.7)。壁窓では $\theta=\mathrm{Ad}(a_1),\tau=\mathrm{Ad}(b_1)$ が $\mathrm{Inn}(A_n)$ に落ちる($a_1,b_1\in A_n$・$\varepsilon=0$)ため、$\mathrm{Out}(P)\cong C_2$ 水準の可換性は空虚 |
| **W-4** | $\bar\rho$ の供給源 | 壁窓は $A_n\times S_3$ で $S_3$ 因子が完全に硬い。5 重 packing 以外に $\rho$ を入れる余地がなく、その packing の検出力は W-2 のとおり見積り不能 |
| **W-5** | **本設計が壁に効かないことの一行の理由** | pentagon の情報が**深さ 4 に集中している**(定理 D4-POWER)のに対し、**完全群には深さがない**。**「深さを持たない窓には、深さで測る道具は届かない」** |

> ### ★ 結論(司令塔へ)
> **裁定 386 の FV-WALL 再開トリガーは、本設計では充足されない。** 凍結は維持すべきである。
> **充足条件を明記する**(将来の再判定用):
> - **(T-1)** 壁窓に対し、$d(N)\ge2$ を回復する**細分**($N'\subsetneq N_{\rm wall}$ で $\gamma_2/\gamma_3$ が非自明になるもの)を構成でき、かつその細分が壁窓の非可解性を保つ。**または**
> - **(T-2)** 完全群商に対する pentagon 検出力の**別の事前見積り法**(LCS でない filtration — 例えば $\mathbb F_\ell$ 表現論・$H^1(\langle\rho\rangle,\cdot)$ の非可換版)が確立する。**または**
> - **(T-3)** 壁窓の $\mathfrak m(N_{\rm wall})$($m$ 像)が測定され、上記いずれかの前件が判定可能になる(現状 $m=0$ と $m=18$ の 2 層のみ)。
>
> **(T-2) は【文献要請】の型である(§7)。**

---

## 5. 必要な補題群のスケッチ + 危険箇所

### 5.1 埋めるべき補題(優先順)

> **補題 NW-1(窓対の存在)**。$p\ge7$、$e\ge1$ に対し、$N\in\mathrm{NFI}_{PB_3}(B_3)$ で $N_{F_2}=\gamma_5(F_2)F_2^{p^e}$(または $\mathcal V_{4,p^e}$ の verbal 核)となるものが存在し、$c\in N$ かつ $N_{\rm ord}=p^e$ となるように取れる。
> **段**: (a) $\mathcal V_{4,p^e}$ の verbal 部分群 $\mathcal V(PB_3)$ は $PB_3$ 完全不変・$PB_3\trianglelefteq B_3$ 特性ゆえ $\mathcal V(PB_3)\trianglelefteq B_3$。(b) 有限指数。(c) $c\in\mathcal V(PB_3)$ かどうかは $c$ の $PB_3/\mathcal V$ での位数の問題 — $c$ を殺したいなら $N:=\mathcal V(PB_3)\cdot\langle\langle c\rangle\rangle$ を取り、$N_{F_2}$ が変わらないことを Dedekind で確認(**罠 #5 に該当 — 分裂を仮定しないこと**)。(d) $N_{\rm ord}$ の計算。
> **【HSP-GAP-1】** (c)(d) は未検証。$PB_3\cong F_2\times\langle c\rangle$ でも $N$ が分裂するとは限らない(**罠 #5**)。

> **補題 NW-2(WD の自動性)**。$W:=\mathcal V(K(0,5))$、$N_{F_2}:=\mathcal V(F_2)$ とすると $j(\mathcal V(F_2))\subseteq\mathcal V(K(0,5))$。
> **証明**: verbal 部分群は任意の準同型で像が像の verbal に入る($j$ は単射準同型)。∎(3 行・閉じている)

> **補題 NW-3($\bar\rho$ の well-defined 性と位数)**。$\mathcal V$ 完全不変 ⟹ $\rho(W)=W$ ⟹ $\bar\rho\in\mathrm{Aut}(Q)$ で $\bar\rho^5=1$。$\bar\rho\ne1$($\bar T_1\ne\bar T_4$ を $\mathrm{gr}_1(Q)$ で確認)。∎(閉じている)

> **補題 D2-INT(整数版の深さ 2)**。§2.1 の整数証明書は $\Lambda^2(\mathbb Z^5)\to\mathrm{gr}_2(K(0,5))$ の核への所属を与える。**ただし「$\mathfrak t$ の二次関係式がすべて群の $\mathrm{gr}_2$ でも成立する」ことは (R1)(R2) が群の関係式の 2 次項であることを要する。**
> **【HSP-GAP-2】** $\mathrm{gr}(K(0,5))$ が捻れなしで階数が $F_3\rtimes F_2$ の和になること(almost-direct product の性質)は**本稿では検算の整合(階数 $5,4,10,21$ の一致 4 件)からの状況証拠**であり、証明していない。**正典外の一般論に依存しないためには、標的窓の有限商で直接確認する**(F-6 の一部)。

> **補題 PB4-EQ**(= 補題 CENT-FREE §1.5)。$Z(PB_4)\cap[PB_4,PB_4]=1$ の一行。**要検分**: full twist の $PB_4^{ab}$ での像が非零であること(2008.00066 (A.2)(A.5) から確認可能・司令塔が (A.5) をページ画像照合済み)。

### 5.2 ★ 危険箇所(踏むと全部壊れる 8 件)

| # | 罠 | 対策 |
|---|---|---|
| **D-1** | **水準混同(最重要)**: HS の舞台 $\mathrm{Out}^\sharp_n$ と工房の $\mathrm{NFI}_{PB_3}(B_3)$。**条件式は一致・窓の圏は別物**(§1.4) | 設計文書に §1.4 の辞書を必ず添付。「$\mathrm{Out}^\sharp_5\cong\widehat{GT}$ を移送した」とは**絶対に書かない** |
| **D-2** | **$K(0,5)$ と $PB_4$ の混同** | $K(0,5)=PB_4/Z(PB_4)$。補題 CENT-FREE で pentagon については同値。**settled/isolated/reduction は同値でない** |
| **D-3** | **定理 G3 の類推** | hexagon 側の可換性は自動。pentagon 側が自動でない理由(§2.7)を明記しない設計は起票しない |
| **D-4** | **$\rho$ の位数と標数 5** | 篩 F-2。$N_{\rm ord}$、$\lvert P\rvert$、$\lvert Q\rvert$ のいずれにも 5 が現れない窓を選ぶ |
| **D-5** | **lift 存在形を使うこと** | 使わない(定理 PENT-NORM のノルム形のみ)。使う場合は「どの $\tilde F$ か」の量化を cert に明記 |
| **D-6** | **語の向き(規約 W-1/W-2)** | pentagon の 5 因子は**非可換な積**であり順序に敏感。定理 PENT-NORM の順序($\rho^4,\rho^3,\rho^2,\rho^1,\rho^0$)は (III) の巡回回転。**GAP 実装では規約 W-1 の反転が入る** — CV-13 型の向きゲート必須 |
| **D-7** | **$\bar\rho$ の marking** | verbal 窓なら選択なし(§3.2 (iii))。$p_i$-packing 窓を使うなら $K(0,4)$ の同一視 5 通りの整合が必要 — **罠 #3/#12** |
| **D-8** | **U-10 への新規荷重** | 本稿は **U-10 を一切使わない**。$\mathrm{PENT}_W$ は $\widehat{GT}$ 側の必要条件(命題 HSP-SOUND)で、$\widehat{GT}=\widehat{GT}_{gen}$ を仮定しない |
| **D-9** ★ | **記号衝突(grep 事故)**: 初稿は深さ 4 の生成元を $\psi_4$、深さ 3 を $\sigma_3$ と書いていた。**$\psi_n$ は 2405 (3.1) の dihedral 写像 $PB_3\to D_n^3$(工房の正典記号・`sol/sol_reply_73_math.md` 等で使用中)、$\sigma_1,\sigma_2$ は braid 生成元**。**両方 $\mathfrak h_3,\mathfrak h_4$ に改名済**(本文はすべて改名後)。以後の文書・コード・cert でこの 2 元を $\psi/\sigma$ で書かないこと |

> **既存の未解決依存への新規荷重: なし。**
> - **U-10**($\widehat{GT}=\widehat{GT}_{gen}$)を使わない(D-8)。
> - **U-PB4** は補題 CENT-FREE で **pentagon 判定に関しては迂回**(荷重が減る)。
> - **U-11 / GAP-GTPI-1**(模型忠実性)には触れない(本稿は $K_\pi$ を標的にしない)。
> - 新規の未解決は【HSP-GAP-1】【HSP-GAP-2】【HSP-GAP-3】(§7)。

### 5.3 定義ゲート 8 項目・罠 12 件の適用(委嘱の規律)

**新窓 $N^{(4,p)}$ を切る以上、較正スイート v2 の 8 項目を通す前提を設計に織り込む**(定義ノート §4)。本件で特に効くもの:

| 項目 | 本件での意味 |
|---|---|
| **2**(探索と検証の helper 非共有) | 簡約 hexagon (3.10)(3.11) で探索、**full $B_3/N$ 上の (3.3)(3.4)** で検証。**pentagon は第三の独立レーン**($Q$ 上)— 3 レーンが互いに helper を共有しないこと |
| **3**(source kernel 証明書) | settled は個数一致では不足(**罠 #2**)。冪零窓では $T_{m,f}$ の核を marked factor map で証明書化 |
| **6**(reduction の分岐被覆) | $N^{(4,p)}\subset N^{(3,p)}$(類を落とす)の reduction で $\mathrm{PENT}$ の整合(深さを落とすと検出力が消えることの実測 = **定理 D3-BLIND の実測版**) |
| **7**($N_5$ control・$c\ne1$) | 補題 NW-1 (c) の $c$ の扱いに直結。**$c$ が生きている窓での挙動を必ず control に置く** |
| **罠 #5** | $PB_3/N\ne(F_2/N_{F_2})\times\langle cN\rangle$ を仮定しない |
| **罠 #6** | charming は $[F_2/N_{F_2},F_2/N_{F_2}]$ で列挙(**$[B_3/N,B_3/N]$ ではない**) |
| **罠 #12** | 計算量予測に $\lvert Q\rvert$、$\lvert[P,P]\rvert$、$\lvert\mathcal X_N\rvert$ を記録 |

---

## 6. 検算 script(収蔵先とハッシュ)

**収蔵**: `search/probe/hsp7_v1/`。**すべて単系統 python・厳密有理数または 2 素数以上の剰余算術。$K^{(5)}$ 非接触**(純粋な自由 Lie 環の線型代数)。

| script | SHA-256 | 内容 |
|---|---|---|
| `hs_prop7_gr2_check.py` | `b10b0c7994fa5a8d9d3603562328bd514386d336caaf180cbfc9c537dde91868` | 深さ 2($\Lambda^2$ 直接実装・厳密有理数)。$\dim V=5$/関係式 6/$\dim\mathfrak t_2=4$/**$P=0$**/対照 $[T_1,T_2]\ne0$/**整数係数証明書** |
| `hs_prop7_depth3_check.py` | `608f878e96f559d803a11cb4455411e546c3fd3862992e4b272856d73ba74d06` | **第二独立実装**(テンソル代数・厳密有理数)。深さ 2 を再現 + 深さ 3: $\dim\mathfrak t_3=10$・$\nu_3$ の階数 1・$\ker\nu_3=\langle u_1+u_2\rangle$ |
| `hs_prop7_depth4_check.py` | `cc24a95c44ef2154b632ca6738c9dfce8dece03df26b81feeffbe4e789d11331` | 深さ 4(mod $10^9{+}7$ と mod $2^{31}{-}1$ の**二素数一致**)。$\dim\mathfrak t_4=21$・$\nu_4$ 階数 3(単射)・(3.10)-locus 上階数 2・$\Theta\ne0$ |
| `hs_prop7_hexagon_vs_pentagon.py` | `7f99fc778e404d22cd02e68a05da2d6c5ad160829b335eebb447262538612ba7` | $F_2$ 側 hexagon の次数別解空間(厳密有理数)。$\theta^2=\tau^3=1$・$xyz=1$ の自己検査つき。**深さ 2: $c_2=0$ 強制/深さ 3: $\langle u_1+u_2\rangle$/深さ 4: $\langle(1,4,1)\rangle=\mathfrak h_4$** |
| `hs_prop7_dummy_and_primes.py` | `dc3a4557b37687f86edd391b41806dceb71b1c0c9d696321a82d31dc1250b826` | dummy 検証 + **標数プロファイル** $p\in\{2,3,5,7,11,13,10^9{+}7\}$。**$p=5$ でのみ $\nu_4(\mathfrak h_4)=0$**・$\mathfrak h_3$ は全 $p$ で pentagon 通過 |

**内蔵している独立の整合検査(偶然の一致では説明できない 6 件)**:
$\dim\mathfrak t_1=5$、$\dim\mathfrak t_2=4$、$\dim\mathfrak t_3=10$、$\dim\mathfrak t_4=21$ が **$F_3\rtimes F_2$ の Witt 数の和**と全て一致 / $\rho(t_{13})=t_{14}$ が $t_{ij}$ の $T$-展開と独立に整合 / $\tau^3=\mathrm{id}$・$\theta^2=\mathrm{id}$・$xyz=1$ / Hall 関係 $[[[x,y],y],x]=[[[x,y],x],y]$ / 深さ 2 の結論が **2 実装**(外積 vs テンソル)で一致 / 深さ 4 が **2 素数**で一致。

---

## 7. 格付け・GAP・新規性・IF-FIRST・申し送り

### 7.1 格付け表(項目別)

| 主張 | 格 |
|---|---|
| 定理 NORM((I)(II)(III) = 位数 2/3/5 のノルム) | **paper-proof**(HS 原文 + 3 行) |
| **定理 PENT-NORM**((III) ⟺ $\rho$-ノルム) | **paper-proof**(2 行・巡回回転) |
| 定義 HSP-W/HSP-T、補題 HSP-WD、命題 HSP-SOUND | **paper-proof** |
| **補題 CENT-FREE**($K(0,5)$ 窓で $PB_4$ pentagon 判定可) | **paper-proof(要検分)** — full twist の abelian 化での非零性に依存 |
| **定理 D2-BLIND** | **paper-proof + 単系統 candidate**(整数証明書つき・2 実装一致)。**cross-checked ではない**(CV-9 未実施・同一著者) |
| **系 D2-C2**(C2-Q R3 の独立証明) | **paper-proof**(D2-BLIND + 1 行) |
| **定理 D3-BLIND** | **paper-proof**((b) は手計算 3 行)**+ 計算 candidate**((a)) |
| **定理 D4-POWER / 系 D4-DUM** | **finite-exhaustive candidate**(厳密有理数 + 2 素数)。**紙の証明は (a) の手計算部分のみ** |
| **命題 HSP-COLLAPSE / 系 HSP-ODD / 系 HSP-WALL** | **paper-proof**(4 行) |
| $p=5$ 退化 | **計算 candidate**(1 実装・7 標数) |
| 系 KPI-RETRO($K_\pi$ 20/20 の説明) | **状況証拠**(証明ではない) |
| §4 の壁窓判定 | **設計判断**(命題 HSP-COLLAPSE は定理・W-2 は「見積り不能」という UNKNOWN の宣言) |

**verified(Lean)は一つもない。cross-checked も一つもない**(CV-9 主検問未実施・全 script は本稿起草者が書いた **single lane**)。

### 7.2 【GAP】— 埋められなかった穴

> **【HSP-GAP-1】窓対の存在**(補題 NW-1 (c)(d))。$c$ の扱いと $N_{\rm ord}$ の計算が未検証。**罠 #5 の領域**。

> **【HSP-GAP-2】$\mathrm{gr}(K(0,5))$ の整数構造**。捻れなし・階数の和・二次表示は**状況証拠 4 件**で支えているが証明していない。§2 の全結論は $\otimes\mathbb Q$ の水準では確実、**整数/有限窓水準では標的窓での直接確認が必要**(篩 F-6 に編入済)。

> **【HSP-GAP-3】非冪零窓での事前見積り法が無い**。完全群商($K_\pi$・壁窓)に対して LCS 論法は沈黙する。**これが §4 の判定と §3.1 の判定を「証明」でなく「見積り不能の宣言」に留めている原因。**
> ### 【文献要請 HSP-L1】
> - **困難**: 有限群 $Q$($Q$ は非冪零・しばしば完全群を商にもつ)と位数 5 の $\bar\rho\in\mathrm{Aut}(Q)$ に対し、ノルム写像 $N_{\bar\rho}(g)=\bar\rho^4(g)\cdots g$ の**像・fiber の大きさ**を、$Q$ の構造(合成因子・$\bar\rho$ の作用)から**事前に見積る**方法。冪零の場合は LCS の次数別解析(本稿 §2)で解けるが、完全群では filtration が無い。
> - **欲しい結果の型**: (α) 非可換 $H^1(\mathbb Z/5,Q)$ の有限性/計算可能性と、$N_{\bar\rho}$ の fiber との対応。(β) $Q$ が(準)単純のとき「twisted norm が全射/自明」となる判定条件。(γ) $\bar\rho$ が外部自己同型か内部かで挙動が変わるか($\mathrm{Out}(A_n)=C_2$ に位数 5 は無い ⟹ 壁窓では $\bar\rho$ は必然的に内部側 — この観察が使えるか)。
> - **格**: UNKNOWN。**外部検索は一切していない**(文献ゲート遵守)。

> **【HSP-GAP-4】深さ 5 以上は未計算。** 定理 D4-POWER は深さ 4 の話。深さ 5 で検出力がさらに増える(または $p=5$ 退化が回復する)かは UNKNOWN。$\dim\mathfrak t_5$、$\mathrm{gr}_5(F_2)$(階数 6)の計算は同じ script で可能(次数 5 のテンソル空間は $5^5=3125$ — 実行時間のみの問題)。

### 7.3 新規性の申告(**grep 済**)

`grep -rn "Prop 7\|pentagon\|rho-norm\|ノルム\|psi_4\|sigma_3\|HSP-"` を `docs/ sol/ provenance/ ideas/` で実施。**先行が 2 件見つかったので、初稿の新規性主張を下方修正する。**

> ### ★ 先行の発見 1(**定理 NORM の hexagon 半分は既在**)
> `docs/notes/epsilon_mechanism_v2.md` **L97**: 「θ-公理 $f\tilde\theta(f)=1$ = **位数 2 作用素の 2 重ノルム**。τ-公理 $R_\tau(m,f)=c^m$ = **位数 3 作用素の 3 重ノルム**。$B_3/Z\cong PSL_2(\mathbb Z)\cong C_2*C_3$ の二つの捻れ生成元に対応。」
> ⟹ **「hexagon = 位数 2,3 のノルム」は工房が独立に到達済み**(【GAP-1′】の文脈)。**定理 NORM の表の上 2 行は新規ではない。**
> **本稿の寄与はその第 3 行**: 位数 5 の作用素が $K(0,5)$ 上に**存在し**、その 3 重目のノルムが pentagon そのものであること(定理 PENT-NORM)。$C_2*C_3$ が $B_3/Z$ の中で閉じているのに対し、**位数 5 は $B_3$ の外(= $M(0,5)$)にしかない** — これが「cross-frame でなければ書けない」ことの、既存の言葉での言い換えである。
> ⟹ **ideas_008 の【GAP-1′】(「$B_3$ 方向の 2 本のノルム公理が、なぜ $\tilde\chi$ 方向のノルム条件を導くのか」)と本稿は同じ族の問いを扱っている。** 司令塔は両者の接続を検討されたい(§7.5-7)。

> ### 先行の発見 2(**記号衝突**)
> $\psi_4$ は既に dihedral 写像として使用中。危険箇所 D-9 に記載し改名済。

- **pentagon の語判定**は既存(`gtpi_v1.md` の `Chk6` $c_3$・`litgate_pentagon_v1.md` §2.1 の 2008.00066 (2.20))。**本稿は判定式を新設していない。**
- **新規と主張するもの(修正後)**: ①定理 PENT-NORM(**pentagon = 位数 5 のノルム**・量化子なし)②定理 D2/D3-BLIND と系 D2-C2 ③**定理 D4-POWER と dummy $\mathfrak h_4$** ④命題 HSP-COLLAPSE と系 HSP-ODD ⑤補題 CENT-FREE ⑥$p=5$ 退化 ⑦篩 HSP-F。
- ①は HS の Lemma 1 + Prop 7 の**組み合わせの読み替え**であって HS 自身が書いていてもおかしくない(HS §2.3 の証明は実質これをやっている)。しかも hexagon 側は工房で既在(上記)。**「初」とは書かない。**
- ③の $\mathfrak h_4=(1,4,1)$ は古典の GT₀ vs GT の次数 4 の差に対応するはずのもの。**外部文献未確認ゆえ「工房内で独立に導出した」とのみ書く。**

### 7.4 ★ IF-FIRST(**実測に先行して凍結すべき予言・アンカー・停止規則**)

> **本節は実装前の凍結対象。値をコードに書かない・測定完了まで開封しない(u7_fire 様式)。**

**アンカー(既測データとの retrodiction)**
- **A-HSP-1**: $K_\pi$ 窓の `Chk6` $c_3$ = 20/20 PASS。本設計の $\mathrm{PENT}_W$ を $K_\pi$ に載せた場合も **20/20 PASS** であること(二経路一致)。
- **A-HSP-2**: dummy $f_{\rm dum}=\exp(t\mathfrak h_4)$ は**どの適合窓でも FAIL**、$\exp(t\mathfrak h_3)$($\mathfrak h_3=u_1+u_2$)は**どの適合窓でも PASS**。

**予言(測る前に凍結)**
| # | 予言 |
|---|---|
| **P-HSP-1** | $d(N)=1$ かつ $Q$ 冪零の窓では $\bar f=1$ が全 charming 候補で成立し、$\mathrm{PENT}_W$ は 100% PASS(**命題 HSP-COLLAPSE の実測版**) |
| **P-HSP-2** | $K_\pi$: 20/20 PASS(**新情報ゼロ**) |
| **P-HSP-3** | 類 3 以下の冪零窓: 100% PASS(**定理 D2/D3-BLIND の実測版**) |
| **P-HSP-4** | 類 4・指数 $p$($p\ge7$)の窓: hexagon 解のうち pentagon を通るのは **$\mathfrak h_4$-座標について $1/p$**。とくに $p=7$ なら **6/7 が FAIL** |
| **P-HSP-5** | 同じ設計を $p=5$ で走らせると **100% PASS**($\nu_4(\mathfrak h_4)\equiv0$ の実測版)— **$p=7$ と $p=5$ の対照が本走の最強の内部 control** |
| **P-HSP-6** | $m$ 依存性: $\Theta\ne0$ ゆえ pentagon を通る $\mathfrak h_4$-座標の値は **$c_2^2=(m(m+1)/6)^2$ の関数**として $m$ ごとに変わる(定数でない) |

**停止規則**
- **S-1**: 篩 F-1〜F-4 のいずれかが落ちたら **その窓は起票しない**(実装予算ゼロ)。
- **S-2**: F-6(dummy が実際に FAIL すること)が確認できなければ**本走に進まない**。
- **S-3**: P-HSP-5($p=5$ control)が PASS 100% にならなければ、**実装バグと判定して本走を止める**。
- **S-4**: 本走で FAIL が 1 件でも出たら、**その 1 件について full $B_3/N$ 上の (3.3)(3.4) 再検証 + 2008.00066 (2.20) の $PB_4$ 経路での独立再現**を先に済ませる(pentagon-fake の主張は二経路一致まで保留)。
- **S-5**: 深さ 5 以上に踏み込む場合は本ノートの v2 を先に書く(**versioned 規律**)。

### 7.5 申し送り(司令塔へ)

1. ★ **標的の差し替え判断を要請**: 委嘱の第一標的 $K_\pi$ は篩 F-1/F-2/F-3 で落ちる(§3.1)。**類 4 冪零窓 $N^{(4,7)}$ への差し替え**を推奨する。速達で先行照会済。
2. ★ **裁定 386(FV-WALL)の再開トリガーは充足しない**(§4)。凍結維持を推奨。充足条件 (T-1)(T-2)(T-3) を地図に記載されたい。
3. ★ **裁定 408 の文言の更なる精密化**: 「層 (b) は GTPI/HS Prop 7 のみが道」→ 本稿は **HS Prop 7 の道が「深さ 4・$d(N)\ge2$・標数 $\ne5$ の窓」に限られる**ことを示した。**dihedral 予想の open 標的族(奇・混合)には届かない**(系 HSP-ODD)。地図の該当行を更新されたい。
4. **【文献要請 HSP-L1】**(§7.2)を関所に提出。
5. **CV-9**: 本稿の script はすべて起草者が書いた single lane。**非当事者(falsifier)の判読**が済むまで cross-checked と書かない。
6. **新規性**: §7.3 のとおり「初」の主張はしない。$\mathfrak h_4$ の外部文献照合が要るなら paper-scout へ。
7. ★ **【GAP-1′】との接続**(§7.3 の先行発見 1): `epsilon_mechanism_v2.md` L97 が既に「hexagon = 位数 2,3 のノルム」に到達しており、本稿はその族に**位数 5(pentagon)**を追加した。**【GAP-1′】(「$B_3$ 方向の 2 本のノルムが、なぜ $\tilde\chi$ 方向のノルムを導くのか」)は、$C_2*C_3=B_3/Z$ という**三角群の構造**の問いである。位数 5 は $B_3/Z$ に無く $M(0,5)$ にしかない — この対比が【GAP-1′】の解決に効く可能性がある。発案係/Sol への諮問候補。
8. **記号衝突の恒久対策**: $\mathfrak h_3,\mathfrak h_4$ を規約台帳(`conventions_ledger_v1.md`)に登録されたい(D-9)。

### 7.6 Sol への監査依頼(優先順位つき)

- **監査点 A(最優先)**: **§2.7 の対比** — 「hexagon 側の可換性は定理 G3 で自動、pentagon 側は自動でない」の論理。G3 の証明が使っている「$T_{m,f}$ が $B_3$ 準同型で $S_3$ 上恒等」に対応する $M(0,5)$ 水準の構造が**存在しない**ことが、本設計全体の存在理由である。ここが誤りなら本稿は C2-Q の再演になる。
- **監査点 B**: **定理 D4-POWER (a)** — hexagon の深さ 4 斉次解空間が 1 次元 $\langle(1,4,1)\rangle$ であること。手計算($1+\tau_0+\tau_0^2$ の像が階数 1)と script が一致しているが、$\tau$ が**次数付きでない**(filtered)ことの扱いに一段の注意が要る。とくに「$y^m$ 共役は深さ 5 以上にしか効かない」の一行。
- **監査点 C**: **定理 D2-BLIND の整数版**(【HSP-GAP-2】)。$\mathrm{gr}_2(K(0,5))$ の整数構造を正典外の一般論なしに固定する方法があるか。
- **監査点 D**: **補題 CENT-FREE** — $Z(PB_4)\cap[PB_4,PB_4]=1$ と、それが pentagon 判定の $PB_4\to K(0,5)$ 移送を正当化すること。**これは【文献要請 U-PB4】の一部を消す可能性がある**ので、その射程の判定も願いたい。
- **監査点 E**: **命題 HSP-COLLAPSE** の 4 行(とくに「部分群の LCS は全体の LCS に含まれる」+「$\gamma_2(P)=\gamma_3(P)$ は商に遺伝」)。ここから系 HSP-ODD(奇 dihedral 族が構造的に外れる)が出るので、影響が大きい。
- **監査点 F**: **§3.2 の verbal 窓設計**が定義ゲート 8 項目・罠 12 件に照らして妥当か。とくに罠 #5(分裂を仮定しない)と項目 7($c\ne1$ control)。

---

## 付録 A. 記号早見

| 記号 | 意味 |
|---|---|
| $K(0,n)$ | $\pi_1(\mathcal M_{0,n})$。$K(0,4)=F_2$、$K(0,5)\cong F_3\rtimes F_2\cong PB_4/Z(PB_4)$ |
| $j$ | $K(0,4)\hookrightarrow K(0,5)$, $x\mapsto x_{12},y\mapsto x_{23}$ |
| $\rho$ | $x_{i,j}\mapsto x_{i+3,j+3}$。位数 5。$(1\,4\,2\,5\,3)\in S_5$ の上 |
| $T_i$ | $\mathrm{gr}_1$ での $x_{i,i+1}$ の類。$\rho: T_1\to T_4\to T_2\to T_5\to T_3\to T_1$ |
| $N_\rho(f)$ | $\rho^4(f)\rho^3(f)\rho^2(f)\rho(f)f$($\rho$-ノルム)= pentagon の defect |
| $\nu_k$ | $\sum_{i=0}^4\rho^i$ の $\mathrm{gr}_k$ での作用 |
| $P$ | $\sum_i\rho^i([T_1,T_2])$(pentagon cycle)。**$=0$ in $\mathrm{gr}_2$** |
| $\Theta$ | $\tfrac12\sum_{i>j}[\rho^iw,\rho^jw]$、$w=[T_1,T_2]$。**$\ne0$ in $\mathfrak t_4$** |
| $\mathfrak h_3$ | $u_1+u_2=[[x,y],x]+[[x,y],y]$。hexagon の深さ 3 の唯一方向・**pentagon を通る** |
| $\mathfrak h_4$ | $v_1+4v_2+v_3$。hexagon の深さ 4 の唯一方向・**pentagon を破る = dummy** |
| $d(N)$ | $\lvert\gamma_2(P)/\gamma_3(P)\rvert$($P=F_2/N_{F_2}$)。C2-Q の $d$ |
| $\mathrm{PENT}_W$ | 定義 HSP-T の有限 pentagon 検査 |
