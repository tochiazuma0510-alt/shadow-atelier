# Sol(max) reply 314 - task312/v8 independent static code and performance audit

## Verdict

**PASS for the load-bearing v8 implementation (static source audit only).**
The two malformed v7 rows are repaired, both programs place a literal
five-case/six-pair preflight before case work, every advertised expected tuple
agrees with a manual calculation from the fixture, both 19-owner mutation
suites remain fail-closed, and the pinned exact-one driver has a reachable
typed production `STATIC_BLOCKED` route.  No avoidable unbounded or repeated
work was introduced.

There is one **non-load-bearing reporting defect**: Luna reply line 14 reports
its own current length as 4698 bytes, whereas the named file is 4703 bytes.
That row of the reply's identity table is inaccurate by 5 bytes.  The reply is
not a driver input or pin, so this does not weaken the producer, checker,
fixture, driver, or execution gate; it is not an implementation defect.

No Python, Node, GAP, GHA, workflow, network, or git command was run.  None of
the five v8 paths was executed.  Byte/hash reading and all algebra below were
read-only/static.  Consequently all execution accounting remains:

```text
EXECUTION:                         UNEXECUTED
PRODUCER MUTATIONS ACTUAL:         0/19
CHECKER MUTATIONS ACTUAL:          0/19
SELFTEST PRODUCER/CHECKER ACTUAL:  0/2
PRODUCTION ACTUAL:                 UNEXECUTED
ACTUAL A5 / ACTUAL A6:             0/3 / 0/3
LIFT / FAKE CERTIFICATE / IHARA:   NONE
```

## 1. Current identities and pin closure - PASS

