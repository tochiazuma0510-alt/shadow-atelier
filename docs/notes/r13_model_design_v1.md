# 【R-1〜R-3 設計】$K^{(9)}$ 窓の厳密モデル構成 — wac_v1 手法の移植設計と作業指示書

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 942 項 ②
**格**: candidate(設計・**Sol 未監査**)。**走行ゼロ**。
**前提**: `docs/notes/p8_corr_v1.md`(P8-CORR・三値判定 = 別対象)/ `docs/notes/t63_reconnaissance_v1.md` §2(幾何の設定)

> ## ⚠⚠ 本設計書の禁止事項((F3) 順序要件・裁定 942)
> $$\boxed{\ \textbf{数値出力は一切しない。設計は}\textbf{記号のまま}\textbf{。}\ }$$
> - $u_9$・$a_9$・$\operatorname{ord}(a_9)$ の**値および中間値に触れない**。
> - 窓の構造量($\deg\lambda_9$・$g(W_9)$ 等)も**私は出さず**、**実装係の R-0 で確定させる**(予言対象には触れないが、順序要件に最も忠実な運用を採る)。
> - ★ **本設計書の実行は prereg カード凍結後**(`p8_corr_v1.md` §5・(F3))。**R-0 のみ先行可**(§3.1 参照)。

---

## §1 wac_v1 手法の抽出 — **流用可能部**と**窓依存部**の分離

### 1.1 手法の骨格(cert / スクリプト構造から抽出・数値非接触)

| 段 | 内容 | 出所 |
|---|---|---|
| **W-a** | 被覆曲線 $C$ の**厳密モデル**を得る(hyperelliptic 形 $y^2=f_6(x)$) | `u_meas_caseb_a5_20260731.json` の `exact_solution`(`exact_verification_all_zero = true`) |
| **W-b** | 被覆写像 $t$ を $C$ 上の関数として**明示表示**($t=A(x)+B(x)\,y$ 型) | 同 cert `our_object.model` |
| **W-c** | cusp を選び**有理 uniformizer** を取る($\infty_+$・$s=1/x$) | 司令塔伝達 + `u_meas_uloc_v2` |
| **W-d** | ★ **Norm 経路**で主係数を抽出: $N_\tau(x)=(A(x)-\tau)^2-f_6(x)B(x)^2$、$\kappa$ = $N_\tau$ の**最高次係数**、$\delta=\tau-t(\text{cusp})$、$u_0^{-1}=\kappa\cdot(\cdots)$ | `u_meas_m7b_v2` の `M7_B1.method` 逐語 |
| **W-e** | **GATE**(冪判定・Frobenius パターン)で健全性を確認 | `u_meas_uloc_fire2.py` の GATE 1a/1b |
| **W-f** | ★ **PREREGISTRATION(u 計算より前に凍結)** → **FIRE** | 同 `(2) PREREGISTRATION, frozen before any u computation` / `(3) FIRE` |

> ### ★★ 発見 — **prereg は既に実装実績がある**
> `search/probe/wac_v1/u_meas_uloc_fire2.py` は **`(2) PREREGISTRATION, frozen before any u computation`** を**コード構造として持つ**。⟹ `p8_corr_v1.md` §5 のカード案は**新様式ではなく既存様式の $K^{(9)}$ 版**であり、**実装コストは低い**。

### 1.2 ★ 流用可能部 / 窓依存部

| 分類 | 項目 |
|---|---|
| ★ **流用可能(設計を差し替えるだけ)** | **W-c**(cusp + 有理 uniformizer の取り方)/ **W-d**(Norm 経路による主係数抽出の**論理**)/ **W-e**(GATE の型)/ **W-f**(prereg + FIRE の**枠組み**) |
| ⚠ **窓依存(新規に作る)** | **W-a**(モデル — **曲線の種数と型が変わりうる**)/ **W-b**($t$ の明示表示)/ **W-d の具体形**(hyperelliptic を前提にした $(A-\tau)^2-f_6B^2$ は**種数 2 かつ超楕円の場合の形**) |

$$\boxed{\ \textbf{⟹ 移植の成否は }\textbf{W-a(モデル)}\ \textbf{に集中する。そこを先に判定するのが }\textbf{R-0}\ }$$

---

## §2 $K^{(9)}$ 窓への移植設計

### 2.0 対象の型(**先に固定** — P8-CORR の教訓)

