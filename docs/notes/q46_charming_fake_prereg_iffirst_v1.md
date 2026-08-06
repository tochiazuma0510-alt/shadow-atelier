# 2008.00066 **Question 4.6**(charming ∧ fake GT-shadow の実例)— 事前登録票 v1(**IF-FIRST 凍結**)

**状態札: `candidate(事前登録票・紙のみ / 機械実行ゼロ / 本走宇宙の候補評価ゼロ / 封印非接触 / novelty = 「文献上未解答・初例候補」— 発効主張はしない)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-06
- 委嘱: 司令塔(**裁定 608-4** + 追加材料)— 「検分者 §7 の候補回答を IF-FIRST 事前登録票として起草せよ。**走らせない**(Sol 認可 = 便 112 後)」
- 入力正本(すべて既在・本票は 1 バイトも改変しない):
  - `docs/notes/b4_direct_adjudication_feasibility_v1_1.md`(以下 **本体 v1.1**)— 定理 B4-VAC / CORE-4 / B4-IND / PENT-FORM / B4-CANON
  - `docs/notes/b4_theorem_check_v1.md`(検分ノート)§7 観察 **Q46-CAND**(本票の原案)
  - `docs/scout/ls_pentagon_term_correspondence_v1.md`(文献 pin)
  - **`docs/scout/q46_citation_sweep_v1.md`(引用掃引・commit `06484af`)— novelty 節の唯一の根拠**
  - `docs/notes/hs_prop7_translation_v1.md`(HSP-SOUND・定義 NW(7)・HSP-T)/ `docs/notes/hsp7_hexagon_arbitration_v1.md`(2401 Prop 3.4 逐語)/ `docs/notes/nw7_mainrun_predictions_iffirst_v1.md`(本走の 294/42/252)
- ★ **本票は走らせない。** 発火は **Sol 認可(便 112 以降)+ 司令塔裁定 + CAL-B4 全 PASS** の 3 条件。

---

## 0. 票の性格と拘束(先に 6 行)

| # | 拘束 |
|---|---|
| **0-1** | ★ **本票は機械を 1 度も走らせていない。** 記載の数値はすべて紙の導出か、**既に確定・Sol 検収済みの本走測定値**(294 / 42 / 252)である。**これが IF-FIRST の意味である。** |
| **0-2** | 本票は**発火より前に単独コミットされねばならない**(裁定 543 恒久規則)。 |
| **0-3** | 予言は **Q46-P1〜P7** の 7 本。各々に**格**と**登録済み分岐**を付す。 |
| **0-4** | ★ **格 T の予言は的中しても情報量ゼロ**。**バグ検出器**として運用する(票 v1 §0-4 の規律を継承)。 |
| **0-5** | ★ **novelty は「文献上未解答・初例候補」という格でのみ書く**(§7)。**「初例である」という発効主張はしない** — 発効は prereg + Sol ゲート + 司令塔の novelty ゲート通過後。 |
| **0-6** | ★★ **番号混同の禁止**: 本票の標的は **Question 4.6**(charming ∧ fake の実例)である。**Question 4.7**(非 Abelian 窓で genuine を全同定)は**別の問い**であり、掃引ノートによれば **2405.11725 が解決したのは Q4.7 の gentle 版であって Q4.6 ではない**。**全文書・全 cert・全報告で 4.6 と 4.7 を混ぜない**(§7.2 の防壁 R-Q1)。 |

---

## 1. 標的(逐語)

`docs/scout/q46_citation_sweep_v1.md` §① が原文から取得した逐語:

> **Question 4.6** Is it possible to find $K, N \in \mathrm{NFI}_{PB_4}(B_4)$ such that $K \le N$ and the natural map
> $\mathrm{GT}^\heartsuit(K) \to \mathrm{GT}^\heartsuit(N)$ is not onto? In other words, can one produce an example of a charming GT-shadow that is also fake?

★ **問いの型は「存在」である。** ゆえに **practical 制限(【GAP-B4-2】)は答えを弱めない** — practical な shadow も shadow だからである(個数の主張だけが practical 限定になる)。

---

## 2. 窓の定義(**凍結** — 後から変えない)

### 2.1 主窓 $\mathbf N$(既在・再定義しない)

$$\mathbf N=\mathcal V(F_2)\times\langle c\rangle,\quad \mathbf N_0=\mathcal V(PB_3)=\mathcal V(F_2)\times\langle c^{7}\rangle,\quad N_{F_2}=\mathcal V(F_2)=\gamma_5(F_2)F_2^{\,7},$$
$$P=F_2/N_{F_2}\ (\lvert P\rvert=7^8),\qquad [P,P]\ (7^6=117{,}649),\qquad \mathcal X_{\mathbf N}\ (6\ \text{元}).$$

### 2.2 ★ 標的の $B_4$ 窓 $\tilde{\mathbf N}_{\rm core}$(本票の主役)

$\psi:PB_3\twoheadrightarrow P$($x_{12}\mapsto x,\ x_{23}\mapsto y,\ x_{13}\mapsto x^{-1}y^{-1}$、$\ker\psi=\mathbf N$)、$p_i:PB_4\twoheadrightarrow PB_3$ を第 $i$ の紐を忘れる射(残る 3 本を**順序保存**で $1,2,3$ に付け替え)とする。

$$\boxed{\ \tilde{\mathbf N}_{\rm core}\ :=\ \bigcap_{i=1}^{4}\ker(\psi\circ p_i)\ =\ \bigcap_{i=1}^{4}p_i^{-1}(\mathbf N)\ =\ \mathrm{core}_{B_4}\bigl(\ker\tilde\psi\bigr)\ }$$

($\tilde\psi=\psi\circ p_4$ は 2008 **Prop 3.9** の延長そのもの = 本体 v1.1 補題 **B4-FORGET**。最後の等号 = 本体 v1.1 補題 **CORE-4**。)

**機械表現**(これが計算の全部): $PB_4/\tilde{\mathbf N}_{\rm core}\hookrightarrow P^4$ で、6 生成元の像は

| $PB_4$ 生成元 | $p_1$ 座標 | $p_2$ 座標 | $p_3$ 座標 | $p_4$ 座標 |
|---|---|---|---|---|
| $x_{12}$ | $1$ | $1$ | $x$ | $x$ |
| $x_{13}$ | $1$ | $x$ | $1$ | $x^{-1}y^{-1}$ |
| $x_{14}$ | $1$ | $x^{-1}y^{-1}$ | $x^{-1}y^{-1}$ | $1$ |
| $x_{23}$ | $x$ | $1$ | $1$ | $y$ |
| $x_{24}$ | $x^{-1}y^{-1}$ | $1$ | $y$ | $1$ |
| $x_{34}$ | $y$ | $y$ | $1$ | $1$ |

★ **$P$(既在の $7^8$ pc 群)を 4 つ並べるだけで実装できる。** $R=PB_4/\mathcal V(PB_4)$($7^{41}$・ANUPQ 必要)は**不要** ⟹ **本体 v1.1 の工程 P1 の環境ブロッカー(ANUPQ バイナリ死)を迂回して走れる。**

### 2.3 副窓 $\tilde{\mathbf N}^*$(Q4.6 の対の片割れ・**紙のみ・本走で構築しない**)

$$\tilde{\mathbf N}^*:=\mathcal V(PB_4)=\gamma_5(PB_4)PB_4^{\,7}\qquad(\text{本体 v1.1 定理 \textbf{B4-CANON}}).$$

> ### 補題 **PAIR**($\tilde{\mathbf N}^*\le\tilde{\mathbf N}_{\rm core}$ かつ両者は同じ $B_3$ 窓を誘導する)
> **(1)** $p_i(\mathcal V(PB_4))\subseteq\mathcal V(PB_3)=\mathbf N_0\subseteq\mathbf N$($p_i$ は準同型・verbal は verbal に写る)⟹ $\mathcal V(PB_4)\subseteq p_i^{-1}(\mathbf N)$ が全 $i$ ⟹ $\boxed{\tilde{\mathbf N}^*\le\tilde{\mathbf N}_{\rm core}}$。
> **(2)** $(\tilde{\mathbf N}^*)_{PB_3}=\mathbf N_0$(B4-CANON (2))かつ $(\tilde{\mathbf N}_{\rm core})_{PB_3}=\mathbf N_0$(B4-IND)⟹ $\boxed{\textbf{両窓は同一の }B_3\textbf{ 窓 }\mathbf N_0\textbf{ を誘導する}}$。
> **(3)** ゆえに 2008 (2.17) の座標系 $(m+7\mathbb Z,\ f\mathbf N_0)\in\mathbb Z/7\times PB_3/\mathbf N_0$ は**両窓で同一**であり、自然な射 $\mathrm{GT}^\heartsuit(\tilde{\mathbf N}^*)\to\mathrm{GT}^\heartsuit(\tilde{\mathbf N}_{\rm core})$ は**ラベル上の恒等写像**、すなわち**部分集合の包含**である。
> **(4)** 両窓の差は**ちょうど pentagon (2.20) の課し方だけ**である((2)(3) と、GT-pair の定義が hexagon 2 本 + pentagon 1 本であることから)。∎

★ **(3)(4) が本票の設計の心臓である**: Q4.6 が問う写像 $\mathrm{GT}^\heartsuit(K)\to\mathrm{GT}^\heartsuit(N)$ が、この対では**集合の包含**になるので、非全射性は「差集合が空でない」ことに帰着する。

---

## 3. ★★ 系間移送(**委嘱の指定箇所** — CORE-4 と同じ精度で)

本票の主張は「**$B_3$-gentle 系での測定(本走の 294 / 252)が、$B_4$ 系の窓 $\tilde{\mathbf N}_{\rm core}$ における charming ∧ fake の判定に転写される**」である。移送は 5 段に分解でき、各段を明示する。

### 3.1 ★ 補題 **XFER-0**(**可視量の一致** — 移送の土台)

> ### 補題 XFER-0
> $$\mathbf N\cap F_2\;=\;\mathbf N_0\cap F_2\;=\;(\tilde{\mathbf N}_{\rm core})_{F_2}\;=\;(\tilde{\mathbf N}^*)_{F_2}\;=\;\mathcal V(F_2)\;=\;N_{F_2}.$$
> すなわち **4 つの窓はいずれも $f$ を同じ精度 $P=F_2/\mathcal V(F_2)$ でしか見ない**。
> **証明.** $\mathbf N=\mathcal V(F_2)\times\langle c\rangle$、$\mathbf N_0=\mathcal V(F_2)\times\langle c^7\rangle$ は $F_2\times\langle c\rangle$ の**箱型**部分群ゆえ $(A\times B)\cap(F_2\times1)=A\times1$(補題 NW-1a・NW-1b (2))。$(\tilde{\mathbf N}_{\rm core})_{PB_3}=(\tilde{\mathbf N}^*)_{PB_3}=\mathbf N_0$(補題 B4-IND / 定理 B4-CANON (2))ゆえ $F_2$ との交わりも $\mathcal V(F_2)$。∎
>
> ### ★ 系 XFER-0′($\mathrm{PENT}_W$ の値は 4 窓で同一)
> $\mathrm{PENT}_W$ は定義 HSP-T により **$\bar f\in P$ のみの関数**である(許容窓の条件 (W-c) $j(N_{F_2})\subseteq W$ が well-definedness を与える。翻訳ノート §1.3)。XFER-0 より、$\mathbf N$ の shadow・$\tilde{\mathbf N}_{\rm core}$ の shadow・$\tilde{\mathbf N}^*$ の shadow は**同一の $\bar f$ を持つ** ⟹ $\mathrm{PENT}_W$ の値は 3 者で同一。
> ⟹ **本走で測った 252 件の $\mathrm{PENT}_W$-FAIL は、$\tilde{\mathbf N}_{\rm core}$ の shadow についての事実として、そのまま読める。**

### 3.2 補題 **XFER-1**(窓の実在 — $\tilde{\mathbf N}_{\rm core}\in\mathrm{NFI}_{PB_4}(B_4)$)

> **(1)** $\tilde{\mathbf N}_{\rm core}=\bigcap_i\ker(\psi p_i)$ は準同型の核の有限交わりゆえ $PB_4$ の有限指数部分群。
> **(2)** $B_4$-正規性: 補題 **CORE-4**(本体 v1.1 §2.2)が $\mathrm{core}_{B_4}(p_4^{-1}(\mathbf N))=\bigcap_ip_i^{-1}(\mathbf N)$ を示す。核は定義から $B_4$-正規。
> **(3)** $\tilde{\mathbf N}_{\rm core}\le PB_4$ ✓。
> **(4)** $(\tilde{\mathbf N}_{\rm core})_{PB_3}=\mathbf N_0$(補題 **B4-IND** — 20 本の合成の 8/12 分解、退化 12 本すべてで $\lambda(c)\ne1$)。
> **(5)** $(\tilde{\mathbf N}_{\rm core})_{\rm ord}=\mathrm{lcm}\bigl(\mathrm{ord}(x_{12}\mathbf N_0),\mathrm{ord}(x_{23}\mathbf N_0),\mathrm{ord}(c\mathbf N_0)\bigr)=\mathrm{lcm}(7,7,7)=7$(**Prop 2.3**、$PB_3/\mathbf N_0\cong P\times C_7$)⟹ $\mathcal X_{\tilde{\mathbf N}_{\rm core}}=\mathcal X_{\mathbf N}$(6 層)。∎

### 3.3 ★ 補題 **XFER-2**(**hexagon の逐語同一性**)— 2 段に分ける

**段 (a) 方程式の同一性**(群を指定する前の、$B_3$ の中の等式として):
2008 (2.18)(2.19) に $x_{12}=\sigma_1^2$, $x_{23}=\sigma_2^2$ と (A.5) の $x_{13}x_{23}=x_{12}^{-1}c$、$x_{12}x_{13}=x_{23}^{-1}c$ を代入すると

| 2008 | 代入後 | 2401 |
|---|---|---|
| (2.18) $\ \sigma_1x_{12}^mf^{-1}\sigma_2x_{23}^mf\equiv f^{-1}\sigma_1\sigma_2(x_{13}x_{23})^m$ | $\sigma_1^{2m+1}f^{-1}\sigma_2^{2m+1}f\equiv f^{-1}\sigma_1\sigma_2x_{12}^{-m}c^{m}$ | **(3.3) と逐語一致** |
| (2.19) $\ f^{-1}\sigma_2x_{23}^mf\,\sigma_1x_{12}^m\equiv\sigma_2\sigma_1(x_{12}x_{13})^mf$ | $f^{-1}\sigma_2^{2m+1}f\,\sigma_1^{2m+1}\equiv\sigma_2\sigma_1x_{23}^{-m}c^{m}f$ | **(3.4) と逐語一致** |

($\sigma_1x_{12}^m=\sigma_1\sigma_1^{2m}=\sigma_1^{2m+1}$、$\sigma_2x_{23}^m=\sigma_2^{2m+1}$。抽出ノート §2.1 の「hexagon は完全一致」の内訳。)

**段 (b) 判定の場の同一性**:
2008 は $B_3/(\tilde{\mathbf N}_{\rm core})_{PB_3}=B_3/\mathbf N_0$ で、本走は $B_3/\mathbf N$ で評価する。**2401 Prop 3.4**(逐語 = 仲裁ノート §1)より、$(m,f)\in\mathbb Z\times[F_2,F_2]$ に対し
$$\text{(3.3)(3.4) mod }N\ \iff\ f\theta(f)\in N_{F_2}\ \wedge\ \tau^2(y^mf)\tau(y^mf)y^mf\in N_{F_2}$$
であり、**右辺は $N_{F_2}$ のみに依存**する。XFER-0 より $\mathbf N_0\cap F_2=\mathbf N\cap F_2=\mathcal V(F_2)$ ⟹

$$\boxed{\ \text{hexagon mod }(\tilde{\mathbf N}_{\rm core})_{PB_3}\ \iff\ \text{hexagon mod }\mathbf N\qquad(\forall m\in\mathbb Z,\ \forall f\in[F_2,F_2]).\ }$$

> ★ **独立確認**: 本体 v1.1 補題 **B4-KAPPA** が、$\kappa:PB_3\to\mathbb Z$($fc^k\mapsto k$)について hexagon defect $d_1,d_2$ の $\kappa$ が恒等的に $0$ であることを、$f=1$ の直接計算 + $PB_3^{\rm ab}=\mathbb Z^3$ 上の $\sigma_1,\sigma_2$-共役行列(座標の互換)で示している。Prop 3.4 とは独立の経路。
> ⚠ **既在の停止規則 S-8′ と整合**: 「$\mathbf N$ と $\mathbf N_0$ の判定が 1 件でも食い違えば実装バグ」(NW-P8 の versioned 撤回・裁定 474)。本票の §5 停止規則 S-Q46-2 はこれを継承する。

### 3.4 ★ 補題 **XFER-3**(**pentagon の空虚** — $\psi\circ p_4$ 構造の帰結)

> ### 補題 XFER-3(= 本体 v1.1 定理 **B4-VAC**)
> すべての charming $f$ に対し (2.20) は $PB_4/\tilde{\mathbf N}_{\rm core}$ の中で**恒真**。
> **証明の骨(明示計算)**: $PB_4/\tilde{\mathbf N}_{\rm core}\hookrightarrow P^4$ ゆえ (2.20) は 4 座標の連立と同値。第 $i$ 座標は 5 本の合成 $\psi p_i\varphi_\bullet$ による代入であり、**20 本の完全表**(本体 v1.1 付録 A.1)は各 $i$ について **2 本が $\psi$・3 本が退化**(像が位数 7 の巡回群)であることを与える。退化写像は像が可換かつ指数 7 ゆえ $[F_2,F_2]$ も $\mathcal V(F_2)$ も潰す。よって
> $$i{=}4:\ 1\!\cdot\!1\!\cdot\!f=f\!\cdot\!1,\quad i{=}3:\ 1\!\cdot\!f\!\cdot\!1=f\!\cdot\!1,\quad i{=}2:\ 1\!\cdot\!f\!\cdot\!1=1\!\cdot\!f,\quad i{=}1:\ f\!\cdot\!1\!\cdot\!1=1\!\cdot\!f$$
> — 4 座標すべて恒等式。∎

> ### ★★ 補題 **XFER-STRUCT**(**なぜそうなるか** — 委嘱が指定した「$\psi\circ p_4$ 構造経由」の説明)
> $\tilde{\mathbf N}_{\rm core}$ は $\psi\circ p_i$($i=1..4$)の核の交わりであり、**各 $p_i$ は 1 本の紐を忘れる**。ゆえに $PB_4/\tilde{\mathbf N}_{\rm core}$ は、**「$B_4$ の対象でありながら、4 本の紐のうちどれか 1 本を落とした $B_3$ のデータしか保持しない」**群である。この構造から次の 2 つが同時に従う:
> **(i)** 5 本の余面 $\varphi_\bullet$ は「5 点の隣接対を潰す」操作だが、$p_i$ を合成すると **各座標で 2 本が $\psi$ に潰れ 3 本が退化する**(付録 A.1 の 8/12 分解)⟹ **pentagon は $B_4$ の窓の言葉で書かれていながら、$B_3$ の情報しか使えず、空虚になる。**
> **(ii)** hexagon の場は $B_3/(\tilde{\mathbf N}_{\rm core})_{PB_3}=B_3/\mathbf N_0$ であり、XFER-2 により $B_3$ 窓 $\mathbf N$ での判定と**同一**。
> $$\boxed{\ \Longrightarrow\ \tilde{\mathbf N}_{\rm core}\ \textbf{の 2008-理論は、charming 層の上では }B_3\textbf{-gentle 理論 at }\mathbf N\ \textbf{の忠実な複製である。}\ }$$
> ★ **fake 判定だけがこの複製の外から来る** — すなわち **4 本目の紐を本当に見る解像度**($\tilde{\mathbf N}^*=\mathcal V(PB_4)$ の pentagon、または $Q=K(0,5)/W$ 上の $\bar\rho$-ノルム)から。**2 つの異なる解像度を組み合わせるのが本構成の中身であり、単一の窓の中では出せない**(検分ノート §7 の指摘)。
> ★ **Dolgushev らの 35 窓(Table 1)は $\psi:PB_4\to S_d$ 由来の「一般の」窓であり、忘却射の核という退化した窓は標本に入っていない** — これが Q4.6 が 2020 年以来開いたままである一因の候補(**推測。証明でも文献主張でもない**)。

### 3.5 補題 **XFER-4**(charming と全射性)

> **(1) charming(2008 Def 2.19)**: (i) $f\,(\tilde{\mathbf N}_{\rm core})_{PB_3}$ が $f_1\in[F_2,F_2]$ で代表できる ⟸ 本走宇宙の定義 $\bar f\in[P,P]=[F_2,F_2]\mathcal V(F_2)/\mathcal V(F_2)$ と $\mathcal V(F_2)\subseteq\mathbf N_0$。(ii) $T^{F_2}$ 全射 = SURJ ⟸ **H8′**($P$ は 7 群・$\bar f\in[P,P]=\Phi(P)$・$\gcd(2m+1,7)=1$)。
> **(2) GT-shadow(Def 2.9 + Prop 2.10)**: $T^{PB_2}$ 全射 $\iff$ $2m+1$ が $\mathbb Z/7$ の単元 $\iff m\in\mathcal X$。$T^{PB_3}$ 全射: $PB_3/\mathbf N_0\cong P\times C_7$ は 7 群で $\Phi(P\times C_7)=[P,P]\times1$、像は $x^{u},{}^{f}\!y^{u},c^{u}$($u=2m+1$、$\gcd(u,7)=1$)を含むので Frattini 論法で全射(**H8′ の直接拡張**)。$T^{PB_4}$ 全射は **Prop 2.10** で自動。
> **(3)** ⟹ **2401-charming $\iff$ 2008-charming**(本体 v1.1 補題 **CHARM-EQ**)。∎

### 3.6 ★★ 定理 **XFER**(対象の転写)

> ### 定理 XFER
> XFER-0〜4 の下で、写像 $(m\bmod7,\ \bar f)\mapsto[(m,f)]$ は
> $$\boxed{\ \{\text{本走の hexagon 通過 }\mathbf{294}\ \text{元}\}\ \xrightarrow{\ \sim\ }\ \mathrm{GT}^\heartsuit_{2008}(\tilde{\mathbf N}_{\rm core})\big\vert_{\rm practical}\ }$$
> の**全単射**を与える。
> **証明.** (⊆) hexagon(XFER-2)+ pentagon 恒真(XFER-3)⟹ GT-pair。charming + 全射性(XFER-4)⟹ charming GT-shadow。(⊇) 逆に practical な charming shadow は $(m,\bar f)\in\mathcal X\times[P,P]$ のラベルをもち(XFER-1 (5) と XFER-0)、hexagon mod $\mathbf N_0$ $\iff$ hexagon mod $\mathbf N$(XFER-2)ゆえ本走の 294 元のいずれか。単射性: $f,f'\in F_2$ が $\mathbf N_0$ を法に等しければ $f^{-1}f'\in\mathbf N_0\cap F_2=\mathcal V(F_2)$ ⟹ $\bar f=\bar f'$。∎

### 3.7 ★★ 定理 **XFER-FAKE**(fake 判定の転写)— **独立 2 経路**

> ### 定理 XFER-FAKE
> $\mathrm{PENT}_W$-FAIL の **252 元**は、$\tilde{\mathbf N}_{\rm core}$ の charming GT-shadow として **fake**(= 2008 の意味で genuine でない)である。
>
> **経路 α(HS 経由・定理 PENT-FORM に依存しない)**
> $[(m,f)]$ が genuine なら $\exists\hat T\in\widehat{GT}=\mathrm{Aut}(\widehat{PaB})$ で $T_{\tilde{\mathbf N}_{\rm core}}=\hat P\circ\hat T\circ I$ が当該 shadow を与える((2.31))。$\hat T$ の座標 $(\hat m,\hat f)\in\hat{\mathbb Z}\times\widehat{F_2}$(Prop 2.18・Cor 2.21 で $\hat f\in([\widehat{F_2},\widehat{F_2}])^{\rm cl}$)は $[m,\bar f]$ を**持ち上げる**。**命題 HSP-SOUND**(翻訳ノート §1.3)により $\mathrm{PENT}_W([m,\bar f])$ が偽ならそのような持ち上げは存在しない。系 XFER-0′ で $\bar f$ は窓を越えて同一。⟹ 矛盾。∎
>
> **経路 β(2008 内部・HS 翻訳に依存しない)**
> 補題 **PAIR** (1) より $\tilde{\mathbf N}^*\le\tilde{\mathbf N}_{\rm core}$。**Cor 3.13** の易しい向き(genuine ⟹ 全ての $K\le N$ に survive)より、genuine なら $\tilde{\mathbf N}^*$ に survive、すなわち $[(m,f)]\in\mathrm{GT}^\heartsuit(\tilde{\mathbf N}^*)$ の像。補題 PAIR (3) よりこの射はラベル上の恒等ゆえ、$[(m,f)]$ 自身が $\tilde{\mathbf N}^*$ の GT-pair でなければならない。ところが本体 v1.1 **定理 PENT-FORM**(+ 当該元は hexagon 通過ゆえ (3.10) を満たす)より (2.20) mod $\tilde{\mathbf N}^*$ $\iff$ $\mathrm{PENT}_W$ で、これは偽。⟹ 矛盾。∎
>
> ★ **2 経路は独立である**: 経路 α は HS Prop 7 由来の $\mathrm{PENT}_W$ の健全性のみを使い、【GAP-B4-1】(= 定理 PENT-FORM)に**依存しない**。経路 β は 2008 の公理と Cor 3.13 のみを使い、**HS 翻訳に依存しない**。どちらか一方が崩れても結論は残る。

### 3.8 ★★ 系 **Q46-ANSWER**(Question 4.6 への候補回答)

> $$\boxed{\ K:=\mathcal V(PB_4)\ \le\ N:=\tilde{\mathbf N}_{\rm core}\quad\text{について}\quad \mathrm{GT}^\heartsuit(K)\longrightarrow\mathrm{GT}^\heartsuit(N)\ \textbf{は全射でない}\ }$$
> であり、像に入らない practical な charming shadow が **252 個**存在する。これらは **charming ∧ fake** である。
> **証明.** 補題 PAIR (3) より当該射は部分集合の包含。定理 XFER より $\mathrm{GT}^\heartsuit(N)\vert_{\rm practical}$ は 294 元。定理 PENT-FORM + 本走測定より、そのうち 252 元は (2.20) mod $K$ を満たさない ⟹ $\mathrm{GT}^\heartsuit(K)$ に属さない ⟹ 像に入らない。fake であることは定理 XFER-FAKE。∎
>
> ⚠ **非全射性の主張には $\mathrm{GT}^\heartsuit(K)$ の**濃度**を知る必要がない**(1 元でも像外にあれば足りる)。**BH-α-pent(42)は非全射性には不要**であり、「像がちょうど 42 元」という**強い形**にのみ必要である(§4 の Q46-P5 / P6 の格の差)。
> ⚠ **practical 制限は非全射性を弱めない**: 像は $K$ の**全** shadow(非 practical 込み)の像だが、補題 PAIR (3) によりラベル上の恒等ゆえ、252 元のいずれかが像に入るには**その元自身が $K$ の GT-pair でなければならない**。これは (2.20) の失敗で排除される。

---

## 4. ★ 予言(**発火前に凍結** — Q46-P1〜P7)

> **表の読み方**(票 v1 の規約を継承): **格 T** = 定理の帰結(前件つき・的中は情報量ゼロ・**バグ検出器**)/ **格 T\*** = 定理級だが前件に candidate を含む / **格 C** = 予想(登録済み分岐あり)。

| ID | 予言 | 値 | 格 | 根拠 / 分岐 |
|---|---|---|---|---|
| **Q46-P1** | $\tilde{\mathbf N}_{\rm core}$ は $B_4$-正規・有限指数・$\le PB_4$。機械の正規性検査(生成元の $\sigma_1,\sigma_2,\sigma_3$ 共役が $P^4$ の像で保存)を通る | PASS | **T** | XFER-1(CORE-4) |
| **Q46-P2** | $(\tilde{\mathbf N}_{\rm core})_{PB_3}=\mathbf N_0$((2.4) を 5 本の余面で機械計算) | $\mathbf N_0$ | **T** | XFER-1 (4) = B4-IND |
| **Q46-P3** | $\lvert PB_4:\tilde{\mathbf N}_{\rm core}\rvert$(= $P^4$ 内の生成部分群の位数) | $7^{8}\le\ \cdot\ \le7^{29}$、かつ **$Z(PB_4)=\langle\Delta^2\rangle\le\tilde{\mathbf N}_{\rm core}$**、かつ **$P^4$ の真部分群**($\mathbb F_7$-階数 5 < 8) | **T\*** | 本体 v1.1 付録 A.4。**正確な値は測定量**(予言しない) |
| **Q46-P4** ★ | (2.20) mod $\tilde{\mathbf N}_{\rm core}$ の通過数($[P,P]$ 全 117,649 件・$m$ 非依存) | **117,649**(全通過) | **T** | XFER-3 = B4-VAC。**バグ検出器**(§5 の S-Q46-1) |
| **Q46-P5** ★★ | 2008 hexagon (2.18)(2.19) を **$B_3/\mathbf N_0$ の中で直接評価**したときの通過 shadow 数 | **294**(本走の hexagon 通過集合と**集合として一致**) | **T** | XFER-2。**Lane V の `ApplyQElt` バグの回帰試験を兼ねる**(仲裁ノート §3) |
| **Q46-P6** ★★ | $\mathrm{GT}^\heartsuit_{2008}(\tilde{\mathbf N}_{\rm core})\vert_{\rm practical}$ の元数、およびそのうち **fake** の数 | **294** / fake **252**(genuine **42**) | **T\***(fake 252)/ **C**(genuine が**ちょうど** 42) | XFER + XFER-FAKE(2 経路)。**genuine = 42 の側のみ BH-α-pent 相対** |
| **Q46-P7** | 対 $(K,N)=(\mathcal V(PB_4),\tilde{\mathbf N}_{\rm core})$ で $\mathrm{GT}^\heartsuit(K)\to\mathrm{GT}^\heartsuit(N)$ が非全射 | 非全射・像の余 $\ge252$ | **T\*** | 系 Q46-ANSWER。**紙のみ**($K$ を機械で構築しない) |

### 4.1 登録済み分岐

| 分岐 | 内容 | 帰結 |
|---|---|---|
| **BQ-1a**(本票の予言) | Q46-P4 が全通過 | XFER-3 実測確認 ⟹ P6 へ進む |
| **BQ-1b** | Q46-P4 で FAIL が出る | ★ **理論の誤りより先に実装を疑う**(S-Q46-1)。20 合成表・余面 (A.18)・$p_i$ の付け替え規約(順序保存)を再検査 |
| **BQ-2a**(本票の予言) | Q46-P5 = 294 | XFER-2 実測確認 |
| **BQ-2b** | Q46-P5 ≠ 294 | ★ **S-8′ 発火**(N と N₀ の判定一致は定理)⟹ IMPLEMENTATION_BUG / STOP |
| **BQ-3a**(本票の予言) | Q46-P6 の genuine が 42 | BH-α-pent と整合 |
| **BQ-3b** | genuine が 42 でない | BH-α-pent(framework/measurement-relative)への反証入力 ⟹ 全面点検 |

---

## 5. 停止規則(**提案** — 発効は司令塔裁定 + Sol ゲート)

| ID | trigger | verdict |
|---|---|---|
| **S-Q46-0** | **CAL-B4(§6)が全 PASS していない** | **発火禁止**(前件不成立) |
| **S-Q46-1** | Q46-P4 で (2.20) FAIL が 1 件でも出る | **IMPLEMENTATION_BUG_SUSPECTED / STOP**(定理 B4-VAC は別人格の独立再導出で PASS 済) |
| **S-Q46-2** | Q46-P5 の通過数が本走の 294 と 1 件でも食い違う | **IMPLEMENTATION_BUG_SUSPECTED / STOP**(既在 S-8′ の継承) |
| **S-Q46-3** | Q46-P2 で $(\tilde{\mathbf N}_{\rm core})_{PB_3}\ne\mathbf N_0$ | **STOP**(余面 (A.18) か $p_i$ 規約の実装誤り) |
| **S-Q46-4** | Q46-P3 が $[7^8,\ 7^{29}]$ の外、または $\Delta^2\notin\tilde{\mathbf N}_{\rm core}$ | **STOP** |
| **S-Q46-5** ★ | 成果物・cert・報告のいずれかに **Question 4.6 と 4.7 の取り違え**、または **novelty ゲート未通過のまま「初例」「解決」の語** | **報告無効 / 差戻し**(§7.2 の R-Q1/R-Q2) |
| **S-Q46-6** | 判定機が N⁽¹⁹⁾ と $\tilde{\mathbf N}_{\rm core}$ で**別コード**になっている | **CV-9 判読を経ずに一致を格付けしない**(§6.3) |

---

## 6. 較正(CAL-B4 の適用可否 — 委嘱の指定項目)

### 6.1 適用可否の結論

> $$\boxed{\ \textbf{適用可能。ただし「判定機を窓非依存の汎用関数として書く」ことが条件である。}\ }$$

- CAL-B4 の N⁽¹⁹⁾ / N⁽³⁴⁾ は窓が **$S_9$ / $S_{18}$ の置換 6 個**で与えられる(2008 (4.1): 窓 $\leftrightarrow$ (A.3) を満たす 6 つ組 $(g_{12},g_{23},g_{13},g_{14},g_{24},g_{34})$)。
- $\tilde{\mathbf N}_{\rm core}$ は **$P^4$ の元 6 個**で与えられる(§2.2 の表)。
- ⟹ 判定機を **`penta(G, [g12,g23,g13,g14,g24,g34], f_word)`**(= 「任意の有限群 $G$ と 6 元の組」を受ける関数)として書けば、**N⁽¹⁹⁾・N⁽³⁴⁾・$\tilde{\mathbf N}_{\rm core}$ を同一コードに流せる**。

### 6.2 較正項目の対応表

| CAL-B4 | N⁽¹⁹⁾ | N⁽³⁴⁾ | $\tilde{\mathbf N}_{\rm core}$ への適用 |
|---|---|---|---|
| C-1 $\lvert PB_4:N\rvert$ | 216 | 762,048 | ✓(Q46-P3・**予言は範囲のみ**) |
| C-2 (2.4) と $N_{\rm ord}$ | 6 | 9 | ✓(Q46-P2 = $\mathbf N_0$、$N_{\rm ord}=7$) |
| C-3 $\lvert F_2:N_{F_2}\rvert$ / 交換子 | 7776 / 216 | 20,575,296 / 254,016 | ✓($7^8$ / $7^6$) |
| C-4 pentagon 通過数 | **216**(**宇宙 = 全 7776**) | **4096**(**宇宙 = 交換子部分群**) | ✓(Q46-P4・**宇宙 = 交換子部分群 117,649**) |
| C-5 hexagon 持ち上げ | 36 | 243 | ✓(Q46-P5 = 294 だが**単位が違う** — 下記 ⚠) |
| C-6 $\lvert\mathrm{GT}\rvert$ / $\lvert\mathrm{GT}^\heartsuit\rvert$ | 72 / 12 | — / 486 | ✓(Q46-P6 の $\mathrm{GT}^\heartsuit$ = 294) |
| C-8 Package GT `penta` 突合 | ✓ | ✓ | ✓(**第三者照合が $\tilde{\mathbf N}_{\rm core}$ にも掛かる**) |

> ⚠ **単位の罠 3 つ**(較正で必ず明示すること):
> **(i) 宇宙の差**: N⁽¹⁹⁾ の 216 は **$F_2/N_{F_2}$ 全体(7776)の中**(Property 4.2 strong)、N⁽³⁴⁾ の 4096 は **交換子部分群の中**(Property 4.3 weak)。本票の宇宙は**交換子部分群 $[P,P]$**。
> **(ii) $f$ 単位 vs shadow 単位**: C-4 は **$f$ の個数**、C-5 と Q46-P5/P6 は **shadow $(m,f)$ の個数**。cert に**単位欄**を必須にする(本体 v1.1 §9.2【GAP-B4-4】)。
> **(iii) friendly の $m$ 範囲**: N⁽¹⁹⁾ は $N_{\rm ord}=6$ ゆえ $2m+1\in\{1,5\}$、$m\in\{0,2,3,5\}$(4 値)。本票は $N_{\rm ord}=7$ ゆえ $m\in\mathcal X$(6 値)。

### 6.3 CV-9 の要求

- 判定機が **1 本のコード**なら CV-9 判読は**不要**(同一仕様が自明)。
- **2 実装(置換群 backend / pc 群 4 重直積 backend)に分かれる場合は、falsifier の CV-9 判読を必須前件とする**(S-Q46-6)。
- ★ **推奨**: 1 本のコード + 3 つの窓インスタンス。これで CV-9 リスクが構造的に消える。

---

## 7. novelty(**格 = 文献上未解答・初例候補。発効主張はしない**)

### 7.1 掃引の結果(`docs/scout/q46_citation_sweep_v1.md` の引用)

| # | 事実 | 出所 |
|---|---|---|
| **N-1** | arXiv 上で "GT-shadow" を含む論文は **4 本で全数**(2026-08-06 時点。arXiv API 全文検索 + Semantic Scholar 被引用の二系統で収束) | 掃引 §② |
| **N-2** | **Question 4.6 は 4 本の掃引範囲内で未解答**。2106.06645 は §8 で**再掲するのみ**(GT パッケージで探索できる、という作業提案) | 掃引 §③ |
| **N-3** | **2401.06870 脚注 2(2024)**: 「the authors of this paper do not know a single example of a fake GT-shadow」 — gentle 版でも fake の実例は 2024 年時点で未発見 | 掃引 §③ |
| **N-4** ★ | **2405.11725 が解決したのは Question 4.7 であって Question 4.6 ではない**(Cor 5.4 が [7, Question 4.7] の gentle 版を解決、と本文が明記) | 掃引 §③ |
| **N-5** | MIT PRIMES の 2 本(非 arXiv)は PDF 抽出失敗で **UNVERIFIED**。内容主張はしない | 掃引 §② |

### 7.2 ★ 掃引の**射程の限界**(正直申告 — 本票が自分で加える留保)

| # | 留保 |
|---|---|
| **L-1** | 掃引は検索語 **"GT-shadow"** による悉皆である。**別語彙**(例: fake の別名、GT₀-shadow、Guillot 系の変種)で書かれた先行があれば掛からない |
| **L-2** | 掃引ノート自身が申告するとおり、**Fresse・Horel・Bar-Natan・Schneps 等 GT 業界本流からの引用は未探索** |
| **L-3** | 本票の構成は「忘却射の核」という**退化した窓**を使う。Dolgushev らの Table 1 は $\psi:PB_4\to S_d$ 由来の一般の窓なので標本外(§3.4 XFER-STRUCT)だが、**「退化窓は自明で面白くないから誰も書いていないだけ」という可能性は排除できない** ⟹ §7.3 の自己批判へ |

### 7.3 ★ 自己批判(**主張を弱める方向の検討** — 先に書く)

> **反論候補 A**: 「$\tilde{\mathbf N}_{\rm core}$ は pentagon が空虚な窓なので、Q4.6 の意図(pentagon が効く場での fake)を外している」。
> **本票の応答**: Q4.6 の**逐語**は「$K\le N$ で $\mathrm{GT}^\heartsuit(K)\to\mathrm{GT}^\heartsuit(N)$ が非全射な対はあるか」であり、**窓に非退化性の条件は課されていない**。ただし**この反論は正当な「意義」の議論であり、司令塔 → Sol → 研究者の判断事項**である。本票は「逐語の意味で答える」と「意図の意味で答える」を**区別して記録**する。
>
> **反論候補 B**: 「fake であることの根拠は $B_3$ 側の測定($\mathrm{PENT}_W$)であって、$B_4$ 側で自足していない」。
> **本票の応答**: 経路 β(§3.7)は **2008 の公理 + Cor 3.13 + 定理 PENT-FORM** のみで閉じており、$B_4$ 側で自足する。ただし PENT-FORM は**文献相対**(【GAP-B4-1′】)。経路 α は HS 相対。**どちらの経路も外部依存を持つことは正直に記帳する。**
>
> **反論候補 C**: 「252 という個数は practical 制限つきである」。
> **本票の応答**: Q4.6 は存在問題ゆえ答えは弱まらない(§1)。個数の主張のみ practical 限定(【GAP-B4-2】)。

### 7.4 記法の防壁

| # | 規約 |
|---|---|
| **R-Q1** ★ | **Question 4.6 と 4.7 を混ぜない。** 本票の標的は 4.6。2405.11725 が解いたのは **4.7 の gentle 版**。cert・報告・便のすべてで番号を明示し、「Dolgushev の open question」と曖昧に書かない |
| **R-Q2** ★ | novelty は **「文献上未解答(掃引 v1 の射程内)・初例候補」**とのみ書く。**「初」「解決」「answered」は司令塔の novelty ゲート通過まで禁止**(既在の恒久規律「初・新規と言う前に grep」+ 本票の L-1〜L-3) |
| **R-Q3** | 「fake」は 2008 の定義(genuine でない)でのみ使う。工房の A 型正札「PENT_W-FAIL 非算術 shadow」とは**別の語**であり、**同一対象の別枠での呼称**であることを cert に明記(本体 v1.1 §7 の R1–R3) |

---

## 8. 走行仕様(**発火は Sol 認可後** — 実装係向け)

| 段 | 内容 | 入力 | 出力 | 予言 |
|---|---|---|---|---|
| **R0** | CAL-B4 全 PASS の確認 | 既在 cert | gate | S-Q46-0 |
| **R1** | $P^4$ の中に $\tilde{\mathbf N}_{\rm core}$ の商 $G_{\rm core}:=\langle\text{§2.2 の 6 元}\rangle\le P^4$ を構築。$B_4$-正規性検査($\sigma_1,\sigma_2,\sigma_3$ 共役で 6 元の像が $G_{\rm core}$ 内に閉じる)。$\lvert G_{\rm core}\rvert$ 実測。$\Delta^2$ の像が $1$ か検査。(2.4) で $(\tilde{\mathbf N}_{\rm core})_{PB_3}$ を計算し $\mathbf N_0$ と照合 | $P$(既在 pc 群) | 窓 cert | P1・P2・P3 |
| **R2** | $[P,P]$ の全 117,649 元で $D_{B_4}$(§2.2 の 6 元を使う (2.20))を評価 | R1 | 通過数 | **P4 = 117,649** |
| **R3** | 2008 hexagon (2.18)(2.19) を $B_3/\mathbf N_0$ で**直接**評価(word-level 経路・$705{,}894$ 対 または 294+対照標本) | $PB_3/\mathbf N_0\cong P\times C_7$ | 通過 shadow 集合 | **P5 = 294**(本走と集合一致) |
| **R4** | R2 ∩ R3 で $\mathrm{GT}^\heartsuit_{2008}(\tilde{\mathbf N}_{\rm core})\vert_{\rm practical}$ を確定。lane P の $\mathrm{PENT}_W$ 通過集合(既在 cert)と join して fake/genuine 分解 | R2,R3,lane P cert | 294 = 252 + 42 | **P6** |

- **$R=PB_4/\mathcal V(PB_4)$(ANUPQ)は一切使わない** ⟹ 本体 v1.1 の工程 P1 ブロッカーを迂回。
- **本走宇宙の再測定は行わない**(R3 は $\mathbf N_0$ での**独立評価**であり、本走の $\mathbf N$ 判定を上書きしない。両者の一致が S-Q46-2 の検査対象)。
- cert の必須欄: `FW=B4-2008` / `window_arity=4` / `equation_ids` / **`count_unit`(f 集合 / shadow 集合)** / `universe`(全体 or 交換子部分群) / `practical_only=true`。

---

## 9. 格付け・【GAP】・規律申告

### 9.1 格付け

| 対象 | 格 |
|---|---|
| 補題 **XFER-0** / 系 **XFER-0′** | **paper-proof**(箱型計算 + HSP-T の well-definedness) |
| 補題 **XFER-1** | **paper-proof**(CORE-4 + B4-IND 相対。両者は検分ノートで独立再導出 PASS) |
| ★ 補題 **XFER-2** | **paper-proof**(段 (a) = 代入・段 (b) = 2401 Prop 3.4 の逐語適用。独立確認 = B4-KAPPA) |
| 補題 **XFER-3** | **paper-proof**(= B4-VAC。別人格の独立再導出で PASS) |
| ★★ 補題 **XFER-STRUCT** | **paper-proof**(構造の言い換え)。ただし末尾の「Table 1 に退化窓が入っていないことが Q4.6 未解決の一因」は ★ **推測**(証明でも文献主張でもない) |
| 補題 **XFER-4** | **paper-proof**(H8′ の直接拡張 + Prop 2.10) |
| ★★ 定理 **XFER** | **paper-proof**(XFER-0〜4 相対)+ **測定相対**(294 は本走の値) |
| ★★ 定理 **XFER-FAKE** | **conditional candidate**。経路 α = HSP-SOUND 相対 / 経路 β = 定理 PENT-FORM 相対(【GAP-B4-1′】= 文献相対)。**2 経路は独立** |
| ★★ 系 **Q46-ANSWER** | **conditional candidate**。**Sol 未監査**。**発火前** |
| 補題 **PAIR** | **paper-proof** |
| `verified` | ✗(Lean 未使用) |
| `cross-checked` | ✗(CV-9 判読未実施・機械実行ゼロ) |
| **novelty** | ★ **「文献上未解答(掃引 v1 の射程内)・初例候補」**。**発効主張はしない**(§7.2 の L-1〜L-3・R-Q2) |

### 9.2 【GAP】

| 札 | 内容 | 状態 |
|---|---|---|
| **【GAP-B4-1′】**(本体 v1.1 から継承) | 定理 PENT-FORM が引用する LS-(4)・LS-(abs) は pin ノート経由で、本起草者は原文頁画像を見ていない | **文献相対**。経路 α が独立の保険 |
| **【GAP-B4-2】**(継承) | practical でない 2008 GT-shadow の存否(原論文 p.23 で未解決) | **UNKNOWN**。Q4.6 の答え(存在)には影響しない・個数のみ限定 |
| ★ **【GAP-Q46-1】**(新) | $\tilde{\mathbf N}_{\rm core}$ が **isolated** か否かは未検討。Q4.6 の回答には不要だが、$\mathrm{GT}^\heartsuit(\tilde{\mathbf N}_{\rm core})$ が群かどうかは isolated 性に依存する | **UNKNOWN**(任意測定項目)。**本票はこれを主張に使わない** |
| ★ **【GAP-Q46-2】**(新) | 「逐語で答える」と「意図で答える」の差(§7.3 反論候補 A)。**退化窓での回答が Q4.6 の意義を満たすか**は数学的問題ではなく判断事項 | **要裁定**(司令塔 → Sol → 研究者) |
| **【GAP-B4-3】**(継承) | Cor 3.13 の停止点に有効上界なし | **UNKNOWN**。本票は Cor 3.13 の**易しい向きしか使わない**ので影響なし |

### 9.3 規律申告

- ★ **機械を 1 度も走らせていない。** 本票の数値はすべて (i) 紙の導出 (ii) 既在の本走測定値(294/42/252・Sol 検収済)(iii) 本体 v1.1 付録 A の既在出力 のいずれか。
- ★ **本走宇宙(705,894 対)の候補を 1 件も新規評価していない。**
- **封印 3 量非接触。既在文書を 1 バイトも改変していない**(本体 v1・v1.1・検分ノート・掃引ノートすべて read-only)。
- ★ **HS2000 Prop 7 を使用していない**(罠 D-5 遵守)。経路 α で使うのは既在の **HSP-SOUND**(翻訳ノート §1.3・量化子なしの $\mathrm{PENT}_W$ 形)である。
- ★ **外部文献検索ゼロ。** §7 の事実はすべて `docs/scout/q46_citation_sweep_v1.md` からの引用であり、本起草者は LS1994 / HS2000 / 2106.06645 / 2405.11725 の原文を 1 頁も開いていない。
- ★ **走らせない。** 発火 3 条件 = Sol 認可(便 112 以降)+ 司令塔裁定 + CAL-B4 全 PASS。
- **新しい停止規則を発効させない**(§5 は提案)。

---

## 10. Sol への監査点(4 点・便 112 用)

> **Q-1 ★★★ 系間移送の妥当性**(§3)。$B_3$-gentle 系での測定(hexagon 294・$\mathrm{PENT}_W$-FAIL 252)が、$B_4$ 系の窓 $\tilde{\mathbf N}_{\rm core}$ における charming ∧ fake の判定に転写される、という 5 段(XFER-0〜4 + XFER)に穴がないか。とくに **XFER-0(4 窓が同じ $\bar f\in P$ しか見ない)**と **XFER-2 段 (b)(2401 Prop 3.4 を $\mathbf N_0$ に適用してよいこと — Prop 3.4 の前件は $N\in\mathrm{NFI}_{PB_3}(B_3)$ と $(m,f)\in\mathbb Z\times[F_2,F_2]$ の 2 条のみ)**。

> **Q-2 ★★ 定理 XFER-FAKE の 2 経路**(§3.7)。経路 α(HSP-SOUND)と経路 β(2008 Cor 3.13 + PENT-FORM)が**独立**である、という会計を認めるか。とくに経路 β の「補題 PAIR (3) によりラベル上の恒等ゆえ、survive するには当該元自身が $K$ の GT-pair でなければならない」という一段。

> **Q-3 ★★ 系 Q46-ANSWER の意義**(§7.3 反論候補 A・【GAP-Q46-2】)。$\tilde{\mathbf N}_{\rm core}$ は pentagon が空虚な**退化窓**である。Q4.6 の**逐語**は満たすが、**意図**(pentagon が効く場での fake)を満たすか。満たさないと判断する場合、どの追加条件(非退化性の定義)を課すべきか。

> **Q-4 ★ novelty の格**(§7)。掃引ノート(arXiv "GT-shadow" 4 本悉皆・Q4.6 未解答・2401 脚注 2・2405 は Q4.7)を根拠に **「文献上未解答・初例候補」**の格で書き、**発効主張をしない**運用でよいか。§7.2 の留保 L-1〜L-3(別語彙・本流引用未探索・退化窓ゆえ誰も書かなかっただけの可能性)は十分か。

---

## 11. 本票の凍結宣言

本票は **Q46-P1〜P7 の予言値**と **§5 の停止規則**と **§7 の novelty 格**を凍結する。発火後にこれらを緩める改稿は行わない(**S-7′ 準拠**)。改訂が必要な場合は **versioned な別票(v2)**として起草し、v1 と分岐の記録を不変保存する。

> ★ **登録済み分岐への着地は「外れ」ではなく「決着」である**(票 v1 §7 の丙類規約を継承)。ただし **S-Q46-1/2 の発火(実装バグ疑い)は決着ではなく STOP** である。
