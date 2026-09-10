# 増分 CV-9 判読 — R07 fixed-lambda cycle batch **v6 / envelope-v1 / k = 128**(rank 1834 → 1962・第 18 親 batch-parent-v5 の入場・9-key acceptance・fresh λ_1834 oracle 初回・役割別経過秒計器の初回)

対象 run: **34416548935 / attempt 1**(success・head `866c87eaec6bca55d2578906c0f338cb34582373`・job 102682595416・2026-09-10T00:32:56Z completed・**全 step success**・workflow name `d972-r07-fixed-lambda-cycle-batch-v6-envelope-v1`)
候補 artifact **10131122423**(393,848,401 B・API digest `sha256:f00b171ee9c5dfec53aef2b502c8adc1bf4458c689fbad3606d47bfca6e71545`・zip entry **11,915**)
診断 artifact **10131139047**(同 bytes・digest `e6349289…`)
判読者: falsifier(非当事者・事後)。判読日 2026-09-10。
前回 CV-9 正本: `docs/notes/fixed_lambda_batch_v5_cv9_reading_v1.md`(裁定 2224・限定 7 条・F-v5-1)。
数学者審査: `docs/notes/rotation_equivalence_math_review_v1.md`(§4.6 の計器要求 3 点・3 モデル予測)。

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 7 条(§10)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 7 条)・rank 1962 / gen 8667 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。v5 の rank 1834 の直系後継として置き換える(合算ではない)。**

**a(128) = 128**(offered 128 / accepted 128 / dependent 0 / skipped 0・partial false)。rank 1962 = 1834 + 128。消化率 128 / 35,921 = **0.3564 %**。

見出し 6 つ:

1. **【F-v5-1 の分岐観測が出た — 積み上げ(読み C)で確定】P 残差 = 327.034622 s。** v5 判読が事前登録した分岐点は「≈322 s なら積み上げ・≈278 s なら回転」。**観測 327.03 は回転読みから 49 s 離れ、積み上げ読みから 5.0 s。積み上げが確定した。** 6 点再フィット `fixed(k,n) = 26.63 + 1.2596k + 45.885n`(残差 ≤ 2.60)・`producer(k,n) = 33.93 + 12.4046k + 43.52n`。**壁は残り、わずかに悪化**(最良の (k,N) でも最終 run が 10,046 s = cap の **1.86 倍**・v5 時点は 1.79 倍)。層あたり増分自体が **+42.82 → +45.04 → +49.21** と増えており、線形 n モデルは楽観側に外れる。
2. **【一次データ・本判読の最大の収穫】新計器(裁定 2228)が層費用の機構を分離した。** 層 i の再認証(P `native-metadata`)は **`20.044 + 0.0077966·R_i` 秒**(3 層の残差 ≤ 0.074 s)。すなわち **「層あたり定数 ≈ 20 s」+「Θ(k·R_i) 項 = 6.09×10⁻⁵ s/(候補×行)」の混合**であって、純 per-layer でも純 per-byte でも純 Θ(k·R) でもない。**数学者 §4.6 が「n=3 では 4 % 以内に密集して分離しない」とした 3 モデルを、計器が内側から分離した。** per-byte モデルは決定的に棄却(実測 **0.00223 s/MB** = 仮定値 0.118 s/MB の **1/53**)。
3. **【重大な副産物】v5 判読の「回転すれば k_max ≈ 425 で約 110 run」は棄却される。** 新候補の消去相は **1.507×10⁻⁴ s/(候補×行)**(v5 から得た数学者の 1.51×10⁻⁴ を再現)で、R = 48,384 では k=128 でも消去相だけで **933 s**。塔の上端では k_max ≈ **250** まで落ちる(私の見積り)。**回転しても k を上げて run 数を減らす逃げ道は無い。**(数学者 §4.4 の結論を測定で裏づけた。**外挿であり法則ではない — 裁定 2225 に従い gate ではなく診断として提出し、次の裁定に載せる前に数学者の次数確定を経ること。**)
4. **【解決】公開 selftest 版から本走版への差分は P/C とも「2 literal・1 hunk」のみ**(§1.2)。P は `BATCH_V5_INVENTORY_REGISTRATION = None → 実 dict` と `IMPLEMENTATION_COMPLETE = False → True`、C は `THIRD_BATCH_INVENTORY_REGISTRATION = None → 実 dict` と `CURRENT_PRODUCER_REGISTRATION = None → P6 pin`。**他に一切の差分なし**(git の実バイトから逆置換で全数確認)。公開 selftest は `None/False` の guard を保持したまま走った(= 本走経路は未通過)ので、**selftest の証拠力は本走内の再実行が担っている** — その in-run 実行は run binary(sha `c8a8b232…`)に対して argv 込みで記録されており、空虚ではない。
5. **【一次データ】end-to-end 較正が 3 段先まで揃った。** λ_1834 の下で **v5 が消費した 128 弦・v4 の 128 弦・v3 の 128 弦がいずれも 0/128 失敗**(= 全部が充足に転じたまま)。乱択基準線は 128 本中 **42.75 ± 5.34**(2,000 回の実験で平均 42.80・sd 5.37)→ **z ≈ 15.98 σ が 3 回**(1 段・2 段・3 段先)。v5 判読は 2 回だった。
6. **【継続】ρ₂ は依然 DERIVED、共有 kernel は NOT_MEASURED、新最終 λ の oracle は未計算。** 限定条項 3・4・1 はそのまま。ancestry は **481 + 128 = 609**(= 32 + 65 + 512、512 = 128×4)で累積則どおり。

---

## 1. (1) 規約表 diff(v5 → v6)

### 1.1 宣言の突合

| 規約 | v5 の宣言 | **v6 の宣言** | 本 run の実測 | 判別性 |
|---|---|---|---|---|
| `batch_size` / `max_batches` / `refill` | 128 / 1 / False | **同一** | selected 128 / processed 128 / refill False | — |
| `selection_policy` | `CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX` | **同一文字列** | 弦 roster 昇順先頭 128(index 120..651) | **判別**(gap≠1 が 68/127・最大 gap 60) |
| `partial_policy` | `PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY` | 同 | `partial=False` | — |
| caps | 5400s/7168MiB・10800s/7168MiB(outer 6000/11400・selftest 300/360) | **同(不変)** | P 1,756.596 / C 2,073.829(harness 外形)・`outer_terminated` **5 実行すべて False** | — |
| **親** | 17 role | **18 role**(`ROLES` literal・第 18 = `batch-parent-v5`) | acceptance の `parents` が 18 件・順序一致 | **最大の変更点** |
| **acceptance の key 数** | 8 | **9**(`batch_anchor_v5` を追加) | 実測 9 key(§2.1) | **判別**(P に 6/7/8-key の後方要求が残存) |
| **選定 λ** | λ_1706(`d036e848…`) | **λ_1834(`b224f95d…`)= v5 の final λ** | `selection/start.json` の `selection_lambda_sha256` が同 sha | **本 run の核心(§3)** |
| basis(固定 5 弦) | 辺 [2,3,4,6,11] | 同 | 残差 5/5 = 0・**fit は一意**(§3.4) | fit `[0,1,2,1,1]` → **`[2,0,2,1,2]`**(λ 依存・正しい挙動) |
| ρ₂ | `mode=derived, value=1, directly_read=False`・ancestry **481** | 同・**609** | separator に 609 = 32 + 65 + 512 | **DERIVED のまま**(未昇格) |
| lower-zero | `source_lower_zero = NOT_ASSERTED` / `physical_lower_zero = true` | 同 | separator に同値 | **契約どおり** |
| terminal | 3 値 | 同 3 値 | `BATCH_COMPLETE_CANDIDATE` | 他 2 値は canary のみ |
| **selftest 群** | **4 群**・P[30,10,6,7] / C[28,9,6,7] | **5 群**(第 5 = `batch-parent1834-three-layer-admission`)・**P[30,10,6,7,8] / C[28,9,6,7,8]** | 五群とも PASS・exit 0・**literal と件数完全一致**(§6) | **§6** |
| metadata canary | 16 件 | 同 16 件 | 16/16 拒否 PASS。**`duplicate-parent-role` の理由が `acceptance-eighteen-ordered-roles` に更新** | 非空虚 |
| 静的 registry | `…v5.audit-registry.v1`(task 1079)・499,053 B | **`…v6.audit-registry.v1`(task 1108)・867,833 B**。v5(499,053)・v4(236,390)・historical(76,867)を**併載** | 4 本とも driver literal から抽出し artifact 同梱コピーと**バイト完全一致**(§1.4) | 継承の物理保持 |
| 変換対象 | P4→P5 137→156 / C4→C5 117→140 | **P5→P6 156→177 / C5→C6 140→165** | registry の `current_transitions` に記載・私が全数分類(§1.3) | — |
| shared TCB | 4 kernel | 同 4 kernel | `current_run_call_coverage = NOT_MEASURED`・`kernel_third_independence_claimed = false` | **限定条項 継続** |
| 規約文字列(coverage-receipt) | `normalizer_convention` / `target_update_sign` / `correction_word_factor_sign` | **3 本とも v5 と文字列同一** | §4.3 で私が独立に検算し一致 | 継続 |
| **新設(計器)** | — | `parent-timing-receipt.json`(6,130,429 B)+ `parent-timing/**` 43 件 | P 26 / C 31 の完了区間・全行 accounted・unparsed 0 | **§7.3** |

→ **凍結宣言と実装・実データの間に齟齬は見つからなかった。緩めた箇所は 1 つも無い。**

### 1.2 公開 selftest 版 → 本走版の逆置換(要点)

