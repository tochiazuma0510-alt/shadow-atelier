# 整錐 ④ 設計 v1 — Brown (7.8) の整数化と「一つの対象の捩れが両方を支配する」複体(裁定 749/751/752 合流・相 2 第一委嘱)

**状態札: `design + paper proof / all candidate / Sol 未監査 / GAP 実走ゼロ・cert 発行ゼロ / 封印非接触 / 新規 S 形成なし / 判定語の発効は司令塔専権 / 実走は仕様化まで`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-07 / 委嘱: 司令塔(裁定 **749**(二相戦略)・**749 補記**(④ の両刃性・等値化)・**751**(三分法)・**752**(triage 検収))
- 入力正本: `docs/scout/brown_eq14_verbatim_v1.md`(§2.4 の (7.8)・§2.5 の $\mathrm{Lie}_4(D_1)=0$・p.25 の重み 16/18/20 行)/ `docs/scout/brown_prop64_lattice_verbatim_v1.md`(**§2.3 格子 UNKNOWN**・**§2.1「$e$ は $\mathbf Z$ 上定義」**・**§3 の p.6 逐語**)/ `tor_sweep_design_v1.md`+追補 A,B / `weight_family_spectroscopy_design_v1_addendum_fgap3.md`(**命題 FG-2**)/ LEDGER 745–752
- **自前検算**: §3 の次元・確率の会計は python(整数・分数のみ・GAP 不使用・cert ではない)。再現コマンドは §3.4。

---

## 0. 判定(先に 7 行)

| # | 事項 | 結果 |
|---|---|---|
| **①** | **整複体の定義** | (7.8) を **ls(深さ次数付き)世界**で整数化し、深さ 4 層を**連結写像 $\rho_k$**(深さフィルトレーションの $d_1$)として接続。★ **$\rho_k=c_k\cdot e$、$c_k=\mathrm{num}(B_k)/\text{分母}$**(Brown p.25)⟹ **こだまは「$\rho_k$ の単因子」として自動的に出る**(§1) |
| **②** ★★★ | **「一つの対象の捩れが両方を支配する」の精密文** | $\mathrm{coker}(\iota_{k,r})$ の $p$-捩れ $\iff$ ∃$v\in\mathrm{ls}^{\mathbf Z}$:$pv$ は括弧だが $v$ は括弧でない $\iff$ **A 側から見れば括弧代数の縮み・S 側から見れば例外部分の伸び**。**同一の捩れの二つの読み**(§2.2) |
| **③** ★★★ | **捩れを殺す構造の有無(両刃の検査)** | ★ **殺す構造は存在しない — 反例が実物である**:$(12,691)$ で $\mathrm{coker}(\rho_{12})\ne0$。⟹ 双対性・Euler 標数はいずれも**捩れゼロを与えない**(§2.3)。**問いは「捩れがあるか」でなく「こだま分で尽きるか」**(裁定 749 補記③ と一致) |
| **④** ★★★ | **等値化の最終形** | $$\textbf{井原予想の }p\textbf{-進の運命}\iff \textbf{Brown の }e:\mathsf P_k\to(\mathrm{ls}_4/L_4)_k\ \textbf{が }\mathbf Z\ \textbf{上飽和か}$$ ★ **$k=12$ は Brown の明示整生成元($f_{12}$・$\bar e_{12}$ 118 項)で今日検算できる**(§2.4) |
| **⑤** ★★★ | **Washington 型定量化** | 捩れ確率 $\approx p^{-(\mathrm{codim}+1)}$。★ **深さ 2 床は codim 大 ⟹ 全重み全素数で捩れ確率 $\approx4\times10^{-4}$**(P-D2-1 の定量的裏づけ)・★ **深さ 4 層は codim 0(正方)⟹ $p^{-1}$ ⟹ 非正則素数の古典的発見論($\frac12\ln\ln X$)を模型が再現**(§3) |
| **⑥** | **試験番地** | (32,37) 深さ 2 床は D2-SNF-1 で即採点(予言: 空・確率 $\sim37^{-11}$)・深さ 4 層は $\dim\mathrm{ls}_{4,32}=O(k^3)$ ⟹ **数百次元 = 構成可能**(§4.1)。157 は Massey/深さ 3 層(§4.2) |
| **⑦** ★★ | **(12,23) 窓側 ④-2 = 当** | Δ の mod 23 射影像は **$S_3$**(h(ℚ(√−23))=3 由来)⟹ ねじれ位数 3 と 2 はいずれも **$\mid6$** ⟹ **TWIST-6 の帯域に収まる唯一の番地**(691 は 690 ∤ 6 で RW-NOEIG に殺された)⟹ **群論側の実現可能性は高い**。ただし橋(観測量)は UNKNOWN(§4.3) |
| **⑧** | **ls 世界の選択** | filtered は **命題 FG-2**(深さ三角性なし)で深さ局所化が死ぬ。ls は方程式が**深さ斉次** ⟹ 深さ固定切片が独立。$\dim(\mathrm{ls}_r)_k=O(k^{r-1})$ ⟹ **天文学的 $k$ でも部品は構成可能**(§5) |

> ### ⚠⚠ 記号衝突の警告(**最初に固定する・違反すると静かに壊れる**)
> - $\mathcal S_k$ = **工房の S 側解空間**(hexagon+$\nu_k$ の核 $\cong\mathfrak{grt}_k$)。TOR-SWEEP の対象。
> - $\mathsf P_k$ = **偶周期多項式空間**(Brown の $\mathsf S_{2n}$)。$\dim=\dim S_k(SL_2(\mathbf Z))$。
> **本ノートでは Brown の $\mathsf S$ を必ず $\mathsf P$ と書く。**(裁定 752 の $\ker\beta_k\otimes\mathbf Q=\mathsf S_k$ は本ノートの記法では $=\mathsf P_k$。)