| 項目 | 記号 | 出所 |
|---|---|---|
| 窓 | $H_9^{\rm fun}\le P_9$($P_9=PB_3/K^{(9)}$ 系) | t63 A5 / HF-2 |
| 被覆 | $\lambda_9:W_9\to\mathbf P^1_t$、$W_9=P_9/H_9^{\rm fun}$ | t63 §2.1 |
| 次数 | $D:=\deg\lambda_9=[P_9:H_9^{\rm fun}]$ | ★ **R-0 で確定** |
| 種数 | $g:=g(W_9)$ | ★ **R-0 で確定** |
| cusp | $P_0^{(9)}$、$\lambda_9^{-1}(0)=\{P_0^{(9)}\}$(全分岐) | t63 A6 |
| 分岐指数 | $e(\lambda_9,P_0^{(9)})=M_9=2\cdot9=18$ | t63 A6 |
| 基礎体 | $F_9=\mathbf Q(\zeta_{36})$ | E1 §5.1 |
| 標的 | $\lambda_9=u_9\,s_9^{18}\bigl(1+O(s_9)\bigr)$ の**主係数 $u_9\in F_9^\times$** | t63 §2.2 |

### 2.1 ★ R-0(**前提確認**・新設)— 設計の分岐点

**実装係が出すもの**(いずれも $u_9$ の値に触れない**構造量**):

| # | 項目 | 方法 |
|---|---|---|
| R-0-a | $D=[P_9:H_9^{\rm fun}]$ | GAP: $H_9^{\rm fun}$ を構成し指数を取る(★ $n=3$ の先例 = `c1_class_check_20260728.json` の `h2fun_index`) |
| R-0-b | 分岐データ(各 $P_i$ 上の cycle type) | GAP: $P_9$ の $H_9^{\rm fun}$ 上の置換表現で $x,y,z$ の像の cycle type |
| R-0-c | **種数 $g$** | Riemann–Hurwitz: $2g-2=D\,(2\cdot0-2)+\sum_{P}\bigl(e_P-1\bigr)$(分岐は $0,1,\infty$ の上のみ = Belyi) |
| R-0-d | $H_9^{\rm fun}$ の**自己正規化**と**窓 assert** | $n=3$ の先例に倣う(`h2fun_self_normalizing`) |

$$\boxed{\ \textbf{★ }g\ \textbf{の値が設計を二枝に分ける(2.2)}\ }$$
⚠ **R-0 は $u$ に触れないので prereg 凍結前に走らせてよい**(むしろ **prereg カードの [5] window_assert を書くために先に要る**)。

### 2.2 R-1(モデル構成)— **二枝設計**

| 枝 | 条件 | 設計 |
|---|---|---|
| ★ **枝 H**(hyperelliptic) | $g\le2$、または $W_9$ が超楕円 | ★ **wac_v1 をほぼそのまま流用**: $y^2=f(x)$ 型の厳密モデルを未定係数法+Gröbner で解く(`u_meas_caseb_groebner*.py` 系の設計を流用) |
| ⚠ **枝 P**(plane / 一般) | $g\ge3$ かつ非超楕円 | 平面モデル(特異点つき)+ 正規化、または **$\mathbf P^1$ 上の相対的記述**($\lambda_9$ を有理写像として直接扱う)。⚠ **wac_v1 の $(A-\tau)^2-f_6B^2$ 形は使えない** ⟹ W-d を **resultant / norm form** の一般形へ差し替え(下記 2.4) |

★ **どちらの枝でも共通の要件**: モデルは **$F_9=\mathbf Q(\zeta_{36})$ 上で厳密**(浮動小数点禁止)。

### 2.3 R-2(cusp と有理 uniformizer)

1. $\lambda_9^{-1}(0)=\{P_0^{(9)}\}$(t63 A6)を**機械で確認**(fail-closed)。
2. $P_0^{(9)}$ が **$F_9$-有理点**であることを確認(★ そうでなければ **UNKNOWN (u3)** で停止)。
3. $F_9$-有理な uniformizer $s_9$ を取る(wac_v1 の $s=1/x$ に相当する選択)。
4. ★ **uniformizer の取り替えで結論が不変**であることを確認(t63 §2.2・私の `k9_t63_gap2_audit_v1.md` §3.2 で代数は検算済 ⟹ **実装は 2 通りの $s_9$ で走らせて一致を見る**)。

