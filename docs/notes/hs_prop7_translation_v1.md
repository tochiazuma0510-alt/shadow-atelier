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

---
---

# 8. 便 100 検収 erratum(裁定 422)— 呼称分離・撤回・修理形採録・**補題 NW-1 v2**

> **形式**: **追記型。§0–§7 と付録 A は一切改変しない。** 本節は Sol 便 100 返信(`sol/sol_reply_100_math27.md`)の W100-1.1〜1.5・W100-7.1・P100-1.1・P100-1.2 に対する **current erratum** であり、下表の項目については**本節が effective source** である(CV-10)。
> 起草: 数学者(Opus 5)・2026-08-02 / 委嘱 = **裁定 422**(便 100 検収)修文束 A。
> **本節の主張はすべて紙の証明。** 唯一の機械は **§8.11 の検算 1 本**(自由 Lie 環の線型代数・整数/有理数演算・14 検査 FAILS=0)であり、**窓の測定・shadow の測定は一切していない。$K^{(5)}$ 非接触。**

## 8.0 効力表(どの主張が本節で置き換わるか)

| 本文の箇所 | 状態 | 置換先 |
|---|---|---|
| §1.2「HS Prop 7 の二行証明」型の呼称 | ★ **呼称変更** | §8.1(**HS (III) の PENT-NORM 書換え**) |
| §2.1 系 D2-C2 の「pentagon は $c_2$ に何の条件も課さない」 | ★ **弱化** | §8.2 の正文 |
| §2.3 系 D4-PRED(検出比 $(p-1)/p$) | ★ **撤回** | §8.3.1(「解は高々 1」まで)+ §8.3.2(修理形) |
| §7.4 P-HSP-4 / P-HSP-5 / P-HSP-6 | ★ **撤回**(P-HSP-5 は限定 control として残置) | §8.3.2 / §8.3.4 |
| §7.4 A-HSP-2 の $\mathfrak h_3$ 半分 | ★ **弱化**(当方の自己捕獲) | §8.3.3 |
| §2.4 / §3.1 の「$p=5$ は情報ゼロ」「$K_\pi$ は構造的に情報ゼロ」 | ★ **弱化** | §8.3.4 / §8.4 |
| §2.5 系 HSP-ODD・系 HSP-WALL | ★ **限定を明示**(nilpotent route 限定) | §8.5 |
| §5.1 補題 NW-1(省略記号つき)・【HSP-GAP-1】 | ★ **置換・閉鎖(紙)** | §8.7 **補題 NW-1 v2** |
| §2.3 系 D4-DUM($f_{\rm dum}=\exp(t\mathfrak h_4)$) | ★ **有限群元として明示化** | §8.7.4 定義 DUM-FIN |
| 上記以外(PENT-NORM・HSP-WD・HSP-SOUND・CENT-FREE・D2-BLIND・D3-BLIND・HSP-COLLAPSE・篩 F-1〜F-6 の骨格) | **不変**(Sol PASS) | — |

---

## 8.1 【W100-1.1】呼称の分離 — 「**HS (III) の PENT-NORM 書換え**」

Sol F100-1.1 は §1.2 の 2 行を PASS としたうえで、**HS Proposition 7 本体と同一視するな**と指示した。以後、工房の文書・cert・地図・LEDGER では次の呼称を用いる。

> | 対象 | 正式名 | 内容 | 前件 |
> |---|---|---|---|
> | 本稿 §1.2 の定理 | ★ **HS (III) の PENT-NORM 書換え** | (III) $\iff\rho^4(f)\rho^3(f)\rho^2(f)\rho(f)f=1$。**量化子なしの代数的巡回書換え** | **(I)(II) 不要** |
> | HS Proposition 7 | **HS Prop. 7**(構成定理) | (III) $\iff$ $F$ が $K(0,5)$ 上の $\rho$-可換 lift をもつ | ★ **(I)(II) 相対**(直後の Remark の Ihara 例が前件の必要性を示す) |

- **禁止表現**: 「HS Prop 7 の 2 行証明」「Prop 7 を 2 行で示した」。**本稿が 2 行で示したのは (III) の書換えであって Prop 7 の lift 同値ではない。**
- §1.2 の ★ 設計上の意味 2「Prop 7 の付加価値は検出ではなく構成」という区別は**この呼称分離と同じことを言っている**ので有効。ただし「構成」の側は (I)(II) 相対であることを併記する。
- §7.1 格付け表の行「**定理 PENT-NORM**((III) ⟺ $\rho$-ノルム)| paper-proof(2 行・巡回回転)」は**そのまま有効**(この行は元から (III) の書換えしか主張していない)。

---

## 8.2 【W100-1.2】系 D2-C2 の弱化(正文)

**撤回する文**(§2.1 の ⚠ 精確化の第 1 文):

> ~~「**pentagon は $c_2$ に何の条件も課さない**(深さ 2 の成分が空虚だから)」~~

**正文(以後これを引く)**:

> ### 系 D2-C2(v2・便 100 W100-1.2 の指定形)
> P99-C2-BLIND の結論と**独立に整合して**、pentagon の一次の LCS 影である**次数 2 成分も $c_2$ を分離しない**。
> **これは、任意の invariant の factorization や full pentagon の $c_2$-射影を分類する定理ではない。**

**理由(Sol W100-1.2 を当方が確認)**: 本文 §2 自身が $\Omega_4=\nu_4(F_4)+c_2^2\Theta$ と書き、§2.3 (d) で $\Theta\ne0$ を報告している。ゆえに**高次方程式が $c_2$ の可能値を制限することは論理的に残る**。「D2 だけから P99 の要求した factorization theorem を埋めた」は出ない。

**波及**:
- §7.1 の行「系 D2-C2(C2-Q R3 の独立証明)| paper-proof(D2-BLIND + 1 行)」は**格は保つが射程を上記正文に限る**。
- §2.1 の ⚠ 第 2 文(「$c_2$ は detector ではないが parameter ではある」)は**不変**(むしろ弱化と整合)。
- 「P99 の factorization theorem を埋めた」という主張は**どの文書でも使わない**。

---

## 8.3 【W100-1.3 / W100-1.4】撤回と修理形の採録

### 8.3.1 撤回表(凍結予言から外すもの)

