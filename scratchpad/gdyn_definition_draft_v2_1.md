# $G_{\rm dyn}$ 定義起草 **v2.1** — 定理 DYN-NOGO・二窓テスト・$T/O$ の明示化

`DIR: 正側(算術像の上界)/ FRAME: Out(F̂₂) を力学で切る`

> **v2.1 について(先に読むこと)**: 委嘱の修文 3 点(①kernel 経由の一行 ②有限指数が load-bearing ③系を (G-1) 限定 + (G-2) 単独 witness 併記)、および射程明記・一般補題化は、**すべて v2 の §1・§7 に既に反映済**である(v2 sha16 `5886e2483137646b`)。⟹ **v2.1 の実質差分は §8 のみ** — v2 の証明を精査した結果、**同じ仮定から結論が 3 本取れる(等号版)**ことが分かったので、補題を鋭形へ強化し、そこから**新しい系 VE-COF(「(G-2) 窓は決して cofinal にならない」)**と実務用の必要条件 VE-TEST を導いた。§1–§7 は 1 バイトも改変していない。

**状態札**: `§1 = ★補題 VE-NOGO + 系 DYN-NOGO(paper-proof・falsifier 独立検証 PASS)/ §2 = 撤回 2 件 / §3 = 実装仕様 v2(candidate)/ §4 = T/O の分岐データ(式から自前導出・機械検算なし)/ §5 = prereg 文 / §7 = falsifier 検証記録 / §8 = ★鋭形 VE-NOGO⁺ + 系 VE-COF + VE-TEST(v2.1 新設・paper-proof・未監査)/ novelty は [12][14] の UNVERIFIED 債務に依存`

- 起草: 影工房 数学者(Opus 5)/ 2026-08-26 / **v1(`gdyn_definition_draft_v1.md`)は 1 バイトも改変せず並置**。v1 の §1(Wood 射程判定)・§2(定義)は**そのまま有効**。差分は本 v2 の §1–§5。
- 契機: implementer の P-DYN-1 初測定(cert `gdyn_p_dyn1_972_v1_20260826.json`)で **G-2 が両写像 FAIL**。根因は窓固有ではなく**私の設計の誤り**と判明。

---

## §1 ★補題 VE-NOGO(一般形)と系 DYN-NOGO

**falsifier 独立検証 = PASS**(別証明 = $\pi\circ\psi$ の経由分解・数値 5291 構成で反例 0)。以下は falsifier の修文 5 点を織り込んだ最終形。

### 1.1 一般補題(力学固有ではない)

> ### 補題 VE-NOGO
> $G_0$ を群、$H\lneq G_0$ を**真の**部分群、$\psi:H\twoheadrightarrow G_0$ を**全射**準同型(= 定義域が真部分群の**仮想自己準同型**)とする。$N\trianglelefteq G_0$ を**有限指数**の正規部分群とする。もし
> $$\text{(G-2)}\qquad \psi(N\cap H)\subseteq N$$
> ならば **$NH=G_0$**(= 下記の**退化枝**)。
> **系(G-1 版)**: さらに $N\subseteq H$(G-1)ならば $NH=H=G_0$ となり $H\lneq G_0$ に矛盾。
> $$\boxed{\ \textbf{(G-1) を満たす有限指数の }\psi\textbf{-安定窓は存在しない。}\ }$$

**証明.** $K:=N\cap H$ と置く。$\psi$ は全射なので、$\ker\psi$ を含む $H$ の部分群と $G_0$ の部分群が指数を保って対応し、$\psi^{-1}(\psi(K))=K\cdot\ker\psi\supseteq K$ より
$$[G_0:\psi(K)]=[H:K\ker\psi]\ \le\ [H:K].$$
第二同型定理より $[H:K]=[H:N\cap H]=[NH:N]=[G_0:N]/[G_0:NH]$。一方 (G-2) は $\psi(K)\subseteq N$ を与えるので $[G_0:N]\le[G_0:\psi(K)]$。**$[G_0:N]$ が有限**だから両者を結合でき
$$[G_0:N]\ \le\ \frac{[G_0:N]}{[G_0:NH]}\ \Longrightarrow\ [G_0:NH]\le1 .\qquad\blacksquare$$

