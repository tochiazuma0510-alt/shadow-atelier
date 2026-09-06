# fixed-lambda cycle batch v2(k = 64・rank 1450 → 1514)増分 CV-9 判読(falsifier 逐語・裁定 2176 で正本化)
著者: falsifier(opus/max・非当事者)。司令塔が scratchpad 報告書(sha256 先頭 16 桁 6bd0e23eac0a4033・保存ファイル全体)を逐語転記(2026-09-06)。

**工房裁定(2176)**: CV-9 = **同一対象**(限定 9 条)→ **batch v2 状態 rank 1514/gen 8219 を受理**(cross-checked 限定 9 条・v1 の 1482・control-96 の 1482 とは別状態で合算しない・GRADE2 NOT_DECIDED・verified=false)。第三実装で再導出: 全 54,433 弦の残差再計算 → 失敗 36,274/先頭 index 70/edge 125 を再現し failed-indices.u32 と全件バイト一致(v1・control-96 と三点一致)・階段形 64/64(挿入順前進消去)・λ ⊥ 新 64 行 64/64・λ·t_final = λ·t₀ = 1・row_pairings = sha(0x00×1514)・λ の新 64 lead 成分を逆順後退代入で完全再現・t_final に θ_j·n_j を逆順足し戻して t₀ の sha = 親 anchor 3bba0da3…(θ ≠ 0 が 42/64)・head 鎖 64/64・checkout-sources 24/24 が repo とバイト一致。事前登録は健全(REGISTRATION・SELFTEST_REJECTIONS {P:[30,8], C:[28,7]} が literal 登録で final gate 完全一致・anchor literal・恒真 gate/silent cap なし・rank == 1450 + accepted なので独立率 1.00 は gate の強制ではない・checker の変更は締め方向)。**k = 64 の独立率 = 64/64(a/k 1.00)**・P 825.5 s/C 1,023.7 s・P+C 28.9 s/行(run 単位・v1 比 1.064 倍速)・**限界単価 P+C 27.0 s/行(逐次 42.4 に対し 1.57 倍速)**・候補あたり 11.06 s(primal+p1 93.7 %・P 全体の 80.3 %)。**F-k64-2(重要・枠組みの言い換え)**: a/k は batch サイズの関数ではない — BATCH_SIZE が算術に効くのは failed[:BATCH_SIZE] の 1 箇所で消去は候補ごと逐次(rank_before = 1450+i)・**前半 32 本は v1 と物理行までバイト同一** ⟹ 本 run の新規情報は roster index 123..177 の 32 本だけ・正しい量は「roster 前置長 n における a(n)」(a(32) = 32・a(64) = 64・a(128) は k = 128 の batch でも k = 64 の続きでも同じ数)・k を上げる価値は費用側のみ・F4 反例は未排除(64/36,274 = 0.18 %)。**F-k64-1(要修正)**: v2 の selftest は 3 群 → 2 群で dependent-independent-target-signs-and-packed と private-prefix-publication-resume-and-isolation が消え、producer の canary_reduction(F4 第二反例)が削除 ⟹ 本 run で DEPENDENT 枝は合成でも実データでも一度も通っていない(緩和: 算術領域は v1 とバイト同一・独立性主張は階段形実測に依拠で silent な誤りは通らない = risk は liveness)。継承が cert に未記録 → arithmetic_selftest_inherited_from と不変算術領域の行範囲/sha を受領証に足す(再走コスト 0)。**F-k64-4**: 固定費は固定でない(68.7 → 104.7 s・ZIP 94.7 → 187.1 MB・fixed(k) ≈ 32.7 + 1.124k)⟹ producer cap から取れる k は 484 → ≈ 436・必要 run 98 → ≈ 107。軽微: F-k64-3 空き座標の債務 112 → 114(v1 F-flb-5 を反証)/ F-flb-3 解消(diagnostics = candidate は仕様・run-receipt が宣言・187 MB の情報ゼロ重複)/ F-flb-1 継続(共有 TCB 2 本は sha 不変・P1 経路 72 % で load-bearing・docstring "Independent" が checkout-sources に同梱・F8.89 の登録は返信側で run の cert には無い)/ F-k64-5 語長は raw/source 相を厳密支配するが費用の 3.5 %・p1+primal 93.7 % は無相関(候補秒 ≈ 10.794 + 0.0424×語長/1000)/ F-k64-6 v1 報告の訂正(partial_policy は v1 にも存在)。限定 9 条: (i) 射程 = λ_1450 固定・roster 前置 64 本の 1 batch(前半 32 は v1 と同一行)・NONMEMBER ではない (ii) a(64) = 64 は前置長 64 の一点 (iii) DEPENDENT 枝は本番・合成とも未通過 (iv) 共有 TCB 2 本が P1 相で load-bearing・cert 未登録 (v) 旧 1450 行の実バイト未取得(λ ⊥ 旧行は checker 実測に依拠)(vi) 段別 timestamp なし (vii) elapsed 非 cross-check (viii) λ·ρ₂ DERIVED (ix) rank 1514 の oracle 未計算。

---

# 増分 CV-9 判読 — R07 fixed-lambda cycle batch **v2 / k = 64**(rank 1450 → 1514)

対象: run **34011731149/1**(success・event=push・head `c2a8a6acd60c0cd859edd2e262cfce074b3acaf1`・04:31:50Z→05:04:55Z)
候補 artifact **9983058782**(187,072,168 B・digest `sha256:26dbf2aed33fa2275d4aaee7436839bcdb4025f2f20b903c30a28116eafca649`)
判読者: falsifier(非当事者・事後)。判読日 2026-09-06。
前回 CV-9 正本: `docs/notes/fixed_lambda_batch_v1_cv9_reading_v1.md`(裁定 2172 + 2173 追補)。
設計票: `sol/luna_task_1023_r07_fixed_lambda_k64_registration_design.md`・`sol/luna_task_1025..1029`。
Sol 側記帳: `sol/sol_reply_163_onboarding_astra_delta.md` F8.89(共有 TCB 登録)・F8.96–F8.99。

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 9 条(§8)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 9 条)・rank 1514 / gen 8219 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。**

**k = 64 の独立率 = offered 64 / accepted 64 / dependent 0 / skipped 0 = a/k 1.00。**
ただし **§6.2 の指摘 F-k64-2 が本 run の解釈を変える**: a/k は batch サイズの関数ではなく roster 前置長の関数であり、
しかも **前半 32 本は v1 の 32 本と物理行までバイト同一**。よって本 run が新たに与えた独立性の実データは
**roster index 123..177 の 32 本**である(v1 の 32 本の再現 + 32 本の新規)。

同一性の根拠(すべて私の第三実装が生バイトから再導出。P/C の PASS フラグは根拠に使っていない):

