# Luna reply 324 - task320 v11 ancestry-independent incremental repair

## Verdict and scope

**IMPLEMENTED / UNEXECUTED.**  The five authorized v11 paths were created and
no v7--v10 path was edited.  No Python, Node, GAP, GHA, workflow, network, or
git command was run.  Consequently no SELFTEST PASS, production result, or
actual mathematical result is claimed.

The commission names
`sol/luna_task_307_r07_actual_joint_slice_kernel_general_v7.md`, which is not
present in this worktree.  I read the complete sole task307/v7 kickoff at its
repository name,
`sol/luna_task_307_r07_task304_solmax_reject_repair_v7.md`, together with all
other commissioned inputs and the complete v10 producer, checker, driver,
and fixture.  This filename discrepancy did not require weakening a code or
receipt gate.

## Final load-bearing identities

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_joint_slice_kernel_general_v11.py` | 48381 | `52fa8eb2dc784012f087b0790661f94e446746253e6fe0d8a28dea5a49db84b8` |
| `crosscheck/check_d972_r07_joint_slice_kernel_general_v11.py` | 52662 | `c22fab29394e6d4fb2a7c6e0042547c5adaba9308794d9e2c654757e24176f26` |
| `search/d972_r07_joint_slice_kernel_general_gha_driver_v11.g` | 7102 | `a760d863325c33994b016db233c5487a0650a2aed8bc16cbeaa6b8db62b0ca7f` |
| `search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json` | 12964 | `cab24a5e6ddd7812094b920bffd7688564092a3c9b718484bf3f887cf59d2058` |

All four files are ASCII, have zero CR bytes, and have exactly one final LF.
The driver embeds the exact producer, checker, and fixture byte/SHA pins in
this table.  It deliberately has no recursive self-hash.

Read-only identity inspection also found the four v10 files unchanged at
their commissioned identities: 15310 / `54e9264...ead8`, 28812 /
`e186e3ec...b739`, 6417 / `6ffe5fe4...3a1e`, and 10356 /
`645eac3b...0e9` respectively.

## Literal freeze and v10-to-v11 ledger

After normalizing only schema and fixture seal and adding the registered
mutation metadata, a read-only PowerShell JSON comparison made the v10 and
v11 fixture objects exactly equal.  Thus the five cases, all thirty
base/binding pairs, six stored actions, action/case order, targets, twelve
v10 trailing-zero repairs, and five expected tuples are unchanged:

```text
nonzero-member       2 2 8 2 MEMBER     [1,1] null
outside-nonmember    1 1 2 1 NONMEMBER  null  [0,1]
zero-member          1 1 2 0 MEMBER     [0,0] null
zero-nonmember       1 0 0 0 NONMEMBER  null  [1,0]
post-c-cancel        2 1 2 1 MEMBER     [1,2] null
```

The exact ledger is:

1. Schema, fixture seal, paths, markers, and receipt/verdict schemas advance
   from v10 to v11.
2. The fixture adds only the 19-entry `mutation_registry`; all mathematical
   case content remains literal v10 content.  Both programs still preflight
   all 30 base/binding pairs and all six stored 2x2 / 2x2 / 11x11 actions,
   including exact integer F3 scalars, before compile or replay.
3. The producer row-only echelon is replaced by a coefficient-retaining
   online owner for closure and Hd1.
4. The mirrored checker echelon is removed.  The checker now uses bounded
   coefficient enumeration for acceptance and checker-owned dense augmented
   Gauss--Jordan tableaus for retained bases and transforms.
5. Receipt scalars, both owner transcripts, kernel reconstructions, member
   ancestry, nonmember dual, mutation canonical digests, reseals, exact
   stages/codes/reasons, and top-level output seals are now bound.
6. The driver adds v11 to stale rejection, pins the new inputs, requires
   exactly one full-line marker, checks sealed nonempty outputs, compares
   nonempty terminal payloads, and writes its only sentinel last.

Production remains exactly
`STATIC_BLOCKED:actual typed matrices are not staged` in both programs.

## Producer algorithm

`RetainedF3Basis` owns one insertion-order raw-row roster and one normalized
RREF dictionary.  Each pivot entry contains both its mathematical row and a
coefficient vector in that raw roster.

For a candidate `x`, reduction maintains the invariant

```text
x = (current coefficients) * (accepted raw rows) + remainder.
```

Subtracting a pivot multiple from the remainder adds the same multiple of
the pivot transform to the coefficient half.  If the remainder is zero, the
returned coefficients directly reconstruct the dependent candidate.  If it
is nonzero, existing transforms first receive a zero coordinate, the new
raw row receives its identity coordinate, the remainder and transform are
scaled together, and the new pivot is eliminated from every old pivot row
and old transform together.  The result is a fully normalized reduced row
and a fully normalized raw-roster transform.

Every queue pop exports its prior-roster reduction, remainder, final direct
coefficients, acceptance/index metadata, and direct reconstruction digest.
Each owner exports its explicit insertion order, raw rows, pivots, reduced
rows, transforms, per-pivot reconstruction digests, all candidate
transcripts, and an owner digest.  The producer directly replays all of these
before sealing each case and the aggregate receipt.

The closure owner is constructed once per case.  The left-kernel nullspace is
the one necessary fixed calculation.  The resulting Hd1 rows are inserted
once into a second retained owner.  Hd1 rank and target membership come from
that owner.  MEMBER coordinates are expanded from accepted Hd1 rows through
left-kernel coefficients to closure-row coefficients, then replayed directly
to theta, z, and eta.  NONMEMBER duals are checked against the retained Hd1
rows.  Producer-side two-way raw/owner span checks use these same owners and
do not build another echelon.

## Genuinely independent checker algorithm

The checker does not import producer code and does not respell the online
owner.  Its line of construction is different:

1. Closure candidates are accepted by exhaustive F3 coefficient membership
   over the already accepted list (rank at most two), with reverse action
   traversal retained as an independent ordering.
2. Only after the complete accepted list is known, `DenseTableau` builds one
   dense matrix `[raw rows | identity]`.  It chooses pivots from the bottom,
   performs full Gauss--Jordan row operations on both blocks, and obtains a
   canonical reduced tableau plus transforms back to the full raw list.
3. The checker independently enumerates the complete coefficient kernel,
   selects an independent basis by bounded coefficient containment, builds
   its kernel tableau once, reconstructs Hd1, selects its independent Hd1
   rows, and builds its Hd1 tableau once.
4. Separate receipt closure, receipt-kernel, and receipt-Hd1 tableaus are each
   built once.  Checker and receipt spans are compared only by two-way
   containment of mathematical rows.  Coordinate dictionaries or transform
   vectors from different bases are never compared.
5. Every producer transform and reduction is nevertheless replayed directly
   against the producer raw rows.  The verdict records independent transform
   digests for all six checker/receipt bases per case.
6. `closure_rank`, `kernel_dim`, full nonzero kernel cardinality, target,
   slice membership, terminal, Hd1 rank/content, member theta ancestry or
   separating dual, kernel reconstruction, owner transcripts, and the
   aggregate change-of-basis digest are all required explicitly.

## Mutation registry: 19 producer plus 19 checker gates

Each row below is one producer gate and a second independently reconstructed
checker gate.  Both sides require the same registered exact stage, code, and
reason; they use distinct narrow exception classes.  Mutation boundaries
catch only `SemanticReject` (producer) or `IndependentReject` (checker).
Unrelated `RuntimeError`, `ValueError`, `KeyError`, `TypeError`, or
`IndexError` is fatal and cannot count as rejection.

| owner | scope / case | producer expected stage / code | checker expected stage / code | exact reason |
|---|---|---|---|---|
| `field_modulus` | raw / 1 | `raw.field_modulus` / `M_FIELD_MODULUS` | same | `field modulus is not F3` |
| `theta_seed` | raw / 1 | `raw.theta_seed` / `M_THETA_SEED` | same | `theta seed binding changed` |
| `theta_action` | raw / 1 | `raw.theta_action` / `M_THETA_ACTION` | same | `theta action owner changed` |
| `z_action` | raw / 1 | `raw.z_action` / `M_Z_ACTION` | same | `z action owner changed` |
| `eta_action` | raw / 1 | `raw.eta_action` / `M_ETA_ACTION` | same | `eta action owner changed` |
| `D_entry` | raw / 1 | `raw.D_entry` / `M_D_ENTRY` | same | `D map owner changed` |
| `O_entry` | raw / 1 | `raw.O_entry` / `M_O_ENTRY` | same | `O map owner changed` |
| `C_entry` | raw / 1 | `raw.C_entry` / `M_C_ENTRY` | same | `C map owner changed` |
| `action_order` | raw / 1 | `raw.action_order` / `M_ACTION_ORDER` | same | `action order binding changed` |
| `premature_C` | raw / 1 | `raw.premature_C` / `M_PREMATURE_C` | same | `C was applied before closure` |
| `target` | raw / 1 | `raw.target` / `M_TARGET` | same | `target membership changed` |
| `seed_index` | certificate / 0 | `certificate.seed_index` / `M_SEED_INDEX` | same | `certificate seed index is invalid` |
| `parent` | certificate / 4 | `certificate.parent` / `M_PARENT` | same | `certificate parent is invalid` |
| `row_theta` | certificate / 0 | `certificate.row_theta` / `M_ROW_THETA` | same | `certificate row theta does not replay` |
| `left_kernel` | certificate / 0 | `certificate.left_kernel` / `M_LEFT_KERNEL` | same | `left-kernel basis content changed` |
| `Hd1` | certificate / 1 | `certificate.Hd1` / `M_HD1` | same | `Hd1 content changed` |
| `member_ancestry` | certificate / 0 | `certificate.member_ancestry` / `M_MEMBER_ANCESTRY` | same | `member theta ancestry does not replay` |
| `dual` | certificate / 1 | `certificate.dual` / `M_DUAL` | same | `separating dual does not replay` |
| `terminal` | certificate / 1 | `certificate.terminal` / `M_TERMINAL` | same | `certificate terminal changed` |

The seven v10 wrong-owner producer controls named by task322 now mutate the
produced certificate fields themselves.  In particular `parent` uses the
actual action row of case 4; the other receipt cases are selected so the
owned object exists.  Every control carries owned-before/after and complete
canonical-before/after SHA-256 values, the reseal field/value, and exact
semantic stage/code/reason.  The checker reconstructs the mutation and these
digests, reseals it independently, reaches its own gate, and compares the
complete observed transcript.  It does not accept producer
`{owner,rejected}` Booleans; no such Boolean is used as semantic evidence.

Actual mutation execution counts remain producer 0/19 and checker 0/19.

## Exact performance accounting

### Five baseline producer cases

| construction/query | exact count | classification |
|---|---:|---|
| base plus stored-action invertibility RREF | 33 = 15 + 18 | necessary fixed action gates; max 11x11 |
| left-kernel nullspace RREF | 5 | necessary, one 1x`r` matrix per case, `r <= 2` |
| retained closure owner | 5 | exactly one per case; width 13, rank `<= 2` |
| retained Hd1 owner | 5 | exactly one per case; width 2, rank `<= 2` |
| known closure/Hd1 rank or membership rebuild | 0 | all queries reduce against retained owners |
| member ancestry rank rebuild | 0 | direct coefficient composition and replay |

Thus all eight avoidable producer Hd1 rebuilds from task322 are removed.
Producer mutation oracles reuse the five baseline contexts and introduce no
additional RREF or retained-basis construction.

### Five baseline checker cases

| construction/query | exact count | classification |
|---|---:|---|
| base plus stored-action invertibility elimination | 33 = 15 + 18 | necessary fixed action gates; max 11x11 |
| checker raw dense tableaus | 15 = closure + kernel + Hd1 for each case | one per logically distinct raw basis |
| receipt dense tableaus | 15 = closure + kernel + Hd1 for each case | one per logically distinct receipt basis |
| other full RREF/echelon rebuild | 0 | containment and solves reuse these tableaus |
| ancestry rank rebuild | 0 | direct linear combination |

The checker therefore has exactly 30 dense augmented builds, rather than the
72 v10 Hd1/member/span/ancestry RREF calls.  All 58 duplicate or repeated
known-basis rebuilds identified by task322 are removed.  Finite enumeration
selects candidates but is not a hidden matrix rebuild.

The largest mathematical closure tableau is 2x13, augmented to at most
2x15.  Kernel and Hd1 tableaus are at most 2x2, augmented to 2x4.  Every
coefficient search has exponent at most two, hence at most `3^2 = 9`
vectors; there is no `3^11` enumeration.  Literal queue bounds are
`6,3,3,3,3`, exact pop counts remain `4,1,1,1,2`, total pops are 9, and total
programmed capacity is 18.  Closure ranks remain `2,1,1,1,2`.

There are exactly 19 producer and 19 checker mutation oracles.  Mutation
oracles perform no extra RREF/tableau construction; the one left-kernel
mutation uses only the same bounded coefficient enumeration.  The producer
parses the fixture once.  The checker parses fixture and receipt once each.
Deep copies replace v10's mutation JSON round trips; canonical serialization
occurs only for explicit seals and digests.

No retry, sleep, poll, lock, thread, process pool, background child,
subprocess in either Python program, or unbounded queue is present.  The
driver alone owns the prescribed serial producer invocation followed by one
checker invocation.

## Driver and final static accounting

The ASCII driver stale-rejects all six owned output names for every version
v7 through v11 (30 paths).  In the selected mode it emits one producer and
then one checker command.  SELFTEST requires exact-one full-line producer
PASS, checker PASS with `19/19`, and both terminal markers.  PRODUCTION
requires exact-one full-line static terminal from each program.  Both modes
require nonempty receipt, verdict, and logs, require one 64-hex top-level seal
field in each output, extract nonempty terminal payloads, and require equality.
The sole `.ok` sentinel write is the final generated shell operation.

All statements above are static inspection results only.  No executable was
run, so candidate reachability is not promoted to an executed or verified
claim.

```text
IMPLEMENTATION:             IMPLEMENTED
EXECUTION:                  UNEXECUTED
SYNTHETIC SELFTEST:         UNEXECUTED
PRODUCTION:                 UNEXECUTED / STATIC_BLOCKED
ACTUAL A5 / ACTUAL A6:      0/3 / 0/3
LIFT / FAKE / IHARA:        NONE
```

`TASK324_R07_TASK320_V11_ANCESTRY_INDEPENDENT_INCREMENTAL_REPAIR`
