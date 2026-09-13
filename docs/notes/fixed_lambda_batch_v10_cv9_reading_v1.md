# 増分 CV-9 判読 — R07 fixed-lambda cycle batch **v10**(rank 2346 → 2474・**第 22 親 batch-parent-v9 の入場**・**13-key acceptance**・fresh λ_2346 oracle・**prefix view の一般化(全層 prefix)**・**P 第 9 群 = 第 22 親 + 現行契約の 29 否定例**・**old 側非再測の受領証明示**・**子プロセス辺の TCB 登録**)

対象 run: **34731988156 / attempt 1**(私が `gh run view` で確認 = `status completed` / `conclusion success`・head `785bd2d87f2b97452a7f0deb2085afe4e7e56d95`・workflow `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v10.yml`(WF 名 `d972-r07-fixed-lambda-cycle-batch-v10-envelope-v1`)・2026-09-13T02:01:24Z → 03:13:07Z・**P / C / 両 selftest / metadata / driver-bootstrap の exit code 6/6 が 0**)
候補 artifact **10310711557**(**448,498,707 B**・zip entry **12,590** — 私が central directory を読んで数えた)/ 診断 artifact **10310542290**
判読者: falsifier(非当事者・事後)。判読日 2026-09-13。
適用規律: **増分 CV-9**(裁定 2105 / 2110 / 2117・memory「CEGAR incremental CV-9」)— 規約表 diff を毎回・pin + TCB 集合が同一なら類似度は省略・**弱化検出が主目的**。
前回 CV-9 正本: `docs/notes/fixed_lambda_batch_v9_cv9_reading_v1.md`(裁定 2293・限定 8 条・F-v9-1〜8・裁定 2294 / 2295 追補)。**本書は v9 正本を一切編集していない。**

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 8 条(§4・新設 1・解消 1)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 8 条)・rank 2474 / gen 9179(state_head `168d2cf1004ee6ace61fd082dedb21af41ff1047cf3a88482ed8170ad81786f9`・run 34731988156 / attempt 1)を受理・`verified=false`・GRADE2 NOT_DECIDED(member / nonmember とも)・`full_A0=false`・A0 actual 0/1 不変。v9 の rank 2346 の直系後継として置き換える(合算ではない)。**

**a(128) = 128**(offered 128 / accepted 128 / dependent 0 / skipped 0・`partial=false`・`durable_tail=null`)。rank 2474 = 2346 + 128。消化率 128 / 35,780 = **0.3577 %**。

**検査の弱化は 1 件も検出できなかった**(§5・機械全数)。**v9 の前件 5 件のうち 4 件が解消**(F-v9-3 / F-v9-4 / F-v9-5 / F-v9-7・加えて F-v9-8 も解消)、**F-v9-2 のみ範囲縮小で継続**。

| v10 の前件 | 判定 | 根拠(要約) |
|---|---|---|
| **F-v9-3**(P 側に第 22/21 親の現行値向け否定例が無い) | **解消(双方向の明示負例が実通過)** | P 第 9 群 **`batch-parent2346-seven-layer-and-current-contracts`(29 件)** が新設され、`current-v10-previous768-as-native640` / `current-v10-total896-as-native768`(**現行値 → 直前版 640/768 に差し替える負例**)と `current-v10-checker-as-v9-repair2`(**現行 checker 名 → 直前 checker 名**)、およびその鏡像 `native-v9-previous640-as-native512` / `native-v9-total768-as-native640` / `native-v9-checker-as-v8` を含む。gate は `current_final_previous_and_total_parent_rows` / `current_independent_checker_entry_identity`。P10 L12141-12147 が `native_v9_final_parent_counts`(歴史)と `current_final_parent_counts`(現行)、`native_v9_checker_entry_identity` と `current_checker_entry_identity` を**両方**駆動する |
| **F-v9-4**(old λ 非再測の受領証明示) | **解消** | P10 **L10145** が `batch_observation` に `"old_side_recomputed_in_this_run": False` を書く。C10 **L7922-7926** が「ちょうど 7 key」(`batch_observation_current_exact_seven_keys`)と `value["old_side_recomputed_in_this_run"] is False`(`batch_observation_old_side_not_recomputed`)を要求。C 第 9 群に **`old-side-recomputed-is-true` / `old-side-recomputed-is-integer-zero` / `old-side-recomputed-field-missing`** の 3 否定例(C10 L10965-10971)。**空虚でない** |
| **F-v9-2**(著者 public wire の pin が形式検査のみ) | **範囲縮小で継続(弱化なし)** | `PUBLIC_V10_WIRE` は driver L10327 の `is not None` 1 箇所のみ(v9 と同じ)。`v10_adjacent_public_contract`(driver L16899-16917)は v9 から **1 条追加**(`canonical(contract['provenance_scope']) == canonical(current_public_declaration_scope())`・ラベル `adjacent-declaration-is-root-review-provenance`)。**その `provenance_scope` の中身が「`declaration_contents_read_in_this_run: false` / `byte_monotonicity_is_semantic_evidence: false`」の自己申告**(driver `current_public_declaration_scope()`・公刊 `shared-tcb.json.public_declaration_scope` で私も実バイト確認)。v9 正本が示した二択のうち **「provenance のみと正直に宣言する」側が採られた**。さらに wire の 1 本 `keysets`(12,401 B / `6f92e487…`)は **canonical(登録表 `current_count_inputs`) と完全一致**することを私が独立計算で確認(§1.2)— 6 本のうち 1 本は実バイトに束縛されている |
| **F-v9-5**(P の subprocess 辺が TCB に計上されていない) | **解消** | 公刊 `shared-tcb.json`(22,386 B)に **`current_execution_edges`(2 本)** が新設。`producer-key-contract-child`(`--key-contract-selftest`)と `producer-parent-contract-child`(`--selftest-parent2346-contract-child`)。各辺が source pin(1,034,265 / `33c4bbb9…`)・env allowlist 16 + 必須 2・`secret_environment_values_serialized: false`・`additional_child_budget_seconds: 0`・`parent_production_binding: false` / `child_production_binding: true`・`mathematical_third_independence_claimed: false`・`status: DECLARED_EXECUTION_EDGE` を持つ |
| **第 22 親(batch-parent-v9)の 13-key acceptance 入場** | **入場済み(私が公刊 acceptance の key を数えた)** | `acceptance.json`(**17,819,829 B**・私の sha256 `9b7b2188a8d0edee63a1db9f17d7e430f7653f437ab5cd74d8f0e25b3e1e4f0c`)の top-level key は**ちょうど 13**:`schema, parents, anchor, batch_anchor, next_batch_anchor, batch_anchor_v5, batch_anchor_v6, batch_anchor_v7, batch_anchor_v8, `**`batch_anchor_v9`**`, code, runtime, registration`。`parents` は 22 role。`batch_anchor_v9` = rank 2346 / gen 9051 / state `fc1ac4d9…` / λ `289190c3…` / target `96785516…` / 768 / 896 / 993 / 64 / `accepted_schema = …v9` / `old_oracle {35647, 242, 489}` = **v9 正本が受理した object そのもの**。`run-receipt.accepted_artifacts` は **22 role**(`batch-parent-v9` = artifact 10306226977 / run 34717506638 / head `6b105348…` / 429,844,909 B / `94da553a…` / WF `…-v9-repair-v2.yml`) |
| **fresh λ_2346 / 旧 λ_2218 の記録** | **正しい** | `selection/start.json.selection_lambda_sha256 = 289190c37a1a564ec7f062677caad94d4a8dddccb1afee5cd7d117beaa438776`(= v9 final λ)・`state_head fc1ac4d9…`・`previous_target e1b34dfa…`(= v8 final target)・`target 96785516…`(= v9 final target)・rank 2346 / gen 9051。`batch_observation.current` = **35,780** / 847 / 435、`old` = **35,647** / 489 / 242(= v9 正本 §3-D の実測値と完全一致・親 artifact は v8 の 10301413308) |
| **10 領域の原文同一 / 最適化の未導入** | **確認(原文同一)** | `canonical` / `seal` / `check_seal` / `json_bytes` / `read_json` / `sha` / `require` / `integer` / `same_json` / `file_pin` の **10 定義すべてが source segment の sha256 まで同一**。加えて **v9r2 の 304 定義のうち 287 が byte 同一・削除 0**、import 集合は P/C とも **1 行も差が無い**、`lru_cache` / `functools.cache` / `_CACHE` 等の導入は **0 件**(§5.4) |
| **19 reader が第 22 親の必須経路** | **必須経路(selftest 専用クローンではない)** | 新設 19 本はすべて `authenticate_batch_v9_parent` から(直接 or 2 段)呼ばれ、`authenticate_batch_v9_parent` は **本走の `authenticate_acceptance` L8531** が `authenticate_parent_with_parser_bytes("batch-parent-v9", 6, admission, authenticate_batch_v9_parent)` として渡す。`promote_batch_v9_anchor` は **`run_actual` L10471**。`batch_v9_prior_admission` は `authenticate_acceptance` L8514-8528。**第 9 群の canary は同じ関数を再利用**(`parent2346_contract_child.exercise` が同名関数を呼ぶ)— クローンではない(§5.6) |
| **計器 3 本が判定経路に触れていない** | **触れていない(source と受領証の両方)** | §5.7 |
| **selftest 群の群別拒否件数** | **実 stdout と一致(三系)** | P `[30,10,6,7,8,8,12,1,29]`(計 **111**)・C `[28,9,6,7,8,10,14,15,20]`(計 **117**)。**私が stdout の `rejected_cases` を 1 件ずつ数えた**(§6) |

### 本判読の一次事実(新規)

