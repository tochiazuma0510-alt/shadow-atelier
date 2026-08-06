# 【EDIM-GAP-1】設計 — $\mathfrak t=\mathrm{gr}(K(0,5))$ の**半直積直接実現**($k=8\ldots12$ への道)

**状態札: `design / candidate / Sol 未監査 / 窓ゼロ・GAP ゼロ・封印非接触 / 機械 = 付録の分数演算 1 本(scratchpad/semidirect.py)/ 実装は未着手`**

- 起草: 影工房 数学者(Claude / Opus 5)・2026-08-06
- 委嘱: 裁定 646【1】「半直積直接実現 — $x,y$ の $\{a_i\}$ 上微分作用の明示形を導出し、$k=8..12$ への実装スペックを実装係へ渡せる粒度で。$k=7$ 改修は fallback へ降格」
- 動機: イデアル商方式は $k=8$ で **21.1 GB**(8GB 不能)。本設計はその路線を**置換**する。

---

## 0. 結論(3 行)

> 1. ★ **微分作用の明示形が出た**(§2)。$\mathfrak n=\mathrm{Lie}(A,B,C)$、$\mathfrak h=\mathrm{Lie}(X,Y)$ として
> $$\delta_X:\ A\mapsto[A,B],\ B\mapsto-[A,B],\ C\mapsto0;\qquad \delta_Y:\ A\mapsto0,\ B\mapsto[B,C],\ C\mapsto-[B,C].$$
> 2. ★ **$\rho$ も次数 1 で明示形が出て、$\rho^5=\mathrm{id}$ が機械確認できた**(§3・付録)。
> 3. ★ **規模が 2〜3 桁縮む**: $k=12$ で イデアル方式の周囲次元 $\mathrm{Witt}(5,12)=20{,}343{,}700$ に対し、本方式は $\dim\mathfrak t_{12}=44{,}555$ — **457 倍小さい**(§4)。

---

## 1. 模型(candidate)

$K(0,5)\to K(0,4)$(第 5 点を忘れる)は分裂ファイブレーションで、$K(0,5)\cong F_3\rtimes F_2$。graded で
$$\boxed{\ \mathfrak t=\mathfrak n\rtimes\mathfrak h,\qquad \mathfrak n=\mathrm{Lie}(A,B,C)\ \text{自由},\quad \mathfrak h=\mathrm{Lie}(X,Y)\ \text{自由}\ }$$
$$A:=t_{15},\quad B:=t_{25},\quad C:=t_{35},\qquad X:=t_{12},\quad Y:=t_{23},$$
$t_{45}=-(A+B+C)$(頂点 5 の球面関係 $\sum_{j\ne5}t_{j5}=0$)。

**元の表示**: $(n,h)$、$n\in\mathfrak n$、$h\in\mathfrak h$。**括弧**:
$$\bigl[(n_1,h_1),(n_2,h_2)\bigr]=\bigl(\,[n_1,n_2]+\delta_{h_1}(n_2)-\delta_{h_2}(n_1),\ [h_1,h_2]\,\bigr)$$
$\delta:\mathfrak h\to\mathrm{Der}(\mathfrak n)$ は $X\mapsto\delta_X,\ Y\mapsto\delta_Y$ の**一意な Lie 準同型拡張**($\mathfrak h$ が自由ゆえ拡張は自動・矛盾なし)。

---

## 2. ★ 微分作用の導出(**紙 4 行**)

Drinfeld–Kohno の (R2): 三点 $\{i,j,5\}$ で $[t_{i5},\,t_{ij}+t_{j5}]=0$ ⟹
$$\boxed{\ [t_{ij},\,t_{i5}]=[t_{i5},\,t_{j5}]\ }$$
(R1): $\{i,j\}\cap\{k,5\}=\emptyset$ なら $[t_{ij},t_{k5}]=0$。これだけで:

| | $A=t_{15}$ | $B=t_{25}$ | $C=t_{35}$ |
|---|---|---|---|
| $\delta_X=\mathrm{ad}(t_{12})$ | $[t_{12},t_{15}]=[t_{15},t_{25}]=\ \boxed{[A,B]}$ | $[t_{12},t_{25}]=[t_{25},t_{15}]=\ \boxed{-[A,B]}$ | $\boxed{0}$(非交差) |
| $\delta_Y=\mathrm{ad}(t_{23})$ | $\boxed{0}$(非交差) | $[t_{23},t_{25}]=[t_{25},t_{35}]=\ \boxed{[B,C]}$ | $[t_{23},t_{35}]=[t_{35},t_{25}]=\ \boxed{-[B,C]}$ |

**整合性検査(紙)**: $\delta_X(A+B+C)=[A,B]-[A,B]+0=0$、$\delta_Y(A+B+C)=0+[B,C]-[B,C]=0$。すなわち両微分は $t_{45}=-(A+B+C)$ を殺す — $[t_{12},t_{45}]=[t_{23},t_{45}]=0$(非交差)と**一致**。★ これが導出の自己検査である。

---

## 3. ★ $\rho$ と $j$ の明示形

球面関係 5 本を解くと(付録 A・分数演算):
$$T_1=X,\quad T_2=Y,\quad T_3=t_{34}=X+A+B,\quad T_4=t_{45}=-(A+B+C),\quad T_5=t_{15}=A.$$
($t_{13}=-(X+Y+A+B+C)$, $t_{14}=Y+B+C$, $t_{24}=-(X+Y+B)$ も同時に出る。)
$\rho:T_i\mapsto T_{i+3\ (\mathrm{mod}\ 5)}$ を次数 1 で解くと **一意**に:

$$\boxed{\ \rho(A)=A+B+X,\quad \rho(B)=C,\quad \rho(C)=-A-B-C-X-Y,\quad \rho(X)=-(A+B+C),\quad \rho(Y)=A\ }$$

★ **機械確認: $\rho^5=\mathrm{id}$ が $5\times5$ 行列として厳密に成立**(付録 A)。これが $\rho$ の明示形の唯一の非自明な検査である。
$\rho$ は $\mathfrak n$ を保たない($\rho(A)$ が $X$ 成分をもつ)— ファイブレーションが $\rho$-同変でないことの反映であり、**正常**。

$$j:\ x\mapsto T_1=X,\quad y\mapsto T_2=Y\quad\Longrightarrow\quad j(\mathrm{Lie}(x,y))\subseteq\mathfrak h,\ \ j(h)=(0,h).$$
★ **$j$ が $\mathfrak h$ にそのまま落ちる**のが本模型の最大の実務上の利点。

---

## 4. 規模比較(**本設計の存在理由**)

| $k$ | イデアル方式の周囲 $\mathrm{Witt}(5,k)$ | 本方式 $\dim\mathfrak t_k=\mathrm{Witt}(3,k)+\mathrm{Witt}(2,k)$ | 比 |
|---|---|---|---|
| 6(既走) | 2,580 | 125 | 21× |
| 7 | 11,160 | **330** | 34× |
| **8** | 48,750 | **840** | 58× |
| 9 | 217,000 | 2,240 | 97× |
| 10 | 976,248 | 5,979 | 163× |
| 11 | 4,438,920 | 16,290 | 273× |
| **12** ★ | **20,343,700** | **44,555** | ★ **457×** |

$k\le6$ の $\dim\mathfrak t_k=5,4,10,21,54,125$ は **E-DIM5/6 の実測と 6/6 一致**(`search/certs/edim56_20260806.json`)。★ **本模型は既に 6 点で検証済み。**

---

## 5. 実装スペック(**実装係へ渡す粒度**)

### 5.1 データ構造

- $\mathfrak n$ 側: 自由 Lie 環 $\mathrm{Lie}(A,B,C)$ の元。**疎な非可換多項式**(3 文字)で保持。次数 $k$ の反復括弧は単項式 $\le2^{k-1}$ 個($k=12$ で 2048)。
- $\mathfrak h$ 側: $\mathrm{Lie}(X,Y)$ の元。★ **括弧木つきで保持する**($\delta_h$ の再帰計算に必要)。基底は Lyndon 語の標準括弧づけ($\dim=\mathrm{Witt}(2,k)$、$k=12$ で 335)。
- 元 = 対 $(n,h)$。

### 5.2 演算

