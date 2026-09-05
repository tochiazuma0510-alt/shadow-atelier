# CV-9 増分判読 — R07 **actual root seed materializer v3**(seed 34・rank 1355→1356)

判読者: falsifier(反証前哨・非当事者)
対象: GHA run `33956437467`(success)・terminal `Separator`・candidate artifact `9966542166`
親規律: 裁定 2110(`docs/notes/r1355_rss_v1_cv9_reading_v1.md`)/ 19 規約表の親 = 裁定 2105(`docs/notes/seed30_mat_v1_cv9_reading_v1.md`)
判読範囲: 「producer と checker が同一対象を独立に計算しているか」の一点のみ(裁定 316/318 スコープ制限)
日付: 2026-09-05

---

## 0. 裁定

**同一対象(SAME OBJECT)。限定 4 条。別対象・判定不能の余地は見つからなかった。**

producer `search/d972_r07_actual_root_seed_materializer_v3.py`(sha256 `36cc620b…`・1651 行)と
checker `search/check_d972_r07_actual_root_seed_materializer_v3.py`(sha256 `eca60918…`・1024 行)は、

> pin 済み親 artifact `9966008518`(rank1355 root seed scalars)の 176 スカラ列を走査順に再検査して**最初の非零** = (character 0, seed 34, scalar 1) を選び、その v541 違反を物理化し、**rank 1355 の受理済み Separator 状態へ挿入順で 1 pivot を追加**し、受理済み target 剰余をその 1 本だけで消去し、新 λ を逆代入で構成して**全 1356 行への直交性を最終スイープする**

という同一対象を計算している。

**今回いちばん重い変更**: `λ·ρ₂ = 1` が **実測から前提へ落ちた**(§3 F-v3-2)。両側が同じく落としているので同一対象性は保たれるが、2105 の格付け文面を流用すると過大主張になる。

---

## 1. ① 19 規約表の機械 diff(seed30 mat v1 → v3)

凡例: P = producer / C = checker。**16 規約が保持・一致**、**3 規約が強化**、**1 規約が弱化**、**1 規約が pin 経由へ移行**。

