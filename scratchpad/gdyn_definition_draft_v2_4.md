# $G_{\rm dyn}$ 定義起草 **v2.4** — DYN-NOGO・二窓テスト・$T/O$・**[DYN-CEIL] 天井の文献確定**

> ### ★ v2.4 差分(文献ゲート通過の降ろし・裁定 1706・**§9 を新設**・§5/§8.2 を本文更新)
> **結論**: 私が v2.3 §8.2 で「$\ker(F_2\twoheadrightarrow\mathrm{IMG}(T))\ne1$ は**推測であって証明ではない**(格 = `heuristic`)」と書いた命題は、**文献で無条件に確定した**。
> **鎖(現物で逐語照合済・§9.1)**: [survey Thm 3.3 + 直後の "In particular" 節] PCF 有理写像の IMG は **contracting** → [survey Thm 3.6 = 0802.2554 Thm 4.2] contracting 群は**自由部分群を持たない** ⟹ $\ker=1$ なら $F_2\hookrightarrow\mathrm{IMG}(T)$ で矛盾 ⟹ **$\ker\ne1$**。
> **⟹ $T$-塔には分解能の天井が存在する(格 = `literature-backed`・原典 [Nek05 Thm 5.5.3] は未見)。**
> **設計上の含意**: **「一塔は有界・族が本体」** — DYN-NOGO の「一窓は死・塔は生」の続き。$G_{\rm dyn}$ が**全 Belyi-extending 族で量化している**ことは飾りではなく**本質**である(§9.6)。
> **⚠ 走行中の $\Lambda$ 天井テストとは別物**: $\ker\ne1$ は $\Lambda$ の挙動を含意しない(核が $[F_2,F_2]$ 内なら $\Lambda$ は細り続けうる)⟹ $\Lambda$ 停留が出れば**可換化水準の独立な構成的証明書**として別記帳(§9.5)。
> **機械**: ③ $T$(および $O$)が多項式共役でないことを確認 ⟹ **経路 B(BKN 従順性・多項式限定)は元々不可**であり、v2.3 の不主張は正当だった(§9.3)。
> **本便は `gdyn_t_measurement_spec_v1_3.md` を触らない**(implementer の $\Lambda$/G18/C3-B 走行と衝突させないため)。
> **v2.3(sha16 `3768570dde7e08b1`)・v2.2(`ea4bd521936c3e5c`)・v2.1(`058821265491e435`)・v2(`5886e2483137646b`)・v1(`2dd0d41aeaef6494`)は不変のまま並置。**

> ### ★ 本文書の規約(2 本・全文書共通)
> **(R-1) 訂正は同ターンで本文に打つ**(訂正表だけでは足りない・被訂正文は除去か ⚠ マーカ)。**(R-2) `gate:` は述語を実際に評価した場合のみ・文書内の文字列検査は `doc-keyword:`。**

> ### v2.3 の変更(falsifier 第 2 便・**すべて本文に直接打った**)
> | # | 箇所 | 内容 |
> |---|---|---|
> | **Z-1** | **§5(prereg)** | §8.2 の結論を**伝播**: (b) の等号(切断力ゼロ)の外れ方は**二義**(力学が弱い/塔が届いていない・実験で分離不能)。**cert 実装者が読むのは §5** なのでここに書かねば意味がない |
> | **Z-2** | **§3.2** | $z^2$ 較正 (a) は **「何にでも当たる試験」= 陰性対照ではない**($\bigcap\mathcal W_k\supseteq[F_2,F_2]\ne1$ で塔非分離でも自明通過)⟹ 明記 |
> | **Z-3** | **§3.3** | mutant $\psi$ 破壊対照に**期待値を事前登録**(どの差し替えで判定がどう変わるはずか) |
> | **Z-4** | **全文** | 「falsifier 独立**検証**」→「独立**照合**」へ全置換(**「検証」は Lean 予約語**・2026-07-18 研究者指示)。機械置換 4+2+1 箇所・残 0 を機械確認 |
> | **Z-5** | **§6-2 / §7 / §8.5 の債務②** | **$O(t)-1$ の因数分解は不要化 ⟹ 債務閉鎖**(Riemann–Hurwitz + Galois 性・**falsifier 帰属**・私の再検算つき) |
> **v2.2(sha16 `ea4bd521936c3e5c`)・v2.1(`058821265491e435`)・v2(`5886e2483137646b`)・v1(`2dd0d41aeaef6494`)は不変のまま並置。**

> ### v2.2 差分(falsifier 要修正 D のみ・**§8.2 と §8.5 の 2 箇所**)
> **v2.1(sha16 `058821265491e435`)からの変更は下記 2 箇所だけ。他は 1 バイトも変えていない。**
> **(D)** §8.2 の「移動標的 = 唯一の道・§3 の二窓設計は必然」を**撤回**し、**必要条件の主張に限定**した。VE-COF が示すのは**固定窓族の死**のみで、移動標的が機能することは何も言っていない。較正例 $z^2$ で $\bigcap_k\mathcal W_k\supseteq[F_2,F_2]\ne1$(塔が点を分離しない実例)。一般に $\bigcap_kN_k=\ker(F_2\twoheadrightarrow\mathrm{IMG}(\varphi))$ で、$T/O$ についてこれが $1$ かは **UNKNOWN**。**P-DYN-1′(b) の切断力上限に直結**する旨も明記(切断力ゼロが「力学が弱い」のか「塔が届いていない」のかは実験では分離できない)。
> §8.5 の一覧表の該当行も同時に訂正。

