# W-6 掘削 BOTTOM-UP 設計 **v3** — F103-3.2 blocker 7 件の閉鎖

**状態札: `design / 走らせていない(本書の GAP 実行ゼロ)/ Sol 未承認 / 発火未認可 / 実測ゼロ / 封印 3 量非接触・Im R 非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05・**新設**(`w6_bottomup_design_v2.md` は**不改変**。v2 → v3 の差分は本書が正本)
- 委嘱: 司令塔 —「**BOTTOM-UP は v3 で blocker 7 を閉じよ**」(F103-3.2 の 1〜7 + scope 表の except 集合の書換)
- **入力正本**:
  - `sol/sol_reply_103_math30.md` **§2–§3**(F103-2.1 訂正裁定・F103-2.2 引用規約・F103-3.1 PASS 部・**F103-3.2 blocker 1〜7**・F103-3.3 差戻し裁定)
  - `docs/notes/w6_bottomup_design_v2.md`(v2)/ `docs/notes/w6_kill_theorems_v2_erratum.md`(erratum v2)/ `w6_kill_theorems_v1.md` / `k5_w6_construction_v1.md` / `addendum_b_k20paper`
  - **既走 cert 2 本**(限定認可分・本書が格付けを訂正する対象):
    - `search/certs/k5gen_w6_bu_s0_20260805.json`(SHA-256 `0fba174308f53c6c1c45f4785e05bba4790807f450d7b234372829e688f50cf1`・`fails_total`=0)
    - `search/certs/h2_census_s4_20260805.json`(SHA-256 `4b8673209d55c46fe1bc01a1e2736df03f296cd7d775df6da98f8f582df73b30`・`row_count`=17・`fails_total`=0・`tier`=`inventory-census`)
  - `docs/week1-定義ノート.md` §1〜§3(**isolated の定義**・$x=\sigma_1^2$、$y=\sigma_2^2$、$c=\Delta^2$)
- **外部文献ゼロ。**

> ## 非接触の申告
> **本書は 1 行も実行していない**(GAP 起動ゼロ・python 実行ゼロ)。$\mathrm{Im}\,R_{N,K^{(5)}}$ 非接触・$d_N$ 非評価・封印 3 量非接触・**証明書は上記 2 本の構造欄(`row_count` / `asserts` 名 / `scope_out` / `stop_rule_status`)のみを読み、数学的測定値は読んでいない**。PSL 屋根は宇宙から除外(campaign X-4)。

---

## 0. 判定(blocker 7 件 × 閉じ方)

| # | F103-3.2 の blocker | 本書での閉じ方 | 節 |
|---|---|---|---|
| **1** | marked datum の同値関係が未定義(「1 対 1」が presentation 依存) | ★ **定義 MARK-ISO**($\widehat G_5$ 上 base-fixed: $\varphi\circ\rho=\rho'$)+ **補題 MARK-BIJ**(全単射の証明)。$\pi'\circ\varphi=\pi$ は $\rho$ 全射から**自動**であることも証明 | §1 |
| **2** | $\delta_{\rm roof}$ の型が全 marked datum 上で未定義 | ★ **roof data を型に含める**: $\mathrm{Roof}(\mathcal D)=\{U\trianglelefteq\widehat P: U\cap V=1,\ f_1\in\text{im}(U\cap P)\}$ を定義し、$\delta_{\rm roof}:\mathrm{Roof}(\mathcal D)\to V/W$ を**関数として**定義。$\mathrm{Roof}=\emptyset$ は `ROOF_VACUOUS`(「屋根でない」と書かない) | §2 |
| **3** | SAT 述語に roof 条件節がない | ★ 述語を**書き直し**、$\bigwedge_{U}(\text{RoofApplicable}(U)\rightarrow\delta_{\rm roof}(U)\ne0)$ と **ISO 旗**を連言に追加。source-map タグに `roof` / `iso` を新設 | §3 |
| **4** | L-4 の isolated が未検査・fail-closed gate なし | ★ **ISO-GATE**(既定 `ISOLATED_UNKNOWN` = fail-closed)を S3.5 直後・S4′ 直前に設置。UNKNOWN は **kill 禁止・候補主張禁止・EMPTY 寄与禁止**(在庫には残す)。**S-BU-11** 新設 | §4 |
| **5** | 非中心層 = 認可宇宙の縮小か列挙か未決 | ★ **正式に縮小**(司令塔推奨を採る)。宇宙 **U-2′/U-3′ = (V-cen) 層のみ**。非中心層は `SCOPE_OUT`(`NOT_ENUMERATED_THIS_PASS` から格上げ)。**理由 3 点を明記**し、以後の悉皆・下限主張に前件として必ず付す | §5 |
| **6** | S0 の分母が誤記(A-0〜A-13 全 14 項) | ★ **登録 assert = 11 項**(A-0〜A-5 + A-9〜A-13)と確定。**A-6/A-7/A-8 は明示的に範囲外**。S-BU-1 の trigger 文を差替。既走 cert の `stop_rule_status` 文字列は**新版 cert で訂正**(過去 cert 不改変) | §6 |
| **7** | census 17 行の格・p=3 の一般化・scope 表の except 集合 | ★ 格 = **単一 lane candidate inventory**(`cross-checked census` と呼ばない)。p=3 の結論は **(V-cen) 層・列挙範囲内**限定。scope 表の除外集合を **`exponent > p or nonabelian core`** へ書換(**非巡回初等アーベル核は射程内**) | §7 |

> ### ★ F103-2.2 の引用規約(本書全体に効く)
> $$\boxed{\ \textbf{下限「}p=2\textbf{ で 4,000 / }p=3\textbf{ で 13,500」は }c\in N\ \wedge\ \textbf{(V-cen)}\ \wedge\ \textbf{isolated}\ \wedge\ \textbf{当該 }p\textbf{-primary 枝}\ \textbf{の下での下限である。無条件下限として引用しない。}\ }$$
> 本書で下限に言及する箇所には、この 4 前件を**毎回**併記する(§5.3・§7.3)。

---

## 1. 【blocker 1】marked datum の同値関係

### 1.1 定義 MARK-ISO

v2 §3.1 の marked datum $\mathcal D=(V,\widehat P,\rho)$($\pi_{\widehat P}\circ\rho=q$、$\rho$ 全射、$\rho(c)=1$)に対し:

> ### 定義 MARK-ISO(本書)
> $\mathcal D=(V,\widehat P,\rho)$ と $\mathcal D'=(V',\widehat P',\rho')$ が **marked 同型**($\mathcal D\cong\mathcal D'$)であるとは、群同型 $\varphi:\widehat P\to\widehat P'$ が存在して
> $$\textbf{(M-a)}\ \ \varphi\circ\rho=\rho',\qquad\qquad \textbf{(M-b)}\ \ \pi_{\widehat P'}\circ\varphi=\pi_{\widehat P}\quad(\textbf{基底 }\widehat G_5\textbf{ 上})$$
> が成り立つことをいう。**基底は固定する**($\widehat G_5$ の自己同型による twist は同値に含めない)。

> ### 補題 MARK-ISO-a(**(M-b) は自動**)
> $\rho$ が全射ならば **(M-a) ⟹ (M-b)**。
> **証明.** $(\pi_{\widehat P'}\circ\varphi)\circ\rho=\pi_{\widehat P'}\circ\rho'=q=\pi_{\widehat P}\circ\rho$。$\rho$ 全射ゆえ $\pi_{\widehat P'}\circ\varphi=\pi_{\widehat P}$。∎
> ⟹ **実装では (M-a) だけを検査すればよい**(検査コストが半分になる)。また $\varphi(V)=\varphi(\ker\pi_{\widehat P})=\ker\pi_{\widehat P'}=V'$ も従うので、**$V$ の同一視は $\varphi\vert_V$ が誘導する**(加群の同一視を別に指定しなくてよい)。

### 1.2 補題 MARK-BIJ(「1 対 1」の**証明**)

> ### 補題 MARK-BIJ(candidate・本書)
> $\mathcal W:=\{N\trianglelefteq B_3\ :\ N\subseteq K^{(5)},\ c\in N,\ [K^{(5)}:N]<\infty\}$ と置く。写像
> $$\ker:\ \{\text{marked datum}\}/\!\cong\ \longrightarrow\ \mathcal W,\qquad [\mathcal D]\longmapsto\ker\rho$$
> は**全単射**である。

**証明.**
**well-defined**: $\mathcal D\cong\mathcal D'$ なら (M-a) より $\ker\rho=\ker(\varphi\circ\rho)=\ker\rho'$($\varphi$ 単射)。
**単射**: $\ker\rho=\ker\rho'=:N$ とする。$\varphi:\widehat P\to\widehat P'$ を $\varphi(\rho(b)):=\rho'(b)$ で定義すると、$\ker\rho\subseteq\ker\rho'$ より well-defined、$\rho'$ 全射より全射、$\ker\rho'\subseteq\ker\rho$ より単射。(M-a) は定義そのもの。⟹ $\mathcal D\cong\mathcal D'$。
**全射**: $N\in\mathcal W$ に対し $\widehat P:=B_3/N$、$\rho:=$ 標準射影と置く。$N\subseteq K^{(5)}$ ゆえ $\pi_{\widehat P}\circ\rho=q$ を満たす $\pi_{\widehat P}$ が存在し、$\rho$ は全射、$c\in N$ ゆえ $\rho(c)=1$。$V=\ker\pi_{\widehat P}=K^{(5)}/N\cong K^{(5)}_{F_2}/N_{F_2}$($c\in N$ を使う・v2 §3.1)。⟹ $\ker\rho=N$。∎

> ### ★ なぜ base-fixed か(**設計判断の理由を明記**)
> $\mathrm{Aut}(\widehat G_5)$ による twist を同値に含めると、対応先は $\mathcal W$ ではなく **$\mathcal W$ の $\mathrm{Aut}$-軌道**になる。本設計が数えたいのは**窓 $N$ そのもの**(そこから $N_{F_2}$・$\alpha(N_{F_2})$・$\bar x,\bar y$ が定まる)なので、**base-fixed が正しい**。⟹ 「1 対 1」は presentation 依存ではなくなった。
> ⚠ その代償として、**同じ抽象拡大類 $[\varepsilon]$ から複数の非同値な marked datum が出る**(lift の自由度)。これは v2 §3.2 の $\lvert V\rvert^2$ 総当りが数えている自由度そのものであり、**S3.5 の出力は「類」ではなく「窓」である**。

---

## 2. 【blocker 2】$\delta_{\rm roof}$ の型を全 marked datum 上で定義する

### 2.1 定義 ROOF-DATA

> ### 定義 ROOF-DATA(本書)
> marked datum $\mathcal D=(V,\widehat P,\rho)$ に対し、その **roof presentation の集合**を
> $$\mathrm{Roof}(\mathcal D):=\Bigl\{\,U\trianglelefteq\widehat P\ \Bigm|\ U\cap V=1,\ \ \text{かつ}\ \ f_1\in\mathrm{im}\bigl(U\cap P\to G_5\bigr)\,\Bigr\}$$
> と定める($P=\rho(PB_3)$、$\pi:P\to G_5$)。各 $U\in\mathrm{Roof}(\mathcal D)$ に対し $N':=\rho^{-1}(U)$ と置く。

> ### 補題 ROOF-TYPE(candidate・本書)
> $U\trianglelefteq\widehat P$ が $U\cap V=1$ を満たすとき、$N'=\rho^{-1}(U)$ は
> **(a)** $N'\trianglelefteq B_3$、$c\in N'$、$N\subseteq N'$;
> **(b)** $K^{(5)}\cap N'=N$;
> **(c)** $\ker(P\to PB_3/N')=U\cap P$ であり、$V\cap(U\cap P)=1$。
> したがって $\mathcal D$ と $U$ から **v1 定理 ROOF-KILL §4.1 の設定**($N'$、$G'=PB_3/N'$、$D=PB_3/(K^{(5)}N')$)が**一意に復元される**。
> さらに $U\in\mathrm{Roof}(\mathcal D)$ ならば $\pi^{-1}(f_1)\cap(U\cap P)$ は**ちょうど 1 元**からなる。これを $u_{f_1}$ と書く(= ROOF-KILL の $(f_1,1)$)。

**証明.**
(a) $U\trianglelefteq\widehat P$ と $\rho$ 全射から $N'\trianglelefteq B_3$。$\rho(c)=1\in U$ ゆえ $c\in N'$。
(b) $K^{(5)}\cap N'\supseteq N$ は明らか。$\rho(K^{(5)}\cap N')\subseteq V\cap U=1$ ⟹ $K^{(5)}\cap N'\subseteq\ker\rho=N$。
(c) 定義から。$V\cap(U\cap P)\subseteq V\cap U=1$。
**一意性**: $\pi^{-1}(f_1)$ は $V$ の剰余類。$x_1,x_2\in\pi^{-1}(f_1)\cap(U\cap P)$ なら $x_1^{-1}x_2\in V\cap(U\cap P)=1$。**存在**は $\mathrm{Roof}$ の第 2 条件(=「$f_1$ の $D$ における像が自明」の言い換え)。∎

> ### ★ 第 2 条件の言い換えと十分条件
> $D=PB_3/(K^{(5)}N')\cong G_5/\mathrm{im}(U\cap P)$ なので、「$f_1$ の $D$-像が自明」⟺「$f_1\in\mathrm{im}(U\cap P)$」⟺ 定義の第 2 条件 ✓。
> **十分条件(v1 §4.2 (b))**: $5\nmid\lvert D\rvert$。$f_1$ の位数が 5 だからである。

### 2.2 $\delta_{\rm roof}$ の型

> ### 定義 DELTA-ROOF(v1 §4.2 (d) の型付け)
> $$\boxed{\ \delta_{\rm roof}(\mathcal D,\cdot):\ \mathrm{Roof}(\mathcal D)\longrightarrow V/W,\qquad U\longmapsto\bigl[\widetilde f_0^{\,-1}\,u_{f_1}\bigr]\ }$$
> ($\widetilde f_0\in\mathcal L=\pi^{-1}(f_1)\cap[P,P]$ は任意 — 取り替えは $W$ ぶんの差で、$V/W$ では不変)。
> $$\textbf{S8 の述語}:\quad \textbf{KILL}\iff\exists\,U\in\mathrm{Roof}(\mathcal D):\ \delta_{\rm roof}(\mathcal D,U)=0 .$$

> ### ⚠ 空の場合の扱い(**過剰主張の防止**)
> $\mathrm{Roof}(\mathcal D)=\emptyset$ のとき S8 は**空虚に真**(kill しない)。この行は **`ROOF_VACUOUS`** と記帳し、**「屋根で書けない」「屋根型ではない」とは書かない**($\mathrm{Roof}$ は本設計の列挙手続きが見つけた範囲であって、$N'$ の非存在の証明ではない)。**S-BU-12** で保護する(§8)。

### 2.3 $\mathrm{Roof}(\mathcal D)$ の列挙(有限・安い)

$U\trianglelefteq\widehat P$ かつ $U\cap V=1$ ⟹ $[U,V]\subseteq U\cap V=1$ ゆえ $U$ は $V$ を中心化し、$U\hookrightarrow\widehat P/V\cong\widehat G_5$ は**単射**で像は $\widehat G_5$ の正規部分群。⟹

$$\boxed{\ \mathrm{Roof}(\mathcal D)\ \textbf{の列挙は }\widehat G_5\ (\text{位数 }3000)\ \textbf{の正規部分群のリストからの持上げ検査に帰着する。}\ }$$

**手続き**: (i) `NormalSubgroups(Ĝ₅)` を一度だけ計算(層に依らない前計算)(ii) 各 $\bar U$ に対し $\widehat P$ 内の持上げ $U$($U\cap V=1$・$U\trianglelefteq\widehat P$)を探す (iii) 第 2 条件($f_1\in\mathrm{im}(U\cap P)$)を検査。**コストは秒オーダー**(v2 §6.3 の見積りを変えない)。

---

## 3. 【blocker 3】SAT 述語 v2(roof 条件節を含む)

### 3.1 述語(**v2 §4.1 の boxed を差し替える**)

層 $\mathcal S(V)$ に対し、SAT が判定する命題:

$$\boxed{
\begin{aligned}
\exists\,[\varepsilon]\in H^2(S_4,V)\ \ \exists\,\rho\in\mathrm{Lift}(q,\widehat P_{[\varepsilon]})\ :\ \ 
&\underbrace{\mathrm L1\wedge\mathrm L2\wedge\mathrm L3}_{\text{marked}}\ \wedge\ \underbrace{\mathrm{ISO}(\mathcal D)=\texttt{PROVEN}}_{\text{§4}}\ \wedge\ \underbrace{\mathrm{SURJGATE}(\mathcal D)}_{\text{v2 §2.3}}\\
\wedge\ &\underbrace{\mathrm{NC}\text{-}2'\ \wedge\ (W\ne0)\ \wedge\ (\operatorname{coker}\psi_W\ne0)\ \wedge\ (\text{障害類}\ne0)}_{\text{S4}'\text{--S7}}\\
\wedge\ &\underbrace{\bigwedge_{\bar U\in\mathrm{RoofCand}}\Bigl(\mathrm{RoofApplicable}(\bar U,\mathcal D)\ \longrightarrow\ \delta_{\rm roof}(\mathcal D,U_{\bar U})\ne0\Bigr)}_{\textbf{S8(新設)}}
\end{aligned}}$$

- $\mathrm{RoofCand}$ := $\widehat G_5$ の正規部分群の**層に依らない前計算リスト**(§2.3)。
- $\mathrm{RoofApplicable}(\bar U,\mathcal D)$ := 「$\bar U$ が $U\cap V=1$ の持上げをもち、かつ $f_1\in\mathrm{im}(U\cap P)$」。**含意形**にすることで、$\mathrm{Roof}(\mathcal D)=\emptyset$ の datum が誤って落ちない。
- **変数**: (i) $[\varepsilon]$ の座標 (ii) $\rho(\sigma_1),\rho(\sigma_2)$ の $V$-成分($2\dim V$) (iii) 補助($\widetilde f_0$ の $W$-成分・$\beta_\theta,\beta_\tau$・**各 $\bar U$ の持上げ座標**)。

### 3.2 source-map 契約の更新(v2 §4.2 SM-1 の差替)

| タグ | 由来 |
|---|---|
| `lift` | L-1 / L-2 / L-3(§v2 3.2) |
| `iso` ★新 | ISO-GATE(§4) |
| `surj` | SURJ-GATE(v2 §2.3) |
| `lattice` | NC-2′(erratum v2 §2.3) |
| `w` / `coker` / `class` | S5 / S6 / S7 |
| `roof` ★新 | S8(§3.1 の含意節。**$\bar U$ ごとに節群を分け、$\bar U$ の id をタグに含める**) |

**SM-2〜SM-4 は v2 のまま**。ただし **SM-4(紙篩との全数照合)には roof 条件を必ず含める**(含めない照合は【BU-GAP-6】を閉じない)。

> ⚠ **SAT の位置づけは v2 §4.3 のまま(第 2 系統の照合レーン・critical path 外)**。F103-3.1 で「SAT を critical path から独立照合 lane へ降格する方向も正しい」と PASS を得ている。

---

## 4. 【blocker 4】ISO-GATE(fail-closed)

### 4.1 何が問題か

**isolated**(定義ノート §2)= 「$N$ の全 GT-shadow が settled」であり、**marked lift の段では判定できない**(shadow 側の性質であって、群構造だけからは出ない)。一方 **命題 K5-BIT の窓の前件に isolated が入っている**(v1 §1.1)ので、**S4′〜S8 の kill はすべて isolated に依存する**。v2 の L-4 はこれを「判定しない」と書いただけで gate がなかった。

### 4.2 定義 ISO-GATE

> ### 定義 ISO-GATE(fail-closed・本書)
> 各 marked datum $\mathcal D$ に状態 $\mathrm{ISO}(\mathcal D)\in\{\texttt{PROVEN},\texttt{UNKNOWN}\}$ を付す。**既定値は `UNKNOWN`**。
> **`PROVEN` を付けてよいのは次だけ**:
> 1. $\ker\rho=K^{(n)}$ の形(正典 Thm 4.3 が $K^{(n)}$ の isolated 性を与える)。
> 2. 将来、isolated 判定の専用手続きが設計・較正された場合、その cert が PASS を出したもの(**現時点では存在しない**)。
>
> $$\boxed{\ \mathrm{ISO}(\mathcal D)=\texttt{UNKNOWN}\ \Longrightarrow\ \textbf{kill 禁止・候補主張禁止・EMPTY-THM 寄与禁止。ただし在庫行としては残す。}\ }$$

**設置位置**: **S3.5(marked lift)の直後・S4′ の直前**。理由: S4′ 以降はすべて K5-BIT 経由の kill であり、その前件に isolated が入っているから。

### 4.3 停止規則

| # | trigger | verdict |
|---|---|---|
| **S-BU-11** ★新 | $\mathrm{ISO}(\mathcal D)=\texttt{UNKNOWN}$ の候補について kill / 候補発見 / EMPTY 寄与を書こうとした | `ISOLATED_UNVERIFIED / STOP` |

> ⚠ **実務上の帰結を先に書いておく**(S-8 の趣旨): 本設計が列挙する窓は一般に $K^{(n)}$ の形ではないので、**現時点では ISO-GATE を通る候補はほぼ存在しない**。⟹ **S4′〜S8 は当面「在庫の注記」しか生まない**。これを承知の上で v3 を出す。**isolated 判定手続きの設計が、W-6 掘削の実質的な次の律速である**(§9-3)。

---

## 5. 【blocker 5】認可宇宙の正式縮小(**縮小を採る**)

### 5.1 縮小後の宇宙

> ### U-2′ / U-3′(v1 U-2/U-3 の差替)
> $$\boxed{\ \textbf{列挙宇宙}\ :=\ \textbf{(V-cen) 層のみ}\ =\ \{V\ :\ V\ \textbf{は}\ S_4\twoheadrightarrow S_3\ \textbf{から inflate された }\mathbf F_p[S_4]\textbf{-加群}\}\ }$$
> - **U-2′**: $p=2$、$\dim_{\mathbf F_2}V\in\{2,3,4\}$、$S_3$-inflate。
> - **U-3′**: $p=3$、$\dim_{\mathbf F_3}V=2$、$S_3$-inflate。
> - **非中心層($V_4$ が非自明作用)**: **`SCOPE_OUT`**(`NOT_ENUMERATED_THIS_PASS` から格上げ)。

### 5.2 縮小の理由(**3 点・明記が blocker の要求**)

1. **kill が原理的に無認可**: 非中心層では (V-cen) が破れ、SURJ-GATE の第 1 枝が使えない。第 2 枝($V\subseteq\Phi(P)$)は **marked datum 上の述語**であって**加群水準の census では層別できない**。⟹ 加群 census に非中心行を並べても、その行から先へ進む認可がない(【K5-GAP-W1】未閉)。
2. **在庫の意味が変わる**: 使えない層を宇宙に残したまま「在庫表を完了した」と書くと、**悉皆主張の前件が曖昧になる**。事前登録規律(S-7′)は、宇宙を**明示的に**縮小することを要求する。
3. **費用対効果**: 非中心層の $\mathbf F_p[S_4]$-加群は有限表現型の保証がない($p=2$ で $S_4$ は $\mathbf F_2$ 上 wild ではないが、$V_4$ 非自明作用の分だけ型が増える)。**列挙コストが増える一方で、出口がない。**

### 5.3 縮小の代償(**主張の縮小である**)

$$\boxed{\ \textbf{以後の悉皆・下限・EMPTY 主張はすべて「(V-cen) 層の中で」という前件を持つ。}\ }$$

- erratum v2 の下限(4,000 / 13,500)は、F103-2.2 の 4 前件($c\in N$・(V-cen)・isolated・当該 $p$ 枝)**に加えて**、本縮小の前件を持つ。
- 非中心層について「空」「無い」とは**書かない**(**S-BU-6** 継続)。
- 既走 cert `h2_census_s4_20260805.json` の `scope_out` にある `NOT_ENUMERATED_THIS_PASS` 行は、**新版 census cert で `SCOPE_OUT (universe narrowed by design v3 §5)` へ書き換える**(**過去 cert は不改変**)。

---

## 6. 【blocker 6】S0 の分母訂正

### 6.1 登録 assert = **11 項**(確定)

$$\boxed{\ \textbf{A-0,\ A-1,\ A-2,\ A-3,\ A-4,\ A-5,\ A-9,\ A-10,\ A-11,\ A-12,\ A-13}\quad(\textbf{計 11 項})\ }$$

**A-6 / A-7 / A-8 は明示的に範囲外**である(A-6 = 障害群 control、A-7 = dummy ソルバ較正、A-8 = SAT encoder の mutant matrix — いずれも **kill 段/SAT 段の較正**であり、限定認可 = S0 較正 + 在庫表 の外)。

### 6.2 S-BU-1 の trigger 文(差替・逐語)

| # | trigger(v3) | verdict |
|---|---|---|
| **S-BU-1** | **§6.1 の 11 項のいずれかが不一致** | `PREREGISTRATION_FALSIFIED / INTEGRITY_STOP`(S-7′ 逐語) |

### 6.3 既走 cert の訂正(**過去 cert は不改変**)

`search/certs/k5gen_w6_bu_s0_20260805.json` の `stop_rule_status` は
`"S0_PASS -- all A-0..A-13 asserts match design v2 §7.2 expected values"`
であり、**分母の誤記**(A-6〜A-8 を含む範囲として読める)。

- **実測値そのものは全項 PASS**(`fails_total`=0)で、**数学的な影響はない**。
- **処置**: cert は不改変。**新版 cert で `"S0_PASS -- all 11 registered asserts (A-0..A-5, A-9..A-13) match design v3 §6.1; A-6..A-8 are out of scope"` へ訂正**(ep-keeper 案件)。**`asserts` 配列の実体は 18 エントリで A-6〜A-8 を含んでいない**ので、訂正は文字列 1 本で足りる。

---

## 7. 【blocker 7】census の格・p=3 の射程・scope 表

### 7.1 格(**確定**)

> $$\boxed{\ \texttt{h2\_census\_s4\_20260805.json}\ (\text{17 行})\ \textbf{の格} = \textbf{単一 lane candidate inventory}\ }$$
> - $H^2(S_4,V)$ は **1 実装のみ**で計算されている(第 2 系統なし)。⟹ **`cross-checked census` と呼ばない。**
> - **判定欄を持たない**(`tier`=`inventory-census`・`scope_statement` が S-BU-10 準拠を明記)。⟹ kill / 候補発見 / EMPTY-THM のいずれにも使わない。
> - **`verified` は論外**(Lean なし)。

### 7.2 17 行の内訳と、紙側の閉形式

| 帯 | 行数 | 紙側の根拠 | 機械との関係 |
|---|---|---|---|
| $p=2$、$\dim=2,3,4$ | **3 / 3 / 6 = 12** | ★ **補題 F2S3**(v2 §6.1・F103-3.1 で PASS)の閉形式 | cert の `p2_dim2_3_4_count_cross_check_vs_A9` が `expected [3,3,6] / measured_total 12` で一致 |
| $p=3$、$\dim=2$ | **5** | ★ **本書 §7.2.1**(新)。cert は「設計文書に閉形式なし・$GL(2,3)$ 悉皆総当りで測定」と注記していた | ★ **紙側の閉形式を後から供給する**(下記) |
| **計** | **17** | | |

#### 7.2.1 ★ 補題 F3S3(candidate・本書 — cert の $p=3$ 行 5 に紙の根拠を与える)

> $\mathbf F_3[S_3]$ は $O_3(S_3)=A_3\cong C_3$ を巡回 Sylow 3-部分群にもつ。単純加群は $S_3/O_3(S_3)\cong C_2$ のもの、すなわち **自明 $\mathbf 1$ と符号 $\mathrm{sgn}$**(ともに 1 次元)。Cartan 行列 $\begin{psmallmatrix}2&1\\1&2\end{psmallmatrix}$ より射影被覆は $P(\mathbf 1)=\mathbf 1\vert\mathrm{sgn}\vert\mathbf 1$、$P(\mathrm{sgn})=\mathrm{sgn}\vert\mathbf 1\vert\mathrm{sgn}$(ともに 3 次元・uniserial)。$\mathbf F_3S_3$ は **serial(Nakayama)代数**で、不可分解加群は射影被覆の商 **6 個**($\mathbf 1$, $\mathbf 1\vert\mathrm{sgn}$, $P(\mathbf 1)$, $\mathrm{sgn}$, $\mathrm{sgn}\vert\mathbf 1$, $P(\mathrm{sgn})$)。
> ⟹ **$\dim=2$ の加群は**: 分解型 $\mathbf 1\oplus\mathbf 1$、$\mathbf 1\oplus\mathrm{sgn}$、$\mathrm{sgn}\oplus\mathrm{sgn}$ の 3 個 + 不可分解 $\mathbf 1\vert\mathrm{sgn}$、$\mathrm{sgn}\vert\mathbf 1$ の 2 個 = $\boxed{5}$。

⟹ cert の `p3_dim2_measured_count`=5 と**一致**。
⚠ **ただし `cross-checked` とは書かない**: 紙(本補題)と機械($GL(2,3)$ 総当り)は別系統だが、**CV-9 非当事者判読を経ていない**(v1/v2 と同じ規律)。**「二系統の第 1 歩」までである。**

### 7.3 p=3 についての一般化禁止

$$\boxed{\ \textbf{「}p=3\textbf{ は cap 8000 の下で候補ゼロ」は、(V-cen) 層・}\dim_{\mathbf F_3}V=2\ \textbf{・本 pass の列挙範囲の中でのみ言える。}\ }$$
- $\dim_{\mathbf F_3}V\ge3$ は**列挙していない**(cap 8000 の外)。
- 非中心層は `SCOPE_OUT`(§5)。
- erratum v2 の $p=3$ 下限 13,500 は F103-2.2 の 4 前件つき。
⟹ **「$p=3$ には W-6 が無い」とは書かない**(**S-BU-6** 逐語)。

### 7.4 scope 表の除外集合の書換(**逐語**)

| 旧(cert `scope_out`) | ★ 新(v3 で採る文言) |
|---|---|
| `non_elementary_abelian_core (C4,C9,noncyclic)` | ★ **`core_exponent_gt_p_or_nonabelian`** — 説明: 「**核 $V$ の指数が $p$ を超える($C_4$、$C_9$ 等)、または核が非アーベル**」 |

> ⚠ **旧文言は「非巡回」を除外集合に読み込ませる誤り**を含んでいた。**非巡回の初等アーベル核($\mathbf F_2^2$、$\mathbf F_2^3$ 等)は射程内**である — 実際、既知の唯一の実物 $K^{(20)}$ の $V\cong\mathbf F_2^3$ は非巡回初等アーベルであり、**本設計の中心的な対象**である。
> **処置**: 過去 cert は不改変。新版 census cert で文言を差し替える(ep-keeper 案件)。

---

## 8. 段の再構成 v3(v2 §3.3 の差替)

| 段 | 名 | v3 での内容 | 変更 |
|---|---|---|---|
| **S0** | 較正 | **11 項**(§6.1) | ★ 分母訂正 |
| **S1** | 宇宙(加群) | **(V-cen) 層のみ**(U-2′/U-3′) | ★ 正式縮小(§5) |
| **S2** | 位数 | erratum v2 の下限(**4 前件つき**) | ★ 引用規約(§0) |
| **S3** | 拡大類 | $H^2(S_4,V)$ 全類 | 不変 |
| **S3.5** | marked lift | L-1〜L-3(**同値は MARK-ISO**・§1) | ★ 同値関係を定義 |
| **S3.6** ★新 | **ISO-GATE** | `PROVEN` / `UNKNOWN`(fail-closed) | ★ 新設(§4) |
| **S4′** | 格子 | NC-2′ | 不変 |
| **S5 / S6 / S7** | $W\ne0$ / coker / 障害類 | 不変 | 不変 |
| **S8** | 屋根 | **$\mathrm{Roof}(\mathcal D)$ 上の $\delta_{\rm roof}$**(§2)。空なら `ROOF_VACUOUS` | ★ 型を定義 |
| **S8.5** | SAT | §3 の述語(roof 節つき)・**critical path 外の照合レーン** | ★ 述語更新 |
| **S9** | GQuotients | ★ **別ゲート継続**(F103-3.3)。S3.5 の第 2 系統 | 不変 |

### 停止規則(v3 追加分)

| # | trigger | verdict |
|---|---|---|
| **S-BU-11** ★新 | ISO `UNKNOWN` のまま kill / 候補 / EMPTY 寄与 | `ISOLATED_UNVERIFIED / STOP` |
| **S-BU-12** ★新 | $\mathrm{Roof}(\mathcal D)=\emptyset$ を「屋根型でない」と書こうとした | `OVERCLAIM / STOP`(`ROOF_VACUOUS` と記帳する) |
| **S-BU-13** ★新 | census / 在庫表を `cross-checked` と格付けしようとした | `GRADE_OVERCLAIM / STOP`(§7.1) |
| S-BU-1〜10 | v2 のまま(S-BU-1 の trigger 文のみ §6.2 で差替) | — |

---

## 9. 【GAP】更新と申し送り

| 札 | 内容 | 状態 |
|---|---|---|
| **【BU-GAP-8】**(更新) | **isolated 判定手続きそのものが未設計**。ISO-GATE は fail-closed の受け皿であって、判定器ではない | ★ **UNKNOWN(実質的な次の律速)** |
| **【BU-GAP-9】**(更新) | 非中心層は宇宙から**正式に外れた**(§5)。⟹ その帯の悉皆性は**構造的に主張できない** | **設計判断として確定**(【K5-GAP-W1】は未閉のまま) |
| **【BU-GAP-10】** ★新 | $\mathrm{Roof}(\mathcal D)$ の列挙が**すべての** $N'$ を捕まえる保証(§2.3 は $\widehat P$ 内の正規部分群として捕まえるので、$N\subseteq N'$ でない屋根は原理的に射程外) | **UNKNOWN**(S-BU-12 が保護する) |
| **【BU-GAP-6】**(更新) | SAT 符号化と紙篩の同値性 — **roof 節を含めた全数照合**で閉じる設計(SM-4) | **UNKNOWN(手順は確定)** |

**司令塔への申し送り**

1. ★★★ **ISO-GATE を入れた結果、S4′〜S8 は当面ほぼ発火しない**(§4.3 の警告)。⟹ **isolated 判定手続きの設計**が W-6 掘削の次の律速。**これを次便の設計委嘱に載せるかの判断**を仰ぐ。
2. ★★ **新版 cert 2 本の起票が要る**(ep-keeper 案件・いずれも**過去 cert 不改変**): (a) S0 cert の `stop_rule_status` 文字列訂正(§6.3)(b) census cert の `scope_out` 文言差替(§5.3 の `SCOPE_OUT (universe narrowed)` + §7.4 の `core_exponent_gt_p_or_nonabelian`)。**測定値の再走は不要**(値は全項 PASS のまま)。
3. ★ **補題 F3S3**(§7.2.1)は cert の $p=3$ 行 5 に紙の根拠を与える新しい小補題。**Sol 監査対象**に載せられたい。
4. ⚠ **本書は凍結も発火も請求しない。** F103-3.3 の差戻しに対する blocker 閉鎖のみ。凍結請求は、ISO-GATE の見通し(申し送り 1)が付いてから **v4** で行う。
