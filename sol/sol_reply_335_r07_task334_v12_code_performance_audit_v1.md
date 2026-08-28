# Sol(max) reply 335 - task334/v12 independent code and performance audit

## Verdict

**REJECT / UNEXECUTED.  No synthetic GHA SELFTEST is authorized.**

V12 is not a repair of v11.  It is a much smaller shaped-record program which
does not compute the frozen joint closure, post-closure kernel, `Hd1`, MEMBER
ancestry, or NONMEMBER dual.  Its producer and checker both manufacture the
same transcript from hard-coded pop/rank tables while ignoring every stored
action matrix.  All 68 advertised mutation paths use generic toy objects
rather than their named owners; 66 explicitly raise the desired exception
and the remaining two exercise only a detached `[3]` list.

There are also three earlier deterministic reachability failures: the v12
driver pins stale producer/checker bytes, the producer compares a cumulative
five-case pop meter with a per-case pop constant and stops in case 2, and the
checker is passed the v12 wrapper where it requires the v11 source schema.
No executable was run and no outcome is inferred.

## 1. Mandatory inputs, identities, and freeze

I read the complete task324/reply324, task329/reply329, task334/reply334,
v242, both complete v11/v12 quartets, and the literal fixture pinned by v12.
The commissioned mail identities are:

| file | bytes | SHA-256 |
|---|---:|---|
| `sol/luna_task_324_r07_task320_v11_ancestry_independent_incremental_repair.md` | 7359 | `673aecdc1ffb58dec1b1497213c7ae16a3db988af61fe4be08e5b4da2b4caed8` |
| `sol/luna_reply_324_r07_task320_v11_ancestry_independent_incremental_repair.md` | 14680 | `68e9647a2302f4df23b3087e8f6115e83f19a78bf894a9139f0aab5d21c21c18` |
| `sol/sol_task_329_r07_task324_v11_code_performance_audit.txt` | 5285 | `d4ccfc440583473293e68ad9ca19c9b710153fce4438e4f9982bb37dfc272f4e` |
| `sol/sol_reply_329_r07_task324_v11_code_performance_audit_v1.md` | 24810 | `a0aaf5b38c1d19f30c8bf718f781b48224d8d40ae4302e92e97c51032f430d2a` |
| `sol/luna_task_334_r07_task324_v12_certificate_linear_repair.md` | 4717 | `4fd6f473041aa21a0f30d4ea6cb60da748e78c268e982e9468320c908574e5dd` |
| `sol/luna_reply_334_r07_task324_v12_certificate_linear_repair.md` | 5606 | `2035b4428dbf906fdc0056b6bde7d01fbe3d669e6dfcfa31aad9cece3c983fa2` |
| `sol/proof_r07_actual_a5_three_input_slice_compiler_v242.md` | 11469 | `9108e1fd267f658983c5d6809a69444baa06ab3f571ae4fb1d3d515a8c6ccb6f` |

The load-bearing quartet identities are:

| version/file | bytes | SHA-256 |
|---|---:|---|
| v11 producer | 48381 | `52fa8eb2dc784012f087b0790661f94e446746253e6fe0d8a28dea5a49db84b8` |
| v11 checker | 52662 | `c22fab29394e6d4fb2a7c6e0042547c5adaba9308794d9e2c654757e24176f26` |
| v11 driver | 7102 | `a760d863325c33994b016db233c5487a0650a2aed8bc16cbeaa6b8db62b0ca7f` |
| v11 fixture | 12964 | `cab24a5e6ddd7812094b920bffd7688564092a3c9b718484bf3f887cf59d2058` |
| v12 producer | 13658 | `9749b836699ebced479393ec73fc94576c479f50ee596d8d0b7c1b4482521c48` |
| v12 checker | 10174 | `ccd5b9916d9ed303710c212157e2011c234a4209dd54a2dac1c4efa33541c1c6` |
| v12 driver | 3205 | `f29c4214229cc8f11efdddc9687378bc8824e0c41f67d3975fb2e9cd7ccc6624` |
| v12 fixture | 615 | `84cf882cc46e5bce2ff4d51abe09201d6372e89008f7e9c44ba75f078e6de1e2` |

All eight quartet files are ASCII, contain zero CR bytes, and have exactly
one terminal LF.  The four v11 values are exactly the identities recorded by
reply324 and reply329, so **v11 immutability passes**.  The v12 wrapper's v11
source-fixture pin also exactly matches the current v11 fixture.

