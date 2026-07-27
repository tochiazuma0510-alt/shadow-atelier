# 比較橋 $B_{\rm FC}$ の紙上攻略 — 前件の精密化と一般証明(**v1**)

2026-07-27 起草: Claude(数学者レイヤー・Opus 5)。司令塔委嘱「$B_{\rm FC}$ の紙上攻略」。
入力: `docs/week4-K3飽和_opus_v3.md`(v3.1–v3.3 = $B_{\rm FC}$ の定義・(5′) の型・§2.6)・`docs/week4-A5算術飽和_v4.md`(§1.4 較正・§3 FC-1〜FC-7)・`sol/sol_reply_29_v3delta.md` F1・`sol/sol_reply_31_manifest.md` F5・`docs/week4-K5_Rule1_v1.md` §1・§7。
検算: `search/week4-bfc-antecedents.mjs`(**13/13 PASS**・本稿発)。
**規律**: $K^{(5)}$ の個別モデル・$u$ には一切触れていない(紙上の一般論のみ)。外部文献は使っていない(§12 に【文献要請 13】を 1 本立てる)。

---

## 0. 判定(先に 10 行)

1. **$B_{\rm FC}$ は 2 段に分解する。第 1 段は無料、第 2 段が全内容である。**
 - **$B_{\rm FC}$-I**(型の段): $G_K$ 上で $\rho_\Lambda\circ\mathrm{Ih}_N$ が $\tau(\mu_M)$ 内の平行移動になる、すなわち $\exists!\,c\in\mathrm{Hom}(G_K,\mu_M)$ で $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(c(\gamma))$。→ **証明済み(§5・定理 B-3)。有限群論と (W2) だけで出る。較正も幾何も要らない。**
 - **$B_{\rm FC}$-II**(同定の段): その $c$ が $\kappa_{u^{-1}}$ である。→ **本稿で証明した(§6–§9・定理 B-7)。**
2. **$B_{\rm FC}$-II はさらに 3 枚に割れ、3 枚とも閉じた**: **II-a** 剛性 descent(§6・定理 B-4)/ **II-b** torsor 比較と $b=1$(§8・補題 B-6)/ **II-c** cusp の局所 Kummer(§7・補題 B-5)。
3. **前件 (4) から「明示 $\mathbb Q$-モデル」「明示局所助変数」「actual marking(exact conjugator)」は消える。** これらは橋の前件ではなく、**$u$ を計算するための窓固有の作業**であり、橋の外にある(§12.2・命題 B-9 で分離)。
4. **前件 (5)(FC-2b/FC-3)は残るが、FC-3 は前件ではなく帰結になる** — (W3)(W5) から $K$-モデルと $\mathrm{Fib}\cong\Lambda$ が**構成できる**(§6)。残る真の入力は較正 FC-2b($A_5$ v4 で証明済・窓非依存)のみ。
5. **$b$ の自由度は二重に吸収される**: (i) 規約 (TB2) の下では $b=1$ が**定理**である(§8)。(ii) 仮に $b\ne1$ でも $R^{\rm cyc}_{\rm formal}$ の結論は $b$ で不変(§10・系 B-8・検算 V8)。Rule 1 (7.1)(7.2) の $b_i$ 欄は**規約監査**であって数学的穴ではない(ただし $K^{(5)}$ の二 dessin 比較 $a_{\rm eff}$ では依然 load-bearing)。
6. **閉じなかったもの = 枠組み札ただ 1 枚**:【GAP-TB】= 接基点繊維関手の 4 性質 (TB1)–(TB4)。これは新しい穴ではなく、**$A_5$ v4 の【GAP-C3】(Deligne 1989 §15)を 4 項目に鋭くしたもの**である。両実例も暗黙に同じ 4 つを使っていた。
7. **新しい前件を 1 本発見した**: **(W5) $\Lambda$ が $\Phi(\mathfrak F_0)$-安定**(v3.1 の (6′) 第 1 節)は、$K$-モデルの存在そのものを供給する。$\mathbb Q$-モデルには $\Phi(\mathrm{GT}(N))$-安定が要る。**$K^{(3)}$ でこれは自明でない**: $\lvert\mathrm{Aut}(G_3)\rvert=1296$ のうち $\Lambda$ を保つのは **432** 個だけで、$\Phi(\mathrm{GT})$ の 12 元はその中に入っている(**検算 V6・V7**)。
8. **前件 (3) の一部は導出できる**: 「$\langle X\rangle$ が $P/H$ 上推移的(= 全分岐)かつ $\lvert\Lambda\rvert=\mathrm{ord}(X)$」から **$N_P(H)=H$ が自動**(命題 B-2)。$K^{(3)}$ で悉皆確認(**検算 V3**: 該当 12 個・反例 0)。
9. **$R^{\rm cyc}$ の状態札は変わる**: $B_{\rm FC}$ は `candidate / UNKNOWN` から **`paper-proof (framework-conditional)`** へ。したがって $R^{\rm cyc}$ 全体(= $B_{\rm FC}+R^{\rm cyc}_{\rm formal}$)も同じ札になる。**`verified` ではない。二人監査も未了。**
10. **五札(§5.2.5)は再構成が要る**: BRIDGE-FAIL の中身が変わり、**BRIDGE-UNKNOWN の入口は (W5) 不成立と【GAP-TB】の 2 つだけ**になる(§13)。

> **自制**: 本稿は**私一人の紙上証明**である。$A_5$ v4 §1.4 が一度「証明した」と書いてから Sol の指摘で 2 度書き直された前例(補題 B の循環・W133)を思えば、**§6 の descent と §8 の $b=1$ は特に監査を要する**(§14 で名指しする)。

---

## 1. 二例の並置 — 何が窓非依存で、何が窓固有だったか

$A_5$ v4 と $K^{(3)}$ v3.1 が **(5′) を閉じた論証**を段ごとに並べる。**「一般化の可否」欄が本稿の作業リストである。**

| 段 | $A_5$ v4 での実装 | $K^{(3)}$ v3.1 での実装 | 一般化 |
|---|---|---|---|
| **(a) 較正** $\alpha^{\rm Ih}=\alpha^{\rm std}$ | §1.4 補題 C・D0・D・系 E・補題 I3‡(自前証明) | §2.1 で **import**(便 27 F5 が PASS 確認) | **窓非依存・証明済**(v4 §1.4.2 の【P173】が既に明言)。**そのまま使う** |
| **(b) $\mathbb Q$-モデルの存在と一意性** | §3.4 FC-4: passport $(5,5,5)$・次数 5 の dessin が同型を除き一意(悉皆 192→120→軌道 2→$S_5$-軌道 1)+ $\mathrm{Aut}_U(W)=C_{S_5}(A_5)=1$ + $H^1(G_\mathbb Q,1)=1$ | §2.2 (P5)(P7): 明示平面モデル $F=t^2+(x-1)^2(4x-1)t+4x^6$ + $N_G(H)=H$ + (P4) exact conjugator | **一般化できた**(§6・定理 B-4)。**悉皆一意性も明示モデルも不要** — $N_P(H)=H$ から descent の cocycle 条件が自動で立つ |
| **(c) cusp の局所理論** | §3.5: $\mathbb Q((\beta))\otimes\mathbb Q(W_0)\cong\mathbb Q((\beta))[\xi]/(\xi^5+2\beta)$ を直接計算 | §2.1「局所 Kummer」: 全分岐点で $\lambda=u\,s^M(1+O(s))$ | **一般化できた**(§7・補題 B-5)。半局所 Dedekind 環の完備化 + Eisenstein のみ |
| **(d) torsor 比較** | §3.5 (3.5): $\gamma:\ j\mapsto\chi_5(\gamma)j+\kappa(\gamma)$ | §2.3(b): $G_K$ 上で $\chi\equiv1$ ゆえ線形部が消え平行移動のみ | **一般化できた**(§8)。しかも**「平行移動である」こと自体は無料**(§5) |
| **(e) $u$ の値** | §2.3 $z'^5=2t$ ⇒ $u=-1/2$ | §3 $t=4x^6+24x^7+\cdots$ ⇒ $u=-4$ | **窓固有**。橋の外(§12.2) |
| **(f) marked 同定** | (3.3) exact conjugator $h=(1\,3\,4\,5)$ | (P4) $h=[6,1,5,4,2,3]$ | **窓固有**。橋の外(命題 B-9 の前件) |
| **(g) 正規化不変性** | §2.4 Belyi 正規化 6 通りで $[2]^4$ 不変 | §3 Möbius 4 通り / ordered-passport 保存 2 通り | **窓固有**。$u$ の抽出の頑健性であって橋ではない |

### 1.1 抽出された共通機構(3 行)

> **(i)** $G_K$ 上では円分指標が自明になるので、$\Lambda$ 上の作用は $\langle X\rangle$-torsor の**平行移動だけ**になる。
> **(ii)** その平行移動指標は、$\Lambda\cong\mathrm{Fib}_{\vec{01}}(W_0)$ を通して、**全分岐 cusp の Kummer torsor の類**である。
> **(iii)** その類は Belyi 写像の cusp での主係数 $u$ で $[u^{-1}]$ と読める。

**(i) は無料**(§5)。**(ii)(iii) が橋の本体**(§6–§9)。両実例が実際に踏んだのはこの 3 段であり、**(b)(c)(d) に見えた「窓固有の工夫」は、一般論の特殊化にすぎなかった**。

### 1.2 見落としていた点(自認)

