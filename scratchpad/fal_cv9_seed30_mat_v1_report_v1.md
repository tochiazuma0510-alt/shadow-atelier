# CV-9 仕様同一性判読 — R07 **actual seed30 materializer v1**(副検問・事後)

判読者: falsifier(反証前哨・非当事者)
対象: GHA run `33946247365`(success)・terminal `Separator`・rank 1354 → 1355
先例: `docs/notes/separator_run2_cv9_reading_v1.md`(裁定 2060)/ `docs/notes/rsb_v2_cv9_reading_v1.md`(裁定 2096)
判読範囲: 「producer と checker が同一対象を独立に計算しているか」の一点のみ(裁定 316/318 スコープ制限)。数学的正しさの監査・実装レビュー・追加テストの発案はしない。
日付: 2026-09-05

---

## 0. 裁定

**同一対象(SAME OBJECT)。限定 4 条。**

producer `search/d972_r07_actual_seed30_materializer_v1.py`(sha256 `3ce9293e…`・1563 行)と
checker `search/check_d972_r07_actual_seed30_materializer_v1.py`(sha256 `f4f8ba2d…`・1022 行)は、

> 固定 6 親(P1 `9931437113` / Task554 5 body / Task712 `9915928157` / Separator `9944214057` / scalar `9962060495`+`9962060193` / ρ₂ `9925190479`)に対し、**seed 30・character 0・空 actor 語**の違反を v541 式で物理化し、**rank 1354 の受理済み Separator 状態へ挿入順で 1 pivot を追加**し、**受理済み ρ₂ 剰余をその 1 本だけで消去**し、**新 λ を逆代入で構成する**

という同一対象を計算している。**別対象・判定不能の余地は見つからなかった。**

今回の新規コード(この 1 周回の差分)は**両側で完全に打ち直されている**(トークン類似度 0.12〜0.58、§2.2)。従来から持ち越しの逐語クローンは **v15 seed 核のみ**(0.947〜1.000)で、2096 の測定から**不変**。

限定 4 条は §3。とくに **λ の全 1355 行への直交性は最終スイープされていない**(§4 F1・当哨が数値反証を撃った)。

---

## 1. 同一対象と判定した根拠(すべて確認済み・file:line)

以下 P: = producer、C: = checker。

