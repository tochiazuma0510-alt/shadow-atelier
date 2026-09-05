# CV-9 増分判読 — R07 rank1355 root seed scalars v1(副検問・事後・短縮版)

判読者: falsifier(反証前哨・非当事者)
対象: GHA run `33954712636`(success)・terminal `ROOT_SEED_VIOLATION`
先例規律: `docs/notes/seed30_mat_v1_cv9_reading_v1.md` §7(裁定 2105)の 5 項増分手順
判読範囲: 「producer と checker が同一対象を計算しているか」の一点のみ(裁定 316/318)
日付: 2026-09-05

---

## 0. 裁定

**同一対象(SAME OBJECT)。限定 3 条**(前回の限定 4 条から **(iii) が消滅** — F1 が塞がった)。

producer `search/d972_r07_rank1355_root_seed_scalars_v1.py`(`973ccd1d…`・560 行)と
checker `search/check_d972_r07_rank1355_root_seed_scalars_v1.py`(`f3c7ca25…`・650 行)は、

> 受理済み rank1355 状態(generation 8060・head `36feb776…`・λ `f83bbaa5…`)の λ から
> 4 character 分の root covector を新規に導出し、P1 8059 行 1 パスで縮約し、
> Task554 の seed 関係式だけを畳んで **4×44 = 176 個の seed scalar** を作り、
> character-major/seed 0..43 の走査順で最初の非零を返す

という同一対象を計算している。**別対象・判定不能の余地は見つからなかった。**

---

## ① 19 規約表の機械 diff

19 行は 3 群に割れる。**規則が変わった行は無い**(定数の差し替えと、実行されない機構の退役のみ)。

**(A) 不変で存続 — 5 行**

| 旧# | 規約 | P | C | 一致 |
|---|---|---|---|---|
| 1 | 親を計算前に live 照合 | workflow `:98-157`(gh api + jq -e・**9 artifact**・Task554 は `conclusion=="failure"` まで固定) | 同一 workflow・同一引数 | 同一 staging を両者へ(`:311-338`) |
| 5 | 事象の rolling 封(`sha(prev‖canonical(event))`・零頭・rolling 欄を含めない) | `:340-341` | `:385-386` | 同一。event 本体キー 11 個も同一 |
| 6 | mod-3 係数畳込み | `:342-343` **各項ごとに `+(3−c)·v`** | `:359-362` **一括で `−Σc·v`** | **式は同値・書き方は別物。当哨が 20,000 個のランダム式(重複項・係数 {1,2} 込み)で全数照合 → 不一致 0** |
| 18 | 封の正規形(`sort_keys`) | `sealed :88` | `seal :95` | 同一 canonical バイト(20 ファイルのバイト一致が実証) |
| 19 | 格の自己抑制 | `CLAIMS :63-66`・`cross_checked False` | `CLAIMS :76-79` | workflow `:331` が `.cross_checked == false` を要求 |

