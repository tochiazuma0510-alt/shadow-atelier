# Sol(max) reply 352 — task351 A0/v10 code / soundness / performance audit

判定は **REJECT / UNEXECUTED** である。指定された順序で全資料と pinned owner を読み、候補は一切実行せず、Python / Node / GAP / GHA / workflow / git / network も使わなかった。以下の「仮想修理」は後続経路を静的に追うためだけの仮定であり、v10 の変更や実行を許可しない。

## 1. Frozen candidate and prerequisite order

### 1.1 物理 identity

指定された六 owner は read-only 再計算と一致した。

| owner | bytes | SHA-256 | 判定 |
|---|---:|---|---|
| recovery-v2 | 2,690 | `67dd555f6e0f943d0161ef2f2c8124b4cc31c9167846b45b43fd2001f5fbba3f` | PASS |
| producer v10 | 147,892 | `235a798e097a7388603a72462a4fef28d9a7e044c47e4339eb4e30714bd9e472` | PASS |
| checker v10 | 131,175 | `b2723e9d6703f3cf529ffab7c571ce5dce8b23a428eb54810f57b05aba4a5b0f` | PASS |
| driver v10 | 12,812 | `51ce34e7908af9c6a489c76607a95a2c9b55142e04a9d19aaa1154177b06cba3` | PASS |
| fixture v10 | 3,785 | `de6273d681238b1aa560353c70a245cc28823326908e31be464fa2c399917203` | PASS |
| reply351 | 4,721 | `245ef2c07cabad4ea598e457e2748b6884272d9a9494702adaa469526e976169` | PASS |

Producer/checker に列挙された 26 個の `SOURCE_PINS` も全て path / bytes / SHA が一致した。26 owner の総量は 17,639,182 bytes である。driver の ZIP は 5,001,811 bytes / `f3ac82a0...f566`、sole member は 86,368,039 bytes / `c261aa96...0ab` であり、manifest と一致する。

### 1.2 raw checkpoint の self seal — 先行観察の訂正

ここは LF convention を区別すると **PASS** である。ZIP member は canonical JSON 一行の末尾に LF を一つ持つ。`"self_digest":"<64hex>",` は全 document に一度だけ現れる。

- seal property を除き **末尾 LF を残した物理文字列**: 86,367,958 bytes、`f438ce78e7b76d252cbdc096b7c53deebbbc2dffd3c7e7f7a392337255bb43da`。
- `live.validate_seal` が実際に行う JSON parse → key-sort / compact ASCII canonicalization、すなわち JSON 外の末尾 LF を含まない body: 86,367,957 bytes、`29bb74f3bd8048913a0365bc4c599f3731d32ba56967f3a238c7468b7fcfd123`。

後者が raw の claimed seal と一致する。したがって raw owner の reseal、上書き、adapter は不要かつ禁止である。前者を self body と扱った先行観察は撤回する。再現手順は次の read-only PowerShell と同値である（`$s` は sole ZIP member の ASCII text）。

```powershell
$pat = '"self_digest":"[0-9a-f]{64}",'
if ([regex]::Matches($s,$pat).Count -ne 1) { throw 'seal occurrence' }
$physicalMinusProperty = [regex]::Replace($s,$pat,'',1)
if (-not $physicalMinusProperty.EndsWith("`n") -or
    $physicalMinusProperty.EndsWith("`n`n")) { throw 'exactly one terminal LF' }
