# 増分 CV-9 判読 — R07 fixed-lambda cycle batch **v3 / k = 128**(rank 1450 → 1578)

対象 run: **34023589045/1**(success・event=push・head `794c5e9f883cb5ff21b2ee087c1d4baa84ac6760`・09:04:03Z→10:08:05Z)
候補 artifact **9987222571**(369,233,546 B・digest `sha256:781c9f467bd38305c524a0a2bf5b361f45e75bc4234d9cf6e891e01175db9e2e`)
判読者: falsifier(非当事者・事後)。判読日 2026-09-06。
前回 CV-9 正本: `docs/notes/fixed_lambda_batch_v2_cv9_reading_v1.md`(裁定 2176 + 2177 追補)。

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 8 条(§8)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 8 条)・rank 1578 / gen 8283 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。v1 の rank 1482・v2 の rank 1514・control-96 の 1482 とは行の由来が異なる別状態であり、合算しない。**

**a(128) = 128。** offered 128 / accepted 128 / dependent 0 / skipped 0。
ただし §5.1 のとおり、**本 run の新規情報は roster index 179..281 の 64 本だけ**である(前半 64 本は v2 の 64 本と**物理行までバイト同一**であることを私が両 artifact から実バイトで確認した)。

**v2 判読の 2 大指摘のうち 1 つは閉じ、1 つは残った**:

- **【解消 F-flb-1 / F-k64-1(cert 記録面)】** v3 は workflow に **static audit registry**(60 記述子・3 版 × 20 領域)と **shared TCB 受領証**を新設し、`arithmetic_selftest_inherited_from` を run-receipt に載せた。私はこの 60 記述子すべてを repo の実バイトから独立に再計算し、**不一致 0**。私が v2 で提案した受領証 field は、提案より強い形(全 source を gap/overlap なしで分割し、9 不変領域の三版バイト同一を run 中に実測)で実装されている。
- **【継続 F-k64-1(試験の実体面)】** producer/checker とも selftest は依然 **2 群**で、**DEPENDENT 枝の陽性/陰性試験は合成でも本番でも一度も通っていない**(`dependent_candidates = 0`・selftest に 1 件も無い)。registry 自身が `"Historical DEPENDENT/target/publication suite PASS is a reference, not a current-run pass."` と明記しており、**正直だが穴は塞がっていない**(risk は soundness ではなく liveness、§6.1)。

同一性の根拠(すべて私の第三実装が生バイトから再導出。P/C の PASS フラグは根拠に使っていない):

- **選定 oracle の完全再現**: `chord-residuals.u8` を `(values − tau·fit) mod 3` で全 54,433 弦ぶん再計算し公刊配列と**完全一致**。失敗 **36,274** 件・先頭 index **70**・先頭 edge **125** を再現し `failed-indices.u32` と**全件バイト一致**。基準 5 弦 [2,3,4,6,11] の残差 5/5 = 0・fit `[1,1,2,1,0]`。**v1・v2・control-96 と四点一致。**
- **roster 政策の判別**: 選定 128 件 = 失敗 index 昇順の先頭 128(70..281)で 128/128 一致。gap ≠ 1 が **54 件**あるので「先頭 128 整数を機械的に取った」のではないことをデータが判別。
- **消去構造**: 128 本の normalized 行を生バイトから復元し、自 lead で 1 が **128/128**、先行 lead で 0 が**違反 0 件**、後続 lead で非零が **5,319 箇所** → **RREF ではなく挿入順前進消去**であることをデータが判別。→ **階段形+相異なる pivot 128 個なので 128 本の一次独立は定理として従う**(producer の INDEPENDENT フラグに依存しない)。
- **λ(F1)**: λ_new ⊥ 新 128 行が **128/128 で 0**、λ_new·t_final = 1、λ_new·t₀ = 1、`row_pairings_sha256 = 71f45b82ab075986…` = **sha(0x00 × 1578)** を手計算一致。親側 `anchor_pairing.row_pairings_sha256 = 1db92b26f408ddb6…` = **sha(0x00 × 1450)** も一致。さらに **λ の 128 個の新 lead 成分を逆順後退代入で完全再現**(不一致 0)、**復元 λ が公刊 λ 配列と完全一致**。
- **target 恒等式(988.8/988.9)**: t_final に θ_j·n_j を逆順に足し戻して t₀ を再構成 → packed sha が **親 anchor の `target_remainder_sha256` `3bba0da3f619eab5f78e715beabd22d9c7975b36f72d28ee8d7528d9d0f4648a` と一致**。θ ≠ 0 が **79/128** なので非空虚。
- **鎖(v2 より強い)**: `rolling_sha256 = sha(bytes.fromhex(predecessor) ‖ canonical(body))` の**式ごと私が再実装**し、anchor `076c4b9d…` から **128 段連続で 128/128 再計算一致**、最終 = `state_head e793896e…`。instruction の seal sha も 128/128 再現。`physical_offset = 12096×(1450+i)` が 128/128。
- **source**: artifact 同梱 `checkout-sources/`(24)+ `audit-history-sources/`(4)= **28/28 が repo 作業ツリーとバイト全一致**。
- **親 pin**: continuation = artifact **9977040548 / 304,642,285 B / `a7ecd56dba33e354…`** = 2154 受理実体 = v1/v2 と同一。

---

## 1. (1) 規約表 diff(v2 → v3)

| 規約 | v2(k=64)の宣言 | **v3(k=128)の宣言** | 本 run の実測 | 判別性 |
|---|---|---|---|---|
| `batch_size` | 64 | **128** | selected 128 / processed 128 | 実データで判別 |
| `selection_policy` | `..._64_...` | **`CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX`** | roster 昇順先頭 128(70..281) | **判別**(gap≠1 が 54) |
| `max_batches` / `refill` | 1 / False | 同 | 1 / False | — |
| `partial_policy` | `PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY` | 同 | `partial=False` | — |
| `producer_limits` / `checker_limits` | 5400s/7168MiB・10800s/7168MiB | **同(不変)** | 実 1623.542 s / 1956.717 s | — |
| basis(固定 5 弦) | [2,3,4,6,11] | 同 | 残差 5/5 = 0・fit [1,1,2,1,0] | — |
| Ω 語化 | `sr(0)=0, sr(1)=1, sr(2)=-1; ordered repair x,y,central; mod54 then exact /18` | **同一文字列** | repair = [−ε_x/6, −ε_y/6, sr(ω)] が **128/128**・ε ≡ 0 (mod 6) が **128/128** | **ω=2 が 43/128** |
| target 減算符号 | `remainder_before - theta * normalized_row` | **同一文字列** | 逆順再構成で t₀ 一致(θ≠0 が 79/128) | **非空虚に判別** |
| correction 語因子符号 | `+sr(theta)` | **同一文字列** | 各行 manifest の `target_literal_factor` が `coefficient = θ`(128/128)・`exponent = sr(θ)`(128/128・値 +1:42 / −1:37 / 0:49) | **受領証水準では判別**(語の再構成は射程外・§10) |
| ρ₂ | `mode=derived, value=1, directly_read=False` | 同 | `original_rho2_packed_sha256` あり・**DERIVED のまま** | 未昇格 |
| lower-zero | `source_lower_zero = NOT_ASSERTED` / `physical_lower_zero = true` | 同 | separator.json に同値 | **契約どおり** |
| terminal | 3 値 | 同 | `BATCH_COMPLETE_CANDIDATE` | 他 2 値は canary のみ |
| **selftest 群** | 2 群・実拒否 P [30,8] / C [28,7] | **2 群**(`k128-version-registration-and-types` / `k128-full-roster-cutoff-and-restoration`)・実拒否 **P [30,9] / C [28,8]** | 両群 PASS・exit 0 | **§6.1 の継続差分** |
| metadata canary | 16 件・`metadata_regression_from: …-v1` | **同 16 件・同 v1** | 16/16 拒否 PASS | 継承の明記は従来どおり |
| **【新設】静的継承 registry** | 無し | **`audit-region-registry.json` 76,867 B / `9fe3d9cf1449c353…`**・60 記述子(9 不変 + 2 literal 除外 + 9 変更) | **私が 60/60 を repo 実バイトで再計算・不一致 0** | **§6.2** |
| **【新設】shared TCB 受領証** | 無し(F8.89 は Sol 返信側のみ) | **`shared-tcb.json` 12,201 B / `7c304d97f64715a9…`**・4 kernel 範囲 | **私が 4/4 を repo 実バイトで再計算・一致** | **§6.3** |
| **【新設】run-receipt field** | 無し | `arithmetic_selftest_inherited_from` / `arithmetic_selftest_inheritance` / `shared_tcb` / `kernel_third_independence_claimed=false` | run-receipt に literal で存在 | **F-flb-1 の cert 面が閉じた** |