- **選定 oracle の完全再現**: `chord-residuals.u8` を `(values − tau·fit) mod 3` で全 54,433 弦ぶん再計算し、
  公刊 `chord-residuals.u8` と**配列一致**。失敗集合 36,274 件・先頭 index 70・先頭 edge 125 を再現し、
  公刊 `failed-indices.u32`(36,274 件)と**全件バイト一致**。基準 5 弦 [2,3,4,6,11] の残差は 5/5 で 0。
  この値は **v1 batch・control-96 step 64 と完全一致**(別 workflow・別実装・第三実装の三点一致)。
- **roster 政策の判別**: 選定 64 件は失敗 index 昇順の先頭 64(70..177)で、**64/64 一致**。
  gap が 1 でない箇所が 33 件あるので「先頭 64 整数を機械的に取った」のではないことをデータが判別。
- **消去構造**: 64 本の normalized 行を生バイトから復元し、
  自 lead で 1 が **64/64**、先行 lead で 0 が **違反 0 件**。
  後続 lead で非零が **1,319 箇所** → **RREF ではなく挿入順前進消去**であることをデータが判別。
  → **階段形+相異なる pivot なので 64 本の一次独立は定理として従う**(producer の INDEPENDENT フラグに依存しない)。
- **λ(F1)**: λ_new ⊥ 新 64 行を **64/64 で 0**、λ_new·t_final = 1、λ_new·t₀ = 1。
  `row_pairings_sha256` = **sha(0x00 × 1514) = 50236812e92be45a…** を手計算一致。
  さらに **λ の 64 個の新 lead 成分を逆順後退代入で独立に再現**(不一致 0)。λ は free 座標 1625 より上で全零。
- **target 恒等式(988.8/988.9)**: t_final に θ_j·n_j を **逆順に足し戻し**て t₀ を再構成 →
  packed sha が親 anchor の target sha **`3bba0da3f619eab5f78e715beabd22d9c7975b36f72d28ee8d7528d9d0f4648a` と一致**。
  θ ≠ 0 が **42/64** なので非空虚。θ の 64 値は producer 申告 `target_scalar` と全一致。
- **鎖**: `predecessor`/`rolling_sha256` が anchor `076c4b9d…` から **64/64 連続**、最終 = `state_head f25595b7…`。
  `global_row_id` = 1450..1513、`local_row_offset` = 0..63、`physical_sha256` = 実ファイル sha が **64/64 一致**。
- **source**: artifact 同梱 `checkout-sources/` **24 件が repo 作業ツリーとバイト全一致(不一致 0)**。
  producer pin 208,805 B / `6626dbcad3400829…`・checker pin 177,544 B / `4ada8490ef931e63…` が
  **workflow / run-receipt / artifact / 作業ツリーの四者一致**。
- **親 pin**: continuation = artifact **9977040548 / 304,642,285 B / `a7ecd56dba33e354…`** = 2154 受理実体 = v1 と同一。

---

## 1. (1) 規約表 diff(v1 → v2)

| 規約 | v1(k=32)の宣言 | v2(k=64)の宣言 | 本 run の実測 | 判別性 |
|---|---|---|---|---|
| `batch_size` | 32 | **64** | selected 64 / processed 64 | 実データで判別 |
| `selection_policy` | `CHORD_FIRST_ROSTER_32_THEN_FIRST_AUX` | **`..._64_...`** | roster 昇順先頭 64(70..177) | **判別**(§4.1) |
| `max_batches` / `refill` | 1 / False | 1 / False(不変) | max_batches 1・refill False | — |
| `partial_policy` | `PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY` | **同**(不変) | `partial=False` | — |
| `producer_limits` / `checker_limits` | 5400s/7168MiB・10800s/7168MiB | **同**(不変) | 実 826.0 s / 1024.7 s | — |
| basis(固定 5 弦) | [2,3,4,6,11] | 同 | 残差 5/5 = 0・fit [1,1,2,1,0] | — |
| Ω 語化 | `sr(0)=0, sr(1)=1, sr(2)=-1; ordered repair x,y,central; mod54 then exact /18` | **同一文字列** | coverage-receipt に同文字列。repair = [−ε_x/6, −ε_y/6, sr(ω)] が **64/64** 成立・ε は 64/64 で 6 の倍数 | **ω=2 が 23/64** |
| g = sr(ω)(central) | 同上 | 同上 | central ≠ 0 が **47/64**、**central 単独 11 件** | **F-cy-1 は再び完全閉鎖** |
| target 減算符号 | `remainder_before - theta * normalized_row` | **同一文字列** | 私の逆順再構成で t₀ 一致(θ≠0 が 42/64) | **非空虚に判別** |
| correction 語因子符号 | `+sr(theta)` | **同一文字列** | 宣言のみ(語の再構成は私の射程外) | 未判別(v1 と同) |
| ρ₂ | `mode=derived, value=1, directly_read=False` | 同 | parents **161 = 97 + 64**・`identity_convention` 4 規則を明示 | **DERIVED のまま** |
| lower-zero | `source_lower_zero = NOT_ASSERTED` / `physical_lower_zero = true` | 同 | separator.json に同値 | **契約どおり** |
| terminal | 3 値 | 同 | `BATCH_COMPLETE_CANDIDATE`(t_final support 30,670) | 他 2 値は canary のみ |
| **selftest 群** | **3 群**(`fixed-selection-full-roster-and-aux` / `dependent-independent-target-signs-and-packed` / `private-prefix-publication-resume-and-isolation`)・実拒否 P 39 / C 19 | **2 群**(`k64-version-registration-and-types` / `k64-full-roster-cutoff-and-restoration`)・実拒否 **P 30+8=38 / C 28+7=35** | 両群 PASS・exit 0 | **§6.1 の重大差分** |
| metadata canary | 16 件 | **16 件**・`metadata_regression_from: d972-r07-fixed-lambda-cycle-batch-v1` | 16/16 拒否 PASS | **継承が cert に明記されている唯一の群** |

→ **凍結宣言と実装・実データの間に齟齬は見つからなかった。**
なお **v1 CV-9 §1.1 の REGISTRATION 引用に `partial_policy` が欠けていた**(実際は v1 にも存在)。
私の v1 報告側の写し落ちであり、実装の変更ではない(【軽微 F-k64-6】= 私の訂正)。

### 1.1 source 差分の実測(v1 → v2)

私が両ファイルを行単位で突き合わせた結果:

- **producer**: 差分は 783 行。**算術領域(v1 L73–2942 ↔ v2 L74–2943)の差は 1 行のみ**
  (`WORKFLOW = ".github/workflows/d972-r07-fixed-lambda-cycle-batch-v1.yml"` → `-v2.yml`)。
  他は先頭定数(`SCHEMA` / `C_FILE` / `BATCH_SIZE,MAX_BATCHES` / `POLICY` / `SELFTEST_ROOT_CREATED` 追加)と
  **L2943 以降の selftest 総入替**。
