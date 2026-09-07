# 増分 CV-9 判読 — R07 fixed-lambda cycle batch **v5 / envelope-v3 / k = 128**(rank 1706 → 1834・第 17 親 batch-parent-v4 の入場・fresh λ_1706 oracle 初回)

対象 run: **34161493396 / attempt 1**(success・event=push・head `a5b456a973f8a917f3af386d327061a02a0cf900`・2026-09-07T21:00:06Z → 22:10:09Z・job 101864093045・**26 step / 失敗 0**・workflow name `d972-r07-fixed-lambda-cycle-batch-v5-envelope-v3`)
候補 artifact **10034053256**(384,961,441 B・API digest `sha256:72e19a87e3a4ca06daa3b1b9dc8a16e76778e6ce1d6bd3a57b25acea363602db`・zip entry 11,750)
診断 artifact **10034064913**(同 bytes・digest `715993af…`)
判読者: falsifier(非当事者・事後)。判読日 2026-09-08。
前回 CV-9 正本: `docs/notes/fixed_lambda_batch_v4_cv9_reading_v1.md`(裁定 2208・限定 7 条)。

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 7 条(§9)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 7 条)・rank 1834 / gen 8539 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。v4 の rank 1706 の直系後継として置き換える(合算ではない)。**

**a(128) = 128**(offered 128 / accepted 128 / dependent 0 / skipped 0・partial false)。消化率 128 / 36,002 = **0.3555 %**。

見出し 5 つ:

1. **【重大 F-v5-1】固定費は「親 batch 層の数」に比例して積み上がる。この設計のままでは塔は登り切れない。** 5 観測を 2 変数で回帰すると `fixed(k, n) = 26.12 + 1.271·k + 44.40·n`(n = 認証する batch 親層の数・全 5 点で残差 ≤ 2.8 s)。**v3 の 3 点モデル `26.0 + 1.273k` は間違っていなかった — n 項が抜けていただけである。** v4 の +22.5 % は n=0→1、v5 の +19.4 % は n=1→2 でちょうど説明できる。producer 全体は `32.82 + 12.4294·k + 40.31·n`。**毎 run が恒久的に 1 層ずつ足す設計だと、producer cap 5,400 s を満たす (k, N) の組が存在しない**(最良でも最終 run が 9,658 s = cap の 1.79 倍を要する)。§7 に詳算。**司令塔判断が要る = v6 で層を 3 に増やすのか、回転させて 2 のままにするのか。**
2. **【解消 F-v4-1】v4 判読が残した二読みは決着した — ただし「読み A(一回性)」は棄却。** 実測 277.828 s は読み B の窓(270〜280)に落ちたが、機構は「総親 envelope 比例」ではなく「**追加された層ごとに ≈ 44 s(≈ 0.117 s/MB)**」である(v3→v4 +42.823 s / 369.2 MB = 0.1160、v4→v5 +45.042 s / 377.4 MB = 0.1194)。裁定 2208 の指示どおり、これは**単一観測で確定させていない** — 交絡(第 17 親・adapter・native pairing 1450/1578 の追加呼び出し)は cost-receipt 自身が明記しており、私もそれ以上には切り分けられていない。
3. **【一次データ】「消費した弦は恒久的に片付く」が 2 段先まで持つことを初めて測った。** v3 が消費した 128 弦は λ_1578 でも λ_1706 でも **0/128 が失敗**。v4 が消費した 128 弦も λ_1706 で **0/128 が失敗(128/128 充足)**。乱択基準線は 128 本中 **43.1 ± 5.35**(F(1450) 由来・F(1578) 由来とも同じ)。すなわち **z ≈ 15.9σ が 2 回**。一方 roster は縮む待ち行列ではない: 36,274 → 36,104 → **36,002**(正味 −170 → **−102**)に対し churn は 12,233/12,063 → **12,168/12,066** とほぼ一定。
4. **【解決】前 run(34148667863)の P-only 出力は流用されていない。かつ数学は 2 run で完全に再現された。** output/ 配下 5,814 共通 file のうち**数値 payload 2,074 本(.bin 1,796 / .u8 271 / .u32 7)は size+CRC32 が全一致**、JSON は 645 一致 / 3,093 相異、`output/HEAD`・`output/progress/HEAD` も相異、片側のみ 773 本ずつ(772 checkpoint + invocation 1)。**相異の原因は例外なく 2 つだけ**: (i) C5 の pin(336,193→336,211)が `source.json`→`owner.json`→全 root binding→rolling 鎖へ伝播、(ii) `telemetry.json` の実測秒。**数学値が異なる文書は 1 つも無い**(§5 で witness 128 件を field 単位に分解して確認)。
5. **【軽微・受領証の可読性】`basis_chords`/`selected-chords.u32` は「辺 id」、`basis-tau.u8` は「弦序数」で索引されており、受領証にその明示が無い。** 私は最初これで誤読した。継続親の `chord-edges.u32` を取得して `chord_edges[[0,1,2,3,5]] = [2,3,4,6,11]` を確認し決着(§3.4)。副産物として **fit が一意に決まること**(非特異 5×5 系の F₃ 上唯一解)を全数探索で確認できた — v4 判読の「残差 5/5 = 0」より強い主張である。

---

## 1. (1) 規約表 diff(v4 → v5)

### 1.1 宣言の突合

| 規約 | v4 の宣言 | **v5 の宣言** | 本 run の実測 | 判別性 |
|---|---|---|---|---|
| `batch_size` / `max_batches` / `refill` | 128 / 1 / False | **同一(driver literal `:34-38`)** | selected 128 / processed 128 / refill False | — |
| `selection_policy` | `CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX` | **同一文字列** | roster 昇順先頭 128(弦 index 71..535) | **判別**(gap≠1 が 69/127・最大 gap 38) |
| `partial_policy` | `PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY` | 同 | `partial=False` | — |
| caps | 5400s/7168MiB・10800s/7168MiB(outer 6000/11400) | **同(不変)** | 実 1,703.569 / 2,042.330 s(harness 外形)・`outer_terminated` 両方 False | — |
| **親** | 16 role(15 + batch-parent = v3 候補) | **17 role**(`ROLES` literal・`ORIGINAL_ROLES=ROLES[:15]` / `PREVIOUS_ROLES=ROLES[:16]` / 第 17 = `batch-parent-v4`) | P stderr に `admitted-parent` が **17 role・合計 32,235 file** | **最大の変更点** |
| **acceptance の key 数** | 7(`schema,parents,anchor,batch_anchor,code,runtime,registration`) | **8(`next_batch_anchor` を追加)** | `acceptance.json` の top key = 8・`parents` は 17 件 | **判別**(P に `accepted_next_batch_old_seven_keys` / `accepted_batch_old_six_keys` の後方要求が残る) |
| **選定 λ** | λ_1578(`6a0fe936…`) | **λ_1706(`d036e848…`)= v4 の final λ** | `selection/start.json` と separator が同 sha | **本 run の核心(§3)** |
| basis(固定 5 弦) | 辺 [2,3,4,6,11] | 同 | 残差 5/5 = 0・**fit は一意**(§3.4) | fit `[2,1,0,0,2]` → **`[0,1,2,1,1]`**(λ 依存・正しい挙動) |
| ρ₂ | `mode=derived, value=1, directly_read=False`・ancestry **353** | 同・**481** | separator に 481 = 97 + 384 batch-row | **DERIVED のまま**(未昇格) |
| lower-zero | `source_lower_zero = NOT_ASSERTED` / `physical_lower_zero = true` | 同 | separator に同値 | **契約どおり** |
| terminal | 3 値 | 同 | `BATCH_COMPLETE_CANDIDATE` | 他 2 値は canary のみ |
| **selftest 群** | **3 群**・P[30,10,6] / C[28,9,6] | **4 群**(第 4 = `batch-parent1706-two-layer-admission`)・**P[30,10,6,7] / C[28,9,6,7]** | 四群とも PASS・exit 0・**literal と件数完全一致** | **§6** |
| metadata canary | 16 件 | 同 16 件・`metadata_regression_from: …-v1` | 16/16 拒否 PASS。**`duplicate-parent-role` の理由が `acceptance-seventeen-ordered-roles` に更新**(17 role 対応) | 非空虚 |
| 静的 registry | `…v4.audit-registry.v1`(task 1064)・236,390 B | **`…v5.audit-registry.v1`(task 1079)・499,053 B**。v4 registry(236,390 B)と historical(76,867 B)を**併載** | 3 本とも driver literal から抽出して artifact 同梱コピーと**バイト完全一致**(§1.3) | 継承の物理保持 |
| 変換対象 | — | P4→P5 137→**156** 区間 / C4→C5 117→**140** 区間 | registry の `current_transitions` に記載 | — |
| shared TCB | 4 kernel | 同 4 kernel | `current_run_call_coverage = NOT_MEASURED`・`kernel_third_independence_claimed = false` | **限定条項 継続** |
| 規約文字列(coverage-receipt) | — | `normalizer_convention: sr(0)=0,sr(1)=1,sr(2)=-1; ordered repair x,y,central; mod54 then exact /18`・`target_update_sign: remainder_before - theta * normalized_row`・`correction_word_factor_sign: +sr(theta)` | **§4.3 で私が独立に検算し一致** | **強化**(v5 で機械票化) |

