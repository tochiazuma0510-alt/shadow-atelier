# fixed-lambda cycle batch v1(初回 batch・rank 1450 → 1482)増分 CV-9 判読(falsifier 逐語・裁定 2172 で正本化)
著者: falsifier(opus/max・非当事者)。司令塔が scratchpad 報告書(sha256 先頭 16 桁 4137108849e7684d・保存ファイル全体)を逐語転記(2026-09-06)。

**工房裁定(2172)**: CV-9 = **同一対象**(限定 9 条)→ **batch v1 の状態 rank 1482/gen 8187 を受理**(cross-checked 限定 9 条・GRADE2 NOT_DECIDED・verified=false・逐次経路の rank 1482 とは行の由来が異なる別状態)。同一性は P/C の PASS フラグに依存せず第三実装で全量再導出: target 恒等式(t_final に θ_j·n_j を逆順に足し戻した t₀ の packed sha = 親 anchor の target sha 3bba0da3…・θ ≠ 0 が 20/32)・選定 oracle が control-96 step 64 と完全一致(first_failed_index 70・residual_nonzero 36,274 = 別 workflow・別実装で同じ oracle 再現)・row_pairings = sha(0x00×1482) 手計算一致・λ_new の新 32 lead 成分を逆順後退代入で完全再現・消去は挿入順前進消去(RREF ではない)をデータが判別。**実効前進率**: offered 32/accepted 32/dependent 0(独立率 1.00)・rank 1450 → 1482・producer 432.4 s・checker 551.3 s。対照 control-96(逐次 32 段)比: oracle 32 回 → 1 回・P+C 92.6 s/行 → **30.7 s/行(3.01 倍速)**・逐次限界単価比 1.38 倍速。相分解: 候補 10.97 s のうち P1 補正 7.93 s(72 %)+ primal 2.39 s(22 %)= 律速は固定次元配列作業(SLP 語長 34〜12,354 letters で時間は 5.7 % しか動かない)。**F-flb-6(重大・朗報)**: 2164 の checker 構造的天井(rank ≈ 1,890)は**解消** — batch checker は thin anchor から始まり prefix を再生しない(551 s = 枠の 5.1 %)。新しい律速 = (a) P1 補正相 (b) k を上げたときの独立率 a/k(未知)。**F-flb-1(要修正)**: P/C で実行コードが文字一致する数値カーネル 2 本(`vectorized_projection_chunk`(docstring は "Independent bounded implementation" だがコピー)・`sparse_adjoint`(正規化 sha 一致))が producer 時間 94 % の P1 相を通る load-bearing → 表現訂正か共有 TCB としての明示登録。**次の実験の推奨**: 32/32 独立は k = 32 の一点観測で Task 988 F4 の反例は排除されない・外挿(残 46,902 行・k ≈ 480/run・98 run・16.7〜25 日)は全てこの一点に乗る ⟹ **k = 64/128 で a/k を測るのが情報量最大**。その他: DEPENDENT 枝・aux 枝は本番 0 回発火(canary は両側とも F4 の二反例を張る)・elapsed_seconds は cross-check されない・diagnostics = candidate 同一バイト数(F-c96-3 継続)・新 lead は 1562..1593 の連続 32 整数(空き座標 112 は前後不変)。限定 9 条: (i) 射程 = λ_1450 固定の roster 先頭 32 本の 1 batch(rank 1450 → 1482)・NONMEMBER ではない (ii) 独立率 1.00 は k = 32 の一点観測 (iii) DEPENDENT/aux 枝は本番未発火 (iv) 継承カーネル 2 本が P1 相で load-bearing (v) 旧 1450 行の実バイトは未取得(λ_new ⊥ 旧行は checker の ThinAnchor.measure_selection の全数実測に依存)(vi) checker に段別 timestamp なし (vii) elapsed は非 cross-check (viii) λ·ρ₂ は DERIVED (ix) 最終 rank 1482 の oracle は未計算。**判読規律**: batch 型では⑤に「offered/accepted/dependent・独立率・相分解の秒」と「target 恒等式の逆順足し戻し」を恒久追加。

---

# 増分 CV-9 判読 — R07 fixed-lambda cycle batch v1(rank 1450 → 1482 を 1 batch で・初回本走)

