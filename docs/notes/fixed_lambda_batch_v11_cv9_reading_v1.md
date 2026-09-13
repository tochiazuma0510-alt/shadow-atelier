# 増分 CV-9 判読 — R07 fixed-lambda cycle batch **v11 repair-2**(rank 2474 → 2602・**第 23 親 batch-parent-v10 の入場**・**14-key acceptance**・fresh λ_2474 oracle・**歴史 keyset と著者 wire の「公開登録 metadata 8 本」化**・**P 第 10 群 = 第 23 親 + 現行契約の 14 否定例**・**dry 契約(30 case / 24 range / 34 label)**・**CPU 型 telemetry**)

対象 run: **34756692935 / attempt 1**(success・head `efa99f04d84f16df8d0930a55b7051145e78e455`・workflow `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v11.yml`・**P / C / 両 selftest / metadata / driver-bootstrap の exit code 6/6 が 0**)
候補 artifact **10318688636**(**476,191,819 B**・zip entry **12,792** — 私が central directory を読んで数えた)/ 診断 artifact **10319095955**
系譜(逆置換検問 3 段): 初回 **34746915217**(commit `200ac2f5`・metadata admission で fail-closed・裁定 2310)→ repair-1 **34753243056**(commit `6976c107`・P selftest で fail-closed・裁定 2312)→ **repair-2 34756692935(commit `efa99f04`・success)**
判読者: falsifier(非当事者・事後)。判読日 2026-09-13。
適用規律: **増分 CV-9**(裁定 2105 / 2110 / 2117・memory「CEGAR incremental CV-9」)— 規約表 diff を毎回・pin + TCB 集合が同一なら類似度は省略・**弱化検出が主目的**。
前回 CV-9 正本: `docs/notes/fixed_lambda_batch_v10_cv9_reading_v1.md`(裁定 2302 / 2307 / 2308・限定 8 条・F-v10-1〜16・付録 C = 再走 34735785100 との同一数学照合)。**本書は v10 正本を一切編集していない。**

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 8 条(§4・新設 1・解消 1)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 8 条)・rank 2602 / gen 9307(state_head `b180ec9401b830d835aa005174b3c4906d0333999f4b1afafb52875dc79bbde0`・run 34756692935 / attempt 1)を受理・`verified=false`・GRADE2 NOT_DECIDED(member / nonmember とも)・`full_A0=false`・A0 actual 0/1 不変。v10 の rank 2474 の直系後継として置き換える(合算ではない)。rank 2602 の sealed object は 1 本のみ(v11 系譜で候補 artifact を出したのは repair-2 だけ)。**

**a(128) = 128**(offered 128 / accepted 128 / dependent 0 / skipped 0・`partial=false`・`durable_tail=null`)。rank 2602 = 2474 + 128。消化率 128 / 35,626 = **0.3593 %**。

**検査の弱化は 1 件も検出できなかった**(§5・機械全数)。**逆置換検問 3 段も通過**(§5.5・工房の hunk 数と私の独立計数が完全一致)。**v10 の前件 4 件(F-v10-2 / F-v10-8 / F-v10-11 / F-v10-16)はすべて解消**、F-v10-9 は再発なし。

| v11 の前件 | 判定 | 根拠(要約) |
|---|---|---|
| **F-v10-2**(著者 wire pin が形式検査のみ) | **解消(実バイト + canonical の二重結合)** | 著者 temp の 6 本が **repo 内の公開登録 metadata 8 本**(`search/public-metadata-v11/`)になり、**WF が in-run で 3 回**(repo 側 L370-385・report 側 L473-495・run 後 L723-761)`stat -c %s` + `sha256sum -c` で全 8 本を検査する。**私は 8 本すべての sha256 を自分で計算し、WF の pin と完全一致を確認した。** さらに **8 本すべてが厳密な canonical JSON**(`canonical(parse(raw)) == raw`)で、**`keysets.json`(13,234 B / `be2747fe…`)は artifact 同梱の登録表 `new_source_audit.current_count_inputs` の canonical と 1 バイト違わず、P11 L1126 `CURRENT_COUNT_INPUT_SHA256` の literal とも一致**(§1.2・私の独立計算)。**自己 SHA 循環は 8 本とも無し**(自分の sha256 文字列を自身に含まない)。公刊 `shared-tcb.json.public_declaration_scope` も `declaration_contents_read_in_this_run` を **v10 の false → v11 は true** に改め、`descriptor_purpose` を `ORIGINAL_PUBLICATION_PROVENANCE_SEPARATE_FROM_CANONICAL_INPUT` とした |
| **F-v10-8**(歴史 keyset が両側 source literal) | **解消(登録 snapshot + 名前付き参照)** | **P の `NATIVE_V9_KEYSETS`(9,102 B の source literal)は削除**され(§5.4)、両側とも `historical-keysets.json`(71,827 B)+ `historical-keysets-provenance.json`(345,456 B)を読む。**P は `historical_family` / `historical_document_contract` / `historical_keysets`、C は `RegisteredHistoricalMetadata` クラス — 実装は別物で、相手の helper は使っていない**(C の import は v10 と 1 行も違わず P を import しない)。**C の独立数値和は保たれている**: `HISTORICAL_INDEPENDENT_KEY_COUNTS`(C 自身の 8 × 15 の literal)と snapshot の key 数が一致することを要求(`registered_historical_independent_exact_key_count:*`)、snapshot の role / namespace も **C 自身の `*_BATCH_ROLE` / `*_BATCH_SCHEMA` 定数**と突合する。**schema 検査は失われていない**: `check()` が `set(value) == expected_keys` **かつ** `value.get("schema") == expected_schema` を要求(§5.4) |
| **F-v10-11**(CPU 型 telemetry) | **解消(共変量として正しく記録)** | `runtime-observation.json` に **`cpu_model: "AMD EPYC 7763 64-Core Processor"`**。`cost-receipt.limitations[5]` が **「The nullable CPU model in runtime-observation.json is only a covariate; it does not identify a timing cause」**と明記 — **交絡除去を主張していない**(裁定 2303 の要求どおり) |
| **F-v10-16**(math_head の混入) | **混入なし** | `math_head` の出現は P11 **0**・C11 **0**・driver **0**(私が grep) |
| **F-v10-9**(内訳票の分類) | **再発なし** | v11 の P 増分 +94,998 B は **追加定義 90,492 B + 変更定義 +1,639 B + module 残余 2,867 B**。module 側は **追加 16 本 11,321 B − 削除 1 本 9,102 B + 変更 5 本 +20 B**。最大の新規定数は `TENTH_CASE_SPECS` **4,818 B** で、v10 のような 156 KB の fixture 定数は存在しない(むしろ歴史 keyset literal 9,102 B が source から出て行った) |
| **F-v11-1**(canary 期待文字列の require 由来導出) | **解消(実通過)** | repair-1 が `v11_public_wire_value_reason(name)`(理由 literal の単一定義)と **`v11_public_wire_value_error_text(name)`(実際に `require(False, reason)` を呼び、捕捉した `ValueError` の文字列を返す)** を新設し、canary の期待値と本番比較器が同一の formatter を共有する。**公刊 `metadata-gate.json` の 5 canary はいずれも `reason: "batch_workflow:v11-public-wire-whole-registered-value:<name>"` を記録**(初回に欠けていた `batch_workflow:` prefix つき)。拒否しなければ `v11-public-wire-require-did-not-reject:<name>` で fail-closed |
| **F-v11-2**(fixture の登録表導出 + dry 契約) | **解消(ただし dry の射程は限定条項 8 に明記)** | repair-2 の P 2 hunk が `old_acceptance` / `portable` fixture を **`REGISTERED_PUBLIC_METADATA_CONTEXT["values"]["keysets"]` の `current_exact_keys.acceptance` と `current_schema` から導出**し、**`require(sha(canonical(acceptance_table)) == CURRENT_COUNT_INPUT_SHA256, "k128_current_acceptance_registered_table")` を新設**(検査の追加)。driver の `v11_k128_dry_preconditions()`(+189 行)は 30 case / 24 source range / 34 gate label を実登録表・実 `REGISTRATION`・実 `code_contract()['producer']` と突合する。**dry は判定経路に触れず**、`status = SOURCE_BOUND_STATIC_PREMISES_NOT_TARGET_EXECUTION` / `new_runtime_results = None` / `target_execution_import_AST_compile_selftest = 0` / **各 case の `actual_target_rejection_observed` が `None` であることを要求**する(= 実 P 拒否の観測ではないと自ら記録) |
| **第 23 親(batch-parent-v10)の 14-key acceptance 入場** | **入場済み(私が公刊 acceptance の key を数えた)** | `acceptance.json`(**20,271,337 B**・私の sha256 `c53e0d845ecfbb67fe0b64a7f1c4328fceb8c619adef67cce96addd5f46ff205`)の top-level key は**ちょうど 14**(`batch_anchor_v10` を含む)・`parents` 23 role。`batch_anchor_v10` = rank 2474 / gen 9179 / state `168d2cf1…` / λ `e910b7b6…` / 896 / 1024 / 1121 / 64 / `old_oracle {35780, 847, 435}`。**内包する v10 側 pin は `output/result.json` 208,957 B `eba88c80…`・`output/HEAD` 1,258 B・`checker-result.json` 15,974 B・`output/parent-intake.json` 12,871 B で、v10 正本 付録 A に私が記録した実測と完全一致**(= 元 run 34731988156 の object) |
| **再走 34735785100 が親に含まれないこと** | **含まれない** | `run-receipt.accepted_artifacts` は 23 role で `batch-parent-v10` = artifact **10310711557** / run **34731988156** / 448,498,707 B。**受理 artifact 全体を走査して `34735785100` の出現は 0**(私が機械で確認) |
| **fresh λ_2474 の oracle** | **正しい** | `selection/start.json.selection_lambda_sha256 = e910b7b65d64b1450e2c9b8aad495488e34b643fc0c6f4a01af5b1a78abf4e36`(= v10 final λ)・rank 2474 / gen 9179 / state `168d2cf1…`。`batch_observation.current` = **35,626** / 1368 / 697、`old` = λ_2346 `289190c3…` / **35,780**(= v10 正本 §0 の current と完全一致)。C の独立再計算 `{"chords": 54433, "failed": 35626, "selected": 128}`・`failed-indices.u32` = **142,504 B = 4 × 35,626** |
| **計器 receipt の telemetry only** | **触れていない** | `parent-timing-receipt` は **63 区間すべて OBSERVED**(live-parent 23 + intake-inventory 23 + native-intake 9 + directory-restoration 8)・`errors []`・4 抑制 flag。隣接 2 受領証も COMPLETE_MEASURED_SCOPE + 抑制 flag(§5.7) |
| **selftest 群の群別拒否件数** | **実 stdout と一致(三系)** | **10 群**。P `[30,10,6,7,8,8,12,1,29,14]`(計 **125**)・C `[28,9,6,7,8,10,14,15,20,13]`(計 **130**)。**私が stdout の `rejected_cases` を 1 件ずつ数えた**(§6) |

