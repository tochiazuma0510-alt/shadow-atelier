# Sol 便 128 返信 — 手 2 ゲート / entangled 屋根

日付: 2026-08-13

入力: `ops/inbox_codex/sol_task_128_entangled.txt` 全節

仕様正本: `docs/notes/ab_instrument_redesign_v1.md` (指定 commit `98e2e309`)

## F128-0. 到達段と一行結果

条件付きパイプラインは **段 1 (手 2)** まで到達した。指定 predicate の生値は

```text
hand2_same_invariant_PB3_S3_quotient_raw_boolean = false
stage_reached = 1
stopped_after_hand2 = true
```

である。$F_2\twoheadrightarrow S_3$ は 18 本、核は 3 類あるが、$\tau$ が三類を巡回するため、$\theta,\tau$ の双方で不変な全射核は **0 類**だった。$G_9\twoheadrightarrow S_3$ の 18 本は、制約を外せばこの三類全てと一致する。しかし eligible な不変核との共通類は空である。

委嘱の fail-closed 規則に従い、段 2 の $N_E$ 構成、entangled roof gate、事前登録、SINGLE-BIT 測定は実行していない。

\[
|\operatorname{Im}R|_{\rm raw}=\texttt{null}\quad(\text{未測定}),
\qquad\text{全体状態}=\mathrm{UNKNOWN}.
\]

## F128-1. 手 2 — $\operatorname{Hom}(F_2,S_3)$ の全 36 写像

### F128-1.1. 宇宙の完全性

$F_2=\langle x,y\rangle$ なので写像は $(\varphi(x),\varphi(y))\in S_3^2$ に一意に対応し、宇宙は $6^2=36$ 通りで尽きる。$PB_3=F_2\times\langle c\rangle$ からの全射 $PB_3\twoheadrightarrow S_3$ では、中心元 $c$ の像は $Z(S_3)=1$ に入るため必ず消える。従ってこの 36 通りは pure $S_3$ quotient の全宇宙でもある。

生値:

| 像の位数 | 写像数 |
|---:|---:|
| 1 | 1 |
| 2 | 9 |
| 3 | 8 |
| 6 | 18 |
| **合計** | **36** |

核同値類は 11 類。kernel ID `qk_oabc` は

\[
k=|\operatorname{Im}\varphi|,qquad
(a,b,c)=(\operatorname{ord}\varphi(x),\operatorname{ord}\varphi(y),
\operatorname{ord}\varphi(xy))
\]

を表す。この 11 signature は $S_3$ 内の標識対の同時共役軌道を全て区別する。

### F128-1.2. 全 11 核類と $\theta,\tau$ 作用

$z=(xy)^{-1}$ として

\[
\theta:(x,y)\mapsto(y,x),qquad
\tau:(x,y)\mapsto(y,z)
\]

を用いた。

| kernel ID | $|\operatorname{Im}|$ | map 数 | $\theta$ target | $\tau$ target | 両方不変 |
|---|---:|---:|---|---|:---:|
| `q1_o111` | 1 | 1 | `q1_o111` | `q1_o111` | true |
| `q2_o122` | 2 | 3 | `q2_o212` | `q2_o221` | false |
| `q2_o212` | 2 | 3 | `q2_o122` | `q2_o122` | false |
| `q2_o221` | 2 | 3 | `q2_o221` | `q2_o212` | false |
| `q3_o133` | 3 | 2 | `q3_o313` | `q3_o331` | false |
| `q3_o313` | 3 | 2 | `q3_o133` | `q3_o133` | false |
| `q3_o331` | 3 | 2 | `q3_o331` | `q3_o313` | false |
| `q3_o333` | 3 | 2 | `q3_o333` | `q3_o333` | true |
| `q6_o223` | 6 | 6 | `q6_o223` | `q6_o232` | false |
| `q6_o232` | 6 | 6 | `q6_o322` | `q6_o322` | false |
| `q6_o322` | 6 | 6 | `q6_o232` | `q6_o223` | false |

両作用で不変な核は `q1_o111` と `q3_o333` の 2 類だけである。前者の像は自明、後者は便 127 で扱った対角 $C_3$。**像 $S_3$ の三類には両作用不変なものが無い。**

全射三類に限ると作用は