`DIR: 正側(算術像の上界)/ FRAME: Out(F̂₂) を力学で切る`

> **v2.1 について(先に読むこと)**: 委嘱の修文 3 点(①kernel 経由の一行 ②有限指数が load-bearing ③系を (G-1) 限定 + (G-2) 単独 witness 併記)、および射程明記・一般補題化は、**すべて v2 の §1・§7 に既に反映済**である(v2 sha16 `5886e2483137646b`)。⟹ **v2.1 の実質差分は §8 のみ** — v2 の証明を精査した結果、**同じ仮定から結論が 3 本取れる(等号版)**ことが分かったので、補題を鋭形へ強化し、そこから**新しい系 VE-COF(「(G-2) 窓は決して cofinal にならない」)**と実務用の必要条件 VE-TEST を導いた。§1–§7 は 1 バイトも改変していない。

**状態札**: `§1 = ★補題 VE-NOGO + 系 DYN-NOGO(paper-proof・falsifier 独立照合 PASS)/ §2 = 撤回 2 件 / §3 = 実装仕様 v2(candidate)/ §4 = T/O の分岐データ(**v2.3 で機械裏づけ済** — sympy の恒等式 + Riemann–Hurwitz `gate:`・§6-2 補題 O-RH)/ §5 = prereg 文(**v2.3 で Z-1/Z-3 を追加**)/ §7 = falsifier 照合記録 / §8 = ★鋭形 VE-NOGO⁺ + 系 VE-COF + VE-TEST(v2.1 新設・paper-proof・未監査)/ **§9 = ★系 DYN-CEIL(v2.4 新設・literature-backed・原典 [Nek05 5.5.3] 未見)**/ novelty は [12][14] の UNVERIFIED 債務に依存`

- 起草: 影工房 数学者(Opus 5)/ 2026-08-26 / **v1(`gdyn_definition_draft_v1.md`)は 1 バイトも改変せず並置**。v1 の §1(Wood 射程判定)・§2(定義)は**そのまま有効**。差分は本 v2 の §1–§5。
- 契機: implementer の P-DYN-1 初測定(cert `gdyn_p_dyn1_972_v1_20260826.json`)で **G-2 が両写像 FAIL**。根因は窓固有ではなく**私の設計の誤り**と判明。

---

## §1 ★補題 VE-NOGO(一般形)と系 DYN-NOGO

**falsifier 独立照合 = PASS**(別証明 = $\pi\circ\psi$ の経由分解・数値 5291 構成で反例 0)。以下は falsifier の修文 5 点を織り込んだ最終形。

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

**格**: **paper-proof(falsifier 独立照合 PASS)**。ただし §3–§4 は依然 `candidate`。

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

> ### ⚠ Z-2:$z^2$ 較正は**陰性対照ではない**(v2.3 追加・重要)
> $\mathcal W_k=\gamma_2(F_2)F_2^{2^k}\supseteq[F_2,F_2]$ が全 $k$ で成り立つので $\bigcap_k\mathcal W_k\supseteq[F_2,F_2]\ne1$ — **この塔は点を分離しない**(§8.2)。ゆえに **$z^2$ 較正は「塔が届いていなくても自明に全通過する試験」**である。
> ⟹ **(a) が通ることは、判定器が正しく動いている証拠にはならない。**「何にでも当たる試験」であって、**陰性対照(判定器が FALSE を返せることの実証)ではない**。
> **(a) の効用は 1 つだけ**: **FALSE が出たら実装バグ**という片側検出。**PASS には情報量がない。**
> ⟹ 陰性側の保証は **§3.3 の破壊対照(Z-3)にしか無い** — cert では両者を混同しないこと。

### 3.3 本測定段 — $T$(または $O$)の IMG 塔

| 段 | 窓 | 位数(上界) | 判定 |
|---|---|---|---|
| $T$ 第 1 階 | $N_1=\ker(F_2\twoheadrightarrow A_4)$ の $S_3$-対称化 | $\le 12^3=\mathbf{1728}$ | **即実行可** |
| $O$ 第 1 階 | $\ker(F_2\twoheadrightarrow S_4)$ の $S_3$-対称化 | $\le 24^3=\mathbf{13{,}824}$ | 実行可 |
| $T$ 第 2 階 | $N_2$ | $\le 12^{13}\approx1.1\times10^{14}$(**粗い上界**) | **要先行測定**(GAP の低指数/商計算・分単位)。**推測で埋めない** |

**手順(第 1 階)**: ①$F_2\twoheadrightarrow A_4$($x\mapsto a$ 位数 3・$y\mapsto b$ 位数 3・$(ab)^{-1}$ 位数 2)の $S_3$-軌道 3 本の共通核 $N_1^{\rm sym}$ を構成 ②$GT(N_1^{\rm sym})$ を既存の hexagon+charming+onto 計器で列挙 ③$N_2^{\rm sym}$ を §3.1 の再帰で構成 ④各 $g$ について fibre $R^{-1}(g)$ を走査し ∃lift 判定 ⑤$|\mathrm{DYN}_T|$ を出力。
**対照**: 陽性 = 単位 shadow と複素共役($u=-1$)は必ず通る($G_\mathbb{Q}$ の元)。

