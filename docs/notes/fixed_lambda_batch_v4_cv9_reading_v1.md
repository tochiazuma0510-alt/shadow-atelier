# 増分 CV-9 判読 — R07 fixed-lambda cycle batch **v4 / envelope-v3 / k = 128**(rank 1578 → 1706・fresh λ_1578 oracle 初回)

対象 run: **34120585268 / attempt 1**(success・event=push・head `92720e5371164545259c3007cb11e951fa5e1686`・12:12:10Z → 13:19:18Z・workflow name `d972-r07-fixed-lambda-cycle-batch-v4-envelope-v3`)
候補 artifact **10020349387**(377,383,320 B・API digest `sha256:84040119b08d4ee1e9a3b4524618164172f382f9a97314084131bb9fd0a3cac5`)
判読者: falsifier(非当事者・事後)。判読日 2026-09-07。
前回 CV-9 正本: `docs/notes/fixed_lambda_batch_v3_cv9_reading_v1.md`(裁定 2187・限定 8 条)。

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 7 条(§9)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 7 条)・rank 1706 / gen 8411 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。v3 の rank 1578 の直系後継であり、v1(1482)・v2(1514)・control-96(1482)とは合算しない。**

**a(128) = 128**(offered 128 / accepted 128 / dependent 0 / skipped 0)。ただしこれは v3 の a(128) の再現ではない — **λ が別物なので選定 128 弦は v3 と共通元 0 個**であり、完全に新しい 128 本である(§4.3)。

三つの見出し:

1. **【解消 F-k64-1】DEPENDENT 枝は本番コードで実際に通った。** 私が v3 判読で出した唯一の未解決指摘が閉じた。P 側 `k128_dependent_continuation_canary`(P4 L4054–4186)・C 側 `k128_dependent_publication_canary`(C4 L3262–3399)が第 2 群に入り、**実 fixture 生データを artifact から取得して私が独立に検算**した(§6)。「独立 → 非零従属(係数 2)→ 次独立」の三段が P/C 別々の数値で成立し、再 seal 陰性も両側に実在する。事前登録 P[30,10,6] / C[28,9,6] は driver の literal と実測が完全一致。
2. **【新規・重大な一次データ】fresh λ による失敗集合の入れ替わりを初めて測った。** 旧 λ_1450 の失敗 36,274 と新 λ_1578 の失敗 36,104 は、**共通 24,041・旧のみ 12,233・新のみ 12,063**(Jaccard 0.497)。**正味の減少は 170 本にすぎない**(§4.2)。同時に、**v3 が消費した 128 弦は新 λ の下で 128/128 が充足に転じた**(乱択 128 本の期待値 ≈ 42.7・200 回の最大 57)。すなわち「消費した弦は恒久的に片付く」は実データで確認されたが、**roster 全体は縮む作業待ち行列ではない**。Task 988 F4 に対して、これは v3 判読時点では取れなかった型の情報である。
3. **【要修正 F-v4-1】費用モデル `fixed(k) ≈ 26.0 + 1.273k` は k 単独の関数としては外れた。** 同じ k = 128 で計測外固定費が **189.963 → 232.786 s(+22.5 %)**。機構は特定できた(第 16 親 = batch-parent 369 MB / 11,437 file の認証が P/C 両方に新設)。候補 ZIP の底は +2.2 % しか伸びていないので、これは主に**一回性の構造費**と読むのが最良で、**k_max ≈ 429**(v3 の 433 から実質不変)。ただし二読みを分ける安価な次観測がある(§7.4)。

同一性の根拠(すべて私の第三実装が生バイトから再導出。P/C の PASS フラグは根拠に使っていない):

- **選定 oracle の完全再現**: `chord-residuals.u8` を `(values − tau·fit) mod 3` で全 54,433 弦ぶん再計算し公刊配列と**バイト完全一致**(不一致 0)。失敗 **36,104** 件・先頭 index **74**・先頭 edge **131** を再現し `failed-indices.u32` / `failed-edges.u32` と**全件バイト一致**。基準 5 弦 [2,3,4,6,11] の残差 5/5 = 0・fit `[2,1,0,0,2]`(v3 の `[1,1,2,1,0]` から変化 = λ 依存)。
- **λ の系譜**: v3 候補の `output/final/lambda.bin` の sha = `6a0fe9368f2ec7f2…` = 本 run の `selection_lambda_sha256`。**v3 が産んだ λ をそのまま oracle に食わせている**ことを両 artifact の実バイトで確認。v3 の `state_head e793896e…` = 本 run の anchor head、v3 の `target_remainder 7868b780…` = 本 run の start target。
- **消去構造**: 128 本の normalized 行を生バイトから復元し、自 lead で 1 が **128/128**、先行 lead で 0 が**違反 0 件**、後続 lead で非零が **5,423 箇所** → **RREF ではなく挿入順前進消去**。→ **階段形+相異なる pivot 128 個なので 128 本の一次独立は定理として従う**(producer の INDEPENDENT フラグに依存しない)。
- **λ(F1)**: λ_new ⊥ 新 128 行が **128/128 で 0**、λ_new·t_final = 1、λ_new·t₀ = 1、`row_pairings_sha256 = 84a8935d…` = **sha(0x00 × 1706)** を手計算一致。**λ の 128 個の新 lead 成分を逆順後退代入で完全再現**(不一致 0・非零 79)、**復元 λ 配列 == 公刊 λ**。
- **target 恒等式**: t_final に θ_j·n_j を逆順に足し戻して t₀ を再構成 → packed sha が **`7868b7806a0dc41c2bda8a1c4c6a10d1cfa2c2e6968aadf561e93820f12053e1` = 親 target** と一致。θ ≠ 0 が **81/128** なので非空虚。
- **鎖**: `rolling_sha256 = sha(bytes.fromhex(predecessor) ‖ canonical(body))` を式ごと再実装し、anchor `e793896e…` から **128 段連続で 128/128 再計算一致**、最終 = `state_head 13c631c6…`。`predecessor` 連結 128/128、`physical_offset = 12096×(1578+i)` が 128/128、instruction/row-manifest の自 seal が各 128/128。
- **fixed 参照**: 親(v3 候補)の `output/fixed/` は **manifest.json 一件のみ**、実 payload 16 本(10,304,823 B)は旧 64 continuation 側。両者を結ぶ受領証を検算し、`chord-tau.u8` が fixed payload と **tree 段出力でバイト同一**であることを確認 = 参照経由で実データが実際に流れている(§3)。
- **registry v2**: driver の `br'''…'''` から抽出した原文が **236,390 B / `84f5bbc6a85e77915535968e4342c09b6bf3e5b94638ab14184c67ca677ce114`**、artifact 同梱 `audit-region-registry.json` と**バイト完全一致**。**472 区間・254 分類を repo 実バイトで全数再計算し不一致 0**(§1.2)。
- **source**: `checkout-sources/` 24 + `audit-history-sources/` 6 = **30/30 が repo 作業ツリーとバイト全一致**。
- **配置 pin**: WF 22,153/`56a8349f…`・driver_v2 536,145/`35f73f5d…`・P 290,457/`a58f7c11…`・C 261,170/`a29380ec…`・旧 P archive 284,974/`3ba71767…`・旧小 WF archive 20,296/`c8dc6981…` の 6 件を repo で再計測し 2197 の pin と全一致。

---

## 1. (1) 規約表 diff

### 1.1 v3(k=128) → v4(envelope-v3)

