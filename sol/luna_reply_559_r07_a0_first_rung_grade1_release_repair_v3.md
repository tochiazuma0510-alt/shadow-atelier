# Luna Reply 559 — bounded release repair for the A0 first-grade engine v3

Role: Luna implementation only.  I made only the four Task559 release
repairs in the two versioned v3 programs and created this designated reply.
I did not run a real prepare, block, or merge phase, the 56-second
calibration, parallel Python, git, GHA, es7ops, or another agent.

## 1. Frozen source gate

The six sources named by Task559 were read in full before the v3 snapshot was
made.  The frozen v2 programs remain byte-for-byte unchanged:

```text
search/d972_r07_a0_first_rung_grade1_v2.py
  bytes  114,922
  sha256 df3aea9f49f5f76cd52f10923a38f75072eb2fc9cd4808578259ee48c4129ee4

search/check_d972_r07_a0_first_rung_grade1_v2.py
  bytes  55,010
  sha256 a11824ff42602698219ccd130e1a03d1fd4dcdc76a3cbece4a9ed816e0ac050d
```

`sol/sol_reply_558_audit_r07_a0_first_rung_grade1_engine_v2.md`
ends in the required `FIRST_GRADE_ENGINE_V2_PASS_AFTER_REPAIR`.  The new
programs use `d972.r07.a0.first-rung-grade1.v3`, the v3 state schema, and the
v3 certificate pathname.  The checker pins the final v3 producer SHA-256 and
does not import it or share a new helper.

## 2. R1 — complete NONMEMBER roster gates

The checker now calls `validate_nonmember_block_roster` at the beginning of
the NONMEMBER path, before packet or transition algebra.  For every block it
requires exact origin count, complete origin reductions, four transitions
per pivot, and one DAG node per pivot.  It type/range-checks every expression
pivot and requires each F3 coefficient to be exactly 1 or 2; DAG reductions
must refer only to earlier pivots.  This is a soundness gate, not telemetry,
and does not reproduce a producer pivot order.

The checker fixture reaches the gate with a rank-zero, one-origin block,
deletes its sole origin reduction, and requires the exact rejection.  Its
reported `"truncated_origin_reduction":"REJECTED"` is the reached canary.

## 3. R2 — strict streaming state validation

Both programs now validate the prepare, block, and merge state chain before
resume or downstream consumption.  The gates cover the complete current
input receipt and digest, fixed dimensions, phase/fixture semantics, exact
parent and ordered four-block bindings, characters and packet bindings,
origin/rank/attempt/queue/cardinality fields, DAG ranks/digests and pivot
rosters, merge roster and physical-rank data, exact terminal kinds, and exact
blob receipt shapes.

Blob receipts have an exact key set and validate filename shape, plain-integer
rows and widths, encoding, computed byte count, filesystem size, and SHA-256.
Authentication uses fixed 1 MiB chunks.  Consumption retains chunks from the
same authenticated stream rather than reading another full byte string.
The small authentication cache binds resolved path, size, declared digest,
mtime, and inode and rechecks file metadata around a retained read, so a
same-name replacement is not trusted merely because its size agrees.  Large
blobs are authenticated once when relevant to the phase boundary; no row
loop rescans unrelated packets or old lifts.

Before finalizing a provisional merge the producer explicitly requires the
stored ordered `block_sha256` list to equal the four loaded block digests.
Completed prepare/block/merge resumes use the same strict gates.  The
producer fixture constructs and consumes small prepare, four block, and merge
states through these validators and reports `"state_validators":"PASS"`.

## 4. R3 — idempotent certificate recovery

`build_terminal_certificate` is now the single deterministic certificate
builder.  It accepts only authenticated, nonfixture final MEMBER or NONMEMBER
states and reconstructs the exact producer pin, input/state chain, ordered
blocks, source ancestry, MEMBER degree-two receipt when applicable, and all
false downstream flags.  Runtime comes from the already sealed final merge
body's `elapsed_seconds`, so recovery cannot change canonical bytes.

