# full origin refinement v1(26 step・rank 1385)増分 CV-9 判読(falsifier 逐語・裁定 2131 で正本化)
著者: falsifier(opus/max・非当事者)。司令塔が scratchpad 報告書(sha256 先頭 16 桁 d7d9784b7cf4059e・保存ファイル全体)を逐語転記(2026-09-05)。

**工房裁定(2131)**: CV-9 = **同一対象**(限定 7 条・規約表 17 保持/5 拡大/1 移行/2 弱化/9 新設)。工房格 = **checker PASS(系統完全分離・全 26 scan/26 step をゼロ replay しバイト一致で相互束縛・保存 output 975 ファイルの不変を非当事者が全数確認・cap 不作動(completion checker 1,222 秒/7,200・producer resume 1,802/1,800 = 資源終端は実測どおり))・cross-checked は限定つき** — (i) 射程 = rank 1359 → 1385 の 26 周回のみ・**rank 1385 での全 origin scan は存在しない**(HEAD.current_scan = null)・NONMEMBER ではない (ii) informative は character 0 の 32,280 のみ・96,840 は構造零(char 1〜3 の q は 26/26 で零ベクトル)(iii) 26 step すべて actor origin(character 0・basis 506〜823・24 手が basis 815〜823 の 9 node に集中)・seed は一度も選ばれず 44 seed は 26 scan 全部で零 (iv) target.scalar 列に零 8 個(rank +26 / target 変化 18)(v) packet 3 step は前提・λ·ρ₂ は 3 周連続 DERIVED (vi) 挿入/正規化/target 更新は 2117 pair の再利用 (vii) **走査表の算術は 1 本のコードに帰着**(子 q_a = A_a* q の `sparse_adjoint` は両 join_v15 で本文バイト同一・homogeneous 値の `vectorized_projection_chunk` は 0.9908 かつ checker 側 docstring が "Independent bounded implementation" と誤宣言・本周回で初めて主エンジン化)、非クローン錨(`finite27_actor` の pushforward 側実測)の被覆は選択 26 点のみ = 0.0031 %。**独立性は 2125 より明確に低下**。弱化 2: scan が deadline 割込み可能に(緩和: 全 payload 生成後 os.replace で publish・部分 scan は出ない・scan=None は UNKNOWN_RESOURCE のみ)/ λ·ρ₂ の DERIVED 継続。GRADE2 NOT_DECIDED・verified=false。**判読規律(改訂)**: ①毎回・③は「その周回で新しく load-bearing になった関数対」を測る(継承 TCB でも)・②は同一 pair 継続 run なら省略可・⑤に恒久 4 件追加(終端 scan の有無・選択 origin の内訳と first_hit の生バイト再導出・非クローン錨の被覆率・UNKNOWN_RESOURCE 時の GHA 実測秒 vs max-seconds)+ seed2 pin 未実行の明記・completion 型 run では preserved-input 全数照合。

---

# CV-9 増分判読 — R07 **full origin refinement v1**(rank 1359 → 1385・terminal UNKNOWN_RESOURCE)

判読者: falsifier(反証前哨・非当事者)
対象: producer run `33967668257`/1(head `fd04734d20d472e7c09f31de3f92f8a50d6d841a`・**failure**)+
**checker-only completion run `33971897879`/1**(head `64475e1dfab1537a38d1b3131971bfed5fc3071c`・success)
親規律: 裁定 2125(`docs/notes/packet_loop_v2_cv9_reading_v1.md`・改訂規律 ①〜⑤・恒久項目 2 つ)/ 2117 / 2110 / 2105
判読範囲: 「producer と checker が同一対象を独立に計算しているか」の一点のみ(裁定 316/318 スコープ制限)
日付: 2026-09-05

---

## 0. 裁定

**同一対象(SAME OBJECT)。限定 7 条。別対象・判定不能の余地は見つからなかった。**

ただし **2125 と比べて「独立性」は明確に落ちている**。今周回の主役である
**32,280 origin の走査表は、両側とも継承 TCB の(ほぼ)クローンで計算されている**。
「両側が独立に 129,120 origin を計算した」とは**書けない**(§3 F-fo-1)。

producer `search/d972_r07_full_origin_refinement_v1.py`(sha256 `d7e32aad…`・97,806 B・1,545 行)と
checker `search/check_d972_r07_full_origin_refinement_v1.py`(sha256 `1ee388c9…`・75,083 B・1,154 行)は、

> rank 1359 の受理済み state から、**各周回で 4 character 分の `q = B^*λ` と 4 個の子 `q_a = A_a^* q` を作り直し**、
> character-major / seed 0..43 / basis_i 0..8058 × actor(1,-1,2,-2)の順に **32,280 origin/character = 129,120 origin**
> を評価し(seed は固定 44 packet との pairing、actor は v541 (4.1) `K_t b_i + T_{2,t} z_i` から ActRed を引いたもの)、
> **最初の非零 1 本だけ**を完全物理化(96,776 lower 座標の全消滅を要求)→ 挿入順 1 掃引 → 正規化 append →
> target 1 段更新 → λ 逆代入 → λ の全行スイープ、を繰り返す

という同一対象を計算している。checker は**全 26 scan・全 26 step を親からゼロ replay** し、
scan の 26 payload と step の 11 payload を manifest ごとバイト一致要求する
(`check_…_v1.py:846` → `FIXED.compare_directory`)。

**今回いちばん重い事実**(2125 と同型・規模拡大):
26 周回すべてで **active character は 0 のみ**。character 1,2,3 の root は恒等的に零ベクトル
(`packed_sha256 = 8f23754a…` = 当哨が外部計算した `sha256(0x00×9072)` と 26/26 一致)。
したがって declared 129,120 のうち **informative は 32,280(25%)**、**96,840 は構造零**。
cert は `informative_pair_count` / `structural_zero_pair_count` / `active_characters` で正直に分離している。

---

## 1. ① 規約表の機械 diff(packet loop v2 → full origin refinement v1)

凡例: P = producer / C = checker。**2125 の 25 規約のうち 17 が保持、5 が拡大、1 が移行、2 が弱化**。**新設 9**。

