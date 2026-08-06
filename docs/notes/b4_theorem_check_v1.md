# B₄ 実現可能性ノート v1 の定理検分 — 独立再導出と裁定(v1)

**状態札: `candidate(検分ノート・別人格による独立再導出 / 機械は記号語計算+整数級数+自由群への GAP スモーク 2 本のみ / 本走宇宙の候補評価ゼロ / 封印非接触 / novelty 主張なし)`**

- 検分者: 影工房 数学者(Claude / Opus 5)/ 2026-08-06 — **起草者と別人格**(研究者恒常指示「数学者に定理かどうか確かめてもらわないと」)
- 検分対象: `docs/notes/b4_direct_adjudication_feasibility_v1.md`(以下「本体」)の定理 **B4-VAC** / **B4-CANON** / 命題 **BIT-252** / **【GAP-B4-1】** の危険度
- 走行中の追加素材(司令塔・文献ゲート経由): `docs/scout/ls_pentagon_term_correspondence_v1.md`(LS1994 / LS-Ptolemy / HS2000 の pin)— 項目 4 の裁定はこれを反映済み
- 正典: `papers/txt/2008.00066-*.txt` 由来の抽出ノート `b4_original_gtshadows_extraction_v1.md`(§/式番号 pin 済)/ `docs/notes/2401.06870-抽出ノート_v1.md` / `docs/notes/hs_prop7_translation_v1.md` / `docs/notes/hsp7_hexagon_arbitration_v1.md` §0–§1 / `docs/notes/auto_settled_check_v1.md` §3.4 / `docs/week1-定義ノート.md`
- **本ノートは既在文書を 1 バイトも改変しない。**

---

## 0. 裁定(先に一枚)

| # | 対象 | 裁定 | 一行理由 |
|---|---|---|---|
| **1** | 定理 **B4-VAC** | ★ **PASS(定理として成立)** + **要修正 3 件(提示・射程・付録)** | $\tilde\psi=\psi\circ p_4$、$B_4$-核 $=\bigcap_ip_i^{-1}(N)$、20 合成の 8/12 分解、4 座標すべて恒等 — **全段を独立に再導出し一致**。ただし §0-2 の見出しは Prop 3.9 の**真の** $\tilde N$ まで射程があるかのように読める(本体 §2.6 表と矛盾) |
| **2** | 定理 **B4-CANON** | ★ **PASS(定理として成立)** + **重大な実装仕様の要修正 1 件** | (1)(2)(3)(4) すべて成立。分裂単射論法に穴なし($\varphi_{123}$ = 標準包含・$p_4\circ\varphi_{123}=\mathrm{id}$ は Fadell–Neuwirth 分裂)。**ただし §5.1/工程 P1 の「ANUPQ `Pq`(p=7, class 4)」は誤り**(`Exponent:=7` が要る)— そのままだと B4-EXQ-1 が偽 STOP する |
| **3** | 命題 **BIT-252** | ★ **PASS(4 段すべて論理的に妥当)** + **証明経路の要修正 2 件** | (i)(ii)(iii)(iv) すべて成立。ただし **(i) の閉性は「像 = 部分群」で 1 行で出る**(2401 Def 4.2)ので、$\bigcap_K\mathrm{im}$ 経由で前件「$K$ も isolated」を背負う必要がない ⟹ **【GAP-B4-5】は不要**(かつ独立に**充足も確認**した) |
| **4** | **【GAP-B4-1】** | ★★ **要修正 — 「P3 で埋まる穴」ではなく「紙で先に閉じるべき穴」。かつ文献 pin で閉じられる** | 2008 (2.20) は **LS1994 (III) と逐語同一**、LS1994 §4 が (III)⟹(III′)=$\mathrm{PENT}_W$ を明示。**変換に使う前件は (I) = 2401 (3.10)**。⟹ 同値は **hexagon 相対**であって全 $[P,P]$ では成り立たない。**現行 P3(117,649 悉皆一致)は偽アラームを出す設計**(§5.4) |

> ### ★ 一行で
> **本体の 3 定理は数学的に健全である。危険は定理側ではなく (a) 判定機の実装仕様(ANUPQ の指数律)と (b) 【GAP-B4-1】を「経験で埋める」とした設計判断の 2 点にあり、どちらも紙で先に直せる。**

**加えて、本体が見落としている★所見が 1 件ある(§7)**: 本体自身の定理 B4-VAC + 既在 HSP-SOUND は、**2008 の Question 4.6(charming ∧ fake の実例)に対する候補回答**を与える。本体 §3.5 注 2 は $\tilde{\mathbf N}^*$ について「例を与えない」と書くが、$\tilde{\mathbf N}_{\rm core}$ については**逆に例を与える**。

---

## 1. 検分の作法と申告

- **独立再導出の範囲**: 本体の主張を読んだうえで、(A.18) の余面表・(A.3)/(A.6) の共役関係・(2.4)・Prop 2.3・2401 Prop 3.4 / Def 4.2 / Cor 5.4 / Prop 3.14 / Remark 3.16 という**正典の一次データだけ**から再構成した。本体の付録 A のスクリプトは**読んでいない**(結果表とだけ突合)。
- **機械**: `scratchpad/b4check.py`(**自作・本体のスクリプトとは別実装**)— 自由群の語簡約による 20 合成の生成元像、pentagon の 4 座標評価、LCS 階数の有理数係数級数解法。群の元の列挙ゼロ。加えて GAP スモーク 2 本(**自由群 $F_2$ のみ**・本走宇宙非接触)。
- **本走宇宙(705,894 対)の候補評価はゼロ。封印 3 量非接触。**
- **読んだ範囲の申告**: 一次論文の頁画像は 1 枚も開いていない(抽出ノートと reader の scout ノートに依拠)。外部文献の自主検索はゼロ(§0 の scout ノートは司令塔が文献ゲート経由で降ろしたもの)。
- **検分対象外**: 補題 B4-KAPPA・補題 B4-MONO・定理 B4-DIR (a)(b)・系 B4-42・補題 CHARM-EQ は委嘱 4 項目に含まれないため**判定していない**(ただし B4-DIR (c) と系 B4-42 (H5) は項目 2/4 の途中で必要になったので確認した — 下記に付記)。

---

## 2. 項目 1 — 定理 **B4-VAC** の独立再導出

### 2.1 補題 B4-FORGET($\tilde\psi=\psi\circ p_4$)= **PASS**

Fadell–Neuwirth により $p_4:PB_4\twoheadrightarrow PB_3$(第 4 紐忘却)は**全射準同型**で、$\ker p_4=F_3=\langle x_{14},x_{24},x_{34}\rangle$、分裂 $PB_4\cong F_3\rtimes PB_3$。生成元上 $p_4(x_{ij})=x_{ij}\,(j\le3)$、$p_4(x_{i4})=1$。Prop 3.9 の $\tilde\psi$ は生成元上まさに $\psi\circ p_4$ と一致し、$\psi\circ p_4$ は**構成上準同型**である。

⟹ **$\tilde\psi$ の well-definedness に (A.3) の場合分けは不要**。本体の主張どおり。$\ker\tilde\psi=p_4^{-1}(N)$、$\lvert PB_4:\ker\tilde\psi\rvert=\lvert PB_3:N\rvert$ も自明。**PASS**。

### 2.2 ★ $B_4$-核 = $\bigcap_{i=1}^4p_i^{-1}(N)$ — 本体の 1 行を**明示計算で補完**

本体 §2.2 の根拠は「$B_3/PB_4=S_4$ の $S_4/S_3$ 4 剰余類・$N\trianglelefteq B_3$ ゆえ捻れは吸収される」の 1 行である。これは**剰余類内の曖昧さ**しか説明しておらず、**代表元の取り方で $p_i$ の同一視がずれない**ことを言っていない。以下で埋める。

