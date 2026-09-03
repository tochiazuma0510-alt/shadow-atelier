# Task 605 - audit of selected-SLP adjoint Fox replay v467

## Verdict

`PASS`

V467 is a sound conditional evaluation theorem.  Its Fox-pair convention is
the left Fox convention used by v443; its reverse pass has the correct signs
and coefficient-two scales; and endpoint-one is an explicit, occurrencewise
gate at the exact current marked quotient.  Consequently the reverse scalar
collection may replace expansion only for the current Fox-row computation,
while the authenticated ordered SLP remains the source witness.  The theorem
does not use physical-lower zero as source-kernel membership and does not
promote any finite-rung result.

There is no load-bearing repair.  The actual selected payload, its endpoint
checks, the eleven-occurrence replay, and the fresh grade-two residual remain
unproduced inputs/runs, exactly as v467 says.  This is a paper verdict, not a
computational receipt and not Lean verification.  `verified=false`.

## 1. Inputs read in full

| input | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_605_audit_r07_selected_slp_adjoint_fox_replay_v1.md` | 1,882 | 36 | `515ecd421a4201103fae3ea9c367443ba8d475a7648e4f996a65b569da67394d` |
| `sol/proof_r07_selected_slp_adjoint_fox_replay_v467.md` | 8,481 | 202 | `f80a63b2db0efe56777a48d1ddaab61518df9a802884549834e63e517e9a8dc5` |
| `sol/proof_r07_selected_ancestry_slp_lift_v465.md` | 9,801 | 254 | `b779fca02449a1e4465bf0a29f7da8388f4c2e32c28a6f959e8c50189f2c7693` |
| `sol/proof_r07_reverse_selected_physical_slp_extraction_v466.md` | 6,810 | 154 | `0a7f1cf9d4f2d494379d39ea62ad20c0c27bb9935f29e9a9af4874493e0de308` |
| `sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md` | 10,291 | 323 | `80970217b415d7b764e399b5ce5892075b1f82f7f87f0c6199e9f6b0e404f24c` |
| `sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md` | 8,050 | 230 | `3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4` |
| `sol/proof_r07_a0_relative_fibre_echelon_lift_v441.md` | 11,696 | 329 | `5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb` |

## 2. Fox convention and the v443 side convention

For left Fox derivatives,

\[
 D(uv)=D(u)+\eta(u)D(v),\qquad
 D(u^{-1})=-\eta(u)^{-1}D(u).
\]

Thus v467's pair law

\[
 (g,u)\odot(h,v)=(gh,u+gv),\qquad
 (g,u)^{-1}=(g^{-1},-g^{-1}u)
\]

is exact.  It also has the correct side relative to v443.  If
\(g=\sigma(q_g)n(v_g)\) left-multiplies a group-ring term \([q]f\), and
\(a\) is the right term's \(A\)-coordinate, v443 (2.4) gives

\[
 [q_g]E(v_g)[q]f=[q_gq]E(S(a)v_g)f=L_g([q]f),
\]

which is precisely the \(gv\) in the Fox pair, not a right action and not an
action by the left factor's parity.  V443's negative-letter rule likewise
adds \(-pz^{-1}\) after updating the running prefix from \(p\) to \(pz^{-1}\),
which is the inverse rule above.

Each occurrence must still perform its own exact substitution and chain-rule
evaluation before its fixed prefix, sign, and physical aggregation.  V467
requires that order and never postulates an actor action on the already
aggregated physical module.  It is therefore compatible with v443's crossed
cochains and section-left/kernel-right arithmetic.

## 3. Endpoint-one is an executable current-quotient premise

For \(N=\ker\eta\), the left coefficient in the product rule is one on
\(N\), so

\[
 D(uv)=D(u)+D(v),\qquad D(u^{-1})=-D(u)\quad(u,v\in N).
\]

V467 does not infer this premise from an SLP type.  Sections 2 and 5 require
direct evaluation of every reached literal seed under every registered
substitution and require endpoint one before additive evaluation.  The same
gate covers literal transition-defect/earlier-correction leaves in the
selected payload; the prior root is separately authenticated and endpoint
checked.  Structural induction then puts ordered products, inverses, actor
conjugates, echelon words, \(C_T\), and the complete \(C_1\) in the same
kernel.

The load-bearing meaning of "current marked quotient" is the exact marked
finite quotient underlying this precision-two replay, not merely its coarse
degree-zero image.  V467 explicitly refuses to carry endpoint-one to a finer
quotient.  When the same SLP is later evaluated at a refinement, endpoints
must be replayed there and the ordered syntax, including factors whose
current Fox rows cancel, must still be present.  This is exactly the
naturality/limitation boundary of v465.

## 4. Reverse signs, scales, and nested ancestry

From

\[
 b_j=\sigma_j\left(z_{o(j)}-\sum_{p<j}q_{jp}b_p\right)
\]

one occurrence of \(\lambda_jb_j\) contributes

\[
 \sigma_j\lambda_j z_{o(j)}
 +\sum_{p<j}(-\sigma_j\lambda_jq_{jp})b_p.
\]

Hence both assignments in v467 (3.2) have the right sign and scale.  In
particular, \(2^{-1}=2\) in \(\mathbf F_3\): an accepted coefficient-two
pivot and a root coefficient two contribute scale \(2\cdot2=1\), while each
parent receives the additional minus sign.  No special sign convention is
needed for coefficient two.

Descending pivot order is essential and sufficient.  Every edge points to
an earlier pivot, so a node is visited only after all later uses have added
their coefficients.  Substitution proves (3.3), and applying the same
argument successively proves the nested case:

- an old-derived zero-lower grade origin first distributes its outer weight
  to the original old row and its recorded lower reductions with coefficients
  \(1\) and \(-q\); it has no invented normalization scale;
- each reached accepted lower pivot then contributes its own recorded
  \(\sigma\) and \(-\sigma q\);
- accepted block and old-source pivots use the identical recurrence; and
- defect origins retain their typed seed-reduction or actor-transition
  expression.  The plus signs in v451 (2.4)--(2.5) are not negated again:
  their internal packet subtractions are already in the literal defect SLP.

Actor-conjugated origins must remain typed with their exact actor paths; they
are evaluated as such rather than merged with an unacted seed.  That is
already required by v465--v467's payload and occurrence rules.  Re-forwarding
the accumulated origins must recover the unique 3,317 root coefficients and
zero grade-one remainder; this is an executable consistency gate, not a new
search.

## 5. Why additive evaluation suffices, and only where claimed

After the endpoint gates, every occurrence-specific Fox evaluator is a
homomorphism from the selected kernel words to the additive group of its
group-ring row.  Therefore (3.3) may be evaluated by accumulating the
weighted reached literal origins.  The PB3 normal map, prefix left
translations, occurrence transport, signed H1/H2/P aggregation, boundary
quotient, and auxiliary linear maps can then be applied in their registered
order.

All eleven literal occurrences remain separate until that last registered
aggregation.  In particular, the repeated occurrence is not identified and
no cancellation is moved across a type, prefix, inverse slot, or relation
block.  The same scalar origin weights may be used in each occurrence because
each occurrence is a linear evaluation of the same source SLP; its actual
substitution and actor path are nevertheless evaluated independently.

This linearization changes only the method used to compute the current Fox
row.  It neither sorts nor deletes nodes in the source object.  The witness is
still the exact ordered
\(C_1=\operatorname{Compose}(C_{<1},C_T)\) fixed by v465.  This distinction is
what makes current-quotient cancellation legal without silently changing a
higher-precision or finer-quotient representative.

## 6. Lower, boundary, exponent, and source-kernel gates

V467 requires the complete precision-one target equation before extracting a
top block.  Its normalized exponent and every integral side coordinate are
checked integrally before reduction modulo three.  The registered PB3 normal
map, fixed prefixes and signs, PB3/PB4 boundary quotient, and all auxiliary
and physical-lower coordinates remain mandatory.  These conditions match
v451 and v441; a regular lower block alone is not enough.

Nothing in the adjoint theorem turns
\(E_{<d}^{\mathrm{phys}}(W)=0\) into membership in a source relative kernel.
V465 (2.3) and v466 retain the separate rule: any later assertion such as
\(W\in K_n^D\) needs a direct source-reduction replay of the exact SLP.  V467
makes no such assertion, so there is no illicit substitution of physical
zero for source-kernel membership.

## 7. Resource statement

The reverse pass needs compact node/edge tables and scalar weights.  Literal
Fox rows can be evaluated and accumulated one at a time for each active
occurrence/component, so peak storage need not contain one ambient-width row
for every SLP node.  The claim is only the absence of the multiplicative
`number of SLP nodes x ambient width` storage term.

V467 does not bound flat literal length or claim that origin evaluation is
linear in the compact DAG size.  It explicitly charges runtime to the cost of
evaluating the reached literal origins in addition to the selected edge
count.  Re-evaluation or actor-path expansion may therefore be expensive
without contradicting the theorem.  No stronger runtime or memory claim is
being smuggled in, and no redesign is warranted by this audit.

## 8. Fresh grade-two handoff and claim boundary

The order in v467 Section 5 is the required v451 order:

1. authenticate the selected SLP and replay exact current endpoints;
2. replay the grade-one MEMBER equality and all exponent/lower/auxiliary
   gates for the complete \(C_1\);
3. check the full precision-one target equation; and only then
4. compute \(T_{\le2}-A_{\le2}(C_1)\) and extract its grade-two block.

Thus \(\rho_2\) is freshly dependent on the exact chosen ordered
representative.  It is not the Task595 residual and cannot be copied from a
different representative merely because the grade-one class agrees.  V467
does not claim that this residual is MEMBER of the target-independent
grade-two fibre; that is a subsequent v451/v441 decision.

Accordingly this audit closes only the conditional paper bridge:

```text
TASK605_V467_AUDIT:                         PASS
FOX_PAIR_AND_SECTION_SIDE:                 SOUND
CURRENT_ENDPOINT_GATE:                     REQUIRED_AND_EXECUTABLE
REVERSE_SIGNS_SCALES_NESTED_DAGS:          SOUND
ORDERED_SLP_PRESERVED:                     YES
ACTUAL_SELECTED_SLP_REPLAY:                NOT_YET_PRODUCED
FRESH_GRADE2_RESIDUAL:                     NOT_YET_COMPUTED
FIRST_RUNG_OR_LATER_GRADE_PROMOTION:        NOT_DECLARED
A0_COMMON_COFINAL_FAKE_IHARA:               NOT_DECLARED
verified:                                  false
```
