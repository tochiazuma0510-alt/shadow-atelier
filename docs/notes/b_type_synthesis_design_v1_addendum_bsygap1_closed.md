# 【BSY-GAP-1】**閉鎖** — 原因は (iii)、Magnus 文字基底と Malcev 基底の取り違え(裁定 647)

**状態札: `measured / candidate / ★ BSY-GAP-1 閉鎖 / 前 addendum 2 件の一部を撤回(§4)/ 窓ゼロ・GAP ゼロ・封印非接触 / 機械 = scratchpad/tau_lambda.py, lambda_dict.py(分数演算)`**

- 実行: 影工房 数学者(Claude / Opus 5)・2026-08-06
- 委嘱: 裁定 647「(iii) の 30 行を即実行 — $\tau$ を『$F$ の Lie 語の $x,y$ に $\log(g_y),\log(g_z)$ を代入して $\exp$』で再実装し非斉次系の solvable を判定」

---

## 0. 結論(2 行)

> $$\boxed{\ \textbf{原因は (iii)。Magnus 文字 }\{X,Y\}\ \textbf{と Malcev 生成元 }\{\lambda_x,\lambda_y\}=\{\log(1{+}X),\log(1{+}Y)\}\ \textbf{の取り違えだった。}\ }$$
> $$\boxed{\ \textbf{正しい基底で ACDIK を解くと }c_2=0,\ a=b=-\kappa^*_3/2,\ \boxed{F_4=(0,0,0)}\ \textbf{— hexagon とも pentagon とも完全整合。}\ }$$

---

## 1. $\tau$ の再実装(委嘱の 30 行)

$\lambda_x:=\log(1{+}X)$, $\lambda_y:=\log(1{+}Y)$, $\lambda_z:=\log(g_z)$($g_z=((1{+}X)(1{+}Y))^{-1}$)。
$F$ を **$\lambda$ の自由 Lie 環の元**として書き、$\tau:\lambda_x\mapsto\lambda_y,\ \lambda_y\mapsto\lambda_z$、$\theta:\lambda_x\leftrightarrow\lambda_y$ を**Lie 代数準同型**として括弧木に沿って代入する($\exp$ は最後に 1 回)。
自己検査: $\exp(\lambda_x)=1{+}X$ ✔、$\lambda_z$ の 1 次項 $=-X-Y$ ✔。

$F_3=a(\mu_1+\mu_2)$($\mu=[\lambda_x,\lambda_y]$, $\mu_i$ は $\mathfrak h_3$ の $\lambda$ 版)、$F_4=0$ での残差:

| | 次数 $\le3$ | 次数 4 |
|---|---|---|
| (3.10) | **ZERO** | ★ **ZERO** |
| (3.11) | **ZERO** | ★ **ZERO** |

> $$\boxed{\ \textbf{深さ 4 の hexagon は「正しい実装では斉次」— 前 addendum の「非斉次」は実装アーティファクトだった。}\ }$$
> 非斉次系の求解も `solvable: True`、特殊解 $(0,0,0)$、(3.11) 単独の階数 1 ⟹ 核 2 次元、(3.10) の $\alpha=\gamma$ を課して **1 次元 = $\mathrm{span}(1,4,1)$** — **D4-POWER (a) と一致**。

---

## 2. ★ 辞書を正しい基底で取り直す(決定的な一歩)

同じ Fox/Magnus ルートで $\mathrm{pr}(h(\exp B))$ を**両基底**で測ると:

| 基底元 | $1$ | $\xi$ | $\eta$ | $\xi^2$ | $\xi\eta$ | $\eta^2$ |
|---|---|---|---|---|---|---|
| **Magnus 文字** $u,u_1,u_2,v_1,v_2,v_3$ | 対角(前 addendum のとおり) | | | | | |
| **Malcev** $\mu$ | 1 | $-1/2$ | $-1/2$ | $1/3$ | $1/4$ | $1/3$ |
| **Malcev** $\mu_1$ | 0 | $-1$ | 0 | ★ $1$ | ★ $1/2$ | 0 |
| **Malcev** $\mu_2$ | 0 | 0 | $-1$ | 0 | ★ $1/2$ | ★ $1$ |
| **Malcev** $\nu_1,\nu_2,\nu_3$ | 0 | 0 | 0 | $\mathrm{diag}(1,1,1)$ | | |

