# Week 4 — 【GAP-E2】正面 作戦計画 v2

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 09**。
**v1(`docs/week4-E2作戦_v1.md`)は残す**。本稿は v1 の §1.2–§1.6・§F-1 を**置き換えず補強**し、Sol 便 12(`sol/sol_reply_12_e2.md`)の F4/F6/F8/F9/F10 と裁定 12 の指示に応える。
依存: `sol/sol_reply_12_e2.md`(便 12)・`sol/裁定_12_e2.md`・`docs/week4-E2作戦_v1.md`・`docs/week3-狩場計画_v4.md`(T2・命題 E1・系 E2′-a)・`docs/week1-定義ノート.md` v2。
検算スクリプト(**共有ツリーに開示・監査対象**): `docs/scout/class4.mjs`・`docs/scout/rational4.mjs`・`docs/scout/witness4.mjs`(v1 の 21 点計算)・**`docs/scout/metab.mjs`(本稿の新規・自由 metabelian 塔の厳密モデル)**。

---

## 0. 冒頭結論

| # | 内容 | 札 |
|---|---|---|
| **D1** | **定理 E9′ の中心恒等式 (†) は紙で閉じた**。21 点補間は**不要になった**。(†) は二つの補題 — **Lemma A**: $\mathcal N(pq) = \rho^3$($\rho := r_1r_2r_3$、**$m$ に依らない**)、**Lemma B**: $3E_m = -T_m\kappa_m + B_m\rho$ — に完全に還元し、両方を手計算で証明した(§1) | **紙上証明**(Opus 単独・Sol 未監査)。**全定数を `docs/scout/` の独立スクリプトが再現** |
| **D2** | **命題 E10 の全称版に lift 補題を追加**(便 12 F6 の指示どおり一行)。$(\mathbb Z/n)^\times \to (\mathbb Z/n')^\times$ の全射性を CRT で証明(§2) | **紙上証明**(3 行) |
| **D3** | **★ 命題 E16(捻れ無しの崩壊)**: $\theta$ が $A^\sigma$ を保つ(= $\iota_{X^u}\vert_A = \mathrm{id}$)なら、E2 の torsion 条件は **$\theta(E_m) = E_m^{-1}$ ただ一つ**と同値。系 E2′-a より $\iota_{X^u}\vert_A = \mathrm{id} \iff \mathrm{class}(P)\le2$。⇒ **障害は $S_3$-加群構造ではなく内部捻れ $\iota_{X^u}$ が担う**(§3.1)。便 12 の「$\mathbb Z_2[\langle\sigma,\theta\rangle]$-加群構造で特徴づけよ」という枠組みは、**$\langle\sigma,\theta\rangle$ が $S_3$ でない**ため直接には成立しない | **紙上証明**+H6 の別証明として整合 |
| **D4** | **★ 定理 E18(次数付き障害)**: $\iota_{X^u}$ は $\mathrm{gr}_j(A)$ 上**恒等**に作用するので、**associated graded の上でだけ $\langle\bar\sigma,\bar\theta\rangle$ は真に $S_3$ になる**。障害は (i) $\sigma$-非自明イソタイプ $M_j^-$ からは**決して来ない**($M_j^-$ は $\langle\theta\rangle$-コホモロジー的自明 — crossed product $\mathbb Z_2[\omega]*C_2\cong M_2(\mathbb Z_2)$)、(ii) すべて $M_j^+ = \mathrm{gr}_j(A)^{\bar\sigma}$ に載り、$O_j := (1+\bar\theta)\vert_{M_j^+}$ で測る。**$O_j = 0 \iff \mathrm{gr}_j$ に $S_3$ の自明表現が現れない**(§3.2) | **紙上証明** |
| **D5** | **★★ 自由 Lie 環での初出は weight 5**: $L_j(V)$($V$ = $S_3$ の 2 次元標準表現)における自明表現の重複度は $j = 2,3,4$ で **0**、$j = 5$ で **1**。⇒ **class ≤ 4 が無条件に安全な理由の表現論的説明**(定理 E9/E9′ の再証明)であり、**class 5 が第一の生きた層であることの独立な構造的根拠**(§3.2・表) | **紙上証明**(自由 Lie 環の指標公式)+ `docs/scout/` で数値照合 |
| **D6** | **★★★ 定理 E19: 自由 metabelian 塔 class ≤ 7 では 2-一次障害は存在しない**。厳密 Smith 標準形の**基本因子が全て奇数**($m = 0..63$・class $3..7$)⇒ **$\mathbb Z_2$-可解 ⟺ $\mathbb Q$-可解**。すなわち「mod $2^j$ で新たに現れる可除性障害」は**この範囲では原理的に起こらない**。$\mathbb Q$-可解性も $m\le63$ で成立 ⇒ **全ての $j$ で可解**。さらに **Lucas による $m\bmod 8$ 周期性**で「基本因子が全て奇数」は **class ≤ 7 の全ての $m\in\mathbb Z$** へ拡張される(系 E19-b)(§3.3) | **単系統**(`docs/scout/metab.mjs`・厳密 BigInt・自己検査 13 項 PASS)。**cross-checked ではない** |
| **D7** | **便 12 の ★ を部分的に修正**: 「残り得る障害はむしろ 2-一次」は、**metabelian 塔 class ≤ 7 では成り立たない**(D6)。残る障害は $\mathbb Q$-線型の問題か、**$A$ 非可換(導来長 ≥ 3)**の領域である | **本稿の主張**(射程つき) |
| **D8** | **★ 定理 E21: 系 E12-a は非可換 2 群では常に空虚**。$\gamma_3[A,A]A^2$ による商 $A/B\cong\mathbb F_2$ が**必ず** $\langle\sigma,\theta\rangle$-自明加群になる($\sigma(w)\equiv w\ (\gamma_3)$、$\theta(w)=w^{-1}\equiv w\ (A^2)$)ので、非自明な同時安定 1 次元指標が常に存在する。⇒ E12-a を安価な safe criterion として使う道は**本設定では閉じている**(§3.4) | **紙上証明** |
| **D9** | **掃引宇宙 v2 の登録表**(新 ID・既存上書き禁止・3 層)を §4 に固定。**発射順は Sol の F14 どおり**①完全 class-5 非 metabelian ②metabelian class-6 記号的 SNF(**D6 により事実上完了・残るのは $m$ 量化子**)③有限群掃引 | **事前登録** |

★ **一行でいうと**: (†) は紙で閉じ、E15 の「2-一次障害」仮説は **metabelian 塔 class ≤ 7 では反証された**(基本因子が全て奇数)。障害が残り得るのは **$A$ 非可換**の領域だけであり、そこでは線型モデル自体が使えない。**狩場は導来長 ≥ 3 に一点集中する。**

---

## 1. 定理 E9′ の中心恒等式 (†) — **紙上証明**(便 12 F4 / W98 への応答)

### 1.0 Hall 座標の正本(監査用・開示形)

自由 class-4 rank-2 冪零群 $F_2/\gamma_5$、$A_{\mathrm{free}} := \gamma_2/\gamma_5 \cong\mathbb Z^6$。**基底の順序を固定する**(以後この順序を正本とする):

$$ w := [x,y],\quad p := [w,x],\quad q := [w,y],\quad r_1 := [p,x],\quad r_2 := [p,y],\quad r_3 := [q,y]. $$

重み: $w$ は 2、$p,q$ は 3、$r_1,r_2,r_3$ は 4。$A$ は可換(補題 E8.0)。$\gamma_4 = \langle r_1,r_2,r_3\rangle$ は $P$ の中心に入る。**Jacobi**: $[q,x] = r_2$。以後 $A$ を**加法的**に書く。

**構造定数(全て手計算で導出・§1.1–§1.2 で証明。`docs/scout/class4.mjs` が独立に再現)**

$$
\theta:\quad w\mapsto -w,\quad p\mapsto -q,\quad q\mapsto -p,\quad r_1\mapsto -r_3,\quad r_2\mapsto -r_2,\quad r_3\mapsto -r_1.
$$
$$
\tau:\quad w\mapsto w-p+r_1,\quad p\mapsto q-r_2,\quad q\mapsto -p-q+2r_1+2r_2+r_3,
$$
$$
\qquad r_1\mapsto r_3,\quad r_2\mapsto -r_2-r_3,\quad r_3\mapsto r_1+2r_2+r_3.
$$
$$
\sigma_m = \mathrm{Ad}(\bar Y^{m})\circ\tau:\quad
w\mapsto w-p+mq+r_1-mr_2+\tbinom m2 r_3,\quad
p\mapsto q-r_2+mr_3,
$$
$$
\qquad q\mapsto -p-q+2r_1+(2-m)r_2+(1-m)r_3,\qquad \sigma_m\vert_{\gamma_4} = \tau\vert_{\gamma_4}.
$$

> **記法.** $\rho := r_1+r_2+r_3$、$T_m := \binom{m+1}2 = \frac{m(m+1)}2$、$B_m := \binom{T_m+1}2 = \frac{T_m(T_m+1)}2$、$\kappa_m := \mathcal N(w)$、$\mathcal N := 1+\sigma+\sigma^2$。

**$\theta$ の一言**: $\theta = -s$、ここで $s$ は基底の対合 $(w,p,q,r_1,r_2,r_3)\mapsto(w,q,p,r_3,r_2,r_1)$。ゆえに
$$ \boxed{\ \ker(1+\theta) = \{v : v_p = v_q,\ v_{r_1} = v_{r_3}\} = \langle w,\ p+q,\ r_1+r_3,\ r_2\rangle\ } $$
は**階数 4 の直和因子**である。E9′ の witness $\bar f = w^{\lambda T_m}(pq)^{-\lambda^2B_m}$ は $\langle w, p+q\rangle$ に入るので (H-a) は自明に満たす。

### 1.1 補題の証明 — $\theta$ と $\tau$

**$\theta$**($x\leftrightarrow y$、$F_2$ の自己同型):
$\theta(w) = [y,x] = w^{-1}$ は**自由群の中で厳密**。$\gamma_3$ は $\gamma_2$ を中心化する($[\gamma_3,\gamma_2]\subseteq\gamma_5 = 1$)ので
$\theta(p) = [\theta w,\theta x] = [w^{-1},y] = ([w,y]^{-1})^{w^{-1}} = q^{-1}$、同様に $\theta(q) = p^{-1}$。
$\gamma_4$ は中心なので $\theta(r_1) = [\theta p,\theta x] = [q^{-1},y] = r_3^{-1}$、$\theta(r_2) = [q^{-1},x] = [q,x]^{-1} = r_2^{-1}$、$\theta(r_3) = [p^{-1},x] = r_1^{-1}$。∎

**$\tau$**: §1.3 の自由 metabelian モデル(§3.3)が同じ値を独立に与える(自己検査 4 項)。ここでは値のみ用いる。

### 1.2 **Lemma A** — $\mathcal N(p+q) = 3\rho$($m$ に依らない)

> **Lemma A.** 自由 class-4 対象において、**全ての $m$** に対し $\ \mathcal N(p+q) = 3(r_1+r_2+r_3) = 3\rho$。

**証明.**(全て $A$ の中の加法計算。$\gamma_4$ 上 $\sigma = \tau$。)
$$ \sigma(p+q) = (q - r_2 + mr_3) + (-p-q+2r_1+(2-m)r_2+(1-m)r_3) = -p + 2r_1 + (1-m)r_2 + r_3. $$
$$
\begin{aligned}
\sigma^2(p+q) &= \sigma(-p) + \sigma\bigl(2r_1+(1-m)r_2+r_3\bigr)\\
&= (-q + r_2 - mr_3) + \bigl(2r_3 + (1-m)(-r_2-r_3) + (r_1+2r_2+r_3)\bigr)\\
&= -q + r_1 + (1+m)r_2 + (2+m)r_3 .
\end{aligned}
$$
加えると $p,q$ 成分は打ち消し、
$$ \mathcal N(p+q) = (2+1)r_1 + \bigl((1-m)+(2+m)\bigr)r_2 + (1+2)r_3 = 3r_1+3r_2+3r_3 = 3\rho. \qquad\blacksquare $$

★ **$m$ が完全に消える**のが本補題の要点である。

### 1.3 **$\kappa_m$ の閉形**(手計算)

$\mathrm{Ad}(\bar Y^{m})$ は $\gamma_3$ 上 $g\mapsto g+m[g,y]$、$\gamma_4$ 上恒等、$w$ 上 $w\mapsto w+mq+\binom m2 r_3$($[w,y^k] = q^kr_3^{\binom k2}$ の帰納法)。ゆえに $\sigma(w)$ は上表のとおり。続けて
$$
\sigma^2(w) = \sigma(w)-\sigma(p)+m\sigma(q)+\sigma(r_1)-m\sigma(r_2)+\tbinom m2\sigma(r_3)
$$
を展開すると
$$ \sigma^2(w) = w-(1+m)p-q+\bigl(1+2m+\tbinom m2\bigr)r_1+(1+m)r_2+1\cdot r_3 $$
(係数の内訳: $r_2$ は $-m+1+m(2-m)+m+2\binom m2 = 1+m$、$r_3$ は $\binom m2 - m + m(1-m)+1+m+\binom m2 = 1$)。したがって
$$ \boxed{\ \kappa_m = 3w - (m+2)p + (m-1)q + \tfrac{m^2+3m+4}2\,r_1 + 1\cdot r_2 + \tfrac{m^2-m+2}2\,r_3\ } $$
特に **$\kappa_m$ の $r_2$-座標は $m$ に依らず $1$** である。

### 1.4 **Lemma B** — $3E_m = -T_m\kappa_m + B_m\rho$

> **Lemma B(補題 E9.2 の class-4 精密化).** 自由 class-4 対象において
> $$ \boxed{\ 3E_m \;=\; -T_m\,\kappa_m \;+\; B_m\,\rho\ },\qquad T_m = \tbinom{m+1}2,\ B_m = \tbinom{T_m+1}2 .$$

**証明は 4 段。**

**(B1) $E_m\in A^\sigma$、$\kappa_m,\rho\in A^\sigma$。**
$\tau(E_m) = \tau(X^mZ^mY^m) = Y^mX^mZ^m$、ゆえに
$\sigma(E_m) = \bar Y^{-m}(Y^mX^mZ^m)\bar Y^{m} = X^mZ^mY^m = E_m$。(一行。)
$\sigma^3 = \mathrm{Inn}_A(E_m) = \mathrm{id}$($A$ 可換)より $\sigma\mathcal N = \mathcal N$、ゆえに $\kappa_m = \mathcal N(w)\in A^\sigma$。
$\rho$: $\tau\vert_{\gamma_4}$ の不動空間は $ar_1+br_2+cr_3\mapsto cr_1+(-b+2c)r_2+(a-b+c)r_3$ を等置して $a=b=c$、すなわち $\langle\rho\rangle$。

**(B2) $\dim_{\mathbb Q}A^\sigma = 2$、したがって $A^\sigma\otimes\mathbb Q = \mathbb Q\kappa_m\oplus\mathbb Q\rho$。**
フィルトレーション $A\supseteq\gamma_3\supseteq\gamma_4$ に対し $\dim\ker(\sigma-1)\le\sum_j\dim\ker(\bar\sigma-1)\vert_{\mathrm{gr}_j}$。
$\mathrm{gr}_2 = \langle w\rangle$: $\bar\sigma = \mathrm{id}$、次元 1。
$\mathrm{gr}_3 = \langle p,q\rangle$: $\bar\sigma(p)=q,\ \bar\sigma(q)=-p-q$、特性多項式 $\lambda^2+\lambda+1$、固有値 1 を持たない、次元 0。
$\mathrm{gr}_4$: (B1) より次元 1。
合計 $\le 2$。一方 $\kappa_m$($w$-係数 $3\ne0$)と $\rho\in\gamma_4$ は一次独立な $\sigma$-不動ベクトルなので**ちょうど 2**。∎

**(B3) $w$-座標 ⇒ 比例係数。** (B2) より $E_m = a\kappa_m + b\rho$($a,b\in\mathbb Q$)。$\rho\in\gamma_4$ なので $w$-座標を比べて、$E_m\equiv w^{-T_m}\ (\mathrm{mod}\ \gamma_3)$(定理 H6 の内容。§1.5 に独立導出)と $\kappa_m$ の $w$-座標 $3$ から
$$ -T_m = 3a,\qquad a = -T_m/3. $$

**(B4) $r_2$-座標 ⇒ $b$。** $\kappa_m$ の $r_2$-座標は $1$(§1.3)、$\rho$ の $r_2$-座標は $1$。よって
$$ (E_m)_{r_2} = -\tfrac{T_m}3 + b . $$
§1.6 で **$(E_m)_{r_2} = \binom{m+2}4$** を Magnus 係数の手計算で示す。すると
$$ 3b = 3\tbinom{m+2}4 + T_m . $$
初等恒等式
$$ 3\tbinom{m+2}4 = \frac{(m+2)(m+1)m(m-1)}{8} = \frac{T_m(T_m-1)}2 = \tbinom{T_m}2 $$
(∵ $T_m = \frac{m(m+1)}2$、$T_m-1 = \frac{(m+2)(m-1)}2$)より
$$ 3b = \tbinom{T_m}2 + T_m = \frac{T_m(T_m-1)}2 + T_m = \frac{T_m(T_m+1)}2 = B_m . $$
ゆえに $3E_m = 3a\kappa_m + 3b\rho = -T_m\kappa_m + B_m\rho$。∎

### 1.5 $E_m\equiv w^{-T_m}\pmod{\gamma_3}$(H6 の独立導出・1 行)

$E_m = x^m(xy)^{-m}y^m$。$\mathrm{mod}\ \gamma_3$ で $(xy)^m \equiv x^my^mw^{-\binom m2}$(Hall–Petrescu の 2 段目)ゆえ
$E_m \equiv x^mw^{\binom m2}y^{-m}x^{-m}y^m = w^{\binom m2}[x^{-m},y^m] = w^{\binom m2 - m^2} = w^{-T_m}$。∎

### 1.6 $(E_m)_{r_2} = \binom{m+2}4$ — Magnus 係数による手計算

Magnus 埋め込み $x\mapsto1+\xi$、$y\mapsto1+\eta$、$\mathbb Z\langle\xi,\eta\rangle/(\deg>4)$。$c_u(\cdot)$ で語 $u$ の係数を表す。**選ぶ語は $u_0 := \xi^2\eta^2$。**

**(a) 次数 4 の Lie 元での $u_0$-係数.**
$\ell_1 = [[[\xi,\eta],\xi],\xi] = 3\xi\eta\xi^2-\eta\xi^3-3\xi^2\eta\xi+\xi^3\eta$、
$\ell_2 = [[[\xi,\eta],\xi],\eta] = 2\xi\eta\xi\eta-\xi^2\eta^2-2\eta\xi\eta\xi+\eta^2\xi^2$、
$\ell_3 = [[[\xi,\eta],\eta],\eta] = \xi\eta^3-3\eta\xi\eta^2+3\eta^2\xi\eta-\eta^3\xi$。
ゆえに $c_{u_0}(\ell_1) = c_{u_0}(\ell_3) = 0$、**$c_{u_0}(\ell_2) = -1$**。$r_i$ の Magnus 像は $1+\ell_i$。

**(b) 補正項の $u_0$-係数.** $\mu(g) = \mu(w)^\alpha\mu(p)^\beta\mu(q)^\gamma\prod\mu(r_i)^{\delta_i}$ の次数-4 成分は
$$ G_4 = \alpha W_4 + \tbinom\alpha2 W_2^2 + \beta P_4 + \gamma Q_4 + \delta_1\ell_1+\delta_2\ell_2+\delta_3\ell_3 $$
($W_2 = [\xi,\eta]$、$W_k,P_k,Q_k$ は $\mu(w),\mu(p),\mu(q)$ の次数-$k$ 成分。$\mu(p),\mu(q)$ に次数 1,2 成分は無いので交叉項は出ない)。
$\mu(w) = (1+\xi)^{-1}(1+\eta)^{-1}(1+\xi)(1+\eta)$ の語は $\xi^a\eta^b\xi^c\eta^d$($c,d\le1$、符号 $(-1)^{a+b}$)の形。$u_0 = \xi^2\eta^2$ を与えるのは $(a,b,c,d) = (2,2,0,0)$(符号 $+$)と $(2,1,0,1)$(符号 $-$)の 2 通りで相殺 ⇒ **$c_{u_0}(W_4) = 0$**。同じ数え方で $c_{\xi\eta^2}(\mu(w)) = 0$、$c_{\xi^2\eta}(\mu(w)) = -1$。
$W_2^2 = \xi\eta\xi\eta-\xi\eta^2\xi-\eta\xi^2\eta+\eta\xi\eta\xi$ ⇒ **$c_{u_0}(W_2^2) = 0$**。
$\mu(p) = \mu(w)^{-1}(1+\xi)^{-1}\mu(w)(1+\xi)$: $u_0$ を 4 ブロックに切る分解を尽くすと生き残るのは 1 通りで、値は $-c_{\xi\eta^2}(\mu(w)) = 0$ ⇒ **$c_{u_0}(P_4) = 0$**。
$\mu(q) = \mu(w)^{-1}(1+\eta)^{-1}\mu(w)(1+\eta)$: 同様に生き残るのは 2 項、$c_{\xi^2\eta}(\mu(w)^{-1})\cdot(-1) = (+1)(-1) = -1$ と、$u_4 = \eta$ の場合の $(-1)+1 = 0$ ⇒ **$c_{u_0}(Q_4) = -1$**。
したがって
$$ \boxed{\ c_{u_0}\bigl(\mu(E_m)\bigr) = -\gamma - \delta_2\ }\qquad(\gamma = (E_m)_q,\ \delta_2 = (E_m)_{r_2}). $$

**(c) $c_{u_0}(\mu(E_m))$ の閉形.** $E_m = x^m z^m y^m$、$z = y^{-1}x^{-1}$。$\zeta := \mu(z)-1 = \sum_{(i,j)\ne(0,0)}(-1)^{i+j}\eta^j\xi^i$、
$$ \mu(E_m) = \Bigl(\sum_a\tbinom ma\xi^a\Bigr)\Bigl(\sum_k\tbinom mk\zeta^k\Bigr)\Bigl(\sum_d\tbinom md\eta^d\Bigr). $$
$\zeta^k$ の語は $\eta^{j}\xi^{i}$ 型ブロックの連接。$\xi^s\eta^t$ に等しくなるのは「純 $\xi$ ブロックが $s$ の合成、続いて純 $\eta$ ブロックが $t$ の合成」の場合だけ($\eta$ の後に $\xi$ が来るブロックは $\xi^s\eta^t$ の中に置けない)。符号は $(-1)^{s+t}$、個数は合成数 $\binom{s-1}{k_1-1}\binom{t-1}{k_2-1}$。よって $F(s,t) := c_{\xi^s\eta^t}\bigl(\mu(z)^m\bigr)$ は
$$ F(0,0)=1,\quad F(1,0)=F(0,1)=-m,\quad F(2,0)=F(0,2)=m+\tbinom m2,\quad F(1,1)=\tbinom m2, $$
$$ F(2,1)=F(1,2) = -\bigl(\tbinom m2+\tbinom m3\bigr),\quad F(2,2)=\tbinom m2+2\tbinom m3+\tbinom m4 . $$
$S := \binom m2$ と置き $c_{u_0}(\mu(E_m)) = \sum_{a,d\le2}\binom ma\binom md F(2-a,2-d)$ を展開すると
$$ c_{u_0}(\mu(E_m)) = S + 2\tbinom m3 + \tbinom m4 - 2m\tbinom m3 + 3S^2 - m^2S $$
$$ = S\Bigl[\tfrac{(m-1)(m-2)}2\Bigr] - \tfrac{2(m-1)\cdot m(m-1)(m-2)}6 + \tbinom m4
= m(m-1)(m-2)\cdot\frac{6(m-1)-8(m-1)+(m-3)}{24} = -\tbinom{m+1}4 . $$

**(d) 結論.** $\rho$ の $q$-座標は $0$、$\kappa_m$ の $q$-座標は $m-1$(§1.3)なので、(B2)(B3) から $E_m$ の $q$-座標は**新しい計算なしに**決まる:
$$ \gamma = (E_m)_q = a\,(m-1) = -\frac{T_m(m-1)}3 = -\frac{(m-1)m(m+1)}6 = -\tbinom{m+1}3 . $$
これと (b)(c) より
$$ \delta_2 = -\gamma - c_{u_0}(\mu(E_m)) = \tbinom{m+1}3 + \tbinom{m+1}4 = \tbinom{m+2}4 . \qquad\blacksquare $$

### 1.7 **定理 E9′ の証明**((†) の閉鎖)

> **定理 E9′.** $N$ 許容($c\in N$)、$P$ 2 生成・$\mathrm{class}(P)\le4$、$3\nmid\lvert A\rvert$。$\lambda := 3^{-1}\bmod\exp A$ と置くと
> $$ \bar f := w^{\lambda T_m}(pq)^{-\lambda^2B_m} $$
> は (H-a) と (H-b′) を同時に満たす。

**証明.** (H-a): $\bar f\in\langle w,p+q\rangle\subseteq\ker(1+\theta)$(§1.0)。
(H-b′): 加法的に $f_0 := 3T_m\,w - B_m\,(p+q)$ と置くと、$\mathcal N$ の $\mathbb Z$-線型性と Lemma A・Lemma B から
$$ \mathcal N(f_0) = 3T_m\kappa_m - B_m\cdot3\rho \overset{\text{Lem B}}{=} 3T_m\kappa_m - 3\bigl(3E_m + T_m\kappa_m\bigr) = -9E_m. $$
これが **(†)** である(**紙上で閉じた。21 点補間は不要**)。指数ベクトルを $\lambda^2$ 倍し $9\lambda^2\equiv1$、$3\lambda^2\equiv\lambda\pmod{\exp A}$ を使うと $\mathcal N(\bar f) = E_m^{-1}$。$P$ への押し出しは $A^P$ が $A_{\mathrm{free}}$ の $\theta,\sigma$-同変商であることによる。∎

> **系(無料で出る).** Lemma B と §1.3 の $\kappa_m$ から、$E_m$ の class-4 Hall 閉形が従う:
> $$ E_m = \Bigl(-\tbinom{m+1}2,\ \tbinom{m+2}3,\ -\tbinom{m+1}3,\ -\tbinom{m+3}4,\ \tbinom{m+2}4,\ -\tbinom{m+1}4\Bigr). $$

> **状態札(W60/W92)**: §1 は **紙上証明(Opus 単独・Sol 未監査)**。全構造定数・全恒等式は `docs/scout/class4.mjs` と `docs/scout/metab.mjs`(独立の 2 モデル: Magnus 切断代数 / 自由 metabelian 加群)が再現する。**verified(Lean)ではない。** 便 12 W98 が求めた「Hall 基底順・六座標・次数上界・21 点 residual・script hash」のうち、**次数上界と 21 点は不要になった**(恒等式が閉じたため)。Hall 基底順は §1.0、座標は §1.3 と §1.7 系、script は `docs/scout/` に開示。

---

## 2. 命題 E10 の補修 — charming residue の lift 補題(便 12 F6)

> **補題 E10.1(単元の持ち上げ).** $n'\mid n$ なら自然な還元 $(\mathbb Z/n)^\times\twoheadrightarrow(\mathbb Z/n')^\times$ は**全射**である。