| 規約 | v3 の宣言 | **v4 の宣言** | 本 run の実測 | 判別性 |
|---|---|---|---|---|
| `batch_size` / `max_batches` / `refill` | 128 / 1 / False | **同一** | selected 128 / processed 128 / refill False | — |
| `selection_policy` | `CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX` | **同一文字列** | roster 昇順先頭 128(index 74..393) | **判別**(gap≠1 が 67/127) |
| `partial_policy` | `PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY` | 同 | `partial=False` | — |
| caps | 5400s/7168MiB・10800s/7168MiB(outer 6000/11400) | **同(不変)** | 実 1,669.026 / 2,014.299 s(harness 外形) | — |
| **親** | continuation(rank 1450・artifact 9977040548) | **batch-parent = v3 候補 9987222571(rank 1578/gen 8283)+ continuation を第 16 role として併存** | 16 role 全取得・保全 flags 25/25 | **層構造が変わった最大点** |
| **選定 λ** | λ_1450(`7c0dbe47…`) | **λ_1578(`6a0fe936…`)= v3 の final λ** | start.json / separator が同 sha | **本 run の核心(§4)** |
| basis(固定 5 弦) | [2,3,4,6,11] | 同 | 残差 5/5 = 0 | fit は `[1,1,2,1,0]` → **`[2,1,0,0,2]`**(λ 依存・正しい挙動) |
| Ω 語化・target 減算符号・correction 符号 | 三規約文字列 | **同一文字列** | §8.2 の三層で非空虚に判別 | **強化**(§8.2) |
| ρ₂ | `mode=derived, value=1, directly_read=False`・accepted target-derivation parents **97** | 同・**225**(= 97 + v3 の 128) | separator の `lambda_rho2` に 225 と `anchor_accepted_parent_batch_rows=128` | **DERIVED のまま**(未昇格) |
| lower-zero | `source_lower_zero = NOT_ASSERTED` / `physical_lower_zero = true` | 同 | separator に同値 | **契約どおり** |
| terminal | 3 値 | 同 | `BATCH_COMPLETE_CANDIDATE` | 他 2 値は canary のみ |
| **selftest 群** | **2 群**・実拒否 P[30,9] / C[28,8] | **3 群**(`k128-version-registration-and-types` / `k128-full-roster-cutoff-and-restoration` / **`batch-parent1578-admission-and-projection`**)・**P[30,10,6] / C[28,9,6]** | 三群とも PASS・exit 0・件数完全一致 | **§6 = F-k64-1 の解消** |
| metadata canary | 16 件・`metadata_regression_from: …-v1` | 同 16 件・同 v1 | 16/16 拒否 PASS・`rejected_count=16` | 継承の明記は従来どおり |
| 静的 registry | `…v4.audit-registry.v1`(task 1055)・136 P 区間 | **`…v4.audit-registry.v2`(task 1064)・137 P 区間**・236,390 B/`84f5bbc6…` | **472 区間 / 254 分類を私が全数再計算・不一致 0** | §1.2 |
| shared TCB | 4 kernel | 同 4 kernel(13,187 B/`d94ffbe0…`) | **4/4 を repo 実バイトで再計算・一致**・`sparse_adjoint` は P/C バイト同一 | `NOT_MEASURED` 継続 |
| **freeze の位相** | driver が WF 内 inline(283,886 B・3,601 行) | **driver が repo file(536,145 B)・WF は 22,153 B の小 envelope** | WF が driver sha を **literal env** で保持し実行前後に `sha256sum --check` + `cmp` | **§2.3 で評価**(弱化ではない) |

→ **凍結宣言と実装・実データの間に齟齬は見つからなかった。緩めた箇所は 1 つも無い。**

### 1.2 registry v2 の全数再計算(私の第三実装)

driver_v2 の `INHERITANCE_REGISTRY_RAW` を抽出 → 236,390 B / `84f5bbc6…`(申告 pin と一致・artifact 同梱ファイルともバイト一致)。

| 検査 | 結果 |
|---|---|
| `source_files` 8 件(P1–P4 / C1–C4)の bytes / sha256 / lf / cr / bom / final_lf | **8/8 を repo 実バイトで再計算・一致** |
| P 側 baseline(P3)122 区間 + current(P4)137 区間の bytes / sha256 | **259/259 一致・不一致 0** |
| C 側 baseline(C3)96 + current(C4)117 | **213/213 一致・不一致 0** |
| 被覆(gap / overlap / EOF) | **4 source すべてで 1 行目から `lf` 行目まで隙間・重複なし**(私が独立に検算) |
| 分類 254 件の整合(UNCHANGED なら両版 sha 同一・CHANGED なら相異・ADDED は baseline_ordinal = null) | **254/254 整合・矛盾 0** |
| P: 104 UNCHANGED / 18 CHANGED / 15 ADDED、C: 79 / 17 / 21、削除 0 | 一致(2197 の記載どおり) |
| 不変バイト率 | P **146,269 / 290,457 = 50.4 %**(2,295 行)、C **105,668 / 261,170 = 40.5 %**(1,673 行) |

**算術核が UNCHANGED 側にあることを確認**: `reduce_candidate_numeric` / `advance_reduction_numeric` / `final_separator_numeric` / `classify_batch` / `make_reduction_state` / `f3_array` / `current_batch_tree` / `encode_array` / `decode_array`(P)と `select_all_residuals`(C)がすべて **P3/C3 とバイト同一**。

**18 の P 側 CHANGED を全部読んだ**(数学的意味の確認):

| symbol | 実差分 | 数学的意味 |
|---|---|---|
| `character_counts`(414 行) | **+2 行のみ**(`REGISTERED_ARTIFACTS["batch-parent"] = BATCH_PARENT_ARTIFACT` と空行) | 無し |
| `authenticate_acceptance` | acceptance の key が 6 → **7**(`batch_anchor` 追加)・role 数 15 → **16** | 親層の拡張のみ |
| `current_derived_rho2` | 97 → **225** の accepted target-derivation parents(= 97 + v3 の 128) | **正しい延長**。ρ₂ は依然 DERIVED |
| `final_manifest_value` / `public_head_value` / `result_value` / `run_candidates` / `run_actual` | `anchor_accepted_parent_batch_rows` の追加と `batch_observation` の配線 | 記録面のみ |
| 残り(`MODULE_PREFIX`・`outer_metadata`・`finish_inputs`・`input_preservation`・`validate_host_paths`・`k128_registration_canary`・`selftest`・`diagnostic`・`cli`) | 定数・16 role 対応・canary 総入替 | 無し |

→ **算術本体に手は入っていない。**

### 1.3 v4-envelope-v2 → envelope-v3 の修理(本便の主題)

**P の修理(1065 の作者票)を私が独立に検算した。**

- 差分は **二 hunk のみ**: 新関数 `batch_fixed_reference_manifest` を L1390–1471 に **82 行追加**、`authenticate_batch_parent` 内の caller 2 行 → 1 行。
- **逆置換の検算**: 新 P から L1390–1471 を除去し caller を旧 2 行に戻した bytes が **284,974 B / `3ba71767585b6a49efccb5d20bb60eb8939848669c19692a63018b9486f41d36` と完全一致**(1065 の主張を私が再現)。
- registry ベースの区間比較(旧 P4 136 → 新 P4 137): **135 不変・1 変更(`authenticate_batch_parent`)・1 追加・削除 0**。**C4 は 117/117 完全不変**。

**driver の修理**: 新関数 `batch_fixed_reference`(**84 行**・L3764–3847)+ caller 1 行置換 + registry v1 → v2 の差替え + 冒頭コメント。registry の差分は **P 側に 1 区間(`batch_fixed_reference_manifest`・ADDED_CURRENT)を足しただけ**で、C 側は分類まで完全同一・**UNCHANGED → CHANGED に落ちた区間は 0**。

**修理の意味論**(私の読解): 新 reader は「参照側(batch-parent)には manifest 一件しか無い」「実 payload 16 本は登録済みの continuation 側にある」を **exact roster** で要求し、16 本すべてを `file_pin`(bytes + sha256)で旧 64 側の実ファイルへ結ぶ。JSON 5 本は 5 key → 3 key 射影、binary 11 本は 5 key 保持 + `shape` 積 × dtype 幅 = bytes の EOF 照合。**payload を親へコピー・生成しない**ことを受領証で宣言し、両ディレクトリの `iterdir()` 全数と symlink 不許可まで要求する。→ **数学的対象は変わっていない**(fixed 値は λ 非依存であり、どちらの経路でも同じバイトを読む)。§3 でそれを実データで確かめた。