→ **凍結宣言と実装・実データの間に齟齬は見つからなかった。**

### 1.1 source 差分の実測(v2 → v3)— v1→v2 よりはるかに小さい

私が両ファイルを行単位で突き合わせた結果:

- **producer**(v2 3,420 行 → v3 3,434 行・diff 457 行): 算術本体 **v2 L74–2963 ↔ v3 L74–2963 の差は `WORKFLOW` 文字列 1 行のみ**(`-v2.yml` → `-v3.yml`・v3 L2018)。他は先頭定数(`SCHEMA` / `C_FILE` / `BATCH_SIZE,MAX_BATCHES` / `POLICY`)と L2892 以降の canary 総入替(64→128 の rename と境界値の書き換え)。
- **checker**(v2 2,675 行 → v3 2,695 行・diff 404 行): selftest 前領域の実質差は (1) 定数(`SCHEMA`/`BATCH_SIZE`/`POLICY`/`PRODUCER_FILE`/`CHECKER_FILE`/`CHECKER_WORKFLOW`)(2) `select_all_residuals` の docstring 1 行(64→128)(3) `check_registration` の `integer(..., "registered_k128", 128, 128)` literal 固定 のみ。**v2 で追加された締めゲート 4 本(`phase_candidate_ordinal` / `new_batch_row_local_offset` / `registered_selected_count` / `launch["workflow"]` literal 一致)は v3 で byte 単位不変**であり、境界は literal ではなく `BATCH_SIZE` 参照で書かれている(C3 :1114 `0, BATCH_SIZE - 1` / :1290 / :1935)。**緩めた箇所は 1 つも無い。**
- **canary の強化 2 点**(私の実測): producer に `last-selected-cycle-word` 事例が追加(拒否 9 件目)、`truncated-last-residual` が **commit 後に実 file を切り詰め manifest を再 seal してから reload を拒否させる**形へ変更(v2 は commit 時点で拒否)→ hash ではなく **descriptor 形状**を試す、より強い試験になっている。checker にも `one-hundred-twenty-eighth-cycle-word-changed` が追加(拒否 8 件目)。
- `BATCH_SIZE` の実効箇所は producer `failed[:BATCH_SIZE]`(:381)と各種上界のみ。**消去アルゴリズムには入らない**。

### 1.2 交差辺(独立性)

- checker の import は `check_d972_r07_complete_oracle_cegar_continuation_v2` のみ。`importlib` 使用 0。
- producer の `check_d972` ヒットは全部ハッシュ pin メタデータ。`importlib` は自系 `d972_r07_complete_oracle_cegar_continuation_v1.py`(`L_SHA` pin)だけ。
- **v1/v2 と同じ二系統分離**。

---

## 2. 事前登録と入力 pin

| 検査 | 結果 |
|---|---|
| 起動 commit | `794c5e9f`。workflow(3,601 行)・producer(3,434 行)・checker(2,695 行)の pin が run-receipt / source-receipt / artifact / **repo 作業ツリー**の四者一致。 |
| workflow freeze | `283,886 B / 6224c2bad40e7a95291b92aa8cb3d5088bc41969287c2262d0c4249058bcab1f / LF 3601 / CR 0`。私が repo で再計算し **Task 1045 F9 の freeze 宣言と一致**。 |
| 事前登録の凍結 | `REGISTRATION = {batch_size 128, max_batches 1, CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX, PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY, refill False, 5400s/7168MiB, 10800s/7168MiB}` が inline driver に **literal**(`:187-192`)。 |
| **selftest の事前登録** | `SELFTEST_NAMES`(2 群名)と **`SELFTEST_REJECTIONS = {'producer-selftest':[30,9],'checker-selftest':[28,8]}` が literal**(`:193-195`)。final gate が群名列(`:2630`)と拒否件数列(`:2635`)の**完全一致**を要求 → 実測と一致。**試験件数の後付け調整は不可能。** |
| **registry の事前登録** | `INHERITANCE_REGISTRY_PIN = {bytes 76867, sha256 9fe3d9cf…}` と **原文 76,867 B の raw literal** が workflow に焼かれ、`public_audit_registry()` が先に全バイト pin を検証(`:1855`)。私が workflow の `br'''…'''` から抽出した原文と artifact 同梱 `audit-region-registry.json` は**同一 sha**。 |
| 親 pin | `head["rank"] == 1450 and head["generation"] == 8155`(`:2094`)・`completed_steps == 64 / rank == 1450 / generation == 8155`(`:2247`, `:2268`)を literal 要求。 |
| **恒真 gate** | **見つからなかった。** `selected ∈ [0,128]` → `processed ∈ [0,selected]` → `dependent ∈ [0,processed]` → `accepted ∈ [0,processed]` と、`rank == 1450 + accepted` / `generation == 8155 + accepted` / `processed == dependent + accepted`(`:3257-3264`)。**accepted は固定されていない**ので、DEPENDENT が出ても gate は通る。**a(128)=128 は gate の強制ではない。** |
| silent cap | 見つからなかった。上界(`selected ∈ [0,128]`・`sequence ∈ [0,771]`・`len(bodies) <= BATCH_SIZE`)はすべて `require` で失敗側に落ちる。`progress['sequence'] == 3 + 6×processed = 771` を要求し、実測 phase 記録は 772(= 771 + final)。 |
| 保存 | `preservation-result.json`: `status PASS`・`errors []`・`missing []`・**flags 24/24 すべて true**(15 親 + 9)・`no_parent_file_renamed_trimmed_or_overwritten true`・`acquired_parent_baselines 15`・出力 6,586 file / 1,164 dir。**新 flag `all_static_audit_receipts_registry_and_history_copies_unchanged = true`** で registry/履歴 copy も保全対象に入った。 |
| 実行 source | `checkout-sources/` 24 + `audit-history-sources/` 4 = **28/28 が repo とバイト全一致**(私が全ファイル取得して比較)。 |
| 資源 | producer 実 **1,623.542 s**(内側 cap 5,400 s の **30.1 %**・外側 6,000 s の 27.1 %)・`ru_maxrss` 442,952 KiB(cap の **6.0 %**)。checker 実 **1,956.717 s**(cap 10,800 s の **18.1 %**・外側 11,400 s の 17.2 %)・`ru_maxrss` 1,547,480 KiB(**21.1 %**)。`outer_terminated` 両方 False。 |
| runtime | `python 3.13.15 / numpy 2.5.1` を `runtime-observation.json` が expected と actual で照合、gate `exact-accepted-runtime`(`:1517`)。 |