| 演算 | 実装 |
|---|---|
| 括弧 | §1 の公式。$\delta_{h}$ は $h$ の括弧木に沿って $\delta_{[h_1,h_2]}=[\delta_{h_1},\delta_{h_2}]$ で再帰。$\delta_X,\delta_Y$ は §2 の 3 値で定義し Leibniz で伸ばす |
| $\rho$ | 次数 1 の像(§3)を代入して**括弧木を再評価**。$\mathfrak h$ の基底元は $X,Y$ の反復括弧なので、$\rho^i(X),\rho^i(Y)$(次数 1 の対)を代入して $\mathfrak t$ 内で括弧を取り直す。1 基底元あたり $k-1$ 回の括弧 |
| $\nu_k=\sum_{i=0}^4\rho^i$ | 上を 5 回 |
| ゼロ判定 | $(n,h)$ の両成分がゼロか。$\mathfrak n$ 側は Lyndon 座標(3 文字)、$\mathfrak h$ 側は Lyndon 座標(2 文字) |

**総コスト**($k=12$ の最悪): $H_k$ の基底 $\le\mathrm{Witt}(2,12)=335$ 本 × 5 シフト × 11 括弧 $\approx1.8\times10^4$ 回の括弧演算。**分オーダーの見込み。**

### 5.3 ★ 較正(**通らなければ結果を報告しない**)

| # | 検査 | 期待 |
|---|---|---|
| **C-1** | $\rho^5=\mathrm{id}$ を次数 1 と次数 2,3 で | id |
| **C-2** | $\delta_X(A+B+C)=\delta_Y(A+B+C)=0$ | 0 |
| **C-3** | $\dim\mathfrak t_k$($k=1..6$) | 5,4,10,21,54,125 |
| **C-4** ★★ | **$k=3,4,5,6$ で $\dim H_k,\dim\mathcal S_k$ を再計算し、`edim56_20260806.json` と完全一致** | $H=1,1,2,3$ / $\mathcal S=1,0,1,0$ |
| **C-5** | $\nu_3(j(\mathfrak h_3))=0$、$\nu_4(j(\mathfrak h_4))\ne0$ | D3-BLIND / D4-POWER |

> **C-4 が生命線。** 本模型はイデアル方式と**独立な第二実装**であり、C-4 が通れば E-DIM5/6 の格が `cross-checked candidate(同一実装・二素数)` から **`cross-checked(二実装)`** へ上がる — 便 113 の監査点が 1 つ閉じる。

### 5.4 発注の段取り

1. C-1〜C-3(1 日・紙の検算の機械化)
2. **C-4**(既測との突合 — ここで止めて司令塔検収)
3. $k=7,8$ 本計算 → 予言票 `..._addendum_edim78_prediction.md`(commit `346c264`)と突合
4. $k=9\ldots12$(予言は各段の**走行前**に IF-FIRST 単独コミット)

---

## 6. GAP と限定

- **【EDIM-GAP-1a】** 「$\mathfrak t\cong\mathfrak n\rtimes\mathfrak h$ で $\mathfrak n$ が $A,B,C$ 上**自由**」は candidate。根拠 = $K(0,5)\cong F_3\rtimes F_2$(almost-direct product)+ 次元一致 6 点。**証明ではない** ⟹ C-4 が実質的な検証。
- **【EDIM-GAP-1b】** §2 の微分作用は (R1)(R2) からの導出だが、**球面関係との整合は $A+B+C$ を殺すことしか確認していない**。$\delta$ が $\mathfrak n$ の他の関係を壊さないことは $\mathfrak n$ が自由(1a)に依存。
- 本設計は **$k=7$ のブロック LU 改修を不要にする**(裁定 646 で fallback へ降格済)。
- 判定文は UNKNOWN 規律を継承: 本設計が動いても「$k^*\ge\cdots$」は**自由性仮定の下で**としか書けない(L-4 未着・S-ED-5)。

---

## 付録 A — 機械確認(`scratchpad/semidirect.py`・分数演算・窓非接触)

球面関係 5 本の解、$\rho$ の $5\times5$ 行列(25 未知数の一意解として求解 — **過剰決定系が矛盾なく解けたこと自体が検査**)、$\rho^5=\mathrm{id}$、次元表 $k=1..12$。出力は §3・§4 の表そのもの(手写しなし)。