$$\boxed{\ \textbf{二つの基底は同じ辞書を与えない。}\ \mu_1\ \textbf{は }\xi^2\ \textbf{と }\xi\eta\ \textbf{に漏れる — これが深さ 3 が深さ 2 に混ざる正体。}\ }$$

**ACDIK を Malcev 基底で解く**($\kappa^*_3=1$、$\mathrm{pr}(h)=0+\tfrac12(\xi+\eta)-\tfrac12(\xi^2+\xi\eta+\eta^2)$):
$$c_2=0,\qquad a=b=-\tfrac12,\qquad \boxed{(\alpha,\beta,\gamma)=(0,0,0)}\qquad(\textbf{rank 6・consistent}).$$

- hexagon: $F_4=0\in\mathrm{span}(1,4,1)$ ✔
- pentagon: $\dim\mathcal S_4=0$ ⟹ $F_4=0$ **強制** ✔
- $m\equiv0$ 層の自由度 = $a$ の 1 個 ⟹ $p^1=7$ 元 ⟹ $\lvert H_W\rvert=6\times7=42$ ✔(既測と一致)

$$\boxed{\ \textbf{矛盾は完全に解消。【BSY-GAP-1】閉鎖。}\ }$$

---

## 3. 拘束の解除・維持

| 項目 | 変更 |
|---|---|
| 合同式経路 (ii) の深さ $\ge4$ 使用禁止 | ★ **解除可**(candidate 格で)。**ただし必ず Malcev 基底で** |
| 深さ 3 の BR-3 | 無傷(**変更なし**)。深さ 3 では両基底の差が効かない |
| BH-BRIDGE / BH-α / $\lvert H_W\rvert=42$ | **無傷**(むしろ 42 が独立に再現された) |
| E-DIM5/6 の結果 | ★ **無傷**。graded では両基底の主要項が一致 ⟹ $\dim H_k,\dim\mathcal S_k$ は基底非依存 |
| 【BSY-GAP-1′】 | ★ **閉**((iii) が原因と確定) |

---

## 4. ★ 撤回(**versioned 規律**・前 2 件の addendum は改変しない)

| 出所 | 撤回する記述 | 正しい記述 |
|---|---|---|
| `..._bsygap1_decisive.md` §1 | 「辞書は 6/6 一致 ⟹ 原因②は棄却」 | **辞書そのものは正しいが、適用していた基底が誤りだった。** Magnus 文字基底では 6/6 一致、**Malcev 基底では対角でない**。⟹「②棄却」は**基底を固定した上での話**として限定される |
| 同 §2・§5 | 「深さ 4 の hexagon は真に非斉次(原因④)」 | ★ **撤回。** 非斉次性は Magnus 文字への代入という誤実装の産物。**正しい実装では斉次**であり、原因④は存在しない |
| `..._bsygap1_variants.md` §2 | (i)(ii) は識別力ゼロ | **維持**(独立に正しい・ただし今や moot) |

---

## 5. ★ 教材(規約台帳 pending 7 件目として上申)

> **「Magnus 文字基底 $\{X,Y\}$ と Malcev 生成元基底 $\{\lambda_x,\lambda_y\}=\{\log(1{+}X),\log(1{+}Y)\}$ を混同しない。」**
> - 両者は **graded では一致**($\lambda_x\equiv X$ mod 次数 2)が、**非斉次(Malcev)計算では別物**。
> - 群の元は $\exp(\text{Malcev Lie 元})$ であり、$f(y,z)$ 型の代入は **Malcev 生成元への代入**である。**Magnus 文字への代入ではない。**
> - 症状: 「本来斉次な条件が非斉次に見える」「辞書が対角に見える基底で計算してしまう」。
> - **CV-13(向き規約)・D-6(語の向き)・pr 経由の座標読み出し(pending 6 件目 = graded/ungraded)に続く同型事故の 7 件目。** 前件との差: 今回は**どちらの基底も正しい**が、**混ぜると壊れる**型である。

---

## 6. 判定文(UNKNOWN 規律)

> 書いてよい: 「$\chi\equiv1$ 層の算術元は Malcev 基底で $c_2=0$, $F_3=a\mathfrak h_3$, $F_4=0$($a=-\kappa^*_3/2$)を満たす — hexagon・pentagon・$\lvert H_W\rvert=42$ の 3 者と整合(candidate)」
> 書いてはならない: 「深さ 4 の算術条件が確立した」— **単系統(本数学者のみ)・Sol 未監査**。便 113 の監査対象。/ 「合同式経路が使える」— 深さ 5 以上は未検証。
