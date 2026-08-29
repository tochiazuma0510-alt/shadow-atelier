# Sol(max) reply 360 — task358 A4/v6b code/performance static audit

## 0. Verdict and execution boundary

判定は **REJECT / UNEXECUTED** である。監査対象は commit
`e7182efad87d053224ec19d115ab1d8096dbf445` の frozen v2 三ファイルであり、
共有 worktree の後続 HEAD に対して三ファイルが同 commit と byte-for-byte 同一で
あることも `git diff --quiet e7182efa -- <three paths>` で確認した。

Python（候補を含む）、Node、GAP、GHA、workflow、network は実行していない。
以下の到達性・停止点は全て source-only の静的 trace であり、実測 runtime/RSS や
実行成功の主張ではない。両 source に目視上の Python syntax error は見当たらないが、
`py_compile` も行っていない。

Actual task198 baseline は、task357 の manifest codec と layer-local ordinal の二停止を
静的には修理しており、supported POSIX なら baseline の ordinary route は到達可能で
ある。しかし intended row-4 outside path が absent である clean supported-POSIX routeでも、
一 invocation 内で row 1 の parsed receipt DOM reservation を解放しない。
この 186,103,464-byte reservation が残ったまま row 5 に入り、row 5 receipt の
`json.loads` より前の live reservation が 750,000,000-byte cap を越える。従って
producer/checker とも rows 1--4 の narrow terminal 後、row 5 で typed resource stopし、
七 row resultを返さない。さらに semantic receipt reseal DAG、baseline revalidation、
optional output の fail-closed durability、exact type/ABI validator に独立した欠陥がある。

## 1. Frozen identities and authority graph