- **checker**: selftest 前領域の差は **+43 / −15 行**で、内訳は
  (1) 定数(SCHEMA/BATCH_SIZE/POLICY/PRODUCER_FILE/CHECKER_FILE/`CHECKER_WORKFLOW` 新設)
  (2) `check_registration` / `check_acceptance_header` / `check_executable_paths` への切り出し(`batch_size` を 64 に literal 固定)
  (3) **締め方向の追加ゲート 4 本**: `phase_candidate_ordinal ∈ [0,63]`(:1113)・
  `new_batch_row_local_offset ∈ [0,63]`(:1290)・`registered_selected_count ∈ [0,64]`(:1935)・
  **`launch["workflow"] == CHECKER_WORKFLOW`(:1786)**(v1 は正規表現 `[a-z0-9-]+\.yml` 一致だった → literal 一致へ強化)。
  **緩めた箇所は 1 つも無い。**
- `BATCH_SIZE` の実効箇所は producer `failed[:BATCH_SIZE]`(:381)と各種上界のみ。**消去アルゴリズムには入らない**(§6.2)。

### 1.2 交差辺

- producer が `check_*` を import する箇所 **0**(`check_d972` の 11 ヒットは全部ハッシュ pin メタデータ)。
  `importlib` は自系の `d972_r07_complete_oracle_cegar_continuation_v1.py`(`L_SHA` pin 付き)を読むだけ。
- checker が `d972_*` を import / 動的 load する箇所 **0**(`importlib` の使用 0)。
  読むのは `check_d972_r07_complete_oracle_cegar_continuation_v2` のみ。
- **v1 と同じ二系統分離**(消去: `m.physical_reduce` 対 `L.reduce_dense` / 選定: `oracle.solve_five` 対 明示逆行列 / λ: 自前後退代入 対 `L.next_separator`)。

### 1.3 類似度 — 【継続 F-flb-1】共有 TCB 2 本は v2 でも同一・同経路

| 関数 | P 側 file / bytes / sha | C 側 file / bytes / sha | v1 からの変化 |
|---|---|---|---|
| `vectorized_projection_chunk` | `search/d972_r07_actual_grade2_root_scalar_batch_v2.py` 118,315 / `3c93c50c4302…` | `search/check_..._actual_grade2_root_scalar_batch_v2.py` 119,619 / `e0237d100c7f…` | **同一 sha(無変化)** |
| `sparse_adjoint` | `search/d972_r07_targeted_grade2_owner_generated_join_v15.py` 126,565 / `76546bef263a…` | `search/check_..._join_v15.py` 141,770 / `8f718811c518…` | **同一 sha(無変化)** |

F8.89 の shared TCB 登録表の 4 pin と**完全一致**。本 run でも P1 相が候補時間の **72.0 %** を占めるので前者は確実に load-bearing。
**checker 側 docstring `"""Independent bounded implementation of the sparse packed projection."""`
(`search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py:271`)は本 run の `checkout-sources/` にそのまま同梱されている。**
F8.89 の登録は Sol 返信文書側にあり、**run の cert(run-receipt / source-receipt / coverage-receipt)には共有 TCB の記載が無い**。
→ 新規事由ではないが、cert 単独では独立性の限界が読み取れない状態が続いている。

---

## 2. 事前登録と入力 pin

| 検査 | 結果 |
|---|---|
| 起動 commit | `c2a8a6ac`「Run fixed lambda k64 batch v2 [r07-fixed-lambda-cycle-batch-v2-run]」。**workflow(2,314 行)・producer(3,420 行)・checker(2,675 行)がこの 1 commit で初出**(v1 と同じ形)。 |
| 事前登録の凍結 | `REGISTRATION = {batch_size 64, max_batches 1, selection_policy CHORD_FIRST_ROSTER_64_THEN_FIRST_AUX, partial_policy PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY, refill False, producer_limits 5400s/7168MiB, checker_limits 10800s/7168MiB}` が **workflow inline driver に literal で焼かれている**(`.github/workflows/d972-r07-fixed-lambda-cycle-batch-v2.yml:188-192`)。final gate が `owner['registration'] == REGISTRATION`(:1958)を要求。 |
| **selftest の事前登録** | `SELFTEST_NAMES`(2 群名)と **`SELFTEST_REJECTIONS = {'producer-selftest':[30,8],'checker-selftest':[28,7]}` が literal 登録**(:193-195)、final gate が群名列と拒否件数列の**完全一致**を要求(:1388, :1393)。→ 実測 P [30,8] / C [28,7] と一致。**試験件数の後付け調整は不可能**。 |
| 親 pin | `start['rank']==1450 and start['generation']==8155 and start['anchor_completed_steps']==64` を final gate が literal 要求(:1964)。anchor artifact 9977040548 / 304,642,285 B / `a7ecd56dba…` を run-receipt が pin(= 2154 受理実体・v1 と同一)。 |
| 恒真 gate | 見つからなかった。`rank == 1450 + accepted` / `generation == 8155 + accepted` / `processed == dependent + accepted` はすべて **accepted を固定していない**(dependent が出ても gate は通る)。**「64 になるまで通さない」形にはなっていない**ので、独立率 1.00 は gate の強制ではない。 |
| silent cap | 見つからなかった。上界(`selected ∈ [0,64]`・`sequence ∈ [0,387]`・`len(bodies) <= 64`)はすべて `require` で**失敗側に落ちる**。暗黙の切り捨ては無い。 |
| 保存 | `preservation-result.json`: `status PASS`・`errors []`・`missing []`・**flags 22/22 すべて true**・`no_parent_file_renamed_trimmed_or_overwritten true`・`acquired_parent_baselines 15`・`producer_and_checker_outcomes_checked_separately true`。出力 3,322 file / 588 dir。 |
| 実行 source | `checkout-sources/` **24/24 が repo 作業ツリーとバイト全一致**(私が全ファイルを取得して比較)。 |
| 資源 | producer 実 826.027 s(内側 cap 5,400 s の **15.3 %**・外側 6,000 s)・`ru_maxrss` 437,064 KiB(cap 7,168 MiB の **6.0 %**)。checker 実 1,024.656 s(cap 10,800 s の **9.5 %**・外側 11,400 s)・`ru_maxrss` 1,546,708 KiB(**21.1 %**)。`outer_terminated` は両方 False。 |

**oracle の失敗 roster がどの λ に対するものか**: `selection/start.json` の
`selection_lambda_sha256 = 7c0dbe475f9b162f4648f5468ee1098eb86b43dbee247d71f811076559ab88fe`
= 親(rank 1450)の Separator = **v1 と同一の λ**。新 λ(`1f411a4b3697d41e…`)は別 field で保持され、
`new_lambda_oracle = null`(F7 の型分離は守られている)。

---

## 3. 終端受領証(F1)— 全数確認

