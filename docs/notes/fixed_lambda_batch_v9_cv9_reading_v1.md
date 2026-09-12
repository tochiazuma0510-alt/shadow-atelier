# 増分 CV-9 判読 — R07 fixed-lambda cycle batch **v9 repair-v2**(rank 2218 → 2346・第 21 親 batch-parent-v8 の入場・12-key acceptance・fresh λ_2218 oracle・**登録表の prefix view による歴史ブロックの再指向**・**P 側 production key 契約の否定例の新設**・**native-metadata 操作別計器の追加**)

対象 run: **34717506638 / attempt 1**(success・head `6b105348b2372a6b59de29904912172b5720e8ec`・workflow `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v9-repair-v2.yml`・**P / C / 両 selftest / metadata / driver-bootstrap の exit code 6/6 が 0**)
候補 artifact **10306226977**(429,844,909 B・zip entry **12,348**・mirror sha256 `94da553a…`)/ 診断 artifact **10306192099**
系譜: 初回 **34714029903**(failure・裁定 2283)→ repair-v1 **34714930484**(failure・裁定 2286)→ **repair-v2 34717506638(success)**
判読者: falsifier(非当事者・事後)。判読日 2026-09-13。
適用規律: **増分 CV-9**(裁定 2105 / 2110 / 2117・memory「CEGAR incremental CV-9」)— 規約表 diff を毎回・pin + TCB 集合が同一なら類似度は省略・**弱化検出が主目的**。
前回 CV-9 正本: `docs/notes/fixed_lambda_batch_v8_cv9_reading_v1.md`(裁定 2277・限定 7 条・F-v8-1〜7・裁定 2279 追補)。**本書は v8 正本を一切編集していない。**

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 8 条(§4・新設 1・解消 0)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 8 条)・rank 2346 / gen 9051(state_head `fc1ac4d9057ef401de1740954cefa4c45d48ccfdbcffddfb59c8f5f8cae566ff`・run 34717506638)を受理・`verified=false`・GRADE2 NOT_DECIDED(member / nonmember とも)・`full_A0=false`・A0 actual 0/1 不変。v8 の rank 2218 の直系後継として置き換える(合算ではない)。**

**a(128) = 128**(offered 128 / accepted 128 / dependent 0 / skipped 0・`partial=false`・`durable_tail=null`)。rank 2346 = 2218 + 128。消化率 128 / 35,647 = **0.3591 %**。

**検査の弱化は 1 件も検出できなかった**(§5・機械全数)。**逆置換検問(裁定 2283 (3) / 2286 (3))も通過** — 3 版の全差分は「識別子 literal の整合」「why 文字列の分割」「計時区間の登録補完」「著者側 wire 文書の差し替え」に限られ、検査の削除・条件の緩和は 0 件(§5.3)。

| v9 の前件 | 判定 | 根拠(要約) |
|---|---|---|
| **F-v8-1**(P の登録表 key 契約の selftest が空虚) | **解消(非空虚な否定例が実通過)** | P 第 8 群 = **`production-registered-key-contract`**(1 件 `extra-production-progress-head-key`)。P9r2 L10898-10981 が**別プロセスの子**を起こし `production=True` で実登録表を束縛(L10908-10909 `CURRENT_KEY_CONTRACT is True` を要求)、**正例が正常に読めること**(L10929-10930)と**両者の封が有効であること**(L10937-10938)を先に確立したうえで、余分な key 1 個の負例が `current_registered_exact_keys:progress-head` で**確かに落ちる**ことを要求(L10945-10951)。落ちなければ `production_key_canary_did_not_reject` を投げる。**分離条件つきの非空虚な否定例**である |
| **F-v8-3**(old λ の同 run 再測) | **方式は 2278 どおり(再測はしない)・ただし受領証に明示条項なし** | P L6212 と C L6241 はともに**親の保存 `selection.json` / 保存 `failed-indices.u32`(4 × 36,107 B・先頭 304)と literal `{36107,304,603}` の突合**にとどまる(C L6436-6438)。current 側(35,647)だけが C の独立再計算。receipt 側の自己抑制は `failure_set_monotonicity_asserted:false` / `independence_rate_predicted:false` / `new_final_lambda_oracle_not_inferred:true` の 3 つで、**「old は本 run で再測していない」と名指しする field は無い**(→ F-v9-4) |
| **F-v9-1**(P WORKFLOW / C CHECKER_WORKFLOW / WF path の identity) | **一致(静的・実行時とも)** | P9r2 L8617 `WORKFLOW` = C9r2 L56 `CHECKER_WORKFLOW` = repo の WF path = `runtime-observation.json` / `run-receipt.launch` / `shared-tcb.launch` / `parent-timing-receipt.launch` の `workflow` = **`.github/workflows/d972-r07-fixed-lambda-cycle-batch-v9-repair-v2.yml`**。WF 自身も L10/11/12・L174/177/183 で 3 ファイルを repair-v2 名で参照 |
| **第 21 親 batch-parent-v8 の 12-key acceptance 入場** | **入場済み** | acceptance は `batch_anchor_v8` を含むちょうど 12 key(C9r2 L1495-1496 が明示集合 + `V9_CURRENT_ACCEPTANCE_KEY_COUNT = 6 + 6`)。親 = artifact **10301413308** / run **34701203323** / state_head **`0c6b08c4…`** / λ `63b796b6…` / bytes 413,467,399 / mirror `cb63da6d…` = **v8 正本が受理した object そのもの**。`run-receipt.accepted_artifacts` は **21 role** |
| **fresh λ_2218 の current / old 記録** | **正しい** | `selection/start.json.selection_lambda_sha256 = 63b796b6…`(= v8 final λ)・`state_head 0c6b08c4…`・`previous_target 2df80b53…`(= v7 final target)・`target e1b34dfa…`(= v8 final target)。`batch_observation.current` = **35,647** / 489 / 242、`old` = **36,107** / 603 / 304(= v8 正本 §3.1 の実測値と完全一致) |
| **4 計器が判定経路に触れていない(telemetry only)** | **触れていない(source と受領証の両方で確認)** | §5.4 |
| **selftest 群の群別拒否件数** | **実 stdout と一致(三系)** | P `[30,10,6,7,8,8,12,1]`(計 82)・C `[28,9,6,7,8,10,14,15]`(計 97)。**私が stdout の `rejected_cases` を 1 件ずつ数えた**(§6) |

### 本判読の一次事実(新規)

1. **P の歴史ブロックが「同一 pin 源の prefix view」へ移った。** v8 では v7 期のブロックが `current_count(...)` を読んでいた(当時はそれが現行値だったので偶然一致していた)。v9 では同じ登録表の**層リストの先頭 5 層**から `NATIVE_LAYER_COUNTS["batch-parent-v7"]` を導き(P9r2 L1201-1203 / L1210-1217)、歴史ブロックは `native_v7_count(...)` を読む。**私は artifact 同梱の登録表からこの prefix view を再計算し、2090 / 8795 / 512 / 640 / 737 / 609 / 5 / 20 / 3,840 / 3,860 / 5 / [1450…2090] を得た — これは v8 正本 §2.1 の表と 1 個残らず一致する。** literal を足したのではなく、一つの pin 源から二つの view を作った点で v8 より強い。
2. **F-v8-1 は「別プロセスの production 束縛」という正攻法で解消された。** v8 の指摘は「`CURRENT_KEY_CONTRACT` は selftest で常時 False だから key 契約の否定例が存在しない」だった。v9 は P が自分自身を子プロセスとして起こし、そこだけ `production=True` で束縛して否定例を 1 本通す。親側は最後まで `production=False` のまま(L10990 / L11047 の二重確認)。**正例が通ること・封は両方有効であることを先に示してから負例が落ちることを要求する**ので、「何にでも当たる試験」ではない。
3. **登録表の key 一覧が「公刊 JSON の実 key 数」と全数一致した。** 登録表 `current_exact_keys` は acceptance 12 / parent-intake 73 / selection-start 19 / parent-layout 14 / head 24 / result 48 / checker-result 50 / final-manifest 27 / progress-head 16 / owner 8 / start 59 / selection 27 / separator 12 / source 10 / fixed-manifest 9。**私は実出力から HEAD 24・result 48・checker-result 50・selection-start 19・parent-intake 73・final-manifest 27・progress-head 16・owner 8 を数え、すべて一致を確認した。** C の独立和(12 / 73 / 59 / 14)とも一致。
4. **λ の失敗数が 7 世代目で減少に転じた。** 36,274 → 36,104 → 36,002 → 35,921 → 36,000 → 36,107 → **35,647**(今期 net **−460**)。v8 判読 F-v8-4 の「2 期連続増加」は今期反転した。**ただし単調減少が回復したわけではない**(7 世代のうち 3 回は増えている)。**Task 988 F4 の反例は依然排除されていない。**
5. **rank 2346 の sealed object は 1 つだけ。** v9 系譜の 3 run のうち候補 artifact を出したのは repair-v2 のみ(初回は artifact 無し、repair-v1 は診断 artifact 51,198,859 B のみ)。**F-v7-3 型(同一 rank に 2 つの seal)の再発は無い。** 「同一数学・別 seal」の比較は **今回 candidate が 1 本しかないので該当なし**。
6. **v7 判読の厳密式 `128·R + 8,128` が 6 層目も的中した。** C の `ordered_reductions_elements_parsed` 実測 193,728 / 210,112 / 226,496 / 242,880 / 259,264 / **275,648**(= 128 × 2090 + 8,128)。
7. **一意 parse バイトは v8 実測と層ごとに完全一致し、6 層目が加わった。** 129.778 / 141.432 / 153.185 / 164.938 / 176.691 / **188.444 MB**。6 層すべてで `parse_attempts = unique_documents = 128`・`repeated_input_bytes = 0`(F-v7-2 の解消が継続)。

