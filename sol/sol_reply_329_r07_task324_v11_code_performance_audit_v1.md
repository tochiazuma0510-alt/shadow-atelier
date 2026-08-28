# Sol(max) reply 329 - task324/v11 independent code and performance audit

## Verdict

**REJECT / UNEXECUTED.  No synthetic GHA SELFTEST is authorized.**

The v11 byte pins, literal v10 freeze, five mathematical cases, retained
coefficient invariant, core checker independence, narrow exception boundary,
all 19 producer mutations, all 19 checker mutations, and the driver terminal
rules pass static inspection.  The v10 ancestry, mirrored-checker, broad-catch,
wrong-owner, and repeated-RREF blockers are materially repaired.

There are nevertheless four load-bearing v11 defects.

1. **The receipt replay is incomplete.**  Producer fields
   `closure_queue_pops` and `closure_queue_bound` are emitted at producer
   lines 649--650, but checker `audit_receipt` lines 705--813 never compare
   either field with `context["pops"]`, `context["maximum_pops"]`, or the
   number of closure reduction records.  The checker also does not bind the
   top-level `production_input` scalar.  Thus, for example, the `zero-member`
   receipt can have both queue scalars changed to zero and all enclosing
   seals recomputed while every v11 checker gate still accepts.  In the
   `nonzero-member` case the two dependent reduction records can likewise be
   deleted, the owner/change/case/top seals and affected mutation-control
   digests recomputed, and the remaining owner checks still pass:
   `verify_owner_export` requires only accepted-count equality, not the
   independently reconstructed candidate/pop transcript.
   Consequently the advertised queue-exhaustion and all-candidate transcript
   are not certificate-bound.
2. **The performance contract is not met.**  Producer lines 641--642 replay
   both owner exports and `audit_certificate` lines 945--946 replay the same
   exports again.  Producer lines 955--963 rebuild the already-owned Hd1
   independent list by coefficient enumeration.  On the checker side,
   closure containment, complete kernel construction, kernel-basis selection,
   left-kernel span comparison, and Hd1 selection repeatedly enumerate
   coefficient spaces even though dense retained tableaus are then built.
   The frozen fixture keeps every exponent at most two, but the algorithm is
   `3^r`, not actual-ready: checker lines 438 and 617 enumerate all
   coefficients with `repeat=len(rows)`, and basis selection nests further
   exhaustive containment.  V242 does not bound the actual joint-image rank
   by two; its occurrence-lifted joint width alone contains eleven occurrence
   coordinates.  This is precisely a latent `3^11`-or-worse production path.
3. **The checker imposes an unjustified equality on a nonunique witness.**
   Checker line 793 requires the producer `member_theta` to equal the
   checker's independently selected `member_theta`.  Both are vectors in the
   common Theta coordinates, but v242 Theorem 5.1 requires only a valid
   witness; it supplies neither injectivity of the map from the endpoint-zero
   slice nor a canonical-witness rule.  Different closure/kernel bases can
   therefore give different valid theta witnesses for the same target.  The
   direct producer ancestry is already replayed at lines 669--692.  The extra
   equality can reject a valid actual MEMBER certificate.
4. **Canonical F3 receipt data and the final verdict seal are not fully
   enforced.**  Raw fixture scalars are typed and range-checked, but receipt
   transforms, reduction coefficients, direct coefficients, kernel
   coefficients, ancestry coefficients, and dual coefficients are mostly
   consumed modulo 3 without an exact `int`/`0 <= x < 3` check.  For a concrete
   static counterexample, add 3 to a `zero-member` owner transform coefficient
   and recompute its reconstruction/owner/change/case/top seals; checker
   `combine` reduces it modulo 3 and accepts it.  The case is not the baseline
   for any certificate mutation record, so no other field forces the canonical
   representative.  In addition, the driver only counts a 64-hex
   `verdict_digest_sha256` substring (lines 63 and 73); no independent consumer
   recomputes the checker verdict seal.  In PRODUCTION the producer receipt
   seal is likewise only pattern-counted because the checker intentionally
   does not load that static receipt.

These are contract failures even though the frozen synthetic data would
otherwise traverse the intended success path.  No program or workflow was
run, and no executable outcome is inferred.

## 1. Inputs and exact file identities

