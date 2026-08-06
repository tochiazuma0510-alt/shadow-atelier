# B₄ 窓での 252 直接裁定 — 実現可能性ノート(v1)

**状態札: `candidate(実現可能性ノート・紙のみ / 機械は付録 A の記号計算+整数級数のみ / 本走宇宙の候補評価ゼロ / 封印非接触 / novelty 主張なし)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-06
- 委嘱: 司令塔(**裁定 598**)— 「NW(7) の 252(PENT_W-FAIL 非算術 shadow)の**身分**を、B₄ 本来系で直接裁けるか」。地図第 4 版の軸 (ii)(理論同定)の初手。
- 入力正本(すべて既在・本ノートは 1 バイトも改変しない):
  - `docs/notes/b4_original_gtshadows_extraction_v1.md`(2008.00066 抽出・§/式番号 pin 済)
  - `papers/txt/2008.00066-what-are-gt-shadows.txt`(**読んだ範囲は §9.1 に申告**)
  - `docs/notes/hs_prop7_translation_v1.md`(§1.0–1.5・§2.1・§5 定義 NW(p)+補題 NW-1b・§8.7.6–8.7.8)
  - `docs/notes/nw7_mainrun_predictions_iffirst_v1.md`(票 v1)/ 同 `_addendum_pentlayer_v1.md`
  - `docs/notes/hsp7_hexagon_arbitration_v1.md` §0–§1.1(**2401 Prop 3.4 の逐語**)
  - `docs/notes/auto_settled_check_v1.md` §3.4(補題 VERBAL-ISO)
  - `docs/notes/litgate_pentagon_v1.md`(余面 (A.18) の画像照合記録・Package GT の `penta`)

---

## 0. 結論(三択・先に 6 行)

> ## ★ 判定 = **条件付き実現可能**(工程表 = §8、欠けの列挙 = §9.2)

| # | 結論 |
|---|---|
| **0-1** | ★★ **委嘱の問いは二つに割れる。片方は既に裁定済み、もう片方は B₄ の管轄外である。** (α)「252 は B₄ 本来系の genuine か」= **既に否**(pentagon で死ぬ)。B₄ の寄与は**新情報ではなく、根拠の差し替え**(HS Prop 7 翻訳 → 2008 の公理そのもの)。(β)「252 の**内訳**(= gentle 系の genuine か)」= **B₄ では原理的に裁けない**。B₄ の極限は $\widehat{GT}$、内訳が問うのは $\widehat{GT}_{gen}$ だから。**法廷が違う**(§4.3)。 |
| **0-2** | ★★ **Prop 3.9 の持ち上げ窓は使えない。** $\tilde\psi$ 構成の窓(およびその $B_4$-核)では、**pentagon (2.20) が全 charming $f$ に対し恒真**である(**定理 B4-VAC**・§2.4・機械検算つき)。⟹ 「PENT_W-FAIL ⟹ (2.20)-FAIL」は**この窓では偽**であり、**252 の全件が反例**になる。Prop 3.9 は cofinality の存在定理であって計算レシピではない。 |
| **0-3** | ★★ 使える窓は **$\tilde{\mathbf N}^*:=\mathcal V(PB_4)=\gamma_5(PB_4)PB_4^{\,7}$**(同じ verbal 法則を arity 4 へ上げたもの)。$\tilde{\mathbf N}^*\in\mathrm{NFI}_{PB_4}(B_4)$、$\tilde{\mathbf N}^*_{PB_3}=\mathcal V(PB_3)=\mathbf N_0$(**厳密等号**)、$\tilde{\mathbf N}^*_{F_2}=N_{F_2}$、$\tilde N^*_{\rm ord}=7$、$\lvert PB_4:\tilde{\mathbf N}^*\rvert=7^{41}$、$PB_4/\tilde{\mathbf N}^*\cong C_7\times Q$(**定理 B4-CANON**・§2.5)。 |
| **0-4** | ★★ **hexagon 側は新情報ゼロが定理として出る。** 2401 **Prop 3.4** は hexagon 判定が $N_{F_2}$ のみに依存すると言う。$\tilde{\mathbf N}^*_{F_2}=N_{F_2}$ ゆえ、B₄ 窓での hexagon は**うちの hexagon と恒等に一致**(§3.4。独立に $c$-指数計算 = **補題 B4-KAPPA** でも確認)。⟹ **B₄ 裁定の実体は pentagon 1 本に完全に縮約される**。 |
| **0-5** | ★★ ゆえに、条件が揃えば $$\boxed{\ \mathrm{GT}^\heartsuit_{2008}(\tilde{\mathbf N}^*)\big\vert_{\rm practical}=\textbf{42},\qquad \textbf{その全元が genuine}\ }$$ が従う(**系 B4-42**・§3.5)。これは 2008 の **Question 4.7**(非 Abelian 窓で genuine を全同定できる例はあるか)が求める型の実例である。**novelty は主張しない**(§9.4)。 |
| **0-6** | ★ 内訳(β)は **1 ビット**に縮約できる(**命題 BIT-252**・§4.4): $\mathfrak G_{\rm gen}^{\rm gentle}(\mathbf N)\in\{42,\ 294\}$ のいずれかで、中間はない。**42 側は 1 元 × 1 窓 × 117,649 件の検査で決着する**(§4.5)。294 側なら $\widehat{GT}_{gen}\supsetneq\widehat{GT}$ が有限窓で証人つきになる。**この実験は B₃-gentle 側にあり、B₄ ではない。** |

> ### ★ 一行で
> **B₄ 法廷は既に評決を下している(252 = 非オブジェクト)。B₄ を建て増しする価値は「評決の根拠を HS 翻訳から 2008 の公理へ差し替えること」と「Q4.7 型の完全同定を 1 つ得ること」にあり、252 の内訳は別の法廷(gentle 塔)に持ち込むべきである。**

---

## 1. 記号・前提・引用と自前導出の分離

### 1.1 うちの窓(既在・再測定しない)

$$\mathbf N=\mathcal V(F_2)\times\langle c\rangle,\quad \mathbf N_0=\mathcal V(PB_3)=\mathcal V(F_2)\times\langle c^{7}\rangle,\quad N_{F_2}=\mathcal V(F_2)=\gamma_5(F_2)F_2^{\,7},$$
$$W=\mathcal V(K(0,5)),\quad P=F_2/N_{F_2}\ (\lvert P\rvert=7^8),\quad Q=K(0,5)/W\ (\lvert Q\rvert=7^{40}),\quad \lvert[P,P]\rvert=7^6=117{,}649 .$$

$\mathcal X_{\mathbf N}=\{m\bmod 7:2m+1\not\equiv0\}$($\lvert\mathcal X\rvert=6$)。本走宇宙 $=6\times117{,}649=705{,}894$。本走の答え = hexagon **294**・PENT_W **42**・hexagon-only **252**(BH-α-pent v1.1)。

$PB_3=F_2\times\langle c\rangle$、$F_2=\langle x_{12},x_{23}\rangle$、$c=x_{12}x_{13}x_{23}=x_{23}x_{12}x_{13}=(\sigma_1\sigma_2)^3$(A.5)。$x_{13}=x_{12}^{-1}cx_{23}^{-1}$。

### 1.2 引用する既在の結果(本ノートは再証明しない)

| 札 | 内容 | 出所 |
|---|---|---|
| **(2.20)** | pentagon: $\varphi_{234}(f)\varphi_{1,23,4}(f)\varphi_{123}(f)\,N=\varphi_{1,2,34}(f)\varphi_{12,3,4}(f)\,N$ in $PB_4/N$。**$f$ のみの条件($m$ 非依存)** | 2008 Def 2.6・p.13(頁画像照合済 = litgate_pentagon §6.1) |
| **(A.18)** | 余面 5 本の生成元値(§2.2 の表) | 2008 App A.4(頁画像照合済) |
| **(2.4)** | $N_{PB_3}=\bigcap_\varphi\varphi^{-1}(N)$(5 本の交わり) | 2008 p.9(画像照合済) |
| **Prop 3.9(A)** | $\forall N\in\mathrm{NFI}(PB_3)\ \exists K\in\mathrm{NFI}^{\rm isolated}_{PB_4}(B_4):K_{PB_3}\le N$ | 2008 p.33(txt L2563–2605 逐語確認) |
| **Cor 3.13** | $[(m,f)]$ genuine $\iff$ 全ての $K\le N$ に survive | 2008 p.38 |
| **Thm 3.8** | $\widehat{GT}\cong\varprojlim\mathrm{ML}$ | 2008 p.33 |
| **Q4.7** | 「$F_2/N_{F_2}$ 非 Abelian で genuine を全同定できる $N$ はあるか」(逐語 = txt L3578–3581) | 2008 §4 |
| **Prop 3.4** | $N\in\mathrm{NFI}_{PB_3}(B_3)$、$(m,f)\in\mathbb Z\times[F_2,F_2]$ ⟹ hexagon (3.3)(3.4) mod $N$ $\iff$ (3.10)$\wedge$(3.11) が **$N_{F_2}$ の中**で成立 | **2401 §3 p.11**(仲裁ノート §1 に逐語・頁画像照合済) |
| **CENT-FREE** | $f\in[PB_4,PB_4]$ で $PB_4$ 水準 pentagon $\iff$ $K(0,5)=PB_4/Z(PB_4)$ 水準 pentagon | 翻訳ノート §1.5 |
| **VERBAL-ISO** | $N_{F_2}$ 完全不変 ⟹ $N$ isolated | auto_settled_check §3.4(Sol F105-3.3 で paper theorem 受理) |
| **H8′** | $P$ が $p$ 群・$\bar f\in[P,P]$・$\gcd(2m+1,p)=1$ ⟹ SURJ 自動 | week3-狩場計画_v2 §2.1 |
| **BH-α-pent v1.1** | $\mathfrak G_{\rm ar}(\mathbf N)=\mathfrak G_{\rm pent}(\mathbf N)=H_W$、$\lvert H_W\rvert=42$ | 裁定 586・F110-1.2(framework/measurement-relative) |

### 1.3 本ノートが自前で導く命題(9 本)

補題 **B4-FORGET** / 補題 **B4-IND** / ★定理 **B4-VAC** / ★定理 **B4-CANON** / 補題 **B4-MONO** / 定理 **B4-DIR** / 補題 **B4-KAPPA** / ★系 **B4-42** / ★命題 **BIT-252**。

---

## 2. 委嘱① — 窓の持ち上げ

### 2.1 Prop 3.9 の構成の逐語(txt L2571–2605)

> $\psi:PB_3\to S_n$、$\ker\psi=N$ とする。$\tilde\psi(x_{12}):=\psi(x_{12})$, $\tilde\psi(x_{23}):=\psi(x_{23})$, $\tilde\psi(x_{13}):=\psi(x_{13})$, $\tilde\psi(x_{14})=\tilde\psi(x_{24})=\tilde\psi(x_{34}):=\mathrm{id}$ は準同型 $PB_4\to S_n$ を定め、$\varphi_{123}^{-1}(\ker\tilde\psi)=N$。ゆえに (3.11) の 5 本の交わりは $\le N$。**$\tilde{N}$ を「$PB_4$ の指数 $\lvert PB_4:\ker\tilde\psi\rvert$ の正規部分群すべての交わり」とすると $\tilde N$ は特性部分群ゆえ $\tilde N\in\mathrm{NFI}_{PB_4}(B_4)$**。Cor 3.5 で isolated な $K\le\tilde N$ を取れば $K_{PB_3}\le N$。∎

★ 読みの要点 3 つ:
1. **$\ker\tilde\psi$ 自身は $B_4$ で正規とは限らない**(下記 §2.3 で反例的に確認できる)。だから Dolgushev は「指数 $d$ の正規部分群**全体**の交わり」という**特性化**を挟む。
2. その特性部分群 $\tilde N$ は**計算対象ではない**。$d=\lvert PB_4:\ker\tilde\psi\rvert=\lvert P\rvert=7^8$ のとき、$PB_4$ の指数 $7^8$ の正規部分群は膨大にあり、その全交わりの指数は天文学的。**Prop 3.9 は存在(cofinality)の定理であって、レシピではない。**
3. さらに Cor 3.5 で isolated 化する段でもう一段細かくなる。

### 2.2 補題 **B4-FORGET**($\tilde\psi$ の正体 = 4 本目の紐を忘れる射)

> ### 補題 B4-FORGET
> $p_4:PB_4\to PB_3$ を「第 4 の紐を忘れる」写像($x_{i4}\mapsto1$、$x_{ij}\mapsto x_{ij}$($j\le3$))とすると、Prop 3.9 の $\tilde\psi$ は
> $$\boxed{\ \tilde\psi=\psi\circ p_4\ }$$
> である。とくに $\tilde\psi$ の well-definedness は (A.3) の場合分けを引かずに従う($p_4$ は Fadell–Neuwirth 分裂 $PB_4\cong F_3\rtimes PB_3$ の射影)。
> **証明.** 生成元上で両辺が一致する($x_{12},x_{23},x_{13}$ は保存・$x_{14},x_{24},x_{34}\mapsto1$)。$p_4$ は $PB_n\to PB_{n-1}$ の標準射影で準同型。∎

★ 帰結: $\ker\tilde\psi=p_4^{-1}(N)$、$\lvert PB_4:\ker\tilde\psi\rvert=\lvert PB_3:N\rvert=\lvert P\rvert$。また $\sigma_3$ 共役は $x_{13}$ を $x_{14}$ 型へ移すので $\ker\tilde\psi\not\trianglelefteq B_4$(§2.1 の読み 1)。**$B_4$-核**は
$$\tilde{\mathbf N}_{\rm core}:=\mathrm{core}_{B_4}(\ker\tilde\psi)=\bigcap_{i=1}^{4}p_i^{-1}(N)\qquad(p_i=\text{第 }i\text{ の紐を忘れる射})$$
であり($B_4/PB_4=S_4$ の $S_4/S_3$ 4 剰余類・$N\trianglelefteq B_3$ ゆえ捻れは吸収される)、$PB_4/\tilde{\mathbf N}_{\rm core}\hookrightarrow P^4$。⟹ **座標ごとに $P$ の中で計算できる**(指数は $\le7^{32}$ だが列挙は不要)。

### 2.3 補題 **B4-IND**(下位誘導 (2.4) の値 = $\mathbf N_0$)

$\psi:PB_3\to P$($x_{12}\mapsto x,\ x_{23}\mapsto y,\ x_{13}\mapsto x^{-1}y^{-1},\ c\mapsto1$)を取る(核 $=\mathbf N$)。

> ### 補題 B4-IND
> $$\boxed{\ (\ker\tilde\psi)_{PB_3}=(\tilde{\mathbf N}_{\rm core})_{PB_3}=\mathcal V(F_2)\times\langle c^{7}\rangle=\mathbf N_0\ }$$
> **証明.** $(2.4)$ より $(\ker\tilde\psi)_{PB_3}=\bigcap_{\varphi}\ker(\psi p_4\varphi)$、$(\tilde{\mathbf N}_{\rm core})_{PB_3}=\bigcap_{i,\varphi}\ker(\psi p_i\varphi)$(20 本)。**付録 A.1 の機械生成表**より、20 本のうち **8 本は $\psi$ そのもの**(核 $=\mathbf N$)、残り 12 本は像が $P$ の**位数 7 の巡回部分群**に入る「退化写像」である。退化写像 $\lambda$ について $w=f\,c^k$($f\in F_2$)の像は $g^{\varepsilon(f)+k}$ 型($g\in\{x^{\pm},y^{\pm}\}$、$\varepsilon$ は $x_{12}$ か $x_{23}$ の指数和)または $g^{k}$ 型。$f\in\mathcal V(F_2)$ では $\varepsilon(f)\equiv0\ (7)$ ゆえ、12 本の条件は総合して $k\equiv0\ (\mathrm{mod}\ 7)$ に帰着する。逆に $\mathcal V(F_2)\times\langle c^7\rangle$ は 20 本すべての核に入る($\mathcal V(F_2)$ は指数 7 の巡回群で死に、$c^{7}$ も死ぬ)。∎

★ **整合の所見**: 誘導される $B_3$ 窓は、うちの **control 窓 $\mathbf N_0$ そのもの**である。$\mathbf N_0$ は既に定義 NW($p$)で事前登録されており(翻訳ノート §5)、$\mathbf N/\mathbf N_0\cong C_7$(指数 7・$c$ 方向のみ)。**「B₄ へ持ち上げると $c$ が 1 段だけ生き返る」**が (2.4) の意味の全部である。

### 2.4 ★ 定理 **B4-VAC**(Prop 3.9 窓は pentagon の検出力ゼロ)

> ### 定理 B4-VAC
> $\tilde{\mathbf N}\in\{\ker\tilde\psi,\ \tilde{\mathbf N}_{\rm core}\}$ とする。**すべての charming $f$(すなわち $f\in[F_2,F_2]\,\mathcal V(F_2)$)に対し、pentagon (2.20) は $PB_4/\tilde{\mathbf N}$ の中で恒真**である。
> **証明.** $\tilde{\mathbf N}_{\rm core}=\bigcap_ip_i^{-1}(N)$ ゆえ、(2.20) mod $\tilde{\mathbf N}_{\rm core}$ は 4 座標の連立に同値で、第 $i$ 座標は 5 本の合成 $\psi p_i\varphi_\bullet$ による代入である。付録 A.1 の表より、各 $i$ について 5 本のうちちょうど 2 本が $\psi$、3 本が退化写像である。退化写像の像は可換ゆえ $f\in[F_2,F_2]$ は $1$ に写る。よって第 $i$ 座標の等式は(付録 A.2 の機械生成出力)
> $$i=4:\ 1\cdot1\cdot f(x,y)=f(x,y)\cdot1,\quad i=3:\ 1\cdot f(x,y)\cdot1=f(x,y)\cdot1,$$
> $$i=2:\ 1\cdot f(x,y)\cdot1=1\cdot f(x,y),\quad i=1:\ f(x,y)\cdot1\cdot1=1\cdot f(x,y)$$
> となり、**4 座標すべてが恒等式**。$\ker\tilde\psi$ は $i=4$ 座標のみなので同じ。∎

> ### ★ 委嘱②への直接回答(その 1)
> $$\boxed{\ \textbf{「PENT}_W\textbf{-FAIL}\Rightarrow(2.20)\textbf{-FAIL」は Prop 3.9 窓では}\textbf{偽}\textbf{であり、252 の}\textbf{全件}\textbf{が反例である。}\ }$$
> 理由は構造的である: $\tilde\psi=\psi\circ p_4$ は **$B_3$ のデータしか持たない**。4 本目の紐を忘れる射で作った窓は、4 本目の紐を本当に要する関係式(= pentagon)を**課せない**。Prop 3.9 は「$K_{PB_3}\le N$」という**下位互換性**だけを保証しており、pentagon の情報量については何も言っていない。

⟹ **実装上の副産物**: この事実は**無料のバグ検出器**である(§8 の B4-EXQ-6)。

### 2.5 ★ 定理 **B4-CANON**(使うべき窓 = verbal lift $\mathcal V(PB_4)$)

> ### 定理 B4-CANON
> $$\tilde{\mathbf N}^*:=\mathcal V(PB_4)=\gamma_5(PB_4)\,PB_4^{\,7}$$
> とおく。このとき
> **(1)** $\tilde{\mathbf N}^*$ は $PB_4$ で完全不変 ⟹ 特性部分群 ⟹ $PB_4\trianglelefteq B_4$ より **$\tilde{\mathbf N}^*\trianglelefteq B_4$**。有限指数(下記 (4))ゆえ $\tilde{\mathbf N}^*\in\mathrm{NFI}_{PB_4}(B_4)$。
> **(2)** $\boxed{\tilde{\mathbf N}^*_{PB_3}=\mathcal V(PB_3)=\mathbf N_0}$(**厳密等号**)。とくに $\tilde{\mathbf N}^*_{F_2}=\mathcal V(F_2)=N_{F_2}$、$\tilde N^*_{\rm ord}=7$、$\mathcal X_{\tilde{\mathbf N}^*}=\mathcal X_{\mathbf N}$(6 層)。
> **(3)** $PB_4\cong\mathbb Z\times K(0,5)$($\mathbb Z=Z(PB_4)=\langle\Delta^2\rangle$)ゆえ $\boxed{PB_4/\tilde{\mathbf N}^*\cong C_7\times Q}$。
> **(4)** $PB_4$ の LCS 階数は $(6,4,10,21)$ ⟹ $\boxed{\lvert PB_4:\tilde{\mathbf N}^*\rvert=7^{41}}$(付録 A.3 の機械検算)。同じ計算が $K(0,5)$ の階数 $(5,4,10,21)$ ⟹ $\lvert Q\rvert=7^{40}$ を再現する(**NW-P4 の紙側独立確認**)。
>
> **証明.**
> **(1)** verbal ⟹ 完全不変 ⟹ 特性。有限生成冪零・類 $\le4$・指数 $7$ ゆえ有限指数。
> **(2)** ($\supseteq$)各余面 $\varphi$ は準同型ゆえ $\varphi(\mathcal V(PB_3))\subseteq\mathcal V(PB_4)$。($\subseteq$)**$p_4\circ\varphi_{123}=\mathrm{id}_{PB_3}$**(付録 A.1 の表 1 行目)ゆえ $\varphi_{123}$ は分裂単射。$\varphi_{123}(w)\in\mathcal V(PB_4)$ なら $w=p_4\varphi_{123}(w)\in p_4(\mathcal V(PB_4))\subseteq\mathcal V(PB_3)$。$\mathcal V(PB_3)=\mathcal V(F_2)\times\langle c^7\rangle$ は箱型計算(補題 NW-1a)。$\tilde N^*_{\rm ord}=\mathrm{lcm}(7,7,7)=7$(Prop 2.3)。
> **(3)** $PB_4^{\rm ab}=\mathbb Z^6$ で $\Delta^2=\prod_{i<j}x_{ij}\mapsto(1,\dots,1)$、座標射影で $\Delta^2\mapsto1$ なる準同型が取れる ⟹ 中心が直因子として分裂。verbal 部分群は直積を尊重する。
> **(4)** 純組紐群の LCS 公式 $\prod_k(1-t^k)^{\phi_k}=\prod_{i=1}^{n-1}(1-it)$。類 $4<p=7$ ゆえ Lazard(正則 $p$ 群)で $\lvert G/\gamma_5G\,G^7\rvert=7^{\sum_{k\le4}\phi_k}$。∎

> ### ★ なぜこの窓なのか(設計の一行)
> **$\mathbf N$ が「$F_2$ の verbal 窓 + $c$」、$W$ が「$K(0,5)$ の同じ verbal 窓」であるのと**同じ法則**を $PB_4$ に適用しただけ**である。marking の自由度がゼロ(翻訳ノート §5 の設計利点 (iii) がそのまま効く)で、罠 #3/#12 と CV-9 規約事故の温床を構造的に消す。

### 2.6 3 つの窓の比較(委嘱①のまとめ)

| 窓 | 定義 | $\tilde{\mathbf N}_{PB_3}$ | $B_4$ 正規 | 計算可能性 | pentagon 検出力 |
|---|---|---|---|---|---|
| $\ker\tilde\psi$ | $p_4^{-1}(\mathbf N)$ | $\mathbf N_0$ | ✗ | ◎($P$ の中) | **ゼロ**(定理 B4-VAC) |
| $\tilde{\mathbf N}_{\rm core}$ | $\bigcap_ip_i^{-1}(\mathbf N)$ | $\mathbf N_0$ | ✓ | ◎($P^4$ の中) | **ゼロ**(同) |
| Prop 3.9 の $\tilde N$ | 指数 $7^8$ の正規部分群 全交わり | $\le\mathbf N_0$ | ✓ | ✗(天文学的) | 未知(構成不能) |
| ★ $\tilde{\mathbf N}^*=\mathcal V(PB_4)$ | $\gamma_5PB_4^{\,7}$ | $\mathbf N_0$(**等号**) | ✓ | ◎(pc 群 $7^{41}$) | ★ **$W$ 水準**(§3.3) |

---

## 3. 委嘱② — 判定の形と PENT_W との論理関係

### 3.1 補題 **B4-MONO**(窓単調性)

> $\tilde{\mathbf N}'\le\tilde{\mathbf N}$ なら「(2.20) mod $\tilde{\mathbf N}'$」⟹「(2.20) mod $\tilde{\mathbf N}$」。すなわち **FAIL は細かい窓へ伝播し、PASS は粗い窓へ伝播する**。(自明: 商の射影。)

### 3.2 定理 **B4-DIR**(委嘱②「向き」への回答)

$L:=$ $PB_4\twoheadrightarrow K(0,5)$ による $W$ の逆像。$W$ は verbal ゆえ $L$ は $PB_4$ で特性、$\lvert PB_4:L\rvert=\lvert Q\rvert=7^{40}$、$L\in\mathrm{NFI}_{PB_4}(B_4)$。

> ### 定理 B4-DIR
> **(a)** $\tilde{\mathbf N}\le L$ なる任意の $B_4$ 窓について、$\;\mathrm{PENT}_W\text{-FAIL}\Longrightarrow(2.20)\bmod\tilde{\mathbf N}\ \text{FAIL}$。
> **(b)** $\tilde{\mathbf N}\not\le L$ では一般に偽。**明示反例**: $\tilde{\mathbf N}\in\{\ker\tilde\psi,\tilde{\mathbf N}_{\rm core}\}$ では 252 の全件が (2.20)-PASS(定理 B4-VAC)。
> **(c)** $\tilde{\mathbf N}^*\le L$ である($\tilde{\mathbf N}^*=7\mathbb Z\times W$、$L=\mathbb Z\times W$、指数 7)。さらに charming $f$ に対しては **CENT-FREE** により逆も成り立ち、$$(2.20)\bmod\tilde{\mathbf N}^*\iff(2.20)\bmod L .$$
> **証明.** (a) は B4-MONO と「(2.20) mod $L$ = $K(0,5)/W$ 水準の pentagon」から。(c) の前半は定理 B4-CANON (3) と $\mathcal V(\mathbb Z\times K)=7\mathbb Z\times\mathcal V(K)$。後半は CENT-FREE(pentagon の defect は 5 本の準同型像の積ゆえ $[PB_4,PB_4]$ に入り、$Z(PB_4)\cap[PB_4,PB_4]=1$)。∎

> ### ⚠ 【GAP-B4-1】(**本ノート最大の未閉点**)
> 「$K(0,5)/W$ 水準の pentagon」= **$\mathrm{PENT}_W$($\rho$-ノルム形 $\bar\rho^4(\bar f)\cdots\bar\rho(\bar f)\bar f=1$)」**という同一視は、**余面 5 本 $\varphi_\bullet$ の像が $\rho$ の 5 回転 $\rho^i\circ j$ に一致すること**を要する。これは古典的だが、**本ノートは項ごとの対応を確かめていない**。実際、$K(0,5)$ の球面関係式 $x_{45}=(x_{14}x_{24}x_{34})^{-1}$, $x_{51}=(x_{12}x_{13}x_{14})^{-1}$ を代入しても、$\varphi_{12,3,4}$ の引数 $(x_{13}x_{23},x_{34})$ と $\rho^4$ の引数 $(x_{34},x_{45})$ は**素朴には一致しない**(共役・並べ替えを要する)。CENT-FREE の証明が扱ったのは $Z(PB_4)$ のずれだけで、**この項対応は仮定されている**。
> ⟹ **本ノートは (2.20) と $\mathrm{PENT}_W$ の同値を主張しない。** §8 の工程 2/3 は、この同値を**紙で仮定せず機械で試験する**設計にしてある(§3.3)。

### 3.3 ★ 判定機の形(委嘱②「判定の手順」)

$f\in[F_2,F_2]$ の類 $\bar f\in[P,P]$ に対し、$\tilde{\mathbf N}^*$ 水準の pentagon 判定は **5 本の準同型の像の積 1 本**である。$R:=PB_4/\tilde{\mathbf N}^*$($\lvert R\rvert=7^{41}$・pc 群)とおくと、各余面は $\bar\varphi_\bullet:P\to R$ に降りる($\varphi_\bullet(N_{F_2})\subseteq\mathcal V(PB_4)$・verbal)。生成元上の値は (A.18) そのもの:

| $\bar\varphi$ | $x\ (=x_{12}P)\mapsto$ | $y\ (=x_{23}P)\mapsto$ |
|---|---|---|
| $\bar\varphi_{123}$ | $x_{12}$ | $x_{23}$ |
| $\bar\varphi_{234}$ | $x_{23}$ | $x_{34}$ |
| $\bar\varphi_{12,3,4}$ | $x_{13}x_{23}$ | $x_{34}$ |
| $\bar\varphi_{1,23,4}$ | $x_{12}x_{13}$ | $x_{24}x_{34}$ |
| $\bar\varphi_{1,2,34}$ | $x_{12}$ | $x_{23}x_{24}$ |

(右辺は $R$ の元。)判定式:
$$D_{B_4}(\bar f):=\bigl(\bar\varphi_{1,2,34}(\bar f)\,\bar\varphi_{12,3,4}(\bar f)\bigr)^{-1}\cdot\bar\varphi_{234}(\bar f)\,\bar\varphi_{1,23,4}(\bar f)\,\bar\varphi_{123}(\bar f)\ \in R,\qquad \text{(2.20)}\iff D_{B_4}(\bar f)=1 .$$

★ **$m$ 非依存**(抽出の所見どおり)⟹ 評価は **117,649 件**であって 705,894 件ではない(lane P と同じ節約)。

> ### ★ 委嘱②への直接回答(その 2 — 論理関係の最終形)
> | 主張 | 状態 |
> |---|---|
> | genuine ⟹ (2.20) mod $\tilde{\mathbf N}$(任意の窓) | **定理**(2008 の公理・Cor 2.13 経由)。**HS Prop 7 の翻訳を一切要しない** |
> | genuine ⟹ $\mathrm{PENT}_W$ | 既在(HSP-SOUND・HS 経由) |
> | $\mathrm{PENT}_W$-FAIL ⟹ (2.20) mod $\tilde{\mathbf N}^*$ FAIL | **【GAP-B4-1】相対で真**(定理 B4-DIR (a)(c)) |
> | $\mathrm{PENT}_W$-FAIL ⟹ (2.20) mod (Prop 3.9 窓) FAIL | ★ **偽**(反例 = 252 全件) |
> | (2.20) mod $\tilde{\mathbf N}^*$ $\iff$ $\mathrm{PENT}_W$ | ★ **UNKNOWN**(【GAP-B4-1】)⟹ **機械同値試験で決める**(§8 工程 3) |

### 3.4 hexagon 側は新情報ゼロ(定理として)

2008 の GT-pair は hexagon (2.18)(2.19) を **$B_3/\tilde{\mathbf N}_{PB_3}$ の中で**課す。$\tilde{\mathbf N}^*_{PB_3}=\mathbf N_0$ であり、**2401 Prop 3.4** は $(m,f)\in\mathbb Z\times[F_2,F_2]$ について hexagon 判定が $N_{F_2}$ **のみ**に依存すると言う。$\mathbf N_0\cap F_2=\mathbf N\cap F_2=\mathcal V(F_2)$ ゆえ:

$$\boxed{\ \textbf{hexagon mod }\tilde{\mathbf N}^*_{PB_3}\ \Longleftrightarrow\ \textbf{hexagon mod }\mathbf N\quad(\text{全 }m,\ \text{全 charming }f).\ }$$

これは工房の仲裁ノート(裁定 474 系・NW-P8 の versioned 撤回、S-8′「不一致 1 件でも実装バグ」)と**同じ結論**である。本ノートは独立に次を得た:

> ### 補題 B4-KAPPA($c$-指数は恒等的に消える — 独立確認)
> $\kappa:PB_3=F_2\times\langle c\rangle\to\mathbb Z$ を $\kappa(fc^k)=k$ とする。任意の $m\in\mathbb Z$, $f\in F_2$ に対し、hexagon (2.18)(2.19) の defect $d_1,d_2\in PB_3$ は $\kappa(d_1)=\kappa(d_2)=0$。
> **証明.** ($f=1$) (A.5) の $x_{13}x_{23}=x_{12}^{-1}c$, $x_{12}x_{13}=x_{23}^{-1}c$ と (A.6) $\sigma_2^{-1}x_{12}\sigma_2=x_{23}^{-1}x_{12}^{-1}c$ を使って直接計算すると
> $$d_1=x_{23}^{-m}(x_{12}x_{23})^mx_{12}^{-m}\in F_2,\qquad d_2=x_{12}^{-m}x_{13}^{-m}x_{23}^{-m}c^{m}$$
> で $\kappa(d_1)=0$、$\kappa(d_2)=-m+m=0$。($f$ 依存性)$f\to fg$($g\in F_2$)と替えると $d_1(fg)=g^{-1}\,W^{U^{-1}}\,d_1(f)$($W=g\cdot(g^{-1})^{\sigma_1^{2m+1}}$、$U$ の $S_3$ 像は $(23)$)と書ける。$PB_3^{\rm ab}=\mathbb Z^3$(基底 $x_{12},x_{23},x_{13}$、$\kappa=$ 第 3 座標)の上で $\sigma_1$-共役は第 2・第 3 座標の互換、$\sigma_2$-共役は第 1・第 3 座標の互換(A.6 から直接)。$g=(a,b,0)$ とすると $W=(0,b,-b)$、$W^{U^{-1}}=(-b,b,0)$ ⟹ $\kappa=0$。$d_2$ も同型の計算で $\kappa(d_2(fg))=\kappa(d_2(f))$。∎

⟹ **B₄ 裁定の実体は pentagon 1 本に完全に縮約される。** これは委嘱の「判定の形」への構造的回答である。

### 3.5 ★ 系 **B4-42**(条件つき・Q4.7 型の完全同定)

> ### 系 B4-42
> 次の 5 条件の下で:
> **(H1)** 【GAP-B4-1】が閉じる(= (2.20) mod $\tilde{\mathbf N}^*$ $\iff$ $\mathrm{PENT}_W$、機械同値試験で可)、
> **(H2)** 本走の測定値(hexagon 294・PENT_W 42)、
> **(H3)** BH-α-pent v1.1($\mathfrak G_{\rm ar}(\mathbf N)=42$)、
> **(H4)** practical 制限(§9.2【GAP-B4-2】)、
> **(H5)** SURJ 自動($\tilde{\mathbf N}^*$ でも成立 — 下記注)、
> $$\boxed{\ \mathrm{GT}^\heartsuit_{2008}(\tilde{\mathbf N}^*)\big\vert_{\rm practical}\ \textbf{はちょうど 42 元からなり、その全元が genuine である。}\ }$$
> **証明.** 2008 Def 2.9 + Prop 2.10 より GT-shadow $=$ GT-pair $\wedge$ ($T^{PB_3},T^{PB_2}$ 全射)。$\tilde N^*_{\rm ord}=7$ ゆえ $T^{PB_2}$ 全射 $\iff m\in\mathcal X$。$T^{PB_3}$ 全射: $PB_3/\mathbf N_0\cong P\times C_7$ は 7 群、$\Phi(P\times C_7)=[P,P]$、像は $x^{u},\,{}^{f}\!y^{u},\,c^{u}$($\gcd(u,7)=1$)を含むので Frattini 論法(H8′ の直接拡張)で全射 ⟹ **(H5)**。hexagon は §3.4 で $\mathbf N$ のそれと同一、pentagon は (H1) で $\mathrm{PENT}_W$ と同一。ゆえに集合として $\{$hexagon$\}\cap\{\mathrm{PENT}_W\}=\mathfrak G_{\rm pent}$、(H2)(H3) より $\lvert\cdot\rvert=42$ かつ $=\mathfrak G_{\rm ar}$。arithmetic ⟹ genuine ゆえ全元 genuine。∎

> ### ★ この系の意味(3 点)
> 1. **Question 4.7 が求める型の実例**である: $F_2/\tilde{\mathbf N}^*_{F_2}=P$ は非 Abelian(類 4)で、$\mathrm{GT}^\heartsuit$ の genuine 元を**全同定**している。⟹ **司房への申し送り**: 本件を主張するなら novelty 検査(repo/台帳 grep + 文献)を司令塔が先に通すこと(§9.4)。
> 2. **Question 4.6 への陰性データ**でもある: $\mathrm{GT}^\heartsuit(\tilde{\mathbf N}^*)$ が全 genuine ⟹ 任意の $K\le\tilde{\mathbf N}^*$ について $\mathrm{GT}^\heartsuit(K)\to\mathrm{GT}^\heartsuit(\tilde{\mathbf N}^*)$ は全射 ⟹ **この窓は charming∧fake の例を与えない**。
> 3. **窓の大きさ**: $\lvert PB_4:\tilde{\mathbf N}^*\rvert=7^{41}\approx4.5\times10^{34}$。Table 1 の最大は $762{,}048$、Leila 部分群でも $2.85\times10^{14}$。**この差は「窓の商を置換群でなく pc 群で持つ」ことから来る**(Dolgushev の実装は $S_d$ ベースなので $\lvert PB_4:N\rvert$ が律速する)。一方**実際の律速量 $\lvert F_2:N_{F_2}\rvert=7^8=5{,}764{,}801$ は Table 1 の $N^{(31)}$($8.9\times10^6$)と同程度**であり、桁の差は表現の差であって計算量の差ではない。**この対比を「大きい窓を征服した」と読ませないこと**(§7 の防壁 R6)。

---

## 4. 委嘱③ — genuine の正式判定(Cor 3.13 の有限化)

### 4.1 Cor 3.13 の構造と、有限化が難しい正確な理由

Cor 3.13: $[(m,f)]$ genuine $\iff$ $\forall K\le N$($K\in\mathrm{NFI}_{PB_4}(B_4)$)に survive。survival の像 $\mathrm{im}(\mathrm{GT}^\heartsuit(K)\to\mathrm{GT}^\heartsuit(N))$ は $K$ について**減少**し、$\mathrm{GT}^\heartsuit(N)$ は有限。ゆえに:

> ### 補題(停止するが停止点が読めない)
> 減少族は有限集合の中で**必ず停止**し、Mittag-Leffler(有限集合の逆極限)より $$\mathfrak G_{\rm genuine}(N)=\bigcap_{K\le N}\mathrm{im}\bigl(\mathrm{GT}^\heartsuit(K)\to\mathrm{GT}^\heartsuit(N)\bigr)=\text{(停止値)} .$$
> ⟹ **障害は「無限個の窓」ではなく「停止点の有効上界がない」ことである。**【GAP-B4-3】

⟹ **陰性証明書は有限**(1 窓で足りる)。**陽性証明は、survival の切り詰めからは原理的に出ない。**

### 4.2 ★ 有限化の正しい形 = **サンドイッチ**

$$\mathfrak G_{\rm ar}(N)\ \subseteq\ \mathfrak G_{\rm genuine}(N)\ \subseteq\ \mathrm{GT}^\heartsuit(N)$$
(左 = $G_{\mathbb Q}\subseteq\widehat{GT}$、右 = genuine は shadow)。**両端の濃度が一致すれば、Cor 3.13 は切り詰め誤差ゼロで 1 窓で閉じる。**

> $$\boxed{\ \lvert\mathfrak G_{\rm ar}(N)\rvert=\lvert\mathrm{GT}^\heartsuit(N)\rvert\ \Longrightarrow\ \textbf{Cor 3.13 は当該窓で完全に有限化される}\ }$$

NW(7)+$\tilde{\mathbf N}^*$ はまさにこの形である(系 B4-42)。**これが委嘱③「どの下位窓集合で打ち切れるか・打ち切りの正当化」への回答である: 打ち切るのではなく、下から挟むのが正しい**。下界を作る道具は算術実現(円分指標・複素共役・Belyi)であって、窓の列挙ではない。

### 4.3 ★★ 委嘱の問い(β)は B₄ の管轄外である

252 の**内訳**が問うているのは、地図第 4 版の言葉で「**gentle 系と B₄ 本来系の差の定量**」である。ところが:

| 理論 | 極限 | 有限窓の圏 | genuine の意味 |
|---|---|---|---|
| B₄ 本来系(2008) | $\widehat{GT}$ | $\mathrm{NFI}_{PB_4}(B_4)$ | $\widehat{GT}$ 由来(Cor 3.13) |
| B₃-gentle(2401) | $\widehat{GT}_{gen}$ | $\mathrm{NFI}_{PB_3}(B_3)$ | $\widehat{GT}_{gen}$ 由来(2401 Def 4.2・Thm 5.2) |

252 は **$\widehat{GT}$ 由来でないことが既に確定**している(pentagon FAIL)。残る問いは「**$\widehat{GT}_{gen}$ 由来か**」であり、これを裁く塔は **gentle 塔**($\mathrm{NFI}_{PB_3}(B_3)$ の下降列)である。**B₄ の窓をいくら細かくしても $\widehat{GT}_{gen}$ の像は見えない。**

$$\boxed{\ \textbf{B}_4\ \textbf{は }252\textbf{ の「死因」を厳密化する法廷であって、「内訳」を裁く法廷ではない。}\ }$$

### 4.4 ★ 命題 **BIT-252**(内訳は 1 ビット)

> ### 命題 BIT-252
> 前件: (i) $\mathbf N$ と下位窓 $K$ がともに isolated(VERBAL-ISO)、(ii) $\mathrm{GT}(\mathbf N)$ は位数 **294** の群(GRP + 本走)、(iii) $\mathfrak G_{\rm ar}(\mathbf N)$ は位数 **42** の部分群(BH-α-pent)。このとき
> $$\boxed{\ \mathfrak G^{\rm gentle}_{\rm genuine}(\mathbf N)\ \in\ \bigl\{\,\mathfrak G_{\rm ar}\ (42\ \text{元}),\ \ \mathrm{GT}(\mathbf N)\ (294\ \text{元})\,\bigr\}\quad\textbf{— 中間はない}. }$$
> すなわち **252 は「全員が gentle-genuine」か「全員が gentle-fake」かのどちらかで、混在はあり得ない**。
> **証明.** $\mathfrak G^{\rm gentle}_{\rm genuine}=\bigcap_K\mathrm{im}(\mathrm{GT}(K)\to\mathrm{GT}(\mathbf N))$ は部分群の交わりゆえ部分群。算術元は全窓に survive するので $\supseteq\mathfrak G_{\rm ar}$。$[\mathrm{GT}(\mathbf N):\mathfrak G_{\rm ar}]=294/42=7$ は**素数**ゆえ、$\mathfrak G_{\rm ar}\le H\le\mathrm{GT}(\mathbf N)$ なる部分群は両端のみ。∎
>
> ### ★ 系(理論分離の払い戻し)
> $\mathfrak G_{\rm ar}\subseteq\mathrm{im}(\widehat{GT}\to\mathrm{GT}(\mathbf N))\subseteq\mathfrak G_{\rm pent}=42$(HSP-SOUND)ゆえ **$\mathrm{im}(\widehat{GT})=42$**。よって
> - **ビット $=294$** なら $\widehat{GT}_{gen}$ の像 $(294)\ \supsetneq\ \widehat{GT}$ の像 $(42)$ ⟹ **$\widehat{GT}_{gen}\supsetneq\widehat{GT}$ が有限窓で証人つきになる**。
> - **ビット $=42$** なら、この窓で両理論の像は一致し、252 は理論分離の情報をもたない。

### 4.5 ★ 決定実験(1 元 × 1 窓 × 117,649 件)— **B₃ 側**

ビットの **42 側だけは 1 窓で決着する**(294 側は無限深度か構造定理を要する)。**2401 Prop 3.4 により gentle 塔の識別力は $K_{F_2}$ にしかない**ので、下降は $N_{F_2}$ を細かくする方向に限る。

> **設計**: $K:=\mathcal V_5(F_2)\times\langle c\rangle$、$\mathcal V_5(F_2):=\gamma_6(F_2)F_2^{\,7}$(類 5 へ 1 段)。$P':=F_2/\mathcal V_5(F_2)$、$\lvert P'\rvert=7^{2+1+2+3+6}=7^{14}$、$\lvert[P',P']\rvert=7^{12}$。$[P',P']\to[P,P]$ の fiber は **$7^6=117{,}649$ 元**。
> **手順**: 252 から**任意に 1 元** $g=(m,\bar f)$ を取る。$\bar f$ の 117,649 個の持ち上げ $\bar f'$ 各々について $(m,\bar f')$ が (3.10)(3.11) を $\mathcal V_5(F_2)$ の中で満たすかを検査。
> - **1 件も通らない** ⟹ $g$ は $K$ に survive しない ⟹ BIT-252 より **252 全件が gentle-fake**。**内訳 CLOSED**。
> - **通るものがある** ⟹ 不決(より深い窓へ)。
> **コスト**: $7^{14}$ の pc 群での語評価 $\times\,2\times117{,}649$ ⟹ **数分**。$m$ は固定(1 層のみ)。

> ⚠ **本ノートはこの実験を実行しない**(紙のみ)。実施は司令塔の裁定 + prereg(IF-FIRST)を経ること。**BIT-252 が事前に登録されていることが肝**である(結果が 42 側でも 294 側でも事後緩和にならない)。

### 4.6 B₄ 塔は $\tilde{\mathbf N}^*$ で閉じる

系 B4-42 の下では $\mathrm{GT}^\heartsuit(\tilde{\mathbf N}^*)=\mathfrak G_{\rm ar}$ なので、**$\tilde{\mathbf N}^*$ より深い B₄ 窓に降りても 1 元も減らない**(サンドイッチの両端が既に一致)。⟹ **B₄ 側の下降は打ち切ってよい**。委嘱③の「どの下位窓集合で打ち切れるか」への回答は: **$\{\tilde{\mathbf N}^*\}$ の 1 個で足りる。ただしそれは survival の切り詰めが正当化されるからではなく、下界が上界に届いているからである。**

---

## 5. 委嘱④ — 計算量

### 5.1 位数見積り

| 対象 | 位数 | 表現 | 備考 |
|---|---|---|---|
| $P=F_2/\mathcal V(F_2)$ | $7^8=5{,}764{,}801$ | pc 群(既在) | 候補の住所 |
| $[P,P]$ | $7^6=117{,}649$ | — | **pentagon 判定の宇宙**($m$ 非依存) |
| $R=PB_4/\mathcal V(PB_4)$ | $7^{41}\approx4.5\times10^{34}$ | **pc 群(41 生成)** | ANUPQ `Pq`(p=7, class 4)で構築 |
| $Q=K(0,5)/W$ | $7^{40}$ | pc 群(既在) | $R\cong C_7\times Q$ |
| $PB_4/\tilde{\mathbf N}_{\rm core}$ | $\le7^{32}$ | $P^4$ の部分群 | 参考(検出力ゼロ) |
| $PB_3/\mathbf N_0$ | $7^9$ | $P\times C_7$ | hexagon 側(§3.4 で不要と判明) |

### 5.2 1 元あたりのコストと総コスト

$D_{B_4}(\bar f)$ の評価 = **pc 群 $R$ における準同型像 5 回 + 積 4 回 + 比較 1 回**。pc 準同型の像は指数ベクトルの collection で、41 生成・類 4 の群なら 1 回あたり $10^{-4}$ 秒級。

$$\textbf{総コスト}=117{,}649\times(5\ \text{像}+4\ \text{積})\ \approx\ 10^6\ \text{回の collection}\ \approx\ \textbf{数分}.$$

- **メモリ**: 41 生成の pc collector table は $O(41^2)$ 語 ⟹ **8GB 制約に無関係**。
- **GHA 可否**: **可**(単一 job・shard 分割すら不要)。lane P(既走)と同じ規模。
- **$R$ の構築**: $PB_4$ の表示 (A.3)(6 生成・15 関係)に $p$-quotient(p=7, class 4)。予言 $\lvert R\rvert=7^{41}$。**数秒〜数分**。
- **252 全件**: pentagon は $m$ 非依存ゆえ、252 は 117,649 件の評価に**含まれている**(別コストなし)。

### 5.3 ★ 費用対効果の正直な会計

| 作業 | コスト | 得られる新情報 |
|---|---|---|
| $\tilde{\mathbf N}^*$ での (2.20) 評価 | 数分 | **【GAP-B4-1】の決着**(2 系統一致 or 不一致)。252 の身分は**変わらない** |
| N⁽¹⁹⁾ 較正 | 秒 | 判定機の正当性(必須先行) |
| N⁽³⁴⁾ 較正 | 分〜時間 | 同上(第 2 フィクスチャ) |
| BIT-252 決定実験(B₃ 側) | 数分 | ★ **252 の内訳が 42 側なら CLOSED** |

⟹ **どれも安い。高いのは設計・監査・規約の側である。**

---

## 6. 委嘱⑤ — 較正設計(T2 の B₄ 版)

### 6.1 正解データ(2008 §4.3・txt L3524–3546 逐語)

> **N⁽¹⁹⁾**(Philadelphia): $N_{\rm ord}=6$。**$F_2/N_{F_2}$ の中で pentagon (mod N⁽¹⁹⁾) を満たす $fN_{F_2}$ が 216 個**。そのうち **36 個**だけが、$m\in\{0,\dots,5\}$ で $2m+1$ が $\mathbb Z/6\mathbb Z$ の単元かつ $(m,f)$ が hexagon (2.18)(2.19)(mod $N^{(19)}_{PB_3}$)を満たす。
> **N⁽³⁴⁾**(Mighty Dandy): $N_{\rm ord}=9$。**$[F_2/N_{F_2},F_2/N_{F_2}]$ の中で** pentagon を満たすものが **4096 個**、うち hexagon へ持ち上がるのが **243 個**。

★ **宇宙の違いに注意**: N⁽¹⁹⁾ の 216 は**全体 $F_2/N_{F_2}$(7776 元)の中**、N⁽³⁴⁾ の 4096 は**交換子部分群の中**(254,016 元)。**この差を取り違えると較正が偽 PASS する**(Property 4.2 strong vs 4.3 weak の差)。

### 6.2 較正ゲート **CAL-B4**(発火前件・必須)

| # | 項目 | 期待値 | 由来 |
|---|---|---|---|
| **C-1** | $\psi:PB_4\to S_9$((4.3) の 6 置換)から $\lvert PB_4:N^{(19)}\rvert$ | **216** | Table 1 |
| **C-2** | (2.4) で $N^{(19)}_{PB_3}$、Prop 2.3 で $N_{\rm ord}$ | **6** | §4.3 |
| **C-3** | $\lvert F_2:N^{(19)}_{F_2}\rvert$ / $\lvert[F_2/N_{F_2},\cdot]\rvert$ | **7776** / **216** | Table 1 |
| **C-4** ★ | $F_2/N_{F_2}$ **全 7776 元**で (2.20) を検査 | **216 件 PASS** | §4.3 |
| **C-5** ★ | C-4 の 216 件 × $m\in\{0,2,3,5\}$($2m+1\in\{1,5\}$ = $\mathbb Z/6$ の単元)で hexagon (2.18)(2.19) | **36 件** | §4.3 |
| **C-6** | $\lvert\mathrm{GT}(N^{(19)})\rvert$ / $\lvert\mathrm{GT}^\heartsuit(N^{(19)})\rvert$ | **72** / **12**($\cong D_6$) | Table 1・§4.1 |
| **C-7**(任意) | N⁽³⁴⁾($\psi:PB_4\to S_{18}$・(4.4))で交換子部分群内 pentagon | **4096** → hexagon **243** | §4.3 |
| **C-8** ★ | **第三者照合**: Package GT の `PaB.py::penta` と自前判定を同一入力で突合 | 全一致 | litgate_pentagon §2.2 |
| **C-9** ★ | **定理 B4-VAC の実測**: $\tilde{\mathbf N}_{\rm core}$ での (2.20) 通過数 | **117,649**(全通過) | 本ノート §2.4 |

> ### ★ CAL-B4 の設計思想
> - C-1〜C-6 は**うちの窓を一切使わない**(N⁽¹⁹⁾ は $S_9$ の置換 6 個で完全に指定される)⟹ **窓構成(Prop 3.9・verbal lift)の議論から独立**。判定機だけを較正する。
> - C-4/C-5 は**(2.20) と (2.18)(2.19) の両方**を通す ⟹ 余面 (A.18) の簿記・(2.4) の交わり・Prop 2.3 の lcm・friendly 条件の**全経路**が同時に検査される。
> - C-9 は**本ノートの定理を検出器に変えたもの**: 「Prop 3.9 窓で 117,649 件全通過」が出なければ、余面か退化写像の実装に誤りがある。**期待値が既知の全通過**なので、識別力ゼロの検査を「通った」と報告する罠(§8.7.6 の SURJ 事故型)を避けるため、**C-9 は PASS 報告でなく「全通過でなければ STOP」という停止規則として運用する**。
> - **CAL-B4 が全 PASS するまで、NW(7) の B₄ 数値を 1 つも信用しない。**

---

## 7. 委嘱⑥ — 用語版差の防壁

### 7.1 対応表(2401 vs 2008)

| 概念 | **2008(B₄ 本来系)** | **2401(B₃-gentle)** | NW(7) での状態 |
|---|---|---|---|
| 窓 | $N\in\mathrm{NFI}_{PB_4}(B_4)$ | $N\in\mathrm{NFI}_{PB_3}(B_3)$ | **圏が違う**。B₄ 窓は $\tilde{\mathbf N}$ と書く(記号で分離) |
| GT-pair | hexagon×2 **+ pentagon** (Def 2.6) | hexagon×2 のみ | 差は pentagon 1 本 |
| **GT-shadow** | GT-pair + 全射 3 本 (Def 2.9) | **charming** GT-pair + 全射 (Def 3.7) | ★ **同名別物** |
| charming | $f$ が $[F_2,F_2]$ で代表 $\wedge$ $T^{F_2}$ 全射 (Def 2.19) | $2m+1$ 単元 $\wedge$ $f\in$ 商の交換子群(対レベル) | ★ **本窓では同値**(補題 CHARM-EQ・下記) |
| $\mathrm{GT}(N)$ | 非 charming 込み | (2401 の $\mathrm{GT}(N)$ は 2008 の $\mathrm{GT}^\heartsuit$ 側) | ★ Table 1 の **|GT| 列**と本走の **294** は**比較禁止** |
| $\mathrm{GT}^\heartsuit(N)$ | charming shadow | — | **比較は $\mathrm{GT}^\heartsuit$ 同士のみ** |
| genuine | $\widehat{GT}=\mathrm{Aut}(\widehat{PaB})$ 由来 | $\widehat{GT}_{gen}$ 由来 | ★ **別概念**(§4.3) |
| friendly | $2m+1$ 単元 (2.36) | (charming に内蔵) | $\mathcal X_{\mathbf N}$ の定義 |

> ### 補題 CHARM-EQ(本窓では版差が消える)
> NW(7) の宇宙($\bar f\in[P,P]$, $m\in\mathcal X$)では **2401-charming $\iff$ 2008-charming**。
> **証明.** 2008 (1): $\bar f\in[P,P]=[F_2,F_2]N_{F_2}/N_{F_2}$ $\iff$ $fN_{F_2}$ が $[F_2,F_2]$ の元で代表される。2008 (2) $T^{F_2}$ 全射 = SURJ で、H8′ により $\mathcal X$ の全 $m$・全 charming $\bar f$ で自動。2401 側の 2 条件も同一の 2 条件。∎
>
> ⟹ ★ **本窓では版差は pentagon の 1 ビットに封じ込められる**(これが防壁の本体)。

### 7.2 判定機への混入禁止規約(**R1–R6**)

| # | 規約 |
|---|---|
| **R1** | 判定機の入力・出力・cert には **framework tag** を必須欄とする: `FW=B4-2008` / `FW=B3-2401`。**タグなしの "shadow" という語を機械に渡さない。** |
| **R2** | cert に **window arity** 欄(3 or 4)と**実際に評価した方程式 ID の列**(`hex2.18`,`hex2.19`,`pent2.20` / `3.10`,`3.11`,`PENT_W`)を必須で書く。欄を欠く cert は無効。 |
| **R3** | 「genuine」は**必ず添字つき**で書く: $\text{genuine}_{\widehat{GT}}$ / $\text{genuine}_{\widehat{GT}_{gen}}$。裸の genuine は文書でも禁止。 |
| **R4** | **異 framework の計数を突き合わせない。** とくに Table 1 の `|GT|` 列(非 charming 込み)と本走の 294 を並べない。並べるのは `|GT♡|` 同士のみ。 |
| **R5** | 2008 の $N$ と本走の $\mathbf N$ は**別記号**($\tilde{\mathbf N}$ vs $\mathbf N$)。$\tilde{\mathbf N}_{PB_3}$ と $\mathbf N$ の関係は §2.6 の表を唯一の正本とする。 |
| **R6** | ★ **窓の「大きさ」を $\lvert PB_4:\tilde{\mathbf N}\rvert$ で語らない。** 律速量は $\lvert F_2:\tilde{\mathbf N}_{F_2}\rvert$ である(§3.5 注 3)。$7^{41}$ を Table 1 の $762{,}048$ と並べる文を書かない。 |

---

## 8. 工程表(条件付き実現可能)

| 工程 | 内容 | 前件 | コスト | 出力 |
|---|---|---|---|---|
| **P0** ★ | **CAL-B4 較正ゲート**(§6.2 C-1〜C-6, C-8) | なし | 秒〜分 | 判定機の免許 |
| **P0b** | C-7(N⁽³⁴⁾) | P0 | 分〜時間 | 第 2 フィクスチャ |
| **P1** | $R=PB_4/\mathcal V(PB_4)$ の構築(ANUPQ・p=7・class 4・表示 (A.3)) | P0 | 分 | pc 群 $R$・**予言 $\lvert R\rvert=7^{41}$** |
| **P2** | 5 本の $\bar\varphi:P\to R$ 構成 + $[P,P]$ 全 117,649 件で $D_{B_4}$ 評価 | P1 | 数分 | (2.20) 通過集合 |
| **P3** ★ | **同値試験**: P2 の通過集合 と lane P の $\mathrm{PENT}_W$ 通過集合の突合 | P2 + lane P cert | — | **【GAP-B4-1】の決着** |
| **P4** | C-9(Prop 3.9 窓で全通過)= 停止規則 | P1 | 分 | バグ検出器 |
| **P5** | (別軸・B₃)**BIT-252 決定実験**(§4.5) | prereg + 裁定 | 数分 | 252 の内訳(42 側なら CLOSED) |

### 8.1 事前登録する予言(IF-FIRST・**発火前に凍結**)

| ID | 予言 | 格 | 分岐 |
|---|---|---|---|
| **B4-EXQ-1** | $\lvert PB_4:\mathcal V(PB_4)\rvert=7^{41}$ | **T\***(紙の LCS 計算・付録 A.3) | 破れたら LCS 公式の適用ミス ⟹ STOP |
| **B4-EXQ-2** | $PB_4/\mathcal V(PB_4)\cong C_7\times Q$、$\lvert Q\rvert=7^{40}$ | **T\*** | 同上 |
| **B4-EXQ-3** | $\mathcal V(PB_4)_{PB_3}=\mathbf N_0$ | **T**(定理 B4-CANON (2)) | 実装バグ検出器 |
| **B4-EXQ-4** ★ | (2.20) mod $\mathcal V(PB_4)$ の通過集合 $=$ $\mathrm{PENT}_W$ の通過集合(**42 件**) | **C**(【GAP-B4-1】) | **(a)** 一致 ⟹ 2 系統一致(CV-9 判読へ)/ **(b)** B₄ が真に強い(42 未満)⟹ **$\mathfrak G_{\rm ar}<42$ ⟹ BH-α-pent と矛盾 ⟹ 全面点検**/ **(c)** B₄ が真に弱い(42 超)⟹ (2.20)-PASS かつ $\mathrm{PENT}_W$-FAIL の新類 |
| **B4-EXQ-5** | CAL-B4: 216 / 36(N⁽¹⁹⁾)・4096 / 243(N⁽³⁴⁾) | **T**(公表値・情報量ゼロ = **バグ検出器**) | 不一致 ⟹ STOP |
| **B4-EXQ-6** | Prop 3.9 窓での (2.20) 通過数 $=117{,}649$(全通過) | **T**(定理 B4-VAC) | 不一致 ⟹ 実装 STOP |
| **B4-EXQ-7** | BIT-252: $\mathfrak G^{\rm gentle}_{\rm genuine}\in\{42,294\}$ | **T\***(命題 BIT-252) | 中間値が出たら前件(isolated/294/42)のどれかが偽 ⟹ STOP |

★ **格 T の予言は的中しても情報量ゼロ**(票 v1 §0-4 の規律)。**バグ検出器としてのみ運用する。**

---

## 9. 格付け・【GAP】・規律申告

### 9.1 読んだ範囲の申告(文献ゲート第 6 項)

- `papers/txt/2008.00066-what-are-gt-shadows.txt`: **L2563–2610**(Prop 3.9 とその証明)/ **L2638–2660**(Prop 3.9 の用途)/ **L3516–3546**(§4.3 の N⁽¹⁹⁾・N⁽³⁴⁾ 段落)/ **L3548–3581**(Question 4.4–4.7)/ Table 1 の該当列(L3170–3325 の数値ブロック)。**それ以外は抽出ノート `b4_original_gtshadows_extraction_v1.md` の記述に依拠**し、原文頁画像は本ノートでは 1 枚も開いていない。
- 外部文献検索は**ゼロ**。papers/ の新規 PDF を開いていない。

### 9.2 【GAP】一覧

| 札 | 内容 | 状態・処方 |
|---|---|---|
| ★ **【GAP-B4-1】** | (2.20) の余面 5 項 $\leftrightarrow$ $\mathrm{PENT}_W$ の $\rho$ 5 回転 の**項対応**。CENT-FREE は $Z(PB_4)$ のずれのみを扱い、これを仮定している | **UNKNOWN**。処方 = **工程 P3 の機械同値試験**(紙で仮定しない)。または §9.3 の【文献要請】 |
| **【GAP-B4-2】** | 2008 の GT-shadow に **practical でない元**があり得るか($\mathbb Z\times F_2$ で代表できない onto 射の存否)は**原論文でも未解決**(p.23) | **UNKNOWN(原論文由来)**。系 B4-42 は `practical` 制限つきでのみ主張する。**Table 1 の数値も practical**(2008 §4 脚注 5)なので較正には影響しない |
| **【GAP-B4-3】** | Cor 3.13 の survival 減少列の**停止点に有効上界がない** | **UNKNOWN**。陰性は 1 窓で有限・陽性はサンドイッチでのみ(§4.2)。【文献要請】§9.3 |
| **【GAP-B4-4】** | 工程 P3 の突合には $[P,P]$ の**共通ラベル付け**が要る(CV-9 危険)。別プロセスの index join は規約事故の温床 | **処方**: 同値試験は「同一 GAP プロセスで $Q$ と $R$ の両述語を同一列挙上で評価」。ただしこれは探索器/照合器分離を崩すので、**発見用の数値は既存 lane P cert を正本とし、P3 は仕様同一性試験としてのみ位置づける**。falsifier の CV-9 判読を必須前件に |
| **【GAP-B4-5】** | 命題 BIT-252 の前件 (i)「$K$ も isolated」: $K_{F_2}=\gamma_6F_2^7$ は verbal ゆえ VERBAL-ISO が使えるが、**VERBAL-ISO の証明は $c\in N$ を前件に置いている**(auto_settled_check §3.4 逐語) | **要確認**。$K=\mathcal V_5(F_2)\times\langle c\rangle$ は $c\in K$ を満たすので**前件充足**(本ノートの読み)。Sol 検分を請う |

### 9.3 【文献要請】(2 件)

> ### 【文献要請 B4-L1】(**優先**)
> **困難**: Drinfeld 型 pentagon(4 本紐・余面 5 本: $f^{2,3,4}f^{1,23,4}f^{1,2,3}=f^{1,2,34}f^{12,3,4}$)と、球面型 5-巡回 pentagon($\rho^4(f)\rho^3(f)\rho^2(f)\rho(f)f=1$ in $\Gamma_{0,5}$)の**同値**を、**項ごとの明示的な対応(必要なら共役子の telescoping)つきで**述べている箇所。
> **欲しい結果の型**: 「$K(0,5)=PB_4/Z(PB_4)$ の中で、$\varphi_\bullet(f)$ の像 5 個が $\rho^i(j(f))$ の並べ替え(+ 明示共役)に一致する」という**計算可能な辞書**。あるいは「両者は (I)(II) の下で同値」という**前件つき**の定式化(前件がある場合、それが何かを明示)。
> **既在候補**(papers/ に既にある・司令塔判断で節 pin を): `lochak-schneps-1994-LMS200-GT-automorphisms-braid-groups.pdf`、`lochak-schneps-universal-ptolemy-teichmuller-groupoid.pdf`、`harbater-schneps-2000-*`。
> **代替**: 工程 P3 の機械同値試験(117,649 件悉皆)で**この窓に限り**経験的に決着できる ⟹ **文献が降りなくても走行は止まらない**。

> ### 【文献要請 B4-L2】(非緊急)
> **困難**: Cor 3.13 の survival 減少列が**いつ停止するか**の有効上界。
> **欲しい結果の型**: 「$\mathrm{GT}^\heartsuit(N)$ の位数(または $\lvert F_2:N_{F_2}\rvert$)から、$\mathfrak G_{\rm genuine}$ に到達する窓の深さを bound する」型の言明。profinite 群の有限商の族に対する Mittag-Leffler の**有効版**。**無いなら「無い」で確定させたい**(その場合サンドイッチが唯一の道であると記帳できる)。

### 9.4 格付け

| 対象 | 格 |
|---|---|
| 補題 **B4-FORGET** | ★ **paper-proof**(標準事実の同定・2 行) |
| 補題 **B4-IND** | ★ **paper-proof**(付録 A.1 の記号計算で機械確認済) |
| ★ 定理 **B4-VAC** | ★ **paper-proof**(付録 A.1/A.2 で機械確認済)**Sol 未監査** |
| ★ 定理 **B4-CANON** | ★ **paper-proof candidate**((4) の位数は付録 A.3 の級数計算 = **機械**。$\lvert Q\rvert=7^{40}$ を再現している点が傍証)**Sol 未監査** |
| 補題 **B4-MONO** / 定理 **B4-DIR** | ★ **paper-proof**(ただし (c) 後半は CENT-FREE 相対・【GAP-B4-1】相対) |
| 補題 **B4-KAPPA** | ★ **paper-proof candidate**(2401 Prop 3.4 と独立に同結論。**起草者が同一系統なので `cross-checked` は付さない** — CV-9 未実施) |
| ★ 系 **B4-42** | **conditional candidate**((H1)–(H5) 相対・とくに BH-α-pent 相対) |
| ★ 命題 **BIT-252** | ★ **paper-proof candidate**(前件 (i)(ii)(iii) 相対・【GAP-B4-5】) |
| 補題 **CHARM-EQ** | ★ **paper-proof**(H8′ 相対) |
| `verified` | ✗ 付かない(Lean 未使用) |
| `cross-checked` | ✗ 付かない(CV-9 判読未実施) |
| **novelty** | ★ **主張しない**。系 B4-42 が Question 4.7 の型の実例であることは**原文の問い(txt L3578–3581)との照合**にすぎず、**先行の有無は未調査**。主張するなら司令塔が repo/台帳 grep + 文献検査を先に通すこと |

### 9.5 規律申告

- ★ **本走宇宙(705,894 対)の候補を 1 件も評価していない。** GAP も pc 群も起動していない。機械は付録 A の python のみ(**記号的な語計算 + 整数級数**、群の元の列挙ゼロ)。
- **封印 3 量($n=5$ 関連・$\mathrm{Im}\,R$・$d_N$・$u$ 値)非接触。**
- **既在文書を 1 バイトも改変していない**(票 v1・prereg・翻訳ノート・仲裁ノートすべて read-only)。
- **HS Prop 7 の lift 存在形を使っていない**(罠 D-5 遵守)。$\widehat{GT}$ の使用は 2008 の定義・Cor 3.13・Thm 3.8 と HSP-SOUND(既在)のみ。
- **新しい停止規則を発効させない**。§6.2 C-9 と §8.1 の分岐は**提案**であり、発効は司令塔裁定 + Sol ゲート。

---

## 10. Sol への監査点(4 点)

> **Q-1 ★★ 定理 B4-VAC と、それが Prop 3.9 の読みに与える含意**(§2.4)。「Prop 3.9 の $\tilde\psi$ 窓は charming $f$ 上で pentagon が恒真ゆえ、252 の判定に使えない」という結論を認めるか。とくに補題 B4-FORGET($\tilde\psi=\psi\circ p_4$)と、$B_4$-核が $\bigcap_ip_i^{-1}(N)$ になる一段(共役が「第 $i$ の紐を忘れる」に対応し、捻れが $N\trianglelefteq B_3$ で吸収される)に穴がないか。

> **Q-2 ★★ 定理 B4-CANON (2) の厳密等号**(§2.5)。$\tilde{\mathbf N}^*_{PB_3}=\mathcal V(PB_3)=\mathbf N_0$ を、$p_4\circ\varphi_{123}=\mathrm{id}$ による分裂単射論法で出した一段。**5 本の余面のうち 1 本が分裂単射であれば残り 4 本を見なくてよい**、という論法の可否。

> **Q-3 ★★ 【GAP-B4-1】の扱い方**(§3.2)。(2.20) の余面形と $\mathrm{PENT}_W$ の $\rho$ 形の項対応を**紙で証明せず、117,649 件の悉皆一致で経験的に決める**という設計判断を認めるか。認めない場合、(a) 文献 pin(【文献要請 B4-L1】)を待つ、(b) 球面関係式から項対応を紙で構成する、のどちらを指示するか。**また、経験的一致が得られた場合の格付け**(`cross-checked` を付してよいか、CV-9 判読の対象になるか)の指示を請う。

> **Q-4 ★★ 命題 BIT-252 と決定実験の位置づけ**(§4.4–4.5)。「252 の内訳は 1 ビットで、42 側なら 1 元 × 1 窓 × 117,649 件で決着する」という縮約を認めるか。とくに (a) $\mathfrak G^{\rm gentle}_{\rm genuine}$ が部分群であること(逆極限の像 = 減少交わり)、(b) $[\mathrm{GT}(\mathbf N):\mathfrak G_{\rm ar}]=7$ 素数からの中間排除、(c) **この実験が B₄ でなく B₃-gentle 側にある**という管轄の判定(§4.3)。

---

## 付録 A. 機械検算(**本走非接触**・記号計算と整数級数のみ)

### A.1 20 本の合成 $\psi\circ p_i\circ\varphi$(補題 B4-IND・定理 B4-VAC の土台)

スクリプト `scratchpad/b4comp.py`(自由群の語簡約のみ・群の元の列挙ゼロ)。入力は (A.18) の余面表と $p_i$ の生成元値、$\psi(x_{12})=x,\psi(x_{23})=y,\psi(x_{13})=x^{-1}y^{-1}$。

```
=== 20 composites  psi o p_i o phi   (images of x12, x23) ===
  p_4 o phi123     : x12->x        x23->y          = psi
  p_4 o phi234     : x12->y        x23->1          cyclic-image (DEGENERATE)
  p_4 o phi12_3_4  : x12->x^-1     x23->1          cyclic-image (DEGENERATE)
  p_4 o phi1_23_4  : x12->y^-1     x23->1          cyclic-image (DEGENERATE)
  p_4 o phi1_2_34  : x12->x        x23->y          = psi
  p_3 o phi123     : x12->x        x23->1          cyclic-image (DEGENERATE)
  p_3 o phi234     : x12->1        x23->1          cyclic-image (DEGENERATE)
  p_3 o phi12_3_4  : x12->1        x23->1          cyclic-image (DEGENERATE)
  p_3 o phi1_23_4  : x12->x        x23->y          = psi
  p_3 o phi1_2_34  : x12->x        x23->y          = psi
  p_2 o phi123     : x12->1        x23->1          cyclic-image (DEGENERATE)
  p_2 o phi234     : x12->1        x23->y          cyclic-image (DEGENERATE)
  p_2 o phi12_3_4  : x12->x        x23->y          = psi
  p_2 o phi1_23_4  : x12->x        x23->y          = psi
  p_2 o phi1_2_34  : x12->1        x23->1          cyclic-image (DEGENERATE)
  p_1 o phi123     : x12->1        x23->x          cyclic-image (DEGENERATE)
  p_1 o phi234     : x12->x        x23->y          = psi
  p_1 o phi12_3_4  : x12->x        x23->y          = psi
  p_1 o phi1_23_4  : x12->1        x23->x^-1       cyclic-image (DEGENERATE)
  p_1 o phi1_2_34  : x12->1        x23->y^-1       cyclic-image (DEGENERATE)