- v3.1 §5.2.5 の BRIDGE-IN は「**明示**モデル・**明示**局所助変数・actual marking」を封印対象に入れていた。これは**橋の前件と $u$ の計算手続きを混ぜている**。両者を分けると、橋の前件からは「明示」の語が全部落ちる(§13)。
- $A_5$ の FC-4(b)(passport の悉皆一意性)と $K^{(3)}$ の (P4)(exact conjugator)は、**同じ役割 = モデル認識**を果たしていた。これは橋ではなく、**「手元の明示曲線が $W_0$ である」ことの証明書**である(命題 B-9)。

---

## 2. 枠組み前件 (TB1)–(TB4) — 接基点繊維関手から使うものの悉皆

本稿が接基点の理論から使う性質を**全部**列挙する。以後これ以外は使わない(使ったら誤り)。記号は $A_5$ v4 §1.1 に従う: $U=\mathbf P^1_\mathbb Q\smallsetminus\{0,1,\infty\}$、座標 $\beta$、$\Omega:=\bar{\mathbb Q}\{\{\beta\}\}=\bigcup_n\bar{\mathbb Q}((\beta^{1/n}))$。

> **(TB1)(繊維関手)** 有限エタール $W\to U_k$($k\subseteq\bar{\mathbb Q}$ 有限次)に対し
> $$ \mathrm{Fib}_{\vec{01}}(W):=\mathrm{Hom}_{k((\beta))\text{-alg}}\bigl(\mathcal O(W\times_U\mathrm{Spec}\,k((\beta))),\ \Omega\bigr) $$
> は $\deg(W/U)$ 個の元をもつ集合で、$\mathrm{Fib}_{\vec{01}}$ は $\pi_1(U_k,\vec{01})$-集合の圏との同値を与える(Grothendieck–Galois)。
> **(TB2)(基点規約と $\zeta$ 系)** 整合的な $1$ の冪根系 $(\zeta_n)_n$($\zeta_{mn}^m=\zeta_n$)を固定する。$G_\mathbb Q$ は $\Omega$ に**係数のみ**で作用し、すべての $\beta^{1/n}$ を固定する。これが分裂 $s_{\vec{01}}:G_\mathbb Q\to\pi_1(U_\mathbb Q,\vec{01})$ を与える(作用は $\Omega$ への後合成)。
> **(TB3)(幾何的基本群)** $\pi_1(U_{\bar{\mathbb Q}},\vec{01})\cong\hat F_2=\langle x,y\rangle$、$x,y,z=(xy)^{-1}$ はそれぞれ $0,1,\infty$ の慣性生成元、$xyz=1$。
> **(TB4)(慣性の正規化)** $x$ は $\mathrm{Gal}(\Omega/\bar{\mathbb Q}((\beta)))\cong\hat{\mathbb Z}(1)$ の、**$(\zeta_n)$ が定める**位相的生成元 $\sigma_\zeta:\beta^{1/n}\mapsto\zeta_n\beta^{1/n}$($\bar{\mathbb Q}$ 上恒等)の像である。$\hat{\mathbb Z}(1)$ は $\Omega$ への後合成で $\mathrm{Fib}_{\vec{01}}$ に作用する。

> **★ (TB1)–(TB4) の身分**: これは**当工房が §1.1 で置いた規約**((TB2))と、**接基点の理論の標準事実**((TB1)(TB3)(TB4))の混合である。標準事実側が【GAP-TB】(§12.1)。**$A_5$ v4 §3.5 も $K^{(3)}$ §2.1 も、まさにこの 4 つを暗黙に使っていた** — 本稿は使用箇所を明示化しただけで、依存を増やしていない。

> **(TB2) の一意化について**: $(\zeta_n)$ の選択は $\hat{\mathbb Z}^\times$ の自由度をもつが、**同じ $(\zeta_n)$ が $x$ の向き((TB4))と Kummer 指標 $\kappa$ の値の両方を決める**ので、選択は §8 でちょうど相殺する。**これが $b=1$ の正体である。**

---

## 3. 窓前件 (W1)–(W5) — 最小仮定リスト

以下すべて**有限群論の条件**(+ 正典からの読み取り)であり、有限計算で決着する。

| # | 内容 | 型 | 供給元 |
|---|---|---|---|
| **(W1)** | $\bar N\trianglelefteq\hat F_2$ は開・$G_\mathbb Q$-安定(= $N$ は isolated、または少なくとも $\widehat{GT}$-軌道が $\{N\}$)。$P:=\hat F_2/\bar N$、$X:=\pi(x)$、$M:=\mathrm{ord}(X)$ | 正典 | D1 Thm 4.3 等 |
| **(W2)** | $1\to\mathfrak F_0\to\mathrm{GT}(N)\xrightarrow{\tilde\chi}(\mathbb Z/2M)^\times\to1$ 完全、$\tilde\chi\circ\mathrm{Ih}_N=\chi_{2M}$。$K:=\mathbb Q(\zeta_{2M})$ | 正典 | D1 (4.12) 等 |
| **(W3)** | $H\le P$ で **$N_P(H)=H$** | 有限計算 | 窓ごと |
| **(W4)** | **$\langle X\rangle$ が $P/H$ 上推移的**(= $\lambda=0$ 上で全分岐)かつ **$[P:H]=M$** | 有限計算 | 窓ごと |
| **(W5)** | $\Lambda:=\{H\text{ の }P\text{-共役}\}$ が **$\Phi(\mathfrak F_0)$-安定** | 有限計算 | 窓ごと |
| **(W5$^{\mathbb Q}$)** | (任意) $\Lambda$ が **$\Phi(\mathrm{GT}(N))$-安定**($\mathbb Q$-モデルが欲しいとき) | 有限計算 | 窓ごと |

> **v3.1 の (3)(4)(5)(6′) との対応**:
> - v3.1 **(3)**(「$\mathrm{ord}(X)=\lvert\Lambda\rvert=M$ で $\langle X\rangle$ が単純推移」)$\Longleftarrow$ **(W3)+(W4)**(命題 B-2)。逆に (W4) + 「$\lvert\Lambda\rvert=M$」から (W3) が出る(**同値**)。
> - v3.1 **(4)**(明示 $\mathbb Q$-モデル・$\mathbb Q$-有理全分岐 cusp・actual marking)$\Longleftarrow$ **(W3)+(W4)+(W5)**(定理 B-4・補題 B-5)。**「明示」「actual marking」は不要**。
> - v3.1 **(5)**(FC-2b/FC-3)$=$ **較正 (TB1)–(TB4) + $A_5$ v4 §1.4**。FC-3 は前件ではなく帰結(§6.3)。
> - v3.1 **(6′)** の第 1 節(「$\Lambda$ が $\Phi(\mathfrak F_0)$-安定」)$=$ **(W5)**。**これが橋の前件でもあった**ことが本稿の発見。第 2 節(「$\rho_0$ 忠実」)は $R^{\rm cyc}_{\rm formal}$ 側の前件で、**橋には要らない**。

---

## 4. $B_{\rm FC}$ の分解

$$ \boxed{\ B_{\rm FC}\ =\ \underbrace{B_{\rm FC}\text{-I}}_{\text{型: 平行移動である}}\ +\ \underbrace{B_{\rm FC}\text{-II}}_{\text{同定: その指標が }\kappa_{u^{-1}}} } $$

| 段 | 主張 | 依存 | 状態 |
|---|---|---|---|
| **I** | $\exists!\,c\in\mathrm{Hom}_{\rm cont}(G_K,\mu_M)$: $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(c(\gamma))\ \forall\gamma\in G_K$ | (W1)(W2)(W4)(W5) のみ | **§5・定理 B-3 で証明** |
| **II-a** | 一意な $K$-モデル $W_0\to U_K$ が存在(幾何的連結) | (W1)(W3)(W5) + 較正 | **§6・定理 B-4 で証明** |
| **II-b** | $\Lambda\cong\mathrm{Fib}_{\vec{01}}(W_0)$ が $G_K$-集合としても $\mu_M$-torsor としても同型($b=1$) | (TB1)(TB3)(TB4) + (W3)(W4) + 較正 | **§8・補題 B-6 で証明** |
| **II-c** | $\mathrm{Fib}_{\vec{01}}(W_0)$ の torsor 類 $=[u^{-1}]\in K^\times/K^{\times M}$ | (TB1)(TB2) + (W4) | **§7・補題 B-5 で証明** |
| **合成** | $c=\kappa_{u^{-1}}$、すなわち **(5′)** | 上の全部 | **§9・定理 B-7** |

> **★ 分解の効き目**: これで「$B_{\rm FC}$ が UNKNOWN」という粗い札が、**「【GAP-TB】が未閉鎖」という 1 点**に縮む。委嘱の言う「$B_{\rm FC}$ の第 $k$ 段に絞る」の答えは **$k=$ II-b の (TB4)** である。

---

## 5. $B_{\rm FC}$-I の証明 — 型は無料

> **命題 B-1(regular 可換部分群は自己中心化).** $A\le\mathrm{Sym}(\Omega)$ が可換かつ**正則**(単純推移)なら $C_{\mathrm{Sym}(\Omega)}(A)=A$。
> **証明.** $\omega_0\in\Omega$ を固定し $\Omega\xrightarrow{\sim}A$, $a\cdot\omega_0\leftrightarrow a$ と同一視する。$A$ は左移動として作用。$\sigma\in C(A)$、$\sigma(\omega_0)=b\cdot\omega_0$ とすると $\sigma(a\cdot\omega_0)=a\cdot\sigma(\omega_0)=ab\cdot\omega_0$、すなわち $\sigma$ は右移動 $R_b$。$A$ 可換ゆえ $R_b=L_b\in A$。∎