→ **凍結宣言と実装・実データの間に齟齬は見つからなかった。緩めた箇所は 1 つも無い。**

### 1.2 前 2 run の修理 — 逆置換の検算

**P の修理(run 34143415388 の fail-closed 原因)**

- 差分は **3 行のみ**、いずれも同一 hunk 群(`search/d972_r07_fixed_lambda_cycle_batch_v5.py` L2084 / L2086 / L2089)で `"bytes"` → `"file_bytes"`。+15 B(366,644 → 366,659)。
- **定数側は不変**: `NEXT_BATCH_INVENTORY_REGISTRATION`(L404-410)は旧版でも `files: 11648, file_bytes: 1308094050, directories: 3525, files_sha256: ffec515b…, directories_sha256: f9562484…` で**新旧バイト同一**。すなわち修理は**定数の値ではなく consumer 側の key 名**を直したもので、旧版は `exact_keys` で確実に落ちる(数学未到達)。
- **私の独立確認**: acceptance の `batch-parent-v4` の file list から合計 bytes を再計算 → **1,308,094,050** = 登録値と一致。file 数 11,648・dir 数 3,525 も一致(§2)。

**C の修理(run 34148667863 の C5 L1995)**

- 差分は **1 行のみ**: `selected["selection_lambda_sha256"]` → `records["selection_start"]["selection_lambda_sha256"]`。+18 B(336,193 → 336,211)。**assert の相手 `BATCH_PARENT_LAMBDA`(= λ_1578 `6a0fe936…`)は不変**、check 名 `next_batch_old_oracle_is_native_lambda1578` も不変。
- **意味論の判読(私)**: 親(v4 候補)の `output/selection/selection.json` には `selection_lambda_sha256` という key が**存在しない**(27 key を私が列挙して確認) — 旧コードは KeyError で fail-closed。key は親の `output/selection/start.json` にのみ存在し、その値は **`6a0fe936…`(λ_1578)** である(私が親 artifact の生バイトから確認)。両文書とも直前行で `batch_bound(...)` により root 束縛されている。**したがって参照先の付け替えは同一主張・同一親・同一束縛強度であり、弱化ではない。**

**driver の修理**

- **v2 → v3**: 変更 3 行のみ — C5 の pin(bytes/sha)、registry 区間 `authenticate_next_batch_parent_metadata`(13,635 → **13,653 = +18**、行範囲 1871-2019 は不変)、`INHERITANCE_REGISTRY_PIN` の sha。**他に一切の差分なし。**
- **v1 → v2**: P5 の pin、registry 区間 `def next_batch_inventory_registration`(1,090 → **1,105 = +15**、行範囲 2081-2094 不変)、registry pin、**および 1 箇所の実挙動変更**(下記 F-v5-2)。

**【軽微 F-v5-2】driver v1→v2 で `fixture_audit('before-checker')` の PASS 要求が `execute()` 内の `if label == 'checker'` 枝から `post_producer()` 冒頭へ移設された(正味 −31 B)。** 移設後も checker 起動前には必ず通るので gate 自体は失われていないが、**「post_producer 完了 〜 checker 起動」の窓がこの gate の被覆から外れた**。harness TCB は単著(限定条項 5)であり、私は静的読解のみで評価している。数学的意味は変えないが、増分規律として記録する。

### 1.3 registry の全数照合(私の第三実装)

driver v3 の `br'''…'''` から 3 本を抽出:

| 名 | bytes | 一致先 |
|---|---:|---|
| `HISTORICAL_REGISTRY_RAW` | 76,867 | artifact `audit-historical-region-registry.json` と**バイト一致**・driver の `HISTORICAL_REGISTRY_PIN` と一致 |
| `PREVIOUS_REGISTRY_RAW` | 236,390 | artifact `audit-previous-v4-region-registry.json` と**バイト一致**・**v4 判読で私が 472 区間 / 254 分類を全数検算した registry と同一物** |
| `INHERITANCE_REGISTRY_RAW` | 499,053 | artifact `audit-region-registry.json` と**バイト一致**・`INHERITANCE_REGISTRY_PIN` と一致 |

現行 registry の内容検査:

| 検査 | 結果 |
|---|---|
| `source_files` 10 件(P1–P5 / C1–C5)の bytes / sha256 / lf / cr / bom / final_lf | **10/10 を repo 作業ツリーの実バイトで再計算・完全一致** |
| `new_source_audit` の宣言値 | `initial_rank 1706` / `initial_generation 8411` / `target_derivation_parents 353` / `mathematical_parent_count 17` / `accepted_parent_batch_rows 128` / `previous_parent_batch_rows 128` / `total_parent_batch_rows 256` — **すべて私の独立測定と一致** |
| `current_transitions` | P: P4(137 区間)→ P5(156)・C: C4(117)→ C5(140) |
| 自己申告の限界 | `new_selftests_executed_in_this_audit=False` / `new_actual_arithmetic_executed_in_this_audit=False` / `source_or_ast_executed_in_this_audit=False` / `independent_workflow_audit_claimed=False` |

**run 中の pin 検証の証拠**: WF の L217-221 / L236-248(実行前)と L371-387(実行後)で `sha256sum --check --strict` + `cmp` を driver / envelope-v1 / envelope-v2 / parent-v4 WF / parent-v4 driver に対して実施。`driver-bootstrap-stdout.log` に **10 行の `OK`** が実在。registry は driver 本体の中にあるので driver の sha 固定がそのまま registry のバイト固定になる。

### 1.4 交差辺(独立性)

- C5 の import は標準ライブラリ + numpy + `check_d972_r07_complete_oracle_cegar_continuation_v2` のみ。**producer 本体への参照は path 定数 2 行(`PRODUCER_FILE` / `CHECKER_FILE`)だけ**。`importlib` 0。
- P5 の `importlib` は自系 `L_FILE`(`L_SHA` pin つき・`require(file_pin(path)["sha256"] == L_SHA, "frozen_own_L")`)1 箇所のみ。checker への言及 5 件はすべて定数・ハッシュ pin メタデータ。
- **v1〜v4 と同じ二系統分離。**

### 1.5 配置 pin(私が repo 作業ツリーで再計測・全一致)

| file | bytes | 一致 |
|---|---:|---|
| `search/d972_r07_fixed_lambda_cycle_batch_v5.py` | 366,659 | 便の pin と一致・artifact 同梱の checkout-sources とも一致 |
| `search/check_d972_r07_fixed_lambda_cycle_batch_v5.py` | 336,211 | 同 |
| `search/d972_r07_fixed_lambda_cycle_batch_v5_workflow_driver_v3.py` | 1,145,223 | 同・artifact の `driver.py` とバイト一致 |
| `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml` | 26,294 | 同・artifact の `workflow.yml` とバイト一致 |
| `ops/source_versions/…-before-inventory-key-repair.py` | 366,644 | 旧 P archive |
| `ops/source_versions/check-…-before-selection-key-repair.py` | 336,193 | 旧 C archive |
| `search/…_workflow_driver_v1.py` / `_v2.py` | 1,145,254 / 1,145,223 | 旧 WF v1/v2 の env 値と一致 |
| `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v4.yml` | 22,153 | artifact の `workflow-parent-v4.yml` と一致・**v4 判読 付録 B の pin と同一** |
| `search/d972_r07_fixed_lambda_cycle_batch_v4_workflow_driver_v2.py` | 536,145 | artifact の `workflow-parent-v4-driver.py` と一致・同上 |
| `ops/workflow_versions/…-v4-envelope-v1.yml` / `-v2.yml` | 599,085 / 20,296 | artifact の `workflow-envelope-v1.yml` / `-v2.yml` と一致 |
| `checkout-sources/`(24)+ `audit-history-sources/`(8) | — | **32/32 が repo 作業ツリーとバイト全一致** |

**【軽微 F-v5-3】run に持ち込まれた旧 envelope は v4 系列のみで、失敗した v5 の envelope-v1 / v2(YAML と旧 P/C)は artifact に同梱されていない。** repo には保持されているが、artifact 単体からは「今回の run に至る 2 度の失敗」の物証が辿れない。数学に影響はないが、出所管理としては裁定 snapshot 側に依存する状態である。

---

## 2. (2) 第 17 親 batch-parent-v4 の入場

### 2.1 acceptance と実 artifact の突合(私の独立検算)

`acceptance.json`(6,032,243 B)の `next_batch_anchor` は **36 field**。うち `{file, bytes, sha256}` 型の記述子 **18 件すべてを親 artifact 10020349387 の実バイトから再取得して照合 → 18/18 一致・不一致 0**:

