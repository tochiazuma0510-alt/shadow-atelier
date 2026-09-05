# root scalar batch v2(v541 修正式)run CV-9 判読(falsifier 逐語・裁定 2096 で正本化)
著者: falsifier(opus/max・非当事者)。司令塔が scratchpad 報告書(sha256 先頭 16 桁 7713db71eb381252)を逐語転記(2026-09-05)。

**工房裁定(2096)**: CV-9 = **同一対象**(限定 4 条)。工房格 = **checker PASS(同一著者系統・v541 差分は両側打ち直し(token 0.75〜0.90)・F₃ packed dot 表は両側別実装で全数照合済・ただし v15 低位核と seed 生成核は逐語〜0.96〜0.98 クローン)・cross-checked は限定つき** — (i) 射程 = character 0 の root covector・走査順 origin 0..30 の 31 件・補正済み seed scalar 44 個全部・lower 収縮値 4×8059 全部(post-fold actor scalar 32,236 個は未封)(ii) root covector と seed2=0 は事前 pin/assertion で独立発見ではない(新情報 = seed 30/35/36 = 1)(iii) w_t の錨は Task712 の degree-2 一致のみ(定数・degree-1 ブロックは 0.96 クローン対で二系統一致では retire 不能)(iv) root_characters 4・504 は宣言定数。主張 = 「v541 修正式で走査順最初の非零 scalar が seed 30 で 1(seed 2 は旧式の 1 から 0 に訂正)」という有限事実。GRADE2 NOT_DECIDED・verified=false。

---

# CV-9 仕様同一性判読 — R07 actual grade-two root scalar batch **v2**(v541 修正式・副検問・事後)

判読者: falsifier(反証前哨・非当事者)
対象: GHA run `33941591417`/1(success)・terminal `RootViolationBatch`
先例: `docs/notes/j3_run2_cv9_reading_v1.md`(裁定 2077・run 33903333330 = 旧式 v1)
判読範囲: 「producer と checker が同一対象を計算しているか」の一点のみ(裁定 316/318 スコープ制限)。数学的正しさの監査・実装レビュー・追加テストの発案はしない。
日付: 2026-09-05

---

## 0. 裁定

**同一対象(SAME OBJECT)。限定 4 条。**

producer と checker は「固定 4 親(P1 `9931437113` / Task554 5 body + 12 blob / Task712 `9915928157` / Separator `9944214057`)に対し、**v541 (2.1)+(2.2)+(4.1)** の修正式で 32,280 個の scalar accumulator を組み、**v540 (2.4) の走査順(44 seeds → basis_i 0..8058 × slot 0..3)で最初の非零を返す**」という同一対象を計算している。今回の重点である **v541 差分 (a) raw seed slice と (b) lower-to-top 項 `K_t b_i`** は、**両側に別々のコードとして書かれている**(逐語コピーではない)。走査順規約は **v1 から不変**。別対象・判定不能の余地は見つからなかった。

ただし cross-checked の射程には限定 4 条(§3)が付く。とくに **「最初の違反」は今回 seed 30(actor ではない)**であり、origin 31..32279 は封も比較もされていない。

---

## 1. 同一対象と判定した根拠(すべて確認済み・file:line)