> **命題 B-2(指数の整合 — v3.1 (3) の分解).** $\langle X\rangle$ が $P/H$ 上推移的で $\mathrm{ord}(X)=M$ とする。このとき
> $$ \lvert\Lambda\rvert=M\iff [P:H]=M\iff N_P(H)=H, $$
> かつこのとき $P/H\to\Lambda,\ gH\mapsto gHg^{-1}$ は **$\langle X\rangle$-同変な全単射**であり、$\tau(\zeta_M)$(共役)は左移動 $L_X$ に対応する。
> **証明.** 推移性から $[P:H]\le\lvert\langle X\rangle\rvert=M$。また $\lvert\Lambda\rvert=[P:N_P(H)]\le[P:H]$。よって $\lvert\Lambda\rvert\le[P:H]\le M$。$\lvert\Lambda\rvert=M$ なら全部等号で $N_P(H)=H$。逆も同様。写像 $gH\mapsto gHg^{-1}$ は well-defined・$P$-同変・全射で、単射性は $N_P(H)=H$ と同値。同変性から $\tau(\zeta_M)\leftrightarrow L_X$。∎
> **⇒ (W3) は (W4) + 「$\lvert\Lambda\rvert=M$」の言い換えである。** 検算 **V3**($K^{(3)}$ で該当 $H$ が 12 個・$N_P(H)\ne H$ の反例 0)・**V4**(同変全単射)。

> ### 定理 B-3($B_{\rm FC}$-I).
> (W1)(W2)(W4)(W5) の下で、$\rho_\Lambda\circ\mathrm{Ih}_N|_{G_K}$ の像は $\tau(\mu_M)$ に含まれる。すなわち**一意な連続準同型**
> $$ \boxed{\ c\ :=\ \tau^{-1}\circ\rho_\Lambda\circ\mathrm{Ih}_N|_{G_K}\ :\ G_K\longrightarrow\mu_M\ } \tag{5.1} $$
> が定まり、$\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(c(\gamma))\ (\forall\gamma\in G_K)$。

**証明.**
1. (W5) より $\Phi(\mathfrak F_0)$ は $\Lambda$ を保ち、(W2) より $\gamma\in G_K\Rightarrow\tilde\chi(\mathrm{Ih}_N(\gamma))=\chi_{2M}(\gamma)=1\Rightarrow\mathrm{Ih}_N(\gamma)\in\mathfrak F_0$。ゆえに $\rho_\Lambda(\mathrm{Ih}_N(\gamma))\in\mathrm{Sym}(\Lambda)$ が定義される。
2. shadow の定義 $\Phi_{(m,f)}(X)=X^{2m+1}$ と $\tilde\chi(m,f)=2m+1$ より、$\varphi\in\mathfrak F_0$ なら $2m+1\equiv1\ (2M)$、とくに $\bmod\ M$ でも $1$ だから $\Phi_\varphi(X)=X$。
3. ゆえに $H'\in\Lambda$ に対し $\Phi_\varphi(XH'X^{-1})=\Phi_\varphi(X)\Phi_\varphi(H')\Phi_\varphi(X)^{-1}=X\Phi_\varphi(H')X^{-1}$、すなわち $\rho_\Lambda(\varphi)$ は $\tau(\zeta_M)$ と**可換**。
4. (W4)+命題 B-2 より $\tau(\mu_M)$ は $\Lambda$ 上の **regular 可換**部分群。命題 B-1 より $C_{\mathrm{Sym}(\Lambda)}(\tau(\mu_M))=\tau(\mu_M)$。ゆえに $\rho_\Lambda(\mathfrak F_0)\subseteq\tau(\mu_M)$、とくに $\rho_\Lambda(\mathrm{Ih}_N(G_K))\subseteq\tau(\mu_M)$。
5. $\tau$ は単射(命題 B-2)だから $c$ は well-defined。$\rho_\Lambda\circ\mathrm{Ih}_N$ が連続準同型ゆえ $c$ も。∎

> **★ これは補題 $R'$(v3.1 §5.2.3)の $G_K$ 版であり、証明は逐語同じである。** v3.1 は補題 $R'$ を **(6′) の縮約**にしか使っていなかったが、**同じ補題が (5′) の「型」を無料で供給する**ことに気づいていなかった。これが本稿最大の構造的発見である。
>
> **★ 帰結(用語)**: $\mu_M\subset K$ ゆえ $\mathrm{Hom}_{\rm cont}(G_K,\mu_M)=H^1(G_K,\mu_M)\cong K^\times/K^{\times M}$(Kummer 理論)。よって (5.1) は窓 $(N,H)$ に**正準な類**
> $$ \boxed{\ \mathfrak s(N,H)\ :=\ [c]\ \in\ K^\times/K^{\times M}\quad(\textbf{shadow 類})\ } \tag{5.2} $$
> を与える。**$B_{\rm FC}$ とは「shadow 類 $=$ Belyi 類 $[u^{-1}]$」という主張に他ならない。**
>
> **注(較正はここでは要らない)**: 定理 B-3 は $\mathrm{Ih}_N$ の**存在と (W2)** しか使わない。$\alpha^{\rm Ih}=\alpha^{\rm std}$ が要るのは §8(幾何側との同定)である。**依存関係を正確にすると、較正の使用箇所は 1 か所だけになる。**

---

## 6. $B_{\rm FC}$-II-a — 剛性 descent(**$\mathbb Q$-モデルの存在は前件でなく帰結**)

$\tilde H:=\pi^{-1}(H)\le\hat F_2$(開)、$\tilde\Lambda:=\{\tilde H\text{ の }\hat F_2\text{-共役}\}$ と置く。$\bar N\subseteq\tilde H$ ゆえ $\tilde\Lambda\xrightarrow{\sim}\Lambda$(自然な全単射)。

### 6.1 準備

> **補題 B-4a.** (W3) $N_P(H)=H$ $\Longrightarrow$ $N_{\hat F_2}(\tilde H)=\tilde H$。
> **証明.** $\bar N\trianglelefteq\hat F_2$ かつ $\bar N\subseteq\tilde H$ より、$n\in\bar N$, $h\in\tilde H$ に対し $nhn^{-1}=h\cdot(h^{-1}nhn^{-1})\in\tilde H\bar N=\tilde H$。ゆえに $\bar N\subseteq N_{\hat F_2}(\tilde H)$。$N_{\hat F_2}(\tilde H)/\bar N=N_P(H)=H$ だから $N_{\hat F_2}(\tilde H)=\tilde H$。∎

> **補題 B-4b.** (W1)(W5) + 較正($\alpha^{\rm Ih}=\alpha^{\rm std}$)$\Longrightarrow$ $\tilde\Lambda$ は $\alpha^{\rm std}(G_K)$-安定。
> **証明.** (W1) より $\alpha^{\rm std}_\gamma(\bar N)=\bar N$ で、誘導自己同型 $\beta_\gamma\in\mathrm{Aut}(P)$ が定まる。較正より $\alpha^{\rm std}=\alpha^{\rm Ih}$ だから $\beta_\gamma=\Phi(\mathrm{Ih}_N(\gamma))$($\Phi$ の定義式と (1.1) が逐語同一)。$\gamma\in G_K$ なら定理 B-3 の 1 より $\mathrm{Ih}_N(\gamma)\in\mathfrak F_0$、(W5) より $\beta_\gamma(\Lambda)=\Lambda$。$\alpha^{\rm std}_\gamma(\tilde H)$ は $\beta_\gamma(H)\in\Lambda$ の引き戻しゆえ $\tilde\Lambda$ に入る。∎

### 6.2 定理

> ### 定理 B-4(剛性 descent).
> (TB1)–(TB3)・(W1)(W3)(W5) と較正の下で、$\tilde H$ に対応する $\bar{\mathbb Q}$-被覆 $W\to U_{\bar{\mathbb Q}}$ は **$K$ 上の幾何的連結モデル $W_0\to U_K$ をもち、それは(同型まで一意な同型を除いて)一意**である。**(W5$^{\mathbb Q}$) を仮定すれば $\mathbb Q$-モデルが取れる。**

**証明.** (TB2) の分裂により $\pi_1(U_K,\vec{01})=\hat F_2\rtimes_{\alpha}G_K$($\alpha:=\alpha^{\rm std}$)と書ける。(TB1) より、求める $K$-モデルは
$$ \mathcal H\le\hat F_2\rtimes G_K\ \text{開},\quad \mathcal H\cap\hat F_2=\tilde H,\quad \mathcal H\cdot\hat F_2=\pi_1(U_K,\vec{01}) $$
なる部分群と 1:1 に対応する(第 3 条件が幾何的連結性)。

**構成.** 補題 B-4b より各 $\gamma\in G_K$ について $\alpha_\gamma(\tilde H)\in\tilde\Lambda$。そこで
$$ C_\gamma:=\{c\in\hat F_2:\ c^{-1}\tilde Hc=\alpha_\gamma(\tilde H)\}\ \ne\ \emptyset . $$
$c,c'\in C_\gamma$ なら $d:=c'c^{-1}$ が $d^{-1}\tilde Hd=\tilde H$ を満たす(直接計算)ので補題 B-4a より $d\in\tilde H$。ゆえに
$$ C_\gamma=\tilde H\,c_\gamma\quad(\text{1 つの }c_\gamma\text{ による左剰余類}) \tag{6.1} $$
は**一意に定まる**。写像 $\gamma\mapsto\tilde Hc_\gamma$ は、連続写像 $\gamma\mapsto\alpha_\gamma(\tilde H)\in\tilde\Lambda$(有限集合)を経由するので**連続**。