| # | 規約 | v1 → v3 | 判定 |
|---|---|---|---|
| 1 | 6 親を計算前に live 照合(`gh api` + `jq -e`) | 内訳が変化: ρ₂ が抜け **delta(seed30 候補)**が入る。P1/Task554/Task712/Separator は不変 | 一致(両側同一 workflow) |
| 2 | 違反の同一性 | v1 = seal `cba44225…`/`seed 30` を literal 凍結 → v3 = **literal を持たず** pin 済み親 result(`02a814c5…`)から導出 | **移行**(§2 で外部照合済) |
| 3 | 「最初の違反」の継承 | v1 は P が 2 点のみ(2105 F2)→ v3 は**両側とも 176 レコード全走査 + rolling 再計算 + first-nonzero**(P `:470-487` は `canonical(record)==line` のバイト厳密・C `:222-241`) | **強化 / 2105 F2 閉鎖** |
| 4 | SeedRed(seed) raw 事象列 | P `collect_selected_seedred:511-607` / C `combined_selected:296-335`。origin_id = `ORIGIN_RANGES[s][0]+seed` 不変 | 一致 |
| 5 | 事象の rolling 封(`sha(prev_hex ‖ canonical(event))`・零頭・畳込み前に封) | P `:582-588` / C `:322-328` | 一致 |
| 6 | mod-3 係数畳込み → 非零のみ・node 昇順 | P `np.flatnonzero:595` / C `sorted(dict):334` | 一致(別実装・support **1052**) |
| 7 | owner/kind 判定 | P segment 記述子 / C `OLD_OFFSETS`/`NEW_OFFSETS` 算術。定数不変 | 一致(当哨が 8059 node 全部で再照合・不一致 0) |
| 8 | 物理化写像 `+(3−c)·row ≡ −c·row` | P `add_scaled(...,3-coefficient):865` / C `subtract(...,coefficient):421` | 一致(式同値・書き方は別物) |
| 9 | 下位 96776 座標の完全消滅 | P `:898-899` / C `require_lower_zero:442` | 一致 |
| 10 | v541 filtered projector を完全欠損にのみ当て top = 平凡 character slice | P `:937-966` / C `:443-446` | 一致(cert で `source-d.bin` sha = `e96170bf…` = `plain` = `full_projector` の両者) |
| 11 | `q·d = 1` / `λ_old·G = 1` / `B*q` 一致 | P `:914-917,1458` / C `:597-600,837` | 一致(cert `pairings = {q_d:1, lambda_G:1, B_adjoint_q_equal:true}`) |
| 12 | 挿入順 1 掃引・lead 一意・単調要求なし・free 座標で打切らない | P `physical_reduce:1239-1267` / C `reduce_dense:539-558` | 一致(両側とも掃引後に全旧 lead 零を要求) |
| 13 | 正規化 `normalized = remainder·scale` | P `normalize_pivot:1270-1281` / C `normalize:561-568` | 一致・**非対称の向きが反転**(§3 F-v3-4) |
| 14 | 新 target 段は新 pivot 1 本のみ | P `update_target:1284-1298` / C `next_target:571-579` | 一致(`new_target_eliminations = 1`) |
| 15 | λ = 新 target 剰余の最初の非零を free、pivot_id 降順で逆代入 | P `separator_after_append:1318-1356` / C `next_separator:710-742` | 一致 |
| 15′ | **λ の最終全行スイープ**(新設) | P `check_final_separator:1301-1315`(pairings バイト列を積んで sha)/ C `:733-740`(`final_lambda_allrows` ループ + `normalized` + remainder) | **新設 / 2105 F1 閉鎖** |
| 16 | 「依然 Separator」の判定 | P `first_nonzero(target_raw):1515` / C `np.any(updated):883` | 一致 |
| 17 | λ の受理条件 3 本 | `λ·normalized = 0` と `λ·new_target = 1` は不変。**`λ·ρ₂ = 1` が実測 → 前提**(v1 は第 1 引数 = `rho2_raw`、v3 は `state["old_remainder"]`) | **弱化**(§3 F-v3-2) |
| 18 | 封の正規形(`sort_keys=True`) | P `sealed:162` / C `seal:103` | 一致(cert の result.json 再封が成立) |
| 19 | 格の自己抑制 | P `CLAIMS:118` / C `CLAIMS:66`・workflow `:368` が `cross_checked == false` を**要求** | 一致 |

**相互束縛(不変)**: C `compare_candidate:?` は自前計算バイトに対し全 9 ファイル + roster + **manifest 再構成**の一致を要求。コメントに「self-consistent resealing cannot supply authority」。当哨も manifest の 8 receipt を独立に再ハッシュして全一致。

---

## 2. ②③ の省略可否 — **③ は省略できなかった**

### ②(import 交差辺): 省略条件を満たす。交差辺は無い。

- producer の import/exec は `d972_*` のみ(`load_pinned_module` で `root_scalar_batch_v2`、`join_v15` は sha 照合のみ)。
- checker の import は `check_*` のみ(`BASE = check_..._root_scalar_batch_v2`、`ROOTS = check_..._rank1355_root_seed_scalars_v1`)。`ROOTS` 自身も `BASE` しか import しない。
- **系統 pin 4 本は 2110 とバイト同一**: `3c93c50c…` / `76546bef…`(P 側)、`e0237d10…` / `8f718811…`(C 側)。
- ただし **checker の TCB に新規 1 本**が入った: `check_d972_r07_rank1355_root_seed_scalars_v1.py`(`f3c7ca25…`)。checker 系統であり 2110 で判読済み。producer 側は逆に `physical_state_separator_v2`(`b068c9f3…`)を**退役**。

### ③(類似度): **「定数差し替え版」ではなかったので再測定した。**

省略条件(前周回ファイルの定数差し替え版であることを diff 1 本で示す)は成立しない:

| | 同一 | 書き換え | 新規 | 退役 |
|---|---:|---:|---|---|
| producer(44 関数) | **34** | 3(<0.70) | `check_final_separator` / `collect_selected_seedred` / `replay_selected_seed` / `validate_current_state` / `validate_old_state` | `collect_seedred30` / `replay_seed30` / `validate_state_parent` / `_source_receipt_expected` |
| checker(39 関数) | **24** | 7(<0.70) | `changed_after_reverse` / `combined_selected` | `combined_seed30` / `parser` |

書き換えの内訳(v1 → v3 同側・AJ=True): P `validate_scalar_parent` 0.156 / `join_parents` 0.379 / `selftest` 0.303。C `load_scalar` 0.183 / `expected_parents` 0.376 / `load_state` 0.371 / `selftest` 0.366 / `check_actual` 0.453 / `b_and_pairings` 0.491 / `main` 0.634。新規ロジックは (i) 親選択・認証層、(ii) F1 最終スイープ、(iii) 二親状態検証、に集中。

**測定結果(両側・2105 と同一手法)**:

| 単位 | AJ=True | AJ=False | 2105(v1) |
|---|---:|---:|---:|
| `collect_selected_seedred` ↔ `combined_selected` | 0.1614 | 0.3368 | 0.1770 |
| `physical_reduce` ↔ `reduce_dense` | 0.2255 | **0.6600** | 0.2255 |
| `normalize_pivot` ↔ `normalize` | 0.5806 | 0.5806 | 0.5806 |
| `update_target` ↔ `next_target` | 0.5090 | 0.5090 | 0.5090 |
| `separator_after_append` ↔ `next_separator` | **0.4327** | 0.5984 | 0.5055 |
| `check_final_separator` ↔ `next_separator` | 0.2185 | 0.3217 | (新設) |
| `replay_selected_seed` ↔ `reconstruct_defect` | 0.1196 | 0.3467 | 0.1210 |
| `validate_current_state` ↔ `load_state` | 0.1073 | 0.1836 | 0.2121 |
| `validate_old_state` ↔ `load_state` | 0.1782 | 0.3432 | (新設) |
| `selftest` ↔ `selftest` | 0.1817 | 0.3076 | 0.1254 |

→ **コピペ回帰なし。** cross-side は 2105 と同水準かそれ以下(λ 逆代入対は 0.5055 → 0.4327 に低下)。承知のクローン対は 1.000。

**v15 seed 核クローンは持ち越し(不変)**: base pin 4 本が同一なので `_seed_evaluate_seed ↔ _checker_seed_evaluate_seed`(0.98)、`_seed_full_project ↔ _checker_seed_full_project`(0.97)等は 2105 の測定がそのまま生きる。**raw seed 行と projector は二系統一致では永久に retire できない**(毎回残す一句)。

---

## 3. 指摘

### 【要修正】F-v3-1. 公表されてきた類似度は difflib の autojunk により長い関数で系統的に過小

当哨が v1 pair を自前スクリプトで再測定したところ、`autojunk=True`(difflib 既定)で **2105 の 11 値を 11/11 完全再現**、`autojunk=False` では長い 6 対だけが 0.12〜0.23 → 0.31〜0.66 に上がり、短い 5 対(pack/unpack/dot/normalize/update_target)は不変だった。原因は autojunk の「長さ 200 超の系列で 1% 超出現する要素を junk 扱い」— Python ソースでは `(` `)` `,` `=` `require` `<STR>` 等、**まさに共有された定型部分**を捨てる。③ の目的がコピペ検出である以上、junk を捨てた数字は独立性を実際より良く見せる。判定は変わらない(クローンは 0.95〜1.00、最大の 0.6600 でも遠い)が、**次回から AJ=False も併記**すべき。

### 【要修正】F-v3-2. `λ·ρ₂ = 1` が実測から前提へ落ちた — 2105 の格付け文面を流用すると過大主張

