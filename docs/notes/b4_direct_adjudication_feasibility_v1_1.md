# B₄ 窓での 252 直接裁定 — 実現可能性ノート(**v1.1**)

**状態札: `candidate(実現可能性ノート・紙のみ / 機械は付録 A の記号計算+整数級数+F₇ 線型代数のみ / 本走宇宙の候補評価ゼロ / 封印非接触 / novelty 主張なし)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-06
- 版: **v1.1**。**v1(`b4_direct_adjudication_feasibility_v1.md`・commit `eeaf198`)は 1 バイトも改変せず並置する**(versioned 規律)。差分の全一覧 = **§11**。
- 委嘱: 司令塔(**裁定 598** 初版 / **裁定 608** 改版)。改版の入力:
  - **検分ノート** `docs/notes/b4_theorem_check_v1.md`(別人格の数学者による独立再導出・三定理 PASS + 要修正 11 件)
  - **文献 pin** `docs/scout/ls_pentagon_term_correspondence_v1.md`(reader・LS1994 / LS-Ptolemy / HS2000 の頁画像照合つき抽出)
- 入力正本(すべて既在・本ノートは 1 バイトも改変しない): v1 §0 の一覧に上記 2 本を追加。

---

## 0. 結論(三択・先に 6 行)

> ## ★ 判定 = **条件付き実現可能**(工程表 = §8、欠けの列挙 = §9.2)
> **v1.1 での格上げ**: v1 で最大の未閉点だった **【GAP-B4-1】は紙で閉じた**(定理 **PENT-FORM**・§3.2)。ただし**閉じ方が (3.10) 相対**であるため、v1 の突合設計(悉皆一致)は**偽アラーム設計**であり層別へ改訂した(§8)。

| # | 結論 |
|---|---|
| **0-1** | ★★ **委嘱の問いは二つに割れる。片方は既に裁定済み、もう片方は B₄ の管轄外である。** (α)「252 は B₄ 本来系の genuine か」= **既に否**。B₄ の寄与は新情報ではなく**根拠の差し替え**(HS Prop 7 翻訳 → 2008 の公理そのもの)。(β)「252 の**内訳**(= gentle 系の genuine か)」= **B₄ では原理的に裁けない**。B₄ の極限は $\widehat{GT}$、内訳が問うのは $\widehat{GT}_{gen}$ だから。**法廷が違う**(§4.3)。 |
| **0-2** ★改 | ★★ **Prop 3.9 の構成に現れる 2 つの自然な窓は使えない。** $\ker\tilde\psi$ とその $B_4$-核 $\tilde{\mathbf N}_{\rm core}$ では、**pentagon (2.20) が全 charming $f$ に対し恒真**である(**定理 B4-VAC**・§2.4・機械検算つき)。⟹ 「$\mathrm{PENT}_W$-FAIL ⟹ (2.20)-FAIL」は**この 2 窓では偽**であり、**252 の全件が反例**になる(**反例の舞台は $\tilde{\mathbf N}_{\rm core}$** — $\ker\tilde\psi$ は $B_4$-正規でないので 2008 の窓ではない)。**Prop 3.9 が最終的に取る特性部分群 $\tilde N$ の検出力は未知であり、構成不能ゆえ実用にならない**(§2.6 の表)。 |
| **0-3** | ★★ 使える窓は **$\tilde{\mathbf N}^*:=\mathcal V(PB_4)=\gamma_5(PB_4)PB_4^{\,7}$**。$\tilde{\mathbf N}^*\in\mathrm{NFI}_{PB_4}(B_4)$、$\tilde{\mathbf N}^*_{PB_3}=\mathcal V(PB_3)=\mathbf N_0$(**厳密等号**)、$\tilde{\mathbf N}^*_{F_2}=N_{F_2}$、$\tilde N^*_{\rm ord}=7$、$\lvert PB_4:\tilde{\mathbf N}^*\rvert=7^{41}$、$PB_4/\tilde{\mathbf N}^*\cong C_7\times Q$(**定理 B4-CANON**・§2.5)。 |
| **0-4** | ★★ **hexagon 側は新情報ゼロが定理として出る**(2401 **Prop 3.4** は hexagon 判定が $N_{F_2}$ のみに依存)。⟹ **B₄ 裁定の実体は pentagon 1 本に完全に縮約される**(§3.5)。 |
| **0-5** ★改 | ★★ **【GAP-B4-1】は紙で閉じた**: LS1994 (III) は 2008 (2.20) と逐語同一で、LS1994 §4 の項レベル変形を工房記法で書き下すと $$\boxed{\ (2.20)\ \Longleftrightarrow\ \mathrm{PENT}_W\qquad\textbf{ただし (3.10) を前件とする}\ }$$(**定理 PENT-FORM**・§3.2)。使う材料は **(I)=(3.10) 2 回・球面関係 (4) 3 回・中心元吸収 3 回**のみで、**(II)(hexagon 第 2 本)は使わない**・**全段が等式代入ゆえ可逆**。**HS2000 Prop 7 は使用しない**(lift 存在の量化子 = 罠 D-5)。 |
| **0-6** | ★★ 条件が揃えば $\mathrm{GT}^\heartsuit_{2008}(\tilde{\mathbf N}^*)\vert_{\rm practical}=\textbf{42}$・**全元 genuine**(**系 B4-42**・§3.6)= 2008 **Question 4.7** が求める型の実例。**novelty は主張しない**(§9.4)。 |
| **0-7** | ★ 内訳(β)は **1 ビット**(**命題 BIT-252**・§4.4): $\mathfrak G_{\rm gen}^{\rm gentle}(\mathbf N)\in\{42,294\}$、中間なし。**42 側は 1 元 × 1 窓 × 117,649 件で決着**(§4.5)。294 側なら **$\widehat{GT}\to\widehat{GT}_{gen}$ が全射でない**ことが有限窓で証人つきになる。**この実験は B₃-gentle 側にあり、B₄ ではない。** |

> ### ★ 一行で(不変)
> **B₄ 法廷は既に評決を下している(252 = 非オブジェクト)。B₄ を建て増しする価値は「評決の根拠を HS 翻訳から 2008 の公理へ差し替えること」と「Q4.7 型の完全同定を 1 つ得ること」にあり、252 の内訳は別の法廷(gentle 塔)に持ち込むべきである。**

---

## 1. 記号・前提・引用と自前導出の分離

### 1.1 うちの窓(既在・再測定しない)

$$\mathbf N=\mathcal V(F_2)\times\langle c\rangle,\quad \mathbf N_0=\mathcal V(PB_3)=\mathcal V(F_2)\times\langle c^{7}\rangle,\quad N_{F_2}=\mathcal V(F_2)=\gamma_5(F_2)F_2^{\,7},$$
$$W=\mathcal V(K(0,5)),\quad P=F_2/N_{F_2}\ (7^8),\quad Q=K(0,5)/W\ (7^{40}),\quad \lvert[P,P]\rvert=7^6=117{,}649 .$$
$\mathcal X_{\mathbf N}$ は 6 元。本走宇宙 $=705{,}894$。本走の答え = hexagon **294**・$\mathrm{PENT}_W$ **42**・hexagon-only **252**。
$PB_3=F_2\times\langle c\rangle$、$c=x_{12}x_{13}x_{23}=x_{23}x_{12}x_{13}=(\sigma_1\sigma_2)^3$(A.5)。

### 1.2 引用する既在の結果(本ノートは再証明しない)

v1 §1.2 の表に、**文献 pin 由来の 3 行**を追加する:

| 札 | 内容 | 出所 |
|---|---|---|
| **LS-(III)** | $f(x_{12},x_{23}x_{24})\,f(x_{13}x_{23},x_{34})=f(x_{23},x_{34})\,f(x_{12}x_{13},x_{24}x_{34})\,f(x_{12},x_{23})$。舞台 $=\hat K_4=\widehat{PB_4}$(中心あり) | LS1994 §1 p.4(**頁画像照合済** = pin ノート A-1) |
| **LS-(4)** | $K(0,5)$ 内で $\bar x_{45}=\bar x_{12}\bar x_{13}\bar x_{23}$、$\bar x_{15}=\bar x_{23}\bar x_{24}\bar x_{34}$(基点 4 の Hurwitz 関係 $\bar x_{14}\bar x_{24}\bar x_{34}\bar x_{45}=1$ と $\bar\omega_5=1$ から) | LS1994 §2 p.7(**頁画像照合済** = pin A-2) |
| **LS-(abs)** | $f\in[F_2,F_2]$ と、$\alpha,\beta$ と可換な $\gamma$ について $f(\gamma\alpha,\beta)=f(\alpha,\gamma\beta)=f(\alpha,\beta)$ | LS1994 p.13(lemma 5 直前・**頁画像照合済** = pin A-2) |
| **LS-(III′)** | $f(x_{34},x_{45})f(x_{51},x_{12})f(x_{23},x_{34})f(x_{45},x_{51})f(x_{12},x_{23})=1$。舞台 $=\hat M(0,5)$。$\rho(x_{ij})=x_{i+3,j+3}$ の下で $\rho^4(f)\rho^3(f)\rho^2(f)\rho(f)f=1$ に**逐語一致** | LS1994 §4 p.17(**頁画像照合済** = pin A-2/A-3) |
| **Prop 3.4** | $(m,f)\in\mathbb Z\times[F_2,F_2]$ の hexagon 判定は $N_{F_2}$ **のみ**に依存 | 2401 §3 p.11(仲裁ノート §1 に逐語) |
| **VERBAL-DESCENT** | $\mathcal V(Q)=\mathcal V(R)=1$ ゆえ、**任意の**準同型 $h:F_2\to Q$(resp. $R$)で $h(N_{F_2})=1$ | 検分ノート §5.3(3 行の補題) |

そのほか (2.20) / (A.18) / (2.4) / Prop 3.9(A) / Cor 3.13 / Thm 3.8 / Q4.6 / Q4.7 / CENT-FREE / VERBAL-ISO / H8′ / BH-α-pent v1.1 は v1 §1.2 のまま。

### 1.3 本ノートが自前で導く命題

補題 **B4-FORGET** / ★補題 **CORE-4**(v1.1 新) / 補題 **B4-IND** / ★定理 **B4-VAC** / ★定理 **B4-CANON** / 補題 **B4-MONO** / 定理 **B4-DIR** / ★★定理 **PENT-FORM**(v1.1 新) / 補題 **B4-KAPPA** / ★系 **B4-42** / ★命題 **BIT-252** / 補題 **CHARM-EQ**。

---

## 2. 委嘱① — 窓の持ち上げ

### 2.1 Prop 3.9 の構成の逐語(txt L2571–2605)— v1 と同一

要点 3 つ(v1 §2.1 のまま): ① $\ker\tilde\psi$ は $B_4$-正規とは限らない ② Dolgushev の $\tilde N$(指数 $\lvert PB_4:\ker\tilde\psi\rvert$ の正規部分群**全交わり**)は**構成不能** ③ さらに Cor 3.5 の isolated 化で一段細かくなる。⟹ **Prop 3.9 は cofinality の存在定理であってレシピではない。**

### 2.2 補題 **B4-FORGET** と ★補題 **CORE-4**

> ### 補題 B4-FORGET
> $p_4:PB_4\to PB_3$(第 4 紐忘却)について $\tilde\psi=\psi\circ p_4$。とくに well-definedness に (A.3) の場合分けは不要($p_4$ は Fadell–Neuwirth 分裂 $PB_4\cong F_3\rtimes PB_3$ の射影)。$\ker\tilde\psi=p_4^{-1}(N)$。∎

$\sigma_3$ 共役が $x_{13}$ を $x_{14}$ 型へ移すので $\ker\tilde\psi\not\trianglelefteq B_4$。$B_4$-核を取る必要があるが、**「$p_i$ をどう同一視するか」を定めないと $\bigcap_ip_i^{-1}(N)$ という式自体が well-defined でない**(v1 の「捻れは吸収される」1 行は剰余類内の曖昧さしか扱っていなかった — 検分 §2.2 の指摘)。以下で埋める。

> ### ★ 補題 CORE-4(v1.1 新・検分ノート §2.2 の補題を採録)
> $N\trianglelefteq B_3$、$N\le PB_3$、$[B_3:N]<\infty$ とし、$p_i:PB_4\twoheadrightarrow PB_3$ を「第 $i$ の紐を忘れ、残る 3 本を**順序保存**で $1,2,3$ に付け替える射」とする。このとき
> $$\mathrm{core}_{B_4}\bigl(p_4^{-1}(N)\bigr)=\bigcap_{i=1}^{4}p_i^{-1}(N).$$
>
> **証明.**
> **(1) 剰余類内の不変性.** $B_{3,1}:=\{b\in B_4:w_b(4)=4\}$(指数 4)上で $p_4$ は準同型 $B_{3,1}\to B_3$ に延び、$u\in B_{3,1}$ に対し $u\,p_4^{-1}(N)\,u^{-1}=p_4^{-1}(p_4(u)Np_4(u)^{-1})=p_4^{-1}(N)$($N\trianglelefteq B_3$)。
> **(2) 代表元.** $b_4:=1,\ b_3:=\sigma_3,\ b_2:=\sigma_2\sigma_3,\ b_1:=\sigma_1\sigma_2\sigma_3$。
> **(3) 鍵 — 3 本の合成が 6 生成元すべてで厳密に一致する.** $c_b(g):=b^{-1}gb$ とし、(A.2) の $x_{12}=\sigma_1^2,\ x_{23}=\sigma_2^2,\ x_{34}=\sigma_3^2,\ x_{13}=\sigma_2\sigma_1^2\sigma_2^{-1},\ x_{24}=\sigma_3\sigma_2^2\sigma_3^{-1},\ x_{14}=\sigma_3\sigma_2\sigma_1^2\sigma_2^{-1}\sigma_3^{-1}$ と (A.6) から:
>
> | 生成元 | $c_{\sigma_3^{-1}}$ の値 | $p_4\!\circ\!c_{\sigma_3^{-1}}$ | $p_3$ | $c_{\sigma_2^{-1}}$ の値 | $p_3\!\circ\!c_{\sigma_2^{-1}}$ | $p_2$ | $c_{\sigma_1^{-1}}$ の値 | $p_2\!\circ\!c_{\sigma_1^{-1}}$ | $p_1$ |
> |---|---|---|---|---|---|---|---|---|---|
> | $x_{12}$ | $x_{12}$ | $x_{12}$ | $x_{12}$ | $\sigma_1x_{23}\sigma_1^{-1}$ | $1$ | $1$ | $x_{12}$ | $1$ | $1$ |
> | $x_{13}$ | $x_{14}$ | $1$ | $1$ | $x_{12}$ | $x_{12}$ | $x_{12}$ | $x_{12}^{-1}x_{23}x_{12}$ | $1$ | $1$ |
> | $x_{23}$ | $x_{24}$ | $1$ | $1$ | $x_{23}$ | $1$ | $1$ | $x_{13}$ | $x_{12}$ | $x_{12}$ |
> | $x_{14}$ | $x_{13}$ | $x_{13}$ | $x_{13}$ | $x_{14}$ | $x_{13}$ | $x_{13}$ | $x_{12}^{-1}x_{24}x_{12}$ | $1$ | $1$ |
> | $x_{24}$ | $x_{23}$ | $x_{23}$ | $x_{23}$ | $x_{23}^{-1}x_{34}x_{23}$ | $1$ | $1$ | $x_{14}$ | $x_{13}$ | $x_{13}$ |
> | $x_{34}$ | $x_{34}$ | $1$ | $1$ | $x_{24}$ | $x_{23}$ | $x_{23}$ | $x_{34}$ | $x_{23}$ | $x_{23}$ |
>
> ($\sigma_3^{-1}x_{14}\sigma_3=\sigma_2\sigma_1^2\sigma_2^{-1}=x_{13}$、$\sigma_3^{-1}x_{24}\sigma_3=\sigma_2^2=x_{23}$、$\sigma_2^{-1}x_{34}\sigma_2=(\sigma_3\sigma_2\sigma_3^{-1})^2=\sigma_3\sigma_2^2\sigma_3^{-1}=x_{24}$、$\sigma_1^{-1}x_{24}\sigma_1=\sigma_3(\sigma_1^{-1}x_{23}\sigma_1)\sigma_3^{-1}=\sigma_3x_{13}\sigma_3^{-1}=x_{14}$ は**厳密な等式**。共役形の 4 箇所は $\ker p_\bullet\trianglelefteq PB_4$ ゆえ値 $1$。)
> ⟹ $p_4\circ c_{\sigma_3^{-1}}=p_3$、$p_3\circ c_{\sigma_2^{-1}}=p_2$、$p_2\circ c_{\sigma_1^{-1}}=p_1$(各 6 生成元で一致)。合成して $p_4\circ c_{b_i^{-1}}=p_i$。
> **(4) 結論.** $b\,p_4^{-1}(N)\,b^{-1}=\ker(\psi\circ p_4\circ c_{b^{-1}})$。$b=b_iu$($u\in B_{3,1}$)と書けば (1)(3) より $=\ker(\psi\circ p_i)=p_i^{-1}(N)$。∎

$\tilde{\mathbf N}_{\rm core}:=\bigcap_i\ker(\psi p_i)$ は核なので $B_4$-正規・有限指数・$\le PB_4$ ⟹ **$\tilde{\mathbf N}_{\rm core}\in\mathrm{NFI}_{PB_4}(B_4)$**、$PB_4/\tilde{\mathbf N}_{\rm core}\hookrightarrow P^4$。

★ **付随事実(v1.1 新)**: $\Delta^2=\prod_{i<j}x_{ij}$ について $p_i(\Delta^2)=c\in\mathbf N$ ⟹ **$Z(PB_4)=\langle\Delta^2\rangle\le\tilde{\mathbf N}_{\rm core}$**。すなわち $\tilde{\mathbf N}_{\rm core}$ は $K(0,5)$ の部分群の逆像である。付録 A.4 の $\mathbb F_7$-階数 5(6 生成元に関係 1 本)がこれを機械側から裏づける。

### 2.3 補題 **B4-IND**(下位誘導 (2.4) の値 = $\mathbf N_0$)

> $$\boxed{\ (\ker\tilde\psi)_{PB_3}=(\tilde{\mathbf N}_{\rm core})_{PB_3}=\mathcal V(F_2)\times\langle c^{7}\rangle=\mathbf N_0\ }$$
> **証明.** 20 本の合成 $\psi p_i\varphi$(**付録 A.1 の完全表** — $x_{12},x_{23},x_{13},c$ の全列)は **8 本が $\psi$**(核 $=\mathbf N$)、**12 本が退化**(像が位数 7 の巡回群)に分かれる。★ **12 本すべてで $\lambda(c)\ne1$** ゆえ、$w=f\,c^k$($f\in\mathcal V(F_2)$、$\varepsilon(f)\equiv0$)に対し**退化 1 本だけで $k\equiv0\ (\mathrm{mod}\ 7)$ が出る**。逆に $\mathcal V(F_2)\times\langle c^7\rangle$ は 20 本すべての核に入る。∎

★ **v1 からの訂正(検分 §2.3 要修正 2)**: v1 の付録表は $x_{12},x_{23}$ 列しか印字しておらず、4 本($p_3\varphi_{234}$, $p_3\varphi_{12,3,4}$, $p_2\varphi_{123}$, $p_2\varphi_{1,2,34}$)が「$1,1$」= 自明写像に見えた。**実際には $x_{13}$ と $c$ の上で非自明**であり、結論はむしろ $\lambda(c)\ne1$ に依存している。付録 A.1 を完全印字に差し替えた。また v1 の「総合して $k\equiv0$」は弱い言い方で、**各本が単独で十分**である。

### 2.4 ★ 定理 **B4-VAC**(2 窓での pentagon 検出力ゼロ)

> ### 定理 B4-VAC
> $\tilde{\mathbf N}\in\{\ker\tilde\psi,\ \tilde{\mathbf N}_{\rm core}\}$ とする。**すべての charming $f$ に対し pentagon (2.20) は $PB_4/\tilde{\mathbf N}$ の中で恒真**である。
> **証明.** 退化写像の像は巡回(可換)かつ指数 7 ゆえ $[F_2,F_2]$ も $\mathcal V(F_2)$ も潰す。各座標 $i$ について 5 本のうち 2 本が $\psi$・3 本が退化(付録 A.1)なので (2.20) の第 $i$ 座標は
> $$i{=}4:\ 1\!\cdot\!1\!\cdot\!f=f\!\cdot\!1,\quad i{=}3:\ 1\!\cdot\!f\!\cdot\!1=f\!\cdot\!1,\quad i{=}2:\ 1\!\cdot\!f\!\cdot\!1=1\!\cdot\!f,\quad i{=}1:\ f\!\cdot\!1\!\cdot\!1=1\!\cdot\!f$$
> となり 4 座標すべて恒等式。$PB_4/\tilde{\mathbf N}_{\rm core}\hookrightarrow P^4$ ゆえ連立と同値。$\ker\tilde\psi$ は $i=4$ 座標のみ。∎

> ### ★ 委嘱②への直接回答(その 1)★改
> $$\boxed{\ \textbf{「}\mathrm{PENT}_W\textbf{-FAIL}\Rightarrow(2.20)\textbf{-FAIL」は }\tilde{\mathbf N}_{\rm core}\textbf{ では偽であり、252 の全件が反例である。}\ }$$
> 舞台を $\tilde{\mathbf N}_{\rm core}$ と明記する($\ker\tilde\psi$ は $B_4$-正規でなく 2008 の窓ではないので、反例の舞台に使えない)。理由は構造的: $\tilde\psi=\psi\circ p_4$ は **$B_3$ のデータしか持たない**。Prop 3.9 は「$K_{PB_3}\le N$」という下位互換性だけを保証しており、pentagon の情報量については何も言っていない。
> ⚠ **射程の限定(v1.1 で訂正)**: 本定理は **Prop 3.9 の構成の途中に現れる 2 窓**についての言明である。**Prop 3.9 が最終的に取る特性部分群 $\tilde N$(および Cor 3.5 の isolated 化)の pentagon 検出力は未知**であり、構成不能ゆえ実用にならない(§2.6 の表と整合)。

### 2.5 ★ 定理 **B4-CANON**(使うべき窓 = verbal lift)

> $\tilde{\mathbf N}^*:=\mathcal V(PB_4)=\gamma_5(PB_4)PB_4^{\,7}$ について
> **(1)** verbal ⟹ 完全不変 ⟹ 特性、$PB_4\trianglelefteq B_4$ ゆえ $\tilde{\mathbf N}^*\trianglelefteq B_4$、有限指数 ⟹ $\in\mathrm{NFI}_{PB_4}(B_4)$。
> **(2)** $\tilde{\mathbf N}^*_{PB_3}=\mathcal V(PB_3)=\mathbf N_0$(**厳密等号**)。$\tilde{\mathbf N}^*_{F_2}=N_{F_2}$、$\tilde N^*_{\rm ord}=7$、$\mathcal X$ は 6 層。
> **(3)** $PB_4\cong\mathbb Z\times K(0,5)$ ゆえ $PB_4/\tilde{\mathbf N}^*\cong C_7\times Q$。
> **(4)** $\lvert PB_4:\tilde{\mathbf N}^*\rvert=7\cdot\lvert Q\rvert=7^{41}$。
>
> **証明.** (1) 上記。(2) ($\supseteq$)余面は準同型ゆえ $\varphi(\mathcal V(PB_3))\subseteq\mathcal V(PB_4)$。($\subseteq$)$p_4\circ\varphi_{123}=\mathrm{id}_{PB_3}$(付録 A.1 最終行)ゆえ $\varphi_{123}$ は分裂単射で、$\varphi_{123}(w)\in\mathcal V(PB_4)\Rightarrow w=p_4\varphi_{123}(w)\in p_4(\mathcal V(PB_4))=\mathcal V(PB_3)$($p_4$ 全射ゆえ verbal は verbal に**全射で**写る)。$\mathcal V(PB_3)=\mathcal V(F_2)\times\langle c^7\rangle$ は箱型。$\tilde N^*_{\rm ord}=\mathrm{lcm}(7,7,7)=7$(Prop 2.3、$PB_3/\mathbf N_0\cong P\times C_7$)。(3) $PB_4^{\rm ab}=\mathbb Z^6$ で $\Delta^2\mapsto(1,\dots,1)$、座標射影が $\Delta^2\mapsto1$ ⟹ 中心が直因子。verbal は直積を尊重。**(4)** ★ **(3) と既在の実測値 $\lvert Q\rvert=7^{40}$(NW-P4)から直ちに従う** — $PB_4$ への Lazard 適用を独立仮定にしなくてよい。∎

> ★ **v1 からの格上げ(検分 要修正 11)**: v1 は (4) を LCS 公式 + Lazard で導き `paper-proof candidate` としていた。**(3) + 既在実測の経路を採れば `paper-proof`** に上がる。LCS 公式による独立計算(付録 A.3: $PB_4$ 階数 $(6,4,10,21)$、$K(0,5)$ 階数 $(5,4,10,21)$)は**独立検算として保持**する($\lvert Q\rvert=7^{40}$ の紙側再現)。

### 2.6 4 つの窓の比較(委嘱①のまとめ)

| 窓 | 定義 | $\tilde{\mathbf N}_{PB_3}$ | $B_4$ 正規 | 計算可能性 | pentagon 検出力 |
|---|---|---|---|---|---|
| $\ker\tilde\psi$ | $p_4^{-1}(\mathbf N)$ | $\mathbf N_0$ | ✗(**2008 の窓ではない**) | ◎($P$ の中) | **ゼロ**(定理 B4-VAC) |
| $\tilde{\mathbf N}_{\rm core}$ | $\bigcap_ip_i^{-1}(\mathbf N)$(CORE-4) | $\mathbf N_0$ | ✓ | ◎($P^4$ の中) | **ゼロ**(同) |
| Prop 3.9 の $\tilde N$ | 指数 $7^8$ の正規部分群 全交わり(+ Cor 3.5) | $\le\mathbf N_0$ | ✓ | ✗(構成不能) | **未知** |
| ★ $\tilde{\mathbf N}^*=\mathcal V(PB_4)$ | $\gamma_5PB_4^{\,7}$ | $\mathbf N_0$(**等号**) | ✓ | ◎(pc 群 $7^{41}$・**環境ブロッカーあり** §5.4) | ★ **$W$ 水準**(§3) |

---

## 3. 委嘱② — 判定の形と $\mathrm{PENT}_W$ との論理関係

### 3.1 補題 **B4-MONO**(窓単調性)と 定理 **B4-DIR**

> **B4-MONO**: $\tilde{\mathbf N}'\le\tilde{\mathbf N}$ なら (2.20) mod $\tilde{\mathbf N}'$ ⟹ (2.20) mod $\tilde{\mathbf N}$。FAIL は細かい窓へ、PASS は粗い窓へ伝播。

$L:=$($PB_4\twoheadrightarrow K(0,5)$ による $W$ の逆像)$\in\mathrm{NFI}_{PB_4}(B_4)$、$\lvert PB_4:L\rvert=7^{40}$。

> **B4-DIR**: **(a)** $\tilde{\mathbf N}\le L$ なら $\mathrm{PENT}_W$-FAIL ⟹ (2.20) mod $\tilde{\mathbf N}$ FAIL。**(b)** そうでない窓では一般に偽(反例 = 定理 B4-VAC)。**(c)** $\tilde{\mathbf N}^*=7\mathbb Z\times W\le L=\mathbb Z\times W$ で、charming $f$ に対しては pentagon defect $D\in[PB_4,PB_4]=[K(0,5),K(0,5)]$ ゆえ
> $$D\in\tilde{\mathbf N}^*\iff D\in L\iff \bar D\in W .$$
> ⟹ **$\tilde{\mathbf N}^*$ が中心を丸ごとは含まない($7\mathbb Z$ のみ)ことは、charming $f$ の pentagon 判定に一切影響しない。**(検分 §3.3 が独立に検証)

### 3.2 ★★ 定理 **PENT-FORM**(v1.1 新)— 【GAP-B4-1】の**紙による閉鎖**

**出発点(pin ノート A-1 + 検分 §5.1)**: **LS1994 (III) と 2008 (2.20) は左右を入れ替えただけの同一式**である。(A.18) で (2.20) を展開すると
$$f(x_{23},x_{34})\cdot f(x_{12}x_{13},x_{24}x_{34})\cdot f(x_{12},x_{23})\;=\;f(x_{12},x_{23}x_{24})\cdot f(x_{13}x_{23},x_{34}) .$$
⟹ **2008 系と LS 系の pentagon の同定に版差はない。**

$\mathrm{PENT}_W$ の側は LS1994 (III′) と逐語一致(pin A-2/A-3)。記号を固定する:
$$f_1:=f(x_{12},x_{23}),\quad f_2:=f(x_{45},x_{51}),\quad f_3:=f(x_{23},x_{34}),\quad f_4:=f(x_{51},x_{12}),\quad f_5:=f(x_{34},x_{45}),$$
$$\text{(III′)}\iff f_5f_4f_3f_2f_1=1\iff \rho^4(f)\rho^3(f)\rho^2(f)\rho(f)f=1\iff \mathrm{PENT}_W .$$

> ### ★★ 定理 PENT-FORM
> $f\in[F_2,F_2]$ とする。$K(0,5)$(およびその任意の商)の中で、**関係 (I) $f(a,b)f(b,a)=1$ が代入対 $(a,b)=(x_{45},x_{34})$ と $(x_{12},x_{15})$ で成立する**ならば
> $$\boxed{\ \textbf{(2.20)}\ \Longleftrightarrow\ \textbf{(III′)}\ =\ \mathrm{PENT}_W .\ }$$
> 使う材料は **LS-(4)・LS-(abs)・(I)** のみで、**(II)(hexagon 第 2 本)は使わない**。**全段が等式代入ゆえ両向き**である。
>
> **証明.** $K(0,5)$ の中で次の 3 つの可換性を先に確認する。
> - $x_{45}=x_{12}x_{13}x_{23}=\varphi_{123}(c)$(**LS-(4)**)は紐 $\{1,2,3\}$ 上の $PB_3$ の中心元ゆえ **$x_{12},x_{13},x_{23}$ と可換**((A.5): $Z(PB_3)=\langle c\rangle$)。
> - $x_{15}=x_{23}x_{24}x_{34}=\varphi_{234}(c)$(**LS-(4)**・(A.18) で $\varphi_{234}(c)=x_{23}x_{24}x_{34}$)は紐 $\{2,3,4\}$ 上の $PB_3$ の中心元ゆえ **$x_{23},x_{24},x_{34}$ と可換**。
> - $x_{12}$ と $x_{34}$ は添字が交わらないので可換((A.3))。
>
> **段 A** $\;f(x_{13}x_{23},x_{34})=f_5^{-1}$:
> $x_{45}=x_{12}(x_{13}x_{23})$ より $x_{13}x_{23}=x_{12}^{-1}x_{45}$。$\gamma:=x_{12}^{-1}$ は $x_{45}$ とも $x_{34}$ とも可換なので **LS-(abs)** で
> $$f(x_{13}x_{23},x_{34})=f(x_{12}^{-1}x_{45},x_{34})=f(x_{45},x_{34})\overset{(I)}{=}f(x_{34},x_{45})^{-1}=f_5^{-1}.$$
>
> **段 B** $\;f(x_{12},x_{23}x_{24})=f_4^{-1}$:
> $x_{15}=(x_{23}x_{24})x_{34}$ と $[x_{34},x_{15}]=1$ より $x_{23}x_{24}=x_{15}x_{34}^{-1}=x_{34}^{-1}x_{15}$。$\gamma:=x_{34}^{-1}$ は $x_{12}$ とも $x_{15}$ とも可換なので **LS-(abs)** で
> $$f(x_{12},x_{23}x_{24})=f(x_{12},x_{34}^{-1}x_{15})=f(x_{12},x_{15})\overset{(I)}{=}f(x_{15},x_{12})^{-1}=f_4^{-1}\qquad(x_{51}=x_{15}).$$
>
> **段 C** $\;f(x_{12}x_{13},x_{24}x_{34})=f_2$(★ **(I) を使わない**):
> $x_{45}=x_{12}x_{13}x_{23}$ と $[x_{23},x_{45}]=1$ より $x_{12}x_{13}=x_{45}x_{23}^{-1}=x_{23}^{-1}x_{45}$。
> $x_{15}=x_{23}x_{24}x_{34}$ より $x_{24}x_{34}=x_{23}^{-1}x_{15}$。
> **両スロットに同じ $\gamma=x_{23}^{-1}$** が現れ、$\gamma$ は $x_{45}$ とも $x_{15}$ とも可換。$f\in[F_2,F_2]$ の指数和はゼロゆえ
> $$f(\gamma x_{45},\gamma x_{15})=\gamma^{0}\,f(x_{45},x_{15})=f(x_{45},x_{51})=f_2 .$$
> (**LS-(abs)** の両スロット版。$h(w)=\gamma^{\varepsilon(w)}h_0(w)$ で $\varepsilon\vert_{[F_2,F_2]}=0$。)
>
> **合成.** (2.20) は $f_3\cdot f(x_{12}x_{13},x_{24}x_{34})\cdot f_1=f(x_{12},x_{23}x_{24})\cdot f(x_{13}x_{23},x_{34})$、すなわち段 A/B/C を代入して
> $$f_3f_2f_1=f_4^{-1}f_5^{-1}\iff f_5f_4f_3f_2f_1=1 .$$
> 各段は**等式による置換**なので両向きに使える。∎

> ### ★ 有限窓への降下(**verbal 窓ゆえ自動**)
> 上の証明は $K(0,5)$ の群関係だけを使うので、任意の商 — とくに $Q=K(0,5)/W$ — にそのまま降りる。唯一 $f$ に課される条件が (I) であり、その有限版は **VERBAL-DESCENT**(検分 §5.3)で処理される:
> $$f\theta(f)\in N_{F_2}=\mathcal V(F_2)\ \ \text{(= 2401 (3.10))}\ \Longrightarrow\ \forall h:F_2\to Q,\ \ h\bigl(f\theta(f)\bigr)\in\mathcal V(Q)=1 .$$
> ⟹ 段 A の $(a,b)=(x_{45},x_{34})$、段 B の $(x_{12},x_{15})$ という**非標準の代入対**でも (I) が $Q$ の中で成立する。**marking の自由度がゼロな verbal 窓だからこそ、代入ごとの検査が不要になる**(翻訳ノート §5 の設計利点 (iii) の払い戻し)。

> ### ★★ 系 PENT-EQ(判定機の等価性・**層つき**)
> $$\boxed{\ \bar f\in S_1:=\{\bar f\in[P,P]:\ (3.10)\ \text{が成立}\}\ \Longrightarrow\ \bigl[\ (2.20)\bmod\tilde{\mathbf N}^*\iff\mathrm{PENT}_W\ \bigr].}$$
> **証明.** B4-DIR (c) で (2.20) mod $\tilde{\mathbf N}^*$ $\iff$ $\bar D\in W$ $\iff$ (2.20) の $Q$ での像。そこに定理 PENT-FORM を適用。∎
>
> ⚠ **$S_0\setminus S_1$ では何も言えない。** (I) を落とすと段 A/B が使えず、(2.20) は「捻れた 5 項恒等式」と同値になるだけである。**v1 の工程 P3(117,649 件の悉皆一致)は、この層で不一致が出るのが自然な設計であり、偽アラームを生む**(検分 §5.4 (b))。§8 で層別に改訂した。

### 3.3 ★ 委嘱②への直接回答(その 2 — 論理関係の最終形)★改

| 主張 | 状態(v1.1) |
|---|---|
| genuine ⟹ (2.20) mod $\tilde{\mathbf N}$(任意の窓) | **定理**(2008 の公理)。**HS Prop 7 の翻訳を一切要しない** |
| genuine ⟹ $\mathrm{PENT}_W$ | 既在(HSP-SOUND) |
| $\bar f\in S_1$ で (2.20) mod $\tilde{\mathbf N}^*$ $\iff$ $\mathrm{PENT}_W$ | ★ **定理 PENT-FORM + 系 PENT-EQ**(**紙で閉鎖・文献相対**) |
| $\bar f\in S_0\setminus S_1$ での関係 | **UNKNOWN**(予言しない・STOP 条件にしない) |
| $\mathrm{PENT}_W$-FAIL ⟹ (2.20) mod $\tilde{\mathbf N}_{\rm core}$ FAIL | ★ **偽**(反例 = 252 全件・定理 B4-VAC) |

### 3.4 判定機の形(委嘱②「判定の手順」)

$R:=PB_4/\tilde{\mathbf N}^*$($7^{41}$・pc 群)とおくと各余面は $\bar\varphi_\bullet:P\to R$ に降りる。生成元上の値は (A.18):

| $\bar\varphi$ | $x\mapsto$ | $y\mapsto$ |
|---|---|---|
| $\bar\varphi_{123}$ | $x_{12}$ | $x_{23}$ |
| $\bar\varphi_{234}$ | $x_{23}$ | $x_{34}$ |
| $\bar\varphi_{12,3,4}$ | $x_{13}x_{23}$ | $x_{34}$ |
| $\bar\varphi_{1,23,4}$ | $x_{12}x_{13}$ | $x_{24}x_{34}$ |
| $\bar\varphi_{1,2,34}$ | $x_{12}$ | $x_{23}x_{24}$ |

$$D_{B_4}(\bar f):=\bigl(\bar\varphi_{1,2,34}(\bar f)\,\bar\varphi_{12,3,4}(\bar f)\bigr)^{-1}\cdot\bar\varphi_{234}(\bar f)\,\bar\varphi_{1,23,4}(\bar f)\,\bar\varphi_{123}(\bar f),\qquad \text{(2.20)}\iff D_{B_4}(\bar f)=1 .$$
★ **$m$ 非依存** ⟹ 評価は **117,649 件**。

### 3.5 hexagon 側は新情報ゼロ(定理として)

$\tilde{\mathbf N}^*_{PB_3}=\mathbf N_0$、$\mathbf N_0\cap F_2=\mathbf N\cap F_2=\mathcal V(F_2)$、**2401 Prop 3.4** ⟹
$$\boxed{\ \textbf{hexagon mod }\tilde{\mathbf N}^*_{PB_3}\iff\textbf{hexagon mod }\mathbf N\quad(\text{全 }m,\ \text{全 charming }f).\ }$$
独立確認 = **補題 B4-KAPPA**(v1 §3.4 のまま): $\kappa:PB_3\to\mathbb Z$($fc^k\mapsto k$)について hexagon defect $d_1,d_2$ は $\kappa(d_1)=\kappa(d_2)=0$($f=1$ の直接計算 + $f\to fg$ 変化分が $PB_3^{\rm ab}=\mathbb Z^3$ 上で消えること)。

⟹ **B₄ 裁定の実体は pentagon 1 本に完全に縮約される。**

### 3.6 ★ 系 **B4-42**(条件つき・Q4.7 型の完全同定)

> 前件 **(H1)** 系 PENT-EQ が層 $S_2$(full hexagon ⊆ $S_1$)で適用できること(**紙で閉じた** — 文献相対)、**(H2)** 本走の測定値(hexagon 294・$\mathrm{PENT}_W$ 42)、**(H3)** BH-α-pent v1.1($\mathfrak G_{\rm ar}=42$)、**(H4)** practical 制限、**(H5)** SURJ 自動 の下で
> $$\boxed{\ \mathrm{GT}^\heartsuit_{2008}(\tilde{\mathbf N}^*)\big\vert_{\rm practical}\ \textbf{はちょうど 42 元からなり、その全元が genuine である。}\ }$$
> **証明.** GT-shadow = GT-pair ∧($T^{PB_3},T^{PB_2}$ 全射)(Def 2.9 + Prop 2.10)。$T^{PB_2}$ 全射 $\iff m\in\mathcal X$。$T^{PB_3}$ 全射: $PB_3/\mathbf N_0\cong P\times C_7$ は 7 群で $\Phi=[P,P]\times1$、像が $x^u,{}^f\!y^u,c^u$($\gcd(u,7)=1$)を含む ⟹ Frattini 論法(H8′ の直接拡張)= **(H5)**。hexagon は §3.5 で $\mathbf N$ のそれと同一、pentagon は $S_2$ 上で $\mathrm{PENT}_W$ と同一(H1)。ゆえに $\mathfrak G_{\rm pent}$ と一致し (H2)(H3) より 42 元 $=\mathfrak G_{\rm ar}$。arithmetic ⟹ genuine。∎

> ★ 意味(v1 と同一): ① **Question 4.7** が求める型の実例(novelty 検査は司令塔ゲート)② $\mathrm{GT}^\heartsuit(\tilde{\mathbf N}^*)$ が全 genuine ⟹ **この窓は Question 4.6 の例を与えない**(★ **別の窓 $\tilde{\mathbf N}_{\rm core}$ は与える** — §7.3 と別ノートの prereg)③ 窓の大きさは $\lvert PB_4:\tilde{\mathbf N}^*\rvert$ でなく $\lvert F_2:\tilde{\mathbf N}^*_{F_2}\rvert=7^8$ で語る(防壁 R6)。

---

## 4. 委嘱③ — genuine の正式判定(Cor 3.13 の有限化)

### 4.1 Cor 3.13 の構造と、有限化が難しい正確な理由

survival の像 $\mathrm{im}(\mathrm{GT}^\heartsuit(K)\to\mathrm{GT}^\heartsuit(N))$ は $K$ について減少し、有限集合の中で**必ず停止**する。Mittag-Leffler より $\mathfrak G_{\rm genuine}(N)=\bigcap_K\mathrm{im}(\cdots)$ = 停止値。
⟹ **障害は「無限個の窓」ではなく「停止点の有効上界がない」ことである**【GAP-B4-3】。陰性証明書は 1 窓で有限、陽性は survival の切り詰めからは原理的に出ない。

### 4.2 ★ 有限化の正しい形 = **サンドイッチ**

$$\mathfrak G_{\rm ar}(N)\subseteq\mathfrak G_{\rm genuine}(N)\subseteq\mathrm{GT}^\heartsuit(N),\qquad
\boxed{\ \lvert\mathfrak G_{\rm ar}\rvert=\lvert\mathrm{GT}^\heartsuit(N)\rvert\Rightarrow\text{Cor 3.13 は当該窓で切り詰め誤差ゼロ}\ }$$
**打ち切るのではなく、下から挟むのが正しい。** 下界の道具は算術実現(円分指標・複素共役・Belyi)であって窓の列挙ではない。

### 4.3 ★★ 委嘱の問い(β)は B₄ の管轄外である

| 理論 | 極限 | 有限窓の圏 | genuine の意味 |
|---|---|---|---|
| B₄ 本来系(2008) | $\widehat{GT}$ | $\mathrm{NFI}_{PB_4}(B_4)$ | $\widehat{GT}$ 由来(Cor 3.13) |
| B₃-gentle(2401) | $\widehat{GT}_{gen}$ | $\mathrm{NFI}_{PB_3}(B_3)$ | $\widehat{GT}_{gen}$ 由来(**2401 Def 4.2**・survival 版 = **2401 Cor 5.4**) |

$$\boxed{\ \textbf{B}_4\ \textbf{は }252\textbf{ の「死因」を厳密化する法廷であって、「内訳」を裁く法廷ではない。}\ }$$

### 4.4 ★ 命題 **BIT-252**(内訳は 1 ビット)★証明経路を改訂

> ### 命題 BIT-252(v1.1)
> 前件: **(ii)** $\mathrm{GT}(\mathbf N)$ は位数 **294** の群($\mathbf N$ isolated = VERBAL-ISO + GRP + 本走)、**(iii)** $\mathfrak G_{\rm ar}(\mathbf N)$ は位数 **42** の部分群(BH-α-pent)。このとき
> $$\boxed{\ \mathfrak G^{\rm gentle}_{\rm genuine}(\mathbf N)\in\{\mathfrak G_{\rm ar}\ (42),\ \mathrm{GT}(\mathbf N)\ (294)\}\quad\textbf{— 中間はない}.}$$
> **証明(v1.1・1 段短縮).** $\mathbf N$ が isolated ゆえ $\mathrm{GT}(\mathbf N)=\mathrm{Aut}_{\mathrm{GTSh}}(\mathbf N)$ は群で、射影 $\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N)$ は関手性から**群準同型**。**2401 Def 4.2** により
> $$\mathfrak G^{\rm gentle}_{\rm genuine}(\mathbf N)=\mathrm{im}\bigl(\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N)\bigr)$$
> ゆえ **「群準同型の像は部分群」の 1 行で閉性**が出る。算術元は $\widehat{GT}\subseteq\widehat{GT}_{gen}$ 由来ゆえ $\supseteq\mathfrak G_{\rm ar}$。$[\mathrm{GT}(\mathbf N):\mathfrak G_{\rm ar}]=7$ は素数ゆえ Lagrange で中間なし(**正規性は不要**)。∎
>
> ★ **v1 からの改訂(検分 要修正 5/6/10)**: v1 は $\bigcap_K\mathrm{im}(\mathrm{GT}(K)\to\mathrm{GT}(\mathbf N))$ を経由し、各項の部分群性のために前件「$K$ も isolated」を背負っていた(⟹【GAP-B4-5】)。**この負債は不要**。なお $\bigcap$ 経由で書く場合は **isolated $K$ に限った交わりが全 $K$ の交わりと一致すること**(2401 **Prop 3.14** の cofinality + 減少性)を明記する必要がある。**【GAP-B4-5】は「不要」かつ「充足」($K=\mathcal V_5(F_2)\times\langle c\rangle$ は $PB_3$ の特性部分群 2 つの積ゆえ $B_3$ 正規・$c\in K$・$K_{F_2}$ verbal ⟹ isolated)の二重で閉じる**(検分 §4.2)。

> ### ★ 系(理論分離の払い戻し)★言明を精密化
> $\mathfrak G_{\rm ar}\subseteq\mathrm{im}(\widehat{GT}\to\mathrm{GT}(\mathbf N))\subseteq\mathfrak G_{\rm pent}$(HSP-SOUND)で両端 42 ⟹ $\mathrm{im}(\widehat{GT})=42$。よって
> - **ビット $=294$** なら $$\boxed{\ \textbf{自然な射 }\widehat{GT}\to\widehat{GT}_{gen}\ \textbf{は全射でない}\ }$$(1 つの有限窓での像の真の包含がその証人)。
> ★ **v1 からの訂正(検分 要修正 7)**: v1 は「$\widehat{GT}_{gen}\supsetneq\widehat{GT}$」と書いたが、これは $\widehat{GT}\hookrightarrow\widehat{GT}_{gen}$ の**単射性を暗黙に使う**。単射性は本ノートでは **UNKNOWN** ⟹ **非全射形**で書く。
> - **ビット $=42$** なら、この窓で両理論の像は一致し、252 は理論分離の情報をもたない。

### 4.5 決定実験(1 元 × 1 窓 × 117,649 件)— **B₃ 側**

**2401 Prop 3.4 により gentle 塔の識別力は $K_{F_2}$ にしかない**ので、下降は $N_{F_2}$ を細かくする方向に限る。

> **設計**: $K:=\mathcal V_5(F_2)\times\langle c\rangle$、$\mathcal V_5(F_2)=\gamma_6(F_2)F_2^{\,7}$。$\lvert P'\rvert=7^{14}$、$\lvert[P',P']\rvert=7^{12}$、$[P',P']\to[P,P]$ の fiber は $7^6=117{,}649$。$K_{\rm ord}=7=\mathbf N_{\rm ord}$ ⟹ **$m$ は固定**。持ち上げは必ず $[P',P']$ に入る(fiber が一致)⟹ **charming 自動**、SURJ は H8′ で自動(検分 §4.4 が全段を独立確認)。
> **手順**: 252 から**任意に 1 元** $g=(m,\bar f)$。$\bar f$ の 117,649 個の持ち上げについて (3.10)(3.11) を $\mathcal V_5(F_2)$ の中で検査。
> - **全滅** ⟹ **2401 Cor 5.4 の易しい向き**(genuine ⟹ 全 $K$ に survive)の対偶で $g$ は fake ⟹ BIT-252 より **252 全件が gentle-fake**。**内訳 CLOSED**。
> - **通るものがある** ⟹ 不決(より深い窓へ)。
> **必要な前件は「$\mathbf N$ が isolated」だけ**($K$ の isolated 性も Cor 5.4 の難しい向きも不要 — 検分 §4.4)。**コスト**: 数分。

⚠ **本ノートはこの実験を実行しない。** 実施は司令塔裁定 + prereg(IF-FIRST)を経ること。

### 4.6 B₄ 塔は $\tilde{\mathbf N}^*$ で閉じる

系 B4-42 の下では $\mathrm{GT}^\heartsuit(\tilde{\mathbf N}^*)=\mathfrak G_{\rm ar}$ ⟹ **より深い B₄ 窓に降りても 1 元も減らない**。委嘱③「どの下位窓集合で打ち切れるか」への回答: **$\{\tilde{\mathbf N}^*\}$ の 1 個で足りる。ただし survival の切り詰めが正当だからではなく、下界が上界に届いているからである。**

---

## 5. 委嘱④ — 計算量

### 5.1 位数見積り

| 対象 | 位数 | 表現 |
|---|---|---|
| $P=F_2/\mathcal V(F_2)$ | $7^8$ | pc 群(既在) |
| $[P,P]$ | $7^6=117{,}649$ | **pentagon 判定の宇宙**($m$ 非依存) |
| $R=PB_4/\mathcal V(PB_4)$ | $7^{41}$ | pc 群(41 生成)**※ 構築に環境ブロッカー §5.4** |
| $Q=K(0,5)/W$ | $7^{40}$ | pc 群(既在)。$R\cong C_7\times Q$ |
| $PB_4/\tilde{\mathbf N}_{\rm core}$ | $7^{8}\le\ \cdot\ \le7^{29}$ | $P^4$ の部分群(★ 付録 A.4: $\mathbb F_7$-階数 5 ⟹ 上界が $7^{32}$ から $7^{29}$ へ) |
| $PB_3/\mathbf N_0$ | $7^9$ | $P\times C_7$ |

### 5.2 1 元あたりのコストと総コスト

$D_{B_4}$ の評価 = pc 群 $R$ での準同型像 5 回 + 積 4 回 + 比較 1 回。$\Rightarrow$ 総計 $117{,}649\times9\approx10^6$ 回の collection ≒ **数分**。メモリは $O(41^2)$ 語 ⟹ 8GB 制約に無関係。GHA 可(shard 分割不要)。252 は $m$ 非依存ゆえ別コストなし。

### 5.3 費用対効果の会計 ★改

| 作業 | コスト | 得られる情報 |
|---|---|---|
| $\tilde{\mathbf N}^*$ での (2.20) 評価(工程 P2/P3) | 数分(**+ P1 のブロッカー解除**) | ★ **定理 PENT-FORM の 2 実装確認**(新規発見ではなくバグ検出器)。252 の身分は変わらない |
| $\tilde{\mathbf N}_{\rm core}$ での (2.20) 評価(**P1 不要**) | 数分 | ★ 定理 B4-VAC の実測 + **Question 4.6 の標的**(別ノートの prereg) |
| CAL-B4 較正(N⁽¹⁹⁾/N⁽³⁴⁾) | 秒〜時間 | 判定機の免許(必須先行) |
| BIT-252 決定実験(B₃ 側) | 数分 | ★ 252 の内訳が 42 側なら CLOSED |

### 5.4 ★★ 実装仕様の訂正と環境ブロッカー(v1.1 新・検分 §3.5)

> ### ★ 仕様の誤り(v1 の誤記)
> v1 §5.1/工程 P1 は $R$ の構築を「ANUPQ `Pq`(p=7, class 4)」と書いた。**これは違う群を作る。** `ClassBound` は**下方指数-$p$ 中心列** $P_1=G,\ P_{i+1}=[P_i,G]P_i^{\,p}$ に沿う切り詰めであって $\gamma_{c+1}(G)G^{p}$ ではない。
> - 反例: $G=\mathbb Z$、$p=7$ で $P_3=49\mathbb Z$ vs $\gamma_3(\mathbb Z)\mathbb Z^7=7\mathbb Z$。
> - 機械確認(検分ノート・自由群 $F_2$ のみ): `PQuotient(F2,7,2)` の位数 $=16807=7^5$、一方 $\lvert F_2:\gamma_3F_2^{\,7}\rvert=7^3$。
>
> **正しい仕様**: `Pq(F : Prime:=7, ClassBound:=4, Exponent:=7)`。
> ⚠ **誤ったままだと B4-EXQ-1(予言 $7^{41}$)が的中せず、「LCS 公式の適用ミス ⟹ STOP」という誤分岐に落ちる** — 予言体系が**実装の誤りを理論の誤りと読む**方向に働く。

> ### ★★ 環境ブロッカー(**工程 P1 は現状の工房環境で実行不能**)
> 本機の ANUPQ は外部バイナリ `pq` が動作しない。**`LoadPackage("anupq")` は `true` を返すので見落としやすい**が、`Pq(...)` は `Error, failed to find any more of line (iostream dead?)` で即死する(最小スモークでも同じ)。
> **⟹ 工程 P1 は「保留」とし、実行の前に環境修理または代替路の実装を要する。**
> **代替路(数学的に正しい・実装判断は ep-keeper / implementer)**: 指数 7・類 4 の群では $P_i=\gamma_i$ なので $P_5(G)\subseteq\gamma_5(G)G^7$。GAP ライブラリの `PQuotient(PB_4,7,4)` で $\bar G:=PB_4/P_5$ を作り、$R=\bar G/(\gamma_5(\bar G)\cdot\mathrm{Agemo}_1(\bar G))$ を取る。**中間商 $\bar G$ の大きさは未見積り**【工程要請 W-1】。
> ★ **迂回**: $\tilde{\mathbf N}_{\rm core}$ 側の計算($P^4$ の中)は **$R$ を要さない** ⟹ 工程 P1 のブロッカーを迂回して先に走れる(§5.3 の 2 行目・別ノートの prereg)。

---

## 6. 委嘱⑤ — 較正設計(T2 の B₄ 版)— v1 と同一 + 注記

### 6.1 正解データ(2008 §4.3・txt L3524–3546 逐語)

> **N⁽¹⁹⁾**: $N_{\rm ord}=6$。**$F_2/N_{F_2}$(7776 元)の中で** pentagon を満たす $fN_{F_2}$ が **216 個**。うち **36 個**だけが $m\in\{0,\dots,5\}$ で $2m+1$ が $\mathbb Z/6$ の単元かつ hexagon (2.18)(2.19) を満たす。
> **N⁽³⁴⁾**: $N_{\rm ord}=9$。**$[F_2/N_{F_2},F_2/N_{F_2}]$(254,016 元)の中で** pentagon を満たすのが **4096 個**、うち hexagon へ持ち上がるのが **243 個**。

★ **宇宙の違いに注意**(Property 4.2 strong vs 4.3 weak)。

### 6.2 較正ゲート **CAL-B4**(発火前件・必須)

| # | 項目 | 期待値 |
|---|---|---|
| **C-1** | $\psi:PB_4\to S_9$((4.3))から $\lvert PB_4:N^{(19)}\rvert$ | **216** |
| **C-2** | (2.4) で $N^{(19)}_{PB_3}$、Prop 2.3 で $N_{\rm ord}$ | **6** |
| **C-3** | $\lvert F_2:N^{(19)}_{F_2}\rvert$ / 交換子部分群 | **7776** / **216** |
| **C-4** ★ | 全 7776 元で (2.20) 検査 | **216 件 PASS** |
| **C-5** ★ | C-4 の 216 件 × $m\in\{0,2,3,5\}$ で hexagon | **36 件** |
| **C-6** | $\lvert\mathrm{GT}(N^{(19)})\rvert$ / $\lvert\mathrm{GT}^\heartsuit(N^{(19)})\rvert$ | **72** / **12**($\cong D_6$) |
| **C-7**(任意) | N⁽³⁴⁾($S_{18}$・(4.4))交換子部分群内 pentagon → hexagon | **4096** → **243** |
| **C-8** ★ | Package GT `PaB.py::penta` と自前判定の第三者突合 | 全一致 |
| **C-9** ★ | $\tilde{\mathbf N}_{\rm core}$ での (2.20) 通過数 | **117,649**(全通過)— **停止規則として運用**(PASS 報告にしない) |

**CAL-B4 が全 PASS するまで、NW(7) の B₄ 数値を 1 つも信用しない。**

---

## 7. 委嘱⑥ — 用語版差の防壁

### 7.1 対応表(2401 vs 2008)— v1 と同一

| 概念 | **2008(B₄)** | **2401(B₃-gentle)** | NW(7) での状態 |
|---|---|---|---|
| 窓 | $\mathrm{NFI}_{PB_4}(B_4)$ | $\mathrm{NFI}_{PB_3}(B_3)$ | **圏が違う**($\tilde{\mathbf N}$ vs $\mathbf N$) |
| GT-pair | hexagon×2 **+ pentagon** | hexagon×2 のみ | 差は pentagon 1 本 |
| **GT-shadow** | GT-pair + 全射 3 本 | **charming** GT-pair + 全射 | ★ **同名別物** |
| charming | $f\in[F_2,F_2]$ 代表 ∧ $T^{F_2}$ 全射 | $2m+1$ 単元 ∧ $f\in$ 商の交換子群 | ★ 本窓では同値(**CHARM-EQ**) |
| $\mathrm{GT}(N)$ / $\mathrm{GT}^\heartsuit(N)$ | 非 charming 込み / charming | (2401 の $\mathrm{GT}$ が $\mathrm{GT}^\heartsuit$ 側) | Table 1 の `|GT|` 列と 294 は**比較禁止** |
| genuine | $\widehat{GT}$ 由来 | $\widehat{GT}_{gen}$ 由来 | ★ **別概念** |

> **補題 CHARM-EQ**: NW(7) の宇宙では 2401-charming $\iff$ 2008-charming(2008 (1) $=\bar f\in[P,P]$、2008 (2) $=$ SURJ $=$ H8′ で自動)。⟹ **本窓では版差は pentagon の 1 ビットに封じ込められる。**

### 7.2 ★ LS 系との版差(v1.1 新 — 文献 pin 由来)

| 項目 | LS1994 | LS-Ptolemy | HS2000 | 工房 |
|---|---|---|---|---|
| (I) の引数順 | $f(x,y)f(y,x)=1$ | $f(y,x)f(x,y)=1$ | $f(y,x)f(x,y)=1$ | (3.10) $f\theta(f)\in N_{F_2}$ |
| (III) の形 | **2 項 = 3 項**(cocycle 形)・$\hat K_4$ 上 | 5 項積 $=1$・$\hat K(0,5)$ | 5 項積 $=1$(巡回シフト差) | (2.20) = LS1994 (III) の**左右入替** |
| 回転元 | $V=\mathrm{Inn}((\sigma_4\sigma_3\sigma_2\sigma_1)^{-3})$、$V(x_{ij})=x_{i+2,j+2}$ | $(\alpha\beta)^5=1$ | $\rho(x_{ij})=x_{i+3,j+3}$ | $\bar\rho$(HS2000 の $\rho$ 規約) |
| 向き | $V$ と $\rho$ は**互いに逆回転** | — | — | — |

> **防壁 R7(v1.1 新)**: **LS1994 の $V$ と HS2000/工房の $\rho$ は逆回転である。** $\rho^i$ の指数を LS の $V$ 由来の式から直接写さない。工房の $\mathrm{PENT}_W$ の定義は $\bar\rho^4\cdots\bar\rho\cdot\mathrm{id}$ の順で凍結済み(翻訳ノート §1.0)であり、これを唯一の正本とする。**定理 PENT-FORM は $V$/$\rho$ の向きに依存しない**(5 項の**集合**と積の順序だけを使い、回転そのものを使わないため)。

### 7.3 判定機への混入禁止規約(**R1–R7**)

| # | 規約 |
|---|---|
| **R1** | cert に **framework tag**(`FW=B4-2008` / `FW=B3-2401`)必須。タグなしの "shadow" を機械に渡さない |
| **R2** | cert に **window arity**(3/4)と**評価した方程式 ID の列**を必須。欠く cert は無効 |
| **R3** | 「genuine」は必ず添字つき($\text{genuine}_{\widehat{GT}}$ / $\text{genuine}_{\widehat{GT}_{gen}}$) |
| **R4** | 異 framework の計数を突き合わせない(Table 1 `|GT|` と 294 を並べない) |
| **R5** | $\tilde{\mathbf N}$ と $\mathbf N$ は別記号。関係は §2.6 の表が唯一の正本 |
| **R6** | 窓の「大きさ」を $\lvert PB_4:\tilde{\mathbf N}\rvert$ で語らない(律速量は $\lvert F_2:\tilde{\mathbf N}_{F_2}\rvert$) |
| **R7** ★ | LS1994 の $V$ と工房の $\rho$ は**逆回転**。回転の指数を論文間で直接写さない(§7.2) |

---

## 8. 工程表(条件付き実現可能)★全面改訂

| 工程 | 内容 | 前件 | コスト | 状態 |
|---|---|---|---|---|
| **P0** ★ | **CAL-B4 較正ゲート**(§6.2 C-1〜C-6, C-8) | なし | 秒〜分 | 実行可 |
| **P0b** | C-7(N⁽³⁴⁾) | P0 | 分〜時間 | 実行可 |
| **P1** ★改 | $R=PB_4/\mathcal V(PB_4)$ の構築 — **`Pq(F : Prime:=7, ClassBound:=4, Exponent:=7)`** | P0 | 分 | ⚠ **保留**(ANUPQ バイナリ死・§5.4。代替路 = `PQuotient`+$\gamma_5\cdot\mathrm{Agemo}_1$、中間商の見積り =【工程要請 W-1】) |
| **P2** | 5 本の $\bar\varphi:P\to R$ 構成 + $[P,P]$ 全 117,649 件で $D_{B_4}$ 評価 | P1 | 数分 | P1 待ち |
| **P3** ★改 | **層別突合**(下表)。P2 の通過集合 と lane P の $\mathrm{PENT}_W$ 通過集合 | P2 + lane P cert | — | P1 待ち |
| **P4** ★ | **C-9**($\tilde{\mathbf N}_{\rm core}$ で全通過)= 停止規則 | P0 | 分 | ★ **P1 不要・即実行可** |
| **P5** | (別軸・B₃)**BIT-252 決定実験**(§4.5) | prereg + 裁定 | 数分 | prereg 待ち |
| **P6** ★新 | (別ノート)**Question 4.6 prereg**($\tilde{\mathbf N}_{\rm core}$) | prereg + Sol 認可(便 112 後) | 分 | **走らせない** |

### 8.1 ★ 工程 P3 の層別設計(検分 要修正 8)

| 層 | 定義 | 事前予言 | 不一致時 |
|---|---|---|---|
| **S0** | $[P,P]$ 全件(117,649) | **予言しない**(定理 PENT-FORM の前件 (I) が無い層) | **STOP にしない**(探索的情報として記録のみ) |
| **S1** | (3.10) $f\theta(f)\in N_{F_2}$ を満たす $\bar f$ | ★ **完全一致**(**系 PENT-EQ = 定理**) | **IMPLEMENTATION_BUG / STOP** |
| **S2** | full hexagon 通過($\subseteq S_1$。$m$ を伴う) | ★ **完全一致**(S1 の部分) | 同上 |

> **一致/不一致の判定は S1・S2 でのみ行う。** S1 の層自体($\lvert S_1\rvert$)は本走の副産物として既に得られている可能性があるが、**得られていなければ (3.10) 単独の評価を先に行う**(コスト = 117,649 件の 1 述語)。

### 8.2 事前登録する予言(IF-FIRST・**発火前に凍結**)★改

| ID | 予言 | 格 | 分岐 |
|---|---|---|---|
| **B4-EXQ-1** | $\lvert R\rvert=7^{41}$(**`Exponent:=7` 付きの仕様で**) | **T\*** | 不一致 ⟹ **まず実装仕様を疑う**(§5.4)。理論の誤りと読まない |
| **B4-EXQ-2** | $R\cong C_7\times Q$、$\lvert Q\rvert=7^{40}$ | **T\*** | 同上 |
| **B4-EXQ-3** | $\tilde{\mathbf N}^*_{PB_3}=\mathbf N_0$ | **T** | 実装バグ検出器 |
| **B4-EXQ-4** ★改 | **単位を統一**: 層 **S2** 上で、(2.20) mod $\tilde{\mathbf N}^*$ を満たす **shadow $(m,\bar f)$ の個数** $=$ $\mathrm{PENT}_W$ を満たす shadow の個数 $=$ **42**。さらに層 **S1** 上で **$\bar f$ の集合として完全一致** | **T**(定理 PENT-FORM の帰結 = **バグ検出器**) | **(a)** 一致 ⟹ 2 実装一致(CV-9 判読へ)/ **(b)** S1 または S2 で不一致 ⟹ **実装または規約の誤り**(理論の新発見と読まない)。⚠ **v1 の分岐 (c)「新類の発見」は削除**(S0 の不一致は理論的に予期されるものであり、発見ではない) |
| **B4-EXQ-5** | CAL-B4: 216/36・4096/243 | **T**(公表値・**バグ検出器**) | 不一致 ⟹ STOP |
| **B4-EXQ-6** | $\tilde{\mathbf N}_{\rm core}$ での (2.20) 通過数 $=117{,}649$ | **T**(定理 B4-VAC) | 不一致 ⟹ 実装 STOP |
| **B4-EXQ-7** | BIT-252: $\mathfrak G^{\rm gentle}_{\rm genuine}\in\{42,294\}$ | **T\*** | 中間値 ⟹ 前件(isolated/294/42)のどれかが偽 ⟹ STOP |
| **B4-EXQ-8** ★新 | $\lvert PB_4:\tilde{\mathbf N}_{\rm core}\rvert$ は $7^{8}$ 以上 $7^{29}$ 以下($\mathbb F_7$-階数 5・付録 A.4) | **T\*** | 範囲外 ⟹ 実装 STOP |

★ **格 T の予言は的中しても情報量ゼロ。バグ検出器としてのみ運用する。** ★ **v1.1 で B4-EXQ-4 は格 C → 格 T に降格した**(定理 PENT-FORM が閉じたため、これはもう「発見」ではない)。

---

## 9. 格付け・【GAP】・規律申告

### 9.1 読んだ範囲の申告

- `papers/txt/2008.00066-*.txt`: **L2563–2610 / L2638–2660 / L3516–3546 / L3548–3581** および Table 1 の数値ブロック。**原文頁画像は本ノートでは 1 枚も開いていない。**
- **LS1994 / LS-Ptolemy / HS2000 の原文は 1 頁も開いていない。** 本ノートの LS 由来の事実はすべて **pin ノート `docs/scout/ls_pentagon_term_correspondence_v1.md`(reader が頁画像照合済)からの引用**である(A-1 / A-2 / A-3 / A-5 / 版差台帳)。⟹ **格は「文献相対」**(§9.4)。
- 外部文献の自主検索は**ゼロ**。

### 9.2 【GAP】一覧 ★改

| 札 | 内容 | 状態 |
|---|---|---|
| **【GAP-B4-1】** | (2.20) と $\mathrm{PENT}_W$ の項対応 | ★★ **CLOSED(紙)** — 定理 PENT-FORM(§3.2)。**HS2000 Prop 7 は不使用**。1a(各段の書き下し)= 本ノートで実施済 / 1b(逆向き)= **全段が等式代入ゆえ可逆** / 1c((II) 非使用)= **証明が (II) を一度も使わない**ことを明示 ⟹ 3 つとも閉。**ただし格は「文献相対」**(下記【GAP-B4-1′】) |
| ★ **【GAP-B4-1′】**(新・格の限定) | 定理 PENT-FORM は **LS-(4)(球面関係)と LS-(abs)(中心元吸収)を pin ノート経由で引用**しており、原文頁画像を本起草者は見ていない。また **LS1994 (III) = 2008 (2.20) の逐語同一性**も pin と検分の突合に依拠 | **文献相対**。閉じるには (i) 司令塔/reader による「(4) と p.13 注意」の**再照合**、または (ii) 球面群 $K(0,5)$ の表示から $x_{45}=\varphi_{123}(c)$・$x_{15}=\varphi_{234}(c)$ を**自前で導出**(Hurwitz 関係 $x_{14}x_{24}x_{34}x_{45}=1$ と $\Delta^2=1$ から。見積り: 紙 1 頁)。**【文献要請 B4-L1 は取り下げ、代わりに B4-L1′(下記)を起票**する |
| **【GAP-B4-2】** | practical でない 2008 GT-shadow の存否(原論文 p.23 で未解決) | **UNKNOWN(原論文由来)**。系 B4-42 は practical 制限つき。Table 1 も practical(§4 脚注 5) |
| **【GAP-B4-3】** | Cor 3.13 の survival 減少列の**停止点に有効上界がない** | **UNKNOWN**。【文献要請 B4-L2】(継続) |
| **【GAP-B4-4】** | 工程 P3 の突合に要する $[P,P]$ の共通ラベル付け(CV-9 危険)。**層 S1/S2 の定義自体も両実装で一致していなければならない** | **処方**: 同値試験は同一プロセス・同一列挙で。発見用の数値は既存 lane P cert を正本とし、P3 は**仕様同一性試験**として位置づける。falsifier の CV-9 判読を必須前件に。**単位欄($f$ 集合 / shadow 集合)を cert に追加** |
| ~~【GAP-B4-5】~~ | BIT-252 の前件「$K$ も isolated」 | ★ **CLOSED**(§4.4 — 証明経路の変更で**不要**、かつ独立に**充足**も確認) |
| ★ **【工程要請 W-1】**(新) | ANUPQ 代替路(`PQuotient(PB_4,7,4)` → $\gamma_5\cdot\mathrm{Agemo}_1$)の**中間商 $\bar G$ の位数見積り**と 8GB 内での実行可否 | **未見積り**。ep-keeper / implementer へ |

### 9.3 【文献要請】

> ### 【文献要請 B4-L1′】(B4-L1 を差し替え・**優先度低**)
> **困難**: 定理 PENT-FORM が引用する 2 つの群論的事実の**原文再照合**。
> **欲しい結果の型**: (i) LS1994 **p.7 の関係 (4)**($\bar x_{45}=\bar x_{12}\bar x_{13}\bar x_{23}$、$\bar x_{15}=\bar x_{23}\bar x_{24}\bar x_{34}$)と、(ii) LS1994 **p.13**(lemma 5 直前)の中心元吸収 $f(\gamma\alpha,\beta)=f(\alpha,\gamma\beta)=f(\alpha,\beta)$ の逐語。
> **状態**: pin ノートが**既に頁画像照合済**と記載(A-2)。⟹ **本要請は「起草者が原文を見ていない」ことの明示にすぎず、走行のブロッカーではない**。代替として §9.2 の (ii)(自前導出)でも閉じる。

> ### 【文献要請 B4-L2】(継続・非緊急)
> Cor 3.13 の survival 減少列の**停止点の有効上界**。profinite 群の有限商族に対する Mittag-Leffler の有効版。**無いなら「無い」で確定させたい**(その場合サンドイッチが唯一の道と記帳できる)。

### 9.4 格付け ★改

| 対象 | 格 |
|---|---|
| 補題 **B4-FORGET** | **paper-proof** |
| ★ 補題 **CORE-4** | **paper-proof**(生成元上の厳密計算 6×3。**検分ノート由来** — 起草は検分者、本ノートは採録) |
| 補題 **B4-IND** | **paper-proof**(付録 A.1 の完全表で機械確認済) |
| ★ 定理 **B4-VAC** | **paper-proof**(**別人格の独立再導出で PASS** — 検分 §2)。**Sol 未監査** |
| ★ 定理 **B4-CANON** | ★ **paper-proof**((4) を (3)+既在実測 $\lvert Q\rvert=7^{40}$ 経由に変更し candidate から格上げ)。**別人格の独立再導出で PASS**。**Sol 未監査** |
| 補題 **B4-MONO** / 定理 **B4-DIR** | **paper-proof**((c) は検分 §3.3 が独立検証) |
| ★★ 定理 **PENT-FORM** / 系 **PENT-EQ** | ★ **paper-proof(文献相対)** — 引用する群関係は pin ノート経由(【GAP-B4-1′】)。**Sol 未監査** |
| 補題 **B4-KAPPA** | **paper-proof candidate**(2401 Prop 3.4 と独立に同結論。`cross-checked` は付さない) |
| ★ 系 **B4-42** | **conditional candidate**((H1)–(H5) 相対・とくに BH-α-pent 相対) |
| ★ 命題 **BIT-252** | ★ **paper-proof**(証明経路を「像 = 部分群」に短縮し前件を削減。前件 = 294/42 の測定相対は継承)。**別人格の独立再導出で 4 段 PASS** |
| 補題 **CHARM-EQ** | **paper-proof**(H8′ 相対) |
| `verified` | ✗(Lean 未使用) |
| `cross-checked` | ✗(CV-9 判読未実施。検分ノートは「別人格による独立再導出」であって二系統**実装**の一致ではない) |
| **novelty** | ★ **主張しない**。系 B4-42 の Q4.7 該当性も、別ノートの Q4.6 標的も、**先行の有無は未調査**。主張するなら司令塔の novelty ゲートを先に通すこと |

### 9.5 規律申告

- ★ **本走宇宙(705,894 対)の候補を 1 件も評価していない。** GAP も pc 群も起動していない。機械は付録 A の python のみ(記号語計算・整数級数・$\mathbb F_7$ 線型代数)。
- **封印 3 量非接触。既在文書を 1 バイトも改変していない**(**v1 を含む** — v1.1 は並置)。
- ★ **HS2000 Prop 7 を使用していない**(罠 D-5 遵守。司令塔の使用禁止指示を逐語履行)。$\widehat{GT}$ の使用は 2008 の定義・Cor 3.13・Thm 3.8 と HSP-SOUND のみ。
- **新しい停止規則を発効させない**(§6.2 C-9・§8.1・§8.2 は提案。発効は司令塔裁定 + Sol ゲート)。

---

## 10. Sol への監査点(5 点)★改

> **Q-1 ★★ 補題 CORE-4**(§2.2)。$\mathrm{core}_{B_4}(p_4^{-1}(N))=\bigcap_ip_i^{-1}(N)$ を、代表元 $1,\sigma_3,\sigma_2\sigma_3,\sigma_1\sigma_2\sigma_3$ と「$p_4c_{\sigma_3^{-1}}=p_3$ 等が 6 生成元すべてで厳密一致」で示した一段。

> **Q-2 ★★ 定理 B4-CANON (2) の厳密等号**(§2.5)。**5 本の余面のうち $\varphi_{123}$ 1 本が分裂単射であれば残り 4 本を見なくてよい**、という論法の可否。

> **Q-3 ★★★ 定理 PENT-FORM**(§3.2)。段 A/B/C の 3 段(とくに**段 C が両スロットに同じ $\gamma=x_{23}^{-1}$ を出し、$f\in[F_2,F_2]$ の指数和ゼロで消える**こと)に穴がないか。および **(II) を一度も使っていない**ことの確認。**HS2000 Prop 7 を使わない**方針(lift 量化子 = 罠 D-5 の回避)を承認するか。

> **Q-4 ★★ 系 PENT-EQ の層**(§3.2 末・§8.1)。同値を **$S_1$((3.10) 充足域)以上でのみ**登録し、$S_0$ の不一致を STOP にしない設計を認めるか。登録層は $S_1$ と $S_2$ のどちらを正とすべきか。

> **Q-5 ★★ 命題 BIT-252 の短縮経路**(§4.4)。$\mathfrak G^{\rm gentle}_{\rm genuine}=\mathrm{im}(\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N))$(2401 Def 4.2)で閉性を 1 行にし、前件「$K$ も isolated」を落とす改訂。および系の言明を「**$\widehat{GT}\to\widehat{GT}_{gen}$ は全射でない**」に精密化する訂正。

---

## 11. ★ v1 → v1.1 差分表(全件)

| # | 箇所 | 種別 | 内容 | 出所 |
|---|---|---|---|---|
| 1 | §2.2 | **証明の追加** | 補題 **CORE-4** を挿入($B_4$-核の well-definedness) | 検分 要修正 1 / 裁定 608-1 |
| 2 | 付録 A.1 | **提示の修正** | 表を $x_{13}$・$c$ 込みの完全印字へ。12 本すべてで $\lambda(c)\ne1$ を明示。「総合して」→「各本が単独で十分」 | 検分 要修正 2 / 裁定 608-1 |
| 3 | §0-2 / §2.4 / §2.6 | **射程の訂正** | 「Prop 3.9 の持ち上げ窓」→「構成に現れる 2 窓」。反例の舞台 = $\tilde{\mathbf N}_{\rm core}$ と明記。$\ker\tilde\psi$ は 2008 の窓でないと注記 | 検分 要修正 3 / 裁定 608-1 |
| 4 | §5.4 / 工程 P1 | **仕様の訂正 + ブロッカー** | `Pq(... Exponent:=7)`。ANUPQ バイナリ死 ⟹ **P1 保留**・代替路・【工程要請 W-1】 | 検分 要修正 4 / 裁定 608-3 |
| 5 | §3.2 | ★★ **新定理** | **PENT-FORM**(段 A/B/C)+ 系 **PENT-EQ**。【GAP-B4-1】紙閉鎖。**HS2000 Prop 7 不使用** | 文献 pin + 裁定 608-2 |
| 6 | §4.4 | **証明経路の短縮** | 「像 = 部分群」1 行へ。前件「$K$ も isolated」削除 | 検分 要修正 5 |
| 7 | §4.4 | **抜けの補完** | $\bigcap$ を isolated $K$ に限る場合の cofinality(2401 Prop 3.14)注記 | 検分 要修正 6 |
| 8 | §4.4 系 | **言明の精密化** | 「$\widehat{GT}_{gen}\supsetneq\widehat{GT}$」→「$\widehat{GT}\to\widehat{GT}_{gen}$ は全射でない」 | 検分 要修正 7 / 裁定 608-3 |
| 9 | §8.1 / §8.2 | ★ **設計の改訂** | P3 を **S0/S1/S2 層別**へ。B4-EXQ-4 の**単位統一**($f$ 集合 vs shadow 集合)。**分岐 (c) を削除**(偽アラーム)。B4-EXQ-4 を格 C → **格 T** へ降格 | 検分 要修正 8 / 裁定 608-3 |
| 10 | §9.2 | **GAP の更新** | 1 = CLOSED、1′ = 新設(文献相対)、5 = CLOSED、W-1 = 新設 | 検分 要修正 9/10 |
| 11 | §2.5 / §9.4 | **格上げ** | B4-CANON (4) を (3)+既在実測経路で **paper-proof** へ。BIT-252 も paper-proof へ | 検分 要修正 11 |
| 12 | §7.2 / R7 | **新規防壁** | LS の $V$ と工房の $\rho$ は**逆回転** — 指数を論文間で写さない | 文献 pin 版差台帳 |
| 13 | §2.2 / §5.1 / A.4 | **数値の精密化** | $Z(PB_4)\le\tilde{\mathbf N}_{\rm core}$、$\mathbb F_7$-階数 5 ⟹ $\lvert PB_4:\tilde{\mathbf N}_{\rm core}\rvert\le7^{29}$(v1 は $7^{32}$)。B4-EXQ-8 新設 | 本ノート(付録 A.4) |
| 14 | 工程 P4 / P6 | **工程の追加** | P4($\tilde{\mathbf N}_{\rm core}$ の C-9)は **P1 不要で即実行可**。P6 = Question 4.6 prereg(**別ノート**) | 検分 §7 / 裁定 608-4 |

**v1 の主張で撤回したものはない。** 変更はすべて (a) 証明の補完 (b) 射程・言明の精密化 (c) 実装仕様の訂正 (d) 突合設計の改訂 (e) 新定理の追加 である。

---

## 付録 A. 機械検算(**本走非接触**・記号計算・整数級数・$\mathbb F_7$ 線型代数のみ)

### A.1 ★ 20 本の合成 $\psi\circ p_i\circ\varphi$ — **完全印字**($x_{12},x_{23},x_{13},c$)

スクリプト `scratchpad/b4comp2.py`(v1 の `b4comp.py` を $x_{13},c$ 列込みに拡張)。

```
=== 20 composites  psi o p_i o phi   (images of x12, x23, x13, c) ===
  p_4 o phi123     : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_4 o phi234     : x12->y        x23->1        x13->1        c->y         CYCLIC-IMAGE (degenerate), <y>
  p_4 o phi12_3_4  : x12->x^-1     x23->1        x13->1        c->x^-1      CYCLIC-IMAGE (degenerate), <x>
  p_4 o phi1_23_4  : x12->y^-1     x23->1        x13->1        c->y^-1      CYCLIC-IMAGE (degenerate), <y>
  p_4 o phi1_2_34  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_3 o phi123     : x12->x        x23->1        x13->1        c->x         CYCLIC-IMAGE (degenerate), <x>
  p_3 o phi234     : x12->1        x23->1        x13->y        c->y         CYCLIC-IMAGE (degenerate), <y>
  p_3 o phi12_3_4  : x12->1        x23->1        x13->x^-1     c->x^-1      CYCLIC-IMAGE (degenerate), <x>
  p_3 o phi1_23_4  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_3 o phi1_2_34  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_2 o phi123     : x12->1        x23->1        x13->x        c->x         CYCLIC-IMAGE (degenerate), <x>
  p_2 o phi234     : x12->1        x23->y        x13->1        c->y         CYCLIC-IMAGE (degenerate), <y>
  p_2 o phi12_3_4  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_2 o phi1_23_4  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_2 o phi1_2_34  : x12->1        x23->1        x13->y^-1     c->y^-1      CYCLIC-IMAGE (degenerate), <y>
  p_1 o phi123     : x12->1        x23->x        x13->1        c->x         CYCLIC-IMAGE (degenerate), <x>
  p_1 o phi234     : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_1 o phi12_3_4  : x12->x        x23->y        x13->x^-1y^-1 c->1         = psi
  p_1 o phi1_23_4  : x12->1        x23->x^-1     x13->1        c->x^-1      CYCLIC-IMAGE (degenerate), <x>
  p_1 o phi1_2_34  : x12->1        x23->y^-1     x13->1        c->y^-1      CYCLIC-IMAGE (degenerate), <y>
  totals: psi = 8 , degenerate = 12

  NOTE: every degenerate row has lambda(c) != 1  => each single row already forces k = 0 mod 7
        on w = f*c^k with f in V(F2).  (lemma B4-IND)

