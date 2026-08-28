# ② #fib 式の裁定 と ③ 汎用 fibre checker 仕様 v1

`DIR: 972 fake 側(落下狩り)/ FRAME: B₃-gentle`
**委嘱**: 司令塔・裁定 1717(c) の ②③。**② は implementer B の 4265 行分布が依存(即答級)。**
**格**: §1 = **裁定(確定)**+機械照合。§2 = 実装仕様(candidate)。
**著者**: 数学者(Opus 5)/ 2026-08-28。**規約 (R-1)(R-2) 準拠。**

---

# §1 ② #fib 式の読みの裁定

## 1.1 結論(1 行)

$$\boxed{\ \frac{K_{\rm ord}}{M_{\rm ord}}\ \neq\ [M:K].\ \ \textbf{2 つの因子は GT-pair }[m,f]\textbf{ の 2 座標であって、どちらも }PB_3\textbf{-指数ではない。}\ }$$

## 1.2 式の由来(なぜこの形か)

$K\le M$ に対し $R_{K,M}:GT(K)\to GT(M)$(**source-first**)。$g=[m,f]\in GT(M)$ の **raw 候補繊維**は、$g$ に還元する対 $(m',f')$ の全体である。(3.60) より還元は
$$R_{K,M}\bigl([m',f']\bigr)=\bigl(m'+M_{\rm ord}\mathbb Z,\ f'M_{F_2}\bigr)$$
なので、2 座標は**独立に**持ち上がる:

| 座標 | 持ち上げの自由度 | 個数 |
|---|---|---|
| **$m$ 方向** | $m'\in\mathbb Z/K_{\rm ord}$ で $m'\equiv m\ (M_{\rm ord})$ | $\dfrac{K_{\rm ord}}{M_{\rm ord}}$($M_{\rm ord}\mid K_{\rm ord}$ は $K\le M$ から) |
| **$f$ 方向** | $f'\in F_2/K_{F_2}$ で $f'\equiv f\ (M_{F_2})$ | $[M_{F_2}:K_{F_2}]$ |

$$\#\mathrm{fib}(K)=\frac{K_{\rm ord}}{M_{\rm ord}}\cdot[M_{F_2}:K_{F_2}]$$

- **$N_{\rm ord}$ は「$x_{12}N,x_{23}N$ の位数の lcm」**(2401 の定義)であって指数ではない。$K$ が $M$ を細分しても $K_{\rm ord}=M_{\rm ord}$ でありうる(**その場合 $m$ 因子は 1**)。
- **$[M:K]$($PB_3$ 指数)は $F_2$ 部分と中心部分を混ぜる**ので、$[M_{F_2}:K_{F_2}]$ とも別物。

## 1.3 「$M_{\rm ord}=18$ は 972 窓と別物では?」への回答 — **同一である**(機械照合)

```
gate: is M_ord = 18 really the 972 window M ?
  charming m mod 18 (gcd(2m+1,18)=1) : [0,2,3,5,6,8,9,11,12,14,15,17]   count = 12
  |GT(M)| = 972 ;  972 / 12 = 81 = 3^4 ? True
  => 972 = 12 (m-classes) x 81 (charming f-classes)  -> CONSISTENT
```
出所: `sol/sol_reply_159_iv.md` L2928 逐語 `C_M_ord=M_ord=18`(§12 = 972 窓 $M$ の $C_M$ fibre filter 節)。
**独立の裏取り**: $M_{\rm ord}=18$ から charming $m$ が 12 個、$972=12\times81$ で $\lvert GT(M)\rvert$ が割り切れる。⟹ **$M_{\rm ord}=18$ は 972 窓のもの。別物ではない。**

## 1.4 $K_2$ 実測点との整合(`gate:`)

```
gate: K2 numeric check
  K2_ord/M_ord = 36/18 = 2  (exact ? True)          <- m 方向
  [M_F2:K2_F2] = 8*3 = 24                            <- f 方向 ([M_F2:K1_F2]=8, [K1:K2]=3)
  #fib(K2) = 2 * 24 = 48   observed 48 -> MATCH ? True
```
入力の出所: `M_ord=18`(上)/ `K2_ord=36`(sol §23.11 の witness 表ヘッダ `m mod 36`)/ `[M_F2:K1_F2]=8`(OBS-UNIF-1 の `K^(36) cap N_S4` 行)/ `[K1:K2]=3`(sol §23.11 逐語)。