> ### ★ Z-3:破壊対照の**事前登録**(v2.3 新設 — 期待値を先に固定する)
> **陰性側の保証はここにしか無い**(§3.2 の $z^2$ は陰性対照ではない)。⟹ **走行前に次の期待値を cert に pin し、事後変更しない。**
>
> | mutant | 差し替え内容 | **期待される判定の変化** | 変化しなければ |
> |---|---|---|---|
> | **M-a** | $\psi_T\to\psi_{T_\sigma}$($\sigma$ = 型 $(3,2,3)$ の strand) | $\mathrm{DYN}$ の**元集合が変わる**(位数が同じでも集合として違う)。**位数まで一致したら要精査** | 判定器が $\psi$ を見ていない |
> | **M-b** | ∞-点の代表 $r_0=xyx^{-1}\to r_0'=x$(**§1.4 で不可と証明済の値**) | $\psi_T$ が**準同型として壊れる**(3 特別値が $xyz=1$ と非整合)⟹ **§6 の G2(well-defined 性)で fail-close** | 実装が G2 を素通しした |
> | **M-c** | 3 特別値のうち 1 つを $1$ に潰す | $\psi$ が全射でなくなる ⟹ **G2 で fail-close** | 同上 |
> | **M-d** | 慣性の型テンプレートを strand 1 用のまま別 strand に流用 | **§8.4 の停止原因の再現** ⟹ 位数 2 の慣性の位置がずれて G13 で fail | G13 が効いていない |
> | **M-e** | $\bar\psi$ の合成順を逆($\phi_g\circ\bar\psi\to\bar\psi\circ\phi_g$ を取り違え) | 判定が変わる(W-1 型) | 規約が固定されていない |
>
> ⚠ **M-b/M-c は「判定が変わる」ではなく「ゲートで落ちる」ことが期待値**である — 破壊対照の出口が 2 種類あるので混同しないこと。

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
> ### ★ Z-1:外れ方の分岐(v2.3 で **§8.2 の結論を伝播** — **cert 実装者はここを読む**)
> **(a) が外れる ⟹ 実装バグ。**⚠ ただし **(a) が通っても情報はゼロ**($z^2$ 塔は点を分離しないので「何にでも当たる試験」— §3.2 の Z-2)。陰性側の保証は **§3.3 の破壊対照(M-a〜M-e)にしかない。**
> **(b) が等号(切断力ゼロ)のときの解釈は二義である**:
> 1. **力学が弱い** — $T$ の $\mathrm{IMG}$ が算術像を切るだけの情報を持たない;
> 2. **塔が届いていない** — 分解能が $\ker(F_2\twoheadrightarrow\mathrm{IMG}(T))$ で頭打ちになり、$\mathrm{DYN}_T$ は核の中を見分けられない(§8.2)。
>
> ### ⚠ v2.4 更新(裁定 1706)— **漸近側は確定した。有限水準の分離不能は残る。**
> v2.3 はここで「**$T$ について $\ker=1$ かは UNKNOWN**」「分離するには独立判定が要る — **未着手・UNKNOWN**」と書いていた。**文献ゲート通過により $\ker\ne1$ が確定(§9)** ⟹ **本ブロックで置換**:
> - **(2) は漸近的には真と確定した**($T$-塔には天井が実在する)。⟹ 「$T$ でも足りない ⟹ 写像の選定基準を再設計」は**もはや単なる可能性ではなく、族水準へ移るべき積極的根拠**である(§9.6「一塔は有界・族が本体」)。
> - **しかし有限水準での (1)/(2) の分離は依然として不能**: 天井は**漸近的**な性質で、**どの深さから効き始めるかは未知**。ゆえに「深さ $k$ で切断力ゼロ」を観測しても、それが (1) か (2) かは**この実験だけでは決まらない**。
> - ⟹ **cert には引き続き両方の解釈を書くこと。**追加で「**天井の存在は文献確定・発効深度は未知**」の 1 行を必ず入れる。
> - **可換化水準に限れば構成的な分離が可能**: $\Lambda_{N_k}$ が停留すれば「塔が可換化を細分し切れない」ことの**独立な証明書**になる(§9.5)。⚠ ただし $\ker\ne1$ はこれを**含意しない**(核が $[F_2,F_2]$ 内なら $\Lambda$ は細り続けうる)。

---

## §6 未決・債務

1. **定理 DYN-NOGO の独立照合**(falsifier 並行中)— これが PASS するまで v2 全体は candidate。
2. ~~§4 の分岐データ… $O(t)-1$ の因数分解は未実行。要 cross-check。~~ ⟹ **★ Z-5:債務②は閉鎖(因数分解は不要化)。falsifier 帰属。**

