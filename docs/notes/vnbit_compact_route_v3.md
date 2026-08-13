# vN-BIT compact route **v3** — pure anchor 修復・monomial lift の凍結・8 候補は **2 類**

- 起草: 影工房 **数学者**(Claude / Opus 5)/ 2026-08-13
- 委嘱: 司令塔(裁定 1155)「(1) C-2′ 必須欄 (2) monomial lift の versioned 凍結 (3) 8 候補の同値性 (4) SURJ-LIN 再計算と P-vNC2 再凍結の要否」
- **関連既存定理**: **LIFT-AFF / GEN-AFF / MARK / SURJ-LIN**(私の v1・v2)/ **BU-S35 §26・§43・§61**($\rho(\sigma_1)=\tau'^{-1}\theta'$, $\rho(\sigma_2)=\theta'^{-1}\tau'^2$, $\theta=\mathrm{Ad}(\Delta)$, $\tau=\mathrm{Ad}(\delta)$)/ 定理 **M1**($Y=\tau(X)$)/ 便 130・131 cert(凍結済)
- v1・v2 は**不改変**(versioned 規律)。
- **規律**: u/c 非接触・封印 3 量非接触・prereg 非抵触。**novelty 表は grep 出力のコピーのみ**(規律 GREP-3)。

---

## 0. 結論(先に 4 行)

1. ★★★ **8 候補はちょうど 2 類**(委嘱 3)。gauge 群 $=\mathrm{End}_W(V)^\times=\{\pm1\}^3$(Schur)、共役核 $\{\pm I\}$ ⟹ **実効 gauge 群の位数 4**。分類器は
   $$\boxed{\ H^1\bigl(S_3,\ \mathbf F_2^3\bigr)\cong\mathbf F_2\quad(\textbf{位数 2・機械確認})\ }$$
   ⟹ $8=2\ \text{類}\times4\ \text{gauge}$ ✓。**同一類内は同じ窓核・異なる類は別窓**。