対象: run **34004423047/1**(success・event=push・head `81a1b22975308ae0ac628f97da447a008a1d087e`・01:38:33Z→01:56:40Z)
候補 artifact **9980697123**(`d972-r07-fixed-lambda-cycle-batch-v1-candidate-34004423047-1`・94,677,901 B)
判読者: falsifier(非当事者・事後)。判読日 2026-09-06。
親裁定: 2143/2144(cycle_mat E 1 本)・**2154**(resume64・rank 1450 受理・限定 8 条)・**2164**(control-96・rank 1482 受理・限定 8 条)。
数学契約: `sol/luna_reply_988_r07_fixed_lambda_batch_math_audit.md`(Astra 監査・F0〜F12)。

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 9 条(§7)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 9 条つき)。`verified=false`。GRADE2 NOT_DECIDED。**

**batch の実効前進率(§5 に独立節)= offered 32 / accepted 32 / dependent 0・rank 1450 → 1482(+32)・
producer 432.437 s・checker 551.331 s。同じ +32 を出した control-96 の P 822.483 s + C 2,139.770 s に対し
run 単位で 3.01 倍速、逐次の限界単価 42.36 s/行 に対し 30.74 s/行 = 1.38 倍速。**

同一性の根拠(すべて私の第三実装による再導出。producer/checker の PASS フラグは根拠に使っていない):

- **選定**: `chord-residuals.u8` から残差を再計算(= `values − tau·fit`)し、失敗集合 36,274 件・先頭 index 70 を再現。
  公刊 `failed-indices.u32` と**全 36,274 件バイト一致**。選定 32 件は昇順 roster の先頭 32(index 70..119)で
  **policy と完全一致**。各 witness の τ(z_e) = T·d、τ(k_e) = 0、六項の係数 [e:+1, J 順 −d_j]、
  scalar = 残差 ∈ {1,2} を **32/32 で再現**。
- **消去**: 32 本の normalized 行を生バイトから復元し、insertion 順の階段形(自 lead で 1・先行 lead で全零)を **32/32 確認**。
  同時に「後続 lead で非零」が **322 箇所**あり、**RREF ではなく挿入順前進消去**であることをデータが判別している。
- **target 恒等式(988.8/988.9)**: t_final に θ_j·n_j を逆順に足し戻して t₀ を再構成し、
  その packed sha が親 anchor の target sha **`3bba0da3f619eab5f78e715beabd22d9c7975b36f72d28ee8d7528d9d0f4648a` と一致**。
  θ ≠ 0 が 20/32 なので**非空虚**。
- **最終 Separator(F1)**: λ_new ⊥ 新 32 行を全数 0 で確認、λ_new·t_final = 1、λ_new·t₀ = 1。
  `row_pairings_sha256` = **sha(0x00 × 1482) = e6f763f1…** を手計算で一致確認。
  さらに **free 座標からの逆順後退代入を私が独立に走らせ、λ_new の新 32 lead 成分を完全再現**した。
- **入力**: 親 artifact 9977040548 を GitHub API で照会 → 304,642,285 B / `a7ecd56dba…` = workflow の pin =
  2154 で受理した実体。候補 ZIP は Release ミラー実測 sha `d21f9e0b93b07032…` と **API digest が一致(二点一致)**。
- **source**: artifact 同梱 `checkout-sources/` **24 件が repo 作業ツリーとバイト全一致**(unmatched 0)。

---

## 1. (1)(2)(3) — 規約表 diff / 交差辺 / 類似度

### 1.1 規約表 diff(E 1 本 → k 本一括で何が増えたか)

