# FAKE-VOID の三層定式化と母集団台帳(v1)

- 起草: 数学者 Opus(2026-08-01)
- 札: **P5-1「FV 三層格上げ」**(発案係第 17 便・裁定 355 採択。P5-2 と同便同梱)
- 前提文書: `docs/地図.md` P5 行・帯 0–3 / `docs/week1-定義ノート.md` §2(正本定義)/ `docs/notes/p52_deathcause_v1.md`(定理 D)
- **格**: §1–§3 は**紙の証明**(定理 FV-EQ・系 FV-SUB は自前・Sol 監査前)。§4 の台帳は**機械生成**(`search/fv-pin.py`)。cross-checked でも verified でもない。
- 機械再現: `python search/fv-pin.py --verify --census`(最終行 `VERDICT: ... ALL PASS`)

---

## 0. スコープ宣言(先に書く)

**(S-1) 封印非接触.** K⁽⁵⁾ blind campaign の封印 3 量($u_9/a_9$・$c$ の平方類・$\hat c_\mu$)に一切触れていない。
K⁽⁵⁾ は §4 で **FV-28(観測欄 = 封印)** として母集団に登録するのみで、値は読んでいない。

**(S-2) EP 非依存.** 本稿の三予想はいずれも **EP(N∞ evidence pipeline)の発効に依存しない**。
- FV-SOLV / FV-WALL は GT-shadow の reduction $R_{K,N}$ の全射性のみで述べられ、検査は既存の GAP/node atlas 機構(EP の外)で完結する。
- FV-N∞ の**編入部**(§3.3)は定理 D であり、その突合器 `search/p52-deathcause-check.py` は工房の lane コードを import しない独立 python である(p52 §7)。
⟹ **EP が uncalibrated/UNKNOWN のままでも本稿の三層は成立し、また崩れない。**

**(S-3) 用途分離.** 本稿は**証拠の会計**であって、新しい正の結果ではない。
とくに「fake witness ゼロ」から genuine 性を導く操作は一切していない(有限深度の PASS から genuine を導かない — 工房の掟 2)。

**(S-4) 新語の申告(CV-9).** **pentagon-fake / arith-fake は正典語ではない**(§1.3 で導入する工房の細分語)。
正典語の **fake**(2401 Def 4.2 の否定)は本稿の **hexagon-fake** に一致する。規約台帳への登録を要請する(§7 要請 1)。

---

## 1. 定義層 — fake の三種公理化

### 1.1 舞台

$\mathcal N:=\mathrm{NFI}_{PB_3}(B_3)$($N\trianglelefteq B_3$, $N\le PB_3$, 有限指数)。
$K\le N$ のとき $R_{K,N}:\mathrm{GT}(K)\to\mathrm{GT}(N)$(定義ノート (3.60))。
$s\in\mathrm{GT}(N)$ が $K$ へ **survive** $\iff s\in\mathrm{Im}(R_{K,N})$。
$\mathrm{GTSh}(N,N)$ = settled shadow のなす**群**(非 isolated な $N$ でも群であることに注意 — 以下の帯の定義はこれを使う)。

$\mathrm{GT}(N)$ の中に**四つの入れ子**を置く:

$$\mathfrak G_{\rm ar}(N)\ \subseteq\ \mathfrak G_{\rm pent}(N)\ \subseteq\ \mathfrak G_{\rm gen}(N)\ \subseteq\ \mathrm{GT}(N)$$

- $\mathfrak G_{\rm gen}(N):=\mathrm{Im}\bigl(\widehat{GT}_{\rm gen}\to\mathrm{GT}(N)\bigr)$ — **genuine**(2401 Def 4.2)。
  **Cor 5.4** により $\mathfrak G_{\rm gen}(N)=\bigcap_{K\le N}\mathrm{Im}(R_{K,N})$。
- $\mathfrak G_{\rm pent}(N):=\mathrm{Im}\bigl(\widehat{GT}\to\mathrm{GT}(N)\bigr)$ — pentagon($\widehat{B_4}$ 内)を担ぐ本来の $\widehat{GT}$ の像。$\widehat{GT}\subseteq\widehat{GT}_{\rm gen}$ ゆえ包含。
- $\mathfrak G_{\rm ar}(N):=\mathrm{Im}(\mathrm{Ih}_N)$、$\mathrm{Ih}_N:G_{\mathbb Q}\to\mathrm{GTSh}(N,N)\subseteq\mathrm{GT}(N)$ — **arithmetical**。$G_{\mathbb Q}\hookrightarrow\widehat{GT}$(Belyi–Drinfeld)ゆえ包含。

この鎖が定義ノート §2 の「arithmetical ⇒ genuine ⇒ charming」の精密形である。

### 1.2 プローブ(観測可能量の正確な形)

> **定義(fake プローブ).** 対 $\mathfrak p=(N,K)$($K\le N$ in $\mathcal N$)を **fake プローブ**という。判定は
> - $\mathbf{VOID}(\mathfrak p)$ $:\iff R_{K,N}$ が全射;
> - $\mathbf{WITNESS}(\mathfrak p)$ $:\iff \mathrm{GT}(N)\setminus\mathrm{Im}(R_{K,N})\ne\emptyset$。このとき差集合の各元は **fake の有限証明書**である。

**非対称性(掟)**: $\mathbf{WITNESS}$ は 1 個の有限計算で確定するが、$\mathbf{VOID}$ は**深さ 1 の情報しか持たない** — 全 $K$ にわたる無限個の $\mathfrak p$ が $\mathbf{VOID}$ で初めて genuine が言える。
**⟹ 我々の哨戒データの内容は、有限個の $\mathfrak p$ についての $\mathbf{VOID}$ のみである。** §4 の台帳はこの一文を機械的に実体化したものである。

### 1.3 三種の fake

> **定義(fake の三分).** $s\in\mathrm{GT}(N)$ が **non-arithmetical** であるとき、次のちょうど一つが起きる:
> | 種別 | 定義 | 障害の所在 |
> |---|---|---|
> | **hexagon-fake**(= 正典語の *fake*) | $s\in\mathrm{GT}(N)\setminus\mathfrak G_{\rm gen}(N)$ | 有限段では hexagon (3.3)(3.4) を満たすが、**塔全体で整合的に持ち上がらない** |
> | **pentagon-fake**(工房語) | $s\in\mathfrak G_{\rm gen}(N)\setminus\mathfrak G_{\rm pent}(N)$ | gentle 塔は登れるが **pentagon** が塞ぐ |
> | **arith-fake**(工房語) | $s\in\mathfrak G_{\rm pent}(N)\setminus\mathfrak G_{\rm ar}(N)$ | $\widehat{GT}$ には居るが **$G_{\mathbb Q}$ の像でない** |

種別名の根拠: $\widehat{GT}_{\rm gen}$ が charming に課す追加条件は hexagon の塔整合性のみ、$\widehat{GT}$ が $\widehat{GT}_{\rm gen}$ に課す追加条件は pentagon のみ、$G_{\mathbb Q}\to\widehat{GT}$ の欠落は算術のみ。**障害は三つの定義関係に一対一で局在する。**

### 1.4 定理 FV-EQ — 三層の値段

> **定理 FV-EQ.** $\mathcal N^0\subseteq\mathcal N$ を isolated 対象からなる cofinal 部分 poset とする(Prop 3.14 で存在)。
> **(a)** $\mathcal N^0$ 上に hexagon-fake が無い $\iff$ すべての $N\in\mathcal N^0$ で $\widehat{GT}_{\rm gen}\twoheadrightarrow\mathrm{GT}(N)$。
> **(b)** $\mathcal N^0$ 上に pentagon-fake が無い $\iff \widehat{GT}=\widehat{GT}_{\rm gen}$。
> **(c)** $\mathcal N^0$ 上に arith-fake が無い $\iff \mathrm{Ih}:G_{\mathbb Q}\to\widehat{GT}$ が全射 $\iff$(Belyi 単射と併せて)**井原予想**。
> **(d)** (a)∧(b)∧(c) $\iff$ すべての $N\in\mathcal N^0$ で $\mathrm{Ih}_N:G_{\mathbb Q}\to\mathrm{GT}(N)$ が全射。

