# 増分 CV-9 判読 — R07 fixed-lambda cycle batch **v8**(rank 2090 → 2218・第 20 親 batch-parent-v7 の入場・11-key acceptance・fresh λ_2090 oracle・**親層定数の登録表からの実導出**・**二重 parse の解消**)

対象 run: **34701203323 / attempt 1**(success・head `f799fad95e2560cefda9a8ae8d7b73d575d348b0`・workflow `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v8.yml`・**P / C / 両 selftest / metadata の exit code 5/5 が 0**)
候補 artifact **10301413308**(413,467,399 B・zip entry **12,214**・mirror sha256 `cb63da6d…`)/ 診断 artifact **10301755032**
判読者: falsifier(非当事者・事後)。判読日 2026-09-13。
適用規律: **増分 CV-9**(裁定 2105 / 2110 / 2117・memory「CEGAR incremental CV-9」)— 規約表 diff を毎回・pin + TCB 集合が同一なら類似度は省略・**弱化検出が主目的**。
前回 CV-9 正本: `docs/notes/fixed_lambda_batch_v7_cv9_reading_v1.md`(裁定 2262・限定 7 条・F-v7-1〜7・裁定 2263 追補)。

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 7 条(§4)。新設 0・解消 0。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 7 条)・rank 2218 / gen 8923(state_head `0c6b08c424be0ceef6b735cb69b819426ed04daef9d35ef317080c44371b8a6c`・run 34701203323)を受理・`verified=false`・GRADE2 NOT_DECIDED(member / nonmember とも)・`full_A0=false`・A0 actual 0/1 不変。v7 の rank 2090 の直系後継として置き換える(合算ではない)。**

**a(128) = 128**(offered 128 / accepted 128 / dependent 0 / skipped 0・`partial=false`・`durable_tail=null`)。rank 2218 = 2090 + 128。消化率 128 / 36,107 = **0.3545 %**。

**弱化は 1 件も検出できなかった**(§5・機械全数)。v8 の前件 3 件はすべて満たされている。

| v8 前件 | 判定 | 根拠(要約) |
|---|---|---|
| **F-v7-4**(P が親行数 / 祖先数 / key 定数を literal でなく登録表から実導出) | **解消(機構として)** | P8 L953-1019 が実 registry(3,733,130 B / `3e1fe009…`)を読み、`current_count_inputs` の canonical sha を P 自身の literal `77f1b037…`(L937)で pin し、512 / 640 / 737 / 3,840 / 3,860 / 5 / 2,090 / 8,795 を導出。`current_derived_rho2`(L7443-7444)と `final_manifest_value`(L7544-7545)が**同一の源**を読むので 2251 の「片方だけ更新」は構造的に不可能。C8 は登録表を読まず独立和で同値に到達(L427-441)。**8/8 一致** |
| **F-v7-2**(5 層の二重 parse の解消と意味論保存) | **解消・意味論は保存(むしろ 1 条強化)** | 実測: 5 層すべて `parse_attempts = unique_documents = 128`・`repeated_input_bytes = 0`(v7 は 256/128・重複 64.7〜82.3 MB/層)。置換先 `reused_parent_reduction`(P8 L1063-1075)は**2 回目の物理読みも封検査も schema 検査も残し**、省いたのは `json.loads` のみ。加えて `canonical(retained_value) == raw` という v7 に無い制約を追加 |
| **第 20 親 batch-parent-v7 の 11-key acceptance 入場** | **入場済み** | acceptance は `batch_anchor_v7` を含むちょうど 11 key(P8 L6161 は登録表由来・C8 L967-970 は独立 literal 集合 + `CURRENT_ACCEPTANCE_KEY_COUNT = 6 + 5`)。親 = artifact 10173275037 / run 34523172734 / state_head `31b3d6db…`(= **受理された**方の v7 object) |
| **fresh λ_2090 の current / old 記録** | **正しい** | `selection/start.json.selection_lambda_sha256 = dd565268…`(v7 final λ)。`batch_observation.current` = **36,107** / 304 / 603、`old` = **36,000** / 110 / 212(= v7 正本 §3.1 の実測値と完全一致) |
| **第 7 selftest 群の件数** | **実 stdout と一致** | P `[30,10,6,7,8,8,12]`(計 81)・C `[28,9,6,7,8,10,14]`(計 82)。**私が stdout の `rejected_cases` を 1 件ずつ数えた**(裁定 2263 の erratum を踏まえ、literal からは数えていない) |

### 本判読の一次事実(新規)

1. **登録表は「宣言」から「導出源」になった。** v7 判読 F-v7-4 の指摘(表はあるが P/C はそれを読まない)は、v8 で P 側が実際に読む形へ改修された。しかも表の**内容は P の source literal で cryptographic に pin** されているので、driver が表を書き換えれば run は落ちる。私は artifact 同梱の registry を取得して canonical sha を再計算し、`77f1b037…` の一致を確認した。
2. **二系統の意味が一段変わった(重要)。** P の親層定数は今や**単一の源**から出る。P 内部の drift(2251 型)は不可能になった代わりに、**その値が正しいことの外部証拠は C の独立和ただ一つ**になった。C8 L426 のコメント「Independent C sums: the public P/driver registry is an external static cross-check only.」は正直な自己申告であり、私はこの構造を是とする — ただし**限定条項 3・5 と併せて読むこと**(§4)。
3. **二重 parse の除去で一意 parse バイトは 1 バイトも変わっていない。** 層別一意バイトは **129.778 / 141.432 / 153.185 / 164.938 MB** で **v7 判読 §7.3 の実測値と完全一致**、これに新 5 層目 **176.691 MB** が加わった。除去されたのは v7 が「repeated」と測った **64.730 / 70.546 / 76.412 / 82.277 MB**(+ 5 層目相当 88.143 MB)。
4. **C の ordered_reductions 要素数は v7 判読の厳密式 `128·R + 8,128` の予言を 5 層目で的中させた。** 実測 193,728 / 210,112 / 226,496 / 242,880 / **259,264**(= 128 × 1962 + 8,128)。
5. **λ の失敗数が 2 期連続で増加した。** 36,274 → 36,104 → 36,002 → 35,921 → 36,000 → **36,107**(今期 net **+107**)。v7 判読の「roster 枯渇までの外挿は定義不能」はさらに強化された。**Task 988 F4 の反例は依然排除されていない。**
6. **rank 2218 の sealed object は 1 つだけ。** v8 workflow の run は 34701203323 の 1 本のみ(`gh run list` で確認・conclusion success)。**F-v7-3 型(同一 rank に 2 つの seal)の再発は無い。**