> ### 補題 CORE-4(本稿・B4-FORGET の系の補完)
> $N\trianglelefteq B_3$、$N\le PB_3$、$[B_3:N]<\infty$ とする。$p_i:PB_4\twoheadrightarrow PB_3$ を「第 $i$ の紐を忘れる射」(残る 3 本を順序保存で $1,2,3$ に付け替える)とすると
> $$\mathrm{core}_{B_4}\bigl(p_4^{-1}(N)\bigr)=\bigcap_{i=1}^{4}p_i^{-1}(N).$$

**証明.**
**(1) 剰余類内の不変性.** $B_{3,1}:=\{b\in B_4:w_b(4)=4\}$($w_b$ = $S_4$ 像)は指数 4 の部分群で、$p_4$ は $B_{3,1}\twoheadrightarrow B_3$ に準同型として延びる。$u\in B_{3,1}$ に対し
$u\,p_4^{-1}(N)\,u^{-1}=p_4^{-1}\bigl(p_4(u)Np_4(u)^{-1}\bigr)=p_4^{-1}(N)$($N\trianglelefteq B_3$)。

**(2) 代表元.** $b_4:=1,\ b_3:=\sigma_3,\ b_2:=\sigma_2\sigma_3,\ b_1:=\sigma_1\sigma_2\sigma_3$ は $B_{3,1}$ の 4 つの左剰余類を尽くす(下記 (3) が示すとおり 4 つの異なる核を与えるので、相異なる剰余類)。

**(3) 鍵: 3 本の合成が生成元上で厳密に一致する.** $c_b(g):=b^{-1}gb$ と書く。(A.2) の定義 $x_{12}=\sigma_1^2,\ x_{23}=\sigma_2^2,\ x_{34}=\sigma_3^2,\ x_{13}=\sigma_2\sigma_1^2\sigma_2^{-1},\ x_{24}=\sigma_3\sigma_2^2\sigma_3^{-1},\ x_{14}=\sigma_3\sigma_2\sigma_1^2\sigma_2^{-1}\sigma_3^{-1}$ と (A.6) から:

| 生成元 | $\sigma_3^{-1}(\cdot)\sigma_3$ | $p_4$ の値 | $p_3$ の値 | | $\sigma_2^{-1}(\cdot)\sigma_2$ | $p_3$ の値 | $p_2$ の値 | | $\sigma_1^{-1}(\cdot)\sigma_1$ | $p_2$ の値 | $p_1$ の値 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $x_{12}$ | $x_{12}$ | $x_{12}$ | $x_{12}$ | | $\sigma_1x_{23}\sigma_1^{-1}$ | $1$ | $1$ | | $x_{12}$ | $1$ | $1$ |
| $x_{13}$ | $x_{14}$ | $1$ | $1$ | | $x_{12}$ | $x_{12}$ | $x_{12}$ | | $x_{12}^{-1}x_{23}x_{12}$ | $1$ | $1$ |
| $x_{23}$ | $x_{24}$ | $1$ | $1$ | | $x_{23}$ | $1$ | $1$ | | $x_{13}$ | $x_{12}$ | $x_{12}$ |
| $x_{14}$ | $x_{13}$ | $x_{13}$ | $x_{13}$ | | $x_{14}$ | $x_{13}$ | $x_{13}$ | | $x_{12}^{-1}x_{24}x_{12}$ | $1$ | $1$ |
| $x_{24}$ | $x_{23}$ | $x_{23}$ | $x_{23}$ | | $x_{23}^{-1}x_{34}x_{23}$ | $1$ | $1$ | | $x_{14}$ | $x_{13}$ | $x_{13}$ |
| $x_{34}$ | $x_{34}$ | $1$ | $1$ | | $x_{24}$ | $x_{23}$ | $x_{23}$ | | $x_{34}$ | $x_{23}$ | $x_{23}$ |

($\sigma_3^{-1}x_{14}\sigma_3=\sigma_2\sigma_1^2\sigma_2^{-1}=x_{13}$、$\sigma_3^{-1}x_{24}\sigma_3=\sigma_2^2=x_{23}$、$\sigma_2^{-1}x_{34}\sigma_2=(\sigma_3\sigma_2\sigma_3^{-1})^2=\sigma_3\sigma_2^2\sigma_3^{-1}=x_{24}$、$\sigma_1^{-1}x_{24}\sigma_1=\sigma_3(\sigma_1^{-1}x_{23}\sigma_1)\sigma_3^{-1}=\sigma_3x_{13}\sigma_3^{-1}=x_{14}$ はいずれも**厳密な等式**。共役形で書いた 4 箇所は $\ker p_\bullet$ が $PB_4$ で正規ゆえ値 $1$。)

⟹ **$p_4\circ c_{\sigma_3^{-1}}=p_3$、$p_3\circ c_{\sigma_2^{-1}}=p_2$、$p_2\circ c_{\sigma_1^{-1}}=p_1$(いずれも 6 生成元すべてで厳密一致)**。合成して $p_4\circ c_{b_i^{-1}}=p_i$。

**(4) 結論.** $b\,p_4^{-1}(N)\,b^{-1}=\ker(\psi\circ p_4\circ c_{b^{-1}})$。$b=b_iu$($u\in B_{3,1}$)と書けば (1)(3) より $=\ker(\psi\circ p_i)=p_i^{-1}(N)$。∎

> ★ **要修正 1**: 本体 §2.2 の「捻れは吸収される」は (1) しか含まない。**(3) を書かないと $p_i$ の同一視が定まらず、$\bigcap_ip_i^{-1}(N)$ という式自体が well-defined でない**(順序保存の付け替えを暗黙に選んでいる)。上の補題 CORE-4 で置換すること。

$\tilde{\mathbf N}_{\rm core}=\bigcap_i\ker(\psi p_i)$ ゆえ $PB_4/\tilde{\mathbf N}_{\rm core}\hookrightarrow P^4$ で、$\tilde{\mathbf N}_{\rm core}\in\mathrm{NFI}_{PB_4}(B_4)$(核なので $B_4$ 正規・有限指数・$\le PB_4$)。**本体の主張どおり。**

### 2.3 20 本の合成の勘定 — **PASS(独立実装で一致)**

$\psi:PB_3\to P$($x_{12}\mapsto x,\ x_{23}\mapsto y,\ x_{13}\mapsto x^{-1}y^{-1}$、$c=x_{12}x_{13}x_{23}\mapsto1$)、(A.18) の余面表、順序保存の $p_i$ から $\psi p_i\varphi$ を全 20 本計算した(手計算 + 独立スクリプト `scratchpad/b4check.py`)。

- **$\psi$ そのもの = 8 本**: $(i,\varphi)\in\{(4,\varphi_{123}),(4,\varphi_{1,2,34}),(3,\varphi_{1,23,4}),(3,\varphi_{1,2,34}),(2,\varphi_{12,3,4}),(2,\varphi_{1,23,4}),(1,\varphi_{234}),(1,\varphi_{12,3,4})\}$。**各 $i$ についてちょうど 2 本。**
- **退化(像が位数 7 の巡回群)= 12 本**。**各 $i$ についてちょうど 3 本。**

本体 §0-2/§2.4 の勘定と**完全一致**。

> ★ **要修正 2(付録 A.1 の表が不完全)**: 本体の表は $x_{12},x_{23}$ の像しか印字していない。そのため 12 本のうち **4 本($p_3\varphi_{234}$, $p_3\varphi_{12,3,4}$, $p_2\varphi_{123}$, $p_2\varphi_{1,2,34}$)が `x12->1 x23->1` と表示され、あたかも自明写像に見える**。実際にはこれらは $x_{13}$ と $c$ の上で非自明である:

| 合成 | $x_{12}\mapsto$ | $x_{23}\mapsto$ | $x_{13}\mapsto$ | $c\mapsto$ |
|---|---|---|---|---|
| $\psi p_3\varphi_{234}$ | $1$ | $1$ | $y$ | $y$ |
| $\psi p_3\varphi_{12,3,4}$ | $1$ | $1$ | $x^{-1}$ | $x^{-1}$ |
| $\psi p_2\varphi_{123}$ | $1$ | $1$ | $x$ | $x$ |
| $\psi p_2\varphi_{1,2,34}$ | $1$ | $1$ | $y^{-1}$ | $y^{-1}$ |

