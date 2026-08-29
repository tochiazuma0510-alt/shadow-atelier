# Luna task 378: R07 annotated PB boundary compiler v1

Date: 2026-08-29

Role: mechanical implementation of the already proved A8 compiler.  Do not
change the mathematics, run a production search, dispatch GHA, edit an
existing owner, or add SELFTEST/mutation/retry lanes.  Create only the three
new executables and the reply listed below.

## Frozen parent and theorem

Read in full:

- `sol/proof_r07_endpoint_to_vankampen_boundary_compiler_v197.md`;
- `sol/proof_r07_annotated_pure_braid_combing_boundary_v354.md`;
- task292-v2 producer/checker exact PB presentation owners;
- task377 v5 producer/checker/driver and reply.

The accepted parent is task377 v5, frozen at commit
`618673718c7564cd4bc55cc392155ae354b15b77`:

```text
search/d972_r07_direct_relator_a5_a7_fusion_v5.py
  57482 bytes
  ce9c6b0d7ba587f877634b60e0162f8ad3f60091b182b3031775b512f719f2ff
crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v5.py
  29559 bytes
  e651ad1909e3a50152e9ff7574b6a3f7dddf841402fff04ef809c81e940ccfba
search/d972_r07_direct_relator_a5_a7_fusion_gha_driver_v5.g
  6675 bytes
  5f1aefba79c4fde1c5a0688a62a83effe3bb590e16c016c95a6797514d6f2dea
```

Accept only a physical v5 MEMBER receipt, its ACCEPTED independent verdict,
the bound v5 checkpoint and A5 sidecar.  Authenticate their seals, byte/SHA
links, exact producer/checker source identities, terminal equality and fixed
word scope.  Any missing or non-MEMBER parent is `UNKNOWN_INPUT`, never an A8
negative.

## Producer: finite support graph

For each `B in (H1,H2,P)`, read the parent
`result.endpoint_exact.full_C1_replay.blocks[B].z_finite_support`.  Require the
parent task292 ZERO terminal and `D1_z_zero=true`.  Work over GF(3), and key a
PB group vertex only by the complete faithful Artin tuple; a digest or finite
quotient is not an equality key.

1. The positive Cayley 1-cell key is `(source_full_artin_key, component)`.
   A negative traversal of generator `x` from `g` is the negative of the
   positive cell `(g*x^-1,x)`.  Preserve coefficients modulo 3.
2. Insert every support cell and the prefix paths of its retained
   representative source word and target word.  Identify vertices by exact
   Artin keys, retain a literal representative path for each, and build one
   finite connected labelled multigraph rooted at the identity.
3. Choose a deterministic spanning tree.  For every oriented non-tree cell
   `e=(g,x)`, form the literal loop `w_e=p_g*x*p_(gx)^-1`.  Decompose `z_B`
   into the fundamental cycles by exact sparse tree-edge elimination.  Replay
   the complete equality before continuing; a coefficient 2 is not an
   unsigned multiplicity.

## Producer: annotated recursive PB combing

Use exactly task292's generator order and `pure_relations(n)` roster.  Do not
register derived rewrite rules as new relators.

Implement proof-producing collection for the recursive presentation

```text
P_n = P_(n-1) semidirect F(A_1n,...,A_(n-1)n), n=3,4.
```

An annotation entry is `(conjugator_word, relator_index, sign)` and the live
invariant is the literal free-group identity

```text
input_word * inverse(current_word)
  = product(conjugator * relator^sign * inverse(conjugator)).
```

Required primitive details:

- For a positive old generator `a` and positive kernel generator `k`, use
  task292's original relator
  `r=a^-1*k*a*phi_a(k)^-1`; the move `k*a -> a*phi_a(k)` has annotation
  `a*r*a^-1`.
- Derive the negative-kernel move from that same relator (inverse plus
  context); do not assume a new relation.  Derive an old-inverse move by
  first collecting `h*a -> a*u`, where `h=phi_(a^-1)(u)`, then reversing the
  trace and conjugating by `a^-1`.
- Obtain every `phi` word from the same Artin action used by task292 and
  require the defining positive relator to match a unique item of the
  original two/eleven-relator roster.
- Free cancellation has an empty annotation.  Context insertion, reversal
  and concatenation must preserve the displayed literal invariant and be
  checked at bounded cadence.
- Recursively collect ranks 4, 3 and 2.  For every fundamental loop require
  both the faithful Artin identity key and empty recursive normal form, then
  require its final conjugate-relator product to equal the loop by literal
  free reduction.

For each block, combine the cycle coefficient, trace sign and conjugator to
emit the finite original-relator chain `q_B`.  Use the unchanged task292 Fox
owner to replay, collect by `(component,full_artin_key)`, and require exactly

```text
D2_B(q_B) = z_B.
```

A MEMBER receipt retains the parent identities, support graph, tree paths,
cycle coefficients, every loop and trace, collected `q_H1,q_H2,q_P`, and the
three direct D2 equality replays.  It may claim only A8 for this fixed word;
A9, compatible lift, mixed-prime/perfect-core, fake and Ihara remain NONE.

## Resource and exact-resume contract

Expose cadence, seconds, RSS, operation and checkpoint-byte caps.  Guard the
letter-crossing/annotation expansion hot path, not just block boundaries.
Checkpoint completed graphs/cycles plus the current combing state: literal
input/current words, recursive rank/position, action words, annotation DAG,
cycle cursor and accumulated q.  Resume is all-or-none path/bytes/SHA and
binds all frozen sources plus the four physical parent artifacts.  Recompute
Artin keys and relator words; serialize no unauthenticated Python objects.

A controlled bound is `UNKNOWN_RESOURCE` and preserves the checkpoint.  It
is not an A8 negative.  Keep annotations as a DAG with shared word nodes and
flatten only the selected final traces, so a long trace is not copied after
every rewrite.

## Independent checker and driver

The checker must not import the new producer.  Use the checker-side task292
presentation and Artin implementation.  Authenticate the same accepted v5
parent, then for all three blocks independently:

1. replay the finite graph/cycle decomposition against the parent `z_B`;
2. replay every literal loop = conjugate-product identity from the original
   two/eleven relators;
3. rebuild q from cycle coefficients and traces;
4. independently Fox-expand q and require its collected chain equals z_B.

The GAP driver runs exactly one producer and, only on MEMBER, one checker.
Preserve receipt, verdict, checkpoint, progress and checker logs separately.
It exposes the four parent paths and the resume/resource arguments.  No
production run in this task.

## Deliverables

- `search/d972_r07_endpoint_zero_annotated_boundary_v1.py`
- `crosscheck/check_d972_r07_endpoint_zero_annotated_boundary_v1.py`
- `search/d972_r07_endpoint_zero_annotated_boundary_gha_driver_v1.g`
- `sol/luna_reply_378_r07_annotated_pb_boundary_compiler_v1.md`

Run only bounded static checks: Python in-memory byte compilation, frozen
owner restoration, GAP `ReadAsFunction`, ASCII and exact driver pins.  Stop
at the first real ABI obstruction and report it precisely; do not invent a
field or patch the parent owner.
