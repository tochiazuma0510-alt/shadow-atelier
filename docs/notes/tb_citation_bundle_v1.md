# (TB1)/(TB4ᵘ)/(TB3) 引用化 3 枚束 — 条項単位の対応判定・依存表引用差替版・格更新案 **v1**

**状態札: `candidate(引用化起草・紙のみ / Lean 検証ではない / cross-checked でもない / 封印非接触($n=5$ の値・窓データ・機械計算・$\varepsilon$ bits に一切触れていない)/ novelty 主張なし)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05・**新設 v1**
- 委嘱: 司令塔「TB1/TB4ᵘ/TB3 の引用化起草(3 枚束・1 回で)」
- 入力(pin 2 本): `docs/notes/reading_deligne_s15_profinite_v1.md`(以下「読解 D」)/ `docs/notes/reading_ihara_icm1990_tb3_v1.md`(以下「読解 I」)
- 入力(形の正本): `docs/notes/framework_promotion_campaign_v2.md`(§0 の errata で有効化された v1 §6 系・【文献要請 13/14】)+ `docs/week4-BFC攻略_opus_v2.md` §2(TB 条文)・§4(分解表)・§6・§7・§7.1・**§12.1【GAP-TB】**・§13.1
- 語彙: `docs/notes/conventions_ledger_v1.md` **§1.5(CV-10 細則 `proof_body_status`)**・`docs/notes/div_law_v1.md` §A.3(F99-3.2 Route A 語彙)
- **原典**: `papers/delivered/deligne_1989_groupe_fondamental_P1_moins_3points.pdf`(SHA-256 `689b516faf3a05c657920d21a74f68fdc7d0adbd4f7c75d78928e5356c636e44`・**頁対応 PDF = 印字 − 78**)/ `papers/ihara-ICM1990-vol1-braids-galois-arithmetic.ocr.pdf`(**PDF = 印字 + 88**)

> ### ★ 本束は既存文書を 1 バイトも改変していない
> BFC v2・ASM v1/v2・追記 A/B/C 案・CLAIMS のいずれにも触れていない。本束が提示するのは **(a) 対応判定 (b) 依存表の引用差替版(additive erratum 方式・本文不改変) (c) 札文言案(発効は Sol 検収後)** のみである。

---

## 0. 判定(先に 6 行)

| TB | 総合判定(3 値) | 一行 |
|---|---|---|
| **(TB1)** | ★ **読み替えつき一致**(条件つき) | 圏同値は **Deligne §10.16** で pin できるが、**「$\mathrm{Fib}_{\vec{01}}$ が繊維関手である」に番号つき pin は無い**。§15 が構成するのは $T_s^0$ の被覆への**制限関手**であって繊維関手ではない ⟹ **工房側初等補題 TB1-FF を明示することを条件に一致**(§3) |
| **(TB4ᵘ)** | ★ **読み替えつき一致**(かつ**独立仮定としての内容が縮む**) | 4 条項のうち **(δ) は工房の $\mathrm{Fib}$ 定義の tautology・(α) は初等 Kummer・(γ) は (TB1)+(TB3) の読み替えで従う** ⟹ 真に外部 pin を要するのは **(β)(canonical な射の存在と命名)= (16.1.1) + §15.20–15.23** の 1 本(§4) |
| **(TB3)** | ★ **読み替えつき一致**(条項 (c) は**弱い pin**) | (a)(b) は Ihara ICM §2.3 で逐語 pin。★ **(c)「$z$ が $\infty$ の慣性生成元」は括弧書き 1 語 "(a loop around ∞)" のみ**・明文も証明本文もない。**ただし (5′) 証明鎖では非 load-bearing**(§5) |

> ### ★ 一行で
> $$\boxed{\ \textbf{(5}'\textbf{) 証明鎖が真に外部文献を要する箇所は}\ \mathbf{2}\ \textbf{つ} \;=\; \underbrace{\text{Deligne \S10.16}}_{\text{圏同値}} \;+\; \underbrace{\text{Deligne \S15.23 PREUVE / 14.2}}_{\text{局所 }\pi_1=\hat{\mathbf Z}(1)}\ }$$
> 残りは (i) 工房規約((TB2))・(ii) 工房定義の tautology・(iii) 初等可換代数/群論・(iv) ★ **本束で新規に浮上した未 pin 項目 1 件(【GAP-TB-EXACT】・§6.4)**。

> ### ⚠ 到達した格は「引用で閉じた」ではない
> 本束が請うのは **`canonical-source-pinned`**(条項ごとに §/式番号があり読み替えが条文化され `proof_body_status` が記入済)であって、**`canonical-source-relative`**(全 pin が `present` に着地)ではない。理由は 4 つ(§7.3)。

> ### ★ 差戻しにしなかった理由(委嘱「不一致なら差戻しでよい」への回答)
> **条項水準では 不一致 が 1 件出た**((TB1-b)「$\mathrm{Fib}_{\vec{01}}$ が繊維関手」に番号つき pin が無い・§3.2)。それでも束全体を差し戻さなかったのは、次の 3 点が同時に成り立つからである:
> 1. **不足分が初等であり、私がその場で埋められた**(補題 TB1-FF・§3.3)。⟹ 「文献が供給しない」であって「主張が偽」ではない。
> 2. **不足分を隠さず「工房債務 3 本」として札に載せた**(§7.2 (N-1))。⟹ 引用化の名の下に初等事実を外部化してもいないし、埋めた事実を伏せてもいない。
> 3. **請う格を `canonical-source-relative` から `canonical-source-pinned` へ自分で下げた**(§7.3)。⟹ 到達点の申告が実態と一致している。
> ⚠ **逆に、甘くしなかった点を明示する**: (a) 読解 D の「3 点 pin で閉じる」を**採らなかった**(§3.2・R-1)/ (b) 読解 I の「供給する 3/3」の (c) を**工房条文の (TB3-c) と取り違えていると判定した**(§5.3・R-5)/ (c) **未 pin 項目を 1 件新設した**(【GAP-TB-EXACT】・§6.4)— **これは campaign FP-1 の「3 項目に局在」を「4 項目」へ悪化させる方向の発見であり、伏せていない**。

---

## 1. 方法 — 何を判定したか

### 1.1 判定の 3 値(定義)

| 値 | 定義 |
|---|---|
| **一致** | 工房条文の意味内容が、pin 先の言明の意味内容に**記法の翻訳のみで**含まれる。 |
| **読み替えつき一致** | 明示された読み替え注(**RD-k**・§2)を経由すれば一致する。**その読み替え自体は文献本文にない**(= 工房側が負う債務)。 |
| **不一致** | pin 先が工房条文を供給しない(番号つき言明が無い / 射程が違う / 版が違う)。 |

### 1.2 独立再判定の宣言(委嘱の指示)

読解 I §5.1 の「**供給する 3/3**」・読解 D §7 の「**3 点 pin で閉じる**」は**採らずに再判定した**。差分は **§10**(訂正 2 件・昇格 2 件・新規 3 件)。**読解係の越権はない** — 読解 D §6-2 が「工房条項との意味論的同一性の裁定は数学者/falsifier/司令塔の専権」と明示的に申告しており、本束はその専権の行使である。

### 1.3 私が自分の目で見た範囲の申告(文献ゲート規律)

| 範囲 | 方法 | 用途 |
|---|---|---|
| Deligne 印字 237–241(PDF 159–163)= §15.13–15.25 | **pdftotext(ClearScan OCR)のみ** | 15.16/15.17/15.20 完備化不変性/15.21/15.22/15.23 の逐語再取得 |
| Deligne 印字 255(PDF 177)= §16.1 | ★ **pdftocairo 150 dpi 頁画像で照合**(本束の判定で唯一、読解 D の「判断しない」を覆す箇所のため) | §16.1 の前提・(16.1.1)–(16.1.3)・Betti 正規化文の水準 |
| Ihara ICM | ★ **自分では開いていない**。読解 I の 400 dpi 逐語転記に依拠 | (TB3) 全条項 |

- ⚠ **上記のうち「テキストのみ」の逐語は、いずれも散文(数式記号を含まない)であり OCR 劣化 risk は低いが、採択前に 1 回の頁画像照合を推奨**(監査点ではなく手続き)。**当該頁は読解 D が 150 dpi 画像で全読済**(読解 D §5.2)。
- ⚠ **Ihara 側は二次引用**(読解 I 経由)。私は原本を開いていない。**逐語の正確さは読解 I の 400 dpi 申告に依存する**。

---

## 2. 読み替え注の正式条文化(**RD-1 〜 RD-6**)

> **本節が本束の規範部分である。** 以後の判定で「読み替えつき一致」と書いたものは、すべて下の RD-k のいずれかを経由する。**RD-k は定理ではなく、工房が負う翻訳の債務である。**

### RD-1(étale 辞書)
Ihara の $\hat\pi_1(X(\mathbf C); a,b)$ — 有限被覆のファイバー全単射の整合系として定義され、一般 Riemann 存在定理により有限エタール被覆 $X\otimes\bar{\mathbf Q}$ 上を走らせてよい(印字 103)— を、工房の $\pi_1^{\rm ét}(U_{\bar{\mathbf Q}};a,b)$ と同一視する。**Ihara は「étale fundamental group」の語を §2.3 周辺で用いない**(読解 I §0.1)。この同一視は fiber-functor 記述そのものであり無害だが、**条文には 1 行の辞書を添える**。

### RD-2(慣性語・**接基点による共役曖昧性の消去**)
Ihara は §2.3 で **"inertia" の語を使わない**。$x$ は "a small positive loop around $0$"、$y=p^{-1}\circ x'\circ p$(印字 105–106)。工房の「$0$ の慣性生成元」はこの $x$ を指す。
★ **この読み替えの実質**: 通常の基点では「$0$ の慣性部分群」は**共役類までしか定まらない**。接基点 $\vec{01}$ のもとでは、局所 Galois 群 $I_0=\mathrm{Gal}(\Omega/\bar{\mathbf Q}((\beta)))$ から $\pi_1$ への canonical な射 $\iota$ の像として**特定の部分群**が定まる。⟹ **「$0$ の慣性部分群」$:=\mathrm{im}(\iota)$ と定義する**のが工房の規約であり、この規約のもとで (TB3) の「$x$ は $0$ の慣性生成元」は「**$x$ は $\mathrm{im}(\iota)$ の位相的生成元**」を意味する。**接基点を使う理由そのものがこの一点である。**

### RD-3(Deligne の Betti / 副有限の分離)
**(15.10.1)/(15.10.2) は「Théorie classique(n° 3 à 12)」節にあり Betti 版である**($\mathbf Z(1)_B=2\pi i\mathbf Z$)。工房が引くべきは **副有限節 §15.13–15.26** と **(16.1.1) の étale 実現**である。⟹ **Betti の式番号を副有限条項の pin に使わない**(campaign FP-6 の版ずれ規律の条文化)。**位相側の番号を引いてよいのは、classique↔profinie の compatibility(15.16/15.17)を経由すると明記した箇所に限る。**

### RD-4(座標 $\beta$ の二役・**graded 模型 ↔ 完備化模型の橋**)
工房は大域座標 $\beta$ を固定し、**(i) 形式近傍を $\mathrm{Spec}\,k((\beta))$ と自明化** し **(ii) 接基点 $\vec{01}=\partial/\partial\beta$ を指定** する、という**二役を同時に負わせている**。Deligne は座標非依存の $T_s=\mathrm{Spec}\,\mathrm{Gr}(R)$(15.20.1)・$T_s^0=\mathrm{Spec}\,\mathrm{Gr}(K)$(15.20.2)を使う。橋は次の 3 本:

1. **15.20 の完備化不変性**(逐語・印字 240): 「Étendons les scalaires de $R$ à son complété $R^\wedge$ … **Ce passage au complété ne change pas $T_s$ ni les $T_{s_1}$ ($s_1\to s$) et $\mathrm{Spec}(K')_{(s)}=\mathrm{Spec}(K'^\wedge)_{(s)}$**.」
2. **15.21**(逐語・印字 240–241): 「Soit $Z$ un revêtement fini étale de $Y-y$. Sur $\mathrm{Spec}(K_y)$, il induit un revêtement fini étale, spectre d'une extension finie étale $K'$ de $K_y$. **Le revêtement induit $\mathrm{Spec}(K')_{(y)}$ de $T_y^0$ défini en 15.20 coïncide avec celui de 15.18.**」
3. **15.22**(逐語・印字 241): 「Prenons pour $\bar X$ une droite d'origine $s$ sur $k$. **L'espace tangent $T_s$ est alors canoniquement isomorphe à $\bar X$. C'est encore l'espace tangent en $s$ du complété $\bar X^\wedge$ de $\bar X$ en $s$.**」+ **15.23 LEMME**(穴あき形式円板 $X_s^\wedge$ の有限エタール被覆と穴あき直線 $X$ の有限エタール被覆が圏同値・逆関手 $R\mapsto R_{(s)}$)。

⟹ **工房の完備化模型と Deligne の graded 模型は同じ圏を与える。座標 $\beta$ の選択は、この同値の下では「どの自明化を書くか」の選択にすぎない。**
⚠ **読解 D の pin 表は 15.20 を「代数的記述」・15.21 を「曲線への適用」としか記載しておらず、この 3 本が RD-4 の一次根拠であることを立てていない**(§10 の昇格 R-3)。

### RD-5(Ihara 旧論文との基点差)
[Ih₂][A-I₂] は基点 $\vec{\infty1}$ で $x,y$ は $0,1$ のまわりのループ ⟹ **定義が微妙に異なる**(印字 114 脚注 1 逐語: 「In these papers, the base point is $\vec{\infty1}$ and $x,y$ are loops around $0,1$, respectively. So, the definitions are slightly different.」)。⟹ **本束が pin するのは ICM 版(基点 $\vec{01}$)のみ**。Ihara 系の他文献から式を輸入するときは、**この脚注を経由して規約を合わせることを条文で義務づける**。

### RD-6(★ **接基点の三者同一視 — 本束の最大の翻訳債務**)
次の 3 つを**同一の繊維関手**とみなす:

| 提示 | 定義 | 出所 |
|---|---|---|
| **Deligne 流 $\vec{01}$** | 接ベクトル $v\in T_0^0$ を基点とし、制限関手 $R\mapsto R_{(s)}$(15.13/15.15/15.18/15.20)を経由 | Deligne §15 |
| **Ihara 流 $\vec{01}$** | $\bar Y$ の $P$ での局所環の **Puiseux 級数環 $\bar{\mathbf Q}\{\{t_{ij}\}\}$ への局所埋め込み**で (i) $\mathbf P^1$ の $i$ での局所環の自明な埋め込み (ii) $P$ が定める剰余体埋め込み を延長するもの | Ihara ICM 印字 105 |
| **工房の $\mathrm{Fib}_{\vec{01}}$** | $\mathrm{Hom}_{k((\beta))\text{-alg}}\bigl(\mathcal O(W\times_U\mathrm{Spec}\,k((\beta))),\ \Omega\bigr)$、$\Omega=\bar{\mathbf Q}\{\{\beta\}\}$ | BFC v2 §2 |

★ **Ihara 流と工房のそれは逐語同一である**: BFC 補題 B-5a が $\mathcal O(W_0\times_U\mathrm{Spec}\,K((\beta)))\cong\prod_{P\mid0}\kappa(P)((s_P))$ と分解するので、$k((\beta))$-代数準同型 $\to\Omega$ は「$\lambda^{-1}(0)$ の点 $P$ を選び、$\kappa(P)((s_P))\hookrightarrow\Omega$ を選ぶ」ことに他ならない — これは Ihara の「$P$ と、そこでの branch」という記述そのものである。
⚠ **Deligne 流との同一性については、証明本文がどちらの文献にもない**: Ihara は帰属を宣言するだけ(印字 105 逐語「we proceed more "conceptually" using **Deligne's tangential base points [De]**」「**For $a,b\in\mathfrak B$, Deligne defines** $\pi_1=\pi_1(X(\mathbf C);a,b)$ and the $G_{\mathbf Q}$-action on its profinite completion.」)、Deligne は Ihara の Puiseux 実装を扱わない。
⟹ **`proof_body_status = omitted` / `omission_kind = silent_omission`**。**本束の最大の翻訳債務であり、監査点 S-1。**
★ さらに: Ihara の「**the positive real root for $t_{ij}^{1/e}$, on $I_{ij}$**」は**位相的 branch の正規化**であり、工房の $\Omega$ における記号系 $\beta^{1/n}$($(\beta^{1/mn})^m=\beta^{1/n}$・$G_{\mathbf Q}$ が全て固定 =(TB2))に対応する。**両者が同じ正規化を指すことは (TB4ᵘ) には不要**(生成元の exact 一致を要求しないため)**だが、exact (TB4)/$\varepsilon$ には必要**。⟹ **本束は前者しか主張しない。**

---

## 3. (TB1) の条項単位判定

**工房条文(BFC v2 §2 逐語)**: 有限エタール $W\to U_k$($k\subseteq\bar{\mathbf Q}$ 有限次)に対し $\mathrm{Fib}_{\vec{01}}(W):=\mathrm{Hom}_{k((\beta))\text{-alg}}(\mathcal O(W\times_U\mathrm{Spec}\,k((\beta))),\Omega)$ は $\deg(W/U)$ 個の元をもつ集合で、$\mathrm{Fib}_{\vec{01}}$ は $\pi_1(U_k,\vec{01})$-集合の圏との同値を与える(Grothendieck–Galois)。

### 3.1 条項への分解と判定

| # | 条項 | pin | `proof_body_status` | 判定 |
|---|---|---|---|---|
| **TB1-a** | $\mathrm{Fib}_{\vec{01}}(W)$ が well-defined で $\lvert\mathrm{Fib}_{\vec{01}}(W)\rvert=\deg(W/U)$ | Deligne **15.20**($K'/K$ étale $\Rightarrow$ $\mathrm{Spec}(K')_{(s)}\to T_s^0$ 有限エタール)+ **15.21**。★ **ただし工房条文は Deligne を要さず初等に閉じる**(補題 TB1-FF (a)(b)) | present(15.20/15.21)| ★ **読み替えつき一致**(RD-4)。**格の正名: これは「引用 pin」ではなく「工房内初等補題」である** — 引用化の名の下に初等事実を外部化しない |
| **TB1-b** | $\mathrm{Fib}_{\vec{01}}$ が Galois 圏 $\mathcal C_k$ の**繊維関手**(foncteur fondamental)である | ★ **番号つき pin は無い** | — | ★★ **不一致**(§3.2)。⟹ **工房側補題 TB1-FF (c) として明示する**ことを条件に「読み替えつき一致」へ回復 |
| **TB1-c** | 繊維関手が $\pi_1$-集合の圏同値を与える | ★ **Deligne 10.16**(逐語: 「Il a montré que $F_s$ induit une équivalence de catégories (revêtements finis de $X$) $\to$ ($\pi_1(X,s)^{\wedge}$-ensembles finis)」)+ **10.16 末尾**(「**les foncteurs fibres sont tous isomorphes et on pose $\pi_1(X,F)^{\wedge}=\mathrm{Aut}(F)$**」)+ 10.14(cf. SGA 1 V §4–6) | ★ **external_reference**(原本引用表記「SGA 3 V 7」/「SGA 3 V 5.7」・**印字どおり記載する**) | **読み替えつき一致** |
| **TB1-d** | $k$ 非代数閉($k\subseteq\bar{\mathbf Q}$ 有限次)でも成立 | **15.18 + (15.18.1)**(ガロア降下・char 0)。★ ただし **10.16 は任意の連結スキームで述べられている**ので圏同値自体は直接効く | present(15.18)/ external_reference(10.16) | **一致** |

### 3.2 ★ TB1-b が不一致である理由(**読解 D の「3 点 pin で閉じる」への訂正**)

読解 D §3.2 末は「**10.16(圏同値)+ 15.13/15.15/15.18(接基点繊維関手の構成)+ 15.23(局所模型)の 3 点 pin で閉じる**」と書く。**この読みは一段を飛ばしている**:

- **§15.13–15.18 が構成するのは $T_s^0$ の有限エタール被覆への制限関手 $R\mapsto R_{(s)}$ であって、繊維関手ではない。** 15.13 の目標宣言は逐語「on se propose de construire un **foncteur 15.2(A)** attachant à un revêtement fini étale $R$ de $X$ un **revêtement fini étale $R_{(s)}$ de $T_s^0$**」であり、値は**集合ではなく被覆**である。
- **§10.16 の $F_s$ は通常の点 $s\in X$ での繊維関手**である。$\mathrm{Fib}_{\vec{01}}$ にこれを適用するには「$\mathrm{Fib}_{\vec{01}}$ が繊維関手である」が要る。
- **10.16 末尾の「les foncteurs fibres sont tous isomorphes et on pose $\pi_1(X,F)^{\wedge}=\mathrm{Aut}(F)$」は、任意の繊維関手 $F$ に対して $\pi_1(X,F)$ を定義してよいことを与える** ⟹ **前提「$F$ が繊維関手」が満たされれば pin は閉じる**。

⟹ **足りないのは 1 段だけであり、それは初等である。** 以下に書き下す。

### 3.3 ★ 工房側補題 **TB1-FF**(繊維関手性・**本束が工房に負わせる債務 1/3**)

記号: $k\subseteq\bar{\mathbf Q}$ 有限次、$U=\mathbf P^1_k-\{0,1,\infty\}$、$\beta$ = 標準座標、$\Omega=\bar{\mathbf Q}\{\{\beta\}\}=\bigcup_n\bar{\mathbf Q}((\beta^{1/n}))$、$j:\mathrm{Spec}\,k((\beta))\to\mathbf P^1_k$ を $k[\beta]\hookrightarrow k((\beta))$ が定める射、$\mathcal C_k:=$($U_k$ 上の有限エタール被覆)。

> **補題 TB1-FF.**
> **(a)** $j$ は $U$ を経由する。
> **(b)** $W\to U$ が有限エタール次数 $d$ なら $A_W:=\mathcal O(W\times_U\mathrm{Spec}\,k((\beta)))$ は $k((\beta))$ 上次数 $d$ の有限エタール代数であり、$\lvert\mathrm{Hom}_{k((\beta))\text{-alg}}(A_W,\Omega)\rvert=d$。
> **(c)** $\mathrm{Fib}_{\vec{01}}:=\mathrm{Hom}_{k((\beta))\text{-alg}}(A_{(-)},\Omega)$ は $\mathcal C_k$ の繊維関手である。

**証明.**
**(a)** $\beta\in k((\beta))^\times$(逆元 $\beta^{-1}$)、$\beta-1=-(1-\beta)$ で $1-\beta\in k[[\beta]]^\times$。ゆえに $j$ の像は $\{0,1,\infty\}$ を避ける。(BFC 補題 B-5a の証明が同じ論法を使っている。)
**(b)** 有限エタール性は底変換で保たれるので $W\times_U\mathrm{Spec}\,k((\beta))\to\mathrm{Spec}\,k((\beta))$ は次数 $d$ の有限エタール、すなわち $A_W$ は $k((\beta))$ 上次数 $d$ の有限エタール代数。$\bar{\mathbf Q}$ が代数閉・char 0 ゆえ **Puiseux(Newton–Puiseux)の定理**により **$\Omega$ は代数閉体**であり、$k((\beta))\subseteq\bar{\mathbf Q}((\beta))\subseteq\Omega$。$A_W$ が étale ゆえ $A_W\otimes_{k((\beta))}\Omega\cong\Omega^{d}$、したがって
$$\lvert\mathrm{Hom}_{k((\beta))\text{-alg}}(A_W,\Omega)\rvert=\lvert\mathrm{Hom}_{\Omega\text{-alg}}(A_W\otimes\Omega,\Omega)\rvert=d.$$
> ⚠ **精密化(自認)**: 「$\Omega$ は $k((\beta))$ の**代数閉包**」と書いてはならない。$k$ が真の数体なら $\bar{\mathbf Q}((\beta))$ は $k((\beta))$ 上代数的でない(係数が生成する拡大が無限次になりうる)。必要かつ十分なのは「**$\Omega$ が $k((\beta))$ を含む代数閉体である**」ことだけで、上の計数はそれで足りる。($k=\bar{\mathbf Q}$ の場合に限り $\Omega$ は $\bar{\mathbf Q}((\beta))$ の代数閉包であり、これは §4.3 の TB4-INJ で使う。)

**(c)** $\mathrm{Fib}_{\vec{01}}=F_\Omega\circ j^*$ と分解する。$j^*:\mathcal C_k\to\mathcal C_{k((\beta))}$ は底変換ゆえ Galois 圏の射(有限極限・有限余極限を保つ)。$F_\Omega$ は $\mathcal C_{k((\beta))}$ の標準繊維関手。合成は有限集合値で完全。**保存性**(同型を反映する)は次で従う: $k[\beta,\beta^{-1},(\beta-1)^{-1}]\to k((\beta))$ は単射ゆえ $j$ は $U$ の生成点 $\eta$ を hit する。$f:W\to W'$ を $\mathcal C_k$ の射とし $j^*f$ を同型とする。$k(U)\to k((\beta))$ は体の拡大ゆえ忠実平坦で、$j^*f$ が生成ファイバーの底変換であることから $f_\eta$ は同型。$U$ は連結正規、$W,W'$ は $U$ 上有限エタールゆえ正規かつ $U$ 上有限で、**連結正規底上の有限エタール被覆は生成ファイバーで決まる**($\mathrm{Hom}_U(W,W')\to\mathrm{Hom}_{k(U)}(W_\eta,W'_\eta)$ が全単射)から $f$ 自身が同型。∎

> ★ **格の申告**: TB1-FF は **紙・初等・単系統**であり、Sol 監査未。**「引用で閉じた」の一部ではなく、工房が自前で埋める一段である。**

### 3.4 (TB1) の総合

$$\boxed{\ \textbf{(TB1)} = \underbrace{\text{Deligne 10.16}}_{\text{external\_reference}} + \underbrace{\text{補題 TB1-FF}}_{\text{工房・初等}} + \underbrace{\text{RD-4}}_{\text{graded}\leftrightarrow\text{完備化}}\ }$$

⚠ **二重の external_reference を避けたい場合の第二経路**: **SGA1 V**(在庫: `papers/sga1-grothendieck-raynaud-arxiv0206203.pdf`・LEDGER 記録あり)に直接 pin する。**本束は両方を提示し、選択は司令塔・Sol に委ねる。**(私の意見: Deligne 10.16 は「工房が使う副有限理論の言語をまとめて宣言する箇所」であり読み手に親切だが、`proof_body_status` を `present` に着地させたいなら SGA1 V が要る。**私は SGA1 を 1 頁も開いていない**。)⟹ **監査点 S-2(委嘱名指し)。**

---

## 4. (TB4ᵘ) の条項単位判定

**工房条文(BFC v2 §2・便 44 F7.2 の指定形 逐語)**: 局所慣性 $I_0=\mathrm{Gal}(\Omega/\bar{\mathbf Q}((\beta)))$ の $\pi_1$ への像は $\overline{\langle x\rangle}$ であり、その作用は $\Omega$ への後合成(左作用)である。**ただし選んだ生成元 $\sigma_\zeta$ と $x$ の exact な一致は要求しない。**

### 4.1 条項への分解と判定

| # | 条項 | pin | `proof_body_status` | 判定 |
|---|---|---|---|---|
| **TB4ᵘ-α** | $I_0=\mathrm{Gal}(\Omega/\bar{\mathbf Q}((\beta)))\cong\hat{\mathbf Z}(1)$ | ★ **15.23 PREUVE**(逐語「par le lemme d'Abhyankar, on a $\pi_1(X)=\pi_1(X_s^\wedge)=\hat{\mathbf Z}(1)$」— **工房が要る側($X_s^\wedge$ = 穴あき形式円板)が逐語で書かれている**)+ **14.2** の ℓ-adique 実現(「Le $\pi_1$ profini est donc la limite projective $\hat{\mathbf Z}(1)$ des noyaux $\mu_n$」) | present + external_reference(Abhyankar) | **読み替えつき一致**(RD-4)。★ **ただし $(\alpha)$ 自体は Kummer 理論で初等**($\Omega=\bigcup\bar{\mathbf Q}((\beta^{1/n}))$・$\mathrm{Gal}=\varprojlim\mu_n$)⟹ **引用は canonicity のためであって存在のためではない** |
| **TB4ᵘ-β** | canonical な射 $\iota:I_0\to\pi_1(U_{\bar{\mathbf Q}},\vec{01})$ が存在し、それが**制限関手が誘導する標準射**である | ★ **(16.1.1)**(逐語・150 dpi 画像照合済: $\pi_1(T_s^0,v)_{\rm mot}\to\pi_1(X,v)_{\rm mot}$, 「**correspondant, dans les diverses théories du $\pi_1$, au foncteur de restriction de $X$ à $T_s^0$**」)+ 副有限節だけで閉じる第二経路 **15.20+15.21+15.22+15.23** | present | ★ **読み替えつき一致**(§4.2)。**これが (TB4ᵘ) で唯一の真の引用 pin** |
| **TB4ᵘ-γ** | $\mathrm{im}(\iota)=\overline{\langle x\rangle}$ | ★ **Deligne 単独では書けない**($x$ を導入しない)。分解 = (γ1) $\iota$ 単射(**工房補題 TB4-INJ**)+ (γ2) $x$ が $\mathrm{im}(\iota)$ の位相的生成元(**RD-2 の読み替え** + **15.17 CONSTRUCTION**) | — / present(15.17) | ★★ **読み替えつき一致**。かつ ★ **(TB1)+(TB3)+RD-2 から従う**(§4.3)⟹ **独立仮定としての内容が消える** |
| **TB4ᵘ-δ** | 作用が $\Omega$ への後合成(左作用) | **工房の $\mathrm{Fib}$ 定義の tautology**。Deligne 側の対応は 10.16($\pi_1=\mathrm{Aut}(F)$)・15.9(classique 版逐語「le groupe des automorphismes du foncteur $R\mapsto R_t$」) | — | **一致(内容ゼロ)**。§4.4 |

### 4.2 ★ (TB4ᵘ-β) — 読解 D が「判断しない」とした §16.1 の前提を**独立に判定した**

読解 D §2.2 の ⚠ は「(16.1.1) の置かれた §16.1 は $X=\mathbf P^1_{\mathbf Q}-S$・良還元の文脈で述べられている … この選択は数学者/司令塔の専権」として判断を留保する。**私は判定する。**

**原文(印字 255・PDF 177・私が 150 dpi 画像で照合)**:
> 「**16.1.** Soient $\mathbf P^1_{\mathbf Q}$ la droite projective sur $\mathbf Q$, $S$ un ensemble fini non vide de points rationnels et $X:=\mathbf P^1_{\mathbf Q}-S$. Soit $b$ un point base défini sur $\mathbf Q$. **Si $(X,b)$ a bonne réduction sur un ouvert $U$ de $\mathrm{Spec}(\mathbf Z)$, on a défini en 13.3 à 13.7 le $\pi_1$ motivique $\pi_1(X,b)_{\rm mot}$** comme un schéma en groupes prounipotent …」

⟹ ★ **良還元の仮定は「$\pi_1$ motivique を定義した」という文の条件節である** — (16.1.1) の存在条件ではなく、**motivique 対象が定義できるための条件**である。

さらに工房の設定では前提が**逐語で充足される**:
- $S=\{0,1,\infty\}$ は $\mathbf P^1(\mathbf Q)$ の有限非空集合 ✓
- ★ **良還元**: $0,1,\infty$ の 3 切断は $\mathrm{Spec}\,\mathbf Z$ の**全ファイバーで互いに相異なる**($0\not\equiv1\bmod p$ が全素数 $p$ で成立・$\infty$ は別)⟹ **$U=\mathrm{Spec}\,\mathbf Z$ 全体で良還元** ✓
- $b=\vec{01}=\partial/\partial\beta$ は $\mathbf Z$ 上定義された接ベクトル ✓

$$\Longrightarrow\ \boxed{\ \textbf{§16.1 の前提は工房の}\ U=\mathbf P^1_{\mathbf Q}-\{0,1,\infty\}\ \textbf{で literally 充足される。読解 D の ⚠ は本設定では解消する。}\ }$$

⚠ **ただし残る 1 点(監査点 S-3(d))**: (16.1.1) の両辺は **$_{\rm mot}$ 添字つき**(画像で確認)であり、工房が要るのはその **étale(profinie)実現**である。「diverses théories du $\pi_1$」に profinie が含まれるという読みは §10.1 の 3 理論の列挙に依るが、**読解 D の §10.1 照合はテキストのみ**(読解 D §5.3-1)。

★ **⟹ 本束は motivique 依存を避ける二段構えを推奨する**:
$$\underbrace{\text{15.20 + 15.21 + 15.22 + 15.23}}_{\textbf{副有限節だけで制限関手が閉じる}}\ +\ \underbrace{\text{(16.1.1)}}_{\textbf{その射に名前と canonicity を与える}}$$
第 1 段は副有限節の中で完結し(15.21 逐語が「有限エタール被覆 $Z\to Y-y$ から $\mathrm{Spec}(K_y)$ 上の有限エタール $K'$ が誘導され、$\mathrm{Spec}(K')_{(y)}$ が $T_y^0$ の被覆として 15.18 のそれと一致する」と述べる)、**motivique にも良還元にも依存しない**。⟹ **(16.1.1) を pin から外しても (TB4ᵘ-β) は立つ**(私の判定・監査点 S-3)。

### 4.3 ★★ (TB4ᵘ-γ) は (TB1)+(TB3) から従う — **BFC §12.1「追加の論点(便 44 F7.2)」への一段**

BFC v2 §12.1 末は逐語: 「**「(TB1)+(TB3) の『inertia generator』という語から (TB4ᵘ) が既に従う」と主張するなら、その導出を一段書く必要がある。本稿は現状 (TB4ᵘ) を独立の枠組み仮定として立てている**(§14.1-2)。」

**その一段を書く。**

> #### 工房側補題 **TB4-INJ**($\iota$ の単射性・**債務 2/3**)
> $\iota:I_0=\mathrm{Gal}(\Omega/\bar{\mathbf Q}((\beta)))\to\pi_1(U_{\bar{\mathbf Q}},\vec{01})=\mathrm{Aut}(\mathrm{Fib}_{\vec{01}})$ は単射。
> **証明.** $n\ge1$ に対し $W_n:=\{(\beta,t)\in U\times\mathbf A^1:\ t^n=\beta\}$ と置く。$\beta\in\mathcal O(U)^\times$・char 0 ゆえ $W_n\to U$ は次数 $n$ の有限エタール。$A_{W_n}=\bar{\mathbf Q}((\beta))[T]/(T^n-\beta)=\bar{\mathbf Q}((\beta^{1/n}))$ で、$\mathrm{Fib}_{\vec{01}}(W_n)=\{\zeta\,\beta^{1/n}:\zeta\in\mu_n\}$。$\sigma\in\ker\iota$ は全ての $n$ で $\beta^{1/n}$ を固定するので $\sigma\in\mathrm{Gal}(\Omega/\bigcup_n\bar{\mathbf Q}((\beta^{1/n})))=\mathrm{Gal}(\Omega/\Omega)=1$。∎
> ★ **この証明は $x$ の名前を一度も使わない**(循環がない)。

> #### 導出 **TB4-GEN**((γ) の一段)
> **RD-2** により、接基点 $\vec{01}$ のもとで「$0$ における慣性部分群」は $\mathrm{im}(\iota)$ と定義される(共役の曖昧さがない)。**TB4-INJ** より $\mathrm{im}(\iota)\cong\hat{\mathbf Z}(1)$ は procyclic。**(TB3)** の「$x$ は $0$ の慣性生成元」は、この規約のもとで「**$x$ は $\mathrm{im}(\iota)$ の位相的生成元**」を意味する。ゆえに
> $$\mathrm{im}(\iota)=\overline{\langle x\rangle}.$$
> **この読み替えの正当性**(= Ihara の位相的 $x$ が実際に $\mathrm{im}(\iota)$ を位相生成すること)は次の 3 本の合成で支えられる:
> (i) Ihara の $x$ が基点 $\vec{01}$ の**小ループ**として定義されている(印字 105–106);
> (ii) 位相側と副有限側の制限関手が一致する — **15.17 CONSTRUCTION**(逐語・印字 238: 「Si $k=\mathbf C$, l'espace des points $R_{(s)}(\mathbf C)$ du revêtement $R_{(s)}$ de $T_s^0$ est le revêtement $R(\mathbf C)_{(s)}$ de 15.7」)+ **15.16 LEMME**;
> (iii) 位相側で $\pi_1(T_s^0,t)\to\pi_1(X,t)$ の像が $t$ を基点とする小ループの生成する部分群であること — **(15.10.1)** + **15.9**(RD-3 により、位相側の番号を引くのはここだけと明記して引く)。
> ★ **ここで「正(positive)」の語は要らない**: (TB4ᵘ) は生成元の exact 一致を要求しないので、必要なのは「$x$ が位相的生成元である」だけであり、**向きの正規化には依存しない**。⟹ **§4.5 の $\mu_s$ 指示対象の曖昧さ(S-4)は (TB4ᵘ) に影響しない。**

$$\Longrightarrow\ \boxed{\ \textbf{(TB4}^{\rm u}\textbf{) の独立仮定としての内容は}\ (\alpha)(\beta)(\delta)\ \textbf{に縮み、うち}\ (\alpha)\ \textbf{は初等・}(\delta)\ \textbf{は定義・真の引用 pin は}\ (\beta)\ \textbf{の 1 本。}\ }$$

⚠ **この縮約は BFC §14.1-2 の現状記述(「(TB4ᵘ) を独立の枠組み仮定として立てている」)を更新しうる。⟹ 監査点 S-3。本束は BFC 本文を改変しない。**

### 4.4 (TB4ᵘ-δ) — 「後合成が左作用」は数学的内容ゼロ

$\mathrm{Fib}_{\vec{01}}(W)=\mathrm{Hom}_{k((\beta))\text{-alg}}(A_W,\Omega)$ 上の $\mathrm{Gal}(\Omega/\bar{\mathbf Q}((\beta)))$ の作用は $\sigma\cdot f:=\sigma\circ f$ で、$(\sigma\tau)\cdot f=\sigma\circ(\tau\circ f)=\sigma\cdot(\tau\cdot f)$ ⟹ **左作用**。**これは工房の定義から直ちに従う。**

★ **重要な帰結(【文献要請 13】(ii) 縮小形の射程訂正)**: BFC §12.1 の【文献要請 13】(ii) の縮小形は逐語「**正の位相 transport が algebraic fiber functor の後合成左作用へ送られ、逆作用ではない**ことの標準比較定理・記法確認」である。これは (δ)(左作用であること)ではなく、**比較同型 $\pi_1^{\rm top}\to\mathrm{Aut}(\mathrm{Fib})$ が準同型か反準同型かという「向き」の問題**である。反準同型なら $x\mapsto$ その逆元、すなわち $\varepsilon\mapsto-\varepsilon$。⟹ **(TB4ᵘ) は生成元を固定しないのでどちらでも生き残る** ⟹ $$\boxed{\ \textbf{【文献要請 13】(ii) の縮小形は (TB4}^{\rm u}\textbf{) の射程外であり、exact (TB4)}/\varepsilon\ \textbf{側の要請である。}\ }$$

### 4.5 ★ (TB4ᵘ) の $\varepsilon$ 非固定 — F7.2 分解との構造整合(**画像照合で 1 点精密化**)

**campaign v1 FP-7 / 読解 D §4 の読み**(= Deligne の canonical な言明はすべて $\mathbf Z(1)$ を源とする射で書かれ、$\hat{\mathbf Z}(1)\cong\hat{\mathbf Z}$ の自明化は本文のどこでも固定されない)を、**私も独立に確認した**:

- §15 冒頭の $\mu_0:\mathbf Z(1)\to\pi_1(X,t)_{\rm mot}$、(15.10.2) $\mathbf Z(1)_B\to\pi_1(X,t)$、(16.1.2) $\mu_s:\mathbf Z(1)\to\pi_1(X,v)_{\rm mot}$ — **すべて源が $\mathbf Z(1)$**(150 dpi 画像で (16.1.2) を確認)。
- 自明化(生成元の指定)が現れるのは**実現ごとの記述のみ**: Betti では「le générateur $2\pi i$ de $\mathbf Z(1)_B$」、ℓ-adique では 14.2 の系。

⟹ **$\varepsilon$ = $\mathbf Z(1)$ の自明化の自由度**という工房の同定(便 44 F7.2)は Deligne の記法と構造的に整合する。**新規主張ではない**(campaign FP-7 の追認)。

★ **本束が 1 点精密化する(新規・読解 D 未申告)**: Betti 正規化文の**水準**である。150 dpi 画像の逐語配置は

> (16.1.2) $\mu_s:\mathbf Z(1)\to\pi_1(X,v)_{\rm mot}$.
> 「Par passage au $\pi_1$ rendu abélien, indépendant du point base, les morphismes (16.1.2) induisent **en homologie**
> (16.1.3) $\mu_s:\mathbf Z(1)\to H_1(X)_{\rm mot}$.
> **En réalisation de Betti, $\mu_s$ envoie le générateur $2\pi i$ de $\mathbf Z(1)_B$ sur un petit lacet positif $\sigma_s$ autour de $s$. En homologie, les $\sigma_s$ ont pour seule relation $\sum\sigma_s=0$.**」

⟹ ★ **$\mu_s$ は (16.1.2)($\pi_1$ 水準)と (16.1.3)($H_1$ 水準)の両方の名前であり、正規化文の直前の定義は (16.1.3) である。** 「un petit lacet positif」という語は $\pi_1$ 水準の対象を指すが、**この文の $\mu_s$ の指示対象は原文で一意でない。**

$$\Longrightarrow\ \boxed{\ \textbf{(TB4}^{\rm u}\textbf{) は}\ \varepsilon\ \textbf{を固定しないので本束は無傷。だが exact (TB4)}/\varepsilon\ \textbf{を将来引用で閉じようとするなら、この 1 行が最初の障害である。}\ }$$
⟹ **監査点 S-4。**(現行の供給元 `Z-norm-seal/v1` + retained TB4-3/A3 framework は本束によって**一切変更されない**。)

---

## 5. (TB3) の条項単位判定

**工房条文(BFC v2 §2 逐語)**: $\pi_1(U_{\bar{\mathbf Q}},\vec{01})\cong\hat F_2=\langle x,y\rangle$、$x,y,z=(xy)^{-1}$ はそれぞれ $0,1,\infty$ の慣性生成元、$xyz=1$。

### 5.1 条項への分解と判定

| # | 条項 | pin(Ihara ICM 1990・読解 I の 400 dpi 転記に依拠) | `proof_body_status` | 判定 |
|---|---|---|---|---|
| **TB3-a** | $\pi_1(U_{\bar{\mathbf Q}},\vec{01})\cong\hat F_2$(副有限自由・階数 2) | 「**This group is free on $x,y$.**」(印字 106)+「$\hat\pi_1(X(\mathbf C),\vec{01})=\hat F_2$」((2.3.2) 直前・同頁)+ $\hat\pi_1$ の整合系記述と GRET(印字 103) | ★ **omitted / silent_omission**(§5.2) | **読み替えつき一致**(RD-1) |
| **TB3-b** | $x,y$ が $0,1$ の慣性生成元(基点 $\vec{01}$) | $p$・$x$・$x'$・$y=p^{-1}\circ x'\circ p$ の定義文(印字 105–106)+ 挿絵 | present(構成) | **一致**(RD-2 経由) |
| **TB3-c** | $z=(xy)^{-1}$ が $\infty$ の慣性生成元 | ★ **括弧書き 1 語のみ**: 「$z=(xy)^{-1}$ **(a loop around $\infty$)**」(印字 106 Remark) | ★ **omitted / silent_omission** | ★ **読み替えつき一致(弱い)**(§5.3) |
| **TB3-d** | $xyz=1$ | $z:=(xy)^{-1}$ の**定義から自明**。Ihara の (3.1.1)(II) も「**if** $xyz=1$」と条件節で書く | — | **一致(定義)**。§5.4 |

### 5.2 ★ (TB3-a) の `proof_body_status` は `omitted` である

- Ihara は §2.2 で「$P_4\simeq F_2$ (free, rank 2)」、§2.3 で「This group is free on $x,y$」と**宣言する**が、**証明を付けていない**(読解 I の転記範囲に証明本文なし)。
- **副有限自由性**($\hat F_2$)は「自由群の副有限完備化」という**記号の定義**であって、$\pi_1^{\rm ét}$ との同一視は RD-1(GRET)を経由する。
- Deligne 序論(印字 84)の自由生成の図は **動機づけの記述であって主張ではない**(campaign v1 §6.5 の判定を私も支持する)。

⟹ ★ **(TB3-a) は「引用 pin 済」だが「証明本文つき pin」ではない。** `proof_body_status = omitted`(`omission_kind = silent_omission`・`source_wording` = 上の逐語)。**第二 pin が欲しければ SGA1**(Exp. XIII の tame $\pi_1$ / Riemann 存在定理・在庫あり)**が候補**だが、**本束はそこまで進まない**(委嘱の範囲外・司令塔の判断事項)。

### 5.3 ★ (TB3-c) の pin は弱い — **読解 I の「供給する 3/3」への訂正**

読解 I §5.1 は条項 (a)(b)(c) の 3 つを「○」とするが、**その (c) は「接基点の固定」**(𝔹・Puiseux branch・positive real root・[De])であって、**工房条文の第 3 の慣性生成元($z$)ではない**。工房の (TB3) 条文には「$z$ が $\infty$ の慣性生成元」という条項が独立に立っており、**これに対する Ihara の供給は括弧書き 1 語である**。

| 何が pin されるか | 何が pin されないか |
|---|---|
| $z=(xy)^{-1}$ が「$\infty$ のまわりのループ」であること(括弧書き) | ★ **$z$ が $\infty$ の慣性部分群の位相的生成元であること**(明文なし) |
| | ★ **$\infty$ の慣性の「どの共役」か**($y$ に対する $p$ による transport のような明示がない) |

★ **軽減(重要)**: **(5′) 証明鎖(定理 B-4・系 B-4c・補題 B-5/B-5ᵘ)は $z$ を使わない。** 使うのは (TB3-a)($\hat F_2$ の同定・定理 B-4 の第 1 行)と (TB3-b) の **$x$ 側のみ**(補題 B-5b)。$z$ が要るのは **passport / M2-GEO / 命題 B-9(モデル認識の三つ組 $(\sigma_0,\sigma_1,\sigma_\infty)$)** であり、それらは ASM の**層 1/層 2 の別行**である。

$$\Longrightarrow\ \boxed{\ \textbf{(TB3-c) は本束(= (5}'\textbf{) 鎖)の射程外。pin の弱さを明示したまま残し、passport 側で使うときに別途 pin を要求する。}\ }$$

### 5.4 (TB3-d)「$xyz=1$」の読み方(**注記・修文提案ではない**)

BFC v2 §2 の条文は「$x,y,z=(xy)^{-1}$ はそれぞれ $0,1,\infty$ の慣性生成元、$xyz=1$」と**並列に**書くため、$xyz=1$ が独立の内容をもつように読める。**もたない**: $z$ は $(xy)^{-1}$ と定義されているので $xyz=1$ は恒等式である。**内容はすべて (TB3-c)(その $z$ が $\infty$ の慣性生成元であること)に入っている。**
⟹ **本束は BFC 本文を改変しない。**依存表(§6)では $xyz=1$ を独立行に立てず、(TB3-c) に吸収する。

---

## 6. 依存表の引用差替版 —(5′) 証明鎖(**additive erratum 方式・本文不改変**)

> **方式**: BFC v2 §6.2(定理 B-4)・§6.3(系 B-4c)・§7/§7.1(補題 B-5 / B-5ᵘ)の**本文は 1 バイトも改変しない**。以下は「証明本文のこの箇所で『仮定 (TBk) による』と読める部分を、文献 pin へ差し替えた対応表」である(CV-10 の erratum 運用・F97-1.1 で承認済の方式)。

### 6.1 定理 B-4(a)($K$-版・剛性 descent)

| 証明中の箇所(BFC §6.2) | 現行の依存表記 | ★ **引用差替版** |
|---|---|---|
| 「(TB2) の分裂により $\pi_1(U_K,\vec{01})=\hat F_2\rtimes_\alpha G_K$ と書ける」— **$\hat F_2$ 部分** | (TB3) | **Ihara ICM §2.3**(印字 105–106・「This group is free on $x,y$」+「$\hat\pi_1(X(\mathbf C),\vec{01})=\hat F_2$」)経由 **RD-1**。`proof_body_status = omitted(silent_omission)` |
| 同 — **分裂 $s_{\vec{01}}$** | (TB2) | ★ **工房規約**(BFC §2 末の逐語「これは当工房が §1.1 で置いた規約」)⟹ **引用対象外**。差し替えない |
| 同 — **半直積(完全列)** | ★ **どの TB にも明示されていない** | ★★ **【GAP-TB-EXACT】**(§6.4・**本束で新規に浮上**) |
| 「(TB1) より、求める $K$-モデルは $\mathcal H\le\hat F_2\rtimes G_K$ 開部分群と 1:1 に対応する」 | (TB1) | ★ **Deligne §10.16**(圏同値・`external_reference`・原本表記「SGA 3 V 7」)+ **補題 TB1-FF**(工房・初等)+ **RD-4**。**[C-1]** |
| 補題 B-4a / B-4b・cocycle 条件・部分群性・閉性/開性・逆元・一意性 | — | **TB 非依存**(純群論・副有限群論)。差し替えなし |

### 6.2 系 B-4c(= FC-3)

| 証明中の箇所(BFC §6.3) | 現行の依存表記 | ★ **引用差替版** |
|---|---|---|
| 「**(TB4) が採る「$\Omega$ への後合成」は左作用**なので、stabilizer $\mathcal H$ をもつ推移的 $\pi_1$-集合は左剰余類空間」 | (TB4) | ★ **$\mathrm{Fib}_{\vec{01}}$ の定義(BFC §2)の tautology**(§4.4)+ **Deligne §10.16**($\pi_1=\mathrm{Aut}(F)$)。⟹ **exact (TB4) を呼ぶ必要がない — (TB4ᵘ-δ) で足りる**(★ 指摘・§6.5) |
| 「左剰余類空間 $\cong\pi_1(U_K,\vec{01})/\mathcal H$((TB1))」 | (TB1) | **[C-1]** と同じ |
| $G_K$-同変性「(接基点の定義そのもの)」 | (TB2) | **工房規約** ⟹ 引用対象外 |
| $\tilde\Lambda\cong\Lambda$・$L_X\leftrightarrow\tau(\zeta_M)$ | (W) 側 + Rule 1 命名 | **TB 非依存**。差し替えなし |

### 6.3 補題 B-5ᵘ(= B-5 の (i)(ii-loc)(iii)(7.1)(7.2))

| 証明中の箇所(BFC §7・§7.1) | 現行の依存表記 | ★ **引用差替版** |
|---|---|---|
| 補題 B-5a(繊維の分解 $\prod_{P\mid0}\kappa(P)((s_P))$) | — | **TB 非依存**(可換代数: 有限 $R$-加群の完備化 + CRT)。★ **ただしこの分解が RD-6 の要**(Ihara の branch の代数的定義との逐語一致) |
| 補題 B-5b「$\mathrm{Gal}(\Omega/\bar{\mathbf Q}((\beta)))=\hat{\mathbf Z}(1)$ が $e_P$ 個の埋め込みを推移的に置換」 | (TB4) | ★ **Deligne 15.23 PREUVE**(逐語「$\pi_1(X)=\pi_1(X_s^\wedge)=\hat{\mathbf Z}(1)$」)+ **14.2**(ℓ-adique 実現)。**[C-2]**。★ 推移性自体は局所体論(全分岐拡大の $\Omega$ への埋め込みへの Galois 作用) |
| 「$\langle x\rangle$-軌道の個数と長さ」を (W4) の $\langle X\rangle$-軌道と読む | (TB3)+(TB4) | ★ **(TB4ᵘ-γ)** = **RD-2 + TB4-INJ + TB4-GEN**(§4.3)⟹ **(TB1)+(TB3) から従う** |
| (i)$\lambda^{-1}(0)=\{P_0\}$・$K$-有理・$e=M$ | (W4) + B-5b | 上の 2 行の合成 |
| (ii-loc) uniformizer 取り替え | — | **TB 非依存**(初等) |
| (iii)(7.1) 完備化・Eisenstein・$\Omega$ の根の集合 | — | **TB 非依存**($\Omega$ の定義のみ) |
| (7.2) $\gamma\in G_K$ の作用は係数作用のみ | (TB2) | **工房規約** ⟹ 引用対象外 |

### 6.4 ★★ 新規に浮上した未 pin 項目 —【GAP-TB-EXACT】

> **【GAP-TB-EXACT】** 同所性完全列
> $$1\longrightarrow\pi_1(U_{\bar{\mathbf Q}},\vec{01})\longrightarrow\pi_1(U_K,\vec{01})\longrightarrow G_K\longrightarrow1$$
> は、**BFC v2 §2 の悉皆リスト (TB1)–(TB4) に明示されていない**が、**§6.2 の証明の第 1 行が使う**(「$\pi_1(U_K,\vec{01})=\hat F_2\rtimes_\alpha G_K$ と書ける」)。BFC §2 は逐語「**本稿が接基点の理論から使う性質を全部列挙する。以後これ以外は使わない(使ったら誤り)**」と宣言しているので、**これは列挙漏れである**。
> **弁護できる読み**: (TB2) が「分裂 $s_{\vec{01}}:G_{\mathbf Q}\to\pi_1(U_{\mathbf Q},\vec{01})$ を与える」と言う時点で、全射 $\pi_1\to G_{\mathbf Q}$ が前提されている ⟹ **(TB2)+(TB3) に含意されているとみなす**ことは可能。
> **私の推し**: ★ **隠さず【GAP-TB】の第 4 項目として立てる**(規律 5)。**pin 候補** = Deligne **10.17–10.19**(相対版 groupoid $P(X/k)^\wedge=\varprojlim P_A^0$・(10.19.1)(10.19.2)・⚠ **読解 D の照合はテキストのみ**)/ **SGA1 IX**(在庫あり)。
> ⟹ **監査点 S-5。**

### 6.5 ★ (5′) 鎖の依存の最終形(**引用差替後**)

| 種別 | 項目 | 供給元 |
|---|---|---|
| **[C-1] 外部文献** | 繊維関手 $\to$ $\pi_1$-集合の圏同値 | **Deligne §10.16**(`external_reference`「SGA 3 V 7」)/ 代替 = SGA1 V |
| **[C-2] 外部文献** | 局所 $\pi_1$($=\hat{\mathbf Z}(1)$)と全分岐埋め込みへの推移作用 | **Deligne §15.23 PREUVE + 14.2**(`present` + Abhyankar が `external_reference`) |
| **外部文献(構造)** | 制限関手 $R\mapsto R_{(s)}$ の canonical 性 | **Deligne 15.20/15.21/15.22/15.23**(`present`)+ **(16.1.1)**(`present`・命名) |
| **外部文献($\hat F_2$)** | $\pi_1^{\rm geom}\cong\hat F_2=\langle x,y\rangle$・$x$ が $0$ の慣性生成元 | **Ihara ICM §2.3**((a) は `omitted`・(b) は `present`) |
| **工房規約** | (TB2)(根系・係数作用・分裂)・RD-2(慣性 $:=\mathrm{im}(\iota)$) | BFC §1.1・§2 |
| **工房初等補題(債務 3 本)** | **TB1-FF**(繊維関手性)・**TB4-INJ**($\iota$ 単射)・**TB4-GEN**($x$ が $\mathrm{im}(\iota)$ を位相生成) | 本束 §3.3・§4.3 |
| ★ **未 pin** | **【GAP-TB-EXACT】** 同所性完全列 | §6.4 |
| **射程外(本鎖で非 load-bearing)** | **(TB3-c)** $z$ の $\infty$-慣性 / **exact (TB4)**・$\varepsilon$ / $(Z_{2M}$-link$)$ | §5.3 / BFC §12.1(現行の供給元は不変) |

★ **副産物の指摘 2 件**(**BFC 本文は改変しない・司令塔の裁定事項**):
1. **系 B-4c の証明文は「(TB4) が採る」と書くが、実際に使うのは (TB4ᵘ-δ) だけ**である ⟹ 依存欄を **(TB4ᵘ)** へ弱められる。
2. **定理 B-4(a) の依存欄「(TB1)–(TB3)」のうち (TB3) は「$\hat F_2$ の同定」だけを使い、慣性生成元条項は使わない**(慣性が効くのは B-5b 側)⟹ 解像度を上げられる。

---

## 7. 格の更新案(**発効は Sol 検収後**)

### 7.1 更新の対象と、**動かさないもの**

| 動かす | 動かさない |
|---|---|
| ASM v2 **§V.2.4** の **TB1–TB4 行**の格欄・pin 欄 | ★ `candidate`(ASM 全体)は**動かない** |
| ASM v2 §V.2.4 の **BFC 行 / B-5$_{\rm loc}$ 行**の「相対」の中身 | ★ `verified` は**付けない**(Lean 未到達) |
| CLAIMS **W3-17** の状態欄(追記のみ) | ★ **exact (TB4)・$(Z_{2M}$-link$)$ の欄は 1 文字も動かない**(本束の射程外) |
| | ★ **矢印・主張・domain は 1 つも動かない**(追記 C 案 §設計方針 2 と同流儀) |

### 7.2 ★ 札文言案(3 本)

> #### **(N-1)** ASM §V.2.4 の **TB1–TB4 行**
> **現行**: 格 = 「★ **枠組み仮定**(自前再導出はするが Lean 化しない)」/ pin = 「【GAP-TB】」
> **★ 案**:
> ```text
> 格:  framework assumption — TB1 / TB3 / TB4^u は canonical-source-pinned (v1)
>      (exact TB4 と Z_{2M}-link は本 pin の射程外・現行の供給元のまま)
> pin: Deligne 1989 §10.16 (圏同値・external_reference "SGA 3 V 7")
>      Deligne 1989 §15.20 / 15.21 / 15.22 / 15.23 (+PREUVE) / 15.16 / 15.17 (present)
>      Deligne 1989 (16.1.1)(16.1.2) (present・命名と canonicity)
>      Ihara ICM 1990 §2.3 印字 105-106 ((a)=omitted / (b)=present)
> 読み替え: RD-1 〜 RD-6 (tb_citation_bundle_v1.md §2) を条文として添付
> 工房債務: TB1-FF / TB4-INJ / TB4-GEN (同 §3.3・§4.3・紙・単系統・Sol 監査未)
> 未 pin:  [GAP-TB-EXACT] 同所性完全列 (同 §6.4) ← 【GAP-TB】の第 4 項目として新設
> 非 load-bearing: (TB3-c) z の ∞-慣性 (同 §5.3)
> ```

> #### **(N-2)** ASM §V.2.4 の **BFC 行 / B-5$_{\rm loc}$ 行**、および CLAIMS **W3-17** の状態欄
> **現行(W3-17)**: `candidate(paper-proof (framework-conditional on TB1–TB4+(Z_{2M}-link)) / two-mathematician audit PASS …)`
> **★ 案(追記のみ・既存文字列は削らない)**:
> ```text
> candidate(paper-proof (framework-conditional on TB1–TB4+(Z_{2M}-link))
>           / two-mathematician audit PASS
>           / ★ TB1・TB3・TB4^u = canonical-source-pinned v1
>               (tb_citation_bundle_v1.md・読み替え注 RD-1〜RD-6・工房債務 3 本・
>                未 pin 1 件 [GAP-TB-EXACT] つき。Sol 検収後に発効)
>           / exact TB4・Z_{2M}-link の欄は不変)
> ```

> #### **(N-3)** P97-1.1 の 4 札のうち **層 3 の札**
> **現行**: `theorem_framework-relative (BFC/TB/CAL)`
> **★ 案**: `theorem_framework-relative (BFC/TB/CAL) [TB: canonical-source-pinned v1]`
> ⟹ **札の種別は変えない**(相対 theorem 格のまま)。**角括弧で pin 状態を注記するだけ**にする — 種別を変えると P97-1.1(裁定 366)の再裁定が要るため。

### 7.3 ★ 到達した格の正名 — **「引用 pin 済」と「引用で閉じた」を区別する**

campaign v1 §0-⑥ は到達可能な終状態を `canonical-source-relative / framework-independent`(F99-3.2 Route A の語彙)とした。**本束はそこまで到達していない。** 語彙を 2 段に割ることを提案する:

| 語 | 定義 | 本束 |
|---|---|---|
| **`canonical-source-pinned`** | 条項ごとに §/式番号の pin があり、**読み替え注が条文化**され、**`proof_body_status` が全 pin で記入済** | ★ **本束が請うのはこれ** |
| **`canonical-source-relative`** | 上に加えて **全 pin が `proof_body_status = present`**、または `external_reference` の連鎖が `present` に着地している(CV-10 §1.5・v1.6 の Fresse 型着地) | ★ **未到達** |

**未到達の理由(4 点・すべて本束が自分で申告する)**:
1. **Deligne 10.16 が `external_reference`**(証明本文は SGA 側・原本表記は「SGA 3 V 7」で SGA1 か SGA3 かの判断は本束もしない)。
2. **Ihara (TB3-a)(TB3-c) が `omitted`**(証明本文なし)。
3. **工房債務 3 本(TB1-FF / TB4-INJ / TB4-GEN)が単系統・Sol 監査未。**
4. ★ **【GAP-TB-EXACT】が未 pin。**

$$\Longrightarrow\ \boxed{\ \textbf{「枠組み仮定が消えた」でも「引用で閉じた」でもない。「出所のない仮定が、§番号 pin と読み替え注と債務 3 本つきの引用へ変わった」である。}\ }$$

---

## 8. Sol 監査点(5 個・**危うい箇所の自己申告**)

> **S-1(最重要)★★ 接基点の三者同一視(RD-6)**
> Deligne 流 $\vec{01}$($T_s^0$ 経由の制限関手)・Ihara 流 $\vec{01}$(Puiseux branch + $I_{01}$ 上の正実根)・工房の $\mathrm{Fib}_{\vec{01}}$($\mathrm{Hom}_{k((\beta))}(-,\Omega)$)の同一視。**私の判定**: Ihara 流と工房のそれは**逐語同一**(補題 B-5a の分解 $\prod_P\kappa(P)((s_P))$ を経由すれば「点 $P$ + branch」という Ihara の記述そのもの)。**Deligne 流との同一性は、証明本文がどちらの文献にもない**(Ihara は帰属を宣言・Deligne は Ihara 実装を扱わない)⟹ `omitted / silent_omission`。
> **諮問**: この一段を **(i) 工房側補題として書き下す**(「Ihara の branch 関手 $\cong$ Deligne の $R\mapsto R_{(s)}$ 経由の繊維関手」— RD-4 の 3 本 + 15.17 で書けると私は見るが、$T_s^0$ の幾何点の選択と $\Omega$ の $\beta^{1/n}$ 系の対応づけが残る)か、**(ii) 規約として封じる**(「工房は Ihara 流の提示を採る」と宣言し、Deligne は (TB4ᵘ-β) の canonicity にのみ使う)か。**私は (ii) を推す**が、(ii) を採ると **Deligne §15 の pin の値打ちが (β) の 1 本に縮む**ので、司令塔の「引用化キャンペーン」の狙いと整合するか判断を仰ぎたい。

> **S-2(委嘱名指し)★★ (TB1) の閉じ方 —「構成 pin + SGA1 V」経路の可否(§3.2–§3.4)**
> 読解 D の「10.16 + 15.13/15.15/15.18 + 15.23 の 3 点 pin で閉じる」を**私は採らなかった**: §15 が構成するのは $T_s^0$ の**被覆**への制限関手であって繊維関手ではなく、**「$\mathrm{Fib}_{\vec{01}}$ が繊維関手」に番号つき pin が無い**からである。私の処方は **Deligne 10.16 末尾(任意の繊維関手 $F$ に対し $\pi_1(X,F)^\wedge=\mathrm{Aut}(F)$)+ 工房補題 TB1-FF(初等・§3.3)**。
> **諮問**: (a) **TB1-FF の 3 段証明に穴はないか**(とくに (c) の保存性 — 「連結正規底上の有限エタール被覆は生成ファイバーで決まる」の使い方)。(b) ★ **`external_reference` を二重にしない第二経路として SGA1 V へ直接 pin すべきか**。Deligne 10.16 は原本表記が「SGA 3 V 7」であり(§5.1-4 の疑義・本束も正誤判断はしない)、`proof_body_status` を `present` に着地させたいなら **SGA1 V(在庫あり・私は 1 頁も開いていない)** が要る。**司令塔の「引用化」の狙いが `pinned` 止まりでよいのか `relative` まで行くのかで答えが変わる。**(c) この経路を採ると **(TB1) の実質は「Grothendieck–Galois + 初等補題」に落ち、Deligne §15 は (TB1) には効かず (TB4ᵘ-β) と RD-4 にのみ効く** — この配分は正しいか。

> **S-3 ★★「(TB1)+(TB3) から (TB4ᵘ-γ) が従う」の導出(§4.3)+ (16.1.1) の要否(§4.2)**
> BFC §12.1 が「主張するなら一段書け」と指定した導出を書いた。核は **RD-2**(接基点のもとで「$0$ の慣性部分群」$:=\mathrm{im}(\iota)$ と定義する)+ **TB4-INJ**(初等)+ **TB4-GEN**(15.17 + (15.10.1) + 15.9 の合成)。
> **諮問**: (a) **RD-2 を「定義」と呼んでよいか**(呼べるなら (γ) は循環でなく読み替えになる。呼べないなら (γ) は独立仮定のまま)。(b) **TB4-GEN の (iii)** で位相側の **(15.10.1)/15.9** を引いているが、これは RD-3(Betti 番号を副有限条項の pin に使わない)の**唯一の例外**として明記した — この例外の張り方は安全か。(c) この縮約が正しければ **BFC §14.1-2 の現状記述が更新される**が、本束は本文を改変していない。**更新の可否。**
> **(d) ★「diverses théories du $\pi_1$」に profinie が含まれるという読み(§4.2)**: (16.1.1) の両辺は **$_{\rm mot}$ 添字つき**(私が 150 dpi 画像で確認)。「diverses théories」の内訳(§10.1 の 3 理論)は**読解 D の照合がテキストのみ**。私は motivique 依存を避けるため **制限関手そのものは副有限節(15.20/15.21/15.22/15.23)だけで閉じ、(16.1.1) は命名と canonicity に限定する二段構え**を推奨した。⟹ **(16.1.1) を pin から外しても (TB4ᵘ-β) は立つ**というのが私の判定である。穴はないか。(§16.1 の良還元前提は工房の $U$ で literally 充足されるので**外さなくてもよい**が、外せる方が依存が軽い。)

> **S-4 ★ Betti 正規化文の水準(§4.5・本束の新規発見)**
> 「En réalisation de Betti, $\mu_s$ envoie le générateur $2\pi i$ de $\mathbf Z(1)_B$ sur un petit lacet positif $\sigma_s$ autour de $s$」の $\mu_s$ は、**(16.1.2)($\pi_1$ 水準)と (16.1.3)($H_1$ 水準)の両方の名前**であり、直前の定義は (16.1.3) である(150 dpi 画像で配置を確認)。
> **(TB4ᵘ) は $\varepsilon$ を固定しないので本束は無傷**だが、**exact (TB4)/$\varepsilon$ を将来引用で閉じようとするならこの 1 行が最初の障害**になる。
> **諮問**: 指示対象を $\pi_1$ 水準に一意化する別 pin(**Compatibilités 後半 §15.44–15.49** が候補・**誰も画像で読んでいない**)に心当たりがあればご教示いただきたい。**なお現行の供給元(`Z-norm-seal/v1` + retained TB4-3/A3 framework)は本束によって一切変更されない。**

> **S-5 ★★【GAP-TB-EXACT】の格(§6.4)**
> 同所性完全列 $1\to\pi_1(U_{\bar{\mathbf Q}},\vec{01})\to\pi_1(U_K,\vec{01})\to G_K\to1$ は BFC §2 の**悉皆リストに載っていない**が §6.2 の証明第 1 行が使う。§2 は「以後これ以外は使わない(使ったら誤り)」と宣言している。
> **諮問**: **(TB2)+(TB3) に含意されているとみなす**か、**【GAP-TB】の第 4 項目として立てる**か。**私は後者を推す**(隠さない・規律 5)。**pin 候補** = Deligne 10.17–10.19(要画像確認)/ SGA1 IX(在庫あり)。**立てる場合、本束の「(TB1)(TB3)(TB4ᵘ) の 3 項目に局在」という campaign FP-1 の主張は「4 項目」へ更新される。**

---

## 9. 本束が**主張しないこと**・未閉鎖

### 9.1 主張しないこと

1. 「**枠組み層が昇格した**」— **主張しない**。本束は対応判定・引用差替版・札文言案を作っただけである。
2. 「**(TB1)/(TB3)/(TB4ᵘ) が引用で閉じた**」— **主張しない**。到達したのは `canonical-source-pinned` であって `canonical-source-relative` ではない(§7.3・未到達の理由 4 点)。
3. 「**exact (TB4) / $\varepsilon$ / $(Z_{2M}$-link$)$ について何かが変わった**」— **主張しない**。現行の供給元・欄は 1 文字も動かない。
4. `cross-checked` — **付さない**(機械計算を 1 件も走らせていない)。
5. `verified` — **付さない**(Lean 未使用)。
6. **novelty** — 主張しない。§4.2(§16.1 前提の充足)・§4.5(Betti 正規化文の水準)・§6.4(【GAP-TB-EXACT】)は **本束内の新規判定**だが、「工房初」「新規」の語は使わない(repo grep 未実施・memory `novelty-claims-need-grep`)。
7. $K^{(5)}$ の値・窓データ・$\hat c_\mu$・PSL 封印欄・$\varepsilon$ bits・$u$ 値 — **一切触れていない**。

### 9.2 二次引用のリスク申告

| # | 項目 | リスク |
|---|---|---|
| **T-1** | **Ihara ICM の全逐語** | ★ **私は原本を開いていない**。読解 I の 400 dpi 転記に全面依存(§1.3) |
| **T-2** | Deligne 印字 237–241 の逐語(15.16/15.17/15.20 完備化不変性/15.21/15.22/15.23) | **pdftotext(OCR)のみ**で私は再取得した。当該頁は読解 D が 150 dpi 画像で全読済だが、**私が新たに引いた 3 文(RD-4 の 1・2・3)は読解 D の転記に含まれていない** ⟹ **採択前に 1 回の頁画像照合を推奨**(手続き) |
| **T-3** | Deligne §10.1(3 理論の列挙)・§10.17–10.19(相対版) | 読解 D の照合が**テキストのみ**。S-3 / S-5 の pin 候補がここに掛かる |
| **T-4** | Deligne §15.44–15.49(Compatibilités 後半) | **誰も画像で読んでいない**。S-4 の候補 pin |
| **T-5** | SGA1(在庫あり) | ★ **私は 1 頁も開いていない**。§3.4・§5.2・§6.4 の「第二 pin 候補」はすべて**未確認の候補**である |

### 9.3 【文献要請】の現況(本束の消費分)

- **【文献要請 13】**: ★ **(i)(iii) は本束で消費**((i) = Deligne 10.16 + 補題 TB1-FF / (iii) = (TB4ᵘ-δ) は工房定義の tautology)。**(ii) の縮小形は (TB4ᵘ) の射程外であることが判明**(§4.4)⟹ **exact (TB4)/$\varepsilon$ 側の要請として仕切り直す**のが正しい記帳。
- **【文献要請 14】**((TB3) の正典 pin): ★ **(a)(b) は Ihara ICM で消費**。**(c)(接基点を基点とした関係式)は Ihara ICM §2.3 の 𝔹/Puiseux/positive-real-root で消費**。★ **ただし工房条文の (TB3-c)($z$ が $\infty$ の慣性生成元)は未消費**(§5.3)⟹ **要請 14 の残余として立て直す**(passport / 命題 B-9 側で要る)。
- **【文献要請 U7-3】**((GR)): **未消費のまま維持**(非標的・campaign 札 H)。
- ★ **新規の要請は起票しない** — S-1〜S-5 はいずれも**手持ちの正典と在庫(SGA1)で処理を試みるべき段階**であり、遠征を要する困難ではないと判定した。

---

## 10. 読解係ノートへの訂正・昇格・追加(**独立再判定の差分**)

| # | 種別 | 内容 |
|---|---|---|
| **R-1** | ★ **訂正**(読解 D §7-1・§3.2 末) | 「TB1 は **10.16 + 15.13/15.15/15.18 + 15.23 の 3 点 pin で閉じる**」は**一段足りない**。§15 が構成するのは $T_s^0$ の**被覆**への制限関手であって**繊維関手ではない**(15.13 の目標宣言が逐語「un revêtement fini étale $R_{(s)}$ de $T_s^0$」)。⟹ **工房補題 TB1-FF** を明示することを条件に閉じる(§3.2・§3.3) |
| **R-2** | ★ **解消**(読解 D §6-4 の「判断しない」) | (16.1.1) を「一般曲線の副有限版」として使ってよいか — **§16.1 の前提は工房の $U$ で literally 充足される**(良還元は $0,1,\infty$ が $\mathrm{Spec}\,\mathbf Z$ の全ファイバーで相異なることから自動)。かつ原文で良還元は **$\pi_1$ motivique を定義するための条件節**である(150 dpi 画像で確認)(§4.2) |
| **R-3** | ★ **昇格**(読解 D §3.2 の pin 表) | **15.20 の完備化不変性**・**15.21 の一致文**・**15.22 の $T_s\cong\bar X$ canonique** の 3 文は、**工房の完備化模型と Deligne の graded 模型の橋そのもの**(RD-4)。読解 D の表は 15.20 を「代数的記述」・15.21 を「曲線への適用」としか記載していない |
| **R-4** | ★ **昇格**(読解 D §3.2 の「C との比較」行) | **15.16 LEMME / 15.17 CONSTRUCTION** は **(TB4ᵘ-γ) の橋の一次根拠**(位相側 $x$ と副有限側 $\mathrm{im}(\iota)$ を繋ぐ唯一の compatibility)。読解 D は 1 行の副次項目として置いている(§4.3) |
| **R-5** | ★ **訂正**(読解 I §5.1「供給する 3/3」) | 読解 I の (c) は「**接基点の固定**」であって工房条文の**第 3 の慣性生成元 $z$ ではない**。**工房の (TB3-c)($z$ が $\infty$ の慣性生成元)への供給は括弧書き 1 語 "(a loop around ∞)" のみ**・明文も証明本文もなし ⟹ `omitted / silent_omission`。**ただし (5′) 鎖では非 load-bearing**(§5.3) |
| **R-6** | ★ **新規**(どちらのノートにもない) | **Betti 正規化文の水準の曖昧さ** — $\mu_s$ が (16.1.2)($\pi_1$)と (16.1.3)($H_1$)の両方の名前である(§4.5・監査点 S-4) |
| **R-7** | ★ **新規**(どちらのノートにもない) | **【GAP-TB-EXACT】** — 同所性完全列が BFC §2 の悉皆リストに無いまま §6.2 で使われている(§6.4・監査点 S-5) |
| **R-8** | **追認** | 読解 D §0-1/§0-2(副有限節に (15.10.1) の番号つき対応物は無い・(16.1.1) が正しい pin)/ §0-4($\varepsilon$ = $\mathbf Z(1)$ 自明化の自由度)/ §5.1 の原本誤植 3 件 — **いずれも私の再判定と一致**。読解 I §5.2(Ihara の Puiseux 構成と Deligne 接基点の関係)も**方向としては支持**するが、**「同一である」ことの証明本文が無い**という一点を RD-6 で明示化した |

---

## 11. 次に取りに行くもの(**提案・司令塔の裁定事項**)

| 優先 | 標的 | 費用の見積り |
|---|---|---|
| **1** | **S-5【GAP-TB-EXACT】の pin** — Deligne 10.17–10.19 の**画像照合**(読解係 1 便)か、SGA1 IX の pin | 小(在庫内) |
| **2** | **S-1 の裁定**((i) 補題化 / (ii) 規約化)— これが決まらないと RD-6 が宙に浮く | 裁定のみ |
| **2′** | ★ **S-2 の裁定**(`pinned` 止まりでよいか `relative` まで行くか)— 「行く」なら **SGA1 V の精読 1 便**(Exp. V §4–6・Galois 圏と基本関手)が要る。行かないなら Deligne 10.16 の `external_reference` のまま確定 | 裁定 + 中(SGA1 精読) |
| **3** | **工房債務 3 本(TB1-FF / TB4-INJ / TB4-GEN)の Sol 監査** | Sol 便 1 項目 |
| **4** | **T-2 の頁画像照合**(RD-4 の 3 文)— 採択前の手続き | 小 |
| **5** | (TB3-a) の第二 pin(SGA1 XIII)/(TB3-c) の pin — **passport 側で要るときに** | 中(本束の射程外) |

---

## 付録 A. 本束が導入した記号・略号

| 記号 | 意味 | 定義箇所 |
|---|---|---|
| **RD-1 〜 RD-6** | 読み替え注(工房が負う翻訳の債務) | §2 |
| **TB1-a/b/c/d** | (TB1) の条項 | §3.1 |
| **TB4ᵘ-α/β/γ/δ** | (TB4ᵘ) の条項 | §4.1 |
| **TB3-a/b/c/d** | (TB3) の条項 | §5.1 |
| **TB1-FF / TB4-INJ / TB4-GEN** | 工房側初等補題(債務 3 本) | §3.3・§4.3 |
| **[C-1] / [C-2]** | (5′) 鎖が真に外部文献を要する 2 箇所 | §6.5 |
| **【GAP-TB-EXACT】** | 本束で新規に浮上した未 pin 項目 | §6.4 |
| **`canonical-source-pinned`** | 本束が請う格(≠ `canonical-source-relative`) | §7.3 |