git に両版が残っている(`da438cc7` = P6 公開 selftest 版・`429e3d7e` = C6 公開 selftest 版・`866c87ea` = 本走版)。私は両版を実バイトで取り出し、bytes/sha256 が便の主張(P6 453,749 B/`75401d4d…`・C6 427,740 B/`a5c44972…`)と一致することを確認したうえで diff を取った。

**P6(453,749 → 453,972 B・+223 B・hunk 1 つ・変更 2 行)**

```
-BATCH_V5_INVENTORY_REGISTRATION = None
+BATCH_V5_INVENTORY_REGISTRATION = {"files":11750,"file_bytes":1347269002,"directories":3547,
+  "files_sha256":"cd787746…","directories_sha256":"a5eb5b69…"}
-IMPLEMENTATION_COMPLETE = False
+IMPLEMENTATION_COMPLETE = True
```

**C6(427,740 → 428,108 B・+368 B・hunk 1 つ・変更 2 行)**

```
-THIRD_BATCH_INVENTORY_REGISTRATION: dict[str, Any] | None = None
-CURRENT_PRODUCER_REGISTRATION: dict[str, Any] | None = None
+THIRD_BATCH_INVENTORY_REGISTRATION = {同じ inventory dict}
+CURRENT_PRODUCER_REGISTRATION = {"file":"search/d972_r07_fixed_lambda_cycle_batch_v6.py",
+  "bytes":453972,"sha256":"c8a8b232…"}
```

**意味論の判読(私)**:

- `IMPLEMENTATION_COMPLETE` は `run_actual()` 冒頭の `require(IMPLEMENTATION_COMPLETE, "task1109_incomplete_static_draft")` **1 箇所のみ**で使われる。False の版では本走経路が即 fail-closed する。**したがって公開 selftest は本走経路を通っていない**(便 1128 の自己申告 `status=PASS_SELFTEST_ONLY`・「normal None/False admission guards remain frozen」と一致)。
- `BATCH_V5_INVENTORY_REGISTRATION` は `batch_v5_inventory_registration()` 1 箇所で消費され、冒頭が `require(type(registered) is dict, "batch_v5_root_restored_inventory_registration_pending")`。**None では必ず落ちる**ので、公開 selftest ではこの検査は「未登録として拒否される」側しか通っていない。
- C 側も `require(type(THIRD_BATCH_INVENTORY_REGISTRATION) is dict and type(CURRENT_PRODUCER_REGISTRATION) is dict, "v6_formal_inventory_and_final_source_binding_pending")` で同様。
- **⇒ 空虚性の帰結**: 「既採択 selftest をそのまま使用」という主張は *設計の同一性* についてのみ真であり、*本走 binary の検証* は担っていない。**その穴は本走内の再実行が塞いでいる** — `execution/producer-selftest-start.json` の argv が `python -B …/search/d972_r07_fixed_lambda_cycle_batch_v6.py --selftest --selftest-root …`(head 866c87ea の checkout)であり、5 群 61 拒否が本走内で PASS している(§6)。**この二段構えを混同しないことが判読上の要点。**
- Astra の「登録済 14 source spans・72 current metadata slot のみ結合・実変更 5 slot」は **配置作業(root 側 TEMP の手順)についての主張**であり、artifact からは検証できない(TEMP path の受領証は私の手元に無い)。**私が検証できるのは結果物であり、その結果物の差分は上記 2 literal ちょうどである。** 「5 slot 変更」と「2 literal」は矛盾しない(slot は driver 側の metadata slot を含む数え方)。私はこの手順主張を **未再測(静的主張)** として扱う。

### 1.3 registry の全数分類(私の第三実装)

`audit-region-registry.json`(867,833 B)の `current_transitions` を全数分類した:

| 側 | baseline | current | `EXACT_RAW_BYTES_UNCHANGED` | `ADDED_CURRENT` | `REGISTERED_CHANGED_RAW_BYTES` | **削除** |
|---|---:|---:|---:|---:|---:|---:|
| P | P5 156 区間 | P6 **177** | **143** | **21** | **13** | **0** |
| C | C5 140 区間 | C6 **165** | **128** | **25** | **12** | **0** |

- **新設 21(P)/25(C) はすべて第 18 親関連**(`batch_v5_*` / `promote_batch_v5_anchor` / `authenticate_third_batch_parent_metadata` / `check_third_*` / `third_batch_*` / `historical_v5_*`)**+ 計器 2 本**(P `parent_timing_complete`・C `emit_parent_timing`)。**算術核に新設は無い。**
- **`body_retention` 57 区間(P 37 / C 20)は `byte_identical: true` が 57/57**。`old_loader_context` 8 区間は **P3/C3 まで遡ってバイト同一**。
- 変更 13/12 の中で **バイト数がほぼ変わらないもの(= 等長置換)を私が実際に diff した**(等長置換は「同じ大きさの別物」を隠せるので最優先):

| 側/symbol | bytes | 実差分 | 判定 |
|---|---:|---|---|
| P `current_derived_rho2` | 1511 → 1511 | `353 → 481`(親の ancestry 件数)・`previous 128→256` / `total 256→384`・require 名も `all353… → all481…` | **正しい前進**。exact literal 要求の強度は不変 |
| P `final_manifest_value` | 1269 → 1269 | 同じ 128/256 → 256/384 | 同上 |
| P `input_preservation` | 1452 → 1452 | `WORKFLOW` 文字列 v5 → v6 | 同上 |
| P `validate_host_paths` | 392 → 391 | require 名 `…seventeen_roles → …eighteen_roles`(駆動は `ROLES`) | ラベルのみ |
| C `check_next_parent_roles` | 311 → 314 | `PARENT_ROLES → V5_PARENT_ROLES`(= 先頭 17 射影) | **必須の修正**(§2.4) |
| C `main` | 4251 → 4250 | require 名 `…seventeen… → …eighteen…` | ラベルのみ |
| C `next_batch_parent_admission_canary` | 5690 → 5693 | 同じ `V5_PARENT_ROLES` 化 | 同上 |

**弱化は 1 件も見つからなかった。**

### 1.4 registry と pin の物理固定

- driver v1 の 4 本の raw literal を抽出 → `HISTORICAL_REGISTRY_RAW` 76,867 B / `PREVIOUS_REGISTRY_RAW` 236,390 B / `PREVIOUS_V5_REGISTRY_RAW` 499,053 B / `INHERITANCE_REGISTRY_RAW` 867,833 B。**4 本とも artifact 同梱コピーと sha256 完全一致**、かつ各 `*_PIN` とも一致。
- `source_files` **12 本(P1–P6 / C1–C6)を repo 作業ツリーの実バイトで再計算 → 12/12 完全一致**(bytes + sha256)。
- **run 中の pin 検証の証拠**: `driver-bootstrap-stdout.log` に **14 行の `OK`**(v5 は 10 行)。repo 側 7 本 + `_temp` 側 7 本 — driver・v4/v5 の WF と driver・envelope-v1/v2 を `sha256sum --check --strict` + `cmp` で検査。
- 配置 4 本を私が repo 作業ツリーで再計測: P6 453,972 B / `c8a8b232…`、C6 428,108 B / `59d525f7…`、driver_v1 2,281,118 B / `88af646a…`、WF 30,603 B / `c02e1e39…` — **便の pin と 4/4 一致**。
- **artifact 同梱コピーと repo の全数照合**: `checkout-sources/`(24)+ `audit-history-sources/`(10)= **34/34** が size + CRC32 で一致。`workflow.yml` / `driver.py` / `workflow-parent-v5.yml` / `workflow-parent-v5-driver.py` / `workflow-parent-v4.yml` / `workflow-parent-v4-driver.py` / `workflow-envelope-v1.yml` / `workflow-envelope-v2.yml` の **8/8** も一致。
- **候補 artifact と診断 artifact の同一性**: 中央ディレクトリを両方読み、**entry 11,915 / 名前集合一致 / size・CRC32 の相異 0 / 展開合計 1,395,498,726 B 一致**。API digest だけが違う(ZIP コンテナのバイトが違うだけ)。`candidate_and_diagnostics_upload_the_same_envelope_root: true` を独立に裏づけた。

### 1.5 公開 JSON の key 集合の機械列挙(前 2 回の失敗型の再発防止)

**私は v5 親と v6 の同名 15 文書の top-level key 集合を機械列挙して差分を取った**:

| 文書 | v5 key 数 | v6 key 数 | 追加 | 削除/改名 |
|---|---:|---:|---|---|
| `output/HEAD` / `result.json` / `owner.json` / `source.json` / `selection/start.json` / `selection/selection.json` / `final/separator.json` / `final/manifest.json` / `fixed/manifest.json` / `progress/HEAD` / `checker-result.json` / `source-receipt.json` / `batch-observation-receipt.json` | 24/48/8/10/19/27/12/27/9/16/50/18/12 | **同数** | **なし** | **なし** |
| `output/parent-intake.json` | 41 | **49** | `accepted_batch_v5_{anchor,checker,head,parent_intake,result}_sha256`・`second_intermediate_{generation,rank,target_derivation_parents}` | **なし** |
| `output/start.json` | 39 | **44** | `accepted_batch_v5_{anchor,checker,head,parent_intake,result}_sha256` | **なし** |

**⇒ 15 文書中 13 が key 集合完全同一、残る 2 も追加のみ。改名も削除も 0。**

前 2 回の失敗型に対応する検査:

1. **C5 の失敗型(親の `selection.json` から `selection_lambda_sha256` を読もうとした)**: 私が実バイトから列挙した結果、**v5 でも v6 でも `selection_lambda_sha256` は `selection/start.json`(19 key)に存在し `selection/selection.json`(27 key)には存在しない**。C6 の第 5 群に literal canary **`lambda-source-is-completed-selection`** が入っており、この誤りは拒否 receipt として固定された。
2. **P5 の失敗型(定数 dict の key 名 `bytes` vs `file_bytes`)**: P6 の第 5 群に literal canary **`inventory-old-bytes-key`** が入っている。加えて `batch_v5_inventory_registration()` は `exact_keys(registered, ("files","file_bytes","directories","files_sha256","directories_sha256"))` で総当たり要求。

