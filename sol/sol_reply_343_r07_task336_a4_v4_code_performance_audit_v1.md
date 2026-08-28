# task343 監査報告 — task336 A4/v4 code/performance audit

## 0. 裁定と実行境界

**REJECT / UNEXECUTED**。本便は指定入力と実バイトの静的・敵対的監査である。Python、Node、GAP、GHA、workflow、network、git、producer、checker は実行していない。実装にも触れていない。

v4 には v272--v274 の数学的核の一部が実際に書かれている。しかし literal production は最初の 6,441-row 処理より前に停止し、SELFTEST も 48 mutation の途中で hard stop する。それらを局所修正しても、checker は suffix trie の群/アファイン値を一度も構成せず、6,441 rows、chronological B/K oracle、MEMBER/NONMEMBER、word recurrence、action closure、v247 anchor を独立に再構成しない。従って SELFTEST も production も許可できない。A4 は入力 authority の **1/3** のままである。

## 1. 実物 identity と dependency graph

### 1.1 v4 の四 machine files

PowerShell の read-only byte/hash で再計算した。Reply336 の数値とは一致する。

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v4.py` | 98,454 | `d895996da8c6014327028d5bd5c7076f27aa481f2d68511ac2cdbd55b1adaa6c` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v4.py` | 49,223 | `e006cfef8f6c650298f8ceaab0522c9459d5868d6d25939d575177eee60fc3eb` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v4.g` | 7,087 | `6cf2553045090a9dca8003fa8d5a6d6378811f666809aff61b851d4309ecb53a` |
| `search/certs/d972_r07_word_independent_successor_kernel_selftest_v4_20260829.json` | 593 | `2cbf25f57c9b28c9b8b212b5ac6b56c10fc570ea33a75f1e3eb5adaa50c38c16` |

### 1.2 load-bearing pins

| owner | bytes | SHA-256 |
|---|---:|---|
| task198 receipt | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| task198 acceptance-v2 manifest | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| task198 producer attestation | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| task198 checker attestation | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| task198 checker verdict | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |
| task198 producer source | 137,169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| task198 checker source | 157,253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| task198 GAP driver | 20,541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |
| task176 producer source | 66,109 | `878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b` |
| task176 checker source | 84,980 | `4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695` |
| task176 accepted receipt | 13,649,089 | `715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41` |
| task176 artifact manifest | 349 | `de62e5e55a2e348a3cce297764f7ff4bfedc10ebe2545f22cbc1551f15e1adc1` |
| frozen q3 receipt | 231,570 | `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72` |
| pinned E4 arithmetic | 535,219 | `fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29` |
| A4/v1 producer | 89,162 | `fe5dcf38b774b15c1a2907e70f8e6f90beca90b887aef1e0ea661f486817b862` |
| A4/v1 checker | 55,388 | `157c61927884eeb3d7a01d1f6e8df6755e52dc708353fdb38eb7ad57239333d2` |

Task176 receipt は `status=COMPLETE` / `terminal=R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS`、manifest は run `33044121344`、head `0533e42019c9f67f6cec3d1566152db17b903836`、artifact `9635036013`、ZIP `250e25c9...89912` である。V4 はこの receipt、manifest、checker のいずれも読まない。

### 1.3 literal import/process graph

```text
GAP driver
  -> exact-pin tables
  -> writes one bash shell
  -> GAP Exec(shell)
       -> timeout 14400s producer
       -> timeout 14400s checker
       -> token comparison / verdict nonempty+seal-string / sentinel last

producer
  -> Python stdlib only
  -> dynamic import pinned d972_b345_seedspan_triple4_v1.py
  -> pinned q3 JSON
  -> hashes task176 producer source only
  -> never imports task176, never reads task176 receipt/checker

checker
  -> Python stdlib only
  -> dynamic import the same pinned E4 arithmetic helper
  -> pinned q3 JSON
  -> does not even hash TASK176_SOURCE although a constant is declared
  -> never reads task176 receipt/checker
