# CV-9 増分判読 — R07 **fixed root packet loop v2**(rank 1356 → 1359・terminal ROOT_SEEDS_ZERO)

判読者: falsifier(反証前哨・非当事者)
対象: GHA run `33964709359`(success・head `fff114c41bd8748ad0e708919fe0820335c9cce8`)・terminal `ROOT_SEEDS_ZERO`・candidate artifact `9969090590`・diagnostics `9969090847`
親規律: 裁定 2117(`docs/notes/seed34_mat_v3_cv9_reading_v1.md`・改訂規律 ①〜⑤)/ 2110(`docs/notes/r1355_rss_v1_cv9_reading_v1.md`)/ 19 規約表の親 = 2105
判読範囲: 「producer と checker が同一対象を独立に計算しているか」の一点のみ(裁定 316/318 スコープ制限)
日付: 2026-09-05

---

## 0. 裁定

**同一対象(SAME OBJECT)。限定 5 条。別対象・判定不能の余地は見つからなかった。**

producer `search/d972_r07_fixed_root_packet_loop_v2.py`(sha256 `e040c7b3…`・1398 行)と
checker `search/check_d972_r07_fixed_root_packet_loop_v2.py`(sha256 `5289253a…`・1054 行)は、

> **λ 非依存の固定 44 seed packet**(4 character × 44 seed = 176 本の `D_s` の character slice)を両側が独立にゼロから構築し、rank 1356 の受理済み state から出発して、**各周回で 4 本の B-adjoint root `q_a = B_a^*λ` を作り直し**、character-major/seed 0..43 の順で packet と pairing し、**最初の非零 1 本だけ**を物理化して挿入順 1 掃引 → 正規化 append → target 1 段更新 → λ 逆代入 → **λ の全行スイープ**を行い、非零が尽きたところで `ROOT_SEEDS_ZERO` を宣言する

という同一対象を計算している。checker は packet 4 ファイル + manifest と全 3 step の 8 payload + manifest を**自前計算バイトでバイト一致要求**し、終端 scan(176 pairing)と terminal 判定を**自分の scan から独立に再導出**する(`same(actual_result, result)` = `check_..._v2.py:906`)。

**今回いちばん重い事実**: 終端の 176 pairing のうち**情報を持つのは 44 本だけ**である。character 1,2,3 の root は**恒等的に零ベクトル**(`packed_sha256 = 8f23754a…` = 当哨が外部計算した `sha256(0x00 × 9072)` と一致)。cert はこれを `informative_pair_count: 44` / `nonzero_root_block_count: 1` として**正直に宣言している**(2110 R1-1 / Sol 163 F5 の事前登録どおり)ので同一対象性は揺るがないが、**格付け文面で「44 seed packet の全 176 pairing を λ が消した」と書くと過大主張になる**(§3 F-pkt-1)。

---

## 1. ① 規約表の機械 diff(seed34 materializer v3 → fixed root packet loop v2)

凡例: P = producer / C = checker。**11 規約が保持・一致**、**6 規約が拡大/強化**、**2 規約が移行**、**6 規約が新設**。**弱化は今回ゼロ**(2117 で弱化した `λ·ρ₂` は弱化のまま据え置き + 宣言が明示化)。