**証明.** (a) は $\mathfrak G_{\rm gen}$ の定義そのもの。
(b)(c) は共通の一行に帰する: **副有限群 $P=\varprojlim P_N$ の閉部分群 $H$ は、各 $P_N$ における像から復元される**($\ker(P\to P_N)$ が $1$ の基本近傍系をなすので $H=\bigcap_N\pi_N^{-1}(\pi_N H)$、$H$ 閉より等号)。
(b): Thm 5.2 で $\widehat{GT}_{\rm gen}\cong\varprojlim_{\mathcal N^0}\mathrm{GT}(N)$。$\widehat{GT}$ はその閉部分群だから、$\forall N:\mathfrak G_{\rm pent}(N)=\mathfrak G_{\rm gen}(N)\Rightarrow\widehat{GT}=\widehat{GT}_{\rm gen}$。逆は自明。
(c): $G_{\mathbb Q}$ はコンパクト・$\mathrm{Ih}$ は連続ゆえ $\mathrm{Im}(\mathrm{Ih})$ は $\widehat{GT}$ の閉部分群。同じ一行。
(d): $\mathfrak G_{\rm ar}(N)=\mathrm{GT}(N)$ $\iff$ 鎖 §1.1 の三つの包含がすべて等号。∎

**帰結(これが本稿の中心的な帰結である).**
> **系 FV-COST.** 「全 $\mathcal N^0$ で fake が存在しない(三層とも)」は **井原予想 $\wedge$($\widehat{GT}=\widehat{GT}_{\rm gen}$)と同値**であり、後者は定義ノート §2 が明記する**未解決問題**である。

⟹ **FAKE-VOID を母集団無指定で述べることは、夢(P6)の言い換えにすぎない。**
予想として意味を持たせるには母集団を切らねばならない — これが三層に分ける第一の理由であり、
「fake witness ゼロ」を無条件に唱えることが禁じられる数学的理由でもある。

### 1.5 系 FV-SUB — 定理から従うプローブは独立証拠でない

> **系 FV-SUB.** $N$ について $\mathfrak G_{\rm ar}(N)=\mathrm{GT}(N)$(= 全 shadow が arithmetical)が成り立つなら、
> **すべての** $K\le N$ について $\mathfrak p=(N,K)$ は $\mathbf{VOID}$ である。

**証明.** arithmetical ⇒ genuine ⇒(Cor 5.4)全細分に survive。∎

これは会計上決定的である。工房が持つ
**定理 K3**(`W3-11`: $\mathrm{Ih}_{K^{(3)}}\twoheadrightarrow\mathrm{GT}(K^{(3)})$)・
**定理 A₅**(`W3-8`: $\mathrm{Ih}_{N_A}\twoheadrightarrow\mathrm{GT}(N_A)\cong F_{20}$、(I1)(I2) 下)・
**2405 Thm 5.3**($K^{(2^\alpha)}$、公刊)
のいずれかで覆われる底窓のプローブは、**定理の系であって独立証拠ではない**。
p52 §7.4 が 744 の reason vector に対して行った降格と**同型の操作**を、ここでは哨戒データ全体に対して行う。

---

## 2. 帯の定義(母集団の切り方)

> **定義.** $\mathcal D:=\{N\in\mathcal N\mid \mathrm{GTSh}(N,N)\ \text{可解}\}$(**可解帯**)、$\mathcal W:=\mathcal N\setminus\mathcal D$(**壁帯**)。

- 判定は有限群の可解性判定なので**決定可能**。$\mathrm{GTSh}(N,N)$ は $N$ が isolated でなくても群なので $\mathcal N$ 全体で well-defined。
- **「D 型」の意味**: 現在 $\mathcal D$ 側で観測済みの $\mathrm{GTSh}$ はすべて **affine/holomorph 型**である —
  $\mathrm{Aff}(\mathbb Z/n_0)\times\mathcal Z_2$(dihedral・Thm 4.6)、$F_{20}=\mathrm{AGL}(1,5)$($A_5$ 窓)、
  $\mathrm{Hol}(\mathbb Z/k)$・$D_{4k}$(PSL 7 窓・W3-7)、$\mathrm{Syl}_2(S_t)\times\mathrm{Hol}(\mathbb Z/N_{\rm ord})$(梯子)。
  帯の名 "D 型" はこの経験的形状を指す(**予想 P3 の主張であって定義ではない** — 定義は可解性一本)。
- **注意**: $\mathcal D$ は細分で閉じない(閉じるかどうか自体 UNKNOWN)。三予想はいずれも**細分側を制限しない**強い形で述べる。

### 2.1 訂正 — 「壁族 6 窓」のうち $\mathcal W$ に入るのは 4 窓(裁定 373 ①で受理)

C-WALL-FAM は $\ker\tilde\chi\cong C_\ell\times S_t$ という**形**で括られた 6 窓だが、$S_3,S_4$ は可解である。
cert 自身の欄がそう言っている(`python search/fv-pin.py --bands`):

```
# window	cert	solvable	derived_length	band
n=24	search/certs/wall2_cert_20260731.json	false	-	W(non-solvable)
n=28	search/certs/wall28_cert_20260731.json	false	-1	W(non-solvable)
n=36	search/certs/wall36_cert_20260731_r2.json	false	-1	W(non-solvable)
n=37	search/certs/wall37_cert_20260731_r2.json	false	-1	W(non-solvable)
n=40	search/certs/wall40_cert_20260801.json	true	2	D(solvable)
n=45	search/certs/wall45_cert_20260801.json	true	3	D(solvable)
n=21 (T5-dl3)	search/certs/dl3_cert_20260731.json	true	3	D(solvable)
n=18 (W-CENT-B)	search/certs/centb_cert_20260731.json	true	-	D(solvable)

# BAND_W_COUNT=4 BAND_D_COUNT=4
```

> **$\mathcal W$ の既知元 = 4 窓** $n\in\{24,28,36,37\}$($\ker\tilde\chi\cong C_{19}\times S_5,\ C_{23}\times S_5,\ C_{31}\times S_5,\ C_{31}\times S_6$)。
> **$n=40$($C_{37}\times S_3$・dl 2)と $n=45$($C_{41}\times S_4$・dl 3)は $\mathcal D$ の元である。**

数値も cert も無傷で、訂正は**分類語のみ**(裁定 339 の「6 窓」呼称の伝播)。
**副産物**: $n=40$($\lvert C(w_0)\rvert=222$)と $n=45$($984$)は「**小さい・可解・fake データ 0**」— FV-SOLV の
**最安の新規プローブ標的**である(§3.1 候補標的欄)。実走の起票は司令塔採否。

---

## 3. 三層の予想文(Sol ゲート便様式)

### 3.1 FV-SOLV(**予想へ格上げ**)

> **予想 FV-SOLV.**
> $$\forall N\in\mathcal D,\ \forall K\in\mathcal N\ (K\le N),\ \forall s\in\mathrm{GT}(N):\quad s\in\mathrm{Im}(R_{K,N}).$$
> 同値形(Cor 5.4): $\forall N\in\mathcal D$ の全 GT-shadow が **genuine**。すなわち $\mathcal D$ 上に **hexagon-fake は存在しない**。

- **層**: (a) のみ。**(b)(c) は主張しない**(主張すれば系 FV-COST により未解決問題と井原予想を含んでしまう)。
- **量化子(negative-claim レジーム・裁定 156 系)**: $N$ は $\mathcal D$ 全体を走り、$K$ は $\mathcal N$ 全体を走る。
  「存在しない」と言っている対象は **hexagon-fake だけ**であり、pentagon-fake・arith-fake については何も言わない。
- **反証条件**: 三つ組 $(N,K,s)$、$N\in\mathcal D$、$K\le N$、$s\in\mathrm{GT}(N)\setminus\mathrm{Im}(R_{K,N})$。
  $\mathrm{GT}(N),\mathrm{GT}(K)$ は有限で $R$ は明示式ゆえ、**反証は 1 個の有限計算**。