> ⚠ **「$N$ が有限指数」は load-bearing**(falsifier 指摘)。$N=1$ は (G-1)∧(G-2) を**同時に**満たす反例であり、証明は $[G_0:N]=\infty$ で崩れる。定理文から有限指数を落としてはならない。
> **退化枝の定義**: $NH=G_0$ $\iff$ $H$ の $G_0/N$ における像が全体 $\iff$ 「どの $H$-剰余類にいるか」という第 1 階の情報が窓に一切写らない $\iff$ **判定に内容がない**。
> **(G-2) 単独は空虚でない**(falsifier witness・非可換商 $S_3$ でも成立): $G_0=F_2=\langle a,b\rangle$、$H=\ker(F_2\to\mathbb Z/2;\,a\mapsto1,b\mapsto0)$、$\psi(a^2)=1,\ \psi(b)=a,\ \psi(aba^{-1})=b$(全射)、$N=\ker(F_2\to\mathbb Z/2;\,a,b\mapsto1)$。$N\ne H$ ゆえ $NH=F_2$(退化枝)で (G-2) は成立する。⟹ **系は (G-1) 付きに限定して述べること。**

### 1.2 系 DYN-NOGO(Belyi の場合)

$\varphi$ を Belyi-extending、$d=\deg\varphi>1$、$H_\varphi$ 指数 $d$、$\psi_\varphi$ 全射 ⟹ 補題 VE-NOGO がそのまま適用され、**G-1 と G-2 は同時に成立しない**。
**実測との照合**: $z^2$・$M$ 窓・$\mathrm{ord}(\bar x)=18$。$x^{18}\in M_{F_2}\cap H$、$\psi_{z^2}(x^{18})=\psi((x^2)^9)=x^{9}$、$\bar x^{9}\ne1$ ⟹ FAIL。**補題の具体的な現れ**であり $M$ の非 verbal 性のせいではない。
**素数版**: $z^n$ では G-1 が $n\mid\mathrm{ord}(\bar x)$、G-2 が $\gcd(\mathrm{ord}(\bar x),n)=1$ を強制 ⟹ $n=1$。

### 1.3 ★射程 — 「一窓は死・塔は生」(falsifier 所見 3・**設計に有利**)

**証明は Belyi 性も $F_2$ の自由性も次数 $d$ も使っていない。**使うのは「$H\lneq G_0$・$\psi:H\twoheadrightarrow G_0$・$N$ 有限指数正規」だけ。⟹ **障害は力学固有ではなく、仮想自己準同型と固定有限窓の一般的な非両立**である。

さらに決定的に重要なこと:
> **補題 VE-NOGO は「窓写像 $N\mapsto\psi^{-1}(N)$ の不動点が無い」と言っているだけで、その軌道については何も言わない。**
> $$\underbrace{\psi(N\cap H)\subseteq N}_{\text{不動点 = 死}}\qquad\text{対}\qquad \underbrace{\psi(N_{k+1}\cap H)\subseteq N_k\ \ (N_k\supsetneq N_{k+1})}_{\text{軌道 = 生}}$$
> **後者は標的が粗いので矛盾を生まない。**IMG 塔 $\{N_k\}$ はまさにこの軌道であり、射影極限では $\hat\psi:\hat H_\varphi\to\hat F_2$ が問題なく存在する。⟹ **本補題は各有限段の主張のみで、compatible system の非存在は一切言わない。二窓/塔設計(§3)は補題と完全整合。**

**格**: **paper-proof(falsifier 独立検証 PASS)**。ただし §3–§4 は依然 `candidate`。

---

## §2 撤回 2 件(v1 §3 の設計は無効)

| # | 撤回する記述 | 所在 | 理由 |
|---|---|---|---|
| **R-1** | **ゲート G-1 と G-2 の組**(一窓での力学両立テスト) | v1 §3.1 | **定理 DYN-NOGO により両立不能**。設計そのものが誤り。 |
| **R-2** | 「**verbal 窓では G-2 自動**」および v1 §3.2 の**棲み分け表**($z^2\to$972 / $z^3\to$83 / $z^7\to$NW(7)) | v1 §3.1–3.2 | **誤り**。$\psi(\mathcal V(H))\subseteq\mathcal V(F_2)$(真)と $\psi(\mathcal V(F_2)\cap H)\subseteq\mathcal V(F_2)$(要件)を取り違えた。**NW(7) でも破れる**: $x^{7}\in\mathcal V(F_2)=\gamma_5F_2^{7}$、$\psi_{z^7}(x^{7})=x\notin\mathcal V(F_2)$。**表は全面無効**。 |