### 本判読の一次事実(新規)

1. **「著者 temp の宣言文書」という積年の穴が repo 内の登録物になった。** v9 / v10 で私が繰り返し限定条項に書いてきた「著者 wire は形式検査のみ・repo 外で中身を読めない」は、v11 で **8 本の登録 metadata が repo に入り、WF が in-run で 3 度 bytes+sha を検証し、driver-bootstrap の pin ログ 52 行にも 8 本すべてが現れる**ことで解消した。**私は 8 本すべてを自分で hash し、WF pin・公刊 `shared-tcb.registered_public_metadata`・`run-receipt.registered_public_metadata`・artifact 同梱コピーの 4 者一致を確認した。**
2. **`keysets.json` は「登録表そのもの」である。** 私が artifact の `audit-region-registry.json`(**30,574,417 B**・私の sha `76f148d5…` = driver `INHERITANCE_REGISTRY_PIN`)から `new_source_audit.current_count_inputs` を取り出して canonical 化したところ、**13,234 B / `be2747fe…` で登録 `keysets.json` と 1 バイト違わず**、P11 の `CURRENT_COUNT_INPUT_SHA256` literal とも一致した。値の規約の出所が「harness の内部表」から「repo の登録物」へ移り、外部から指させるようになった。
3. **歴史 keyset の source literal が消えた。** P の `NATIVE_V9_KEYSETS`(9,102 B)は削除され、C 側では `check_*_native_keysets` の 3 関数が 9,754 / 9,260 / 8,771 B → 147 / 143 / 143 B に縮んだ。**縮んだのはデータであって検査ではない**: 代表例 `check_v9_acceptance_header` は 12 key の literal 集合 + schema literal が `check_registered_native_keysets(9, "acceptance", value, "native_v9_acceptance_exact_twelve_plain_keys")` 1 行になり、**同じラベルのまま**、期待値が snapshot 由来になった(`check()` は key 集合と schema の両方を要求)。
4. **prefix view は 8 層に伸び、v10 の表を再現した。** 私は登録表から 7 層 prefix view を再計算し、**2346 / 9051 / 22 role / 768 / 896 / 993 / 865 / 5,376 / 5,404 / 7 / [1450…2346]** を得た — **v10 正本 §2.1 の現行値表と 1 個残らず一致**。現行 8 層 view は 2474 / 9179 / 23 / 896 / 1024 / 1121 / 993 / 6,144 / 6,176 / 8 / [1450…2474]。
5. **失敗数は今期減少した。** 36,274 → 36,104 → 36,002 → 35,921 → 36,000 → 36,107 → 35,647 → 35,780 → **35,626**(今期 net **−154**)。隣接差 −170 / −102 / −81 / +79 / +107 / −460 / +133 / **−154** で、**9 世代のうち増加は 3 回**。**単調減少は依然として成り立たない。Task 988 F4 の反例は排除されていない。**
6. **逆置換検問 3 段の hunk 数は工房の申告と完全一致した。** repair-1 = driver **4 hunk**(+16/−3)+ WF **1 hunk / 2 行**、repair-2 = P **2 hunk**(+11/−5)+ C **1 hunk / 1 行**(+1/−1)+ driver **16 hunk**(+203/−14)+ WF **4 hunk**(+15/−15)+ 登録 metadata **5 本 各 +1/−1**。driver の `require(` 出現は **2,019 → 2,020 → 2,058** と単調増加(削除 0)。
7. **repair-2 の driver 定数変更 241 件はすべて VALUE 型**(ADDED / REMOVED / TYPE / LEN は 0 件)で、内訳は **pin 再結合 211 件**(file 102 / sha256 58 / bytes 51)と **source region 座標 30 件**(offset 15 / first_line 15 — P が 60 B 伸びた分の再計算)。`name` / `rejected_count` / `expected_completion_order` / `stage_rules` / `case_count` は 1 件も動いていない。

---

## 1. (1) pin と TCB

### 1.1 便の pin の実測照合(私が `sha256sum` を実行)

| 対象 | bytes | sha256 | 判定 |
|---|---:|---|---|
| P11 `search/d972_r07_fixed_lambda_cycle_batch_v11.py` | 1,129,263 | `7ec45483543d189eaf42ba2ddf92fddbe58d05aac02d3070a23a833778401e7c` | **一致** |
| C11 `search/check_d972_r07_fixed_lambda_cycle_batch_v11.py` | 949,977 | `4d522af166c78e5b0ea69ee30bd6df53c62b1ec6a6f3aa91ed3c681079533b71` | **一致** |
| driver `search/d972_r07_fixed_lambda_cycle_batch_v11_workflow_driver_v1.py` | 63,275,225 | `b7b7b73cee231c2f396c16b6ceabe9053c50363269d11702f87a82cbbb2a9224` | **一致** |
| WF `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v11.yml` | 69,996 | `555631a754ac9a27a89803d891cd1e3edab367a39f5dfcc5111cb6cd2925ba1b` | **一致** |

**公開登録 metadata 8 本(新設・私が全部 hash した)**:

| ファイル | bytes | sha256(私の実測 = WF pin) | canonical? |
|---|---:|---|:---:|
| `public-declarations/keysets.json` | 13,234 | `be2747fe98bfd884fc7b48a3b90e8bf842d42f5abc8a6290cce20a70199b7666` | **厳密 canonical** |
| `public-declarations/P_timing.json` | 87,050 | `7ad6c949d23b53676aa9f4960406a5b6a6310807eaee0bf8e685f6e64cbc3e6d` | 同 |
| `public-declarations/C_timing.json` | 107,220 | `ebca662204bca5e6779c2675010a273bcc8e2a9e955450386651da5a7b9fe516` | 同 |
| `public-declarations/producer_interface.json` | 116,242 | `13114244ad773521452424f402e510808c7c17432f78679aa859169b05cb4ff0` | 同 |
| `public-declarations/producer_final_adoption.json` | 859 | `2cda686fd94f32395f988bc65efdfc6a20b1b0d1cd31ebdba443b933cd348081` | 同 |
| `public-declarations/checker_final_adoption.json` | 903 | `207ab2f43c4e20d5f1acd779664f7f06d31dd77352b1746e6d9d425c7e87ce64` | 同 |
| `historical-keysets.json` | 71,827 | `a7f7ad8f1550c74947386f0e934d18f7b70ed0292080e5fb402c8d84da877aa0` | 同 |
| `historical-keysets-provenance.json` | 345,456 | `00290a630966127ce5059387627d496a7c7dc2941672f8e22657ec237bce19bf` | 同 |

**8 本とも `canonical(parse(raw)) == raw`(ASCII・sort_keys・LF 終端)であり、bytes pin と value pin が一致する。8 本とも自分の sha256 文字列を自身に含まない(自己 SHA 循環なし)。**

