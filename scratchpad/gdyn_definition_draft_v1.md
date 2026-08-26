# $G_{\rm dyn}$ 定義起草 v1 — 力学系的 Belyi 写像の仮想自己準同型族の正規化群

`DIR: 正側(算術像の上界)+ 対象選定 / FRAME: Out(F̂₂) を力学で切る(GT とは別方向)`

**状態札**: `§1 = 文献判定(逐語 pin つき)/ §2 = 定義起草 candidate(well-defined 補題 5 本は未証明・列挙のみ)/ §2.5 = paper-proof(短い)/ §3 = 実験仕様 candidate / novelty は §1(a) の判定に依存`

- 起草: 影工房 数学者(Opus 5)/ 2026-08-26 / 委嘱: 司令塔(研究者承認済み・新対象確定作業)
- 一次資料: `papers/wood-math0304489-belyi-extending-maps.pdf`(sha256 `6820541a…3ff78`・**全文精読**)。金庫報告 `intel/gdyn_hunt_20260826/report_v1.md` は本起草前に未読(独立性のため)。
- 既在の工房資産: 定義ノート §2・`gt_grt_dictionary_memo_v1.md`(NILP-VOID)・`d972_idx3_arith_datum_independent_v1.md`

---

## §0 三行

1. **Wood の写像クラスは $G_{\rm dyn}$ のそれと厳密に一致する** — Belyi-extending $\iff$ 「$\{0,1,\infty\}$ 上でのみ分岐 ∧ $\varphi(\{0,1,\infty\})\subseteq\{0,1,\infty\}$」$\iff$ **post-critical set $\subseteq\{0,1,\infty\}$ の PCF 写像で ℚ 上定義**。恒等的に同じ対象。
2. **Wood は群を定義していない**(逐語判定・§1(a))。彼が作るのは (i) dessin へのモノイド作用 (ii) 不変量 $M_\varphi=M\circ\varphi_*$ (iii) 「両方の不変量が一致する」という**必要条件の族**。**正規化子として $\mathrm{Out}(\hat F_2)$ を切る操作はどこにもない。** ⟹ **空席は残っている。**
3. ★**方向が予想と逆で、そこが価値**: new-type relations は $\widehat{GT}$ の**中で $G_\mathbb{Q}$ の像を切る**関係式。ゆえに $G_{\rm dyn}\supseteq\widehat{GT}$ ではなく、**$G_\mathbb{Q}\subseteq\widehat{GT}\cap G_{\rm dyn}\subseteq\widehat{GT}$** が正しい絵。⟹ **$G_{\rm dyn}$ は井原問題を「上から」削る道具**であり、工房が現在持たない **算術像の計算可能な上界**を有限窓で与える(§3)。

---

## §1 Wood の射程の精密判定

### 1(a) 定式化と「群に達しているか」の逐語判定

**定義(§3.1 逐語)**:
> "A map $\varphi:\mathbb P^1\to\mathbb P^1$ is called **Belyi-extending** if $\varphi$ is a Belyi map defined over $\mathbb Q$, and $\varphi(\{0,1,\infty\})\subseteq\{0,1,\infty\}$."

**Proposition 2(§3.1 逐語)**:
> "Let $(X,p_X)$ be a Belyi pair corresponding to a dessin $\Delta$ and $\varphi$ be a Belyi-extending map. If $I$ is a $G_\mathbb{Q}$-invariant of dessins, so is $I\circ\varphi$."
> 証明の核: "for $\sigma\in G_\mathbb{Q}$, $\sigma(\varphi)=\varphi$, and thus $\sigma((X,\varphi\circ p_X))=(\sigma(X),\varphi\circ\sigma(p_X))$."

⟹ **可換性 $\sigma\circ\varphi_*=\varphi_*\circ\sigma$ の根拠は「$\varphi$ が ℚ 上定義」というだけ。** Thurston 剛性も力学系的性質も使っていない。