**維持されるもの**: v1 §1(Wood 射程判定)・§2(定義 D・slack 3 源・L1–L5・$G_\mathbb{Q}\subseteq G_{\rm dyn}$ の証明・$\widehat{GT}$ との関係)は**無傷**。$\psi_\varphi$ の profinite な定義は最初から窓を経由していないため、定理 DYN-NOGO の影響を受けない。

---

## §3 二窓テスト — 実装仕様 v2

### 3.0 原理

$\psi_\varphi$ は**細分側から粗い側へ**降りる。よって判定も二窓で行う。$\psi_\varphi$ は同型
$$\bar\psi:\ H_\varphi/\psi_\varphi^{-1}(N)\ \xrightarrow{\ \sim\ }\ F_2/N$$
を誘導する(全射の完全逆像ゆえ)。

> **定義(二窓判定)**: $N''\subseteq N$ を $\psi_\varphi(N''\cap H_\varphi)\subseteq N$ なる細分窓とする。$g\in GT(N)$ が $\mathrm{DYN}_\varphi(N)$ に属するとは、
> **$\exists$ lift $\tilde g\in GT(N'')$ of $g$** で、$\phi_{\tilde g}$ が $H_\varphi/N''$ を保ち、$\bar\psi$ の下で $\phi_g$ を(内部自己同型を除いて)誘導すること。

**量化が「∃ lift」で正しい理由**: $g=\mathrm{Ih}_N(\sigma)$ なら $\tilde g=\mathrm{Ih}_{N''}(\sigma)$ が証人 ⟹
$$\boxed{\ \mathrm{Im}(\mathrm{Ih}_N)\ \subseteq\ \mathrm{DYN}_\varphi(N)\ }$$
が保たれる ⟹ **算術像の計算可能な上界**(v1 §3.2 の狙いはそのまま生きる)。**片側証明書**: 通らなければ非算術。

### 3.1 IMG 塔窓(二窓性が構成から無料)

$R$ を $H_\varphi$ の $F_2$ における右剰余類代表系($|R|=d$)とし
$$N_1:=\mathrm{Core}_{F_2}(H_\varphi),\qquad N_{k+1}:=\bigl\{g\in N_1\ :\ \psi_\varphi(r^{-1}gr)\in N_k\ \ (\forall r\in R)\bigr\}.$$
これは $F_2\to\mathrm{IMG}_k(\varphi)\le\mathrm{Aut}(T_k)$($d$ 進木の深さ $k$)の核であり、**$r=1$ を取れば $\psi_\varphi(N_{k+1}\cap H_\varphi)\subseteq N_k$ が構成から成立** ✓。DYN-NOGO と矛盾しない(標的が**粗い**窓だから)。

> ⚠ **$B_3$-正規化(必須)**: $N_k$ は $F_2$-正規だが $B_3$-正規とは限らない($S_3$ が $x,y,z$ を置換するため)。$\mathcal B$ は $S_3=\mathrm{Aut}(\mathbb P^1,\{0,1,\infty\})$ の両側合成で閉じている(Wood §3.2 Remark)ので、**$\varphi$ の $S_3$-軌道全体で同じ構成を行い交わりを取る**と $NFI_{PB_3}(B_3)$ に入る。指数は各段で最大 $6$ 倍(実際は軌道の重複で小さくなる)。

### 3.2 較正段 — $z^2$(陽性対照)

$\psi_{z^2}$: $x^2\mapsto x$、$y\mapsto y$、$xyx^{-1}\mapsto1$。$S_3$-対称化した塔は**verbal**:
$$\mathcal W_k:=\gamma_2(F_2)\,F_2^{2^{k}},\qquad |F_2/\mathcal W_k|=4^{k}\quad(k=1,2,3:\ 4,\ 16,\ 64).$$
降下 $\psi(\mathcal W_{k+1}\cap H)\subseteq\mathcal W_k$ は $\psi(x^{2^{k+1}})=x^{2^{k}}$、$\psi([x^2,y])=[x,y]$ 等で成立(**要機械確認**)。
**予言(陽性対照)**: $\mathrm{IMG}(z^2)$ は加算機 $=\mathbb Z$ で**初等的**ゆえ切断力ゼロ ⟹ **$\mathrm{DYN}_{z^2}(\mathcal W_k)=GT(\mathcal W_k)$(全 shadow 通過)**。通らなければ**実装バグ**。コストは無視できる。

### 3.3 本測定段 — $T$(または $O$)の IMG 塔