### 1.4 交差辺(独立性)

- C4 の import は `check_d972_r07_complete_oracle_cegar_continuation_v2` のみ。`importlib` 0。producer 本体への参照は **path 定数 2 行だけ**。
- P4 の `importlib` は自系 `L_FILE`(`L_SHA` pin つき)1 箇所のみ。`check_d972…` の 13 hit は全部ハッシュ pin メタデータ。
- **v1/v2/v3 と同じ二系統分離。**

---

## 2. 事前登録と入力 pin

| 検査 | 結果 |
|---|---|
| 起動 commit | `92720e53`。WF / driver_v2 / P / C の pin が run-receipt・artifact 同梱コピー・**repo 作業ツリー**の三者一致。 |
| 事前登録の凍結 | `REGISTRATION = {batch_size 128, max_batches 1, CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX, PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY, refill False, 5400s/7168MiB, 10800s/7168MiB}` が driver に **literal**(`:31-35`)。 |
| **selftest の事前登録** | `SELFTEST_NAMES` 3 群名と **`SELFTEST_REJECTIONS = {'producer-selftest':[30,10,6],'checker-selftest':[28,9,6]}` が literal**(`:36-38`)。gate(`:4756-4761`)が **群名列の完全一致**と**拒否件数列の完全一致**を要求 → 実測と一致。**試験件数の後付け調整は不可能。** |
| 親 pin | `start['rank'] == 1578 and start['generation'] == 8283 and anchor_completed_steps == 64`(`:5512`)を literal 要求。旧 64 側は `rank == 1450 / generation == 8155`(`:3954`, `:4365`)。 |
| **恒真 gate** | **見つからなかった。** `selected ∈ [0,128]` → `processed ∈ [0,selected]` → `dependent ∈ [0,processed]` → `accepted ∈ [0,processed]`、`rank == 1578 + accepted` / `generation == 8283 + accepted` / `processed == dependent + accepted`(`:5536-5543`)。**accepted は固定されていない** → DEPENDENT が出ても gate は通る。**a(128) = 128 は gate の強制ではない。** 唯一の下限は `selected == 0 or accepted >= 1`。 |
| silent cap | 見つからなかった。`failed[:BATCH_SIZE]`(P4 `:552`)は**登録済み政策そのもの**。上界はすべて `require` で失敗側に落ちる。`progress['sequence'] == 3 + 6×processed`(= 771)と `ordinary(sequence, 0, 771)` の二重。 |
| **予言 gate** | `require(wanted['matches_prediction'] is True, 'conditional-first-independent-under-all-measured-premises')`(driver `:5459`)= **落ちうる硬い gate**。「最初の候補は INDEPENDENT」は前提(親 span が λ で零・raw_pairing = selection_scalar ≠ 0)から**数学的に強制される**較正項目であり、実際に `candidates/000000/{witness,reduction,manifest}.json` を読んで照合されている。**恒真ではないが発見でもない**(§8.3)。 |
| 保存 | `preservation-result.json`: `status PASS`・`errors []`・`missing []`・**flags 25/25 すべて true**・`no_parent_file_renamed_trimmed_or_overwritten true`・`acquired_parent_baselines 16`(v3 は 15)。 |
| 実行 source | `checkout-sources/` 24 + `audit-history-sources/` 6 = **30/30 が repo とバイト全一致**(私が全ファイル取得して比較)。 |
| runtime | `python 3.13.15 / numpy 2.5.1` を `runtime-observation.json` が expected/actual で照合。 |
| artifact | 候補 10020349387 = 377,383,320 B / `84040119…`、診断 10020372140 = **同 bytes** / `7097d7cc…`(私が GitHub API で再取得)。二重保管は v2 で閉じた既知型。 |

### 2.3 freeze 位相の変更(driver が repo file へ出た)の評価

v3 の「WF 一枚 283,886 B に driver 全体が inline」から、v4 は「WF 22,153 B + repo の driver 536,145 B」に分かれた。**弱化ではない**と判定する理由:

- WF が `WORKFLOW_DRIVER_SHA256` / `_BYTES` を **literal env** で持ち、`sha256sum --check --strict` と `cmp` を**配置前(step 1)と最終(step 19)の二回**実行し、両回の `sha256sum` 出力どうしを `cmp` で突合(WF `:220`, `:344-345`)。
- 実行は `$RUNNER_TEMP/…/driver.py`(検証済みコピー)から。
- 7 file の実測 sha が artifact に保存され、私が repo と照合して **7/7 一致**。
- `test "$workflow_bytes" -lt 500000` により WF 自身の肥大も封じている。

ただし **旧 P archive(`ops/source_versions/…-before-reference-repair.py`)はこの 7 file 集合の外**(2197 のとおり非実行履歴)。私が repo 実バイトで独立に pin を確認した(284,974 / `3ba71767…`)。

---

## 3. fixed 参照結合(2196/2198 の追加確認項目 ①)

| 検査 | 結果 |
|---|---|
| 親(v3 候補)側 `output/fixed/` | **manifest.json 一件のみ**(2,903 B / `ba4d2d96b562abc1…`)。受領証 `reference_inventory` が `files:[manifest.json]`・`directories:[]` を宣言 |
| 旧 64 continuation 側 `output/fixed/` | **17 file**(manifest 3,159 B/`3ec178df…` + payload 16 本)。受領証 `payload_inventory` の合計 = **10,307,982 B** = **10,304,823(16 payload)+ 3,159(manifest)** ← 私が加算して一致 |
| 16 payload の内訳 | `basis.json` 38,457 / `bfs-order.u32` 217,728 / `canonical-index.json` 6,078,393 / `carry.u8` 544,320 / `chord-edges.u32` 217,732 / `chord-tau.u8` 272,165 / `geometry.json` 1,067 / `next-pos.u32` 435,456 / `p1-exponent-residues.json` 49,480 / `parent-edge.u32` 217,728 / `parent.u32` 217,728 / `phi.u32` 1,306,368 / `potential-tau.u8` 272,160 / `prev-pos.u32` 435,456 / `selected-chords.u32` 20 / `tag-fox.json` 565 |
| `payloads_copied_or_created` | **false**(親へコピーしていない) |
| 型射影 | `json_descriptors 5` / `binary_descriptors 11`。driver 側で `math.prod(shape) × {u8:1,u32le:4} == bytes` を全 binary に要求 |
| geometry 由来 | 親/旧の `accepted_geometry_stage_sha256` が登録 oracle の `output/geometry/manifest.json` 実 sha `7365fa98…` と三者一致 |
| **λ 非依存の実証** | 本 run の `output/selection/tree/chord-tau.u8`(272,165 B)の sha = **`bcd90726adbc76a64f5b13970da0de66d148aa94422952760f2be9b86240005f`** = fixed manifest の同名 descriptor と一致、かつ **v3 候補の同ファイルとバイト完全同一**。→ **参照経由で実バイトが実際に読まれ、λ が変わっても fixed 値は同一**であることがデータで確認された |
| 本 run の `output/fixed/manifest.json` | 2,903 B / `1a1f4644…`(自 run の owner/source/start に結び直した参照型)。`accepted_fixed_manifest` は旧 64 の 3,159 B/`3ec178df…` を指す → **参照鎖が保存されている** |

→ **2193 の停止原因(層構造の仮定不整合)は、参照型を参照型として受理しつつ実 payload を実 bytes で結ぶ形で解消された。数学対象は不変。**

---

## 4. 【独立節・重点 A】fresh λ_1578 oracle — 本 run の最大の新規情報