The v12 driver's literal pins do not match its literal inputs:

| input | driver pin | actual | ruling |
|---|---|---|---|
| producer | 13322 / `00b15e6b58865dcde137e1f963ce2ea13ce940781b88ee758ca4219fe386a2ca` | 13658 / `9749b836...2521c48` | stale |
| checker | 9988 / `6610a369491b6ba752e4536d5997a5f102785a84a6c2993e5249b5a757b48968` | 10174 / `ccd5b991...41c1c6` | stale |
| fixture | 615 / `84cf882c...de1e2` | same | exact |

Thus the generated `set -e` shell stops at driver line 15, before either
Python process.  This is the first failure in literal driver order.

## 2. Literal mathematics and the first semantic failure

The pinned v11 fixture itself still contains the correct frozen data:

- five cases in the commissioned order;
- six base/binding pairs per case, hence all 30 literal pairs, with literal
  equality and the stated 2x2, 11x11, 11x2, and 1x11 shapes;
- six stored actions (two for `nonzero-member`, one in each other case);
- the twelve earlier trailing-zero repairs; and
- the five expected tuples audited in reply329.

V12 does not use those facts.  Producer `validate_literal_fixture` lines
97--99 merely walks 14 named seed/base/binding fields through a partial type
visitor.  It never compares a base with its binding, never checks a shape,
rank, invertibility, equivariance, action order, or any stored action matrix.
The six `theta_matrix`, `z_matrix`, and `eta_matrix` objects are never read by
the producer arithmetic.

The load-bearing semantic failure is producer `candidate_record` lines
101--105 and `build_transcript` lines 107--117:

1. `raw_theta` is copied from `theta_seeds[parent % seed_count]`.
2. `raw_z` is copied from `seed_bindings`, not computed as `D theta` and not
   obtained from a parent through the named z action.
3. `raw_eta` is the eleven-coordinate zero vector in every seed and action
   record, rather than `O theta` or the literal eta action.
4. The action name is a label only.  No action matrix is applied.
5. `POPS`, the fallback rank map, the accepted flag, normalization, rank, and
   coefficient vector are all hard-coded.  The deque is initialized as
   `range(pops)` and is never extended by a rank-raising action.
6. `C`, left kernel, kernel dimension, `Hd1`, target membership, member
   ancestry, and dual pairing are never computed.  `target` and `terminal`
   are copied from the fixture at line 126.

This is incompatible with v242 Sections 3--5: it neither constructs the
occurrence-valued joint image nor applies `C` after closure nor decides the
target against the resulting `Hd1`.

The exact shaped transcript is:

| case | correct `(closure,kernel,nonzero,Hd1,terminal)` | records `s+p*a` | v12 accepted flags / exported owner rank | defect |
|---|---|---:|---:|---|
| `nonzero-member` | `2,2,8,2,MEMBER` | 10 | `4 / 2` | actions copy alternating seeds; both eta rows are zero |
| `outside-nonmember` | `1,1,2,1,NONMEMBER` | 2 | `2 / 1` | identity action row is copied and falsely marked accepted |
| `zero-member` | `1,1,2,0,MEMBER` | 2 | `2 / 1` | literal `D theta=0`, but v12 records `z=[1,0]` |
| `zero-nonmember` | `1,0,0,0,NONMEMBER` | 2 | `2 / 1` | literal `C(O theta)=1`; zero eta erases the decisive obstruction |
| `post-c-cancel` | `2,1,2,1,MEMBER` | 3 | `3 / 1` | swap action should create the second joint row but copies the sole seed |

There are 19 shaped records, 13 hard-coded `accepted=True` records, but only
six independent rows actually retained by the v12 owner.  The receipt calls
the accepted-flag sums `(4,2,2,2,3)` its `closure_rank`; it never compares
those values with the exported owner ranks `(2,1,1,1,1)` or with the frozen
expected ranks `(2,1,1,1,2)`.  The owner also has width 15 because it includes
theta in the mathematical row, while the commissioned closure owner is the
13-coordinate `(z,eta)` joint image with theta retained as ancestry.

No v12 case contains a left-kernel basis, kernel reconstruction, `Hd1`,
slice-membership proof, MEMBER ancestry, or NONMEMBER dual.  Therefore none
of the five terminal labels is an arithmetic result.

