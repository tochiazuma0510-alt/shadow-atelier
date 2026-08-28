# Sol(max) reply 344 — task338 A5/A6-v13 code and performance audit

## Verdict

**REJECT / UNEXECUTED.**  No Python, Node, GAP, GHA, workflow, network, git,
producer, or checker was run.  This is a source-and-byte audit only, and no
runtime output is inferred.

There are several independent fatal blockers.

1. The committed v13 wrapper freezes this workstation's absolute Windows
   source path.  Both Python programs require it to equal their runtime
   resolved path.  Thus a normal Linux GHA checkout fails wrapper validation
   before the first case.
2. On the exact Windows checkout named by the wrapper, and assuming clean
   stale-output paths, the producer compiles the five cases and passes the
   first 24 controls, but control 25, `candidate_parent`, changes
   `transcript[0].parent` while `owner_value` reads a nonexistent top-level
   `candidate_parent`.  Both owner values hash as `null`; the producer raises
   an uncaught `RuntimeError` before the semantic oracle, writes no receipt,
   and never prints its required terminal.
3. Supplying a hypothetically repaired producer receipt does not reach the
   checker controls.  The first dependent record has
   `normalized_ancestry = null`, as the retained-basis contract requires,
   while `check_f3_receipt` requires a list.  The checker stops at case
   `nonzero-member`, transcript ordinal 2, with `UNKNOWN_INPUT: receipt
   coefficient vector`.
4. After allowing the legitimate null, checker control 12, `seed_index`, is
   the next failure: its owner locator also reads a nonexistent top-level
   field.  Four early certificate owners and all ten later nested owners have
   this checker defect.  Ten corresponding producer nested owners fail, and
   the producer's ten anchor-control branches independently reference four
   locals which that branch never assigns.
5. PRODUCTION has no actual route.  The driver never passes `--actual-input`;
   producer and checker accept and propagate only `STATIC_BLOCKED`; the
   optional input ABI trusts strings, integers, supplied pair dictionaries,
   and copied Booleans; and `corrected_base_pairs` has no production caller.
   No task198 authority member, task232 context, accepted A4 basis, A3
   coefficient map, task192/task193 row, actual joint matrix, A5 terminal, or
   A6 pair polynomial is consumed.

The frozen finite-field arithmetic itself is sound and statically reachable
before the producer's mutation failure.  That is only a synthetic width-13
linear-algebra result.

## 1. Files, bytes, and literal dependency graph

The following byte counts and SHA-256 values were recomputed read-only from
the files on disk.  They agree with the v13 driver's pins and reply338.

| role | path | bytes | SHA-256 |
|---|---|---:|---|
| producer | `search/d972_r07_joint_slice_kernel_general_v13.py` | 79,617 | `feb69c5ab8e1b4db21ff5df05dac1690718310dc4c99cf4b67fc439ca9bc4268` |
| checker | `crosscheck/check_d972_r07_joint_slice_kernel_general_v13.py` | 73,233 | `dc344638ae42110f7cd028164c3ac5f6b5e1a908bdc596e5b4718c21db3cad07` |
| GAP driver | `search/d972_r07_joint_slice_kernel_general_gha_driver_v13.g` | 11,044 | `79d93c2cff7173ca0c6ca3d356b4b3d3e7efcdffcb0b5351947ec273d5c50778` |
| v13 wrapper | `search/certs/d972_r07_joint_slice_kernel_general_selftest_v13_20260829.json` | 11,163 | `60a3e1449f911fcfc3946373bcb471ea8efbaed4f1a2064e9ffbfba527fae50d` |
| sole imported repository source | `search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json` | 12,964 | `cab24a5e6ddd7812094b920bffd7688564092a3c9b718484bf3f887cf59d2058` |

No v13 `ci/out` receipt, verdict, log, terminal, seal, shell, or sentinel was
created or treated as evidence.

The complete repository import/data graph is:

```text
GAP driver
  -> pins producer, checker, v13 wrapper, immutable v11 source
  -> emits one bash shell
       -> producer (standard-library imports only)
            -> v13 wrapper -> exact v11 source
            -> optional standalone JSON anchor only if --actual-input exists
       -> seal-only python -c consumer
       -> checker (standard-library imports only; no producer/helper import)
            -> v13 wrapper -> exact v11 source
            -> producer receipt
            -> optional same standalone JSON anchor
       -> seal-only python -c consumer
       -> exact producer/checker terminal comparison
       -> sole .ok sentinel
  -> GAP reads sentinel -> driver PASS line
```

Neither Python file imports a repository arithmetic helper.  The producer
uses `argparse`, `copy`, `hashlib`, `itertools`, `json`, `time`, `deque`, and
`Path` (plus a dynamic best-effort `resource` import); the checker has its own
standard-library implementation.  There is no edge to any of the five
accepted task198 authority files, any task232 implementation/output, A2/A3,
task192/task193, an A4 receipt/verdict, or a roof/tower evaluator.

The accepted task198 authority boundary which a real consumer would have to
bind is, by task330, the following five files in `ci/in`:

| member | bytes | SHA-256 |
|---|---:|---|
| `d972_r07_seven_context_roof_presentation_v1.json` | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| `d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json` | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| producer attestation | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| checker attestation | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| checker verdict | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |

V13 refers to none of them.

### Absolute-path first failure

The wrapper contains

```text
C:\Users\81905\Desktop\shadow-atelier\search\certs\
d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json
```