| 項目 | 宣言値 | 私の独立検算 |
|---|---|---|
| λ_new ⊥ 新 64 行 | (全 0) | **64/64 で 0** |
| λ_new ⊥ 全 1514 行 | `row_pairings_sha256 = 50236812e92be45acd184218dec4872819aeb241bab75c5df8513d1b10e17810`・`rows 1514` | **sha(0x00 × 1514) と一致**。旧 1450 行は本 ZIP に無いので直接検算不能だが、checker は `ThinAnchor.measure_selection()`(`check_…_v2.py:756-771`)で旧 1450 行を全部読み、**三角性・λ_anchor ⊥ 全行・両 target との pairing = 1・target が全 lead で 0** を直接測り、`finish_arithmetic`(`:358-378`)で 1514 行すべてに dot している |
| λ_new · t₀ | `lambda_parent_remainder = 1` | **1**(再構成した t₀ に対して) |
| λ_new · t_final | `lambda_new_remainder = 1` | **1** |
| λ_pivots | 0 | 一致 |
| anchor / final pairing rows | 1450 / 1514 | 一致 |
| λ の新 lead 成分 | (公刊 λ) | **逆順後退代入で 64/64 完全再現**(不一致 0)。うち非零は 40 |
| free 座標 | — | **1625**(t_final の最初の非零・値 1・λ[1625]=1)。**λ は 1625 より上で全零** |
| λ の character 別 support | `[1002, 0, 0, 0]`・trit `[11094, 502, 500]` | **base-3 4-trit/byte で復号して完全一致** |
| head 連鎖 | — | anchor `076c4b9d…` → 64 段連続 → `f25595b78b0ddbee…` = `state_head`。**64/64** |

**注(構造的)**: `row_pairings_sha256` は零ベクトルの sha であり、**実質的には行数しか運ばない受領証**である。
実効的な内容は `lambda_pivots == 0` と両 remainder = 1、および checker 側 `require(not any(pairings) and ...)` の方にある。
これは v1 から変わらない仕様上の性質であって、本 run の欠陥ではない。

---

## 4. 実データによる規約判別(非空虚性)

### 4.1 選定 64 本の実体

roster index: **70, 72, 73, 77, 79, 80, 81, 82, 83, 84, 85, 87, 88, 89, 90, 91, 94, 98, 99, 101, 103, 105, 106, 107, 109, 111, 113, 114, 116, 117, 118, 119**(← v1 と同一の 32 本)
**+ 123, 124, 125, 127, 131, 132, 134, 136, 138, 139, 140, 141, 142, 143, 145, 146, 147, 148, 149, 152, 157, 158, 159, 160, 162, 163, 169, 170, 171, 172, 174, 177**(新規 32 本)

- span = index 70..177(108)。v1 は 70..119(50)。
- gap ≠ 1 が **33 件**あるので「先頭 64 整数を機械的に取った」のではないことをデータが判別。
- `chords_checked = 54433`(全宇宙走査)・`auxiliary_tests = 2`・`aux_values = [0,0]`(両 aux を評価して両方零 → **aux 枝は本番未発火**)。
- `terminal(selection) = VIOLATION_CANDIDATE`。

### 4.2 v1 との突き合わせ(Task 1023 の要求どおり二つを区別する)

私が v1 artifact 9980697123 を取得して直接比較した:

- **(a) 同じ選定条件か** → **YES**。同一 λ・同一 oracle 値(36,274 / index 70 / edge 125)・先頭 32 index が完全一致。
- **(b) 実 payload が一致したか** → **文書としては不一致・数学的内容は一致**。
  witness 記録で **v1↔v2 が全 32 本で一致する field** =
  `basis_chords, basis_coefficients, coordinate, cycles, edge, eta, failed_chord, kind, materialization, ordinal, roster_index, scalar, tau`。
  **差が出る field** = `schema, owner_sha256, selection_start_sha256, source_sha256, start_sha256, sha256, selection_policy` のみ(= 版の束縛)。
  producer 候補記録も同様で、**`lead / sigma / target_scalar / selection_scalar / omega / epsilon / repair_exponents / alpha_support / raw_slp_letters / source_homogeneous_scalar / rank / generation` が 32/32 一致**、
  差は `witness_sha256 / row_manifest_sha256 / candidate_manifest_sha256` の 3 印のみ。
- **(c) 物理行**: 抽出した ordinal 0,1,15,16,30,31 の `reduction/physical-normalized.bin` が **v1 と 6/6 バイト同一**。
  → **v2 の最初の 32 段は v1 の 32 段と同じ span を作っている**(rolling head だけが版束縛で異なる)。

### 4.3 ω / central 指数(64 本)

| 量 | v2 全 64 | うち前半 32(= v1) | 後半 32(新規) |
|---|---|---|---|
| ω = 0 / 1 / 2 | **17 / 24 / 23** | 9 / 9 / 14 | 8 / 15 / 9 |
| repair = [−ε_x/6, −ε_y/6, sr(ω)] | **64/64 成立** | 32/32 | 32/32 |
| ε ≡ 0 (mod 6) | 64/64 | — | — |
| repair_x≠0 / repair_y≠0 / central≠0 | **40 / 38 / 47** | 17 / 18 / 23 | 23 / 20 / 24 |
| 三因子すべて ≠ 0 | 23 | 9 | 14 |
| **central 単独(x=y=0, cen≠0)** | **11** | 6 | 5 |
| 修理なし [0,0,0] | 5 | 3 | 2 |
| central 指数の値 | +1 が 24・**−1 が 23**・0 が 17 | — | — |

→ **`sr(2) = −1` の literal 採用は 23 件で判別されている**(裁定 2173 のとおり、これは
**receipt/wire 上の signed literal 指数の採用**であって −1 対 +2 を登録 Q2 source / 物理行の値で識別したという主張ではない)。

### 4.4 σ / θ / lead

- **σ**: 1 が **31**、2 が **33**(前半 32 は v1 と同じ 17:15、後半 32 は 14:18)。
- **θ(`target.scalar`)**: 0 が **22**、1 が **23**、2 が **19**(前半 32 は v1 と同じ 12/9/11)。
  **θ≠0 の 42 件が (988.8) の符号規約を判別**(逆符号なら t₀ 再構成が壊れる)。
- **`selection_scalar`**(別 field・混ぜない): 1 が 29・2 が 35。前半 32 は v1 と同じ 12:20。
- **lead**: **1562..1624 の連続 63 個 + 1627**。**1625 と 1626 は飛ばされている**。
  付与順は非単調(降順ステップ 15 回)。
- **t_final**: support **30,670 / 48,384**、最初の非零(free 座標)= **1625**、値 1、λ[1625] = 1。

### 4.5 情報性の内訳

- λ_new の character 別 support = **[1002, 0, 0, 0]** → **character 0 だけが情報的**(限定継続)。
  λ の非零 1,002 のうち **961 が座標 < 1562**(親由来の帯)。