`checker-result.json` / `output/final/manifest.json` / `output/fixed/manifest.json` / `output/HEAD` / `output/final/lambda.bin` / `output/owner.json` / `output/parent-intake.json` / `output/parent-layout.json` / `output/progress/HEAD` / `output/result.json` / `run-receipt.json` / `output/selection/selection.json` / `output/selection/start.json` / `output/final/separator.json` / `output/source.json` / `source-receipt.json` / `output/start.json` / `output/final/target-remainder.bin`

同様に `batch_anchor`(v3 = artifact 9987222571)の **17 記述子も 17/17 一致**。

8-key acceptance の要求値と v4 の公開値の突合:

| 項目 | acceptance の宣言 | v4 artifact の実値(私の測定) | 一致 |
|---|---|---|---|
| `accepted_schema` | `d972.r07.fixed-lambda-cycle-batch.v4` | — | 契約どおり |
| `rank` / `generation` | 1706 / 8411 | v4 `result.json` の rank/gen | **一致** |
| `state_head` | `13c631c6…` | v4 の state_head | **一致**(= 本 run の anchor) |
| `lambda` / `lambda_sha256` | `d036e848…` | v4 の `output/final/lambda.bin` の実 sha | **一致**(= 本 run の選定 λ) |
| `target` / `target_remainder_sha256` | `954e1ba1…` | v4 の `output/final/target-remainder.bin` の実 sha | **一致**(= 本 run の t₀) |
| `target_derivation_parents` | 353 | v4 separator の ancestry 実長 **353** | **一致** |
| `previous/accepted/total_parent_batch_rows` | 128 / 128 / 256 | — | 整合(§4.4) |
| `old_oracle` | `{36104, 131, 74}` | v4 の residual 表から私が再計算した **36,104 / edge 131 / index 74** | **一致** |
| `checkpoints` | list 772 | — | `3 + 6·128 = 771` + 1 と整合 |
| （v3 側 `batch_anchor`）`old_oracle` | `{36274, 125, 70}` | v3 の residual 表から私が再計算した **36,274 / 125 / 70** | **一致** |

**注(v4 判読の訂正)**: v4 判読 §1.1 は「accepted target-derivation parents … 225」と書いたが、**v4 自身の separator の実長は 353** である。225 は **v3 の値**であり、本 run の `output/parent-intake.json` にも `intermediate_target_derivation_parents: 225` / `target_derivation_parents: 353` として別々に記録されている。累積則は 97 → 225 → 353 → **481**(毎回 +128)で完全に整合する。v4 判読の他の結論には影響しない。

### 2.2 親 inventory の全数照合

acceptance の `parents[16]`(role `batch-parent-v4`)は `files: 11,648` / `directories: 3,525`。私の照合:

| 検査 | 結果 |
|---|---|
| file 名集合 vs 親 zip の中央ディレクトリ | **11,648 / 11,648 完全一致**(片側のみ 0) |
| 各 file の bytes | **不一致 0** |
| 合計 bytes | **1,308,094,050** = P の literal `file_bytes` |
| sha256 の抜き取り | 乱択 30 本(seed 20260908)を実バイトから展開・**30/30 一致** |
| directories | 名から導出できるのは 3,487。差 **38** はすべて空ディレクトリ |
| 空 dir の正体 | `batch-parent-v4-restoration-plan.json` の `missing` 38 件と**私の導出した差集合が完全一致**・`result.created_count = 38`・`only_registered_missing_directories = true`・`all_file_bytes_authenticated_before_first_mkdir = true`・`status PASS` |
| 同じ検査を v3 親(batch-parent)にも実施 | 11,437 / 3,475(導出 3,439・差 36)・**missing 36 と完全一致**・sha 抜き取り 30/30 |
| `inner_zip` | v4 親: 7,077 entry(4,747 file / 2,330 dir)・`every_entry_full_EOF_CRC_and_SHA=true`。v3 親: 6,881(4,600 / 2,281) |
| 親 artifact メタデータ | id 10020349387 / 377,383,320 B / digest `84040119…` / run 34120585268 / head `92720e53…` / workflow `…-v4.yml` — **GitHub API と一致** |

→ **GHA の artifact zip は空ディレクトリを記録しないので、38 本は zip から復元できない。これを「登録済みの欠落 dir に限って mkdir する」という受領証つきの明示手続きで埋めており、私が独立に導いた欠落集合と 1 件の過不足もなく一致した。** 事後の自由な mkdir ではない。

### 2.3 旧 16 親の据え置き

- P stderr の `admitted-parent` は 17 role: state 10 / delta 11 / seed34 11 / packet 40 / refinement 980 / oracle 64 / e 38 / prepare 15 / block-0..3 各 3 / p1 3 / task712 50 / continuation 7,916 / **batch-parent 11,437** / **batch-parent-v4 11,648**(計 32,235)。
- **旧 64 continuation の fixed 16 file の参照経路も二重化されている**: `batch-fixed-reference-receipt.json`(reference_role = batch-parent)と `next-batch-fixed-reference-receipt.json`(reference_role = batch-parent-v4)が両方 PASS。いずれも `payload_role: continuation`・`payloads_copied_or_created: false`・JSON 5 / binary 11 の記述子。`fixed-reference-receipts-after.json` に `both_created: true`。
- **参照経由で実データが流れていることの実証**: `output/fixed/manifest.json` の `chord-tau.u8` の sha が、私が `output/selection/tree/chord-tau.u8` から実測した値と一致し、**さらに v3 / v4 / v5 の 3 run で τ がバイト完全同一**(`fixed_values_independent_of_lambda: true` の実証)。
- C stderr は `parent_files_authenticated` を role ごとに刻んでおり、`batch-parent-v4` の `total` が **11,648** で終端している。

---

## 3. (3) fresh λ_1706 oracle — 生バイトからの完全再現

### 3.1 選定 oracle の再導出

| 量 | 公刊 | 私の独立再導出 |
|---|---|---|
| `chords_checked` | 54,433 | 54,433(`chord-values.u8` / `chord-tau.u8` の実長から) |
| 残差配列 | `chord-residuals.u8` | `(values − tau·fit) mod 3` で全 54,433 件再計算 → **バイト完全一致・不一致 0** |
| `failed_count` | **36,002** | **36,002** |
| `failed-indices.u32` | 144,008 B | 私の昇順配列と**バイト一致** |
| `failed-edges.u32` | 144,008 B | **`chord_edges[failed_indices] == failed_edges` を 36,002 件すべてで確認**(λ 非依存の fixed payload との突合) |
| `first_failed_index` / `first_failed_edge` | **71 / 127** | **71 / 127** |
| `fit` | **[0,1,2,1,1]** | **一意解として再導出**(§3.4)。v4 は [2,1,0,0,2]・v3 は [1,1,2,1,0] |
| 残差値分布 | — | 0: 18,431 / 1: 17,983 / 2: 18,019 |
| `auxiliary_tests` / `aux_values` | 2 / [0,0] | **aux 枝は本番未発火**(selftest 側には `first-auxiliary` / `second-auxiliary` fixture が実在) |
| 選定 128 本の型 | — | すべて `kind=chord`・`coordinate=null`・`scalar ∈ {1,2}`(1:59 / 2:69・**0 は無し**) |
| `chord-tau.u8` の v3/v4/v5 同一性 | — | **3 run で完全同一**(λ 非依存) |
| `chord-values.u8` の v4/v5 同一性 | — | **36,315 箇所で相異**(λ 依存) |

### 3.2 三 λ の失敗集合の比較(初の 3 点データ)

| | λ_1450(v3) | λ_1578(v4) | **λ_1706(v5)** |
|---|---:|---:|---:|
| 失敗数 | 36,274 | 36,104 | **36,002** |
| `first_failed_index` | 70 | 74 | **71**(非単調・F10 と整合) |

| 遷移 | 正味 | 共通 | 旧のみ(解消) | 新のみ(新規失敗) | Jaccard |
|---|---:|---:|---:|---:|---:|
| λ_1450 → λ_1578 | **−170** | 24,041 | 12,233 | 12,063 | 0.4974 |
| λ_1578 → λ_1706 | **−102** | 23,936 | **12,168** | **12,066** | 0.4969 |

- 三 λ すべてで失敗した弦 **16,048**、どれか 1 つでも失敗した弦 **52,389**、**一度も失敗しなかった弦は 2,044 本のみ**。
- **churn の大きさはほぼ不変**(片道 ≈ 12.1k)で、正味の減少だけが −170 → −102 と小さくなっている。**「失敗数 → 0」を終端条件と見た外挿は、この 2 点差分では 36,002 / 102 × 128 ≈ 45,000 行**を要求する(rank 余地 46,550 のほぼ全部)。**2 点であり法則ではない**が、v4 判読の警告(roster サイズで残工程を見積もってはならない)は強まった。

