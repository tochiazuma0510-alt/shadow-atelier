# Sol 便 113 返信 — k=3 両車線本体

作成: Sol / 2026-08-12  
対象: `ops/inbox_codex/sol_task_113_k3_mainlines.txt` 全節 0–5  
格付け: **exact candidate computation + import-free cross-check**（Lean verified ではない）

## 0. 結論

- **車線 1（t3, m=4）**: 指定した (F_9)-有理極点
  (Pi_0=-Q_0=(0,-2)) に対し、**(F_9)-有理解なし**。
  producer の ideal は単位 ideal、独立 checker は Gröbner 基底を再利用せず
  非零障害 `645911` を再導出した。したがって委嘱範囲での
  `m4_solution_exists_over_F9=false`。m=2 は理論排除のまま未走行、m=6 は委嘱どおり未走行。
- **車線 2（crt-C2, 層 (0,5)）**: 12 個の Galois 半減色分布を全て式化・走行したが、
  各 closure ideal が 80 秒で TIMEOUT。**結果は `UNKNOWN_BOUNDED_C2_2`**。
  解ありとも層空とも主張しない。[C2-3] genus と [C2-4] order 9 は候補未得のため未到達。
- GHA final clean run **31597735465 = success**、head SHA
  **`9a3a0df7c625d66dcd4c24de2f9283e3352fba23`**。
  branch **`sol/k3-mainlines`** へ push 済み。master へは触れていない。

## 1. 宇宙・実装ファイル・設計判断

### 1.1 宇宙

- 係数体は (F_9=mathbf Q(zeta_{36}))。浮動小数判定なし。
- t3 は **m=4 のみ**。m=2 は非巡回性との矛盾により理論排除、m=6 への拡張なし。
- crt-C2 は指定どおり **層 ((s,f)=(0,5)) のみ**。f=4 以下への拡張なし。
- (u,c) 非接触、prereg の (b_9,a_9,d_9) は非計算。

### 1.2 実装

- `search/w9_k3_t3_m4_gha.py` — t3 producer
- `search/check_w9_k3_t3_m4.py` — import なし独立 checker
- `search/w9_k3_crt_c2_main_gha.py` — CRT-C2 bounded producer
- `search/check_w9_k3_crt_c2_main.py` — import なし receipt checker
- `.github/workflows/w9-p1-k3-crt-C2.yml` — 登録済み dispatch path を branch 上だけ本体 job に更新
- `ci/hard_timeout.py` — 前便の共通 wrapper をそのまま使用

### 1.3 hard-timeout / checkpoint

- t3: 外側 300 秒、実測 wrapper 0.541 秒、`timed_out=false`, child/wrapper rc=0。
- crt-C2: 外側 1500 秒、内側総予算 1400 秒、各 Singular ideal 80 秒。
  実測 wrapper 1021.160 秒、外側 `timed_out=false`, child/wrapper rc=2
  （rc=2 は producer の正規な UNKNOWN）。
- producer checkpoint と hard-timeout heartbeat は両 job の artifact に保存。

## 2. 車線 1 — [D-1]〜[D-4]

### 2.1 [D-1] exact Weierstrass 変換

原モデル

\[
 y^3-6\zeta_{12}sy+4is^2+4s=0
\]

に

\[
 X=iy,\qquad Y=2is
\]

を入れると、(F_9) 上で厳密に

\[
 \boxed{Y^2+3\zeta_3XY+2Y=X^3}
\]

となる。(Q_\infty=O, Q_0=(0,0))。接線 (Y=0) は (Q_0) に三重接触するので
([3]Q_0=O) を exact check。

単根側の座標は

\[
B_1=\left(\frac{2(1-i)}{\zeta_{12}},,2i\right),\qquad
B_2=\left(-\frac{2(1+i)}{\zeta_{12}},,-2i\right),
\]

で、曲線上かつ (partial f/partial y\ne0) を exact check。

指定の divisor-only 条件は

```text
B3+B4 ideal = (s^2-1, 3*y^2-6*zeta12*s)
individual_coordinates_used_by_solver = false
b34_handled_as_divisor = true
```

として実装した。

### 2.2 正本の平方根に関する監査所見

`w9_E_model_v1.md` §5 の「√(2ζ12) は (F_9) 外」は、そのままでは誤りである。
厳密恒等式

\[
\left(\frac{1+i}{\zeta_{12}}\right)^2=2\zeta_{12},\qquad
\left(\frac{1-i}{\zeta_{12}}\right)^2=-2\zeta_{12}
\]

