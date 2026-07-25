# Week 3 較正バッテリー manifest v1 — spec 射影(sealed 除去版)

本書は manifest v1 の spec 射影(sealed 除去済み)。実装はこのファイルだけを正とする。

2026-07-25 起草: Claude(数学者レイヤー・Opus)。司令塔 委嘱 04 の任務 2。**G-07 / P80 / P83 の実装。**

本書は **7 段 25200 B₃ 点の対象定義・fixture・期待値・UNKNOWN・cap を一元化した唯一の正本**である。
v2 §3.1–3.5・v3 §5.3–5.5 に散っていた情報はすべてここへ移した。**以後、実装は本書だけを参照する**(v2/v3 の該当節は履歴として残すが、実装が参照してはならない)。

- 数学的正本: `docs/week3-狩場計画_v4.md`(本書と食い違ったら **v4 が上位**。manifest を止めて差し戻す)。
- 監査根拠: `sol/sol_reply_07_audit.md`(F18/F19/F20・G-01〜G-09)・`sol/裁定_07_audit.md`。
- 状態札: **紙上相互監査**(W60)。**cross-checked でも verified でもない**。genuine は一切主張しない(W28)。

---

## 0. 開示規律(**実装ブラインド性の保護** — 本書を読む前に)

本書の各欄には **`disclosure` 属性**がある。**implementer へ渡すのは `spec` 射影だけ**である。

| disclosure | 内容 | 実装担当へ |
|---|---|---|
| **`spec`** | 対象定義・marked 生成元の像・宇宙数値(index / ord / charming set / derived / candidate total)・c の生死・evaluation mode・schema・cap・停止規則・**fixture(U-F・A-F)** | **渡す**(fixture は列挙前に検査する較正ゲート) |
| **`sealed`** | `gt_count`・staged count(`h10_fail` 等)・reduction の像/繊維/ker・`known_solutions`・`isolated`・`prop_C_formula` | **渡さない**。司令塔が **128-bit nonce + canonical JSON の SHA-256 を計算前 commit** し、結果が出てから開封(P67 六要件) |

> **司令塔の作業**: 本書から `sealed` 欄を除去した **`spec` 射影**を生成して implementer へ渡す。`sealed` 欄は nonce つきで封印する。**開封は byte 列で**(再 canonicalize しない)。

**canonicalization**: `gtsh-canon/v1` = UTF-8・キー辞書順・空白なし・整数は 10 進・置換は 1-indexed の巡回表記文字列(例 `"(1 3 2 4 5)"`)・群の元は各段の `element_encoding` に従う。`target_hash` は `target_definition` オブジェクトの canonical JSON の SHA-256(小文字 hex)。

---

## 1. 全体規則(**全段共通・違反は即停止**)

### 1.1 cap(P83 — 機械可読欄)

```json
{
  "cap": {
    "per_stage_wall_seconds": 600,
    "aggregate_wall_seconds": 1800,
    "max_rss_bytes": 2147483648,
    "gap_options": "-o 2g",
    "forbidden_constructions": ["full_cayley_table_squared"],
    "required_data_structures": ["BFS", "Int32Array"],
    "on_stage_timeout": "stage_result = UNKNOWN; halt",
    "on_aggregate_timeout": "all_remaining_stages = UNKNOWN; halt"
  }
}
```

- **W58(厳守)**: 七段それぞれが 600 秒以内でも、**集約 1800 秒を超えた時点で残りの段を UNKNOWN に倒す**。「あと 1 段だから」で延長しない。
- **二乗 Cayley 表の構築は禁止**(20736² は 8GB を確実に飛ばす)。BFS + Int32Array のみ。

### 1.2 停止規則(P84 — 厳守)

