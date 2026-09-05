# 増分 CV-9 判読 — complete oracle CEGAR resume64 v1(実 64 段・rank 1450 候補)

対象: producer/checker run **33990567016/1**(success・P 一回 829.112209 s・C 一回 1462.7485207660002 s・PASS)
候補 artifact **9977040548**(`d972-r07-complete-oracle-cegar-resume64-v1-candidate-33990567016-1`)
判読者: falsifier(非当事者・事後)。判読日 2026-09-06。
親裁定: 2131 / 2138 / 2143 / 2144 / 2145 / **2149**(限定 8)/ **2150**(ω 規約非依存・rank 1418 受理)/ **2151**(SLP 長 3048 訂正)。
判読規律: 2149 §9 の改訂規律(①②③ = source sha 無変更 1 行・⑤ に 3 項追加)+ Astra 依頼(`ops/express/20260906_astra_fable_cegar_resume64_cv9.md`)。

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 8 条(§8 で 2149 版から更新)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 8 条つき)。`verified=false`。GRADE2 NOT_DECIDED。**

同一性の根拠は今回、規約宣言の diff ではなく**規約の実データ判別**で取れた:

- 修理三因子の指数が 64/64 で `sr(ω)`(signed)に一致(§4.1)。
- **target 減算の符号規約が実データで判別可能**: `親 remainder − 子 remainder = target.scalar × 正規化行`(mod 3)を自前 trit 演算で **63/63 再現**、逆符号読みは **23/63** しか成立せず、その 23 は **scalar = 0 の step と完全一致**。すなわち **scalar ≠ 0 の 40 step は符号規約を判別している**(§4.2)。ω 規約(§4.1)が本 run のどの gate でも判別できないのと対照的で、「何にでも当たる試験」ではない。
- cap の意味論が両側で累積(cumulative)に揃っている(P `d972_r07_complete_oracle_cegar_continuation_v1.py:1447,1661` / C `check_d972_r07_complete_oracle_cegar_continuation_v2.py:1151,1440 "cumulative_cap_carried_across_resume"`)。

**ただし本判読で 1 件の重大な発見がある(§6.1)。CV-9 の同一性は揺るがないが、キャンペーンの cap 梯子(32→64→128)と撤退条件の書き方に直接効く。**

---

## 1. ①②③(source sha 無変更・1 行規律)

- **20 source(P 系 9 + C 系 10 + 修理 C v2)がすべて repo 作業ツリーとバイト一致。mismatch 0 / missing 0。**
  producer `search/d972_r07_complete_oracle_cegar_continuation_v1.py` = 126,940 B / `67d2302c3c4d571a…`、
  checker `search/check_d972_r07_complete_oracle_cegar_continuation_v2.py` = 129,557 B / `e985b4ca3922fc4f…`。
- `source-receipt.json` は**前周回 completion artifact のものとバイト同一**(両者 `3a50dd12025079a6…`)。データ pin 3 本も同一。
- `executed-sources/` は 22 件 = 上記 20 + workflow 2 本(continuation-v1.yml / resume64-v1.yml)。20 件は receipt と全一致。
- 交差辺の再確認(安価なので実施): producer が `check_*` を import する箇所 **0**、checker が `d972_*` を import / 動的 load する箇所 **0**。新規 module の TCB 流入なし。

→ **①②③ は「両側 source sha 無変更・新規 module なし」で省略が妥当。**

## 2. 入力 pin と保存宇宙(⑤ 前段)

