# 補題 B-6$^{\rm tw}$ の **link-free proof ID** — $\bar t_M$ を追った全文導出(v1)

**状態札: `candidate(単系統・Sol 未監査)/ BFC v2 本文は不改変(本稿は別 proof ID の提示)/ Lean 検証ではない / 値の名指しはしない / 封印非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05・**新設 v1**
- 委嘱: 司令塔(裁定 517)「$\bar t_M$ を追った B-6$^{\rm tw}$ の全文導出(link-free proof ID)を起草。BFC v2 §13.1【v2.7・F7】表の**自認欠落**を埋める 1 本の一般論。twisted 指数 $b_{\rm op}=(\bar t_M\varepsilon)^{-1}$ の **well-defined 性**と **$\gamma$ 非依存性**を正面から。(M-a) への接続を明記」
- **依拠(repo 内のみ・外部文献ゼロ)**: `docs/week4-BFC攻略_opus_v2.md` §2(TB1–TB4・(TB4$^{\rm u}$)・(2.1)(2.1′)・(TB2′)=$(Z_{2M}$-link$)$)/ §5(命題 B-1・**命題 B-2**・定理 B-3)/ §6.3(**系 B-4c**)/ §7・§7.1(補題 B-5・**補題 B-5$^{\rm u}$**・(7.1)(7.2))/ §8(**補題 B-6** と第 3 段の link 使用箇所 box)/ §8.1(**補題 B-6$^{\rm tw}$・定理 B-7$^{\rm tw}$**・U5)/ §10(**系 B-8**)/ §13.1(前件表・**F7 の link 要否表**)。`docs/notes/match_one_supply_v1.md`(MOS・裁定 517)/ `docs/notes/s3_family_completion_v1.md`(補題 Λ-REG・定理 SIXP-fam・【MATCH-one】)/ `sol/sol_reply_103_math30.md` §4・§5

> ## 遵守申告
> - **BFC v2 本文は 1 行も改変していない。** 本稿は F7 表が「**未提示**」と自認した行 —「B-6$^{\rm tw}$(link-free proof ID)」— を**別 proof ID として全文提示**するものである(便 51 F2.2 の要求形: 現行 proof と混ぜない)。**現行 proof ID(link を前件にもつ)は有効なまま**であり、本稿はそれを置換しない。
> - **値の名指しをしない**: 本稿が出すのは「**ある単元 $b$ が存在して一意**」までである。$b=1$ も $b=\varepsilon^{-1}$ も**主張しない**(それらは link と exact (TB4) を要する特殊化であり §6 で**含意の向きだけ**を書く)。BFC v2 §10.1.5 の「shadow を特定の Kummer 類として名指しする言明」には**触れない**。
> - **矢印跨ぎ禁止**: $\mathrm{ord}([u_n]_{2n})$・$\mathrm{ord}(a_n)$・$\mathrm{Ih}$ の全射性には触れない。
> - **封印非接触**: $K^{(5)}$ の値・窓データ・測定値・Rule 1 の実測 $\hat b_i$ に触れていない。§7 で $K^{(5)}$ に言及するのは「**凍結された命名がある窓では凍結命名を使う**」という手続き規律としてのみ。

---

## 0. 判定(先に 4 行)

| # | 問い | 判定 |
|---|---|---|
| **①** | **link-free proof は立つか** | ★★ **立つ**(§4 補題 B-6$^{\rm tw}$-lf)。前件は **(TB1)(TB2)(TB3)(TB4$^{\rm u}$)+(W1)–(W5)+(CAL)**。**$(Z_{2M}$-link$)$ は要らない** |
| **②** | **$b$ の well-defined 性・$\gamma$ 非依存性** | ★★ **正面から閉じた**(§5)。$b$ は $\tau^{-1}\circ\bigl(c_\Lambda\,m(\cdot)\,c_\Lambda^{-1}\bigr)\in\mathrm{Aut}(\mu_M)$ の**指数として内在的に定義**される — $G_K$ も $\gamma$ も root object も**現れない**。一意性は $\tau$ の単射性から |
| **③** | **$\bar t_M$ はどこへ行ったか** | ★ **値の同定にだけ現れる**(§6 系 B-6$^{\rm tw}$-val)。root object が供給される窓では $b=(\bar t_M\varepsilon)^{-1}=b_{\rm op}$ となり**現行 proof ID と一致**。$(Z_{2M}$-link$)$($t_{2M}=1$)+ exact (TB4)($\varepsilon=1$)で $b=1$ = 補題 B-6 (8.1) を回復 ⟹ **両 proof ID は矛盾せず、link-free 版が現行版を含む** |
| **④** | **(M-a) は閉じるか** | ★★ **閉じる**(§9)。窓 $(K^{(n)},H_{2,1,0})$ で 定理 B-7$^{\rm tw}$-lf が **MOS-1 を逐語で与える**。⟹ **$(Z_{2M}$-link$)$ は (M-a) の鎖から完全に落ち、$n=7,9$ の `not_assessed` は障害でなくなる**。⚠ ただし §10 の 2 点(値の名指し・黒箱の継承)は閉じない |

---

## 1. 何を埋めるのか — F7 表の自認欠落

BFC v2 §13.1【v2.7・F7】「前件の型列挙 — link 要否まで」の当該 2 行(逐語):

> | **B-6$^{\rm tw}$(現行 proof ID)** | TB1,TB2,TB3,TB4$^{\rm u}$+$(Z_{2M}$-link$)$+(W1)–(W5)+(CAL) | **必要**(現行 proof は link を前件にもつ) |
> | **B-6$^{\rm tw}$(link-free proof ID・未提示)** | TB1,TB2,TB3,TB4$^{\rm u}$+(W1)–(W5)+(CAL) | **不要**。ただし $\bar t_M$ を追った導出を**別 proof ID として全文提示**する必要がある(便 51 F2.2) |

**本稿はこの第 2 行を提示する。** 現行 proof ID の何がどこで link を呼んでいたかは BFC v2 §8 が特定済である(逐語):

> 上の 1 と 2 が生む等式は、根 object を区別して書くと
> $$\underbrace{c_\Lambda\,m(\zeta_M^{\rm TB2})\,c_\Lambda^{-1}}_{\text{1 段: (TB4) の }\sigma_\zeta\text{ 由来}}=\underbrace{\tau(\zeta_M^{\rm Rule1})}_{\text{2 段: }\tau\text{ の命名}}$$
> **第 3 段の「生成元 $\zeta_M$ で一致するから」は、この左右の $\zeta_M$ が同じ元であることを要する** — すなわち $(Z_{2M}$-link$)$。

$$\boxed{\ \textbf{本稿の方針: 左右の生成元を最後まで区別したまま、\textbf{生成元非依存}の補題で閉じる。}\ }$$

---

## 2. 記号と入力(既在の黒箱の**型**だけを使う)

窓 $(N,H)$、$P=F_2/\bar N$、$X\in P$、$M:=\mathrm{ord}(X)$、$K:=\mathbf Q(\zeta_{2M})$、$\Lambda:=H$ の $P$-共役類、$\mathrm{Fib}:=\mathrm{Fib}_{\vec{01}}(W_0)$。

| 記号 | 型 | 出所(**黒箱として引用**) |
|---|---|---|
| $m:\mu_M\to\mathrm{Sym}(\mathrm{Fib})$ | **単純推移**($\mathrm{Fib}$ は $\mu_M$-torsor) | BFC v2 **(7.1)**(補題 B-5(iii)/ **B-5$^{\rm u}$**) |
| $\tau:\mu_M\to\mathrm{Sym}(\Lambda)$ | **単射準同型**。$\tau(\zeta^\tau)=\mathrm{conj}_X$ という**命名**で定まる($\zeta^\tau$ は $\mu_M$ の**ある生成元**) | week4 v3 §5.2.0 の定義 / BFC v2 **命題 B-2**((W3)+(W4) の下で $\lvert\Lambda\rvert=M$・$\tau$ 単射・regular) |
| $c_\Lambda:\mathrm{Fib}\xrightarrow{\sim}\Lambda$ | 全単射・**$\hat F_2$-同変**・**$G_K$-同変**。$x$ の作用が $\mathrm{conj}_X=\tau(\zeta^\tau)$ に対応 | BFC v2 **系 B-4c** |
| $\sigma_\zeta$ | $\mathrm{Gal}(\Omega/\bar{\mathbf Q}((\beta)))$ の生成元。$\beta^{1/n}\mapsto\zeta_n^{\rm TB2}\beta^{1/n}$、$\bar{\mathbf Q}$ 上恒等 | **(TB2)** |
| $\varepsilon\in\hat{\mathbf Z}^\times$ | $x=\iota(\sigma_\zeta^{\,\varepsilon})$ — **一意に存在** | **(TB4$^{\rm u}$)+ (2.1)**(同じ procyclic 群の 2 つの位相的生成元) |
| $\kappa_{u^{-1}}:G_K\to\mu_M$ | 局所 Kummer 指標。**元で添字づけられ生成元非依存** | BFC v2 **(7.2)**(補題 B-5$^{\rm u}$) |

> ### ⚠ 本稿が**仮定しない**もの(ここが現行 proof ID との差)
> - $\zeta^\tau=\zeta_M^{\rm TB2}$($=$ $(Z_{2M}$-link$)$ の level $M$ 帰結)— **仮定しない**。
> - $\varepsilon=1$(exact (TB4))— **仮定しない**。
> - 窓ごとの **Rule 1 root object の存在** — **仮定しない**(§7 で決着)。

---

## 3. 補題 TORS-U(**生成元非依存の torsor 比較**・有限群論・自足)

> ### 補題 TORS-U【candidate・本稿の道具】
> $A$ を位数 $M$ の**有限巡回群**、$\mathrm{Fib},\Lambda$ を有限集合とし
> - $m:A\to\mathrm{Sym}(\mathrm{Fib})$ は**単純推移**な作用、
> - $\tau:A\to\mathrm{Sym}(\Lambda)$ は**単射**準同型、
> - $c:\mathrm{Fib}\to\Lambda$ は全単射
>
> とする。さらに **$A$ のある生成元の対 $(a_0,a_1)$** について
> $$c\circ m(a_0)\circ c^{-1}=\tau(a_1)\tag{TU-gen}$$
> が成り立つとする。このとき
> $$\boxed{\ \exists!\,b\in(\mathbf Z/M)^\times\ \text{s.t.}\ c\circ m(a)\circ c^{-1}=\tau\bigl(a^{\,b}\bigr)\quad(\forall a\in A).\ }$$

**証明.**
1. $\Phi:A\to\mathrm{Sym}(\Lambda)$、$\Phi(a):=c\,m(a)\,c^{-1}$ と置く。固定した全単射による共役は群同型 $\mathrm{Sym}(\mathrm{Fib})\to\mathrm{Sym}(\Lambda)$ を与えるので、$\Phi$ は準同型であり、$m$ が単純推移(ゆえに単射)だから $\Phi$ も**単射**。
2. **像の一致**: $a_0$ は $A$ を生成するから $\Phi(A)=\langle\Phi(a_0)\rangle$。(TU-gen) より $\Phi(a_0)=\tau(a_1)$ で、$a_1$ が $A$ を生成し $\tau$ が単射だから $\langle\tau(a_1)\rangle=\tau(A)$。よって
$$\Phi(A)=\tau(A).$$
3. $\tau$ は単射だから $\tau:A\to\tau(A)$ は同型。$\psi:=\tau^{-1}\circ\Phi:A\to A$ は**単射準同型**で、$A$ は有限だから**自己同型**。
4. $A$ は位数 $M$ の巡回群ゆえ $\mathrm{Aut}(A)\cong(\mathbf Z/M)^\times$、すなわち一意な $b\in(\mathbf Z/M)^\times$ があって $\psi(a)=a^{\,b}$。定義より $\Phi(a)=\tau(\psi(a))=\tau(a^b)$。
5. **一意性**: $\tau(a^{b})=\tau(a^{b'})$ が全 $a$ で成り立てば、$\tau$ 単射より $a^{b-b'}=1$ が全 $a\in A$ で成り立ち、生成元に適用して $b\equiv b'\ (\mathrm{mod}\ M)$。∎

> **★ この補題の要点**: 結論の $b$ は **$(c,m,\tau)$ だけから決まる**。**どの生成元を「$\zeta_M$」と呼ぶかは一切現れない** — (TU-gen) は「**ある**生成元の対で一致する」という形でしか使われない。**現行 proof の第 3 段が要求していた「左右の $\zeta_M$ が同じ元」は、ここでは不要である。**
>
> **⚠ 前件 2 の必要性**: (TU-gen) を落とすと $\Phi(A)$ と $\tau(A)$ が $\mathrm{Sym}(\Lambda)$ の**別の**部分群になりうるので、$\psi$ が定義できない。**「生成元の対で 1 回だけ一致する」ことがちょうど必要な入力**である。

---

## 4. 補題 B-6$^{\rm tw}$-lf(**link-free proof ID**)

> ### 補題 B-6$^{\rm tw}$-lf【candidate / proof ID: `b6tw-linkfree/v1`】
> **前件: (TB1)(TB2)(TB3)(TB4$^{\rm u}$) + (W1)(W2)(W3)(W4)(W5) + (CAL)。$(Z_{2M}$-link$)$ は仮定しない。**
> このとき
> $$\boxed{\ \exists!\,b\in(\mathbf Z/M)^\times:\qquad c_\Lambda\circ m(\xi)\circ c_\Lambda^{-1}=\tau\bigl(\xi^{\,b}\bigr)\qquad(\forall\xi\in\mu_M)\ }\tag{8.2-lf}$$

**証明.**

**第 1 段($\sigma_\zeta$ の $\mathrm{Fib}$ 上の作用)**。補題 B-5$^{\rm u}$ の (7.1) より
$$\mathrm{Fib}=\bigl\{\,\xi\,(u^{-1})^{1/M}\beta^{1/M}\ :\ \xi\in\mu_M\,\bigr\}\subset\Omega .$$
(TB2) により $\sigma_\zeta$ は $\bar{\mathbf Q}$ 上恒等で($u\in K^\times\subset\bar{\mathbf Q}$ ゆえ $(u^{-1})^{1/M}$ も $\xi$ も固定する)、$\beta^{1/M}\mapsto\zeta_M^{\rm TB2}\beta^{1/M}$。ゆえに
$$\sigma_\zeta\ \text{の}\ \mathrm{Fib}\ \text{上の作用}\ =\ m\bigl(\zeta_M^{\rm TB2}\bigr).$$
(この段は補題 B-6 の第 1 段と**同じ計算**だが、$x$ との同一視は**行わない**。)

**第 2 段($x$ の $\mathrm{Fib}$ 上の作用)**。(TB4$^{\rm u}$) より $x$ の作用は $I_0$ の像に属し $\Omega$ への後合成である。(2.1) の $\varepsilon\in\hat{\mathbf Z}^\times$ により $x=\iota(\sigma_\zeta^{\,\varepsilon})$ だから
$$x\ \text{の}\ \mathrm{Fib}\ \text{上の作用}\ =\ m\bigl(\zeta_M^{\rm TB2}\bigr)^{\varepsilon}\ =\ m\bigl((\zeta_M^{\rm TB2})^{\varepsilon}\bigr)$$
($\mu_M$ は位数 $M$ ゆえ $\hat{\mathbf Z}$ の作用は $\bmod\,M$ で効く)。ここで
$$a_0:=(\zeta_M^{\rm TB2})^{\varepsilon}\ \textbf{は }\mu_M\textbf{ の生成元である}$$
— $\zeta_M^{\rm TB2}$ は原始 $M$ 乗根、かつ還元 $\hat{\mathbf Z}^\times\to(\mathbf Z/M)^\times$ は群準同型なので $\varepsilon\bmod M\in(\mathbf Z/M)^\times$ だから。

**第 3 段($\Lambda$ への輸送)**。系 B-4c より $c_\Lambda$ は $\hat F_2$-同変で、$x$ の $\Lambda$ 上の作用は $\mathrm{conj}_X$、すなわち $\tau$ の命名により $\tau(\zeta^\tau)$(命題 B-2 の (B2-bij):左移動 $L_X\leftrightarrow\mathrm{conj}_X$)。ゆえに
$$c_\Lambda\circ m(a_0)\circ c_\Lambda^{-1}=\tau(a_1),\qquad a_1:=\zeta^\tau\ (\mu_M\ \text{の生成元}).$$
**ここで $a_0$ と $a_1$ を同一視しない** — これが現行 proof ID との唯一の差である。

**第 4 段(補題 TORS-U の適用)**。$A=\mu_M$(位数 $M$ の巡回群)、$m$ は (7.1) より単純推移、$\tau$ は単射((W3)(W4)+命題 B-2)、$c_\Lambda$ は全単射(系 B-4c)、第 3 段が (TU-gen) を与える。よって 補題 TORS-U より一意な $b\in(\mathbf Z/M)^\times$ が存在して (8.2-lf)。∎

> ### 前件の使用箇所(悉皆・自己申告)
> | 前件 | 使用箇所 |
> |---|---|
> | (TB2) | 第 1 段($\sigma_\zeta$ の定義と $\bar{\mathbf Q}$ 上恒等・係数作用) |
> | (TB4$^{\rm u}$) + (2.1) | 第 2 段($x$ が $I_0$ の像・$\varepsilon$ の存在と一意性) |
> | (TB1)(TB3) | 系 B-4c と (7.1) の背後(黒箱経由) |
> | (W4) | (7.1)(補題 B-5$^{\rm u}$(i)(iii))・命題 B-2 |
> | (W3) | 命題 B-2($\tau$ 単射・$\lvert\Lambda\rvert=M$) |
> | (W1)(W2)(W5)+(CAL) | 定理 B-4 / 系 B-4c(黒箱経由) |
> | **$(Z_{2M}$-link$)$** | ★ **使用箇所なし** |
> | **exact (TB4)** | ★ **使用箇所なし** |

---

## 5. $b$ の well-defined 性と $\gamma$ 非依存性(委嘱の正面課題)

### 5.1 内在的定義

補題 TORS-U の証明が与えるのは、単なる存在ではなく**構成**である:

$$\boxed{\ b\ :=\ \bigl(\tau^{-1}\circ\Phi\bigr)\ \text{の指数},\qquad \Phi(\xi):=c_\Lambda\,m(\xi)\,c_\Lambda^{-1},\qquad \tau^{-1}\circ\Phi\in\mathrm{Aut}(\mu_M)\cong(\mathbf Z/M)^\times.\ }$$

| 要件 | 根拠 |
|---|---|
| **存在** | $\tau^{-1}\circ\Phi$ が $\mu_M$ の自己同型であること(TORS-U 3・4)。$\Phi(A)=\tau(A)$ が第 3 段の生成元一致から出る |
| **一意性** | $\tau$ の単射性(TORS-U 5)。$\tau$ の単射性は (W3)(W4)+命題 B-2 が供給し、$K^{(n)}$ 族では **補題 Λ-REG**(`s3_family_completion_v1.md` §3)が全 $\alpha\ne0$ で供給する |
| **単元性** | $\mathrm{Aut}$(巡回群 $C_M$)$=(\mathbf Z/M)^\times$。**逆元 $b^{-1}$ も自動的に存在** |
| ★ **$\gamma$ 非依存** | **定義に $G_K$ が現れない。** $b$ は $(c_\Lambda,m,\tau)$ の関数であり、これらは窓データと枠組みデータだけで決まる。$\gamma\in G_K$ が現れるのは §8 の (B7tw-lf) で $\xi=\kappa_{u^{-1}}(\gamma)$ を**代入する段**であり、そこでは $b$ は既に確定している |

$$\Longrightarrow\quad\boxed{\ \textbf{(8.2-lf) は }\mu_M\textbf{ 上の準同型の恒等式であって、}\gamma\textbf{ を含まない。ゆえに }b\textbf{ は全 }\gamma\textbf{ に一様な単一の単元である。}\ }$$

### 5.2 ★ fitting 禁止(BFC v2 §8.1 U5・§15.8)との整合

U5 は「**$b$ は式から決まるのではなく、先に決めてから式に入れる**」「$G_K$-character を見てから $b$ を fitting することは**禁止**」と定め、出所を **(U-i)(数学: $\varepsilon$ から)**・**(U-ii)(実装: Rule 1 (7.1) の torsor 全体測定)** の 2 つに限定した。本稿の $b$ は**第 3 の出所**である:

> ### (U-iii)(内在)— 本稿が追加する出所
> $b$ は **torsor 比較の恒等式 (8.2-lf)** で決まる。この式は $\mathrm{Sym}(\Lambda)$ 内の**準同型の等式**であって、$G_K$-character の等式ではない。⟹ **$G_K$ のデータを一切見ずに $b$ が確定する。**

**なぜ U5 の禁止に抵触しないか(2 点)**:
1. **fitting される対象が違う**。U5 が禁じたのは「(B7tw) を満たすように $b$ を後から選ぶ」ことである。実際 U5 の反例(`PASS(ord1)` 分岐で $\kappa_i(G_K)=1$ なら $b\in\{1,3,7,9\}$ が同じ自明指標を与える)は、**(B7tw) が $b$ を決めないこと**を示す。本稿は (B7tw) から $b$ を決めていない — **(8.2-lf) から決めている**。
2. **(8.2-lf) には fitting の自由度がない**。TORS-U 5 の一意性により、$b$ は $(c_\Lambda,m,\tau)$ から**一意に**決まる。$\kappa$ の像が小さくても影響しない($\kappa$ が式に現れないから)。

> ★ **U5 の反例が本稿に効かないことの直接確認**: $\kappa_i(G_K)=1$ の窓でも、(8.2-lf) は $\mu_M$ **全体**上の等式なので $b$ は一意に定まる。U5 の非一意性は「$G_K$ の像が小さい」ことに由来し、**torsor 全体を見る (U-ii) と同じ理由で (U-iii) にも効かない**。

### 5.3 命名の取り替えに対する挙動(健全性検査)

$\tau$ の命名を $\zeta^\tau\mapsto(\zeta^\tau)^{s}$($s\in(\mathbf Z/M)^\times$)と取り替えると $\tau\mapsto\tau':=\tau\circ(\,\cdot\,^{s^{-1}})$ となり、(8.2-lf) の $b$ は $b\mapsto sb$ に変わる。**$b$ は命名に相対的な量である。** しかし
- $b$ は依然として**単元**であり、
- 系 B-8 により $R^{\rm cyc}_{\rm formal}$ の結論 (R6-full)・(7.4) は $b$ に依らない、
- $\tau(\mu_M[e])$ は $\mu_M[e]$ が特性部分群ゆえ命名に**不変**((6′) の像の等式は影響を受けない)

から、**命名の取り替えは (M-a) の用途に何の影響も与えない**(§9)。⟹ **$b$ の「値」を語らない限り、命名の自由は無害である。**

---

## 6. 系 B-6$^{\rm tw}$-val — **$\bar t_M$ を追った値の同定**と現行 proof ID との一致

ここで初めて root object を持ち込む。**この節の結論は (M-a) には使わない**(§10)。

> ### 系 B-6$^{\rm tw}$-val【candidate】
> 補題 B-6$^{\rm tw}$-lf の前件に加えて、当該窓が **Rule 1 の field-generator object** $\zeta_{2M}^{\rm Rule1}\in K$ を供給し、**$\tau$ がその level $M$ 冪で命名されている**、すなわち
> $$\zeta^\tau=\zeta_M^{\rm Rule1}:=\bigl(\zeta_{2M}^{\rm Rule1}\bigr)^2$$
> と仮定する。$t_{2M}\in(\mathbf Z/2M)^\times$ を $\zeta_{2M}^{\rm TB2}=(\zeta_{2M}^{\rm Rule1})^{t_{2M}}$ で定め $\bar t_M:=t_{2M}\bmod M$ と置くと
> $$\boxed{\ b\ =\ b_{\rm op}\ =\ \bigl(\bar t_M\,\varepsilon\bigr)^{-1}\bmod M\ }$$
> である。

**証明.**

**(a) level 降下(型が $\bar t_M$ になる理由)**。(TB2) の整合性 $\zeta_{2M}^2=\zeta_M$ と Rule 1 側の定義 $\zeta_M^{\rm Rule1}=(\zeta_{2M}^{\rm Rule1})^2$ から、level $2M$ の関係式を 2 乗して
$$\zeta_M^{\rm TB2}=\bigl(\zeta_{2M}^{\rm TB2}\bigr)^2=\bigl((\zeta_{2M}^{\rm Rule1})^{t_{2M}}\bigr)^2=\bigl(\zeta_M^{\rm Rule1}\bigr)^{t_{2M}}=\bigl(\zeta_M^{\rm Rule1}\bigr)^{\bar t_M}$$
($\zeta_M^{\rm Rule1}$ の位数は $M$ ゆえ指数は $\bmod\,M$ でしか効かない)。**これが BFC v2【v2.9・F2.2】の「level $M$ の式なので型は $\bar t_M$」の再導出である。** また $t_{2M}\in(\mathbf Z/2M)^\times\Rightarrow\bar t_M\in(\mathbf Z/M)^\times$。

**(b) 生成元の対の書き換え**。§4 第 2・3 段の $(a_0,a_1)$ は
$$a_0=(\zeta_M^{\rm TB2})^{\varepsilon}=\bigl(\zeta_M^{\rm Rule1}\bigr)^{\bar t_M\varepsilon}=(\zeta^\tau)^{\bar t_M\varepsilon},\qquad a_1=\zeta^\tau .$$

**(c) 指数の計算**。$\Phi\bigl((\zeta^\tau)^{\bar t_M\varepsilon}\bigr)=\tau(\zeta^\tau)$。$\bar t_M\varepsilon\in(\mathbf Z/M)^\times$ なので、任意の $k\in\mathbf Z/M$ に対し $j:=(\bar t_M\varepsilon)^{-1}k$ と置けば $k=\bar t_M\varepsilon j$ であり、$\Phi,\tau$ が準同型だから
$$\Phi\bigl((\zeta^\tau)^{k}\bigr)=\Phi\bigl((\zeta^\tau)^{\bar t_M\varepsilon j}\bigr)=\Phi\bigl((\zeta^\tau)^{\bar t_M\varepsilon}\bigr)^{\,j}=\tau(\zeta^\tau)^{\,j}=\tau\bigl((\zeta^\tau)^{j}\bigr)=\tau\Bigl(\bigl((\zeta^\tau)^{k}\bigr)^{(\bar t_M\varepsilon)^{-1}}\Bigr).$$
$\xi=(\zeta^\tau)^k$ は $\mu_M$ を走るので $\Phi(\xi)=\tau(\xi^{(\bar t_M\varepsilon)^{-1}})$。補題 B-6$^{\rm tw}$-lf の一意性より $b=(\bar t_M\varepsilon)^{-1}=b_{\rm op}$。∎

### 6.1 特殊化 — 現行 proof ID の回復(**両 ID の無矛盾性**)

| 追加前件 | 帰結 |
|---|---|
| $(Z_{2M}$-link$)$($\iff t_{2M}=1$) | $\bar t_M=1$ ⟹ $b=\varepsilon^{-1}=b_{\rm cmp}$ = **現行 B-6$^{\rm tw}$ (8.2)** |
| $(Z_{2M}$-link$)$ **かつ** exact (TB4)($\varepsilon=1$) | $b=1$ ⟹ **補題 B-6 (8.1)** |

$$\boxed{\ \textbf{link-free proof ID は現行 proof ID を}\textbf{特殊化として含む}\textbf{。両者は矛盾しない。}\ }$$

⚠ **ただし混ぜない**(便 51 F2.2 の規律): 本稿は**別 proof ID** であり、BFC v2 本文の現行 proof ID の前件欄を書き換えない。**「本稿は link-free でもある」と現行 proof に読み替えてはならない。**

> **★ (2.2) との整合**: $\bar t_M=1$ は $(Z_{2M}$-link$)$ の**必要条件であって十分条件ではない**(BFC v2【v2.7・F4.1】: $t_{20}=11$ の例)。本稿の $b$ の**値**は $\bar t_M$ にしか依らないので、**$b$ の観測から link の成否は判定できない** — この非可逆性は既在の指摘(2.2)と同型であり、本稿はそれを再確認するだけで新しい主張をしない。

---

## 7. ★ root object は (M-a) に要るのか — 自分の監査点 4 への回答

`match_one_supply_v1.md` §11 監査点 4 で私は「$\exists$ 単元 $b$ だけを結論とする導出に、**Rule-1 側 root object の窓ごとの存在は要るか**」を未決として残した。**本稿の §4 が答えを与える。**

> ### 回答: **要らない。**
> 補題 B-6$^{\rm tw}$-lf の証明に現れる第 2 の生成元 $a_1=\zeta^\tau$ は、**$\tau$ の命名に使われている生成元そのもの**である。$\tau$ は「$\mu_M\to\mathrm{Sym}(\Lambda)$ の準同型で $\tau(\zeta^\tau)=\mathrm{conj}_X$」として定義される以上、**$\zeta^\tau$ は $\tau$ の定義の一部**であって、**別途供給されるべき窓データではない**。
> ⟹ **`inventory=not_assessed` の窓($n=7,9$ 等)でも 補題 B-6$^{\rm tw}$-lf は成立する。**

**この読みを支える既在の記述**: BFC v2 §2【v2.7・F3.4】は $(Z_{2M}$-link$)$ を「**規約(無償)** — 新しい算術仮定ではなく**未指定だった比較データの選択**」と型付けている。すなわち link は**算術的事実ではなく、二つの命名の整合の要求**である。本稿は**二つの命名を突き合わせない**ので、その要求が発生しない。

### 7.1 ただし手続き上の 2 つの注意(誇張しない)

1. **凍結された命名がある窓では、凍結命名を使う。** $K^{(5)}$ は Rule 1 (1.5) が $\zeta_{20}^{\rm Rule1}:=\bar T$ を凍結している。**本稿を口実に命名を取り替えることは禁止**(凍結記録の破壊になる)。その窓では §6 の $b=b_{\rm op}$ の形で読む。
2. **命名の自由は「値を語らない」限りで無害**(§5.3)。**窓を跨いで $b$ の値を比較する言明**(補題 B-9′ 型の二 detector 比較)には、**同じ $M$・同じ root object**という既在の型条件が依然として要る(BFC v2【v2.11・F7-1-2】)。本稿はその型条件を緩めない。
3. ⟹ `match_one_supply_v1.md` §6 の「Route T の per-n 手続き = ゼロ」は**数学的には正しい**が、運用上は **C5-fam の R-2(ラベル規約)に「$\tau$ の命名」を 1 行記録することを推奨**する(seal 行為ではない・versioned 行為でもない)。**自認**(match_one v1 はこの 1 行に触れていなかった)。

---

## 8. 定理 B-7$^{\rm tw}$-lf(twisted comparison bridge・link-free)

> ### 定理 B-7$^{\rm tw}$-lf【candidate / proof ID: `b7tw-linkfree/v1`】
> **前件: (TB1)(TB2)(TB3)(TB4$^{\rm u}$) + (CAL) + (W1)–(W5)。$(Z_{2M}$-link$)$ は仮定しない。**
> 補題 B-6$^{\rm tw}$-lf の(一意な)$b\in(\mathbf Z/M)^\times$ について
> $$\boxed{\ \rho_\Lambda\bigl(\mathrm{Ih}_N(\gamma)\bigr)=\tau\bigl(\kappa_{u^{-1}}(\gamma)^{\,b}\bigr)\qquad(\forall\gamma\in G_K)\ }\tag{B7tw-lf}$$
> が成り立つ。$b$ は $\gamma$ に依らない(§5.1)。

**証明**(現行 B-7$^{\rm tw}$ の証明の 2 か所差し替え — 構造は同じ)。
1. **系 B-4c** の $G_K$-同変性より、$\Lambda$ 上の $\gamma$-作用は $\mathrm{Fib}$ 上の作用の $c_\Lambda$ による輸送:
$$\rho_\Lambda(\mathrm{Ih}_N(\gamma))=c_\Lambda\circ(\gamma\text{-作用})\circ c_\Lambda^{-1}.$$
2. **補題 B-5$^{\rm u}$ の (7.2)**(exact (TB4) を呼ばない)より $\gamma$-作用 $=m(\kappa_{u^{-1}}(\gamma))$。
3. **補題 B-6$^{\rm tw}$-lf (8.2-lf)** を $\xi=\kappa_{u^{-1}}(\gamma)$ に適用して
$$\rho_\Lambda(\mathrm{Ih}_N(\gamma))=c_\Lambda\,m\bigl(\kappa_{u^{-1}}(\gamma)\bigr)\,c_\Lambda^{-1}=\tau\bigl(\kappa_{u^{-1}}(\gamma)^{\,b}\bigr).$$
さらに **定理 B-3**((W1)–(W5) のみに依存)が $\rho_\Lambda\circ\mathrm{Ih}_N|_{G_K}=\tau\circ c$ の形を与えるので、$\tau$ の単射性より $c=\kappa_{u^{-1}}^{\,b}$。∎

> **⚠ 定理文の読み方(U5 の規律を継承)**: 「**§5.1 で内在的に定まった $b$** が (B7tw-lf) を満たす」。**「(B7tw-lf) を満たす $b$ が一意に存在する」ではない**($\kappa$ の像が小さい窓では後者は偽 — U5 の反例)。**順序が本質的である**: $b$ を先に (8.2-lf) で確定し、その後で $\gamma$ を代入する。

---

## 9. **(M-a) への接続** — MOS-1 が閉じる形(委嘱の必須節)

### 9.1 instantiation

窓を $\bigl(K^{(n)},\ H_n^{\rm fun}=H_{2,1,0}\bigr)$($n\ge3$ 奇)に取る。`match_one_supply_v1.md` §5 の記号で
$$P=G_n,\quad M=\mathrm{ord}(X)=2n,\quad K=\mathbf Q(\zeta_{2M})=\mathbf Q(\zeta_{4n})=F_n,\quad N=K^{(n)},\quad \Lambda=\Lambda_1 .$$

| 定理 B-7$^{\rm tw}$-lf の前件 | 族供給元 | 状態 |
|---|---|---|
| (TB1)(TB2)(TB3)(TB4$^{\rm u}$) | 枠組み。便 103 **F103-4** で (5′) は `theorem-framework-relative [TB: canonical-source-pinned/v2]` | 継承 |
| (W1) | W1-fam(全 $n$ 一斉) | 閉 |
| (W2) | (W2)-fam(裁定 120)+ W2-arith Route A(裁定 122) | candidate |
| (W3) | **ODD-H (1.3)**(補題 H(3))— 全 $\alpha\ne0$ | 証明済 |
| (W4) | **ODD-H 補題 G + 補題 C(2)** — 全 $\alpha$ | 証明済(登録主張は $\alpha=1$) |
| (W5) | Sol 便 73 (1.13)(1.14) + **定理 SIXP-fam(1)** | candidate |
| (CAL) | $A_5$ v4 §1.4(窓非依存) | 閉 |
| $\tau$ の単射性(命題 B-2 経由) | ★ **補題 Λ-REG**(`s3_family_completion_v1.md` §3)— 全 $\alpha\ne0$ | candidate |
| **$(Z_{2M}$-link$)$** | ★ **不要** | — |

### 9.2 MOS-1 の逐語一致

`match_one_supply_v1.md` §5.1 の **(MOS-1)**:
$$\exists b\in(\mathbf Z/2n)^\times\ (\gamma\ \text{に依らない}):\quad \rho_0\bigl(\mathrm{Ih}_{K^{(n)}}(\gamma)\bigr)=\tau\bigl(\kappa_{u^{-1}}(\gamma)^{\,b}\bigr)\quad(\forall\gamma\in G_{F_n}).$$

定理 B-7$^{\rm tw}$-lf は $M=2n$、$K=F_n$ でこれを**逐語で**与える($\gamma\in G_{F_n}$ に対し (W2) より $\mathrm{Ih}_N(\gamma)\in\mathfrak F_0$ だから $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\rho_0(\mathrm{Ih}_N(\gamma))$ — 定理 B-3 の第 1 段)。$\gamma$ 非依存性は §5.1。

$$\boxed{\ \textbf{(M-a) の供給 = 定理 B-7}^{\rm tw}\textbf{-lf の当該窓での適用。}\ (Z_{2M}\textbf{-link) は鎖から完全に落ちる。}\ }$$

### 9.3 下流(**ここから先は本稿の結論ではない**)

(M-a) が供給されれば、`s3_family_completion_v1.md` §12 の **定理 APPLY-fam** の前件 (M-a) が満たされる。ただし
- **(M-b)**(手元の類が当該窓の $[u_{n,\alpha}]_{2n}$ であること)は**本稿の射程外**(C1′ 系);
- **(M-c)**($\mathrm{ord}=n$)も**本稿の射程外**(総組立側);
- 系 B-8 が $R^{\rm cyc}_{\rm formal}$ の結論への輸送を与える(既在)。

**本稿は $\mathrm{Ih}$ の全射性を主張しない。**

---

## 10. 何が閉じ、何が閉じないか

| | 状態 |
|---|---|
| ★ **$\exists!$ 単元 $b$ の形の橋(MOS-1)** | **閉じた**(link 不要・§4・§8・§9) |
| ★ **$n=7,9$ の `not_assessed`** | **(M-a) の障害ではなくなった**(§7) |
| **$b$ の値の同定($b=1$ / $b=\varepsilon^{-1}$)** | ⚠ **閉じない**。**link + exact (TB4) が依然要る**(§6.1)。Rule 1 (7.1)(7.3) の $\hat b_i=1$ 受理検査は**本稿では discharge されない** |
| **shadow を特定の Kummer 類として名指しする言明**(BFC v2 §10.1.5) | ⚠ **閉じない**(exact $\varepsilon=1$ が要る)。`bridge_result_i` 系の `amendment-pending` は不変 |
| **窓を跨いだ $b$ の値の比較**(補題 B-9′ 型) | ⚠ **閉じない**(同一 $M$・同一 root object の型条件は不変・§7.1-2) |
| **黒箱の格** | 命題 B-2・系 B-4c・補題 B-5$^{\rm u}$・定理 B-3・定理 B-4 は**引用**であり本稿は再検証していない(【B6LF-GAP-1】) |

---

## 11. FINDING

| # | 格 | 内容 |
|---|---|---|
| **B6LF-1** | ★★ **link-free proof ID の提示** | 補題 B-6$^{\rm tw}$-lf(§4)。前件から $(Z_{2M}$-link$)$ と exact (TB4) が落ちる。**F7 表の「未提示」行が埋まる**。現行 proof ID は特殊化として含まれる(§6.1)⟹ 両 ID は無矛盾 |
| **B6LF-2** | ★★ **鍵は生成元非依存化** | **補題 TORS-U**(§3): 「$A$ の**ある**生成元の対で一致 ⟹ 全体で単元冪だけずれて一致」。現行 proof が要求した「左右の $\zeta_M$ が同じ元」は、**像の一致 $\Phi(A)=\tau(A)$ さえ言えれば不要**である。link が隠れていたのは**同一視のため**であって**数学的必要**ではなかった |
| **B6LF-3** | ★★ **$b$ の第 3 の出所 (U-iii)** | $b:=$ $\tau^{-1}\circ\Phi\in\mathrm{Aut}(\mu_M)$ の指数。**$G_K$ を見ずに確定**するので U5 の fitting 禁止に抵触しない。U5 の反例(`ord1` 分岐で $b$ が 4 通り)は **(B7tw) が $b$ を決めないこと**の例であり、**(8.2-lf) は $\mu_M$ 全体上の等式なので影響を受けない**(§5.2) |
| **B6LF-4** | ★ **root object 不要の決着** | `match_one_supply_v1.md` の監査点 4 に回答: $a_1=\zeta^\tau$ は **$\tau$ の定義の一部**であって別途供給される窓データではない。⟹ `not_assessed` 窓でも成立(§7) |
| **B6LF-5** | ★ **$\bar t_M$ の型の再導出** | level $2M$ の関係式を 2 乗すると指数は $\bmod\,M$ に落ちる(§6(a))。**BFC v2【v2.9・F2.2】の型付けを独立に再導出**した。また **$b$ の値は $\bar t_M$ にしか依らない**ので、**$b$ の観測から link の成否は判定できない**(既在 (2.2) と同型の非可逆性) |
| **B6LF-6** | ⚠ **自認(match_one v1 の補正)** | match_one v1 §6 の「Route T の per-n 手続き = ゼロ」は数学的には正しいが、**$\tau$ の命名を C5-fam に 1 行記録すること**を推奨に加える(seal 行為ではない)。凍結命名のある窓($K^{(5)}$)では**凍結命名を使う**(§7.1) |
| **B6LF-7** | ★ **命名の取り替えは無害** | $\tau$ の命名を単元 $s$ でひねると $b\mapsto sb$ だが、(i) $b$ は単元のまま、(ii) 系 B-8 で結論不変、(iii) $\tau(\mu_M[e])$ は特性部分群ゆえ不変 ⟹ **(6′) の像の等式も (M-a) も影響を受けない**(§5.3) |

## 12. 【GAP】

| 札 | 内容 | 重み |
|---|---|---|
| **【B6LF-GAP-1】** | **黒箱を再検証していない**: 命題 B-2・**系 B-4c**・補題 B-5$^{\rm u}$・定理 B-3・定理 B-4 は**型だけを引用**した。とくに系 B-4c の証明は「(TB4) が採る『$\Omega$ への後合成』は左作用」と書かれており、**私はこれを (TB4$^{\rm u}$) の内容(左作用)として読んだ**。この読みが誤りで系 B-4c が exact (TB4) を要するなら、本稿の連鎖も同じ前件を継承する(**ただし現行 B-7$^{\rm tw}$ の proof ID も同じ前件表を採るので、本稿だけが悪化することはない**) | 中 |
| **【B6LF-GAP-2】** | **値の同定は閉じない**(§10)。$b=1$ を要する言明(Rule 1 の $\hat b_i$ 受理検査・shadow の Kummer 類名指し)には link と exact (TB4) が依然要る | 中(射程) |
| **【B6LF-GAP-3】** | **(W2) は candidate**(裁定 120/122)。本稿の前件に入る | 中 |
| **【B6LF-GAP-4】** | 本稿は**単系統・Sol 未監査**。補題 TORS-U・補題 B-6$^{\rm tw}$-lf・系 B-6$^{\rm tw}$-val・定理 B-7$^{\rm tw}$-lf・(U-iii) はいずれも本稿が初出(**工房外の既知性は未調査**。torsor 比較の一意単元という形自体は標準的な議論であり、「初」とは書かない) | — |
| **【B6LF-GAP-5】** | **機械検算なし**(本稿は純粋に紙の議論・有限群論の 5 行補題)。既在の Node 検算 13/13・GAP 25/25 は現行 proof ID のもので、**本稿の新しい主張を検査していない** | 軽 |

**「verified」「cross-checked」は本稿で一度も使っていない。**

## 13. Sol への申し送り(監査点 4・優先順)

1. ★★ **補題 TORS-U の可否(最重要)**: 「$\Phi(a_0)=\tau(a_1)$($a_0,a_1$ は**生成元**)⟹ $\Phi(A)=\tau(A)$ ⟹ $\tau^{-1}\Phi\in\mathrm{Aut}(A)$ ⟹ 一意な単元冪」の 3 段に穴はないか。とくに **$\Phi(A)=\tau(A)$ を出す段**($a_0$ が生成元であること・$\tau$ が単射であること)が本稿の全体重を支えている。
2. ★★ **§4 第 3 段の読み(link が本当に落ちるか)**: 系 B-4c の結論「$x$ の作用が $\tau(\zeta_M)$ に対応する」を、**「$\tau$ の命名生成元 $\zeta^\tau$ での一致」**と読み、**$\zeta_M^{\rm TB2}$ との同一視を含まない**とした判読は正しいか。**もし系 B-4c の $\zeta_M$ が既に TB2 側の元を指しているなら、link は B-4c に移動するだけで消えない**(本稿の主張は撤回になる)。**これが本稿の生死を分ける一点である。**
3. ★ **(U-iii) の是非**: $b$ を「$G_K$ を見ずに (8.2-lf) で確定する」第 3 の出所として認めてよいか。U5 が禁じた fitting は **(B7tw) への当てはめ**であって **(8.2-lf) からの決定ではない**、という切り分けで足りるか。
4. ★ **命名の自由(§7)**: `inventory=not_assessed` の窓で $\tau$ の命名を自由に取れる(そして取り替えても (M-a) に無害である)という読みでよいか。**凍結命名のある窓では凍結命名を使う**という手続き規律で、Rule 1 側の記録と衝突しないか。

## 14. 出所

| 節 | 主たる出所 |
|---|---|
| §1 | BFC v2 §13.1【v2.7・F7】表 / §8 の link 使用箇所 box(裁定 54) |
| §2 | BFC v2 §2(TB1–TB4・TB4$^{\rm u}$・(2.1)(2.1′)・(TB2′))/ §5 命題 B-2 / §6.3 系 B-4c / §7.1 補題 B-5$^{\rm u}$(7.1)(7.2) |
| §3 | **本稿**(有限群論・自足)。命題 B-1(regular 可換部分群の自己中心化)と同型の道具立てだが**別命題**である |
| §4 | 上記の合成。第 1 段 = 補題 B-6 第 1 段の計算(同一視を除く)、第 2 段 = 現行 B-6$^{\rm tw}$ の (2.1) 使用、第 3 段 = 系 B-4c |
| §5 | BFC v2 §8.1 U5(便 46 F4)・§15.8 / 本稿 §3 |
| §6 | BFC v2 §2(2.1′)【v2.7・F4.1】【v2.9・F2.2】/ §8(8.1)/ §8.1(8.2) |
| §7 | BFC v2 §2【v2.7・F3.4】(link は「規約(無償)」)/ `match_one_supply_v1.md` §11 監査点 4 / Rule 1 (1.5)($K^{(5)}$ 凍結命名) |
| §8 | BFC v2 §9 定理 B-7 の証明構造 / §8.1 定理 B-7$^{\rm tw}$ の (a)(b) 差し替え / §5 定理 B-3 |
| §9 | `match_one_supply_v1.md` §5(MOS-1)・§4(族供給表)/ `s3_family_completion_v1.md` §3(補題 Λ-REG)・§5(定理 SIXP-fam)・§12(定理 APPLY-fam)/ 便 103 F103-4 |
| §10 | BFC v2 §10.1.5 / §10(系 B-8)/ 【v2.11・F7-1-2】 |

### 14.1 【文献要請】

**本稿からの新規はゼロ。** 本稿は既在の前件を**減らす**方向の仕事であり、外部文献を要さない(補題 TORS-U は有限巡回群の自己同型群の初等的事実のみを使う)。

### 14.2 司令塔への上申(3 点)

1. ★★ **監査点 2(系 B-4c の $\zeta_M$ の読み)を便 105 の最優先に置かれたい。** ここが崩れると本稿は撤回、立てば **(M-a) の per-window 会計が消える**。**二値の分岐点**である。
2. ★ **BFC v2 への反映は Sol PASS 後**。本稿は別 proof ID の提示であり、BFC v2 §13.1 F7 表の「未提示」を「提示済(`b6tw-linkfree/v1`)」に更新するのは**司令塔の裁定事項**。本稿は本文を改変していない。
3. ★ **`match_one_supply_v1.md` §6 に B6LF-6 の 1 行補正**($\tau$ の命名の C5 記録を推奨に追加)を反映されたい。**自認**。