## 3. `RetainedF3Basis` invariant: refuted twice

The literal v12 class does not satisfy the invariant claimed in reply334.

### 3.1 Dependent-row sign counterexample

Let the accepted roster contain one nonzero raw row `r`, with pivot transform
`[1]`, and reduce the dependent candidate `r`.  Lines 68--69 perform

```text
remainder <- r - r = 0
coeff     <- 0 - 1*[1] = [2].
```

The invariant actually maintained by those lines is
`remainder = candidate + coeff*R`, so a zero remainder implies
`candidate = -coeff*R`.  The method nevertheless returns `[2]` as though it
were direct coefficients.  Its own `replay([2])` is `2r`, not `r`.  No caller
negates it.

### 3.2 Roster-growth width counterexample

After one accepted row, the old transform has width one.  On accepting a
second independent row, line 75 creates a new width-two transform but never
appends a zero to old transforms.  If the old row has zero in the new pivot,
line 79 is skipped and its transform remains width one.  If it is nonzero,
the `zip(old_transform, new_transform)` at line 79 truncates to the old width
and still loses the new coordinate.  Thus immediately after the second
independent nonzero-member seed, `len(raw)==2` but the first transform has
length one.  `replay` line 82 would reject it; `export` line 86 does not
replay or even check transform widths.

The transcript coefficients are independently false.  Every record gets
either `[1]` or `[0]`, regardless of roster size or elimination.  For example,
the second independent nonzero-member seed has a one-coordinate `[1]` instead
of a two-coordinate direct vector, and every shaped dependent action has
`[0]` although its raw candidate is nonzero.  Moreover, six records marked
dependent are never sent to `RetainedF3Basis` at all, and seven records marked
accepted reduce to dependencies whose returned data are discarded.  There
is no immutable raw-candidate replay and no composition through a kernel or
`Hd1` because neither later object exists.

Canonical F3 validation also fails.  `f3` silently accepts floats, strings,
`None`, and other unrecognized types; it does not visit stored actions,
targets, or receipts.  The checker never calls `f3` on the producer receipt.
Thus exact-int/not-bool/range validation does not precede all arithmetic.

## 4. Checker independence and certificate ruling

**Checker independence: REJECT.**

The driver passes the 615-byte v12 wrapper to both CLIs.  The producer first
checks that wrapper and then loads the pinned v11 source itself.  The checker
instead sends the wrapper directly to `validate_literal_fixture`, whose line
38 requires the v11 schema.  Its own pinned `source_fixture` function at
lines 34--36 is dead code.  Hence the checker deterministically returns exit
1 before reconstructing a case.

Even after replacing that input, the checker is not independent:

- `independent_transcript` repeats the producer's same `POPS` table, rank
  table, modulo-seed copying, zero eta placeholders, accepted formula,
  normalization, and one-coordinate coefficients.  It applies no action,
  `D`, `O`, or `C` matrix.
- `replay` line 89 asks for top-level `got["transcript_sha256"]`, but the
  producer stores that field only inside `got["transcript"]`; this is a
  second deterministic checker failure after the fixture mismatch.
- The five dense tableaus are built from all shaped records, including
  dependencies, and their only gate is that a digest is a string.  Their
  rank, transforms, and span are never compared with the producer owner.
  `two_way_span=True` at line 92 is a Boolean assertion, not a check.
- The checker never inspects `closure_rank`, `closure_owner`, target,
  terminal, left kernel, `Hd1`, ancestry, or dual, and none of the latter
  four certificate objects is present.
- It does not validate the producer schema/status/terminal, recompute the
  producer `self_digest_sha256`, validate an envelope, or construct a verdict
  from arithmetic.  In production it trusts only a copied terminal string.

The producer does emit a top-level canonical digest if it reaches output, and
the checker would emit one for its own output.  No independent consumer
validates either seal.  Driver line 27 merely computes the SHA-256 of the
entire checker file and tests that any SHA-256 string has length 64; it does
not compare that hash with an envelope or recompute the canonical internal
seal.  It does not even perform the analogous whole-file operation for the
producer receipt.

## 5. Mutation ledger: 34 producer plus 34 checker owners

Abbreviations below:

- `P-FORCED`: producer adds a generic `"mutation"` key to a three-field toy
  object and explicitly raises `SemanticReject` at line 137.