| # | 規約 | v2 → full-origin v1 | 判定 |
|---|---|---|---|
| 1 | 親を計算前に live 照合(`gh api` + `jq -e`) | 10 → **11 tuple**(packet run 33964709359 を追加)。id/name/bytes/digest/run/head + `expired==false` を全件・run の `status/conclusion` も全件(Task554 だけ `failure` 要求) | 拡大 |
| 2 | 違反の選択規則 | v2 = 4 root × 44 seed の最初の非零 → v1 = **4 root × 32,280 origin の最初の非零**。P `first_hit:520-538` / C `first_hit:534-548` | **拡大**(宇宙が 176 → 129,120) |
| 3 | 走査順 | v2 = character-major / seed 0..43 → v1 = **character-major / seed 0..43 / basis_i 0..8058 / actor slot 0..3**。両側の `SCOPE.order` はバイト同一文字列 | **拡大・一致** |
| 4 | root の生成 | P `fresh_vectors:411` = `ARITH.sparse_adjoint`(Python ループ)/ C `scan_arithmetic:479` = `FIXED.pullback`(`np.add.at`) | 一致(**二実装**・2125 と同じ) |
| 5 | **子 `q_a = A_a^* q`(新設)** | P `:412` / C `:480` **両側とも `ARITH.sparse_adjoint`**。producer 系 `join_v15.py:192` と checker 系 `check_…_join_v15.py:192` は**本文バイト同一** | **新設・実装は 1 本**(§3 F-fo-1) |
| 6 | P1 cache 1 パス収縮 | P `p1_contract:422-455`(`:448` `base.vectorized_projection_chunk`)/ C `dynamic_p1:387-412`(`:408` `BASE.vectorized_projection_chunk`)。256 行 chunk・digest pin・trailing 空検査は両側 | 一致(**ただし呼ぶ関数が 0.9908 クローン**) |
| 7 | actor 値 = homogeneous + lower-to-top − ActRed | P `actor_accumulator:458-517` / C `full_actor_values:415-472`。式は同一、batching は別(P は character ごと、C は active をまとめて) | 一致(**打ち直しあり** 0.31/0.47) |
| 8 | lower covector の生成 | P `:598 base.actor_adjoints` / C `:483 BASE.checker_actor_adjoints` | 一致(**0.72/0.79 の近クローン**) |
| 9 | 12 blob 認証 + 5 body read/active character | P `:513-515` / C `scan_io` に独立記録。両側 5/12/max1 | 一致 |
| 10 | 4 分カウント(declared / informative / structural-zero / nonzero) | P `scan_result:577-579` / C `scan_payloads:574-577`。式同一 | 一致 |
| 11 | 零 root character の全零要求 | P `:562-564 structural_zero_all_origins` / C は payload バイト一致で束縛 + P 側 `load_scan:675` | 一致 |
| 12 | terminal 決定規則 | P `terminal_for:1196-1204`(first_hit None → `ROOT_ORIGINS_ZERO` / resource → `UNKNOWN_RESOURCE` / cap → `UNKNOWN_CAP`)/ C `terminal_for_state:861-873`(**自前 scan から再導出**・非零 hit に `ROOT_ORIGINS_ZERO` を許さない・`scan is None` は `UNKNOWN_RESOURCE` のみ) | 一致(名称は `ROOT_SEEDS_ZERO` → `ROOT_ORIGINS_ZERO`) |
| 13 | 耐久 prefix(payload → manifest → publish → HEAD) | P `write_bundle:165-174` + `publish_directory:154`(`.pending-NNNNNN-uuid` → `os.replace`)/ C `audit_prefix_directory:850-859`(`.pending-*` `.orphan-*` を除外) | 一致 |
| 14 | 同一 owner resume | P `run_actual:1248-1252`(owner/start/source を `same` 要求)/ workflow が cap1 → resume32 の実 2 回起動 | 一致 |
| 15 | **scan と step の分離・cached scan(新設)** | 完全 scan を publish → HEAD が指す → step を publish → HEAD が進み **scan 参照を消す**。cap1 の最終 scan は resume で再利用(P `load_scan:617-653`)、**C は必ず再計算**(`replay_scan:931`) | **新設・一致** |
| 16 | **canonical P1 metadata index(新設)** | 6,078,393 B の `canonical-index.json`(sha `452fe97a…`)。instruction stream を 1 回だけ認証、decode 済み 8059×lift 行列は保持しない。P `canonical_index:348` / C `canonical_index:498` | **新設・一致** |
| 17 | 選択 actor の完全物理化 | P `materialize_actor:830-878`(`filtered_actor_source` = `ARITH._seed_act` 多項式 actor)/ C `materialize_actor:682-741`(**`finite27_actor:336` = 27 元通常群係数展開**・`_checker_seed_act` は**呼ばない**) | **新設・二実装**(§3 F-fo-6) |
| 18 | 96,776 lower 全零を slice 前に要求 | P `:865-866` / C `:718 LEGACY.require_lower_zero` | 一致 |
| 19 | ActRed correction の出所 | P `:855` = **cache 表** `scan["p1_values"][c,0,node]` / C `:710` = **生の decode lift** `dot(q, lift[2][a])` | **一致・二経路**(強い) |
| 20 | literal 受領証(`t*W*t^-1`・event 順・cancel 保持) | P `actor_literal:805` / C `actor_literal:668` | 一致(0.7634 = 宣言ビルダー) |
| 21 | 挿入順 1 掃引・正規化・target 1 段 | 2117 pair の**再利用**(`m.physical_reduce` / `LEGACY.reduce_dense` 等) | 一致(打ち直しなし) |
| 22 | λ の全行スイープ(2105 F1) | 全 26 step で `direct_pairing.rows == rank_after` ∧ `row_pairings_sha256 == sha(0x00×rank_after)`。start の 1359 行も C `:295-300` が実掃引 | 一致(26/26 当哨再計算) |
| 23 | `λ·ρ₂` | **明示 DERIVED 据え置き**(`mode:"derived"` / `original_rho2_directly_read:false`)。親 role が 3 → **6**(base / seed30 / seed34 / packet-step-1/2/3) | **弱化据え置き**(3 周連続) |
| 24 | 封の正規形・格の自己抑制 | `sort_keys` / ASCII / 末尾 LF。`candidate:true / cross_checked:false / verified:false` を全 JSON に。workflow が `jq -e` で要求 | 一致 |
| 25 | mixed-generation parent layout | 旧 5 + **新 5**(`packet-instruction-generic-seal` 他)= 10 否定試験。両側の receipt が**バイト同一**(sha `2b508eb5…`) | 拡大・一致 |
| **26** | **scan の deadline 割込み(新設・弱化)** | 2125 は「`scan_roots` は `check_deadline` を呼ばない = 途中打切りで偽の全零になる経路が無い」。**v1 の scan は `boundary()` 経由で割込み可能**(`p1_contract:451` `actor_accumulator:483` 等) | **弱化**(緩和策は §3 F-fo-2 末尾) |

**相互束縛**: C `compare_directory` が各 scan の **26 ファイル**(root/children/seeds/actors/p1/actor-lower ×4 + result + manifest)と
各 step の **11 payload + manifest** をバイト一致要求。終端 `result.json` 全体も `same(actual_result, result)`(`:987`)。

---

