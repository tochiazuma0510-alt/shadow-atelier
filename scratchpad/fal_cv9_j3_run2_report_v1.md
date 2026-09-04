# CV-9 仕様同一性判読 — R07 actual grade-two root scalar batch v1(J3・副検問・事後)

判読者: falsifier(反証前哨・非当事者)
対象: GHA run `33903333330`/1(success)・terminal `RootViolationBatch`・head `386ee1753f45450857c68e1166932798add82d66`
日付: 2026-09-05
先例: `docs/notes/physconn_v11_cv9_reading_v1.md`(裁定 2048)・`docs/notes/separator_run2_cv9_reading_v1.md`(裁定 2060)
判読範囲: 「producer と checker が同一対象を計算しているか」の一点のみ(裁定 316/318 スコープ制限)。数学的正しさの監査・実装レビュー・追加テストの発案はしない。

---

## 0. 裁定

**同一対象(SAME OBJECT)。限定 4 条。**

producer と checker は「Separator λ(generation 8059・S₀ head `69fdcc8c…`・λ sha `7522ee1f…`)を Task712 の B 随伴で character 別に引き戻した root covector q に対し、固定 P1 8,059 行の射影と Task554 の 32,280 relation origin による blockwise fold(v540 §3)を行い、**v540 (2.4) の走査順で最初の非零 scalar** を返す」という同一対象を計算している。特に重点である**「最初の違反」の順序規約は両者で同一に固定**されており、別対象・判定不能の余地は見つからなかった。

ただし cross-checked の射程には **限定 4 条**(§3)が付き、その一つ(射程 = origin 0,1,2 の 3 件のみ)は工房側の文面に必ず書く必要がある。

---

## 1. 同一対象と判定した根拠(すべて確認済み・file:line)

| # | 規約 | producer | checker | 一致 |
|---|---|---|---|---|
| 1 | 4 親の入力 pin(P1 `9931437113` / Task554 5 body / Task712 `9915928157` / Separator `9944214057`) | `search/d972_r07_actual_grade2_root_scalar_batch_v1.py:36-110` | `search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py:33-91` | 同一 literal(id/name/bytes/digest すべて) |
| 2 | 同一 launch ファイルを両者が読む | workflow producer step `--run-launch $RUNNER_TEMP/launch.json` | checker step `--check-launch $RUNNER_TEMP/launch.json` | 同一ファイル・launch_sha256 を result に束縛 |
| 3 | λ の取得(`output/lambda.bin` 12,096 bytes・sha `7522ee1f…`) | `:587-590` | `:395-397` | 同一 |
| 4 | root covector = `sparse_adjoint(forward["B"], 36288, 48384, λ)` | `:654-655` | `:449-450` | 同一(同一関数・§2 の逐語クローン) |
| 5 | 子 = `sparse_adjoint(forward[actor], 36288, 36288, root)`・actor 順 (1,-1,2,-2) | `:656-657` | `:451-452` | 同一 |
| 6 | root/child の出力 pin(support 2742・lead 3・値 2・packed sha) | `EXPECTED_ROOT/EXPECTED_CHILD :114-130` | `:92-106` | 同一 literal |
| 7 | active character の pin(`[True,False,False,False]`) | `:681` `actual_active_root_pin` | `:558` `checker_active_root_pin` | 同一 |
| 8 | P1 射影(256 行 chunk・byte_offset = character×9072・sparse packed) | `:268-283`, `:697-719` | `:201-216`, `:575-594` | AST 正規化 0.9835 = 実質同一 |
| 9 | relation fold の順序(v540 §3 手順 1-4: prepare seed → prepare old-actor → block b の origin → block b の new-actor) | `accumulate_scalars :449-522` | `:478-535` | ループ入れ子・添字式(`ORIGIN_RANGES[source][0] + 44 + 4*pivot + slot`)が一致 |
| 10 | **走査順序(44 seeds → basis_i 0..8058 × slot 0..3)** | `_scan_accumulated :767-773` | `:625-634` | AST 0.9822 = 同一 |
| 11 | origin_id の採番と prefix chain(`sha256(chain ‖ canonical(record))`) | `:752-763` | `:611-623` | 同一 |
| 12 | Violation の封(`LIVE_SCHEMA + ".Violation"`) | `ARITH._sealed`(v15:1654) | 自前 `_sealed :646-648` | 生成文字列が同一 |
| 13 | relation source 受領証(5 body digest+ranks+offsets+actor order+counts) | `relation_source_sha256 :286-301` | `:219-234` | 実測値 `47effc68…` が両側一致 |

