# control-96(cap 96・rank 1482・前進率対照)増分 CV-9 判読(falsifier 逐語・裁定 2164 で正本化)
著者: falsifier(opus/max・非当事者)。司令塔が scratchpad 報告書(sha256 先頭 16 桁 ab0218fe2ba1c99b・保存ファイル全体)を逐語転記(2026-09-06)。

**工房裁定(2164)**: CV-9 = **同一対象**(限定 8 条)→ **rank 1482/gen 8187 を受理**(cross-checked 限定 8 条・GRADE2 NOT_DECIDED・verified=false)。算術 source 22 件が repo と全件バイト一致・交差辺 0・**harness TCB は新規**(workflow resume-next-v1 + inline driver.py 単著 = gate の TCB; 判読はその出力に依存せず全量を第三実装で再導出)。ZIP 608,103,877 B/sha 5ec5667b… を falsifier 独立 DL・Astra DL・API digest の三点一致・事前登録(dispatch-input の observed_parent と max_appends=96 が発射前 REST body とバイト一致)・親 pin = 2154 受理実体・旧 64 保全は 5,145 file 中 5,143 がバイト同一(変化は HEAD と result.json のみ)・埋め込み accepted-parent 7,916 file 全一致・head 連鎖 96/96・row_pairings = sha(0x00×rank_after) 96/96(最終 sha(0x00×1482))・λ_j·target_j = 1 と λ_j ⊥ 全新規行 96/96・invocation 4 件(0→1/1→32/32→64/64→96)・入力契約 canary は陽陰 8 変異全拒否+実入力通過・2154 F-r64-2 の恒真 jq gate は resume-next-v1 に存在せず(final_mode でデータ依存結合検査)。符号規約は 95/95 成立・逆符号 32/95 = scalar 0 の step と完全一致 ⟹ scalar ≠ 0 の 63 step が規約を判別。cen_pow = sr(ω) 96/96・三因子 x 59/y 58/central 57・中心因子単独 13 step(F-cy-1 完全閉鎖)・**ω = 2 は 26/96(新 32 で 11/32 = 34 %)へ増加**。λ の台は 96/96 で char 0 のみ・q の char 1〜3 零・κ tag 0 のみ・score tag 3〜5 零・witness 96/96 chord・basis 固定。**前進率(F-r64-1 更新)**: 先頭失敗弦 index は 4 → 99(+1.0010/段・後退 23/95・消化 0.182 %)= 完全に安定・加減速なし。**失敗弦総数**: 2154 の「横ばい」は端点 2 点の読みで、96 観測では OLS 傾き −1.602 ± 0.336(NW t = −4.77)だが大半は消化 prefix の機械的減少(68 → 1)で、固定 tail(index ≥ 103)は −0.919 ± 0.361(t ≈ −2.6・弱い・band [103,27216) は平坦・減少は上半分に散漫・多重性込み p ≈ 0.02)⟹ 「減っている」とも「横ばい」とも断定しない両面報告。外挿更新(線形・予言ではない): roster 経路 ≈ 5.44×10⁴ 段(rank ≈ 5.58×10⁴)/ tail 経路 ≈ 3.94×10⁴ 段(rank ≈ 4.08×10⁴)= 2154 の外挿を 3 % 以内で再現・桁は動かない。**F-c96-1(重大・資源)**: 2154 の「append 単価 ≥ 25 s・上昇中」は第三点で否定 — 単価は 22.75/22.70/22.75/**21.20** s で平坦(最後の 32 段で 7 % 低下)・checker も微減・本 run の使用率 P 15 %/C 20 %/job 16 %。**しかし checker は毎回 start から全 prefix を再生するため内部 cap 10,800 s は ≈ 508 段で尽きる = 現行 full-prefix-replay checker の構造的天井 = cap ≈ 500 / rank ≈ 1,890**(cap 倍々で rank 5.4×10⁴ を狙うと純計算 ≈ 38 日・200 run 超)。⟹ 撤退条件は (a) 前進率 1.00 弦/段 (b) tail 減少 0.92 弦/段(弱い)(c) checker の構造的天井 rank ≈ 1,890 の三つで書く・rank 5×10⁴ は資源でなく設計の問題(増分検証か段階 anchor への切替)。F-c96-2: result.json の new_physical_appends 96 は累積(本 run 32)。F-c96-3: candidate と diagnostics は同一 path を upload(同一バイト数・digest 差は ZIP 非再現性)。F-c96-4: alias 逆対照は pin 継承だが accepted_target_derivation_parents 33 → 128・最終 129 = 33+96 の動的証拠あり。F-c96-5: target.scalar = 0 は 96 中 32 段(新 32 で 28 %)。限定 8 条: (i) 射程 = rank 1450 → 1482 の 32 周回(累積 96)・rank 1482 の oracle なし (ii) F-cy-1 閉鎖 (iii) ω = 2 が 26/96 へ増加・gate は両読みを区別しない (iv) informative は char 0 のみ・lead [1458,1593] (v) κ/aux/score 零 (vi) witness は roster 先頭・消化 0.182 % (vii) 算術 TCB 不変・harness TCB 新規(単著) (viii) base 1386 行の λ 直交未再現・λ·ρ₂ DERIVED。

---

# 増分 CV-9 判読 — complete oracle CEGAR resume-next v1「対照 96」(実 96 段・rank 1482 候補)

対象: run **33995829771/1**(success・head `920780033b3aaa519a898e8b6b1d29fe67a04cd1`・job 101386095754)
候補 artifact **9978703124**(`d972-r07-complete-oracle-cegar-resume-next-v1-candidate-33995829771-1`)
判読者: falsifier(非当事者・事後)。判読日 2026-09-06。
親裁定: 2131 / 2138 / 2143 / 2144 / 2145 / 2149 / 2150 / 2151 / **2154**(限定 8・rank 1450 受理)/ **2155**(一回限りの対照 96)。
判読規律: 2154 §9(①②③ = source sha 無変更 1 行・⑤ に chord-residual 全列を追加)+ Astra 依頼
(`ops/express/20260906_astra_fable_control96_success_cv9.md`)。

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 8 条(§11)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 8 条つき)。`verified=false`。GRADE2 NOT_DECIDED。**

同一性は今回、**保存の全数バイト照合**で最強の形で取れた:

- 親 output 5,145 file のうち **5,143 file が新 output でバイト同一**、変化したのは `HEAD` と `result.json` の 2 件のみ。
  すなわち **step 000001–000064 の manifest・snapshot 000000–000063 の全 phase payload は文字どおり同一バイト**であり、
  前 64 段の head 連鎖は「一致した」のではなく「同じバイトである」。
- 埋め込み `accepted-parent/` **7,916 file が、私が独立に GitHub API から取得して sha を検算した親 ZIP と全件バイト一致**(mismatch 0 / missing 0)。
- 20 本の凍結算術 source と `source-receipt.json` は親と**バイト同一**(`3a50dd12025079a6…`)。
- 規約宣言(符号恒等式文字列・signed_representative・raw_repair_order・cap 意味論)は親と同一で、
  **符号規約は実データで 63 step が判別している**(§5.1)。

**重要な更新が 2 件ある(§7・§8.1)。CV-9 の同一性は揺るがないが、キャンペーンの続行判断に直接効く。**

---

## 1. ①②③(source sha 無変更・1 行規律)

- **算術 TCB は不変**: `executed-sources/` 22 件(python 20 + workflow 2)が**すべて repo 作業ツリーとバイト一致**(unmatched 0)。
  producer `search/d972_r07_complete_oracle_cegar_continuation_v1.py` = 126,940 B / `67d2302c3c4d571a…`、
  checker `search/check_d972_r07_complete_oracle_cegar_continuation_v2.py` = 129,557 B / `e985b4ca3922fc4f…`。
  いずれも起動 commit `920780033b…` の版とも一致。`source-receipt.json` は親と**バイト同一**。
- 交差辺の再確認: producer が `check_*` を import する箇所 **0**、checker が `d972_*` を import / 動的 load する箇所 **0**。
- **【差分の正直な申告】harness TCB は新規**: workflow が resume64-v1 → **resume-next-v1(109,035 B / `7050a882297d8304…`)** に替わり、
  さらに**新 file `driver.py`(83,342 B / `d85b4f6ac81f25e7…`)が artifact に保存されている**(親 artifact には無かった)。
  これは workflow inline の metadata driver で、`coverage-receipt.json`・preservation・final gate を生成する。
  算術には触れないが**gate の TCB ではある**。→ 私は coverage-receipt の値を根拠に使わず、
  **§3–§6 の全量を生バイトから第三実装で独立に再導出した**(下記はすべて自前計算値)。

→ **①②③ は「算術 source sha 無変更・新規算術 module なし・交差辺 0」。harness は新規だが判読は harness 出力に依存していない。**

## 2. 入力 pin と保存宇宙(⑤ 前段)

| 検査 | 結果 |
|---|---|
| 候補 ZIP 実体 | **608,103,877 B / `5ec5667b77a3ed788161ed3e75e9b6ca65f170849deab2272e581b0291c1ef9e`**。<br>**私自身の独立 DL と Astra の DL が両方このハッシュ**で、GitHub API の `digest` とも一致(三点一致) |
| ZIP entry / 展開忠実度 | **15,703 entry**・非圧縮計 **2,088,905,182 B**・**unsafe path 0 / symlink 0** |
| 事前登録された dispatch 入力 | `dispatch-input.json` の `observed_parent`(9,275 文字)と `max_appends`(`"96"`)が、<br>**発射前にローカルに置かれた REST body `…/cegar-resume-next-dispatch-parent33990567016-cap96-v1.json`(10,004 B / `d5ad1f602a9efda6…`)の中身とバイト一致**。<br>`observed-parent-input.txt` / `observed-parent.json` とも整合。**silent cap も後付け変更もない** |
| 親 pin の実体 | run 33990567016/1 / artifact 9977040548 / `sha256:a7ecd56dba33e354…`。<br>**私が独立取得した親 ZIP の sha256 がこの値と一致**(= 2154 で受理済の実体そのもの) |
| 親 pin の状態 | rank **1450** / gen **8155** / completed 64 / Separator / UNKNOWN_CAP / state_head `076c4b9d…` / start `87bd9b89…`。<br>すべて 2154 判読済の値と一致 |
| 埋め込み `accepted-parent/` | **7,916 file / 1,046,747,777 B が親 ZIP とバイト全一致**(mismatch 0) |
| `before/HEAD` `before/result.json` | 親 `output/HEAD` `output/result.json` と**バイト同一** |
| 旧 output の不変 | 共通 **5,145 file** のうち変化は `HEAD` と `result.json` の **2 件のみ** → **旧不変 5,143 file**(sha 全数照合) |
| 新規分 | snapshot 32 dir(000064–000095)・step 32 dir(000065–000096)・**invocation 1 件のみ**(`ec3519d26c104847b242300151526416`)。他に新規 output file なし |
| 新 output roster | **7,706 file / 1,252 dir / 1,028,793,851 B**(自前 walk = run-receipt 一致) |
| live parents | 15(元 14 + accepted-parent)。`task554_accepted_failure: true` を保持 |
| 事前試験の継承 | `prior_tests_authenticated_without_rerun` 6 件・**全件 `rerun: false`** と正直に記帳(§9.3) |
| 入力契約の対照 | `input-contract-canary.json`: **8 変異すべて拒否**(bool-count / wrong-rank / wrong-workflow / missing-checker-entry / nonresumable-terminal / path-traversal / reset-cap / noninteger-cap)、かつ**実入力は通る**。<br>= 陽性対照 + 陰性対照が揃った非空虚試験 |
| `all-parent-files-before` vs `after` | バイト同一 / `preservation-result.errors` = `[]` / 不変 flag 5 本すべて true |

## 3. ④ 終端受領証・head 連鎖(96/96)

自前実装(project module を一切 import せず canonical / sha / trit unpack / dot を独立実装。
`canonical = json.dumps(sort_keys, separators=(",",":"), ensure_ascii) + "\n"` を親データで較正済)で生バイトから再導出。

| 検査 | 結果 |
|---|---|
| head 連鎖 `sha(bytes.fromhex(prev) + canonical(instruction − rolling))` | **96/96 一致**、終端 `330ffd80fc3ce0b8930084d9ced4e929e02e7f9a35e72c11459f1c3b8a600bce` = `output/HEAD.state_head` |
| **前 64 head の同一性** | **step manifest 000001–000064 が親とバイト同一**(§2)。連鎖の前半は再計算でなく同一バイト |
| rank / generation | 1386+k / 8091+k を **96/96**(k = 1…96)。最終 rank **1482** / gen **8187** |
| snapshot sha | `checker-result.snapshots[j].snapshot_sha256` = 実 `snapshots/*/start.json` の sha、**96/96** |
| `row_pairings_sha256 == sha(0x00 × rank_after)` | **96/96**(`e/physical/result.json` の `separator.direct_pairing` から)。<br>最終 rank 1482 → `e6f763f1858d097239395c80ac7d953aa0111988028facc0e60830a04f852ad6` = `checker-result.direct_pairing` と一致 |
| `lambda_pivots=0 / parent_remainder=1 / new_remainder=1` | **96/96** |
| λ_j · target_j = 1 | **96/96**(自前 trit 内積) |
| λ_j ⊥ (step ≤ j の全新規正規化行) | **96/96** |
| λ_final ⊥ 全 96 新規行 / λ_final · target_final = 1 | 成立 |
| λ_final / target_final の sha | `HEAD.lambda_sha256` `HEAD.target_remainder_sha256` と一致 |
| 正規化行の monic 性 | **96/96**(自分の lead で 1・lead 未満は全零) |
| checker replay | `status PASS` / `prefix_steps_replayed 96` / `snapshots 96` / `steps 96` / `physical_appends 96` / `checked_cursor.last_complete_phase = "physical"`(全 9 phase) |
| invocation | **4 件**(0→1 cap1 / 1→32 cap32 / 32→64 cap64 / **64→96 cap96 = 本 run**)。旧 3 件不変・新規ちょうど 1 件 |
| 出力の同一性 | `checker-result.json == checker-stdout.json`、`producer-result.json == output/result.json`、exit code 双方 `0` |

**再現できなかった部分(正直な申告)**: 受理済み **1386 base 行との λ 直交性は `state/physical.bin` 不在のため未再現**(2149/2154 限定を継続)。

## 4. ⑤ target.scalar 列 / lead

- **96 段の target.scalar**(instruction・checker steps・coverage-receipt の三者が一致):
  `[1,2,2,2,2,0,1,2,0,0,1,2,0,2,2,0,0,0,1,0,2,2,2,1,0,2,2,2,1,2,2,2,`
  `0,0,0,2,2,0,2,0,0,1,0,1,0,2,0,2,1,2,0,0,1,0,0,2,1,1,1,2,1,0,2,2,`
  `0,2,0,0,0,2,2,2,0,1,1,2,2,1,1,2,1,2,2,0,1,0,2,0,2,1,1,2,2,0,1,1]`
  **前 64 は 2154 で判読した親の列と完全一致**。全 96 の分布 **零 32 / 一 24 / 二 40**、新 32 は **零 9 / 一 10 / 二 13**。
- lead は **96 個すべて相異**・すべて character 0 ブロック内(< 12096)。範囲 **[1458, 1593]**(幅 136)。
  **新 32 の lead は {1562,…,1593} = 連続 32 座標そのもの**(隣接 3 組が入れ替わっているだけ)。前 64 は親と同一。

## 5. ⑤ 規約の実データ判別

### 5.1 target 減算の符号恒等式(**非空虚性の要**)

`lambda_rho2.identity_convention.all_one_row_steps` = `parent_remainder − child_remainder = target.scalar × accepted_normalized_row`
を、生 `target-remainder.bin` / `physical-normalized.bin` から自前 trit 演算で検算。

- **成立 95/95**(step 1–95)。
- **逆符号読み(`−scalar × row`)は 32/95 しか成立せず、その 32 は scalar = 0 の step と完全一致。**
- → **scalar ≠ 0 の 63 step が符号規約を判別している**(2154 の 40 step から増加)。ダミー(何にでも当たる試験)ではない。
- 恒等式の文字列も per-step `target_derivation.identity` = `parent_remainder - new_remainder = target.scalar * new_normalized_row` が **96/96 で単一**、
  checker 側 `identity_convention` の 3 文字列も親と同一。

### 5.2 修理三因子 ω / central 指数の全 96 列(`legality.omega` は読まない)

`output/snapshots/*/e/raw/raw-word.json` の **SLP node の `w` 値**から直接抽出。

| 量 | 全 96 | 新 32(step 64–95) | 参考: 前 64 |
|---|---|---|---|
| ω(w) 分布 | **0:39 / 1:31 / 2:26** | 0:10 / 1:11 / **2:11** | 0:29 / 1:20 / 2:15 |
| ω = 2 の step | 2,6,21,22,28,32,34,42,46,50,51,55,57,59,60,**67,71,77,81,82,84,86,88,90,93,95** | 11 件(**34.4 %**) | 15 件(23.4 %) |
| `repair-x` 指数 ≠ 0 | 59 / 96 | 18 / 32 | 41 / 64 |
| `repair-y` 指数 ≠ 0 | 58 / 96 | 18 / 32 | 40 / 64 |
| `repair-central` 指数 ≠ 0 | **57 / 96** | 22 / 32 | 35 / 64 |
| 三因子すべて 0 | 12 / 96 | 3 / 32 | 9 / 64 |
| **中心因子の単独実走**(x=y=0 かつ central=±1) | **13 step**(6,7,12,22,55,56,61,**67,72,81,85,86,93**) | 6 件 | 7 件 |
| `cen_pow == sr(ω)`(sr=[0,1,−1]) | **96/96 成立** | — | 64/64 |
| commutator 長 | **3048**(96/96)・repair-central ∈ {0, 3048}・r-x ∈ {0,3174,6348} / r-y ∈ {0,1398,2796} | — | 同 |
| raw-root SLP 長 | 34–12,328(96/96 で `actual == normalized`。上界検査は依然として恒真) | — | 同 |
| `legality.omega` / `epsilon_exact_zero` | 96/96 で 0 / true(**修理後 root のリテラル。三因子の実走の根拠に使ってはならない**) | — | 同 |
| 前 64 の ω/central 列 | **親と完全一致** | — | — |

- **F-cy-1 は 96 段でも完全に閉じている**。中心因子は **13 step で単独に**効いている。
- **ω = 2 は 26/96 へ増加し、新 32 では 34 %**。2150/2151 により物理行は規約非依存だが、
  **literal 受領証・rolling head・SLP 長は分岐する**。本 run のどの gate も両読みを区別しない点は不変。
  → 限定 (iii) の**重みは段数とともに増している**(注意喚起であって欠陥指摘ではない)。

## 6. ⑤ 情報性の内訳(character / tag / 補助チャネル)

すべて生 payload から自前算出(coverage-receipt の値は根拠に使っていない)。

| 量 | 全 96 |
|---|---|
| λ の台 | **96/96 で character 0 ブロックのみ**(char 1–3 は全 step 零)。char 0 内の非零 trit **892–1009**、λ_final = **985**(新 32 は 939–1009) |
| q の零 root | **96/96 で character 1,2,3 が完全零**。char 0 の非零 packed byte **1,053–1,152**(9,072 の最大 12.70 %)。新 32 は 1,101–1,152 |
| κ | **tag 0 のみ台**(d0 1,286–1,384 / d1 3,948–4,113)。**tag 1–5 は d0/d1 とも 96/96 で恒等零。shared aux 8 スロットも 96/96 全零** |
| score | 6 tag × 2 component の非零パターンは **96/96 で単一** — tag0 両 component 非零、tag1/tag2 は component 0 のみ、**tag3/4/5 は両 component 零** |
| `b-aux.u8` | **(0,0) が 96/96** |
| witness | **96/96 が `kind: "chord"`**(origin/seed 由来 0・auxiliary 分岐は 96/96 不発) |
| `basis_chords` | **96/96 で不変**(edge 2,3,4,6,11 = roster index 0,1,2,3,5) |
| `physical_lower_zero` / `source_lower_zero` | 96/96 `true` / 96/96 `NOT_ASSERTED` |
| `whole_word_direct_replay` / `target_word_direct_replay` / `eleven_slot_replay` | **96/96 すべて false**(982/983 の十一 slot 読み出しは本 run に含まれない) |
| `literal_outer_exponent` | −1 が **48** 件 / +1 が **48** 件 |
| `ρ₂` | `mode: derived` / `value: 1` / `original_rho2_directly_read: false`(96/96) |

**2149/2154 限定 (v) は 96 周回でも完全に不変。6 source tag のうち 3 本と補助チャネル全体は一度も励起されていない。**

---

## 7. 【独立節・重点】前進率の対照結果 — F-r64-1 の更新

`tree/chord-residuals.u8`(54,433 B × 96 段)から全列を直接測った。
**前 64 段の `residual_nonzero` 列・先頭 index 列は親と完全一致**(= 保存が数値レベルでも効いている)。

### 7.1 先頭失敗弦(witness)の roster index

| 量 | step 0–63 | step 64–95 | step 0–95 |
|---|---|---|---|
| 先頭 index | 4 → 69 | 70 → 99 | **4 → 99**(最大 **102** = step 94) |
| 最小二乗の傾き | **+1.0002 / step** | **+1.0024 / step** | **+1.0010 / step** |
| 後退遷移 | 18 / 63 | **5 / 32** | **23 / 95**(最大後退 −6) |
| 消化率 | 0.127 % | — | **99 / 54,433 = 0.1819 %** |

- **前進率は完全に安定**(1.00 弦/段)。加速も減速もしていない。
- 後退遷移の割合は 28.6 %(前 63)→ **15.6 %(後 32)**へ減った。ただし n=32 では有意差とは言えない。
- `failed_chord` の edge id は 10 → **193**、96 個すべて相異。

### 7.2 失敗弦の総数 — 【F-r64-1 の実質的な訂正】

| 量 | step 0–63 | step 64–95 | step 0–95 |
|---|---|---|---|
| 端点 | 36,134 → 36,259 | 36,274 → 36,292 | **36,134 → 36,292** |
| 平均 | 36,280.5 | 36,209.4 | 36,256.8(sd 107.2) |
| 32 段ブロック平均 | 36,315.5 | 36,245.4 | 36,209.4 |
| 最小二乗の傾き | −1.846(t=−2.66) | −1.850(t=−0.68) | **−1.602 ± 0.336(Newey-West t = −4.77)** |
| Mann-Kendall | — | — | **z = −4.03** |

**2154 の「失敗総数は横ばい(正味 +125)」は端点 2 点だけの読みで、96 観測では成り立たない。
残差の自己相関はほぼ 0(lag1 acf 0.08)なので OLS の se がそのまま使える。**

ただし**この減少の大半は機械的**である。先頭 index が 1/段で進むと、消化された弦がそのまま総数から 1 減る。分解すると:

| 区間 | step0 | step95 | 傾き | t |
|---|---|---|---|---|
| **消化 prefix**(index < 103) | 68 | **1** | −0.705 / step(機械的) | — |
| **固定 tail**(index ≥ 103) | 36,066 | 36,291 | **−0.919 ± 0.361** | **−2.55**(NW −2.72・block bootstrap で P(傾き≥0) = 0.001) |

- すなわち **prefix の消化(機械的)を除いても、なお ≈ 0.92 弦/段 の減少が残る**。
- ただしこれは**弱い信号**である: 96 段での予測総減少は −88 で、系列の sd(100.7)と同程度。
  さらに index band に分けると **[103, 27216) は完全に平坦(合計 −0.047・|t| < 0.7)、減少は [27216, 54433) に集中(−0.872・t = −2.95)**。
  上半分をさらに 4 分割すると最強でも t = −2.83 の band が 1 つで、鋭い局在ではなく**散漫な弱い傾き**。
  6 band の多重検定を考えれば p ≈ 0.02 程度。**「減っている」と断定する強さはない。**
- **消化 prefix はほぼ尽きた**(index < 103 に残る失敗弦は step95 で **1 本**)。次の数段で先頭 index は 103 の壁を越える。

### 7.3 外挿(線形外挿であって予言ではない)

| 経路 | 率 | roster 消し切りまで | 到達 rank |
|---|---|---|---|
| roster index の前進 | 1.001 弦/段 | **≈ 5.44 × 10⁴ 段** | ≈ 5.58 × 10⁴ |
| tail の失敗総数の減少 | 0.919 弦/段 | **≈ 3.94 × 10⁴ 段** | ≈ 4.08 × 10⁴ |

**2154 の外挿(≈5.3 × 10⁴ 段・rank ≈5.5 × 10⁴)は 96 観測で 3 % 以内で再現された。**
新たな tail 減少の経路を使っても同じ 10⁴ のオーダーで、**桁は動かない**。
非存在の証明ではない(失敗集合は毎段 λ ごとに再計算されるので一斉零化は排除されない)が、
**96 観測の範囲で収束の兆候は依然として無い**。

---

## 8. 資源の実測 — 【新発見 F-c96-1(重大・司令塔判断案件)】

### 8.1 実測時間と、これまでの「単価上昇」の否定

| invocation | prefix | append | producer 実秒 | prefix 1.34 s/step を差し引いた append 単価 |
|---|---|---|---|---|
| 0 → 1(cap 1) | 0 | 1 | 81.047 | 22.75 |
| 1 → 32(cap 32) | 1 | 31 | 763.238 | 22.70 |
| 32 → 64(cap 64) | 32 | 32 | 829.112 | 22.75 |
| **64 → 96(cap 96)** | 64 | 32 | **822.483** | **21.20** |

**2154 F-r64-1 の「append 単価 ≥ 25 s・rank と共に上昇中(+5.3 %)」は第三点で否定される。**
同一の分解定数(固定 58.3 s + prefix 1.34 s/step)を置くと単価は 22.75 / 22.70 / 22.75 / **21.20** で、
**rank 1387→1482 の 96 段を通じて平坦、最後の 32 段でむしろ 7 % 低下**した。私はこの訂正を明記する。

| checker | 段数 | 実秒 | 平均 | 限界(前 run 差分) |
|---|---|---|---|---|
| completion | 32 | 754.542 | 23.58 | — |
| resume64 | 64 | 1,462.749 | 22.86 | 22.13 |
| **control96** | 96 | **2,139.770** | **22.29** | **21.16** |

checker は**段数に線形**(限界 ≈ 21 s/段・固定 ≈ 50 s)で、単価はやはり微減。

本 run の枠内使用率: **producer 822.5 / 5,400 s = 15.2 %**、**checker 2,139.8 / 10,800 s = 19.8 %**、
job 3,249 s / 330 min = 16.4 %、vmem 7 GiB。**停止は完全に append 数 cap**(terminal = UNKNOWN_CAP かつ `count == cap` が gate)。

### 8.2 【重大】現行アーキテクチャの実際の天井は rank ≈ 1,890 であって 5 × 10⁴ ではない

checker は**毎回 start から全 prefix を再生する**。限界単価 21.16 s/段 から:

- **checker の内部 cap 10,800 s は ≈ 508 段(rank ≈ 1,894)で尽きる。**
- checker の外側 190 分(11,400 s)でも ≈ 538 段。
- job 330 分(19,800 s)は、cap M で append を M/2 とすると P ≈ 58 + 11.4 M、C ≈ 21.2 M、観測 overhead ≈ 300 s なので **M ≈ 597 が壁**。
- → **先に効くのは checker の 10,800 s で、実効的な天井は cap ≈ 500 / rank ≈ 1,890。**

さらに cap を倍々にして rank 5.4 × 10⁴ を目指した場合の**累積計算量**は、checker 側が
Σ 21.2 × (96 × 2ⁱ), i = 0..9 ≈ **2.1 × 10⁶ s ≈ 24 日**、producer 側が 5.4 × 10⁴ × 21.5 ≈ **1.2 × 10⁶ s ≈ 14 日**。
**合計 ≈ 38 日の純計算**(2154 の「producer だけで ≥ 15 日」より広い)、かつ **1 job 330 分の壁により 200 run 超**が要る。

**司令塔への一行**: 撤退条件は段数 cap ではなく、(a) 実測前進率 1.00 弦/段(安定)、(b) tail 減少 0.92 弦/段(弱い)、
(c) **現行 full-prefix-replay checker の構造的天井 rank ≈ 1,890** の三つで書くのが妥当。
rank 5 × 10⁴ に届かせるには checker の全 prefix 再生をやめる(増分検証)か、
検証を段階的 anchor に切る設計変更が要る — これは計算資源の問題ではなく**設計の問題**である。

---

## 9. 新規発見・継続所見

### 9.1 【要修正 F-c96-2】`result.json` の `new_physical_appends` は依然として累積(2154 F-r64-3 の継続)

`output/result.json`: `new_physical_appends: 96` / `max_appends_this_invocation: 96` — どちらも**累積・絶対値**。
本 invocation の実 append は **32**(`run-receipt.json` の `new_appends_this_run: 32` が正しい字段)。
Astra は express で正しく区別しているが、**下流が result.json だけを読むと「本 run で 96 段進んだ」と誤読する**。字段名の是正を継続推奨。

### 9.2 【軽微 F-c96-3】candidate と diagnostics は同一 path の二重 upload

workflow は candidate(`if: success()`)と diagnostics(`if: always()`)に**同じ `${{ runner.temp }}/resume-next/` を渡している**。
実際に両 artifact は **608,103,877 B で同一バイト数**(digest が違うのは upload-artifact の ZIP が再現的でないため)。
すなわち diagnostics は candidate に無い情報を持たず、逆に candidate は log も pending も全部含む。
gate 通過の区別は artifact **名**と、内部の `run-receipt.json`(final gate 通過時のみ生成)でしか付かない。
名前で認証する resume-next 契約では実害はないが、**「診断は別物」という説明は実態と違う**ので記述を合わせるべき。

### 9.3 【軽微 F-c96-4】alias 逆対照は依然 pin 継承 — ただし動的証拠は 96 段でより強い

`snapshot-isolation-selftest.json` は本 run で**再走されていない**(`rerun: false`。sha は親実体と一致を確認)。
しかし本 run 自身が動的に覆っている: `checker-result.start_sha256` = `87bd9b89…`(**parents 33 件版**で凍結)である一方、
per-step の `accepted_target_derivation_parents` は **33 → 128** と伸び、最終 checker の同リストは **129 件 = 33 + 96**。
**start は凍り current は 129 まで伸びた。** 格付け文面では pin ではなくこちらを根拠に挙げるべき(2154 §6.4 と同じ結論)。

### 9.4 【軽微 F-c96-5】target.scalar = 0 が 96 中 32 段

零 scalar の段は §5.1 の恒等式より **target remainder を一切動かさない**(rank と λ は動く)。
新 32 では 9/32(28.1 %)で、前 32(43.8 %)より下がり、全体では 33.3 %。
§7 と併せて「rank は伸びるが target への接近は起きていない」という描像は不変。事実の提示に留める。

### 9.5 workflow の jq gate は消えた(2154 F-r64-2 の解消)

resume64-v1 にあった 13 連言の jq gate(PASS 側恒真)は **resume-next-v1 には存在しない**(`jq -e` の出現 0)。
代わりに `final_mode` が **データ依存の結合検査**を持つ:
`coverage["target_scalars"] == [row["target_scalar"] for row in checked["steps"]]` と
`coverage == checked == head == produced` の completed_steps 一致。**F-r64-2 は解消済み。**

---

## 10. 実測値の一覧(Astra 申告との突合)

| 項目 | Astra 申告 | 判読者の独立再導出 | 一致 |
|---|---|---|---|
| ZIP bytes / sha256 | 608,103,877 / `5ec5667b77a3ed78…` | 同(自前 DL + API digest) | ✔ |
| diagnostics | 608,103,877 / `b018a2d9151fba18…` | API のみ確認・**未回収**(§9.2 により候補と同内容) | ✔ |
| P step 22:26:32Z–22:40:18Z | 主張 | producer 内部 **822.482748 s**(finished 22:40:14Z) | ✔ |
| 全 C step 22:40:18Z–23:15:58Z | 主張 | checker 内部 **2,139.769708 s** | ✔ |
| rank / gen / terminal | (payload 未回収で未記帳) | **1482 / 8187 / UNKNOWN_CAP / Separator** | 新規 |
| 追加 append | (未記帳) | **32**(before 64 → 96) | 新規 |
| current snapshot / checkpoint / oracle | — | **null / null / null** | 新規 |
| 旧 64 保全 | 「維持」 | **共通 5,145 中 5,143 がバイト同一**、変化は HEAD と result.json のみ | ✔ |
| 全 output | — | 7,706 file / 1,252 dir / 1,028,793,851 B | 新規 |
| P / C sha | 不変 | repo 作業ツリー・起動 commit とバイト一致 | ✔ |
| 全 target 差分符号 | 依頼 | **95/95 成立・逆符号 32/95 は scalar 0 のみ → 63 step が判別** | ✔ |
| 中央項 | 依頼 | **cen = sr(ω) 96/96・単独実走 13 step** | ✔ |
| 全失敗数・先頭 index 全列 | 依頼 | §7 に全列 | ✔ |
| selection / final lambda / q 全 character | 依頼 | §6(λ・q とも char 1–3 は 96/96 零) | ✔ |
| κ 各 tag / aux | 依頼 | §6(tag 1–5 と shared aux は 96/96 恒等零) | ✔ |

---

## 11. CV-9 裁定案・工房格付け案(一行)

> **CV-9 = 同一対象(限定 8 条)。工房格 = checker PASS(算術 source sha 無変更・新規算術 module なし・交差辺 0・
> 96 段の head 連鎖 / target.scalar / row_pairings / λ 直交 / 符号恒等式 / ω・central / q・κ・score・aux・witness・basis を
> 非当事者が生バイトから第三実装で全数再導出し一致・親 output 5,145 file 中 5,143 file の不変と埋め込み親 7,916 file の
> バイト全一致を独立取得の親 ZIP に対して再 hash して確認・ZIP 実体と展開忠実度も再検算・
> 事前登録 dispatch 入力とのバイト一致・入力契約 canary は 8 変異全拒否 + 実入力通過の陽陰両対照・
> cap は append 数のみで producer 15.2 % / checker 19.8 %)・cross-checked は限定 8 条つき** —
> (i) 射程 = rank 1450 → **1482** の 32 周回(累積 96 段)・**rank 1482 の λ に対する oracle 計算は存在しない**
>   (`current_snapshot/checkpoint/oracle_terminal = null`)・依然 Separator・MEMBER/NONMEMBER いずれでもない
> (ii) **F-cy-1 は 96 段でも完全閉鎖**(三因子実走 x 59/96・y 58/96・central 57/96、**中心因子は 13 step で単独実走**)
> (iii) **ω = 2 は 26/96 へ増加(新 32 では 34 %)**。2150/2151 により物理行は規約非依存だが
>   **literal 受領証・rolling head・SLP 長は規約で分岐する**・本 run のどの gate も両読みを区別しない(不変・重みは増大)
> (iv) informative は character 0 のみ(q char1–3 は 96/96 完全零・λ の台は 96/96 で char 0 内 892–1009 trit・
>   lead は [1458,1593] の幅 136 窓、新 32 は連続 32 座標 {1562..1593})
> (v) κ は tag 0 のみ台・tag1–5 と shared aux は 96/96 恒等零・score tag3–5 も 96/96 零・`b_aux` も 96/96 零
>   (auxiliary witness 分岐は一度も不発火)
> (vi) **探索射程**: 弦は毎段**全 54,433 が評価**され、witness は roster 順の**先頭失敗弦**。
>   **96 段で index 4 → 99(+1.001/段・23/95 が後退)・消化 0.182 %・
>   失敗総数は −1.60/段(t=−4.8)で減るが、その 0.70/段 は消化の機械的効果で、
>   固定 tail の減少 0.92/段(t=−2.6)は弱く散漫**・basis は 96/96 で固定
> (vii) 独立性は最深部で単一系統(継承クローン load-bearing)・**算術 TCB は不変だが harness TCB は新規**
>   (workflow 109,035 B + inline `driver.py` 83,342 B は単著・独立検査なし。判読はこの出力に依存していない)
> (viii) λ ⊥ 受理済 1386 base 行は `state/physical.bin` 不在で判読者未再現・λ·ρ₂ は DERIVED・
>   **事前試験 6 件(alias 逆対照を含む)は再走ではなく sha pin による継承**
>   (ただし alias 修理の有効性は §9.3 の動的証拠 = start が 33 親で凍結・per-step 33→128・final 129 で成立)
> GRADE2 NOT_DECIDED・full_A0 false・verified=false。
> **正式受理 1450 を維持し 1482 を候補とする Astra の境界維持は妥当**であり、
> CV-9 の観点からは 1482 の受理を妨げる材料は見つからなかった(受理の可否は司令塔の裁定)。

---

## 12. 判読者の限界(正直な申告)

- 受理済み **1386 base 行との λ 直交性は `state/physical.bin` 不在のため再計算していない**。
- 各 phase の算術本体(section/cochain/tree/raw/source/primal/p1/B)は checker が producer バイトと突合した結果を受け入れており、
  **私が第三実装で再計算したのは §3–§7・§10 の表に挙げた量のみ**。
- §7.3・§8.2 の外挿は**現在の観測率の線形外挿であって予言ではない**。失敗集合は毎段再計算されるため、
  ある段での一斉零化は**この観測からは排除されない**。§8.2 の日数見積りも現行設計を前提とした算術で、設計変更で無効になる。
- §7.2 の tail 減少は **t ≈ −2.6・96 観測**の弱い信号で、band 分解では鋭い局在を示さない。
  **「減少している」と断定していない**し、逆に 2154 の「横ばい」も 96 観測では支持できない、という両面の報告である。
- ω = 2 の 26 行が同じ物理行を与えるか否かは 2150/2151 の数学裁定に依拠しており、**私は独立に検証していない**(CV-9 スコープ外)。
- 「この観点では穴を見つけられなかった」は**保証ではない**。特に再 hash されない alias の不在は依然として証明されていない(2149 F-al-2 を継続)。
- 本 run の gate 自体(`driver.py`)は単著・未レビューであり、私はその出力を根拠に採らなかったが、**gate の正しさそのものは監査していない**。

---

判読ファイル: `C:\Users\81905\Desktop\shadow-atelier\scratchpad\fal_cv9_control96_report_v1.md`


sha256(this file, excluding this line) = ea7e834d302f3cc7