---

## 1. (1) pin と TCB

### 1.1 便の pin の実測照合(私が `sha256sum` を実行)

| 対象 | bytes | sha256 | 判定 |
|---|---:|---|---|
| P8 `search/d972_r07_fixed_lambda_cycle_batch_v8.py` | 655,812 | `97f2523d29070bafb7e4295bfca7a975dad1be94daa17eb341f7a80e0bfd4e13` | **一致** |
| C8 `search/check_d972_r07_fixed_lambda_cycle_batch_v8.py` | 628,063 | `503365d539903df3e34d324a5ff26f65fb9245e36f55bd22230aa8c01cc1c35f` | **一致** |
| driver `search/d972_r07_fixed_lambda_cycle_batch_v8_workflow_driver_v1.py` | 8,592,553 | `1678973709f6c99ebc6fbd366535d73c47dc9885d5e9212c89a10c29dcb4a722` | **一致** |
| WF `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v8.yml` | 38,746 | `044b3635ac5cd17f58aa4b9dabc0d50cdb92d9a2368e4f62da3fcb2eff72b02f` | **一致** |

- **C8 が P8 を bytes + sha256 で pin している**: `CURRENT_PRODUCER_REGISTRATION = {"bytes":655812, "file":"search/d972_r07_fixed_lambda_cycle_batch_v8.py", "sha256":"97f2523d…"}`(照合は C8 L1026 `v8_registered_final_P8_opaque_full_pin`)。**上表の私の実測と完全一致。**
- **P8 が C8 を pin する経路は file 名のみ**(P8 L34 `C_FILE` / L1048-1051 `current_checker_entry_identity`)。v7 と同じ非対称で、**変化なし**(§5)。名前変異は selftest 第 7 群 `current-v8-checker-as-v7-repair2` で実際に拒否されている。

### 1.2 artifact 実バイトからの独立確認(私が HTTP Range で取得し、自分で sha256 を計算)

| entry | bytes | 私の sha256 | 意味 |
|---|---:|---|---|
| `audit-region-registry.json` | **3,733,130** | `3e1fe0092dbec2c3ae654c7d2712796b347ac4835a933b7619962616d68db15a` | 便の pin と一致。**F-v7-4 の導出源そのもの** |
| `output/HEAD` | 1,257 | `e81b16d2…` | = checker-result の `public_head_sha256` |
| `output/final/lambda.bin` | 12,096 | `63b796b6…` | = checker-result の `lambda_sha256`(新 λ_2218) |
| `output/final/manifest.json` | 1,925 | `6e771fd3…` | = checker-result の `final_manifest_sha256` |
| `output/parent-intake.json` | 10,012 | `69e75edc…` | = checker-result の `parent_intake_sha256` |
| `output/selection/start.json` | 1,115 | `8e401f0e…` | = checker-result の `selection_start_sha256` |

**公刊 5 ハッシュが artifact の実バイトと結ばれた。**(ZIP 全量 DL はしていない — 限定条項 7。)

### 1.3 in-run の pin 検証証拠

`driver-bootstrap-stdout.log`(2,123 B)に **22 行の `OK`**(v7 は 18 行)。repo 側 11 + `/home/runner/work/_temp/fixed-lambda-batch-v8/` 側 11。**v8 driver 自身が repo 側の検査対象に入っている**(`search/d972_r07_fixed_lambda_cycle_batch_v8_workflow_driver_v1.py: OK`)。
**【軽微・継続】現行 WF(`…-batch-v8.yml`)自身はこの 22 行に含まれない。** 同梱コピー `workflow.yml` は 38,746 B で repo の pin と bytes 一致(sha は §1.1 で repo 側を実測)。

### 1.4 TCB(v7 から**不変**)

- **算術 TCB**: `shared-tcb.json`(17,178 B)の `registered_shared_tcb.kernels` は **4 区間 = 共有カーネル 2 本 × P/C 各 1**(`vectorized_projection_chunk` / `sparse_adjoint`)。**v7 と同一集合**(本数の増加は無い)。`status = DECLARED_SHARED_TCB` / `verified = false` / `current_run_call_coverage = NOT_MEASURED` / `kernel_third_independence_claimed = false`。
- **交差辺(独立性)**: C8 の import は標準ライブラリ + numpy + `check_d972_r07_complete_oracle_cegar_continuation_v2` のみ(C8 L10-37)。**P8 を import する経路は無い。** P8 の import も v7 と同一集合(`importlib.util` は v7 から継続・用途は `task994_own_L` の読み込み P8 L1269-1271)。
- **C8 は current registry を読まない**: C8 の `add_argument` 全 11 個に `--audit-region-registry` は**無い**(P8 は L9600 で必須引数として持つ)。**導出の独立性は構造として保証されている。**
- **harness TCB は単著**(WF 38,746 B + driver 8,592,553 B)。Astra の別読票 2 本(1172 / 1177)は static public integration review であり、その自己申告も `STATIC_PUBLIC_INTEGRATION_NO_UNRESOLVED_FINDING_**RUNTIME_UNOBSERVED**`(`sol/luna_reply_1177_r07_v8_public_runtime_receiver_independent_review.md` L3)。**run 側の判読は本書が唯一**である。

### 1.5 凍結 envelope(宇宙・cap)

`cost-receipt.registration` / `run-receipt` の実値: `batch_size 128` / `max_batches 1` / `refill false` / `selection_policy CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX` / `partial_policy PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY` / producer `5,400 s・7,168 MiB` / checker `10,800 s・7,168 MiB`。**v7 と数値として完全同一 — caps・宇宙は 1 バイトも動いていない。**

---

## 2. (2) 規約表 diff(v7 → v8)

### 2.1 値の規約(私が両側の source と実出力から再計算)