1. **prefix view が「特定の 1 層」から「全層」へ一般化された。** v9 では `NATIVE_LAYER_COUNTS` は v7 用の 1 view として使われていた。v10 は `load_current_count_registry`(P10 L1216-1219)で**層リストの全 prefix について** `registered_layer_counts` を適用し、`native_v7_count`(L1223-1230)と **`native_v8_count`(L1232-1239)** が同じ dict の別 key を読む。**私は artifact 同梱の登録表(15,060,310 B)から両 view を自分で再計算し、v8 view = 2218 / 8923 / 21 / 640 / 768 / 865 / 737 / 6 / 4,608 / 4,632 / [1450…2218] / 6、v7 view = 2090 / 8795 / 20 / 512 / 640 / 737 / 609 / 5 / 3,840 / 3,860 / [1450…2090] / 5 を得た — v9 正本 §2.1 と v8 正本 §2.1 の表に 1 個残らず一致する。** 歴史値の literal は 1 個も増えていない。
2. **第 22 親の descriptor は P 自身の source でも pin されている。** `BATCH_V9_PARENT_FACTS`(P10 L1118・587 B)が rank 2346 / gen 9051 / state / λ / target / 768 / 896 / 993 / 64 を持ち、`batch_v9_anchor_header`(L7070-7096)が acceptance の `batch_anchor_v9` を **field ごとに strict-integer + 完全一致**で突合する(`batch_anchor_registered_count:*` / `batch_anchor_registered_value:*`)。**harness 側 acceptance と P source の二重 pin**であり、v8 期から一歩前進(限定条項 5 の射程が狭まる)。
3. **P の +274,051 B の内訳は「第 9 群が主」。** 定義単位の全数 diff では**追加 26 本 91,271 B・変更 17 本 +2,770 B・削除 0**、残り **180,010 B は module 直下**。その module 増分の **87 %(156,222 B)は `BATCH_V9_PUBLIC_HEADER_FIXTURE`** で、**用途は第 9 群 child の positive fixture 1 箇所のみ**(P10 L12057)。第 9 群の総費用は 156,222 + 8,631(`NINTH_CASE_SPECS`)+ 22,018(child + canary 関数)= **186,871 B = 増分の 68.2 %**。Astra 内訳(裁定 2297)は総和が 274,051 で私の総和と一致するが、この fixture を「登録定数/名前空間」に分類している(§5.5・**数値の齟齬ではなく分類の差**)。
4. **選定 λ の失敗数が再び増加した。** 36,274 → 36,104 → 36,002 → 35,921 → 36,000 → 36,107 → 35,647 → **35,780**(今期 net **+133**)。隣接差 −170 / −102 / −81 / +79 / +107 / −460 / **+133** で、**8 世代のうち増加は 3 回**。**Task 988 F4 の反例は依然排除されていない。**
5. **rank 2474 の sealed object は 1 つだけ。** v10 系譜は 1 run のみ(初回で success)。**F-v7-3 型(同一 rank に 2 つの seal)の再発は無い。** 逆置換検問の対象となる修理版も存在しない。
6. **本 run は v9 より 15〜22 % 速い。** P total 1,601.351 s(v9 1,893.895・**−15.4 %**)/ C total 1,817.972 s(v9 2,184.731・**−16.8 %**)/ p1 相 786.791 s(v9 1,011.433・**−22.2 %**)。**7 層目の P 残差は 442.865 s で v9 の 463.278 s より小さい**(層が増えたのに減った)。**層あたり費用の系列比較は runner 速度で交絡しており、本 run から費用モデルを更新してはならない**(§7.1・裁定 2225 / memory「cost-extrapolation-needs-math-review」)。
7. **v7 判読の厳密式 `128·R + 8,128` が 7 点目も的中。** C の `ordered_reduction_elements` 実測 193,728 / 210,112 / 226,496 / 242,880 / 259,264 / 275,648 / **292,032**(= 128 × 2218 + 8,128)。**私が checker-stderr.log の JSON 行を全数 parse して抽出した。**

---

## 1. (1) pin と TCB

### 1.1 便の pin の実測照合(私が `sha256sum` を実行)

| 対象 | bytes | sha256 | 判定 |
|---|---:|---|---|
| P10 `search/d972_r07_fixed_lambda_cycle_batch_v10.py` | 1,034,265 | `33c4bbb97313bc1ea2017b6ac6ad2cc0932ae15d1affc8bcd6a8aaedd0c76085` | **一致** |
| C10 `search/check_d972_r07_fixed_lambda_cycle_batch_v10.py` | 870,249 | `a21fd2b54958f84ea67e7b3a079893cff70544961005d6c79a0f6ff47e752ca8` | **一致** |
| driver `search/d972_r07_fixed_lambda_cycle_batch_v10_workflow_driver_v1.py` | 32,326,911 | `acf206e5fe423288f3449e5e034a1bd125a6c203e6c274b64f41fc36ab94c802` | **一致** |
| WF `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v10.yml` | 47,555 | `88856a3329ccb59750c427fd27ba6857d89953b75a65f93a11f260783f67f34a` | **一致** |

比較元(v9 repair-v2・私が再実測し **v9 正本 §1.1 と完全一致**を確認): `…batch_v9_repair_v2.py` 760,214 / `99cefc6c…`・`check_…_v9_repair_v2.py` 758,932 / `66132850…`・`…repair_workflow_driver_v2.py` 16,522,905 / `d57d5ece…`・`…-v9-repair-v2.yml` 42,858 / `492f5bf2…`。

- **C10 が P10 を bytes + sha256 で pin**: `CURRENT_PRODUCER_REGISTRATION = {'file': 'search/d972_r07_fixed_lambda_cycle_batch_v10.py', 'bytes': 1034265, 'sha256': '33c4bbb9…'}`(C10 **L536**・照合は L1639 `current_registered_final_producer_opaque_full_pin`)。**上表の私の実測と完全一致。**
- **v9 期の producer pin は凍結保持**: `HISTORICAL_V9_PRODUCER_REGISTRATION`(C10 **L463**)= 760,214 / `99cefc6c…`。上書きではなく並置 — 歴史検査の拠り所が残った(前進)。
- **P10 が C10 を pin する経路は file 名のみ**(P10 **L35** `C_FILE = "check_d972_r07_fixed_lambda_cycle_batch_v10.py"`)。v7 / v8 / v9 と同じ非対称で、**変化なし**(限定条項 5)。ただし `current_checker_entry_identity`(P10 L1281-1283)が公刊 source entry の `file == "search/" + C_FILE` を要求し、`native_v9_checker_entry_identity`(L1285-1287)が v9 repair-v2 の path を literal で要求する — **第 9 群の 2 否定例で試験済み**。
- **driver も同じ 2 本を pin**: `CURRENT_EXECUTABLE_PINS`(driver **L35**)が producer 1,034,265 / `33c4bbb9…`・checker 870,249 / `a21fd2b5…`。
- **WF も 4 ファイルを bytes+sha で env に持つ**(WF L182-196: `PRODUCER_*` / `CHECKER_*` / `WF_FILE` / `WORKFLOW_DRIVER_*`)— 私の実測と一致。

### 1.2 artifact 実バイトからの独立確認(私が HTTP Range で取得し、自分で sha256 を計算)

| entry | bytes | 私の sha256 | 意味 |
|---|---:|---|---|
| `audit-region-registry.json` | **15,060,310** | `bff0d81b71c606117ecfed87f7993e2b800af1e278ddc6bac8c86be8cc4a6d4b` | driver `INHERITANCE_REGISTRY_PIN`(L5479)と一致。**§2.1 の値表の導出源そのもの**(v9 の 7,503,966 B から倍増) |
| その canonical `new_source_audit.current_count_inputs` | **12,401** | `6f92e487d6190ac36c00b40392a1082d9854032af4fbade4f2e30d9ad7126c00` | **= P10 L1126 `CURRENT_COUNT_INPUT_SHA256` の literal**、**かつ `PUBLIC_V10_WIRE.keysets` の pin(12,401 B / `6f92e487…`)と bytes・sha とも一致** |
| `acceptance.json` | **17,819,829** | `9b7b2188a8d0edee63a1db9f17d7e430f7653f437ab5cd74d8f0e25b3e1e4f0c` | top-level 13 key・`parents` 22 role(§0) |

**C10 が pin する v9 親の登録表 entry は `(7503966, "5d1796b1…")`(C10 L542)で、これは v9 正本 §1.2 で私が自分で計算した値そのものである** — 世代を跨いだ独立照合が成立した。
(ZIP 全量 DL はしていない — 限定条項 7。私が bytes を読んだ entry は付録 A の一覧。)

### 1.3 in-run の pin 検証証拠

`driver-bootstrap-stdout.log`(3,094 B)に **32 行の `OK`**(v9 は 26)。repo 側 16 + `/home/runner/work/_temp/fixed-lambda-batch-v10/` 側 16。
**【解消 = F-v9-8】1 行目が `…/.github/workflows/d972-r07-fixed-lambda-cycle-batch-v10.yml: OK` であり、現行 WF 自身が in-run pin 検査に入った。** v9 で指摘した穴は閉じている。
`runtime-observation.json`(428 B)= `launch {run 34731988156, attempt 1, head 785bd2d8…, workflow .github/workflows/d972-r07-fixed-lambda-cycle-batch-v10.yml}`・`expected == actual`(python 3.13.15 / numpy 2.5.1)。

### 1.4 TCB(kernel 集合は**不変**+ 子プロセス辺が**登録された**)

- **算術 TCB**: 公刊 `shared-tcb.json`(22,386 B)の `registered_shared_tcb.kernels` は **4 区間 = 共有カーネル 2 本 × P/C 各 1**。file・line_first/last・region_sha256 が **v9 と 1 文字も違わない**(`vectorized_projection_chunk` P 342-357 `b68bbb5a…` / C 269-284 `6e785bdf…`、`sparse_adjoint` P/C とも 192-203 `4b755842…`)。`status = DECLARED_SHARED_TCB` / `verified = false` / `current_run_call_coverage = NOT_MEASURED` / `kernel_third_independence_claimed = false`。**集合の増加は無い。**
- **交差辺(独立性)**: **C10 の import は C9r2 と 1 行も違わない**(私が import 行を diff して空)。標準ライブラリ + numpy + `check_d972_r07_complete_oracle_cegar_continuation_v2` のみで、**P10 を import する経路は無い**。
- **C10 は current registry を読まない**: `add_argument` に `--audit-region-registry` は**無い**。C10 内の `"audit-region-registry.json"` 7 箇所(L157/217/275/334/393/469/542)は**親 artifact の ZIP entry pin 表**であり現行登録表の読み込みではない。**導出の独立性は構造として保証されている。**
- **【解消 = F-v9-5】子プロセス辺が TCB に登録された**: `shared-tcb.json.current_execution_edges` が **2 本**(§0)。P10 の import 集合は v9r2 と**完全同一**(`subprocess` は既にあった)なので、増えたのは辺の本数(1 → 2)と**その明示登録**である。
- **harness TCB は単著**(WF 47,555 B + driver 32,326,911 B)。**run 側の判読は本書が唯一**である。