as `source_binding.resolved_path`.  Producer
`load_wrapper_from_value` and checker `check_wrapper_value` compare that
literal string with `str(ROOT / SOURCE_REL)`.  The bytes and relative-path
pins are portable; this asserted workstation path is not.  On a normal
hosted Linux checkout it is the literal first SELFTEST and PRODUCTION
failure.  A successor must authenticate a canonical repository-relative
path, resolve it under the runtime repository root, and record the observed
absolute path only after loading; it must not commit one machine's absolute
path as an equality premise.

## 2. Route-by-route reachability and first failures

### SELFTEST on the named Windows checkout

Under the smallest portability repair (or on this exact checkout), the
driver pins pass, stale paths are required absent, and the emitted shell
starts the producer.  The producer loads the wrapper and v11 source,
validates the five literal cases, compiles all five, checks their arithmetic
receipts, and enters the ordered 44-control list.  Controls 1--24 have
physical edits and reach their registered gates.  Control 25 then does:

```text
mutate_receipt: transcript[0]["parent"] = 99
owner_value(before, "candidate_parent")  -> before.get("candidate_parent") -> None
owner_value(after,  "candidate_parent")  -> after.get("candidate_parent")  -> None
```

The case receipt is resealed and its complete canonical bytes differ, but
the claimed owner hashes do not.  Line 1387 raises `RuntimeError("mutation
did not change owned canonical object")`.  `main` catches only
`UnknownInput` and `UnknownResource`, so there is a traceback/nonzero exit,
no producer terminal, no written receipt (writing occurs only after all
controls), and `set -euo pipefail` prevents receipt sealing, checker launch,
terminal comparison, and sentinel creation.

Individually continuing after that defect, controls 25--34 all have the same
top-level-owner bug.  At control 35 the producer takes the anchor branch,
changes the wrapper placeholder, but never assigns `owned_before`,
`owned_after`, `before_digest`, or `after_digest`; every anchor control
35--44 would raise `UnboundLocalError` before its oracle.

### Hypothetical checker route

After minimally repairing producer owner extraction and its anchor locals,
the checker loads and independently reconstructs all five cases.  Its first
call to `verify_receipt` starts with `check_f3_receipt`.  Accepted closure
records have list-valued normalized ancestry, while a dependent record has
no normalized pivot row or transform.  Producer
`RetainedF3Basis.consider` therefore correctly exports `None`; producer
validation explicitly allows it.  Checker lines 814--817 unconditionally
require a list.  The first affected row is `nonzero-member` ordinal 2 (the
`m`-image of the first seed).  The checker exits `UNKNOWN_INPUT` before
writing a verdict or starting any checker mutation.

If the checker is minimally repaired to accept `None` exactly when the
decision is `DEPENDENT`, control 12 mutates `rows[0].seed_index`, but checker
`owner_value` reads `receipt.get("seed_index")`.  Both owner hashes are
`null`, so it raises `RuntimeError("checker mutation did not change owner")`
before `verify_receipt`.  The same defect affects `parent`, `row_theta`, the
misnamed `left_kernel`, and all ten transcript/member nested owners recorded
in Section 6.

### PRODUCTION with no actual input

Driver lines 118 and 121 invoke producer and checker without
`--actual-input`.  The wrapper is still the synthetic wrapper.  After the
absolute-path issue is repaired, producer emits only:

```text
status = terminal = STATIC_BLOCKED:actual typed matrices are not staged
production_input = false
actual_a5_a6_milestone = false
```

The checker merely authenticates this static receipt and emits the same
static terminal.  The shell can compare those terminals and write its
sentinel, but that is a successful static-block protocol, not an A5/A6
calculation.

### Malformed and shaped purported actual inputs

The driver has no variable or CLI interpolation by which either can be
supplied.  If the Python programs are invoked directly:

- a missing path or malformed JSON raises `FileNotFoundError` or
  `JSONDecodeError`, neither caught by the declared terminal handlers, so the
  input does not receive an honest `UNKNOWN_INPUT` receipt;
- a syntactically valid wrong-shaped dictionary reaches an owner gate and is
  `UNKNOWN_INPUT`;
- a shaped dictionary passes if it has the v247 package label, any nonempty
  receipt-id and word strings, integers in the allowed small sets, three
  literal `true` flags, a nonempty pair list with unequal string endpoints
  whose rendering omits `[x,y]^3`, and the expected order string;
- after accepting that shaped fiction, producer still returns
  `STATIC_BLOCKED`; checker repeats the same shallow gate and checks only the
  static producer receipt.

An actual future A4-v4 package is not this top-level standalone anchor shape
and would either be rejected at `package` or stripped of its authenticated
producer/checker/basis context.  `corrected_base_pairs` is never called by
`production`, and the checker has no independent pair constructor.

### Intended actual task198/task232 route

There is no statement at which the intended route enters v13.  In
particular, no code reconstructs the ten actual task232 contexts

```text
types: E3,E3,E3,E3,E3,E4,E4,E4,E4,E4
IDs:   21,22,23,24,25, 1,27,21,26,28
E3: (x,y), (x,z), (y,z), (u,x), (u,y)
    z=PP(x,y)^-1, u=PP(y,x)^-1
E4: (A23,A34), (PP(A12,A13),PP(A24,A34)), (A12,A23),
    (PP(A13,A23),A34), (A12,PP(A23,A24))
```

with right-to-left `PP(A,B)=B+A`, distinct `E3-C21`/`E4-C21` tags, and the
authenticated ten-to-eleven occurrence reinsertion.  No actual `D`, `O`,
post-action `C`, simultaneous marked-generator action, `d1`, `e1`, `w`, or
target is built.  Consequently the literal actual route stops before joint
closure; there is no kernel, `Hd1`, MEMBER/NONMEMBER certificate, or A6 pair
language to continue tracing.

