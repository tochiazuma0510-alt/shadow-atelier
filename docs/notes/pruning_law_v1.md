# 刈り込み処方(PRUNE)— 核の一般形の同定と紙上導出の試み v1

- 起草: 影工房 数学者(Claude)/ 2026-07-30
- 委嘱: レーン A-1(裁定 220/221 後)— I10-1 の刈り込み処方 / LG-6「なぜ $S_t$ 全部でなく $\mathrm{Syl}_2$ か」/ Stab 律 の合流点
- 入力: 裁定 220(I10-1 判定)/ `search/certs/i10_1_*_20260730.json` / `docs/notes/i10_1_prediction_v1.md`(NORM 包絡)/ `docs/notes/lg34_semilocal_design_v1.md` LG-6・【LG-b】/ `docs/notes/structthm_h2_v1.md`(STR-1/STR-2)
- 状態: **candidate**。§2 の同定は GAP 単系統の実測。§3 の律は 16 標本適合の **candidate**。§4 の導出は**半分だけ通り、残り半分の詰まり所を名指しした**。
- **封印遵守**: 有限群論と初等加群論のみ。分岐データは $\mathsf w:=b_1^{-1}a_1$、$\bar x=\mathsf w^2$。

---

## 0. 結論(先出し)

| 任務 | 結果 |
|---|---|
| **① $C_5^2$ の同定** | **和ゼロ(augmentation)ではない。$\{v\in\mathbf F_5^3: v_1=v_2\}$ — すなわち $\mathrm{Syl}_2$ が動かすブロック対の「対角」**。$\langle\bar x\rangle$(全対角)を**含む**。$r=2$ の $C_5$ も同じ規則で $\{v_1=v_2\}=\langle\bar x\rangle$(§2) |
| **② 律の形** | $\ell^{r-1}$ **ではない**。正しくは $$\boxed{\ \ker\widetilde\chi\ \cong\ C_{O_{2'}(\mathrm{Stab})}(S)\ \times\ S,\qquad S:=\mathrm{Syl}_2(\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x))\ }$$ すなわち**「$S$ の固定点まで刈り込む」**。奇部の位数は $\ell^{s_2(r)}$($s_2$ = **$r$ の 2 進桁和**)(§3) |
| **③ 統一** | **2-部律(Stab 律)と奇部律は同一の $S$ で書ける** — LG-6 の「なぜ $S_t$ 全部でなく $\mathrm{Syl}_2$ か」は「$S$ は自分自身を固定するから丸ごと残る」で説明がつく(§3.3) |
| **④ 適合** | **16/16 標本**(単一巡回 13 + $t=3$ の 18 + $r=2$ の 10 + $r=3$ の 50)。CYC-GEN を殺した $t=3$ の値も PRUNE が出す(§3.2) |
| **⑤ 導出** | $\subseteq$ 方向(奇部 $\subseteq C(S)$)は**既測の 2 事実から従う**(§4.2)。$\supseteq$ 方向(**飽和**)が詰まり所 — §4.3 で名指し |
| **⑥ 次の判別点** | **$r=4$**。$\ell^{r-1}$ 律なら $\ell^3=125$、PRUNE なら $\ell^{s_2(4)}=\ell^1=5$ — **25 倍差**。$n=20$・$\Xi=4.5\times10^8$(§5) |

---

## 1. 記法と既測の土台

窓は命題 0.3 型($c\in N$、$P=A_n$、$\bar x=(\ell^r,1^t)$、$\ell$ 奇)。$\mathrm{Aut}(P)=S_n$ で
$$\mathrm{Stab}:=\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)=C_{S_n}(\bar x)=(C_\ell\wr S_r)\times S_t .$$
$B:=C_\ell^{\,r}$(輪積の**基底**)、$T:=S_r$(輪積の**頂**)。$\ell$ 奇ゆえ
$$O_{2'}(\mathrm{Stab})=\bigl(B\rtimes O_{2'}(S_r)\bigr)\times O_{2'}(S_t),\qquad
S:=\mathrm{Syl}_2(\mathrm{Stab})=\mathrm{Syl}_2(S_r)\times\mathrm{Syl}_2(S_t).$$
$\langle\bar x\rangle\cong C_\ell$ は $B$ の**全対角**。

$\Xi$(監査 §7.1・命題 3.1)は $[m,f]\mapsto E_{m,f}\in\mathrm{Aut}(P)$。$m=0$ では $E_{0,f}(\bar x)=\bar x$・$E_{0,f}(\bar y)=\bar y^{\,f}$ ゆえ
$$\boxed{\ \Xi(\ker\widetilde\chi)\subseteq\mathrm{Stab}\ }$$
であり、$\Xi$ は群準同型(合成則 (3.53) の $E$ の乗法性)。

---

## 2. 任務 ① — 部分加群の同定(実測の生成元から)

### 2.1 座標の取り方(**$f$-座標ではなく $\Xi$-像で読む**)

最初に $f$ 自身の座標を見たが、**核の $f$ のうち $\bar y$ を中心化するものは単位元だけ**($r=2$: 1/10、$r=3$: 1/50)。$f$ は $C_P(\bar y)$ に住んでいない。正しい座標は $\Xi$-像である:
$$f=c\cdot\alpha\quad(c\in C_{S_n}(\bar y),\ \alpha\in\mathrm{Stab}),\qquad \Xi([0,f])=\alpha .$$
分解は一意($C_{S_n}(\bar y)\cap\mathrm{Stab}=C_{S_n}(P)=1$)。

**較正**: この規約で $m=0$ hexagon((3.3)(3.4)・$c=1$)を $\Xi$-制限で解くと $\lvert\ker\widetilde\chi\rvert=10$($r{=}2$)・$50$($r{=}3$)— **証明書の値と一致**(`prune_ident2.g`)。さらに $\Xi$ は**単射**(相異なる $\alpha$ が 10 個 / 50 個)⟹ $\ker\Xi=1$(D1 の観測が本族でも成立)。

### 2.2 実測

**$r=3$($n=15$)**: $\bar x$ の巡回 $=[1,3,5,7,9],[2,4,6,8,10],[11,13,15,12,14]$、$B=\langle$それら$\rangle\cong C_5^3$、$\bar x=$ 全対角。
$$\Xi(\ker\widetilde\chi)\ \text{位数}\ 50\ \cong C_{10}\times C_5,\qquad A:=\mathrm{Syl}_5(\Xi(\ker))\ \text{位数}\ 25\cong C_5^2 .$$
$A$ の $B$-座標(全 25 個・機械出力):
$$A=\bigl\{(a,a,b)\ :\ a,b\in\mathbf F_5\bigr\}\ =\ \{v\in\mathbf F_5^3:\ v_1=v_2\}.$$
- **和ゼロ(augmentation)ではない**(座標和は $0,1,2,3,4$ を全部取る)。
- **$\langle\bar x\rangle=\langle(1,1,1)\rangle\subseteq A$** ✓(行 $[1,1,1]$ が存在)。
- $\mathrm{Syl}_2(\Xi(\ker))=\langle\tau\rangle$、$\tau=(1,6)(2,7)(3,8)(4,9)(5,10)$ = **ブロック 1 と 2 の入れ替え**(ブロック 3 は点ごとに固定)。

> $$\boxed{\ A=\{v:v_1=v_2\}=C_B(\tau)=B^{\tau}\ }$$
> **$A$ は $\tau$ の固定部分空間そのもの。** $\dim=2$。

**$r=2$($n=10$)**: $B\cong C_5^2$、$A$ 位数 5、座標 $\{(a,a)\}$ = **対角** $=\langle\bar x\rangle=B^\tau$($\tau$ = 2 ブロックの入れ替え)。$\dim=1$ ✓。
$\Xi(\ker)=A\times\langle\tau\rangle\cong C_{10}$ ✓。

**両窓とも** $\Xi(\ker\widetilde\chi)=B^{\tau}\times\langle\tau\rangle$ で、位数 $5\cdot2=10$ / $25\cdot2=50$ ✓ 証明書一致。

### 2.3 なぜ「和ゼロ」ではないか(加群論の注意)

$B=\mathbf F_5[C_3]$ を**輪積の頂 $C_3$ の加群**として見ると $x^3-1=(x-1)(x^2+x+1)$、$\mathbf F_5$ に 1 の原始 3 乗根はない($\lvert\mathbf F_5^\times\rvert=4$)ので $x^2+x+1$ は既約 ⟹ $B=\langle\text{対角}\rangle\oplus(\text{和ゼロ})$ で**部分加群は 4 個だけ**。もし $A$ が $C_3$-部分加群なら位数 25 のものは和ゼロしかない。
**しかし $A$ は $C_3$-部分加群ではない** — $\Xi(\ker)$ に $C_3$ は入っておらず($\lvert\Xi(\ker)\rvert=50$、$3\nmid50$)、$A$ は $\langle\tau\rangle$-加群としてのみ意味をもつ。$\tau$ は互換なので $\dim B^\tau=r-1$($r=3$)。**「和ゼロか対角か」という問いの立て方自体が、作用する群を $C_3$ と取り違えていた**。

---

## 3. 任務 ② — 刈り込み処方(PRUNE)の主張文

### 3.1 主張

> ### 予想 PRUNE(刈り込み処方・candidate)
> charming・$c\in N$・$P$ 単純な窓で、$S:=\mathrm{Syl}_2\bigl(\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)\bigr)$ とおくと
> $$\boxed{\ \Xi\bigl(\ker\widetilde\chi\bigr)\;=\;C_{O_{2'}(\mathrm{Stab})}(S)\;\times\;S\;=:\;\mathrm{Pr}(\mathrm{Stab}) \ }$$
> (直積:$S$ は定義から固定点集合に自明作用し、位数は互いに素)。したがって
> $$\lvert\ker\widetilde\chi\rvert=\bigl\lvert C_{O_{2'}(\mathrm{Stab})}(S)\bigr\rvert\cdot\lvert S\rvert,\qquad
> \mathrm{GTSh}(N,N)\;\cong\;S\times\Bigl(C_{O_{2'}(\mathrm{Stab})}(S)\rtimes Q\Bigr).$$
> **刈り込み = 「奇根基の $S$-固定点を取り、$S$ を戻す」という関手 $\mathrm{Pr}$。**

$\mathrm{Pr}$ は $S$ の取り方(Sylow)に依らず共役を除いて定まる。

### 3.2 適合(16 標本)

$\bar x=(\ell^r,1^t)$ で $\mathrm{Stab}=(C_\ell\wr S_r)\times S_t$、$O_{2'}(\mathrm{Stab})=\bigl(B\rtimes O_{2'}(S_r)\bigr)\times O_{2'}(S_t)$。
$O_{2'}(S_t)=C_3$($t=3$)、$=1$($t\ne3$)。$O_{2'}(S_r)$ も同様。

| 窓族 | $r$ | $t$ | $S$ | $C_{O_{2'}}(S)$ | 予測 $\lvert\ker\rvert$ | 実測 | |
|---|---|---|---|---|---|---|---|
| A16/A18/A20(3 窓) | 1 | 5 | $D_8$ | $C_\ell$($D_8$ は尾部にあり $B$ に自明作用) | $8\ell$ | $88/104/120$ | ✓ |
| 梯子 $t=1$ | 1 | 1 | $1$ | $C_9$ | $9$ | (予言 9) | — |
| 梯子 $t=2$ | 1 | 2 | $C_2$ | $C_9$ | $18$ | (予言 18) | — |
| **梯子 $t=3$** | 1 | 3 | $C_2$ | $C_9\times C_{C_3}(\tau)=C_9\times1$ | $\mathbf{18}$ | **18** | ✓ **CYC-GEN(54)を殺した値を PRUNE が出す** |
| 梯子 $t=4$ | 1 | 4 | $D_8$ | $C_9$ | $72$ | (予言 72) | — |
| settled S1/S3/S4/S5 | 1 | 0 | $1$ | $C_\ell$ | $\ell$ | $\mathrm{Hol}$ 側と整合 | ✓ |
| **`W-E-A10-5x2t0`** | **2** | 0 | $C_2$(ブロック互換) | $B^\tau=C_5$ | $\mathbf{10}$ | **10** | ✓ |
| **`W-E-A15-5x3t0`** | **3** | 0 | $C_2$(ブロック互換) | $B^\tau=C_5^2$ | $\mathbf{50}$ | **50** | ✓ |

**$t=3$ の行が要**: そこでは $O_{2'}(S_3)=C_3$ が存在し、$S=C_2$ が**それを反転する**ので $C_{C_3}(S)=1$ — つまり「尾部の奇部は全部死ぬ」。CYC-GEN(丸ごと残す)は $54$ を予言して死んだ。**PRUNE は死因まで説明する**。

### 3.3 LG-6 への回答 — 「なぜ $S_t$ 全部でなく $\mathrm{Syl}_2$ か」

PRUNE の下では **2-部と奇部は別々の法則ではない**:
- 奇部は $S$ の**固定点**まで刈られる。
- 2-部が $S$ **丸ごと**残るのは、$S$ が**自分自身を中心化する**からではなく、$\mathrm{Pr}$ の定義が「$S$ を戻す」だからである。より内在的には、$\mathrm{Pr}(H)=C_{O_{2'}(H)}(S)\times S$ は $H$ の**$S$-固定点関手の像**と $S$ の合成であり、$H$ の 2-側は $S$ 以上に大きくなりようがない($S$ は Sylow)。
- 単一巡回窓で「$\mathrm{Syl}_2(S_t)$ 丸ごと」に見えたのは、そこで $O_{2'}(S_t)=1$($t\ne3$)で**刈るべき奇部が最初からなかった**ため。$t=3$ で初めて刈り込みが見え、実際に $C_3$ が消えた。

> **LG-6 / 【LG-b】への一行回答(candidate)**: 「$S_t$ の奇部が GT に見えない」のではなく、**$O_{2'}$ の $S$-非固定部分が見えない**。$t\le5$ では $O_{2'}(S_t)$ が $t=3$以外で自明なので、現象が「$\mathrm{Syl}_2$ しか残らない」の形に退化して見えていた。

### 3.4 STR-2 の一般化

STR-2(裁定・W4)は $\mathrm{GTSh}\cong D_8\times\mathrm{Hol}(\mathbf Z/N_{\rm ord})$。PRUNE はこれを
$$\mathrm{GTSh}\ \cong\ S\times\bigl(C_{O_{2'}(\mathrm{Stab})}(S)\rtimes Q\bigr)$$
に一般化する。$r=1$・$t\ne3$ では $C_{O_{2'}}(S)=C_\ell=\langle\bar x\rangle$、$Q=\mathrm{Aut}(C_\ell)$ ゆえ第二因子 $=\mathrm{Hol}(\mathbf Z/\ell)$ ✓、$S=\mathrm{Syl}_2(S_t)$ ✓ — **STR-2 の逐語再現**。
$r=3$ での検算: $S\times(C_5^2\rtimes C_4)$、位数 $2\cdot100=200$ ✓ 実測 $\lvert\mathrm{GTSh}\rvert=200$・`IdGroup [200,47]` と整合。$r=2$: $C_2\times(C_5\rtimes C_4)=C_2\times\mathrm{Hol}(C_5)$、位数 40 ✓ 実測 `[40,12]` ✓。

### 3.5 位数の閉じた式 — **$\ell^{r-1}$ ではなく $\ell^{s_2(r)}$**

$S\cap T=\mathrm{Syl}_2(S_r)$ の $r$ 個のブロックへの作用を考える。$r=\sum_i 2^{a_i}$(2 進展開・相異なる $a_i$)なら
$$\mathrm{Syl}_2(S_r)\cong\prod_i\mathrm{Syl}_2(S_{2^{a_i}}),$$
各因子は自分のブロック塊上**推移的**。ゆえに軌道数 $=\#\{i\}=s_2(r)$($r$ の 2 進桁和)。$B=\mathbf F_\ell^{\,r}$ の置換加群としての固定部分空間の次元は軌道数に等しいので

> ### 系 PRUNE-1(位数の閉じた式)
> $t\notin\{3\}$ かつ $O_{2'}(S_r)$ 側の寄与を除けば
> $$\boxed{\ \bigl\lvert\text{核の奇部}\bigr\rvert=\ell^{\,s_2(r)},\qquad s_2(r)=r\ \text{の 2 進桁和}.\ }$$

| $r$ | 1 | 2 | 3 | **4** | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $s_2(r)$ | 1 | 1 | 2 | **1** | 2 | 2 | 3 | 1 |
| $\ell^{r-1}$ 律なら | $\ell^0$ | $\ell^1$ | $\ell^2$ | $\ell^3$ | $\ell^4$ | $\ell^5$ | $\ell^6$ | $\ell^7$ |
| 実測 | $\ell$ | $\ell$ | $\ell^2$ | ? | ? | ? | ? | ? |

**$\ell^{r-1}$ 律は $r=2,3$ でだけ $s_2$ と一致する偶然**($s_2(2)=1=2-1$、$s_2(3)=2=3-1$)。**$r=1$ では既に破れている**(観測 $\ell$、$\ell^{r-1}=1$)— 裁定 220 の「$5^{0+1}$?」の疑問符はここを突いていた。
**$s_2$ 律は $r$ について単調でない**(4 で 1 に落ちる)— これが最も鋭い署名。

---

## 4. 任務 ② の後半 — 紙上導出の試み

### 4.1 何を示すべきか

$\Xi$ が単射(既測)として、示すべきは
$$\Xi(\ker\widetilde\chi)\ \overset{(\subseteq)}{\subseteq}\ \mathrm{Pr}(\mathrm{Stab})\ \overset{(\supseteq)}{\subseteq}\ \Xi(\ker\widetilde\chi).$$

### 4.2 【通る】$\subseteq$ 方向 — 既測の 2 事実からの帰結

> ### 補題 PR-1($\subseteq$)
> 次の 2 つを仮定する:
> **(D)** $\ker\widetilde\chi=A\times S'$(奇部 $A$ と 2-部 $S'$ の**直積**)。
> **(T)** $S'\cong\mathrm{Syl}_2(\mathrm{Stab})$ で、$\Xi(S')$ は $\mathrm{Stab}$ の Sylow 2-部分群(**Stab 律**)。
> このとき $\Xi(A)\subseteq C_{O_{2'}(\mathrm{Stab})}\bigl(\Xi(S')\bigr)$。

**証明.** (D) より $A$ は $S'$ を元ごとに中心化する。$\Xi$ は準同型なので $\Xi(A)$ は $\Xi(S')$ を中心化する。$\Xi(A)$ は奇位数で $\mathrm{Stab}$ の正規部分群($A$ は $\ker\widetilde\chi$ の特性部分群、$\ker\widetilde\chi\trianglelefteq\mathrm{GTSh}$)…ではないので、正確には:$\Xi(A)$ は奇位数の部分群で $\Xi(S')$ を中心化する。$\mathrm{Stab}=(C_\ell\wr S_r)\times S_t$ の奇位数元は $O_{2'}(\mathrm{Stab})$ に入るとは限らないが、$\Xi(A)$ は $\ker\widetilde\chi$ の像ゆえ $\mathrm{Stab}$ で正規化され、奇位数の正規化される部分群は $O_{2'}$ に入る。∎(最後の一歩は $\mathrm{Stab}$ の可解性を使う — 本族では $\mathrm{Stab}$ は $t\le5$・$r\le4$ で可解。**非可解 Stab 窓では別途要検討**。)

**格**: (D)(T) は**既測の観測**(15/15・16/16)であって定理ではない。よって補題 PR-1 は「観測 ⟹ 観測」の橋であり、**$\subseteq$ を無条件に証明したわけではない**。しかし **2 つの独立な観測を 1 つに束ねた**点で前進 — 以後は (D)(T) だけを証明対象にすればよい。

### 4.3 【詰まる】$\supseteq$ 方向 — **飽和(saturation)**が出ない

示すべきは「$C_{O_{2'}(\mathrm{Stab})}(S)$ の**すべての**元が実際に shadow として実現する」。これは**存在主張**であり、hexagon (3.3)(3.4) を解いて $f$ を作る必要がある。詰まる箇所を正確に書く:

> ### 【GAP-PR-1】$\alpha\in C_{O_{2'}(\mathrm{Stab})}(S)$ から $f$ を作る構成が無い
> $m=0$ の hexagon は
> $$s_1f^{-1}s_2f=f^{-1}s_1s_2,\qquad f^{-1}s_2fs_1=s_2s_1f$$
> で、$\Xi$-制限は $f\in C_{S_n}(\bar y)\alpha$ を与えるだけ。**この 375〜750 元の剰余類の中に解があるか**は、現状では**走査でしか分からない**(実測では各 $\alpha\in\mathrm{Pr}$ にちょうど 1 個の $f$、$\alpha\notin\mathrm{Pr}$ には 0 個 — $\Xi$ 単射と整合)。
> **必要な補題の型**: 「$\alpha$ が $S$ を中心化する ⟹ hexagon の $f$ が $C_{S_n}(\bar y)\alpha$ 内に存在」。これは **I10-3 の LOC(局所化)仮説と同じ型の主張**($S$-中心化が $f$ の実効台を $\langle\bar x\rangle$ 側へ落とす)であり、独立に攻めるより **LOC-1〜3 の証明経路に相乗り**するのが自然。

> ### 【GAP-PR-2】(D) の直積性が出ない
> $\ker\widetilde\chi=A\times S'$(半直積でない)は 16/16 の観測。これは STR-1 の $\varepsilon=0$(【GAP-1】)と**同じ穴**である。$\mathrm{Pr}$ が直積の形をしているのは (D) の帰結であって、(D) 自体は未証明。

> ### 【GAP-PR-3】Stab 律((T))の像側の理由が無い
> 「$\Xi(\ker)$ の 2-部が $\mathrm{Stab}$ の Sylow **丸ごと**」の理由。LG-6 の未解明部そのもの。PRUNE はこれを前提にしており、**説明していない**。
> ただし PRUNE は問いを狭めた: 以前は「なぜ $S_t$ の奇部が消えるか」+「なぜ 2-部が丸ごと残るか」の 2 問だったが、前者は $C(S)$ で説明済みになり、**残る未解明は後者 1 問**。

### 4.4 詰まりの構造(なぜ半分しか出ないか)

$\subseteq$ は**群論的**($\Xi$ が準同型・直積・中心化)。$\supseteq$ は**算術的**(hexagon の可解性)。GT 側の入力(F2 三条件・$R_\tau$・(3.53))は $\subseteq$ にはほとんど効かず、$\supseteq$ に全部効く。
$R_\tau$(「$N_{\rm ord}$ 外の奇素数を第二 hexagon が全滅させる」)は「**何が死ぬか**」の定理であり、PRUNE の $\subseteq$ 側と同じ向き。**「何が生き残るか」を出す定理は工房にまだ一本もない** — これが $\supseteq$ が出ない構造的理由である。

---

## 5. 任務 ③ — 次の判別点

### 5.1 決定的判別: $r=4$

| 窓 | $n$ | $S=\mathrm{Syl}_2(S_4)$ | ブロック軌道 | PRUNE 予測 $\lvert$奇部$\rvert$ | $\ell^{r-1}$ 律の予測 |
|---|---|---|---|---|---|
| $\bar x=(5^4)$、$t=0$ | 20 | $D_8$(4 ブロックに**推移的**) | 1 | $\boxed{5^1=5}$、$\lvert\ker\rvert=5\cdot8=\mathbf{40}$ | $5^3=125$、$\lvert\ker\rvert=1000$ |

**25 倍差**。$\mathrm{Syl}_2(S_4)=D_8$ がブロックに推移的なので $B^S=$ 全対角 $=\langle\bar x\rangle$ ちょうど。

**存在設計の一次点検**(裁定 209 のチェック順: 系 0.4′ → 補題 R 両パリティ):
- 系 0.4′: $N_{\rm ord}=\ell=5\ge4$ ✓。$\mathrm{ord}(\mathsf w)=10\ge7$ ✓($p\ge1$ 必要)。
- 補題 R($n=20$、$c(b')_{\min}=20-2\lfloor20/3\rfloor=8$、$\mathsf w=(2\ell)^p(\ell)^{r-2p}$、$c(\mathsf w)=r-p$、$\mathrm{sign}(\mathsf w)=(-1)^p$):
 - $p=2$($\mathsf w=(10,10)$、$c=2$、偶)⟹ $k$ 偶 $\le10$、$c(a')=10$。和 $=10+8+2=20\le22$ ✓ **余裕 2**
 - $p=1$($\mathsf w=(10,5,5)$、$c=3$、奇)⟹ $k$ 奇 $\le9$、$c(a')=11$。和 $=11+8+3=22=22$ ✓ **等号**
 **両パリティ枝とも Ree 通過**。実現探索は $S_{20}$ の無作為探索(存在は UNKNOWN)。
- 予算: $\mathrm{Stab}=C_5\wr S_4$ 位数 $15{,}000$、$C_P(\bar y)=7{,}500$、$c_m=\varphi(10)=4$ ⟹ $\Xi=4\times7500\times15000=\mathbf{4.5\times10^8}$(A19-13t6 の $5.3\times10^8$ と同等 = 実行可能圏)。

### 5.2 安価な補助判別

- **$r=3,\ t=3$**($\bar x=(5^3,1^3)$、$n=18$): $S=C_2\times C_2$、$C_{O_{2'}}(S)=B^{\tau_1}\times C_{C_3}(\tau_2)=5^2\times1$ ⟹ $\lvert\ker\rvert=25\cdot4=100$。$r$ の問いには非決定的だが、**2 つの $C(S)$ 刈り込みが同時に効く初の窓**(基底側と尾部側)。$\Xi=4\times2250\times4500=4.05\times10^7$ — $r=4$ の 1/11。
- **$r=5$**($n=25$): $s_2(5)=2$ ⟹ $\ell^2=25$、$\lvert\ker\rvert=25\cdot8=200$。$\ell^{r-1}$ なら $5^4=625$。$\mathrm{Stab}=C_5\wr S_5$ 位数 $375{,}000$ ⟹ $\Xi\approx2.8\times10^{11}$ **不能**。
 ⟹ **$r=4$ が唯一の実行可能な決定打**。

### 5.3 予言として凍結すべき欄(案・値は司令塔の凍結対象)

$r=4$ 窓 `W-E-A20-5x4t0`(実現後に確定)について: $\lvert\ker\widetilde\chi\rvert$ / 奇部の位数 / 奇部の $B$-座標(全対角か否か)/ $\mathrm{Syl}_2(\Xi(\ker))$ が $D_8$ か / $\lvert\mathrm{GTSh}\rvert=\lvert\ker\rvert\cdot4$ / $\mathrm{GTSh}\cong D_8\times\mathrm{Hol}(C_5)$ か。

---

## 6. 自己点検

- §2 の同定は **GAP 単系統**。ただし $\lvert\ker\rvert=10,50$ が証明書と一致したことが hexagon 規約の較正になっている(独立実装ではないが、判定器と別経路)。
- §3 の PRUNE は **16 標本適合の candidate**。うち 4 標本(梯子 $t=1,2,4$・settled 群)は**予言値であって実測ではない** — 実質の実測適合は **12 標本**。
- $r$ の範囲は $\le3$、$t$ の範囲は $\le5$ しか見ていない。$s_2$ 律の非単調性は **$r\ge4$ で一度も検証されていない**(§5 がその手当て)。
- §4.2 の補題 PR-1 は最後の一歩で $\mathrm{Stab}$ の**可解性**を使う。非可解 $\mathrm{Stab}$(壁標的の本命)では未検討 — **壁キャンペーンへ持ち込む前に要拡張**。
- $\Xi$ の単射性は本族 2 窓で実測。一般には未証明(監査 §7.1 の観測)。
- 「和ゼロではない」は $\tau$ を作用群に取った場合の話。**もし将来 $\Xi(\ker)$ に $C_3$(輪積頂の奇部)が入る窓が出れば、$A$ は $C_3$-加群になり和ゼロが復活しうる** — その窓は $O_{2'}(S_r)\ne1$ すなわち $r\ge3$ かつ $S_r$ の奇部が生き残る場合で、PRUNE は「生き残らない」と予言している($C_{O_{2'}(S_r)}(S)$ で $S$ が $C_3$ を反転するため)。$r=3$ で実際に生き残らなかった ✓。

## 7. 検算(GAP 4.16.0・`gap.ps1`・単系統)

| スクリプト | 内容 |
|---|---|
| `search/probe/wac_v1/prune_ident.g` | $f$-座標での試行(核の $f$ は $C_P(\bar y)$ に住まないことを確認 — 座標の取り直しの根拠) |
| `search/probe/wac_v1/prune_ident2.g` | $\Xi$-像での同定($\lvert\ker\rvert=10,50$ の較正・$\ker\Xi=1$・$A=B^\tau$ の座標全列挙・$\mathrm{Syl}_2$ の生成元) |

**登録宇宙の掃引結果ではない。台帳請求権は発生していない。**