### 1.5 凍結 envelope(宇宙・cap)

公刊 `output/owner.json.registration` / `cost-receipt.registration` / `run-receipt.registration` の実値(私が 3 文書の実バイトで突合): `batch_size 128` / `max_batches 1` / `refill false` / `selection_policy CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX` / `partial_policy PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY` / producer `5,400 s・7,168 MiB` / checker `10,800 s・7,168 MiB`。**v7 / v8 / v9 と数値として完全同一 — caps・宇宙は 1 バイトも動いていない。**
`output/owner.json.scope` も `vertices 54432 / edges 108864 / chords 54433 / legality_rows 5 / source_lower 96776 / physical_lower 32260 / physical 48384 / p1_rows 8059 / characters [0,1,2,3] / auxiliary_tests 2` で不変。

---

## 2. (2) 規約表 diff(v9 → v10)

### 2.1 値の規約(**私が登録表から再計算し、C の独立和・実出力と三者照合**)

| 量 | v9 | v10 | P10 の出所(登録表導出) | C10 の出所(**独立**) | 実出力 | 私の再計算 |
|---|---:|---:|---|---|---:|:---:|
| 親 role 数 | 21 | **22** | 登録表 `parent_roles` ≡ `ROLES`(L1191) | `PARENT_ROLES = (*V9_PARENT_ROLES, "batch-parent-v9")`(L54) | 22 | 一致 |
| batch 親層数 n | 6 | **7** | `ROLES[15:]`(L1204) | `V10_CURRENT_PARENT_LAYER_COUNT = 8 − 1`(L583) | 7 | 一致 |
| `previous_parent_batch_rows` | 640 | **768** | 登録表の層和 | `V10_CURRENT_PREVIOUS_BATCH_ROWS`(L578) | 768 | 一致 |
| `total_parent_batch_rows` | 768 | **896** | 同上 | `V10_CURRENT_TOTAL_BATCH_ROWS`(L579) | 896 | 一致 |
| `target_derivation_parents` | 865 | **993** | `ancestry(97) + total` | `97 + 896`(L581) | 993 | 一致 |
| `previous_parent_target_derivations` | 737 | **865** | 同上 | `97 + 768`(L580) | 865 | 一致 |
| acceptance top-level key 数 | 12 | **13** | 登録表 `current_exact_keys.acceptance`(P10 L8463 が `exact_keys(…, "acceptance_thirteen_plain_keys")`) | `6 + 7`(L588)+ 13 名の明示集合(**L1580**) | **13**(私が公刊 acceptance を数えた) | 一致 |
| `parent-intake` key 数 | 73 | **81** | 登録表 | `25 + 8 × 7`(L590) | **81**(私が数えた) | 一致 |
| `start` key 数 | 59 | **64** | 同上 | `34 + 5 × (7 − 1)`(L589) | 64 | 一致 |
| `parent-layout` key 数 | 14 | **15** | 同上 | `acceptance + 2`(L591) | 15(登録表・私は実バイト未取得) | 一致 |
| `candidate_phase_manifests_checked` | 4,608 | **5,376** | `6 × total` | `6 × 896`(L585) | 5,376 | 一致 |
| `checkpoints_checked` | 4,632 | **5,404** | `7 × 772` | `(4 + 6 × 128) × 7`(L586) | 5,404 | 一致 |
| `invocations_checked` | 6 | **7** | 層 `invocations` の和 | `V10_CURRENT_INVOCATION_COUNT`(L587) | 7 | 一致 |
| `native_pairing_rows_rechecked` | [1450…2218] | **[1450,1578,1706,1834,1962,2090,2218,2346]** | 累積 | `V10_CURRENT_NATIVE_PAIRING_ROWS`(L582) | 一致 | 一致 |
| `initial_rank` / `initial_generation` | 2218 / 8923 | **2346 / 9051** | `1450 + total` / `8155 + total` | `SEVENTH_BATCH_RANK`(L523)/ `SEVENTH_BATCH_GENERATION`(L524) | 2346 / 9051 | 一致 |
| selftest 群 | 8 | **9** | `[30,10,6,7,8,8,12,1,29]`(L12320) | `[28,9,6,7,8,10,14,15,20]` | 一致(§6) | 一致 |
| schema | `.v9` | `.v10` | — | — | 全公開 JSON | — |

**私は artifact の `audit-region-registry.json`(15,060,310 B)から `current_count_inputs` を取り出し、P10 の `registered_layer_counts`(L1163-1189)を自分で再実装して上表の「私の再計算」列を埋めた。16/16 一致。** 表の canonical sha も `6f92e487…` = P10 L1126 の literal と一致。
登録表 `current_exact_keys` の要素数(私が数えた): acceptance **13** / parent-intake **81** / start **64** / parent-layout **15** / head 24 / result 48 / checker-result 50 / final-manifest 27 / progress-head 16 / owner 8 / selection 27 / selection-start 19 / separator 12 / source 10 / fixed-manifest 9。

### 2.2 **最大の規約変更 = prefix view の一般化**(v10 の中心)

```
P9r2 require(... len(prefix) == current_count("previous_parent_target_derivations") ...)   # v9: 現行値 = 737
P10  require(... len(prefix) == native_v8_count("previous_parent_target_derivations") ...) # v10: 歴史値 = 737(現行は 865)
```

`NATIVE_LAYER_COUNTS` は登録表の層リストの**各 prefix** に `registered_layer_counts` を適用して作られる(P10 **L1216-1219**)。`native_v8_count`(**L1232-1239**)は `NATIVE_LAYER_COUNTS["batch-parent-v8"]` だけを見せ、`current_exact_keys` / `key_counts` の参照を明示的に禁じる(`native_v8_numerical_scope_only`)。`native_v7_count` は v9 と同じまま残る。
**私は artifact の登録表から 6 層 prefix view を再計算し、2218 / 8923 / 21 / 640 / 768 / 865 / 737 / 6 / 4,608 / 4,632 / [1450…2218] / 6 を得た — v9 正本 §2.1 の現行値表と 1 個残らず一致。** literal を新設したのではなく、同一の pinned 表の別 view を取っただけであることが数値で裏づけられた。
歴史 role view も literal ではなく prefix:`HISTORICAL_V5_ROLES = ROLES[:17]` … **`HISTORICAL_V9_ROLES = ROLES[:21]`**(P10 L45-49)。
C 側も対称に、v9 期の `V9_CURRENT_*` 群を凍結したまま `V10_CURRENT_*` 群を別に定義(C10 L578-591)。v9 期の 12-key acceptance 検査は **`native_v9_acceptance_exact_twelve_plain_keys`(C10 L7150)**として**保持**されている。

### 2.3 公開 JSON key 集合(私が実バイトから数えた)

`acceptance.json` **13**・`output/HEAD` **24**・`result.json` **48**・`checker-result.json` **50**・`selection/start.json` **19**・`parent-intake.json` **81**・`final/manifest.json` **27**・`progress/HEAD` **16**・`owner.json` **8** — **9 文書すべてが登録表の `current_exact_keys` の要素数および C の独立和と一致**(`tree.json` は 14 key で登録表の管轄外)。
**【解消 = F-v9-7】** `run-receipt` の自己申告 key から**版番号が消えた**。v9 の `selection_lambda2218_oracle_is_separate_from_new_final_lambda_oracle` → v10 **`selection_lambda_oracle_is_separate_from_new_final_lambda_oracle`**。私が run-receipt の 94 key を全走査し、**3〜4 桁の数字を含む key は `sha256` だけ**であることを確認した。C 側の設計文書も `new_version_free_ledger_keys: "Only the ninth-group ledger uses stable descriptive names. Historical ledgers retain their original rank/version keys."` と明示している(歴史 ledger を改名しない判断は妥当)。

---

## 3. (3) 群別 PASS(本走の検査群)

