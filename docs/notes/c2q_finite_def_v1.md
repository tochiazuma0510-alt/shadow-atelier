# C2-Q 有限版 c₂ の定義と分離能力(v1)

- 起草: 数学者(Opus)・2026-08-01
- 入力: 裁定 397 / `docs/notes/c2q_blocker_v1.md`(実装係の定義閉塞ノート)/ `docs/notes/fake_void_v1.md` A.4 / `docs/scout/覚書_fvl1_20260801.md`
- 正典: `docs/week1-定義ノート.md`(定義・規約 W-1〜W-4)・arXiv 2401.06870・2405.11725
- **commit しない**。値はすべて機械生成(手写しなし)。

---

## 0. 要旨(先に結論)

| # | 結論 | 格 |
|---|---|---|
| **R1** | 有限版 c₂ は **γ₂(P)/γ₃(P)(P = F₂/N_{F₂})の中の f̄ の類**として定義でき、この群は **[x,y] で生成される巡回群 ℤ/d**。代表・窓の取替の両方に対して well-defined(§1) | **紙の証明**(Sol 監査未) |
| **R2** | **定理 C2-FIN**: 任意の charming GT-pair で **3c₂ ≡ m(m+1)/2 (mod d)**、同値に **λ² ≡ 24c₂+1 (mod 8d)**。これは **hexagon (3.11) だけの帰結**(§2) | **紙の証明**(sympy 記号検算つき) |
| **R3** | **C2-Q の答は「hexagon だけ」= 分離能力ゼロ**。A.4 の二分岐の第 1 枝で確定。しかも gcd(3,d)=1 の窓では **c₂ は m の関数**にすぎない(§4) | **定理からの帰結** |
| **R4** | **較正段の 2 窓は両方 d = 1**(K⁽³⁾: P = G₃ 位数 108 で γ₂=γ₃=C₃³ / N_A: P = A₅ は完全群)⟹ **c₂ は恒等的に自明・較正は数学的に空**(§3.5・§5) | **二実装一致 + 既存 cert の `derived_order` と独立一致** |
| **R5** | 較正の代替: **K⁽⁴⁾(d=2)・K⁽⁸⁾(d=4)・K⁽¹⁶⁾(d=4)**(2 冪 ⟹ 2405 Thm 5.3 で arithmetical)。プローブは **K⁽¹²⁾(d=2)・N_Q(d=2)**。実測 348 元で関係式 **失敗 0**(§5) | **二実装一致・実測** |
| **R6** | **命題 D-ODD**: **4 ∤ n なら d(K⁽ⁿ⁾) = 1**。すなわち **dihedral 予想の open 標的族(奇・混合)では c₂ は構造的に盲目** | **紙の証明**(§2.4) |
| **R7** | c₂ が m から決まらない情報を持つのは **3 \| d のときだけ**。現行窓在庫では該当ゼロ。最小の該当窓は **Heisenberg mod 3 窓 N₀ = π⁻¹(F₂³γ₃(F₂))(位数 27・d=3)**(§4.3) | **紙 + 計算** |
| **R8** | 副産物 **命題 C2-COC**: c₂ は groupoid 合成の 1-cocycle **c₂(g₁∘g₂) = c₂(g₁) + χ_vir(g₁)²·c₂(g₂)**。合成表 5,088 対で失敗 0(§2.6・§5) | **紙の証明 + 実測** |
| **R9** | 閉塞ノートの「32 元中 26 元が [F₂,F₂] に入らない」は**正しい観測だが charming の反証ではない**。有限商では **368/368 が γ₂(P) に入る**ことを再確認(§1.6) | **実測** |

**運用への含意(司令塔向け 1 行)**: C2-Q は「起票して測る」案件から「**定理で閉じた**」案件へ移る。層 (b) の fake 検出器としての c₂ は**死んだ**。ただし副産物(C2-COC・D-ODD・d センサス)は残る。

---

## 1. 定義

### 1.1 設定と記号

$N \in \mathrm{NFI}_{PB_3}(B_3)$ を窓とし、$N_{F_2} := N \cap F_2$(2401 (3.2))、
$$P := F_2/N_{F_2} \quad(\text{有限群}),\qquad \pi: F_2 \twoheadrightarrow P .$$
$\gamma_1(G)=G$、$\gamma_{i+1}(G)=[G,\gamma_i(G)]$。**交換子は paper 規約** $[u,v] := uvu^{-1}v^{-1}$、$c := [x,y]$。
語の評価は**規約 W-2**(定義ノート §1.5.1)に従う。$\bar x := \pi(x)$、$\bar y := \pi(y)$、$\bar c := \pi(c)$。

$\pi$ は全射なので $\gamma_i(P) = \pi(\gamma_i(F_2))$。よって
$$Q_N := \gamma_2(P)/\gamma_3(P)$$
は有限アーベル群である。

### 1.2 補題 C2-CYC($Q_N$ は $\bar c$ で生成される巡回群)

> **補題 C2-CYC.** $P$ が 2 元生成($\bar x,\bar y$)なら $Q_N = \langle \bar c\, \gamma_3(P)\rangle$ は巡回群である。その位数を
> $$\boxed{\,d = d(N) := |Q_N| = \mathrm{ord}\bigl(\bar c \bmod \gamma_3(P)\bigr)\,}$$
> と書く。

**証明.** 一般に $\gamma_2(G)/\gamma_3(G)$ は、$G$ の生成系 $\{g_i\}$ に対する $[g_i,g_j]$ の像で生成される(交換子の双線型性 $[uv,w]\equiv[u,w][v,w]$、$[u,vw]\equiv[u,v][u,w] \pmod{\gamma_3}$ から、任意の $\gamma_2$ の元が生成元の交換子の積 mod $\gamma_3$ に書ける)。生成元が 2 個なら候補は $[\bar x,\bar y]$ ただ一つ。∎

*(実測での確認: §5 の全窓で `ord([x,y] mod γ₃) = |γ₂|/|γ₃|` が成立 — GAP・python 双方。)*

### 1.3 定義 D1(有限版 c₂)

> **定義 D1.** $\bar f \in \gamma_2(P)$ を満たす $f$(= **charming** な GT-pair の $f$)に対し、
> $$\boxed{\; c_2^{\mathrm{fin}}(f\,N_{F_2}) := \bigl(\text{唯一の } e \in \mathbb Z/d \text{ で } \bar f \equiv \bar c^{\,e} \bmod \gamma_3(P)\bigr) \;\in\; \mathbb Z/d \;}$$
> と定める。すなわち $Q_N \xrightarrow{\ \sim\ } \mathbb Z/d$($\bar c \mapsto 1$)の下での $\bar f$ の像。

**符号規約(CV-13 の継承)**: 同型 $Q_N \cong \mathbb Z/d$ は **生成元 $\bar c = [\bar x,\bar y]$ を $+1$ に送る**ことで固定する。これは既存 CV-13 anchor(`c2_of([x,y]) = +1`)と**同じ規約**である(§1.7 で自由群版との整合を示す)。**順序対 $(x,y)$ を入れ替えると $c \mapsto c^{-1}$ ゆえ $c_2 \mapsto -c_2$** — 向きは規約であって定理ではない。

### 1.4 命題 P1(coset 代表の取替に対する不変性)

> **命題 P1.** $D1$ の値は $f$ の **coset $fN_{F_2}$ にのみ依存する**。すなわち $n \in N_{F_2}$ に対し $c_2^{\mathrm{fin}}(fn) = c_2^{\mathrm{fin}}(f)$。

**証明.** 定義が $\bar f = \pi(f) \in P$ だけを使っており、$\pi(fn) = \pi(f)$ だから。∎(自明だが、これこそ閉塞ノートの生語 Magnus 係数が持っていなかった性質である。)

