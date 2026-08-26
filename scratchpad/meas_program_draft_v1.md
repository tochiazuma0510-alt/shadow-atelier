# MEAS プログラム 草案 v1 — 井原の証人問題の測度論的再定式化

- **委嘱**: 司令塔(研究者発案・優先度高)。骨子 6 点の精密化・訂正。
- **格**: 全体 `candidate`。§2–§3 の定理 M1–M3・M6–M7 は**紙証明を起草済**(自前・未監査 ⟹ Sol 監査に回す前提)。§4 の M4/M5 は**前件つき**。§5–§6 の読みは**解釈**であって測定ではない。
- **著者**: 数学者(Opus 5)。**新規の窓計算ゼロ**(GAP 不使用)。機械は密度・log 比の整数/浮動小数計算のみ。
- **読んだ範囲**: `docs/状態.md`・`sol/sol_reply_159_iv.md` §15.1/§12.5–12.7・`docs/notes/b4_direct_adjudication_feasibility_v1.md` §4.4・`docs/notes/bit252_adversarial_reading_v1.md` ③・`docs/notes/bhunt_l1_bridge_v1_1_erratum.md` §5.3・`scratchpad/d972_idx3_arith_datum_independent_v1.md` §7–§12(既読)。**外部文献の直接参照ゼロ**(文献ゲート遵守)。

---

## §0 要旨と、司令塔の粗描への訂正 4 点

測度論化の**本当の利得は「像の測度」ではない**。閉部分群の Haar 測度は 0-1 的でほとんど情報を持たない(定理 M2)。利得は次の 3 つに局在する。

1. **窓ごとの fake/証人ビットが、そのまま Haar 測度の局所因子である**(定理 M6+M7)。⟹ 972 戦役・BIT-252 は「1 個の測度因子の決定」という同一の型で、両者は**素数指数の二分律**という 1 本の補題に統一される。
2. **リフト空間 $L(g)$ の正準測度は、構成不要で存在する** — $L(g)$ は Haar の条件付き測度(fibre)そのものだから(定理 M3)。DICHOT (2) は「有限段から組み上げる」場合にだけ必要で、しかも**それ単独では足りない**(段全射性が要る)。
3. **証人問題は「$\prod q_j$ の正値性」= 総和 $\sum(1-q_j)$ の収束性**に翻訳される(定理 M5)。ここで**ランダムネスは仮定ではなく Haar** であり、増分の独立性は**定理**である。仮定が要るのは「欠陥関数の繊維上の分布」だけで、それは有限段で測れる。

### 訂正(司令塔の粗描に対して)

| # | 粗描 | 訂正 |
|---|---|---|
| **C-1** | $\mu(C)=\lim\lvert C_N\rvert/\lvert GT(N)\rvert$ | 分母は $GT(N)$ ではなく**安定像** $GT(N)^{\rm st}=p_N(\varprojlim)$。段が全射でない限り生密度は**下界**にしかならない。しかも「段が全射か」= fake/証人問題そのもの ⟹ **台帳は 2 列(生密度・安定密度)必須で、安定列はほぼ UNKNOWN**。 |
| **C-2** | 「極限測度 > 0 ⟹ 証人存在(構成不要)」 | 真だが**コンパクト性(König)より弱い**。$\forall j:V_j\ne\emptyset$ だけで存在は出る(測度 0 でよい)。測度が買うのは存在ではなく **(a) 汎用性/ランダム探索の成功 (b) 有限段データからの外挿の型 (c) 片側反証の座標**。 |
| **C-3** | 「DICHOT (2) を前件として一様測度の逆極限が well-defined」 | DICHOT (2)(繊維 = $\ker R$ の剰余類)は**一様性**を与えるが**両立性**は与えない。両立性 $\iff$ 段写像 $F_M\to F_N$ の**全射性**。⟹ 正しい前件は (2)+**段全射**。逆に $\mathcal G$ が群と分かっていれば $L(g)=p_K^{-1}(g)$ で測度は自動(M3)。 |
| **C-4** | 「NW(7) = 1/7」 | 値は正しい($42/294$)が、**同じ工房内に別の 1/7 がある**(`bit252_adversarial_reading_v1.md` ③ の可解性事前確率 $7^1/7^2$)。両者は別物 ⟹ 台帳で **NAME-COLLIDE 警告**を立てる。さらに NW(7) では $\mathfrak G_{\rm ar}=\mathfrak G_{\rm pent}$ ゆえ **1/7 は井原ギャップ(gap 1)の密度ではない**(gap 1 は 1)。 |