| 規約 | 凍結時の宣言 | 本 run の実測 | 判別性 |
|---|---|---|---|
| 選択規則 | `CHORD_FIRST_ROSTER_32_THEN_FIRST_AUX`・`batch_size 32`・`max_batches 1`・`refill false` | roster 昇順の先頭 32(index 70..119)。aux は弦失敗が 0 のときだけ | **実データで判別**(§4.1) |
| basis の選び方 | 固定 5 弦(親から継承) | `basis_chords [2,3,4,6,11]`・basis 残差は 5/5 で 0 | 固定・変更なし |
| Ω 語化(v547 三因子) | `sr(0)=0, sr(1)=1, sr(2)=-1; ordered repair x,y,central; mod54 then exact /18` | repair = [−ε_x/6, −ε_y/6, sr(ω)] が **32/32**。ε は 32/32 で 6 の倍数 | **ω=2 が 14/32・ε≠0 が x 17/y 18** |
| g = sr(ω)(central 因子) | 同上 | central 指数 ≠ 0 が **23/32**、うち **central 単独(x=y=0)6 件** | **F-cy-1 は再び完全閉鎖** |
| P1 減算 | `old-global-ascending-embedded-original-lead; new-owner-major-ascending-original-lead` | alpha support 5,300〜5,448 / 8,059(全候補で活性) | 非空虚 |
| lower-zero | source 96,776 全零 | 32/32(checker `each_candidate_full_96776_zero`) | — |
| **k 行の実消去** | 挿入順前進消去・依存は append しない | 32 offered → **32 independent / 0 dependent**・rank 増分 = 追加行数 32 | **依存枝は本番未発火**(§6.2) |
| **新 λ(batch 後 Separator)** | 旧 λ とは**別型**(F7)。`selection_lambda_sha256` と `lambda_sha256` を別 field で保持 | 旧 λ `7c0dbe47…`(親由来)/ 新 λ `0c2f6b2e…`。`new_lambda_oracle = null` を明記 | **型分離は実装で守られている** |
| target 減算符号 | `remainder_before - theta * normalized_row` | 私の再構成で t₀ 一致(θ≠0 が 20/32) | **非空虚に判別** |
| correction 語因子符号 | `+sr(theta)` | 宣言のみ(語の再構成は私の射程外) | 未判別 |
| terminal | `BATCH_COMPLETE_CANDIDATE` / `COMPLETE_ZERO_CANDIDATE` / `LINEAR_MEMBERSHIP_CANDIDATE` の 3 値 | `BATCH_COMPLETE_CANDIDATE`(t_final ≠ 0・support 31,003) | 他 2 値は canary のみ |
| source lower zero(literal) | **NOT_ASSERTED を維持**(F6) | `separator.json: source_lower_zero = "NOT_ASSERTED"`・`physical_lower_zero = true` | **契約どおり** |

→ **凍結宣言(Task 988 F2〜F7)と実装・実データの間に齟齬は見つからなかった。**

### 1.2 交差辺

- producer が `check_*` を **import する箇所 0**(`check_d972` の 11 ヒットは全部ハッシュ pin のメタデータ)。
- checker が `d972_*` を import / 動的 load する箇所 **0**(`importlib` の使用も 0)。
- 消去系: producer は `m.physical_reduce / normalize_pivot / update_target`(`d972_r07_actual_root_seed_materializer_v3`)、
  checker は `L.reduce_dense / normalize / next_target`(`check_..._continuation_v2`)。**別系統**。
- 選定系: producer は `oracle.solve_five`(解く)、checker は **明示逆行列 `inverse`**(`basis.T @ inverse ≡ I` を検算してから
  `d = inverse @ tau[e]`)。**アルゴリズムが違う**。
- 最終 λ: producer は自前の逆順後退代入 + `m.check_final_separator`、checker は `L.next_separator`(凍結 one-row wrapper を
  「最後の 1 行 + 残り全部を pivots」として再利用)+ 自前の全 1482 行 pairing。**解法が違う。**

### 1.3 類似度 — 【要修正 F-flb-1】P/C で実行コードが文字一致する数値カーネルが 2 本ある

| 関数 | producer 側 | checker 側 | 実行コード |
|---|---|---|---|
| `vectorized_projection_chunk` | `search/d972_r07_actual_grade2_root_scalar_batch_v2.py:342` | `search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py:269` | **docstring と error label 以外は 1 文字も違わない** |
| `sparse_adjoint` | `search/d972_r07_targeted_grade2_owner_generated_join_v15.py:192` | `search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py:192` | **正規化後 sha 完全一致(27e32afb43d1)** |

`vectorized_projection_chunk` の checker 版 docstring は
`"""Independent bounded implementation of the sparse packed projection."""` と**独立を明示的に主張**しているが、
本体はコピーである(producer 版は `"""Project one bounded row chunk with the exact sparse packed kernel."""`、
差は他に `require` のラベルが `projection_chunk_shape` → `checker_projection_chunk_shape` のみ)。

**load-bearing 性**: checker 側の呼び出しは `check_d972_r07_complete_oracle_cegar_continuation_v2.py:236`
(`FixedBundle` の P1 cache 射影)、producer 側は `search/d972_r07_full_origin_refinement_v1.py:448`。
本 run の producer 時間の **94 %(p1 253.6 s + primal 76.4 s)が P1 相**なので、この経路は確実に走っている。
`sparse_adjoint` を含む `join_v15` も両側で `ARITH` として import されている(`..._grade2_root_scalar_batch_v2.py:25 / :22`)が、
本 run の経路で実際に呼ばれた行までは私は特定していない。

→ **継承由来で本 run の新規事由ではない**(2143/2154/2164 の「継承クローン」限定条項の実体がこれ)。
だが「独立実装」という docstring は事実に反するので、**表現の訂正か、当該 2 本を「共有 TCB」として明示登録するかのどちらかが要る**。