## 3. Independent hand trace of the five frozen cases

Every literal coefficient is in canonical F3.  In all five cases
`Theta=F3^2`, `Z=F3^2`, `E_hat=F3^11`, and the synthetic printed quotient is
`F3`; the closure row is `(z,eta)` of width 13.  The stored `A` and every
marked action are square and invertible, all 30 base/binding matrices agree,
and the displayed `D/O` equivariance identities hold.  The 11 occurrence
labels are merely `occurrence00` through `occurrence10`, not the actual typed
task232 roster.

Write `e0,e1` for the first two standard vectors in each displayed factor.
The chronological arithmetic is as follows.

### `nonzero-member`

- Seeds are `A=(e0;e0)` and `B=(e1;e1)` in `Z+E_hat`, both accepted, with
  retained transforms `(1,0)` and `(0,1)` after final padding.
- FIFO pop `A`: `mA=B` is dependent with coefficients `(0,1)`; `nA=2B` is
  dependent with `(0,2)`.  Pop `B`: `mB=A` and `nB=2A` are dependent with
  `(1,0)` and `(2,0)`.
- Thus the six candidates are `A,B,B,2B,A,2A`; pops are 2 and closure rank
  is 2.  `C=0`, so the left kernel is all `F3^2`, with basis `(1,0),(0,1)`
  and eight nonzero elements.
- Its reconstructed `Hd1` rows are `e0,e1`, rank 2.  Target `(1,1)` has
  coefficients `(1,1)`, giving closure/theta ancestry `(1,1)` and a valid
  MEMBER certificate.

### `outside-nonmember`

- The seed has `theta=e0`, `z=e0`, `eta=e0` and is accepted.  The sole
  identity action yields the same row, dependent with coefficient `(1)`.
- There are 2 candidates, 1 pop, and rank 1.  Since `C=0`, the kernel basis is
  `(1)`, its two nonzero elements give `Hd1=<e0>`, and `Hd1` rank is 1.
- Target `e1` is outside.  The dual `(0,1)` annihilates `e0` and pairs to 1
  with the target, so NONMEMBER is valid.

### `zero-member`

- The seed has `theta=e0`, `z=0`, `eta=e0`; the identity image is dependent
  with coefficient `(1)`.  Candidate/pop/rank counts are `2/1/1`.
- `C=0`, so the kernel basis is `(1)` and has two nonzero elements.  Its
  reconstructed `Hd1` row is zero; the retained nonzero `Hd1` rank is 0.
- Target zero is represented by the empty retained basis.  The lifted
  coefficients are zero, giving `theta=z=eta=0`, hence a valid MEMBER
  certificate with `member_theta=(0,0)`.

### `zero-nonmember`

- The closure is the same one accepted row and one dependent identity image.
  Here `C(eta)=1`, so the `1 x 1` image matrix is `(1)`, the kernel is zero,
  its nonzero cardinality and `Hd1` rank are both 0.
- Target `e0` is not zero; dual `(1,0)` pairs to 1.  NONMEMBER is valid.

### `post-c-cancel`

- Seed `A=(e0;e0)` is accepted.  Its `m`-image
  `B=(e1;e1)` is accepted and enqueued.  Popping `B` yields `A`, dependent
  with coefficients `(1,0)`.  Hence candidates/pops/rank are `3/2/2`.
- The two `C`-images are both 1.  Producer left-kernel basis `(2,1)` and
  checker bottom-pivot basis `(1,2)` span the same line; it has two nonzero
  elements.
- The producer `Hd1` raw row is `(2,1)`.  Its normalized row is `(1,2)` with
  raw transform `(2)`.  Target `(1,2)` is obtained with retained coefficient
  2, hence kernel coefficient `2*(2,1)=(1,2)`.  This reconstructs
  `theta=z=(1,2)` and an eta row killed by `C`, so MEMBER is valid.

The independently derived summary is therefore:

| case | candidates | pops | closure rank | kernel dim | nonzero kernel | `Hd1` rank | terminal |
|---|---:|---:|---:|---:|---:|---:|---|
| nonzero-member | 6 | 2 | 2 | 2 | 8 | 2 | MEMBER |
| outside-nonmember | 2 | 1 | 1 | 1 | 2 | 1 | NONMEMBER |
| zero-member | 2 | 1 | 1 | 1 | 2 | 0 | MEMBER |
| zero-nonmember | 2 | 1 | 1 | 0 | 0 | 0 | NONMEMBER |
| post-c-cancel | 3 | 2 | 2 | 1 | 2 | 1 | MEMBER |

This proves the five advertised tuples from the live matrices, not from the
wrapper table.  It establishes only static reachability of a synthetic
finite-linear-algebra suite.  It supplies no actual A4 word-bearing basis or
anchor and no actual A5/A6 numerator.

## 4. Retained-basis invariant and checker independence

### Producer signs, padding, and post-closure algebra

The retained-basis signs are correct.  During reduction, each pivot step is

```text
remainder <- remainder - m * pivot_row
coefficients <- coefficients + m * pivot_transform
```

so

```text
raw_candidate = sum(coefficients[i] * R_i) + remainder.
```