```

- **8 本が $\psi$**(核 $=\mathbf N$)、**12 本が退化**(像が位数 7 の巡回群)。1 行目 `p_4 o phi123 = psi`(生成元 3 つとも保存)が **$p_4\circ\varphi_{123}=\mathrm{id}_{PB_3}$**(定理 B4-CANON (2) の分裂単射)。
- 退化 12 本の $c$ 上の値は $c=x_{12}x_{13}x_{23}$ から従い、核の条件は $\varepsilon(f)+k\equiv0$ か $k\equiv0\ (\mathrm{mod}\ 7)$。$f\in\mathcal V(F_2)$ で $\varepsilon(f)\equiv0$ ⟹ **総合して $k\equiv0\ (7)$** ⟹ 補題 B4-IND。

### A.2 pentagon の恒真性(定理 B4-VAC)

```
=== pentagon (2.20) modulo ker(psi-tilde) and modulo the B4-core, on charming f ===
    rule: a DEGENERATE substitution sends every f in [F2,F2] to 1 (abelian image).
  coord i=4 :  LHS = f(x,y)   RHS = f(x,y)   -> IDENTITY (no pentagon content)
  coord i=3 :  LHS = f(x,y)   RHS = f(x,y)   -> IDENTITY (no pentagon content)
  coord i=2 :  LHS = f(x,y)   RHS = f(x,y)   -> IDENTITY (no pentagon content)
  coord i=1 :  LHS = f(x,y)   RHS = f(x,y)   -> IDENTITY (no pentagon content)
