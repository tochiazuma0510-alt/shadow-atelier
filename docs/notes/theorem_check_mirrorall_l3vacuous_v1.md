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
> $N\trianglelefteq B_3$、$N\le PB_3$、$c\in N$ とする。ある素数 $q\ge5$ について
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

> ### 補題 ABEL-TYPE(candidate・本稿。ABEL-INDEX の強化)
> $c\in N$ で $P=F_2/N_{F_2}$ が可換なら
> $$\boxed{\ P\cong(\mathbf Z/n)^2\quad\text{または}\quad \mathbf Z/n\times\mathbf Z/3n\ (3\nmid n)\ }$$
> とくに **$P$ の各 Sylow 部分群は階数ちょうど 2(巡回でない)**。

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

## F.9 MIRROR-ALL 現況(一行)

$$\boxed{\ \textbf{15 対}\ =\ \underbrace{\textbf{13}}_{\text{紙の定理 MIRROR-ODD}}\ +\ \underbrace{\textbf{1}}_{\substack{\text{432: census 強制}\\ \text{(third-party 照合)}}}\ +\ \underbrace{\textbf{1}}_{\substack{\text{486: 同定待ち}\\ \text{(機械 2 系統は chiral)}}}\ }$$

⟹ **「この帯の双子対は全て鏡映対」は依然として定理ではない**(486 の 1 窓が紙でも第三者でも未閉)。ただし未閉部分は **1 窓・1 ビット**まで縮んだ。432 の決着は**紙 + 第三者**の合わせ技であり、**紙単独の射程は 13/15 のまま**である(この区別を報告で潰さないこと)。

## E. 帰属

- 双子 census = 裁定 548 W-1。鏡映を witness に使う着想 = **Sol F110-2.1**。$[-1,1]$ の shadow 性・$\ker T_{-1,1}=\iota(N)$・MIRROR-CRIT・ABEL-INDEX = **登録票 v1(数学者)**。
- **本稿の新規部分**: 補題 PSL-GEN / 補題 MIRROR-PSL / **定理 MIRROR-ODD**(+ 適用表)/ 補題 ABEL-TYPE / 命題 L3-KERNEL / 補題 L3-A,B,C / **定理 L3-CRIT** / 17 行予言表。
- S3.5 の枠組み(EMB-C・EMB-BRAID・EMB-LIN)= `bu_s35_embedding_v1.md`(数学者)。行の正本 = `h2_census_s4_20260805.json`(実装側)。**実測 16/64 の提示 = 司令塔(走行中更新)**。
