# Luna Reply 562 — minimal first-grade merge hot-loop repair v4

Role: Luna implementation only.  I implemented only the bounded Task562
recovery repair.  No real prepare, block, merge, mutation campaign, git, GHA,
parallel Python, or other agent was used.

## 1. Frozen inputs

Every input listed by Task562 was read in full before implementation.  Their
exact receipts are:

| frozen input | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_first_rung_grade1_v3.py` | 138,202 | `bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff` |
| `search/check_d972_r07_a0_first_rung_grade1_v3.py` | 69,193 | `67f56ee92aea7e17ce88303657ca519ee9539269eef44e6e5550da63d6a4a012` |
| `sol/luna_reply_559_r07_a0_first_rung_grade1_release_repair_v3.md` | 7,931 | `8ccb6304243e3045e2edb1cde5ce196b90ab7a4a8a4579c9c4f0da95d20ae976` |
| `sol/sol_reply_560_audit_r07_a0_first_rung_grade1_engine_v3.md` | 10,225 | `5ba42f2aadcf216a75df298d05657ce3fff27bbfd5c40226e6fcf2e7cee4ed64` |
| `.github/workflows/d972-r07-a0-first-rung-grade1-v3.yml` | 17,079 | `553315da1624c4184218a8e7cdaaa4996498da15890d10832c2d5d3dd5dc3917` |

The Task560 audit ends in `FIRST_GRADE_ENGINE_V3_PASS` and permits the exact
v3 producer/checker pair for production.  Task562 records that run
`33677346616` sealed one prepare and four exhausted character states.  I did
not access or recompute that production state in this task.

## 2. Preserved semantic and state contract

The v4 producer deliberately retains:

```python
SCHEMA = "d972.r07.a0.first-rung-grade1.v3"
STATE_SCHEMA = SCHEMA + ".state"
```

Thus the sealed v3 prepare/block bodies, HEAD files, content-addressed blobs,
input pins, dimensions, and parent digests remain direct inputs to the
unchanged `--merge <state-dir>` interface.  The checker retains the same
state schema as well.  Only the public certificate pathname changes to
`search/certs/d972_r07_a0_first_rung_grade1_v4.json`; its object schema stays
on the deliberate v3 compatibility contract.

No row traversal, lead selection, pivot ID, normalization, packed storage,
reduction expression, roster, ancestry DAG, terminal predicate, dual,
literal expansion, direct replay, or degree-two continuation was changed.
The CLI and all phase dispatch choices are identical to v3.  There is no
RREF, batch elimination, reordered pivot pass, split computation, or new
mathematical shortcut.

## 3. Monotone packed-byte cursor

`PackedEchelon.reduce_packed` no longer constructs
`work[cursor:] != 0`, calls `any`, and calls `argmax` after every pivot
elimination.  It advances a packed-byte cursor over zero bytes in Python.
At a nonzero byte it uses the unchanged `_PACKED_FIRST` table, looks up the
same actual lead in `lead_to_pivot`, records the same
`[pivot, coefficient]`, and applies the unchanged full-row `_PACKED_AXPY`
lookup.  If the lead has no pivot it stops immediately, exactly as v3 does.
After an elimination it deliberately revisits the same byte so a later trit
in that byte cannot be skipped.

The full-row AXPY was retained.  Therefore this repair does not add the
stronger prefix-invariant assumption that a suffix-only update would have
required.  Cursor monotonicity follows from the same normalized echelon
invariant already required by the v3 algorithm, and pivot IDs remain
insertion ordered even when lead order is nonmonotone.

## 4. Single lower reduction

The former acceptance/normalization tail of `PackedEchelon.insert` is now
the private `_accept_remainder(remainder, reductions)` helper.  Ordinary
`insert` performs exactly one `reduce_packed` and delegates its exact result
to that helper.  The lower-first merge path likewise passes the remainder
and expression it has already computed to the helper instead of invoking
`insert(physical_lower)` and repeating the reduction.

The helper preserves both possible record forms exactly.  A dependent row
returns only `accepted=False` and the ordered reduction expression.  An
accepted row retains its insertion-ordered pivot, actual lead, original
leading coefficient, scale, normalized packed bytes, and reduction list.

## 5. Bounded v3/v4 reducer equivalence

The producer fixture contains a tiny local copy of the frozen v3 reduction
algorithm.  On deterministic 12-trit rows, it compares v4 and the reference
after every operation for exact packed remainder bytes, ordered reductions,
complete acceptance record, lead list, and stored matrix bytes.

The six covered cases are:

1. an all-zero row and its rejected insertion;
2. a nonzero row whose lead has no registered pivot;
3. pivots at leads 5 and 6 in the same packed byte;
4. nonmonotone insertion leads `[5,3]`;
5. an accepted lead with coefficient 2 and normalization scale 2;
6. a dependent row reduced in actual-lead order by pivot IDs
   `[[1,1],[0,2],[2,2]]` and rejected.

The coefficient-two accepted case and dependent rejected case enter through
the already-reduced helper, so both halves of the lower-first repair are
reached.  The prior independent `[5,3]` canary, v443 accumulation canary,
projector ancestry canary, state/certificate canaries, and three semantic
mutations also remain reached.  Producer output reports:

```json
"reducer_equivalence": {"cases": 6, "dependent": "REJECTED", "status": "PASS"}
```

## 6. Versioned checker and serial commands

The checker is a direct versioned snapshot of the independent v3 checker.
Its algebra and validators were not weakened or redesigned.  It imports no
producer helper, pins the final v4 producer SHA-256
`1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4`,
accepts the deliberate v3 state schema, and reads only the v4 public
certificate pathname.

The required checks were run serially with bytecode directed outside the
repository:

```powershell
$task562Cache = Join-Path $env:TEMP 'task562_pycache'
$env:PYTHONPYCACHEPREFIX = $task562Cache
python -B -m py_compile search/d972_r07_a0_first_rung_grade1_v4.py search/check_d972_r07_a0_first_rung_grade1_v4.py
python -B -u search/d972_r07_a0_first_rung_grade1_v4.py --fixture
python -B -u search/check_d972_r07_a0_first_rung_grade1_v4.py --fixture
```

All three commands exited 0.  Measured outer wall times were 0.312 s,
1.211 s, and 0.859 s respectively.  Exact fixture output was:

```json
{"block_ranks": [1, 1, 1, 1], "certificate_recovery": "PASS", "elapsed_seconds": 0.3767138999828603, "fixture": "PASS", "merge_sha256": "a2bf587024a1e43f8994a7178d9ee609a239917466b360eb637236788f312f9f", "nonmonotone_leads": [5, 3], "packet_projector_ancestry": "PASS", "physical_rank": 4, "reducer_equivalence": {"cases": 6, "dependent": "REJECTED", "status": "PASS"}, "semantic_mutations_rejected": 3, "state_validators": "PASS", "terminal": "FIXTURE_MEMBER", "v443_actor_accumulation": "PASS"}
{"canonical_terms": 2622, "fixture": "PASS", "mutations_rejected": 3, "pinned_inputs": 18, "projectors": 16, "raw_terms": 3936, "truncated_origin_reduction": "REJECTED", "v443_actor_accumulation": "PASS"}
```

No v4 bytecode is present under the repository `search/__pycache__`.

## 7. Output receipts and claim boundary

```text
search/d972_r07_a0_first_rung_grade1_v4.py
  bytes  144,552
  sha256 1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4

search/check_d972_r07_a0_first_rung_grade1_v4.py
  bytes  69,184
  sha256 ffd78b41fc9f7a1f59925eb8f07db7278b704c3580bb7e8fa3a586e85db9fe06

search/certs/d972_r07_a0_first_rung_grade1_v4.json
  ABSENT — no real merge or production terminal was run
```

The only intended production action is a future parent-owned
`--merge <state-dir>` over the authenticated v3 prepare and four block
artifacts, followed by the independent v4 checker.  The implementation and
fixtures do not decide grade-one membership or promote any downstream claim.

FIRST-GRADE MERGE V4: MINIMAL HOT-LOOP REPAIR IMPLEMENTED; INDEPENDENT AUDIT REQUIRED

V3 PREPARE/BLOCK COMPATIBILITY: RETAINED

FIRST-GRADE MEMBERSHIP: NOT COMPUTED BY THIS TASK

ORDER-54,432 / FULL-Q0 / A0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: NOT DECLARED

verified=false