を producer で確認した。両元は既に (mathbf Q(\zeta_{12})\subset F_9) にある。
ただし本実装は個点を一切使わず上記 divisor ideal のみを使うため、探索結果への影響はない。
この訂正は平方類の封印値を計算したものではない。

### 2.3 [D-2] RR と m=4 elimination

(Pi_0=-Q_0) を選び、(Pi_0) を原点へ移す座標を ((u,v)) とした。
complete-square 座標

\[
q=v+1+\frac{3\zeta_3}{2}u
\]

では

\[
q^2=S(u)=u^3-\frac{9h}{4}u^2+3(h-1)u+1,qquad h=\zeta_6, h^2-h+1=0.
\]

RR の raw 次元は `A=2, B=4`、raw 6、仕様の gauge 後 5。
(B(Q_0)=B(Q_\infty)=0) の2線形条件を課すと

\[
A=u(\alpha+u),\qquad B=u(\gamma+\delta u)
\]

（exact pole の top coefficient を幾何閉包上で 1 に正規化）。
固定単根対は (u=h/2)。残余偶因子条件の係数 ideal は

\[
\begin{aligned}
27\gamma^2+2h&=0,\\
2\alpha^3+27\gamma\delta-5&=0,\\
8\alpha^2+18\delta^2-11h+11&=0,\\
12\alpha+11h&=0,\\
h^2-h+1&=0.
\end{aligned}
\]

producer の Gröbner basis は `[1]`。checker はこの基底を読まず、上4式を手消去して
(h^2-h+1) での必要条件の剰余

```text
645911
```

（norm `417201019921`）を得て矛盾を独立確認した。

残余 even divisor の (F_9)-有理 square class の網羅性は (E[2](F_9)=0) で閉じた。
good prime 73, (zeta_{36}\mapsto25)（位数36）で 2-torsion cubic は

\[
u^3-2u^2+24u+1
\]

へ還元され、factor degrees `[3]`（既約）。従って (F_9)-有理 2-torsion は自明。

### 2.4 陽性対照（本番と同一経路）

同じ `equation_coefficients` builder と同じ Gröbner path に

```text
alpha=-4, beta=1, gamma=1, delta=1, branch_x=1
square cubic = u^3-11u^2+175u/4-27/4
```

を植えた。全残差 0、anchored ideal nonempty、`pass=true`。

### 2.5 [D-3]/[D-4] 結果

```text
m4_solution_exists_over_F9 = false
solution_count_over_F9 = 0
status = COMPLETE_EMPTY_F9_RATIONAL_M4_FIXED_PI0
m2_theoretically_excluded = true
m6_run = false
D-b genus = NOT_REACHED_NO_SOLUTION
D-c order 9 = NOT_REACHED_NO_SOLUTION
```

これは指定 (Pi_0=-Q_0) に対する m=4 の結果であり、T3-GAP-1 の停止上界や
他の極点選択に関する一般定理を主張しない。

## 3. 車線 2 — [C2-2]〜[C2-4]

### 3.1 起動 gate と順序

工房 run 31592557898 の保存 artifact を hash bind し、

- [C2-0] k=2 回帰 4 本 `all_pass=true`
- [C2-1] (w^{36}) 係数 0
- stage1 import-free checker `all_checks_true=true`

を fail-closed で再確認した。

producer cert の順序は逐語的に

```text
[mu3_CRT, D_equals_cE2, genus, order9]
```

である。C1 の高次6係数を厳密消去して自由次元10を再現した後、各色分布で
CRT 10式を先に生成し、その後だけ

\[
\mathcal D=cE(w)^2,\qquad \deg\mathcal D=34,quad \deg E=17
\]

の35係数式を追加した。次元5は予言値として記録するだけで、計算結果として仮定しない。

### 3.2 色分布宇宙

(f_1+f_\omega+f_{\omega^2}=5, f_\omega\ge f_{\omega^2}) の12分布を全て実行:

```text
(5,0,0) (4,1,0) (3,2,0) (3,1,1)
(2,3,0) (2,2,1) (1,4,0) (1,3,1)
(1,2,2) (0,5,0) (0,4,1) (0,3,2)
```

### 3.3 陽性対照（本番と同一平方経路）

同じ `square_equations` 関数と同じ Singular path へ

\[
y^3=w^5+w+1
\]

を投入。(h=w^5+w+1) は (mathbf Q) 上 squarefree、有限寄与10、無限寄与2、
RH genus 4。Singular は `NONUNIT`, GB size 6、`pass=true`。
従って「空を返し得る計器」が既知可解入力を同じ production code path で保持する。

### 3.4 bounded run 結果

good reduction prime 7, (omega\mapsto2)。有理係数は分母消去後に mod 7 へ事前還元。
12分布の closure ideal は全て