### 2.4 R-3(主係数の抽出)— Norm 経路の一般形

**wac_v1 の形**(超楕円・次数 2 の被覆の norm):
$$N_\tau(x)=(A(x)-\tau)^2-f_6(x)B(x)^2,\qquad \kappa=\mathrm{lc}(N_\tau),\qquad \delta=\tau-t(\text{cusp}).$$

**一般形へ差し替える設計**(枝 P でも通る形):
$$\boxed{\ N_\tau(x)\ :=\ \mathrm{Res}_{\,\text{fiber coord}}\bigl(\ \lambda_9-\tau,\ \ \text{(モデルの定義式)}\ \bigr)\ }$$
すなわち $\lambda_9-\tau$ の**ファイバー座標に関する終結式**(= $t-\tau$ のノルム)を取り、その**最高次係数** $\kappa$ を読む。超楕円の場合これは $(A-\tau)^2-f B^2$ に退化する ⟹ **wac_v1 の形の一般化**。

**主係数の読み出し**: $s_9$ 展開で
$$\lambda_9=u_9\,s_9^{18}\bigl(1+O(s_9)\bigr)\ \Longrightarrow\ u_9=\lim_{s_9\to0}\ \lambda_9\,s_9^{-18}$$
を**厳密級数展開**(sympy の `series`/`nseries` ではなく**多項式演算**で)実行する。

⚠★ **本工程の出力は prereg 凍結後にのみ開示**((F3))。⟹ **実装は「計算して cert に書くが、判定はしない」**(wac_v1 の `d_no_interpretation` を継承)。

---

## §3 実装係への作業指示書

### 3.1 工程と発注順(★ **prereg との前後関係が重要**)

| 工程 | 内容 | prereg 前後 | 依存 |
|---|---|---|---|
| ★ **R-0** | 前提確認($D$・分岐・$g$・窓 assert) | ★ **前でよい**(むしろ prereg カードに必要) | なし |
| **R-1** | 厳密モデル構成(枝 H / 枝 P) | ★ **前でよい**($u$ に触れない) | R-0 |
| **R-2** | cusp + 有理 uniformizer + 全分岐確認 | ★ **前でよい** | R-1 |
| ⚠ **R-3** | **主係数 $u_9$ の抽出** | ✘ ★ **prereg 凍結後のみ** | R-2 + **prereg カード** |
| — | R-4 以降(`b_value_9`・$a_9$ の位数) | ✘ prereg + **Sol K9 監査 PASS** 後 | 裁定 942 |

$$\boxed{\ \textbf{⟹ R-0/R-1/R-2 は }\textbf{今すぐ発注してよい}\ \textbf{。R-3 で止める。}\ }$$

### 3.2 指示書(**そのまま渡せる形**)

```
=== 作業指示: R-0〜R-2(K^(9) 窓の厳密モデル構成)===
発注根拠 : 司令塔裁定 942 / 設計 = docs/notes/r13_model_design_v1.md
★ 停止線 : R-2 まで。R-3(主係数 u_9 の抽出)には着手しないこと。
           理由 = (F3) 順序要件(prereg カード凍結が先)。

[R-0] 前提確認(GAP)
  (a) H_9^fun を構成し D := [P_9 : H_9^fun] を出す
      ※ n=3 の先例 = search/certs/c1_class_check_20260728.json
        (pn_size / h2fun_size / h2fun_index / h2fun_self_normalizing)
  (b) P_9 の H_9^fun 上の置換表現で x,y,z の像の cycle type を出す
  (c) Riemann-Hurwitz で genus g を出す(分岐は 0,1,∞ の上のみ)
  (d) 窓 assert: H_9^fun が自己正規化か・n=3 の先例と同型の検査を通すか
  出力: cert (schema r13-r0/v1)。⚠ u に一切触れないこと。

[R-1] 厳密モデル構成
  枝の判定: g <= 2 または超楕円 → 枝 H / それ以外 → 枝 P(司令塔へ報告)
  枝 H: 未定係数法 + Gröbner で y^2 = f(x) 型の厳密モデル
        ※ 設計流用元 = search/probe/wac_v1/u_meas_caseb_groebner*.py
  枝 P: 着手前に司令塔・数学者へ報告(設計の差し替えが要る)
  要件: 係数はすべて F_9 = Q(zeta_36) 上で厳密(浮動小数点禁止)
        exact_verification_all_zero 相当の検算を必ず入れる
  出力: cert (schema r13-r1/v1)

[R-2] cusp と有理 uniformizer
  (a) lambda_9^{-1}(0) = {P_0^(9)} を機械確認(fail-closed)
  (b) P_0^(9) が F_9-有理点であることを確認
      → 有理でなければ即停止し UNKNOWN(u3) として報告
  (c) F_9-有理な uniformizer s_9 を取る
  (d) ★ 2 通りの s_9 を取り、後段の結論が不変であることを設計上確認できる
      形で両方を cert に記録(値の比較は R-3 以降)
  出力: cert (schema r13-r2/v1)

[共通の記録要件]
  u_touched            : false        ★ R-0〜R-2 では必ず false
  d_no_interpretation  : "machine values only; verdict は司令塔"
  window_assert        : H_9^fun であることの機械確認結果
  M_assert / F_assert  : M = 18, F_9 = Q(zeta_36) の機械確認
  helper_disjoint      : 照合器を別途書く場合は helper 非共有を明記
=== END ===
```