## 1.5 ★ 誤読の影響と再計算指示

**誤読 $\bigl(K_{\rm ord}/M_{\rm ord}\to[M:K]\bigr)$ は $\#\mathrm{fib}$ を過大評価する。**

- **最頻ケースは $K_{\rm ord}=M_{\rm ord}$**(細分が $x_{12},x_{23}$ の位数を上げない場合)⟹ **正しい $m$ 因子は 1**、$\#\mathrm{fib}=[M_{F_2}:K_{F_2}]$。誤読では**指数 $[M:K]$ 倍に膨らむ**。
- $K_2$ で両者が偶然一致することはありうる($[M:K_2]$ がたまたま 2 なら)。**1 点一致を根拠にしてはならない。**

> ### 再計算指示(implementer B 向け・4265 行分布)
> 各 LINS 行 $L$ について $K:=L\cap M$ を作り、**次の 2 量を別々に**計算する:
> 1. **$K_{\rm ord}$** = $F_2/K_{F_2}$(および中心座標)における $\bar x_{12},\bar x_{23}$ の位数の lcm。**$M_{\rm ord}=18$ との比を取る**(整除しなければ $K\not\le M$ = 入力エラー ⟹ 停止)。
> 2. **$[M_{F_2}:K_{F_2}]$** = $F_2$ 部分の指数比。**$[M:K]$ で代用しない。**
> 3. $\#\mathrm{fib}=1\times2$。**$\le100$ の選別はこの値で行う。**
> ⟹ 誤読で作った分布は**破棄して再計算**。上の 3 数を行ごとに receipt に残す(§2 の G-F1)。

---

# §2 ③ 汎用 fibre checker 仕様(implementer 実装粒度)

## 2.0 目的と射程

任意の在庫窓 $K=L\cap M$($L$ = LINS/Zassenhaus/dihedral 在庫)に対し、指定 seed の **raw 候補繊維を悉皆**し hexagon/charming/onto を判定する。
**射程**: 出るのは「その $K$ で seed が持ち上がるか」のみ。⚠ **陽性は $K$ が isolated でなければ何も記帳できない**(cofin v1.2 §9.2 W-4: 非 isolated では $GT(K)$ が群でなく $I_K$ の部分群性が消える ⟹ 二択律も 1 元経済も使えない)。**陰性(落下)は isolated 不要**(DROP-FREE)。

## 2.1 事前計算(**列挙の前に必ず**・G18 の本節版)

| # | 量 | 用途 |
|---|---|---|
| F1 | $K_{\rm ord}$、$M_{\rm ord}=18$、比 $K_{\rm ord}/M_{\rm ord}$ | $m$ 方向の自由度。**整除しなければ停止** |
| F2 | $[M_{F_2}:K_{F_2}]$ | $f$ 方向の自由度 |
| F3 | $\#\mathrm{fib}(K)=$ F1$\times$F2 | **予算確定。列挙前に確定する** |
| F4 | $K^\diamond=K$ か(isolated 判定) | 陽性を記帳できるか |
| F5 | $\lvert F_2/K_{F_2}\rvert$ | 述語評価の作業サイズ |

## 2.2 2 モード

### モード A(**row 36 モード** = 1 元経済・DICHOT (3))
- **入力**: $g^\ast=$ row 36(zero-based・`seed_pool_432` 凍結・**c′ 非依存**)。
- **問い**: $g^\ast\in\mathrm{im}(R_{K,M})$ か。
- **出口**: `LIFT_EXISTS`(witness 1 本で停止可)/ `NO_LIFT`(**悉皆必須・early stop 禁止**)。
- **`NO_LIFT` が出たら即時停止**(§2.6)。