| 段 | 窓 | 位数(上界) | 判定 |
|---|---|---|---|
| $T$ 第 1 階 | $N_1=\ker(F_2\twoheadrightarrow A_4)$ の $S_3$-対称化 | $\le 12^3=\mathbf{1728}$ | **即実行可** |
| $O$ 第 1 階 | $\ker(F_2\twoheadrightarrow S_4)$ の $S_3$-対称化 | $\le 24^3=\mathbf{13{,}824}$ | 実行可 |
| $T$ 第 2 階 | $N_2$ | $\le 12^{13}\approx1.1\times10^{14}$(**粗い上界**) | **要先行測定**(GAP の低指数/商計算・分単位)。**推測で埋めない** |

**手順(第 1 階)**: ①$F_2\twoheadrightarrow A_4$($x\mapsto a$ 位数 3・$y\mapsto b$ 位数 3・$(ab)^{-1}$ 位数 2)の $S_3$-軌道 3 本の共通核 $N_1^{\rm sym}$ を構成 ②$GT(N_1^{\rm sym})$ を既存の hexagon+charming+onto 計器で列挙 ③$N_2^{\rm sym}$ を §3.1 の再帰で構成 ④各 $g$ について fibre $R^{-1}(g)$ を走査し ∃lift 判定 ⑤$|\mathrm{DYN}_T|$ を出力。
**対照**: 陽性 = 単位 shadow と複素共役($u=-1$)は必ず通る($G_\mathbb{Q}$ の元)。破壊 = $\psi$ を別の $\varphi$ のものに差し替えて判定が変わること。

### 3.4 既存アトラスへの適用 — **コスト見積りのみ**(実行判断は司令塔)

$[F_2:N'']\ge d\cdot[F_2:N_{F_2}]$ より($|F_2/M_{F_2}|=1{,}469{,}664$):

| アトラス | $\varphi$ | $[F_2:N'']$ の下界 | 所見 |
|---|---|---|---|
| 972($M$) | $z^2$ | $\ge2.94\times10^{6}$ | shadow 列挙が重いが不可能ではない |
| 972($M$) | $T$($d=12$) | $\ge1.76\times10^{7}$ | 現行計器では困難 |
| 83 | $z^3$ | $\ge3\times192\cdot(\text{c-part})$ | **G-1 は満たすが**、二窓形では $N''$ の構成が必要 — 未見積り |
| NW(7) | $z^7$ | $\approx7^{16}\approx3\times10^{13}$ | **不能** |

⟹ **既存アトラスは全て「先に IMG 塔で装置を作ってから」**が合理的。

---

## §4 $T$ と $O$ の明示データ(式から自前導出)

$$T(t)=\frac{t^{3}(t^{3}+8)^{3}}{(t^{6}-20t^{3}-8)^{2}},\qquad O(t)=\frac{108\,t^{4}(t^{4}-1)^{4}}{(t^{8}+14t^{4}+1)^{3}}$$

### 4.1 $T$ — 分岐データ(**自前検算**)

$\deg T=12$。$T(\infty)=1$(分子・分母とも monic 次数 12)。**鍵の恒等式(本ノートで展開)**:
$$t^{3}(t^{3}+8)^{3}-(t^{6}-20t^{3}-8)^{2}\;=\;64\,(t^{3}-1)^{3}$$
(左辺 $=t^{12}+24t^9+192t^6+512t^3$、右辺の 2 乗 $=t^{12}-40t^9+384t^6+320t^3+64$、差 $=64t^9-192t^6+192t^3-64$ ✓)。

| 上 | 点 | 指数 | 個数 |
|---|---|---|---|
| $0$ | $t=0$、$t^3=-8$ の 3 根 | **3** | 4 |
| $1$ | $t^3=1$ の 3 根、$t=\infty$ | **3** | 4 |
| $\infty$ | $t^6-20t^3-8=0$ の 6 根 | **2** | 6 |

⟹ **signature $(3,3,2)$・$\deg=12=|A_4|$ ⟹ Galois 被覆で $F_2/H_T\cong A_4$**(司令塔の見立てを確認)。$H_T=\ker(F_2\twoheadrightarrow A_4)$ は**正規**・階数 13。
$T(\{0,1,\infty\})=\{0,1,1\}\subseteq\{0,1,\infty\}$ ✓ **Belyi-extending**。