---

## §4 fail-closed 条項と検算

| # | 条件 | 動作 |
|---|---|---|
| F-1 | $\lambda_9^{-1}(0)$ が 1 点でない | ★ **即停止**。t63 A6 と矛盾 ⟹ 前提の再検討(**設計の誤り**を疑う) |
| F-2 | $e(\lambda_9,P_0^{(9)})\ne18$ | ★ **即停止**。$M_9=2n$ の規約が崩れる(P8-CORR の法の取り違えと同型の事故) |
| F-3 | $P_0^{(9)}$ が $F_9$-有理でない | **UNKNOWN (u3)** で報告(prereg カードの UNKNOWN 条項) |
| F-4 | モデルが厳密に閉じない(浮動小数点が残る) | ★ **即停止**。wac_v1 は `exact_verification_all_zero=true` を達成している ⟹ **同水準を要求** |
| F-5 | 枝 P(非超楕円)と判明 | **司令塔・数学者へ報告**(W-d の一般形〔§2.4〕へ設計差し替え) |
| F-6 | $u$ に触れる出力が cert に混入 | ★ **即停止**((F3) 違反)。`u_touched` を必ず検査 |

**検算の型**(wac_v1 の実績を継承): ① 厳密検証(全項ゼロ)② 複数素点での剰余一致(`residues` 相当)③ 2 通りの uniformizer での不変性(R-2(d))。

---

## §5 【GAP】・見積り・申告

| # | 内容 | 重さ |
|---|---|---|
| ★ **【R13-GAP-1】** | **$H_9^{\rm fun}$ の構成そのもの**(i8_bridge が「窓 campaign 待ち」と記す当のもの)⟹ **R-0-a が本体** | ★★ 大 |
| **【R13-GAP-2】** | 枝 P(非超楕円)の場合の W-d 一般形(終結式)の**実装可能性** — 設計は書いたが**実行可能性は未確認** | ★ 中 |
| **【P8-GAP-1】**(継承) | **(7.1)** の一次定義(R-4 の前提・実装係が grep 中) | 中 |

**見積り**(candidate): **R-0 は小**(GAP・$n=3$ の先例あり)。**R-1 は枝による** — 枝 H なら wac_v1 と同規模、**枝 P なら設計から作り直し**で数倍。**R-2 は小**。
$$\boxed{\ \textbf{⟹ }R\text{-}0\ \textbf{を最優先で走らせ、}g\ \textbf{を確定させるのが最も情報量が大きい}\ }$$

**帰属**: wac_v1 の手法(W-a〜W-f)= 実装係(2026-07-31・裁定 268–272)。委嘱 = 司令塔(裁定 942)。
**本設計の新規部分**: ① wac_v1 手法の**流用可能部/窓依存部の分離**(移植の成否は W-a に集中)② **R-0(前提確認)工程の新設**と $g$ による**二枝設計** ③ **W-d の一般形(終結式)への差し替え設計** ④ **prereg との前後関係の明示**(R-0/R-1/R-2 は前でよい・**R-3 で止める**)⑤ **fail-closed 6 条項** ⑥ ★ **prereg が wac_v1 に実装実績を持つ**ことの発見(実装コストが低い)。
**申告**: ★ **数値出力ゼロ**($D$・$g$ も出していない)。走行ゼロ。**Sol 未監査**。⟹ **verified ではない**。