The exact task307 name commissioned by task324,
`sol/luna_task_307_r07_actual_joint_slice_kernel_general_v7.md`, is absent.
The sole task307/v7 kickoff is
`sol/luna_task_307_r07_task304_solmax_reject_repair_v7.md` (3756 bytes,
SHA-256 `861b8996ce7e04e9cf5ac54eef218729673a0b297cbb193c9e2dcc011868c7e1`).
It is the same substitution disclosed by Luna.  Because that unique kickoff,
the complete v10/v11 quartets, task322 and its reply, task320's reply, and
v242 were all available, the filename discrepancy does not block this code
audit.  V242 was read at 11469 bytes / SHA-256
`9108e1fd267f658983c5d6809a69444baa06ab3f571ae4fb1d3d515a8c6ccb6f`.

Independent current v11 identities are:

| file | bytes | SHA-256 | ASCII / CR / trailing LF |
|---|---:|---|---|
| `search/d972_r07_joint_slice_kernel_general_v11.py` | 48381 | `52fa8eb2dc784012f087b0790661f94e446746253e6fe0d8a28dea5a49db84b8` | yes / 0 / 1 |
| `crosscheck/check_d972_r07_joint_slice_kernel_general_v11.py` | 52662 | `c22fab29394e6d4fb2a7c6e0042547c5adaba9308794d9e2c654757e24176f26` | yes / 0 / 1 |
| `search/d972_r07_joint_slice_kernel_general_gha_driver_v11.g` | 7102 | `a760d863325c33994b016db233c5487a0650a2aed8bc16cbeaa6b8db62b0ca7f` | yes / 0 / 1 |
| `search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json` | 12964 | `cab24a5e6ddd7812094b920bffd7688564092a3c9b718484bf3f887cf59d2058` | yes / 0 / 1 |

The three driver pins equal the producer/checker/fixture identities exactly;
there is deliberately no recursive driver hash.  The v10 quartet remains at
its commissioned identities:

| file | bytes | SHA-256 |
|---|---:|---|
| producer v10 | 15310 | `54e9264ab6d1771970493c766b10601e848ec6fd432eae7f9d4e1a938753ead8` |
| checker v10 | 28812 | `e186e3ec67adbb8199f78fd15f09eaa36c3e28c2954d39c3bce80648b811b739` |
| driver v10 | 6417 | `6ffe5fe493627fb096387d0ac42a6f22da0351d747d52ba2997789fcd7833a1e` |
| fixture v10 | 10356 | `645eac3beb37c65803d44bdd3661ddb77f757182fe257cb5809db562bc8240e9` |

All eight load-bearing files are ASCII, contain no CR, and have exactly one
final LF.  After replacing only schema and fixture-seal values and deleting
v11 `mutation_registry`, the parsed v10 and v11 fixture objects are exactly
equal.  Hence the five cases, 30 base/binding pairs, six actions, twelve v10
trailing-zero repairs, action/case order, targets, and expected objects are
unchanged.

## 2. Literal mathematics and all five cases

All 30 base/binding pairs are literal equalities.  In every case their shapes
are respectively

```text
A_theta 2x2, A_Z 2x2, A_E 11x11,
D 2x2, O 11x2, C 1x11.
```

All entries are literal integers in `{0,1,2}`.  The six stored actions are
`nonzero-member/m,n` and one `m` action in each other case; every stored
theta/z/eta action is respectively 2x2, 2x2, and 11x11 and is invertible.
Both programs perform the complete five-case base/binding and stored-action
preflight before compilation or replay.

The convention is matrix times column vector over F3.  Accepted mathematical
rows are stored as lists only for row-span elimination.  If the accepted joint
rows are `(z_j,eta_j)`, the producer forms the `qdim x r` matrix
`(C eta_j)` and takes its column nullspace.  Thus its null vectors are exactly
the left coefficients on accepted joint rows.  `C` is first applied at
producer lines 564--567 and checker lines 435--447, after invariant closure.
The resulting `h_a=sum a_j z_j` rows have the correct orientation for target
row-span membership.  NONMEMBER duals annihilate all Hd1 rows and pair to 1
with the target.  No target sign is silently changed.