---

## 1. (1) pin と TCB

### 1.1 便の pin の実測照合(私が `sha256sum` を実行)

| 対象 | bytes | sha256 | 判定 |
|---|---:|---|---|
| P9r2 `search/d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py` | 760,214 | `99cefc6c3eff5f0b192f9b2b1ee4e17e277b41b849e2392625041b86f0046db1` | **一致** |
| C9r2 `search/check_d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py` | 758,932 | `66132850f7dc4ff1edda0d5fe9bce565356fd84b0a10ca1ede328cd65d5b4ffa` | **一致** |
| driver `search/d972_r07_fixed_lambda_cycle_batch_v9_repair_workflow_driver_v2.py` | 16,522,905 | `d57d5ece97d18f66a83da4fd7defbf7b476b0cee1d9a9482455a09615cb50984` | **一致** |
| WF `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v9-repair-v2.yml` | 42,858 | `492f5bf2b6084e3151ebc62a8fa581ed0719e3b001111f26f2a6bfeb3b46cc1c` | **一致** |

系譜の旧版(比較元・私が実測):
`…batch_v9.py` 760,194 / `41ec6429…`・`check_…_v9.py` 758,892 / `bd8f14d9…`・`…workflow_driver_v1.py` 16,522,073 / `410b7519…`・`…repair_workflow_driver_v1.py` 16,522,256 / `cf034041…`・`…-v9.yml` 42,764 / `3ba2af8e…`・`…-v9-repair-v1.yml` 42,818 / `39b05cfb…`。v8 側の 2 本(`97f2523d…` / `503365d5…`)も v8 正本 §1.1 と一致。

- **C9r2 が P9r2 を bytes + sha256 で pin している**: `CURRENT_PRODUCER_REGISTRATION = {"bytes":760214, "file":"search/d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py", "sha256":"99cefc6c…"}`(C9r2 L462・照合は L1554 `v9_registered_final_P9_opaque_full_pin`)。**上表の私の実測と完全一致。**
- **P9r2 が C9r2 を pin する経路は file 名のみ**(P9r2 L35 `C_FILE`)。v7 / v8 と同じ非対称で、**変化なし**(§5)。
- **driver も同じ 2 本を pin**: `CURRENT_EXECUTABLE_PINS`(driver L35)が producer 760,214 / `99cefc6c…`・checker 758,932 / `66132850…`。さらに driver L5714-5718 が **basename が `..._v9_repair_v2.py` であること**と `os.environ[PREFIX+'_FILE']` との canonical 一致を要求。

### 1.2 artifact 実バイトからの独立確認(私が HTTP Range で取得し、自分で sha256 を計算)

| entry | bytes | 私の sha256 | 意味 |
|---|---:|---|---|
| `audit-region-registry.json` | **7,503,966** | `5d1796b17630510365d7d340c4c267f60a512f43daca967d64b10b2119cd0e52` | driver `INHERITANCE_REGISTRY_PIN`(L5479)= `shared-tcb.registry` と一致。**F-v7-4 系の導出源そのもの** |
| その canonical `new_source_audit.current_count_inputs` | — | `15619cfaec72a2d99196ce441f6072f065449b76e3df02295cfa0b8838df92ad` | **= P9r2 L1114 `CURRENT_COUNT_INPUT_SHA256` の literal**(canonical = `json.dumps(sort_keys,(",",":"),ensure_ascii)+"\n"`・P9r2 L1308-1309) |

加えて、artifact 同梱の実行体が repo の pin と bytes 一致していることを entry 一覧で確認した:
`checkout-sources/search/d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py` **760,214**・`checkout-sources/search/check_…_v9_repair_v2.py` **758,932**・`driver.py` **16,522,905**(`parent-timing-receipt.driver` の pin が `d57d5ece…` = 私の実測と一致)・`workflow.yml` **42,858**。
(ZIP 全量 DL はしていない — 限定条項 7。)

### 1.3 in-run の pin 検証証拠

`driver-bootstrap-stdout.log`(2,511 B)に **26 行の `OK`**(v8 は 22)。repo 側 13 + `/home/runner/work/_temp/fixed-lambda-batch-v9/` 側 13。**repair-v2 driver 自身が repo 側の検査対象に入っている**(`search/d972_r07_fixed_lambda_cycle_batch_v9_repair_workflow_driver_v2.py: OK`)。
**【軽微・継続 = F-v8-6】現行 WF(`…-v9-repair-v2.yml`)自身はこの 26 行に含まれない。** 同梱コピー `workflow.yml` は 42,858 B で repo の pin と bytes 一致(sha は §1.1 で repo 側を実測)。

### 1.4 TCB(v8 から**不変**+ P に 1 本の新辺)

- **算術 TCB**: `shared-tcb.json`(18,218 B)の `registered_shared_tcb.kernels` は **4 区間 = 共有カーネル 2 本 × P/C 各 1**(`vectorized_projection_chunk` P L342-357 / C L269-284、`sparse_adjoint` P/C とも L192-203)。**v7 / v8 と同一集合**(本数の増加は無い)。`status = DECLARED_SHARED_TCB` / `verified = false` / `current_run_call_coverage = NOT_MEASURED` / `kernel_third_independence_claimed = false`。
- **交差辺(独立性)**: C9r2 の import は標準ライブラリ + numpy + `check_d972_r07_complete_oracle_cegar_continuation_v2` のみ(C9r2 L10-37)で **v8 と 1 行も違わない**。**P9r2 を import する経路は無い。**
- **C9r2 は current registry を読まない**: `add_argument` 全 11 個に `--audit-region-registry` は**無い**(P9r2 は L11166 で必須引数として持つ)。C 内の "audit-region-registry.json" 6 箇所(L156/216/274/333/392/468)は**親 artifact の ZIP entry pin 表**であり、現行登録表の読み込みではない。**導出の独立性は構造として保証されている。**
- **【軽微・新設 = F-v9-5】P の import に `subprocess` が加わった**(v8 の import 集合との差はこの 1 本のみ)。用途は F-v8-1 修理のための自己子プロセス起動(P9r2 L10985-11047)。環境は 16 個の allowlist に絞られ credentials を継がず(L10996-11001)、子の argv は同一 source path と同一登録表 path を指し、実行前後で `file_pin(source_path)` と `file_pin(registry path)` の不変を要求する(L11044-11045)。**設計としては tight だが、P の TCB に「プロセス生成」という新しい種類の辺が 1 本増えた事実は裁定文に残すべき。**
- **harness TCB は単著**(WF 42,858 B + driver 16,522,905 B)。**run 側の判読は本書が唯一**である。

### 1.5 凍結 envelope(宇宙・cap)

`cost-receipt.registration` / `run-receipt.registration` / `output/owner.json.registration` の実値: `batch_size 128` / `max_batches 1` / `refill false` / `selection_policy CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX` / `partial_policy PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY` / producer `5,400 s・7,168 MiB` / checker `10,800 s・7,168 MiB`。**v7 / v8 と数値として完全同一 — caps・宇宙は 1 バイトも動いていない。**
`output/owner.json.scope` も `vertices 54432 / edges 108864 / chords 54433 / legality_rows 5 / source_lower 96776 / physical_lower 32260 / physical 48384 / p1_rows 8059 / characters [0,1,2,3] / auxiliary_tests 2` で不変。

---

## 2. (2) 規約表 diff(v8 → v9)

### 2.1 値の規約(**私が登録表から再計算し、C の独立和・実出力と三者照合**)