| 量 | v7 | v8 | P8 の出所 | C8 の出所(**独立**) | 実出力 |
|---|---:|---:|---|---|---:|
| 親 role 数 | 19 | **20** | 登録表 `parent_roles` ≡ `ROLES`(L42・L972) | `PARENT_ROLES = (*V7_PARENT_ROLES, "batch-parent-v7")`(L52) | 20 |
| batch 親層数 n | 4 | **5** | `ROLES[15:]`(L988) | `CURRENT_PARENT_LAYER_COUNT = 5`(L433) | 5 |
| `previous_parent_batch_rows` | 384 | **512** | 登録表の層和(L995-996) | `CURRENT_PREVIOUS_BATCH_ROWS`(L427) | 512 |
| `total_parent_batch_rows` | 512 | **640** | 同上 | `CURRENT_TOTAL_BATCH_ROWS`(L428) | 640 |
| `target_derivation_parents` | 609 | **737** | `ancestry(97) + total`(L997) | `97 + 640`(L429-431) | 737 |
| acceptance top-level key 数 | 10 | **11** | 登録表 `current_exact_keys.acceptance`(L6161) | `6 + layer_count`(L438)+ 11 名の明示集合(L968) | 11 |
| `parent-intake` key 数 | 57 | **65** | 登録表(key 契約 L1183 経由) | `25 + 8 × 5`(L440) | **65** |
| `start` key 数 | 49 | **54** | 同上 | `34 + 5 × (5 − 1)`(L439) | 54 |
| `parent-layout` key 数 | 11 | **13** | 同上 | `acceptance + 2`(L441) | 13 |
| `candidate_phase_manifests_checked` | 3,072 | **3,840** | `6 × total`(L999) | `6 × 640`(L435) | 3,840 |
| `checkpoints_checked` | 3,088 | **3,860** | `5 × 4 + 3,840`(L1001) | `(4 + 6 × 128) × 5`(L436) | 3,860 |
| `native_pairing_rows_rechecked` | [1450…1962] | **[1450,1578,1706,1834,1962,2090]** | 累積(L1002-1005) | `CURRENT_NATIVE_PAIRING_ROWS`(L432) | 一致 |
| selftest 群 | 6 | **7** | `[30,10,6,7,8,8,12]`(L9512) | `[28,9,6,7,8]` + 10 + 14(L8058 / L8062 / L8065) | 一致(§6) |
| schema | `.v7` | `.v8` | — | — | 全公開 JSON |

**私は registry の `current_count_inputs` を artifact から取得し、上表の P 側 8 量(rank 2090 / gen 8795 / 512 / 640 / 737 / 3,840 / 3,860 / 5)を自分で再計算した。8/8 一致。** 表の canonical sha も `77f1b037…` = P8 L937 の literal と一致。

### 2.2 **最大の規約変更 = 「導出源」そのもの**(F-v7-4 の修理)

```
P8 L7443-7444  "anchor_previous_parent_batch_rows": current_count("previous_parent_batch_rows"),   # current_derived_rho2
P8 L7544-7545  "anchor_previous_parent_batch_rows": current_count("previous_parent_batch_rows"),   # final_manifest_value
```

v7 ではこの 2 箇所が**別々の literal** で、片方だけ更新したのが裁定 2251 の事故だった。v8 では両方が同一の `CURRENT_COUNTS` を読む。さらに `current_final_parent_counts`(P8 L1039-1046)が公開 HEAD 生成時に 4 量を一括再検査する。
**登録表が改竄されれば `current_registered_count_subobject_canonical_pin`(L962-963)で落ちる。表の全ファイル pin は `finish_current_count_registry`(L1033-1037)で run 中 2 回再確認される(L7150 / L7160)。**
親 intake の全量も同じ源から組まれる(P8 L5621-5669 が `current_count("initial_rank")` / `…("target_derivation_parents")` / `…("checkpoints_checked")` 等で構成)。それを C8 が独立和から組み直して `same_json` で突合する(C8 L2864-2924)。

### 2.3 公開 JSON key 集合

実出力で確認: `output/HEAD` 24 key・`result.json` 48・`checker-result.json` 50・`selection/start.json` 19・`parent-intake.json` 65 — **すべて登録表の `key_counts`(head 24 / result 48 / checker-result 50 / selection-start 19 / parent-intake 65)と一致**し、かつ C8 の独立和(§2.1)とも一致。
**【軽微・継続 = F-v7-7】** `run-receipt` の自己申告 key が今期も版番号入り(`selection_lambda1962_…` → **`selection_lambda2090_oracle_is_separate_from_new_final_lambda_oracle`**)。literal 名で読む消費者を毎 run 壊す設計は未修正。

---

## 3. (3) 群別 PASS(本走の検査群)