$canonicalBody = $physicalMinusProperty.Substring(0,$physicalMinusProperty.Length - 1)
$bytes = [Text.Encoding]::ASCII.GetBytes($canonicalBody)
# bytes = 86367957; SHA-256 = 29bb74f3...0fd123
```

raw の固定統計も読取結果と一致する: rank / columns / boundary columns は全て 2,896、raw support 合計 20,354（最大 12）、ancestry 合計 137,926（最大 258）、target support 3,944、stored remainder support 5,315、stored solution support 625、current dual support 1,188、monitor の boundary pairs 3,145,728、progress pair attempts 3,145,088 である。

### 1.3 task176 authority

Accepted receipt は 13,649,089 bytes / `715441d8...7f41`。top-level `self_digest_sha256` を除いた canonical body は 13,649,000 bytes / `f8f0ce249ff547d3e1235bd4b9760daa2b34b23771bf7da47b48dbd5cbbfae1d` で一致する。recovery-v2 canonical body は 2,601 bytes / `e95b4e7781a14cffd07d445141f20c942861168d201f2ce62879a0ddf3a45026` で一致する。

v2 は v1 の physical owner 2,035 bytes / `41d2cb72...90a8` / self `f8c6c0fa...f581` を `supersedes` で保持し、`/accepted_receipt/self_digest_sha256` の `...b34f...` を `...b34b...` に訂正する。上書きも黙認もなく、`execution=UNEXECUTED`、`mathematical_grade_change=false` である。receipt manifest、recovered verdict、run `33044121344`、head `0533e420...836`、artifact `9635036013`、archive `250e25c9...9912`、三 member 名、producer/checker source、task176 reply の v2 記載も physical資料と一致した。

Decoded owner の固定値は Q0 = 1,469,664、Gamma = 243、Delta = 357,128,352、Q0 roster 52,907,904 bytes、parents 5,878,656 bytes、letters 1,469,664 bytes、Gamma states 235,710 bytes、parents 486 bytes、records 243 bytes である。ten coordinate widths は `5*40+5*154=970`。projection kernel orders は `[9,9,9,9,9,1,1,1,3,3]` である。

## 2. Literal driver and terminal reachability

### 2.1 driver trace

driver は全 pin を `StringFile` で読み、`ci/out` の prefix stale scan と十 owner の exact stale checkを行う。その後 sole ZIP member を temporary regular output に展開し、raw bytes/SHA を照合して `os.replace` と file/directory fsync を行う。producer log の prefix は一行だけに限定され、checker terminal と byte-exact `cmp` され、case gate を通った後だけ sentinel を最後に書く。この terminal / sentinel 部分は概ね fail-closed である。

ただし外側の `timeout` は一つもない。producer の内部 10,800 秒だけで、checker 7,200 秒、artifact 3,600 秒、全体 21,600 秒の分解は driver に実装されていない。また shell の mode は `SELFTEST` 以外を全て production に丸める。

### 2.2 FIRST LITERAL STOP — SELFTEST

委嘱後に最初に許可され得る SELFTEST 経路の最初の決定的停止は producer の実 baseline である。

`_triangular_subset_frame` は raw の先頭六列を取るが、`_validate_triangular_subset` は六 pivot 全体を `pivot_set` に入れてから、各 P row が自分以外の **future pivot** も含まないことを `search/...v10.py:2290-2291` で要求する。これは production の正しい `seen_pivots`（earlier only）条件より強い。frozen owner では column 5 の ancestry は正確に `[[5,2]]`、その P5 support は 8 で、column-6 pivot を coefficient 2 で含む。従って baseline は `triangular selftest P equation` で止まり、mutation/process/SELFTEST receipt に到達しない（呼出しは lines 2312, 2520）。

これを「仮想修理 H1: selftest も chronological `seen_pivots` のみ禁止」とした後も、最初の triangular mutation が `_physical_mutation` を通ると `read_bounded_json` line 2120 の未定義変数 `meter` で `NameError` となる（H2 が必要）。さらに H1/H2 後に producer が SELFTEST receipt を作れても、checker `validate_selftest_envelope` lines 2046-2047 は旧 fixture 2,784 bytes / `a96d7e...e641` を要求し、現行 3,785 bytes / `de6273...7203` で必ず停止する（H3）。

### 2.3 default / fresh production

driver default は production だが、既定の `ci/in/d972_r07_history_free_positive_fast_resume_selftest_v10.accepted.json` は frozen tree に存在しない。producer は全 source 読取、86 MB parse、light build、2,896 列 triangular build を済ませた後に `UNKNOWN_INPUT:selftest_identity_missing` を出し、driver line 156 の `test -s "$selftest_receipt"` が checker より前に失敗する。これは SELFTEST first stop と別の physical availability stop である。

仮にその file を置いても authority は不十分である。driver は path/bytes/SHA を pin せず、producer は自己 seal、schema、terminal、fixture SHA、false claims だけを見る。status、full selftest ledger、producer/checker verdict/identity を見ないため、第三者が self-reseal した小さな JSON を production prerequisite にできる。

さらに production は `require_selftest_identity` の返す summary を捨て、`Search(..., None)`（lines 2764-2766）を構築する。COMMON receipt の `selftest` は必ず `None` となり、checker `validate_common` line 1759 → `validate_selftest` の dict 要求で必ず止まる。

最初の correction hit には別の producer hard stop もある。`runtime["gamma"].states[gid-1]` は `(E3_element, tuple(31 E4 elements))` という full JointGroup state だが、`bind_section_identity` lines 1843-1847 はこれを単一 quotient element `(permutation, pc_bytes)` 専用の task176 `packed_joint_blob` に渡す。後者は task176 lines 283-301 で type error にする。970-byte projected ten-state と full JointGroup diagnostic の型が混同されている。

### 2.4 resume / UNKNOWN / hard exception

- resume preflight は main の try より前に `read_bounded_json` を呼ぶため、line 2120 の `meter` `NameError` は typed UNKNOWN にもならない。
- H2 後も parsed DAG literal node は `['literal', [[symbol,coef],...]]` であるのに、producer lines 263-264 と checker lines 134-136 は outer だけ `tuple(raw)` にして set に入れる。inner list が unhashable なので全 nontrivial sidecarで `TypeError`。producer lines 2196-2198 の `nodes` / `intern` 復元も同じ欠陥を持つ。
- portable manifest は自身が external pin を持たず、任意に self-consistent な checkpoint bytes/SHA を指定できる。復元した new row の ordinary boundary/correction provenance、active dual、scalar を replay せず、hash/self-seal された carrier を実行履歴 authority として扱う。
- `UNKNOWN_INPUT` は sidecar を禁じる点は正しいが、`missing:<path>` 等 `/` を含む producer reason は checker `safe_terminal` と driver regex に通らない。
- `UNKNOWN_RESOURCE` checkpoint validator line 1955 の `checkpoint.get("heavy_reconstructible") is bool` は value を type object と比較しており常に false。prepool sidecar は当該 field 自体も欠く。この route は H2/DAG 修理後にも拒否される。
- hard exception は producer/checker terminal を残さず driver を止めるので false PASS にはならない。ただし上記 NameError/TypeError は意図した typed failure truth を壊す。

COMMON 成立時に `Search.run` は candidate を返す前、最終 receipt の atomic write より先に checkpoint を unlink する（lines 2058-2064）。この crash window は v276 の durability 条件に反する。

### 2.5 route別の最初の停止点

| route | frozen tree の earliest result | その点だけを仮想修理した後 |
|---|---|---|
| prerequisite / baseline | 六 identity、26 source pin、raw/recovery-v2/task176 seal は全て PASS。ここに停止はない | SELFTESTへ進む |
| SELFTEST | producer lines 2290-2312、P5 が future P6 pivot を含むため誤拒否 | H1後は line 2120 `meter` NameError、H2後は checker lines 2046-2047 の旧 fixture pin |
| default fresh PRODUCTION | accepted SELFTEST input が物理的に無く、producerは UNKNOWN_INPUT、driver line 156 が checker前に停止 | accepted ownerをversioned pinして与えても、correction hitでは JointGroup/single-quotient codec型違反。そこを直してCOMMONまで行けば `Search(..., None)` によりcheckerが selftestを拒否 |
| authenticated restore | producer main tryより前の line 2120 `meter` NameError | H2後は literal DAG inner-list unhashable `TypeError`。さらに直しても manifest/provenance authority と v290 accounting が失格 |
| nonpositive UNKNOWN_INPUT | default routeでは上記 missing accepted input後にdriverが停止。一般の `missing:<path>` reasonは checker/driver safe-terminal grammarにも不適合 | reason grammarを直しても accepted inputを権威化しない限りproduction認可にはならない |
| nonpositive UNKNOWN_RESOURCE | H2/DAG修理を仮定した最初の literal blockerは line 1955 の `value is bool` と prepool ownerの field欠落 | transportを直しても4 GB DOM、untrusted carrier、restore semantic gapが残る |
| performance | checker selected-K0ごとのE4 inverseが一回約650 MiB級、outer wall/RSS capなし | exact open-address cache/full-key equalityと全体deadlineが必要。§9の重複全量workも同時に除く |

## 3. Recovery-v2 and physical authority

Producer `SourceRegistry` と checker `Sources` / `open_physical` は Linux では `O_NOFOLLOW`、regular、link count 1、固定/上限長、opened-fd before/after `(dev,ino,size,mtime,nlink)`、pathname-after identity、SHA を照合する。task176 zlib owner は strict base64、compressed/raw digest、`raw_limit+1`、EOF、unused/unconsumed tail を照合する。raw ZIP も sole name / raw size / raw digest で bounded である。

弱点は次の通りである。

- driver の ZIP 自体は GAP pin と Python open の間に同一 handle を保持しない。ただし extracted raw SHA が固定なので数学的 bytes の置換は防いでいる。ZIP/output directory の no-follow / directory identity は記録しない。
- `O_NOFOLLOW` が無い platform では 0 に fallback する。pathname identity は多くの置換を捕えるが、driver は bash、producer は Linux fork を必須とし、Windows route は実質存在しない。
- v10 checker は recovery-v1/v2、accepted receipt、recovered verdict の canonical self seal を再計算せず、field と outer pin を比較するだけである。frozen bytes には十分だが、ordinary semantic validator / mutation gate にはなっていない。
- recovery-v2 が列挙する task176 checker 84,980 bytes / `4e6b97...695`、task176 reply 47,164 bytes / `aa1731...0c`、hashes file、archive owner は v10 `SOURCE_PINS` に無い。v2 の run/head/artifact/archive/hash-file/task176-reply fields も `validate_task176_authority` で照合されない。

module load/call graph は次の通りで、checker が task176 source composite を呼ばない点は PASS である。

| owner | producer | checker |
|---|---|---|
| `live` | exec。row/sparse arithmetic、target、`AllSevenModel`、boundary、`FibreOracle` 等を call | bytes auth only、exec/call なし |
| task176 source | exec。packing、deletion、Q0 enumeration、membership、A/L/kernel、coordinate evaluator 等を call | bytes auth only、**exec/call なし** |
| `old` E3/E4 | exec。quotient/context/Fox/PB relation primitivesを call | exec。同じ低位 arithmetic を call |
| `joint` | exec。`JointGroup` | exec。`JointGroup`, `complete_relators`, `materialize_tokens` が v172 経由で到達 |
| `v172` | exec。`build_roster` | exec。`build_roster` |
| `g760` | exec。self-contained `construct_base` | 同左 |
| `pb4` | exec。self-contained `base_raw_columns` | 同左 |
| task175 / old_bridge | auth only | auth only |
| q3 / joint receipt | 両方 parse | q3 のみ parse、joint receipt は auth only |
| docs / manifest / recovery owners | auth、manifest/v2等必要分 parse | auth、task176 authority必要分 parse |

呼ばれる関数経路から追加の repository-local dynamic import は無い。各 predecessor の `main` 内 loader は到達しない。Producer は task176 private/composite API に強く依存するが producer側なので禁止違反ではない。checker側の packing/value/Q0/Gamma/fibre/kernel は local 実装である。

## 4. Exact selected Q0 and Gamma semantics

全 parent owner の静的 grammar は正しい。Q0 は 1,469,664 records、qid 1 が唯一の `(0,0)` root、他は `0<parent<qid` と letter 1/2。Gamma は 243 records、gid 1 が唯一の `(0,0)` root、他は earlier nonzero parent と record 1..26、walk は `record-1` を使う。両 walk とも leaf-to-root chunks を reverse して literal root-to-leaf word にする。

しかし COMMON checker は selected replay に到達する前に止まる。

1. physical q3 `marked_permutations` は各 row が **1..36** である。checker lines 386-392 は誤って `set(range(36))`、すなわち 0..35 を要求し、そのまま `bytes(row)` にするので frozen owner で必ず `q3 Q0 marked permutation owner` STOP。producer/task176 は正しく `old.perm_from_row(...,36)` で 1 を引く。
2. これを仮想修理しても `q0_perm_mul(left,right)` lines 467-472 は `left[right[i]]` である。frozen old primitive lines 635-637 と task176 recurrence line 796 は `right[left[i]]`（`state.translate(right_table)`）である。二文字目以降の非可換 word で 36-byte roster replay の向きが反転する。

従って v11 は「q3 literal grammar 1..36」→「明示的 `x-1` conversion」→「`right∘left` recurrence」を別々に gate しなければならない。

その二点の後では、checker は selected Q0 parent word、36-byte roster slice、十個の 40/154-byte marked-generator owner、十 coordinate Q0 values、selected Gamma parent word、970-byte projected recordを local E3/E4 model で比較する。`base_word=red(gword+qword)` の順序、K-nonzero で同じ object を delta に使うこと、K-zero で `red(kernel+gword+qword)` を使うことも明示されており、この部分は sound である。

一方 `gamma_full_state_hex` は checker lines 1414-1418 で「hex とその自己 SHA」でしかなく、full JointGroup state を独立再構成しない。producer は前節の type errorを持つ。970-byte projected owner と full diagnostic を代用してはならず、diagnostic なら acceptance から外すべきである。

## 5. Exact K-nonzero and K-zero schedules

### 5.1 K nonzero

仮想的に前節を修理すれば、この schedule の数学は実装されている。checker は eleven-occurrence formula から `K`、merged distinct targets、kernel orders、`W` を再構成し、`bound=W+1`（`W<Delta`）または全 Delta fallback を要求する。`qid=c//243+1, gid=c%243+1` は `0<=c<1,469,664*243` の bijection で、selected `gword+qword`、ten-coordinate product、formula scalar、direct column、active-dual pairingを再計算する。各 target fibre の大きさの和が高々 W なので W+1 個の相異なる Delta 元の一つは support 外にあり、nonzero K を保つ、という pigeonhole 仮説と実装は一致する。copied boundだけを信じてはいない。