| 量 | v8 | v9 | P9r2 の出所(登録表導出) | C9r2 の出所(**独立**) | 実出力 | 私の再計算 |
|---|---:|---:|---|---|---:|:---:|
| 親 role 数 | 20 | **21** | 登録表 `parent_roles` ≡ `ROLES`(L1175) | `PARENT_ROLES = (*V8_PARENT_ROLES, "batch-parent-v8")`(L53) | 21 | 一致 |
| batch 親層数 n | 5 | **6** | `ROLES[15:]`(L1192) | `V9_CURRENT_PARENT_LAYER_COUNT = 7 − 1`(L509) | 6 | 一致 |
| `previous_parent_batch_rows` | 512 | **640** | 登録表の層和 | `V9_CURRENT_PREVIOUS_BATCH_ROWS`(L504) | 640 | 一致 |
| `total_parent_batch_rows` | 640 | **768** | 同上 | `V9_CURRENT_TOTAL_BATCH_ROWS`(L505) | 768 | 一致 |
| `target_derivation_parents` | 737 | **865** | `ancestry(97) + total` | `97 + 768`(L507) | 865 | 一致 |
| `previous_parent_target_derivations` | 609 | **737** | 同上 | `97 + 640`(L506) | 737 | 一致 |
| acceptance top-level key 数 | 11 | **12** | 登録表 `current_exact_keys.acceptance` | `6 + 6`(L514)+ 12 名の明示集合(L1495) | 12 | 一致 |
| `parent-intake` key 数 | 65 | **73** | 登録表 | `25 + 8 × 6`(L516) | **73** | 一致 |
| `start` key 数 | 54 | **59** | 同上 | `34 + 5 × (6 − 1)`(L515) | 59 | 一致 |
| `parent-layout` key 数 | 13 | **14** | 同上 | `acceptance + 2`(L517) | 14 | 一致 |
| `candidate_phase_manifests_checked` | 3,840 | **4,608** | `6 × total` | `6 × 768`(L511) | 4,608 | 一致 |
| `checkpoints_checked` | 3,860 | **4,632** | `6 × 4 + 4,608` | `(4 + 6 × 128) × 6`(L512) | 4,632 | 一致 |
| `invocations_checked` | 5 | **6** | 層 `invocations` の和 | `V9_CURRENT_INVOCATION_COUNT`(L513) | 6 | 一致 |
| `native_pairing_rows_rechecked` | [1450…2090] | **[1450,1578,1706,1834,1962,2090,2218]** | 累積 | `V9_CURRENT_NATIVE_PAIRING_ROWS`(L508) | 一致 | 一致 |
| `initial_rank` / `initial_generation` | 2090 / 8795 | **2218 / 8923** | `1450 + total` / `8155 + total` | `SIXTH_BATCH_RANK`(L449)/ `SIXTH_BATCH_GENERATION` | 2218 / 8923 | 一致 |
| selftest 群 | 7 | **8** | `[30,10,6,7,8,8,12,1]`(L11078) | `[28,9,6,7,8,10,14,15]` | 一致(§6) | 一致 |
| schema | `.v8` | `.v9` | — | — | 全公開 JSON | — |

**私は artifact の `audit-region-registry.json`(7,503,966 B)から `current_count_inputs` を取り出し、P9r2 の `registered_layer_counts`(L1131-1157)を自分で再実装して上表の「私の再計算」列を埋めた。16/16 一致。** 表の canonical sha も `15619cfa…` = P9r2 L1114 の literal と一致。

### 2.2 **最大の規約変更 = 歴史ブロックの「prefix view」への再指向**(v9 の中心)

```
P8   require(... len(prefix) == current_count("previous_parent_target_derivations") ...)   # v8: 現行値 = 609
P9r2 require(... len(prefix) == native_v7_count("previous_parent_target_derivations") ...) # v9: 歴史値 = 609(現行は 737)
```

`NATIVE_LAYER_COUNTS` は登録表の層リストの**各 prefix** に `registered_layer_counts` を適用して作られる(P9r2 L1201-1203)。`native_v7_count`(L1210-1217)は `NATIVE_LAYER_COUNTS["batch-parent-v7"]` だけを見せ、`current_exact_keys` / `key_counts` の参照を明示的に禁じる(`native_v7_numerical_scope_only`)。
**私は artifact の登録表から prefix(5 層)view を再計算し、2090 / 8795 / 512 / 640 / 737 / 609 / 5 / 20 / 3,840 / 3,860 / 5 / [1450,1578,1706,1834,1962,2090] を得た — v8 正本 §2.1 と 1 個残らず一致。** literal を新設したのではなく、同一の pinned 表の別 view を取っただけであることが数値で裏づけられた。
C 側も対称に、v8 期の `CURRENT_*` 群を凍結したまま `V9_CURRENT_*` 群を別に定義する(C9r2 L427-428 のコメント「Historical v8 independent sums remain fixed … no historical CURRENT_* meaning changes」)。v8 期の 11-key acceptance 検査は `native_v8_acceptance_exact_eleven_plain_keys` として**保持**されている。

### 2.3 公開 JSON key 集合

実出力で確認(私が実バイトから数えた): `output/HEAD` **24**・`result.json` **48**・`checker-result.json` **50**・`selection/start.json` **19**・`parent-intake.json` **73**・`final/manifest.json` **27**・`progress/HEAD` **16**・`owner.json` **8**・`tree.json` 14 — **すべて登録表の `current_exact_keys` の要素数および C の独立和と一致**。
**【軽微・継続 = F-v8-5】** `run-receipt` の自己申告 key が今期も版番号入り(`selection_lambda2090_…` → **`selection_lambda2218_oracle_is_separate_from_new_final_lambda_oracle`**)。literal 名で読む消費者を毎 run 壊す設計は未修正。

---

## 3. (3) 群別 PASS(本走の検査群)

| 群 | 何を要求しているか | 結果 | 私の独立確認 |
|---|---|---|---|
| **A. 第 21 親の入場** | 12-key acceptance・`batch_anchor_v8` の記述子が親 artifact と一致 | **PASS** | C9r2 L452-460 の `SIXTH_BATCH_*` / `FIXED_ARTIFACTS["batch-parent-v8"]` が rank 2218 / gen 8923 / state `0c6b08c4…` / target `e1b34dfa…` / λ `63b796b6…` / run 34701203323 / artifact 10301413308 / 413,467,399 B / mirror `cb63da6d…` / WF `…-v8.yml` を持ち、**v8 正本 §0・§1.2 の値と完全一致**。`run-receipt.accepted_artifacts` は 21 role、`accepted_batch_anchor_v8` が存在 |
| **B. 親層の累積則** | 128 / 640 / 768・祖先 97 → … → 865・pairing 7 点・層の分割和 | **PASS** | `parent-intake.json` の実バイトで確認: `previous 640 / total 768 / tdp 865 / old_tdp 97 / pairings [1450,1578,1706,1834,1962,2090,2218] / candidate_manifests 768 / phase 4,608 / checkpoints 4,632 / invocations 6`。中間記録 `intermediate 1578/8283/225`・`second 1706/8411/353`・`third 1834/8539/481`・`fourth 1962/8667/609`・`fifth 2090/8795/737` も揃う |
| **C. fresh λ_2218 oracle** | 選定 λ = v8 final λ・state_head = 受理側・roster 128 本 | **PASS** | `selection/start.json`: `selection_lambda_sha256 63b796b6…` / `state_head 0c6b08c4…` / `previous_target 2df80b53…`(= v7 final target)/ `target e1b34dfa…`(= v8 final target)/ `rank 2218` / `generation 8923` |
| **D. current 側 roster の独立再計算** | C が自前で残差選定をやり直す | **PASS** | `checker-stderr.log`: `{"chords": 54433, "failed": 35647, "phase": "fixed_lambda_all_residuals_selected", "selected": 128}` — **P の公刊 `failed_count 35647` と一致**。`tree.json` 実バイト: `residual_nonzero 35647 / first_failed_index 242 / first_failed_edge 489 / fit [1,2,0,0,0] / basis_chords [2,3,4,6,11] / independent_tau_columns 5 / aux_values [0,0]`。`failed-indices.u32` は **142,588 B = 4 × 35,647**(私が entry サイズから割り算した) |
| **E. old 側 oracle** | 36,107 / 304 / 603 が親の実体に結ばれる | **PASS(ただし再測ではない)** | P は親の保存 batch_anchor 内の `old_oracle` と literal の突合(P9r2 L6211-6213)、C は**親の保存 `selection.json` から読んだ値**と literal の突合(C9r2 L6240-6242)+ `failed-indices.u32` が **4 × 36,107 B** で先頭要素 304(C9r2 L6436-6438)。**どちらも λ_2090 から残差表を再計算してはいない**(→ F-v9-4・限定条項 2) |
| **F. 128 行の受理** | 128/128 INDEPENDENT・dependent 0・skipped 0 | **PASS** | `result.json`: `accepted_new_rows 128 / processed 128 / dependent 0 / skipped_after_linear [] / selected_count 128`。`checker-result.json`: `accepted_rows_compared 128 / candidate_decisions_compared 128 / all_completed_payloads_and_json_compared true / public_final_compared true / partial false / durable_tail null` |
| **G. 鎖と rank** | 2346 = 2218 + 128・gen 9051 = 8923 + 128 | **PASS** | HEAD / result / checker-result / final-manifest / progress-HEAD / run-receipt.current の 6 文書で `rank 2346 / generation 9051 / state_head fc1ac4d9…` が一致(私が実バイトで突合)。`anchor_previous 640 / anchor_total 768 / anchor_accepted 128 / anchor_completed_steps 64` |
| **H. 予言の非空虚性** | `first_candidate` 5 条件 → INDEPENDENT | **PASS(7 回目)** | `matches_prediction: true` / `expected = observed = INDEPENDENT` / `ordinal 0` / `raw_pairing 1` / `selection_scalar 1` / 5 条件すべて true。`independence_rate_predicted: false` の自己抑制は維持 |
| **I. UNKNOWN の置き場** | 未計算を 0 と読んでいないか | **PASS** | `new_lambda_oracle: null`・`failure_set_monotonicity_asserted: false`・`independence_rate_predicted: false`・`new_final_lambda_oracle_not_inferred: true`・`grade2_member/nonmember = NOT_DECIDED`・`full_A0 false`・`verified false`・`current_run_call_coverage = NOT_MEASURED`・`original_rho2_directly_read: false`・`positive_readout NOT_APPLICABLE`・`old_success_suites 0`・`old_insert/snapshot_numeric_replays 0`・`workshop_CV9: PENDING`。**NONMEMBER 主張は一切していない** |
| **J. 計器(診断)** | 6 層の parse / ordered reduction / 外側 55 区間 / 隣接 2 受領証 | **PASS** | §5.4 |