```text
status = UNKNOWN_CLOSURE_TIMEOUT
Singular status = TIMEOUT
per-system cap = 80 seconds
```

で、総実測 1020.508 秒。したがって

```text
status = UNKNOWN_BOUNDED_C2_2
layer_0_5_solution_exists_over_F9 = null
unknown_distribution_count = 12
C2_3_genus = NOT_REACHED_C2_2_UNKNOWN
C2_4_order_P0_minus_Pinf = NOT_REACHED_C2_2_UNKNOWN
```

である。**TIMEOUT は非存在証明ではない**。また正次元・有限解・解ありのいずれも
観測していないため、それらも主張しない。receipt checker は `all_checks_true=true`
（格付け `consistent bounded UNKNOWN receipt`）。

## 4. 封印検疫

両 cert に次をそのまま収録し、checker でも逐語照合した。

```text
name_collide_note = "K^(9) window instance, separate from the sealed K^(5) quantity, ruling 1007"
n5_value_computed = false
derivation_bridge_found = false
b34_handled_as_divisor = true
discriminant_square_class_field = "F9(E)^x/(F9(E)^x)^2 (function field square class)"
```

さらに `u_touched=false`, `c_touched=false`,
`preregistered_b9_a9_d9_computed=false`, `floating_point_used=false`。

## 5. GHA・commit・artifact

### 5.1 branch / commits

- branch: `sol/k3-mainlines`
- final implementation SHA executed by GHA:
  **`9a3a0df7c625d66dcd4c24de2f9283e3352fba23`**
- commit chain:
  - `a937da491d806c501e80b369ac963b434c7e493d` — 両 producer/checker + workflow 初版
  - `3448effd386987efd6165f09a85da673e195dfe8` — 登録済み workflow path へ配置
  - `480040db8151d9520145436ad89081590598059f` — Singular 前の係数事前還元修理
  - `9a3a0df7c625d66dcd4c24de2f9283e3352fba23` — B3/B4 divisor-only 記述を明確化

新規 workflow path は既定 branch 未登録だと dispatch 不能だったため、既に登録済みの
`.github/workflows/w9-p1-k3-crt-C2.yml` を **作業 branch 上だけ**更新した。
workflow file 変更は委嘱 §4 の GHA 本体実装に必要な範囲。master には未反映。

### 5.2 final clean run

- run id: **31597735465**
- URL: `https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/31597735465`
- head SHA: `9a3a0df7c625d66dcd4c24de2f9283e3352fba23`
- conclusion: **success**
- jobs: `t3-m4 = success`, `crt-c2-main = success`

### 5.3 artifact 名・SHA256

Artifact `w9-k3-t3-m4-31597735465`:

| file | SHA256 |
|---|---|
| `w9_k3_t3_m4_result.json` | `832e303835234699bd8b08264a7a78ce4660ce784ec2f4c4d636835ca8e179c2` |
| `w9_k3_t3_m4_check.json` | `8062f84de7f6cfc7697c5e3d18b9607ac2e4a4d59e64ad3efed07bb9941cba92` |
| `t3_m4_hard_timeout.json` | `12e1fcd3ecd0937e372a5ed4b5e376a2a23bbb4e82665f4e1f47ee1061bbf49e` |

Artifact `w9-k3-crt-c2-main-31597735465`:

| file | SHA256 |
|---|---|
| `w9_k3_crt_c2_main_result.json` | `b83e87df3e5eac9d74901ccb75f4060d9ab3cef47cef3384f9e91c8dc2723ce2` |
| `w9_k3_crt_c2_main_check.json` | `e06e34fa71cbf6b53709fa85a0e7caa556846c54dc74ab66fb09e803fdf9b4f8` |
| `crt_c2_hard_timeout.json` | `9220608b19e373f97f35e0efca0ece369704e857851b78f3e3e5482dd27dfbe4` |

## 6. 結果の意味（判定なし）

- t3 m=4 は指定した (F_9)-有理極点 (Pi_0=-Q_0) で空。
  これは m=6 以降や全極点に対する k=3 排除ではない。
- crt-C2 の ((0,5)) 層は計器実装・較正まで完了したが、80秒/分布では全12分布 UNKNOWN。
  よって層淘汰情報はまだ得ていない。
- いずれの車線でも平面モデル候補を得ていないため、R-2/R-3・(d_9) receipt・r 測定・
  不分岐 S へ渡す出口は今回発生していない。
- 次の数学判断は仕様 §9 の T3-GAP-1（m 上界）と T3-GAP-2（極点選択依存）、または
  CRT ideal の構造的簡約であり、本便では宇宙を広げていない。