### 5.2 K zero

Producer の live `CoarseInverse` は `array('I')` open addressing、coarse full-key collision probe、lookup後の **full 40/154-byte** `section[coordinate] == section_target` を行う。この producer側 primitive は sound である。checkerの独立経路は次の理由で REJECT する。

1. chronological one-coordinate recurrenceと coarse duplicate rejection、全 pair digest は再計算するが、task176 accepted singleton-bucket count/digest metadata 自体とは結ばない。
2. `first_gamma` は gid 1..243 の first value を作るが、authenticated `A_families[Sj].literal_elements` とは key の set だけを比較する（lines 1299-1305）。各 `gamma_state_id`、sorted table、`literal_table_sha256` を比較しない。
3. 最重要: coarse lookup後、lines 1311-1318 は `source=a^-1*t` を作るが、retained `states[(qid-1)*width:qid*width] == source` を要求しない。続く `a*source=t` は定義上の tautology で、source の Q0 membership proof ではない。coarse collision / same permutation with different PC component を誤受理できる。不一致 gamma は candidate にせず **skip** すべきである。
4. producer は `qid is None` を skip するが checker は全 gamma value に `qid is not None` を要求する。leastness proof は見つかった exact full-state candidateだけを列挙すべきである。
5. S5/S6/S7 の authenticated word generators は 0 個、kernel order は 1 である。checker は `require(generators and ...)` とするため、これらの正しい trivial kernel を拒否する。
6. BFS は full ten-coordinate states と word を再構成するが、receipt に canonical kernel state blobs ownerを持たず、cursor/state word/kernel wordだけを比較する。producer `kernel_cursor` は selected word が無い時に candidate の default値へ silent fallback する（lines 1810-1812）。hard stop が必要である。
7. 最後の target、formula scalar、eleven/direct H1/H2/P、dual pairingの replay はあるが、上記 membership gap の後なので load-bearing K0 certificate にはならない。

