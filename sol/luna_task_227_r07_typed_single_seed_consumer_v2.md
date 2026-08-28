# Luna task 227 - R07 typed single-seed endpoint consumer v2

Date: 2026-08-28

Role: bounded mechanical implementation.  Sol owns the mathematics and git/GHA.
Do not run Python, Node, GAP, git, GHA, or network.  Do not edit a workflow.
Report only to `sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md`.

## 1. Objective and mathematical boundary

Implement only the v216 one-seed pre-gate, consuming the corrected task226
specialization package.  Read in full:

- `sol/proof_r07_single_seed_endpoint_orbit_gate_v216.md`;
- `sol/proof_r07_simultaneous_pointed_endpoint_gate_v214.md`;
- `sol/proof_r07_actual_two_word_endpoint_specializer_v225.md`;
- `sol/luna_task_226_r07_actual_two_word_endpoint_specializer_v2.md`; and
- the old task219 task/reply/code solely as a rejected historical comparison.

Do not reconstruct the task192/task198 word data in this consumer.  Task226
owns that specialization and authenticates it.  This consumer authenticates a
positive independently accepted task226 package and decides exactly

```text
bar_epsilon_1 in C(U0),
U0 = Span_F3[D1] { u0 },
u0 = (z0-1) odot w,
D1 = H2(Z/9), z0=[x,y]^3.
```

The closure is in eleven occurrence coordinates.  `C` is applied only after
closure.  A member is only a projected coefficient seed.  A nonmember dual
excludes all first relative-ideal multipliers for this fixed task226 package,
but is not a global lift-nonexistence or fake theorem.

## 2. Authorized files

Create only:

```text
search/d972_r07_typed_single_seed_endpoint_consumer_v2.py
crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py
search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g
search/certs/d972_r07_typed_single_seed_endpoint_consumer_selftest_v2_20260828.json
sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md
```

Do not change or import task219 implementation files.  `.py`, `.g`, and JSON
are ASCII only.

## 3. Input ABI and authentication

PRODUCTION consumes a guarded repo-relative task226 receipt, canonical member
and manifest, and independent task226 checker attestation.  Authenticate exact
bytes, SHA-256, schema, COMPLETE terminal, self-digest, run/head/artifact/member
identities, dependency pins, and checker acceptance.  Reject SELFTEST as
PRODUCTION, path traversal/aliases, stale sidecars, output collisions, and
nonpositive inputs as `UNKNOWN_INPUT`.

Consume the task226 `specialization_v216_abi` section.  It must carry:

```text
modulus 9 and the D1 commutator/generator convention;
11 ordered occurrences;
for each occurrence: ordinal, combined_block H1/H2/P,
  q_degree 3/4, key_width 4/10, p_o,
  sparse xi_o, sparse w_o, q_o(x), q_o(y), ancestry;
three sparse bar_epsilon_1 block maps;
sparse occurrence u0;
ten_to_eleven and occurrence-ledger digests.
```

Require exact internal consistency rather than trusting the serialized `w_o`
or `u0`: recompute `w_o=factor_sign*p_o*xi_o`, the conjugated occurrence
actions, `z0=[x,y]^3`, and `u0=(z0-1) odot w`.  Require Q3 keys of width 4,
Q4 keys of width 10, and actor keys of width 3.  Never coerce an occurrence
key to an H2 triple.

If task226's static SELFTEST schema names differ, adapt only through a sealed
versioned parser in this new consumer and record the exact map.  Do not modify
task226 files.

## 4. Producer: one-seed invariant queue

Represent a vector as eleven separately tagged sparse F3 group-algebra maps.
Use task226's marked occurrence images to act by

```text
(g odot v)_o = p_o q_o(g) p_o^-1 v_o.
```

Insert only the recomputed nonzero `u0`.  Whenever a row raises rank, retain
its exact coefficient ancestry in the initial seed and enqueue its four
marked translates by `x`, `x^-1`, `y`, `y^-1`.  Queue exhaustion is mandatory
and the rank cap is 486.  A zero `u0` is a valid exhausted rank-zero closure;
do not turn it into an input error.

After occurrence-space exhaustion, apply the literal block map `C`:

```text
occurrences 1..3   -> H1 Q3 block
occurrences 4..6   -> H2 Q3 block
occurrences 7..11  -> P  Q4 block
```