| owner | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v2.py` | 66,200 | `ca8755b6ad4bf9de001783d76d4de0e4d5d8680795540264ee843680a8deb3e9` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v2.py` | 62,039 | `8ec2fb33d17ac19cab2f13a141e91f05423b87e9edb82fbd8f5543512c0d3252` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v2_20260829.json` | 8,457 | `8fd4de7b89eb07e3adb272782f3052c9b9b3bb90bf7a27212933ae40f892a91d` |
| `sol/luna_reply_358_r07_a4_v6b_authority_trace_finite_repair.md` | 12,083 | `fadefc88e4911234e82b358848b635f88040edd7ac6597a2954f66cce69092b9` |

Fixture の declared canonical self seal は
`abd50579d5d18857ea015bc07fcef4b3bdc7f8f145cfe555f0146f746700d88f`。
両 source は exact relative fixture path、8,457 bytes、file SHA と self sealを pinし、
任意 absolute `--fixture` を拒否する（producer 24--27, 510--518、checker 24--27,
381--386）。fixture は両 programを pinしないため、この dependency graph は acyclic。
scope も `covered_rows=[1..7]`, `remaining_rows=[8..48]`,
`candidate_only=true`, `synthetic=false`, `full_a4_selftest=false` である。

Actual task198 の physical owners も一致した。

| class | bytes | SHA result |
|---|---:|---|
| receipt | 31,017,244 | `82f79555...6b19f5` MATCH |
| acceptance manifest | 2,722 | `cc8c16c8...33ea4` MATCH |
| two attestations + verdict | 81 + 95 + 150 | all MATCH |
| producer/checker/driver sources | 137,169 + 157,253 + 20,541 | all MATCH |

Producer 401--424 と checker 302--315 は manifest の artifact/run/head/member/zip/
terminal、三 source、二 attestation、verdict、top-level receipt bindingを actual constants
へ結ぶ。六 ancillary owner は先に no-follow openされる（producer 506--508、checker
377--379）。この graph と pins は静的に整合する。両 v2 は stdlib-only で相互 import、
task356/v1 import、subprocess/pool/sleep/retry/poll を持たない。従って module-level
isolation は PASS。ただし checker は producer とほぼ同じ lifetime/meter designを再記述
して同一欠陥を持ち、実行済み cross-check の証拠はない。

## 2. Actual codecs and the false semantic-reseal DAG

### 2.1 Baseline decoder is repaired

Receipt validator は top-level `self_digest_sha256` だけを body から外し、manifest
validator は `manifest_self_digest_sha256` だけを外す。manifest の foreign top-level
`self_digest_sha256` も拒否する（producer 391--399、checker 292--300）。両 raw document
は sorted compact ASCII の exact byte framingを要求する（producer 359--389、checker
260--290）。Actual manifest の seal fieldと 0f630... seal、actual receipt の c8f7e... seal
に一致するため、task357 の最初の baseline stop は解消している。

ただし producer 520--530 / checker 388--396 の receipt **sealer** は
`self_digest_sha256` に加えて `manifest_self_digest_sha256` まで黙って `pop` する。
「exactly receipt seal keyだけを remove」する codec ではなく、foreign sealを rejectせず
launderする実装である。

### 2.2 Rows 1/5/6/7 bind the old receipt self seal

より重大なのは、`seal_receipt` が shallow local `body` に新しい
`self_digest_sha256` を挿入して bytesを返すだけで、caller の `changed` DOMを更新しない
ことである。続く `copy_manifest` は returned raw の bytes/SHAを計算する一方、nested
receipt self sealには `changed["self_digest_sha256"]`、すなわち baseline の古い値を
使う（producer 543--549, call 648、checker 408--414, call 501）。

従って rows 1/5/6/7 の実際の DAG は次である。

```text
changed receipt body -> new receipt raw self seal                  correct
new receipt raw      -> manifest.receipt.{bytes,sha256}            correct
old baseline DOM     -> manifest.receipt.self_digest_sha256        WRONG / stale
manifest with stale nested seal -> manifest_self_digest_sha256     internally sealed
```

各 row は final manifest/receipt comparisonより前の intended semantic validatorで reject
するため、この stale nested sealは現在の first-rejection traceに隠れる。もし semantic
mutationが通過すれば producer 503 / checker 374 の第二 manifest validation がこれを
拒否する。よって fixture/reply が列挙する五 node resealは成立しない。Row 2 の manifest
self resealだけ、rows 3/4 の no-resealだけは正しい。

Body raw は producer 525--529 / checker 391--395 で final serialization 前に削除され、
returned receipt raw の retained tokenも `copy_manifest` 完了後まで保たれてから解放される
（producer 643--651、checker 496--504）。この **raw byte lifetime 自体** は PASS だが、
その rawから得た新 self sealを semantic DOMへ返さないため authority bindingが失敗する。

## 3. Baseline and rows 1--7 ordinary semantics

Layer-local ordinal は正しく修理された（producer 428--430、checker 319--321）。

```text
Gamma_Cayley positions 1..6318  -> ordinals 1..6318
action        positions 6319..6422 -> ordinals 1..104
Q0_lift       positions 6423..6441 -> ordinals 1..19
```

Manifest と receipt の両 lexical path は manifest semantic binding より先に同じ ordinary
routeで admitされる（producer 490--503、checker 368--374）。Row 4 basename override は
なく、candidate pathへ `.resolve()` もしない。Row 3 は decode前の physical SHA binding、
`MutationAccepted` は narrow catch外である。

Sequential one-meter traceは次になる。

| row | static first route | static outcome in the actual invocation |
|---:|---|---|
| 1 | `*.authority.row_order` -> `*:authority:layer_ordinal` | intended narrow terminal 1、しかし parsed receipt tokenが漏れる |
| 2 | `*.authority.manifest_acceptance` -> `*:authority:manifest_acceptance` | intended narrow terminal 1 |
| 3 | `*.transport.receipt_identity` -> `*:transport:receipt_sha256` | intended narrow terminal 1、decodeなし |
| 4 | `*.transport.path_containment` -> `*:path:registered_containment` | outside pathがabsentなら narrow terminal 1、basename bypassなし。pre-existing collisionは別途 §5 |
| 5 | intended `*.authority.normal_generation` | receipt parse reservationで `*:meter:peak_live`; narrow terminalなし |
| 6 | intended bridge occurrence rejection | row 5 abortのため未到達 |
| 7 | intended evaluator width rejection | row 5 abortのため未到達 |

従って clean supported-POSIX source traceで構成される narrow terminals は各 side 4/7であり、
七 row result objectは返らない。Fixed outside pathに collisionがあれば row 4 cleanupでさらに
早く abortし得る。これは実測 countではなく静的 control/lifetime traceである。
Windows/no-`O_NOFOLLOW` が typed unsupported inputとなり PASSを返さない点は正しい。

## 4. Exact types and task198 owner semantics

良い点として、normal-generation proof は recursive exact-type/value equality、11-row
occurrence ledger は全12 fieldsの exact keys/types/values、ledger-derived canonical digest、
stored digest、frozen digestの三者を照合する（producer 452--466、checker 341--353）。
Coordinate ownerも hard-coded digest文字列だけではなく、task198/task176 の10-entry typed
ownerを source内で再掲して canonical hashし、bridge/evaluator stored digestへ結ぶ。

しかし「exact task198 codec/ABI」にはなお次の穴がある。

1. `layer_counts` は plain dict equalityだけで、recursive `strict_equal` ではない
   （producer 446、checker 335）。従って `6318.0`, `104.0`, `19.0` は Python equalityで
   integer constantsと等しく、明示された exact-int contractに反する。
2. Row valuesは key shapeと integer typeを調べるが、`target_state/state/generator/record/
   letter` の正値条件と `orientation in {-1,1}` を調べない（producer 428--437、checker
   319--326）。Actual task198 checker は strict positive integer と ±1 orientationを要求
   する（task198 checker 636--654）。
3. Presentation chunks は field typeだけで、actual `chunk_seals(rows)` equality、contiguous
   coverage、`sealed=true`, `prefix_complete=true` を再現しない。`resume_cursor`,
   source encoding, legacy digestにも actual value constraintがない（producer 439--449、
   checker 328--339）。
4. Evaluator は top-level key set、widths、coordinate digest、entry points/encoding/semantics
   の一部だけを固定する。`module` と `relator_rows_sha256` の value/typeを全く検査せず、
   `canaries` は八 keyの集合だけを検査して nested word/value shapesを受理する
   （producer 469--474、checker 355--358）。Actual task198 checker は independently rebuilt
   evaluator objectとの exact equalityを要求する（task198 checker 1610--1612）。

また evidence の owner/kind/logical path は actual mutation functionから返された observation
ではなく、別の `_spec` と `OWNER_BY_NAME` tablesから name lookupする（producer 83--84,
614--624、checker 49--50, 472--479）。現行七 branchesとの一致は目視確認できるものの、
constructor と evidence labelの機械的 dataflowはなく、「actual constructor/observationから
derive」の強い条件は満たさない。

## 5. Physical owner and baseline lifetime

Initial reads は directory components と final componentを `O_NOFOLLOW` で辿り、一つの
live file fdの before/after `fstat` と pathname-afterを比較してから identityを作る
（producer 233--316、checker 149--226）。task357 の post-close fabricated identity は
修理済みである。Workspace cache evictionも exact common-path containmentで keyを消し、
残存 keyを assertする。File caseの hard linkは baseline recheck前に unlinkされる。

一方、per-case baseline recheck は current fd before/after/pathname の内部一致を検査しても、
current `mtime_ns` を baseline identityへ比較しない。また bytesを再hashせず、baseline fdを
保持もしない（producer 317--332、特に326、checker 227--240、特に235）。同じ inode,
size, mode, nlinkの in-place content changeを見逃して `baseline_revalidated=true` にできる。
これは「unchanged baseline handle/path identity」の証明にならない。

Row 4 は `workspace.parent / fixed-basename.outside` を使う（producer 641、checker 494）。
共通 temp parentに同名 foreign ownerが既にあっても path rejection後にそれを除去/restore
せず、`owner_disposed` は workspace deletionだけから trueにする。missing pathを期待する
なら unique siblingと before/after missing assertionが必要であり、現状は isolated physical
case ownerの lifetimeを証明しない。

## 6. Deterministic DOM-owner leak and exact resource formulas

### 6.1 Literal row-5 stop

Local semantic receipt parse は retained owner `case:<name>:receipt` を作る（producer
490--502 -> 477, 365、checker 368--374 -> 360, 266）。しかし case `finally` が解放する
のは `case:<name>:manifest` と `case:<name>:clone` だけで、receipt ownerがない
（producer 724--727、checker 563--566）。Filesystem cacheは evictされても meter tokenは
別 ownerなので残る。

Let

```text
R = 31,017,244   M = 2,722   F = 8,457   S = 315,289
baseline cache tokens = 2(S+F+R+M) = 62,687,424
baseline parsed tokens = 6(F+R+M)  = 186,170,538
B0 = 248,857,962
```

Row 1後に漏れる token は `6R = 186,103,464`。Row 5 receipt parse直前の live
reservationは

```text
B0                                      248,857,962
+ leaked row-1 receipt DOM              186,103,464
+ row-5 receipt clone                   200,000,000
+ changed-manifest clone                     10,000
+ local manifest cache 2M                    5,444
+ local manifest parsed DOM 6M              16,332
+ local receipt cache 2R                 62,034,488
=                                      697,027,690
```

ここへ row-5 parsed receipt `6R = 186,103,464` を retainしようとして
`883,131,154 > 750,000,000` となる。producer 137--148 / 359--366 と checker
87--95 / 260--267 により `*:meter:peak_live` が `json.loads` 前に確定する。

### 6.2 Corrected intended full-run formulas

Leakを仮に直した no-output seven-case routeの exact wire sizesでは、row 2 の
`true -> false` が manifestを1 byte増やし、row 6 の `H1 -> H1_mutated` が receiptを
8 bytes増やす。Luna reply の両 raw formulaはこの9 bytesを落としている。

```text
opened_bytes
 = S+F+R+M + 3(R+M) + (R+8+M) + (M+1) + R
 = 186,443,551                         # reply: 186,443,542

