# 機械観測 2 件の定理昇格検分 — MIRROR-ALL / L3-VACUOUS v1

**状態札: `paper only / proof candidate / Sol 未監査 / GAP 実行ゼロ / 封印非接触 / 新規探索ゼロ`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-06
- 委嘱: 司令塔(裁定 603 予定の入力)—「機械観測 2 件の定理昇格可否の検分。紙のみ・封印非接触」+ 走行中更新(【B】の問いの精密化 = 行別判定式と 17 行予言表)
- 入力(すべて既在・**外部文献ゼロ**):
  - `docs/notes/twin_witness_prereg_iffirst_v1.md`(登録票 §1.4 の 15 対表・§2 MIRROR-SHADOW/MIRROR-CRIT/ABEL-INDEX・§7 予言)
  - `search/certs/twin_witness_run_v1_20260806.json`(裁定 602 の観測・M1 = 15/15)
  - `docs/notes/bu_s35_embedding_v1.md`(定理 EMB-C・EMB-BRAID・系 EMB-LIN)
  - `docs/notes/w6_bottomup_design_v4_1_addendum.md`(exact 17-row 分母)
  - `search/certs/w6_bu_s35_math_detail_20260806.json`(行ごとの `dim_H2_S4` / `num_classes` / `lane_a_marked_lift_counts` / totals)
  - `search/certs/h2_census_s4_20260805.json`(**行の加群同型型の正本**: `socle_structure` 欄 `F2^a + (F2C2)^b + D^c` と `dim_H1_S4` / `dim_H2_S4`)

> ### 非接触・規律の申告
> - **GAP 起動ゼロ。窓の探索ゼロ。列挙ゼロ。** 走らせた機械は **python 1 本・約 60 行**(加群 $\theta,\tau$ 行列の関係式検査と $\lvert\ker N_\theta\rvert\cdot\lvert\ker N_\tau\rvert$ の計算のみ・整数演算)。既存 cert は**読んだだけ**。
> - **封印 3 量非接触**($n=5$ 関連・$\mathrm{Im}\,R$・$d_N$・genuine 層の $u$ 値)。705,894 対宇宙非接触。kill 定理非適用。
> - **L3 層(13 対・$c\notin N$)には一切触れていない**(【要裁定 T-1】を尊重)。本稿の主定理は **$c\in N$ を前件に明示的に使う**。
> - 本稿は発火・凍結・unlock を一切請求しない。全命題は **candidate**(Sol 監査未了)。**Lean 不使用 ⟹ verified と呼ばない。**

---

## 0. 判定(先に 6 行)

| 件 | 判定 | 中身 |
|---|---|---|
| **【A】MIRROR-ALL** | **条件付き(13/15 は定理・残り 2 は機械のみ)** | 新定理 **MIRROR-ODD**(§A.3)が **15 対中 13 対**を紙で閉じる。うち **5 対は §7 で UNKNOWN だったもの**(504×2・882・936×2)。残るのは **432 と 486 = 指数が $\{2,3\}$ のみで割れる 2 窓**ちょうど。ゆえに「この帯の双子対は全て鏡映対」は**まだ定理ではない**が、**未証明部分は 2 窓の有限 1 ビットに縮んだ**。 |
| **【B】L3-VACUOUS** | **不成立(恒偽は偽)** | 「exact 17 層で L-3 恒偽」は**定理でない**(司令塔更新の実測 16/64 と一致して**反証**)。代わりに **完全な行別判定式**(§B.4)が定理として立つ: $\text{L-3}\iff M_R\to V\twoheadrightarrow\mathrm{head}\,V$ が全射。 |
| 予言 | **17 行すべてに数値予言**(§B.5) | L-3 成立数と**像位数分布**を全 17 行で確定的に予言。既知 2 点(**D⊕D = 0/256**・**F2⊕D = 16/64**)を**両方とも再現**。L-3 が非ゼロなのは **3 行だけ**(`p2_d2_a0b0c1` = 8/16、`p2_d3_a1b0c1` = 16/64、`p3_d2_bruteforce_1` = 18/27)。 |
| 検算 | **cert と完全一致** | 私の加群モデルは cert の **17 行すべての `dim_H1_S4`・`dim_H2_S4`・per-class lift 数**、および **`total_classes`=449 / `accepted_classes`=73** を**独立に再現**した(§B.3)。 |
| D⊕D の理由 | $\dim_{\mathbf F_2}\mathrm{Hom}_{\widehat G_5}(M_R,D)=1$ | 2 つの $D$ 成分に入るコサイクル値写像は**必ず比例**する ⟹ 像は対角止まりで $D\oplus D$ に届かない(§B.6)。 |
| 残るギャップ | §C | 432/486(A)・仕様同一性の非当事者判読(B)・古典的コホモロジー事実の孫引き(B) |

---

# Part A — MIRROR-ALL

## A.1 問題の正確な縮約(既在の確認・新規性なし)

登録票 §1.6 O-1(L1 の 56 member は全相異)+ D-1(LINS の $\le1000$ 悉皆)より、L1 上で双子関係は完全マッチング。$\iota\in\mathrm{Aut}(B_3)$ は $PB_3$ と $c\in N$ の条件を保つ($\iota(c)=c^{-1}$)から、$N\in L2$ なら $\iota(N)\in L2$ かつ $B_3/\iota(N)\cong B_3/N$。ゆえに

$$\iota(N)\ne N\ \Longrightarrow\ \{N,\iota(N)\}\ \text{は双子対}\ \overset{\text{O-1+D-1}}{\Longrightarrow}\ \iota(N)=K\ (\text{登録された相方}).$$

⟹ **各対につき残る内容は「$\iota(N)\ne N$」という 1 ビットだけ**(委嘱文の読みは正しい)。以下このビットを紙で取りにいく。

> ★ 逆向きの注意(誤読防止): 「$\iota(N)=K$」の**最後の一歩だけ**が census 依存(O-1/D-1)である。**「$\iota(N)\ne N$」自体は census に依存しない純紙の主張**であり、以下の定理はそちらを与える。

## A.2 新しい鍵 — $c\in N$ は $\widehat P$ を $PSL_2(\mathbf Z)$ 商にする

> ### 補題 PSL-GEN(candidate・本稿)
> $c\in N$ とする。$U:=\Delta N,\ W:=\delta N\in\widehat P=B_3/N$($\Delta=\sigma_1\sigma_2\sigma_1,\ \delta=\sigma_1\sigma_2$)と置くと
> $$\boxed{\ \widehat P=\langle U,W\rangle,\qquad U^2=W^3=1\ }$$
> すなわち $\widehat P$ は $B_3/\langle c\rangle\cong PSL_2(\mathbf Z)\cong C_2\ast C_3$ の商である。

**証明.** $B_3=\langle\Delta,\delta\mid\Delta^2=\delta^3\rangle$(標準表示)、$c=\Delta^2=\delta^3$。$c\in N$ より $U^2=W^3=1$。$\sigma_1=\delta^{-1}\Delta,\ \sigma_2=\Delta^{-1}\delta^2$(`bu_s35_embedding_v1.md` (1.1)・検算済)ゆえ $\langle U,W\rangle\ni\sigma_1N,\sigma_2N$ ⟹ 全体。∎

> ### 補題 MIRROR-PSL(candidate・本稿)— MIRROR-CRIT の $\widehat P$ 版
> $c\in N$ のとき
> $$\boxed{\ \iota(N)=N\iff \exists\beta\in\mathrm{Aut}(\widehat P):\ \beta(U)=U,\ \ \beta(W)=W^{-1}\ }$$

**証明.** $\iota(\Delta)=\Delta^{-1}$、$\sigma_2\sigma_1=\Delta\delta\Delta^{-1}$ ゆえ $\iota(\delta)=(\sigma_2\sigma_1)^{-1}=\Delta\delta^{-1}\Delta^{-1}$。$\iota(c)=c^{-1}$ より $\iota$ は $\Gamma:=B_3/\langle c\rangle$ に降り、そこで $U\mapsto U^{-1}=U$、$W\mapsto UW^{-1}U^{-1}$。内部自己同型 $\mathrm{Inn}(U^{-1})$ を合成した $\iota':=\mathrm{Inn}(U^{-1})\circ\iota$ は $U\mapsto U,\ W\mapsto W^{-1}$。$\bar N:=N/\langle c\rangle\trianglelefteq\Gamma$ は内部自己同型で不変だから $\iota(N)=N\iff\iota'(\bar N)=\bar N\iff\iota'$ が $\widehat P=\Gamma/\bar N$ に降りる。∎

> ★ **意味**: 判定は「**位数 3 の生成元だけを反転する対称性**が商に存在するか」に化けた。これは dessin/hypermap の **reflexibility(鏡像対称性)** そのものであり、**非鏡映対 = chiral(掌性のある)dessin** である。§A.5 の【文献要請】はこの語で出す。

## A.3 定理 MIRROR-ODD(本稿の主結果)

> ### 定理 MIRROR-ODD(candidate・本稿)
> **【射程の訂正 2026-08-06・§G.6.c】: 下の「$N\le PB_3$」は証明のどの段でも使われていない。正しい前件は「$c\in N$」+ (H) だけであり、本定理は窓以外の $B_3$-正規部分群にも適用できる**(この訂正により census の非窓層 11 対で独立確認が取れた)。
> $N\trianglelefteq B_3$、~~$N\le PB_3$~~、$c\in N$ とする。ある素数 $q\ge5$ について
> $$\textbf{(H)}\quad \mathrm{Syl}_q(\widehat P)\ \text{は非自明・巡回・正規}$$
> が成り立てば
> $$\boxed{\ \iota(N)\ne N\ }$$
> ゆえに(補題 MIRROR-SHADOW より)$[-1,1]\in\mathrm{GTSh}(\iota(N),N)$ は**非 settled shadow**であり、**$N$ は非 isolated**。

**証明.** $A:=\mathrm{Syl}_q(\widehat P)=O_q(\widehat P)$ は唯一ゆえ**特性**。$A$ 巡回 ⟹ $\mathrm{Aut}(A)$ は可換。$\mu:\widehat P\to\mathrm{Aut}(A)$ を共役表現とする。

**(1) 正規閉包 $\widehat P_0$.** $\widehat P_0:=\langle W,\,UWU^{-1}\rangle$ と置く。$U^2=1$ より $U\widehat P_0U^{-1}=\widehat P_0$、また $W\in\widehat P_0$ ゆえ $\widehat P_0\trianglelefteq\widehat P=\langle U,W\rangle$(補題 PSL-GEN)。$\widehat P/\widehat P_0$ は $U$ の像で生成される ⟹ $[\widehat P:\widehat P_0]\le2$。さらに $\widehat P_0$ は**位数 3 の 2 元で生成される**から
$$\boxed{\ \widehat P_0^{\rm ab}\ \text{は指数 }3\text{ の初等可換群、}\ \lvert\widehat P_0^{\rm ab}\rvert\ \text{は}\ 9\ \text{を割る}.\ }\tag{A.1}$$

**(2) $\mu(W)\ne1$(ι を使わない).** $\lvert A\rvert$ は奇数、$[\widehat P:\widehat P_0]\le2$ ⟹ $A\subseteq\widehat P_0$、したがって $A=\mathrm{Syl}_q(\widehat P_0)\trianglelefteq\widehat P_0$。
いま $\mu(W)=1$ と仮定する。$\mathrm{Aut}(A)$ 可換ゆえ $\mu(UWU^{-1})=\mu(U)\mu(W)\mu(U)^{-1}=\mu(W)=1$ ⟹ $\mu(\widehat P_0)=1$ ⟹ $A\le Z(\widehat P_0)$。$A$ は正規 Hall(= 完全な Sylow)部分群だから Schur–Zassenhaus で $\widehat P_0=A\rtimes Q$、中心的ゆえ $\widehat P_0=A\times Q$ ⟹ $\widehat P_0^{\rm ab}\cong A\times Q^{\rm ab}$ は位数 $q\ge5$ の元をもつ — (A.1) の指数 3 に矛盾。ゆえに **$\mu(W)\ne1$**。

**(3) ι の排除.** $\iota(N)=N$ とすると補題 MIRROR-PSL の $\beta$ が存在。$A$ 特性ゆえ $h:=\beta|_A\in\mathrm{Aut}(A)$ で、任意の $g$ に対し $\mu(\beta(g))=h\,\mu(g)\,h^{-1}=\mu(g)$($\mathrm{Aut}(A)$ 可換)。$g=W$ に適用して
$$\mu(W)^{-1}=\mu(W^{-1})=\mu(\beta(W))=\mu(W)\ \Longrightarrow\ \mu(W)^2=1,$$
一方 $W^3=1$ ゆえ $\mu(W)^3=1$ ⟹ $\mu(W)=1$ — (2) に矛盾。∎

> ### 系(工程上の意味)
> **(H) を満たす窓は、悉皆列挙を一切せずに「非 isolated・明示 witness $[-1,1]$」が確定する。** これは M-ISO-2 fixture の**紙側の供給源**である(算術元であることの限定文は登録票 §5.2 のまま不変)。

## A.4 15 対への適用(どこまでが指数だけで出るか)

$\widehat P$ の位数は指数に等しい。(H) の**正規性**は多くの窓で Sylow の数え上げだけから出る($n_q\mid\lvert\widehat P\rvert/q^k$、$n_q\equiv1\ (q)$)。

| # | 指数 | $q$ | $\mathrm{Syl}_q$ | 正規性の根拠 | 巡回性の根拠 | **判定** |
|---|---|---|---|---|---|---|
| 1 | 126 | 7 | $C_7$ | **自動**($n_7\mid18$, $\equiv1(7)\Rightarrow1$) | 位数 $7$ | **定理** |
| 2 | 234 | 13 | $C_{13}$ | **自動**($n_{13}\mid18$) | 位数 $13$ | **定理** |
| 3 | 342 | 19 | $C_{19}$ | **自動** | 位数 $19$ | **定理** |
| 4 | 378 | 7 | $C_7$ | **自動**($n_7\mid54$, 全約数 $\not\equiv1$ 除く) | 位数 $7$ | **定理** |
| 5 | **432** | — | — | $432=2^4\cdot3^3$ ⟹ $q\ge5$ なし | — | **未証明** |
| 6 | **486** | — | — | $486=2\cdot3^5$ ⟹ $q\ge5$ なし | — | **未証明** |
| 7 | 504 | 7 | $C_7$ | cert 構造式 `C7 : (A4 x S3)`(自動は不可: $n_7\in\{1,8,36\}$) | 位数 $7$ | **定理**(cert 入力 1 個) |
| 8 | 504 | 7 | $C_7$ | cert 構造式 `C7 : (C3 x S4)` | 位数 $7$ | **定理**(同) |
| 9 | 558 | 31 | $C_{31}$ | **自動** | 位数 $31$ | **定理** |
| 10 | 666 | 37 | $C_{37}$ | **自動** | 位数 $37$ | **定理** |
| 11 | 702 | 13 | $C_{13}$ | cert 構造式 `C13 : ((C3xC3):C6)`(自動は不可: $n_{13}\in\{1,27\}$) | 位数 $13$ | **定理**(cert 入力 1 個) |
| 12 | 774 | 43 | $C_{43}$ | **自動** | 位数 $43$ | **定理** |
| 13 | **882** | 7 | $C_{49}$ | **自動**($n_7\mid18$) | cert 構造式 `C49 : (C3 x S3)`(← $C_7\times C_7$ でないこと) | **定理**(cert 入力 1 個)★ |
| 14 | 936 | 13 | $C_{13}$ | **自動**($n_{13}\mid72$, $\equiv1(13)\Rightarrow1$) | 位数 $13$ | **定理**★ |
| 15 | 936 | 13 | $C_{13}$ | **自動** | 位数 $13$ | **定理**★ |

**集計**: **13/15 が定理**。うち **9 窓は指数の数値だけで完結**(cert 入力ゼロ)、**4 窓は census cert の構造式を 1 個だけ入力**(504×2 の正規性・702 の正規性・882 の巡回性)。★ = 登録票 §7 で **UNKNOWN だったものが本稿で閉じた**もの(5 対: 504×2・882・936×2)。

> ### 旧道具との関係(なぜ届くようになったか)
> 旧 MIRROR-OBSTRUCTION(登録票 §2.4 (b))は $P=PB_3/N$ 上で「$\mu(P)$ が初等可換 2 群でない」を要求し、$\mu(P)$ の 3-part が紙で決まらない窓で止まっていた。本稿は
> 1. 舞台を $P$ から **$\widehat P$** に上げ($c\in N$ を**生成の形**で使う = PSL-GEN)、
> 2. 判定を「$\beta(U)=U,\ \beta(W)=W^{-1}$」に正規化して(MIRROR-PSL)、要求を **$\mu(W)\ne1$ の 1 本**に減らし、
> 3. その $\mu(W)\ne1$ を **$\widehat P_0^{\rm ab}$ の指数 3**(A.1)から**無条件に導いた**。
>
> ⟹ 「$\mu$ の 3-part を決める」という旧来の未決点が**消えた**。

## A.5 残る 2 窓(432・486)— なぜ届かないか

定理の (H) は $q\ge5$ を要求する。これは本質的で、証明の心臓 (A.1)「$\widehat P_0^{\rm ab}$ の指数は 3」が **$q=3$ を排除できない**ためである。実際:

- **432** $=2^4\cdot3^3$、$\widehat P=(((C_3\times C_3):Q_8):C_3):C_2$。特性部分群の候補 $O_3(\widehat P)\supseteq C_3\times C_3$ は $\mathrm{Aut}=GL(2,3)$ が**非可換** ⟹ 補題の可換性が使えない。一般化版(§A.6 Tool R2′)は「$h\in\mathrm{Aut}(A)$ で $\mu(U)$ を中心化し $\mu(W)$ を反転するものが存在するか」という**具体的な有限判定**になり、$GL(2,3)$ 内ではこれが**可能な配置が実在する**(例: 単冪元の反転は $\mathrm{diag}(1,-1)$ で起こる)⟹ 一般論では落ちない。
- **486** $=2\cdot3^5$、$\widehat P=((C_9:C_9):C_3):C_2$。ここでは $S:=\mathrm{Syl}_3(\widehat P)=\widehat P_0$(位数 243・指数 2)が確定し、判定は「**$U$-同変な $\alpha\in\mathrm{Aut}(S)$ で $W\mapsto W^{-1}$**」に落ちる。$S$ の下降中心列の各因子は $S$ 自身に中心化されるので、**巡回特性切片からの障害は原理的に出ない**。
  - ★ 副産物(反証可能な帰結): (A.1) より $S^{\rm ab}\cong C_3\times C_3$ が**必然**。⟹ $S$ は位数 3 の 2 元で生成される位数 243 の群。**もし $S$ が相対自由(class 3 の $C_3\ast C_3$ 商 = 生成元の任意の置換が延びる)なら $\iota(N)=N$ となり機械観測と矛盾する** ⟹ **予言: $S$ は相対自由でない(class 4 = maximal class 側)**。これは 486 窓に対する独立チェック項目になる。

> ### 【文献要請】(§A.5 起点)
> - **困難**: $\{2,3\}$-群 $\widehat P$($(2,3)$-生成)について、「位数 3 の生成元のみを反転する自己同型の非存在」= **regular dessin / hypermap の chirality** を、**群の不変量から判定する機構**が欲しい。
> - **欲しい結果の型**: (i) $(2,3)$-生成有限群の **reflexibility/chirality の判定法**(chirality group・chirality index 等の不変量)。(ii) 特に $p$-群($p=3$)商における chirality の**存在・非存在の族的判定**。(iii) $C_2\ast C_3$ の有限商における「$W\mapsto W^{-1}$ 型の外部対称性」の障害理論。
> - **なぜ効くか**: 現状 432/486 は機械の 1 ビット(witness word)でしか閉じていない。上の機構があれば **MIRROR-ALL が帯全体で定理化**する。
> - 探索語の当たり: *chiral regular dessin*, *chirality group of a hypermap*, *reflexible (2,3)-generated group*, *Petrie/mirror symmetry of maps*。

## A.6 一般化と副産物(帯に依らない形)

> ### Tool R2′(一般形・candidate)
> $A$ を $\widehat P$ の特性部分群または**特性切片**とし、$\mu:\widehat P\to\mathrm{Aut}(A)$ を作用とする。$\iota(N)=N$ なら
> $$\exists h\in\mathrm{Aut}(A):\quad h\,\mu(U)\,h^{-1}=\mu(U),\qquad h\,\mu(W)\,h^{-1}=\mu(W)^{-1}.$$
> $\mathrm{Aut}(A)$ 可換ならこれは $\mu(W)=1$ に退化する(= §A.3 で使った形)。

