# TB 引用化 3 枚束 **v2.1** — 便 103 F103-4 の条件履行(追記型・v2 不改変)

**状態札: `candidate(引用化起草・紙のみ / Lean 検証ではない / cross-checked でもない / 封印非接触 / novelty 主張なし)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05
- **v1 = `docs/notes/tb_citation_bundle_v1.md`(凍結)・v2 = `docs/notes/tb_citation_bundle_v2.md`(凍結・本 v2.1 は 1 バイトも改変していない)**
- **v2.1 = 便 103 `sol/sol_reply_103_math30.md` §4(F103-4)の 4 条件の履行**(追記型・CV-10 additive erratum 方式)

> ## ⚠ 読み方
> **v2 の §3.2(transport 不要の理由)・§3.3 補題 EXSEQ (a) の証明・§5 RD-6′(iii) は、本 v2.1 の §1〜§3 を経ずに引用してはならない。**
> v2 のそれ以外(§1 会計の撤回・§2 の 4 ブロック表・§3.1・§3.4 SPLIT・§4 TB1-FF′・§5.2 TB4-GEN′・§6・§7・§8・§9)は**有効**。ただし **§2 のブロック ② 表と §7 の 2 行は §3.4 / §4.4 の更新版で読む**。

---

## 0. 便 103 §4 の受領

| 項 | Sol | 本 v2.1 |
|---|---|---|
| **裁定** | **(5′) を `theorem-framework-relative [TB: canonical-source-pinned/v2]` として条件付き PASS**。【GAP-TB-EXACT】の旧 source mismatch は**この格で閉じる**。**ただし `canonical-source-relative` / `verified` とは書かない** | §5 で札文言を確定 |
| **回答 1** | transport は不要。**ただし理由を修正**(IX Th. 6.1 自体は幾何基点を使う) | ★ **§3(修理 C)** |
| **回答 2** | reader exercise 2 件は `canonical-source-pinned` には**十分**。**極限段は工房補題として責任を引き受けること** | ★ **§4(修理 D)** |
| **回答 3** | EXSEQ (a) に Hensel/valuation は不要 | ★ **§2(修理 B)** |
| **文言修理 1** | RD-6′ は「compatible roots of unity の取り直し = generator identification を $\hat{\mathbf Z}^\times$ で変える」と「compatible Puiseux roots の取り直し = $\hat{\mathbf Z}(1)$-torsor」を**分離**せよ。**両者をともに $\hat{\mathbf Z}^\times$ とする説明は誤り** | ★ **§1(修理 A)** |
| **文言修理 2** | 不要な Hensel/valuation 説明を削れ | §2 |

---

## 1. 【修理 A】RD-6′(iii) の分離 — **二つの取り直しは別物である**

### 1.1 ★ 自認(v2 の誤り)

> **v2 §5 RD-6′(iii) の逐語**:
> 「$(\beta^{1/n})_n$ を別の整合系 $(\zeta_n\beta^{1/n})_n$ に取り替えると $\mathrm{im}(\iota)$ の位相的生成元は変わるが、閉部分群 $\mathrm{im}(\iota)=\overline{\langle x\rangle}$ は変わらない。**理由**: $\mathrm{im}(\iota)$ は procyclic であり、取り替えは $\hat{\mathbf Z}^\times$ の元による生成元の付け替えにすぎない。」

$$\boxed{\ \textbf{★ この「理由」は二重に誤りである。撤回する。}\ }$$

1. **群が違う**: compatible Puiseux roots の取り直しを支配するのは $\hat{\mathbf Z}^\times$ ではなく **$\hat{\mathbf Z}(1)=\varprojlim\mu_n$** である(§1.2)。
2. **効果が違う**: Puiseux 系の取り直しは **$\mathrm{im}(\iota)$ の生成元を「付け替えない」**($\chi$ が不変・§1.2 (i))。生成元の付け替え($\hat{\mathbf Z}^\times$ 作用)を起こすのは **$(\zeta_n)$ の取り直し**の方である(§1.3)。

⟹ **v2 は二つの取り直しを 1 つに潰し、しかも間違った方の記述を当てていた。** ただし ★ **「閉部分群 $\mathrm{im}(\iota)=\overline{\langle x\rangle}$ は変わらない」という結論は両方の取り直しについて正しく、(TB4ᵘ) と補題 TB4-GEN′ は無傷である**(便 103「閉 inertia subgroup の結論は変わらない」)。

### 1.2 **RD-6′(iii-a)** — compatible Puiseux roots の取り直しは $\hat{\mathbf Z}(1)$-torsor

記号: $\Omega=\bar{\mathbf Q}\{\{\beta\}\}$、$I_0=\mathrm{Gal}(\Omega/\bar{\mathbf Q}((\beta)))$。$\Omega$ を $\bigcup_n\bar{\mathbf Q}((\beta^{1/n}))$ と書くには、**整合系** $\mathbf b=(b_n)_n$($b_n\in\Omega$, $b_n^n=\beta$, $b_{mn}^m=b_n$)を 1 つ選ぶ必要がある。

> **条文 (iii-a).**
> **(1)(torsor)** $\beta$ の整合的 Puiseux 系の全体 $\mathcal B$ は、$\hat{\mathbf Z}(1)=\varprojlim_n\mu_n$ の**単純推移的作用**
> $$\eta\cdot\mathbf b:=(\eta_n b_n)_n\qquad(\eta=(\eta_n)\in\hat{\mathbf Z}(1))$$
> をもつ **$\hat{\mathbf Z}(1)$-torsor** である。**($\hat{\mathbf Z}^\times$-作用ではない。)**
> **(2)($\chi$ の不変性)** 各 $\mathbf b\in\mathcal B$ が定める同型
> $$\chi^{\mathbf b}:I_0\xrightarrow{\ \sim\ }\hat{\mathbf Z}(1),\qquad \chi^{\mathbf b}_n(\sigma):=\sigma(b_n)/b_n$$
> は **$\mathbf b$ に依らない**。
> **(3)(splitting への効果)** (TB2) の分裂 $s_{\vec{01}}^{\mathbf b}$($\tilde\gamma$ = $\bar{\mathbf Q}$ 上 $\gamma$・すべての $b_n$ を固定)は $\mathbf b$ に**依る**: $\mathbf b'=\eta\cdot\mathbf b$ に対し
> $$s^{\mathbf b'}_{\vec{01}}(\gamma)=\iota(\eta)\,s^{\mathbf b}_{\vec{01}}(\gamma)\,\iota(\eta)^{-1}\qquad(\forall\gamma\in G_K),$$
> すなわち **$\mathrm{im}(\iota)$ の元による共役**(1-コサイクルの境界)だけずれる。
> **(4)(結論)** $\mathrm{im}(\iota)$ は可換なので (3) の共役は $\mathrm{im}(\iota)$ を**各点固定**する。⟹ **$\mathrm{im}(\iota)=\overline{\langle x\rangle}$ は不変**、かつ $\hat F_2=\pi_1(U_{\bar{\mathbf Q}},\vec{01})$ も部分群として不変。

**証明.**
**(1)** $\mathbf b,\mathbf b'\in\mathcal B$ に対し $\eta_n:=b'_n/b_n$ は $\eta_n^n=1$ かつ $\eta_{mn}^m=b'^m_{mn}/b^m_{mn}=b'_n/b_n=\eta_n$、ゆえに $\eta\in\hat{\mathbf Z}(1)$ で $\mathbf b'=\eta\cdot\mathbf b$。逆に $\eta\cdot\mathbf b\in\mathcal B$ は明らか。作用が自由なのは $\eta_n b_n=b_n\Rightarrow\eta_n=1$ から。
**(2)** $\sigma\in I_0$ は $\bar{\mathbf Q}\subset\bar{\mathbf Q}((\beta))$ を各点固定するので $\sigma(\eta_n)=\eta_n$。ゆえに
$$\chi^{\eta\cdot\mathbf b}_n(\sigma)=\frac{\sigma(\eta_nb_n)}{\eta_nb_n}=\frac{\eta_n\,\sigma(b_n)}{\eta_nb_n}=\chi^{\mathbf b}_n(\sigma).$$
**(3)** $\tilde\gamma^{\mathbf b'}$ は $b'_n=\eta_nb_n$ を固定するので $\tilde\gamma^{\mathbf b'}(b_n)=\gamma(\eta_n)^{-1}\eta_n b_n$。ゆえに $\tilde\gamma^{\mathbf b'}\circ(\tilde\gamma^{\mathbf b})^{-1}$ は $\bar{\mathbf Q}$ 上恒等で $b_n\mapsto(\eta_n/\gamma(\eta_n))b_n$、すなわち $\chi^{\mathbf b}$ の下で $\eta\cdot\gamma(\eta)^{-1}\in\hat{\mathbf Z}(1)$ に対応する $I_0$ の元。$\gamma$ の $\hat{\mathbf Z}(1)$ への作用は $s^{\mathbf b}_{\vec{01}}(\gamma)$ による共役と一致するので、これは $\iota(\eta)\,s^{\mathbf b}(\gamma)\,\iota(\eta)^{-1}s^{\mathbf b}(\gamma)^{-1}$ に等しい。移項して (3)。
**(4)** $\mathrm{im}(\iota)\cong\hat{\mathbf Z}(1)$ は可換ゆえ $\iota(\eta)$ による共役は $\mathrm{im}(\iota)$ 上恒等。∎

### 1.3 **RD-6′(iii-b)** — compatible roots of unity の取り直しは $\hat{\mathbf Z}^\times$ で generator identification を変える

> **条文 (iii-b).**
> **(1)** (TB2) が固定する整合系 $(\zeta_n)_n$($\zeta_{mn}^m=\zeta_n$、各 $\zeta_n$ 原始的)は、$\hat{\mathbf Z}(1)$ の**位相的生成元**にほかならない。その全体は **$\hat{\mathbf Z}^\times$-torsor** である($(\zeta_n)\mapsto(\zeta_n^t)$, $t\in\hat{\mathbf Z}^\times$)。
> **(2)** $\sigma_\zeta\in I_0$ を $\chi(\sigma_\zeta)=(\zeta_n)$ で定めると、$(\zeta_n)\rightsquigarrow(\zeta_n^t)$ は $\sigma_\zeta\rightsquigarrow\sigma_\zeta^{\,t}$ を与える。⟹ **これが「generator identification を $\hat{\mathbf Z}^\times$ で変える」の内容である。**
> **(3)** $\sigma_\zeta$ は §1.2 (2) により **Puiseux 系 $\mathbf b$ に依らない**(定義が $\chi$ だけを使うため)。
> **(4)** $\overline{\langle\sigma_\zeta\rangle}=\mathrm{im}(\iota)$ は $t$ に依らない($\hat{\mathbf Z}^\times$ は位相的生成元を位相的生成元へ写す)。⟹ **閉部分群の結論は不変。**

> ### ⚠ $\varepsilon$ について本 v2.1 が主張しないこと
> BFC (2.1) の $\varepsilon$($x=\iota(\sigma_\zeta^{\,\varepsilon})$)への影響は **本 v2.1 の射程外**である。正本は **BFC v2 §2 の (2.1)/(2.1′) と三量 $b_{\rm cmp}/b_{\rm op}/\hat b_i$** であり、供給元は **`Z-norm-seal/v1` + retained TB4-3/A3 framework**。**本 v2.1 はこれらを一切変更しない**(RD-6′(iv) 不変・$\varepsilon$ は seal-relative のまま)。

### 1.4 RD-6′(i)(ii)(iv) は不変

v2 §5 の (i)(Deligne 流との同一性を主張しない)・(ii)(Deligne §15 の役割を ④-2/④-3 に限定)・(iv)(三つの exact generator の canonical 同一視を主張しない・$\varepsilon$ は seal-relative)は**そのまま有効**。**差し替えたのは (iii) のみ**((iii-a)+(iii-b) の 2 条へ分離)。

---

## 2. 【修理 B】補題 EXSEQ (a) の証明 — 付値・Hensel を削除

### 2.1 ★ 削除する記述(v2 §3.3 の逐語)

> ~~「$\bar{\mathbf Q}$ は $\Omega$ の中で代数閉($\Omega$ の付値 $v$ は $\bar{\mathbf Q}$ 上自明・剰余体 $\bar{\mathbf Q}$ ゆえ、$\bar{\mathbf Q}$ 上代数的な $\xi\in\Omega$ は $v(\xi)=0$ で剰余が $\bar{\mathbf Q}$、Hensel の逐次近似で $\xi\in\bar{\mathbf Q}$)」~~

★ **不要かつ迂遠であった。自認。** 付値も Hensel も一切要らない。

### 2.2 差し替え(**補題 EXSEQ (a) の証明・訂正版**)

> **補題 EXSEQ (a)**(主張は v2 §3.3 のまま). $\Phi:(\text{有限エタール}/\mathrm{Spec}\,K)\to\mathcal C_K$, $\mathrm{Spec}\,L\mapsto U_L$ に対し $\mathrm{Fib}_{\vec{01}}\circ\Phi\cong F_{\bar{\mathbf Q}}$。
>
> **証明(訂正版).**
> $$\mathrm{Fib}_{\vec{01}}(U_L)=\mathrm{Hom}_{K((\beta))\text{-alg}}\bigl(L\otimes_KK((\beta)),\ \Omega\bigr)=\mathrm{Hom}_{K\text{-alg}}(L,\Omega).$$
> $L/K$ は有限次で $K\subseteq\bar{\mathbf Q}$ ゆえ、$L$ の各元は $\mathbf Q$ 上代数的である。したがって $K$-代数準同型 $f:L\to\Omega$ の像の各元は $\Omega$ の中で $\mathbf Q$ 上、とくに $\bar{\mathbf Q}$ 上代数的である。**固定した $\bar{\mathbf Q}\subset\Omega$ は $\mathbf Q$ の代数閉包(とくに代数閉体)である**から、$\bar{\mathbf Q}$ 上代数的な $\xi\in\Omega$ の $\bar{\mathbf Q}$ 上の最小多項式は $\bar{\mathbf Q}[T]$ で 1 次式に分解し、ゆえに $\xi\in\bar{\mathbf Q}$。よって $f(L)\subseteq\bar{\mathbf Q}$、すなわち
> $$\mathrm{Hom}_{K\text{-alg}}(L,\Omega)=\mathrm{Hom}_{K\text{-alg}}(L,\bar{\mathbf Q})=F_{\bar{\mathbf Q}}(\mathrm{Spec}\,L).$$
> 関手性は明らか。∎

**(b)(c) は v2 §3.3 のまま**(ただし (c) は §4 の補題群で書き直す)。

---

## 3. 【修理 C】「transport 不要」の**理由**の書き直し

### 3.1 ★ 撤回する構造説明(v2 §3.2 の逐語)

> ~~「★ 6.13 は「幾何点」を一度も要求しない — 「基本関手 $F$ と $a\in F(S)$」だけである。⟹ **接基点への transport は不要**である。**SGA 1 IX 6.1 の証明が実際に使う道具**が、最初から基本関手一般で述べられているからである。」~~

$$\boxed{\ \textbf{★ 結論(transport 不要)は正しいが、この理由づけは誤りである。撤回する。}\ }$$

**何が誤りか**: **SGA 1 Exp. IX Th. 6.1 は幾何学的基点 $\bar a$ を用いて述べられた定理である**(v2 §3.1 の逐語がまさにそう書いている)。「その証明が使う道具が base-point-free だから定理が base-point-free に読める」というのは、**定理の主張文と証明の道具を混ぜた論法**であり、正しくない。定理の主張文をそのまま $\mathrm{Fib}_{\vec{01}}$ に適用することはできない。

### 3.2 ★ 正しい構造(便 103 F103-4-1 の指定形)

$$\boxed{\ \begin{aligned} &\textbf{(i) 名前 pin}: &&\textbf{SGA 1 Exp. IX Th. 6.1}\ \text{が「この形の完全列が成り立つ」という既知の定理である}\\ &&&\text{(ただし\textbf{幾何基点版}であり、工房の基点にそのまま適用はしない)}\\[2pt] &\textbf{(ii) 実働 pin}: &&\textbf{SGA 1 Exp. V Prop. 6.13}\ \text{が}\ \textbf{基本関手 }F\ \text{と}\ a\in F(S)\ \text{だけを要求する}\\ &&&\text{(= base-point-free の材料はここにある)}\\[2pt] &\textbf{(iii) 工房の仕事}: &&\textbf{補題 EXSEQ が }F=\mathrm{Fib}_{\vec{01}}\ \text{について}\ \textbf{IX Th. 6.1 の証明手順を再走する}\\ &&&\text{(有限ガロア段で V 6.13}\ \to\ \text{射影極限)}\\[4pt] &\Longrightarrow &&\textbf{Deligne 流基点と Ihara 流基点(あるいは幾何基点と接基点)の}\\ &&&\textbf{比較 transport を別途要求しない。} \end{aligned}\ }$$

★ **依存の重心の移動**: この構造では、**ブロック ② の数学的な重みは V Prop. 6.13 + 工房補題 EXSEQ にある**。**IX Th. 6.1 は「同型の主張が文献に既知として存在すること」を示す名前 pin**である。⟹ **v2 §2 のブロック ② 表を §3.4 で更新する。**

### 3.3 ★ この訂正が **RD-6′(i) の convention route と整合する理由**(1 行)

convention route(工房は Ihara/Puiseux presentation を規約として採用し、Deligne 流との同一性を主張しない)を採ると、**そもそも「基点間の比較 transport」を作る義務が消える**。§3.2 (iii) はその上で「では完全列はどう得るのか」に答えるもので、**答えは「工房が IX の証明を自分の基本関手で再走する」**である。**両者は同じ方針の表と裏**であり、v2 §3.2 の誤った理由づけは、この整合を「文献側が既にやってくれている」と読み違えたものである。

### 3.4 ★ ブロック ② の pin 表(**v2 §2 の当該表を差し替える**)

| # | 内容 | 種別 | pin / 補題 | `proof_body_status` |
|---|---|---|---|---|
| ②-1 | 完全列 $1\to\pi_1(\overline X_0,\bar a)\to\pi_1(X,a)\to\pi_1(S,b)\to1$ が**既知の定理として存在する**(**幾何基点版**) | **P(名前 pin)** | **SGA 1 Exp. IX Th. 6.1**(PDF 211 / 新頁 195 / 旧 LNM 253・150 dpi 画像✓) | **present**。⚠ 証明中に reader_exercise 1 件(§4.3) |
| ②-2 | ★ **実働**: Galois 圏 $\mathcal C$・**基本関手 $F$**・連結対象 $S$・$a\in F(S)$ に対する開部分群同定 | ★ **P(実働 pin)** | ★★ **SGA 1 Exp. V Prop. 6.13**(PDF 130 / 新頁 114 / 旧 139–140・150 dpi 画像✓)— **幾何点を要求しない** | ★ **omitted / reader_exercise**(「La démonstration est laissée au lecteur.」)⟹ **§4.2 で工房が引き受ける** |
| ②-3 | 底 $\mathrm{Spec}\,K$ への射 $p$ の存在 | **L** | **補題 EXSEQ (a)(b)**(証明は §2.2 で訂正) | — |
| ②-4 | ★ **IX の証明手順の再走**(有限ガロア段 → 射影極限) | ★ **L(責任引受)** | **補題 EXSEQ-STAB**(§4.2・**証明つき**)+ **補題 EXSEQ-LIM**(§4.3・**証明骨子つき**) | — |
| ②-5 | 接基点 splitting | **L + C** | **補題 SPLIT**(v2 §3.4・不変)+ **(TB2)** | — |

---

## 4. 【修理 D】reader_exercise 2 件の**責任引受**

> **便 103 F103-4-2 逐語**: 「reader exercise 2 件は **`canonical-source-pinned` の札には十分**。ただし canonical-source-relative や verified への昇格根拠ではない。**極限段は工房補題として責任を引き受けること。**」

### 4.1 引き受けの宣言

$$\boxed{\ \textbf{工房は次の 2 件を「SGA 1 がそう書いているから」ではなく、\textbf{工房補題として}引き受ける。}\ }$$

| # | 元の reader_exercise | 引き受け先 | 本 v2.1 での状態 |
|---|---|---|---|
| **RE-1** | **SGA 1 V Prop. 6.13** 全体(「La démonstration est laissée au lecteur.」) | ★ **補題 EXSEQ-STAB**(我々が使う特殊形) | ★ **証明を書いた**(§4.2) |
| **RE-2** | **SGA 1 IX Th. 6.1** 証明中の極限段(「On laisse au lecteur le soin de vérifier que $\pi_1(\overline X_0,\bar a)\to\varprojlim\pi_1(X_i,a_i)$ est un isomorphisme」) | ★ **補題 EXSEQ-LIM** | ★ **証明骨子を書いた**(§4.3)。**未閉の 1 点を明示**(§4.3 末) |

### 4.2 ★ 補題 **EXSEQ-STAB**(RE-1 の引受・**証明つき**)

> **補題 EXSEQ-STAB.** $\pi:=\pi_1(U_K,\vec{01})=\mathrm{Aut}(\mathrm{Fib}_{\vec{01}})$ とし、$S$ を $\mathcal C_K$ の連結対象、$a\in\mathrm{Fib}_{\vec{01}}(S)$、$U:=\mathrm{Stab}_\pi(a)$ と置く。$\mathcal C_K/S$($S$ 上の対象の圏)の繊維関手を
> $$F'(X'):=\bigl(\text{$\mathrm{Fib}_{\vec{01}}(X')\to\mathrm{Fib}_{\vec{01}}(S)$ による $a$ の逆像}\bigr)$$
> とすると、$\mathrm{Aut}(F')\xrightarrow{\ \sim\ }U$(開部分群)。
>
> **証明.** ブロック ①(SGA 1 V Th. 4.1 / §7 / Prop. 6.1・工房補題 TB1-FF′)により、$\mathrm{Fib}_{\vec{01}}$ は $\mathcal C_K$ を**有限連続 $\pi$-集合の圏**へ同値に写し、$\mathrm{Fib}_{\vec{01}}$ 自身は忘却関手に対応する。以下この同一視の下で議論する。
> $S$ は連結なので $\pi$ は $\mathrm{Fib}_{\vec{01}}(S)$ に推移的に作用し(V 5.3)、$\mathrm{Fib}_{\vec{01}}(S)\cong\pi/U$($a\leftrightarrow eU$)。$U$ は有限集合の点の固定部分群ゆえ開。
> **$\pi$-集合の圏で $\pi/U$ 上の対象の圏は、$U$-集合の圏に同値である**:
> $$E\longmapsto E_0:=(\text{$E\to\pi/U$ による $eU$ の逆像}),\qquad E_0\longmapsto \pi\times^U E_0:=(\pi\times E_0)/U$$
> が互いに擬逆(標準的な誘導・制限の随伴。$E\cong\pi\times^UE_0$ は $E$ の各点 $e$ を $(g,g^{-1}e)$ で表すことによる — $g$ は $e$ の像 $gU$ の代表)。
> この同値の下で $F'$ は $U$-集合の忘却関手に対応する。ゆえに $\mathrm{Aut}(F')=\mathrm{Aut}(\text{$U$-集合の忘却関手})=U$。∎
>
> ★ **格**: 紙・初等・**単系統**・Sol 監査未。**SGA 1 が読者に委ねた段を、我々が使う形で工房が書いた**ものである(SGA 1 の一般形 6.13 全体を証明したとは主張しない)。

### 4.3 ★ 補題 **EXSEQ-LIM**(RE-2 の引受・**証明骨子つき**)

記号: $K_i$ は $K$ の有限ガロア部分拡大で $\bar{\mathbf Q}=\bigcup_iK_i$、$U_{K_i}=U\times_{\mathrm{Spec}\,K}\mathrm{Spec}\,K_i$。

> **補題 EXSEQ-LIM.** 自然な射 $\pi_1(U_{\bar{\mathbf Q}},\vec{01})\to\varprojlim_i\pi_1(U_{K_i},F'_i)$ は同型。同値な言い換え: **$U_{\bar{\mathbf Q}}$ の任意の有限エタール被覆はある $U_{K_i}$ 上の有限エタール被覆から来て、その descent は $K_j\supseteq K_i$ を取り直す差を除き一意**。
>
> **証明(骨子・$U$ が曲線であることを使う).** char 0。連結被覆に帰着してよい。
> **(存在)** $U_{\bar{\mathbf Q}}$ の連結有限エタール被覆は、$\bar{\mathbf Q}(\beta)$ の有限次分離拡大 $M$ で、$U_{\bar{\mathbf Q}}$ の $M$ における正規化が $U_{\bar{\mathbf Q}}$ 上エタールになるもの、と 1:1 に対応する。$M=\bar{\mathbf Q}(\beta)[T]/(g)$ と書くと $g$ の係数は有限個で、それらに現れる $\bar{\mathbf Q}$ の元も有限個ゆえ、ある $K_i$ に含まれる。$M_i:=K_i(\beta)[T]/(g)$ と置けば $M_i\otimes_{K_i}\bar{\mathbf Q}\cong M$(必要なら $K_i$ を大きくして $g$ の $K_i(\beta)$ 上の既約性を確保)。$V_i:=$($U_{K_i}$ の $M_i$ における正規化)と置く。char 0 ゆえ $\bar{\mathbf Q}/K_i$ は分離的で、正規化は底の分離拡大と可換なので $V_i\times_{K_i}\bar{\mathbf Q}$ は $U_{\bar{\mathbf Q}}$ の $M$ における正規化。$V_i\to U_{K_i}$ は有限平坦で、**非エタール軌跡は $U_{K_i}$ の閉集合**であり、その $\bar{\mathbf Q}$ への底変換が空(仮定)ゆえ**空**。したがって $V_i\to U_{K_i}$ はエタール。
> **(一意性)** $V_i,V'_i$ の底変換が $U_{\bar{\mathbf Q}}$ 上同型なら、その同型は有限個の係数で定まるのである $K_j\supseteq K_i$ 上で定義され、$V_i\times K_j\cong V'_i\times K_j$。
> **(同型への翻訳)** 以上により制限関手 $\varinjlim_i(\text{有限エタール}/U_{K_i})\to(\text{有限エタール}/U_{\bar{\mathbf Q}})$ は圏同値。繊維関手は両側で $\mathrm{Fib}_{\vec{01}}$(§4.2 の $F'_i$)と両立するので、$\mathrm{Aut}$ を取って主張を得る。∎
>
> ### ⚠ 未閉の 1 点(**隠さず申告**)
> 上の (存在) で使った「**char 0 において正規化は底体の分離拡大と可換**」と「**有限平坦射の非エタール軌跡が閉である**」の 2 つは、私は**標準事実として使っており、本束で証明も文献 pin もしていない**。⟹ **`omitted`(工房債務)**。EGA IV の該当箇所で閉じる型だが、**私は EGA IV を 1 頁も開いていない**(v2 §9-4 の申告と同じ)。
> ★ **したがって EXSEQ-LIM は「工房が責任を引き受けた補題」であって「工房が完全に証明した補題」ではない。** この区別を札に書く(§5)。

### 4.4 `proof_body_status` 一覧の更新(**v2 §7 の 2 行を差し替え**)

| pin / 補題 | v2 の値 | ★ **v2.1 の値** |
|---|---|---|
| SGA 1 V Prop. 6.13 | omitted / reader_exercise | ★ **omitted / reader_exercise(文献側)+ 工房が EXSEQ-STAB として引受・§4.2 で証明済** |
| SGA 1 IX Th. 6.1 | present(内部に reader_exercise 1 件) | ★ **present(名前 pin)+ 極限段は工房が EXSEQ-LIM として引受・§4.3 で骨子提示(内部に工房債務 2 件)** |

**他の行は v2 §7 のまま。**

---

## 5. 格の確定文(**便 103 の条件付き PASS を受けて**)

### 5.1 ★ 書いてよい文 / 書いてはならない文

> **★ 書いてよい**:
> ```text
> (5′) = theorem-framework-relative [TB: canonical-source-pinned/v2]
>        (条件付き PASS・便 103 F103-4 / 条件履行 = tb_citation_bundle_v2_1.md)
> 【GAP-TB-EXACT】= 閉(旧 source mismatch は上記の格で閉じる)
> ```
> **★ 書いてはならない**(便 103 逐語):
> ```text
> ~~canonical-source-relative~~   ~~verified~~   ~~unconditional~~
> ```

### 5.2 札文言(**v2 §8.1 (N-1′)(N-2′)(N-3′) への追記行**)

> **(N-1″)** ASM §V.2.4 TB 行 — v2 §8.1 の block に次の 4 行を**追記**:
> ```text
> ブロック②の構造(v2.1 §3.2 で訂正):
>      IX Th.6.1 = 名前 pin(幾何基点版・そのままは適用しない)
>      V Prop.6.13 = 実働 pin(基本関手 F と a∈F(S) のみ要求)
>      工房 EXSEQ が Fib_01→ について IX の証明手順を再走する
>      ⟹ 基点間の比較 transport は別途要求しない
> reader_exercise 2 件の引受(v2.1 §4):
>      RE-1 (V 6.13)  -> 工房補題 EXSEQ-STAB(証明済・単系統)
>      RE-2 (IX 極限段) -> 工房補題 EXSEQ-LIM(骨子・工房債務 2 件を内包)
>      ⟹ canonical-source-pinned には十分 / relative・verified の根拠にはしない
> 規約 RD-6′(iii) は 2 条へ分離(v2.1 §1):
>      (iii-a) compatible Puiseux roots の取り直し = Ẑ(1)-torsor
>              χ: I_0 ≅ Ẑ(1) は不変・splitting は im(ι) 共役だけずれる
>      (iii-b) compatible roots of unity の取り直し = Ẑ^× で generator identification を変える
>      両者とも im(ι) = closure⟨x⟩ は不変(TB4ᵘ / TB4-GEN′ は無傷)
> ```
> **(N-2″)** CLAIMS W3-17 の追記行を `canonical-source-pinned v2`(条件履行 = v2.1)へ同期。**exact TB4・$(Z_{2M}$-link$)$ の欄は不変。**
> **(N-3″)** P97-1.1 層 3 の札は v2 §8.1 (N-3′) のまま。

### 5.3 工房債務の最終一覧(**7 本**)

| # | 債務 | 状態 |
|---|---|---|
| **L-1** | TB1-FF′(繊維関手性・$j^*$ の完全性) | v2 §4・証明済・単系統 |
| **L-2** | TB4-INJ($\iota$ 単射) | v1 §4.3・証明済・**F102-7.1 で成立確認** |
| **L-3** | TB4-GEN′($\mathrm{im}(\iota)=\overline{\langle x\rangle}$・**閉部分群としてのみ**) | v2 §5.2・証明済・**F102-7.1 で成立確認** |
| **L-4** | EXSEQ (a)(b) | ★ **v2.1 §2.2 で証明を訂正**(付値・Hensel 削除) |
| **L-5** | SPLIT(接基点 splitting) | v2 §3.4・証明済・単系統 |
| **L-6** | ★ **EXSEQ-STAB**(RE-1 引受) | ★ **v2.1 §4.2・証明済・単系統** |
| **L-7** | ★ **EXSEQ-LIM**(RE-2 引受) | ★ **v2.1 §4.3・骨子のみ・工房債務 2 件(正規化の底変換・非エタール軌跡の閉性)を内包** |

---

## 6. v2 の該当箇所への差し替え索引(**CV-10 erratum**)

| v2 の箇所 | 処置 | v2.1 の差し替え先 |
|---|---|---|
| §5 RD-6′ **(iii)** | ★ **撤回・分離** | §1.2(iii-a)+ §1.3(iii-b) |
| §3.3 補題 EXSEQ (a) の**証明**(付値・Hensel の段) | ★ **削除・差し替え** | §2.2 |
| §3.2 の**理由づけ**(「IX の証明が base-point-free だから」) | ★ **撤回・書き直し** | §3.2 |
| §2 ブロック ② の表 | ★ **差し替え** | §3.4 |
| §7 の V 6.13 行・IX 6.1 行 | ★ **差し替え** | §4.4 |
| §8.2 の格請求文 | ★ **確定** | §5.1・§5.2 |
| **上記以外(§1 会計撤回・§2 の ①③④ 表・§3.1・§3.4 SPLIT・§4・§5.1(i)(ii)(iv)・§5.2・§6・§9・§10)** | **不変** | — |

---

## 7. 本 v2.1 が**主張しないこと**

1. 「**(5′) が無条件になった / `canonical-source-relative` になった / `verified` になった**」— ★ **いずれも主張しない**(便 103 の明示禁止)。到達したのは **`theorem-framework-relative [TB: canonical-source-pinned/v2]`** である。
2. 「**SGA 1 V Prop. 6.13 の一般形を証明した**」— **主張しない**。証明したのは**我々が使う特殊形(EXSEQ-STAB)**のみ。
3. 「**EXSEQ-LIM を完全に証明した**」— ★ **主張しない**(§4.3 末の未閉 2 点)。
4. 「**Deligne 流と Ihara 流の接基点が同一である**」— **主張しない**(RD-6′(i)・不変)。
5. 「**$\varepsilon$ / exact (TB4) / $(Z_{2M}$-link$)$ について何かが変わった**」— **主張しない**(§1.3 末の box)。
6. 「**SGA 1 / EGA IV を通読した**」— **主張しない**。開いたのは SGA 1 Exp. V §4–§7(PDF 120・126・130・131)と Exp. IX §6(PDF 211)のみ。**EGA IV は 1 頁も開いていない。**
7. `cross-checked` / `verified` — **付さない**(機械計算ゼロ・Lean 未使用)。**novelty** — 主張しない。
8. $K^{(5)}$ の値・窓データ・$\hat c_\mu$・PSL 封印欄・$\varepsilon$ bits・$u$ 値 — **一切触れていない**。