**これは瑕疵ではなく提示の欠落だが、補題 B4-IND の結論($k\equiv0\bmod7$)は $\lambda(c)\ne1$ にこそ依存している**ので、表に $x_{13}$ 列(または $c$ 列)を足すこと。なお全 12 本で $\lambda(c)\in\{x^{\pm1},y^{\pm1}\}$(= 巡回像の生成元)であり、**12 本のどれか 1 本だけで $k\equiv0\ (7)$ が出る**(本体は「総合して」と書くが、実は各本が単独で十分)。

### 2.4 pentagon の 4 座標 — **PASS**

退化写像は像が巡回(可換)ゆえ $[F_2,F_2]$ を $1$ に潰す。さらに像は指数 7 ゆえ $\mathcal V(F_2)=\gamma_5F_2^{\,7}$ も潰す。よって charming $f$($[F_2,F_2]$ の代表)に対し (2.20) の各座標は:

| 座標 | LHS $=\varphi_{234}\!\cdot\!\varphi_{1,23,4}\!\cdot\!\varphi_{123}$ | RHS $=\varphi_{1,2,34}\!\cdot\!\varphi_{12,3,4}$ | 判定 |
|---|---|---|---|
| $i=4$ | $1\cdot1\cdot f$ | $f\cdot1$ | 恒等 |
| $i=3$ | $1\cdot f\cdot1$ | $f\cdot1$ | 恒等 |
| $i=2$ | $1\cdot f\cdot1$ | $1\cdot f$ | 恒等 |
| $i=1$ | $f\cdot1\cdot1$ | $1\cdot f$ | 恒等 |

$PB_4/\tilde{\mathbf N}_{\rm core}\hookrightarrow P^4$ ゆえ 4 座標の連立 $\iff$ (2.20) mod $\tilde{\mathbf N}_{\rm core}$。$\ker\tilde\psi$ は $i=4$ 座標のみ。**定理 B4-VAC は成立**。独立スクリプトも同一出力。

### 2.5 ★ 要修正 3 — 射程の過大表示

本体 §0-2 の見出しは「**Prop 3.9 の持ち上げ窓は使えない**」であるが、定理 B4-VAC が扱うのは $\ker\tilde\psi$ と $\tilde{\mathbf N}_{\rm core}$ の 2 つだけで、**Prop 3.9 が実際に取る窓($\lvert PB_4:\ker\tilde\psi\rvert$ 指数の正規部分群 全交わり、さらに Cor 3.5 で isolated 化したもの)には及ばない**。本体 §2.6 の表自身が「Prop 3.9 の $\tilde N$ … pentagon 検出力: **未知(構成不能)**」と正しく書いており、**§0-2 と §2.6 が矛盾している**。

修文案: 「Prop 3.9 の**構成の途中に現れる 2 つの自然な窓**($\ker\tilde\psi$ とその $B_4$-核)は pentagon の検出力がゼロである。Prop 3.9 が最終的に取る特性部分群 $\tilde N$ の検出力は**未知**であり、構成不能ゆえ実用にならない。」

同様に §0-2 の「252 の**全件**が反例になる」は、**$\tilde{\mathbf N}_{\rm core}$ に限れば正当**である($\ker\tilde\psi$ は $B_4$-正規でないので 2008 の窓ではなく、反例の舞台に使えない)。$\tilde{\mathbf N}_{\rm core}$ は正当な窓なので**反例の主張自体は生き残る** — ただし窓を明記すること。

**⟹ 項目 1 の裁定: PASS(定理として成立)。要修正 3 件(いずれも提示・射程の問題で、数学的瑕疵ではない)。**

---

## 3. 項目 2 — 定理 **B4-CANON** の独立再導出

### 3.1 (1) $\tilde{\mathbf N}^*=\mathcal V(PB_4)\in\mathrm{NFI}_{PB_4}(B_4)$ — **PASS**

verbal $\Rightarrow$ 完全不変 $\Rightarrow$ 特性。$PB_4\trianglelefteq B_4$ ゆえ $\tilde{\mathbf N}^*\trianglelefteq B_4$。$PB_4/\gamma_5PB_4^{\,7}$ は有限生成・冪零類 $\le4$・指数 7 ゆえ有限。∎

### 3.2 (2) $\tilde{\mathbf N}^*_{PB_3}=\mathcal V(PB_3)=\mathbf N_0$(**厳密等号**)— **PASS・穴なし**

委嘱の「分裂論法の下部群像の取り方に穴がないか」への回答:

- $\varphi_{123}$ は (A.18) より $x_{12}\mapsto x_{12},x_{23}\mapsto x_{23},x_{13}\mapsto x_{13}$、すなわち**紐 $\{1,2,3\}$ 上の標準包含 $PB_3\subset PB_4$**。曖昧さゼロ。
- $p_4\circ\varphi_{123}=\mathrm{id}_{PB_3}$ は生成元上で即座(Fadell–Neuwirth 分裂の切断そのもの)。私の 20 合成表の 1 行目 $\psi p_4\varphi_{123}=\psi$ とも独立に整合。
- **($\subseteq$)**: $w\in\varphi_{123}^{-1}(\mathcal V(PB_4))$ なら $w=p_4\varphi_{123}(w)\in p_4(\mathcal V(PB_4))$。$p_4$ が**全射**ゆえ verbal 部分群は $p_4(\mathcal V(PB_4))=\mathcal V(PB_3)$(語の値が値に全射で写る)。⟹ $w\in\mathcal V(PB_3)$。
- **($\supseteq$)**: 各余面 $\varphi$ は準同型ゆえ $\varphi(\gamma_5PB_3)\subseteq\gamma_5PB_4$、$\varphi(PB_3^{\,7})\subseteq PB_4^{\,7}$。⟹ $\mathcal V(PB_3)\subseteq\bigcap_\varphi\varphi^{-1}(\mathcal V(PB_4))$。

⟹ **5 本の余面のうち $\varphi_{123}$ 1 本だけで ($\subseteq$) が出る。残り 4 本は ($\supseteq$) 側でしか使われず、そこでは「準同型は verbal を verbal に送る」という自明な事実しか要らない。論法は健全。** (2.4) を「$N\cap PB_3$」と読み違えていないことも確認済(抽出ノート §1.2 の警告どおり (2.4) を使用)。

$\mathcal V(PB_3)=\mathcal V(F_2\times\mathbb Z)=\mathcal V(F_2)\times7\mathbb Z=\mathcal V(F_2)\times\langle c^7\rangle=\mathbf N_0$(直積上の verbal は成分ごと: $(a,b)^7=(a^7,b^7)$ から $A^7\times B^7$ が生成される)。$\tilde{\mathbf N}^*_{F_2}=\mathbf N_0\cap F_2=\mathcal V(F_2)=N_{F_2}$。

$\tilde N^*_{\rm ord}$: Prop 2.3 の lcm を $PB_3/\mathbf N_0\cong P\times C_7$ で評価 — $\mathrm{ord}(x_{12})=\mathrm{ord}(x_{23})=7$、$\mathrm{ord}(c)=7$ ⟹ **7**。$\mathcal X_{\tilde{\mathbf N}^*}=\mathcal X_{\mathbf N}$(6 層)。**PASS**。

### 3.3 (3) $PB_4/\tilde{\mathbf N}^*\cong C_7\times Q$ — **PASS**

$PB_4^{\rm ab}=\mathbb Z^6$(基底 $x_{ij}$)で $\Delta^2=\prod_{i<j}x_{ij}\mapsto(1,\dots,1)$。座標射影 $\pi:PB_4\to\mathbb Z$($x_{12}$ 成分)は $\Delta^2\mapsto1$ ゆえ $\langle\Delta^2\rangle=Z(PB_4)$ 上で同型 ⟹ **中心が直因子**: $PB_4=\langle\Delta^2\rangle\times\ker\pi$、$\ker\pi\cong PB_4/Z(PB_4)=K(0,5)$。verbal は直積を尊重するので $\mathcal V(PB_4)=7\mathbb Z\times W$、$PB_4/\tilde{\mathbf N}^*\cong C_7\times Q$。**PASS**。

