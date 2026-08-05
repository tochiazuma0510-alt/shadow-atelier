# EXSEQ-LIM v1.1 — 便 105 F105-1.3 の補筆 5 点(addendum・**v1 本文は 1 バイトも改変しない**)

**状態札: `candidate(証明ノート・紙のみ / Lean 検証ではない / cross-checked でもない / 単系統 / 封印非接触 / novelty 主張なし)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05
- 委嘱: 司令塔「`sol/sol_reply_105_math32.md` **F105-1.3** が挙げた 5 点を addendum で閉じよ(本文不改変)」
- 対象: `docs/notes/tb_exseq_lim_proof_v1.md`(以下 **v1**)。**v1 の §0–§11・付録 A はすべて不改変**。本 addendum は CV-10 の意味で当該 5 項目の **effective source** である。
- 原典: `papers/sga1-grothendieck-raynaud-arxiv0206203.pdf`(**頁対応: 新頁 = PDF − 16**)
- **格の扱い**: F105-1.3 の裁定どおり、`[TB: canonical-source-pinned/v2](条件履行 = v2.1)` は**維持**する。本 addendum は格を上げない。旧 PASS の巻き戻しもしない。

---

## 0. 5 点の対応表(先に一覧)

| # | F105-1.3 の指摘(逐語要旨) | 本 addendum の該当節 | 処理 |
|---|---|---|---|
| **1** | 冒頭は SGA 入力を 3 件と数えるが §7.4 で Cor. 4.8 を使うので実際は **4 件** | **§1** | ★ **会計を 4 件へ訂正**(BF-4 を新設・pin と照合状態を明記) |
| **2** | affine finite étale cover ↔ 有限 étale algebra の対応、affine sheaf $\Omega$ ↔ Kähler module の同定を「認める」としており、**自前証明だけという会計ではない** | **§2** | ★ **「認めている事実」の正直な会計欄**を新設(3 件・各々の依存の向きと、使っている箇所を明示) |
| **3** | 有限段で射が isomorphism になる箇所は、**射だけでなく inverse と二つの恒等式**をさらに有限段へ降ろす一行が要る | **§3** | ★ **補題 LIM-D′** を追加(2 行)+ v1 の該当 3 箇所へ適用 |
| **4** | EXSEQ-LIM (3) は abstract group isomorphism まで。profinite exact sequence に使うなら **topology・continuity・compact-to-Hausdorff** を明記せよ | **§4** | ★ **定理 EXSEQ-LIM (3′)** を追加(位相の定義・連続性・同相の 3 段) |
| **5** | §0 は relative への障害を **Ihara ③-1 一点**とするが、§10 は **③-1 と block ④ Abhyankar の二点**を正しく列挙する。前者を訂正せよ | **§5** | ★ **§0 判定 3 の逐語訂正**(1 点 → 2 点) |

> **本 addendum が新たに使う外部入力: SGA 1 Exp. I Cor. 4.8 の 1 件のみ**(v1 §7.4 で既に使用済のものを、会計表へ正式に載せる)。**新しい文献を開いていない。【文献要請】は起票しない。**

---

## 1. 【補筆 1】SGA 入力の会計を **3 件 → 4 件** に訂正

### 1.1 訂正する箇所(v1 §0 判定 2 の逐語)

> ~~「使う外部入力は **SGA 1 Exp. I の 3 項目(Prop. 3.1・Déf. 4.1・Déf. 4.9)= すべて `present`/定義**のみ」~~

**正文(以後これを引く)**:

> 使う外部入力は **SGA 1 Exp. I の 4 項目(Prop. 3.1・Déf. 4.1・Déf. 4.9・Cor. 4.8)**であり、**すべて `present`(証明本文つき)または定義**である。

### 1.2 会計表 v1.1(v1 §2.2 の表に **BF-4** を追加)

| # | 内容 | pin | 照合 | `proof_body_status` | 使用箇所 |
|---|---|---|---|---|---|
| **BF-1** | net(非分岐)$\iff\Omega^1_{X/Y}$ が $x$ で零 | SGA 1 Exp. I, **Prop. 3.1 (ii)**(PDF 18 / 新頁 2) | 150 dpi 画像✓ | **present** | v1 §5 (net)・§3 |
| **BF-2** | étale = plat + net | SGA 1 Exp. I, **Déf. 4.1 a)**(PDF 20 / 新頁 4) | 150 dpi 画像✓ | **定義** | v1 §3・§5 |
| **BF-3** | revêtement étale = fini + étale | SGA 1 Exp. I, **Déf. 4.9**(PDF 21 / 新頁 5) | テキスト(pdftotext) | **定義** | v1 §3・§5 |
| ★ **BF-4**(**新規計上**) | $X'$ が $Y$ 上 net、$X$ が $Y$ 上 étale ⟹ $g:X\to X'$ は étale | SGA 1 Exp. I, **Cor. 4.8**(PDF 19–20 / 新頁 3–4) | テキスト(pdftotext)。**150 dpi 画像照合は未実施 —【残件 A-1】** | **present**(Cor. 4.8 は Prop. 4.7/4.5 系列から本文で導かれる) | ★ **v1 §7.4 の ★**($\mathcal C_K/U_{K_i}\simeq\mathcal C_{K_i}$ の一段) |

> ### ★ なぜ v1 が数え落としたか(自認)
> v1 §2.2 の表は「**§3–§7 の主線(LIM-A〜LIM-D と EXSEQ-LIM (1)(2)(3))**で使う入力」を数えており、**§7.4 の接続段(EXSEQ-STAB との突合 = 補題 L-6 の補完)**で使う Cor. 4.8 を表に載せなかった。v1 §0 判定 2 の文が「本ノートが使う外部入力」と**ノート全体**を主語にしているため、この会計は誤りである。**主線だけなら 3 件、ノート全体なら 4 件**であり、後者が正しい会計単位である。
> なお v1 の付録 A には Cor. 4.8 の行が既に存在した(「テキスト」照合)。**付録 A と §2.2 の間の不整合**であり、Sol の指摘は付録 A 側が正しいことを追認している。

### 1.3 【残件 A-1】(新規・小)

> **Cor. 4.8 の逐語画像照合が未実施。** BF-1/BF-2 は 150 dpi 画像で逐語照合済だが、BF-3/BF-4 は pdftotext のみである。**BF-4 は §7.4 の一段に load-bearing** なので、次の原典照合機会に **PDF 19–20 の画像照合**を行う。
> **現状の格への影響**: BF-4 は `present` の定理であり内容の読みも一意だが、**「画像照合済」とは書かない**(v1 付録 A の表記を維持)。

---

## 2. 【補筆 2】「認めている事実」の正直な会計欄(**自前証明だけという会計ではない**)

F105-1.3 item 2 の指摘は正当である。v1 は §2.3 の注で **1 件だけ**(SGA の $\Omega^1=\mathcal I/\mathcal I^2$ と Kähler 微分の同一視)を「標準事実を使う(申告)」と書いたが、**実際にはもう 2 件、圏の記述の水準で認めている事実がある**。ここに 3 件すべてを列挙する。

### 2.1 認容事実の表(★ = v1 で申告済 / ☆ = 本 addendum で新たに申告)

| # | 認めている事実 | v1 で使う箇所 | 依存の向き | 証明を書かない理由 |
|---|---|---|---|---|
| **AC-1** ★ | SGA 1 Exp. I §1 の $\Omega^1_{X/Y}=\mathcal I/\mathcal I^2$(対角イデアル定義)と、**アフィンの場合の Kähler 微分加群 $\Omega_{B/A}$**(普遍導分 $b\mapsto\overline{b\otimes1-1\otimes b}$)の同一視 | §5 LIM-C の (net) 段(BF-1 を $\Omega_{B_i/A_{K_i}}$ に対して使う) | **BF-1 を使うために必要**。これが無いと BF-1 の $\Omega^1$ と EL-2 の $\Omega_{B/A}$ が別物になる | 標準(EGA IV 16.3 / SGA 1 Exp. I §1 の脚注)。**v1 は EL-2 を自前証明したので、この同一視だけが残っている** |
| **AC-2** ☆ | **アフィン化**: $U_L=\mathrm{Spec}\,A_L$ 上の**有限 étale スキーム $W$** は affine であり、$W\mapsto B=\mathcal O(W)$ は圏 $\mathcal C_L$ と「有限 étale $A_L$-代数の圏」の**反変同値**を与える | §3 LIM-A(「$B:=\mathcal O(W)$ と置く」)・§4 LIM-B・§6 LIM-D(「$\mathcal C$ の射は $\mathcal O$ の $A$-代数準同型の逆向き」) | **v1 の全経路の前提**。これが無いと「幾何的対象 = 構造定数の有限データ」という新経路の出発点が立たない | 有限射はアフィン射(定義)、底がアフィンなら全空間もアフィン、$\mathrm{Spec}$ と大域切断の随伴 — いずれも scheme 論の標準。**本ノートの新規性はここにはない** |
| **AC-3** ☆ | **アフィン層の同定**: $W$ が affine のとき、層 $\Omega^1_{W/U_L}$ の大域切断が加群 $\Omega_{B/A_L}$ であり、**層が零 $\iff$ 加群が零** | §5 LIM-C(BF-1 の「$\Omega^1_{X/Y}$ が零」を「$\Omega_{B/A}=0$」と読む段) | AC-1 と対で必要。AC-1 が「どの加群か」、AC-3 が「層と加群のどちらで零を判定してよいか」 | 準連接層の標準(アフィン上では大域切断関手が完全・忠実)。**AC-1 と一体で 1 件と数えてもよいが、Sol の指摘に合わせて分離して申告する** |

### 2.2 ★ 会計の正文(v1 §0 判定 2 の第 2 文の読み替え)

> ~~「他はすべて初等代数(PID 上の有限自由性・多項式恒等式の降下・$\Omega$ の底変換)で、**本ノートが自前で証明を書いた**」~~

**正文**:

> 他の**代数的**な入力(PID 上の有限生成捩れなし加群の自由性・多項式恒等式の降下・$\Omega$ の底変換 EL-2)は本ノートが自前で証明を書いた。ただし、**幾何的対象を代数のデータへ翻訳する 3 件(AC-1/AC-2/AC-3)は標準事実として認めており、本ノートは証明を書いていない**。
> ⟹ 正確な会計は「**外部入力 = SGA 1 の 4 件 + 認容する標準事実 3 件**、**自前証明 = EL-1, EL-2, LIM-A, LIM-B, LIM-C, LIM-D, EXSEQ-LIM (1)(2)(3) と本 addendum の LIM-D′, (3′)**」である。

> ### ⚠ この訂正が意味すること(過小評価も過大評価もしない)
> - **旧経路(v2.1 §4.3)との比較(v1 §1 の表)は不変**である。旧経路も AC-1〜AC-3 を同じだけ使ったうえで、**さらに**正規化の底変換可換性・非エタール軌跡の閉性を背負っていた。**債務 2 件が消えたという結論は動かない。**
> - しかし「**自前証明だけ**」「**債務ゼロ**」という v1 の言い切りは**過剰**だった。正しくは「**SGA 1 の外に出る債務がゼロ**」であり、「認容事実がゼロ」ではない。
> - AC-1〜AC-3 はいずれも `present` な原典 pin を取ろうと思えば取れる標準事実である(EGA I/II の $\mathrm{Spec}$-大域切断随伴、EGA IV 16.3)。**しかしそれは正典外**なので、**本 addendum は pin を取らず「認容」として開示するに留める**。**【文献要請】の型ではない**(困難ではなく、単に会計の可視化である)。

---

## 3. 【補筆 3】有限段での isomorphism — **inverse と二恒等式の降下**(補題 LIM-D′)

F105-1.3 item 3 の指摘は正当である。v1 の LIM-D(§6)は $\varinjlim_j\mathrm{Hom}\to\mathrm{Hom}$ の全単射しか主張していないが、v1 は 3 箇所で「有限段で**同型**が得られる」ことを暗に使っている。**Hom の全単射は、射の降下しか与えない。**

### 3.1 ★ 補題 **LIM-D′**(iso の降下)

> **補題 LIM-D′.** $i\in I$、$V,V'\in\mathcal C_{K_i}$ とし、$\phi:\rho_iV\to\rho_iV'$ が $\mathcal C_{\bar{\mathbf Q}}$ の**同型**であるとする。このとき、ある $j\ge i$ と $\mathcal C_{K_j}$ の**同型** $\phi_j:\rho_{ij}V\to\rho_{ij}V'$ が存在して $\rho_j(\phi_j)=\phi$ となる。
>
> **証明.** $\psi:=\phi^{-1}$ と置く。LIM-D(全射性)を $\phi$ と $\psi$ に別々に適用し、$j_1\ge i$ と $\phi_{j_1}$、$j_2\ge i$ と $\psi_{j_2}$ を得る。$I$ は有向なので $j\ge j_1,j_2$ を取り、両者を $\mathcal C_{K_j}$ へ底変換して $\phi_j,\psi_j$ とする。
> 二つの恒等式 $\psi_j\circ\phi_j=\mathrm{id}_{\rho_{ij}V}$ と $\phi_j\circ\psi_j=\mathrm{id}_{\rho_{ij}V'}$ は、**$\mathcal C_{K_j}$ の Hom 集合における 2 つの等式**である。底変換 $\rho_j$ でこれらは $\psi\circ\phi=\mathrm{id}$、$\phi\circ\psi=\mathrm{id}$ に写り、これは仮定より真。**LIM-D の単射性**($\varinjlim_{j'\ge i}\mathrm{Hom}\to\mathrm{Hom}$ が単射)により、$\psi_j\circ\phi_j$ と $\mathrm{id}$ は**ある $j'\ge j$ で既に一致する**(単射性は「底変換後に一致する 2 射は、十分先の有限段で一致する」を含む — v1 §6 の (単射) 段が $A_{K_{j'}}\hookrightarrow A_{\bar{\mathbf Q}}$ の単射性から与えているのは、まさにこの形である)。同様に第 2 恒等式についても $j''$ を取り、$j'''\ge j',j''$ で両方が成立する。この $j'''$ が求める段であり、$\phi_{j'''}$ は同型。∎

> ★ **一行で**: 「射は降りる」だけでは足りず、「**逆射も降りる**」と「**二つの合成が有限段で恒等になる**」の 3 つを別々に降ろす。有向性で 3 つの段を合流させる。

### 3.2 v1 の該当箇所への適用(3 箇所)

| # | v1 の箇所 | 何が「同型」か | LIM-D′ の適用形 |
|---|---|---|---|
| **(i)** | §4 LIM-B 末「$e_l\otimes1\mapsto e_l$ が $A_{\bar{\mathbf Q}}$-代数同型を与える」 | ここは **LIM-D′ 不要**。両辺の自由基底を明示的に対応させており、逆写像も同じ基底で明示できる(**構成的**)。 | — |
| **(ii)** | §7.3(3)の**単射性**「$V\cong\rho_i(V_i)$ なる $i,V_i$ がある。$\sigma$ は自然変換だからこの同型と可換で」 | $\mathcal C_{\bar{\mathbf Q}}$ の同型 $V\cong\rho_iV_i$ | ★ **不要**(この同型は $\mathcal C_{\bar{\mathbf Q}}$ の中で使うだけで、有限段へ降ろしていない)。**LIM-A+LIM-B+LIM-C の本質的全射性がそのまま与える。** |
| **(iii)** ★ | §7.3(3)の**全射性・well-defined 性**「別の表示 $V\cong\rho_{i'}(V_{i'})$ に対し $j\ge i,i'$ を取れば **LIM-D(充満忠実)により $\rho_{ij}V_i\cong\rho_{i'j}V_{i'}$ が $\mathcal C_{K_j}$ で成り立ち**」 | ★ **ここが指摘の対象**。$\mathcal C_{\bar{\mathbf Q}}$ で $\rho_iV_i\cong V\cong\rho_{i'}V_{i'}$ という同型があり、それを **$\mathcal C_{K_j}$ の同型として**必要としている | ★ **LIM-D′ をここへ適用する。** 「LIM-D により」を「**LIM-D′ により**」へ読み替え、必要なら $j$ を LIM-D′ が与える段へ取り直す($I$ 有向ゆえ可能)。$\sigma^{(j)}$ の自然性はこの $\mathcal C_{K_j}$-同型に対して使うので、**同型が $\mathcal C_{K_j}$ の中に実在すること**が要る。 |

> ### ★ 訂正の正文(v1 §7.3 定理 EXSEQ-LIM (3) 証明・全射性段)
> > **well-defined**: 別の表示 $V\cong\rho_{i'}(V_{i'})$ に対し $j\ge i,i'$ を取れば ~~LIM-D(充満忠実)~~ ★ **LIM-D′(iso の降下・本 addendum §3.1)** により $\rho_{ij}V_i\cong\rho_{i'j}V_{i'}$ が **$\mathcal C_{K_j}$ の同型として**成り立ち(必要なら $j$ を取り直す)、$\sigma^{(j)}$ の自然性と系の両立性から両者は一致する。
>
> **これは証明の修理であって結論の変更ではない。** EXSEQ-LIM (3) の主張形は不変。

---

## 4. 【補筆 4】EXSEQ-LIM (3) の **profinite 強化**

F105-1.3 item 4 の指摘は正当である。v1 §7.3 は $\mathrm{Aut}(F_{\bar{\mathbf Q}})\xrightarrow{\sim}\varprojlim_i\mathrm{Aut}(F_{K_i})$ を**抽象群の同型**としてしか示していない。v2.1 §3.4 の完全列は **profinite 群の完全列**なので、位相を明示する。

### 4.1 位相の定義(v1 に無かった一段)

> ### 定義 TOP-AUT
> $L$ を $K\subseteq L\subseteq\bar{\mathbf Q}$ の体、$F_L:\mathcal C_L\to\mathbf{FinSet}$ を v1 §2.1 の繊維関手とする。
> $$\mathrm{Aut}(F_L)\ \subseteq\ \prod_{W\in\mathrm{Ob}(\mathcal C_L)}\mathrm{Sym}\bigl(F_L(W)\bigr)$$
> を、右辺(**有限離散群の直積 = compact Hausdorff totally disconnected**)の**部分空間位相**を入れた位相群とする。

> ### 補題 TOP-1($\mathrm{Aut}(F_L)$ は profinite)
> $\mathrm{Aut}(F_L)$ は上の直積の**閉部分群**であり、したがって **profinite**(compact・Hausdorff・全不連結)である。
> **証明.** 元 $(\sigma_W)_W$ が $\mathrm{Aut}(F_L)$ に属する条件は
> $$\forall\,(g:W\to W')\in\mathrm{Mor}(\mathcal C_L):\quad F_L(g)\circ\sigma_W=\sigma_{W'}\circ F_L(g)$$
> であり、各条件は**座標 $W,W'$ の 2 つだけに依存する条件**である。$\mathrm{Sym}(F_L(W))$ は離散(有限集合上の全単射の有限群)なので各条件は閉集合を定め、その交わりも閉。閉部分空間ゆえ compact、直積が Hausdorff・全不連結ゆえ部分空間も同様。群演算(合成・逆)は各座標で連続。∎
> > ⚠ **射の集合が真クラスでないこと**: $\mathcal C_L$ は $A_L$ 上有限自由な代数の圏(LIM-A)なので、同型類の集合は小さく、骨格を取れば小圏である。位相はこの骨格上の積で定める(同型類の代表の取り方に依らないことは、自然変換の定義から従う)。

### 4.2 ★ 定理 **EXSEQ-LIM (3′)**(位相つき)

> **定理 EXSEQ-LIM (3′).** v1 §7.3 の群同型
> $$\Lambda:\ \pi_1(U_{\bar{\mathbf Q}},\vec{01})=\mathrm{Aut}(F_{\bar{\mathbf Q}})\ \xrightarrow{\ \sim\ }\ \varprojlim_{i\in I}\mathrm{Aut}(F_{K_i})$$
> は**位相群の同型(同相)**である。ここで右辺は各 $\mathrm{Aut}(F_{K_i})$ に定義 TOP-AUT の位相を入れた逆極限(積位相の部分空間)である。
>
> **証明(3 段)**。
> **(a) 右辺は profinite。** 補題 TOP-1 より各 $\mathrm{Aut}(F_{K_i})$ は profinite。profinite 群の逆極限は積の閉部分群として profinite(とくに **Hausdorff**)。
> **(b) $\Lambda$ は連続。** 積位相の普遍性より、各 $i$ について $\Lambda_i:\mathrm{Aut}(F_{\bar{\mathbf Q}})\to\mathrm{Aut}(F_{K_i})$ の連続性を見ればよい。さらに $\mathrm{Aut}(F_{K_i})$ の位相は $\mathrm{Sym}(F_{K_i}(V))$($V\in\mathcal C_{K_i}$)への射影で生成されるので、各 $V$ について合成
> $$\mathrm{Aut}(F_{\bar{\mathbf Q}})\ \xrightarrow{\ \Lambda_i\ }\ \mathrm{Aut}(F_{K_i})\ \xrightarrow{\ \mathrm{pr}_V\ }\ \mathrm{Sym}\bigl(F_{K_i}(V)\bigr)$$
> の連続性を見ればよい。**EXSEQ-LIM (2)**(v1 §7.2)の自然同型 $F_{\bar{\mathbf Q}}\circ\rho_i\cong F_{K_i}$ は**有限集合の全単射** $\beta_V:F_{K_i}(V)\xrightarrow{\sim}F_{\bar{\mathbf Q}}(\rho_iV)$ を与え、$\Lambda_i$ の定義は $(\Lambda_i\sigma)_V=\beta_V^{-1}\circ\sigma_{\rho_iV}\circ\beta_V$ である。ゆえに上の合成は
> $$\mathrm{Aut}(F_{\bar{\mathbf Q}})\ \xrightarrow{\ \mathrm{pr}_{\rho_iV}\ }\ \mathrm{Sym}\bigl(F_{\bar{\mathbf Q}}(\rho_iV)\bigr)\ \xrightarrow{\ \mathrm{conj}\ \beta_V\ }\ \mathrm{Sym}\bigl(F_{K_i}(V)\bigr)$$
> と分解する。第 1 矢は**定義 TOP-AUT の座標射影**(連続)、第 2 矢は**有限離散群の間の群同型**(連続)。ゆえに $\Lambda_i$ は連続。
> **(c) compact → Hausdorff。** $\Lambda$ は (b) より連続、v1 §7.3 より**全単射**、定義域は補題 TOP-1 より **compact**、値域は (a) より **Hausdorff**。連続全単射 compact→Hausdorff は閉写像、したがって**同相**。∎

> ### ★ どこで「有限深度から profinite へ渡っている」か(1 行)
> **(b) の要点は「$\Lambda$ の各座標が、値域側の有限離散群への写像として、定義域側のただ 1 つの座標のみに依存する」ことである。** 位相の情報はここで尽きており、残りは (c) の標準論法が引き受ける。**逆写像の連続性を直接構成する必要はない** — これが compact-to-Hausdorff を使う理由である。

### 4.3 v2.1 §3.4 の完全列への接続(位相の申し送り)

v1 §7.4 は $\varprojlim_i\mathrm{Stab}_\pi(a_i)=\bigcap_i\mathrm{Stab}_\pi(a_i)=\ker(p:\pi\to G_K)$ を使う。位相つきで読むと:

- $\mathrm{Stab}_\pi(a_i)\le\pi$ は**開かつ閉**(有限集合 $F_K(U_{K_i})$ への連続作用の点安定化群)。
- ゆえに $\bigcap_i\mathrm{Stab}_\pi(a_i)$ は $\pi$ の**閉**部分群であり、部分空間位相で profinite。
- **定理 (3′)** と合わせて、$\pi_1(U_{\bar{\mathbf Q}},\vec{01})\to\pi$ の像は $\ker p$ に**位相群として**同型に写る。⟹ v2.1 §3.4 の短完全列は **profinite 群の短完全列**として意味をもつ。

> ⚠ **本 addendum が主張しないこと**: 上の 3 点は「(3′) を完全列へ接続する際の読み方」であって、**v2.1 §3.4 の完全列そのものの完全性の証明ではない**(それは L-4 = EXSEQ (a)(b) と L-6 = EXSEQ-STAB の担当・v1 §9 の消し込み表のとおり)。ここで閉じたのは **L-7 の位相版**だけである。

---

## 5. 【補筆 5】§0 判定 3 の逐語訂正 — **relative への残存障害は 1 点 → 2 点**

### 5.1 訂正する箇所(v1 §0 判定 3 の逐語)

> ~~「**relative への残存障害は Ihara ③-1($\pi_1^{\rm geom}\cong\hat F_2$ の `omitted`)ただ 1 点に絞られた**(§10)」~~

**正文(以後これを引く)**:

> ★ **`canonical-source-relative` への残存障害は 2 点である**:
> **(③-1)** Ihara ③-1($\pi_1^{\rm geom}\cong\hat F_2$)= `omitted / silent_omission`、および
> **(④)** Deligne 15.23 PREUVE の **Abhyankar** = `external_reference`(**v1 の射程外・未検討**)。

### 5.2 これは v1 の内部不整合の訂正である(新事実ではない)

v1 §10.1 の表と boxed 結論は**最初から 2 点**を正しく列挙していた:

> 「$\boxed{\textbf{★ }\texttt{relative}\textbf{ への残存障害は }\mathbf{2}\textbf{ 点に絞られた: ③-1(Ihara の }\hat F_2\textbf{ 自由性)と ④ の Abhyankar。}}$」

**誤っていたのは §0 判定 3 の 1 文だけ**であり、§10 は正しい。Sol の指摘は「前者を二点へ訂正せよ」= §0 を §10 に合わせよ、という**内部整合の要求**である。**外部の事実関係は何も変わらない。**

### 5.3 ★ ②(EXSEQ-STAB / EXSEQ-LIM)についての **P-2 の未決を再掲**

さらに正確を期すため、v1 §11 の監査点 P-2 が**未決である**ことを §0 の読者にも見えるようにしておく:

> ブロック ② の `reader_exercise`(SGA 1 V 6.13 / IX 6.1)は、**工房補題 L-6 / L-7 が `present` で代替している**。この代替を `canonical-source-relative` の条件充足として数えてよいかは **司令塔・Sol の裁定事項**であり、**v1 も本 addendum も「数えてよい」とは主張しない**。
> ⟹ したがって残存障害の正確な言い方は:
> $$\boxed{\ \textbf{P-2 を「数えてよい」と裁定した場合に}\ \textbf{残る障害が 2 点(③-1 と ④)。裁定前は ② の代替可否も未決のまま。}\ }$$

---

## 6. 本 addendum 後の状態

### 6.1 v1 §9(工房債務 L 系)への差分

| # | 補題 | v1 での状態 | ★ 本 addendum 後 |
|---|---|---|---|
| **L-7** | EXSEQ-LIM | 「本ノートで完全証明(債務 2 件は消滅)」 | ★ **証明本文つき・単系統**は不変。**追加**: (i) 会計は SGA 4 件 + 認容 3 件(§1・§2)、(ii) iso 降下の一行を補完(§3)、(iii) **profinite 版 (3′) を追加**(§4)。**「完全」という語は §2.2 の会計の下で読む** |
| L-1〜L-6 | 各行 | — | **不変**(本 addendum は触れない) |

### 6.2 格(不変)

$$\boxed{\ \texttt{[TB: canonical-source-pinned/v2]}\ \textbf{(条件履行 = v2.1)を維持。本 addendum は格を上げない。}\ }$$

- `cross-checked` / `verified` — **付さない**(機械計算ゼロ・Lean 未使用・単系統・起草者は v1 と同一)。
- **novelty** — 主張しない。
- $\varepsilon$ / exact (TB4) / $(Z_{2M}$-link$)$ / $K^{(5)}$ の値・窓データ・封印欄 — **一切触れていない**。
- **本 addendum で新たに開いた原典頁: なし**(BF-4 = Cor. 4.8 は v1 §7.4 で既に開いていたものを会計表へ載せただけ)。

### 6.3 【GAP】/【残件】

| 札 | 内容 | 状態 |
|---|---|---|
| ★ **【残件 A-1】**(新規・小) | **SGA 1 Exp. I Cor. 4.8 (BF-4) の 150 dpi 画像照合が未実施**(pdftotext のみ)。§7.4 の一段に load-bearing | **OPEN**(次の原典照合機会に処理・**発火や格に依存しない**) |
| **AC-1 / AC-2 / AC-3** | 認容する標準事実 3 件(§2.1)。正典外なので pin を取らず開示に留める | **申告済**(債務ではなく**会計の可視化**) |
| **P-2**(v1 §11) | 工房補題が `reader_exercise` pin を代替して `relative` を数えてよいか | **未決**(司令塔・Sol の裁定事項・§5.3) |
| ③-1 / ④ | `relative` への残存障害 2 点(§5.1) | **UNKNOWN**(③-1)/ **未検討**(④・v1 射程外) |

---

## 7. Sol への監査点(2 点・便 106 用)

> **Q-1 ★★ 定理 EXSEQ-LIM (3′) の (b) 段**(§4.2)。「$\Lambda$ の各座標が定義域のただ 1 つの座標に依存する」という分解が、**EXSEQ-LIM (2) の自然同型 $\beta$ を経由して**正しく書けているか。とくに $\beta_V$ が **$V$ について自然**であること(v1 §7.2 の主張)が、$\Lambda_i$ が $\mathrm{Aut}(F_{K_i})$ に**実際に着地する**(単なる座標族でなく自然変換になる)ために使われている点。
>
> **Q-2 ★ 補題 LIM-D′**(§3.1)。「2 つの恒等式を有限段へ降ろす」段で、**LIM-D の単射性が『底変換後に一致する 2 射は十分先の有限段で既に一致する』を含む**と読んだ(v1 §6 の (単射) 段が $A_{K_j}\hookrightarrow A_{\bar{\mathbf Q}}$ の単射性から与えている形)。この読みが v1 §6 の証明の逐語と整合しているか。**もし LIM-D の単射性が「同じ $j$ での 2 射」しか比べていないなら、LIM-D′ は $j$ の取り直しを 1 段追加する必要がある**(本 addendum は取り直しを明示的に書いたので結論は変わらないが、依存の記帳が変わる)。

---

## 付録 B. 本 addendum が **v1 のどの文字も書き換えていない**ことの確認

- 本 addendum は **新規ファイル** `docs/notes/tb_exseq_lim_proof_v1_1_addendum.md` である。
- `docs/notes/tb_exseq_lim_proof_v1.md` は**読み込みのみ**で、編集していない。
- 訂正は §1.1 / §2.2 / §3.2 / §5.1 で「**撤回する文(取消線)+ 正文**」の形で示し、**v1 側は原状のまま保存**する(versioned 規律・CV-10 の effective source 方式)。