**cocycle 条件(ここで (W3) が効く).** $\gamma,\delta\in G_K$ に対し
$$ \alpha_{\gamma\delta}(\tilde H)=\alpha_\gamma\bigl(c_\delta^{-1}\tilde Hc_\delta\bigr)=\alpha_\gamma(c_\delta)^{-1}\,\alpha_\gamma(\tilde H)\,\alpha_\gamma(c_\delta) =\bigl(c_\gamma\alpha_\gamma(c_\delta)\bigr)^{-1}\tilde H\bigl(c_\gamma\alpha_\gamma(c_\delta)\bigr), $$
すなわち $c_\gamma\alpha_\gamma(c_\delta)\in C_{\gamma\delta}=\tilde Hc_{\gamma\delta}$。**(6.1) の一意性から cocycle 条件は自動で成立する。**

**部分群であること.** $\mathcal H:=\{(hc_\gamma,\gamma):h\in\tilde H,\ \gamma\in G_K\}$ と置く。
$$ (hc_\gamma,\gamma)(h'c_\delta,\delta)=\bigl(h\,c_\gamma\alpha_\gamma(h')\alpha_\gamma(c_\delta),\ \gamma\delta\bigr), $$
$c_\gamma\alpha_\gamma(\tilde H)c_\gamma^{-1}=\tilde H$ より $c_\gamma\alpha_\gamma(h')=h''c_\gamma$($h''\in\tilde H$)、そして $c_\gamma\alpha_\gamma(c_\delta)\in\tilde Hc_{\gamma\delta}$。ゆえに積は $\mathcal H$ に入る。
**閉性と開性**: $\mathcal H=\{(g,\gamma):\tilde Hg=\tilde Hc_\gamma\}$ は、連続写像 $(g,\gamma)\mapsto(\tilde Hg,\ \tilde Hc_\gamma)\in(\tilde H\backslash\hat F_2)^2$(**右辺は有限集合**)による対角線の逆像なので**閉**。$C_1=N_{\hat F_2}(\tilde H)=\tilde H$ より $c_1=1$ と取れて $\mathcal H\cap\hat F_2=\tilde H$、$\mathcal H\to G_K$ は全射ゆえ $\mathcal H\hat F_2=\pi_1$、したがって $[\pi_1:\mathcal H]=[\hat F_2:\tilde H]<\infty$。副有限群の有限指数閉部分群は**開**。閉かつ積で閉じた副有限群の部分集合は逆元でも閉じるので、$\mathcal H$ は開部分群。∎(存在)

**一意性.** $\mathcal H'$ を別の解とすると、$\gamma$ ごとに $(c'_\gamma,\gamma)\in\mathcal H'$ が取れ、$\mathcal H'\cap\hat F_2=\tilde H$ の正規性から $c'_\gamma\in C_\gamma=\tilde Hc_\gamma$。ゆえに $\mathcal H'=\mathcal H$。∎(一意性)

**(W5$^{\mathbb Q}$) の場合**: 上の議論の $G_K$ を $G_\mathbb Q$ に置換すればよい(補題 B-4b の $\mathfrak F_0$ を $\mathrm{GT}(N)$ に置換)。∎

> **★ 何が起きたか**: これは Weil descent の**剛性版**($\mathrm{Aut}_U(W)=N_P(H)/H=1$ ゆえ descent データが一意 ⇒ cocycle 条件が自動)を、$\pi_1$ の言葉で直接書いたものである。**外部文献を引かずに閉じた。**
>
> **★ $A_5$/$K^{(3)}$ が払っていた代金との比較**: $A_5$ は「$H^1(G_\mathbb Q,\mathrm{Aut})=H^1(G_\mathbb Q,1)=1$」(FC-4(c))という**同じ論法**を使っていたが、「dessin の同型類が一意」(FC-4(b))という悉皆計算と抱き合わせだった。$K^{(3)}$ は明示モデルを外から持ってきた。**どちらも不要**だったことになる。
>
> **⚠ 注意(W5 の非自明性)**: $K^{(3)}$ では $\lvert\mathrm{Aut}(G_3)\rvert=1296$ のうち $\Lambda$ を保つのは **432 個**(検算 **V7**)。$\Phi(\mathrm{GT}(K^{(3)}))$ の 12 元はすべてその中(検算 **V6**)。**つまり (W5)/(W5$^{\mathbb Q}$) は「自明に成り立つ条件」ではない** — v3.1 §2.2 が記録した「$\mathrm{Aut}(G_3)$ が二つの $G_3$-類を融合する」現象は、まさにこの条件が破れうることの実例である。

### 6.3 FC-3 は帰結である

> **系 B-4c(= FC-3).** 定理 B-4 の $W_0$ について、$p\mapsto\mathrm{Stab}_{\hat F_2}(p)$ は $G_K$-同型
> $$ \mathrm{Fib}_{\vec{01}}(W_0)\ \xrightarrow{\ \sim\ }\ \tilde\Lambda\ \xrightarrow{\ \sim\ }\ \Lambda $$
> を与える。$\hat F_2$-同変でもあり、左からの $X$-作用が $\tau(\zeta_M)$ に対応する。
> **証明.** (TB1) より $\mathrm{Fib}_{\vec{01}}(W_0)\cong\mathcal H\backslash\pi_1(U_K,\vec{01})$、その $\hat F_2$-集合としての制限は $\tilde H\backslash\hat F_2\cong\hat F_2/\tilde H$($\hat F_2$ の推移性 = 幾何的連結性)。$\mathrm{Stab}(g\tilde H)=g\tilde Hg^{-1}$ で、補題 B-4a より全単射。$G_K$-同変性は $\mathrm{Stab}(s_v(\gamma)p)=s_v(\gamma)\mathrm{Stab}(p)s_v(\gamma)^{-1}=\alpha^{\rm std}_\gamma(\mathrm{Stab}(p))$(接基点の定義そのもの)。命題 B-2 で $\tilde\Lambda\cong\Lambda$ と $L_X\leftrightarrow\tau(\zeta_M)$。∎
>
> **⇒ v3.1 の前件 (5) のうち FC-3 部分(と便 27 F5 が要求した (FC3-i)(FC3-ii)(FC3-iii))は、すべて (W3)(W5) からの帰結になった。** 前件に残るのは **FC-2b(較正)だけ**である。

---

## 7. $B_{\rm FC}$-II-c — cusp の局所理論と Kummer torsor

$W_0^c$ を $W_0$ の滑らかな射影モデル($\mathbf P^1_K$ の $K(W_0)$ における正規化)、$\lambda:W_0^c\to\mathbf P^1_K$ を延長した Belyi 写像とする。

> **補題 B-5a(繊維の分解).** $R:=\mathcal O_{\mathbf P^1_K,0}$(DVR・uniformizer $\beta$)、$B:=$ $K(W_0)$ における $R$ の整閉包(半局所 Dedekind)とすると
> $$ \mathcal O\bigl(W_0\times_U\mathrm{Spec}\,K((\beta))\bigr)\ \cong\ B\otimes_R K((\beta))\ \cong\ \prod_{P\mid 0}\ \kappa(P)((s_P)) $$
> ($P$ は $\lambda^{-1}(0)$ の閉点、$s_P$ は $P$ での uniformizer)。
> **証明.** $\mathrm{Spec}\,K((\beta))\to\mathbf P^1_K$ は $\beta,\beta-1$ が単元ゆえ $U$ を経由し、$W_0\times_U\mathrm{Spec}\,K((\beta))=W_0^c\times_{\mathbf P^1}\mathrm{Spec}\,K((\beta))$。$B$ は有限 $R$-加群だから $B\otimes_RR^\wedge=B^\wedge$(($\beta$)-進完備化)、半局所 Dedekind の完備化は CRT で $\prod_P B_P^\wedge$ に分解。$\beta$ を可逆にして $\prod_P\mathrm{Frac}(B_P^\wedge)=\prod_P\kappa(P)((s_P))$。∎

> **補題 B-5b(幾何点 $\leftrightarrow$ 慣性軌道).** $\lambda^{-1}(0)$ の**幾何**点は $\mathrm{Fib}_{\vec{01}}(W_0)$ 上の $\langle x\rangle$-軌道と 1:1 に対応し、軌道の長さが分岐指数である。
> **証明.** 補題 B-5a を $\bar{\mathbb Q}$ 上で読むと $\prod$ の各因子は $\bar{\mathbb Q}((s_P))/\bar{\mathbb Q}((\beta))$ で全分岐次数 $e_P$、その $\Omega$ への埋め込みは $e_P$ 個で $\mathrm{Gal}(\Omega/\bar{\mathbb Q}((\beta)))=\hat{\mathbb Z}(1)$ が推移的に置換する((TB4))。∎

