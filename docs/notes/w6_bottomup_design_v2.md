# W-6 掘削 BOTTOM-UP 設計 **v2 — 方針起草**(F102-6.3 差戻しへの逐条対応)

**状態札: `design / 方針起草(凍結請求ではない)/ 走らせていない(GAP 実行ゼロ)/ Sol 未承認 / 発火未認可 / 実測ゼロ / 封印 3 量非接触・Im R 非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05・**新設**(`w6_bottomup_design_v1.md` は**不改変**)
- 委嘱: 司令塔 —「Sol の blocking 4 点への逐条対応**方針**を起草。**限定認可分**(S0 較正 + $H^2(S_4,V)$ 在庫表)の実施要領を § に切り出す(これだけは即発注できる形に)」
- **入力正本**: `sol/sol_reply_102_math29.md` **F102-6.3**(blocking 4 点・限定認可の範囲)/ `docs/notes/w6_bottomup_design_v1.md`(v1)/ **`docs/notes/w6_kill_theorems_v2_erratum.md`(本書の理論的前提。とくに補題 LAT-Γ・NC-2′・系 THETA-2000/4500・$V\subseteq Z(G_{20})$)** / `w6_kill_theorems_v1.md` / `k5_w6_construction_v1_addendum_b_k20paper.md` / `docs/week1-定義ノート.md` §1〜§3
- **外部文献ゼロ。**

> ## 非接触の申告
> **本書は 1 行も実行していない**(GAP 起動ゼロ)。**$\mathrm{Im}\,R_{N,K^{(5)}}$ 非接触・$d_N$ 非評価・封印 3 量非接触・証明書非読。** PSL 屋根は宇宙から除外(campaign X-4)。v1 §5.2 の段別非接触表を継承する。

---

## 0. 判定(先に 6 行)

| # | 内容 |
|---|---|
| **①** ★★★ | **blocking (i) は完全に解ける。** ★ **定理 VCEN-MOD**(§2): $A$ 自明の下で **(V-cen) ⟺ $O_2(S_4)=V_4$ が $V$ に自明作用 ⟺ $V$ が $S_4\twoheadrightarrow S_3$ から inflate された加群**。⟹ (V-cen) は**加群だけで決まる**ので、**列挙の定義そのものに置ける**(kill より前・追加コストゼロ)。「順序を入れ替える」より強い解 |
| **②** ★★ | **blocking (i) の残り(非中心版 SURJ)には既存の受け皿がある。** ★ **SURJ-GATE = (V-cen) $\vee$ ($V\subseteq\Phi(P)$)**(§2.3)。後者は補題 SURJ-W6 の Frattini 論法(既出)で、**非中心でも効く**。両方外れた層は **SCOPE_OUT**(kill しない) |
| **③** ★★ | **blocking (ii) は「marked datum」の型定義で閉じる**(§3)。抽象類ではなく **$\rho:B_3\twoheadrightarrow\widehat P$($q$ の持上げ・$\rho(c)=1$)を第一級の対象**にする。取得段は **$\lvert V\rvert^2\le256$ 通りの総当り**(braid 関係式 + $\rho(c)=1$ + 全射性)で、**GQuotients より 3 桁安い**。$N,\ P,\ \bar x,\bar y,\ \alpha$-lattice, defect はすべて $\rho$ から定義される |
| **④** ★ | **blocking (iii)**: SAT の存在述語を**逐語で定式化**した(§4.1)。同時に、**erratum v2 で宇宙が激減したため SAT は critical path から外れる**(§4.3)— 直接悉皆列挙で足りる。**SAT を「第 2 系統の照合レーン」へ降格する提案**を司令塔判断に付す(研究者発案の段なので当方では決めない) |
| **⑤** ★ | **blocking (iv)**: GQuotients は**別ゲートのまま維持**(§5)。ただし §3 の marked lift 列挙が**第 1 系統**、GQuotients が**第 2 系統**という二系統の役割分担に変える |
| **⑥** ★★★ | ★ **宇宙が壊滅的に小さくなった**(§6.1): erratum v2 の下限($p=2$ で $\lvert PB_3/N\rvert\ge4000$、$p=3$ で $\ge13500$)と VCEN-MOD を合わせると、**cap 8000 の下で (V-cen) 層の加群は 4 型**、うち $\lvert V\rvert=8$ の帯は **$V\cong\mathbf F_2\oplus D$ ただ 1 型**。v1 の「(加群,類) 150〜400」は**桁が違っていた** |

> ⚠ **本書は凍結を請求しない。** 方針(型・順序・ゲート)を確定し、**限定認可分(§7)だけを発注可能な形にする**。宇宙 U-2/U-3 の再凍結と S1〜S9 の発火は、§7 の在庫表の実測値を見てから **v2 本体(別紙)**で請求する。

---

## 1. blocking 4 点への逐条対応(要旨表)

| Sol の blocking | 対応方針 | 節 | 残る GAP |
|---|---|---|---|
| **(1) kill と SURJ の順序が逆**(非自明 $S_4$-module の典型は非中心) | ★ **順序ではなく型で解く**: (V-cen) を**加群の性質**として特徴づけ(定理 VCEN-MOD)、列挙宇宙を **(V-cen) 層** と **非中心層** に**最初から**分ける。kill は (V-cen) 層でのみ発火。非中心層は SURJ-GATE の第 2 枝($V\subseteq\Phi(P)$)を試し、それも外れたら **SCOPE_OUT(kill 禁止)** | §2 | 【K5-GAP-W1】は**閉じない**(非中心かつ非 Frattini の層は掘らない) |
| **(2) marked realization がない** | ★ **marked datum** $(V,[\varepsilon],\rho)$ を第一級の対象に。取得段 **S1.5** を新設($\lvert V\rvert^2$ 総当り) | §3 | 【BU-GAP-3】($p=3$ の持上げ依存)は**消える**(marked なら持上げは決まっている) |
| **(3) S8.5 の同値主張が未実装** | ★ 存在述語を逐語化(§4.1)+ **clause source-map 契約**(§4.2)。実装は次段。★ **SAT の位置づけ自体の再検討**を上申(§4.3) | §4 | 【BU-GAP-6】は**未閉のまま**(降格提案が通れば重要度が下がる) |
| **(4) 格付け語が強すぎる** | ★ 全面採択。**SAT witness / GAP 再構成 / coker checker は cross-check の候補**。LRAT は **Lean 内検証済み checker を通した場合のみ** verified を名乗る(user memory「Lean axiom policy」「Solver candidate philosophy」に整合) | §5.3 | — |

---

## 2. ★★★ (V-cen) を**加群の条件**にする(blocking (1) の解)

### 2.1 定理 VCEN-MOD

> ### 定理 VCEN-MOD(candidate・本書)
> $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$c\in N$、$\widehat P=B_3/N$、$P=PB_3/N$、$V=\ker(\widehat P\to\widehat G_5)$ が**アーベル**とする。$V$ は $\widehat G_5=B_3/K^{(5)}$-加群である。このとき
> $$\textbf{(V-cen)}\ \bigl(V\subseteq Z(P)\bigr)\iff G_5\ \textbf{が}\ V\ \textbf{に自明に作用する}.$$
> さらに $A=[G_5,G_5]\cong C_5^3$ が $V$ に自明に作用するならば($p\in\{2,3\}$・$\dim V\le11$ で補題 A-TRIV により自動)、$V$ は $S_4=\widehat G_5/A$-加群であり
> $$\boxed{\ \textbf{(V-cen)}\iff V_4:=G_5/A=O_2(S_4)\ \textbf{が}\ V\ \textbf{に自明作用}\iff V\ \textbf{は}\ S_4\twoheadrightarrow S_4/V_4\cong S_3\ \textbf{から inflate された加群}\ }$$

**証明.** $V$ はアーベルゆえ自身に自明に作用し、$P$ の共役作用は $P/V\cong G_5$ を経由する。⟹ $V\subseteq Z(P)$ ⟺ $G_5$ が自明作用 ✓。$A\subseteq G_5$ が自明作用のとき、$G_5$ の作用は $G_5/A\cong C_2^2$ を経由する。$\widehat G_5/A\cong S_4$ の中で $G_5/A$ は指数 6 の正規部分群で位数 4 ⟹ $G_5/A=V_4=O_2(S_4)$($S_4$ の位数 4 の正規部分群は $V_4$ のみ)。⟹ (V-cen) ⟺ $V_4$ 自明作用 ⟺ 作用が $S_4/V_4\cong S_3$ を経由。∎

> ### ★ これが blocking (1) をどう解くか
> Sol は「S4–S8 はノルム/障害 witness だけで候補を落とすが、SURJ を与える (V-cen) は S10 まで調べない」と指摘した。**VCEN-MOD により (V-cen) は加群の同型類だけで決まる**ので、**列挙の第 0 段(宇宙の定義)で判定できる**。⟹ 「gate を前に置く」どころか **gate が宇宙の定義に吸収される**。
> ⚠ **前件 $V$ アーベル**は v1 の宇宙(初等アーベル核)では自動。非アーベル核【BU-GAP-1】へは**そのまま拡張できない**(SCOPE_OUT のまま)。

### 2.2 ★ 較正(既在の実物と一致すること)

$K^{(20)}$: $V\cong\mathbf F_2^3$ で $\Gamma$ の像は **3 座標の置換 $S_3$**、$G_{20}$(したがって $G_5$)は $V$ に**自明**に作用する(addendum B §2.3 の符号消失・erratum v2 §3 の $Z(G_{20})=V$)。⟹ **$K^{(20)}$ の $V$ は $S_3$-inflate 加群**であり、VCEN-MOD が予言するとおり (V-cen) を満たす。★ **既知の唯一の実物と整合する**(較正項目 A-12・§7)。

### 2.3 ★ SURJ-GATE(非中心層の受け皿)

> ### 定義 SURJ-GATE
> 候補 $(V,[\varepsilon],\rho)$ に対し
> $$\textbf{SURJ-GATE}\ :=\ \textbf{(V-cen)}\ \ \vee\ \ \bigl(V\subseteq\Phi(P)\bigr).$$
> - 第 1 枝: **補題 SURJ-CENT**(v1 §2.2・Sol も条件付きで PASS)。
> - 第 2 枝: **補題 SURJ-W6**(w6 §4.2 の Frattini 論法・**既出**)。$HV=P$ かつ $V\subseteq\Phi(P)$ ⟹ $H=P$。**中心性を要しない。**
> - **どちらも成らない候補は `SCOPE_OUT`(S-BU-7)**: kill も生存判定もしない。【K5-GAP-W1】が未閉鎖である以上、自己判断で続行しない。

⟹ Sol の「非中心版 SURJ を先に証明する」という代替枝を、**既存の Frattini 補題の再利用**で部分的に満たす。**完全な非中心版 SURJ は【K5-GAP-W1】として開いたまま**であり、本書はそれを証明しない(証明したと書かない)。

---

## 3. ★★ marked datum の型と取得段(blocking (2) の解)

### 3.1 型定義

記号(定義ノート §1): $B_3=\langle\sigma_1,\sigma_2\mid\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle$、$x=\sigma_1^2$、$y=\sigma_2^2$、$\Delta=\sigma_1\sigma_2\sigma_1$、$c=\Delta^2$、$q:B_3\twoheadrightarrow\widehat G_5=B_3/K^{(5)}$。

> ### 定義 MARKED(本書)
> **marked datum** とは 3 つ組 $\mathcal D=(V,\ \widehat P,\ \rho)$ で:
> 1. $V$: 有限 $\mathbf F_p[\widehat G_5]$-加群($p\in\{2,3\}$)。
> 2. $\widehat P$: 拡大 $1\to V\to\widehat P\xrightarrow{\ \pi_{\widehat P}\ }\widehat G_5\to1$(類 $[\varepsilon]\in H^2(\widehat G_5,V)\cong H^2(S_4,V)$)。
> 3. $\rho:B_3\to\widehat P$: **$q$ の持上げ**($\pi_{\widehat P}\circ\rho=q$)であって **$\rho$ は全射**かつ **$\rho(c)=1$**。
>
> このとき **$N:=\ker\rho$** は $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$c\in N$ を自動的に満たし、
> $$P:=\rho(PB_3)=\rho(F_2),\quad \bar x:=\rho(x),\quad \bar y:=\rho(y),\quad N_{F_2}=N\cap F_2,\quad \alpha(N_{F_2})\subseteq\mathbf Z^2,$$
> $$W=V\cap[P,P],\quad \mathcal L=\pi^{-1}(f_1)\cap[P,P],\quad \beta_\theta,\beta_\tau,\quad \delta_{\rm roof}$$
> が**すべて定義される**。逆に、v1 の宇宙の任意の窓 $N$($N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$c\in N$、$V$ 有限)は $\widehat P:=B_3/N$、$\rho:=$ 標準射影で marked datum を与える。
> $$\boxed{\ \textbf{marked datum の同型類} \longleftrightarrow \textbf{窓 }N\textbf{ の集合}\quad(\textbf{1 対 1}).}$$

**逆向きの確認**: $c\in N$ ⟹ $\rho(c)=1$ ✓;$N\subseteq\ker q=K^{(5)}$ ✓;$\ker(\widehat P\to\widehat G_5)=K^{(5)}/N\cong K^{(5)}_{F_2}/N_{F_2}=V$($c\in N$ を使う)✓。∎

> ### ★ Sol の指摘との対応
> 「抽象 $H^2(S_4,V)$ の類だけでは、指定された $B_3$ 商、marked lifts $x,y$、$\alpha$-lattice、defect を定義できない」 — **そのとおりである。** v1 の段 S4/S5/S7/S8 は暗黙に $\rho$ を使っていた。**v2 では $\rho$ を対象の一部にする。**

### 3.2 取得段 **S1.5**(marked lift の列挙)

$\rho$ は $\rho(\sigma_1),\rho(\sigma_2)$ で決まる。各々 $\pi_{\widehat P}^{-1}(q(\sigma_i))$ の $\lvert V\rvert$ 個から選ぶ。

$$\textbf{候補数}=\lvert V\rvert^2\ \le\ 16^2=\mathbf{256}\quad(p=2,\ \dim V\le4).$$

各候補で**有限回の群演算**により次を検査する:

| # | 条件 | 意味 |
|---|---|---|
| **L-1** | $\rho(\sigma_1)\rho(\sigma_2)\rho(\sigma_1)=\rho(\sigma_2)\rho(\sigma_1)\rho(\sigma_2)$ | $\rho$ が well-defined($B_3$ は 1 関係子群) |
| **L-2** | $\rho(c)=\rho(\sigma_1\sigma_2\sigma_1)^2=1$ | $c\in N$ |
| **L-3** | $\langle\rho(\sigma_1),\rho(\sigma_2)\rangle=\widehat P$ | 全射性(破れたら**より小さい窓**であり、その像を別 datum として拾う) |
| **L-4** | $N=\ker\rho$ が isolated | ⚠ **本段では判定しない**(定義ノート §2 の isolated は shadow 側の性質)。**【BU-GAP-8】として明示**し、isolated は前件として持ち回る |

> ### ★ 理論的な位置づけ(**なぜ安いか**)
> $q$ の持上げの集合は、非空ならば $Z^1(B_3,V)$ の torsor である。非空性の障害は $q^\ast[\varepsilon]\in H^2(B_3,V)$ であり、$B_3$ は **2 生成 1 関係子**なので $H^2(B_3,V)$ は $\mathbf F_p$ 上の小さな線型代数(表示 2-複体)。⟹ **$\lvert V\rvert^2$ 総当りは理論上も冗長でなく、素直に最速**である。
> ⚠ **これは S9(GQuotients)を置き換えるものではない**(§5)。**同じ対象を別実装で 2 度作るのが二系統の趣旨**である。

### 3.3 段の再構成(v1 §3.1 の差替案)

| 段 | 名 | 内容 | v1 からの変更 |
|---|---|---|---|
| **S0** | 較正 | assert 表(§7.2) | ★ 項目追加 |
| **S1** | **宇宙**(加群) | $\mathbf F_p[S_4]$-加群 $V$ を列挙し、**(V-cen) 層(= $S_3$-inflate)** と **非中心層**に分ける | ★★ **VCEN-MOD による層別が新設**(旧 S10 が消える) |
| **S2** | **位数** | erratum v2 の下限($p=2$: $\lvert V\rvert\ge8$ / $p=3$: $\ge27$) | ★★ **系 THETA-1000(v2)/1500/2000/4500 に差替**(旧 S2 より強い) |
| **S3** | 拡大類 | $H^2(S_4,V)$ の全類(分裂類も較正のため入れる) | 不変 |
| **S1.5→S3.5** | ★ **marked lift** | §3.2 の L-1〜L-3 | ★★ **新設**(blocking (2)) |
| **S4′** | **格子** | $\alpha(N_{F_2})$ を計算し **NC-2′** を適用($p=2$ では「$0\ne W\ne V$」に潰れる) | ★ **NC-2′ に差替**(erratum v2 §2.3) |
| **S5** | $W\ne0$ | KT-4 | 不変 |
| **S6** | 障害群 | $\operatorname{coker}\psi_W\ne0$ | 不変($W$ 上・v1 の訂正どおり) |
| **S7** | 障害類 | $[(-\beta_\theta,-\beta_\tau)]\ne0$ | 不変 |
| **S8** | 屋根 | $\delta_{\rm roof}\ne0$ | 不変 |
| **S8.5** | SAT | §4(**位置づけは司令塔判断待ち**) | ★ 降格提案 |
| **S9** | **GQuotients** | ★ **第 2 系統の照合**(S3.5 の結果と突合) | ★ 役割が変わる |
| — | SURJ-GATE | **S1 で層別・S3.5 で第 2 枝を判定** | ★ 旧 S10 を前倒し・分割 |

---

## 4. SAT 段(blocking (3))

### 4.1 ★ 存在述語の逐語定式化

層 $\mathcal S(V)$ := 固定した加群 $V$ に対する marked datum 全体とする。SAT が判定すべき命題は**逐語**で:

$$\boxed{\ \exists\,[\varepsilon]\in H^2(S_4,V)\ \ \exists\,\rho\in\mathrm{Lift}(q,\widehat P_{[\varepsilon]})\ :\ \mathrm{L}\text{-}1\wedge\mathrm{L}\text{-}2\wedge\mathrm{L}\text{-}3\wedge\mathrm{SURJGATE}\wedge\mathrm{NC}\text{-}2'\wedge(W\ne0)\wedge(\operatorname{coker}\psi_W\ne0)\wedge(\text{障害類}\ne0)\ }$$

**変数**: (i) $[\varepsilon]$ の $\mathbf F_p$-座標($\dim H^2(S_4,V)$ 個)(ii) $\rho(\sigma_1),\rho(\sigma_2)$ の $V$-成分($2\dim V$ 個)(iii) 補助変数($\widetilde f_0$ の $W$-成分・$\beta$ の成分)。
**節**: 上の各連言項を $\mathbf F_p$ 上の多項式条件 → CNF へ落としたもの。$p=2$ なら XOR 節が主。
**UNSAT の意味**: 「この層には $\widetilde m=0$ の項で障害の立つ marked datum が**存在しない**」。

> ⚠ **v1 の述語(「$\Gamma$-同変・非分裂・障害類 $\ne0$ の拡大類が存在するか」)は $\rho$ を含んでいなかった** — Sol の blocking (2) と (3) は同根である。上の述語は $\rho$ を明示的に量化する。

### 4.2 clause source-map 契約(**実装前に凍結する規約**)

| # | 契約 |
|---|---|
| **SM-1** | 各節に **由来タグ**(L-1 / L-2 / L-3 / SURJGATE / NC-2′ / W / coker / class)を必ず付す。タグ無し節を生成した encoder は**不合格**。 |
| **SM-2** | 由来タグごとの節数・変数番号域を cert に出力し、**紙の条件と 1:1 で対応表**を作る(【BU-GAP-6】の照合はこの表の上で行う)。 |
| **SM-3** | **両側較正**(v1 DF-BU-8 を継承): 既知 UNSAT 層($K^{(20)}$ 型・障害類 0)と既知 SAT 層(合成 dummy)の**双方**で正しく判定するまで、UNSAT を陰性として使わない(`CALIBRATION_PENDING`)。 |
| **SM-4** | **紙篩との突合**: S4′〜S8 で紙が落とした候補が SAT でも落ちること(および逆)を、**層ごとに全候補で**照合する(宇宙が小さいので**全数照合が可能**・§6)。⟹ 【BU-GAP-6】は**閉じられる見込み**。 |

### 4.3 ★ 位置づけの再検討(**司令塔判断を仰ぐ**)

erratum v2 により宇宙が激減した(§6)。cap 8000 の (V-cen) 層は **加群 4 型 × 類 $\le p^{\dim H^2}$ × lift $\le256$** で、**総候補数は数千のオーダー**である。⟹

$$\boxed{\ \textbf{直接悉皆列挙が可能であり、SAT は「存在の一撃判定」としては不要になった。}\ }$$

**提案**: S8.5 を **critical path から外し、第 2 系統の照合レーン**(SM-4 の全数照合 = encoder の忠実性の検査台)へ降格する。**UNSAT+LRAT の価値は残る**(悉皆性の機械証明)が、それは**直接列挙が先に答えを出した後の裏取り**になる。
⚠ **本段は研究者発案(統計×ソルバー統合)であり、当方の権限で削らない。** 降格の可否は司令塔裁定を仰ぐ(§9-3)。

---

## 5. GQuotients ゲートと格付け(blocking (4))

### 5.1 二系統の役割分担

| 系統 | 実装 | 出力 |
|---|---|---|
| **第 1 系統** | §3.2 の marked lift 総当り(拡大を明示構成 → $\rho(\sigma_i)$ を総当り) | 窓 $N$ の候補と、その $P,\bar x,\bar y$ |
| **第 2 系統** | `GQuotients(B_3, \widehat P)` + marked 条件($\ker\subseteq K^{(5)}$・$c\mapsto1$)のフィルタ | 同じ集合(であるべき) |
| **判定** | ★ **両者の突合**。個数が食い違ったら `TWO_LANE_MISMATCH / STOP`(どちらが取りこぼしたかを検分) | 【BU-GAP-2】(GQuotients の取りこぼし)の**実地試験**になる |

### 5.2 `lins` の扱い

v1 §7.1 のとおり **lins 探索認可は取り下げたまま**。ただし第 3 系統として温存(【BU-GAP-2】が実際に発火した場合のみ)。

### 5.3 格付け語(Sol の blocking (4) を逐語採択)

| 産物 | 名乗ってよい格 |
|---|---|
| SAT witness | ★ **candidate のみ**(ソルバー = 候補発見器) |
| GAP 再構成 / coker checker / marked lift 総当り | ★ **cross-check の候補**。CV-9 非当事者判読を経て初めて `cross-checked` |
| LRAT | ★ **実在する Lean 検証済み checker を通した場合のみ** verified(通さないなら `LRAT-checked (non-Lean)`) |
| 紙の定理(VCEN-MOD 等) | ★ **paper-proof candidate**(Sol 未監査) |

---

## 6. ★★ 宇宙の見積り(erratum v2 + VCEN-MOD の帰結)

### 6.1 加群 — **有限表現型ゆえ厳密に数えられる**

**(V-cen) 層 = $\mathbf F_p[S_3]$-加群**(VCEN-MOD)。

> ### ★ 補題 F2S3(candidate・本書)
> $$\mathbf F_2[S_3]\ \cong\ \mathbf F_2[C_2]\ \times\ M_2(\mathbf F_2).$$
> ⟹ **すべての $\mathbf F_2[S_3]$-加群は $\ \mathbf F_2^{\,a}\oplus(\mathbf F_2C_2)^{\,b}\oplus D^{\,c}$**($\mathbf F_2$=自明、$\mathbf F_2C_2$= 自明の非分裂自己拡大($\tau$ 自明・$\theta$ が unipotent)、$D$= 2 次元単純)。**分解は一意**(有限表現型・2 ブロック)。

**証明.** $\mathbf F_2C_3\cong\mathbf F_2\times\mathbf F_4$($t^3-1=(t-1)(t^2+t+1)$、後者は $\mathbf F_2$ 上既約)。$C_2$ は $C_3$ を反転するので第 1 因子に自明・第 2 因子に Frobenius で作用 ⟹ $\mathbf F_2S_3\cong\mathbf F_2[C_2]\times(\mathbf F_4\rtimes C_2)$。Galois 拡大の skew 群環は行列環ゆえ $\mathbf F_4\rtimes C_2\cong M_2(\mathbf F_2)$。次元 $2+4=6$ ✓。$M_2(\mathbf F_2)$ 上の加群は $D^c$、$\mathbf F_2[C_2]$ 上の不可分解は $\mathbf F_2$ と $\mathbf F_2C_2$ の 2 個。∎

| $\dim_{\mathbf F_2}V$ | (V-cen) 層の加群 | 個数 |
|---|---|---|
| 2 | $(a,b,c)=(2,0,0),(0,1,0),(0,0,1)$ | **3** |
| 3 | $(3,0,0),(1,1,0),(1,0,1)$ | **3** |
| 4 | $(4,0,0),(2,1,0),(2,0,1),(0,2,0),(0,1,1),(0,0,2)$ | **6** |
| **計(dim 2〜4)** | | ★ **12(厳密・見積りではない)** |

### 6.2 ★★ erratum v2 の帯制約を掛けると **4 型**に落ちる

erratum v2 §2.5: $p=2$ の生存帯は $\lvert V\rvert\ge8$、しかも $\lvert V/W\rvert=4$ と $V/W\cong(2)/(4)\cong\mathbf F_4=D$(**$\Gamma$-加群として $D$**)が**強制**される。

| $\dim V$ | 強制条件 | 残る加群 |
|---|---|---|
| **3**(4,000) | $\lvert W\rvert=2$(⟹ $W$ 自明 1 次元)、$V/W\cong D$ | ★ **$V\cong\mathbf F_2\oplus D$ の 1 型のみ**($\mathrm{Ext}^1_{\mathbf F_2S_3}(D,\mathbf F_2)=0$ — 別ブロック ⟹ 非分裂拡大なし)。**= $K^{(20)}$ の加群そのもの** |
| **4**(8,000) | $\lvert W\rvert=4$、$V/W\cong D$ | $\mathbf F_2^2\oplus D$ / $\mathbf F_2C_2\oplus D$ / $D\oplus D$ の **3 型**(商 $\cong D$ をもつのは $c\ge1$ の 3 型のみ)。$W$ は前 2 型では一意($\mathbf F_2^2$ / $\mathbf F_2C_2$)、$D\oplus D$ では **$D$-部分加群のいずれか(一意ではない)** |
| $p=3$ | $\lvert V\rvert\ge27$ ⟹ $\lvert PB_3/N\rvert\ge13{,}500$ | ★ **cap 8000 の下ではゼロ** |

$$\boxed{\ \textbf{cap 8000・(V-cen) 層の加群は }\mathbf 4\ \textbf{型。v1 の「30〜50 型・(加群,類) 150〜400」は桁が違っていた。}\ }$$

⚠ **これは「掘る対象が消えた」ではない**。$W$ と $V/W$ の**形**が決まっただけで、**類と lift の自由度**($H^2$ と $\lvert V\rvert^2$)は残る。**空だとは主張しない**(S-BU-6)。

### 6.3 コスト

| 段 | コスト |
|---|---|
| S0 較正 | GAP 数分 |
| S1(加群)/ S2(位数) | ★ **紙**(§6.1 の表) |
| S3($H^2(S_4,V)$) | ★ **位数 24 の群コホモロジー・4〜12 個** — 秒〜分 |
| S3.5(marked lift) | ★ $\lvert V\rvert^2\le256$ × 類数 — **秒** |
| S4′〜S8 | $\mathbf F_p$ 線型代数 + $\mathbf Z^2$ の格子 — **秒** |
| S9(GQuotients) | ★ 唯一重い。**S3.5 を通った候補にだけ**走らせる |

---

## 7. ★★★ 限定認可分の実施要領(**これだけは即発注できる形**)

> ### 認可の範囲(F102-6.3 逐語)
> 「結果を棄却・EMPTY-THM・候補発見へ使わない **S0 の較正と $H^2(S_4,V)$ の在庫表/census** だけを開始してよい。C4/C9/非可換核【BU-GAP-1】は『空』でなく明示的 SCOPE_OUT のまま残すこと。SAT、S1–S8 kill、S9 は未認可。」

### 7.1 発注物(2 本・implementer / ep-keeper 案件)

| # | 成果物 | 内容 |
|---|---|---|
| **W6BU-S0** | 較正 cert `k5gen_w6_bu_s0_<date>.json` | §7.2 の assert 表を全項目 fail-closed で検査 |
| **W6BU-CENSUS** | 在庫表 cert `k5gen_w6_bu_census_<date>.json` | §7.3 の表を機械生成(**判定欄を持たない**) |

### 7.2 S0 assert 表(**不一致なら即停止 S-BU-1**)

| # | assert | 期待値 | 根拠 |
|---|---|---|---|
| **A-0** | $S_4$ における $\theta\tau$ の位数 | **4**($\theta=(1\,2)$、$\tau=(1\,3\,4)$) | 補題 GAMMA (a)・v1 §2.1 |
| **A-1** | $\lvert\widehat G_5\rvert/\lvert G_5\rvert/\lvert A\rvert$ | **3000 / 500 / 125** | 定義ノート §3 |
| **A-2** | $\widehat G_5/A\cong S_4$、$G_5/A\cong V_4=O_2(S_4)$ | true | ★ **VCEN-MOD の前提**(新設) |
| **A-3** | $\mathbf F_p[A]$ の非自明既約の次元 | **4**(全 31 個) | 補題 A-TRIV (a) |
| **A-4** | $\mathbf P^2(\mathbf F_5)$ 上の $S_4$-軌道の最小サイズ | **3** | 補題 A-TRIV (b) |
| **A-5** | $\dim H^2(S_4,\mathbf F_2)$(自明係数) | **2** | UCT |
| **A-9** ★新 | $\mathbf F_2[S_3]$ のブロック分解 / dim 2〜4 の加群個数 | **$\mathbf F_2C_2\times M_2(\mathbf F_2)$ / 3, 3, 6** | ★ 補題 F2S3(§6.1) |
| **A-10** ★新 | $K^{(20)}$ control: $\lvert G_{20}\rvert$ / $\lvert Z(G_{20})\rvert$ / $\lvert[G_{20},G_{20}]\rvert$ / $\lvert W\rvert$ / $\lvert V/W\rvert$ | **4000 / 8 / 250 / 2 / 4** | ★ erratum v2 §3.5(python 側)を **GAP で再現**(= 二系統化) |
| **A-11** ★新 | $2\mathbf Z^2$ の指数 2 部分格子で $\Gamma$-安定なものの個数 | **0** | ★ 補題 LAT-Γ(erratum v2 §2.2) |
| **A-12** ★新 | $K^{(20)}$ の $V$ が $S_3$-inflate($V_4$ 自明作用)か | **true** | ★ 定理 VCEN-MOD の較正(§2.2) |
| **A-13** ★新 | $\mathrm{Ext}^1_{\mathbf F_2S_3}(D,\mathbf F_2)$ | **0** | §6.2($\mathbf F_2\oplus D$ の一意性) |

> ⚠ **A-6/A-7(旧)= 障害群・dummy の較正は本発注に含めない**(kill 段の較正であり、限定認可の外)。

### 7.3 在庫表の様式(**判定欄を持たないこと**)

| 列 | 内容 |
|---|---|
| `module_id` | `p2_d3_a1b0c1` 形式(§6.1 の $(a,b,c)$) |
| `p`, `dim` | 標数と次元 |
| `s3_inflated` | **true/false**(= (V-cen) 層か。VCEN-MOD による) |
| `socle_structure` | 合成因子と不可分解分解 |
| `dim_H2_S4` | $\dim_{\mathbf F_p}H^2(S_4,V)$ ★ **計算対象の本体** |
| `dim_H2_S3` | $\dim_{\mathbf F_p}H^2(S_3,V)$(参考。$p=3$ では $H^2(S_4,V)\cong H^2(S_3,V)$ が成り立つはず — $\lvert V_4\rvert=4$ が $p=3$ で可逆) |
| `dim_H1_S4` | 参考(lift の自由度 $Z^1$ の見積り) |
| `window_order` | $500\cdot\lvert V\rvert$ |
| `band_note` | erratum v2 §2.5 の帯表のどこに落ちるか(**文字列のみ・棄却しない**) |
| `scope_out_reason` | 非初等核・$A$ 非自明・PSL 屋根は **`SCOPE_OUT` と明記**(「空」と書かない) |

### 7.4 停止規則(この発注に効くもの)

| # | trigger | verdict |
|---|---|---|
| **S-BU-1** | A-0〜A-13 のいずれか不一致 | `PREREGISTRATION_FALSIFIED / INTEGRITY_STOP`(S-7′ 逐語) |
| **S-BU-6** | 除外帯を「空だった」と書こうとした | `OVERCLAIM / STOP` |
| **S-BU-8** | 在庫表の規模が §6.1 の厳密値(3/3/6)と食い違った | `UNIVERSE_MISMATCH / STOP` — ★ **補題 F2S3 が偽**の可能性を第一容疑に |
| **S-BU-9** | campaign §2.2 の禁止量に触れざるを得なくなった | campaign **S-4** 逐語 |
| ★ **S-BU-10** 新 | 在庫表に**棄却・生存・EMPTY の語**が現れた | `SCOPE_VIOLATION / STOP`(限定認可の範囲外) |

### 7.5 非接触(この発注の全段)

$\mathrm{Im}\,R$ 非接触・$d_N$ 非評価・封印 3 量非接触・証明書非読。**inference-contact event(裁定 412)は発火しない。**

---

## 8. 【GAP】(新設・更新)

| 札 | 内容 | 状態 |
|---|---|---|
| **【BU-GAP-1】** | 非初等アーベル核($C_4$・$C_9$・非可換) | ★ **一部閉**(系 THETA-2000 が $\lvert V\rvert=4$ の $C_4$ 型も殺す)。**残りは SCOPE_OUT** |
| **【BU-GAP-2】** | GQuotients の取りこぼし | ★ **二系統突合で実地試験できる**ようになった(§5.1) |
| **【BU-GAP-3】** | $p=3$ で NC-2 が持上げ依存 | ★ **消える**(marked datum では $\rho$ が決まっている・§3.1) |
| **【BU-GAP-6】** | SAT 符号化と紙篩の同値性 | ★ **全数照合で閉じられる見込み**(§4.2 SM-4・宇宙が小さいため) |
| **【BU-GAP-7】** | 統計 v2 の層優先順位 | ★ **重要度低下**(層が 4 型しかない) |
| **【BU-GAP-8】** ★新 | **isolated 性を marked datum の段で判定できない**(定義ノート §2 の isolated は shadow 側の性質)。前件として持ち回るしかない | **UNKNOWN**(【W5-GAP-1】と同根) |
| **【BU-GAP-9】** ★新 | **非中心層で SURJ-GATE の両枝が外れる候補**の扱い。SCOPE_OUT にすると、その帯の悉皆性は**永久に主張できない** | **UNKNOWN**(【K5-GAP-W1】と同根) |
| **【K5-GAP-W1】** | 非中心版 SURJ | ★ **閉じない**(本書は Frattini 枝で部分的に迂回しただけ) |

---

## 9. 司令塔への申し送り

1. ★★★ **§7 の限定認可分は即発注可能**(S0 較正 + 在庫表)。**判定欄を持たない**ことと **S-BU-10** の新設が Sol の限定条件への対応。
2. ★★★ **宇宙が 4 型に落ちた**(§6.2)。⟹ v1 の U-2/U-3 は**再凍結が要る**が、それは在庫表の実測を見てから **v2 本体**で請求したい(本書は凍結を請求しない)。
3. ⚠ **S8.5(SAT)の降格提案は司令塔裁定を仰ぐ**(§4.3)。**研究者発案の段なので当方の権限で削らない。** 降格しない場合でも §4.1 の逐語述語と §4.2 の source-map 契約は必要。
4. ★★ **$p=3$ は cap 8000 の下で候補ゼロ**(erratum v2 系 THETA-4500)。掘るなら $\lvert PB_3/N\rvert\ge13{,}500$ ⟹ **cap の見直しか、$p=3$ の撤収か**の判断が要る。
5. ★ **A-10($K^{(20)}$ control)を GAP 側で再現**すると、erratum v2 の python 悉皆計算が**二系統化**する(CV-9 判読の入力になる)。**F102-6.2 の再検問とも直結する**ので優先度は高い。
6. ⚠ **本書は方針起草であり、Sol 承認前・司令塔認可前は 1 行も走らせない。**