- v1: workflow が ρ₂ を `gh api` + `stage_..._rho2_v9_flat_v4.py` で stage し、producer `:1309-1311` が `rho2_raw` を読み、`separator_after_append(rho2_raw, ...)` の第 1 引数として `dot(λ, ρ₂) == 1` を**実測**していた。
- v3: workflow に ρ₂ の取得も stager も**無い**(親 6 本の 6 本目は delta)。producer `:1534` は第 1 引数に `state["old_remainder"]`(親 target 剰余)を渡す。checker docstring も「no actors, old target solve or rho2 IO」と明記。
- cert は `separator.lambda_rho2 = 1` を出すが、その根拠欄は `lambda_rho2_basis: "accepted-parent-target-derivation"`、`parents.rho2.target_derivation_accepted_as_premise: true`。
- **判定への影響は無い**(両側が同じく前提化しており、宣言も正直・別対象ではない)。**格付け文面への影響は大きい**: 「λ·ρ₂ = 1 を両系統が独立に計算した」は今回**言えない**。言えるのは「λ·(親 target 剰余) = 1 かつ λ ⊥ 全 1356 行」まで。ρ₂ への橋は `target-remainder ≡ ρ₂ mod span` という**親由来の前提**。

### 【軽微】F-v3-3. checker の否定試験が 10 → 3 に減った

v1 checker は `reject_test` 呼び出し 10 箇所(2105 §4「8 種」+ 他)。v3 は 3 箇所(`stale_selected_seed` / `stale_parent_head` / `bad_row_in_final_lambda_pass`)。docstring が「Only changed-interface canaries; no old suite or parent arithmetic」と意図を宣言している。持ち越しコード経路の in-repo な負の網は薄くなったが、`compare_candidate` のバイト相互束縛が強いので**同一対象判定には影響しない**。記録のみ。

### 【軽微】F-v3-4. 正規化の非対称の向きが反転

- P `normalize_pivot(remainder, old_leads)`: `lead not in old_leads` ∧ 旧 lead 全零 ∧ 正規化後も旧 lead 全零 を要求。
- C `normalize(remainder)`: `old_leads` を取らない(`reduce_dense` 側の `earlier_pivot_zeros` で担保)。

結論同値で強い側が producer。2105 では Conv 3 で強い側が checker だった(その非対称は今回解消)。cert 文面で「再確立された」と書くなら根拠側を明記すること。

### 【軽微】F-v3-5. v15 seed 核クローンの持ち越し(2105 から不変・毎回の一句)

base pin 4 本が同一である限り、raw seed 行と filtered projector の「独立実装」の実体は 0.97〜0.98 クローン対である。今回の錨は Task712(独立親)との degree-2 一致、`q·d = 1` / `λ_old·G = 1` の 2 対 pairing、および §4 の外部照合。

### 見つからなかったもの(正直な範囲報告・保証ではない)

- **別対象・判定不能の余地**: 見つからなかった(19 規約 + 新設 1 のすべてで一致)。
- **import 交差辺**: 見つからなかった。
- **silent cap**: 見つからなかった。task554 blob・P1 instructions(8059 行)・state instructions(1354 pivot)はいずれも完全消費 + trailing 空検査 + rolling 再計算(P `:631,788,1090,1093` / C `:350,371,653,671,673`)。scalars.jsonl は両側 176 行全消費。cap は producer/checker 各 40 分・job 90 分で、超過時は job 失敗 → candidate 未 upload(upload は checker PASS gate の**後**)、diagnostics は `if: always()`。**fail-closed**。
- **事前登録違反**: 見つからなかった。seed は literal で凍結されていないが、pin 済み親 artifact のバイト(`02a814c5…`)で決定論的に固定されており、当哨が親 artifact を独立に download して走査順最初 = seed 34 を確認(§4)。
- **ダミー検査(何にでも当たる試験)**: 見つからなかった。残る 3 つの reject は本周回の新規経路を狙い撃ちしている。とくに C `changed_after_reverse:972-979` は **row 0 の 2 回目の読み(= 逆代入後の最終スイープ)でだけ行を壊し**、`next_separator` が拒否することを要求する — F1 スイープが実効であることの負のカナリア。P 側も `check_final_separator` に不正行を与えて例外理由の prefix `final_separator_nonzero_row:` まで検査する。**2110 R1-3 は両側で閉鎖。**
- **「見つからなかった」を非存在と読む型**: 該当なし。主張は seed 34 の物理化という肯定的事実。