For a new pivot with normalization `s`,
`normalized=s*remainder`; after appending the new raw row its transform is
`(-s*old_coefficients, s)`.  Existing transforms are padded before roster
growth and receive the same row subtraction as their reduced rows.  An
accepted candidate gets its unit direct coefficient; a dependent candidate
gets its zero-remainder coefficients, later padded to the final roster.
`export` and `replay_owner` directly reconstruct every normalized row and
every accepted and dependent chronological candidate.  The five hand traces
above exercise unit, scalar-2, zero-row, and post-C cancellation cases.

`C` is applied only after the joint queue exhausts.  Its image matrix is
oriented as quotient-coordinate rows by closure-basis columns, so each
nullspace row is correctly a coefficient vector on accepted closure rows.
Theta, z, and eta are all reconstructed with that vector; `C eta=0` is
replayed; `Hd1` is the z projection; MEMBER ancestry composes the `Hd1` and
kernel coefficients; and NONMEMBER solves an augmented annihilator with
pairing 1.  No retained-basis or frozen arithmetic defect was found.

### What is and is not independent

The checker does not import the producer or any shared arithmetic helper.  It
uses rightmost pivots in `BottomSpan`, a separately implemented bottom-pivot
augmented `DenseTableau`, its own FIFO action reconstruction, its own
bottom-nullspace basis, two-way closure/kernel/`Hd1` span comparisons, its
own MEMBER solve, and an augmented NONMEMBER dual.  Producer and checker
indeed choose different post-C bases in `post-c-cancel`, which is a useful
independence witness.

The common expected-case dictionary is compared only after arithmetic, so it
does not by itself decide a tuple.  The checker replays producer ancestry
fields against the producer's retained raw roster while independently
checking the mathematical spans; using certificate coordinates for
certificate replay is legitimate and does not make those coordinates the
arithmetic authority.

Independence nevertheless stops at the synthetic core.  The mutation
registry and semantic labels are copied; the baseline checker is unreachable
because of its null-shape bug; several physical owners are not located; and
both production paths share the same shallow Boolean anchor validator.  The
checker has no independent actual word parser, rho0/rho1/q evaluation,
task198/task232 reconstruction, actual full-cokernel action, or base-pair
constructor.  Thus the synthetic algorithm is structurally independent, but
there is no independent actual A5/A6 checker.

## 5. V247, v280, and v281 trust-boundary audit

`ANCHOR_CONTRACT` consists of placeholder strings such as
`A4_ANCHOR_RECEIPT_REQUIRED`, `A4_REQUIRED_LEAST_INDEX`, and
`u_z_REQUIRED_SOURCE_WORD`.  Wrapper controls compare those strings with a
second hard-coded copy.  This authenticates neither an A4 object nor any
mathematics.

`validate_actual_anchor` has none of the required operations.  It does not:

- authenticate receipt bytes, a self seal, accepted producer/checker
  identities, task198 authority, or common roof/tower identities;
- parse or deterministically free-reduce a word;
- evaluate any ordered A4 basis word in Delta1, Delta0, or D1;
- prove that the supplied K elements are a complete independent basis;
- compute `q(k_i)` as one of `1,z0,z0^2`, the exponent `a_i`, the least
  nonzero index, its inverse, `u_*`, or `k_*`;
- evaluate rho1/rho0/q, prove K membership, or replay a roof fibre;
- consume an authenticated A3 coefficient ledger or derive a Heisenberg
  normal-form section; or
- construct or replay pair endpoints.

`corrected_base_pairs` accepts external coefficient and section-string lists,
concatenates `section + "*" + literal_word` without parsing or free
reduction, and copies one `rho0_replay` Boolean into both endpoint fields.  It
trusts the very `base_pairs` list which v280 requires the consumer to reject
as evidence.  It is also unreachable from production.

V280 is binding and is strictly stronger than the obsolete v13/v247-shaped
dictionary.  A5 must consume the complete accepted ordered word-bearing A4
basis `(u_i,k_i)`, independently evaluate every word, compute
`q(k_i)=z0^a_i`, choose the least nonzero `j`, compute
`e=a_j^-1`, `u_*=red(u_j^e)`, and `k_*=k_j^e`, and replay all three equalities
without a Boolean premise.  It must then form the ordered adapted basis

```text
k_*,  k_i k_*^-a_i  (i != j, in old order)
```

with literal words, record its invertible change matrix, and replay both
directions.  Exactly the `k_*` seed may carry the exponent-nine occurrence
endpoint; the other `t-1` pointed seeds remain present with zero occurrence
endpoint.  A supplied anchor subreceipt is only a derived-value comparison.

The A3+A4 base point must likewise be local: authenticate the canonical A3
map `lambda_g`, derive `s(g)=x^a y^b h^r` from each authenticated D1 key, and
construct `lambda_g*(red(s(g)u_*)-s(g))` in canonical order.  A supplied pair
roster, formula string, or substring canary is not evidence.

V281 fixes the positive handoff language as well.  Every MEMBER ancestry
term must remain a literal factored pair `c*(A*u_i-A)=c*A*(u_i-1)`, represented
by an authenticated prefix DAG `(earlier parent, literal letter)` and an
authenticated kernel-word dictionary.  Equality of finite-shadow elements
must never identify distinct literal prefixes.  This representation avoids
re-evaluating long prefixes, but it does not weaken replay: a downstream
positive ZERO must still expand every `U=red(Au_i), V=A`, independently
evaluate literal endpoints, and construct the full C1 chains.  V14 need only
emit and independently replay this exact A6 language; it may not claim any
v281 A7 ZERO.

## 6. All 44 producer and 44 checker mutation routes

The table below is a static route audit, not an execution record.