**相互束縛(fail-closed の実体)**: checker は character record 全体(封入り scalar オブジェクトを含む)を自前再構成して**完全一致**を要求(`:720-731`)、terminal/result/output-manifest も同様(`:734-743`)、出力ファイル名集合も完全一致を要求(`:770` `checker_output_exact_roster`)。したがって走査順序・fold 順序・pin のどこかがズレれば必ず落ちる。

**紙との一致**: `sol/proof_r07_actual_scalar_blockwise_fubini_v540.md:68-71` が走査順を「first 44 seeds, then the four actors for every old row in character order, then the four actors for every new row in character order」と固定し、`:93` が「Scan the final array in the order (2.4). The first nonzero entry is the v534 Violation」と定義する。実装の平坦走査(basis_i 昇順 × ACTORS)は、P1 の global order が old0..old3(505,503,503,503)→ new0..new3(1509,1512,1512,1512)である(manifest `global_order = [0,505,1008,1511,2014,3523,5035,6547,8059]`・両側が要求)ことから、紙の順序と厳密に一致する。

**数値恒等式(整数のみ・当哨が撃った)**: Σold = 505+503+503+503 = 2014、Σnew = 1509+3·1512 = 6045、2014+6045 = **8059** ✓。4·44 + 4·2014 = **8232** = TASK554_ORIGINS ✓。ORIGIN_RANGES 累積 2064/4120/6176/8232 ✓。44 + 4·8059 = **32280** = SCALAR_ORIGINS ✓。36288/4 = 9072 = SLICE_BYTES、4·9072 = 36288 = P1_ROW_BYTES、48384/4 = 12096 ✓。すべて一致。

**事前登録**: workflow env で 8 親の run/attempt/head/artifact id/name/bytes/digest を**計算前に**固定し、`gh api` + `jq -e` で live 照合(repository_id `1312092366`・`expired == false`・Task554 は `conclusion == "failure"` まで固定)。**silent cap は見つからなかった**: P1 cache は 8,059 行全消費 + trailing 空を強制(`:718` / `:593`)、cache の sha 再計算一致も強制(`:719` / `:594`)。

**ダミー検査(何にでも当たる試験)の検出**: 見つからなかった。両 selftest は 8 種の変異を**実行して**棄却する — task712 transpose 破壊・separator internal 受領証の改竄・p1 manifest digest 改竄・p1 cache 切り詰め・**バイト長を変えない task554 式の並べ替え**・整合再封された child/scalar-prefix・terminal claim / parent join・launch sha handoff。Sol 912 が指摘した「実行せずに `true` を返す」型は Task913/915 で修理済みであることをソース上で確認した。

---

## 2. 独立性の実体

### 2.1 checker は再計算している(確認済み)

`covectors()`(`:443-460`)は λ と Task712 テーブルから root/child を自前構成、`p1_values()`(`:552-599`)は 292 MB cache を自前で全ストリーム、`accumulate_scalars()`(`:478-535`)は prepare + 4 block を自前で再パースして 32,280 accumulator を再構成、`_scan_accumulated()`(`:602-643`)は走査を再実行。producer の出力は**中間状態の読み直しではなく**、完全再構成物との厳密一致で検査される。

### 2.2 しかし核は逐語クローン(確認済み・前回と同型)

| 共有単位 | 実測 |
|---|---|
| v15 モジュール先頭 **lines 1-424** | `diff` で**行 2-6(docstring)のみ相違**。`pack_trits`/`unpack_trits`/`dot_mod3`/`normal_terms`/`sparse_adjoint`/`_table_line`/`_read_table`/`_task712_root`/`table_identity`/`read_task712_envelope`/`canonical`/`sha`/`read_canonical`/`read_receipt` の全体 |
| `_raw_dual_keys`/`validate_raw_dual`/`_dual_next_state_head` | 逐語一致(producer v15:1071-1092,1292-1300 / checker v15:683-704,895-903) |
| **seed 生成核**(producer v15:443-826 ↔ checker v15:1820-2204) | 接頭辞正規化後の**トークン類似度 0.98713**。残る 18 個の差分ブロックはすべて一時変数(`begin`/`target_index`)・`;` による行結合・`vector`/`value` 改名・呼出カウンタのみ。**アルゴリズムは同一** |
| `SEED_REGISTERED_ROW_SHA`(両 v15:75) | 44 seed 行の連結ハッシュを**ハードコード pin**。同じ生成器から採った値なので、二系統一致の独立証拠にはならない(回帰 pin) |
| batch ファイル側(AST 正規化) | `vectorized_projection_chunk` 0.9835・`_scan_accumulated` 0.9822・`relation_source_sha256` 0.9943・`terminal_kind` 0.9934 |