| 群 | 何を要求しているか | 結果 | 私の独立確認 |
|---|---|---|---|
| **A. 第 22 親の入場** | 13-key acceptance・`batch_anchor_v9` の記述子が親 artifact と一致 | **PASS** | 公刊 `acceptance.json` の top-level key を私が数えて **13**(`batch_anchor_v9` を含む)。C10 L1580-1581 が同じ 13 名の明示集合を要求。C10 L520-535 の `SEVENTH_BATCH_*` が rank 2346 / gen 9051 / state `fc1ac4d9…` / target `96785516…` / λ `289190c3…` / P 760,214 / C 758,932 / **親 zip の files 12,348 + directories 3,679**(= v9 正本が数えた zip entry 数)を持ち、**v9 正本 §0・§1.1 の値と完全一致**。`run-receipt.accepted_artifacts` は 22 role |
| **B. 親層の累積則** | 128 / 768 / 896・祖先 97 → … → 993・pairing 8 点・層の分割和 | **PASS** | `parent-intake.json`(12,871 B)の実バイトで確認: `previous 768 / total 896 / tdp 993 / old_tdp 97 / pairings [1450,1578,1706,1834,1962,2090,2218,2346] / candidate_manifests 896 / row_manifests 896 / phase 5,376 / checkpoints 5,404 / invocations 7`。`parent_layers` は 7 件で末尾が `batch-parent-v9`(rank 2346・gen 9051・state `fc1ac4d9…`・tdp 865 → 993)。中間記録 1578/8283/225・1706/8411/353・1834/8539/481・1962/8667/609・2090/8795/737・**2218/8923/865** も揃う |
| **C. fresh λ_2346 oracle** | 選定 λ = v9 final λ・state_head = 受理側・roster 128 本 | **PASS** | `selection/start.json`(1,116 B): `selection_lambda_sha256 289190c3…` / `state_head fc1ac4d9…` / `previous_target e1b34dfa…` / `target 96785516…` / `rank 2346` / `generation 9051` / anchor 128 / 768 / 896 |
| **D. current 側 roster の独立再計算** | C が自前で残差選定をやり直す | **PASS** | `checker-stderr.log`(1,381,696 B)に `{"chords": 54433, "failed": 35780, "phase": "fixed_lambda_all_residuals_selected", "selected": 128}` — **P の公刊 `failed_count 35780` と一致**。`tree.json` 実バイト: `residual_nonzero 35780 / first_failed_index 435 / first_failed_edge 847 / fit [2,2,1,1,1] / basis_chords [2,3,4,6,11] / independent_tau_columns 5 / aux_values [0,0] / full_chord_eof true`。`failed-indices.u32` は **143,120 B = 4 × 35,780**(私が entry サイズから割り算した) |
| **E. old 側 oracle** | 35,647 / 242 / 489 が親の実体に結ばれる | **PASS(ただし再測ではない・受領証に明示)** | P は親の保存 `batch_anchor_v9.old_oracle` と literal の突合(P10 **L7095**)、C は同じ object の `same_json`(C10 **L7245**)+ 親の保存 `failed-indices.u32` が **4 × 35,647 B** で先頭要素が `selected[first_field]`(C10 **L7445-7447**)。**どちらも λ_2218 から残差表を再計算してはいない**。**今期はそれが `old_side_recomputed_in_this_run: false` として公刊された**(限定条項 2) |
| **F. 128 行の受理** | 128/128 INDEPENDENT・dependent 0・skipped 0 | **PASS** | `result.json`: `accepted_new_rows 128 / processed 128 / dependent 0 / skipped_after_linear [] / selected_count 128`。`checker-result.json`: `accepted_rows_compared 128 / candidate_decisions_compared 128 / candidate_phases_compared` 128 件 / `selection_phases_compared ["section","cochain","tree"]` / `all_completed_payloads_and_json_compared true / public_final_compared true / partial false / durable_tail null` |
| **G. 鎖と rank** | 2474 = 2346 + 128・gen 9179 = 9051 + 128 | **PASS** | HEAD / result / checker-result / final-manifest / progress-HEAD / run-receipt の 6 文書で `rank 2474 / generation 9179 / state_head 168d2cf1…` が一致(私が実バイトで突合)。`anchor_previous 768 / anchor_total 896 / anchor_accepted 128 / anchor_completed_steps 64`。`progress/HEAD.sequence = 771 = 4 + 6×128 − 1` |
| **H. 予言の非空虚性** | `first_candidate` 5 条件 → INDEPENDENT | **PASS(8 回目)** | `matches_prediction: true` / `expected = observed = INDEPENDENT` / `ordinal 0` / `raw_pairing 2` / `selection_scalar 2` / 5 条件(`candidate_exists` / `first_processing_complete` / `parent_span_zero` / `derived_rho2_one` / `raw_pairing_matches_nonzero_selection`)すべて true。`independence_rate_predicted: false` の自己抑制は維持 |
| **I. UNKNOWN の置き場** | 未計算を 0 と読んでいないか | **PASS** | `new_lambda_oracle: null`・`failure_set_monotonicity_asserted: false`・`independence_rate_predicted: false`・**`old_side_recomputed_in_this_run: false`**・`grade2_member/nonmember = NOT_DECIDED`・`full_A0 false`・`verified false`・`current_run_call_coverage NOT_MEASURED`・`original_rho2_directly_read false`・`positive_readout NOT_APPLICABLE`・`old_success_suites 0`・`old_insert/snapshot_numeric_replays 0`・`historical_payload_reacquired_in_this_run false`・`new_final_q_computed false`・`workshop_CV9: PENDING`。**NONMEMBER 主張は一切していない** |
| **J. 計器(診断)** | 外側 59 区間 / 隣接 2 受領証 / parse 台帳 | **PASS** | §5.7・§7.1 |

---

## 4. 限定条項(**8 条**・v9 から新設 1・**解消 1**)

1. **射程 = rank 2346 → 2474 の 1 batch のみ。** rank 2474 の λ\* に対する oracle は**未計算**(`new_lambda_oracle = null`)。**NONMEMBER 主張ではない。**
2. **a(128) = 128 は roster 前置 128 本の観測**(batch パラメータ k の性質ではない)。消化率 128 / 35,780 = **0.3577 %**。**Task 988 F4 の反例は排除されていない。** 失敗数は今期 **+133** と増加し、8 世代のうち増加は 3 回で**単調減少は成り立たない**。**old λ_2218 の 35,647 は本 run で再測されていない**(親の保存 anchor / 保存 `failed-indices.u32` の長さ・先頭要素との突合まで)— 今期からこれは `old_side_recomputed_in_this_run: false` として**受領証に明示**されている(F-v9-4 の解消)。
3. **算術 TCB は共有カーネル 2 本を含む**(P/C 各 1 で計 4 区間・v9 と集合同一)。`current_run_call_coverage = NOT_MEASURED`・`kernel_third_independence_claimed = false`。**第三独立性はこの 2 本に及ばない。** P1 相が候補時間の **68.6 %**(786.791 / 1,147.134)なので `vectorized_projection_chunk` は確実に load-bearing。
4. **旧 2,346 行の実バイトは私自身は未取得。** λ_new ⊥ 旧行 と ρ₂ の旧行部分は checker の再現に依存する。**ρ₂ は依然 DERIVED**(`original_rho2_directly_read: false`)。「選定 λ_2346 が旧 2,346 行を殺す」ことも本 run で私が再測したわけではない。
5. **harness TCB は単著**(WF 47,555 B + driver 32,326,911 B)。**登録表を書いたのは driver 著者**であり、その値を外部から縛るのは **C の独立和**である(F-v8-2 の継続)。**ただし v10 では第 22 親の descriptor について P source 側の pin(`BATCH_V9_PARENT_FACTS` + `batch_v9_anchor_header` の field 全数突合)が加わったため、この条の射程は第 22 親に関して 1 段狭まった。** また **P は C を file 名でしか pin しない**(P10 L35)。**著者側 public wire 文書の pin は依然形式検査のみ**(`PUBLIC_V10_WIRE` は `is not None` 1 箇所・`public_wire` / `root_adoption` は file 非空 str・bytes>0・sha256 16 進の型検査のみ)。**今期はその限界が機械宣言された**(`public_declaration_scope.declaration_contents_read_in_this_run = false` / `byte_monotonicity_is_semantic_evidence = false`)ことと、**6 本のうち `keysets` 1 本は canonical(登録表 count-inputs)と bytes・sha 一致で実バイトに束縛されている**ことを併記する。**これらの文書は repo 外(著者 temp)にあり、私は中身を読めない。**
6. **checker の相別 timestamp は依然無い。** `cost-receipt.limitations` が自ら「C candidate-phase timestamps are absent from these saved phase receipts … no C residual or P+C unmeasured subtotal inferred」と宣言(v9 と逐語同一)。**F-k64-7 継続。**
7. **私は 448 MB の ZIP を全量ダウンロードしていない**(HTTP Range で必要 entry を個別取得)。ZIP 全体の sha は工房記録に依拠し、自分でバイト再計算していない。**私が sha256 を自分で計算したのは付録 A の 7 対象だけ。** `output/parent-layout.json`(15,411,341 B)と `output/start.json`(580,199 B)、`acceptance.json` の入れ子(top-level key と `batch_anchor_v9` 以外)は読んでいない。
8. **【新設】歴史文書の keyset は両側とも source literal である。** P の `NATIVE_V9_KEYSETS`(P10 L1122・9,102 B)と C の `native_v9_acceptance_exact_twelve_plain_keys`(C10 L7150)の期待値はいずれも**著者が source に書いた literal**で、登録表 prefix view からは導出されていない(数値量とは対照的)。外部拘束は「P と C が独立に同じ 12 / 73 / 59 / 14 を書いたこと」と「親 artifact の実バイトが実際にその key 集合を持つこと」の 2 点のみである。**第 9 群の 8 否定例**(`native-v9-*-with-current-only-key` / `current-v10-*-with-native-v9-keyset` の 2×4)**で試験されている**点は評価する。

### 4.1 前回 8 条との 1 対 1 対応

| v9 の条 | v10 での扱い |
|---|---|
| 1. 射程 1 batch | **継続**(条 1・rank が 2346→2474 に更新) |
| 2. a(k) の意味・F4 未排除・old λ 再測なし | **継続 + 明示化**(条 2)。**「old は再測していない」が受領証 field になった**(F-v9-4 解消)。失敗数は今期 **+133** と再増加 |
| 3. 共有 kernel 2 本 NOT_MEASURED | **継続・集合も不変**(条 3・P1 相の比率 71.4 % → 68.6 %) |
| 4. 旧行の実バイト未取得・ρ₂ DERIVED | **継続**(条 4・旧行数 2,218 → 2,346) |
| 5. harness TCB 単著 + 登録表が値の源 + wire pin は形式検査のみ | **継続・ただし射程縮小**(条 5・第 22 親は P source でも pin・wire の provenance-only が機械宣言・keysets 1 本は実バイト拘束) |
| 6. checker 段別 timestamp 無し | **継続**(条 6) |
| 7. ZIP 全量 DL せず | **継続**(条 7・読んだ entry を明記) |
| 8. P 側に第 21 親の現行値向け否定例が無い | **解消**(§5.8)。P 第 9 群 29 件が現行値 768/896・現行 checker 名と、直前版 640/768・直前 checker 名の**双方向**を撃つ |
| —(新設) | **条 8**(歴史 keyset が両側 source literal) |

**8 条 → 8 条(新設 1・解消 1)。**

---

## 5. 弱化検出(本判読の主目的)

### 5.1 検査 1 — `require` ラベル集合の全数 diff(私の AST 実装)

| 側 | v9r2 のラベル | v10 のラベル | **削除** | 追加 | **出現回数が減ったラベル** |
|---|---:|---:|---:|---:|---:|
| P | 618(呼出 933) | **679(呼出 1,059)** | **5** | 66 | **0** |
| C | 656(呼出 708) | **734(呼出 798)** | **4** | 82 | **0** |

(私の器は `require(cond, "literal")` の第 2 引数が文字列定数の呼出だけを数える。v9 正本の器は別の規約で 655 / 723 を報告したが、**版間の比較は同一の器で行っている**ので結論に影響しない。)

