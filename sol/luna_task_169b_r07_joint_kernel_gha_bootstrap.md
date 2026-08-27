# Luna task 169b: exact-transition checker and GHA preflight bootstrap

Date: 2026-08-27
Role: Luna / static implementation only

## 1. Scope and reason

Continue task 169 from its resource STOP.  The first serial producer probe
stopped at the registered 600-second cap while rebuilding the 6,441 exact
joint-kernel relation values.  Static audit has found a separate propagation
bug: `--seconds 18000` reaches task 168, but both task 169's
`build_joint_domain` and the independent checker still use their unrelated
600-second constants.  This is an execution-cap defect, not a mathematical
terminal.

Complete the exact transition-cache staging and prepare a GHA-only bootstrap
which can create the previously nonexistent preflight.  Do not run Python,
GAP, Node, git, or GHA in this turn.  Do not weaken any equality, relation
roster, conjugate roster, word reconstruction, mutation, or claim gate.

Read task 169 and its reply completely before editing.  Preserve all of its
mathematical scope and warning sentences.

## 2. Authorized files

You may edit only these existing uncommitted task-169 drafts:

```text
search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py
crosscheck/check_d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py
sol/luna_reply_169_r07_joint_kernel_coeff_intersection_v1.md
```

Create only this additional ASCII GHA bootstrap driver:

```text
search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_driver_v1.g
```

Do not edit the existing full driver in this turn.  It remains unfinalized
until a preflight artifact has returned and can be pinned.

## 3. Producer exact-transition route

Finish and statically audit the staged producer evaluator.  It must evaluate
each freely reduced relation from the identity, letter by letter, in the
same pinned direct product `Q0 x E3 x E4^31`.  A cache entry may store only
the exact result of multiplying one authenticated state by one signed marked
generator.  It must not cache a truth value, quotient, hash-only state, or
heuristic representative.

Retain direct legacy `group.eval(reduced)` and `p_eval` equality canaries at:

- the first and last local ordinal of each of the three relation layers; and
- every global ordinal divisible by 257.

Bind the canary ordinal roster, count, per-word SHA, exact canonical value
blobs, aggregate digest, transition hit/miss counts, and final complete
6,441-row exact-value digest into the receipt and validation.  The complete
digest must have the same preimage format as task 169 already registered.

## 4. Independent checker acceleration

Implement an independent exact letter-transition evaluator in the checker.
It must import neither the producer nor its helpers, and it must not copy a
serialized producer cache.  Use a visibly different internal organization
(for example per-factor state tuples plus a letter-indexed transition table)
while computing the same literal products.

The checker must:

1. reconstruct all four signed marked letters independently;
2. begin every final relation at the identity;
3. compare the same deterministic canary ordinals with its own legacy full
   evaluator;
4. independently reproduce the complete relation-value digest and the
   producer's canary digest/count/ordinal roster;
5. retain all 173,907 conjugate rewrites and row-space checks; and
6. include bounded exhaustive fixtures where cached and uncached evaluation
   agree for every word through a preregistered small length, plus mutations
   of a cached transition, a canary value, a canary ordinal, and the complete
   digest.

No shared helper or producer import is allowed.  Performance improvement may
not replace any exact evaluation by a presentation assumption.

## 5. Separate resource-cap plumbing

Add an explicit positive CLI option `--domain-seconds` to producer and
checker.  Thread it into every task-169 relation-roster and RS wall-clock
check.  In producer full mode, keep `--seconds` exclusively as task 168's
existing full-search budget and use `--domain-seconds` exclusively for the
task-169 joint-domain construction.  Do not conflate the two.

Use 600 seconds as the local/default value.  Permit the GHA bootstrap driver
to pass exactly 5,400 seconds.  Serialize this cap as a resource-policy field
in the producer receipt; the checker must require that the receipt value
equals its own explicit `--domain-seconds` argument.  It is a resource bound,
not part of the mathematical universe, and must not change any roster or
rank.  Reject nonpositive, nonfinite, or over-5,400 values.

On resource exhaustion retain the existing UNKNOWN/STOP semantics.  Never
emit READY, NONEMPTY, EMPTY, or CROSSCHECK_PASS from a partial domain.

## 6. Source finalization order

Once the two Python sources are static-final:

1. compute their exact bytes and SHA-256 without executing them;
2. insert the final producer bytes/SHA into the independent checker;
3. recompute and record the final checker bytes/SHA;
4. pin both final sources and every inherited immutable input in the new
   bootstrap driver; and
5. leave no `TO_BE_FINALIZED`, wildcard pin, or self-referential source pin
   in the bootstrap driver.

The producer cannot pin itself.  The checker and driver must pin it exactly.

## 7. GHA bootstrap driver

The new ASCII GAP driver is only for the missing preflight.  It must not
require a pre-existing preflight certificate and must refuse full mode.
Under one explicit bootstrap flag it must, serially:

1. reject pre-existing outputs owned by this driver;
2. run the producer with `--preflight --domain-seconds 5400` into temporary
   output A;
3. run the same frozen producer command again into temporary output B;
4. require byte-for-byte identity of A and B;
5. require the unique producer marker and the exact preflight READY token;
6. run the frozen independent checker once on A with
   `--domain-seconds 5400`;
7. require the unique checker PASS marker and bind its target SHA to A;
8. copy A only after all gates to the canonical GHA artifact path; and
9. emit producer logs A/B, checker log, verdict, hashes, timing, and a final
   sentinel suitable for artifact collection.

Use one process at a time.  Give each producer and the checker an outer cap
strictly larger than 5,400 seconds, while keeping the total driver/workflow
envelope at most 18,000 seconds.  Preserve full logs on failure.  Check shell
`pipefail`, exact process counts, exact terminal counts, forbidden positive
claims, 6,441 relations, 173,907 RS rows, mutation totals, and byte equality.

The driver must have a cheap static/fixture selftest that does not attempt the
large domain.  It may audit a committed INPUT_STOP fixture, but must not call
the producer's heavy `--self-test` locally.

## 8. Report

Update the task-169 reply to distinguish:

- the already observed local STOP and exercised old-source hashes;
- the unexecuted static-final accelerated source hashes;
- the new bootstrap driver hash and exact invocation flags;
- `GHA dispatched = false` and all ranks/results still UNKNOWN; and
- the fact that the old full driver remains intentionally unfinalized.

Repeat task 169's five warning lines verbatim.  End with a static terminal
such as `R07_760_JOINT_COEFF_GHA_BOOTSTRAP_STATIC_READY`; this is not a
mathematical or cross-checked terminal.