- **C11 が P11 を bytes + sha256 で pin**: `CURRENT_PRODUCER_REGISTRATION = {"bytes":1129263, "file":"search/d972_r07_fixed_lambda_cycle_batch_v11.py", "sha256":"7ec45483…"}`(C11 **L611**)。**私の実測と完全一致。**
- **P11 が C11 を pin する経路は file 名のみ**(v7〜v10 と同じ非対称・**変化なし**・限定条項 5)。
- **driver / WF も同じ 2 本と 8 本を pin**(driver L35 `CURRENT_EXECUTABLE_PINS`、WF L191-274)。

### 1.2 artifact 実バイトからの独立確認(私が HTTP Range で取得し、自分で sha256 を計算)

| entry | bytes | 私の sha256 | 意味 |
|---|---:|---|---|
| `audit-region-registry.json` | **30,574,417** | `76f148d5c05ff02a01944b90a95af4abcfe024e0a53eef29b3dc53e28bd396c2` | driver `INHERITANCE_REGISTRY_PIN`(L5479)と一致 |
| その canonical `new_source_audit.current_count_inputs` | **13,234** | `be2747fe98bfd884fc7b48a3b90e8bf842d42f5abc8a6290cce20a70199b7666` | **= 登録 `keysets.json` と 1 バイト違わず・= P11 L1126 の literal** |
| `acceptance.json` | **20,271,337** | `c53e0d845ecfbb67fe0b64a7f1c4328fceb8c619adef67cce96addd5f46ff205` | top-level 14 key・`parents` 23 role(§0) |

### 1.3 in-run の pin 検証証拠

`driver-bootstrap-stdout.log`(5,123 B)に **52 行の `OK`**(v10 は 32)。**1 行目は現行 WF `…-v11.yml`(F-v9-8 の解消が継続)**、さらに **登録 metadata 8 本すべてが個別に OK 行を持つ**。
`runtime-observation.json` = `launch {run 34756692935, attempt 1, head efa99f04…, workflow …-v11.yml}`・`expected == actual`(python 3.13.15 / numpy 2.5.1)・**`cpu_model "AMD EPYC 7763 64-Core Processor"`**。
WF は登録 metadata を **3 箇所**(L370-385 repo 側 / L473-495 report 側 / L723-761 run 後)で `stat -c %s` + `sha256sum -c` 検証する。

### 1.4 TCB(kernel 集合・import 集合・子プロセス辺とも**不変**)

- **算術 TCB**: 公刊 `shared-tcb.json`(26,075 B)の `registered_shared_tcb.kernels` は **4 区間 = 共有カーネル 2 本 × P/C 各 1**、file・line(P 342-357 / C 269-284、P/C とも 192-203)は **v9 / v10 と同一**。`status DECLARED_SHARED_TCB` / `verified false` / `current_run_call_coverage NOT_MEASURED` / `kernel_third_independence_claimed false`。
- **交差辺**: **P11 / C11 の import 集合は v10 と 1 行も違わない**(私が import 行を diff して空)。C は `check_d972_r07_complete_oracle_cegar_continuation_v2` のみを import し、**P を import する経路は無い**。
- **子プロセス辺**: `current_execution_edges` は **2 本**(`producer-key-contract-child` / `producer-parent-contract-child`)で v10 と同数・同 id。
- **新設**: `shared-tcb.json` に **`registered_public_metadata`**(8 本の `{copy, original}` 対・bytes+sha)が加わった。`public_declaration_scope` は `declaration_contents_read_in_this_run: **true**` / `byte_monotonicity_is_semantic_evidence: false` / `descriptor_purpose: ORIGINAL_PUBLICATION_PROVENANCE_SEPARATE_FROM_CANONICAL_INPUT` / 「six canonical public inputs are separately compared as whole values」。
- **harness TCB は単著**(WF 69,996 B + driver 63,275,225 B + 登録 metadata 8 本)。**run 側の判読は本書が唯一**である。

### 1.5 凍結 envelope(宇宙・cap)

公刊 `output/owner.json.registration` / `cost-receipt.registration` / `run-receipt.registration`: `batch_size 128` / `max_batches 1` / `refill false` / `CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX` / `PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY` / producer `5,400 s・7,168 MiB` / checker `10,800 s・7,168 MiB`。**v7〜v10 と数値として完全同一 — caps・宇宙は 1 バイトも動いていない。**
`owner.json.scope` も `vertices 54432 / edges 108864 / chords 54433 / legality_rows 5 / source_lower 96776 / physical_lower 32260 / physical 48384 / p1_rows 8059 / characters [0,1,2,3] / auxiliary_tests 2` で不変。

---

## 2. (2) 規約表 diff(v10 → v11)

### 2.1 値の規約(**私が登録表から再計算し、C の独立和・実出力と三者照合**)

| 量 | v10 | v11 | P11 の出所(登録表導出) | C11 の出所(**独立**) | 実出力 | 私の再計算 |
|---|---:|---:|---|---|---:|:---:|
| 親 role 数 | 22 | **23** | 登録表 `parent_roles` ≡ `ROLES` | `PARENT_ROLES = (*V10_PARENT_ROLES, "batch-parent-v10")`(L55) | 23 | 一致 |
| batch 親層数 n | 7 | **8** | `ROLES[15:]` | `V11_CURRENT_PARENT_LAYER_COUNT`(L658) | 8 | 一致 |
| `previous_parent_batch_rows` | 768 | **896** | 登録表の層和 | `V11_CURRENT_PREVIOUS_BATCH_ROWS`(L653) | 896 | 一致 |
| `total_parent_batch_rows` | 896 | **1024** | 同上 | `V11_CURRENT_TOTAL_BATCH_ROWS`(L654) | 1024 | 一致 |
| `target_derivation_parents` | 993 | **1121** | `ancestry(97) + total` | `97 + 1024`(L656) | 1121 | 一致 |
| `previous_parent_target_derivations` | 865 | **993** | 同上 | `97 + 896`(L655) | 993 | 一致 |
| acceptance key 数 | 13 | **14** | 登録表 `current_exact_keys.acceptance` | `6 + 8`(L663)+ C L2006 `acceptance_exact_fourteen_plain_keys` | **14**(私が公刊 acceptance を数えた) | 一致 |
| `parent-intake` key 数 | 81 | **89** | 登録表 | `25 + 8 × 8`(L665) | **89**(私が数えた) | 一致 |
| `start` key 数 | 64 | **69** | 同上 | `34 + 5 × (8 − 1)`(L664) | 69 | 一致 |
| `parent-layout` key 数 | 15 | **16** | 同上 | `acceptance + 2`(L666) | 16(登録表・実バイト未取得) | 一致 |
| `candidate_phase_manifests_checked` | 5,376 | **6,144** | `6 × total` | `6 × 1024`(L660) | 6,144 | 一致 |
| `checkpoints_checked` | 5,404 | **6,176** | `8 × 772` | `(4 + 6 × 128) × 8`(L661) | 6,176 | 一致 |
| `invocations_checked` | 7 | **8** | 層 `invocations` の和 | `V11_CURRENT_INVOCATION_COUNT`(L662) | 8 | 一致 |
| `native_pairing_rows_rechecked` | [1450…2346] | **[1450,1578,1706,1834,1962,2090,2218,2346,2474]** | 累積 | `V11_CURRENT_NATIVE_PAIRING_ROWS`(L657) | 一致 | 一致 |
| `initial_rank` / `initial_generation` | 2346 / 9051 | **2474 / 9179** | `1450 + total` / `8155 + total` | `EIGHTH_BATCH_RANK`(L598)/ `EIGHTH_BATCH_GENERATION` | 2474 / 9179 | 一致 |
| selftest 群 | 9 | **10** | `[30,10,6,7,8,8,12,1,29,14]` | `[28,9,6,7,8,10,14,15,20,13]` | 一致(§6) | 一致 |
| schema | `.v10` | `.v11` | — | — | 全公開 JSON | — |

**私は artifact の `audit-region-registry.json`(30,574,417 B)から `current_count_inputs` を取り出し、`registered_layer_counts` を自分で再実装して上表の「私の再計算」列を埋めた。全量一致。**
登録表 `current_exact_keys` の要素数(私が数えた): acceptance **14** / parent-intake **89** / start **69** / parent-layout **16** / head 24 / result 48 / checker-result 50 / final-manifest 27 / progress-head 16 / owner 8 / selection 27 / selection-start 19 / separator 12 / source 10 / fixed-manifest 9。

### 2.2 **最大の規約変更 = 歴史 keyset と著者 wire の「公開登録 metadata」化**(v11 の中心)

```
C10  require(type(value) is dict and set(value) == {"schema","parents","anchor","batch_anchor",
             "next_batch_anchor","batch_anchor_v5",…,"batch_anchor_v8","code","runtime","registration"} and
             value["schema"] == SEVENTH_BATCH_SCHEMA + ".acceptance", "native_v9_acceptance_exact_twelve_plain_keys")
C11  check_registered_native_keysets(9, "acceptance", value, "native_v9_acceptance_exact_twelve_plain_keys")
```