| # | 規約 | producer | checker | 一致 |
|---|---|---|---|---|
| 1 | 4 親 pin + 12 blob pin + Task712/root/child pin | `search/d972_r07_actual_grade2_root_scalar_batch_v2.py:38-205` | `search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py:35-175` | **literal ブロック単位で機械 diff = 完全一致**(`EXPECTED_CHILD` のみ改行位置差) |
| 2 | 同一 launch ファイル | `--run-launch $RUNNER_TEMP/launch.json` | `--check-launch $RUNNER_TEMP/launch.json` | `.github/workflows/d972-r07-actual-grade2-root-scalar-batch-v2.yml:452,476` |
| 3 | root/child covector 構成(`sparse_adjoint`・actor 順 (1,-1,2,-2)) | `:1063-1086` | `:773-791` | 同一。実測 root sha `af62027a…`・support 2742・lead 3 値 2(**v1 と同一対象**) |
| 4 | **v541 (2.1) 直接 seed = raw 行の平凡な character slice** | `raw_seed_direct :366-408`(`evaluated[2][character]`) | `checker_raw_seed_direct :292-332`(`full[2][character]`) | 同一式・同一 44 行順・同一 receipt 本体キー |
| 5 | **v541 (4.1) lower adjoint κ = (π_a K_t)^* q** | `actor_adjoint :434-483` | `checker_actor_adjoint :360-414` | 同一構成(tag→component→parity→source character・`q[...,u_j·g]`・aux 8 は零) |
| 6 | κ の degree-2 制限 = Task712 homogeneous adjoint(バイト一致要求) | `:497 task712_pure_top_adjoint` | `:426 checker_task712_top_adjoint` | 同一・**独立親への束縛** |
| 7 | κ の Task554 座標への埋込み(old = d0[owner]‖aux(8) 幅 6056、grade companion = d1 全 72576、new = d1[owner] 幅 18144) | `old_covector_slices :592-604` / `new_covector_slices :606-614` | `checker_old_slices :508-519` / `checker_new_slices :521-529` | 同一。呼出も同一(`source` / `target` = 所有 character) |
| 8 | **w_t を relation 減算の前に加算** | `accumulate_scalars :836-855`(old)・`:874-881`(new) | `:825-841`(old)・`:861-869`(new) | 同一順序 |
| 9 | relation fold の入れ子と添字(`ORIGIN_RANGES[source][0] + 44 + 4*pivot + slot`) | `:854-903` | `:842-891` | 同一 |
| 10 | **走査順(44 seeds → basis_i × slot)** | `_scan_accumulated :1186-1193` | `:986-993` | 同一。**v1 から不変** |
| 11 | origin 採番と prefix chain `sha256(chain ‖ canonical(record))` | `:1173-1180` | `:971-978` | 同一 |
| 12 | v2 relation recipe seal | `relation_source_sha256 :616-634` | `:531-549` | **当哨が第三実装で再計算 → `1d0bc36c…` = 実 cert 値と一致**(§6) |

**相互束縛(fail-closed の実体・v1 より広い)**: checker は `_expected_character :1013-1114` で character record 全体(`filtered_direct` 受領証・44 seed scalar 配列・4 本の lower 収縮配列を含む)を自前再構成し、`check_output :1203-1206 checker_repaired_payload_exact` で **producer が書いた `seed-scalars-a0.bin`(44 B)と `actor-lower-a0-t{0..3}.bin`(各 8059 B)をバイト一致要求**、`:1265 checker_output_exact_roster` でファイル集合の完全一致を要求する。

**紙との一致(副検問の本体)**: v541 §6「receipts must state that actor direct values include the full lower-to-top term and seed direct values are raw slices」→ cert に `actor_direct_includes_lower_to_top` / `seed_direct_is_raw_character_slice` / `projected_direct_seed_routine_called` が実在(§4 F2-4 の留保つき)。v541 §6「Old seed-row hashes ... cannot be reused」→ **`SEED_REGISTERED_ROW_SHA` は v2 から完全に消えている**(v1 には存在)。

**数値恒等式(整数のみ・当哨が撃った)**: Σold 505+503+503+503 = 2014、Σnew 1509+3·1512 = 6045、計 **8059**。4·44+4·2014 = **8232**。44+4·8059 = **32280**。4·6048+4·18144+8 = **96776**。blob 総バイトを 12 本の pin から再計算 → **67,011,332**(宣言定数ではなく導出可能)。offsets [0,505,1008,1511]/[2014,3523,5035,6547]。すべて一致。

**事前登録・silent cap**: 見つからなかった。P1 cache は 8,059 行 1 パス全消費 + trailing 空 + sha 再計算(producer `:1115-1136` / checker `:939-955`)。12 blob も全バイト消費 + trailing 空 + descriptor sha 一致(producer `stream_packed_dots :547-589` / checker `:466-505`)。workflow は 8 親を `gh api`+`jq -e` で計算前に live 照合(`:88-141`・Task554 は `conclusion == "failure"` まで固定)。

