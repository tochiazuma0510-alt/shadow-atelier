# Luna task 226 - R07 actual two-word endpoint specializer v2

Date: 2026-08-28

Role: bounded mechanical implementation.  Sol owns the mathematics and git/GHA.
Do not run Python, Node, GAP, git, GHA, or network.  Do not edit a workflow.
Report only to
`sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md`.

## 1. Objective and supersession

Implement the corrected A2 specializer specified by
`sol/proof_r07_actual_two_word_endpoint_specializer_v225.md`.  Read that file
in full before editing.  Also read v174, v189, v194, v198, v213, v214, v216,
the task192/task198 instructions and replies, and the exact task179/task192/
task198 producer interfaces needed below.

This task replaces the rejected task219 production interpretation.  Do not
patch task219 and do not import it.  In particular, do not expect task198 to
contain word-specific `occurrence_values`, `fixed_residual`, or task192
ancestry.

The two load-bearing words are

```text
g0 = g760
a  = c_exact
f  = reduce(g0 + a)
```

and they have different roles:

```text
d_B       = -delta R_B(g0)
e_B       = -delta R_B(f)
epsilon_B = 1 - R_B(f)
```

For occurrence `o`, with `r_o=rho_o(g0)` and the immutable task198 sign and
prefix-occurrence list, implement v225 exactly:

```text
Q_o  = signed base-factor product named by fox_prefix_occurrences
P_o  = Q_o*r_o  when factor_sign=+1, else Q_o
xi_o = r_o^-1 - 1
w_o  = factor_sign * P_o * xi_o
```

The output of this task is the authenticated specialization package
`(P_o,xi_o)_1^11`, `(epsilon_H1,epsilon_H2,epsilon_P)`, `w`, and
`u0=([x,y]^3-1) odot w`.  It does not decide the v216 membership gate and
must not emit a multiplier, lift, fake, or Ihara claim.

## 2. Authorized files

Create only:

```text
search/d972_r07_actual_two_word_endpoint_specializer_v2.py
crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py
search/d972_r07_actual_two_word_endpoint_specializer_gha_driver_v2.g
search/certs/d972_r07_actual_two_word_endpoint_specializer_selftest_v2_20260828.json
sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md
```

Do not change any predecessor.  `.py`, `.g`, and JSON are ASCII only.

## 3. Production inputs and authentication

The PRODUCTION path consumes guarded repo-relative `ci/in/` files for:

1. a positive independently accepted task192 cached-v3 receipt, canonical
   member, manifest, and checker attestation; and
2. a positive independently accepted task198 roof-presentation receipt and
   checker attestation.

Authenticate exact bytes, SHA-256, schema, terminal, self-digest, immutable
run/head/artifact/member identities, dependency pins, and checker acceptance
before importing values.  Reject SELFTEST receipts in PRODUCTION and reject
absolute/traversal/alias paths, output collisions, duplicate paths, stale
sidecars, and nonpositive terminals as `UNKNOWN_INPUT`.

From task192 require and cross-check:

```text
g0 == receipt g760
a  == exactification.literal.c_exact
f  == exact_direct_replay.replay.corrected_word
f  == reduce(g0 + a)
exact_direct_replay row == direct all-seven change from g0 to f
```

From task198 consume only its reusable fields: ten typed coordinates,
ten-to-eleven insertion, occurrence ledger, presentation/evaluator ABI,
source ancestry, and exact `entry_points` / `section_cocycle` names.  Do not
require or synthesize word-specific fields in that receipt.

If a positive input is not yet staged, keep PRODUCTION fail-closed and name
the smallest exact missing input in the reply.  SELFTEST must remain runnable
without production inputs.

## 4. Q3/Q4 and actor arithmetic

Implement the v225 canonical class-two model independently in producer and
checker.

For `Qr1`, order degree-one `A_ij` lexicographically and central `c_ijk`
lexicographically.  Use the commutator convention
`[g,h]=g^-1 h^-1 g h`, the three bracket signs in v225 (4.4), and the exact
product/inverse formulas (4.5)--(4.6), all modulo 9.

The serialized group keys have different widths:

```text
Q3: 3 degree-one + 1 central = 4
Q4: 6 degree-one + 4 central = 10
D1=H2(9) actor:              3
```

Never store a Q3/Q4 group-algebra key as a D1 triple.  The marked map from an
actor to each occurrence is literal evaluation of the actor's source word
through that occurrence substitution.