- **現在の証拠(§4 が正本)**: 独立プローブ **7 本 / 底窓 5 個**($N_Q$:3・$N_2$:1・$N_3$:1・$N_5$:1・$K^{(12)}$:1)+
  定理級閉鎖 **3 窓族**($K^{(3)}$・$N_A$・$K^{(2^\alpha)}$)。残り 10 プローブは系 FV-SUB により spot-check。
- **弱形(実測そのもの・別札)**: **FV-SOLV⁻** := 上式の $K$ を「§4 の台帳が記録した $K$」に制限したもの。
  **FV-SOLV⁻ は観測、FV-SOLV は賭けである。** 混同禁止。
- **候補標的(最安・裁定 373 ①の副産物)**: $\mathcal D$ の元でありながら fake データ 0 の**小さい**窓 —
  **$n=40$**($\ker\tilde\chi\cong C_{37}\times S_3$・222 元・dl 2)・**$n=45$**($C_{41}\times S_4$・984 元・dl 3)・
  **$n=21$**(T5-dl3・$C_{17}\times S_4$・408 元・dl 3)・**$n=18$**(W-CENT-B・$C_9\times D_{18}$・162 元)。
  いずれも SURV 悉皆済みで窓の実物と生成対が手元にあるため、細分を 1 本足すだけで FV プローブになる。
  **dl 2 と dl 3 の両方が揃っている**のが利点 — FV-SOLV が導来長に依存するかを $\mathcal D$ の内部で測れる。
- **監査依頼(Sol)**: ①$\mathcal D$ の定義($\mathrm{GTSh}(N,N)$ の可解性)が量化子として適切か、
  ②細分側を無制限にする強形が過大でないか(制限形の提案があれば)、③系 FV-COST の証明。

### 3.2 FV-WALL(**予想にしない** — 第一照準として分離登録)

> **登録 FV-WALL(照準・予想ではない).**
> $\mathcal W$(既知元 = **4 窓** $n\in\{24,28,36,37\}$・§2.1)上の fake プローブ実行数は **0 本**である
> (§4.3 の悉皆 census が機械的根拠)。
> よって工房は $\mathcal W$ について **FAKE-VOID を主張しない・予想しない・UNKNOWN とする**。

**予想にしない三つの理由(明示的に記録する):**
- **(W1) データ 0**: $\mathcal W$ の元が 4 個判明しているのに、そのいずれについても $R_{K,N}$ を一度も計算していない。
  構造測定($\ker\tilde\chi\cong C_\ell\times S_t$・SURV 悉皆)は fake について**何も言わない** — settled も $\ker\tilde\chi$ も survive とは別の述語である。
- **(W2) 証明機構が届かない**: $\mathcal D$ 側の唯一の正の機構は **算術飽和**(定理 K3・A₅・R^cyc_formal 系)であり、
  その前件は Kummer 理論 + $\mathrm{GTSh}$ の affine 型構造に依存する。$\mathcal W$ では $\mathrm{GTSh}$ が非可解ゆえ **前件が成立しない**。
- **(W3) 外挿の基礎がない**: $\mathcal D$ 側の全観測が affine 型窓から来ている。$\mathcal W$ への外挿は形状の外挿であり、根拠ゼロ。

**第一照準(設計).** 壁窓 $N$($n=24$、$w_0=(19,1^5)$、$\ker\tilde\chi\cong C_{19}\times S_5$)に対し、
$K^{(3)}$ で成功した**二方向**をそのまま移植する:
- **L 型**(中心方向): $K=N\cap N_0$、$N_0$ = Heisenberg $H_3$(位数 27)窓 — 中心 torsor 方向の持ち上げ。
- **M₅ 型**(円分方向): $K=N\cap N_q$、$N_q$ = 巡回 control($q$ 素数・$q\nmid N_{\rm ord}$)— 円分方向の持ち上げ。
理由: $K^{(3)}$ の最初の 2 プローブがこの 2 方向であり(FV-05)、**同じ設計を可解側と壁側で走らせれば比較が apples-to-apples になる**。
費用見積は本稿の射程外(implementer 委嘱の対象)。**UNKNOWN の申告**: 私はこのプローブの結果を予言しない — 予言する根拠を持たないことが、まさにこれを第一照準にする理由である。

### 3.3 FV-N∞(**UNKNOWN 隔離**+定理 D による部分編入)

> **登録 FV-N∞.** N∞ 枝(K⁽⁵⁾ campaign の model-builder 副枝)は **schema ごと隔離・UNKNOWN**。本稿はこれを解除しない。
> 編入するのは次の 2 行だけである:
>
> **編入 N∞-1(gauge-free).** 定理 D(p52 §5): $B\le4$ のとき事前登録宇宙 $\mathcal U_B$ の stage 1 生存者は**全点** $\mathrm{rootpart}(a)\ne[2,2,1]$。
> ゆえに **$B\le4$ の整数箱には decision lane を通る対象が 1 点も存在しない**。これは**定理**(重心恒等式 $4A_4=5(P_1+Q_1)$ と Gauss から $5\mid a_4$)であって、空振りの記録ではない。
> **編入 N∞-2(gauge 相対).** 定理 D+: searcher の正規形(depressed)では $B\le24$ まで空で、$B^*=25$ は**鋭い**。
>
> **非編入(明示して残す).** 命題 MIN0: depressed を課さなければ **$B=5$ で既に 6 点実在する**。
> ⟹ 帯の空虚性は **探索格子(整数 ∧ depressed ∧ 小箱)の性質**であって、枝そのものの空虚性ではない。
> **したがって定理 D は「N∞ 枝は空」を許さず、$K^{(5)}$ の層 (c) を 1 ミリも動かさない。**

- **層**: N∞ は $K^{(5)}$ の **arith 層 (c)** に(bridge predicate 経由で)しか接続していない。層 (a)(b) には無関係。
- **重みの会計(重要)**: 系 D′ と p52 §7.4 により、$86{,}410{,}020$ 点は相異なる $(a,p)$ **456** → $V$-軌道 **114 個**に潰れ、
  bound=5 を足しても $+170$ 個。**しかもこの 284 個は GT-shadow のプローブではない。**
  ⟹ **N∞ データの FAKE-VOID への寄与は $0$ である。** 地図 P5 行が「全観測で witness ゼロ」と束ねるとき、この 0 を大きな数と一緒に置いてはならない。
- **EP 非依存の確認**: 編入 2 行はいずれも紙の定理であり、EP の発効・較正・positive control のいずれも前件にしない。

**retraction との関係(裁定 373 ②の限定解除を適用).**
定理 D の実測突合が使う bound 3/4/5 の cert 群は `schema mb/ninfty-branch-search/v1` に属し、
`certificates/mb/actions/30289323147/RETRACTED_AS_CANDIDATE.md`(裁定 66・便 54 Part B)で
「候補としての引用・救済・照合器入力を禁止」とされた資産である。裁定 373 ② が範囲を明示した:

> **点リスト(座標データ)を事前登録宇宙の定義として使うことは可。禁止が継続するのは
> verdict / hit / 判定欄を証拠または照合器の判定入力として使うこと。**

**⟹ 本稿 FV-25/26/27 は「点リストのみ使用・verdict 不使用」で運用する**(CV-10 連鎖に添える 1 行)。
具体的には: 744 点と bound=5 の stage 1 生存 680 点は**座標として**再走査の入力であり、
retracted な stage 2 hit(8 件)の判定欄は証拠として使っていない — むしろ定理 D+ がそれを独立に否定している。

---

## 4. 母集団台帳(行ごとに格を明示 — 一括表示禁止)

> **F96 の教訓の適用**(便 96 F96-1.6:「`unconditional` という語は絶対無条件ではない … と書くのが正確である」):
> **束ねた札を一つ貼らない。** 以下の各行は独立に格を持ち、行をまたいだ格の継承はしない。