`RegisteredHistoricalMetadata.__init__`(C11)は snapshot を**次の条件で受け入れる**:
- header がちょうど `{schema, native_domains}` で schema == `d972.r07.registered-historical-keysets.v1`(`registered_historical_snapshot_exact_header`)
- `native_domains` がちょうど 8(`registered_historical_snapshot_exact_eight_domains`)
- 各 domain の `generation` / `role` / `namespace` が **C 自身の `(BATCH_PARENT_ROLE, OLD_BATCH_SCHEMA) …(EIGHTH_BATCH_ROLE, EIGHTH_BATCH_SCHEMA)` 定数**と一致(`registered_historical_domain_identity:N`)
- 15 family の別名が全単射で sorted(`registered_historical_exact_bijective_aliases`)
- 各 family の `schema == namespace + "." + common`、keys が sorted / unique / ASCII、**長さが C 自身の `HISTORICAL_INDEPENDENT_KEY_COUNTS`(8 × 15 の literal)と一致**(`registered_historical_independent_exact_key_count:N:local`)、`"schema" in keys` かつ `("sha256" in keys) == (local != "acceptance")`
- 第 3 世代の `parent_intake` は **present false / schema null / keys null** を明示要求(`registered_historical_proven_absent_v3_intake`)
- 生成後は `__setattr__` が `registered_historical_metadata_is_immutable` で不変

そして `check(generation, local, value, label)` は **`set(value) == expected_keys` かつ `value.get("schema") == expected_schema`** を要求する。**⇒ v10 で source literal だった「keys + schema」は、登録 snapshot 由来になったうえで検査内容は同一であり、さらに C 自身の独立 key 数との一致が追加された。**
P 側は別実装(`historical_family` / `historical_keysets` / `historical_document_contract`)で、`historical_family` が `3 ≤ generation ≤ 10`・8 domain・`domain[1] == ROLES[generation+12]`(role alias 禁止)・`present is True`(欠落文書の拒否)を要求する。**加えて `read_json` に 1 行 `historical_full_file_contract(root, name, value)` が追加され**(§5.4)、登録親 root から歴史 member path を読むときは常に世代・role 束縛と schema/keys 契約が適用される(**検査の追加**)。

### 2.3 公開 JSON key 集合(私が実バイトから数えた)

`acceptance.json` **14**・`output/HEAD` **24**・`result.json` **48**・`checker-result.json` **50**・`selection/start.json` **19**・`parent-intake.json` **89**・`final/manifest.json` **27**・`progress/HEAD` **16**・`owner.json` **8** — **9 文書すべてが登録表の `current_exact_keys` の要素数および C の独立和と一致**。
`run-receipt` の自己申告 key に版番号入りは今期も無い(`selection_lambda_oracle_is_separate_from_new_final_lambda_oracle`)。**F-v9-7 の解消は継続。**

---

## 3. (3) 群別 PASS(本走の検査群)

| 群 | 何を要求しているか | 結果 | 私の独立確認 |
|---|---|---|---|
| **A. 第 23 親の入場** | 14-key acceptance・`batch_anchor_v10` が親 artifact と一致 | **PASS** | 公刊 `acceptance.json` の top-level key を私が数えて **14**。`parents` 23 role。`batch_anchor_v10` の内包 pin(result 208,957 B `eba88c80…` / HEAD 1,258 B / checker-result 15,974 B / parent-intake 12,871 B)が **v10 正本 付録 A の私の実測と一致**。`run-receipt.accepted_artifacts` 23 role・**再走 34735785100 は不在** |
| **B. 親層の累積則** | 128 / 896 / 1024・祖先 97 → … → 1121・pairing 9 点 | **PASS** | `parent-intake.json`(14,316 B・**89 key**)の実バイト: `previous 896 / total 1024 / tdp 1121 / old_tdp 97 / pairings [1450,…,2474] / candidate_manifests 1024 / row_manifests 1024 / phase 6,144 / checkpoints 6,176 / invocations 8`。`parent_layers` は 8 件で末尾が `batch-parent-v10`(rank 2474・gen 9179・state `168d2cf1…`・tdp 993 → 1121)。第 7 中間記録 2346/9051/993 も揃う |
| **C. fresh λ_2474 oracle** | 選定 λ = v10 final λ・state_head = 受理側・roster 128 本 | **PASS** | `selection/start.json`(1,117 B・19 key): `selection_lambda_sha256 e910b7b6…` / `state_head 168d2cf1…` / `previous_target 96785516…` / `target f10b60b8…` / rank 2474 / gen 9179 / anchor 128 / 896 / 1024 |
| **D. current 側 roster の独立再計算** | C が自前で残差選定をやり直す | **PASS** | `checker-stderr.log`(1,425,673 B)に `{"chords": 54433, "failed": 35626, "phase": "fixed_lambda_all_residuals_selected", "selected": 128}`。`tree.json`: `residual_nonzero 35626 / first_failed_index 697 / first_failed_edge 1368 / fit [1,0,2,0,0] / basis_chords [2,3,4,6,11] / independent_tau_columns 5 / aux [0,0] / full_chord_eof true`。`failed-indices.u32` は **142,504 B = 4 × 35,626**(私が entry サイズから割った) |
| **E. old 側 oracle** | 35,780 / 435 / 847 が親の実体に結ばれる | **PASS(再測ではない・受領証に明示)** | `acceptance.json.batch_anchor_v10.old_oracle = {35780, 847, 435}` = v10 正本の current 実測。`batch_observation.old` も同値。**`old_side_recomputed_in_this_run: false` が公刊されている**(限定条項 2) |
| **F. 128 行の受理** | 128/128 INDEPENDENT・dependent 0・skipped 0 | **PASS** | `result.json`: `accepted_new_rows 128 / processed 128 / dependent 0 / skipped_after_linear [] / selected_count 128`。`checker-result.json`: `accepted_rows_compared 128 / candidate_decisions_compared 128 / all_completed_payloads_and_json_compared true / public_final_compared true / partial false / durable_tail null` |
| **G. 鎖と rank** | 2602 = 2474 + 128・gen 9307 = 9179 + 128 | **PASS** | HEAD / result / checker-result / final-manifest / progress-HEAD / run-receipt で `rank 2602 / generation 9307 / state_head b180ec94…` が一致(私が実バイトで突合)。`anchor 128 / 896 / 1024`・`anchor_completed_steps 64`・`progress/HEAD.sequence 771` |
| **H. 予言の非空虚性** | `first_candidate` 5 条件 → INDEPENDENT | **PASS(9 回目)** | `matches_prediction true` / `expected = observed = INDEPENDENT` / `ordinal 0` / `raw_pairing 2` / `selection_scalar 2` / 5 条件すべて true。`independence_rate_predicted false` の自己抑制は維持 |
| **I. UNKNOWN の置き場** | 未計算を 0 と読んでいないか | **PASS** | `new_lambda_oracle null`・`failure_set_monotonicity_asserted false`・`independence_rate_predicted false`・`old_side_recomputed_in_this_run false`・`grade2_member/nonmember NOT_DECIDED`・`full_A0 false`・`verified false`・`current_run_call_coverage NOT_MEASURED`・`positive_readout NOT_APPLICABLE`・`old_success_suites 0`・`historical_payload_reacquired_in_this_run false`・`new_final_q_computed false`・`workshop_CV9 PENDING`。**NONMEMBER 主張は一切していない** |
| **J. 計器(診断)** | 外側 63 区間 / 隣接 2 受領証 / CPU 型 | **PASS** | §5.7 |

---

## 4. 限定条項(**8 条**・v10 から新設 1・**解消 1**)