\[
\begin{aligned}
\theta &: (q6\_o223)(q6\_o232\ q6\_o322),\\
\tau &: (q6\_o223\ q6\_o232\ q6\_o322).
\end{aligned}
\]

従って三類は一つの $\langle\theta,\tau\rangle$-軌道である。

## F128-2. $G_9$ 側 18 本との突合

正典 marking の $G_9=PB_3/K^{(9)}$ を 27 点置換群として再構成し、36 assignments 全てについて marked Cayley map の well-definedness を調べた。

| 項目 | 生値 |
|---|---:|
| $|G_9|$ | 2916 |
| assignments checked | 36 |
| $G_9$ 上 well-defined | 28 |
| 像 1 | 1 |
| 像 2 | 9 |
| 像 6 | 18 |
| $G_9\twoheadrightarrow S_3$ | 18 |
| 各全射の kernel order in $G_9$ | 486 |
| 全射 kernel classes in $F_2$ | 3 |

8 本の $C_3$ assignments は $G_9$ に降りず、便 127 の 3-part 不在と一致する。18 本の全射の核類は

```text
q6_o223, q6_o232, q6_o322
```

であり、$F_2\twoheadrightarrow S_3$ の全射三類と完全に同じである。

突合の二つの生値を分離すると:

```text
unrestricted_same_S3_kernel_class_count = 3
theta_tau_invariant_surjective_kernel_class_count = 0
eligible_invariant_same_S3_kernel_class_count = 0
antecedent_iii_raw_boolean = false
```

すなわち「同じ $PB_3$ 商」は制約なしなら三類あるが、委嘱が先に要求した **個別核の $\theta,\tau$ 不変性**を同時に課すと空になる。

### F128-2.1. 三核の不変交叉

全射三核の交叉は $\theta,\tau$ 不変になる。その marked quotient の生値は

| 項目 | 生値 |
|---|---:|
| quotient order | 108 |
| derived order | 27 |
| abelianization order | 4 |
| marked-isomorphic to $G_3$ | true |

である。従って三核を不変化すると得られるのは $S_3$ ではなく $G_3$ である。この値は producer/checker が別々に再構成した。

## F128-3. 指定ゲートの射程

今回の `false` から閉じるのは

```text
direct_stable_S3_factor_candidate_closed = true
```

である。一方、次は主張しない。

```text
global_absence_of_entangled_roofs_claimed = false
axis_1_global_death_authorized_by_this_gate = false
```

理由は $G_9$ 自身に見えている。$G_9$ は $\theta,\tau$-安定な quotient だが、その三つの $S_3$ quotient kernels は個別不変でなく相互に置換される。従って「個別不変な $S_3$ 核が無い」ことは、より大きい安定商 $E$ の内部で複数の $S_3$ 商が置換される方式まで排除しない。

委嘱どおり後段へは進まないが、括弧書きの「軸 1 全体の死」をこの生値だけから導くのは射程過大である。閉じたのは **単独の不変 $S_3$ 核、および characteristic な直積 $S_3$ 因子を使う案**である。

## F128-4. SPLIT-TWIN 輸入の型監査

`ribet_dig_campaign_v1_addendum_a.md` §3.3 の SPLIT-TWIN は

\[
E_p=C_p\rtimes(C_3\times S_3),\qquad |E_p|=18p
\]

を **$B_3/N$** として構成する。その $E_p\twoheadrightarrow S_3$ は標準の外側 quotient

\[
B_3/N\twoheadrightarrow B_3/PB_3\cong S_3
\]

である。pure subgroup image はその核なので

\[
|PB_3/N|=|E_p|/6=3p.
\]

$p$ は奇数だから $3p$ は奇数であり、$PB_3/N$ は $S_3$ へ全射できない。従って生値は

```text
SPLIT_TWIN_imports_pure_S3_antecedent_i = false
```

である。仕様正本の「$C_3\times S_3$ が $B_3$ 窓商であることから pure $S_3$ 橋を輸入できる」という読みは、外側 quotient と pure quotient の型を混同している。SPLIT-TWIN 自体の記述を否定するものではない。

## F128-5. 条件付き段 2–3 の未到達記録

段 1 が false のため、委嘱の順序どおり停止した。