| 検査 | 結果 |
|---|---|
| 候補 ZIP 実体 | **304,642,285 B / `a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792`** = Astra F8.55 一致 |
| ZIP entry 数 / 展開忠実度 | 7,916 entry・展開ツリーと ZIP の**不一致 0 / 欠落 0**(非圧縮計 1,046,747,777 B)・**unsafe path 0 / symlink 0** |
| 親 = accepted completion | run 33988391926 / artifact **9976060093** / `sha256:9f51b038…`(前周回で判読済の実体) |
| 埋め込み `accepted-completion/` | **2,699 file / 352,403,548 B が、前回私が独立展開した completion candidate とバイト全一致**(mismatch 0) |
| `before32/HEAD` `before32/result.json` | 親 `output/` の同名ファイルとバイト同一・rank 1418 / gen 8123 / completed 32 / Separator |
| 旧 output の不変 | 親と共通 **2,584 file** のうち**変化は HEAD と result.json の 2 件のみ** → **旧不変 2,582 file**(比較 346,724,717 B)。Astra 申告と一致 |
| 新 output roster | **5,145 file / 836 dir / 686,612,253 B**(自前 walk)= run-receipt・Astra 申告と一致 |
| 新規分 | snapshot 32 dir(000032–000063)・step 32 dir・**invocation 1 件のみ**(`2c723e694ab1425c…`)。他に新規ファイルなし |
| live parents | 15 = 元 14 + completion。P1 = `task809-canonical-p1-degree2-lift-v9`(9931437113)、Task712 = `fixed-root-packet-loop-v2`(9969090590)、Task554 grade1 block ×5(`task554_accepted_failure: true`)|
| 事前試験の継承 | `prior_tests_authenticated_without_rerun` 6 件(oracle-v2-full / producer-selftest / checker-selftest / producer-parent-layout / checker-parent-layout / **snapshot-isolation-selftest**)。**6 件とも sha を埋め込み親の実体と突合して一致**。全件 `rerun: false` と正直に記帳 |

## 3. ④ 終端受領証・head 連鎖(64/64)

自前実装(project module を一切 import せず canonical/sha/pack/unpack/dot を独立実装)で生バイトから再導出。

| 検査 | 結果 |
|---|---|
| head 連鎖 `sha(bytes.fromhex(prev)+canonical(instruction−rolling))` | **64/64 一致**、終端 `076c4b9df33957b090a7bf698e4dd1100e85350cfff86f88eb9ab12a39fdb667` = HEAD / result / checker-result |
| **前 32 head の同一性** | 前周回(rank 1418 受理分)の head 列と**32/32 バイト一致**、index 31 = `0c2451e45fb1859f…` |
| rank / generation | 1386+j+1 / 8091+j+1 を 64/64 |
| `row_pairings_sha256 == sha(0x00 × rank_after)` | **64/64**。最終 rank 1450 = `1db92b26f408ddb6f3ac47574cd49cf4dc131efa8090477bf6d0a5feea4bdf1c` = checker-result.direct_pairing と一致 |
| `lambda_pivots=0 / parent_remainder=1 / new_remainder=1` | 64/64 |
| λ_j · target_j = 1 | **64/64**(自前 trit 内積) |
| λ_j ⊥ (step ≤ j の全新規正規化行) | **64/64** |
| λ_final ⊥ 全 64 新規行、λ_final · target_final = 1 | 成立 |
| λ_final / target_final の sha | HEAD の `lambda_sha256` `target_remainder_sha256` と一致 |
| checker の replay 配列 | `snapshots` 64 件 / `steps` 64 件、`snapshot_sha256` は実 `snapshots/*/start.json` と 64/64 一致 |

**再現できなかった部分(正直な申告)**: 受理済み **1386 base 行との直交性は本 artifact に `state/physical.bin` が存在しないため未再現**(2149 限定 (viii) を継続)。

## 4. ⑤ 規約の実データ判別

### 4.1 修理三因子 ω / central 指数の全 64 列(`legality.omega` は読まない)

`output/snapshots/*/e/raw/raw-word.json` の **SLP node の `w` 値**から直接抽出。

| 量 | 全 64 | 新 32(step 32–63) |
|---|---|---|
| ω(w) 分布 | **0:29 / 1:20 / 2:15** | 0:12 / 1:10 / **2:10** |
| ω = 2 の step | 2,6,21,22,28,**32,34,42,46,50,51,55,57,59,60** | 10 件 |
| `repair-x` 指数 ≠ 0 | 41 / 64 | 23 / 32 |
| `repair-y` 指数 ≠ 0 | 40 / 64 | 25 / 32 |
| `repair-central` 指数 ≠ 0 | **35 / 64** | 20 / 32 |
| 三因子すべて 0 | 9 / 64(旧 8 + step 53) | 1 / 32 |
| **中心因子の単独実走**(x=y=0 かつ central=±1) | **7 step**(6,7,12,22,**55,56,61**) | 3 件 |
| `cen_pow == sr(ω)`(sr=[0,1,−1]) | **64/64 成立** | — |
| commutator 長 | **3048**(64/64)・repair-central 長 ∈ {0, 3048}・r-x=1058 / r-y=466 | 2151 訂正と一致 |
| `actual_slp_length == normalized` | 64/64(値域 34–12,328)。上界検査は依然として恒真 | — |
| `legality.omega` / `epsilon_exact_zero` | 64/64 で 0 / true(**修理後 root のリテラル。三因子の実走の根拠に使ってはならない**) | — |