**削除 9 件はすべて版番号の改名であり、対応する v10 側の後継を 1 件ずつ特定した:**

| 側 | v9r2 で消えたラベル | v10 の後継 | 判定 |
|---|---|---|---|
| P | `current_count_six_separate_native_layers` | `current_count_seven_separate_native_layers`(L1204) | 改名 |
| P | `production_requires_exact_twenty_one_roots_acceptance_and_output` | `…_twenty_two_roots_…`(L12441) | 改名 |
| P | `selftest_exact_eight_group_counts` | `selftest_exact_nine_group_counts`(L12320) | 改名 |
| P | `task1184_formal_binding_pending_static_draft` | `task1191_…`(L10427) | 改名 |
| P | `twenty_one_registered_roots` | `twenty_two_registered_roots`(L8471) | 改名 |
| C | `acceptance_exact_twelve_plain_keys` | `acceptance_exact_thirteen_plain_keys`(L1581)。**12-key 版は `native_v9_acceptance_exact_twelve_plain_keys`(L7150)として保持** | 改名 + 歴史版保持 |
| C | `all_twenty_one_roots_and_exact_acceptance` | `all_twenty_two_roots_and_exact_acceptance`(L11102) | 改名 |
| C | `c9_current_root_key_counts_from_independent_sums` | `c10_current_root_key_counts_from_independent_sums`(L8117) | 改名 |
| C | `v9_formal_inventory_and_final_source_binding_pending` | `current_formal_inventory_and_final_source_binding_pending`(L1604・**版番号を外した**) | 改名(版依存を解消) |

**⇒ 消えた検査は 1 件も無い。** `raise` の literal は P 2 → 5(追加のみ・削除 0)、C 2 → 2。

### 5.2 検査 2 — 同名ラベルの**条件式**の diff(改名では隠せない弱化の検出)

v9r2 / v10 で同名かつ 1 回出現のラベルについて `require(...)` の第 1 引数を AST dump で比較。**実差分は P 6 件・C 1 件のみ**、いずれも前進:

| 側 | ラベル | v9r2 | v10 | 判定 |
|---|---|---|---|---|
| P | `batch_v8_737_prefix_plus_128_exact_DERIVED`(L6180) | `current_count(…)` × 3 | `native_v8_count(…)` × 3 | **正しい前進**(§2.2)。値は 737/128/865 で v9 と同一 |
| P | `batch_v8_complete_2218_native_basis_state_and_865_ancestors`(L6736) | `current_count(…)` × 3 | `native_v8_count(…)` × 3 | 同上(2218 / 64 / 865) |
| P | `batch_v8_preserves_five_original_parent_layers`(L6752) | `current_count("parent_layer_count") − 1` | `native_v8_count(…) − 1` | 同上(6 − 1 = 5。role 名の literal 5 本は不変) |
| P | `new_lambda2218_direct_all_rows_parent_start_and_final_targets`(L6741) | `current_count("initial_rank")` | `native_v8_count("initial_rank")` | 同上(2218) |
| P | `batch_v8_internal_prior_view_exact_twenty_one_roles`(L6154) | `== list(ROLES)` | `== list(HISTORICAL_V9_ROLES)` | **正しい前進**。`ROLES` が 22 になったため v8 の 21-role prior view を固定。`len == 21` の要求は残存 |
| P | `separate_selftest_process_modes`(L12427) | `not (args.selftest and args.key_contract_selftest)` | `sum((args.selftest, args.key_contract_selftest, args.selftest_parent2346_contract_child)) <= 1` | **強化**。旧 2 変数に限れば論理的に同値で、第 3 の mode に対する排他が加わった |
| C | `batch_observation_independently_measured_parent_conditions` | `pairing["rows"] == SIXTH_BATCH_RANK` | `== SEVENTH_BATCH_RANK` | 正しい前進(2218 → 2346) |

**⇒ 条件式の緩和は 1 件も無い。** P の 5 件は「現行値を読んでいた歴史ブロックを歴史値へ向け直した」もので、**私は登録表から 6 層 prefix view を再計算して v9 の実測値と完全一致することを確認した**(§2.2)ため、値の書き換えによる誤魔化しではない。

### 5.3 検査 3 — **全 helper のラベル対の多重集合 diff**(`require` 以外の検査の削除も捕まえる)

`require` だけでなく `exact_keys` / `same_json` / `integer` / `pair` / `k128_reject` / `current_count` / `native_v*_count` 等、**ラベル様の文字列定数を引数に取る全 Call** を (関数名, ラベル) の多重集合として比較した。

| 側 | 対の数 | 呼出総数 | 消えた対 | **減った対** |
|---|---:|---:|---:|---|
| P | 691 → **766** | 1,071 → **1,228** | **6**(§5.1 の 5 件 + `exact_keys(acceptance_twelve_plain_keys)` → **`acceptance_thirteen_plain_keys`**(L8463)) | **4** |
| C | 1,059 → **1,199** | 1,156 → **1,319** | **4**(§5.1 と同じ) | **0** |

P の「減った対 4」は **`current_count(accepted_parent_batch_rows)` 11→10・`current_count(previous_parent_batch_rows)` 6→5・`current_count(total_parent_batch_rows)` 6→5・`current_count(upstream_completed_steps)` 6→5** で、**新設 `native_v9_final_parent_counts`(P10 L1266-1272)が同じ 4 対を `native_v8_count` で読むようになった分**である(`current_final_parent_counts` L1257-1263 は現行文書用に残存)。**登録表由来の呼出総数は 104(current 67 + v7 37)→ 142(current 64 + v7 37 + v8 41)と増えている。**

**⇒ 検査の削除 0・緩和 0・実質減少 0。**

### 5.4 検査 4 — **定義単位の全数 inventory diff**(逆置換検問の代替。v10 は修理版が無いので版間 diff が検問になる)

| 側 | 定義数 | **削除** | byte 同一 | 変更 | 追加 |
|---|---:|---:|---:|---:|---:|
| P | 304 → **330** | **0** | **287** | 17(**+2,770 B・すべて増加または ±0**) | 26(91,271 B) |
| C | 324 → **352** | **0** | **304** | 20(**+5,516 B・すべて増加または ±0**) | 28(99,146 B) |

- **変更 17 / 20 本のうち、byte が減ったものは 1 本も無い**(最小は ±0 の `production_key_contract_child` / `main`)。
- **module 直下の代入**: P 95 → 106(**削除 0**・追加 11 = 179,554 B・変更 5 = **+2 B**)、C 135 → 163(**削除 0**・追加 28 = 5,949 B・変更 6 = **−29 B**、内訳は `PRODUCER_FILE` −9 / `CURRENT_PRODUCER_REGISTRATION` −3 等の識別子 literal のみ)。
- **10 領域の原文同一**(Astra 内訳の検証): `canonical` / `seal` / `check_seal` / `json_bytes` / `read_json` / `sha` / `require` / `integer` / `same_json` / `file_pin` の **10 本すべてが source segment の sha256 まで一致**。
- **最適化の未導入**: P10 に `lru_cache` / `functools.cache` / `@cache` / `_CACHE` / `_cache` は **0 件**。**import 集合は P/C とも v9r2 と 1 行も違わない**(私が import 行を diff した)。canonical の重複除去・述語の短絡最適化に相当する変更は定義 diff にも現れていない。

### 5.5 検査 5 — **Astra 内訳票(裁定 2297)の独立確認**

私の会計(定義境界 = `ast.get_source_segment`):

```
P10 − P9r2 = 1,034,265 − 760,214 = +274,051 B
            = 180,010(module 直下)+ 91,271(追加定義 26 本)+ 2,770(変更定義 17 本)
追加 26 本の内訳 = 19(native-v9 ordinary reader)67,586
                 + 2(第 9 群 child + canary)22,018
                 + 5(count/key/identity/oracle helper)1,667
```

Astra 票との対応:

| 区分 | Astra | 私 | 差 | 説明 |
|---|---:|---:|---:|---|
| 登録定数/名前空間 | 179,854 | 180,010 | −156 | 定義直前のコメント/空行の帰属差 |
| native-v9 ordinary reader 19 本 | 67,647 | 67,586 | +61 | 同上 |
| count/key/identity 5 本 | 1,682 | 1,667 | +15 | 同上(私の 5 本 = `native_v8_count` / `native_v9_final_parent_counts` / `native_v9_checker_entry_identity` / `native_v9_key_contract` / `batch_v9_uncomputed_final_oracle`) |
| 第 9 群と canary | 22,025 | 22,018 | +7 | 同上 |
| 純増 | 2,843 | 2,770 | +73 | 同上(私の「純増」= 変更定義 17 本の delta) |
| **合計** | **274,051** | **274,051** | **0** | **完全一致** |

**⇒ Astra 票は本数の区分(19 / 2 / 5 = 26)まで私の区分と一致し、byte も合計 0 差・区分ごと最大 156 B(0.06 %)の境界差のみ。** 「canonical / seal / check_seal / json_bytes / read_json 等 10 領域は原文同一」「canonical 重複除去 / cache / 述語最適化は未導入」も §5.4 で独立に確認した。
**【記帳・分類の注意】** ただし「登録定数/名前空間 179,854」の **87 %(156,222 B)は `BATCH_V9_PUBLIC_HEADER_FIXTURE`** で、**その唯一の参照は第 9 群 child の positive fixture(P10 L12057)**である。production 側の登録定数の増加は残り約 23,300 B に過ぎない。**第 9 群の総費用は 186,871 B = 増分の 68.2 %** であり、「v10 の肥大は第 22 親の reader が主」と読むと誤る。

### 5.6 検査 6 — **19 reader が第 22 親の必須経路であること**(selftest-only クローンの排除)

私は AST で呼出元(囲む関数)を全数抽出した。