**⇒ 前 2 回の失敗型は両方とも「拒否事例の literal」として恒久化された。** これは今回の最も実務的な改善である。

### 1.6 交差辺(独立性)

- C6 の import は標準ライブラリ + numpy + `check_d972_r07_complete_oracle_cegar_continuation_v2` のみ。producer 本体への参照は path 定数(`PRODUCER_FILE`)と `CURRENT_PRODUCER_REGISTRATION`(bytes/sha の pin)だけで、**コードの取り込みは無い**。
- **注意点(新設ではないが明示)**: `CURRENT_PRODUCER_REGISTRATION` により **C は P の sha を pin する**。これは「同じ対象を見ているか」を締める束縛であって共有ではない。逆向き(P が C を pin)も定数のみ。**v1〜v5 と同じ二系統分離。**

---

## 2. (2) 第 18 親 batch-parent-v5 の入場

### 2.1 9-key acceptance

`acceptance.json`(8,338,053 B・sha `fe6e89fc…`)の top-level key は **ちょうど 9**:
`{schema, parents, anchor, batch_anchor, next_batch_anchor, batch_anchor_v5, code, runtime, registration}`。C6 の `check_acceptance_header` が `acceptance_exact_nine_plain_keys` で総当たり要求。

`batch_anchor_v5`(36 key)の束縛値と、**v5 の公開値との突合**:

| 項目 | `batch_anchor_v5` の値 | v5 側の実値 | 一致 |
|---|---|---|---|
| `accepted_schema` | `d972.r07.fixed-lambda-cycle-batch.v5` | — | — |
| `rank` / `generation` | **1834 / 8539** | v5 の final rank/gen | ✔ |
| `lambda` / `lambda_sha256` | `output/final/lambda.bin` 12,096 B / **`b224f95d…`** | v5 final λ(= 本 run の選定 λ) | ✔ |
| `target` / `target_remainder_sha256` | `output/final/target-remainder.bin` 12,096 B / **`99c3f3ef…`** | v5 final target(= 本 run の t₀) | ✔(§4.3 で私が t₀ を逆算再現) |
| `state_head` | **`30a0c1c1cb42763112bbcae3f90bb315846cedb2dd0dfc502bf710d91db2b693`** | v5 本 run の sealed state_head(F-v5-5 で 2 つあると注意された内の**採択された方**) | ✔ |
| `target_derivation_parents` | **481** | v5 の ancestry 件数 | ✔ |
| `accepted / previous / total_parent_batch_rows` | 128 / **256** / **384** | 128×3 の累積 | ✔ |
| `old_oracle` | `{36002, 127, 71}` | v5 の旧 oracle(λ_1706) | ✔ |
| `terminal` / `kind` / `upstream_completed_steps` | `BATCH_COMPLETE_CANDIDATE` / `Separator` / 64 | 同 | ✔ |

**記述子の全数照合**: `batch_anchor_v5` に埋まった `{bytes,file,sha256}` 記述子は **791 個**(名前つき 18 + checkpoints 772 + invocations 1)。**791/791 が親 inventory の同名 entry と bytes・sha256 完全一致・欠落 0・不一致 0。**

### 2.2 親 inventory の実バイト束縛

- acceptance の `batch-parent-v5` は **files 11,750 / directories 3,547 / 合計 1,347,269,002 B**。
- **私が v5 artifact 10034053256 の中央ディレクトリを直接読み、名前集合と各 entry の展開サイズを全数比較 → 11,750/11,750 が名前一致・サイズ不一致 0・合計バイト一致。**
- **directories 3,547 = 名前から導出できる 3,507 + 空 dir 40**(`ZIP-*-extracted` 3 本・`metadata-fixture/empty`・`selftest-fixtures/P/registration/host-0/parents/*` 群 など)。導出集合 ⊂ 宣言集合で、余分は 0。
- **登録定数の再計算**: `sha(canonical(files))` = **`cd787746ac83526d5979ea70b8a7c6b2e325f43a7418f7e3e3359145841647b2`**、`sha(canonical(directories))` = **`a5eb5b697fe0d8cac615eb94ff672d78450e36df7d0f5034b977af54bc11fa14`** — **P6/C6 の登録定数と完全一致**(私の第三実装)。
- **実バイトの sha256 抜き取り検査**: 名前つき 18 記述子 + 無作為 10 checkpoint + invocation 1 + 主要 payload 3 = **32 file を v5 artifact から実際に取得して sha256 を再計算 → 32/32 一致・0 不一致。**
- C6 の `THIRD_BATCH_ENTRY_PINS`(**37 entry**)も **37/37 が親 inventory・実 zip サイズと一致**。
- C6 の親コード pin `THIRD_BATCH_P/C`(v5 の P/C・366,659 B / `6e19d029…`・336,211 B / `111e23bf…`)を repo 作業ツリーで再計算 → 一致。

### 2.3 旧 17 親の参照が v5 と同一か

- acceptance の先頭 17 親の `files`/`directories` 件数と合計バイトを再計算: `continuation` 7,916 / 1,265 / 1,046,747,777、`batch-parent` 11,437 / 3,475 / 1,267,599,138、`batch-parent-v4` 11,648 / 3,525 / 1,308,094,050 — **v5 判読 付録 B の値と 1 バイトも違わない。**
- artifact id も同一(9977040548 / 9987222571 / 10020349387)。`anchor`(rank 1450・`7c0dbe47…`)・`batch_anchor`(rank 1578)・`next_batch_anchor`(rank 1706・target `954e1ba1…`)も v5 と同値。
- **旧 64 continuation の fixed payload**: 3 本の fixed-reference 受領証(`batch-` / `next-batch-` / `v5-batch-`)がいずれも `payload_role: continuation`・`payload_inventory` **17 file(16 payload + manifest.json)**・`accepted_fixed_manifest` 3,159 B / `3ec178df…`・`geometry` 1,808 B / `7365fa98…` で**完全に同一**、かつ `payloads_copied_or_created: false`。**3 層とも同じ fixed payload を参照しており、複製していない。**

### 2.4 native 6/7/8-key 受付の先頭 15/16/17 親への射影

役割 literal が明示的に階層化されている:

- C6: `V4_PARENT_ROLES`(16)・`V5_PARENT_ROLES = (*V4_PARENT_ROLES, "batch-parent-v4")`(17)・`PARENT_ROLES = (*V5_PARENT_ROLES, "batch-parent-v5")`(18)・`OLD_PARENT_ROLES = V4_PARENT_ROLES[:-1]`(15)。
- P6: `ROLES`(18)・`HISTORICAL_V5_ROLES = ROLES[:17]`。
- 要求は総当たり: `old_batch_exact_fifteen_roles` / `next_batch_exact_sixteen_roles` / `third_batch_exact_seventeen_roles`、`accepted_batch_old_six_keys` / `accepted_next_batch_old_seven_keys` / `accepted_batch_v5_old_eight_keys`。

**⇒ 6/7/8/9-key の後方互換は「先頭 15/16/17/18 親への射影」として明示され、緩んでいない。**

---

## 3. (3) fresh λ_1834 oracle — 生バイトからの完全再現

### 3.1 選定 oracle の再導出

| 量 | 公刊 | 私の独立再導出 |
|---|---|---|
| `chords_checked` | 54,433 | 54,433 |
| 残差配列 `chord-residuals.u8` | 54,433 B | `(values − tau·fit) mod 3` で全数再計算 → **バイト完全一致・不一致 0** |
| `failed_count` | **35,921** | **35,921** |
| `failed-indices.u32` | 143,684 B | 私の昇順配列と**バイト一致** |
| `failed-edges.u32` | 143,684 B | **`chord_edges[failed_indices] == failed_edges` を 35,921 件すべてで確認**(継続親 9977040548 の `output/fixed/chord-edges.u32` 217,732 B を取得して照合) |
| `first_failed_index` / `first_failed_edge` | **120 / 234** | **120 / 234**(`fe[0] = 234`) |
| `fit` | **[2,0,2,1,2]** | **一意解として再導出**(§3.4) |
| 残差値分布 | — | 0: 18,512 / 1: 18,049 / 2: 17,872 |
| `values` 分布 | — | 0: 18,060 / 1: 18,287 / 2: 18,086 |
| `auxiliary_tests` / `aux_values` | 2 / [0,0] | **aux 枝は本番未発火**(selftest 側に fixture あり) |
| 選定 128 本の型 | — | すべて `kind=chord`・`coordinate=null`・`scalar ∈ {1,2}`(1:73 / 2:55・**0 は無し**) |
| 選定 128 本 = roster 先頭 128 | — | **`selected` の `roster_index` が `sorted(failed_indices)[:128]` と完全一致** |
| `edge` の整合 | — | **`chord_edges[roster_index] == edge` を 128/128 で確認** |
| `chord-tau.u8` の λ 非依存性 | — | v5 と CRC32 一致(`a9ae54c3`)・`potential-tau.u8` も一致(`48c7448d`) |

### 3.2 四 λ の失敗集合の比較(初の 4 点データ)

| | λ_1450(v3) | λ_1578(v4) | λ_1706(v5) | **λ_1834(v6)** |
|---|---:|---:|---:|---:|
| 失敗数 | 36,274 | 36,104 | 36,002 | **35,921** |
| `first_failed_index` | 70 | 74 | 71 | **120**(非単調・大きく跳ねた) |
| `first_failed_edge` | 125 | 131 | 127 | **234** |