- `PASS*` means the physical synthetic owner changes, the appropriate
  temporary/case seal is recomputed where applicable, the normal validator
  is reached, and the exact listed registered stage/code/reason is obtained
  under the prior minimal repairs.
- `LOCATOR FAIL` means the nested object really changes and the case seal is
  recomputed, but `owner_value` hashes an unrelated missing top-level field,
  so the normal oracle is never reached.
- `LOCAL FAIL` means the producer anchor branch changes the placeholder but
  references unassigned locals before its validator.
- `PLACEHOLDER*` means the checker reaches the exact listed gate only by
  changing the synthetic hard-coded wrapper placeholder; it is not a real
  A4/word/evaluator/pair owner and is therefore rejected as a production
  control.

| # | owner; physical object changed | producer route | checker route | registered narrow rejection |
|---:|---|---|---|---|
| 1 | `field_modulus`; raw `case.modulus` | PASS* | PASS* | `raw.field_modulus / M_FIELD_MODULUS / field modulus is not F3` |
| 2 | `theta_seed`; `theta_seeds[0][0]` | PASS* | PASS* | `raw.theta_seed / M_THETA_SEED / theta seed binding changed` |
| 3 | `theta_action`; `A_theta[0][0]` | PASS* | PASS* | `raw.theta_action / M_THETA_ACTION / theta action owner changed` |
| 4 | `z_action`; `A_Z[0][0]` | PASS* | PASS* | `raw.z_action / M_Z_ACTION / z action owner changed` |
| 5 | `eta_action`; `A_E[0][0]` | PASS* | PASS* | `raw.eta_action / M_ETA_ACTION / eta action owner changed` |
| 6 | `D_entry`; `D[0][0]` | PASS* | PASS* | `raw.D_entry / M_D_ENTRY / D map owner changed` |
| 7 | `O_entry`; `O[0][0]` | PASS* | PASS* | `raw.O_entry / M_O_ENTRY / O map owner changed` |
| 8 | `C_entry`; `C[0][0]` | PASS* | PASS* | `raw.C_entry / M_C_ENTRY / C map owner changed` |
| 9 | `action_order`; raw `action_names` | PASS* | PASS* | `raw.action_order / M_ACTION_ORDER / action order binding changed` |
| 10 | `premature_C`; raw `C_phase` | PASS* | PASS* | `raw.premature_C / M_PREMATURE_C / C was applied before closure` |
| 11 | `target`; raw target coordinate | PASS* | PASS* | `raw.target / M_TARGET / target membership changed` |
| 12 | `seed_index`; accepted `rows[0].seed_index` | PASS* | LOCATOR FAIL (`seed_index` absent at top level) | `certificate.seed_index / M_SEED_INDEX / certificate seed index is invalid` |
| 13 | `parent`; accepted row parent | PASS* | LOCATOR FAIL (`parent` absent) | `certificate.parent / M_PARENT / certificate parent is invalid` |
| 14 | `row_theta`; accepted `rows[0].theta` | PASS* | LOCATOR FAIL (`row_theta` absent) | `certificate.row_theta / M_ROW_THETA / certificate row theta does not replay` |
| 15 | `left_kernel`; `left_kernel_basis[0]` | PASS* | LOCATOR FAIL (looks for `left_kernel`) | `certificate.left_kernel / M_LEFT_KERNEL / left-kernel basis content changed` |
| 16 | `Hd1`; top-level `Hd1[0]` | PASS* | PASS* | `certificate.Hd1 / M_HD1 / Hd1 content changed` |
| 17 | `member_ancestry`; ancestry theta | PASS* | PASS* | `certificate.member_ancestry / M_MEMBER_ANCESTRY / member theta ancestry does not replay` |
| 18 | `dual`; top-level dual coordinate | PASS* | PASS* | `certificate.dual / M_DUAL / separating dual does not replay` |
| 19 | `terminal`; top-level terminal | PASS* | PASS* | `certificate.terminal / M_TERMINAL / certificate terminal changed` |
| 20 | `production_input`; wrapper source binding | PASS* (SHA changed) | PASS* (byte count changed; reported “reseal” remains old source SHA) | `wrapper.production_input / M_PRODUCTION_INPUT / production input binding changed` |
| 21 | `closure_queue_pops`; top-level scalar | PASS* | PASS* | `certificate.closure_queue_pops / M_CLOSURE_QUEUE_POPS / closure queue pop count changed` |
| 22 | `context_pops`; top-level scalar | PASS* | PASS* | `certificate.context_pops / M_CONTEXT_POPS / context pop receipt changed` |
| 23 | `closure_candidate_count`; top-level scalar | PASS* | PASS* | `certificate.closure_candidate_count / M_CLOSURE_CANDIDATE_COUNT / closure candidate count changed` |
| 24 | `closure_queue_bound`; top-level scalar | PASS* | PASS* | `certificate.closure_queue_bound / M_CLOSURE_QUEUE_BOUND / closure queue bound changed` |
| 25 | `candidate_parent`; `transcript[0].parent` | LOCATOR FAIL | LOCATOR FAIL | `certificate.candidate_parent / M_CANDIDATE_PARENT / candidate parent changed` |
| 26 | `candidate_action`; `transcript[0].action` | LOCATOR FAIL | LOCATOR FAIL | `certificate.candidate_action / M_CANDIDATE_ACTION / candidate action changed` |
| 27 | `candidate_decision`; `transcript[0].decision` | LOCATOR FAIL | LOCATOR FAIL | `certificate.candidate_decision / M_CANDIDATE_DECISION / candidate decision changed` |
| 28 | `candidate_normalization`; transcript normalization | LOCATOR FAIL | LOCATOR FAIL | `certificate.candidate_normalization / M_CANDIDATE_NORMALIZATION / candidate normalization changed` |
| 29 | `candidate_coefficients`; transcript reduction vector | LOCATOR FAIL | LOCATOR FAIL | `certificate.candidate_coefficients / M_CANDIDATE_COEFFICIENTS / candidate coefficients changed` |
| 30 | `candidate_rank`; transcript post-rank | LOCATOR FAIL | LOCATOR FAIL | `certificate.candidate_rank / M_CANDIDATE_RANK / candidate rank changed` |
| 31 | `dependent_record_deletion`; chronological transcript | LOCATOR FAIL | LOCATOR FAIL | `certificate.dependent_record_deletion / M_DEPENDENT_RECORD_DELETION / dependent candidate record deleted` |
| 32 | `dependent_record_reorder`; two dependent records | LOCATOR FAIL | LOCATOR FAIL | `certificate.dependent_record_reorder / M_DEPENDENT_RECORD_REORDER / dependent candidate records reordered` |
| 33 | `f3_plus3_coefficient`; nested coefficient set to 3 | LOCATOR FAIL | LOCATOR FAIL | `certificate.f3_plus3_coefficient / M_F3_PLUS3_COEFFICIENT / coefficient is outside canonical F3` |
| 34 | `member_witness_equality`; top-level `member_theta[0]` | LOCATOR FAIL | LOCATOR FAIL | `certificate.member_witness_equality / M_MEMBER_WITNESS_EQUALITY / member witness does not map to the target slice` |
| 35 | `a4_anchor_identity`; wrapper placeholder receipt-id | LOCAL FAIL | PLACEHOLDER* | `production.anchor.identity / M_A4_ANCHOR_IDENTITY / A4 anchor receipt identity changed` |
| 36 | `anchor_least_index`; wrapper placeholder | LOCAL FAIL | PLACEHOLDER* | `production.anchor.least_index / M_ANCHOR_LEAST_INDEX / A4 anchor least index changed` |
| 37 | `anchor_projected_exponent`; wrapper placeholder | LOCAL FAIL | PLACEHOLDER* | `production.anchor.projected_exponent / M_ANCHOR_PROJECTED_EXPONENT / A4 projected exponent changed` |
| 38 | `anchor_inverse_scalar`; wrapper placeholder | LOCAL FAIL | PLACEHOLDER* | `production.anchor.inverse_scalar / M_ANCHOR_INVERSE_SCALAR / A4 inverse scalar changed` |
| 39 | `anchor_substituted_cube`; placeholder `forbidden_pair` | LOCAL FAIL | PLACEHOLDER* | `production.anchor.forbidden_cube / M_ANCHOR_SUBSTITUTED_CUBE / superseded literal cube pair was supplied` |
| 40 | `anchor_word`; placeholder `literal_word` | LOCAL FAIL | PLACEHOLDER* | `production.anchor.word / M_ANCHOR_WORD / A4 anchor word changed` |
| 41 | `anchor_rho0`; placeholder replay string | LOCAL FAIL | PLACEHOLDER* | `production.anchor.rho0 / M_ANCHOR_RHO0 / A4 anchor rho0 replay failed` |
| 42 | `anchor_rho1_kernel`; placeholder kernel string | LOCAL FAIL | PLACEHOLDER* | `production.anchor.rho1_kernel / M_ANCHOR_RHO1_KERNEL / A4 anchor rho1 is not in K` |
| 43 | `anchor_q_z0`; placeholder q string | LOCAL FAIL | PLACEHOLDER* | `production.anchor.q_z0 / M_ANCHOR_Q_Z0 / A4 anchor q value is not z0` |
| 44 | `base_pair_order`; placeholder order string | LOCAL FAIL | PLACEHOLDER* | `production.anchor.base_pair_order / M_BASE_PAIR_ORDER / corrected base-pair order changed` |