**oracle の失敗 roster がどの λ に対するものか**: `selection/start.json` の `selection_lambda_sha256 = 7c0dbe475f9b162f4648f5468ee1098eb86b43dbee247d71f811076559ab88fe` = 親(rank 1450)の Separator = **v1/v2 と同一の λ**。新 λ(`6a0fe936…`)は別 field、`new_lambda_oracle = null`(F7 の型分離は守られている)。

---

## 3. 終端受領証(F1)— 全数確認

| 項目 | 宣言値 | 私の独立検算 |
|---|---|---|
| λ_new ⊥ 新 128 行 | (全 0) | **128/128 で 0** |
| λ_new ⊥ 全 1578 行 | `row_pairings_sha256 = 71f45b82ab0759863b0e3b056613d8ff2bf9fced2fb7a27d6fbc89992eaa48ef`・`rows 1578` | **sha(0x00 × 1578) と一致**。親側 `1db92b26…` も **sha(0x00 × 1450)** と一致。旧 1450 行の実バイトは本 ZIP に無いので直接検算不能(§8-5)。checker は `ThinAnchor.measure_selection()`(C3 :756)で旧 1450 行を全部読み、`finish_arithmetic()`(C3 :358)で 1578 行すべてに dot する — **この 2 関数はいずれも registry の不変領域内**で v1/v2 とバイト同一 |
| λ_new · t₀ | `lambda_parent_remainder = 1` | **1**(再構成した t₀ に対して) |
| λ_new · t_final | `lambda_new_remainder = 1` | **1** |
| λ_pivots | 0 | 一致 |
| anchor / final pairing rows | 1450 / 1578 | 一致 |
| λ の新 lead 成分 | (公刊 λ) | **逆順後退代入で 128/128 完全再現**(不一致 0・非零 84)。**復元 λ 配列 == 公刊 λ** |
| free 座標 | — | **1691**(t_final の最初の非零・値 1・λ[1691]=1)。**λ は 1691 より上で全零**、λ[1690]=0 |
| λ の character 別 support | `[1052, 0, 0, 0]`・trit `[11044, 538, 514]` | **base-3 4-trit/byte で復号して完全一致**。内訳 = 座標<1562 が 967 + lead 帯 84 + free 1 = 1052 |
| head 連鎖 | — | anchor `076c4b9d…` から **128 段を rolling 式ごと再計算して一致** → `e793896e…` = `state_head` |
| 物理行 sha | 各 row manifest | **128/128 が実バイトの sha と一致**、`predecessor_row_manifest_sha256` 鎖 128/128、candidate の `row_manifest_sha256` = row manifest の file sha 128/128 |

**注(構造的・v2 から不変)**: `row_pairings_sha256` は零ベクトルの sha であり、**実質的には行数しか運ばない受領証**。実効的な内容は `lambda_pivots == 0` と両 remainder = 1、および checker 側の直接測定にある。本 run の欠陥ではない。

---

## 4. 実データによる規約判別(非空虚性)

### 4.1 選定 128 本の実体

- roster index **70..281**(span 212)。前半 64 = v2 と同一(70..177)、**後半 64 = 179, 182, 184, 186, 191, …, 280, 281**。
- gap ≠ 1 が **54 件**(前半 33 + 後半 27 + 境界 1)→ 政策が実データで判別されている。
- `chords_checked = 54433`(全宇宙走査)・`auxiliary_tests = 2`・`aux_values = [0,0]`(両 aux 評価・両方零 → **aux 枝は本番未発火**)。
- `terminal(selection) = VIOLATION_CANDIDATE`。witness は 128/128 が `kind=chord`・`cycles` 長 6・`tau = [0]*5`。

### 4.2 v2 との突き合わせ — **前半 64 本は物理行までバイト同一(64/64)**

私は **v2 artifact 9983058782 と v3 artifact 9987222571 の両方から `output/rows/000000..000063/physical-normalized.bin` をそれぞれ独立に取得し、64 組すべてを全バイト比較した。結果 = 64/64 完全一致**(片側 64 × 12,096 = 774,144 B)。これは抽出比較ではなく**全数**である(v2 判読の §4.2 は 6 本抽出だったので、その限界はここで解消)。

派生量も一致:

- 前半 64 の σ = 1:31 / 2:33、θ = 0:22 / 1:23 / 2:19、`selection_scalar` = 1:29 / 2:35、ω = 0:17 / 1:24 / 2:23、central ≠ 0 が 47 — **すべて v2 判読 §4.3–4.4 の値と完全一致**。
- 前半 64 の lead 列は集合 {1562..1624} ∪ {1627}、降順ステップ **15 回** — v2 判読と一致。

**Astra(root)主張との照合**: 司令塔経由で伝えられた Astra の主張(「rows/000000..000063 の 64 file・片側 774,144 B が raw byte + 全 SHA で一致」「rank 1578/gen 8283・128/128 accepted・dependent 0」「P+C 平均 27.959672460 s/行・64→128 差商 27.026139899 s/行」)は、**私の独立測定と全項目一致した**(私の値: 64/64 バイト一致・774,144 B・rank 1578 / gen 8283 / accepted 128 / dependent 0・P+C = 3578.838074867 s ⇒ **27.959672460 s/行**(完全一致)・差商 27.026142 s/行(私の v2 秒が小数 3 桁までの引用なので下 5 桁で差が出る。Astra の値から逆算した v2 P+C = 1849.165121 s は私の v2 報告の 1849.165 と整合))。**独立に得た結論であって、Astra の主張を根拠として採用したのではない。**

### 4.3 ω / central 指数(128 本)

| 量 | v3 全 128 | うち前半 64(= v2) | 後半 64(新規) |
|---|---|---|---|
| ω = 0 / 1 / 2 | **40 / 45 / 43** | 17 / 24 / 23 | 23 / 21 / 20 |
| repair = [−ε_x/6, −ε_y/6, sr(ω)] | **128/128 成立** | 64/64 | 64/64 |
| ε ≡ 0 (mod 6) | **128/128** | — | — |
| repair_x≠0 / repair_y≠0 / central≠0 | **77 / 74 / 88** | 40 / 38 / 47 | 37 / 36 / 41 |
| 三因子すべて ≠ 0 | 41 | 23 | 18 |
| **central 単独(x=y=0, cen≠0)** | **23** | 11 | 12 |
| 修理なし [0,0,0] | 13 | 5 | 8 |
| central 指数の値 | +1 が 45・**−1 が 43**・0 が 40 | — | — |