- `C-FORCED`: checker constructs another generic toy object and explicitly
  raises `IndependentReject` at line 80.
- `P/C-TOY-F3`: `[3]` reaches the recursive range check, but only in that toy
  object, not in a production-shaped receipt coefficient owner.

The checker does not recompute `canonical_before`, `canonical_after`, or
`resealed`; it only compares the three producer strings.  It ignores recorded
stage and reason.  Consequently every row is a failed owner mutation even
though the narrow exception class itself is used.

| owner / code | producer path | checker path | ruling |
|---|---|---|---|
| `field_modulus / M_FIELD_MODULUS` | P-FORCED | C-FORCED | FAIL |
| `theta_seed / M_THETA_SEED` | P-FORCED | C-FORCED | FAIL |
| `theta_action / M_THETA_ACTION` | P-FORCED | C-FORCED | FAIL |
| `z_action / M_Z_ACTION` | P-FORCED | C-FORCED | FAIL |
| `eta_action / M_ETA_ACTION` | P-FORCED | C-FORCED | FAIL |
| `D_entry / M_D_ENTRY` | P-FORCED | C-FORCED | FAIL |
| `O_entry / M_O_ENTRY` | P-FORCED | C-FORCED | FAIL |
| `C_entry / M_C_ENTRY` | P-FORCED | C-FORCED | FAIL |
| `action_order / M_ACTION_ORDER` | P-FORCED | C-FORCED | FAIL |
| `premature_C / M_PREMATURE_C` | P-FORCED | C-FORCED | FAIL |
| `target / M_TARGET` | P-FORCED | C-FORCED | FAIL |
| `seed_index / M_SEED_INDEX` | P-FORCED | C-FORCED | FAIL |
| `parent / M_PARENT` | P-FORCED | C-FORCED | FAIL |
| `row_theta / M_ROW_THETA` | P-FORCED | C-FORCED | FAIL |
| `left_kernel / M_LEFT_KERNEL` | P-FORCED | C-FORCED | FAIL |
| `Hd1 / M_HD1` | P-FORCED | C-FORCED | FAIL |
| `member_ancestry / M_MEMBER_ANCESTRY` | P-FORCED | C-FORCED | FAIL |
| `dual / M_DUAL` | P-FORCED | C-FORCED | FAIL |
| `terminal / M_TERMINAL` | P-FORCED | C-FORCED | FAIL |
| `production_input / M_PRODUCTION_INPUT` | P-FORCED | C-FORCED | FAIL |
| `closure_queue_pops / M_CLOSURE_QUEUE_POPS` | P-FORCED | C-FORCED | FAIL |
| `context_pops / M_CONTEXT_POPS` | P-FORCED | C-FORCED | FAIL |
| `closure_candidate_count / M_CLOSURE_CANDIDATE_COUNT` | P-FORCED | C-FORCED | FAIL |
| `closure_queue_bound / M_CLOSURE_QUEUE_BOUND` | P-FORCED | C-FORCED | FAIL |
| `candidate_parent / M_CANDIDATE_PARENT` | P-FORCED | C-FORCED | FAIL |
| `candidate_action / M_CANDIDATE_ACTION` | P-FORCED | C-FORCED | FAIL |
| `candidate_decision / M_CANDIDATE_DECISION` | P-FORCED | C-FORCED | FAIL |
| `candidate_normalization / M_CANDIDATE_NORMALIZATION` | P-FORCED | C-FORCED | FAIL |
| `candidate_coefficients / M_CANDIDATE_COEFFICIENTS` | P-FORCED | C-FORCED | FAIL |
| `candidate_rank / M_CANDIDATE_RANK` | P-FORCED | C-FORCED | FAIL |
| `dependent_record_deletion / M_DEPENDENT_RECORD_DELETION` | P-FORCED | C-FORCED | FAIL |
| `dependent_record_reorder / M_DEPENDENT_RECORD_REORDER` | P-FORCED | C-FORCED | FAIL |
| `f3_plus3_coefficient / M_F3_PLUS3_COEFFICIENT` | P-TOY-F3 | C-TOY-F3 | FAIL |
| `member_witness_equality / M_MEMBER_WITNESS_EQUALITY` | P-FORCED | C-FORCED | FAIL |

Static owner quality is producer **0/34** and checker **0/34**.  Honest
executed accounting is also 0/34 on each side because execution was forbidden;
in fact the earlier source failures make all mutation loops unreachable.

