# Luna reply 338 — task335 A5/A6 v13 semantic rebase (v247 binding)

IMPLEMENTED / UNEXECUTED.  The five permitted v13 outputs were created and
statically inspected only.  No Python, Node, GAP, GHA, workflow, git, or
network command was run.  v7--v12 files and the immutable v11 source were not
modified.

## Load-bearing identities

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_joint_slice_kernel_general_v13.py` | 79617 | `feb69c5ab8e1b4db21ff5df05dac1690718310dc4c99cf4b67fc439ca9bc4268` |
| `crosscheck/check_d972_r07_joint_slice_kernel_general_v13.py` | 73233 | `dc344638ae42110f7cd028164c3ac5f6b5e1a908bdc596e5b4718c21db3cad07` |
| `search/d972_r07_joint_slice_kernel_general_gha_driver_v13.g` | 11044 | `79d93c2cff7173ca0c6ca3d356b4b3d3e7efcdffcb0b5351947ec273d5c50778` |
| `search/certs/d972_r07_joint_slice_kernel_general_selftest_v13_20260829.json` | 11163 | `60a3e1449f911fcfc3946373bcb471ea8efbaed4f1a2064e9ffbfba527fae50d` |

The wrapper binds `search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json` at exactly 12964 bytes and SHA-256
`cab24a5e6ddd7812094b920bffd7688564092a3c9b718484bf3f887cf59d2058`, with
schema `d972-r07-joint-slice-kernel-general/v11/selftest` and seal
`literal-static-fixture-v11`.  The reply is intentionally excluded from the
four-file identity table because it is self-referential.

## Import and input graph

The producer imports only `argparse`, `copy`, `hashlib`, `json`, `os`,
`collections.deque`, and `pathlib.Path`; it loads the v13 wrapper and then the
byte-pinned v11 source.  The checker imports only `argparse`, `copy`,
`hashlib`, `json`, `collections.deque`, and `pathlib.Path`; it has no import of
the producer and independently loads the same immutable v11 bytes.  The ASCII
driver pins producer/checker/wrapper/source bytes, emits a bounded shell, runs
one producer and then one checker, and uses only a seal-only JSON consumer for
each internal digest.

Both programs preflight exact integers (with `type(x) is int`), canonical F3
values `{0,1,2}`, rectangular dimensions, all 30 base/binding matrix pairs,
all six stored actions and their order/equivariance/invertibility, the five
source expected tuples, the source registry, and the twelve v11 trailing-zero
repair identifiers.  The wrapper also authenticates its trace expectations,
synthetic-linear flag, and `actual_a5_a6_milestone=false`.

## v13 live arithmetic trace

The queue contains only accepted rank-raising rows and is exhausted before C
is applied.  Each action below is a live matrix application to theta, z, and
eta; theta is retained only as ancestry and the pivot universe is the 13-vector
`(z,eta)`.

| case | chronological candidates (decision) | candidates / pops | closure / kernel / nonzero / Hd1 | terminal and witness |
|---|---|---:|---|---|
| `nonzero-member` | seeds `e0 A`, `e1 B` accepted; `m(e0)=B`, `n(e0)=2B`, `m(e1)=A`, `n(e1)=2A` dependent | 6 / 2 | 2 / 2 / 8 / 2 | MEMBER; theta `[1,1]` |
| `outside-nonmember` | seed `A` accepted; identity `m(A)=A` dependent | 2 / 1 | 1 / 1 / 2 / 1 | NONMEMBER; dual `[0,1]` |
| `zero-member` | seed `(z,eta)=([0,0],[1,0,0,...])` accepted; identity action dependent | 2 / 1 | 1 / 1 / 2 / 0 | MEMBER; theta `[0,0]` |
| `zero-nonmember` | same live seed/action; C image is nonzero, so kernel is empty | 2 / 1 | 1 / 0 / 0 / 0 | NONMEMBER; dual `[1,0]` |
| `post-c-cancel` | seed `A` accepted; `m(A)=B` accepted; `m(B)=A` dependent | 3 / 2 | 2 / 1 / 2 / 1 | MEMBER; theta `[1,2]` |

The post-closure C images are respectively zero, zero, zero, nonzero on the
one retained row, and `[1,1]` on the two retained rows.  The producer's live
nullspaces are `[[1,0],[0,1]]`, `[[1]]`, `[[1]]`, `[]`, and `[[2,1]]`; the
last Hd1 row is `[2,1]`, and target coefficient `2` gives the member ancestry
closure coefficients `[1,2]`.  The checker may choose the noncanonical
rightmost-pivot spans (for example `[1,2]` for the last kernel), and proves
two-way containment rather than coordinate equality.

## Retained-basis invariant

For every live owner, with raw insertion rows `R_i`, reduction returns

```text
raw_candidate = sum_i reduction_coefficients[i] * R_i + remainder  (over F3).
```

An accepted remainder is normalized at its first producer pivot by `scale`;
the new raw-row transform is
`(-scale * prior_coefficients) ++ [scale]`, existing transforms are padded by
zero before the roster grows, and every old pivot row and transform receives
the same elimination update.  Thus every exported direct coefficient vector,
including dependent zero-relation coefficients, replays the original raw
candidate exactly.  The producer replays both accepted and dependent records,
owner transforms, kernel rows, Hd1 rows, and MEMBER ancestry before sealing.

## Independent checker

The checker uses a separate rightmost/bottom-pivot `BottomSpan`, a dense
`[raw|identity]` tableau built only after closure, protected-right-hand-side
affine solving, and its own nullspace, Hd1, target, MEMBER, and NONMEMBER
calculations.  It does not import producer helpers and does not use producer
pivots, ranks, ancestry, terminals, or mutation booleans as mathematical
evidence.  It replays the producer owner exports and transcript, checks the
producer digest and every reconstruction digest, and proves two-way span
containment for closure, kernel, and Hd1.  Noncanonical MEMBER coordinates are
not compared for equality; the supplied witness and the independent witness
are each replayed to the target.  NONMEMBER duals annihilate every independent
Hd1 row and pair to one with the target.

## Mutation owners and envelopes

The identical producer/checker roster has 44 real owners.  Producer gates use
only `SemanticReject`; checker gates use only `IndependentReject`, and each
requires the registered exact stage, code, and reason.  Raw mutations are
resealed with `mutation_fixture_seal`; receipt mutations recompute the actual
`case_digest_sha256`; wrapper and anchor mutations pass through the normal
binding validators.

Inherited v11 owners (codes are the registered `M_` suffixes):

`field_modulus/M_FIELD_MODULUS`, `theta_seed/M_THETA_SEED`,
`theta_action/M_THETA_ACTION`, `z_action/M_Z_ACTION`,
`eta_action/M_ETA_ACTION`, `D_entry/M_D_ENTRY`, `O_entry/M_O_ENTRY`,
`C_entry/M_C_ENTRY`, `action_order/M_ACTION_ORDER`,
`premature_C/M_PREMATURE_C`, `target/M_TARGET`, `seed_index/M_SEED_INDEX`,
`parent/M_PARENT`, `row_theta/M_ROW_THETA`, `left_kernel/M_LEFT_KERNEL`,
`Hd1/M_HD1`, `member_ancestry/M_MEMBER_ANCESTRY`, `dual/M_DUAL`, and
`terminal/M_TERMINAL`.

The v13 transcript/envelope owners are:

`production_input/M_PRODUCTION_INPUT`,
`closure_queue_pops/M_CLOSURE_QUEUE_POPS`, `context_pops/M_CONTEXT_POPS`,
`closure_candidate_count/M_CLOSURE_CANDIDATE_COUNT`,
`closure_queue_bound/M_CLOSURE_QUEUE_BOUND`,
`candidate_parent/M_CANDIDATE_PARENT`, `candidate_action/M_CANDIDATE_ACTION`,
`candidate_decision/M_CANDIDATE_DECISION`,
`candidate_normalization/M_CANDIDATE_NORMALIZATION`,
`candidate_coefficients/M_CANDIDATE_COEFFICIENTS`,
`candidate_rank/M_CANDIDATE_RANK`,
`dependent_record_deletion/M_DEPENDENT_RECORD_DELETION`,
`dependent_record_reorder/M_DEPENDENT_RECORD_REORDER`,
`f3_plus3_coefficient/M_F3_PLUS3_COEFFICIENT`, and
`member_witness_equality/M_MEMBER_WITNESS_EQUALITY`.

The v247 anchor owners are:

`a4_anchor_identity/M_A4_ANCHOR_IDENTITY`,
`anchor_least_index/M_ANCHOR_LEAST_INDEX`,
`anchor_projected_exponent/M_ANCHOR_PROJECTED_EXPONENT`,
`anchor_inverse_scalar/M_ANCHOR_INVERSE_SCALAR`,
`anchor_substituted_cube/M_ANCHOR_SUBSTITUTED_CUBE`,
`anchor_word/M_ANCHOR_WORD`, `anchor_rho1_kernel/M_ANCHOR_RHO1_KERNEL`,
`anchor_rho0/M_ANCHOR_RHO0`, `anchor_q_z0/M_ANCHOR_Q_Z0`, and
`base_pair_order/M_BASE_PAIR_ORDER`.

The actual production ABI requires package
`r07-a4-anchored-relative-ideal-lift/v247`, an independently accepted
`least_index`, projected exponent, inverse scalar, and
`literal_word=u_z`, together with the exact gates
`rho0(u_z)=1`, `rho1(u_z) in K`, and `q(rho1(u_z))=z0`.  The only constructor
for an actual base family is
`sum_g lambda_g * (s(g)u_z-s(g))`; both endpoints are retained for replay.
The superseded `s(g)[x,y]^3-s(g)` pair is explicitly forbidden.  The five
frozen cases are synthetic linear arithmetic only and contain no fabricated
word anchor or actual A5/A6 result.

Envelope/seal coverage is explicit: receipt case and production flags are
bound, producer self-digest and checker verdict-digest are recomputed, the
driver requires exact-one PASS/terminal lines (therefore rejecting duplicate
terminals), stale v7--v13 receipt/verdict/log/terminal/shell/sentinel paths
and seal sidecars are rejected before execution, and queue-cap exhaustion is
`UNKNOWN_RESOURCE` rather than a malformed-input pass.

## Resource and driver accounting

Producer and checker meter JSON reads/parses, candidate construction, queue
pops, action applications, field operations, pivot reductions, coefficient
updates, nullspace/solve work, ancestry replay, mutation work,
canonicalization, serialization, RSS, and output writes with per-case and
total snapshots.  The final digest canonicalization, output canonicalization,
and write are reserved before the detached resource snapshot is sealed.  No
`3^r` coefficient enumeration, repeated known-basis rebuild, recursive
ancestry expansion, sleep/poll/retry/lock/thread/pool, or Python subprocess is
present in either checker/producer.  With candidate count `N`, width 13,
closure rank `r`, kernel dimension `d`, and Hd1 rank `h`, the reported bounds
are `O(N*13*r)` retained-basis work, `O(r^2*13)` producer nullspace work,
`O(r^2*(13+r))` checker tableau work, `O(h^2+13*h)` solves, and
`O(44*(N+13^3))` mutation work.

The ASCII driver has explicit SELFTEST and PRODUCTION branches.  It pins the
four load-bearing inputs, stale-rejects all owned v7--v13 outputs, runs one
bounded producer followed by one bounded checker, validates both canonical
internal seals with bounded seal-only consumers, requires nonempty outputs and
logs, requires exact-one full-line SELFTEST PASS (checker `44/44`) or static
terminal, extracts terminal sidecars, compares the full terminal payloads, and
writes `R07_JOINT_SLICE_KERNEL_GENERAL_V13_OK` as the shell's sole final
successful operation.  Production remains fail-closed until actual typed
matrices and the accepted A4 anchor arrive.

Remaining blocker: no actual typed matrix input or independently accepted A4
word-bearing receipt is staged, so no actual A5/A6 compilation is claimed.

```text
IMPLEMENTATION:                  IMPLEMENTED
SELFTEST / PRODUCTION:           UNEXECUTED
FIVE FROZEN CASES:               STATICALLY REACHABLE
ACTUAL A5 / ACTUAL A6:           0/3 / 0/3
LIFT / FAKE / IHARA:             NONE
```

`TASK338_R07_TASK335_A5A6_V13_SEMANTIC_REBASE`