**モノイド性(§4 逐語)**: "The family of Belyi-extending maps is **closed under composition**."(左右から $\mathrm{Aut}(\mathbb P^1,\{0,1,\infty\})\cong S_3$ を合成した族の概念も §3.2 Remark で導入。)

**★判定(a)**: **群の定義には達していない。** Wood が構成するのは
- 写像の**モノイド** $\mathcal B$(合成閉・$S_3$ 両側作用つき)、
- dessin 集合へのモノイド作用 $\varphi_*$、
- 不変量 $I\circ\varphi_*$(Prop 2 で $G_\mathbb{Q}$-不変)、
- 具体例 $M_{4t(1-t)}$(= cartographic group)、$M_{\varphi\circ(1/t)}$、$M_{\varphi\circ(t/(t-1))}$(**本人が新規と明言**)。
**「全ての $\varphi_*$ と可換な $\mathrm{Out}(\hat F_2)$ の元」という部分群は一度も定義されていない。**§5 の "further research" も「新しい $\varphi$ を探して新しい不変量を作る」方向のみ。
⟹ **$G_{\rm dyn}$ の空席は Wood によっては埋まっていない。**

### 1(b) 参照 [12]–[14] の書誌(本文から読み取り)

| # | 書誌(Wood の References から逐語) | $G_{\rm dyn}$ への近さ |
|---|---|---|
| **[12]** | **H. Nakamura, "Some classical views on the parameters of the Grothendieck-Teichmüller group", *to appear in Progress in Galois Theory*.** | ★**最重要**。Wood 本文(§1)逐語: "In [12], Nakamura **discusses the general properties necessary for a map to give new-type relations via the Belyi-extending procedure**, computes these relations in some specific examples, and **gives a list of examples left for further work**." ⟹ **関係式系の一般論はここにある**。ただし「必要な性質の議論+具体例+宿題リスト」であって、**群を定義した形跡は Wood の要約からは読み取れない**。 |
| [13] | H. Nakamura and L. Schneps, "On a subgroup of the Grothendieck-Teichmüller group acting on the tower of profinite Teichmüller modular groups", **Invent. Math. 141 (2000), no. 3, 503–560**. | 具体例(特定の $\varphi$)。**タイトルに "a subgroup of $\widehat{GT}$" とある** — $\widehat{GT}$ の**部分群**を切っている ⟹ §0-3 の「方向」と整合。**空席リスクの本命はここ**。 |
| [14] | H. Nakamura and H. Tsunogai, "Harmonic and equianharmonic equations in the Grothendieck-Teichmüller group", **Forum Math. 15 (2003), no. 6, 877–892**. | 具体例($\varphi$ = 調和/等調和)。 |

> 【**文献要請 D-1**】 **[12] Nakamura, "Some classical views on the parameters of the GT group", Progress in Galois Theory**(会議録・Springer Developments in Mathematics 系と推定・**書誌の確定が必要**)。**欲しい形**: (i) new-type relations の一般的定式化(どの $\varphi$ が関係式を与えるかの必要十分条件)(ii) それが**部分群を定義しているか**、定義しているならその群の名前と性質。**なぜ必要か**: $G_{\rm dyn}$ の空席判定の最終決定打。
> 【**文献要請 D-2**】 **[13] Nakamura–Schneps, Invent. Math. 141 (2000)**。**欲しい形**: そこで切られている "a subgroup of $\widehat{GT}$" の定義と、それが「Belyi-extending 族の正規化子」と一致するか。**空席リスクの直撃点。**

### 1(c) 「不変量の共通核」と「正規化子」の数学的差