- **F-cy-1 は完全に閉じた**。しかも中心因子は 7 step で**単独に**効いており、「他因子に紛れて動いただけ」ではない。
- **ω = 2 は 15 step へ増加**(2149 時点は 5)。裁定 2150/2151 により物理行は規約非依存だが、**literal 受領証・rolling head・SLP 長は分岐する**。本 run のどの gate も両読みを区別しない点は不変(mod 3 legality は e ≡ 2 で両立・語長上界式は signed 前提)。

### 4.2 【新】target 減算規約は実データで判別されている

`lambda_rho2.identity_convention.all_one_row_steps` = `parent_remainder − child_remainder = target.scalar × accepted_normalized_row` を、
生 `target-remainder.bin` / `physical-normalized.bin` から自前 trit 演算で検算した。

- **成立 63/63**(step 1–63)。
- **逆符号読み(`−scalar × row`)は 23/63 しか成立せず、その 23 は scalar = 0 の step と完全一致。**
- したがって **scalar ≠ 0 の 40 step が符号規約を判別している**。ダミー(何にでも当たる)ではない。
- 併せて「正規化行は自分の lead で monic・lead 未満は全零」を 64/64 確認。

### 4.3 target.scalar 列 / lead

- **新 32 の target.scalar = Astra F8.55 の実列と完全一致**
  `[0,0,0,2,2,0,2,0,0,1,0,1,0,2,0,2,1,2,0,0,1,0,0,2,1,1,1,2,1,0,2,2]`(零 14 / 一 8 / 二 10)。
- 前 32 は受理済み 1418 run の列と一致。全 64 では 零 23 / 一 14 / 二 27。
- lead は 64 個すべて相異・すべて char 0 ブロック内(< 12096)。範囲 **[1458, 1561]**(2149 時点は幅 72 → 今回 幅 104)。
  **新 32 の lead は {1530,…,1561} = 連続 32 座標そのもの**(隣接 2 組が入れ替わっているだけ)。

### 4.4 λ の character 別台

- **λ の台は 64/64 で character 0 ブロック内のみ**(char 1–3 は全 step 零)。char 0 内の非零 trit は **892–993**、λ_final は 960。
- q.bin は **64/64 で character 1,2,3 が完全零**。char 0 の非零 packed byte は 1,053–1,125(9,072 の最大 **12.40 %**)。
- **2149 限定 (iv) は継続**(rank が 1418→1450 に伸びても char 1–3 に台は出ていない)。

### 4.5 failed_chord / basis の変化

- witness は **64/64 が `kind: "chord"`**(origin/seed 由来 0・auxiliary 分岐は 64/64 で不発 = `b_aux` が常に (0,0))。
- `failed_chord`(edge id)は **10 → 122**(前 32 は 10–62、新 32 は 58–122)。64 個すべて相異。
- **`basis_chords` は 64/64 で不変の (2,3,4,6,11)**。`basis_coefficients` は 36 種。
- `eta = [0,0]` / `tau = [0,0,0,0,0]` / `materialization = MATERIALIZATION_PENDING` が 64/64。cycles は 6 個・係数 0 も保持(規約どおり)。

### 4.6 κ / score / aux の内訳(**本 run には coverage 集計 file が無いので判読者が実 snapshot から新規算出**)

親 `coverage-receipt.json` の layout(`d0 = 文字 major × 6 tag × 1008` / `d1 = 24192 + 文字 major × 6 tag × 3024` / 末尾 8 が shared aux)を**旧 32 行の receipt 値と突合して検証(32/32 一致)**したうえで、新 32 に適用。