| # | 撤回する主張 | 撤回理由(Sol W100-1.3・当方確認) | 残る正しい部分 |
|---|---|---|---|
| **R-1** | 系 **D4-PRED**「hexagon を満たす候補のうち pentagon を通るのは**ちょうど 1 通り**・検出比 $(p-1)/p$」 | 1 次元 affine fiber 上で $\nu_4(\mathfrak h_4)\ne0$ が言うのは **解が高々 1 個**まで。**offset がその直線に入る証明がない**ので 0 個でもよい | 「$\nu_4(\mathfrak h_4)\ne0$ ⟹ pentagon 解は **fiber あたり高々 1 個**」 |
| **R-2** | **P-HSP-4**「類 4・指数 $p$($p\ge7$)の窓: pentagon を通るのは $1/p$。$p=7$ なら 6/7 が FAIL」 | R-1 と同じ(全 hexagon 候補への一般化) | ★ **§8.3.2 の明示 family に限れば定理**(定理 DUM-1/p) |
| **R-3** | **P-HSP-5**「$p=5$ で走らせると **100% PASS**」 | $\nu$ 自体は $p=5$ でも 0 でない(同じ計算が $\Theta\ne0$ を報告)。言えるのは「$\mathfrak h_4$-座標による **fiber 内分離**が死ぬ」まで | ★ **§8.3.2 の $m=0$ dummy family に限れば有効な control**(全候補 control としては撤回) |
| **R-4** | **P-HSP-6**「pentagon を通る $\mathfrak h_4$-座標の値は $c_2^2$ の関数として $m$ ごとに変わる」 | R-1 と同じ未証明(offset 所属)に依存 | 「$\Omega_4$ の式に $c_2^2\Theta$ が現れ、$\Theta\ne0$」までは不変 |
| **R-5** | 【当方の自己捕獲・Sol 指摘外】 **A-HSP-2** の後半「$\exp(t\mathfrak h_3)$ は**どの適合窓でも PASS**」 | §8.3.3 参照。有限窓では $\gamma_4$ 剰余が残るため **exact な PASS は出ない** | 「$\bmod\ \gamma_4(Q)$ で PASS」(= 定理 D3-BLIND の実測版として正しい形) |

**維持するもの**: A-HSP-1(較正として・§8.4 の位置づけ)・P-HSP-1・P-HSP-2(較正として)・P-HSP-3・停止規則 S-1〜S-5。

### 8.3.2 ★★ 修理形の採録 — **定理 DUM-1/p**(P100-1.1)

> ### 定理 DUM-1/p(有限 dummy family と「ちょうど $1/p$」の正しい射程)
> $p\ge7$。$N_{F_2}:=\gamma_5(F_2)F_2^{\,p}$、$P:=F_2/N_{F_2}$、$W:=\gamma_5(K(0,5))K(0,5)^{\,p}$、$Q:=K(0,5)/W$(§8.7 の窓対)。$h_4\in\gamma_4(P)$ を §8.7.4 の**明示の交換子語**とし、
> $$f_t:=h_4^{\,t}\quad(t\in\{0,1,\dots,p-1\}),\qquad m=0$$
> の $p$ 元だけを事前登録する。このとき:
> **(a)** 各 $[0,f_t]$ は **charming**($f_t\in\gamma_4(P)\subseteq[P,P]$、$2\cdot0+1=1\in(\mathbb Z/N_{\rm ord})^\times$)。
> **(b)** 各 $[0,f_t]$ は **簡約 hexagon (3.10)(3.11) を exact に満たす**(§8.7.5・**次数 4 の斉次解ではなく $P$ の中の等式として**)。
> **(c)** **SURJ は自動**(§8.7.6・既在の系 H8′)。
> **(d)** $\mathrm{PENT}_W([0,f_t])\iff t\cdot\nu_4(j\mathfrak h_4)=0$ in $\gamma_4(Q)$。
> ⟹ **$\nu_4(j\mathfrak h_4)\ne0$ in $\gamma_4(Q)$ が標的商で直接確認できれば、$t=0$ の 1 個だけが PASS、他の $p-1$ 個が FAIL。すなわち「ちょうど $1/p$」は、全 shadow ではなくこの明示 family についての定理になる。**

**証明(要点)**。(a) 明らか。(b)(c) は §8.7.5 / §8.7.6。(d): $\gamma_4(Q)$ は $\gamma_5(Q)=1$ より $Q$ の中心に含まれ、$Q^{\,p}=1$ より初等アーベル。$\bar\rho$ は $\gamma_4(Q)$ を保つので 5 因子はすべて可換な $\gamma_4(Q)$ の中にあり、積は座標の和に一致する。ゆえに
$$N_{\bar\rho}(j(f_t))=\prod_{i=0}^{4}\bar\rho^{\,i}\bigl(j(h_4)\bigr)^{t}=\bigl(\nu_4(j\mathfrak h_4)\bigr)^{t}\quad\text{in }\gamma_4(Q)\cong\mathbb F_p^{\,\dim}. \qquad\blacksquare$$

> ★ **なぜ「深さ 4 = 窓の最上層」でだけ全部が exact になるのか(設計上の核心)**
> $f_t$ が $\gamma_4(P)$(= 類 4 窓の **最上層**・中心・初等アーベル)に居るため、
> ① BCH 補正がすべて $\gamma_8=1$ に落ち、② $\theta,\tau,\bar\rho$ の作用が**次数付き作用そのもの**になり、③ 群の積が $\mathbb F_p$-加法になる。
> ⟹ **「次数 4 の斉次計算」と「有限群での exact な等式」が一致する。**
> これは深さ 3 では成立しない(§8.3.3)。**Sol の修理形が深さ 4 = 類 4 窓の最上層を選んだことは偶然でなく、この三つを同時に成立させる唯一の位置である。**

### 8.3.3 ★ 当方の自己捕獲 — $\mathfrak h_3$ アンカー(A-HSP-2 後半)の弱化

**発見**: §7.4 の A-HSP-2 は「$\exp(t\mathfrak h_3)$($\mathfrak h_3=u_1+u_2$)は**どの適合窓でも PASS**」と書いていたが、これは**有限窓では成立しない**。

**理由**。$h_3\in\gamma_3(P)$ を $\mathfrak h_3$ に対応する交換子語とする。類 4 窓では $\gamma_3(Q)$ は可換($[\gamma_3,\gamma_3]\subseteq\gamma_6=1$)だが**中心ではない**($[\gamma_3,\gamma_1]=\gamma_4\ne1$)。$\prod_i\bar\rho^i(j(h_3))$ の $\gamma_3/\gamma_4$ における類は $\nu_3(\mathfrak h_3)=0$(定理 D3-BLIND (a))だが、**積そのものは $\gamma_4(Q)$ の元であって $1$ とは限らない**。しかもその $\gamma_4$-剰余は**語 $h_3$ の代表元の取り方に依存する**。

**正しいアンカー形(置換)**:
> **A-HSP-2′**: dummy $f_t=h_4^{\,t}$($t\ne0$)は**適合窓で FAIL**(定理 DUM-1/p (d)・$\nu_4(j\mathfrak h_4)\ne0$ 相対)。$h_3$ 方向は **$\bmod\ \gamma_4(Q)$ で PASS**(定理 D3-BLIND の実測版)。**exact な PASS は主張しない。**