---

# 1. 委嘱① — 整複体の定義

## 1.1 ls 世界の格子(定義 LAT 流儀)

> ### 定義 LAT-ls(本ノート・$\mathbf Z$-構造の正本)
> 重み $k$・深さ $r$ について
> - $(\mathrm{ls}_r)_k^{\mathbf Z}$ := 線型化二重シャッフル方程式の**整数解格子**。多項式表現では $r$ 変数・次数 $k-r$ の多項式のうち、線型化 shuffle・stuffle・パリティ条件を満たすものの $\mathbf Z$-格子(**方程式はすべて整係数** ⟹ 解格子は飽和・自由)。**基底 = Hermite 標準形で決定的に固定**。
> - $L_{k,r}^{\mathbf Z}$ := $\mathrm{Lie}^r(\mathrm{ls}_1)_k\cap(\mathrm{ls}_r)_k^{\mathbf Z}$(**飽和**)= 深さ 1 生成元 $\bar\sigma_{2n+1}$ の $r$ 重 Ihara 括弧が張る部分の飽和格子。
> - $\mathsf P_k^{\mathbf Z}$ := 偶周期多項式の整格子(Brown Example 8.4 の "**Choose integral generators**" $f_{12}=[x_1^8,x_2^2]-3[x_1^6,x_2^4]+\dots$ が $k=12$ の実物)。
>
> **整性の担保(3 点・すべて逐語 pin 済)**
> 1. $\bar\sigma_{2n+1}=(-1)^n(\mathrm{ad}\,e_0)^{2n}e_1$(**(1.6)**)— 整係数 ✔
> 2. Ihara 括弧は整係数の構造定数 ⟹ $\beta_k$・$L_{k,r}$ は分母なし ✔(追補 B §1.3 で確認済)
> 3. **$e$ は $\mathbf Z$ 上定義**(p.25 逐語: "the differential $d$ is related to our map $e$ (**which is defined over Z**) up to a non-trivial isomorphism of the space of period polynomials")✔
>
> ⚠ **【CONE-GAP-1】**: Brown 論文は合同の基礎となる $\mathbf Z$-格子を**定義していない**(`brown_prop64_lattice_verbatim_v1.md` §2.3: "lattice" は全文 0 hit)。⟹ **上の定義は我々の選択**であり、結果は**格子言明**(【D-GAP-1】型)。★ ただし p.25 の "up to a non-trivial isomorphism of the space of period polynomials" は「$d$ と $e$ の間に $\mathsf P$ の自己同型のずれがある」と読め、**その自己同型が $GL(\mathsf P^{\mathbf Z})$ か否かが単因子を変える** ⟹ 【CONE-GAP-2】(一点読要請 §6.3)。

## 1.2 深さ 2 床 = (7.8) の整数化

> ### 定義 CONE-2(深さ 2 床)
> $$\mathsf C^{(2)}_k:\qquad 0\longrightarrow \bigl(\textstyle\bigwedge^2\mathrm{ls}_1\bigr)_k^{\mathbf Z}\ \xrightarrow{\ \beta_k\ }\ (\mathrm{ls}_2)_k^{\mathbf Z}$$
> $\beta_k(\bar\sigma_a\wedge\bar\sigma_b)=\{\bar\sigma_a,\bar\sigma_b\}$。**(7.8)** の逐語($0\to\mathsf S\to D_1\wedge D_1\to D_2\to0$)の $\mathbf Z$-版であり
> $$H^{-1}(\mathsf C^{(2)}_k)=\ker\beta_k=\mathsf P_k^{\mathbf Z}\ (\textbf{飽和}),\qquad H^{0}(\mathsf C^{(2)}_k)=\mathrm{coker}\,\beta_k .$$
> **既測定量との対応**: $\mathrm{coker}(\beta_k)_{\rm tors}$ の台 $=$ **D2-SNF-1 の測定量**(追補 B §1.1・発注済)。⟹ **④ の 1 階は既に発注済みである。**

## 1.3 深さ 4 層 = 連結写像 $\rho_k$($e_f$ の受け皿)

深さフィルトレーション $\mathcal D^\bullet$ は filtered 世界($\mathfrak g^{\mathfrak m}\subset\mathrm{Lie}(x,y)$)にあり、その**関連付き次数**が ls 世界。両者を繋ぐのが**連結写像**である。

> ### 定義 CONE-4(深さ 4 層・本ノートの中核)
> $\lambda\in\mathsf P_k^{\mathbf Z}$(= 深さ 2 の関係式 $\sum\lambda_{ij}\{\bar\sigma_{2i+1},\bar\sigma_{2j+1}\}=0$)に対し、深さ 1 生成元を filtered 世界の lift $\tilde\sigma$ に持ち上げて
> $$\rho_k(\lambda)\ :=\ \Bigl[\ \sum_{i<j}\lambda_{ij}\{\tilde\sigma_{2i+1},\tilde\sigma_{2j+1}\}\ \Bigr]^{(\text{深さ }4)}\ \bmod\ L_{k,4}^{\mathbf Z}$$
> $$\boxed{\ \rho_k:\ \mathsf P_k^{\mathbf Z}\ \longrightarrow\ \bigl(\mathrm{ls}_4/L_4\bigr)_k^{\mathbf Z}\ }$$
> **well-defined の 3 点**: (i) 深さ 2 成分は $\lambda\in\mathsf P_k$ ゆえ消える;(ii) 深さ 3 成分はパリティ(Prop 4.3・$k$ 偶 $\not\equiv3$)で消える ⟹ **先頭は深さ 4** ✔;(iii) lift の取り替えは $L_{k,4}$ の元だけ動かす(重み族分光 命題 F-1 の一般形)⟹ **商で well-defined** ✔。
> ★ これは**深さスペクトル系列の $d_1$(連結準同型)の整数版**である。