| 群 | 何を要求しているか | 結果 | 私の独立確認 |
|---|---|---|---|
| **A. 第 20 親の入場** | 11-key acceptance・`batch_anchor_v7` の記述子が親 artifact と一致・inventory(files 12,050 / dirs 3,613 / 1,444,771,837 B) | **PASS** | P8 の `BATCH_V7_INVENTORY_REGISTRATION`(L928-935)の **files 12,050 / file_bytes 1,444,771,837 は、v7 判読 §1.6 で私が v7 artifact の中央ディレクトリから独立に測った値と完全一致**。親 artifact 記述子(id 10173275037 / run 34523172734 / bytes 403,815,011 / head bf0b5c0b)も v7 判読と一致 |
| **B. 親層の累積則** | 128 / 512 / 640・祖先 97 → … → 737・pairing 6 点・layer coverage の分割和 | **PASS** | `parent-intake.json` の実バイトで確認: `previous 512 / total 640 / tdp 737 / pairings [1450,1578,1706,1834,1962,2090] / old_tdp 97`。C8 L2864-2924 が同じ値を独立和から構成して突合 |
| **C. fresh λ_2090 oracle** | 選定 λ = v7 final λ・state_head = 受理側・roster 128 本 | **PASS** | `selection/start.json`: `selection_lambda_sha256 dd565268…` / `state_head 31b3d6db…` / `previous_target 706a8d1d…`(= v6 final target)/ `target 2df80b53…`(= v7 final target)。**v7 判読 §2.1・§4.3 の値と一致** |
| **D. current 側 roster の独立再計算** | C が自前で残差選定をやり直す | **PASS** | `checker-stderr.log`: `{"chords": 54433, "failed": 36107, "phase": "fixed_lambda_all_residuals_selected", "selected": 128}` — **P の公刊 `failed_count 36107` と一致**。`tree.json` 実バイト: `residual_nonzero 36107 / first 304 / edge 603 / fit [0,1,1,1,0] / basis_chords [2,3,4,6,11]` |
| **E. old 側 oracle** | 36,000 / 110 / 212 が親の実体に結ばれる | **PASS(ただし再測ではない)** | P は source literal(P8 L7814-7817)、C は**親の保存済み `selection.json` から読んだ値**と literal の突合(C8 L4807-4809)+ `failed-indices.u32` が 4 × 36,000 B で先頭要素 110(C8 L4994-5000)。**どちらも λ_1962 から残差表を再計算してはいない**(→ F-v8-3・限定条項 2) |
| **F. 128 行の受理** | 128/128 INDEPENDENT・dependent 0・skipped 0 | **PASS** | `result.json`: `accepted_new_rows 128 / processed 128 / dependent 0 / skipped_after_linear [] / partial false`。`checker-result.json`: `accepted_rows_compared 128 / candidate_decisions_compared 128 / all_completed_payloads_and_json_compared true / public_final_compared true` |
| **G. 鎖と rank** | 2218 = 2090 + 128・gen 8923 | **PASS** | HEAD / result / checker-result / final-manifest の 4 文書で `rank 2218 / generation 8923 / state_head 0c6b08c4…` が一致(私が実バイトで突合) |
| **H. 予言の非空虚性** | `first_candidate` 5 条件 → INDEPENDENT | **PASS(6 回目)** | `matches_prediction: true` / `expected = observed = INDEPENDENT` / `raw_pairing 2` / `selection_scalar 2`。`independence_rate_predicted: false` の自己抑制は維持 |
| **I. UNKNOWN の置き場** | 未計算を 0 と読んでいないか | **PASS** | `new_lambda_oracle: null`・`failure_set_monotonicity_asserted: false`・`independence_rate_predicted: false`・`new_final_lambda_oracle_not_inferred: true`・`grade2_member/nonmember = NOT_DECIDED`・`full_A0 false`・`current_run_call_coverage = NOT_MEASURED`。**NONMEMBER 主張は一切していない** |
| **J. 計器(診断)** | 5 層の parse / ordered reduction | **PASS**(`observation_error: null` 5/5・`status COMPLETED`) | §5.3 |

---

## 4. 限定条項(**7 条**・v7 から新設 0・解消 0)

1. **射程 = rank 2090 → 2218 の 1 batch のみ。** rank 2218 の λ\* に対する oracle は**未計算**(`new_lambda_oracle = null`)。**NONMEMBER 主張ではない。**
2. **a(128) = 128 は roster 前置 128 本の観測**(batch パラメータ k の性質ではない)。消化率 128 / 36,107 = **0.3545 %**。**Task 988 F4 の反例は排除されていない。** 失敗数は **2 期連続で増加**(+79 → +107)したため、roster 枯渇までの見積りは依然として定義できない。**本条には「old λ_1962 の 36,000 は本 run で再測されていない(親の保存バイトと literal の突合まで)」を含める**(§3-E)。
3. **算術 TCB は共有カーネル 2 本を含む**(P/C 各 1 で計 4 区間)。`current_run_call_coverage = NOT_MEASURED`・`kernel_third_independence_claimed = false`。**第三独立性はこの 2 本に及ばない。** P1 相が候補時間の **71.6 %**(1,005.997 / 1,405.008)なので `vectorized_projection_chunk` は確実に load-bearing。
4. **旧 2,090 行の実バイトは私自身は未取得。** λ_new ⊥ 旧行 と ρ₂ の旧行部分は checker の再現に依存する。**ρ₂ は依然 DERIVED**(`mode=derived` / `original_rho2_directly_read=False`)。「選定 λ_2090 が旧 2,090 行を殺す」ことも本 run で私が再測したわけではない。
5. **harness TCB は単著**(WF 38,746 B + driver 8,592,553 B)。**加えて v8 では「P の親層定数の値」も harness 側の登録表に由来する**(表の内容は P の literal sha で固定されるが、**表を書いたのは driver 著者**)。この値を外部から縛るのは **C の独立和ただ一つ**である(§5.4)。
6. **checker の相別 timestamp は依然無い。** `cost-receipt.limitations` が自ら「C phase timestamps are absent; no C residual or P+C unmeasured subtotal is inferred」と宣言。可視化できたのは `input-preservation` 26.316 s = C 全体の **1.23 %** にとどまる(v7 は 5.25 %)。**F-k64-7 継続。**
7. **私は 413 MB の ZIP を全量ダウンロードしていない**(HTTP Range で必要 entry を個別取得)。ZIP 全体の sha は工房記録の mirror 値を採り、自分でバイト再計算していない。**私が sha256 を自分で計算したのは付録 A の 16 対象だけ。**

### 4.1 前回 7 条との対応

| v7 の条 | v8 での扱い |
|---|---|
| 1. 射程 1 batch | **継続**(条 1) |
| 2. a(k) の意味・F4 未排除 | **継続 + 悪化の継続**(条 2・失敗数が 2 期連続増加) |
| 3. 共有 kernel 2 本 NOT_MEASURED | **継続・集合も不変**(条 3) |
| 4. 旧行の実バイト未取得・ρ₂ DERIVED | **継続**(条 4) |
| 5. harness TCB 単著 | **継続 + 範囲拡大の明記**(条 5・登録表が値の源になったため) |
| 6. checker 段別 timestamp 無し | **継続 + 可視化率は低下**(条 6・5.25 % → 1.23 %。計器の対象が変わったため) |
| 7. ZIP 全量 DL せず | **継続**(条 7) |

**新設は無し。7 条 → 7 条。**

---

## 5. 弱化検出(本判読の主目的)

### 5.1 検査 1 — `require` ラベル集合の全数 diff(私の AST 実装)