```

### A.3 LCS 階数と窓の指数(定理 B4-CANON (4))

スクリプト `scratchpad/lcs.py`(有理数係数の形式級数のみ)。$\prod_k(1-t^k)^{\phi_k}=\prod_{i=1}^{n-1}(1-it)$ を次数 6 まで解く。

```
PB_4 LCS ranks (deg1..6): [6, 4, 10, 21, 54, 125]
PB_3 LCS ranks (deg1..6): [3, 1, 2, 3, 6, 9]
sum deg<=4 for PB4: 41 => |PB4 : gamma5 PB4^7| = 7^41
K(0,5) = PB4/Z  => ranks [5, 4, 10, 21] sum 40
Witt(2,k) k=1..5: [2, 1, 2, 3, 6]
```

- $K(0,5)$ の階数 $(5,4,10,21)$ は**翻訳ノート §5 補題 NW-1b (6) の「$5,4,10,21$」と一致** ⟹ $\lvert Q\rvert=7^{40}$(NW-P4)を紙側から独立に再現。
- $PB_3$ の階数 $(3,1,2,3,\dots)$ は Witt$(2,k)=(2,1,2,3,6)$ に中心の $+1$($k=1$)を足したもの ⟹ $\lvert PB_3:\mathcal V(PB_3)\rvert=7^{3+1+2+3}=7^9$、$\lvert P\rvert=7^{8}$(NW-P2)と整合。
- $\mathcal V_5(F_2)=\gamma_6F_2^7$ での $\lvert P'\rvert=7^{2+1+2+3+6}=7^{14}$(§4.5 の決定実験の見積り)。

> **注**: いずれも「類 $<p=7$ ゆえ正則 $p$ 群(Lazard)で $\lvert G/\gamma_{c+1}GG^p\rvert=p^{\text{Hirsch 長}}$」という一段を使っている。この一段は工房の既在計算($\lvert P\rvert=7^8$・$\lvert Q\rvert=7^{40}$)が実測で支持している。