**ダミー検査(何にでも当たる試験)の検出**: 見つからなかった。両 selftest は **旧一側射影 `_seed_full_project` を実際に実行して分離を要求**(producer `:1439,1475,1483` / checker `:1862,1875`)、および **full actor `_seed_act` を実行して adjoint と突合**(producer `:1495-1520` / checker `:1825-1846`)する。producer selftest は合成 Violation を origin 0(seed)と origin 44(actor)で発火させる(`:2000,2009`)。

---

## 2. 独立性の実体(測定値)

### 2.1 v1 から改善した点(確認済み)

| 項目 | v1 | v2 |
|---|---|---|
| F₃ packed dot 表 | 共有 v15 核のみ | **両側で別々に手書き**。producer `_PACKED_DOT :534-544`(`%3`/`//=3` 反復)・checker `_CHECKER_PACKED_DOT :457-464`(`(x//3**i)%3` 内包表記)。当哨が両者 + 素朴 base-3 参照を 81×81 全数照合 → **不一致 0** |
| v541 差分の実装形 | (存在せず) | **打ち直し**。トークン/AST 類似度 `actor_adjoint` **0.746/0.826**、`_polynomial_pull` **0.801/0.891**、`raw_seed_direct` **0.904/0.948**、`stream_packed_dots` **0.858/0.944**(比較: 承知のクローンは 1.000) |
| 索引順の実差 | — | producer `SEED_DEGREE2_PRODUCT[alpha][gamma]`(`:427`)vs checker `[gamma][alpha]`(`:353`)。当哨が表の**対称性を数値確認** → 同値。**転記が独立である弱い証拠** |
| selftest 設計 | 8 変異 | **設計が別物**。producer = 1 actor の lower-only/mixed/pure-top + tiny packed 血統(rng 541)。checker = 4 character × 4 actor の **16 本 mixed full-action 比較** + 2 行 full-defect 再構成(rng 541922) |
| 照合の幅 | origin 0,1,2 の 3 件 | **44 seed scalar 全部 + 4×8059 lower 収縮値**がバイト比較 |

### 2.2 なお逐語クローンの部分(測定値・v15 モジュールは v1 と**バイト同一**)

`ARITH_SHA256 = 76546bef…`(producer 側)/ `8f718811…`(checker 側)は v1 の pin と同一。両モジュールの共通逐語前置は 1 行のみだが、**関数単位では以下が完全一致**(トークン類似度 1.00000・改名を除き本文同一):

`pack_trits` / `unpack_trits` / `dot_mod3` / `sparse_adjoint` / `_read_table` / `_table_line` / `read_task712_envelope` / `validate_raw_dual` / `_dual_next_state_head` / `_sealed` / `_load_words`

seed 生成核は **ほぼ逐語**(トークン類似度):

| 単位 | 類似度 | v2 での役割 |
|---|---:|---|
| `_seed_evaluate_seed` ↔ `_checker_seed_evaluate_seed` | **0.98257** | v541 (2.1) の raw seed 行を産む |
| `_SeedContext` ↔ `_CheckerSeedContext` | 0.97810 | 文脈 |
| **`_seed_act` ↔ `_checker_seed_act`** | **0.96000** | **両 selftest が (4.1) を突合する「直接 full actor」参照** |
| `_seed_e_poly` / `_seed_sign_kernel` | 0.9867 / 0.9759 | (4.1) の重み |
| `_seed_cv` / `_seed_lower_coord` / `_seed_grade1_coord` | 本文同一 | (4.1) の座標・符号 |
| `_seed_full_project` | 0.97122 | 負制御(旧式)専用 |
| `_seed_affine_eval` / `_seed_substitute` | 0.9059 / 0.9512 | tag actor 値 |

batch ファイル側にも完全一致が残る: `relation_source_sha256` **1.0000**、`vectorized_projection_chunk` **1.0000**、`terminal_kind` **1.0000**(いずれも文字列定数を正規化した上での測定。`terminal_kind` は実際には述語フィールドが異なる = §4 F2-7)。