| case | closure / post-C kernel / Hd1 | target and certificate | exact tuple |
|---|---|---|---|
| `nonzero-member` | Seeds `e1,e2` give rank 2. `m` swaps them and `n=2m`; the two new scalar multiples are dependent. `C=0`, so `N=F3^2` (dimension 2, 8 nonzero) and `Hd1=F3^2`. | `(1,1)` is MEMBER with theta `(1,1)`. | `2,2,8,2,MEMBER,[1,1],null` |
| `outside-nonmember` | One `e1` joint row, identity action, rank 1. `C=0`, so `N=F3`, and `Hd1=<e1>`. | `e2` is NONMEMBER; dual `e2`. | `1,1,2,1,NONMEMBER,null,[0,1]` |
| `zero-member` | The occurrence row is nonzero but its z row is zero. `C=0`, so `N=F3` and Hd1 consists of a zero row, rank 0. | Zero target is MEMBER with zero theta. | `1,1,2,0,MEMBER,[0,0],null` |
| `zero-nonmember` | One nonzero occurrence row has `C eta=1`; hence `N=0` and `Hd1=0`. | `e1` is NONMEMBER; dual `e1`. | `1,0,0,0,NONMEMBER,null,[1,0]` |
| `post-c-cancel` | Swap closure gives `e1,e2`; their C-images are `(1,1)`. Producer kernel basis is `(2,1)` and checker lex basis is `(1,2)`, the same line. | `(1,2)=2(2,1)` is MEMBER with theta `(1,2)`. | `2,1,2,1,MEMBER,[1,2],null` |

Queue pops are exactly `(4,1,1,1,2)`, declared bounds are
`(6,3,3,3,3)`, and closure ranks are `(2,1,1,1,2)`.  This gives nine pops,
seven accepted closure rows, kernel dimensions `(2,1,1,0,1)`, and Hd1 ranks
`(2,1,0,0,1)`.  The five literal expected tuples are therefore 5/5 correct.

## 3. `RetainedF3Basis` coefficient invariant

The claimed invariant is correct.

Let `R` be the accepted raw-row roster and let an owned pivot row satisfy
`b_p = T_p R`.  During reduction of a candidate `x`, producer lines 211--228
maintain

```text
x = c R + v,
```

where `v` is the current remainder.  Eliminating pivot multiple `q` replaces
`v` by `v-q b_p` and `c` by `c+q T_p`; hence the displayed equality is
preserved.  There are two terminal branches.

- If `v=0`, the returned prior-roster vector `c` directly reconstructs the
  dependent raw candidate.  Later accepted rows only append zero coordinates.
- If `v` has pivot `p` and normalization scalar `s`, the new normalized row is
  `s v=(-s c,s)(R,x)`.  Lines 238--246 first zero-pad every old transform and
  then install exactly this new transform.  Lines 247--256 eliminate the new
  pivot from every old row and apply the identical add operation to its
  transform.  Thus all old and new normalized rows remain direct combinations
  of the immutable accepted raw roster.

Accepted candidates receive the new identity coordinate; dependent candidates
retain their reduction coordinates.  `_padded_reductions` pads both branches,
replays `prior coefficients + remainder = raw`, and separately replays the
final direct coefficients.  `export` checks normalized pivot positions,
zeroes at other pivots, every transform, every raw-row containment, and all
digests.  All rank, index, pivot, and coefficient fields are assigned on both
accepted and dependent branches, including the empty Hd1 owner in the
zero-member and zero-nonmember cases.

The MEMBER composition is also correctly oriented: Hd1-owner raw coordinates
are expanded through `raw_labels` to kernel-basis coordinates, multiplied by
the left-kernel basis to closure-row coordinates, and then applied directly to
theta, z, and eta.  These are immutable accepted raw-row coordinates, not
pivot-column coordinates.  Thus task322's coefficient-ancestry blocker is
closed.

## 4. Checker independence and replay decision

**Core algorithmic independence: PASS.  Complete checker contract: REJECT.**

The checker imports no producer module.  Closure acceptance uses exhaustive
coefficient containment and reverse action traversal.  After the complete raw
list is selected, `DenseTableau` builds `[raw | I]`, chooses the bottom
available pivot rather than the producer's online first-pivot update, and
performs full Gauss--Jordan operations on both halves.  Kernel vectors are
selected from a lexicographically enumerated full kernel, rather than by the
producer nullspace.  Checker and receipt closure/kernel/Hd1 spans are compared
by containment of mathematical rows, never by equality of coordinate vectors
from the two tableaus.  Producer transforms and direct reductions are replayed
against producer raw rows without importing or calling `RetainedF3Basis`.