→ **`sr(2) = −1` の literal 採用は 43 件で判別されている**(裁定 2173 の枠組みどおり、これは **receipt/wire 上の signed literal 指数の採用**であって −1 対 +2 を登録 Q2 source / 物理行の値で識別したという主張ではない)。

### 4.4 σ / θ / lead / literal 因子

- **σ**: 1 が **75**、2 が **53**(前半 64 は 31:33、後半 64 は 44:20)。
- **θ(`target.scalar`)**: 0 が **49**、1 が **42**、2 が **37**。**θ≠0 の 79 件が (988.8) の符号規約を判別**。
- **`selection_scalar`**(別 field・混ぜない): 1 が 64・2 が 64。
- **`target_literal_factor`**(各 row manifest): `coefficient == θ` が **128/128**、`exponent == sr(coefficient)` が **128/128**(+1:42 / −1:37 / 0:49)。**`correction_word_factor_sign = +sr(theta)` は受領証水準で非空虚に判別された**(v1/v2 判読では「宣言のみ・未判別」としていた項目。ただし語の再構成そのものは依然私の射程外)。
- **lead**: **1562..1689 の 128 個が欠落なく連続**(distinct 128・[min,max] 内の欠番 0)。付与順は非単調(降順ステップ 32 回)。
- **t_final**: support **30,547 / 48,384**、最初の非零(free 座標)= **1691**、値 1、λ[1691] = 1。

### 4.5 情報性の内訳

- λ_new の character 別 support = **[1052, 0, 0, 0]** → **character 0 だけが情報的**(限定継続)。λ の非零 1,052 のうち **967 が座標 < 1562**(親由来の帯)、84 が新 lead 帯、1 が free 座標。
- κ: `degree0/degree1` とも **tag 0 のみ非零**、`kappa aux_values` は 8 個すべて 0。
- score: `by_tag = [40203, 23052, 23052, 0, 0, 0]`(total 86,307)→ **tag 3〜5 は零**。**v2 と同一値**(選定は同じ λ_1450 なので整合)。
- q: character 0 のみ support 2,880。`p1_equation_residual_support = 0`。
- alpha support **5,221〜5,455 / 8,059** → P1 減算は全候補で活性(非空虚)。

### 4.6 preserved-input 全数照合

15 role・親 baseline 全件の before/after が `all_parent_files_and_directories_unchanged: true`、`all_code_and_raw_unchanged: true`、acceptance 不変。P と C が**別々に**同じ `input_preservation` dict を出し(私が両 result を突合して 9 field 全一致を確認)、workflow が両者一致を要求。`flags` 24/24 true・`errors []`・`missing []`。

---

## 5. 【独立節・重点 A】a(128) と独立率

### 5.1 一次データ

| 量 | v1(k=32) | v2(k=64) | **v3(k=128)** |
|---|---:|---:|---:|
| offered(= selected_count) | 32 | 64 | **128** |
| **INDEPENDENT** | 32 | 64 | **128** |
| **DEPENDENT** | 0 | 0 | **0** |
| SKIPPED_AFTER_LINEAR | 0 | 0 | **0**(`skipped_after_linear = []`) |
| **a(n)** | a(32)=32 | a(64)=64 | **a(128)=128** |
| rank | 1450 → 1482 | 1450 → 1514 | **1450 → 1578** |
| generation | 8155 → 8187 | 8155 → 8219 | **8155 → 8283** |
| terminal | BATCH_COMPLETE_CANDIDATE | 同 | 同 |

**k = 128 でも従属は出なかった。** 裁定 2176/2177 の枠組み(a(n) = 同 λ・同初期 span・同候補順の前置長に対する量)で読むと:

- **a(128) = 128**。すなわち λ_1450 の失敗 roster の**先頭 128 本は互いに一次独立**。
- **本 run の新規情報は roster index 179..281 の 64 本のみ**(前半 64 本は v2 の物理行と全バイト同一 = §4.2)。a(64)=64 の再現に加えて a(65..128) が新たに 64 本ぶん確定した、という読み方が正しい。
- 消化率は **128 / 36,274 = 0.353 %**(v2 は 0.18 %)。**Task 988 F4 の反例は依然として排除されていない。**
- rank 1578 の λ\* に対する oracle は未計算(`new_lambda_oracle = null`)なので、「先頭 index が 281 まで進んだ」とは言えない(F10 の非単調性)。**比較可能な前進量は rank だけ。**

### 5.2 【所見 F-k128-1】lead frontier の「債務」は非単調 — v2 の F-k64-3 を訂正

| | anchor(1450) | v1 後(1482) | v2 後(1514) | **v3 後(1578)** |
|---|---:|---:|---:|---:|
| lead の最大 | 1561 | 1593 | 1627 | **1689** |
| frontier(= max lead + 1) | 1562 | 1594 | 1628 | **1690** |
| 空き座標(frontier − rank) | 112 | 112 | **114** | **112** |

v2 判読では「後半 32 段で lead 1625・1626 が飛ばされ、債務が +2 になった。**lead frontier は rank と 1:1 で進む**という外挿は成立しない」と書いた。**v3 はこれを部分的に反証する**: v3 の candidate #64 と #65 の lead はまさに **1626 と 1625** であり、v2 で空いた 2 座標が埋まった。結果、**128 段全体では frontier が 1562 → 1690 とちょうど 128 進み、債務は anchor と同じ 112 に戻っている**。

→ 正しい言い方は「**債務は batch の切り所によって一時的に増減する局所量であり、単調でも保存量でもない**」。v2 の「+2」は k=64 で止めたことによる境界効果だった。**私の v2 §5.7 の書き方(債務は増えた)は誤導であり、ここで訂正する。**

---

## 6. 新規発見

### 6.1 【継続・要修正 F-k64-1】DEPENDENT 枝は v3 でも合成・本番とも未通過

事実(すべて一次データ):

- producer selftest = 2 群のみ(`k128-version-registration-and-types` 30 件 / `k128-full-roster-cutoff-and-restoration` 9 件)。**`DEPENDENT` が producer v3 に現れるのは実装本体(`:477, :497, :509, :515, :1374-1375, :1672, :1735, :1762, :1781`)だけで、selftest には 1 箇所も無い。**
- checker v3 で `DEPENDENT` が現れるのは `:1334` の 1 箇所(実装本体)のみ。selftest には無い。
- 本番でも `dependent_candidates = 0`、`aux_values = [0,0]`。→ **本 run でも DEPENDENT 枝・aux 本番枝は一度も通っていない**(aux は §6.4 のとおり selftest 側では通る)。
- `old_success_suites: 0` は producer/checker/metadata の全受領証で維持。

**ただし v2 判読の指摘のうち「継承が cert に記録されていない」部分は完全に閉じた**(§6.2)。そして継承の実体的な強さも上がった: **DEPENDENT 判定を含む producer の行はすべて `P-core-before-workflow`(P3 L80–2017)の内側**にあり、この領域は **P1/P2/P3 の三版でバイト同一**であることを私が再計算で確認した(§6.2)。checker の `:1334` も `C-candidate-replay-and-final`(C3 L1296–1746)= 三版バイト同一領域の内側。→ **v1 の `canary_reduction`(v1 :3026, :3065 = Task 988 F4 第二反例, :3070)が試したのは、いま走っているのと同一バイトのコードである**ことが機械照合可能になった。