2. ★ **数学的に自然な正規化がある**(委嘱 2): $H^1(C_3,\mathbf F_2^3)=\mathbf 0$ ゆえ **$\tau'$ の符号は全部 gauge で消せる** ⟹ 正規形は $\tau'=$ 符号なし。残る本質的自由度は **$\theta'$ の固定ブロック(block 2)の符号 1 ビットのみ**($H^1(C_2,\mathbf F_2^3)=\mathbf F_2$)。⟹ **辞書順は要らない — 1 ビットの名前で凍結できる**。
3. ★★ **P-vNC2 系は再凍結が必要**(委嘱 4)。標識が変わると $\dim\ker(I+\theta')$ が変わる。**予言**:
   $$\boxed{\ \dim\ker(I+\theta')\in\{11,10\},\quad \dim Z^1\in\{25,24\},\quad \lvert H^1(C_2*C_3,V)\rvert\in\{\mathbf{81},\ \mathbf{27}\}\ }$$
   $\dim\ker(I+\tau'+\tau'^2)=\mathbf{14}$ は**不変**($H^1(C_3,\mathbf F_2^3)=0$ の帰結)。
4. ⟹ **測定対象は 2 窓**。コストは 2 倍(2 × ≤81 類 × 324 行)= 依然として数秒。

---

## 1. 委嘱 1 — C-2′ 必須欄

### 1.1 追加する等式

BU-S35 §26 の $\rho(\sigma_1)=\tau'^{-1}\theta'$, $\rho(\sigma_2)=\theta'^{-1}\tau'^2$ と、$PB_3$ の純生成元 $x=\sigma_1^2$, $y=\sigma_2^2$ より:

$$\boxed{\ \textbf{(A1)}\quad \bigl((\tau')^{-1}\theta'\bigr)^2=\rho(X),\qquad
\textbf{(A2)}\quad \bigl((\theta')^{-1}(\tau')^2\bigr)^2=\rho(Y)\ }$$

**cert 必須欄**(`pure_anchor`):
```
pure_anchor : { A1_holds: bool, A2_holds: bool,
                rho_X_block_signs: [s1,s2,s3], rho_Y_block_signs: [t1,t2,t3],
                residual_rank_A1: int, residual_rank_A2: int }   # 不一致時の差 rank
```
**A1_holds ∧ A2_holds が false なら測定を実行しない。**

### 1.2 ★ 符号パターンの整合検査(**私が追加する無料の検査**)

$V$ の block $i$ 上で $W=P\times G_3$ は $\rho_P\otimes\chi_i$ で作用するので
$$\rho(X)=\mathrm{diag}\bigl(\chi_1(\bar X)R_X,\ \chi_2(\bar X)R_X,\ \chi_3(\bar X)R_X\bigr),\qquad \bar X:=X\ \text{の}\ G_3\ \text{像}.$$

- $G_3^{\rm ab}\cong C_2\times C_2$(機械確認済・v2 §8)で、$C_2^2$ の**非単位元は 3 つの指数 2 部分群のうち**ちょうど 1 つ**に属する** ⟹
  $$\boxed{\ \bar X\neq1\ \Longrightarrow\ (\chi_1,\chi_2,\chi_3)(\bar X)\ \textbf{は }+1\ \textbf{がちょうど 1 個}\ }$$
  ⟹ 便 131 の実測 $\rho(X)=\mathrm{diag}(-R_X,R_X,-R_X)$ は **$(-,+,-)$ = $+$ が 1 個** ✓ **整合**。
- **定理 M1**($Y=\tau(X)$)と $\tau'$ のブロック巡回より
  $$\boxed{\ \rho(Y)\ \textbf{の符号パターンは }\rho(X)\ \textbf{の巡回シフト}\ }$$
  ⟹ $(-,+,-)$ に対し $\rho(Y)$ は $(-,-,+)$ か $(+,-,-)$ の**いずれか**でなければならない。
- ⚠ **$\bar X=1$ なら $\rho(X)=\mathrm{diag}(R_X,R_X,R_X)$(符号なし)** ⟹ 便 131 の実測と矛盾するので $\bar X\ne1$ が従う。**この 1 行を cert に記録**(窓が $G_3$ 方向に非自明であることの確認 = テンソル型の実証)。

**cert 必須欄(追加)**: `sign_pattern_check : { X_plus_count: 1, Y_is_cyclic_shift_of_X: bool, Xbar_nontrivial_in_G3ab: bool }`

---

## 2. 委嘱 3 — 8 候補の同値性:**定理 TWIST-2**

### 2.1 gauge 群の同定

> ### 補題 GAUGE
> $V=\bigoplus_{i=1}^3 V_i'$($V_i'=V_7\otimes\chi_i$、相異なる絶対既約 $W$-加群)。Schur の補題より
> $$\mathrm{End}_W(V)=\prod_{i=1}^3\mathrm{End}_W(V_i')=\mathbf F_3^3,\qquad \mathrm{End}_W(V)^\times=\{\pm1\}^3\ (\text{位数 }8).$$
> $D\in\{\pm1\}^3$ による共役は $\rho|_W$ を**点ごとに固定**し、$(\theta',\tau')\mapsto(D\theta'D^{-1},D\tau'D^{-1})$ を与える。共役で自明に作用するのは中心 $\{\pm I\}$ のみ ⟹ **実効 gauge 群の位数 4**(機械確認)。

⚠ **前件**: $V_7$ が $\mathbf F_3$ 上**絶対既約**であること。⟹ **gating C-9** に追加(`IsAbsolutelyIrreducible` 1 行)。可約なら $\mathrm{End}$ が大きくなり gauge 群が変わる。

### 2.2 ★ gauge 同値 ⟹ **窓核が同一**

> ### 命題 SAME-KERNEL
> $\phi_1:B_3\to\tilde E_1$、$\phi_2=\mathrm{Ad}(D)\circ\phi_1:B_3\to\tilde E_2=D\tilde E_1D^{-1}$ とすると
> $$\ker\phi_2=\ker\phi_1 .$$
> ⟹ **gauge 同値な monomial lift は文字どおり同じ窓 $N_E\subseteq PB_3$ を定める。**

**証明**. $\mathrm{Ad}(D)$ は単射なので $\ker(\mathrm{Ad}(D)\circ\phi_1)=\ker\phi_1$。∎

### 2.3 ★★★ 定理 TWIST-2(分類)

> ### 定理 TWIST-2
> $\rho|_W$ を固定したときの $\bar W$ への monomial 拡張の gauge 類は
> $$H^1\bigl(\bar W/W,\ \mathrm{End}_W(V)^\times\bigr)=H^1\bigl(S_3,\ \mathbf F_2^3\bigr)\cong\mathbf F_2$$
> で分類される(Clifford 理論の標準形)。⟹ **ちょうど 2 類**。
>
> **機械確認**(規約統一版・§8): $\dim Z^1=3$, $\dim B^1=2$, $\dim H^1=1$, $\lvert H^1\rvert=\mathbf 2$。
> **勘定の一致**: 8 候補 $\div$ 実効 gauge 4 $=\mathbf 2$ ✓✓

**⟹ 委嘱 3 の答え**:
$$\boxed{\ \textbf{8 候補は }\mathbf 2\ \textbf{つの窓に対応する。}\ \textbf{同一類の 4 個は同じ核・別類は別窓。}\ }$$
$$\boxed{\ \textbf{仕様}:\ \mathbf 2\ \textbf{窓を}\textbf{両方測る}\ \textbf{(コスト 2 倍 = 数秒)。片方だけ測って結論しない。}\ }$$

★ **P-vNC3-1(凍結)**: 実効 gauge 群(位数 4)は 8 解に**自由に**作用する ⟹ **軌道は 2 個・各サイズ 4**。(自由でなければ $\lvert H^1\rvert=2$ と矛盾 ⟹ 実装バグまたは補題 GAUGE の前件破綻。)

---

## 3. 委嘱 2 — 正規化と versioned 凍結

### 3.1 ★ 数学的に自然な正規化がある

因子ごとに符号の自由度を見る(機械確認・§8):

| 部分群 | 加群 | $H^1$ | 意味 |
|---|---|---|---|
| $C_3=\langle\tau\rangle$(3 ブロック巡回) | $\mathbf F_2^3=\mathbf F_2[C_3]$(**自由**) | $\mathbf 0$ | ★ **$\tau'$ の符号は全部 gauge で消せる** |
| $C_2=\langle\theta\rangle$(block 1,3 交換・2 固定) | $\mathbf F_2^3=\mathbf F_2[C_2]\oplus\mathbf F_2$ | $\mathbf F_2$ | ★ **block 2 の符号 1 ビットだけが本質的** |
| $S_3$(全体) | $\mathbf F_2^3$ | $\mathbf F_2$ | 上と整合(2 類) |

> ### 正規形 NORM-TWIST(**辞書順ではなく不変量で固定**)
> $$\boxed{\ \tau'\ \textbf{の 3 ブロック符号を }(+,+,+)\ \textbf{に gauge 固定する。}\ \textbf{残る 1 ビットは }\theta'\ \textbf{の block 2 符号 }\epsilon\in\{+,-\}\ }$$
> ⟹ 2 窓を **`class = "+"`** と **`class = "-"`** と名づけて versioned に凍結する。
> ⚠ 便 131 の辞書順先頭 $\tau'=\tau\cdot\mathrm{diag}(I_7,-I_7,-I_7)$ は**この正規形ではない**($\tau$ 符号が残っている)⟹ gauge で $(+,+,+)$ に移してから $\epsilon$ を読むこと。

★ **委嘱文の「なければ辞書順先頭の採用を宣言」に対する回答: 辞書順は不要。$\epsilon$ という 1 ビットの不変量で名前が付く。** ただし $\epsilon$ の符号の**向き**(どちらを $+$ と呼ぶか)は $B$($=\theta'$ の block 2 の $7\times7$ 部)の取り方に依存するので、**`B` の digest を cert に束縛**して規約を固定する。

### 3.2 凍結する版

```
marking_version : "vnbit-monomial/v3"
tau_signs       : [+1,+1,+1]              # NORM-TWIST で gauge 固定
theta_block2_eps: "+" | "-"               # ★ 本質的な 1 ビット = 窓の名前
B_matrix_sha256 : <theta' の block 2 の 7x7 部の digest>   # eps の向きの規約固定
gauge_orbit_size: 4                        # P-vNC3-1 の検査
```

---

## 4. 委嘱 4 — SURJ-LIN 再計算と P-vNC2 の**再凍結は必要**

### 4.1 何が変わり、何が変わらないか

| 量 | 変わるか | 理由 |
|---|---|---|
| $\dim\ker(I+\tau'+\tau'^2)=\mathbf{14}$ | ★ **不変** | $H^1(C_3,\mathbf F_2^3)=0$ ⟹ $\tau'$ は常に符号なし形に gauge 共役 ⟹ v2 §1.2 の「3 ブロック巡回 ⟹ $\mathrm{rank}=7$」がそのまま効く |
| $\dim\ker(I+\theta')$ | ★ **変わる** | 交換部(block 1,3)の寄与は符号によらず $7$(**私の紙証明・§4.2**)。**block 2 の符号 $\epsilon$ が $(-1)$-固有空間を $d\leftrightarrow7-d$ と入れ替える** |
| $\dim B^1=21$ | 不変 | $V$ は $\bar W$-既約・非自明 ⟹ $V^{\bar W}=0$ |
| $\dim H^1(C_2*C_3,V)$、$\lvert H^1\rvert$ | ★ **変わる** | 上の帰結 |

### 4.2 補題(交換部の寄与は符号によらない)

> ### 補題 SWAP-7
> $\theta'$ が block 1,3 を交換する部分を $\theta'(v_1,v_3)=(s_1Av_3,\ s_3Cv_1)$ と書き、$(\theta')^2=I$ を課すと $s_1s_3AC=I$。このとき
> $$\dim\ker(I+\theta')\big|_{\text{block }1,3}=7\qquad(\textbf{符号 }s_1,s_3\ \textbf{によらない}).$$

**証明**. $v_1+s_1Av_3=0\Rightarrow v_1=-s_1Av_3$。第 2 式に代入すると $v_3-s_1s_3CAv_3$。$C=s_1s_3A^{-1}$ より $s_1s_3CA=I$ ⟹ 恒等的に $0$。⟹ $v_3\in V_7$ は自由、$v_1$ は決まる ⟹ 次元 $7$。∎

### 4.3 ★★ 再凍結する予言

便 130 の(符号なし)実測 $\dim\ker(I+\theta)=11$ から $d=11-7=4$ と読める。⟹

> ### P-vNC3-2(★ 凍結・強い予言)
> | 窓 | $\dim\ker(I+\theta')$ | $\dim Z^1$ | $\dim H^1$ | $\lvert H^1\rvert$ = 類の個数 |
> |---|---:|---:|---:|---:|
> | $\epsilon=+$ | $7+4=\mathbf{11}$ | $\mathbf{25}$ | $\mathbf 4$ | $\mathbf{81}$ |
> | $\epsilon=-$ | $7+3=\mathbf{10}$ | $\mathbf{24}$ | $\mathbf 3$ | $\mathbf{27}$ |
>
> **和は必ず $11+10=21$**(補題 SWAP-7 と $d+(7-d)=7$ から)。⟹ **どちらか一方が 11、他方が 10 でなければ実装バグ。**

### 4.4 SURJ-LIN の再計算指示

**定理 SURJ-LIN(v2 §1.3)の形は不変**:
$$\#\{\text{全射を与える類}\}=\lvert H^1(C_2*C_3,V)\rvert-\lvert H^1(\bar W,V)\rvert$$
ただし **両項とも $\epsilon$ ごとに計算し直す**($\bar W$ の $V$ 上の作用が $\epsilon$ で変わるため)。⟹

> ### 実行指示 SL-RE
> ```
> for eps in {+,-}:
>     rho_eps := NORM-TWIST 正規形の (theta',tau')
>     C-2' の A1/A2 を検査(false なら停止)
>     dimZ1 := dim ker(I+theta') + 14            → P-vNC3-2 の検査
>     Zbar  := OneCocycles(barW_eps, V)          → 仕様 GEN-SUB(v2 §2.1)
>     surj_classes := H^1 類 \ infl(Zbar)
>     段 1–5 を実行(v2 §4)
> 報告: eps ごとの |Im R| と Θ_2 rigidity、および両者の一致/不一致
> ```

⚠ **v1/v2 の P-vNC-* / P-vNC2-* のうち、$\dim Z^1=25$・$\lvert H^1\rvert=81$ を前提にした行は本稿 P-vNC3-2 で置換される**(versioned: 旧予言は不改変・本稿が supersede)。$\lvert GT(N_W)\rvert=324$・$\Theta_1$ rigid・$\lvert\mathrm{Im}R\rvert\in\{972,324\}$・$\mathrm{rank}(A_1)=\mathrm{rank}(A_2)$ は**標識に依存しないので有効のまま**。

---

## 5. cert schema `vnbit_compact/v3`(v2 への差分)

```
pure_anchor       : { A1_holds, A2_holds, rho_X_block_signs, rho_Y_block_signs,
                      residual_rank_A1, residual_rank_A2 }           # ★ §1.1
sign_pattern_check: { X_plus_count: 1, Y_is_cyclic_shift_of_X,
                      Xbar_nontrivial_in_G3ab }                       # ★ §1.2
gauge             : { End_W_V: "F_3^3", gauge_group_order: 8,
                      effective_gauge_order: 4, anchor_solutions: 8,
                      orbit_count: 2, orbit_sizes: [4,4],             # ★ P-vNC3-1
                      H1_S3_F2_3_order: 2 }
marking_version   : "vnbit-monomial/v3"
window            : { eps: "+"|"-", tau_signs: [+1,+1,+1],
                      B_matrix_sha256, V7_absolutely_irreducible }    # ★ C-9
per_eps           : [ { eps, dim_ker_I_plus_theta, dimZ1, H1_order,
                        H1_barW_order, surjective_class_count,
                        lift_table[324], theta2_rigid, Im_R_size } × 2 ]
cross_eps         : { dim_ker_sum_is_21: bool, Im_R_agrees: bool }    # ★ P-vNC3-2/3
```

---

## 6. 予言(prereg・走行前に凍結)

| # | 予言 | 根拠 |
|---|---|---|
| **P-vNC3-1** | anchor 解 8 個に実効 gauge 群(位数 4)が**自由に**作用 ⟹ **軌道 2 個・各 4** | 定理 TWIST-2 + $\lvert H^1(S_3,\mathbf F_2^3)\rvert=2$ |
| **P-vNC3-2** | $\dim\ker(I+\theta')$ は 2 窓で $\{11,10\}$、**和は 21**。$\lvert H^1(C_2*C_3,V)\rvert$ は $\{81,27\}$ | 補題 SWAP-7 + $H^1(C_2,\mathbf F_2^3)=\mathbf F_2$ |
| **P-vNC3-3** | $\dim\ker(I+\tau'+\tau'^2)=\mathbf{14}$ は**両窓で同じ** | $H^1(C_3,\mathbf F_2^3)=0$ |
| **P-vNC3-4** | $\rho(Y)$ の符号パターンは $\rho(X)$ の**巡回シフト**、$+$ はそれぞれ 1 個 | 定理 M1 + $G_3^{\rm ab}=C_2^2$ |
| **P-vNC3-5**(★ 弱い見立て) | 2 窓は**同じ** $\lvert\mathrm{Im}R\rvert$ を与える。外れたら「窓の 1 ビットが答えを変える」= 重要 | heuristic のみ・**証明ではない** |
| (継承) | $\lvert GT(N_W)\rvert=324$ / $\Theta_1$ rigid / $\lvert\mathrm{Im}R\rvert\in\{972,324\}$ / $\mathrm{rank}A_1=\mathrm{rank}A_2$ / $\Theta_2$ は rigid でない(弱い見立て) | v1・v2(標識非依存) |

---

## 7. novelty grep 領収書(規律 GREP-3: **実行後にコピー**・自分の新規ファイル除外)

```
$ grep -rn "monomial" docs/ sol/ | grep -v vnbit_compact | wc -l
122    → ★既出(多数・一般技術)
$ grep -rn "gauge 類|gauge orbit|ゲージ類" docs/ sol/ | grep -v vnbit_compact | wc -l
1      → 便131 の入力
$ grep -rn "Clifford|Schur.*End_W|End_W(V)" docs/ sol/ | grep -v vnbit_compact | wc -l
19     → ★既出(Clifford/Schur は工房の標準道具)
$ grep -rn "H\^1(S_3|Shapiro|シャピロ" docs/ sol/ | grep -v vnbit_compact | wc -l
18     → ★既出(一般文脈)
$ grep -rn "twist 類|twist class|捻り類" docs/ sol/ | grep -v vnbit_compact | wc -l
0      → ★新規(定理 TWIST-2 の呼称)
$ grep -rn "pure anchor|純アンカー" docs/ sol/ | grep -v vnbit_compact | wc -l
1      → 便131 の入力
```

| 主張 | 判定 |
|---|---|
| monomial 拡張・Clifford・Schur・Shapiro | ★ **既出**(122 / 19 / 18 件)— **一般技術として依拠** |
| **定理 TWIST-2(この 8 候補が $H^1(S_3,\mathbf F_2^3)=\mathbf F_2$ で 2 類)** | 個別適用の記述は grep 0 ⟹ ★ **本稿の増分** |
| **補題 SWAP-7(交換部の寄与は符号によらず 7)** | grep 0 ⟹ ★ **新規**(小さいが P-vNC3-2 の要) |
| **正規形 NORM-TWIST($\tau'$ 符号は消せる・本質は 1 ビット)** | grep 0 ⟹ ★ **新規** |
| 符号パターン整合検査(§1.2) | $G_3^{\rm ab}=C_2^2$ は私の v2 §8 の既測。**組合せ論的帰結が増分**(小) |
| $H^1(S_3,\mathbf F_2^3)$ 等の値 | **古典**(Shapiro)。本稿は**機械で裏取り**したのみ |

---

## 8. 検算(機械生成の数値の出所)

inline(本便)。Sol のコード非使用・標準ライブラリのみ。**規約統一版**(積 $(gh)(i)=g(h(i))$、作用 $(g\cdot v)_i=v_{g^{-1}(i)}$)。

| 検査 | 出力 |
|---|---|
| $H^1(S_3,\mathbf F_2^3)$ | $\dim Z^1=3$, $\dim B^1=2$, $\dim H^1=1$, $\lvert H^1\rvert=\mathbf 2$ |
| $H^1(C_3,\mathbf F_2^3)$ | $\dim H^1=\mathbf 0$, $\lvert H^1\rvert=1$ ⟹ **$\tau'$ 符号は全部 coboundary** |
| $H^1(C_2^{\rm swap(1,3)},\mathbf F_2^3)$ | $\dim H^1=1$, $\lvert H^1\rvert=\mathbf 2$ ⟹ **block 2 の 1 ビットだけ本質的** |
| gauge 勘定 | $\lvert\{\pm1\}^3\rvert=8$、共役核 $\{\pm I\}=2$、実効 $=4$、$8/4=\mathbf 2$ ✓ |
| P-vNC3-2 の 2 値 | $d=4$ ⟹ $(11,10)$、$\dim Z^1=(25,24)$、$\lvert H^1\rvert=(\mathbf{81},\mathbf{27})$ |

⚠ **初回計算の誤りを自己記帳**: 最初の $H^1$ 実装は積の規約($g\circ h$ か $h\circ g$)と作用の規約が不整合で、$S_3$ に対し $\dim H^1=-1$ という不合理な値を出した(非可換群でのみ露見)。**規約を統一して再計算し、$C_2$・$C_3$ の既知値(Shapiro)で較正してから採用した**。上表は再計算後の値。

**格付け**: §8 の $H^1$ = **機械・単系統**(古典値との照合つき)。定理 TWIST-2 / 命題 SAME-KERNEL / 補題 GAUGE / 補題 SWAP-7 = **paper-proof(単系統・Sol 未監査)**。§1.2 / §5 = **設計**。**verified ではない。** u/c・封印 3 量・prereg 非接触。

---

## 9. 司令塔への回答(4 行)

1. **委嘱 1**: (A1)(A2) を `pure_anchor` 必須欄に。★ 無料の追加検査として **$\rho(X)$ の $+$ は 1 個・$\rho(Y)$ は $\rho(X)$ の巡回シフト**($G_3^{\rm ab}=C_2^2$ と定理 M1 から)を入れた。便 131 の実測 $(-,+,-)$ は**整合**。
2. **委嘱 3**(先に答える): **8 候補はちょうど 2 窓**。gauge 群 $=\mathrm{End}_W(V)^\times=\{\pm1\}^3$(Schur・前件 = $V_7$ の絶対既約性 ⟹ **C-9 に追加**)、実効位数 4、分類器 $H^1(S_3,\mathbf F_2^3)=\mathbf F_2$(機械)。同一類は**同一核**(命題 SAME-KERNEL)。⟹ **2 窓を両方測る**(数秒)。
3. **委嘱 2**: **辞書順は不要**。$H^1(C_3,\mathbf F_2^3)=0$ より $\tau'$ の符号は全部 gauge で消せ、本質は **$\theta'$ の block 2 の 1 ビット $\epsilon$** のみ(正規形 NORM-TWIST)。⟹ 2 窓を `eps="+"`/`eps="-"` として versioned 凍結。$\epsilon$ の向きは `B_matrix_sha256` で規約固定。
4. **委嘱 4**: ★ **再凍結が必要**。$\dim\ker(I+\theta')$ は $\{11,10\}$ で**和は必ず 21**(補題 SWAP-7)、$\lvert H^1(C_2*C_3,V)\rvert$ は $\{\mathbf{81},\mathbf{27}\}$ — **強い falsifiable 予言 P-vNC3-2**。$\dim\ker(I+\tau'+\tau'^2)=14$ と $\lvert GT(N_W)\rvert=324$・$\Theta_1$ rigid・$\lvert\mathrm{Im}R\rvert\in\{972,324\}$ は**標識非依存で有効**。SURJ-LIN の形も不変で、両項を $\epsilon$ ごとに再計算するだけ(実行指示 SL-RE)。