---

## 4. ⑤ 入力 pin・終端受領証・外部照合(すべて当哨が実測)

**入力 pin**: SCALAR `9966008518`(run 33954712636)/ DELTA `9963533999`(run 33946247365)/ STATE `9944214057`(run 33891714539)— 依頼文と一致。**producer の literal 定数と checker の `ROOTS.DELTA_FILES` / `ROOTS.STATE_FILES` が全項目一致**(別ファイル由来の 2 系統が同じ親バイトを指す)。

**終端受領証**(candidate 9966542166 を download して実読):

```
kind Separator / rank_before 1355 / rank_after 1356 / new_pivots 1
new_target_eliminations 1 / old_target_reductions 885 (= 884+1)
physical_reductions 902 / selected_rows 1052 / literal_p1_roots 1445 / raw_events 2756
lower_zero_count 96776 / seed 34 / character 0 / old_state_derivation_premise true
state_head d467e4e6… / claims GRADE2 NOT_DECIDED / cross_checked false / verified false
```

**F1 スイープ受領証(規律 ⑤ の格上げ項目・名前が変わっている)**

- 規律の `old_state_rows_checked + new_pivot_rows_checked = rank` は、v3 では**親(rss_v1)受領証の再検査**として残る: P `:404-405` / C `:202` が `1354 + 1 = 1355 = rank_before` を要求。
- **今周回分の受領証は `separator.direct_pairing`**: `rows = 1356 = rank_after`、`lambda_pivots = 0`、`lambda_parent_remainder = 1`、`lambda_new_remainder = 1`、`row_pairings_sha256 = 216d4302eb1c96fd35681515646489b476746fb14145ac77493ca86fef22d5c6`。
- **当哨の外部計算**: `sha256(0x00 × 1356) = 216d4302eb1c96fd3568…` → **一致**。producer は実際の内積値をバイト列に積んで hash し(`check_final_separator:1305-1308`)、checker は定数 `sha(b"\0"*1356)` を要求するので、この 1 本が「1356 本すべてが零だった」と「本数が 1356 だった」を同時に束縛する。
- 行の内訳: 1354(state/physical.bin)+ 1(seed30 delta pivot)+ 1(新 pivot)= 1356。checker `row_reader:839-841` が `index < 1354` で physical.bin、以降 `saved_pivot` に切替。transcript も 1356 本(pivot_id 1355 → 0)。

**外部照合(コードを介さず artifact のバイトから)**

1. **走査順**: rss_v1 候補の `seed-scalars-a0.bin` を直読 → `[0:34]` 全零・`[34] = 1`・非零は `(34,1) (35,2) (36,2)` のみ、a1/a2/a3 は**全零**。よって character-major 176 列の最初の非零は index 34 = (character 0, seed 34)。`scalars.jsonl` 176 行の最初の非零レコードも同一。
2. **2110 R1-2 の凍結 pin**: `direct_receipt.raw_row_packed_sha256[2] = e67d0a0b21aaf41fd1617811b45cd51191a0087c7d04fcc33dda5a58f4fcfca6`・`raw_row_support[2] = 568` → **無傷**。
3. **今周回の選択行**: 親の `raw_row_packed_sha256[34] = 5990517725f4a2cd…`・`raw_row_support[34] = 1464` が v3 cert の `raw_seed.selected_direct_receipt`(`packed_sha256 5990517725f4a2cd…` / `support 1464`)と一致。
4. **head 連鎖**: `sha(bytes.fromhex(36feb776…) ‖ canonical(instruction body))` を当哨が再計算 → `d467e4e6…` **一致**(rank 1356・generation 8061・lead 1418・offer 8060)。
5. **cert 内部整合**: `result.json` 再封成立 / `checker.result_sha256 == sha(canonical(result))` / `lambda.bin` sha = `f7406d70…` = `separator.lambda_sha256` / `physical-normalized.bin` sha = `a17e774a…` = `transcript[0].row_sha256` / `source-d.bin` sha = `e96170bf…` = `plain_character_source_sha256` = `full_projector_character_source_sha256` / manifest の 8 receipt を独立再ハッシュして全一致。
6. なお `selected_direct_receipt.scalar = 2` と `first_violation.scalar = 1` は**別量**(前者 = `direct-seeds-a0.bin[34]` = 2、後者 = `seed-scalars-a0.bin[34]` = 1)。当哨が両バイトを直読して確認、矛盾ではない。