> ### 補題 O-RH($O(t)-1$ の因数分解を要さずに「上 1 は 12 点・全て $e=2$」を出す)
> **着想は falsifier**(Riemann–Hurwitz + Galois 性)。**私が独立に再検算した**(下の `gate:`)。
> $\deg O=24$、被覆は $\mathbb P^1\to\mathbb P^1$(両側 $g=0$)、Galois 群 $S_4$。
> - 上 $0$: $t=0$・$t^4=1$ の 4 根・$t=\infty$ の **6 点、$e=4$** ⟹ $\sum(e-1)=6\cdot3=18$
> - 上 $\infty$: $t^8+14t^4+1=0$ の **8 点、$e=3$** ⟹ $8\cdot2=16$
> - Riemann–Hurwitz($g=0$): $\displaystyle R=\sum_P(e_P-1)=2\deg O-2=46$
> - ⟹ **上 $1$ の寄与は $46-34=12$**。**Galois ⟹ 同一分岐点上の $e$ は一定**なので、上 1 の点数 $r$ と指数 $e$ は $r(e-1)=12$ かつ $re=24$ を満たす ⟹ $re-r=12$ ⟹ $r=12,\ e=2$。**一意に決まる。**
> ⟹ **$O(t)-1$ を因数分解する必要はない。** $O$ の signature $(4,2,3)$・$\deg=24=\lvert S_4\rvert$ が確定。
>
> ```
> gate: Riemann-Hurwitz, O (deg 24, S4, type (4,2,3))
>   over 0  : 6 points e=4  -> 18
>   over inf: 8 points e=3  -> 16
>   known total = 34 ; RH total = 2d-2 = 46 ; over 1 must give 12
>   Galois => e constant over 1. e=2 => r*(2-1)=12 => r=12
>   consistency: r*e = 12*2 = 24 == d ? True
>   => 12 points, all e=2, forced by Galois (constant e) + RH.   PASS ? True
>   signature (4,2,3): 1/4+1/2+1/3 = 1.083333 > 1 ? True  (spherical, g=0 ok)
> gate: Riemann-Hurwitz, T (deg 12, A4, type (3,3,2))
>   sum(e-1) = 4*2+4*2+6*1 = 22 ;  RH: R = 2d-2 = 22   MATCH ? True
>   each fibre sums to d ? True
> ```
> **$T$ 側の整合($22=4\cdot2+4\cdot2+6\cdot1$)も同時に再検算し一致。**⟹ §4.1/§4.2 の分岐表は**紙 + 機械の二系統で裏づけ済**となった。
3. §3.2 の $\psi_{z^2}(\mathcal W_{k+1}\cap H)\subseteq\mathcal W_k$ は**要機械確認**。
4. $T$ 第 2 階の窓位数は**未測定**($12^{13}$ は粗い上界)。**推測で埋めない。**
5. **UNVERIFIED 債務(v1 §4 から継承・novelty 欄へ)**: **[12]** Nakamura, *Some classical views on the parameters of the GT group*(Progress in Galois Theory)と **[14]** Nakamura–Tsunogai, Forum Math. **15** (2003) 877–892 は**未取得・未確認**。**[NS] Invent. 141 は LNS 2026 §1/§8 の再説明により「lego 条件 = 別種」と判定済**(空席は白)。⟹ **novelty は [12] 確認まで主張しない。**

---

## §7 falsifier 照合記録(2026-08-26)

**判定 = PASS**(独立別証明 = $\pi\circ\psi$ の経由分解 / 数値 5291 構成で反例 0)。反映した修文 5 点:

| # | 指摘 | 反映箇所 |
|---|---|---|
| **F-1** | 「全射ゆえ割る」に kernel 経由の一行が要る | §1.1 の証明を $\psi^{-1}(\psi(K))=K\ker\psi$ 経由へ書き直し(**$\le$ で十分**・divisibility は不要) |
| **F-2** | **「$N$ が有限指数」が load-bearing**($N=1$ が (G-1)∧(G-2) の反例) | §1.1 に ⚠ 注記。定理文から有限指数を落とさない旨を明記 |
| **F-3** | 系は **(G-1) 付き**に限定せよ。(G-2) 単独の $\psi$-安定 $N$ は**実在** | §1.1 の系を (G-1) 版に限定。**witness を逐語収録**($H=a$-parity・$\psi(a^2)=1,\psi(b)=a,\psi(aba^{-1})=b$・$N=$ 対角 $\mathbb Z/2$ の核)。**退化枝 $NH=G_0$ の定義**も明示 |
| **F-4** | no-go は**各有限段のみ** — 塔の射影極限・compatible system には無言 | §1.3 を新設。「**不動点 = 死 / 軌道 = 生**」の境界線を式で明示。IMG 塔・二窓設計(§3)が補題と**完全整合**であることを記載 |
| **F-5** | 証明は Belyi 性・自由性・次数 $d$ を使わない一般事実 ⟹ **一般補題として定式化**せよ | §1.1 を **補題 VE-NOGO(一般形)**に昇格($G_0$ 任意群・$H\lneq G_0$・$\psi:H\twoheadrightarrow G_0$)。Belyi の場合は §1.2 の**系 DYN-NOGO** に降格。位置づけを「力学固有の障害ではなく、**仮想自己準同型と固定有限窓の一般的な非両立**」へ訂正 |

**格の更新**: §1(補題 VE-NOGO・系 DYN-NOGO・射程)= **paper-proof(falsifier 独立照合 PASS)**。§2 の撤回 2 件は確定。**§3(二窓仕様)・§4($T/O$ の分岐データ)・§5(prereg)は依然 `candidate`。**