1. **各段の fixture が 1 つでも外れたら即停止**。次段へ進まず、その段と以降を **構成 UNKNOWN** とする(W36)。
2. **後段の既知値を使った補正を禁止**。「段 2b が 8 だったから段 3 も合うはず」という推論で fixture 不一致を通さない。
3. 停止時は `stop_reason`・`stage`・`fixture_id`・`observed`・`expected` を certificate に残す。
4. **cap 超過は結果を見てからの免除をしない**(W35)。

### 1.3 語彙(G-04 / W54 — 厳守)

| 出力名 | 意味 | 自動出力 |
|---|---|---|
| `frobenius_zero` | 命題 E4 の指標和 N(v_m) = 0 | **可** |
| `m_missing` | その (N, m) で同時 hexagon 解が無い(`intersection_size = 0`) | **可** |
| `fake_witness` | 粗い K の既存 shadow が細分 M へ持ち上がらない | **不可**(下記 4 項が揃った別 certificate に限る) |

**fake certificate の必須 4 項(F11)**: ①粗い K の具体的 shadow [m₀, f_K](完全列挙の個数証明つき)②m₀ の**全 lift m′ ∈ 𝒳_M** に対する欠落 ③補題 H3 の仮定リストまたは fiber product の直接解析 ④W34 の完全 reduction 像。**一つでも欠けたら `fake_witness` を書かない。**

### 1.4 certificate schema(全段共通)

```text
gtsh-cert/v2
  target_definition   {...}            # spec   (§2 の各段)
  target_hash         "<sha256>"       # spec
  s3_marking          {...}            # spec   (G-02・§1.5)
  universe            { pb3_index, b3_points, n_ord, charming_set,
                        derived_order, candidate_total }        # spec
  c_in_N              true|false       # spec
  evaluation_mode     "quotient_ok" | "word_level_required"     # spec
  triangle_marking    { applicable, exact_order_binv_a } | "not_applicable"  # spec (G-01)
  hexagon_free_certificate {           # 排他的 staged count (F16/W49)
      candidate_total, h10_fail, h11_fail, generation_fail,
      shadow_total }                   # shadow_total は導出値 (引き算が成り立つこと)
  generation_pass_count  <int>         # G-05: boolean 禁止・候補別に数える(出力は <int>・期待値欄は <int>|UNKNOWN — A1/A2 の期待は UNKNOWN)
  generation_detail   [ { m, f_hash, pass } ]                   # 候補別欄
  torsion_generation_agrees  true|false|UNKNOWN                 # 参考値のみ (W52)
  derived_product_check { ab_order_observed, product_expected, agree }  # W46
  frobenius_zero      [ m ... ]
  m_missing           [ m ... ]
  kernel_certificate  { kernel_scope: "PB3", pb3_kernel_index,
                        b3_kernel_index, justification: "2401 (3.32)" }
  reductions          [ { target, surjective, image_size, fibre, kernel_order,
                          kernel_structure } ]
  isolated            true|false|UNKNOWN
  runtime             { wall_seconds, max_rss_bytes }
  # 段固有の追加欄
  quotient_eval_diff_count  <int>       # evaluation_mode = word_level_required の段のみ
                                        # (語レベル評価と商内評価が食い違った候補数・観測値)
  layer_id                  <string>    # P75: P 完全な段で、指定 Delta_bar に対応する S3 層
```

- **排他的 staged count(F16/W49)**: `h10_fail` は最初に (3.10) で落ちた数、`h11_fail` は h10 通過後に (3.11) で落ちた数、`generation_fail` は両方通過後に生成性で落ちた数。
 **`shadow_total = candidate_total − h10_fail − h11_fail − generation_fail` が成り立たない証明書は不正**(独立に数えた重複可能な fail 数を入れる運用は禁止)。
- **G-05**: `generation_pass_count` は boolean ではない。一つの m に複数解があり得るため、**候補ごとの欄**(`generation_detail`)と**総数**を出す。
- **W52**: 生成判定の**正本は `⟨X^u, f⁻¹Y^u f⟩ = P`**。系 T2-B の `⟨g,r⟩ = Q` は参考値 `torsion_generation_agrees` に置くだけで、判定に使わない。