---

## 4. 限定条項(**8 条**・v8 から新設 1・解消 0)

1. **射程 = rank 2218 → 2346 の 1 batch のみ。** rank 2346 の λ\* に対する oracle は**未計算**(`new_lambda_oracle = null`)。**NONMEMBER 主張ではない。**
2. **a(128) = 128 は roster 前置 128 本の観測**(batch パラメータ k の性質ではない)。消化率 128 / 35,647 = **0.3591 %**。**Task 988 F4 の反例は排除されていない。** 失敗数は今期 **−460** と減少に転じたが、7 世代のうち 3 回は増えており**単調減少の前提は回復していない**。**本条には「old λ_2090 の 36,107 は本 run で再測されていない(親の保存バイトと literal の突合まで)」を含める**(§3-E)。
3. **算術 TCB は共有カーネル 2 本を含む**(P/C 各 1 で計 4 区間)。`current_run_call_coverage = NOT_MEASURED`・`kernel_third_independence_claimed = false`。**第三独立性はこの 2 本に及ばない。** P1 相が候補時間の **71.4 %**(1,011.433 / 1,417.334)なので `vectorized_projection_chunk` は確実に load-bearing。
4. **旧 2,218 行の実バイトは私自身は未取得。** λ_new ⊥ 旧行 と ρ₂ の旧行部分は checker の再現に依存する。**ρ₂ は依然 DERIVED**(`original_rho2_directly_read: false`)。「選定 λ_2218 が旧 2,218 行を殺す」ことも本 run で私が再測したわけではない。
5. **harness TCB は単著**(WF 42,858 B + driver 16,522,905 B)。**P の親層定数の値も harness 側の登録表に由来する**(表の内容は P の literal sha `15619cfa…` で固定されるが、**表を書いたのは driver 著者**)。この値を外部から縛るのは **C の独立和ただ一つ**である(F-v8-2 の継続)。**加えて v9 では、driver が pin する「著者側 public wire 文書」は形式検査(file 非空・bytes>0・sha256 16 進)しか受けない**ことを明記する(§5.3.2)。
6. **checker の相別 timestamp は依然無い。** `cost-receipt.limitations` が自ら「C candidate-phase timestamps are absent from these saved phase receipts … no C residual or P+C unmeasured subtotal inferred」と宣言。**F-k64-7 継続。**
7. **私は 429 MB の ZIP を全量ダウンロードしていない**(HTTP Range で必要 entry を個別取得)。ZIP 全体の sha は工房記録の mirror 値 `94da553a…` を採り、自分でバイト再計算していない。**私が sha256 を自分で計算したのは付録 A の 6 対象だけ。**
8. **【新設】第 21 親(batch-parent-v8)の admission に対する否定例は C 側にしか無い。** C の第 8 群 `batch-parent2218-six-layer-admission`(15 件)は現行値に向いた否定例(`current-previous-batch-count-is-stale` / `current-total-batch-count-is-stale` / `current-field-in-native65-intake` / `current-schema-in-native65-intake`)を含むが、**P の第 8 群は key 契約(1 件)に充てられ、P の現行値向け否定例は v8 期のまま凍結**(第 7 群の `current-previous512-as-native384` / `current-v8-checker-as-v7-repair2` は v8 の 512/384 と v8 checker 名を撃つもので、v9 の 640/768 と v9 checker 名は撃たない)。**検査の削除ではない**(P の件数は 81 → 82 と増えている)が、**P 側の「現行親層数の stale 検出」は今期 selftest で試験されていない**。`run-receipt.selftest_group_scopes` に `"one-side-specific-eighth-metadata-group"` と**事前登録されている**点は評価する。

### 4.1 前回 7 条との 1 対 1 対応

| v8 の条 | v9 での扱い |
|---|---|
| 1. 射程 1 batch | **継続**(条 1・rank が 2218→2346 に更新) |
| 2. a(k) の意味・F4 未排除・old λ 再測なし | **継続**(条 2)。**「2 期連続悪化」は今期解消**(失敗数 −460)だが、**単調性の前提は回復していない** |
| 3. 共有 kernel 2 本 NOT_MEASURED | **継続・集合も不変**(条 3・P1 相の比率 71.6 % → 71.4 %) |
| 4. 旧行の実バイト未取得・ρ₂ DERIVED | **継続**(条 4) |
| 5. harness TCB 単著 + 登録表が値の源 | **継続 + 範囲の明確化**(条 5・公開 wire pin は形式検査のみであることを追記) |
| 6. checker 段別 timestamp 無し | **継続**(条 6) |
| 7. ZIP 全量 DL せず | **継続**(条 7) |
| —(新設) | **条 8**(P 側に第 21 親の現行値向け否定例が無い) |

**7 条 → 8 条(新設 1・解消 0)。**

---

## 5. 弱化検出(本判読の主目的)

### 5.1 検査 1 — `require` ラベル集合の全数 diff(私の AST 実装)

| 側 | v8 のラベル | v9r2 のラベル | **削除** | 追加 | **出現回数が減ったラベル** |
|---|---:|---:|---:|---:|---:|
| P | 596(呼出 906) | **655(呼出 1,042)** | **6** | 65 | **0** |
| C | 638(呼出 682) | **723(呼出 780)** | **4** | 89 | **0** |

**削除 10 件はすべて版番号の改名であり、対応する v9 側の後継を 1 件ずつ特定した:**

| 側 | v8 で消えたラベル | v9r2 の後継 | 判定 |
|---|---|---|---|
| P | `all737_accepted_parents_and_only_new_accepted_target_rows` | `all865_…`(L8842) | 改名 |
| P | `current_count_five_separate_native_layers` | `current_count_six_separate_native_layers`(L1192) | 改名 |
| P | `production_requires_exact_twenty_roots_acceptance_and_output` | `…_twenty_one_roots_…`(L11193) | 改名 |
| P | `selftest_exact_seven_group_counts` | `selftest_exact_eight_group_counts`(L11078) | 改名 |
| P | `task1171_formal_binding_pending_static_draft` | `task1184_formal_binding_pending_static_draft`(L9517) | 改名 |
| P | `twenty_registered_roots` | `twenty_one_registered_roots`(L7570) | 改名 |
| C | `acceptance_exact_eleven_plain_keys` | `acceptance_exact_twelve_plain_keys`(L1496)。**11-key 版は `native_v8_acceptance_exact_eleven_plain_keys` として保持** | 改名 + 歴史版保持 |
| C | `all_twenty_roots_and_exact_acceptance` | `all_twenty_one_roots_and_exact_acceptance` | 改名 |
| C | `c8_current_root_key_counts_from_independent_sums` | `c9_current_root_key_counts_from_independent_sums` | 改名 |
| C | `v8_formal_inventory_and_final_source_binding_pending` | `v9_formal_inventory_and_final_source_binding_pending`(L1519) | 改名 |