| 側 | v7 のラベル | v8 のラベル | **削除** | 追加 | **出現回数が減ったラベル** |
|---|---:|---:|---:|---:|---:|
| P | 584 | **662** | **6** | 84 | **0** |
| C | 805 | **950** | **4** | 149 | **0** |

**削除 10 件はすべて版番号の改名であり、対応する v8 側の後継を 1 件ずつ特定した:**

| 側 | v7 で消えたラベル | v8 の後継 | 判定 |
|---|---|---|---|
| P | `acceptance_ten_plain_keys` | `acceptance_eleven_plain_keys`(L6161) | 改名 |
| P | `all609_accepted_parents_and_only_new_accepted_target_rows` | `all737_…`(L7432) | 改名 |
| P | `nineteen_registered_roots` | `twenty_registered_roots`(L6169) | 改名 |
| P | `production_requires_exact_nineteen_roots_acceptance_and_output` | `…_twenty_roots_…`(L9618) | 改名 |
| P | `selftest_exact_six_group_counts` | `selftest_exact_seven_group_counts`(L9513) | 改名 |
| P | `task1147_formal_binding_pending_static_draft` | `task1171_formal_binding_pending_static_draft`(L8108) | 改名 |
| C | `acceptance_exact_ten_plain_keys` | `acceptance_exact_eleven_plain_keys`(L970) | 改名 |
| C | `all_nineteen_roots_and_exact_acceptance` | `all_twenty_roots_and_exact_acceptance` | 改名 |
| C | `v7_formal_inventory_and_final_source_binding_pending` | `v8_formal_inventory_and_final_source_binding_pending`(L981) | 改名 |
| C | `v7_registered_final_P7_opaque_full_pin` | `v8_registered_final_P8_opaque_full_pin`(L1026) | 改名 |

**⇒ 消えた検査は 1 件も無い。**

### 5.2 検査 2 — 同名ラベルの**条件式**の diff(改名では隠せない弱化の検出)

v7 / v8 で同名かつ 1 回出現のラベル(P 440 / C 523)について、`require(...)` 呼び出しの source 断片を正規化して比較。**実差分は P 2 件・C 1 件のみ**、いずれも前進:

| 側 | ラベル | v7 | v8 | 判定 |
|---|---|---|---|---|
| P | `batch_v6_internal_prior_view_exact_nineteen_roles` | `== list(ROLES)` | `== list(HISTORICAL_V7_ROLES)` | **正しい前進**。`ROLES` が 20 になったため v6 の 19-role prior view は `ROLES[:19]`(L46)で固定する必要がある。`len == 19` の要求は残存 |
| P | `batch_observation_requires_measured_parent_premises` | `direct["rows"] == 1962` | `direct["rows"] == current_count("initial_rank")`(= 2090) | **F-v7-4 の適用**(literal → 登録表導出) |
| C | `batch_observation_independently_measured_parent_conditions` | `pairing["rows"] == FOURTH_BATCH_RANK` | `== FIFTH_BATCH_RANK` | 正しい前進 |

**⇒ 条件式の緩和は 1 件も無い。**

### 5.3 検査 3 — F-v7-2 の修理が検査を減らしていないか(逐語比較)

```
v7  reduction = old_batch_document(root, directory + "/reduction/reduction.json", "reduction")   # P7 L2077
      -> read_json(raw 読み + json.loads) -> check_seal(value) -> schema 一致

v8  reduction = reused_parent_reduction(root, directory + "/reduction/reduction.json",
                                        retained_reduction, BATCH_SCHEMA)                        # P8 L2399
      -> raw = safe_file(root, name).read_bytes()                        <- 2 回目の物理読みは残る
      -> require(raw == slot["raw"] and canonical(slot["value"]) == slot["raw"])   <- v7 に無い追加制約
      -> check_seal(value) -> schema 一致                                 <- v7 と同一
```

保持側 `retain_parent_reduction`(P8 L1053-1061)は (i) slot が空であること(= 1 行 1 オブジェクト)、(ii) 名前が `output/candidates/[0-9]{6}/reduction/reduction.json` に完全一致すること、(iii) 保持 raw の bytes / sha が**manifest 登録値と一致**すること、を要求する。`reused_parent_reduction` は使用後 `slot.clear()` する(1 回限り)。
**⇒ 省かれたのは `json.loads` だけ。2 回目の読み・封検査・schema 検査は残り、canonical 往復という制約が 1 条増えた。弱化ではない。**
実測(P stderr の `parser-bytes-timing.v1` 5 本・`reduction.json` と `physical-literal.json` の 2 種別): 5 層すべて `read_calls = parse_attempts = successful_parses = unique_documents = 128`・`repeated_parse_attempts = 0`・`repeated_input_bytes = 0`・`failed_parses = 0`・`changed_length_repeats = 0`・`observation_error = null`。

### 5.4 検査 4 — 「登録表が緩衝材になっていないか」

**登録表は P の検査を緩めていない**。理由 3 点を実バイトで確認した:

1. 表の内容は P の source literal `CURRENT_COUNT_INPUT_SHA256`(L937)で canonical sha 固定。**私が独立に再計算して一致**。
2. 表の形は `exact_keys` で 8 フィールド固定(L968-969)、層 role は `ROLES[15:]` と一致必須(L988)、`parent_roles == list(ROLES)` 必須(L972)。**表が P の source から独立に役者を増やすことはできない。**
3. 値そのものは **C の独立和(登録表を読まない経路)**と 8/8 一致し、実出力の key 数(11 / 65 / 54 / 13 / 24 / 48 / 50)とも一致。

**ただし残余リスクを明記する(限定条項 5)**: P 単独では値の正しさを担保できなくなった。**「P と C が一致した」の意味が、v7 までの「二つの literal 集合の一致」から「一つの pinned 表と一つの独立和の一致」に変わった。** 私の判定は「同等以上」だが、**この構造変化は裁定文に 1 行残すべき**である(F-v8-2)。

### 5.5 検査 5 — 空虚性(登録表 key 契約の否定例が無い)