### 1.5 S₃ marking(**G-02** — 全段に必記)

標準 braid 射影は σ₁ ↦ (12)、σ₂ ↦ (23)、ゆえに **Δ ↦ (13)、δ_B ↦ (123)**。
本計画が用いる marking は **Δ ↦ (12)、δ_B ↦ (123)** であり、これは**標準射と (123) による同時共役**である(v4 §2.4・スクリプト確認済み)。PB₃ の核は同じなので数学は壊れないが、**「標準射に等しい」と「標準射と同時共役」を schema で区別する**(F4)。

```json
"s3_marking": {
  "convention": "Delta_delta",
  "Delta_image": "(1 2)",
  "deltaB_image": "(1 2 3)",
  "equals_standard": false,
  "simultaneous_conjugate_of_standard": true,
  "conjugator": "(1 2 3)"
}
```

### 1.6 記号衛生(W55 系・本書で導入)

- **δ_B := σ₁σ₂**(B₃ 側・Q で位数 3)と **d_G := τθ**(Guillot 側・Out(Q₈) で位数 2)を混同しない。本書では B₃ 側は必ず `deltaB` と書く。
- **段 A2 の C₅ 生成元は ζ と書く**(v3 は `t` と書いていたが、A₅ の t = (1 2 3) と衝突する)。**実装は ζ を使うこと。**

---

## 2. 七段(実装順)

**実装順(便 07 F18 合格・変更禁止)**: **1a → 1b → 2a → 2b → A1 → A2 → 3**
理由: 軽い既知較正 → 交わり → verbal 塔 → 新機構(Q7・完全群)を最小規模 → c 生存 → 最大規模。
**合計 B₃ 点数 = 48 + 1296 + 192 + 768 + 360 + 1800 + 20736 = 25200**(再検算一致)。

---

### 段 1a — `N_Q`(Q₈)

**(1) 対象定義**(disclosure: spec)
```json
{ "id": "1a", "name": "N_Q",
  "definition": "pi^{-1}( ker( F2 ->> Q8 ) )",
  "ambient": "B3", "quotient": "Q8",
  "element_encoding": "quaternion units {1,-1,i,-i,j,-j,k,-k}",
  "marked_images": { "x": "i", "y": "j", "c": "1" },
  "source": "week3-狩場計画_v2 §3.1" }
```
`s3_marking`: §1.5 の共通形。

**(2) 宇宙**(spec): `pb3_index = 8`、`b3_points = 48`、`n_ord = 4`、`charming_set = [0,1,2,3]`(N_ord = 4 は 2 冪ゆえ charming 条件は空虚)。
**(3) derived / candidate**(spec): `derived_order = 2`(= \|[Q₈,Q₈]\|)、`candidate_total = 8`(= 4 × 2)。
**(4) c と評価**(spec): `c_in_N = true`、`evaluation_mode = "quotient_ok"`。**語レベル評価も並走**させ一致を見る(安い)。
`triangle_marking`(spec): `{ "applicable": true, "exact_order_binv_a": 8 }`(= 2k、k = 4)。**G-01 の exact order 欄**。
**(5) 期待値**(**(SEALED — 司令塔保管。開封は照合後)***)
**(6) reduction**(**(SEALED — 司令塔保管。開封は照合後)***)
**(7) isolated**(**(SEALED — 司令塔保管。開封は照合後)***)
**(8) cap / 撤退**(spec): §1.1 共通。fixture 不一致で即停止(§1.2)。

---

### 段 1b — `M_Q = K⁽³⁾ ∩ N_Q`