### 4.1 oracle の完全再現

| 量 | 公刊 | 私の独立再導出 |
|---|---|---|
| `chords_checked` | 54,433 | 54,433(`chord-values.u8` / `chord-tau.u8` の実長から) |
| 残差配列 | `chord-residuals.u8` | `(values − tau·fit) mod 3` で全 54,433 件再計算 → **バイト完全一致・不一致 0** |
| `failed_count` | **36,104** | **36,104**(残差 ≠ 0 の個数) |
| `failed-indices.u32` | sha `26079aa3…` | 私の昇順配列と **144,416 B バイト一致** |
| `failed-edges.u32` | sha `b11b6be7…` | selection の `selected[].edge` と先頭 128 が一致 |
| `first_failed_index` / `first_failed_edge` | **74 / 131** | **74 / 131** |
| 基準 5 弦 [2,3,4,6,11] | 残差 0 | `tau[basis]·fit ≡ values[basis] (mod 3)` を確認 → **5/5 が 0** |
| `fit` | **[2,1,0,0,2]** | 同(v3 は [1,1,2,1,0]) |
| 残差値分布 | — | 0: 18,329 / 1: 17,956 / 2: 18,148(ほぼ 1/3 ずつ) |
| `auxiliary_tests` / `aux_values` | 2 / [0,0] | **aux 枝は本番未発火**(selftest 側では通る・§8.4) |
| `terminal(selection)` | `VIOLATION_CANDIDATE` | 選定 128 本すべて `kind=chord`・`scalar ∈ {1,2}`(1:66 / 2:62・0 は無し) |

### 4.2 **旧 λ_1450 と新 λ_1578 の失敗集合の比較(初データ)**

| 量 | 値 |
|---|---:|
| 旧 λ_1450 の失敗(v3 の oracle) | **36,274** |
| 新 λ_1578 の失敗(本 run) | **36,104** |
| **正味の差** | **−170** |
| 共通(両方で失敗) | **24,041** |
| **旧のみ = 新 λ で解消した弦** | **12,233** |
| **新のみ = 新 λ で新たに失敗した弦** | **12,063** |
| 和集合 | 48,337 / 54,433 |
| Jaccard 係数 | **0.4974** |
| `chord-tau.u8` の v3/v4 バイト同一性 | **同一**(λ 非依存) |
| `chord-values.u8` の v3/v4 同一性 | **相異**(λ 依存) |

**【最重要】v3 が消費した 128 弦の運命**:

| 検査 | 結果 |
|---|---|
| v3 選定 128 弦が新 λ でまだ失敗している数 | **0 / 128** |
| v3 選定 128 弦が新 λ で残差 0 になった数 | **128 / 128** |
| うち `values_new = 0` かつ `tau·fit_new = 0` | 46 |
| うち両者が等しい非零値 | 82(値のヒストグラムが `tau·fit` のそれと**完全一致**: 0:46 / 1:43 / 2:39) |
| **乱択 128 本の基準線** | 200 回の抽出で **平均 42.7・最大 57** |
| 旧 λ で v3 選定 128 弦が失敗していたか | 128/128(定義どおり) |
| v4 選定 128 弦と v3 選定 128 弦の共通元 | **0** |
| v4 選定 128 弦のうち旧 λ でも失敗していたもの | **39 / 128**(残り 89 は新たに失敗した弦) |

読み方(私の判断):

- 「**消費した弦は次の λ の下で恒久的に充足に転じる**」は、乱択基準線 ≈ 43 に対し 128/128 なので**偶然ではない**。これは設計意図の直接確認であり、**producer が誤った行を足していればこの検査は落ちる**ので、fresh λ が初めて可能にした強い end-to-end 較正である。ただし「定理として強制される」ことを受領証から示したわけではない(§11)。
- 一方で **roster は縮む作業待ち行列ではない**。128 本を消費して 12,233 本が消えたが 12,063 本が新規に現れ、正味は −170。**「失敗数 → 0」を終端条件と見た単純外挿は、この 1 点差分では 36,104 / 170 × 128 ≈ 27,200 行**(rank 余地 46,678 の 58 %)を要求する。**2 点だけの差分であり法則ではない**が、v3 判読の「消化率 0.353 %」という言い方が実は roster の縮小率を意味しないことを、本 run が初めて数値で示した。
- `first_failed_index` が 70 → 74 としか動いていないこと(F10 の非単調性)も、この churn 構造と整合する。

### 4.3 選定 128 本の実体

- roster index **74..393**(span 320)・distinct 128・`failed_indices[0:128]` と**完全一致**。
- gap = 1 が 60、**gap ≠ 1 が 67**、最大 gap 14 → 「先頭 128 整数を機械的に取った」のではないことをデータが判別。
- `witness.kind` は 128/128 が `chord`、`coordinate` は 128/128 が null、`scalar` は 1:66 / 2:62(**0 は無し** = `scalar in (1,2)` の require が非空虚)。
- **v3 の選定集合との共通元 0** → 本 run の 128 本は完全に新しい情報である(v3 が v2 の 64 本を物理行までバイト同一で再現していたのとは対照的)。

### 4.4 情報性の内訳(すべて result.json / 私の λ 実測)

- λ_new の character 別 support = **[1132, 0, 0, 0]** → **character 0 だけが情報的**(継続)。私の実測: 非零 1,132・最小 index 2・最大 index 1819・trit 内訳 [10964, 540, 592]。
- 内訳: 座標 < 1690 が **1,052**、新 lead 帯が **79**、free 座標(1819)が **1**。合計 1,132 ✓。
- λ_new と λ_old(= λ_1578)は **座標 < 1690 の範囲だけで 1,079 箇所異なる** → 前段 λ のコピーではない。
- score `by_tag = [40302, 23364, 23364, 0, 0, 0]`(total 87,030)→ **tag 3〜5 は零**(v3 は [40203, 23052, 23052, 0,0,0])。
- κ: `degree0/degree1` とも **tag 0 のみ非零**(total 5,454)、`kappa aux_values` 8 個すべて 0。
- q: character 0 のみ support 3,156。`p1_equation_residual_support = 0`。

---

## 5. 階段形・独立・λ・target・鎖(F1 全数確認)

| 項目 | 宣言値 | 私の独立検算 |
|---|---|---|
| 128 行の自 lead 係数 | — | **128/128 が 1** |
| 先行 lead での零 | — | **違反 0 件**(strict staircase) |
| 後続 lead での非零 | — | **5,423 箇所** → **RREF ではなく挿入順前進消去** |
| lead 集合 | — | **1690..1818 の 128 個・distinct 128・欠番は 1791 のみ 1 個** |
| lead 付与順 | — | 非単調(降順ステップ 31 回・昇順 96 回)。先頭 12 = [1690,1692,1691,1693,1696,1694,1695,1697,1698,1701,1699,1702] |
| **独立性** | producer の INDEPENDENT フラグ | **階段形+相異なる pivot 128 個から定理として従う**(フラグに依存しない) |
| λ_new ⊥ 新 128 行 | (全 0) | **128/128 で 0** |
| λ_new · t_final | `lambda_new_remainder = 1` | **1** |
| λ_new · t₀ | `lambda_parent_remainder = 1` | **1**(再構成した t₀ に対して) |
| `row_pairings_sha256` | `84a8935d91036a00e62362f5601416d094f4708da6986096f9353659cfa146eb`・`rows 1706` | **sha(0x00 × 1706) と一致** |
| `lambda_pivots` | 0 | 一致 |
| λ の新 lead 成分 | (公刊 λ) | **逆順後退代入で 128/128 完全再現**(不一致 0・非零 79)。**復元 λ 配列 == 公刊 λ** |
| free 座標 | — | **1819**(t_final の最初の非零・値 1・λ[1819]=1)。λ は 1819 より上で全零 |
| t_final support | — | **30,636 / 48,384** |
| **target 恒等式** | 親 `target_remainder_sha256 = 7868b780…` | t_final に θ_j·n_j を**逆順**に足し戻して packed sha が**一致**。θ ≠ 0 が **81/128** で非空虚 |
| target 鎖 | 各 row の `target.json` | `parent_remainder_sha256` の連結が **128/128**、終端 = `954e1ba1…` = 公刊 `target_remainder_sha256` |
| **rolling 鎖** | anchor `e793896e…` → `state_head 13c631c6…` | `sha(bytes.fromhex(predecessor) ‖ canonical(body))` を式ごと再実装し **128 段 128/128 再計算一致**・`predecessor` 連結 128/128 |
| `physical_offset` | — | `12096 × (1578 + i)` が **128/128** |
| 自 seal | — | instruction **128/128**・row manifest **128/128**・主要文書 8/8(result / selection / separator / start / final manifest / fixed manifest / checker-result / tree manifest) |
| 物理行 sha | 各 row manifest | **128/128** が実バイトの sha と一致(instruction の `physical_sha256` とも三者一致) |

