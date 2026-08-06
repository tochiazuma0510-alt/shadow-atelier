# BIT-252 **片側判定**試験 — 事前登録票 v1(**IF-FIRST 凍結**)

**状態札: `candidate(事前登録票・紙のみ / 機械実行ゼロ / 本走宇宙の新規評価ゼロ / 封印非接触 / 走行しない)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-06
- 委嘱: 司令塔(**裁定 637**・便 112 返書 **R-6b** の宿題)。**Sol 修正**: 「BIT-252 の**二択決着は FAIL**。**片側判定のみ認可**」。
- 対象: `docs/notes/b4_direct_adjudication_feasibility_v1_2.md` §4.4–4.5(命題 **BIT-252** と決定実験)。★ **v1/v1.1/v1.2 および事前登録票 `q46_…_v1.md` は 1 バイトも改変しない**(本票は versioned に上書きする別登録)。§11 に v1.2 への erratum を置く。
- 入力正本(すべて既在): `docs/notes/hs_prop7_translation_v1.md`(定義 NW(7)・補題 NW-1a/1b・**補題 DUM-HEX** §8.7.5・**定理 DUM-1/p** §8.3.2・NW-P5)/ `docs/notes/nw7_mainrun_predictions_iffirst_v1.md`(票 v1)+ `_addendum_pentlayer_v1.md`(PREC-1・付録 A)/ `docs/notes/hsp7_hexagon_arbitration_v1.md` §1(**2401 Prop 3.4** 逐語)/ `docs/notes/auto_settled_check_v1.md` §3.4(VERBAL-ISO)/ `docs/notes/b4_theorem_check_v1.md` §4(検分)/ `docs/scout/q46_citation_sweep_v1.md`(**2401 脚注 2**)
- ★ **本票は走らせない。** 発火は **凍結コミット後の司令塔発射**による。

---

## 0. 票の性格と拘束(先に 7 行)

| # | 拘束 |
|---|---|
| **0-1** | ★★ **本試験は片側判定である。** 認可される結論は **「片側の否定」だけ**である。**「294」「$\mathfrak G_{\rm genuine}=\mathrm{GT}(\mathbf N)$」「$\widehat{GT}\to\widehat{GT}_{gen}$ が全射」を、本試験の結果から導いてはならない**(2401 **Cor 5.4** の survival は**全深窓量化**であり、有限一窓では出ない)。 |
| **0-2** | ★ **停止規則は二分岐のみ**(§5)。**VERDICT A(全滅)** ⟹ $g^*\notin\mathrm{im}(\widehat{GT}_{gen})$。**VERDICT B(1 件以上通過)** ⟹ **`SURVIVES_TO_K` / 内訳 UNKNOWN**。第三の verdict を作らない。 |
| **0-3** | ★ **試験元は結果を見る前に semantic UID で一意凍結**(§3)。**選び直し禁止**。別の元を試すには**別票(v2)**を要する。 |
| **0-4** | ★ **分母 117,649・窓は $K$ **一窓のみ**・$m=0$ 固定・**延長禁止**(§2)。「通らなかったので次の窓へ」を本票の中で行わない。 |
| **0-5** | 機械実行は**ゼロ**。記載の数値はすべて紙の導出か、既に確定・Sol 検収済みの既在値である。**これが IF-FIRST の意味である。** |
| **0-6** | 本票は**新しい停止規則を発効させない**。§5 は提案であり、発効は司令塔裁定 + Sol ゲート。 |
| **0-7** | ★ **格 T の予言は的中しても情報量ゼロ**。**バグ検出器**として運用する(票 v1 §0-4 の規律を継承)。 |

---

## 1. Sol 修正の受領 — 何が生き残り、何が落ちたか

| 対象 | 判定 | 本票での扱い |
|---|---|---|
| **命題 BIT-252 の群論部分**($\mathfrak G^{\rm gentle}_{\rm genuine}(\mathbf N)$ は $\mathfrak G_{\rm ar}$ を含む部分群、$[\mathrm{GT}(\mathbf N):\mathfrak G_{\rm ar}]=7$ 素数 ⟹ 値は $\{42,294\}$) | **生きる**(値についての言明として正しい) | §7 の **Level 2** の前件として引く。**測定相対**(BH-α-pent) |
| **「1 元 × 1 窓の実験で二択が決着する」** | ★ **FAIL** | **撤回**。有限一窓の survival 試験は **genuine を肯定できない**(Cor 5.4 は全深窓量化)。⟹ **片側判定へ縮約**(§5) |
| **v1.2 §0-7 の「294 側なら…証人つきになる」** | ★ **誤読を招く** | §11 の erratum で訂正。**294 は本試験の出力になり得ない** |
| **決定実験の否定側**(全滅 ⟹ $g^*$ は fake) | **生きる** | Cor 5.4 の**易しい向き**(genuine ⟹ 全窓に survive)の対偶のみを使う ⟹ §7 Level 1 |

> ### ★ 一行で
> $$\boxed{\ \textbf{有限一窓の survival 試験は「genuine でない」を証明できるが、「genuine である」は証明できない。}\ }$$

---

## 2. 宇宙・窓・パラメータの凍結(**後から変えない**)

### 2.1 主窓(既在・再定義しない)

$$\mathbf N=\mathcal V(F_2)\times\langle c\rangle,\quad N_{F_2}=\mathcal V(F_2)=\gamma_5(F_2)F_2^{\,7},\quad P=F_2/N_{F_2}\ (\lvert P\rvert=7^8),\quad \lvert[P,P]\rvert=7^6 .$$
本走の答え: hexagon **294**・$\mathrm{PENT}_W$ **42**・hexagon-only **252**。

### 2.2 ★ 試験窓 $K$(**一窓のみ**)

$$\boxed{\ K:=\mathcal V_5(F_2)\times\langle c\rangle,\qquad \mathcal V_5(F_2):=\gamma_6(F_2)\,F_2^{\,7},\qquad P':=F_2/\mathcal V_5(F_2).\ }$$

| 事実 | 値 | 根拠 |
|---|---|---|
| $K\in\mathrm{NFI}_{PB_3}(B_3)$ | ✓ | $\mathcal V_5(F_2)$ と $\langle c\rangle$ はともに $PB_3$ の特性部分群、その積も特性 ⟹ $B_3$ 正規。有限指数 |
| $K\le\mathbf N$ | ✓ | $\gamma_6\subseteq\gamma_5$ |
| $K_{F_2}=\mathcal V_5(F_2)$ | ✓ | 箱型($(A\times B)\cap(F_2\times1)=A\times1$・補題 NW-1a/1b (2)) |
| $K_{\rm ord}$ | **7** | Prop 2.3 の lcm。$\mathrm{ord}(\bar x)=\mathrm{ord}(\bar y)=\mathrm{ord}(\bar c)=7$ ⟹ $\mathcal X_K=\mathcal X_{\mathbf N}$ |
| $K$ は isolated | ✓ | VERBAL-ISO(前件 $c\in K$ ✓・$K_{F_2}$ verbal ✓)。★ **本試験の結論には不要**(検分 §4.4)だが記録 |
| $\lvert P'\rvert$ | $7^{2+1+2+3+6}=\mathbf{7^{14}}$ | Witt$(2,k)=(2,1,2,3,6)$・類 $5<p=7$ ゆえ正則 $p$ 群(Lazard) |
| $\lvert[P',P']\rvert$ | $7^{12}$ | 同上 |
| **fiber** $\ker(P'\to P)=\mathcal V(F_2)/\mathcal V_5(F_2)$ | $7^{\mathrm{Witt}(2,5)}=7^6=\mathbf{117{,}649}$ | ★ **本票の分母** |

- ★ fiber $=\gamma_5(P')$ は **$P'$ の中心・初等アーベル**であり、$[P',P']$ に含まれる ⟹ **持ち上げは自動的に charming**(検分 §4.4 が独立確認)。
- ★ SURJ は **H8′**($P'$ は 7 群・$\bar f'\in[P',P']=\Phi(P')$・$\gcd(2m+1,7)=1$)で**自動**。

### 2.3 ★ 延長禁止

> **本票の射程は $K$ ただ一窓・$m=0$ ただ一層・$g^*$ ただ一元である。** VERDICT B が出ても、**本票の中で**より深い窓($\gamma_7F_2^{\,7}$、$\gamma_5F_2^{\,49}$ 等)や第 2 の試験元へ進んではならない。進むなら**別票(v2)を先に凍結**する。

---

## 3. ★ 試験元の凍結(**semantic UID**・選び直し禁止)

### 3.1 選定基準(**結果を見る前に書く**)

| # | 基準 | 理由 |
|---|---|---|
| **C-1** ★★ | **252 への所属が「測定リストの参照」ではなく「定理」で言える元を選ぶ** | 本走 cert の 252 リストから選ぶと**選定が測定依存**になり、IF-FIRST が壊れる |
| **C-2** | **$m=0$** を選ぶ | (3.11) の $y^m$ 因子が消え、判定が最も単純な形になる(PRE-1 と同じ計算層)。$m=0\in\mathcal X$(=$2m+1=1$ は単元) |
| **C-3** | 判定に必要な構造がすべて既在の紙で押さえられている元を選ぶ | 較正 fixture(§6)を同じ道具で組める |

### 3.2 ★ 凍結される試験元 $g^*$

$$\boxed{\ g^*:=\bigl[\,m=0,\ \ \bar f=\bar h_4\,\bigr],\qquad h_4:=v_1\cdot v_2^{\,4}\cdot v_3\ \in\gamma_4(F_2)\ }$$
$$v_1:=[[[x,y],x],x],\qquad v_2:=[[[x,y],x],y],\qquad v_3:=[[[x,y],y],y].$$

> ### semantic UID ブロック(**これが凍結の本体** — 実装の順序・pcgs・添字に依存しない)
> ```
> UID              : BIT252-TESTELT-v1
> ambient          : F2 = <x,y> (自由群), x = x_12, y = x_23  (定義ノート §1.5.1)
> commutator conv  : [a,b] := a^-1 b^-1 a b        (GAP Comm(a,b) と同一・CV-1/CV-2 pin)
> v1               : Comm(Comm(Comm(x,y),x),x)
> v2               : Comm(Comm(Comm(x,y),x),y)
> v3               : Comm(Comm(Comm(x,y),y),y)
> f_word           : v1 * v2^4 * v3                (順序無害: gamma_4(P) は中心)
> m                : 0
> window(main)     : N   = V(F2)  x <c>,  V(F2)  = gamma_5(F2) F2^7
> window(test)     : K   = V5(F2) x <c>,  V5(F2) = gamma_6(F2) F2^7
> f_class(main)    : f_word * V(F2)   in [P,P]      (= 群元 h_4 の類・Lazard 座標 h_4 = v1 + 4 v2 + v3)
> alias            : dummy family t=1  (定理 DUM-1/p の f_t = h_4^t で t=1)
> ```
> ★ **凍結時に司令塔が上記ブロックの SHA-256 を計算し、cert に pin する**(値の書き写し禁止・機械生成)。

### 3.3 ★ $g^*\in252$ は **定理**である(測定参照なし)

| # | 主張 | 根拠 |
|---|---|---|
| **(a)** | $\bar h_4\in[P,P]$、$m=0\in\mathcal X$ ⟹ **本走宇宙の元** | $\gamma_4(F_2)\subseteq[F_2,F_2]$ |
| **(b)** | $(0,\bar h_4)$ は **hexagon を通る** | ★ **補題 DUM-HEX**(翻訳ノート §8.7.5): $f_t=h_4^{\,t}$ は hexagon を **$P$ の中の exact な等式**として満たす($\theta_*\mathfrak h_4=-\mathfrak h_4$、$(1+\tau_*+\tau_*^2)\mathfrak h_4=0$。$\gamma_4(P)$ が中心・初等アーベルで $\theta,\tau$ がそこで次数付き作用ゆえ) |
| **(c)** | $(0,\bar h_4)$ は **$\mathrm{PENT}_W$ を落ちる** | ★ **定理 DUM-1/p** + **NW-P5**($\eta:=\nu_4(j\mathfrak h_4)\ne0$・発火条件 2 で実測 Sol PASS): $\mathrm{PENT}\iff t\eta=0$、$t=1$ ゆえ $\eta\ne0$ で FAIL |
| **(d)** | ⟹ $g^*\in$ **252**(hexagon-PASS ∧ $\mathrm{PENT}_W$-FAIL) | (b)+(c) |

⟹ **選定は本走 cert の内容に一切依存しない。**

### 3.4 却下した候補(**なぜ選ばなかったか**)

| 候補 | 却下理由 |
|---|---|
| 252 の中の**一般の元** | 252 のリストは本走 cert からしか得られない ⟹ **選定が測定依存**(C-1 違反) |
| $h_4^{\,t}$($t=2..6$) | 同値だが単純さで劣る。**t=1 が最小の非零 $t$** |
| ★ $g_1$($\log g_1=\mathfrak h_3$・PRE-2 の測定対象) | ★ **252 所属が定理で言えない**。$g_1\in A=\mathrm{hex}(0)$ は PRE-1 で確定だが、**$\mathrm{PENT}_W$ の可否は $\xi=D(g_1)$ 未測定ゆえ UNKNOWN**(【EXQ-GAP-3】・分岐 B-2 は OPEN)⟹ **C-1 違反** |
| 生の Hall 語 $r$($\log r=\mathfrak h_3+(v_1{+}v_2{+}v_3)$) | ★ **そもそも hexagon を通らない**(PENT-LAYER addendum §5: (3.11) の次数 4 欠陥 $=3\ne0\bmod7$)⟹ 252 の元ですらない。**負の較正 fixture としてのみ使う**(§6 の F-4) |

---

## 4. 判定手続き

### 4.1 判定の定義(**survival の有限形**)

$g^*$ が $K$ に **survive** する $:\iff$ $\exists\bar f'\in[P',P']$ で
1. $\bar f'$ は $P'\to P$ で $\bar h_4$ に写る(= fiber の元・**117,649 個**)、かつ
2. $(m,\bar f')=(0,\bar f')$ が **$K$ の GT-shadow** である。

**2 の中身**(2401 **Prop 3.4** を $N:=K$、$(m,f)\in\mathbb Z\times[F_2,F_2]$ に適用。前件は 2 条のみで充足):
$$\textbf{(3.10)}\ \ f'\,\theta(f')\in\mathcal V_5(F_2),\qquad \textbf{(3.11)}_{m=0}\ \ \tau^2(f')\,\tau(f')\,f'\in\mathcal V_5(F_2).$$
charming と SURJ は §2.2 の通り**自動**、$m=0\in\mathcal X_K$ ✓。⟹ **検査すべきは (3.10)(3.11) の 2 本のみ。**

### 4.2 ★ Lane G(主・群の中の悉皆)

$P'$($7^{14}$ の pc 群)を構築し、fiber の **117,649 元**を列挙して (3.10)(3.11) を評価する。
⚠ **実装前件**: $P'=F_2/\gamma_6F_2^{\,7}$ の構築経路を先に確定すること。**ANUPQ の外部バイナリ `pq` は本機で動作しない**(`LoadPackage` は `true` を返すが `Pq(...)` は `iostream dead`・B₄ ノート v1.2 §5.4)。代替: `PQuotient(F_2,7,5)` で $\bar G$ を作り $P'=\bar G/(\gamma_6(\bar G)\cdot\mathrm{Agemo}_1(\bar G))$。**予言 $\lvert P'\rvert=7^{14}$**。

### 4.3 Lane L(副・$\mathbb F_7$ 線型代数)— **任意・不一致は仲裁**

fiber は $\gamma_5(P')$(中心・初等アーベル・階数 6)であり、$\bar f'=\exp(\mathfrak h_4'+\zeta)$($\zeta\in\mathrm{gr}_5\otimes\mathbb F_7$)と書ける。$[\gamma_4,\gamma_4]\subseteq\gamma_8=1$ ゆえ BCH の交差項は消え:
- **(3.10)**: $\theta$ は**次数付き**ゆえ $f'\theta(f')=\exp\bigl((1+\theta_*)\mathfrak h_4+(1+\theta_*)\zeta\bigr)$、$(1+\theta_*)\mathfrak h_4=0$ ⟹ $\boxed{(1+\theta_*)\zeta=0}$(**線型**)。
- **(3.11)$_{m=0}$**: $\tau$ は次数付きでないので $\mathfrak h_4$ が次数 5 へ落とす項 $\Psi_5$ が入り $\boxed{(1+\tau_*+\tau_*^2)\zeta=-\Psi_5}$(**アフィン**)。

⟹ **通過集合は $\mathrm{gr}_5\otimes\mathbb F_7$($\dim 6$)の中の空集合またはアフィン部分空間**。
★ この構造は **PRE-1(次数 4 の $\Psi$)の 1 次上**であり、既存 `search/probe/hsp7_v1/hs_prop7_hexagon_vs_pentagon.py` の**次数 5 拡張**で計算できる。
⚠ Lane L は**本起草者の導出**である。Lane G と食い違ったら **理論か実装のどちらかが誤り** ⟹ **数学者へ差戻し**(実装バグと即断しない)。

---

## 5. ★★ 停止規則(**二分岐のみ** — 逐語)

> ### VERDICT A — `NO_SURVIVAL`
> **trigger**: fiber の **117,649 元すべて**が (3.10) または (3.11) を落とす(通過数 $=0$)。
> **結論(認可される)**:
> - **Level 1(前件最小)**: $g^*$ は $K$ に survive しない ⟹ **2401 Cor 5.4 の易しい向き**(genuine ⟹ 全 $K'\le\mathbf N$ に survive)の対偶で $\boxed{g^*\notin\mathrm{im}(\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N))}$ ⟹ **$\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N)$ は全射でない**。★ **BIT-252 を使わない**。
> - **Level 2(BIT-252 相対)**: 命題 BIT-252 + $\mathfrak G_{\rm ar}=42$(BH-α-pent・**測定相対**)⟹ $\boxed{\lvert\mathfrak G^{\rm gentle}_{\rm genuine}(\mathbf N)\rvert=42}$ ⟹ **252 全件が gentle-fake**。
> **格**: Level 1 = paper-proof(測定相対 = 通過数 0 の実測)。Level 2 = **conditional**(BH-α-pent 相対)。

> ### VERDICT B — `SURVIVES_TO_K` / **内訳 UNKNOWN**
> **trigger**: 通過数 $\ge1$。
> **結論(認可される)**: 「$g^*$ は $K$ に survive する」**のみ**。
> ★ **禁止事項(逐語)**: 本 verdict から次を導いてはならない —
> - 「$\mathfrak G^{\rm gentle}_{\rm genuine}=294$」/「$g^*$ は genuine」/「252 は gentle-genuine」
> - 「$\widehat{GT}\to\widehat{GT}_{gen}$ は全射でない(が示された)」/「$\widehat{GT}_{gen}\supsetneq\widehat{GT}$」
> - 「内訳が決着した」
> **理由**: 2401 **Cor 5.4** の survival 特徴づけは **$\forall K'\le\mathbf N$** の量化を含み、**有限一窓の PASS はその全称命題の一事例にすぎない**。
> **内訳の状態**: **UNKNOWN のまま**(v1.2 §0-7 の表現は §11 で訂正)。

### 5.1 STOP 規則(**提案**・発効は司令塔裁定 + Sol ゲート)

| ID | trigger | verdict |
|---|---|---|
| **S-B1-0** | §6 の較正 fixture が 1 つでも落ちる | **発火禁止 / STOP** |
| **S-B1-1** ★ | 通過数が $\{0\}\cup\{7^k:0\le k\le6\}$ **以外** | **IMPLEMENTATION_BUG_SUSPECTED / STOP**(§4.3 のアフィン構造の破れ) |
| **S-B1-2** | fiber の列挙数が **117,649** でない | **STOP**(分母の過不足) |
| **S-B1-3** | cert の試験元 UID が §3.2 の凍結 SHA-256 と一致しない | **STOP**(選び直しの検出) |
| **S-B1-4** ★ | cert・報告・便のいずれかに **「294」「二択決着」「全射である」「genuine である(g\* について)」** の語が VERDICT B の文脈で現れる | **報告無効 / 差戻し**(Sol 裁定の逐語履行) |
| **S-B1-5** | 窓を $K$ 以外へ延長した / 第 2 の試験元を追加した / $m\ne0$ を評価した | **票の射程外 ⟹ 別票を要する** |
| **S-B1-6** | Lane G と Lane L の通過数が不一致 | **数学者へ差戻し**(実装バグと即断しない・§4.3) |
| **S-B1-7** | $\lvert P'\rvert\ne7^{14}$ | **STOP**(構築経路の誤り。まず `Exponent`/`Agemo` の仕様を疑う) |

---

## 6. 較正(**hexagon 検査器の既知解 fixture**・発火前件)

すべて **$P$(類 4)側**で、**同一の検査器コードに $\mathcal V(F_2)$ を渡して**走らせる(窓だけ差し替え)。

| # | 入力 | 期待 | 出所 |
|---|---|---|---|
| **F-1** | $m=0$, $f=1$ | **PASS** | 自明((3.10)(3.11) とも $1$) |
| **F-2** | $m=-1\ (=6)$, $f=1$ | **PASS** | 補題 LAY-2: $x^{-1}z^{-1}y^{-1}=1$ は $F_2$ の中の **exact な等式** |
| **F-3** ★ | $m=0$, $f=h_4^{\,t}$($t=0..6$) | **7/7 PASS** | 補題 **DUM-HEX**($P$ の中の exact な等式) |
| **F-4** ★ | $m=0$, $f=r:=\mathrm{Comm}(\mathrm{Comm}(x,y),x)\cdot\mathrm{Comm}(\mathrm{Comm}(x,y),y)$ | ★ **FAIL** | **負の fixture**。PENT-LAYER addendum §5: (3.11) の次数 4 欠陥 $=(2\alpha-\beta+2\gamma)$ at $(1,1,1)=3\ne0\bmod7$ |
| **F-5** | $m=0$, $f=g_1:=r\,s^{-1}$($s=v_1v_2v_3$、$\log g_1=\mathfrak h_3$) | **PASS** | PRE-1($\Psi=0$・F106-2.3 で Sol PASS) |
| **F-6** ★★ | 層 $m=0$ の通過数(宇宙 $=[P,P]$ 全 117,649) | **49** | 本走の実測(B-1a・$294/6$)。**回帰試験** |
| **F-7** ★ | $\mathrm{gr}_4\otimes\mathbb F_7$ の次数 4 斉次 hexagon 解空間 | **直線 $\mathbb F_7(1,4,1)$**(343 点悉皆) | D4-POWER (a)。★ **交換子規約・基底 $(v_1,v_2,v_3)$・$\theta_*/\tau_*$ の作用を同時に較正する**(PENT-LAYER addendum 付録 A で既に整数演算で確認済) |
| **F-8** | fiber の全 117,649 元が $P'\to P$ で $\bar h_4$ に写る | 全一致 | 列挙器自身の検査 |

> ★ **F-7 が最重要**: $[a,b]$ の向きを取り違えると $\mathfrak h_4=v_1+4v_2+v_3$ が別の元になる。**F-7 が通らない実装で試験元 UID を解釈してはならない。**

---

## 7. 予言(**凍結** — BIT1-P1〜P5)

| ID | 予言 | 格 | 分岐 |
|---|---|---|---|
| **BIT1-P1** | $\lvert P'\rvert=7^{14}$、$\lvert[P',P']\rvert=7^{12}$、fiber $=7^6=117{,}649$ | **T\***(Witt + Lazard) | 不一致 ⟹ S-B1-7 |
| **BIT1-P2** | 較正 F-1〜F-8 が全 PASS | **T**(既知解・**情報量ゼロ = バグ検出器**) | 1 件でも落ちれば S-B1-0 |
| **BIT1-P3** ★ | fiber の通過数 $\in\{0\}\cup\{7^k:0\le k\le6\}$ | **T\***(§4.3 のアフィン構造) | 範囲外 ⟹ S-B1-1 |
| **BIT1-P4** | Lane G と Lane L の通過数が一致 | **T\***(Lane L は本起草者の導出) | 不一致 ⟹ S-B1-6(数学者へ差戻し) |
| **BIT1-P5** ★ | ★ **どちらの verdict になるかの登録済み予想** | **C**(下記) | A / B の 2 分岐は §5 に登録済 |

### 7.1 ★ BIT1-P5 の中身(**正直な予想を先に書く**)

> **予想: VERDICT B(`SURVIVES_TO_K`)の側に賭ける。** 根拠(**証明ではない**):
> 次数 4 で同型の問いが立ったとき($\Psi:=[(\tau_\bullet+\tau_\bullet^2)\mathfrak h_3]_{\deg4}$ が $(1+\tau_*+\tau_*^2)$ の像に入るか)、**PRE-1 の答は $\Psi=0$、すなわち可解**であった。次数 5 の $\Psi_5$ が同様に可解である可能性は低くない。
> ⚠ **これは類推であって根拠ではない。** 実際、$\Psi_5$ の値は**未計算**であり、$\ker(1+\theta_*)\cap\ker(1+\tau_*+\tau_*^2)$ の次元 $d_5$ も**未計算**である。
>
> ### ★ B が出ても無駄走ではない(**設計上の要点**)
> VERDICT B のとき、run は次の 2 つの**構造的データ**を返す:
> - $d_5=\dim\bigl(\ker(1+\theta_*)\cap\ker(1+\tau_*+\tau_*^2)\bigr)$ on $\mathrm{gr}_5\otimes\mathbb F_7$(通過数 $=7^{d_5}$)
> - $\Psi_5$ が像に入るという事実(可解性)
> これらは**次の窓を設計するための入力**である。⟹ **B は「内訳 UNKNOWN の維持」+「深さ 5 の構造の確定」**という二重の出力を持つ。

### 7.2 ★ VERDICT A が出た場合の意味(**先に書いておく**)

掃引ノート `docs/scout/q46_citation_sweep_v1.md` の **N-3**: **2401.06870 脚注 2(2024)**逐語「the authors of this paper do not know a single example of a fake GT-shadow」。
⟹ VERDICT A は **gentle 系の fake GT-shadow の実例**を与える型の結果である。
⚠ **novelty は主張しない**。掃引の射程限界(別語彙・GT 業界本流の引用未探索)は Q4.6 票 §7.2 の L-1〜L-3 がそのまま当てはまる。**「初」「解決」の語は司令塔の novelty ゲート通過まで禁止**(S-B1-4 と同流儀)。

---

## 8. 走行仕様(**凍結後に司令塔が発射**)

| 段 | 内容 | 出力 |
|---|---|---|
| **R0** | §6 の較正 F-1〜F-8($P$ 側・同一コード・窓だけ差し替え) | gate cert |
| **R1** | $P'$ の構築(§4.2)。$\lvert P'\rvert$ を実測 | **BIT1-P1** |
| **R2** | fiber(117,649)の列挙 + F-8 | 列挙 cert |
| **R3** | Lane G: (3.10)(3.11) を $m=0$ で全件評価 | 通過数 |
| **R3′**(任意) | Lane L: $\mathbb F_7$ アフィン系を解く | 通過数(照合) |
| **R4** | verdict 判定(§5 の二分岐のみ) | `NO_SURVIVAL` or `SURVIVES_TO_K` |

**cert 必須欄**: `FW=B3-2401` / `window_arity=3` / `window=K(gamma6 F2^7 x <c>)` / `m=0`(固定)/ `test_element_uid_sha256` / `denominator=117649` / `equation_ids=[3.10, 3.11]` / `verdict ∈ {NO_SURVIVAL, SURVIVES_TO_K}` / `lane ∈ {G,L}` / `calibration=F-1..F-8`。
★ **本走宇宙(705,894 対)の再測定はしない。** 本試験は $\mathbf N$ の判定を一切上書きしない。

---

## 9. 格付け・【GAP】・規律申告

### 9.1 格付け

| 対象 | 格 |
|---|---|
| §2.2 の窓 $K$ の性質($\in\mathrm{NFI}$・$\le\mathbf N$・$K_{\rm ord}=7$・fiber $=7^6$) | **paper-proof**(検分ノート §4.4 が独立確認) |
| §3.3 の $g^*\in252$(**定理**) | **paper-proof candidate**((b) = 補題 DUM-HEX / (c) = 定理 DUM-1/p + **NW-P5 実測相対**) |
| §4.1 の survival の有限形 | **paper-proof**(2401 Prop 3.4 + H8′) |
| §4.3 の Lane L(アフィン構造) | ★ **paper-proof candidate**(**本起草者の導出・Sol 未監査**)。BIT1-P3/P4 の根拠 |
| §5 VERDICT A **Level 1** | **paper-proof**(Cor 5.4 の易しい向きのみ)+ 実測相対 |
| §5 VERDICT A **Level 2** | **conditional**(BIT-252 + BH-α-pent 相対) |
| §5 VERDICT B | ★ **UNKNOWN の宣言**(結論を出さないことが結論) |
| `verified` / `cross-checked` | ✗(Lean 未使用・CV-9 判読未実施・機械実行ゼロ) |
| **novelty** | ★ **主張しない**(§7.2) |

### 9.2 【GAP】

| 札 | 内容 | 状態 |
|---|---|---|
| ★ **【GAP-BIT-1】** | $\Psi_5$ の値と $d_5$ が**未計算** ⟹ verdict がどちらになるかは紙で決まらない | **UNKNOWN**(本試験の測定対象そのもの) |
| ★ **【GAP-BIT-2】** | Lane L のアフィン還元は本起草者の導出で **Sol 未監査**。とくに「$\theta$ は次数付き・$\tau$ は次数付きでない」の非対称と、$\mathfrak h_4'$ の持ち上げ選択が $\zeta$ のアフィン平行移動にしか効かないこと | **要監査**(Sol Q-2) |
| **【GAP-BIT-3】** | $P'$ の構築経路(ANUPQ ブロッカーの射程内か) | **未確定**(【工程要請 W-1】と同根) |
| **【GAP-B4-3】**(継承) | Cor 3.13 / Cor 5.4 の survival 減少列の**停止点に有効上界がない** | **UNKNOWN**。★ **本票の片側性はまさにこの GAP の帰結である** |

### 9.3 規律申告

- ★ **機械実行ゼロ**。§2.2 の位数は Witt 数の算術(既在)、他はすべて既在の紙・既在の測定値。
- ★ **本走宇宙(705,894 対)の候補を 1 件も新規評価していない。** 試験元 $g^*$ の 252 所属も**定理で言っており、cert のリストを引いていない**。
- **封印 3 量非接触。既在文書を 1 バイトも改変していない**(B₄ ノート v1/v1.1/v1.2・Q4.6 票・翻訳ノート・検分ノート・掃引ノートすべて read-only)。
- **外部文献検索ゼロ。** §7.2 の 2401 脚注 2 は掃引ノートからの引用。
- ★ **走らせない。** 発火は凍結コミット後の司令塔発射。
- **新しい停止規則を発効させない**(§5.1 は提案)。

---

## 10. Sol への監査点(3 点)

> **Q-1 ★★★ 片側性の実装**(§5)。VERDICT B から導いてよい結論を「$g^*$ は $K$ に survive する」**のみ**に限り、「294」「全射」「genuine」を **S-B1-4 で報告無効**にする設計が、R-6b の修正の逐語履行になっているか。**Level 1 / Level 2 の二段**(前件最小の非全射性 / BIT-252 相対の $=42$)の分離を認めるか。

> **Q-2 ★★ Lane L のアフィン還元**(§4.3・【GAP-BIT-2】)。fiber $=\gamma_5(P')$ が中心・初等アーベルゆえ $\bar f'=\exp(\mathfrak h_4'+\zeta)$ と書け、$[\gamma_4,\gamma_4]\subseteq\gamma_8=1$ で BCH 交差項が消える ⟹ (3.10) が線型・(3.11) がアフィンになる、という一段。および **BIT1-P3(通過数 $\in\{0\}\cup\{7^k\}$)を格 T\* のバグ検出器として登録**してよいか。

> **Q-3 ★★ 試験元の凍結**(§3)。$g^*=(0,h_4)$ を選び、**252 所属を定理(DUM-HEX + DUM-1/p + NW-P5)で言う**ことで選定を測定非依存にした設計を認めるか。とくに **$g_1$($\log=\mathfrak h_3$)を「$\mathrm{PENT}_W$ 未測定ゆえ 252 所属が定理で言えない」として却下**した判断(§3.4)。

---

## 11. ★ v1.2 への erratum(**当該ファイルは不改変**)

対象: `docs/notes/b4_direct_adjudication_feasibility_v1_2.md`(commit `0fa1569`)。**1 バイトも改変しない。**

| # | 箇所 | 訂正 |
|---|---|---|
| **E-4** ★ | §0-7 の「**294 側なら $\widehat{GT}\to\widehat{GT}_{gen}$ が全射でないことが有限窓で証人つきになる**」 | ★ **誤読を招く表現**。正しくは「**42 側**(= 有限一窓での survival 失敗)が観測されたときに、**$\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N)$ の非全射性**が有限証人つきで出る」である。**294 側は有限一窓では出せない**(Cor 5.4 の全深窓量化)。また「$\widehat{GT}\to\widehat{GT}_{gen}$ が全射でない」は **294 側**の帰結であり、**本試験の出力にはなり得ない** |
| **E-5** | §4.4 系・§4.5 の「**決着する**」の語 | **VERDICT A の側にのみ適用される**。VERDICT B は「決着」ではなく **UNKNOWN の維持**である。命題 BIT-252 そのもの(値が $\{42,294\}$ に入ること)は**生きている**が、**実験がその二択を決着させるとは言えない** |
| **E-6** | §4.5 の「**通るものがある ⟹ 不決(より深い窓へ)**」 | 表現は正しいが、**本票では「より深い窓へ」を自動的に行わない**(延長禁止・§2.3)。深化は別票 v2 の凍結を要する |

> ★ **登録値への影響**: v1.2 の予言 B4-EXQ-1〜9 と Q4.6 票の Q46-P1〜P7 は**いずれも変更されない**。⟹ **S-7′ に抵触しない。**

---

## 12. 本票の凍結宣言

本票は **§2 の窓・分母・$m$**、**§3 の試験元 UID**、**§5 の二分岐と禁止事項**、**§6 の較正**、**§7 の予言**を凍結する。発火後にこれらを緩める改稿は行わない(**S-7′ 準拠**)。改訂が必要なら **versioned な別票(v2)**として起草し、v1 と結果の記録を不変保存する。

> ★ **登録済み分岐への着地は「外れ」でなく「決着」である**(票 v1 §7 の丙類規約)。ただし **VERDICT B は「予言の決着」であって「内訳の決着」ではない** — この 2 つを報告で混ぜないこと。