temporary_bytes
 = 3(R+M) + (R+8+M) + (M+1) + R
 = 155,099,839                         # reply: 155,099,830

metered logical opens = 19 reads + 20 atomic-write opens + 14 rechecks = 53
writes = 10; events = 16 baseline + 50 cases = 66; mutations = 7

parsed bytes
 = F + 4(R+M) + (R+8+M) + (M+1) + M + M
 = 155,116,462

dom_bytes charged
 = opened 186,443,551 + parsed 155,116,462
   + 4*200,000,000 + 4*10,000 + 10,000 + R
 = 1,172,627,257 < 1,500,000,000.
```

Let `B=R-88` be a receipt body, `b=M-97` a manifest body,
`D=30,540,174` the frozen rows payload, `Fb` the canonical fixture body length,
`L` the occurrence-ledger serialization length, `C` the coordinate-owner serialization
length, and `Ei` each case event-trace serialization. The exact no-output canonical count is

```text
588,916,696 + Fb + 2L + 3C + sum(E1..E7),
```

where 588,916,696 accounts for all receipt/manifest body+final construction,
ordinary canonical framing/self-seal replay, baseline rows digest, row-2 manifest, and rows
3/4 manifest parsing. The registered per-call bounds give this value well below 750,000,000.

The corrected largest intended retained-token peak is row 6:

```text
248,857,962                         baseline cache + parsed DOM
+ 2*(R+8+M)       =  62,039,948    case cache
+ 6*(R+8+M)       = 186,119,844    case parsed DOM
+ 200,000,000                        receipt clone
+ 10,000                             changed-manifest clone
+ (R+8)            = 31,017,252    parse canonical transient
= 728,045,006 < 750,000,000.
```

Luna reply の 728,034,934 は changed-manifest clone 10,000 と row-6 size delta由来72を
落とす。なお `opens=53` は meter上の論理 countにすぎない。各 `_nofollow` が開く root/
directory-component fd群は一件としてしか reserve/chargeされず、`mkdtemp`, link/unlink,
rmtreeも数えないため、物理 open/operation の「full formula」ではない。

Cache raw eviction、body/raw tokenの局所寿命、one full receipt clone/semantic rowは改善済み。
一方 rows 5--7 は全6,441 rowsを type-walkした後に `rows == baseline_rows` でもう一度
full structural traversalする（producer 447--448、checker 336--337）。Strict typed
comparisonと cached digest判定を一 traversalに統合できるので、なお avoidable duplicated
31-MB-class processingである。

## 7. Optional output atomicity and durability

Staging directoryを parent `st_nlink` の post snapshotより先に削除する順序は正しい
（producer 760--768、checker 595--601）。`atomic_write` と output parent sync の directory
fdも `fsync` exception時には `finally` で closeされる（producer 705--711, 752--756、
checker 547--553, 587--591）。

しかし target は producer 748 / checker 585 の `os.link` で公開された後に、

1. staged link unlink、
2. target parent open/fsync、
3. staging directory rmtree、
4. parent identity comparison

を行う。これらのいずれかが失敗しても targetを unlinkして rollbackせず、failureを返し
ながら published targetが残る。特に post-publication fsync failure、cleanup failure、
parent-identity failureの全てが fail-openである。また rmtree は parent fsync **後** なので、
successful returnでも staging-directory removalを再fsyncしない。

さらに initial parent fdは `O_NOFOLLOW` directory chainで開かれず、second fsync fdや
current pathname identityを initial fdへ比較しない。Lexically `ci/out` 内の symlinked/
substituted parentへ公開でき、old `parent_fd` の self-consistencyだけでは検出できない。
従って exclusive hard-link publication自体は stale targetを上書きしないものの、要求された
bound-parent, publish-last/fail-closed, durable-cleanup contractは **REJECT**。

## 8. Final adjudication

Task357 の manifest seal field、layer reset、row-4 basename bypass、opened-fd identity、fixture
pin、occurrence digest、checker canonical-after は有意に修理された。しかし九項目全体は
完成していない。特に receipt DOM owner leakだけで frozen sequential traceは row 5 にて
決定的に停止し、stale nested receipt sealと optional-output fail-openは meter修理後にも残る。

AUDIT VERDICT:                    REJECT / UNEXECUTED
AUDITED COMMIT:                   e7182efad87d053224ec19d115ab1d8096dbf445
STATIC SYNTAX INSPECTION:         NO OBVIOUS ERROR; NOT COMPILED
ACTUAL BASELINE ROUTE:            STATICALLY REACHABLE ON SUPPORTED POSIX
ROWS 1--7 PRODUCER TRACE:         REJECT (rows 1--4; row 5 peak-meter stop)
ROWS 1--7 CHECKER TRACE:          REJECT (rows 1--4; row 5 peak-meter stop)
SEMANTIC RECEIPT RESEAL DAG:      REJECT (nested self seal is stale)
V297/V298 PHYSICAL SUBSTRATE:     REJECT (baseline revalidation incomplete)
OUTPUT ATOMICITY / DURABILITY:    REJECT (published target survives later failure)
STATIC CAPS / PERFORMANCE:       REJECT
EXECUTION / GHA:                  UNEXECUTED
FULL 48x2 SELFTEST:               INCOMPLETE
ACTUAL A4:                        remains 1/3
LIFT / FAKE / IHARA:              NONE

TASK360_R07_TASK358_A4_V6B_CODE_PERFORMANCE_AUDIT_V1