> ### ★★ 命題 CONE-A(candidate・本ノート。**こだまの正体**)
> Brown p.25 の恒等式(重み 12,16,18,20 で逐語)は、上の記法でちょうど
> $$\boxed{\ \rho_k\ =\ c_k\cdot e,\qquad c_k=\frac{\mathrm{num}\bigl(\zeta(k)\pi^{-k}\bigr)}{\text{分母}}\ =\ \frac{691}{144},\ \frac{3617}{720},\ \frac{43867}{9000},\ \frac{174611}{35280}\ }$$
> と書ける($e:\mathsf P_k\hookrightarrow(\mathrm{ls}_4/L_4)_k$ は Brown の $\mathbf Z$ 上定義の単射)。ゆえに
> $$\mathrm{coker}(\rho_k)\ \cong\ \mathrm{coker}(e)\ \oplus\ \bigl(\mathsf P_k/c_k\mathsf P_k\bigr)\quad(\text{分解は }c_k\ \text{が単位でない素点で})$$
> $$\Longrightarrow\ \boxed{\ p\mid\mathrm{num}(B_k)\ \Longrightarrow\ p\ \textbf{は }\rho_k\ \textbf{の単因子を割る = こだま}\ }$$

> ### ★★★ 第一予言 **P-CONE-1**(**較正・測定前に凍結**)
> $k=12$ では $\dim\mathsf P_{12}=1$、$L_{12,4}=0$(Brown §7.4 逐語「weight 12, depth 4 では $\dim D_4=1$ だが $\mathrm{Lie}_4(D_1)=0$」)、$\dim(\mathrm{ls}_4)_{12}=1$ ⟹ $\rho_{12}$ は**階数 1 の正方写像 $\mathbf Z\to\mathbf Z$**。命題 CONE-A より
> $$\boxed{\ \mathrm{coker}(\rho_{12})\ \cong\ \mathbf Z/691\quad(\textbf{2,3-部分を除いて};144=2^43^2)\ }$$
> すなわち **④ の深さ 4 層の単因子はちょうど 691** — **実測済みこだまの整数版**。
> **検算法**(今日できる): Brown の明示整生成元 $f_{12}$(Example 8.4)と $\bar e_{12}$(118 項・係数は表示範囲で整数)を使い、$\rho_{12}(f_{12})$ を $\bar e_{12}$ で割った比が $\pm691/144$ になるかを見る。
> **外れたら**: 格子の取り方(【CONE-GAP-1/2】)が Brown のそれと違う ⟹ **④ の全ての単因子読みが再較正を要する** ⟹ 最優先の STOP 条件。

## 1.4 ④ の全体(錐)

> ### 定義 CONE(**④ の正本**)
> $$\boxed{\ \text{④}_{k}\ :=\ \mathrm{Cone}\Bigl(\ \iota_{k,\bullet}:\ L_{k,\bullet}^{\mathbf Z}\ \hookrightarrow\ (\mathrm{ls}_\bullet)_k^{\mathbf Z}\ \Bigr)\ }$$
> (深さ $\bullet$ ごとの 2 項複体。$H^{-1}=\ker\iota=0$($\iota$ は単射)、$H^0=\mathrm{coker}\,\iota$。)
> 深さ 2 では $\mathrm{coker}\,\iota_{k,2}$ が $\mathrm{coker}\,\beta_k$ と同じ捩れを持ち、深さ 4 では $\mathrm{coker}\,\iota_{k,4}\supseteq\mathrm{im}(e)$ が $e_f$ の住処。**連結写像 $\rho_k$ が 2 階と 4 階を繋ぐ**(§1.3)。

**項と既測定量の対応表**(委嘱の指定):

| ④ の項 | 内容 | 既測定量 | 状態 |
|---|---|---|---|
| $\mathrm{coker}(\beta_k)_{\rm tors}$ | 深さ 2 床 | **D2-SNF-1**(追補 B §1.4) | ★ 発注済・予言 P-D2-1(空) |
| $\ker\beta_k=\mathsf P_k$ | 周期多項式 | 重み族分光 §1.2 の独立導出($s_{12},s_{16},s_{18},s_{20},s_{22}$) | ★ 計算済(原始整ベクトル) |
| $\rho_k$ の単因子 | 深さ 4 層 | **(12,691) = 実測済こだま** | ★ **P-CONE-1 として凍結** |
| $\mathrm{coker}(e)_{\rm tors}$ | **超過**(こだまを超える分) | 未測定 | ★ **④ の主標的**(§2.4) |
| $\mathrm{coker}(N_k)_{\rm tors}$ | S 側(filtered) | **TOR-SWEEP**(P-T-1) | 実測中($k\le12$) |

---

# 2. 委嘱② — 捩れの意味論と「捩れを殺す構造」の検査

## 2.1 二つの現象の定義(混同禁止)

- **A 縮み**:$\bmod p$ で $\mathrm{Lie}(\mathrm{ls}_1)$(= $\bar\sigma$ たちの生成する括弧代数)の階数が有理階数より小さくなる。
- **S 伸び**:$\bmod p$ で解空間(ls 側なら $\mathrm{ls}_r$、filtered 側なら $\mathcal S_k$)が有理次元より大きくなる。