**checker 側で本当に打ち直されている部分**: 親検証層(`state_descriptor` 0.13・`validate_task554` 0.41・`read_json` 0.10・`receipt` 0.49・`validate_separator` 0.70)と出力照合層(`check_output`/`validate_character_record`/`validate_output_objects` = producer に対応物なし)。`accumulate_scalars` は 0.67 だが差は局所変数名のみで構造は同一。

### 2.3 核クローンの risk 処理(当哨が撃った)

**v15 の F₃ 低位核は retire できる。** 素朴実装(基数 3 直書き・Python int 累算)との照合、pin された runtime `numpy==2.5.1` 上で:

- `pack_trits`: 全 3⁴ = 81 通りの 4-trit ブロックを網羅 → **不一致 0**
- `unpack_trits`: 全有効バイト 0..80 を網羅 → **不一致 0**。バイト 81 は `packed_digit` で棄却されることも確認
- 往復: 幅 36288 / 48384 / 145152 で一致
- `dot_mod3`: ランダム 200 本 + 全要素 2 の最悪ケース(幅 48384/145152)+ **uint16 溢れプローブ**(生和 160,000 > 65,535)→ **不一致 0**
- `sparse_adjoint`: ランダム 60 テーブルを密転置参照と照合 → **不一致 0**

**ただし条件付き**: `dot_mod3` が正しいのは numpy が uint16 の累算器を uint64 に昇格するからで(実測 `np.sum(uint16).dtype == uint64`)、uint16 のまま合計する処理系なら幅 16k 超で静かに誤る。workflow の `numpy==2.5.1` pin が安全性を担保している = **runtime pin が数学的前提の一部**。

**retire できない残り**: §2.2 の seed 生成核(約 384 行のクローン)。`direct[2]`(= 今回の答えを決める量)はここが産む。安価な全数照合は存在しない。第三の別導出実装(または Lean 層)が要る。

### 2.4 Sol 919 の Node replay が再計算したもの(確認済み)

`sol/sol_reply_919_audit_actual_root_violation_run2.md` の replay は **封・受領証の再計算であって算術の再計算ではない**。実際に再計算しているのは: artifact/ファイルの sha と byte、公開された q ファイルの基数 3 復号(support/lead)、埋込み封の canonical 再ハッシュ、5 body digest からの relation 受領証 `47effc68…`、そして **32 零バイトから `(seed0,0),(seed1,0),(seed2,1)` の 3 レコードだけを鎖ハッシュして prefix `d007a8d4…` に一致**すること。

λ から q、`<q,P_i>`、`direct[2]` を**独立に計算し直してはいない**。したがって算術系統は producer と checker の **2 つ(クローン核を共有)**であり、三系統ではない。しかも三者すべて Sol の実装である(前回と同じ「一著者多実装」)。

---

## 3. 主張の射程

### cross-checked と呼べる有限事実

- λ(generation 8059・S₀ head `69fdcc8c…`・sha `7522ee1f…`)を `B_adj_a0` の随伴で引いた character 0 の root q: support **2742**・lead **3**・lead 値 **2**・packed sha `af62027a…`、4 子はすべて support 2742(sha `aa54bbed…`/`1b982829…`/`f98650b3…`/`2245611c…`)。
- character 1,2,3 の root/child は**バイト単位でゼロ**(`RootZero`・実 cert で確認)。
- 固定 P1 artifact `9931437113` の 8,059 行を **1 パス**で走査(cache sha `b88edb9b…` 再計算一致・trailing 空)。
- Task554 の 5 body(digest 固定)から v540 §3 の blockwise fold を実行した結果、**走査順の origin 0(seed 0)= 0、origin 1(seed 1)= 0、origin 2(seed 2)= 1**。prefix chain `d007a8d4…` がこの 3 件だけを束縛。