Seal the generator order, central order, bracket table, multiplication,
inverse, word evaluation, and all ten source substitutions.  In SELFTEST
exhaust the 729 actor elements and check identity, inverses, generator closure,
`h=[x,y]` order 9, `z0=h^3` central of order 3, and 243 cosets.  For Q3/Q4,
use exhaustive checks on a deterministic small basis plus destructive bracket
sign controls; do not enumerate all Q4 elements.

## 5. Literal specialization and redundant identities

Reconstruct the eleven signed factors for `g0` and the three block relation
words for both `g0` and `f`.  Preserve the repeated E3 `(x,y)` positions and
the distinct E3/E4 `C21` types.

For every occurrence retain:

```text
ordinal, block, type, ten_index, rho generator images,
factor_sign, orientation, fox_prefix_occurrences,
r_o, Q_o, P_o, r_o_inverse,
xi_o sparse terms, w_o sparse terms,
all unreduced factor and ancestry terms
```

Require both independent target replays:

1. combine `factor_sign * P_o * delta(r_o^-1)` and compare with the literal
   negative Fox derivative of `R_B(g0)` in a SELFTEST word-level Fox model;
2. compare the combined endpoints with `1-R_B(g0)` in Q3/Q4.

Require both independent residual replays:

1. `epsilon_B = 1-R_B(f)`;
2. `epsilon_B = endpoint(d_B - (delta R_B(f)-delta R_B(g0)))`.

The production certificate may retain endpoint-only sparse terms, but the
SELFTEST must exercise the full redundant Fox identity.  A task192 roof
boundary chain is not the universal residual and must never be substituted.

Build `u0=(z0-1) odot w` occurrencewise using the v214 conjugated action and
retain its exact sparse ancestry.  Do not close its orbit or apply the block
sum as a membership test; those are A3/task216 work.

## 6. Independent checker and mutations

The checker must not import the producer or share its word reduction,
substitution, PB bracket, group product/inverse, sparse algebra, prefix,
endpoint, action, digest, or seal helpers.  Use a different deterministic
collection/pivot order where a choice exists.  Authenticate both predecessor
inputs independently and reconstruct the complete package.

SELFTEST must use two nonempty words `g0` and `a` with nontrivial
`f=reduce(g0+a)`, all eleven positions, both inverse orientations, the repeated
E3 slot, and the distinct typed C21 slots.  It must prove the role separation
by checking that changing only `f` changes a residual endpoint but not `w`,
while changing `g0` changes the occurrence target package.

Register and reject distinct mutations of at least:

```text
g0, c_exact, corrected_word, right-correction order,
task192 run/head/artifact/member, task198 run/head/receipt/checker,
ten-to-eleven insertion, repeated E3 position, E3/E4 C21 type,
one source substitution, factor sign, inverse orientation,
one prefix occurrence, prefix order, direct-slot base factor,
inverse-slot base-factor duplication, xi inverse, residual sign,
using f for d, using g0 for e, importing a boundary chain as e,
Q3 width, Q4 width, actor width, one bracket sign,
product cross-term, inverse cross-term, actor occurrence map,
action conjugation, z0 power, u0 ancestry,
SELFTEST-for-PRODUCTION, traversal, stale output,
false lift, false fake, false Ihara
```

Every registered mutation is attempted exactly once and rejected.  Digest
equality alone is not an arithmetic check.

## 7. Terminals, resources, driver, and report

Use schemas and exact terminals which distinguish:

```text
R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_SELFTEST_PASS
R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_COMPLETE
UNKNOWN_INPUT
UNKNOWN_RESOURCE
```

The COMPLETE terminal means only that the actual specialization package was
constructed and independently accepted.  Include explicit false boundary
flags for v216 membership, pointed mu1, exact PB endpoint zero, cofinal lift,
fake, and Ihara.

Use one invocation-wide wall/RSS meter and explicit caps for input bytes,
word steps, sparse support, group operations, mutation work, checker work,
and serialized bytes.  Resource exhaustion is typed UNKNOWN_RESOURCE and is
never a mathematical negative.

The ASCII GAP driver is serial and fail-closed, uses fresh `ci/out`, redirects
logs, requires exact-one producer/checker markers, exact terminal equality,
and a nonempty mode-specific sentinel.  It exposes SELFTEST and PRODUCTION,
but Luna executes neither and does not edit a workflow.

The reply states exact file identities, dependency cone, schemas, terminal
vocabulary, resource envelope, mutation count, exact missing production
inputs, and the v220 mapping:

```text
A2 paper contract:          1/3 (already supplied by v225)
A2 implementation SELFTEST: not counted until parent GHA acceptance
A2 actual specialization:   not counted until two positive actual inputs
A3 and later:               untouched
```

End with an explicit statement that no compatible lift, fake, or Ihara
witness was constructed.