| # | 規約 | v3 → packet-loop v2 | 判定 |
|---|---|---|---|
| 1 | 親を計算前に live 照合(`gh api` + `jq -e`) | 6 run / **10 artifact**(seed34 が pin に追加・repository_id と head_sha まで一致要求) | 一致(両側同一 workflow) |
| 2 | **違反の選択規則** | v3 = pin 済み親 `scalars.jsonl` 176 レコードの走査順最初の非零 → v2 = **親 scalar 表を持たず、その場で `q_a = B_a^*λ` を導出して packet と pairing し最初の非零** | **移行**(自前導出化 = 強化) |
| 3 | 走査順 character-major / seed 0..43 | P `:926-928` の generator / C `:736-738` の `index//44, index%44` | 一致(別実装) |
| 4 | SeedRed 事象列の収集 | v3 = 選択 1 seed → v2 = **44 seed 全部**。P `collect_relations:570-634`(自前 append + rolling)/ C `:361-386`(`LEGACY.combined_selected` を 44 回) | **拡大** |
| 5 | 事象の rolling 封(`sha(prev ‖ canonical(event))`・畳込み前に封) | P `:625-629` / C は v3 checker の `combined_selected` 内 | 一致 |
| 6 | mod-3 畳込み → 非零のみ・node 昇順 | 44×8059 係数表。P `np.flatnonzero` / C `final` list | 一致(別実装) |
| 7 | owner/kind 判定(OLD/NEW_OFFSETS) | P = segment 記述子 / C = `LEGACY.OLD_OFFSETS`/`NEW_OFFSETS` 算術。定数不変 | 一致 |
| 8 | 物理化写像 `+(3−c)·row ≡ −c·row` | P `add_scaled(...,3-c):700` / C `subtract(...,c):452` | 一致(式同値・書き方は別物) |
| 9 | 下位 96776 座標の完全消滅 | v3 = 1 seed → v2 = **44 seed 全部**。P `:791` / C `LEGACY.require_lower_zero:501` | **拡大** |
| 10 | v453 direct slice は complete lower-zero の後にのみ | P `:793` コメント + 制御流 / C `:507-509` コメント + 制御流 | 一致 |
| 11 | `q·d = 1` / `λ·G = 1` | v3 = 1 対 → v2 = **毎 step**。P `:1005 require(q_d == lambda_g == scalar)` / C `:781 require(dot(functional, raw) == scalar)` | 一致(P は adjoint 側と forward 側を両方計算して等号、C は pushforward 側 1 本) |
| 12 | 挿入順 1 掃引・lead 一意・単調要求なし | `m.physical_reduce` / `LEGACY.reduce_dense` = **2117 の pair をそのまま再利用**(新規実装ではない) | 一致(§3 F-pkt-5) |
| 13 | 正規化 `normalized = remainder·scale` | `m.normalize_pivot(remainder, old_leads)` / `LEGACY.normalize(remainder)` = 再利用。非対称(強い側 = P)も 2117 のまま | 一致 |
| 14 | 新 target 段は新 pivot 1 本のみ | `m.update_target` / `LEGACY.next_target` = 再利用 | 一致(**step 3 は scalar 0** = §3 F-pkt-2) |
| 15 | λ = 新 target 剰余の最初の非零を free、pivot_id 降順で逆代入 | P は **新規 `next_separator:948-969`**(v3 の `separator_after_append` から 0.48 の書き直し)/ C は **v3 の `next_separator` をそのまま** | 一致(P 側のみ打ち直し) |
| 15′ | λ の最終全行スイープ(2105 F1) | v3 = 1 回 → v2 = **start + 毎 step**。P `m.check_final_separator`(`:525` `:1173` + `next_separator` 内)/ C `LEGACY.next_separator` の `final_lambda_allrows` + `:799` の 2 target 直接 pairing | **拡大** |
| 16 | 「依然 Separator」の判定 | P `first_nonzero(target)` / C `np.any(updated)` | 一致 |
| 17 | `λ·ρ₂` | 2117 で実測→前提へ弱化。v2 は **明示 DERIVED**(`mode:"derived"`・`original_rho2_directly_read:false`・3 親を名指し)。P `derived_rho2:937-946` / C `rho2_derivation:584-594` | **弱化据え置き + 宣言強化**(M3-1 = Task947 §1 の要求どおり) |
| 18 | 封の正規形(`sort_keys=True`・ASCII・末尾 LF) | P `canonical:114` / C `canonical:100` | 一致(当哨が全 cert を再封して成立確認) |
| 19 | 格の自己抑制 | `candidate:true / cross_checked:false / verified:false` を packet manifest・step manifest・step result・result・checker-result のすべてに。workflow が `jq -e` で 3 箇所要求 | 一致 |
| **20** | **packet の λ 非依存性**(新設) | packet は P1 / Task554 / raw seed のみから構築。P `build_packet` が `state` を使うのは seed30/34 の regression 照合だけ(`:811`)/ C `rebuild_packet` も同様(`:510-513`)。resume 時 P は保存 packet を読むが C は**毎回ゼロから再構築してバイト一致要求** | **新設・一致** |
| **21** | **declared 176 / nonzero root blocks / informative / nonzero の 4 分**(2110 R1-1) | P `:931-934` / C `:740-744`。field 名・算出式とも同一 | **新設・一致**(ただし §3 F-pkt-3 の非対称あり) |
| **22** | **terminal の決定規則**(新設) | P `terminal_for:1176-1184`(first_hit None → ROOT_SEEDS_ZERO / resource → UNKNOWN_RESOURCE / cap → UNKNOWN_CAP)/ C `terminal_for_state:709-719`(**自前 scan から再導出**し、first_hit があれば `nonzero_root_cannot_claim_empty:717` で UNKNOWN_* 以外を拒否) | **新設・一致 + C が P の宣言を拒否可能** |
| **23** | **耐久 prefix と HEAD**(新設) | 完全 step を fsync/rename してから HEAD を進める。P `append_step` + `publish_directory` / C `audit_steps_directory:693-707` + step ごとの `compare_directory` | **新設・一致** |
| **24** | **同一 owner resume**(新設) | P `load_prefix:1075-1175` が owner/start/source/packet pin と rolling chain を要求。workflow が **cap1 → resume176 の実 2 回起動**で確認 | **新設・P 側のみ**(§3 F-pkt-6) |
| **25** | **mixed-generation parent layout**(v2 の修理・新設) | seed30 = flag 欠落 / seed34 = flag `true` を**書き換えず**判別。P `saved_parent_layout:177-238` / C `validate_parent_generations:136-178`。workflow が両側の `parent_layout` を `diff` で突合 + 各 5 件の否定試験 | **新設・一致**(当哨が artifact 内の両 JSON を直接比較 → 完全一致・layout sha `2a8df24a…`) |

**相互束縛**: C `compare_directory:684-691` は自前計算バイトに対し **packet 4 ファイル + manifest** と **各 step の 8 payload + manifest** の完全 roster 一致とバイト一致を要求。さらに `same(actual_result, result):906` が result.json 全体(176 個の `values` を含む scan を内包)をバイト一致で要求する。当哨も packet manifest の 4 receipt を独立に再ハッシュして全一致。

---

## 2. ②③ の省略可否 — **今回は両方とも省略不可**(新しい pair)

### ②(import 交差辺): **交差辺は無い。**