Thus only producer controls 1--24 are individually sound synthetic controls;
checker controls 1--11 and 16--24 are individually sound after the baseline
null repair.  None of the two literal ordered suites completes.  Most
importantly, none of controls 35--44 mutates an actual accepted A4 receipt,
basis word, finite representation value, K proof, derived anchor, adapted
basis, A3 coefficient, locally generated pair, or endpoint replay.

## 7. Resource and unnecessary-work audit

### Concrete frozen counts

Across the five cases the core producer constructs 15 chronological
candidates, performs 7 queue pops and 9 marked-action applications, accepts
7 closure rows, and records 8 dependent rows.  Per-case derived queue bounds
are `58,15,15,15,15`; actual pops are `2,1,1,1,2`.  The bound is checked only
after the queue is empty, so it is an assertion, not a live resource cap.

The producer closure reductions perform eight nonzero pivot eliminations in
the hand trace (four in the first case, one in each of the next three, and
one in the last) and 13 scalar transform updates.  Target solving adds three
nonzero pivot eliminations: two for `(1,1)` and one for the final `(1,2)`.
Kernel dimensions total 5 and retained nonzero `Hd1` ranks total 4.

The checker makes 15 `BottomSpan.contains` calls and, for all 7 accepted
rows, immediately calls `BottomSpan.add`, which repeats the same reduction.
Those seven accepted-row reductions are unnecessary.  Before the baseline
receipt bug it builds five closure and three nonempty-`Hd1` dense tableaux.
After the null-shape repair and complete baseline receipt checks, it builds
27 dense tableaux in total:

```text
independent closure 5 + independent Hd1 3
+ producer kernel 4 + checker kernel 4
+ producer Hd1 3 + checker Hd1 3
+ producer-receipt closure 5 = 27.
```

Some are appropriate independent span witnesses, but several rebuild a
known basis solely to ask containment again.  A single separately owned
sparse echelon object per mathematical span can supply solve and both
containment directions without losing independence.

### Asymptotic work

Let `N` be the chronological candidate count, width be 13, closure rank `r`,
kernel dimension `d`, and retained `Hd1` rank `h`.

- Producer online closure is
  `O(N*(13*r + r^2))`: each candidate updates a width-13 row and up to `r`
  coefficient entries for up to `r` pivots, and the invariant replay forms a
  length-`r` linear combination.  Because `r<=13` in this toy, the wrapper's
  `O(N*13*r)` suppresses the `r^2` term harmlessly here, but it is not the
  right generic accounting for a future wider actual row.
- The post-C image costs `O(11*r)`.  For quotient width `q=1`, its present
  nullspace work is `O(r + d*r)`; reconstruction of theta/z/eta costs
  `O(15*d*r)`.  A generic `q` should be shown explicitly rather than the
  receipt's unrelated `O(r^2*13)` label.
- Retaining the `Hd1` basis costs
  `O(d*(2*h+h^2))`, and target solve/replay costs `O(2*h+h^2)`.
- Producer certificate export/replay and storage are
  `O(N*(13+r)+r*(13+r)+d*r+15*d+d*h)`.  The complete chronological
  transcript therefore has linear-in-`N` but coefficient-width-`r` output;
  there is no output-byte cap.
- Checker closure is `O((N+r)*13*r)` because accepted candidates are reduced
  twice.  A dense augmented span build is `O(r^2*(13+r))`; kernel and `Hd1`
  work add the corresponding `r,d,h` terms above.  Two-way span checks are
  polynomial and appropriate, but do not require 27 fresh objects.

The successful producer design would replay both owner exports twice per
case during compile plus baseline validation (20 owner-replay calls), then
twice for each of 22 certificate controls (44 more).  The checker would make
10 baseline producer-owner replays plus 44 more for its 22 certificate
controls.  Each side also deep-copies and hashes complete case receipts for
those controls.  Thus the advertised `O(44*(N+13^3))` is not a faithful
bound: the relevant term is at least `O(22*S)` per side for receipt size `S`,
with multiple full canonicalizations/reseals per mutant, in addition to raw
matrix validation and tableau work.

Each chronological candidate is separately canonicalized for its raw hash
and record hash; each owner and case is hashed again; the shell's seal-only
consumer parses and canonicalizes the complete producer and checker outputs
once more.  These costs are small for 15 toy candidates but material for an
actual word-bearing transcript.  Hash immutable input bytes once, retain
compact coefficient/DAG ancestry, and canonicalize complete envelopes only
at explicit seal boundaries.  Do not replace literal replay with hashes.

### Meter and cap defects

The producer calls `meter.begin` only during the compile loop.  It leaves the
current bucket at `post-c-cancel`, then charges all five baseline receipt
validations, the entire mutation suite, RSS, and final serialization
reservations to that last case.  Wrapper/source reads occur before any case
and appear only in totals.  Consequently `per_case` is neither per-case core
work nor a partition of totals.  The checker correctly creates a separate
`mutation-controls` bucket, but still reassigns case buckets manually during
receipt verification.  A successor needs explicit phases: input, one bucket
per case/actual closure, certificate replay, mutations, and final I/O.

`rss_bytes` is also not portable: `resource` is absent on the intended
Windows host and gives zero; on Linux `ru_maxrss` is normally KiB, not bytes.
There is no live RSS, candidate, wall-clock, ancestry, canonicalization, or
serialized-output cap.  Shell `timeout` kills the process without allowing
an `UNKNOWN_RESOURCE` receipt.  The only programmatic resource exception is
the post-exhaustion queue assertion, so `UNKNOWN_RESOURCE` is effectively a
dead honest terminal for the frozen route.  Missing files and malformed JSON
can escape as uncaught built-in exceptions, so `UNKNOWN_INPUT` is likewise
incomplete.

The final meter tries to reserve two canonicalizations, one serialization,
and one write before detaching its snapshot.  This avoids direct
self-reference, but it does not measure bytes, actual peak memory, or a cap,
and its per-case attribution is already corrupt.  V14 should state exactly
which final passes are excluded/reserved, record exact encoded bytes from the
detached payload, and let an independent consumer check the seal.

### Preserving performance without weakening proof

The bounded repairs are:

- return `(represented,remainder,coefficients)` from one incremental
  reduction, rather than `contains` followed by `add`;
- use one sparse retained basis per span and a distinct checker pivot order,
  rebuilding only the producer-versus-checker span witnesses needed for two
  directions;
- keep parent/action plus coefficient ancestry as a DAG and expand only the
  selected MEMBER support, while still replaying every selected literal row;
- cache each authenticated A4 word evaluation and each v281 prefix-DAG node
  once per typed occurrence; combine terms only on identical reconstructed
  literal prefix and kernel word;
- run physical mutations on bounded real-shaped fixtures through the same
  adapter/validators, rather than deep-copying a future large actual receipt
  22 times; and
- check caps before queue insertion, elimination, ancestry expansion, and
  serialization, returning a sealed last-replayable `UNKNOWN_RESOURCE`
  object.  A cap never means NONMEMBER.

## 8. Minimal bounded v14 successor contract