---

## 2. 事前登録と入力 pin((5) 前段)

| 検査 | 結果 |
|---|---|
| 起動 commit | `81a1b229…`「Run initial fixed-lambda cycle batch [r07-fixed-lambda-cycle-batch-v1-run]」。**workflow・producer・checker がこの 1 commit で初出**。 |
| 事前登録の凍結 | commit 時点の producer sha = `229785eb91be9852…`(213,861 B)、checker sha = `7a4289506ce78b0e…`(181,828 B)。**workflow env の pin・repo 作業ツリー・artifact 同梱 source の三者と一致**。 |
| silent cap | なし。`REGISTRATION = {batch_size 32, max_batches 1, selection_policy CHORD_FIRST_ROSTER_32_THEN_FIRST_AUX, refill False, producer_limits 5400s/7168MiB, checker_limits 10800s/7168MiB}` が **workflow inline driver に literal で焼かれ**、final gate が `owner.json['registration'] == REGISTRATION` と `invocation[batch_size]==32, max_batches==1, processed_candidates_before==0, accepted_new_rows_before==0` を要求(`.github/workflows/d972-r07-fixed-lambda-cycle-batch-v1.yml:1794-1799`)。 |
| 親 pin | anchor = 9977040548 / 304,642,285 B / `a7ecd56dba…`(API 実測一致)= **2154 受理実体**。`start.json` の `rank==1450 and generation==8155 and anchor_completed_steps==64` を final gate が literal で要求(同 :1675-1679)。 |
| 恒真 gate | 見つからなかった。final gate はすべてデータ依存(2154 F-r64-2 の恒真 jq gate は本 workflow に存在しない)。 |
| 保存 | parent baseline **15 role / 9,150 file**(continuation 単独 7,916)。`preservation-result.json` は `status PASS・errors []・missing []・flags 全 true・no_parent_file_renamed_trimmed_or_overwritten true`。P と C が**それぞれ独立に** input_preservation を出し、workflow が両者の一致を要求。 |
| 実行 source | `checkout-sources/` 24 件が **repo 作業ツリーとバイト全一致(unmatched 0)**。 |
| candidate ZIP | Release ミラー実測 sha `d21f9e0b93b070327b4ef02e975dc377a8020e7f8aa7553a720d97d690ed85f0` = **GitHub API digest と一致**。1,911 entry・非圧縮計 326,338,251 B・unsafe path 0。 |

**oracle の failing chord roster がどの λ に対するものか**: `selection/start.json` の
`selection_lambda_sha256 = 7c0dbe475f9b162f4648f5468ee1098eb86b43dbee247d71f811076559ab88fe`
= 親(rank 1450)の Separator。36,274 件の失敗弦は**この λ に対して**評価されたもので、新 λ に対する roster ではない。
**control-96 の step 64(rank 1450 起点)の実測値(先頭 index 70・失敗総数 36,274)と完全一致**しており、
別 workflow・別実装で同じ oracle が再現されたことになる(§5.3)。

---

## 3. (4) 終端受領証 — F1 の全数確認

| 項目 | 宣言値 | 私の独立検算 |
|---|---|---|
| λ_new ⊥ 新 32 行 | (全 0) | **32/32 で 0** |
| λ_new ⊥ 全 1482 行 | `row_pairings_sha256 = e6f763f1858d097239395c80ac7d953aa0111988028facc0e60830a04f852ad6`・`rows 1482` | **sha(0x00 × 1482) と一致**。旧 1450 行は本 ZIP に無いので直接検算はできないが、**checker は `ThinAnchor.row()` で親 blob から実バイトを読み、`finish_arithmetic` で 1482 行すべてに dot している**(`check_…_batch_v1.py:369-375`) |
| λ_new · t₀ | `lambda_parent_remainder = 1` | **1**(再構成した t₀ に対して) |
| λ_new · t_final | `lambda_new_remainder = 1` | **1** |
| λ_pivots | 0 | 一致 |
| anchor_pairing_rows / final_pairing_rows | 1450 / 1482 | — |
| head 連鎖 | — | anchor `076c4b9d…` から 32 段の `predecessor`/`rolling_sha256` が **32/32 で連続**、最終 `fc41c186f114f4ef…` = `state_head` |