> ### 補題 B-5(局所 Kummer).
> (W4) を仮定する。すると
> **(i)** $\lambda^{-1}(0)$ はただ 1 点 $P_0$ からなり、$P_0$ は **$K$-有理**で分岐指数 $M$。
> **(ii)** $P_0$ での任意の $K$-有理 uniformizer $s$ について $\lambda=u\,s^M(1+O(s))$、$u\in K^\times$。**$[u]_M\in K^\times/K^{\times M}$ は $s$ の選び方にも $K$-モデルの取り方にも依らない。**
> **(iii)** $K((\beta))$-代数として
> $$ \mathcal O\bigl(W_0\times_U\mathrm{Spec}\,K((\beta))\bigr)\ \cong\ K((\beta))[T]/(T^M-u^{-1}\beta), $$
> したがって
> $$ \mathrm{Fib}_{\vec{01}}(W_0)=\bigl\{\,\xi\,(u^{-1})^{1/M}\beta^{1/M}\ :\ \xi\in\mu_M\,\bigr\}\subset\Omega \tag{7.1} $$
> は $\mu_M$-torsor($\mu_M$ は乗法で作用・$m(\xi)$ と書く)であり、
> $$ \boxed{\ \gamma\cdot p\ =\ m\bigl(\kappa_{u^{-1}}(\gamma)\bigr)\,p\qquad(\forall\gamma\in G_K,\ p\in\mathrm{Fib}) \ } \tag{7.2} $$
> すなわち **torsor 類は $[u^{-1}]\in K^\times/K^{\times M}=H^1(G_K,\mu_M)$**。

**証明.**
**(i)** (W4) と補題 B-5b: $\langle X\rangle=\langle x\rangle$ の像は $\mathrm{Fib}\cong P/H$ 上推移的だから幾何点は 1 個、分岐指数 $=[P:H]=M$。$G_K$ はこの唯一の幾何点を保つので、対応する閉点 $P_0$ の剰余体は $\kappa(P_0)=K$($\lvert\{\text{幾何点}\}\rvert=[\kappa(P_0):K]=1$)。
**(ii)** $P_0$ は滑らかな $K$-有理点なので $\mathfrak m_{P_0}/\mathfrak m^2\cong K$、$K$-有理 uniformizer $s$ が取れる。$v_{P_0}(\lambda)=e_{P_0}=M$ より $\lambda=us^M+\cdots$、$u\in K^\times$。$s'=as(1+O(s))$($a\in K^\times$)に取り替えると $u\mapsto ua^{-M}$ なので $[u]_M$ は不変。$K$-モデルは定理 B-4 で一意なので $[u]_M$ は窓のデータだけで決まる。
**(iii)** $h:=u^{-1}\lambda s^{-M}\in K[[s]]$ は $h(0)=1$、$M\in K^\times$ だから $h^{1/M}\in K[[s]]$(定数項 1)が**一意に**存在する。$\tilde s:=s\,h^{1/M}$ は uniformizer で $\tilde s^M=u^{-1}\lambda=u^{-1}\beta$。補題 B-5a と (i) より $\mathcal O(\cdots)=K((s))=K((\tilde s))$、次数は $M$、$T^M-u^{-1}\beta$ は $K((\beta))$ 上 Eisenstein ゆえ既約。よって同型。
(7.1) は $T^M-u^{-1}\beta$ の $\Omega$ における根の集合。$\gamma\in G_K$ は (TB2) より $\beta^{1/M}$ を固定し係数に作用するので $\gamma\bigl(\xi(u^{-1})^{1/M}\beta^{1/M}\bigr)=\xi\,\kappa_{u^{-1}}(\gamma)\,(u^{-1})^{1/M}\beta^{1/M}$。$\mu_M\subset K$ ゆえ $\kappa_{u^{-1}}:G_K\to\mu_M$ は準同型で $M$ 乗根の選び方に依らない。∎

> **★ $A_5$ v4 §3.5 との照合**: そこでは $\xi^5=-2\beta$、すなわち $u^{-1}=-2$、$u=-1/2$。(7.1) は $\{\zeta_5^j(-2)^{1/5}\beta^{1/5}\}$ で**逐語一致**。$K^{(3)}$ §2.1 の「$\lambda=us^M(1+O(s))$ ⇒ $[u^{-1}]$」も (ii)(iii) の特殊化。

---

## 8. $B_{\rm FC}$-II-b — torsor 比較と $b=1$

> ### 補題 B-6(torsor 比較).
> (TB1)–(TB4)・(W1)(W3)(W4)(W5) と較正の下で、系 B-4c の同型 $c_\Lambda:\mathrm{Fib}_{\vec{01}}(W_0)\xrightarrow{\sim}\Lambda$ は
> $$ \boxed{\ c_\Lambda\circ m(\xi)\circ c_\Lambda^{-1}\ =\ \tau(\xi)\qquad(\forall\xi\in\mu_M)\ } \tag{8.1} $$
> を満たす。すなわち **$b=1$**。

**証明.**
1. (TB4) より $x$ は $\mathrm{Fib}$ に $\sigma_\zeta$ の後合成で作用する。(7.1) の点 $p=\xi'(u^{-1})^{1/M}\beta^{1/M}$ に対し、$\sigma_\zeta$ は $\bar{\mathbb Q}$(ゆえに $(u^{-1})^{1/M}$ と $\xi'$)を固定し $\beta^{1/M}\mapsto\zeta_M\beta^{1/M}$ を与えるから
$$ x\cdot p=\zeta_M\,p=m(\zeta_M)\,p . $$
2. 系 B-4c より $c_\Lambda$ は $\hat F_2$-同変で、$x$ の $\Lambda$ 上の作用は $\tau(\zeta_M)$(命題 B-2)。ゆえに $c_\Lambda\circ m(\zeta_M)\circ c_\Lambda^{-1}=\tau(\zeta_M)$。
3. $m,\tau$ はともに準同型 $\mu_M\to\mathrm{Sym}(\Lambda)$ で、$c_\Lambda$ による共役も準同型。生成元 $\zeta_M$ で一致するから全体で一致。∎

> **★ $b=1$ の正体**: (TB2) の $(\zeta_n)$ が **$x$ の向き**((TB4))と **$\kappa$ の値**((7.2))の**両方**を決めているので、$(\zeta_n)\mapsto(\zeta_n^t)$($t\in\hat{\mathbb Z}^\times$)に取り替えると $\tau$ の生成元と $\kappa$ の値が**同時に**ひねられて相殺する。**$b$ は「二つの独立な規約のずれ」ではなく、「一つの規約を二度使う」ことで消える。**
>
> **⚠ ただし実装では $b$ を記録せよ**: Rule 1 §7.4 の言うとおり、実装が (a) GAP の右共役規約、(b) 埋め込み (1.6) と別の原始根、(c) 惰性生成元の反転、のいずれかを踏むと $b\ne1$ が出る。**それは「(TB2) を破った」ことの検出器**であり、数学的発見ではない。**$b_i$ 欄の厳格運用(Rule 1 (7.1)・受理条件 (7.3))は本稿によっても撤回されない**(§10)。

---

## 9. 主定理

> ### 定理 B-7(比較橋 $B_{\rm FC}$).
> **枠組み** (TB1)–(TB4)、**較正** $\alpha^{\rm Ih}=\alpha^{\rm std}$($A_5$ v4 §1.4・窓非依存)、**窓前件** (W1)(W2)(W3)(W4)(W5) の下で:
> **(a)** 一意な $K$-モデル $W_0\to U_K$ が存在し、$\lambda^{-1}(0)$ は唯一の $K$-有理点 $P_0$(分岐指数 $M$)。
> **(b)** $[u]_M\in K^\times/K^{\times M}$ が窓のデータだけから定まる。
> **(c)** すべての $\gamma\in G_K$ について
> $$ \boxed{\ \rho_\Lambda\bigl(\mathrm{Ih}_N(\gamma)\bigr)\ =\ \tau\bigl(\kappa_{u^{-1}}(\gamma)\bigr) \ } \tag{9.1} $$
> — すなわち **v3.1 の (5′) = (7.3)**。同値に、shadow 類 $=$ Belyi 類: $\mathfrak s(N,H)=[u^{-1}]$。

**証明.** (a) は定理 B-4 + 補題 B-5(i)。(b) は補題 B-5(ii)。(c): 定理 B-3 より $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(c(\gamma))$。他方、系 B-4c の $c_\Lambda$ は $G_K$-同変だから、$\Lambda$ 上の $G_K$-作用は $\mathrm{Fib}$ 上の作用の輸送であり、(7.2) と補題 B-6 (8.1) より
$$ \rho_\Lambda(\mathrm{Ih}_N(\gamma))\ \overset{\text{系 B-4c}}{=}\ c_\Lambda\circ\bigl(\gamma\text{-作用}\bigr)\circ c_\Lambda^{-1}\ \overset{(7.2)}{=}\ c_\Lambda\circ m(\kappa_{u^{-1}}(\gamma))\circ c_\Lambda^{-1}\ \overset{(8.1)}{=}\ \tau(\kappa_{u^{-1}}(\gamma)). $$
$\tau$ 単射より $c=\kappa_{u^{-1}}$。∎

> **系 B-7′(族定理).** 定理 B-7 の前件に加えて $R^{\rm cyc}_{\rm formal}$ の前件 **(2)**($\mathfrak F_0\cong C_e$, $e\mid M$)と **(6′) の忠実性**($\rho_0$ が忠実)を仮定すれば、v3.1 §5.2.2 の証明と合わせて
> $$ \mathrm{Ih}_N\ \text{が全射}\iff\mathrm{ord}\bigl([u^{-1}]_M\bigr)=e,\qquad \mathrm{Fix}(\ker\mathrm{Ih}_N)=K\bigl((u^{-1})^{1/M}\bigr) $$
> が**前件から結論まで一貫した定理として**成立する。**これが「族定理 $R^{\rm cyc}$」の完成形である。**
> **前件の総数は 7 本**: (W1)(W2)(W3)(W4)(W5) + (2) + 「$\rho_0$ 忠実」。**すべて有限計算か正典読み取りで決着する。**

> **⚠ 状態札(誇張しない)**: 系 B-7′ は **`paper-proof (framework-conditional)`**。(i) **Lean `verified` ではない**、(ii) **Sol 監査未了**、(iii) **【GAP-TB】に条件つき**、(iv) $u$ の**計算**は依然窓固有(§12.2)。