なお $K(0,5)\cong PB_4/Z(PB_4)$ は、司令塔が降ろした scout ノート(LS1994 p.16, p.6 命題 2(vi): $K(0,n+1)\simeq K_n/Z\subset B_n/Z\subset M(0,n+1)$)で**一次文献からも裏づけられた**。既在の補題 CENT-FREE の前提はこの点で強化された。

**付随して確認**(項目 4 のために必要だった): 定理 B4-DIR (c) 後半は正しい。$D:=$ pentagon defect は 5 本の準同型像の積で $f\in[F_2,F_2]$ ゆえ $D\in[PB_4,PB_4]=[K,K]\subseteq K$。よって $D\in L=\mathbb Z\times W\iff D\in W\iff D\in7\mathbb Z\times W=\tilde{\mathbf N}^*$。∎

### 3.4 (4) $\lvert PB_4:\tilde{\mathbf N}^*\rvert=7^{41}$ — **PASS(ただし導出経路を 1 段短縮できる)**

$\prod_k(1-t^k)^{\phi_k}=\prod_{i=1}^{n-1}(1-it)$ を独立実装で解いた(有理数係数の形式級数):

| 群 | LCS 階数 (deg 1..6) | $\sum_{k\le4}$ |
|---|---|---|
| $PB_4$ | $6,4,10,21,54,125$ | **41** |
| $PB_3$ | $3,1,2,3,6,9$ | 9 |
| $F_2$ | $2,1,2,3,6,9$(Witt) | 8 |
| $K(0,5)=PB_4/Z$ | $5,4,10,21$ | **40** |

本体 §A.3 と完全一致。$\lvert P\rvert=7^8$・$\lvert Q\rvert=7^{40}$ という**工房の実測値を再現**しており、Lazard 段(類 $4<p=7$ ⟹ $\lvert G/\gamma_5GG^7\rvert=7^{\text{Hirsch}}$)は実測に支持されている。

> ★ **経路の短縮(要修正ではないが記すべき)**: (4) は **(3) から直接出る** — $PB_4/\tilde{\mathbf N}^*\cong C_7\times Q$ かつ $\lvert Q\rvert=7^{40}$ は**既在の実測値**なので、$\lvert PB_4:\tilde{\mathbf N}^*\rvert=7\cdot7^{40}=7^{41}$。⟹ **$PB_4$ への Lazard 適用を独立仮定にしなくてよい**。本体の格付け「paper-proof candidate((4) の位数は機械)」は、この経路を採れば **paper-proof** に上げられる。

### 3.5 ★★ 重大な要修正 — 工程 P1 の **ANUPQ 仕様が誤り**

本体 §5.1 表と §8 工程 P1 は $R=PB_4/\mathcal V(PB_4)$ の構築を「**ANUPQ `Pq`(p=7, class 4)**」と指定している。**これは違う群を作る。**

- `Pq` / `PQuotient` の `ClassBound` は**下方指数-$p$ 中心列** $P_1=G,\ P_{i+1}=[P_i,G]P_i^{\,p}$ に沿う切り詰めであり、$G/P_{c+1}$ は $G/\gamma_{c+1}(G)G^{p}$ **ではない**。
- 決定的反例(整数論的にも自明): $G=\mathbb Z$、$p=7$ で $P_3=49\mathbb Z$ に対し $\gamma_3(\mathbb Z)\mathbb Z^7=7\mathbb Z$。
- **機械確認**(GAP 4.16.0 ライブラリの `PQuotient`、自由群 $F_2$ のみ・本走非接触): `PQuotient(F2, 7, 2)` の位数 = **16807 $=7^5$**。一方 $\lvert F_2:\gamma_3F_2^{\,7}\rvert=7^{2+1}=7^3$。⟹ **$7^5\ne7^3$、仕様の誤りは実測で確定**。

**正しい仕様**: `Pq(F : Prime:=7, ClassBound:=4, Exponent:=7)`(指数律を課す)。そのままだと **B4-EXQ-1(予言 $\lvert R\rvert=7^{41}$)が的中せず「LCS 公式の適用ミス ⟹ STOP」という誤った分岐に落ちる** — 予言体系が**バグ検出器として逆に働く**(実装の誤りを理論の誤りと読む)。

> ### ★ 追加の運用所見(工房環境)
> **本機の ANUPQ は外部バイナリ `pq` が動作しない**。`LoadPackage("anupq")` は `true` を返すが、`Pq(...)` は即座に `Error, failed to find any more of line (iostream dead?)` で落ちる(自由群 $F_2$・$p=2$・class 2 の最小スモークでも同じ)。⟹ **工程 P1 は現状の環境では実行不能**。
> 代替の**数学的に正しい**回避路(実装は ep-keeper / implementer の判断):指数 7・類 4 の群では $P_i=\gamma_i$ なので $P_5(G)\subseteq\gamma_5(G)G^7$。よって GAP ライブラリの `PQuotient(PB_4,7,4)` で $\bar G:=PB_4/P_5$ を作り、$R=\bar G/\bigl(\gamma_5(\bar G)\cdot\mathrm{Agemo}_1(\bar G)\bigr)$ を取れば $R\cong PB_4/\mathcal V(PB_4)$ が得られる(中間商 $\bar G$ の大きさは未見積り)。**この見積りは本ノートの射程外** ⟹ 【工程要請】として司令塔へ。

**⟹ 項目 2 の裁定: 定理 B4-CANON は (1)(2)(3)(4) すべて PASS・分裂論法に穴なし。ただし §5.1/工程 P1 の実装仕様は要修正(誤り)+ 環境上の実行不能が判明。**

---

## 4. 項目 3 — 命題 **BIT-252** の精査

### 4.1 前件の実在確認(正典と突合)

| 前件 | 正典の根拠 | 判定 |
|---|---|---|
| genuine の定義 = $\widehat{GT}_{gen}$ 由来 | **2401 Def 4.2**(逐語: 「genuine ⟺ ∃$(\hat m,\hat f)\in\widehat{GT}_{gen}$ が $[m,f]$ に射影」) | ✓ |
| survival 特徴づけ | **2401 Cor 5.4**(genuine ⟺ 全細分 $K$ で $\mathrm{Im}(R_{K,N})$ に入る) | ✓ **gentle 系にも存在する**(本体は 2008 Cor 3.13 型を仮定して使っているが、gentle 版が独立に在る) |
| isolated の cofinality | **2401 Prop 3.14** | ✓ |
| $R_{N,H}$ が群準同型 | **2401 Remark 3.16**(isolated $N\le H$) | ✓ |
| $N$ が isolated | **VERBAL-ISO**(前件 $c\in\mathbf N$ ✓・$N_{F_2}=\mathcal V(F_2)$ verbal ✓) | ✓ |

### 4.2 (i) 閉性 — **PASS。ただし証明経路を要修正(2 箇所)**

委嘱の問い「genuine 集合の合成閉性は何から出るか」への回答:

> ### ★ 最短経路(本体より 1 段短い)
> $N$ が isolated なら $\mathrm{GT}(\mathbf N)=\mathrm{Aut}_{\mathrm{GTSh}}(\mathbf N)$ は**群**で、射影 $\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N)$ は**関手性から群準同型**である。2401 Def 4.2 により
> $$\mathfrak G^{\rm gentle}_{\rm genuine}(\mathbf N)=\mathrm{im}\bigl(\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N)\bigr)$$
> であるから、**閉性は「群準同型の像は部分群」の 1 行**で出る。

本体は代わりに $\bigcap_K\mathrm{im}(\mathrm{GT}(K)\to\mathrm{GT}(\mathbf N))$ を経由し、その各項が部分群であることを言うために **「$K$ も isolated」という前件 (i)** を背負っている(⟹【GAP-B4-5】)。これは**不要な負債**である。