1. **射程 = rank 2474 → 2602 の 1 batch のみ。** rank 2602 の λ\* に対する oracle は**未計算**(`new_lambda_oracle = null`)。**NONMEMBER 主張ではない。**
2. **a(128) = 128 は roster 前置 128 本の観測**(batch パラメータ k の性質ではない)。消化率 128 / 35,626 = **0.3593 %**。**Task 988 F4 の反例は排除されていない。** 失敗数は今期 **−154** だが、9 世代のうち増加は 3 回で**単調減少は成り立たない**。**old λ_2346 の 35,780 は本 run で再測されていない**(親の保存 anchor / `old_oracle` との突合まで)— `old_side_recomputed_in_this_run: false` として受領証に明示(F-v10-4 の継続)。
3. **算術 TCB は共有カーネル 2 本を含む**(P/C 各 1 で計 4 区間・v9〜v11 で集合同一)。`current_run_call_coverage = NOT_MEASURED`・`kernel_third_independence_claimed = false`。**第三独立性はこの 2 本に及ばない。** P1 相が候補時間の **71.2 %**(1,019.79 / 1,431.54)なので `vectorized_projection_chunk` は確実に load-bearing。
4. **旧 2,474 行の実バイトは私自身は未取得。** λ_new ⊥ 旧行 と ρ₂ の旧行部分は checker の再現に依存する。**ρ₂ は依然 DERIVED**。「選定 λ_2474 が旧 2,474 行を殺す」ことも本 run で私が再測したわけではない。
5. **harness TCB は単著。** WF 69,996 B + driver 63,275,225 B + **登録 metadata 8 本**を書いたのは同一の著者であり、値の規約(登録表 = `keysets.json`)も歴史 keyset(`historical-keysets.json`)もその著者の登録物である。**v11 でこれらは「repo 内・in-run で bytes+sha 検証・canonical 一致」まで強化されたが、内容を決めたのが著者であるという一点は動かない。** 外部からこれを縛るのは **C の独立和(`V11_CURRENT_*`)と C 独自の `HISTORICAL_INDEPENDENT_KEY_COUNTS`**、および P/C が別実装で同じ登録物を読むことである。**P は C を file 名でしか pin しない**(継続)。
6. **checker の相別 timestamp は依然無い。** `cost-receipt.limitations[1]` が自ら宣言(v9 以来逐語同一)。**F-k64-7 継続。**
7. **私は 476 MB の ZIP を全量ダウンロードしていない**(HTTP Range で必要 entry を個別取得)。ZIP 全体の sha は自分でバイト再計算していない。**私が sha256 を自分で計算したのは付録 A の 15 対象だけ。** `output/parent-layout.json`・`output/start.json`・`acceptance.json` の入れ子(top-level key と `batch_anchor_v10` 以外)・`producer_interface.json` の全内容は読んでいない。
8. **【新設】dry 契約(第 10 群の 30 case)は「実 P の拒否の観測」ではない。** `v11_k128_dry_preconditions()` が検証するのは **公開契約と登録表・`REGISTRATION`・実 source D3 との静的整合**であり、契約自身が `status = SOURCE_BOUND_STATIC_PREMISES_NOT_TARGET_EXECUTION` / `new_runtime_results = None` / `target_execution_import_AST_compile_selftest = 0` / 各 case `actual_target_rejection_observed = None` / 「only ValueError captured; expected substring in str(exception), not exact text equality」と宣言している。**30 case が「実際に P がその gate で落ちること」を示すのは、あくまで P selftest 第 1・2 群(k128・計 40 拒否)の実行であって dry ではない。** dry は「公開された gate 表が実 source と矛盾しないこと」までを保証する。**この区別を格付け文で消さないこと。**

### 4.1 前回 8 条との 1 対 1 対応

| v10 の条 | v11 での扱い |
|---|---|
| 1. 射程 1 batch | **継続**(条 1・rank が 2474→2602 に更新) |
| 2. a(k) の意味・F4 未排除・old λ 再測なし | **継続**(条 2・失敗数は今期 −154 だが単調性は未回復) |
| 3. 共有 kernel 2 本 NOT_MEASURED | **継続・集合も不変**(条 3・P1 比率 68.6 % → 71.2 %) |
| 4. 旧行の実バイト未取得・ρ₂ DERIVED | **継続**(条 4・旧行数 2,346 → 2,474) |
| 5. harness TCB 単著 + 登録表が値の源 + **wire pin は形式検査のみ** | **継続・ただし wire 部分は解消**(条 5)。8 本が repo 内 + in-run bytes/sha + canonical 一致になったため、限定は「著者が内容を決めた」一点に縮んだ |
| 6. checker 段別 timestamp 無し | **継続**(条 6) |
| 7. ZIP 全量 DL せず | **継続**(条 7) |
| 8. 歴史 keyset が両側 source literal | **解消**(§2.2・P の `NATIVE_V9_KEYSETS` 削除・C は snapshot + 独立 key 数) |
| —(新設) | **条 8**(dry 契約の射程 = 静的整合であって実拒否の観測ではない) |

**8 条 → 8 条(新設 1・解消 1)。**

---

## 5. 弱化検出(本判読の主目的)

### 5.1 検査 1 — `require` ラベル集合の全数 diff(私の AST 実装)

| 側 | v10 のラベル | v11 のラベル | 削除 | 追加 | 出現回数が減ったラベル |
|---|---:|---:|---:|---:|---:|
| P | 679(呼出 1,059) | **759(呼出 1,201)** | **5** | 85 | **1** |
| C | 734(呼出 798) | **826(呼出 896)** | **15** | 107 | **0** |

**この器は `require(cond, "literal")` の第 2 引数が文字列定数の呼出だけを数えるため、v11 の「ラベルを helper 引数へ移す」改修を削除と誤検出する。** §5.3 の全 helper 多重集合と grep で 1 件ずつ追跡した結果:

- **C の 15 件**: 12 件は**存置**(`check_registered_native_keysets` / `check_registered_native_records` の `label` 引数として同じ文字列が渡る。`acceptance_exact_seven_plain_keys` 2 箇所・`c7/c8/c9/c10_parent*_intake_not_current*` 2〜3 箇所ずつ・`native_v5…v9_acceptance_exact_*_plain_keys` 各 1・`next_parent_fixed_reference_exact_nine_fields` は **6 → 7 箇所に増加**・`old_batch_retains_six_key_v3_acceptance` 1)。残り 3 件は版番号改名(`acceptance_exact_thirteen_plain_keys` → `acceptance_exact_fourteen_plain_keys` + **歴史版 `native_v10_acceptance_exact_thirteen_plain_keys` の新設**、`all_twenty_two_…` → `all_twenty_three_…`、`c10_current_root_key_counts_…` → `c11_…`)。
- **P の 5 件**: すべて版番号改名(`current_count_seven_…` → `current_count_eight_separate_native_layers`、`…twenty_two_roots…` → `…twenty_three_roots…`、`selftest_exact_nine_group_counts` → `…_ten_…`、`task1191_…` → `task1194_…`、`twenty_two_registered_roots` → `twenty_three_registered_roots`)。
- **P の減少 1 件** `accepted_batch_old_acceptance_schema` 7 → 4: 第 5〜8 世代の 4 箇所が **`historical_document_contract(old_acceptance, N, "acceptance")`**(schema + exact keys を snapshot から要求)に置き換わったため。第 3・4・9・10 世代は明示 require のまま残る。**検査は失われていない。**

### 5.2 検査 2 — 同名ラベルの**条件式**の diff

| 側 | 件数 | 内容 |
|---|---:|---|
| P | **5** | いずれも歴史ブロックの prefix view 化(`current_count(…)` → **`native_v9_count(…)`**)。値は 993 / 128 / 1121 / 2346 / 7 で v10 の現行値と同一。`batch_v9_internal_prior_view_exact_twenty_two_roles` は `list(ROLES)` → `list(HISTORICAL_V10_ROLES)`(`len == 22` の要求は残存) |
| C | **14** | 12 件が **schema literal → 登録 snapshot 参照**(`OLD_BATCH_SCHEMA` / `FIFTH_BATCH_SCHEMA` / `SEVENTH_BATCH_SCHEMA` 等 → `registered_historical_metadata().domain(N)[2]`)、2 件が世代更新(`SEVENTH_BATCH_RANK` → `EIGHTH_BATCH_RANK`、`SEVENTH_BATCH_INVENTORY_REGISTRATION` → `EIGHTH_…`) |

**⇒ 条件式の緩和は 1 件も無い。** C の置換先 `domain(N)[2]` は §2.2 のとおり **C 自身の `*_BATCH_SCHEMA` 定数と一致することを要求されている**ので、schema の拘束は失われていない。

### 5.3 検査 3 — **全 helper のラベル対の多重集合 diff と呼出数**

| 側 | ラベル対 | 呼出総数 | 消えた対 | 減った対 |
|---|---:|---:|---:|---|
| P | 766 → **860** | 1,228 → **1,394** | 11(§5.1 の 5 + `exact_keys(acceptance_thirteen_plain_keys)` + `exact_keys(accepted_batch_v5..v9_old_*_keys)` 5) | 2(`exact_keys(batch_fixed_reference_exact_keys)` 7→2・`require(accepted_batch_old_acceptance_schema)` 7→4) |
| C | 1,199 → **1,380** | 1,319 → **1,529** | 15(§5.1) | **0** |

**さらに「関数呼出そのもの」を AST で全数計数した**(ラベルの有無に依らない):

| 側 | 総 Call | 減った関数 | 主要 helper |
|---|---:|---|---|
| P | 8,360 → **9,353** | **`current_count` 66 → 65 のみ**(`native_v9_count` が 0 → 37 で新設) | require 1,183 → **1,351**・exact_keys 93 → **98**・integer 341 → **381**・check_seal 54 → **62**・k128_reject 54 → 54 |
| C | 6,345 → **7,272** | `check_v10_current_anchor_batch_counts` 7 → 2(**後継 `check_v11_current_anchor_batch_counts` が 9 箇所**)・`set` 131(builtin) | require 881 → **1,001**・same_json 490 → **571**・integer 89 → **98**・pair 65 → **78**・新設 `check_registered_native_keysets` **26**・`check_registered_native_records` **4** |

**⇒ 検査の削除 0・緩和 0・実質減少 0。**

### 5.4 検査 4 — **定義単位と module 代入の全数 inventory**

| 側 | 定義数 | 削除 | byte 同一 | 変更 | 追加 |
|---|---:|---:|---:|---:|---:|
| P | 330 → **365** | **0** | 295 | 35(**+1,639 B**) | 35(90,492 B) |
| C | 352 → **405** | **0** | 278 | 74(**−30,942 B**) | 53(115,037 B) |