### cross-checked ではない(必ず文面に書く)

1. **origin 3..32279 について何も言っていない。** 32,280 個の accumulator は計算されたが、走査は origin 2 で return するので **32,277 件は封も比較もされていない**。terminal の `global_relation_count: 32280` は定数リテラルで、走査数の証明ではない(`require(origin == SCALAR_ORIGINS)` は ScalarEOF 分岐にしか無く、未到達)。
2. **actor 分岐は実データで一度も評価されていない。** selftest の合成 accumulator でのみ通っている(§1 空虚性チェック該当。ただし selftest が実行されている分、完全な空虚ではない)。
3. **「violation batch 全体」ではない。** terminal `RootViolationBatch` は「4 character のうち少なくとも 1 つが Violation」の意味で、実質は character 0 の 1 件。checker 返り値の `root_characters: 4` は**リテラル定数**で「4 character を走査した」という意味ではない(3 つは root が零で scalar scan に入っていない)。
4. **dual orbit 504 の完全性は含まない。** `COMPLETE_DUAL_ORBITS=false`。`future_active_orbit_bound: 504`(terminal)・`future_orbit_bound: 504`・`remaining_independent_after_root: 503` はいずれも**両側ハードコード literal**で、再計算も検査もされていない(一致は無内容)。
5. **root q 自体は事前 pin への回帰照合**であって独立発見ではない(`EXPECTED_ROOT`/`EXPECTED_CHILD`・producer:114-130 / checker:92-106 = preflight Sol 909 由来)。この run 固有の新情報は「最初の違反位置」だけで、そこは pin されていない(= 答えを書いていない)。
6. GRADE2_MEMBER / GRADE2_NONMEMBER = NOT_DECIDED。**verified=false**(Lean 未)。

---

## 4. 指摘

**【要修正 F-1】凍結文書と実装の規約が食い違ったまま。** `sol/proof_r07_actual_scalar_blockwise_fubini_v540.md:34-35` は「Task554's canonical normal-form condition makes the indices strictly increasing」と宣言するが、これは実データに反する(Sol 918: seed 式 32/176・actor 8015/8056・DAG 1955/2014 が非整列)。実装は Task917 で「順序保存・重複禁止のみ」に修理されたが、**紙 v540 は未改訂**(`git log` の最終 commit `0b32fe68` は origin count 8100→8232 の修正のみ)。F₃ 和は可換なので**値には無影響**だが、CV-9 の主検問対象(凍結された規約宣言)が実装と食い違っている。→ v540 §1 の当該一文を実装に合わせて改訂。

**【要修正 F-2】v540 §4 の cert 要件が Violation 分岐で満たされていない。** `:127` は receipt が「all five parent identities, **the value-vector hashes**, the order constants and the scalar rolling hash」を束縛せよと宣言する。しかし `value_vector_sha256` は **ScalarEOF オブジェクトにしか無い**(producer:780 / checker:642)。実際に発行された cert(候補 artifact `9948564628` を Release ミラーから取得・zip sha `013fd8de…` が Sol 919 と一致・展開して確認)の `character-a0.json` / `result.json` / `terminal.json` のどこにも 5 本の value vector のハッシュが無い。checker が同じ値を再計算して完全一致を要求しているので**現物の同一性は担保されている**が、**宣言した cert 形と実 cert が違う** = 副検問の対象そのもの。→ Violation 側にも `value_vector_sha256` を入れる、または v540 §4 を「EOF 分岐に限る」と改訂。

**【要修正 F-3】格付け文面での数値引用。** checker 返り値の `root_characters: 4` と `relation_origins: 32280` はどちらもリテラル定数で、「4 character を走査した」「32,280 関係を検査した」と読める。実際は character 0 のみ実走・origin は 3 件しか検査されていない(§3-1,3)。文面ではこの二つを検査量として引用しない(引用するなら「宣言値」と明記)。