**(1) 対象定義**(spec)
```json
{ "id": "1b", "name": "M_Q",
  "definition": "K^(3) cap N_Q",
  "quotient": "G3 x_{C2^2} Q8  (order 216)",
  "K3": { "psi3": "PB3 -> D3^3", "x": "(r,s,s)", "y": "(rs,r,rs)", "c": "(1,1,1)",
          "source": "2405.11725 (3.1)", "G3_order": 108, "K_ord": 6 },
  "marked_images": { "x": "((r,s,s), i)", "y": "((rs,r,rs), j)", "c": "(1,1)" } }
```
**(2) 宇宙**(spec): `pb3_index = 216`、`b3_points = 1296`、`n_ord = 12`(= lcm(6,4))、
`charming_set = [0,2,3,5,6,8,9,11] ⊂ Z/12`(条件 3 ∤ (2m+1) ⟺ m ≢ 1 mod 3、8 元)。
**(3) derived / candidate**(spec): `derived_order = 54`(= 27·2)、`candidate_total = 432`(= 8 × 54)。
**(4) c と評価**(spec): `c_in_N = true`、`evaluation_mode = "quotient_ok"`。
`triangle_marking`(spec): `{ "applicable": true, "exact_order_binv_a": 24 }`(= 2·12)。
**(5) 期待値**(**(SEALED — 司令塔保管。開封は照合後)***)
**(6) reduction**(**(SEALED — 司令塔保管。開封は照合後)***)
**(7) isolated**(**(SEALED — 司令塔保管。開封は照合後)***)
**(8) cap / 撤退**(spec): §1.1 共通。加えて **`derived_product_check` を必須**(W46 — H7′ 撤回後、fiber product の [Q,Q] は対象ごとに実測する)。期待: `ab_order_observed = 4`(\|Q_M^{ab}\|)⇒ \|[Q_M,Q_M]\| = 54。

---

### 段 2a — `N₂ = N_{P₂}`(P₂ = F₂/F₂⁴γ₃、位数 32)

**(1) 対象定義**(spec)
```json
{ "id": "2a", "name": "N_2",
  "definition": "pi^{-1}( F2^4 gamma_3(F2) )",
  "quotient": "P2 = F2 / F2^4 gamma_3, order 32",
  "presentation_verbal": "F2^4 gamma_3",
  "presentation_restricted": "D_3^(2)",
  "equality_scope": "p=2, n<=4, rank=2",
  "equality_proof": "計画v2 定理 T1a",
  "marked_images": { "x": "X", "y": "Y", "c": "1" } }
```
**(2) 宇宙**(spec): `pb3_index = 32`、`b3_points = 192`、`n_ord = 4`、`charming_set = [0,1,2,3]`。
**(3) derived / candidate**(spec): `derived_order = 2`(⟨w⟩、w = [X,Y])、`candidate_total = 8`。
**(4) c と評価**(spec): `c_in_N = true`、`evaluation_mode = "quotient_ok"`。
`triangle_marking`(spec): `{ "applicable": true, "exact_order_binv_a": 8 }`。
**(5) 期待値**(**(SEALED — 司令塔保管。開封は照合後)***)
**(6) reduction**(**(SEALED — 司令塔保管。開封は照合後)***)
**(7) isolated**(**(SEALED — 司令塔保管。開封は照合後)***)
**(8) cap / 撤退**(spec): §1.1 共通。fixture **U-F7(両表示の一致)**を必ず通す。

---

### 段 2b — `N₃ = N_{P₃}`(P₃ = F₂/F₂⁴γ₄、位数 128)

