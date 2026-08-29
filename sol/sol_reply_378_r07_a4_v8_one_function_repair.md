# Task378 - A4/v8 one-function producer repair

## 0. Static closure and exact owners

The bounded producer-only repair is source-statically complete.  The new
producer has the following final physical identity:

| owner | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v6.py` | 102,151 | `6bbae63e284e055bba2097696f0202645bc38ec9856815af9c1857ecd2131a58` |

The paired frozen owners remain byte-for-byte unchanged:

| frozen paired owner | bytes | SHA-256 |
|---|---:|---|
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v5.py` | 99,782 | `33b7905fb1f00b23b8e30c8b90b57a793cabf62ed272fb258790d3c88ba34165` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v5_20260829.json` | 8,489 | `474d8e19ca49cad06b560cf0ac1d5eeeac1927fe2666224cb9501e77b5cc8481` |

Removing the one root fixture seal member again gives exactly 8,400 ASCII
bytes and SHA-256
`c674491a2f50b200a70349780f0e7a80c21cc0fc3cecd44432dc6e70c51f63fb`.
The fixture contains no v5/v6 program path or task373/task378 reply path, so
the fixture/task198 dependency graph remains acyclic.

As a static delta audit, I removed the new `admit_path` block from v6, removed
the explicit frozen-fixture schema label, and reversed the three producer-local
Task/version/schema substitutions.  The resulting 944-line text equals the
frozen v5 producer line for line.  Thus the only control-flow/validation
addition is the commissioned admission function; every other delta is a
producer-local version/schema label, and all other code is inherited unchanged
from the task375-audited owner.

## 1. Producer-owned admission definition and ordinary call chain

There is exactly one `def admit_path` and exactly three `admit_path(` tokens:
the definition plus the existing manifest and receipt calls.

- Lines 454--455 define the producer-owned function and enter
  `producer.transport.path_containment` with stage `transport` and owner
  `role + ".path"`.
- Lines 456--457 independently normalize the lexical candidate and the exact
  registered receipt-or-manifest path.
- Lines 458--460 admit only the registered owner or an owner contained in the
  invocation workspace.  A containment failure records
  `_path_identity(lexical, "path")` under the same `<role>.path` owner and
  raises `TraceReject` with the exact validator/stage/reason
  `producer.transport.path_containment` / `transport` /
  `producer:path:registered_containment`.
- Lines 461--466 walk every component from the lexical anchor and apply the
  same path-kind observation and narrow rejection to a symlink.
- Line 467 returns the normalized lexical path unchanged after those checks.

The sole ordinary validator is defined at line 667.  Its two admission calls
are both at line 668, first for the manifest and then for the receipt, before
their respective physical opens.  Static reachability is:

```text
main 944--959
  -> execute 883--907
     -> untouched baseline ordinary_route 884
        -> ordinary_route 667 -> admit_path twice at 668
     -> seven-case loop 892--900
        -> run_mutation 852--877 -> ordinary_route 857
           -> the same two admit_path calls at 668
```

There is no checker import, alias, Boolean admission shortcut, second
validator route, or copied checker evidence.  The function uses only the
producer's existing `EventSink`, `_inside`, `_path_identity`, `TraceReject`,
resource constants, and producer-owned paths.

## 2. Version truthfulness without changing frozen bindings

The source label is now `Task378/v6` at line 2 and the producer result schema
is `d972-r07-a4-actual-owner-trace/v6` at line 29.  The paired authority
fixture remains explicitly frozen as
`d972-r07-a4-actual-owner-trace/v5/authority-fixture/v5` at line 30, with its
v5 path and exact byte/SHA/self-seal pins at lines 31--34.  `load_fixture`
checks that frozen schema and self seal at lines 680--683 and the immutable
task198 receipt/manifest identities at line 685.  Hence the producer-local
schema bump neither changes a fixture/task198 edge nor changes any registered
rejection reason.

## 3. Task375 PASS-clause preservation

The exact reverse-delta result above is load-bearing for every item below;
the line references are the final v6 locations.

### Authority, baseline, and seven meanings

- The six immutable task198 source pins are unchanged at lines 95--102.
  Receipt and manifest pins remain at lines 39--44, and fixture enforcement is
  at lines 680--688.
- The eleven-entry occurrence literal still has row 11 with exactly
  `context_id=28` at line 92.  Its exact twelve-field/type/equality checks are
  at lines 614--624.  The complete deferred ABI canary literal remains at
  line 129, is parsed only after the process cap at line 950, and is checked
  completely at lines 632--650.
- The untouched baseline is line 884.  The exact seven registered mutation
  names are line 114; their physical constructors and plans are lines
  730--759; all seven re-enter the ordinary route at line 857 within the loop
  at lines 892--900.

The registered first-rejection meanings remain exact:

| row | validator / stage / reason | v6 evidence |
|---:|---|---|
| 1 | `producer.authority.row_order` / `authority` / `producer:authority:layer_ordinal` | line 584 |
| 2 | `producer.authority.manifest_acceptance` / `authority` / `producer:authority:manifest_acceptance` | line 574 |
| 3 | `producer.transport.receipt_identity` / `transport` / `producer:transport:receipt_sha256` | line 670 |
| 4 | `producer.transport.path_containment` / `transport` / `producer:path:registered_containment` | lines 454--466 |
| 5 | `producer.authority.normal_generation` / `authority` / `producer:authority:normal_generation_proof` | line 611 |
| 6 | `producer.authority.bridge_occurrence` / `authority` / `producer:authority:bridge_occurrence_ledger` | lines 618--620 |
| 7 | `producer.authority.evaluator_abi` / `authority` / `producer:authority:evaluator_abi_canary` | lines 635--649 |

Only `TraceReject` is caught at line 858; the exact fixture/stage/reason/owner
comparison is line 862, and `MutationAccepted` remains outside that catch at
line 875.  Thus the narrow exception discipline is unchanged.

### Physical owners, identity, revalidation, and cleanup

The case writer still binds a concrete child target to its actual parent and
performs fd-relative exclusive staging, link, readback, identity checks, and
namespace cleanup at lines 762--840.  Row 4 still creates an
invocation-unique outside parent and a missing receipt leaf with path-kind
identity at lines 745--749.  Its registered before-path identity is taken at
line 891; same-kind and changed-owner requirements are lines 853--860.

The retained-fd revalidator remains at lines 414--440.  The exact source
formula is `14 * (S+F+R+M)` at line 111: one pre-case call at line 898 and one
post-rejection call at line 873 for each of seven cases.  Case rollback is
lines 814--840, disposal is lines 863--877, and outer cache eviction and leak
checks are lines 899--902.

### Modeled tokens, process cap, and duplicate-work boundary

With `S=315,289`, `F=8,489`, `R=31,017,244`, and `M=2,722`, the unchanged
source formulas at lines 103--111 recompute to:

```text
authority terminal payload A = S+F+R+M                     = 31,343,744
modeled peak = A+(R+8)+1,048,576                           = 63,409,572
owner-read bytes                                            = 186,443,583
temporary/case-stage bytes                                  = 155,099,839
parsed input                                                 = 279,185,470
fourteen retained-fd revalidations                           = 438,812,416
```

The public ledger still labels these as modeled payload tokens and explicitly
omits parsed DOM/container/interpreter/allocator overhead, capacity slack, and
RSS (lines 186--243).  Exact final peak, terminal payload, counters, and zero
reservations are asserted at lines 903--904.  They are not an RSS or observed
allocation claim.

The bounded incremental canonical encoder is unchanged at lines 247--296.
The fused physical canonical comparison, seal-body hash, and row whole/chunk
feeds remain at lines 489--557; the separate non-serializing row schema walk
is lines 582--607.  Receipt identity is passed directly to the manifest at
lines 692--715, and fresh sequential mutation parsing remains at lines
720--750.  There is no `deepcopy`, full `json.dumps(...).encode(...)`, or
result publisher in v6.

Linux `RLIMIT_AS` installation/readback remains at lines 909--925.  In
`main`, `--output` is rejected at line 947, the limit is installed at line
948, deferred ABI parsing follows at line 950, and the first fixture/authority
load follows at line 955.  Canonical stdout remains the sole result route at
lines 933--956.  The two `os.link` sites at lines 803 and 864 are confined to
the physical mutation case writer and its disposal audit; neither is a result
publisher.

### Exact scope

The frozen fixture scope is required at line 684 and the result repeats it at
line 905:

```text
covered_rows=[1,2,3,4,5,6,7]
remaining_rows=[8,...,48]
candidate_only=true
full_a4_selftest=false
actual_a4_numerator=false
```

The frozen independent checker and fixture identities above did not change.
Therefore the checker PASS findings, rows 8--48 noncoverage, absence of a
driver, and A4=1/3 boundary are all retained.

## 4. Static-only handoff

Only read-only PowerShell inspection, in-memory static comparison, SHA-256
hashing, and `apply_patch` for the two designated outputs were used.  I did
not run Python, Node, GAP, either candidate, syntax compilation, import
compilation, mutations, RSS measurement, GHA, workflows/workflow dispatch,
git, or network commands.  No runtime result or resource observation is
claimed.  The v8 hybrid tranche remains UNEXECUTED and requires a fresh
independent static reaudit of this exact v6 producer against the frozen v5
checker and fixture before any driver may be designed.

TASK375 UNDEFINED admit_path:            REPAIRED
PRODUCER-OWNED ORDINARY ADMISSION ROUTE: REACHABLE
TASK375 PASS CLAUSES:                    RETAINED
ROWS 1--7 PRODUCER/CHECKER ROUTE:        IMPLEMENTED
RUNTIME / MUTATIONS / GHA:               UNEXECUTED
FRESH INDEPENDENT REAUDIT REQUIRED:      YES
PINNED GHA DRIVER:                       NOT PRESENT
FULL 48x2 SELFTEST:                      INCOMPLETE
ACTUAL A4:                               remains 1/3
LIFT / FAKE / IHARA:                     NONE

TASK378_R07_A4_V8_ONE_FUNCTION_REPAIR