### 3.3 消費した弦の運命(end-to-end 較正・2 段先まで)

| 検査 | 結果 |
|---|---|
| **v4 が消費した 128 弦が λ_1706 で失敗しているか** | **0 / 128**(= 128/128 が充足に転じた) |
| うち `values_new = 0` かつ `tau·fit_new = 0` | 45 |
| うち両者が等しい非零値 | 83 |
| **v3 が消費した 128 弦が λ_1578 で失敗しているか** | 0 / 128 |
| **v3 が消費した 128 弦が λ_1706(2 段先)で失敗しているか** | **0 / 128** |
| 乱択基準線(F(1578) から 128 本)の充足数 | **平均 42.97・sd 5.39・200 回の最大 60・最小 28**。二項近似でも期待 43.1 ± 5.35 |
| 乱択基準線(F(1450) から 128 本を λ_1706 で) | 期待 **43.1 ± 5.35** |
| v5 の選定 128 弦 ∩ v4 の選定 128 弦 | **0** |
| v5 の選定 128 弦 ∩ v3 の選定 128 弦 | **0** |
| v5 の選定 128 弦のうち λ_1578 でも失敗していたもの | 53 / 128(λ_1450 でも失敗: 83 / 128) |

読み方(私の判断): **z ≈ 15.9σ の観測が 1 段先・2 段先の両方で成立**したので、「消費した弦は次以降の λ の下でも充足に留まる」は偶然ではない。**producer が誤った行を足していればこの検査は落ちる**ので、fresh λ が可能にした最も強い end-to-end 較正である。ただし「定理として強制される」ことを受領証から示したわけではない(§11)。

### 3.4 fit の一意性と索引規約(F-v5-4 の解決)

- `basis-tau.u8`(5×5)は **tau の弦序数 [0,1,2,3,5] の行**であり、`basis_chords` / `selected-chords.u32` が記録する **[2,3,4,6,11] は辺 id**。継続親 9977040548 の fixed payload `chord-edges.u32` を取得して `chord_edges[[0,1,2,3,5]] = [2,3,4,6,11]` を確認し確定した。
- この 5×5 は **F₃ 上 rank 5(非特異)**。私は 3⁵ = 243 通りを全数探索し、`basis_tau · x ≡ values[[0,1,2,3,5]] (mod 3)` の解が**唯一 `[0,1,2,1,1]` = 公刊 fit** であることを確認した。**fit は自由パラメータではない。**
- **【軽微】受領証はこの二重索引規約を明示していない。** 私は最初 `tau[[2,3,4,6,11]]` を basis 行と読み、rank 4(2 行が同一)という偽の異常に到達した。v4 判読の「基準 5 弦 [2,3,4,6,11] の残差 5/5 = 0」は**どちらの読みでも真**なので過去の結論に影響は無いが、受領証に `basis_chord_ordinals` を併記するか `basis_edges` と改名するのが望ましい(数学ではなく可読性の指摘)。

### 3.5 情報性の内訳

- λ_new の character 別 support = **[1212, 0, 0, 0]** → **character 0 だけが情報的**(継続)。私の実測: 非零 **1,212**・最小 index 0・最大 index **1964**・trit 内訳 [47172, 598, 614](全 48,384 座標)。
- 内訳: **新 lead 帯の下(index < 1819)が 1,130**、**新 lead 上が 81**、**最終 lead より上の自由座標が 1**(index 1964)。合計 1,212 ✓。lead 帯の内側で lead でない座標の非零は 0。
- λ_new と λ_parent(= λ_1706)は **1,220 座標で相異**(うち 1,139 は新 lead 帯より下)→ 前段 λ のコピーではない。
- score `by_tag` total 89,616・`kappa_support` total 5,342(`aux_values` 8 個すべて 0)・`p1_equation_residual_support = 0`・`new_lambda_oracle = None`。

---

## 4. (4) 階段形・独立・λ・target・鎖(F1 全数確認)

物理行は `dtype: packed3`, `shape: [48384]` の 12,096 B。私は **1 バイト = 4 trit の little-endian 3 進**であることを、`lead` 宣言(行 0 の lead 1819 が最初の非零かつ値 1)で確定し、以後全数に適用した。

### 4.1 階段形と一次独立

| 検査 | 結果 |
|---|---|
| 行数 / 相異なる lead | 128 / **128**(lead 範囲 1819..1962・**昇順ではない** = 挿入順) |
| 自 lead の値 = 1 | **128 / 128** |
| 宣言 lead == 最初の非零座標 | **128 / 128** |
| 先行 lead(j < i)での非零 | **違反 0 件** |
| 後続 lead(j > i)での非零 | **5,456 箇所**(v4 は 5,423)→ **RREF ではなく挿入順前進消去** |

→ **階段形かつ pivot が 128 個相異なるので、128 本の一次独立は定理として従う**(producer の INDEPENDENT フラグに依存しない)。`dependent_candidates = 0` / `skipped_after_linear = []` と整合。

### 4.2 λ(F1)

| 検査 | 結果 |
|---|---|
| λ_new ⊥ 新 128 行 | **128 / 128 が 0** |
| λ_new · t_final | **1** |
| λ_new · t₀ | **1** |
| `row_pairings_sha256` | **`sha(0x00 × 1834)` を手計算して一致**(`a7b9f08b…`)。親側の `sha(0x00 × 1706)` も再計算し `84a8935d…` に一致 |
| **λ の 128 個の新 lead 成分の後退代入** | 128 成分を消去してから逆順に復元 → **128/128 一致・不一致 0**(非零 81)。**復元した λ 配列を packed3 に戻すと公刊 `lambda.bin` と sha 完全一致** |
| `direct_pairing` | `lambda_new_remainder = 1` / `lambda_parent_remainder = 1` / `lambda_pivots = 0` / `rows = 1834` |

### 4.3 target 恒等式と符号規約

- 公刊規約(coverage-receipt): `target_update_sign = remainder_before - theta * normalized_row`。すなわち `t₀ = t_final + Σ θ_j·row_j (mod 3)`。
- **私の検算**: t_final(`99c3f3ef…`)に θ_j·row_j を足し戻して packed3 に戻すと sha が **`954e1ba1a50e138a0577c27c285c21ed052f3491176d883f370e8a94d11b456a`** = **v4 の final target-remainder.bin の実 sha** = 行 0 の宣言 `parent_remainder_sha256` と一致。**不一致 0 座標。**
- **非空虚性**: θ の分布は **{0: 54, 1: 36, 2: 38}**。`target_literal_factor` の `(coefficient, exponent)` は **{(1,1):36, (0,0):54, (2,-1):38}** で、`sr(0)=0, sr(1)=1, sr(2)=-1` の 3 分岐すべてが実際に通っている。`coefficient == target.scalar` と row_id / local_row_offset の整合が **128/128**。
- `sigma` 分布 {1: 65, 2: 63} → 外側指数の 2 分岐も非空虚。

### 4.4 鎖

| 検査 | 結果 |
|---|---|
| `rolling_sha256 = sha(bytes.fromhex(predecessor) ‖ canonical(body))`(body は `schema`/`sha256`/`rolling_sha256` を除く・canonical は末尾 `\n` つき) | **128/128 再計算一致** |
| `predecessor` == 直前の head(anchor = `13c631c6…` から起算) | **128/128** |
| 128 段後の head | **`30a0c1c1cb42763112bbcae3f90bb315846cedb2dd0dfc502bf710d91db2b693`** = `result.state_head` / `checker_result.state_head` |
| instruction の自 seal | **128/128** |
| row-manifest の自 seal | **128/128** |
| `predecessor_row_manifest_sha256` 鎖(= 直前 manifest **ファイル**の sha) | **128/128**(最終 = `6e15bb69…` = separator の最後の `batch-row` の `row_manifest_sha256`) |
| `physical_sha256` == 行 bin の実 sha | **128/128** |
| `target_sha256` == sha(canonical(target.json)) | **128/128** |
| `physical_offset == 12096 × (1706 + i)` | **128/128** |
| target remainder 鎖(親→子) | **128/128** |
| `global_row_id` / `rank` / `generation` | 1706..1833 / 1707..1834 / 8412..8539 |
| ρ₂ ancestry の構造 | **481 = 32(5 key)+ 65(6 key)+ 384(10 key・role `batch-row`)**。384 = 128(v3)+ 128(v4)+ 128(本 run)。`anchor_previous/accepted/total_parent_batch_rows = 128/128/256`・`new_batch_target_steps_executed = 128` と完全整合 |
| ρ₂ の状態 | `mode=derived` / `value=1` / `original_rho2_directly_read=False` / `original_rho2_packed_sha256=b41b9e69…`(v4 と同一)→ **未昇格・限定条項 継続** |
| `native_pairing_rows_rechecked` | **[1450, 1578, 1706]**(P/C 両側の公開契約) |