```

Python 両本体に subprocess、pool、thread、sleep、retry、poll、lock はない。ただし checker は producer と同じ `reconstruct_quotients` / `f2_substitute` / `fox_gradient_without_sections` / `pure_relations` / quotient arithmetic を同一 dynamic module から使う。「helper 非共有 arithmetic」ではない。

## 2. Literal reachability と最初の failure

### 2.1 PRODUCTION

Actual task198 receipt の canary keyset は読み戻しで

```text
nonsplit_y_y_section_cocycle, source_2_2, x, x_action_y,
x_inverse, xy, xy_section_cocycle, y
```

であり、`y_inverse` は存在しない。

| route | literal first failure |
|---|---|
| GAP production | authority adapter と 40 actor 構成の後、producer L695--698 が存在しない `y_inverse` canary を要求し `evaluator:canary_direct:y_inverse` |
| direct producer production | 同じ。`UNKNOWN_INPUT reason=...` を出し exit 1 |
| direct checker production | checker Authority L331--333 がさらに keyset 自体に `y_inverse` を要求し `authority:evaluator_canary_names` |

Bash は `set -eu` であるため、producer exit 1 で直ちに中断し、checker、terminal grep、verdict、sentinel に到達しない。しかも driver L62/L68 の regex は行末直前に terminal token を要求するのに、producer/checker の UNKNOWN 行は `reason=...` を後続させる。Exit status を仮に無視しても UNKNOWN 行は regex に一致しない。

`y_inverse` を「actual receipt にないので要求しない」と最小修正し、cap が十分大きいと仮定すると、producer の次の決定的 failure は第 6,319 行目、最初の `action` row である。実 receipt の 288 primitive corpus は空語を含むが、`[1]`, `[-1]`, `[2]`, `[-2]` を一つも含まない。それに対し `assembled_row` L1337--1341 は作用字を単語 primitive として `materialize_piece` へ渡すため、L840 の `trie:missing_primitive_inverse_terminal` で停止する。Actor cache を直接使うべき箇所である。

さらにこれを仮修正しても positive pair は閉じている。

- K 作用 query が一つでも NONMEMBER/rank-rise なら、その作用の係数列を action matrix に記録しない。後で再 query しないため L1508 `K:complete_source_action_matrix` は失敗する。
- 全 K 作用が MEMBER で producer が透過した場合、`oracle.rounds` に必ず MEMBER record が入る。その record には `dual_support`, `correlation_pairs`, `selected_column/complete_zero_accumulator` がないため、checker L696--700 が `producer:dual_meter` で拒否する。

従って actual データの未知な rank に依存せず、現行 source の end-to-end positive route は到達不能である。

### 2.2 SELFTEST

Producer SELFTEST は最初の 34 mutation に対し、実 owner ではない `typed_mutations[name]` を付け、その flag を見て明示的に `Reject` する。35 番目 `omitted_candidate_discrepancy` では `mutation_payload` L1632 が `mutant["kernel"]` を参照するが、SELFTEST cert にあるのは `boundary.sample_E_new` であり `kernel` は存在しない。ここで `KeyError('kernel')`、producer `..._STOP KeyError`、exit 2 となる。Bash `set -e` が checker の起動前に停止させる。

この key path を仮修正しても、48 本は production owner ではなく miniature dict の shaped field に対する明示 `Reject` である。Fixture の `expected_mutation_count=48` も producer/checker のどちらも検査しない。Checker SELFTEST も sealed producer の terminal を requirement にせず、`producer_certificate_seen` Boolean に写すだけである。

### 2.3 terminals / malformed / cap / cleanup

- `MEMBER`: producer 局所コードは combined raw B/K replay を行うが、checker はその時系列係数を再構成しない。
- `NONMEMBER`: producer 局所コードは finite dual と 65-seed correlation を計算するが、checker は producer transcript ごとの再 correlation をしない。
- `UNKNOWN_INPUT` / malformed path/input: producer は reason 付き exit 1、driver は checker 前に中断する。
- `UNKNOWN_RESOURCE`: 同様に reason 付き exit 1。Certificate/checkpoint を書かず、checker に渡さない。
- hard exception: `*_STOP` / exit 2。数学 terminal に変換しない点だけは正しいが、driver は fail する。
- cleanup: atomic temp+rename はなく `write_bytes` 直接である。Cap/hard stop の後の回復所有者もない。

## 3. Authority、affine/Fox、trie、6,441-row semantics

### 3.1 実装された部分

- Producer/checker は task198 五ファイルの top-level exact path、bytes/SHA、manifest/receipt self seal、run/head/artifact/ZIP/member、attestation を照合する。
- Rows/layers/proof を `receipt["Delta0"]["presentation"]`、bridge を `receipt["bridge"]["occurrence_ledger"]` から読む。V3 の top-level schema 誤読は修正された。
- 6,318/104/19 local ordinals、declared seven chunks、normal proof の主要数値、bridge map/order、ABI name/width、false witness flags は照合する。Receipt は一度 read/parse し、output に 6,441-row roster をコピーしない。
- Producer の十 context は実 A4/v1/task232 の固定置換と一致する。Actual `reconstruct_quotients`、`f2_substitute`、`fox_gradient_without_sections`、quotient multiplication/inversion を用い、`(a,u)(b,v)=(ab,u+a.v)` と逆元を実 sparse F3 で計算する。Roof hash/placeholder ではない。
- Producer は三 ancestry grammar の literal word equality を全 row で検査し、prefix trie の terminal affine 値を row assembly に実際に使う。

### 3.2 authority の欠品

- Manifest 中の task198 三 source identity は dict の文字列として照合するだけで、現在の三 physical source の bytes/SHA を producer/checker のどちらも読み戻さない。Driver もこれらを pin しない。
- Task176 は producer source のみ producer が hash する。Accepted receipt、artifact manifest、independent checker、v247 の direct ten-coordinate canary を両側とも読まない。Checker は task176 producer source すら読まない。
- Seven chunk SHA と `rows_sha256` は declared value を比べるだけで、actual row slices/whole rows から再計算しない。Bridge occurrence/typed-coordinate digest も declared value だけで、11 項目の exact block/slot/context/orientation/role/sign/spelling から再計算しない。6,441-relator bridge replay digest もない。
- Normal proof は部分照合であり、checker で `all_record_generator_closure_order`, `marked_action_loop_count` 等が欠ける。
- ABI canary は roof values の一部だけを再計算し、source-section / section-cocycle の actual law、bridge canary、task176 direct canary を再生しない。その上、存在しない `y_inverse` を発明して first failure にしている。
- `input_bytes` は `read_bytes()` で 31 MB を allocation した後に charge する。E4 module は hash と import で二回読み、q3 も hash と text parse で二回読む。

### 3.3 trie/row の決定的欠品

- Actual inventory 243 sections / 26 records / 19 q0 relators / 288 primitives / 114,458 primitive letters / 15,970 prefix edges / 26,136 suffix edges / 5,475,488 stored row letters は実 receipt と一致する。
- Producer prefix trie は topology を作るが、terminal 毎に root から全 path を再生する。Prefix edge を一回ずつ評価せず、terminal work は 15,970 ではなく 114,458 ten-context edge applications である。
- Producer row assembly は identity から全 part を multiply するため、actual tuple multiplications は `3*6318+4*104+2*19=19,408`。V268 の first-part assignment を用いた 12,967 より 6,441 多い。この row-assembly sparse work は meter に charge されない。
- Producer は trie assembly の後に **全 6,441 long words** を `runtime.direct_row` で flat evaluate し、MEMBER または accepted K の分岐で同じ word を `exact_discrepancy` からもう一度 flat evaluate する。Fixed six-row sample に限定されていない。
- Checker `ReverseSuffixTrie` は edge topology と `opposite` dict を作るだけで、roof/affine state、terminal value、right-associated recurrence がない。Main はその trie を row assembly に一度も使わず、authority rows の literal ancestry 式を比較するだけで `row_assemblies += 1` と計上する。Checker-owned 6,441 affine rows と producer rows の照合は存在しない。

## 4. Full-D lazy oracle / finite-active dual

### 4.1 producer で実際に実装された核

Producer 側の次の部分は shaped declaration ではない。

1. `5*2+5*11=65` の tagged PB3/PB4 Fox seeds を actual `pure_relations` から作り、roof identity を要求する。
2. Raw row key `(context,component,element)`、raw ledger key `(context,relator,translation)`、actual quotient inverse/multiplication を使う。
3. Active registry を target と live combined B/K row support の和集合とし、actual projection echelon の back-substitution から dual を作る。All-live-row dot zero と target dot nonzero を直接検査する。
4. 65 seeds の全 occurrence で `t=g*h^-1`、`t*h=g`、coefficient accumulation、lex-first nonzero key、actual translated column、strict rank rise を行う。
5. MEMBER で actual B/K raw coefficient replay、NONMEMBER で complete accumulator と dual pairing を producer 内で計算する。

### 4.2 正しさ/独立性/性能の欠品

- Typed occurrence は `(context,component)` で preindex されていない。各 seed occurrence に対し dual 全 support を走査するため、実 CPU work は matching-pair 数 `P_q` ではなく `O_total * ell_q`。Meter は match した pair だけ数えるので、実 slow work を過少申告する。Accumulator は zero entries も保存/出力する。
- `active_keys`, `bplusk_rank`, `dual_support`, `all_row_dots`, `target_dots`, `new_keys` の多くは `Meter.bump` ではなく counter 直接代入/加算であり、対応 cap を超えてもその場で止まらない。Active set/dual/accumulator の大 allocation も cap check より先である。
- Checker は chronological B/K rows を構成せず、最初の producer K row 一本を空 basis に対し probe するだけである。Producer の各 dual、active registry、selected column、rank rise、zero accumulator、MEMBER coefficients を再計算しない。
- Checker L896--899 は producer の `all_row_dots` / `target_dot` Boolean を信用し、`complete_all_65` が欠けていても default `True` で通す。これは task343 の明示 REJECT 条件である。
- Checker-owned `MaxPivot` は pivot を descending で reduce するのに、dual pullback も同じ descending 順で行う。Projection の逆順、すなわち ascending が必要であり、multirow で old row が later/lower pivot を持つ場合に一般に誤る。Current main はこの関数を zero-row probe でしか使わないため、実 multirow gate に到達しない。

## 5. K chronology、boundary discrepancy、word、anchor

### 5.1 producer で正しく書かれた recurrence

Producer の internal reduction は `remainder=input+correction` である。Export 時に

```text
r = v - Psi(Q) - sum(c_l*k_l),    k_new = s*r
```

へ符号変換し、`accept_k` は literal に

```text
W_new = (W_v * product_l W_l^(-c_l))^s
E_new = s*(E_v + Q - sum_l c_l E_l)
```

を作る。Initial row は `E_v=0`、source conjugate は actual context actor による全 raw key の左 translation を使う。`exact_discrepancy` は literal word の ten-context raw defect と `representative+Psi(E)` の exact equalityを検査する。これらは v273 の本質的実装である。

### 5.2 欠品

- Action rank-rise の matrix coefficient欠落は §2.1 のとおりで、「新 K が必要な closure」を実装したはずのルート自身が final matrix gate を通らない。
- `WordDAG.materialize` は memo なしの再帰展開である。`source`, `inverse`, `conjugate`, `product` の展開文字数を charge せず、`power` の最後だけを展開後に charge する。Prior K words を literal で繰り返し結合するため、係数/DAG の増大に対する有効な事前 cap がない。
- `exact_discrepancy` は同じ ledger の `Psi` を equality 用と output 用に二回展開し、各 raw key で 65 seeds を linear search する。
- `pairwise_commutation` は全 ordered K pair×10 contexts で連結 long word を再 Fox-evaluateする `O(10 t^2)` の大きな不要 work である。V273 の exact item replay と elementary-abelian target から必要な checker canary は有界 sample でよい。
- Checker が行うのは各 producer K word の `delta(W)=representative+Psi(E)` だけである。Candidate/parent/action、`Q,c,s`、increasing prior order、word DAG、rank independence、dependent coefficient、queue、action matrix を再構成しない。任意の actual word とそれに合う representative/E を producer が出せば通る。
- Producer anchor は actual K words を built-in H2(9) へ投影し、least nonzero、inverse scalar、literal power、`(0,0,3)`、ten-context raw replay、current K membership を実際に計算する。ただし task176 accepted receipt/checker と v247 の projected-kernel premiseを authenticate しない。Checker は H2 projection、least index、scalar、powered word、anchor membership を一つも再計算せず producer fields を形だけ見る。

### 5.3 v280 の下流 trust boundary に対する裁定

**NO――v4 は、v280 の A5 consumer が anchor と area-adapted basis を Boolean-free に再構成できる「認証済み A4 入力」をまだ輸出していない。**　区別すべきなのは、producer object に素材が一部存在することと、それが accepted ordered word-bearing basis として認証されていることの二点である。

- `kernel.K_items` は insertion order の list であり、各 item に literal `word`、normalized `row`、raw `discrepancy`、`exact_raw_affine_replay.actual_delta` がある。したがって literal word 素材と ten-context Fox/affine 素材は存在する。しかし checker はその list が chronological rank-rise basis であること、B を法とする独立性・完全性、parent/action recurrence、queue/action closure を再構成しない。よってその order を v280 (1.3) の **accepted ordered basis** として下流へ渡せない。
- Producer/checker の `direct_row` / `runtime.row` は各 word を ten task232 contexts で実評価し、各 roof が identity であることを要求し、raw affine defect を比較する。この部分は単なる anchor Boolean より強い。ただし output は roof の canonical value を捨てて gradient dict だけを返し、各 item に型付きの `rho0(u_i)` と actual `rho1(u_i)=k_i` の有限群値を別々には輸出しない。`row` は normalized B+K representative、`actual_delta` は `row+Psi(E)` という raw ten-tagged module 値であり、v247 §7 / v280 (1.4) の二つの群評価を識別する receipt field ではない。さらに task176 accepted evaluator/checker は入力認証されず、v4 checker は producer と同じ frozen E4 helper を動的 load する。
- Producer は各 literal word に `h2_signed_word` を適用して exponent `basis_projections` を作るので、候補の `q(k_i)` 計算自体は存在する。しかし各 `D_1` group value は K item ごとに輸出されず、checker は一件も再計算しない。Checker L701--704 は `dynamic_least_nonzero=True`、固定 `d1_z0=[0,0,3]`、`delta0_identity=True`、`delta1_k_membership=True` と non-null dict を読むだけで、`selected_index`、`inverse_scalar`、powered `source_word`、全 `a_i`、`q(k_i)`、`rho0`、`rho1`、K membership を導出しない。
- 従って v280 の consumer は現 receipt から producer の `basis_projections` / selected-anchor Booleans を信頼せずに anchor を **認証付きで**再計算できないし、元 basis から invertible scaling/shear matrix と adapted words を二方向 replay するための前提 basis theoremも持たない。Literal words だけなら再評価の入力にはなるが、それは「accepted A4 package」ではない。

V5 の最小 consumer-facing contract は、(i) exact accepted producer/checker pair と同一 task198/task176 tower/map identities を pin し、(ii) ordered K item ごとに literal word と canonical actual `rho1` 値、complete `rho0` identity 値、actual `D_1` 値を出し、(iii) checker が word から三者を独立再評価して ordered-basis completeness を再構成し、(iv) checker/A5 consumer が全 `a_i`、least `j`、`e=a_j^{-1}`、powered word、anchor 三 endpoint を導出する形である。Anchor fields と adapted basis-change matrix は可読用 derived fields に限り、acceptance を制御してはならない。Adapted basis は consumer が元の認証済み basis に scaling/shear を施し、matrix の両方向と全 `rho0/rho1/q` 値を replay すればよい。

## 6. Resource/performance truth

### 6.1 present-shape work

- Authority raw receipt は 31,017,244 bytes。Raw bytes + parsed object + self-seal canonical bytes が同時に生存する。Actual RSS は UNEXECUTED なので未測定である。
- Producer trie topology は 15,970 edges だが、terminal path replay は 114,458 ten-context steps。Row assembly は 19,408 ten-context tuple multiplications。従って flat replay 前の actual 下限だけで 133,866 tuple steps、reply336 の `15,970+12,967=28,937` ではない。
- 全 row の二重 direct replay は、stored word の 5,475,488 letters に対して正確に

  ```text
  2 * 10 * 5,475,488 = 109,509,760
  ```

  source-letter/context substitution iterations を追加する。さらに frozen `word_substitute` は各 source letter 追加後に growing output 全体を `reduce_word` する。Context 0,5,7 は異なる一文字 generator への置換であり、自由既約 word の長さ `L` が保たれる。よって二重 replay のこの 3 contexts だけで `3*sum L(L+1)` 文字 visit、Cauchy により

  ```text
  sum L^2 >= 5,475,488^2 / 6,441 = 4,654,707,164
  visits >= 13,980,547,956
  ```

  である。これは K/action/anchor より前の不要 Python work の下限である。有界 4h production の意味ある到達性を支持しない。
- 各 query は live pivots 全体の reduction、dual の all-row scan、そして actual CPU として `O_total*ell_q` correlation を直列で行う。Boundary insertion は B-only reduction と insert 内の再 reduction、combined insert を行う。
- Output は `oracle.rounds` に全 dual/accumulator/column を持ち、同じ query dict を actions にも埋める。K item で row、actual delta、representative、Psi(E) を重複させる。Large dual/row/coefficient/transcript の serial duplicate である。
- `write_sealed` は最終 resource/output_bytes を入れる前の encode 長を charge し、その後再 encode する。Final bytes と charged bytes/snapshot が一致しない。Allocation/canonicalization も cap check より先である。
- Checker には wall/RSS/support/serialization の cap 自体がない。Counters だけで `UNKNOWN_RESOURCE` route は存在しない。

### 6.2 checkpoint

Checkpoint は `null`。`Meter.last_replayable_state` は実 checkpoint ではなく、cap の後に復元できない label である。従って数時間後の cap は authority parse、trie、processed rows、B/K、queue、DAG の全てを失う。Missing checkpoint 自体は数学誤りではないが、現行の明示的不要二重 flat scan、未制限 checker、未照合の巨大 transcript と併せると production 実行は許可できない。

## 7. SELFTEST と 48 physical mutations

48 名は producer/checker で同じである。しかし actual owner mutation は **0/48** である。

| names | literal behavior | ruling |
|---|---|---|
| `per_layer_ordinal`, `authority_binding`, `canonical_input_bytes`, `resolved_path_traversal`, `normal_generation_proof`, `bridge_typed_occurrence_ledger`, `evaluator_abi_canary` | miniature cert に `typed_mutations/typed_mutation` flag を追加 | authority bytes/path/row/proof/bridge/ABI は変化せず、reseal も production validator もない |
| `raw_boundary_coefficient`, `live_echelon_inherited_scale`, `producer_checker_basis_change`, `conjugator_order`, `source_word_basis_boundary_difference`, `negative_dual`, `action_matrix`, `projected_h2_exponent`, `k_z_inverse_scalar_powered_word` | 同じ flag + explicit Reject | actual row/echelon/word/action/H2/anchor owner は変化しない |
| `live_resource_cap`, `positive_status_terminal`, `nonpositive_false_progress`, `duplicate_markers` | 同じ flag + explicit Reject | cap は超えず、physical log/envelope/sentinel を変化しない |
| `inconsistent_section_word`, `altered_primitive_terminal`, `wrong_trie_edge_orientation`, `wrong_action_orientation`, `wrong_target_inverse`, `producer_checker_row_mismatch` | 同じ flag + explicit Reject | receipt row/trie state/assembled row を変化しない |
| `missing_base_boundary`, `changed_boundary_block_tag`, `left_right_translation_swap`, `omitted_inverse_action`, `changed_parent_action_ancestry`, `incomplete_queue_claim`, `wrong_support_inversion_product`, `false_zero_correlation` | 同じ flag + explicit Reject | 65 seeds/translation/queue/correlation に到達しない |
| `omitted_candidate_discrepancy`, `omitted_prior_k_discrepancy`, `flipped_q_sign`, `missing_discrepancy_scale`, `reversed_source_action_discrepancy`, `changed_raw_tag_translation`, `modulo_discovered_b_only_replay` | producer は先頭の `omitted_candidate_discrepancy` で存在しない `kernel` を参照し hard stop。checker は miniature `K_items[0]` の shaped fieldのみ | producer で全 7 未到達、checker も actual discrepancy validator ではない |
| `deleted_active_key`, `unregistered_dual_key`, `raw_pivot_functional`, `omitted_matching_occurrence`, `incomplete_translation_key`, `premature_zero_correlation`, `omitted_new_key_registration` | producer は先行 hard stop のため全 7 未到達。checker は shaped dual dict のフィールドのみ | actual active registry/projection/occurrence/translation/new-key owner ではない |

`mutation_owner_reject` / `reject_typed_mutation` は mutated condition が真であることを見た後に無条件に `raise Reject(...mutation_rejected)` する。これは「名付けた owner が mutant を拒否した」証拠ではない。SELFTEST の positive も actual authority/affine/trie/basis/ledger/DAG/anchor ではなく、期待値を入れた miniature record である。

## 8. V272--v274 実装境界と最小 v5 修理

### 8.1 genuine implementation

- Actual ten-context affine/Fox arithmetic。
- 65 tagged literal base relations。
- Producer の finite active support union、projection back-substitution dual、full `t=g*h^-1` correlation、strict lazy B insertion。
- Producer の chronological full-D NONMEMBER 受理の数学的意図。
- V273 の raw discrepancy grammarと exact `E_new` / `W_new` recurrence。
- Producer の dynamic H2 least-index/scalar/word 構成。

### 8.2 shaped / incomplete declarations

- Full task198 inner-seal/bridge/ABI replay、task176 authority/canary、physical source binding。
- Advertised prefix/suffix performance path。Producer は long words を二重 rescan し、checker suffix trie は未使用。
- Checker の 6,441 row equality、chronological B/K、MEMBER/NONMEMBER、dual/correlation、rank-rise、word recurrence、queue/action、anchor replay、および v280 consumer 用の ordered-basis / per-item `rho0/rho1/q` 認証。
- `all_row_dots`, `complete_all_65`, `full_D_all_65`, `bounded_expansion`, action-matrix completeness、SELFTEST mutation の Booleans。
- Resource caps、final sealed accounting、replayable checkpoint、bounded production feasibility。

### 8.3 smallest versioned v5 repair

1. Actual canary roster のみ要求し、`y^-1` は receipt field ではなく actual actor inverse/direct inverse-word law として比較する。Task176 accepted receipt/manifest/checker と task198 三 physical sources を両側/driver で pin する。Rows/chunks/bridge/ABI digests を literal owners から再計算する。
2. Action row の単字は primitive trie ではなく 40 actor cache から与える。Producer trie は persistent edge delta を一回ずつ使い、flat replay を六 fixed rows + actors/primitives/new K/anchor だけに限る。全 6,441 の二重 direct replay を削除する。
3. Checker に helper-nonshared right-associated affine suffix evaluator を実装し、全 6,441 rows を実際に構成する。Producer の initial row 全体をコピーせず照合できる streamed digest/coefficient certificate を設計する。
4. Action NONMEMBER/rank-rise に対し、new normalized K row を含む完全な matrix column をその場で作る。MEMBER round と dual round の schema を分け、checker が両方を再構成する。
5. Checker は producer chronological raw B/K roster を独立 max-pivot で再構成し、各 active registry、dual、65-family correlation、selected column、rank rise、MEMBER coefficient、zero accumulator を再計算する。Max-pivot dual は projection operations の逆順に修正する。Occurrence を `(context,component)` で index し、実 CPU と meter を同じ `P_q` にする。
6. Persistent/memoized word+ledger DAG を用い、展開前 cap、一回の `Psi(E)`、independent `Q,c,s,parent/action` replay を入れる。`O(t^2)` pairwise full-word replay は有界 canary に置き換える。Checker は ordered K item ごとの canonical actual `rho0/rho1/q` 値を literal word から再計算して basis 完全性を認証し、全 H2 projection、least index、scalar、powered word、三 endpoint を Boolean-free に導出する。V280 の A5 consumer はこの accepted basis から scaling/shear matrix と adapted words を局所構成し、basis change の両方向を replay する。
7. 48 mutations は physical owner を変え、必要な場合は reseal し、actual production validator に投入する。Hash/flag/explicit Reject は廃止する。Normal SELFTEST は production classes と同じ owner を実行する。
8. Driver は nonpositive producer receipt も sealed typed object として checker に渡し、reason を含む canonical terminal payload を比較する。Atomic writes、exact output basenames、v1--v5 全 owned stale files、checker caps/RSS を入れる。
9. Production に進む前に、authority identity、next query ordinal、raw B/K、echelon rebuild、queue head、word/ledger DAG、counters を持つ実 checkpoint を置く。Transcript は一回だけ保存し、dual/accumulator/row の重複 serial copy を除く。

この v5 の静的 Sol(max) 再監査と actual-owner SELFTEST PASS の前に、合成 SELFTEST も production も実行してはならない。

AUDIT: REJECT
EXECUTION: UNEXECUTED
SYNTHETIC SELFTEST AUTHORIZED: NO
A4 INPUT AUTHORITY: 1/3
A4 INVARIANT CLOSURE: 0/1
A4 WORD-BEARING K + ANCHOR: 0/1
ACTUAL A4: 1/3
LIFT / FAKE / IHARA: NONE

`TASK343_R07_TASK336_A4_V4_CODE_PERFORMANCE_AUDIT`
