# task333 監査報告 — task328/A4-v3 code/performance audit

## 0. 裁定

**REJECT / UNEXECUTED**。本便は指定資料の全読みによる静的・敵対的監査だけであり、Python、Node、GAP、GHA、workflow、git、network は実行していない。

v3 の production は受理済み task198 receipt の実在 schema を誤読するため、最初の 6,441 行の前で停止する。それを直しても、successor defect は十個の tagged affine/Fox chain ではなく roof word の終端群値の hash であり、境界は正しい型・seed 数・生成作用を持たず、`B+K`、独立 checker、v247 anchor、34 owner mutation のどれも実装されていない。GAP driver は producer/checker を起動せず、生成される shell も stale checker SHA で直ちに失敗する。

したがって task330 の裁定どおり actual A4 authority は **1/3 のまま**である。SELFTEST も許可しない。lift / fake / Ihara への昇格はない。

## 1. 対象 identity

### 1.1 task328 の五成果物

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v3.py` | 33,283 | `a228657ddf900d503c6d9574cd8fbefb338b0817412fbe108e234cf28f0aebab` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v3.py` | 14,916 | `77ab461a03836597c552fa14f300ad39edf97c678e43eea268b6e3474c70552d` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v3.g` | 3,677 | `a338918b418d4167470cca09fcc7550bd5a7fd63820da7a60e5a320fbbbf0c02` |
| `search/certs/d972_r07_word_independent_successor_kernel_selftest_v3_20260828.json` | 434 | `b385994a1e0d44e6c4cde981ab7b91b2db97d26773889c1db8270372799afda4` |
| `sol/luna_reply_328_r07_task315_a4_v3_actual_local_evaluator_repair.md` | 6,457 | `125216a0dd8dd30fae34fe14d790f619eccdfb8ba2e107f9cc80ea71fc2bf28d` |

Luna reply に記載された checker SHA は実物と一致する。一方 driver L21 は旧 SHA `e10098766a07fe5542229b6dbda85fef7dcddb37de965aa3d56a07c1b5f95598` を pin しており、実物とは一致しない。

### 1.2 task198 の受理済み authority-v2 bundle

| file | bytes | SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_seven_context_roof_presentation_v1.json` | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json` | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt` | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt` | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json` | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |

Receipt self digest は `c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f`、manifest self digest は `0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684`。Manifest が記録する run/head は両側とも `33155710862` / `bed1d5e6b41477b8799f2a33a24e46f7800f9510`、artifact id は `9686477718`、zip SHA は `8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854` である。

Manifest 内の task198 source identity は producer 137,169 bytes / `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c`、checker 157,253 / `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1`、driver 20,541 / `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068`。

