# 【BSY-GAP-1】更新 — 偶数 Bernoulli 部を入れても**解消しない**(L-5 pin 受領後)

**状態札: `candidate / 未解消(原因候補が 2 件に縮小)/ 窓ゼロ・GAP ゼロ・封印非接触 / 機械は付録の分数演算 1 本`**

- 実行: 影工房 数学者(Claude / Opus 5)・2026-08-06
- 入力: **`docs/scout/icm_depth4_verbatim_v1.md`(f8b0de5・400dpi 頁画像 pin・L-5 完了)** / `docs/notes/b_type_synthesis_design_v1.md` §2.4 / **`docs/notes/b_type_synthesis_design_v1_addendum_edim56_result.md`(本日の実測)**
- 委嘱: 司令塔(L-5 配達時の指示)—「偶数 $m$ の Bernoulli 因子込みで深さ 4 を再導出し、$(1,4,1)$ との整合を判定せよ」

---

## 0. 結論(3 行)

> 1. ★ **原因候補①(BH ノートの ACDIK 転記が不完全)は棄却** — pin が「食い違い 0 件」を確定させた(転記は逐語一致)。
> 2. ★ **委嘱の本命(偶数 Bernoulli 因子の欠落)も棄却** — 偶数因子**および** (6.4.2) の補正因子を全部入れて再計算したが、**$\chi\equiv1\ (\mathrm{mod}\ 7)$ では両者とも $\bmod\ 7$ で消え、$(1,1,1)$ 方向は変わらない**(付録・4 通りの $\chi$ で機械確認)。
> 3. ★ **矛盾はむしろ鋭くなった** — 本日の E-DIM 実測 $\dim\mathcal S_4=0$ により、pentagon は $m\equiv0$ 層で $F_4=0$ を**強制**する。すなわち再導出が出すべき正解は「$F_4\in\mathbb Q(1,4,1)$」ですらなく $\boxed{F_4=0}$ である。
>
> $$\boxed{\ \textbf{【BSY-GAP-1】は解消せず、更新。原因候補は 2 件に縮小した(§3)。}\ }$$

---

## 1. 何を計算したか(pin の完全式を使う)

pin §1.4 / §2 の逐語式(**BH ノートの転記と一致**):
$$\psi^{\rm ab}_\sigma=\exp\Bigl\{\sum_{m\ge3,\rm odd}\frac{\kappa^*_m}{m!}P_m\Bigr\}\times\exp\Bigl\{-\frac12\sum_{m\ge2,\rm even}\frac{b_m(1-\chi(\sigma)^m)}{m!}P_m\Bigr\},\quad P_m=(X+Y)^m-X^m-Y^m,$$
$X=\log(1+\xi)$, $Y=\log(1+\eta)$, $\log\bigl((1-e^{-t})/t\bigr)=\sum b_mt^m/m!$、注記 "$mb_m$ is the $m$-th Bernoulli number"。

**前回(§2.4)との差分 3 点**をすべて入れた:
- **(a) 偶数因子の $m=2$ 項**($P_2=2XY$ は次数 2 から始まり、$\log$ 補正で次数 3・4 に寄与)。
- **(b) 偶数因子の $m=4$ 項**($P_4$ は次数 4 から始まる)。
- **(c) (6.4.2) の補正因子** $\bigl(\tfrac{\underline x^{\chi}-1}{\underline x-1}\bigr)\bigl(\tfrac{\underline y^{\chi}-1}{\underline y-1}\bigr)$ — 前回は $\chi^{(p)}(\sigma)=1$ を仮定して $1$ と置いていたが、**窓が見るのは $\chi\equiv1\ (\mathrm{mod}\ p^e)$ という弱い条件**なので一般の $\chi$ で入れ直した。$\mathrm{pr}$ 後は $G(\xi)G(\eta)$、$G(t)=\sum_{k\ge1}\binom{\chi}{k}t^{k-1}$。