> ★ **要修正 4**: 命題 BIT-252 の証明を「像 = 部分群」経路に置き換え、前件 (i) を落とすこと。あわせて **【GAP-B4-5】を閉じる**。
>
> ★ なお **【GAP-B4-5】は独立に充足も確認した**(落とさない場合の保険): $K=\mathcal V_5(F_2)\times\langle c\rangle$ について — $\mathcal V_5(PB_3)\langle c\rangle=\mathcal V_5(F_2)\times\langle c\rangle=K$ なので $K$ は $PB_3$ の 2 つの特性部分群の積 ⟹ $PB_3$ 特性 ⟹ $K\trianglelefteq B_3$。有限指数 ✓。$K\le\mathbf N$ ✓($\gamma_6F_2^{\,7}\le\gamma_5F_2^{\,7}$)。VERBAL-ISO の前件 $c\in K$ ✓、$K_{F_2}=\mathcal V_5(F_2)$ verbal ✓。⟹ **$K$ は isolated**。
>
> ★ **要修正 5(小)**: 本体は $\bigcap$ を「全 $K\le\mathbf N$」で取るが、部分群性を isolated 経由で言うなら**「isolated $K$ に限った交わり」で取る**必要がある。両者が一致することは Prop 3.14(cofinality)+ 減少性から出るので**書けば埋まる**が、現状は書かれていない。

### 4.3 (ii) 中間なし — **PASS**

$\mathfrak G_{\rm ar}\le H\le\mathrm{GT}(\mathbf N)$ なら Lagrange で $[\mathrm{GT}(\mathbf N):H]\cdot[H:\mathfrak G_{\rm ar}]=7$。7 が素数ゆえ一方が 1。**正規性は不要**。∎ 本体どおり。

前件の格は**測定相対**: $\lvert\mathrm{GT}(\mathbf N)\rvert=294$(本走)・$\lvert\mathfrak G_{\rm ar}\rvert=42$(BH-α-pent v1.1 = framework/measurement-relative)。命題はこの格を継承する — 本体の表記はこれを正しく明示している ✓。

### 4.4 (iii)「1 元で足りる」— **PASS(含意の向きも正しい)**

委嘱の問い「全滅 ⟹ 全 252 が fake の含意方向」への精査:

1. $g\in252$ を任意に 1 つ取る。$g$ が $K$ に survive しなければ、**Cor 5.4 の易しい向き**(genuine $\Rightarrow$ 全 $K$ に survive — $\widehat{GT}_{gen}$ 由来なら関手性で全 $K$ の像に入る)の対偶で $g$ は fake。
2. ⟹ $\mathfrak G^{\rm gentle}_{\rm genuine}\ne\mathrm{GT}(\mathbf N)$。
3. ⟹ BIT-252 (ii) より $\mathfrak G^{\rm gentle}_{\rm genuine}=\mathfrak G_{\rm ar}$(42 元)。
4. ⟹ $252=\mathrm{GT}(\mathbf N)\setminus\mathfrak G_{\rm ar}$ の**全件**が fake。∎

**含意方向は正しい。** さらに **(iii) は Cor 5.4 の易しい向きしか使わない**ので、§4.2 で述べた「像 = 部分群」経路と合わせれば **決定実験に必要な前件は「$N$ が isolated」だけ**になる($K$ の isolated 性も survival 特徴づけの難しい向きも不要)。