**帰結(重要)**: v541 (b) の新項 `w_t` は、**両側とも同じクローン対 `_seed_act`/`_checker_seed_act` を「正解の前方作用」として突合している**。クローン外の錨は `task712_pure_top_adjoint`(独立親 Task712 との一致)だけで、これは **α = degree-2 の制限しか拘束しない**。α ∈ {定数, degree-1}(= まさに新項)には非クローンの錨が存在しない。二系統一致では retire できない。

### 2.3 Sol 162 §4「shared legacy seed arithmetic design は 922/923 で開示」の実体

**開示は実在する。ただし定性的で、量は書かれていない。**

- `sol/luna_task_922_r07_filtered_root_scalar_batch_v2.md` §1: 「Existing independent v15 arithmetic contexts may be reused on their respective producer/checker sides; do not call either old projected direct-seed routine.」
- `sol/sol_reply_926_audit_filtered_root_scalar_v2.md` F926-3: 「It intentionally retains the checker-v15 arithmetic design and the same fixed marking data as the producer lane, so this is implementation cross-checking, **not independent mathematical provenance or Lean verification**.」

→ 「設計を共有している」ことは明言されており、**格の誤読を招く申告ではない**。ただし「どの単位がどれだけクローンか」は §2.2 が初出。格付け文面には §2.2 の数値を使うのが正確。

---

## 3. 主張の射程

### cross-checked と呼べる有限事実(v1 より広い)

1. **最初の違反 = `origin_id 30` / `origin_kind "seed"` / `seed 30` / `scalar 1`**(`output/character-a0.json` の `scalar` レコード・`scalar_prefix_digest 3ea7d56c…`)。**当哨が保存済み 44 バイト配列から chain を第三実装で再計算 → prefix digest 完全一致**。
2. **補正済み seed scalar 44 個すべて**(`seed-scalars-a0.bin`・sha `7f9f5493…`): 非零は **30, 35, 36 の 3 個(いずれも 1)**、他は 0。**seed 2 = 0**(= v541 修正が答えを変えた実体)。producer/checker がバイト一致。
3. **lower 収縮値 4×8059 すべて**(`actor-lower-a0-t{0..3}.bin`)がバイト一致。しかも**非零が濃い** — t0: 4326/8059、t1: 4349、t2: 4272、t3: 4306(old 行 1304-1331/2014、new 行 2968-3018/6045)。→ **v541 (b) の補正は空虚でない**。v1 で「actor 分岐は実データで一度も評価されていない」とした穴は、**直接値の側では塞がった**。
4. root covector(support 2742・lead 3・値 2・sha `af62027a…`)と 4 子、character 1,2,3 の RootZero、P1 cache 1 パス(sha `b88edb9b…` 再計算一致)。
5. v2 relation recipe seal `1d0bc36c…`(当哨が第三実装で再計算一致)。

### cross-checked ではない(必ず文面に書く)

1. **origin 31..32279 について何も言っていない。** 32,280 個の accumulator は両側で計算されたが、走査は origin 30 で return する。**post-fold の actor scalar 32,236 個はどの受領証にも束縛されていない**(hash も比較もない)。cross-check されたのは actor の**直接側入力**(top 値 + lower 収縮値)までで、relation 減算後の値ではない。
2. **seed 2 = 0 は「発見」ではなく production 経路の assertion**(producer `:1243` / checker `:1039`)。真値が非零なら run は失敗して報告しない。今回の新情報(seed 30/35/36 = 1)は pin されていない。
3. **root covector は preflight 由来の事前 pin への回帰照合**(`EXPECTED_ROOT`/`EXPECTED_CHILD`)。独立発見ではない。v1 と同じ。
4. **`root_characters: 4`(checker 戻り値 `:1268`)はリテラル定数**。実走は character 0 のみ。`relation_origin_declared_count: 32280` は「宣言値」と明記されるようになったが検査量ではない(実際に検査された origin は 31 件)。
5. **`future_orbit_rows_executed: 0` / `future_active_orbit_declared_bound: 504` はいずれもリテラル**(producer `:1362-1364`)。前者は「将来 dual orbit の行を 1 本も実行していない」という正直な射程宣言、後者は未検査の宣言定数。504 の主張を cert は支えていない。
6. GRADE2 MEMBER/NONMEMBER = NOT_DECIDED。A0/COMMON/COFINAL_LIFT/FAKE/IHARA = NOT_DECLARED。**verified=false**(Lean 未)。

