# 整錐 ④ 追補 E — T2-HECKE の採点と「小孔 $C_k$ の住む環」の同定(裁定 776①)

**状態札: `採点 + 正札案 / candidate / Sol 未監査 / GAP 実走ゼロ・cert 発行ゼロ / 判定語の発効は司令塔専権 / 本体および追補 A–D は不改変(versioned)`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-11 / 委嘱: 司令塔(**裁定 776①**)
- 生値: `t2_hecke` 系 cert(d4394df)— 較正 $\tau(2)=-24$ **PASS**(coboundary 混入の構造発見込み)/ **$144169\mid\mathrm{disc}$・$\mathrm{disc}=576\cdot144169$ 厳密** / 指数列 $(24{:}24,\ 28{:}216,\ 30{:}192,\ 32{:}24)$
- **自前検算**: §2 の指数会計は python(整数のみ・GAP 不使用・cert ではない)。

---

## 0. 採点表(先に)

| 予言 | 凍結文言(追補 D §3.2) | 生値 | 採点 |
|---|---|---|---|
| **H-b カナリア** | $k=12$ で $T_2=\tau(2)=-24$ | $-24$ | ★ **PASS** |
| **P-T2-1** | $144169\mid\mathrm{disc}$($k=24$) | $\mathrm{disc}=576\cdot144169$ | ★ **的中**(しかも**厳密一致** — 予言の副条件「$\mathrm{disc}=576\cdot144169$ なら $a_2=540\pm12\sqrt{144169}$ を機械が確認」まで成立) |
| **P-T2-2** | $k=28,30,32$ の disc は平方因子を除いて Hecke 体の判別式 | 指数列 $216,192,24$ | ★ **形は成立**(指数が測れている = 平方因子が分離できている)。個々の $d_K$ の値は**未 pin** |
| **H-f** | $T_2T_3=T_3T_2$ | (cert に依る) | — |

> ### ★ 較正の副産物 = **coboundary 混入の構造発見**(受理)
> 周期多項式の空間は本質的に $H^1_{\rm cusp}(SL_2(\mathbf Z),V_{k-2})$ であり、**多項式表現は余輪体(coboundary)を法としてのみ well-defined**。Heilbronn–Merel 行列で素朴に作った $T_n$ の像は余輪体を含みうる ⟹ **商を取ってから固有値を読む**必要がある。
> $$\boxed{\ \textbf{これは実装の瑕疵ではなく、対象($H^1$)の性質である。較正 }\tau(2)=-24\ \textbf{がその一段を捕まえた。}\ }$$
> ⟹ **発注仕様 T2-HECKE 段 H-a の「整性」カナリアに、余輪体商の一行を追加**すべき(差分は §4)。

---

# 1. P-T2-1 の厳密一致の意味

$\mathrm{disc}(\mathbf Z[T_2])=576\cdot144169=83{,}041{,}344$。
- $144169$ は**素数**(自前確認・追補 D §3.1)、かつ $144169\equiv1\pmod 4$($144168=4\cdot36042$)
 ⟹ **$\mathbf Q(\sqrt{144169})$ の判別式は $d_K=144169$**(平方因子なし)。
- $\mathrm{disc}(\mathbf Z[T_2])=[\mathcal O_K:\mathbf Z[T_2]]^2\cdot d_K$ ⟹ $[\mathcal O_K:\mathbf Z[T_2]]^2=576$ ⟹ **指数 $=24$** ✓ — cert の指数列の $k=24$ 行と**独立に一致** ✔
- ⟹ $a_2=\dfrac{1080\pm\sqrt{576\cdot144169}}2=540\pm12\sqrt{144169}$ ✓ — 追補 D §3.1 で「**要 pin**」としていた値が **機械で確定**。
$$\boxed{\ \textbf{【D-GAP-1】(重み 24 の }a_2\ \textbf{と Hecke 体)は閉。pin は文献でなく自前測定が与えた。}\ }$$

---

# 2. ★★★ 指数列 $(24,216,192,24)$ の構造的意味

## 2.1 素因数分解(自前)

| $k$ | $\dim\mathsf P_k$ | 指数 $[\mathcal O_K:\mathbf Z[T_2]]$ | 分解 |
|---:|---:|---:|---|
| 24 | 2 | **24** | $2^3\cdot3$ |
| 28 | 2 | **216** | $2^3\cdot3^3$ |
| 30 | 2 | **192** | $2^6\cdot3$ |
| 32 | 2 | **24** | $2^3\cdot3$ |

> ### ★★ 観察 IDX-1(candidate・本追補)
> $$\boxed{\ \textbf{4 重み全てで指数は }3\textbf{-smooth(素因数は }2\ \textbf{と }3\ \textbf{のみ)}\ }$$

## 2.2 ★★★ ④ にとっての帰結(**これが本採点の眼目**)

指数が $3$-smooth ⟹ 任意の素数 $p\ge5$ について $p\nmid[\mathcal O_K:\mathbf Z[T_2]]$ ⟹