- **module 代入**: P 106 → 121(追加 16 = 11,321 B・**削除 1 = `NATIVE_V9_KEYSETS` 9,102 B**・変更 5 = +20 B)、C 163 → 199(追加 36 = 7,704 B・**削除 0**・変更 6 = −3 B)。
- **C の変更定義が正味 −30,942 B 縮んだ理由は「データの移動」であって検査の削除ではない**: 最大の縮みは `check_seventh_native_keysets` 9,754 → **147** B、`check_sixth_native_keysets` 9,260 → 143 B、`check_fifth_native_keysets` 8,771 → 143 B、`check_v9_intake_header` 2,763 → 262 B など。代表例の逐語 diff は §2.2 に示したとおり、**12 key の literal 集合 + schema literal → 同じラベルの `check_registered_native_keysets(9, …)` 1 行**である。§5.3 の呼出数(すべて増加)と併せて、**削除された検査は無い**。
- **10 領域の原文同一**: `canonical` / `seal` / `check_seal` / `json_bytes` / `sha` / `require` / `integer` / `same_json` / `file_pin` の **9 本は source segment の sha256 まで一致**。**`read_json` のみ変更で、差分は +1 行 `historical_full_file_contract(root, name, value)`(検査の追加)**。
- **import 集合は P / C とも v10 と 1 行も違わない。** `lru_cache` / `functools.cache` / `_CACHE` の導入は 0 件。

### 5.5 検査 5 — **逆置換検問(3 段)**

私は 3 commit を独立に diff し、hunk 数を自分で数えた(`diff -U0` 基準)。**工房の申告と完全一致。**

| 差分 | 対象 | hunk | 行 | 内容 |
|---|---|---:|---:|---|
| 初回 → repair-1 | driver | **4** | +16 / −3 | **① 理由 literal の単一定義化**(`v11_public_wire_value_reason(name)`)**② 期待文字列の require 由来導出**(`v11_public_wire_value_error_text` が `require(False, reason)` を実行し `str(ValueError)` を返す・拒否しなければ fail-closed)**③ canary 2 箇所と本番比較器 1 箇所をその helper に付け替え**。**検査の追加であって緩和ではない**(手書き prefix と実 formatter の乖離という初回の失敗型を構造的に閉じた) |
| 初回 → repair-1 | WF | **1** | 2 | driver の bytes + sha256 のみ |
| repair-1 → repair-2 | P | **2** | +11 / −5 | `old_acceptance` / `portable` fixture を **登録表 `current_exact_keys.acceptance` と `current_schema` から導出**+ **`require(sha(canonical(acceptance_table)) == CURRENT_COUNT_INPUT_SHA256, "k128_current_acceptance_registered_table")` を新設**。**14-key gate(P L9575 `acceptance_fourteen_plain_keys`)は一切触れていない — 直ったのは fixture の側**で、これは**強化**(fixture が世代更新で陳腐化しない構造になった) |
| repair-1 → repair-2 | C | **1** | +1 / −1 | `CURRENT_PRODUCER_REGISTRATION` の bytes + sha を repair-2 の P へ |
| repair-1 → repair-2 | driver | **16** | +203 / −14 | 新設 `v11_k128_dry_preconditions()`(+189 行)・`metadata_canary()` の先頭でそれを呼ぶ 1 行・**残りは 14 の module 定数の pin 再結合**(§5.6) |
| repair-1 → repair-2 | WF | **4** | +15 / −15 | P/C/driver と登録 metadata 5 本の bytes + sha |
| repair-1 → repair-2 | 登録 metadata | — | 各 +1 / −1 | P_timing / C_timing / producer_interface / producer_final_adoption / checker_final_adoption(1 行 JSON の差し替え) |

**driver の `require(` 出現は 2,019 → 2,020 → 2,058 と単調増加**(3 段で削除 0)、**追加/削除された def は `+v11_k128_dry_preconditions` のみ**。

#### 5.5.1 repair-2 driver の 14 定数を JSON 構造で全数 diff(私の実装)

| 指標 | 値 |
|---|---:|
| 総 diff | **241** |
| 種別 | **VALUE 241 / ADDED 0 / REMOVED 0 / TYPE 0 / LEN 0** |
| leaf 別 | `file` 102・`sha256` 58・`bytes` 51(= pin 再結合 **211**)/ `first_line` 15・`offset` 15(= P が 60 B 伸びた分の source region 再計算 **30**) |

**⇒ key の追加・削除・型変更・配列長変化は 1 件も無い。`name` / `rejected_count` / `expected_completion_order` / `stage_rules` / `case_count` / gate ラベルは不変。**

### 5.6 検査 6 — **F-v10-2 の実バイト結合**(著者 wire が実値に縛られたか)

1. **repo 側**: 私が 8 本の sha256 を計算 → WF の 8 組の `PUBLIC_METADATA_*_BYTES` / `*_SHA256` と**完全一致**(§1.1)。
2. **in-run**: WF が 3 箇所で `stat` + `sha256sum -c`(repo 側 / report 側 / run 後)。`driver-bootstrap-stdout.log` の 52 OK 行に 8 本すべてが現れる。
3. **公刊受領証**: `shared-tcb.registered_public_metadata` と `run-receipt.registered_public_metadata` が 8 本の `{copy, original}` 対を bytes + sha で記録し、**両者の値は一致**(= 同梱コピーと repo 原本が同一バイト)。さらに `public-metadata-after-*.json` が **20 段階の工程ごとに**同じ対を再記録する。
4. **値の結合**: `keysets.json` の canonical = artifact 同梱登録表の `current_count_inputs` の canonical = P11 の `CURRENT_COUNT_INPUT_SHA256`(私の独立計算で三者一致)。`producer_interface.json` は dry 契約の格納先で、その `k128_registration_dry_canary_contract_D3` が **自身の canonical bytes と sha を宣言**し、driver が `publication['bytes'] == len(raw) and publication['sha256'] == sha(raw)` を要求(`v11-k128-dry-whole-publication-D2`)。
5. **否定側**: `metadata-gate.json` の **5 本の public-wire canary** が、各登録 metadata の 1 スカラーだけを変えた負例を作り、**同一の本番比較器**で `batch_workflow:v11-public-wire-whole-registered-value:<name>` で落ちることを要求。各 canary は `positive_ordinary_comparator_passed: true`(正例が同じ比較器を通る)・`registered_value_unchanged: true`・`copy_D3_adjusted_only: true` を併記する。**分離条件つきの非空虚な否定例。**
6. **自己参照の不在**: 8 本とも自分の sha256 を含まない(循環なし)。

**⇒ v9 / v10 で 2 期にわたり「形式検査のみ」と書いてきた限定は、今期消えた。**

### 5.7 検査 7 — 計器が判定経路に触れていないこと(telemetry only)

| 受領証 | bytes | 自己申告 |
|---|---:|---|
| `parent-timing-receipt.json` | **7,026,514** | `status PASS` / `outer_expected_count 63` / **63 件すべて OBSERVED**(live-parent 23 + intake-inventory 23 + native-intake 9 + directory-restoration 8)/ `errors []` / `causal_mechanism_identified false` / `mathematical_success_inferred false` / `inclusive_intervals_added_together false` / `candidate false` / `cross_checked false` / `verified false` |
| `parent-authentication-timing-receipt.json` | **8,881,103** | v10 と同型(COMPLETE_MEASURED_SCOPE + 4 抑制 flag) |
| `native-metadata-operations-receipt.json` | **8,854,579** | 同上 |
| `runtime-observation.json` | 428 超 | **`cpu_model` を追加**。`cost-receipt.limitations[5]` が「共変量にすぎず timing の原因を同定しない」と明記 |

**dry 契約も判定経路ではない**: `v11_k128_dry_preconditions()` は `metadata_canary()` の先頭で**静的整合のみ**を検査し、`new_runtime_results is None` / `target_execution_import_AST_compile_selftest == 0` / 各 case `actual_target_rejection_observed is None` を要求する(= 実行結果を作らない・実拒否を主張しない)。**ただしこれは「metadata 群の PASS 条件に静的契約が加わった」という意味では gate である**(通らなければ metadata admission が落ちる)。**計測値が判定に入るのではなく、公開契約と実 source の整合が判定に入る**点を区別して読むこと。

### 5.8 検査 8 — 空虚性(第 10 群と dry 契約)