**⇒ 消えた検査は 1 件も無い。** なお `same_json(...)` 経由の pin 検査は私の AST 器では拾えないため、`v8_registered_final_P8_opaque_full_pin` → **`v9_registered_final_P9_opaque_full_pin`**(C9r2 L1554)は grep で個別に確認した。

### 5.2 検査 2 — 同名ラベルの**条件式**の diff(改名では隠せない弱化の検出)

v8 / v9r2 で同名かつ 1 回出現のラベルについて `require(...)` の第 1 引数を正規化して比較。**実差分は P 5 件・C 1 件のみ**、いずれも前進:

| 側 | ラベル | v8 | v9r2 | 判定 |
|---|---|---|---|---|
| P | `batch_v7_609_prefix_plus_128_exact_DERIVED` | `current_count(…)` × 3 | `native_v7_count(…)` × 3 | **正しい前進**(§2.2)。同一 pin 源の prefix view へ。値は 609/128/737 で v8 と同一 |
| P | `batch_v7_complete_2090_native_basis_state_and_737_ancestors` | `current_count(…)` × 3 | `native_v7_count(…)` × 3 | 同上(2090 / 64 / 737) |
| P | `batch_v7_preserves_four_original_parent_layers` | `current_count("parent_layer_count") − 1` | `native_v7_count(…) − 1` | 同上(5 − 1 = 4。role 名の literal 4 本は不変) |
| P | `new_lambda2090_direct_all_rows_parent_start_and_final_targets` | `current_count("initial_rank")` | `native_v7_count("initial_rank")` | 同上(2090) |
| P | `batch_v7_internal_prior_view_exact_twenty_roles` | `== list(ROLES)` | `== list(HISTORICAL_V8_ROLES)` | **正しい前進**。`ROLES` が 21 になったため v7 の 20-role prior view を固定する必要がある。`len == 20` の要求は残存 |
| C | `batch_observation_independently_measured_parent_conditions` | `pairing["rows"] == FIFTH_BATCH_RANK` | `== SIXTH_BATCH_RANK` | 正しい前進(2090 → 2218) |

**⇒ 条件式の緩和は 1 件も無い。** P の 4 件はいずれも「現行値を読んでいた歴史ブロックを歴史値へ正しく向け直した」もので、**私は登録表から prefix view を再計算して v8 の実測値と完全一致することを確認した**(§2.2)ため、値の書き換えによる誤魔化しではない。

### 5.3 検査 3 — **逆置換検問**(裁定 2283 (3) / 2286 (3)・本節が本判読の中心)

私は 3 版すべてを独立に diff した。工房の計数と一致する(hunk 数は `diff -U0` 基準)。

| 差分 | hunk | 変更行 | 内容 |
|---|---:|---:|---|
| **P**: `…_v9.py` → `…_v9_repair_v2.py` | **2** | 2 | `C_FILE`(L35)と `WORKFLOW`(L8617)の 2 literal のみ |
| **C**: `check_…_v9.py` → `check_…_v9_repair_v2.py` | **2** | 4 | `PRODUCER_FILE` / `CHECKER_FILE` / `CHECKER_WORKFLOW`(L54-56)と `CURRENT_PRODUCER_REGISTRATION`(L462・bytes+sha を repair-v2 の実測値へ)の 4 literal のみ |
| **driver**: `…workflow_driver_v1.py` → `…repair_workflow_driver_v1.py` | **2** | 6 | ①巨大な `require` 1 本を**同じ 5 条件の `require` 5 本に分割**(why 文字列の細分化。連言は逐語で保存)②`V8_PARENT_FORMAL_RECEPTION` の `file` の区切り文字を `\\` → `/`(**bytes 16,074,290 と sha256 `8aa1e988…` は不変**) |
| **driver**: `…repair_workflow_driver_v1.py` → `…_v2.py` | **12** | 15 | §5.3.1 |

初回 run の fail-closed ラベルは失敗ログに `formal-file-directory-registration-separate-from-full-typed-parent-reception` として現れており、repair-v1 の①②はまさにその 1 本を 5 本に割り、期待値の path 綴りを実物に合わせたものである。**分割後も連言は逐語で同一**(`set(parent) == 4 keys` ∧ `canonical(registration) == canonical(v8_batch_registration())` ∧ `V8_PARENT_FORMAL_RECEPTION is not None` ∧ `canonical(root_receipt) == canonical(…)` ∧ `full_typed is True and type(scope) is str`)で、条件は 1 つも落ちていない。

#### 5.3.1 driver repair-v1 → repair-v2 の 15 行を全数分類(私が JSON 構造 diff を実装して中身まで比較)

| 変数 | 差分の実体 | 判定 |
|---|---|---|
| `CURRENT_EXECUTABLE_PINS` | producer/checker の file・bytes・sha を repair-v2 の**実測値**へ(6 フィールド) | 識別子 literal |
| `INHERITANCE_REGISTRY_RAW` / `INHERITANCE_REGISTRY_PIN` | 7,503,946 → **7,503,966**(+20 B = 改名分 10 文字 × 2 箇所)・sha を `5d1796b1…` へ。**私が artifact の実バイトからこの sha を再計算して一致を確認** | 識別子 literal |
| `current-v9-exact-source-basename-and-hash`(L5717) | 期待 basename を `…_v9_repair_v2.py` へ | 識別子 literal |
| `PARENT_TIMING_CONTRACTS` | 差分 30 件は**すべて `*/public_contract/{source,declaration,root_adoption,current_public_binding_overlay,stage_descriptions}` の pin**。`expected_completion_order` / `stage_rules` / `fields` / `monotonic_bounds` / `inclusive_relationships` は**一字も変わっていない** | 著者 wire 差し替え |
| `OUTER_PARENT_TIMING_STAGES`(2 行)/ `OUTER_PARENT_TIMING_SCOPE`(1 行) | `directory-restoration` と `native-intake` に **`batch-parent-v8` を追加**(scope 文字列に `/v8` を追記) | **計時区間の登録補完(追加)** |
| `SEVENTH_METADATA_SELFTESTS` / `EIGHTH_METADATA_SELFTESTS` | `producer-selftest.public_serializer` の pin 差し替えのみ。**`name` と `rejected_count` は不変** | 著者 wire 差し替え |
| `P_SEVENTH_SERIALIZER` | 差分 10 件はすべて fixture path の `check_…_v9.py` → `check_…_v9_repair_v2.py` 改名。**当該 fixture の raw は bytes 47・sha `068ff813…`・text `"opaque synthetic metadata; no source execution\n"` で byte-identical** | 識別子 literal |
| `P_EIGHTH_SERIALIZER` | `runtime_variables/actual_source/file_const` の 1 literal | 識別子 literal |
| `PUBLIC_V9_WIRE` / `V9_AUTHENTICATION_PUBLIC_CONTRACT` / `V9_NATIVE_OPERATIONS_PUBLIC_CONTRACT` | `source` は repair-v2 の実測 pin へ。`public_wire` / `root_adoption` / `current_public_binding_overlay` は task1189 の "repair2" 文書へ差し替え | 識別子 literal(source)+ 著者 wire 差し替え |

**⇒ 検査の弱化は 0 件。** 「計時区間の登録補完」は**測定の追加**であって検査の緩和ではない。この追加が必要だった理由は repair-v1 の失敗ログに直接現れている:

```
{"ordinal":20,"original_operation_result_not_replaced":true,
 "reason":"ValueError:batch_workflow:outer-parent-timing-registered-interval"}
```

すなわち repair-v1 では ordinal 20(= `batch-parent-v8`)の計時書き込みが未登録で例外になり(**包まれた本体の結果は差し替えられていない**)、区間だけが欠落していた。repair-v2 はそれを登録した。本 run の `parent-timing-receipt.json` は `outer_expected_count = 55` / `outer_intervals = 55` / **全 55 が `OBSERVED`** / `errors 0` / `missing_intervals 0`(P/C とも)で、内訳は live-parent 21・intake-inventory 21・native-intake 7・directory-restoration 6 = **55**、4 stage すべてに `batch-parent-v8` が入っている。

#### 5.3.2 **【要修正・新設 = F-v9-2】著者側 public wire の pin は形式検査しか受けない**