---

## 4. 指摘

**【要修正 F2-1(v1 F-1 の持ち越し・未修理)】** `sol/proof_r07_actual_scalar_blockwise_fubini_v540.md:34` の「Task554's canonical normal-form condition makes the indices strictly increasing」は依然未改訂(最終 commit `0b32fe68` は origin count 修正のみ)。v2 は v540 の fold を無改変で継承し、実装の `_expression`(producer `:636-645`)/`_expr`(checker `:551-559`)は**一意性と範囲しか要求しない**。F₃ 和は可換なので値には無影響だが、**凍結された規約宣言が実装と食い違ったまま**。→ v540 §1 の当該一文を実装に合わせて改訂。

**【要修正 F2-2】v541 (4.1) の検証錨がクローン内に閉じている。** v541 §4 は「A bounded checker can test (4.1) against direct full-actor evaluation」と宣言し、実装もそうしているが、その「direct full actor」は producer `_seed_act` / checker `_checker_seed_act` = **トークン類似度 0.96 のクローン対**。非クローンの錨は `task712_pure_top_adjoint`(degree-2 制限のみ)だけで、**新項 `w_t` を産む α ∈ {定数, degree-1} ブロックには錨がない**。→ 格付け文面に明記。retire には第三実装(または Lean 層)が要る。**当哨は安価な全数照合を見つけられなかった。**

**【要修正 F2-3】格付け文面での数値引用(v1 F-3 の縮小版)。** 「32,280 relations を照合した」「4 character を走査した」と読める引用をしない。実際は origin 31 件が走査され、character 0 のみ実走、post-fold actor 値 32,236 個は未封。引用するなら「宣言値」と明記。

**【軽微 F2-4】cert 上の規約フラグは「宣言」であって「計測」ではない。** `actor_direct_includes_lower_to_top` / `seed_direct_is_raw_character_slice` / `projected_direct_seed_routine_called` は producer `:1270-1272` / checker `:1078-1080` の**ハードコード literal**。実効性は workflow の凍結ソース sha pin(`:63,65,316-322`)から来ており、cert 自身が証明しているわけではない。設計としては正しいが、証拠として引用しない。(当哨は `_seed_full_project` の全呼出箇所が selftest 専用であること、`--actual-canary-launch` が `--selftest` 外で拒否されること(producer `:2098` / checker `:1960`)をソース上で確認した。)

**【軽微 F2-5(v1 F-4 未修理)】** producer `raw_dual :1152` は `separator["manifest"].get("state_head", SEPARATOR_STATE_HEAD)`、checker `make_raw :901` は定数。現状 fail-closed で実害なし。

**【軽微 F2-6(v1 F-5 未修理)】** `safe_path` の境界が非対称(producer `:242` は `path == root` を許容・checker `:204` は不許容)。実害なし。

**【軽微 F2-7(v1 F-6 未修理・独立性のプラス)】** `terminal_kind` の述語が別フィールド(producer `:1331` は `scalar_schema`.endswith("Violation")、checker `:1133` は `schema`.endswith("RootViolation"))。意図的なら一行コメントが要る。

**【軽微 F2-8】checker の負制御が 1 本無内容。** `:1858-1859 checker_v541_omitted_lower_negative_control` は `(scalar - known_scalar) % 3 != scalar` を要求するが、直前に `known_scalar != 0` を確立済みなので恒真。害はないが証拠にならない。

### v1 から修理済み(確認済み)

- **v1 F-2 解消**: `value_vector_sha256`(5 本)が **Violation 分岐にも入った**(producer `:1181` / checker `:979`)。実 cert(`character-a0.json`)で 5 本を実見・うち 4 本は `actor_top_value_sha256` と一致。
- **v1 F-7 解消**: `future_active_orbit_declared_bound` へ改名 + `future_orbit_rows_executed: 0` を併記。
- **v1 §3-1 の count 語法 解消**: `global_relation_declared_count` / `relation_origin_declared_count`。
- **v1 §3-2 部分解消**: actor の直接値(top + lower)が全 8059×4 で実データ評価 + バイト照合された。post-fold 値は依然未封。
- **v541 §6 遵守**: `SEED_REGISTERED_ROW_SHA` は v2 から削除。