> ### 命題 IDX-2(candidate・本追補)
> $k\in\{24,28,30,32\}$ と任意の素数 $p\ge5$ について
> $$\boxed{\ \mathbf Z[T_2]\otimes\mathbf Z_p\ =\ \mathcal O_K\otimes\mathbf Z_p\ =\ \textbf{極大整環}\ }$$
> したがって $\mathbf Z[T_2]\subseteq\mathbf T\subseteq\mathcal O_K$ より **$\mathbf T\otimes\mathbf Z_p=\mathcal O_K\otimes\mathbf Z_p$** も極大。
> ⟹ $\mathrm{End}_{\rm Hecke}(\mathsf P_k^{\mathbf Z})\otimes\mathbf Z_p$ は**極大整環**であり、
> $$\mathcal O_K\otimes\mathbf Z_p\cong\begin{cases}\mathbf Z_p\times\mathbf Z_p & p\ \text{分裂}\\ \mathbf Z_{p^2}\ (\text{不分岐 2 次}) & p\ \text{惰性}\\ \text{分岐 DVR} & p\mid d_K\end{cases}$$

> ### ★ P-CONE-6′ への直接の帰結
> $C_k\in\mathrm{End}_{\rm Hecke}(\mathsf P_k^{\mathbf Z})$(命題 CONE-A′)。命題 IDX-2 より $p\ge5$ で **$C_k$ は極大整環の元**として振る舞う ⟹ $\bmod\,p$ での階数落ちは **$p$ の分解型で決まる**:
> $$\boxed{\ \mathrm{rank}_{\mathbf F_p}\rho_k\ =\ 2-\sum_{\mathfrak p\mid p,\ \mathfrak p\mid C_k}f(\mathfrak p/p)\ }$$
> - **$p$ 分裂 + 合同が片方の素点** ⟹ **$\mathrm{rank}=1$**(固有形式枝)
> - **$p$ 惰性**($f=2$)⟹ $\mathrm{rank}=0$(スカラー枝に見える)
> ★ **$(103,24)$**: $\left(\frac{144169}{103}\right)=+1$(自前計算)⟹ **分裂**、かつ $103\nmid24$(指数)⟹ 極大 ⟹ **P-CONE-6′ の「$\mathrm{rank}=1$」枝が構造的に支持された**。
> ★ **$(37,32)$**: $37\nmid24$(指数)⟹ 極大 ⟹ 同じ論法が使える。**残るのは $37$ の分解型のみ**(= 重み 32 の $d_K$ が要る ⟹ §4 の追加測定 1 行)。
> $$\Longrightarrow\ \boxed{\ \textbf{【CC-GAP-3】(こだまの形が未決)は「}d_K\ \textbf{を測り }\left(\tfrac{d_K}p\right)\ \textbf{を見る」1 行に縮んだ。}\ }$$

## 2.3 $3$-smooth の理由(**UNKNOWN・予言化**)

$4/4$ で $3$-smooth になる構造的理由は本追補では**同定できていない**。
> ### 予言 **P-T2-3**(新規凍結)
> $$\boxed{\ \dim\mathsf P_k=2\ \textbf{の重み }k\ge34\ \textbf{でも }[\mathcal O_K:\mathbf Z[T_2]]\ \textbf{は }3\textbf{-smooth}\ }$$
> **外れたら**: $p\ge5$ が指数に現れる ⟹ その $p$ で $\mathbf Z[T_2]$ が非極大 ⟹ **命題 IDX-2 がその重みで使えなくなる**(こだまの形の判定に $T_3$ 以上が要る)⟹ 実務的にも重要。
> ⚠ **$\dim\mathsf P_k\ge3$($k\ge36$)では判別式の意味が変わる**(3 次以上の体)⟹ 予言の射程は $\dim\mathsf P_k=2$ に限る。

---

# 3. 正札案 — 「小孔 $C_k$ の住む環の同定完了」