**(1) 対象定義**(spec)
```json
{ "id": "2b", "name": "N_3",
  "definition": "pi^{-1}( F2^4 gamma_4(F2) )",
  "quotient": "P3 = F2 / F2^4 gamma_4, order 128",
  "presentation_verbal": "F2^4 gamma_4",
  "presentation_restricted": "D_4^(2)",
  "equality_scope": "p=2, n<=4, rank=2",
  "equality_proof": "計画v2 定理 T1b (収集公式の原典照合は【GAP-E5】で未了)",
  "marked_images": { "x": "X", "y": "Y", "c": "1" },
  "derived_basis": { "w": "[X,Y]", "p": "[w,X]", "q": "[w,Y]" } }
```
**(2) 宇宙**(spec): `pb3_index = 128`、`b3_points = 768`、`n_ord = 4`、`charming_set = [0,1,2,3]`。
**(3) derived / candidate**(spec): `derived_order = 8`(⟨w,p,q⟩ ≅ C₂³)、`candidate_total = 32`。
**(4) c と評価**(spec): `c_in_N = true`、`evaluation_mode = "quotient_ok"`。
`triangle_marking`(spec): `{ "applicable": true, "exact_order_binv_a": 8 }`。
**(5) 期待値**(**(SEALED — 司令塔保管。開封は照合後)***)
**(6) reduction**(**(SEALED — 司令塔保管。開封は照合後)***)
**(7) isolated**(**(SEALED — 司令塔保管。開封は照合後)***)
**(8) cap / 撤退**(spec): §1.1 共通。
★ **本段は定理 H9 の最大の反証機会**。**R が非全射を返したら fake ではなく「私の証明か実装の誤り」**であり、その解明が最優先タスクになる(fail-closed の向きが逆)。

---

### 段 A1 — `N_A`(A₅)

**(1) 対象定義**(spec)
```json
{ "id": "A1", "name": "N_A",
  "definition": "pi^{-1}( ker( q: F2 ->> A5, x|->X, y|->Y ) )",
  "quotient": "A5",
  "element_encoding": "permutations of {1..5}, 1-indexed cycle strings",
  "marking": { "t": "(1 2 3)", "a": "(1 4 5)",
               "X": "a t^{-1} = (1 3 2 4 5)",
               "Y": "t X t^{-1} = (1 3 4 5 2)",
               "Z": "t^2 X t^{-2} = (1 4 5 3 2)",
               "s": "t X^3 = (1 4)(3 5)",
               "theta_P": "Ad(s)", "tau_P": "Ad(t)" },
  "marked_images": { "x": "X", "y": "Y", "c": "1" },
  "B3_quotient": "Q = B3/N_A = A5 x S3 (order 360), Delta_bar=(s,(1 2)), deltaB_bar=(t,(1 2 3))" }
```
**(2) 宇宙**(spec): `pb3_index = 60`、`b3_points = 360`、`n_ord = 5`、`charming_set = [0,1,3,4]`(𝒳 = {m ∈ ℤ/5 : gcd(2m+1,5) = 1})。
**(3) derived / candidate**(spec): `derived_order = 60`(A₅ 完全)、`candidate_total = 240`(= 4 × 60)。
**(4) c と評価**(spec): `c_in_N = true`、`evaluation_mode = "quotient_ok"`。
`triangle_marking`(spec): `{ "applicable": true, "exact_order_binv_a": 10 }`(= 2k、k = 5)。**系 T2-A′ の実例第 1 号**。私のスクリプトで ord_Q(σ̄₁) = 10 を確認済み。
**(5) 期待値**(**(SEALED — 司令塔保管。開封は照合後)***)
**(6) reduction**(**(SEALED — 司令塔保管。開封は照合後)***)
**(7) isolated**(**(SEALED — 司令塔保管。開封は照合後)***)
**(8) cap / 撤退**(spec): §1.1 共通。**P75**: P 完全ゆえ成層は S₃ 上の 3 層(命題 E6)。**どの layer が指定 Δ̄ に対応するかを certificate に残す**(`layer_id`)。

---

### 段 A2 — `M_{A,5} = N_A ∩ N₅`