## 2.2 ★★★ 精密文(**「一つの対象の捩れが両方を支配する」**)

> ### 定理 CONE-B(candidate・本ノート)
> $\iota:L^{\mathbf Z}\hookrightarrow M^{\mathbf Z}$ を有限階数自由 $\mathbf Z$-加群の**単射**($L$ は飽和とは限らない像)とする。次は同値:
> $$\textbf{(i)}\ p\mid\#\mathrm{coker}(\iota)_{\rm tors}\quad\textbf{(ii)}\ \exists v\in M^{\mathbf Z}\setminus\iota(L^{\mathbf Z}):\ pv\in\iota(L^{\mathbf Z})\quad\textbf{(iii)}\ \mathrm{rank}_{\mathbf F_p}(\iota\otimes\mathbf F_p)<\mathrm{rank}_{\mathbf Q}\iota$$
> **証明.** Smith 標準形。(i)⟺(iii) は追補 B §1.1 と同じ。(ii) は非飽和性の定義。∎
>
> ### ★ 二つの読み(**同一の $p$-捩れ**)
> | 読み | 内容 | 現象名 |
> |---|---|---|
> | **A 側の読み**((iii) 経由) | $\iota\otimes\mathbf F_p$ の階数が落ちる = **括弧代数の像が $\bmod p$ で縮む** | **A 縮み** |
> | **S 側の読み**((ii) 経由) | $v$ は「$1/p$ 倍の括弧」= $\bmod p$ では**括弧では書けない新しい元** ⟹ 例外部分 $M/\iota(L)$ が $\bmod p$ で伸びる | **S 伸び** |
> $$\boxed{\ \textbf{A 縮みと S 伸びは、}\mathrm{coker}(\iota)\ \textbf{の同一の }p\textbf{-捩れ元の、二つの言い換えにすぎない。}\ }$$
> ★ これが裁定 749④「一つの対象の捩れが両方を支配する」の**精密文**であり、裁定 747 の共鳴教義(独立事象の同時発生)が**同一事象の二重記述**であったことを意味する — ★ **教義の強化ではなく修正**:「二つの独立な稀事象の一致」ではなく「**一つの稀事象の二つの顔**」。偶然一致の確率論(RA-11 の null)は**この階層では適用できない**(§3.3)。

## 2.3 ★★★ 捩れを殺す構造の検査(**両刃・最優先**)

裁定 751 の三分法に沿って、no-go 側の候補を 3 つ検査する。

| 候補 | 主張の形 | 判定 |
|---|---|---|
| **(a) 双対性** | $\mathrm{ls}$ 上の完全対($\theta$ 対合 + Poincaré 型)が $L$ に制限しても unimodular ⟹ $L$ は直和因子 ⟹ **coker 捩れゼロ** | ★ **不成立**。反例が実物: $\mathrm{coker}(\rho_{12})=\mathbf Z/691\ne0$(命題 CONE-A・P-CONE-1)。もし双対性が捩れを殺すなら 691 は現れない。⟹ **双対性は ④ に無い(少なくとも $\rho$ 層に)** |
| **(b) Euler 標数** | $\chi$ が捩れを制約する | ★ **空振り**。$\chi$ は階数のみで決まり**捩れに完全に鈍感** ⟹ 情報ゼロ(検査したが no-go にも存在にも使えない・正直記録) |
| **(c) 完全対 / スペクトル系列の退化** | 深さフィルトレーションのスペクトル系列が $E_2$ で退化 ⟹ 連結写像 $\rho$ がゼロ ⟹ 捩れなし | ★ **不成立**。$\rho_{12}\ne0$(値 $691/144$)⟹ **$d_1$ は非零** ⟹ 退化しない |

> ### ★★ 検査の結論(**両刃の裁定**)
> $$\boxed{\ \textbf{④ の捩れを一般に殺す構造は存在しない — }(12,691)\ \textbf{がその反例である。}\ }$$
> ⟹ **no-go の望みは「捩れゼロ」ではありえない。** 正しい no-go の形は
> $$\boxed{\ \textbf{「④ の捩れは既知のこだま分(}c_k\ \textbf{の素因子)でちょうど尽きる」}\ }$$
> であり、これは裁定 749 補記③ の等値化と**完全に一致**する。**⟹ 相 2 の主砲標的の定式化を本設計が追認する。**

## 2.4 ★★★ 等値化の最終形(**測れる 1 問へ**)

命題 CONE-A の分解 $\rho_k=c_k\cdot e$ より、$\rho_k$ の捩れは
$$\underbrace{\mathsf P_k/c_k\mathsf P_k}_{\textbf{こだま(既知・Bernoulli 分子)}}\ \oplus\ \underbrace{\mathrm{coker}(e)_{\rm tors}}_{\textbf{超過(未知)}}$$
に分かれる。ゆえに