従って v287 §6 の full-state condition は未実装である。

## 6. Triangular solver, ancestry, and final COMMON

Production triangular builder は全 2,896 raw rows を canonical parseし、各 ancestry の strictly increasing indices、future index なし、nonzero diagonal、unique/correct pivotを調べる。P=A*C の weighted raw support contribution は 1,011,460、P support inspection は正確に 289,774、各 P は coefficient-one pivot、`min(P)=pivot`、全 earlier pivots zero である。P digest `3c645f...9d28`、target `968f0b...0d82`、initial dual support 1,188 / `096025...0f0c` と一致する。初期 target reduction の nonzero pivot hit は 226、remainder support は 5,315 であり、初期 DAG recursion は default recursion limitを越えない。SELFTESTだけが future pivot を誤って拒む。

`FormalReducer` は actual row を active dual と direct rowから rank-one追加し、coefficient 2 の inverse word/direct rowも producer/checker双方で再計算する。COMMON checker は formal solution の全 symbolを selected old/new record と一対一にし、old record は authenticated raw owner の literal recordと完全一致させ、新 boundary/correction は direct provenanceを再生する。selected rows の literal F3 sum が target に一致し、boundary/correction decomposition、correction product、各 selected joint-kernel factor、exponent gate、corrected word、eleven/direct all-seven、final residual zeroを独立に導く。