Those facts make the linear-algebra implementation genuinely helper-nonshared
and algorithmically different.  They do not cure the incomplete queue-field
binding, noncanonical receipt coefficients, exponential actual path, or the
noncanonical MEMBER-witness equality described in the verdict.  In particular,
the fixture happens to leave all accepted closure rows in the same raw order in
producer and checker; reversing the distinct actions changes only dependent
candidate order.  The bottom-pivot and kernel-basis canaries still exercise a
different tableau, but no fixture canary tests two different valid theta
witnesses.

## 5. Mutation ledger: 19 producer plus 19 checker gates

Every row below is statically reachable.  The named owner value changes on the
selected literal case, the complete scoped object changes, the raw mutation is
sealed with `mutation_fixture_seal` or the certificate mutation is resealed
with `case_digest_sha256`, and only the narrow `SemanticReject` /
`IndependentReject` exception is counted.  Stage, code, and reason are matched
exactly; unrelated Python exceptions escape the mutation boundary and are
fatal.  Checker records must equal the independently reconstructed producer
records field for field.

| owner (scope/case) | producer gate | checker gate | exact reason |
|---|---|---|---|
| `field_modulus` (raw/1) | `raw.field_modulus / M_FIELD_MODULUS` STATIC | `raw.field_modulus / M_FIELD_MODULUS` STATIC | `field modulus is not F3` |
| `theta_seed` (raw/1) | `raw.theta_seed / M_THETA_SEED` STATIC | `raw.theta_seed / M_THETA_SEED` STATIC | `theta seed binding changed` |
| `theta_action` (raw/1) | `raw.theta_action / M_THETA_ACTION` STATIC | `raw.theta_action / M_THETA_ACTION` STATIC | `theta action owner changed` |
| `z_action` (raw/1) | `raw.z_action / M_Z_ACTION` STATIC | `raw.z_action / M_Z_ACTION` STATIC | `z action owner changed` |
| `eta_action` (raw/1) | `raw.eta_action / M_ETA_ACTION` STATIC | `raw.eta_action / M_ETA_ACTION` STATIC | `eta action owner changed` |
| `D_entry` (raw/1) | `raw.D_entry / M_D_ENTRY` STATIC | `raw.D_entry / M_D_ENTRY` STATIC | `D map owner changed` |
| `O_entry` (raw/1) | `raw.O_entry / M_O_ENTRY` STATIC | `raw.O_entry / M_O_ENTRY` STATIC | `O map owner changed` |
| `C_entry` (raw/1) | `raw.C_entry / M_C_ENTRY` STATIC | `raw.C_entry / M_C_ENTRY` STATIC | `C map owner changed` |
| `action_order` (raw/1) | `raw.action_order / M_ACTION_ORDER` STATIC | `raw.action_order / M_ACTION_ORDER` STATIC | `action order binding changed` |
| `premature_C` (raw/1) | `raw.premature_C / M_PREMATURE_C` STATIC | `raw.premature_C / M_PREMATURE_C` STATIC | `C was applied before closure` |
| `target` (raw/1) | `raw.target / M_TARGET` STATIC | `raw.target / M_TARGET` STATIC | `target membership changed` |
| `seed_index` (certificate/0) | `certificate.seed_index / M_SEED_INDEX` STATIC | `certificate.seed_index / M_SEED_INDEX` STATIC | `certificate seed index is invalid` |
| `parent` (certificate/4) | `certificate.parent / M_PARENT` STATIC | `certificate.parent / M_PARENT` STATIC | `certificate parent is invalid` |
| `row_theta` (certificate/0) | `certificate.row_theta / M_ROW_THETA` STATIC | `certificate.row_theta / M_ROW_THETA` STATIC | `certificate row theta does not replay` |
| `left_kernel` (certificate/0) | `certificate.left_kernel / M_LEFT_KERNEL` STATIC | `certificate.left_kernel / M_LEFT_KERNEL` STATIC | `left-kernel basis content changed` |
| `Hd1` (certificate/1) | `certificate.Hd1 / M_HD1` STATIC | `certificate.Hd1 / M_HD1` STATIC | `Hd1 content changed` |
| `member_ancestry` (certificate/0) | `certificate.member_ancestry / M_MEMBER_ANCESTRY` STATIC | `certificate.member_ancestry / M_MEMBER_ANCESTRY` STATIC | `member theta ancestry does not replay` |
| `dual` (certificate/1) | `certificate.dual / M_DUAL` STATIC | `certificate.dual / M_DUAL` STATIC | `separating dual does not replay` |
| `terminal` (certificate/1) | `certificate.terminal / M_TERMINAL` STATIC | `certificate.terminal / M_TERMINAL` STATIC | `certificate terminal changed` |