**【要修正・F-v8-1】** `current_key_contract`(P8 L1026-1031)は `CURRENT_KEY_CONTRACT` が真のときだけ働き、これは `load_current_count_registry(..., production=...)`(L1018)で決まる。**本番は `production=True`(L8109)だが selftest は `production=False`(L9495)。** `require(CURRENT_REGISTRY_CONTEXT is None, "current_registry_single_process_binding")`(L956)で 1 プロセス 1 束縛に限定されるため、**selftest プロセスでは key 契約は最初から最後まで no-op** である。
⇒ **「key 集合が登録表と食い違えば落ちる」ことを示す否定例が P 側に 1 件も無い。** 本番 PASS は「契約が通った」ことしか示さない。C 側には独立の key 数検査(C8 L2924 / L5632)があり二重化されているので**事故の確率は低い**が、**P の契約自体は未試験**である。

---

## 6. selftest(**7 群**・件数は実 stdout から私が数えた)

| 側 | 群 | 件数(**stdout 実数**) | source literal | 登録表 | 判定 |
|---|---|---:|---:|---:|---|
| P | `k128-version-registration-and-types` | **30** | 30 | 30 | PASS |
| P | `k128-full-roster-cutoff-and-restoration` | **10** | 10 | 10 | PASS |
| P | `batch-parent1578-admission-and-projection` | **6** | 6 | 6 | PASS |
| P | `batch-parent1706-two-layer-admission` | **7** | 7 | 7 | PASS |
| P | `batch-parent1834-three-layer-admission` | **8** | 8 | 8 | PASS |
| P | `batch-parent1962-four-layer-admission` | **8** | 8 | 8 | PASS |
| P | **`batch-parent2090-five-layer-admission`** | **12** | 12 | 12 | PASS(**新設**) |
| C | `k128-version-registration-and-types` | **28** | 28 | 28 | PASS |
| C | `k128-full-roster-cutoff-and-restoration` | **9** | 9 | 9 | PASS |
| C | `batch-parent1578-admission-and-projection` | **6** | 6 | 6 | PASS |
| C | `batch-parent1706-two-layer-admission` | **7** | 7 | 7 | PASS |
| C | `batch-parent1834-three-layer-admission` | **8** | 8 | 8 | PASS |
| C | `batch-parent1962-four-layer-admission` | **10** | 10 | 10 | PASS |
| C | **`batch-parent2090-five-layer-admission`** | **14** | 14 | 14 | PASS(**新設**) |

- **三系一致**: 実 stdout の `rejected_cases` 実数 = source literal(P8 L9512 `[30,10,6,7,8,8,12]` / C8 L8058 `[28,9,6,7,8]` + L8062 `== 10` + L8065 `== 14`)= 登録表の `producer_expected_rejections` / `checker_expected_rejections`。**P 81 + C 82 = 163 拒否。**
- **新設第 7 群(P)**: `omit-v6-from-old19-projection` / `v7-local0-as-v6-local0` / `inherited609-as-complete737` / `omit-v7-theta0-ancestry` / `previous-target-from-v7-start-previous` / `packed-hash-as-v7-plain-target` / `v7-fixed-reference-as-colocated-payload` / `inventory-omitted-empty-directory` / `v7-header-with-v6-schema` / `v7-header-with-lambda1962` / **`current-previous512-as-native384`** / **`current-v8-checker-as-v7-repair2`**。
- **新設第 7 群(C)**: `omit-v6-from-native19-projection` / `alias-v7-local0-to-v6` / `…-v5` / `…-v4` / `…-v3` / `drop-zero-from-complete737` / `previous-from-v7-start-previous` / `lambda-source-is-completed-selection` / `registered-empty-directory-missing` / `uncomputed-oracle-is-zero` / `current-field-in-native57-intake` / **`current-previous-batch-count-is-stale`** / **`current-total-batch-count-is-stale`** / `current-schema-in-native57-intake`。
- **【評価・非空虚】太字の 5 件は今期の前件そのものの否定形である**: `current-previous512-as-native384`(P)と `current-previous/total-batch-count-is-stale`(C)は **2251 の失敗型(古い親行数の残留)を直接撃ち**、`current-v8-checker-as-v7-repair2`(P)は **2255 の失敗型(旧 path 名)を直接撃つ**。v7 で「登録表は宣言にすぎない」と指摘した点に対し、**修理と同時に否定例が入った**ことを確認した。
- `inherited609-as-complete737` / `drop-zero-from-complete737` は祖先数の代用と θ=0 記録の脱落を、`inventory-omitted-empty-directory` / `registered-empty-directory-missing` は空 dir の脱落を撃つ(v7 と同型の継続)。
- **fixture gate**: P/C とも `new_mathematical_selftest_groups: 2` + `new_parent_metadata_selftest_groups: **5**` = 7 群。`parent2090_fixture_gate` の受領証が P(18,285 B)/ C(18,355 B)の双方に実在。
- **metadata canary**: `metadata-gate.json` の `metadata_regression_cases: 16`・exit 0・`run-receipt.metadata_regression_cases_registered: 16`。**v7 と同数・継続。**
- **in-run 実行の証拠**: `producer-selftest-exit-code.txt` / `checker-selftest-exit-code.txt` とも **0**、selftest stdout の `schema` は `d972.r07.fixed-lambda-cycle-batch.v8.selftest`。公開 selftest 版の分岐は今期も生じていない。

---

## 7. 格付け提案

**CV-9 = 同一対象(SAME OBJECT)・限定 7 条 → 工房格付け案: checker PASS / cross-checked(限定 7 条)・rank 2218 / gen 8923(state_head `0c6b08c424be0ceef6b735cb69b819426ed04daef9d35ef317080c44371b8a6c`・run 34701203323)を受理・`verified=false`・GRADE2 NOT_DECIDED・`full_A0=false`・A0 actual 0/1 不変。v7 の rank 2090 の直系後継として置き換える(合算ではない)。**