**引用可能性の所見(F-5 の副産物)**: 補題 VE-NOGO は自己相似群論の一般命題として単独で意味を持つ(「仮想自己準同型は、その定義域に含まれる有限指数の特性商へは決して降りない」)。**$G_{\rm dyn}$ の外でも使える形**になったので、将来の論文化では独立した補題として置ける。

**残る債務(§6 と重複・再掲)**: ① ~~$O(t)-1$ の因数分解~~ ⟹ **閉鎖**(§6-2 の補題 O-RH・v2.3)② §3.2 の $\psi_{z^2}(\mathcal W_{k+1}\cap H)\subseteq\mathcal W_k$ は要機械確認 ③ $T$ 第 2 階の窓位数は未測定($12^{13}$ は粗い上界・**推測で埋めない**)④ [12]/[14] は UNVERIFIED ⟹ **novelty は主張しない**。

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

**意義(§1.3 の射程の強化)**: v2 §1.3 は「(G-1) 付きの固定窓は死ぬが、軌道(移動標的)なら生きる」と述べた。VE-COF はさらに強く、**(G-1) を課さない (G-2) 単独の窓(退化枝を含む)を全部集めても点を分離しない**と言う。

> ### ⚠ **v2.2 訂正(要修正 D)— 「唯一の道」は言い過ぎだった**
> **v2.1 の記述(撤回)**: 「移動標的 $\psi(N_{k+1}\cap H)\subseteq N_k$ は『便利な代案』ではなく**唯一の道**である。§3 の二窓設計はこの意味で**必然**。」
> **正しい射程**: VE-COF が示すのは **固定窓族の死(= 必要条件)** だけであって、**移動標的が機能することは何も言っていない**。「固定窓は駄目」⟹「移動標的なら良い」は導出されない。
> **反例(較正段そのもの)**: $z^2$ の $S_3$-対称化塔 $\mathcal W_k=\gamma_2(F_2)F_2^{2^k}$ は移動標的の条件を満たすが、**全 $k$ で $\mathcal W_k\supseteq[F_2,F_2]$** ゆえ
> $$\bigcap_k\mathcal W_k\ \supseteq\ [F_2,F_2]\ \neq\ 1$$
> で**塔は点を分離しない**。⟹ 移動標的でも「窓が届かない」ことは実際に起こる。
> **一般形**: 定義から $\displaystyle\bigcap_k N_k=\ker\bigl(F_2\twoheadrightarrow\mathrm{IMG}(\varphi)\bigr)$。
> ### ⚠ v2.4 更新 — **UNKNOWN は解消された**
> v2.2/v2.3 のこの位置には「**これが $1$ かどうかは $T$・$O$ について UNKNOWN**(… 推測であって証明ではない・格 = `heuristic`)」と書いてあった。**文献ゲート通過(裁定 1706)により無条件に確定 ⟹ 本文を置換する**:
> $$\boxed{\ \ker\bigl(F_2\twoheadrightarrow\mathrm{IMG}(T)\bigr)\ \neq\ 1\qquad(\textbf{格 = literature-backed}\,;\ \text{原典 [Nek05 Thm 5.5.3] は未見})\ }$$
> 鎖と逐語照合は **§9**。⟹ **$T$-塔は点を分離せず、分解能に天井がある。**$O$ も同じ論法(PCF 有理写像)で同結論。
> **P-DYN-1′(b) への直結**: $\ker(F_2\twoheadrightarrow\mathrm{IMG}(T))\ne1$ なら、**二窓テストの分解能はこの核で頭打ちになる** — $\mathrm{DYN}_T$ はこの核の中を見分けられない。⟹ **(b)「切断力が非零」の上限がここで決まる**。切断力ゼロが出ても「$T$ の力学が弱い」とは限らず「塔が届いていない」だけかもしれない。**この二つは実験では分離できない** ⟹ cert に**両方の解釈**を書くこと。
> **格**: 「移動標的が機能する」は **UNKNOWN**。§3 の二窓設計は「VE-COF に抵触しない唯一既知の形」であって「必然」ではない。

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
| 移動標的の塔 | 補題と整合(生) | **VE-COF に抵触しない唯一既知の形。機能するかは UNKNOWN**(v2.2 訂正・$z^2$ で $\bigcap\mathcal W_k\supseteq[F_2,F_2]\ne1$) |
| 実装の自己診断 | なし | **VE-TEST(1 元判定)** |

**残債務(v2 §6 から更新)**: ① ~~$O(t)-1$ の因数分解~~ ⟹ **閉鎖**(§6-2 補題 O-RH・v2.3)② $\psi_{z^2}$ の降下の機械確認 ③ $T$ 第 2 階の窓位数未測定 ④ [12]/[14] UNVERIFIED ⟹ novelty 非主張。
**v2.1 で追加された債務**: ⑤ 補題 VE-NOGO⁺・系 VE-COF は**未監査**(§1 の VE-NOGO は falsifier PASS 済だが、鋭形の 3 本の等号と VE-COF は本稿が初出)。

---

## §9 ★[DYN-CEIL] — $T$-塔の分解能天井(文献確定・v2.4 新設)