| # | 規約 | P | C | 一致 |
|---|---|---|---|---|
| 1 | 6 親の run/artifact/bytes/digest を計算前に live 照合 | `.github/workflows/d972-r07-actual-seed30-materializer-v1.yml:104-186`(`gh api`+`jq -e`・Task554 は `conclusion=="failure"` まで固定) | 同一 workflow・同一引数 | **同一 staging・同一 root を両者に渡す**(`:311-338`) |
| 2 | **違反の同一性** = seal `cba44225…`・`origin_id 30`・`origin_kind "seed"`・`seed 30`・`scalar 1`・`character 0`・`actors []` | `:456-468` | `:214-218,243-249` | 同一。`raw_dual_sha256 c19d8972…` も両側 |
| 3 | **「最初の違反」の継承** | `:472` は `seed_scalars[2]==0 and seed_scalars[30]==1` の 2 点のみ | `:255` は `not any(scalars[:30]) and scalars[30]==1`(**seed 0..29 全零を要求**) | 結論同一・**C が真に強い**(§4 F2) |
| 4 | SeedRed(30) の raw 事象列(5 body・old 4 + new 4×4 = 20 expression・event_id 昇順) | `collect_seedred30 :499-590` | `load_task554 :259-280` + `combined_seed30 :282-321` | 同一。origin_id = `ORIGIN_RANGES[s][0]+30`・global_index = `offset+local` |
| 5 | 事象の rolling seal(`sha(prev_hex ‖ canonical(event))`・零頭から・rolling 欄を含めない) | `:583-586` | `:310-313` | 同一。**両側とも係数畳込みの前に封をする**(非可換祖先の保存) |
| 6 | mod-3 係数畳込み → 非零のみ・node 昇順 | `:587-591`(numpy `flatnonzero`) | `:315-318`(dict + `sorted`) | 同一結果。**実装は別物**。support = **902** を両側が要求 |
| 7 | 選択行の **owner/kind 判定** | segment 記述子(`:530-570`) | `OLD_OFFSETS`/`NEW_OFFSETS` の算術(`:391,404`) | **当哨が 8059 node 全部で両写像を照合 → 不一致 0**(§5) |
| 8 | **物理化写像**: d2 から (3−c)·row を加算 ≡ c·row を減算 | `:846 add_scaled(d2, p1_dense, 3-coefficient)` | `:396 subtract(defect[2], …, coefficient)` | **式は同値・書き方は別物**。old は `d0[owner]‖aux(8)` 幅 6056 と `d1` 全 72576、new は `d1[owner]` 幅 18144 — 両側同一 |
| 9 | 下位 96776 座標の完全消滅 | `:874-876` | `:426-429 require_lower_zero` | 同一。`4·6048+4·18144+8 = 96776` を当哨が検算(§5) |
| 10 | **v541 直接側契約**: full filtered projector は完全欠損にのみ当て、その top = 平凡な character-0 slice | `:879-886` | `:418-421` | 同一。`projected[2][0] == defect[2][0]` かつ他 3 character 零 |
| 11 | `G = B_fwd_a0(d)` と 2 対 pairing | `apply_sparse :1338`(Python ループ) | `np.add.at :526-530`(ベクトル化) | **別実装・同一対象**。両側 `q·d = 1`・`λ_old·G = 1`・`B^T λ_old = q`(保存 q とバイト一致) |
| 12 | **挿入規則**: 挿入順 1 掃引・lead 一意・単調要求なし・free 座標で打ち切らない | `physical_reduce :1106-1134` | `reduce_dense :535-555` | 同一。両側とも各 old 行の自 lead が 1 を要求、掃引後に**全 1354 lead で零**を要求 |
| 13 | 正規化: `normalized = remainder · scale`(F₃ では自己逆元) | `normalize_pivot :1137-1149` | `normalize :557-565` | 同一。raw/normalized の区別を両側が保持 |
| 14 | **新 target 段**: 新 pivot 1 本のみで消去(884 は再計算せず参照) | `update_target :1151-1166` | `next_target :567-576` | 同一。`new_target_eliminations = 1` |
| 15 | **λ の定義**: 新 target 剰余の**最初の非零座標**を free とし、pivot_id 1354→0 の逆順代入で `λ[lead_i] = −⟨row_i, λ⟩` | `separator_after_append :1168-1209` | `next_separator :668-698` | 同一。走査域・順序・新 pivot の `offer=8059` まで一致 |
| 16 | **「依然 Separator」の判定規則** | `kind = "Separator" if first_nonzero(target_raw)` `:1400` | `kind = "Separator" if np.any(updated)` `:855` | 同一 |
| 17 | λ の受理条件(3 本) | `:1201-1204`: `λ·ρ₂=1` ∧ `λ·normalized=0` ∧ `λ·new_target=1` | `:696` の 2 本 + `:874` の `λ·updated=1` | **3 本とも同一**(引数束縛を追跡して確認: P の第 1 引数 = ρ₂ 原本、第 2 引数 = 新 target 剰余) |
| 18 | 封の正規形 | `sealed(schema, body) :162` | `seal(body) :103` | `sort_keys=True` により**同一 canonical バイト**。実際 result.json がバイト一致 |
| 19 | 格の自己抑制 | `CLAIMS :131-138`・`cross_checked: False` | `CLAIMS :62-68`・`cross_checked: False` | 同一。workflow `:394` が `.cross_checked == false` を**要求**(自己昇格の封鎖) |

**相互束縛(独立性の実体・今回いちばん広い)**: checker `compare_candidate :755-779` は、**自前で再計算したバイト**に対して producer 出力の**全ファイルのバイト一致**を要求する — `source-d.bin` / `physical-raw.bin` / `physical-remainder.bin` / `physical-normalized.bin` / `target-remainder.bin` / `lambda.bin` / `instruction.json` / `result.json` / `manifest.json`、およびファイル集合の完全一致。**candidate 側の自己封は権威にしない**と明記(`:757`)。