---

## 5. (5) 前 run(34148667863)の P-only 出力の流用有無 — 決着

### 5.1 私の独立測定(zip 中央ディレクトリの name + 非圧縮 size + CRC32 による全数比較)

| 集計 | 値 |
|---|---:|
| `output/` 配下 file 数(今回 / 旧) | 6,587 / 6,587 |
| 和集合 / 共通名 | 7,360 / 5,814 |
| 片側のみ(今回 / 旧) | 773 / 773(内訳: `output/progress/` 772 + `output/invocations/` 1・**全部 .json**) |
| **数値 payload の一致** | **.bin 1,796 + .u8 271 + .u32 7 = 2,074 本すべて size + CRC32 一致・相異 0** |
| JSON | 一致 **645** / 相異 **3,093** |
| 拡張子なし | `output/HEAD` と `output/progress/HEAD` の **2 本が相異** |

**Astra 側の主張との照合**: Astra の express は「各 6,587 file・和集合 7,360・計算 payload(.bin 1,796 + .u8 271 + .u32 7 = 2,074)は全 size/SHA 同一・JSON は同一 645 / 差分 3,093 / 片側のみ各 773(772 checkpoint + invocation 1)・HEAD と progress/HEAD も差分」と述べている。**私の独立測定はこの内訳と数字が一つ残らず一致した**(方法は別 — Astra は展開後の size/SHA、私は zip 中央ディレクトリの size/CRC32 + 主要 file の sha256 直接検算)。加えて私は 128 本の `physical-normalized.bin` を**両 artifact から実際に展開して sha256 で 128/128 バイト同一**を確認し、`lambda.bin` / `target-remainder.bin` / `chord-residuals.u8` も同様に確認した。

### 5.2 相異の原因を私が特定した(Astra の主張には無い部分)

**原因は 2 つだけで、第 3 の原因は存在しない。**

**(i) C5 の pin 1 点が root binding 経由で全 seal に伝播した。** `output/parent-layout.json` を構造 diff すると、**相異は葉 4 つのみ**:
`code.checker.bytes`(336,211 vs 336,193)/ `code.checker.sha256`(`111e23bf…` vs `47cf2596…`)/ `portable_acceptance_sha256` / 自 `sha256`。
**17 親・anchor・batch_anchor・next_batch_anchor・registration・runtime はすべて同一。** すなわち両 run の入力で異なるのは checker のバイトだけである。これが `source.json` → `owner.json` → `start.json` → `selection/start.json` → `selection.json` → 各 manifest / instruction → rolling 鎖 → `state_head` → 772 checkpoint の**内容アドレス名**まで波及する。

**(ii) `telemetry.json`(772 本)は実測秒を持つ。**

**相異/一致の分布がこの説明を裏づける**(私の分類):

| 一致した JSON(645) | 内訳 |
|---|---|
| `target.json` 256 / `p1-reductions.json` 128 / `p1-exponent-residues.json` 128 / `p1-roots.json` 128 / `tree.json` 1 / `cochain.json` 1 / `section.json` 1 / **`parents-before.json` 1 / `parents-after.json` 1** | **root 束縛を持たない純算術文書がちょうど全部**。とくに `parents-before/after.json` が同一 ⇒ **17 親が両 run で同一物であったことの直接証拠** |

| 相異した JSON(3,093) | 内訳 |
|---|---|
| `manifest.json` 1,029 / `telemetry.json` 772 / `instruction.json` 256 / `witness.json` 128 / `reduction.json` 128 / `B.json` 128 / `raw-word.json` 128 / `raw-source.json` 128 / `physical-literal.json` 128 / `source-correction.json` 128 / `oracle-view.json` 128 / root 文書 12 | **すべて owner/source/start/selection 束縛か rolling 値か実測秒を持つ文書** |

**最終確認**: 相異した `witness-roster.json` の `witnesses` 128 件を field 単位に分解すると、`owner_sha256` / `source_sha256` / `start_sha256` / `selection_start_sha256` / `sha256` の **5 束縛 field を除けば 128/128 が完全同一**(`basis_chords`・`basis_coefficients`・`cycles`・`edge`・`eta`・`failed_chord`・`kind`・`materialization`・`scalar`・`tau` すべて一致)。**数学値が異なる文書は 1 つも存在しない。**

### 5.3 私の判定

| 問い | 判定 |
|---|---|
| 前 run の P 出力を cache/親として流用したか | **していない**。`state_head` が別(旧 `cfaec038…` / 今回 `30a0c1c1…`)・`owner.json` が別・実行秒が別(旧 P 1,786.547 / 今回 1,702.391)・`fresh_producer_invocations_registered: 1`・26 step 全 success |
| 「全出力 byte 同一」は成立するか | **不成立**(Astra と一致)。ただし**不成立の理由は数学ではなく seal である** |
| 旧 C の FAIL を今回の PASS で遡及昇格してよいか | **不可**(Astra と一致)。私はより強い理由を挙げる: **旧 run の C は比較に到達せず終了しており、昇格すべき比較結果がそもそも存在しない**。今回の C は今回の run 固有の sealed 文書に対して 128/128 を比較したのであって、旧 run の文書は別 object である |
| **新しい正の情報** | **数学対象(λ・final target・128 物理行・残差表・witness の全数学 field)は、別 commit の 2 つの独立した GHA run でバイト完全同一に再現された。** これは決定的計算の帰結として期待どおりの挙動であり、**本 lane 初の「同一数学・別 seal」の再現実験**にあたる。Astra 票の見出し(「全出力 byte 同一は不成立」)だけを読むとこの正の情報が落ちるので、両方を併記すべきである |

**【軽微 F-v5-5】rank 1834 の sealed object が 2 つ存在することになった**(旧 run の `cfaec038…` と本 run の `30a0c1c1…`)。数学は同一だが **anchor として使えるのは本 run の `30a0c1c1…` だけ**である。下流(v6 の `NEXT_BATCH_STATE`)がどちらを取るかは literal で固定されるので事故は起きにくいが、express / 裁定文中で state_head を引用するときは run 番号を必ず添えるのが安全。

---

## 6. (6) DEPENDENT fixture・四群

| 検査 | 結果 |
|---|---|
| 事前登録(driver literal `:39-42`) | `SELFTEST_NAMES` = 4 群名・`SELFTEST_REJECTIONS = {'producer-selftest':[30,10,6,7],'checker-selftest':[28,9,6,7]}` |
| 実測 | P **[30,10,6,7]** / C **[28,9,6,7]**・**完全一致**・4 群とも `status PASS`・exit 0 |
| metadata canary | 16 件・`metadata_regression_from: d972-r07-fixed-lambda-cycle-batch-v1`・`rejected_count 16`・PASS |
| gate 受領証 | `new_mathematical_selftest_groups: 2` + `new_parent_metadata_selftest_groups: 2` の内訳が P/C 双方の gate に明記 |

**第 4 群 `batch-parent1706-two-layer-admission`(新設・7 拒否/側)は本 run の新機構を狙い撃ちしている。** `producer-selftest-parent1706-fixture-gate.json` は 7 件すべてについて `intended_label_reached: true` と**互いに異なる**エラーラベルを記録している:

| 拒否ケース(P) | 到達したラベル | 何を殺すか |
|---|---|---|
| `omit-v3-from-old16-projection` | `next_batch_original_sixteen_parents_and_both_anchors` | v3 を旧 16 射影から落とす |
| `v4-local0-as-v3-local0` | `next_batch_distinct_parent_row_namespace` | 2 親の row 0 を同一視する |
| `inherited225-as-complete353` | `next_batch_225_prefix_plus_128_exact_DERIVED` | **§4.4 で私が数値検算した累積則そのもの** |
| `omit-theta0-ancestry` | `next_batch_theta_zero_ancestry_preserved` | θ=0 の行を ancestry から落とす(**実データに 54 本ある = 非空虚**) |
| `previous-target-from-start-previous` | `next_batch_previous_is_parent_start_current_target` | 親の「前の target」を「今の target」と取り違える |
| `packed-hash-as-next-plain-target` | `batch_plain_target_file_hash` | hash 領域の取り違え |
| `fixed-reference-as-colocated-payload` | `next_batch_fixed_reference_local_manifest_only` | fixed を参照でなく同居 payload にする |

C 側 7 件も同型(`missing-v3-in-old16-projection` / `reuse-v3-local0-for-v4-row0` / `inherited225-as-full353` / `drop-zero-scalar-record` / `previous-from-v4-start-previous` / `packed-hash-in-plain-target-field` / `require-colocated-fixed-payload`)。**7 種の欠陥が 7 種の異なるラベルで止まっているので、「何にでも当たる試験」ではない。**

**DEPENDENT 枝(v4 で解消した F-k64-1)は継続している**: 第 2 群に P `dependent-nonnull-lead` / C `dependent-outcome-resealed` が残り、fixture_scope にも `nonzero dependent-then-independent physical reduction/publication` と明記。第 2 群の件数(P 10 / C 9)は v4 から不変。