従って未選択 row が探索 dualや pivotを変えても、最終 acceptance を偽造することはできない。これは v278 の「selected supportのみ load-bearing」と整合する。ただし checkpoint の実行履歴 truth は別問題であり §7 のとおり失格である。

最後の `heavy_input_sha256` は correction があっても checker が 64-hex shapeしか確認しない。opened authority tuple、Q0/Gamma owners、selected full-state fibre、kernel、code identitiesから独立に導出しないため heavy identity gate は FAIL である。producerの `heavy_public` digestや Boolean は authority にならない。

## 7. Checkpoint, DAG, process, and failure truth

Checkpoint/resume は REJECT である。独立した欠陥は次の通り。

- `read_bounded_json` の未定義 `meter`、JSON literal DAG の unhashable normalization、untrusted portable manifestは §2 の通り。
- resume preflight は sidecar全体を一度 parseして捨て、`restore_checkpoint` でもう一度 open/read/parseする。最大 4,000,000,000-byte ownerを二重処理し、stale output check よりも前に行う。
- restore は new row の sparse shape/pivot/DAG idを注入するが、ordinary boundary/correction provenance、active dual、pairing、rank fields、実 process epochを replayしない。semantic rebuild canaryも無い。
- `checkpoint_body` は heavy build後も常に `heavy_complete:false` とし、`heavy_reconstructible` だけで済ませる。completed heavy provenance/cacheを sidecarに保持せず、resume は Q0/stores/membership/kernel全体を再構築する。expected heavy digest比較はあるが、既完了 work と materialization frontier の型が虚偽である。
- current producer meter は resume前に実施した source authentication、raw parse、light/triangular rebuildの countersを、checkpointの historical countersで上書きする。v290 が要求する `completed semantic += historical`、非zero `restore_validation`、fresh invocation input/wall、peak/gauge lawの分離がない。`sparse_operations` counter は宣言されるだけで一度も bump されない。
- checkpoint作成ごとに target reductionを行い、その後 `exact_dual` 内でも再度 reductionする。last serialization charge、semantic cumulative、gaugesが型分離されていない。
- `AncestryDAG.expand` は memo保存時とmemo hitごとに sparse dictをcopyする。現初期 chainは有限だが、後続 actual DAGの深さに recursion capがなく、support合計に対して二次的 copyとなり得る。cap は expansion完了後にしか検査されない。
- checkpoint delete-before-final-write の crash windowがある。

Process owner の disjoint intervals、absolute socket deadline、epoch all-or-discard、timeout/death/partial時の terminate→join→kill→close、Linux fork限定、PRODUCTIONで fault injectionしない点はよい。しかし:

- light ownerを heavy transitionで一度閉じ、heavy 1.4 GB超 runtimeを構築した後に再forkする。workersはboundary light dataしか使わないのに、W=4なら全 heavy pagesが各 child RSSに現れ、meterの「parent RSS + child RSS sum」はCOW shared pageも重複加算する。5.7 GB capに対し極めて不利である。
- owner置換で heavy前の boundary accountingを捨て、`process_restarts`、committed epochs、IPC累計が final ownerに加算されない。STOP送信 bytes も `frames_sent_bytes` に入らない。
- parent は全 pair streamを作ってからW sliceを作り、ACTIVE時には同じ matching descriptorsを再走査して contributorsを復元する。
- SELFTEST timeout/blocked-send は deadlineまでbusy loopする。fault専用とはいえ不要なCPU workである。

## 8. Checker independence and physical mutations

COMMON の selected boundary/correction、target、Q0/Gamma、formula/direct row、coefficient-two inverse、correction product、joint-kernel、eleven/all-seven、residualを producer helperなしで再計算する設計は良い。しかし q3/Q0、K0 full-state、heavy identity、selftest binding の欠陥により checker independence 全体は FAIL である。UNKNOWN は数学をbuildしない点は正しいが、source transportは `hash_source=False` で path envelopeしか見ず、resource sidecarは最大4 GBをDOM化する。

