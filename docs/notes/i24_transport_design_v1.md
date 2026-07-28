# I-24 relabel transport capsule — 枝値付け替えの型付き輸送則の設計 **v1**

**状態札: candidate(裁定前・未 commit・紙上 + 使い捨て検算スクリプト)**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-29
設問: 司令塔委嘱(便 79 検収の修理波・裁定 170)/ **F79-4.1**(I-24 の「同一 dessin ⟹ $j$ 盲目」は現証明書からは出ない)+ **P79-E**(relabel transport capsule の 7 欄要求)の数学的中身の設計
依拠:
- `sol/sol_reply_79_math6.md` **F79-4.1 / P79-E / F79-3.2(補題 INV の承認)**
- `search/certs/i24_u3_recheck_20260729.json`(schema `i24-u3-recheck/v1`・GAP 一レーン)
- `docs/notes/oddH_full_proof_v1.md`(補題 A(1)–(4)・命題 ODD-H (1.2)(1.9)(1.11)・**命題 ODD-P**(ordered passport 閉形式)・§5.2 正準生成元)
- `docs/notes/t63_reconnaissance_v1.md` §1–2(A1–A7・(T) = (2.3)・$[u]_M$ の uniformizer/モデル非依存 = BFC 補題 **B-5(ii-loc)(ii-win)**)
- `docs/notes/i23_cascade_lemma_v1.md` §6.2(**補題 INV**)/ `docs/notes/i17_check_v1.md` §5(caveat C1・C1′)
- `docs/manifest_k5_appendixA_v1.md` §1.1(**分岐辞書** $\sigma_0,\sigma_1,\sigma_\infty\leftrightarrow X,Y,Z$)・§2(K3 regression: モデル・cusp・uniformizer・$u=-4$・covariance control $u'=-256/729$)
- `docs/week4-K3飽和_opus_v3.md` §3(**便 27 P8 の Möbius の数え方の訂正**・【GAP-20b】の閉鎖射程 = `ordered-passport-preserving`)
- `sol/sol_reply_79_math6.md` **F79-5.1**($\operatorname{Ad}(\Delta):x\mapsto y,y\mapsto x$ / $\operatorname{Ad}(\delta):x\mapsto y,y\mapsto zc$ の承認)
- 外部文献なし。使う事実は **Möbius 群の 3 点推移性**・**局所展開**・**$\mu_{4n}\subset F_n$** のみ。

> ## 封印遵守
> **封印 3 量($u_9/a_9$ の値・$c$ の平方類・$\hat c_\mu$)に一切触れていない。** 触れた $u$ の値は**公開値 $u_3=-4$ と公開の covariance control $u_3'=-256/729$ のみ**(いずれも `manifest_k5_appendixA_v1.md` §2 の登録値)。$K^{(5)}$ は blind 進行中につき適用先から除外。
> ⚠ **§7.4 の予言 I24-P1($j=3$ 窓での $u$ の値)は測定前の予言**であり、**凍結(pre-registration)手続きの対象**として扱うことを要請する。

---

## 1. 結論 — 委嘱の設問への明言

**設問**: 「変換因子 $-1$ が $i\in F_m$ により平方 ⟹ **SQ 述語(平方類)は relabel 不変**が救えるか。救えるなら『$u$ そのものは $j$ 依存でも $[u]_2$ は $j$ 盲目』という弱いが十分な形で C1′ を再閉鎖できるか。」

| # | 問い | 答 |
|---|---|---|
| **(a)** | 変換因子は本当に $-1$ か | **YES・証明**(補題 TR)。$1\leftrightarrow\infty$ 交換で $0$ を固定する Möbius は $\mu(t)=t/(t-1)$ **ただ一つ**で、$\mu'(0)=-1$。cusp は動かないので局所輸送則が閉じる |
| **(b)** | SQ 述語($[u]_2$)は relabel 不変か | **YES・証明**(補題 SQ-INV)。しかも**要求より強い**: $-1=\zeta_{4n}^{2n}\in(F_n^\times)^{2n}$ なので **$[u]_{2n}$ 自体が不変**。ゆえに $a_n$、$\operatorname{ord}(a_n)$、$\mathcal P_{n,p}$、`FULL_p_DEPTH`、$[u]_2$ の**すべてが $j$ 盲目**。平方類まで落とす必要すらない |
| **(c)** | それは $n=3$ 限定か | **NO・全奇数 $n$ で成立**(定理 J-BLIND)。群論側は $\nu=\operatorname{Ad}(\Delta\delta)$ という **$B_3$ 由来の自己同型**で族化でき、$\nu(H_{3,\alpha,\beta})=H_{2,-\alpha,\beta-1}$(**定理 W-REL**)。$n=3$ の $S_6$ witness はその 1 標本 |
| **(d)** | **これで C1′ は再閉鎖されるか** | **NO。届かない。** C1′ の**生きている曖昧性は $j$ ではなく $[\alpha]$** である。命題 ODD-P(ordered passport)は既に $j$ と「$\alpha$ が単元」を判別しており、残るのは $j=2$ 行の $\varphi(n)/2$ 個の単元類 — 本稿の機構はそこに一切触れない。**$n=3$ では $\varphi(3)/2=1$ なので C1 は閉じる**が、$n\ge5$($q=7$ なら 3 類)では閉じない |

**要約**: **$j$-盲目性は証明できた(しかも強い形で・全奇数 $n$ で)。しかし C1′ の再閉鎖には至らない** — I-24 の予想 2(述語の共役不変性)のうち**$j$ 方向は閉じ、$\alpha$ 方向(予想 1 = $\alpha$ 軌道予想)は依然として開いている**。

---

## 2. F79-4.1 の受諾 — 何が壊れていたか

証明書 `i24_u3_recheck_20260729.json` が示したのは次の 2 点である。

* `h2fun_h3fun_p3_conjugate: false` — $H_{2,1,0}$ と $H_{3,1,0}$ は $G_3$ 内で共役でない。
* `h1_XY_to_XZ_holds: true`, `h1_witness_g: "[5,1,4,3,6,2]"` — 独立生成対 $(X,Y)|_{H_{2,1,0}}$ と $(X,Z)|_{H_{3,1,0}}$ は $S_6$ 内で**同時共役**。

**Sol の指摘(受諾)**: 後者は branch label $1\leftrightarrow\infty$ を交換する $S_3$-relabeling であって、**標識付き dessin の同値ではない**。したがって

> 同一 dessin の別表示 $\Longrightarrow u$ または SQ 述語は $j$ 盲目

は現証明書からは出ない。**証明書 §5 の `verdict` 欄 `"u3_reproduction_status": "IDENTITY_SAME_X_CUSP_VIA_H1_WITNESS"` は誤った読み**であり、正しくは `"RELABEL_(1,inf)_TRANSPORT_FACTOR_-1"` である(§8 の schema で欄ごと差し替える)。

**修理の骨格**: 「同一 dessin」を主張するのをやめ、**別 dessin の間の輸送則を型付きで書く**。輸送則が「$[u]_M$ を保つ」ことを証明できれば、$j$ 盲目性は**同一性を経由せずに**得られる。以下がその設計である。

---

## 3. 幾何の骨格 — 枝値の $S_3$ と基底 Möbius 変換

### 3.1 分岐辞書(登録済み・本稿の前件 (R1))

$$\boxed{\ x\ \leftrightarrow\ \lambda=0,\qquad y\ \leftrightarrow\ \lambda=1,\qquad z\ \leftrightarrow\ \lambda=\infty\ }$$
($\sigma_0=\bar x$, $\sigma_1=\bar y$, $\sigma_\infty=\bar z$ — `manifest_k5_appendixA_v1.md` §1.1 の `perm_triple` 規約。K3 側も §2 の $\bar x,\bar y,\bar z\leftrightarrow\sigma_0,\sigma_1,\sigma_\infty$ で同じ)

### 3.2 relabel の定義と passport への効き

$\lambda:W\to\mathbf P^1$ を Belyi 写像、$\mu\in\operatorname{PGL}_2$ を $\mu(\{0,1,\infty\})=\{0,1,\infty\}$ なる Möbius 変換とする。**relabel された写像**を
$$\lambda^{\mu}:=\mu\circ\lambda$$
と定める。$\lambda^\mu$ の枝値 $v$ でのモノドロミーは $\lambda$ の $\mu^{-1}(v)$ でのそれ、すなわち
$$\operatorname{type}_{\lambda^\mu}=\operatorname{type}_{\lambda}\circ\mu^{-1},\qquad
\lambda^{\mu,-1}(0)=\lambda^{-1}(\mu^{-1}(0)).$$

> **★ 型の分岐点(P79-E の心臓)**: **$u$ は「$\lambda$ の $0$ の上の全分岐点での主係数」**である。したがって relabel が $u$ を輸送するかどうかは、**$\mu^{-1}(0)$ が何か**で完全に決まる。

### 3.3 6 つの relabel の完全分類($H_{2,\alpha,\beta}$ 窓・ordered passport $(2n,2^{n-1}1^2,2n)$ の場合)

| # | $\mu$ | $(\mu(0),\mu(1),\mu(\infty))$ | $\mu^{-1}(0)$ | 新 $0$-cusp | $u$ の輸送 | 行き先の窓 |
|---|---|---|---|---|---|---|
| 1 | $t$ | $(0,1,\infty)$ | $0$ | **同一点 $P_0$** | 因子 $1$ | $j=2$(自分) |
| **2** | $\dfrac{t}{t-1}$ | $(0,\infty,1)$ | $0$ | **同一点 $P_0$** | **因子 $\mu'(0)=-1$**(局所・補題 TR) | **$j=3$** ★本稿の主題 |
| 3 | $1/t$ | $(\infty,1,0)$ | $\infty$ | 旧 $\infty$-cusp(別点) | **局所公式なし**(大域データ) | $j=2$ |
| 4 | $\dfrac{1}{1-t}$ | $(1,\infty,0)$ | $\infty$ | 旧 $\infty$-cusp(別点) | 局所公式なし(= #3 の後に #2) | $j=3$ |
| 5 | $1-t$ | $(1,0,\infty)$ | $1$ | 型 $2^{n-1}1^2$ の点 | **$u$ の定義域外**(全分岐でない) | — |
| 6 | $\dfrac{t-1}{t}$ | $(\infty,0,1)$ | $1$ | 同上 | **定義域外** | — |

**先行研究との接続**: `docs/week4-K3飽和_opus_v3.md` §3(便 27 P8 の訂正)は既にこの 6 通りを正しく数え、「全分岐点を $0$ に置くのは 4 通り / ordered passport を保つのは **#1,#3** の 2 通り / 残る 2 通り(**#2,#4**)は passport 順を $(6,6,2^21^2)$ に変える / 最後の 2 通り(#5,#6)は定義域外」と書いている。**【GAP-20b】の閉鎖射程は `ordered-passport-preserving` = #1,#3 に限定されていた。**
**本稿の寄与は #2(と #4)の輸送則を計算し、それが $[u]_M$ を保つことを証明する点**であり、閉鎖射程を **4/4(u が定義される全て)** へ広げる。

---

## 4. 補題 TR — cusp を保つ relabel の局所輸送則

> ### 補題 TR(主係数の変換則)
> $F$ を標数 $0$ の体、$\lambda:W\to\mathbf P^1_F$ を $F$ 上定義された Belyi 写像、$P\in W(F)$ を $\lambda(P)=0$、$e(\lambda,P)=M$ の点、$s$ を $P$ の $F$-有理 uniformizer とし
> $$\lambda=u\,s^{M}\bigl(1+O(s)\bigr),\qquad u\in F^\times$$
> と書く。$\mu\in\operatorname{PGL}_2(F)$ が $\mu(\{0,1,\infty\})=\{0,1,\infty\}$ かつ **$\mu(0)=0$** を満たすとする。このとき $\lambda^\mu=\mu\circ\lambda$ は $F$ 上の Belyi 写像で、
> 1. $\lambda^{\mu,-1}(0)=\lambda^{-1}(0)\ni P$、$e(\lambda^\mu,P)=M$(**cusp も分岐指数も動かない**)、
> 2. $$\boxed{\ \lambda^\mu=\bigl(\mu'(0)\cdot u\bigr)\,s^{M}\bigl(1+O(s)\bigr),\qquad\text{すなわち}\quad u^\mu=\mu'(0)\,u\ }$$
> 3. $\{0,1,\infty\}$ を保ち $0$ を固定する Möbius 変換は $\mu=\mathrm{id}$ と $\mu(t)=t/(t-1)$ の**ちょうど 2 つ**で、
> $$\mu'(0)\in\{+1,\,-1\}.$$

**証明.**
(1) $\mu(0)=0$ かつ $\mu$ は同型なので $\mu^{-1}(0)=0$、よって $\lambda^{\mu,-1}(0)=\lambda^{-1}(0)$。分岐指数の乗法性と $e(\mu,\cdot)=1$ から $e(\lambda^\mu,P)=1\cdot M=M$。
(2) $\mu(0)=0$ より $\mu$ は $0$ の近傍で $\mu(t)=\mu'(0)t+O(t^2)$ と展開でき、$\mu'(0)\ne0$($\mu$ は同型)。$\lambda(P)=0$ ゆえ $s\to0$ で $\lambda\to0$ だから代入でき、
$$\lambda^\mu=\mu'(0)\lambda+O(\lambda^2)=\mu'(0)u\,s^M(1+O(s))\cdot\bigl(1+O(s^M)\bigr)=\mu'(0)u\,s^M(1+O(s)).$$
(3) Möbius 変換は 3 点の像で一意。$0\mapsto0$ を課すと残りは $(1,\infty)\mapsto(1,\infty)$ または $(\infty,1)$。前者は $\mathrm{id}$。後者は $\mu(t)=(at+b)/(ct+d)$ に $\mu(0)=0\Rightarrow b=0$、$\mu(1)=\infty\Rightarrow d=-c$、$\mu(\infty)=a/c=1\Rightarrow a=c$ を課して $\mu(t)=t/(t-1)$。このとき
$$\mu'(t)=\frac{(t-1)-t}{(t-1)^2}=\frac{-1}{(t-1)^2},\qquad \mu'(0)=-1.$$
また $\mu\circ\mu(t)=\dfrac{t/(t-1)}{t/(t-1)-1}=t$ なので $\mu$ は**対合**であり、$(\mu'(0))^2=1$ と整合する。$\blacksquare$

> **★ 註(なぜ $u$ の**値**は不変でないか)**: 補題 TR は $u\mapsto-u$ という**値の変化**を主張する。「同一 dessin だから $u$ が同じ」という v1 の読み(F79-4.1 が突いた点)は**幾何的に誤り**であり、正しくは「別の dessin で、$u$ は $-1$ 倍される」。**符号は本当に動く。** 動かないのは次節の class である。

---

## 5. 補題 SQ-INV と定理 J-BLIND — 因子 $-1$ が消える水準

$F_n:=\mathbf Q(\zeta_{4n})$($n\ge3$ 奇)、$M:=2n$、$v_n:=u_n^{-1}$、$a_n:=[v_n]_{2n}\in F_n^\times/F_n^{\times2n}$(t63 §2.3 / BFC (7.2))。

> ### 補題 SQ-INV(算術)
> $$-1=\bigl(\zeta_{4n}\bigr)^{2n}\ \in\ \bigl(F_n^\times\bigr)^{2n}.$$
> したがって任意の $w\in F_n^\times$ に対し
> $$\boxed{\ [-w]_{2n}=[w]_{2n}\ \text{ in } F_n^\times/F_n^{\times2n}\ }$$
> であり、**a fortiori** $[-w]_2=[w]_2$($[-1]_2=1$ は $i=\zeta_{4n}^{n}\in F_n$ からも直接出る)。

**証明.** $\zeta_{4n}\in F_n$ は定義。$(\zeta_{4n})^{2n}=e^{2\pi i\cdot 2n/4n}=e^{\pi i}=-1$。$\blacksquare$

> ### 定理 J-BLIND($j$ 盲目性)
> $n\ge3$ 奇。前件 (R1)(R2)(R3)(§9)の下で、good 窓 $H_{2,\alpha,\beta}$ と $H_{3,\alpha',\beta'}$ が **$[\alpha]=[\alpha']$** を満たすなら
> $$\boxed{\ [u_{H_2}]_{2n}=[u_{H_3}]_{2n}\ \text{ in } F_n^\times/F_n^{\times2n},\qquad\text{ゆえに}\quad a_{H_2}=a_{H_3}.\ }$$
> とくに **$a_n$ の関数として書ける全ての述語** — $[u]_2$(SQ)、$\operatorname{ord}(a_n)$、$\mathcal P_{n,p}$、`FULL_p_DEPTH`、補題 C$'$ の上界判定 — は **$j$ の取り方に依存しない**。

**証明.** §6 の定理 W-REL により、$H_{3,\alpha,\beta}$ 窓の dessin を $\mu(t)=t/(t-1)$ で relabel したものは $H_{2,-\alpha,\beta-1}$ 窓の dessin と同型で、$[-\alpha]=[\alpha]$ かつ $\beta$ の違いは $G_n$-共役(ODD-H 補題 I(1))ゆえ、これは $H_{2,\alpha,\cdot}$ の類の dessin である。補題 TR より両者の $0$-cusp における主係数は $u_{H_2}=-u_{H_3}$($\mu'(0)=-1$)。BFC B-5(ii-loc)(ii-win) により $[\cdot]_{2n}$ は uniformizer とモデルに依らないので、class の等式
$$[u_{H_2}]_{2n}=[-u_{H_3}]_{2n}\overset{\text{補題 SQ-INV}}{=}[u_{H_3}]_{2n}$$
が成り立つ。$a=[u^{-1}]_{2n}$ も同時に等しい。$\blacksquare$

> **★ 委嘱の設問への直接の答**: 司令塔スペックは「$[u]_2$ が救えるか」を問うたが、**$-1$ は $2n$ 乗でもあるので、平方類まで落とさずに $[u]_{2n}$ の水準でそのまま救える**。「弱いが十分な形」ではなく「**強い形で十分**」である。
> **★ 逆に言えば**: $u$ の**値**を $j$ 窓間で比較する主張(例:「$j=3$ 窓でも $-4$ が出るはず」)は**偽**である。出るのは $+4$(§7.4)。**値の一致を canary にしてはならない** — canary は class の一致で書く。

---

## 6. 群論側の族化 — relabel は $B_3$ 由来の自己同型で実現される

$n\ge3$ 奇、$G_n=A\rtimes Q$、$A=\bigoplus_i(\mathbf Z/n)e_i$、$Q=\{1,q_1,q_2,q_3\}$、$X=a_1q_1$、$Y=a_1a_2a_3q_2$、$Z=(XY)^{-1}=a_1^2a_2^{-1}a_3q_3$(ODD-H 補題 A)。

### 6.1 補題 REL — relabel の実現子

> ### 補題 REL
> $\Delta=\sigma_1\sigma_2\sigma_1$、$\delta=\sigma_1\sigma_2$、$g:=\Delta\delta\in B_3$ と置く。$N\in\mathrm{NFI}_{PB_3}(B_3)$ で **$c=\Delta^2\in N$** なるものについて、$g$ による共役は $G:=PB_3/N$ の自己同型 $\nu:=\operatorname{Ad}(g)$ を誘導し、
> $$\boxed{\ \nu(X)=X,\qquad \nu(Y)=X^{-1}ZX,\qquad \nu(Z)=Y\ }$$
> を満たす。とくに三つ組は
> $$(X,Y,Z)\ \longmapsto\ (X,\ Z,\ (XZ)^{-1})\qquad(\text{同時共役の差を除く})$$
> へ写り、これは **branch label の $(1\ \infty)$-交換**そのものである。さらに $\nu^2=\operatorname{Ad}(X^{-1})$ は内部、すなわち $\nu$ は $\operatorname{Out}(G)$ で**対合**。

**証明.** $K\trianglelefteq B_3$ なので $\operatorname{Ad}(g)$ は $PB_3/N$ に降りる。F79-5.1 が承認した
$$\operatorname{Ad}(\Delta):x\mapsto y,\ y\mapsto x,\qquad \operatorname{Ad}(\delta):x\mapsto y,\ y\mapsto zc$$
から、$\operatorname{Ad}(\Delta)\circ\operatorname{Ad}(\delta)=\operatorname{Ad}(\Delta\delta)$ で
$$x\mapsto\operatorname{Ad}(\Delta)(y)=x,\qquad y\mapsto\operatorname{Ad}(\Delta)(zc)=\operatorname{Ad}(\Delta)(z)\cdot c=x^{-1}zx\cdot c$$
($z=(xy)^{-1}$ より $\operatorname{Ad}(\Delta)(z)=(yx)^{-1}=x^{-1}y^{-1}=x^{-1}zx$;$c$ は $B_3$ の中心)。$c\in N$ ゆえ $G$ では $c\mapsto1$ で $\nu(Y)=X^{-1}ZX$。$\nu(Z)=\nu((XY)^{-1})=(X\cdot X^{-1}ZX)^{-1}=(ZX)^{-1}=X^{-1}Z^{-1}=Y$($XYZ=1$ より $Y=X^{-1}Z^{-1}$)。三つ組の像 $(X,X^{-1}ZX,Y)$ を $X$ で同時共役すると $(X,Z,XYX^{-1})=(X,Z,(XZ)^{-1})$。$\nu^2$ は §6.2 の明示形から $\operatorname{Ad}(a_1^{-1}q_1)=\operatorname{Ad}(X^{-1})$。$\blacksquare$

> **★ (F2) の $c$-落としとの合流**: WCP5-D で問題になった「$\operatorname{Ad}(\delta)$ の中心成分 $c$」は、**$c\in N$ の窓では自動的に消える**。$K^{(n)}$ は $\psi_n(c)=(1,1,1)$ なので該当する。**relabel の族化は $c\in N$ の窓に限る**(前件 (R4))。

### 6.2 $\nu$ の明示形と定理 W-REL

$\nu$ は $A$(特性・ODD-H 補題 A(4))を保ち、$X^2=2e_1$, $Y^2=2e_2$, $Z^2=2e_3$(ODD-H §5.2)と補題 REL から一意に決まる:

$$\boxed{\ \nu|_A:\ e_1\mapsto e_1,\quad e_2\mapsto-e_3,\quad e_3\mapsto e_2;\qquad
\nu(q_1)=q_1,\quad \nu(q_2)=a_1^{-1}q_3,\quad \nu(q_3)=a_1^{-1}q_2.\ }$$

> ### 定理 W-REL(窓の付け替え規則)
> 全ての奇数 $n\ge3$、$\alpha\in\mathbf Z/n$、$\beta\in\mathbf Z/n$ について
> $$\boxed{\ \nu\bigl(H_{2,\alpha,\beta}\bigr)=H_{3,\ \alpha,\ \beta-1},\qquad
> \nu\bigl(H_{3,\alpha,\beta}\bigr)=H_{2,\ -\alpha,\ \beta-1}.\ }$$
> ゆえに $G_n$-共役類の完全不変量 (1.11) の水準では
> $$\boxed{\ (2,[\alpha])\ \longleftrightarrow\ (3,[\alpha])\ }$$
> であり、**$(1\ \infty)$-relabel は $[\alpha]$ を保ったまま $j$ だけを入れ替える**。
> さらに、$F_2$-集合として
> $$\bigl(G_n/H;\ x\mapsto X,\ y\mapsto Z\bigr)\ \cong\ \bigl(G_n/\nu(H);\ x\mapsto X,\ y\mapsto Y\bigr)$$
> ($wH\mapsto\nu(w)\nu(H)$ が同型を与える)。

**証明.** $\nu(a_2)=-e_3$、$\nu(a_1^\alpha a_3)=\alpha e_1+e_2$、$\nu(a_1^\beta q_2)=\beta e_1\cdot a_1^{-1}q_3=a_1^{\beta-1}q_3$ より
$$\nu(H_{2,\alpha,\beta})=\langle a_3,\ a_1^\alpha a_2,\ a_1^{\beta-1}q_3\rangle=H_{3,\alpha,\beta-1}$$
((1.2) の $j=3$ では $j'=2$)。同様に $\nu(a_3)=e_2$、$\nu(a_1^\alpha a_2)=\alpha e_1-e_3$(その逆元 $-\alpha e_1+e_3$ を取れば $U_{2,-\alpha}$ の生成元)、$\nu(a_1^\beta q_3)=a_1^{\beta-1}q_2$ より $\nu(H_{3,\alpha,\beta})=H_{2,-\alpha,\beta-1}$。$[-\alpha]=[\alpha]$ は (1.11) の $\pm$ 同一視。最後の $F_2$-集合の同型は $\nu(X)=X$, $\nu(Z)=Y$(補題 REL)から直接。$\blacksquare$

> **★ 構造的な整合(なぜ $(1\ \infty)$ だけが窓族を保つか)**: ODD-H の三述語のうち (P3) は **$\langle X\rangle$ が $G_n/H$ 上推移的**という条件で、$X$ を名指ししている。$\nu=\operatorname{Ad}(\Delta\delta)$ は **$X$ を固定する唯一の非自明 relabel** なので、(1.2) の族を族へ写す。他の relabel($\operatorname{Ad}(\delta\Delta)$ = $(0\ \infty)$ など)は $X$ を動かすので (P3) を保たず、窓の族の外へ出る。**幾何側(表 §3.3 の #2 だけが cusp を保つ)と群論側(補題 REL の $\nu$ だけが $X$ を保つ)が同じ 1 つの relabel を指している** — これが本設計の骨格である。

---

## 7. 既存データによる裏取り(3 件)+ 予言

### 7.1 使い捨て検算スクリプト(数学者レーン・Python・GAP 非依存)

`relabel_check.py`(scratchpad・約 130 行・整数演算のみ。**証明書として登録する価値はないと判断**。再現には本稿の定義を実装すれば足りる)で次を確認:

| # | 検査 | 結果 |
|---|---|---|
| S1 | $n=3,5,7,9,11,15$ で $XYZ=1$、$X^2=2e_1$、$Y^2=2e_2$、$Z^2=2e_3$ | PASS |
| S2 | §6.2 の $\nu$ が**自己同型**(準同型性の抽出検査 + 全単射) | PASS |
| S3 | $\nu(X)=X$、$\nu(Y)=X^{-1}ZX$、$\nu(Z)=Y$、$\nu^2=\operatorname{Ad}(X^{-1})$ | PASS |
| **S4** | **定理 W-REL**: 全 $\alpha\ne0$・全 $\beta$ で $\nu(H_{3,\alpha,\beta})=H_{2,-\alpha,\beta-1}$ かつ $\nu(H_{2,\alpha,\beta})=H_{3,\alpha,\beta-1}$($n=3,5,7,9,11,15$) | **PASS(FAILS = 0)** |
| **S5** | **証明書 §4 の独立再現**($n=3$・剰余類 6 点の置換を Python で構成): passport $(6,2^21^2,6)$ / $(6,6,2^21^2)$ ✓、`h0`($ (X,Y)\sim(X,Y)$)**偽** ✓、`h1`($(X,Y)\sim(X,Z)$)**真・witness は一意** ✓ | **PASS** |
| S6 | $\nu(H_{3,1,0})=H_{2,2,2}$ で、$H_{2,2,2}$ は $H_{2,1,0}$ と $G_3$-共役 | PASS |

> **S5 の位置づけ**: 証明書は GAP、本検算は Python(独立実装)。**剰余類のラベル付けが違うので witness 置換の字面は一致しない**(証明書 `[5,1,4,3,6,2]` vs 本検算の別ラベル)。一致するのは**構造的事実**(`h0` 偽・`h1` 真・witness の個数 = 1)である。したがってこれは「証明書 §4 の**構造的**二系統一致」であり、値の二系統一致ではない。
> **witness が一意であること**の意味: witness の集合は被覆の deck 群 $N_{G_n}(H)/H$ 上の torsor であり、good 窓は自己正規化 (P2) なので deck 群は自明 — **一意性は (P2) の別証**であり、同時に「$\varphi$ は一意 ⟹ Galois 同変 ⟹ 自動的に降下する」という §9(R3) の議論の裏づけでもある。

### 7.2 covariance control $u'=-256/729$ は relabel #3 の実測である

`manifest_k5_appendixA_v1.md` §2 / `search/week4-u-k3.mjs` (13)–(16):
* モデル $t^2+(x-1)^2(4x-1)t+4x^6=0$、Belyi 写像 $\lambda=-t$、cusp $P_0=(x,t)=(0,0)$、uniformizer $s=x$、$t=4x^6+O(x^7)$ ⟹ $u=-4$。
* もう一方の正規化 **$\lambda'=-1/t=1/\lambda$**(= 表 §3.3 の **#3**, $\mu(t)=1/t$)で $u'=-256/729$。

$$\frac{u'}{u}=\frac{-256/729}{-4}=\frac{64}{729}=\Bigl(\frac23\Bigr)^{6}\ \in\ \bigl(F_3^\times\bigr)^{6}
\quad\Longrightarrow\quad [u']_6=[u]_6 .$$

**これは本設計の予言である。** $n=3$ では good 窓の $G_3$-共役類は $(2,[1])$ と $(3,[1])$ の 2 つだけで、#3 は passport $(6,2^21^2,6)$ を保つ(§3.3)から、relabel された dessin は **passport の一意性により再び $(2,[1])$ 類**である。$u$ は被覆の同型類と「$0$ の上の点」だけの関数(B-5(ii-win))なので、class は一致しなければならない。**実測 (16) がその通りになっている。**

> **⚠ 射程**: これは $n=3$ 固有の議論($\varphi(3)/2=1$ ゆえ passport が類を一意に決める)。$n\ge5$ では #3 が $[\alpha]\mapsto[-\alpha^{-1}]$ 型の写像を誘導しうる(未計算)ので、**族的主張にしてはならない**。→【I24-c】

### 7.3 $\varphi(n)/2$ と K5 fixture の `sq`/`ns`(観察・証明ではない)

`manifest_k5_appendixA_v1.md` §1.2 は $K^{(5)}$ の 2 類を **`K5-sq`(平方剰余類 $\{1,4\}$)** と `K5-ns` と名づけている。これは $[\alpha]\in(\mathbf Z/5)^\times/\{\pm1\}=\{[1],[2]\}$ の 2 類であり、**$\alpha$ の平方剰余性が類を分ける**。$\varphi(n)/2$ 個の単元類の集合に $(\mathbf Z/n)^\times/\{\pm1\}$ が単純推移に作用していることの現れである。
**これは I-24 の予想 1($\alpha$ 軌道予想)を判定しない** — 「$G_{\mathbf Q}$ の dessin 作用がこの $\varphi(n)/2$ 個を 1 軌道に混ぜるか」は別問題である。ただし**もし 1 軌道なら**、補題 INV(i23 §6.2)により SQ 述語は $[\alpha]$ 盲目になり **C1′ は完全に閉じる**。→【I24-a】

### 7.4 **予言 I24-P1(測定前・凍結対象)**

補題 TR + 定理 W-REL から、$n=3$ について次が**値の水準で**予言される。

> ### 予言 I24-P1
> $H_{3,[1]}$ 類($n=3$ の第 2 の good 類)の Belyi 写像は、**同じ平面モデル $t^2+(x-1)^2(4x-1)t+4x^6=0$ 上で**
> $$\lambda_3\ :=\ \mu(\lambda_2)\ =\ \frac{-t}{-t-1}\ =\ \frac{t}{t+1}\qquad(\mu(w)=w/(w-1),\ \lambda_2=-t)$$
> で与えられ、**同じ cusp $P_0=(0,0)$・同じ uniformizer $s=x$** に対し
> $$\boxed{\ \lambda_3=4x^6+O(x^7),\qquad\text{すなわち}\quad u_{H_3}=+4=-u_{H_2}\ }$$
> である。したがって
> * **値は一致しない**($-4$ ではなく $+4$)、
> * **class は一致する**: $[+4]_6=[-4]_6$(補題 SQ-INV: $-1=\zeta_{12}^6$)、$[+4]_2=[-4]_2=1$、$\operatorname{ord}([u_{H_3}^{-1}]_6)=3$(= full depth・$u_{H_2}$ と同じ)。

**局所計算(3 行)**: $t=4x^6+O(x^7)$ ⟹ $t+1=1+O(x^6)$ ⟹ $\lambda_3=t/(t+1)=4x^6(1+O(x))\cdot(1+O(x^6))=4x^6+O(x^7)$。∎

> **★ この予言は I-24(b) の「$j=3$ 窓で $u$ を再測定して $-4$ が再現するか」を訂正する。** 発案は「複素共役対だから $-4$ が再現する」と読んだが、**正しい機構は複素共役ではなく Möbius $(1\ \infty)$ で、答は $+4$** である。$-4$ が出たら本設計が偽(または符号規約のずれ)。**どちらでも情報量が大きい。**
> **検定コスト**: `search/week4-u-k3.mjs` の $\lambda$ を 1 行差し替えるだけ(公開値のみ・封印非接触)。加えて $\lambda_3=t/(t+1)$ の分岐データが passport $(6,6,2^21^2)$ になることを確認すれば、窓同定まで閉じる。

---

## 8. `relabel-transport/v1` — typed certificate の設計(P79-E の中身)

P79-E が要求した 7 欄に、**fail-closed に必要な 4 欄を追加**する。

```text
[relabel-transport-capsule]
schema_id                       = "relabel-transport/v1"

# --- P79-E の 7 欄 ---
source_ordered_triple           = { labels: ["0","1","inf"],
                                    perms:  [<sigma_0>, <sigma_1>, <sigma_inf>],
                                    coset_labeling_id: <ラベル付けの pin> }
target_ordered_triple           = { 同上 }
branch_permutation_S3           = <{0,1,inf} 上の置換 pi>        # pi = mu|_{0,1,inf}
base_mobius_transform           = <PGL_2(Q) の行列 [[a,b],[c,d]]>  # lambda^mu = mu . lambda
chosen_cusp_local_parameter     = { source: { point: <P>, uniformizer: <s>, e: <M>,
                                              field_of_rationality: <F> },
                                    target: { point: <P'>, uniformizer: <s'>, e: <M> } }
leading_coefficient_transport   = { cusp_preserved: <bool>,
                                    factor: <mu'(0) = +1 | -1>,      # cusp_preserved = true のときのみ
                                    global_datum_id: <...> }         # false のとき必須
square_class_effect             = { level: <2 | M | 2M>,
                                    factor_class: <[factor]_level>,
                                    justification_id: <"SQ-INV" 等> }

# --- 追加 4 欄(fail-closed に必要) ---
simultaneous_conjugacy_witness  = { g: <perm>, uniqueness: <bool>, deck_group_order: <int> }
orientation                     = HOLOMORPHIC | ANTIHOLOMORPHIC | UNKNOWN
window_classes                  = { source: (j,[alpha]), target: (j,[alpha]) }
invariance_claim                = { predicate: <"[u]_2" | "a_n" | "ord(a_n)" | ...>,
                                    scope: <"this window pair" | "family: n odd">,
                                    proof_id: <"TR+SQ-INV+W-REL" 等> }
```

### 検査規則(受領側・fail-closed)

| # | 条項 |
|---|---|
| **RT-1** | **passport 整合**: `type_source ∘ mu^{-1} = type_target` を受領側で再計算。不一致は**不受理**。 |
| **RT-2** | **witness 必須**: `simultaneous_conjugacy_witness.g` を再検算し、$(X,Y)_{\rm src}\mapsto$ 指定対 の同時共役を確認。**passport の一致だけでは不受理**(= F79-4.1 の教訓)。 |
| **RT-3** | **$\mu$ の一意性**: `branch_permutation_S3` から $\mu$ は一意に決まる。申告された `base_mobius_transform` が $\{0,1,\infty\}$ 上で `branch_permutation_S3` を誘導しなければ**不受理**。 |
| **RT-4** | **cusp gate**: `cusp_preserved` は $\mu^{-1}(0)=0$ **から受領側が計算する**。producer の申告値を信じない。`cusp_preserved = false` で `global_datum_id` が空なら**不受理**(局所公式は使えない)。 |
| **RT-5** | **全分岐 gate**: source の $\mu^{-1}(0)$ の上の点が**全分岐**(型が単一の $M$-サイクル)でなければ、$u$ は定義されないので**不受理**(表 §3.3 の #5,#6)。 |
| **RT-6** | **水準 gate**: `square_class_effect.level` を超える主張を `invariance_claim` に書けない。**`level = 2` の capsule は `a_n`(水準 $2n$)の不変性を licence しない。** 逆に `level = 2n` は水準 2 を含意する(射影)。 |
| **RT-7** | **orientation gate**: `orientation = UNKNOWN` のとき、`invariance_claim` は「$\operatorname{Gal}(F_n/\mathbf Q)$ を法として」の形でしか書けない(§9 (R2))。**述語が Galois 不変(補題 INV)なら結論は同じ**なので、SQ・$\operatorname{ord}(a_n)$ 型の述語では UNKNOWN でも通す。**値の主張は通さない。** |
| **RT-8** | **deck 群**: `deck_group_order != 1` の窓では witness が一意でなく、輸送の同型 $\varphi$ が Galois 同変とは限らない。その場合 `orientation`/降下の議論を別途要求する(good 窓は (P2) より $=1$)。 |

### 既存 artifact の書き換え

`search/certs/i24_u3_recheck_20260729.json` の
`section5_conclusion.u3_reproduction_status = "IDENTITY_SAME_X_CUSP_VIA_H1_WITNESS"`
は **`"RELABEL_1INF_TRANSPORT_FACTOR_MINUS_ONE"`** へ差し替え、`section4_relabeling_hypothesis` に上記 capsule を 1 件添付するのが最小の修理である(**再計算は不要** — 既存の witness はそのまま使える。修理は**読み**の側)。

---

## 9. 前件・射程・残る穴

### 9.1 名前つき前件

| # | 前件 | 状態 |
|---|---|---|
| **(R1)** | 分岐辞書 $x,y,z\leftrightarrow0,1,\infty$ | **閉**(`manifest_k5_appendixA_v1.md` §1.1 の `perm_triple` 規約に登録済) |
| **(R2)** | **(TB1) 圏同値 + 「$F_2$-集合の relabel $\leftrightarrow$ 底の Möbius 後合成」の対応が向きを保つ** | ⚠ **枠組仮定 + 規約**。もし規約が向き反転(反正則)なら $\mu$ は $t\mapsto\overline{t}/(\overline t-1)$ 型になり $u_{H_2}=-\overline{u_{H_3}}$ となる。**その場合でも補題 INV(複素共役は $F_n$ の体自己同型)により SQ・$\operatorname{ord}(a_n)$ 型の述語の結論は変わらない**。変わるのは**値の予言 I24-P1 のみ**($+4$ は実数なので $n=3$ では実は変わらない) |
| **(R3)** | **target 窓の $F_n$-モデルと $F_n$-有理 uniformizer** | **自動**。$\lambda_3:=\mu\circ\lambda_2$ と定義すれば、$\mu\in\operatorname{PGL}_2(\mathbf Q)$ なのでモデル・cusp・uniformizer は source から**継承**される。外部の測定と突き合わせるときだけ B-5(ii-win)(モデル非依存)が要る。**さらに good 窓は (P2) より deck 群が自明なので、二つの被覆の間の同型は一意 ⟹ Galois 同変 ⟹ 定義体へ自動降下**(§7.1 S5 の witness 一意性がこれを実測している) |
| **(R4)** | **$c\in N$**(補題 REL の族化に必要) | $K^{(n)}$ で **閉**($\psi_n(c)=(1,1,1)$)。一般の窓では要確認 |
| **(R5)** | A7(BFC B-5 の当該窓 instance) | **source 窓については既存の caveat と同じ**。target 窓は (R3) により追加負荷なし |

### 9.2 **閉じないもの(委嘱の設問 (d) の根拠)**

| # | 曖昧性 | 本設計の効き |
|---|---|---|
| **$j$**($j=2$ vs $3$) | **閉じる**(定理 J-BLIND) | ただし **命題 ODD-P(ordered passport)が既に $j$ を判別している** — passport $(2n,2^{n-1}1^2,2n)$ は $j=2$ かつ $\alpha$ 単元に限る。したがって**本設計の限界価値は「passport 記録を信頼しなくてよくなる」という多重防御**であり、生きた曖昧性を減らしてはいない |
| **$[\alpha]$**(単元類 $\varphi(n)/2$ 個) | **閉じない** | $\nu$ は $[\alpha]$ を**保つ**(定理 W-REL)。$\operatorname{Aut}(G_n)$ には $\alpha\mapsto u\alpha$ があるが(ODD-H §5.4)、それは **marking を変える** ので dessin の relabel ではない。GT 作用も $\pm1$ 倍しか動かさない(ODD-H §11.2)。**残るのは Galois 作用が $\varphi(n)/2$ 類を混ぜるか(= I-24 予想 1)だけ** |
| $\beta$ | **無関係** | $\beta$ は $G_n$-共役で消える(ODD-H 補題 I(1))。dessin の同型類に影響しない |

$$\boxed{\ \textbf{C1}(n=3):\ \varphi(3)/2=1\ \text{ゆえ}\ \textbf{閉}\ .\qquad
\textbf{C1}'(n\ge5):\ \varphi(n)/2\ge2\ \text{ゆえ}\ \textbf{開}\ (q=7\ \text{なら}\ 3\ \text{類}).\ }$$

---

## 10. 自己監査(falsifier 前)

| # | リスク | 判定 |
|---|---|---|
| R-a | 補題 TR で $\mu$ の展開を $\lambda\to0$ で使ってよいか | ○ $\lambda(P)=0$ かつ $\mu$ は $0$ で正則($\mu(0)=0$ ゆえ極でない)。#3(=$1/t$)では $\mu$ が $0$ で極なので**使えない** — 表 §3.3 で `cusp_preserved=false` として分離済 |
| R-b | $\mu'(0)$ が $\operatorname{PGL}_2$ の代表の取り方に依るか | ○ **依らない**。$\mu(t)=t/(t-1)$ は $0$ を固定する正規化で一意に決まる写像であり、$\mu'(0)$ は写像の不変量 |
| R-c | $[u]_M$ の well-defined 性(uniformizer 取り替え) | ○ $s\mapsto as(1+\cdots)$ で $u\mapsto ua^{-M}$、$a\in F^\times$ ゆえ class 不変(BFC B-5(ii-loc)・t63 §2.2 で確認済) |
| **R-d** | **補題 REL の $\operatorname{Ad}(\Delta),\operatorname{Ad}(\delta)$ の値が正しいか** | ○ **F79-5.1 で Sol が独立追跡・承認**($B_3=\langle a,b\mid a^2=b^3\rangle$、$a=\Delta,b=\delta$ の計算)。$\operatorname{Ad}(\Delta\delta)$ の合成は本稿で新規 |
| **R-e** | **$\nu$ の明示形(§6.2)が正しいか** | ○ **検算 S2/S3 で $n=3..15$ の 6 標本 PASS**(自己同型性・3 つの定義関係・$\nu^2$)。導出自体は $X^2=2e_1$ 等から一意に決まる |
| R-f | 定理 W-REL の $\beta-1$ の $1$ はどこから来たか | ○ $\nu(q_2)=a_1^{-1}q_3$ の $a_1^{-1}$。**検算 S4 で全 $(\alpha,\beta)$ 悉皆 PASS**。なお $\beta$ は共役で消えるので下流に影響しない |
| **R-g** | **「同一 dessin」の誤読を別の形で再現していないか** | ○ **本稿は同一性を一切主張しない。** 主張は「別 dessin・輸送因子 $-1$・class 不変」の 3 段。F79-4.1 の指摘を型として schema に焼いた(RT-2/RT-4/RT-6) |
| **R-h** | **$j$ 盲目性を C1′ 閉鎖と誤読する危険** | ○ **§1(d)・§9.2 で明示的に否定**。★教材候補: 「**既に別の装置(passport)が閉じている曖昧性を閉じても、生きた曖昧性は減らない**」 |
| R-i | 予言 I24-P1 を測定前に既成事実化する危険 | ○ **凍結対象と明記**。$+4$ は**予言**であり実測ではない |
| R-j | (R2) の向き規約が未確定 | △ **残る**。ただし述語水準の結論は補題 INV で守られる(RT-7 で型化) |
| R-k | 表 §3.3 の #4($1/(1-t)$)の輸送 | △ **未計算**。#3 の後に #2 を合成すれば出るが、#3 に局所公式がないので大域データが要る。capsule では `cusp_preserved=false` として `global_datum_id` を要求 |
| R-l | 本稿の「新しさ」の申告 | ○ **grep 済**。6 通りの Möbius の数え方・#1/#3 の passport 保存性・【GAP-20b】の閉鎖射程は `docs/week4-K3飽和_opus_v2/v3.md` §3 に**既出**(便 27 P8)。**新規は (i) #2 の輸送因子 $-1$ の計算、(ii) 補題 SQ-INV による水準 $2n$ での消滅、(iii) $\nu=\operatorname{Ad}(\Delta\delta)$ による族化と定理 W-REL、(iv) capsule schema、(v) 予言 I24-P1**。ラベル: **【GAP-20b】の射程拡張 + F79-4.1 の修理** |

---

## 11. 未閉鎖項・次の一手

* 【I24-a】**$\alpha$ 軌道予想(I-24 予想 1)** — 生き残った唯一の実質的な穴。「$H_{2,\alpha,0}$($\alpha\in(\mathbf Z/n)^\times$)たちが $G_{\mathbf Q}$-dessin 作用で単一軌道か」。**肯定なら補題 INV で C1′ が完全に閉じる。** $n=5$ の 2 類(`K5-sq`/`K5-ns`)が定義体 $\mathbf Q(\sqrt5)$ 上の共役対か、が最小の検定 — ただし **$K^{(5)}$ は blind 進行中**なので手続き上の確認が要る。
* 【I24-b】**予言 I24-P1 の測定**(`search/week4-u-k3.mjs` の $\lambda$ を $t/(t+1)$ に差し替え・数行)。**凍結後**に発注すること。副産物として $\lambda_3$ の passport が $(6,6,2^21^2)$ になることの確認。
* 【I24-c】**relabel #3/#4 の一般 $n$ での窓写像**($(0\ \infty)$ が $(j,[\alpha])$ をどう写すか)。$n=3$ では passport 一意性で閉じたが族的には未計算。$\operatorname{Ad}(\delta\Delta)$ を §6.2 と同じ手順で明示形にすれば出る(半日級)。
* 【I24-d】**capsule schema の凍結**: `relabel-transport/v1` を `typed-edge/v1`(`docs/notes/typed_edge_capsule_v1.md`)の `operation` 列挙に載せるか、独立 schema にするかの判断 — **司令塔案件**。載せるなら `operation = relabel` の新設が要り、それは「capsule 側で語を作らない」規律により **`typed-edge/v2` への版上げ**を意味する。
* 【I24-e】本稿は紙上(paper-proof candidate)+ 使い捨て検算。**Lean 検証ではない。二系統一致でもない**(S5 のみ構造的二系統)。
* 【I24-f】**証明書 §5 の verdict 差し替え**(§8 末尾)— 事務作業だが、**誤った読みが JSON に残っている**ので優先度は高い。

> ### 【文献要請】
> **困難**: 本稿は relabel(底の $S_3$)による $u$ の輸送を閉じたが、**窓の $[\alpha]$ 類の間の関係**(= Galois 軌道)には手が届かない。$[\alpha]$ 類は「同じ passport をもつ非同型 dessin の族」であり、それらの**定義体・moduli 体・Galois 軌道**を分岐データから読む道具がない。
> **欲しい結果の型**: 「与えられた passport をもつ dessin の集合への $G_{\mathbf Q}$ の作用を、モノドロミー群の構造(ここでは $G_n=(\mathbf Z/n)^3\rtimes C_2^2$ という**メタアーベル**な群)から決定する定理」。とくに **dihedral / metabelian モノドロミーの dessin の Galois 軌道が円分指標で記述される**型の結果。キーワードの当て: dessins d'enfants の Galois 軌道不変量(passport を超えるもの)、abelian/metabelian covers の moduli field、Belyi 写像の Galois 作用の明示公式。
> **使い道**: 【I24-a】が閉じ、C1′ が述語水準で完全に無害化される。i17/I-23 のカスケード全体の土台が固まる。