| 遷移 | 正味 | 共通 | 旧のみ(解消) | 新のみ(新規失敗) | Jaccard |
|---|---:|---:|---:|---:|---:|
| λ_1450 → λ_1578 | −170 | 24,041 | 12,233 | 12,063 | 0.4974 |
| λ_1578 → λ_1706 | −102 | 23,936 | 12,168 | 12,066 | 0.4969 |
| **λ_1706 → λ_1834** | **−81** | **23,978** | **12,024** | **11,943** | **0.5001** |

- 四 λ すべてで失敗した弦 **10,728**、どれか 1 つでも失敗 **53,629**、**一度も失敗しなかった弦は 804 本のみ**。
- **churn の大きさはほぼ不変**(片道 ≈ 12.0k)で、正味の減少だけが **−170 → −102 → −81** と縮んでいる。
- **【要修正・射程】「失敗数 → 0」を終端条件と見た外挿は今回さらに悪化した**: 35,921 / 81 × 128 ≈ **56,770 行** > 残 rank 余地 **46,422 行**。**すなわち roster を空にする経路は、行予算の中に収まらない。** 3 点差分であり法則ではないが、v4/v5 判読の警告(roster サイズで残工程を見積もってはならない)はさらに強まった。**Task 988 F4 の反例は依然排除されていない。**

### 3.3 消費した弦の運命(end-to-end 較正・3 段先まで)

| 検査 | 結果 |
|---|---|
| **v5 が消費した 128 弦が λ_1834 で失敗しているか(1 段先)** | **0 / 128** |
| **v4 が消費した 128 弦が λ_1834 で失敗しているか(2 段先)** | **0 / 128** |
| **v3 が消費した 128 弦が λ_1834 で失敗しているか(3 段先)** | **0 / 128** |
| 乱択基準線(λ_1706 roster から 128 本) | 理論 42.75 ± 5.34・**実験 2,000 回で平均 42.80 / sd 5.37 / 最小 26 / 最大 60** |
| 2 段・3 段の基準線 | 43.17 / 43.12(ほぼ同じ) |
| **z** | **15.98 σ が 3 回** |
| v6 の選定 128 弦 ∩ v5 / v4 / v3 の選定 128 弦 | **0 / 0 / 0**(再消費なし) |
| v6 の選定 128 弦のうち λ_1706 でも失敗 | 46 / 128(λ_1578 で 73・λ_1450 で 93) |

読み方(私の判断): v5 判読では 1 段先・2 段先の 2 回だったものが、**3 段先まで 0/128 で揃った**。producer が誤った行を足していればこの検査は落ちるので、fresh λ が可能にした最も強い end-to-end 較正である。**ただし「定理として強制される」ことを受領証から示したわけではない**(§11)。

### 3.4 fit の一意性と索引規約(F-v5-4 の再確認)

- `basis-tau.u8`(5×5)は **`chord-tau[[0,1,2,3,5]]` と完全一致**(私が実バイトで確認)。`chord-tau[[2,3,4,6,11]]` とは一致しない。
- `basis_chords` / `selected-chords.u32` の **[2,3,4,6,11] は辺 id** — `chord_edges[[0,1,2,3,5]] = [2,3,4,6,11]` を継続親の fixed payload で再確認。
- 3⁵ = 243 通りを全数探索し、`basis_tau · x ≡ values[[0,1,2,3,5]] (mod 3)` の解が **唯一 `[2,0,2,1,2]` = 公刊 fit** であることを確認。**fit は自由パラメータではない。**
- **【軽微・継続】受領証はこの二重索引規約を依然明示していない。** v5 判読の指摘(`basis_chord_ordinals` の併記か `basis_edges` への改名)は未反映。数学ではなく可読性の指摘。

### 3.5 情報性の内訳

- 選定 λ(= λ_1834)の character 別 support = **[1212, 0, 0, 0]** — v5 判読が v5 の新 λ について測った **1,212 / trit [598, 614]** と**完全一致**。すなわち **v5 の final λ が v6 の selection λ である**ことが数値でも確認できた。
- 新 λ(`b3eb3b39…`)の support = **1,303**・character 0 のみ(trit 1 が 664・trit 2 が 639)・非零 index の範囲 2..2131。
- 帯構造: **新 lead 帯より下(index < 1964)が 1,214**、**帯内が 88**(= 128 lead のうち非零のもの)、**最終 lead(2128)より上の自由座標が 1**(index 2131)。合計 1,303 ✔。**帯内で lead でない座標の非零は 0。**
- `kappa_support` total 5,368・`score_support` total 91,539・`p1_equation_residual_support = 0`・`new_lambda_oracle = None`。

---

## 4. (4) 階段形・独立・λ・target・鎖(全数確認)

物理行は `dtype: packed3`, `shape: [48384]` の 12,096 B。1 バイト = 4 trit の little-endian 3 進として全 128 行を展開し、`physical_sha256` と **128/128 一致**を確認したうえで以下を計算した。

### 4.1 階段形と一次独立

| 検査 | 結果 |
|---|---|
| 行数 / 相異なる lead | 128 / **128**(lead 範囲 **1964..2128**・**昇順ではない** = 挿入順) |
| 自 lead の値 = 1 | **128 / 128** |
| 宣言 lead == 最初の非零座標 | **128 / 128** |
| 先行 lead(j < i)での非零 | **違反 0 件** |
| 後続 lead(j > i)での非零 | **5,418 箇所**(v5 は 5,456)→ **RREF ではなく挿入順前進消去** |

→ **階段形かつ pivot が 128 個相異なるので、128 本の一次独立は定理として従う**(producer の INDEPENDENT フラグに依存しない)。`dependent_candidates = 0` / `skipped_after_linear = []` と整合。

### 4.2 λ

| 検査 | 結果 |
|---|---|
| λ_new ⊥ 新 128 行 | **128 / 128 が 0** |
| λ_new · t_final | **1** |
| λ_new · t₀ | **1** |
| `row_pairings_sha256` | **`sha(0x00 × 1962)` を手計算 → `96677f1792f186788889014ec1d487143b850fa3c8d5f4162ce878a6188fec4f` = separator の値と一致**(親側 `sha(0x00 × 1834)` も再計算し `a7b9f08b…` を確認) |
| **λ の 128 個の新 lead 成分の後退代入** | 128 成分を消去してから逆順に復元 → **48,384 座標すべて一致・不一致 0**(非零 88)。**復元した λ を packed3 に戻すと公刊 `lambda.bin` と sha 完全一致(`b3eb3b39…`)** |
| `direct_pairing` | `lambda_new_remainder = 1` / `lambda_parent_remainder = 1` / `lambda_pivots = 0` / `rows = 1962` |

### 4.3 target 恒等式と符号規約

- 公刊規約(coverage-receipt): `target_update_sign = remainder_before - theta * normalized_row`(v5 と文字列同一)。
- **私の検算**: `t_{i+1} = (t_i − θ_i·row_i) mod 3` を 128 段すべてで実行 → **不一致 0 / 128**、最終値が公刊 `target-remainder.bin` と一致。逆に t_final に Σθ_j·row_j を足し戻すと sha が **`99c3f3efbdf1b1edac1690699bd948bf8d7d938ff1c03538a5b75171a309f74a`** = **v5 の final target = `batch_anchor_v5.target` = 行 0 の `target-before.bin`** と一致。
- **非空虚性**: θ の分布は **{0: 42, 1: 50, 2: 36}** で `sr(0)=0, sr(1)=1, sr(2)=-1` の **3 分岐すべてが通っている**。`sigma` は **{1: 66, 2: 62}** で外側指数の 2 分岐も非空虚。
- coverage-receipt の `raw_readout` を 128 件集計: `section_scalar` {0:51, 2:42, 1:35}・`source_homogeneous_scalar` {1:47, 0:42, 2:39}・`omega_unrepaired` {1:47, 0:45, 2:36}・`repair_exponents` は **29 通りの相異なる三つ組**(−2..2)・`epsilon_unrepaired` は 11 通り・`raw_slp_letters` は 26..12,328。**修復・符号の分岐は広く発火している。**

### 4.4 鎖

| 検査 | 結果 |
|---|---|
| `rolling_sha256 = sha(bytes.fromhex(predecessor) ‖ canonical(body))`(body = instruction − {schema, sha256, rolling_sha256}) | **128/128 再計算一致** |
| `predecessor` == 直前の head(anchor = `30a0c1c1…` から起算) | **128/128・断絶 0** |
| 128 段後の head | **`11ade7a4b5e8bf35b072e6d4cf7bbbc27e67e0ec6a77c0e38abd45e42b70cbd9`** = `result.state_head` = `checker_result.state_head` |
| instruction の自 seal | **128/128** |
| row-manifest の自 seal | **128/128** |
| `physical_sha256` == 行 bin の実 sha | **128/128** |
| `physical_offset == 12096 × (1834 + i)` | **128/128** |
| `target_scalar` == `target.json` の `scalar` | **128/128** |
| `global_row_id` / `rank` / `generation` | 1834..1961 / 1835..1962 / 8540..8667(rank_before/after が連続) |
| ρ₂ ancestry の構造 | **609 = 32(5 key)+ 65(6 key)+ 512(10 key・role `batch-row`)**。512 = 128 × 4(v3 / v4 / v5 / 本 run)。`anchor_previous/accepted/total_parent_batch_rows = 256/128/384`・`new_batch_target_steps_executed = 128` と完全整合。**481 + 128 = 609 の累積則どおり** |
| ρ₂ の状態 | `mode=derived` / `value=1` / `original_rho2_directly_read=False` / `original_rho2_packed_sha256=b41b9e69…`(**v4・v5 と同一**)→ **未昇格・限定条項 継続** |
| `native_pairing_rows_public_contract` | **[1450, 1578, 1706, 1834]**(P/C 両側)。v5 の [1450,1578,1706] に 1834 が加わった |
| `first_candidate` 予言 | 5 条件すべて True・`expected INDEPENDENT` / `observed INDEPENDENT` / `matches_prediction True`。`first_independent_prediction_is_conditional: true`・`independence_rate_predicted: false`・`failure_set_monotonicity_asserted: false` |