Fixture mutation は「全て ordinary live ownerへ到達」の条件を満たさない。

- `future_ancestry_index`, `zero_diagonal`, `changed_raw_sparse_entry`, `changed_ancestry_coefficient`, `duplicate_pivot`, `wrong_pivot`, `hidden_smaller_pivot`, `skipped_P_equation`: six-column temporary ownerを変える実コードはあるが、baselineがH1で自壊し、H1後もH2 NameErrorで validator に到達しない。full 2,896-ownerでもない。
- `empty_support`, `one_support`, `short_support`, `typed_present_shape_filter`, `f3_cancellation`, `active`, `zero`, `three_serial_duals`, `deadline_timeout`, `blocked_pipe`, `worker_death`, `partial_result`, `bounded_cleanup`: producer は関連probe/faultの一部を実 ownerで行うが fixture の `process_cases` roster自体を読みも照合もしない。mutationごとの physical owner / narrow first rejection ledgerではない。
- `heavy_call_before_heavy_digest`, `fabricated_heavy_digest`, `stale_correction_progress`, `zero_promoted_to_negative`: miniature dict validatorだけである。`light_resource_checkpoint`, `heavy_transition` は `owner_gate:true` という ledgerのみ。
- boundary 13件 `wrong_typed_support`, `missing_interval`, `overlapping_interval`, `wrong_t_orientation`, `changed_accumulator`, `changed_winner`, `changed_scalar`, `cross_epoch_frame`, `blocked_send`, `partial_worker`, `dead_worker`, `surviving_process`, `counter_reset`: producerは名前をcheckerへcopyするだけ。checker側 physical mutation関数は定義されるが mainから呼ばれない。
- selected correction 30件 `selected_q0_roster_state`, `selected_q0_parent`, `selected_q0_letter`, `selected_marked_generator`, `selected_gamma_state`, `selected_gamma_parent`, `selected_gamma_record`, `selected_qid`, `selected_gid`, `selected_cursor_quotient`, `selected_cursor_remainder`, `selected_schedule_kind`, `selected_k0_fibre_nonleast`, `selected_kernel_order`, `selected_heavy_input_identity`, `selected_section_word`, `selected_coefficient_two_inverse_word`, `recovery_v1_substitution`, `recovery_v2_corrected_field`, `recovery_v2_self_seal`, `q0_parent_letter_roster`, `q3_marked_permutation`, `one_coordinate_mark`, `gamma_parent_record_word`, `gamma_projected_970_byte_state`, `gamma_full_vs_projected_substitution`, `k0_coarse_key_full_blob_least_base`, `kernel_generator_order_cursor_word`, `product_order`, `heavy_identity_final_row`: producer/checkerのどちらも fixture fieldを参照せず、owner変更、ordinary validator、rejectionは全て **NONE**。
- positive 7件 `omitted_selected_row`, `changed_selected_row`, `changed_selected_coefficient`, `wrong_coefficient_two_word`, `copied_sparse_equality_boolean`, `changed_target`, `changed_boundary_preimage` と physical 11件 `symlink_candidate`, `hardlink_candidate`, `toctou_substitution`, `unbound_checkpoint`, `positive_claim_on_resource_exit`, `separator_flip`, `cofinal_flip`, `fake_flip`, `ihara_flip`, `terminal_reseal`, `stale_output`:同様に producerは名前だけ。checkerの `run_common_mutations` / `run_unknown_transport_mutations` は dead codeである。

実際の verdict は全 route で `mutations.executed:false` を発行する。baseline reachabilityも無く、resealされたauthorityを ordinary gateで拒む suiteも無い。PHYSICAL MUTATIONS は REJECT である。

## 9. Mandatory unnecessary-work and feasibility audit

以下は実測時間ではなく、literal codeから得た個数/上限である。

### 9.1 large owner / module work

| work | literal count |
|---|---:|
| producer eager source read/hash | 26 owners、17,639,182 bytes |
| checker COMMON/SELFTEST eager source read/hash | 上記26 + producer、27 owners、17,787,074 bytes |
| producer compiled modules | 7、合計 1,292,967 source bytes |
| checker compiled modules | 5、合計 1,102,988 source bytes |
| compiled roster identity replay | 6,441 full JointGroup wordsをproducerとcheckerで各一回、合計12,882 |

13,649,089-byte task176 receiptは driver pin、producer eager registry、checker eager registryで各一回読む。producerとSELFTEST checkerは内容を使わないのに保持する。COMMON checkerはさらにJSON parseし、six compressed ownersから合計 60,492,663 raw bytesを展開しつつ、元raw、DOM中のbase64 strings、encoded bytes、compressed bytes、re-encoded canonical base64を同時期に持つ。

86,368,039-byte old sourceは driverが一回展開/書込し、producerが一回 read/hash、bytearray→bytes copy、decode/parseし、sealのため約86.37 MBを一回 canonicalizeする。COMMON checkerは一回 read/hash/parseした `_source_value` を保持したまま、同じ `source_raw` を `validate_common` で再び decode/parseする。従って pipeline全体で raw JSON parseは producer一回 + checker二回、checker内では二つの巨大DOMと86 MB bytesが同居する。selected old recordを得るためだけの二重DOMは不要である。