### 4.1 表 1 — 母集団台帳(31 行)

pin 列は §4.3 の機械出力の行 ID を指す。**値は本文に手写ししていない**(machine-piped 規律)。

| 行 | 窓族(母集団の要素) | 関門(何を検査したか) | pin | 格(この行だけの) | 効く層 |
|---|---|---|---|---|---|
| **FV-01** | $K^{(3)}=K^{(6)}$ | 算術飽和: 全 12 元 arithmetical | A-1, A-1d | **paper-proof / two-mathematician audit PASS**(定理 K3・W3-11)。有限層 $\alpha$ は **Lean verified**(W3-14/14b/14c/14d)、**算術層は verified でない** | **(a)(b)(c) 全閉** |
| **FV-02** | $N_A$($A_5$ 窓) | 算術飽和: 全 20 元 arithmetical | A-2, A-2d | **paper-proof / two-mathematician audit PASS**(定理 A₅・W3-8)**・(I1)(I2) 条件付き** | **(a)(b)(c) 全閉(条件付き)** |
| **FV-03** | $K^{(2^\alpha)}$, $\alpha\ge2$ | 2405 Thm 5.3(公刊) | A-3a/b/c | **文献依拠**。我々の cert は Thm 4.3 との列挙一致(較正)のみで、arithmeticity の cert ではない | **(a)(b)(c) 全閉(文献)** |
| **FV-04** | $N_A$(**$PB_3$ 実装模型水準**) | pentagon lift: `red: GT(K_π)→GT(N_A)` が同型・繊維濃度 $\kappa=1$・20/20 | D-0, D-1 | **紙の証明 + 単系統 GAP**(定理 GTPI)。**$PB_3$ 模型水準** — $PB_4$ 水準の主張ではない。**監査点 A($c_4$ の模型忠実性)に全体重・UNKNOWN**。CV-9 主検問は 400/400 通過(裁定 364)だが正典忠実性は便 98 待ち | **(b) の初データ** |
| **FV-05** | $K^{(3)}\leftarrow\{L,\ M_5,\ M_3,\ 1b,\ K^{(9)},\ K^{(18)}\}$(6 プローブ) | $R$ 全射 12/12 | census | **cross-checked**。ただし**系 FV-SUB により定理 K3 の系** ⟹ **独立証拠でなく spot-check** | (a)・独立性なし |
| **FV-06** | $K^{(4)}\leftarrow\{K^{(8)},K^{(12)},K^{(36)}\}$(3 プローブ) | $R$ 全射 4/4 | census | **cross-checked**。**2405 Thm 5.3 の系** ⟹ spot-check | (a)・独立性なし |
| **FV-07** | $N_A\leftarrow M_{A,5}$(1 プローブ) | 全単射 20/20(繊維 1) | census | **cross-checked**。**定理 A₅ の系** ⟹ spot-check | (a)・独立性なし |
| **FV-08** | $N_Q$($Q_8$ 窓)$\leftarrow\{1b,2a,2b\}$(3 プローブ) | $R$ 全射 4/4 | census | **cross-checked** | **(a)・独立** |
| **FV-09** | $N_2\leftarrow 2b$(1 プローブ) | $R$ 全射 4/4 | census | **cross-checked** | **(a)・独立** |
| **FV-10** | $N_3\leftarrow M_3$(1 プローブ) | $R$ 全射 8/8(核位数 6) | census | **cross-checked** | **(a)・独立** |
| **FV-11** | $N_5$(**$c\ne1$ control**)$\leftarrow M_{A,5}$(1 プローブ) | $R$ 全射 4/4(核位数 5) | census | **cross-checked**。中心項 $c$ が生きる唯一のプローブ行 | **(a)・独立** |
| **FV-12** | $K^{(12)}\leftarrow K^{(36)}$(1 プローブ) | $R$ 全射 24/24 | census | **cross-checked**。系 MIX-12(candidate)が採択されれば FV-SUB で spot-check へ降格する | **(a)・独立**(現時点) |
| **FV-13** | class-6 $j=2$($m=0..63$) | 中心障害 $\mathrm{ob}$ の像 $\subseteq\{(0,0),(0,1)\}$ ⟹ fake 候補 0 | C-1(40 系) | candidate(三経路独立収束・裁定 21)。**実現ギャップ開**: 事前登録 manifest が「$\mathrm{ob}\ne0$ でも実現+charming なしに反例でない」と明記 ⟹ **対偶として $\mathrm{ob}=0$ も窓上の $\mathbf{VOID}$ を意味しない** | **機構層**(窓プローブではない) |
| **FV-14** | class-6 $j=3$($m=0..63$) | 線型可解 20/64・全 20 系で $\mathrm{ob}=0$(重複度正) | C-2(96 ファイル) | 数値部 **cross-checked**(裁定 23)。**実現ギャップ開**(同上) | **機構層** |
| **FV-14b** | $J=L\cap M_5$($K^{(3)}$ の第 3 細分・gluing obstruction 関門) | — | **該当 cert 未発見** | **未実行**。設計 2 版(`docs/week3-J設計_v{1,2}`)と**封印予測**($\lvert\mathrm{GT}(J)\rvert=144$・$\Phi$ 全単射 ⟹ 障害自明・封印 sha は LEDGER 2026-07-25 項)は在るが、便 05 ゲートで止まったまま走っていない。開封済み封印は PSL のみ | **潜在プローブ 1 本**(未走) |
| **FV-15** | **W-A 帯 66 窓**(指数 $\le192$) | `windows_processed:66`・`nonabelian_count:0`・単一 LINS・canonical 語 ID | F-1(封緘正本)・F-1b(probe) | **構造測定**・裁定 167/172 が **lead 水準**と明記(悉皆主張ではない) | **fake プローブ 0 本** |
| **FV-16** | 指数 $(192,360]$ の **67 窓** | 非可換核 0(裁定 225) | F-2 | **構造測定**。**cert が JSON パース不能**(judge の `compression:1.` バグ・裁定 225 が既知として非改変を裁定)⟹ 機械監査は sha256 pin までしかできない | **0 本** + 要修理 |
| **FV-17** | 梯子 **13 窓 + 兄弟 9 窓**($N_{\rm ord}=9$) | Cyc 律・Tail 律・$\lvert\ker\tilde\chi\rvert$ | F-3 | **構造測定**(prediction-first 17/17 は的中の記録であって survive の記録ではない) | **0 本** |
| **FV-18** | **PSL 7 窓** S1–S7 | $\lvert\mathrm{GT}\rvert$・settled 率(case B は半分) | F-4 | **構造測定**。**settled $\ne$ survive** — 非 isolated の観測は fake について何も言わない | **0 本** |
| **FV-19** | **帯 $\mathcal W$** 窓 $n=24$($w_0=(19,1^5)$) | $\ker\tilde\chi\cong C_{19}\times S_5$・SURV 悉皆 2280/2280・cert `solvable:false` | E-1 | 構造測定 **cross-checked** | **0 本 = FV-WALL 第一照準** |
| **FV-20** | 帯 $\mathcal W$ 窓 $n=28$ | $C_{23}\times S_5$・2760 悉皆・`solvable:false` | E-2 | 構造測定 cross-checked(二環境) | **0 本** |
| **FV-21** | 帯 $\mathcal W$ 窓 $n=36$ | $C_{31}\times S_5$・3720 悉皆・`solvable:false` | E-3 | 構造測定 cross-checked | **0 本** |
| **FV-22** | 帯 $\mathcal W$ 窓 $n=37$ | $C_{31}\times S_6$・22320 悉皆・`solvable:false`(初の $S_6$ 型) | E-4 | 構造測定 cross-checked | **0 本** |
| **FV-23** | **帯 $\mathcal D$** 窓 $n=40$(族名は「壁」だが可解) | $C_{37}\times S_3$・222 悉皆・**`solvable:true`, dl 2** | S-1 | 構造測定 cross-checked。**§2.1 の訂正対象** | **0 本**・FV-SOLV 候補標的(最安) |
| **FV-24** | 帯 $\mathcal D$ 窓 $n=45$(同上) | $C_{41}\times S_4$・984 悉皆・**`solvable:true`, dl 3** | S-2 | 構造測定 cross-checked。**§2.1 の訂正対象** | **0 本**・FV-SOLV 候補標的 |
| **FV-24b** | 帯 $\mathcal D$ 窓 $n=21$(T5-dl3) | $C_{17}\times S_4$・408 悉皆・`solvable:true`, dl 3 | S-3 | 構造測定 cross-checked | **0 本**・FV-SOLV 候補標的 |
| **FV-24c** | 帯 $\mathcal D$ 窓 $n=18$(W-CENT-B) | $C_9\times D_{18}$・162 悉皆・`solvable:true` | S-4 | 構造測定 cross-checked | **0 本**・FV-SOLV 候補標的(最小) |
| **FV-25** | N∞ $\mathcal U_3\cup\mathcal U_4$(86,410,020 走査・stage1 生存 744) | decision lane 全点 REJECT・二環境一致 | G-1 | **cross-checked**(二環境・裁定 342)。定理 D により **spot-check へ降格**(p52 §7.4)。cert 自身が `complete_search:false`・`calibrated_detector:false`・`EXPLICIT_NON_DECLARATIONS`(「fake は存在しない等の結論を宣言しない」)を持つ。**点リストのみ使用・verdict 不使用**(裁定 373 ②) | **fake 層への寄与 = 0**(GT-shadow プローブではない) |
| **FV-26** | N∞ bound=5(389,743,420 走査・stage1 生存 680) | $\mathrm{rootpart}(a)=[2,2,1]$ が 0 件 | G-2(40 ファイル) | **単系統**・out-of-sample。schema は RETRACTED — **点リストのみ使用・verdict 不使用**(裁定 373 ②)。stage 2 hit 8 件の判定欄は証拠に使わない | **寄与 = 0** |
| **FV-27** | 定理 D / D+ / MIN / MIN0 | $B\le4$ 空(gauge-free)/ $B\le24$ 空(depressed・鋭い)/ $B^*=25$ / gauge-free $B=5$ に 6 点 | G-3・**G-3a(追記 A)** | **紙 + python 単系統**・**Sol 監査前**。引用時は追記 A(`p52_deathcause_v1_addendum_novelty.md`)を effective source に併記 — §7.3 の新規性帰属と用法注記が更新されている(裁定 373 ②③) | **FV-N∞ の編入部**(§3.3) |
| **FV-28** | $K^{(5)}$ 系 | — | — | **blind campaign・立入禁止**。本稿は値を一切読んでいない | 母集団に属するが**観測欄は封印** |