**P 第 10 群 `batch-parent2474-native-and-current-contracts`(14 拒否)** は v10 第 9 群と同じ構成(別プロセス child + production 束縛 + 正例先行 + no-op guard + 期待エラー完全一致 + fail-closed + 事後 inventory 不変)。ラベル群 `parent2474_added_key_is_absent` / `parent2474_removed_key_is_present` / `parent2474_actual_nonzero_canonical_mutation` / `parent2474_exact_twelve_positive_definitions` / `parent2474_fourteen_rejections_and_original_positive_raw_unchanged` / `parent2474_source_registry_and_current_checker_raw_unchanged` / `parent2474_uses_existing_second_child_and_original_deadline` が新設され、**`parent2474_current_checker_actual_full_raw_D3`(C の実 raw D3 を読む)**も加わった。
**C 第 10 群 `batch-parent2474-eight-layer-admission`(13 拒否)** は `c11_parent2474_local0_not_v3…v9`(7)・`c11_parent2474_native22_projection`・`c11_parent2474_complete1121_zero_retained`・`c11_parent2474_previous_is_v10_start_target`・`c11_parent2474_registered_empty_directory_eof`・`c11_parent2474_unobserved_oracle_stays_null`・`c11_parent2474_old_selection_lambda_contract`。
**dry 契約(30 case)** の非空虚性は別種である。driver は各 case について **実 `REGISTRATION` / 実登録表から負例を組み立て直し、宣言された「最初に落ちる条件」がその位置で実際に偽になること**を再計算する(例: registration 系は 5 段の述語列 `states` を作り `all(states[:index]) and not states[index]` を要求、`NOT_ORDINARY_INT_EQUAL` は `expected` が実登録値と canonical 一致することを要求、`FAIL_SEQUENCE_SCOPE` は `limit = 6 × 128 + initial_checkpoints − 1` を実表から再計算)。**つまり「gate 表が実物と矛盾しない」ことは実計算で確かめられている。実 P がその gate で落ちる観測は含まない(限定条項 8)。**

---

## 6. selftest(**10 群**・件数は実 stdout から私が数えた)

| 側 | 群 | 件数(**stdout 実数**) | driver 登録 | run-receipt | 判定 |
|---|---|---:|---:|---:|---|
| P | `k128-version-registration-and-types` | **30** | 30 | 30 | PASS |
| P | `k128-full-roster-cutoff-and-restoration` | **10** | 10 | 10 | PASS |
| P | `batch-parent1578-admission-and-projection` | **6** | 6 | 6 | PASS |
| P | `batch-parent1706-two-layer-admission` | **7** | 7 | 7 | PASS |
| P | `batch-parent1834-three-layer-admission` | **8** | 8 | 8 | PASS |
| P | `batch-parent1962-four-layer-admission` | **8** | 8 | 8 | PASS |
| P | `batch-parent2090-five-layer-admission` | **12** | 12 | 12 | PASS |
| P | `production-registered-key-contract` | **1** | 1 | 1 | PASS |
| P | `batch-parent2346-seven-layer-and-current-contracts` | **29** | 29 | 29 | PASS |
| P | **`batch-parent2474-native-and-current-contracts`** | **14** | 14 | 14 | PASS(**新設**) |
| C | `k128-version-registration-and-types` | **28** | 28 | 28 | PASS |
| C | `k128-full-roster-cutoff-and-restoration` | **9** | 9 | 9 | PASS |
| C | `batch-parent1578-admission-and-projection` | **6** | 6 | 6 | PASS |
| C | `batch-parent1706-two-layer-admission` | **7** | 7 | 7 | PASS |
| C | `batch-parent1834-three-layer-admission` | **8** | 8 | 8 | PASS |
| C | `batch-parent1962-four-layer-admission` | **10** | 10 | 10 | PASS |
| C | `batch-parent2090-five-layer-admission` | **14** | 14 | 14 | PASS |
| C | `batch-parent2218-six-layer-admission` | **15** | 15 | 15 | PASS |
| C | `batch-parent2346-seven-layer-admission` | **20** | 20 | 20 | PASS |
| C | **`batch-parent2474-eight-layer-admission`** | **13** | 13 | 13 | PASS(**新設**) |

- **三系一致**: 実 stdout の `rejected_cases` 実数 = driver 登録値 = `run-receipt.new_selftest_rejections_registered` = `{"producer-selftest":[30,10,6,7,8,8,12,1,29,14], "checker-selftest":[28,9,6,7,8,10,14,15,20,13]}`。**P 125 + C 130 = 255 拒否**(v10 は 111 + 117 = 228)。`new_selftest_groups_registered = {"producer": 10, "checker": 10}`。
- **gate 一致**: `producer-selftest-gate` = 2 + 7 + 1 = **10**、`checker-selftest-gate` = 2 + 8 + 0 = **10**。
- **metadata 群**: `metadata-gate.json` が `metadata_regression_cases: 16`(v7 以来同数)+ **`registered_public_wire_canary_cases: 5`**、`run-receipt` が **`all_metadata_canary_cases_registered: 21`** / `public_wire_canary_cases_registered: 5` / `metadata_regression_cases_registered: 16`。
- **in-run 実行の証拠**: producer / checker / 両 selftest / metadata / driver-bootstrap の **exit code 6 本すべてが `0`**(私が実バイトで確認)。selftest stdout の `schema` は `…v11.selftest`、`status PASS` / `candidate false` / `cross_checked false` / `verified false` / `actual_anchor_arithmetic_replayed false` / `old_success_suites 0`。
- `run-receipt.selftest_group_scopes` に `"one-side-specific-eighth-metadata-group"` / `"one-side-specific-ninth-metadata-group"` / 第 10 群相当が**事前登録**されている。

---

## 7. 格付け提案

**CV-9 = 同一対象(SAME OBJECT)・限定 8 条 → 工房格付け案: checker PASS / cross-checked(限定 8 条)・rank 2602 / gen 9307(state_head `b180ec9401b830d835aa005174b3c4906d0333999f4b1afafb52875dc79bbde0`・run 34756692935 / attempt 1)を受理・`verified=false`・GRADE2 NOT_DECIDED・`full_A0=false`・A0 actual 0/1 不変。v10 の rank 2474 の直系後継として置き換える(合算ではない)。rank 2602 の sealed object は 1 本。**

**司令塔への一行**: v11 は **v10 の前件 4 件をすべて解消**した — **F-v10-2 解消**(著者 wire 6 本が repo 内の登録 metadata 8 本になり、WF が in-run で 3 度 bytes+sha を検証、8 本とも厳密 canonical、`keysets.json` は artifact 同梱登録表の canonical と 1 バイト違わず P11 の literal とも一致、自己 SHA 循環なし、5 本の負例 canary つき)、**F-v10-8 解消**(P の `NATIVE_V9_KEYSETS` 9,102 B を削除し、両側が別実装で登録 snapshot を読む。C は自前の `HISTORICAL_INDEPENDENT_KEY_COUNTS` と role/namespace 定数で snapshot を拘束し、`check()` は keys と schema の両方を要求)、**F-v10-11 解消**(`cpu_model` を記録し「共変量にすぎない」と明記)、**F-v10-16 混入なし**(`math_head` 0 件)。**F-v11-1 / F-v11-2 も解消**(canary 期待文字列は実 `require` から導出、fixture は登録表から導出し新 require を 1 本追加、dry 契約 30 case / 24 range / 34 label は実登録値から再計算)。**第 23 親 batch-parent-v10 は 14-key acceptance で入場**(私が公刊 acceptance の key を数えて 14・内包 pin は v10 正本 付録 A の実測と一致・**再走 34735785100 は受理 artifact に不在**)。**fresh λ_2474 は current 35,626 / old 35,780 として正しく記録**され current 側は C が独立に 35,626 / selected 128 を再計算。**弱化は 1 件も検出できなかった** — 定義削除 0(P/C とも)・module 定数削除は歴史 literal 1 本のみ・helper 呼出は全種増加・条件式の緩和 0・逆置換 3 段の全差分は「理由 formatter の一本化」「fixture の登録表導出」「dry 契約の新設」「pin 再結合」に限られ、**repair-2 driver の 241 件の定数差分はすべて VALUE 型(key の追加・削除・型変更・配列長変化 0)**。残す宿題は **限定条項 8(dry は実拒否の観測ではない)** と **限定条項 5(登録物の内容を決めたのは harness 著者)**。

### 7.1 診断(**gate ではない** — 裁定 2225 / 2303 / memory「cost-extrapolation-needs-math-review」)

- 実測: producer **2,047.513 s**(cap 5,400 の **37.9 %**)/ checker **2,304.022 s**(cap 10,800 の **21.3 %**)/ P+C **4,351.535 s**。P 残差 **602.179 s**(v10 は 442.865)。
- 候補相: p1 **1,019.790 s(71.2 %)**/ primal 308.250 / reduction 47.765 / source 32.806 / raw 13.389 / B 9.536。**律速は 11 run 連続で P1 補正相。**
- **交絡の扱い**: v10 判読 §7.1 で指摘した「runner 速度が層費用の系列比較を壊す」問題に対し、v11 は `cpu_model`(AMD EPYC 7763)を記録した。**ただし 1 run 分の観測では共変量として使えるだけで、v10 の runner と同型だったかは本書では確定していない**(v10 の receipt に CPU 型が無いため)。**費用モデルの更新・外挿は本判読では行わない。**
- phase counts: 6 相すべて 128 / 128、final 1 / 1、selection 3 / 3、processed 128。

### 7.2 v12 の前件として裁定に載せるべき所見 F-v11-*