---

## 10. $b$ の自由度 — Rule 1 (7.1)(7.2) の型で吸収できるか

**答: できる。しかも二重に。**

> **系 B-8($b$-頑健性).** $b\in(\mathbb Z/M)^\times$ を任意とし、(9.1) の代わりに**ひねった形**
> $$ \rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau\bigl(\kappa_{u^{-1}}(\gamma)^b\bigr)\qquad(\forall\gamma\in G_K) \tag{10.1} $$
> を仮定しても、$R^{\rm cyc}_{\rm formal}$ の結論 **(R6-full)** と **(7.4)** は**変わらない**。
> **証明.** $\xi\mapsto\xi^b$ は $\mu_M$ の自己同型なので (i) $\lvert\kappa^b(G_K)\rvert=\lvert\kappa(G_K)\rvert=\mathrm{ord}([u^{-1}]_M)$、(ii) $\mu_M[e]$ は $\mu_M$ の特性部分群ゆえ $\kappa^b(G_K)\subseteq\mu_M[e]\iff\kappa(G_K)\subseteq\mu_M[e]$、(iii) $\ker\kappa^b=\ker\kappa$。v3.1 §5.2.2 の証明の 2・3・5 はこれらしか使わない。∎(検算 **V8**)

**吸収の二層**:

| 層 | 内容 | 帰結 |
|---|---|---|
| **第 1 層(数学)** | (TB2) の規約の下で **$b=1$ が定理**(補題 B-6) | 正しい実装なら $b_i=1$ が出る「はず」 |
| **第 2 層(頑健性)** | $b\ne1$ でも結論不変(系 B-8) | 万一 $b_i\ne1$ でも**単一窓の $R^{\rm cyc}$ は生き残る** |

> **⚠ ただし $K^{(5)}$ の二 dessin 比較 (P2) では $b$ は依然 load-bearing**: Sol 便 31 F5.2 の $a_{\rm eff}=[b_{\rm ns}]^{-1}a[b_{\rm sq}]$ は**二つの窓の間の比較**であり、系 B-8 の「単一窓では相殺」は効かない。$b_{\rm sq}\ne b_{\rm ns}$ なら $[u_{\rm ns}^{-1}]_{10}=[u_{\rm sq}^{-1}]_{10}$ という完全一致形が崩れる。**Rule 1 §7.3 の受理条件 $b_{\rm sq}=b_{\rm ns}$ は正しく、本稿は撤回を要求しない。**
> **本稿が言えるのは 1 点だけ**: 「$b_i\ne1$ が出たら、それは**発見ではなく (TB2) 違反**である」— Rule 1 §7.4 (a)(b)(c) の診断リストが正しいことの理論的裏づけ。

---

## 11. 実例二つとの整合検査

### 11.1 $A_5$ 窓

| 前件 | 値 / 根拠 | 判定 |
|---|---|---|
| (W1) | $N_A$ isolated(裁定 15 A1.v2.2・二系統) | ✓ |
| (W2) | $\lvert\mathrm{GT}\rvert=20$、$(\mathbb Z/10)^\times\cong C_4$、$\mathfrak F_0\cong C_5$、$K=\mathbb Q(\zeta_{10})=\mathbb Q(\zeta_5)$ | ✓ |
| (W3) | $N_{A_5}(A_4)=A_4$(v4 (3.2)) | ✓ |
| (W4) | $X$ は 5-サイクル ⇒ $A_5/A_4$(5 点)上推移的、$[P:H]=5=M$ | ✓ |
| (W5)/(W5$^\mathbb Q$) | $\mathrm{Aut}(A_5)=S_5$ は指数 5 部分群の唯一の類を保つ | ✓(自明に成立) |
| **帰結** | $\mathbb Q$-モデル存在・$P_0$ が $\mathbb Q$-有理・全分岐 5 | v4 §2.1 の LMFDB モデルと一致 |
| **(9.1)** | $\tau(\kappa_{-2}(\gamma))$ = v4 (3.5) の $j\mapsto j+\kappa(\gamma)$($G_K$ 上 $\chi_5=1$) | **逐語一致** ✓ |

**★ $A_5$ で FC-4(b)(passport 悉皆一意性)が要らなかったこと**の確認: 定理 B-4 は $H$ から直接 $W_0$ を作るので、「その型の dessin が一意」は不要。v4 の悉皆は**モデル認識**(LMFDB モデル = $W_0$)にのみ使われていた。実際 v4 §3.4 の【v3 追加】自身が「(3.3) の exact conjugator で FC-4(d) の load-bearing 部分は直接閉じるので、(b) の悉皆は補助証拠に落とす」と書いており、**本稿の分離と独立に同じ結論に達していた**。

### 11.2 $K^{(3)}$ 窓 — 検算 `search/week4-bfc-antecedents.mjs`(13/13)

| # | 検査 | 結果 |
|---|---|---|
| **V1** | $[P:H]=6=M=\mathrm{ord}(X)$、$\langle X\rangle$ が $P/H$ 上推移的 | PASS |
| **V2** | $N_P(H)=H$ | PASS |
| **V3** | 命題 B-2 の悉皆: 「$\langle X\rangle$ 推移的 かつ $\lvert\Lambda\rvert=6$」を満たす $H$ は 12 個、**すべて** $N_P(H)=H$(反例 0) | PASS |
| **V4** | $P/H\to\Lambda$ が $\langle X\rangle$-同変全単射・$\tau$ は 6-サイクル | PASS |
| **V5** | $\Lambda$ は $\Phi(\mathfrak F_0)$(3 元)で安定 | PASS |
| **V6** | **【新規】**$\Lambda$ は $\Phi(\mathrm{GT}(K^{(3)}))$ 全 12 元で安定 ⇒ **$\mathbb Q$-モデルが (W5$^\mathbb Q$) から従う** | PASS |
| **V7** | **【新規】**$\lvert\mathrm{Aut}(G_3)\rvert=1296$、$\Lambda$ を保つのは **432 個**のみ ⇒ (W5) は自明でない | PASS |
| **V8** | $b\in(\mathbb Z/6)^\times$ のひねりで $\mathrm{ord}(\kappa)$・$\ker\kappa$・$\tau(\mu_6)$ が不変(系 B-8) | PASS |

> **★ V6 の意味(v3.1 への上向きの寄与)**: 定理 K3 §2.2 (P7) は「残留 descent なし」を、明示 $\mathbb Q$-モデル + exact marking + $N_G(H)/H=1$ に依拠して主張していた(W5 に従い「$\mathrm{Aut}=1$ 単独では不十分」と正しく限定した上で)。**V6 は、その主張を明示モデルに依らず有限群論だけで再導出する**。定理 K3 の (P7) に**独立な第二証明**が付いたことになる(数値結論は不変)。
>
> **★ V7 の意味**: $\Phi(\mathrm{GT})\subsetneq\{$ $\Lambda$ を保つ 432 元 $\}\subsetneq\mathrm{Aut}(G_3)$。**もし $\Phi(\mathrm{GT})$ が 432 の外にはみ出していたら $\mathbb Q$-モデルは存在せず、橋は $K$ 上でしか架からなかった。** 実例が「たまたま」ではないことの確認。

### 11.3 整合の総括

**二例とも、本稿の前件 (W1)–(W5) を満たし、本稿の結論 (9.1) が既存の個別計算と逐語一致する。** 一般化が二例を再現できないという事故はない。

---

## 12. 閉じなかったもの — 障害の同定

### 12.1 【GAP-TB】(唯一の残存)— 接基点繊維関手の 4 性質

> **【GAP-TB】** (TB1)(TB3)(TB4) の標準事実部分に、原典の §/定理番号を付けた照合が無い。
> - **(TB1)** 接基点での繊維関手が $\pi_1$-集合の圏同値を与えること。
> - **(TB3)** $\pi_1(U_{\bar{\mathbb Q}},\vec{01})\cong\hat F_2$ と慣性生成元の指定。
> - **(TB4)(最重要)** $\vec{01}$ における慣性が $\mathrm{Gal}(\Omega/\bar{\mathbb Q}((\beta)))\cong\hat{\mathbb Z}(1)$ と**正準に**同一視され、$\mathrm{Fib}$ への作用が $\Omega$ への後合成であること。
>
> **障害の正確な所在**: **(TB4) が第 $k$ 段**である。(TB1)(TB3) は圏同値と生成元の名づけで、破れても記法の問題にとどまる。**(TB4) が破れると補題 B-6 の 1(「$x\cdot p=\zeta_Mp$」)が出ず、$\Lambda$ と $\mathrm{Fib}$ の $\mu_M$-torsor 構造の同一視が失われる。すると (9.1) は「$\tau(\text{何か})$」までしか言えず、$\kappa_{u^{-1}}$ との同定ができない。**
>
> **新しい穴ではない**: $A_5$ v4 §6 の【GAP-C3】(「枠組みそのもの — 接基点での繊維関手の存在と Galois 同変性」)と同じもの。**本稿はそれを 4 項目に分解し、うち (TB4) だけが load-bearing であることを特定した。** これは前進(粗い札 → 名指しの 1 項目)。
>
> **両実例も同じ札に依存していた**: $A_5$ v4 §3.5 の「$\gamma$ は $\beta^{1/5}$ を固定し係数のみに作用」と「$\hat F_2$ の $\mathrm{Fib}$ への作用」の突合、$K^{(3)}$ §2.1 の「局所 Kummer」。**本稿は依存を増やしていない。**