> ### ~~補題 ABEL-TYPE v1~~(**誤り・撤回。下の v2 を使うこと**)
> ~~$P\cong(\mathbf Z/n)^2$ または $\mathbf Z/n\times\mathbf Z/3n$ $(3\nmid n)$。とくに **$P$ の各 Sylow 部分群は階数ちょうど 2(巡回でない)**。~~
>
> ### ★ 補題 ABEL-TYPE **v2**(candidate・本稿。2026-08-06 修文。指摘: **Sol / 便 112 返書**)
> $c\in N$ で $P=F_2/N_{F_2}$ が可換なら
> $$\boxed{\ P\cong(\mathbf Z/n)^2\quad\text{または}\quad \mathbf Z/n\times\mathbf Z/3n\qquad(n\ge1\ \textbf{— }n\text{ に条件は付かない})\ }$$
> **Sylow の階数(正しい形)**:
> - **$p\ne3$**: $p$-成分は $(\mathbf Z/p^a)^2$ = **homocyclic 階数 2**(または自明)。⟹ **非自明巡回にはなれない**。
> - **$p=3$**: 第 1 型なら $(\mathbf Z/3^k)^2$;第 2 型 $\mathbf Z/n\times\mathbf Z/3n$ で $3^k\,\|\,n$ なら $C_{3^k}\times C_{3^{k+1}}$、**とくに $3\nmid n$ のとき 3-成分は $C_3$(階数 1・巡回)**。
> $$\Longrightarrow\ \boxed{\ \text{「各 Sylow は階数 2」は\textbf{偽}。正しくは「}p\ne3\text{ の Sylow が階数 2」}\ }$$

> ### 修文の影響検査(**既用の結論は全て無傷**・逐一確認)
> | 使用箇所 | 使った形 | v2 での成否 |
> |---|---|---|
> | **882**($\lvert P\rvert=147=3\cdot7^2$) | 「$P$ 可換 ⟹ Sylow$_7$ は $C_7\times C_7$」⟹ cert の $C_{49}$ と矛盾 ⟹ $P$ 非可換 | **無傷**。$147=3n^2\ (n=7)$ ⟹ 第 2 型 $\mathbf Z/7\times\mathbf Z/21$ ⟹ 7-成分 $=C_7\times C_7$ ✓($7\ne3$ ゆえ v2 の第 1 項が効く)。※ここで 3-成分は $C_3$(階数 1)だが**使っていない** |
> | **486**($\lvert P\rvert=81$) | 「$P$ 可換 ⟹ 巡回でない」⟹ $\mathrm{ord}(\bar x)=81$ を排除 ⟹ $n\in\{18,54\}$ | **無傷**。$81=n^2\ (n=9)$ のみ($3n^2=81\Rightarrow n^2=27$ は非整数)⟹ $P\cong C_9\times C_9$ ⟹ 非巡回 ✓ |
> | **ABEL-INDEX**($\lvert P\rvert\in\{n^2,3n^2\}$) | 指数の形のみ | **無傷**(v1/v2 で同一) |
> ⟹ **MIRROR-ODD・§F.2 の型絞り込み・§F.6.2 の予言はいずれも再計算不要。**

**証明.** 登録票 §2.4 ABEL-INDEX の証明より $P\cong\mathbf Z[\omega]/(\alpha)$、$\alpha\sim n(1-\omega)^{\varepsilon}$。$\varepsilon=0$ なら加法群は $(\mathbf Z/n)^2$。$\varepsilon=1$、$3\nmid n$ なら $\mathbf Z[\omega]/(n)\times\mathbf Z[\omega]/(1-\omega)\cong(\mathbf Z/n)^2\times\mathbf Z/3$。$3\mid n$ の場合は $(1-\omega)^m$ の形に統合され $\mathbf Z/3^{k+1}\oplus\mathbf Z/3^k$ 型 — いずれも階数 2。∎

> **使い方**: 指数から $\lvert P\rvert$ が出れば、可換の場合の同型型が**一意に決まる**。ゆえに census の構造式が「$q$-Sylow は巡回」と言えば **$P$ は非可換**が即座に従う(例: 882 の $C_{49}$)。ABEL-INDEX が不決だった $\lvert P\rvert=147,\,81$ でもこれは効く。

> ### 一般帯への拡張可否(委嘱の一言)
> **MIRROR-ODD は指数上界に依存しない。** 前件は「$c\in N$ かつ $\widehat P$ が $q\ge5$ の巡回正規 Sylow をもつ」だけである。ゆえに**任意の帯**で、$\lvert\widehat P\rvert$ が $2^a3^b$ 型でない窓の多くを一撃で覆う。**覆えないのは $\lvert\widehat P\rvert=2^a3^b$ の窓と、$q\ge5$-Sylow が非巡回/非正規の窓**に限られる。これは「鏡映対性は $\{2,3\}$-部分に本質的な難しさが集中する」という帯構造の主張でもある(candidate)。

---

# Part B — L-3 の恒偽性

## B.0 判定

**「exact 17 層宇宙で L-3 は恒偽」は不成立**(定理ではない)。司令塔更新の実測(`p2_d3_a1b0c1` で 16/64)と本稿の理論は一致し、**理論が先に同じ数を出す**(§B.5)。代わりに以下が定理として立つ。

## B.1 枠組み — 像 $\cap\,V$ は「関係部分群のコサイクル値」

設定は `bu_s35_embedding_v1.md` のまま: $1\to V\to\widehat{\mathcal P}\xrightarrow{\pi}\widehat G_5\to1$($V$ は $\mathbf F_p[\widehat G_5]$-加群)、marked lift = $\rho:B_3\to\widehat{\mathcal P}$、$\pi\rho=q$、$\rho(c)=1$。定理 EMB-C($q(c)=1$)より marked lift は
$$\rho:\ \Gamma:=B_3/\langle c\rangle\cong C_2\ast C_3\ \longrightarrow\ \widehat{\mathcal P},\qquad \pi\rho=\bar q$$
と同一(定理 EMB-BRAID)。**$R:=\ker(\bar q:\Gamma\twoheadrightarrow\widehat G_5)$** と置く。

> ### 命題 L3-KERNEL(candidate・本稿)
> $$\boxed{\ \mathrm{im}\,\rho\cap V=\rho(R),\qquad \lvert\mathrm{im}\,\rho\rvert=3000\cdot\lvert\rho(R)\rvert\ }$$
> であり $\rho|_R:R\to V$ は準同型で $\bar q$-同変、すなわち
> $$\rho|_R\in\mathrm{Hom}_{\widehat G_5}(M_R,\,V),\qquad M_R:=R^{\rm ab}\otimes\mathbf F_p .$$
> したがって $\mathbf{L\text{-}3}\iff\rho(R)=V$。

**証明.** $\pi\rho=\bar q$ ゆえ $\rho(R)\subseteq V$、かつ $\mathrm{im}\,\rho\cap V=\rho(R)$($v=\rho(g)\in V\Rightarrow\bar q(g)=1\Rightarrow g\in R$)。$\mathrm{im}\,\rho/\rho(R)\cong\widehat G_5$(位数 3000)。同変性: $r\in R,g\in\Gamma$ で $\rho(grg^{-1})=\rho(g)\rho(r)\rho(g)^{-1}=\bar q(g)\cdot\rho(r)$($V$ 上の作用)。$V$ は $\mathbf F_p$ 加群ゆえ $\rho|_R$ は $R^{\rm ab}\otimes\mathbf F_p$ を経由。∎

**$M_R$ の正体**(Bass–Serre 木 $T$ の $R$-商グラフの鎖複体; $R$ は $\Gamma$ の捩れ元を避けるので自由):
$$0\to M_R\to\mathbf F_p[\widehat G_5]\to\mathbf F_p[\widehat G_5/\langle u\rangle]\oplus\mathbf F_p[\widehat G_5/\langle w\rangle]\to\mathbf F_p\to0,\qquad u=\bar q(\Delta),\ w=\bar q(\delta).$$
階数検算: $3000-(1500+1000)+1=501$、Euler 標数 $\chi(R)=3000\cdot(1/2+1/3-1)=-500$ ⟹ $R\cong F_{501}$ ✓。

## B.2 判定式の骨格 — 3 本の補題

> ### 補題 L3-A(押し出しと核)
> 部分加群 $W\le V$ に対し
> $$\rho(R)\subseteq W\iff \rho_W:\Gamma\to\widehat{\mathcal P}/W\ \text{が}\ \widehat G_5\ \text{を経由}\ \Longrightarrow\ \varepsilon_W:=(\text{押し出し類})=0\ \text{in}\ H^2(\widehat G_5,V/W).$$

> ### 補題 L3-B(lift 依存度)
> marked lift の集合が空でなければ、それは $Z^1(\Gamma,V)$ の torsor。したがって
> $$\{\rho|_R\}=\rho_0|_R+\mathrm{res}\bigl(Z^1(\Gamma,V)\bigr),\qquad \dim\mathrm{res}\bigl(Z^1(\Gamma,V)\bigr)=\dim H^1(\Gamma,V)-\dim H^1(\widehat G_5,V).$$
> **$d_V:=\dim H^1(\Gamma,V)-\dim H^1(\widehat G_5,V)=0$ なら $\rho(R)$ は拡大類だけで決まり、lift に依らない。**($\ker\mathrm{res}=\mathrm{inf}\,Z^1(\widehat G_5,V)$、inflation は単射。)

> ### 補題 L3-C(Nakayama への還元)
> $$\mathbf{L\text{-}3}\iff \rho(R)+\mathrm{rad}\,V=V\iff M_R\xrightarrow{\rho|_R}V\twoheadrightarrow\mathrm{head}\,V\ \text{が全射}.$$

**帰結(判定式の最終形)**: 単純加群 $S$ ごとに、**head の $S$-重複度**と、**到達可能な $\mathrm{Hom}_{\widehat G_5}(M_R,S)$ の張る空間の次元**を比べればよい。

## B.3 係数の確定(すべて cert と独立に一致)

$\widehat G_5=A\rtimes S_4$、$\lvert A\rvert=125$ は $p\in\{2,3\}$ と互いに素 ⟹ $H^n(\widehat G_5,V)\cong H^n(S_4,V)$。(V-cen) ゆえ $V$ は $S_4\twoheadrightarrow S_3$ からの inflation。$u\mapsto(1\,2)$、$w\mapsto(1\,3\,4)$(`bu_s35_embedding_v1.md` §4.5)。

### B.3.1 加群の同定(cert `socle_structure` = `F2^a + (F2C2)^b + D^c` と一致)

$p=2$ の $\mathbf F_2[S_3]$ 直既約は 3 つ(Sylow$_2$ が位数 2 の巡回 ⟹ 主ブロックは Brauer 木):

| 記号 | 実体 | $\dim$ | head | soc | $\theta$ | $\tau$ |
|---|---|---|---|---|---|---|
| $\mathbf F_2$ | 自明 | 1 | $\mathbf F_2$ | $\mathbf F_2$ | $1$ | $1$ |
| $E=\mathbf F_2C_2$ | $\mathrm{Ind}_{A_4}^{S_4}\mathbf F_2$ | 2 | $\mathbf F_2$ | $\mathbf F_2$ | swap | $1$ |
| $D$ | 2 次元単純(射影的) | 2 | $D$ | $D$ | $\binom{1\ 1}{0\ 1}$ | $\binom{0\ 1}{1\ 1}$ |

$p=3$ の 2 次元(inflate)は 5 型: $\mathbf F_3^2$、$\mathbf F_3\oplus\mathrm{sgn}$、$\mathrm{sgn}^2$、$U_a$(soc 自明・head sgn)、$U_b$(soc sgn・head 自明)。

### B.3.2 コホモロジー(本稿が独立に計算した値)

| $S$ | $\dim H^1(\Gamma,S)$ | $\dim H^1(S_4,S)$ | $d_S$ | $\dim H^2(S_4,S)$ | 根拠 |
|---|---|---|---|---|---|
| $\mathbf F_2$ | 1 | 1 | **0** | 2 | $\mathrm{Hom}(C_6,\mathbf F_2)$ / $\mathrm{sgn}$ / $H^*(S_4;\mathbf F_2)=\mathbf F_2[x_1,x_2,x_3]/(x_1x_3)$ |
| $E$ | 1 | 0 | **0** | 1 | Shapiro: $H^n(S_4,E)=H^n(A_4;\mathbf F_2)$、$H^1(A_4;\mathbf F_2)=0$、$H^2(A_4;\mathbf F_2)=\mathbf F_2$ |
| $D$ | 1 | 1 | **0** | 1 | $D$ は $\mathbf F_2[S_3]$-射影 ⟹ LHS が $H^n(S_4,D)=(H^n(V_4;\mathbf F_2)\otimes D)^{S_3}$ に潰れる |
| $\mathbf F_3$ | 1 | 0 | **1** | 0 | $H^*(S_4;\mathbf F_3)=H^*(C_3;\mathbf F_3)^{\rm st}$: 次数 $0,3,4,7,\dots$ |
| $\mathrm{sgn}_3$ | 1 | 1 | **0** | 1 | 同上・符号ひねりで次数 $1,2,5,6,\dots$ |

> ★ **本稿が計算したこれらの値は、cert の 17 行すべての `dim_H1_S4` / `dim_H2_S4` を再現する**:
> $p=2$: $\dim H^1=a+c$、$\dim H^2=2a+b+c$ — **12/12 一致**。
> $p=3$: $(\mathbf F_3^2,\mathrm{sgn}^2,U_a,U_b,\mathbf F_3\!\oplus\!\mathrm{sgn})$ の $(\dim H^1,\dim H^2)=(0,0),(2,2),(1,0),(0,1),(1,1)$ — cert の行 4,5,2,1,3 と **5/5 一致**。
> ⟹ **行の加群同定が確定**(とくに `p3_d2_bruteforce_1` $=U_b$、`_2` $=U_a$、`_3` $=\mathbf F_3\oplus\mathrm{sgn}$、`_4`$=\mathbf F_3^2$、`_5`$=\mathrm{sgn}^2$)。

### B.3.3 lift 数と受理類数(独立再現)