**自由群版との橋(実用形)**: charming は $f \in \gamma_2(F_2)\,N_{F_2}$ と同値だから、$f = g\,n$($g \in \gamma_2(F_2)$、$n \in N_{F_2}$)と書ける。このとき
$$c_2^{\mathrm{fin}}(fN_{F_2}) \;\equiv\; c_2^{\mathrm{raw}}(g) \pmod d,\qquad
c_2^{\mathrm{raw}}: \gamma_2(F_2) \xrightarrow{\ \sim\ } \gamma_2(F_2)/\gamma_3(F_2)\cong\mathbb Z .$$
**これが well-defined であること**: $g,g'$ が二つの選択なら $g^{-1}g' = n n'^{-1} \in N_{F_2}\cap\gamma_2(F_2)$ で、$c_2^{\mathrm{raw}}$ は $\gamma_2(F_2)$ 上の準同型ゆえ $c_2^{\mathrm{raw}}(g')-c_2^{\mathrm{raw}}(g) \in c_2^{\mathrm{raw}}\bigl(N_{F_2}\cap\gamma_2(F_2)\bigr) = d\mathbb Z$。
最後の等号は
$$Q_N \;\cong\; \gamma_2(F_2)\big/\bigl(\gamma_2(F_2)\cap \gamma_3(F_2)N_{F_2}\bigr) \;=\; \gamma_2(F_2)\big/\gamma_3(F_2)\bigl(N_{F_2}\cap\gamma_2(F_2)\bigr)$$
から従う(Dedekind: $u\in\gamma_2$、$u=g_3 n$、$g_3\in\gamma_3\subseteq\gamma_2$ ⟹ $n\in\gamma_2$)。∎

> **⟹ $d$ の第二の顔**: $d$ は「$N_{F_2}$ が交換子部分群から切り取る格子 $c_2^{\mathrm{raw}}(N_{F_2}\cap\gamma_2(F_2)) = d\mathbb Z$ の指数」である。**$d=1$ は「$N_{F_2}$ が既に原始交換子($c_2^{\mathrm{raw}}=1$ の元)を含む」ことを意味する**。

### 1.5 命題 P2($N$ の取替 — 三つの取替すべて)

> **命題 P2.**
> **(a) 細分(reduction)に沿う自然性.** $N \le H$($\Rightarrow N_{F_2}\le H_{F_2}$)なら **$d(H) \mid d(N)$** で、reduction $R_{N,H}: [m,f]\mapsto[m, fH_{F_2}]$ (3.60) に対し
> $$c_2^{\mathrm{fin}}\bigl(R_{N,H}[m,f]\bigr) \;\equiv\; c_2^{\mathrm{fin}}([m,f]) \pmod{d(H)} .$$
> **(b) marking の同型に対する自然性.** $\varphi: P \to P'$ が $\varphi(\bar x)=\bar x'$、$\varphi(\bar y)=\bar y'$ を満たす同型なら $c_2$ は保たれる。**ただし $\bar x \leftrightarrow \bar y$ を入れ替える同型では $c_2 \mapsto -c_2$**。
> **(c) 共役不変性.** $c_2^{\mathrm{fin}}(u f u^{-1}) = c_2^{\mathrm{fin}}(f)$($u \in P$ 任意)。