### 1.3 v3 が pin する local dependency

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_b345_seedspan_triple4_v1.py` | 535,219 | `fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29` |
| `ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json` | 231,570 | `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72` |
| `search/d972_r07_all_seven_extension_section_census_v1.py` | 66,109 | `878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b` |

参照監査した task176 checker は 84,980 bytes / `4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695`、final task193 producer/checker は 37,956 / `7ec85fe5b359a371e7c7c6b701426c5521d2a9651f560cba0193fa9c34aa2530` および 33,149 / `278903c62c8f742cb985f44267f5f428c12dac9c514117f91eb6ae0daea17940`。v3 は task176 checker も task193 の二実装も load しない。

## 2. Findings

### F1 — BLOCKER: 実 receipt schema を誤読し、production は row 1 に到達しない

受理済み receipt の 6,441-row roster は `receipt["Delta0"]["presentation"]["rows"]` にある。`layer_counts` と `normal_generation_proof` も同じ presentation 内である。Top level には `D_all`, `Delta0`, `Gamma`, `Q0`, `bridge`, `evaluator`, `resource`, `status`, `terminal` 等があるが、`rows`, `layer_counts`, `normal_generation_proof`, `contexts` はない。

Producer の正 branch は次の順で停止する。

1. `authenticate` は exact path と manifest/receipt/verdict の主要 digest を通せる。
2. `validate_receipt` L146 が top-level `layer_counts` と `rows` を要求し、最初に `ValueError("row/layer counts")`。
3. L146 だけを迂回しても L150 の `receipt["normal_generation_proof"]` が `KeyError`。
4. それも迂回しても `authenticate` L167 の `receipt["rows"]` が `KeyError`。
5. Schema adapter を部分的に足しても `LocalRuntime.reconstruct_context_registry` L296–299 は不存在の top-level `contexts` を要求する。
6. さらに後の `primitive_corpus` と checker も top-level `receipt["rows"]` を再度要求する。

Checker は `validate_authority` L59 の `receipt roster` で同じ理由により停止する。ゆえに production の第一 call は 6,441 行を一行も処理できない。

### F2 — BLOCKER: driver は job を実行せず、生成 shell も最初の source pin で失敗する

GAP source L17–39 は `ci/out/...v3.sh` を `PrintTo` で書くだけで、`Exec` がない。L40 の “source emitted” は producer/checker の実行 terminal ではない。

仮に生成 shell を別途実行しても、producer pin の次にある checker SHA test L21 が、実物 `77ab...` に対して stale `e100...` を要求して失敗する。さらに shell は SELFTEST 専用で production route がない。これは F1 より手前の driver-route first failure である。

### F3 — BLOCKER: `LocalRuntime` は一部の実 API を見つけるが、必要 object graph を構成しない

静的 callable trace は次のとおり。

| v3 call | 実在性・signature | 判定 |
|---|---|---|
| frozen E4 `reconstruct_quotients(q3)` | 実在し、actual E3/E4 `MatchedQuotient` を返す | 利用可能 |
| frozen E4 `cheap_context_registry(e4)` | 実在し、actual 31 contexts を返す | 利用可能。ただしその前に偽 top-level context gate が落ちる |
| task176 `build_fine_deletion(e3,e4,budget)` / `make_deleter(old,e3,e4,fine,q0_marked)` | 呼出 signature は実在 | 利用可能 |
| task176 `eval_word_coordinates(old,e3,e4,contexts,delete,word)` | 実在 | 利用可能 |
| task176 `blob`, `multiply_blob`, `inverse_blob` | v3 の引数形で実在 | 利用可能 |
| frozen E4 `canonical_packed_permutation(...)` | **不存在**。この helper の owner は task176 producer | L307 で停止 |

`LocalRuntime.reconstruct_quotients` L300–302 は callable の形だけを一つ見て `{"e4": module, "q3": dict, "contexts": ...}` を返す placeholder であり、quotient object の再構成ではない。幸い後段の deletion call は別の actual `self.e3/self.e4_quotient` を渡すが、報告される `self.quotients` は実 object でない。

また `identity` L311 は `bytes(40)` / `bytes(154)`、すなわち全零 byte 列である。Packed permutation identity は permutation identity と PC zero tail の codec に従う必要があり、これは群 identity ではない。Typed codec registry も構成されていない。したがって E3/E4、31 contexts、fine deletion、40 actors の一部には実在 API があるものの、現行 call graph では到達不能で、全体として actual object graph にならない。

### F4 — BLOCKER: successor defect の数学的型が違う

Roof identity `r=a_1^{e_1}\cdots a_n^{e_n}` の A4 input は、十個の tag を互いに混同しない affine/Fox left chain

`Def(r) = direct_sum_t sum_i rho_t(prefix_{i-1}) * delta_t(a_i^{e_i})`

である。逆文字では cocycle/Fox の逆元則を用い、各 occurrence の block/slot、raw packed blob、F3 raw coefficient を保存し、task198 の seven/eleven occurrence bridge を exact に通した後、完全な typed PB3/PB4 translated boundary `D` で剰余を取らなければならない。Frozen E4 には exact route `fox_gradient_without_sections(word, quotient, progress_hook=None)` があり、task179 型の occurrence-column 構成も参照できる。

v3 はこの関数を一度も呼ばない。`LocalRuntime.eval` は roof word の**終端群値**だけを十 context で求め、`bridge_defect` L330–336 はそれを 128-bit truncated SHA key `ten_index:1:hash` にして `factor_sign` を置くだけである。Component は常に `1`、block/slot と raw blob は消失し、同じ key の occurrence は加算せず上書きされる。Roof identity の終端値は本来 identity なので、これは Fox derivative の情報をまるごと失う。Hash、ledger sign、group value のいずれも affine chain の代用品ではない。

さらに群 identity gate、raw coefficient replay、exact occurrence ancestry がない。これは schema 修正とは独立の数学的 REJECT 事由である。

### F5 — BLOCKER: 13-seed と x/y closure は型も生成群も誤る

v269 から継承した「13 base rows」は、十個の independently tagged summands には適用できない。v3 自身の `CONTEXT_TYPES` は PB3 型 5 個、PB4 型 5 個なので、correct base roster は

`5 * 2 + 5 * 11 = 65`

raw seeds である。同じ quotient element でも tag が違えば別 coordinate であり、統合できない。v163 の distinct `H1/H2/P` occurrence-block 表現を採る場合でも `2+2+11=15` であって 13 ではない。したがって task333 本文に残った 13-row 前提自体を load-bearing premise として採用しない。

また L239 の `(1,-1,2,-2)` は source `x,y` と逆元だけであり、complete PB boundary の生成作用ではない。Cross-checked task176 actual receipt では E4 context singleton image order は S5–S7 が `357,128,352`、S8–S9 が `119,042,784` であるのに対し、pinned coarse Q4 order は `583,152,628,325,845,597,028,352`。従って各 context の x/y pair が full E4 marked quotient を生成することはない。

境界を**明示 orbit queue で全展開する方式**なら、tagged PB3 coordinate ごとに 3 marked generators とその逆元、すなわち 6 actions、tagged PB4 coordinate ごとに 6 marked generatorsとその逆元、すなわち 12 actions を用いる必要がある。各 coordinate の最終受理 pivot 数を `b_t` とすると、action candidate の正しい上界は

`6 * sum_{t in PB3 tags} b_t + 12 * sum_{t in PB4 tags} b_t <= 12*b`

であり、これとは別に 65 initial seed insertions がある。従って v271 型 explicit queue の total attempted insertions の粗い上界は `65+12*b`。現行の `13` initial / `4*b` candidate bound は不正である。ただし E4 rank が巨大化し得るので、この explicit full-marked queue は完全性 oracle/参照上界であって、修復版の hot path に採用すべきではない。

実装上も、L235 と L243 は新しく受理した pivot ではなく毎回 `echelon.rows[min(echelon.rows)]` を queue に入れる。そのため、誤った四作用についてさえ全受理 row の orbit closure にならない。Parent/action ancestry は文字列と boolean だけで raw coefficient を持たない。

Checker L124–140 も不存在の `bridge.base_boundary_rows` 13 本を要求し、52 個の shaped column を作るだけである。`q=(g,-g)`、`(q[0],-q[1])==(g,g)` は恒等的な tuple 操作で、群積 `q h=g`、support inversion、dual column、rank rise のどれも計算しない。`strict_rank_rises`, `complete_zero_correlation`, `two_way_span` は hard-coded。Task193 の最終 producer/checker も呼ばれない。

### F6 — BLOCKER: v268 の三 ancestry grammar と trie evaluation が実装されていない

Authenticated 6,441 rows は `Gamma_Cayley` 6,318、`action` 104、`Q0_lift` 19 で、三つの別 ancestry grammar を持つ。Producer は式 (1.2)–(1.4) を layer ごとに replay せず、各 row の保存済み `word` をそのまま source DAG にして直接評価する。Ancestry から組み立てた word と authenticated row word の equality gate はない。

`primitive_corpus` は空 word を `if w` で落とす。v268 の 288 inventory に含まれる identity section word が空なので、正しい roster を渡しても 288 gate を満たせない。Production が返す prefix/suffix edge inventory `15970/26136` は hard-coded で、構築した trie edge 数との equality を要求しない。

Prefix trie は各 node に value を一個しか持たないまま十 context に対して `evaluate` を十回行うため、後の context が前の値を上書きする。Terminal-to-word map もなく、trie value は全 6,441 row の組立てに一度も使われない。DAG は source node だけで、`conjugate` と `materialize` は実 closure で使われない。

Checker の reverse suffix trie は group element を評価せず、L148 で `(letter,suffix)` という nested tuple を作るだけである。`row` L150–151 は全 word に同じ固定十-key dictionary を返し、producer row と key set だけを比べる。Coefficient、blob、word、direct quotient evaluation は比べない。

### F7 — BLOCKER: 実 group-operation 数は v268 bound から桁違いに外れる

Authenticated stored row word length の合計は `5,475,488` letters。`run_actual` は各 row を trie から組み立てず `runtime.eval(word)` する。これは十回 `_frozen_eval` を呼び、各 `_frozen_eval` がさらに task176 `eval_word_coordinates` で十 context 全部を再評価する。従って到達性だけを直した場合の row work の下界は

`100 * 5,475,488 = 547,548,800`

quotient context-letter steps である。加えて 40 actor の構成は `40*10=400` one-letter context evaluations、prefix trie は `15,970*10=159,700` component multiplications を行うが、その trie 結果は捨てられる。

v268 の設計上限は producer 28,937 ten-context tuple multiplications（289,370 component ops）、checker 39,103（391,030 component ops）である。現行 producer は cache を構築したうえで使わず、少なくとも 5.475 億 letter-step を追加する。性能 gate を満たさない。

### F8 — BLOCKER: `B+K`、coefficient replay、dual、v247 anchor がない

`boundary` と `total` は別 Echelon で、boundary row は `total` に一度も挿入されない。`total` は 6,441 initial `K` row だけで、`B+K` の rank、`K mod D`、boundary difference のどれも計算しない。K に必要な source `x^±1,y^±1` の四作用 closure もなく、各 initial row を一回挿入するだけである。ここで四作用が正しいのは **K の source closure** に限られ、F5 の full typed boundary `D` を四作用で生成できるという意味ではない。

Producer Echelon の coefficient algebra に符号誤りがある。L201–206 の `reduce` が返す `old` は `remainder = input + replay(old)` を満たす。正規化後の ancestry は `{label:scale} + scale*old` であるべきだが、L211 は `{label:scale} - scale*old` を保存する。既存 pivot で reduction が起きた受理 row の replay は失敗する。Dependent insertion は `None` だけを返し、zero relation certificate を保存しない。Boundary accepted row の coefficient replay もない。

`dual({"__target__":1})` は authenticated typed universe 外の人工 coordinate を入れ、remainder の最小 key に 1 を置くだけである。全 row annihilation の back-substitution も、target pairing も、独立 checker correlation もない。

Checker MaxPivotEchelon は reduction で得た old coefficients を捨て、常に `{label:scale}` だけを保存する。さらに L158 は string label ではなくその数値 coefficient を `echelon.raw[...]` の key に使うため、到達すれば最初の pivot replay で `KeyError` になる。

Basis item には source word/node の materialization がなく、integer word DAG、normalization、prior-K factors、inverse/exponent-two、boundary-difference ancestry がない。L366 の anchor は `word_bearing`, `direct_actual_eval`, `h2_projection`, `inverse_scalar:2`, `powered_word`, `least_index:0` を literal boolean/integer で宣言するだけで、actual basis から v247 の H2 projection、least nonzero index、inverse scalar、powered word、coarse/successor/context gates を計算しない。Action matrices、basis change、two-way span もない。

### F9 — BLOCKER: 34 mutations は owner gate を一つも試験せず、checker は 26 個しか持たない

Producer は 34 名を列挙するが、`synthetic_certificate` L378–385 は private copy に `mutation_owner_payload[owner]=name` を足して digest change を確かめ、validator を呼ばずに `owner_validator_rejected` と記録するだけである。Positive/kernel/boundary/anchor/resource-stop の本体も fixture literal である。

Checker `MUTATIONS` は最初の 26 名だけで、次の八 owner を欠く。

- `missing_base_boundary`
- `changed_boundary_block_tag`
- `left_right_translation_swap`
- `omitted_inverse_action`
- `changed_parent_action_ancestry`
- `incomplete_queue_claim`
- `wrong_support_inversion_product`
- `false_zero_correlation`

Checker も private copy の hash が変わることしか見ず、mutant を owner gate に投入しない。しかも checker selftest L163 は producer `attempted/rejected == 26` を要求するが producer は 34 を出すため deterministic failure。仮にそこを越えても checker の terminal line は `26/26`、driver L32 は `34/34` を要求する。従って SELFTEST route 自体が内部不整合である。

Producer L412 と checker L192 は全 `Exception` を `UNKNOWN_INPUT` に潰し、checker は文字列上 `...CHECKER_PASS terminal=UNKNOWN_INPUT` と出す。Owner-specific failure と implementation bug を区別する narrow exception discipline もない。

### F10 — authority/canary/seal は部分的に良いが、commission gate を満たさない

Producer が task198 五 input の resolved exact path、manifest/receipt/verdict の主要 SHA、receipt self digest、attestation hash を照合し、frozen E4/q3/task176 producer を bytes+SHA pin する点は有効である。しかし次が欠ける。

- Manifest self digest は保存 literal と比較するだけで、manifest body から再計算しない。
- Manifest の run/head は見るが、artifact id、member bytes/SHA、zip SHA、terminal member 全体を producer/checker 両側で exact replay しない。
- `task198_source_identities` は path shape だけで、記載された三 source の実 disk bytes/SHA を照合しない。
- Receipt の ordinal scan、seven chunks、presentation row digest、normal proof、bridge 全 spellings を実 schema から再照合しない。
- Evaluator は `entry_points` の存在だけを見て、receipt の actual canary、multiply/inverse/action/source-section/section-cocycle law を replay しない。
- Checker は producer よりさらに少ない三 digest と top-level 誤 schema だけで、attestation、source identity、chunks、bridge、ABI canary を独立再構成しない。
- Output path は caller が与えた任意 basename を `ci/out` 内なら受け入れ、登録済み exact output basename を要求しない。
- Checker verdict は self seal を持たない。

### F11 — resource accounting、serialization、sentinel が成立しない

- Producer は receipt を全 read/JSON parse してから `input_bytes` を charge するため、cap が allocation を防がない。Pinned module/json も hash 用 read の後に loader/read-text で再読する。
- `rss_bytes` は実測されず 0 のまま。`decoded_word_length`, `boundary_records`, `membership_queries`, `dual_correlations` は charge されない。Authenticated stored words は 5,475,488 letters なので、名前どおり全 decoded letters を数えるなら宣言 cap 4,000,000 を既に超える。
- Fine deletion は task176 の別 `Budget` で動き、v3 Meter に実 work が統合されない。
- Parsed 6,441-row receipt に加えて `initial_rows` 6,441 本を output に保持する。Reply328 の streaming/memory claim と一致しない。
- Actual positive result に `resource` field がない。Checker positive resultにも cap と final resource snapshot がない。
- `write_sealed` は serialization 前の値を encode してから meter を bump するため、serialized byte charge と final sealed payload が同じ snapshot にならず、write 自身も sealed resource に反映されない。
- Emitted shell は `set -eu` だけで `pipefail` と timeout がない。V authority verdict は 150 bytes だけで SHA を pin せず、receipt/attestation も driver pin しない。
- Stale output は拒否せず L28 で削除する。L27 の sentinel 名も実 PO/CO/log/OK 名と一致しない。
- PTERM/CTERM は各行数を別々に数えるだけで producer/checker terminal equality を要求しない。OK は emitted shell の末尾に文字列として置かれるが、GAP driver 自身は shell を実行しないため sentinel-last の証拠にならない。

Python 本体に sleep/retry/poll/lock/subprocess は見当たらないが、これは上記の blocking failures を救わない。

## 3. First failure と独立した追加 failure の順序

| entry route | 最初の failure | その後を仮修正した場合の次の load-bearing failures |
|---|---|---|
| GAP driver | shell を emit するだけで producer/checker を実行しない | 手動 shell 実行なら checker SHA pin mismatch、次いで 34/26 selftest mismatch |
| direct producer production | `validate_receipt`: `row/layer counts` | nested normal proof/rows、fake contexts、missing packed helper、空 primitive、missing boundary field、wrong defect、wrong closure/echelon/anchor |
| direct checker production | `validate_authority`: `receipt roster` | missing 13 seeds、tuple suffix evaluator、fixed row、MaxPivot replay `KeyError` |
| direct SELFTEST pair | producer は synthetic 34-record receipt を作る | checker が 26 を要求して停止。意味的 owner mutation も皆無 |

F1/F2 を直しても F4–F9 は互いに独立な数学的・checker 的 REJECT 事由である。従って「最初の例外だけを直して再実行」は許可できない。

## 4. 最小の versioned repair

これは数行修正ではなく、少なくとも `v4` として次を同時に置換する必要がある。

1. Task198 receipt の唯一の schema adapter を作り、`Delta0.presentation.rows/layer_counts/normal_generation_proof` と actual context/bridge spellingsを producer/checker 双方が独立に exact seal・ordinal・chunk・canary まで読む。
2. Frozen E4/task176 の実 owner/signature に binding し、actual packed identity/codec、E3/E4、31 contexts、finite deletion、40 actors を構築する。Placeholder `quotients` は廃止する。
3. v268 の三 ancestry grammar を literal replayし、prefix/suffix trie に **affine ten-tuple state** と terminal map を持たせ、assembled word を authenticated row word と直接比較する。6,441 long words の再評価を禁止する。
4. 各 row に `fox_gradient_without_sections`（checker は独立等価実装）を適用し、十 tag、occurrence block/slot、raw blobs、F3 coefficients を保つ exact affine chain/bridge を構築する。Hash key と終端群値を廃止する。
5. 五 PB3 tag×2 と五 PB4 tag×11 の **65 tagged base families** を pinned arithmetic から再構成する。Full-marked orbit を hot path で materialize せず、v272 型 support-inversion lazy column generator で authenticated `(i,j,t=g h^-1)` column universe を与える。v271 型 full-marked queue は小さい canary と完全性 oracle に限定する。
6. K は source `x^±1,y^±1` の四作用だけで closure し、coefficient-bearing active `B+K` echelon を作る。Target を `B+K` で reduce し、zero なら **MEMBER** として明示 B/K raw replayを返す。Nonzero なら typed universe 内で dualを back-solveし、全 `(i,j,t=g h^-1)` boundary columnsとの相関を取る。非零相関があれば witness column を active B に一本だけ追加して rank-strict に反復し、全相関 zero なら full `D` annihilation を伴う **NONMEMBER** dual を返す。受理・従属の両方に raw coefficient replay を持たせ、現行の符号誤りを直す。
7. Basis ancestry から integer wordを materializeし、normalization/prior-K/boundary difference を replayしてから actual ten-quotient direct evaluation、v247 H2/least-index/inverse-scalar/powered-word gates を計算する。Anchor literal を廃止する。
8. Producer/checker 各 34 mutation をそれぞれの owner validator に本当に投入する。Checker は arithmetic/tries/boundary/echelon を producer 非共有で再構成し、row coefficients、basis change、dual correlations、terminal を exact 比較する。
9. Driver は正しい bytes/SHA を pin して production pair を timeout 付きで実行し、stale artifact を削除せず拒否し、sealed verdict と exact-one/equal terminals を確認した最後にだけ sentinel を作る。全 read/parse/work/RSS/serialization を final sealed resource snapshot に charge する。

Performance の hot-path 事前登録は lazy 方式で行う。Full boundary column universe の大きさを `N_SI`、active boundary の最終 rank-rise 数を `r_B` とすれば、追加 column は高々 `r_B` 本、full-correlation pass は高々 `r_B+1` 回、correlation query は高々 `(r_B+1)N_SI` である（各 nonzero pass で一本だけ追加し、最後の zero pass が full `D` annihilation certificate）。`65+6*B3+12*B4 <= 65+12*b` は explicit v271 oracle の比較上界であって production hot path の目標ではない。Word 側は affine prefix/suffix trie により producer 28,937 / checker 39,103 ten-tuple multiplication envelope を基準にする。この設計と静的再監査が完了するまでは実行対象にならない。

AUDIT: REJECT / EXECUTION: UNEXECUTED (SELFTEST 不許可、actual A4 authority = 1/3).