EMB-LIN より 1 類あたりの marked lift 数 $=\lvert\ker N_\theta\rvert\cdot\lvert\ker N_\tau\rvert$。python 検算(60 行):
$\mathbf F_2:2,\ E:2,\ D:8$;$\mathbf F_3:3,\ \mathrm{sgn}:9,\ U_a:27,\ U_b:27$ ⟹ **cert の per-class 値 17/17 一致**。
受理類(marked lift が存在する類)$=\ker\bigl(H^2(\widehat G_5,V)\to H^2(\langle u\rangle,V)\oplus H^2(\langle w\rangle,V)\bigr)$。計算すると **$\mathbf F_2$ 成分だけが制約を受け**(各 $\mathbf F_2$ 成分の類は 1 次元部分空間 $\langle\nu\rangle$ に限られる)、$E,D$ 成分は無制約、$p=3$ では $\mathrm{sgn}$ 成分が $0$ に限られ $\mathbf F_3$ 成分は $H^2=0$。
⟹ 受理類数 $=\sum_{\rm rows}2^{\#\rm summands}$ 等 ⟹ **合計 73 / 全 449** — cert の `totals` と**完全一致**。

## B.4 定理(判定式)

> ### 定理 L3-CRIT(candidate・本稿)
> (V-cen) の 17 行宇宙において、marked lift $\rho$ に対し
> $$\boxed{\ \mathbf{L\text{-}3}(\rho)\iff M_R\xrightarrow{\ \rho|_R\ }V\twoheadrightarrow\mathrm{head}\,V\ \text{が全射}\ }$$
> であり、head 成分は次で完全に決まる($V=\mathbf F_p^{\,a}\oplus E^{\,b}\oplus D^{\,c}$ 等の直既約分解に沿って):
>
> **(p=2)** $\dim_{\mathbf F_2}\mathrm{Hom}_{\widehat G_5}(M_R,\mathbf F_2)=\dim_{\mathbf F_2}\mathrm{Hom}_{\widehat G_5}(M_R,D)=\mathbf 1$。ゆえに
> - $\mathbf F_2$-成分 $j$: head 成分 $=\varepsilon_j\ne0$ なら $f$、$\varepsilon_j=0$ なら $0$($f$ は**全成分共通**の生成元)
> - $E$-成分: head 成分は**恒等的に $0$**(∵ $\pi_*=\mathrm{cor}_{A_4}^{S_4}:H^2(A_4;\mathbf F_2)\to H^2(S_4;\mathbf F_2)$ が零)
> - $D$-成分 $j$: $\varepsilon_j\ne0$ なら $g$、$=0$ なら $0$($g$ も全成分共通)
> $$\Longrightarrow\quad \mathbf{L\text{-}3}\ \text{が起こりうる}\iff b=0,\ a\le1,\ c\le1;\quad\text{そのとき}\iff \text{該当 }\varepsilon\ \text{が全て}\ne0 .$$
>
> **(p=3)** $\mathrm{sgn}$ の head 成分は恒等的に $0$($d_{\rm sgn}=0$ かつ受理類は $\varepsilon=0$ のみ)。$\mathbf F_3$ の head 成分は $\mathrm{res}(Z^1(\Gamma,\mathbf F_3))$($1$ 次元)を動く(**lift 依存**)。
> $$\Longrightarrow\quad \mathbf{L\text{-}3}\ \text{が起こりうる}\iff \mathrm{head}\,V\cong\mathbf F_3\ (\text{重複度 }1,\ \mathrm{sgn}\ \text{を含まない})\iff V\cong U_b .$$

**さらに像位数**:
$$\boxed{\ \lvert\mathrm{im}\,\rho\rvert=3000\cdot\lvert\rho(R)\rvert,\qquad
\rho(R)=\mathrm{im}\bigl(M_R\xrightarrow{(f\text{-部},\,g\text{-部})}V\bigr)\ }$$
$p=2$ では $f$ と $g$ が全成分で共通なので、$\rho(R)$ は「$\mathbf F_2$ を 1 本 + $D$ を 1 本」までしか作れない:
$$\lvert\rho(R)\rvert=2^{[\exists\,\text{triv 型成分で }\varepsilon\ne0]}\cdot4^{[\exists\,D\text{ 成分で }\varepsilon\ne0]}\ \Longrightarrow\ \lvert\mathrm{im}\,\rho\rvert\in\{3000,\ 6000,\ 12000,\ 24000\}\ \textbf{のみ}.$$

## B.5 ★ 17 行予言表(実装係の shard 実測と突合する形)

記号: $A:=a+b$(head が自明な直既約の個数)、$C:=c$、$L$ = 1 類あたり lift 数、受理類数 $=2^{A+C}$($p=2$)。

| # | module_id | $V$ | 全 lift | **L-3 数(予言)** | 像位数分布(予言) |
|---|---|---|---:|---:|---|
| 1 | `p2_d2_a0b0c1` | $D$ | 16 | **8** | 3000×8, **12000×8** |
| 2 | `p2_d2_a0b1c0` | $E$ | 4 | **0** | 3000×2, 6000×2 |
| 3 | `p2_d2_a2b0c0` | $\mathbf F_2^2$ | 16 | **0** | 3000×4, 6000×12 |
| 4 | `p2_d3_a1b0c1` | $\mathbf F_2\oplus D$ | 64 | **16** ✅観測一致 | 3000×16, 6000×16, 12000×16, **24000×16** |
| 5 | `p2_d3_a1b1c0` | $\mathbf F_2\oplus E$ | 16 | **0** | 3000×4, 6000×12 |
| 6 | `p2_d3_a3b0c0` | $\mathbf F_2^3$ | 64 | **0** | 3000×8, 6000×56 |
| 7 | `p2_d4_a0b0c2` | $D\oplus D$ | 256 | **0** ✅観測一致 | 3000×64, 12000×192 |
| 8 | `p2_d4_a0b1c1` | $E\oplus D$ | 64 | **0** | 3000×16, 6000×16, 12000×16, 24000×16 |
| 9 | `p2_d4_a0b2c0` | $E^2$ | 16 | **0** | 3000×4, 6000×12 |
| 10 | `p2_d4_a2b0c1` | $\mathbf F_2^2\oplus D$ | 256 | **0** | 3000×32, 6000×96, 12000×32, 24000×96 |
| 11 | `p2_d4_a2b1c0` | $\mathbf F_2^2\oplus E$ | 64 | **0** | 3000×8, 6000×56 |
| 12 | `p2_d4_a4b0c0` | $\mathbf F_2^4$ | 256 | **0** | 3000×16, 6000×240 |
| 13 | `p3_d2_bruteforce_1` | $U_b$(soc sgn/head 自明) | 27 | **18** ★唯一の $p=3$ 非ゼロ | 3000×9, **27000×18** |
| 14 | `p3_d2_bruteforce_2` | $U_a$(soc 自明/head sgn) | 27 | **0** | 3000×9, 9000×18 |
| 15 | `p3_d2_bruteforce_3` | $\mathbf F_3\oplus\mathrm{sgn}$ | 27 | **0** | 3000×9, 9000×18 |
| 16 | `p3_d2_bruteforce_4` | $\mathbf F_3^2$ | 9 | **0** | 3000×1, 9000×8 |
| 17 | `p3_d2_bruteforce_5` | $\mathrm{sgn}^2$ | 81 | **0** | 3000×81 |
| | **合計** | | **1263** | **42** | |

```json
{"prediction_id":"L3-PRED-v1","doc":"docs/notes/theorem_check_mirrorall_l3vacuous_v1.md",
 "total_marked_lifts":1263,"total_L3_true":42,
 "rows":[
  {"module_id":"p2_d2_a0b0c1","lifts":16,"L3":8,"image_orders":{"3000":8,"12000":8}},
  {"module_id":"p2_d2_a0b1c0","lifts":4,"L3":0,"image_orders":{"3000":2,"6000":2}},
  {"module_id":"p2_d2_a2b0c0","lifts":16,"L3":0,"image_orders":{"3000":4,"6000":12}},
  {"module_id":"p2_d3_a1b0c1","lifts":64,"L3":16,"image_orders":{"3000":16,"6000":16,"12000":16,"24000":16}},
  {"module_id":"p2_d3_a1b1c0","lifts":16,"L3":0,"image_orders":{"3000":4,"6000":12}},
  {"module_id":"p2_d3_a3b0c0","lifts":64,"L3":0,"image_orders":{"3000":8,"6000":56}},
  {"module_id":"p2_d4_a0b0c2","lifts":256,"L3":0,"image_orders":{"3000":64,"12000":192}},
  {"module_id":"p2_d4_a0b1c1","lifts":64,"L3":0,"image_orders":{"3000":16,"6000":16,"12000":16,"24000":16}},
  {"module_id":"p2_d4_a0b2c0","lifts":16,"L3":0,"image_orders":{"3000":4,"6000":12}},
  {"module_id":"p2_d4_a2b0c1","lifts":256,"L3":0,"image_orders":{"3000":32,"6000":96,"12000":32,"24000":96}},
  {"module_id":"p2_d4_a2b1c0","lifts":64,"L3":0,"image_orders":{"3000":8,"6000":56}},
  {"module_id":"p2_d4_a4b0c0","lifts":256,"L3":0,"image_orders":{"3000":16,"6000":240}},
  {"module_id":"p3_d2_bruteforce_1","lifts":27,"L3":18,"image_orders":{"3000":9,"27000":18}},
  {"module_id":"p3_d2_bruteforce_2","lifts":27,"L3":0,"image_orders":{"3000":9,"9000":18}},
  {"module_id":"p3_d2_bruteforce_3","lifts":27,"L3":0,"image_orders":{"3000":9,"9000":18}},
  {"module_id":"p3_d2_bruteforce_4","lifts":9,"L3":0,"image_orders":{"3000":1,"9000":8}},
  {"module_id":"p3_d2_bruteforce_5","lifts":81,"L3":0,"image_orders":{"3000":81}}]}
```

**追加の細粒度予言(同じ実測から取れる・より鋭い)**
- **P-L3-1**: $p=2$ の全 12 行で、像位数は **$\{3000,6000,12000,24000\}$ の 4 値しか出ない**。5 値目が出たら §B.4 が壊れている。
- **P-L3-2**: $p=2$ では **L-3 は拡大類の関数**(同一類の lift は全て同じ判定・同じ像位数)。行 4 の 16 個の成功は**ちょうど 1 つの類の全 lift**であること。
- **P-L3-3**: $p=3$ では **L-3 は lift 依存**(同一類内で $9:18$ に割れる)。行 13 で「1 類・27 lift・うち 18 が成功」。
- **P-L3-4**: **L-3 ⟺ $\lvert\mathrm{im}\,\rho\rvert=3000\cdot\lvert V\rvert$**(常に)。
- **P-L3-5**: 行 2・9(= $E$ のみの行)は $\lvert V\rvert=4,16$ なのに像位数が 6000 止まり ⟹ **$E$ 成分は head に決して届かない**の直接観測。

## B.6 D⊕D が 0 で $\mathbf F_2\oplus D$ が非 0 になる構造的理由(最初の検算例)

**(i) $D\oplus D$(行 7)**: $\rho|_R$ の 2 成分は $\mathrm{Hom}_{\widehat G_5}(M_R,D)$ の元だが、
$$\dim_{\mathbf F_2}\mathrm{Hom}_{\widehat G_5}(M_R,D)=\underbrace{\bigl[\dim H^1(\Gamma,D)-\dim H^1(\widehat G_5,D)\bigr]}_{=1-1=0}+\underbrace{\dim\ker\bigl(H^2(\widehat G_5,D)\to H^2(\langle u\rangle,D)\oplus H^2(\langle w\rangle,D)\bigr)}_{=1-0=1}=\mathbf 1 .$$
($H^2(C_2,D)=D^\theta/N_\theta D=0$、$H^2(C_3,D)=0$ ∵ $\lvert C_3\rvert$ と $\lvert D\rvert$ が互いに素。)
⟹ **2 成分は必ず $\mathbf F_2$-比例**($0$ か同一の $g$)⟹ 像は $0$ / $D$(対角)/ $D$(片側)のいずれかで、**位数 16 の $D\oplus D$ には決して届かない**。
同じことを $H^2$ 側で言えば: $\mathrm{Hom}_{\widehat G_5}(D\oplus D,D)=\mathbf F_2^2\to H^2(\widehat G_5,D)=\mathbf F_2$ は**次元の理由で単射になり得ない**。**これが 0/256 の全内容**であり、拡大類の値にも lift の選び方にも一切依存しない。

**(ii) $\mathbf F_2\oplus D$(行 4)**: head は $\mathbf F_2\oplus D$ = **非同型な 2 つの単純**。それぞれ重複度 1 なので上の衝突が起こらない。$\mathrm{Hom}(M_R,\mathbf F_2)$ と $\mathrm{Hom}(M_R,D)$ はどちらも 1 次元で、両方の生成元を同時に使えば $(f,g):M_R\to\mathbf F_2\oplus D$ は全射(非同型単純への射影が両方全射 ⟹ Goursat)。
⟹ L-3 $\iff$ $\varepsilon_{\mathbf F_2}\ne0$ **かつ** $\varepsilon_D\ne0$。受理類は $\varepsilon_{\mathbf F_2}\in\{0,\nu\}\times\varepsilon_D\in\{0,1\}$ の 4 個、条件を満たすのは **1 個**、その類の lift は 16 個 ⟹ **16/64**。

> ★ **一言でいう機構**: 「像 $\cap V$ = コサイクル値が生成する部分加群」は正しいが、**その部分加群は $M_R$ からの $\widehat G_5$-射の像**であり、各単純 $S$ について使える射の空間は**たかだか 1 次元**である。ゆえに **head に同じ単純が 2 回現れた瞬間に L-3 は恒偽**になる。$D\oplus D$ はその最小例、$\mathbf F_2^2$・$\mathbf F_2^3$・$\mathbf F_2^4$・$\mathbf F_2^2\oplus\cdots$ も同型。**$E$ は別の理由**(転送 $\mathrm{cor}=0$)で head に届かない。

## B.7 反証条件(予言が外れたら何を疑うか・順序つき)

| 観測 | 先に疑うもの |
|---|---|
| 像位数に第 5 の値が出る | §B.4 の「$\mathrm{Hom}(M_R,S)$ が 1 次元」= §B.3.2 の $H^1/H^2$ 値。**まず cert の `dim_H1_S4`/`dim_H2_S4` と突合**(そこは一致済なので、次は $\mathrm{res}$ の全射性 = $H^2(S_4;\mathbf F_2)\to H^2(C_2;\mathbf F_2)$) |
| 行 4 の 16 成功が 1 類に収まらない | $d_{\mathbf F_2}=d_D=0$(lift 非依存)が壊れている ⟹ $H^1(S_4,D)=\mathbf F_2$ の再検 |
| 行 13 が 0、または他の $p=3$ 行が非 0 | 行 1/2/3 の加群同定(§B.3.2 の $H^1/H^2$ による同定)⟹ `socle_structure` の `ordA/ordB/|image|` と突合 |
| $E$ 行で 12000 以上が出る | $\pi_*=\mathrm{cor}_{A_4}^{S_4}=0$(= $\mathrm{res}:H^2(S_4;\mathbf F_2)\twoheadrightarrow H^2(A_4;\mathbf F_2)$、二重被覆 $2.S_4\vert_{A_4}=SL(2,3)$ 由来)が偽 |
| lift 総数が 1263 でない | EMB-LIN か受理類の判定($\mathrm{res}$ to $\langle u\rangle,\langle w\rangle$)⟹ **§B.3.3 は cert と一致済なので実装側を先に疑う** |

---

## C. 【GAP】(埋めていない穴)

| # | 内容 | 状態 |
|---|---|---|
| **【TC-GAP-1】** | **432・486 の $\iota(N)\ne N$ は紙で未証明**。機械の witness word(cert 記載)だけが根拠 = **cross-checked**(2 系統)であって定理ではない | §A.5 の【文献要請】待ち / または個別の有限計算を Lean 化 |
| **【TC-GAP-2】** | 504×2・702 の Sylow 正規性、882 の Sylow 巡回性は **census cert の構造式**を入力にしている(指数だけからは出ない) | 許容(登録済 INVENTORY)。ただし「純紙 9 窓 / cert 入力 4 窓」の区別を消さないこと |
| **【TC-GAP-3】** | Part B は古典的事実を**再導出せず使用**: $H^*(S_4;\mathbf F_2)=\mathbf F_2[x_1,x_2,x_3]/(x_1x_3)$、$H^2(A_4;\mathbf F_2)=\mathbf F_2$、$2.S_4$ の存在、$H^*(C_3;\mathbf F_3)$ の Aut 作用 | 標準教科書事項。ただし**本稿の 17 行分の帰結は cert の $H^1/H^2$ 値と独立一致**しており、誤りなら cert 側と衝突するはず |
| **【TC-GAP-4】** | **仕様同一性(CV-9 型)**: 本稿の「L-3 $\iff\mathrm{im}\,\rho=\widehat{\mathcal P}$」という読みが、実装係の L-3 判定(`⟨ρσ1,ρσ2⟩ = P̂`)と**同一対象**であることは、非当事者(falsifier)の判読を経ていない | 予言表を実測と突合する**前に**判読を通すこと |
| **【TC-GAP-5】** | $M_R\cong\ker(\mathbf F_p[\widehat G_5]\to\mathbf F_p[\widehat G_5/u]\oplus\mathbf F_p[\widehat G_5/w])$ は Bass–Serre 経由の導出であり、階数 501 の数値検算以外の機械照合はしていない(**判定式は $M_R$ の明示形を使わない**ので影響は限定的) | 参考情報 |
| **【TC-GAP-6】** | Part A の補題群(PSL-GEN・MIRROR-PSL・MIRROR-ODD・ABEL-TYPE)と Part B の命題群は **すべて candidate**(Sol 監査未了)。**Lean 不使用 ⟹ verified ではない** | Sol 監査待ち |

## D. novelty grep(実施済・`docs/` 全域)

| 語 | 結果 |
|---|---|
| `MIRROR-ODD` / `PSL-GEN` / `MIRROR-PSL` / `L3-CRIT` / `ABEL-TYPE` | **0 hit**(全て本稿が初出) |
| `関係加群` / `relation module` / `正規閉包` | **0 hit** |
| `MIRROR-CRIT` / `MIRROR-OBSTRUCTION` / `ABEL-INDEX` | 既出(`twin_witness_prereg_iffirst_v1.md` §2)。**本稿はその強化であり置換ではない**(旧補題は $P$ 側・本稿は $\widehat P$ 側) |
| `PSL2` / `C_2*C_3` | 既出(`bu_s35_embedding_v1.md` §2 定理 EMB-C の帰結ほか)。**「$c\in N$ ⟹ $\widehat P$ が $(2,3)$-生成」を $\iota$ 判定に使う接続は未出** |
| `chirality` / `reflexible` / `dessin の鏡像` | `docs/scout/` に Nielsen 同値・braid 軌道の遠征記録あり。**chirality/reflexibility そのものは未出** ⟹ §A.5 で【文献要請】として起票 |

---

# F. 追補(2026-08-06)— 432/486 の地図同定と Conder census 照合

**追補の格**: 本節で参照する Conder census の数値は**司令塔が文献ゲート経由で降ろした第三者データ**であり、**証明の根拠ではなく標的の指示**として扱う(引用箇所に `[census]` と明記)。**私は原ファイルを読んでいない**(`scratchpad\conder\` は私の到達範囲外)。本節の**紙の主張は census を一切使わずに成立する**。

## F.1 辞書(定理・census 非依存)

> ### 命題 MAP-DICT(candidate・本稿)
> $c\in N$、$\widehat P=B_3/N=\langle U,W\rangle$($U=\Delta N$, $W=\delta N$, $U^2=W^3=1$)とする。
> **(a)** $\ \sigma_1N=W^{-1}U$ かつ $\ \mathrm{ord}(UW)=\mathrm{ord}(W^{-1}U)=\mathrm{ord}(\sigma_1N)=:n$。
> **(b)** 対応する orientably-regular map は
> $$\text{頂点次数 }3,\quad \text{面サイズ }n,\quad V=\tfrac{\lvert\widehat P\rvert}{3},\quad E=\tfrac{\lvert\widehat P\rvert}{2},\quad F=\tfrac{\lvert\widehat P\rvert}{n},\quad g=1+\tfrac{\lvert\widehat P\rvert}{2}\Bigl(\tfrac12-\tfrac1n-\tfrac13\Bigr).$$
> **(c)** $\ \boxed{\ \iota(N)=N\iff\text{この地図は reflexible}\ }$

**証明.** (a) $\delta^{-1}\Delta=\sigma_1$(§A.2 の (1.1))ゆえ $W^{-1}U=\sigma_1N$。$(W^{-1}U)^{-1}=U^{-1}W=UW$ ⟹ 位数一致。
(b) 標準対応: 回転群 $G=\langle R,S\mid R^p=S^q=(RS)^2=1,\dots\rangle$($R$=面回転, $S$=頂点回転, $RS$=辺の対合)。$S:=W$(位数 3 ⟹ 頂点次数 3)、$RS:=U$ ⟹ $R=UW^{-1}$、$\mathrm{ord}(R)=\mathrm{ord}(UW)=n$。$V=\lvert G\rvert/q$, $E=\lvert G\rvert/2$, $F=\lvert G\rvert/p$ と Euler。$U\ne1$, $W\ne1$ は $\widehat P\twoheadrightarrow S_3$ で $\Delta\mapsto$ 互換, $\delta\mapsto$ 3-巡回 から。
(c) $\Gamma=C_2\ast C_3$ 上で、地図の鏡映 $\rho_{\rm map}:R\mapsto R^{-1},S\mapsto S^{-1}$ と本稿の $\rho:U\mapsto U,W\mapsto W^{-1}$ は
$$\rho_{\rm map}=\mathrm{Inn}(W)\circ\rho$$
($\rho_{\rm map}(U)=\rho_{\rm map}(RS)=R^{-1}S^{-1}=WUW^{-1}$、$\rho_{\rm map}(W)=W^{-1}$ を確認)であり**内部自己同型ぶんしか違わない**。$\bar N\trianglelefteq\Gamma$ は内部自己同型で不変ゆえ $\rho$-不変 $\iff\rho_{\rm map}$-不変。補題 MIRROR-PSL と合わせて (c)。∎

> ★ **司令塔の翻訳は正しい**。さらに **$n$ は「$\sigma_1$ の像の位数」という工房の既存量**であることが分かった(census 行との突合キーはこれ)。

## F.2 我々の 2 窓の型(紙の絞り込み)

Euler の算術(整数演算スクリプトで検算):

| $\lvert\widehat P\rvert$ | $n$ | $V$ | $E$ | $F$ | genus |
|---|---|---|---|---|---|
| 486 | 6 | 162 | 243 | 81 | **1** |
| 486 | **18** | 162 | 243 | 27 | **28** |
| 486 | **54** | 162 | 243 | 9 | **37** |
| 486 | 162 | 162 | 243 | 3 | 40 |
| 432 | 6 | 144 | 216 | 72 | 1 |
| 432 | **8** | 144 | 216 | 54 | **10** |
| 432 | 12 | 144 | 216 | 36 | 19 |
| 432 | **24** | 144 | 216 | 18 | 28 |

**486 窓**: $\widehat P/S\cong C_2$($S=\mathrm{Syl}_3$)で $W\in S$, $U\notin S$ ⟹ $\sigma_1N\notin S$ ⟹ $n=2\cdot3^{j}$、$3^{j}=\mathrm{ord}(\bar x)$($\bar x=\sigma_1^2N\in P$, $\lvert P\rvert=81$)。
- $j=0$ ⟹ $\bar x=1\Rightarrow\bar y=\theta(\bar x)=1\Rightarrow P=1$ ✗。
- $j=4$ ⟹ $P=\langle\bar x\rangle$ 巡回 ⟹ 可換 ⟹ **補題 ABEL-TYPE**(§A.6)より $P\cong(\mathbf Z/n)^2$ 型で巡回になり得ない ✗。
- $j=1$($n=6$)⟹ genus 1 ⟹ 型 $\{3,6\}$ のトーラス地図 $\{3,6\}_{b,c}$、回転群位数 $6(b^2+bc+c^2)=486\Rightarrow b^2+bc+c^2=81$ の解は $(9,0),(0,9)$ **のみ**(検算済)⟹ $bc(b-c)=0$ ⟹ **reflexible** ⟹ 機械観測(chiral = M1)と矛盾 ✗。
$$\Longrightarrow\ \boxed{\ n\in\{18,\ 54\}\quad(\text{genus }28\ \text{または}\ 37)\ }$$

**432 窓**: 構造式 `(((C3xC3):Q8):C3):C2` が示唆する $P\cong(C_3\times C_3)\rtimes Q_8$(位数 72)を仮定すると、$\bar x,\bar y$ の $P/O_3(P)\cong Q_8$ での像は $Q_8$ を生成 ⟹ **$Q_8$ の生成対は必ず位数 4 の 2 元**($\Phi(Q_8)=\{\pm1\}$)⟹ $4\mid\mathrm{ord}(\bar x)$、$\mathrm{ord}(\bar x)\mid\exp(P)\mid12$ ⟹ $\mathrm{ord}(\bar x)\in\{4,12\}$。
$$\Longrightarrow\ \boxed{\ n\in\{8,\ 24\}\quad(\text{genus }10\ \text{または}\ 28)\ }$$
($n=6$ は $b^2+bc+c^2=72$ が**無解**ゆえ紙で排除済。)

> ### ★ 一致(census 側との突合)
> `[census]` の chiral **C10.1 = order 432 / type {3,8} / genus 10** は、私が独立に計算した $(m,n)=(432,8)\Rightarrow g=10$ と**完全一致**。
> `[census]` の chiral **C28.2 = order 486 / type {3,18} / genus 28** も $(486,18)\Rightarrow g=28$ と**完全一致**。
> ⟹ **432 窓の第一候補は C10.1**($n=8$)、**486 窓の第一候補は C28.2**($n=18$)。ただしこれは**同定ではない**($n$ を実測していない・同型の型に複数行がありうる)。

## F.3 ★★★ 重大な警告 — census の「order」規約(再抽出せずに使ってはならない)

Conder 系のリストは各項の `Order` に **自己同型群の位数**を書く。向き付け可能面上の regular map では
$$\text{chiral: }\lvert\mathrm{Aut}\rvert=\lvert\mathrm{Rot}\rvert=2E,\qquad \textbf{reflexible: }\lvert\mathrm{Aut}\rvert=2\lvert\mathrm{Rot}\rvert=4E .$$
我々の窓は $\mathrm{Rot}=\widehat P$ で $\lvert\widehat P\rvert=2E$。したがって

$$\boxed{\ \textbf{我々の窓の reflexible 版は「order 486」ではなく「order 972」、「order 432」ではなく「order 864」の行に載る。}\ }$$

- **規約の裏づけ(私の独立計算)**: `[census]` の chiral 2 件(C10.1 @432 / C28.2 @486)は、**$\lvert\mathrm{Rot}\rvert=2E$ 規約のときだけ** genus 10 / 28 と整合する(F.2 の表)。⟹ chiral 側は $2E$ 規約で確定 ⟹ reflexible 側は $4E$ 規約である公算が高い。
- **帰結**: 「**位数 486 に reflexible 0 件**」は、**「$E=243$ の reflexible が無い」の証拠にならない**(そもそもその bucket には載らない)。同様に「位数 432 に reflexible 44 件」は $E=108$(回転群位数 216)の地図群であり、**我々の窓とは別物**の公算が高い。
- 私の紙側からの傍証: §F.4 の構成が正しければ、**$E=243$ の reflexible 地図は実在する**(= 「0 件」は規約由来の見かけ)。

> ### 再抽出スペック(司令塔へ・これだけあれば決着)
> 1. **order 972**(= $4E$, $E=243$)の **reflexible** 行を、**type $\{3,18\}$ と $\{3,54\}$** に限って列挙(genus 28 / 37)。
> 2. **order 864**(= $4E$, $E=216$)の **reflexible** 行を、**type $\{3,8\}$ と $\{3,24\}$** に限って列挙(genus 10 / 28)。
> 3. 併せて **order 486 の chiral 11 件の type 分布**($\{3,18\}$ と $\{3,54\}$ が何件ずつか)と **order 432 の chiral 24 件の type 分布**($\{3,8\}$/$\{3,24\}$)。
> 4. 各行の**回転群の同定情報**(あれば `SmallGroup` ID / 構造)— これが `[432,734]` / `[486,39]` と突合できれば**窓の一意同定**になる。
> - **1,2 が真に空**であって初めて「我々の 2 窓は chiral」の第三者裏づけになる(それでも**格は third-party 照合**であって証明ではない)。

## F.4 委嘱(2)への回答 — 「486 に reflexible な (2,3)-生成が無い」は**たぶん偽**(証明を試みて逆を見つけた)

**(i) 紙の障害論法は $q=3$ 側へ延びない(理由が特定できた).**
486 窓では $S:=\mathrm{Syl}_3(\widehat P)=\widehat P_0=\langle W,\,UWU\rangle$(§A.5)。§A.3 の障害は「特性切片 $A$($\mathrm{Aut}(A)$ 可換)に $W$ が非自明に作用する」ことを使うが、
$$\text{$S$ の下降中心列の因子 }\gamma_i(S)/\gamma_{i+1}(S)\ \text{は定義により $S$ に中心化される}\ \Longrightarrow\ \mu(W)=1 .$$
$W\in S$ である以上、**$S$ 由来の可換自己同型群をもつ特性切片からは障害が原理的に出ない**。$q\ge5$ のときは $W\in\widehat P_0$ が $A$ の**外**にいて初めて $\mu(W)\ne1$ が出ていた。⟹ **§A.3 の機構は $q=3$ では構造的に失効する**(単なる技術的不足ではない)。

**(ii) 逆に reflexible な例を作れる(構成).**
$F:=C_3\ast C_3=\langle w,w'\rangle$ とし、$\rho_0:w\mapsto w^{-1},w'\mapsto w'^{-1}$、$\tau_0:w\leftrightarrow w'$ と置く。どちらも $\mathrm{Aut}(F)$ の元で、生成元上で $\rho_0\tau_0=\tau_0\rho_0$。$M\trianglelefteq F$ を**特性部分群**とし $R:=F/M$ と置くと $\rho_0,\tau_0$ は $R$ に降り、
$$G:=R\rtimes\langle\tau\rangle\quad(\tau^2=1)$$
は $G=\langle\tau,\ w\rangle$、$\tau^2=w^3=1$ で **(2,3)-生成**、$\lvert G\rvert=2\lvert R\rvert$、かつ $\beta:=\rho\rtimes\mathrm{id}$ が $\beta(\tau)=\tau,\ \beta(w)=w^{-1}$ を与える ⟹ **reflexible**。
⟹ **$\lvert R\rvert=243$ なる特性商 $R$ が 1 つでもあれば、位数 486 の reflexible (2,3)-生成群が存在する**(= 委嘱 (2) の標的命題は偽)。
候補: $R=F/\gamma_4(F)$。次数別に $\gamma_1/\gamma_2=C_3^2$(位数 9)、$\gamma_2/\gamma_3=C_3$(位数 3・$[w^3,w']=1$ から $[w,w']^3\in\gamma_3$)、$\gamma_3/\gamma_4$ は $(\mathbf Z/3)^2$ の商(自由 Lie 環の 3 次は階数 2)⟹ $\lvert R\rvert\le3^5=243$、下界は $C_3\wr C_3$(位数 81・class 3・位数 3 の 2 元で生成)。
$$\boxed{\ \textbf{未決の 1 ビット: }\lvert(C_3\ast C_3)/\gamma_4\rvert\ \text{は}\ 243\ \text{か}\ 81\ \text{か}\ }$$
$p=3$・class 3 では Lazard 対応が効かない(class $<p$ が必要)ため、$w^3=w'^3=1$ が 3 次成分を潰す可能性を紙で排除できない。**GAP 3 行(`NilpotentQuotient` / `LowerCentralSeries`)で決着する**ので、実装係に投げるのが最短。

**(iii) 結論(委嘱 (2) への回答)**: 「位数 486 に reflexible な (2,3)-生成群は存在しない」は、(ii) の構成があるため**一般命題としては成立しない見込み**。正しい標的は**型を固定した命題**:
> **標的 T-486**: 「$E=243$・型 $\{3,18\}$(または $\{3,54\}$)の **reflexible** orientably-regular map は存在しない」
これなら census(order 972・type 制限)で真偽が判定でき、真なら我々の 486 窓の chiral 性が第三者裏づけを得る。**なお (ii) の構成が与える reflexible 群の型 $n=\mathrm{ord}(\tau w)$ は別に計算する必要があり、$\{3,18\}$ とは限らない**(むしろ小さい $n$ になる公算)。

## F.6 再抽出後の場合分け(固定・2026-08-06 追補 2)

`[census]`(第三者・司令塔再抽出・**証明ではない**)で判明した事実:

| E | type | reflexible(order $4E$ 棚) | chiral(order $2E$ 棚) |
|---|---|---|---|
| 243 | $\{3,18\}$ | **R28.3** `{3,18}_18` genus 28(**1 件実在**) | **C28.2** genus 28 |
| 243 | $\{3,54\}$ | **該当ゼロ** | (未報告) |
| 216 | $\{3,8\}$ | **ゼロ** | **C10.1** genus 10 |
| 216 | $\{3,24\}$ | **R28.5** 実在 | (未報告) |

★ **私の §F.3 の規約警告は当たり**($E=243$ で reflexible と chiral が**同じ辺数で併存**)。同時に **§F.4 (ii) の構成 $R\rtimes\langle\tau\rangle$ は R28.3 の実在で裏づけ**られた ⟹ 「位数 486 に reflexible な (2,3)-生成は無い」路線は**確定的に死亡**(私の見立てどおり)。

> ### 場合分け($n=\mathrm{ord}(\sigma_1N)$ の実測待ち・紙側はここで固定)
>
> | 窓 | $n$ | genus | census の帰結 | 我々がすべきこと |
> |---|---|---|---|---|
> | **432** | **8** | 10 | $\{3,8\}$/$E{=}216$ に **reflexible が 1 件も無い** ⟹ **どの群であれ chiral が強制**される | **完了**。$\iota(N)\ne N$ の**独立第三者裏づけ**が成立(格: third-party 照合) |
> | **432** | **24** | 28 | R28.5(reflexible)が併存 | **同定が必要** ⟹ §F.7 |
> | **486** | **18** | 28 | R28.3 と C28.2 が併存 | **同定が必要** ⟹ §F.7 |
> | **486** | **54** | 37 | $\{3,54\}$/$E{=}243$ に **reflexible ゼロ** ⟹ **chiral 強制** | **完了**(同上) |
> | いずれか | 上記以外 | — | 紙の絞り込み(§F.2)が破れている | **STOP**。$P$ の構造読み(432)・ABEL-TYPE 適用(486)・census 完全性のどれかを再検分 |
>
> **強制ケースの論理**(重要): 「型 $\{3,n\}$・辺数 $E$ の reflexible 地図が census(悉皆域内)に 1 件も無い」+「我々の窓はその型・その辺数の地図である」(命題 MAP-DICT)⟹ **我々の窓は reflexible ではない = $\iota(N)\ne N$**。**群の同定は不要**で、$n$ の 1 値だけで閉じる。これが最も価値の高い決着経路。

### F.6.1 $n$ の紙側予言(実測で反証可能)

- **432**: $P\cong(C_3\times C_3)\rtimes Q_8$ で **$Q_8$ の作用が忠実**なら、位数 4 の元は $O_3(P)=C_3^2$ 上**固定点自由**($SL(2,3)$ の位数 4 元の固有値は $\pm i\notin\mathbf F_3$)⟹ $P$ に位数 12 の元は無い ⟹ $\mathrm{ord}(\bar x)=4$ ⟹ $\boxed{n=8}$ ⟹ **強制ケース**。逆に作用の核が $Z(Q_8)$ を含めば $n=24$ もありうる。
  $$\Longrightarrow\ \textbf{予言 P-MAP-1}:\ n_{432}=8\ (\text{genus }10,\ =\text{C10.1 の型}).$$
- **486**: 構造式 `((C9:C9):C3):C2` は $\exp(\mathrm{Syl}_3(\widehat P))=9$ を示唆。$\exp=9$ なら $\mathrm{ord}(\bar x)\in\{3,9\}$、$3$ は §F.2 で排除済 ⟹ $\boxed{n=18}$ ⟹ **同定ケース**。
  $$\Longrightarrow\ \textbf{予言 P-MAP-2}:\ n_{486}=18\ (\text{genus }28,\ \text{C28.2 / R28.3 の型}).$$

### F.6.2 ★ 実測着弾(2026-08-06・機械値)— 予言 2 本とも的中

| 量 | 実測 | 予言 | 判定 |
|---|---|---|---|
| $\mathrm{ord}(\sigma_1N)$ @432(両 member) | **8 / 8** | P-MAP-1: **8** | **的中** |
| $\mathrm{ord}(\sigma_1N)$ @486(両 member) | **18 / 18** | P-MAP-2: **18** | **的中** |
| $\lvert(C_3\ast C_3)/\gamma_4\rvert$ | **243**(進行 9/27/243/2187) | §F.4 の 2 択のうち **243** | **的中(2 択の上側)** |

**帰結(確定)**:
1. **432 窓 = 型 $\{3,8\}$・$E=216$・genus 10。** `[census]` は $E=216$・$\{3,8\}$ の reflexible を(悉皆域内で)**ゼロ**と報告 ⟹ **どの群であれ chiral が強制** ⟹ $\iota(N)\ne N$ の**第三者裏づけ成立**(格 = third-party 照合)。**群の同定は不要**。
   - 副次の紙の帰結: $n=8\Rightarrow\mathrm{ord}(\bar x)=4\Rightarrow P$ に位数 12 の元なし ⟹ (§F.6.1 の議論が逆向きに効いて)**$Q_8$ の $O_3(P)$ への作用は忠実**、$P\cong(C_3\times C_3)\rtimes Q_8$ の読みが**追認**された。
2. **486 窓 = 型 $\{3,18\}$・$E=243$・genus 28。** R28.3(reflexible)と C28.2(chiral)が併存 ⟹ **純粋な同定問題**(§F.7・§F.9)。
3. **$\lvert F/\gamma_4\rvert=243$** ⟹ §F.4 (ii) の $G_R:=\bigl((C_3\ast C_3)/\gamma_4\bigr)\rtimes\langle\tau\rangle$ は**位数 486 の reflexible な (2,3)-生成群として実在** ⟹ 委嘱 (2) の当初標的「位数 486 に reflexible な (2,3)-生成は存在しない」は**確定的に偽**(私の §F.4 の見立てどおり)。

> ### ★ 予言 P-MAP-3(同定の見通し・**警告つき**)
> $G_R$ の型を計算すると $U=\tau,\ W=w$ で $(UW)^2=w'w$ ⟹ $n_{G_R}=2\cdot\mathrm{ord}(ww')$。$R$ 内で $w^3=w'^3=[w,w']^3=1$(∵ $[w^3,w']=1$ の class-3 展開)ゆえ $(ww')^3\in\gamma_3(R)$ で、$\gamma_3(R)\cong C_3^2\ne1$ ⟹ **$\mathrm{ord}(ww')=9$ が期待され $n_{G_R}=18$**。
> $$\Longrightarrow\ \boxed{\ \textbf{R28.3 の回転群}\ \cong\ \bigl((C_3\ast C_3)/\gamma_4\bigr)\rtimes C_2\ \textbf{(候補)}\ }$$
> **警告**: $R$ の構造は「位数 243・2 生成・$\gamma$ 階数 $(9,3,9)$・exp 9」で、cert の $\mathrm{Syl}_3(\widehat P_{486})=$ `(C9:C9):C3` と**同じ外形**である。⟹ **$\mathrm{Rot}(\text{R28.3})\cong\mathrm{Rot}(\text{C28.2})\cong\widehat P_{486}=[486,39]$ が起こりうる**。そのとき **IdGroup 比較は原理的に決定力ゼロ**になる(掌性は群でなく**標識対**の性質)。指示書はこの分岐を必ず持つこと。

## F.7 実測指示書 **MAP-ID-1**(数学者 → 実装係。§F.6 の同定ケースのみ発火)

**目的**: 我々の窓の地図が census のどの行か確定する。**IdGroup 一致は必要条件にすぎない**(同型な回転群をもつ chiral 行と reflexible 行は**併存しうる** — 掌性は群でなく**標識づけられた生成対**の性質)。決定的なのは **marked pair の同値**である。

**Step 0(無料カナリア・全ケースで先に走らせる)**
$$\widehat P\ \text{内で}\ R_w:=\sigma_1N,\quad S_w:=(\sigma_1\sigma_2)N\quad\Longrightarrow\quad (R_wS_w)^2=1,\ \ R_wS_w\ne1 .$$
(紙: $R_wS_w=\sigma_1^2\sigma_2N$ で、$B_3$ 内の恒等式 $\boxed{(\sigma_1^2\sigma_2)^2=c}$ が成り立つ — 検算: $\sigma_1\sigma_2\sigma_1^2\sigma_2=(\sigma_2\sigma_1\sigma_2)\sigma_1\sigma_2=\sigma_2\sigma_1\sigma_2\sigma_1\sigma_2$ ⟹ 両辺に $\sigma_1$ を左から付けて $c=(\sigma_1\sigma_2)^3$ と一致。)
落ちたら **STOP**(規約か窓構成が壊れている)。

**Step 1(必須・最軽量)**: $n:=\mathrm{Order}(R_w)$ を両窓で測り、$\mathrm{Order}(S_w)=3$ と $\lvert\widehat P\rvert\in\{432,486\}$ も記録。⟹ §F.6 の表で分岐。

**Step 2(同定ケースのみ)**:
1. census 行の *defining relations* から有限表示群 `Grow` を作る。**注意**: reflexible 行の表示は**全自己同型群(位数 $4E$)**のことがある ⟹ `Size(Grow)` を必ず表示し、$4E$ なら**回転部分群(指数 2・$\langle R,S\rangle$)**を取ってから使う。位数が $2E$ になっていることを確認してから次へ。
2. 型の向き(双対)に注意: census の $\{p,q\}$ = (面サイズ, 頂点次数)。我々の地図は**頂点次数 3・面サイズ $n$** なので、行が $\{3,n\}$ なら**双対対応**で $R\mapsto S_w,\ S\mapsto R_w$、行が $\{n,3\}$ なら $R\mapsto R_w,\ S\mapsto S_w$。
3. 決定テスト(4 通りを試すだけ):
   ```
   for (imR,imS) in [ (Rw,Sw), (Sw,Rw), (Rw^-1,Sw^-1), (Sw^-1,Rw^-1) ]:
       f := GroupHomomorphismByImages(Grow, Phat, [R,S], [imR,imS]);
       if f <> fail and IsBijective(f) then  -> この行の地図と一致
   ```
   ★ **Aut 軌道を走査する必要はない**: 地図の同型 = 「標識対を対応させる同型の存在」そのものなので、**我々の specific pair 1 組を試せば十分**。
4. 期待される結果と**反証条件**:
   - **chiral 行(C28.2 / C10.1)と一致 ⟹ 我々の機械結果と整合**(第三者裏づけ)。
   - **reflexible 行(R28.3 / R28.5)と一致 ⟹ 重大な矛盾** ⟹ 直ちに **STOP** し、裁定 602 の witness word(MC-1 の $\rho(\iota(w))\ne1$)を再検算する。**これは本当に risk を負うテスト**であり、通れば価値がある。
   - **どの行とも一致しない ⟹ STOP**(census 完全性 or 型の同定 or 窓構成のいずれかが誤り)。
5. 記録: `Size(Grow)`・IdGroup 両者・成功した組合せ・失敗した組合せ(全部)。cert 化は不要、報告文で足りる。

**費用見積**: Step 0/1 は各窓で数秒(既存 scope2 の窓構成をそのまま使う)。Step 2 は位数 $\le486$ の有限表示群 1〜2 個の `Size`+同型判定 ⟹ 数秒〜数十秒。**GAP `-o 2g` で足りる。**

## F.8 実測指示書 **MAP-ID-2**(486 窓の同定・数学者 → 実装係・確定版)

**前提**: $\widehat P:=\widehat P_{486}=B_3/N$(pair `b2bef4dba95b` の A 側)、$\mathrm{IdGroup}=[486,39]$、$R_w:=\sigma_1N$($\mathrm{ord}=18$・実測済)、$S_w:=(\sigma_1\sigma_2)N$($\mathrm{ord}=3$)、$(R_wS_w)^2=1$(§F.7 Step 0 のカナリア)。

> ### ★ Test ORB(**主経路・census 表示を必要としない・これだけで決着する**)
> $\widehat P$ の内部だけで完結する。
> 1. `A := AutomorphismGroup(Phat);`(位数 486 の可解群 ⟹ 数秒)
> 2. 型 $\{3,18\}$ の**標識対を全列挙**:
>    $$\mathcal M:=\{(r,s)\ :\ \mathrm{ord}(r)=18,\ \mathrm{ord}(s)=3,\ (rs)^2=1,\ rs\ne1,\ \langle r,s\rangle=\widehat P\}$$
> 3. $\mathcal M$ を $A$-軌道に分ける(`OrbitsDomain(A, M, OnPairs)` 相当)。**軌道の個数 = 回転群が $\widehat P$ である型 $\{3,18\}$ の地図の個数**。
> 4. 各軌道の代表 $(r,s)$ について **reflexible 判定**:
>    $$\exists\alpha\in A:\ \alpha(r)=r^{-1}\ \wedge\ \alpha(s)=s^{-1}\quad(\text{= reflexible})$$
>    (`ForAny(A, a -> r^a = r^-1 and s^a = s^-1)`。$\lvert A\rvert$ が大きければ `RepresentativeAction` 2 段でも可)
> 5. **我々の対 $(R_w,S_w)$ がどの軌道に入るか**を記録。
>
> **期待される出力(= `[census]` との突合)**: `[census]` は $E=243$・$\{3,18\}$ に **chiral 1 件(C28.2)+ reflexible 1 件(R28.3)** と報告している。両者の回転群がともに $\widehat P$ なら **軌道は 2 個・うち 1 個が reflexible・1 個が chiral** となり、**我々の対は chiral 軌道に入る**はずである。
>
> **反証条件(全部 STOP 対象)**:
> - 我々の対 $(R_w,S_w)$ が **reflexible 軌道**に入った ⟹ **裁定 602 の witness word と正面衝突** ⟹ 直ちに STOP・MC-1 の $\rho(\iota(w))\ne1$ を再検算。
> - 軌道が 1 個しか無い ⟹ $\mathrm{Rot}(\text{R28.3})\not\cong\widehat P$ ⟹ 予言 P-MAP-3 が外れただけで**矛盾ではない**(このときは IdGroup 比較が決定力をもつ ⟹ Test PRES へ)。
> - 軌道が 3 個以上、または reflexible 軌道が 0/2 個 ⟹ census の完全性か型の同定を再検分。
>
> ★ **この test の価値**: 掌性を **witness word とは完全に別経路**($\mathrm{Aut}(\widehat P)$ の直接探索)で再導出し、同時に census の件数と突き合わせる。**二系統性が上がる**(ただし同一 GAP プロセス内なので格は cross-checked 止まり)。

> ### Test PRES(補助・census の *Defining relations* を使う経路)
> 1. census 行 **R28.3** と **C28.2** の defining relations から有限表示群を作る。`Size` を必ず出力: **$972$ なら全自己同型群**(reflexible 行の慣例)⟹ **回転部分群(指数 2)を取ってから**使う。$486$ になっていることを確認。
> 2. `IdGroup` を両方出す。**$[486,39]$ と一致するか**を記録(※ 一致しても**同定は完了しない** — 予言 P-MAP-3 の警告参照。**不一致なら排除できる**という片側の効力のみ)。
> 3. 決定テスト(標識対の同値・4 通り):
>    ```
>    for (imR,imS) in [ (Sw,Rw), (Rw,Sw), (Sw^-1,Rw^-1), (Rw^-1,Sw^-1) ]:
>        f := GroupHomomorphismByImages(Grow, Phat, [R,S], [imR,imS]);
>        if f <> fail and IsBijective(f) then -> この行の地図と一致
>    ```
>    (census の型 $\{p,q\}$ =(面サイズ, 頂点次数)。我々は頂点次数 3・面 18 ⟹ 行が $\{3,18\}$ なら **双対対応** $R\mapsto S_w,\ S\mapsto R_w$ が第一候補。)
> 4. **期待**: C28.2 で成功・R28.3 で失敗。逆なら **STOP**。
>
> ### 追加(無料・432 窓でも同じ Test ORB を回す)
> 型 $\{3,8\}$($\mathrm{ord}(r)=8,\ \mathrm{ord}(s)=3,\ (rs)^2=1$)で軌道を取り、**全軌道が chiral** であることを確認する。`[census]`(order 864 棚に $\{3,8\}$ reflexible ゼロ)と整合するはずで、整合すれば **432 の census 強制**が我々の側からも裏づけられる。

**費用**: いずれも位数 $\le486$ の群 1 個の `AutomorphismGroup` と数万対の走査 ⟹ 数秒〜1 分。`gap.ps1 -o 2g` で足りる。**cert 化は不要**(報告文に軌道数・reflexible 軌道の有無・我々の対の所属を書けばよい)。

## F.5 追加の【GAP】

| # | 内容 | 状態 |
|---|---|---|
| **【TC-GAP-7】** | 2 窓の $n=\mathrm{ord}(\sigma_1N)$ | **閉**(実測 432→8・486→18。紙の予言 P-MAP-1/2 と一致・§F.6.2) |
| **【TC-GAP-8】** | census の order 規約(reflexible = $4E$) | **実質閉**(再抽出で $E=243$ の reflexible が order 972 棚に実在=R28.3。凡例逐語も 2E/4E と整合)。ただし**私は原ファイル未読**ゆえ格は third-party |
| **【TC-GAP-9】** | $\lvert(C_3\ast C_3)/\gamma_4\rvert$ | **閉 = 243**(nq 実測)⟹ §F.4 (ii) の reflexible 構成は実在 |
| **【TC-GAP-10】** | 432 の $P\cong(C_3\times C_3)\rtimes Q_8$ は構造式からの読み | **傍証追加**($n=8$ ⟹ 位数 12 の元なし ⟹ $Q_8$ 作用忠実と整合)。厳密には未閉だが、**432 の結論は $n=8$ だけに依存し $P$ の同定に依存しない** |
| **【TC-GAP-11】** | **486 窓が C28.2 か R28.3 か**(純粋な同定問題)。我々の側の答え($\iota(N)\ne N$ ⟹ C28.2)は機械 2 系統で出ているが、census 行との**突合は未実行** | **§F.8 MAP-ID-2 を実装係へ**(Test ORB が主経路) |
| **【TC-GAP-12】** | $\mathrm{Rot}(\text{R28.3})\cong\bigl((C_3\ast C_3)/\gamma_4\bigr)\rtimes C_2$ か(予言 P-MAP-3)。真なら **IdGroup 比較は決定力ゼロ**になり Test ORB / Test PRES の標識対テストが必須 | 未検証(§F.8 で同時に判明する) |

## F.10 ORB 実測の判読(2026-08-06 追補 3・確定)

**実測**: 486 — $\lvert\mathrm{Aut}\widehat P\rvert=1458$、$\lvert\mathcal M\rvert=2916$、**軌道 2・両方 reflexible=FALSE**、我々の対は orbit1。
432 — $\lvert\mathrm{Aut}\widehat P\rvert=432$、$\lvert\mathcal M\rvert=864$、**軌道 2・両方 chiral**、我々の対は orbit1。**STOP 条項は不発。**

### F.10.1 算術カナリア(実測が自動で通した検査)

生成対の $\mathrm{Aut}$-固定化群は**常に自明**(生成元を固定する自己同型は恒等)⟹ **全軌道の長さ $=\lvert\mathrm{Aut}\widehat P\rvert$**。実測は
$$2916=2\cdot1458,\qquad 864=2\cdot432$$
で **軌道数 $=\lvert\mathcal M\rvert/\lvert\mathrm{Aut}\rvert=2$ ちょうど**。⟹ 列挙・軌道分解は整合(壊れていれば端数が出る)。

### F.10.2 判読① — 「chiral 1 枚 = 2 軌道」は**論理的に強制**(追試不要)

$\nu:\mathcal M\to\mathcal M,\ (r,s)\mapsto(r^{-1},s^{-1})$ と置く。**well-defined**: $\mathrm{ord}$ は保存、$sr=s(rs)s^{-1}$ ゆえ $\mathrm{ord}(sr)=\mathrm{ord}(rs)=2$ ⟹ $(r^{-1}s^{-1})^2=((sr)^2)^{-1}=1$、$\langle r^{-1},s^{-1}\rangle=\langle r,s\rangle$ ✓。$\nu^2=\mathrm{id}$、かつ $\nu$ は $\mathrm{Aut}$-作用と**可換**($\alpha(r^{-1})=\alpha(r)^{-1}$)⟹ $\nu$ は**軌道集合の対合**。

$$\boxed{\ \text{軌道 }O\ \text{が reflexible}\iff\nu(O)=O\ }\qquad\Longrightarrow\qquad \text{chiral 軌道は }\nu\text{ で 2 個ずつ対になる}.$$

⟹ 軌道が 2 個で**どちらも $\nu$-固定でない**なら、$\nu$ は 2 軌道を**入れ替えるしかない**。⟹ 「2 軌道 = 1 枚の chiral 地図とその鏡像」は**実測から論理的に従う**(司令塔の仮読みは正しい・**追試 1 行は論理的には不要**)。
> ★ ただし**バグ検出用の無料カナリア**としては有用: $\nu(R_w,S_w)=(R_w^{-1},S_w^{-1})$ が **orbit2** に入ることを 1 行で確認せよ。orbit1 に入れば「reflexible=FALSE」判定が壊れている(述語が $\mathrm{Inn}$ しか探していない等)。**論理の補強ではなく実装の検温**として推奨。

### F.10.3 判読② — 「reflexible 軌道ゼロ ⟹ $\iota(N)\ne N$」は**厳密**(census 非依存)

MAP-DICT を経由する必要すらない。$S:=W=\delta N$、$R:=UW^{-1}$、$U=RS$、我々が測った対は $(R_w,S_w)=(\sigma_1N,\ \delta N)=(W^{-1}U,\ W)=(R,S)^{W^{-1}}$(共役)。

> **補題 REFL-EQUIV(candidate・本稿)**
> $$\exists\alpha\in\mathrm{Aut}(\widehat P):\ \alpha(R)=R^{-1},\alpha(S)=S^{-1}\iff\exists\beta\in\mathrm{Aut}(\widehat P):\ \beta(U)=U,\beta(W)=W^{-1}.$$
> **証明.** ($\Leftarrow$) $\alpha:=\mathrm{Inn}(W)\circ\beta$。$\beta(R)=\beta(U)\beta(W)^{-1}=UW$、$W(UW)W^{-1}=WU=R^{-1}$ ✓;$\beta(S)=W^{-1}$、$W W^{-1}W^{-1}=W^{-1}=S^{-1}$ ✓。
> ($\Rightarrow$) $\alpha(U)=\alpha(RS)=R^{-1}S^{-1}=(SR)^{-1}$、$SR=WUW^{-1}$ かつ $U^2=1$ ゆえ $(SR)^{-1}=WUW^{-1}$。$\beta:=\mathrm{Inn}(W^{-1})\circ\alpha$ とすると $\beta(U)=U$ ✓、$\beta(W)=W^{-1}$ ✓。∎

右辺は**補題 MIRROR-PSL の判定条件そのもの**。ゆえに
$$\boxed{\ \text{我々の対の軌道が reflexible でない}\iff\iota(N)\ne N\ }$$
⟹ **ORB 実測は $\iota(N)\ne N$ の直接証明(census 完全に非依存)**。432 の「census 強制」も**降格不要でそのまま自前の結果**になった。

**格の限定**: ORB は「witness word 1 本」とは**別方法**($\mathrm{Aut}$ 悉皆)だが、窓 $\widehat P$ の構成は scope2 と**同じ系統**であり、同一 GAP プロセス内。⟹ **cross-checked が上限**(Lean 不使用ゆえ verified ではない)。**census は third-party の echo(独立確認)であって根拠ではない** — 逆に、我々の結果が census の件数(chiral 1 / reflexible 1 @{3,18}、reflexible 0 @{3,8})と**独立に整合した**ことが相互の信頼度を上げる。

### F.10.4 判読③ — census 側への逆情報(我々から third-party へ)

486 で $\widehat P$ 上に reflexible 軌道が**ゼロ** ⟹ `[census]` の **R28.3 の回転群は $[486,39]$ と非同型**(同型なら reflexible 軌道が 1 個以上必要)。⟹ 予言 P-MAP-3 は**修正して残す**:
> **P-MAP-3′(検証は任意)**: $\mathrm{Rot}(\text{R28.3})\cong G_R:=\bigl((C_3\ast C_3)/\gamma_4\bigr)\rtimes C_2$ であり、**$G_R\not\cong[486,39]$**。
> 検証手順(2 行): `nq` で $R=(C_3\ast C_3)/\gamma_4$(位数 243)を作り $\tau$($w\leftrightarrow w'$)で半直積 ⟹ `IdGroup` を出す。$[486,39]$ でなければ P-MAP-3′ の前半と整合、さらにその群で ORB を回して reflexible 軌道が出れば確定。

## F.9 MIRROR-ALL 現況(一行)

$$\boxed{\ \textbf{15 対}\ =\ \underbrace{\textbf{13}}_{\substack{\text{紙の定理}\\ \text{MIRROR-ODD}}}\ +\ \underbrace{\textbf{2}}_{\substack{\text{432 / 486: 機械 2 方法}\\ \text{(witness word + ORB 軌道悉皆)}\\ \text{cross-checked}}}\qquad\text{[census = third-party echo・根拠ではない]}\ }$$

**格の確定(2026-08-06)**:
- **紙単独の射程は 13/15**(定理 MIRROR-ODD)。ここは変わらない。
- 残り 2 窓は **cross-checked**: ①裁定 602 の witness word($\rho(\iota(w))\ne1$・GAP + python MC-1)、②**ORB 軌道悉皆**($\mathrm{Aut}(\widehat P)$ 内に $(r,s)\mapsto(r^{-1},s^{-1})$ を実現する $\alpha$ が**存在しない**ことの悉皆確認)。②は①と**方法が独立**で、補題 REFL-EQUIV(§F.10.3)により $\iota(N)\ne N$ と**厳密に同値**。
- `[census]` は **third-party echo**(件数と型が独立に整合)。**証明の根拠として引かない。**
- ⟹ 「この帯の双子対は全て鏡映対」= **cross-checked(not verified)**。**定理と呼べるのは 13 対**。Lean 化するなら残り 2 窓の ORB 判定(有限群の悉皆)が対象。

---

# G. 追補(2026-08-06)— 層別 exotic 双子地図(発案札 β-1 の検分つき)

**委嘱**: 司令塔「`docs/notes/exotic_twin_absence_ideation_v1.md` 札 β-0/β-1 の検分」。**判定: PASS(主張は正しい)。ただし射程の訂正 1 件と、札が自分で過小評価している上位発見 1 件を付す。**

## G.1 検分(5 点)

**① 混在 5 対の実在と意味** — `search/certs/lins_twin_census_v1_20260806.json` を直接読んで確認(読取りのみ):

| 位置 | 対の数 | member の内訳 |
|---|---|---|
| 指数 **384**・IdGroup `[384,608]` | **1 対** | `e1c59d6e5c4e`($c\in N$)/ `47962c00d339`($c\notin N$)。**両者とも `in_PB3=False`** |
| 指数 **750**・IdGroup `[750,6]` | **4 対** | `cfc550cc66d2`($c\in N$)と `9013ff0ddc90` `956f94cba991` `b0a21732e56f` `f5ef81767991`($c\notin N$)の**4 本**。**5 member 全て `in_PB3=False`** |

合計 **5 対** ⟹ 登録票 O-3 の「混在 5 件」と一致 ✓。「混在」の意味は札の読みどおり(**片側 $c\in N$・片側 $c\notin N$ で同一指数・同一 IdGroup = 商が同型**)✓。
**★ ただし決定的な訂正: 混在 5 対の 10 member は全て $N\not\le PB_3$**(`in_PB3=False`)。**窓ではない**(GT-shadow の枠組みは $N\in\mathrm{NFI}_{PB_3}(B_3)$、すなわち $N\le PB_3$ を要求する)。

**② 「$\iota$ は $c\in N$ を保存」の厳密性** — **正しい**。
$$c\in N\ \Rightarrow\ \iota(c)=c^{-1}\in\iota(N)\ \Rightarrow\ c\in\iota(N);\qquad c\in\iota(N)\ \overset{\iota}{\Rightarrow}\ c^{-1}\in N\ \Rightarrow\ c\in N .$$
> ★ **札より強く・より初等的にできる**: $\langle c\rangle=Z(B_3)$ は**特性部分群**ゆえ、任意の $\varphi\in\mathrm{Aut}(B_3)$ で $\varphi(c)=c^{\pm1}$。よって
> $$\boxed{\ \textbf{任意の }\varphi\in\mathrm{Aut}(B_3)\ \text{に対し}\ c\in N\iff c\in\varphi(N)\ }$$
> ⟹ 混在対は「**$\iota$ で説明されない**」だけでなく「**$\mathrm{Aut}(B_3)$ のどの元でも説明されない**」。Dyer–Grossman($\mathrm{Out}(B_3)=C_2$)も $\iota$ の具体形も**使わない**。

**③ 「混在対は M1 不可能」** — 正しい ✓。$c\in A$, $c\notin B$ なら ② より $c\in\iota(A)$ ゆえ $\iota(A)\ne B$ ⟹ 非鏡映双子。

**④ 対が本当に双子か(pairing 基準)** — ✓。cert は「$N\ne K$ 正規・同指数 $\le1000$・$B_3/N\cong B_3/K$」で対を作り、上記 5 対は**両 member の IdGroup が一致**(`[384,608]` / `[750,6]`)⟹ 商は同型 ✓。

**⑤ 格と層** — **exotic(非鏡映)双子の実在は成立**。ただし
$$\boxed{\ \textbf{これは「窓の外の層」の観測であり、窓(}N\le PB_3\textbf{)の exotic ではない}\ }$$
L2 の「exotic ゼロ」言明とは**層が違う**(札の主張どおり — ただし札は $in\_PB_3$ に触れていないので、そこを明示的に補う必要がある)。

## G.2 ★ 札が過小評価している上位発見 — 指数 750 は**サイズ 5 のクリーク**

cert 読解で判明(計算不要・cert 既載):
- 指数 750・`[750,6]` の双子対は **10 本 = $\binom52$** で、**5 個の相異なる正規部分群が 1 つのクリーク**を成す(twin 関係 = 商の同型は同値関係 ⟹ クリーク)。**登録票 O-1 の「L0 で重複出現 15 件」の正体はこれ**(20 スロット − 5 member = 15)。
- $\iota$ は各繊維に**位数 $\le2$ の対合**として作用 ⟹ 5 元の繊維は**軌道 $\ge3$ 個**、サイズ 2 の軌道は**高々 2 個** ⟹
$$\boxed{\ \text{この 10 対のうち}\ \textbf{少なくとも 8 対}\ \text{は非鏡映(exotic)}\ }$$
- **$c$ 論法が覆うのはそのうち 4 対**(混在分)。残り 4 対以上は**クリークのサイズだけ**から出る。⟹ **exotic の証拠としてはクリーク論法のほうが強い**(札 α の (E2) 型)。
- 指数 384 側は別構成: `[384,608]` の 2 元クリーク(混在 = exotic 1 対)と `[384,615]` の 2 元クリーク(**両方 $c\notin N$** ⟹ $c$ 論法では排除できない・鏡映対かもしれない)が並んでいるだけ。

## G.3 層別 exotic 地図(確定・本節が正本)

**census exotic 台帳(完結版・2026-08-06)**。全 174 対の繊維分布は **サイズ 2 × 164 本 + サイズ 5 × 1 本**(cert 全走査で確認・**兄弟クリークなし**)。

| 層 / 繊維 | 定義 | 対の数 | **exotic(非鏡映)** | 根拠 |
|---|---|---|---|---|
| **L2** | $N\le PB_3$ かつ $c\in N$、指数 $\le1000$ | **15** | **ゼロ(15/15 が鏡映対)** | 13 対 = **紙**(定理 MIRROR-ODD §A.3)/ 432・486 = **機械 2 方法**(witness word + ORB 軌道悉皆・§F.10)。加えて O-1 より L1 の 56 member は全相異 ⟹ **サイズ $\ge3$ の繊維も無い** |
| **L3** | $N\le PB_3$ かつ $c\notin N$ | 13 | **UNKNOWN(未評価)** | **【要裁定 T-1】で保留**。$\iota$ 判定自体は原理的に可能(MIRROR-SHADOW は $c\in N$ 不要)だが、**認可なしに撃たない** |
| **750-クリーク**(唯一のサイズ $\ge3$ 繊維) | 指数 750・`[750,6]`・**5 元**・全 member $\not\le PB_3$・$c$: 1 True + 4 False | **10** | **$\ge8$**(= $10-k$, $k\in\{0,1,2\}$)。★ **$k$ は未決**(系 CHARGE-750 の前提は実測で不成立 — §G.5.1 実測) | $\iota(A)=A$ 強制 + 繊維サイズ 5 > 2(§G.5.1(a))。$k$ の決定は $\iota(B_i)$ の直接同定が必要 ⟹ **便 112 scope 請求へ回付**(§G.5.3) |
| **384/`[384,608]`**(サイズ 2・混在) | 指数 384・全 member $\not\le PB_3$・$c$: 1 True + 1 False | **1** | **1(確定・残余ビットなし)** | 両 member が $\iota$-不動点 ⟹ **型 E1** の実物(§G.5.1(c)) |
| **混在層**(横断カテゴリ) | 対の両 member で `c_in_N` が割れる | **5** = 750 の 4 + 384 の 1 | **全 5 対が exotic(確定)** | ② の特性中心論法(**$\mathrm{Aut}(B_3)$ 全体で説明不能**)。★ **10 member 全て $N\not\le PB_3$ = 窓ではない** |
| **384/`[384,615]`** | サイズ 2・両 member $c\notin N$ | 1 | **UNKNOWN** | $c$ 論法では排除できない(鏡映対かもしれない) |
| **L0 の残り** | 上記以外(サイズ 2 繊維) | $174-10-1-1-15-13=134$ | **UNKNOWN** | 未評価。**「無い」とは言わない** |

**確定した exotic 総数: $\ \ge\mathbf 9$ 本**(750 で $\ge8$ + 384/`608` で 1)。**すべて窓の外**($N\not\le PB_3$)。

> ### 出力文言の規律(登録票 §5.1 の精神を継承)
> - 書いてよい: 「**窓の外の層(**$N\not\le PB_3$**)に、$\mathrm{Aut}(B_3)$ で説明できない双子(exotic)が実在する**(cert 既載・計算ゼロ)」。
> - **書いてはならない**: 「exotic 双子を初観測」(層を落とすと**窓の exotic と誤読される**)/「窓には exotic が無い」(L3 と L0 残りは UNKNOWN)/ 混在 5 対を GT-shadow の言葉(GTSh・settled・isolated)で語ること(**窓ではないので述語が未定義**)。

## G.5 追補 2(2026-08-06)— 繊維分布の確定・軌道構造の厳密計数・**司令塔フラグ表の訂正 1 件**

### G.5.0 ★ 訂正(cert 生データで再確認)

司令塔の読み「**384 は別繊維 2 本で全員 $c\notin N$**」は**誤り**。cert 生データ:

| 繊維 | member | `c_in_N` | `in_PB3` |
|---|---|---|---|
| 指数 384 ・`[384,608]` | `e1c59d6e5c4e` | **True** | False |
| 〃 | `47962c00d339` | False | False |
| 指数 384 ・`[384,615]` | `aa06e88b9851` / `5d0e51c54de4` | False / False | False / False |

⟹ **384 の 2 繊維のうち `[384,608]` は混在**($1$ True $+1$ False)。ゆえに混在 5 対 $=$ **750-クリークの 4 対 $+$ 384/`[384,608]` の 1 対**であり、「混在 5 対 ⊆ クリーク」ではない。
(整合: もし 384 が全員 $c\notin N$ なら混在は 4 対にしかならず、登録票 O-3 の「5 件」と合わない。)

**繊維分布は司令塔の読みどおり**: **サイズ 2 が 164 本 + サイズ 5 が 1 本**($164+\binom52=164+10=174$ 対 ✓・兄弟クリークなし ✓)。

### G.5.1 軌道構造の厳密計数(委嘱 ①)

繊維 $F$ 上で $\iota$ は**対合**(D-1 の悉皆性より $\iota(N)\in F$)。$c$-分割は $\iota$-安定(§G.1②)。

**(a) 750-クリーク** $F=\{A\}\sqcup\{B_1,\dots,B_4\}$($A$: $c\in A$)。
- $\{A\}$ は**シングルトン**の $\iota$-安定部分 ⟹ $\boxed{\iota(A)=A}$(**census 水準で確認できる $\iota$-不動点**)✓ 司令塔①の読みは正しい。
- $\{A,B_i\}$ の **4 対はすべて非鏡映**(= 混在 4 対そのもの)。
- $\{B_1..B_4\}$ 上で $\iota$ は対合 ⟹ 2-巡回の個数 $k\in\{0,1,2\}$ ⟹ 鏡映対は $k$ 本。
$$\boxed{\ \textbf{exotic 対数}=10-k\ \in\{8,9,10\},\qquad\textbf{確定下限は 8}\ }$$

**(b) 残り 1 ビット $k$ の決定条件(紙)**。$Q:=B_3/N\cong[750,6]\cong((C_5\times C_5){:}C_5){:}C_6$、$P_5:=\mathrm{Syl}_5(Q)$(位数 125・正規)と置く。$f:B_3\twoheadrightarrow Q$ に対し**中心荷重** $\zeta(f):=f(c)\in Z(Q)$ を定める。
- $c\mapsto6$ in $B_3^{\rm ab}=\mathbf Z$ ⟹ $\bar c$ の $Q/P_5\cong C_6$ での像は $0$ ⟹ $\bar c\in P_5$。$\bar c\in Z(Q)\cap P_5\subseteq Z(P_5)$、**位数 $p^3$ の非可換群の中心は $C_p$** ⟹ $Z_5(Q):=Z(Q)\cap P_5\cong C_5$(**特性**)。⟹ $B_i$ 側は $\mathrm{ord}(\bar c)=5$、$A$ 側は $\bar c=1$。
- $\ker f=\ker f'$ $\iff$ $f'=\alpha\circ f$($\alpha\in\mathrm{Aut}\,Q$)⟹ **$\zeta$ の $\mathrm{Aut}(Q)$-軌道が $N$ の不変量**。また $\zeta(f\circ\iota)=f(c^{-1})=\zeta(f)^{-1}$ かつ $\ker(f\circ\iota)=\iota(N)$。
$$\Longrightarrow\quad \iota(B_i)=B_i\ \Longrightarrow\ \exists\alpha\in\mathrm{Aut}(Q):\ \alpha|_{Z_5(Q)}=(\text{反転}).$$
> ### 系 CHARGE-750(candidate・本稿)
> $$\boxed{\ \mathrm{Aut}(Q)\to\mathrm{Aut}(Z_5(Q))\cong C_4\ \text{の像が反転を含まない}\ \Longrightarrow\ k=2\ \Longrightarrow\ \textbf{exotic はちょうど 8 対}\ }$$
> ($\lvert Z_5(Q)\rvert=5$ は奇数ゆえ $\zeta=\zeta^{-1}$ は $\zeta=1$ のみ ⟹ $B_i$ に不動点は出ない ⟹ 4 元上の不動点なし対合 = 2-巡回 2 本。)
> **決定は 1 行**: `Q:=SmallGroup(750,6); z:=生成元 of O_5(Center(Q)); ForAny(AutomorphismGroup(Q), a-> z^a = z^-1);` — **抽象群だけの計算で、census も窓も触らない**(登録宇宙の外に出ない)。

> ### ★ 実測(2026-08-06・司令塔): **前提は成立しなかった**
> $\lvert\mathrm{Aut}(Q)\rvert=1200$、**$\mathrm{Aut}(Q)\to\mathrm{Aut}(Z_5(Q))\cong C_4$ は全射**(反転を誘導する)。
> ⟹ **系 CHARGE-750 は発火せず、$k$ は未決のまま**。$\iota(B_i)=B_i$ は荷重論法では**排除できない**(「$B_i$ に不動点なし」は無反転を前件とする条件つき帰結であった — 条件が偽になった以上、結論は引けない)。
> $$\Longrightarrow\quad \textbf{exotic}\in\{8,9,10\}\ (750\text{-クリーク}),\qquad \textbf{確定}\ \ge 8+1=\mathbf 9\ (\text{384 の 1 対を含む})\ \text{は不変}.$$
>
> **副次の帰結(実測から紙で従う・訂正を含む)**: $\mathrm{Aut}(Q)$ は核 $\ker\bigl(\mathrm{Aut}(Q)\to\mathrm{Aut}(Z_5)\bigr)=:K$($\lvert K\rvert=300$)をもち、$Z_5\setminus\{1\}$ に**推移的**に作用する。$\mathrm{Aut}(Q)$ は $\mathrm{Epi}(B_3,Q)$ に**自由**に作用し、核 5 個 ⟹ $\lvert\mathrm{Epi}\rvert=5\cdot1200=6000$。荷重ごとに分けると $\lvert E_1\rvert=1200$($A$ の 1 軌道)、$\lvert E_{\ne1}\rvert=4800$ ⟹ $\mathrm{Aut}(Q)$-軌道 4 個 ⟹ 各 $B_i$ の軌道は 4 つの非自明荷重の**すべて**に $\lvert K\rvert=300$ 個ずつ代表をもつ。
> $$\boxed{\ \textbf{各 }B_i\textbf{ の「荷重」は }\zeta\ne1\textbf{ という 1 ビットに退化し、4 つの }B_i\textbf{ を区別しない}\ }$$

**(c) 384/`[384,608]` 繊維**(サイズ 2・混在)。$c$-分割の両部分がシングルトン ⟹ **両 member とも $\iota$-不動点** ⟹ 鏡映対ではない。
$$\boxed{\ \textbf{型 E1(reflexible 同型対)の実物・残余ビットなしで完全確定}\ }$$

**確定合計**: exotic 対 $\ \ge 8+1=\mathbf 9$ 本(全 174 対中)。**うち 5 本が混在対**(4 + 1)。

### G.5.2 「$c\in N$ の member が 1 個だけ存在する」ことの意味(委嘱 ②・3 行)

1. $A$ は $c\in A$ ⟹ **$Q=[750,6]$ は $\Gamma=C_2\ast C_3=PSL_2(\mathbf Z)$ の商**(補題 PSL-GEN)= 辺数 $375$ の正則地図の回転群。すなわち **$Q$ は $(2,3)$-生成群**であり、これは 5 member 中 $A$ だけがもつ性質。
2. 一方 $B_i$ は $\mathrm{ord}(\bar c)=5$ ⟹ $\langle c^5\rangle\subseteq B_i$ ⟹ $B_3/B_i$ は $B_3/\langle c^5\rangle$($PSL_2(\mathbf Z)$ の $C_5$ による中心拡大)の商。⟹ **繊維は「中心 $\langle c\rangle$ をどこまで殺すか」で $A$(全殺し)と $B_i$(1/5 だけ残す)に分かれる**。
3. その残り $C_5$ は $P_5=((C_5\times C_5){:}C_5)$ の**中心そのもの** $Z_5(Q)$ であり、$\lvert Z_5(Q)\rvert=5=\lvert F\rvert$。~~⟹ 繊維サイズ 5 = 中心荷重の値域サイズ(荷重と member が 1:1)~~ ⟹ ★ **この機構仮説は実測で反証された**(§G.5.1 の実測: $\mathrm{Aut}(Q)$ が $Z_5$ の反転を含む ⟹ 非自明荷重は**単一の $\mathrm{Aut}$-軌道**に潰れ、4 つの $B_i$ を区別しない)。**$\lvert F\rvert=5=\lvert Z_5(Q)\rvert$ は現時点で説明のつかない数値一致にとどまる**(内訳は「荷重 $0$ が 1 核 + 荷重 $\ne0$ が 4 核 = $K$-軌道 4 個」であり、$4=\lvert Z_5\setminus\{1\}\rvert$ の一致は偶然かもしれない)。
   ただし **$c$-分割そのもの($A$ 対 $B_i$)は荷重の 1 ビットで完全に説明される** ⟹ **発案札 α の「源 0 = 中心荷重」は生きている**(L2 が exotic ゼロなのは**層の定義 $c\in N$ が $\zeta\equiv1$ に凍結して源 0 を丸ごと殺しているから**)。反証されたのは「$B$ 側の内訳まで荷重で説明できる」という**強い版だけ**である。

### G.5.3 限界注記 **CHARGE-LIMIT**(2 行)+ 残務の回付先

> **注記 CHARGE-LIMIT**: 中心荷重 $\zeta$ は「$\mathrm{Aut}(Q)$-軌道」としてしか不変量にならない。$\mathrm{Aut}(Q)\to\mathrm{Aut}(Z(Q))$ の像が反転を含む群では $\zeta$ は「$1$ か否か」の 1 ビットに退化し、**$\iota$-対合の軌道内訳(不動点の有無・2-巡回の本数)は抽象的不変量では決まらない**。
> ⟹ 一般則: **$\iota$-固定性は「標識づけられた核」の性質であり、抽象量(IdGroup・構造式・中心荷重)はどれも潰れうる。判定は必ず「核そのものの同定」または「$\mathrm{Aut}$ の直接探索」まで降りる必要がある。**

★ これは工房で **3 度目**の同じ教訓である: ①§F.6.2(IdGroup は chiral/reflexible を区別しない可能性)→ ②§F.8(だから ORB = $\mathrm{Aut}$ 直接探索が主経路)→ ③本節(中心荷重も潰れた)。**「抽象不変量で掌性を決めようとしない」を規約級の心得として記録する。**

**残務の回付(実行しない・裁定請求のみ)**:
- $k$ の決定に必要な操作は **$\iota(B_i)$ の直接同定**(census の `canonical_id_words` に生成元反転 $a\mapsto a^{-1},b\mapsto b^{-1}$ を適用し、得られる正規部分群を繊維内で同定)。**4 member 分・数秒。**
- ただし $B_i$ は $c\notin N$ member ⟹ **【要裁定 T-1】と同族**につき、**認可なしに撃たない**。**便 112 の scope 請求へ回付**。
- 請求時に明記すべき射程(誤解防止): 本操作は**語レベルの $\iota$-像同定のみ**であり、hexagon・charming・(SURJ)・kernel 比較・settled/isolated の**述語は一切評価しない**(そもそも $B_i$ は $N\not\le PB_3$ で窓ではなく、GT-shadow の述語が未定義)。T-1 が守っている「$c\notin N$ 窓に checker で TRUE/FALSE を付けない」規範には**触れない**操作である。

## G.6 追補 3(2026-08-06)— R-6a 実測の批准・台帳最終形・MIRROR-ODD 整合検査

**実測**(`search/certs/r6a_summary_v1_20260806.json`・両固定表 `scratchpad/r6a_bothfixed_table.json`・二系統一致の語レベル):
**①** 750-クリークの $B$ 4 人は**全員 $\iota$-固定** ⟹ $k=0$ ⟹ **exotic $=10-k=\mathbf{10}$**(§G.5.1 の式の**最大値**)。系 CHARGE-750 の「$\mathrm{Aut}$ が反転を実現 ⟹ 固定が起こりうる」と整合 ✓。
**②** 指数 $<384$ の 45 対 $=$ 鏡映 33 $+$ **両固定 12**(全て `in_PB3=False` = 窓外・最小指数 **24**・両 $c\in N$ は 336 の 1 対のみ)。
**③** **L3 の 13 対は全て鏡映** ⟹ 窓層(L1 = 28 対)に exotic ゼロ。

### G.6.a 「both-fixed ⟹ E1 型 exotic」の**批准**(厳密化つき)

> ### 補題 BOTH-FIXED-EXOTIC(candidate・本稿)
> $A\ne B$ が同一繊維($B_3/A\cong B_3/B$・同指数)にあり $\iota(A)=A$、$\iota(B)=B$ とする。このとき
> **(i)** $\iota$ はこの双子関係を説明しない($\iota(A)=A\ne B$)— **初等・文献不要**。
> **(ii)** さらに $\mathrm{Out}(B_3)=\langle\iota\rangle$(Dyer–Grossman)を認めれば、**どの $\varphi\in\mathrm{Aut}(B_3)$ も $\varphi(A)=B$ を満たさない**:$\mathrm{Inn}$ は正規部分群を動かさず、$\varphi(A)\in\{A,\iota(A)\}=\{A\}$。
> ⟹ **同型 $B_3/A\cong B_3/B$ は $B_3$ の自己同型に持ち上がらない = exotic(型 E1)** ✓ **批准**。

**繊維の一般公式(記録)**: 繊維サイズ $m$、$\iota$-不動点 $f$、2-巡回 $t$($m=f+2t$)とすると
$$\boxed{\ \text{その繊維の exotic 対数}=\binom m2-t\ }$$
(鏡映対は 2-巡回 1 つにつき 1 本のみ)。⟹ 両固定サイズ 2($f=2,t=0$)は $1-0=1$ ✓;750-クリーク($m=5,f=5,t=0$)は $10-0=10$ ✓。
★ **これまでに確定した exotic 23 対はすべて型 E1**(両固定)である。**E3(同一繊維に交わらない鏡映対 2 本)は 1 件も出ていない**。

### G.6.b §G.3 台帳 — **最終形**

| 層 / カテゴリ | 対数 | 鏡映 | **exotic** | 未測定 | 根拠 |
|---|---:|---:|---:|---:|---|
| **L2**(窓・$c\in N$) | **15** | 15 | **0** | 0 | 裁定 602(witness word)+ ORB 軌道悉皆(§F.10) |
| **L3**(窓・$c\notin N$) | **13** | 13 | **0** | 0 | **R-6a** |
| **窓 合計(L1)** | **28** | **28** | **0** | 0 | ⟹ $\boxed{h^{\rm win}>1000}$(**指数 $\le1000$ の全窓で exotic 不在**) |
| 非窓・指数 $<384$ | 39 | 27 | **12**(E1) | 0 | R-6a。全て `in_PB3=False`・最小指数 **24**($[24,3]=SL(2,3)$・両 $c\notin N$) |
| 非窓・指数 384(混在 `[384,608]`) | 1 | 0 | **1**(E1) | 0 | §G.5.1(c)(両部分がシングルトン ⟹ 両固定) |
| 非窓・750-クリーク | 10 | 0 | **10**(E1) | 0 | R-6a($k=0$) |
| 非窓・その他(指数 $(384,1000]$・750 除く) | **96** | — | — | **96** | **UNKNOWN**(未測定。「無い」とは言わない) |
| **合計** | **174** | 55 | **23** | 96 | |

$$\boxed{\ h^{\rm cen}=24\ (\text{達成: }[24,3]=SL(2,3)\text{ の両固定対}),\qquad h^{\rm win}>1000\ }$$
($h^{\rm cen}$ = census 全体での exotic 最小指数。census の最小指数自体が 24 なので**下限も 24** ⟹ 等号。)

> **書式規律(不変)**: exotic 23 対は**すべて窓の外**($N\not\le PB_3$)。GTSh・settled・isolated の語で語らない(述語が未定義)。96 対は **UNKNOWN**(非存在を主張しない)。

### G.6.c ★ MIRROR-ODD との整合検査 — **11/11 の独立確認**

> ### 定理 MIRROR-ODD の射程の**明確化**(v1 の但し書きの訂正)
> §A.3 の証明を読み直すと、**$N\le PB_3$ はどの段でも使っていない**(PSL-GEN も MIRROR-PSL も $c\in N$ のみを使う)。
> $$\boxed{\ \textbf{MIRROR-ODD の前件は「}c\in N\textbf{」+「}q\ge5\textbf{ の非自明巡回正規 Sylow」だけ — 窓である必要はない}\ }$$
> ⟹ **census の非窓層にも適用でき、そこが独立の検定場になる。**

census cert の構造式から、**指数 $<384$ で両 member が $c\in N$ の対は 12 本**:

| 指数(IdGroup) | 商の構造 | 巡回正規 Sylow$_q$($q\ge5$) | MIRROR-ODD | R-6a 実測 |
|---|---|---|---|---|
| 42 `[42,1]`, 78, 114, 186, 222, 258, 366 | $C_p\!:\!C_6$($p=7,13,19,31,37,43,61$) | ✓ $C_p$ | **鏡映を強制** | **鏡映** ✓ |
| 168 `[168,49]`, 312 `[312,51]` | $C_p\!:\!(C_2\times A_4)$ | ✓ | **鏡映を強制** | **鏡映** ✓ |
| 294 `[294,1]` | $C_{49}\!:\!C_6$ | ✓ $C_{49}$(巡回) | **鏡映を強制** | **鏡映** ✓ |
| 336 `[336,134]` | $C_7\!:\!(((C_4\!\times\!C_2)\!:\!C_2)\!:\!C_3)$ | ✓ $C_7$ | **鏡映を強制** | **鏡映** ✓ |
| **336 `[336,208]`** | $\mathbf{PSL(3,2)\!:\!C_2}$ | ✗(単純部分群 ⟹ $n_7=8$) | **沈黙** | **両固定**(exotic) |

$$\Longrightarrow\ \boxed{\ \textbf{定理が発火する 11 対はすべて鏡映・沈黙する 1 対だけが両固定 — 矛盾ゼロ}\ }$$

> ### ★ 反証可能な形での言明(**司令塔の両固定表と 1 行で突合できる**)
> **両固定 12 対のうち唯一の両 $c\in N$ の対は、必ず `[336,208] = PSL(3,2):C2` の繊維でなければならない。** もし `[336,134]`($C_7$ 正規巡回)側だったら **MIRROR-ODD は反証される** ⟹ 即 STOP・§A.3 の証明を再検分。
> **750-クリークとの整合も同型**: $c\in N$ の member $A$ は $\iota$-固定だが、$[750,6]=((C_5\times C_5)\!:\!C_5)\!:\!C_6$ の Sylow$_5$ は**位数 125・非巡回** ⟹ **MIRROR-ODD は沈黙** ⟹ 矛盾なし ✓。
> **指数 24 の両固定**($[24,3]=SL(2,3)$)は両 member が $c\notin N$ ⟹ **PSL-GEN が使えず定理は沈黙** ⟹ **「$\iota$-固定が定理で強制される型」ではなく「測定でしか分からない型」**(委嘱 (c) の 1 行判定)。

### G.6.d 委嘱 (d) — T-1 で保留していた紙延長の再起票可否(1 行)

> **可(限定つき)**: **MIRROR-SHADOW は $c\in N$ を使わない**(§2.2 は $B_3$ 内の恒等式)ので、R-6a の「L3 13 対は全て鏡映」= $\iota(N)\ne N$ を入力すれば、**L3 の 26 directed 窓すべてで $[-1,1]\in\mathrm{GTSh}(\iota(N),N)$ が非 settled shadow ⟹ 非 isolated** が**紙で言える** — これは再起票してよい。
> **不可**: **MIRROR-ODD の L3 への延長**(PSL-GEN が $c\in N$ を必須とする ⟹ L3 の鏡映性は**機械のみ**・紙の裏づけゼロ)、および **checker の TRUE/FALSE を L3 に付けること**(M-ISO-6 の禁止は不変・T-1 は解除しない)。

## G.7 追補 4(2026-08-06)— G4/G5 帯掃引の批准・**「reflexible 優勢」の読み替え**

**実測**(`search/certs/sg_g4_g5_orb_20260806.json`・裁定 649 発火・4 shard 併合):**36 群** $=$ **31 `isolated_self_mirror_no_twin`** $+$ **5 `single_mirror_pair_non_exotic`**、**exotic 0**。位数は $1152,1296,1458,1728,1944$(**すべて $2^i3^j$**)。

### G.7.0 カナリア(私の側で再検算・**全通過**)

| 検査 | 結果 |
|---|---|
| `M_size / aut_order = num_orbits`(生成対の $\mathrm{Aut}$-固定化群は自明 ⟹ 全軌道長 $=\lvert\mathrm{Aut}\rvert$・§F.10.1) | **36/36 PASS** |
| 全軌道の長さ $=\lvert\mathrm{Aut}(\widehat P)\rvert$ | **PASS** |
| $\nu$ が軌道集合上の対合(§G.6.a) | **PASS** |

内訳: $1152{:}\,7/0$、$1296{:}\,5/2$、$1458{:}\,6/0$、$1728{:}\,5/1$、$1944{:}\,8/2$(isolated / chiral 対)。

### G.7.1 ★★ 委嘱② の回答 — 「帯で掌性が消える」は**読み替えが要る**

> ### 補題 FIBER-FORCED(自明だが決定的)
> 繊維サイズ($=$ 同型な商をもつ窓の個数 $=\lvert\mathcal M\rvert/\lvert\mathrm{Aut}(\widehat P)\rvert$)が **1 ならば、その窓は自動的に $\iota$-固定**($\nu$ は 1 点集合を動かせない)。

⟹ **31 の "reflexible 孤立" は「掌性が消えた」のではなく「そもそも選択肢が 1 個しかない」**。$\iota$-固定は**強制**であり、**掌性機構については何も語らない**(cert の `num_orbits=1` がその証拠)。
$$\boxed{\ \textbf{情報を持つのは繊維サイズ 2 の 5 群だけ — そしてそれは }5/5\ \textbf{が chiral 対}\ }$$

> ### ★ 両帯を貫く不変(**これが本当の観測**)
> | 帯 | 繊維サイズ 2 の窓群 | うち chiral 対 | 両 $\iota$-固定(E1) |
> |---|---:|---:|---:|
> | 指数 $\le1000$(L2 = c∈N 窓) | 15 | **15** | 0 |
> | 指数 $(1000,2000]$・$2^i3^j$ | 5 | **5** | 0 |
> | **合計** | **20** | **20** | **0** |
> ⟹ **観測されたすべての「窓の双子」は chiral 対**であり、**窓層に E1 型 exotic は 1 件も無い**。帯を跨いでこの性質は**変わっていない**。「相転移」は**繊維サイズ分布**に起きたのであって掌性ではない。

### G.7.2 機構仮説(**司令塔の直観の精密化**)

> ### 定理 MIRROR-ODD′(**射程の一般化**・candidate・本稿)
> $c\in N$ とし、$A$ を $\widehat P$ の特性部分群または特性切片で $\mathrm{Aut}(A)$ **可換**なものとする。
> $$\boxed{\ \mu(W)\ne1\ \Longrightarrow\ \iota(N)\ne N\ }\qquad(W=\delta N,\ \mathrm{ord}(W)\mid3)$$
> **証明.** $\iota(N)=N$ なら(MIRROR-PSL の $\beta$ と $\mathrm{Aut}(A)$ の可換性で)$\mu(W)=\mu(W)^{-1}$ ⟹ $\mu(W)^2=1$;$W^3=1$ ⟹ $\mu(W)=1$。∎
> ⟹ **定理 MIRROR-ODD(§A.3)は「$q\ge5$ の巡回正規 Sylow が $\mu(W)\ne1$ を *強制する*」という特殊化にすぎない**($q\ge5$ は $\widehat P_0^{\rm ab}$ の指数 3 との衝突を作るためだけに使われた)。

**⟹ 機構の言明(candidate)**:
$$\underbrace{\boxed{\ \textbf{掌性は「}W\textbf{ が非自明に作用する特性切片」が\textbf{製造}している。}\ q\ge5\ \textbf{の巡回正規 Sylow はその最も安価な供給源}\ }}_{\textbf{★ 2026-08-06 実測(P-BAND-2)で\textbf{棄却}。§G.8 を見よ — 5 chiral 群は当該切片を\textbf{もたない}}}$$
$2^i3^j$ 帯は定義上その供給源を持たない ⟹ **MIRROR-ODD が沈黙する帯 = 掌性の製造装置が外された帯** ⟹ reflexible が優勢になるのは**自然**であり、「相転移」というより **原因の除去**である。

> ### CHARGE-750 との統一(司令塔の読みは正しい・ただし経路が 1 段深い)
> §G.5 では「$\mathrm{Aut}(Q)$ が $Z_5$ の反転を実現する ⟹ $\iota$-固定が起こりうる」だった。今回は「$\mathrm{Aut}(\widehat P)$ が $(U,W)\mapsto(U,W^{-1})$ を実現する ⟹ reflexible」。**どちらも「$\iota$-奇な不変量が $\mathrm{Aut}$ で潰れるか」の同じ問い**である(注記 CHARGE-LIMIT の系)。ただし $2^i3^j$ 帯で効いているのは $\lvert\mathrm{Aut}\rvert$ の大きさ**そのもの**ではなく、**$\iota$-奇な不変量の供給源($q\ge5$ 切片)の不在**である ⟹ 「Aut が大きいから」は**近因**、「奇素数切片が無いから」が**遠因**。

> ### ★ 反証可能な予言 **P-BAND-2**(**安価・機構の直接検定**)
> 36 群それぞれについて、**$W$ が非自明に作用する巡回特性切片**($\mathrm{Aut}$ 可換)を探せ。機構仮説が正しければ
> - **5 つの chiral 群には存在する**(MIRROR-ODD′ が発火して掌性を説明する)。
> - **31 の reflexible 群には存在しない**($W$ はすべての巡回特性切片を中心化する)。
> 外れたら機構仮説は棄却(掌性の供給源が他にある)。**繊維サイズ 1 の 31 群では $\iota$-固定が強制なので、この検定だけが機構の情報を持つ。**

### G.7.3 委嘱① — 帯限定量化と「$h^{\rm win}>2000$」の可否

> **逐語の量化(SG-GAP-3 の帯限定を明示)**:
> $$\forall N:\ \Bigl[N\trianglelefteq B_3,\ N\le PB_3,\ c\in N,\ \lvert B_3/N\rvert\in(1000,2000],\ \lvert B_3/N\rvert=2^i3^j\Bigr]\ \Longrightarrow\ \text{$N$ の繊維は単一の }\iota\text{-軌道}$$
> すなわち **exotic ゼロ**。

$$\boxed{\ \textbf{「}h^{\rm win}>2000\textbf{」は書けない}\ }$$
**理由**: 掃引したのは $(1000,2000]$ の **$2^i3^j$ 位数のみ**。この帯の非 $\{2,3\}$-smooth 位数($1050,1092,\dots$ など多数)は**未測定**であり、そこは紙でも埋まらない — **MIRROR-ODD は各窓の掌性($\iota(N)\ne N$)を出すが、繊維に軌道が 2 つ以上ないこと(= exotic ゼロ)は出さない**。
⟹ 正しい書き方は次の 2 行:
- **$h^{\rm win}>1000$**(無条件・指数 $\le1000$ の悉皆 census)。
- **$(1000,2000]$ の $2^i3^j$ 位数に限れば exotic ゼロ**(36 群・機械)。**帯全体への一般化を書いたら `OVERCLAIM / STOP`。**

> ### ★ 副産物(紙で埋まる部分の正確な同定)
> ### 系 NO-E1(candidate・本稿)
> $\widehat P$ が $q\ge5$ の非自明**巡回正規 Sylow** をもつなら、その繊維の**全 member が chiral**(MIRROR-ODD が全窓に効く)⟹ **その繊維に $\iota$-固定点は存在しない** ⟹
> $$\boxed{\ \textbf{E1 型 exotic(両}\iota\textbf{-固定)は、MIRROR-ODD の射程内では\textbf{紙で不可能}}\ }$$
> ⟹ 観測された census の exotic **23 対はすべて E1** だったから、**射程内では E1 が原理的に出ない**ことと整合する(実際 23 対はすべて $q\ge5$ の巡回正規 Sylow を欠くか $c\notin N$ 側だった)。残る危険は **E2/E3(繊維サイズ $\ge4$)** のみ。

**exotic 被覆の地図(3 域)**:

| 域 | 範囲 | E1 型 | E2/E3 型 | 根拠 |
|---|---|---|---|---|
| **A** | $c\in N$ かつ $q\ge5$ の巡回正規 Sylow(**指数無制限**) | **紙で不可能**(系 NO-E1) | UNKNOWN | MIRROR-ODD |
| **B** | 窓・指数 $\le1000$ | 0 | 0 | census 悉皆(機械) |
| **C** | 窓・指数 $(1000,2000]$ かつ $2^i3^j$ | 0 | 0 | G4/G5 掃引(機械・36 群) |
| — | それ以外(例: $(1000,2000]$ の非 $2^i3^j$、$>2000$) | **UNKNOWN** | **UNKNOWN** | 未測定 |

### G.7.4 委嘱③ — 5 鏡映対の格

$1296{:}\,2$ 対、$1728{:}\,1$ 対、$1944{:}\,2$ 対。位数はすべて $2^i3^j$ ⟹ **$q\ge5$ の Sylow が存在しない** ⟹ **MIRROR-ODD は 1 対も覆わない**。
$$\boxed{\ \textbf{この 5 対の chiral 性は「機械のみ」— 紙の裏づけはゼロ}\ }$$
(格: ORB 軌道悉皆による **candidate / single-system**。低指数帯 L2 の 13/15 が紙で閉じているのと**対照的**であり、報告でこの区別を潰さないこと。**MIRROR-ODD′ + P-BAND-2 が通れば紙に昇格しうる**唯一の経路。)

### G.7.5 委嘱④ — §G.3 台帳への帯行(**追加**)

| 層 / カテゴリ | 対数(繊維サイズ 2) | 鏡映 | exotic | 未測定 | 根拠・格 |
|---|---:|---:|---:|---:|---|
| **窓・指数 $(1000,2000]$・$2^i3^j$**(G4/G5 帯) | **5** | **5** | **0** | 0 | 機械のみ(ORB 悉皆・36 群中 31 は繊維サイズ 1 = $\iota$-固定強制)。**紙の裏づけゼロ** |
| 窓・指数 $(1000,2000]$・非 $2^i3^j$ | — | — | — | **全部** | **UNKNOWN**(未掃引) |

**$h$ 指標の最終形**:
$$h^{\rm cen}=24,\qquad h^{\rm win}>1000,\qquad \boxed{\ (1000,2000]\cap\{2^i3^j\}\ \text{に窓の exotic なし(帯限定)}\ }$$

## G.8 追補 5(2026-08-06)— **P-BAND-2 の棄却**(仮説の埋葬)と救済形

**採点結果**(実測 `11e94cc`・36 行表): **reflexible 側 31/31 的中・chiral 側 0/5**(5 群とも「$W$ が非自明に作用する巡回特性切片」は **NOT_EXISTS**)。

### G.8.1 裁定 — **機構仮説は棄却**。しかも「31/31 的中」は**無情報**だった

> $$\boxed{\ \textbf{§G.7.2 の機構仮説「掌性は }W\textbf{ 非自明作用の(巡回)特性切片が製造する」は\textbf{棄却}}\ }$$
> 5 つの chiral 窓群は当該切片を**もたない**のに chiral である ⟹ **掌性の供給源は別にある**。

**★ さらに厳しい自己批判(隠さず記録)**: 当該切片は **36 群すべてで NOT_EXISTS**(0/36)。すなわち私の予言は
$$\text{「reflexible 側に無い」= 全体で無いことの一部}\quad\Longrightarrow\quad \textbf{31/31 の「的中」は検定力ゼロの空振り}$$
であった。**片側が定数の予言は予言ではない。** 事前に「両側で分かれる」ことの見込みを吟味していれば出さずに済んだ。
**再発防止(自分に課す)**: **予言を出す前に「もし仮説が偽なら測定値はどう変わるか」を 1 行書く**(差が出ない設計なら出さない)。

**なぜ外したかの診断(数学的な理由が特定できた)**: 「**巡回**」を課したのが致命だった。$A$ が巡回なら $\mathrm{Aut}(A)$ 可換 ⟹ 補正 $h$ が無力 ⟹ 条件は $\mu(W)=1$ に退化する。ところが $2^i3^j$ 群では
- $A$ が巡回 **2-**切片: $\mathrm{Aut}(C_{2^a})$ は 2 群 ⟹ 位数 3 の元が無い ⟹ **$\mu(W)=1$ は自動**(検定不能)。
- $A$ が巡回 **3-**切片: $\mu(W)\ne1$ には $A\cong C_{3^b}$($b\ge2$)が要る ⟹ 稀。
$$\Longrightarrow\ \boxed{\ \textbf{巡回切片は }2^i3^j\ \textbf{帯では原理的にほぼ空振りする道具だった}\ }$$

### G.8.2 生存・死亡の仕分け(**混同禁止**)

| 対象 | 状態 |
|---|---|
| **定理 MIRROR-ODD**(§A.3)・**MIRROR-ODD′**(§G.7.2)| **無傷**(証明済みの**十分条件**。5 群で沈黙しているだけで矛盾していない) |
| L2 の **13/15 紙閉じ** | **無傷** |
| **系 NO-E1**(§G.7.3) | **無傷**(§G.8.4 で再確認) |
| **補題 FIBER-FORCED** と §G.7.1 の読み替え(31 は繊維サイズ 1 ゆえ $\iota$-固定強制・情報は 5 群のみ) | **無傷**(機構仮説と独立) |
| §G.7.2 の**機構の言明**(掌性の製造元) | **棄却**(取り消し線つきで残置) |
| 「reflexible 優勢 = 原因の除去」という**因果の物語** | **棄却**。残るのは**相関の観測**のみ($q\ge5$ 供給源が無い帯で繊維サイズ 1 が優勢)。因果は未同定 |

### G.8.3 救済形 — **Tool R2′ の復権**(P-BAND-2′)

棄却されたのは「巡回」版であって、**一般形は最初から §A.6 Tool R2′ に書いてあった**。それを検定形に直す:

> ### 判定式 SECT(candidate・$\iota$-固定の**必要条件**・任意の特性切片で成立)
> $A$ を $\widehat P$ の特性切片、$\mu:\widehat P\to\mathrm{Aut}(A)$ を作用とする。$\iota(N)=N$ なら
> $$\boxed{\ \exists h\in\mathrm{Aut}(A):\quad h\,\mu(U)\,h^{-1}=\mu(U)\ \ \wedge\ \ h\,\mu(W)\,h^{-1}=\mu(W)^{-1}\ }$$
> すなわち**対 $(\mu(U),\mu(W))$ と $(\mu(U),\mu(W)^{-1})$ が $\mathrm{Aut}(A)$ で同時共役**。$\mathrm{Aut}(A)$ 可換のときだけ「$\mu(W)=1$」に退化する(= 死んだ版)。

> ### ★ 単元条件は $p\in\{2,3\}$ では**常に満たされる**(だから対条件が全て)
> $\mu(W)$ は位数 $\mid3$。$A$ が $p$-初等可換で $\mathrm{Aut}(A)=GL(d,p)$ のとき:
> - $p=2$: 位数 3 の元の有理標準形は $x^2+x+1$(自己相反)⟹ $M\sim M^{-1}$ **常に**。
> - $p=3$: $\mu(W)$ は単冪 ⟹ Jordan 型が $M$ と $M^{-1}$ で一致 ⟹ **常に**共役。
> $$\Longrightarrow\ \boxed{\ \textbf{障害は「}\mu(W)\sim\mu(W)^{-1}\textbf{」ではなく、\textbf{$\mu(U)$ を固定したままの同時性}にしかありえない}\ }$$
> ⟹ **非可換 $\mathrm{Aut}(A)$(= 非巡回切片)でしか障害は出ない**。私の旧版が空振りしたのはここ。

> ### **P-BAND-2′(再定式化・安価)**
> 36 群の各々について、**主組成列の因子(chief factor)** $A$(初等可換 $p^d$、$p\in\{2,3\}$)を全て取り、$\mu(U),\mu(W)\in GL(d,p)$ を計算して**判定式 SECT** を検定せよ。
> - **予言 (i)**: 31 の reflexible 群では **全 chief factor で SECT が成立**(定理の必要条件ゆえ**必ず**成立 — これは検定ではなく**実装の健全性検査**)。
> - **予言 (ii)**(**これが本番**): **5 つの chiral 群では、少なくとも 1 つの chief factor で SECT が破れる**。
> - **★ 差が出ない場合の意味を先に固定**: 5 群でも全 chief factor が SECT を通ったら ⟹ **掌性は切片(局所)不変量では検出できない** ⟹ §G.8.4 の (H2)/(H3) へ移り、**§A.5 の条件付き【文献要請】(chirality group / chirality index)を発火**する。
> ⟹ **どちらに転んでも情報が出る設計**(前回の失敗の是正)。

### G.8.4 掌性源の仮説候補(委嘱②・優先順)

| # | 仮説 | 内容 | 検定 |
|---|---|---|---|
| **(H1)** | **chief factor 障害** | ある非巡回 chief factor で $(\mu(U),\mu(W))$ が同時共役でない | **P-BAND-2′**(即実行可・数分) |
| **(H2)** | **拡大(コホモロジー)障害** | 全 chief factor では対称性が実現するが、拡大を通して**持ち上がらない** ⟹ 障害は $H^1/H^2$ 側 | H1 が外れたら。Part B の $M_R$/$Z^1$ 器具が流用できる |
| **(H3)** | **Nielsen 類(大域)現象** | 掌性は**標識対**の性質で、どの特性切片にも像を残さない。発案札 α の **W-COLLAPSE**($\mathrm{ord}\,U=2,\mathrm{ord}\,W=3$ が素数 ⟹ Wilson 演算子が $\{\mathrm{id},\iota\}$ に退化)より、**演算子起源でない真の Nielsen 類分裂**しかありえない | 【文献要請】chirality group / chirality index |

> **私の見立て(candidate)**: (H1) の目は十分ある — §G.8.3 の観測より障害は「$\mu(U)$ を固定したままの同時性」だけに宿るので、**$U$($\iota$ が固定する側)と $W$($\iota$ が反転する側)の非可換な絡み**が chief factor 水準で見える可能性は高い。ただし **CHARGE-LIMIT の教訓**(抽象不変量は潰れうる・判定は $\mathrm{Aut}$ 直接探索まで降りる)から、(H2)(H3) を**同時に生きた選択肢として保持**する。

### G.8.5 委嘱③ — **系 NO-E1 と危険域評価は無傷**(確認)

系 NO-E1 の証明は「**定理 MIRROR-ODD**($q\ge5$ 巡回正規 Sylow ⟹ 全 member chiral ⟹ 繊維に $\iota$-固定点なし)」だけを使う ⟹ **棄却された機構仮説を一切参照していない** ⟹ **無傷** ✓。
$$\boxed{\ \text{被覆地図(§G.7.3 の 3 域 A/B/C)・}h^{\rm cen}=24\text{・}h^{\rm win}>1000\text{・帯限定 exotic ゼロ — すべて不変}\ }$$
**E2/E3 危険域の評価も不変**(繊維サイズ $\ge4$ が残る唯一の危険)。ただし 1 点だけ**弱くなった**: §G.7.2 の因果物語で「$2^i3^j$ 帯は掌性の供給源が無い」と言えていた分だけ、**帯の外(未掃引域)で E2/E3 が出にくいと期待する根拠も消えた** ⟹ 未掃引域の危険度評価は**素の UNKNOWN に戻す**。

### G.8.6 台帳への記録(予言の墓標)

| 予言 | 結果 | 格 |
|---|---|---|
| **P-BAND-2** | **棄却**(chiral 側 0/5)。reflexible 側 31/31 は**検定力ゼロ** | 死亡・記録として残置 |
| **P-BAND-2′** | 未実行(§G.8.3) | 発火待ち(どちらに転んでも情報が出る) |

## G.9 追補 6(2026-08-06・裁定 681)— SECT の紙定理化・掌性源の三層成層・文献要請の発火

**実測**(`search/certs/sg_pband2prime_20260806.json`・`8fe536d`): **31/31 健全**(reflexible 群は全 chief factor で SECT 成立 = 実装健全性検査 PASS)/ **chiral 3/5 が SECT 破れ**、破れは**すべて $3^2=GL(2,3)$ 因子でのみ**(§G.8.3 の「障害は非可換 $\mathrm{Aut}(A)$ にしか住めない」と**厳密整合**)/ 残り **2/5**(`(1944,826)`・`(1944,921)`)は組成列に $3^2$ 因子が無く**全通過** = **局所検出不能の確定標本**。

### G.9.1 委嘱① — **「SECT 破れ ⟹ chiral」は定理**(ただし前件 1 つを要確認)

> ### 定理 SECT-CHIRAL(candidate・本稿。**Tool R2′ の対偶**)
> $A=M/L$ を $\widehat P$ の**特性切片**($M,L$ ともに $\widehat P$ の**特性**部分群)、$\mu:\widehat P\to\mathrm{Aut}(A)$ を共役作用とする。
> $$\boxed{\ \nexists h\in\mathrm{Aut}(A):\ h\mu(U)h^{-1}=\mu(U)\wedge h\mu(W)h^{-1}=\mu(W)^{-1}\ \Longrightarrow\ \iota(N)\ne N\ (\textbf{chiral})\ }$$
> **証明.** $\iota(N)=N$ なら MIRROR-PSL の $\beta\in\mathrm{Aut}(\widehat P)$($\beta(U)=U,\ \beta(W)=W^{-1}$)が存在。$M,L$ 特性ゆえ $\beta$ は $A$ に $\beta_A\in\mathrm{Aut}(A)$ を誘導し、$\beta_A\circ\mu(g)=\mu(\beta(g))\circ\beta_A$(切片の代表元で直接確認)。$g=U$ で $\beta_A$ は $\mu(U)$ を中心化、$g=W$ で $\mu(W)\mapsto\mu(W)^{-1}$ ⟹ $h:=\beta_A$ が存在してしまう。対偶。∎

> ### ⚠【GAP-G9-1】前件の確認が必要:**chief factor は「正規」であって「特性」とは限らない**
> 実測は chief series の因子で回している。$\beta$ は正規部分群を**置換**するだけなので、$M,L$ が特性でなければ $\beta_A$ が定義できない。⟹ **3 群それぞれについて、破れが出た $3^2$ 因子 $M/L$ の $M,L$ が特性であることを確認せよ**(最も安価な十分条件: **その位数の正規部分群が一意**、または Fitting/下降中心/$O_p$ 系など特性系の項である)。確認できれば**そのまま紙の定理が適用**、できなければ**特性細分**に取り替えて再検定。**この 1 点だけで昇格の可否が決まる。**

> ### ★ $3^2$ 因子での SECT の**閉じた形**(手で検算できる)
> $A\cong C_3^2$、$\mathrm{Aut}(A)=GL(2,3)$、$\mu(W)\ne1$(位数 3 ⟹ 単冪 = 転移子 $T$)とする。$S:=\{h: hTh^{-1}=T^{-1}\}$ は $h_0=\mathrm{diag}(1,-1)$ を代表とする $C(T)$ の剰余類で $\lvert S\rvert=6$、**その 6 元はすべて対合**($[[a,b],[0,-a]]^2=a^2I=I$)。$\mu(U)$ は対合ゆえ $C(\mu(U))=\{\pm I,\pm\mu(U)\}$(非中心のとき)。$\pm I\notin S$ より
> $$\boxed{\ \textbf{SECT}\iff \mu(U)=\pm I\ \ \text{または}\ \ \mu(U)\,\mu(W)\,\mu(U)^{-1}=\mu(W)^{-1}\ \ (\iff\langle\mu(U),\mu(W)\rangle\cong S_3)\ }$$
> $$\Longrightarrow\ \textbf{SECT 破れ}\iff \mu(U)\ \text{は非中心対合で}\ \mu(W)\ \text{を反転しない}\iff\langle\mu(U),\mu(W)\rangle\not\cong S_3 .$$
> ⟹ **証拠は $2\times2$ 行列 2 個**であり、$GL(2,3)$(位数 48)内の有限判定は**人手で検算できる大きさ**。⟹ 3 対の掌性は「$\lvert\mathrm{Aut}\rvert$ 数千の悉皆探索」ではなく**小さな紙の証明書**になる。

**格の昇格(委嘱①の答え)**:
$$\boxed{\ \text{帯の 3 対}:\ \textbf{機械のみ}\ \longrightarrow\ \textbf{紙の定理}(\text{SECT-CHIRAL})+\textbf{機械が供給した有限入力}(\mu(U),\mu(W)\ \text{の 2 行列})\ }$$
(**【GAP-G9-1】の特性性確認を条件とする**。格の名は **紙定理+機械入力** — §A.4 で 504×2/702/882 が cert の構造式 1 個を入力にしたのと**同種**であり、「機械のみ」より厳密に強い。**純紙ではない**ことは潰さない。)

### G.9.2 委嘱② — 掌性源の**三層成層**(台帳の最終形)

**統一の視点**: 三層はすべて**同一の紙道具 SECT(= Tool R2′)**の適用場面の違いにすぎない。

| 層 | 供給源 | SECT の形 | 検出コスト | 実例 | 格 |
|---|---|---|---|---|---|
| **層 1: Sylow 切片** | $q\ge5$ の巡回正規 Sylow $A$ | $\mathrm{Aut}(A)$ **可換** ⟹ SECT は $\mu(W)=1$ に退化し、$\widehat P_0^{\rm ab}$ の指数 3 と衝突して **$\mu(W)\ne1$ が強制** | **ゼロ**(指数と構造式だけ) | **L2 の 13/15**・非窓 11 対(§G.6.c) | **紙**(定理 MIRROR-ODD) |
| **層 2: $3^2$ SECT** | 特性 $3^2$ 切片で $\langle\mu(U),\mu(W)\rangle\not\cong S_3$ | $\mathrm{Aut}(A)=GL(2,3)$ **非可換** ⟹ 対の同時共役条件が本体 | **極小**($2\times2$ 行列 2 個・手検算可) | **帯の 3 対**(1296×2 相当・1728×1 相当のいずれか — cert の factor 別内訳参照) | **紙定理+機械入力** |
| **層 3: 非局所** | **どの特性切片にも像を残さない** | 全切片で SECT 成立するのに chiral | 大域($\mathrm{Aut}(\widehat P)$ 悉皆) | **`(1944,826)`・`(1944,921)`** の 2 対 | **機械のみ**(紙の裏づけゼロ) |

> ### ★ 層 3 の存在が確定したことの意味(**一級の陰性成果**)
> $$\boxed{\ \textbf{掌性は「特性切片の不変量」では汲み尽くせない — 反例が 2 標本、明示的に手元にある}\ }$$
> これは **CHARGE-LIMIT**(§G.5.3「抽象不変量は潰れうる・判定は $\mathrm{Aut}$ 直接探索まで降りる」)の**4 度目にして最も鋭い実例**であり、単なる教訓ではなく**定理の射程の下界**(局所理論では届かない)を与える。§G.8.3 で「差が出ない場合の意味」を先に固定しておいた設計が効いた。

### G.9.3 委嘱③ — **【文献要請】発火**(層 3 の 2 対について)

§G.8.3 の発火条件(「5 群でも全 chief factor が SECT を通ったら文献要請」)は **2 群で成立** ⟹ **発火する**。

> ## 【文献要請】掌性の非局所不変量(chirality group / chirality index)
> **宛先**: 司令塔(取り寄せ判断・機構抽出は文献ゲート)
>
> **① 具体的な困難(この設定の言葉で)**
> $\Gamma=C_2\ast C_3=PSL_2(\mathbf Z)$ の有限商 $\widehat P$($\lvert\widehat P\rvert=1944=2^3\cdot3^5$、`SmallGroup(1944,826)` と `(1944,921)`)を考える。標識対 $(U,W)$($U^2=W^3=1$、$\langle U,W\rangle=\widehat P$)の $\mathrm{Aut}(\widehat P)$-類は**ちょうど 2 個**で、$\nu:(U,W)\mapsto(U,W^{-1})$ がそれらを**入れ替える**(= 対応する正則地図が **chiral**、鏡映対を成す)。**ところが $\widehat P$ の主組成列のどの因子上でも、$\mu(U)$ を中心化しつつ $\mu(W)$ を反転する $h\in\mathrm{Aut}(A)$ が存在する**(SECT 全通過)。すなわち**掌性がどの特性切片にも像を残していない**。$3^2$ 因子をもつ他の 3 群では $GL(2,3)$ 内の同時共役条件が破れて掌性が説明できたので、**この 2 群だけが「非局所的に掌性をもつ」確定標本**である。
>
> **② 欲しい結果の型**
> - **(i)** **chirality group $X(\mathcal M)$ / chirality index** の定義と**計算法**(既に scout 済の **BJNS `math/0609070`** が主候補)。とくに「$X$ が非自明 ⟹ 局所(切片)不変量では検出できない」型の言明、あるいは逆に **$X$ を特性切片の言葉で下から評価する定理**があるか。
> - **(ii)** $(2,3)$-生成有限群(= $PSL_2(\mathbf Z)$ 商)で、**位数が $2^i3^j$** の場合の chirality の**判定法・族的な例**。とくに **$\lvert\widehat P\rvert=2^i3^j$ で chiral になる仕組み**の既知の説明。
> - **(iii)** 「掌性 = 標識対の Nielsen 類(T-system)の分裂」という定式化(発案札 α)と chirality group の**関係**。$\mathrm{Out}(\Gamma)=C_2$ 下で T-system が 1 個でも Aut-類が 2 個になる現象の**一般論**。
> - **(iv)**(あれば)**chirality index の下界**が群の構造(Sylow・Frattini 商・拡大類)から出る定理。
>
> **③ なぜ効くか**: 層 3 は現状**機械のみ**で、紙の道具が 1 つも届いていない。上の (i)(iv) のいずれかが降りれば **層 3 に紙の足場ができ**、帯の 5 対全部(さらに未掃引域)に射程が伸びる。降りてこなくても「非局所は本当に非局所」という**陰性の確認**になる。
> **④ 非接触**: 本要請は封印量・$\mathrm{Im}\,R$・L3 checker に無関係。外部検索は司令塔が実施(私は自分で漁らない)。

### G.9.4 台帳・格の更新(§G.3 の帯行を差し替え)

| 層 / カテゴリ | 対数 | 鏡映 | exotic | 掌性の格 |
|---|---:|---:|---:|---|
| 窓・指数 $(1000,2000]$・$2^i3^j$ | **5** | 5 | 0 | **3 対 = 紙定理+機械入力**(層 2・**【GAP-G9-1】条件つき**)/ **2 対 = 機械のみ**(層 3・文献要請発火) |

**予言の採点(墓標の更新)**: **P-BAND-2′ は的中**(予言 (ii)「5 chiral の少なくとも 1 因子で SECT が破れる」は **3/5 で成立**)。**部分的中**として記録する — 5/5 を予言していたので**全部当たったわけではない**。外れた 2 群が層 3 を露出させ、**結果的に最も価値のある情報**を出した(§G.8.3 で分岐の意味を先に決めておいた効果)。

## G.10 追補 7(2026-08-06・裁定 683 系)— **chirality group $X$ の自前計算**(設計・未実行)

**受領**: `papers/bjns-2009-chirality-groups-maps-hypermaps.pdf`(BJNS, arXiv `math/0609070v1`, 23 頁)+ トリアージ `docs/scout/bjns_retrieval_triage_v1.md`。
> **読解範囲の申告**: 私は**原著本文を読んでいない**。以下は**トリアージ経由の孫引き**(§3 Prop 2 / Thm 3 / Prop 5 / Cor 6 / Example 1 / Cor 9 / Thm 21 / Cor 22–25)。⟹ **【PIN-CHIR-1】** 定義の逐語確認(Prop 2 の 4 商の同型と Prop 5 の「$\mathrm{Mon}$ の正規部分群」)は**発火前に 1 回**取ること。

**司令塔の一工夫の受領**: 要請 (ii)(iii)(iv) は空振り ⟹ **文献は答えでなく測定器をくれた**。⟹ 層 3 の 2 標本の $X$ を**自前で計算**し、**位数・同型型・$\widehat P$ 内の位置**という最初の定量データを取る。本節はその**設計のみ**(実行しない)。

### G.10.1 我々の設定への翻訳

$\Gamma=C_2\ast C_3=\Delta^+$、窓 $N$ の像 $\bar N\trianglelefteq\Gamma$、反射 $r=\iota$(§A.2 MIRROR-PSL の正規化: $U\mapsto U,\ W\mapsto W^{-1}$)。BJNS の記号で $H=\bar N$、$H^r=\iota(\bar N)$、
$$H_\Delta=\bar N\cap\iota(\bar N),\qquad H^\Delta=\bar N\,\iota(\bar N),\qquad \boxed{\ X=H^\Delta/H=\bar N\iota(\bar N)/\bar N\ \trianglelefteq\ \mathrm{Mon}=\Gamma/\bar N=\widehat P\ },\qquad \kappa=\lvert X\rvert .$$
- $X=1\iff$ reflexible ✓(§F.10.3 の判定と同値)。
- **Cor 6**: $\kappa\mid\lvert\widehat P\rvert$($=1944$ 等)。
- **Prop 5**: $X$ は $\widehat P$ の**正規部分群**として実現 ⟹ 「$X$ が $\widehat P$ のどこに住むか」を問える ⟹ **層 3 の機構仮説を絞る量**になる。

> ### ★ 計算の鍵(本稿の観察・実装可能形)
> $\bar N$ が $\Gamma$ の**正規閉包**として $\bar N=\langle\langle r_1,\dots,r_k\rangle\rangle^\Gamma$ と書けるなら
> $$\iota(\bar N)=\langle\langle \iota(r_1),\dots,\iota(r_k)\rangle\rangle^\Gamma\ \Longrightarrow\ \boxed{\ X=\bigl\langle\bigl\langle\ \pi(\iota(r_1)),\dots,\pi(\iota(r_k))\ \bigr\rangle\bigr\rangle^{\widehat P}\ }\quad(\pi:\Gamma\twoheadrightarrow\widehat P)$$
> すなわち **$\widehat P$ の中で「反転した関係子の像」の正規閉包を取るだけ**。無限群 $\Gamma$ を扱わずに済む。
> ($r_j$ は $\widehat P$ の $(u,w)$ 上の表示の関係子。$\Gamma$ の関係 $u^2,w^3$ は $\iota$ で $u^2,w^{-3}$ に写り $\Gamma$ 内で自明 ⟹ $X$ に寄与しない ✓。)

### G.10.2 実測指示書 **CHIR-1**(数学者 → 実装係・凍結前の草案)

**入力**: `sg_g4_g5_orb_20260806.json` の各行の `(order,id)` と標識対 `rep_r/rep_s`(= $(U,W)$ に対応)。**36 群すべて**を対象(31 は control)。

```
P  := SmallGroup(order,id);
U  := rep_r;  W := rep_s;                      # cert の代表対をそのまま使う
# 1) (U,W) 上の有限表示を得る
iso := IsomorphismFpGroupByGenerators(P, [U,W]);   FP := Image(iso);
rels := RelatorsOfFpGroup(FP);                     # 語 = r_j
# 2) 反転写像 rho: u -> u, w -> w^-1 を語に適用(指数の一斉反転ではない! w だけ)
#    実装: 自由群の語を文字ごとに読み、生成元 2 (=w) の指数だけ符号反転
# 3) P へ引き戻す
imgs := [ Value(rho(r_j)) under u->U, w->W ];
X    := NormalClosure(P, Subgroup(P, imgs));
# 4) 記録
kappa := Size(X); IdGroup(X); IsAbelian(X);
IsSubset(Centre(P), X); IsSubset(FrattiniSubgroup(P), X); IsSubset(DerivedSubgroup(P), X);
# 5) X が覆う chief factor の同定(層2/層3 の判別に必須)
for each chief factor M/L of P: record  (X∩M)L/L ≠ 1 ?   and  SECT(M/L) pass/fail
```
**出力 cert**: `search/certs/chir1_<date>.json` — 行ごとに `order,id,kappa,X_idgroup,X_abelian,X_in_center,X_in_frattini,X_in_derived,covered_chief_factors[(index,size,sect_pass)]`。

**コスト**: 位数 $\le1944$ の群 36 個の `IsomorphismFpGroupByGenerators` + 正規閉包 ⟹ **数分**(`gap.ps1 -o 2g`)。

### G.10.3 カナリア(**実装の健全性 — 予言ではない**)

| # | 検査 | 根拠 |
|---|---|---|
| **C1** | **31 の reflexible 群で $\kappa=1$** | $X=1\iff$ reflexible(定義)。**1 個でも $\kappa\ne1$ なら実装バグ ⟹ STOP** |
| **C2** | 5 の chiral 群で $\kappa>1$ | 同上 |
| **C3** | $\kappa\mid\lvert\widehat P\rvert$ | **BJNS Cor 6** |
| **C4** | 鏡映対の**両 member で $\kappa$ 一致** | $\bar N\iota(\bar N)$ は対で共通 |
| **C5** | $\widehat P/X$ が **reflexible**(ORB/SECT を商上で再走) | **BJNS Thm 3**(最大 reflexible 商)。**最も強い検査** |
| **C6** ★ | $X$ の同型型が **BJNS Thm 21/Cor 22–25 の除外リスト**($S_n\,(n\ge3)$・$D_n\,(n>2)$ 等)に**入らない** | **文献が我々の計算を検算する**(逆向きの二系統)。入ったら実装か孫引きの誤り ⟹ STOP |

### G.10.4 IF-FIRST 予言(**各行に「偽ならどう変わるか」を明記** — §G.8.1 の再発防止規則の適用)

| # | 予言 | **偽なら測定値はどう変わるか**(検定力の担保) |
|---|---|---|
| **P-CHIR-1** | 5 群すべてで **$\kappa$ は 3 冪**($X\le O_3(\widehat P)$) | $\kappa$ が偶数 ⟹ 掌性の欠陥が 2-部にも住む ⟹ 「$\iota$ が $U$(位数 2)を固定し $W$(位数 3)を反転する」という非対称性が欠陥の所在を決めるという直観が誤り |
| **P-CHIR-2** ★本命 | **層 3 の 2 群で $X\le Z(\widehat P)$**(少なくとも $X\le\Phi(\widehat P)$) | $X\not\le\Phi$ なら欠陥は Frattini 商(最も見やすい特性切片)に像をもつ ⟹ 「局所で見えない」ことと衝突 ⟹ (H2) 中心拡大説は棄却され (H3) 大域説へ |
| **P-CHIR-3** | **層 2 の 3 群では $X$ が「SECT が破れた $3^2$ 因子」を覆う** | 覆っていなければ補題候補 SECT-COVER(§G.10.6)が偽 ⟹ SECT と $X$ は別物を測っていることになる |
| **P-CHIR-4** | $\kappa(\text{層 3})\le9$(小さく深い) | 大きい($\ge27$)なら欠陥は「広く薄い」⟹ 大域説 (H3) 側の証拠。**どちらでも情報が出る** |

### G.10.5 結果の読み方(**分岐表・発火前に固定**)

| 観測 | 層 3 の機構としての含意 | 次の一手 |
|---|---|---|
| $X\le Z(\widehat P)$ | **中心拡大の障害**(H2)。$\widehat P$ は reflexible な $\widehat P/X$ の中心拡大で、反射対称性が拡大類 $\in H^2(\widehat P/X,X)$ の水準でのみ壊れる | Part B の $Z^1/H^2$ 器具をそのまま流用して**紙の定理**を狙う(最有望) |
| $X\le\Phi$ だが非中心 | 深い非中心障害。局所不可視は説明できるが道具は未整備 | $X$ の $\widehat P/X$-加群構造を見る |
| $X\not\le\Phi$ | **層 3 の「局所不可視」と衝突** ⟹ SECT の検定が chief factor だけで足りていなかった疑い | 特性切片の取り直し(【GAP-G9-1】と同根) |
| $X=\widehat P$(totally chiral) | 最も劇的。BJNS §5 の族(Ree/Suzuki/$A_n$/$SL_d$)は非可解で、**可解 $2^i3^j$ の totally chiral は文献に例がない** ⟹ 新規例の候補 | 直ちに Sol 監査+新規性 grep |

### G.10.6 補題候補 **SECT-COVER**(本稿・candidate)

> $A=M/L$ を特性切片とし $\widehat P$ で **SECT が破れる**とする。もし $X$ の $A$ での像が自明($X\cap M\le L$)なら、$R:=\widehat P/X$ の中で $\bar M/\bar L\cong A$ が同じ $\mu(U),\mu(W)$ 作用で現れ、$R$ は reflexible(Thm 3)ゆえ **SECT は $A$ 上で成立**してしまう ⟹ 矛盾。
> $$\Longrightarrow\ \boxed{\ \textbf{SECT 破れ}\ \Longrightarrow\ X\ \textbf{はその因子を覆う}\ }$$
> ⚠ **穴**: $\bar M,\bar L$ が $R$ で**特性**であることを要する(【GAP-G9-1】と同型の注意)。⟹ 現状 **candidate**。P-CHIR-3 はこの補題の実測検定でもある。

### G.10.7 規律

- **本節は設計のみ・実行ゼロ**(GAP 起動なし)。**発火は司令塔**、実装は係。
- **【PIN-CHIR-1】**(BJNS 定義の逐語確認)を発火前に取ること。取れないなら $X$ の呼称を「$\bar N\iota(\bar N)/\bar N$」と**自前定義のまま**書き、chirality group の語を借りない。
- 出力の格: **candidate / single-system**。$\kappa$ の値そのものは機械値であり、**「層 3 の機構が同定できた」と書くには §G.10.5 の分岐 + 紙の定理が要る**。
- 封印非接触・L3 checker 非接触・外部検索ゼロ(文献は司令塔ゲート経由の受領物のみ)。

## G.4 これが効く先(1 行ずつ)

- **選択効果の会計**(cv9 判読の任務 3)に直接効く: 「L2 に exotic ゼロ」は**層の定義($c\in N$)が中心荷重型の exotic を構造的に殺した結果**であり、$\iota$-剛性の証拠として過大評価してはならない — **札 β-0 の主張のこの部分は正しく、重要**。
- **【GAP】追加なし**(本節は cert 読解と初等群論のみ。新しい未検証仮定を導入していない)。
- 発案札への差し戻し: 札 β-0 に **`in_PB3=False` の明示**と **750-クリーク(E2 型の実物)への格上げ**を反映されたい。EX-1(バケット算法)は**指数 750 の 5 元クリークを既に説明できる**ので、実行の主眼は「他の指数に同型のクリークがあるか」に絞れる。

## E. 帰属

- 双子 census = 裁定 548 W-1。鏡映を witness に使う着想 = **Sol F110-2.1**。$[-1,1]$ の shadow 性・$\ker T_{-1,1}=\iota(N)$・MIRROR-CRIT・ABEL-INDEX = **登録票 v1(数学者)**。
- **本稿の新規部分**: 補題 PSL-GEN / 補題 MIRROR-PSL / **定理 MIRROR-ODD**(+ 適用表)/ 補題 ABEL-TYPE / 命題 L3-KERNEL / 補題 L3-A,B,C / **定理 L3-CRIT** / 17 行予言表。
- S3.5 の枠組み(EMB-C・EMB-BRAID・EMB-LIN)= `bu_s35_embedding_v1.md`(数学者)。行の正本 = `h2_census_s4_20260805.json`(実装側)。**実測 16/64 の提示 = 司令塔(走行中更新)**。