**(B) 退役 — 13 行**(旧 #2,4,7〜17)。materializer 固有の機構(物理化写像・下位 96776 消滅・挿入掃引・正規化・target 段・λ 逆代入・Separator 判定・λ 受理 3 条)は本 run では**一つも実行されない**(`materialization_performed: false`・`actor_origins_executed: 0`・`orbit_rows_executed: 0`)。対応する対象は artifact `9963533999` からバイト pin で前提として読まれる。旧 #17(λ 受理)だけは**より強い形で再確立**(→ ④)。

**(C) 新規 — 8 行**(両側で literal / 規則が完全一致)

| 新# | 規約 | P | C |
|---|---|---|---|
| N1 | 走査宇宙 = 4 character × 44 seed = 176・character-major/seed0-43・actor 0・orbit 0 | `SCOPE :59-61` | `SCOPE :73-75`(literal 同一) |
| N2 | λ は**構成せず** delta artifact から読む | `:220-227` | `:204-208` |
| N3 | 新 root covector `q_a = sparse_adjoint(B_fwd_a, 36288, 48384, λ)` を **4 character 全部**新規導出(事前 pin なし) | `new_roots :266-277` | `fresh_roots :285-298` |
| N4 | P1 縮約 = 8059 行 1 バッファパス・character byte offset `a·9072` | `:292-323` | `:309-339` |
| N5 | seed-only fold = 5 body × 4 source × 44 seed・offset OLD/NEW | `seed_only_fold :326-371` | `fold_seeds :364-392` |
| N6 | 終端 = 176 順で最初の非零 → `ROOT_SEED_VIOLATION`、全零 → `ROOT_SEEDS_ZERO` | `:465-466` | `terminal_record :432-437` |
| N7 | 両側の raw seed 評価器を `actual_pin=False` で呼ぶ | `:438` | `:342` |
| N8 | **最終 λ の全 1355 行直交スイープ** | `:226`+`:249` | `:244`+`:249-250` |

**規約差(両向き・独立著作の証拠であって欠陥ではない)**: producer のみが `manifest["mode"]`・`rank_before==1354`・`checker["new_pivots"]==1`・`old_state_derivation_premise is True` を検査(`:194-202`)。checker のみが `instruction["offer"]==8059`(`:196`)と、**delta の source-receipt に対する materializer producer/checker 両ソースの sha 突合**(`:177-184`)を検査し、さらに **4 character 全部の P1 縮約を実行**(producer は `active` のみ計算)。片側だけの網はいずれも「強い側」であり、対象の同一性には影響しない。

**silent cap・事前登録違反**: 見つからなかった。P1 cache は 8059 行全消費 + trailing 空 + sha 再計算(P `:318-319` / C `:337-338`)、physical.bin は 1354 行全消費 + trailing 空 + sha 一致(P `:239-253` / C `:236-249`)、Task554 5 body は 1 本ずつ全消費して解放。cap は producer/checker 各 40 分・job 90 分で、超過時は step 失敗 → candidate は upload されない(diagnostics のみ `if: always()`)。**fail-closed。**

---

## ② import 交差辺 grep

**交差辺なし(確認済み)。**

- producer の動的 import は 1 本のみ: `:139-143 spec_from_file_location("task937_accepted_root_v2", d972_r07_actual_grade2_root_scalar_batch_v2.py)`。直前 `:135` が **producer 系統 2 本を sha 照合**してから読む。`check_*` は一切 import/exec しない(ファイル名の出現は `LINEAGES` 宣言辞書のみ)。
- checker の import は 1 本のみ: `:31 import check_d972_r07_actual_grade2_root_scalar_batch_v2 as BASE`。直前 `:26-30` が **import 前に**checker 系統 2 本を sha 照合し、symlink を拒否。producer 系統ファイル名の出現は `LINEAGES` 宣言(`:68-69`)と、delta の source-receipt に対する **sha 突合**(`:180-184`・import ではない)のみ。
- 系統 pin は 4 本とも 2096/2105 の測定時と**バイト同一**: producer `3c93c50c…`/`76546bef…`、checker `e0237d10…`/`8f718811…`。→ **v15 seed 核と projector のクローン測定値(0.947〜1.000)は再測定不要で持ち越し確定**(pin による証明)。

---

## ③ 新差分のトークン類似度(当哨が測定・`<STR>` 正規化 difflib)

| producer | checker | tok-sim |
|---|---|---:|
| `run_actual` | `check_actual` | **0.1115** |
| `load_separator` | `load_delta` | **0.2613** |
| `selftest` | `selftest` | 0.2209 |
| `seed_only_fold` | `fold_seeds`(+`fold_expression`) | **0.2845** |
| `load_separator` | `state_dots` | 0.3425 |
| `p1_root_values` | `cache_contractions` | 0.3888 |
| `new_roots` | `fresh_roots` | 0.3928 |
| `pinned_parent_descriptors` | `task554_parent` | 0.4907 |
| `main` | `main` | 0.6844 |
| `root_record` | `root_receipt` | 0.7331 |
| `scalar_stream` | `scalar_records` | 0.7749 |
| `without_roots` | `path_independent` | **0.9516** |
| `canonical`/`sha`/`receipt`/`progress` | 同名 | 1.0000(いずれも 1〜2 行の定型) |

**判定**: 本周回の実質差分は **0.11〜0.39** で打ち直し。0.73〜0.78 の 2 本(`root_record`/`scalar_stream`)は**スキーマ literal が同一でなければならない**(バイト一致要求のため)ことによる不可避の重なりで、制御構造は別(producer は二重ループ、checker は `divmod(index,44)`)。**v15 seed 核クローンの持ち越しは②の pin より確定・悪化も改善もなし。**

---

## ④ F1(最終 λ の全 1355 行直交スイープ)— **塞がった**

**両側の本番経路に実装され、実際に走った。**

| | producer | checker |
|---|---|---|
| 旧 1354 行 | `:249 require(base.ARITH.dot_mod3(lam, row) == 0, "new_lambda_old_row")`(physical.bin を 12096 B ずつ 1354 回 stream・同時に sha 再計算 → `1246ae0c…` 一致) | `:244 require(dot(delta["lambda"], unpack(row, WIDTH)) == 0, ...)`(同上) |
| 新 pivot 1 行 | `:226 dot_mod3(lam, new_row) == 0` | `:249 dot(lambda, normalized) == 0` |
| 剰余 | `:227 dot_mod3(lam, remainder) == 1` | `:250 dot(lambda, target) == 1` |
| 受領証 | `old_state_rows_checked 1354` / `new_pivot_rows_checked 1` / `lambda_pivots 0` / `lambda_saved_remainder 1`(**封済み launch.json 内**) | 同一値を checker-result に出力 |

**実行証跡**: producer.log `{"parent":"old-physical-new-lambda","rows":1354,"total":1354}` / checker.log `{"phase":"separator_rows","checked":1355,"total":1355}`。

**部分的独立性**: 内積は producer が v15 の `dot_mod3`、checker が自前 numpy `dot :143-145`(`np.sum(uint64*uint64) % 3`)で **別実装**。ただし行の base-3 復号は両側とも `ARITH.unpack_trits`(1.0000 クローン対)。当哨が第三実装(素の base-3 展開)で `q-a0-root.bin` を復号 → support **2691** が cert と一致し、梱包規約は独立に確認済み。

**F1 が買ったもの / 買っていないもの**:
- **買った**: 「λ ⊥ 全 1355 行」は**挿入三角性の前提に一切依存せず**本 run 内で成立。2105 の限定 (iii) と、当哨が §4 F1 で撃った数値反証(逆代入の in-loop 検査が三角性違反を素通りする例)は**本 run では発火しない**。
- **買っていない**: 「target-remainder ≡ ρ₂ mod span(rows)」(= 884+1 本の reduction 簿記)は依然親の前提。本 run は **ρ₂ 本体を一度も読まない**。λ·ρ₂ = 1 は親 run が直接検査済み(2105 §1 #17)なので連鎖としては支えがあるが、本 run の cert 単体では ρ₂ を含まない。

**負のカナリア**: 両 selftest に「λ⊥row スイープが落ちる」合成試験は**無い**(→ 指摘 R1-3)。ただしスイープ自体は 1354 本の実データ内積を 0 に拘束するので「何にでも当たる試験」ではない。

---

## ⑤ 入力 pin と終端受領証の突合

当哨が candidate `9966008518`(zip sha `148b028e…`)と diagnostics `9966008810` を Release から取得し、**第三実装で再計算**した。

**入力 pin(封済み launch.json 内・全て一致)**
- delta = seed30 materializer candidate `9963533999`(run 33946247365 / head `7f6dfadd…` / 915410 B / `sha256:f9627416…`)+ 5 ファイル受領証。diagnostics の `artifact-9963533999.json` が live 値と一致・`expired: false`。
- P1 `9931437113`(cache `b88edb9b…` 292,444,992 B / instructions `8b549337…`)・Task554 5 artifact(`9865061266` 他)・Task712 `9915928157`(manifest `48c5d1f4…` ×4)・Separator `9944214057`(physical `1246ae0c…` 16,377,984 B)。
- source-receipt: 6 ファイル(新 pair 2 本 + batch v2 2 本 + v15 2 本)が workflow 凍結値と一致。

**終端受領証(第三実装で再計算 → 完全一致)**
- `result` / `manifest` / `first_violation` / 4 つの `character` の封を再計算 → 全て一致。`canonical(result)` == result.json バイト。
- **176 レコードの rolling chain を bin から第三実装で再構築 → `scalar_final_head 59fcadc1…` 一致・scalars.jsonl のバイトまで一致。**
- **first_violation = index 34 / character 0 / seed 34 / origin_kind "seed" / scalar 1 / rolling `52ae192c…`** を第三実装が独立に再現。`separator_generation 8060` / `separator_head 36feb776…` / `lambda_sha256 f83bbaa5…` / `materialization_performed false`。
- `q-a0-root.bin` の base-3 第三実装復号 → support 2691 = cert 値。`p1-values-a0.bin` の sha = `value_vector_sha256 6274f01a…`。
- checker-result: `files_compared 20`(= 16 bin + launch + scalars.jsonl + result + manifest)・`cache_passes 1`・`old_state_rows_checked 1354`・`cross_checked false`・`verified false`。

**整数恒等式(当哨が撃った・すべて OK)**: `4·44=176` / `OLD_OFFSETS` `NEW_OFFSETS` が階段和(2014 + 6045 = 8059)/ `1354·12096 = 16,377,984` / `⌈48384/4⌉ = 12096` / `⌈36288/4⌉ = 9072` / `4·9072 = 36288` / `36288·8059 = 292,444,992` / `8059+1 = 8060` / `1354+1 = 1355`。

**λ が本当に新しいことの確認**: root covector の support が **2742(rank1354・裁定 2096)→ 2691(本 run)** に変化。古い q の使い回しではない。

---

## 指摘

**【要修正 R1-1】格付け文面の数量引用(2096 F2-3 の再来・今回いちばん重い)。**
scope は `characters [0,1,2,3]` / `scalar_count 176` と宣言するが、**実測で q_a = 0(support 0)が character 1,2,3**。したがって 176 個中 **132 個は q=0 による構造的な零**であり、P1 縮約も character 1,2,3 は全零(`active_characters: [0]`)。実質的な新情報は **character 0 の 44 個**と、**「4 character 中 3 つで B\*λ = 0」という事実そのもの**の 2 点だけ。「176 scalar を走査した」「4 character 全走査」を成果幅として引用しない。

**【軽微 R1-2】`actual_pin=False` が λ 非依存の pin を 2 つ道連れにしている。**
`raw_seed_direct` / `checker_raw_seed_direct` の `actual_pin` ブロックは `character==0 ∧ row_sha[2]==SEED2_RAW_PACKED_SHA256 ∧ row_support[2]==568 ∧ values[2]==0` の 4 連言(producer base `:389-392` / checker base `:313-316`)。**λ に依存するのは `values[2]==0` だけ**で、raw seed 行の sha と support は degree-2 character slice のみに依存し λ が変わっても不変。`actual_pin=False` はそれらも同時に落としており、raw seed 行の唯一の錨が 0.98 クローン対 `_seed_evaluate_seed`/`_checker_seed_evaluate_seed` に閉じた。
→ **当哨が cert から外部照合して今回は閉じた**: `characters[0].direct_receipt.raw_row_packed_sha256[2] = e67d0a0b…` = 凍結定数、`raw_row_support[2] = 568`。**値としては無傷**。ただし機構が無いので次周回は自動では守られない。安い修正 = フラグを 2 つに割る(行 pin は常時 ON・scalar pin のみ λ 更新時 OFF)。

**【軽微 R1-3】F1 スイープに負のカナリアが無い。**
両 selftest(producer 5 本 / checker 5 本)は root 動的性・stale head 拒否・176 順序・全零終端・重複項 offset を検査するが、**「λ⊥row が破れる合成 fixture を拒否する」試験が両側とも無い**。スイープは実データ 1354 本の内積を拘束するので空虚ではないが、合成 3 行 fixture 1 本で足りる。

**【軽微 R1-4】`without_roots` ↔ `path_independent` が tok-sim 0.9516 の準クローン。** 6 行の再帰 dict フィルタ(`root` キー除去)。実害なし・記録のみ。

**【軽微 R1-5】11 seed で関係式が空。** seed 4〜12・32・43 は `raw_event_count == 0`(総 event 12,427・最大 3,338)。当該 seed は direct 値も 0 なので結論に影響しないが、fold 分岐が実データで一度も走らない seed が 44 中 11 ある。空虚性としては軽微(残り 33 seed が濃く走る)。

### 見つからなかったもの(正直な範囲報告・保証ではない)
- **別対象・判定不能の余地**: 見つからなかった(①の (A)+(C) 13 規約すべてで一致)。
- **silent cap / 事前登録違反**: 見つからなかった。
- **ダミー検査**: 見つからなかった。checker selftest `:598` は封が整合した stale head を**拒否**することを要求し、`:606-609` は重複項 + global offset を分離する(手計算 fixture)。producer selftest は零 root を含む動的 active 判定と `ROOT_SEEDS_ZERO` 分岐を分離する。
- **「見つからなかった」を非存在と読む型**: 該当なし。主張は seed 34 で scalar 1 という肯定的証拠。

---

## 格付け案(一行)

> **CV-9 = 同一対象(限定 3 条)。工房格 = checker PASS(同一著者系統・本周回の差分は両側打ち直し(tok 0.11〜0.39・スキーマ literal 由来の 0.73〜0.78 が 2 本)・系統は完全分離(交差辺なし・4 系統 pin は 2096/2105 と同一 sha)・候補全 20 ファイルをバイト一致で相互束縛・ただし v15 seed 核と projector は 0.95〜1.00 クローン持ち越し)・cross-checked は限定つき** — (i) 射程 = rank1355 の λ に対する **character 0 の seed scalar 44 個**(残り 3 character は **q = B\*λ = 0** ゆえ 132 個が構造的零・actor origin 44..32279 と orbit は未走査・`materialization_performed false`) (ii) rank1354 状態の導出・884 旧 target reduction・**target-remainder ≡ ρ₂ mod span** は再計算せず前提(本 run は ρ₂ を読まない) (iii) **λ の全 1355 行直交性は本 run の両側本番経路でスイープ済(裁定 2105 F1 は閉鎖・三角性前提は不要になった)** (iv) raw seed 行の凍結 pin は `actual_pin=False` で外れており、当哨が cert から外部照合して今回のみ閉じた(値は無傷 `e67d0a0b…`/support 568)。**主張 = 「rank1355(generation 8060・head `36feb776…`・λ `f83bbaa5…`)に対し、v541 修正式で走査順最初の非零 root seed scalar が character 0・seed 34 で 1(seed 0..33 は 0・非零は 34→1, 35→2, 36→2 の 3 個・seed 30 は 1 から 0 に落ちた)」という有限事実。GRADE2 MEMBER/NONMEMBER = NOT_DECIDED・NONMEMBER ではない・verified = false(Lean 未)。**

---

## 次周回以降について

**⑤ のみでは足りない。ただし②③④は次周回から省いてよい。**

- **②(import 交差辺)と③(類似度)は pin で足りる**: 系統 4 本の sha が `3c93c50c…`/`76546bef…`/`e0237d10…`/`8f718811…` のままなら、クローン測定値は再測定不要。**新 pair 自身の producer/checker が「前周回のファイルの定数差し替え版」であることを diff 1 本で確認**すれば、③の再測定も不要(規則が変われば diff に出る)。
- **④(F1)は閉じたので恒久的に落として良い** — ただし**受領証 `old_state_rows_checked` + `new_pivot_rows_checked` の和が rank と一致するか**を⑤の一項目に格上げすること(本 run なら 1354+1 = 1355)。これが崩れたら再判読。
- **①だけは毎回必要**: 本周回で 13 規約が退役し 8 規約が新設された。CEGAR は周回ごとに「何を実行し何を前提にするか」を変えるので、規約表の (A)/(B)/(C) 割りは毎回やり直す必要がある。ただし**表の機械 diff で足りる**(1 走)。
- **R1-2 が残る限り、⑤に「`raw_row_packed_sha256[2] == e67d0a0b… ∧ raw_row_support[2] == 568`」の外部照合を毎回入れること**(当哨が今回やった 1 行)。フラグを割れば不要になる。
- **v15 seed 核(0.95〜1.00 クローン)が変わらない限り、raw seed 行と projector は二系統一致では永久に retire できない。**格付け文面にはこの一句を毎回残すこと(2105 §7 から不変)。

---

## 付録: 参照ファイル(絶対パス)

- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_rank1355_root_seed_scalars_v1.py`
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_rank1355_root_seed_scalars_v1.py`
- `C:\Users\81905\Desktop\shadow-atelier\.github\workflows\d972-r07-rank1355-root-seed-scalars-v1.yml`
- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_actual_grade2_root_scalar_batch_v2.py`(`:389-392` = R1-2 の pin ブロック)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_actual_grade2_root_scalar_batch_v2.py`(`:313-316` = 同上)
- `C:\Users\81905\Desktop\shadow-atelier\sol\sol_reply_939_audit_r07_rank1355_root_seeds.md`(静的 PASS・F1 の存在を明記)
- `C:\Users\81905\Desktop\shadow-atelier\docs\notes\seed30_mat_v1_cv9_reading_v1.md`(裁定 2105・本判読の親規律)
- `C:\Users\81905\Desktop\shadow-atelier\docs\notes\rsb_v2_cv9_reading_v1.md`(裁定 2096・19 規約表の初出)

---

本文（この区切りより上）の sha256 先頭 16 桁: `9ddaa1af28e33ef5`