---

## §1 設定 — 4 列の鎖(何を測っているかの固定)

$\mathcal I$ = 窓(有限指数正規部分群)の有向poset、$K\subseteq N$ のとき $R_{K,N}:GT(N)\to GT(K)$(細 → 粗)。

**前件 (P-ISO)**: 使う cofinal 部分系はすべて **isolated** 窓からなる ⟹ 各 $GT(N)$ は群、$R$ は群準同型(2401 Def 3.13 直後 / Remark 3.16)。**格 = UNKNOWN**(isolated 窓の cofinal 性は当工房で未証明。`RUNG-LADDER/v1`(公平 isolated-core 累積梯子・cofinal 保証)が**まさにこの前件を放電するための器具**)。

**前件 (P-COF)**: 系は全窓 poset で cofinal ⟹ $\mathcal G:=\varprojlim_N GT(N)\cong\widehat{GT}_{gen}$(2405 Thm 5.2)。

各窓で **4 つの部分集合の鎖**を分けて書く(混ぜないことが最重要):

$$\underbrace{\mathrm{Im}(\mathrm{Ih}_N)}_{\text{算術}}\ \subseteq\ \underbrace{\mathfrak G_{\rm pent}(N)}_{\widehat{GT}\ \text{の窓像}}\ \subseteq\ \underbrace{GT(N)^{\rm st}}_{\widehat{GT}_{gen}\ \text{の窓像}=\text{genuine}}\ \subseteq\ \underbrace{GT(N)}_{\text{窓の全 shadow}}$$

- **gap 1** = 第 1 の指数 = **井原ギャップ**(窓水準)。
- **gap 2** = 第 2 の指数 = **pentagon ギャップ**($\widehat{GT}_{gen}\supsetneq\widehat{GT}$ の窓証拠)。
- **gap 3** = 第 3 の指数 = **fake 指数**(有限深度で死ぬ shadow の分)。

生密度 $\lvert\mathrm{Im}(\mathrm{Ih}_N)\rvert/\lvert GT(N)\rvert$ は **3 つのギャップの積**であって、単独では何のギャップも同定しない。**台帳はこの分解つきで書く**(§6)。

---

## §2 辞書の定理化

### 定理 M1(窓密度 = Haar 測度)
(P-ISO)(P-COF) の下、$\mathcal G$ は副有限群、$\mu$ を正規化 Haar、$p_N:\mathcal G\to GT(N)$、$GT(N)^{\rm st}:=p_N(\mathcal G)$ とする。