---

## 5. (5) 入力保存と run の健全性

| 検査 | 結果 |
|---|---|
| `input_preservation` | `acceptance_unchanged` / `all_code_and_raw_unchanged` / `all_parent_files_and_directories_unchanged` すべて **true**、before/after の sha 一致 |
| 5 実行の cap | producer 1,756.596 s / 5,400(outer 6,000)・checker 2,073.829 / 10,800(11,400)・metadata 28.030 / 300・P selftest 3.515 / 300(360)・C selftest 6.016 / 300(360)。**`outer_terminated` は 5/5 とも False** |
| RSS | P `ru_maxrss` 621,964 KB ≈ **607 MiB** / C 1,674,728 KB ≈ **1,636 MiB**(上限 7,168 MiB) |
| stderr の全行会計 | P 10,363 行 / 674,986 B・C 17,278 行 / 1,186,347 B。**`unparsed_or_rejected_lines: 0`・`duplicate_count: 0`・`empty_lines: 0`・`all_lines_accounted: true`・`whole_raw_stderr_pin_reread: true`** |
| runtime | Python 3.13.15 / numpy 2.5.1(`expected` と `actual` が一致) |
| run-receipt の自己申告 | `workshop_CV9: PENDING`・`cross_checked: true`・`verified: false`・`full_A0: false`・`grade2_*: NOT_DECIDED`・`new_lambda_oracle: null`・`new_final_q_computed: false`・`old_mathematical_suites_rerun: 0`・`current_run_call_coverage: NOT_MEASURED`・`kernel_third_independence_claimed: false`・`selection_lambda1834_oracle_is_separate_from_new_final_lambda_oracle: true` |

---

## 6. (6) selftest 群

| 側 | 群 | 拒否件数 | 本走内の実測 |
|---|---|---|---|
| P | `k128-version-registration-and-types` | 30 | PASS |
| P | `k128-full-roster-cutoff-and-restoration` | 10 | PASS(`dependent-nonnull-lead` 継続) |
| P | `batch-parent1578-admission-and-projection` | 6 | PASS |
| P | `batch-parent1706-two-layer-admission` | 7 | PASS |
| P | **`batch-parent1834-three-layer-admission`** | **8** | PASS(**新設**) |
| C | `k128-version-registration-and-types` | 28 | PASS |
| C | `k128-full-roster-cutoff-and-restoration` | 9 | PASS(`dependent-outcome-resealed` 継続) |
| C | `batch-parent1578-admission-and-projection` | 6 | PASS |
| C | `batch-parent1706-two-layer-admission` | 7 | PASS |
| C | **`batch-parent1834-three-layer-admission`** | **8** | PASS(**新設**) |

- **source 側 literal**: P6 に `require([len(item["rejected_cases"]) for item in (first,…,fifth)] == [30, 10, 6, 7, 8], …)`、C6 に `== [28, 9, 6, 7, 8]`。**実行結果の件数と完全一致。**
- 新設第 5 群の拒否事例(P): `omit-v4-from-old17-projection` / `v5-local0-as-v4-local0` / `inherited353-as-complete481` / `omit-v5-theta0-ancestry` / `previous-target-from-v5-start-previous` / `packed-hash-as-v5-plain-target` / `v5-fixed-reference-as-colocated-payload` / **`inventory-old-bytes-key`**。
- 新設第 5 群の拒否事例(C): `omit-v4-from-native17-projection` / `alias-v5-local0-to-v4` / `alias-v5-local0-to-v3` / `drop-zero-from-complete481` / `previous-from-v5-start-previous` / **`lambda-source-is-completed-selection`** / **`registered-empty-directory-missing`** / **`uncomputed-oracle-is-zero`**。
- **【評価】この 5 群目は「§2 で私が検算した束縛の一つ一つに対応する否定形」になっている。** 特に `inherited353-as-complete481`(ancestry を親の値で代用する誤り)・`drop-zero-from-complete481`(θ=0 の記録を落とす誤り)・`uncomputed-oracle-is-zero`(未計算の新 λ oracle を 0 と読む誤り)は、私が §3・§4 で人手で潰した誤りと同じ形である。**非空虚。**
- metadata canary: **16 件・16/16 拒否・PASS**。`duplicate-parent-role` の理由文字列が **`batch_workflow:acceptance-eighteen-ordered-roles`** に更新済み。
- fixture gate: P/C とも `new_mathematical_selftest_groups: 2` + `new_parent_metadata_selftest_groups: 3` = 5 群。`parent1706_fixture_gate` / `parent1834_fixture_gate` の受領証が実在。
- **in-run 実行の証拠**: `execution/producer-selftest-start.json` の argv = `python -B …/search/d972_r07_fixed_lambda_cycle_batch_v6.py --selftest --selftest-root …`(head 866c87ea の checkout)。**公開 selftest 版ではなく本走 binary に対して実行されている**(§1.2 の空虚性の穴はここで塞がる)。

---

## 7. (7) 費用 — F-v5-1 の分岐観測と新計器の読み

### 7.1 実測(P の相分解は私が telemetry を全数集計)

| | v1(k=32) | v2(k=64) | v3(k=128) | v4(k=128) | v5(k=128) | **v6(k=128)** |
|---|---:|---:|---:|---:|---:|---:|
| 開始 rank | 1450 | 1450 | 1450 | 1578 | 1706 | **1834** |
| 親 role 数 / **batch 親層数 n** | — / 0 | 15 / 0 | 15 / 0 | 16 / 1 | 17 / 2 | **18 / 3** |
| producer 実秒(自己申告) | 432.437 | 825.483 | 1,622.717 | 1,668.098 | 1,702.391124 | **1,755.573520** |
| producer 実秒(harness 外形) | n/a | 826.027 | 1,623.542 | 1,669.026 | 1,703.569491 | **1,756.595762** |
| checker 実秒(自己申告) | 551.331 | 1,023.682 | 1,956.121 | 2,013.378 | 2,041.425509 | **2,073.026046** |
| **P + C(自己申告)** | 983.768 | 1,849.165 | 3,578.838 | 3,681.476 | 3,743.816633 | **3,828.599566** |
| **1 行あたり P+C** | 30.743 | 28.893 | 27.960 | 28.762 | 29.248 | **29.911** |
| 候補六相 合計 | 351.018 | 707.981 | 1,419.982 | 1,422.421 | 1,411.645316 | **1,415.425968** |
| selection(3 相) | 11.880 | 11.963 | 11.836 | 11.871 | 11.831757 | **11.947591** |
| final separator | 0.869 | 0.893 | 0.936 | 1.020 | 1.085957 | **1.165339** |
| **計測外の固定費(P 残差)** | 68.670 | 104.647 | 189.963 | 232.786064 | 277.828094 | **327.034622** |
| 出力 ZIP | 94,677,901 | 187,072,168 | 369,233,546 | 377,383,320 | 384,961,441 | **393,848,401** |
| producer cap 使用率(5,400 s) | 8.0 % | 15.3 % | 30.1 % | 30.9 % | 31.5 % | **32.5 %** |
| checker cap 使用率(10,800 s) | 5.1 % | 9.5 % | 18.1 % | 18.6 % | 18.9 % | **19.2 %** |

**私の独立集計**: `coverage-receipt.json` の `phase_measurements` **772 本**(= 128×6 + selection 3 + final 1)を全数合算 → **1,428.538898 s**。P 残差 = 1,755.573520 − 1,428.538898 = **327.034622** — cost-receipt の `producer_residual` と**小数点以下まで一致**。

相分解(私の集計・cost-receipt と一致):

| 相 | 128 候補の合計 | 1 候補あたり | 候補時間比 | v5 の比 |
|---|---:|---:|---:|---:|
| raw | 13.275624 | 0.103716 | 0.94 % | 0.95 % |
| source | 32.014143 | 0.250110 | 2.26 % | 2.41 % |
| primal | 308.581591 | 2.410794 | 21.80 % | 21.87 % |
| **p1(corrected_source)** | **1,015.499339** | **7.933588** | **71.75 %** | 71.67 % |
| B(四 character) | 9.451397 | 0.073839 | 0.67 % | 0.67 % |
| reduction(実消去) | 36.603874 | 0.285968 | 2.59 % | 2.43 % |
| **候補 計** | **1,415.425968** | **11.0580** | 100 % | — |

**律速は 6 run とも P1 補正相**(primal + p1 = 1,324.081 s = 候補六相の 93.55 %)。

### 7.2 【F-v5-1 の分岐観測】積み上げ(読み C)で確定

v5 判読が事前登録した分岐点(裁定 2224 に採録):

| 予測 | 意味 | 観測 327.035 との差 |
|---:|---|---:|
| ≈ **322** s | 層が積み上がる(n = 3) | **+5.02** |
| ≈ **278** s | 層が回転(n = 2 のまま) | **+49.21** |
| ≈ **235** s | 層が 1 に戻る | **+92.03** |

**⇒ 積み上げ(読み C)で確定。** cost-receipt も `accepted_batch_layers: 3`・`mathematical_parent_count: 18`・`new_eighteenth_parent_and_adapter_added: true` と明記している。

6 点再フィット:

| 対象 | モデル | 最大残差 |
|---|---|---:|
| P 残差 | **`fixed(k,n) = 26.63 + 1.2596·k + 45.885·n`** | 2.60 |
| producer 全体 | **`producer(k,n) = 33.93 + 12.4046·k + 43.520·n`** | 6.37 |
| checker 全体 | `checker(k,n) = 81.13 + 14.7129·k + 37.784·n` | 11.21 |

