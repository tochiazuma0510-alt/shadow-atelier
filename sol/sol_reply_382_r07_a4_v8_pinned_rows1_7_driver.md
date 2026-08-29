# Sol(max) reply 382 — A4/v8 pinned rows-1--7 driver static blocker

## 0. Decisive result

The commissioned driver is **INCOMPLETE / STATIC BLOCKER**.  I did not create
`search/d972_r07_a4_actual_owner_trace_gha_driver_v8.g`.  Both frozen candidate
owners contain the same load-bearing row-4 contradiction: the ordinary route
enters the containment validator once for the manifest and again for the
receipt, but the mutation acceptance gate requires that validator to occur
exactly once.  Row 4 therefore reaches the intended narrow path rejection and
then deterministically converts it to an input stop instead of returning a row
record.

A driver obeying task382's exact-zero-exit, complete-JSON, seven-row and
independent-admission requirements could never publish its accepted sentinel
against these owners.  Masking the nonzero exits, deleting row 4, editing the
expected trace, accepting partial stdout, or synthesizing a fixture-shaped
result would violate the commission.  The only truthful action is to leave the
driver absent and require a new versioned source repair before driver creation.

This is a source-static finding.  I used read-only PowerShell inspection and
SHA-256 hashing only.  I did not run or compile Python, Node, GAP, either
candidate, mutations, GHA, workflows, git, or network commands.

## 1. Frozen identities

The mandated owner pins themselves match exactly:

| frozen owner | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v6.py` | 102,151 | `6bbae63e284e055bba2097696f0202645bc38ec9856815af9c1857ecd2131a58` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v5.py` | 99,782 | `33b7905fb1f00b23b8e30c8b90b57a793cabf62ed272fb258790d3c88ba34165` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v5_20260829.json` | 8,489 | `474d8e19ca49cad06b560cf0ac1d5eeeac1927fe2666224cb9501e77b5cc8481` |

Removing only the fixture's root seal member leaves 8,400 canonical ASCII
bytes with SHA-256
`c674491a2f50b200a70349780f0e7a80c21cc0fc3cecd44432dc6e70c51f63fb`.
Thus this blocker is not identity drift, a fixture-seal failure, or an
authority substitution.  It is control-flow logic inside both exact frozen
programs.

The requested driver identity is:

```text
path:    search/d972_r07_a4_actual_owner_trace_gha_driver_v8.g
status:  ABSENT BY FAIL-CLOSED DECISION
bytes:   N/A
SHA-256: N/A
```

The physical identity of this reply is necessarily reported by the enclosing
handoff after the file is closed and hashed; embedding a file's own physical
SHA-256 in that same file would be self-referential.

## 2. Producer contradiction

The producer's path admission definition enters
`producer.transport.path_containment` unconditionally at P:455.  Its ordinary
route invokes that same function twice at P:668: first with literal role
`manifest`, then with literal role `receipt`.

For `resolved_path_traversal`, P:745--749 keeps the manifest path unchanged and
replaces only the receipt path with an invocation-unique absent path outside
the workspace and repository.  Consequently the row-4 event sequence has:

1. the manifest call at P:668 entering
   `producer.transport.path_containment` at P:455 and succeeding; and
2. the receipt call at P:668 entering the identical validator at P:455, then
   raising the exact registered containment rejection at P:458--460.

`run_mutation` reaches the ordinary route at P:857 and catches that exact
`TraceReject` at P:858.  It constructs `entered` from every event validator at
P:861.  At this point

```text
rejection.validator = "producer.transport.path_containment"
entered.count(rejection.validator) = 2
```

but P:862 requires `entered.count(rejection.validator) == 1`.  The condition
therefore raises `InputStop("producer:fixture:trace:resolved_path_traversal")`.
No row-4 record is returned, rows 5--7 are not reached, final accounting at
P:903--904 is not reached, and no complete sealed stdout result is emitted.

This is not cured by the task378 `admit_path` restoration.  The restored
function made both calls reachable, which exposes the pre-existing uniqueness
predicate as impossible for row 4.

## 3. Independent checker contradiction

The checker independently has the same defect; this is not producer evidence
being injected into it.  Its `admit` enters
`checker.transport.path_containment` unconditionally at C:319, and its
ordinary route calls `admit` for manifest and receipt at C:498.

The row-4 checker plan at C:557--561 likewise changes only the receipt path to
an invocation-unique absent outside owner.  Therefore the successful manifest
admission and rejecting receipt admission put two copies of
`checker.transport.path_containment` into the journal.  `run_case` calls the
ordinary route at C:659, catches the intended `NarrowRejection` at C:660, and
builds `entered` at C:661.  Hence

```text
rejection.validator = "checker.transport.path_containment"
entered.count(rejection.validator) = 2
```

while C:664 requires the count to equal 1 and raises
`CheckerInputStop("checker:fixture:trace:resolved_path_traversal")`.  The
checker also cannot return a seven-row sealed stdout object.

The fixture's row-4 expectations are otherwise coherent: path-kind owner,
transport stage, no downstream reseals, and the exact respective narrow
reasons `producer:path:registered_containment` and
`checker:path:registered_containment`.  The failure is solely the use of a
whole-trace validator-count uniqueness test for a validator intentionally
shared by two role-specific admission events.

## 4. Consequence for task379 and task382

Task379 correctly established exact physical identities, the bounded v5-to-v6
delta, existence of one producer admission definition, its two ordinary calls,
and preservation of the authority/resource/publication boundaries.  Its
combined claim that all seven producer rows can complete, however, is
superseded by the count contradiction above.  Therefore the aggregate
`TASK379 PASS CLAUSES` status is `REGRESSED`; the regression is narrow to
row-4 trace acceptance, not the immutable authority, allocation ledger,
streaming, `RLIMIT_AS`, stdout-only, or rows-1--7 scope clauses.

Task382 requires exact-zero producer and checker exits and an exact-one
complete stdout JSON line from each.  Both are impossible with these frozen
owners, before any driver-side canonical admission, cross-comparison,
deadline accounting, or durable publication can succeed.  No fixed candidate
commands or future artifact names were emitted because binding them into a
knowingly unusable driver would create a false `COMPLETE` implementation.  No
raw, admitted, log, temporary, alias, or sentinel artifact was created.

## 5. Minimal truthful repair boundary

A successor commission should remain bounded and versioned:

1. Create new producer and checker owners; do not overwrite v6/v5.
2. Preserve the two role-specific containment events and all fixture meanings.
   Replace the impossible whole-trace `count == 1` predicate in both mutation
   gates with an exact rule that acknowledges row 4's two containment entries
   (successful manifest, rejecting receipt) while retaining count 1 for the
   other six registered rejection validators.  Equivalently, bind uniqueness
   to the terminal rejecting admission event and explicitly require the row-4
   manifest/receipt event order.
3. Change no authority pin, mutation constructor, first validator/stage/reason,
   revalidation, allocation, `RLIMIT_AS`, streaming, stdout-only, or conclusion
   flag.  Apply only truthful local version/schema labels.
4. Freeze the repaired source identities and conduct a fresh independent
   source audit of the exact delta and all seven routes.
5. Only after that audit, create the pinned driver with task382's canonical
   admission, serial resource/deadline discipline and fail-closed durable
   publication; then give that driver its own fresh independent audit before
   any GHA execution.

This repair does not cover rows 8--48, increase A4, construct a basis or lift,
prove fake, or produce an Ihara witness.

A4/V8 PINNED ROWS1-7 DRIVER:             INCOMPLETE
FROZEN OWNER AUTHENTICATION:             OPEN
INDEPENDENT PRODUCER/CHECKER ROUTES:      OPEN
CANONICAL RESULT/SELF-SEAL ADMISSION:     OPEN
RESOURCE / DEADLINE BOUNDS:               OPEN
DURABLE FAIL-CLOSED PUBLICATION:          OPEN
TASK379 PASS CLAUSES:                     REGRESSED
DRIVER EXECUTION:                         UNEXECUTED
FRESH INDEPENDENT DRIVER AUDIT:           REQUIRED
ROWS1-7 GHA:                              FORBIDDEN
FULL 48x2 SELFTEST:                       INCOMPLETE
ACTUAL A4:                                remains 1/3
LIFT / FAKE / IHARA:                      NONE

TASK382_R07_A4_V8_PINNED_ROWS1_7_DRIVER