- `authenticate_batch_v9_parent`(17,559 B)は **直接呼出 0・ただし `authenticate_acceptance` L8531 で `authenticate_parent_with_parser_bytes("batch-parent-v9", 6, admission, authenticate_batch_v9_parent)` として callable で渡される**(v8 親は L8528 で同型)。**本走の必須経路。**
- `promote_batch_v9_anchor`(8,688 B)← **`run_actual` L10471**。
- `batch_v9_prior_admission` ← `authenticate_acceptance` L8514 / 8518 / 8522 / 8525 / 8528(5 箇所)。
- 残る 16 本はすべて `authenticate_batch_v9_parent` / `promote_batch_v9_anchor` / `batch_v9_saved_*` の内部から呼ばれる(例: `batch_v9_saved_rows` ← L7808、`batch_v9_saved_parent_intake` ← L7710、`batch_v9_saved_checkpoints` ← L7821、`batch_v9_ancestry_count/records` ← L7810/7811、`batch_v9_document` は 11 箇所)。
- **第 9 群 `parent2346_contract_child.exercise` は同じ関数群を呼ぶ**(L12079-12101 で `batch_v9_old_input_projection` / `batch_v9_source_binding` / `batch_v9_previous_target_binding` / `batch_v9_inventory_registration` / `batch_v9_anchor_header` / `batch_v9_fixed_local_layout` / `batch_v9_uncomputed_final_oracle`、L12141-12147 で `native_v9_final_parent_counts` と `current_final_parent_counts`、`native_v9_checker_entry_identity` と `current_checker_entry_identity`、`native_v9_key_contract` と `current_key_contract`)。**クローンではなく production 関数そのものを否定例に当てている。**
- C 側の裏づけ: 公刊 `checker-selftest-stdout.json.production_interfaces_used` に `check_seventh_native_parent_projection` … `check_v10_current_anchor_batch_counts` / `check_current_batch_observation_header` が並び、P 側は `authenticate_acceptance` / `read_json` / `check_seal` 等を列挙している。

### 5.7 検査 7 — 計器 3 本が判定経路に触れていないこと(telemetry only)

**source 側**(driver):
- `record_outer_parent_timing` は全体が `try/except` で、失敗時は stderr に `original_operation_result_not_replaced: true` の 1 行を書くだけ。**包まれた演算は block の外**(`timed_parent_call` が `value = operation()` を先に実行し、**その後**に計時を記録する)。
- `check_v10_adjacent_timing_receipt`(L17111-)は **受領証が無ければ `None` を返す**(失敗しない)。存在する場合に要求するのは `canonical(value) == canonical(seal(…collect…))` すなわち**再導出の決定性のみ**で、`status` が PASS であることは要求しない。
- `collect_v10_adjacent_timing`(L17087-)は status を `COMPLETE_MEASURED_SCOPE` / `PARTIAL_OR_UNAVAILABLE` のどちらでも返し、`'missing_receipt_or_event_is_mathematical_failure': False` を自ら書き込む。

**受領証側**(私が実バイトから読んだ):

| 受領証 | bytes | 自己申告 |
|---|---:|---|
| `parent-timing-receipt.json` | **6,853,867** | `status PASS` / `outer_expected_count 59` / **`outer_intervals` 59 件すべて `OBSERVED`** / `errors []` / `causal_mechanism_identified false` / `mathematical_success_inferred false` / `inclusive_intervals_added_together false` / `all_original_stderr_bytes_retained true` / `candidate false` / `cross_checked false` / `verified false` |
| `parent-authentication-timing-receipt.json` | **8,648,780** | `kind authentication` / `COMPLETE_MEASURED_SCOPE` / P 7 events・C 54 events / 4 抑制 flag(`missing_receipt_or_event_is_mathematical_failure` / `unattributed_time_renamed_seal` / `inclusive_and_exclusive_intervals_added` / `whole_envelope_bytes_inferred_from_operation_scope`)すべて false / 側別に `arithmetic_success_inferred false` / `unobserved_values_filled_with_zero false` / `partial_counter_addition_identities_asserted false` / `operations_added_to_inclusive_native_seconds false` |
| `native-metadata-operations-receipt.json` | **8,625,964** | `kind operations` / `COMPLETE_MEASURED_SCOPE` / P 7 events・C 14 events / 同上の抑制 flag |

外側 59 区間の内訳(私が数えた): **live-parent 22 + intake-inventory 22 + native-intake 8 + directory-restoration 7 = 59**、4 stage すべてに `batch-parent-v9` が入っている(driver `OUTER_PARENT_TIMING_STAGES` L10980-10984 の登録と一致)。**v9 repair-v1 で起きた「新親の計時区間が未登録で例外」型(裁定 2286)の再発は無い。**
C 側 `bytes_accounted = 1,381,696` は `checker-stderr.log` の entry サイズと完全一致(`whole_stderr_EOF_after_pin true`)。
**⇒ 3 計器はいずれも判定経路に触れていない。** `run-receipt` は 3 本を pin(6,853,867 / 8,648,780 / 8,625,964)するが、その `status` を gate にしてはいない。

### 5.8 検査 8 — 空虚性(第 9 群の否定例が実通過したか・**F-v9-3 の解消判定**)

P 第 9 群 `batch-parent2346-seven-layer-and-current-contracts`(**29 件**)を逐語で読んだ(child = P10 L11966-12224、canary = L12225-12292)。非空虚性の根拠は 6 点:

1. **production 束縛が本物**: child は `require(CURRENT_KEY_CONTRACT is True, "parent2346_child_actual_production_binding")`(L11975)で実登録表を production で束縛し、親は起動前(L12231 `parent2346_parent_keeps_original_nonproduction_binding`)と回収後(L12291 `parent2346_parent_binding_never_changed`)の 2 回、自分が非 production であることを確認する。子は登録表と交わらない root を要求する(`parent2346_child_disjoint_registry`)。
2. **正例が先に通ることを確立**: 各 case で `exercise(case, positive, positive_name)` を**負例より前に**実行する(L12129 相当)。**「何にでも当たる試験」ではない。**
3. **分離条件(ダミー検査)**: 正例・負例の**両方**に `check_seal` を当て(L12176-12177・コメント「Observations of the generic seal are separate from the ordinary schema/key gate below」)、落ちる理由が seal ではなく key/schema gate であることを特定する。
4. **no-op guard**: `require(canonical(changed) != canonical(original), "parent2346_saved_mutation_not_noop")`(L12172)、識別子変更系は `parent2346_identity_mutation_not_noop`。
5. **期待エラーの完全一致 + fail-closed**: `require(observed == "fixed_lambda_batch:" + expected, "parent2346_exact_ordinary_refusal_path")`(L12182)。拒否しなければ `raise ValueError("parent2346_canary_did_not_reject:" + name)`(L12184)。
6. **事後不変**: `require(len(rejected) == 29 and rejected == [case["name"] for case in NINTH_CASE_SPECS] and CURRENT_KEY_CONTRACT is True and inventory(positive) == positive_before, "parent2346_twenty_nine_rejections_and_positive_full_inventory_unchanged")`(L12205-12207)、`parent2346_source_and_registry_after_pins`(L12208-12209)。canary 側は子の stdout の封・16 key 完全集合・`positive_normal_read` / `positive_raw_unchanged` が True・`actual_parent_arithmetic` が False・source/registry pin の前後不変を要求する(L12281-12290)。

**F-v9-3 が要求した「直前版 512/640 と直前 checker 名を狙う明示負例」は、v10 の値へ平行移動して両方向とも実在する:**

| case 名 | gate | 狙い |
|---|---|---|
| `current-v10-previous768-as-native640` | `current_final_previous_and_total_parent_rows` | **現行 768 を直前版 640 に差し替える**(v9 で欠けていた型) |
| `current-v10-total896-as-native768` | 同上 | **現行 896 を直前版 768 に** |
| `native-v9-previous640-as-native512` | 同上 | 歴史 640 を 512 に |
| `native-v9-total768-as-native640` | 同上 | 歴史 768 を 640 に |
| `current-v10-checker-as-v9-repair2` | `current_independent_checker_entry_identity` | **現行 checker 名を直前 checker 名(v9_repair_v2)に** |
| `native-v9-checker-as-v8` | 同上 | 歴史 checker 名を v8 に |
| `current-v10-previous-count-bool` / `native-v9-previous-count-bool` | 同上 | bool を int と読む型混同 |

C 第 9 群 `batch-parent2346-seven-layer-admission`(**20 件**)は `omit-v8-from-native21-projection` / `alias-v9-local0-to-v8`…`-v3`(6 件)/ `drop-zero-from-complete993` / `previous-from-v9-start-previous` / `lambda-source-is-completed-selection` / `registered-empty-directory-missing` / `uncomputed-oracle-is-zero` / `current-field-in-native73-intake` / `current-previous-batch-count-is-stale` / `current-total-batch-count-is-stale` / `current-schema-in-native73-intake` / **`current-checker-is-v9-repair2`** / **`old-side-recomputed-is-true`** / **`old-side-recomputed-is-integer-zero`** / **`old-side-recomputed-field-missing`**。**太字 4 件は今期の前件そのものの否定形**である。C 側の設計宣言も `positive_before_negative`(「正例を先に同じ helper で通す・宣言した 1 箇所だけを変異させる・正負両方の seal を検証・ラベルが違えば・落ちなければ・余分な変異があれば失敗」)を明記している。
**非対称は残るが向きが逆になった**: P 29 / C 20 で、P 側が現行・歴史の両方を撃つ。`run-receipt.selftest_group_scopes` に **`"one-side-specific-ninth-metadata-group"`** が**事前登録**されている。

---

## 6. selftest(**9 群**・件数は実 stdout から私が数えた)

