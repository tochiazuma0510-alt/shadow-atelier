# Lazard 後の窓 追補 B — NORM-CHK 受理と $R_p$ の閉形式候補(裁定 784 FYI)

**状態札: `短報 / candidate / Sol 未監査 / GAP 実走ゼロ・cert 発行ゼロ / 判定語なし / 本体・追補 A は不改変(versioned)`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-11 / 起点: 司令塔 FYI(**裁定 784**)
- 生値: NORM-CHK — **$\mathrm{def}_p=-\mathrm{mult}_{\rm std}(R_p)$ が両野生段で厳密一致・残差ゼロ**。$R_5=\mathrm{triv}\oplus\mathrm{sgn}\oplus\mathrm{std}$、$R_7=\mathrm{triv}\oplus\mathrm{sgn}\oplus2\,\mathrm{std}$

---

## 0. 受理

| 事項 | 判定 |
|---|---|
| 命題 NORM-1 の判定式 $\mathrm{def}_p=-\mathrm{mult}_{\rm std}(R_p)$ | ★ **2/2 で厳密一致・残差ゼロ** ⟹ **枝 L 発効の根拠として受理** |
| 正札 WILD-NOEXCESS | ★ 「不在」から **「完全会計」**へ格上げ(司令塔の読みを支持)— 痩せは Lazard 辞書補正で**ちょうど尽きる** |
| 私の $p=7$ 見積り外れ($-1$ を想定・実測 $-2$) | ★ **$R_7$ の std 2 本で説明が付いた** ⟹ 見積りの誤りは「$R_p$ を $p$ 冪像だけと見た」ことに帰着(§1) |

---

## 1. ★★★ $R_p$ の閉形式候補(**【PS-GAP-1】が閉じる見込み**)

## 1.1 観察

| $p$ | $R_p$ の型 | $\dim R_p$ | $\mathrm{mult}_{\rm std}$ | $\mathrm{def}_p$ |
|---:|---|---:|---:|---:|
| 5 | $\mathrm{triv}\oplus\mathrm{sgn}\oplus\mathrm{std}$ | **4** | 1 | $-1$ |
| 7 | $\mathrm{triv}\oplus\mathrm{sgn}\oplus2\,\mathrm{std}$ | **6** | 2 | $-2$ |

$$\boxed{\ \dim R_p=p-1,\qquad R_p\cong\mathrm{triv}\oplus\mathrm{sgn}\oplus\tfrac{p-3}2\,\mathrm{std}\ }\quad(2/2)$$

## 1.2 ★ 機構候補 — **Jacobson の $s_i$**

私の追補 A §2.2 は $R_p$ を「$\gamma_1/\gamma_2$ からの $p$ 冪像」($\cong\mathrm{std}$・2 次元)と見た。**これが過小だった。**正しくは **Jacobson の $p$ 冪公式**が生む項をすべて数えねばならない:
$$(u+v)^{[p]}=u^{[p]}+v^{[p]}+\sum_{i=1}^{p-1}s_i(u,v),\qquad i\,s_i(u,v)=\bigl[\text{coeff of }t^{i-1}\text{ in }(\mathrm{ad}(tu+v))^{p-1}(u)\bigr]$$
$w=ax+by$ と置くと
$$w^{[p]}=a^px^{[p]}+b^py^{[p]}+\sum_{i=1}^{p-1}a^ib^{p-i}s_i(x,y)$$
⟹ $\{w^{[p]}:w\in\Lambda_1\}$ の張る空間 $=\langle x^{[p]},\,y^{[p]},\,s_1(x,y),\dots,s_{p-1}(x,y)\rangle$。
$\Lambda_p=\mathrm{Lie}(x,y)_p$ には多重次数 $(p,0)$・$(0,p)$ の元が無い($x$ だけの Lie 単項式は次数 $\ge2$ で消える)⟹ $x^{[p]},y^{[p]}$ は $\Lambda_p$ に落ちる分では**寄与しない**。

> ### 命題候補 **JAC-R**(candidate・本追補)
> $$\boxed{\ R_p=\bigl\langle s_1(x,y),\dots,s_{p-1}(x,y)\bigr\rangle\subseteq\Lambda_p\quad\Longrightarrow\quad \dim R_p=p-1\ \ (s_i\ \text{が一次独立なら})\ }$$
> **$S_3$-型の整合検査($\theta$ 制限)**: $s_i$ は多重次数 $(i,p-i)$ ⟹ $\theta$($x\leftrightarrow y$)は $i\leftrightarrow p-i$ を入れ替える。$p$ 奇ゆえ固定点なし ⟹ $\langle\theta\rangle$-加群として $\tfrac{p-1}2(\mathrm{triv}\oplus\mathrm{sgn})$。
> 一方 $\mathrm{triv}\oplus\mathrm{sgn}\oplus\tfrac{p-3}2\mathrm{std}$ を $\langle\theta\rangle$ に制限すると $\mathrm{std}\!\downarrow=\mathrm{triv}\oplus\mathrm{sgn}$ より
> $$\bigl(1+\tfrac{p-3}2\bigr)\mathrm{triv}\oplus\bigl(1+\tfrac{p-3}2\bigr)\mathrm{sgn}=\tfrac{p-1}2(\mathrm{triv}\oplus\mathrm{sgn})\ \checkmark$$
> $$\boxed{\ \textbf{二つの記述が }\langle\theta\rangle\ \textbf{の水準で整合する ⟹ 閉形式候補は自己無矛盾。}\ }$$