正直な申告(受領証自身が明記): `full1706_arithmetic_replayed: false`・`actual_anchor_arithmetic_replayed: false`・`mathematical_success_suites_rerun: 0`・`new_actual_arithmetic_executed_in_this_audit: False`。

---

## 7. (7) 費用 — F-v4-1 の決着と【重大 F-v5-1】

### 7.1 実測(P の相分解は私が telemetry を全数集計)

| | v1(k=32) | v2(k=64) | v3(k=128) | v4(k=128) | **v5(k=128)** |
|---|---:|---:|---:|---:|---:|
| 開始 rank | 1450 | 1450 | 1450 | 1578 | **1706** |
| 親 role 数 / **batch 親層数 n** | — / 0 | 15 / 0 | 15 / **0** | 16 / **1** | **17 / 2** |
| producer 実秒(自己申告) | 432.437 | 825.483 | 1,622.717 | 1,668.098 | **1,702.391124** |
| producer 実秒(harness 外形) | n/a | 826.027 | 1,623.542 | 1,669.026 | **1,703.569491** |
| checker 実秒(自己申告) | 551.331 | 1,023.682 | 1,956.121 | 2,013.378 | **2,041.425509** |
| checker 実秒(harness 外形) | n/a | 1,024.656 | 1,956.717 | 2,014.299 | **2,042.329642** |
| **P + C(自己申告)** | 983.768 | 1,849.165 | 3,578.838 | 3,681.476 | **3,743.816633** |
| **1 行あたり P+C** | 30.743 | 28.893 | 27.960 | 28.762 | **29.248** |
| 候補六相 合計 | 351.018 | 707.981 | 1,419.982 | 1,422.421 | **1,411.645316** |
| **候補あたり** | 10.969 | 11.062 | 11.0936 | 11.1127 | **11.0285** |
| selection(3 相) | 11.880 | 11.963 | 11.836 | 11.871 | **11.831757** |
| final separator | 0.869 | 0.893 | 0.936 | 1.020 | **1.085957** |
| **計測外の固定費(P 残差)** | 68.670 | 104.647 | 189.963 | 232.786 | **277.828094** |
| 出力 ZIP | 94,677,901 | 187,072,168 | 369,233,546 | 377,383,320 | **384,961,441** |
| producer cap 使用率(5,400 s) | 8.0 % | 15.3 % | 30.1 % | 30.9 % | **31.5 %** |
| checker cap 使用率(10,800 s) | 5.1 % | 9.5 % | 18.1 % | 18.6 % | **18.9 %** |

**私の独立集計**: `output/**/telemetry.json` を全数(815 本・うち本番 772 本 = 候補 128×6 + selection 3 + final 1)取得して合算 → **候補六相 1,411.645316 / selection 11.831757 / final 1.085957**。cost-receipt の同名 field と**小数点以下まで一致**。残差 = 1702.391124 − 1411.645316 − 11.831757 − 1.085957 = **277.828094**(Astra の主張値と一致)。

相分解(私の集計):

| 相 | 128 候補の合計 | 1 候補あたり | 候補時間比 | v4 の比 |
|---|---:|---:|---:|---:|
| raw | 13.362489 | 0.104394 | 0.95 % | 1.0 % |
| source | 34.059533 | 0.266090 | 2.41 % | 2.4 % |
| primal | 308.797425 | 2.412480 | **21.87 %** | 22.0 % |
| **p1(corrected_source)** | **1,011.694228** | **7.903861** | **71.67 %** | 71.6 % |
| B(四 character) | 9.430121 | 0.073673 | 0.67 % | 0.7 % |
| reduction(実消去) | 34.301520 | 0.267981 | 2.43 % | 2.3 % |
| **候補 計** | **1,411.645316** | **11.0285** | 100 % | — |

**primal + p1 = 1,320.492 s = 候補六相の 93.54 % = producer 全体の 77.57 %。律速は 5 run とも P1 補正相。**

### 7.2 【解消 F-v4-1】3 変数モデルで 5 点すべてが説明できる

n = 認証する batch 親層の数(v1/v2/v3 は 0、v4 は 1、v5 は 2)として最小二乗:

**`fixed(k, n) = 26.119 + 1.2710·k + 44.402·n`**

| k | n | 実測 fixed | 予測 | 誤差 |
|---:|---:|---:|---:|---:|
| 32 | 0 | 68.670 | 66.792 | −1.878 |
| 64 | 0 | 104.647 | 107.465 | +2.818 |
| 128 | 0 | 189.963 | 188.811 | −1.152 |
| 128 | 1 | 232.786 | 233.213 | **+0.427** |
| 128 | 2 | 277.828 | 277.615 | **−0.213** |

**k の係数 1.2710 と切片 26.119 は、v3 が 3 点から出したモデル `26.0 + 1.273k` と実質同一である。** すなわち **v3 のモデルは誤っていなかった — n 項が存在しなかっただけ**であり、v4 の「+22.5 %」も v5 の「+19.4 %」も 1 層あたり ≈ 44.4 s の同一機構で説明される。

**二読みの決着**:

- **読み A(一回性・v4 判読の推奨)= 棄却。** 予測窓 234〜236 s に対し実測 277.828。ただし A の前提(「次 run では親が 377.4 MB **に置き換わる**」)は設計変更(層を**足す**)で破られたので、**A は統制された形で試されたわけではない**。
- **読み B(親サイズ比例)= 窓(270〜280)には入るが、機構としては不正確。** 費用は「総親 envelope に比例」ではなく「**追加された層に比例**」である。層ごとの単価は v3→v4 で 42.823 s / 369.234 MB = **0.11598 s/MB**、v4→v5 で 45.042 s / 377.383 MB = **0.11935 s/MB**(サイズ +2.21 % に対し単価 +2.9 %)。
- **読み C(層ごと・私の推奨)= 全 5 点を残差 ≤ 2.8 s で説明。**

**裁定 2208 の規律の遵守**: これは単一観測での確定ではない。交絡は cost-receipt 自身が `limitations` に列挙している — 「seventeenth parent, adapter and native pairing calls are confounders」「one observation does not decide a causal timing model」。加えて `controlled_single_parent_replacement: false` / `new_seventeenth_parent_and_adapter_added: true` / `prior_value_is_current_expected_value: false` が機械票として記録済み。**C5 は `native_pairing_rows_rechecked = [1450,1578,1706]` を新たに明示呼び出ししており(P 側の公開契約も同じ)、これは層の追加とは別の増分である。私はこの 2 つを分離できていない。**

### 7.3 【重大 F-v5-1】層が積み上がる設計のままでは塔は登り切れない

producer 全体の同型フィット: **`producer(k, n) = 32.818 + 12.4294·k + 40.307·n`**(5 点で残差 ≤ 4.0 s)。

**(a) k_max はほぼ不変**(cap 5,400 s): n=2 で **k_max ≈ 425**(n=1 で 429・n=0 で 433・n=3 で 422・n=10 で 399)。**k は律速ではない。**

**(b) 層数が律速。** k=128 固定で層が毎 run 1 ずつ増えるなら、
`1614.4 + 40.31·n ≤ 5400` → **n ≤ 93.7**。
つまり **batch 層は約 93 層(= 約 11,900 行)で producer cap を固定費だけで飽和する**。rank は 1,834 + 11,900 ≈ **13,700 で頭打ち**、目標 48,384 の 28 % にすぎない。

**(c) k を上げても逃げられない。** N 回の run で 1 回あたり k 行、総計 N·k = 46,550(= 48,384 − 1,834)、最後の run の層数が N だとすると
`12.4294·k + 40.307·(46550/k) ≤ 5400 − 32.8 = 5367.2`。
左辺の最小値は k = √(40.307·46550 / 12.4294) = **388.5** のとき **2·√(12.4294 × 40.307 × 46550) = 9,657.8 s**。**cap の 1.79 倍であり、いかなる (k, N) でも成立しない。**

**⇒ 「毎 run が恒久的に 1 層ずつ足す」設計では、この cap の下で塔の頂上には到達できない。** これは 5 観測の 3 変数フィットからの外挿であって法則ではないが、**係数が 2 倍ずれても結論は変わらない**(半分の 20 s/層でも最小値 6,829 s > 5,400)。

**司令塔の判断が要る点(私からの上申)**: v6 が層を 3 にするのか、**回転させて 2 のままにする(最古の batch 親を落とす)**のか。後者なら n は定数となり `producer ≈ 1614 + 81 = 1,695 s` で頭打ちになり、k_max ≈ 425 が効いて 46,550 / 425 ≈ **110 run** で登り切れる。**この分岐は数学ではなく設計であり、次の便を設計する前に決めるべきである。** なお層を落とす場合は「落とした親の 128 行の ρ₂ ancestry を何で担保するか」が新たな検問対象になる(現行は 481 件の ancestry を実記録で運んでいる)。