- λ_new は座標 ≥ 1562 の範囲で `{新 64 lead} ∪ {1625}` の外に非零を持たない(1626・1627 は 0)。
- κ: `degree0/degree1` とも **tag 0 のみ非零**(total 5,387)、`kappa aux_values` は 8 個すべて 0。
- score: `by_tag = [40203, 23052, 23052, 0, 0, 0]` → **tag 3〜5 は零**。
- q: character 0 のみ support 2,880。`p1_equation_residual_support = 0`。
- alpha support **5,241〜5,448 / 8,059** → P1 減算は全候補で活性(非空虚)。

### 4.6 preserved-input 全数照合

15 role・親 baseline 全件の before/after が `all_parent_files_and_directories_unchanged: true`、
code before/after が `all_code_and_raw_unchanged: true`、acceptance 不変。
P と C が別々に同じ `input_preservation` dict を出し(私が両 result を突合して 9 field 全一致を確認)、
workflow が両者一致を要求。`flags` 22/22 true・`errors []`・`missing []`。

---

## 5. 【独立節・重点】k = 64 の独立率と実効前進率

### 5.1 独立率(一次データ)

| 量 | v1(k=32) | **v2(k=64)** |
|---|---:|---:|
| offered(= selected_count) | 32 | **64** |
| **INDEPENDENT** | 32 | **64** |
| **DEPENDENT** | 0 | **0** |
| SKIPPED_AFTER_LINEAR | 0 | **0**(`skipped_after_linear = []`) |
| **独立率 a/k** | **1.00** | **1.00** |
| rank | 1450 → 1482 | **1450 → 1514** |
| generation | 8155 → 8187 | **8155 → 8219** |
| terminal | BATCH_COMPLETE_CANDIDATE | 同 |

**k = 64 で従属は出なかった。Task 988 F4 の反例(相異なる違反が相互独立とは限らない)は、
本 run では実現していない。** ただし §6.2 の指摘により、この観測の意味は
「λ_1450 の失敗 roster **先頭 64 本**が互いに独立」であって「batch サイズ 64 でも独立が保たれた」ではない。
消化率は依然 64 / 36,274 = **0.18 %**。

### 5.2 v1 との比較表(実効前進率)

| | v1(k=32) | **v2(k=64)** | 比 |
|---|---:|---:|---:|
| 追加行 | 32 | **64** | 2.00 |
| oracle 回数 | 1 | **1** | — |
| producer 実秒(自己申告) | 432.437 | **825.483** | 1.909 |
| producer 実秒(harness 外形) | (n/a) | **826.027** | — |
| checker 実秒(自己申告) | 551.331 | **1023.682** | 1.857 |
| checker 実秒(harness 外形) | (n/a) | **1024.656** | — |
| P + C | 983.768 | **1849.165** | 1.880 |
| **1 行あたり P+C(run 単位)** | **30.743** | **28.893** | **1.064 倍速** |
| **限界単価 P+C(v1→v2 の 2 点差分)** | — | **27.044** | 逐次 42.36 に対し **1.566 倍速** |
| 限界単価 P / C(内訳) | — | **12.283 / 14.761** | — |
| 候補六相 合計 | 351.018 | **707.981** | 2.017 |
| 候補あたり | 10.969 | **11.062** | 1.008 |
| selection(oracle 1 回) | 11.880 | **11.963** | 1.007 |
| final separator | 0.869 | **0.893** | 1.028 |
| **計測外の固定費** | **68.670** | **104.647** | **1.524** |
| producer cap 使用率 | 8.0 % | **15.3 %** | — |
| checker cap 使用率 | 5.1 % | **9.5 %** | — |
| checker / 候補 | 17.229 | **15.995** | 0.928 |

### 5.3 producer の相分解(私が 384 個の telemetry.json を全取得して合計)

| 相 | 64 候補の合計 | 1 候補あたり | 候補時間比 | v1 の比 |
|---|---:|---:|---:|---:|
| raw | 6.917 | 0.1081 | 1.0 % | 0.9 % |
| source | 17.982 | 0.2810 | 2.5 % | 2.3 % |
| primal | 153.368 | 2.3964 | **21.7 %** | 21.8 % |
| **p1(corrected_source)** | **509.718** | **7.9643** | **72.0 %** | 72.2 % |
| B(四 character) | 4.791 | 0.0749 | 0.7 % | 0.7 % |
| reduction(実消去) | 15.206 | 0.2376 | 2.1 % | 2.1 % |
| **候補 計** | **707.981** | **11.0622** | 100 % | — |
| selection(section 11.639 + cochain 0.092 + tree 0.232) | 11.963(1 回) | — | — | — |
| final separator | 0.893 | — | — | — |
| 計測外の固定費 | **104.647** | — | — | — |

- **primal + p1 = 663.086 s = 候補六相 707.981 s の 93.66 % = producer 全 825.483 s の 80.33 %。**
  (裁定 2173 の分母規律に従い、候補相内比率と process 全体比率を分けて書く。v1 は 94.01 % / 76.31 %。)
- **律速は v1 と同じく P1 補正相**。比率は k を倍にしてもほぼ不変(72.2 % → 72.0 %)。

### 5.4 【所見 F-k64-5】F-flb-8 の精密化 — 語長は効くが効き目が小さい

v1 で私は「コストは語長でなく固定次元の配列作業で決まる」と書いた。**結論は維持されるが、表現は精密化が要る。**
64 点の回帰(相ごと):

| 相 | corr(語長, 秒) | 傾き(s / 1,000 letters) | 候補時間の占有 |
|---|---:|---:|---:|
| raw | **+0.997** | 0.0045 | 1.0 % |
| source | **+1.000** | 0.0378 | 2.5 % |
| primal | +0.099 | 0.0007 | 21.7 % |
| p1 | **−0.060** | −0.0011 | 72.0 % |
| B | +0.200 | 0.0001 | 0.7 % |
| reduction | +0.253 | 0.0005 | 2.1 % |
| **合計** | **+0.885** | **0.0424** | 100 % |

- 全体の相関は 0.885 と高いが、**それは raw + source(合計 3.5 %)が語長にほぼ完全比例している**ことに由来する。
- **支配的な p1 + primal(93.7 %)は語長と無相関**(−0.06 / +0.10)。
- フィット: **候補秒 ≈ 10.794 + 0.0424 × (語長/1000)**。
  実測でも 34 letters → 10.751 s、12,354 letters → 11.398 s(語長 363 倍に対し時間差 **0.65 s = 6.0 %**)。
- → 正しい言い方は「**語長は raw/source 相を厳密に支配するが、その二相は費用の 3.5 % にすぎない**」。
  「語長は無関係」は言い過ぎだった(私の v1 表現の訂正)。

### 5.5 【要修正 F-k64-4】「固定費」は固定ではない — 外挿の下方修正

計測外の固定費(入力受入・親全 file hash・出力 inventory 等)は **68.670 s(k=32)→ 104.647 s(k=64)**。
2 点フィットで **fixed(k) ≈ 32.7 + 1.124 k**。出力 ZIP が 94.7 MB → 187.1 MB と k 比例で増えているので、
「出力の inventory / hash が k に比例する」という説明と整合する(2 点なので**傾向であって法則ではない**)。

