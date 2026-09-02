# Sol Task 563 — narrow independent audit of first-grade merge hot-loop v4

Role: Sol(max) mathematical/static auditor.  Process every numbered section
in order.  This is a narrow release audit, not a new implementation campaign.
Do not modify producer/checker code, run production, use git/GHA, spawn another
agent, or request broader self-tests.  Write only the designated reply.

## 1. Read and authenticate the complete scope

Read in full and report byte/SHA-256 receipts for:

1. `sol/luna_task_562_r07_a0_first_grade_merge_hotloop_v4.md`
2. `sol/luna_reply_562_r07_a0_first_grade_merge_hotloop_v4.md`
3. `search/d972_r07_a0_first_rung_grade1_v3.py`
4. `search/check_d972_r07_a0_first_rung_grade1_v3.py`
5. `search/d972_r07_a0_first_rung_grade1_v4.py`
6. `search/check_d972_r07_a0_first_rung_grade1_v4.py`
7. `sol/sol_reply_560_audit_r07_a0_first_rung_grade1_engine_v3.md`

The production certificate
`search/certs/d972_r07_a0_first_rung_grade1_v4.json` must be absent.

## 2. Audit only the semantic diff

Confirm from the complete v3/v4 diff that production behavior changed only
in these bounded items:

1. a monotone packed-byte cursor replaces repeated suffix mask/any/argmax in
   `PackedEchelon.reduce_packed` while preserving the exact first-nonzero lead,
   reduction order, coefficient, full-row AXPY, and stop at a missing pivot;
2. `_accept_remainder` factors the old acceptance tail verbatim, and the
   lower-first merge uses the already computed remainder instead of reducing
   the same lower row twice;
3. the public certificate pathname is versioned to v4;
4. all other added code is fixture-only, version wording, or the explicit
   v3 state-compatibility comment.

Check the same-byte case carefully: after an elimination the current byte is
revisited, so a later trit cannot be skipped.  Check the cursor invariant
against both rows freshly inserted by v4 and rows loaded from the sealed v3
block artifacts.  Reject any change to row universe, aggregation, pivot IDs,
DAG expressions, terminal predicate, dual, ancestry expansion, replay, or
next-degree residual.

## 3. State/certificate/checker compatibility

Confirm that v4 deliberately retains the v3 `SCHEMA`/`STATE_SCHEMA`, accepts
the exact sealed v3 prepare and four block states, and changes neither their
body nor blob contract.  Confirm that a v4 terminal certificate binds the v4
producer hash and uses the v4 pathname, and that the independent v4 checker
pins that exact producer and otherwise preserves the complete v3 checker.
There must be no producer import or shared new helper in the checker.

## 4. Bounded checks and performance relevance

Run serially only:

```powershell
$task563Cache = Join-Path $env:TEMP 'task563_pycache'
$env:PYTHONPYCACHEPREFIX = $task563Cache
python -B -m py_compile search/d972_r07_a0_first_rung_grade1_v4.py search/check_d972_r07_a0_first_rung_grade1_v4.py
python -B -u search/d972_r07_a0_first_rung_grade1_v4.py --fixture
python -B -u search/check_d972_r07_a0_first_rung_grade1_v4.py --fixture
```

Confirm the six-case reducer-equivalence gate is reached and compares exact
remainders, ordered reductions, acceptance records, leads, and matrix bytes.
Do not add calibration, profiling, production rows, mutation campaigns, or
heavy parallel work.  State qualitatively whether removing one suffix scan
per reduction and one complete lower reduction is genuinely load-bearing for
the observed merge; do not demand a runtime promise.

## 5. Verdict and exact claim boundary

Write only:

`sol/sol_reply_563_audit_r07_a0_first_grade_merge_hotloop_v4.md`

Choose exactly one terminal:

`FIRST_GRADE_MERGE_V4_PASS`

or

`FIRST_GRADE_MERGE_V4_STOP`

PASS authorizes one parent-owned GHA recovery merge over the already saved
v3 prepare/block artifacts followed by the v4 checker.  It does not authorize
rebuilding those five phases and does not itself promote a mathematical
result.  End with the exact v220 boundary:

`FIRST RUNG: 0/6 GRADES DECIDED UNTIL A PRODUCTION CHECKER TERMINATES`

`A0: 0/1 ACTUAL`

`ORDER-54,432 / FULL-Q0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: NOT DECLARED`

`verified=false`