## 2. ②③ の省略可否 — **両方とも省略不可だった**(TCB が両側 +1)

### ②(import 交差辺): **交差辺は無い。**

- producer 鎖: `full_origin_refinement_v1` →(`exec_module`・sha pin `e040c7b3`)→ `fixed_root_packet_loop_v2` → `materializer_v3`(`36cc620b`)+ `rank1355`(`973ccd1d`)→ `batch_v2`(`3c93c50c`)→ `join_v15`(`76546bef`)。全て `d972_*`。
- checker 鎖: `check_full_origin_refinement_v1`(`:25-29` sha pin `5289253a`)→ `check_fixed_root_packet_loop_v2` → `check_materializer_v3`(`eca60918`)→ `check_batch_v2`(`e0237d10`)+ `check_rank1355`(`f3c7ca25`)→ `check_join_v15`(`8f718811`)。全て `check_*`。
- checker が producer ファイルに触れるのは `producer_source_receipt:259` の **sha 計算のみ**(import も exec もしない)。
- **系統 pin 4 本**(`3c93c50c` / `76546bef` / `e0237d10` / `8f718811`)は 2110/2117/2125 と**バイト同一**。
- **TCB は両側で 1 本ずつ増えた**: P = 4 → **5**、C = 4 → **5**。すなわち **2125 で格付けした pair(packet loop v2)が今周回の前提モジュールになった**(F-pkt-5 の予告どおり)。よって ②③ の省略条件は満たさない。

### ③(類似度): 測定した(AJ=True / AJ=False 併記・手法は 2117/2125 と同一 = ast 抽出 → tokenize → SequenceMatcher)。

**A. 本周回で打ち直された対(新しい算術)**

| 単位 | AJ=True | AJ=False |
|---|---:|---:|
| `P.append_step` ↔ `C.rebuild_step` | **0.0326** | 0.3990 |
| `P.selftest` ↔ `C.selftest` | 0.0621 | 0.1435 |
| `P.canonical_input` ↔ `C.source_lift` | 0.0787 | 0.3399 |
| `P.fresh_vectors` ↔ `C.scan_arithmetic` | 0.0832 | 0.2931 |
| `P.make_scan` ↔ `C.scan_arithmetic` | 0.0960 | 0.3061 |
| `P.materialize_seed` ↔ `C.materialize_seed` | 0.1163 | 0.5058 |
| `P.subtract_lifts` ↔ `C.source_lift` | 0.1165 | 0.2120 |
| `P.actor_relation` ↔ `C.actor_relation` | 0.1660 | 0.4260 |
| `P.scan_payloads` ↔ `C.scan_payloads` | 0.1974 | 0.2695 |
| `P.derived_rho2` ↔ `C.rho2_derivation` | 0.2105 | 0.2105 |
| `P.materialize_actor` ↔ `C.materialize_actor` | 0.2363 | 0.3563 |
| `P.terminal_for` ↔ `C.terminal_for_state` | 0.3106 | 0.3106 |
| **`P.actor_accumulator` ↔ `C.full_actor_values`** | **0.3118** | 0.4733 |
| `P.scan_result` ↔ `C.scan_payloads` | 0.3590 | 0.5231 |
| `P.p1_contract` ↔ `C.dynamic_p1` | 0.4341 | 0.5859 |
| `P.canonical_index` ↔ `C.canonical_index` | 0.4581 | 0.6014 |
| `P.head_record` ↔ `C.head_record`(宣言) | 0.5865 | 0.5865 |
| `P.first_hit` ↔ `C.first_hit` | 0.6302 | 0.6740 |
| `P.actor_literal` ↔ `C.actor_literal`(宣言ビルダー) | 0.7634 | 0.7634 |
| `canonical` / `sha`(封の定義) | 1.0000 | 1.0000 |

→ **新しい層にコピペ回帰は無い。** 0.7 超は宣言ビルダーと封の定義のみ。

**B. 継承 TCB の primitive(今周回で打ち直していない・しかし走査表の本体)**

| 単位 | AJ=True | AJ=False | 備考 |
|---|---:|---:|---|
| **`sparse_adjoint` ↔ `sparse_adjoint`** | **1.0000** | **1.0000** | **本文バイト同一**(両者 `…join_v15.py:192`)。**4 個の子を作る** |
| **`vectorized_projection_chunk` ↔ 同名** | **0.9908** | **0.9908** | 差分は **docstring 1 行 + エラーラベル 1 個だけ**。P1 収縮の全体 |
| `relation_source_sha256` ↔ 同名 | 0.9930 | 0.9930 | |
| `check_table_transpose` ↔ 同名 | 0.9701 | 0.9701 | `B_adj = Bᵀ` 検査 |
| `source_context` ↔ `checker_source_context` | 0.9254 | 0.9254 | |
| `old_covector_slices` ↔ `checker_old_slices` | 0.8545 | 0.8545 | |
| `new_covector_slices` ↔ `checker_new_slices` | 0.8042 | 0.8042 | |
| `stream_packed_dots` ↔ `checker_stream_dots` | 0.7954 | 0.8437 | 12 blob の dot |
| `actor_adjoints` ↔ `checker_actor_adjoints` | 0.7161 | 0.7904 | lower covector 生成 |
| `actor_adjoint` ↔ `checker_actor_adjoint` | 0.6100 | 0.7427 | 2096 (iii) の「近クローン錨」本体 |

**C. v15 seed 核クローンの持ち越し(不変・毎回の一句)**

| 単位 | AJ=True | AJ=False |
|---|---:|---:|
| `_seed_cv` ↔ `_checker_seed_cv` | 0.9821 | 0.9821 |
| `_seed_evaluate_seed` ↔ `_checker_seed_evaluate_seed` | 0.9782 | 0.9804 |
| `_seed_full_project` ↔ `_checker_seed_full_project` | 0.9712 | 0.9712 |
| `_seed_act` ↔ `_checker_seed_act` | 0.9467 | 0.9600 |

**raw seed 行と projector は二系統一致では永久に retire できない。** ただし今周回では
**checker は `_checker_seed_act` を一度も呼んでいない**(grep で新 checker 内 0 件)ので、
**選択された actor の像**についてはこのクローンから抜けた(§3 F-fo-6)。

---

## 3. 指摘

### 【重大】F-fo-1. 32,280 origin の走査表は、両側とも継承 TCB の(ほぼ)クローンで計算されている

本周回の主張の中心は「32,280 origin を走査して最初の非零を取った」だが、その配列を作る算術は次のとおり:

| 走査表の構成要素 | P 側 | C 側 | 二側性 |
|---|---|---|---|
| root `q = B^*λ` | `sparse_adjoint`(Python ループ) | `FIXED.pullback`(`np.add.at`) | **あり** |
| **子 `q_a = A_a^* q`(4 本 × 4 character)** | `ARITH.sparse_adjoint` | `ARITH.sparse_adjoint` | **なし(本文バイト同一)** |
| **homogeneous 値(5 × 8,059 / character)** | `base.vectorized_projection_chunk` | `BASE.vectorized_projection_chunk` | **ほぼ無し(0.9908)** |
| lower covector | `actor_adjoints` | `checker_actor_adjoints` | 弱(0.72) |
| 12 blob dot | `stream_packed_dots` | `checker_stream_dots` | 弱(0.80) |
| slice レイアウト | `old/new_covector_slices` | `checker_old/new_slices` | 弱(0.80–0.85) |
| ActRed 畳込みループ | `actor_accumulator` | `full_actor_values` | **あり**(0.31/0.47・batching も別) |
| seed 44 本の dot | `m.dot(root, packet_row)` | `dot(root, tops[a,seed])` | 形式のみ |

- `search/d972_r07_targeted_grade2_owner_generated_join_v15.py:192` と
  `search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py:192` の `sparse_adjoint` は
  **同じ行番号・同じ本文**(当哨が両者を print して逐字比較)。**子は本周回の新設オブジェクトなのに実装が 1 本しかない。**
- `search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py:271` の docstring は
  `"""Independent bounded implementation of the sparse packed projection."""` だが、
  `search/d972_r07_actual_grade2_root_scalar_batch_v2.py:342-` との差分は **docstring 1 行と
  `"projection_chunk_shape"` → `"checker_projection_chunk_shape"` のラベル 1 個だけ**。
  **本文は逐字コピー。**「independent」という宣言と実物の乖離 = CV-9 副検問が拾うべき stub 型。
  しかもこの関数は **v2 の pair では一度も呼ばれておらず**(grep: `fixed_root_packet_loop_v2` 両側に出現なし)、
  **本周回で初めて走査表の主エンジンになった**。
- 影響: 「同一対象か」には影響しない(両者は同じものを計算している)。**格付け文面に影響する** —
  「両側が独立に 129,120 origin を計算した」は誤り。言えるのは
  「**両側が独立に配列を再構成しバイト一致した。ただし homogeneous 値と子ベクトルの算術は 1 本のコードに帰着する**」まで。
  転記・バッチング・I/O のバグは捕まるが、**その 1 本が共有する意味論の誤りは二系統一致では捕まらない**。

### 【重大】F-fo-2. rank 1385 での全 origin scan は**存在しない**。terminal は `scan = null` の `UNKNOWN_RESOURCE`

- `output/HEAD` の `current_scan_manifest_sha256 = null`、`output/result.json` の `scan = null` / `scan_manifest_sha256 = null`(当哨が直読)。
- 26 個の scan は **rank 1359〜1384** のもの。**rank 1385 の λ について origin の値は一切測っていない。**
- checker `terminal_for_state:867-869` は `scan is None` なら `declared == "UNKNOWN_RESOURCE"` を要求するだけで、
  **「実際に資源で止まったか」は検査しない**。候補 artifact には **producer のログが同梱されていない**
  (top-level は checker.log / previous-checker.log のみ)。
- **当哨が外部で裏を取った**: GHA job API より producer resume step は
  `13:04:04Z → 13:34:06Z` = **1,802 秒**(`--max-seconds 1800` にちょうど当たっている)。
  `--max-appends 32 > 26` なので cap 側ではない。`output/` に `resource-stop.json` は無い(= 異常 exit3 経路ではなく正規終端)。
  よって **cap が零終端に化けてはいない**が、**その根拠は cert の外**にある。