**「$K$ に survive しない」= 「117,649 個の持ち上げが全滅」の同値性**も確認した:
- $K_{\rm ord}$: $PB_3/K$ で $\mathrm{ord}(c)=1$、$\mathrm{ord}(x_{12})=\mathrm{ord}(x_{23})=7$ ⟹ $K_{\rm ord}=7=\mathbf N_{\rm ord}$ ⟹ **$m$ は一意に決まる**(本体「$m$ は固定・1 層のみ」✓)。
- $f'$ の動く範囲 $=\mathbf N/K$ の $f$-ファイバー $=\lvert\mathcal V(F_2):\mathcal V_5(F_2)\rvert=7^{\phi_5(F_2)}=7^6=117{,}649$ ✓(独立計算で $\phi_5(F_2)=6$ を確認)。
- $\lvert P'\rvert=7^{2+1+2+3+6}=7^{14}$ ✓、$\lvert[P',P']\rvert=7^{12}$ ✓、$[P',P']\to[P,P]$ のファイバー $=7^{6}$ ✓ で $P'\to P$ の全ファイバーと一致 ⟹ **charming 性は自動**(持ち上げは必ず $[P',P']$ に入る)。
- SURJ は H8′(7 群・$\bar f'\in[P',P']$・$\gcd(2m+1,7)=1$)で自動 ✓。

### 4.5 (iv) 294 側の帰結 — **PASS(ただし言明の精密化を推奨)**

$\mathfrak G_{\rm ar}\subseteq\mathrm{im}(\widehat{GT}\to\mathrm{GT}(\mathbf N))\subseteq\mathfrak G_{\rm pent}$(HSP-SOUND)で両端 42 ⟹ $\mathrm{im}(\widehat{GT})=42$。ビットが 294 なら $\mathrm{im}(\widehat{GT}_{gen})=294\supsetneq42=\mathrm{im}(\widehat{GT})$。

> ★ **要修正 6(言明)**: この結論の**正確な形**は「**自然な射 $\widehat{GT}\to\widehat{GT}_{gen}$ は全射でない**(1 つの有限窓での像の真の包含がその証人)」である。本体の「$\widehat{GT}_{gen}\supsetneq\widehat{GT}$」は $\widehat{GT}\hookrightarrow\widehat{GT}_{gen}$ の単射性を暗黙に使っている。単射性は本ノートでは**確認していない**(UNKNOWN)ので、非全射形で書くのが安全。

**⟹ 項目 3 の裁定: BIT-252 の 4 段すべて PASS。要修正 3 件(証明経路 2・言明 1)。【GAP-B4-5】は「不要」かつ「充足」の二重で閉じる。**

---

## 5. 項目 4 — 【GAP-B4-1】の危険度(**文献 pin 反映後の裁定**)

### 5.1 走行中に判明した決定的事実 — 2008 (2.20) は LS1994 (III) と**逐語同一**

scout ノート A-1 の LS1994 (III):
$$f(x_{12},x_{23}x_{24})\cdot f(x_{13}x_{23},x_{34})=f(x_{23},x_{34})\cdot f(x_{12}x_{13},x_{24}x_{34})\cdot f(x_{12},x_{23})$$
2008 (2.20)(= (A.18) で展開したもの):
$$f(x_{23},x_{34})\cdot f(x_{12}x_{13},x_{24}x_{34})\cdot f(x_{12},x_{23})=f(x_{12},x_{23}x_{24})\cdot f(x_{13}x_{23},x_{34})$$
**左右を入れ替えただけの同一式**(舞台も同じ: LS1994 は $\hat K_4=\widehat{PB_4}$ = 中心を殺していない世界、2008 は $PB_4/N$)。⟹ **2008 系と LS 系の pentagon の同定に版差はない。**

また scout A-2 の (III′)
$$f(x_{34},x_{45})f(x_{51},x_{12})f(x_{23},x_{34})f(x_{45},x_{51})f(x_{12},x_{23})=1$$
は $\rho(x_{ij})=x_{i+3,j+3}$ の下で $\rho^4(f)\rho^3(f)\rho^2(f)\rho(f)f=1$ に**逐語一致** = 工房の $N_\rho(f)$ = $\mathrm{PENT}_W$ の定義式そのもの。**項の順序まで一致**。

### 5.2 変換に使われる前件 = **(I)**、すなわち 2401 の **(3.10)**

scout A-2 が明記する (III)→(III′) の材料は 3 つ:
1. **関係 (I)**: $f(x,y)f(y,x)=1$ ← **これは 2401 Prop 3.4 の (3.10) $f\,\theta(f)\in\mathsf N_{F_2}$ そのもの**($\theta:x\leftrightarrow y$)。
2. **関係 (4)**(球面/Hurwitz): $\bar x_{45}=\bar x_{12}\bar x_{13}\bar x_{23}$ 等 — $K(0,5)$ の**群の関係式**。
3. **中心元の吸収**: $\gamma$ が $\alpha,\beta$ と可換で $f\in[F_2,F_2]$ なら $f(\gamma\alpha,\beta)=f(\alpha,\gamma\beta)=f(\alpha,\beta)$ — **任意の群で成立する語の恒等式**。

⟹ **2 と 3 は群の恒等式なので任意の商に降りる。1 だけが $f$ に対する条件である。**

構造的な理由も見えた: 5 本の余面は「5 点球面の巡回隣接対 $\{i,i+1\}$ を潰す」操作と 1:1 だが、**2008 の $\varphi_\bullet$ は残る 4 点のうちどれを $\infty$ に取るかを ρ-非同変に選んでいる**(5 が潰れないときは 5 を、5 が潰れるときは潰した点を $\infty$ にする)。$\infty$ の取り替えは $K(0,4)=F_2$ の $\theta$(位数 2)・$\tau$(位数 3)対称そのもの。**だから (I)/(3.10) が要る。** 事実、$\varphi_{123}(f)=\rho^0(f)$ と $\varphi_{234}(f)=\rho^2(f)$ は**素で一致**し、ずれは残り 3 項に集中する。

HS2000 Prop 7 の Remark(scout C-2)が「この (I)(II) 前提は実際に必要である」と明記していることも、この読みと整合する。

### 5.3 ★ 有限窓への降下 — **verbal 窓ゆえ自動**(本稿の鍵補題)

> ### 補題 VERBAL-DESCENT(本稿)
> $Q=K(0,5)/\mathcal V(K(0,5))$、$R=PB_4/\mathcal V(PB_4)$ とおく。$Q,R$ は変種「類 $\le4$ かつ指数 7」に属するので $\mathcal V(Q)=\mathcal V(R)=1$。ゆえに **任意の**準同型 $h:F_2\to Q$(または $R$)に対し $h(\mathcal V(F_2))=\mathcal V(h(F_2))\subseteq\mathcal V(Q)=1$、すなわち $h(N_{F_2})=1$。
> ⟹ (3.10)($f\,\theta(f)\in N_{F_2}$)は、$h(x)=u,h(y)=v$ なる**任意の代入対** $(u,v)$ に対して $f(u,v)f(v,u)=1$ を $Q$(resp. $R$)の中で与える。∎

これが効く理由: LS1994 の書換えは中間段でも (I) を色々な代入対で使う。marking を持つ窓なら「どの代入で降りるか」を逐一検査する必要があるが、**verbal 窓では検査が不要**になる。翻訳ノート §5 の「設計利点 (iii)(marking の自由度ゼロ)」がここで払い戻される。

### 5.4 ★★ 裁定 — 「先に紙で閉じるべき穴」であり、pin で閉じられる

司令塔の 3 つの下問に個別に答える。

> **(a) HS2000 Prop 7 は有限窓 $\mathcal V(PB_4)$ 商へ降りるか。**

**降りない。かつ使うべきでない。** Prop 7 の右辺は「$\tilde F\in\mathcal A^\sharp_5$ への**延長が存在して** $[\rho,\tilde F]=\mathrm{inn}\,f$」という**存在命題**であり、その延長の存在自体が LS lemma 7 / lemma 9 のタワー(副有限)論法に依存する。有限商 $Q$ には対応する自己同型が存在する保証も一意性もない。これは工房が定理 PENT-NORM で**意図的に捨てた**量化子(翻訳ノート §1.2 注 1・罠 D-5)であり、Prop 7 を引くとその危険を再輸入する。

**しかし Prop 7 は不要である。** 必要なのは項レベルの等式変形 (III)⟺(III′) であり、それは **Pin A(LS1994 §4 p.17)** が供給する。Prop 7 の価値は (α) 独立な裏づけ、(β) **「(I)(II) 前提が必要」という明示**(= 層別の根拠)の 2 点に限る。

> **(b) 前件 (I)(II) は pentagon 単独判定の計画と整合するか — 順序制約が生じないか。**

**★ 生じる。これが本項目の最大の指摘である。**

- LS1994 が (III)→(III′) に使うのは **(I) のみ**((II) は列挙されていない)。⟹ 必要な順序制約は「**(3.10) を先に検査せよ**」。
- 一方 **本体 §3.3/工程 P2 は $D_{B_4}$ を $[P,P]$ 全 117,649 件で評価**し、**工程 P3 はその通過集合と $\mathrm{PENT}_W$ 通過集合を悉皆突合**する設計である。**(3.10) を満たさない $f$ の上では両者が一致する理由がない。**
- ⟹ **現行 P3 は不一致を出すのが自然**であり、そのとき **B4-EXQ-4 の分岐 (c)「B₄ が真に弱い ⟹ (2.20)-PASS かつ $\mathrm{PENT}_W$-FAIL の新類」が偽アラームとして発火する。**

> ★ **要修正 7(P3 の層別化・必須)**: 突合は**必ず層別**で行う。
> | 層 | 定義 | 事前予言 |
> |---|---|---|
> | **S0** | $[P,P]$ 全件(117,649) | **UNKNOWN(不一致を許容)** — 情報としては探索的 |
> | **S1** | (3.10) $f\theta(f)\in N_{F_2}$ を満たす $f$ | ★ **一致すべき**(LS1994 の変換が適用可能な層) |
> | **S2** | full hexagon 通過(本走の 294 の $f$ 成分) | ★ **一致すべき**(S1 の部分集合) |
> **一致/不一致の判定は S1・S2 でのみ行い、S0 の不一致は STOP 条件にしない。**

> ★ **要修正 8(B4-EXQ-4 の単位の混同)**: 現行の予言は「(2.20) mod $\mathcal V(PB_4)$ の通過集合 $=$ $\mathrm{PENT}_W$ の通過集合(**42 件**)」だが、左辺は **$f$ の集合**(宇宙 117,649)、右辺の 42 は **shadow $(m,f)$ の個数**(宇宙 705,894・hexagon 通過の 294 の内数)である。**単位が違うので、literal には偽の予言**。「S2 上で $(m,f)$ として 42 件」と書き直すこと。CV-9 判読(【GAP-B4-4】)の対象に単位欄を追加すべき。

> **(c) 中心商の扱いは B4-CANON の窓と噛み合うか。**

**噛み合う。** LS1994 の (III) は $\hat K_4$(中心あり)、(III′) は $\hat M(0,5)$(中心自明)で、その橋は $\hat B_4/Z\subset\hat M(0,5)$(scout A-5・LS1994 p.16)。工房側の対応物は本体 定理 B4-DIR (c) で、私も §3.3 で独立に検証した:
$$D\in[PB_4,PB_4]=[K,K]\ \Longrightarrow\ \bigl(D\in\tilde{\mathbf N}^*=7\mathbb Z\times W\iff D\in L=\mathbb Z\times W\iff \bar D\in W\bigr).$$
すなわち **$\tilde{\mathbf N}^*$ が中心を丸ごとは含まない($7\mathbb Z$ しか含まない)ことは、charming $f$ の pentagon 判定には一切影響しない**。$Q=K(0,5)/W$ への通過は無損失。**中心の扱いに穴はない。**

### 5.5 残る穴(pin 後)

| 札 | 内容 | 状態 |
|---|---|---|
| **【GAP-B4-1a】** | LS1994 §4 p.17 の (III)→(III′) 書換えの**各段**は scout ノートに材料が列挙されているだけで、**式変形自体は原文にも本工房にも書き下されていない**。工房記法での再現が要る | **有界の作業**。reader に p.17・p.13 の逐語追加抽出を依頼するか、(4)+中心吸収+(I) から自前導出(見積り: 紙 1〜2 頁) |
| **【GAP-B4-1b】** | **逆向き (III′)⟹(III)**。各段が等式代入なので可逆と見込まれるが、**scout が記録しているのは順方向のみ** | **要明記**。等式代入であることを確認して書けば閉じる見込み |
| **【GAP-B4-1c】** | (II) が変換のどこかで暗黙に使われていないか(LS1994 の材料列挙は要約であり、原文の全段は未確認) | **保守的運用で回避可**: 層別を S2(full hexagon)で行えば (I)(II) 両方が成立している |

⟹ **【GAP-B4-1】は「経験決定計画 P3 で埋まる穴」ではなく「文献 pin により紙で閉じられる穴」である。P3 は独立の確認役(2 実装の突合)へ降格すべきで、同値の**根拠**にしてはならない。**

理由をもう一段: P3 は「1 つの窓の上で 2 つの述語の外延が一致する」ことしか示さない。**述語の同一性(内包)は示さない** — これはまさに規約台帳 CV-9 が分離せよと定めている区別である。文献 pin は内包側を与える。両方あって初めて `cross-checked` の格付けが正当になる。

**⟹ 項目 4 の裁定: 危険度は「経験で埋めてよい穴」から「先に紙で閉じるべき穴 + 現行 P3 は偽アラーム設計」へ引き上げ。ただし pin により閉鎖は有界の作業。**

---

## 6. 要修正一覧(本体へのフィードバック)

| # | 箇所 | 種別 | 内容 |
|---|---|---|---|
| **1** | §2.2 | 証明の欠落 | $B_4$-核の一段に補題 CORE-4(代表元 $1,\sigma_3,\sigma_2\sigma_3,\sigma_1\sigma_2\sigma_3$ と $p_4c_{\sigma_3^{-1}}=p_3$ 等の厳密一致)を挿入 |
| **2** | 付録 A.1 | 提示 | 表に $x_{13}$(または $c$)列を追加。4 本が「$1,1$」に見えるが非自明 |
| **3** | §0-2 | 射程の過大 | 「Prop 3.9 の持ち上げ窓」→「Prop 3.9 の構成に現れる 2 窓」。§2.6 表との矛盾解消。反例の舞台は $\tilde{\mathbf N}_{\rm core}$ と明記($\ker\tilde\psi$ は $B_4$-正規でなく 2008 の窓ではない) |
| **4** ★★ | §5.1 表 / §8 P1 | **仕様の誤り** | `Pq(p=7, class 4)` → `Pq(F : Prime:=7, ClassBound:=4, Exponent:=7)`。機械確認済($F_2$ で $7^5$ vs $7^3$) |
| **5** | §4.4 証明 | 経路 | $\mathfrak G_{\rm genuine}=\mathrm{im}(\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N))$(2401 Def 4.2)で閉性を 1 行に。前件 (i) と【GAP-B4-5】を落とす |
| **6** | §4.4 証明 | 抜け | $\bigcap$ を isolated $K$ に限る場合、cofinality(2401 Prop 3.14)で全 $K$ と一致することを明記 |
| **7** | §4.4 系 | 言明 | 「$\widehat{GT}_{gen}\supsetneq\widehat{GT}$」→「$\widehat{GT}\to\widehat{GT}_{gen}$ は全射でない」($\widehat{GT}$ の単射性は UNKNOWN) |
| **8** ★★ | §8 P3 / §8.1 B4-EXQ-4 | **設計の誤り** | 突合を S0/S1/S2 に層別。S0 の不一致は STOP にしない。予言の**単位**($f$ 集合 vs shadow 集合)を明記 |
| **9** | §9.2【GAP-B4-1】 | 格上げ | 「P3 で決める」→「文献 pin で紙で閉じる(残る有界作業 = GAP-B4-1a/1b/1c)。P3 は確認役」 |
| **10** | §9.2【GAP-B4-5】 | 閉鎖 | 不要(修正 5)かつ充足(§4.2 の確認)の二重で閉じる |
| **11** | §9.4 格付け | 上げ | B4-CANON (4) は既在実測 $\lvert Q\rvert=7^{40}$ + (3) から出るので **paper-proof** に上げられる |