- **producer** `dependencies:364-388` は `d972_*` のみを sha pin 付きで `exec_module`: `d972_r07_actual_root_seed_materializer_v3.py`(`36cc620b…`)と `d972_r07_rank1355_root_seed_scalars_v1.py`(`973ccd1d…`)。materializer が `d972_r07_actual_grade2_root_scalar_batch_v2.py`(`3c93c50c…`)を、それが `d972_r07_targeted_grade2_owner_generated_join_v15.py`(`76546bef…`)を引く。
- **checker** `:22-48` は `check_*` のみ: `check_..._materializer_v3.py`(`eca60918…`)を LEGACY として import し、`BASE, ROOTS = LEGACY.BASE, LEGACY.ROOTS`(= `check_..._batch_v2` `e0237d10…` / `check_..._rank1355_root_seed_scalars_v1` `f3c7ca25…`)。`check_..._batch_v2.py:22` は `check_..._join_v15`(`8f718811…`)を ARITH とする。
- **producer 側 ARITH = `join_v15`、checker 側 ARITH = `check_join_v15`** を確認(`d972_..._batch_v2.py:25` vs `check_..._batch_v2.py:22`)。系統は完全分離。
- checker が producer ファイルに触れるのは `producer_source_receipt:672-682` の **sha 計算のみ**(import も exec もしない)。
- **系統 pin 4 本は 2110/2117 とバイト同一**: `3c93c50c` / `76546bef`(P 側)、`e0237d10` / `8f718811`(C 側)。
- **TCB モジュール集合は両側で 1 本ずつ増えた**(§3 F-pkt-5)。よって ②③ の省略条件は満たさない。

### ③(類似度): 再測定した(AJ=True / AJ=False 併記・手法は 2117 F-v3-1 と同一)。

**A. 本周回で実際に走った算術の cross-side 対**

| 単位 | AJ=True | AJ=False | 備考 |
|---|---:|---:|---|
| `P.collect_relations` ↔ `C.collect_relations` | **0.0752** | 0.2771 | 44 seed の事象収集 |
| `P.subtract_p1` ↔ `C.p1_packet_pass` | 0.2435 | 0.5054 | 8059 行 1 パス |
| `P.subtract_lower` ↔ `C.lower_packet_pass` | 0.1603 | 0.4171 | 12 blob |
| `P.build_packet` ↔ `C.rebuild_packet` | **0.0691** | 0.2045 | packet 全体 |
| `P.scan_roots` ↔ `C.evaluate_roots` | 0.2836 | 0.2836 | 4 root + 176 pairing |
| `P.scan_roots` ↔ `C.scan_certificate` | 0.1461 | 0.3238 | scan 証明書 |
| `P.append_step` ↔ `C.rebuild_step` | 0.0617 | 0.4383 | 1 step 全体 |
| `P.next_separator`(新) ↔ `C3.next_separator`(v3) | 0.2346 | 0.4086 | λ 逆代入(実効対) |
| `P.terminal_for` ↔ `C.terminal_for_state` | 0.2973 | 0.2973 | 終端判定 |
| `P.selftest` ↔ `C.selftest` | 0.0602 | 0.2370 | カナリア |
| `P.derived_rho2` ↔ `C.rho2_derivation` | 0.7626 | 0.7626 | **宣言ビルダー**(バイト一致必須・算術なし) |
| `P.literal_reference` ↔ `C.literal_certificate` | 0.4182 | 0.7721 | 同上 |
| `P.canonical` / `P.sha` ↔ 同名 | 1.0000 | 1.0000 | 承知のクローン(封の定義) |

→ **コピペ回帰なし。** 0.7 を超えるのは「出力がバイト一致でなければならない宣言ビルダー」と封の定義のみで、算術は 0.06〜0.29(AJ=False でも 0.20〜0.51)。

**B. 2117 から再利用している pair(今周回では打ち直していない)**

| 単位 | AJ=True | AJ=False |
|---|---:|---:|
| `P3.physical_reduce` ↔ `C3.reduce_dense` | 0.2255 | 0.6600 |
| `P3.normalize_pivot` ↔ `C3.normalize` | 0.5806 | 0.5806 |
| `P3.update_target` ↔ `C3.next_target` | 0.5090 | 0.5090 |
| `P3.check_final_separator` ↔ `C3.next_separator` | 0.2185 | 0.3217 |

(すべて 2117 の測定と一致。**pivot 挿入・正規化・target 更新の算術は今周回の新規実装ではない** = §3 F-pkt-5)

**C. v15 seed 核クローンの持ち越し(不変・毎回の一句)**

| 単位 | AJ=True | AJ=False |
|---|---:|---:|
| `_seed_evaluate_seed` ↔ `_checker_seed_evaluate_seed` | 0.9804 | 0.9826 |
| `_seed_full_project` ↔ `_checker_seed_full_project` | 0.9712 | 0.9712 |
| `_seed_act` ↔ `_checker_seed_act` | 0.9467 | 0.9600 |
| `_seed_cv` ↔ `_checker_seed_cv` | 0.9821 | 0.9821 |
| `check_table_transpose`(BASE 同名) | **1.0000** | 1.0000 |

**raw seed 行と projector は二系統一致では永久に retire できない。** 今回さらに `check_table_transpose`(B_adj = Bᵀ の検査)が**完全クローン**であることを記録する。ただし本周回では **両側とも `forward.B` から自前で adjoint を作っており**(P = `join_v15.sparse_adjoint:192` の Python ループ、C = `pullback:534` の `np.add.at` ベクトル化)、adjoint テーブルは receipt の識別子としてしか使われない。この 2 実装は互いに独立。

**D. v1 → v2 の同側 diff(v2 = v1 + parent-layout 修理か)**

- producer: 既存 41 関数中 **37 本が完全同一**、変更 4 本(`load_saved_delta` 0.99 / `load_start` 0.897 / `owner_and_tables` 0.905 / `main` 0.924)、新規 6 本(すべて parent-layout)、退役 0。
- checker: 既存 35 関数中 **31 本が完全同一**、変更 4 本(`expected_start` 0.986 / `load_start` 0.992 / `main` 0.927 / `selftest` 0.996)、新規 5 本(すべて parent-layout)、退役 0。
- → **Astra 返書 952 F5 の申告(算術・resume に変更なし)は機械的に裏付けられる。** v2 の差分は run 33963515077 の `KeyError('target_derivation_accepted_as_premise')` 修理に限定されている。

