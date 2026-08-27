# Luna task 198 - R07 seven-context compressed roof presentation v1

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_198_r07_seven_context_roof_presentation_v1.md`.

Role: bounded mechanical implementation only.  Do not run Python, GAP,
Node, git, GHA, or network locally.  Parent Sol owns mathematical audit,
repository brokerage, and every execution.  Do not edit task176, task179,
task192--task197, proof, provenance, or workflow files.

## 1. Objective and governing theorem

Read in full:

```text
sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md
sol/proof_r07_task179_relative_frattini_successor_v145.md
sol/proof_r07_recursive_relative_magnus_frattini_compiler_v168.md
sol/proof_r07_diagonal_context_cyclic_contraction_v173.md
sol/proof_r07_pointed_pair_obstruction_hensel_v184.md
sol/proof_r07_compressed_diagonal_successor_relation_module_v188.md
sol/luna_task_176_r07_all_seven_extension_section_census_v1.md
sol/luna_reply_176_r07_all_seven_extension_section_census_v1.md
the complete final task175/task176/task179 producer/checker dependency cone
```

Build a complete finite marked presentation of the correctly typed v173
roof common-source group

\[
 \Delta_0=\operatorname{im}!left(
 F(x,y)\longrightarrow\prod_{i=1}^7Q_{i,0}\right),
\tag{1.1}
\]

in a compressed word-bearing form consumable by v188 Theorem 2.1.  Do not
enumerate \(357{,}128{,}352\) states.

The existing task176/task179 source represents an all-context group by

\[
 1\to\Gamma\to D_{\rm all}\to Q_0\to1,
 \qquad
 (|\Gamma|,|Q_0|,|D_{\rm all}|)
 =(243,1{,}469{,}664,357{,}128{,}352),
\tag{1.2}
\]

using ten typed coordinate values.  First authenticate the precise marked
map between that ten-coordinate representation and the two hexagon plus five
pentagon contexts in (1.1).  `Q0`, `D_all`, and `Delta0` are distinct names
until that map and its kernel are proved.

This task stops after the complete compressed roof presentation and action
interface.  It does not consume an actual task192/task193 word and does not
compute the successor kernel or multiplier.

## 2. Authorized files

Create only:

```text
search/d972_r07_seven_context_roof_presentation_v1.py
crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py
search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g
search/certs/d972_r07_seven_context_roof_presentation_selftest_v1_20260828.json
sol/luna_reply_198_r07_seven_context_roof_presentation_v1.md
```

Pin exact bytes/SHA-256 of every source, proof contract, fixture, and
committed arithmetic receipt.  Temporary files stay outside the repository.
Do not self-pin the GAP driver.

## 3. Exact ten-coordinate to seven-context type bridge

Authenticate and reconstruct the task176/task179 runtime.  Retain the exact
source substitutions defining:

1. both PB3 hexagon contexts;
2. all five ordered PB4 pentagon contexts;
3. the ten raw/deleted coordinate values used by task176;
4. every duplication, deletion, block, component, orientation, and sign map
   between the two representations; and
5. the common marked source generators \(x^{\pm1},y^{\pm1}\).

Evaluate the same source word on both sides.  Construct a marked
homomorphism

\[
 \theta:D_{\rm all}\longrightarrow\Delta_0^{(7)}.
\tag{3.1}
\]

Prove its image is (1.1), compute its kernel exactly using task176's
extension-section reduction, and return exactly one typed branch:

```text
ROOF_BRIDGE_ISOMORPHISM
ROOF_BRIDGE_PROPER_QUOTIENT
UNKNOWN_RESOURCE
UNKNOWN_INPUT
```

On the isomorphism branch, replay injectivity and an explicit inverse on the
marked compressed generators.  Equal orders alone are not a kernel proof.
On a proper quotient branch, compute and certify the bridge kernel and image
order, then stop after the typed terminal.  Sections 4--6 apply only to the
isomorphism branch; a later versioned contract must construct a different
base quotient.  Do not continue using \(D_{\rm all}\) as \(\Delta_0\).

The receipt must give an on-demand exact evaluator, multiplication, inverse,
and source section for the resulting \(\Delta_0\), with no all-state table.

## 4. Complete Q0 Schreier basis stream

Use task176's complete \(1{,}469{,}664\)-state Q0 BFS, parent/letter section,
`qmul`, `qinv`, and exact transition lookup.  For each state \(q\) and each
positive marked generator \(g\in\{x,y\}\), form

\[
 h(q,g)=s(q)g,s(qg)^{-1}.
\tag{4.1}
\]

Omit exactly the \(|Q_0|-1\) trivial tree edges.  For a rank-two free source,
the remaining roster must contain

\[
 2|Q_0|-(|Q_0|-1)=|Q_0|+1=1{,}469{,}665
\tag{4.2}
\]

word-bearing Schreier generators of \(R_{Q_0}=\ker(F(x,y)\to Q_0)\).
Encode every word as a prefix-DAG expression referencing authenticated
parent/letter records; do not expand millions of long words.  Retain the
exact image of every generator in \(\Gamma\) (or in the proper-quotient
kernel from Section 3).

Stream/chunk this roster under one global resource meter.  A prefix or word
radius is not a complete presentation.

## 5. Complete kernel presentation for Delta0

Let

\[
 \varphi:R_{Q_0}\twoheadrightarrow\Gamma_7
\tag{5.1}
\]

be the exact image map induced by the typed bridge, where \(\Gamma_7\) is
the relevant finite extension kernel (equal to \(\Gamma\) only after the
Section 3 proof).  From the Schreier basis stream:

1. select a deterministic word-bearing subset whose images generate all of
   \(\Gamma_7\), with exact incremental subgroup closure;
2. express every other Schreier image as a word in that selected set;
3. construct a complete marked presentation of \(\Gamma_7\) by a separate
   complete 243-or-smaller Cayley traversal; and
4. substitute the selected source words into those kernel relators.

Export a compressed relator DAG for

\[
 R_{\Delta_0}=\ker(F(x,y)\to\Delta_0)
\tag{5.2}
\]

consisting of:

1. every nonselected Schreier generator times its retained selected-image
   expression inverse; and
2. every complete \(\Gamma_7\)-presentation relator after literal source
   substitution.

Prove, using the free Schreier basis and the complete finite presentation of
\(\Gamma_7\), that the normal closure of this DAG is exactly (5.2).  Merely
showing that all exported words evaluate to the identity proves only one
containment and is a STOP.

Retain exact counts, selected generator indices, all finite-kernel Cayley
edges, expression ancestries, and the theorem inputs.  The consumer must be
able to evaluate each relator at a successor level incrementally without
expanding its roof section words.

## 6. Compressed Delta0 action interface

Export enough authenticated data and pure replay primitives for a later
successor consumer to:

1. evaluate \(x^{\pm1},y^{\pm1}\) in all seven contexts;
2. evaluate every Section 5 relator through a prefix DAG;
3. conjugate a successor-kernel vector by either marked generator;
4. compute a compressed roof section word/value on demand;
5. multiply and invert roof values via the Gamma/Q0 section cocycle; and
6. prove reduction of each relator to the roof identity.

The receipt serializes the small Gamma graph, Q0 parent/letter and transition
digests, typed bridge, selected-image expressions, relator DAG, and sealed
chunk checkpoints.  It must not serialize \(D_{\rm all}\) or
\(\Delta_0\) as a 357-million-row list.

All equality is exact coordinate equality.  Hashes authenticate stored
chunks but never replace equality.

## 7. Independent checker

The checker must not import the producer or its BFS, section, Schreier,
subgroup, prefix-DAG, codec, or seal helpers.  It may import separately
authenticated predecessor arithmetic exactly as prior independent checkers
do.

Use:

1. a different Q0 generator/tie order and inverse transversal;
2. a different Gamma generating subset and Cayley traversal;
3. a different relator-DAG topological order; and
4. different sparse/set encodings.

Independently replay the typed ten-to-seven map, bridge kernel/order, complete
Q0 state set, Schreier count/basis semantics, every Gamma-image expression,
complete Gamma presentation, normal-generation theorem data, and a sampled
materialization of selected and lexicographically boundary relators.  For
the complete million-row stream, compare canonical chunk digests only after
each checker-owned chunk has been semantically reconstructed.

## 8. Resource and resume contract

Use one monotonic production meter across runtime reconstruction, Q0 replay,
Schreier streaming, Gamma closure, relator construction, checker replay, and
resume.  Enforce at least:

```text
wall_seconds
rss_bytes (aggregate process tree where workers exist)
q0_states
q0_edges
schreier_rows
gamma_operations
dag_nodes
serialized_bytes
checkpoint_bytes
```

Check wall/RSS at sub-second intervals inside long loops.  A resource stop is
`UNKNOWN_RESOURCE:phase=...:cap=...:value=...:limit=...` with a sealed,
schema-validated checkpoint when it fits.  Resume authenticates all input
identities, caps, cursors, chunk seals, parent/letter digest, selected Gamma
state, and partial DAG, and charges replay against the new global meter.
Preflight-reject counters already beyond the new cap.  No generic exception
may be translated into `UNKNOWN_RESOURCE`.

Production may use process shards only for immutable disjoint Schreier
chunks.  Workers return source-indexed rows; one parent process performs the
canonical merge, Gamma selection, and final DAG.  Do not run local workers.

## 9. SELFTEST and mutations

SELFTEST uses a genuinely non-split finite extension with:

1. a nonabelian Q0;
2. a nontrivial finite Gamma;
3. ten raw typed coordinates mapping to seven genuinely distinct contexts;
4. at least one duplicate/deletion identification in the bridge;
5. non-tree Schreier generators with both trivial and nontrivial Gamma
   images; and
6. a complete relator presentation whose quotient order is independently
   recovered.

The fixture contains expected mathematical values, not producer output
bytes.  Mutations cover at least: context map/order/sign; deletion; source
generator; Q0 parent/letter/transition; tree-edge omission; Schreier count;
Gamma image; selected generator; subgroup closure; expression coefficient;
Gamma relator; substituted source word; DAG edge/order; normal-generation
flag; group order; chunk boundary/digest; stale input; resume cursor/seal;
and every resource terminal field.

## 10. Driver and final ledger

Use only the generic GHA runner.  Modes are `SELFTEST` and `PRODUCTION`.
Pin all inputs, reject stale outputs, require exact-one producer/checker
markers, compare exact terminals, and write a nonempty sentinel only after
independent acceptance.  No workflow edit.

The reply processes Sections 1--10 in order, gives exact identities and
separate GHA wall/RSS estimates for predecessor reconstruction, Schreier
streaming, and checking, and ends with:

```text
TEN-COORDINATE -> SEVEN-CONTEXT TYPE BRIDGE:  NOT EXECUTED BY LUNA
COMPRESSED DELTA0 GROUP/SECTION:              NOT EXECUTED BY LUNA
COMPLETE Q0 SCHREIER BASIS STREAM:            NOT EXECUTED BY LUNA
COMPLETE MARKED DELTA0 PRESENTATION:          NOT EXECUTED BY LUNA
357,128,352-STATE MATERIALIZATION:            FORBIDDEN / NOT USED
ACTUAL SUCCESSOR K / POINTED MU1:             NOT ATTEMPTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:       NOT DECLARED
```