> ### 【文献要請 13】接基点における慣性の正準同一視
> **困難**: 補題 B-6 の第 1 段(= (TB4))。$U=\mathbf P^1-\{0,1,\infty\}$ の $0$ での接基点 $\vec{01}$ について、
> (i) 繊維関手 $\mathrm{Fib}_{\vec{01}}(W)=\mathrm{Hom}_{k((\beta))}(\mathcal O(W\times_U k((\beta))),\Omega)$ が $\pi_1(U_k,\vec{01})$-集合の圏同値を与えること、
> (ii) $\mathrm{Gal}(\Omega/\bar k((\beta)))\cong\hat{\mathbb Z}(1)$ の像が $0$ の慣性部分群であり、$(\zeta_n)$ が定める生成元が標準生成元 $x$ に対応すること、
> (iii) $G_k$ の**係数作用**が定める分裂と (ii) の慣性作用が、どちらも $\Omega$ への後合成として**同時に**記述されること。
> **欲しい結果の型**: 上の (i)–(iii) を、$\S$/定理番号つきで述べた文献 1 本(または各項目に 1 本ずつ)。第一候補は Deligne, *Le groupe fondamental de la droite projective moins trois points*(1989)の §15(既に $A_5$ v4 §1.4.4 が名指ししている)。**優先度は中**: 本稿の結論は (TB1)–(TB4) を定義/規約として採る限り自己完結しており、これは**枠組みの裏取り**である。
> **注意**: 降ろされた場合、確認すべきは「(TB4) の生成元の向きが $(\zeta_n)$ とどう結びつくか」の 1 点。ここで規約差があれば $b\ne1$ になるが、系 B-8 により**単一窓の結論は不変**。

### 12.2 橋の外へ出したもの — 「モデル認識段」(命題 B-9)

定理 B-7 は $W_0$ の**存在と一意性**を言うが、**手元の明示曲線 $C$ が $W_0$ であること**は言わない。$u$ を数値として計算するにはこれが要る。

> **命題 B-9(モデル認識).** $(C,\lambda_C)$ を $K$ 上の滑らかな射影曲線と Belyi 写像で、$C|_U\to U$ が有限エタール・幾何的連結とする。**証明書**として
> **(R-1)** $C_{\mathbb C}$ の分岐 cycle 三つ組 $(\sigma_0,\sigma_1,\sigma_\infty)$($\sigma_0\sigma_1\sigma_\infty=1$、標準的向き・$0,1,\infty$ の順)、
> **(R-2)** 明示的共役元 $h$ で $h\sigma_0h^{-1}=X_{|P/H},\ h\sigma_1h^{-1}=Y_{|P/H},\ h\sigma_\infty h^{-1}=Z_{|P/H}$(同時共役)
> が与えられれば、$C\cong W_0$($U$ 上の $K$-同型)であり、したがって $[u_C]_M=[u]_M$。
> **証明(素描).** (R-2) は $C$ の幾何 monodromy 表現の核が $\bar N$ を含み、点 stabilizer が $\tilde H$ の共役であることを与える(3 点球面の pure mapping class group は自明ゆえ標準生成三つ組は同時共役を除き一意)。ゆえに $C\times_K\bar{\mathbb Q}\cong W$。$C$ が $K$-モデルだから定理 B-4 の一意性で $C\cong W_0$。∎
>
> **状態**: 素描である。**「3 点球面の標準生成三つ組は同時共役を除き一意」という位相的事実**と、**位相的 $\pi_1$ と接基点 $\pi_1$ の比較**(Riemann existence + 経路の取り替え = 共役)を使っており、これは (TB1)–(TB4) と同格の枠組み事実である。**【GAP-TB】に相乗りする。**
>
> **★ これが両実例の「一番手間のかかった部分」の正体**: $A_5$ の (3.3)($h=(1\,3\,4\,5)$)も $K^{(3)}$ の (P4)($h=[6,1,5,4,2,3]$)も、**命題 B-9 の (R-2) そのもの**である。$K^{(3)}$ §3 の Möbius 正規化の数え方(ordered passport 保存 2 通り)は、(R-1) の「$0,1,\infty$ の順」を手元のデータベース記法に合わせる作業であった。
>
> **⇒ 運用上の帰結**: BRIDGE-IN の封印対象は「明示モデル」ではなく **(R-1)(R-2) の証明書**である。**橋(定理 B-7)は封印の外に出せる**(結果に依存しない一般論だから)。

### 12.3 閉じたが監査を要する 2 か所(自己申告)

| # | 箇所 | 不安の内容 |
|---|---|---|
| **A-1** | **§6 定理 B-4 の cocycle 自動性** | (6.1) の一意性から cocycle 条件を導く 3 行。「$c_\gamma\alpha_\gamma(c_\delta)\in C_{\gamma\delta}$」の計算で $\alpha$ が**左作用**であること・$\rtimes$ の積の向きを取り違えていないか。**規約の向きに敏感な唯一の箇所。** |
| **A-2** | **§8 補題 B-6 の 1** | (TB4) から「$x\cdot p=m(\zeta_M)p$」を出す段。**後合成が左作用であること**と、$\mathrm{Fib}$ の $\hat F_2$-作用が慣性については後合成で書けること。**【GAP-TB】と同じ場所に立っている。** |

> **さらに小さいが記録しておく点**: 補題 B-5(i) の「唯一の幾何点 ⇒ $\kappa(P_0)=K$」は標数 0 の分離性を使う(幾何点の個数 $=[\kappa(P_0):K]$)。$K$ 完全体ゆえ問題ないが、書いておく。

---

## 13. 前件リストの最終形(封印用)

### 13.1 定理 B-7($B_{\rm FC}$)の前件

| 層 | # | 内容 | 型 | 状態 |
|---|---|---|---|---|
| **枠組み** | (TB1) | 接基点繊維関手の圏同値 | 標準事実 | **【GAP-TB】** |
| | (TB2) | $(\zeta_n)$ 固定・$G_\mathbb Q$ は $\Omega$ に係数作用・$\beta^{1/n}$ 固定 | **当工房の規約** | 閉 |
| | (TB3) | $\pi_1(U_{\bar{\mathbb Q}},\vec{01})=\hat F_2=\langle x,y\rangle$ | 標準事実 | **【GAP-TB】** |
| | (TB4) | $x=$ $(\zeta_n)$ が定める $\hat{\mathbb Z}(1)$ の生成元の像・作用は後合成 | 標準事実 | **【GAP-TB】(load-bearing)** |
| **較正** | (CAL) | $\alpha^{\rm Ih}=\alpha^{\rm std}$ | 証明済 | **閉**($A_5$ v4 §1.4・窓非依存) |
| **窓** | (W1) | $\bar N$ 開・$G_\mathbb Q$-安定 | 正典 | 窓ごと |
| | (W2) | 完全列 + $\tilde\chi\circ\mathrm{Ih}=\chi_{2M}$ | 正典 | 窓ごと |
| | (W3) | $N_P(H)=H$ | 有限計算 | 窓ごと |
| | (W4) | $\langle X\rangle$ が $P/H$ 上推移的・$[P:H]=M$ | 有限計算 | 窓ごと |
| | (W5) | $\Lambda$ が $\Phi(\mathfrak F_0)$-安定 | 有限計算 | 窓ごと |

**$R^{\rm cyc}$(系 B-7′)にはこれに 2 本足す**: **(2)** $\mathfrak F_0\cong C_e,\ e\mid M$(正典)/ **(F)** $\rho_0$ が忠実(有限計算)。

**$u$ を数値で得るにはさらに**: **(R-1)(R-2)** モデル認識証明書(命題 B-9)+ 局所展開の計算。

### 13.2 消えた前件(v3.1 からの差分)

| v3.1 | 扱い |
|---|---|
| (4)「明示 $\mathbb Q$-モデル」 | **削除**。(W3)(W5) から存在と一意性が**導かれる**(定理 B-4) |
| (4)「$\mathbb Q$-有理な全分岐 cusp」 | **削除**。(W4) から**導かれる**(補題 B-5(i)) |
| (4)「actual marked identification」 | **橋の外へ移動**(命題 B-9 の (R-2)) |
| (5) FC-3 | **削除**。(W3)(W5) から**導かれる**(系 B-4c) |
| (5) FC-2b | **残る**(= (CAL))。ただし既に証明済・窓非依存 |
| (3)「$\mathrm{ord}(X)=\lvert\Lambda\rvert=M$・単純推移」 | **(W3)+(W4) に分解**(命題 B-2 で同値) |

### 13.3 五札(v3.1 §5.2.5)の改訂案

| 札 | v3.1 | **改訂** |
|---|---|---|
| **FORMAL-IN** | $(0)(1)(2)(3)(5')(6')$ | 不変(ただし $(3)$ は (W3)(W4) と読む) |
| **BRIDGE-IN** | 明示モデル・cusp・助変数・marking・FC 規約 | **(W1)–(W5) + (CAL) + (TB1)–(TB4)**。**「明示」の語は全部落ちる** |
| **BRIDGE-FAIL** | BRIDGE-IN を満たすのに (7.3) 破れ | **意味が変わる**: (W1)–(W5) を満たすのに (9.1) が破れたら、それは**定理 B-7 の証明の誤り**(= `proof consistency failure`)。**橋の「実験的反証」はもう存在しない** — 橋は定理になったから |
| **BRIDGE-UNKNOWN** | 比較が閉じられない | **入口は 2 つだけ**: (i) **(W5) 不成立**(⇒ $K$-モデルなし・SCHEMA-OUT へ)、(ii) **【GAP-TB】が破れる**(枠組みの誤り) |
| **SCHEMA-OUT** | regular detector 不在等 | 不変 + **(W3) 不成立**($N_P(H)\ne H$)を明示追加 |
| **【新】MODEL-MISMATCH** | — | **(R-1)(R-2) の証明書が取れない / 取れたのに $u_C$ が別値** ⇒ モデル認識の失敗であって橋の反証ではない |