**格**: §9.1–§9.2 = `literature-backed`(現物逐語照合・**原典 [Nek05 Thm 5.5.3] は未見**)。§9.3 = `paper-proof + 機械一致`。§9.4–§9.6 = 系と設計含意。
**現物**(`papers/`・司法塔経由・文献ゲート通過): `nekrashevych-img-survey-lms387.pdf`(sha16 `5d606152275904a9`)/ `nekrashevych-0802.2554-free-subgroups-rooted-trees.pdf`(`397eac9bfe398c2d`)/ `bkn-0802.2837-amenability-automata-groups.pdf`(`02d5ac4adfacc164`)。
**私が読んだ範囲**: 上 2 本を `pdftotext` でテキスト化し、**該当箇所のみ**逐語確認(survey 全 2,853 行のうち §3.3–§3.4 周辺と PCF 言及行;0802.2554 全 505 行のうち導入・§3・§4)。**BKN は読んでいない**(§9.3 により本件では不要)。

---

### 9.1 ① 鎖の一次照合(逐語)

> **[survey L803]** "Since the virtual endomorphism associated with the iterated monodromy group IMG(p) maps a loop  to its lift by p, expanding maps will have contracting iterated monodromy group. More precisely, **the following theorem is proved in [Nek05, Theorem 5.5.3]**, where also a more detailed definition of an expanding covering is given."
> **[survey L805 = Theorem 3.3]** "**If the partial self-covering $p:M_1\to M$ is expanding, then IMG(p) is a contracting self-similar group.**"
> **[survey L806・直後の無番号文]** "**In particular, the iterated monodromy groups of post-critically finite rational functions are contracting.**"
> **[survey L856 = Theorem 3.5]**(三分岐)"Let $G$ be a group acting faithfully on a locally finite rooted tree $T$… Then one of the following is true: (1) $G$ has no free subgroups; (2) there is a free non-abelian subgroup $F\le G$ and a point $\xi$ … such that the stabilizer $F_\xi$ is trivial; (3) there is a point $\xi$ … and a free non-abelian subgroup $F\le G$ such that $F$ acts faithfully on all neighbourhoods of $\xi$."
> **[survey L870 = Theorem 3.6]** "**Contracting groups have no free subgroups.**"(証明が survey 本文に再録されている: 第 3 分岐は「切片が有限集合に落ちる」ことで、第 2 分岐は別途排除)
> **[0802.2554 L299 = Theorem 4.2]** "**Contracting groups have no free subgroups.**"
> **[0802.2554 L300(証明冒頭)]** "We have to eliminate the possibilities (2) and (3) of **Theorem 3.3**."
> **[0802.2554 L304 = Examples 3]** "Iterated monodromy groups … of expanding self-coverings of orbispaces, **in particular, iterated monodromy groups of post-critically finite rational functions, are contracting hence have no free subgroups.**"
> **[0802.2554 L29(導入)]** "This theorem implies, for instance, that **the iterated monodromy groups of post-critically finite rational functions** and other expanding dynamical systems (see [Nek05, BGN03]) **have no free subgroups**."
> **[survey L590(前振り)]** "In fact, we will prove later that **iterated monodromy groups of post-critically finite rational functions do not contain free subgroups**."

> ### ⚠ 引用番号の衝突(CV-9 型・**必ず論文タグを付けて引用すること**)
> **三分岐定理**は **survey では Theorem 3.5**、**0802.2554 では Theorem 3.3** である(同一内容・別番号)。0802.2554 の Thm 4.2 の証明が「Theorem 3.3 の (2)(3) を排除する」と書いているのは**自身の 3.3**(= survey 3.5)を指す。
> **無自由部分群定理**は **survey Thm 3.6 = 0802.2554 Thm 4.2**。
> ⟹ 以後 **[survey Thm 3.x] / [0802.2554 Thm y.z]** の形で必ずタグ付けする。

**格の記帳(3 点セットの 1)**: 最終命題「PCF 有理写像の IMG は自由部分群を持たない」は**二つの独立に公刊された出所で逐語に述べられている**(0802.2554 Examples 3 と導入;survey L590/L806+Thm 3.6)。**ただし「expanding ⟹ contracting」の証明は [Nek05 Thm 5.5.3] にあり、原典書籍は未入手・未見。** ⟹ **格 = `literature-backed`(原典未見)**。`verified` でも `paper-proof` でもない。

---

### 9.2 ② 適用条件の pin — $T$ は前提を満たすか

**必要なのは「$T$ が PCF 有理写像であること」だけ**である(survey L806 / 0802.2554 Examples 3 は PCF 有理写像に対して**追加条件なしで**述べている)。