=== consistency check: p_4 o phi123 = id on PB3 (split retraction) ===
   images of (x12,x23,x13,c) under p_4 o phi123 = ['x12', 'x23', 'x13', 'x12/x13/x23']
```

★ **v1 の表との差**: 4 本($p_3\varphi_{234}$, $p_3\varphi_{12,3,4}$, $p_2\varphi_{123}$, $p_2\varphi_{1,2,34}$)は $x_{12},x_{23}$ 列だけ見ると「$1,1$」だが、**$x_{13}$ と $c$ の上で非自明**である。補題 B4-IND の結論は $\lambda(c)\ne1$ にこそ依存する。

### A.2 pentagon の恒真性(定理 B4-VAC)— v1 と同一

```
  coord i=4 :  LHS = f(x,y)   RHS = f(x,y)   -> IDENTITY (no pentagon content)
  coord i=3 :  LHS = f(x,y)   RHS = f(x,y)   -> IDENTITY (no pentagon content)
  coord i=2 :  LHS = f(x,y)   RHS = f(x,y)   -> IDENTITY (no pentagon content)
  coord i=1 :  LHS = f(x,y)   RHS = f(x,y)   -> IDENTITY (no pentagon content)
```

### A.3 LCS 階数(独立検算・$\lvert Q\rvert=7^{40}$ の紙側再現)

`scratchpad/lcs.py`。$\prod_k(1-t^k)^{\phi_k}=\prod_{i=1}^{n-1}(1-it)$。

```
PB_4 LCS ranks (deg1..6): [6, 4, 10, 21, 54, 125]   sum(k<=4) = 41
PB_3 LCS ranks (deg1..6): [3, 1, 2, 3, 6, 9]        sum(k<=4) = 9   (|P| = 7^8)
K(0,5) = PB4/Z  => ranks [5, 4, 10, 21]             sum = 40        (|Q| = 7^40, NW-P4)
Witt(2,k) k=1..5: [2, 1, 2, 3, 6]                   sum = 14        (|P'| = 7^14, §4.5)
```

### A.4 ★ $\tilde{\mathbf N}_{\rm core}$ の指数の絞り込み(v1.1 新)

`scratchpad/core_rank.py`。6 生成元の $(P^{\rm ab})^4=\mathbb F_7^8$ での像の階数。

```
x12 [0, 0, 0, 0, 1, 0, 1, 0]
x13 [0, 0, 1, 0, 0, 0, 6, 6]
x14 [0, 0, 6, 6, 6, 6, 0, 0]
x23 [1, 0, 0, 0, 0, 0, 0, 1]
x24 [6, 6, 0, 0, 0, 1, 0, 0]
x34 [0, 1, 0, 1, 0, 0, 0, 0]
F_7-rank of abelianized image = 5
=> |image in (P^ab)^4| = 7^5 ; |(P^ab)^4| = 7^8
=> |PB4 : N_core| divides 7^5 * (7^6)^4 = 7^29
   crude lower bound: >= |P| = 7^8 (each coordinate onto)
```

★ **階数が 6 でなく 5 であることの意味**: 6 行の和が $\equiv0$、すなわち $\Delta^2=\prod_{i<j}x_{ij}$ の像がゼロ。これは $p_i(\Delta^2)=c$ と $\psi(c)=1$ の帰結であり、**$Z(PB_4)\le\tilde{\mathbf N}_{\rm core}$**(§2.2 の付随事実)を機械側から裏づける。