### 4.2 会計の要約(表 1 から機械的に読める形)

- **層 (a) を動かした行**: FV-01/02/03(定理)+ FV-05〜FV-12(プローブ 17 本)。
- **そのうち独立**: FV-08〜FV-12 の **7 プローブ / 底窓 5 個**。残り 10 プローブは系 FV-SUB で spot-check。
- **層 (b) を動かした行**: FV-04 **ただ 1 行**(しかも $PB_3$ 模型水準)。
- **層 (c) を動かした行**: FV-01/02/03 のみ($K^{(3)}$・$N_A$・2 冪)。
- **fake データ 0 の窓**: FV-15〜FV-24c — W-A 66・(192,360] 67・梯子 13+9・PSL 7・帯 $\mathcal W$ 4・帯 $\mathcal D$ の族窓 4。
  **合計は取らない**: canonical UID による窓の重複判定を経ていないため(§6 要 cert 化 4)。
- **未走の潜在プローブ**: FV-14b($J=L\cap M_5$)— 封印予測つきで設計済み、走れば $K^{(3)}$ の 7 本目のプローブになる
  (ただし系 FV-SUB により、定理 K3 が正しければ結果は $\mathbf{VOID}$ が確定しているので、
  **新しい証拠ではなく K3 のトリップワイヤ**として位置づけるのが正しい — P-FV-1)。
- **観測 = 「17 プローブ・底窓 8 個・すべて $\mathbf{VOID}$」。** これが地図 P5 行「全観測で witness ゼロ」の実体である。

### 4.3 pin と検証コマンド(machine-piped)

```
python search/fv-pin.py --verify --census --bands
```

生成器 = `search/fv-pin.py`。
`--verify` は表 1 の pin 実在 + sha256 と 9 本のプローブ述語(`surjective`/`image_size`)を再検査、
`--census` は **cert 樹全体を悉皆走査して reduction プローブを列挙**する(= FV-15〜FV-24c の「0 本」の機械的根拠。
census に現れない窓は、定義により fake プローブを 1 本も持たない)、
`--bands` は C-WALL-FAM 各窓を cert の `solvable` 欄で $\mathcal D/\mathcal W$ に振り分ける(§2.1 の根拠)。

**本器が主張すること/しないこと(明記)**: 本器は「fake witness ゼロ」を主張しない。
主張するのは「pin した cert が実在し、その reduction 欄が `surjective=true` である」だけ。
その帰結が**どの層のどの量化子に効くか**は表 1 の格欄の責任である。

機械出力(2026-08-01・本稿起草時)の要約行:

```
# PROBE_ENTRIES=17 DISTINCT_BASE_WINDOWS=8 UNPARSABLE_JSON=4
# BY_BASE_WINDOW={'K12': 1, 'K3': 6, 'K4': 3, 'N2': 1, 'N3': 1, 'N5': 1, 'N_A': 1, 'N_Q': 3}
# ALL_SURJECTIVE=True
# BAND_W_COUNT=4 BAND_D_COUNT=4
VERDICT: pins_missing=0 failures=0 ALL PASS
```

**「fake_witness」という欄はどの cert にも存在しない**(用語としては散文にのみ現れる)。
機械可読の代理量は行ごとに別物である — `surjective`+`image_size`(細分プローブ)/ `m_missing:[]`(バッテリー・PSL)/
`nonabelian_count:0`(W-A 帯)/ `pass_count == Cv_size` + `hexagon_fail_count:0`(帯 $\mathcal W/\mathcal D$ の族窓)/
`26_eq_27:true` + `settled_fail_count:0`(梯子)。
**このうち fake 層に効くのは第一のものだけ**である — 残りは §1.2 のプローブ判定を計算していない。
これが表 1 で「0 本」と書いた行の実体であり、代理量の見かけの豊富さに騙されないための注記である。

`UNPARSABLE_JSON=4` は既知の judge バグ(`"compression":1.` — JSON では不正)を持つ 4 cert:
`search/certs/{wall_census_192_360_20260730, kerchi_judge_selftest_p5, kerchi_judge_selftest_cinN_control, strike_a20_full_20260729}.json`。
うち 1 本目は **FV-16 の正本 cert** である(§6 要 cert 化 2)。

---

## 5. 事前登録した予言(反証可能・コード外)

- **P-FV-1(トリップワイヤ・定理 K3 から導出)**: 今後 $K^{(3)}$ の**どの**細分 $K$ にプローブを打っても $\mathbf{VOID}$ が返る。
  1 本でも $\mathbf{WITNESS}$ が返れば **定理 K3 は偽**(系 FV-SUB の対偶)。同様に $N_A$ については (I1)(I2) 込みで定理 A₅ が、$K^{(2^\alpha)}$ については 2405 Thm 5.3 が倒れる。
- **P-FV-2(系 MIX-12 のトリップワイヤ)**: $K^{(12)}$ の新規プローブは $\mathbf{VOID}$。$\mathbf{WITNESS}$ なら系 MIX-12(candidate)が倒れる。
- **P-FV-3(異常主張の門・定理 FV-EQ(b) から)**: いかなる窓でも **pentagon-fake を 1 個示せば $\widehat{GT}\subsetneq\widehat{GT}_{\rm gen}$ が証明される** — 定義ノート §2 が未解決と書く問題の解決である。
  ⟹ **pentagon-fake の主張は例外なく異常主張として扱い、Sol 監査と(可能なら)Lean を通す前に台帳へ書かない。**
