# B₄ 窓での 252 直接裁定 — 実現可能性ノート(**v1.2**)

**状態札: `candidate(実現可能性ノート・紙のみ / 機械は付録 A の記号計算+整数級数+F₇ 線型代数+忠実 Artin 表現での語同一性検査のみ / 本走宇宙の候補評価ゼロ / 封印非接触 / novelty 主張なし)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-06
- 版: **v1.2**。**v1(`…_v1.md`・commit `eeaf198`)と v1.1(`…_v1_1.md`・commit `3eeeb79`)は 1 バイトも改変せず並置**。差分の全一覧 = **§11**。
- 委嘱: 司令塔(**裁定 598** 初版 / **裁定 608** v1.1 / **PENT-FORM 相互検分 PASS を受けた改版指示** v1.2)。v1.2 の入力:
  - 相互検分の結果(**PENT-FORM = PASS**)+ 司令塔の 7 項改版指示
  - `docs/notes/b4_theorem_check_v1.md`(検分ノート)/ `docs/scout/ls_pentagon_term_correspondence_v1.md`(文献 pin)
  - ★ **原文 PDF 逐語**: `papers/dolgushev-2008.00066-gt-shadows-original.pdf` **p.23 / p.25 / p.39**(本起草者が**頁画像で直接確認**・§9.1)

---

## 0. 結論(三択・先に 7 行)

> ## ★ 判定 = **条件付き実現可能**(工程表 = §8、欠けの列挙 = §9.2)
> **v1.2 での格上げ 3 件**: ① **定理 PENT-FORM の格が「文献相対」から「正典 + $\Delta^2$ + Hurwitz 相対」へ**(球面関係 LS-(4) を自前導出・§3.2.1)② **$S_0$ 層(全 117,649)にも無条件の予言がついた**(定理 **PENT-FORM′**・§3.2.3)⟹ 工程 P3 の**全層がバグ検出器**になった ③ **practical 制限が消えた**(2008 原文 p.39 逐語「every charming GT-shadow is practical」⟹ 前件 (H4) と【GAP-B4-2】を削除・§3.6)。

| # | 結論 |
|---|---|
| **0-1** | ★★ **委嘱の問いは二つに割れる。片方は既に裁定済み、もう片方は B₄ の管轄外。** (α)「252 は B₄ 本来系の genuine か」= **既に否**(B₄ の寄与は新情報でなく**根拠の差し替え**)。(β)「252 の**内訳**(gentle 系の genuine か)」= **B₄ では原理的に裁けない**(B₄ の極限は $\widehat{GT}$、内訳が問うのは $\widehat{GT}_{gen}$)。**法廷が違う**(§4.3)。 |
| **0-2** | ★★ **Prop 3.9 の構成に現れる 2 つの自然な窓は使えない**: $\ker\tilde\psi$ とその $B_4$-核 $\tilde{\mathbf N}_{\rm core}$ で **pentagon (2.20) は全 charming $f$ に恒真**(**定理 B4-VAC**・§2.4)。⟹「$\mathrm{PENT}_W$-FAIL ⟹ (2.20)-FAIL」は**この 2 窓では偽**、**252 全件が反例**(舞台 = $\tilde{\mathbf N}_{\rm core}$)。**Prop 3.9 が最終的に取る $\tilde N$ の検出力は未知・構成不能。** |
| **0-3** | ★★ 使える窓は **$\tilde{\mathbf N}^*:=\mathcal V(PB_4)=\gamma_5(PB_4)PB_4^{\,7}$**。$\in\mathrm{NFI}_{PB_4}(B_4)$、$\tilde{\mathbf N}^*_{PB_3}=\mathcal V(PB_3)=\mathbf N_0$(**厳密等号**)、$\tilde{\mathbf N}^*_{F_2}=N_{F_2}$、$\tilde N^*_{\rm ord}=7$、$\lvert PB_4:\tilde{\mathbf N}^*\rvert=7^{41}$、$PB_4/\tilde{\mathbf N}^*\cong C_7\times Q$(**定理 B4-CANON**)。 |
| **0-4** | ★★ **hexagon 側は新情報ゼロが定理として出る**(2401 **Prop 3.4**)⟹ **B₄ 裁定の実体は pentagon 1 本に完全に縮約される**。 |
| **0-5** ★改 | ★★★ **pentagon の形の同定は 2 段で閉じた**。**無条件**(§3.2.3 **PENT-FORM′**): 全 $f\in[F_2,F_2]$ で $$(2.20)\iff \tilde D(f):=f(x_{45},x_{34})^{-1}f(x_{12},x_{15})^{-1}f(x_{23},x_{34})f(x_{45},x_{51})f(x_{12},x_{23})=1 .$$ **(I)=(3.10) を足すと**(§3.2.2 **PENT-FORM**): $\tilde D=D$ となり $(2.20)\iff\mathrm{PENT}_W$。使う材料は **球面関係 4 回・中心元吸収 3 回・(I) 2 回**のみ、**(II) は不使用**、**全段が等式代入ゆえ可逆**。**HS2000 Prop 7 は使用しない**(lift 量化子 = 罠 D-5)。 |
| **0-6** ★改 | ★★ 条件が揃えば $\mathrm{GT}^\heartsuit_{2008}(\tilde{\mathbf N}^*)=\textbf{42}$・**全元 genuine**(**系 B4-42**・§3.6)= 2008 **Question 4.7** が求める型の実例。★ **practical の但し書きは不要**(2008 p.39 逐語)。**novelty は主張しない**。 |
| **0-7** | ★ 内訳(β)は **1 ビット**(**命題 BIT-252**): $\mathfrak G_{\rm gen}^{\rm gentle}(\mathbf N)\in\{42,294\}$、中間なし。**42 側は 1 元 × 1 窓 × 117,649 件で決着**。294 側なら **$\widehat{GT}\to\widehat{GT}_{gen}$ が全射でない**ことが有限窓で証人つきになる。**実験は B₃-gentle 側。** |

---

## 1. 記号・前提・引用と自前導出の分離

### 1.1 うちの窓(既在・再測定しない)

$$\mathbf N=\mathcal V(F_2)\times\langle c\rangle,\quad \mathbf N_0=\mathcal V(PB_3)=\mathcal V(F_2)\times\langle c^{7}\rangle,\quad N_{F_2}=\mathcal V(F_2)=\gamma_5(F_2)F_2^{\,7},$$
$$W=\mathcal V(K(0,5)),\quad P=F_2/N_{F_2}\ (7^8),\quad Q=K(0,5)/W\ (7^{40}),\quad \lvert[P,P]\rvert=7^6=117{,}649 .$$
本走の答え = hexagon **294**・$\mathrm{PENT}_W$ **42**・hexagon-only **252**。$PB_3=F_2\times\langle c\rangle$、$c=x_{12}x_{13}x_{23}=x_{23}x_{12}x_{13}=(\sigma_1\sigma_2)^3$(**A.5**)。

### 1.2 引用する既在の結果 ★改(**文献相対の依存を 2 行削除**)

| 札 | 内容 | 出所 |
|---|---|---|
| **(2.20)** | pentagon(**$f$ のみの条件**) | 2008 Def 2.6・p.13(頁画像照合済) |
| **(A.18)/(A.3)/(A.5)/(A.2)** | 余面 5 本の生成元値・$PB_4$ の関係式・$c$ と $Z(PB_3)$・$x_{ij}$ の定義 | 2008 App A(頁画像照合済 = litgate_pentagon §6) |
| **(2.4)** / **Prop 2.3** / **Prop 2.10** / **Def 2.9** / **Def 2.19** / **Remark 2.15** / **Cor 3.13** / **Thm 3.8** / **Q4.6** / **Q4.7** | 2008 の定義・命題群 | 同上。**Def 2.19(p.25)・Remark 2.15(p.23)・§4 冒頭(p.39)は本起草者が頁画像で直接確認**(§9.1) |
| **Prop 3.4** | $(m,f)\in\mathbb Z\times[F_2,F_2]$ の hexagon 判定は $N_{F_2}$ **のみ**に依存 | 2401 §3 p.11(仲裁ノート §1 に逐語) |
| **K(0,5) の表示** | $K(0,5)\cong PB_4/\langle\Delta_4^2\rangle$、$x_{i5}$ は基点 $i$ の **Hurwitz 関係**で定まる | 翻訳ノート §1.0(工房の $K(0,5)$ の定義)+ pin B-1(頁画像照合済)。★ **$\mathrm{PENT}_W$ の定義自体がこの表示に立っている**ので、本ノートの新規依存ではない(§3.2.4) |
| ~~LS-(4)~~ | ~~球面関係~~ | ★ **v1.2 で自前導出に置換**(補題 **SPH**・§3.2.1) |
| ~~LS-(abs)~~ | ~~中心元吸収~~ | ★ **v1.2 で自前証明に置換**(補題 **ABS**・§3.2.1) |
| **VERBAL-DESCENT** | $\mathcal V(Q)=\mathcal V(R)=1$ ゆえ任意の $h:F_2\to Q$ で $h(N_{F_2})=1$ | 検分ノート §5.3 |
| **CENT-FREE / VERBAL-ISO / H8′ / BH-α-pent v1.1 / HSP-SOUND / GRP** | 既在 | v1 §1.2 のまま |

### 1.3 本ノートが自前で導く命題

補題 **B4-FORGET** / 補題 **CORE-4** / 補題 **B4-IND** / ★定理 **B4-VAC** / ★定理 **B4-CANON** / 補題 **B4-MONO** / 定理 **B4-DIR** / ★補題 **SPH**(v1.2 新) / ★補題 **ABS**(v1.2 新) / ★★定理 **PENT-FORM′**(v1.2 新・**無条件**) / ★★定理 **PENT-FORM**(条件つき) / 系 **PENT-EQ** / 補題 **B4-KAPPA** / ★系 **B4-42** / ★命題 **BIT-252** / 補題 **CHARM-EQ** / ★補題 **CHARM⟹PRACT**(v1.2 新)。

---

## 2. 委嘱① — 窓の持ち上げ(v1.1 から不変)

### 2.1 Prop 3.9 の読み(要点 3 つ)

① $\ker\tilde\psi$ は $B_4$-正規とは限らない ② Dolgushev の $\tilde N$(指数 $\lvert PB_4:\ker\tilde\psi\rvert$ の正規部分群**全交わり**)は**構成不能** ③ Cor 3.5 の isolated 化でさらに細かくなる。⟹ **Prop 3.9 は cofinality の存在定理であってレシピではない。**

### 2.2 補題 **B4-FORGET** と 補題 **CORE-4**

> **B4-FORGET**: $p_4:PB_4\to PB_3$(第 4 紐忘却)について $\tilde\psi=\psi\circ p_4$。$\ker\tilde\psi=p_4^{-1}(N)$。∎

> ### 補題 CORE-4
> $N\trianglelefteq B_3$、$N\le PB_3$、有限指数とし、$p_i$ を「第 $i$ の紐を忘れ、残る 3 本を**順序保存**で $1,2,3$ に付け替える射」とすると
> $$\mathrm{core}_{B_4}\bigl(p_4^{-1}(N)\bigr)=\bigcap_{i=1}^{4}p_i^{-1}(N).$$
> **証明.** **(1)** $B_{3,1}:=\{b\in B_4:w_b(4)=4\}$(指数 4)上で $p_4$ は準同型に延び、$u\in B_{3,1}$ に対し $u\,p_4^{-1}(N)u^{-1}=p_4^{-1}(N)$。**(2)** 代表元 $b_4=1,\ b_3=\sigma_3,\ b_2=\sigma_2\sigma_3,\ b_1=\sigma_1\sigma_2\sigma_3$。**(3)** (A.2)/(A.6) から、6 生成元すべてで
> $$p_4\circ c_{\sigma_3^{-1}}=p_3,\qquad p_3\circ c_{\sigma_2^{-1}}=p_2,\qquad p_2\circ c_{\sigma_1^{-1}}=p_1$$
> が**厳密に**成立する(表は v1.1 §2.2。$\sigma_3^{-1}x_{14}\sigma_3=x_{13}$、$\sigma_3^{-1}x_{24}\sigma_3=x_{23}$、$\sigma_2^{-1}x_{34}\sigma_2=x_{24}$、$\sigma_1^{-1}x_{24}\sigma_1=x_{14}$ はいずれも厳密な等式)。合成して $p_4\circ c_{b_i^{-1}}=p_i$。**(4)** $b=b_iu$ と書けば $b\,p_4^{-1}(N)b^{-1}=\ker(\psi p_i)=p_i^{-1}(N)$。∎

$\tilde{\mathbf N}_{\rm core}:=\bigcap_i\ker(\psi p_i)\in\mathrm{NFI}_{PB_4}(B_4)$、$PB_4/\tilde{\mathbf N}_{\rm core}\hookrightarrow P^4$。★ $p_i(\Delta^2)=c\in\mathbf N$ ⟹ **$Z(PB_4)\le\tilde{\mathbf N}_{\rm core}$**(付録 A.4 の $\mathbb F_7$-階数 5 が裏づけ)。

### 2.3 補題 **B4-IND**: $(\ker\tilde\psi)_{PB_3}=(\tilde{\mathbf N}_{\rm core})_{PB_3}=\mathbf N_0$

20 本の合成 $\psi p_i\varphi$(**付録 A.1 の完全表**)は **8 本が $\psi$**・**12 本が退化**(像は位数 7 の巡回群)。**12 本すべてで $\lambda(c)\ne1$** ⟹ $w=fc^k$($f\in\mathcal V(F_2)$)に対し**退化 1 本だけで $k\equiv0\ (7)$** が出る。逆包含は自明。∎

### 2.4 ★ 定理 **B4-VAC**

> $\tilde{\mathbf N}\in\{\ker\tilde\psi,\tilde{\mathbf N}_{\rm core}\}$ では (2.20) が全 charming $f$ に**恒真**。各座標で 5 本のうち 2 本が $\psi$・3 本が退化(退化像は可換かつ指数 7 ゆえ $[F_2,F_2]$ も $\mathcal V(F_2)$ も潰す)⟹ 4 座標すべて恒等式。∎

> ### ★ 委嘱②への直接回答(その 1)
> $$\boxed{\ \textbf{「}\mathrm{PENT}_W\textbf{-FAIL}\Rightarrow(2.20)\textbf{-FAIL」は }\tilde{\mathbf N}_{\rm core}\textbf{ では偽であり、252 の全件が反例である。}\ }$$
> ⚠ **射程**: 本定理は Prop 3.9 の**構成の途中に現れる 2 窓**の言明。最終的な特性部分群 $\tilde N$ の検出力は**未知**(§2.6 の表と整合)。

### 2.5 ★ 定理 **B4-CANON**

$\tilde{\mathbf N}^*=\mathcal V(PB_4)$ について **(1)** $\in\mathrm{NFI}_{PB_4}(B_4)$ **(2)** $\tilde{\mathbf N}^*_{PB_3}=\mathcal V(PB_3)=\mathbf N_0$(**厳密等号**。$p_4\circ\varphi_{123}=\mathrm{id}$ による分裂単射論法)、$\tilde{\mathbf N}^*_{F_2}=N_{F_2}$、$\tilde N^*_{\rm ord}=7$ **(3)** $PB_4\cong\mathbb Z\times K(0,5)$ ゆえ $PB_4/\tilde{\mathbf N}^*\cong C_7\times Q$ **(4)** $\lvert PB_4:\tilde{\mathbf N}^*\rvert=7\cdot7^{40}=7^{41}$((3)+既在実測 $\lvert Q\rvert=7^{40}$ から直ちに)。∎

### 2.6 4 つの窓の比較

| 窓 | 定義 | $\tilde{\mathbf N}_{PB_3}$ | $B_4$ 正規 | 計算可能性 | pentagon 検出力 |
|---|---|---|---|---|---|
| $\ker\tilde\psi$ | $p_4^{-1}(\mathbf N)$ | $\mathbf N_0$ | ✗(2008 の窓ではない) | ◎($P$) | **ゼロ** |
| $\tilde{\mathbf N}_{\rm core}$ | $\bigcap_ip_i^{-1}(\mathbf N)$ | $\mathbf N_0$ | ✓ | ◎($P^4$) | **ゼロ** |
| Prop 3.9 の $\tilde N$ | 指数 $7^8$ の正規部分群 全交わり(+Cor 3.5) | $\le\mathbf N_0$ | ✓ | ✗(構成不能) | **未知** |
| ★ $\tilde{\mathbf N}^*=\mathcal V(PB_4)$ | $\gamma_5PB_4^{\,7}$ | $\mathbf N_0$(等号) | ✓ | ◎(pc 群 $7^{41}$・**環境ブロッカー** §5.4) | ★ **$W$ 水準** |

---

## 3. 委嘱② — 判定の形と $\mathrm{PENT}_W$ との論理関係

### 3.1 補題 **B4-MONO** と 定理 **B4-DIR**

> **B4-MONO**: $\tilde{\mathbf N}'\le\tilde{\mathbf N}$ なら (2.20) mod $\tilde{\mathbf N}'$ ⟹ (2.20) mod $\tilde{\mathbf N}$。
> **B4-DIR**: **(a)** $\tilde{\mathbf N}\le L$($L$ = $W$ の $PB_4$ への逆像)なら $\mathrm{PENT}_W$-FAIL ⟹ (2.20)-FAIL。**(b)** そうでない窓では偽(反例 = B4-VAC)。**(c)** charming $f$ では pentagon defect $D\in[PB_4,PB_4]=[K(0,5),K(0,5)]$ ゆえ $D\in\tilde{\mathbf N}^*\iff D\in L\iff\bar D\in W$ — **$\tilde{\mathbf N}^*$ が中心を丸ごとは含まないことは判定に影響しない**。

### 3.2 ★★ pentagon の形の同定(**v1.2 で 2 段化・自前化**)

#### 3.2.1 準備 — 自前の 2 補題

> ### ★ 補題 **SPH**(球面関係の**自前導出**)
> $K(0,5)=PB_4/\langle\Delta_4^2\rangle$ とし、$x_{i5}$ は基点 $i$ の Hurwitz 関係で定める。このとき
> $$\boxed{\ x_{45}=x_{12}x_{13}x_{23}=c=\varphi_{123}(c),\qquad x_{15}=x_{23}x_{24}x_{34}=\varphi_{234}(c).\ }$$
> **証明.**
> **(1)** $\Delta_4^2=x_{12}\,(x_{13}x_{23})\,(x_{14}x_{24}x_{34})=c\,(x_{14}x_{24}x_{34})$ — **忠実な Artin 表現 $B_4\hookrightarrow\mathrm{Aut}(F_4)$ での機械検算**(付録 A.5)。
> **(2)** 基点 4 の Hurwitz: $x_{14}x_{24}x_{34}x_{45}=1$ ⟹ $x_{45}=(x_{14}x_{24}x_{34})^{-1}$。
> **(3)** $K(0,5)$ では $\Delta_4^2=1$、よって (1) から $x_{14}x_{24}x_{34}=c^{-1}$。(2) と合わせて **$x_{45}=c$**。
> **(4)** $[x_{14},x_{23}]=1$((A.3) の**入れ子**の場合 $1<2<3<4$。機械検算 = 付録 A.5)⟹ $\Delta_4^2=x_{12}x_{13}\,x_{14}\,x_{23}x_{24}x_{34}$。
> **(5)** 基点 1 の Hurwitz: $x_{12}x_{13}x_{14}x_{15}=1$ ⟹ $x_{15}=(x_{12}x_{13}x_{14})^{-1}$。(4) と $\Delta_4^2=1$ から $x_{12}x_{13}x_{14}=(x_{23}x_{24}x_{34})^{-1}$、よって **$x_{15}=x_{23}x_{24}x_{34}$**。∎
>
> ★ **構造的な読み**: $\varphi_{123}(c)=x_{12}x_{13}x_{23}$、$\varphi_{234}(c)=x_{23}x_{24}x_{34}$((A.18))。すなわち **2 本の余面による $PB_3$-中心の像が、球面の 2 本の「余分な」生成元 $x_{45},x_{15}$ になる**。
> ★ **格**: 使ったのは (A.2)(A.3)(A.5)(A.18)(**正典**)+ $\Delta_4^2$ の積表示(**機械検算・忠実表現**)+ $K(0,5)$ の Hurwitz 表示。**文献 pin への依存はここで消えた。**

> ### 補題 **ABS**(中心元吸収・**自前証明**・$\gamma$ の指数を明示)
> $G$ を群、$\alpha,\beta,\gamma\in G$ で $\gamma$ が $\alpha,\beta$ と可換とする。$h,h_0:F_2\to G$ を $h(x)=\gamma^{a}\alpha,\ h(y)=\gamma^{b}\beta$、$h_0(x)=\alpha,\ h_0(y)=\beta$ で定めると、$\langle\alpha,\beta,\gamma\rangle$ の中で $\gamma$ は中心的ゆえ、任意の $w\in F_2$ について
> $$h(w)=\gamma^{\,a\,\varepsilon_1(w)+b\,\varepsilon_2(w)}\;h_0(w)\qquad(\varepsilon_1,\varepsilon_2=x,y\ \text{の指数和}).$$
> とくに $w\in[F_2,F_2]$ では $\varepsilon_1(w)=\varepsilon_2(w)=0$ ゆえ $h(w)=h_0(w)$。∎
> (★ v1.1 の「$\gamma^0$」表記を $\gamma^{\varepsilon_1(f)+\varepsilon_2(f)}$ の形へ精密化した。$a,b\in\{0,\pm1\}$ の 3 通りが §3.2.2 の段 A/B/C に対応する。)

#### 3.2.2 ★★ 定理 **PENT-FORM**(条件つき同値)

記号: $f_1:=f(x_{12},x_{23})$, $f_2:=f(x_{45},x_{51})$, $f_3:=f(x_{23},x_{34})$, $f_4:=f(x_{51},x_{12})$, $f_5:=f(x_{34},x_{45})$。工房の $\mathrm{PENT}_W$ の欠陥写像は $D=\bar\rho^4(jf)\bar\rho^3(jf)\bar\rho^2(jf)\bar\rho(jf)\,jf=f_5f_4f_3f_2f_1$(翻訳ノート §1.2 の $\rho(x_{ij})=x_{i+3,j+3}$ 規約)。

(A.18) で (2.20) を展開すると
$$\underbrace{f(x_{23},x_{34})}_{\varphi_{234}}\cdot\underbrace{f(x_{12}x_{13},x_{24}x_{34})}_{\varphi_{1,23,4}}\cdot\underbrace{f(x_{12},x_{23})}_{\varphi_{123}}\;=\;\underbrace{f(x_{12},x_{23}x_{24})}_{\varphi_{1,2,34}}\cdot\underbrace{f(x_{13}x_{23},x_{34})}_{\varphi_{12,3,4}} .$$

> ### 定理 PENT-FORM
> $f\in[F_2,F_2]$ とする。$K(0,5)$(および任意の商)の中で、**(I) $f(a,b)f(b,a)=1$ が代入対 $(x_{45},x_{34})$ と $(x_{12},x_{15})$ で成立する**ならば
> $$\boxed{\ (2.20)\ \Longleftrightarrow\ f_5f_4f_3f_2f_1=1\ =\ \mathrm{PENT}_W .\ }$$
> **証明.** 補題 **SPH** から次の 3 つの可換性が出る: $x_{45}=\varphi_{123}(c)$ は $Z(PB_3)$ の像ゆえ $x_{12},x_{13},x_{23}$ と可換 / $x_{15}=\varphi_{234}(c)$ は $x_{23},x_{24},x_{34}$ と可換 / $[x_{12},x_{34}]=1$((A.3)・添字が交わらない)。
> **段 A**($\gamma=x_{12}^{-1}$、$a=-1,b=0$): $x_{45}=x_{12}(x_{13}x_{23})$ より $x_{13}x_{23}=x_{12}^{-1}x_{45}$。補題 **ABS** で $f(x_{13}x_{23},x_{34})=f(x_{45},x_{34})$、(I) で $=f(x_{34},x_{45})^{-1}=f_5^{-1}$。
> **段 B**($\gamma=x_{34}^{-1}$、$a=0,b=-1$): $x_{15}=(x_{23}x_{24})x_{34}$ と $[x_{34},x_{15}]=1$ より $x_{23}x_{24}=x_{34}^{-1}x_{15}$。**ABS** で $f(x_{12},x_{23}x_{24})=f(x_{12},x_{15})$、(I) で $=f(x_{15},x_{12})^{-1}=f_4^{-1}$($x_{51}=x_{15}$)。
> **段 C**($\gamma=x_{23}^{-1}$、$a=b=-1$。★ **(I) を使わない**): $x_{12}x_{13}=x_{23}^{-1}x_{45}$、$x_{24}x_{34}=x_{23}^{-1}x_{15}$(いずれも SPH と可換性)。**両スロットに同じ $\gamma$** が出るので **ABS** で $f(x_{12}x_{13},x_{24}x_{34})=\gamma^{\varepsilon_1(f)+\varepsilon_2(f)}f(x_{45},x_{15})=f(x_{45},x_{51})=f_2$。
> **合成**: $f_3f_2f_1=f_4^{-1}f_5^{-1}\iff f_5f_4f_3f_2f_1=1$。各段は等式による置換ゆえ**両向き**。∎
>
> ★ **使用材料の会計**: 球面関係 **4 回**(段 A で $x_{45}$・段 B で $x_{15}$・段 C で両方)/ 中心元吸収 **3 回**(段 A/B/C)/ **(I) 2 回**(段 A/B)。**(II)(hexagon 第 2 本)は一度も使わない。**

#### 3.2.3 ★★ 定理 **PENT-FORM′**(**無条件形** — v1.2 新)

> ### 定理 PENT-FORM′
> **全ての $f\in[F_2,F_2]$** について((I) を仮定せず)、$K(0,5)$ および任意の商の中で
> $$\boxed{\ (2.20)\ \Longleftrightarrow\ \tilde D(f):=f(x_{45},x_{34})^{-1}\,f(x_{12},x_{15})^{-1}\,f(x_{23},x_{34})\,f(x_{45},x_{51})\,f(x_{12},x_{23})=1 .\ }$$
> **証明.** 定理 PENT-FORM の証明から (I) の適用を落とすと、段 A は $f(x_{13}x_{23},x_{34})=f(x_{45},x_{34})$ まで、段 B は $f(x_{12},x_{23}x_{24})=f(x_{12},x_{15})$ まで、段 C はそのまま $=f_2$。(2.20) に代入して
> $$f_3f_2f_1=f(x_{12},x_{15})\,f(x_{45},x_{34})\iff \tilde D(f)=1 .\qquad\blacksquare$$
>
> ### ★ 系(2 つの形の関係)
> $\tilde D$ は $D=f_5f_4f_3f_2f_1$ の**第 1・第 2 因子だけを「(I) 未使用版」に置き換えたもの**である:
> $$f_5=f(x_{34},x_{45})\ \longleftrightarrow\ f(x_{45},x_{34})^{-1},\qquad f_4=f(x_{51},x_{12})\ \longleftrightarrow\ f(x_{12},x_{15})^{-1} .$$
> (I) はまさにこの 2 つの一致を主張する。ゆえに **$\bar f\in S_1$(= (3.10) 充足域)では $\tilde D=D$**、すなわち PENT-FORM′ ⟹ PENT-FORM。
>
> ### ★★ 実装上の含意(**工程 P3 の全層がバグ検出器になる**)
> $\tilde D$ の 5 個の引数対 $(x_{45},x_{34}),(x_{12},x_{15}),(x_{23},x_{34}),(x_{45},x_{51}),(x_{12},x_{23})$ は**すべて $K(0,5)$ の 5 本の隣接生成元 $x_{12},x_{23},x_{34},x_{45},x_{51}$ で書けている**($x_{15}=x_{51}$)。⟹ **$\mathrm{PENT}_W$ を計算する既存の装置($Q$ 上の $\bar\rho$ 実装)に、引数対を 2 箇所だけ差し替えた第 2 の述語を足すだけ**で $\tilde D$ が計算できる。実装コストはほぼゼロ。

#### 3.2.4 ★ 系 **PENT-EQ**(層つき)と、残る依存の会計

$$\boxed{\ \bar f\in S_0=[P,P]\ \Longrightarrow\ \bigl[(2.20)\bmod\tilde{\mathbf N}^*\iff\tilde D(\bar f)=1\ \text{in}\ Q\bigr]\quad(\textbf{無条件}) }$$
$$\boxed{\ \bar f\in S_1=\{(3.10)\ \text{充足}\}\ \Longrightarrow\ \bigl[(2.20)\bmod\tilde{\mathbf N}^*\iff\mathrm{PENT}_W\bigr] }$$
(B4-DIR (c) で (2.20) mod $\tilde{\mathbf N}^*$ $\iff$ $Q$ での像、そこに PENT-FORM′ / PENT-FORM を適用。$S_1$ への降下は **VERBAL-DESCENT**: $f\theta(f)\in\mathcal V(F_2)$ ⟹ 任意の代入対で $\mathcal V(Q)=1$ に落ちる。)

> ### ★ 【GAP-B4-1】の状態(**v1.2 で格上げ**)
> **v1.1**: 「紙で閉鎖・ただし**文献相対**(LS-(4) と LS-(abs) を pin 経由で引用)」。
> **v1.2**: **LS-(4) は補題 SPH で自前導出・LS-(abs) は補題 ABS で自前証明** ⟹ **文献相対は解消**。
> $$\boxed{\ \textbf{新しい格 = 「正典 (A.2)(A.3)(A.5)(A.18)(2.20) + }\Delta_4^2\ \textbf{積表示(機械検算)+ }K(0,5)\ \textbf{の Hurwitz 表示」相対}\ }$$
> ★ **残る依存 $K(0,5)$ の Hurwitz 表示は、本ノートの新規依存ではない**: 比較対象である $\mathrm{PENT}_W$ 自身が $K(0,5)$ の生成元 $x_{i,i+1}$ と $\rho$ の上で定義されている(翻訳ノート §1.0/§1.2)。すなわち **Hurwitz 表示は「定理の仮定」ではなく「比較する述語の定義」の一部**である。残余は【GAP-B4-1″】として §9.2 に narrow に立てる。

### 3.3 ★ 委嘱②への直接回答(その 2 — 論理関係の最終形)

| 主張 | 状態(v1.2) |
|---|---|
| genuine ⟹ (2.20) mod $\tilde{\mathbf N}$(任意の窓) | **定理**(2008 の公理)。**HS Prop 7 の翻訳を一切要しない** |
| genuine ⟹ $\mathrm{PENT}_W$ | 既在(HSP-SOUND) |
| **全 $\bar f\in[P,P]$** で (2.20) mod $\tilde{\mathbf N}^*$ $\iff$ $\tilde D=1$ | ★ **定理 PENT-FORM′**(**無条件**) |
| $\bar f\in S_1$ で (2.20) mod $\tilde{\mathbf N}^*$ $\iff$ $\mathrm{PENT}_W$ | ★ **定理 PENT-FORM**((3.10) 相対) |
| $\mathrm{PENT}_W$-FAIL ⟹ (2.20) mod $\tilde{\mathbf N}_{\rm core}$ FAIL | ★ **偽**(反例 = 252 全件) |

### 3.4 判定機の形

$R:=PB_4/\tilde{\mathbf N}^*$($7^{41}$・pc 群)で各余面は $\bar\varphi_\bullet:P\to R$ に降り、
$$D_{B_4}(\bar f)=\bigl(\bar\varphi_{1,2,34}(\bar f)\bar\varphi_{12,3,4}(\bar f)\bigr)^{-1}\bar\varphi_{234}(\bar f)\bar\varphi_{1,23,4}(\bar f)\bar\varphi_{123}(\bar f),\qquad (2.20)\iff D_{B_4}=1 .$$
生成元上の値は (A.18)($\bar\varphi_{123}:x\mapsto x_{12},y\mapsto x_{23}$ / $\bar\varphi_{234}:x_{23},x_{34}$ / $\bar\varphi_{12,3,4}:x_{13}x_{23},x_{34}$ / $\bar\varphi_{1,23,4}:x_{12}x_{13},x_{24}x_{34}$ / $\bar\varphi_{1,2,34}:x_{12},x_{23}x_{24}$)。★ **$m$ 非依存** ⟹ 117,649 件。

### 3.5 hexagon 側は新情報ゼロ(定理として)

$\tilde{\mathbf N}^*_{PB_3}=\mathbf N_0$、$\mathbf N_0\cap F_2=\mathbf N\cap F_2=\mathcal V(F_2)$、**2401 Prop 3.4** ⟹ hexagon mod $\tilde{\mathbf N}^*_{PB_3}$ $\iff$ hexagon mod $\mathbf N$。独立確認 = **補題 B4-KAPPA**($\kappa(d_1)=\kappa(d_2)=0$)。⟹ **B₄ 裁定の実体は pentagon 1 本に完全に縮約される。**

### 3.6 ★ 系 **B4-42**(v1.2 で前件を 1 つ削除)

> ### ★ 補題 CHARM⟹PRACT(**原文逐語**・v1.2 新)
> 2008 **Def 2.19**(p.25・頁画像で直接確認)の charming 第 1 条件は「the coset $f\mathsf N_{PB_3}$ can be represented by $f_1\in[F_2,F_2]$」であり、**Remark 2.15**(p.23・同)の practical は「representable by pairs $(m,f)$ with $f\in F_2\le PB_3$」である。$[F_2,F_2]\subseteq F_2$ ゆえ
> $$\boxed{\ \textbf{charming}\ \Longrightarrow\ \textbf{practical}. \ }$$
> ★ 原論文も **§4 冒頭(p.39・頁画像で直接確認)で逐語**「Clearly, every charming GT-shadow is practical.」と述べている。
> ⟹ **$\mathrm{GT}^\heartsuit(N)$ に practical の但し書きは不要。** p.23 末の未解決(「$\mathbb Z\times F_2$ で代表できない onto 射の存否」)は **non-charming な shadow についての問い**であり、本ノートの主張には一切入らない。

> ### 系 B4-42
> 前件 **(H1)** 系 PENT-EQ が層 $S_2$(full hexagon $\subseteq S_1$)で適用できること(**紙で閉じた**)、**(H2)** 本走の測定値(294 / 42)、**(H3)** BH-α-pent v1.1($\mathfrak G_{\rm ar}=42$)、**(H5)** SURJ 自動 の下で
> $$\boxed{\ \mathrm{GT}^\heartsuit_{2008}(\tilde{\mathbf N}^*)\ \textbf{はちょうど 42 元からなり、その全元が genuine である。}\ }$$
> **証明.** GT-shadow = GT-pair ∧($T^{PB_3},T^{PB_2}$ 全射)。$T^{PB_2}$ 全射 $\iff m\in\mathcal X$。$T^{PB_3}$ 全射: $PB_3/\mathbf N_0\cong P\times C_7$ で $\Phi=[P,P]\times1$、像が $x^u,{}^f\!y^u,c^u$($\gcd(u,7)=1$)を含む ⟹ Frattini(H8′ の直接拡張)= (H5)。hexagon は §3.5 で $\mathbf N$ と同一、pentagon は $S_2$ 上で $\mathrm{PENT}_W$ と同一(H1)。⟹ $\mathfrak G_{\rm pent}$ と一致、(H2)(H3) より 42 元 $=\mathfrak G_{\rm ar}$。arithmetic ⟹ genuine。**charming ⟹ practical(補題 CHARM⟹PRACT)ゆえ practical の但し書きは不要**。∎
> ★ **v1.1 の前件 (H4)(practical 制限)は削除された。**

意味: ① **Question 4.7** が求める型の実例(novelty 検査は司令塔ゲート)② この窓は Q4.6 の例を**与えない**(★ 別の窓 $\tilde{\mathbf N}_{\rm core}$ は与える — 別票)③ 窓の大きさは $\lvert F_2:\tilde{\mathbf N}^*_{F_2}\rvert=7^8$ で語る(防壁 R6)。

---

## 4. 委嘱③ — genuine の正式判定(v1.1 から不変)

**4.1** Cor 3.13 の survival 減少列は**必ず停止**するが**停止点の有効上界がない**【GAP-B4-3】。陰性は 1 窓で有限、陽性は切り詰めから出ない。
**4.2 サンドイッチ**: $\mathfrak G_{\rm ar}\subseteq\mathfrak G_{\rm genuine}\subseteq\mathrm{GT}^\heartsuit(N)$ で**両端の濃度が一致すれば切り詰め誤差ゼロ**。打ち切るのではなく下から挟む。
**4.3 管轄**: B₄ の極限は $\widehat{GT}$、内訳が問うのは $\widehat{GT}_{gen}$(2401 Def 4.2 / Cor 5.4)⟹ **B₄ は 252 の「死因」を厳密化する法廷であって「内訳」を裁く法廷ではない。**
**4.4 命題 BIT-252**: $\mathbf N$ isolated ゆえ $\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N)$ は群準同型、**2401 Def 4.2** より $\mathfrak G^{\rm gentle}_{\rm genuine}=$ その像 ⟹ 部分群(1 行)。$\mathfrak G_{\rm ar}$ を含み $[\mathrm{GT}(\mathbf N):\mathfrak G_{\rm ar}]=7$ 素数 ⟹ $\{42,294\}$、中間なし。系: ビット $=294$ なら **$\widehat{GT}\to\widehat{GT}_{gen}$ は全射でない**(単射性は UNKNOWN ゆえ非全射形で書く)。
**4.5 決定実験**: $K=\mathcal V_5(F_2)\times\langle c\rangle$、252 から 1 元、fiber 117,649 件、$m$ 固定、charming/SURJ 自動、**必要な前件は「$\mathbf N$ が isolated」だけ**。全滅 ⟹ **252 全件 gentle-fake**。数分。**本ノートは実行しない。**
**4.6** 系 B4-42 の下では B₄ 塔は $\tilde{\mathbf N}^*$ で閉じる(より深く降りても 1 元も減らない)。

---

## 5. 委嘱④ — 計算量

### 5.1 位数見積り

| 対象 | 位数 | 表現 |
|---|---|---|
| $P$ | $7^8$ | pc 群(既在) |
| $[P,P]$ | $7^6=117{,}649$ | **判定の宇宙**($m$ 非依存) |
| $R=PB_4/\mathcal V(PB_4)$ | $7^{41}$ | pc 群(41 生成)**※ §5.4 のブロッカー** |
| $Q=K(0,5)/W$ | $7^{40}$ | pc 群(既在)。$R\cong C_7\times Q$ |
| $PB_4/\tilde{\mathbf N}_{\rm core}$ | $7^{8}\le\cdot\le7^{29}$ | $P^4$ の部分群($\mathbb F_7$-階数 5) |

### 5.2 コスト

$D_{B_4}$ = 準同型像 5 回 + 積 4 回 ⟹ $117{,}649\times9\approx10^6$ collection ≒ **数分**。$\tilde D$ は $Q$ 上で既存 $\mathrm{PENT}_W$ 装置の引数対を 2 箇所差し替えるだけ ⟹ **追加コストほぼゼロ**。メモリ $O(41^2)$ ⟹ 8GB 無関係。GHA 可。

### 5.3 費用対効果

| 作業 | コスト | 得られる情報 |
|---|---|---|
| $\tilde{\mathbf N}^*$ での (2.20) 評価(P2/P3) | 数分(**+ P1 ブロッカー解除**) | 定理 PENT-FORM′/PENT-FORM の 2 実装確認(**全層がバグ検出器**) |
| $\tilde{\mathbf N}_{\rm core}$ での (2.20) 評価(**P1 不要**) | 数分 | B4-VAC 実測 + Question 4.6 の標的(別票) |
| CAL-B4 較正 | 秒〜時間 | 判定機の免許(必須先行) |
| BIT-252 決定実験(B₃ 側) | 数分 | 252 の内訳が 42 側なら CLOSED |

### 5.4 ★ 実装仕様の訂正と環境ブロッカー

> **仕様**: `Pq(F : Prime:=7, ClassBound:=4, Exponent:=7)`。**`Exponent:=7` を落とすと違う群になる**(`ClassBound` は下方指数-$p$ 中心列 $P_{i+1}=[P_i,G]P_i^{\,p}$ に沿う切り詰めで $\gamma_{c+1}G^{p}$ ではない。反例 $G=\mathbb Z$: $P_3=49\mathbb Z$ vs $7\mathbb Z$。機械確認: `PQuotient(F2,7,2)` $=7^5$ vs $\lvert F_2:\gamma_3F_2^{7}\rvert=7^3$)。誤ると **B4-EXQ-1 が偽 STOP**。
> **★ 環境ブロッカー**: 本機の ANUPQ は外部バイナリ `pq` が動作しない(**`LoadPackage` は `true` を返す**が `Pq(...)` は `iostream dead` で即死)。⟹ **工程 P1 は保留**。代替路: 指数 7・類 4 では $P_i=\gamma_i$ ゆえ `PQuotient(PB_4,7,4)` で $\bar G$ を作り $R=\bar G/(\gamma_5(\bar G)\mathrm{Agemo}_1(\bar G))$。中間商の見積り =【工程要請 W-1】。
> ★ **迂回**: $\tilde{\mathbf N}_{\rm core}$ 側($P^4$ の中)と $\tilde D$ 側($Q$ の中)は **$R$ を要さない**。

---

## 6. 委嘱⑤ — 較正設計(CAL-B4)

### 6.1 正解データ(2008 §4.3・p.39/p.42–43)

**N⁽¹⁹⁾**($N_{\rm ord}=6$): **$F_2/N_{F_2}$ 全体(7776)の中で** pentagon 充足 **216**、うち hexagon へ持ち上がるのは **36**。**N⁽³⁴⁾**($N_{\rm ord}=9$): **交換子部分群(254,016)の中で** pentagon 充足 **4096**、hexagon 持ち上げ **243**。

### 6.2 較正ゲート

| # | 項目 | 期待値 |
|---|---|---|
| C-1 | $\lvert PB_4:N^{(19)}\rvert$($\psi:PB_4\to S_9$・(4.3)) | **216** |
| C-2 | (2.4) と Prop 2.3 | $N_{\rm ord}=$ **6** |
| C-3 | $\lvert F_2:N_{F_2}\rvert$ / 交換子 | **7776** / **216** |
| C-4 ★ | 全 7776 元で (2.20) | **216 件** |
| C-5 ★ | C-4 × $m\in\{0,2,3,5\}$ で hexagon | **36 件** |
| C-6 | $\lvert\mathrm{GT}\rvert$(**practical 版**)/ $\lvert\mathrm{GT}^\heartsuit\rvert$ | **72** / **12**($\cong D_6$) |
| C-7(任意) | N⁽³⁴⁾ | **4096** → **243** |
| C-8 ★ | Package GT `PaB.py::penta` と第三者突合 | 全一致 |
| C-9 ★ | $\tilde{\mathbf N}_{\rm core}$ での (2.20) 通過数 | **117,649** — **停止規則として運用** |
| **C-10** ★新 | $Q$ 上で $\tilde D$ と $D$ を全 117,649 件に評価し、**$S_1$ 上で解集合が一致・$S_0\setminus S_1$ では一般に不一致**であること | $S_1$ 一致 | 

**CAL-B4 が全 PASS するまで NW(7) の B₄ 数値を 1 つも信用しない。**

---

## 7. 委嘱⑥ — 用語版差の防壁

### 7.1 対応表と CHARM-EQ

2008 と 2401 で **GT-shadow は同名別物**(2008 = GT-pair+全射 / 2401 = charming GT-pair+全射)。**genuine も別概念**($\widehat{GT}$ 由来 / $\widehat{GT}_{gen}$ 由来)。★ **補題 CHARM-EQ**: NW(7) の宇宙では 2401-charming $\iff$ 2008-charming ⟹ **版差は pentagon の 1 ビットに封じ込められる**。

### 7.2 LS 系との版差

| 項目 | LS1994 | LS-Ptolemy | HS2000 | 工房 |
|---|---|---|---|---|
| (I) の引数順 | $f(x,y)f(y,x)=1$ | $f(y,x)f(x,y)=1$ | $f(y,x)f(x,y)=1$ | (3.10) |
| (III) の形 | 2 項 = 3 項($\hat K_4$) | 5 項積 $=1$ | 5 項積(巡回シフト差) | (2.20) = LS1994 (III) の左右入替 |
| 回転元 | $V(x_{ij})=x_{i+2,j+2}$ | $(\alpha\beta)^5=1$ | $\rho(x_{ij})=x_{i+3,j+3}$ | $\bar\rho$(HS 規約) |

### 7.3 防壁 **R1–R8**

| # | 規約 |
|---|---|
| **R1** | cert に **framework tag**(`FW=B4-2008` / `FW=B3-2401`)必須 |
| **R2** | cert に **window arity**(3/4)と**評価した方程式 ID**(`pent2.20` / `PENT_W` / **`Dtilde`**)を必須 |
| **R3** | 「genuine」は必ず添字つき |
| **R4** ★改 | 異 framework の計数を突き合わせない。★ **Table 1 の `|GT|` 列は practical 限定の計数**(p.39 逐語)であり、`|GT♡|` は**限定不要**(補題 CHARM⟹PRACT)。この非対称を混ぜない |
| **R5** | $\tilde{\mathbf N}$ と $\mathbf N$ は別記号。関係は §2.6 の表が唯一の正本 |
| **R6** | 窓の「大きさ」を $\lvert PB_4:\tilde{\mathbf N}\rvert$ で語らない(律速量は $\lvert F_2:\tilde{\mathbf N}_{F_2}\rvert$) |
| **R7** | LS1994 の $V$ と工房の $\rho$ は**逆回転**。指数を論文間で直接写さない |
| **R8** ★新 | **$x_{ij}=x_{ji}$ は対称規約**($\sigma_{ij}^2=x_{ij}$・LS1994 命題 1)。$x_{51}$ と $x_{15}$ は**同一元**。$\bar\rho$ の実装で添字を「$i<j$ に正規化」する段を落とすと $\rho^3,\rho^4$ の項がずれる(**罠 D-6/D-7**)。⟹ 規約台帳への 1 行を起草(`docs/notes/conventions_ledger_addendum_xij_symmetry_draft.md`) |

---

## 8. 工程表

| 工程 | 内容 | 前件 | コスト | 状態 |
|---|---|---|---|---|
| **P0** | CAL-B4(C-1〜C-6, C-8) | なし | 秒〜分 | 実行可 |
| **P0b** | C-7(N⁽³⁴⁾) | P0 | 分〜時間 | 実行可 |
| **P0c** ★新 | **C-10**($Q$ 上で $\tilde D$ vs $D$) | P0 | 分 | ★ **P1 不要・即実行可** |
| **P1** | $R$ の構築(`Exponent:=7`) | P0 | 分 | ⚠ **保留**(ANUPQ ブロッカー・【工程要請 W-1】) |
| **P2** | 5 本の $\bar\varphi:P\to R$ + 117,649 件で $D_{B_4}$ | P1 | 数分 | P1 待ち |
| **P3** ★改 | **層別突合**(§8.1) | P2 + lane P cert + P0c | — | P1 待ち |
| **P4** | C-9($\tilde{\mathbf N}_{\rm core}$ で全通過) | P0 | 分 | ★ **P1 不要・即実行可** |
| **P5** | (B₃ 側)BIT-252 決定実験 | prereg + 裁定 | 数分 | prereg 待ち |
| **P6** | (別票)Question 4.6 prereg | Sol 認可(便 112 後) | 分 | **走らせない** |

### 8.1 ★ 工程 P3 の層別設計(**v1.2 で $S_0$ にも予言がついた**)

| 層 | 定義 | 事前予言 | 不一致時 |
|---|---|---|---|
| **$S_0$** ★改 | $[P,P]$ 全件(117,649) | ★ **(2.20)-PASS 集合 $=\ker\tilde D$**(**定理 PENT-FORM′・無条件**) | **IMPLEMENTATION_BUG / STOP** |
| **$S_1$** | (3.10) 充足域 | ★ **(2.20)-PASS 集合 $=$ $\mathrm{PENT}_W$-PASS 集合**(定理 PENT-FORM) | 同上 |
| **$S_2$** | full hexagon($\subseteq S_1$・$m$ を伴う) | ★ shadow 単位で **42** | 同上 |

★ **v1.1 との差**: v1.1 は「$S_0$ の不一致は STOP にしない(予言しない)」としていたが、**PENT-FORM′ により $S_0$ にも格 T の予言がつく** ⟹ **117,649 件すべてがバグ検出器**になった。$S_0$ で $\mathrm{PENT}_W$ と比較してはならない(比較相手は $\tilde D$)という点だけ注意。

### 8.2 事前登録する予言(IF-FIRST)

| ID | 予言 | 格 | 分岐 |
|---|---|---|---|
| **B4-EXQ-1** | $\lvert R\rvert=7^{41}$(`Exponent:=7` 付き仕様で) | **T\*** | 不一致 ⟹ **まず実装仕様を疑う** |
| **B4-EXQ-2** | $R\cong C_7\times Q$、$\lvert Q\rvert=7^{40}$ | **T\*** | 同上 |
| **B4-EXQ-3** | $\tilde{\mathbf N}^*_{PB_3}=\mathbf N_0$ | **T** | バグ検出器 |
| **B4-EXQ-4** | **$S_2$ 上で shadow 単位 42、$S_1$ 上で $\bar f$ 集合として完全一致** | **T** | 不一致 ⟹ 実装/規約の誤り(**新発見と読まない**) |
| **B4-EXQ-4′** ★新 | **$S_0$(全 117,649)で (2.20)-PASS 集合 $=\ker\tilde D$** | **T**(PENT-FORM′) | 不一致 ⟹ **IMPLEMENTATION_BUG / STOP** |
| **B4-EXQ-5** | CAL-B4: 216/36・4096/243 | **T** | 不一致 ⟹ STOP |
| **B4-EXQ-6** | $\tilde{\mathbf N}_{\rm core}$ で (2.20) 通過 $=117{,}649$ | **T**(B4-VAC) | 不一致 ⟹ STOP |
| **B4-EXQ-7** | BIT-252: $\{42,294\}$ | **T\*** | 中間値 ⟹ STOP |
| **B4-EXQ-8** | $\lvert PB_4:\tilde{\mathbf N}_{\rm core}\rvert\in[7^8,7^{29}]$ かつ $\Delta^2$ の像 $=1$ | **T\*** | 範囲外 ⟹ STOP |
| **B4-EXQ-9** ★新 | $\Delta_4^2=c\,(x_{14}x_{24}x_{34})$ と $[x_{14},x_{23}]=1$(忠実 Artin 表現での語同一性) | **T**(付録 A.5 で**既に検算済**) | 不一致 ⟹ 実装 STOP |

★ **格 T の予言は的中しても情報量ゼロ。バグ検出器としてのみ運用する。**

---

## 9. 格付け・【GAP】・規律申告

### 9.1 読んだ範囲の申告 ★改

- `papers/txt/2008.00066-*.txt`: L2563–2610 / L2638–2660 / L1820–1845(Remark 2.15)/ L2005–2035(Def 2.19)/ L3038–3050(§4 冒頭)/ L3516–3546 / L3548–3581 / Table 1 数値ブロック。
- ★ **原文 PDF の頁画像を本起草者が直接開いた**: `papers/dolgushev-2008.00066-gt-shadows-original.pdf` **p.23**(Prop 2.14・Remark 2.15・(2.54)(2.55))/ **p.25**(Prop 2.18・**Def 2.19**・(2.58)–(2.61))/ **p.39**(§4 冒頭「**Clearly, every charming GT-shadow is practical.**」・(4.2)(4.3)・Remark 4.1・N⁽¹⁹⁾ の $D_6$)。**v1/v1.1 では 1 枚も開いていなかった** — v1.2 で解消。
- **LS1994 / LS-Ptolemy / HS2000 の原文は 1 頁も開いていない。** v1.2 は**これらへの数学的依存を持たない**(補題 SPH/ABS で自前化)。pin ノートは §7.2 の版差台帳の出所としてのみ引く。
- 外部文献の自主検索は**ゼロ**。

### 9.2 【GAP】一覧 ★改

| 札 | 内容 | 状態 |
|---|---|---|
| **【GAP-B4-1】** | (2.20) と $\mathrm{PENT}_W$ の項対応 | ★★ **CLOSED**(定理 PENT-FORM′/PENT-FORM)。**格は「正典 + $\Delta^2$ + Hurwitz 相対」**(文献相対を脱した) |
| ~~【GAP-B4-1′】~~ | ~~LS-(4)/LS-(abs) の文献相対~~ | ★ **CLOSED**(補題 SPH / 補題 ABS で自前化) |
| ★ **【GAP-B4-1″】**(新・narrow) | $K(0,5)$ の **Hurwitz 表示**($x_{i5}$ の定義関係)の出所 | **定義相対**。★ **$\mathrm{PENT}_W$ 自身がこの表示の上で定義されている**ので、本定理の**追加の**仮定ではない(§3.2.4)。閉じるなら「工房の $K(0,5)$ 定義を正典化する」1 行で足りる |
| ~~【GAP-B4-2】~~ | ~~practical 制限~~ | ★ **削除**(補題 CHARM⟹PRACT。原文 p.23/p.25/p.39 を頁画像で直接確認)。p.23 末の未解決は **non-charming shadow** についての問いであり本ノートの主張に入らない |
| **【GAP-B4-3】** | Cor 3.13 の停止点に有効上界なし | **UNKNOWN**。【文献要請 B4-L2】 |
| **【GAP-B4-4】** | 突合に要する $[P,P]$ の共通ラベル付け(CV-9 危険)。$S_1/S_2$ の定義も両実装で一致が要る | **処方**: 同値試験は同一プロセス・同一列挙で。発見用の数値は lane P cert を正本、P3 は**仕様同一性試験**。falsifier の CV-9 判読を必須前件。**単位欄・述語 ID 欄($\tilde D$ か $D$ か)を cert に追加** |
| ~~【GAP-B4-5】~~ | BIT-252 の前件 | ★ **CLOSED** |
| **【工程要請 W-1】** | ANUPQ 代替路の中間商 $\bar G$ の位数見積り | **未見積り**。ep-keeper / implementer へ |

### 9.3 【文献要請】

> **【文献要請 B4-L1′】は取り下げる**(補題 SPH/ABS の自前導出により不要になった)。
> **【文献要請 B4-L2】(継続・非緊急)**: Cor 3.13 の survival 減少列の**停止点の有効上界**。無いなら「無い」で確定させたい。

### 9.4 格付け ★改

| 対象 | 格 |
|---|---|
| 補題 **B4-FORGET** / **CORE-4** / **B4-IND** / **B4-MONO** / **B4-DIR** / **CHARM-EQ** | **paper-proof**(CORE-4 は検分ノート由来・本ノートは採録) |
| ★ 定理 **B4-VAC** / **B4-CANON** | **paper-proof**(**別人格の独立再導出で PASS**)。**Sol 未監査** |
| ★ 補題 **SPH** | **paper-proof**(正典 + **忠実 Artin 表現での機械検算**(付録 A.5)+ Hurwitz 表示) |
| ★ 補題 **ABS** | **paper-proof**(3 行・外部入力ゼロ) |
| ★★ 定理 **PENT-FORM′**(無条件) | ★ **paper-proof**(SPH + ABS + (A.18)。**相互検分 PASS** の条件つき形の一般化) |
| ★★ 定理 **PENT-FORM** / 系 **PENT-EQ** | ★ **paper-proof**(★ **相互検分 PASS**)。**Sol 未監査** |
| ★ 補題 **CHARM⟹PRACT** | ★ **paper-proof**(原文 p.23/p.25/p.39 を**本起草者が頁画像で直接確認**) |
| 補題 **B4-KAPPA** | **paper-proof candidate**(`cross-checked` は付さない) |
| ★ 系 **B4-42** | **conditional candidate**((H1)(H2)(H3)(H5) 相対・とくに BH-α-pent 相対) |
| ★ 命題 **BIT-252** | ★ **paper-proof**(測定相対は継承)。**別人格の独立再導出で 4 段 PASS** |
| `verified` | ✗(Lean 未使用) |
| `cross-checked` | ✗(CV-9 判読未実施) |
| **novelty** | ★ **主張しない**(先行の有無は未調査。司令塔の novelty ゲートを先に通すこと) |

### 9.5 規律申告

- ★ **本走宇宙(705,894 対)の候補を 1 件も評価していない。** GAP も pc 群も起動していない。機械は付録 A の python のみ(記号語計算・整数級数・$\mathbb F_7$ 線型代数・**自由群 $F_4$ の語同一性**)。
- **封印 3 量非接触。既在文書を 1 バイトも改変していない**(v1・v1.1・検分ノート・pin ノート・事前登録票 v1 すべて read-only)。
- ★ **HS2000 Prop 7 を使用していない**(罠 D-5)。
- **新しい停止規則を発効させない**(§6.2・§8.1・§8.2 は提案)。

---

## 10. Sol への監査点(5 点)

> **Q-1 ★★ 補題 CORE-4**。$\mathrm{core}_{B_4}(p_4^{-1}(N))=\bigcap_ip_i^{-1}(N)$ を代表元 4 つ × 6 生成元の厳密一致で示した一段。

> **Q-2 ★★ 定理 B4-CANON (2) の厳密等号**。$\varphi_{123}$ 1 本が分裂単射なら残り 4 本を見なくてよい、という論法の可否。

> **Q-3 ★★★ 補題 SPH と 定理 PENT-FORM′**。$\Delta_4^2=c\,(x_{14}x_{24}x_{34})$(忠実 Artin 表現で機械検算)+ 基点 4/1 の Hurwitz + $\Delta_4^2=1$ から $x_{45}=\varphi_{123}(c)$, $x_{15}=\varphi_{234}(c)$ を出し、**LS1994 への数学的依存をゼロにした**一段。および**無条件形 PENT-FORM′**((I) を使わない $\tilde D$)が、$S_0$ 全層の予言として登録に足るか。

> **Q-4 ★★ 系 PENT-EQ の層設計**。$S_0$ は $\tilde D$ と、$S_1/S_2$ は $\mathrm{PENT}_W$ と比較する三層突合を認めるか。登録層は $S_1$ と $S_2$ のどちらを正とすべきか。

> **Q-5 ★★ 補題 CHARM⟹PRACT による前件削除**。Def 2.19 の第 1 条件($f_1\in[F_2,F_2]$ 代表)が Remark 2.15 の practical($f\in F_2$)を含意するので **$\mathrm{GT}^\heartsuit$ に practical の但し書きは不要**、という読み(原論文 p.39 も逐語で同じことを述べる)。⟹ **【GAP-B4-2】削除**を認めるか。

---

## 11. ★ v1.1 → v1.2 差分表(全件)

| # | 箇所 | 種別 | 内容 | 出所 |
|---|---|---|---|---|
| 1 | §3.2.1 | ★ **新補題 SPH** | 球面関係 $x_{45}=c$, $x_{15}=\varphi_{234}(c)$ を $\Delta^2$ 積表示 + Hurwitz + $\Delta^2$ 中心性から**自前導出**。$\Delta^2$ 積表示は忠実 Artin 表現で機械検算(付録 A.5) | 指示 ① |
| 2 | §3.2.1 | ★ **新補題 ABS** | 中心元吸収を自前証明。$\gamma$ の指数を $\gamma^{a\varepsilon_1(w)+b\varepsilon_2(w)}$ と明示(**v1.1 の $\gamma^0$ 表記を修正**) | 指示 ①⑦ |
| 3 | §3.2.4 / §9.2 | ★ **格上げ** | 定理 PENT-FORM の格が **「文献相対」→「正典 + $\Delta^2$ + Hurwitz 相対」**。【GAP-B4-1′】CLOSED・narrow な【GAP-B4-1″】へ | 指示 ① |
| 4 | §3.2.3 / §8.1 / §8.2 | ★★ **新定理 PENT-FORM′** | **無条件形**: 全 $f\in[F_2,F_2]$ で (2.20) $\iff\tilde D=1$。⟹ **$S_0$ 層 117,649 件全部に格 T の予言**(B4-EXQ-4′)・$S_0$ も STOP 対象へ・C-10 と工程 P0c を新設 | 指示 ② |
| 5 | §3.6 / §9.2 | ★ **前件削除** | **補題 CHARM⟹PRACT**(原文 p.23/p.25/p.39 を頁画像で直接確認)⟹ 系 B4-42 の **(H4) を削除**・**【GAP-B4-2】を削除**・「practical」の但し書きを全文から除去 | 指示 ⑤ |
| 6 | §7.3 R4 | **精密化** | Table 1 の `|GT|` は practical 限定の計数、`|GT♡|` は限定不要 — この非対称を混ぜない | 指示 ⑤ の系 |
| 7 | §7.3 R8 | ★ **新規防壁** | $x_{ij}=x_{ji}$ 対称規約($\sigma_{ij}^2=x_{ij}$)。$\bar\rho$ 実装ずれの**罠 D-6/D-7**。規約台帳への 1 行を別ファイルで起草 | 指示 ⑥ |
| 8 | §3.2.2 | **nit** | 球面関係の使用回数を **3 → 4**(段 A 1・段 B 1・段 C 2)に訂正 | 指示 ⑦ |
| 9 | §12 | ★ **新設** | 事前登録票 v1 への **erratum 3 件**(XFER-0 の標語・XFER-FAKE の独立性会計・practical) | 指示 ③④⑤ |
| 10 | §9.1 | **申告の更新** | 原文 PDF 頁画像 3 枚(p.23/p.25/p.39)を**本起草者が直接**開いた旨を明記 | 本ノート |

**v1.1 の主張で撤回したものはない。** 変更は (a) 自前化による格上げ (b) 予言の追加 (c) 冗長な前件の削除 (d) 表記の精密化 (e) 別票への erratum である。

---

## 12. ★ 事前登録票 v1 への **erratum**(指示③④⑤)

対象: `docs/notes/q46_charming_fake_prereg_iffirst_v1.md`(commit `4d9bd5b`)。
★ **当該ファイルは 1 バイトも改変しない**(IF-FIRST 凍結)。**登録された予言値 Q46-P1〜P7・分岐 BQ-1/2/3・停止規則 S-Q46-0〜6・novelty の格は 1 つも変更されない** ⟹ **S-7′ に抵触しない**。

| # | 対象 | 訂正 |
|---|---|---|
| **E-1** ★ | §3.1 **XFER-0 の標語** | 「4 窓はいずれも $f$ を同じ精度 $P$ でしか見ない」は **charming 層(= $f$ を $F_2$ の元で代表する層)に限って**正しい。**$PB_3$ 水準では偽**: $PB_3/\mathbf N=P$ に対し $PB_3/\mathbf N_0\cong P\times C_7$ で、$c$ 方向の情報が $\mathbf N_0$ 側にだけ残る。**補題 XFER-0 の等式($\cap F_2$ が 4 窓で一致)自体は不変**であり、誤りは標語の量化子のみ。訂正後の標語 = 「**charming 層の上では、4 窓はいずれも $f$ を同じ精度 $P$ でしか見ない**」 |
| **E-2** ★ | §3.7 **XFER-FAKE の「2 経路独立」** | 「独立」の範囲を過大に書いていた。**両経路は $\mathrm{PENT}_W$ の測定(本走 lane P)を共有する。** 独立なのは**橋の部分だけ**である: 経路 α の橋 = HSP-SOUND(HS 由来)/ 経路 β の橋 = 定理 PENT-FORM(2008 + 自前導出)。⟹ 正しい会計は「**測定は共有・橋は 2 本**」。★ **真の第 2 測定経路**($R=PB_4/\mathcal V(PB_4)$ 上で (2.20) を直接測る)は **ANUPQ 環境ブロッカーで停止中**(§5.4)であり、**現時点で $\mathrm{PENT}_W$ の測定は単一系統である**。この一行を fake 判定の格に必ず添える |
| **E-3** ★ | §1 / §3.6 / §4 / §9.2 の **practical** | **charming ⟹ practical**(補題 CHARM⟹PRACT・原文 p.23/p.25/p.39)ゆえ、$\mathrm{GT}^\heartsuit(\tilde{\mathbf N}_{\rm core})$ の「$\vert_{\rm practical}$」は**冗長**。定理 XFER の像は $\mathrm{GT}^\heartsuit(\tilde{\mathbf N}_{\rm core})$ **全体**である。**【GAP-B4-2】は削除**。§1 の「存在問題ゆえ practical 制限は答えを弱めない」は「**そもそも制限が存在しない**」へ強化される。★ **予言値は不変**(294 / 252 / 42) |

> ★ **司令塔への申し送り**: 本 erratum は本ノート(v1.2)に記録した。**事前登録票側からの発見性**を確保したい場合は、票の **versioned bump(v1.1)を別途発注**されたい(本起草者は凍結票を改変しない方針を採った)。

---

## 付録 A. 機械検算(**本走非接触**)

### A.1 20 本の合成 $\psi\circ p_i\circ\varphi$ — 完全印字(`scratchpad/b4comp2.py`)

```
  p_4 o phi123     : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_4 o phi234     : x12->y        x23->1        x13->1        c->y         CYCLIC-IMAGE, <y>
  p_4 o phi12_3_4  : x12->x^-1     x23->1        x13->1        c->x^-1      CYCLIC-IMAGE, <x>
  p_4 o phi1_23_4  : x12->y^-1     x23->1        x13->1        c->y^-1      CYCLIC-IMAGE, <y>
  p_4 o phi1_2_34  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_3 o phi123     : x12->x        x23->1        x13->1        c->x         CYCLIC-IMAGE, <x>
  p_3 o phi234     : x12->1        x23->1        x13->y        c->y         CYCLIC-IMAGE, <y>
  p_3 o phi12_3_4  : x12->1        x23->1        x13->x^-1     c->x^-1      CYCLIC-IMAGE, <x>
  p_3 o phi1_23_4  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_3 o phi1_2_34  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_2 o phi123     : x12->1        x23->1        x13->x        c->x         CYCLIC-IMAGE, <x>
  p_2 o phi234     : x12->1        x23->y        x13->1        c->y         CYCLIC-IMAGE, <y>
  p_2 o phi12_3_4  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_2 o phi1_23_4  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_2 o phi1_2_34  : x12->1        x23->1        x13->y^-1     c->y^-1      CYCLIC-IMAGE, <y>
  p_1 o phi123     : x12->1        x23->x        x13->1        c->x         CYCLIC-IMAGE, <x>
  p_1 o phi234     : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_1 o phi12_3_4  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_1 o phi1_23_4  : x12->1        x23->x^-1     x13->1        c->x^-1      CYCLIC-IMAGE, <x>
  p_1 o phi1_2_34  : x12->1        x23->y^-1     x13->1        c->y^-1      CYCLIC-IMAGE, <y>
  totals: psi = 8 , degenerate = 12
  (every degenerate row has lambda(c) != 1 => each single row forces k = 0 mod 7)
  p_4 o phi123 = id on PB3 (split retraction): x12->x12 x23->x23 x13->x13 c->x12/x13/x23