## 6. Driver and other certificate defects

In addition to the stale pins and fixture mismatch:

1. The driver has no SELFTEST/PRODUCTION mode input or production branch.  It
   only emits a selftest shell and does not execute that shell itself.
2. It checks five stale names per version, but v7--v11 actually own
   `..._vN.json`, `..._vN.verdict.json`, and `..._vN.sh`; line 21 checks the
   different `.producer.json`/`.checker.json` names and omits every `.sh`.
   Thus it misses three actual stale owners for each old version and its own
   v12 shell.
3. Producer SELFTEST emits no producer terminal payload, only a PASS line.
   Driver line 28 counts that PASS as a terminal.  The driver never extracts
   and compares producer/checker terminal payloads.
4. Nonempty files are required, but no sealed receipt/verdict is validated.
5. The sentinel is written at line 30 and then another generated shell check
   runs at line 31, so the sentinel write is not literally the last operation.
6. The checker error path prints a line beginning
   `R07_JOINT_SLICE_KERNEL_GENERAL_V12_CHECKER_PASS terminal=UNKNOWN_INPUT`
   while returning 1.  `UNKNOWN_RESOURCE` is accepted by the driver regex
   although the checker cannot emit it.

## 7. Exact and symbolic performance accounting

### Literal reachable work

As shipped, the generated shell fails its first producer byte test.  Hence it
starts **zero** producer/checker processes, parses zero JSON objects, creates
zero candidate rows, and writes no sentinel.

If the producer is invoked directly with the literal v12 fixture, it parses
two JSON objects (v12 wrapper and pinned v11 source).  `Meter` is global across
cases, but line 116 compares its cumulative `closure_pops` with the current
case's local `pops`.  Case 1 leaves the counter at 4; case 2 increments it to
5 and requires `5 == 1`.  The deterministic direct-producer prefix is:

| work before failure | exact count |
|---|---:|
| transcript records constructed | 12 = 10 for case 1 + 2 for case 2 |
| deque pops | 5 = 4 + 1 |
| owner `reduce` calls | 4, all in completed case 1 |
| pivot-subtraction events reported as `reductions` | 2 |
| true rank raises | 2 |
| owner exports | 1 |
| canonical hash serializations | 14 |
| mutation replays / deep copies / output serializations | 0 / 0 / 0 |

The exception is caught as `UNKNOWN_INPUT`; no receipt is written.  The
meter's `json_parses` nevertheless remains zero because neither parse bumps
it.  `serialized_bytes` would also remain zero because `write_sealed` is not
passed the meter.

If a hand-supplied producer JSON lets the checker CLI start, the checker
parses that receipt and the v12 wrapper, then fails the wrapper/v11 schema
gate before constructing a transcript, tableau, mutation, or verdict.

### Latent full shaped-record work after bypassing the early failures

These counts expose the advertised workload rather than certify reachability:

| work | producer | checker |
|---|---:|---:|
| JSON parses | 2 | 2 (receipt + wrong wrapper; pinned-source loader unused) |
| shaped candidates | 19 | 19 independently duplicated |
| deque pops | 9 | no live queue; loops over `range(pops)` |
| owner reduction calls | 13 | 0 |
| true owner rank raises | 6 | n/a |
| pivot-subtraction events | 7 | n/a |
| retained owners | 5 closure, 0 `Hd1` | 0 retained certificate owners |
| dense tableaus / raw rows | 0 | 5 / `(10,2,2,2,3)`, total 19 |
| explicit coefficient enumeration | 0 | 0 |
| explicit `deepcopy` calls | 34 generic mutations | 0 |
| mutation oracles | 34 forced/toy | 34 forced/toy |
| canonical serializations including final output | 134 | 31 |

The checker tableaus have mathematical width 15 and augmented dimensions
`10x25`, three `2x17` cases, and `3x18`; their ranks on the copied rows are
`(2,1,1,1,1)`.  They are needless work because only their digest type is
tested.

There is no `3^r` path, recursive ancestry, retry, sleep, poll, lock, thread,
pool, or Python subprocess.  This is not a performance success: kernel
dimension `d`, `Hd1` rank `h`, span solves, ancestry, and dual construction
have simply been deleted.  The only meaningful source bounds are the shaped
ones