Echelon the complete block images and test `bar_epsilon_1`.

On membership emit `PROJECTED_MEMBER_SEED` with:

- an exact linear ancestry in occurrence basis rows;
- the induced sparse coefficient in `F3[D1](z0-1)`;
- direct replay on `w` and after `C`;
- reduction of the coefficient to zero in `F3[D1/<z0>]`; and
- queue/rank/block-span completeness data.

On nonmembership emit `PROJECTED_NONMEMBER_DUAL` with a complete sparse dual
which annihilates every block-image basis row, pairs nontrivially with the
target, and is directly checked against all 729 actor translates of `u0`.

Resource exhaustion before either complete certificate is
`UNKNOWN_RESOURCE`, never nonmembership.

## 5. Independent checker

The checker must not import producer or task219 helpers and must independently
authenticate task226.  Reimplement D1 and Q3/Q4 multiplication/inversion,
sparse rows, action, `C`, echelon, ancestry, dual pairing, digest, and seals.

Its completeness path is deliberately different.  Enumerate the canonical
243-element transversal

```text
T={x^a y^b h^r: 0<=a,b<9, 0<=r<3}
```

and form the 486 ideal elements `t(z0-1)` and `t(z0-1)^2`.  Act all of them
on `w`, compare the resulting occurrence and block-image spans with the
producer spans, and then replay the member ancestry or nonmember dual.
Also exhaust all 729 actor translates for the terminal certificate.

Do not infer span equality from ranks or digests alone: reduce every basis of
each span against the other.

## 6. SELFTEST and destructive controls

SELFTEST is production-shaped and uses eleven typed Q3/Q4 occurrence
coordinates, repeated E3 positions, distinct E3/E4 C21 types, nontrivial
conjugated actions, inverse slots, and a non-equivariant block map.  Exercise:

1. a nonzero `u0` with at least two rank increases and one dependent queue
   row;
2. one member target with recovered coefficient ancestry;
3. one nonmember target with a separating dual; and
4. a zero-`u0` rank-zero closure edge case.

Register and reject distinct mutations of at least: task226 bytes/SHA/schema/
terminal/run/head/artifact/member/checker; modulus; actor width; Q3/Q4 width;
one `p_o`, `xi_o`, `w_o`, q-map, sign, occurrence tag, repeated slot, C21 type,
block tag, and u0 term; commutator sign; z0 power; action conjugation; orbit
generator; early C; queue exhaustion; rank cap; basis row; ancestry
coefficient; quotient-zero claim; member replay; dual annihilation; dual
target pairing; 486-roster completeness; 729-translate completeness; resource
phase/cap/value/limit; SELFTEST-for-PRODUCTION; traversal/stale output; and
false mu1/lift/fake/Ihara flags.  Every registered mutation is attempted once
and rejected.

## 7. Terminals, resources, driver, and v220 mapping

Use exact terminals:

```text
R07_TYPED_SINGLE_SEED_ENDPOINT_CONSUMER_V2_SELFTEST_PASS
PROJECTED_MEMBER_SEED
PROJECTED_NONMEMBER_DUAL
UNKNOWN_INPUT
UNKNOWN_RESOURCE
```

Use one invocation-wide wall/RSS meter and explicit caps for input bytes,
actor operations, occurrence support, orbit actions, rank increases, block
rows, checker roster, dual work, mutations, and serialized bytes.

The ASCII GAP driver is serial and fail-closed, uses fresh `ci/out`, redirects
logs, requires exact-one markers and exact producer/checker terminal equality,
and writes a nonempty mode-specific sentinel only after acceptance.  It
exposes SELFTEST and PRODUCTION; Luna runs neither and edits no workflow.

The reply reports exact file identities, schemas, resource envelope, mutation
count, exact missing production input, and this milestone accounting:

```text
A3 actual package:       counts only after accepted actual task226 input
A3 orbit closure:        counts only after complete actual queue/486 crosscheck
A3 membership-or-dual:   counts only after an accepted actual terminal
SELFTEST infrastructure: does not increment A3
A4 and later:            untouched
```

End by stating that no pointed multiplier, exact PB endpoint zero, compatible
lift, fake, or Ihara witness was constructed.