Independent read-only byte/SHA-256 inspection of the five commissioned paths
gives:

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_joint_slice_kernel_general_v8.py` | 12999 | `18bd8b83d3ceb3d7091e5bcf4eaaf0b4fbdfdcc6f1e5299bd44ac84b8f7f5877` |
| `crosscheck/check_d972_r07_joint_slice_kernel_general_v8.py` | 24993 | `6cd630b82ee1e4118b77f90b12b7186a9c0d2b604814bdd4f8d2b3e16b84376d` |
| `search/d972_r07_joint_slice_kernel_general_gha_driver_v8.g` | 4860 | `e78fa0d72181bf4420065fd08f020d35d85107154cf053c152656b8f30940b6c` |
| `search/certs/d972_r07_joint_slice_kernel_general_selftest_v8_20260828.json` | 10322 | `df30c2e965e6306731c84423ee6c397dc3150b7ac0373147de50e9c437fab864` |
| `sol/luna_reply_312_r07_task307_fixture_repair_v8.md` | **4703** | `776684656f49a93ccac28c895c0c703e127adb67e4a981c8195874f56a483677` |

Driver line 15 pins the current producer, checker, and fixture to exactly the
first, second, and fourth rows above.  All three byte and digest pairs match.
The driver itself has zero non-ASCII bytes.  Source schemas, fixture seal and
path, output paths, success markers, production prefixes, and sentinel are v8;
there is no stale v7 identity in the load-bearing four paths.

The first four Luna identity rows (lines 10--13) are exact.  Its line-14
`reply 4698` claim is not exact for the current bytes.  Omitting a
self-referential SHA is reasonable, but a byte length is still measurable;
the 5-byte discrepancy is therefore a reply-precision failure, not a
self-reference exception.

## 2. Literal repair and all-case preflight - PASS

Fixture line 8 now has the repaired zero-based `A_E_binding` rows 6 and 7:

```text
row 6 = [0,0,0,0,0,0,1,0,0,0,0]
row 7 = [0,0,0,0,0,0,0,1,0,0,0]
```

Each has eleven entries and is byte-for-value equal to the corresponding
`A_E` row.  Direct inspection of every literal pair gives the complete 30-pair
matrix below; `=` means literal list equality, with both sides independently
having the displayed dimensions.

| case | `A_theta/binding` | `A_Z/binding` | `A_E/binding` | `D/binding` | `O/binding` | `C/binding` |
|---|---|---|---|---|---|---|
| `nonzero-member` | `= 2x2` | `= 2x2` | `= 11x11` | `= 2x2` | `= 11x2` | `= 1x11` |
| `outside-nonmember` | `= 2x2` | `= 2x2` | `= 11x11` | `= 2x2` | `= 11x2` | `= 1x11` |
| `zero-member` | `= 2x2` | `= 2x2` | `= 11x11` | `= 2x2` | `= 11x2` | `= 1x11` |
| `zero-nonmember` | `= 2x2` | `= 2x2` | `= 11x11` | `= 2x2` | `= 11x2` | `= 1x11` |
| `post-c-cancel` | `= 2x2` | `= 2x2` | `= 11x11` | `= 2x2` | `= 11x2` | `= 1x11` |

Producer lines 63--87 and checker lines 299--323 encode exactly those six
pairs and fixed shapes.  For each side they also require a list of the exact
row/column counts and entries with `type(x) is int` and `0 <= x < 3`.
Producer `parse_fixture` calls the preflight at lines 89--91 before
`selftest` can call `compile_case`; checker `run` calls it at lines 326--327
before receipt loading or any `replay`.  Neither preflight reads
`expected_cases`; expectations cannot waive a binding or dimension failure.

## 3. Manual reconstruction of every expected tuple - PASS

Here the tuple order is
`(closure_rank, kernel_dim, 3^d-1, Hd1_rank, terminal, member_theta, dual)`.
Writing `e1=(1,0)` and `e2=(0,1)`, literal arithmetic over `F_3` gives:

| case | manual closure / post-C calculation | full expected tuple |
|---|---|---|
| `nonzero-member` | The two seeds already give independent flat rows with `z=e1,e2`; `C eta=(0,0)`.  The coefficient kernel has basis `(1,0),(0,1)` and `Hd1=<e1,e2>`.  Target `(1,1)` uses theta `(1,1)`. | `(2,2,8,2,MEMBER,[1,1],null)` |
| `outside-nonmember` | The sole row has `z=e1`, `eta=occurrence00`, and zero C-image.  Kernel basis `(1)` gives `Hd1=<e1>`.  Target `e2` is outside, and `(0,1)` annihilates `e1` while pairing to 1 with `e2`. | `(1,1,2,1,NONMEMBER,null,[0,1])` |
| `zero-member` | The sole flat row is nonzero through `eta`, but `D theta=0` and `C eta=0`.  Kernel basis `(1)` maps to zero in `Hd1`; the zero target has the lex-first zero theta witness. | `(1,1,2,0,MEMBER,[0,0],null)` |
| `zero-nonmember` | The sole flat row is again nonzero through `eta`, while its C-image is 1.  The coefficient kernel and `Hd1` are empty.  Target `e1` is outside and dual `(1,0)` pairs to 1. | `(1,0,0,0,NONMEMBER,null,[1,0])` |
| `post-c-cancel` | The seed and swap action give theta/z rows `e1,e2`; their C-images are `(1,1)`.  Producer kernel basis `(2,1)` gives `Hd1=<(2,1)>`; target `(1,2)=2(2,1)` and the combined theta is `(1,2)`. | `(2,1,2,1,MEMBER,[1,2],null)` |

These five calculations agree entry-for-entry with fixture line 6, including
the member witnesses and nonmember duals, not only the advertised ranks.  The
checker enumerates both nonzero multiples when representing a one-dimensional
kernel, but its rank/span replay makes the same dimensions and `Hd1` spaces.
These are static deductions, not observed terminals.

## 4. Producer and checker mutation gates - PASS

Producer lines 128--154 construct all mutations.  Canonical difference and
resealing are required at lines 150--152, outside the `compile_case` exception
region at lines 153--154.  Thus a no-op, unknown owner, construction failure,
or reseal failure cannot be counted as semantic rejection.  Selftest lines
166--170 invokes exactly the 19-owner roster on the fixed
`outside-nonmember` case, requires every individual rejection, and only then
forms the aggregate.

Checker lines 212--289 similarly keep construction, canonical difference,
and resealing outside the two semantic `try` regions.  Lines 350--360 select
the required cases and individually require owner identity, canonical change,
reseal, oracle reach, semantic rejection, and final rejection before append;
line 362 separately requires all 19 records.

The first static rejecting gates for every owner are:

| owner | producer `compile_case` | independent checker |
|---|---|---|
| `field_modulus` | typed modulus, line 93 | `independent_terminal` typed field, line 182 |
| `theta_seed` | seed/binding equality, line 93 | `independent_terminal` control owner, line 186 |
| `theta_action` | action owner, line 93 | `independent_terminal` action owner, line 184 |
| `z_action` | action owner, line 93 | `independent_terminal` action owner, line 184 |
| `eta_action` | action owner, line 93 | `independent_terminal` action owner, line 184 |
| `D_entry` | map owner, line 94 | `independent_terminal` map owner, line 185 |
| `O_entry` | map owner, line 94 | `independent_terminal` map owner, line 185 |
| `C_entry` | map owner, line 94 | `independent_terminal` map owner, line 185 |
| `action_order` | control owner, line 95 | `independent_terminal` control owner, line 186 |
| `premature_C` | control owner, line 95 | `independent_terminal` control owner, line 186 |
| `target` | MEMBER/NONMEMBER mismatch, line 121 | `independent_terminal` semantic terminal, line 209 |
| `seed_index` | seed/binding equality, line 93 | resealed `replay` seed replay, line 152 |
| `parent` | parent control, line 95 | resealed `replay` seed replay, line 152 |
| `row_theta` | seed/binding equality, line 93 | resealed `replay` typed row, line 150 |
| `left_kernel` | kernel-method control, line 95 | resealed `replay` basis independence, line 162 |
| `Hd1` | C/binding map owner, line 94 | resealed `replay` full `Hd1` span, line 167 |
| `member_ancestry` | seed/binding equality, line 93 | resealed `replay` member equations, line 171 |
| `dual` | MEMBER/NONMEMBER mismatch, line 121 | resealed `replay` dual equations, line 177 |
| `terminal` | terminal enum, line 120 | resealed `replay` receipt terminal, line 141 |

For the `target` canaries, changing the outside case target from `e2` to `e1`
makes it a member of `Hd1=<e1>`, so both routes reach the intended semantic
terminal gate.  Receipt indices at checker line 350 provide the required two
rows, two-element kernel basis, member witness, `Hd1`, and dual to the eight
receipt mutations.  Both independent and producer wrong-nonempty-seal
canaries remain mandatory (producer lines 157--160; checker lines 328--336).

## 5. Exact-one driver and typed production route - PASS

The driver rejects stale outputs before work (line 19) and emits a shell with
`set -euo pipefail` (line 21).  In SELFTEST, lines 25 and 28 use quoted
`grep -Fxc` counts and compare each complete producer/checker success line to
literal `1`; lines 26 and 29 require nonempty artifacts and identical nonempty
normalized terminals.  In production, lines 34--36 perform the same exact-one
and quoted equality checks on the full space-containing `STATIC_BLOCKED`
lines.  Line 38 is the sole sentinel write and immediately exact-counts its
line as one; it occurs only after all mode gates.

Producer lines 175--176 and checker line 373 select
`STATIC_BLOCKED:actual typed matrices are not staged` without entering the
SELFTEST fixture paths.  Driver lines 31--36 run producer then checker, demand
their four nonempty artifacts, exact-count both complete terminal lines, and
compare the extracted values.  The route is statically reachable and remains
typed/fail-closed; no actual production matrices are claimed.

## 6. Performance audit and fixed bounds - PASS

The added preflight is a fixed linear scan: 5 cases times 6 pairs equals 30
literal equalities.  The six shapes contain
`4+4+121+4+22+11 = 166` entries per side, hence at most 1660 per-entry
dimension/type/range checks over both sides of all five cases.  It performs no
rank, closure, kernel, or case compilation.

The SELFTEST semantic-call accounting is exact and contains no redundant
second baseline pass:

```text
producer: 5 baseline compile_case + 19 required mutation oracles = 24 calls
checker:  5 baseline replay + 11 fixture independent_terminal
          + 8 receipt replay mutation oracles                    = 24 calls