| 段・欄 | 生値 |
|---|---|
| 段 2: $N_E$ / entangled roof construction | not reached |
| 段 2: pure quotient non-product check | not reached |
| 段 3: size gate | not reached |
| preregistration created | false |
| frozen spectrum / branch destinations | null |
| blind declaration | null |
| measurement authorized | false |
| measurement performed | false |
| reduction image set formed | false |
| $|\operatorname{Im}R|$ raw | null |
| finite-depth B type recognition | false |
| status | UNKNOWN |

324 は「可到達候補」という設計値のままであり、本便の観測値ではない。

## F128-6. producer/checker 生出力

producer:

```json
{"G9_epimorphism_kernel_classes": 3, "G9_epimorphisms": 18, "eligible_common_kernel_classes": 0, "hand2_raw_boolean": false, "hom_F2_S3": 36, "image_distribution": {"1": 1, "2": 9, "3": 8, "6": 18}, "raw_image_size": null, "run_id": "d972-entangled-hand2-20260813T035300Z", "stage_reached": 1, "status": "UNKNOWN", "surjective_kernel_classes": 3, "theta_tau_invariant_surjective_kernel_classes": 0, "unrestricted_common_kernel_classes": 3}
```

helper 非共有 checker:

```json
{"G9_epimorphism_kernel_classes": 3, "G9_epimorphisms": 18, "G9_order": 2916, "G9_well_defined_maps": 28, "all_checks_true": true, "eligible_common_kernel_classes": 0, "hand2_raw_boolean": false, "hom_F2_S3": 36, "image_distribution": {"1": 1, "2": 9, "3": 8, "6": 18}, "kernel_classes": 11, "raw_image_size": null, "stage_reached": 1, "status": "UNKNOWN", "surjective_kernel_classes": 3, "surjective_kernel_intersection_marked_G3": true, "surjective_kernel_intersection_quotient_order": 108, "theta_tau_invariant_surjective_kernel_classes": 0, "unrestricted_common_kernel_classes": 3}
```

再現:

```powershell
python search/d972_entangled_hand2_v1.py --hard-timeout-seconds 300
python search/check_d972_entangled_hand2_v1.py --hard-timeout-seconds 300
```

producer は SymPy permutation group と marked Cayley traversal を使用した。checker は Python 標準ライブラリの tuple permutations、$S_3$ 同時共役軌道、27 点上の $G_9$ 直接再構成を使用し、producer を import していない。双方に atomic checkpoint と hard-timeout がある。

## F128-7. 成果物と SHA-256

| path | SHA-256 |
|---|---|
| `search/d972_entangled_hand2_v1.py` | `78dfcd8e5b19047dce03e53a9877da24be0c452203c10d84268048bb68823afd` |
| `search/check_d972_entangled_hand2_v1.py` | `993c6920c5ca2e701200b6e15072d9136f413eb7bf9d0679a5f5242fb107414f` |
| `search/certs/d972_entangled_hand2_v1_20260813.json` | `1b734d6c058389ef7acfffe39976c548d3134e4c9a4e962656671b401595f048` |
| `search/certs/d972_entangled_hand2_v1_check_20260813.json` | `cc64b374046624eadf4d6114a6530bf22f76e72627474effcb5585719855b602` |
| `search/certs/d972_entangled_hand2_v1_checkpoint.json` | `82e98cd9d7d37fc28a44b00da896c95400c5e7e50d085f63c000b455a17a2dfc` |
| `search/certs/d972_entangled_hand2_v1_check_checkpoint.json` | `e8e391f56507d4d775ca04af11f5a55aaf64041e89463c64d23762235291652e` |

格は producer/checker 二系統一致の cross-checked candidate。Lean 証明書は本便の射程外である。

## F128-8. 規律・git

- u/c 非接触、封印 K5 非接触、既存事前登録量の変更なし。
- NAME-COLLIDE は kernel ID と generator-order signature を併記して回避した。
- 有限深度から B 型を認定していない。
- HEAD `be712298e8427b13edfdb09ca5eb11a704a1dced`、branch `master`。
- git は read-only。commit / push / workflow dispatch は行っていない。
- 本便の producer/checker/cert/checkpoint と本返信以外の既存 dirty worktree は変更していない。