- **P-FV-4(FV-04 の忠実性 1 ビット)**: 定理 A₅((I1)(I2) 下)は $N_A$ で層 (b) が閉じることを**予言する**。
  GTPI の $\kappa=1$ 観測は $PB_3$ 模型水準でこれと**一致した**。両者は独立(片方は算術・片方は模型計算)なので、この一致は **監査点 A($c_4$ の模型忠実性)の 1 ビットの弱いテストに合格した**ことを意味する。
  逆向きの含意はない($PB_3$ 模型水準から真の pentagon 層へは渡れない)。**不一致が出ていたら模型忠実性が疑われるはずだった** — 出なかったことを記録する。
- **P-FV-5**: 壁帯の第一照準(§3.2)については**予言しない**。予言の根拠を持たないことを事前登録する。

---

## 6. 要 cert 化 / cert 化不能(正直記帳)

**要 cert 化 = 4 件**
1. **FV プローブ専用 cert schema が無い**。現在 reduction 欄は各窓 cert の付随フィールドで、schema も欄名も不統一
   (`reductions` / `reduction`、`target` / `to`、`fibre` が配列だったり `{note:...}` だったり、`image_size` 欠落あり)。
   FAKE-VOID を台帳の一級市民にするなら `fv-probe/v1`(底窓 UID・細分 UID・$\lvert\mathrm{GT}\rvert$ 両側・像・繊維・全射真偽・二系統印)を新設すべき。
2. **FV-16 の正本 cert が機械可読でない**(`search/certs/wall_census_192_360_20260730.json`・judge の `1.` バグ)。
   裁定 225 は「凍結証明書は非改変」と裁定済みなので、**改変せず再発行(v2)+ 旧 cert への `superseded_by`** が筋。同バグの他 3 本も同時に。
3. **FV-14b($J=L\cap M_5$)が設計・封印予測つきで未走**。便 05 ゲートで止まったまま忘れられている。
   走らせれば $K^{(3)}$ のトリップワイヤ(P-FV-1)が 1 本増え、**封印予測 $\lvert\mathrm{GT}(J)\rvert=144$ の開封**もできる。
   起票は司令塔採否(数学的には安価 — $L$ と $M_5$ の cert が両方手元にある)。
4. **FV-15/17/18/19–24c の「0 本」を canonical UID で突合していない**。census は cert 側から見た悉皆だが、
   窓側の名簿(66 + 67 + 13 + 9 + 7 + 4 + 4)と付き合わせていないため、**窓の重複・取りこぼしを排除できていない**。
   ゆえに本稿は合計を取らない。canonical UID(裁定済み・`certs/canonical_uid_selftest_20260730.json`)との突合が要る。

> **解消済み(裁定 373 ①・探索で判明)**: 起草時に「壁 $n=24$ の cert pin 未特定」としていた項は
> `search/certs/wall2_cert_20260731.json`(E-1)で解決した。同時に W-A 66 窓の封緘正本は
> `wall_probe_20260728.json` ではなく **`wall_miner_v5_20260729.json`**(`windows_processed:66`・`nonabelian_count:0`)であることが判明し、pin を差し替えた。

**cert 化不能 = 1 件**
5. **FV-03**(2 冪 dihedral)の arithmeticity は**公刊文献の定理**であり、工房の cert 体系では証明できない。
   出典 pin(2405 Thm 5.3)で扱い、**我々の cert(A-3a/b/c)は列挙較正であって根拠ではない**と表 1 に明記した。

---

## 7. 主張しないこと / 【GAP】/ 要請

1. **【GAP-FV-1】機構が無い.** FV-SOLV には**支持する機構がない**。$\mathcal D$ 上で hexagon-fake が消える理由を、
   私は「観測が全部そうだった」以上に説明できない。定理 K3・A₅ の証明は**算術飽和**(層 (c))を経由しており、
   層 (a) だけを直接閉じる論法を工房は持っていない。**FV-SOLV は現時点で純粋に経験的な賭けである。**
2. **【GAP-FV-2】実現ギャップ.** FV-13/14(class-6)の機構層の結果を窓層のプローブへ翻訳する橋が無い
   (事前登録 manifest が明示的に禁じている)。この橋が架かれば、64 系の計算が一気に窓プローブの証拠に変わる — 高配当の空白。
3. **UNKNOWN(一級)**: (i) $\mathcal D$ が細分で閉じるか。(ii) $\mathcal W$ の任意の 1 プローブの結果。
   (iii) FV-04 の $PB_3$ 模型と $PB_4$ 水準の関係(監査点 A)。(iv) N∞ 枝の存否($K^{(5)}$ の層 (c))。
4. 本稿は **cross-checked でも verified でもない**。§1–§3 の証明は単系統(私)・§4 の台帳は単一生成器。
   系 FV-COST・定理 FV-EQ の独立再導出は Sol へ。
5. **【要請 1・CV-9】** 新語 **pentagon-fake / arith-fake** を規約台帳へ登録(正典語 *fake* = hexagon-fake との関係を明記)。
   格付けの前に非当事者判読(falsifier)を経ること。
6. **【文献要請 FV-L1】**
   **困難**: 層 (b) は定理 FV-EQ(b) により「$\widehat{GT}=\widehat{GT}_{\rm gen}$ か」という未解決問題そのものであり、
   工房が持つのは $N_A$ の $PB_3$ 模型水準での $\kappa=1$ という 1 点のみ。この層に賭けてよいかの較正材料が無い。
   **欲しい結果の型**: (i) 副有限版の「pentagon $\Rightarrow$ hexagon」型定理(Furusho が associator/pro-unipotent 設定で示した型の
   副有限類似の**有無・部分結果・既知の障害**)、(ii) $\widehat{GT}\subsetneq\widehat{GT}_0=\widehat{GT}_{\rm gen}$ を分離しうる既知の不変量や部分商、
   (iii) **隣接設定における「有限段の解が塔へ持ち上がらない」現象(= fake の類似)の既知例**。
   とくに (iii) が 1 例でもあれば、FV-SOLV の外挿がどれだけ楽観的かの較正になる(**現在は例ゼロ**が唯一の根拠であり、
   それは「まだ誰も探していない」と区別がついていない)。
7. **文献要請にしない件(既配達で足りる可能性)**: FV-WALL (W2) の「非可解モノドロミー窓で $G_{\mathbb Q}$ の像を下から測る機構」は、
   既配達の剛性/Hurwitz 資料(`papers/delivered/` の 3 本・裁定記録あり)が該当しうる。**私は未精読**につき、
   新規遠征を要請せず、必要になった時点で自分で読む(範囲は申告する)。

---

## 8. 新規性の確認(grep 済み)

- **既出**: 「全観測で fake witness ゼロ」(地図 P5 行・帯 0–3)。K³ 二細分の survive 12/12(W3-1/W3-2)。
  バッテリー 7 段の「どの段からも fake witness なし」(W3-3)。class-6 の「fake 候補ゼロ」(W3-10/W3-12)。
  744/86M の全滅と定理 D(p52・裁定 361)。GTPI の 20/20(裁定 278/359/364)。壁族 6 窓(C-WALL-FAM・裁定 339)。