**(1) 対象定義**(spec)
```json
{ "id": "A2", "name": "M_A5",
  "definition": "N_A cap N_5,  N_5 = ker( beta_5: B3 -> S3 x C5 )",
  "quotient": "A5 x C5 (order 300)",
  "C5_generator": "zeta",
  "marked_images": { "x": "(X, zeta^2)", "y": "(Y, zeta^2)", "c": "(1, zeta)" },
  "symbol_note": "C5 の生成元は zeta。v3 の t は A5 の (1 2 3) と衝突するため改名(§1.6)" }
```
**(2) 宇宙**(spec): `pb3_index = 300`、`b3_points = 1800`、`n_ord = 5`(= lcm(5,5,5))、`charming_set = [0,1,3,4]`。
**(3) derived / candidate**(spec): `derived_order = 60`(= \|[A₅×C₅, A₅×C₅]\| = \|A₅×1\|)、`candidate_total = 240`。
**(4) c と評価**(spec): **`c_in_N = false`**(c̄ = (1,ζ) は位数 5)、**`evaluation_mode = "word_level_required"`**。
> **実装注意(最重要・M₅ で判明した罠)**: **簡約 hexagon を商 P の中で評価してはならない。** θ/τ を**自由群の語レベル**で適用してから φ で評価すること(定義ノート §2)。**近道を使うと壊れる。本段はその罠の実地検査である。**
> **正規形の事前固定(falsifier 指摘 2026-07-26)**: 語レベル評価の規約は **M₅ 実装(凍結 tag v1.0-g1 系列・search/week3-M5-explorer.g)の語レベル θ/τ 規約と同一**とする — f の代表語は候補列挙で用いた生成語(自由簡約形・左から簡約)をそのまま使い、θ/τ を代表語へ文字ごとに適用してから φ で評価する。**列挙開始後の規約変更は禁止**(必要が生じたら停止して司令塔へ)。
`triangle_marking`(spec): **`"not_applicable"`**。理由: 定理 T2 / 系 T2-A′ は **c ∈ N を仮定する**。A2 では Δ̄² = c̄ が位数 5 なので B₃/M は PSL(2,ℤ) の商ではない(Δ̄ は位数 10、δ̄_B は位数 15)。**exact_order 欄を書かない。**
**(5) 期待値**(**(SEALED — 司令塔保管。開封は照合後)***)
**(6) reduction**(**(SEALED — 司令塔保管。開封は照合後)***)
補題 A2A1 の骨子: ①候補集合が一致([A₅×C₅ の導来] = A₅×1 ≅ A₅、𝒳 も同一)②A₅ 完全ゆえ f は [F₂,F₂] の語で代表でき **C₅ 成分は 1** ③C₅ 側の hexagon は可換商ゆえ自動(N₅ の m-full 性)④A₅ と C₅ に非自明な共通商が無い(A₅ 単純非可換・A₅^{ab} = 1)ので Goursat より生成性が全体へ。
> **W57(厳守)**: 両対象の isolated が UNKNOWN の間、この全単射を **「群同型」と呼ばない**。言えるのは「集合の全単射」と「gt_count の等号」まで。
**(7) isolated**(**(SEALED — 司令塔保管。開封は照合後)***)
**(8) cap / 撤退**(spec): §1.1 共通。**本段の fixture 不一致は「語レベル評価の実装バグ」か「補題 A2A1 の誤り」のいずれかを意味する。どちらでも情報量があるので、必ず停止して原因を切り分ける。**

---

### 段 3 — `M₃ = K⁽³⁾ ∩ N₃`(最大規模)

