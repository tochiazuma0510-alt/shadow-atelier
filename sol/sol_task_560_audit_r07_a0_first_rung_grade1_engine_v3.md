# Sol Task 560 — narrow release audit of A0 first-grade engine v3

Role: Sol(max), independent adversarial audit. Process every numbered section
in order. This is a **diff-limited release audit**, not a new mathematical
design review. Task558 already accepted the affine/Fourier mathematics and
identified exactly R1--R4. Decide only whether Task559 closes those four
release defects without changing the accepted finite question.

## 1. Frozen inputs

Read in full:

1. `sol/sol_reply_558_audit_r07_a0_first_rung_grade1_engine_v2.md`
2. `sol/luna_task_559_r07_a0_first_rung_grade1_release_repair_v3.md`
3. `sol/luna_reply_559_r07_a0_first_rung_grade1_release_repair_v3.md`
4. `search/d972_r07_a0_first_rung_grade1_v2.py`
5. `search/check_d972_r07_a0_first_rung_grade1_v2.py`
6. `search/d972_r07_a0_first_rung_grade1_v3.py`
7. `search/check_d972_r07_a0_first_rung_grade1_v3.py`

Freeze the new receipts:

```text
producer v3  138,202 bytes
bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff

checker v3   69,193 bytes
67f56ee92aea7e17ce88303657ca519ee9539269eef44e6e5550da63d6a4a012

Task559 reply 7,931 bytes
8ccb6304243e3045e2edb1cde5ce196b90ab7a4a8a4579c9c4f0da95d20ae976
```

Require the v2 hashes in Task558 and confirm that the v3 checker pins the
exact v3 producer. The production certificate
`search/certs/d972_r07_a0_first_rung_grade1_v3.json` must be absent.

## 2. Audit only R1--R4

Inspect the v2-to-v3 diffs and the load-bearing call sites. Establish or reject
each item:

- **R1:** every NONMEMBER block has the complete origin/transition/DAG roster,
  with pivot and F3 coefficient type/range checks before algebra; the truncated
  origin canary reaches this gate.
- **R2:** prepare/block/merge consumption and completed resume authenticate the
  exact current input receipt, state parent/dimensions/cardinalities and relevant
  blobs by bounded streaming; provisional merge binds the ordered four exact
  block digests. Authentication must not rescan a large blob inside a row loop.
- **R3:** after an authenticated final merge, a missing certificate is rebuilt
  deterministically and an existing certificate must equal the complete
  canonical expected object. Fixture and provisional terminals cannot be
  published. Check specifically the crash-after-HEAD-before-certificate path.
- **R4:** packet ingestion and lower replay are inside the advertised resource
  and progress gates, including a completion check.

Also confirm that v3 did not alter the accepted affine formulas, finite row
universe, pivot policy, ancestry semantics, or terminal mathematical criteria.
Do not request an optimization, profiling framework, new checkpoint scheme,
full mathematical re-audit, mutation campaign, or broader tests unless a
specific soundness defect in this diff forces it.

## 3. Bounded independent checks

Run only these serial, seconds-scale checks with bytecode outside the repo:

```powershell
$task560Cache = Join-Path $env:TEMP 'task560_pycache'
$env:PYTHONPYCACHEPREFIX = $task560Cache
python -B -m py_compile search/d972_r07_a0_first_rung_grade1_v3.py search/check_d972_r07_a0_first_rung_grade1_v3.py
python -B -u search/d972_r07_a0_first_rung_grade1_v3.py --fixture
python -B -u search/check_d972_r07_a0_first_rung_grade1_v3.py --fixture
```

Do not run a real prepare, block, merge, calibration, parallel Python, git,
GHA, es7ops, or another agent. Do not modify either program. Temporary files
remain outside the repository.

## 4. Decision and sole output

Create only
`sol/sol_reply_560_audit_r07_a0_first_rung_grade1_engine_v3.md`.
Record exact hashes, commands, outputs, timings, and concise evidence for each
R1--R4 decision.

If all four repairs close and no regression is found, end exactly with:

`FIRST_GRADE_ENGINE_V3_PASS`

`GHA_RELEASE: ALLOWED`

`FIRST-GRADE MEMBERSHIP: NOT COMPUTED`

`ORDER-54,432 / FULL-Q0 / A0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: NOT DECLARED`

`verified=false`

Otherwise end with `FIRST_GRADE_ENGINE_V3_STOP`, name only the concrete
blocking defect and the smallest necessary repair, and keep GHA release
forbidden.