**$\psi_T$ の生成元像**(慣性生成元 $\gamma_P$ について $T_*(\gamma_P)\sim(\text{loop at }T(P))^{e_P}$、$\iota_*(\gamma_P)=$ $P\in\{0,1,\infty\}$ のときのみ非自明):
$$\boxed{\ \psi_T:\ x^{3}\text{-共役}\mapsto x,\quad y^{3}\text{-共役}\mapsto y,\quad \text{別の }y^{3}\text{-共役}\mapsto z,\quad \text{他の 11 個の慣性生成元}\mapsto1\ }$$
(3 本目は $P=\infty$ 由来: $T(\infty)=1$ で $e=3$、$\iota_*(\gamma_\infty)=z$。)

### 4.2 $O$ — 分岐データ(**自前検算**)

$\deg O=24$(分母次数 24 > 分子次数 20)。$O(\infty)=0$(位数 $24-20=4$)。

| 上 | 点 | 指数 | 個数 |
|---|---|---|---|
| $0$ | $t=0$、$t^4=1$ の 4 根、$t=\infty$ | **4** | 6 |
| $1$ | — | **2** | 12 |
| $\infty$ | $t^8+14t^4+1=0$ の 8 根 | **3** | 8 |

⟹ **signature $(4,2,3)$・$\deg=24=|S_4|$ ⟹ Galois で $F_2/H_O\cong S_4$**。$O(\{0,1,\infty\})=\{0\}$ ✓ **Belyi-extending**。
$$\boxed{\ \psi_O:\ \text{3 本の }x^{4}\text{-共役}\ \mapsto\ x,\ y,\ z\ \ (\text{それぞれ }P=0,1,\infty\ \text{由来}),\quad \text{他の 23 個}\mapsto1\ }$$

### 4.3 IMG の非初等性(一行・**candidate**)

Thurston 軌道体で判定する。$T$: $0$ と $1$ は**超吸引的固定点**(臨界固定点・局所次数 3)ゆえ $\nu(0)=\nu(1)=\infty$、$\nu(\infty)\ge2$ ⟹ signature $(\infty,\infty,\ge2)$。$O$: $0$ が超吸引的固定点で $1,\infty\to0$ ⟹ $(\infty,\ge2,\ge3)$。**いずれも Euclid 型リスト $\{(2,2,2,2),(2,4,4),(2,3,6),(3,3,3),(2,2,\infty),(\infty,\infty)\}$ に無い ⟹ 双曲軌道体 ⟹ 非例外的 ⟹ IMG は仮想可換でない。**
**対比**: $z^n$ は $(\infty,\infty)$、$4z(1-z)$ は $z^2-2$(Chebyshev)と共役で $(2,2,\infty)$ — **どちらも Euclid 型 = 例外的 = IMG 初等的(加算機 $\mathbb Z$ / 無限二面体)**。⟹ **水準 1 の 2 写像は力学的に退化しており切断力が原理的に低い。$T/O$ が本来の弾。**

---

## §5 事前登録 P-DYN-1′(旧 P-DYN-1 の差し替え)

> **P-DYN-1(旧)**: 装置設計の誤り(定理 DYN-NOGO)により**未測定**。問い自体は有効。**取り下げず「未測定・場所を変えて再登録」と記帳。**
> ### 予言 P-DYN-1′
> **(a) 較正**: $\mathrm{DYN}_{z^2}(\mathcal W_k)=GT(\mathcal W_k)$(全通過)。**外れたら実装バグ**。
> **(b) 本測定**: $T$ の IMG 塔第 1 階窓 $N_1^{\rm sym}$($\le1728$)で $\mathrm{DYN}_T(N_1^{\rm sym})\subsetneq GT(N_1^{\rm sym})$、すなわち **$G_{\rm dyn}$ の切断力が非零**。
> **(c) 定量**: $\mathrm{Im}(\mathrm{Ih})\subseteq\mathrm{DYN}_T$ は定理(v1 §2.4)。**$\mathrm{DYN}_T$ が $\mathrm{Im}(\mathrm{Ih})$ に等しいか真に大きいか**が最初の実データ。**真に大きければ「力学上界 ⊋ 算術像」の初の定量**、等しければ **$G_{\rm dyn}$ が算術像を完全に切り出す**という強い結果。
> **外れ方の分岐**: (b) が等号(切断力ゼロ)⟹ $T$ でも足りず、写像の選定基準を再設計。(a) が外れる ⟹ 実装。

---

## §6 未決・債務