Wood の構成は $I\mapsto I\circ\varphi_*$、すなわち **dessin 集合上の関数の族**を作る。これが切る対象は
$$\mathcal C:=\{\alpha : \alpha\ \text{が全ての}\ I\circ\varphi_*\ \text{を保つ}\}\qquad(\text{不変量の共通核・}\textbf{条件は軌道の水準}).$$
一方 $G_{\rm dyn}$ が切るのは
$$\mathcal N:=\{\alpha : \alpha\ \text{が族}\ \{(\hat H_\varphi,\psi_\varphi)\}\ \text{を正規化}\}\qquad(\textbf{構造写像の水準}).$$
- **$\mathcal N\subseteq\mathcal C$ は成り立つ**(構造を保てば構造から作った不変量も保つ)。
- **逆は一般に偽**。$\mathcal C$ は「不変量の値が一致」しか要求せず、**$\psi_\varphi$ との intertwining は要求しない**。$I$ が粗ければ($M_\varphi$ は同型類の関数)$\mathcal C$ は巨大になりうる。
- **一致する十分条件**: 不変量の族が dessin を**完全に分離**する(= $\varphi_*$ の軌道が点になる)場合。しかし Wood 自身が §5 で「complete list は理論的理想」と書いており、**現状の $M_\varphi$ 族は分離しない**(§4 の例は逆に「2 軌道を分けた」1 例の報告)。
⟹ **$\mathcal C$ と $\mathcal N$ は別物で、$\mathcal N$(= $G_{\rm dyn}$)の方が真に強い条件。Wood の仕事は $\mathcal N$ の定義には直結しない。**

---

## §2 $G_{\rm dyn}$ の定義起草(主納品)

### 2.1 データ — 仮想自己準同型 $\psi_\varphi$ の構成(自前・完全に明示的)

$U:=\mathbb P^1\setminus\{0,1,\infty\}$、$\hat F_2=\hat\pi_1(U_{\bar{\mathbb Q}},\vec{01})$。$\varphi$ を Belyi-extending とし
$$S_\varphi:=\varphi^{-1}(\{0,1,\infty\})\ \supseteq\ \{0,1,\infty\},\qquad V_\varphi:=\mathbb P^1\setminus S_\varphi\ \subseteq\ U .$$
$\varphi$ は $\{0,1,\infty\}$ の外で不分岐ゆえ **$\varphi:V_\varphi\to U$ は次数 $d=\deg\varphi$ の被覆**。ここから 2 本の射:
$$\varphi_*:\pi_1(V_\varphi)\hookrightarrow\pi_1(U)\ (\text{指数 }d),\qquad \iota_*:\pi_1(V_\varphi)\twoheadrightarrow\pi_1(U)\ (\text{開埋入}).$$
$$\boxed{\ H_\varphi:=\mathrm{im}(\varphi_*)\le F_2\ (\text{指数 }d),\qquad \psi_\varphi:=\iota_*\circ(\varphi_*)^{-1}:H_\varphi\twoheadrightarrow F_2\ }$$
これが**仮想自己準同型**(Nekrashevych の IMG 構成と同一のデータ)。**$\psi_\varphi$ は全射**(∵ $\iota_*$ が全射)。