V14 must not be a patch which merely fixes the two owner locators.  The
smallest admissible successor has the following exact boundary.

1. **Driver and envelope.**  Require a production input path (for example a
   bound `D344Actual`) and pass the exact same resolved immutable bytes to
   producer and checker with `--actual-input`.  Missing input is
   `UNKNOWN_INPUT`, not a successful static terminal.  Authenticate canonical
   repository-relative paths, bytes, SHA-256, schemas, self seals, accepted
   producer/checker terminals, and common roof/tower/task192 identities.  The
   envelope binds the accepted task198 five-member authority bundle, positive
   A2 and A3 packages, task192/task193 objects, and a future independently
   accepted A4-v4 producer/checker pair.  Until those exist, production must
   stop honestly without changing any numerator.
2. **Actual typed reconstruction.**  Producer and helper-nonshared checker
   independently reconstruct the ten task232 substitutions, their distinct
   types/IDs/tags, and the authenticated ten-to-eleven occurrence map.  They
   build the full-cokernel `d1=-D1(g760)`, `e1=-beta1^193`, the eleven-vector
   `w`, complete boundary reductions, marked actions, and post-action block
   map `C` from accepted literal inputs.  Production dimensions are derived
   from these objects; width 13 remains SELFTEST-only.
3. **Boolean-free A4 adapter.**  Read the complete ordered word-bearing A4
   basis, not a standalone anchor.  Independently parse/evaluate every `u_i`,
   check rho1/rho0 values against its accepted `k_i`, compute every `a_i`,
   derive least `j,e,u_*,k_*`, and replay rho1/rho0/q.  Derived supplied fields
   may be compared but never control acceptance.  Construct the ordered
   adapted basis, its invertible matrix and inverse, replay both directions
   and all words, and build exactly one endpoint-bearing seed plus all other
   pointed seeds.  A checker may instead build the original seeds and prove
   the complete occurrence-level spans equal in both directions.
4. **Local A3 base point.**  Authenticate the canonical A3 coefficient map,
   derive every D1 normal-form section locally, construct the ordered
   `s(g)u_*-s(g)` pairs locally, and replay both rho0 endpoints, rho1 values,
   q-images, coefficient order, and the A3 ledger.  Reject any supplied pair
   list as evidence.
5. **Actual v242 closure and terminal.**  Form every joint seed
   `((k_i-1)d1,(k_i-1) odot w)` before `C`, close under all marked actions to
   queue exhaustion with retained literal/row ancestry, then compute the
   post-C nullspace, `Hd1`, and
   `r0=e1-kappa0*d1`.  Emit either independently replayed MEMBER ancestry or
   a dual which annihilates both independently reconstructed `Hd1` spans and
   pairs to 1.  Rank equality alone is insufficient.
6. **A6/v281 handoff.**  On MEMBER, emit base-point pairs first and live
   closure pairs as canonical factored records
   `(coefficient,prefix-DAG-node,kernel-word-index)`, together with enough
   earlier-parent/literal-letter data to reconstruct every `A`, `red(Au_i)`,
   and roof-fibre endpoint.  Producer and checker reconstruct the literal
   pair polynomial and the equations for `mu1`; no exact-PB ZERO, lift, fake,
   or Ihara claim follows.
7. **Physical controls.**  Fix every existing nested owner locator and the
   checker null contract, then replace the ten placeholder anchor controls
   with mutations of actual package bytes/identity, basis word and `k_i`,
   rho1/rho0/q evaluation, exponent, least index/inverse/`u_*`, adapted
   change matrix/inverse, one-endpoint seed, A3 coefficient/key/section,
   locally generated pair/order/endpoints, and the v281 prefix parent,
   letter, kernel index/word, and coefficient.  Retain physical controls for
   task193 signs, noncycle `d1` endpoint, typed occurrence/reinsertion,
   premature `C`, boundary coefficient, candidate/dependency ancestry,
   nullspace, target, MEMBER equality, and dual.  Each control changes the
   object used by normal production, reseals only authentication envelopes,
   and reaches the normal narrow gate; explicit raises and copied Booleans do
   not count.
8. **Bounds and independent checking.**  Use pre-operation live caps and
   phase-correct meters; compact DAG ancestry; exact output-byte bounds; one
   producer followed by one structurally distinct checker; exact terminal
   equality; and sentinel-last.  Checker must read original upstream bytes,
   rebuild arithmetic with helper-nonshared evaluators, and never accept a
   producer terminal, pivot, Boolean, cache, or DAG evaluation as its
   mathematical authority.

This successor is bounded by the finite accepted dimensions.  V280 adds only
`O(t+support(lambda))` group operations plus literal word evaluation before
closure, and the adapted basis leaves only one endpoint-bearing seed.  V281
stores `p` prefix nodes and `t` used kernel words and permits future endpoint
work `O(10*(p+L_K)+sum_o N*s_o)` before intrinsic PB-normal-form cost, while
preserving literal expansion at the positive boundary.

No SELFTEST, PRODUCTION, or GHA run is authorized by this audit.  V220
deltas 90--92 remain unchanged.

```text
CODE/PERFORMANCE AUDIT:          REJECT
SELFTEST / PRODUCTION:           UNEXECUTED
FIVE FROZEN CASES:               STATICALLY REACHABLE
ACTUAL A5 / ACTUAL A6:           0/3 / 0/3
LIFT / FAKE / IHARA:             NONE
```

`TASK344_R07_TASK338_A5A6_V13_CODE_PERFORMANCE_AUDIT`