1. **定理 DYN-NOGO の独立検証**(falsifier 並行中)— これが PASS するまで v2 全体は candidate。
2. §4 の分岐データは**式からの自前導出・機械検算なし**。とくに $O$ の「上 1 に 12 点・指数 2」は次数勘定からの帰結で、**$O(t)-1$ の因数分解は未実行**。要 cross-check。
3. §3.2 の $\psi_{z^2}(\mathcal W_{k+1}\cap H)\subseteq\mathcal W_k$ は**要機械確認**。
4. $T$ 第 2 階の窓位数は**未測定**($12^{13}$ は粗い上界)。**推測で埋めない。**
5. **UNVERIFIED 債務(v1 §4 から継承・novelty 欄へ)**: **[12]** Nakamura, *Some classical views on the parameters of the GT group*(Progress in Galois Theory)と **[14]** Nakamura–Tsunogai, Forum Math. **15** (2003) 877–892 は**未取得・未確認**。**[NS] Invent. 141 は LNS 2026 §1/§8 の再説明により「lego 条件 = 別種」と判定済**(空席は白)。⟹ **novelty は [12] 確認まで主張しない。**

---

## §7 falsifier 検証記録(2026-08-26)

**判定 = PASS**(独立別証明 = $\pi\circ\psi$ の経由分解 / 数値 5291 構成で反例 0)。反映した修文 5 点:

| # | 指摘 | 反映箇所 |
|---|---|---|
| **F-1** | 「全射ゆえ割る」に kernel 経由の一行が要る | §1.1 の証明を $\psi^{-1}(\psi(K))=K\ker\psi$ 経由へ書き直し(**$\le$ で十分**・divisibility は不要) |
| **F-2** | **「$N$ が有限指数」が load-bearing**($N=1$ が (G-1)∧(G-2) の反例) | §1.1 に ⚠ 注記。定理文から有限指数を落とさない旨を明記 |
| **F-3** | 系は **(G-1) 付き**に限定せよ。(G-2) 単独の $\psi$-安定 $N$ は**実在** | §1.1 の系を (G-1) 版に限定。**witness を逐語収録**($H=a$-parity・$\psi(a^2)=1,\psi(b)=a,\psi(aba^{-1})=b$・$N=$ 対角 $\mathbb Z/2$ の核)。**退化枝 $NH=G_0$ の定義**も明示 |
| **F-4** | no-go は**各有限段のみ** — 塔の射影極限・compatible system には無言 | §1.3 を新設。「**不動点 = 死 / 軌道 = 生**」の境界線を式で明示。IMG 塔・二窓設計(§3)が補題と**完全整合**であることを記載 |
| **F-5** | 証明は Belyi 性・自由性・次数 $d$ を使わない一般事実 ⟹ **一般補題として定式化**せよ | §1.1 を **補題 VE-NOGO(一般形)**に昇格($G_0$ 任意群・$H\lneq G_0$・$\psi:H\twoheadrightarrow G_0$)。Belyi の場合は §1.2 の**系 DYN-NOGO** に降格。位置づけを「力学固有の障害ではなく、**仮想自己準同型と固定有限窓の一般的な非両立**」へ訂正 |

**格の更新**: §1(補題 VE-NOGO・系 DYN-NOGO・射程)= **paper-proof(falsifier 独立検証 PASS)**。§2 の撤回 2 件は確定。**§3(二窓仕様)・§4($T/O$ の分岐データ)・§5(prereg)は依然 `candidate`。**

**引用可能性の所見(F-5 の副産物)**: 補題 VE-NOGO は自己相似群論の一般命題として単独で意味を持つ(「仮想自己準同型は、その定義域に含まれる有限指数の特性商へは決して降りない」)。**$G_{\rm dyn}$ の外でも使える形**になったので、将来の論文化では独立した補題として置ける。

**残る債務(§6 と重複・再掲)**: ① §4 の $O(t)-1$ の因数分解は未実行(次数勘定からの帰結)② §3.2 の $\psi_{z^2}(\mathcal W_{k+1}\cap H)\subseteq\mathcal W_k$ は要機械確認 ③ $T$ 第 2 階の窓位数は未測定($12^{13}$ は粗い上界・**推測で埋めない**)④ [12]/[14] は UNVERIFIED ⟹ **novelty は主張しない**。

---

## §8 ★v2.1 の追加 — 鋭形 VE-NOGO⁺・系 VE-COF・実務系 VE-TEST

**格**: `paper-proof(自前・未監査)`。§1 の補題を**同じ仮定のまま**強化したもので、§1–§7 の内容は一切変更しない。

### 8.0 委嘱修文 3 点の所在(既反映の確認)