**証明.**
(a) $\rho: P_N = F_2/N_{F_2} \twoheadrightarrow P_H = F_2/H_{F_2}$ は全射準同型ゆえ $\rho(\gamma_i(P_N)) = \gamma_i(P_H)$。よって $Q_N \twoheadrightarrow Q_H$ が誘導され、生成元 $\bar c \mapsto \bar c'$ を保つ。巡回群の全射 $\mathbb Z/d(N) \twoheadrightarrow \mathbb Z/d(H)$($1\mapsto 1$)は $d(H)\mid d(N)$ と還元写像に他ならない。$f$ の像も可換図式で送られる。∎
(b) $\gamma_i$ は特性的、$\varphi$ は $[\bar x,\bar y] \mapsto [\bar x',\bar y']$ を送るから、$Q_N \cong Q_{N'}$ が生成元を保つ。入替の場合 $[\bar y,\bar x] = [\bar x,\bar y]^{-1}$ で符号が反転する。∎
(c) $[u, \gamma_2(P)] \subseteq \gamma_3(P)$ ゆえ $P$ の共役は $Q_N$ に自明に作用する。∎

> **⟹ 「$c_2$ は逆系 $\{ \mathbb Z/d(N) \}$ の元」**: (a) により $c_2$ は isolated poset 上の自然変換 $\mathrm{GT}(-) \to \mathbb Z/d(-)$ を与え、genuine な元(= $\varprojlim$ の元)に対しては $\varprojlim_N \mathbb Z/d(N)$ の元を定める。これが Furusho の $c_2 \in \widehat{\mathbb Z}$ の有限段での正体である。

### 1.6 閉塞ノートの観測の解消(R9)

閉塞ノート §1 の「32 元中 26 元が生の $[F_2,F_2]$ に属さない」は**正しい**。しかし charming が要求するのは $\bar f \in \gamma_2(P)$ である。実測(§5)では

- K⁽³⁾ **12/12**、N_A **20/20**、さらに K⁽⁴⁾ 4/4・K⁽⁶⁾ 12/12・K⁽⁸⁾ 16/16・K⁽¹²⁾ 24/24・K⁽¹⁶⁾ 64/64・K⁽³⁶⁾ 216/216 —
- **合計 368/368 で $\bar f \in \gamma_2(P)$**。

⟹ **charming は破れていない**。破れていたのは「生語の Magnus 係数 = c₂」という同一視だけである。閉塞ノートの判断(値を出さずに止める)は**正しかった**。

### 1.7 自由群版 $c_2^{\mathrm{raw}}$ と Magnus 展開の一致(CV-13 の継承)

既存 CV-13 anchor は $c_2^{\mathrm{raw}}$ を「次数 $\le 2$ の Magnus 展開の $XY$ 係数」として実装している。$F_2/\gamma_3(F_2)$ の正規形 $x^ay^bc^k$(Heisenberg 座標)と Magnus 展開の関係は
$$w \equiv x^a y^b c^k \pmod{\gamma_3} \;\Longrightarrow\; \mathrm{Magnus}(w) = 1 + aX + bY + \dots + \bigl(\tfrac{a(a-1)}2\bigr)XX + (ab + k)\,XY + (-k)\,YX + \dots$$
であり、$a=b=0$ なら $XY$ 係数 $= k = c_2^{\mathrm{raw}}(w)$、かつ $XY$ 係数 $= -\,YX$ 係数(既存実装の反対称性チェックと一致)。
$[x,y] = xyx^{-1}y^{-1}$ の座標は $(0,0,1)$(記号計算で確認・§5)ゆえ **$c_2^{\mathrm{raw}}([x,y]) = +1$** — 既存 anchor と**同一規約**。

> **したがって CV-13 の向き規約は有限版へそのまま継承される。**
> **⚠ ただし新しい盲点**: $d \le 2$ の窓では $\mathbb Z/d$ の中で $+1 = -1$ となり、**向き anchor は数学的に無力**になる(定義ノート §1.5.3「二重打ち消しの罠」と同型の現象)。**向き検査は $d \ge 3$ の窓でしか意味を持たない**(§3.4 A2)。

---

## 2. 有限版 Furusho 関係式

### 2.1 前提

以下 **c ∈ N** を仮定する(中心 $c$ が窓の核に入る)。このとき:
- $N_{F_2}$ は $\theta,\tau \in \mathrm{Aut}(F_2)$ で不変(定義ノート §2 の 2026-07-25 注記の対偶)。よって $\theta,\tau$ は $P$、さらに $\bar P := P/\gamma_3(P)$ に降りる。
- 簡約 hexagon(2401 Prop 3.4)が使える: **(3.10)** $f\theta(f)\in N_{F_2}$、**(3.11)** $\tau^2(y^mf)\,\tau(y^mf)\,y^mf \in N_{F_2}$。
- $N_{\mathrm{ord}} = \mathrm{lcm}(\mathrm{ord}\,\bar x, \mathrm{ord}\,\bar y)$($\mathrm{ord}(cN)=1$)。

**在庫確認(この仮定は現行窓在庫を全て覆う)**: K⁽ⁿ⁾ は $\psi_n(c)=(1,1,1)$(2405 (3.1))、N_A は `docs/week4-A5算術飽和_v4.md` l.76「c ∈ N_A、N_ord = 5」、1a/1b/2a/2b/3 は cert の `c_in_N: true`。唯一の例外 $N_5$($c\ne1$ control)は $P$ アーベル(cert `derived_order: 1`)ゆえ $d=1$ で本節の主張は空。§2.5 に $c\notin N$ の一般形を置く。

### 2.2 定理 C2-FIN

> **定理 C2-FIN.** $c\in N$ の窓 $N$、$d=d(N)$ とする。$[m,f]$ を **charming GT-pair**(すなわち $\bar f \in \gamma_2(P)$ かつ hexagon)とし $c_2 := c_2^{\mathrm{fin}}(f) \in \mathbb Z/d$、$\lambda := 2m+1$ とおく。このとき
> $$\boxed{\;3\,c_2 \;\equiv\; \frac{m(m+1)}2 \pmod d\;}\qquad\Longleftrightarrow\qquad \boxed{\;\lambda^2 \;\equiv\; 24\,c_2 + 1 \pmod{8d}\;}$$
> **証明に使うのは (3.11) と charming のみ。(3.10) は一切使わない。**

**証明.**
$\bar P := P/\gamma_3(P)$ は冪零類 $\le 2$、$\gamma_2(\bar P) = Q_N = \langle\bar c\rangle \cong \mathbb Z/d$ で**中心的**。$\bar z := (\bar x\bar y)^{-1}$。

*(段 1)* 類 2 の群では交換子が双線型かつ中心的。$\tau$ が $\bar P$ に降りることから($c\in N$)、
$$\tau(\bar c) = [\tau\bar x,\tau\bar y] = [\bar y,\bar z] = \bar c,\qquad \theta(\bar c)=[\bar y,\bar x]=\bar c^{-1}.$$
($[\bar y,\bar z] = [\bar y,\bar y^{-1}\bar x^{-1}] = [\bar y,\bar x^{-1}] = [\bar y,\bar x]^{-1} = \bar c$。)
よって $\bar f = \bar c^{\,c_2}$ に対し $\tau(\bar f) = \tau^2(\bar f) = \bar c^{\,c_2}$。

*(段 2)* $\tau^2(y^mf) = \bar x^m\tau^2(\bar f)$、$\tau(y^mf) = \bar z^m\tau(\bar f)$(**$\tau(y)=z,\ \tau^2(y)=x$**)。中心性から (3.11) の像は
$$\bar c^{\,3c_2}\cdot \bar x^m\bar z^m\bar y^m \;=\; 1 \quad\text{in } \bar P .$$

*(段 3)* 類 2 の恒等式 $\bar x^m\bar z^m\bar y^m = \bar c^{\,\binom m2 - m^2}$(記号計算で確認・§5)。よって
$$3c_2 + \binom m2 - m^2 \equiv 0 \pmod d \iff 3c_2 \equiv m^2-\frac{m(m-1)}2 = \frac{m(m+1)}2 \pmod d .$$

*(段 4)* 両辺を 8 倍: $24c_2 \equiv 4m(m+1) = (2m+1)^2-1 = \lambda^2-1 \pmod{8d}$。$\mathbb Z/d \xrightarrow{\times 8} \mathbb Z/8d$ は単射なので**二式は同値**。∎

**★ 「24」の由来**: 「$3$($\tau$ 軌道の 3 項)」×「$8$($\lambda=2m+1$ への平方完成)」。この係数が正典と一致することが**規約の検算**になる — 交換子規約か語規約を取り違えた実装は $\lambda^2 \equiv -24c_2+1$ を出す。

### 2.3 well-defined 性と構造補題

$m$ は $\mathbb Z/N_{\mathrm{ord}}$ の元でしかない。関係式が矛盾しないためには $\frac{(m+N_{\mathrm{ord}})(m+N_{\mathrm{ord}}+1)}2 \equiv \frac{m(m+1)}2 \pmod d$、すなわち
$$m N_{\mathrm{ord}} + \frac{N_{\mathrm{ord}}(N_{\mathrm{ord}}+1)}2 \equiv 0 \pmod d$$
が必要。これは次から**自動で従う**:

> **補題 C2-STR(構造補題).** $c\in N$ の窓で $n_x := \mathrm{ord}(\bar x)$、$n_y := \mathrm{ord}(\bar y)$、$P^{\mathrm{ab}} \cong \mathbb Z/a_1\times\mathbb Z/a_2$ とすると
> $$\text{(i)}\ d \mid \gcd(n_x,n_y) \mid N_{\mathrm{ord}},\qquad \text{(ii)}\ N_{\mathrm{ord}} \text{ が偶なら } d \mid N_{\mathrm{ord}}/2,\qquad \text{(iii)}\ d \mid \gcd(a_1,a_2).$$

**証明.** (i) $\bar P$ で $\bar x^{n_x}=1$ ゆえ $\bar c^{\,n_x} = [\bar x^{n_x},\bar y] = 1$、同様に $\bar c^{\,n_y}=1$。
(ii) $\tau$-不変性より $\mathrm{ord}(\bar z) = \mathrm{ord}(\bar y) = \mathrm{ord}(\bar x)$、ゆえ $\bar z^{N_{\mathrm{ord}}}=1$。類 2 の公式 $\bar z^{n} = \bar x^{-n}\bar y^{-n}\bar c^{-n(n+1)/2}$(§5 で記号確認)に $n=N_{\mathrm{ord}}$ を入れて $\bar c^{\,N_{\mathrm{ord}}(N_{\mathrm{ord}}+1)/2}=1$、すなわち $d \mid \frac{N_{\mathrm{ord}}(N_{\mathrm{ord}}+1)}2$。$N_{\mathrm{ord}}$ 偶なら $\frac{N_{\mathrm{ord}}}2(N_{\mathrm{ord}}+1)$ で $N_{\mathrm{ord}}+1$ は奇 ⟹ (i) と合わせ $v_2(d)\le v_2(N_{\mathrm{ord}})-1$、奇素数では $v_p(d)\le v_p(N_{\mathrm{ord}})$ ⟹ $d \mid N_{\mathrm{ord}}/2$。
(iii) 交換子は全射 $\Lambda^2(P^{\mathrm{ab}}) \twoheadrightarrow \gamma_2(P)/\gamma_3(P)$ を誘導し、$\Lambda^2(\mathbb Z/a_1\times\mathbb Z/a_2)\cong \mathbb Z/\gcd(a_1,a_2)$。∎

**well-defined 性の確認**: (i) より $mN_{\mathrm{ord}}\equiv0 \pmod d$。$N_{\mathrm{ord}}$ 奇なら $\frac{N_{\mathrm{ord}}(N_{\mathrm{ord}}+1)}2$ は $N_{\mathrm{ord}}$ の倍数ゆえ $\equiv0$;偶なら (ii) の証明中の $d \mid \frac{N_{\mathrm{ord}}(N_{\mathrm{ord}}+1)}2$ がそのまま効く。∎ **矛盾なし。**

### 2.4 命題 D-ODD(奇・混合 dihedral 窓では $d=1$)

> **命題 D-ODD.** $4 \nmid n$ なら $d(K^{(n)}) = 1$。すなわち **$c_2^{\mathrm{fin}}$ は $K^{(n)}$ 上で恒等的に自明**。

**証明.** $n$ を奇とする。

*(段 1)* $\gamma_2(G_n) = C_n^3$、したがって $|G_n^{\mathrm{ab}}| = 4n^3/n^3 = 4$。
実際 $n$ 奇なら $\gamma_2(D_n) = \langle r^2\rangle = \langle r\rangle = C_n$ ゆえ $\gamma_2(G_n) \subseteq \gamma_2(D_n^3) = C_n^3$。逆向きは:$D_n$ の関係 $srs^{-1}=r^{-1}$ から
$$[X,Y] = \bigl([r,rs],\,[s,r],\,[s,rs]\bigr) = (r^{2},\,r^{-2},\,r^{-2}),$$
また $X=(r,s,s)$、$Y=(rs,r,rs)$ による $C_n^3$ への共役作用は符号パターン $(+,-,-)$ と $(-,+,-)$、すなわち**偶符号変換群 $\cong C_2\times C_2$**。$v=(2,-2,-2)\in(\mathbb Z/n)^3$ の軌道は $\{(2,-2,-2),(2,2,2),(-2,-2,2),(-2,2,-2)\}$ で、最初の 2 つの和が $(4,0,0)$。$n$ 奇ゆえ $4 \in (\mathbb Z/n)^\times$ で $e_1$ が張る中に入り、対称性から $e_2,e_3$ も入る。よって正規閉包は $C_n^3$ 全体。

*(段 2)* $|G_n^{\mathrm{ab}}| = 4$ ⟹ $G_n^{\mathrm{ab}} \cong \mathbb Z/a_1\times\mathbb Z/a_2$ で $\gcd(a_1,a_2) \mid 2$ ⟹ 補題 C2-STR (iii) から $d\mid 2$。

*(段 3)* $N_{\mathrm{ord}} = K_{\mathrm{ord}} = \mathrm{lcm}(n,2) = 2n$ は偶ゆえ (ii) から $d \mid n$(奇)。段 2 と合わせ $d \mid \gcd(2,n) = 1$。

$n \equiv 2 \pmod 4$ のときは $n = 2n_0$($n_0$ 奇)で 2405 Prop 3.5 の $K^{(n_0)} = K^{(2n_0)}$ により同一窓に帰着。∎

*(段 1 の実測確認: $|\gamma_2(G_n)| = n^3$ が $n = 3,5,7,9,11,13,15$ で python・GAP 双方で成立・§5.1。)*

> **★ これが本稿で最も重い一行**: **dihedral 予想の未解決標的族(奇 $n$・$n\equiv2\bmod4$、最小 open 標的 $K^{(3)}=K^{(6)}$ を含む)は、すべて $d=1$ である。** $c_2$ はその族で**測る前から恒等的に 0**。

### 2.5 $c \notin N$ の場合(語レベルの一般形)

$\tau$ が降りないので §2.2 段 1 が使えない。代わりに (3.11) を**自由群の語**として $F_2/\gamma_3(F_2)$(Heisenberg)で評価する。語 $f$ の Heisenberg 座標を $(a,b,k)$($f\equiv x^ay^bc^k$)とすると、記号計算(§5)により **(3.11) の左辺は常にアーベル化 $(0,0)$**、かつ
$$\kappa(W) \;=\; -\tfrac12\bigl(a^2-4ab+b^2+2m(a+b)+(a+b)-6k+m^2+m\bigr).$$
(3.11) $\in N_{F_2}$ より $\kappa(W)\in d\mathbb Z$、すなわち
$$\boxed{\;6k \;\equiv\; m^2+m + a^2-4ab+b^2+(2m+1)(a+b) \pmod{2d}\;}$$
$a=b=0$(代表を $\gamma_2(F_2)$ から取った場合)で $6c_2\equiv m^2+m \pmod{2d}$ となり定理 C2-FIN に一致する。

> **【GAP】C2-G1**: $c\notin N$ の窓では **(3.11) 自体が class $[m,f]$ の上で well-defined とは限らない**(代表の取替 $f\mapsto fn$ が $\tau(n)\notin N_{F_2}$ で壊れる)。厳密には $B_3/N$ 上の (3.3)(3.4) から導き直すべきである。**本稿はこれを行っていない。**
> **ただし実害はゼロ**: 現行窓在庫で $c\notin N$ なのは $N_5$ のみで、そこは $P$ アーベル ⟹ $d=1$ ⟹ 主張が空。

### 2.6 命題 C2-COC(合成の 1-cocycle 則)

> **命題 C2-COC.** $N$ が isolated(全 shadow が settled)なら、groupoid 合成 (3.53) に対し
> $$c_2\bigl([m_1,f_1]\circ[m_2,f_2]\bigr) \;\equiv\; c_2([m_1,f_1]) \;+\; \chi_{\mathrm{vir}}([m_1,f_1])^2\cdot c_2([m_2,f_2]) \pmod d,\qquad \chi_{\mathrm{vir}} = 2m+1 .$$

**証明.** (3.53) は $f_1 E_{m_1,f_1}(f_2)$、$E_{m,f}(x)=x^{2m+1}$、$E_{m,f}(y)=f^{-1}y^{2m+1}f$。settled なら $E$ は $P$ の自己同型を誘導し、$P^{\mathrm{ab}}$ 上では $\times\lambda_1$ のスカラー。したがって $\Lambda^2(P^{\mathrm{ab}})$ 上、ひいてはその商 $Q_N$ 上で $\times\lambda_1^2$。$c_2$ は $\gamma_2(P)\to Q_N$ の準同型ゆえ結論を得る。∎

**整合**: $\lambda = \lambda_1\lambda_2$(2405/2401 (3.49))と定理 C2-FIN から $24c_2 = \lambda^2-1 = \lambda_1^2(\lambda_2^2-1)+(\lambda_1^2-1) = \lambda_1^2\cdot24c_2(f_2)+24c_2(f_1)$ — **命題 C2-COC と完全に一致**。二つの独立な導出が合う。

### 2.7 二次剰余判定の有限版(問い 2 への答)

Furusho の設定では $\lambda$ が**未知**で「$24c_2+1$ が平方数か」が可解性条件になる。有限版では:

> **系 C2-QR.** $c_2 \in \mathbb Z/d$ を与えたとき、それを実現する $m$ が存在する必要十分条件は
> $$\boxed{\;1+24c_2 \ \text{が}\ \mathbb Z/8d\ \text{の平方であること}\;}$$
> であり、そのとき平方根 $\lambda$ は自動的に奇数で $m=(\lambda-1)/2$ を与える。**したがって「二次剰余判定」は法 $8d$ で残る**($d$ = §1.2 の $|\gamma_2(P)/\gamma_3(P)|$)。

**証明.** $m^2+m-6c_2\equiv0 \pmod{2d} \iff (2m+1)^2 \equiv 1+24c_2 \pmod{8d}$。$1+24c_2$ は奇ゆえ平方根も奇。逆向きは $m:=(\lambda-1)/2$、$(\lambda^2-1)/8 = m(m+1)/2$。∎

> **★ しかし判定は現実には空回りする**:
> **系 C2-QR2.** $3\mid d$ のとき、charming GT-pair の $\chi_{\mathrm{vir}}$ 可逆条件 $\gcd(2m+1,N_{\mathrm{ord}})=1$ から **可解性は自動**である。
> **証明.** $3\mid d\mid N_{\mathrm{ord}}$ ゆえ $3\nmid 2m+1$、すなわち $m\not\equiv1 \pmod 3$ ⟹ $m\equiv0,2 \pmod 3$ ⟹ $3\mid m(m+1)/2$ ⟹ $3c_2\equiv m(m+1)/2 \pmod 3$ は可解。∎
> $3\nmid d$ なら $3$ は $\mathbb Z/d$ で可逆ゆえ常に可解。**⟹ 全ての場合で可解性条件は自動的に満たされ、判定は一度も落ちない。**
>
> **法の在り処の混同禁止**: 既存 `c2q_calibration.py` は法として $N_{\mathrm{ord}}$ と小素数バッテリを使い、真の法は UNKNOWN と正直に申告していた。**真の法は $8d$ であり、$d\mid N_{\mathrm{ord}}$(補題 C2-STR)だが一般に $d \ne N_{\mathrm{ord}}$**(実例: K⁽³⁾ は $N_{\mathrm{ord}}=6$ に対し $d=1$)。

---

## 3. 窓ごとの計算仕様(実装係向け)

### 3.0 発注前ゲート(**必読・これを飛ばすと空振りする**)

> **G0(d ゲート)**: 窓ごとに **まず $d$ だけを計算し、$d=1$ の窓は測定対象から外す**(値が数学的に恒等 0 で情報ゼロ)。
> **G1(向き anchor ゲート)**: CV-13 向き anchor は **$d\ge3$ の窓でのみ有効**。$d\le2$ の窓では実行しても意味がない旨を cert に明記する。
> **G2(較正窓の差替)**: 裁定 380 が指定した較正母集団(K⁽³⁾ 12 元 + N_A 20 元)は**両方 $d=1$ で空**。§3.5 の代替母集団を使うこと。

### 3.1 共通手続き(GAP)

**規約**: paper 語 `"AB"` ↔ GAP `B*A`(規約 W-1)。**paper $[x,y]=xyx^{-1}y^{-1}$ ↔ GAP `Comm(Y,X)`**(GAP の `Comm(a,b)=a^{-1}b^{-1}ab`)。

```gap
# --- step 1: 窓の marking (X, Y) から d を出す ---
P    := Group(X, Y);;
g2   := DerivedSubgroup(P);;
g3   := CommutatorSubgroup(P, g2);;
d    := Size(g2)/Size(g3);;
hom  := NaturalHomomorphismByNormalSubgroup(g2, g3);;
cbar := Image(hom, Comm(Y, X));;              # paper [x,y] の像
Assert(0, Order(cbar) = d);                    # 補題 C2-CYC の実測確認(必須)

# --- step 2: 語の評価(規約 W-2 = prepend) ---
EvalWord := function(w, X, Y)
  local elt, t;
  elt := One(X);
  for t in w do
    if t[1] = "x" then elt := X^t[2] * elt; else elt := Y^t[2] * elt; fi;
  od;
  return elt;
end;;

# --- step 3: c2 の抽出 ---
C2Fin := function(w, X, Y, g2, hom, cbar, d)
  local F, im, cur, e;
  F := EvalWord(w, X, Y);
  if not F in g2 then return "NOT_CHARMING"; fi;   # ここで落ちたら窓かデータの誤り
  im := Image(hom, F);
  cur := One(im);
  for e in [0..d-1] do
    if cur = im then return e; fi;
    cur := cur * cbar;
  od;
  return "FAIL_NOT_IN_CYCLIC";                     # 補題 C2-CYC 違反 = バグ
end;;
```

**性能上の助言**: 全計算は **$\bar P = P/\gamma_3(P)$ の中で完結する**(定義も定理も類 2 の情報しか使わない)。$\bar P$ は劇的に小さい — 実測で $|P|=23{,}328 \Rightarrow |\bar P| = 32$(K⁽³⁶⁾)。大窓では
`q := NaturalHomomorphismByNormalSubgroup(P, g3);; Pbar := Image(q);;` を先に取ること。

### 3.2 窓 K⁽³⁾(G₃ = 位数 108)

- **marking**: $X = \psi_3(x) = (r,s,s)$、$Y = \psi_3(y) = (rs,r,rs)$ in $D_3^3$(2405 (3.1))。GAP では $D_3 = \langle r,s\rangle$、$r=(1,2,3)$、$s = (i \mapsto -i)$、**$rs$(paper 積)$=$ GAP `s*r`**。3 ブロック $\{1..3\},\{4..6\},\{7..9\}$ に埋め込む。
- **期待値(実測・§5)**: $|P| = 108$、$|\gamma_2| = 27$($=$ `K3.v1.json` の `invariants.derived_order` と一致)、$|\gamma_3| = 27$、**$d = 1$**。
- **f 像の抽出**: `K3.v1.json` の各 shadow は既に **`f_triple`** に $\psi_3$ 像を持っている(例 idx=2: `[[2,0],[1,0],[0,0]]` $=(r^2,r,1)$)。これを $D_3^3$ の元に戻せば `EvalWord` と一致することを**先に検算せよ**(相互 fixture)。
- **結果**: $Q_N = 1$ ⟹ 全 12 元で $c_2 = 0$、定理 C2-FIN は $0\equiv0$。**情報ゼロ**。

### 3.3 窓 N_A(A₅ 型)

- **marking**: $X = (1,3,2,4,5)$、$Y = (1,3,4,5,2)$(定義ノート §1.5.4 A5-CONV fixture)。
- **適合テスト(必須・先に通す)**: paper 語 $y x^{-1}$ の評価が **$(1,2,4)$**(GAP では `X^-1*Y`)。$(2,5,3)$ が出たら規約が逆。**python/GAP 双方で通ることを確認済**(§5)。
- **期待値(実測・§5)**: $|P| = 60 = |A_5|$、$A_5$ は**完全群**ゆえ $\gamma_2 = \gamma_3 = P$、**$d = 1$**。
- **結果**: 全 20 元で $c_2 = 0$。**情報ゼロ**。しかも $d=1$ は $A_5$ が完全であることの直接の帰結なので、**この窓では改良の余地がない**(どんな精密化をしても $\gamma_2/\gamma_3$ は自明)。

### 3.4 検算アンカー(全窓共通・cert に必記)

| # | アンカー | 内容 | 有効条件 |
|---|---|---|---|
| **A1** | 自明元 | $f=1$ ⟹ $c_2=0$。かつ定理から $m(m+1)/2\equiv0 \pmod d$ が従うこと | 常に |
| **A2** | **CV-13 向き** | $c_2([x,y]) = +1$ かつ $c_2([y,x]) = -1 \equiv d-1$、**両者が異なること** | **$d\ge3$ でのみ有効**。$d\le2$ では $+1=-1$ で盲点(§1.7) |
| **A3** | 準同型性 | $f,g\in\gamma_2(P)$ で $c_2(fg) = c_2(f)+c_2(g)$ | 常に |
| **A4** | **cocycle** | 合成表の全対で $c_2(i\circ j) \equiv c_2(i) + (2m_i+1)^2 c_2(j) \pmod d$(命題 C2-COC) | isolated 窓 |
| **A5** | 関係式 | $3c_2 \equiv m(m+1)/2 \pmod d$ ⟺ $\lambda^2\equiv24c_2+1 \pmod{8d}$ | $c\in N$ |
| **A6** | 構造 | $d \mid \gcd(\mathrm{ord}\bar x,\mathrm{ord}\bar y)$、$N_{\mathrm{ord}}$ 偶なら $d\mid N_{\mathrm{ord}}/2$、$d\mid\gcd(a_1,a_2)$($P^{\mathrm{ab}}=\mathbb Z/a_1\times\mathbb Z/a_2$) | $c\in N$ |
| **A7** | reduction 整合 | $N\le H$ で $d(H)\mid d(N)$ かつ $c_2^H(R(f))\equiv c_2^N(f) \pmod{d(H)}$。実施可能対: $K^{(36)}\!\to\!K^{(12)}$、$K^{(12)}\!\to\!K^{(4)}$、$K^{(8)}\!\to\!K^{(4)}$、$K^{(16)}\!\to\!K^{(8)}$ | 常に |
| **A8** | charming 再検算 | 全 $f$ で $\bar f \in \gamma_2(P)$。**1 件でも落ちたら窓定義か語規約のバグ**(閉塞ノートの生語判定とは別物であることに注意) | 常に |
| **A9** | 補題 C2-CYC | `Order(cbar) = Size(g2)/Size(g3)`。落ちたら $P$ が 2 元生成でないか実装バグ | 常に |

### 3.5 較正母集団の差替(**G2 の具体案**)

裁定 380 の較正母集団は $d=1$ で空である。**定理級に覆われた窓のうち $d\ge2$ のもの**へ差し替える:

| 窓 | 根拠 | $N_{\mathrm{ord}}$ | $d$ | 元数 | 較正力 |
|---|---|---|---|---|---|
| **K⁽⁴⁾** | 2405 Thm 5.3(2 冪 ⟹ arithmetical) | 4 | **2** | 4 | 弱($c_2\in\{0,1\}$) |
| **K⁽⁸⁾** | 同上 | 8 | **4** | 16 | **最良**($c_2$ が 0,1,2,3 全てを取る・A2 向き anchor が有効) |
| **K⁽¹⁶⁾** | 同上 | 16 | **4** | 64 | 良(A2 有効) |
| ~~K⁽³⁾~~ | 定理 K3 | 6 | **1** | 12 | **空** |
| ~~N_A~~ | 定理 A₅ | 5 | **1** | 20 | **空** |

**プローブ段の候補(定理非被覆・$d\ge2$)**: **K⁽¹²⁾**($d=2$・24 元)、**N_Q = 1a**($Q_8$・$d=2$)、**N_2 = 2a**($d=2$)、**N_3 = 2b**($d=2$)、**M_Q = 1b**($d=2$)。
**ただし §4 の結論により、これらを走らせても fake は原理的に出ない。** 走らせる価値があるのは「評価器の較正」と「A4/A7 の構造検査」としてのみ。

---

## 4. C2-Q への回答(分離能力)

### 4.1 直接の答: **hexagon だけ**

> **定理 C2-FIN(§2.2)は (3.11) と charming のみから従う。**
> $\Rightarrow$ **$\lambda^2 \equiv 24c_2+1 \pmod{8d}$ は全ての GT-shadow が自動的に満たす。**
> $\Rightarrow$ **層 (b) の fake 検出器としての分離能力は厳密にゼロ。** fake_void A.4 の二分岐の**第 1 枝で確定**。

**論理の精密化(誤読防止)**: 「pentagon が要らない」の意味は次のとおり。charming($\bar f\in\gamma_2(P)$)は gentle 圏における pentagon の**代役**であり、$c_2$ を**定義するため**には必要である。しかし一度 $c_2$ が定義されれば、その**値**は hexagon が完全に固定する。したがって仮に「charming かつ hexagon を満たすが pentagon 解に持ち上がらない」元(= pentagon-fake)が存在しても、**それも関係式を満たす**。⟹ 検出できない。

### 4.2 メタ論証(なぜ第 2 枝は最初から不可能だったか)

$B_3$-gentle 圏では $\mathrm{GT}(N)$ は **hexagon + charming + 全射性**で*定義*される。よって「$\mathrm{GT}(N)$ の全元が満たす恒等式」は定義条件の帰結でしかありえない。
⟹ **GT-pair のデータ $(m,\bar f)\in\mathbb Z/N_{\mathrm{ord}}\times P$ の関数として書ける不変量は、原理的に pentagon の破れを検出できない。**
⟹ 層 (b) を動かす唯一の道は**枠をまたぐ比較**($\mathrm{GT}^\heartsuit$ / $PB_4$ 側 = GTPI 線・FV-04・HS Prop. 7 の有限商翻訳)である。fake_void A.2 の第二照準の方が正しい賭けだった。

### 4.3 さらに強い形: $c_2$ は多くの場合 **$m$ の関数にすぎない**

定理 C2-FIN は $3c_2$ を決める。よって:

- **$\gcd(3,d)=1$ のとき**: $c_2 \equiv 3^{-1}\cdot\frac{m(m+1)}2 \pmod d$ — **$c_2$ は $m$ から一意に決まる**。新しい情報は 1 ビットもない。
  **現行窓在庫はすべてこの場合**($d\in\{1,2,4\}$;実測 §5)。実測でも同じ $m$ を持つ shadow は必ず同じ $c_2$ を取った(K⁽⁸⁾ の 16 元・K⁽¹²⁾ の 24 元)。
- **$3\mid d$ のとき**: $c_2$ は $\mathbb Z/3$ ぶんだけ $m$ から独立 — **これが $c_2$ の情報を持つ唯一の部分**。ただし
  (i) 系 C2-QR2 によりその部分に hexagon は何の制約も課さない(関係式は $0\equiv0$ に退化する)、
  (ii) genuine 側でも制約されない: genuine 元の $c_2$ は $(\hat\lambda^2-1)/24 \bmod d$ だが、$\hat\lambda\in\widehat{\mathbb Z}^\times$ の持ち上げの自由度 $\hat\lambda\mapsto\hat\lambda+2N_{\mathrm{ord}}t$ が $c_2$ を $\mathbb Z/3$ 全体に動かす(差は $N_{\mathrm{ord}}t(\hat\lambda+N_{\mathrm{ord}}t)/6$)。
  ⟹ **この自由部分も fake 検出器にはならない。**

**最小の $3\mid d$ 窓(記録のため)**: $N_0 := \pi^{-1}\bigl(F_2^3\gamma_3(F_2)\bigr)$、$P = $ Heisenberg mod 3(位数 27)、$N_{\mathrm{ord}}=3$、**$d=3$**(実測 §5)。fully invariant ゆえ $B_3$-安定・$c\in N_0$。T-25 の「Heisenberg 窓 $N_0$」と同一物。**ここは $c_2$ が自由に動く唯一の観測地点**だが、上記 (ii) により Furusho 関係式の検定にはならない。

### 4.4 UNKNOWN として明示的に残すもの

1. **【U1】** pentagon の破れを捕まえる**より深い**フィルトレーション($\gamma_3/\gamma_4$ 以降、Lie 側の $\sigma_3$ に対応する次数)が有限段で計算可能な形で存在するか — **UNKNOWN**。本稿は $\gamma_2/\gamma_3$ しか扱っていない。
2. **【U2】** $3\mid d$ の窓で $c_2$ の自由部分が「genuine では全値を取る」かどうかは、$\mathrm{GT}(N_0)=\mathrm{GT}_{\mathrm{gen}}(N_0)$ を仮定しないと言えない(循環)。本稿の §4.3(ii) は「制約が導けない」までしか主張しない。
3. **【U3】** $c\notin N$ の窓での定理 C2-FIN(§2.5 の【GAP】C2-G1)。実害ゼロだが未閉鎖。

### 4.5 【文献要請】

> **困難**: $B_3$-gentle 圏の有限商データ $(m,\bar f)$ の中で、**hexagon の帰結ではない** pentagon 由来の制約を、$\gamma_2/\gamma_3$ より深いフィルトレーション($\gamma_3/\gamma_4$ 等)に取り出せるか。$\gamma_2/\gamma_3$ では本稿の定理により完全に空振りすることが確定した。
> **欲しい結果の型**: (a) associator / GT 側で「hexagon 解空間」と「pentagon 解空間」が**最初に分岐する次数**を特定した結果(覚書 FV-L1 が挙げた Löffler arXiv:1502.06847 の grt hexagon 解空間への射影が最も近い隣接と思われる)。(b) $\widehat{GT}$ の下降中心フィルトレーションでの graded piece の既知の記述($\mathfrak{grt}_1$ の生成元が次数 3,5,7,… であることの離散版)。(c) Harbater–Schneps Prop. 7(関係 (III) ⟺ $\hat K(0,5)$ 上の $(14253)$ の持ち上げとの可換性)を**有限商の置換群計算**に落とす既存の試み。
> **不要なもの**: Furusho Question 14 そのものの追加文献(覚書 FV-L1 で十分)。

---

## 5. 検算(機械出力の要約)

**実装 2 系統**(いずれも本稿の設計者が同一セッションで書いたもの ⟹ 独立性は限定的。格は **candidate/自己二重化**であって cross-checked ではない。ただし下記 (E) は真に独立):

- (A) **記号計算**(sympy・Heisenberg 座標 $(a,b,k)$、積則 $(a,b,k)(a',b',k')=(a+a',b+b',k+k'-a'b)$)
  `scratchpad/c2q/heis2.py`
  - $[x,y]=(0,0,1)$、$[y,x]=(0,0,-1)$、$z=(xy)^{-1}=(-1,-1,-1)$、$\tau^3=\mathrm{id}$、$\theta^2=\mathrm{id}$、$\tau(c)=c$、$\theta(c)=c^{-1}$ — 全て OK
  - **(3.11) 左辺のアーベル化は $(0,0)$(任意の $f$ について)**
  - $f\in\gamma_2$ に制限して $\kappa(W) = (6k-m^2-m)/2$ ⟹ **$6c_2=m^2+m$** ⟹ $\lambda^2-(24c_2+1)=0$
  - **(3.10) は $f\in\gamma_2$ で $\kappa=0$ — 情報ゼロ**
  - $x^mz^my^m = c^{\binom m2-m^2}$、$z^{n_0} = x^{-n_0}y^{-n_0}c^{-n_0(n_0+1)/2}$
  - 一般形 $\kappa(W) = -\frac12(a^2-4ab+b^2+2m(a+b)+(a+b)-6k+m^2+m)$
- (B) **有限群計算・python**(純 python 置換群・paper 規約 $\mathrm{mul}(a,b)[i]=a[b[i]]$)`scratchpad/c2q/dcalc.py`
- (C) **有限群計算・GAP 4.16.0**(`DerivedSubgroup` / `CommutatorSubgroup` / `NaturalHomomorphismByNormalSubgroup`・paper $[x,y]$ ↔ `Comm(Y,X)`)`scratchpad/c2q/dcheck.g`, `scratchpad/c2q/fib.g`, `scratchpad/c2q/heis3.g`
- (D) **(B) と (C) は全項目で一致**(下表)。関係式実測 `scratchpad/c2q/predict.py`、cocycle 実測 `scratchpad/c2q/cocycle.py`
- (E) **既存 cert の `invariants.derived_order`(2026-07 の GAP バッテリが独立に生成)と $|\gamma_2|$ が一致**: K3=27、K4=2、K8=16、K12=54、K16=128、K36=1458、N5=1 — **これは真に独立な第三の系統**

### 5.1 $d$ センサス

| 窓 | $P$ | $|P|$ | $|\gamma_2|$ | $|\gamma_3|$ | **$d$** | $N_{\mathrm{ord}}$ |
|---|---|---|---|---|---|---|
| K⁽³⁾=K⁽⁶⁾ | $G_3$ | 108 | 27 | 27 | **1** | 6 |
| K⁽⁴⁾ | | 32 | 2 | 1 | **2** | 4 |
| K⁽⁵⁾=K⁽¹⁰⁾ | $G_5$ | 500 | 125 | 125 | **1** | 10 |
| K⁽⁷⁾=K⁽¹⁴⁾ | $G_7$ | 1372 | 343 | 343 | **1** | 14 |
| K⁽⁸⁾ | | 256 | 16 | 4 | **4** | 8 |
| K⁽⁹⁾ | $G_9$ | 2916 | 729 | 729 | **1** | 18 |
| K⁽¹¹⁾, K⁽¹³⁾, K⁽¹⁵⁾ | | 5324/8788/13500 | $n^3$ | $n^3$ | **1** | $2n$ |
| K⁽¹²⁾ | | 864 | 54 | 27 | **2** | 12 |
| K⁽¹⁶⁾ | | 2048 | 128 | 32 | **4** | 16 |
| K⁽²⁰⁾ | | 4000 | 250 | 125 | **2** | 20 |
| K⁽²⁴⁾ | | 6912 | 432 | 108 | **4** | 24 |
| K⁽³²⁾ | | 16384 | 1024 | 256 | **4** | 32 |
| K⁽³⁶⁾ | | 23328 | 1458 | 729 | **2** | 36 |
| **N_A** | $A_5$(完全) | 60 | 60 | 60 | **1** | 5 |
| **N_Q**(1a) | $Q_8$ | 8 | 2 | 1 | **2** | 4 |
| **N_2**(2a) | $F_2/F_2^4\gamma_3$ | 32 | 2 | 1 | **2** | — |
| **N_3**(2b) | $F_2/F_2^4\gamma_4$ | 128 | — | — | **2**(注) | — |
| **M_Q**(1b) | $G_3\times_{C_2^2}Q_8$ | 216 | 54 | 27 | **2** | — |
| **N₅**(control) | アーベル | 5 | 1 | 1 | **1** | 5 |
| **N₀**(Heisenberg mod 3) | $H_3$ | 27 | 3 | 1 | **3** | 3 |

注 1: N_3 は $d$ が**最大類 2 商だけで決まる**(補題: $d = |\gamma_2(\bar P)|$、$\bar P = P/\gamma_3(P)$)ことと $P_3/\gamma_3 = P_2$(2a)から $d=2$。
注 2(出所): K⁽ⁿ⁾ 行と N_A 行は $\psi_n$ / A5-CONV marking から**正典どおりに構成**した群。**N_2・N_3・M_Q・N₀ の行は cert の `target_definition` の記述からの再構成**であって cert 内の群オブジェクト自体を読んだものではない($|P|$ が cert 記載の位数 32 / 128 / 216 と一致することのみ確認)。**プローブ段を起票する場合は cert 側の marking で再計算すること。**
**観測されたパターン**: $d(K^{(n)}) = 1 \iff 4\nmid n$($\Leftarrow$ は命題 D-ODD で証明済、$\Rightarrow$ は上表の実測)。$4\mid n$ では $d = 2$($n\equiv4 \bmod 8$)/ $4$($8\mid n$)。

### 5.2 定理 C2-FIN の実測(prediction = $m$ のみから / measurement = $f\_word$ のみから)

| 窓 | $d$ | shadow 数 | charming($\bar f\in\gamma_2(P)$) | **関係式の失敗** |
|---|---|---|---|---|
| K⁽³⁾ | 1 | 12 | 12/12 | **0** |
| K⁽⁴⁾ | 2 | 4 | 4/4 | **0** |
| K⁽⁶⁾ | 1 | 12 | 12/12 | **0** |
| K⁽⁸⁾ | 4 | 16 | 16/16 | **0** |
| K⁽¹²⁾ | 2 | 24 | 24/24 | **0** |
| K⁽¹⁶⁾ | 4 | 64 | 64/64 | **0** |
| K⁽³⁶⁾ | 2 | 216 | 216/216 | **0** |
| **計** | | **348** | **348/348** | **0** |

(N_A の 20 元は $d=1$ ゆえ $0\equiv0$ で自明成立・上表とは別勘定。合計 368 元。)

**K⁽⁸⁾ の詳細($d=4$・$c_2$ が全 4 値を取る唯一の実測)**:

| $m$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $\lambda$ | 1 | 3 | 5 | 7 | 9 | 11 | 13 | 15 |
| $c_2$(実測) | 0 | 3 | 1 | 2 | 2 | 1 | 3 | 0 |
| $3c_2 \bmod 4$ | 0 | 1 | 3 | 2 | 2 | 3 | 1 | 0 |
| $m(m+1)/2 \bmod 4$ | 0 | 1 | 3 | 2 | 2 | 3 | 1 | 0 |
| $\lambda^2 \equiv 24c_2+1 \bmod 32$ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

$c_2$ が $m$ の関数になっている(§4.3)ことがそのまま読める。

### 5.3 命題 C2-COC の実測(合成表全対)

| 窓 | $d$ | 検査対 | 失敗 |
|---|---|---|---|
| K⁽³⁾ | 1 | 144 | 0 |
| K⁽⁴⁾ | 2 | 16 | 0 |
| K⁽⁸⁾ | 4 | 256 | 0 |
| K⁽¹²⁾ | 2 | 576 | 0 |
| K⁽¹⁶⁾ | 4 | 4096 | 0 |
| **計** | | **5,088** | **0** |

### 5.4 規約の適合テスト

- **A5-CONV 主判定**: paper 語 $yx^{-1}$ の $A_5$ での評価 $= (1,2,4)$ — **python(左作用合成)・GAP(`X^-1*Y`)双方で PASS**、誤方向値 $(2,5,3)$ は出ず。
- **`f_triple` 相互 fixture**: `K3.v1.json` の `f_triple` が本稿の評価と一致(idx=2 の $x x y^{-1}y^{-1} \mapsto (r^2,r,1)$、idx=4 の $xyxy\mapsto(1,1,r)$ を手計算で照合)。

---

## 6. 未閉鎖項・格の申告

| 項 | 内容 | 格 |
|---|---|---|
| 定義 D1・命題 P1/P2・補題 C2-CYC/C2-STR | 紙の証明 | **紙の証明・Sol 監査未・Lean 未** |
| 定理 C2-FIN・命題 C2-COC・命題 D-ODD・系 C2-QR/QR2 | 紙の証明 + 記号検算 | **紙の証明・Sol 監査未・Lean 未** |
| $d$ センサス・348 元の関係式実測・5,088 対の cocycle 実測 | python + GAP 一致、$|\gamma_2|$ は既存 cert と独立一致 | **candidate(同一設計者の二実装)+ $|\gamma_2|$ のみ cross-checked** |
| §4 の C2-Q への回答 | 定理 C2-FIN からの直接の帰結 | **定理の系** |
| 【GAP】C2-G1($c\notin N$) | 未導出(実害ゼロ) | **UNKNOWN(明示)** |
| 【U1】(3) 深いフィルトレーション | 未着手 | **UNKNOWN(明示)**・【文献要請】§4.5 |
| 【U2】$3\mid d$ 窓の genuine 側の全値実現 | 循環を避けて未主張 | **UNKNOWN(明示)** |

**$K^{(5)}$ 非接触を申告**(本稿は $K^{(5)}$ の値を一切読んでいない。§5.1 の K⁽⁵⁾ 行は $G_5$ の群構造 $|P|,|\gamma_2|,|\gamma_3|$ のみで、shadow の値ではない)。

---

# 追記 A(便 99 検収・裁定 412)— erratum 1 件・**撤回 2 件**

> **追記型**: §0–§6 の本文を**一切改変しない**。以下は erratum(記法の訂正)と**撤回**(系 C2-QR2 / §4.2 のメタ論証)である。
> 起草: 数学者(Opus 5)・2026-08-02。入力 = **Sol 便 99 返信 F99-3.8 / W99-3.4 / W99-3.5**(`sol/sol_reply_99_math26.md` §3.6)。

## A.0 検収の結果(先に 3 行)

1. **個別核は PASS**: 有限定義 D1・命題 P1/P2・自然性・**真の法が $8d$** であること・定理 C2-FIN・命題 C2-COC・命題 D-ODD、および結論 **R3(層 (b) の分離能力は厳密ゼロ)** は通った。
2. **erratum 1 件**: D1 の自由群版の表示で、最初の矢印は同型でなく**核 $\gamma_3(F_2)$ をもつ全射**(§A.1)。
3. ★ **撤回 2 件**: **系 C2-QR2 は現形で偽**(反例あり・§A.2)。**§4.2 の一般メタ論証は差戻し**、限定命題 **P99-C2-BLIND** へ差し替え(§A.3)。**R3 はこの 2 件の撤回に依存していない**(§A.2.4・§A.3.3)。

## A.1 【erratum F99-3.8】D1 の自由群版の矢印

**該当箇所**: §1.4「自由群版との橋(実用形)」の
$$c_2^{\mathrm{raw}}: \gamma_2(F_2) \xrightarrow{\ \sim\ } \gamma_2(F_2)/\gamma_3(F_2)\cong\mathbb Z .$$

**誤り**: 最初の矢印は**同型ではない**。正しくは

$$\boxed{\ c_2^{\mathrm{raw}}:\ \gamma_2(F_2)\ \twoheadrightarrow\ \gamma_2(F_2)/\gamma_3(F_2)\ \xrightarrow{\ \sim\ }\ \mathbb Z\ }$$

— **第 1 矢印は核 $\gamma_3(F_2)$ をもつ全射**、同型は**商から $\mathbb Z$ への矢印だけ**である($\gamma_3(F_2)\ne1$ なので $\gamma_2(F_2)$ 自身は $\mathbb Z$ と同型でない)。

**影響**: なし。§1.4 の証明は「$c_2^{\rm raw}$ が $\gamma_2(F_2)$ 上の**準同型**であること」しか使っておらず、単射性を使っていない。well-defined 性の議論($c_2^{\rm raw}(N_{F_2}\cap\gamma_2(F_2))=d\mathbb Z$)も不変。

## A.2 【撤回 W99-3.4】系 C2-QR2 は**現形で偽**

### A.2.1 反例(Sol 提示・当方で再現)

| $d$ | $c_2$ | $1+24c_2$ | $\bmod\ 8d$ | $\bmod\ 8d$ の平方か | $\exists m:3c_2\equiv\frac{m(m+1)}2\ (d)$ |
|---|---|---|---|---|---|
| **5** | 3 | 73 | $33\ (\bmod\ 40)$ | ✗ **非平方** | ✗ **解なし** |
| **15** | 3 | 73 | $73\ (\bmod\ 120)$ | ✗ **非平方** | ✗ **解なし** |

($\bmod\ 40$ の平方は $\{0,1,4,9,16,20,24,25,36\}$ で $33$ を含まない。)

### A.2.2 誤りの正確な所在(**向きの取り違え**)

§2.7 の証明は
> 「$3\nmid d$ なら $3$ は $\mathbb Z/d$ で可逆ゆえ常に可解」

と書いたが、これが示しているのは「**$m$ を与えて $c_2$ を解く**」向き($c_2\equiv3^{-1}\frac{m(m+1)}2$)であって、系 C2-QR が問うている「**$c_2$ を与えて $m$ を解く**」向きではない。後者は $m$ についての二次合同式であり、可解性は自動でない。
$3\mid d$ の分岐も同様で、証明が示したのは「$3c_2\equiv\frac{m(m+1)}2$ が **$\bmod\ 3$ で**可解」までであり、**$\bmod\ d$(同値に $\bmod\ 8d$ の平方根)全体**を結論できない。

### A.2.3 訂正後の正しい射程

> ### 系 C2-QR(**不変・正しい**)
> $c_2\in\mathbb Z/d$ に対し「それを実現する $m$ が存在する」$\iff$「$1+24c_2$ が $\mathbb Z/8d$ の平方」。
> ### 系 C2-QR2(**撤回**)
> 「可解性は自動」は**偽**。$3\nmid d$ でも $3\mid d$ でも反例がある(最小: $3\nmid d$ で $(d,c_2)=(5,3)$、$3\mid d$ で $(15,3)$)。
> ### ★ 逆向き使用の禁止(Sol の明示)
> 既存の genuine shadow から得た $c_2$ は **定理 C2-FIN により自動的に条件を満たす**(その shadow 自身が $m$ の証人だから)。しかしこれを**逆向きに「任意の $c_2$ が実現可能」へ使ってはならない**。実際の GT-shadow の実現には、$\lambda$ の $N_{\rm ord}$ での単元性・hexagon・全射性・$f$ の存在が**別に**要る。

### A.2.4 下流への影響(**R3 は無傷**)

| 依存箇所 | 影響 |
|---|---|
| **R3 / §4.1(分離能力ゼロ)** | ★ **無傷**。根拠は**定理 C2-FIN そのもの**(全 shadow が関係式を満たす)であって C2-QR2 ではない |
| **§4.3 (i)**「系 C2-QR2 によりその部分に hexagon は何の制約も課さない」 | ⚠ **根拠を差し替え**。正しい根拠は **C2-FIN の形**そのもの: $3c_2$ しか決まらないので、$3\mid d$ の窓では $c_2$ の $\mathbb Z/3$ 成分に hexagon は何の制約も課さない。**C2-QR2 を経由しない**(実際の shadow については $m$ が既に存在するので可解性は問題にならない) |
| **§2.7 の「判定は一度も落ちない」** | ⚠ **撤回**。任意の $c_2\in\mathbb Z/d$ については落ちる場合がある。**実在の shadow については落ちない**(証人が居るから)— この 2 つを区別する |
| **§4.3 (ii)・§4.4 の U1/U2/U3** | 不変 |
| **命題 D-ODD($4\nmid n\Rightarrow d=1$)** | 不変(C2-QR2 と無関係) |

### A.2.5 検算(独立・整数演算のみ)

**script**: `search/probe/noent3_v1/c2qr2_counterexample_check.py`
**SHA-256**: `bf37b5d29ef0fde650514820595a411389254c1ae1c1149e803e1149173b7d89`

| # | 検査 | 実測 |
|---|---|---|
| (1) | Sol の反例 2 件の逐点再現 | $(5,3)$: $33\ (40)$ 非平方・$m$ 解なし / $(15,3)$: $73\ (120)$ 非平方・$m$ 解なし |
| (2) | **系 C2-QR の同値**を $1\le d\le60$ の全 $(d,c_2)$ で確認 | **不一致 0**(= C2-QR は正しい) |
| (3) | C2-QR2 の「常に可解」の**反例の個数** | $1\le d\le60$ で **730 対**(うち $3\nmid d$ が 559・$3\mid d$ が 171)。最小 $d$: $3\nmid d$ で **5**、$3\mid d$ で **15**(= Sol の 2 例が最小) |
| (4) | 「$m$ から $c_2$ を解く」向きは $3\nmid d$ で常に可能 | **失敗 0**(= §A.2.2 の診断の裏取り) |

**格**: 単系統 python・整数演算のみ。**cross-checked でも Lean でもない。$K^{(5)}$ 非接触**(純粋な合同計算)。

## A.3 【差戻し W99-3.5】§4.2 の一般メタ論証 → 限定命題 P99-C2-BLIND

### A.3.1 何が偽か

§4.2 は 2 つのことを言っていた。

1. 「$\mathrm{GT}(N)$ の全元が満たす恒等式は定義条件の帰結でしかありえない」— ★ **一般には偽**。**ある有限対象の全点が偶然満たす恒等式はあり得る**(全称量化は有限集合上の偶然を排除しない)。
2. 「$(m,\bar f)$ の任意の関数として書ける不変量は原理的に pentagon の破れを検出できない」— ★ **広すぎる**。外部の source map / pentagon evaluator を組み込んだ関数なら、**同じデータ表現から破れを評価し得る**。

### A.3.2 採用する限定命題(Sol 逐語)

> ### P99-C2-BLIND
> gentle の定義 axioms(hexagon + charming)**だけから全称的に導かれる invariant** は、それら axioms を満たす候補同士を**分離できない**。とくに **C2-FIN だけから得る $c_2$ は pentagon の独立 detector ではない**。

**併記すべき注記(Sol の指示・逐語趣旨)**:
- 一般の $(m,\bar f)$-invariant まで blind と言うには、**その invariant が gentle-axiom quotient を経由するという factorization theorem が別途必要**である。
- **GTPI のような cross-frame 評価はこの限定の外にある**(枠をまたぐ評価器は $(m,\bar f)$ 表現の上に書けても、gentle axioms だけからは導かれない)。

### A.3.3 §4.2 の結論文の訂正

§4.2 の末尾は「⟹ 層 (b) を動かす**唯一の道**は枠をまたぐ比較である」と書いていた。**「唯一」は撤回する。** 正しくは:

> **本稿の $c_2$(= C2-FIN 経由で gentle axioms から全称的に出る量)では層 (b) は動かない**(P99-C2-BLIND)。**枠をまたぐ比較(GTPI / $PB_4$ / HS Prop. 7)は動かしうる道の一つとして生きている**が、「他に道が無い」ことは**証明されていない**(§4.4【U1】= より深いフィルトレーションは依然 UNKNOWN)。

> ### ⚠ 司令塔への波及(要判断)
> **裁定 408 の文言**「層 (b) は GTPI / HS Prop 7 **のみ**が道と確定」は、この差戻しにより**「のみ」を弱める**必要がある(確定しているのは「$c_2$ では動かない」まで)。**LEDGER の裁定本文は履歴として不改変**とし、**本追記を effective source** として地図・CLAIMS 側の記述を更新されたい(【ruling propagation check】)。

## A.4 この追記が変えないもの

- 定義 D1・命題 P1/P2・補題 C2-CYC/C2-STR・**定理 C2-FIN**・命題 C2-COC・**命題 D-ODD**・系 C2-QR の言明と証明。
- §3 の計算仕様(発注前ゲート G0/G1/G2 を含む)・§5 の実測(348 元・5,088 対)・§6 の格付け表。
- **$K^{(5)}$ 非接触の申告。**