**司令塔への一行**: v8 の 3 前件はすべて満たされた — **F-v7-4 は機構として解消**(P は実 registry 3,733,130 B / `3e1fe009…` を読み、その `current_count_inputs` の canonical sha を自分の literal `77f1b037…` で pin して 512 / 640 / 737 / 3,840 / 3,860 / 5 / 2,090 / 8,795 を導出。`current_derived_rho2` と `final_manifest_value` が同一の源を読むので 2251 型の内部 drift は不可能。**C は登録表を読まず独立和で同じ 8 量に到達**し、実出力の key 数 11 / 65 / 54 / 13 / 24 / 48 / 50 まで一致)、**F-v7-2 は解消**(5 層すべてで `parse_attempts = unique = 128`・`repeated_input_bytes = 0`。置換先は 2 回目の物理読みと封検査を残し `json.loads` だけを省き、`canonical(value) == raw` を**追加**した = 弱化ではなく 1 条強化。一意 parse バイトは v7 実測と層ごとに完全一致 129.778 / 141.432 / 153.185 / 164.938 MB + 新層 176.691 MB)、**第 20 親 batch-parent-v7 は 11-key acceptance で入場**(inventory files 12,050 / 1,444,771,837 B は v7 判読で私が独立に測った値と一致・親は**受理側** `31b3d6db…`)。**fresh λ_2090 は current 36,107 / old 36,000 として正しく記録**され、**current 側は C が `select_all_residuals` で独立に 36,107 / selected 128 を再計算**、old 側(36,000 / 110 / 212)は v7 正本 §3.1 の実測値と一致する。**第 7 群は P [30,10,6,7,8,8,12] / C [28,9,6,7,8,10,14] が実 stdout・source literal・登録表の三系で一致**(私は stdout から 1 件ずつ数えた)。**弱化は機械全数で 0 件**(require ラベル削除 10 件はすべて版番号改名・条件式の実差分 3 件はすべて前進・出現回数の減少 0)。残す宿題は **F-v8-1(P の登録表 key 契約が selftest で常時無効 = 否定例ゼロ)** と、**二系統の意味が「二つの literal 集合の一致」から「一つの pinned 表と一つの独立和の一致」へ変わった**という構造変化の明記。

### 7.1 診断(**gate ではない** — 裁定 2225 / memory「cost-extrapolation-needs-math-review」)

- 実測: producer **1,831.695 s**(cap 5,400 の 33.9 %)/ checker **2,132.366 s**(cap 10,800 の 19.7 %)/ P+C **3,964.061 s**。P 残差 **413.376 s**(v7 は 369.370)。
- 層あたり P 残差増分: +42.823 / +45.042 / +49.207 / +42.336 / **+44.006**。**v7 判読 F-v7-1 の 7 点線形モデル `26.422 + 1.2642k + 45.4855n` の (k,n) = (128,5) 予測 415.67 に対し観測 413.376(−2.29 s)。8 点目でも線形で足り、「層費用は加速する」は依然棄却されたまま。**
- 候補相の内訳: p1 **1,005.997 s(71.6 %)**/ primal 305.828 / reduction 40.449 / source 30.131 / raw 13.081 / B 9.523。**律速は 8 run 連続で P1 補正相。**
- 二重 parse の除去で層あたり **64.7〜88.1 MB** の再 parse が消えたが、**P 残差の層あたり増分はほぼ不変**(+42.3 → +44.0)。⇒ **parse は層費用の主因ではない**という v7 の読み(R 比例項の 7 割強が未帰属)は、**今回の除去実験によって因果的に裏づけられた**。v7 では相関でしか言えなかった点である。

### 7.2 v9 の前件として裁定に載せるべき所見 F-v8-*

| 札 | タグ | 内容 |
|---|---|---|
| **F-v8-1** | **【要修正・空虚性】** | **P の登録表 key 契約 `current_key_contract` は selftest で常時無効**(P8 L1018 / L9495 が `production=False`・L956 で 1 プロセス 1 束縛)。**「key 集合が登録表と食い違えば落ちる」否定例が P 側に 1 件も無い。** C 側の独立 key 数検査(C8 L2924 / L5632)で二重化はされているが、v9 では第 8 群に key 契約の否定例を 1 件足すか、`production=True` の小 fixture を 1 本通すこと |
| **F-v8-2** | 【要修正・記帳】 | **二系統一致の意味が変わった**: P の親層定数は単一の pinned 表から出るため、**値の外部証拠は C の独立和ただ一つ**。裁定文と限定条項 5 に「harness 著者が書いた表が P の値の源である」ことを明記すること(§5.4) |
| **F-v8-3** | 【要修正・計器】 | **old λ 側(36,000 / 110 / 212)は本 run で再測されていない**(P は source literal L7814-7817、C は親の保存 `selection.json` との突合 L4807-4809)。current 側だけが独立再計算。「current と old の差」を一次データとして使い続けるなら、**同一 run 内で λ_1962 の残差表を再計算する計器**を足すか、使わないと決めること |
| **F-v8-4** | 【一次データ・射程】 | **失敗数が 2 期連続で増加**(35,921 → 36,000 → **36,107**・今期 net **+107**)。6 世代の推移 36,274 / 36,104 / 36,002 / 35,921 / 36,000 / 36,107。**roster 単調減少の前提は完全に消えた**。残工程見積りを roster サイズで語る記述は台帳・地図から外すこと |
| **F-v8-5** | 【軽微・継続(F-v7-7)】 | `run-receipt` の自己申告 key が今期も版番号入り(`selection_lambda2090_…`)。literal 名で読む消費者を毎 run 壊す |
| **F-v8-6** | 【軽微・継続】 | `driver-bootstrap-stdout.log` の in-run pin は 22 行に増えた(v7 は 18)が、**現行 WF 自身は依然含まれない**。同梱 `workflow.yml`(38,746 B)と repo の一致は外部照合(§1.1 / §1.3) |
| **F-v8-7** | 【軽微】 | P8 の `BATCH_V7_PARENT_FACTS`(L901-916)は、**親の公刊値**(rank 2090 / gen 8795 / state_head / λ / target / 祖先 737)と**現世代の累積行数**(previous 512 / total 640)を同じ辞書に同居させている。命名から 512/640 を親 v7 の公刊値(実際は 384/512)と誤読しうる。**事故には至っていない**(C8 L4816 が acceptance の当該ブロックを自分の独立和と `same_json` で突合するため drift は検出される)が、v9 で名前を分けること |
| **F-v7-1** | 【診断・継続】 | 8 点目でも線形で足りる(§7.1)。「非線形に悪化するから急げ」という根拠は今期も無い |
| **F-v7-3** | 【今期は非該当】 | v8 workflow の run は 34701203323 の 1 本のみ。**rank 2218 の sealed object は 1 つ**。ただし rank の引用に state_head を併記する運用は継続すること |
| **F-v7-5 / F-v7-6** | 【軽微・継続】 | 陳腐化コメント(C8 L323-324 に同型が残存: 「Current P8 stays guard-closed below until root supplies its actual final opaque pin.」の直下 L1026 が実際に束縛している)・計器の identity 依存(P8 L2245-2246 のエラーメッセージ literal を鍵にした型検査開始検出・L6021 の path literal 置換)。**いずれも自己検知型で今期は `observation_error: null` 5/5** |
| **F-v5-2 / F-v5-3 / F-v5-4 / F-k64-7** | 【軽微・継続】 | fixture 被覆窓・envelope 履歴(今期は失敗 run 自体が無い)・`basis-tau.u8` の二重索引(`basis_chords [2,3,4,6,11]` は今期も受領証に規約が未明示)・C の相別 timestamp 不在 |