- κ: **tag 0 のみ台**(d0 1,286–1,381 / d1 3,948–4,113)。**tag 1–5 は d0/d1 とも 64/64 で恒等零。shared aux 8 スロットも 64/64 全零。**
- score: 6 tag × 2 component の非零パターンは **64/64 で単一** — tag0 は両 component 非零、tag1/tag2 は component 0 のみ、**tag3/4/5 は両 component 零**。
- `b-aux.u8` = (0,0) が 64/64。
- **2149 限定 (v) は 64 周回でも完全に不変**。6 source tag のうち 3 本と補助チャネル全体は一度も励起されていない。

## 5. UNKNOWN_CAP の性質と資源

- terminal = **UNKNOWN_CAP**。`cap_reached(completed_steps, max_appends)` は**累積**判定(P `:1447`)。C も `result["completed_steps"] - before <= max(0, value["max_appends"] - before)`(v2 `:1440`)で累積を要求 = **両側の cap 意味論は一致**。
- 実測: **producer 829.112209 s / 内 5,400 s(15.4 %)・外 100 分**、**checker 1,462.7485 s / 内 10,800 s(13.5 %)・外 190 分**、job 330 分、vmem 7 GiB。
  → **停止は完全に append 数 cap。時間・資源には一切余裕がある**(UNKNOWN_RESOURCE ではない)。
- invocation は 3 件(cap1/resume=false、cap32/resume、**cap64/resume・本 run**)。owner / source / start / fixed manifest は 3 件とも同一。

## 6. 新規発見

### 6.1 【重大 F-r64-1】CEGAR の前進率が測定できた — 64 段で roster の 0.127 %、失敗弦の総数は減っていない

`tree/chord-residuals.u8`(54,433 B)から直接測った。

| 量 | 実測 |
|---|---|
| 各 step で評価される弦 | **全 54,433**(`full_chord_eof: true`・`np.all(np.diff(chords) > 0)`・残差恒等式を私も再計算して一致)。**探索の cap ではない** |
| `residual_nonzero`(失敗弦の総数) | **35,992 – 36,549**(= 66.12 – 67.15 %)。step0 36,134 → step63 36,259、**正味 +125。減少していない** |
| 先頭失敗弦の **roster index** | step0 **4** → step63 **69**。64 段で **+65 = 1.03 / step** |
| 単調性 | **単調でない。63 遷移中 18 回が後退**(最大 −6)。一度消した弦が λ の更新で再び失敗する |
| 消化済み prefix の割合 | 69 / 54,433 = **0.12676 %** |
| 未消化 tail の失敗密度 | step0 66.39 % → step63 66.70 %(**改善なし**) |

**含意(算術のみ。数学的な可否判断は CV-9 スコープ外)**:
この機構の前進は「roster 先頭から 1 段あたり約 1 弦を消す」であり、rank は 1 段あたり 1 増える。
この率のまま roster を消し切るには **約 5.3 × 10⁴ 段(rank ≈ 5.5 × 10⁴)** が要る。
実測 append 単価は rank 1387–1418 で 24.6 s、rank 1419–1450 で 25.9 s(**32 rank で +5.3 %、rank と共に上昇中**)。
定数 25 s と仮定してすら producer 実時間だけで **≥ 1.3 × 10⁶ s ≈ 15 日**、実際は単価上昇でそれ以上。

**ただし非存在の証明ではない**: 失敗集合は毎段 λ ごとに再計算されるので、原理的にはある 1 段で一斉に零になり得る。
64 観測の範囲で**収束の兆候が無い**という事実の報告に留める。

**司令塔への一行**: 撤退条件を「段数 cap」ではなく**この実測前進率(弦/段)と失敗総数の趨勢**で書き直すのが妥当。cap 128 は資源的には楽勝(下記)だが、この率では 128 段でも roster の 0.25 % に届かない。

参考(外挿・予測であって記帳値ではない): checker は毎回 start から全 prefix を再生するので **22.9–23.6 s/step** で線形 → cap 128 で ≈ 2,900–3,000 s(内 10,800 s の 27 %)。
producer は「prefix 読み ≈ 1.34 s/step + append ≈ 24.6 s/append」で分解でき、cap 128(64 append)で ≈ 1,700 s(内 5,400 s の 31 %)。
**producer の内 5,400 s が効き始めるのは概ね cap 256–300 付近**(append 単価が rank と共に上がるため、それより早い可能性がある)。