**(1) 対象定義**(spec)
```json
{ "id": "3", "name": "M_3",
  "definition": "K^(3) cap N_3",
  "quotient": "G3 x_{C2^2} P3 (order 3456)",
  "marked_images": { "x": "((r,s,s), X)", "y": "((rs,r,rs), Y)", "c": "(1,1)" } }
```
**(2) 宇宙**(spec): `pb3_index = 3456`、`b3_points = 20736`、`n_ord = 12`、`charming_set = [0,2,3,5,6,8,9,11]`。
**(3) derived / candidate**(spec): `derived_order = 216`(= 27·8)、`candidate_total = 1728`(= 8 × 216)。
根拠: Q^{ab} = ⟨(ā,X̄),(b̄,Ȳ)⟩ ≤ C₂²×(C₄×C₄) は (s,t) ↦ (sā+tb̄, sX̄+tȲ) が単射ゆえ ≅ C₄×C₄(位数 16)⇒ \|[Q,Q]\| = 3456/16 = 216。
**(4) c と評価**(spec): `c_in_N = true`、`evaluation_mode = "quotient_ok"`。
`triangle_marking`(spec): `{ "applicable": true, "exact_order_binv_a": 24 }`。
**(5) 期待値**(**(SEALED — 司令塔保管。開封は照合後)***)
**(6) reduction**(**(SEALED — 司令塔保管。開封は照合後)***)
**(7) isolated**(**(SEALED — 司令塔保管。開封は照合後)***)
**(8) cap / 撤退**(spec): §1.1 共通。**最大規模ゆえ二乗 Cayley 表禁止が最も効く段**。`derived_product_check` 必須(期待 `ab_order_observed = 16` ⇒ derived 216)。

---

## 3. fixture 一覧(**spec** — 1 つでも外れたら列挙へ進まない)

| # | 内容 | 期待値 |
|---|---|---|
| U-F1 | 各段の \|PB₃:·\| / \|B₃:·\| | §2 の各段(2)のとおり |
| U-F2 | 各段の ord / derived / candidate_total / charming_set の元 | §2 の各段(2)(3)のとおり |
| U-F3 | Q₈ 自己検査: i⁴=1, i²=j²=(ij)², ord(ij)=4, [i,j]=−1 | PASS |
| U-F4 | P₂ 自己検査: X⁴=Y⁴=(XY)⁴=1, [X,Y] 中心・位数 2, class 2 | PASS |
| U-F5 | P₃ 自己検査: exponent 4, class 3, γ₃ = ⟨p,q⟩ 中心, w²=p²=q²=1, \|P₃\|=128 | PASS |
| U-F6 | 塔の包含: **P₃ ↠ P₂** と **P₂ ↠ Q₈** を marked factor map で**別々に** | PASS |
| U-F7 | 両表示の一致(定理 T1): P₂/P₃ が verbal 表示と restricted 表示の**双方の**関係式を満たす | PASS |
| U-F8 | θ, τ が各 P に降りること(生成元の像で検査。**c ∈ N の段のみ**商評価が正当) | PASS |
| U-F9 | E_m := X^m Z^m Y^m の値表を各層で**独立計算し証明書へ出力**する(**期待値は本 fixture に書かない — sealed 側に封印**・開封時に司令塔が突合) | 出力欄の存在(値の事前指定なし) |
| **U-F10** | **exact order(G-01)**: c ∈ N の各段で `ord_Q(deltaB_bar^{-1} Delta_bar) = 2·n_ord` | 1a/2a/2b: 8、1b/3: 24、A1: **10** |
| **U-F11** | **S₃ marking(G-02)**: Δ̄ ↦ (12)、δ̄_B ↦ (123)、かつ**標準射との同時共役元が (123)** | PASS |
| **A-F1** | A₅ 自己検査: X,Y,Z の位数 5、XYZ = 1、s² = 1、sXs⁻¹ = Y、t³ = 1、τ: X→Y→Z→X | PASS |
| **A-F2** | ⟨X,Y⟩ = ⟨X,t⟩ = ⟨s,t⟩ = A₅(位数 60) | PASS |
| **A-F3** | B₃/N_A ≅ A₅×S₃: Δ̄²=δ̄_B³=1、braid 関係、σ̄₁²=(X,1)、σ̄₂²=(Y,1)、\|⟨Δ̄,δ̄_B⟩\| = 360 | PASS |
| **A-F4** | **段 A2 の評価方式**: 判定は**語レベル評価のみ**を採用。商内評価は**診断目的でのみ並走**させ、一致/不一致を候補ごとに記録する | 語レベル評価が採用され、`quotient_eval_diff_count` が記録されていること |
| **A-F5** | A2 の E_m を **語レベルで**構成し、C₅ 成分の hexagon が全 m ∈ 𝒳 で成立 | PASS(補題 A2A1 ③) |
| **A-F6** | A2 の derived: \|[A₅×C₅, A₅×C₅]\| = 60、射影 A₅×1 → A₅ が同型 | PASS |