---

## 7. ★★ 本体が見落としている所見 — $\tilde{\mathbf N}_{\rm core}$ と 2008 **Question 4.6**

本体 §3.5 注 2 は「$\mathrm{GT}^\heartsuit(\tilde{\mathbf N}^*)$ が全 genuine ⟹ **この窓は charming∧fake の例を与えない**」と書く(正しい)。しかし **同じノートの定理 B4-VAC は、別の窓では逆のことを言っている。**

> ### 観察 **Q46-CAND**(本稿・条件つき)
> $\tilde{\mathbf N}_{\rm core}=\bigcap_{i=1}^4p_i^{-1}(\mathbf N)\in\mathrm{NFI}_{PB_4}(B_4)$ について:
> 1. $(\tilde{\mathbf N}_{\rm core})_{PB_3}=\mathbf N_0$(補題 B4-IND・§2.3 で再確認)、$(\tilde{\mathbf N}_{\rm core})_{\rm ord}=7$。
> 2. hexagon (2.18)(2.19) mod $\mathbf N_0$ $\iff$ hexagon mod $\mathbf N$(2401 Prop 3.4 は $N_{F_2}$ のみに依存し、$\mathbf N_0\cap F_2=\mathbf N\cap F_2=\mathcal V(F_2)$。近道 A(verbal ゆえ $\theta,\tau$ が降りる)は $c\in N$ を要さない — 仲裁ノート §1)。
> 3. pentagon (2.20) mod $\tilde{\mathbf N}_{\rm core}$ は**全 charming $f$ で恒真**(定理 B4-VAC)。
> 4. $T^{PB_3},T^{PB_2}$ 全射は $PB_3/\mathbf N_0\cong P\times C_7$ の Frattini 論法で自動(H8′ の直接拡張。$\Phi(P\times C_7)=[P,P]\times1$、像が $x^u,{}^{f}\!y^u,c^u$ を含み $\gcd(u,7)=1$)。
> ⟹ $\mathrm{GT}^\heartsuit_{2008}(\tilde{\mathbf N}_{\rm core})\big\vert_{\rm practical}$ は**本走の hexagon 通過 294 元そのもの**。
> 5. 一方、$\mathrm{PENT}_W$-FAIL の 252 元は **HSP-SOUND**($\widehat{GT}$ 由来 ⟹ (III) が $\hat K(0,5)$ で成立 ⟹ $Q$ で $\mathrm{PENT}_W$)により **genuine でない**。$f$ の類は $\mathbf N_0\cap F_2=N_{F_2}$ 単位で決まり、$\mathrm{PENT}_W$ は $fN_{F_2}$ の関数(翻訳ノート §5)なので、窓を $\mathbf N$ から $\mathbf N_0$ に細めても判定は変わらない。
> ⟹ $$\boxed{\ \tilde{\mathbf N}_{\rm core}\ \text{は、2008 の枠組みで }\mathbf{charming}\wedge\mathbf{fake}\ \text{な GT-shadow を }\mathbf{252}\ \text{個もつ窓の候補である。}\ }$$

- これは 2008 **Question 4.6**(p.43「charming かつ fake の例は 1 つも見つかっていない」)が求める型の対象である。
- **重要**: この観察は **【GAP-B4-1】に依存しない**。HSP-SOUND は $\widehat{GT}\to$ (III′) を直接使い、(2.20) を経由しないからである。
- 構造的な説明: 「charming shadow であること」は **pentagon の検出力がゼロな窓**($\tilde{\mathbf N}_{\rm core}$)が供給し、「fake であること」は **pentagon に敏感な別の対象**($Q=K(0,5)/W$ 上の $\rho$-ノルム)が供給する。**2 つの異なる解像度を組み合わせる**のがこの構成の中身であり、単一の窓の中では出せない。Dolgushev らの 35 窓は $\psi:PB_4\to S_d$ 由来の「一般の」窓なので、忘却射の核という退化した窓は標本に入っていない。