### 6.2 【要修正 F-r64-2】workflow jq gate の 13 連言は PASS 側で恒真 — ただし 2149 F-co-2 の私の書き方を訂正する

`check_d972_r07_complete_oracle_cegar_continuation_v2.py:1493–1500` は
`full_four_character_scope: True` / `section_equalities_each: 8059` / `chords_each: CHORDS` / `auxiliary_tests_each: 2` /
`ordinary27_actual_source: True` / `source_lower_trits_each_E: LOWER` / `literal_modulus: 54` / `all_four_B_summed_each_E: True` /
`external_e_attached: 1` / `whole_normalized_word_replay: False` / `eleven_slot_replay: False` / `grade2_*: "NOT_DECIDED"` / `full_A0: False`
を**すべてリテラルで書く**。`d972-r07-complete-oracle-cegar-resume64-v1.yml:936–950` の jq gate はまさにこれらを検査する = **PASS 側では判別能力ゼロ**。

**2149 での私の記述の訂正**: 「測定されていない」は言い過ぎだった。等価な非空虚検査が別所にある —
`check_d972_r07_complete_oracle_cegar_continuation_v2.py:894–897`(`oracle_snapshot_join`)が producer の各 step の `oracle-result.json` に対して
`section_equalities == 8059 / chords_checked == CHORDS / auxiliary_tests == 2` を要求し、
同 `:941–942` で checker が独立に組んだ document と producer の保存バイトを**バイト比較**している。
さらに数値自体は**データの形で裏付けられる**: 私の実測で `section/equation-values.u8` = 8,059 B、`tree/chord-residuals.u8` = 54,433 B、`cochain/b-aux.u8` = 2 B。
→ **gate は冗長であって根拠欠落ではない**。字段名の改名(`four_character_bytes_compared` 等)か gate からの除去を推奨、という結論は維持。

### 6.3 【軽微 F-r64-3】`max_appends_this_invocation` は誤称 — result.json 単独で読むと本 run の作業量を誤る

`result.json` の `new_physical_appends: 64` は**累積**、`max_appends_this_invocation: 64` は**絶対 cap**。
本 invocation の実 append は **32**(`run-receipt.json` の `new_appends_this_run: 32` が正しい字段)。
Astra は F8.55 で正しく区別しているが、**下流が result.json だけを読むと「本 run で 64 段進んだ」と誤読する**。字段名の是正を推奨。

### 6.4 【軽微 F-r64-4】alias 逆対照は pin 継承 — ただし本 run には**より強い動的証拠**がある

`snapshot-isolation-selftest.json`(旧 alias パターンの逆対照・`legacy_alias_control_detected: true`)は本 run で**再走されていない**
(`prior_tests_authenticated_without_rerun`、`rerun: false`。6 件とも sha を埋め込み親と突合して一致は確認済み)。
alias 欠陥は**状態依存**(v1 では親リストが 33→65 に伸びた末尾の再 hash で初めて露見した)なので、32 段で走らせた pin 済み対照は 64 段を覆わない。

**しかし本 run 自身が動的に覆っている**: 私の実測で
`checker-result.start_sha256` = `87bd9b89c593d68f…` = `sha(canonical(output/start.json))`(**parents 33 件版**)である一方、
`checker-result.lambda_rho2.accepted_target_derivation_parents` = **97 件**(= 33 + 64)。
**start は凍り current は 97 まで伸びた**。これは 2149 §5.3 の意味論が 64 段でも保たれている直接証拠であり、
pin された対照より強い。**格付け文面では pin ではなくこちらを根拠に挙げるべき。**

### 6.5 【軽微 F-r64-5】target.scalar = 0 が 64 中 23 段

零 scalar の段は §4.2 の恒等式より **target remainder を一切動かさない**(rank と λ は動く)。
新 32 では 14/32(43.8 %)と旧 32 の 9/32(28.1 %)より増えている。§6.1 と併せて、
**「rank は伸びるが target への接近は起きていない」**という描像と整合する。事実の提示に留める。