**同じ理由で hexagon も弱まる**: $h_3\theta(h_3)$ は $\gamma_4(P)$ に入るが $1$ とは限らないので、**$h_3^{\,t}$ は exact な hexagon 解ではない**(次数 4 の補正項が要る)。⟹ **$\mathfrak h_3$-family を dummy/control として使うなら「$\bmod\ \gamma_4$」を判定式に明記すること。**

### 8.3.4 【W100-1.4】標数 5 の正しい射程

**撤回**: 「$p=5$ 窓一般の情報量はゼロ」「全 hexagon shadow が 100% PENT PASS」。

**正文**:
> $\nu=\sum_{i=0}^4\rho^i$ は $\mathrm{ord}(\bar\rho)=5$ ゆえ標数 5 で $(\rho-1)^4$ に退化し、計算した特定方向について $\nu_4(\mathfrak h_4)\equiv0\pmod5$。**しかし $\nu$ 自体は 0 にならない**(同じ計算が $\Theta\ne0$ を報告している)。ゆえに言えるのは
> **「$p=5$ では $\mathfrak h_4$-座標による fiber 内分離が死ぬ」**
> までである。

**control としての残置**: P-HSP-5 は **§8.3.2 の $m=0$ dummy family に限れば有効**(その family では PENT $\iff t\nu_4(\mathfrak h_4)=0$ が全 $t$ で真になる)。**全候補 control としては撤回。** 停止規則 S-3(「$p=5$ control が 100% PASS でなければ実装バグ」)も**同 family 限定**に読み替える。

**篩 F-2 の格**: 「窓の関与標数に 5 を含まない」は **$\mathfrak h_4$-座標検出器に対する篩**であって、pentagon 一般の篩ではない。$p=5$ の affine obstruction は **UNKNOWN**(W100-7.1)。

---

## 8.4 【W100-1.5】$K_\pi$ の扱い — 「情報ゼロ」は撤回、**安価な向き較正として残す**

**撤回**: 系 KPI-RETRO の言い回しのうち「$K_\pi$ は**構造的に情報ゼロ**」「新しい情報は出ない公算が大きい」を**断定として使わない**。

**Sol W100-1.5 の 3 点(当方確認済)**:
1. **HSP-COLLAPSE の前件は $Q$ 冪零**である。提案した $K_\pi$ packing $Q\le A_5^5$ は**非冪零**なので、**篩 F-1 はこの標的を排除しない**。§3.1 の表で $K_\pi$ を F-1/F-3 で「✗」としたのは**射程外適用**であり、正しくは「**F-1/F-3 は非冪零 packing には適用できない(判定不能)**」。
2. mod 5 の $\mathfrak h_4$ 退化は **class-4 Lie detector の一方向**の話であり、非冪零 $A_5^5$ の norm map 全体を消さない。⟹ 篩 F-2 の $K_\pi$ 行も同様に「判定不能」。
3. 既測 20/20 は有力な **retrodiction** だが、本文自身の格付けどおり**状況証拠**。

**正しい位置づけ(正文)**:
> **$K_\pi$ は discovery の第一標的から外す**(裁定 420 の判断を追認)。ただし **安価な向き較正として残す** — 既存 `Chk6` の $c_3$ 判定と、本稿の $\mathrm{PENT}_W$(定義 HSP-T)の**二経路一致**を見る価値がある。P-HSP-2(20/20 PASS)は**予言でなく較正アンカー**として凍結する。
> **新情報を狙う第一標的は $p=7$ の類 4 冪零窓へ移す**(§3.2・§8.7)。

---

## 8.5 【W100-7.1】系 HSP-ODD / HSP-WALL の限定(nilpotent route 限定の記帳)

**正文(以後これを引く)**:
> ### 系 HSP-ODD(v2・nilpotent route 限定)
> $d(N)=1$ の奇・混合 dihedral 窓および壁窓は、**冪零 $K(0,5)$-window を経由する限り** $\mathrm{PENT}_W$ が恒真(検出力ゼロ)。
> **UNKNOWN(この限定の外)**: ① 非冪零 packing($Q$ が完全群を商にもつ場合)② 深さ 5 以上 ③ $p=5$ の affine obstruction ④ 他の cross-frame detector。

**地図の文言**(裁定 408/420 の第二修正 → **便 100 W100-7.1 で再修正**):

| 追認される地図 | 追認されない地図 |
|---|---|
| gentle axioms 内部では **P99-C2-BLIND の範囲で** $c_2$ は独立 detector にならない。既知の cross-frame 候補には **GTPI 型**と **HS norm 型**がある。HS の **現在設計できている LCS/$\mathfrak h_4$ route** は、$d(N)\ge2$・good characteristic・class 4 の**冪零窓**を第一候補とする | ~~「HS Prop 7 の**全経路**が厳密に $d\ge2$、class $\ge4$、characteristic $\ne5$ に限られる」~~ |

⟹ **§7.5 申し送り 3(「HS Prop 7 の道が深さ 4・$d(N)\ge2$・標数 $\ne5$ の窓に限られる」)は、上表の左欄の形(= 現在設計できている route について)に読み替える。**
⟹ **§4 の FV-WALL 凍結維持の判断は不変**(W-2「非冪零 $W$ では検出力の事前見積りが立たない」は、まさに上の UNKNOWN ① と同じ内容であり、Sol の限定と整合する)。充足条件 (T-1)(T-2)(T-3) も不変。

---

## 8.6 【P100-1.2】HS 本走の**発火前チェックリスト**(5 条・全て閉じるまで $N^{(4,7)}$ 本走は未認可)

| # | 条件(Sol P100-1.2 逐条) | 本節での状態 |
|---|---|---|
| **1** | **NW-1 を曖昧な省略記号なしの verbal subgroup として一意に定義し、$N\trianglelefteq B_3$・$N_{F_2}$・$N_{\rm ord}$・$c$ の扱いを紙で固定する** | ★ **本節 §8.7 で履行(紙で閉じた)** — 司令塔検分 + Sol 監査待ち |
| **2** | 最初の素数は **$p=7$ に事前登録**し、$\mathfrak h_4$ の生存と $\nu_4(\mathfrak h_4)\ne0$ を**その有限商で直接確認**する | **未履行**(機械が要る)。**§8.7.7 に事前登録の型を書いた**。これが【HSP-GAP-2】の $p=7$ instance |
| **3** | P100-1.1 の $m=0$ finite dummy family を **exact group element** として作り、hexagon / charming / SURJ / PENT を**別々に**判定する | ★ **構成は §8.7.4 で履行**($\mathrm{Exp}$ を経由しない交換子語)。**4 判定の分離**は §8.3.2 (a)-(d) で分離済 |
| **4** | 探索レーン・full $B_3/N$ hexagon レーン・$K(0,5)/W$ PENT レーンを **helper 非共有**にする | **未履行**(実装時)。§5.3 項目 2 に既記 — 発注仕様に転記すること |
| **5** | **CV-9 判読**まで D3/D4 を cross-checked と呼ばない | **遵守中**(§7.1 の宣言どおり・本節でも格は上げていない) |