```

Those mutation calls are the prescribed fail-closed canaries, not accidental
full recompilation.  Producer reads/parses the fixture file once.  Checker
reads/parses the fixture once and the distinct producer receipt once.  The
JSON round-trips in producer line 129 and checker lines 214--215 are bounded
mutation-local defensive copies; they neither reread nor reparse the fixture
file and their counts are fixed (19 case copies in producer; 19 case plus 19
receipt copies in checker).

The computational hot path is the required 24 semantic calls per component,
especially the repeated fixed `11x11` action rank/equivariance checks and the
checker's complete left-kernel canary.  Its bounds are small and explicit:

- Theta dimension is 2, so the flat closure has at most two accepted rows.
  With at most two literal seeds and two actions, at most
  `2 + 2*2 = 6` queued rows are popped per case.
- Checker `left_kernel` enumerates at most `3^2 = 9` coefficient vectors and
  retains at most 8 nonzero vectors; it never enumerates `3^11`.
- Producer `span_solve` examines at most `3^2 = 9` coefficients.  Producer and
  checker dual searches each examine at most `3^2 = 9` candidates because Z
  and every target have dimension 2.
- All remaining rank/RREF and matrix work has dimensions bounded by 11 and is
  polynomial; there is no data-dependent unbounded retry or closure loop.

Neither Python source imports or launches subprocesses and neither contains a
sleep, lock, thread, process pool, retry, polling loop, or external I/O beyond
its one-shot inputs/outputs.  The driver has exactly the architecturally
required serial producer and checker invocations under one GAP-launched shell;
there is no extra compute subprocess, background job, sleep, or lock.  Thus no
unnecessary full recompilation, file reparse, exponential growth, or serial
coordination was added by v8.

## 7. Final accounting

```text
TASK312/V8 LOAD-BEARING STATIC CODE AUDIT:     PASS
V7 TWO MALFORMED BINDING ROWS:                REPAIRED TO 11/11
ALL-CASE BINDING PREFLIGHT:                   5 x 6 PAIRS PASS STATICALLY
EXPECTED FIXTURE TUPLES:                      5/5 MANUALLY CONFIRMED
PRODUCER MUTATION GATE:                       19/19 REQUIRED; 0/19 ACTUAL
INDEPENDENT CHECKER MUTATION GATE:            19/19 REQUIRED; 0/19 ACTUAL
EXACT-ONE DRIVER / PINS:                      PASS STATICALLY
PRODUCTION STATIC_BLOCKED ROUTE:              PASS STATICALLY; UNEXECUTED
PERFORMANCE / FIXED-BOUND AUDIT:              PASS
LUNA REPLY BYTE-LENGTH REPORT:                4698 CLAIMED / 4703 ACTUAL
LUNA REPLY DEFECT CLASS:                      NON-LOAD-BEARING REPORT ERROR
ACTUAL A5 / ACTUAL A6:                        0/3 / 0/3
LIFT / FAKE CERTIFICATE / IHARA RESULT:        NONE DECLARED
```

`TASK314_R07_TASK312_V8_SOLMAX_CODE_PERFORMANCE_AUDIT_PASS_UNEXECUTED`