`result.json` のバイト一致は、`separator.transcript`(**1355 本の λ 値**)・`pivot.reductions`(**889 本**)・`ancestry`(**raw_events 2606・selected_lifts 902・p1_roots 1340**)まで含む。**echo ではない**: checker は candidate ディレクトリに `:884` で初めて触れる(それ以前の全計算は親のみから・grep で確認)。

---

## 2. 独立性の実体(測定値)

### 2.1 系統の分離(ファイル単位・確認済み)

| | producer 側 | checker 側 |
|---|---|---|
| 上流 batch | `d972_r07_actual_grade2_root_scalar_batch_v2.py`(`:53` pin `3c93c50c…`) | `check_…_root_scalar_batch_v2.py`(`:36` pin `e0237d10…`)= `BASE` |
| 上流 separator | `d972_r07_grade2_physical_state_separator_v2.py`(`:56` pin `b068c9f3…`) | `check_…_physical_state_separator_v2.py`(`:38` pin `bb5d0c0a…`)= `TARGET` |
| v15 算術核 | `d972_r07_targeted_grade2_owner_generated_join_v15.py`(`:55` pin `76546bef…`) | `check_…_join_v15.py`(`:37` pin `8f718811…`)= `BASE.ARITH` |

**交差辺は無い**(確認済み): checker 系統 3 本のいずれも producer 系統を import しない(`import`/`spec_from_file_location`/`exec_module` を grep)。producer は `check_*` を一切参照しない。checker 冒頭 `:41-45` は **import 前に**3 本を sha 照合し、`:6-7` に「新 producer は import も実行もしない」と明記。ρ₂ 読み出しも `separator_v2._read_target_parent`(P `:1309`)vs `TARGET._target`(C `:794`)で**別モジュール**。

### 2.2 新規コードの類似度(当哨が測定・トークン列 difflib 比・文字列は `<STR>` 正規化)

| 単位 | P | C | tok-sim |
|---|---|---|---:|
| 挿入順掃引 | `physical_reduce` | `reduce_dense` | **0.2255** |
| 正規化 | `normalize_pivot` | `normalize` | 0.5806 |
| target 1 段 | `update_target` | `next_target` | 0.5090 |
| **λ 逆代入** | `separator_after_append` | `next_separator` | **0.5055** |
| SeedRed 収集 | `collect_seedred30` | `combined_seed30` | **0.1770** |
| 欠損再構成 | `replay_seed30` | `reconstruct_defect` | **0.1210** |
| 状態読込 | `validate_state_parent` | `load_state` | 0.2121 |
| selftest | `selftest` | `selftest` | 0.1254 |
| pack / unpack / dot | — | — | 0.494 / 0.332 / 0.539 |

→ **この周回の差分は逐語コピーではない。** 参考: 承知のクローン対は 1.000。

### 2.3 なお逐語クローンの部分(2096 から**不変**・当哨が再測定)

| 単位 | tok-sim | 今回の役割 |
|---|---:|---|
| `_seed_evaluate_seed` ↔ `_checker_seed_evaluate_seed` | **0.9804** | **raw seed 30 行そのものを産む**(P `:816` / C `:368`) |
| `_seed_full_project` ↔ `_checker_seed_full_project` | **0.9712** | v541 完全欠損への filtered projector(P `:879` / C `:418`) |
| `_seed_act` ↔ `_checker_seed_act` | 0.9467 | 今回は未使用(actor 経路なし) |
| `read_task712_envelope` | **1.0000** | Task712 表の読み出し(P `:800` / C `:515`) |
| `pack_trits` ほか | **1.0000** | 低位核 |

**帰結**: raw seed 行と projector は**二系統一致では retire できない**(0.97〜0.98 クローン対が両側の「独立実装」の実体)。これは 2096 で既に格付けに織り込み済みの限定であり、今回**悪化も改善もしていない**。今回の錨は Task712(独立親)との degree-2 一致と、`q·d = 1` / `λ_old·G = 1` の 2 対 pairing のみ。

---

## 3. 主張の射程

### cross-checked と呼べる有限事実