In particular, the seven v10 wrong-owner controls now mutate produced
certificate objects.  `parent` uses the actual action row in case 4;
`left_kernel` duplicates one of the two actual basis rows; `Hd1`, ancestry,
dual, and terminal mutate fields that exist on their selected cases.  The raw
count is therefore producer 19/19 STATIC and checker 19/19 STATIC, while the
only honest executed counts remain 0/19 and 0/19.  The mutation roster itself
passes; it simply does not cover the unbound queue/canonicality fields found
above.

## 6. Independently derived performance accounting

Let

```text
queue pops p = (4,1,1,1,2),       sum 9
closure ranks r = (2,1,1,1,2),    sum 7
kernel dimensions d = (2,1,1,0,1),sum 5
Hd1 ranks h = (2,1,0,0,1),        sum 4.
```

### Producer

| work | exact successful five-case SELFTEST count |
|---|---:|
| invertibility RREFs | 33 = 15 base + 18 stored-action; maximum 11x11 |
| left-kernel nullspace RREFs | 5; maximum 1x2 |
| retained closure owners / insertion attempts | 5 / 9; width 13, rank at most 2 |
| retained Hd1 owners / insertion attempts | 5 / 5; width 2, rank at most 2 |
| full `replay_owner_export` calls | 20 = two per owner; one complete set of 10 is redundant |
| coefficient tuples visited by `itertools.product` | 23 = 6 dual + 7 baseline kernel-independence + 7 duplicate Hd1 selection + 3 left-kernel mutation |
| full-object mutation deep copies | 19, plus one copied kernel row |
| JSON parses | 1 fixture parse |

There are no remaining producer rank/RREF queries over known closure or Hd1
bases.  However, the duplicate export replays and the seven-tuple second Hd1
basis construction are avoidable known-basis work.  Counting every successful
path call to `digest`, the producer performs 249 canonical hash
serializations, followed by one final canonical output serialization.  The
large count comes from replaying every owner, pivot, reduction, and mutation
digest repeatedly.  There are 99 explicit `copy.deepcopy` calls on the full
successful path (79 during owner construction/export and 20 in mutation
construction, including the copied kernel row).

### Checker

| work | exact successful five-case SELFTEST count |
|---|---:|
| independent invertibility eliminations | 33 = 15 base + 18 stored-action; maximum 11x11 |
| checker raw dense tableaus | 15 = closure/kernel/Hd1 per case |
| receipt dense tableaus | 15 = closure/kernel/Hd1 per case |
| dense-tableau solves/containment queries | 48, including two mutation queries |
| coefficient tuples visited by `itertools.product` | 201 total |
| full-object mutation deep copies | 19, plus one copied kernel row |
| JSON parses | 2 = fixture once and producer receipt once |

The 201 checker coefficient tuples split exactly as follows:

```text
independent raw reconstruction:
  closure containment 21 + full kernels 27 + kernel basis selection 50
  + Hd1 basis selection 7 + dual search 6                         = 111
receipt audit:
  second full kernels 27 + kernel independence 7 + kernel two-way 26
  + Hd1 reverse containment 11 + receipt Hd1 selection 7          = 78
left-kernel mutation:
  full kernel 9 + duplicate-vector independence 3                 = 12
TOTAL                                                               201
```

Every individual frozen-fixture enumeration has exponent at most two and at
most nine vectors.  That makes the proposed synthetic run finite; it does not
make the algorithm actual-ready.  For general closure rank `r`, lines 438 and
617 each cost `3^r`; selection from the resulting kernel can make repeated
containment cost proportional to `(3^d-1)3^d`.  No source guard proves
`r <= 2` for the future v242 inputs.  The list queues are bounded in the
fixture (capacities `6,3,3,3,3`, total 18), but `pop(0)` also performs avoidable
left shifts and should become a deque before a larger actual closure.

