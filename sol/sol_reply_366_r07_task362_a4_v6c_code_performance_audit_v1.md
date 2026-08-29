# Sol(max) reply 366 — task362 A4/v6c code/performance static audit

## 0. Verdict and execution boundary

判定は **STATIC REJECT / UNEXECUTED** である。三 frozen owner は指定値と
byte-for-byte 一致した。

| owner | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v3.py` | 94,299 | `22edde4e3c2fa00ad858f7aa8175774037c0f02ebd28eec27d83ffd184bb534c` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v3.py` | 91,766 | `f9b1305d975a53309fff527aa9061aa3182fb3409a7e4003d35044cb98e64c25` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v3_20260829.json` | 8,457 | `0d58bace814a7b838f7bf08a91ca7e1eea79e7d4d5099b52281ea7cce61ed225` |

Binding recordsも一致した: task362 contract = 10,384 bytes /
`dcb5d0096396a09be8046739344a8f1d9083e2914bb41a3eab9bd4703472257d`,
task362 reply = 11,927 bytes /
`5ebf314fbdc5f77073cf8b5b7a166aa57144f77f8471e30501865235cbbee621`,
task360 audit = 19,738 bytes /
`f8f172d753493ea08463f635fc05ac04ac6326b11a5835dea167b6b0277c6d32`。

Python/Node/GAP、候補 program、GHA/workflow、network、git は一切実行して
いない。以下は source-only trace であり、syntax compile、runtime、RSS の主張では
ない。両 source に目視上の syntax error は見当たらない。

## 1. Decisive ordinary-route failures

### F1 — checker は actual baseline 自体を拒否する

Actual task198 occurrence row 11 は `context_id=28` を持つ（task198 checker
94, 101--107）。v3 checker の独立 literal は row 11 に `context_id` を書かず、代わりに
余分な `source` を書いた後、その `source` だけを pop する（checker 51--54）。従って
最終 expected row は `context_id` のない 11-key dict である。一方 validator は
`context_id` を含む 12-key setを要求し、さらに actual と expected の recursive exact
equalityを要求する（checker 343--346）。

よって `execute` の baseline `ordinary(...)`（checker 508--509）は bridge entry
（369--375）で `checker:authority:bridge_occurrence_ledger` を投げる。この baseline call は
case の narrow catch の外なので、checker は mutation 1 にすら入らず、七 row resultを
返さない。

### F2 — producer/checker の case writer は workspace の外を開く

`_nofollow_parent(path)` / `parent_nofollow(path)` は `path.parent` の fd と
`path.name` を返す（producer 266--276; checker 151--160）。しかし case writer は
mutation file `path` ではなく、既に存在する directory `workspace` を渡す（producer
647--650; checker 457--460）。従って得るものは

```text
parent fd = workspace.parent
leaf      = workspace.name
```

である。temporary regular file は workspace の**隣**に作られ、最後にその fileを既存
workspace directory名へ renameしようとする（producer 656--664; checker 465--472）。
Clean supported POSIX でも file は directoryを置換できず、producer は row 1 の `_plan`
（626--636）で `producer:case:atomic_write`、checkerも F1 を直した仮定の下で同じ row 1
stopとなる。ordinary validator、evidence、first rejection は一件も得られない。

したがって frozen source の静的到達結果は:

| side | baseline | rows 1--7 | result object |
|---|---|---|---|
| producer | statically reachable on supported POSIX | row 1 constructorで停止、0/7 | none |
| checker | bridge ledgerで停止 | 0/7 | none |

## 2. Task360 semantic/type obligations

Receipt/manifest reseal DAGそのものは **statically repaired** である。Receipt sealer は
foreign manifest sealを拒否し receipt sealだけを除去し、manifest側も逆向きを行う
（producer 564--573; checker 391--398）。`SealedReceipt` は DOM/raw/raw SHA/length/new
self sealを運び、`copy_manifest` は tupleを検査して三 nested receipt 値をそこから結ぶ
（producer 141--155, 576--586; checker 87--90, 399--407）。Rows 1/5/6/7 の五 node
DAG、row 2 の manifest-only reseal、rows 3/4 の no-resealも source上は正しい
（producer 626--644; checker 437--455）。task360 の stale nested seal defect は消えた。

Producer の exact presentation/type/ABI repairも source上は整合する。Single typed row
walkが exact keys/string/positive integer/orientation、layer-local ordinal、chunk seals and
coverageを同時に検査する（producer 438--480）。Normal proof、11-entry/12-field occurrence
ledger、coordinate owner、full evaluator ABI/canariesを exact comparisonする（484--523）。
Checker側も同じ型・ABI checksを別 sourceに持つ（297--366）が、F1 の独立 literal errorで
baseline全体としては FAIL である。

Read-only source/JSON inspectionでは producer literal、checker literal、actual receipt の
evaluator canaries はいずれも canonical 16,464 bytes、SHA-256
`6fb8df36710628faded5438e993a21416809e056b214c5a732aac05688fb66d0`
で完全一致した。従って ABI canary 自体でなく occurrence row 11 が checker stopの原因で
ある。

Fixture は self seal
`faa301467e8c5047b192da539467409631cdd9abe5a480f18aa175926b897a14`、scope
`covered_rows=[1..7]`, `remaining_rows=[8..48]`, `candidate_only=true`,
`full_a4_selftest=false`, `actual_a4_numerator=false` を保持する（fixture 2--3,
13--15, 25--30）。Fixture は v3 programを pinせず、両 programは stdlib-onlyで相互
import/shared helperを持たない（producer 7--19; checker 7--19）。従って seal DAGの
acyclicityと module-level non-sharing は PASS。ただし checker は producer evidenceを
受け取らないという設計だけでは F1/F2 を救えず、実行済み cross-checkも存在しない。

## 3. Physical owners and baseline lifetime

Task360 の baseline revalidation defectは修理されている。両側は六 source、fixture、
manifest、receipt の live no-follow fdを invocation中保持し、各 case前後に rewind、exact
length/SHA、device/inode/type/mode/size/nlink/mtime、fresh no-follow pathname identityを
比較する（producer 313--381, 716--720, 846--847; checker 184--247, 508--512,
631--632）。この部分は PASS である。

Row 4 の unique outside parent と before/after absence cleanupも改善されている
（producer 632--635, 701--705; checker 443--446, 500--503）。ただし evidence identity
には残存 defect がある。`plan.identity_kind="path"` なのに `before` は一律
`baseline[plan.role+"_identity"]`、すなわち receipt **file** identityから取る（producer
687--693; checker 488--493）。Only `after` の kindしか planと比較しない。従って row 4
evidenceは top-level kind/path と after ownerが `path` なのに、before projectionの
`owner_kind` は `file` となる（producer 678--680, 707; checker 484--486, 505）。これは
v297 の「I_before/I_afterを registered identity typeで比較」という契約（v297 82--87）と
task362 の actual owner/kind dataflowを満たさない。

## 4. Exact resource account and performance

Declared opened/temporary/DOM arithmeticは intended wire sizesについては正しい:

```text
opened    = 186,443,551
temporary = 155,099,839
parsed    = 155,116,462
DOM       = 1,172,627,257
```

しかし `largest intended peak = 728,045,006` は final source の meter lifetimeを表さない。
`canon_meter` は retained final receipt rawに actual lengthでなく full 35,000,000-byte boundを
retainする（producer 219--230, 564--567; checker 127--137, 391--394）。Manifest final rawも
10,000を retainする。どちらも ordinary validation前に解放されず、case `finally` の
`release_prefix` まで liveである（producer 626--636, 727--732; checker 437--447,
519--524）。

Writerだけを仮に直した row 1 の exact meter traceは:

```text
baseline retained B0                         248,857,962
receipt clone                                200,000,000
retained sealed receipt bound                 35,000,000
changed-manifest clone + sealed manifest          20,000
case cache 2(R+M)                             62,039,932
case parsed owners 6(R+M)                    186,119,796
                                              -----------