**証明.** $u'\in(\mathbb Z/n')^\times$ を取り、$\gcd(a,n')=1$ なる整数 $a$ で代表する。$a+n't$ が $n$ と互いに素になる $t$ を作る。素数 $p\mid n$ について:
(i) $p\mid n'$ なら $p\nmid a$ かつ $p\mid n't$ ゆえ $p\nmid a+n't$(自動)。
(ii) $p\nmid n'$ なら $n'$ は $\bmod\ p$ で可逆なので $a+n't\equiv0\ (p)$ となる $t$ は $\bmod\ p$ でただ一つ。$p\ge2$ ゆえ避けられる。
(ii) の素数全体に中国剰余定理を適用して $t$ を選べば $\gcd(a+n't,n)=1$。∎

> **命題 E10(全称版・補修済).** $N\le N'$ をともに許容対象、$k := N_{\mathrm{ord}}$、$k' := N'_{\mathrm{ord}}$($k'\mid k$)。$N$ が**全ての charming $m$** で $m$-full(torsion 部)なら、$N'$ もそうである。

**証明.** charming $m\in\mathbb Z/k$ ↔ 単元 $u = 2m+1\in(\mathbb Z/2k)^\times$ は全単射($2k$ の単元は奇数)。$u'\in(\mathbb Z/2k')^\times$ を任意に取る。$2k'\mid2k$ ゆえ補題 E10.1 より $u'$ は $u\in(\mathbb Z/2k)^\times$ へ持ち上がり、$u$ は奇数だから $u = 2m+1$ なる charming $m$ を与える。$N$ が $m$-full なら E10-T(便 12 F6)より $N'$ は $m\bmod k'$ で torsion 解をもち、$2(m\bmod k')+1\equiv u'\pmod{2k'}$。∎

> **★ 便 12 F6/Errata 4 の遵守**: E10 が降ろすのは **torsion 解のみ**である。**生成条件は別判定**(E10-S は元の解が生成していた場合に限る)。「全商に生成 shadow がある」とは**書かない**。

---

## 3. 【中核】修正目標での E15 攻撃 — 2-一次障害の構造解析

**便 12 F9 の目標式**を出発点にする:
$$ (\ast)\qquad -\lambda E_m \;\in\; \ker(1+\theta) + (1-\sigma)A ,\qquad \lambda = 3^{-1}\bmod\exp A. $$

> **補題 E15.0(目標式と E8(iii) の同値 — 記録).** $A$ 有限可換・$3$ 可逆・$\sigma^3=\mathrm{id}$・$E_m\in A^\sigma$ とする。$e := \lambda\mathcal N$ は $A_+ := A^\sigma$ への冪等射影で $A = A_+\oplus A_-$、$A_- := \ker\mathcal N = (1-\sigma)A$。このとき
> $$ (\ast) \iff -E_m\in\mathcal N\bigl(\ker(1+\theta)\bigr) \iff E_m\in e\bigl(\ker(1+\theta)\bigr). $$

**証明.** $-\lambda E_m = b + c$($b\in\ker(1+\theta)$、$c\in A_-$)と書けたとする。$e$ を施すと $e(c)=0$、$-\lambda E_m\in A_+$ ゆえ $-\lambda E_m = e(b)$。逆に $-\lambda E_m = e(b)$ なら $-\lambda E_m - b = -(1-e)b\in A_-$。ゆえに $(\ast)\iff -\lambda E_m\in e(\ker(1+\theta))$。$\mathcal N = 3e$ と $3,\lambda$ が可逆であることから三者は同値。∎

### 3.1 命題 E16 — **捻れが無ければ問題は一行で崩壊する**

> **命題 E16.** $A$ 有限可換 2 群、$\sigma$ の位数 $\mid 3$、$\theta^2=\mathrm{id}$、$E_m\in A^\sigma$ とする。**$\theta(A^\sigma) = A^\sigma$** ならば
> $$ (\ast) \iff \theta(E_m) = E_m^{-1}. $$

**証明.** $\theta(A_+) = A_+$ なら $A_- = \ker\mathcal N$ も $\theta$-安定である($\theta\mathcal N\theta = 1+\theta\sigma\theta+\theta\sigma^2\theta = 1+\sigma^{-1}+\sigma^{-2} = \mathcal N$)。ゆえに
$$ \ker(1+\theta) = \bigl(\ker(1+\theta)\cap A_+\bigr)\oplus\bigl(\ker(1+\theta)\cap A_-\bigr), $$
$$ \mathcal N\bigl(\ker(1+\theta)\bigr) = 3\bigl(\ker(1+\theta)\cap A_+\bigr) = \ker(1+\theta)\cap A_+ $$
(最後の等号は $3$ が $A$ 上可逆ゆえ $3M = M$)。$E_m\in A_+$ だから $-E_m\in\mathcal N(\ker(1+\theta))\iff(1+\theta)E_m = 0$。∎

> **補題 E16.1($\theta$-安定性の正体).** 命題 E1(`docs/week3-狩場計画_v4.md` §3.1)$\ \theta\sigma\theta = \iota_{X^u}\sigma^{-1}$($\iota := \iota_{X^u}\vert_A$)より、$a\in A^\sigma$ に対し $\sigma(\theta a) = \theta(\iota a)$。ゆえに
> $$ \theta(A^\sigma)\subseteq A^\sigma \iff A^\sigma\subseteq C_A(X^u) . $$
> 特に $\iota = \mathrm{id}$、すなわち $X^u\in C_P(A)$ なら成立する。**系 E2'-a により $X^u\in C_P(A)\iff\mathrm{class}(P)\le2$。**

> **系 E16-a(H6 の torsion 部の別証明).** $\mathrm{class}(P)\le2$ なら $A = \langle w\rangle$、$E_m = w^{-T_m}$、$\theta(w) = w^{-1}$ ゆえ $\theta(E_m) = w^{T_m} = E_m^{-1}$。命題 E16 より $(\ast)$ 成立。∎

> **★★ 帰結(委嘱 09 §3(a) への直接回答・便 12 の枠組みの修正).**
> 委嘱は「$A$ の $\mathbb Z_2[\langle\sigma,\theta\rangle]$-加群構造($S_3$ の 2-modular 表現論)で特徴づけよ」と書いたが、**$\langle\sigma,\theta\rangle$ は $S_3$ ではない**。関係式は $\theta\sigma\theta = \iota_{X^u}\sigma^{-1}$ であり、**内部捻れ $\iota_{X^u}$ が消えるのは class $\le2$ に限る**(系 E2'-a)。したがって:
> - class $\le2$($S_3$-加群になる唯一の範囲): 命題 E16 で完全に閉じる。障害ゼロ。
> - class $\ge3$(生きた範囲): $\theta$ は $A^\sigma$ を保たず、$e$ と $\theta$ は**可換でない**($\theta e\theta = \lambda(1+\iota\sigma^{-1}+(\iota\sigma^{-1})^2)\ne e$)。**したがって 2-modular 表現論を $A$ そのものに適用する路線は入口が無い。**
> - 正しい入口は **associated graded**(§3.2)である — そこでは $\iota$ が消えて $S_3$-加群構造が回復する。

### 3.2 定理 E18 — 次数付き障害 $O_j$ と $S_3$ の 2-modular 構造

$P$ を 2 生成有限 2 群、$A = [P,P]$ **可換**(= $P$ metabelian)とし、$\gamma_j := \gamma_j(P)$、$M_j := \gamma_j/\gamma_{j+1}$($j\ge2$)と置く。

> **補題 E18.1(捻れは次数付きで消える).** $\iota_{X^u}$ は各 $M_j$ 上**恒等**に作用する。$\mathrm{Ad}(\bar Y^m)$ も同様。ゆえに $M_j$ 上では
> $$ \bar\sigma = \bar\tau,\qquad \bar\theta\bar\sigma\bar\theta = \bar\sigma^{-1},\qquad \bar\theta^2 = \bar\sigma^3 = 1, $$
> すなわち $\langle\bar\sigma,\bar\theta\rangle$ は**真に $S_3$ を通して作用する**。

**証明.** 任意の $g\in P$ について $(\iota_g-1)\gamma_j = [\gamma_j,g]\subseteq[\gamma_j,P] = \gamma_{j+1}$。$g = X^u$ でも $g = Y^m$ でも同じ。命題 E1 の右辺の $\iota_{X^u}$ が $M_j$ 上消えるので $S_3$ 関係式が回復する。∎

$3$ は $M_j$ 上可逆なので $M_j = M_j^+\oplus M_j^-$、$M_j^+ := M_j^{\bar\sigma}$、$M_j^- := \ker\bar{\mathcal N}$。この分解は $\bar\theta$-安定である。

> **補題 E18.2($\sigma$-非自明部分は障害を出さない).** $M_j^-$ は $\langle\bar\theta\rangle\cong C_2$ 上**コホモロジー的に自明**、すなわち $\widehat H^*(\langle\bar\theta\rangle, M_j^-) = 0$。したがって
> $$ \ker(1+\bar\theta)\vert_{M_j^-} = (1-\bar\theta)M_j^-,\qquad (M_j^-)^{\bar\theta} = (1+\bar\theta)M_j^- . $$

**証明.** $\bar\sigma$ は $M_j^-$ 上 $1+\bar\sigma+\bar\sigma^2 = 0$ を満たすので、$M_j^-$ は $R := \mathbb Z_2[\omega] = \mathbb Z_2[T]/(T^2+T+1)$ 上の加群である($R = W(\mathbb F_4)$ は $\mathbb Q_2$ の**不分岐**二次拡大の整数環)。$\bar\theta\bar\sigma\bar\theta = \bar\sigma^{-1}$ は $\bar\theta$ が $R/\mathbb Z_2$ の Galois 群(Frobenius)に沿って半線型であることを意味する。不分岐(étale)ゆえ Galois 降下により crossed product
$$ R*\langle\bar\theta\rangle \;\cong\; \mathrm{End}_{\mathbb Z_2}(R)\;\cong\;M_2(\mathbb Z_2) $$
であり、その単純加群は $R$ 自身のみ。**正規基底定理**(不分岐なので整基底で成立)より $R\cong\mathbb Z_2[\langle\bar\theta\rangle]$ が $C_2$-加群として自由。ゆえに任意の $R*\langle\bar\theta\rangle$-加群は $\mathbb Z_2[C_2]$-自由であり、Tate コホモロジーは消える(係数 $\mathbb Z/2^e$ でも同じ議論)。∎

> **定理 E18(障害の局在).** 逐次近似(重み $j$ ごとの補正)で $f$ を構成するとき、重み $j$ の段階での障害はただ一つの方程式
> $$ \bar\varepsilon_+ \;=\; \lambda\,(1+\bar\theta)\,\bar\delta \qquad\text{in } M_j^+ $$
> に集約される($\bar\varepsilon$ = 現在の $(1+\theta)$-欠損、$\bar\delta$ = 現在の $\mathcal N$-欠損)。$\bar\delta\in M_j^+$ は自動($\mathcal N f + E_m\in A^\sigma$)、$\bar\varepsilon\in M_j^{\bar\theta}$ も自動($(1-\theta)(1+\theta) = 0$)、$M_j^-$ 成分は補題 E18.2 により**常に**解消できる。したがって
> $$ \boxed{\ \text{潜在障害群}\quad O_j \;:=\; (1+\bar\theta)\bigl(M_j^{\bar\sigma}\bigr) \;\cong\; M_j^{\bar\sigma}\big/\ker(1+\bar\theta)\vert_{M_j^{\bar\sigma}}\ } $$
> であり、$O_j = 0 \iff \bar\theta$ が $M_j^{\bar\sigma}$ 上**反転($-1$)として作用する**。$M_j$ が捩れ自由(相対自由対象)なら、これはさらに **$M_j\otimes\mathbb Q$ に $S_3$ の自明表現が現れない**ことと同値である($M_j^{\bar\sigma}\otimes\mathbb Q$ は自明成分 $\oplus$ 符号成分で、$\bar\theta$ は前者で $+1$、後者で $-1$)。有限指数対象では「$\bar\theta = -1$ on $M_j^{\bar\sigma}$」が正本の判定条件で、上の表現論的判定はその**必要条件を与える持ち上げ**である。

**証明の骨子.** $\Psi_j: M_j\to M_j\oplus M_j$、$\bar g\mapsto((1+\bar\theta)\bar g,\ \bar{\mathcal N}\bar g)$ の像は、$\bar g = \bar g_++\bar g_-$ と分けて $\bar{\mathcal N}\bar g = 3\bar g_+$ ゆえ
$$ \mathrm{im}\,\Psi_j = \{(\lambda(1+\bar\theta)\bar\delta+\eta,\ \bar\delta) : \bar\delta\in M_j^+,\ \eta\in(1+\bar\theta)M_j^-\}. $$
$\bar\varepsilon$ の $M_j^-$-成分は $(M_j^-)^{\bar\theta} = (1+\bar\theta)M_j^-$(補題 E18.2)に入るので**自動的に解消**され、残るのは $M_j^+$-成分の等式のみ。最後の同値は、$\bar\theta$ が $M_j^+$ 上の対合であることから $(1+\bar\theta) = 0\iff\bar\theta=-1\iff$($M_j\otimes\mathbb Q$ の $S_3$-自明成分 $=$ $\bar\theta$ の $+1$ 固有部分 $= 0$)。∎

> **注意(状態札).** 定理 E18 は「**障害はここにしか載らない**」という**局在**の主張である。逆($O_j = 0\ \forall j\Rightarrow$ 可解)には、各段の持ち上げ($\bar g\in\ker(1+\bar\theta)$ を $\gamma_j\cap\ker(1+\theta)$ の元へ厳密に持ち上げる)の二次障害を制御する必要があり、**未閉鎖 =【GAP-E18】**。§3.3 は、metabelian 塔ではこの逆も事実上成立していることを計算で示す。

#### 表 1 — $S_3$ 表現論による $O_j$ の判定(自由対象)

$V$ = $S_3$ の 2 次元標準表現($x,y,z$ の張る空間 $/(x+y+z)$)、$\mathrm{sgn}$ = 符号表現。

**(a) 完全自由対象**: $M_j = L_j(V)$(自由 Lie 環の $j$ 次成分)。自由 Lie 環の指標公式 $\chi_{L_n}(g) = \frac1n\sum_{d\mid n}\mu(d)\chi_V(g^d)^{n/d}$、$\chi_V(1)=2,\ \chi_V(\tau)=-1,\ \chi_V(\theta)=0$ から:

| $j$ | 2 | 3 | 4 | **5** | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| $\dim L_j$ | 1 | 2 | 3 | 6 | 9 | 18 | 30 | 56 | 99 |
| 自明の重複度 | 0 | 0 | 0 | **1** | 1 | 3 | 4 | 9 | 15 |
| $\mathrm{sgn}$ の重複度 | 1 | 0 | 1 | 1 | 2 | 3 | 6 | 9 | 18 |
| $\dim M_j^{\bar\sigma}$ | 1 | 0 | 1 | 2 | 3 | 6 | 10 | 18 | 33 |
| **$O_j$** | $0$ | $0$ | $0$ | **$\ne0$** | $\ne0$ | $\ne0$ | $\ne0$ | $\ne0$ | $\ne0$ |

**(b) 自由 metabelian 対象**: $M_j \cong \mathrm{Sym}^{j-2}(V)\otimes\mathrm{sgn}$(§3.3 のモデルから直ちに従う: 加群は $\mathbb Z[S,T]$ の $j-2$ 次斉次部 $\times\,w$ であり、$\langle S,T\rangle\cong V$、$w$-直線は $\tau$-不変・$\theta$-反転ゆえ $\mathrm{sgn}$)。自明表現の重複度 $=\ \mathrm{Sym}^{j-2}V$ における $\mathrm{sgn}$ の重複度:

| $j$ | 2 | 3 | 4 | **5** | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| $\dim M_j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| $\dim M_j^{\bar\sigma}$ | 1 | 0 | 1 | 2 | 1 | 2 | 2 | 2 | 2 |
| **$O_j$** | $0$ | $0$ | $0$ | **$\ne0$** | $0$ | $\ne0$ | $\ne0$ | $\ne0$ | $\ne0$ |

(表 1(b) の $j\le7$ は `docs/scout/metab.mjs` が独立に再計算して一致。)

> **★★ 委嘱 09 §3(c) 前半への回答.**
> **どちらの塔でも「$S_3$ の自明表現の初出 = weight 5」である。** ゆえに
> 1. **class $\le4$ が無条件に安全なのは偶然ではない** — $L_2,L_3,L_4$ に自明表現が現れないという表現論的事実の帰結であり、定理 E9/E9' の明示 witness はその**具体形**にすぎない。便 12 F9 が要求した「$\theta$-同変な contracting homotopy」の骨格は、weight $\le4$ についてはこれで得られたことになる。
> 2. **class 5 が第一の生きた層である**ことに、掃引や数値実験と独立な**構造的根拠**が付いた(v1 の C5 は「$A$ 非可換になり得る最小 class」という別理由だった。**二つの独立な理由が同じ weight 5 を指す**)。
> 3. **ただし $O_j\ne0$ は「障害が起き得る」であって「起きる」ではない。** §3.3 が、metabelian 塔では実際には**起きない**ことを示す。

### 3.3 定理 E19 — **自由 metabelian 塔には 2-一次障害が存在しない**(class $\le7$)

#### 3.3.1 厳密モデル(`docs/scout/metab.mjs` — 開示形)

古典的事実(Magnus): rank 2 自由群 $F$ について $F'/F''$ は $\mathbb Z[F/F'] = \mathbb Z[s^{\pm1},t^{\pm1}]$ 上の**階数 1 の自由巡回加群**で、生成元は $w = [x,y]$、作用は $a^x = s\cdot a$、$a^y = t\cdot a$(paper 規約 $a^g = g^{-1}ag$)。$s = 1+S$、$t = 1+T$ と置くと $\gamma_j/(\gamma_{j+1}F'')$ は増大イデアル $I = (S,T)$ の $I^{j-2}/I^{j-1}$ に対応し、
$$ \boxed{\ A_c \;:=\; \gamma_2/(\gamma_{c+1}F'') \;\cong\; \mathbb Z[S,T]/(S,T)^{c-1},\qquad \mathrm{rank} = \tbinom c2 .\ } $$
辞書: $w = 1$、$p = S$、$q = T$、$r_1 = S^2$、$r_2 = ST\ (= [q,x])$、$r_3 = T^2$。写像は
$$ \theta:\ f\mapsto -f(T,S),\qquad
\tau:\ f(s,t)\mapsto f\bigl(t,(st)^{-1}\bigr)\cdot s^{-1},\qquad
\sigma_m = t^m\cdot\tau, $$
$$ E_m \;=\; c_m - s^{-m}A_m(s)A_m(st),\quad A_m(u) = 1+u+\cdots+u^{m-1},\quad c_m = t\,A_{m-1}(st)+t\,c_{m-1},\ c_1 = 0 $$
($c_m$ は $x^my^m = (xy)^mc_m$ で定まる Hall-Petrescu 元。導出は $[ab,c] = \beta[a,c]+[b,c]$、$[a,bc] = [a,c]+\gamma[a,b]$ の反復)。

**自己検査(スクリプトが 13 項すべて PASS)**: $\theta^2 = \tau^3 = \mathrm{id}$ / $\theta(w) = w^{-1}$ 厳密 / $\tau(w) = w-p+r_1$、$\tau(p) = q-r_2$、$\tau(q) = -p-q+2r_1+2r_2+r_3$(§1.0 の表と**一致**)/ $E_1,E_2,E_3$ の class-4 座標が `docs/scout/class4.mjs` と**一致** / **命題 E1** $\theta\tau\theta = \iota_x\circ\tau^{-1}$ / $\sigma_m(E_m) = E_m$($m\le6$)/ **Lemma A** $\mathcal N(p+q) = 3\rho$ / **Lemma B** $3E_m = -T_m\kappa_m+B_m\rho$($m\le12$)。

★ **この 13 項は、§1 の紙上証明と `docs/scout/class4.mjs`(Magnus 切断代数)の双方に対する独立照合になっている** — 二つのモデルは数学的に別物である(一方は非可換冪級数環の切断、他方は Laurent 多項式加群)。

#### 3.3.2 結果

$n := \binom c2$ 未知数、$2n$ 本の整数方程式
$$ (1+\theta)f = 0,\qquad \mathcal N f = -E_m $$
の係数行列 $M(m)$ の**整数 Smith 標準形**を厳密 BigInt で計算した。

| class $c$ | $\mathrm{rank}\,A_c$ | $m$ の範囲 | 全 $m$ で $\mathbb Z_2$-可解? | $\max_i v_2(d_i)$ |
|---|---:|---|---|---:|
| 3 | 3 | $0..63$ | **YES** | **0** |
| 4 | 6 | $0..63$ | **YES** | **0** |
| 5 | 10 | $0..63$ | **YES** | **0** |
| 6 | 15 | $0..63$ | **YES** | **0** |
| 7 | 21 | $0..63$ | **YES** | **0** |

(class 8 は 8GB 制約でヒープ超過 — `RAM 8GB constraint` に従い打ち切り。**UNKNOWN**。)

> **定理 E19.** 自由 metabelian rank-2 対象 $A_c$($3\le c\le7$)について、$0\le m\le63$ の全てで **Smith 基本因子 $d_i$ が全て奇数**であり、かつ系は $\mathbb Q$ 上可解である。ゆえに系は $\mathbb Z_2$ 上可解、すなわち**全ての $j$ について mod $2^j$ 可解**である。

> **系 E19-a(★ 便 12 の ★ への回答).** 基本因子が全て奇数であることは、Smith 標準形の可解性判定
> $$ Mx = b \text{ が }\mathbb Z_2\text{-可解} \iff \forall i\le\mathrm{rank}:\ v_2(c_i)\ge v_2(d_i),\ \ \text{かつ}\ \ \forall i>\mathrm{rank}:\ c_i = 0 \qquad (c = Ub) $$
> の第一条件を**恒真**にする。したがってこの範囲では
> $$ \boxed{\ \mathbb Z_2\text{-可解} \iff \mathbb Q\text{-可解}\ } $$
> であり、**「より高い 2 冪で初めて現れる可除性障害」(便 12 F8)は原理的に起こり得ない**。すなわち **metabelian 塔 class $\le7$ には 2-一次障害が存在しない。**

> **系 E19-b($m$ 量化子の部分閉鎖).** $M(m)\bmod2$ は $m$ について**周期的**である。実際 $\sigma_m$ の行列は $(1+T)^m$ の乗算行列(成分 $\binom mi$、$0\le i\le c-2$)と定数行列 $M_\tau$ の積で書け、$\mathcal N = 1+\sigma_m+\sigma_m^2$ の成分はそれらの $\mathbb Z$-係数多項式である。**Lucas の定理**より $\binom mi\bmod2$ は $i<2^L$ のとき $m\bmod2^L$ にしか依存しない。$c\le7$ では $c-2\le5<8$ ゆえ $L = 3$、すなわち
> $$ M(m)\bmod 2 \ \text{は}\ m\bmod 8\ \text{のみに依存する}. $$
> $m = 0..63$ は $\bmod\,8$ の全剰余を尽くすので、**「基本因子が全て奇数」は class $\le7$ の全ての $m\in\mathbb Z$ で成立する**。ゆえに残る問題は**純粋に $\mathbb Q$ 上の問題**であり、素数 2 は完全に落ちた。

> **系 E19-c(降下).** 命題 E10(§2)より、**2 生成 metabelian 2 群で class $\le7$ の許容対象は、$m\le63$ の全ての charming $m$ で torsion-full**(指数 $2^j$ は任意)。$m$ 量化子は $\mathbb Q$-可解性の側にのみ残る =【GAP-E19】。

> **状態札(厳守)**: 定理 E19 は **`docs/scout/metab.mjs` 単系統**(厳密 BigInt・自己検査 13 項)である。**cross-checked ではない**(GAP 側の SNF による第二系統が要る — §4 の作業指示 W-新 2)。**verified でもない。** 便 12 Errata 3 に従い `verified` の語は用いない。**札 = `Z2-solvable candidate (single system, self-checked)`。**

> **★ 便 12 の ★ の修正(D7)**: Sol は「残り得る障害はむしろ 2-一次である」と書いた。これは **metabelian 塔 class $\le7$ では成り立たない**(系 E19-a/b)。正確には:
> - **2-一次障害の潜在的な座席は存在する**($O_j\ne0$ at $j = 5,7,8,\dots$ — 定理 E18・表 1(b))。
> - **しかしその座席は空である**(基本因子が全て奇数)。潜在障害 $O_j$ は実現しない。
> - ゆえに **E15 の残る困難は (i) $\mathbb Q$ 上の $m$ 量化子、(ii) $A$ 非可換(導来長 $\ge3$)の領域**の二つに絞られる。

### 3.4 系 E12-a の適用範囲 — **非可換 2 群では常に空虚**(委嘱 09 §3(b) への回答)

> **命題 E20(E12-a の仮定の言い換え).** $A$ 有限群、$\sigma,\theta\in\mathrm{Aut}(A)$。1 次元指標に限れば
> $$ \{\rho\in\mathrm{Irr}(A) : \rho\circ\sigma = \rho,\ \rho\circ\theta = \rho,\ \dim\rho = 1\} \;=\; \bigl(A\big/\langle[A,A],\ (1-\sigma)A,\ (1-\theta)A\rangle\bigr)^\vee . $$
> ゆえに E12-a の仮定「同時 $\sigma,\theta$-安定な既約は自明のみ」は少なくとも
> $$ A = [A,A]\cdot(1-\sigma)A\cdot(1-\theta)A $$
> を要求する($A$ 可換なら $(1-\sigma)A+(1-\theta)A = A$ と同値)。

> **定理 E21(空虚性).** $P$ を**非可換**な 2 生成 2 群、$A = [P,P]$、$\sigma,\theta$ を本設定の自己同型とする。このとき **E12-a の仮定は決して満たされない。**

**証明.** $\gamma_3 = \gamma_3(P)$ は $P$ の特性部分群なので $\sigma,\theta$-安定。$B := \gamma_3\cdot[A,A]\cdot A^2$ と置くと $B$ も $\sigma,\theta$-安定で、$P$ が 2 生成ゆえ $\gamma_2/\gamma_3$ は $w = [X,Y]$ で生成される巡回群だから
$$ A/B \;\cong\; (\gamma_2/\gamma_3)\big/(\gamma_2/\gamma_3)^2 . $$
$P$ が非可換 2 群なら $\gamma_2\ne\gamma_3$(さもなくば冪零性より $\gamma_2 = 1$)ゆえ $\gamma_2/\gamma_3$ は非自明な有限 2 群、その Frattini 商は $\cong\mathbb F_2$。
作用: $\sigma(w)\equiv w\pmod{\gamma_3}$(∵ $\tau(w) = wp^{-1}$、$p\in\gamma_3$、かつ $\mathrm{Ad}(\bar Y^m)$ も $\gamma_3$ を法として恒等)、$\theta(w) = w^{-1}\equiv w\pmod{A^2}$。ゆえに **$A/B\cong\mathbb F_2$ は $\langle\sigma,\theta\rangle$ の自明加群**であり、その双対は $A$ の非自明な $\sigma,\theta$-不変 1 次元指標を与える。∎

> **帰結.** 便 12 P134 の系 E12-a は数学的には正しいが、**本設定の非可換 2 群には一度も適用できない**。「安価な safe criterion」として CLAIMS に登録するのは差し支えないが、**適用可能性 = 空**を併記すべきである。$3\mid\lvert A\rvert$ 側(Q7 型)や非 2 群では $A/B$ の位数が $\ne2$ になり得るので上の議論は通らず、別途検討の余地がある。

### 3.5 反例が出得る加群型と最小対象(委嘱 09 §3(c))

**(i) 排除された層(本稿までで確定)**

| 層 | 排除の根拠 | 札 |
|---|---|---|
| class $\le2$ | 命題 E16 + 系 E16-a(H6 の別証明) | 紙上証明 |
| class $\le4$(2 生成 2 群 $\Rightarrow$ $A$ 可換) | 定理 E9/E9'(§1・**紙で閉じた**)。構造的理由 = 表 1「自明表現の初出は weight 5」 | 紙上証明 |
| metabelian class $\le7$、$m\le63$、**全指数 $2^j$** | 定理 E19 + 系 E19-c | 単系統 candidate |
| metabelian 一般での**2-一次**障害(class $\le7$ の射程) | 系 E19-a/b | 単系統 candidate |

**(ii) 残る生きた層はただ一つ: $A$ 非可換(導来長 $\ge3$、class $\ge5$、$\lvert P\rvert\ge2^6$)**

ここでは (a) 命題 E8 の線型化が使えない、(b) 定理 E18 の次数付き解析も $A$ 可換を仮定している、(c) 定理 E19 のモデル($F'/F''$ 上の加群)がそもそも $[A,A]$ を潰している — **三つの武器が同時に失効する。**

**(iii) 反例が出得る「加群型」の特定**

$A$ 非可換のときの**最小の非自明化**は $[A,A]\ne1$ かつ $[A,A]\subseteq Z(P)$ である(自由 class-5 対象では $[A,A] = \langle[w,p],[w,q]\rangle\cong\mathbb Z^2\subseteq\gamma_5 = Z$)。すなわち **$A$ は class 2 の冪零群**で、$\mathcal N$ は準同型ではなく**次数 2 の多項式写像**になる。正確には:

> **補題 E22(class-2 $A$ における $\mathcal N$ の Hall-Petrescu 補正).** $[A,A]\subseteq Z(A)$ とする。$\mathcal N(f) := \sigma^2(f)\sigma(f)f$ に対し
> $$ \mathcal N(fg) \;=\; \mathcal N(f)\,\mathcal N(g)\cdot c(f,g),\qquad
> c(f,g) := \bigl[\sigma^2(g),\,\sigma(f)f\bigr]\bigl[\sigma(g),\,f\bigr]\ \in\ [A,A] $$
> であり、$c$ は $[A,A]$ に値をとる双加法的写像である。また $\mathcal B_\theta = \{f:\theta(f)=f^{-1}\}$ は部分群ではないが、$\bar A := A/[A,A]$ 上では $\ker(1+\bar\theta)$ に落ちる。

**証明.** $\sigma^2(fg)\sigma(fg)(fg) = \sigma^2(f)\sigma^2(g)\sigma(f)\sigma(g)fg$ を $\bigl(\sigma^2(f)\sigma(f)f\bigr)\bigl(\sigma^2(g)\sigma(g)g\bigr)$ の順へ並べ替えるとき、$\sigma^2(g)$ を $\sigma(f)f$ の右へ、$\sigma(g)$ を $f$ の右へ通す。生じる交換子は $[A,A]$ に入り中心的なので上の形になる。双加法性も $[A,A]$ の中心性から従う。∎

> **★ したがって $A$ 非可換の層での正しい定式化は「アフィン線型 + 中心的二次形式の値域判定」**である:
> 1. $\bar A = A/[A,A]$ 上で**線型判定**(これは定理 E18・E19 が扱う metabelian 対象そのもの)。
> 2. その解の**持ち上げ**の障害は $[A,A]$ 内の**二次的**条件になる(補題 E22 の $c(f,g)$)。
>
> **これが【GAP-E2】本丸の正確な姿**であり、v1 §3.3 の「route T 単系統(`twistedconjugacy` 全走査)」より遥かに構造が見える定式化である。§4 の W-新 1 に作業指示として起票する。

**(iv) 最小の許容対象の候補**

- **普遍側(最安・最優先)**: $F_2/\gamma_6$($A = \gamma_2/\gamma_6$、階数 12、$[A,A] = \langle[w,p],[w,q]\rangle$ 階数 2、中心)。**これが $A$ 非可換の最小の相対自由対象**であり、§3.3 のモデルの $c=5$ 版に $[A,A]$ を戻したものである。補題 E22 の二次形式で直接撃つのが最安の第一撃。
- **有限側**: $\lvert P\rvert\ge2^6$、class $\ge5$、**導来長 $\ge3$**、かつ $3\mid\lvert\mathrm{Aut}(P)\rvert$(位数 3 の $\tau$ を許容)。極大類 2 群($\lvert P\rvert\ge16$ の二面体・半二面体・一般四元数)は $\mathrm{Aut}$ が 2 群なので除外。$\lvert P\rvert = 64$ の class 5 は極大類ゆえ**除外**され、最小候補は $\lvert P\rvert\ge128$ になる。**正確な最小位数は UNKNOWN =【GAP-E20】**(§4 の掃引 (1) で決定する)。

---

## 4. 掃引宇宙 v2 の登録表(便 12 F14 / W103 / 裁定 12 の指示)

> **規律(絶対)**: 既存 `U-E2-2026-07-26`(v1 §3.1)は**事前登録記録として凍結したまま残す**。上書き・削除・射程変更は**しない**。以下は**新 ID** での再登録であり、v1 の宇宙を置き換えるものではない。**発射順だけを変える。**
> **W103 遵守**: E15 の定理も反例も出ていないので、**2 群を宇宙から除外しない**。除外するのは「紙で閉じた層」だけで、それは control として残す。

### 4.1 三層の宇宙 ID と発射順

Sol の F14/P139/P140 の順序を採用する。**各層は独立した universe ID を持ち、独立に凍結される。**

| 順 | universe ID | 層 | 何を撃つか | なぜここか |
|---|---|---|---|---|
| **①** | **`U-E2-nm5-2026-07-26`** | **完全 class-5・非 metabelian(普遍側)** | 相対自由対象 $F_2/\gamma_6$、$A = \gamma_2/\gamma_6$(階数 12・**非可換**・$[A,A]$ 階数 2 中心)。補題 E22 の**二次形式**で $\mathcal S_m\cap\mathcal B_\theta$ を直接判定 | **$A$ 非可換の最小の相対自由対象**。§3.5 (ii) より**唯一残った生きた層**。ここで $\mathbb Z_2$-不可解が出れば E15 は普遍レベルで反証される |
| **②** | **`U-E2-metab-2026-07-26`** | **metabelian 塔(記号的 SNF)** | 自由 metabelian class $c = 3..8$、$m$ 全域。**定理 E19 の第二系統照合**(GAP の SNF)+ $\mathbb Q$-可解性の $m$ 量化子を記号的に閉じる | **D6 により 2-一次側は事実上決着**。残るのは (i) 第二系統照合、(ii) $\mathbb Q$-可解性の全 $m$、(iii) class 8 以上(8GB でヒープ超過) |
| **③** | **`U-E2-fin-2026-07-26`** | **有限群掃引** | $k\in\{4,8\}$、$2^5\le\lvert P\rvert\le2^8$、**`A_abelian=false` 枝を主目標**、`A_abelian=true` 枝は control | ①②の結果を**封印予測**として先に書いてから発射する(F14) |

### 4.2 各層の対象列挙法・規模・cap・証明書要件

#### ① `U-E2-nm5-2026-07-26`(完全 class-5 非 metabelian)

| 項目 | 事前登録値 |
|---|---|
| **対象(普遍側)** | $P^{(5)} := F_2/\gamma_6$。$A := \gamma_2/\gamma_6$、$\mathbb Z$-階数 12。Hall 基底(**順序を固定**): $w$;$p,q$;$r_1,r_2,r_3$;$t_1 = [r_1,x],t_2 = [r_1,y],t_3 = [r_2,y],t_4 = [r_3,y],t_5 = [w,p],t_6 = [w,q]$。$[A,A] = \langle t_5,t_6\rangle$(**中心**) |
| **対象(有限化)** | $A\otimes\mathbb Z/2^j$、$j = 1..6$。$m = 0..63$ |
| **列挙法** | 列挙ではなく**直接計算**。$\bar A := A/[A,A]$ 上で線型判定(§3.3 のモデルの $c=5$ 版・階数 10)→ 解の集合を求める → 各解の $[A,A]$ への持ち上げを補題 E22 の二次形式で判定 |
| **規模** | $\bar A$ 側: $10\times$(2 本の方程式系)の SNF。持ち上げ側: $\ker$ の階数だけ二次形式を評価。**いずれも秒オーダー** |
| **cap** | node 側 600 秒 / GAP 側 600 秒。ヒープ 2GB(**RAM 8GB 制約**)。超過は `status="cap_exceeded"` で UNKNOWN |
| **certificate(肯定)** | `solution_witness`: $f$ の Hall 座標、$(1+\theta)f$ と $\mathcal N f\cdot E_m$ を**群の積として**直接評価して $1$ になることを独立 checker が再計算 |
| **certificate(否定)** | 線型部が空 ⇒ `unsolvability_certificate`(dual witness $y$: $yM\equiv0$, $yb\not\equiv0\bmod2^j$、matrix content hash・modulus・基底順序つき — 便 12 F13)。線型部は非空だが持ち上げが全滅 ⇒ **`lift_obstruction_certificate`**(新設): $\ker$ の全代表元の列挙 + 各代表元での二次形式の値 + 到達不能性の再計算 |
| **★ 事前登録した両方向の読み** | **全 $(j,m)$ で可解** ⇒ E15 は $A$ 非可換の最小層でも生存。狩場は class 6 以上 or $3\mid\lvert A\rvert$ 側へ。 **一つでも不可解** ⇒ **E15 は普遍レベルで反証**・障害ベクトルを出力・§3.6(v1)の昇格レシピへ。**ただし普遍レベルの不可解性は具体的な有限許容対象の `m_missing` を直ちには与えない**(商へ降りると可解になり得る) |

#### ② `U-E2-metab-2026-07-26`(metabelian 塔・記号的 SNF)

| 項目 | 事前登録値 |
|---|---|
| **対象** | $A_c = \mathbb Z[S,T]/(S,T)^{c-1}$、$c = 3,\dots,8$(階数 $\binom c2 \le 28$) |
| **列挙法** | §3.3 のモデル。**GAP 側で独立実装**(`SmithNormalFormIntegerMat`)して `docs/scout/metab.mjs` と突合 |
| **規模** | $c\le7$: 数分。$c = 8$: node ではヒープ超過 ⇒ **GAP 側で再試行**(`gap.ps1 -o 2g`) |
| **cap** | GAP 600 秒/対象、宇宙 3600 秒。超過は UNKNOWN |
| **必須比較欄** | `elementary_divisors`(全リスト)・`max_v2_divisor`・`rationally_consistent`・`Z2_solvable`・`routes_agree`(node vs GAP)。**不一致は即停止** |
| **残る量化子** | (i) $\mathbb Q$-可解性の全 $m$(**記号的**に: $M(m),b(m)$ の成分は $m$ の多項式なので、左核ベクトル $y(m)$ を $\mathbb Q(m)$ 上で求め $y(m)\cdot b(m)\equiv0$ を多項式恒等式として検査する)。 (ii) $c\ge8$ |
| **certificate** | 肯定は `solution_witness`(直接代入)。否定は dual witness $y$。**記号的**な場合は $y(m)$ の多項式表示と $y(m)b(m)$ の展開係数を保存 |

#### ③ `U-E2-fin-2026-07-26`(有限群掃引)

| 項目 | 事前登録値 |
|---|---|
| $k$ | $k\in\{4,8\}$(主)。$k = 16$ は**別便・別宇宙** |
| $P$ の型 | 2 群、$2^5\le\lvert P\rvert\le2^8$。$\lvert Q\rvert = 6\lvert P\rvert\le1536$ |
| **枝の分離(F14)** | `A_abelian=false`(**主目標** — §3.5 (ii))と `A_abelian=true`(metabelian 枝)を**別々に集計**。metabelian class 5 も**除外しない**(F-1 の射程外指数が残るため)。metabelian class $\ge8$ は明示 UNKNOWN |
| **control** | CT-1〜CT-4(v1 §3.4)+ **固定した class-4 marked representatives**。**control を live discovery count に混ぜない**(F14) |
| 列挙 | E-1 = `lins`(正本)/ E-2 = `SmallGroups`+`autpgrp`(照合)。$\lvert P\rvert\le128$ で**交差検査必須**、食い違えば停止 |
| 判定 | route L(metabelian のみ)/ route T(`twistedconjugacy`)/ **route Q(新・第二照合器)**: $Q$ 内で $g\in\bar\Delta A$、$g^2=1$、$(v_mg)^3=1$ を全数列挙(便 12 F15/P138) |
| cap | 対象 60 秒、宇宙 3600 秒、`lins` index 1536。超過は UNKNOWN |
| **封印予測(発射前に書く)** | (a) class $\le4$ の全対象は $m$-full(**紙で確定** — 一件でも `m_missing` が出たら実装バグ)。 (b) metabelian class $\le7$・$m\le63$ の全対象は $m$-full(**定理 E19**)。 (c) ①の結果に応じた $A$ 非可換層の予測を**①の完了直後に封印してから**③を発射する |

### 4.3 証明書スキーマの差分 `e2-sweep-cert/v2`

v1 §3.5 の `e2-sweep-cert/v1` に対する**追加のみ**(削除なし)。

```json
{
  "schema": "e2-sweep-cert/v2",
  "universe_id": "U-E2-nm5-2026-07-26 | U-E2-metab-2026-07-26 | U-E2-fin-2026-07-26",
  "object": { "...v1 と同じ...",
    "derived_length": 3,
    "A_abelian": false,
    "A_commutator_subgroup_order": 4,
    "A_class": 2
  },
  "per_m": [{
    "...v1 と同じ...",
    "route_quotient_factor": { "available": true, "count": 2, "witness": "..." },
    "routes_agree_LTQ": true,
    "linear_part": { "available": true, "solvable": true, "kernel_rank": 4,
                     "elementary_divisors": [1,1,2,4], "max_v2_divisor": 2 },
    "lift_quadratic": { "attempted": true, "solvable": true,
                        "form_values_hash": "...", "witness": "..." },
    "unsolvability_certificate": {
      "claim": "torsion_intersection_empty",
      "method": "left_kernel_mod_prime_power/v1",
      "modulus": 16, "matrix_shape": [24,16],
      "basis_order": ["w","p","q","r1","r2","r3","t1","t2","t3","t4","t5","t6"],
      "relation_column_order": ["L1","L2","slack1","slack2"],
      "matrix_content_hash": "...", "b_content_hash": "...",
      "dual_witness_y": [ "..." ]
    },
    "lift_obstruction_certificate": {
      "claim": "linear_solutions_exist_but_none_lifts",
      "method": "central_quadratic_exhaustion/v1",
      "kernel_representatives_hash": "...", "form_values": [ "..." ]
    }
  }],
  "m_missing": [],
  "provenance": { "gap_version": "...", "node_version": "...",
                  "script_sha256": {"metab.mjs":"...","class4.mjs":"..."},
                  "input_hash": "...", "seed": null }
}
```

**schema の禁止事項(v1 §3.5 の W54 を継承・強化)**
- `fake_witness` 欄を置いてはならない。`intersection_size = 0` が示すのは `m_missing` まで(W54)。
- `intersection_size = 0` には **`unsolvability_certificate` または `lift_obstruction_certificate` が必須**。求解器の `fail`/`null` だけでは書かない(W101)。
- **`torsion-full` と `generation_pass_count>0` と `shadow exists` を同義にしない**(便 12 W97)。E9/E9′/E19 が与えるのは torsion 部だけである。
- **`verified` の語を使わない**(Lean 予約・便 12 Errata 3)。二系統一致は `cross-checked`、単系統は `candidate`。

### 4.4 作業指示(implementer / falsifier 宛)

> **W-新 1(最優先・implementer)**: `U-E2-nm5` の実装。§3.5 (iii) の**二段構え**(1) $\bar A$ 上の線型判定 — `docs/scout/metab.mjs` の $c=5$ 版がそのまま使える、(2) 補題 E22 の二次形式による持ち上げ判定。**否定側は `lift_obstruction_certificate` を必須**。
> **W-新 2(implementer)**: 定理 E19 の**第二系統照合**。GAP の `SmithNormalFormIntegerMat` で $c = 3..8$、$m = 0..63$ の基本因子リストを出し、`metab.mjs` の出力と**バイト一致**で突合。`routes_agree` を必須欄に。
> **W-新 3(implementer)**: 便 12 P138 の **route Q**(独立 $Q$-判定器)を `U-E2-fin` 用に実装。$g^2 = 1$、$(v_mg)^3 = 1$ の全数列挙と、$g = \bar\Delta f$ による route T との明示対応の全数 hash。
> **W-新 4(falsifier)**: §4.1–4.3 の事前登録に対する反証前哨 — 特に (a) ①の「$\bar A$ 上の線型判定 → 持ち上げ」という二段構えが**十分**か(中間の $[A,A]$ 以外に落とし穴はないか)、(b) 封印予測 (a)(b) が空虚テストになっていないか、(c) `lift_obstruction_certificate` が独立再検査可能か。
> **W-新 5(司令塔経由・Sol へ)**: 定理 E18/E19/E21 と §1 の紙上証明の**相互監査**。特に補題 E18.2($M_2(\mathbb Z_2)$ による crossed product 分解)と系 E19-b(Lucas による $m$ 周期性)は**新しい道具**なので独立検分を求める。

---

## 5. 未閉鎖項・状態札・次の一手

### 5.1 【GAP】表(v1 §2.4 からの差分)

| # | 内容 | v1 での状態 | **本稿での状態** |
|---|---|---|---|
| **【GAP-E2】** | 一般の同時可解性 | 本丸 = class $\ge5$ | **本丸 = $A$ 非可換($=$ 導来長 $\ge3$)のみ**へさらに縮小。正しい定式化は「線型 + 中心的二次形式」(補題 E22) |
| **【GAP-E13】** | class $\ge5$ の判定 | 新設 UNKNOWN | **metabelian 側は class $\le7$・全 $j$ で閉鎖(定理 E19)**。非 metabelian は UNKNOWN(=【GAP-E2】と合流) |
| **【GAP-E15】** | 予想 E15 の真偽 | 新設・最重要 | **反証されず**。射程が大幅に拡大: class $\le4$ は**紙で証明**、metabelian class $\le7$ は $m\le63$・**全 $j$**。残るのは (i) metabelian の $\mathbb Q$-可解性の全 $m$、(ii) $A$ 非可換 |
| **【GAP-E12】** | E12 の絡作用素の正規化 | 新設 UNKNOWN | **優先度を下げる** — 定理 E21 により系 E12-a が空虚である以上、指標和路線の当面の価値は小さい。数学的には依然 UNKNOWN |
| **【GAP-E16】(新設)** | 命題 E16 の仮定 $A^\sigma\subseteq C_A(X^u)$ が class $\ge3$ で成立し得るか(系 E2′-a は $A\subseteq C_A(X^u)$ の場合しか扱っていない) | — | **UNKNOWN**。成立する対象があれば、その対象は $\theta(E_m) = E_m^{-1}$ の一行判定で片付く |
| **【GAP-E18】(新設)** | 定理 E18 の逆($O_j = 0\ \forall j\Rightarrow$ 可解)。各段の持ち上げの二次障害の制御 | — | **UNKNOWN**。§3.3 は metabelian 塔では逆も事実上成立していることを示すが、証明ではない |
| **【GAP-E19】(新設)** | 定理 E19 の $\mathbb Q$-可解性を**全 $m$** へ(記号的 SNF)。および class $\ge8$ | — | **UNKNOWN**(§4.2 ② に作業指示) |
| **【GAP-E20】(新設)** | $A$ 非可換な許容 2 群の**最小位数**($\ge2^7$ と見込まれる) | — | **UNKNOWN**(§4.2 ③ で決定) |
| **【GAP-E2b】** | $\iota_{X^u}$ の吸収 / Burkhart | 恒久閉鎖 | **維持**。ただし便 12 W104 に従い「全ての非 coprime 固定点定理が無力」とは書かない |
| **【GAP-E14】** | class 4・$\exp A\ge32$ | E9′ により閉鎖 | **維持**(§1 で紙上証明が付いたのでさらに強い) |

### 5.2 【文献要請】(便 12 の裁定を踏まえて更新)

> **【文献要請 6′】(【GAP-E2】本丸 = $A$ 非可換)** — v1 の【文献要請 6】を**差し替える**。
> **困難**: 有限 2 群 $A$ が **class 2**($[A,A]\subseteq Z(A)$、$[A,A]$ の階数は小さい)であるとき、位数 3 の自己同型 $\sigma$ に対する $\sigma$-捻れ共役類 $\mathcal S = \{\sigma(a)^{-1}f_0a\}$ と、$\mathcal B_\theta = \{f : \theta(f) = f^{-1}\}$ の交わりの非空性を判定したい。**$\bar A = A/[A,A]$ 上では線型で完全に解ける**(本稿 §3.3)。難しいのは**持ち上げ**であり、それは $[A,A]$ に値をとる**双加法的形式 $c(f,g)$(補題 E22)の値域判定**になる。
> **欲しい結果の型**: (i) class-2 群における「捻れ共役類 $\times$ 反不変集合」の交わりを、中心拡大のコサイクル($H^2$ 的)言語で書く枠組み。(ii) 中心的二次形式の値域(Arf 不変量・Witt 群)による判定条件。(iii) この交わりが空になる**最小の class-2 例**。
> **探す先の当たり**: 中心拡大と捻れ共役性 — Dekimpe らの `twistedconjugacy` の背景文献、冪零群の Reidemeister 数、group cohomology の "twisted quadratic form" 系。
> **★ 探さなくてよい方向(本稿で潰した)**: (a) Burkhart 型の非 coprime 不動点定理(v1 観察 B1)、(b) **$S_3$ の 2-modular 表現論を $A$ そのものへ適用する路線**(§3.1 — $\langle\sigma,\theta\rangle$ が $S_3$ でない)、(c) **系 E12-a 型の「同時安定既約が自明のみ」条件**(定理 E21 — 非可換 2 群では常に空虚)。

### 5.3 状態札の一覧(W60/W92 準拠)

| 主張 | 札 |
|---|---|
| §1 の定理 E9′ と (†)、Lemma A/B、$\kappa_m$ の閉形、$E_m$ の class-4 閉形 | **紙上証明**(Opus 単独・**Sol 未監査**)。全定数を `class4.mjs` と `metab.mjs` の**二つの独立モデル**が再現 |
| §2 の補題 E10.1・命題 E10 全称版 | **紙上証明**(Opus 単独・Sol 未監査) |
| 命題 E16 / 補題 E16.1 / 系 E16-a / 補題 E18.1 / 補題 E18.2 / 定理 E18 / 命題 E20 / 定理 E21 / 補題 E22 | **紙上証明**(Opus 単独・Sol 未監査) |
| 表 1(a)(b) の重複度 | **紙上証明**(指標公式)。$j\le7$ は `metab.mjs` が数値照合 |
| **定理 E19**(class $\le7$・$m\le63$・全 $j$) | **単系統 candidate**(`docs/scout/metab.mjs`・自己検査 13 項 PASS)。**cross-checked ではない**(W-新 2 で第二系統を取る) |
| 系 E19-b($m\bmod8$ 周期性による全 $m$ 拡張) | **紙上証明**(Lucas)+ 上の単系統計算 |
| 予想 E15 | **予想**。定理でも観測でもない。**safe フィルタに使ってはならない**(W42 は生きている) |
| **verified(Lean)** | **一つも無い** |

### 5.4 便 12 の Errata / W への応答表

| 便 12 の項目 | 本稿での対応 |
|---|---|
| Errata 1(「$A$ 非可換 $\iff$ class $\ge5$」は誤り) | **受諾**。本稿は一貫して「$A$ 非可換 $\Rightarrow$ class $\ge5$」とだけ書き、metabelian class $\ge5$ を明示的に別枝として扱う(§3.5・§4.2 ③) |
| Errata 2(160 件から一般化しない) | **受諾**。§3.3 は射程を「class $\le7$・$m\le63$・全 $j$」と明記し、$m$ 量化子を【GAP-E19】に残す |
| Errata 3(`160/160 verified` は状態語違反) | **受諾**。本稿は `verified` を一切使わない。v1 §F-1.1 の該当語は**次版で訂正**(v1 は上書きしない — 本稿がその訂正記録) |
| Errata 4(torsion $\ne$ generation) | **受諾**。§2 と §4.3 の禁止事項に明記 |
| Errata 5(charming residue lift) | **受諾** — §2 の補題 E10.1 |
| Errata 6((†) は single-system candidate) | **解消**。§1 で**紙上証明**が付いたので、(†) は script に依存しない |
| Errata 7(「障害の唯一の素数は 3」を弱める) | **受諾かつ超過達成**。§3.3 は「metabelian 塔 class $\le7$ では 2-一次障害は**存在しない**」という、より強く射程の明確な形へ置き換えた |
| W97 / W98 / W100 / W101 / W102 / W103 / W104 | **全て受諾**(§2・§4.3・§4.2 に反映) |
| P133(E8/E9/E10/E12 の CLAIMS 登録) | 司令塔へ: **E9′ は §1 により candidate から `紙上証明(Sol 未監査)` へ昇格可能**。E16/E18/E19/E21 は**新規起票**を推奨 |
| P134(系 E12-a の登録) | **登録は可。ただし定理 E21(適用可能性 = 空)を併記すること**(§3.4) |
| P135(正しい cohomology 目標) | **受諾し、具体化した** — 定理 E18 が「$\theta$-同変 contracting homotopy」の障害を weight ごとの $O_j$ として明示し、weight $\le4$ では $O_j = 0$ を表現論で証明した |
| P136(F-1 の証明書化) | **§4.2 ② に作業指示**。本稿の `metab.mjs` は F-1 より強い(全 $j$)結果を出すので、証明書はこちらを正本にすることを推奨 |
| P137 / P138(不可解性証明書・独立 Q-route) | **§4.3 / W-新 3 に反映** |
| P139 / P140(次弾 1・2) | **§4.1 の ① ② としてそのまま採用**。ただし ② は D6 により大半が済んでいるので、**予算は ① に寄せることを進言する** |
| P141(Burkhart の限定記帳) | **受諾**(§5.1【GAP-E2b】) |

### 5.5 司令塔への進言(3 点)

1. **予算は ①(完全 class-5 非 metabelian)に寄せるべきである。** ②は定理 E19 で 2-一次側が事実上決着した(残るのは第二系統照合と $\mathbb Q$ の $m$ 量化子で、どちらも安い)。**唯一の生きた層は $A$ 非可換**であり、そこに全ての武器が失効するという事実が §3.5 で確定した。
2. **§1 の紙上証明により、便 12 W98 の保留条件は消滅した。** (†) はもはや script に依存しない。ただし **Sol 未監査**なので `paper mutual-audit PASS` ではない — 次便で監査を求めるべき項目は §4.4 W-新 5 に列挙した。
3. **`docs/scout/metab.mjs` は監査対象として共有ツリーに置いた**(裁定 12 の運用教訓の遵守)。金庫移送は**監査完了後**に。

---

## 付録 — v1 からの訂正(v1 は上書きしない)

| v1 の箇所 | 訂正 |
|---|---|
| §0 C5・§1.5・§2.4 の「$A$ 非可換 $\iff$ class $\ge5$」 | 正しくは「$A$ 非可換 $\Rightarrow$ class $\ge5$」。metabelian class $\ge5$ が存在する(便 12 Errata 1) |
| §F-1.1 の「**160/160 verified**」 | 状態語違反。正しくは `160/160 witness-checked candidate`。**なお本稿の定理 E19 がこれを包含し、かつ全 $j$ へ拡張している** |
| §1.6 C8 の「障害の唯一の素数は 3」 | 「class $\le4$ の明示 witness の分母には 3 しか現れない」という観測へ弱める(便 12 Errata 7)。**さらに本稿 §3.3 は、metabelian 塔 class $\le7$ では 2-一次障害が存在しないことを計算で示す** |
| §1.6 F-3 の「F-1/F-2 が通ったら掃引の宇宙を 2 群から外す」 | **撤回**(便 12 W103)。2 群を宇宙から外さない。§4 の三層登録に置き換える |
| §4 の「スクリプトは `scratchpad/`」 | **`docs/scout/` へ移送済**(裁定 12 の運用教訓: 監査対象の根拠物は監査完了まで共有ツリーに残す) |