**限定 (viii) の部分解消**: 前 2 回の判読では「base 1386 行の λ 直交は未再現」だったが、
本 checker の `ThinAnchor.measure_selection()`(`:733-748`)は **旧 1450 行を全部読み、
(a) 各行が自 lead で 1・先行 lead で 0(三角性) (b) λ_anchor ⊥ 全 1450 行 (c) λ_anchor·前後 target = 1
(d) target が全 lead 座標で 0** を直接測っている。旧 8059 命令の rolling も `base_pivot_metadata` で
`L.OLD_HEAD` まで再計算している。**旧行に対する直交は checker 側では再現された**(私自身は旧行バイトを持たないので未再現)。

---

## 4. (5) 実データによる規約判別(非空虚性)

### 4.1 選定 32 本の実体

roster index: **70, 72, 73, 77, 79, 80, 81, 82, 83, 84, 85, 87, 88, 89, 90, 91, 94, 98, 99, 101, 103, 105, 106, 107, 109, 111, 113, 114, 116, 117, 118, 119**
(gap 列 = 2,1,4,2,1,1,1,1,1,1,2,1,1,1,1,3,4,1,2,2,2,1,1,2,2,2,1,2,1,1,1)。
先頭 edge 125。**gap が 1 でない箇所が 15 件**あるので、「先頭 32 index を機械的に取った」のではなく
**残差が非零の弦だけを昇順に 32 本取った**ことをデータが判別している。
基準 5 弦の残差は 5/5 で 0 = 選定弦は J に属さない(F3 の要求どおり)。

### 4.2 ω / central 指数の全 32 列

| 量 | 値 |
|---|---|
| ω = 0 / 1 / 2 | **9 / 9 / 14**(ω=2 が **43.8 %**・control-96 の新 32 では 34 %) |
| repair = [−ε_x/6, −ε_y/6, sr(ω)] | **32/32 成立**(producer は SLP node の実指数を読み、checker は式から計算 → 両者を result.json 全体のバイト比較で突合) |
| ε ≡ 0 (mod 6) | 32/32 |
| repair_x ≠ 0 / repair_y ≠ 0 / central ≠ 0 | **17 / 18 / 23** |
| 三因子すべて ≠ 0 | 9 |
| **central 単独(x=y=0, cen≠0)** | **6** → **F-cy-1 完全閉鎖** |
| 修理なし([0,0,0]) | 3 |

→ **`sr(2) = −1` の規約は 14 件で判別されている**(`+2` や `+1` なら値が変わる)。

### 4.3 σ / θ / lead

- σ: 1 が 16 件、2 が 16 件(**σ=2 が半数 ⟹ 正規化スケールの符号規約が判別されている**)。
- θ(target.scalar): 0 が **12/32(37.5 %)**、1 が 9、2 が 11。θ=0 の 12 件は「rank は増えるが target は動かない」正常段(F6)。
  **θ≠0 の 20 件が (988.8) の符号規約を判別**している(逆符号なら t₀ 再構成が壊れる)。
- lead: **1562..1593 の連続 32 整数ちょうど**。ただし付与順は非単調(1568 の次が 1564、1573 の次が 1570 等)で、
  「小さい空き座標から順に配る」実装ではないことをデータが判別している。
- t_final: support 31,003 / 48,384、first nonzero(free 座標)= **1594**、その値 2、λ_new[1594] = 2。
  free は新 lead 集合にも属さない。

### 4.4 情報性の内訳

- λ_new の character 別 support = **[1007, 0, 0, 0]** → **character 0 だけが情報的**(限定 (iv) 継続)。
  trit 内訳 [11089, 497, 510]。
- λ_new は座標 ≥ 1562 の範囲で `{free} ∪ {新 32 lead}` の外に非零を **1 つも持たない**(後退代入の構造どおり)。
- `aux_values = [0, 0]` → **aux 枝は本番で未発火**。
- alpha support 5,300〜5,448 / 8,059 → **P1 減算は全候補で活性**。

### 4.5 preserved-input 全数照合

15 role・9,150 file の before/after が `all_parent_files_and_directories_unchanged: true`、
code before/after が `all_code_and_raw_unchanged: true`、acceptance 不変。
P と C が別々に同じ `input_preservation` dict を出し、workflow が両者と自前の inventory の三者一致を要求。

---

## 5. 【独立節・重点】batch の実効前進率

### 5.1 実測(すべて一次データ)

| 量 | 値 |
|---|---|
| offered 候補 | **32**(= 登録 batch_size・refill なし) |
| **独立 (INDEPENDENT)** | **32** |
| **従属 (DEPENDENT)** | **0** |
| SKIPPED_AFTER_LINEAR | 0 |
| rank | **1450 → 1482(+32)** |
| generation | 8155 → 8187(+32) |
| terminal | `BATCH_COMPLETE_CANDIDATE` |
| producer 実秒 | **432.436731**(枠 5,400 s の **8.0 %**) |
| checker 実秒 | **551.331469**(枠 10,800 s の **5.1 %**) |
| job 実時間 | 01:38:33Z → 01:56:40Z = 1,087 s(枠 330 min の 5.5 %) |