- **本稿が新しく与えるもの**:
  ① **定理 FV-EQ**(三層と「$\widehat{GT}_{\rm gen}$ 全射 / $\widehat{GT}=\widehat{GT}_{\rm gen}$ / 井原予想」の逐層同値)と **系 FV-COST**(無指定 FAKE-VOID = 夢の言い換え)。
  ② **系 FV-SUB** と、それによる**哨戒データの再会計** — 17 プローブ中 10 本が定理の系(spot-check)へ降格し、**独立証拠は 7 プローブ / 底窓 5 個**であることの確定。
  ③ **fake の三分公理化**(hexagon / pentagon / arith)と、それが三つの定義関係に一対一で局在するという読み。
  ④ **帯の定義 $\mathcal D/\mathcal W$**($\mathrm{GTSh}(N,N)$ の可解性 — 窓群の可解性ではない)と、FV-WALL を予想にしない三理由の明文化。
  ⑤ **「fake プローブ 0 本」の機械的悉皆確認**(cert 樹の census)と、W-A / 梯子 / PSL / 壁が**構造測定であって fake データではない**という区別。
  ⑥ P-FV-4(GTPI と定理 A₅ の一致 = 監査点 A の 1 ビットの弱テスト合格)。
  ⑦ judge `1.` バグにより **FV-16 の正本 cert が機械可読でない**ことの検出。
  ⑧ **「壁族 6 窓」のうち $n=40/45$ は可解 = 帯 $\mathcal W$ ではない**という cert 自身による分類訂正(§2.1・裁定 373 ①で受理)。
  ⑨ $J=L\cap M_5$ が**封印予測つきで未走のまま忘れられている**ことの発見(FV-14b)。
  ⑩ 代理量の非同型性の明示 — `fake_witness` 欄はどの cert にも存在せず、5 種の代理量のうち fake 層に効くのは 1 種だけ(§4.3 末)。
- **本稿が新しくないもの(正直に)**: 「fake witness ゼロ」という観測そのもの・K3/A₅/2 冪の定理・744 の全滅・
  定理 D・GTPI の 20/20・壁族の核等式。本稿の仕事は**それらの証拠としての重みを層と量化子に正しく割り付けたこと**であって、
  新しい正の結果ではない(§0 (S-3))。
- **地図への修文提案**(司令塔裁定事項): P5 行の「全観測で witness ゼロ(K³/K⁵ 細分・バッテリー 7 窓・class-6/j=3 関門・W-A 帯)」は
  **格の混在**である — W-A 帯は fake プローブ 0 本(構造測定)、class-6 は実現ギャップの開いた機構層。
  実体は「**17 プローブ・底窓 8 個・うち独立 7 本 / 5 窓・全て VOID。帯 $\mathcal W$ 4 窓と W-A 66 窓はデータ 0**」。
  あわせて **P4 行の「壁族 6 窓」も 4 窓(非可解)+ 2 窓(同族だが可解)へ分ける**(§2.1・裁定 373 ①)。

---

# 追記 A(erratum・2026-08-01 夕)— 出所連鎖の訂正と FV-L1 配達の反映

起草時(本文 §0–§8)の後に届いた 2 件を反映する。**本文は改変していない**(以下が effective source)。
発端: ①司令塔の緊急通達(ihnec 線の逐語照合)②文献配達 `docs/scout/覚書_fvl1_20260801.md`(FV-L1 回答)。

## A.1 【出所注記・CV-10 流儀】Cor 5.4 の根は正典に証明がない

> **依存注記.** §1.1 の $\mathfrak G_{\rm gen}(N)=\bigcap_{K\le N}\mathrm{Im}(R_{K,N})$ は 2401 **Cor 5.4** 経由。
> その根 = **Prop 3.15 は正典に証明が掲載されていない**(「読者演習」)。
> 現在の唯一の根は工房自前の **補題 INT**(`ihnec_v1.md` 追補 B・2 行証明・**Sol 未監査**・監査依頼 T-24 発出中)。

**どこで効くかの精密監査(一括注記にしない — §4 と同じ規律).**
Cor 5.4 には二方向あり、**本稿の荷重部分は易しい方しか使っていない**:

| 使用箇所 | 使う向き | Prop 3.15 依存 |
|---|---|---|
| §1.2 「$\mathbf{WITNESS}$ は fake の有限証明書」 | genuine $\Rightarrow$ 全細分に survive の**対偶** | **なし**(自明方向: $s=R_{K,N}(\hat s\ \text{の}\ \mathrm{GT}(K)\ \text{像})$) |
| §1.5 **系 FV-SUB** | 同上(自明方向) | **なし** |
| §1.4 **定理 FV-EQ (a)** | $\mathfrak G_{\rm gen}$ の定義そのもの | **なし** |
| §1.1 の**等号**・§3.1 FV-SOLV の「同値形(Cor 5.4)」 | 全細分に survive $\Rightarrow$ genuine(**難しい方向**) | **あり** |
| §1.4 **FV-EQ (b)(c)** | Thm 5.2($\widehat{GT}_{\rm gen}\cong\varprojlim\mathrm{GT}(N)$)の単射性 | **要確認**(Thm 5.2 が 3.15 に載るか私は未照合) |

⟹ **系 FV-SUB による会計の組み替え(独立 7 プローブ / 定理の系 10 本)は Prop 3.15 に依存しない** — ここは安全。
危ないのは「$\mathbf{VOID}$ を無限本集めれば genuine が言える」という**逆向きの読み**の方で、
本稿はそれを使っていない(むしろ §1.2 でその非対称性を強調している)。
FV-SOLV の**同値形**だけが依存するので、監査未了の間は **FV-SOLV は主定義(全細分で $R$ 全射)の方を正本**とする。
格は candidate のまま不変(裁定どおり)。

## A.2 【訂正】層 (b) の「名前つき未解決問題」の同定 — 覚書 ① を精密化

覚書は層 (b) を **Furusho Question 14** に同定したが、**向きが逆である**。逐語で照合した:

- **Furusho Q14 = 副有限版 (III) pentagon $\Rightarrow$ (II) hexagon**(覚書 L6・L8「未解決は (II) hexagon のみ」)。
- **本稿の層 (b)** が要求するのは $\widehat{GT}_{\rm gen}\subseteq\widehat{GT}$、すなわち
  **hexagon + charming $\Rightarrow$ pentagon** — Q14 の**converse**。

Q14 が肯定的に解けても $\widehat{GT}$ の記述が簡単になるだけで $\widehat{GT}=\widehat{GT}_{\rm gen}$ は出ない。否定的に解けても分離は出ない。
**⟹ Q14 は層 (b) の隣人であって同一ではない。**

**層 (b) の正しい名前つきの家は覚書 L11–L12 の方**である:
**Harbater–Schneps Main Theorem**($\mathrm{Out}^\sharp_4\cong\widehat{GT}_0=\widehat{GT}_{\rm gen}$ vs $\mathrm{Out}^\sharp_n\cong\widehat{GT}$, $n\ge5$)
— 層 (b) は「**$M_{0,4}$ 水準で決まるか $M_{0,5}$ 水準が要るか**」であり、
**HS Prop. 7**(関係 (III) $\iff$ $\hat K(0,5)$ 上の $(14253)\in S_5$ の持ち上げとの可換性)が求める特徴づけである。
覚書の「一工夫」(これを $B_3/N$ 有限商で書けば fake 検出が置換群計算に落ちる)は**層 (b) の本筋**であり、
深読み案件でなく **FV-WALL と並ぶ第二照準**に格上げしてよい、というのが私の見立てである。

## A.3 【訂正・新規性】層 (a) の名前つきの家は 2008.00066 §4.2 — しかも著者は既に 24 対を走らせている

**正典を逐語で読んだ**(`papers/txt/2008.00066-what-are-gt-shadows.txt` §4.2):

> **Is there a charming GT-shadow that is also fake?**
> … At the time of writing, we did not find a single example of a charming GT-shadow that is also fake.
> Here is what we did. In the list (4.2), there are exactly **24 pairs** $(N^{(i)},N^{(j)})$ with $i\ne j$ such that $N^{(j)}\le N^{(i)}$.
> For each such pair, we showed that **every GT-shadow in $\mathrm{GT}^\heartsuit(N^{(i)})$ survives into $N^{(j)}$**, i.e. the natural map
> $\mathrm{GT}^\heartsuit(N^{(j)})\to\mathrm{GT}^\heartsuit(N^{(i)})$ is onto. We also looked at other selected examples of elements $K\le N$
> … where **$K$ is obtained by intersecting $N$ with another element of (4.2)**. In all examples we have considered so far,
> the natural map $\mathrm{GT}^\heartsuit(K)\to\mathrm{GT}^\heartsuit(N)$ is onto.