`PUBLIC_V9_WIRE` は driver 全体で **L10246 の `require(PUBLIC_V9_WIRE is not None, 'root-adopted-v9-public-wire-pending')` 1 箇所でしか使われない**。`V9_AUTHENTICATION_PUBLIC_CONTRACT` / `V9_NATIVE_OPERATIONS_PUBLIC_CONTRACT` の消費側 `v9_adjacent_public_contract`(L14986-15000)は `source` だけを `code_contract()` と canonical 一致させ、`public_wire` / `root_adoption` については **`file` が非空 str・`bytes` が正の int・`sha256` が 16 進** という型検査しかしない。`parent_timing_contract`(L10918-10926)も同様に `public_contract['source']` のみを実行体に束縛する。
その結果、repair-v2 で **P の public wire 宣言は 46,884 B → 10,036 B、`current_public_binding_overlay` は 28,790 B → 10,036 B へ縮み、declaration と overlay と stage_descriptions が同一文書に collapse した**(C 側は 19,510 B → 12,747 B)にもかかわらず、**実行される検査は 1 つも変わっていない**。
これは**本 run の弱化ではない**(縮む前もこれらの pin は実行検査ではなかった)。しかし「著者が宣言した公開契約が版を跨いで黙って縮んでも run は何も言わない」という構造は記帳すべきであり、限定条項 5 に含めた。**これらの文書は repo 外(著者 temp)にあり、私は中身を読めない。**

### 5.4 検査 4 — 4 計器が判定経路に触れていないこと(telemetry only)

**source 側**:
- `record_outer_parent_timing`(driver L10888-10907)は全体が `try/except` で、失敗時は stderr に `original_operation_result_not_replaced: true` の 1 行を書くだけ。**包まれた演算は block の外**(L10911-10916 `timed_parent_call`)。
- `check_v9_adjacent_timing_receipt`(L15199-15207)は **受領証が無ければ `None` を返す**(失敗しない)。存在する場合に要求するのは `canonical(value) == canonical(seal(…collect…))` すなわち**再導出の決定性のみ**で、`status` が PASS であることは要求しない。
- `collect_v9_adjacent_timing`(L15173-15187)は status を `COMPLETE_MEASURED_SCOPE` / `PARTIAL_OR_UNAVAILABLE` のどちらでも返し、`'missing_receipt_or_event_is_mathematical_failure': False` を自ら書き込む。

**受領証側**(私が実バイトから読んだ):

| 受領証 | bytes | 自己申告 |
|---|---:|---|
| `parent-timing-receipt.json` | **6,694,248** | `status PASS` / `outer_expected_count 55` / `outer_intervals 55` OBSERVED / `errors 0` / `causal_mechanism_identified false` / `mathematical_success_inferred false` / `inclusive_intervals_added_together false` / `candidate false` / `cross_checked false` / `verified false` |
| `parent-authentication-timing-receipt.json` | **8,430,863** | `kind authentication` / `COMPLETE_MEASURED_SCOPE` / P 6 events(11,205 行)・C 46 events(18,436 行)/ `missing_receipt_or_event_is_mathematical_failure false` / `arithmetic_success_inferred false` / `unobserved_values_filled_with_zero false` / `partial_counter_addition_identities_asserted false` |
| `native-metadata-operations-receipt.json` | **8,411,677** | `kind operations` / `COMPLETE_MEASURED_SCOPE` / P 6 events・C 12 events / 同上の 4 抑制 flag |
| (外側 55 区間) | — | `outer_inventory` は files 55 / directories 4 で、未登録ファイル・未登録ディレクトリはいずれも 0 |

**⇒ 4 計器はいずれも判定経路に触れていない。** `run-receipt` は 3 本を pin(6,694,248 / 8,430,863 / 8,411,677 — **便の記載と完全一致**)するが、その `status` を gate にしてはいない。

### 5.5 検査 5 — 空虚性(P 側 key 契約の否定例が実通過したか)

**【解消・F-v8-1】** P 第 8 群 `production-registered-key-contract`(1 件)の中身を逐語で読んだ(P9r2 L10898-10981)。非空虚性の根拠は 4 点:

1. **production 束縛が本物**: 子プロセスは `load_current_count_registry(args.audit_region_registry, production=True)` を呼び、直後に `require(CURRENT_KEY_CONTRACT is True, "production_key_child_actual_production_binding")`(L10908-10909)。読む表は**親と同一の実登録表**(`--audit-region-registry str(CURRENT_REGISTRY_CONTEXT["path"])`・L10993)。
2. **正例が通ることを先に確立**: `require(read_json(root, "positive/progress-head.json", "progress-head") == positive, "production_key_positive_normal_read_succeeded")`(L10929-10930)。**「何にでも当たる試験」ではない。**
3. **分離条件(ダミー検査)**: 負例は正例に key を 1 個足して seal を再計算したもので、`check_seal` は**正例・負例の両方で通る**ことを明示的に確認している(L10937-10938 のコメント「These two generic seal observations establish that the later normal read rejects at its key gate.」)。さらに「key 1 個と派生 seal 以外は完全一致」を要求(L10940-10943)。**⇒ 落ちる理由が key 契約であることが特定されている。**
4. **fail-closed**: 拒否しなければ `raise ValueError("production_key_canary_did_not_reject")`(L10950)。拒否メッセージは `fixed_lambda_batch:current_registered_exact_keys:progress-head` の完全一致を要求(L10948)。

親側は `require(CURRENT_KEY_CONTRACT is False, …)` を子の起動前(L10990)と回収後(L11047)の 2 回確認し、子の結果は seal + exact_keys + 全 field の値一致 + source/registry の pin 不変まで検査する(L11036-11046)。**実 stdout で当該群は `status PASS` / `rejected_cases ["extra-production-progress-head-key"]`。**

**【要修正・新設 = F-v9-3】ただし対称性は崩れた。** C は第 8 群に `batch-parent2218-six-layer-admission`(15 件)を新設したが、**P は第 21 親向けの新群を作らず**、第 7 群 `batch-parent2090-five-layer-admission`(12 件)を**v8 と逐語同一のまま**保持している。その 12 件のうち現行値を撃つ 2 件は `current-previous512-as-native384`(v8 の 512/384)と `current-v8-checker-as-v7-repair2`(v8 の checker 名)であり、**v9 の 640/768 と v9 checker 名は P 側 selftest では撃たれていない**。C 側には `current-previous-batch-count-is-stale` / `current-total-batch-count-is-stale` / `current-field-in-native65-intake` / `current-schema-in-native65-intake` があるので**二重化のうち片側は生きている**が、P の現行値 stale 検出は今期未試験である(限定条項 8)。
この非対称は `run-receipt.selftest_group_scopes` に `"one-side-specific-eighth-metadata-group"`、`producer-selftest-gate.json` に `new_production_key_metadata_selftest_groups: 1` / `new_parent_metadata_selftest_groups: 5`、`checker-selftest-gate.json` に `new_parent_metadata_selftest_groups: 6` として**事前登録・明示**されている。**隠していない**点は評価する。

---

## 6. selftest(**8 群**・件数は実 stdout から私が数えた)

| 側 | 群 | 件数(**stdout 実数**) | driver 登録 | run-receipt | 判定 |
|---|---|---:|---:|---:|---|
| P | `k128-version-registration-and-types` | **30** | 30 | 30 | PASS |
| P | `k128-full-roster-cutoff-and-restoration` | **10** | 10 | 10 | PASS |
| P | `batch-parent1578-admission-and-projection` | **6** | 6 | 6 | PASS |
| P | `batch-parent1706-two-layer-admission` | **7** | 7 | 7 | PASS |
| P | `batch-parent1834-three-layer-admission` | **8** | 8 | 8 | PASS |
| P | `batch-parent1962-four-layer-admission` | **8** | 8 | 8 | PASS |
| P | `batch-parent2090-five-layer-admission` | **12** | 12 | 12 | PASS(v8 と逐語同一) |
| P | **`production-registered-key-contract`** | **1** | 1 | 1 | PASS(**新設・F-v8-1 の解消**) |
| C | `k128-version-registration-and-types` | **28** | 28 | 28 | PASS |
| C | `k128-full-roster-cutoff-and-restoration` | **9** | 9 | 9 | PASS |
| C | `batch-parent1578-admission-and-projection` | **6** | 6 | 6 | PASS |
| C | `batch-parent1706-two-layer-admission` | **7** | 7 | 7 | PASS |
| C | `batch-parent1834-three-layer-admission` | **8** | 8 | 8 | PASS |
| C | `batch-parent1962-four-layer-admission` | **10** | 10 | 10 | PASS |
| C | `batch-parent2090-five-layer-admission` | **14** | 14 | 14 | PASS(v8 と逐語同一) |
| C | **`batch-parent2218-six-layer-admission`** | **15** | 15 | 15 | PASS(**新設**) |