残る問題(ここが指摘):

- 継承は **soundness 側の議論としては十分**(誤って INDEPENDENT と判定された従属行が混じれば normalized 行が零になり自 lead = 1 が破れる → 私の階段形実測 128/128 で silent な誤りは通らない)。
- **残るリスクは liveness**: 本物の DEPENDENT が来たときに正しく記録して続行できるか、は**この 3 run のどれでも実行されていない**。registry 自身が `"Historical DEPENDENT/target/publication suite PASS is a reference, not a current-run pass."` と明記しており、**主張としては正直**だが、k を上げて roster を深く掘るほど最初の DEPENDENT に当たる確率は上がる。
- 提案(安価): producer/checker の第 2 群に **DEPENDENT を 1 例だけ通す合成 fixture**(v1 の `canary_reduction` を rename して復帰)を足す。拒否件数 literal を [30,10] / [28,9] に上げるだけで、再走コストは selftest 3.5 s / 6.0 s の内側。次に k を上げるなら、その前にこれを入れるのが安い。

### 6.2 【解消 F-flb-1 / F-k64-1 の cert 面】静的継承 registry を私が全数再計算した

`audit-region-registry.json`(76,867 B / `9fe3d9cf1449c353…`)は workflow に **原文 raw literal** として焼かれ、`public_audit_registry()` が全バイト pin を検証してから REPORT に書き出す(`:1851-1855`)。私は workflow の `br'''…'''` から原文を抽出し、**artifact 同梱の同名 file と同一 sha** であることを確認した。

内容と私の再計算結果:

| 分類 | 件数 | 私の再計算 |
|---|---:|---|
| `unchanged_regions` | 9(P 2 + C 7) | **9/9 が P1/P2/P3(または C1/C2/C3)の三版で raw バイト完全同一**。範囲 sha も 27/27 一致 |
| `literal_exclusions` | 2(`P-workflow-literal` P3 L2018 72 B / `C-selector-docstring` C3 L195 87 B) | 6/6 一致・三版で異なる(= 除外理由が実データで正しい) |
| `reviewed_change_regions` | 9 | 27/27 一致・disposition `STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY` |
| **合計 descriptor** | **60** | **60/60 一致・不一致 0** |
| source 分割 | P 各版 5 範囲 / C 各版 15 範囲 | **6 source すべてで 1 行目から末尾 LF まで gap/overlap なく被覆**(私が独立に検算・未被覆行 0) |
| 不変行の割合 | — | **P: 2,811 / 3,434 行 = 81.9 %**(v1 は 3,463 中 81.2 %・v2 は 3,420 中 82.2 %)、**C: 1,782 / 2,695 行 = 66.1 %** |

9 不変領域の実体は `P-core-before-workflow`(L80–2017)/ `P-core-after-workflow`(L2019–2891)/ `C-primitives-and-selector-signature` / `C-selector-and-reduction-state` / `C-pinned-inputs-and-root-records` / `C-selected-tree-and-witnesses` / `C-candidate-replay-and-final` / `C-input-result-diagnostics` / `C-whole-prefix-check-and-signs`。

さらに workflow の `compare_audit_regions()`(`:1769-1823`)は **run 中に実 source から再計算**しており、`require(descriptors == 60)`・`require(first == cursor)`(gap/overlap 禁止)・`require(cursor == source['lf'] + 1)`(EOF まで)を強制する。**印を押すだけの受領証ではない。** 歴史 4 source は `audit-history-sources/` に全バイト複製され、`historical_sources_imported_or_executed_in_this_run: false` を宣言。私はこの 4 file も repo とバイト一致を確認した。

registry の `limits`(5 条)は正直: 「不変な関数バイトは別途登録された batch size に依存するので、全 n で同じ出力になるという主張ではない」「C 全 body 同一は主張しない」「歴史 DEPENDENT/target/publication 群の PASS は参照であって今回の PASS ではない」「新 aux selftest 被覆は、未使用のままの runtime aux 枝とは別物」「v1/v2 の先頭 32 行 file 同一は metadata のみ・版束縛の owner/HEAD/manifest は異なる」。

→ **私が v2 §6.1 で提案した「`arithmetic_selftest_inherited_from` + 不変算術領域の行範囲/sha を受領証に載せる」は、提案より強い形で実装された。F-flb-1 の「cert 単独では独立性の限界が読み取れない」も §6.3 で閉じる。**

### 6.3 【解消 F-flb-1(shared TCB)】共有カーネル 2 本が run の cert に登録された

`shared-tcb.json`(12,201 B / `7c304d97f64715a9…`)が **4 kernel 範囲**を登録し、私が repo 実バイトで全数再計算した:

| kernel | side | file | 行 | region bytes / sha | 私の検算 |
|---|---|---|---|---|---|
| `vectorized_projection_chunk` | P | `search/d972_r07_actual_grade2_root_scalar_batch_v2.py` | 342–357 | 1,011 / `b68bbb5af24240a8…` | 一致 |
| `vectorized_projection_chunk` | C | `search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py` | 269–284 | 1,020 / `6e785bdf5b4fb8b2…` | 一致 |
| `sparse_adjoint` | P | `search/d972_r07_targeted_grade2_owner_generated_join_v15.py` | 192–203 | 670 / `4b75584298a67005…` | 一致 |
| `sparse_adjoint` | C | `search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py` | 192–203 | **670 / 同一 sha** | 一致 |

- workflow の `compare_audit_shared_kernels()`(`:1827-1842`)が `require(raw_by_kernel[('sparse_adjoint','P')] == raw_by_kernel[('sparse_adjoint','C')])` を実行 → **`sparse_adjoint` は P/C でバイト同一であることが run 中に実測されている**。
- `vectorized_projection_chunk` は 1,011 / 1,020 B で異なり、registry は「Projection sides retain different docstring/error-label bytes」と説明。私は C 側 docstring `"""Independent bounded implementation of the sparse packed projection."""`(`search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py:271`)が本 run の checkout-sources にそのまま同梱されていることを確認した。**cert が共有性を明記した今、この docstring が単独で誤読を招く度合いは下がった**が、docstring 自体は未修正。
- `current_run_call_coverage = NOT_MEASURED` / `kernel_third_independence_claimed = false` を cert が明示。**本 run の実呼出行は依然として特定されていない**(§8-4)。P1 相が候補時間の **72.1 %** を占めるので前者は確実に load-bearing。

### 6.4 【所見】aux 枝は selftest では通っている(2177 追補の型を維持)

producer 第 2 群に `auxiliary-only` / `complete-zero`、checker 第 2 群に `first-auxiliary` / `second-auxiliary` / `all-zero` の陽性 fixture が実在し PASS。**本番 aux 未発火(`aux_values = [0,0]`)と selftest 側の実 PASS 経路は別**であり、裁定 2177(a) の訂正型をそのまま維持する。DEPENDENT にはこの型の陽性 fixture が**無い**(§6.1)。