**帰結 3 点(いずれも本稿の格を下げる方向・正直に記帳する):**
1. **層 (a) の名前つきの家は §4.2 の Question**(Q14 ではない)。FAKE-VOID = この Question への「無い」側の賭けである。
2. **「初の系統的有限データ」は誤り**。著者は $B_4$ 圏で **24 対 + 交叉細分**を既に走らせ、**すべて onto** を得ている。
   我々の新しさは「**初であること**」ではなく「**圏が違うこと**」— 主線($B_3$-gentle・hexagon のみ・2401)側の対応データである
   (2405 Remark 1.2 の同名別物)。§8 の新規性欄をこの向きに読むこと。
3. **設計の独立検証(良い報せ)**: 著者の「$K$ = $N$ と別の窓の**交叉**」という構成は、
   我々の $L=K^{(3)}\cap N_0$・$M_5=K^{(3)}\cap N_5$・$J=L\cap M_5$ と**同一の技法**である。
   我々の哨戒設計は独立に正しい形に到達していた(と同時に、既知技法の再発明でもあった)。

**副産物(機構)**: 覚書 L17 の「有限集合の逆系は自動 Mittag-Leffler ⟹ fake の存在には必ず有限の証人がある」は、
§1.2 の非対称性の**上位の理由**である。像の降鎖 $\mathrm{Im}(R_{K,N})$ は有限集合の減少列ゆえ**必ず有限段で安定**し、
その安定値が $\mathfrak G_{\rm gen}(N)$。⟹ **genuine 判定は原理的には有限深度で決まる — 深度が不明なだけ**。
これは Prop 3.15 の内容と同じ形であり(A.1)、補題 INT の監査が通れば §1.2 に格上げして書ける。

## A.4 c₂ 不変量 — 起票を支持。ただし**決定的な問いを先に置く**

覚書 ② の設計(独立 7 プローブの witness に対する $c_2$ 分布記録)を**支持する**。**値の予言はしない。**
ただし観測の意味は次の 1 問の答で**正反対になる**ので、設計書にこれを明記して起票されたい:

> **決定的な問い(C2-Q)**: 関係 $\lambda^2=24c_2(f)+1$ は **hexagon だけの帰結か、pentagon を要するか。**
> - **hexagon だけの帰結なら**: 全 GT-shadow が自動で満たす ⟹ 測定は**我々の evaluator の較正**にしかならない(分離能力ゼロ)。
> - **pentagon を要するなら**: これは**有限段で計算できる pentagon 持ち上げの必要条件** = **層 (b) 初の実効的な fake 検出器**。

**この問いは我々の手持ちで部分的に決着できる**(委嘱設計案):
1. **較正段(必ず通らねばならない)**: $K^{(3)}$ の 12 元と $N_A$ の 20 元で $\lambda^2\equiv24c_2+1$ を検査。
   定理 K3・A₅ によりこれらは arithmetical ⟹ pentagon 持ち上げ可 ⟹ **必ず成立する**。破れたら実装か定理のどちらかが誤り。
2. **プローブ段**: 定理に覆われていない底窓($N_Q$・$K^{(12)}$、および帯 $\mathcal W$ の 4 窓)で同じ検査。
3. **破れが出た場合の扱い**: それは **pentagon-fake の候補**であり、**P-FV-3(§5)の異常主張の門**が発動する
   — 台帳に書く前に Sol 監査、可能なら Lean。$\widehat{GT}\subsetneq\widehat{GT}_{\rm gen}$ の証明に相当しうるため。
4. **有限商での型**: $c_2$ は $[F_2,F_2]/[F_2,[F_2,F_2]]\cong\mathbb Z$ の像として定義され、有限商では $\mathbb Z/d$ に落ちる。
   関係は合同式になり、覚書 L7(a) の言うとおり**二次剰余の可解性条件**として有限段で判定できる。

## A.5 Theorem B.2(アーベル設定)— 移送先が明示されており、**独立証拠をさらに削る**

`2008.00066` **Prop. B.1** は三条件の同値を与える: **(a) $PB_4/N$ アーベル $\iff$ (b) $PB_3/N_{PB_3}$ アーベル $\iff$ (c) $F_2/N_{F_2}$ アーベル**。
**Thm B.2**: アーベル設定なら $\mathrm{GT}^\heartsuit(N)=\{(m+N_{\rm ord}\mathbb Z,\bar1)\mid\gcd(2m+1,N_{\rm ord})=1\}$ で、**その全てが genuine**(著者は「Kronecker–Weber の類似」と呼ぶ)。

**主線への移送(私の見立て):**
- **群論の半分は 1 行で移る**: charming は $\bar f\in[F_2/N_{F_2},F_2/N_{F_2}]$ を要求するから、
  $F_2/N_{F_2}$ アーベル $\Rightarrow$ 導来部分群自明 $\Rightarrow\bar f=\bar1$。ゆえに $\mathrm{GT}(N)\subseteq\{(m,\bar1)\}$。
  **これは $B_3$-gentle 圏でもそのまま成立する**(Prop B.1 (c) が $F_2$ 側の条件で述べられているのが効く)。
- **genuine の半分は移らない(そのままでは)**: 著者の証明は算術(Kronecker–Weber 型)で、
  $\widehat{GT}_{\rm gen}$ 側の元が $f\equiv1$ を実現することを要する。**移送は未検証** — 断定しない。

**会計への影響(下方修正の予告)**: 移送が成立すれば、**アーベル窓のプローブは定理の系に落ちる**。
機械確認した実例: **$N_5$ は確実にアーベル設定**である — cert が全 4 shadow で `f_word: []`(自明 $f$)を記録しており、
これは Thm B.2 (B.2) 式の指紋そのものである(`certificates/N5.v1.json`)。

> ⟹ **FV-11($N_5$)は「独立」から「定理の系(移送成立時)」へ降格する見込み。**
> **$N_2$・$N_3$ は未確認**(cert `2b` の定義が $\pi^{-1}(F_2^4\gamma_4(F_2))$ = 類 3 冪零ゆえ非アーベルの公算が高いが、照合していない)。
> 最悪の場合、**独立証拠は 7 プローブ / 5 窓 → 4 プローブ / 2 窓($N_Q$ と $K^{(12)}$)まで縮む**。
> これは悪い報せではなく**会計が正しくなる**ということであり、同時に
> **$\mathcal D$ のうち非アーベル・非定理の窓こそが FV-SOLV の真の試験場**であることを指している。

## A.6 追記 A で動いた札(一覧)

| 項 | 変更 |
|---|---|
| §1.1 の等号・§3.1 の同値形 | **出所注記つき**(Prop 3.15 未証明・補題 INT が唯一の根・Sol 監査 T-24 中)。FV-SOLV の正本は主定義の方 |
| §1.4 FV-EQ (b)(c) | Thm 5.2 の Prop 3.15 依存は**要確認**(私は未照合) |
| §1.5 FV-SUB・§1.2 の非対称性 | **無傷**(自明方向のみ使用) |
| §7 【GAP-FV-1】 | 「純粋に経験的な賭け」→「**2008.00066 §4.2 の名前つき未解決問題への賭け。$B_4$ 圏では著者が 24 対 + 交叉を走らせ全て onto。我々は主線($B_3$-gentle)側の対応データ**」 |
| §8 新規性 | 「初の系統的有限データ」の含意を**撤回**。新しいのは**圏**であって順序ではない |
| §3.2 FV-WALL | 第一照準は不変。**第二照準として HS Prop. 7 の有限商翻訳**を新設(A.2) |
| §4 表 1 FV-11($N_5$) | 「独立」に**降格予告**の注記(A.5) |
| 新規作業 | **C2-Q**(較正段 → プローブ段)・**Thm B.2 移送検証**・**$N_2/N_3$ のアーベル性照合** — いずれも起票は司令塔採否 |

**採用禁止の記録**: 覚書 L23 — arXiv 2503.13006(「GT 予想の証明」を称する)は査読痕跡なし・**採用禁止**。本稿は一切参照していない。