**k 本中の独立本数 = 32/32(独立率 1.00)。rank 増分 = 追加行数 = 32。**

### 5.2 producer の相分解 — 【新発見 F-flb-7】律速は oracle ではなく P1 補正相

| 相 | 32 候補の合計 | 1 候補あたり | 比率 |
|---|---:|---:|---:|
| selection(section 11.582 + cochain 0.089 + tree 0.209) | **11.880**(1 回のみ) | — | — |
| raw | 3.29 | 0.103 | 0.9 % |
| source | 7.96 | 0.249 | 2.3 % |
| primal | 76.40 | 2.388 | 21.8 % |
| **p1(corrected_source)** | **253.60** | **7.925** | **72.2 %** |
| B(四 character) | 2.34 | 0.073 | 0.7 % |
| reduction(実消去) | 7.42 | 0.232 | 2.1 % |
| 候補 計 | **351.02** | **10.969** | 100 % |
| final separator | 0.869 | — | — |
| 計測外の固定費(入力受入・親 9,150 file hash 等) | **68.67** | — | — |

- **逐次の 1 段 = oracle 11.9 s + 候補 11.0 s ≈ 22.9 s** で、control-96 の実測限界単価 21.20 s とよく合う。
  つまり **batch 化が削ったのはちょうど oracle 分**(32 × 11.88 → 1 × 11.88 = 368 s の節約)。
- **残る律速は P1 補正相(候補時間の 72 %)**。次の高速化はここを叩くしかない。
- 候補あたり実時間は **10.69〜11.30 s(変動 5.7 %)**なのに **SLP 語長は 34〜12,354 letters(363 倍)**。
  → **【新発見 F-flb-8】コストは語長でなく固定次元の配列作業(8,059 P1 行・96,776 source 座標)で決まる。**
  「語が長い候補は高い」という直観は本データで否定される。

### 5.3 control-96 との頭付き比較(同一 anchor・同一 rank 増分)

両者とも親 = 9977040548(rank 1450)、到達 rank = 1482。**同じ +32 を、別方式で出した対照実験になっている。**

| | control-96(逐次・裁定 2164) | **fixed-λ batch v1** |
|---|---:|---:|
| 追加行 | 32 | **32** |
| oracle 回数 | 32 | **1** |
| 独立/従属 | 32 / 0 | **32 / 0** |
| producer 実秒 | 822.483 | **432.437** |
| checker 実秒 | 2,139.770(96 段を start から再生) | **551.331**(prefix 再生なし) |
| P + C | 2,962.25 | **983.77** |
| 1 行あたり P+C(run 単位) | 92.6 s | **30.7 s** → **3.01 倍速** |
| 1 行あたり(逐次の限界単価 21.20+21.16) | 42.36 s | **30.74 s** → **1.38 倍速** |

**選定 oracle の一致**: 本 run の `first_failed_index = 70`・`residual_nonzero = 36,274` は、
control-96 の step 64(同じ rank 1450 起点)の実測値と**完全に一致**する。
別 workflow・別 producer・別 checker で同じ oracle が再現されたことになり、**選定側の同一対象性の強い証拠**である。

### 5.4 roster 消化は比較できない(正直な申告)

- batch は λ_1450 の失敗弦のうち **index 70..119** を一度に消化した(span 49)。
- 逐次 32 段は先頭 index を **70 → 99** へ進めた(+29)。
- しかし **batch 後の λ* に対する oracle は計算されていない**(`new_lambda_oracle = null`)。
  Task 988 F10 のとおり、旧 λ で零だった未選定弦が新 λ で非零になり得るので、
  **「先頭 index が 119 まで進んだ」とは言えない**。逐次側も同じ理由で「消化」は単調量でない(前回判読で後退 23/95)。
- → **両者を比較できる前進量は rank だけ**であり、そこでは **32 offered → 32 accepted(1:1)**。

### 5.5 【新発見 F-flb-6・重大】checker の構造的天井(F-c96-1)は本アーキテクチャで解消

2164 の F-c96-1 は「checker が毎回 start から全 prefix を再生するので内部 cap 10,800 s は ≈ 508 段 = rank ≈ 1,890 で尽きる」だった。
本 batch checker は **thin anchor から始まり prefix を一切再生しない**
(`old_snapshot_numeric_replays = 0`・`old_insert_numeric_replays = 0`・`old_success_suites = 0` を workflow が literal で要求)。
32 候補で 551.3 s = 枠の 5.1 %。**この天井は消えた。**