| 側 | 群 | 件数(**stdout 実数**) | driver 登録 | run-receipt | 判定 |
|---|---|---:|---:|---:|---|
| P | `k128-version-registration-and-types` | **30** | 30 | 30 | PASS |
| P | `k128-full-roster-cutoff-and-restoration` | **10** | 10 | 10 | PASS |
| P | `batch-parent1578-admission-and-projection` | **6** | 6 | 6 | PASS |
| P | `batch-parent1706-two-layer-admission` | **7** | 7 | 7 | PASS |
| P | `batch-parent1834-three-layer-admission` | **8** | 8 | 8 | PASS |
| P | `batch-parent1962-four-layer-admission` | **8** | 8 | 8 | PASS |
| P | `batch-parent2090-five-layer-admission` | **12** | 12 | 12 | PASS |
| P | `production-registered-key-contract` | **1** | 1 | 1 | PASS(v9 と逐語同一) |
| P | **`batch-parent2346-seven-layer-and-current-contracts`** | **29** | 29 | 29 | PASS(**新設・F-v9-3 の解消**) |
| C | `k128-version-registration-and-types` | **28** | 28 | 28 | PASS |
| C | `k128-full-roster-cutoff-and-restoration` | **9** | 9 | 9 | PASS |
| C | `batch-parent1578-admission-and-projection` | **6** | 6 | 6 | PASS |
| C | `batch-parent1706-two-layer-admission` | **7** | 7 | 7 | PASS |
| C | `batch-parent1834-three-layer-admission` | **8** | 8 | 8 | PASS |
| C | `batch-parent1962-four-layer-admission` | **10** | 10 | 10 | PASS |
| C | `batch-parent2090-five-layer-admission` | **14** | 14 | 14 | PASS |
| C | `batch-parent2218-six-layer-admission` | **15** | 15 | 15 | PASS(v9 と同数) |
| C | **`batch-parent2346-seven-layer-admission`** | **20** | 20 | 20 | PASS(**新設**) |

- **三系一致**: 実 stdout の `rejected_cases` 実数 = driver の `SELFTEST_REJECTIONS` / `NEW_/SIXTH_/SEVENTH_/EIGHTH_/NINTH_METADATA_SELFTESTS` 登録値 = `run-receipt.new_selftest_rejections_registered` = `{"producer-selftest":[30,10,6,7,8,8,12,1,29], "checker-selftest":[28,9,6,7,8,10,14,15,20]}`。**P 111 + C 117 = 228 拒否**(v9 は 82 + 97 = 179)。`run-receipt.new_selftest_groups_registered = {"producer": 9, "checker": 9}`。
- **P 側に第 21 親(2218)の admission 群は今期も無い**(第 8 群は key 契約 1 件のまま)。ただし v9 期の値 640/768 と v9 checker 名は **P 第 9 群の `native-v9-*` 6 件**が撃つ(§5.8)。
- **gate 一致**: `producer-selftest-gate.json` = `new_mathematical_selftest_groups 2` + `new_parent_metadata_selftest_groups 6` + `new_production_key_metadata_selftest_groups 1` = **9**、`ninth_fixture_gate` 58,648 B、`eighth_fixture_gate` 3,200 B(v9 と同値)。`checker-selftest-gate.json` = 2 + 7 + 0 = **9**、`ninth_fixture_gate` 25,495 B。
- **metadata canary**: `metadata-gate.json` の `metadata_regression_cases: 16`・exit 0・`run-receipt.metadata_regression_cases_registered: 16`。**v7 / v8 / v9 と同数・継続。**
- **in-run 実行の証拠**: `producer-exit-code.txt` / `checker-exit-code.txt` / `producer-selftest-exit-code.txt` / `checker-selftest-exit-code.txt` / `metadata-exit-code.txt` / `driver-bootstrap-exit-code.txt` の **6 本すべてが `0`**(私が実バイトで確認)。selftest stdout の `schema` は `d972.r07.fixed-lambda-cycle-batch.v10.selftest`、`status PASS` / `candidate false` / `cross_checked false` / `verified false` / `actual_anchor_arithmetic_replayed false` / `old_success_suites 0`。公開 selftest 版の分岐は今期も生じていない。

---

## 7. 格付け提案

**CV-9 = 同一対象(SAME OBJECT)・限定 8 条 → 工房格付け案: checker PASS / cross-checked(限定 8 条)・rank 2474 / gen 9179(state_head `168d2cf1004ee6ace61fd082dedb21af41ff1047cf3a88482ed8170ad81786f9`・run 34731988156 / attempt 1)を受理・`verified=false`・GRADE2 NOT_DECIDED・`full_A0=false`・A0 actual 0/1 不変。v9 の rank 2346 の直系後継として置き換える(合算ではない)。**

**司令塔への一行**: v10 の前件は **5 件中 4 件が解消**した — **F-v9-3 解消**(P 第 9 群 29 件が新設され、現行 768/896 と現行 checker 名を直前版 640/768・v9 checker 名に差し替える**明示負例**が、正例先行・正負両 seal 検証・no-op guard・期待エラー完全一致・fail-closed の分離条件つきで実通過)、**F-v9-4 解消**(`old_side_recomputed_in_this_run: false` が P の公刊 observation に入り、C が 7-key 完全集合と `is False` を要求し、C 第 9 群に 3 否定例)、**F-v9-5 解消**(`shared-tcb.json.current_execution_edges` に子プロセス 2 辺が source pin・env allowlist・deadline・非 production 親束縛つきで登録)、**F-v9-7 解消**(run-receipt から版番号入り key が消えた)、**F-v9-8 解消**(in-run pin 32 行の 1 行目が現行 WF)。**F-v9-2 のみ継続だが射程は縮小**(wire の provenance-only が機械宣言され、`keysets` 1 本は canonical で実バイト拘束)。**第 22 親 batch-parent-v9 は 13-key acceptance で入場**(私が公刊 acceptance の top-level key を数えて 13・親は v9 正本が受理した object そのもの)。**fresh λ_2346 は current 35,780 / old 35,647 として正しく記録**され current 側は C が独立に 35,780 / selected 128 を再計算(`failed-indices.u32` = 4 × 35,780 B)。**弱化は 1 件も検出できなかった** — 定義削除 0・module 定数削除 0・ラベル削除は版番号改名 9 件のみ(全件後継を特定)・条件式の緩和 0・helper 呼出の実質減少 0・**v9r2 の 304 定義のうち 287 が byte 同一**・10 領域(canonical / seal / check_seal / json_bytes / read_json / sha / require / integer / same_json / file_pin)は原文同一・import 集合不変・cache や重複除去の導入 0。**Astra 内訳票は合計 274,051 B で私の会計と完全一致**(区分ごと最大 156 B の境界差のみ)。残す宿題は **F-v9-2 の残り**と、**新設の限定条項 8(歴史 keyset が両側 source literal)**。

### 7.1 診断(**gate ではない** — 裁定 2225 / memory「cost-extrapolation-needs-math-review」)

- 実測: producer **1,601.351 s**(cap 5,400 の **29.7 %**)/ checker **1,817.972 s**(cap 10,800 の **16.8 %**)/ P+C **3,419.323 s**。P 残差 **442.865 s**(v9 は 463.278)。run 全体 71 分 43 秒。
- **【重要・交絡】本 run は v9 より一律に速い**: P total −15.4 % / C total −16.8 % / p1 相 −22.2 % / primal −16.1 % / selection −14.8 %。**層が 1 つ増えたのに P 残差は 20.4 s 減った**(v9 までの層あたり増分は +42.3〜+49.9 s)。**したがって本 run から「層費用が下がった」とも「モデルが外れた」とも言えない。工房の `model_fixed_128_7 = 499.608` との差 −56.74 s は runner 速度差で説明可能であり、費用モデルの更新・外挿は本判読では行わない**(次数の確定は数学者の領分)。
- 候補相の内訳: p1 **786.791 s(68.6 %)**/ primal 257.940 / reduction 46.068 / source 30.323 / raw 14.346 / B 11.666。**律速は 10 run 連続で P1 補正相。**
- phase counts: 6 相すべて 128 / 128、final 1 / 1、selection 3 / 3、processed 128。
- 7 層の parse 台帳(私が checker-stderr の JSON 行を全数 parse): 14 観測すべてで **`parse_attempts = unique_documents = successful_parses = 128`・`failed_parses = 0`**。
- C の `ordered_reduction_elements`: 193,728 / 210,112 / 226,496 / 242,880 / 259,264 / 275,648 / **292,032**。**v7 判読の厳密式 `128·R + 8,128` が 7 点目(R = 2218)も的中。**

### 7.2 v11 の前件として裁定に載せるべき所見 F-v10-*

