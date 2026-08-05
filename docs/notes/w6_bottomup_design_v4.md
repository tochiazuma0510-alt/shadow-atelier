# W-6 掘削 BOTTOM-UP 設計 **v4** — F104-2.2 の 6 blocker 閉鎖と**凍結の正式請求**

**状態札: `design / ★ freeze 請求(本書が正式請求)/ 走らせていない(本書の GAP 実行ゼロ)/ Sol 未承認 / 発火未認可 / 実測ゼロ / 封印 3 量非接触・Im R 非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05・**新設**(`w6_bottomup_design_v3.md` は**不改変**。v3 → v4 の差分は本書が正本)
- 委嘱: 司令塔 —「**v4 で 6 blocker を閉じよ**」(F104-2.2 の 1〜6 + F104-2.3 の route 2 要件 5 点 + F104-2.4 の cert 欄別化)
- **入力正本**:
  - `sol/sol_reply_104_math31.md` **§2**(F104-2.1 受理 5 点・**F104-2.2 blocker 1〜6**・F104-2.3 ISO route 2 限定裁定・F104-2.4 p=3 dim3/4 の位置づけ・**F3S3 型数 10/18 批准**)
  - `docs/notes/w6_bottomup_design_v3.md`(v3)/ `w6_bottomup_design_v2.md` / `w6_kill_theorems_v2_erratum.md` / `w6_kill_theorems_v1.md` / `k5_w6_construction_v1.md`
  - `docs/week1-定義ノート.md` §2(**GT-pair / charming / GT-shadow / settled / isolated / Prop 3.2 / Prop 3.6 / $N_{\rm ord}$**)
  - **既走 cert 3 本**(本書が欄仕様を訂正する対象・いずれも**不改変**):
    - `search/certs/k5gen_w6_bu_s0_20260805.json`(`0fba1743…0cf1`)
    - `search/certs/h2_census_s4_20260805.json`(`4b867320…3b30`・17 行)
    - `search/certs/h2_census_s4_p3ext_20260805.json`(`597c7480…3b00`・28 行・`tier`=`inventory-census-supplement`)
- **外部文献ゼロ。**

> ## 非接触の申告
> **本書は 1 行も実行していない**(GAP 起動ゼロ)。$\mathrm{Im}\,R_{N,K^{(5)}}$ 非接触・$d_N$ 非評価・封印 3 量非接触。**証明書は構造欄(`row_count` / `tier` / `scope_out` / `scope_statement`)のみを読み、数学的測定値は読んでいない。**

---

## 0. 判定(6 blocker × 閉じ方)

| # | F104-2.2 の blocker | 本書での閉じ方 | 節 |
|---|---|---|---|
| **1** | v3 §9-4 が逐語で「凍結も発火も請求しない」と宣言 ⟹ 便本文だけで反転できない | ★ **本書 §1 が versioned v4 として凍結を正式請求**(FREEZE-1〜5)。**発火請求は S1〜S3.5 に限定**(S3.6 以降は route 2 gate 閉鎖まで請求しない) | §1 |
| **2** | MARK-BIJ の余域 $\mathcal W$ が広すぎる(vector-space 条件を証明していない) | ★ **余域を $\mathcal W_{\rm adm}$ へ制限**(司令塔の第 1 案)。**補題 MARK-BIJ-adm**: $V$ アーベル ⟹ $K^{(5)}$ の共役作用が自明 ⟹ $\widehat G_5$-加群、指数 $p$ ⟹ $\mathbf F_p$-線型空間。**三層宇宙 $\mathcal W\supset\mathcal W_{\rm adm}\supset\mathcal W_{\rm fire}$** を定義 | §2 |
| **3** | SAT roof 節が全称でない(良い lift を 1 つ選んで $\delta=0$ を隠せる) | ★ **述語を $\neg\exists U$ 形へ差替**。許容符号化は **(E1) 全 lift の exact 連言** と **(E2) co-instance(別 UNSAT 系)** の 2 つのみ。**像 $\bar U$ で index して 1 lift 選択は禁止**(**S-BU-14**) | §3 |
| **4** | BU-GAP-10 の説明が ROOF-TYPE と矛盾($N\subseteq N'$ は自動) | ★ **説明を訂正**。真の未閉点 = **1 つの像 $\bar U$ 上の全 lift 列挙**。★ **補題 LIFT-ENUM** で「全 lift = $E$ 内の補元のうち $\widehat P$-正規なもの = $Z^1(\bar U,V)$ torsor + 線型条件」と**有限計算に還元**(数学的未閉 → 実装の悉皆性仕様へ) | §4 |
| **5** | ISO route 2 の cert が陽性 2 件のみ・constant-TRUE が通る・interface 未明記 | ★ **route 2 gate の 5 要件を設計に収載**(R1〜R5)。**紙 bridge 2 本を本書で証明**(B-1 全域無重複・**B-2 settled ⟺ well-defined ∧ 全単射**)+ mutant matrix 6 件 + 第二系統 + TRUE/格の分離 + **$\widehat P=B_3/N$ interface(6 倍則)** | §5 |
| **6** | p3 cert の `scope_out` が旧文言のまま・28 行の位置づけ | ★ **`inventory_universe` / `firing_universe` の別欄化**を cert 仕様に規定。**28 行は探索宇宙外 supplemental で分母に足さない**。scope_out 文言差替。**F3S3 の母関数**で dim 2/3/4 = **5 / 10 / 18** を紙で確定(Sol 批准分の根拠) | §6 |

---

## 1. 【blocker 1】★ 凍結の正式請求(**本書が請求主体**)

> ### ★ 宣言(v3 §9-4 の撤回を含む)
> $$\boxed{\ \textbf{v3 §9-4 の「本書は凍結も発火も請求しない」は、versioned に }\mathbf{v4}\ \textbf{で撤回する。本書 }\mathbf{w6\_bottomup\_design\_v4.md}\ \textbf{が、下記 FREEZE-1〜5 の凍結を正式に請求する。}}$$
> **v3 は不改変**(歴史記録として保存)。凍結の対象は**本書 §1.1 の 5 項**であり、v3 の本文はそのうち §1.1 が指す範囲でのみ v4 の記述に置き換わる。

### 1.1 凍結を請求する 5 項

| # | 凍結対象 | 正本 |
|---|---|---|
| **FREEZE-1** | **対象の型**: marked datum $\mathcal D=(V,\widehat P,\rho)$・同値 MARK-ISO(base-fixed)・$\mathrm{Roof}(\mathcal D)$・$\delta_{\rm roof}:\mathrm{Roof}(\mathcal D)\to V/W$ | v3 §1–§2 + 本書 §2(余域制限)・§4(lift 列挙) |
| **FREEZE-2** | **三層宇宙** $\mathcal W\supset\mathcal W_{\rm adm}\supset\mathcal W_{\rm fire}$(定義は §2.3)。**発火宇宙 $\mathcal W_{\rm fire}$ = (V-cen) 層・$p\in\{2,3\}$・$\dim\le4$・cap 8000** | 本書 §2.3 |
| **FREEZE-3** | **段の順序**: S0 → S1 → S2 → S3 → S3.5 → **S3.6(ISO-GATE)** → S4′ → S5 → S6 → S7 → S8 → (S8.5 照合レーン) → S9 | v3 §8 |
| **FREEZE-4** | **停止規則** S-BU-1〜13(v3)+ **S-BU-14〜16**(本書 §7) | v3 §8 + 本書 §7 |
| **FREEZE-5** | **ゲート**: SURJ-GATE(v2 §2.3)・**ISO-GATE(fail-closed・既定 UNKNOWN)**・GQuotients は**別ゲート継続** | v3 §4 + 本書 §5 |

### 1.2 発火を請求する範囲(**限定**)

$$\boxed{\ \textbf{発火請求は }\mathbf{S1\text{--}S3.5}\ \textbf{(宇宙確定 → }H^2\textbf{ 類 → marked lift 列挙)}\ \textbf{のみ。}\ }$$

- **産物の格**: **窓の single-lane candidate inventory**(判定欄なし)。**kill・候補発見・EMPTY-THM への使用は禁止**(S-BU-10/11/13)。
- **S3.6 以降(ISO-GATE より下流)は本書では請求しない。** route 2 gate の 5 要件(§5)が閉じるまで、全 datum は $\mathrm{ISO}=\texttt{UNKNOWN}$ であり、S4′〜S8 は**発火しても在庫注記しか生まない**(v3 §4.3 の警告)。
- **S8.5(SAT)・S9(GQuotients)も請求しない。**

### 1.3 請求しないもの(明示)

1. **W-5 の isolated 判定**: `UNKNOWN (pending route-2 gate)` のまま(F104-2.3 逐語)。
2. **kill / EMPTY-THM / 候補発見**の一切。
3. **下限 4,000 / 13,500 の無条件引用**(F103-2.2 の 4 前件 + (V-cen) 層縮小の前件つきでのみ引用)。

---

## 2. 【blocker 2】MARK-BIJ の余域制限

### 2.1 なぜ v3 の $\mathcal W$ では広すぎたか(**指摘の受理**)

v3 §1.2 の $\mathcal W=\{N\trianglelefteq B_3:N\subseteq K^{(5)},c\in N,[K^{(5)}:N]<\infty\}$ は、$K^{(5)}/N$ が**単一素数の初等アーベル群**である条件を持たない。一方 marked datum の $V$ は $\mathbf F_p[\widehat G_5]$-加群である。⟹ **全射証明の「$V=K^{(5)}/N$」は、$V$ が $\mathbf F_p$-線型空間であることを証明していなかった。** Sol の指摘は正しい。

### 2.2 補題 MARK-BIJ-adm(**余域を制限した正しい形**)

> ### 定義 $\mathcal W_{\rm adm}$
> $$\mathcal W_{\rm adm}:=\Bigl\{N\in\mathcal W\ \Bigm|\ K^{(5)}/N\ \text{は指数 }p\ \text{の初等アーベル群},\ p\in\{2,3\}\Bigr\}.$$

> ### 補題 MARK-BIJ-adm(candidate・本書)
> $\mathcal D=(V,\widehat P,\rho)$ を、**$V$ が有限 $\mathbf F_p[\widehat G_5]$-加群**である marked datum とする。このとき
> $$\ker:\ \{\text{marked datum},\ V\in\mathbf F_p[\widehat G_5]\text{-Mod}\}/\!\cong\ \xrightarrow{\ \sim\ }\ \mathcal W_{\rm adm}$$
> は**全単射**である。

**証明.**
**well-defined / 単射**: v3 補題 MARK-BIJ の証明がそのまま通る(同値の定義と $\varphi$ の構成は型に依らない)。$N=\ker\rho$ に対し $K^{(5)}/N\cong V$ は指数 $p$ の初等アーベル群 ⟹ $N\in\mathcal W_{\rm adm}$ ✓。
**全射(★ ここが v3 で欠けていた段)**: $N\in\mathcal W_{\rm adm}$ とし $V:=K^{(5)}/N$ と置く。
1. **$V$ は $\mathbf F_p$-線型空間**: 指数 $p$ の初等アーベル群だから ✓。
2. **$B_3$ が共役で作用する**: $N\trianglelefteq B_3$ かつ $K^{(5)}\trianglelefteq B_3$(正典 Prop 3.1)⟹ 共役は $K^{(5)}/N$ を保つ ✓。
3. **★ 作用は $\widehat G_5=B_3/K^{(5)}$ を経由する**: $V$ がアーベルゆえ $[K^{(5)},K^{(5)}]\subseteq N$。したがって $u\in K^{(5)}$、$v\in K^{(5)}$ に対し $uvu^{-1}v^{-1}\in[K^{(5)},K^{(5)}]\subseteq N$、すなわち $K^{(5)}$ の共役作用は $V$ 上で自明 ✓。
4. ⟹ $V$ は $\mathbf F_p[\widehat G_5]$-加群。$\widehat P:=B_3/N$、$\rho:=$ 標準射影と置けば v3 の全射証明が適用でき $\ker\rho=N$。∎

> ### ★ 代替案を採らなかった理由(**設計判断の明記**)
> 司令塔の第 2 案(marked datum の型を**全 finite kernel** へ広げてから層別)も整合的だが、採らない。理由: (a) 型を広げると $V$ が加群でない datum(非アーベル核・混合位数核)が型に入り、$W$・$\alpha$-lattice・$\operatorname{coker}\psi_W$ の**定義がそもそも書けない**行が大量に生じる (b) それらは現に $\mathcal W_{\rm adm}$ の外として **SCOPE_OUT** 済み(§6.2 の除外集合)であり、層別の実益がない。⟹ **余域制限が最小の修理**である。

### 2.3 ★ 三層宇宙(FREEZE-2)

| 層 | 定義 | 用途 |
|---|---|---|
| $\mathcal W$ | $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$c\in N$、有限指数 | ★ **参照のみ**(marked datum の型は付かない) |
| $\mathcal W_{\rm adm}$ | + $K^{(5)}/N$ が指数 $p$($p\in\{2,3\}$)の初等アーベル | ★ **在庫宇宙**(`inventory_universe`)。MARK-BIJ-adm の余域 |
| $\mathcal W_{\rm fire}$ | + **(V-cen)**($S_3$-inflate)+ $\dim_{\mathbf F_p}V\le4$ + $\lvert PB_3/N\rvert\le8000$ | ★ **発火宇宙**(`firing_universe`)。悉皆・下限主張はこの層でのみ |

> ⚠ **$\mathcal W\setminus\mathcal W_{\rm adm}$ は「空」ではない。** 指数 $p$ を超える核・混合位数核・非アーベル核は **SCOPE_OUT**(掘らない)であって、非存在の主張ではない(S-BU-6)。

---

## 3. 【blocker 3】SAT roof 節を $\neg\exists U$ 形へ

### 3.1 何が隠れていたか(**指摘の受理**)

v3 §3.1 は $\bigwedge_{\bar U\in\mathrm{RoofCand}}(\mathrm{RoofApplicable}(\bar U,\mathcal D)\to\delta_{\rm roof}(\mathcal D,U_{\bar U})\ne0)$ と書き、**像 $\bar U$ ごとに持上げ $U_{\bar U}$ を 1 つ選んで**いた。持上げ座標は SAT の**存在変数**なので、$\bar U$ 上に複数の lift があるとき、ソルバは $\delta\ne0$ になる lift を選び、**別 lift の $\delta=0$(= kill)を隠せる**。⟹ v3 の述語は S8 の生存を過大評価する。**Sol の指摘は正しい。**

### 3.2 正しい S8 生存述語(**差替・逐語**)

$$\boxed{\ \mathrm{S8SURV}(\mathcal D)\ :\iff\ \neg\,\exists\,U\trianglelefteq\widehat P\ :\ \bigl(U\cap V=1\bigr)\ \wedge\ \bigl(f_1\in\mathrm{im}(U\cap P)\bigr)\ \wedge\ \bigl(\delta_{\rm roof}(\mathcal D,U)=0\bigr)\ }$$

すなわち $\mathrm{S8SURV}(\mathcal D)\iff\forall U\in\mathrm{Roof}(\mathcal D):\delta_{\rm roof}(\mathcal D,U)\ne0$($\mathrm{Roof}(\mathcal D)=\emptyset$ なら空虚に真 = **`ROOF_VACUOUS`**・v3 §2.2)。

### 3.3 許容される符号化は 2 つだけ

| # | 符号化 | 条件 |
|---|---|---|
| **(E1)** ★ **exact 全 lift 連言** | 各像 $\bar U\in\mathrm{RoofCand}$ について**全ての** lift $U$ を**悉皆列挙**し(§4 の補題 LIFT-ENUM)、$\bigwedge_{\bar U}\bigwedge_{U\in\mathrm{Lift}(\bar U)}(\mathrm{applicable}(U)\to\delta_{\rm roof}(U)\ne0)$ を節にする | **列挙の悉皆性が cert で保証されること**(§4.3) |
| **(E2)** ★ **co-instance(別 UNSAT 系)** | 主インスタンスから roof 節を外し、得られた witness ごとに「$\exists U$ で $\delta_{\rm roof}=0$」を**別の SAT インスタンス**として解く。**SAT が返ったら witness は kill**(生存には co-instance の **UNSAT** が要る) | co-instance も mutant matrix で較正すること |

> ### ⚠ 禁止(**S-BU-14**)
> $$\boxed{\ \textbf{像 }\bar U\ \textbf{で index して lift を 1 つ選ぶ符号化を禁止する。}\ }$$
> 検出法: source-map(v3 §3.2 の `roof` タグ)で、**タグに $\bar U$ の id しか現れず lift id が無い**節群を検出したら `ROOF_QUANTIFIER_BUG / STOP`。

### 3.4 QBF は採らない

$\forall U$ を素直に表すには QBF になるが、**採らない**(工房に QBF の検証系がなく、LRAT に相当する証明書が付かない)。(E1) が第一選択、(E2) が代替である。

---

## 4. 【blocker 4】BU-GAP-10 の説明訂正と、全 lift 列挙の還元

### 4.1 訂正(**v3 §9 の当該行を差し替える**)

| | 記述 |
|---|---|
| **v3(誤)** | 「$\mathrm{Roof}(\mathcal D)$ の列挙が**すべての** $N'$ を捕まえる保証(§2.3 は $\widehat P$ 内の正規部分群として捕まえるので、**$N\subseteq N'$ でない屋根は原理的に射程外**)」 |
| ★ **v4(正)** | $N'=\rho^{-1}(U)$ ならば $N=\ker\rho\subseteq N'$ は **ROOF-TYPE から自動**であり、「$N\subseteq N'$ でない屋根」は**そもそも問題にならない**(v1 §4.1 の設定が $N=K^{(5)}\cap N'$ を課すので $N\subseteq N'$ は前提の一部)。**真の未閉点は、1 つの像 $\bar U\trianglelefteq\widehat G_5$ の上にある全ての lift $U$ を列挙できるかである。** |

### 4.2 ★ 補題 LIFT-ENUM(全 lift の構造 — 有限計算への還元)

> ### 補題 LIFT-ENUM(candidate・本書)
> $\bar U\trianglelefteq\widehat G_5$ とし $E:=\pi_{\widehat P}^{-1}(\bar U)\trianglelefteq\widehat P$ と置く($1\to V\to E\to\bar U\to1$)。このとき
> $$\mathrm{Lift}(\bar U):=\{U\trianglelefteq\widehat P\ :\ U\cap V=1,\ \pi_{\widehat P}(U)=\bar U\}\ =\ \{\,\text{$E$ における $V$ の補元で、さらに }\widehat P\text{-正規なもの}\,\}$$
> であり、
> **(a)** $\mathrm{Lift}(\bar U)\ne\emptyset$ ならば、$E$ における $V$ の補元全体は $Z^1(\bar U,V)$ の**単純推移的**な作用をもつ(補元の共役類は $H^1(\bar U,V)$ で分類される)。
> **(b)** $\widehat P$-正規性は補元上の**線型条件**である($U$ 正規 ⟺ 生成元による共役が $U$ を保つ)。
> **(c)** ⟹ $\lvert\mathrm{Lift}(\bar U)\rvert\le\lvert Z^1(\bar U,V)\rvert\le\lvert V\rvert^{\,d(\bar U)}$($d$ = 生成元数)であり、**全 lift の悉皆列挙は $\mathbf F_p$ 上の有限線型代数**である。

**証明.** 補元と $Z^1$ の対応は群拡大の標準事実(補元 $U_0$ を固定すると、他の補元は $\bar u\mapsto\delta(\bar u)u_0(\bar u)$、$\delta\in Z^1(\bar U,V)$ の形で一意に書ける)。$U\cap V=1$ かつ $\pi(U)=\bar U$ は「$U$ が $E$ 内の $V$ の補元」と同値。正規性は生成元共役の条件で、$\delta$ について $\mathbf F_p$-アフィン。∎

### 4.3 ⟹ BU-GAP-10 の新しい状態

$$\boxed{\ \textbf{【BU-GAP-10】は「数学的未閉」から「実装の悉皆性仕様」へ降格した。}\ }$$

**仕様(cert 必須欄)**: (i) 各 $\bar U$ について $Z^1(\bar U,V)$ の次元と $\lvert\mathrm{Lift}(\bar U)\rvert$ を出力 (ii) 列挙が torsor パラメータの**全域**を走ったことを示す(パラメータ空間の位数と列挙件数の一致) (iii) $H^1$ による共役類つぶしを**しない**(共役でも別 lift は別の $\delta_{\rm roof}$ を与えうるため)。**(iii) を破った実装は S-BU-14 の対象。**

---

## 5. 【blocker 5】ISO-GATE route 2 の実物 gate 要件(**設計に収載**)

> **F104-2.3**: 経路の設計採用は**承認**。ただし現 `isolated_verdict=TRUE` を `iso_gate_state=PROVEN` へ写すことは**不承認**。以下 R1〜R5 が要件である。

### 5.1 R1 — interface と、列挙の全域無重複の紙 bridge

**interface(★ Sol の指摘した未明記点)**:

| 量 | どちら側の群か | 変換 |
|---|---|---|
| 全 hexagon(3.3)(3.4)・$T_{m,f}$・settled 判定 | ★ **$\widehat P=B_3/N$** | — |
| $f$ の住む場所・charming 条件・(SURJ)・$N_{\rm ord}$ | ★ **$P=PB_3/N\cong F_2/N_{F_2}$**($c\in N$) | $\lvert\widehat P\rvert=6\,\lvert P\rvert$(**$[B_3:PB_3]=6$**) |

$$\boxed{\ \textbf{現 fixture の }g\_size=108/1000\ \textbf{は }P\ \textbf{側の位数である。}\widehat P\ \textbf{側では }648/6000\ \textbf{になる。cert に }\texttt{group\_side}\ \textbf{欄を必須化する。}\ }$$

> ### 紙 bridge B-1(candidate・本書)
> $c\in N$ とする。$N$ の GT-pair 全体は
> $$\{[m,f]\}\ \subseteq\ (\mathbf Z/N_{\rm ord})\times P,\qquad N_{\rm ord}=\mathrm{lcm}\bigl(\mathrm{ord}(\bar x),\mathrm{ord}(\bar y)\bigr)\ \ (\mathrm{ord}(\bar c)=1)$$
> の部分集合であり、**charming** の条件は $2m+1\in(\mathbf Z/N_{\rm ord})^\times$ かつ $f\in[P,P]$、**GT-shadow** はさらに (SURJ)($\langle\bar x^{2m+1},\bar f^{-1}\bar y^{2m+1}\bar f\rangle=P$・Prop 3.6)を満たすものである。
> ⟹ **列挙**「$m$ を $0,\dots,N_{\rm ord}-1$ の整数代表で走らせ、$f$ を有限群 $[P,P]$ の元として(語ではなく群の元として)1 回ずつ走らせる」は、**全域(すべての GT-pair を含む)かつ無重複(各類がちょうど 1 回)**である。
> **証明.** $[m,f]=(m+N_{\rm ord}\mathbf Z,\ fN_{F_2})$ という定義(定義ノート §2)により、$(\mathbf Z/N_{\rm ord})\times P$ の元が類の**標準形**を与える。整数代表と群の元は各類の代表を一意に定めるので無重複、定義から全域。∎
> ⚠ **語のまま列挙すると無重複が壊れる**(同じ $fN_{F_2}$ を複数の語が代表する)。**実装は群の元で列挙すること**(cert に `enumeration_domain: group_elements` を必須化)。

### 5.2 R2 — settled ⟺ bijective の **iff** の紙 bridge

> ### 紙 bridge B-2(candidate・本書)
> $[m,f]$ を $N$ の GT-shadow とし、$T_{m,f}:B_3\to B_3/N=\widehat P$(Prop 3.2: $\sigma_1\mapsto\sigma_1^{2m+1}N$、$\sigma_2\mapsto f^{-1}\sigma_2^{2m+1}fN$)とする。このとき
> $$\boxed{\ \textbf{settled}\ (\ker T_{m,f}=N)\iff \underbrace{T_{m,f}(N)=1}_{\textbf{(i) well-defined}}\ \wedge\ \underbrace{\text{誘導される }t:\widehat P\to\widehat P\ \text{が全単射}}_{\textbf{(ii) bijective}} }$$
> **証明.** ($\Rightarrow$)$\ker T_{m,f}=N$ なら $N\subseteq\ker$ ゆえ (i)、かつ誘導 $t$ は単射。$\widehat P$ は**有限**なので単射 ⟹ 全単射 ✓ (ii)。
> ($\Leftarrow$)(i) より $t$ が誘導され、$\ker T_{m,f}=$ ($t$ の核の $B_3$ における逆像)。(ii) より $\ker t=1$ ⟹ $\ker T_{m,f}=N$。∎
> ⚠ **(i) を省く実装は不可**。$N\not\subseteq\ker T_{m,f}$ の場合、$t$ はそもそも定義されないが、**素朴な実装は「生成元の像だけ見て」全単射に見える写像を作ってしまう**。⟹ **fail-closed の実装は「$\widehat P$ 上の準同型として構成を試み、構成に失敗したら `NOT_SETTLED`(または `UNKNOWN`)」**とする(GAP なら `GroupHomomorphismByImages` の `fail` を捕まえる)。
> ⚠ **isolated = 全 GT-shadow が settled**。⟹ **shadow の列挙が全域(B-1)でなければ isolated 判定は無効**。

### 5.3 R3 — mutant matrix(**6 件・全件必須**)

| # | mutant | 期待 | 何を殺すか |
|---|---|---|---|
| **M-ISO-1** | 既知 **isolated 陽性**($K^{(n)}$ 型・正典 Thm 4.3) | `TRUE` | 基本の健全性 |
| **M-ISO-2** ★ | 既知 **non-isolated 陰性** | `FALSE` | ★ **constant-TRUE を殺す**(現 cert に欠けていた一件) |
| **M-ISO-3** ★ | **constant-TRUE** 変異(判定器が常に TRUE を返す) | ★ **検出される**(M-ISO-2 で落ちる) | 現 cert が 2/2 で通してしまった穴 |
| **M-ISO-4** ★ | **settled 1 件反転**(1 個の shadow を non-settled に差し替え) | `FALSE` | 「全 shadow」の量化が効いているか |
| **M-ISO-5** ★ | **候補 1 件欠落**(列挙から shadow を 1 個落とす) | ★ **UNKNOWN or FALSE**(TRUE を返したら不合格) | B-1(全域性)の実装 |
| **M-ISO-6** ★ | **$c\notin N$** の入力 / **shadow 0 件**・前件欠落 | ★ **`UNKNOWN`**(TRUE も FALSE も返さない) | 空虚な真の混入(【W6K-GAP-1】) |

### 5.4 R4 — 第二系統

**現 helper を共有しない第二 enumerator/checker**(別言語・別データ構造)**または同等の独立紙証明**。**GAP 一出力は candidate のまま**(F104-2.3 逐語)。

### 5.5 R5 — `TRUE` と格の分離

$$\boxed{\ \texttt{isolated\_verdict}=\texttt{TRUE}\ \ \textbf{(計算出力)}\quad\ne\quad \texttt{iso\_gate\_state}=\texttt{PROVEN}\ \ \textbf{(格)}\ }$$

- `PROVEN` は **R1〜R4 がすべて閉じ、CV-9 判読を経た**場合のみ。
- **Lean を使っていない以上 `verified` と呼ばない**(cert の `verified_status` は `not verified` のまま)。
- **W-5 は `UNKNOWN (pending route-2 gate)` を保つ**(F104-2.3 逐語)。

---

## 6. 【blocker 6】cert 欄の別化と scope 文言

### 6.1 ★ `inventory_universe` / `firing_universe` の別欄化(**必須**)

```
inventory_universe:  { layer: "(V-cen) / S3-inflated", p: [2,3], dim: [2,3,4],
                       note: "在庫のみ。探索完全性の分母に足さない。" }
