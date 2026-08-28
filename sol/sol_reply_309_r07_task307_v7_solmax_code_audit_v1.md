# Sol(max) reply 309 - task307/v7 independent adversarial static code audit

## Verdict

**PASS (fail-closed static source audit only).**  The v7 checker separates
canonical mutation construction and resealing from the exception region that
interprets semantic rejection, retains a structured verdict for every one of
the 19 owners, and individually requires all mutation predicates before its
19/19 summary.  The driver now enforces literal exact-one markers, quotes the
shell expansions used by `test`, and has a reachable typed production
`STATIC_BLOCKED` route.  The three fatal v6 findings in
`sol/sol_reply_306_r07_task304_v6_solmax_code_audit_v1.md` are therefore
repaired at source level.

No Python, Node, GAP, GHA, workflow, network, or git command was run.  Neither
SELFTEST nor production was executed.  All ranks, mutation routes, and shell
routes below are deductions from the five named v7 files.  In particular:

```text
EXECUTION:                         UNEXECUTED
PRODUCER MUTATIONS ACTUAL:         0/19
CHECKER MUTATIONS ACTUAL:          0/19
SELFTEST PRODUCER/CHECKER ACTUAL:  0/2
ACTUAL A5:                         0/3
ACTUAL A6:                         0/3
LIFT / FAKE / IHARA CONCLUSION:    NONE
```

## 1. Scope, identities, versions, and static boundary - PASS

All five task307 paths named at task lines 13--17 exist.  Independent
read-only byte/SHA-256 recomputation gives:

| v7 path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_joint_slice_kernel_general_v7.py` | 11670 | `279ab542b22ea6756fee48b7da8c2d9e0142e2489def80b6d071e9aed67ff1b6` |
| `crosscheck/check_d972_r07_joint_slice_kernel_general_v7.py` | 23677 | `148ddb801939f2263421e1cfb1e942695ad36eba74d2cb3c27c4e9ed30e3aa35` |
| `search/d972_r07_joint_slice_kernel_general_gha_driver_v7.g` | 4861 | `1c9af2fbff3fc89be1f75b3c17daa6d636543d19b1c8bee4bbcb5e48cc49e441` |
| `search/certs/d972_r07_joint_slice_kernel_general_selftest_v7_20260828.json` | 10317 | `c4d616b758f83379307f5778cbb46794d7aa0e4b651d6072163ce9a4c34de4e4` |
| `sol/luna_reply_307_r07_task304_solmax_reject_repair_v7.md` | 4200 | `2df8c81c0ed9295368092718c00cbd39b6360507c04c6066cc459fe3002bfee5` |

The three driver pins at driver line 15 equal the current producer, checker,
and fixture bytes and hashes.  The GAP driver has zero bytes above ASCII 127.
Producer lines 8--13, checker lines 11--16, fixture lines 2--3 and 14, and
driver lines 6--15 consistently use v7 schemas, seals, paths, and markers.

The Luna reply reports all five byte lengths and the four embeddable hashes at
lines 9--15.  Its own final hash is necessarily supplied externally above:
embedding an ordinary digest into the bytes being digested would change that
digest, exactly as reply lines 17--19 state.  This is not a driver-pin gap;
task304 commissions driver pins for producer, checker, and fixture only.

Because git is expressly forbidden, this is an audit of the five named paths,
not a repository-wide change-set attestation.  No v1--v6 file was used as a
current input; task304/v6 was read only as the commissioned regression
boundary.

Production remains typed and fail-closed.  Producer lines 147--149 select the
literal `STATIC_BLOCKED:actual typed matrices are not staged` envelope without
entering SELFTEST.  Checker lines 338--353 independently select and emit the
same value.  Driver lines 31--36 run producer before checker, require their
four output files to be nonempty, require exactly one of each literal terminal,
extract nonempty normalized strings, and compare them.  Driver line 38 writes
the sole sentinel only afterward.  Thus the v6 unquoted-terminal dead path is
absent and the production `STATIC_BLOCKED` sentinel route is statically
reachable, while actual matrices remain unstaged.

## 2. Fatal checker repair and structured verdicts - PASS

The repaired exception boundary is exact:

- Checker lines 217--227 initialize the per-owner record with `owner`,
  `canonical_changed`, `reseal_passed`, `semantic_oracle`,
  `semantic_oracle_reached`, `semantic_rejection_seen`, `rejected`,
  `rejection_stage`, and `rejection_reason`.
- Unknown owners fail at line 228; any impossible roster/partition gap also
  fails at line 269, in both cases before either semantic `try`.
  Fixture mutations are constructed at lines 229--240, canonical difference
  is required at line 241, and resealing is required at lines 243--245.
  Receipt mutations are constructed at lines 259--269, canonical difference
  is required at line 270, and resealing is required at lines 271--276.
- Only the call to `independent_terminal` is inside the fixture exception
  region (lines 246--255), and only the call to `replay` is inside the receipt
  exception region (lines 277--286).  A no-op, failed reseal, indexing failure,
  construction failure, or unknown owner therefore propagates rather than
  becoming `semantic_rejection_seen=True`.
- Rejection stage and reason are bound at lines 251--257 and 282--288.  An
  oracle that returns normally produces `rejected=False`, which is fatal to
  the caller.
- The caller iterates the exact roster at lines 323--327 and, for each owner
  separately, requires owner identity, canonical change, reseal, oracle reach,
  semantic rejection, and final rejection at lines 328--333.  It appends only
  after those gates (line 334), requires the final roster length at line 335,
  and only then forms the attempted/rejected summary at line 336.

The 19 individual checker verdict routes are all non-noop and have the
following first static semantic rejection.  Every fixture-owner rejection is
recorded with stage `independent_terminal` at lines 251--254; every
receipt-owner rejection is recorded with stage `replay` at lines 282--285.

| owner | literal mutation | designated oracle and first rejecting gate |
|---|---|---|
| `field_modulus` | checker line 230 | `independent_terminal`; typed-field gate, line 182 |
| `theta_seed` | line 231 | `independent_terminal`; seed/binding control, line 186 |
| `theta_action` | line 232 | `independent_terminal`; action-owner binding, line 184 |
| `z_action` | line 233 | `independent_terminal`; action-owner binding, line 184 |
| `eta_action` | line 234 | `independent_terminal`; action-owner binding, line 184 |
| `D_entry` | line 235 | `independent_terminal`; map-owner binding, line 185 |
| `O_entry` | line 236 | `independent_terminal`; map-owner binding, line 185 |
| `C_entry` | line 237 | `independent_terminal`; map-owner binding, line 185 |
| `action_order` | line 238 | `independent_terminal`; action-order control, line 186 |
| `premature_C` | line 239 | `independent_terminal`; post-`C` control, line 186 |
| `target` | line 240 | `independent_terminal`; terminal semantic gate, line 209 |
| `seed_index` | line 259 | `replay`; seed replay, line 152 |
| `parent` | line 260 | `replay`; seed replay, line 152 |
| `row_theta` | line 261 | `replay`; typed-row replay, line 150 |
| `left_kernel` | lines 262--264 | `replay`; kernel-basis independence, line 162 |
| `Hd1` | line 265 | `replay`; full Hd1 span equality, line 167 |
| `member_ancestry` | line 266 | `replay`; member equations, line 171 |
| `dual` | line 267 | `replay`; dual equations, line 177 |
| `terminal` | line 268 | `replay`; receipt/case terminal equality, line 141 |

The case routing is fixed at checker lines 323--327.  In particular, the
`target` mutation changes the fixture-line-9 target from `[0,1]` to `[1,0]`;
the sole closed row has `D`-image `[1,0]` and zero `C`-image, so the mutated
target is MEMBER while its case terminal remains NONMEMBER.  This reaches the
named semantic gate rather than merely a structural failure.  The receipt
mutations use fixture cases with the required rows, two-element kernel basis,
member witness, or dual, as declared at fixture line 6 and instantiated at
lines 8--9.

The inaccurate v6 metadata is also repaired.  Producer controls are read and
individually required at checker lines 320--322; line 336 truthfully emits
`producer_mutation_controls_checked: True`, while the separately generated
records remain under `independent_mutation_controls`.  The checker imports
only standard-library modules at lines 3--8 and never imports the producer.

## 3. Preserved task304 algebraic and mutation contract - PASS

The accepted v6 structure is preserved with v7 identities:

- Fixture lines 8--12 contain exactly the five named cases.  Fixture line 8
  contains two seeds and distinct actions `m` and `n` with distinct matrices.
- Producer lines 81--90 close the joint `(z,eta)` rows by rank and apply `C`
  only after closure before taking a left kernel.  Checker lines 113--134
  reconstruct the same joint closure in reverse action order, enumerate the
  complete nonzero left kernel, and apply `C` at lines 130--131.
- Producer line 100 keeps `kernel_dim=len(basis)` separate from
  `full_nonzero_kernel_cardinality=3^d-1`.  Checker lines 157--164 check the
  receipt basis, its independence, full-kernel cardinality, and full spanning;
  line 178 reports dimension and cardinality separately.
- Closure/span and row-rank equality are replayed at checker lines 142--147;
  typed rows and complete seed/action ancestry at lines 148--156; kernel and
  Hd1 content at lines 157--167; MEMBER equations and ancestry at lines
  168--172; and NONMEMBER dual existence and equations at lines 173--177.
- Producer wrong-seal rejection is independently required at producer lines
  130--133.  Checker lines 300--306 construct and reject their own wrong,
  nonempty seal; checker line 309 additionally requires the producer canary.

Static evaluation of the literal matrices gives exactly the fixture-line-6
expectations:

| case | closure rank | kernel dim `d` | full nonzero `3^d-1` | Hd1 rank | terminal |
|---|---:|---:|---:|---:|---|
| `nonzero-member` | 2 | 2 | 8 | 2 | `MEMBER` |
| `outside-nonmember` | 1 | 1 | 2 | 1 | `NONMEMBER` |
| `zero-member` | 1 | 1 | 2 | 0 | `MEMBER` |
| `zero-nonmember` | 1 | 0 | 0 | 0 | `NONMEMBER` |
| `post-c-cancel` | 2 | 1 | 2 | 1 | `MEMBER` |

These are source/fixture expectations, not observed results.  They retain both
the dimension-two/cardinality-eight canary and the zero-dimensional/zero-
cardinality canary.

The producer's own 19-owner path remains fail-closed.  Its roster is line 14,
literal mutations are lines 101--122, canonical difference and reseal are
outside the semantic `try` at lines 123--125, and only `compile_case` is
interpreted at lines 126--127.  Every individual result is required before the
aggregate at lines 139--143.  The field/seed/action/map/control mutations reach
lines 66--80; `target` and `dual` reach membership line 94; and the terminal
mutation reaches the exact enum at line 93.  Thus producer controls are
statically sound but remain 0/19 actually executed.

## 4. Explicit Boolean `require` audit - PASS

`require` rejects anything not identical to `True` in producer lines 54--55
and checker lines 87--89.  All 32 producer call sites and all 78 checker call
sites were inspected.  Each argument is an equality/inequality, `in`
comparison, `isinstance`/`type` comparison, explicit `is True`/`is not None`,
`all`/`any` Boolean (with `not` where required), or a conjunction of those.
The potentially empty dual roster is explicitly converted with `bool(duals)`
at checker line 175.  No raw string, list, dictionary, integer count, or other
truthy payload is passed to `require`; the v4 truthy-seal class of defect is
absent.

## 5. Driver exact-one, quoting, equality, and sentinel audit - PASS

- Driver lines 16--18 require nonempty pinned bytes and exact length/SHA before
  shell creation.  Line 19 rejects all six stale receipt, verdict, producer
  log, checker log, generated shell, and sentinel paths.
- The generated shell begins with `set -euo pipefail` at line 21.  SELFTEST
  runs producer before checker at lines 24--28.  Production does the same at
  lines 31--32.
- SELFTEST producer and checker exact lines are counted with `grep -Fxc`, the
  emitted count is captured, and it is compared with literal `1` at lines 25
  and 28.  Production applies the same exact-one construction to both complete
  space-containing terminal lines at lines 34--35.  No count is discarded
  through `>/dev/null`.
- Every shell expansion used by `test` is double-quoted: the four captured
  `grep` counts at lines 25, 28, 34, and 35, and the normalized terminal
  variables at lines 29 and 36.  Paths passed to `test -s` are quoted at lines
  26, 29, and 33.
- SELFTEST binds the documented common normalization `SELFTEST_COMPLETE` and
  requires both values nonempty and equal at line 29.  Production extracts the
  two suffixes with anchored literal prefixes, then requires both nonempty and
  exactly equal at line 36.
- The only sentinel write is the `printf` at line 38, after every mode-specific
  gate.  The same line exact-counts the sentinel as `1`; lines 39--41 cannot
  report driver PASS unless that file exists.

This repairs v6 F2 and F3 rather than merely relying on the pinned programs'
intended one-line behavior.

## 6. Reply boundary and final accounting - PASS

Reply lines 23--43 accurately describe the precondition/oracle separation,
structured fields, hard-failure cases, individual owner gates, and corrected
metadata.  Lines 47--56 give the exact driver routes.  Lines 61--66 report all
five expected tuples, and lines 75--80 mark both mutation suites, both
wrong-seal canaries, SELFTEST, and production observation as `UNEXECUTED` or
static-only.  Lines 83--84 correctly keep actual A5 and A6 at 0/3 and declare
no lift, fake certificate, or Ihara result.

```text
TASK307/V7 STATIC CODE AUDIT:               PASS
V6 F1 CHECKER EXCEPTION-BOUNDARY DEFECT:     REPAIRED STATICALLY
V6 F2 PRODUCTION QUOTING/REACHABILITY:       REPAIRED STATICALLY
V6 F3 EXACT-ONE MARKERS:                     REPAIRED STATICALLY
PRODUCER MUTATION GATE:                      19/19 REQUIRED; 0/19 ACTUAL
INDEPENDENT STRUCTURED CHECKER GATE:         19/19 REQUIRED; 0/19 ACTUAL
WRONG-SEAL CANARIES:                         2 REQUIRED; 0 ACTUAL
SELFTEST / PRODUCTION EXECUTION:              UNEXECUTED / UNEXECUTED
PRODUCTION STATIC_BLOCKED ROUTE:             PASS STATICALLY
ACTUAL A5 / ACTUAL A6:                       0/3 / 0/3
LIFT / FAKE / IHARA RESULT:                  NONE DECLARED
```

`TASK309_R07_TASK307_V7_SOLMAX_CODE_AUDIT_PASS_UNEXECUTED`