### 9.2 triangular / target / DAG

- raw support 20,354、ancestry entries 137,926、weighted raw additions 1,011,460、P support inspection 289,774 は必要な exact prefixである。
- `exact_dual` の初回は2,896 pivot scan、286,878 nonpivot row terms、さらに annihilation gateで `2,896*1,188 = 3,440,448` dict lookupsを行う。各 search/checkpointで target reductionを重複して呼ぶ。
- checkpointごとに P public 289,774 entries、全DAG、全new records、dual/remainderをmaterializeする。normal write一回につき少なくとも size-estimate二巡、body seal canonicalization一巡、final JSON canonicalization一巡に加え、P/formal/current-dual digestの全巡がある。new record全履歴を毎回含むので累積I/Oはrank rise数に対して二次的になり得る。
- `expand` は各DAG nodeで growing sparse dictをcopyし、共有nodeのmemo hitでもcopyする。iterative reference-counted expansionへ置換できる。

### 9.3 process / IPC

Meter上限は boundary pairs 8,000,000、first epochは正確に 4,752 pairs。各E4 pairは154-byte valueをhex化してframeに載せるため、8M上限は数GB級の累積JSON IPCになり得る一方、一 worker frame capは32 MiBで先にUNKNOWNとなり得る。parentは support private、全 `pair_stream` rows、slice lists、canonical frame bytesを同時に持つ。ACTIVEごとの contributor再走査も同じpair集合を二度処理する。

fresh light + heavy transitionでは W + W、最大8 process creations、各resumeでも同様に最大2Wを作る。heavy後forkとCOW重複RSS accounting、owner置換による累計喪失は §7 の通りで、正しいが不必要に遅い/大きい。

### 9.4 producer Q0-heavy work

十 storeのraw payloadだけで `1,469,664*970 = 1,425,574,080` bytes (約1.328 GiB)。さらに Q0 roster 52,907,904 bytes、letters、Python `parents:list[int]`、`qstates:list[bytes]`、`qids:dict[bytes,int]`、P rows、86 MB DOM、registry rawを同居させる。

Q0 BFS は 2N = 2,939,328 edgesを走る。新 state edgeは N-1 だけで、duplicate edgeは N+1 = 1,469,665。コードは `prior=ids.get(nxt)` を既に知った後も全十 coordinate `new_blobs` を計算するため、**14,696,650 coordinate group products** が保存にも検査にも使われない。membership scanは N state-major 970-byte rowsを一回copyし、11 family map checks = 16,166,304、transient bytes objectsは10N = 14,696,640個。全 L orderが1なのに `prove_L` は各11 familyで全bitsetを二巡し、合計 32,332,608 bit checksを行う。同一bitset/digestのproofを共有できる。最後の十 store digestはさらに1,425,574,080 bytesを走査する。

### 9.5 checker K0 — load-bearing performance failure

`reconstruct_k0_selected_fibre` は **selected K0 recordごと** に coordinate inverseを作り直し、coordinate cacheを持たない。

- E3 raw state store: `1,469,664*40 = 58,786,560` bytes。
- E4 raw state store: `1,469,664*154 = 226,328,256` bytes。
- E4 dict key payloadだけで `1,469,664*144 = 211,631,616` bytes。一般的な64-bit CPythonでは144-byte `bytes` objectは概ね184 bytes、qid `int` は概ね28 bytesなので、keys+valuesだけで約311,568,768 bytes、dict slotsは別である。
- digestのため `sorted(((qid,key),...))` は1,469,664 tupleとlist pointersを追加し、一般的配置でさらに約94,058,496 bytes。states、dict tableを合わせたE4一回のpeakは保守的にも約650 MiB級であり、`count*width <= 256 MiB` というraw-only capはPython object overheadを全く覆わない。

正しい bounded owner は stable hashを使う deterministic open-address table、例えば `array('I')` の 4,194,304 qid slots（16,777,216 bytes）とfull state storeである。collision時はprobeし、lookup後は retained full 40/154-byte blobと `a^-1*t` の完全一致を要求する。これならE4の主要payloadは226,328,256 + 16,777,216 bytesで、dict key/int/sort tuple数百MBを除ける。同じ coordinateは一度だけ構築/cacheすべきである。

各K0 recordはさらに Gamma 243 gidについて parent walkと **full ten-coordinate** replayをし、欲しい一 coordinate以外の9個も計算する。chronological one-coordinate Gamma recurrenceなら243 edgeだけで済む。kernel BFSも各edgeでbaseからword全体を十coordinate replayする。selected Q0/Gamma parent walkは `reconstruct_task176_selected` と callerで各二回、invariant marked generators `[1],[2]` のten-coordinate replayもselected recordごとに繰り返す。Q0 walk上限N、Gamma walk上限243で、checkerにはwall/RSS meterが無い。

### 9.6 checker/final/UNKNOWN and six-hour bound