**空き座標債務**: frontier(max lead + 1)= **1819**、rank 1706 → 債務 **113**(v3 は frontier 1690 / rank 1578 / 債務 112)。1791 が 1 個飛んだ(挿入順 #100 が 1790、#102 が 1792)。v3 判読の「債務は batch の切り所によって増減する局所量」という訂正どおりの挙動で、**単調でも保存量でもない**ことがもう 1 点で確認された。

**注(構造的・v1 以来不変)**: `row_pairings_sha256` は零ベクトルの sha であり、**実質的には行数しか運ばない受領証**。実効的な内容は `lambda_pivots == 0` と両 remainder = 1、および checker 側の直接測定にある。

---

## 6. 【解消 F-k64-1】DEPENDENT 枝が本番コードで実際に通った

### 6.1 事前登録と実測の一致

| 側 | 事前登録(driver literal) | 実測(`*-selftest-stdout.json`) |
|---|---|---|
| producer | `[30, 10, 6]` | 30 / **10** / 6 — **一致** |
| checker | `[28, 9, 6]` | 28 / **9** / 6 — **一致** |

第 2 群に入った新拒否ケース: producer `dependent-nonnull-lead`、checker `dependent-outcome-resealed`。第 3 群 `batch-parent1578-admission-and-projection` は親層の試験(6 件ずつ)。

`production_interfaces_used` に **`reduce_candidate_numeric` / `restore_reduction` / `publish_candidate_decision` / `advance_reduction_numeric`**(P)、**`BatchReductionState.reduce` / `.advance` / `compare_candidate_publication` / `accepted_row_record` / `candidate_decision_record`**(C)が literal で並ぶ。`fixture_scope` は P で「**nonzero dependent-then-independent physical reduction/publication**」と明記。

### 6.2 実 fixture の生データを私が取得して検算した

artifact に fixture が全保存されている(`selftest-fixtures/P/selection/dependent-continuation/` と `selftest-fixtures/C/roster/dependent-continuation/`)。116 file を取得して独立検算:

**P 側**(anchor rank 1・親行 1 本・入力 `leading_rows = [[0,2,2,0],[0,2,2,0],[0,2,1,0]]`):

| ordinal | outcome | coefficients.u8 | 剰余の非零数 | rank | gen | row_manifest |
|---:|---|---|---:|---|---|---|
| 0 | INDEPENDENT | `[0]` | 2 | 1→2 | 7→8 | `abc4da58…` |
| 1 | **DEPENDENT** | **`[0, 2]`** | **0** | 2→2 | 8→8 | **null** |
| 2 | INDEPENDENT | `[0, 2]` | 1 | 2→3 | 8→9 | `d17b9587…` |

- **従属は非零従属**: 係数 2 で ordinal 0 の行に一次従属(σ = 2 で正規化されているので `2·[0,1,1,0] = [0,2,2,0]`)。私が packed3 を復号して確認。
- DEPENDENT の `reduction/` から **`physical-normalized.bin` / `instruction.json` / `target.json` が実際に消えている**(7 file のみ)。`lead` / `sigma` / `target_scalar` / `normalized_sha256` / `new_row_offset` がすべて null、`remainder_zero = true`。
- **`target-before.bin` == `target-remainder.bin`(バイト同一)** → DEPENDENT で target が動かないことを生バイトで確認。
- `packet/rows/` は 000000 と 000001 の 2 本(8 file)のみ = ordinal 1 で行が publish されていない。
- 次独立(ordinal 2)で `lead = 2` / `new_row_offset = 1` / rank 3 / gen 9 に正しく進む。

**C 側**(anchor rank 0・親行 0 本・入力 `[[2,0,0],[2,0,0],[1,1,0]]`・scalars `[2,2,1]`):

| ordinal | outcome | coefficients | 剰余の非零数 | rank | gen |
|---:|---|---|---:|---|---|
| 0 | INDEPENDENT | `[]` | 1 | 0→1 | 0→1 |
| 1 | **DEPENDENT** | **`[2]`** | **0** | 1→1 | 1→1 |
| 2 | INDEPENDENT | `[1]` | 1 | 1→2 | 1→2 |

→ **P と C の fixture は数値も形も別物**(anchor rank・行数・係数・lead がすべて異なる)。**片方の複製ではない**ことをデータが判別する。

### 6.3 陰性(再 seal)fixture の質 — 両側で性格が違う

| 側 | 陰性名 | 改変内容 | 発火した gate | 私の評価 |
|---|---|---|---|---|
| P | `dependent-nonnull-lead` | DEPENDENT の `reduction.json` の `lead` を null → **0** にし、telemetry の `payload_bytes` を再計算、manifest の各 entry の bytes/sha を更新して**全体を再 seal** | **`fixed_lambda_batch:dependent_preserves_target_and_has_no_normalized_row`** | **意味論 gate**。私が bad-root の manifest 7 entry を実バイトで再計算し **7/7 整合** = hash 不一致では捕まえていない。**強い陰性** |
| C | `dependent-outcome-resealed` | 候補 manifest の `outcome` を DEPENDENT → **INDEPENDENT** にして再 seal | `cycle_batch:candidate_expected_size_hash:candidates/000001/manifest.json` | **checker が自分で再計算した候補記録との size/hash 比較**で落ちる。形式は hash gate だが、比較対象は checker 自身の判定(DEPENDENT)なので**実質は意味論的**。ただし「gate の名前が形式層のもの」である点は記録しておく |

C 側は加えて `k128_dependent_negative_rejected_before_any_state_advance` で**状態が一切進んでいないこと**(physical identity / processed / dependent / decisions)を要求している。

### 6.4 判定 — **F-k64-1 は閉じてよい(liveness の穴は塞がった)**

- v3 判読で私が提案した「合成 fixture 1 例を第 2 群に足し、拒否件数 literal を +1」は、**提案より強い形**(陽性 3 段 + 陰性 1、P/C 別実装、実 production 関数呼び出し、fixture 全保存)で実装され、**本 run で実際に PASS した**。
- 残る限定は**性質が変わった**: これは「未試験」ではなく「**合成 fixture であり、本番 λ・Ω・E/P1 相の算術は通っていない**」という範囲限定である(fixture 自身が `actual_parent_arithmetic: false` / `earlier_five_phase_bodies_evaluated: false` と明記)。DEPENDENT 判定は reduction 相に閉じているので、この範囲限定は**この枝に関しては本質的でない**と私は判断する。
- 本番側の `dependent_candidates = 0` は 4 run 連続で不変(a(k) = k)。

---

## 7. 【独立節・重点 B】費用 — v3 との**制御された比較**(同 k・同算術・rank と親層だけが違う)

### 7.1 実測

| | v1(k=32) | v2(k=64) | v3(k=128・rank1450) | **v4(k=128・rank1578)** | v3→v4 |
|---|---:|---:|---:|---:|---:|
| 追加行 | 32 | 64 | 128 | **128** | 同 |
| producer 実秒(自己申告) | 432.437 | 825.483 | 1,622.717 | **1,668.098** | **+2.80 %** |
| producer 実秒(harness 外形) | n/a | 826.027 | 1,623.542 | **1,669.026** | +2.80 % |
| checker 実秒(自己申告) | 551.331 | 1,023.682 | 1,956.121 | **2,013.378** | **+2.93 %** |
| checker 実秒(harness 外形) | n/a | 1,024.656 | 1,956.717 | **2,014.299** | +2.94 % |
| **P + C(自己申告)** | 983.768 | 1,849.165 | 3,578.838 | **3,681.476** | +2.87 % |
| **1 行あたり P+C** | 30.743 | 28.893 | **27.960** | **28.762** | **+2.87 %** |
| 候補六相 合計 | 351.018 | 707.981 | 1,419.982 | **1,422.421** | +0.17 % |
| **候補あたり** | 10.969 | 11.062 | 11.0936 | **11.1127** | **+0.17 %** |
| selection(oracle 1 回) | 11.880 | 11.963 | 11.836 | **11.871** | +0.30 % |
| final separator | 0.869 | 0.893 | 0.936 | **1.020** | +9.0 % |
| **計測外の固定費** | 68.670 | 104.647 | 189.963 | **232.786** | **+22.54 %** |
| 出力 ZIP | 94,677,901 | 187,072,168 | 369,233,546 | **377,383,320** | **+2.21 %** |
| producer cap 使用率(5,400 s) | 8.0 % | 15.3 % | 30.1 % | **30.9 %** | — |
| checker cap 使用率(10,800 s) | 5.1 % | 9.5 % | 18.1 % | **18.6 %** | — |
| producer `ru_maxrss` | — | 437,064 KiB | 442,952 KiB | **499,868 KiB(6.8 %)** | +12.8 % |
| checker `ru_maxrss` | — | 1,546,708 KiB | 1,547,480 KiB | **1,576,576 KiB(21.5 %)** | +1.9 % |
| `outer_terminated` | — | False | False | **両方 False** | — |

### 7.2 producer の相分解(772 件の phase 測定を私が全集計)

| 相 | 128 候補の合計 | 1 候補あたり | 候補時間比 | v3 の比 |
|---|---:|---:|---:|---:|
| raw | 13.610 | 0.1063 | 1.0 % | 1.0 % |
| source | 34.451 | 0.2692 | 2.4 % | 2.4 % |
| primal | 313.044 | 2.4457 | **22.0 %** | 21.7 % |
| **p1(corrected_source)** | **1,019.136** | **7.9620** | **71.6 %** | 72.1 % |
| B(四 character) | 9.671 | 0.0756 | 0.7 % | 0.7 % |
| reduction(実消去) | 32.509 | 0.2540 | 2.3 % | 2.2 % |
| **候補 計** | **1,422.421** | **11.1127** | 100 % | — |
| selection | 11.871(1 回) | — | — | — |
| final separator | 1.020 | — | — | — |
| **計測外の固定費** | **232.786** | — | — | — |

- **primal + p1 = 1,332.180 s = 候補六相の 93.66 % = producer 全体の 79.86 %**(v3 は 93.83 % / 82.11 %)。**律速は 4 run とも P1 補正相。**
- reduction 相の rank 依存: 傾き **0.000238 s/候補**(v3 は 0.000204)・相関 0.635(v3 は 0.905)・先頭 16 平均 0.2411 → 末尾 16 平均 0.2680。
- **前半 64 の候補あたり 11.0722 s vs 後半 64 の 11.1531 s**(+0.081 s)→ rank 依存はこの窓でも小さい。

### 7.3 【要修正 F-v4-1】`fixed(k)` の 3 点モデルが外れた — 機構は特定できた

| k | rank | 実測 fixed(s) | v3 の 3 点モデル `26.0 + 1.273k` | 誤差 |
|---:|---:|---:|---:|---:|
| 32 | 1450 | 68.670 | 66.7 | +2.0 |
| 64 | 1450 | 104.647 | 107.5 | −2.9 |
| 128 | 1450 | 189.963 | 189.0 | +1.0 |
| **128** | **1578** | **232.786** | **189.0** | **+43.8(実測が 23.2 % 大)** |

**機構の特定**(私の判断・根拠つき):

- v4 は親 role が **15 → 16** に増え、**第 16 親 = v3 候補(369,233,546 B / 11,437 entry)** の全 entry 認証・保全・復元・envelope intake が P/C 両方で新設された。実際、`checker-stderr.log` の末尾に `{"files": 11437, "phase": "parent_files_authenticated", "role": "batch-parent", "total": 11437}` が出ており、**私が独立に数えた v3 候補 ZIP の entry 数 11,437 と一致**する。
- 一方 **候補 ZIP の底は +8,149,774 B(+2.21 %)しか増えていない**(369.2 → 377.4 MB・同じ k = 128)。したがって「親サイズに比例して毎回 22 % ずつ膨らむ」型ではない。
- → **一回性の構造費**(≈ +43 s)と読むのが最も整合的。次 run では親が 377.4 MB になるので、この費目は **+1 s 程度**しか増えないはずである。

### 7.4 cap から取れる k と、二読みを分ける安価な次観測

**読み A(一回性・私の推奨)**: fixed は本 envelope で ≈ 233 s に落ち着き、以後は親 ZIP の伸び(+2.2 %/run)に比例してゆっくり増える。

- producer(k) ≈ **82.7 + 12.386k** → cap 5,400 s で **k_max ≈ 429**(v3 判読の 433 と実質同じ)。
- checker(k) ≈ **148.6 + 14.569k**(v2→v3 の傾きを流用)→ cap 10,800 s で **k_max ≈ 731**。
- **律速は producer(不変)**。限界単価は run 単位で 28.762 s/行。残り 48,384 − 1,706 = **46,678 行**・純 P+C ≈ **15.5 日**、run 数 ≈ 365(k=128 固定)。

**読み B(親サイズ比例)**: +42.8 s を親 envelope の +21.2 % に帰す。この場合 fixed ≈ 0.663 s/MB で伸び、rank が数千に達する前に producer cap が固定費だけで飽和する。

**分ける観測(安価)**: **次 run(同一コード・k=128・親 = 本 run の候補 377.4 MB)の計測外固定費**。
- **≈ 234〜236 s** なら読み A(一回性)確定 → v3 の外挿(k_max ≈ 433・150 run 規模)を維持。
- **≈ 270〜280 s** なら読み B → 計画の作り直しが必要。
追加コストはゼロ(次の batch を回せば自動的に取れる)。

**注意**: いずれも 128 行窓 4 点からの外挿であり、**法則ではない**。特に p1(71.6 %)が本当に rank 非依存かは、この窓では検証できていない(前半 64 と後半 64 の差 +0.081 s はノイズと区別できない)。

---

## 8. 非空虚性・恒真性の検査

### 8.1 「答えを知っている問題」が実際に機構を通ったか

| 較正項目 | 通ったか | 根拠 |
|---|---|---|
| 基準 5 弦の残差 = 0 | **通った** | `require(not np.any(residuals[basis]) …)` が実データで満たされ、私も再計算 |
| `scalar in (1,2)`(選定弦の残差は非零) | **通った** | 実測 1:66 / 2:62・0 は 0 件 |
| 第一候補 INDEPENDENT の予言 | **通った** | 硬い `require`(§2)。前提から強制されるが恒真ではない |
| **DEPENDENT 枝** | **今回初めて通った** | §6 |
| aux 枝(本番) | **通っていない** | `aux_values = [0,0]`。selftest 側では通る(§8.4) |
| 目標減算符号(θ ≠ 0) | **通った** | 81/128 |
| 語因子符号 | **通った** | §8.2 |

### 8.2 語因子の符号 — **三層すべてが非空虚に判別された(v3 より強い)**

私が生受領証から測った三つの符号役割は**互いに逆**であり、データが一意に判別する:

| 役割 | 規約 | 私の実測 |
|---|---|---|
| `target_literal_factor.exponent` | **+sr(θ)** | 128/128 成立(+1:40 / −1:41 / 0:47・θ 分布と一致)。逆符号は 81 件で破れる |
| `physical_factors[].exponent`(消去の語因子) | **−sr(coefficient)** | 32 候補の **52,480 entry で違反 0**。逆符号(+sr)は **34,790 件で破れる** |
| `outer_exponent`(σ の外側指数) | **+sr(σ)** | 32/32 成立。逆符号は不成立 |

ここで `sr(0)=0, sr(1)=+1, sr(2)=−1`。**52,480 entry のうち非零係数が 34,790(66.3 %)** なので、消去は 1,578 本超の親行に対して実際に密である(候補あたり平均 1,640 factor = 1578 + ordinal に一致)。

### 8.3 恒真性・silent cap

- **恒真 gate は見つからなかった**(§2)。`accepted` は自由変数。
- **silent cap は見つからなかった**。`failed[:BATCH_SIZE]` は登録政策そのもの。
- **第一候補予言の位置づけ**: 前提(親 span 零・raw_pairing 非零)から数学的に強制される。したがって「発見」ではなく「較正」であり、**DEPENDENT 枝の試験にはならない**(それは §6 が担う)。なお `conditions` の 5 項目のうち `parent_span_zero` / `derived_rho2_one` は driver 内では **literal として書かれている**(この場で再測定されていない)。実効的な gate は `matches_prediction is True` の一本である — これは記録しておくべき小さな型の弱さだが、前提そのものは v3 の separator 受領証(`sha(0x00×1578)`)と本 run の anchor 検査で別に担保されている。
- `metadata-selftest`: 16/16 拒否・`rejected_count == 16`・`mathematical_success_suites_rerun == 0`。拒否理由が全件別々の gate 名で、ZIP の casefold / duplicate / traversal、重複 JSON key、NaN まで含む。

### 8.4 「何にでも当たる試験」ではない

- 版差分に当たる陰性 fixture が三群に散在: `batch-32/64/127/129/256`・`old-policy`・`old-invocation-k64`・`old-64-witness-cutoff`・`old-owner-scope64`・`parent-batch-rows-64`・`upstream-steps-128`・`batch-head-as-old-anchor`・`saved-v3-head-renamed-v4`・`packed-hash-as-plain-target` 等。
- 陽性 fixture も併走(`auxiliary-only` / `second-auxiliary` / `complete-zero` / DEPENDENT 三段)。
- **落ちている被覆は「変えていない部分」**であり、それは registry の 104(P)/ 79(C)不変区間として文書化されている(実行ではなく静的継承)。

---

## 9. 限定条項(7 条)

1. **射程 = rank 1578 → 1706 の 1 batch のみ**。rank 1706 の λ\* に対する oracle は**未計算**(`new_lambda_oracle = null`)。**NONMEMBER 主張ではない。**
2. **a(128) = 128 は roster 前置 128 本の観測**(batch パラメータ k の性質ではない)。消化率 128 / 36,104 = **0.3546 %**。**Task 988 F4 の反例は排除されていない。** 加えて §4.2 のとおり **roster は縮む待ち行列ではない**(正味 −170 / 消費 128)。
3. **算術 TCB は共有カーネル 2 本を含む**(`vectorized_projection_chunk` / `sparse_adjoint`)。cert に登録され私が 4/4 再計算したが、`current_run_call_coverage = NOT_MEASURED`・`kernel_third_independence_claimed = false`。**第三独立性はこの 2 本に及ばない。** P1 相が候補時間の 71.6 % なので前者は確実に load-bearing。
4. **旧 1,578 行の実バイトは私自身は未取得**。λ_new ⊥ 旧行 と ρ₂ の旧行部分は checker の再現に依存する(その再現コードは registry の不変区間内)。**ρ₂ は依然 DERIVED**(`original_rho2_directly_read: false`・親 225 件)。
5. **harness TCB は単著**(WF 22,153 B + driver 536,145 B)。私は harness 出力を根拠に使わず §3〜§6・§8 を生バイトから第三実装で再導出した。ただし **§7 の相別秒だけは producer の自己計測**である。
6. **checker の段別 timestamp は無い**(`checker-stderr.log` 16,568 行に時刻・秒フィールド **0 個**・producer-stderr 9,815 行も 0 個)ため、checker の限界単価は run 間差商でしか出せない。**F-k64-7 継続。**
7. **私は 377 MB の ZIP を全量ダウンロードしていない**(HTTP Range で必要な entry を個別/一括取得)。ZIP 全体の sha は GitHub API の digest `84040119…` を採り(私が API で再取得して確認)、自分でバイト再計算していない。取得した各 entry は zip の圧縮データから展開しており、内容の照合は私自身の計算である。

### 9.1 前回 8 条との対応

| v3 の条 | 本 run での扱い |
|---|---|
| 1. 射程 1 batch | **継続**(条 1) |
| 2. a(k) の意味・F4 未排除 | **継続 + 強化**(条 2・§4.2 で roster の非単調性を初測定) |
| 3. **DEPENDENT 未試験** | **解消**(§6) |
| 4. 共有 kernel 2 本 NOT_MEASURED | **継続**(条 3) |
| 5. 旧行の実バイト未取得・ρ₂ DERIVED | **継続**(条 4) |
| 6. harness TCB 単著 | **継続**(条 5) |
| 7. checker 段別 timestamp 無し | **継続**(条 6) |
| 8. ZIP 全量 DL せず | **継続**(条 7) |

**新設は無し。** 8 条 → 7 条。

### 9.2 2196/2198 の追加確認項目

| 項目 | 結果 |
|---|---|
| fixed 参照経路の修理が旧 64 の fixed 16 file を実 pin で結んだこと | **確認**(§3)。受領証・実バイト・`chord-tau.u8` の同一性で三重に確認 |
| 受領器 1058/1069 の同型誤用の修理 | **静的主張のみ・未検証**。TEMP 受領器 v2(259,814 B / `9f9e920b…`)は repo に存在せず、私は実物を読んでいない。**Astra 側の主張として据え置く** |
| 1067 説明返信の CV-9 前 commit | **充足**(裁定 2202 で commit `398c1f46` を工房が確認済み) |

---

## 10. CV-9 裁定案・工房格付け案(一行)

**CV-9 = 同一対象(SAME OBJECT)・限定 7 条 → 工房格付け案: checker PASS / cross-checked(限定 7 条)・rank 1706 / gen 8411 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。v3 の 1578 の直系後継として置き換える(合算ではない)。**

**司令塔への一行**: envelope-v3 は **fixed 参照修理が数学的意味を一切変えずに通り**(P は逆置換で旧 raw に戻ることを私が検算・C は 117/117 完全不変)、**私が v3 で出した唯一の未解決指摘 F-k64-1 が実 fixture の実通過で閉じた**(P/C 別実装の「独立 → 非零従属 → 次独立」+ 再 seal 陰性・生データ検算済み)。**本 run 最大の新規情報は fresh λ による失敗集合の初測定**で、**消費した 128 弦は 128/128 が充足に転じた(乱択基準 ≈ 43)一方、正味の roster 減少は 170 本しかない**(12,233 消滅 / 12,063 新生)。すなわち「進んでいる」ことと「roster が減っている」ことは別物であり、**残工程の見積りは rank 余地(46,678 行)で立てるべきで roster サイズでは立てられない**。費用面では **同 k で固定費が +22.5 %(190 → 233 s)**、機構は第 16 親(369 MB / 11,437 entry)の新設と特定でき、候補 ZIP の底は +2.2 % しか伸びていないので**一回性と読むのが最良・k_max ≈ 429 は据え置き**。二読みは**次 run の固定費 1 数値**(234〜236 s か 270〜280 s か)で決着する — 追加コストゼロ。

---

## 11. 判読者の限界(正直な申告)

- 旧 1,578 行の実バイトを取得していないので、λ_new ⊥ 旧行 と ρ₂ 恒等式の旧行部分は checker の再現に依存している。
- 「消費した弦が次の λ で 128/128 充足に転じる」ことが**定理として強制されるか**は、受領証だけからは示せていない。乱択基準線との対比で**偶然ではない**ことしか言えていない(それでも end-to-end 較正としては強い)。
- 語(Ω / P1 / literal)の**再構成**は私の射程外。ε/ω/repair 指数と三層の符号規約は **producer の申告と checker の式計算の受領証水準での突合**として検証した(§8.2)。今回 ω/central の分布は増分規律に従い 32 候補の抽出にとどめた。
- `sparse_adjoint` / `vectorized_projection_chunk` が本 run の実行経路で呼ばれた行は特定していない(両側でバイト同一/差分箇所を確認したのみ)。
- §7.3–7.4 の外挿は **4 点フィット / 128 行窓**であり、法則ではない。「一回性」の読みも次 run で反証されうる。
- Astra 側 TEMP 資産(受領器 v2・1067 機械票・root 独自票)は私の手元に無く、**静的主張として区別して記載した**。本報告の数値はすべて私が artifact / repo の生バイトから独立に導出したものである。
- ZIP 全体の sha は API digest を採用(条 7)。
- **この観点では仕様の齟齬(別対象)を見つけられなかった** — 保証ではない。

---

## 付録 A. Astra 側の主張と私の測定の対応

Astra の本 run 便(`ops/express/20260907_astra_v4_run34120585268_*.md`)は**数値・格付けを一切報告していない**(「全 ZIP / metadata 受領後に報告する」と明記)。したがって本報告の数学的内容に Astra 発の値は含まれない。照合可能だった Astra 主張:

| Astra の主張 | 私の測定 | 一致 |
|---|---|---|
| candidate id 10020349387 / 377,383,320 B / `84040119…` | GitHub API で再取得 | **一致** |
| diagnostics id 10020372140 / `7097d7cc…`(同 bytes) | 同 | **一致** |
| run 34120585268/1・head `92720e5371164545259c3007cb11e951fa5e1686`・job 101737466647 | API: head 一致・started 12:12:10Z・updated 13:19:18Z・conclusion success | **一致** |
| step 14 は 12:15:38Z 開始、step 16 は 12:43:41Z 開始 | 実行受領証: producer started 12:15:41.081Z / finished 12:43:30.107Z、checker started 12:43:41.262Z / finished 13:17:15.561Z | **整合** |
| 1065: 差分は二 hunk・逆置換で旧 284,974 B へ一致・135 不変/1 変更/1 追加・C4 不変 | 私が逆置換を実行し sha 一致、registry 区間比較で 135/1/1/0 と C4 117/117 を確認 | **一致** |
| 1064/1065/1067/1068/1069/1070 の返信 pin | 工房が裁定 2197/2198 で再計測済み(私は再測していない) | 未再測 |
| 受領器 v2 259,814 B / `9f9e920b…`(TEMP・未実行) | repo に存在せず | **未検証(静的主張)** |

## 付録 B. 主要 pin(私の実測)

- run 34120585268/1・head `92720e5371164545259c3007cb11e951fa5e1686`・workflow `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v4.yml`(name `…-envelope-v3`)
- WF 22,153 / `56a8349fd54b16d63da9de2c4762ed04328ef1373f65af45c46019e745a1859b`
- driver_v2 536,145 / `35f73f5d1b8b519a69773690db8f8e514b3cc1d2792cc595ecdc0b92dede7a0c`
- P 290,457 / `a58f7c116558fdc430025a9e095d29d0b04e0f20c9295264fca58a4c13510d0a`(LF 4,507)
- C 261,170 / `a29380ec00876225cc618c7025d671a3da79aea3b31b829dedba13c59ba84633`(LF 3,724・v4 系で不変)
- 旧 P archive 284,974 / `3ba71767585b6a49efccb5d20bb60eb8939848669c19692a63018b9486f41d36`(LF 4,426)
- 旧小 WF archive 20,296 / `c8dc698160b41a21e338cc5a099f4e4abb51a369247a48fbfbd17c907dd02623`
- registry v2 236,390 / `84f5bbc6a85e77915535968e4342c09b6bf3e5b94638ab14184c67ca677ce114`
- shared-tcb 13,187 / `d94ffbe0f4581ff403d1328530ae5d2a7a39205b4962a6dfcb5a203562c4c613`
- 親(batch-parent)= artifact 9987222571 / 369,233,546 B / `781c9f46…`(11,437 entry)
- 親(continuation)= artifact 9977040548 / 304,642,285 B / `a7ecd56d…`
- 選定 λ `6a0fe9368f2ec7f28c4d8076e7d3184fb57322b9d0905a8e7c3c26b467bcee4e`(= v3 final λ)
- 新 λ `d036e848c46b563a5b0f683fb94afcbc759dc4bc402c6db14c82b172ccc0a653`
- state_head `e793896e…` → `13c631c6dee46d4026e996f53370bcc202737f1082582b02271884593f902101`
- target `7868b780…` → `954e1ba1a50e138a0577c27c285c21ed052f3491176d883f370e8a94d11b456a`
- row_pairings `84a8935d91036a00e62362f5601416d094f4708da6986096f9353659cfa146eb` = sha(0x00 × 1706)


---

**裁定 2208 追補(費用量の定義・Astra 指摘で精確化)**: 本判読 §7 の「計測外固定費」232.786 s(v4)/189.963 s(v3)は **P の残差 = P elapsed − P 候補六相(v4: 1,422.421 s)− selection(11.871 s)− final(1.020 s)** であり、P+C の計測外時間ではない(C には相別 timestamp が無い)。F-v4-1 の判定量はこの P 残差とし、次 v5 の公開 cost 票に P 残差・C total・P+C total を別字段で保存する(Astra Task 1079)。v5 は旧 16 親 + 別第 17 親/adapter の追加であって「同一コードで親一個を 369 → 377 MB へ置換」の対照ではないため、単一観測だけで一回性/サイズ比例を確定せず、両親規模・layer 数/source 版を併記して判定する。

---

**裁定 2206(司令塔・2026-09-07)格付け**: 本判読(原本 `scratchpad/fal_cv9_fixed_lambda_batch_v4_report_v1.md` 53,292 B・sha256 8e558313bba32a52159d25605bee76652cc74edaaf3119c5a36efb80cd3cffe5・工房 sha256sum で pin)を正本として採用。CV-9 = 同一対象・限定 7 条(8 条から F-k64-1 を解消・新設なし)→ **rank 1706/gen 8411 を cross-checked(限定 7 条)で受理し、v3 の 1578 の直系後継として置き換える(合算しない)**・verified=false・grade-2 NOT_DECIDED・A0 actual 0/1 不変。**F-k64-1 閉鎖**(DEPENDENT 実 fixture が P/C で実通過・P[30,10,6]/C[28,9,6] 一致)。**新規 F-v4-1(費用)**: 同じ k = 128 で計測外固定費 189.963 → 232.786 s(+22.5 %)・機構 = 第 16 親(v3 候補 369 MB/11,437 entry)の認証が P/C 両方で新設・一回性の構造費と読むのが最良(k_max ≈ 429)・**次 run の固定費 1 数値で決着**(234〜236 s なら一回性/270〜280 s なら親サイズ比例 → 計画作り直し)。残工程の見積りは rank 余地(46,678 行)で立てる(roster サイズは非単調)。
