# Sol(max) reply 379 — independent A4/v8 one-function static reaudit v1

## 0. Decisive result and boundary

The frozen hybrid tranche is **STATIC PASS**.  The v6 producer restores the
single missing producer-owned `admit_path` definition, both ordinary-route
uses are reachable, and reversing that bounded repair plus the local truthful
version/schema labels reproduces the frozen v5 producer byte for byte.  Every
task375 PASS clause is therefore retained; the sole task375 REJECT cause (the
undefined producer name) is closed.

I read task375 and its complete reply, then task378 and its complete reply,
and independently inspected the task379 owners.  This was source-static and
read-only: only PowerShell inspection and SHA-256 hashing were used.  I did not
run Python, Node, GAP, either candidate, syntax/import compilation, mutations,
RSS, GHA/workflows, git, or the network.  The `4bbb2911` label was consequently
not queried through git; the physical tranche is identified by the mandated
byte counts and hashes below.

For line references, `P` denotes the frozen v6 producer and `C` the frozen v5
checker.

## 1. Frozen hybrid owners and fixture seal

All four mandated physical identities match:

| frozen owner | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v6.py` | 102,151 | 961 | `6bbae63e284e055bba2097696f0202645bc38ec9856815af9c1857ecd2131a58` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v5.py` | 99,782 | 752 | `33b7905fb1f00b23b8e30c8b90b57a793cabf62ed272fb258790d3c88ba34165` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v5_20260829.json` | 8,489 | 1 | `474d8e19ca49cad06b560cf0ac1d5eeeac1927fe2666224cb9501e77b5cc8481` |
| `sol/sol_reply_378_r07_a4_v8_one_function_repair.md` | 10,521 | 210 | `4e7fa642fa79cac1cacf23267f7283566d0deb4fe5964b72dcf4d0c9f85cf11a` |

The fixture is one 8,488-byte canonical ASCII line followed by LF.  Removing
the final *root* `,"self_digest_sha256":"<64 hex>"` member (88 bytes), rather
than the nested task198 receipt member, leaves exactly 8,400 bytes with
SHA-256 `c674491a2f50b200a70349780f0e7a80c21cc0fc3cecd44432dc6e70c51f63fb`.
That equals the mandated root seal and the frozen constants consumed at
P:31--34 and C:28--31.

## 2. Exact v5-to-v6 bounded delta

The comparison base is the frozen 944-line, 101,139-byte v5 producer with
SHA-256 `2d0be0e2875404cf25fbaa020d501a7e250c977e9fa9c946362363544540dde9`.
I independently reversed the v6 source in memory as follows:

1. remove P:30, the new explicit frozen-fixture `FIXTURE_SCHEMA` assignment;
2. remove P:454--469, namely the 14 code lines P:454--467 defining
   `admit_path` and its two separator blank lines P:468--469;
3. change only `Task378/v6` back to `Task373/v5` at P:2;
4. change the result schema suffix `/v6` back to `/v5` at P:29; and
5. replace the use of `FIXTURE_SCHEMA` at P:683 with the former expression
   `SCHEMA + "/authority-fixture/v5"`.

The reverse result has 944 lines and 101,139 bytes, has the exact v5 SHA-256
above, and is case-sensitive byte-for-byte equal to the frozen v5 owner.

Those five entries enumerate the complete source delta.  In the forward
direction they are: one truthful docstring version substitution (P:2), one
truthful result-schema substitution (P:29), one explicit constant retaining
the frozen v5 fixture schema (P:30), the commissioned producer function
(P:454--467 plus separation), and the corresponding fixture-schema reference
(P:683).  There is no remaining import, authority, resource, mutation,
publisher, exception, path, result-scope, or conclusion delta.

## 3. Producer-owned path admission and reachability

An exact-token inventory finds one `def admit_path` and three `admit_path(`
tokens total: the definition and exactly the manifest/receipt calls on P:668.
The definition satisfies each commissioned condition directly:

| condition | independent source finding |
|---|---|
| exact event and owner | P:455 enters `producer.transport.path_containment`, stage `transport`, owner `role + ".path"` |
| normalized paths | P:456--457 applies `os.path.abspath` to both candidate and registered paths |
| narrow admission set | P:458 admits only exact registered equality or `_inside(lexical, workspace)` with a non-`None` invocation workspace |
| path-kind failure evidence | P:459 records `_path_identity(lexical, "path")` under the same `<role>.path` owner |
| exact narrow rejection | P:460 raises `TraceReject("producer.transport.path_containment", "transport", "producer:path:registered_containment")` |
| every symlink component | P:461--466 accumulates every component from the lexical anchor, including the leaf, and uses the same observation and reason |
| admitted value | P:467 returns the normalized lexical path |

The referenced names are producer-owned and defined: `os` at P:12, `Path` at
P:18, `ROOT` at P:22, the registered relative paths at P:36--37,
`TraceReject` at P:147, `_inside` at P:318--320, `_path_identity` at
P:353--358, and `EventSink.enter`/`observed` at P:361--365.  Imports P:7--19
are standard-library only.  The function contains no catch, Boolean-return
shortcut, checker import/alias, copied checker result, alternate validator, or
changed reason.  Its only two roles are the literal `manifest` and `receipt`
arguments at P:668.

The physical-open ordering and complete static call chain are:

```text
main P:944--959
  -> load fixture, then execute P:955
     -> untouched baseline ordinary_route P:884
        -> admit manifest P:668
        -> manifest physical store.read P:668
        -> admit receipt P:668
        -> receipt physical store.read P:668
     -> seven-case loop P:892--900
        -> run_mutation P:852--877
           -> ordinary_route P:857
              -> the same two P:668 admissions before their bound opens
```

Thus the baseline and all seven mutations reach the same producer-owned
definition.  `run_mutation` catches only `TraceReject` at P:858, checks exact
owner/identity/validator/stage/reason/reseal data at P:859--862, and leaves
`MutationAccepted` outside that catch at P:875.  The exact retained first
rejections are:

| row / mutation | validator / stage / narrow reason | P lines |
|---|---|---:|
| 1 `per_layer_ordinal` | `producer.authority.row_order` / `authority` / `producer:authority:layer_ordinal` | 584 |
| 2 `authority_binding` | `producer.authority.manifest_acceptance` / `authority` / `producer:authority:manifest_acceptance` | 574 |
| 3 `canonical_input_bytes` | `producer.transport.receipt_identity` / `transport` / `producer:transport:receipt_sha256` | 669--670 |
| 4 `resolved_path_traversal` | `producer.transport.path_containment` / `transport` / `producer:path:registered_containment` | 454--466 |
| 5 `normal_generation_proof` | `producer.authority.normal_generation` / `authority` / `producer:authority:normal_generation_proof` | 611 |
| 6 `bridge_typed_occurrence_ledger` | `producer.authority.bridge_occurrence` / `authority` / `producer:authority:bridge_occurrence_ledger` | 618--620 |
| 7 `evaluator_abi_canary` | `producer.authority.evaluator_abi` / `authority` / `producer:authority:evaluator_abi_canary` | 635--649 |

The frozen checker remains independent: its own admission is C:318--326 and
ordinary route C:497--501; baseline construction is C:680--686, the seven-case
loop is C:687--697, and only its own narrow rejection is accepted at
C:660--675.  No checker evidence is used to make the producer route reachable.

## 4. Inherited authority, physical-owner, and cleanup boundary

Exact reverse equality retains the immutable graph: task198 receipt/manifest
pins are P:39--45, the six source owners are P:95--102, fixture authentication
and graph identities are P:680--688, and the checker enforces the paired graph
at C:65--93 and C:508--510.  The fixture itself points only to the immutable
task198 receipt and manifest, not to either v5/v6 program or task reply, so the
authority graph stays acyclic.

Occurrence row 11 remains the twelve-field entry with `context_id=28` at P:92;
exact typed-ledger comparison remains P:614--624 (and C:462--470).  Coordinate
widths and ownership are P:49--79.  The complete evaluator ABI—including six
entry points, all eight canary keys, typed ten-coordinate values, source,
action, cocycle shapes, and exact recursive equality—remains P:632--650 and
C:472--488.  The ABI literal is deferred until after the process cap (P:948,
P:950).

The seven mutation names are unchanged at P:114; their physical plans are
P:730--759.  The case writer retains fd-relative exclusive stage/link/readback
and cleanup at P:762--840.  Row 4 still allocates an invocation-unique outside
parent and a missing receipt leaf with path-kind identity at P:745--749.
Same-kind/different-owner enforcement is P:853--860.  Rejection cleanup and
outside-owner disposal are P:863--877; the outer finally evicts cache/workspace
and checks owner leaks at P:899--902.

The retained-fd revalidator is P:414--440.  Each of seven cases performs one
pre-route pass at P:898 and one post-rejection pass at P:873, hence fourteen
passes over the nine authority handles assembled at P:886--891.  Cleanup
precedes the post-pass.  The unchanged checker independently has the analogous
physical route at C:573--697.

## 5. Independent allocation and performance accounting

From P:95--111 (identical arithmetic remains at C:65--78), let

```text
S = 81+95+150+137,169+157,253+20,541 =    315,289
F =                                              8,489
R =                                         31,017,244
M =                                              2,722
A = S+F+R+M                                = 31,343,744
```

The source formulas independently recompute to:

```text
authenticated owner-read bytes                         186,443,583
temporary/case-stage bytes                              155,099,839
ordinary parsed bytes                                   155,116,494
four fresh sequential receipt parses                    124,068,976
total parsed input                                      279,185,470
14 retained-fd revalidation bytes                       438,812,416
largest modeled payload-token state                     63,409,572
terminal authority payload-token state A                31,343,744
logical opens / physical writes / events / mutations    53 / 10 / 66 / 7
```

These values fit the declared caps at P:54--66: 250,000,000 opened bytes,
250,000,000 temporary bytes, 350,000,000 parsed bytes, 750,000,000 modeled
payload tokens, 750,000,000 recheck bytes, 256 opens/writes, 10,000 events,
and exactly seven mutations.  The final account at P:903--904 requires the
exact intended counters, 438,812,416 revalidated bytes, zero reservations,
terminal payload `A`, and the exact 63,409,572 peak.

The accounting operations are structurally retained: reserve-before-charge
and owner release are P:186--243; bounded 65,536-character canonical fragments
and exact bytearray growth charges are P:247--296; physical reads use bounded
1,048,576-byte slots and retain exact cache bytes at P:370--413; retained-fd
rehashing is P:414--440.  The public field explicitly calls the value
`modeled_payload_tokens` and excludes parsed DOM, decoder/interpreter/container/
allocator overhead, bytearray slack, and RSS at P:224--240.  Therefore the
63,409,572 figure is a modeled token maximum, not an RSS or total-allocation
measurement.

The canonical path remains incremental.  P:489--557 fuses physical canonical
comparison, root body-seal hashing, whole-row hashing, and bounded 1,024-row
chunk hashing; P:582--607 performs the subsequent typed row walk without
serializing again.  Receipt identity is fed directly into manifest construction
at P:692--715, and the four semantic constructors parse sequentially at
P:720--759.  There is no `deepcopy`, full-document `json.dumps(...).encode(...)`,
second avoidable 31 MB canonical buffer, quadratic string concatenation, or
new full-receipt pass.  The frozen checker retains the corresponding bounded
encoder/buffer at C:147--196, physical store at C:245--316, fused scan at
C:347--421, and nonserializing typed walk at C:435--458.

Linux/POSIX `RLIMIT_AS` installation and exact readback remain P:909--925.
`main` rejects any supplied `--output` at P:947, installs the limit at P:948,
then parses the deferred ABI at P:950 and first loads fixture/authority data at
P:955.  Canonical stdout P:933--956 is the sole result route.  There is no
result-stage path, output conversion, result link/rename, or publisher helper;
the `os.link`/`shutil` uses at P:762--877 are confined to physical mutation
owners and cleanup.  The frozen checker retains the same fail-closed order at
C:704--746 and its stdout-only result path at C:722--733.

## 6. Scope and authorization

The fixture rejects any scope other than rows 1--7 at P:684, and the result
repeats the exact boundary at P:905:

```text
candidate_only=true
synthetic=false
covered_rows=[1,2,3,4,5,6,7]
remaining_rows=[8,9,...,48]
full_a4_selftest=false
actual_a4_numerator=false
```

Rows 8--48 were not audited or covered.  No pinned v8 GHA driver is present.
This STATIC PASS authorizes only creation and a separate independent static
audit of such a rows-1--7 driver; it does not authorize execution, increment
A4, or claim a basis, lift, fake, or Ihara witness.

AUDIT VERDICT:                         STATIC PASS
FROZEN HYBRID OWNERS:                  PASS
EXACT V5->V6 BOUNDED DELTA:            PASS
PRODUCER admit_path DEFINITION/USES:   PASS
ROWS 1--7 PRODUCER ROUTE REACHABLE:    PASS
TASK375 PASS CLAUSES RETAINED:         PASS
V8 CANDIDATE EXECUTION:                FORBIDDEN
PINNED GHA DRIVER:                     NOT PRESENT
FULL 48x2 SELFTEST:                    INCOMPLETE
ACTUAL A4:                             remains 1/3
LIFT / FAKE / IHARA:                   NONE

TASK379_R07_A4_V8_ONE_FUNCTION_REAUDIT_V1