これを織り込むと producer cap 5,400 s から取れる k は:

| 前提 | v1 の見積り | **本 run の実測を入れた見積り** |
|---|---:|---:|
| 1 run の producer cap から取れる k | 484 | **≈ 436**(rank 依存を無視) |
| 1 run の checker cap から取れる k | 627 | **≈ 726**(checker 固定費 ≈ 79 s・限界 14.761 s) |
| **律速** | producer | **producer(変わらず)** |
| 残り行数(48,384 − 1,514) | — | **46,870** |
| 必要 run 数 | 98 | **≈ 107** |
| 純 P+C(限界単価 27.044 s/行) | 16.7 日 | **≈ 14.7 日**(rank 依存 1.7 倍を織り込むと ≈ 25 日) |

**桁は依然として動いていない。** これは線形外挿であって予言ではない。

### 5.6 rank 依存(reduction 相)

reduction 相の秒は候補 ordinal と corr 0.662・傾き **0.000248 s/行**(先頭 16 平均 0.2324 → 末尾 16 平均 0.2445)。
64 行という短い区間の推定なので雑だが、比例モデル(0.2324 × rank/1450 → 傾き 0.000160)より **1.55 倍急**。
rank 48,384 での reduction 相は比例モデルで ≈ 7.8 s/候補、実測傾き外挿で ≈ 11.9 s/候補。
**この差はそのまま §5.5 の外挿の不確かさとして残る。**

### 5.7 【軽微 F-k64-3】空き座標の債務は増えた — v1 の F-flb-5 は反証された

| | anchor(rank 1450) | v1 後(rank 1482) | **v2 後(rank 1514)** |
|---|---:|---:|---:|
| lead の最大 | 1561 | 1593 | **1627** |
| frontier(= max lead + 1) | 1562 | 1594 | **1628** |
| 空き座標(frontier − rank) | 112 | 112 | **114** |

v1 で私は「この batch は空き座標を 1 つも増やしていない」と書き、「一点観測なので傾向とは言わない」と注記した。
**本 run はその一点観測を反証した**: 後半 32 段で **lead 1625・1626 が飛ばされ**、債務が +2 になった。
1625 は最終 Separator の free 座標として使われ、**1626 はどちらでもない**(lead でも free でもない)。
→ **「lead frontier は rank と 1:1 で進む」という外挿は成立しない。**

### 5.8 roster 消化は依然として比較できない(正直な申告)

`new_lambda_oracle = null` なので、**rank 1514 の λ* に対する失敗弦数・先頭 index は未計算**。
Task 988 F10 のとおり旧 λ で零だった弦が新 λ で非零になり得るので、
「先頭 index が 177 まで進んだ」とは言えない。**比較可能な前進量は rank だけ。**

---

## 6. 新規発見

### 6.1 【要修正 F-k64-1】v2 の selftest は DEPENDENT 枝・target 符号・publication 枝の陽陰試験を持たない

事実(すべて一次データ):

- v1 の 3 群のうち、**`dependent-independent-target-signs-and-packed` と
  `private-prefix-publication-resume-and-isolation` が v2 では存在しない。**
  producer からは `canary_selection` / `canary_physical_fixture` / `canary_reduction_store` / **`canary_reduction`** /
  `canary_invocation_history` / `canary_diagnostics` / `canary_publication` が削除され、
  `selftest_root_path` / `k64_reject` / `k64_registration_canary` / `k64_selection_canary` に置き換わった。
  checker からは `selector_canary` / **`reduction_canary`** / `publication_canary` が削除され、
  `k64_registration_canary` / `k64_roster_canary` に置き換わった。
- v1 で DEPENDENT を張っていたのは producer `canary_reduction`(v1 `:3065` = 同一ベクトル再投入で DEPENDENT、
  `:3070` = **Task 988 F4 第二反例**そのもの)と checker `reduction_canary` の θ=1/θ=2 両符号だった。
  **v2 の producer で `DEPENDENT` が現れるのは実装本体(`:477, :509, :1735, :1762`)だけで、selftest には 1 箇所も無い。**
- 本番でも `dependent_candidates = 0`。→ **本 run では DEPENDENT 枝が合成でも実データでも一度も通っていない。**
  同様に `aux_values = [0,0]` で aux 選択枝も未発火(v1 と同じ)。

緩和材料(私が確認した):

- **算術本体は v1 と同一コード**(§1.1: producer の算術領域は `WORKFLOW` 文字列 1 行を除きバイト同一、
  checker の selftest 前領域は締め方向の追加のみ)。したがって v1 run で通った canary の結論は
  同一バイトのコードに対するものである。
- **本 run の独立性主張自体は canary に依存していない**。私が階段形(自 lead=1・先行 lead=0)を
  64/64 で実測したので、64 行の一次独立は**定理として**従う。誤って INDEPENDENT と判定された従属行が
  混じっていれば normalized 行が零になり自 lead = 1 が破れるので、**silent な誤りは通らない**。
  残るリスクは soundness ではなく **liveness**(本物の DEPENDENT が来たときに正しく記録して続行できるか)。

問題(ここが指摘):

- **その継承が cert に一切記録されていない。** v2 の cert で v1 由来を明記しているのは
  metadata canary だけ(`metadata-selftest.json`: `"metadata_regression_from":"d972-r07-fixed-lambda-cycle-batch-v1"`・
  run-receipt: `metadata_regression_base` / `metadata_regression_cases_registered: 16`)。
  **数学 selftest 側には同種の field が無く、`old_success_suites: 0` と書いてあるだけ**なので、
  cert だけを読む第三者には「DEPENDENT 枝は一度も試験されていない」と読める。
- 提案(安価): metadata 群にすでにある型をそのまま流用し、
  `arithmetic_selftest_inherited_from: "d972-r07-fixed-lambda-cycle-batch-v1"` +
  **不変を主張する算術領域の行範囲と sha256**(私の測り方: producer v1 L73–2942 ↔ v2 L74–2943、差は `WORKFLOW` 1 行)を
  受領証に載せる。これなら再走コスト 0 で「継承の根拠」が機械照合可能になる。
- **「何にでも当たる試験」ではない**ことは確認した(分離条件は満たしている)。
  v2 の 2 群は版差分にきちんと当たっている: P `old-32-witness-cutoff` / C `old-first32-cutoff`(32 本切り出しを拒否)、
  `batch-32/33/63/65/128` の全拒否、`old-policy` / `old-acceptance` / `old-owner-schema` / `old-invocation-k32` の拒否、
  かつ **陽性 fixture(`m32/m33/m63/m64/m65`・`failed32/33/63/64/65`・`auxiliary-only`・`second-auxiliary`・`complete-zero`)を併走**している。
  ダミー検査ではない。**落ちているのは「変えていない部分」の被覆だけ**である。