- **三系一致**: 実 stdout の `rejected_cases` 実数 = driver の `EIGHTH/SEVENTH/SIXTH_METADATA_SELFTESTS` 登録値 = `run-receipt.new_selftest_rejections_registered` = `{"producer-selftest":[30,10,6,7,8,8,12,1], "checker-selftest":[28,9,6,7,8,10,14,15]}`。**P 82 + C 97 = 179 拒否**(v8 は 81 + 82 = 163)。`run-receipt.new_selftest_groups_registered = {"producer": 8, "checker": 8}`。
- **新設第 8 群(P)**: `extra-production-progress-head-key` のみ(§5.5)。
- **新設第 8 群(C)**: `omit-v7-from-native20-projection` / `alias-v8-local0-to-v7` / `…-v6` / `…-v5` / `…-v4` / `…-v3` / `drop-zero-from-complete865` / `previous-from-v8-start-previous` / `lambda-source-is-completed-selection` / `registered-empty-directory-missing` / `uncomputed-oracle-is-zero` / `current-field-in-native65-intake` / **`current-previous-batch-count-is-stale`** / **`current-total-batch-count-is-stale`** / `current-schema-in-native65-intake`。
- **【評価・非空虚】太字の 2 件は今期の前件そのものの否定形である** — 第 21 親を入れたときに previous(640)/ total(768)が古いまま残る失敗型(2251 型)を直接撃つ。`drop-zero-from-complete865` は祖先 865 の θ=0 記録脱落、`registered-empty-directory-missing` は空 dir の脱落、`uncomputed-oracle-is-zero` は未計算 oracle を 0 と読む誤りを撃つ(v8 と同型の継続)。
- **fixture gate**: P は `eighth_fixture_gate` 3,200 B(key 契約は fixture が小さい)、C は 19,534 B。`parent1706/1834/1962/2090` の gate も P/C 双方に実在。
- **metadata canary**: `metadata-gate.json` の `metadata_regression_cases: 16`・exit 0・`run-receipt.metadata_regression_cases_registered: 16`。**v7 / v8 と同数・継続。**
- **in-run 実行の証拠**: `producer-selftest-exit-code.txt` / `checker-selftest-exit-code.txt` / `producer-exit-code.txt` / `checker-exit-code.txt` / `metadata-exit-code.txt` / `driver-bootstrap-exit-code.txt` の **6 本すべてが `0`**。selftest stdout の `schema` は `d972.r07.fixed-lambda-cycle-batch.v9.selftest`、`status PASS` / `candidate false` / `cross_checked false` / `verified false` / `actual_anchor_arithmetic_replayed false` / `old_success_suites 0`。公開 selftest 版の分岐は今期も生じていない。

---

## 7. 格付け提案

**CV-9 = 同一対象(SAME OBJECT)・限定 8 条 → 工房格付け案: checker PASS / cross-checked(限定 8 条)・rank 2346 / gen 9051(state_head `fc1ac4d9057ef401de1740954cefa4c45d48ccfdbcffddfb59c8f5f8cae566ff`・run 34717506638 / attempt 1)を受理・`verified=false`・GRADE2 NOT_DECIDED・`full_A0=false`・A0 actual 0/1 不変。v8 の rank 2218 の直系後継として置き換える(合算ではない)。**

**司令塔への一行**: v9 の前件はすべて満たされた — **F-v8-1 は解消**(P が自分自身を子プロセスとして `production=True` で起こし、正例が読めること・封が両方有効であることを先に示したうえで余分 key 1 個の負例が `current_registered_exact_keys:progress-head` で落ちることを要求する、**分離条件つきの非空虚な否定例**が実通過した)、**F-v9-1 は一致**(P `WORKFLOW` = C `CHECKER_WORKFLOW` = repo WF path = run の `launch.workflow` = `…-v9-repair-v2.yml`。C は P を bytes 760,214 + sha `99cefc6c…` で pin し、私の実測と一致)、**第 21 親 batch-parent-v8 は 12-key acceptance で入場**(親 = v8 正本が受理した object そのもの: rank 2218 / state `0c6b08c4…` / λ `63b796b6…` / artifact 10301413308 / run 34701203323)、**fresh λ_2218 は current 35,647 / old 36,107 として正しく記録**され current 側は C が `select_all_residuals` で独立に 35,647 / selected 128 を再計算、**4 計器はいずれも telemetry only**(source の try/except・受領証欠落は `None` で非失敗・`missing_receipt_or_event_is_mathematical_failure: false` の自己申告・外側 55/55 OBSERVED)、**selftest は 8 群で三系一致**(P [30,10,6,7,8,8,12,1] / C [28,9,6,7,8,10,14,15]・私は stdout から 1 件ずつ数えた)。**逆置換検問も通過** — 初回→repair-v1→repair-v2 の全差分は P 2 literal・C 4 literal・driver 2+12 hunk で、JSON 構造 diff の結果その中身は「識別子 literal」「why 文字列の 5 分割(連言は逐語保存)」「計時区間 2 本の登録補完(測定の追加)」「著者 wire 文書の差し替え」だけであり、**検査の削除 0・条件の緩和 0・出現回数の減少 0**。「同一数学・別 seal」の比較は**今回 candidate が 1 本しかないので該当なし**(初回は artifact 無し・repair-v1 は診断のみ)。残す宿題は **F-v9-3(P 側に第 21 親の現行値向け否定例が無い非対称)** と **F-v9-2(著者 public wire の pin が形式検査のみ)**。

### 7.1 診断(**gate ではない** — 裁定 2225 / memory「cost-extrapolation-needs-math-review」)

- 実測: producer **1,893.895 s**(cap 5,400 の 35.1 %)/ checker **2,184.731 s**(cap 10,800 の 20.2 %)/ P+C **4,078.626 s**。P 残差 **463.278 s**(v8 は 413.376)。
- 層あたり P 残差増分: +42.823 / +45.042 / +49.207 / +42.336 / +44.006 / **+49.902**。**6 層目の増分は観測範囲(42.3〜49.9)の上端だが範囲内であり、「層費用が加速する」根拠は今期も得られていない。**(工房の `model_fixed_128_6 = 455.208` に対し観測 463.278、差 +8.070。**外挿はここでは行わない** — 次数の確定は数学者の領分。)
- 候補相の内訳: p1 **1,011.433 s(71.4 %)**/ primal 307.346 / reduction 42.947 / source 32.766 / raw 13.299 / B 9.543。**律速は 9 run 連続で P1 補正相。**
- 6 層の一意 parse バイト: 129.778 / 141.432 / 153.185 / 164.938 / 176.691 / **188.444 MB**。**先頭 5 層は v8 実測と完全一致。** 6 層すべてで `read_calls = parse_attempts = successful_parses = unique_documents = 128`・`repeated_parse_attempts = 0`・`repeated_input_bytes = 0`・`failed_parses = 0`・`changed_length_repeats = 0`。
- C の `ordered_reductions_elements_parsed`: 193,728 / 210,112 / 226,496 / 242,880 / 259,264 / **275,648**。**v7 判読の厳密式 `128·R + 8,128` が 6 層目も的中。**

### 7.2 v10 の前件として裁定に載せるべき所見 F-v9-*