---

## 3. 指摘

### 【要修正】F-pkt-1. 終端 176 pairing のうち**情報を持つのは 44 本**。格付け文面が「全 176」と言うと過大

- 終端 scan(`result.json`):`roots[0].support = 2781`、`roots[1..3].support = 0`、`nonzero_root_blocks = [0]`、`nonzero_root_block_count = 1`、`informative_pair_count = 44`、`nonzero_pair_count = 0`。
- character 1,2,3 の `packed_sha256` は 3 本とも `8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838`。当哨が外部計算した **`sha256(0x00 × 9072)` と一致** = **`B_a^*λ` が恒等的に零ベクトル**。
- したがって残り 132 本は「packet の行が λ に消される」ではなく「**λ が B_1, B_2, B_3 の像全体を消す**」という packet と無関係の(そして本来もっと強い)事実の系である。**この 132 本は packet を一切試していない。**
- **3 step すべてで同じ形**(step 1,2 の root support = `[2715,0,0,0]`、step 3 = `[2667,0,0,0]`)。つまり本 run を通じて情報を持った pairing は毎回 44 本のみ。
- 判定への影響はない(cert が `informative_pair_count` で正直に分離しており、Sol 163 F5 の「2110 R1-1 採用」で**事前登録済み**)。**影響するのは格付け文面だけ**: 言えるのは「**character 0 の 44 本の informative pairing がすべて零、character 1〜3 は `B_a^*λ = 0` ゆえ構造零 132 本**」まで。

### 【要修正】F-pkt-2. step 3 は target を動かしていない(`target_scalar = 0`)。「3 回減らした」ではない

- 当哨がバイトを直読: `steps/000002/target-remainder.bin` と `steps/000003/target-remainder.bin` は**完全に同一**。cert も `target.parent_remainder_sha256 == target.remainder_sha256`(`0a466426db600e19…`)、`target.scalar = 0`。
- 3 step の target scalar は **[1, 1, 0]**。すなわち rank は 3 上がったが target 剰余が動いたのは 2 回。
- 副作用: step 3 の `direct_pairing` の「`lambda_parent_remainder = 1` かつ `lambda_new_remainder = 1`」は**同一ベクトルの二重計上**で、実質 1 本の検査。step 3 の λ の free 座標も step 2 と同じ `(1424, 2)`。
- 両側同じなので同一対象性には影響しない。**受領証の読み方の注意**として記録する。

### 【軽微】F-pkt-3. producer は零 support の character の 44 pairing を計算していない(checker は 176 全部を literal に計算)

- P `scan_roots:920` `if support:` — support が 0 の character では内側の 44 dot をスキップし、`values[character][seed]` は初期値 0 のまま。
- C `evaluate_roots:546-556` は `q` が零でも 44 本の dot を実行し、`require(len(values) == 176, "declared_root_pair_count"):553`。
- 数学的には同値(`⟨0, v⟩ = 0`)で、`values` はバイト一致要求で束縛されるので**穴ではない**。ただし「**両側が独立に 176 を計算した**」は正確ではない(P は 44 のみ)。実際に 176 を literal に計算しているのは checker だけ。

### 【軽微】F-pkt-4. seed2 の λ 非依存 pin は**両系統に置かれた同一 literal 定数**であり、独立証拠ではない

- `d972_r07_actual_grade2_root_scalar_batch_v2.py:170` と `check_d972_r07_actual_grade2_root_scalar_batch_v2.py:148` に同じ `SEED2_RAW_PACKED_SHA256 = "e67d0a0b…"`。P `:650-651` / C `:487-488` が各々これに対して照合。
- packet artifact に入るのは `D_s`(raw − P1 結合)であって raw seed 行ではないため、**当哨による外部再計算は不可**。2110 R1-2 の継続項目として毎回明記する。cert の宣言(`regression.seed2_char0_raw` = packed `e67d0a0b…` / support 568 / `lambda_independent: true` / `scalar_assertion_retired: true`)は確認した。

### 【軽微】F-pkt-5. **TCB が前周回の被検体を丸ごと飲み込んだ**。本周回の「新しい算術」は 3 つに限られる

| | 2117(materializer v3) | 今回(packet loop v2) |
|---|---|---|
| producer TCB(自身を除く pin 済モジュール) | 2 本(`3c93c50c` / `76546bef`) | **4 本**(+ `36cc620b` materializer_v3 + `973ccd1d` rank1355_root_seed_scalars_v1) |
| checker TCB(同) | 3 本(`e0237d10` / `8f718811` / `f3c7ca25`) | **4 本**(+ `eca60918` check_materializer_v3) |

- すなわち **2117 で「checker PASS・cross-checked(限定)」と格付けした pair が、今周回では前提モジュールになった**。二側性は保たれている(P は producer 系 v3、C は checker 系 v3 を引く)が、`physical_reduce`/`reduce_dense`・`normalize_pivot`/`normalize`・`update_target`/`next_target` の算術は**再利用であって今回打ち直していない**(§2 B)。
- したがって本周回で新しく二系統実装されたのは **(i) 44 本の packet 構築 (ii) `q_a = B_a^*λ` と 176 pairing (iii) loop 制御・耐久 prefix・parent layout** の 3 層のみ。格付け文面はこの層分けを明示すべき。