| 委嘱 | 反映済みの所在 | 内容 |
|---|---|---|
| ① kernel 経由の一行 | **§1.1 証明**(第 1 行) | $\psi^{-1}(\psi(K))=K\ker\psi$ から $[G_0:\psi(K)]=[H:K\ker\psi]\le[H:K]$($\le$ で足り、divisibility は不要) |
| ② 有限指数が load-bearing | **§1.1 ⚠ 注記** | $N=1$ が (G-1)∧(G-2) の反例。定理文から落とさない旨を明記 |
| ③ 系を (G-1) 限定 + (G-2) 単独 witness | **§1.1 系・⚠ 第 3 段** | 系は (G-1) 版に限定。falsifier witness($H=a$-parity 核・$\psi(a^2)=1,\psi(b)=a,\psi(aba^{-1})=b$・$N=$ 対角核)を逐語収録。退化枝 $NH=G_0$ の定義も明示 |
| 射程(各有限段のみ・塔には無言) | **§1.3** | 「不動点 = 死 / 軌道 = 生」の境界式。IMG 塔・二窓設計との完全整合 |
| 一般補題化(Belyi 性不使用) | **§1.1 見出し + §7 F-5** | $G_0$ 任意群・$H\lneq G_0$・$\psi:H\twoheadrightarrow G_0$・$N$ 有限指数正規のみ |

⟹ **v2.1 の実質差分は以下 §8.1–§8.5。**

### 8.1 鋭形 — 結論は 3 本(実は 4 本)取れる

§1.1 の証明を読み直すと、不等式の鎖が**両端で一致している** ⟹ 途中の $\le$ はすべて等号でなければならない。これを取り出す。

> ### 補題 VE-NOGO⁺(鋭形)
> $G_0$ 群、$H\le G_0$、$\psi:H\twoheadrightarrow G_0$ 全射準同型、$N\trianglelefteq G_0$ **有限指数**。
> $$\text{(G-2)}\qquad\psi(N\cap H)\subseteq N$$
> を仮定すると、次の**4 つがすべて**成り立つ:
> $$\textbf{(a)}\ NH=G_0,\qquad \textbf{(b)}\ \psi(N\cap H)=N,\qquad \textbf{(c)}\ \ker\psi\subseteq N,\qquad \textbf{(d)}\ N\cap H=\psi^{-1}(N).$$
> (逆に (d) $\Rightarrow$ (G-2) は自明。ゆえに有限指数の下で **(G-2) $\iff$ 「$N$ が $\psi$ について厳密飽和」**。)
> **系(G-1 版・§1.1 と同じ)**: さらに $N\subseteq H$ なら $G_0=NH=H$ となり $H\lneq G_0$ に矛盾。

**証明.** $K:=N\cap H$。$[H:K]=[NH:N]=[G_0:N]/[G_0:NH]<\infty$(第二同型定理・$N$ 有限指数)。$\psi$ 全射ゆえ $\psi^{-1}(\psi(K))=K\ker\psi$ で
$$[G_0:\psi(K)]=[H:K\ker\psi]\le[H:K]=\frac{[G_0:N]}{[G_0:NH]} .$$
(G-2) の $\psi(K)\subseteq N$ から $[G_0:N]\le[G_0:\psi(K)]$。両者を結ぶと
$$[G_0:N]\ \le\ [G_0:\psi(K)]\ =\ [H:K\ker\psi]\ \le\ [H:K]\ =\ \frac{[G_0:N]}{[G_0:NH]}\ \le\ [G_0:N]$$
となり、$[G_0:N]$ が有限だから**鎖全体が等号**。
- 最右の等号 ⟹ $[G_0:NH]=1$、すなわち **(a)**。
- 最左の等号 $[G_0:\psi(K)]=[G_0:N]<\infty$ と $\psi(K)\subseteq N$ ⟹ **(b)**。
- 中央の等号 $[H:K\ker\psi]=[H:K]$ と $K\subseteq K\ker\psi\subseteq H$、$[H:K]<\infty$ ⟹ $K\ker\psi=K$ ⟹ $\ker\psi\subseteq K=N\cap H\subseteq N$、すなわち **(c)**。
- (b)+(c) ⟹ $h\in\psi^{-1}(N)$ なら $\psi(h)=\psi(k)$ なる $k\in K$ が取れ $hk^{-1}\in\ker\psi\subseteq K$ ⟹ $h\in K$。逆包含は (G-2)。よって **(d)**。$\blacksquare$

> ⚠ **有限指数の load-bearing 性の再確認(F-2 との整合)**: $N=1$ は (G-2) を満たすが、$\ker\psi\ne1$ のとき **(c) が破れる**。⟹ 鋭形でも有限指数は落とせない。**これは F-2 の独立な確認になっている**(別の結論が同じ反例で壊れる)。