### モード B(**row 71 モード** = 全 fibre 悉皆・T-DEAD 教訓)
- **入力**: row 71(相互 canary 座標・$c'\iff[0,f_2]$)。
- **問い**: 繊維の**完全な pass/fail 表**。
- **なぜ悉皆か**: **族の死 ≠ shadow の死**。閉形式族(`RUNG-UNIF` の $y^\nu x^{-\nu}w$ 型)が死んでも、別の語で持ち上がりうる(T-DEAD の教訓・`d972` §10.4-2)。⟹ **「閉形式が書けない」を `NO_LIFT` と読んではならない。**
- **出口**: 完全表 + `pass_count`。**early stop 禁止(陽性でも)。**

⚠ **2 モードは同じ列挙器を使い、停止規則だけが違う。**述語コードを分岐させない(分岐は事故源)。

## 2.3 判定述語(順序を固定する)

各候補 $(m',f')$ に対し、**この順で**評価:
1. **charming**: $2m'+1\in(\mathbb Z/K_{\rm ord})^\times$ かつ $f'K_{F_2}\in[F_2/K_{F_2},F_2/K_{F_2}]$。
2. **hexagon 簡約形**(Prop 3.4・$f\in[F_2,F_2]$ 前提が 1 で確認済):(3.10) $f\theta(f)\in K_{F_2}$、(3.11) $\tau^2(y^{m'}f)\tau(y^{m'}f)y^{m'}f\in K_{F_2}$。
 ⚠ **$\theta,\tau$ は自由群の語レベルで適用してから商へ落とす**(定義ノート §2 の注意: $c\notin K$ の対象では商上の近道が壊れる)。
3. **onto**: $\langle\bar x^{2m'+1},\ \bar f^{-1}\bar y^{2m'+1}\bar f\rangle=F_2/K_{F_2}$(Prop 3.6 の $F_2$ 版)。
4. **reduction 一致**: $R_{K,M}([m',f'])=g^\ast$(seed への還元の再確認)。

## 2.4 producer/checker 分離

| | producer | checker |
|---|---|---|
| 入力 | 窓 $L$、$M$、seed、規約宣言 | **producer の receipt の bytes/SHA/path のみ**(source/helper は開かない) |
| 出力 | candidate roster、per-candidate verdict、digests、F1–F5 | 独立に roster を再構成し verdict を再演、digest 突合 |
| 実装 | 別著者・別ライブラリ | 標準ライブラリのみ・import 共有禁止 |

**必須 digest**: `candidate_roster`, `verdict_matrix`, `seed_key`, `window_source`, `convention_block`。

## 2.5 較正必達値(**通らなければ本走禁止**)

| 窓 | $\#\mathrm{fib}$(F3) | valid lift 数 | 出所 |
|---|---|---|---|
| $K^{(36)}\cap N_{S4}$ | 要計算(F1×F2) | **2** | OBS-UNIF-1 |
| $K_Q=M\cap N_Q$ | 同 | **2** | OBS-UNIF-1 |
| LINS-48B | 同 | **2** | 便 159 |
| $K_H=M\cap N_0$(Heisenberg) | 同 | **3** | OBS-UNIF-1 |
| PΓL(2,8) 窓 | 同 | **9** | OBS-UNIF-1(第 4 行) |
| **$K_2=K_1\cap\ker(\exp_{B_3}\bmod3)$** | **48** | **2**(R07/R40) | sol §23.11 |

⚠ **OBS-UNIF-1 の 2,2,2,3,9 は GT-繊維(valid 数)であって $\#\mathrm{fib}$(raw)ではない。**両者を**別欄**で報告すること(混同は D-6 型事故)。$K_2$ は raw 48・valid 2 の**両方が既知**なので、**2 数一致の較正点として最重要**。

## 2.6 ★ 落下(モード A の `NO_LIFT`)が出た場合 — 証明書の完全性要件

**落下 1 件で 648 が一括決着する**(DROP-FREE + M7)ので、証明書は最初から完全形で作る。

| # | 要件 | 検査 |
|---|---|---|
| **CC-1** | **候補被覆の完全性**: `evaluated_count == #fib(K)`(F3 の予測値と一致)・omission 0・duplicate 0 | 予測 F3 と実測の**厳密一致**。ずれたら列挙器が壊れている |
| **CC-2** | **early stop なし**: 全候補に verdict が付く | verdict 行数 = F3 |
| **CC-3** | **seed の同一性**: `seed_key_digest` が `seed_pool_432` row 36 の凍結値 | `symdiff_432` から取っていないこと |
| **CC-4** | **窓の適格性**: $K\le M$(F1 の整除で自動検査)・$K\in\mathrm{NFI}_{PB_3}(B_3)$ | 陰性には isolated 不要だが**記録は必須** |
| **CC-5** | **規約ブロック**: `reduction_index_order:"source_first"`・$\theta/\tau$ の語レベル適用・W-1 の向き | 欠落 cert は格付け対象外 |
| **CC-6** | **mandatory mutants(全て拒否されること)** | 下表 |

**mandatory mutants**(既存 8 + 本件固有 4):
1. source omission / 2. duplicate / 3. wrong parent inclusion($K\not\le M$)/ 4. non-isolated source を isolated と偽る / 5. seed を `symdiff_432` から取る / 6. row 0/1-based shift / 7. **W-1 reverse**(paper 順 ↔ GAP 順)/ 8. charming と onto の取り違え
9. ★ **$\#\mathrm{fib}$ を $[M:K]\cdot[M_{F_2}:K_{F_2}]$ で計算**(§1.5 の誤読)⟹ CC-1 が発火せねばならない
10. ★ **$m$ 方向を落とす**($\#\mathrm{fib}=[M_{F_2}:K_{F_2}]$ 固定)⟹ $K_{\rm ord}>M_{\rm ord}$ の窓で CC-1 発火
11. ★ **$\theta/\tau$ を商上で評価**(語レベルを飛ばす)⟹ $c\notin K$ の窓で判定が変わる
12. ★ **reduction の添字順を target-first に**⟹ CC-5 で停止

**出口**: CC-1〜CC-6 全通過 + producer/checker 一致で初めて `ROW36_NO_LIFT_CROSS_CHECKED`。**それ以前は `RUNG_FALL_CANDIDATE` にも昇格しない。**

## 2.7 実行計画($\#\mathrm{fib}\le100$ の 61 窓・cheap-first)

1. **段 0(全窓・列挙なし)**: 61 窓すべてで F1–F5 を計算し `budget_table` を出す。**ここで $\#\mathrm{fib}$ の分布が確定**(§1.5 の再計算)。
2. **段 1(較正)**: §2.5 の 6 窓を走らせ 2 数一致を確認。**不一致なら本走禁止。**
3. **段 2(本走・cheap-first)**: `budget_table` の $\#\mathrm{fib}$ 昇順にモード A を回す。
 - **venue**: 1 窓ごとに**実測後に判定**($\#\mathrm{fib}$ と述語評価の実測時間から)。ローカル 10 分超が見えたら GHA へ。**GHA なら falsifier 前哨必須**(工房 lane の規律)。
 - **落下が出たら即時停止**し §2.6 の証明書へ。
4. **段 3(モード B)**: row 71 を、段 2 で生き残った窓のうち**安い順に数窓**。相互 canary の材料。

⚠ **段 2 は「深いほど落ちやすい」が MONO(包含鎖上のみ)であることに注意**(cofin v1.2 §6.3 W-2)。**在庫窓どうしは大半が非比較**なので、cheap-first は**コスト最適化であって殺傷力の最適化ではない**。

## 2.8 UNKNOWN(推測で埋めていない)

1. **61 窓の $\#\mathrm{fib}$ 分布は未計算**(§1.5 の再計算待ち)。**「$\le100$ が 61 窓」という数自体が誤読分布に基づく可能性がある** ⟹ 段 0 で再確定すること。
2. 較正 6 窓のうち **$K_2$ 以外の raw $\#\mathrm{fib}$ は未計算**(valid 数のみ既知)。
3. **モード B の row 71 の $\#\mathrm{fib}$** 未計算。
4. 各窓の **isolated 判定($K^\diamond=K$)のコスト**は未評価($\diamond$ 閉包は高い ⟹ **陰性狙いなら不要**、陽性記帳時のみ必要)。