**ただし層あたり増分は一定ではない**: **+42.823 → +45.042 → +49.207**(2 階差 +2.216 / +4.165)。n の 2 次項を入れた `fixed = 25.94 + 1.2750k + 40.50n + 2.709·n(n+1)/2` も残差 2.89 で同等に適合する。**線形 n モデルは楽観側に外れており、v5 の 44.40 s/層 は v6 で 45.885 s/層 に上がった。**

### 7.3 【新計器】層費用の機構が分離できた(裁定 2228 の 1108 追補・数学者 §4.6 の要求 1)

`parent-timing-receipt.json`(6,130,429 B)+ `parent-timing/**` 43 件。宣言は honest:
`arrival_timestamp_used_as_internal_timing: false` / `nested_inclusive_times_summed: false` / `inclusive_intervals_added_together: false` / `causal_mechanism_identified: false` / `mathematical_success_inferred: false` / `measurement_scope = completed caller intervals and full original stderr; internal elapsed is never inferred from arrival time`。

**P 側 26 区間 / C 側 31 区間**(いずれも完了区間のみ・順序前置一致・重複 0)。

**役割別・層別の実測秒(私の集計)**:

| 側 / stage | batch-parent(R=1450) | batch-parent-v4(R=1578) | batch-parent-v5(R=1706) |
|---|---:|---:|---:|
| P `parent-inventory`(A_i + B_i) | 2.865271 | 2.940775 | 2.994358 |
| P `native-metadata`(C_i + D_i) | **31.386035** | **32.272686** | **33.381970** |
| P `state-restore-and-pairing`(F_i) | 0.827212 | 0.917901 | 0.977103 |
| **P 層計** | **35.079** | **36.131** | **37.353** |
| C `parent-inventory` | 4.303568 | 4.380753 | 4.427772 |
| C `native-metadata` | 0.329353 | 0.679774 | 1.120845 |
| C `state-restore` | 11.246076 | 12.247999 | 11.331973 |
| C `direct-pairing` | 0.923551 | 0.969458 | 1.058012 |
| C `historical-intake` | — | 0.051396 | 0.074145 |
| **C 層計** | **16.803** | **18.278** | **17.939** |

P 側非 batch 17 区間の合計 36.881 s(うち continuation の `state-restore-and-pairing` だけで 33.609 s)。P 側計測合計 145.444 s(monotonic span 145.878 s)。

**機構同定(数学者 §4.1 の記号で)**:

1. **A_i(親 envelope 全 file の hash + rglob)= 0.00223 s/MB・0.2548 ms/file**。
   → **per-byte モデル(0.118 s/MB)は 53 倍外れる。層費用は byte 数ではない。** これは §4.2 の数学者の推論(per-byte は 7.5 倍外す)を、直接測定でさらに強く裏づけた。
2. **C_i + D_i(層の 128 行再認証)は `20.044 + 0.0077966·R_i` に適合**(3 層の残差 **≤ 0.074 s**)。
   - 純 Θ(k·R_i) は**棄却**: `P/(k·R_i)` が 1.691e-4 → 1.598e-4 → 1.529e-4 と **10 % 単調に下がる**(観測ノイズ 0.07 s に対して桁違い)。
   - **層あたり定数 ≈ 20.0 s** + **6.09×10⁻⁵ s/(候補×行)**。
3. **F_i(native direct pairing)≈ 0.92〜1.06 s/層**、`historical-intake` ≈ 0.05〜0.07 s/層(D_i/E_i 相当・小さい)。

**⇒ 数学者 §4.6 が「n=3 では 3 モデルが 4 % 以内に密集して分離しない」とした問題は、計器によって内側から解けた。真の形は「定数 + Θ(k·R_i)」の混合である。**

### 7.4 【要修正 F-v6-2】計器の被覆率と欠けている 2 本

| 側 | 6 点モデルの層項 | 計器が説明する層項 | 被覆率 | 未帰属 |
|---|---:|---:|---:|---:|
| P(残差) | 45.885 s/層 | 36.188 s/層 | **78.9 %** | **≈ 9.7 s/層** |
| C(全体) | 37.784 s/層 | 17.673 s/層 | **46.8 %** | **≈ 20.1 s/層** |

- モデル側の傾きは **run 間**(版差込み)の回帰、計器側は **run 内**の分解なので、両者が一致する義務はない。**しかし現行のどの受領証もこの差を説明していない。**
- 候補: `acceptance.json` が層あたり **+2.31 MB**(6,032,243 → 8,338,053 B)成長し、parse・`deepcopy`・`canonical` + sha が複数回走る。`parent-layout.json` も 6.03 → **8.34 MB**。これらは計器の外側。
- **数学者 §4.6 の要求 3 本のうち**:
  - 要求 1(**role/層別の経過秒**)= **実装済み**。
  - 要求 2(**層 i で読んだ `ordered_reductions` 要素の総数と経過秒**)= **未実装**(私は全受領証を検索したが該当計数が無い)。これがあれば C_i の Θ(k·R_i) 係数が回帰なしで確定する。
  - 要求 3(**層 i で hash した bytes 総量・file 数・経過秒**)= **P 側のみ実装**。**C 側の `parent-inventory` 区間は `file_bytes: null`**(`files` のみ)で、C の A_i を per-byte 分解できない。
- **⇒ 要求 2 と C 側の `file_bytes` を足せば、次 run で未帰属分の大半が閉じる可能性が高い。追加コストはほぼゼロ。**

### 7.5 壁の更新(**診断であり gate ではない — 裁定 2225**)

**(a) 積み上げのまま**: `producer(k,n) = 33.93 + 12.4046k + 43.520n ≤ 5,400` → k=128 で **n ≤ 86.8**。n=3 から数えて**あと 83 run**、行にして 10,624、**rank ≈ 12,586 で頭打ち**(目標 48,384 の **26 %**)。v5 時点(13,700 / 28 %)よりわずかに悪い。

**(b) k を上げても逃げられない**: 残 46,422 行を N 回に割ると最終 run の producer は最小でも `33.9 + 2√(12.4046 × 43.520 × 46,422)` = **10,046 s = cap の 1.86 倍**(k* = 403.6)。v5 の 1.79 倍から悪化。**係数が半分になっても結論は変わらない。**

**(c) 【新】回転しても v5 の逃げ道の数字は成立しない**: 新候補の消去相は **1.507×10⁻⁴ s/(候補×行)**(v6 実測 36.604 s / 128 候補 / 平均 rank 1,897.5 — v5 から得た数学者の 1.51×10⁻⁴ を再現)。

| R | k=128 の消去相 |
|---:|---:|
| 1,898(現在) | 36.6 s |
| 12,000 | 232 s |
| 24,000 | 463 s |
| **48,384** | **933 s** |

層の再認証も R に比例する項を持つ(§7.3)ので、R = 48,384 では **1 層あたり 20.0 + 0.0078 × 48,384 = 397 s**。
私の粗い見積り(**線形外挿・法則ではない**): 回転(n=2 固定)なら塔の上端で producer ≈ 3,200 s で cap 内に収まるが、**k_max は ≈ 250 まで落ちる**(六相の R 非依存部 ≈ 10.8 s/候補 + Θ(k·R) 部 ≈ 7.3 s/候補)。
**⇒ v5 判読の「回転すれば k_max ≈ 425 で約 110 run」は棄却。** 現実的には **140〜360 run** の桁になる。**この外挿は「cost-extrapolation-needs-math-review」に該当するので、裁定に載せる前に数学者が計算量の次数をコードから確定すること。私は測定値と一次外挿までを提出する。**

### 7.6 その他の費用所見

- checker: 1,956.121(n=0)→ 2,013.378 → 2,041.426 → **2,073.026**。増分 +57.257 / +28.048 / **+31.601**。cap 使用率 19.2 % で余裕は大きい。
- 出力 ZIP は 377.4 → 385.0 → **393.8 MB**(**+8.887 MB**)。展開合計は **1,395,498,726 B**。
- **次 run(v7)の登録定数の事前計算(私からの照合材料)**: v6 candidate の zip entry は **11,915 file**(dir entry 0)・**file_bytes 1,395,498,726**・名前から導出される dir が **3,538**(空 dir を足したものが `directories` になる)。**v7 の `BATCH_V6_INVENTORY_REGISTRATION` がこれと違えば、その時点で何かがおかしい。**

---

## 8. (8) 事前登録・恒真性・非空虚性

| 検査 | 結果 |
|---|---|
| `accepted` が [0,128] で固定されていないか | **固定されていない**。`accepted_new_rows` は `len(state.rows)` で算出。`terminal` は `LINEAR_MEMBERSHIP_CANDIDATE` / `BATCH_COMPLETE_CANDIDATE` / `COMPLETE_ZERO_CANDIDATE` の 3 分岐、`skipped_after_linear` は linear 時のみ非空。`selection_readout` は `integer(…, 0, BATCH_SIZE)` |
| `rank == 1834 + accepted` | **1962 = 1834 + 128**。P/C/HEAD/final すべて一致。私は 128 段の鎖から独立に導出 |
| 128 という数の literal 化 | `("accepted_new_rows", 128)` 等の literal は **親(v3/v4/v5)についての登録事実**であり、本 run の結果には課されていない |
| silent cap | **無し**。5 実行の `outer_terminated` すべて False・RSS 上限まで 4 倍以上の余裕・`partial=False` |
| `SELFTEST_REJECTIONS` の literal | P `== [30,10,6,7,8]` / C `== [28,9,6,7,8]` を source に確認、実行結果と一致 |
| 選定の判別性 | roster index 120..651・**gap≠1 が 68/127・最大 gap 60**。「先頭 128 連番」ではない |
| 予言の非空虚性 | `first_candidate` の 5 条件がすべて実測 True で `INDEPENDENT` を予言し的中(4 回目)。ただし `first_independent_prediction_is_conditional: true` と自己申告どおり **条件つき・1 件のみ** |
| 「見つからなかった」を非存在と読んでいないか | `new_lambda_oracle: null`・`failure_set_monotonicity_asserted: false`・`independence_rate_predicted: false`。**NONMEMBER 主張は一切していない** |
| 個数一致だけで済ませていないか | 済ませていない。§3・§4 は**バイト同一性**と**代数恒等式**で確認している |
| UNKNOWN の置き場 | `NOT_DECIDED`(grade2)・`NOT_MEASURED`(kernel coverage)・`NOT_ASSERTED`(source_lower_zero)・`NOT_APPLICABLE`(positive_readout / adapter)・`PENDING`(workshop_CV9)が実際に使われている |

