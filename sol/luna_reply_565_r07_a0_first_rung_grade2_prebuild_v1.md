# Luna Reply 565: target-independent first-rung grade-two prebuild (v1)

`GRADE2_PREBUILD_V1_IMPLEMENTED_AUDIT_REQUIRED`

## 1. Scope and mathematical binding

Only the three Task565-designated files were created or edited.  No production
phase, GHA job, git operation, certificate generation, or membership reduction
was run.  The implementation pins v450 together with its mandatory v451 repair,
the Task565 instruction, v448, and the Task566 audit reply.  In particular it
implements v451 (1.3), (2.1)--(2.7), the gates of v451 section 3, and only the
inactive join boundary of v451 section 4.

The implementation keeps the full filtered word-sum projector `P_chi` separate
from the pure-grade projector `e_lambda`; it does not assume that the full
precision word sum is idempotent.  The global `B1` order is exactly all four
lifted-old blocks followed by all four `H^[1]` blocks.  Each original-seed
relation is assembled by summing all four old records and all four character
block origin reductions with their global offsets.

## 2. Producer

`search/d972_r07_a0_first_rung_grade2_prebuild_v1.py` provides:

- canonical, atomic, parent-linked prepare / four block / module state phases;
- strict authentication of the grade-one v3-compatible split state without a
  merge state or target coefficients;
- direct precision-one replay, compact old/new DAG ancestry, exact precision-two
  lifts, and the minimal `44 + 4*rank(B1)` defect roster;
- four width-36,288 character closures, with all six degree-two monomials kept
  coupled, followed by the lower-first widths 32,260 / 48,384 module merge;
- exact v442 extension/crossed-cochain/negative-column, all translated PB3,
  both PB4 blocks, filtration/aggregation, and integral-exponent preflight
  gates; and
- an inactive `--join` path which requires a checked grade-one MEMBER state and
  certificate, reconstructs literal `c1`, independently recomputes the complete
  degree-two target-minus-replay residual, and stops without reducing it.

The sole successful production terminal accepted or emitted is
`FIRST_RUNG_GRADE2_MODULE_READY`.  Resource exhaustion seals
`UNKNOWN_RESOURCE`; it never becomes MEMBER or NONMEMBER.

Large row owners are content-addressed packed streams or file-backed stores.
The producer consumes source character blocks one at a time and streams the
physical lower-grade companion, so it does not materialize four source owners
or duplicate physical rows together.

## 3. Resource ceilings (not estimates)

The state records the supplied ceilings only:

- `R_old = 2014`, `H1 = 6045`, `rank(B1) = 8059`;
- exact minimal defect roster `44 + 4*8059 = 32280`;
- each grade-two character rank at most `36288` and queue attempts at most
  `177432`;
- joint physical input rows at most `153211`;
- one packed source-block basis at most `329204736` bytes; and
- joint packed physical-input ceiling `1853240256` bytes before Python
  metadata.

## 4. Independent checker

`search/check_d972_r07_a0_first_rung_grade2_prebuild_v1.py` does not import the
producer.  It independently implements canonical state/blob authentication,
base-three packing, affine and degree-two polynomial action, the two projector
levels, aggregation, split-`B1` reconstruction, all old/new DAG identities,
the complete defect packets, four closures, and lower/grade module containment.
It compares the complete preflight and compact ancestry objects against its own
reconstruction.  Large blobs are streaming-hashed once at consumption and then
read through file-backed rows.  Sealed echelon leads are independently checked
once and indexed for subsequent containment reductions.

The checker accepts only the target-independent module-ready terminal.  It does
not test grade-two membership and does not emit a certificate.

## 5. Bounded serial fixtures

Commands were run serially with bytecode cache redirected outside the
repository:

```powershell
$env:PYTHONPYCACHEPREFIX = Join-Path $env:TEMP 'task565-pycache'
python -m py_compile search/d972_r07_a0_first_rung_grade2_prebuild_v1.py search/check_d972_r07_a0_first_rung_grade2_prebuild_v1.py
python -B search/d972_r07_a0_first_rung_grade2_prebuild_v1.py --fixture
python -B search/check_d972_r07_a0_first_rung_grade2_prebuild_v1.py --fixture
```

Results:

- `py_compile`: PASS (`0.41 s` wall time);
- producer fixture: PASS (`4.80 s` reported, `5.21 s` wall time);
- checker fixture: PASS (`0.93 s` reported, `1.18 s` wall time);
- both fixtures cover the nine Task565 cases, including seven semantic mutation
  rejections and seven deterministic phase-resume checks.

## 6. Output identities

| File | Bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_first_rung_grade2_prebuild_v1.py` | 145917 | `acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8` |
| `search/check_d972_r07_a0_first_rung_grade2_prebuild_v1.py` | 80693 | `fc6f9976b4e3164d4dff31c05256750ddb4758856f39ac5b1fceb43249fbdecf` |

No real grade-two certificate file was produced, and no MEMBER or NONMEMBER
result was produced.

## 7. Claim boundary

```text
GRADE ONE: terminal still external
GRADE TWO MODULE: executable candidate only
GRADE TWO MEMBER/NONMEMBER: not run
ORDER-54,432 / FULL-Q0 / A0 / COMMON / COFINAL LIFT: not declared
FAKE / IHARA: not declared
verified=false
```