| 札 | タグ | 内容 |
|---|---|---|
| **F-v9-1** | 【解消・記録】 | **P WORKFLOW / C CHECKER_WORKFLOW / repo WF path / run の `launch.workflow` の 4 者一致を確認**(`…-v9-repair-v2.yml`)。v10 では**改名を伴う版で P/C/driver/WF の 4 点 identity を発射前に機械照合する手順**を lane に残すこと(2286 の再発防止) |
| **F-v9-2** | **【要修正・記帳】** | **著者 public wire の pin は形式検査のみ。** `PUBLIC_V9_WIRE` は `is not None` 1 箇所、`v9_adjacent_public_contract` / `parent_timing_contract` は `source` 以外を型検査しかしない。結果、repair-v2 で P の public wire 宣言が 46,884 B → 10,036 B に縮み declaration/overlay/stage_descriptions が同一文書に collapse しても run は無反応。**弱化ではない**(元から実行検査ではない)が、限定条項 5 に明記し、v10 では「宣言文書が縮んだら気づく」機構(bytes の単調性か、内容の一部を run 内で読む)を足すか、**pin を「provenance のみ」と正直に改名すること** |
| **F-v9-3** | **【要修正・空虚性】** | **第 21 親の現行値向け否定例が C 側にしか無い。** P 第 8 群は key 契約(1 件)に充てられ、P の現行値否定例は v8 期の `current-previous512-as-native384` / `current-v8-checker-as-v7-repair2` のまま凍結。v10 では P に `current-previous640-as-native512` 相当と `current-v9-checker-as-v9-repair2` 相当を足し、**両側で現行値 stale を撃つ対称性を回復すること**(事前登録されている点は評価) |
| **F-v9-4** | 【要修正・計器(F-v8-3 の継続)】 | **old λ 側(36,107 / 304 / 603)は本 run でも再測されていない**(P L6212 は親の保存 anchor と literal の突合、C L6240-6242 + L6436-6438 は親の保存 `selection.json` と `failed-indices.u32` の長さ・先頭要素の突合)。2278 の「歴史的比較に限定」方式は実装として採られているが、**受領証にその限定を名指しする field が無い**。v10 では `batch_observation` に `old_side_recomputed_in_this_run: false` 相当を 1 個足すこと |
| **F-v9-5** | 【軽微・新設】 | **P の import に `subprocess` が加わり、P の TCB に「プロセス生成」という新しい種類の辺が 1 本増えた**(F-v8-1 修理のため)。環境 allowlist 16 個・credentials 非継承・同一 source pin の前後不変・親 deadline 内という設計は tight だが、**TCB の記述(shared-tcb / 限定条項 3)はこの辺をまだ数えていない**。v10 では `shared-tcb.json` に子プロセス起動の有無を 1 行足すこと |
| **F-v9-6** | 【一次データ・射程】 | **失敗数が 7 世代目で減少に転じた**(35,921 → 36,000 → 36,107 → **35,647**・今期 net **−460**)。7 世代の推移 36,274 / 36,104 / 36,002 / 35,921 / 36,000 / 36,107 / 35,647。**単調減少は依然として成り立たない**(3 回増えている)。残工程見積りを roster サイズで語る記述は台帳・地図から外したままにすること |
| **F-v9-7** | 【軽微・継続(F-v8-5 / F-v7-7)】 | `run-receipt` の自己申告 key が今期も版番号入り(`selection_lambda2218_…`)。literal 名で読む消費者を毎 run 壊す |
| **F-v9-8** | 【軽微・継続(F-v8-6)】 | `driver-bootstrap-stdout.log` の in-run pin は 26 行に増えた(v8 は 22)が、**現行 WF 自身は依然含まれない**。同梱 `workflow.yml`(42,858 B)と repo の一致は外部照合(§1.1 / §1.3) |
| **F-v8-2** | 【継続】 | 二系統一致の意味は v8 のまま(P の親層定数は単一の pinned 表由来・外部証拠は C の独立和ただ一つ)。**v9 では歴史ブロックも同じ表の prefix view になったため、この構造の射程が 1 段広がった** — 限定条項 5 に反映済み |
| **F-v8-7** | 【解消の方向・要確認】 | v8 で指摘した `BATCH_V7_PARENT_FACTS` の命名混同(親の公刊値と現世代の累積行数の同居)は、v9 では `native_v7_count` の導入で**数値の出所が名前ではなく関数で区別される**ようになった。`BATCH_V8_PARENT_FACTS` の命名自体は残っているので、v10 で名前を分ける宿題は継続 |
| **F-v7-1** | 【診断・継続】 | 9 点目でも線形の範囲内(§7.1)。「非線形に悪化するから急げ」という根拠は今期も無い |
| **F-v7-3** | 【今期は非該当】 | v9 系譜で候補 artifact を出したのは repair-v2 の 1 本のみ。**rank 2346 の sealed object は 1 つ。** rank の引用に state_head を併記する運用は継続すること |
| **F-v5-2 / F-v5-3 / F-v5-4 / F-k64-7** | 【軽微・継続】 | fixture 被覆窓・envelope 履歴(今期は fail-closed 2 本が envelope 内で正しく落ちた)・`basis-tau.u8` の二重索引(`basis_chords [2,3,4,6,11]` は今期も受領証に規約が未明示)・C の相別 timestamp 不在 |

---

## 付録 A. 私自身が sha256 を計算した対象

| 対象 | bytes | sha256 |
|---|---:|---|
| `search/d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py` | 760,214 | `99cefc6c3eff5f0b192f9b2b1ee4e17e277b41b849e2392625041b86f0046db1` |
| `search/check_d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py` | 758,932 | `66132850f7dc4ff1edda0d5fe9bce565356fd84b0a10ca1ede328cd65d5b4ffa` |
| `search/d972_r07_fixed_lambda_cycle_batch_v9_repair_workflow_driver_v2.py` | 16,522,905 | `d57d5ece97d18f66a83da4fd7defbf7b476b0cee1d9a9482455a09615cb50984` |
| `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v9-repair-v2.yml` | 42,858 | `492f5bf2b6084e3151ebc62a8fa581ed0719e3b001111f26f2a6bfeb3b46cc1c` |
| artifact `audit-region-registry.json` | 7,503,966 | `5d1796b17630510365d7d340c4c267f60a512f43daca967d64b10b2119cd0e52` |
| その canonical `new_source_audit.current_count_inputs` | — | `15619cfaec72a2d99196ce441f6072f065449b76e3df02295cfa0b8838df92ad`(= P9r2 L1114 の literal) |

参考(系譜比較のため repo 側で実測): `…batch_v9.py` 760,194 / `41ec6429…`・`check_…_v9.py` 758,892 / `bd8f14d9…`・`…workflow_driver_v1.py` 16,522,073 / `410b7519…`・`…repair_workflow_driver_v1.py` 16,522,256 / `cf034041…`・`…-v9.yml` 42,764 / `3ba2af8e…`・`…-v9-repair-v1.yml` 42,818 / `39b05cfb…`・v8 の P/C(`97f2523d…` / `503365d5…`)。

## 付録 B. 判読者の限界(正直な申告)

- 旧 2,218 行の実バイトを取得していないので、λ_new ⊥ 旧行 と ρ₂ 恒等式の旧行部分は checker の再現に依存している(限定条項 4)。
- **本判読は増分規律に従い、「128 行の階段形・λ の後退代入 48,384 座標・target 恒等式 128 段・rolling 鎖 128/128」の全数再計算を今期も行っていない。** 本書が実測で閉じたのは付録 A の 6 対象・登録表からの導出 16 量(current view)+ 12 量(v7 prefix view)・公刊 JSON の key 数 8 種・計器 6 層 + 外側 55 区間 + 隣接 2 受領証・selftest 179 件・`require` ラベル diff(全数)・条件式 diff(同名単一ラベル全数)・**3 版の全差分の JSON 構造 diff(全数)** である。**したがって「算術が正しい」ことの本期の根拠は C の PASS と §3 の群別確認であり、私の再計算ではない。**
- old λ_2090 の残差表を私自身は再計算していない(F-v9-4)。
- 著者側 public wire 文書(`C:/…/task1189/…`)は repo 外にあり中身を読めない。私が確認したのは driver がそれらを**形式検査しかしていない**ことだけである(F-v9-2)。
- `sparse_adjoint` / `vectorized_projection_chunk` が本 run の実行経路で呼ばれた行は特定していない。
- repair-v1 の P 入口失敗について、**静的原因**(P9 の `WORKFLOW` literal が `…-v9.yml` のままで、実 WF は `…-v9-repair-v1.yml`)は diff で確認し、**失敗した step**(「Run one fresh fixed-lambda batch …」で exit 1)もログで確認したが、**P が出したエラー文字列そのものはログに現れていない**ので直接は見ていない。
- Release ミラーは確認していない(工房記録 `94da553a…` に依拠)。
- **この観点では仕様の齟齬(別対象)も検査の弱化も見つけられなかった — 保証ではない。**

---

**裁定 2293(司令塔・2026-09-13)格付け**: 本判読(60,883 B/236fdc85…・工房 sha256sum で pin)を正本として採用。CV-9 = 同一対象・限定 8 条(新設 1・解消 0)→ **rank 2346/gen 9051(state_head fc1ac4d9…・run 34717506638/1)を cross-checked(限定 8 条)で受理**・v8 の 2218 の直系後継として置換・verified=false・grade-2 NOT_DECIDED・full_A0=false。逆置換検問(初回 → repair-v1 → repair-v2)は通過・弱化 0 件。F-v9-2〜8 を v10 の前件・所見として台帳 2293 に登録。

**裁定 2294 追補(Astra erratum・工房再計算で確認)**: F-v9-6 の「7 世代中 3 回は増加」は誤記。系列 36,274 → 36,104 → 36,002 → 35,921 → 36,000 → 36,107 → 35,647 の隣接差 -170/-102/-81/+79/+107/-460 で増加は **2 回**(+79/+107)。「単調減少の前提は回復していない」の結論と限定条項 2 は不変。

**裁定 2295 追補(Astra 精密化・F-v9-3 の表現)**: 「P の現行値否定例は v8 期(512/384・v8 checker 名)のまま凍結」は表現が過剰。P の旧 case 名 current-previous512-as-native384 の実 positive は 640/768・negative は 640 → 384、current-v8-checker-as-v7-repair2 の実 positive は v9_repair_v2・negative は v7_repair_v2(Astra root 4 fixture 照合)= case 名が旧く値は現行。**直前版 512/640 と v8 checker を狙う明示負例の不足は残る**ため限定条項 8 は維持。