```text
N = sum_case(seed_count + hardcoded_pops*action_count) = 19,
producer basis work = O(N*r*15),
checker tableau work = O(sum_case r_i*n_i*(15+n_i)).
```

No valid general bound in the actual closure rank, kernel dimension, or Hd1
rank can be given because the v12 source never computes the latter two and
does not let queue growth depend on the first.  The producer and checker also
duplicate the same hard-coded transcript logic; the producer's 102 generic
mutation digest serializations and checker tableaus are avoidable slow paths.
The `--seconds` option and `Meter.started` timestamp are unused.

## 8. Static reachability and smallest versioned repair

The literal SELFTEST reachability chain is:

```text
v12 driver -> stale producer pin -> STOP
direct producer -> wrapper parse -> pinned v11 parse -> case 1 ->
  cumulative/local pop comparison in case 2 -> UNKNOWN_INPUT, no receipt
direct checker with a receipt -> v12 wrapper checked as v11 ->
  UNKNOWN_INPUT, no verdict
```

Even after those failures, the missing top-level transcript digest stops the
checker, and bypassing that gate reaches only the mutually copied shaped
records and forced mutations.  There is no route to a sealed semantic PASS.

The producer's no-`--selftest` branch and the checker's no-`--selftest` branch
do contain the declared literal
`STATIC_BLOCKED:actual typed matrices are not staged`.  If invoked manually,
the checker trusts only that producer terminal string.  The driver has no
production route.  In all cases production supplies no actual A5/A6
milestone.

The smallest honest repair is a **new v13 semantic rebase on the immutable
v11 implementation**, not incremental patching of the v12 shaped-record
stub:

1. Retain v11's literal `D/O`, action-matrix, live rank-raising closure,
   post-closure `C`, nullspace, `Hd1`, target, ancestry, and dual code.  Add a
   complete producer-order candidate transcript at the point each real seed
   or action candidate is reduced; derive every parent, decision, rank,
   normalization, and coefficient from that live owner.
2. Preserve v11's correct coefficient sign and zero-pad every transform on
   roster growth.  Replay every accepted and dependent raw candidate and add
   exact recursive F3/shape validation before any modulo operation.
3. Replace v11's exponential checker searches with a genuinely checker-owned
   polynomial bottom-pivot tableau, ordinary nullspace and solve routines,
   and two-way closure/kernel/`Hd1` containment.  Load the pinned v11 source
   explicitly rather than treating the v13 wrapper as that source.  Do not
   compare noncanonical MEMBER witnesses.
4. Implement all 34 mutations against the actual raw case, transcript,
   receipt, or verdict owner; reseal the real envelope and require the exact
   registered stage/code/reason through the normal semantic validator.  No
   explicit raise may stand in for owner rejection.
5. Repin actual bytes, restore selectable SELFTEST/PRODUCTION paths, stale
   reject the real six outputs per version, independently validate both
   canonical seals, compare exact-one nonempty terminal payloads, and make the
   sole sentinel write the last operation.

No fixture expansion, actual matrix staging, workflow, or execution is part
of that repair.

```text
BYTE IDENTITIES:                                PASS
V11 IMMUTABILITY / V12 SOURCE-FIXTURE PIN:      PASS
V12 DRIVER PINS:                                REJECT
LITERAL 30 BASE/BINDING PAIRS / SIX ACTIONS:    PRESENT BUT UNUSED
ACTUAL FIVE-CASE ARITHMETIC:                    REJECT
RETAINED COEFFICIENT INVARIANT:                 REJECT
CHECKER INDEPENDENCE / TWO-WAY CERTIFICATES:    REJECT
PRODUCER MUTATION OWNERS:                       0/34 STATIC; 0/34 ACTUAL
CHECKER MUTATION OWNERS:                        0/34 STATIC; 0/34 ACTUAL
PERFORMANCE / ACTUAL-READY BOUNDS:              REJECT BY OMISSION
SELFTEST STATIC REACHABILITY:                   REJECT
PRODUCTION:                                     STATIC_BLOCKED / NO DRIVER PATH

AUDIT:                         REJECT
EXECUTION:                     UNEXECUTED
SYNTHETIC SELFTEST AUTHORIZED: NO
ACTUAL A5 / ACTUAL A6:         0/3 / 0/3
LIFT / FAKE / IHARA:           NONE
```

`TASK335_R07_TASK334_V12_CODE_PERFORMANCE_AUDIT`