> **⟹ 発火は依然として未認可。FV-WALL は凍結維持。**

---

## 8.7 ★★ 条件 1 の履行 — **補題 NW-1 v2(省略記号なしの verbal 窓対)**

> **本節が §5.1 の補題 NW-1(初稿・$N_{F_2}:=\gamma_5(F_2)F_2^{p^e}[\ldots]$ という省略記号つき)を置き換える。**
> **使う外部入力はゼロ**(verbal 部分群・下中心列・Frattini 部分群の標準事実のみ)。**Lazard 対応も Burnside 型の一般論も呼ばない** — 呼ぶ代わりに、次元は**上界を紙で出し、等号は標的商での機械確認(条件 2)へ回す**(【HSP-GAP-2】の処理方針と同じ)。

### 8.7.1 定義 VAR — 変種と verbal 部分群(**省略記号なし**)

> ### 定義 VAR
> 素数 $p$ と $e\ge1$ に対し、**語の集合**
> $$\mathcal W_{4,p^e}:=\bigl\{\,[x_1,x_2,x_3,x_4,x_5]\ ,\ x_1^{\,p^e}\,\bigr\}$$
> (左正規化交換子・重さ 5 のもの 1 個と、$p^e$ 乗 1 個の**ちょうど 2 語**)が定める群の変種を $\mathfrak V_{4,p^e}$(**類 $\le4$ かつ指数 $\mid p^e$**)とし、任意の群 $G$ に対する **verbal 部分群**を
> $$\boxed{\ \mathcal V(G)\ :=\ \mathcal W_{4,p^e}(G)\ =\ \gamma_5(G)\cdot G^{\,p^e},\qquad G^{\,p^e}:=\bigl\langle\,g^{\,p^e}\ :\ g\in G\,\bigr\rangle\ }$$
> と書く(**$\langle\cdot\rangle$ は「$p^e$ 乗全体が生成する部分群」— $p^e$ 乗元の集合ではない**)。

**確認すべき点はこれだけ**(すべて標準・3 行以内):
- **(V0)** $\gamma_5(G)$ は語 $[x_1,\dots,x_5]$ の verbal 部分群である(左正規化重さ 5 交換子の値が生成する部分群 = $\gamma_5(G)$)。ゆえに $\mathcal V(G)$ は語集合 $\mathcal W_{4,p^e}$ の verbal 部分群そのものであり、**省略記号で補うべき語は存在しない**。
- **(V1)** verbal ⟹ **完全不変**(fully invariant): $\phi\in\mathrm{End}(G)$ に対し $\phi(\mathcal V(G))\subseteq\mathcal V(G)$。
- **(V2)** $G/\mathcal V(G)$ は $G$ の $\mathfrak V_{4,p^e}$ における**最大商**。
- **(V3)** 準同型 $\phi:G\to H$ に対し $\phi(\mathcal V(G))=\mathcal V(\phi(G))\subseteq\mathcal V(H)$。
- **(V4)** $H\trianglelefteq G$ かつ $K$ が $H$ で完全不変 ⟹ $K\trianglelefteq G$($g$ による共役は $H$ の自己同型に制限されるから)。

**以後 $e=1$ を事前登録する**($p\ge7$、指数 $p$)。$\mathcal V:=\mathcal V_{4,p}$、$\mathcal V(G)=\gamma_5(G)G^{\,p}$。$e\ge2$ 版は同じ定義で動くが、本走の宇宙には入れない(**後から変えない**)。

### 8.7.2 ★ 補題 NW-1a — **直積の中での明示計算**(罠 #5 を仮定でなく計算で回避)

$PB_3=F_2\times\langle c\rangle$($F_2=\langle x,y\rangle$、$c$ = full twist、$\langle c\rangle=Z(B_3)\cong\mathbb Z$)。

> ### 補題 NW-1a
> $$\boxed{\ \mathcal V(PB_3)\ =\ \mathcal V(F_2)\times\langle c^{\,p}\rangle\ =\ \bigl(\gamma_5(F_2)F_2^{\,p}\bigr)\times\langle c^{\,p}\rangle\ }$$

**証明.** (i) $c$ は中心ゆえ $\gamma_k(F_2\times\langle c\rangle)=\gamma_k(F_2)$($k\ge2$)、とくに $\gamma_5(PB_3)=\gamma_5(F_2)$。
(ii) $w\in F_2$、$k\in\mathbb Z$ に対し $c$ が中心ゆえ $(wc^k)^{\,p}=w^{\,p}c^{\,kp}$。ゆえに $p$ 乗元の**値の集合**は $\{w^{\,p}c^{\,kp}\}$ で、これが生成する部分群は $k=0$ から $F_2^{\,p}$ を、$w=1,k=1$ から $c^{\,p}$ を含み、逆に各値は $F_2^{\,p}\langle c^p\rangle$ に入る。よって $PB_3^{\,p}=F_2^{\,p}\times\langle c^{\,p}\rangle$。
(iii) 積: $\gamma_5(F_2)\cdot\bigl(F_2^{\,p}\times\langle c^{\,p}\rangle\bigr)=\bigl(\gamma_5(F_2)F_2^{\,p}\bigr)\times\langle c^{\,p}\rangle$。∎