### 【軽微】F-pkt-6. resume 契約は producer 側だけの検査

- P `load_prefix:1075-1175` は既存 prefix の**メタデータ結合と rolling chain のみ**を検査し、**算術は再実行しない**(docstring `"arithmetic replay belongs to checker"`)。実際 step 1 は第 1 起動(`--max-appends 1`)、step 2/3 は第 2 起動(`--resume --max-appends 176`)で作られた。
- checker は resume 経路そのものを検査しない(候補ディレクトリの完全性と全 step の算術 replay のみ)。resume の実効性は **workflow の cap1 → resume176 の実 2 回起動** + `resume-before.json`(completed_steps 1)/ `resume-after.json`(1 → 3・`completed_prefix_unchanged: true`)の受領証で担保されている。当哨が両ファイルを実読して確認。
- 非対称の記録。checker が全 step を親からゼロ replay するので**判定には影響しない**。

### 【軽微】F-pkt-7. 「ROOT_SEEDS_ZERO は像の飽和ではない」の一文は**ソース docstring にしかない**

- producer `:7`「`ROOT_SEEDS_ZERO annihilates this fixed list; it is not an image-saturation certificate.`」/ checker 返書 946 F2 にも同旨。
- cert の JSON 側にあるのは `SCOPE.actor_origins_executed = 0` / `orbit_rows_executed = 0` と `CLAIMS.GRADE2_NONMEMBER = "NOT_DECIDED"` のみ。意味の一文は工房側で供給する必要がある。

### 見つからなかったもの(正直な範囲報告・保証ではない)

- **別対象・判定不能の余地**: 見つからなかった(19 継承規約 + 新設 6 のすべてで一致)。
- **import 交差辺**: 見つからなかった(§2 ②)。
- **cap → ROOT_SEEDS_ZERO の洗浄**: 見つからなかった。**両側に負のカナリアがある**。P `:1298-1301 live_root_and_cap_canary`(非零 root がある合成 scan に対し `terminal_for` が UNKNOWN_CAP / UNKNOWN_RESOURCE を返すことを要求)/ C `:965 reject_test(... "cap_not_empty")`(非零 root の scan に `ROOT_SEEDS_ZERO` を宣言させると拒否)。さらに実行時にも C `:717 nonzero_root_cannot_claim_empty` が働く。加えて `scan_roots` は `check_deadline` を一切呼ばないので、**scan が途中で打ち切られて偽の全零になる経路が存在しない**(完走するか例外で落ちるかの二択)。
- **silent cap**: 見つからなかった。宇宙(4 character × 44 seed・order・declared 176・max_appends 176・actor_origins_executed 0・orbit_rows_executed 0)は**両ファイルのモジュール定数 `SCOPE` としてバイト同一**に置かれ、`owner.json` に封印されて checker が `same()` で突合する(`:861`)。返書 945 に run 前から明記。P1 instruction/cache は 8059 行完全消費 + trailing 空検査 + rolling 再計算(P `:707-712` / C `:425-429`)、12 lower blob は全行 + trailing 空 + digest 一致(P `:757` / C `:468-470`)、44 seed 全部で lower 96776 座標零。cap は producer/checker 各 40 分 + `--max-seconds 1800`、job 130 分に対し**実測 producer 67.8 s + 22.4 s / checker 78.5 s** で全く効いていない。upload は checker PASS の**後**、diagnostics は `if: always()`。**fail-closed**。
- **事前登録違反**: 見つからなかった。選択された seed(35 → 36 → 37)は literal 凍結されておらず、pin 済み親 + packet + λ から決定論的に導出される。Sol 163 F2 は「stale な seed35/36 から予測するな」と明記しており、実際 step 1 の scan で非零だったのは `(0,35)` **1 本だけ**(seed 36 は λ_1356 では零)、step 2 で `(0,36)` と `(0,37)` が新たに非零化した。これは「未追加の行は旧 λ で零でも次の λ で非零になり得る」という Sol 163 F2 の予告どおりの挙動で、CEGAR が必要である理由の実測例。
- **ダミー検査(何にでも当たる試験)**: 見つからなかった。P の 3 カナリア群(`live_root_and_cap_canary` / `durable_before_head_canary` + `actual_prefix_roundtrip_canary` / `fresh_active_character_after_append_canary:1326` + owner 拒否)、C の 4 カナリア群(順序付き relation と derived 親 / fresh 4 root と cap / **再封された packet の破壊を拒否** / committed prefix)、および parent-layout の**両側 5 件ずつの否定試験**(`v3-flag-false` / `v3-flag-missing` / `rho2-packed-identity` / `unexpected-parent-schema` / `base-target-manifest`)はいずれも本周回の新規経路を狙い撃ちしている。とくに P `:1324-1326` は **append 後に active character が 1 → 3 へ変わることを要求**しており、「4 本の B-adjoint を毎回作り直す」(Task947 §2)が実効であることの負のカナリア。
- **「見つからなかった」を非存在と読む型**: **該当あり・ただし cert は正しく抑制している**。`ROOT_SEEDS_ZERO` は「この λ がこの固定 44 seed packet を消した」という**肯定的な有限事実**であり、`GRADE2_NONMEMBER = NOT_DECIDED`、`actor_origins_executed = 0`、`orbit_rows_executed = 0` が宣言されている。§3 F-pkt-1 / F-pkt-7 の 2 点だけが文面リスク。

---

## 4. ⑤ 入力 pin・終端受領証・第三実装再計算(すべて当哨が実測)