### 6.6 【軽微 F-r64-6】lead の局所性・未実行の読み出し

新 32 の pivot lead は **{1530,…,1561} = 連続 32 座標**。全 64 で [1458, 1561](幅 104、PHYSICAL 48,384 の 0.21 %)。
`physical-literal` の `literal_outer_exponent` は −1 が 33 件 / +1 が 31 件、`physical_lower_zero` は 64/64 true、
`source_lower_zero` は 64/64 `NOT_ASSERTED`、`whole_word_direct_replay` / `target_word_direct_replay` / `eleven_slot_replay` は **64/64 false**
(= 982/983 の十一 slot 読み出しは本 run に含まれない。Astra の申告どおり)。

---

## 7. 実測値の一覧(Astra 申告との突合)

| 項目 | Astra 申告 | 判読者の独立再導出 | 一致 |
|---|---|---|---|
| ZIP bytes / sha256 | 304,642,285 / `a7ecd56dba33e354…` | 同 | ✔ |
| 実 entry | 7,916 | 7,916(展開忠実度 100 %) | ✔ |
| rank / gen / terminal | 1450 / 8155 / UNKNOWN_CAP / Separator | 同 | ✔ |
| 新 32 target scalar | 上記 32 個 | 同(生 `result.json` から) | ✔ |
| current snapshot / checkpoint | null / null | null / null(`current_oracle_terminal` も null) | ✔ |
| 最終 λ の 1450 行 pairing 零 / target 1 | 主張 | `sha(0x00×1450)` 一致・λ⊥新 64 行・λ·target=1 を再現(base 1386 行は未再現) | ✔(限定) |
| ρ₂ | DERIVED 値 1 | `mode: "derived"` / `original_rho2_directly_read: false` | ✔ |
| 全 output | 5,145 file / 836 dir / 686,612,253 B | 同 | ✔ |
| 元 completion | 2,699 file | 2,699 file / 352,403,548 B バイト全一致 | ✔ |
| 旧不変 | 2,582 file | 共通 2,584 のうち変化は HEAD と result.json のみ | ✔ |
| P / C sha | `67d2302c…` / `e985b4ca…` | repo 作業ツリーとバイト一致 | ✔ |
| checker-result | 330,955 B / `ff55c51e…` | 同 | ✔ |
| q char0 非零 packed byte(新 32) | (未申告) | `[1104,1089,1089,1089,1089,1092,1095,1107,1104,1086,1101,1104,1113,1104,1092,1104,1116,1095,1113,1098,1113,1119,1119,1101,1113,1104,1113,1098,1119,1113,1101,1125]` | 新規 |

diagnostics 9977050602 は Astra が「API のみ確認・別 ZIP・回収済とは書かない」と正しく区別しており、私も回収していない。

---

## 8. CV-9 裁定案・工房格付け案(一行)