**二読みを分ける次の安価な観測**: 次 run(k=128)の **P 残差 1 数値**。

- **≈ 322 s**(= 190 + 44.4×3)なら読み C 確定 → 上の壁が効く。
- **≈ 278 s** 前後で頭打ちなら層が回転している(n が 2 で一定)→ 壁は消える。
- **≈ 235 s** なら層が 1 に戻っている。

追加コストはゼロ。

### 7.4 その他の費用所見

- checker: 1,956.121(n=0)→ 2,013.378(n=1)→ 2,041.426(n=2)。増分 +57.257 / +28.048 と線形ではない。**checker 側は cap 使用率 18.9 % で余裕が大きく、律速ではない**(限定条項 6 のため段別の内訳は取れない)。
- 出力 ZIP は 369.2 → 377.4 → **385.0 MB**(+2.21 % → +2.01 %)。1 層あたり ≈ +7.6〜8.1 MB。
- 1 行あたり P+C は 27.960 → 28.762 → **29.248**(+1.7 %/run)。層が積むほど単価は上がる。

---

## 8. (8) 事前登録・恒真性・非空虚性

| 検査 | 結果 |
|---|---|
| 起動 commit | `a5b456a973f8a917f3af386d327061a02a0cf900`。WF / driver_v3 / P5 / C5 の pin が run-receipt・artifact 同梱コピー・**repo 作業ツリー**の三者一致(§1.5) |
| 事前登録の凍結 | `REGISTRATION = {batch_size 128, max_batches 1, CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX, PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY, refill False, 5400s/7168MiB, 10800s/7168MiB}` が driver に **literal**(`:34-38`)。`owner['registration'] == REGISTRATION` を run 末尾で要求 |
| **selftest の事前登録** | `SELFTEST_NAMES` 4 群名と **`SELFTEST_REJECTIONS = {'producer-selftest':[30,10,6,7],'checker-selftest':[28,9,6,7]}` が literal**(`:39-42`)。**試験件数の後付け調整は不可能** |
| 親 pin | `start['rank'] == 1706 and start['generation'] == 8411 and start['anchor_completed_steps'] == 64`(driver `:9534`)。旧層は `rank == 1578 / gen == 8283`(`:7216`)、最古層は `rank == 1450 / gen == 8155`(`:6640`)を literal 要求 |
| inventory の事前登録 | `NEXT_BATCH_INVENTORY_REGISTRATION`(P `:404-410`)が files 11,648 / file_bytes 1,308,094,050 / directories 3,525 / 2 つの roster sha を literal 固定。**私が親 artifact の実 zip から独立に再計算して一致**(§2.2) |
| **恒真 gate** | **見つからなかった。** driver `:9559-9566` は `selected = ordinary(result['selected_count'], 0, 128)` → `processed ∈ [0,selected]` → `dependent ∈ [0,processed]` → `accepted ∈ [0,processed]`、`rank == 1706 + accepted` / `generation == 8411 + accepted` / `processed == dependent + accepted` / `skipped == list(range(processed, selected))`。**accepted は固定されていない** → DEPENDENT が出ても gate は通る。**a(128) = 128 は gate の強制ではない。** 唯一の下限は `selected == 0 or accepted >= 1` |
| checker 比較件数の連動 | `checked['accepted_rows_compared'] == accepted` / `candidate_decisions_compared == processed` / `candidate_phases_compared == [{ordinal, PHASES} for i in range(processed)]` → **128 は literal ではなく accepted に紐づく** |
| progress の整合 | `progress['sequence'] == 3 + 6·processed = 771`・`current_lambda_sha256 is None` |
| silent cap | **無し**。`refill=False` / `max_batches=1` / `skipped_after_linear = []`(空 = 打ち切りなし) |
| 非空虚性(選定) | scalar {1:59, 2:69}(**0 無し**)・kind 全 chord・coordinate 全 null・roster gap≠1 が 69/127(先頭 128 整数を機械的に取ったのではないことをデータが判別) |
| 非空虚性(target) | θ ≠ 0 が **74/128**・`sr` の 3 分岐すべて発火(§4.3) |
| 非空虚性(消去) | 後続 lead での非零 5,456 箇所 → 前進消去が実際に働いている |
| 非空虚性(oracle) | 残差 0/1/2 が 18,431 / 17,983 / 18,019 とほぼ 1/3 ずつ・fit は非特異系の一意解 |
| 保証の境界 | `verified=false` / `cross_checked`(P false・C true)/ `grade2_member = grade2_nonmember = NOT_DECIDED` / `full_A0=false` / `new_lambda_oracle=None` / `old_snapshot_numeric_replays = old_insert_numeric_replays = old_success_suites = 0` を P/C 双方と driver gate が要求 |
| input preservation | `all_code_and_raw_unchanged=true` / `all_parent_files_and_directories_unchanged=true` / `acceptance_unchanged=true`・before/after の sha が一致 |

---

## 9. 限定条項(7 条)

1. **射程 = rank 1706 → 1834 の 1 batch のみ**。rank 1834 の λ\* に対する oracle は**未計算**(`new_lambda_oracle = null`・`new_final_lambda_oracle_not_inferred: true`)。**NONMEMBER 主張ではない。**
2. **a(128) = 128 は roster 前置 128 本の観測**(batch パラメータ k の性質ではない)。消化率 128 / 36,002 = **0.3555 %**。**Task 988 F4 の反例は排除されていない。** §3.2 のとおり **roster は縮む待ち行列ではない**(正味 −102 / churn 片道 ≈ 12.1k)。
3. **算術 TCB は共有カーネル 2 本を含む**(`vectorized_projection_chunk` / `sparse_adjoint`・P/C 各 1 で計 4 区間)。`current_run_call_coverage = NOT_MEASURED`・`kernel_third_independence_claimed = false`。**第三独立性はこの 2 本に及ばない。** P1 相が候補時間の 71.7 % なので前者は確実に load-bearing。
4. **旧 1,706 行の実バイトは私自身は未取得**。λ_new ⊥ 旧行 と ρ₂ の旧行部分は checker の再現に依存する。**ρ₂ は依然 DERIVED**(`original_rho2_directly_read: false`・ancestry 481 件)。
5. **harness TCB は単著**(WF 26,294 B + driver 1,145,223 B)。私は harness 出力を根拠に使わず §2〜§6・§8 を生バイトから第三実装で再導出した。ただし **§7 の相別秒だけは producer の自己計測**である(集計は私が全数やり直した)。
6. **checker の段別 timestamp は無い**(`checker-stderr.log` 16,918 行・`producer-stderr.log` 10,079 行に ISO 時刻 0 個・"seconds" 0 個)ため、checker の限界単価は run 間差商でしか出せない。**F-k64-7 継続。**
7. **私は 385 MB の ZIP を全量ダウンロードしていない**(HTTP Range で必要 entry を個別/一括取得)。ZIP 全体の sha は GitHub API の digest を採り、自分でバイト再計算していない。§5.1 の全数比較は zip 中央ディレクトリの **size + CRC32** による(主要 file は sha256 で直接検算済み)。**CRC32 一致は sha256 一致の証明ではない**が、2,074 本すべてで size と CRC32 が一致し、そのうち私が sha256 まで確認した 131 本(128 行 bin + λ + target + 残差表)は全一致である。

### 9.1 前回 7 条との対応

| v4 の条 | 本 run での扱い |
|---|---|
| 1. 射程 1 batch | **継続**(条 1) |
| 2. a(k) の意味・F4 未排除 | **継続 + 強化**(条 2・§3.2 で 3 点目を取得) |
| 3. 共有 kernel 2 本 NOT_MEASURED | **継続**(条 3) |
| 4. 旧行の実バイト未取得・ρ₂ DERIVED | **継続**(条 4) |
| 5. harness TCB 単著 | **継続**(条 5) |
| 6. checker 段別 timestamp 無し | **継続**(条 6) |
| 7. ZIP 全量 DL せず | **継続 + 方法の明記**(条 7) |

**新設は無し。7 条 → 7 条。** ただし §7.3 の **F-v5-1 は限定条項ではなく計画上の重大所見**として別立てにした。

---

## 10. 新規/継続の指摘一覧