---

## 9. 新規/継続の指摘一覧

| 札 | タグ | 内容 | 状態 |
|---|---|---|---|
| **F-v6-1** | **【重大・計画】** | F-v5-1 の分岐観測は **327.03 s = 積み上げ**。壁は残り悪化(最良 (k,N) で 1.86× cap)。さらに新計器により層費用が `20.0 + 0.0078·R_i` と判明したので、**塔が高くなるほど 1 層が高くなる** — 積み上げ設計の壁は n について線形より悪い。**司令塔判断(回転するか)は依然必要。** かつ v5 の逃げ道の数字(k_max 425 / 110 run)は棄却され、正しくは k_max ≈ 250(上端)・140〜360 run 級 | **新設(F-v5-1 の後継)** |
| **F-v6-2** | **【要修正・計器】** | 新計器は P の層項の **78.9 %**・C の **46.8 %** しか説明しない(未帰属 P ≈9.7 / C ≈20.1 s/層)。数学者 §4.6 の**要求 2(`ordered_reductions` 要素数)は未実装**、**要求 3 は C 側 `file_bytes: null` で片肺**。両方足すのは低コストで、次 run で未帰属分が閉じる見込み | 新設 |
| **F-v6-3** | 【軽微】 | 古いエラーラベルの残留: P6 `production_requires_exact_seventeen_roots_acceptance_and_output`(実際の判定式は `ROLES`=18 role 由来で正しい)。数学的意味は変わらないが、ラベルを根拠に読む監査を誤らせる | 新設 |
| **F-v6-4** | 【軽微】 | 「既採択 selftest をそのまま使用」は **設計の同一性についてのみ真**。公開 selftest は `None/False` guard を保持して走っており、本走経路は通っていない。**証拠力は in-run 再実行が担う。** 便の文言にこの区別を書くと誤読が減る | 新設 |
| **F-v5-1** | 【重大 → 分岐決着】 | 「積み上げか回転か」の観測は取れた(上記 F-v6-1 へ引き継ぎ) | **観測完了・設計判断は未決** |
| **F-v5-2** | 【軽微】 | `fixture_audit('before-checker')` が `post_producer()` 冒頭にある構造は driver v6/v1 でも同じ。被覆窓の指摘は継続 | 継続(harness TCB・限定条項 5) |
| **F-v5-3** | 【軽微】 | artifact が持ち込む envelope 履歴は **v4 系列のみ**(`workflow-envelope-v1/v2.yml` は v4 期のもの)。v5 期に失敗した envelope-v1/v2 は依然同梱されない。v6 は失敗発射が無いので新たな欠落は無い | 継続 |
| **F-v5-4** | 【軽微】 | `basis-tau.u8` の行索引が**弦序数** [0,1,2,3,5]、`basis_chords` が**辺 id** [2,3,4,6,11] という二重索引が受領証に明示されていない。私は今回も再導出で確定し、fit の一意性を全数探索で確認した | 継続(未反映) |
| **F-v5-5** | 【軽微 → 解消】 | rank 1962 の sealed object は本 run のもの 1 つのみ。重複は生じていない | 解消 |
| F-k64-1 | 【解消済】 | DEPENDENT 枝 | v6 でも第 2 群に継続(P `dependent-nonnull-lead` / C `dependent-outcome-resealed`) |

---

## 10. 限定条項(7 条)

1. **射程 = rank 1834 → 1962 の 1 batch のみ**。rank 1962 の λ\* に対する oracle は**未計算**(`new_lambda_oracle = null`)。**NONMEMBER 主張ではない。**
2. **a(128) = 128 は roster 前置 128 本の観測**(batch パラメータ k の性質ではない)。消化率 128 / 35,921 = **0.3564 %**。**Task 988 F4 の反例は排除されていない。** §3.2 のとおり **roster を空にする経路は行予算に収まらない**(必要 ≈56,770 行 > 残 46,422 行)。
3. **算術 TCB は共有カーネル 2 本を含む**(`vectorized_projection_chunk` / `sparse_adjoint`・P/C 各 1 で計 4 区間)。`current_run_call_coverage = NOT_MEASURED`・`kernel_third_independence_claimed = false`。**第三独立性はこの 2 本に及ばない。** P1 相が候補時間の 71.75 % なので前者は確実に load-bearing。
4. **旧 1,834 行の実バイトは私自身は未取得**。λ_new ⊥ 旧行 と ρ₂ の旧行部分は checker の再現に依存する。**ρ₂ は依然 DERIVED**(`original_rho2_directly_read: false`・ancestry 609 件・`original_rho2_packed_sha256` は v4/v5 と同一)。
5. **harness TCB は単著**(WF 30,603 B + driver 2,281,118 B)。私は harness 出力を根拠に使わず §2〜§6 を生バイトから第三実装で再導出した。ただし **§7.1 の相別秒と §7.3 の役割別秒は producer/driver の自己計測**である(集計は私が全数やり直した)。
6. **checker の相別 timestamp は依然無い**。新計器は C 側にも 31 区間の stage 秒を与えたが、これは**親認証部分のみ**であり、C 全体 2,073 s のうち計測できたのは **67.1 s(3.2 %)**にすぎない。**F-k64-7 継続。**
7. **私は 394 MB の ZIP を全量ダウンロードしていない**(HTTP Range で必要 entry を個別/一括取得)。ZIP 全体の sha は GitHub API の digest を採り、自分でバイト再計算していない。candidate/diagnostics の同一性判定と親 inventory の全数照合は zip 中央ディレクトリの **size + CRC32** による(主要 file は sha256 で直接検算済み: 親 32 本・本 run の 128 行 bin + λ + target 等)。**CRC32 一致は sha256 一致の証明ではない。**

### 10.1 前回 7 条との対応

| v5 の条 | 本 run での扱い |
|---|---|
| 1. 射程 1 batch | **継続**(条 1) |
| 2. a(k) の意味・F4 未排除 | **継続 + 悪化**(条 2・4 点目のデータで外挿がさらに悪化) |
| 3. 共有 kernel 2 本 NOT_MEASURED | **継続**(条 3) |
| 4. 旧行の実バイト未取得・ρ₂ DERIVED | **継続**(条 4) |
| 5. harness TCB 単著 | **継続**(条 5) |
| 6. checker 段別 timestamp 無し | **継続 + 部分緩和**(条 6・親認証部分のみ 3.2 % が可視化) |
| 7. ZIP 全量 DL せず | **継続 + 方法の明記**(条 7) |

**新設は無し。7 条 → 7 条。** F-v6-1/2/3/4 は限定条項ではなく所見として別立て(§9)。

---

## 11. 判読者の限界(正直な申告)

- 旧 1,834 行の実バイトを取得していないので、λ_new ⊥ 旧行 と ρ₂ 恒等式の旧行部分は checker の再現に依存している。
- 「消費した弦が次以降の λ で充足に留まる」ことが**定理として強制されるか**は、受領証だけからは示せていない。3 段先まで z ≈ 15.98σ が揃ったので**偶然ではない**ことしか言えていない。
- 語(Ω / P1 / literal)の**再構成**は私の射程外。今回は `target_literal_factor` の三つ組の再検算は行わず、代わりに **target 恒等式を 128 段すべて数値で再現**した(こちらの方が強い)。θ / sigma / repair 指数の分岐分布で非空虚性を確認している。
- `sparse_adjoint` / `vectorized_projection_chunk` が本 run の実行経路で呼ばれた行は特定していない。
- §7.5 の外挿は **6 点フィット + 単一 run の R 傾き**からのものであり、法則ではない。交絡(第 18 親・adapter・native pairing 1834 の追加呼び出し・acceptance の成長)を私は完全には分離できていない。**ただし §7.5(b) の不可能性は係数が 2 倍ずれても結論が変わらない。** §7.5(c) の k_max ≈ 250 は特に粗く、**数学者の次数確定を経ずに裁定に載せてはならない。**
- Astra の「14 source spans / 72 metadata slots / 5 slot 変更」という**配置手順の主張は、TEMP 側の受領証を持たないため未再測**である。私が検証したのは結果物であり、その差分は 2 literal ちょうどであった。
- root-task1137 / 1138 / 1139 / 1141 の受領証(TEMP path)も**未再測(静的主張)**。
- **この観点では仕様の齟齬(別対象)を見つけられなかった** — 保証ではない。

---

## 12. CV-9 裁定案・工房格付け案(一行)

**CV-9 = 同一対象(SAME OBJECT)・限定 7 条 → 工房格付け案: checker PASS / cross-checked(限定 7 条)・rank 1962 / gen 8667 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。v5 の 1834 の直系後継として置き換える(合算ではない)。**