> **CV-9 = 同一対象(限定 8 条)。工房格 = checker PASS(source sha 無変更・新規 module なし・交差辺 0・64 段の head 連鎖 / target.scalar / row_pairings / λ 直交 / q・κ・score・aux・witness を非当事者が生バイトから第三実装で全数再導出し一致・親 completion 2,699 file と旧不変 2,582 file を全数再 hash して不変を確認・ZIP 実体と展開忠実度も再検算・cap は append 数のみで producer 15.4 % / checker 13.5 %)・cross-checked は限定 8 条つき** —
> (i) 射程 = rank 1386 → **1450** の 64 周回のみ・**rank 1450 の λ に対する oracle 計算は存在しない**(`current_snapshot/checkpoint/oracle_terminal = null`)・依然 Separator・MEMBER/NONMEMBER いずれでもない
> (ii) **F-cy-1 は完全閉鎖**(三因子実走 x 41/64・y 40/64・central 35/64、**中心因子は 7 step で単独実走**)
> (iii) **ω = 2 は 15/64 へ増加**(2149 時点 5/32)。2150/2151 により物理行は規約非依存だが **literal 受領証・rolling head・SLP 長は規約で分岐する**・本 run のどの gate も両読みを区別しない(不変)
> (iv) informative は character 0 のみ(q char1–3 は 64/64 完全零・λ の台は 64/64 で char 0 内 892–993 trit・lead は [1458,1561] の幅 104 窓、新 32 は連続 32 座標)
> (v) κ は tag 0 のみ台・tag1–5 と shared aux は 64/64 恒等零・score tag3–5 も 64/64 零・`b_aux`/`eta`/`tau` も 64/64 零(auxiliary witness 分岐は一度も不発火)
> (vi) **探索射程の訂正**: 弦は毎段 **全 54,433 が評価されている**(cap ではない)。狭いのは witness = roster 順の**先頭失敗弦**であり、**64 段で roster index 4 → 69(+1.03/段・18/63 が後退)・消化 0.127 %・失敗総数は 66–67 % で横ばい(正味 +125)**・basis は 64/64 で固定 (2,3,4,6,11)
> (vii) 独立性は最深部で単一系統(`read_task712_envelope` 1.0000・`vectorized_projection_chunk` 0.99・`sparse_adjoint` バイト同一)・本 run で新規 module の TCB 流入なし
> (viii) λ ⊥ 受理済 1386 base 行は `state/physical.bin` 不在で判読者未再現・λ·ρ₂ は DERIVED・**事前試験 6 件(alias 逆対照を含む)は再走ではなく sha pin による継承**(ただし alias 修理の有効性は §6.4 の動的証拠 = start が 33 親で凍結・current 97 で成立)
> GRADE2 NOT_DECIDED・full_A0 false・verified=false。**正式受理 1418 を維持し 1450 を候補とする Astra の境界維持は妥当**であり、CV-9 の観点からは 1450 の受理を妨げる材料は見つからなかった(受理の可否は司令塔の裁定)。

---

## 9. 次周回(Task 986 = 実 64 親・絶対 cap 128)の判読範囲(推奨)

**①②③**: P/C sha 無変更なら 1 行で省略可(本 run と同じ)。
**必須 ⑤**: head 連鎖 128/128・前 64 head の同一性・target.scalar 列・`row_pairings = sha(0x00×rank)`・λ 直交・q/κ/score/aux 内訳・preserved-input 全数・実測秒 vs cap。
**§4.2 の恒等式検算は毎回入れること**(符号規約を実データで判別する唯一の非空虚試験)。
**追加すべき 1 項目(新設・§6.1 が理由)**:

1. **`tree/chord-residuals.u8` から先頭失敗弦の roster index と `residual_nonzero` の全 step 列**を取り、
   **(a) index の前進率(弦/段)(b) 失敗総数の趨勢(c) 後退遷移の数**を格付け文面に必ず数値で書く。
   これがキャンペーンの実効的な進捗計であり、cap の梯子(128 → 256 …)を続けるか撤退するかの唯一の量的根拠になる。
2. 2149 §9 の 3 追加項(ω/central 指数列・λ の character 別台・failed_chord/basis)は継続。

**①②③ を復活させる条件**: producer か checker の source sha が変わったとき、または継続器が新しい module を TCB に取り込んだとき。

---

## 10. 判読者の限界(正直な申告)

- 受理済み 1386 base 行との λ 直交性は `state/physical.bin` 不在のため**再計算していない**。
- 各 phase の算術本体(section/cochain/tree/raw/source/primal/p1/B)は checker が producer バイトと突合した結果を受け入れており、
  **私が第三実装で再計算したのは §3・§4・§7 の表に挙げた量のみ**。
- §6.1 の外挿(5.3 × 10⁴ 段・15 日)は**現在の観測率の線形外挿であって予言ではない**。失敗集合は毎段再計算されるため、
  ある段での一斉零化は**この観測からは排除されない**。
- ω = 2 の 15 行が同じ物理行を与えるか否かは 2150/2151 の数学裁定に依拠しており、**私は独立に検証していない**(CV-9 スコープ外)。
- 「この観点では穴を見つけられなかった」は**保証ではない**。特に再 hash されない alias の不在は依然として証明されていない(2149 F-al-2 を継続)。

---

判読ファイル: `C:\Users\81905\Desktop\shadow-atelier\scratchpad\fal_cv9_cegar_resume64_report_v1.md`

sha256(this file, excluding this line) = db7ded7f66561888