| 札 | タグ | 内容 |
|---|---|---|
| **F-v11-1** | 【解消・記録】 | **canary 期待文字列の require 由来導出**(repair-1)。公刊 5 canary の `reason` が `batch_workflow:` prefix つきで記録された。**v12 でも「期待エラー文字列を第 2 の literal として持たない」規律を維持すること**(裁定 2310 の再発防止) |
| **F-v11-2** | 【解消・記録】 | **fixture の登録表導出 + dry 契約**(repair-2)。`k128_current_acceptance_registered_table` の新設で fixture が世代更新に追随する。**v12 では「新しい親を足したら fixture が自動で 15 key になる」ことを第 1 群の否定例で 1 本撃つと、裁定 2312 型の再発が構造的に消える** |
| **F-v11-3** | **【要修正・新設】** | **dry 契約は実 P 拒否の観測ではない**(限定条項 8)。30 case の `actual_target_rejection_observed` は全件 `null`。**v12 では dry が主張する gate 表のうち、少なくとも第 1・2 群で実際に観測された 40 拒否との対応表を receipt に 1 枚足すこと**(静的整合と実観測の橋渡し) |
| **F-v11-4** | 【軽微・新設】 | **登録 metadata の内容を決めたのは harness 著者**(限定条項 5 の残余)。repo 内・in-run 検証・canonical 一致まで来たが、`historical-keysets.json` の keys 自体を外部から縛るのは **C 自身の `HISTORICAL_INDEPENDENT_KEY_COUNTS`(これも同著者)** と「P/C が別実装で読む」ことのみ。**v12 では歴史 keyset を親 artifact の実バイトから再導出して snapshot と突合する検査を 1 本足せば、この条は消せる** |
| **F-v11-5** | 【一次データ・射程】 | **失敗数は今期 −154(35,780 → 35,626)。9 世代の隣接差 −170/−102/−81/+79/+107/−460/+133/−154 で増加は 3 回。単調減少は成り立たない。** 残工程見積りを roster サイズで語る記述は台帳・地図から外したままにすること |
| **F-v11-6** | 【診断・継続(F-v10-11 の後段)】 | **CPU 型は記録されたが、v10 以前の receipt には無いため世代間比較の交絡はまだ切れていない。** v12 以降も記録を続け、**同一 CPU 型の run が 2 つ揃った時点で初めて層費用の比較を数学者に渡すこと** |
| **F-v11-7** | 【軽微・継続(F-v8-2 / F-v10-12)】 | **P は C を file 名でしか pin しない**(5 版連続)。ただし第 10 群に `parent2474_current_checker_actual_full_raw_D3` が入り、**P の selftest は C の実 raw D3 を読むようになった** — 次版で本走側にも広げれば非対称は解消しうる |
| **F-v11-8** | 【軽微・継続(F-k64-7)】 | **C の相別 timestamp は依然無い。** `cost-receipt.limitations[1]` は v9 以来逐語同一 |
| **F-v11-9** | 【今期は非該当】 | v11 系譜で候補 artifact を出したのは repair-2 のみ(初回・repair-1 は fail-closed)。**rank 2602 の sealed object は 1 本。** rank の引用に state_head を併記する運用は継続 |
| **F-v11-10** | 【軽微・継続】 | **F-v5-2 / F-v5-3 / F-v5-4**: fixture 被覆窓・envelope 履歴(今期は fail-closed 2 本が envelope 内で正しく落ちた)・`basis-tau.u8` の二重索引(`basis_chords [2,3,4,6,11]` は今期も受領証に規約が未明示) |

---

## 付録 A. 私自身が sha256 を計算した対象

| 対象 | bytes | sha256 |
|---|---:|---|
| `search/d972_r07_fixed_lambda_cycle_batch_v11.py` | 1,129,263 | `7ec45483543d189eaf42ba2ddf92fddbe58d05aac02d3070a23a833778401e7c` |
| `search/check_d972_r07_fixed_lambda_cycle_batch_v11.py` | 949,977 | `4d522af166c78e5b0ea69ee30bd6df53c62b1ec6a6f3aa91ed3c681079533b71` |
| `search/d972_r07_fixed_lambda_cycle_batch_v11_workflow_driver_v1.py` | 63,275,225 | `b7b7b73cee231c2f396c16b6ceabe9053c50363269d11702f87a82cbbb2a9224` |
| `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v11.yml` | 69,996 | `555631a754ac9a27a89803d891cd1e3edab367a39f5dfcc5111cb6cd2925ba1b` |
| 登録 metadata 8 本 | §1.1 の表 | 同上(8 件すべて WF pin と一致・厳密 canonical) |
| artifact `audit-region-registry.json` | 30,574,417 | `76f148d5c05ff02a01944b90a95af4abcfe024e0a53eef29b3dc53e28bd396c2` |
| その canonical `new_source_audit.current_count_inputs` | 13,234 | `be2747fe98bfd884fc7b48a3b90e8bf842d42f5abc8a6290cce20a70199b7666` |
| artifact `acceptance.json` | 20,271,337 | `c53e0d845ecfbb67fe0b64a7f1c4328fceb8c619adef67cce96addd5f46ff205` |

私が実バイトを取得して読んだ artifact entry: `output/HEAD` 1,259・`output/result.json` 209,022 相当・`checker-result.json`・`cost-receipt.json`・`output/final/manifest.json` 1,927・`output/owner.json` 1,053・`output/progress/HEAD` 837・`output/selection/start.json` 1,117・`output/selection/tree/tree.json` 432・`output/parent-intake.json` 14,316・`run-receipt.json` 1,339,582・`shared-tcb.json` 26,075・`runtime-observation.json`・`metadata-gate.json` 6,668・`producer-selftest-gate.json` 2,103・`checker-selftest-gate.json` 2,095・`producer-selftest-stdout.json` 8,513・`checker-selftest-stdout.json` 8,690・`driver-bootstrap-stdout.log` 5,123・exit code 6 本・`checker-stderr.log` 1,425,673・`parent-timing-receipt.json` 7,026,514・`public-metadata-after-final.json` 2,917・`audit-region-registry.json`・`acceptance.json`。`output/selection/tree/failed-indices.u32` は entry サイズ **142,504 B** のみ(= 4 × 35,626)。

## 付録 B. 判読者の限界(正直な申告)

- 旧 2,474 行の実バイトを取得していないので、λ_new ⊥ 旧行 と ρ₂ 恒等式の旧行部分は checker の再現に依存している(限定条項 4)。
- **本判読は増分規律に従い、「128 行の階段形・λ の後退代入 48,384 座標・target 恒等式 128 段・rolling 鎖 128/128」の全数再計算を今期も行っていない。** 本書が実測で閉じたのは付録 A の対象・登録表からの導出量(現行 8 層 view と 7 層 prefix view)・公刊 JSON の key 数 9 種・外側 63 区間・selftest 255 件・`require` ラベル diff(全数)・条件式 diff(同名単一ラベル全数)・全 helper のラベル対 diff(全数)・**関数呼出の全数計数**・定義単位 inventory(全数)・module 代入 inventory(全数)・**3 commit の hunk 全数と driver 定数 241 件の JSON 構造 diff** である。**「算術が正しい」ことの本期の根拠は C の PASS と §3 の群別確認であり、私の再計算ではない。**
- old λ_2346 の残差表を私自身は再計算していない(限定条項 2)。
- `producer_interface.json`(116,242 B)の全内容、`historical-keysets.json`(71,827 B)の全 keys、`historical-keysets-provenance.json`(345,456 B)は**読んでいない**。私が確認したのは bytes+sha の一致と canonical 性、および driver / C が課す構造条件である。
- `output/parent-layout.json` と `output/start.json`、`acceptance.json` の入れ子(top-level key と `batch_anchor_v10` 以外)は読んでいない。`parent-layout` の 16 key は登録表と C の独立和による。
- 第 10 群 child の実出力(`child-execution.json` 等)と dry 契約の実受領証は取得していない。非空虚性の判定は **source の逐語読解 + 公刊 stdout の `rejected_cases` 実数 + gate の受領証**に依拠している。
- `sparse_adjoint` / `vectorized_projection_chunk` が本 run の実行経路で呼ばれた行は特定していない。
- Release ミラー・診断 artifact 10319095955 は確認していない。初回 34746915217 / repair-1 34753243056 の失敗ログ本文も読んでいない(失敗の静的原因は 3 commit の diff で確認)。
- **この観点では仕様の齟齬(別対象)も検査の弱化も見つけられなかった — 保証ではない。**

---

**裁定 2317(司令塔・2026-09-13)格付け**: 本判読(63,495 B/c08c767c…・工房 sha256sum で pin)を正本として採用。CV-9 = 同一対象・限定 8 条(新設 1 = dry は実拒否の観測ではない・解消 1 = 歴史 keyset literal)→ **rank 2602/gen 9307(state_head b180ec94…・run 34756692935/1)を cross-checked(限定 8 条)で受理**・v10 の 2474 の直系後継として置換・verified=false・grade-2 NOT_DECIDED・full_A0=false・seal 1 本。逆置換 3 段は通過・弱化 0 件。F-v11-1〜10 を v12 の前件・所見として台帳 2317 に登録(要修正 = F-v11-3 dry と実拒否の対応表・軽微 = F-v11-4 歴史 keyset の親 artifact からの再導出)。