### 6.5 【所見】締め方向のみ・分離条件も満たす

- v2 で追加された 4 ゲートは v3 で**バイト不変**(BATCH_SIZE 参照で書かれているため 128 でも自動的に効く)。
- 新 canary 2 件(`last-selected-cycle-word` / `one-hundred-twenty-eighth-cycle-word-changed`)と `truncated-last-residual` の強化(commit 後 file 切詰め + manifest 再 seal → reload 拒否)で**締め方向のみ**。
- **「何にでも当たる試験」ではない**: 版差分に当たる陰性 fixture(`old-policy` / `old-64-witness-cutoff` / `old-invocation-k64` / `old-owner-scope64` / `batch-64` / `batch-127` / `batch-129` 等)と、陽性 fixture(`failed64/65/127/128/129`・`m64/m65/m127/m128/m129`・`auxiliary-only`・`second-auxiliary`・`complete-zero`)が併走。**落ちているのは「変えていない部分」の被覆**であり、それは §6.2 の静的継承で(実行ではなく)文書化された。

### 6.6 【継続 F-k64-7】時間値の非独立性

- checker は producer の `elapsed_seconds` を採用する構造が継続。ただし harness(inline driver)が producer 1,623.542 s / checker 1,956.717 s を**独立計測**して cert に載せており、自己申告(1,622.717 / 1,956.121)との差は 0.83 / 0.60 s。さらに `child_rusage_after` / `child_io_last_sample` も harness 側で採取。**run 単位の秒は裏が取れている。**
- **checker には段別 timestamp が無い**(`checker-stderr.log` 16,234 行に時刻・秒フィールドが 0 個)。→ checker の候補あたり限界単価は §7 の差分でしか出せない(v2 と同じ限界)。
- 相ごとの秒は producer の自己計測(`coverage-receipt.json` の `phase_measurements` 772 件)。自己計測の総和 1,432.754 s は harness 総計 1,623.542 s を超えておらず、上から押さえられている。

### 6.7 【継続・仕様】diagnostics artifact の重複

`9987222571`(candidate)と `9987231704`(diagnostics)はともに **369,233,546 B**、digest だけ違う(`781c9f46…` / `89499643…`)。workflow が両 upload に同じ path `${{ runner.temp }}/fixed-lambda-batch-v3/` を渡し(`:3589`, `:3598`)、run-receipt が `candidate_and_diagnostics_upload_the_same_envelope_root: True` を宣言(`:3452`)。**欠陥ではない**(v2 で閉じた型)。ops 所見: 369 MB を二重保管。`retention-days: 30` が両方に付いた。

---

## 7. 【独立節・重点 B】費用曲線 v1 / v2 / v3

### 7.1 実測(すべて私が `coverage-receipt.json` の 772 件の phase 測定と run-receipt から集計)

| | v1(k=32) | v2(k=64) | **v3(k=128)** | v2→v3 比 |
|---|---:|---:|---:|---:|
| 追加行 | 32 | 64 | **128** | 2.00 |
| oracle 回数 | 1 | 1 | **1** | — |
| producer 実秒(自己申告) | 432.437 | 825.483 | **1,622.717** | 1.966 |
| producer 実秒(harness 外形) | n/a | 826.027 | **1,623.542** | 1.966 |
| checker 実秒(自己申告) | 551.331 | 1,023.682 | **1,956.121** | 1.911 |
| checker 実秒(harness 外形) | n/a | 1,024.656 | **1,956.717** | 1.910 |
| **P + C(自己申告)** | 983.768 | 1,849.165 | **3,578.838** | 1.935 |
| **1 行あたり P+C(run 単位)** | 30.743 | 28.893 | **27.960** | — |
| **限界単価 P+C(直前 run との差商)** | — | 27.044 | **27.026** | ほぼ一定 |
| 限界単価 P / C(内訳) | — | 12.283 / 14.761 | **12.457 / 14.569** | — |
| 候補六相 合計 | 351.018 | 707.981 | **1,419.982** | 2.006 |
| **候補あたり** | 10.969 | 11.062 | **11.094** | 1.003 |
| selection(oracle 1 回) | 11.880 | 11.963 | **11.836** | 0.989 |
| final separator | 0.869 | 0.893 | **0.936** | 1.048 |
| **計測外の固定費** | **68.670** | **104.647** | **189.963** | **1.815** |
| 出力 ZIP | 94,677,901 B | 187,072,168 B | **369,233,546 B** | 1.974 |
| ZIP / 行 | 2.959 MB | 2.923 MB | **2.885 MB** | — |
| producer cap 使用率(5,400 s) | 8.0 % | 15.3 % | **30.1 %** | — |
| checker cap 使用率(10,800 s) | 5.1 % | 9.5 % | **18.1 %** | — |
| producer `ru_maxrss` | — | 437,064 KiB | **442,952 KiB**(6.0 %) | — |
| checker `ru_maxrss` | — | 1,546,708 KiB | **1,547,480 KiB**(21.1 %) | — |

### 7.2 producer の相分解(772 件の phase 測定を私が全集計)

| 相 | 128 候補の合計 | 1 候補あたり | 候補時間比 | v2 の比 | v1 の比 |
|---|---:|---:|---:|---:|---:|
| raw | 13.573 | 0.1060 | 1.0 % | 1.0 % | 0.9 % |
| source | 33.909 | 0.2649 | 2.4 % | 2.5 % | 2.3 % |
| primal | 308.768 | 2.4122 | **21.7 %** | 21.7 % | 21.8 % |
| **p1(corrected_source)** | **1,023.651** | **7.9973** | **72.1 %** | 72.0 % | 72.2 % |
| B(四 character) | 9.428 | 0.0737 | 0.7 % | 0.7 % | 0.7 % |
| reduction(実消去) | 30.654 | 0.2395 | 2.2 % | 2.1 % | 2.1 % |
| **候補 計** | **1,419.982** | **11.0936** | 100 % | — | — |
| selection(section 11.509 + cochain 0.090 + tree 0.237) | 11.836(1 回) | — | — | — | — |
| final separator | 0.936 | — | — | — | — |
| 計測外の固定費 | **189.963** | — | — | — | — |

- **primal + p1 = 1,332.418 s = 候補六相 1,419.982 s の 93.83 % = producer 全 1,622.717 s の 82.11 %。**(v2 は 93.66 % / 80.33 %、v1 は 94.01 % / 76.31 %。裁定 2173 の分母規律に従い候補相内比率と process 全体比率を分けて書く。)
- **律速は 3 run とも P1 補正相**。比率は k を 4 倍にしてもほぼ不変。

### 7.3 【要修正 F-k128-2】fixed(k) の 2 点外挿は外れた — 3 点で引き直す

| k | 実測 fixed(s) | v2 の 2 点モデル `32.7 + 1.124k` | 誤差 |
|---:|---:|---:|---:|
| 32 | 68.670 | 68.67 | 0 |
| 64 | 104.647 | 104.65 | 0 |
| **128** | **189.963** | **176.57** | **−13.39 s(実測が 7.6 % 大きい)** |

