# Luna task 168: g760 Jennings legal-coefficient certificate v1

Date: 2026-08-27
Role: Luna / implementation and bounded mechanical audit only

## 1. Purpose

Read `sol/proof_r07_l3_j9_survival_boundary_v105.md` and
`sol/proof_r07_jennings_legal_coefficient_selector_v106.md` completely.
The frozen g760 producer has now reported `j=9 nonmember=false`.  A boolean
MEMBER discards the most useful positive information: which of the 28 ordered
C-13 Schreier/legal-overapproximation rows express target6 modulo the full D2
boundary image.

After task167 v5 is final, build a versioned positive-certificate adapter.  It
must retain the exact v5/v3 mathematical traversal and checkpoint state, but
at every completed MEMBER j compute the affine coefficient family

```text
A_j = {a in F3^28 : target_j - sum_i a_i legal_row_{j,i} lies in D2_j}.
```

Output one deterministic lexicographically first coefficient vector, a basis
of the homogeneous kernel, and a concrete Schreier-word correction candidate.
This is an overapproximation certificate and guide to the actual A.18 solve;
it is not itself an actual lift.

## 2. Fixed inputs and noninterference

Pin the final task167 v5 source, driver, certificate, task/reply and every
inherited v1--v4 input.  Preserve exactly:

- g760, target6, all 28 legal rows and their frozen order;
- full translated D2 closure and insertion order;
- Jennings basis/projection, caches, terminal rules, and v5 safe-stop;
- append-only checkpoint authentication and the helper-nonshared checker
  requirement for any NONMEMBER.

Do not change the D2 traversal, legal rows, ranks, target, or membership
decision.  The new calculation begins only from the authenticated completed-j
D2 echelon and workspace.

Do not modify v1--v5, workflows, proofs, CLAIMS, or Sol replies.  Use new
versioned producer/driver/checker/certificate/reply files only.  No git, push,
workflow edit, GHA dispatch, full j=9 local run, or parallel Python/GAP.

## 3. Exact 28-coordinate quotient solve

For a completed j:

1. reduce `target_vector` against the authenticated D2 echelon, obtaining
   `target_bar`;
2. independently reduce each of the 28 ordered `legal_vectors` against the
   same D2 echelon, obtaining `legal_bar_i`;
3. solve `sum a_i legal_bar_i = target_bar` over F3 while tracking only the
   28 coefficient coordinates;
4. return `rank_L`, a canonical particular solution, a canonical reduced
   basis of `ker L`, nullity, and the exact lex-first solution for order
   `0<1<2` on coordinates 1..28;
5. replay `target - sum a_i legal_i` directly against the original D2
   echelon and require zero remainder;
6. require `A_j` nonempty iff the unchanged v5 row says
   `nonmember=false`.

Do not track 649,539 input-column coefficients.  D2 is quotient-zero; only the
28 legal provenance coordinates are needed.  Define and test the lex-first
algorithm exactly; do not call an arbitrary RREF particular solution
lex-first without proof.

Serialize the reduced quotient rows and target, their hashes, coefficient
system matrix/rhs hash, particular solution, kernel basis, lex-first solution,
and direct replay receipt.  Bind all of it to the j checkpoint's terminal D2
state commitment and public-row digest.

## 4. Concrete word materialization at the overapproximation level

Let the frozen ordered Schreier words be `s_1,...,s_28`.  For the lex-first
vector form the explicit signed word

```text
c_j = s_1^(a_1) * ... * s_28^(a_28),   a_i in {0,1,2}.
```

Use the producer's fixed word multiplication convention and reduce only by
free cancellation.  Recompute its three context values and projected Sigma
row from the word itself.  Require:

- all three registered K-context values are identity;
- projected `Sigma(c_j)` equals the linear combination of the 28 frozen rows;
- `target_j - Sigma(c_j)` reduces to zero modulo the authenticated D2
  echelon.

Record the signed word, length, exponent sums, SHA-256, context values, Sigma
hash and replay.  Call it `C13_overapproximation_correction_candidate`, never
`legal correction`, `A18 correction`, or `lift`.

## 5. Depth compatibility and actual-domain boundary

When more than one completed MEMBER j is present, require mechanically that
the newly computed affine family is a subset of the preceding family.  Check
this by substituting the new particular solution and every new kernel basis
vector into the preceding system, not by comparing ranks alone.  Report
whether the lex-first vector stabilized; stabilization is data, not assumed.

Every receipt must state:

```text
actual_common_word_domain_intersection_computed = false
literal_A18_replayed = false
two_hexagons_replayed_as_joint_system = false
cofinal_compatibility_proved = false
```

The 28-row system is full-K/C-13 overapproximation.  A positive coefficient
does not prove it belongs to the smaller actual common-word correction image.

## 6. Independent checker and bounded tests

Create a helper-nonshared checker which imports neither the new producer nor
its helper functions.  For a coefficient receipt plus authenticated terminal
checkpoint, independently:

- reconstruct the 28 frozen legal rows and target projection;
- replay the coefficient system and direct zero remainder;
- recompute the affine solution space and lex-first vector;
- materialize/re-evaluate the Schreier word and Sigma row;
- check depth inclusion when multiple j rows exist;
- reject every widened global claim.

The checker may authenticate/replay the lossless v5 D2 checkpoint rather than
regenerate 649,539 translations for a positive certificate, but must state
that this checks coefficient extraction conditional on that producer D2
state.  A later direct full-D2 checker remains a separate promotion gate.

Bounded serial tests must include randomized small F3 systems against
exhaustive enumeration, inconsistent/member systems, nontrivial kernels,
lex-first cases where the RREF particular is not lex-first, all-zero legal
rows, legal-row reorder, coefficient mutation, kernel-basis mutation, target
mutation, D2 state splice, word-order/sign mutation, context failure, Sigma
failure, and false-claim mutation.  Retain v5's completed-j/safe-stop tests.
Generate the final preflight twice byte-identically from a clean pinned overlay
and run producer/checker/driver selftests serially.

## 7. GHA boundary and report

The full producer should be able to run in the same v5 invocation immediately
after a completed j checkpoint, so the first artifact-safe run can return A9
without repeating j=9 in a second job if parent Sol elects to dispatch this
successor instead of plain v5.  Preserve the default safe stop after exactly
11 newly completed relators and upload every checkpoint/coefficient receipt
under `ci/out/` using the unchanged generic workflow.

Report paths, bytes, SHA-256, exact test commands/output, mutation counts,
the coefficient-certificate schema, lex-first proof method, word replay, and
all remaining UNKNOWNs.  Repeat verbatim:

```text
coefficient certificate = C-13/full-K overapproximation data only
j=9 nonmember=false is producer survival evidence, not an A18 lift
actual common-word domain intersection is still required
MEMBER != actual A18 lift
no fake / cofinal lift / Ihara witness declared
```