- **[survey L520]** "If $f$ is post-critically finite, then it is a partial self-covering $f:\hat{\mathbb C}\setminus f^{-1}(P_f)\to\hat{\mathbb C}\setminus P_f$, since $f^{-1}(P_f)\supseteq P_f$." ⟹ **PCF ならば partial self-covering の構造が自動で立つ。**
- **$T$ は PCF**: $T$ は Belyi 写像なので臨界値は $\{0,1,\infty\}$ に含まれ、Belyi-extending の条件 $T(\{0,1,\infty\})\subseteq\{0,1,\infty\}$ より軌道は $\{0,1,\infty\}$ の中に留まる ⟹ $P_T\subseteq\{0,1,\infty\}$ 有限 ✓。**すなわち「Belyi-extending」は定義上「$P_\varphi\subseteq\{0,1,\infty\}$ なる PCF」であり、前提は構成から満たされる。**($T$ の具体値: $T(0)=0,\ T(1)=1,\ T(\infty)=1$ — §4.1 の分岐表。)
- **⚠ 「expanding」の扱い**: survey は Theorem 3.3 の仮定を "expanding" と置き、**その直後の "In particular" 文で PCF 有理写像を無条件に結論に入れている**。すなわち **PCF ⟹ expanding(適切な軌道体計量で)の部分は survey 本文では証明されず [Nek05 Thm 5.5.3] に委ねられている**("where also a more detailed definition of an expanding covering is given")。⟹ **この 1 リンクだけが未見**。**これが格 `literature-backed(原典未見)` の理由である。**
- **例外型(Lattès 等)の心配は不要**: survey Prop 5.2 は $\mathbb R^n/\mathbb Z^n$ 上の $A$ について「IMG が contracting $\iff$ $A$ が expanding」と述べており、Euclid 軌道体型も contracting 側に入る。**survey/0802.2554 のどちらも PCF 有理写像に例外を設けていない。**

---

### 9.3 ③ $T$ は多項式に共役でない — 経路 B は**元々不可**(機械確認)

**判定基準**: 次数 $d\ge2$ の有理写像が Möbius 共役で多項式になる $\iff$ **完全分岐する固定点**($e_P=d$)を持つ。
**Galois 被覆に特化した 1 行**: 分岐点上の各点は同じ $e$ を持ち $\#\text{fibre}\cdot e=d$。完全分岐点は $\#\text{fibre}=1$、すなわち**局所モノドロミー(巡回)が deck 群全体を生成する**ことを要求する ⟹ **deck 群が巡回でなければ完全分岐点は存在しない。**

```
gate: is T (resp. O) conjugate to a polynomial ?
--- T : deg = 12, deck group = A4, |G| = 12 ---
  |G| = deg ? true   G cyclic ? false
  fibres (#pts,e) = [[4,3],[4,3],[6,2]]  each #pts*e = deg ? true
  max ramification index e_max = 3  ; totally ramified needs e = 12
  exists fibre of size 1 ? false     => totally ramified point exists ? false
  possible e (orders of elements of G) = [ 1, 2, 3 ]
--- O : deg = 24, deck group = S4, |G| = 24 ---
  |G| = deg ? true   G cyclic ? false
  fibres (#pts,e) = [[6,4],[12,2],[8,3]]  each #pts*e = deg ? true
  max ramification index e_max = 4  ; totally ramified needs e = 24
  exists fibre of size 1 ? false     => totally ramified point exists ? false
CONCLUSION: neither T nor O is Moebius-conjugate to a polynomial.
```
(`scratchpad/math_gdyn_polyconj_v1.g`)

> ⟹ **経路 B(BKN Duke 154 (2010) の従順性・多項式限定)は $T$ には元々適用できない。**
> ⟹ **v2.3 で私が「従順性経由は使えないので不主張」と判断したのは正当**だった。**実害はゼロ**(経路 A が多項式限定なしで足りる)。
> ⟹ 副産物: **$O$ も同じ理由で多項式共役でない**。$A_4$・$S_4$ が非巡回であることが両方を同時に決めている。

---

### 9.4 ★ 系 DYN-CEIL

> ### 系 DYN-CEIL(分解能天井の存在)
> $\varphi$ を Belyi-extending(= $P_\varphi\subseteq\{0,1,\infty\}$ なる PCF 有理写像)、$\deg\varphi=d>1$ とする。
> $$\bigcap_{k}N_k\ =\ \ker\bigl(F_2\twoheadrightarrow\mathrm{IMG}(\varphi)\bigr)\ \neq\ 1 .$$
> **証明.** $\ker=1$ と仮定すると $F_2\hookrightarrow\mathrm{IMG}(\varphi)$、すなわち $\mathrm{IMG}(\varphi)$ は階数 2 の非可換自由部分群を含む。一方 [survey Thm 3.3 + L806 "In particular" / 0802.2554 Examples 3] より $\mathrm{IMG}(\varphi)$ は contracting、[survey Thm 3.6 = 0802.2554 Thm 4.2] より contracting 群は自由部分群を持たない。矛盾。∎
> **格 = `literature-backed`(原典 [Nek05 Thm 5.5.3] 未見)。**
> **副産物**: 同じ矛盾は「$\mathrm{IMG}(\varphi)$ 自身が非可換自由群である」可能性も排除する。

**3 点セット(要求どおり明記)**
1. **格**: `literature-backed`。**未見リンク = [Nek05 Thm 5.5.3]**(expanding ⟹ contracting の証明と expanding covering の詳細定義)。二次確認は [survey Thm 3.3+L806] と [0802.2554 Examples 3] の**独立 2 出所**。
2. **原典未見**: 書籍 *Self-similar groups*(Nek05)は未入手。**入手できれば格は `paper-proof(文献)` へ上がる**が、現状は上げない。
3. **$\Lambda$ テストとの関係**: §9.5(**別物**)。

---

### 9.5 ⚠ $\Lambda$ 天井テストとの関係 — **別物・独立**

