# (TB1)/(TB4ᵘ)/(TB3) 引用化 3 枚束 **v2** — 4 ブロック依存表・【GAP-TB-EXACT】の頁画像 pin・会計の数え直し

**状態札: `candidate(引用化起草・紙のみ / Lean 検証ではない / cross-checked でもない / 封印非接触 / novelty 主張なし)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05
- **v1 = `docs/notes/tb_citation_bundle_v1.md`(凍結・1 バイトも改変しない)**
- **v2 = 便 102 §7 の履行**(`sol/sol_reply_102_math29.md` **F102-7.1 / F102-7.2 / F102-7.3**)+ 司令塔追加委嘱
- **新規に開いた原典**: `papers/sga1-grothendieck-raynaud-arxiv0206203.pdf`(SGA 1・SMF 再組版版・**頁対応: 新頁 = PDF − 16**・margin の数字は旧 LNM 224 の頁)

> ## ⚠ 読み方(**v1 を単独で引用しないこと**)
> **v1 §0 の「真の外部依存は 2 箇所」・§6.5 の会計・§7.3 の格請求は、本 v2 §1 の撤回を経ずに引用してはならない。**
> v1 の **§2(RD-1〜RD-5)・§3(TB1 条項判定)・§4(TB4ᵘ 条項判定)・§5(TB3 条項判定)・§10(読解係への訂正)** は本 v2 でも有効。**§2 の RD-6 のみ RD-6′ へ全面差し替え**(§5)、**§6.5 の会計と §7 の格案は §2・§8 へ差し替え**。

---

## 0. 便 102 §7 の受領(3 項)

| 項 | Sol の判定 | 本 v2 の処置 |
|---|---|---|
| **F102-7.1** | 引用画像と局所補題は **PASS**(Deligne §10.16–10.20 / §15.13–15.23 / §16.1、Ihara §2.3 の転記は正確。**TB1-FF・TB4-INJ 成立**、**TB4-GEN は RD-2 の向き非依存な閉部分群としてなら成立**) | ★ 受領。TB4-GEN の主張文を「**閉部分群としての一致**」に限定して条文化(§5.2) |
| **F102-7.2** | **S-1 は convention route(方式 (ii))を採択**。compatible roots の変更は procyclic inertia 内で生成元を変えるが**閉部分群は変えない**。三つの exact generator の canonical 同一視は主張せず、$\varepsilon$ は seal-relative のまま。(16.1.1) の motivic 記述は必須でなく名前/説明 pin。p.255 の "small positive loop" は文脈上 (16.1.2) を指し**致命的曖昧性ではない**が、**compatible-root 系との exact 同定はこの一文からは出ない** | ★ **RD-6′ として条文化**(§5)。**S-4 は格下げして記録**(§6) |
| **F102-7.3** | **(5′) 昇格は HOLD**。理由 =【GAP-TB-EXACT】は実在の欠品 + **「外部依存 2 箇所」は literal に偽**(Ihara の geometric $\hat F_2$/inertia marking と未 pin の完全列を数えていない)+ `canonical-source-pinned` の格も明示的未 pin と両立しない。**4 ブロックを依存表に出し各々 pin か工房補題にせよ** | ★ **§1(撤回と数え直し)・§2(4 ブロック依存表)・§3(② の頁画像 pin)・§8(格案 v2)** |

---

## 1. ★ 会計の撤回と数え直し(**自認**)

### 1.1 撤回

> **v1 §0 の逐語**: 「**(5′) 証明鎖が真に外部文献を要する箇所は 2 つ** = Deligne §10.16(圏同値)+ Deligne §15.23 PREUVE / 14.2(局所 $\pi_1=\hat{\mathbf Z}(1)$)」
> **v1 §6.5 の表**: 「[C-1] / [C-2] 外部文献 2 行」

$$\boxed{\ \textbf{★ 撤回する。この会計は literal に偽であった。}\ }$$

**何を数え落としたか(2 件)**:

1. **Ihara ICM §2.3 の geometric $\hat F_2$ / $0,1,\infty$ inertia marking**。v1 は §6.1 の表で「$\hat F_2$ 部分 → Ihara ICM §2.3」と**書いておきながら**、直後の「外部依存 2 箇所」の数え上げから**落とした**。表と会計文が自分の中で食い違っていた。
2. **未 pin の同所性完全列**(【GAP-TB-EXACT】)。v1 は §6.4 でこれを**自分で新設して申告しながら**、「外部依存 2 箇所」の文には反映しなかった。⟹ **同一文書内で、申告した欠品を会計から除外していた。**

★ **誤りの型**: 「(TB1)(TB4ᵘ) の pin を数える」つもりの会計を、「(5′) 鎖全体の外部依存を数える」文として書いた。**射程の取り違えであり、私の責である。**

### 1.2 ★ 数え直し(4 ブロック・**便 102 指定の分割**)

$$\boxed{\ \textbf{(5}'\textbf{) 証明鎖の真の外部依存} = \mathbf{4}\ \textbf{ブロック / 文献 } \mathbf{3}\ \textbf{本(SGA 1・Deligne 1989・Ihara ICM 1990)}\ +\ \textbf{工房補題 } \mathbf{5}\ \textbf{本}\ +\ \textbf{工房規約 } \mathbf{2}\ \textbf{本}\ }$$

---

## 2. ★ 4 ブロック依存表(**各々 pin または工房補題**)

> 記法: **P** = 文献 pin(§/定理番号 + 頁画像照合)/ **L** = 工房補題(初等・本束が証明を書く)/ **C** = 工房規約。
> `proof_body_status` は CV-10 §1.5 の三値 + `omission_kind`。

### ブロック ① — Galois category / fiber functor equivalence

| # | 内容 | 種別 | pin / 補題 | `proof_body_status` |
|---|---|---|---|---|
| ①-1 | Galois 圏 $\mathcal C$ と基本関手 $F$ に対し $F$ が $\mathcal C\simeq\mathcal C(\pi)$($\pi=\mathrm{Aut}(F)$)を与える | **P** | **SGA 1 Exp. V, Th. 4.1**(+ §5)。「foncteur fondamental」の定義もここ(**PDF 120 / 新頁 104**・索引 "foncteur fondamental, 104" と一致) | present |
| ①-2 | 前層スキームの場合: 幾何点 $a$ に対する $F$ が (G1)–(G6) を満たし $\pi_1(S,a):=\mathrm{Aut}(F)$ | **P** | **SGA 1 Exp. V, §7「Cas des préschémas」**(**PDF 131 / 新頁 115**)。逐語「Les propriétés (G 1) à (G 6) sont satisfaites … Le foncteur $F$ définit alors une équivalence de la catégorie $\mathcal C$ avec la catégorie des ensembles finis où $\pi=\pi_1(S,a)$ opère continûment」 | present(公理検証は V 3.4/3.5/3.7・I 4.6 へ委譲) |
| ①-3 | ★ **$\mathrm{Fib}_{\vec{01}}$ が基本関手である** | ★ **P**(v1 では L のみ) | ★★ **SGA 1 Exp. V, Prop. 6.1**(**PDF 126 / 新頁 110**・**150 dpi 画像照合済**)逐語: 「Soient $\mathcal C,\mathcal C'$ deux catégories galoisiennes, $H:\mathcal C\to\mathcal C'$ un foncteur covariant, $F'$ un foncteur fondamental sur $\mathcal C'$ et $F=F'\circ H$. Conditions équivalentes: (i) $H$ est exact … (iii) **$F$ est un foncteur fondamental sur $\mathcal C$**.」 | present |
| ①-4 | $H=j^*$(底変換 $\mathrm{Spec}\,k((\beta))\to U$)が完全であること | **L** | **補題 TB1-FF′**(§4) | — |
| ①-5 | 副有限側の言明(工房の語彙での再掲・**名前 pin**) | **P** | **Deligne 10.16**(`external_reference`「SGA 3 V 7」)+ 10.16 末尾(任意の繊維関手で $\pi_1(X,F)^\wedge=\mathrm{Aut}(F)$) | external_reference |

★ **v1 からの改善**: v1 は ①-3 を「番号つき pin なし ⟹ 工房補題」と判定したが、**SGA 1 V Prop 6.1 が逐語で与える**。**v1 §3.2 の「不一致」判定は ①-3 について解消**(合成関手の完全性 ①-4 だけが工房側に残る)。

### ブロック ② — arithmetic homotopy exact sequence + 接基点 splitting

| # | 内容 | 種別 | pin / 補題 | `proof_body_status` |
|---|---|---|---|---|
| ②-1 | ★ **完全列** $1\to\pi_1(\bar X_0,\bar a)\to\pi_1(X,a)\to\pi_1(S,b)\to1$、$\pi_1(S,b)=\mathrm{Gal}(\bar k/k)$ | ★ **P** | ★★ **SGA 1 Exp. IX, Th. 6.1**(**PDF 211 / 新頁 195 / 旧 LNM 253**・**150 dpi 画像照合済**・逐語 §3.1) | **present**・ただし ⚠ 証明中に **reader_exercise 1 件**(§7) |
| ②-2 | ★ **その機構が基本関手一般で回る**(= 幾何点でなく $\mathrm{Fib}_{\vec{01}}$ でよい) | ★ **P** | ★★ **SGA 1 Exp. V, Prop. 6.13**(**PDF 130 / 新頁 114 / 旧 139–140**・**150 dpi 画像照合済**)— **「$\mathcal C$ une catégorie galoisienne munie d'un foncteur fondamental $F$」で述べられており幾何点を要求しない**(逐語 §3.2) | ★ **omitted / reader_exercise**(逐語「**La démonstration est laissée au lecteur.**」) |
| ②-3 | 底 $\mathrm{Spec}\,K$ への射の存在($\mathrm{Fib}_{\vec{01}}$ の $\mathrm{Spec}\,K$ 上への制限が標準繊維関手) | **L** | **補題 EXSEQ (a)(b)**(§3.3) | — |
| ②-4 | 有限段 → 極限の組み立て | **L** | **補題 EXSEQ (c)**(§3.3)。⚠ 極限段は SGA 1 IX 6.1 の reader_exercise と同じ内容 | — |
| ②-5 | ★ **接基点 splitting** $s_{\vec{01}}:G_K\to\pi_1(U_K,\vec{01})$ | **L + C** | **補題 SPLIT**(§3.4)+ **(TB2)**(工房規約) | — |

★ **v1 の【GAP-TB-EXACT】は本 v2 で pin された**(②-1 + ②-2 の頁画像 + 工房補題 2 本)。**便 102 の「未 pin」指摘は解消。**

### ブロック ③ — geometric $\hat F_2$ と $0,1,\infty$ の inertia marking

| # | 内容 | 種別 | pin / 補題 | `proof_body_status` |
|---|---|---|---|---|
| ③-1 | $\pi_1(U_{\bar{\mathbf Q}},\vec{01})\cong\hat F_2$(階数 2 副有限自由) | **P** | **Ihara ICM 1990 §2.3**(印字 106「This group is free on $x,y$」/「$\hat\pi_1(X(\mathbf C),\vec{01})=\hat F_2$」・印字 103 の $\hat\pi_1$ 記述と GRET)経由 **RD-1** | ★ **omitted / silent_omission** |
| ③-2 | $x,y$ が $0,1$ の慣性生成元(基点 $\vec{01}$) | **P** | 同 印字 105–106($p$・$x$・$x'$・$y=p^{-1}x'p$)経由 **RD-2** | present(構成) |
| ③-3 | $z=(xy)^{-1}$ が $\infty$ の慣性生成元 | ★ **P(弱)** | 同 印字 106 Remark の**括弧書き 1 語** "(a loop around ∞)" | ★ **omitted / silent_omission** |
| ③-4 | 接基点の presentation | **C** | ★ **RD-6′**(convention route・§5) | — |

★ **これが v1 の会計から落ちていた第 1 の項目**(§1.1-1)。**③-3 は (5′) 鎖では非 load-bearing**(v1 §5.3・不変)。

### ブロック ④ — local Kummer / restriction comparison $\hat{\mathbf Z}(1)$

| # | 内容 | 種別 | pin / 補題 | `proof_body_status` |
|---|---|---|---|---|
| ④-1 | $I_0=\mathrm{Gal}(\Omega/\bar{\mathbf Q}((\beta)))\cong\hat{\mathbf Z}(1)$ | **P** | **Deligne 15.23 PREUVE**(「$\pi_1(X)=\pi_1(X_s^\wedge)=\hat{\mathbf Z}(1)$」)+ **14.2**(ℓ-adique 実現) | present + external_reference(Abhyankar) |
| ④-2 | graded 模型 $T_s^0=\mathrm{Spec}\,\mathrm{Gr}(K)$ と完備化模型 $\mathrm{Spec}\,k((\beta))$ の橋 | **P** | **Deligne 15.20**(完備化不変性)+ **15.21** + **15.22** + **15.23 LEMME**(**RD-4**) | present |
| ④-3 | canonical な射 $\iota$ の**命名**(制限関手が誘導する標準射) | **P(名前 pin)** | **Deligne (16.1.1)**。★ **便 102 F102-7.2 により「必須でなく名前/説明 pin」と確定** ⟹ 依存の重みは ④-2 に移る | present |
| ④-4 | $\iota$ の単射性 | **L** | **補題 TB4-INJ**(v1 §4.3・**F102-7.1 で成立確認**) | — |
| ④-5 | $\mathrm{im}(\iota)=\overline{\langle x\rangle}$(**閉部分群としての一致**) | **L + C** | **補題 TB4-GEN′**(§5.2)+ **RD-2 / RD-6′** | — |
| ④-6 | 後合成 = 左作用 | **C** | $\mathrm{Fib}$ の定義の tautology(v1 §4.4・不変) | — |
| ④-7 | 局所 Kummer 表示 (7.1)(7.2) | — | **TB 非依存**(完備化・Eisenstein・$\Omega$ の根・(TB2) の係数作用) | — |

---

## 3. ★ ブロック ② の pin 本体

### 3.1 SGA 1 Exp. IX, Théorème 6.1(**150 dpi 頁画像照合済・PDF 211 / 新頁 195 / 旧 LNM 253**)

> 「**Théorème 6.1.** — Soient $S$ le spectre d'un anneau artinien $A$ de corps résiduel $k$, $\bar k$ une clôture algébrique de $k$, $X$ un $S$ préschéma, $X_0=X\otimes_Ak$, $\overline X_0=X\otimes_A\bar k$, $\bar a$ un point géométrique de $\overline X$, $a$ son image dans $X$, $b$ son image dans $S$. On suppose que $X_0$ est quasi-compact et géométriquement connexe sur $k$ (…). Alors la suite d'homomorphismes canoniques
> $$e\longrightarrow\pi_1(\overline X_0,\bar a)\longrightarrow\pi_1(X,a)\longrightarrow\pi_1(S,b)\longrightarrow e$$
> est exacte, et on a $\pi_1(S,b)\xleftarrow{\ \sim\ }\pi_1(k,\bar k)=$ groupe de Galois de $\bar k$ sur $k$.」

**工房の設定への適用**: $A=k=K$(数体)、$S=\mathrm{Spec}\,K$、$X=U_K$、$X_0=U_K$、$\overline X_0=U_{\bar{\mathbf Q}}$。$U_K$ は $K$ 上幾何的連結($U_{\bar{\mathbf Q}}=\mathbf P^1_{\bar{\mathbf Q}}-\{0,1,\infty\}$ 連結)・quasi-compact ✓。

⚠ **literal な射程**: 6.1 は**幾何点 $\bar a$** で述べられている。工房の基点は接基点(= 基本関手 $\mathrm{Fib}_{\vec{01}}$)である。⟹ **§3.2 が要る。**

### 3.2 ★ SGA 1 Exp. V, Proposition 6.13 —**機構は基本関手一般で回る**(**150 dpi 画像照合済・PDF 130 / 新頁 114**)

> 「**Proposition 6.13.** — Soient $\mathcal C$ **une catégorie galoisienne munie d'un foncteur fondamental $F$**, $S$ un objet connexe de $\mathcal C$, $\mathcal C'$ la catégorie des objets de $\mathcal C$ au-dessus de $S$. Alors $\mathcal C'$ est une catégorie galoisienne, et le foncteur $X\mapsto H(X)=X\times S$ de $\mathcal C$ dans $\mathcal C'$ est exact. **Soit $a\in F(S)$**, et soit $F'$ le foncteur de $\mathcal C'$ dans la catégorie des ensembles finis défini par
> $$F'(X')=\text{image inverse de }a\text{ par }F(X')\longrightarrow F(S).$$
> Alors on a un isomorphisme $F\cong F'\circ H$, et l'homomorphisme correspondant $u:\pi_{F'}\to\pi_F$ **est un isomorphisme de $\pi_{F'}$ sur le sous-groupe ouvert $U$ de $\pi_F$ stabilisateur de l'élément marqué $a$ de $F(X)$**.
> **La démonstration est laissée au lecteur.**」

$$\boxed{\ \textbf{★ 6.13 は「幾何点」を一度も要求しない — 「基本関手 }F\textbf{ と }a\in F(S)\textbf{」だけである。}\ }$$

⟹ **接基点への transport は不要**である。SGA 1 IX 6.1 の証明が実際に使う道具(逐語「Il résulte donc de **V 6.13** que l'on a une suite exacte $e\to\pi_1(X_i,a_i)\to\pi_1(X,a)\to\Gamma_i\to e$」)が、最初から基本関手一般で述べられているからである。

⚠ **`proof_body_status = omitted / omission_kind = reader_exercise`**(逐語「La démonstration est laissée au lecteur.」)。**隠さず記帳する。**

### 3.3 工房補題 **EXSEQ**(**債務 4/5**)

記号は v1 §3.3 と同じ。$K\subseteq\bar{\mathbf Q}$ 有限次、$\mathcal C_K:=$($U_K$ 上の有限エタール被覆)、$F:=\mathrm{Fib}_{\vec{01}}$(①-3 により基本関手)。$K_i$ を $K$ の有限ガロア部分拡大($\bar{\mathbf Q}=\bigcup K_i$)、$\Gamma_i:=\mathrm{Gal}(K_i/K)$、$U_{K_i}:=U\times_{\mathrm{Spec}\,K}\mathrm{Spec}\,K_i$。

> **補題 EXSEQ.**
> **(a)** $\Phi:(\text{有限エタール}/\mathrm{Spec}\,K)\to\mathcal C_K$, $\mathrm{Spec}\,L\mapsto U_L$ に対し $F\circ\Phi\cong F_{\bar{\mathbf Q}}$(= $\mathrm{Spec}\,K$ の幾何点 $\mathrm{Spec}\,\bar{\mathbf Q}$ での標準繊維関手)。
> **(b)** ゆえに canonical な連続準同型 $p:\pi_1(U_K,\vec{01})=\mathrm{Aut}(F)\to\mathrm{Aut}(F_{\bar{\mathbf Q}})=G_K$ がある。
> **(c)** $1\to\pi_1(U_{\bar{\mathbf Q}},\vec{01})\to\pi_1(U_K,\vec{01})\xrightarrow{\ p\ }G_K\to1$ は完全。

**証明.**
**(a)** $F(U_L)=\mathrm{Hom}_{K((\beta))\text{-alg}}(L\otimes_KK((\beta)),\Omega)=\mathrm{Hom}_{K\text{-alg}}(L,\Omega)$。$L/K$ は有限次ゆえ像は $\Omega$ の中の $\bar{\mathbf Q}$ 上代数的な元からなり、**$\bar{\mathbf Q}$ は $\Omega$ の中で代数閉**($\Omega$ の付値 $v$ は $\bar{\mathbf Q}$ 上自明・剰余体 $\bar{\mathbf Q}$ ゆえ、$\bar{\mathbf Q}$ 上代数的な $\xi\in\Omega$ は $v(\xi)=0$ で剰余が $\bar{\mathbf Q}$、Hensel の逐次近似で $\xi\in\bar{\mathbf Q}$)。ゆえに $=\mathrm{Hom}_{K\text{-alg}}(L,\bar{\mathbf Q})=F_{\bar{\mathbf Q}}(\mathrm{Spec}\,L)$。関手性は明らか。
**(b)** (a) と関手性(SGA 1 V Prop. 6.11 の枠組み)から。
**(c)** 各 $i$ で $U_{K_i}$ は $\mathcal C_K$ の**連結**対象($U_{\bar{\mathbf Q}}$ 連結ゆえ)で、$\Gamma_i^{\rm opp}$ の下で principal homogeneous(体の側でそうであり、$\Phi$ が充満忠実 — SGA 1 IX 3.4)。$a_i\in F(U_{K_i})=\mathrm{Hom}_K(K_i,\bar{\mathbf Q})\ne\emptyset$ を取り **V 6.13** を適用すると、$\pi_1(U_{K_i},F'_i)\xrightarrow{\sim}\mathrm{Stab}_{\pi_1(U_K,\vec{01})}(a_i)$(開部分群)。$U_{K_i}$ 連結ゆえ作用は推移的(V 5.3)で、principal homogeneous より単純推移 ⟹
$$1\to\pi_1(U_{K_i},F'_i)\to\pi_1(U_K,\vec{01})\to\Gamma_i\to1\quad\text{完全}.$$
$i$ について射影極限を取る(型ガロア群の圏では完全性が保たれる)と (c) を得る。∎
> ⚠ **極限段の申告**: 「$\pi_1(U_{\bar{\mathbf Q}},\vec{01})\xrightarrow{\sim}\varprojlim_i\pi_1(U_{K_i},F'_i)$」(= $U_{\bar{\mathbf Q}}$ の有限エタール被覆はある $U_{K_i}$ から来る)は、**SGA 1 IX 6.1 の証明が逐語「On laisse au lecteur le soin de vérifier」と書いている段**である。**私も本束では証明を書いていない**(EGA IV §8 の極限論で閉じる型だが、**私は EGA IV を 1 頁も開いていない**)。⟹ **`omitted / reader_exercise` として §7 に登録。**

### 3.4 工房補題 **SPLIT**(**債務 5/5**)— 接基点 splitting

> **補題 SPLIT.** $\gamma\in G_K$ に対し、$\bar{\mathbf Q}$ 上 $\gamma$ と一致し**すべての $\beta^{1/n}$ を固定する** $\Omega$ の体自己同型 $\tilde\gamma$ が一意に存在する。$s(\gamma):=(\text{$\tilde\gamma$ の後合成})$ は $\mathrm{Aut}(F)$ の元で、$s:G_K\to\pi_1(U_K,\vec{01})$ は $p$ の連続切断である。
> **証明.** $\Omega=\bigcup_n\bar{\mathbf Q}((\beta^{1/n}))$ の各段で係数ごとに $\gamma$ を作用させ $\beta^{1/n}$ を固定すれば体同型が定まり、$(\beta^{1/mn})^m=\beta^{1/n}$ と整合するので $n$ について両立し $\tilde\gamma$ が一意に定まる。$\gamma\in G_K$ は $K$ を固定するので $\tilde\gamma|_{K((\beta))}=\mathrm{id}$、ゆえに $f\mapsto\tilde\gamma\circ f$ は $F(W)=\mathrm{Hom}_{K((\beta))}(A_W,\Omega)$ の自己同型を与え、$W$ について自然。$\Omega$ 上の合成が群作用ゆえ $s$ は準同型で連続。EXSEQ (a) の同定の下で $p(s(\gamma))=\tilde\gamma|_{\bar{\mathbf Q}}=\gamma$。∎
> ⟹ $\pi_1(U_K,\vec{01})=\pi_1(U_{\bar{\mathbf Q}},\vec{01})\rtimes_\alpha G_K$、すなわち **BFC §6.2 冒頭の $\hat F_2\rtimes_\alpha G_K$ が正当化される**((TB3) = ③-1 と併せて)。
> ★ **これが (TB2) の内容の全部である** — (TB2) は「分裂を与える」と述べるが、**分裂される完全列の存在は ②-1/②-2 が供給する**(便 102 F102-7.3 の指摘どおり)。

---

## 4. 工房補題 **TB1-FF′**(v1 §3.3 の (c) を SGA 1 V 6.1 経由へ差し替え)

v1 §3.3 の **(a)(b) は不変**(F102-7.1 で成立確認)。**(c) を次で置き換える**:

> **(c′)** $H:=j^*:\mathcal C_k\to\mathcal C_{k((\beta))}$(底変換)は**完全**である。ゆえに **SGA 1 V Prop. 6.1 (i)⇒(iii)** により $\mathrm{Fib}_{\vec{01}}=F_\Omega\circ j^*$ は $\mathcal C_k$ の**基本関手**である。
> **証明((c′) の完全性のみ).** 底変換は有限極限(ファイバー積)と有限余積(disjoint union)を保つ。有限エタール被覆の射のうち Galois 圏の epi = 全射であり、全射性は底変換で保たれる。最後に「非始対象を非始対象へ送る」: $W\ne\emptyset$ なら $j$ が $U$ の生成点を hit する(v1 §3.3 (c) の単射性 $k[\beta,\beta^{-1},(\beta-1)^{-1}]\hookrightarrow k((\beta))$)ので $W\times_U\mathrm{Spec}\,k((\beta))\ne\emptyset$。⟹ V 6.1 (ii) が成立し、(iii) を得る。∎
> ★ **v1 は保存性を正規性 + 生成ファイバーで手証明していた。V 6.1 を使えばその段は不要**(基本関手であることから保存性が従う)。**v1 の証明は誤りではないが冗長であった。**

---

## 5. ★ **RD-6′** — 接基点の convention route(**便 102 F102-7.2 の採択を条文化**)

> ### **RD-6′(規約・v1 の RD-6 を全面差し替え)**
> **工房は接基点 $\vec{01}$ の presentation として Ihara/Puiseux 版を規約として採用する。** すなわち
> $$\mathrm{Fib}_{\vec{01}}(W):=\mathrm{Hom}_{k((\beta))\text{-alg}}\bigl(\mathcal O(W\times_U\mathrm{Spec}\,k((\beta))),\ \Omega\bigr),\qquad \Omega=\bar{\mathbf Q}\{\{\beta\}\}$$
> **をもって $\vec{01}$ の定義とする**(Ihara ICM 印字 105 の branch = 「$\bar Y$ の $P$ での局所環の Puiseux 級数環への局所埋め込み」と、BFC 補題 B-5a の分解 $\prod_P\kappa(P)((s_P))$ を経由して**逐語同一**)。
>
> **(i) 主張しないこと**: **Deligne 流の $T_s^0$ 経由の提示との同一性は主張しない。** v1 §2 の RD-6 が抱えた「証明本文がどちらの文献にもない」という翻訳債務は、**同一性を主張しないことで消える**(便 102 F102-7.2「方式 (ii)、工房が Ihara/Puiseux presentation を規約として採用するのが最小」)。
> **(ii) Deligne §15 の役割の限定**: 本規約の下で Deligne §15 は **④-2(graded ↔ 完備化の橋・RD-4)と ④-3((16.1.1) の名前 pin)** にのみ使う。**(TB1) には使わない**(ブロック ① は SGA 1 V が供給する)。
> **(iii) ★ compatible roots の取り替えに対する不変性**(便 102 F102-7.2 逐語の条文化):
> $$\boxed{\ (\beta^{1/n})_n\ \text{を別の整合系}\ (\zeta_n\beta^{1/n})_n\ \text{に取り替えると}\ \mathrm{im}(\iota)\ \textbf{の位相的生成元は変わるが、閉部分群}\ \mathrm{im}(\iota)=\overline{\langle x\rangle}\ \textbf{は変わらない}\ }$$
> **理由**: $\mathrm{im}(\iota)$ は procyclic であり、取り替えは $\hat{\mathbf Z}^\times$ の元による生成元の付け替えにすぎない。$\hat{\mathbf Z}^\times$ の元は $\hat{\mathbf Z}$ の位相的生成元を位相的生成元へ写す。⟹ **(TB4ᵘ) が要求する subgroup statement は本規約だけで得られる。**
> **(iv) ★ 主張しないこと(再掲・重要)**: **三つの exact generator($x$ / $\sigma_\zeta$ / Ihara の「正の実根」branch)を canonical に同一視したとは言わない。符号 $\varepsilon$ は seal-relative のまま残る**(現行の供給元 `Z-norm-seal/v1` + retained TB4-3/A3 framework は本束によって**一切変更されない**)。

### 5.2 補題 **TB4-GEN′**(F102-7.1 の限定を反映)

> **補題 TB4-GEN′.** RD-2(接基点のもとで「$0$ の慣性部分群」$:=\mathrm{im}(\iota)$)と RD-6′(iii)の下で、**閉部分群として**
> $$\mathrm{im}(\iota)=\overline{\langle x\rangle}.$$
> **証明.** TB4-INJ より $\mathrm{im}(\iota)\cong\hat{\mathbf Z}(1)$ は procyclic。③-2 により $x$ は接基点 $\vec{01}$ における $0$ のまわりの(位相的)ループとして $\mathrm{im}(\iota)$ の位相的生成元である。procyclic 群の位相的生成元が生成する閉部分群は全体。∎
> ★ **主張は閉部分群の一致に限る。生成元の一致・向き・$\varepsilon$ は一切主張しない**(F102-7.1「TB4-GEN は RD2 の向き非依存な**閉部分群**としてなら成立」)。
> ★ **v1 §4.3 が TB4-GEN の根拠に挙げた 3 本のうち (iii)(位相側 (15.10.1)/15.9 の引用)は、閉部分群版では不要になる** — 必要なのは「$x\in\mathrm{im}(\iota)$ かつ位相的生成元」だけで、これは ③-2 + RD-2 で足りる。⟹ **RD-3 の例外(Betti 番号を引く唯一の箇所)は消滅**。**v1 §4.3 の (iii) は撤回する。**

---

## 6. S-4(Betti 正規化文の水準)— **Sol 裁定の受領と格下げ**

| | v1 の記述 | ★ **v2 の記述** |
|---|---|---|
| **事実** | 「En réalisation de Betti, $\mu_s$ envoie le générateur $2\pi i$ …」の直前の定義は (16.1.3)($H_1$ 水準)であり、$\mu_s$ は (16.1.2) と (16.1.3) の両方の名前 | **同じ**(150 dpi 画像・事実は動かない) |
| **判定** | 「**exact (TB4)/$\varepsilon$ を引用で閉じようとするなら最初の障害**」 | ★ **格下げ**。便 102 F102-7.2: 「文脈上 (16.1.2) の $\pi_1$ 写像を指し、次の "En homologie" が (16.1.3) へ移るので、**そこ自体を致命的曖昧性とは判定しない**」 |
| **★ 残る内容** | — | ★ 便 102 逐語: 「**ただし workshop の compatible-root 系との exact 同定はこの一文だけからは出ない**」⟹ **S-4 の値打ちは「曖昧性の指摘」ではなく「この一文は $\varepsilon$ を供給しない」という射程の確認**に移る。**RD-6′(iv) と同じ結論。** |

---

## 7. `proof_body_status` 一覧(**CV-10 §1.5・全 pin 分**)

| pin | 値 | `omission_kind` / 備考 |
|---|---|---|
| SGA 1 V Th. 4.1 / §7 | **present** | 公理検証は V 3.4/3.5/3.7・I 4.6 へ委譲(内部参照) |
| ★ **SGA 1 V Prop. 6.1** | **present** | 画像照合済 |
| ★ **SGA 1 V Prop. 6.13** | ★ **omitted** | **`reader_exercise`**・`source_wording` = 「**La démonstration est laissée au lecteur.**」(画像照合済) |
| ★ **SGA 1 IX Th. 6.1** | **present** | ⚠ 証明中に **`reader_exercise` 1 件**: 「On laisse au lecteur le soin de vérifier que l'homomorphisme naturel $\pi_1(\overline X_0,\bar a)\to\varprojlim\pi_1(X_i,a_i)$ est un isomorphisme」 |
| Deligne 10.16 | **external_reference** | 原本表記「SGA 3 V 7」/「SGA 3 V 5.7」— **正誤判断はしない**(v1 §3.1 と同じ) |
| Deligne 15.20/15.21/15.22/15.23 LEMME/15.16/15.17 | **present** | 15.23 PREUVE は Abhyankar が `external_reference` |
| Deligne (16.1.1)(16.1.2) | **present** | ★ 名前/説明 pin へ降格(F102-7.2) |
| Ihara ICM ③-1 | **omitted** | `silent_omission`(自由性の証明本文なし) |
| Ihara ICM ③-2 | **present** | 構成 |
| Ihara ICM ③-3 | **omitted** | `silent_omission`(括弧書き 1 語)・**(5′) 鎖では非 load-bearing** |

> ### ★ 本 v2 で新たに露出した `reader_exercise` が **2 件**ある
> **ブロック ② の pin は「present な定理」ではあるが、その内部に 2 件の reader_exercise を含む。** ⟹ **格の請求文にこれを書く**(§8)。**「pin した = 証明本文が全部ある」ではない。**

---

## 8. 格の更新案 **v2**(**発効は Sol 検収後**)

### 8.1 v1 §7.2 の 3 案を差し替える

> #### **(N-1′)** ASM §V.2.4 の **TB1–TB4 行**
> ```text
> 格:  framework assumption
>      — TB1 / TB3 / TB4^u は canonical-source-pinned (v2, 4 ブロック)
>      (exact TB4 と Z_{2M}-link は本 pin の射程外・現行の供給元のまま)
> ブロック①(Galois category / fiber functor):
>      SGA 1 Exp. V Th.4.1・§7(PDF 131/新頁 115)・★Prop.6.1(PDF 126/新頁 110・画像✓)
>      + Deligne 10.16(external_reference "SGA 3 V 7"・名前 pin)
>      + 工房補題 TB1-FF′
> ブロック②(arithmetic homotopy exact sequence + 接基点 splitting):
>      ★SGA 1 Exp. IX Th.6.1(PDF 211/新頁 195/旧 253・画像✓・present)
>      ★SGA 1 Exp. V Prop.6.13(PDF 130/新頁 114・画像✓・omitted/reader_exercise)
>      + 工房補題 EXSEQ・SPLIT + (TB2)
>      ⚠ reader_exercise 2 件を内包(V6.13 の証明・IX6.1 の極限段)
> ブロック③(geometric F̂₂ と 0,1,∞ inertia marking):
>      Ihara ICM 1990 §2.3 印字 105-106
>      (③-1 = omitted/silent_omission・③-2 = present・③-3 = omitted・非 load-bearing)
>      + 規約 RD-6′
> ブロック④(local Kummer / restriction comparison Ẑ(1)):
>      Deligne 15.20/15.21/15.22/15.23(+PREUVE)/14.2(present)
>      + (16.1.1) は名前/説明 pin
>      + 工房補題 TB4-INJ・TB4-GEN′(閉部分群としての一致のみ)
> 読み替え: RD-1〜RD-5(v1 §2)+ ★RD-6′(v2 §5・convention route)
> 工房債務: TB1-FF′ / TB4-INJ / TB4-GEN′ / EXSEQ / SPLIT(5 本・紙・単系統・Sol 監査未)
> 非 load-bearing: ③-3(z の ∞-慣性)
> ```

> #### **(N-2′)** CLAIMS **W3-17** の状態欄(追記のみ・既存文字列は削らない)
> ```text
> candidate(paper-proof (framework-conditional on TB1–TB4+(Z_{2M}-link))
>           / two-mathematician audit PASS
>           / ★ TB1・TB3・TB4^u = canonical-source-pinned v2(4 ブロック)
>               (tb_citation_bundle_v2.md・RD-1〜RD-5 + RD-6′・工房債務 5 本・
>                reader_exercise 2 件を内包。Sol 検収後に発効)
>           / exact TB4・Z_{2M}-link の欄は不変)
> ```

> #### **(N-3′)** P97-1.1 層 3 の札
> `theorem_framework-relative (BFC/TB/CAL) [TB: canonical-source-pinned v2]`(**札の種別は変えない** — v1 §7.2 と同じ理由)

### 8.2 ★ 格の請求文(**便 102 の指摘への応答**)

便 102 逐語: 「`canonical-source-pinned` という格も、**明示的未 pin を含む現状とは両立しない**」。

$$\boxed{\ \textbf{★ v2 で明示的未 pin は解消した(【GAP-TB-EXACT】= ブロック ② を頁画像で pin)。ゆえに }\texttt{canonical-source-pinned}\textbf{ を請える。}\ }$$

**ただし請求文に次の 3 条を必ず付す**:
1. **`present` でない pin が 4 件**(V 6.13 = reader_exercise / IX 6.1 内部に reader_exercise 1 件 / Deligne 10.16 = external_reference / Ihara ③-1・③-3 = omitted)。
2. **工房債務 5 本が単系統・Sol 監査未。**
3. ★ **閉鎖後も `source/framework-relative` であり Lean の格ではない**(便 102 F102-7.3 逐語)。

⟹ v1 §7.3 の二段語彙(`canonical-source-pinned` ⊂ `canonical-source-relative`)は**維持**。**`canonical-source-relative` へは到達していない**(理由 = 上の 1・2)。

---

## 9. 本 v2 が**主張しないこと**・残る債務

1. 「**(5′) が昇格した**」— **主張しない**。昇格判定は Sol の専権(便 102 で HOLD)。本 v2 は **HOLD の理由 3 点(4 ブロック未展開・会計の虚偽・未 pin)を解消したと請う**だけである。
2. 「**Deligne 流と Ihara 流の接基点が同一である**」— ★ **主張を取り下げた**(RD-6′(i)・convention route)。
3. 「**$\varepsilon$ / exact (TB4) / $(Z_{2M}$-link$)$ について何かが変わった**」— **主張しない**(RD-6′(iv))。
4. 「**SGA 1 を通読した**」— **主張しない**。私が開いたのは **Exp. V §4–§7(PDF 120・126・130・131)と Exp. IX §6(PDF 211)のみ**。**Exp. XIII(tame $\pi_1$)は 1 頁も開いていない** ⟹ ③-1 の第二 pin 候補は未確認のまま。
5. `cross-checked` / `verified` — **付さない**(機械計算ゼロ・Lean 未使用)。
6. **novelty** — 主張しない。
7. $K^{(5)}$ の値・窓データ・$\hat c_\mu$・PSL 封印欄・$\varepsilon$ bits・$u$ 値 — **一切触れていない**。

### 9.1 残る債務(**明示**)

| # | 債務 | 種別 |
|---|---|---|
| **D-1** | 工房補題 **TB1-FF′ / TB4-INJ / TB4-GEN′ / EXSEQ / SPLIT** の Sol 監査 | 便 1 項目 |
| **D-2** | **EXSEQ (c) の極限段**(= SGA 1 IX 6.1 の reader_exercise)。EGA IV §8 の極限論で閉じる型だが**私は EGA IV を開いていない** | reader_exercise の自前補完 |
| **D-3** | **SGA 1 V 6.13 の reader_exercise** — 自前で証明を書くか、`omitted` のまま札に載せるか | 裁定事項 |
| **D-4** | ③-1 の第二 pin(SGA 1 Exp. XIII 等)— **passport 側で ③-3 が要るときに併せて** | 本 v2 の射程外 |

---

## 10. Sol への再諮問(**3 点・短く**)

> **S′-1** ★ **ブロック ② の pin の形**: 「**SGA 1 V Prop. 6.13 が基本関手一般で述べられているので、接基点への transport は不要**」という私の読み(§3.2)。IX 6.1 は幾何点で述べられているが、その証明が呼ぶ V 6.13 が base-point-free なので、$F=\mathrm{Fib}_{\vec{01}}$ で証明が逐語通る、と読んだ。**この読み替えに穴はないか。**
>
> **S′-2** ★ **reader_exercise 2 件の扱い**(§7・D-2/D-3)。**V 6.13 は「La démonstration est laissée au lecteur」と明記**、**IX 6.1 の極限段も同様**。⟹ ブロック ② の pin を「present な定理」と呼んでよいか、それとも **`omitted/reader_exercise` を含む pin として格を一段落とす**べきか。私は後者(§8.2 の請求文に 3 条を付す形)を採ったが、**より厳しい扱いが正しければ従う。**
>
> **S′-3** **補題 EXSEQ (a) の一段**: 「$\bar{\mathbf Q}$ は $\Omega$ の中で代数閉」(付値が $\bar{\mathbf Q}$ 上自明・剰余体 $\bar{\mathbf Q}$・Hensel 逐次近似)。これで $F(U_L)=\mathrm{Hom}_K(L,\bar{\mathbf Q})$ を得ており、**$p:\pi_1\to G_K$ の存在がここに掛かっている**。穴はないか。