### 6.2 【要修正 F-k64-2】a/k は batch サイズの関数ではない(実験の読み方の訂正)

- `BATCH_SIZE` が算術に効く箇所は producer の **`for raw_index in failed[:BATCH_SIZE]`(`:381`)ただ 1 つ**。
  残りはすべて上界・型・受領証の literal。
- 消去は**候補ごとの逐次**である(実データ: candidate i の `rank_before = 1450 + i`・`rank_after = 1451 + i` が 64/64 成立)。
  各候補は「その時点までの span」に対して簡約される。**同時に 64 本を扱う処理は存在しない。**
- ⇒ **a/k は「roster 前置の何本目まで独立が続くか」であって、batch 化の副作用ではない。**
  k=64 の測定結果は「k=32 を 2 回続けた」場合と同じ値になる(実際、§4.2 で前半 32 本が v1 と物理行までバイト同一であることを確認した)。
- ⇒ 設計票の「k を上げたときの独立率 a/k」という言い方は誤導。正しくは「**roster 前置長 n における累積独立本数 a(n)**」。
  今 a(32) = 32、**a(64) = 64**。次に測るべきは a(128) だが、それは「k=128 の batch」でも
  「k=64 の続き」でも**同じ数**になる。**k を上げる価値は費用(oracle 1 回の償却・固定費の償却)の側にしか無い。**
- ⇒ Task 988 F4 の反例は依然として排除されていない。64 / 36,274 = 0.18 % しか見ていない。
  なお k を上げると**別種のリスク**が入る: 選定は λ_1450 に対して 1 回だけ行われるので、
  k が大きいほど「古い λ で選んだ弦」を深く消化することになる(F10 の非単調性が効く範囲が広がる)。
  **これは独立率とは別の軸**であり、今回のデータでは測られていない。

### 6.3 【解消 F-flb-3】diagnostics artifact の同一バイト数は仕様であることが確定

`9983058782`(candidate)と `9983062604`(diagnostics)がともに **187,072,168 B**、digest だけ違う
(`26dbf2ae…` / `0fdc4cd7…`)。**原因は workflow が両 upload step に同じ path
`${{ runner.temp }}/fixed-lambda-batch-v2/` を渡していること**(`:2299-2311`)で、
run-receipt が **`candidate_and_diagnostics_upload_the_same_envelope_root: True`** と明示宣言している。
→ **欠陥ではない**。v1 の F-flb-3(および F-c96-3)は「仕様として宣言済み」で閉じてよい。
ops 上の所見としてのみ: diagnostics は情報量ゼロの重複であり 187 MB を二重に保管している。

### 6.4 【軽微 F-k64-7】時間値の非独立性は v1 より改善したが完全ではない

- checker は producer の `elapsed_seconds` をそのまま採用する(`check_…_v2.py:1867`:
  `"elapsed_seconds": actual["elapsed_seconds"]`、検査は `finite_measurement` の有限性のみ)。**F-flb-4 は継続。**
- ただし **harness(workflow inline driver)は子プロセスを自前で計測**しており
  (`:1335` `'elapsed_seconds': time.monotonic() - begin`、`:1362-1363` で `0 <= elapsed <= outer + 15` を要求)、
  producer 826.027 s / checker 1024.656 s という**第三の測定値が cert に載っている**。
  自己申告(825.483 / 1023.682)との差は 0.54 / 0.97 s。
  → **§5 の run 単位の秒は harness 側の独立計測で裏が取れている。**
- **相ごとの秒(§5.3)は producer の自己計測**で、型と有限性しか検査されない(`:1773-1777`)。
  ただし自己計測の総和 720.837 s は harness 総計 826.027 s を超えておらず、上から押さえられている。
- **checker には段別 timestamp が無い**(`checker-stderr.log` 8,273 行に時刻なし)。
  → checker の候補あたり限界単価は §5.2 の 2 点差分(14.761 s)としてしか出せない。

### 6.5 【所見】締め方向の変更のみ・λ の型分離も維持

- checker の `launch["workflow"]` 検査が **正規表現一致 → literal 一致**に強化(v1 `:1759` → v2 `:1786`)。
- `phase_candidate_ordinal ∈ [0,63]`・`new_batch_row_local_offset ∈ [0,63]`・`registered_selected_count ∈ [0,64]` を追加。
- `check_registration` が `batch_size` を **`integer(..., 64, 64)`** で literal 固定。
- `selection_lambda_sha256`(旧 `7c0dbe47…`)と `lambda_sha256`(新 `1f411a4b…`)は別 field。
  `progress/HEAD` の `current_lambda_sha256 is None` を final gate が要求(`:2019`)。**成長中の span は Separator を export しない**(F7 どおり)。

---

## 7. CV-9 検問の判定に直結する項目のまとめ

| 検問項目 | 判定 |
|---|---|
| 両実装は同一の数学対象を計算しているか | **同一**。親 anchor・選定 λ・oracle 値(36,274 / 70 / 125)・roster 政策・Ω 規約文字列・target 減算符号・ρ₂ 規約が一致し、実データで判別されている |
| 規約宣言と実物の乖離(stub 型)はあるか | **見つからなかった**。凍結宣言(REGISTRATION・SELFTEST_NAMES・SELFTEST_REJECTIONS)と実測が literal 一致 |
| 分離条件(ダミー検査でないこと) | **満たしている**。版差分に当たる陰性 fixture(`old-32-witness-cutoff` 等)と陽性 fixture が併走。ただし §6.1 のとおり**不変部分の被覆はゼロ** |
| 空虚性(仮定を満たす事例が実在するか) | 選定/Ω/central/σ/θ/P1 はすべて非空虚に判別。**DEPENDENT 枝と aux 枝だけが空虚**(本番 0 回・v2 selftest にも無い) |
| 「見つからなかった」を非存在と読んでいるか | 読んでいない。`new_lambda_oracle = null`・`grade2 NOT_DECIDED`・`positive_readout = NOT_APPLICABLE`・`workshop_CV9 = PENDING` が明示 |
| 個数一致だけで済ませていないか | 済ませていない。rank 増分は階段形の実測で裏付けられ、target 恒等式は逆順再構成で sha 一致 |
| UNKNOWN の置き場 | ある(`NOT_DECIDED` / `NOT_ASSERTED` / `null` / `DERIVED`) |
| 撤退条件の数値 cap | 明記(P 5,400/6,000 s・C 10,800/11,400 s・7,168 MiB)。使用率 15.3 % / 9.5 %・超過時の行き先は partial 経路(本 run では未使用) |

---

## 8. 限定条項(9 条)

1. **射程 = rank 1450 → 1514 の 1 batch のみ**。rank 1514 の λ* に対する oracle は**未計算**(`new_lambda_oracle = null`)。
   新 λ での失敗弦数・先頭 index は不明。NONMEMBER 主張ではない。
