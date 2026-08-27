# Luna task 196 - R07 diagonal-context successor export v1

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_196_r07_diagonal_context_successor_export_v1.md`.

Role: bounded mechanical implementation only.  Do not run Python, GAP,
Node, git, GHA, or network locally.  Parent Sol owns mathematical audit,
repository brokerage, and every execution.  Do not edit task192--task195,
proof, provenance, or workflow files.

## 1. Objective and governing semantics

Read in full:

```text
sol/proof_r07_task179_relative_frattini_successor_v145.md
sol/proof_r07_recursive_relative_magnus_frattini_compiler_v168.md
sol/proof_r07_diagonal_context_cyclic_contraction_v173.md
sol/proof_r07_pointed_neumann_selector_without_annihilator_v174.md
sol/proof_r07_actual_pair_saturation_nakayama_v183.md
sol/proof_r07_pointed_pair_obstruction_hensel_v184.md
sol/luna_task_193_r07_second_frattini_affine_prefix_compiler_v1.md
sol/luna_reply_193_r07_second_frattini_affine_prefix_compiler_v1.md
the complete final task193 implementation/dependency cone
the final task194 implementation if its correlation is reused
```

Task195 static audit isolated a precise missing interface.  A positive
task193 receipt contains the actual second-rung boundary rows and corrected
raw defect, but it does not serialize the complete common diagonal group
\(\Delta_1\), the reduction \(\Delta_1\to\Delta_0\), or the exhaustive
relative kernel \(K\).  This task builds that interface from the same lazy
affine compiler.  It also reconstructs the two actual rows needed by
task195:

\[
 d_1=\text{signed original target of }g_{760},
 \qquad e_1=d_1-B_1a_1.
\tag{1.1}
\]

The output is a production input for a later versioned task195 repair.  This
task does not decide pair saturation or multiplier membership.

## 2. Authorized files

Create only:

```text
search/d972_r07_diagonal_context_successor_export_v1.py
crosscheck/check_d972_r07_diagonal_context_successor_export_v1.py
search/d972_r07_diagonal_context_successor_export_gha_driver_v1.g
search/certs/d972_r07_diagonal_context_successor_export_selftest_v1_20260828.json
sol/luna_reply_196_r07_diagonal_context_successor_export_v1.md
```

Pin exact bytes/SHA-256 of every imported source, proof contract, fixture,
and runtime input.  Temporary files stay outside the repository.  Do not
self-pin the GAP driver.

## 3. Hard positive-input gate

Production accepts exactly:

1. a helper-accepted positive task192 exact-word receipt and immutable
   run/artifact identity;
2. a helper-accepted positive task193 production receipt compiled from that
   same exact word, plus its checker attestation; and
3. cross-checked task194 identities if task194 arithmetic is used.

Authenticate schemas, statuses, exact terminals, self-digests, bytes,
SHA-256, checker lines, and exact corrected-word equality.  Missing,
resource-only, malformed, stale, or mismatched input is `UNKNOWN_INPUT`.
Never substitute the task193 SELFTEST word, a synthetic state graph, a roof
row, Jennings data, or one PB component.

## 4. Reconstruct the actual rows in the same compiler

Authenticate and reuse/adapt the task193 affine-prefix implementation behind
exact pins.  Re-evaluate both literal source words:

```text
g760 = w2 (w3^-1 w2)^8 y^36 x^-108
corrected_word = the positive task192/task193 exact word
```

through the same two printed hexagons and five ordered pentagon contexts.
For each word retain:

1. all seven substituted relation words in printed order;
2. every affine prefix and signed left-Fox term;
3. the separately tagged H1, H2, and pentagon rows;
4. termwise `D1=0`;
5. reduction to the authenticated roof row; and
6. complete boundary-reduction ancestry using every translated two-PB3 and
   eleven-PB4 boundary row.

Bind the sign convention explicitly.  Task193 stores the raw corrected
relation defect.  In the v174/task179 convention the pointed residual is
the separately signed row \(e_1\).  Serialize both rows and directly replay
the declared equality (including a minus sign if that is the registered
convention); do not identify them by a label.

Output `d1` and `e1` as literal block-tagged quotient rows with complete
source provenance.  Directly compare the corrected raw row with the task193
`beta1` fields.

## 5. Complete seven-context diagonal groups

The acting group is not a PB3 component, a PB4 component, or their free
product.  It is

\[
 \Delta_j=\operatorname{im}\left(
 F_2\longrightarrow\prod_{i=1}^7Q_{i,j}\right),
 \qquad j=0,1,
\tag{5.1}
\]

where the same source word acts in all seven contexts.

Construct the simultaneous tuples for the common generators
\(x^{\pm1},y^{\pm1}\).  Enumerate \(\Delta_1\) by deterministic BFS from
the identity, using exact coordinatewise affine equality modulo the complete
boundary image.  Independently enumerate \(\Delta_0\) from the reduced base
tuples.  Resource exhaustion is `UNKNOWN_RESOURCE`, never a declaration
that either group is incomplete.

For every state retain:

1. its canonical first source word and prefix parent/signed edge;
2. all seven exact affine context values at level one;
3. all seven reduced roof values;
4. transitions by \(x^{\pm1},y^{\pm1}\);
5. every equality merge chain or complete separating dual;
6. inverse and multiplication replays needed by the state graph; and
7. a direct proof that reduction is a surjective homomorphism
   \(\Delta_1\to\Delta_0\).

Hashes may index states but never decide equality.  A one-pass application
of the generators is not an orbit closure.

## 6. Exhaustive word-bearing kernel certificate

Let

\[
 K=\ker(\Delta_1\to\Delta_0).
\tag{6.1}
\]

Use the canonical prefix-closed BFS section of the roof state graph.  For
every roof state \(q\) and common generator edge, form the standard Schreier
word

\[
 s(q)\,g\,s(qg)^{-1}.
\tag{6.2}
\]

Retain every nontrivial word, its identity roof image, and its exact
\(\Delta_1\) value.  Close the subgroup they generate inside the complete
\(\Delta_1\) graph.  Prove

\[
 \langle\text{Schreier values}\rangle=K,
 \qquad |K|={|\Delta_1|\over|\Delta_0|},
\tag{6.3}
\]

by literal state membership and reduction replay.  Remove redundant
generators only with an exact incremental subgroup certificate.

The matched first Frattini kernel must then be checked, not assumed, to be
elementary abelian.  Replay order three and pairwise commutation for the
complete subgroup, compute \(t=\dim_{\mathbf F_3}K\), and bind the v184
nilpotence exponent \(2t+1\).  If the group is not elementary abelian, stop
with typed input/type failure rather than using that exponent.

## 7. Exported action interface

The receipt must be sufficient for task195 to close actual orbits without
re-enumerating either diagonal group.  Export:

1. the complete ordered \(\Delta_1\) and \(\Delta_0\) state rosters;
2. the reduction map and generator-transition tables;
3. for every \(\Delta_1\) state, its literal common source word and seven
   context values;
4. the complete word-bearing Schreier basis/certificate for \(K\);
5. the literal quotient actions of \(x^{\pm1},y^{\pm1}\) on \(d_1,e_1\),
   including unreduced rows, boundary ancestry, and roof reductions; and
6. sealed resume state for affine equality, both BFS traversals, and kernel
   closure.

Do not predeclare `complete=true`; completeness is the conclusion of the
replayed state graphs and (6.3).

## 8. Independent checker

The checker must not import the task196 producer or any of its affine,
BFS, Schreier, ordinal, sparse-map, or seal helpers.  It may authenticate
task193's independent arithmetic and implement the same mathematics by a
separately written path.

Use a different generator/BFS tie order and a different roof transversal.
Compare the resulting state sets and maps canonically, not the arbitrary
sections.  Independently reconstruct both source rows, every seven-context
action, all equality/boundary certificates, the complete kernel set, the
Schreier-generated subgroup, (6.3), elementary-abelian rank \(t\), and the
exported action rows.

On any negative equality used for state separation, the checker must replay
the dual against the entire translated boundary family.  A digest alone is
not evidence.

## 9. SELFTEST and destructive controls

Use a bounded noncommutative presentation with seven genuinely distinct
contexts, a nontrivial elementary-abelian relative kernel of rank at least
two, nontrivial boundary equality, and two literal source words whose signed
rows model \(d_1,e_1\).  Run the exact production-shaped affine compiler,
diagonal BFS, reduction, Schreier, and row-action paths.  The checker uses its
independent traversal and must recover the same canonical groups and rows.

At minimum reject mutations of:

```text
task192/task193 exact word
one context or context order
one affine multiplication/inverse
one boundary sign/translation/coefficient
one equality merge or separation dual
one BFS parent or signed edge
one omitted/repeated Delta1 state
one roof reduction image
one multiplication transition
one Schreier word order/inverse
one omitted kernel element
one false subgroup/order equality
one commutator or cube
rank t / nilpotence bound
d1/e1 sign convention
one exported action row/ancestry
resume cursor advanced past a sealed frontier
resource stop changed to completeness
```

## 10. Resource, driver, and reply contract

Register fail-closed caps for affine-oracle rounds, support-occurrence pairs,
\(\Delta_1\) states, \(\Delta_0\) states, multiplication checks, Schreier
words, kernel states, retained boundary columns, checkpoint bytes, aggregate
RSS, and wall time.  Check caps live during every loop.  A cap or dead worker
is `UNKNOWN_RESOURCE:phase=...:cap=...:value=...:limit=...` with the last safe
sealed checkpoint; it is never a smaller group or a negative kernel claim.

Provide serial SELFTEST/PRODUCTION GAP bindings, exact-one producer/checker/
driver markers, visible logs, fresh output, strict terminal equality, and a
nonempty sentinel only after independent acceptance.  Use the generic GHA
runner; do not edit a workflow.

Process Sections 1--9 in order in the reply, list exact identities of all
five files, and end with:

```text
TASK192/TASK193 POSITIVE INPUTS:              REQUIRED / NOT YET SUPPLIED
ACTUAL d1/e1 RECONSTRUCTION:                  NOT EXECUTED BY LUNA
COMPLETE DELTA1 -> DELTA0 STATE GRAPH:        NOT EXECUTED BY LUNA
EXHAUSTIVE WORD-BEARING K CERTIFICATE:        NOT EXECUTED BY LUNA
TASK195 PAIR / POINTED / DIRECT DECISIONS:    NOT ATTEMPTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:       NOT DECLARED
```