> ## 正札 **CONE-HECKE**(発効は司令塔専権・以下は案)
> ### 主張
> $$\boxed{\ k\in\{24,28,30,32\}\ \textbf{について、}\mathrm{End}_{\rm Hecke}\bigl(\mathsf P_k^{\mathbf Z}\bigr)\ \textbf{は全ての素数 }p\ge5\ \textbf{で極大整環である。}\ }$$
> 根拠:$T_2$ を周期多項式格子に実装し($\tau(2)=-24$ で較正)、指数 $[\mathcal O_K:\mathbf Z[T_2]]\in\{24,216,192,24\}$ が **$3$-smooth** であることを測定。
> ### 意味
> ④ の深さ 4 層の「小孔」$C_k$(命題 CONE-A′)は、**$p\ge5$ では極大整環の元として振る舞う** ⟹ こだまの形(スカラー枝/固有形式枝)は **$p$ の分解型だけで決まる**。
> ### ★ 限定(**4 点・必ず併記**)
> | # | 限定 |
> |---|---|
> | **(H1)** | **$\mathbf Z[T_2]$ のみの測定**。$\mathbf T=\mathbf Z[T_2,T_3,\dots]$ は $\mathbf Z[T_2]$ と $\mathcal O_K$ の間にあり、$p\ge5$ での極大性は**挟み撃ちで従う**が、$p=2,3$ では未決 |
> | **(H2)** | $\dim\mathsf P_k=2$ の 4 重みのみ。$\dim\mathsf P_k\ge3$ は射程外 |
> | **(H3)** | **$C_k$ が住む環の同定であって $C_k$ そのものの同定ではない**($\det C_k$・こだまの形は $\rho$ 側 = $\tilde\sigma$ 律速・追補 C (E1) と同じ) |
> | **(H4)** | 格子言明(定義 LAT-ls・$\mathsf P_k^{\mathbf Z}$ の取り方に依存)・単系統・Sol 未監査 |
> ### 言ってよい / いけない
> | ✔ | ✗ |
> |---|---|
> | 「$C_k$ の住む環を $p\ge5$ で極大整環と同定した」 | 「$C_k$ を決定した」(**H3**) |
> | 「重み 24 の Hecke 体を $\mathbf Q(\sqrt{144169})$ と機械で確定した」 | 「合同素数を発見した」(144169 は既知値・我々は**再現**した) |
> | 「P-CONE-6′ の判定が $p$ の分解型 1 点に縮んだ」 | 「P-CONE-6′ が解決した」($d_K$ の測定が残る) |

---

# 4. 差分・追加発注(**本追補は本体を改変しない**)

| 対象 | 差分 |
|---|---|
| 追補 D §3.2 段 H-a | **余輪体商の一行を追加**:「$T_n$ の像から coboundary を除いてから固有値・判別式を読む」(§0 の構造発見) |
| 追補 D §5【D-GAP-1】 | ★ **閉**($a_2=540\pm12\sqrt{144169}$ が機械で確定・§1) |
| 追補 C【CC-GAP-3】 | ★ **縮小**:「こだまの形が未決」→「**$d_K$ を測り $\left(\frac{d_K}p\right)$ を見る 1 行**」(§2.2) |

> ### 追加発注 **T2-SPLIT**(1 行・分オーダー)
> | 段 | 内容 | 出力 | 予言 |
> |---|---|---|---|
> | **H-h** | 各 2 次元重みで $d_K$(判別式の平方因子を除いた部分)と、こだま素数の **Legendre 記号** $\left(\frac{d_K}{p}\right)$ | `d_K[k]`, `legendre[k][p]` | $k=24,p=103$: $+1$(分裂・自前計算と一致すべき)/ $k=32,p=37$: **未知 = 本測定の標的** |
> ★ $\left(\frac{d_{32}}{37}\right)=+1$ なら **$(37,32)$ も固有形式枝**(RA-1 の「方向」が実在する側)。$-1$ なら惰性 ⟹ **rank 0 = スカラー枝に見える** ⟹ RA-1 の魅力が 1 段下がる。**どちらでも情報が出る。**

---

# 5. 【GAP】・novelty・帰属

| # | 内容 | 重さ |
|---|---|---|
| **【E-GAP-1】** | 観察 IDX-1($3$-smooth)の**構造的理由は未同定** ⟹ P-T2-3 で検定 | 中 |
| **【E-GAP-2】** | 命題 IDX-2 は $p\ge5$ 限定。$p=2,3$ では $\mathbf Z[T_2]$ が非極大 ⟹ **④ の $p=2,3$ 挙動は依然 UNKNOWN**(追補 C の帳簿分離と同根) | 中 |
| **【E-GAP-3】** | $d_K$($k=28,30,32$)が未 pin ⟹ T2-SPLIT で測る | 中(縮小済) |
| **【E-GAP-4】** | 本追補の全命題は candidate(単系統・Sol 未監査)・判定語の発効は司令塔専権 | — |

**novelty grep**(`docs/` `provenance/` `sol/`): `IDX-1` / `IDX-2` / `P-T2-3` / `CONE-HECKE` / `T2-SPLIT` = **0 hit**(本追補初出)。「極大整環」「coboundary 商」= 0 hit。

**帰属**: 発案($T_2$ 計器)= 発案係 v4 PS-5。委嘱 = 司令塔(裁定 776①)。実装・生値・**余輪体混入の構造発見** = 実装係(★ 較正が対象の性質を捕まえた良い例)。本追補の新規部分 = §1 の指数の独立再導出と【D-GAP-1】の閉鎖 / **観察 IDX-1** / **命題 IDX-2(極大性 ⟹ こだまの形は分解型で決まる)** / **P-T2-3** / **正札 CONE-HECKE と限定 4 点** / **追加発注 T2-SPLIT**(【CC-GAP-3】を 1 行に縮める)。