> $$\boxed{\ \textbf{井原予想の }p\textbf{-進の運命}\quad\Longleftrightarrow\quad e:\mathsf P_k^{\mathbf Z}\hookrightarrow(\mathrm{ls}_4/L_4)_k^{\mathbf Z}\ \textbf{が }\mathbf Z\ \textbf{上飽和か}\ }$$
> - **飽和(coker 捩れなし)** ⟹ 捩れはこだま分で尽きる ⟹ **予想成立側**(no-go = 裁定 751 の (ii))。
> - **非飽和** ⟹ こだまを超える捩れ = **共鳴の実現**(反例エンジン = (i))。
>
> ### ★ これは $k=12$ で**今日検算できる**
> Brown が明示整生成元を与えている($f_{12}$ = Example 8.4・$\bar e_{12}$ = 118 項・p.24 画像照合済)⟹ $e(f_{12})$ が $(\mathrm{ls}_4)_{12}^{\mathbf Z}$ の**原始元**かを見るだけ($\dim=1$ ゆえ「係数の gcd が 1 か」)。
> **予言 P-CONE-2**: $e(f_{12})$ は原始的($\mathrm{coker}(e)_{\rm tors}=0$)⟹ $k=12$ ではこだま分で尽きる。
> ⚠ **$\bar e_{12}$ の全 118 項の整性は論文に明示なし = UNKNOWN**(`brown_prop64_lattice_verbatim_v1.md` §2.3)⟹ **一点読要請**(§6.3)。

## 2.5 三分法(裁定 751)への現時点の割り付け

| 番地 | (i) 明示 ④+捩れ機構 | (ii) no-go 証明 | (iii) UNKNOWN |
|---|---|---|---|
| **(12,691)** | ★ **④ は明示構成済**(§1.3)・捩れ機構 = $c_{12}=691/144$ | 超過ゼロ(P-CONE-2)なら**こだま止まり = 予想成立側の 1 点** | — |
| **(16,3617)** | ④ の構成は同型(命題 CONE-A が重み 16 でも成立・p.25 逐語) | 同上 | $\sigma_{13}$ 未開通 |
| **(32,37)** | 深さ 2 床は即採点可・深さ 4 層は構成可(§4.1) | motivicity 保証切れ ⟹ (ii) の道具がない | ★ **ここが唯一の開いた場所** |
| **(12,23)** | 窓側 ④-2(§4.3) | — | ★ 橋の観測量が未定義 |

---

# 3. 委嘱③ — Washington 型定量化

## 3.1 発見論的模型

整数行列 $A$($n$ 行 $\times$ $m$ 列・階数 $r$)の単因子について、**Cohen–Lenstra 型の発見論**(成分が「ランダム」)では
$$\Pr\bigl[p\mid d_r(A)\bigr]\ \approx\ 1-\prod_{i=c+1}^{\infty}\bigl(1-p^{-i}\bigr)\ \approx\ p^{-(c+1)},\qquad c:=\dim(\text{target})-r\ (\textbf{余次元}).$$

> ### ★★★ 帰結 CONE-C(**捩れは正方に近い層にしか棲まない**)
> $$\boxed{\ \Pr[\text{捩れ}]\approx p^{-(c+1)}\ \Longrightarrow\ \textbf{余次元 }c\ \textbf{が 1 増えるごとに捩れ確率は }p\ \textbf{分の 1 になる。}\ }$$

## 3.2 各層への適用(**自前計算**)