**【軽微 F-4】規約の非対称(現状 fail-closed)。** producer の RawDual は `separator["manifest"].get("state_head", SEPARATOR_STATE_HEAD)`(producer:735)、checker は定数 `SEPARATOR_STATE_HEAD`(checker:542)。Separator の state manifest には `state_head` キーが存在しないので(`search/d972_r07_grade2_physical_state_separator_v2.py:936-957` の manifest 構築に無し)実害なし。将来 Separator 側が同名キーを足すと producer だけ値が変わり RawDual の封が不一致になって checker が落ちる(= fail-closed)。→ producer も定数に固定するのが素直。

**【軽微 F-5】`safe_path` の境界が非対称。** producer は `path == root` を許容(producer:168)、checker は許容しない(checker:136)。全入力がファイル名なので実害なし。

**【軽微 F-6】`terminal_kind` の述語が両側で別フィールド。** producer は `scalar_schema.endswith("Violation")`(producer:858)、checker は `schema.endswith("RootViolation")`(checker:715)。到達ケースで同値なので今回は独立性の**プラス**に働いているが、意図的設計なら一行コメントが要る。

**【軽微 F-7】未検査の定数が cert に載っている。** `future_active_orbit_bound: 504` は terminal に常に載るが両側ハードコードで再計算も検査もされない。dual orbit 504 の主張(Sol 910)を cert が支えているように見えるが支えていない。→ terminal から外すか declared タグを付ける。

### 反証できなかった点(正直な範囲報告・保証ではない)

- **走査順序の規約**: producer/checker/紙 v540 の三者で一致。順序依存の抜け道は見つからなかった。
- **事前登録と silent cap**: 見つからなかった(§1)。
- **撤退条件**: producer/checker 各 40 分 `timeout`・job 90 分、**両方 success のときだけ** final candidate を publish(`if: steps.producer.outcome == 'success' && steps.checker.outcome == 'success'`)。超過時は diagnostics のみ = 行き先が決まっている。
- **「見つからなかった」を非存在と読む型**: 該当なし。本件の主張は具体値 scalar=1 という肯定的証拠であって陰性探索ではない。
- **分離条件・ダミー検査**: 8 種の変異が実行され棄却される(§1)。何にでも当たる試験は検出できなかった。

---

## 5. CV-9 裁定案 + 工房格付け案

**CV-9 = 同一対象(限定 4 条)。**

格付け案(一行):

> checker PASS(同一著者系統・親検証層と出力照合層は実装独立、F₃ 演算核と seed 生成核は逐語クローン)。**cross-checked は限定つき** — (i) 射程は固定 4 親(P1 `9931437113` / Task554 5 body / Task712 `9915928157` / Separator `9944214057`)に対する **character 0 の root covector と、走査順 origin 0,1,2 の 3 件のみ**(origin 3..32279 と actor 分岐は実データ未検査・characters 1-3 は root 零で scan 不実施)、(ii) root covector 自体は preflight 由来の**事前 pin への回帰照合**で独立発見ではない、(iii) `direct_seed_rows` の意味論は 98.7% トークン一致のクローン + 自己由来ハッシュ pin に依存し二系統一致では検証されない(F₃ 低位核は当哨が全数照合して retire・ただし `numpy==2.5.1` pin 条件付き)、(iv) `global_relation_count 32280` と dual orbit `504` は cert 上の宣言定数で検査されていない。**主張は「λ に対する character 0 の root scalar が seed 2 で 1(seed 0,1 は 0)」という有限事実に限り、GRADE2 MEMBER/NONMEMBER ではない。verified=false(Lean 未)。**

---

## 6. 当哨が実行したコマンド(要点)

- 両 batch ファイル・両 v15 モジュールの sha256 と全文読解
- `diff` で v15 先頭 424 行の逐語一致を確認(相違は docstring のみ)
- Python `tokenize` + `difflib` による seed 核のトークン類似度測定(0.98713)、および `ast.dump` 正規化による batch ファイルの単位別類似度測定
- pin runtime(numpy 2.5.1)上での F₃ 核の全数/敵対照合(pack/unpack 各 81 通り全数、dot_mod3 の uint16 溢れプローブ、sparse_adjoint 60 ケース)
- 恒等式の整数検算(8059 / 8232 / 32280 / ORIGIN_RANGES / 幅)
- 候補 artifact `9948564628` を Release `archive-gha-checkpoints` から取得(zip sha `013fd8de…` が Sol 919 と一致)、展開して実 cert の規約宣言を突合

GHA 発火・大規模計算・実装・修理はしていない。