1. **物理化**: seed 30・character 0・空 actor 語の v541 欠損が、**選択 902 行**の P1 lift 減算で**下位 96776 座標すべて零**になり、その top(character-0 slice)が `source-d.bin` である。両側がバイト一致。
2. **祖先**: raw_events **2606** 本(rolling 封つき)・literal_p1_roots **1340** 本(うち mod 3 で非零に残るのが 902 = **438 本は相殺されるが根として保持**)・選択各行の P1 row sha が instruction 受領証と一致。両側がバイト一致。
3. **挿入**: G を rank 1354 の状態に挿入順で掃引 → **889 本の reduction**、剰余が非零 → lead 一意・全 old lead で零 → 正規化して **rank 1355**。両側が独立に再計算しバイト一致。
4. **target**: 受理済み ρ₂ 剰余(884 reduction 後・24192 hex = 12096 byte・sha `e0053fc6…`)に対し、**新 pivot 1 本だけの消去が 1 回**発生し、剰余は依然非零 → `Separator`。両側一致。
5. **λ**: `λ·ρ₂ = 1`・`λ·(新 pivot) = 0`・`λ·(新 target 剰余) = 1`、および構成時に各 1355 行で `⟨row_i, λ⟩ = 0` を成立させた 1355 本の transcript。両側がバイト一致。

### cross-checked ではない(必ず文面に書く)

1. **「ρ₂ ∉ span(S₀ ∪ {新 pivot})」は λ で支えられているが、λ ⊥ 全 1355 行は最終確認されていない**(§4 F1)。成立は **親状態の挿入三角性**という前提に依存する。前提自体は親 run の checker が全 1354 行を再構成して確立している(`check_…_physical_state_separator_v2.py:420-422,467`)ので**連鎖としては支えがある**が、本 run 内では検査されていない。
2. **884 本の旧 target reduction は再計算していない**(両側とも親受領証の参照・宣言 `old_state_derivation_premise: true`)。rank 1354 状態の 8059 offer / 610996 reduction の導出も同じく前提。
3. **origin 31..32279 は今回も何も言っていない**(2096 の限定 1 を継承)。今回新たに checker が seed 0..29 全零を確認したので「seed 範囲での最初」は閉じたが、**actor origin 44..32279 は未走査**。
4. **q(root covector)は親保存値への回帰照合**であり独立発見ではない(2096 限定 2 を継承)。
5. **ρ₂ のバイトは共有 stager**(`stage_d972_r07_targeted_grade2_rho2_v9_flat_v4.py`・workflow `:305`)経由で両側に届く。両側とも独立の pin(P `:1312 RHO2_SHA256` / C は親状態の受領証 join)で錨を打っているので単一障害点ではないが、**staging は 1 実装**。
6. `eleven_slot_replay: false`・`full_A0_witness: false`・`normalized_exponent_pair: "NOT_REPLAYED"`・`grade2_positive_terminal_complete: false` を両側が明記。**GRADE2 MEMBER/NONMEMBER = NOT_DECIDED**。A0/COMMON/COFINAL_LIFT/FAKE/IHARA = NOT_DECLARED。**verified = false**(Lean 未)。
7. **新 Separator は grade-wide NONMEMBER ではない**(Task927 §5・Task928 §2 の指示どおり両側が明記)。

---

## 4. 指摘

### 【要修正】F1. λ の全行直交性が最終スイープされていない — 否定的主張の唯一の支柱が前提に乗っている

両側の逆代入ループは、**その行を処理した瞬間に** `⟨row_i, λ⟩ = 0` を検査する(P `:1188` / C `:688`)。しかしその後の低 pivot_id の代入が座標を書き換えるため、**最終の λ について全行を掃き直す検査が無い**。成立は「row_i は自分より前の全 lead で零(挿入三角性)」という前提に依存する。

当哨が数値反証を撃った(F₃・整数のみ・node):

```
rows(挿入順) = [[1,0,1], [1,1,0]],  leads = [0,1],  free = 座標 2
  (row1 が row0 の lead(座標 0)で非零 = 三角性違反)
→ 両側の in-loop require はすべて成立(例外なし)
→ λ = [2,0,1]
   dot(λ, row0) = 0
   dot(λ, row1) = 2   ← 直交していない
   dot(λ, ρ₂=[1,0,0]) = 2 ≠ 0  → 本番コードは "Separator" と判定する
   しかし ρ₂ = row0 − row1 = [0,2,1] … の span 内にあり、判定は誤り
```