2. **a/k = 1.00 は roster 前置 64 本の観測**(k という batch パラメータの性質ではない・§6.2)。
   うち前半 32 本は v1 の再現であり、**新規情報は roster index 123..177 の 32 本**。
   36,274 件中 64 件 = 0.18 %。**Task 988 F4 の反例は排除されていない。**
3. **DEPENDENT 枝・aux 枝は本番未発火、かつ v2 の selftest にも無い**(v1 からの後退・§6.1)。
   継承の根拠は「算術領域が v1 と 1 行を除きバイト同一」という私の source 実測にあり、**cert には記録されていない**。
4. **情報的なのは character 0 だけ**(λ support [1002,0,0,0])。lead 帯 [1562,1627]・free 座標 1625。
5. **aux は [0,0] で未発火**、κ は tag 0 のみ、score は tag 3〜5 零、q は character 0 のみ。
6. **算術 TCB は共有カーネル 2 本を含む**(`vectorized_projection_chunk` / `sparse_adjoint`・P/C で実行本文一致)。
   v1 から sha 無変化・P1 経路(候補時間の 72.0 %)で load-bearing。第三独立性はこの 2 本に及ばない。
   `sparse_adjoint` の本 run 実呼出行は特定していない(v1 と同じ限界)。
7. **harness TCB は新規**(workflow 2,314 行 + inline driver 単著)。私は harness 出力(coverage-receipt)を根拠に使わず、
   §3〜§5 を生バイトから第三実装で再導出した。
8. **旧 1450 行の実バイトは私自身は未取得**。λ_new ⊥ 旧行 と ρ₂ の旧行部分は checker の `ThinAnchor` 再現に依存する。
   **ρ₂ は依然 DERIVED**(`mode=derived, value=1, original_rho2_directly_read=False`)。
9. **相ごとの秒は producer の自己計測**(型と有限性のみ検査)。run 単位の秒は harness の独立計測で裏が取れているが、
   **checker の段別 timestamp は無い**ため checker の限界単価は 2 点差分でしか出せない。

---

## 9. CV-9 裁定案・工房格付け案(一行)

**CV-9 = 同一対象(SAME OBJECT)・限定 9 条 → 工房格付け案: checker PASS / cross-checked(限定 9 条)・
rank 1514 / gen 8219 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。
batch v1 の rank 1482 状態および control-96 の rank 1482 状態とは行の由来が異なる別状態であり、合算しない。**

**司令塔への一行**: k=64 は **64/64 独立・P+C 1,849 s・限界単価 27.0 s/行**で、
2164 の checker 構造的天井が消えたことを再確認したが、
**(a) 独立率は batch サイズの関数ではなく roster 前置長の関数であり、今回の新規情報は 32 行分しかない**、
**(b) 「固定費」が k に比例して増えるため producer cap から取れる k は 484 → ≈436 に下方修正**、
**(c) v2 の selftest から 3 群のうち 2 群(DEPENDENT/target 符号/publication)が落ち、
その継承が cert に記録されていない**、の 3 点が新しい。
k=128 に進む前に (c) の受領証 field を 1 つ足す(再走コスト 0)のが安価で効く。

---

## 10. 判読者の限界(正直な申告)

- 旧 1450 行の実バイトを取得していないので、λ_new ⊥ 旧行 と ρ₂ 恒等式の旧行部分は checker の再現に依存している。
- 語(Ω / P1 / literal)の再構成は私の射程外。ε/ω/repair 指数は **producer の申告と checker の式計算の突合**として検証した。
  `correction_word_factor_sign = +sr(theta)` は宣言のみで未判別(v1 と同じ)。
- v1↔v2 の物理行一致は **ordinal 0,1,15,16,30,31 の 6 本の抽出比較**であり、32 本全数ではない
  (ただし producer 記録の `lead/sigma/target_scalar/omega/epsilon/repair/alpha_support/slp_letters` は 32/32 一致を確認した)。
- `sparse_adjoint` が本 run の実行経路で呼ばれた行は特定していない(両側で import されていることまで)。
- §5.5・§5.6 の外挿は **2 点フィット**であり、法則ではない。
- **この観点では仕様の齟齬(別対象)を見つけられなかった** — 保証ではない。

---

## 付録: 主要 pin(すべて私が実バイトから再計算 or API から取得)

| 対象 | 値 |
|---|---|
| run / head | 34011731149/1 / `c2a8a6acd60c0cd859edd2e262cfce074b3acaf1` |
| candidate artifact | 9983058782 / 187,072,168 B / `26dbf2aed33fa2275d4aaee7436839bcdb4025f2f20b903c30a28116eafca649` |
| diagnostics artifact | 9983062604 / 187,072,168 B / `0fdc4cd71988b4466bbec7003b134a8ee492913c806440007dd905eea6dbbe4a` |
| 親 continuation | 9977040548 / 304,642,285 B / `a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792` |
| producer source | `search/d972_r07_fixed_lambda_cycle_batch_v2.py` 208,805 B / `6626dbcad3400829baa0ac9f6ad00527ab1de002d253d41f39575f241f70d74e` |
| checker source | `search/check_d972_r07_fixed_lambda_cycle_batch_v2.py` 177,544 B / `4ada8490ef931e639159b2c3522510b6fc2da82551daa9a7aa3f1a1970d0ca90` |
| 親 target(t₀) | `3bba0da3f619eab5f78e715beabd22d9c7975b36f72d28ee8d7528d9d0f4648a`(**私の逆順再構成が一致**) |
| 選定 λ(旧) | `7c0dbe475f9b162f4648f5468ee1098eb86b43dbee247d71f811076559ab88fe` |
| 新 λ | `1f411a4b3697d41e7071feb837c93e215bf4941ec090cae28252c51f5eb0276f`(**私が lambda.bin を hash して一致**) |
| 最終 target | `a9db05bc4f7de68ac0fa16b5eecdc13f0b140c4420a64a8f49f33670453db458`(同上) |
| row_pairings | `50236812e92be45acd184218dec4872819aeb241bab75c5df8513d1b10e17810` = **sha(0x00 × 1514)** |
| state_head | `f25595b78b0ddbeeb86f4cea3ca9e85e0bd7b5b9c312744d959387ff5fb66a2a`(anchor `076c4b9d…` から 64 段連続) |
| producer result | `producer-stdout.json` 105,893 B / `e6de70cb72affb51a8127b125d3b017408198782893f6274f15ab50bbe6d1527` |
| checker result | `checker-stdout.json` = `checker-result.json` 7,375 B / `26b3364d58a07e73a6387d52f7da834e8a9b4a58f37306da5c80d928e7afced7` |
| run-receipt | 31,694 B / `d742d58b0c2fc66a…`(status PASS・`workshop_CV9 = PENDING`) |

---

報告書 sha256(この行を追記する前の全体): 875db0c92bfafe71660704a0c4d76cb4de5ebd7c17ceff584b36f61bc54c7d83 / 先頭 16 桁 = **875db0c92bfafe71**