### 8.2 ★系 VE-COF — 「(G-2) 窓は決して cofinal にならない」

結論 (c) は $N$ ごとの主張ではなく**族全体への制約**である。ここが v2 から前進した点。

> ### 系 VE-COF
> $G_0$ を剰余有限群、$H\le G_0$、$\psi:H\twoheadrightarrow G_0$ とし、
> $$\mathcal S:=\{\,N\trianglelefteq G_0\ :\ [G_0:N]<\infty,\ \psi(N\cap H)\subseteq N\,\}$$
> と置く。もし $\ker\psi\neq1$ ならば
> $$\bigcap_{N\in\mathcal S}N\ \supseteq\ \ker\psi\ \neq\ 1$$
> であり、ゆえに **$\mathcal S$ は $\mathrm{NFI}(G_0)$ の中で cofinal になりえない**(cofinal なら剰余有限性より交わりが $1$)。
> とくに **$\mathcal S$ 上の逆極限は $\widehat{G_0}$ を与えず、点を分離しない**。

**証明.** 各 $N\in\mathcal S$ に (c) を適用。$\blacksquare$

**意義(§1.3 の射程の強化)**: v2 §1.3 は「(G-1) 付きの固定窓は死ぬが、軌道(移動標的)なら生きる」と述べた。VE-COF はさらに強く、**(G-1) を課さない (G-2) 単独の窓(退化枝を含む)を全部集めても塔として使い物にならない**と言う。⟹ **移動標的 $\psi(N_{k+1}\cap H)\subseteq N_k$ は「便利な代案」ではなく唯一の道**である。§3 の二窓設計はこの意味で**必然**。

### 8.3 実務系 VE-TEST(安価な必要条件・実装の自己診断用)

> 窓 $N$(有限指数正規)が (G-2) を満たすためには **$\ker\psi\subseteq N$ が必要**。
> ⟹ **$\ker\psi$ の元を 1 個でも $N$ の外に見つけたら、その窓で (G-2) は成立しない**(列挙不要・$O(1)$)。

$\varphi=T$ の場合、$\ker\psi_T$ は「$\iota$ で埋まる 11 個の慣性生成元」を含む(§4.1)ので、この検査は具体語 1 本の所属判定で済む。**一窓設計を復活させようとする実装は、この 1 行で即座に落ちる。**

### 8.4 Belyi の場合: $\ker\psi_\varphi\ne1$ は自動($d>1$)

> **命題**: $\varphi$ を Belyi-extending、$d=\deg\varphi>1$ とすると $\ker\psi_\varphi\neq1$。したがって系 VE-COF が**無条件に適用される**。

**証明.** $H_\varphi\le F_2$ は指数 $d$ ゆえ Nielsen–Schreier より階数 $d(2-1)+1=d+1$ の自由群。$\psi_\varphi:H_\varphi\twoheadrightarrow F_2$ が単射なら $F_{d+1}\cong F_2$ となり自由群の階数不変性に反する($d+1>2$)。$\blacksquare$

($T$ では $d=12$・階数 13、$O$ では $d=24$・階数 25。§4 の「14 個の慣性生成元・積 1 の関係で階数 13」と整合。)

### 8.5 まとめ — v2.1 での位置づけの更新

| 主張 | v2 | v2.1 |
|---|---|---|
| 固定窓 + (G-1) | 死(補題 VE-NOGO) | 同(変更なし) |
| 固定窓 + (G-2) 単独 | 退化枝 $NH=G_0$ に落ちる(内容なし) | **加えて $\ker\psi\subseteq N$ を強制** |
| (G-2) 窓の**族** | 言及なし | **★ cofinal になりえない(VE-COF)** |
| 移動標的の塔 | 補題と整合(生) | **必然(唯一の道)** |
| 実装の自己診断 | なし | **VE-TEST(1 元判定)** |

**残債務(v2 §6 から不変)**: ① $O(t)-1$ の因数分解未実行 ② $\psi_{z^2}$ の降下の機械確認 ③ $T$ 第 2 階の窓位数未測定 ④ [12]/[14] UNVERIFIED ⟹ novelty 非主張。
**v2.1 で追加された債務**: ⑤ 補題 VE-NOGO⁺・系 VE-COF は**未監査**(§1 の VE-NOGO は falsifier PASS 済だが、鋭形の 3 本の等号と VE-COF は本稿が初出)。