| 札 | タグ | 内容 |
|---|---|---|
| **F-v10-1** | 【解消・記録】 | **identity 5 点一致を確認**: P10 `WORKFLOW`(L9526)= C10 `CHECKER_WORKFLOW`(L56)= repo WF path = WF 内 `WF_FILE`(L190)= run の `launch.workflow` = `…-v10.yml`。加えて **WF 名 `…-v10-envelope-v1` と artifact 名 marker `…-v10-candidate-34731988156-1`**(WF L620)も一致。C10 は P10 を bytes 1,034,265 + sha `33c4bbb9…` で pin(私の実測と一致)。**v11 でも改名を伴う版では発射前に 5 点の機械照合を lane に残すこと**(裁定 2286 の再発防止) |
| **F-v10-2** | **【要修正・継続(F-v9-2 の縮小版)】** | **著者 public wire の pin は依然形式検査のみ。** `PUBLIC_V10_WIRE` は driver L10327 の `is not None` 1 箇所、`v10_adjacent_public_contract` は `source` と新設 `provenance_scope` 以外を型検査しかしない。**前進 2 点**: ①`public_declaration_scope` が「宣言の中身は本 run で読んでいない / bytes 単調性は意味論的証拠ではない」と機械宣言され公刊 `shared-tcb.json` に入った(v9 正本が提示した「provenance のみと正直に改名」側の採用)②wire 6 本のうち `keysets`(12,401 B / `6f92e487…`)は canonical(登録表 count-inputs)と一致し実バイトに束縛されている。**v11 では残り 5 本(P_timing / C_timing / producer_interface / 両 final_adoption)についても、in-run で読むか bytes 単調性を検査するか、entry 名を provenance-only と明示すること** |
| **F-v10-3** | 【解消】 | **F-v9-3**: P 第 9 群 29 件(現行 768/896・現行 checker 名 ↔ 直前版 640/768・v9 checker 名の**双方向**否定例)。非空虚性 6 点(§5.8)。**両側で現行値 stale を撃つ対称性は回復した** |
| **F-v10-4** | 【解消】 | **F-v9-4**: `batch_observation.old_side_recomputed_in_this_run: false`(P10 L10145)+ C の 7-key 完全集合と `is False`(C10 L7922-7926)+ C 第 9 群 3 否定例。**old 側は依然「親の保存バイトとの突合」までであり、その事実が受領証で名指しされた** |
| **F-v10-5** | 【解消】 | **F-v9-5**: `shared-tcb.json.current_execution_edges` 2 本(key 契約 child / parent2346 child)。source pin・env allowlist 16+2・`additional_child_budget_seconds: 0`・親は非 production・`mathematical_third_independence_claimed: false` |
| **F-v10-6** | 【解消】 | **F-v9-7**: run-receipt の 94 key に版番号入りは 1 つも無い(`selection_lambda_oracle_is_separate_from_new_final_lambda_oracle`)。歴史 ledger は原名を保持する方針も明示 |
| **F-v10-7** | 【解消】 | **F-v9-8**: `driver-bootstrap-stdout.log` 32 行の 1 行目が現行 WF `…-v10.yml: OK`。in-run pin に現行 WF が入った |
| **F-v10-8** | **【要修正・新設】** | **歴史文書の keyset が両側 source literal**(限定条項 8)。P `NATIVE_V9_KEYSETS`(9,102 B)/ C の native_v9 期待値は登録表 prefix view からの導出ではない。**v11 では歴史 keyset も登録表 prefix view(`current_exact_keys` の世代別 snapshot)から導くか、少なくとも「literal であること」を受領証に 1 行書くこと** |
| **F-v10-9** | 【記帳・新設】 | **byte 内訳の分類に注意**: 「登録定数/名前空間」179,854 B の **87 %(156,222 B)は第 9 群 child の positive fixture `BATCH_V9_PUBLIC_HEADER_FIXTURE`**(参照は P10 L12057 の 1 箇所のみ)。**第 9 群の総費用は 186,871 B = v10 増分の 68.2 %**。v11 の内訳票では fixture を selftest 側に分類すること(production 定数の増加と読み違える余地を消す) |
| **F-v10-10** | 【一次データ・射程】 | **失敗数が再び増加**(35,647 → **35,780**・今期 net **+133**)。8 世代の推移 36,274 / 36,104 / 36,002 / 35,921 / 36,000 / 36,107 / 35,647 / 35,780、隣接差 −170 / −102 / −81 / +79 / +107 / −460 / +133 で**増加は 3 回**。**単調減少は成り立たない。** 残工程見積りを roster サイズで語る記述は台帳・地図から外したままにすること |
| **F-v10-11** | 【診断・要注意】 | **本 run は v9 比で P −15.4 % / C −16.8 % / p1 −22.2 % 速く、層が増えたのに P 残差は −20.4 s。** 層あたり費用の系列比較は runner 速度で交絡。**費用モデルの更新・外挿は禁止**(§7.1)。v11 では同一 runner 種別の記録(`runtime-observation` に CPU 型など)を 1 行足せば交絡を切れる |
| **F-v10-12** | 【軽微・継続(F-v8-2)】 | **P は C を file 名でしか pin しない**(P10 L35)。C → P は bytes+sha。非対称は 4 版連続で不変。ただし第 22 親の descriptor は P source(`BATCH_V9_PARENT_FACTS`)でも pin されるようになり、この条の射程は 1 段狭まった |
| **F-v10-13** | 【軽微・継続(F-k64-7)】 | **C の相別 timestamp は依然無い。** `cost-receipt.limitations` の宣言は v9 と逐語同一 |
| **F-v10-14** | 【今期は非該当】 | v10 系譜は 1 run のみで **rank 2474 の sealed object は 1 つ**。rank の引用に state_head を併記する運用は継続すること |
| **F-v10-15** | 【軽微・継続】 | **F-v5-2 / F-v5-3 / F-v5-4**: fixture 被覆窓・envelope 履歴・`basis-tau.u8` の二重索引(`basis_chords [2,3,4,6,11]` は今期も受領証に規約が未明示) |

---

## 付録 A. 私自身が sha256 を計算した対象

| 対象 | bytes | sha256 |
|---|---:|---|
| `search/d972_r07_fixed_lambda_cycle_batch_v10.py` | 1,034,265 | `33c4bbb97313bc1ea2017b6ac6ad2cc0932ae15d1affc8bcd6a8aaedd0c76085` |
| `search/check_d972_r07_fixed_lambda_cycle_batch_v10.py` | 870,249 | `a21fd2b54958f84ea67e7b3a079893cff70544961005d6c79a0f6ff47e752ca8` |
| `search/d972_r07_fixed_lambda_cycle_batch_v10_workflow_driver_v1.py` | 32,326,911 | `acf206e5fe423288f3449e5e034a1bd125a6c203e6c274b64f41fc36ab94c802` |
| `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v10.yml` | 47,555 | `88856a3329ccb59750c427fd27ba6857d89953b75a65f93a11f260783f67f34a` |
| artifact `audit-region-registry.json` | 15,060,310 | `bff0d81b71c606117ecfed87f7993e2b800af1e278ddc6bac8c86be8cc4a6d4b` |
| その canonical `new_source_audit.current_count_inputs` | 12,401 | `6f92e487d6190ac36c00b40392a1082d9854032af4fbade4f2e30d9ad7126c00`(= P10 L1126 の literal・= `PUBLIC_V10_WIRE.keysets` の pin) |
| artifact `acceptance.json` | 17,819,829 | `9b7b2188a8d0edee63a1db9f17d7e430f7653f437ab5cd74d8f0e25b3e1e4f0c` |

参考(比較元として repo 側で実測・**v9 正本 §1.1 と完全一致**): `…batch_v9_repair_v2.py` 760,214 / `99cefc6c…`・`check_…_v9_repair_v2.py` 758,932 / `66132850…`・`…repair_workflow_driver_v2.py` 16,522,905 / `d57d5ece…`・`…-v9-repair-v2.yml` 42,858 / `492f5bf2…`。

私が実バイトを取得して読んだ artifact entry(sha は上表の 3 本のみ自分で計算): `output/HEAD` 1,258・`output/result.json` 208,957・`checker-result.json` 15,974・`cost-receipt.json` 380,696・`output/final/manifest.json` 1,926・`output/owner.json` 1,053・`output/progress/HEAD` 837・`output/selection/start.json` 1,116・`output/selection/tree/tree.json` 431・`output/parent-intake.json` 12,871・`run-receipt.json` 1,163,073・`shared-tcb.json` 22,386・`runtime-observation.json` 428・`metadata-gate.json` 875・`producer-selftest-gate.json` 1,859・`checker-selftest-gate.json` 1,852・`producer-selftest-stdout.json` 7,174・`checker-selftest-stdout.json` 7,685・`driver-bootstrap-stdout.log` 3,094・exit code 6 本・`checker-stderr.log` 1,381,696・`parent-timing-receipt.json` 6,853,867・`parent-authentication-timing-receipt.json` 8,648,780・`native-metadata-operations-receipt.json` 8,625,964・`audit-region-registry.json` 15,060,310・`acceptance.json` 17,819,829。`output/selection/tree/failed-indices.u32` は entry サイズ **143,120 B** のみ(= 4 × 35,780)。

## 付録 B. 判読者の限界(正直な申告)

- 旧 2,346 行の実バイトを取得していないので、λ_new ⊥ 旧行 と ρ₂ 恒等式の旧行部分は checker の再現に依存している(限定条項 4)。
- **本判読は増分規律に従い、「128 行の階段形・λ の後退代入 48,384 座標・target 恒等式 128 段・rolling 鎖 128/128」の全数再計算を今期も行っていない。** 本書が実測で閉じたのは付録 A の対象・登録表からの導出 16 量(current view)+ 12 量(v8 prefix view)+ 11 量(v7 prefix view)・公刊 JSON の key 数 9 種・計器の外側 59 区間 + 隣接 2 受領証 + parse 台帳 14 観測 + ordered reduction 7 点・selftest 228 件・`require` ラベル diff(全数)・条件式 diff(同名単一ラベル全数)・**全 helper のラベル対 diff(全数)**・**定義単位 inventory diff(全数)**・**module 代入 inventory diff(全数)** である。**したがって「算術が正しい」ことの本期の根拠は C の PASS と §3 の群別確認であり、私の再計算ではない。**
- old λ_2218 の残差表を私自身は再計算していない(限定条項 2)。
- 著者側 public wire 文書(`C:/…/task1191/…`)は repo 外にあり中身を読めない。私が確認したのは driver がそれらを**形式検査しかしていない**ことと、`keysets` 1 本が canonical で拘束されていることだけである(F-v10-2)。
- `output/parent-layout.json`(15,411,341 B)と `output/start.json`(580,199 B)、`acceptance.json` の入れ子(top-level key と `batch_anchor_v9` 以外)、`fixture-baselines/P.json`(295,699 B)/ `C.json`(685,563 B)は読んでいない。`parent-layout` の 15 key は登録表と C の独立和による。
- `sparse_adjoint` / `vectorized_projection_chunk` が本 run の実行経路で呼ばれた行は特定していない。
- Release ミラーは確認していない。診断 artifact 10310542290 の中身も読んでいない(候補 artifact のみ)。
- 第 9 群 child の実出力(`child-execution.json` / `case-ledger.json` / `scope.json`)は artifact 内の selftest-fixtures 配下にあるが、私は取得していない。非空虚性の判定は **source の逐語読解 + 公刊 stdout の `rejected_cases` 29 件 + gate の fixture bytes** に依拠している。
- **この観点では仕様の齟齬(別対象)も検査の弱化も見つけられなかった — 保証ではない。**

---

**裁定 2302(司令塔・2026-09-13)格付け**: 本判読(71,386 B/8df4f558…・工房 sha256sum で pin)を正本として採用。CV-9 = 同一対象・限定 8 条(新設 1 = 歴史 keyset の両側 literal・解消 1 = F-v9-3)→ **rank 2474/gen 9179(state_head 168d2cf1…・run 34731988156/1)を cross-checked(限定 8 条)で受理**・v9 の 2346 の直系後継として置換・verified=false・grade-2 NOT_DECIDED・full_A0=false。弱化 0 件。F-v10-1〜15 を v11 の前件・所見として台帳 2302 に登録(要修正 = F-v10-2 wire pin の実バイト拘束・F-v10-8 歴史 keyset の登録表導出・F-v10-11 CPU 型の telemetry)。識別実験の再走 34735785100 は数学採用外。