**入力 pin**(workflow env / producer literal / checker literal の 3 箇所が一致):
BASE `9944214057`(run 33891714539)/ DELTA(seed30)`9963533999`(run 33946247365)/ SEED34 `9966542166`(run 33956437467)/ P1 `9931437113`(run 33851744070)/ Task554 prepare + block0-3 `9865061266` `9865238399` `9865242284` `9865193269` `9865239848`(run 33677346616・**conclusion failure を明示要求**)/ Task712 `9915928157`(run 33814194630)。依頼文と一致。

**終端受領証**(candidate 9969090590 を download して実読):

```
terminal ROOT_SEEDS_ZERO / status PASS / completed_steps 3
rank 1359 / generation 8064 / state_head 7b7380a7ddb78591…
head_sha256 c48e8f673b7da860… / packet_manifest_sha256 d5e3ef0c0d691131…
owner_sha256 a8d206b0ae26f3bf… / scan.lambda_sha256 60ac649575400e98…
scan: declared 176 / informative 44 / nonzero_root_blocks [0] / nonzero_pair_count 0
lambda_rho2: mode derived / value 1 / original_rho2_directly_read false
claims: GRADE2_MEMBER NOT_DECIDED / GRADE2_NONMEMBER NOT_DECIDED / A0..IHARA NOT_DECLARED / verified false
checker-result: status PASS / prefix_steps_replayed 3 / packet_independently_rebuilt true
                raw_seeds_evaluated 44 / lower_coordinates_per_seed 96776
```

**F1 スイープ受領証(規律 ⑤ 項目 2)— 3 step すべてで外部再計算一致**

| step | rank_after | `direct_pairing.rows` | `row_pairings_sha256` | 当哨の `sha256(0x00 × rank_after)` |
|---|---:|---:|---|---|
| 1 | 1357 | 1357 | `f7d4a7a24961c7cf…` | **一致** |
| 2 | 1358 | 1358 | `ca62565d5682cfab…` | **一致** |
| 3 | 1359 | 1359 | `eeffd04f95f6c6ad…` | **一致** |

`lambda_pivots = 0`、`lambda_parent_remainder = 1`、`lambda_new_remainder = 1` は 3 step とも。producer は実際の内積値をバイト列に積んで hash し(`materializer_v3.check_final_separator:1304-1314`)、checker は定数 `sha(b"\0"*(old_rank+1))` を要求する(`:797`)ので、この 1 本が「全行が零だった」と「本数が rank_after だった」を同時に束縛する。**加えて start の 1356 行スイープを両側が独立に実行**(P `:525` / C `:349-359`・producer log の `final-separator-direct-pairings rows 1356` を実読)。

**head 連鎖(第三実装再計算)**: `sha(bytes.fromhex(parent_head) ‖ canonical(instruction body))` を当哨が Python で再計算 → **3 step とも `instruction.rolling_sha256` および `result.state_head` と一致**。
`d467e4e6…` → `75412b18…` → `6e7c802f…` → `7b7380a7…`。

**cert 内部整合(当哨の外部再計算)**: 全 step の `result.json` 再封成立 / 終端 `result.json` と `scan` の再封成立 / `HEAD` の再封成立 かつ `sha(canonical(sealed HEAD)) == result.head_sha256` / `lambda.bin` sha = `separator.lambda_sha256`(3/3)/ `physical-normalized.bin` sha = `pivot.normalized_sha256`(3/3)/ `target-remainder.bin` sha = `target.remainder_sha256`(3/3)/ `checker-result.result_sha256 == sha(canonical(result.json))` / packet manifest の 4 receipt を独立再ハッシュして全一致・`sha(canonical(manifest)) = d5e3ef0c…` が HEAD と result の `packet_manifest_sha256` と一致。

**外部照合(コードを介さず artifact のバイトから)**

1. **零 root の正体**: `sha256(0x00 × 9072) = 8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838` = character 1,2,3 の `roots[a].packed_sha256`(3 本とも)。→ **`B_a^*λ = 0`(a = 1,2,3)**。
2. **世代跨ぎの回帰錨**: packet の `tops.bin[34·9072 : 35·9072]`(character 0, seed 34)が、**2117 判読で当哨が独立に download していた seed34 v3 candidate の `output/source-d.bin` とバイト完全一致**(sha `e96170bf6812d7143feb9b77f9aa6d89313fdbf1b4e1c99aa3f7c50a8fc89f60`)。λ 非依存 packet が前世代の materializer の出力を再現していることの、コードを介さない確認。
3. **12 blob 完全消費の整数検算**: `total_authenticated_bytes = 67011332`。当哨が node で `ΣOLD_RANKS(2014)·(⌈6056/4⌉ + ⌈72576/4⌉) + ΣNEW_RANKS(6045)·⌈18144/4⌉ = 2014·19658 + 6045·4536 = 39591212 + 27420120 = 67011332` を独立導出 → **一致**。
4. **parent layout の両側一致**: artifact 同梱の `producer-parent-layout.json` と `checker-parent-layout.json` の `parent_layout` オブジェクトが**完全一致**(sha `2a8df24a305f6ebc…`)。`deltas[0]`(seed30)= `flag_present false / flag_value null / admission exact-accepted-legacy-target-chain`、`deltas[1]`(seed34)= `true / true / exact-accepted-v3-explicit-target-premise`。**producer は payload のバイト hash から、checker は result の宣言フィールドから**同じ記録に到達している(異なる起点)。両側の `rejected_cases` も同じ 5 件。
5. **DERIVED 親の名指し**: `accepted_target_derivation_parents` = base(`69fdcc8cd740f8ea…`)/ seed30(`36feb776736c6587…`)/ seed34(`d467e4e60b8bff88…`)。依頼文の 3 親と一致。
6. **resume の実効**: `resume-before.json` の `completed_steps = 1`、`resume-after.json` が `steps_before 1 → steps_after 3` かつ `completed_prefix_unchanged: true`。第 1 起動の `producer-first-result.json` は `terminal UNKNOWN_CAP` / `rank 1357` / `scan.first_hit = {character 0, seed 36, scalar 1}`。**cap が ROOT_SEEDS_ZERO に化けていない実例**。