firing_universe:     { layer: "(V-cen) / S3-inflated", p: [2,3], dim_p2: [2,3,4],
                       dim_p3: [2], window_order_cap: 8000,
                       note: "悉皆・下限主張はこの層に限る(F103-2.2 の 4 前件つき)。" }
completeness_denominator: firing_universe   # ★ 28 行を足さない
```

| cert | 行数 | 位置づけ(v4 で確定) |
|---|---|---|
| `h2_census_s4_20260805.json` | 17 | ★ **在庫 + 発火宇宙の交わり**(p=2 dim2–4 の 12 + p=3 dim2 の 5) |
| `h2_census_s4_p3ext_20260805.json` | 28 | ★ **探索宇宙外 supplemental inventory**(p=3 dim3/4 = window order 13,500 / 40,500)。**分母に足さない**(F104-2.4 逐語) |

### 6.2 scope_out 文言の差替(**両 cert 共通・新版で反映**)

| 旧 | ★ 新 |
|---|---|
| `non_elementary_abelian_core (C4,C9,noncyclic)` | **`core_exponent_gt_p_or_nonabelian`**(核の指数が $p$ を超える、または非アーベル。**非巡回初等アーベル核は射程内**) |
| `non-central F_p[S4]-modules ... NOT_ENUMERATED_THIS_PASS` | **`SCOPE_OUT (universe narrowed by design v3 §5 / v4 §2.3)`** |
| (新設) | **`kernel_not_single_prime_elementary_abelian` → `SCOPE_OUT`**($\mathcal W\setminus\mathcal W_{\rm adm}$・§2.3) |

> ⚠ **過去 cert は不改変。** 新版 cert で反映する(ep-keeper 案件)。**測定値の再走は不要**(欄と文言のみ)。

### 6.3 ★ 補題 F3S3 の型数(**母関数・dim 2/3/4 = 5/10/18**)

> ### 補題 F3S3-COUNT(candidate・本書 / Sol が 10・18 を批准)
> $\mathbf F_3S_3$ の不可分解加群は、$P(\mathbf 1)=\mathbf 1\vert\mathrm{sgn}\vert\mathbf 1$ と $P(\mathrm{sgn})=\mathrm{sgn}\vert\mathbf 1\vert\mathrm{sgn}$ の商として得られる **6 個**で、次元は $1,2,3$ の二系列。Krull–Schmidt により
> $$\sum_{n\ge0}\#\{\dim n\ \text{の加群}\}\,x^n=\frac{1}{(1-x)^2(1-x^2)^2(1-x^3)^2}=1+2x+\mathbf 5x^2+\mathbf{10}x^3+\mathbf{18}x^4+30x^5+\cdots$$
> ⟹ $\dim=2,3,4$ の型数は **5 / 10 / 18**。

⟹ cert の $p=3$ 行数(dim2 = 5、dim3/4 の 28 = 10 + 18)と一致。
⚠ **型数の一致だけから $H^2/H^1$ の値を `cross-checked` へは上げない**(F104-2.1 逐語)。**cert は single cohomology implementation の candidate inventory のまま。**

---

## 7. 停止規則(v4 追加分・FREEZE-4)

| # | trigger | verdict |
|---|---|---|
| **S-BU-14** ★新 | roof 節を**像 $\bar U$ で index して lift を 1 つ選ぶ**符号化(または $H^1$ で共役類をつぶす lift 列挙)を検出 | `ROOF_QUANTIFIER_BUG / STOP` |
| **S-BU-15** ★新 | `isolated_verdict=TRUE` を、R1〜R4 未閉のまま `iso_gate_state=PROVEN` へ写した | `ISO_GRADE_OVERCLAIM / STOP` |
| **S-BU-16** ★新 | supplemental inventory(28 行)を探索完全性の**分母**に加算した | `DENOMINATOR_INFLATION / STOP` |
| S-BU-1〜13 | v3 のまま | — |

---

## 8. 【GAP】更新

| 札 | 状態(v4) |
|---|---|
| **【BU-GAP-10】** | ★ **降格**: 数学的未閉 → **実装の悉皆性仕様**(§4.3)。補題 LIFT-ENUM が有限線型代数に還元 |
| **【BU-GAP-8】** | **UNKNOWN(最大の律速)**。route 2 gate の R1〜R4(§5)が閉じるまで全 datum は ISO `UNKNOWN` |
| **【BU-GAP-6】** | **UNKNOWN**。SM-4 の全数照合に **$\neg\exists U$ 形の roof 節**を含めること(§3.2)が追加条件 |
| **【BU-GAP-9】/【K5-GAP-W1】** | 不変(非中心層は SCOPE_OUT・非中心版 SURJ は未閉) |
| **【BU-GAP-11】** ★新 | $\mathcal W_{\rm adm}$ の外(指数 $p$ 超・非アーベル核)は **SCOPE_OUT**。$\mathcal W\setminus\mathcal W_{\rm adm}$ の悉皆性は**構造的に主張しない** |

---

## 9. 司令塔への申し送り

1. ★★★ **本書は凍結を請求する**(§1・FREEZE-1〜5)。**発火請求は S1〜S3.5 のみ**で、S3.6 以降は route 2 gate 閉鎖まで請求しない。
2. ★★★ **route 2 gate の R1〜R4 が W-6 掘削の最大の律速**(§5)。**R1/R2 の紙 bridge は本書が証明済み**なので、残りは **R3(mutant 6 件)・R4(第二系統)の実装**である。⟹ **implementer / ep-keeper への発注仕様として §5.3・§5.4 をそのまま使える。**
3. ★★ **新版 cert 3 本の起票**(過去 cert 不改変・**測定値の再走不要**): (a) S0 cert の `stop_rule_status` 文字列(v3 §6.3)(b)(c) census 2 本の `inventory_universe`/`firing_universe` 別欄化 + `scope_out` 文言(§6.1・§6.2)+ `group_side` 欄(§5.1)。
4. ★ **補題 LIFT-ENUM・B-1・B-2・F3S3-COUNT** は本書の新規小補題。**便 105 の監査対象**に載せられたい。
5. ⚠ **W-5 は `UNKNOWN (pending route-2 gate)`** のまま(F104-2.3 逐語)。**下限 4,000/13,500 の引用は 4 前件 + (V-cen) 縮小の前件つき**(§1.3)。