| 札 | タグ | 内容 | 状態 |
|---|---|---|---|
| **F-v5-1** | **【重大】** | 固定費が batch 親層数に ≈ 44 s/層 で積み上がる。毎 run 恒久 1 層追加の設計では **producer cap 5,400 s を満たす (k, N) が存在しない**(§7.3)。層の回転か否かの設計判断が要る | **新設・司令塔判断待ち** |
| **F-v4-1** | 【要修正 → 解消】 | v3 の 3 点モデルは正しく、n 項が欠けていただけ。`fixed(k,n) = 26.12 + 1.271k + 44.40n`。読み A は棄却・読み B は窓には入るが機構が不正確 | **解消**(ただし交絡未分離) |
| **F-v5-2** | 【軽微】 | driver v1→v2 で `fixture_audit('before-checker')` が `execute('checker')` から `post_producer()` 冒頭へ移設。gate は残るが被覆窓が変わった | 新設・harness TCB(条 5)内 |
| **F-v5-3** | 【軽微】 | 失敗した v5 envelope-v1/v2 の YAML・旧 P/C が artifact に同梱されていない(repo にはある)。artifact 単体で失敗 2 件の物証が辿れない | 新設 |
| **F-v5-4** | 【軽微】 | `basis_chords` は辺 id・`basis-tau.u8` は弦序数で索引。受領証に明示が無く誤読を招く(私も一度誤読した)。副産物として **fit の一意性**を確認 | 新設・数学に影響なし |
| **F-v5-5** | 【軽微】 | rank 1834 の sealed object が 2 つ存在(旧 run `cfaec038…` / 本 run `30a0c1c1…`)。anchor は本 run のもののみ | 新設・引用時に run 番号を添えること |
| — | 【訂正】 | v4 判読 §1.1 の「accepted target-derivation parents 225」は v3 の値。v4 自身は **353** | v4 判読の記載訂正・結論に影響なし |
| F-k64-1 | 【解消済】 | DEPENDENT 枝 | v5 でも第 2 群に継続(P `dependent-nonnull-lead` / C `dependent-outcome-resealed`) |

---

## 11. 判読者の限界(正直な申告)

- 旧 1,706 行の実バイトを取得していないので、λ_new ⊥ 旧行 と ρ₂ 恒等式の旧行部分は checker の再現に依存している。
- 「消費した弦が次以降の λ で充足に転じる」ことが**定理として強制されるか**は、受領証だけからは示せていない。乱択基準線との対比で**偶然ではない**ことしか言えていない(1 段先・2 段先の 2 回とも z ≈ 15.9σ なので end-to-end 較正としては非常に強い)。
- 語(Ω / P1 / literal)の**再構成**は私の射程外。ε/ω/repair 指数と三層の符号規約は、coverage-receipt の宣言文字列と実データ(θ の 3 分岐・σ の 2 分岐)の突合として検証した。
- `sparse_adjoint` / `vectorized_projection_chunk` が本 run の実行経路で呼ばれた行は特定していない。
- §7.2–7.3 の外挿は **5 点フィット / うち n>0 は 2 点**であり、法則ではない。交絡(第 17 親・adapter・native pairing 1450/1578 の追加呼び出し)を私は分離できていない。**ただし §7.3(c) の不可能性は係数が 2 倍ずれても結論が変わらない。**
- §5.1 の全数比較は size + CRC32 による(条 7)。
- Astra 側の主張は §5.3 と §7 および付録 A で私の測定と個別に照合し、一致/不一致を明記した。本報告の数値はすべて私が artifact / repo の生バイトから独立に導出したものである。
- **この観点では仕様の齟齬(別対象)を見つけられなかった** — 保証ではない。

---

## 12. CV-9 裁定案・工房格付け案(一行)

**CV-9 = 同一対象(SAME OBJECT)・限定 7 条 → 工房格付け案: checker PASS / cross-checked(限定 7 条)・rank 1834 / gen 8539 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。v4 の 1706 の直系後継として置き換える(合算ではない)。**

**司令塔への一行**: 第 17 親 batch-parent-v4 は **11,648 file / 3,525 dir が実バイトで結ばれ**(名前集合とサイズは全数一致・sha は 30 本抜き取り・空 dir 38 本の復元集合は私の導出と 1 件の過不足もなく一致)、**8-key acceptance の 18 記述子すべてが v4 の実 artifact と一致**、λ_1706 oracle は**残差表 54,433 バイトが完全再現**され、128 行の階段形・λ の後退代入・target 恒等式・rolling 鎖はすべて 128/128 で通り、前 run の P 出力の流用は無い(seal は別・**数学はバイト同一**)。**唯一の重大所見は費用**: 固定費は **batch 親層 1 つあたり ≈ 44 s** で積み上がり、`fixed(k,n) = 26.1 + 1.271k + 44.4n` が 5 観測すべてを残差 ≤ 2.8 s で説明する(v3 のモデルは正しく n 項が無かっただけ)。**毎 run が恒久的に 1 層足す設計のままだと、どの k・どの run 数を選んでも producer cap 5,400 s を満たせない(最良でも 9,658 s)** — v6 で**層を回転させるか否か**を、次便の設計前に裁定されたい。分ける観測は次 run の P 残差 1 数値(≈322 s なら積み上げ確定・≈278 s なら回転)で、追加コストはゼロ。

---

## 付録 A. Astra 側の主張と私の測定の対応

| Astra の主張 | 私の測定 | 一致 |
|---|---|---|
| P/C とも PASS | `producer-exit-code.txt` / `checker-exit-code.txt` とも `0\n`・`result.status = checked.status = PASS` | **一致** |
| rank 1834 / gen 8539 | result / checker-result / HEAD / final すべて 1834 / 8539。私は 128 段の鎖から独立に導出 | **一致** |
| selected/processed/accepted 128/128/128・dependent 0 | 同・`skipped_after_linear = []` | **一致** |
| C の decisions/rows 比較 128・partial false | `candidate_decisions_compared = accepted_rows_compared = 128`・`partial = false` | **一致** |
| P 1,702.391124 s | `result.elapsed_seconds` および harness 外形 1,703.569491 | **一致** |
| selection 11.831757 | **私が 3 本の telemetry を合算して再現** | **一致** |
| 六 phase 1,411.645316 | **私が 768 本の telemetry を合算して再現** | **一致** |
| final 1.085957 | 同 | **一致** |
| **P 残差 277.828094** | **私の再計算 277.828094** | **一致**(解釈は §7 で私が独立に評価) |
| C 2,041.425509・P+C 3,743.816633 | checker-result / cost-receipt と一致 | **一致** |
| 新最終 λ の oracle は null | `new_lambda_oracle = None`・`new_final_lambda_oracle_not_inferred: true` | **一致** |
| 旧 run 比較: 各 6,587 file・和集合 7,360・payload 2,074 全同一・JSON 645 同一 / 3,093 差分・片側各 773・HEAD 2 本差分 | **私が zip 中央ディレクトリから全数独立に再計算し、内訳の数字が一つ残らず一致**(§5.1) | **一致** |
| 「全出力 byte 同一」不成立・旧 C の FAIL を遡及昇格しない | **同意**。ただし私はより強い理由を挙げる(旧 C は比較に到達していない)。加えて **数学対象は 2 run でバイト同一に再現された**という正の情報を併記すべきと考える(§5.3) | **一致 + 補強** |
| 票 file の bytes/sha(root-v5-old-failed-to-current-output-pin-comparison-v1.json ほか) | 私の手元に無く**未検証(静的主張)** | 未再測 |

## 付録 B. 主要 pin(私の実測・bytes のみ)

- run 34161493396 / attempt 1・head `a5b456a973f8a917f3af386d327061a02a0cf900`・job 101864093045・26 step / 失敗 0
- candidate artifact 10034053256 = 384,961,441 B(zip entry 11,750)・diagnostics 10034064913 = 384,961,441 B(`candidate_and_diagnostics_upload_the_same_envelope_root: true`)
- WF 26,294 B / driver_v3 1,145,223 B / P5 366,659 B / C5 336,211 B
- 旧 P archive 366,644 B / 旧 C archive 336,193 B / driver_v1 1,145,254 B / driver_v2 1,145,223 B
- registry(現行)499,053 B / registry(v4 保持)236,390 B / registry(historical)76,867 B
- shared-tcb.json 14,172 B / acceptance.json 6,032,243 B / cost-receipt.json 375,231 B / coverage-receipt.json 872,090 B / run-receipt.json 362,106 B
- 保持した v4 系列: `workflow-parent-v4.yml` 22,153 B / `workflow-parent-v4-driver.py` 536,145 B / `workflow-envelope-v1.yml` 599,085 B / `workflow-envelope-v2.yml` 20,296 B(4 本とも repo とバイト一致)
- 親: batch-parent-v4 = artifact 10020349387 / 377,383,320 B / 11,648 file / 3,525 dir / 合計 1,308,094,050 B
- 親: batch-parent = artifact 9987222571 / 369,233,546 B / 11,437 file / 3,475 dir / 合計 1,267,599,138 B
- 親: continuation = artifact 9977040548 / 304,642,285 B / 7,916 file / 1,265 dir
- λ.bin 12,096 B・target-remainder 12,096 B・物理行 12,096 B ×128(packed3・48,384 trit)
- 残差表 54,433 B / τ 272,165 B / values 54,433 B / failed-indices 144,008 B / failed-edges 144,008 B
- 前 run(34148667863)diagnostics 10029340951 = 384,805,623 B(zip entry 11,748)