ただし **rank 依存は残る**:

- `reduce_dense` は毎候補 rank 行に対して走る(本 run の reduction 相 0.232 s/候補 @ rank ≈ 1,466)。
- 最終 Separator は rank 行の後退代入(0.869 s @ 1,482 行)。
- 線形外挿すると rank 48,384 では reduction ≈ 7.7 s/候補、final ≈ 28 s。
  **候補単価は 10.97 s → 約 18.5 s(1.7 倍)に増える**見込み。

### 5.6 外挿(線形外挿であって予言ではない)

物理次元上界 48,384(F10)まで残り 46,902 行。

| 前提 | 値 |
|---|---|
| 1 run の producer 枠 5,400 s から取れる k | (5400 − 68.7 − 11.9 − 0.9)/10.97 ≈ **484 行**(rank 依存項を無視) |
| 1 run の checker 枠 10,800 s から取れる k | 10800/17.23 ≈ 627 行 |
| **律速** | **producer 側 cap で k ≈ 480** |
| 必要 run 数 | 46,902 / 480 ≈ **98 run** |
| 純計算時間 | 46,902 × 30.74 s ≈ 1.44 × 10⁶ s ≈ **16.7 日**(rank 依存 1.7 倍を織り込むと ≈ 25 日) |

2164 の control-96 路線(200 run 超・38 日)より改善だが、**桁は動いていない**。

**そして最大の未知数**: 上の外挿は **k = 32 で独立率 1.00 だったという一点観測**に依存している。
Task 988 F4 は「相異なる違反は相互独立を保証しない」の紙上反例(32 行すべて違反でも rank 増分 1)を与えており、
k を 32 → 480 に上げたとき独立率が保たれる保証は数学的にも実測的にもない。
→ **次に情報量が最大の実験は k を 64 / 128 に上げて a/k(独立率)を測ること**であり、
run 数の見積りはその後でしか意味を持たない。

---

## 6. 新規発見・継続所見

### 6.1 【要修正 F-flb-1】P/C 共有の数値カーネル 2 本(§1.3 に詳細)

`vectorized_projection_chunk` と `sparse_adjoint` は P 系 / C 系で実行コードが文字一致。
前者の checker 側 docstring は「Independent bounded implementation」と独立を主張しているが実体はコピー。
本 run の producer 時間の 94 % を占める P1 相を通る。継承由来だが、**表現の訂正 or 共有 TCB としての明示登録**が要る。

### 6.2 【軽微 F-flb-2】DEPENDENT 枝と aux 枝は本番で 0 回発火

- 32/32 が INDEPENDENT、`aux_values = [0,0]` なので aux fallback も未発火。
- ただし **両枝は selftest の合成 fixture で通っている**:
  - producer `canary_reduction`(`:3026-3090`): ordinal 0 = σ=2 & θ=2、**ordinal 1 = 同一ベクトル再投入で DEPENDENT**、
    **ordinal 2 = INDEPENDENT かつ remainder_pairing = normalized_pairing = 0**(Task 988 F4 第二反例そのもの)、
    ordinal 3 = target 零 → `LinearMembershipCandidate`。
  - checker `reduction_canary`(`:2212-2285`): 同じ 4 分岐 + θ=1/θ=2 の両符号 + Linear 後の reduce 拒否。
- → **「何にでも当たる試験」ではない**(陽陰の canary が P 側 3 suite・C 側 3 suite で全て PASS、
  `rejected_cases` に列挙された変異は P 側 21 件・C 側 19 件すべて拒否)。だが **本番データによる裏付けは無い**。

### 6.3 【軽微 F-flb-3】diagnostics artifact は candidate と同一バイト数(F-c96-3 の継続)

`9980697123`(candidate)と `9980698886`(diagnostics)がともに **94,677,901 B**、digest だけ違う
(`d21f9e0b…` / `a9352750…`)。同一 path の二重 upload + ZIP 非再現性という前回と同じ構図。

### 6.4 【軽微 F-flb-4】`elapsed_seconds` は cross-check されない

`compare_producer_result`(`:1839`)は `"elapsed_seconds": actual["elapsed_seconds"]` と producer の値をそのまま採用し、
`finite_measurement` で有限性だけ見る。**§5 の producer 時間は producer 自身の申告**である
(job の外形時間 1,087 s とは整合する)。checker 時間 551.33 s は checker 自身の申告。