1. $GT(N)^{\rm st}=\bigcap_{M\supseteq' N}\mathrm{im}(R_{N,M})$ であり、**有限段で到達する**(有限群の部分群の下向き有向族)。
2. 任意の $S\subseteq GT(N)$ に対し $\mu(p_N^{-1}(S))=\dfrac{\lvert S\cap GT(N)^{\rm st}\rvert}{\lvert GT(N)^{\rm st}\rvert}$。
3. **閉**部分集合 $C\subseteq\mathcal G$ に対し $\mu(C)=\lim_N\dfrac{\lvert p_N(C)\rvert}{\lvert GT(N)^{\rm st}\rvert}=\inf_N(\cdot)$。
4. ⟹ 生密度は下界: $\liminf_N \dfrac{\lvert p_N(C)\rvert}{\lvert GT(N)\rvert}\ \le\ \mu(C)$。等号は全段全射のときのみ。

**証明.** (1) 像の族は下向き有向で有限集合の部分群列 ⟹ 交わりは達成される。$p_N(\mathcal G)$ が交わりに等しいのは有限集合の逆極限の標準事実。(2) $p_N:\mathcal G\to GT(N)^{\rm st}$ は連続全射準同型 ⟹ Haar の押し出しは有限群上の平行移動不変確率測度 = 一様。(3) $C$ 閉 ⟹ $C=\bigcap_N p_N^{-1}(p_N(C))$($x\notin C$ なら $\{p_N^{-1}(p_N(x))\}$ が $x$ の近傍基ゆえ分離する $N$ が取れる)。clopen の減少有向族に上からの連続性。(4) $p_N(C)\subseteq GT(N)^{\rm st}\subseteq GT(N)$。∎

### 定理 M2(0-1 二分律 — 部分群には測度は情報を持たない)
$C\le\mathcal G$ 閉部分群、$\delta_N:=[GT(N)^{\rm st}:p_N(C)]$ とおく。

1. $K\subseteq N$($N$ が細)なら $\delta_K\mid\delta_N$(**単なる単調でなく整除**)。
2. $[\mathcal G:C]=\sup_N\delta_N$、$\mu(C)=1/\sup_N\delta_N$。
3. $\mu(C)>0\iff C$ 開 $\iff[\mathcal G:C]<\infty$;  $\mu(C)=1\iff C=\mathcal G$。

**証明.** (1) $\phi:=R_{K,N}\!\restriction:GT(N)^{\rm st}\twoheadrightarrow GT(K)^{\rm st}$($E:=\ker\phi$)。$p_K(C)=\phi(p_N(C))$ ゆえ $\delta_K=[GT(N)^{\rm st}:p_N(C)E]$、指数の乗法性より $\delta_K\mid\delta_N$。(2) $\mathcal G/C\to\varprojlim GT(N)^{\rm st}/p_N(C)$ は全単射(単射は $C=\bigcap p_N^{-1}p_N(C)$、全射は有限非空の逆極限)。(3) は (2) と M1(3)。∎

> **系 M2′(粗描の系の正しい形)**。$\overline{\mathrm{Im}(\mathrm{Ih})}$ は $G_{\mathbb Q}$ のコンパクト像ゆえ閉部分群。よって「密度が cofinal に 0 ⟹ 測度ゼロ」は**真だが「指数が無限」と同値**にすぎない。**測度そのものは観測量として貧しい**。情報を持つのは **(a) 欠陥指数列 $\delta_N$ とその整除構造**、**(b) 測度 0 のときの精密化 = Hausdorff 次元**(§4.4)。

### 定理 M3(リフト空間の正準測度)
$K$ を窓、$g\in GT(K)$、$L(g):=\varprojlim_{N}R_{K,N}^{-1}(g)$。

1. $L(g)=p_K^{-1}(g)$。ゆえに $L(g)\neq\emptyset\iff g\in GT(K)^{\rm st}$、かつ $L(g)$ は閉部分群 $\mathcal K_K:=\ker p_K$ の剰余類。
2. ⟹ $L(g)$ 上に **$\mathcal K_K$-不変確率測度 $\nu_g$ が一意に存在**(Haar の平行移動)。しかも $\nu_g=\mu(\,\cdot\mid p_K^{-1}(g))$、$\mu=\frac{1}{\lvert GT(K)^{\rm st}\rvert}\sum_{g}\nu_g$(分解)。
3. 有限段表示: $\nu_g(p_N^{-1}(S))=\lvert S\cap F_N^{\rm st}\rvert/\lvert F_N^{\rm st}\rvert$、$F_N^{\rm st}:=R_{K,N}^{-1}(g)\cap GT(N)^{\rm st}$。

**証明.** (1) 定義から座標ごとに繊維に入ることと同値。(2) コンパクト群 $\mathcal K_K$ の Haar の一意性を平行移動で運ぶ。(3) M1(2) の条件つき版。∎

#### ★ 前件の正しい所在(訂正 C-3 の内容)
$\mathcal G$ が群と分かっていれば M3 は自動である。**有限段の一様測度から組み上げる**場合に必要なのは:

- (2)〔DICHOT (2)〕各非空繊維は $\ker R_{K,N}$ の剰余類 ⟹ $F_M\to F_N$ の繊維は $\ker R_{N,M}$ の剰余類で**サイズ一定**($R_{K,M}=R_{K,N}R_{N,M}$ より $\ker R_{N,M}\subseteq\ker R_{K,M}$)。
- (S)〔段全射〕$F_M\to F_N$ が全射。$R_{N,M}$ 全射ならこれは従う。

**一様測度の族が両立系をなす $\iff$ (2)∧(S)**。(2) 単独では、非全射段があると一様の押し出しが非一様になり**逆極限は存在しない**。前件が破れる場合の正しい扱いは $F_N\rightsquigarrow F_N^{\rm st}$ の置き換えであり、その計算は**有限深度では届かない**(= cofinality の壁そのもの)。⟹ **測度化は壁を消さない。壁の所在を「安定像の未知性」に一点集中させる**。

**観測との接続**: `OBS-UNIF-1`(5 窓・繊維 2,2,2,3,9・非空)は (2) の下では**実質的に (S) の測定**である。(2) を認めれば一様性は定理であり、測定の内容は**非空性 = 全射性**に尽きる。台帳ではそう記帳する。

---

## §3 定理 M6/M7 — 密度の乗法公式と、既存 2 定理の統一

### 定理 M6(窓密度の乗法公式)
入れ子の cofinal 梯子 $M=K_0\supsetneq K_1\supsetneq\cdots$(全て isolated)に対し $I_j:=\mathrm{im}(R_{M,K_j})\le X:=GT(M)$、$\rho_j:=\lvert I_j\rvert/\lvert X\rvert$、$q_j:=[I_{j-1}:I_j]^{-1}$ とおく。$(I_j)$ は減少部分群列で

$$\rho_j=\prod_{i\le j}q_i,\qquad \frac{\lvert X^{\rm st}\rvert}{\lvert X\rvert}=\lim_j\rho_j=\prod_{i\ge1}q_i .$$

算術部分群 $A:=\mathrm{Im}(\mathrm{Ih}_M)$ は全窓に survive するので $A\subseteq I_j\ (\forall j)$、ゆえに **$M$ 窓での安定密度**は

$$\frac{\lvert A\rvert}{\lvert X^{\rm st}\rvert}=\frac{\lvert A\rvert/\lvert X\rvert}{\prod_i q_i}. \tag{M6.1}$$

### 定理 M7(素数指数の二分律 — DICHOT-972 と BIT-252 の統一)
$M$ が isolated、$[X:A]=p$ **素数**とする。$X^{\rm st}=\bigcap_K\mathrm{im}(R_{M,K})$ は $A$ を含む部分群ゆえ、$A\le H\le X$ なる部分群が両端しかないことから

$$X^{\rm st}\in\{A,\ X\},\qquad \frac{\lvert A\rvert}{\lvert X^{\rm st}\rvert}\in\{1,\ 1/p\}\quad(\textbf{中間なし}).$$

同値に、$\prod_i q_i\in\{1/p,1\}$ で**非自明因子は高々 1 個**(単調性/落下高々 1 回)。

**証明.** 上記 2 行。∎(§既存: $p=3$ が DICHOT-972、$p=7$ が BIT-252 = `b4_direct_adjudication_feasibility_v1.md` §4.4 の証明と同一の議論。)

> **★ これが MEAS の中核**。窓の fake/証人ビットは**そのまま Haar 測度の局所因子** $\prod q_i\in\{1/p,1\}$ である。
> $$\mu(\overline{\mathrm{Im}\,\mathrm{Ih}})=\prod_{\text{段}}q_i,\qquad q_i\in\{1,1/p_i\}\ (\text{素数指数窓})$$
> ⟹ **窓水準の井原 $\iff$ 全ビットが 1 $\iff$ 全窓が fake 型**。1 個でも 0 ビットが出れば窓水準で反証(片側)。**このプログラムは構造的に片側**である(反証は有限・肯定は無限深度)。

### 系 MEAS-P1(台帳から出る最初の予言・事前登録可)
生指数は整除を継ぐ(M2(1) の生版: 段全射の下 $[GT(K):\mathrm{Im}_K]\mid[GT(N):\mathrm{Im}_N]$)。既登録は $\delta_{83}=1$、$\delta_{972}=3$、$\delta_{NW(7)}=7$。ゆえに

- $3\nmid7$ かつ $7\nmid3$ ⟹ **972 窓と NW(7) は梯子の中で比較不能**(どちらも他方を細分しない)。
- 両者を同時に細分する isolated 窓 $N$(段全射)が取れれば **$21\mid\delta_N$、生密度 $\le1/21$**。
- 測定がこれに反したら、次のいずれかが偽: (a) その段の全射性(= fake 枝が発動)、(b) $\delta_{972}=3$ の前件(裁定 970 P1–P5)、(c) 両窓の同時細分可能性。**⟹ 3 者を分離する一撃**になる。

---

## §4 証人存在の密度判定式

### 補題 M4(通過集合の閉性)— **前件つき**
proper 条件(pentagon)の残差を $D:\mathcal G\to\widehat W$、$\widehat W=\varprojlim W_j$ 副有限・点を分離、$D$ 連続とすれば
$\mathrm{PENT}=D^{-1}(1)=\bigcap_j D_j^{-1}(1)$ は clopen の減少交叉ゆえ**閉**。

【前件・GAP】B₃-gentle 窓では $D$ は**そもそも関数として存在しない**。`BRUN-DEF`(paper-proof)により欠陥は Brunnian 値 ⟹ **全ての deletion(B₃)窓で 0 ビット**。有限段近似 $D_j$ を持つには **類 4 窓の cofinal 系**が要る(`P-PENT-4`: 必要十分 = 類 4)。**§4 全体はこの器具の存在に相対的**であり、器具が無い現状では §4 は**設計図であって測定ではない**。

### 定理 M5(密度公式・存在・総和判定)
$L(g)$ 内で $V_j:=\bigcap_{i\le j}D_i^{-1}(1)$(clopen 減少)、$\rho_j:=\nu_g(V_j)$、$q_j:=\rho_j/\rho_{j-1}$(条件つき通過率)とすると

$$\nu_g(\mathrm{PENT})=\prod_{j\ge1}q_j,\qquad \nu_g(\mathrm{PENT})>0\iff\sum_j(1-q_j)<\infty .$$

$\nu_g(\mathrm{PENT})>0\Rightarrow\mathrm{PENT}\cap L(g)\neq\emptyset$(**証人存在・構成不要**)。

**★ 訂正 C-2 の精密形**: 存在だけならコンパクト性で足りる —
$$\bigl(\forall j:\ V_j\cap L(g)\neq\emptyset\bigr)\ \Longrightarrow\ \mathrm{PENT}\cap L(g)\neq\emptyset$$
(コンパクト空間の非空閉集合の減少交叉)。**測度 0 でも存在は言える**。測度が追加で買うのは:
(a) **汎用性**: $\nu_g$-ランダムなリフトが確率 $>0$ で証人 ⟹ サンプラ+段判定器があれば有限期待時間で発見;
(b) **外挿の型**: $\forall j$ という無限量化を $\sum(1-q_j)<\infty$ という**総和条件**に替える(有限段データが制約を与えられる形にする — 証明はしない);
(c) **片側反証の座標**: ある段で $V_j\cap L(g)=\emptyset$ が出れば有限で決着(§5 の regime (iii))。

### §4.3 欠陥過程 — 独立性を**仮定しない**枠組み

入れ子の cofinal 梯子上で $X_j:=p_{N_j}\in F_{N_j}^{\rm st}$ とおく。$\nu_g$ は $\mathcal K_K$ 上の Haar の平行移動だから:

> **命題 M5.1(増分の独立性は定理であって仮定ではない)**。$X_{j+1}=X_j\cdot U_j$ と書けば、$U_j$ は $\mathcal K_j/\mathcal K_{j+1}$ 上一様で**互いに独立**。すなわち位置過程は核塔上の**等質**(左不変)ランダムウォークであり、Markov 性・等質性は Haar の積構造そのもの。

**しかし欠陥 $D_j=D_j(X_j)$ は部分積の関数**であって、$j$ を跨いだ独立性は**一般に成り立たない**。ゆえに正しい観測量は条件つき法則

$$q_j=\mathbb E_{\nu_g}\bigl[\ \Pr(D_j=1\mid\mathcal F_{j-1})\ \big|\ V_{j-1}\ \bigr]$$

であり、$M_j:=\mathbf 1[V_j]/\rho_j$ は非負 martingale($\mathbb E M_j=1$)、$\nu_g(\mathrm{PENT})=\lim\rho_j$ は**独立性を一切使わずに** tower property だけから出る。**モデル化が入るのは欠陥関数の繊維上の分布のみ**で、それは有限段で測れる:

| 欠陥の繊維上の挙動 | 帰結 | 対応する既存概念 |
|---|---|---|
| $D_j$ が $X_{j-1}$ を経由(新情報ゼロ) | $q_j=1$、$\nu_g(\mathrm{PENT})=\rho_1>0$ | **RUNG-UNIF / ★三位一体** |
| $D_j$ が各繊維上で群 $\mathcal D_j$ に**等分布** | $q_j=1/\lvert\mathcal D_j\rvert$、$\prod=0$(無限個非自明なら) | 素朴事前分布 |
| 中間: $q_j<1$ かつ $q_j\to1$ 十分速く | $\prod q_j>0$(唯一の非自明な正密度) | 「欠陥が漸近的に決定される」 |

> **★ 三位一体の測度形(定理化)**: 「$q_j\equiv1$(正密度)$\iff$ その不変量に関して梯子が cofinal でない $\iff$ 閉形式は生き残るが何も証明しない」。**素朴事前分布は測度ゼロを予言する** ⟹ regime (i) は先験的には例外であり、正密度の主張は**相関を提示して初めて稼げる**。

### §4.4 測度ゼロのときの精密化(M2′ の救済)— **提案**
$\mu=0$ が一般的なので、真に情報を持つ不変量は filtration 相対の **Hausdorff 次元**

$$\dim_H(C):=\liminf_N\frac{\log\lvert p_N(C)\rvert}{\log\lvert GT(N)^{\rm st}\rvert}\in[0,1]$$

である。**同じ台帳データ(2 列)から即座に計算できる**(§6 に列を追加済み)。井原 $\Rightarrow\dim_H=1$;$\dim_H<1$ は「無限指数」より遥かに強い定量的失敗の言明。⟹ 【文献要請 MEAS-L1】(§7)。

---

## §5 三レジームと既存データの読み

| regime | 判定条件 | 存在の出方 | 測度 |
|---|---|---|---|
| **(i) 正密度** | $\sum_j(1-q_j)<\infty$ | タダ・ランダム探索可 | $>0$ |
| **(ii) 測度 0 かつ非空(正準一意/切断型)** | $\rho_j\to0$ かつ $\forall j\ V_j\neq\emptyset$ | **コンパクト性のみ**。繊維あたり通過数が有界(典型 = 1)で繊維サイズ $\to\infty$ が徴候 | $=0$ |
| **(iii) 有限段で空** | $\exists j:\ V_j\cap L(g)=\emptyset$ | **反証**(証人なし) | $=0$ |

**★ 粗描 (iii)「消滅(結論なし)」の訂正**: 「測度の消滅」は (ii)∪(iii) をまとめてしまい**結論を出さない**。決着を与えるのは「**有限段での集合の空**」であり、それは測度ではなくコンパクト性/悉皆の言明である。⟹ **優先すべき測定は密度ではなく有限段の空判定**。

### 既存データの帰属(解釈・測定ではない)

- **`OBS-UNIF-1`(繊維 2,2,2,3,9)**: witness の証拠ではなく **M3 の前件 (S)(段全射)の検証**。§2 の通り (2) を認めれば内容は非空性のみ。規約どおり観測のみ・昇格しない。
- **`RUNG-UNIF` chain(狙撃 n=1・$I=X$・明示リフト 3 本)**: 第 1 段で $q_1=1$、閉形式が段を貫通 ⟹ **完全相関側**。三位一体により pentagon についての情報量 ≈ 0、DICHOT 枝についての情報量 > 0(落下なし)。
- **$C_M$ 全 fibre(78,732 = 972×81・pass 972・行あたり厳密に 1)**: 形は regime (ii) の徴候(繊維 81・通過 1)。**しかし `BRUN-DEF` により検出力ゼロ**(紙の予言 972/972 と一致)。⟹ 台帳には「**繊維幾何の値**」として登録し、「pentagon 通過密度」としては**登録しない**(`NO_INFORMATION`)。行水準の通過率は $972/972=1$。
- **972 の 1/3**: 生密度。安定列は $\{1,\ 1/3\}$ の 1 ビット(M7)で **UNKNOWN**。
- **NW(7) の 1/7**: 生密度。ただし $\mathfrak G_{\rm ar}=\mathfrak G_{\rm pent}$(42)ゆえ **gap 1 = 1**、7 は gap 2+3 側。安定列は $\{42,294\}$ の 1 ビットで UNKNOWN(= BIT-252)。
- **83 線(48/48・両窓 cross-checked)**: 4 列すべて 48 ⟹ **3 つのギャップ全てが 1**。台帳唯一の無条件行。

> **★ 読み(現時点)**: **測定済みの全窓で gap 1(井原ギャップ)の局所因子は 1** である(83: 1、NW(7): 1、972: 未分解)。非自明な指数 3・7 は**井原ギャップではなく pentagon/fake 側**に立っている。**「井原の反例を窓で捕まえた」データは 1 件もない**。

---

## §6 測度台帳 v0

規約: **生密度** = $\lvert\text{分子}\rvert/\lvert GT(N)\rvert$、**安定密度** = $\lvert\text{分子}\rvert/\lvert GT(N)^{\rm st}\rvert$(= 測度)。$\dim_H$ 寄与は $\log(\text{分子})/\log(\text{分母})$(生版)。

| # | 窓/対象 | 分子 | 分母 | 生比 | 層(どのギャップ) | 安定比 | $\log$ 比 | 格 / 前件 | 出所 |
|---|---|---:|---:|---:|---|---|---:|---|---|
| **D-1** | 83 線 2 窓 `[1152,154161]/[1152,154163]` | 48 | 48 | **1** | gap1=gap2=gap3=1 | **1** | 1.000 | **cross-checked**(無条件行) | `docs/状態.md` 83 線・裁定 1620・C-15 |
| **D-2** | 972 窓 $M$ | $\lvert A\rvert=324$ | $\lvert X\rvert=972$ | **1/3** | gap2+gap3 混在 | **{1, 1/3} の 1 ビット・UNKNOWN** | 0.8403 | `candidate`(裁定 970 P1–P5 相対・P1 発効・isolated・TRIAD-972) | `d972_idx3_..._v1.md` §7/§8 |
| **D-3** | NW(7) | $\mathfrak G_{\rm ar}=42$ | $GT(\mathbf N)=294$ | **1/7** | gap1=1 / 7 は gap2+3 | **{1, 1/7} の 1 ビット・UNKNOWN**(= BIT-252) | 0.6576 | `candidate`(前件: 両窓 isolated・$\lvert GT\rvert=294$・$\lvert\mathfrak G_{\rm ar}\rvert=42$) | `b4_direct_adjudication_feasibility_v1.md` §4.4 |
| **D-4** | NW(7) gap 1 | 42 | $\mathfrak G_{\rm pent}=42$ | **1** | **井原ギャップ** | 1 | 1.000 | `candidate`(同上) | 同上 |
| **D-5** | `OBS-UNIF-1` 5 窓 | 繊維 2,2,2,3,9 | — | $q_1=1$ | M3 前件 (S) | — | — | **cross-checked(観測のみ・昇格禁止)** | `sol_reply_159_iv.md` §15.1 |
| **D-6** | $C_M$ 全 fibre | pass 972 | 78,732 | **1/81** | **繊維幾何**(検出力ゼロ) | — | — | cross-checked だが **`NO_INFORMATION`**(BRUN-DEF) | 同 §12.5 |
| **D-7** | $C_M$ 行水準 | 972 | 972 | **1** | 段通過率(紙予言と一致) | — | — | cross-checked(positive calibration) | 同 §12.5 |
| **D-8** | 狙撃 n=1(972 第 1 段) | $I_{K_1}=X$ | $X$ | $q_1=1$ | 落下なし | — | — | cross-checked | `RUNG-UNIF` §12 |
| **D-9** | ⚠ $\mathrm{gr}_5\otimes\mathbf F_7$ 可解性 | $7^1$ | $7^2$ | **1/7** | **測度でない**(ヒューリスティック事前) | — | — | `heuristic`(登録は警告用) | `bit252_adversarial_reading_v1.md` ③ |

> ⚠ **NAME-COLLIDE 警告**: **D-3 と D-9 はどちらも「1/7」だが完全に別物**(窓密度 vs 線型障害の事前確率)。報告文で「NW(7) の 1/7」と書くときは必ずどちらか明記。
> ⚠ **D-6 を「pentagon 通過密度 1/81」と読むのは誤り**(検出力ゼロ)。

### 次に測るべき **1 量**(指定)

$$\boxed{\ \rho_2\ :=\ \frac{\bigl\lvert\mathrm{im}\bigl(GT(K_2)\to GT(M)\bigr)\bigr\rvert}{972}\ \in\{1,\ 1/3\}\quad(\textbf{入れ子の}\ K_2\subsetneq K_1\subsetneq M)\ }$$

- **なぜこれか**: 既存の密度データは**全部 $q_1$** である(`OBS-UNIF-1` の 5 窓は**非入れ子**ゆえ累積交叉が未測定 — `docs/状態.md` の「$n_0>5$ は型違い」がまさにこれ)。乗法公式 $\prod q_i$ の**内容は $q_2$ から始まる**。器具は既に設計済み(`RUNG-LADDER/v1`・$K_2$ 候補 = index-3 cyclic・raw fibre 48・canary 先行契約)。
- **コスト**: DICHOT-972 の「1 元経済」により、測るのは**$X\setminus A$ の 1 元が $GT(K_2)$ に持ち上がるか**の 1 ビット(悉皆不要)。相互 canary の $[0,f_2]$(row 71)が既に登録済みの座標。
- **出口(事前登録・片側)**: $\rho_2=1/3$ ⟹ 落下発生 ⟹ **972 は fake 型で確定**(M7 の 1 ビットが 1/3 に落ち、648 一括死)。$\rho_2=1$ ⟹ 「深度 2 でも落ちない」だけで**証人型の証明にはならない**(regime (ii)/(iii) 未分離)。この非対称性は §3 の片側性そのもの。
- **副次**: 同じ走行で (P-ISO) の 1 事例($K_2$ isolated)と M2(1) の整除($\delta$ が 3 で割れるか)が確認できる。

---

## §7 正直条項・文献申告・要請

1. **測度ゼロ $\neq$ 空**。負方向は測度では**閉じない**(regime (ii))。空を言うには有限段の悉皆かコンパクト性の破れが要る。
2. **proper 側の密度測定は器具前件つき**: `BRUN-DEF` により B₃-gentle(deletion)窓は pentagon に対して 0 ビット。$q_j$ の測定には**類 4 窓**($P$-PENT-4)が必要で、現状**未取得**。⟹ §4 は測定ではなく設計。
3. **本体の難所は従属性**。増分の独立性は Haar の定理だが(M5.1)、**欠陥の独立性は仮定であり、当工房ではまだ 1 度も測っていない**。$\prod q_j>0$ の主張には**証明された** $q_j$ 下界が要る(フィットは不可)。
4. **(P-ISO) は UNKNOWN**。isolated 窓の cofinal 性が無ければ $\mathcal G$ は群ですらない(groupoid のまま)⟹ Haar が定義できない。**MEAS 全体がこの前件に載る**。
5. **格の非昇格**: 本稿の定理はすべて自前紙証明(未監査)。台帳の各行の格はソースの格を継ぐ(生密度が cross-checked でも安定密度は UNKNOWN)。
6. **novelty 申告(grep 済)**: `Haar|ハール|Hausdorff` を repo 全体に grep — 一致は `scratchpad/ihara_icm1990.txt`(無関係な adele 上の Haar)のみ。**当工房に MEAS 型の先行資産はない**。自前知識としては (a) $G_{\mathbb Q}$ 上の Haar と "almost all $\sigma$" 型定理(Jarden / Fried–Jarden の体算術)、(b) Chebotarev = 有限商上の等分布、(c) 副有限群の Hausdorff 次元(Abercrombie / Barnea–Shalev)、(d) 副有限群の正測度生成(Kantor–Lubotzky, Mann)を**未照合の記憶として**申告する。**$\widehat{GT}$ への測度論の適用例は自前知識にない** — ゆえに現時点の格は `novelty candidate`(未確認)。

### 【文献要請】
- **MEAS-L1**(困難: M2′ により部分群の Haar 測度は 0-1 的で貧しい。測度ゼロの閉部分群を区別する定量的不変量が要る)。**欲しい結果の型**: 副有限群の閉部分群の Hausdorff 次元 — filtration 依存性/独立性の条件、$\dim_H=1$ かつ真部分群の例、$\dim_H$ から指数増大率への定量的帰結。
- **MEAS-L2**(困難: $\prod q_j>0$ を有限段データ+構造から**証明**した実例が要る。フィットでは格が上がらない)。**欲しい結果の型**: 副有限塔上の条件つき通過率の積 / martingale による**存在**判定の既存例(Galois 表現の変形空間、岩澤塔、branching random walk on trees の survival 判定など)。翻訳可能な十分条件の形で。
- **MEAS-L3**(novelty 確認): $\widehat{GT}$ または $\mathrm{Out}(\hat F_2)$ 上の Haar 測度・密度・等分布を扱った先行研究の有無。

### 未決・債務(推測で埋めていない)
- (P-ISO) の放電(= `RUNG-LADDER/v1` の cofinality 保証の証明) — **UNKNOWN**。
- $\mathfrak G_{\rm pent}(N)$ の定義の厳密化(どの窓で $\widehat{GT}$ の像が意味を持つか)— NW(7) では既存、972 では未定義。
- M4 の $\widehat W$(残差の副有限受け皿)の明示 — `BRUN-DEF` の Brunnian 商 + Zassenhaus $D_4^{(p)}$ で作れるはずだが**未構成**。
- D-2/D-3 の $\dim_H$ 値(0.8403 / 0.6576)は**単窓の生比の log** であって、極限としての $\dim_H$ ではない(cofinal 梯子上の $\liminf$ が要る)。**混同禁止**。