**整数検算(node・整数のみ・全 22 本 OK)**: `ΣOLD_RANKS 2014` / `ΣNEW_RANKS 6045` / 計 `8059` / OLD・NEW_OFFSETS が階段和と一致 / `ORIGIN_RANGES` 総計 `8232` / `4·6048+4·18144+8 = 96776` / `⌈48384/4⌉ = 12096` / `1354·12096 = 16377984` / `1354·2015 = 2728310` / `⌈36288/4⌉ = 9072` / `1354+1 = 1355` / `1355+1 = 1356 = direct_pairing.rows` / `884+1 = 885` / **owner/kind 写像が 8059 node 全部で両側一致(不一致 0)**。

---

## 5. CV-9 裁定案・工房格付け案(一行・前回書式)

> **CV-9 = 同一対象(限定 4 条)。工房格 = checker PASS(同一著者系統・本周回の差分は両側打ち直し(cross-side tok-sim AJ=True 0.11〜0.58 / AJ=False 0.18〜0.66・2105 と同水準以下)・系統は完全分離(交差辺なし・系統 pin 4 本は 2110 と同一 sha・checker TCB に判読済 `f3c7ca25…` が 1 本追加)・候補全 9 ファイル + manifest をバイト一致で相互束縛・ただし v15 seed 核と projector は 0.97〜0.98 クローン持ち越し)・cross-checked は限定つき** — (i) 射程 = 走査順最初の違反 **(character 0, seed 34, scalar 1)** の 1 周回のみ(actor origin 44..32279 と orbit は未走査・character 1,2,3 は親 run で全零) (ii) rank 1354 状態の導出・884 旧 target reduction・seed30 delta(rank 1355 化)は再計算せず前提 (iii) **`λ·ρ₂ = 1` は本 run では計算していない**(ρ₂ を一切読まない・根拠は `lambda_rho2_basis: accepted-parent-target-derivation` = 親由来の `target-remainder ≡ ρ₂ mod span`)。本 run が実測したのは `λ·(親 target 剰余) = 1` と **λ ⊥ 全 1356 行の最終スイープ**(`direct_pairing.rows = 1356 = rank_after`・`row_pairings_sha256 = 216d4302…` = `sha(0x00×1356)`・当哨が外部計算で一致確認・裁定 2105 F1 は materializer 系でも閉鎖・2110 R1-3 の負のカナリアも両側で新設) (iv) 選択 seed は literal 凍結ではなく pin 済み親 artifact `02a814c5…` 経由の決定論的導出(当哨が親バイトを直読して走査順最初 = seed 34 を外部確認)。**主張 = 「rank 1355(head `36feb776…`・λ `f83bbaa5…`)に seed 34 由来の pivot 1 本(lead 1418・offer 8060)を追加して rank 1356(head `d467e4e6…`・λ `f7406d70…`)とし、target 剰余が依然非零であった」という有限事実。GRADE2 MEMBER/NONMEMBER = NOT_DECIDED・NONMEMBER ではない・verified = false(Lean 未)。**

---

## 6. 次周回の判読は ⑤ のみで足りるか