Checkerはselected boundaryごとにactive dualの完全 descriptor pairingを再構築し、selected correctionごとにdirect/formula/coordinatesを複数回再生する。`selected_row in selected_old/new` はlist membershipで、selected supportが大きい時はdeep dict比較を伴う二次走査になる。symbol-index mapで線形化できる。

UNKNOWN candidateは最大512 MiB、checkpointは最大4,000,000,000 bytesを一括bytearray/bytes/string/DOM化でき、checker wall/RSS capが無い。Producer final writerは4 GBまで許すのにchecker receipt capは512 MiBで不一致である。COMMON serializationとcheckpoint canonicalization中にproducer wall checkは無く、driverにもchecker timeout、artifact/upload reserve、全体deadlineがない。

したがって「producer 10,800 + checker 7,200 + artifact 3,600 <= 21,600秒」は静的に防御できない。特にchecker K0反復、二重86 MB DOM、4 GB sidecar、heavy後fork/RSS、全document canonicalizationは正しい結果を出し得ても明白に不要かつ上限外である。

## 10. Verdict and one bounded successor

v10 の SELFTEST / production / resume は全て禁止する。raw/recovery-v2とsoundな arithmetic/selected-support部分を保存した **一つの versioned v11** を Luna successor とし、少なくとも次を同一便で満たしてから再監査すること。

1. raw ownerは変更しない。H1 chronological selftest、H2 explicit meter parameter、現 fixture pinを直し、SELFTEST baselineをfull ordinary validatorsへ到達させる。
2. accepted SELFTEST receipt **とchecker verdict** をpath/bytes/SHAでversioned pinし、status/full ledger/code identitiesを照合する。summaryを捨てずCOMMONへ同じbindingを運ぶ。driver modeを二値で拒否し、10,800/7,200/3,600/21,600 outer deadlinesと整合するoutput capを実装する。
3. q3 1..36 grammar→0-based conversion→`right[left[i]]` recurrenceを分離し、970-byte projected ownerとfull JointGroup diagnostic codecを型分離する。diagnosticは非load-bearingでよい。
4. K0 checkerを一coordinate一回の deterministic open-address cacheへ替え、full-state equality、不一致/lookup-none skip、exact A first-gid table/digest、trivial kernel、canonical kernel blobs/cursorを照合する。producerのcursor fallbackをhard stopにする。
5. heavy identityをopened physical authoritiesとchecker reconstructed selected semanticsから導出し、64-hex shapeをauthorityにしない。
6. checkpoint JSON nodeをopcode別にrecursive normalizeし、single read/parse、externally pinned carrier、ordinary new-row provenance/canaryを要求する。heavy logical completion/materializationを正直に型付けし、v290の historical semantic add / restore-validation / fresh input-wall / gauge-peak countersを分離する。final receiptをdurable writeした後だけcheckpointをretireする。
7. light boundary workersをheavy build中も維持するかminimal worker imageへ分離し、pair streamをstream/sliceし、winner contributorを二度全走査しない。全IPC/STOP/restart accountingを累積する。
8. Q0 duplicate edgeの十coordinate計算を除き、同一L bitset proofを共有する。checkerはold rawを一度だけparseし、task176 compressed DOM/rawを段階解放し、iterative DAG expansionとsymbol mapsを用いる。
9. fixtureの全 mutation名についてreal owner、ordinary validator、narrow first rejectionを実行し、`run_common_mutations` / UNKNOWN transport suiteをSELFTEST mainから実際に呼ぶ。PRODUCTIONでは一切fault/mutationを走らせない。

これは有限な修理であるが再pinを伴うため v10 のin-place editではなくv11にする。修理後もまず fresh Sol code/performance auditが必要で、現時点では実行commandを提示・許可しない。

v220 への写像は A0 `0/1` のまま。不成立やUNKNOWNはseparatorを意味せず、lift/fake/Ihara/cofinal claimも無い。

AUDIT VERDICT:                         REJECT / UNEXECUTED
FIRST LITERAL STOP:                    search/d972_r07_history_free_positive_fast_resume_v10.py:2290-2312 (`_validate_triangular_subset`: frozen P5 contains future P6 pivot)
MATHEMATICAL POSITIVE PATH:            REJECT
CHECKER INDEPENDENCE:                  REJECT
CHECKPOINT / RESUME:                   REJECT
PHYSICAL MUTATIONS:                    REJECT
UNNECESSARY SLOW WORK:                 search/d972_r07_history_free_positive_fast_resume_v10.py; crosscheck/check_d972_r07_history_free_positive_fast_resume_v10.py; search/d972_r07_positive_common_word_colgen_v1.py; search/d972_r07_all_seven_extension_section_census_v1.py; search/d972_r07_history_free_positive_fast_resume_gha_driver_v10.g
SELFTEST / PRODUCTION AUTHORIZATION:   NO
ACTUAL A0 COMMON + CHECKER:            0/1
SEPARATOR / NEGATIVE CLAIM:            FORBIDDEN
LIFT / FAKE / IHARA:                   NONE

TASK352_R07_TASK351_A0_V10_CODE_PERFORMANCE_AUDIT