---

## 付録 A. 私自身が sha256 を計算した対象

| 対象 | bytes | sha256 |
|---|---:|---|
| `search/d972_r07_fixed_lambda_cycle_batch_v8.py` | 655,812 | `97f2523d29070bafb7e4295bfca7a975dad1be94daa17eb341f7a80e0bfd4e13` |
| `search/check_d972_r07_fixed_lambda_cycle_batch_v8.py` | 628,063 | `503365d539903df3e34d324a5ff26f65fb9245e36f55bd22230aa8c01cc1c35f` |
| `search/d972_r07_fixed_lambda_cycle_batch_v8_workflow_driver_v1.py` | 8,592,553 | `1678973709f6c99ebc6fbd366535d73c47dc9885d5e9212c89a10c29dcb4a722` |
| `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v8.yml` | 38,746 | `044b3635ac5cd17f58aa4b9dabc0d50cdb92d9a2368e4f62da3fcb2eff72b02f` |
| artifact `audit-region-registry.json` | 3,733,130 | `3e1fe0092dbec2c3ae654c7d2712796b347ac4835a933b7619962616d68db15a` |
| その canonical `new_source_audit.current_count_inputs` | — | `77f1b03739ac7786c113bb0242273fe587b6e78ff3cdf87935916a3652f0b1a2`(= P8 L937 の literal) |
| artifact `output/HEAD` | 1,257 | `e81b16d26b2af94a7463bd16af756d43c51786c4445f53c59ad16f36068429cb` |
| artifact `output/final/lambda.bin` | 12,096 | `63b796b6a1d03fce798ccd5b81f2ee4720012b15def7227b5075e40245968b67` |
| artifact `output/final/manifest.json` | 1,925 | `6e771fd32c2c7838cb745f138f58f15fa6c27167c6470a4005fe2efd7420d79e` |
| artifact `output/parent-intake.json` | 10,012 | `69e75edca901f7450e31c78ce9f83d9f0577d4c98f5aea43d3b8ab3078ab048a` |
| artifact `output/selection/start.json` | 1,115 | `8e401f0e60dec78f8a3b73ce378de0f8b09fdf40db9a6ebe3e32151905302c14` |
| artifact `output/selection/tree/tree.json` | 430 | `cd024262d6ed64eb9da5c55b421dec2d8901643814a5f7e736c417e86b60fa6e` |
| artifact `producer-stderr.log` | 727,078 | `bba3238f109519275283dab51871a16175064d52575630783fcd4b8a9ec9e4fb` |
| artifact `checker-stderr.log` | 1,261,463 | `1e2b670db8d3e1e5afccf956c8c119a03f5fd98895771b5c1f36ef2238e35877` |
| artifact `shared-tcb.json` | 17,178 | `6124abcdc881d2791c2899383c0a82179cce23fdcbac4acdef9a98f8f8d02a92` |
| artifact `run-receipt.json` | 842,335 | `caac0d1012ea7bed8c5ec344f90dea07a92727eacc6ae0e2b3404ee43fc20d60` |

## 付録 B. 判読者の限界(正直な申告)

- 旧 2,090 行の実バイトを取得していないので、λ_new ⊥ 旧行 と ρ₂ 恒等式の旧行部分は checker の再現に依存している(限定条項 4)。
- **本判読は増分規律に従い、v7 判読が行った「128 行の階段形・λ の後退代入 48,384 座標・target 恒等式 128 段・rolling 鎖 128/128」の全数再計算を今期は行っていない。** 本書が実測で閉じたのは付録 A の 16 対象・登録表の 8 量・計器 5 層・selftest 163 件・`require` ラベル diff(全数)・条件式 diff(同名単一ラベル全数)である。**したがって「算術が正しい」ことの本期の根拠は C の PASS と §3 の群別確認であり、私の再計算ではない。**
- old λ_1962 の残差表を私自身は再計算していない(F-v8-3)。
- Astra の別読票(1172 / 1177)は static review であり、その自己申告どおり runtime は未観測。私はこれを根拠として使っていない。
- `sparse_adjoint` / `vectorized_projection_chunk` が本 run の実行経路で呼ばれた行は特定していない。
- Release ミラーは確認していない(工房記録に依拠)。
- **この観点では仕様の齟齬(別対象)も検査の弱化も見つけられなかった — 保証ではない。**

---

**裁定 2277(司令塔・2026-09-13)格付け**: 本判読(42,710 B/3af4d98a…・工房 sha256sum で pin)を正本として採用。CV-9 = 同一対象・限定 7 条(新設 0・解消 0)→ **rank 2218/gen 8923(state_head 0c6b08c4…・run 34701203323/1)を cross-checked(限定 7 条)で受理**・v7 の 2090 の直系後継として置換・verified=false・grade-2 NOT_DECIDED・full_A0=false。限定 5 の意味変化(二系統一致 = 一つの pinned 登録表と一つの独立和の一致)を裁定文に明記(F-v8-2)。F-v8-1(登録表 key 契約の selftest 空虚性)・F-v8-3(old λ の同 run 再測計器)・F-v8-4(失敗数 2 期連続増 → 単調減少の前提消滅)・F-v8-5/6/7 を v9 の前件・所見として台帳 2277 に登録。