**足りない。次周回は ① + ⑤(+ TCB 集合の 1 行)。②③ は条件つきで省略可。**

- **①(規約表の機械 diff)は今回も価値を出した**: 3 規約が強化・1 規約が弱化(`λ·ρ₂` の前提化)・1 規約が pin 経由へ移行した。CEGAR は周回ごとに「何を実行し何を前提にするか」を組み替えるので、**弱化の検出は ① でしか拾えない**。1 走で足りる。
- **②③ の省略条件を 1 行に畳んで ⑤ へ**: 「系統 pin 4 本(`3c93c50c` / `76546bef` / `e0237d10` / `8f718811`)が同一 **かつ TCB のモジュール集合が前回と同一**」なら ②③ を省略してよい。**今回 checker TCB に 1 本増えた**ので、集合の同一性も毎回見ること(pin の sha 一致だけでは新規追加を捕まえられない)。
- **③ を再測定するなら AJ=False も併記**(F-v3-1)。既存の 2096/2105/2110 の数字は AJ=True 系列なので、比較のためには AJ=True も残す。
- **⑤ の恒久項目**(今回の実測を踏まえた更新版):
  1. 親 artifact id / run / 全 file pin が producer literal と checker 側 pin で一致
  2. `direct_pairing.rows == rank_after` ∧ `row_pairings_sha256 == sha(0x00 × rank_after)`(**旧名 `old_state_rows_checked + new_pivot_rows_checked` は親受領証の再検査として別項**)
  3. `old_target_reductions` が前周回 +1、`rank_after` が前周回 +1
  4. head 連鎖 `sha(parent_head ‖ canonical(instruction body)) == state_head` を外部再計算
  5. 選択 seed が親 artifact の生バイトで走査順最初であること(コードを介さない直読)
  6. `raw_row_packed_sha256[2] == e67d0a0b… ∧ raw_row_support[2] == 568`(2110 R1-2・`actual_pin` を 2 分割するまで毎回)
  7. `raw_seed.selected_direct_receipt` が親の `direct_receipt[seed]` と一致
- **v15 seed 核(0.95〜1.00 クローン)が変わらない限り、raw seed 行と projector は二系統一致では永久に retire できない** — 格付け文面に毎回残す(2105 §7 から不変)。

---

## 付録: 参照ファイル(絶対パス)

- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_actual_root_seed_materializer_v3.py`(sha256 `36cc620bdc1b772a…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_actual_root_seed_materializer_v3.py`(sha256 `eca60918eb943edd…`)
- `C:\Users\81905\Desktop\shadow-atelier\.github\workflows\d972-r07-actual-root-seed-materializer-v3.yml`
- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_actual_seed30_materializer_v1.py`(比較元 `3ce9293e…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_actual_seed30_materializer_v1.py`(比較元 `f4f8ba2d…` = v3 の `adapted_checker_lineage`)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_rank1355_root_seed_scalars_v1.py`(checker TCB 新規 `f3c7ca25…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_actual_grade2_root_scalar_batch_v2.py`(`:389-392` = 2110 R1-2 の pin ブロック)
- `C:\Users\81905\Desktop\shadow-atelier\docs\notes\seed30_mat_v1_cv9_reading_v1.md`(裁定 2105・19 規約表)
- `C:\Users\81905\Desktop\shadow-atelier\docs\notes\r1355_rss_v1_cv9_reading_v1.md`(裁定 2110・改訂規律)
- `C:\Users\81905\Desktop\shadow-atelier\sol\sol_reply_943_audit_r07_selected_seed_materializer.md`(静的 PASS)
- 当哨の作業物: `C:\Users\81905\AppData\Local\Temp\claude\C--Users-81905-Desktop-shadow-atelier\d2b80bbe-2be7-426c-9dbe-a39ba301883a\scratchpad\cv9\`(`sim_v3.py` / `cal.py` = 類似度較正・`cand\` `scal\` = download した親子 artifact)

---

本文(この区切りより上)の sha256 先頭 16 桁: 757d9416b3432486