The checker performs 203 canonical hash serializations and one final output
serialization on the successful path.  This includes 30 tableau transcript
digests and 117 mutation-path digest calls.  It has 20 explicit deep-copy
calls including the copied kernel row.  There are no JSON round-trip copies.

No Python file contains a retry, sleep, poll, lock, thread, pool, background
child, subprocess, or unbounded queue.  The driver alone emits one serial
producer invocation followed by one checker invocation.

## 7. Driver and static reachability

The v11 driver stale-rejects exactly six outputs for each version v7 through
v11 (30 paths).  In either selected mode it writes one producer command and
then one checker command.  SELFTEST requires exactly one full-line producer
PASS, checker PASS with `19/19`, producer terminal, and checker terminal.
PRODUCTION requires exactly one full-line static terminal from each program.
Both terminal payloads must be nonempty and equal.  The `.ok` write is the
last generated shell operation, and the GAP wrapper then checks that the
sentinel exists and is nonempty.  These terminal and sentinel rules pass.

Static source tracing reaches all five baseline case outcomes, the producer
wrong-fixture-seal canary, 19 producer semantic gates, the checker wrong
fixture seal and wrong producer seal canaries, and 19 checker semantic gates.
The outer checker catch converts unrelated failures to `UNKNOWN_INPUT`; the
driver's exact PASS/terminal gates reject that path.  PRODUCTION does not read
or infer actual matrices and remains exactly

```text
STATIC_BLOCKED:actual typed matrices are not staged
```

Thus this remains a synthetic code candidate, not an A5/A6 computation.

## 8. Smallest versioned repair

A smallest v12 repair should preserve the v10/v11 fixture mathematics and
make only the following code/receipt changes.

1. Bind `closure_queue_pops == context["pops"] ==
   len(closure_owner["reductions"])`, bind the declared queue bound to the
   independently derived bound, bind `production_input`, and either replay
   the complete producer-order candidate transcript from raw fixture data or
   stop certifying dependent-candidate records.
2. Apply exact recursive F3 type/range and dimension checks to every receipt
   coefficient/vector before any modulo operation.  Add canaries for a `+3`
   coefficient and for each formerly unbound scalar/transcript.
3. Remove exact equality with the checker's independently selected
   `member_theta`; retain the already-complete direct receipt ancestry replay.
   Alternatively specify and prove a common canonical witness in an immutable
   raw basis before comparing it.
4. Remove one of the two producer `replay_owner_export` sets and replace the
   producer Hd1 re-selection with the retained owner.  In the checker, replace
   general-path exhaustive closure/kernel/span searches by checker-owned
   bottom-pivot incremental/tableau and nullspace operations; any exhaustive
   rank-two toy canary must be explicitly SELFTEST-only and guarded by the
   frozen rank bound.  Remove the duplicated left-kernel/Hd1 span passes and
   use a deque.
5. Have an independent consumer recompute the complete checker verdict seal
   (and the static production receipt seal), rather than count only a 64-hex
   substring.  Keep the one-producer/one-checker process rule by doing this in
   the driver or by binding a driver-computed full-file digest.

No fixture expansion, actual input staging, or mathematical result is needed
for this repair.

```text
BYTE / PIN / V10 IMMUTABILITY:                  PASS
LITERAL BASE/BINDING PAIRS:                     30/30 PASS
LITERAL STORED ACTIONS:                         6/6 PASS
FIVE EXPECTED TUPLES:                           5/5 STATIC
RETAINED COEFFICIENT INVARIANT:                 PASS
CORE CHECKER ALGORITHM INDEPENDENCE:             PASS
COMPLETE RECEIPT / CANONICALITY REPLAY:          REJECT
PRODUCER MUTATION PATHS:                         19/19 STATIC; 0/19 ACTUAL
CHECKER MUTATION PATHS:                          19/19 STATIC; 0/19 ACTUAL
PERFORMANCE / ACTUAL-READY BOUNDS:               REJECT
DRIVER TERMINALS / SENTINEL LAST:                PASS
OVERALL:                                         REJECT / UNEXECUTED

AUDIT:                         REJECT
EXECUTION:                     UNEXECUTED
SYNTHETIC SELFTEST AUTHORIZED: NO
ACTUAL A5 / ACTUAL A6:         0/3 / 0/3
LIFT / FAKE / IHARA:           NONE
```

`TASK329_R07_TASK324_V11_CODE_PERFORMANCE_AUDIT_COMPLETE`