- 区間傾き: 32→64 で **1.1243 s/k**、64→128 で **1.3331 s/k** → **凸**(k に対し超線形)。
- 3 点最小二乗: **fixed(k) ≈ 26.01 + 1.2734 k**(残差 +1.91 / −2.86 / +0.95 s)。
- ZIP は k にほぼ比例(2.959 → 2.923 → 2.885 MB/行)なので「出力 inventory / hash が k に比例」という説明は維持されるが、**fixed/ZIP は 0.725 → 0.559 → 0.515 s/MB と単調に下がる**ので、単純な「バイト比例」でもない。出力 file 数(v2 3,322 → v3 6,586)にほぼ比例する量と読むほうが実測に合う。
- **3 点でも法則ではない。** 次点(k=256 相当)が取れれば凸性の有無が決まる。

### 7.4 cap から取れる k と残り工程(**明示的に外挿**)

**(a) rank 非依存モデル**(現 rank 1578 近傍のみ有効):

- producer(k) ≈ fixed(k) + 11.094k + 12.772 ≈ **38.8 + 12.367k** → cap 5,400 s で **k_max ≈ 433**(v2 判読の見積り ≈ 436 とほぼ同じ。fixed の上振れを候補単価の据え置きが相殺した)。
- checker(k) ≈ **91.3 + 14.569k**(v2 と v3 の 2 点から独立に出した切片が **91.25 / 91.25 で一致**)→ cap 10,800 s で **k_max ≈ 735**。
- **律速は producer(不変)**。残り行数 48,384 − 1,578 = **46,806**。限界単価 27.026 s/行で**純 P+C ≈ 14.6 日**。

**(b) rank 依存を入れたモデル**(reduction 相のみ rank 依存と仮定):

- reduction 相の秒は候補 ordinal と **corr 0.905**(v2 は 0.662)・傾き **0.000204 s/行**(v2 は 0.000248)。先頭 16 平均 0.2274 → 末尾 16 平均 0.2519。比例モデル(0.2274 × 1/1450 = 0.000157)の **1.30 倍**(v2 は 1.55 倍と推定していた)。
- `cand(R) ≈ 10.854 + 0.2274 + 0.000204·(R − 1450)` として cap を解くと:

| rank R | 候補秒 | その rank で取れる k_max |
|---:|---:|---:|
| 1,578 | 11.11 | **433** |
| 10,000 | 12.83 | 380 |
| 20,000 | 14.87 | 332 |
| 30,000 | 16.91 | 295 |
| 40,000 | 18.95 | 265 |
| 48,000 | 20.58 | 245 |

- **k_max 自身が rank とともに縮む**。1,578 → 48,384 を積分すると **必要 run ≈ 150 回**、producer 側だけで **≈ 9.4 日**。checker も同率で伸びると仮定すると **P+C ≈ 20 日規模**。
- **桁は動いていない**が、これは 128 行の窓から 47,000 行を外挿した値であり、**法則ではない**。特に p1(72 %)が本当に rank 非依存かは、この窓では検証できていない(候補あたり合計は前半 64 で 11.076 s、後半 64 で 11.111 s = +0.035 s。ノイズと区別できない)。

### 7.5 語長との関係(F-k64-5 の再確認)

| 相 | corr(語長, 秒) | 傾き(s / 1,000 letters) | 候補時間の占有 |
|---|---:|---:|---:|
| raw | **+0.998** | 0.0046 | 1.0 % |
| source | **+0.999** | 0.0386 | 2.4 % |
| primal | +0.028 | 0.0002 | 21.7 % |
| p1 | −0.103 | −0.0023 | 72.1 % |
| B | −0.071 | −0.00002 | 0.7 % |
| reduction | −0.054 | −0.0001 | 2.2 % |
| **合計** | **+0.816** | **0.0410** | 100 % |

語長 26〜12,354(平均 5,845)。**結論は v2 と同じ**:「語長は raw/source 相を厳密に支配するが、その二相は費用の 3.4 % にすぎない。支配的な p1 + primal(93.8 %)は語長と無相関」。傾き 0.0410 s/1k は v2 の 0.0424 とほぼ同じ。

---

## 8. 限定条項(8 条)

1. **射程 = rank 1450 → 1578 の 1 batch のみ**。rank 1578 の λ\* に対する oracle は**未計算**(`new_lambda_oracle = null`)。新 λ での失敗弦数・先頭 index は不明。**NONMEMBER 主張ではない。**
2. **a(128) = 128 は roster 前置 128 本の観測**(batch パラメータ k の性質ではない)。うち前半 64 本は v2 の物理行と全バイト同一で、**新規情報は roster index 179..281 の 64 本**。36,274 件中 128 件 = 0.353 %。**Task 988 F4 の反例は排除されていない。** なお k を上げるほど「古い λ_1450 で選んだ弦」を深く消化することになる(F10 の非単調性が効く範囲が広がる)— これは独立率とは別軸で未測定。
3. **DEPENDENT 枝は本番・selftest とも未通過**(v1 以来 3 run 連続)。継承の根拠は §6.2 の静的 registry(算術領域が三版バイト同一)にあり、**今回の実 PASS ではない**。registry 自身がそう明記している。
4. **算術 TCB は共有カーネル 2 本を含む**(`vectorized_projection_chunk` / `sparse_adjoint`)。v3 で cert に登録されたが、`current_run_call_coverage = NOT_MEASURED`・`kernel_third_independence_claimed = false`。**第三独立性はこの 2 本に及ばない**、実呼出行も未特定。
5. **旧 1450 行の実バイトは私自身は未取得**。λ_new ⊥ 旧行 と ρ₂ の旧行部分は checker の `ThinAnchor` 再現に依存する(その再現コードは registry の三版不変領域内)。**ρ₂ は依然 DERIVED。**
6. **harness TCB は単著**(workflow 3,601 行 + inline driver 238,281 B)。私は harness 出力を根拠に使わず、§3〜§5・§7 を生バイトから第三実装で再導出した。ただし **§7 の相別秒だけは producer の自己計測**である。
7. **checker の段別 timestamp は無い**(16,234 行に時刻 0 個)ため、checker の限界単価は run 間差商でしか出せない。
8. **私は 369 MB の ZIP を全量ダウンロードしていない**(HTTP Range で必要な entry を個別取得)。ZIP 全体の sha は GitHub API の digest `781c9f46…` を採り、自分でバイト再計算していない。ただし取得した各 entry は zip の圧縮データから展開しており、内容の照合は私自身の計算である。

---

## 9. CV-9 裁定案・工房格付け案(一行)

**CV-9 = 同一対象(SAME OBJECT)・限定 8 条 → 工房格付け案: checker PASS / cross-checked(限定 8 条)・rank 1578 / gen 8283 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。v1(1482)・v2(1514)・control-96(1482)とは行の由来が異なる別状態であり、合算しない。**