`install_or_validate_terminal_certificate` atomically creates a missing
certificate and otherwise requires byte-for-byte canonical equality with the
same complete object.  Both fresh finalization and completed-final resume use
this builder.  Fixture and provisional terminals are rejected as public
finals.  The producer fixture writes a synthetic nonfixture final object only
to a temporary fixture pathname, invokes the same installer twice, and
requires identical objects and bytes; it reports
`"certificate_recovery":"PASS"`.  No repository certificate was created.

The independent checker reconstructs the expected complete canonical
certificate from the authenticated state chain and compares the entire
public object before retaining the existing direct MEMBER replay or complete
NONMEMBER terminal checks.

## 5. R4 — cap and progress coverage

The initial packet-origin ingestion loop now uses the existing
256-attempt-or-30-second progress cadence and resource gate, plus a check at
loop completion.  Prepare establishes its caps before seed evaluation and
the raw/canonical lower replays; those loops receive the caps, report/enforce
at their existing 256-term-or-30-second points, and enforce once on
completion.  The terminal lower replay receives the merge caps in the same
way.  These paths are statically load-bearing in production; no heavy
self-test, profiler, checkpoint framework, packed-algebra redesign, or
sorted-pivot change was introduced.

## 6. Bounded serial tests

The required commands were run in this order, with only one local Python
process at a time and bytecode directed to the temporary cache:

```powershell
$task559Cache = Join-Path $env:TEMP 'task559_pycache'
$env:PYTHONPYCACHEPREFIX = $task559Cache
python -B -m py_compile search/d972_r07_a0_first_rung_grade1_v3.py search/check_d972_r07_a0_first_rung_grade1_v3.py
python -B -u search/d972_r07_a0_first_rung_grade1_v3.py --fixture
python -B -u search/check_d972_r07_a0_first_rung_grade1_v3.py --fixture
```

Measured wall times were 0.315 s for `py_compile`, 1.387 s for the producer
fixture, and 0.998 s for the checker fixture.  All exited 0.  Exact fixture
output was:

```json
{"block_ranks": [1, 1, 1, 1], "certificate_recovery": "PASS", "elapsed_seconds": 0.4053643000079319, "fixture": "PASS", "merge_sha256": "922589779e328429e578b47ac607fe389724c4885009f94db2e1ba909dd4fcaa", "nonmonotone_leads": [5, 3], "packet_projector_ancestry": "PASS", "physical_rank": 4, "semantic_mutations_rejected": 3, "state_validators": "PASS", "terminal": "FIXTURE_MEMBER", "v443_actor_accumulation": "PASS"}
{"canonical_terms": 2622, "fixture": "PASS", "mutations_rejected": 3, "pinned_inputs": 18, "projectors": 16, "raw_terms": 3936, "truncated_origin_reduction": "REJECTED", "v443_actor_accumulation": "PASS"}
```

Thus the pre-existing v443 accumulation, nonmonotone-lead, packet-projector
ancestry, and three semantic-mutation canaries remain reached, alongside the
minimal R1–R3 fixture-state canaries.  No v3 bytecode exists under the
repository's `search/__pycache__`.

## 7. Output receipts and claim boundary

```text
search/d972_r07_a0_first_rung_grade1_v3.py
  bytes  138,202
  sha256 bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff

search/check_d972_r07_a0_first_rung_grade1_v3.py
  bytes  69,193
  sha256 67f56ee92aea7e17ce88303657ca519ee9539269eef44e6e5550da63d6a4a012

search/certs/d972_r07_a0_first_rung_grade1_v3.json
  ABSENT — no real phase or production terminal was run
```

There is no honest production rank, attempt count, runtime, resource peak,
membership result, or certificate.  The fixtures establish only bounded
implementation canaries.  Independent re-audit remains required and no
mathematical claim is promoted here.

FIRST-GRADE ENGINE v3: FOUR LOCAL RELEASE REPAIRS IMPLEMENTED; REAUDIT REQUIRED

FIRST-GRADE MEMBERSHIP: NOT COMPUTED

ORDER-54,432 / FULL-Q0 / A0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: NOT DECLARED

verified=false
