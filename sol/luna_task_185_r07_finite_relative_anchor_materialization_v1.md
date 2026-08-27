# Luna task 185 — R07 finite relative-anchor materialization v1

Commissioner: Sol / 2026-08-27

Reply to:
`sol/luna_reply_185_r07_finite_relative_anchor_materialization_v1.md`.

Role: bounded mechanical implementation and GHA preparation only.  Read
v149 and v150 in full before implementing.  Do not alter their mathematics.
Do not run Python, Node, GAP, git, or GHA locally; the parent owns all execution
and repository brokerage.

## 1. Objective and exact claim boundary

Materialize in the fixed task157ee/task176 joint group \(G\):

\[
 R_S(G)=\widetilde S=C_E(\Gamma)'=E^{(\infty)},
 \qquad S=PSL(2,8),
\]

retain literal source words for \(\widetilde S\), and compute a canonical
encoding of the frozen 760-letter value

\[
 b_{760}\widetilde S\in G/\widetilde S.
\]

Then inventory the repository for an **authenticated task176-level arithmetic
no-\(S\) quotient coordinate** for the DIH-ARITH fibre defining R07.  If no
such input exists, emit the complete structural receipt together with the
typed comparison state

```text
UNKNOWN_INPUT:ARITHMETIC_NO_S_COSET_NOT_AUTHENTICATED
```

rather than comparing \(b_{760}\) with the identity or a roof row.  A roof
arithmetic membership bit, a dihedral coordinate, or existence of an unnamed
\(\sigma_{07}\) is not this input.

The maximum positive claim is:

```text
word-bearing canonical PSL formation residual in the task176 group
canonical g760 coset in the solvable quotient G/tilde-S
finite v150 selector replay for any explicitly supplied arithmetic coset
```

It is not a task179 successor, cofinal lift, fake certificate, or Ihara
witness.

## 2. Authorized deliverables

Create or edit only:

```text
search/d972_r07_finite_relative_anchor_v1.py
crosscheck/check_d972_r07_finite_relative_anchor_v1.py
search/d972_r07_finite_relative_anchor_gha_driver_v1.g
search/certs/d972_r07_finite_relative_anchor_preflight_v1_20260827.json
sol/luna_reply_185_r07_finite_relative_anchor_materialization_v1.md
```

The checked-in JSON is an immutable
`UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD` fixture.  GHA execution output belongs
under `ci/out` only.

## 3. Frozen inputs and universe authentication

Authenticate by exact path, bytes, and SHA-256 before parsing:

1. v149 and v150;
2. the task157ee producer, helper-nonshared checker, GHA driver, task, reply,
   q3 receipt, and joint receipt from run `32359956713`;
3. the primary E3/E4 arithmetic used by task157ee;
4. the task176 final source/checker/driver and its production record
   `33044121344` as provenance for the extension invariants;
5. the independently frozen g760 construction, requiring reduced length 760,
   SHA-256
   `518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d`,
   and exponent pair `(0,0)`; and
6. the fixed marked PSL and G9 factor models and their generator conventions.

Do not require the 13.6 MB task176 production artifact if the same objects can
be reconstructed losslessly from the checked-in task157ee shelf.  Do not
download an external artifact in the runtime.  If a required literal word or
section is absent from the authenticated shelf, return a precise
`UNKNOWN_INPUT` structural stop; do not infer it from an order or digest.

The expected frozen invariants are acceptance gates, not hard-coded results:

```text
|Gamma|=243
|Phi(Gamma)|=27
|Gamma/Phi(Gamma)|=9
Q0 = PSL(2,8) x G9
|PSL(2,8)|=504
|G9|=2916
|G|=357128352
```

## 4. Producer: canonical residual with source words

Reconstruct the complete 243-state \(\Gamma\) Cayley table and the exact
extension arithmetic needed to evaluate source words in \(G\).  Build

\[
 E=\pi^{-1}(S\times1).
\]

Do not enumerate all of \(G\).  Use the word-bearing task157ee section and
Gamma adjustments to perform the following exact construction.

1. Replay the full Gamma multiplication table, centre, Frattini subgroup,
   and the action of marked lifts of the PSL generators.
2. Solve the inner-action equations against all 243 Gamma states.  For each
   marked PSL generator retain a literal adjusted lift centralizing every
   registered Gamma generator.
3. Enumerate \(C_E(\Gamma)\) only.  Require order
   \(|Z(\Gamma)|\,|S|=27\cdot504=13,608\), direct replay of centralization,
   closure, inverses, and exact projection onto \(S\).
4. Compute its literal derived subgroup \(\widetilde S\).  Require order 504,
   perfectness, the frozen PSL presentation, trivial intersection with Gamma,
   bijective marked PSL projection, and normality under both marked generators
   of \(G\).
5. Independently compute the stable derived term of \(E\) and require equality
   with the same 504-element roster.
6. Retain source words, parent/letter tables, canonical element encodings, and
   full replay digests for a deterministic generating set of \(\widetilde S\).

No assertion such as `canonical_complement=true` is evidence without these
underlying rosters and replays.

## 5. Producer: quotient normal form and g760 coordinate

Construct a lossless canonical normal form for \(G/\widetilde S\), without
enumerating \(G\).  It is permissible to enumerate the expected 708,588
quotient states or to use a proved Gamma-by-G9 normal form.  In either case
require:

```text
order = 243 * 2916 = 708588
complete identity/product/inverse action on the chosen normal form
kernel of G -> quotient equals the materialized tilde-S
```

Evaluate the literal frozen g760 word in the original joint extension and in
the quotient.  Retain:

1. full joint value encoding;
2. marked PSL coordinate and equality with the R07 target;
3. marked G9 coordinate;
4. canonical quotient coordinate, source word, and digest;
5. the unique v150 residual correction which moves any supplied representative
   of that quotient coset to the R07 PSL coordinate; and
6. a direct replay that this selector is constant on all 504 residual
   representatives of at least one complete nontrivial coset, plus a bounded
   deterministic sample of further cosets.

Do not call the g760 quotient coordinate arithmetic merely because its G9
projection belongs to a surjective arithmetic roof projection.

## 6. Arithmetic-input inventory and typed comparison

The receipt must distinguish these two possible authenticated inputs:

```text
PINNED_BASEPOINT:
  one named sigma/F word and its complete task176 quotient coordinate

COMPLETE_ARITHMETIC_FIBRE:
  the complete set p(A_07,G) in G/tilde-S with a completeness theorem/receipt
```

For `PINNED_BASEPOINT`, the conclusion may only say whether g760 matches that
one selected v18 branch.  For `COMPLETE_ARITHMETIC_FIBRE`, it may decide the
existential criterion v150 (4.4).  If neither exists, preserve the structural
result and set comparison to the exact `UNKNOWN_INPUT` string in Section 1.

Inventory likely-looking roof/index-three files, but report each rejected
candidate with a typed reason: wrong object, roof-only, missing F-component,
missing task176 quotient map, one basepoint but unnamed sigma, or incomplete
arithmetic fibre.  Absence from a grep search is not a nonexistence theorem;
the output is an input inventory.

## 7. Independent checker

The checker must not import the producer or producer helpers.  From pinned
primary task157ee inputs it independently rebuilds:

1. Gamma and its centre/Frattini data;
2. the PSL and G9 factors and the relevant extension action;
3. centralizing lifts, \(C_E(\Gamma)\), and its derived subgroup;
4. the stable derived term of \(E\);
5. the quotient normal form and its exact order;
6. the literal g760 value and quotient coordinate; and
7. every claimed v150 selector equality.

Compare full ordered rosters/coordinates/digests, not only orders.  If the
producer reports an arithmetic MATCH or MISMATCH, independently authenticate
the exact input type and completeness scope before replaying it.  If the
arithmetic input is absent, require the exact typed UNKNOWN and absence of all
match/fake/witness/cofinal claims.

## 8. SELFTEST and destructive controls

Use the production validator on a bounded nonabelian toy extension with one
distinguished perfect simple factor and a nontrivial solvable quotient.  Test
the residual-image lemma and the v150 selector on every toy group element.

At minimum, reseal and reject mutations of:

```text
one Gamma product
one centre membership bit
one inner-action adjustment
one centralizer element
one commutator used for the derived subgroup
one tilde-S roster element
one PSL projection
one G-normality image
one stable-derived equality
one quotient multiplication
one quotient order
one g760 letter
one g760 quotient coordinate
one selector correction side/order
one arithmetic input scope label
one incomplete arithmetic-fibre claim
one UNKNOWN/MATCH terminal alteration
```

Mutations must reach reconstruction/semantic replay; stale hash rejection alone
does not count.  Report attempted and rejected counts exactly.

## 9. GHA driver and terminals

Provide an ASCII-only serial driver with exactly two externally bound modes:

```gap
D972_R07_FINITE_RELATIVE_ANCHOR_V1_MODE:="SELFTEST";;
D972_R07_FINITE_RELATIVE_ANCHOR_V1_MODE:="PRODUCTION";;
```

SELFTEST must be bounded and must not enumerate the 708,588-state production
quotient.  PRODUCTION runs producer then checker, with fail-closed time/RSS
caps, `pipefail`, no pre-existing outputs, exact-one markers, terminal
agreement, hashes/timings, and checkpoint-free deterministic restart.  Generic
exceptions fail the job; they are not typed mathematical UNKNOWNs.

Allowed production comparison states are exactly:

```text
STRUCTURE_COMPLETE_ARITHMETIC_UNKNOWN
PINNED_BASEPOINT_MATCH
PINNED_BASEPOINT_MISMATCH
COMPLETE_FIBRE_MATCH
COMPLETE_FIBRE_MISMATCH
UNKNOWN_RESOURCE
UNKNOWN_INPUT
```

The first state is expected if the structural computation completes but the
arithmetic coset input is absent.  Workflow success is not by itself a
cross-checked structural result; require producer/checker agreement.  State a
conservative GHA time/RSS estimate and the exact generic `gap-run.yml`
preamble in the reply.

## 10. Reply

Give numbered dispositions for Sections 1--9, exact bytes/SHA-256 for all five
deliverables, a static GO/STOP verdict, and `GHA dispatched=false`.  Finish
with exactly:

```text
task176 residual materialization only
arithmetic comparison scope explicitly typed
direct task179 route remains independent
no fake / cofinal lift / Ihara witness declared
```