before exact receipt canonical               732,037,690
+ parse canonical transient R                 31,017,244
                                              -----------
actual metered request                        763,054,934 > 750,000,000
```

従って producer 398--405 / checker 259--267 の exact canonical comparisonで row 1 は
`peak_live` stopする。Reply/source の row-6 value 728,045,006 は retained receipt raw
35,000,000 と retained manifest raw 10,000、合計 **35,010,000** を落としている
（producer 90--95; checker 59--64）。F2 を一点修理しても七 row routeは成立しない。

また `METERED_LOGICAL_OPENS=53`（producer 96; checker 65）は実装されていない。
Cache miss reads 19 と case writes 20 は chargeされるが、14 retained-fd revalidation passes
には `opens` reserve/chargeがない（producer 350--371; checker 218--236）。No-output intended
routeの public meterは 39を返す一方、reply 146--149 は53と報告する。Revalidation bytes
自体は `14*(S+F+R+M)=438,811,968 < 750,000,000` で feasibleである。

Task360 が指摘した二度目の 6,441-row structural equality traversalは除去され、typed checkと
row/chunk digestは一 passに融合された（producer 449--480; checker 307--338）。ここは
performance PASS である。一方、両 parse pathは canonical bytesと `bytes(raw)` を比較して
31-MB bytearrayをもう一度 full copyする（producer 397--405; checker 259--267）。さらに
checker `digest_bytes` は常に `bytes(raw)` を作る（checker 138）、各 31-MB physical receipt
hashにも不要な full copyを追加する。これらは reserveされない O(R) allocationであり、
同じ contentは bytearray/memory bufferのまま比較・hash可能なので、明確に avoidableで
peak account外の処理である。要求された finite scopeに superlinear algorithmはないが、
この duplicated 31-MB-class processing と上の false live tokensにより static
caps/performance は REJECT である。

## 5. Optional publication is still not a valid bound-parent transaction

Both output writers repeat the same parent-selection error. For target
`.../ci/out/result.json`, they call `_nofollow_parent(target.parent)` /
`parent_nofollow(target.parent)` (producer 759--765; checker 558--564). This opens
`.../ci` and returns leaf `out`, not an fd for `.../ci/out` and leaf `result.json`.
Because line 761/560 already requires `target.parent.exists()`, the subsequent stale check sees
that directory as the alleged final target and always stops (producer 773--774; checker
572--573). No supported successful publication route exists.

Independently, the success check only compares two `fstat`s of the retained fd and never rewalks
the registered parent pathname to that fd (producer 768, 794--795; checker 567, 593--594), so the
required retained-parent/pathname identity is absent. On a staging failure, cleanup tries to unlink
`staged.json` relative to `parent_fd` although the file is inside `stage_fd`, then suppresses the
error (producer 803--813; checker 602--612); a failed call can leave the staging directory/file.
Thus task360's bound-parent/failure-atomic/durable cleanup defect is not repaired even apart from
the deterministic stale stop.

## 6. Final adjudication

The semantic receipt reseal, exact producer ABI, baseline retained-fd revalidation, fixture DAG,
and fused row walk are genuine repairs. They do not outweigh four load-bearing failures: checker
baseline rejection, both unreachable case writers, a deterministic >750-MB row-1 meter request,
and an unreachable/incomplete optional publication transaction. The task362 reply's six
`REPAIRED/IMPLEMENTED` declarations at lines 199--204 are therefore false for the frozen owners.

```text
AUDIT VERDICT:                         STATIC REJECT / UNEXECUTED
STATIC SYNTAX INSPECTION:              NO OBVIOUS ERROR; NOT COMPILED
SEMANTIC RECEIPT/MANIFEST RESEAL DAG:  STATIC PASS
EXACT TYPE / ABI — PRODUCER:           STATIC PASS
EXACT TYPE / ABI — CHECKER:            REJECT (baseline ledger row 11)
INDEPENDENT CHECKER NON-SHARING:       STATIC PASS (module-level only)
BASELINE RETAINED-FD REVALIDATION:     STATIC PASS
ROW-4 IDENTITY PROJECTION:             REJECT (file/path kind mismatch)
ROWS 1--7 PRODUCER TRACE:              REJECT (row 1 writer; 0/7)
ROWS 1--7 CHECKER TRACE:               REJECT (baseline; 0/7)
STATIC CAPS / RESOURCE ACCOUNT:        REJECT
AVOIDABLE DUPLICATED PROCESSING:       REJECT
OUTPUT ATOMICITY / DURABILITY:         REJECT
EXECUTION / GHA:                       UNEXECUTED
FULL 48x2 SELFTEST:                    INCOMPLETE
ACTUAL A4:                             remains 1/3
LIFT / FAKE / IHARA:                   NONE
```

`TASK366_R07_TASK362_A4_V6C_CODE_PERFORMANCE_AUDIT_V1`