そして $\mathrm{pr}(B'_\sigma)=1+\xi\eta\cdot\mathrm{pr}(h)$(BH (4.2))から $[\mathrm{pr}\,h]_2=(\alpha,\beta,\gamma)$ を読む。

### 1.1 機械確認された $b_m$(pin の定義から自前計算)

$b_1,\dots,b_6=-\tfrac12,\ \tfrac1{12},\ 0,\ -\tfrac1{120},\ 0,\ \tfrac1{252}$、検算 $m\,b_m=-\tfrac12,\tfrac16,0,-\tfrac1{30},0,\tfrac1{42}$ = **Bernoulli 数 $B_m$**(pin の注記どおり)。★ **pin の注記が計算の自己検査になった。**

---

## 2. 結果

| ケース | $\chi$ | $(\alpha,\beta,\gamma)$($\kappa^*_3=1$) | $\bmod 7$ |
|---|---|---|---|
| **A**(前回・$\chi=1$ 厳密) | 1 | $(-\tfrac12,-\tfrac12,-\tfrac12)$ | $(3,3,3)$ |
| **B**(偶数部+補正込み) | 8 | $(2796,\ \tfrac{9575}2,\ 2796)$ | ★ $(3,3,3)$ |
| **B** | 15 | $(193140,\ \tfrac{590295}2,\ 193140)$ | ★ $(3,3,3)$ |
| **B** | 22 | $(\tfrac{4494545}2,\ \tfrac{106572807}{32},\ \tfrac{4494545}2)$ | ★ $(3,3,3)$ |
| **対照**($\chi\not\equiv1$) | 3 | $(0,6,0)$ | $(0,6,0)$ |

$$\Longrightarrow\ \chi\equiv1\ (\mathrm{mod}\ 7)\ \text{では}\ (\alpha,\beta,\gamma)\equiv3\cdot(1,1,1)\ (\mathrm{mod}\ 7)\ \textbf{— 前回と同一方向}.$$

**なぜ消えるか(紙の理由・計算と一致)**: $\chi\equiv1\ (\mathrm{mod}\ 7)$ なら (i) $1-\chi^m\equiv0$、(ii) $\binom{\chi}{k}\equiv0\ (k\ge2)$、(iii) $b_2,b_4$ の分母 $12,120$ と $\kappa^*_3$ の $48$ は 7 と互いに素 ⟹ **偶数因子も補正因子も $\bmod\ 7$ で自明化する。**
★ **対照 $\chi=3$ が $(0,6,0)$ という別の値を出していることが、計算が「常に $(1,1,1)$ を吐く壊れた実装」でないことの識別カナリアである。**

---

## 3. 更新後の原因候補(**2 件に縮小**)

| # | 候補 | 状態 |
|---|---|---|
| ~~①~~ | ~~BH ノートの ACDIK 転記が次数 4 で不完全~~ | ★ **棄却**(pin: 食い違い 0 件) |
| ~~①′~~ | ~~偶数 Bernoulli 因子・(6.4.2) 補正の欠落~~ | ★ **棄却**(本ノート §2) |
| **②** | $\mathrm{pr}(B_\sigma)=\psi^{\rm ab}_\sigma$ から $\mathrm{gr}_4$ 座標を読む**辞書**が誤り。とくに「$h(v_1)=(1-\underline x)^2$, $h(v_2)=(1-\underline y)(1-\underline x)$, $h(v_3)=(1-\underline y)^2$ で $\mathrm{gr}_4\to[\mathrm{pr}\,h]_2$ が同型」の部分(**罠 D-6 族**) | ★ **最有力**。深さ 3 では対称性しか検査していないので、**この辞書は深さ 4 で初めて検査される** |
| **③** | 「窓の $m\equiv0$ 層 $\leftrightarrow$ $\chi(\sigma)\equiv1\ (\mathrm{mod}\ 7)$ の $\sigma$」の対応、あるいは $f_\sigma$ と工房の $\bar f$ の同一視(補題 BR-1)に深さ 4 で効くずれ | 未検査 |

**②/③ を分ける決定実験(提案・未実行)**: $\mathrm{pr}$ の辞書を使わず、$\theta_{\exp(F)}$ を**群の交換子から直接**計算する第二実装を書き、$v_1,v_2,v_3$ の $h$ 値を独立に出す(自由群 $F_2$ の低次商での有限計算・窓非接触)。②なら値が変わり、③なら変わらない。

---

## 4. ★ 更新された「正解の形」(**E-DIM 実測が与えた新情報**)

本日の実測 `search/certs/edim56_20260806.json`: $\dim\mathcal S_4=0$。$m\equiv0$ 層では hexagon も pentagon も斉次($c_2=0$・BCH 補正は次数 $\ge6$)なので:

> $$\boxed{\ m\equiv0\ \text{層の }\mathrm{GT}^{\rm pent}\ \text{の元は }F_3=a\,\mathfrak h_3\ (a\in\mathbb F_7\ \text{自由}),\ F_4=0.\ }$$
> ($\dim H_4=1$ で hexagon は $\mathbb Q\mathfrak h_4$ を許すが、$\dim\mathcal S_4=0$ ゆえ pentagon が $\mathfrak h_4$ 方向を潰す。)

⟹ 算術元も($\mathrm{GT}^{\rm arith}\subseteq\mathrm{GT}^{\rm pent}$・HSP-SOUND)**$F_4=0$ でなければならない**。
⟹ **再導出の目標は「$F_4=0$ が出ること」**であり、$(1,4,1)$ 方向との比例ですらない。**これは前回より 1 段強い制約であり、②/③ の検査基準が鋭くなった。**

> ### ★ 教材(記録に値する)
> 【BSY-GAP-1】は「文献の転記が疑わしい」から始まったが、**pin は転記を無罪にし、委嘱の本命(偶数部)も無罪になった**。残ったのは**自前の辞書**である。
> **外部を疑う前に、自分の規約変換を疑え** — CV-13(向き規約)・D-6(語の向き)・f/f⁻¹ 族に続く同型事故の系譜に、**「pr 経由の座標読み出し」を新しい項目として加える**ことを上申する(規約台帳 pending・ep-keeper 経由)。

---

## 5. 拘束(**この GAP が開いている間**)

- **合同式経路 (ii) は深さ $\ge4$ で使用禁止**(継続)。
- **深さ 3 の BR-3 は無傷**(pin で転記一致・対称性からの $a=b$ は D3-BLIND と独立に整合)。**BH-BRIDGE / BH-α の結論には本 GAP は波及しない**(あちらは深さ 3 までしか使っていない)。
- 勘定経路 (i) は無傷(係数を使わない)。**本日の E-DIM 結果は本 GAP に依存しない。**
- pin の $\kappa^*_m\in\hat{\mathbb Z}^\times$(上付き ×)の解釈は **UNKNOWN のまま**(pin §6 の注意を継承)。**本ノートは $\kappa^*_3$ を単なるスカラーとして扱っており、$\hat{\mathbb Z}^\times$ 解釈は使っていない**(使えば $\kappa^*_3\ne0$ が従うが、それは §2 の結論を強めこそすれ変えない)。

---

## 付録 — 機械確認(`scratchpad/bsyn_gap1_full.py`・分数演算のみ・窓非接触)

$b_m$ の自前計算と Bernoulli 検算、$\chi\in\{1,3,8,15,22\}$ での $(\alpha,\beta,\gamma)$、$\bmod 7$ 還元。出力は §1.1・§2 の表そのもの(手写しなし)。