```

### A.2 pentagon の恒真性(定理 B4-VAC)

```
  coord i=4 : LHS = f(x,y)  RHS = f(x,y)  -> IDENTITY      coord i=3 : ... -> IDENTITY
  coord i=2 : LHS = f(x,y)  RHS = f(x,y)  -> IDENTITY      coord i=1 : ... -> IDENTITY
```

### A.3 LCS 階数(`scratchpad/lcs.py`)

```
PB_4 : [6, 4, 10, 21, 54, 125]   sum(k<=4) = 41
PB_3 : [3, 1, 2, 3, 6, 9]        sum(k<=4) = 9    (|P| = 7^8)
K(0,5) = PB4/Z : [5, 4, 10, 21]  sum = 40         (|Q| = 7^40, NW-P4)
Witt(2,k) k=1..5 : [2, 1, 2, 3, 6]  sum = 14      (|P'| = 7^14)
```

### A.4 $\tilde{\mathbf N}_{\rm core}$ の指数の絞り込み(`scratchpad/core_rank.py`)

```
F_7-rank of abelianized image = 5   (6 generators, one relation: sum of rows = 0)
=> |PB4 : N_core| divides 7^5 * (7^6)^4 = 7^29 ;  lower bound 7^8
```
★ 階数 5 の意味 = $\Delta^2=\prod x_{ij}$ の像がゼロ、すなわち **$Z(PB_4)\le\tilde{\mathbf N}_{\rm core}$**。

### A.5 ★ $\Delta_4^2$ の積表示(補題 SPH の (1)(4)・v1.2 新)

`scratchpad/fulltwist.py`。**忠実な Artin 表現 $B_4\hookrightarrow\mathrm{Aut}(F_4)$**($\sigma_i:t_i\mapsto t_it_{i+1}t_i^{-1},\ t_{i+1}\mapsto t_i$)の中で自由群の語として同一性を判定する(**Artin 1947 の忠実性により、これは証拠ではなく証明である**)。

```
braid relations in Aut(F4): OK  (Artin rep is faithful - Artin 1947)
c = (s1s2)^3 == x12*x13*x23 : True    == x23*x12*x13 : True
[x14,x23]=1 (nested pair, A.3)      : True
Delta^2 == x12*(x13 x23)*(x14 x24 x34) = c*(x14x24x34) : True
Delta^2 == (x12 x13 x14)(x23 x24)(x34)                 : True
Delta^2 central in PB4 (checked vs all 6 x_ij)         : True
```

- 1 行目: 表現の健全性(braid 関係)。2 行目: **(A.5) の $c=(\sigma_1\sigma_2)^3=x_{12}x_{13}x_{23}=x_{23}x_{12}x_{13}$ を独立に再現**。
- 3 行目: **(A.3) の入れ子の場合** $[x_{14},x_{23}]=1$(補題 SPH (4))。
- 4・5 行目: $\Delta_4^2=(\sigma_1\sigma_2\sigma_3)^4$ の **2 通りの積表示**(補題 SPH (1)(4))。
- 6 行目: $\Delta_4^2\in Z(PB_4)$(補題 SPH (3) と定理 B4-CANON (3) の前提)。