**整数検算(node・整数のみ・全 20 本 OK)**: `2014 + 6045 = 8059` / `4·44·9072 = 1596672` / `⌈36288/4⌉ = 9072` / `⌈48384/4⌉ = 12096` / `4·6048 + 4·18144 + 8 = 96776` / `4·6048 = 24192` / `24192 + 4·18144 = 96768` / `⌈6056/4⌉+⌈72576/4⌉ = 19658` / `⌈18144/4⌉ = 4536` / `2014·19658 + 6045·4536 = 67011332`(= cert)/ `4·44 = 176` / `1·44 = 44` / `176 − 44 = 132` / `1354+1+1 = 1356` / `1356+3 = 1359` / `8061+3 = 8064` / lead 1418,1419,1420,1421 が連番 / `176 ≥ 3` / `176 − 2 = 174`(Sol 163 F2 の強い上界)。

**TCB 集合(規律 ⑤ 追加項目)**: source-receipt.json の 10 ファイルの bytes/sha が**リポジトリ作業コピーと全一致**。producer 側 = 自身 + `36cc620b` + `973ccd1d` + `3c93c50c` + `76546bef`。checker 側 = 自身 + `eca60918` + `f3c7ca25` + `e0237d10` + `8f718811`。データ pin 2 本(`fuda1_a0_rmax_data.g` `625b4d11…` / `a0_paper_words_v1.json` `90ba6033…`)は 2117 と同一。

---

## 5. CV-9 裁定案・工房格付け案(一行・前回書式)

> **CV-9 = 同一対象(限定 5 条)。工房格 = checker PASS(同一著者系統・本周回の新規差分は両側打ち直し(cross-side tok-sim AJ=True 0.06〜0.29 / AJ=False 0.20〜0.51・0.7 超は宣言ビルダーと封の定義のみ)・系統は完全分離(交差辺なし・系統 pin 4 本は 2110/2117 と同一 sha・両側 ARITH は producer 系/checker 系に分かれる)・packet 4 ファイル + manifest と全 3 step の 8 payload + manifest をバイト一致で相互束縛・終端 result.json も 176 個の pairing 値ごとバイト一致・ただし v15 seed 核と projector は 0.95〜0.98 クローン持ち越し、B_adj = Bᵀ 検査は 1.00 クローン)・cross-checked は限定つき** — (i) **射程 = 固定 44 seed packet に対する rank 1356 → 1359 の 3 周回のみ**。actor origin(32,236)・dual orbit・全物理像は**一切走査していない**(`actor_origins_executed = 0` / `orbit_rows_executed = 0`)。**grade-2 NONMEMBER ではない**(`GRADE2_MEMBER = GRADE2_NONMEMBER = NOT_DECIDED`・A0/COMMON/COFINAL_LIFT/FAKE/IHARA = NOT_DECLARED)(ii) **終端 176 pairing のうち情報を持つのは character 0 の 44 本のみ**。character 1,2,3 は `B_a^*λ = 0`(当哨が `sha256(0x00 × 9072) = 8f23754a…` を外部計算して確認)ゆえ**構造零 132 本**であり packet を試していない(cert は `informative_pair_count = 44` で正しく分離・2110 R1-1 / Sol163 F5 の事前登録どおり)(iii) rank 1354 状態の導出・884 旧 reduction・seed30 delta・seed34 delta(rank 1356 化)は**再計算せず前提**。`λ·ρ₂ = 1` は 2117 に続き**本 run でも計算していない**(明示 DERIVED = `mode:"derived"` / `original_rho2_directly_read:false` / 3 親 base `69fdcc8c…`・seed30 `36feb776…`・seed34 `d467e4e6…` を名指し)。実測したのは `λ·(親/新 target 剰余) = 1` と **λ ⊥ 全 rank_after 行の最終スイープ**(3 step とも `direct_pairing.rows == rank_after` ∧ `row_pairings_sha256 == sha(0x00 × rank_after)`・当哨が 3/3 外部再計算で一致・start の 1356 行スイープも両側独立に実行)(iv) **pivot 挿入・正規化・target 更新の算術は今周回の新規実装ではなく 2117 で格付けした pair の再利用**。本周回の新しい二系統実装は「44 本の packet 構築」「`q_a = B_a^*λ` と 176 pairing」「loop 制御・耐久 prefix・parent layout」の 3 層(v) **step 3 は target を動かしていない**(`target_scalar = 0`・step 2/3 の `target-remainder.bin` がバイト同一)ので「3 回 target を減らした」ではなく「rank を 3 上げ、target 剰余は 2 回変化した」。**主張 = 「rank 1356(head `d467e4e6…`・λ `f7406d70…`)から seed 35(lead 1419)・36(lead 1420)・37(lead 1421)由来の pivot を 3 本追加して rank 1359(head `7b7380a7…`・λ `60ac6495…`)とし、その λ が固定 44 seed packet の character 0 の 44 pairing をすべて消し(残り 3 character は `B_a^*λ = 0`)、target 剰余は依然非零であった」という有限事実。GRADE2 MEMBER/NONMEMBER = NOT_DECIDED・NONMEMBER ではない・verified = false(Lean 未)。**