- **緩和**: 親 run の checker は全 1354 行を **自前で再構成し** `physical.bin` とバイト比較している(`check_…_physical_state_separator_v2.py:420-422` が各追加行の「全既存 lead で零」を要求、`:467` がバイト比較)。よって三角性はその run で独立に確立済みであり、現実に前提が破れている可能性は低い。**重大ではない。**
- **しかし**: 本 run の否定的主張(依然 Separator)は、**別 artifact の格付けに全面依存**しており、本 run の cert 単体では閉じない。両 selftest は `all(dot(λ, row) == 0 for row in rows)` を検査している(P `:1484` / C `:964`)が、**その fixture は三角性を満たしている**ので失敗モードを踏まない。
- **修正案(安い)**: 本番経路の最後に `⟨λ, row_i⟩ = 0` を全 1355 行で 1 パス掃く。checker は既に `physical.bin` を stream しており、追加コストは 16.4 MB の 1 読み(40 分 cap に対して無視できる)。これを入れれば **三角性前提が完全に不要**になり、「ρ₂ ∉ span」が本 run の cert 単体で閉じる。**CEGAR は何周も回るので、次周回の前に入れる価値が高い。**

### 【軽微】F2. 「最初の違反」の再確立が producer 側だけ弱い

- C `:255`: `not any(scalars[:30]) and scalars[30] == 1` — 44 バイト保存配列から seed 0..29 全零を要求。**scan 順(44 seeds 先)の下で「seed 30 が最初」を再確立している。**
- P `:472`: `seed_scalars[2] == 0 and seed_scalars[30] == 1` — 2 点のみ。

結論は同一で、強い側が checker なので実害はない。ただし cert の文面に「first violation は再確立された」と書くなら、**根拠は checker 側の 1 行**であることを明記すべき。

### 【軽微】F3. raw 事象の型検査が checker 側だけ

C `:290-292` は各項に `len == 2` ∧ `type is int` ∧ `0 <= local < bound` ∧ `coefficient in (1,2)` を要求。P `:521-535` の `append_expression` には対応する検査がなく、下流の `require(len(final)==902 ∧ all in (1,2))` と numpy 添字例外に頼る。片側だけの網であり、対象の同一性には影響しない。

### 見つからなかったもの(正直な範囲報告)

- **silent cap**: 見つからなかった。P1 は cache/instruction とも 8059 行 1 パス全消費 + trailing 空 + sha 再計算(P `:731-777` / C `:341-359`)。state instructions.jsonl も 8059 行全消費 + rolling 再計算 + trailing 空(P `:1040-1073` / C `:621-648`)。Task554 blob も全バイト消費。workflow の cap(producer/checker 各 40 分・job 90 分)は超過時に job 失敗 → candidate 未 upload(`:398` は checker PASS の後段)、diagnostics は `if: always()`。**fail-closed。**
- **ダミー検査(何にでも当たる試験)**: 見つからなかった。両 selftest は実際に**拒否**を要求する(C `:895-901 reject_test` が 8 種・P `:1487-1493`)。C `:947` は挿入順が非単調(leads (1,0))な fixture で reduce の順序依存を分離し、C `:957` は `scale == 2` で raw/normalized の取り違えを分離、C `:924` は再封した事象列の順序入替を拒否する。
- **事前登録違反**: 見つからなかった。対象(seed 30・character 0・空 actor 語)・親 6 組・rank 1354・支持数 902 はすべて計算前に literal で凍結され、workflow が計算前に live 照合する。
- **別対象・判定不能の余地**: 見つからなかった(§1 の 19 規約すべてで一致)。

---

## 5. 当哨が撃った数値検算(整数のみ・node)