**深さ 2 床** $\beta_k$($n=\#$対、target $=(k-2)/2$、$r=n-\dim\mathsf P_k$):

| $k$ | $r$ | target | 余次元 $c$ | $\sum_{p\ge5}p^{-(c+1)}$ |
|---:|---:|---:|---:|---:|
| 12 | 1 | 5 | 4 | $3.9\times10^{-4}$ |
| 16 | 2 | 7 | 5 | $7.3\times10^{-5}$ |
| 20 | 3 | 9 | 6 | $1.4\times10^{-5}$ |
| 24 | 3 | 11 | 8 | $5.4\times10^{-7}$ |
| 32 | 5 | 15 | 10 | $2.1\times10^{-8}$ |

$$\boxed{\ \textbf{重み 12..32 の全床・全素数を合わせた捩れ期待値}\ =\ 8.9\times10^{-4}\ (\textbf{自前計算・}\S3.4)\ }$$
⟹ ★ **P-D2-1(捩れゼロ)は「たぶん空」ではなく「ほぼ確実に空」**。逆に **1 つでも出たら偶然の確率 0.09% ⟹ ほぼ確実に構造**(RA-11 の「1 発の的中 = 理論級証拠」が**この層で定量的に正しい**)。

**深さ 4 層** $\rho_k$:$k=12$ で source 1・target 1 ⟹ **余次元 $c=0$** ⟹ $\Pr\approx p^{-1}$。
$$\sum_{p}\frac1p\ \text{は発散}\quad\Longrightarrow\quad \textbf{深さ 4 層では捩れは「生成的」}$$
★★ しかも $\sum_{p\le X}1/p\approx\ln\ln X$ で、**非正則素数の古典的発見論(重み固定で $\frac12\ln\ln X$)と同じ形**。
$$\boxed{\ \textbf{④ の模型は、非正則素数の分布の古典的発見論を再現する。}\ }$$
⟹ これは模型の**独立な健全性検査**であり、同時に「深さ 4 層の捩れ = Bernoulli 分子」という命題 CONE-A の定量的な裏づけでもある。

## 3.3 ★ 「超過」の期待規模(委嘱の問い)

超過 = $\mathrm{coker}(e)_{\rm tors}$。余次元は
$$c^{\rm exc}_k\ =\ \dim(\mathrm{ls}_4/L_4)_k\ -\ \dim\mathsf P_k .$$
- $k=12$: $1-1=0$ ⟹ $\Pr\approx p^{-1}$ — ただし**その $p^{-1}$ は既にこだま(691)で説明されている** ⟹ 超過の余地は $c^{\rm exc}$ を**こだま因子で割った後**で測る。
- $k\ge16$: $\dim(\mathrm{ls}_4)_k$ は $O(k^3)$ で増え、$\dim\mathsf P_k$ は $\approx k/12$ ⟹ $c^{\rm exc}_k\to\infty$ ⟹ $\Pr\approx p^{-(c+1)}\to0$。
> ### ★ 定量的な帰結(**正直に**)
> $$\boxed{\ \textbf{ランダム模型の下では、超過は重みが上がるほど急速に起こりにくくなる。最初の超過を期待するなら「余次元が小さい層」を探すべきである。}\ }$$
> ⟹ **本模型は「超過は起こりにくい」= 予想成立側に傾く**という予測を出す。RA-3(p² 番地・$X\sim4\times10^{11}$)や RA-5(Vandiver・$\le10^{100}$)の「ゆっくり発散」型の期待は、**余次元 0 の層でのみ成り立つ**。
> ⚠ **【CONE-GAP-3】**: $\dim(\mathrm{ls}_4)_k$ と $\dim L_{4,k}$ の閉形式を本ノートは持っていない($k=12$ の $1,0$ のみ逐語)⟹ $c^{\rm exc}_k$ の表は**作れていない**。⟹ 一点読要請(§6.3)。
> ⚠ **RA-11 の null との整合**(委嘱の指定): §2.2 の精密文により **A 縮みと S 伸びは独立事象ではない**(同一捩れの二つの顔)⟹ RA-11 の「独立な稀事象の同時発生」型 null は**この階層では適用外**。正しい null は上の単因子模型($p^{-(c+1)}$)である。**RA-11 は棄却ではなく適用範囲の限定**(異なる二つの複体を跨ぐ突合には依然有効)。

## 3.4 再現コマンド

```
python -c "
from sympy import primerange
" 2>/dev/null; python -c "
def sieve(n):
 s=[True]*(n+1); s[0]=s[1]=False
 for i in range(2,int(n**.5)+1):
  if s[i]:
   for j in range(i*i,n+1,i): s[j]=False
 return [i for i in range(5,n+1) if s[i]]
P=sieve(200000)
def dimS(k): return k//12-1 if k%12==2 else k//12
for k in range(12,33,2):
 n=len([a for a in range(3,k//2+1,2) if a<k-a]); r=n-dimS(k); c=(k-2)//2-r
 print(k,r,(k-2)//2,c,'%.3g'%sum(p**-(c+1) for p in P))
"
```

---

# 4. 委嘱④ — 試験番地の計画

## 4.1 (32, 37) — 保証切れ×方向つきの第一試験

**深さ 2 床**: D2-SNF-1 のデータで**即採点可**。$k=32$: $7\times15$ 行列・階数 5・余次元 10 ⟹ 予言 $\Pr\approx37^{-11}\approx2\times10^{-18}$ ⟹ **確実に空**。⟹ **深さ 2 は (32,37) について何も言わない**(追補 B §1.3 の切りと整合)。
**深さ 4 層**: $\dim\mathsf P_{32}=2$ ⟹ ★ **初めて $\rho_k$ が $2\times(\cdot)$ の行列**になる = 札 RA-1 の「方向」の正体は **$\rho_{32}$ の階数 1 欠損**である。
$$\boxed{\ \textbf{RA-1 の「方向の欠損」の精密形}:\ \mathrm{rank}_{\mathbf F_{37}}\rho_{32}=1\ (<2)\ }$$
**サイズ見積り**: $(\mathrm{ls}_4)_{32}$ は 4 変数・次数 28 の多項式空間の部分 ⟹ 上界 $\binom{31}{3}=4495$、対称性で割って**数百次元**。$\rho_{32}$ は $2\times(\text{数百})$ ⟹ **単因子計算は自明なコスト**。
★ **律速は $\rho_{32}$ の構成**(重み 32 の filtered lift $\tilde\sigma$ が要る ⟹ ambient $2^{32}$ = 圏外)。
> ### ★ 回避策(**本ノートの提案**)
> $\rho_k$ は**深さ 4 成分しか使わない**。深さ 4 成分の計算に filtered の全 ambient は不要で、**深さ $\le4$ の切片だけで足りる**可能性がある。⚠ ただし **命題 FG-2**($\sigma_m$ の solver は深さ切り詰め不可)により **$\tilde\sigma$ 自体は切り詰められない** ⟹ **$\rho_{32}$ は現状の道具では構成できない**。
> $$\boxed{\ (32,37)\ \textbf{の深さ 4 層は「部品は小さいが原料}(\tilde\sigma_{31}\ \textbf{等)が作れない」— 裁定 751 の (iii) UNKNOWN・障害物の名指し = FG-2}\ }$$

## 4.2 157 — Massey 層の位置づけ

RA-4 の交差項($\kappa_{62}\cup\kappa_{110}$)は **深さ 3 以上**(Massey 積 = 2 次以上の連結写像)。本設計では **$\rho$ の高次版 $d_2,d_3,\dots$**(深さスペクトル系列の高次微分)に当たる。
$$\boxed{\ \textbf{157 の交差項 = ④ の }d_2\ \textbf{以降。}\ d_1=\rho\ \textbf{すら重み 32 で作れない現状では圏外。}\ }$$
⟹ **位置づけ = 台帳に載せるが発注しない**(裁定 751 の (iii)、障害物 = FG-2 と重み)。

## 4.3 ★★ (12, 23) 窓側 ④-2 — **本命候補としての当否 = 当**(群論側)

**設定**: $\Delta$ の mod 23 表現は例外的で、$\mathbf Q(\sqrt{-23})$($h=3$)の類指標から誘導される **dihedral**(自前知識・**要 pin**)。射影像は位数 3 の指標 $\rtimes$ 位数 2 ⟹ **$\cong S_3$**。

> ### ★★ 命題 CONE-D(candidate・本ノート。**窓側実現可能性の判定**)
> $(12,23)$ の dihedral 退化に現れるねじれ指標の位数は **3(類群)と 2(二次体)**。いずれも $\mid6$。
> ⟹ **定理 TWIST-6**(窓の 1 次元 $\mathbf F_p$-合成因子のねじれ位数 $\mid\gcd(6,p-1)$)の**帯域に完全に収まる**。$p=23$: $\gcd(6,22)=2$、$3\nmid22$ ⟹ 位数 3 のねじれは $\mathbf F_{23}^\times$ には入らないが、**2 次元既約 $S_3$-加群として入る**(本体 TWIST-6 の「道 (ii)」)。
> $$\boxed{\ (12,23)\ \textbf{は、RW-NOEIG が }(12,691)\ \textbf{を殺したのと同じ検査を通過する唯一の番地候補である。}\ }$$
> **対比**: $(12,691)$ では $\chi^{11}$ の位数 690 $\nmid6$ ⟹ **系 RW-NOEIG で即死**。$(12,23)$ は死なない。
> **さらに**: 退化先 $S_3$ は**我々の梯子 $G_p=H_{p^3}\rtimes S_3$ のトーラスそのもの**であり、$S_3$ 自身も窓商($\mathrm{ab}=C_2$・$(2,3)$-生成・$\twoheadrightarrow S_3$)、$S_3\times C_3$ も窓商($\mathrm{ab}=C_6$)。⟹ **群論側の受け皿は既に手元にある。**

> ### ⚠ ただし橋は未定義(**正直な限界**)
> 窓が測るのは **GT-shadow** であって Galois 像の**形**ではない。「$\bmod23$ で像が dihedral になる」を窓側の観測量に翻訳する辞書は **E-DIM 橋(707-④)が未完**ゆえ存在しない。
> $$\boxed{\ \textbf{④-2 の当否: 群論側 = 当(唯一 TWIST-6 を通る番地)/ 観測量 = UNKNOWN(橋が未完)}\ }$$
> ⟹ **裁定 751 の (iii)**。ただし**障害物が「橋の不在」1 点に名指しできている**のは他番地より遥かに良い状態であり、**相 2 の投資先としては最有力**(司令塔の見立て「結合先が dihedral 本峰 = 定理最厚地帯」を支持)。
> ⚠ **【CONE-GAP-4】**: $\Delta$ の例外素数リストと mod 23 の dihedral 性(および $h(\mathbf Q(\sqrt{-23}))=3$)は**自前知識・要 pin**。命題 CONE-D の TWIST-6 部分は pin に依存しないが、**前件が偽なら番地ごと消える** ⟹ 一点読要請(§6.3)。

---

# 5. 委嘱⑤ — 深さ次数付き世界の選択(**規約として明文化**)

> ### 規約 CONE-ls(本ノート・以後の ④ 系設計の前提)
> **④ は ls(深さ次数付き)の世界で作る。filtered(hexagon on $\mathrm{Lie}(x,y)$)では作らない。**
>
> **理由 1(決定的)**: **命題 FG-2**(`weight_family_spectroscopy_design_v1_addendum_fgap3.md` §2)— filtered の 3-cycle 条件 $(1+\tau+\tau^2)f=0$ は**深さについて三角でない**(深さ 1 の方程式が $f$ の**全ての**深さ成分を含む)⟹ **深さ局所化が原理的に不可能**。ゆえに filtered で「深さ 4 層だけ」を取り出す複体は作れない。
> **理由 2**: ls の定義方程式(線型化二重シャッフル)は**深さ斉次** ⟹ 各深さ $r$ が独立した有限線型系 ⟹ **深さ固定切片が単独で構成できる**。
> **理由 3**: Brown 自身が (7.8)・$e:\mathsf P\to\mathrm{ls}_4$・Prop 4.3(パリティ)を**すべて ls / dg の世界で述べている** ⟹ 正典との突合が直接できる。
>
> ### ★ 会計(**天文学的 $k$ でも部品は構成可能**)
> $(\mathrm{ls}_r)_k$ は $r$ 変数・次数 $k-r$ の多項式空間の部分空間 ⟹
> $$\dim(\mathrm{ls}_r)_k\ \le\ \binom{k-1}{r-1}\ =\ O\bigl(k^{r-1}\bigr)\qquad(\textbf{$r$ 固定で $k$ の多項式})$$
> | $r$ | $k=12$ | $k=32$ | $k=172$ |
> |---:|---:|---:|---:|
> | 2 | $\le11$ | $\le31$ | $\le171$ |
> | 4 | $\le165$ | $\le4{,}495$ | $\le820{,}260$ |
> $$\boxed{\ \textbf{ambient }2^k\ \textbf{(指数)に対し }\mathrm{ls}_r\ \textbf{は }k^{r-1}\ \textbf{(多項式)。深さを固定する限り、重み 172 でも部品は作れる。}\ }$$
> ⚠ **ただし原料は別問題**: $\rho_k$ の構成には filtered の $\tilde\sigma$ が要り、**そこは $2^k$ のまま**(命題 FG-2 で切り詰め不可)⟹ §4.1 の壁。
> $$\boxed{\ \textbf{④ の「部品」は多項式サイズ、「接着剤」}(\rho=d_1)\ \textbf{だけが指数サイズ — これが相 2 の律速の正確な所在である。}\ }$$
> ★ **相 2 の最重要の技術課題**: $\rho_k$ を $\tilde\sigma$ を経由せずに ls の中だけで特徴づけられるか(= 深さスペクトル系列の $d_1$ を ls 内在的に書けるか)。**書ければ天文学的重みの ④ が全て開く。**⟹ 【CONE-GAP-5】(§6.1)。

---

# 6. 【GAP】・一点読要請・novelty・帰属

## 6.1 未閉の穴

| # | 内容 | 重さ |
|---|---|---|
| **【CONE-GAP-1】** | Brown は合同の $\mathbf Z$-格子を**定義していない**(逐語 pin)⟹ 定義 LAT-ls は我々の選択・結果は**格子言明**(【D-GAP-1】型) | ★ 大 |
| **【CONE-GAP-2】** | p.25 の "up to a non-trivial isomorphism of the space of period polynomials" — **その同型が $GL(\mathsf P^{\mathbf Z})$ か否かで単因子が変わる** | ★ 大 |
| **【CONE-GAP-3】** | $\dim(\mathrm{ls}_4)_k$・$\dim L_{4,k}$ の閉形式が無い ⟹ §3.3 の余次元表が作れない | 中 |
| **【CONE-GAP-4】** | $\Delta$ の mod 23 dihedral 性・$h(\mathbf Q(\sqrt{-23}))=3$ は**要 pin**(命題 CONE-D の前件) | 中 |
| **【CONE-GAP-5】** ★ | $\rho_k=d_1$ を ls 内在的に書けるか(filtered の $\tilde\sigma$ を経由しない特徴づけ)。**書ければ相 2 の律速が消える** | ★ **最大** |
| **【CONE-GAP-6】** | 本ノートの全命題は candidate(単系統・Sol 未監査)。**定理 CONE-B・命題 CONE-A/C/D を確定として引用しない**。判定語の発効は司令塔専権 | — |

## 6.2 ★ 副産物 — 【B-PIN-1】は**閉**

追補 B で発火前 pin を要請した「Brown の未排除命題の主語」は、`brown_prop64_lattice_verbatim_v1.md` §3 に逐語で既載:
> "nor can we presently rule out the existence of relations of the form **{e_f, σ_{2n+1}} ∈ Lie₅ ls₁** which can only occur in **depth ≥ 5 and weight ≥ 15**. Relations which are quadratic in the e_f could first occur in weight 28 and depth 8."
$$\Longrightarrow\ \boxed{\ \textbf{【B-PIN-1】は閉。RA7-PROBE-1 の前件(命題 B-1 の読み)は逐語で確認された。}\ }$$
★ 併せて **RA-7 の族の第 2 番地**が逐語で判明: **「$e_f$ について 2 次の関係式は重み 28・深さ 8 が最初」** ⟹ 台帳に追加(構成は圏外だが番地は確定)。

## 6.3 一点読要請(**正典に引けない断片・UNKNOWN の解消用**)

| # | 読む対象 | 何を確定したいか |
|---|---|---|
| **CR-1** ★ | Brown §8.4 p.24 の $\bar e_{12}$(118 項)の**全係数**と Example 8.4 の $f_{12}$ | **P-CONE-2**($e(f_{12})$ が原始的か)の直接検算。④ の等値化(§2.4)を $k=12$ で閉じる**唯一の入口** |
| **CR-2** | 同 p.25 の "up to a non-trivial isomorphism of the space of period polynomials" の前後 | 【CONE-GAP-2】(その同型が整同型か) |
| **CR-3** | Brown §7 の $D_r$ の定義と $\dim D_r$ の公式(もしあれば) | 【CONE-GAP-3】(余次元表) |
| **CR-4** | $\Delta$ の例外素数と mod 23 表現(Serre/Swinnerton-Dyer 系・**文献ゲート経由**) | 【CONE-GAP-4】(命題 CONE-D の前件) |

## 6.4 novelty grep(`docs/` `provenance/` `sol/` 全域)

`cone_design` / `CONE-2` / `CONE-4` / `CONE-A`〜`CONE-D` / `LAT-ls` / `P-CONE-` / `規約 CONE-ls` / `ρ_k = c_k·e` = **0 hit**(本ノート初出)。`(7.8)` の整数化・「A 縮みと S 伸びは同一捩れの二つの顔」・「捩れは正方に近い層にしか棲まない」も **0 hit**。$\beta_k$・$\mathsf P_k$・$e$・$\mathrm{ls}_r$ の定義は既在(借用)。

## 6.5 帰属

- 教義・委嘱 = 研究者(二相戦略・三分法)+ 司令塔(裁定 749/749 補記/751/752・**④ = 錐の p-捩れという着想そのもの**)。
- 発案 = 発案係 v3(RA-1 の「方向」・RA-3/RA-11 の統計・RA-9 の (12,23))。
- **本ノートの新規部分**: 定義 LAT-ls / 定義 CONE-2 / **定義 CONE-4($\rho_k$ = 連結写像)** / **命題 CONE-A($\rho_k=c_k e$ ⟹ こだまの正体)** / **P-CONE-1(第一予言の凍結)** / **定理 CONE-B(二つの顔)** / §2.3 の両刃検査(双対性・Euler・退化がすべて不成立/空振り)/ **§2.4 の等値化の最終形** / **帰結 CONE-C(捩れは正方層にしか棲まない)** と §3.2 の定量表 / **命題 CONE-D((12,23) が TWIST-6 を通る唯一の番地)** / **規約 CONE-ls**(理由 3 点+多項式サイズ会計)/ 【B-PIN-1】の閉鎖と重み 28・深さ 8 の第 2 番地。