**Wood の dessin 作用との辞書(自前・要検算だが自明)**: dessin $\Delta\leftrightarrow$ 有限指数 $K\le F_2$(共役類)に対し
$$\boxed{\ \varphi_*(\Delta)\ \leftrightarrow\ \psi_\varphi^{-1}(K)\ },\qquad [F_2:\psi_\varphi^{-1}(K)]=d\cdot[F_2:K]=\deg(\varphi\circ p)\ \checkmark$$
**合成則(反変)**: $\psi_{\varphi\circ\varphi'}=\psi_{\varphi'}\circ\psi_\varphi$(定義域を適切に制限)。∵ $(\varphi\varphi')_*=\varphi_*\circ\varphi'_*$(Wood のモノイド作用)。

**明示例(水準 1 の 2 写像・自前計算)**
- $\varphi=z^n$: $S=\{0,\infty\}\cup\mu_n$。$H_{z^n}=\ker(F_2\to\mathbb Z/n:\ x\mapsto1,\ y\mapsto0)$(指数 $n$・階数 $n+1$)。
 $$\psi_{z^n}(x^n)=x,\qquad \psi_{z^n}(x^kyx^{-k})=\begin{cases}y&k\equiv0\\ 1&k\not\equiv0\end{cases}\pmod n .$$
- $\varphi=4z(1-z)$: 臨界点 $1/2\mapsto1$、$0\mapsto0$、$1\mapsto0$、$\infty\mapsto\infty$。$S=\{0,\tfrac12,1,\infty\}$、$d=2$。$H=\ker(F_2\to\mathbb Z/2:\ x\mapsto0,\ y\mapsto1)$。
 $$\psi(x)=x,\qquad \psi(yxy^{-1})=y,\qquad \psi(y^2)=1 .$$
 (向きの規約 = 定義ノート §1.5 の W-1 に従う。**上の 2 例は本ノートの自前計算で、Wood の "extending pattern" とは独立**。要 cross-check。)

### 2.2 正規化条件の精密形

**族の指定(設計選択 D-a)**: $\mathcal B$ = ℚ 上定義の Belyi-extending 写像**全体**(Wood のクラス)。**この選択では $G_\mathbb{Q}$ は各 $\varphi$ を固定する**(Wood Prop 2 の根拠)ので、**$G_\mathbb{Q}$-軌道の slack は不要**。$\bar{\mathbb Q}$ 上へ拡げる変種は §2.6 で分離して扱う。

$\alpha\in\mathrm{Out}(\hat F_2)$、$\tilde\alpha\in\mathrm{Aut}(\hat F_2)$ をその持ち上げとする。

> ### 定義 D(正規化条件)
> $\alpha\in G_{\rm dyn}^{\rm norm}$ $\iff$ **ある持ち上げ $\tilde\alpha$ が存在して**、任意の $\varphi\in\mathcal B$ に対し **ある $\varphi'\in\mathcal B$ と $g,h\in\hat F_2$** が存在し
> $$\text{(N1)}\quad \tilde\alpha(\hat H_\varphi)=g\,\hat H_{\varphi'}\,g^{-1},\qquad\qquad \text{(N2)}\quad \hat\psi_{\varphi'}\circ\mathrm{inn}(g^{-1})\circ\tilde\alpha\big|_{\hat H_\varphi}\;=\;\mathrm{inn}(h)\circ\tilde\alpha\circ\hat\psi_\varphi .$$
> **中心化版**: $\varphi'=\varphi$ を要求したものを $G_{\rm dyn}^{\rm cent}$ と書く。$G_{\rm dyn}^{\rm cent}\subseteq G_{\rm dyn}^{\rm norm}$。
> **周辺条件**: さらに $\alpha$ が quasi-special(HS 2000 §0.1 の (i):ある $\lambda\in\hat{\mathbb Z}^\times$ で $x,y,z$ の共役類を $\lambda$ 乗に送る)を課した版を $G_{\rm dyn}^{\rm per}$ と書く。

**slack の三源(必記)**
1. **内部 slack**: $\alpha\in\mathrm{Out}$ ゆえ $\tilde\alpha$ は $\mathrm{Inn}$ 分の不定。(N1) の $g$、(N2) の $h$ がこれを吸収する。**$\psi_\varphi$ 自身も基点選択で $\mathrm{Inn}$ 分の不定**なので、条件は最初から「$\mathrm{Inn}$ を法として」書かねばならない(Nekrashevych の仮想自己準同型の標準的同値と同じ)。
2. **$G_\mathbb{Q}$-置換 slack**: 設計選択 D-a(ℚ 有理族)では**不要**。$\bar{\mathbb Q}$ 族に拡げる場合のみ、$\varphi'$ を $\varphi$ の $G_\mathbb{Q}$-軌道内に取る条件が加わる。
3. **合成 slack**: $\mathcal B$ は合成閉なので、(N1)(N2) は**モノイド生成系の上でだけ課せば十分**であってほしい ⟹ 補題 L4(下)。これが成れば定義が有限的に扱える。

### 2.3 well-defined 性 — 必要な補題の列挙(**未証明・candidate**)

| 札 | 言明 | 難度の見立て |
|---|---|---|
| **L1** | $\psi_\varphi$ の $\mathrm{Inn}$ を法とした一意性(基点・path の取り替えに対する不変性) | 低(標準・ただし tangential base point の扱いに §13 型の注意) |
| **L2** | (N1)(N2) が $\tilde\alpha$ の取り替えに依らない(= $\mathrm{Out}$ の水準で well-defined) | 低〜中。$g,h$ の存在量化がこれを吸収するはずだが**要検証** |
| **L3** | $G_{\rm dyn}^{\rm norm}$ が**群**である(積・逆で閉じる) | 中。逆元側で $\varphi\mapsto\varphi'$ の対応が全単射になることが要る ⟹ **$\mathcal B$ 上の置換を誘導する**ことの証明 |
| **L4** | (N1)(N2) はモノイド生成系で判定してよい(合成則 $\psi_{\varphi\varphi'}=\psi_{\varphi'}\circ\psi_\varphi$ からの帰納) | 中。**定義の有限化に必須** |
| **L5** | $\hat H_\varphi$ は $\hat F_2$ の**開**部分群で $\hat\psi_\varphi$ は連続全射(profinite 化の整合) | 低(有限指数ゆえ) |

**⟹ 現状の格 = `candidate(定義は書けたが well-defined 性は L1–L5 未証明)`。** L3 が最重要(群にならなければ対象として失格)。

### 2.4 ★$G_\mathbb{Q}\subseteq G_{\rm dyn}$ の証明(1 段落・**Thurston 剛性は不要**)

$\sigma\in G_\mathbb{Q}$ とする。$\varphi$ は **ℚ 上定義**ゆえ $\sigma$ で固定され、したがって $V_\varphi=\mathbb P^1\setminus\varphi^{-1}(\{0,1,\infty\})$ と被覆 $\varphi:V_\varphi\to U$ は**ℚ 上の射**である。$\hat\pi_1$ の関手性より、$\sigma$ の外作用は $\hat\pi_1(V_\varphi)$ と $\hat F_2$ の双方に定義され、**ℚ-射 $\varphi$ と開埋入 $\iota$ の双方が $G_\mathbb{Q}$-同変**である。ゆえに $\hat H_\varphi=\mathrm{im}(\varphi_*)$ は $\sigma$ で(共役を除いて)保たれ、$\hat\psi_\varphi=\iota_*\circ\varphi_*^{-1}$ は $\sigma$ と(内部自己同型を除いて)可換 — すなわち **(N1)(N2) が $\varphi'=\varphi$ で成立**する。$\varphi$ は任意だったから $\sigma\in G_{\rm dyn}^{\rm cent}$。さらに $G_\mathbb{Q}$ は quasi-special(HS §0.1 (i)・Belyi)なので $\sigma\in G_{\rm dyn}^{\rm per}$。∎
**格 = paper-proof(L1/L5 相対・基点の扱いは要 Sol 監査)。** これは Wood Prop 2 を $\pi_1$ 水準へ持ち上げただけで、**力学系的剛性は一切使っていない**。
> ⚠ **司令塔覚書への訂正**: 「Thurston 剛性経由」は不要です。剛性が要るのは、族 $\mathcal B$ を **ℚ-有理性ではなく力学的性質(PCF)で内在的に特徴づけたい**場合、あるいは $\bar{\mathbb Q}$ 族で $\varphi'$ の一意性を言いたい場合です。**この区別は定義の格に直結する**ので明記しました。

### 2.5 写像クラスの同定(記録)

Belyi-extending $\iff$ 「臨界値 $\subseteq\{0,1,\infty\}$」∧「$\varphi(\{0,1,\infty\})\subseteq\{0,1,\infty\}$」$\iff$ **post-critical set $P_\varphi\subseteq\{0,1,\infty\}$**(前方軌道が閉じるため)$\iff$ **$P_\varphi$ が 3 点以下の PCF 写像**、これに **ℚ 上定義**が付く。⟹ **$G_{\rm dyn}$ 構想の写像クラスと Wood のクラスは厳密に同一。**

### 2.6 $\widehat{GT}$ との関係(現状整理)

- $\widehat{GT}$ は $S_3$ 対称性(HS 2000 Prop 3/4/7: (I)(II)(III) $\iff$ $(12),(123),(14253)$ との可換性)で切られる。$G_{\rm dyn}$ は**力学的構造写像**で切られる。**両者の条件は互いに他を含意しない ⟹ 比較不能。**
- **方向の決定的な証拠**: Wood §1 逐語 —「Belyi-extending maps can be used to get relations (called "new-type" relations) **on the image of this injection**」= $G_\mathbb{Q}\hookrightarrow\widehat{GT}$ の**像**に対する追加関係式。⟹ **new-type relations は $\widehat{GT}$ を削る**。⟹ **$\widehat{GT}\subseteq G_{\rm dyn}$ は期待できない**(そうなら関係式は無内容)。[13] のタイトル "a **subgroup** of the Grothendieck-Teichmüller group" もこれを支持。
- ⟹ **正しい絵**:
$$G_\mathbb{Q}\ \subseteq\ \widehat{GT}\cap G_{\rm dyn}^{\rm per}\ \subseteq\ \widehat{GT}$$
**問い**: 右の包含は真か(= 力学条件で井原の隙間が縮むか)。**これは井原予想の精密化であり、$G_{\rm dyn}$ の存在理由そのもの。**
- **どの包含も非自明**: $G_\mathbb{Q}\subsetneq\widehat{GT}\cap G_{\rm dyn}$ か(未知)/ $\widehat{GT}\cap G_{\rm dyn}\subsetneq\widehat{GT}$ か(= new-type relations が非自明か。[12][13][14] が**具体例で肯定**していると読める ⟹ **おそらく真の包含**・要 pin)。

---

## §3 水準 1 実験の仕様骨子

### 3.1 有限窓での力学両立テスト

窓 $N\in NFI_{PB_3}(B_3)$、$G:=F_2/N_{F_2}$。shadow $[m,f]$ の誘導自己準同型 $\phi_{m,f}:x\mapsto x^{u},\ y\mapsto f^{-1}y^{u}f$($u=2m+1$)。

> **ゲート G-1(定義可能性)**: $N_{F_2}\subseteq H_\varphi$。指数 $d$ の $H_\varphi$ に対しこれは「$G^{\rm ab}$ が $\mathbb Z/d$ 商をもつ」と同値。
> **ゲート G-2(level 条件)**: $\psi_\varphi(N_{F_2}\cap H_\varphi)\subseteq N_{F_2}$。これが成れば $\bar\psi_\varphi: H_\varphi/N_{F_2}\to G$ が定義される。**verbal 窓($\gamma_kF_2^\ell$)では自動**。
> **判定式(有限)**: $\ \bar\psi_\varphi\circ\bar\phi_{m,f}\big|_{H_\varphi/N_{F_2}}\ =\ \mathrm{inn}(\bar h)\circ\bar\phi_{m,f}\circ\bar\psi_\varphi\quad(\exists\bar h\in G)$。
> **出力**: 通過集合 $\mathrm{DYN}_\varphi(N)\subseteq GT(N)$。

**$z^n$ の場合の展開(手計算で判定式が閉じる)**: $\phi(x^n)=x^{nu}$ ゆえ $\psi(\phi(x^n))=x^{u}=\phi(\psi(x^n))$ ✓ **自動**。非自明なのは $y$ 側だけで
$$\boxed{\ \bar\psi_{z^n}\bigl(\bar f^{-1}\bar y^{u}\bar f\bigr)\ \overset{?}{=}\ \bar h^{-1}\,\bar f^{-1}\bar y^{u}\bar f\,\bar h\ \ \text{in } G\ }$$
— **$f$ に関する 1 本の方程式**。これが new-type relation の有限窓版である。

### 3.2 既存アトラスに掛けたときの予想

| アトラス | $G^{\rm ab}$ | $z^2$(G-1) | $z^3$(G-1) | $z^7$(G-1) |
|---|---|---|---|---|
| **83 窓**(48 元) | $C_3$ | **✗ 退化**(2 商なし) | **✓** | ✗ |
| **972 窓**(972 元) | $C_2^2$ | **✓** | ✗(3 商なし) | ✗ |
| **NW(7)**(294/42) | $(\mathbb Z/7)^2$ | ✗ | ✗ | **✓**(かつ verbal ⟹ G-2 自動) |

⟹ **$4z(1-z)$($d=2$)は 972 窓でのみ定義可能・$z^2$ も同じ・$z^3$ は 83 窓向け・NW(7) は $z^7$ で verbal の恩恵。** 3 アトラスが**きれいに棲み分ける**のは設計上の朗報です。

**★測れるもの(これが本命)**: $G_\mathbb{Q}\subseteq G_{\rm dyn}$(§2.4)より
$$\mathrm{Im}(\mathrm{Ih}_N)\ \subseteq\ \bigcap_{\varphi}\mathrm{DYN}_\varphi(N)$$
⟹ **算術像の計算可能な上界**。工房は現在、算術像の上界を $GT(N)$ 自身(自明)と survival/pentagon(高価・深度相対)でしか持っていない。**これは新種の、しかも安い上界**である。
**予想 P-DYN-1(事前登録候補)**: 972 窓で $\bigcap_\varphi\mathrm{DYN}_\varphi \subsetneq X_{972}$(= 上界が 972 を真に切る)。**もし $=324$ が出れば $A$ の独立同定になり、$c'$ の 1 ビットが力学側から決まる**(LOCAL-3 の完全な独立検算)。
**予想 P-DYN-2**: 83 窓で $\mathrm{DYN}_{z^3}$ は $\mathrm{Im}(\mathrm{Ih}_N)\supseteq C_2\times C_3$(定理 C3-LIFT)を含み、22 候補のいくつかを落とす。

### 3.3 実装上の注記

- **GAP の FR / IMG パッケージ**(Nekrashevych の仮想自己準同型・IMG を扱う)が使える可能性がある — **要棚卸し**(本ノートは実行しない)。
- 語の向きは **規約 W-1/W-2 厳守**($c\notin N$ 窓では語水準評価)。$\psi_\varphi$ は $F_2$ の**部分群上の**準同型なので、Schreier 生成系での表示を先に固定すること。
- **破壊対照**: $\psi$ を故意に別の $\varphi$ のものに差し替えて判定が反転すること。**陽性対照**: 単位 shadow と複素共役 $[u=-1]$ が必ず通ること($G_\mathbb{Q}$ の元だから)。

---

## §4 未決・要請

1. 【**D-1**】[12] Nakamura(書誌確定+一般論の射程)— **空席判定の決定打**。
2. 【**D-2**】[13] Nakamura–Schneps Invent. Math. 141 の "a subgroup of $\widehat{GT}$" の定義 — **空席リスクの直撃点**。
3. **L1–L5**(§2.3)の証明。とくに **L3(群であること)** が失格判定の分かれ目。
4. §2.1 の 2 例($z^n$・$4z(1-z)$)の $\psi$ は**本ノートの自前計算・単系統**。Wood の "extending pattern" 経由の独立再計算で cross-check すること。
5. **novelty**: §1(a) の判定(Wood は群を定義していない)は Wood 本文に基づく。[12][13] 未読のため **novelty は主張しない** — D-1/D-2 の返り待ち。