すべて OK:
`ΣOLD_RANKS = 2014` / `ΣNEW_RANKS = 6045` / 計 `8059` / OLD_OFFSETS・NEW_OFFSETS が階段和と一致 / `ORIGIN_RANGES` 総計 `8232` / `4·6048+4·18144+8 = 96776` / `4·36288 = 145152` / `⌈145152/4⌉ = 36288` / `⌈48384/4⌉ = 12096` / `2·12096 = 24192`(hex 長)/ `1354·12096 = 16377984`(physical.bin)/ `1354·2015 = 2728310`(p1-coeff.bin)/ **owner 写像が 8059 node 全部で両側一致(不一致 0)**。

λ 逆代入の反証例は §4 F1。

---

## 6. CV-9 裁定案・工房格付け案

> **CV-9 = 同一対象(限定 4 条)。工房格 = checker PASS(同一著者系統・本周回の差分は両側打ち直し(tok 0.12〜0.58)・候補全 9 ファイルがバイト一致で相互束縛・ただし v15 seed 核と projector は 0.97〜0.98 クローン持ち越し)・cross-checked は限定つき** — (i) 射程 = seed 30/character 0/空 actor 語の 1 周回のみ(actor origin 44..32279 は未走査) (ii) rank 1354 状態の導出・884 旧 target reduction・**親行の挿入三角性**は再計算せず前提(親 run の checker が確立済み) (iii) **λ の全 1355 行直交性は最終スイープされていない**(§4 F1・数値反証あり・次周回前に 1 パス追加を推奨) (iv) q は親保存値への回帰照合。主張 = 「rank 1354 の Separator 状態に seed 30 由来の pivot 1 本を追加して rank 1355 とし、ρ₂ の剰余が依然非零であった」という有限事実。**GRADE2 NOT_DECIDED・NONMEMBER ではない・verified = false。**

---

## 7. 以後の CEGAR 周回について(問われた点 4)

**「入力 pin と終端受領証の確認だけで足りる」とは言えない。** 理由:

- checker には周回固有の literal が**38 箇所**散在する(`1354` / `1355` / `8059` / `8060` / `884` / `902` / `2014` / `OLD_HEAD` / `OLD_REMAINDER_SHA` / `STATE_FILES` 9 本の byte+sha)。producer も同様(`STATE_RANK` / `STATE_GENERATION` / `SEED = 30` / `SEED30_SUPPORT = 902` / `OLD_TARGET_REMAINDER_SHA256` ほか)。次周回は rank 1355→1356・generation 8060→8061・新 seed・新親 artifact になるため、**両ファイルとも実質的な新版(v2)になる**。「同じコードが何周も走る」構造ではない。
- ただし**規約は不変**である見込みが高い。よって次周回以降の判読は**増分でよい**:
  1. §1 の 19 規約表を機械 diff(定数の差し替えのみか、規則が変わっていないか)
  2. §2.1 の系統分離に交差辺が生えていないか(import grep 1 本)
  3. §2.2 の類似度を新規差分に対して再測定(コピペ回帰の検出)
  4. §4 F1 が塞がったか
  5. 入力 pin と終端受領証の確認

  1〜4 が全部無変化なら、以後は 5 のみで足りる。**その到達点を作るためにも F1 を先に塞ぐのが得**。
- なお **v15 seed 核(0.947〜1.000 クローン)が変わらない限り、raw seed 行と projector は永久に二系統一致では retire できない**。周回を重ねても射程は広がらないので、格付け文面には毎回この一句を残すこと。

---

## 付録: 参照ファイル(絶対パス)

- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_actual_seed30_materializer_v1.py`
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_actual_seed30_materializer_v1.py`
- `C:\Users\81905\Desktop\shadow-atelier\.github\workflows\d972-r07-actual-seed30-materializer-v1.yml`
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_grade2_physical_state_separator_v2.py`(親の三角性確立: `:420-422,467`)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_task_927_r07_actual_seed30_materialization.md`
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_task_928_r07_actual_seed30_checker_workflow.md`
- `C:\Users\81905\Desktop\shadow-atelier\sol\sol_reply_932_audit_r07_seed30_release.md`(F2 `:48-50` が三角性前提を明示・**開示は実在する**)

---

本文(この区切りより上)の sha256 先頭 16 桁: `1106e2318237fcbb`