> ### ⚠ 規律申告(この観察について)
> - **格 = `conditional candidate`**。相対する前件: (α) HSP-SOUND(既在・HS 経由)、(β) 本走測定(294 / 42 / 252, BH-α-pent v1.1 = framework/measurement-relative)、(γ) 上記 1〜4 の各段(本稿で再導出したが **Sol 未監査**)。
> - **novelty は主張しない**。repo/台帳 grep は実施した(`Question 4.6` / `charming∧fake` / `恒真` / `忘却` — `docs/ provenance/ sol/`)。**該当する先行記述は工房内には無い**(Question 4.6 が未解決であることの引用は 6 箇所あるが、$\tilde{\mathbf N}_{\rm core}$ 型の構成は無い)。**外部文献は未調査** ⟹ 主張するなら司令塔の novelty ゲート(文献検査)を先に通すこと。
> - **検証計画**(安価): $PB_4/\tilde{\mathbf N}_{\rm core}\hookrightarrow P^4$ なので、$P$(既在の $7^8$ pc 群)を 4 つ並べるだけで機械確認できる。$R=PB_4/\mathcal V(PB_4)$($7^{41}$・ANUPQ 要)は**不要**。⟹ **工程 P1 の環境ブロッカーを迂回して先に走れる**。定理 B4-VAC の C-9(全通過)と同一装置。

---

## 8. Sol への監査点(3 点)

> **S-1 ★★ 補題 CORE-4(§2.2)**。$\mathrm{core}_{B_4}(p_4^{-1}(N))=\bigcap_ip_i^{-1}(N)$ を、代表元 $1,\sigma_3,\sigma_2\sigma_3,\sigma_1\sigma_2\sigma_3$ と「$p_4c_{\sigma_3^{-1}}=p_3$, $p_3c_{\sigma_2^{-1}}=p_2$, $p_2c_{\sigma_1^{-1}}=p_1$ が 6 生成元すべてで厳密一致」で示した一段。本体の「捻れは吸収される」1 行が**剰余類内の曖昧さしか扱っていない**という私の指摘を認めるか。

> **S-2 ★★ 【GAP-B4-1】の層別要求(§5.4 (b))**。(III)→(III′) の変換が関係 (I) = 2401 (3.10) を前件にもつ以上、**(2.20) と $\mathrm{PENT}_W$ の同値は hexagon 相対でしか主張できず、$[P,P]$ 全件の悉皆一致は予言できない**という判断を認めるか。認める場合、S1((3.10) のみ)と S2(full hexagon)のどちらを一致の登録層にすべきか。認めない場合、(I) を使わない (III)⟺(III′) の経路を示されたい。

> **S-3 ★★ 観察 Q46-CAND(§7)**。$\tilde{\mathbf N}_{\rm core}$ が 2008 の枠組みで 252 個の charming∧fake shadow をもつ、という結論に穴がないか。とくに (i) $\tilde{\mathbf N}_{\rm core}\in\mathrm{NFI}_{PB_4}(B_4)$ と $(\tilde{\mathbf N}_{\rm core})_{PB_3}=\mathbf N_0$、(ii) hexagon の $\mathbf N\to\mathbf N_0$ 不変性(Prop 3.4 の近道 A が $c\notin\mathbf N_0$ でも効くこと)、(iii) HSP-SOUND による fake 判定が窓を細めても保たれること、の 3 段。

---

## 9. 司令塔への上申(3 件)

1. ★★ **工程 P1 は現状の工房環境で実行不能**(ANUPQ の外部バイナリ `pq` が死んでいる。`LoadPackage` は `true` を返すので**見落としやすい**)。かつ仕様自体も `Exponent:=7` 欠落で誤り。⟹ ep-keeper / implementer へ「$R=PB_4/\mathcal V(PB_4)$ の構築経路の再設計」を発注されたい(代替路は §3.5 に記載)。
2. ★★ **観察 Q46-CAND(§7)は、工程 P1 のブロッカーを迂回して即座に走れる**($P^4$ の中の計算のみ・$7^{41}$ 不要)。これは本体の工程表にない**新しい安価な標的**であり、優先度の再検討に値する。ただし**先に prereg(IF-FIRST)と novelty ゲート**を通すこと。
3. **文献 pin の残作業**: LS1994 **p.17 と p.13** の逐語(f₁…f₅ の全項・lemma 5 直前の注意)が要る。scout ノートは材料を列挙しているが**式変形そのものは載っていない**。reader への追加抽出 1 件で【GAP-B4-1a】が閉じる見込み。

---

## 付録 A. 本稿の機械検算(**本走非接触**)

`scratchpad/b4check.py`(自作・本体の付録スクリプトとは独立実装)。自由群の語簡約 + 有理数係数の形式級数のみ。群の元の列挙ゼロ。

```
=== 20 composites  psi o p_i o phi  (images of x12, x23, x13, c) ===   [4x5=20 行・totals: psi = 8, cyclic(degenerate) = 12]
  p_4 o phi123     x12->x     x23->y     x13->x^-1y^-1  c->1      = psi
  p_3 o phi234     x12->1     x23->1     x13->y         c->y      CYCLIC-IMAGE   <- 本体の表では "1,1" にしか見えない行
  p_2 o phi123     x12->1     x23->1     x13->x         c->x      CYCLIC-IMAGE   <- 同上
  ...
=== pentagon (2.20) mod ker(psi-tilde) / mod B4-core, on f in [F2,F2] ===
  coord i=4 : LHS = 1.1.f (f)   RHS = f.1 (f)   -> IDENTITY
  coord i=3 : LHS = 1.f.1 (f)   RHS = f.1 (f)   -> IDENTITY
  coord i=2 : LHS = 1.f.1 (f)   RHS = 1.f (f)   -> IDENTITY
  coord i=1 : LHS = f.1.1 (f)   RHS = 1.f (f)   -> IDENTITY
=== LCS ranks ===
  PB4 : [6, 4, 10, 21, 54, 125]      sum(k<=4) = 41  => |PB4 : gamma5 PB4^7| = 7^41
  PB3 : [3, 1, 2, 3, 6, 9]           sum(k<=4) = 9   => |PB3 : V(PB3)| = 7^9 ; |P| = 7^8
  F2 (=Witt(2,k)) : [2, 1, 2, 3, 6, 9]   sum(k<=5) = 14 => 7^14 ; |[P',P']| = 7^12 ; fibre = 7^6
  K(0,5) = PB4/Z : [5, 4, 10, 21]    sum = 40        => |Q| = 7^40
```

GAP スモーク(**自由群 $F_2$ のみ**・本走宇宙非接触・`gap.ps1` 経由 / heap 2g):
```
Print("anupq load = ", LoadPackage("anupq"));            -> true
Pq(F2 : Prime:=2, ClassBound:=2);                        -> Error, failed to find any more of line (iostream dead?)
Size(Image(EpimorphismQuotientSystem(PQuotient(F2,7,2))))-> 16807 = 7^5      ( vs |F2 : gamma3 F2^7| = 7^3 )
```

---

## 付録 B. 格付け

| 対象 | 格 |
|---|---|
| 補題 **CORE-4**(本稿) | **paper-proof**(生成元上の厳密計算・6×3 = 18 件) |
| 定理 **B4-VAC** の再導出 | **paper-proof**(独立実装で 20 合成・4 座標を再現) |
| 定理 **B4-CANON** の再導出 | **paper-proof**((4) は既在実測 $\lvert Q\rvert=7^{40}$ + (3) 経路を採れば) |
| 命題 **BIT-252** の 4 段 | **paper-proof**(前件 = 294/42 の測定相対は継承) |
| 補題 **VERBAL-DESCENT**(本稿) | **paper-proof**(3 行) |
| §5 の【GAP-B4-1】裁定 | **文献相対**(scout ノートの抽出に依拠。原文頁画像は本稿では未参照) |
| 観察 **Q46-CAND**(本稿) | **conditional candidate**(HSP-SOUND + 本走測定相対・**Sol 未監査**) |
| ANUPQ 仕様の誤り | ★ **機械確認済**(GAP 4.16.0 ライブラリ `PQuotient` で $7^5$) |
| `verified` | ✗ 付かない(Lean 未使用) |
| `cross-checked` | ✗ 付かない(CV-9 判読未実施。本稿は「別人格による独立再導出」であって二系統実装の一致ではない) |
| **novelty** | ★ **主張しない**(§7 の repo grep 結果を含め、外部文献は未調査) |