> ★ **これが【HSP-GAP-1】(c) の正しい処理である。** 初稿は「$N:=\mathcal V(PB_3)\cdot\langle\langle c\rangle\rangle$ を取り $N_{F_2}$ が変わらないことを **Dedekind で確認**(罠 #5)」と書いたが、**Dedekind も分裂の仮定も要らない** — verbal 部分群が直積分解に対して**箱型($A\times B$ の形)**になることを直接計算すればよい。**「分裂を仮定しない」は、分裂を使わない計算を実際に書くことで満たされる。**

### 8.7.3 ★ 定義 NW($p$)と補題 NW-1b — 窓対の確定

> ### 定義 NW($p$)(**事前登録する窓対**・$p\ge7$、$e=1$)
> $$\boxed{\
> \begin{aligned}
> \mathbf N&:=\mathcal V(PB_3)\cdot Z(B_3)\;=\;\mathcal V(F_2)\times\langle c\rangle &&(\textbf{主標的}\ —\ c\in\mathbf N)\\
> \mathbf N_0&:=\mathcal V(PB_3)\;=\;\mathcal V(F_2)\times\langle c^{\,p}\rangle &&(\textbf{control}\ —\ c\notin\mathbf N_0)\\
> N_{F_2}&:=\mathcal V(F_2)=\gamma_5(F_2)F_2^{\,p} &&(\textbf{両者に共通})\\
> W&:=\mathcal V\bigl(K(0,5)\bigr)=\gamma_5(K(0,5))\,K(0,5)^{\,p} &&(\textbf{pentagon 側の窓})
> \end{aligned}\ }$$
> $P:=F_2/N_{F_2}$、$Q:=K(0,5)/W$。**記号 $N^{(4,p)}$ は以後 $\mathbf N$ を指す。**

> ### 補題 NW-1b(**$N\trianglelefteq B_3$・$N_{F_2}$・$N_{\rm ord}$・$c$ の 4 点を紙で固定**)
> **(1)【$N\trianglelefteq B_3$】** $\mathbf N,\mathbf N_0\in\mathrm{NFI}_{PB_3}(B_3)$。
> **(2)【$N_{F_2}$】** $\mathbf N\cap F_2=\mathbf N_0\cap F_2=\mathcal V(F_2)$。**箱型ゆえ Dedekind も分裂仮定も不要。**
> **(3)【商】** $PB_3/\mathbf N\cong P$、$PB_3/\mathbf N_0\cong P\times C_p$。$P$ は**類 $\le4$・指数 $p$ の有限 $p$ 群**で $\lvert P\rvert\le p^{8}$、$\lvert[P,P]\rvert\le p^{6}$、$P^{\rm ab}\cong C_p^{\,2}$。
> **(4)【$N_{\rm ord}$】** $\boxed{N_{\rm ord}=p}$(両窓)。ゆえに $\mathcal X_{\mathbf N}=\{m\bmod p:\ 2m+1\not\equiv0\}$、$\lvert\mathcal X_{\mathbf N}\rvert=p-1$、**$m=0\in\mathcal X_{\mathbf N}$**。
> **(5)【$c$】** $\mathbf N$ では $\bar c=1$ ⟹ **許容対象**(簡約 hexagon (3.10)(3.11) の商上評価の近道が使える)。$\mathbf N_0$ では $\mathrm{ord}(\bar c)=p$ ⟹ **近道は壊れる**ので **full $B_3/N$ 上の (3.3)(3.4) で $c^m$ 項と $T(c)=c^{2m+1}$ を検査**する(較正スイート項目 7 の型)。
> **(6)【$W$】** $W$ は $K(0,5)$ で完全不変 ⟹ **(W-b) $\rho(W)=W$ 自動**。$j(N_{F_2})\subseteq W$ ⟹ **(W-c) 自動**。$[K(0,5):W]\le p^{40}<\infty$ ⟹ **(W-a) 自動**。$\bar\rho^5=1$、$\bar\rho\ne1$。

**証明.**
**(1)** $\mathcal V(PB_3)$ は $PB_3$ で完全不変(V1)、$PB_3\trianglelefteq B_3$ ゆえ (V4) より $B_3$ で正規。$Z(B_3)=\langle c\rangle\trianglelefteq B_3$。正規部分群の積は正規。両者とも $PB_3$ に含まれる。有限指数は (3)。
**(2)** 補題 NW-1a より $\mathbf N_0=\mathcal V(F_2)\times\langle c^p\rangle$、$\mathbf N=\mathbf N_0\langle c\rangle=\mathcal V(F_2)\times\langle c\rangle$。直積 $F_2\times\langle c\rangle$ の中の**箱型部分群 $A\times B$ は $(A\times B)\cap(F_2\times1)=A\times1$** を満たす。ゆえに交わりは $\mathcal V(F_2)$。
**(3)** 商は箱型から直ちに従う。$P=F_2/\gamma_5(F_2)F_2^{\,p}$ は指数 $\mid p$ で類 $\le4$。有限性と上界: $\gamma_k(P)/\gamma_{k+1}(P)$ は重さ $k$ の基本交換子の像で生成され、$P^{\,p}=1$ より初等アーベル、したがって $\mathbb F_p$-空間として次元 $\le$ Witt 数 $W(2,k)$。$W(2,1..4)=(2,1,2,3)$ より $\lvert P\rvert\le p^{2+1+2+3}=p^8$、$\lvert[P,P]\rvert\le p^{1+2+3}=p^6$。$P^{\rm ab}=F_2^{\rm ab}/p\,F_2^{\rm ab}\cong C_p^2$。
**(4)** $N_{\rm ord}=\mathrm{lcm}\bigl(\mathrm{ord}(\bar x),\mathrm{ord}(\bar y),\mathrm{ord}(\bar c)\bigr)$(定義ノート (3.1))。$P^{\rm ab}\cong C_p^2$ ゆえ $\bar x,\bar y\ne1$、指数 $p$ ゆえ位数はちょうど $p$。$\mathbf N$ では $\mathrm{ord}(\bar c)=1$、$\mathbf N_0$ では $\langle c\rangle/\langle c^p\rangle\cong C_p$ ゆえ $p$。いずれも lcm $=p$。$m=0$ は $2m+1=1$ ゆえ $\mathcal X$ の元。
**(5)** 定義から。近道の可否は定義ノート §2 の実装注(「$\theta/\tau$ を商上の準同型として評価する近道は $c\in N$ に依存」)そのまま。
**(6)** (V1)(V3) と (3) と同じ次元勘定($\mathrm{gr}_k(K(0,5))$ の階数 $5,4,10,21$・§2 の検算)。$\bar\rho\ne1$ は $\mathrm{gr}_1(Q)=Q^{\rm ab}$ 上で $\bar T_1\ne\bar T_4$ から。∎

> ### ★ 【HSP-GAP-1】の状態更新
> **CLOSED(紙)。** (c)($c$ の扱い)は補題 NW-1a + NW-1b (2)(5) で、(d)($N_{\rm ord}$)は NW-1b (4) で閉じた。**罠 #5 は「分裂を仮定しない計算」を実際に書くことで回避した。**
> 残る機械項は **$\lvert P\rvert=p^8$ の等号**(= $\mathrm{gr}_k(F_2)\otimes\mathbb F_p$ の生存)であり、これは **【HSP-GAP-2】の $p=7$ instance = 発火条件 2** に一本化する(§8.7.7)。上界 $\le p^8$ だけは紙で確定している。

### 8.7.4 ★ 定義 DUM-FIN — dummy を **$\mathrm{Exp}$ なしの有限群元**として構成(W100-1.3 への直接回答)

$P$ は類 $\le4$ ゆえ $\gamma_5(P)=1$、したがって $\gamma_4(P)\subseteq Z(P)$。さらに $P^{\,p}=1$ ゆえ $\gamma_4(P)$ は**初等アーベル**である。$\gamma_5(P)=1$ より重さ 4 の交換子写像 $P^{\times4}\to\gamma_4(P)$ は**多重線型**で、$\gamma_4(P)=\gamma_4(P)/\gamma_5(P)=\mathrm{gr}_4(P)$。

> ### 定義 DUM-FIN
> $$\boxed{\ h_4\ :=\ \bigl[[[x,y],x],x\bigr]\ \cdot\ \bigl[[[x,y],x],y\bigr]^{4}\ \cdot\ \bigl[[[x,y],y],y\bigr]\ \in\ \gamma_4(P)\ }$$
> $$f_t:=h_4^{\,t}\quad(t=0,1,\dots,p-1).$$

- **これは群の交換子語であり、$\exp$/BCH/Lazard 対応を一切経由しない。** 「記号だけでは離散有限群の元ではない」(W100-1.3)は解消される。
- $\gamma_4(P)$ が初等アーベルで交換子写像が多重線型ゆえ、$h_4$ は **$\mathfrak h_4=v_1+4v_2+v_3\in\mathrm{gr}_4(F_2)$ の $\bmod\,p$ 像そのもの**である(同一視ではなく、$\gamma_4(P)=\mathrm{gr}_4(P)$ という等号による)。
- **F100-4.3 の用語規約に従う**: $\mathfrak h_4$ は **Lie 元**(bracket convention・係数環・$\bmod\,p$ 還元を併記)、$h_4$ は**群元**。**同一視しない**(規約台帳 §1.3.10 に登録済)。
- **Hall 関係** $[[[x,y],y],x]=[[[x,y],x],y]$ は類 4 で exact(§6 の検算で確認済)。

### 8.7.5 補題 DUM-HEX(hexagon が **exact に**成立すること)

> ### 補題 DUM-HEX
> $m=0$、$f_t=h_4^{\,t}$ に対し、簡約 hexagon **(3.10) $f\theta(f)=1$ と (3.11) $\tau^2(f)\tau(f)f=1$ はいずれも $P$ の中の等式として exact に成立する**(「次数 4 の斉次解」ではなく)。

**証明.** $N_{F_2}=\mathcal V(F_2)$ は完全不変ゆえ $\theta$($x\leftrightarrow y$)と $\tau$($x\mapsto y\mapsto z\mapsto x$、$z=(xy)^{-1}$)は $P$ の自己同型に降りる。両者は $\gamma_4(P)$ を保ち、$\gamma_4(P)=\mathrm{gr}_4(P)$ 上では**次数付き作用 $\theta_*,\tau_*$ の $\bmod\,p$ 還元**そのものである。$\gamma_4(P)$ は可換ゆえ積は座標の和。
- **(3.10)**: $\theta_*(\mathfrak h_4)=\theta_*(v_1+4v_2+v_3)=-v_3-4v_2-v_1=-\mathfrak h_4$($\theta_*v_1=-v_3$、$\theta_*v_3=-v_1$、$\theta_*v_2=-v_2$)。ゆえに $f_t\theta(f_t)=h_4^{\,t}h_4^{-t}=1$。
- **(3.11)**($m=0$ ゆえ $y^m=1$): $(1+\tau_*+\tau_*^2)\mathfrak h_4=(4\alpha-\beta)(v_1+v_2+v_3)$ で $(\alpha,\beta,\gamma)=(1,4,1)$、よって $=0$(§2.3 (a) の手計算)。ゆえに $\tau^2(f_t)\tau(f_t)f_t=1$。∎

> **注**: exact になるのは $f_t$ が**窓の最上層 $\gamma_4(P)$**(中心・初等アーベル)に居るからである(§8.3.2 の ★)。深さ 3 では成立しない(§8.3.3)。
> **注 2**: 主標的 $\mathbf N$ は $c\in\mathbf N$ ゆえ簡約形 (3.10)(3.11) を使ってよい(補題 NW-1b (5))。**control $\mathbf N_0$ では full (3.3)(3.4) を使うこと。**

> ### ★ 精確化 PREC-1(§2.3 (a) の一文の読み方 — **当方の検算で捕獲**)
> §2.3 (a) の証明は「(3.10) が $\alpha=\gamma$、**(3.11) が $(4\alpha-\beta)(v_1+v_2+v_3)=0$**」と書いている。**この 2 つは順に適用されており、その読みでは正しい**が、後半を**単独の恒等式として引用すると誤り**である。検算(§8.11)が与えた**一般形**は
> $$\bigl(1+\tau_*+\tau_*^2\bigr)\bigl(\alpha v_1+\beta v_2+\gamma v_3\bigr)\;=\;\boxed{(2\alpha-\beta+2\gamma)}\,(v_1+v_2+v_3)$$
> であり(像は確かに階数 1・$\mathbb Q(v_1+v_2+v_3)$)、**$(4\alpha-\beta)$ になるのは (3.10)-locus $\alpha=\gamma$ に制限したときだけ**である。
> - 解空間は $\{\alpha=\gamma\}\cap\{2\alpha-\beta+2\gamma=0\}=\mathbb Q\,(1,4,1)=\mathbb Q\,\mathfrak h_4$ ⟹ **定理 D4-POWER (a)(1 次元)は不変・独立に再確認された。**
> - **以後 (3.11) の深さ 4 成分を単独で引くときは $(2\alpha-\beta+2\gamma)$ を書くこと。**

### 8.7.6 SURJ の自動性 — **既在の系 H8′ による**(★ 新規ではない・grep 済)

> ### 系 H8′(既在・`docs/week3-狩場計画_v2.md` §2.1)
> $P$ が $p$ 群、$\bar f\in[P,P]\subseteq\Phi(P)$、$\gcd(2m+1,p)=1$ ならば **全射性は自動**(Frattini 論法)。

窓 $\mathbf N$/$\mathbf N_0$ では $P$($\times C_p$)は $p$ 群、charming は $\bar f\in[P,P]$、$m\in\mathcal X_{\mathbf N}$ は $\gcd(2m+1,p)=1$ を意味する。$\Phi(P)=[P,P]P^{\,p}=[P,P]$(指数 $p$)。ゆえに **$\mathcal X_{\mathbf N}$ の全 $m$・全 charming $\bar f$ について SURJ は自動**(Prop 3.6 により $T_{m,f}$・$T^{PB_3}$・$T^{F_2}$ のどれで判定してもよい)。

> ### ★ Sol P100-1.1 の理由づけへの補正(結論は不変・理由を差し替え)
> Sol は「$\gamma_4$ は中心なので $T_{0,f_t}$ は**恒等写像**となり SURJ は自動」と書いたが、**$T_{0,f_t}$ は一般に恒等写像ではない**: $T_{0,f}(\sigma_2)=f^{-1}\sigma_2f$ であり、$f_t$ は $\gamma_4(P)$ の中心元でも **$\sigma_2$ とは可換とは限らない**($\gamma_4(P)$ は $PB_3/N$ の中心だが $B_3/N$ の中心ではない。実際 $\theta_*(\mathfrak h_4)=-\mathfrak h_4\ne\mathfrak h_4$($p\ne2$)ゆえ $S_3$ 側の作用は $h_4$ を動かす)。
> **結論(SURJ 自動)は正しく、かつより強い形で既に工房にある**(系 H8′ — $m=0$ に限らず $\mathcal X_{\mathbf N}$ 全体で成立)。**理由づけを系 H8′ に差し替えて記帳する。**
> ⟹ **副次的帰結**: この窓族では **SURJ は篩として識別力ゼロ**(全 charming 候補が通る)。判定の実体は hexagon と PENT だけである。**発注仕様にこの一行を入れること**(識別力ゼロの検査を「通った」と報告させない)。

### 8.7.7 発火条件 2 の事前登録の型(IF-FIRST・**測る前に凍結**)

> **本項は実装前の凍結対象。値をコードに書かない。**

| # | 事前登録項目 | 型 |
|---|---|---|
| **NW-P1** | $p=7$、$e=1$。窓対は定義 NW(7) の $\mathbf N$(主)と $\mathbf N_0$(control)**のみ**。後から $p$ も $e$ も変えない | 宇宙の事前登録 |
| **NW-P2** | $\lvert P\rvert=7^8=5{,}764{,}801$、$\lvert[P,P]\rvert=7^6=117{,}649$、$N_{\rm ord}=7$、$\lvert\mathcal X_{\mathbf N}\rvert=6$ | **予言**(紙は $\le$ のみ。等号は機械が決める) |
| **NW-P3** | $\dim_{\mathbb F_7}\gamma_4(P)=3$ かつ $h_4\ne1$ in $\gamma_4(P)$(= **$\mathfrak h_4$ の生存**) | 予言(**【HSP-GAP-2】の $p=7$ instance**) |
| **NW-P4** | $\lvert Q\rvert=7^{40}$、$\dim_{\mathbb F_7}\gamma_4(Q)=21$ | 予言(pc 群で扱う。置換表現では不可) |
| **NW-P5** ★ | $\nu_4(j\mathfrak h_4)\ne0$ in $\gamma_4(Q)$ — **標的商での直接確認** | ★ **発火条件 2 の本体**。これが確認できて初めて定理 DUM-1/p が発火する |
| **NW-P6** | 定理 DUM-1/p の帰結: $p=7$ の dummy family 7 元のうち **PENT PASS はちょうど 1 個($t=0$)** | 予言(NW-P5 相対) |
| **NW-P7** | control($p=5$・同じ family): **7 元中 7 元 = 全 PASS** ではなく **5 元中 5 元 = 全 PASS**($\nu_4(\mathfrak h_4)\equiv0\bmod5$) | ★ **family 限定 control**(§8.3.4・全候補 control ではない) |
| **NW-P8** | control($\mathbf N_0$・$c\notin N$): full (3.3)(3.4) で $c^m$ 項が実際に効くこと($m\ne0$ の $m$ で hexagon の判定が $\mathbf N$ と食い違う $m$ が存在する) | 較正スイート項目 7 の型 |

**停止規則(§7.4 の S-1〜S-5 に追加)**:
- **S-6**: **NW-P3 または NW-P5 が偽なら $p=7$ 本走を止める**(標的の前提が崩れる)。$p=11,13$ へ移す判断は司令塔。
- **S-7**: NW-P2 の等号が破れた(= $\lvert P\rvert<7^8$)場合、**窓の定義を変えずに**次元の実測値で全予言を書き直す(**宇宙を後から変えない**)。

### 8.7.8 §5.1 との差分・依存の会計

| 初稿 §5.1 | v2(本節) |
|---|---|
| $N_{F_2}:=\gamma_5(F_2)F_2^{p^e}[\ldots]$(**省略記号**) | ★ $N_{F_2}=\gamma_5(F_2)F_2^{\,p}$(**2 語の verbal・省略記号なし**) |
| 「$PB_3$ の対応する verbal 部分群の $B_3$ 内での**適合化**」(未定義語) | ★ $\mathbf N=\mathcal V(PB_3)Z(B_3)$、$\mathbf N_0=\mathcal V(PB_3)$(**式で定義**) |
| $c\in N$ を「取れる」(未検証)/ **Dedekind で確認**(罠 #5) | ★ **箱型計算**(補題 NW-1a)で $c$ の両扱いを構成・Dedekind 不要 |
| $N_{\rm ord}=p^e$(未検証) | ★ $N_{\rm ord}=p$(**証明つき**・$e=1$ 登録) |
| dummy $=\exp(t\mathfrak h_4)$(記号) | ★ $f_t=h_4^{\,t}$(**交換子語 = 有限群元**) |
| SURJ の根拠なし | ★ **既在の系 H8′**(識別力ゼロであることも明記) |

**新規の未解決依存: なし。** U-10 は使わない(D-8 不変)。外部文献ゼロ。**Lazard 対応・制限 Burnside の一般論を呼んでいない**(次元の等号を機械へ回したため)— これは【文献要請】を出さずに済ませた処理であり、**呼びたくなったら NW-P2/NW-P3 の実測が先**である。

---

## 8.8 格付けの更新(§7.1 への差分のみ)

| 主張 | 便 100 後の格 |
|---|---|
| HS (III) の **PENT-NORM 書換え** | **paper-proof**(Sol F100-1.1 PASS)。**Prop 7 本体とは呼称分離**(§8.1) |
| HSP-WD / HSP-SOUND | **paper-proof**(F100-1.3 PASS) |
| 補題 CENT-FREE | **paper-proof(限定版)**(F100-1.4 PASS)— **pentagon 恒等式判定のみ**。有限 PASS は $PB_4$ の恒等式を証明しない。完成群で引くときは中心拡大の profinite exactness/closure の一行を併記 |
| **定理 D2-BLIND** | **paper-proof**(F100-1.5 PASS・整数係数ゆえ torsion-free 仮定不要) |
| **系 D2-C2** | **paper-proof(弱化後の正文で)**(§8.2) |
| 定理 D3-BLIND / D4-POWER | **有理次数付き・有限線型計算 candidate**(F100-1.6)。**cross-checked ではない** |
| **系 D4-PRED** | ★ **撤回**(§8.3.1 R-1) |
| ★ **定理 DUM-1/p** | **paper-proof candidate**(**NW-P5 相対**・Sol 未監査) |
| ★ **補題 NW-1a / NW-1b / DUM-HEX** | **paper-proof candidate**(**Sol 未監査**・外部入力ゼロ) |
| 系 H8′ の適用(SURJ 自動) | **既在の系の適用**(新規ではない) |
| 命題 HSP-COLLAPSE | **paper-proof**(F100-1.7 PASS) |
| 系 HSP-ODD / HSP-WALL | **paper-proof(nilpotent route 限定)**(§8.5) |
| $K_\pi$ の位置づけ | ★ **「情報ゼロ」撤回 → 安価な向き較正**(§8.4) |

**verified(Lean)は依然 0 件。cross-checked も 0 件**(CV-9 主検問未実施)。

## 8.9 Sol への監査点(便 101・優先順)

- **監査点 A′(最優先)**: **補題 NW-1a**($\mathcal V(F_2\times\langle c\rangle)=\mathcal V(F_2)\times\langle c^p\rangle$)と **NW-1b (2)**(箱型ゆえ $\mathbf N\cap F_2=\mathcal V(F_2)$)。**罠 #5 を「分裂を仮定しない計算」で回避したという主張**が成立しているか。
- **監査点 B′**: **NW-1b (4)** $N_{\rm ord}=p$(定義ノート (3.1) の lcm 定義に照らして)。とくに control $\mathbf N_0$ でも $p$ になること。
- **監査点 C′**: **補題 DUM-HEX** — hexagon が「次数 4 の斉次解」ではなく **$P$ の中の exact な等式**として成立するという主張(最上層に居ることの帰結)。
- **監査点 D′**: **§8.7.6 の補正** — 「$T_{0,f_t}$ は恒等写像」は偽だが SURJ は系 H8′ で自動、という差し替えが正しいか。**および「SURJ はこの窓族で識別力ゼロ」という帰結**。
- **監査点 E′**: **§8.3.3 の自己捕獲** — $h_3$ 方向は有限窓で exact な hexagon 解でも exact な PENT PASS でもなく、$\gamma_4$ 剰余が残る(代表元依存)。A-HSP-2 の弱化は妥当か。
- **監査点 F′**: **§8.7.7 の事前登録**が「宇宙を後から変えない」規律に照らして十分に閉じているか(とくに S-7 の扱い)。

## 8.10 司令塔への申し送り

1. ★ **発火条件 1 は履行した(紙)。残るのは条件 2(機械)・条件 3 の分離判定(履行済)・条件 4(発注仕様)・条件 5(CV-9)。** 条件 2 は $p=7$ の pc 群計算であり、**$\lvert Q\rvert=7^{40}$ は置換群では不可能・polycyclic なら軽い**(§3.2)。棚: `anupq` / `autpgrp` / `polycyclic`。
2. ★ **【HSP-GAP-1】は CLOSED(紙)。** 【HSP-GAP-2】は $p=7$ instance = 発火条件 2 に一本化した。【HSP-GAP-3】(非冪零窓の事前見積り法)と【文献要請 HSP-L1】は**不変**(W100-1.5 が $K_\pi$ を「判定不能」に戻したことで、むしろ**重要度が上がった**)。
3. **地図の該当行**: §8.5 の表(追認される地図 / されない地図)をそのまま反映されたい。裁定 408/420 の第二修正は本節で**再修正**された。
4. **規約台帳**: $\mathfrak h_3/\mathfrak h_4$ の用語登録(F100-4.3)は台帳 v1.5 §1.3.10 で履行。**既存 script の `psi4`/`sigma3` は次版で改名**(§6 の 5 本)— 実装係への申し送り。
5. **識別力ゼロの検査**: §8.7.6 の副次的帰結(SURJ がこの窓族で識別力ゼロ)は、CV-9-5 の「識別力を持つ dummy fixture」要件と同じ型の問題である。**発注仕様に「SURJ の PASS を証拠として数えない」を明記**されたい。
6. ★ **精確化 PREC-1**(§8.7.5): (3.11) の深さ 4 成分の一般形は $(2\alpha-\beta+2\gamma)$ であり、$(4\alpha-\beta)$ は (3.10)-locus 上の形である。**定理 D4-POWER (a) の結論は不変**(むしろ独立に再確認された)。**§2.3 (a) の本文は不改変**(順に適用しているので誤りではない)。

## 8.11 検算(§8 で新たに走らせたもの — 1 本)

**収蔵**: `search/probe/hsp7_v1/hs_prop7_dumhex_check.py`
**SHA-256**: `7b1c7e067a13a24de2200b60d226a8c58fe7ada44567753365827629fad8df5f`
**python 単系統 / 整数・厳密有理数のみ / 14 検査 FAILS = 0 / $K^{(5)}$ 非接触・窓の測定なし**

| # | 検査 | 使う場所 |
|---|---|---|
| 1–2 | $\tau_*^3=\mathrm{id}$、$\theta_*^2=\mathrm{id}$(自己検査) | 実装の健全性 |
| 3 | **Hall 関係** $[[[x,y],y],x]=v_2$ | 定義 DUM-FIN |
| 4 | $v_1,v_2,v_3$ が一次独立 | §2.3 の基底 |
| 5–7 | ★ $\theta_*(v_1)=-v_3$、$\theta_*(v_2)=-v_2$、$\theta_*(v_3)=-v_1$ | **補題 DUM-HEX (3.10)** |
| 8 | ★ **$\theta_*(\mathfrak h_4)=-\mathfrak h_4$** | **補題 DUM-HEX (3.10)** |
| 9 | ★ $\theta_*(\mathfrak h_3)=-\mathfrak h_3$ | §8.3.3(自己捕獲の前提) |
| 10 | ★ **$(1+\tau_*+\tau_*^2)(\mathfrak h_4)=0$** | **補題 DUM-HEX (3.11)** |
| 11 | ★ 一般形 $(1+\tau_*+\tau_*^2)(\alpha,\beta,\gamma)=(2\alpha-\beta+2\gamma)(v_1{+}v_2{+}v_3)$(像は階数 1) | **精確化 PREC-1** |
| 12 | $\alpha=\gamma$ 上で $(2\alpha-\beta+2\gamma)=(4\alpha-\beta)$ | PREC-1(§2.3 との整合) |
| 13 | ★ **hexagon 深さ 4 解空間 $=\mathbb Z(1,4,1)$ のみ** | **定理 D4-POWER (a) の独立再確認** |
| 14 | (3.10) の深さ 4 条件 $\iff\alpha=\gamma$ | §2.3 (a) |

**実装の独立性**: §6 の 5 本(外積モデル / テンソルモデル / 剰余算術)とは別に、**テンソル代数上の整数係数直接計算 + $\tau_*$ を $x\mapsto y,\ y\mapsto -x-y$ から独立に構成**している。ただし **起草者が書いた single lane** であり、**cross-checked ではない**(CV-9 未実施)。**Lean 検証でもない。**