### 6.5 【所見 F-flb-5】新 lead は 1562..1593 の連続 32 整数 — 空き座標の債務は増えていない

- anchor rank 1450 の lead は全部 [0,1561] にあり、空き座標は 1562 − 1450 = **112**。
- batch 後 rank 1482 の lead は [0,1593]、空き座標は 1594 − 1482 = **112**。
- → **この batch は「空き座標」を 1 つも増やしていない**。次の batch でも同じなら lead frontier は rank と 1:1 で進む。
  一点観測なので傾向とは言わない。

### 6.6 【所見】λ の型分離は実装で守られている

`selection_lambda_sha256`(旧・親由来 `7c0dbe47…`)と `lambda_sha256`(新 `0c2f6b2e…`)が別 field。
`BatchReductionState` は `lambda: None` を不変条件として持ち(`d972_…_batch_v1.py:445-451`)、
**成長中の span は current Separator を一切 export しない**。`new_lambda_oracle = null` で
「新 λ の oracle は未計算」を明示。Task 988 F7 の要求どおり。

---

## 7. 限定条項(9 条)

1. **射程** = rank 1450 → 1482 の **1 batch のみ**。rank 1482 の λ* に対する oracle は**未計算**
   (`new_lambda_oracle = null`)。新 λ での失敗弦数・先頭 index は不明。
2. **k = 32 の一点観測**。独立率 32/32 は k=32 でのみ測られた。Task 988 F4 の反例は排除されていない。
   k を上げたときの独立率は UNKNOWN。
3. **DEPENDENT 枝・aux 枝は本番未発火**。両枝の正しさは合成 canary のみが担保。
4. **情報的なのは character 0 だけ**(λ support [1007,0,0,0])。lead 帯は [1562,1593]。
5. **aux は [0,0] で未発火**、κ は tag 0 のみ、score は tag 3〜5 零。
6. **witness は roster 先頭 32(index 70..119)**。54,433 弦中 36,274 が失敗のままで、消化率は依然 0.2 % 程度。
7. **算術 TCB は継承 22 本 + 新規 2 本**。うち `vectorized_projection_chunk` / `sparse_adjoint` は
   **P/C で実行コードが同一**(§1.3)。第三独立性はこの 2 本に及んでいない。
8. **harness TCB は新規**(workflow 1,993 行 + inline driver 単著)。私は harness 出力(coverage-receipt)を根拠に使わず、
   §3〜§5 を生バイトから第三実装で再導出した。
9. **旧 1450 行の λ 直交は私自身は未再現**(親 ZIP を本判読では取得していない)。checker は `ThinAnchor` で
   親 blob の実バイトを読み全数検算しており、その限りで限定 (viii) は**部分解消**。ρ₂ は依然 DERIVED。

---

## 8. CV-9 裁定案・工房格付け案(一行)

**CV-9 = 同一対象(SAME OBJECT)・限定 9 条 → 工房格付け案: checker PASS / cross-checked(限定 9 条)・
rank 1482 / gen 8187 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。**

**司令塔への一行**: 本 run は「1 batch = 32 行・独立率 1.00・P+C 984 s」で control-96 の 1/3 の時間に同じ rank を出し、
**2164 F-c96-1 の checker 構造的天井(rank ≈ 1,890)を解消した**。
残る律速は **P1 補正相(候補時間の 72 %)** と **k を上げたときの独立率 a/k(未知)** の二つで、
撤退条件はこの二つで書き直すのが妥当。次の一手として情報量が最大なのは **k = 64 / 128 の独立率測定**である。

---

## 9. 判読者の限界(正直な申告)

- 旧 1450 行の実バイトを取得していないので、λ_new ⊥ 旧行 と ρ₂ 恒等式の旧行部分は **checker の再現に依存**している。
- checker には段別 timestamp が無い(`checker-stderr.log` 4,317 行に時刻なし)ため、
  **checker の候補あたり限界単価は分離測定できていない**。§5.6 の checker 側外挿は run 平均 17.23 s/候補による粗い値。
- 語(Ω/P1/literal)の再構成は私の射程外。ε/ω/repair 指数は **producer の申告と checker の式計算の突合**として検証した。
- `sparse_adjoint` が本 run の実行経路で呼ばれた行は特定していない(両側で import されていることまでは確認)。
- **この観点では仕様の齟齬(別対象)を見つけられなかった** — 保証ではない。

---

報告書 sha256(この行を追記する前の全体): 95daf1a1b6d89ccf2e3abfbfe1fa25fa59146930f030edf09210a4f24d927c3e  / 先頭 16 桁 = **95daf1a1b6d89ccf**