### 反証できなかった点(正直な範囲報告・保証ではない)

- **走査順規約**: producer / checker / 紙(v540 (2.4))の三者一致。v1 から不変。抜け道は見つからなかった。
- **事前登録と silent cap**: 見つからなかった(§1)。
- **ダミー検査**: 見つからなかった。旧式の一側射影を実行して分離を要求する負制御が両側にある。
- **撤退条件**: producer/checker 各 40 分 `timeout`、job 90 分、**両方 success のときだけ** candidate を発行(`:510`)。超過時は diagnostics のみ。
- **「見つからなかった」を非存在と読む型**: 該当なし。主張は seed 30 で scalar 1 という肯定的証拠。

---

## 5. CV-9 裁定案 + 工房格付け案

**CV-9 = 同一対象(限定 4 条)。**

格付け案(一行):

> checker PASS(同一著者系統・**v541 差分は両側で打ち直し**(token 0.75–0.90)・**F₃ packed dot 表は両側別実装で当哨が全数照合済**・ただし v15 の低位核と seed 生成核は逐語〜0.96–0.98 クローン)。**cross-checked は限定つき** — (i) 射程は固定 4 親に対する character 0 の root covector、**走査順 origin 0..30 の 31 件**、**補正済み seed scalar 44 個全部**、**lower 収縮値 4×8059 全部**(post-fold の actor scalar 32,236 個は計算されたが未封・未比較)、(ii) root covector と seed 2 = 0 は**事前 pin / production assertion** であって独立発見ではない(新情報は seed 30/35/36 = 1 のみ)、(iii) v541 (4.1) の新項 `w_t` の錨は Task712 の degree-2 一致のみで、定数・degree-1 ブロックはクローン対 `_seed_act` にしか突合されていない、(iv) `root_characters 4` と `future_active_orbit_declared_bound 504` は cert 上の宣言定数で未検査。**主張は「λ の character 0 root covector に対し、v541 修正式で走査順最初の非零 scalar が seed 30 で 1(seed 0..29 は 0・seed 2 は旧式の 1 から 0 に訂正)」という有限事実に限り、GRADE2 MEMBER/NONMEMBER ではない。verified=false(Lean 未)。**

---

## 6. 当哨が実行したこと(要点)

- v2 producer/checker/workflow の sha256 を再計算 → Sol 926 申告値と一致(`3c93c50c…` / `e0237d10…` / `326bc19f…`)
- pin literal ブロックの機械 diff(OLD/NEW_BLOB_PINS・TASK554_BODY_DIGESTS/ARTIFACTS・EXPECTED_ROOT/CHILD・SEED2_*)
- `tokenize`+`difflib` と `ast.dump` 正規化による producer↔checker 28 単位の類似度測定、および v15 モジュール 22 単位の測定
- `SEED_DEGREE2_PRODUCT` の対称性を数値確認(producer/checker の索引転置が同値である根拠)
- 両側の 81×81 packed dot 表を逐語再現し、相互 + 素朴 base-3 参照と全数照合(不一致 0)
- 恒等式の整数検算(8059 / 8232 / 32280 / 96776 / 67,011,332 / offsets)
- 候補 artifact `9962060495` を Release `archive-gha-checkpoints` から取得(zip sha `1091f994…`)・展開
  - `terminal.json` / `result.json` / `manifest.json` / `character-a{0..3}.json` / `filtered_direct` の封を全て再計算一致
  - `q-a0-root.bin` を base-3 復号 → support 2742 / lead 3 / 値 2 を独立確認
  - `seed-scalars-a0.bin` から **prefix chain を第三実装で再計算 → `3ea7d56c…` = cert 値と一致**(最初の違反 = seed 30)
  - `actor-lower-a0-t{0..3}.bin` の非零密度を測定(空虚性チェック)
  - `relation_source_sha256` を第三実装で再計算 → `1d0bc36c…` = cert 値と一致
- 診断 artifact `9962060193` を取得し producer/checker ログを確認
- GHA 発火・大規模計算・実装・修理はしていない。