- 割込み耐性(§1 #26 の緩和策): `make_scan` は全 payload を作ってから `write_bundle` →
  `.pending-NNNNNN-uuid` → `os.replace` で publish するので**部分 scan は publish されない**。
  `terminal_for(scan=None,…)` は `ROOT_ORIGINS_ZERO` を返せず、checker は `scan is None → UNKNOWN_RESOURCE` のみ許す。

### 【要修正】F-fo-3. informative は 32,280 のみ。96,840(75%)は構造零。26 scan すべてで active character は 0 だけ

- 全 26 scan で `roots[1..3].packed_sha256 = 8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838`
  = 当哨が外部計算した **`sha256(0x00 × 9072)`** と一致 ⇒ `B_a^*λ = 0`(a = 1,2,3)。
- `declared 129,120 / informative 32,280 / structural_zero 96,840 / nonzero 18,495〜18,723`(26 scan 全て)。
- 零 support の root では 4 個の子もすべて零(当哨が 26×3 = 78 本を確認)。
- 格付け文面で言えるのは「**character 0 の 32,280 origin を走査した**」まで。残り 96,840 は packet/actor を一切試していない。

### 【要修正】F-fo-4. 26 step の `target.scalar` 列に **0 が 8 個**。rank は 26 上がったが target 剰余は **18 回**しか動いていない

- 列: `[0, 2, 2, 2, 1, 0, 0, 1, 2, 2, 2, 0, 1, 0, 0, 2, 0, 1, 0, 1, 1, 1, 2, 1, 1, 1]`
  → 零は **step 1, 6, 7, 12, 14, 15, 17, 19**。
- 当哨がバイトを直読: 該当 step の `target-remainder.bin` は直前と**完全同一**(step 1 は start target `0a466426…` と同一)。
  26 step の distinct target は **19**(= start + 18 変化)。distinct λ は **26**(rank が毎回増えるため)。
- 副作用: 零 scalar の step では `lambda_parent_remainder` と `lambda_new_remainder` が**同一ベクトルの二重計上**、
  `free_coordinate` も直前と同じ(1434 が step 5,6,7 / 1442 が 11,12 / 1443 が 13,14,15 / 1445 が 16,17 / 1448 が 18,19)。
- 両側同じなので同一対象性には影響しない。**「26 回 target を減らした」は誤り**。正しくは
  「rank を 26 上げ、target 剰余は 18 回変化した」。

### 【軽微】F-fo-5. 26 step すべて **actor origin・character 0・basis_i 506〜823**。seed は一度も選ばれず、44 seed は 26 scan 全部で零のまま

- 全 26 の `origin_kind = "actor"` / `mode = "complete-filtered-actor"` / `character = 0`。
- basis_i: `507, 506, 815, 816, 816, 815, 816, 817, 817, 817, 818, 818, 819, 818, 819, 819, 820, 820, 821, 820, 821, 821, 822, 822, 822, 823`。
- **当哨が `seeds-c0.u8` を 26 本すべてカウント: 非零は合計 0 本。** 固定 44 packet は 26 pivot を通しても零のまま。
  (Sol 163 F2 の「旧 λ で零でも次で非零になり得る」は actor 側では実際に起きている —
  origin 2068 は scan 0 で零、scan 1 で非零。seed 側では 1 度も起きていない。)
- lead 列は非単調(1422, 1424, 1425, 1429, 1432, **1427**, 1428, 1434, …)= 挿入順掃引・単調要求なしと整合。
- **射程の材料(計画監査ではなく観測)**: step 3〜26 の 24 手が basis 815〜823 の **9 node** を消費している
  (≈ 2.7 step/node)。残り 7,235 node を同じ密度で消化すると **2 万手規模**になる。

### 【軽微】F-fo-6. finite27 錨は「各 step の選択 1 origin」だけ。19/26 で mixed が非零。表全体の被覆は 0.0031 %

- `check_…_v1.py:336-373 finite27_actor` は 27 元通常群係数への展開 + affine 置換で、
  producer の多項式 actor(`ARITH._seed_act`)とは別アルゴリズム。**`_checker_seed_act` は新 checker 内に 0 件**(grep 確認)。
- `:703-705` が `homogeneous_value == p1_values[a, slot+1, basis]`(左辺は `pushforward` = **順方向**で計算するので
  随伴恒等式 `⟨q, A·z⟩ = ⟨A^*q, z⟩` の実測になる)、`mixed_value == lower_values[a, basis, slot]`、
  `direct == (homog + mixed) % 3` を要求。`:709-712` の correction は **生の decode lift** から計算(P は cache 表)。
  `:722-723` が `dot(q, d) == selection.scalar == (direct − correction) % 3`。
  ⇒ **選択点については材料的に二側**。
- 実測(当哨が checker-result から集計): `mixed_scalar` は 26 中 **19 本が非零**(零は step 1,3,6,12,17,23,26)。
  `mixed_top_support` は 5,394〜89,094 で **全 26 本が非零ベクトル**。
- **被覆**: 26 錨 ÷(26 scan × 32,236 informative actor 値)= **0.0031 %**。
  裁定 2096 (iii) の「w_t の錨がクローン内に閉じる」は **選択された 26 点でだけ解けた**。走査表は依然クローン内。

### 【軽微】F-fo-7. seed2 の λ 非依存 pin は**本周回では一度も実行されていない**

- `SEED2_RAW_PACKED_SHA256` は本周回の 2 ファイルに **0 件**(grep)。packet は再構築されない
  (`checker-result.old_packet_rebuilt = false` / `old_packet_steps_numerically_replayed = 0`)ため、
  検査経路 `d972_…_batch_v2.py:390` を通らない。packet manifest `d5e3ef0c…` の hash 継承として premise 化。
- ⑤-7 の恒久項目は「本周回は未実行・2125 の packet 受領証から hash で継承」と書くのが正確
  (「両系統の同一 literal 定数であって独立証拠ではない」は不変)。

### 【軽微】F-fo-8. checker-result の 3 フィールドは literal 宣言(ただし実体は伴っている)

- `check_…_v1.py:991` の `"initial_current_lambda_row_pairings": 1359` と `"all_new_scalar_arrays_compared": True`、
  および `"lower_coordinates_per_selected_actor": 96776` は dict の**リテラル**であって測定値ではない。
- ただし実体は確認できる: (a) `load_accepted_start:295-300` が **1,354 base 行 + 5 saved 行**を実掃引し
  `dot(λ, target) == 1` を要求(log の `accepted_current_lambda_sweep` が 1 回)。
  (b) `compare_directory` が scan の 26 payload を全バイト比較し、canary `full_array_tail_corruption`
  (`:1089-1091`)が **`actors-c0.u8` の最終バイト改変を拒否** ⇒ **first-hit prefix で止まっていない**証拠。
- 同様に completion-run-receipt の `producer_output_unchanged: True` も literal だが、直前の assert 群を通過しないと到達しない。

---

## 4. ⑤ 入力 pin・終端受領証・第三実装再計算(すべて当哨が実測)

**入力 pin(11 + 1 tuple)**: P1 `9931437113`(run 33851744070)/ Task554 prepare + block0-3
`9865061266` `9865238399` `9865242284` `9865193269` `9865239848`(run 33677346616・**conclusion failure を明示要求**)/
Task712 `9915928157`(33814194630)/ BASE `9944214057`(33891714539)/ DELTA(seed30)`9963533999`(33946247365)/
SEED34 `9966542166`(33956437467)/ **PACKET `9969090590`(33964709359)**。
completion workflow は 12 番目に **REFINEMENT diagnostics `9970826495`(run 33967668257・`conclusion == "failure"` を要求**・
`d972-r07-full-origin-checker-completion-v1.yml:203`)。全 tuple が id|name|bytes|digest|run|head + `expired == false`。

**TCB / source pin**: `source-receipt.json`(sha `5d65f4313aaed81f…`)の **12 実行体 + 2 データ**を
当哨がリポジトリ作業コピーと突合 → **14/14 バイト一致**。
producer TCB(自身を除く)= `e040c7b3` `36cc620b` `973ccd1d` `3c93c50c` `76546bef`(**5 本**・2125 は 4 本)。
checker lineage = `5289253a` `eca60918` `f3c7ca25` `e0237d10` `8f718811`(**5 本**・2125 は 4 本)。
runtime = Python `3.13.15 … [GCC 13.3.0]` / NumPy `2.5.1`(completion workflow が exact equality を要求)。

**終端受領証**(candidate `9971466432` を download・当哨が実測 51,943,596 B・
sha256 **`0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8`** = GitHub API の `digest` と一致):

```
producer: status PASS / terminal UNKNOWN_RESOURCE / completed_steps 26 / rank 1385 / generation 8090
          state_head 8f6605a28d337cd8… / scan null / scan_manifest_sha256 null
          current_scan_manifest_sha256 null / kind Separator
          lambda_rho2: mode derived / value 1 / original_rho2_directly_read false / newly_executed_target_steps 26
          claims: GRADE2_MEMBER = GRADE2_NONMEMBER = NOT_DECIDED / DUAL_CLOSURES = NOT_EXECUTED
                  A0/COMMON/COFINAL_LIFT/FAKE/IHARA = NOT_DECLARED / verified false
checker : status PASS / terminal UNKNOWN_RESOURCE / prefix_steps_replayed 26 / complete_scans_replayed 26
          rank 1385 / generation 8090 / head_sha256 6bf3b4fce6a3f159… / result_sha256 04a88c1423f6d99f…
          old_packet_rebuilt false / old_packet_steps_numerically_replayed 0
          all_new_scalar_arrays_compared true / complete_actor_evaluations 26
          scan_io 26 件(active [0] / paired 32280 / structural-zero 96840 が 26/26)
          accepted_packet_artifact = 9969090590(run 33964709359/1・ZIP b15b0715…)
          checker_lineage 5 本 / candidate true / cross_checked false / verified false
```

**F1 スイープ + head 連鎖(第三実装再計算)— 26/26 一致**

- 全 26 step で `separator.direct_pairing.rows == result.rank_after` かつ
  `row_pairings_sha256 == sha256(0x00 × rank_after)`(当哨が Python で再計算・26/26 一致)。
  `lambda_parent_remainder = lambda_new_remainder = 1`、`lambda_pivots = 0` も 26/26。
- 全 26 step で `sha(bytes.fromhex(parent_head) ‖ canonical(instruction body without rolling_sha256))`
  = `instruction.rolling_sha256` = `manifest.state_head` = `result.state_head`(26/26 一致)。
  最終 `8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61` = `HEAD.state_head`。
- `HEAD` の封成立、`result.json` の封成立、`result.head_sha256 == sha256(HEAD ファイル全バイト)` = `6bf3b4fc…`。
- 全 26 step で `q_d == lambda_G`(値は 1 または 2)。
- payload hash join 26/26: `target-remainder.bin` / `lambda.bin` / `physical-normalized.bin` /
  `source-d.bin` / `source-full-top.bin`、および `result.scan_manifest_sha256 == sha(canonical(scan manifest))`
  = `manifest.scan_manifest_sha256` = `instruction.scan_manifest_sha256`。
- 全 26 step で `scan.first_hit == step.selection == materialization.selection`。

**外部照合(コードを介さず artifact のバイトから)— 当哨の独立実装**

1. **first_hit の再導出**: 26 scan すべてについて `seeds-cN.u8` / `actors-cN.u8` の生バイトから
   「character-major → seed 0..43 → basis_i × slot」順の最初の非零を当哨が探索 →
   **26/26 で cert の `first_hit` と完全一致**(character / origin_id / basis_i / actor / scalar)。
2. **配列 hash**: 26 scan × 4 character の `seed_values_sha256` / `actor_values_sha256` /
   `p1_values_sha256` / `actor_lower_values_sha256` / root / 子 4 本 = 計 **1,144 本**を再ハッシュ → 全一致。
3. **`nonzero_pair_count`**: 26 scan で当哨のバイト数え上げと一致。
4. **零 root の正体**: `sha256(0x00 × 9072) = 8f23754a…` を外部計算 → character 1,2,3 の
   `packed_sha256` と 26/26 一致。
5. **保存 output の不変**: `preserved-input.json` の **975 ファイル**を当哨が candidate 内で全数照合 →
   **欠落 0 / 不一致 0**、roster も一致(`output/` 配下 968)。`preserved_input_sha256 = 746e097f…` 再計算一致。
   origin = diagnostics `9970826495`(ZIP 51,954,614 B / `15c7686a…`・run 33967668257/1・head `fd04734d…`)。
   ⇒ **checker-only run は「同じ保存 output」を照合している。**
6. **新旧 result の分離**: `checker-result.json` sha `ccb0b3dd…`(= receipt の `new_checker_result_sha256`)、
   `previous-checker-result.json` sha `de95b68f…`(= `previous_checker_result_sha256`)。
   旧 = `status UNKNOWN / terminal UNKNOWN_RESOURCE / prefix 22 / scans 22 / phase new_actor_fold / 1804.649 s / candidate false`。
7. **parent layout の両側一致**: `producer-parent-layout.json` と `checker-parent-layout.json` は
   **バイト同一**(sha `2b508eb54d86cb55…`・JSON diff も空)。`rejected_cases` は
   旧 5 + 新 5 = 10。packet layout は rank 1359 / 3 step / `target_scalar` = `1,1,0`(零を拒否しない)。
8. **resume の実効**: `resume-before` = `completed_steps 1` + cached scan `8cb64841…`、
   `resume-after` = `steps_before 1 → steps_after 26` / `completed_prefix_unchanged: true`。
   checker は cached scan(scan 1)も**独立に再計算**している(step 2 の `replay_scan(1)`)。
9. **DERIVED 親の名指し**: base `69fdcc8c…` / seed30 `36feb776…` / seed34 `d467e4e6…` /
   packet-step-1 `75412b18…` / packet-step-2 `6e7c802f…` / packet-step-3 `7b7380a7…`(6 role)。
10. **cap は効いていない**: completion checker step `14:29:18Z → 14:49:40Z` = **1,222 秒**(内部 7,200 s / step 125 min / job 145 min)。
    producer resume step `13:04:04Z → 13:34:06Z` = **1,802 秒**(`--max-seconds 1800`)⇒ 終端理由は実測どおり資源。
    候補 upload は checker PASS の**後**のみ、diagnostics は `if: always()`。**fail-closed**。
11. **log の整合**: checker.log の phase 集計 = `new_full_scan_replay` 26 / `selected_complete_actor` 26 /
    `physical_insertion` 26 / `fresh_separator` 26 / `whole_step_replayed` 26 / `p1_scan` 832(= 26 × 32 chunk)/
    `fresh_roots` `old_lower_stream` `old_actor_fold` `full_origin_new_body` `new_actor_fold` 各 104(= 26 × 4)/
    `accepted_current_lambda_sweep` 1 / `terminal` 1。

**整数検算(node・整数のみ・23/23 OK)**:
`44 + 4·8059 = 32280` / `4·32280 = 129120` / `3·32280 = 96840` / `8059·4 = 32236`(`actors-cN.u8` バイト)/
`5·8059 = 40295`(`p1-cN.u8`)/ `4·9072 = 36288`(`children-cN.bin`)/ `⌈36288/4⌉ = 9072` / `⌈48384/4⌉ = 12096` /
`1359 + 26 = 1385` / `8064 + 26 = 8090` / `4·6048 + 4·18144 + 8 = 96776` / `4·6 + 2 = 26`(scan ディレクトリのファイル数)/
`⌈8059/256⌉ = 32` / `26·32 = 832` / `26·4 = 104` / `44 + 507·4 + 2 = 2074` / `44 + 823·4 + 1 = 3337` /
`3·32280 + 44 + 8058·4 + 3 = 129119`(canary の最終 origin)/ `1·32280 + 43 = 32323`(canary の char1 seed43)/
`26 − 8 = 18`(target 変化回数)/ `1 + 18 = 19`(distinct target)/ `823 − 815 + 1 = 9`(消費 node 数)。

**ダミー検査(何にでも当たる試験)の検出 — 見つからなかった。両側とも狙い撃ち。**

- P `selftest:1354-1418`: **非零** lower-to-top を要求(`canary_nonzero_actor_lower_to_top`・`lower_value in (1,2)`)、
  homogeneous-only 消費者を拒否(`mixed_value != homogeneous_value`)、
  **非零 hit のある scan に対し** `terminal_for(…,0,0,False) == UNKNOWN_CAP` /
  `terminal_for(…,0,CAP,True) == UNKNOWN_RESOURCE`(**cap → 零終端の洗浄を潰す負のカナリア**)、
  fixture scan で active character が **1 → 3** に変わること、prefix resume のバイト保存、
  owner 改変の拒否、`actors-c3.u8` の**最終バイト改変**の拒否。
- C `selftest:1033-1105`: finite27 の **逆写像 roundtrip**(actor 2 → -2)、
  `finite27_mixed_adjoint_canary`(`direct != 0` を要求し `checker_actor_adjoint` と分解一致)、
  `first_hit` を **character 1 の seed 43(index 32323)** と **最終 origin character 3 / basis 8058 / actor -2(index 129119)**
  で試験(= 実走では一度も現れない character の順序を試している)、
  `cap_with_nonzero_origin` + `reject_test(false_root_origin_eof)`、
  **`actors-c0.u8` の最終バイト改変を拒否**(= first-hit prefix で照合を止めていない証明)、
  `wrong_owner_head_seal`、`new_state_clears_cached_scan`。

**見つからなかったもの(正直な範囲報告・保証ではない)**

- **別対象・判定不能の余地**: 見つからなかった(26 規約すべてで一致・弱化 2 件は §1 #26 と #23 で明示)。
- **import 交差辺**: なし(§2 ②)。
- **cap → `ROOT_ORIGINS_ZERO` の洗浄**: なし(§3 F-fo-2 末尾)。ただし **scan 自体は deadline 割込み可能になった**
  (2125 からの弱化・§1 #26)。
- **silent cap / 事前登録違反**: なし。`SCOPE`(4 character・44 seed・8059 p1_rows・actors (1,-1,2,-2)・
  32,280/character・129,120 total・order 文字列・`operational_append_cap 32`・
  **`mathematical_total_bound: null`**)は両ファイルのモジュール定数として**バイト同一**で
  `owner.json` に封印、checker が `same()` で突合。選択された origin は literal 凍結されておらず、
  pin 済み親 + λ から決定論的に導出される。
- **echo(照合器が producer の出力をなぞるだけ)**: なし。checker は全 26 scan・26 step を親からゼロ replay し、
  自前計算バイトに対する完全 roster + バイト一致を要求する。cached scan(scan 1)も独立再計算。
- **「見つからなかった」を非存在と読む型**: **該当なし**。本 run は `ROOT_ORIGINS_ZERO` を主張していない
  (terminal は `UNKNOWN_RESOURCE`)。`GRADE2_NONMEMBER = NOT_DECIDED`・`DUAL_CLOSURES = NOT_EXECUTED` が宣言済み。

---

## 5. CV-9 裁定案・工房格付け案(一行)

> **CV-9 = 同一対象(限定 7 条)。工房格 = checker PASS(系統は完全分離(交差辺なし・系統 pin 4 本は 2110/2117/2125 と同一 sha)・全 26 scan と全 26 step を親からゼロ replay し scan 26 payload と step 11 payload をバイト一致で相互束縛・保存 output 975 ファイルの不変を非当事者が全数確認・両側に負のカナリア(cap → 零終端の洗浄を両側で拒否・配列の最終バイト改変を両側で拒否)・cap は一切効いていない(checker 1,222 s / 上限 7,200 s)。ただし新しい層(scan 制御・選択 actor の完全物理化・耐久 prefix)は打ち直し(cross-side tok-sim AJ=True 0.03〜0.46)である一方、**走査表そのものの算術は継承 TCB のクローンに帰着する**(子 `q_a` を作る `sparse_adjoint` は両系統で本文バイト同一、P1 収縮の `vectorized_projection_chunk` は docstring 1 行差の 0.9908・しかも checker 側の docstring は "Independent bounded implementation" と誤宣言、`actor_adjoint` 系は 0.61〜0.85)・v15 seed 核 0.95〜0.98 クローンも持ち越し)・cross-checked は限定つき** —
> (i) **射程 = rank 1359 → 1385 の 26 周回のみ**。**rank 1385 での全 origin scan は存在しない**(`HEAD.current_scan_manifest_sha256 = null` / `result.scan = null`)ので、最終 λ が何を消すかは**未測定**。**`ROOT_ORIGINS_ZERO` を宣言していない**し **grade-2 NONMEMBER でもない**(`GRADE2_MEMBER = GRADE2_NONMEMBER = NOT_DECIDED` / `DUAL_CLOSURES = NOT_EXECUTED` / A0・COMMON・COFINAL_LIFT・FAKE・IHARA = NOT_DECLARED)
> (ii) **26 scan すべてで active character は 0 のみ**。character 1,2,3 は `B_a^*λ = 0`(非当事者が `sha256(0x00×9072) = 8f23754a…` を外部計算して 26/26 確認)ゆえ **declared 129,120 のうち informative は 32,280(25%)・構造零 96,840(75%)は一切試されていない**
> (iii) **26 step すべてが actor origin(character 0・basis_i 506〜823)**。**seed は一度も選ばれず、固定 44 packet は 26 scan 全部で零のまま**(非当事者がバイト数え上げ・非零 0 本)。24 手が basis 815〜823 の 9 node に費やされている
> (iv) **`target.scalar` 列 `[0,2,2,2,1,0,0,1,2,2,2,0,1,0,0,2,0,1,0,1,1,1,2,1,1,1]` に零が 8 個**(step 1,6,7,12,14,15,17,19)。rank は 26 上がったが **target 剰余が動いたのは 18 回**(distinct target 19 / distinct λ 26・バイト直読)
> (v) rank 1354 導出・旧 reduction・seed30/34 delta・**packet 3 step は再計算せず前提**(`old_packet_rebuilt: false`)。`λ·ρ₂ = 1` は **3 周連続で未計算**(明示 DERIVED・6 親を名指し)。実測したのは `λ·(親/新 target 剰余) = 1` と **λ ⊥ 全 rank_after 行**(26/26 を外部再計算一致)と start の 1,359 行スイープ
> (vi) **挿入順掃引・正規化・target 更新の算術は 2117 pair の再利用**。本周回の新規二系統実装は「scan 制御と全配列の直列化」「選択 actor の完全物理化(checker 側は finite27 = 非クローン)」「耐久 prefix / cached scan / canonical index」の 3 層
> (vii) **finite27 錨は各 step の選択 1 origin だけ**(26 点・うち mixed 非零 19 点)。走査表 838,136 個の informative actor 値に対する被覆は **0.0031 %**。裁定 2096 (iii) の「w_t の錨がクローン内に閉じる」は**選択点でのみ解けた**
>
> **主張 = 「rank 1359(head `7b7380a7…`・λ `60ac6495…`)から、character 0 の actor origin 由来の pivot を 26 本追加して rank 1385(head `8f6605a2…`)とし、その各段で λ が全 rank_after 行に直交し target 剰余は非零のままであった。26 周回のどの段でも固定 44 seed は零、character 1〜3 の root は零、character 0 の actor origin は毎回 18,500 本前後が非零で残っていた」という有限事実。terminal は資源切れ(producer resume 1,802 s / 上限 1,800 s)。GRADE2 MEMBER/NONMEMBER = NOT_DECIDED・NONMEMBER ではない・verified = false(Lean 未)。**

---

## 6. 次周回(rank 1385 からの継続 run)の判読は⑤のみで足りるか

**足りない。① + ③ + ⑤ が要る。② は条件つきで省略可。**

- **① は省略不可**。今回 ① でしか出なかったものが 2 つある: **(a) scan が deadline 割込み可能になった**
  (2125 の「scan に割込みなし」からの弱化)、**(b) 子 `q_a` という新設オブジェクトが 1 実装しか持たない**。
  CEGAR は周回ごとに前提を組み替えるので、**弱化の検出は ① でしか拾えない**という 2117 の結論は据え置き。
- **③ は省略不可(2125 の条件を改定)**。2125 は「系統 pin 4 本と TCB 集合が同一なら ②③ 省略可」としたが、
  **今回 0.99 / 1.00 のクローンは ③ でしか出なかった**。
  **③ の測定単位は「新規関数対」ではなく「その周回で新しく load-bearing になった関数対」に改める**
  (`vectorized_projection_chunk` は継承 TCB だが**本周回で初めて**走査表の主エンジンになった)。
- **② は条件つき省略可**: 「TCB モジュール集合が前回と同一 かつ 系統 pin が同一 sha」なら省略可。
  次周回が full-origin v1 の**同一 pair の継続 run**(新モジュールを足さない)なら**省略可**。
  逆に v2 を切る/新モジュールを足すなら**不可**。
- **⑤ の恒久項目(今回の実測を踏まえた更新版)**:
  1. 親 artifact id / run / 全 file pin が workflow env・producer literal・checker literal の 3 箇所で一致
  2. `direct_pairing.rows == rank_after` ∧ `row_pairings_sha256 == sha(0x00 × rank_after)` を**全 step**で外部再計算
  3. head 連鎖 `sha(parent_head ‖ canonical(instruction body))` を**全 step**で外部再計算
  4. `roots[a].packed_sha256` が `sha256(0x00×9072)` と一致する character を数え、
     **active / informative / 構造零の内訳を必ず書く**(F-pkt-1 / F-fo-3 の恒久化)
  5. 各 step の `target.scalar` を並べ、**零の個数と target 剰余の実変化回数**を書く(F-pkt-2 / F-fo-4 の恒久化)
  6. **【新規・恒久】終端 scan の有無を明記**。`HEAD.current_scan_manifest_sha256` / `result.scan` が null なら
     「その rank での走査は存在しない」と一行で書く(F-fo-2)
  7. **【新規・恒久】選択 origin の内訳**(seed/actor・character・basis_i の帯)と、
     **生バイトからの first_hit 再導出**を全 scan で行う(F-fo-5)
  8. **【新規・恒久】非クローン錨の被覆率**を分数で書く。「錨があった」ではなく「N 点 / M 値」(F-fo-6)
  9. **【新規・恒久】終端が UNKNOWN_RESOURCE のとき、資源で止まった外部証拠**
     (GHA job step の実測秒 vs `--max-seconds`)を必ず取る。cert 内には無い(F-fo-2)
  10. `regression.seed2_char0_raw` は**本周回で実行されたか**を明記(今回は未実行・hash 継承のみ)(F-fo-7)
  11. TCB モジュール集合(source-receipt の 12 ファイル)と、**前周回の被検体が TCB へ移ったか**の 1 行
  12. **保存 output を再利用する completion 型 run では、`preserved-input` の全ファイルを非当事者が全数照合**(F-fo-2 の前提)
- **v15 seed 核(0.95〜1.00 クローン)が変わらない限り、raw seed 行と projector は二系統一致では永久に retire できない**
  — 格付け文面に毎回残す(2105 §7 から不変)。今回はさらに
  **`sparse_adjoint`(1.0000・本文バイト同一)と `vectorized_projection_chunk`(0.9908・独立と誤宣言)** を加える。

---

## 付録: 参照ファイル(絶対パス)

- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_full_origin_refinement_v1.py`(`d7e32aad…`・97,806 B・1,545 行)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_full_origin_refinement_v1.py`(`1ee388c9…`・75,083 B・1,154 行)
- `C:\Users\81905\Desktop\shadow-atelier\.github\workflows\d972-r07-full-origin-refinement-v1.yml`(`26cdca16…`・535 行)
- `C:\Users\81905\Desktop\shadow-atelier\.github\workflows\d972-r07-full-origin-checker-completion-v1.yml`(`74722395…`・631 行)
- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_fixed_root_packet_loop_v2.py`(producer TCB 新規 `e040c7b3…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_fixed_root_packet_loop_v2.py`(checker TCB 新規 `5289253a…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_actual_grade2_root_scalar_batch_v2.py:342`(`vectorized_projection_chunk`)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_actual_grade2_root_scalar_batch_v2.py:271`(誤宣言 docstring)
- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_targeted_grade2_owner_generated_join_v15.py:192`(`sparse_adjoint`)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_targeted_grade2_owner_generated_join_v15.py:192`(同上・本文バイト同一)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_task_954_r07_full_origin_refinement.md` / `luna_task_955_r07_full_origin_refinement_checker.md` / `luna_task_962_r07_full_origin_checker_completion.md`
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_954_r07_full_origin_refinement.md`(公開 ABI・F1 凍結・F3 TCB)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_955_r07_full_origin_refinement_checker.md`(F4 finite27・F8 TCB)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_962_r07_full_origin_checker_completion.md`(F1〜F4 保存物と pin)
- `C:\Users\81905\Desktop\shadow-atelier\docs\notes\packet_loop_v2_cv9_reading_v1.md`(裁定 2125・親規律)
- 当哨の作業物: `C:\Users\81905\AppData\Local\Temp\claude\C--Users-81905-Desktop-shadow-atelier\d2b80bbe-2be7-426c-9dbe-a39ba301883a\scratchpad\cv9fo\`
  (`cand.zip` `cand\` = download した candidate・`an1.py`〜`an4.py` = 受領証の外部再計算・`sim.py` = 類似度)

---

本文(この区切りより上)の sha256 先頭 16 桁: 8a2a6ee6a718dee9
