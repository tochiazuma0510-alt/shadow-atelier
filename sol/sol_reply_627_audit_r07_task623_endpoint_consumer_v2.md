# Sol(max) Task627 — static audit of Task623 endpoint consumer v2

## Verdict

**FAIL**

The quartet must not be armed or launched.  The paper pins and the intended
false-claim boundary are intact, but the executable route does not implement
the Task623 contract.  Three independent terminal defects suffice:

1. both producer and checker require the deliberately removed
   `derived.states` object and never parse `literal-leaves.bin`;
2. the producer substitutes six Task565 tags (with `% 6` aliasing) for the
   eleven actual occurrence contexts and never performs the required separate
   Task595/Task601 degree-one comparisons; and
3. the checker has no live precision-two replay and unconditionally raises
   `NOT_READY:task601_parent_acceptance_and_independent_target_replay`.

These are load-bearing missing implementations, not a small release patch, so
the classification is `FAIL`, not `PASS_AFTER_REPAIR`.  No selected payload,
fresh residual, grade-two result, A0, COMMON, cofinal-lift, fake, Ihara,
`cross_checked`, or Lean-verified claim follows.  `verified=false`.

This was a static audit only.  I did not execute either program, production,
GHA, or git.

## Exact static inputs

The Task623 quartet currently has the following identities.

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v2.py` | 12,692 | `228262c599d1c4b0f23aa09712280e49a2a3290e0948eff8fd9a84e6d2030b27` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v2.py` | 11,095 | `220df4cab4704dd68629073f94d78db8f8fc5be94ea02ba49c38fa695ec05f36` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v2.yml` | 7,399 | `21c219948fae69ee5b31f46aecb277d3288bd87b2df63fe8c57735fd1dc6360b` |
| `sol/luna_reply_623_r07_fresh_precision2_endpoint_signature_v2.md` | 2,697 | `d4b927beef5baaa31bf4abc0be43dfa87deb9578e469119ce2106e7eb04262ca` |

The five paper/audit pins in both executables match their actual bytes and
SHA-256: v470 `b56aa1...b2b7a`, Task611 `4212af...fccd92`, v471
`38d271...daf99f`, Task613 `04acf8...f75b`, and Task622
`4eaf1f...151e0`.  The pinned Task601 v1 producer/checker and Task565 source
also match `cfd581...d3ff`, `09ee81...86c8`, and `acffa3...ffc8`.

The parent premise itself is not available.  The final addendum in
`sol/luna_reply_601_r07_grade1_selected_slp_v1.md:142-166` records that run
`33723160379/1` ended `UNKNOWN_RESOURCE:time`, its checker did not run, and its
success-only selected-payload upload was skipped.  Task625 therefore specifies
a new staged v2 parent while retaining the compact binary leaf protocol
(`sol/luna_task_625_r07_task601_staged_adjoint_release_v2.md:34-44,76-92`).
Task623 remains pinned to the failed v1 run and v1 checker.

## 1. Exact paper and executable parents — FAIL

The local paper authentication is correctly fail-closed
(`producer:28,61-64`; `checker:16,21-24`), and the workflow does perform a
literal `cmp` between an uploaded Task601 verdict and a rerun output
(`workflow:90-98`).  Those partial positives do not establish the required
parent gate:

- The workflow never hashes the Task601 checker that it executes at line 95.
  Its preflight hashes only the two Task623 programs, the Luna reply, Task565,
  and the five paper inputs (`workflow:47-60`).  Thus “exact pinned Task601
  checker” is asserted by a constant, not enforced on the executable.
- Downloading the named artifact is the only run-status test.  There is no
  comparison with the actual Task601 run conclusion, attempt, head SHA, or
  workflow identity.  Line 55 merely compares the constant `TASK601_HEAD`
  with the same literal.  In particular, an artifact surviving a subsequently
  cancelled/failed run would not prove `conclusion == success`.
- The producer's optional verdict search (`producer:110-113`) is ineffective
  in the workflow layout: line 106 passes the `task601-payload` child, while
  `task601-verdict.json` is its sibling.  It also does not require the Task601
  PASS marker or byte equality.  The Task623 checker receives no parent
  verdict at all.
- `auth_parent`/`auth_task601` require only canonical JSON, `cursor == 8059`,
  and hashes of whatever receipt map happens to be listed
  (`producer:95-114`; `checker:71-87`).  They do not require the Task601
  schema/marker, the exact fifteen-file receipt set, the 3,317 coefficients,
  ranks/counts, false/null gates, or the accepted checker-verdict fields.
- `--state` and `--candidate` are presence-only arguments.  The producer never
  reads `state`; its `candidate` parameter is unused (`producer:121,154-160`).
  The checker reads neither (`checker:149-159`).  Consequently the Task554
  source and Task595 MEMBER basis/remainder are not authenticated here.
- The new manifest echoes only Task601 manifest, ancestry, and roots digests.
  It omits the compact-leaf receipt, the physical transcript receipts, and the
  Task595 basis/remainder receipts required by Task623 (`producer:147`).

The exact byte comparison shown in the workflow is therefore real but not an
authenticated complete parent-consumption contract, and the pinned run has no
payload to compare in any case.

## 2. Complete exact source and leaf reconstruction — FAIL

The incompatibility with Task601 is direct and unconditional.  The accepted
v1 contract emits

```text
derived = {schema, leaf_receipt}
```

and sets `states_exported:false`; it contains neither `derived.states` nor an
embedded `derived.literal_leaves`
(`search/d972_r07_a0_grade1_selected_slp_v1.py:990-1006`).  The independent
Task601 validator expressly rejects either member
(`search/check_d972_r07_a0_grade1_selected_slp_v1.py:346-363`).  Task625 keeps
that output protocol for v2.

By contrast, Task623 producer lines 68-69 and checker lines 43-44 require
`derived.states` to be a list, so every conforming Task601 v1 or v2 parent
fails immediately with `derived_shape`.  Both later look for the equally
forbidden embedded `derived.literal_leaves` (`producer:108-109`;
`checker:84-85`).

The actual exact-leaf receipt is a sorted binary `R07LEAF1` stream whose header
binds the ancestry digest and whose records use `<IIBI>` followed by signed
int8 path letters
(`Task601 producer:258-291`; `Task601 checker:936-1005`).  Neither Task623
program imports `struct`, parses that stream, or even reads
`loaded['literal_leaves']`.  Their semantic list comparison would not be the
required byte-for-byte comparison even if the obsolete JSON fields existed.

Nor is the fictional state walker a reconstruction of Task601's canonical
graph.  It ignores `structure.source_nodes`, `defect_nodes`, `expressions`,
the packed physical node/edge receipts, scale factors, and the authenticated
3,317 grade roots.  Its child recursion does not perform the actual
`word_mul/prepend` recurrence.  A terminal call merely concatenates one stored
prefix with a pure word and reduces it (`producer:80-94`; `checker:56-70`).

There is a partial syntactic attempt to include the prior terms at producer
line 123.  It is insufficient: the producer never checks the registered
`C_1`, and the checker checks only the `C_1` three-field object, not the exact
`C_T` ordered children or `C_<1` terms (`checker:86`).  The full Task601 root
contract is at `Task601 checker:1742-1763`.  Thus neither the complete root nor
exact freely reduced actor-path multiplication is independently reconstructed.

## 3. Endpoint-signature evaluation — FAIL

No authenticated eleven-context evaluator exists in this quartet.

- `TEN` and `LEDGER_SHA` are hard-coded (`producer:23-25`) and the ledger body
  is never read or hashed.  `SIGNS` is never used.
- Task565's `Context.actor_tags_affine` is indexed by its six `floor.OO`
  substitution tags.  Producer lines 118-119 and 129-130 silently reduce the
  alleged ten-context indices modulo `len(actors)`.  Hence indices 6--9 alias
  0--3.  The claimed eleven checks are repetitions of six Task565 tags, not
  eleven actual occurrence contexts with their orientations, fixed prefixes,
  signs, and PB3 typing.
- `base_checks = reached_seeds * 11` therefore reports up to 484 assertions
  although only six distinct tag endpoints were evaluated.  The manifest's
  ledger digest is an unauthenticated constant.
- Lines 123-125 construct a prefix-key dictionary, but each entry recomputes
  the entire prefix from the identity.  Because the default argument of
  `setdefault` is evaluated eagerly, shared prefixes are recomputed too.  This
  is not the specified one-edge recursion
  `endpoint(prefix+next)=endpoint(prefix)*image(next)` and is not the promised
  `O(11U)` trie evaluation.
- No exact-path-to-signature table, terminal assignment, or nonzero bucket
  table is sealed.  Only the counts `L/U/G` and a Boolean are emitted
  (`producer:147`), so the v471 receipt bindings cannot be checked.

Within its wrong six-tag model, letters are multiplied left-to-right, the
endpoint loop precedes bucket construction, the key retains `seed`, and
coefficients are added in F3 (`producer:115-135`).  Those local facts do not
repair the missing eleven-context premise, so complete-signature coalescence
is not licensed.

## 4. Fresh residual, not a grade decision — FAIL

The producer does pin and use Task565 and does not call `run_member_join`, a
resume/closure path, the old projector loop, or a grade-two owner.  Its calls
to `evaluate_seed_precision2`, `act_precision2`, `aggregate_precision2`, and
`direct_target_precision2` are within the permitted arithmetic surface
(`producer:136-145`).  The stated widths 32,260, 48,384, 12,096 and dense
44-seed byte count 10,644,832 are numerically correct.

The required gates around that arithmetic are absent:

- Since `state` and `candidate` are unused, there is no separate comparison of
  the selected degree-one update with the Task601 physical replay or the exact
  Task595 MEMBER equation.  Testing that the complete lower difference happens
  to vanish at lines 142-143 is not a substitute for either comparison.
- The complete source is based on the nonexistent leaf reconstruction and the
  six-tag pseudo-signatures, so its dense replay is not the v470--v471 source.
- The manifest contains support plus sparse and packed rho2 digests, but no
  exact target digest, literal-leaf digest, signature receipts, Task601
  checker-verdict digest, physical transcript receipts, or Task595
  basis/remainder receipts (`producer:147`).
- There is no independent check of any lower or top coordinate.  The only
  checker-side rho2 operation is a length/hash comparison of the producer's
  bytes (`checker:131-140`).

The producer's grade2/A0/COMMON/cofinal/fake/Ihara flags and `verified` remain
false, as required.  That claim-boundary subgate passes; rho2 sealing does not.

## 5. Independent checker and fixtures — FAIL

The checker satisfies the negative import rule syntactically: it imports
neither producer, Task565, nor the old floor helper.  It does not replace them
with an independent implementation.

Its `affine_mul`, `affine_inverse`, one-dimensional `truncated_product`, and
toy `occurrence_aggregate` (`checker:88-109`) are fixture helpers only.  The
live path never calls them, implements no endpoint substitutions, PB3 maps,
occurrence-first precision-two action, target construction, or packed-trit
decode, and imports no array arithmetic capable of replaying 32,260 plus
48,384 coordinates.  After shallow parent/payload receipt checks, lines
157-159 deliberately fail unconditionally.  `--out` is never written, so the
checker PASS marker required by the workflow is unreachable.

The fixtures do not meet Task623 either.

- Producer lines 149-153 test commutative tuple addition, tuple negation, and
  one scalar identity.  They do not cross any production endpoint, trie,
  action, target, lower, rho2, parent, or claim predicate.
- Checker lines 112-148 operate on toy tuples, lists, dictionaries, and byte
  strings.  `endpoint_gate` and `claim_gate` are not the predicates used by
  the live route; the latter duplicates the inline live flag test.  There is
  no real signature mutation fixture, no compact binary leaf parser fixture,
  and no production-path target/lower/rho2 mutation replay.

Accordingly the reported selftest PASS and mutation count 16 are only toy
control-flow facts, not semantic fixture evidence.

## 6. Resource/workflow boundary and report — FAIL

Several workflow mechanics are good: all four GitHub actions use immutable
SHAs; the job is inert via `if: false`; producer and checker are sequenced;
the residual upload is success-only; and the log upload has `always()`
(`workflow:31-130`).  These do not make the route releasable.

- There is no pinned NumPy installation, although the producer imports NumPy
  at module load.  Unlike the Task601 workflow, a clean `setup-python` runtime
  is not provisioned with an authenticated NumPy version.
- The inert Boolean is not the requested versioned fire marker, and the unused
  `TASK601_ACCEPTED=false` variable is not a parent-acceptance gate.
- The 2,700-second/7-GiB producer limits exist, but `guard()` runs only inside
  the final bucket loop.  Parent loading, leaf reconstruction, trie building,
  all 44 seed evaluations, and target construction are unguarded.  Both
  authenticators read every potentially multi-GiB Task601 receipt into one
  `loaded` dictionary (`producer:98-107`; `checker:74-83`), contrary to the
  stated streaming resource shape.
- The checker has no internal wall/RSS/resource guard.  The workflow has no
  address-space cap, and neither program enforces or reports a durable cap.
  A raw `MemoryError` is caught as generic `NOT_READY`, not classified
  `UNKNOWN_RESOURCE`.
- Two sequential 45-minute process allowances sit inside one 60-minute job;
  there is no demonstrated complete checker allowance after a near-cap
  producer.
- Because the checker never writes its output, lines 108-112 cannot reach the
  grep marker and the success-only residual upload is structurally
  unreachable.

The Luna reply is also not an accurate release report.  It says the checker
contains independent arithmetic although that arithmetic is not on the live
path, describes the failed v1 parent as still running (`reply:37-39`), and
omits the workflow SHA while incorrectly saying it is pinned by its own
preflight (`reply:41-47`).

## Prioritized finite repair list

1. **Establish one real parent type and result.**  Do not reuse failed run
   `33723160379/1`.  After Task601 staged v2 itself passes static audit and an
   independent production check, repin producer/checker/run/attempt/head/
   artifact in `producer:15-21`, `checker:8-10`, and `workflow:22-30,68-98`.
   Require the actual run conclusion/head/attempt and hash the exact Task601
   checker before executing it; retain byte-for-byte verdict comparison.
2. **Replace both obsolete parent parsers.**  Rewrite `producer:65-114` and
   `checker:40-87` for the final Task601 receipt schema.  Require the exact
   receipt set and false/null gates; stream-authenticate large receipts; parse
   `literal-leaves.bin` exactly, including header flags, ancestry binding,
   sorted records, coefficients and free reduction.
3. **Implement the canonical graph recurrence.**  Replace the fictional
   `derived.states` walkers at `producer:67-94` and `checker:42-70` with
   independent traversal of the actual source/defect/expression graph and
   packed node/edge roots.  Traverse all 3,317 roots without cancellation
   pruning, use exact boundary-cancelling path multiplication, byte-compare
   the independently encoded leaf stream, and bind exact `C_<1`, `C_T`, and
   `C_1`.
4. **Implement and authenticate the actual eleven contexts.**  Replace
   `producer:23-25,115-140` and the checker stubs at `checker:88-109` with the
   ordered occurrence ledger, orientations, inverses, fixed prefixes, signs,
   PB3 maps and physical order.  Remove `% len(...)`.  Run every reached-seed
   endpoint gate first; then evaluate a genuine one-edge prefix trie; only
   then coalesce by `(seed, complete_11_signature)`.  Seal path/signature and
   nonzero-bucket receipts as well as `L/U/G`.
5. **Close the degree-one and rho2 receipt gates.**  At `producer:121-148`,
   actually authenticate and consume `--state`/`--candidate`, separately
   compare the selected update against Task601 physical replay and Task595's
   exact MEMBER equation, require all 32,260 lower coordinates, check the
   48,384 top width, and bind target, compact leaf, physical transcript,
   basis/remainder, sparse and packed digests in the manifest.
6. **Build the real independent checker.**  Replace `checker:88-160` with
   locally implemented endpoint/group, substitution, truncated-polynomial,
   inverse action, target, PB3, aggregation, graph/leaf/signature and packing
   logic.  Recompute and byte-compare every lower/top coordinate and digest,
   and write a canonical PASS verdict only after completion.  The unconditional
   NOT_READY must remain until that implementation exists, not merely be
   deleted.
7. **Route fixtures and resources through production surfaces.**  Replace
   `producer:149-153` and `checker:112-148` with bounded real-path fixtures for
   every mutation named in Task623.  In `workflow:47-112`, install a pinned
   NumPy, add process-level memory protection and a feasible serial time
   envelope.  Add guards/caps around parent streaming, graph/trie/cache/target
   phases, a durable cap, a versioned inert fire token, refreshed exact hashes,
   and a truthful reply including the workflow identity.

```text
TASK627_TASK623_STATIC_AUDIT:       FAIL
TASK601_COMPACT_PARENT_COMPATIBLE:  NO
EXACT_TASK601_CHECKER_BOUND/RERUN:  PARTIAL; CMP PRESENT, EXECUTABLE/RUN NOT BOUND
CANONICAL COMPLETE ROOT REBUILT:    NO
ACTUAL ELEVEN CONTEXTS/GATES:       NO
TASK595/TASK601 DEGREE1 GATES:      NO
INDEPENDENT 32260/48384 REPLAY:     NO
REAL-PATH FIXTURES:                 NO
WORKFLOW INERT:                     YES
WORKFLOW RELEASABLE:                NO
GRADE2/A0/COMMON/COFINAL/FAKE/IHARA: FALSE
verified:                           false
```

`R07_TASK627_TASK623_ENDPOINT_CONSUMER_V2_STATIC_AUDIT_FAIL`