`gdyn_t_measurement_spec_v1_3.md` §10.6(3) の $\Lambda$ テストは「$\Lambda_{N_k}$ が停留すれば塔は非 cofinal(COF-Λ の対偶)」というもので、**DYN-CEIL とは別の主張**である。

- **DYN-CEIL($\ker\ne1$)は $\Lambda$ の挙動を含意しない。** 核が $[F_2,F_2]$ に含まれていれば、$\Lambda_{N_k}=\ker(\mathbb Z^2\to Q_k^{\rm ab})$ は $0$ へ細り続けうる。**実際 $z^2$ の較正塔がその型**である($\bigcap\mathcal W_k\supseteq[F_2,F_2]\ne1$ なのに $\Lambda_{\mathcal W_k}=2^k\mathbb Z^2\to0$)。
- **逆も含意しない**: $\Lambda$ が停留しても、核が非自明であることは DYN-CEIL が既に与えているので新情報ではない — が、**「可換化水準ですでに天井が効いている」という構成的で深度つきの証明書**になる(DYN-CEIL は存在のみで**発効深度を与えない**)。
- ⟹ **実行中の $\Lambda$ 測定は中止しないこと。** DYN-CEIL が与えるのは「天井が在る」、$\Lambda$ 測定が与えるのは「**どこから**効くかの下からの証拠(可換化水準に限る)」。**別記帳**。

| | DYN-CEIL(§9.4) | $\Lambda$ テスト(spec v1.3 §10.6(3)) |
|---|---|---|
| 主張 | $\ker\ne1$(天井の**存在**) | $\Lambda$ 停留 ⟹ 塔が**非 cofinal** |
| 水準 | 群全体 | 可換化 $\mathbb Z^2$ のみ |
| 深度情報 | **なし**(漸近のみ) | **あり**(停留した段が証拠) |
| 格 | literature-backed | 機械測定(構成的) |
| 相互含意 | **なし(両方向とも)** | |

---

### 9.6 ⑤ 設計含意 — 「**一塔は有界・族が本体**」

DYN-NOGO(§1.3)は「**一窓は死・塔は生**」と言った。DYN-CEIL はその続きである:

$$\underbrace{\text{固定一窓}}_{\text{死(VE-NOGO)}}\ \longrightarrow\ \underbrace{\text{一つの写像 }\varphi\text{ の塔}}_{\textbf{有界(DYN-CEIL)}}\ \longrightarrow\ \underbrace{\text{Belyi-extending 族全体}}_{\text{本体}}$$

⟹ **$G_{\rm dyn}$ の定義が全 Belyi-extending 写像で量化していること(v1 §2 の定義 D)は飾りではなく本質である。** 単一写像の IMG 塔で $G_{\rm dyn}$ 型テストを走らせる限り、分解能は原理的に有界。

> ### ★ 後継問題(DYN-CEIL が置き換えた本当の問い)
> $$\bigcap_{\varphi\ \text{Belyi-extending}}\ \ker\bigl(F_2\twoheadrightarrow\mathrm{IMG}(\varphi)\bigr)\ \overset{?}{=}\ 1 .$$
> **これは $G_{\rm dyn}$ 族が無制限の分解能を持つための必要条件**である(共通核が非自明なら、**全ての** DYN テストが $F_2/\bigcap_\varphi\ker$ を経由し、族全体に共通の天井が生じる)。**UNKNOWN。**
> ⚠ 個々の $\ker$ が非自明であることは、共通核の非自明性を**含意しない** — 異なる $\varphi$ の核は異なりうる。**DYN-CEIL は族水準の問いを否定していない。**

**選定会議向けの 1 行(v2.3 の「$\ker$ 決定不能」を置換)**:
> **$T$-塔の天井は文献で確定した(DYN-CEIL)。$G_{\rm dyn}$ が無限分解能を持ちうるのは族水準でのみであり、単一塔路線の到達点は原理的に有界である。族水準の可否($\bigcap_\varphi\ker=1$?)は UNKNOWN。**

---

### 9.7 UNKNOWN・債務(推測で埋めていない)

1. **[Nek05 Thm 5.5.3] は未見。** 入手できれば DYN-CEIL の格が上がる。**【文献要請 DYN-L2】**: Nekrashevych, *Self-similar groups*(Math. Surveys Monogr. 117)の Thm 5.5.3 と、そこでの "expanding covering" の定義。
2. **共通核 $\bigcap_\varphi\ker$ は UNKNOWN**(§9.6 の後継問題)。族が有限個で尽きるのか、無限族が本当に分離するのかも未検討。
3. **天井の発効深度は未知**(DYN-CEIL は存在のみ)。⟹ 有限水準での (1)/(2) 分離は依然不能(§5 の Z-1 更新)。
4. **BKN(経路 B)は読んでいない** — §9.3 により本件では不要と判断したため。多項式型 Belyi-extending 写像($z^n$・Chebyshev 型)を将来使うなら**その時に読むこと**(それらは多項式なので経路 B が効き、従順性まで言える可能性がある)。
5. v2.3 からの継続債務: ② $\psi_{z^2}$ の降下の機械確認 ③ $T$ 第 2 階の窓位数(spec 側で実測進行中)④ [12]/[14] UNVERIFIED ⟹ **novelty は依然主張しない**。
