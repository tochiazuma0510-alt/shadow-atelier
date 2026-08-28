# Luna task 219 — R07 first-edge single-seed exponent-nine pre-gate v1

Date: 2026-08-28

Role: bounded mechanical implementation.  Sol owns the mathematics.  Do not
run Python, Node, GAP, git, GHA, or network.  Do not edit a workflow.  Report
to `sol/luna_reply_219_r07_first_edge_single_seed_endpoint_pregate_v1.md`.

## 1. Objective and frozen universe

Implement the first executable consequence of v214 and v216 for the named
R07 / row-36 correction only.  The universe is frozen to characteristic
three, the first matching relative Frattini edge, and

```text
chi_07 = [x,y][y,z]^-1,
D1 = H_2(Z/9),
h = [x,y],
c = h^3,
R0 = <c> ~= C3.
```

The pre-gate is the exact finite membership

```text
bar_epsilon_1 in C(U0),
U0 = span_{F3[D1]} { (c-1) odot w }.
```

Here `w` is the eleven-position signed, prefix-conjugated occurrence vector
of v214 (2.4), and `C` combines positions into the printed H1/H2/P blocks
only after occurrence-space closure.  The implementation must begin with the
single seed `(c-1) odot w`; it must not expand a 486-row input roster, and it
must not apply `C` before the occurrence-wise orbit closure.

This gate varies every projected first-edge relative multiplier at once.  A
complete nonmembership dual excludes every first-edge multiplier in `I0` for
the fixed correction.  Membership returns only a projected coefficient seed;
it is not an actual pointed multiplier, exact PB endpoint, cofinal lift, fake,
or Ihara witness.

Read in full before implementation:

- `sol/proof_r07_simultaneous_pointed_endpoint_gate_v214.md`;
- `sol/proof_r07_single_seed_endpoint_orbit_gate_v216.md`;
- `sol/proof_r07_uniform_three_seed_proheisenberg_gate_v217.md`;
- `sol/proof_r07_ten_occurrence_seven_block_action_bridge_v189.md`;
- `sol/proof_r07_proheisenberg_frattini_dovetail_v213.md`;
- task192 and task198 instructions, replies, producers, checkers, drivers,
  fixtures, and every file in their authenticated dependency cones which is
  required to interpret the actual word and occurrence evaluator.

Do not infer an ABI from prose when a live callable or serialized field can be
authenticated.  If the current task192/task198 production outputs do not
contain enough data to build `w` and `bar_epsilon_1`, stop in the reply with
the smallest exact missing-field list.  Do not fill missing actual data with a
toy, synthetic word, g760 prefix, Jennings projection, or receipt tag.

## 2. Authorized files

Create only:

```text
search/d972_r07_first_edge_single_seed_endpoint_pregate_v1.py
crosscheck/check_d972_r07_first_edge_single_seed_endpoint_pregate_v1.py
search/d972_r07_first_edge_single_seed_endpoint_pregate_gha_driver_v1.g
search/certs/d972_r07_first_edge_single_seed_endpoint_pregate_selftest_v1_20260828.json
sol/luna_reply_219_r07_first_edge_single_seed_endpoint_pregate_v1.md
```

Do not change any predecessor.  Use ASCII only in `.py`, `.g`, and JSON.

## 3. Production input authentication

The production path must consume, from guarded repo-relative `ci/in/` paths:

1. one positive, independently accepted task192 cached-v3 production receipt
   and its canonical member bytes/manifest, including the exact nonempty
   `exact_direct_replay.replay.corrected_word` and all artifact/member/run/head
   bindings required by task197; and
2. one complete, independently accepted task198 production receipt, including
   its complete marked roof presentation, ten-to-eleven occurrence ledger,
   seven-context bridge, and executable v188 consumer ABI bindings.

Authenticate byte length, SHA-256, schema, terminal, self-digest, immutable
head/run/artifact/member identities, dependency cones, exact word equality,
presentation completeness, occurrence order/tags/signs/orientations/prefixes,
and the task198 live evaluator ABI.  SELFTEST substitutes must be rejected by
PRODUCTION.  External/absolute/traversal paths, aliases, stale sidecars,
duplicate inputs, and output/input collisions are `UNKNOWN_INPUT`.

The producer must materialize the actual exponent-nine fixed residual and all
eleven actual occurrence values by literal replay of the authenticated common
word.  Receipt labels or coordinate numbers are not values.  Inverse-oriented
occurrences, the repeated E3 value, and the two distinct `C21` typed positions
must remain distinct.  Retain the exact source-word/Fox ancestry used to build
each value.

## 4. Exact first-edge arithmetic