**司令塔への一行**: 第 18 親 batch-parent-v5 は **11,750 file / 3,547 dir(空 40 を含む)が実バイトで結ばれ**(名前集合とサイズは全数一致・登録 sha は私の第三実装で再計算一致・sha256 は 32 本抜き取りで全一致)、**9-key acceptance の 791 記述子すべてが v5 の実 artifact と一致**、fresh λ_1834 の oracle は**残差表 54,433 バイトが完全再現**(failed 35,921・first 120/234)、128 行の階段形・λ の後退代入(48,384 座標すべて)・target 恒等式・rolling 鎖・`sha(0x00×1962)`・ρ₂ ancestry 481+128=609 はすべて 128/128 で通り、公開 JSON の key 集合は 15 文書中 13 が完全同一・残る 2 も追加のみで**前 2 回の失敗型(P の `bytes`/`file_bytes`・C の親 selection.json の key)は両方とも literal 拒否 canary として恒久化された**。**費用については分岐観測が出た** — P 残差 **327.03 s**(積み上げ予測 322・回転予測 278)で**積み上げが確定**、壁は残って悪化(最良でも cap の 1.86 倍)。**さらに新計器が層費用を `20.0 s + 0.0078·R_i` と分離した** — per-byte モデルは 53 倍外れ(実測 0.00223 s/MB)、真の形は「定数 + Θ(k·R_i)」。この結果 **v5 の逃げ道「回転すれば k_max ≈ 425 で約 110 run」は棄却**され、上端では k_max ≈ 250・140〜360 run 級になる。**計器は要求 3 本のうち 1 本だけが完全実装で、要求 2(`ordered_reductions` 要素数)と C 側 `file_bytes` が欠けており、層項の 21 %(P)/ 53 %(C)が未帰属のまま。この 2 つを足すのはほぼ無料なので、次便の設計に入れることを進言する。** 費用の外挿は裁定 2225 と「cost-extrapolation-needs-math-review」に従い **gate ではなく診断**として提出する。

---

## 付録 A. Astra 側の主張と私の測定の対応

| Astra の主張 | 私の測定 | 一致 |
|---|---|---|
| run 34416548935/1・head 866c87ea…・job 102682595416・全 step success | `runtime-observation.json` / `run-receipt.launch` と一致。exit code 6 本すべて 0 | **一致** |
| P step 14 = 23:25:59–23:55:19Z(1,760 s) | P 自己申告 1,755.573520・harness 外形 1,756.595762 | **一致**(整合) |
| C step 16 = 23:55:38–00:30:12Z(2,074 s) | C 自己申告 2,073.026046・harness 外形 2,073.828863 | **一致** |
| candidate 10131122423 = 393,848,401 B / `f00b171e…` | GitHub API と一致・zip entry 11,915 | **一致** |
| diagnostics 10131139047 = 同 bytes / `e6349289…` | **中央ディレクトリを両方読み entry/名前/size/CRC32 が完全一致**(digest 差は ZIP コンテナ差) | **一致 + 補強** |
| 4 配置 file の bytes/sha | repo 作業ツリーで 4/4 再計算一致 | **一致** |
| k 128 / maxbatch 1 / no-refill・caps 不変 | registration・run-receipt・cost-receipt すべて一致・`outer_terminated` 5/5 False | **一致** |
| P/C 既採択 selftest をそのまま使用 | **設計としては真**(2 literal 差のみ)。**ただし公開 selftest は本走経路未通過**(§1.2)。本走内で 5 群が run binary に対し再実行され PASS | **一致 + 但し書き** |
| 「P-C 公開 selftest 時からの 2 literal 逆置換」 | **P 2 literal・C 2 literal・各 1 hunk・他に差分なし** を git 実バイトで確認 | **一致** |
| 「登録済 14 source spans・72 current metadata slot のみ結合・実変更 5 slot」 | **TEMP 側の手順主張のため未再測**。結果物の差分は上記のとおり | 未再測 |
| 第 18 親 inventory は root-task1137 で正式受領 | registry の `parent_inventory_registration.root_receipt` に 18,470 B / `9ba60303…` として記載。**TEMP path のため私は未再測**。ただし登録値そのものは私が実バイトから再計算し一致 | 未再測(値は一致) |
| 正式 accepted は 2224 の rank 1834/gen 8539 を保持・A0 actual 0/1・verified=false | 本判読で rank 1962/gen 8667 へ更新を提案(直系後継・合算せず) | **手続き一致** |

## 付録 B. 主要 pin(私の実測・bytes のみ)

- run 34416548935 / attempt 1・head `866c87eaec6bca55d2578906c0f338cb34582373`・job 102682595416
- candidate artifact 10131122423 = 393,848,401 B(zip entry 11,915・展開合計 1,395,498,726 B)・diagnostics 10131139047 = 393,848,401 B(内容同一)
- WF 30,603 B / driver_v1 2,281,118 B / P6 453,972 B / C6 428,108 B
- 公開 selftest 版: P6 453,749 B(commit da438cc7)/ C6 427,740 B(commit 429e3d7e)
- registry(現行)867,833 B / registry(v5 保持)499,053 B / registry(v4 保持)236,390 B / registry(historical)76,867 B
- acceptance.json 8,338,053 B / parent-layout.json 8,336,957 B / result.json 208,894 B / checker-result.json 15,909 B
- cost-receipt.json 376,210 B / coverage-receipt.json 872,125 B / run-receipt.json 522,127 B / shared-tcb.json 15,160 B
- **parent-timing-receipt.json 6,130,429 B**(新設)+ `parent-timing/**` 43 file
- 保持した v5 系列: `workflow-parent-v5.yml` 26,294 B / `workflow-parent-v5-driver.py` 1,145,223 B(repo とバイト一致)
- 保持した v4 系列: `workflow-parent-v4.yml` 22,153 B / `workflow-parent-v4-driver.py` 536,145 B / `workflow-envelope-v1.yml` 599,085 B / `workflow-envelope-v2.yml` 20,296 B(4 本とも repo とバイト一致)
- 親: batch-parent-v5 = artifact 10034053256 / 384,961,441 B / 11,750 file / 3,547 dir / 合計 1,347,269,002 B
- 親: batch-parent-v4 = artifact 10020349387 / 377,383,320 B / 11,648 file / 3,525 dir / 合計 1,308,094,050 B
- 親: batch-parent = artifact 9987222571 / 369,233,546 B / 11,437 file / 3,475 dir / 合計 1,267,599,138 B
- 親: continuation = artifact 9977040548 / 304,642,285 B / 7,916 file / 1,265 dir / 合計 1,046,747,777 B
- λ.bin 12,096 B・target-remainder 12,096 B・物理行 12,096 B ×128(packed3・48,384 trit)
- 残差表 54,433 B / chord-tau 272,165 B / chord-values 54,433 B / failed-indices 143,684 B / failed-edges 143,684 B / chord-edges(継続親)217,732 B
- 選定 `selection.json` 31,004 B / `selection/start.json` 1,115 B / `final/separator.json` 347,168 B / `final/manifest.json` 1,925 B
- checkout-sources 24 file / audit-history-sources 10 file(**34/34 が repo とバイト一致**)
- **v7 の登録定数の事前計算値**: files 11,915 / file_bytes 1,395,498,726 / 名前由来 dir 3,538(+ 空 dir)


---

**裁定 2244(司令塔・2026-09-10)格付け**: 本判読(原本 `scratchpad/fal_cv9_fixed_lambda_batch_v6_report_v1.md` 65,070 B・sha256 34a1b77e232709c268ddbd0f80f3e5d779b1823b0b3f63fad2072cde1894c177・工房 sha256sum で pin)を正本として採用。CV-9 = 同一対象・限定 7 条(新設なし)→ **rank 1962/gen 8667 を cross-checked(限定 7 条)で受理し v5 の 1834 の直系後継として置き換える(合算しない)**・verified=false・grade-2 NOT_DECIDED・A0 actual 0/1 不変。計器の読み(層 i の再認証 = 20.044 + 0.0077966·R_i s = 層あたり定数 ≈ 20 s + Θ(k·R_i))は診断であって gate ではない(2225)。F-v6-1(壁は n について線形より悪い・v5 の「回転すれば k_max ≈ 425」は棄却・回転時の上端 k_max ≈ 250 は診断値)は**計画上の所見**であり、数学者の次数確定を経てから裁定に載せる(memory: cost-extrapolation-needs-math-review)。F-v6-2(計器が P 層項の 78.9 %/C 46.8 % しか説明しない → ordered_reductions 要素数と C の file_bytes を追加)は v7 driver への要修正。

**裁定 2245 訂正(trailer 表記)**: 上記 trailer の旧表記「回転の逃げ道 k_max ≈ 250 は棄却」は誤りで、棄却されたのは v5 の「k_max ≈ 425・約 110 run」であり、250 は回転時の上端の診断値(gate ではない)。本文・express の射程で扱う。

**裁定 2246 追補(数学者追補より・計器の読みの但し書き)**: 層 i の再認証 = 20.044 + 0.0077966·R_i s の (a) c₁ 項の k は**親の k(k_par)**であって現 run の k ではない (b) 定数 20.0 s も Θ(k_par)(候補あたり 0.153 s)(c) 「per-byte 棄却」は結論は正しいが理由は要修正 — 費用は byte 比例のままで、envelope の byte(0.00223 s/MB)ではなく parse される Θ(R) JSON(reduction.json/physical-literal.json・層あたり 129.78/141.43/153.19 MB)の byte(0.0853 s/MB・単価差 38.2 倍)(d) 積み上げ壁は n の 2 次(T_P(n) = 1,580.7 + 46.68n + 0.5685n²)で線形 n モデルの n ≤ 86.8 は楽観 (e) 回転時の上端は層費用も K 比例なので 250 より小さい(数値は診断)。