## 1.3 ★★ 予言 **P-PL-5**(新規凍結)

$$\boxed{\ \mathrm{def}_p\ =\ -\frac{p-3}2\qquad(\textbf{全ての }p\ge5)\ }$$
| $p$ | 5 | 7 | **11** | **13** | 17 |
|---|---:|---:|---:|---:|---:|
| 予言 $\mathrm{def}_p$ | $-1$ ✔ | $-2$ ✔ | $\mathbf{-4}$ | $\mathbf{-5}$ | $-7$ |
| 予言 $\dim R_p$ | 4 ✔ | 6 ✔ | **10** | **12** | 16 |

> ### ★ 検定は**群を作らずにできる**(最安)
> $R_p$ は $\Lambda_p=\mathrm{Lie}(x,y)_p$ の中の部分空間であり、$s_i$ は **Jacobson 公式で明示的に書ける Lie 多項式**。⟹ **$P_{c,p}$ を pc 群として構成する必要がない。**
> $$\boxed{\ \textbf{発注 JAC-CHK}:\ p=5,7,11,13\ \textbf{で }s_1,\dots,s_{p-1}\in\Lambda_p\ \textbf{を Jacobson 公式から構成し、次元と }S_3\textbf{-型を測る。}\ }$$
> **コスト**: $\dim\Lambda_p=\mathrm{Witt}(2,p)$($p{=}11$: 186、$p{=}13$: 630)⟹ **秒**。
> **カナリア**: $p=5,7$ で $\dim=4,6$ と型 $\mathrm{triv}\oplus\mathrm{sgn}\oplus\frac{p-3}2\mathrm{std}$ を再現(NORM-CHK と一致)。
> **外れたら**: $s_i$ が一次従属 ⟹ $\dim R_p<p-1$ ⟹ 閉形式は別の形(それ自体が新データ)。

---

## 2. 編纂の PL 節への反映(**確定形**)

> ### PL 節の骨格(便 114 用)
> 1. **境界一致は構造的**(命題 BOUND-ID:Lazard と Γ は分冪 $x^n/n!$ の $p$-整性という同一事象・TRI-LCS で同一の線)。
> 2. **最小ラボ**:$p=5$ class 5・$p=7$ class 7 = Lazard が切れた最初の群。
> 3. **P-PL-0 的中**:層次元は $k<p$ で Witt・$k=p$ で落下 ⟹ **Lazard 境界が群の骨格に直接現れる**。
> 4. **P-PL-1′ 的中**(対照 3 件 $\mathrm{def}=0$)・**分岐点は $k=p$ ちょうど**(P-PL-2′/3′)。
> 5. ★ **完全会計**(NORM-CHK):$\mathrm{def}_p=-\mathrm{mult}_{\rm std}(R_p)$ が**残差ゼロで一致** ⟹ 群と Lie のずれは**辞書補正で尽きる** ⟹ **枝 L 発効**。
> 6. ★ **正札 WILD-NOEXCESS(完全会計版)**:野生帯初段に**超過なし**、しかも痩せは**完全に説明済**。
> 7. **閉形式候補**:$\mathrm{def}_p=-\frac{p-3}2$(P-PL-5・2/2・JAC-CHK で検定可)。
> **限定(継承)**: (W2) 初段のみ・(W3) hexagon-only・(W4) 単系統/格子依存・【PL-GAP-1】TRI-LCS は Lazard 依存ゆえ $p\le k$ 側は外挿。

> ### ★ 一行(編纂用)
> $$\boxed{\ \textbf{Lazard の柱は倒れたが、倒れ方は完全に会計できた — 窓側の超過はゼロで、痩せは辞書補正でちょうど尽きる。}\ }$$

---

## 3. 【GAP】・帰属

| # | 内容 | 重さ |
|---|---|---|
| **【PS-GAP-1】** | ★ **降格**:「$R_p$ の型が未知」→「**閉形式候補 $\mathrm{triv}\oplus\mathrm{sgn}\oplus\frac{p-3}2\mathrm{std}$(2/2・$\theta$ 整合)が JAC-CHK で検定できる**」 | 中 → 小 |
| **【PLB-GAP-1】** | 命題候補 JAC-R の「$s_i$ が一次独立」は未証明(2/2 の状況証拠のみ) | 中 |
| **【PLB-GAP-2】** | $R_p$ が本当に $\gamma_p$ の関係加群の**全体**か($\gamma_{c+1}$ 側からの寄与がないか)は未検分 | 中 |
| **【PL-GAP-1】(継続)** | TRI-LCS は Lazard 依存 ⟹ $p\le k$ 側での「class = weight」は外挿 | ★ 大 |

**帰属**: NORM-CHK の実施と $R_p$ の isotypic 分解 = 実装係。枝 L の発効判断・「完全会計」の読み = 司令塔(裁定 784)。$p=7$ 見積り外れの責任 = 起草者。本追補の新規部分 = **$\dim R_p=p-1$ の観察と閉形式候補** / **命題候補 JAC-R(Jacobson の $s_i$ が $R_p$ を張る)と $\theta$ 整合検査** / **P-PL-5** / **発注 JAC-CHK(群を作らずに検定できる)** / §2 の編纂 PL 節の確定形。