Use an explicit normalized Malcev model for `D1=H_2(Z/9)` and seal the chosen
multiplication, inverse, commutator, and reduction conventions.  Prove by
exhaustion inside the producer that:

```text
|D1| = 729,
<x,y> = D1,
h = [x,y] has order 9,
c = h^3 has order 3 and is central,
|D1/<c>| = 243.
```

Use the deterministic transversal
`T={x^a y^b h^r: 0<=a,b<9, 0<=r<3}` and replay its 243 distinct cosets.
This is a sanity basis, not the seed roster.

Represent the eleven occurrence group algebras sparsely with full block and
position tags.  Build

```text
u0 = (c-1) odot w
```

and close its span under `x`, `x^-1`, `y`, `y^-1`, retaining every
rank-raising ancestry.  Queue exhaustion is the only complete terminal.  The
rank may not exceed 486.  Apply the non-equivariant block sum `C` after
closure, row-reduce the resulting H1/H2/P block rows, and test the actual
`bar_epsilon_1`.

On membership, return:

- a literal ancestry in the single orbit seed;
- the corresponding sparse coefficient in `F3[D1](c-1)`;
- direct replay that its occurrence action maps to the target after `C`;
- reduction of that coefficient to zero in `F3[D1/<c>]`.

Call this `PROJECTED_MEMBER_SEED`, never `mu1` or an exact lift.  On
nonmembership, return a complete separating dual which annihilates every
closed orbit row and is nonzero on the target; call it
`PROJECTED_NONMEMBER_DUAL`.  Resource exhaustion while constructing values,
closing the queue, or checking the dual is `UNKNOWN_RESOURCE`, never
nonmembership.

## 5. Independent checker

The checker must not import the producer or share its Malcev/group-algebra,
sparse-row, pivot, orbit-queue, Fox, block-combination, or digest helpers.
Authenticate predecessor inputs independently.  Use a different exact
Heisenberg representation and a different deterministic pivot/order scheme.
Reconstruct all eleven actual values from the input word, then replay:

- the 729-element group and the 243-coset transversal facts;
- the literal occurrence ledger and all prefixes/signs/orientations;
- the one-seed orbit span and queue exhaustion;
- post-closure `C` and the target membership decision;
- member ancestry/coefficient or nonmember dual, as applicable; and
- every resource and false-claim field.

Digest equality is not arithmetic equality.  A positive sentinel requires
matching producer/checker mathematical terminals.

## 6. SELFTEST and destructive controls

Build a production-shaped, noncommutative finite toy using the same producer
and checker entry points.  It must include eleven tagged positions, a repeated
value in two distinct positions, both inverse orientations, a deliberately
non-equivariant `C`, a nonzero single seed, at least two rank increases, one
dependent orbit row, one member target with recovered ancestry, and one
nonmember target with a separating dual.  Check the one-seed span against the
explicit `T(c-1),T(c-1)^2` roster only inside SELFTEST.

At minimum reject distinct mutations of: task192 word/member/head/artifact;
task198 presentation/ABI/context value; Malcev product/inverse/commutator;
`c=h^3`; one occurrence tag, repeated-position identity, prefix, sign, and
inverse orientation; applying `C` early; one orbit generator; queue
exhaustion; pivot ancestry; member coefficient; quotient-zero claim;
nonmember dual pairing and annihilation; resource phase/cap/value/limit;
SELFTEST-for-PRODUCTION substitution; path traversal; stale output; and each
false cofinal/fake/Ihara flag.  Register the exact distinct mutation set in
the fixture and require attempted=rejected for every entry.

Use one invocation-wide wall/RSS meter and explicit caps for input bytes,
word/Fox steps, sparse support, orbit actions, rank increases, pair work,
serialized bytes, and checker work.  A resumable checkpoint is optional
because the group orbit has only 729 states; if provided, it needs the same
portable manifest discipline as task198.  Otherwise every resource stop must
state `INITIAL_ABSENT` and no stale checkpoint may survive.

## 7. Driver and report

The GAP driver is serial and fail-closed, uses fresh `ci/out`, redirected
producer/checker logs, exact-one markers, an exact terminal equality gate, and
a nonempty mode-specific sentinel.  It must expose SELFTEST and PRODUCTION,
but Luna executes neither.  Give conservative GHA wall/RSS estimates rather
than a speedup claim.

The reply must state exact file identities, dependency cone, schema and
terminal vocabulary, resource envelope, mutation count, and any missing
production ABI field.  End with an honest frontier distinguishing static
readiness, GHA SELFTEST, actual task192/task198 inputs, the projected pre-gate,
the later task193/v188 pointed joint gate, exact PB endpoints, cofinal lift,
fake, and Ihara.