**司令塔への一行**: k=128 は **128/128 独立・P+C 3,578.8 s・限界単価 27.03 s/行**で 2164 の天井が消えたことを再々確認し、**私が v2 で出した 3 指摘のうち 2 つが片付いた**(cert への継承記録 = §6.2/§6.3 で提案以上の形で実装・空き座標債務の「増加」= §5.2 で境界効果と判明し撤回)。**残る 1 つは DEPENDENT 枝の未試験**で、これは 3 run 連続かつ k を上げるほど当たりやすくなる方向なので、**k=256 に進む前に合成 fixture 1 例を足すのが安い**(拒否件数 literal を +1 するだけ・再走コストは selftest 数秒)。費用面では **fixed(k) の 2 点外挿が 7.6 % 外れた**(実測 189.96 s)ので 3 点で `26.0 + 1.273k` に引き直したが、**producer cap から取れる k ≈ 433 は据え置き**。ただし **k_max は rank とともに縮む**(rank 40,000 で ≈ 265)ので、残り 46,806 行は **≈ 150 run / P+C ≈ 20 日規模**と見るのが現時点の最良の外挿である。

---

## 10. 判読者の限界(正直な申告)

- 旧 1450 行の実バイトを取得していないので、λ_new ⊥ 旧行 と ρ₂ 恒等式の旧行部分は checker の再現に依存している。
- 語(Ω / P1 / literal)の**再構成**は私の射程外。ε/ω/repair 指数と `target_literal_factor` は **producer の申告と checker の式計算の受領証水準での突合**として検証した(§4.3–4.4)。
- `sparse_adjoint` が本 run の実行経路で呼ばれた行は特定していない(両側でバイト同一であることまで)。
- §7.3–7.4 の外挿は **3 点フィット/128 行窓**であり、法則ではない。
- ZIP 全体の sha は API digest を採用(§8-8)。
- **この観点では仕様の齟齬(別対象)を見つけられなかった** — 保証ではない。

---

## 付録: 主要 pin(すべて私が実バイトから再計算 or API から取得)

| 対象 | 値 |
|---|---|
| run / head | 34023589045/1 / `794c5e9f883cb5ff21b2ee087c1d4baa84ac6760`(09:04:03Z→10:08:05Z・success) |
| candidate artifact | 9987222571 / 369,233,546 B / `sha256:781c9f467bd38305c524a0a2bf5b361f45e75bc4234d9cf6e891e01175db9e2e`(API) |
| diagnostics artifact | 9987231704 / 369,233,546 B / `sha256:89499643872e5909c910f625cbf7517611a1bf31df13e74c3004f0a917fffaac`(API) |
| 親 continuation | 9977040548 / 304,642,285 B / `a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792` |
| workflow | `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v3.yml` 283,886 B / `6224c2bad40e7a95291b92aa8cb3d5088bc41969287c2262d0c4249058bcab1f` / LF 3601 / CR 0 |
| inline driver | `driver.py` 238,281 B / `9246e5c55a3bf5bc0657442d4f6547616e9437644c6ec7b823175f49631608ec` |
| producer source | `search/d972_r07_fixed_lambda_cycle_batch_v3.py` 209,926 B / `a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8` |
| checker source | `search/check_d972_r07_fixed_lambda_cycle_batch_v3.py` 178,914 B / `1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7` |
| audit registry | `audit-region-registry.json` 76,867 B / `9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38`(**60/60 私が再計算**) |
| 継承受領証 | `arithmetic-selftest-inheritance.json` 37,593 B / `30646de054521f9f3bea571e1d9f331facfb97418d545089153cac65174164f5` |
| 共有 TCB 受領証 | `shared-tcb.json` 12,201 B / `7c304d97f64715a941f9ef142fe5fa23d8839fdd4879c2751fee7caa5ea6983b`(**4/4 私が再計算**) |
| 歴史 run(継承元) | 34004423047/1 / head `81a1b22975308ae0ac628f97da447a008a1d087e` / artifact 9980697123 / 94,677,901 B / `d21f9e0b93b07032…`・旧 3 群拒否 P[7,6,26] C[2,3,14] |
| 親 target(t₀) | `3bba0da3f619eab5f78e715beabd22d9c7975b36f72d28ee8d7528d9d0f4648a`(**私の逆順再構成が一致**) |
| 選定 λ(旧・rank 1450) | `7c0dbe475f9b162f4648f5468ee1098eb86b43dbee247d71f811076559ab88fe` |
| 新 λ | `6a0fe9368f2ec7f28c4d8076e7d3184fb57322b9d0905a8e7c3c26b467bcee4e`(**私が lambda.bin を hash して一致**・repack でも一致) |
| 最終 target | `7868b7806a0dc41c2bda8a1c4c6a10d1cfa2c2e6968aadf561e93820f12053e1`(同上) |
| row_pairings(final) | `71f45b82ab0759863b0e3b056613d8ff2bf9fced2fb7a27d6fbc89992eaa48ef` = **sha(0x00 × 1578)** |
| row_pairings(anchor) | `1db92b26f408ddb6f3ac47574cd49cf4dc131efa8090477bf6d0a5feea4bdf1c` = **sha(0x00 × 1450)** |
| state_head | `e793896e585bd0e540e25770359e8d36d1a84d69c012d88615e5ecffc02dfba9`(anchor `076c4b9d…` から **128 段を式ごと再計算**) |
| producer result | `output/result.json` 206,763 B / `5c05826c01d7cbca003a66cafde7430fcc7b997876afe2aaf449235d498dc18f` |
| checker result | `checker-result.json` 11,956 B / `5fcb1f9a8a568cf10df660be339763e6e7619bd73bf5932e286796204cf4020b` |
| coverage receipt | 871,787 B / `0ff16ed67e07ab16da7e21e9554acb7d3401bf396b8d438fb056a89d1067157b` |
| preservation result | 998,292 B / `125b99c98ff6c2a86b90c0c9da3922dbef70612d4b2897df83f868e1c71feaf6` |
| run-receipt | 39,614 B / `e8edc336d16cc4a030b4726aea992f3e1e1633af11635911bdb9dc0cbc1839ca`(status PASS・`workshop_CV9 = PENDING`) |
| producer selftest | `producer-selftest-stdout.json` 1,703 B / `dd24a08d4d0bca711ffd162e08e2e1cda653fdd7570fc6f1f3fb6aab1efbbc7d`(2 群 30+9) |
| checker selftest | `checker-selftest-stdout.json` 1,885 B / `010160b8f9579029e46d5443bdc44fdd1e495271cdb3f8317cc9d31bcb2e8a1c`(2 群 28+8) |

---

報告書 sha256(この行を追記する前の全体): a6890c43518c02728ca3cdfa64f6f38a6c92a6174ec8785ae7a242cef7d3bb76 / 先頭 16 桁 = **a6890c43518c0272**


---

**裁定 2187(司令塔・2026-09-06)格付け**: 本判読(原本 `scratchpad/fal_cv9_fixed_lambda_batch_v3_report_v1.md` 49,682 B・sha256 2633edf730a21810bb31515ed8ace48feaa714f36c5ea8dd360de7340c878bf7)を正本として採用。CV-9 = 同一対象・限定 8 条 → **rank 1578/gen 8283 を cross-checked(限定 8 条)で受理**・verified=false・grade-2 NOT_DECIDED・A0 actual 0/1 不変。v1(1482)/v2(1514)/control-96(1482)とは別状態で合算しない。要修正 = F-k64-1(DEPENDENT 枝の合成 fixture 1 例を k = 256 前に)・F-k128-2(費用モデルを 3 点凸 fixed(k) ≈ 26.0 + 1.273k・k_max ≈ 433 へ更新)。F-k64-3 は撤回。