**A-F4 の意味**: 段 A2 は「答えを当てる」段ではなく「**c ∉ M で近道が使えないことを実地で確認し、語レベル評価が正しく動くことを較正する**」段である。
**`quotient_eval_diff_count` は fixture ではなく観測値**である(私は「必ず食い違う」ことを証明していない — 特定の (m,f) で偶然一致することは排除できない)。ただし **diff_count = 0 が観測されたら報告事項**とし、罠が本当に無害なのか、それとも語レベル評価が実は商評価に退化しているのかを司令塔が切り分ける。

---

## 4. reduction 一覧(実装順に走らせる)

| # | reduction | 段の依存 | disclosure |
|---|---|---|---|
| R1 | M_Q → K⁽³⁾ | 1b 後 | 期待値 sealed |
| R2 | M_Q → N_Q | 1b 後(1a 済) | sealed |
| R3 | N₂ → N_Q | 2a 後(1a 済) | sealed |
| R4 | N₃ → N₂ | 2b 後(2a 済) | sealed |
| R5 | N₃ → N_Q | 2b 後(1a 済) | sealed |
| R6 | **M_{A,5} → N_A** | A2 後(A1 済) | sealed(**集合全単射**・W57) |
| R7 | M₃ → K⁽³⁾ | 3 後 | sealed |
| R8 | M₃ → N₃ | 3 後(2b 済) | sealed |

**W34 の 3 点セット(厳守)**: 非全射を主張する場合は (a) 欠落した m または shadow、(b) 全候補の**完全列挙の個数証明**、(c) reduction 像の完全計算 — を必ず**同時に**出す。**途中 cap なら UNKNOWN に倒す**(結果を見てからの免除はしない)。

**kernel 証明書**: 全段 **PB₃ 上**(補題 F + 2401 (3.32))。`kernel_scope = "PB3"` / `pb3_kernel_index` / `b3_kernel_index` / `justification = "2401 (3.32)"`。PB₃ 側の点数は 8 / 216 / 32 / 128 / 60 / 300 / 3456。

---

## 5. 本書に残る UNKNOWN と【GAP】

| # | 内容 | 状態 |
|---|---|---|
| 【GAP-M1】 | 段 1b・3・A1・A2 の **h10/h11/generation の排他的分配** | **私は導出していない**。invariant(和)のみ fixture。実装の観測値として記録し次版で紙上導出 |
| 【GAP-M2】 | 段 1b・3 の `ker R` の**群構造** | UNKNOWN(位数のみ確定)。**推測を書かない** |
| 【GAP-E11】 | A1・A2 の **isolated** | UNKNOWN。GT を「群」と呼ばない(W57) |
| 【GAP-E5】 | 段 2b の restricted 表示 D₄⁽²⁾ の**収集公式の原典照合** | 未了。`equality_scope` を p=2, n≤4, rank=2 に固定して運用 |
| 【GAP-E6】 | 本書の全数値 | **単系統**(私の node スクリプト)。**cross-checked でも verified でもない** |

**n ≥ 5 への外挿禁止(W44)**: 塔の verbal/restricted 一致は **p = 2, n ≤ 4, rank = 2** でのみ主張する。段 2a/2b の `equality_scope` 欄がその境界である。

---

## 6. 実装担当への一行

**本書の `spec` 射影だけを読み、期待値を推測しないこと。** fixture(§3)は列挙前の較正ゲートであり、**1 つでも外れたら即停止して報告する**(§1.2)。`gt_count` は司令塔が封印している — **合わせに行く対象ではない**。cap(§1.1)は延長交渉の対象ではない。