---

## 6. 次周回の判読は何が要るか

**① + ⑤(+ TCB 集合 1 行)。②③ は条件つきで省略可。**

- **①(規約表の機械 diff)は今回も価値を出した**: 6 拡大・2 移行・**6 新設**を拾った。とくに新設 6 本(packet の λ 非依存性 / 4 分カウント / terminal 決定規則 / 耐久 prefix / 同一 owner resume / mixed-generation parent layout)は ① でしか出ない。弱化は今回ゼロだったが、CEGAR は周回ごとに前提を組み替えるので**弱化の検出は ① でしか拾えない**という 2117 の結論は据え置く。
- **②③ の省略条件(更新)**: 「系統 pin 4 本(`3c93c50c` / `76546bef` / `e0237d10` / `8f718811`)が同一 **かつ TCB のモジュール集合が前回と同一**」なら省略可。**今回は両側で 1 本ずつ増えたので不可だった**。次周回が packet loop v2 の直接の子(TCB が v2 pair を飲み込む)なら**また不可**になる見込み。
- **③ を測るなら AJ=False も併記**(2117 F-v3-1)。既存の 2096/2105/2110/2117 の数字は AJ=True 系列なので比較のため AJ=True も残す。
- **⑤ の恒久項目**(今回の実測を踏まえた更新版):
  1. 親 artifact id / run / 全 file pin が workflow env・producer literal・checker literal の 3 箇所で一致
  2. `direct_pairing.rows == rank_after` ∧ `row_pairings_sha256 == sha(0x00 × rank_after)` を**全 step**で外部再計算
  3. head 連鎖 `sha(parent_head ‖ canonical(instruction body)) == state_head` を**全 step**で外部再計算
  4. `roots[a].packed_sha256` が `sha256(0x00 × 9072)` と一致する character を数え、**informative / 構造零の内訳を必ず書く**(F-pkt-1 の恒久化)
  5. 各 step の `target.scalar` を並べ、0 が混じっていないか確認(F-pkt-2 の恒久化)
  6. packet の char0 seed30/34 行が保存 source-d とバイト一致(世代跨ぎ回帰錨・コードを介さない)
  7. `regression.seed2_char0_raw` = `e67d0a0b…` / support 568(2110 R1-2・**両系統の同一 literal 定数**であって独立証拠ではない旨を毎回付す)
  8. `lower_pass.total_authenticated_bytes` を rank 表から整数で独立導出
  9. TCB モジュール集合(source-receipt の 10 ファイル)と、**前周回の被検体が TCB へ移ったか**の 1 行
- **v15 seed 核(0.95〜1.00 クローン)が変わらない限り、raw seed 行と projector は二系統一致では永久に retire できない** — 格付け文面に毎回残す(2105 §7 から不変)。今回さらに `check_table_transpose` の 1.00 クローンを加える。

---

## 付録: 参照ファイル(絶対パス)

- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_fixed_root_packet_loop_v2.py`(sha256 `e040c7b3cf5f96fe…`・84173 bytes・1398 行)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_fixed_root_packet_loop_v2.py`(sha256 `5289253a82d942d7…`・66251 bytes・1054 行)
- `C:\Users\81905\Desktop\shadow-atelier\.github\workflows\d972-r07-fixed-root-packet-loop-v2.yml`(sha256 `329429a3e8bda846…`・496 行)
- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_fixed_root_packet_loop_v1.py`(比較元 `65169d7a…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_fixed_root_packet_loop_v1.py`(比較元 `c6a42021…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_actual_root_seed_materializer_v3.py`(producer TCB 新規 `36cc620b…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_actual_root_seed_materializer_v3.py`(checker TCB 新規 `eca60918…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_rank1355_root_seed_scalars_v1.py`(producer TCB 新規 `973ccd1d…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_targeted_grade2_owner_generated_join_v15.py`(`sparse_adjoint:192`)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_task_945_r07_fixed_root_packet_loop.md` / `luna_task_947_r07_packet_loop_takeover.md` / `luna_task_950_r07_packet_parent_layout_v2.md`
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_945_r07_fixed_root_packet_loop.md`(producer ABI・F2 module set)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_946_r07_fixed_root_packet_loop_checker_workflow.md`(checker F2/F3)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_952_r07_packet_parent_layout_delta_audit.md`(v2 差分の静的監査 PASS)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_953_r07_after_packet_oracle_intake.md`(次 oracle の intake)
- `C:\Users\81905\Desktop\shadow-atelier\sol\sol_reply_163_onboarding_astra_delta.md`(F2 = packet 定義と 174/176 上界と ROOT_SEEDS_ZERO の意味・F3 = oracle 切替・F5 = M3-1 DERIVED)
- `C:\Users\81905\Desktop\shadow-atelier\docs\notes\seed34_mat_v3_cv9_reading_v1.md`(裁定 2117・改訂規律)
- `C:\Users\81905\Desktop\shadow-atelier\docs\notes\r1355_rss_v1_cv9_reading_v1.md`(裁定 2110)
- 当哨の作業物: `C:\Users\81905\AppData\Local\Temp\claude\C--Users-81905-Desktop-shadow-atelier\d2b80bbe-2be7-426c-9dbe-a39ba301883a\scratchpad\cv9pkt\`(`cand\` `diag\` = download した artifact・`sim_pkt.py` `sim2.py` `sim_clone.py` = 類似度・`chk.js` = 整数検算)

---

本文(この区切りより上)の sha256 先頭 16 桁: 2ecba2b8a97c5fe9