> **★ 運用への含意(重要)**: $K^{(5)}$ の封印は「$B_{\rm FC}$ が架かるか」を試す実験だと位置づけられてきたが、**本稿が正しければそれは試験にならない**。$K^{(5)}$ が実際に試すのは
> (i) **(W1)–(W5) の有限検査**(封印前に済ませられる)、
> (ii) **モデル認識 (R-1)(R-2)**、
> (iii) **$u$ の抽出の二経路一致**、
> (iv) **$\mathrm{ord}([u^{-1}]_{10})=5$ か否か**(= $R^{\rm cyc}$ の予測)
> の 4 つである。**(iv) だけが本当の予測**であり、そこが外れたら疑うべきは(橋ではなく)**私の証明か、(W#) の検査か、$u$ の抽出**である。**司令塔の裁定を要する運用変更**なので §14 に上げる。

---

## 14. Sol への論点(優先順)

1. **【必須】§6 定理 B-4 の cocycle 自動性**(自己申告 A-1)。$\hat F_2\rtimes G_K$ の積の向き・$\alpha$ が左作用であることを含め、(6.1) → cocycle の 3 行を独立に再構成してほしい。**偽なら $B_{\rm FC}$-II-a が落ち、明示モデルが前件に戻る。**
2. **【必須】§8 補題 B-6 の 1**(自己申告 A-2)。(TB4) から $x\cdot p=m(\zeta_M)p$ を出す段。**ここが $b=1$ の全根拠**である。**偽でも系 B-8 で単一窓の結論は救われるが、$K^{(5)}$ の $a_{\rm eff}$ には効く。**
3. **【必須】定理 B-3 の射程**。補題 $R'$ を $\mathfrak F_0$ でなく $\mathrm{Ih}_N(G_K)$ に適用してよいか(私は (W2) から $\mathrm{Ih}_N(G_K)\subseteq\mathfrak F_0$ を使った)。**「(5′) の型は無料」という本稿最大の主張の根拠。**
4. **【推奨】命題 B-2 の同値**($\langle X\rangle$ 推移 + $\lvert\Lambda\rvert=M$ $\iff$ $N_P(H)=H$)。v3.1 (3) の分解が正しいか。
5. **【推奨】命題 B-9 の素描**。「3 点球面の標準生成三つ組は同時共役を除き一意」を私は証明していない(pure mapping class group の自明性に依拠)。**これは【文献要請 13】に含めるべきか、別立てか。**
6. **【推奨】§13.3 の五札改訂**、とくに「BRIDGE-FAIL がもう存在しない」という主張。**橋が定理になったら、$K^{(5)}$ は何を試すのか** — Sol の見解を求む。
7. **【共同設計者への発案要請】** 定理 B-7 の前件から (W3)($N_P(H)=H$)を外せるか。外せれば $\mathrm{Aut}_U(W)\ne1$ の窓(dessin に自己同型がある窓)まで射程が伸びる。私は descent の cocycle 条件が $H^2(G_K,N_P(H)/H)$ の障害に化けると見ているが、**$N_P(H)/H$ が可換なら $H^1$ の捻れで済み、しかも $\mathrm{Fib}\to\Lambda$ が $\lvert N_P(H)/H\rvert:1$ になるだけ**かもしれない。**この一般化に価値があるか、そもそも該当窓が族にあるか**を問いたい。

---

## 15. 司令塔への提案

1. **札の更新**: 【GAP-Rcyc】= $B_{\rm FC}$ を `candidate/UNKNOWN` → **`paper-proof (framework-conditional) / single-mathematician`**。二人監査で PASS すれば `paper-proof / two-mathematician audit PASS`。
2. **【GAP-C3】と【GAP-TB】の統合**: 同じ札である。**(TB4) 単独が load-bearing** という本稿の同定を札に書き込む。
3. **【文献要請 13】**(§12.1)を関所へ。優先度中。
4. **$K^{(5)}$ 運用の再検討**(§13.3 の★): 封印が試す対象が変わる。**凍結 1/2 の内容自体は変更不要**(むしろ (R-1)(R-2) と $u$ 抽出に集中するのが正しい)だが、**「$K^{(5)}$ で $B_{\rm FC}$ を試す」という位置づけの文言**は裁定で更新すべき。
5. **検算の恒久化**: `search/week4-bfc-antecedents.mjs`(13/13)。**V6・V7 は定理 K3 §2.2 (P7) への独立な第二証明**でもあるので、`provenance/LEDGER.md` へ。
6. **可視化**: 「shadow 類 = Belyi 類」という一行と、$B_{\rm FC}$-I/II-a/II-b/II-c の 4 枚分解は図にすると効く(🌒 の拡張候補)。

---

## 16. ★教材(本稿で学んだこと)

1. **「未証明の橋」は分解すると型の段と同定の段に割れ、型の段は無料であることが多い。** $B_{\rm FC}$-I は既に手元にあった補題 $R'$ の別の適用先にすぎなかった。**同じ補題を二度使えることに気づかないと、未証明部を過大に見積もる。**
2. **「明示モデル」は前件ではなく計算手段である。** 存在と一意性が言えれば橋は架かる。両実例が明示モデルから出発したので、それが前件に見えていた。**出発点と前件を混同しない。**
3. **規約の自由度は、同じ規約を二度使うと消える。** $b$ は「$x$ の向き」と「$\kappa$ の値」の両方を $(\zeta_n)$ が決めるので相殺する。**独立に見える二つの規約が同一起源かを必ず問う。**
4. **前件の非自明性は数えて確かめる。** (W5) は「$\mathrm{Aut}(P)$ の 1296 元のうち 432 元」という**明確に非自明な**条件だった(V7)。「たぶん成り立つ」で済ませていたら、族の一般化で最初に破れる項目を見逃していた。
5. **橋が定理になると falsifier の宛先が消える。** ★教材 12(便 29)の裏面: **未証明部を証明したら、五札の BRIDGE-FAIL は空になり、代わりに `proof consistency failure` と MODEL-MISMATCH に置き換わる。** 実験の意味づけを同時に更新しないと、「何も試していない試験」を走らせることになる。
6. **枠組み札は「粗いまま放置」ではなく「項目に割って load-bearing を名指し」する。**【GAP-C3】→ (TB1)–(TB4) → **(TB4) だけ**。同じ未閉鎖でも、次に何を取りに行くかが決まる。

---

## 付録 A. 記号表(本稿で新規に導入したもの)

| 記号 | 型 | 定義 |
|---|---|---|
| $\tilde H$ | $\hat F_2$ の開部分群 | $\pi^{-1}(H)$ |
| $\tilde\Lambda$ | 有限集合 | $\tilde H$ の $\hat F_2$-共役全体($\cong\Lambda$) |
| $m$ | $\mu_M\to\mathrm{Sym}(\mathrm{Fib})$ | (7.1) の乗法作用($\mu_M$-torsor 構造) |
| $c$ | $G_K\to\mu_M$ | (5.1)。**定理 B-3 で無条件に存在** |
| $\mathfrak s(N,H)$ | $K^\times/K^{\times M}$ | **shadow 類** $=[c]$(5.2) |
| $c_\Lambda$ | $\mathrm{Fib}\xrightarrow{\sim}\Lambda$ | 系 B-4c(= FC-3)の同型 |
| $\tilde s$ | $K[[s]]$ の uniformizer | $s\,h^{1/M}$、$\tilde s^M=u^{-1}\beta$(補題 B-5(iii)) |
| $b$ | $(\mathbb Z/M)^\times$ | $c_\Lambda m(\zeta_M)c_\Lambda^{-1}=\tau(\zeta_M^{b^{-1}})$ で定義。**補題 B-6 より $b=1$** |

## 付録 B. 番号つき主張の一覧(機械照合用)

| # | 主張 | 検算 |
|---|---|---|
| **B-1** | regular 可換部分群は $\mathrm{Sym}$ 内で自己中心化 | 紙上(3 行) |
| **B-2** | $\langle X\rangle$ 推移 + $\lvert\Lambda\rvert=\mathrm{ord}(X)$ $\iff$ $N_P(H)=H$、かつ $P/H\cong\Lambda$ | **V3・V4** |
| **B-3** | $B_{\rm FC}$-I: $c\in\mathrm{Hom}(G_K,\mu_M)$ の存在と一意性 | **V5**(前件)・紙上 |
| **B-4** | 剛性 descent: $K$-モデルの存在と一意性 | **V2・V5・V6** |
| **B-5** | 局所 Kummer: $\mathrm{Fib}$ の Kummer 表示と torsor 類 $[u^{-1}]$ | 紙上($A_5$ §3.5 と逐語一致) |
| **B-6** | torsor 比較・$b=1$ | 紙上 |
| **B-7** | **$B_{\rm FC}$**: $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(\kappa_{u^{-1}}(\gamma))$ | 二例で逐語一致(§11) |
| **B-7′** | 族定理 $R^{\rm cyc}$(前件 7 本) | — |
| **B-8** | $b$-頑健性 | **V8** |
| **B-9** | モデル認識(素描・【GAP-TB】相乗り) | $A_5$ (3.3)・$K^{(3)}$ (P4) |
