# Task 611 - audit of leaf-gated precision-two join v470

## Verdict

`PASS`

V470 soundly replaces endpoint and Fox evaluation at every intermediate SLP
node by current-quotient checks on the reached compact relators and the exact
conjugate-leaf formula.  The apparent danger in the old/transition layers is
resolved by the authenticated v468 recursion: those records are generally
products, not single conjugates, but they are intermediate constructors whose
terminal occurrences are all \(P r_sP^{-1}\).  The sealed prior root has the
same registered literal-term form.  The current `Compose` is the ordered
source-group product represented by prior terms followed by the update, so it
preserves endpoint one.

The left Fox side, conjugator cancellation, coefficient-two sign, occurrence
typing, lower-before-top gate, and \(44\cdot11=484\) endpoint-check ceiling
are correct.  There is no load-bearing repair.  This is a conditional paper
verdict, not an execution receipt or Lean verification.

## 1. Inputs read in full

| input | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_611_audit_r07_selected_slp_leaf_gated_precision2_join_v1.md` | 1,775 | 33 | `c650d6b8a20a5168b2f9d02d1e1b6b0b4953f31922256da58c18d3a8c2f23983` |
| `sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md` | 10,291 | 322 | `80970217b415d7b764e399b5ce5892075b1f82f7f87f0c6199e9f6b0e404f24c` |
| `sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md` | 8,050 | 229 | `3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4` |
| `sol/proof_r07_selected_ancestry_slp_lift_v465.md` | 9,801 | 253 | `b779fca02449a1e4465bf0a29f7da8388f4c2e32c28a6f959e8c50189f2c7693` |
| `sol/proof_r07_selected_slp_adjoint_fox_replay_v467.md` | 8,481 | 201 | `f80a63b2db0efe56777a48d1ddaab61518df9a802884549834e63e517e9a8dc5` |
| `sol/proof_r07_canonical_selected_dependency_slp_v468.md` | 12,016 | 284 | `b1e0f09ae0c6f136804e37bc8db8cba85bccede0880ed5f26afed880d28829a6` |
| `sol/proof_r07_canonical_selected_dependency_slp_physical_replay_v469.md` | 8,865 | 234 | `bae6864e6f00f65bfd3ff18a4c5676d5afe190ad0f2c6ffaf83cd9683d3f26f6` |
| `sol/sol_reply_605_audit_r07_selected_slp_adjoint_fox_replay_v1.md` | 10,624 | 221 | `dc69b8149e4bfd1bf683144723493fdb91d3a012c895ff4dab7eb7fb3a18f916` |
| `sol/sol_reply_609_audit_r07_canonical_selected_slp_physical_replay_v1.md` | 8,455 | 179 | `f9f8fcf088e17d81a4980332aac22d04c3723f648984de91b0577ca028e1837f` |
| `sol/proof_r07_selected_slp_leaf_gated_precision2_join_v470.md` | 8,731 | 225 | `b56aa15ee87b4831cc999525233cfadbe8e62cd25c0503c0c98fce3106fb2b7a` |

The audited v470 is bound to SHA-256
`b56aa15ee87b4831cc999525233cfadbe8e62cd25c0503c0c98fce3106fb2b7a`.

## 2. Transition and old ancestry really terminates in the 44 relators

One must distinguish an intermediate expression from a terminal literal
occurrence.  A seed defect, transition defect, or accepted old pivot is not
generally one conjugate.  Nevertheless, the exact constructors fixed in v468
give the following terminating recursion.

- A projected-seed origin is the registered ordered product of the four
  character-signed conjugates of one compact relator.
- An old actor-parent conjugates an earlier old node.  Conjugating an ordered
  product of conjugate leaves produces an ordered product of conjugate leaves,
  with the actor word prepended to each conjugator.
- An old accepted node appends earlier old reductions and its outer inverse
  or identity scale.  These operations introduce no new literal word.
- A seed defect appends referenced old pivots to one compact relator.  A
  transition defect appends referenced old pivots to one acted old pivot.
  Their authenticated `seed_reductions` and `actor_transitions` expressions
  therefore recurse into the same old owner rather than becoming opaque
  transition leaves.
- Character-block, physical-lower, old-connection and physical-grade nodes
  add only conjugation, ordered products, inverses and references to these
  already typed descendants.

Every within-owner edge decreases the accepted-node number, and each
cross-owner edge descends v468's type order.  The recursion therefore
terminates only at a compact relator \(r_s\), occurring as
\(P r_sP^{-1}\); the unacted relator is the case \(P=1\).  Free reduction of
the stored actor path changes neither that free-group element nor its
endpoint.

The prior root does not introduce a broader leaf class.  V443's literal
positive handoff has terms of the form `(seed, actor-path)`, and v468 retains
the sealed `canonical_solution["terms"]` as an exact ordered SLP.  V470
authenticates its literal dictionary and all three roots and applies the same
formula separately to those prior terms.  Thus `reached seed` in Lemma 2.1
and Section 5 ranges over the union of leaves below \(C_T\) and
\(C_{<1}\), as required by the complete root \(C_1\).  An opaque arbitrary
transition word or earlier-correction word would fail this declared literal
schema and is not licensed by v470.

## 3. Every current constructor preserves endpoint one

For each registered occurrence, the direct base gate gives

\[
 \eta\theta_j(r_s)=1.
\]

The conjugator need not have endpoint one:

\[
 \eta\theta_j(P r_sP^{-1})
 =\eta\theta_j(P)\,1\,\eta\theta_j(P)^{-1}=1.
\]

The remaining constructors preserve endpoint one:

- `Prod` is an ordered group product;
- `Pow(T,1)` is \(T\), `Pow(T,2)` is \(T^{-1}\), and a zero power is empty;
- `Act(P,T)` is literal conjugation; and
- the current top-level `Compose(C_<1,C_T)` is the registered source-group
  product in the exact `canonical_solution["terms"] + update` order.

The last point is not an assertion about an arbitrary operadic or
substitutional composition.  It uses precisely the current finalizer meaning
fixed in v465.  Hence, once both roots are endpoint one, the complete root has
endpoint \(1\cdot1=1\).  Structural induction supplies every intermediate
endpoint without evaluating an intermediate Fox row.

## 4. Left Fox formula, inverse sign, and coalescence

With the left Fox convention,

\[
 D(uv)=D(u)+\eta(u)D(v),\qquad
 D(u^{-1})=-\eta(u)^{-1}D(u).
\]

If \(\eta(r)=1\), then

\[
\begin{aligned}
 D(PrP^{-1})
 &=D(P)+\eta(P)D(r)+\eta(P)D(P^{-1})\\
 &=\eta(P)D(r).
\end{aligned}
\]

Thus v470 correctly uses left multiplication by \(\eta(P)\), not right
multiplication, and the derivative of the conjugator cancels.  For the
inverse occurrence,

\[
 D(Pr^{-1}P^{-1})=-\eta(P)D(r).
\]

This is exactly the fixed coefficient-two convention
\([2]=-1\).  Outer coefficient-two scales and inverses of ordered products
also contribute one minus sign after endpoint one has been established;
v467's descending adjoint recurrence therefore supplies the correct
\(\mu_{s,P}\in\mathbf F_3\).

Coalescing equal exact keys \((s,P)\), including deletion after their current
weights sum to zero, is sound for this current Fox-row evaluation.  It occurs
only after v469 has authenticated every local source edge and order.  It
cannot prune the canonical graph or choose a different source word, and it
must be recomputed at a refinement.

All formulas are occurrencewise.  Each \(\theta_j\), marked actor endpoint,
crossed cochain, inverse/sign slot and fixed prefix is evaluated in its own
registered occurrence.  Prefix translation and physical aggregation occur
after the occurrence Fox row.  Consequently v470 does not introduce a common
action on the aggregated physical module.

## 5. Endpoint ceiling and precision-two join

There are at most 44 distinct compact-relator labels in the union of the
update and prior-root leaves.  Checking each label separately in all 11
registered occurrences gives at most

\[
 44\cdot11=484
\]

identity assertions.  Repeated physical slots remain separate receipt
entries even if their substitutions coincide.  This is a ceiling on base
endpoint equality checks, not on actor-path evaluation work: exact actor
endpoints must still be computed occurrencewise, as v470 states.

The claimed shortcut also does not bypass the physical gates.  The consumer
must authenticate the canonical graph first, derive rather than trust the
leaf map, evaluate the occurrence rows, apply the complete registered
occurrence-to-physical chain, and compare every lower/auxiliary and
grade-one coordinate with the independently accepted v469 replay and the
complete precision-one target.  Only after that equality may it extract

\[
 \rho_2=\operatorname{gr}_2
   \left(T_{\le2}-\mathcal E^{\rm phys}_{\le2}(C_1)\right).
\]

The stated width 48,384 and packed size 12,096 bytes agree with v451.  This
fresh residual depends on the exact complete root and is only an input to the
target-independent grade-two fibre, not a grade-two MEMBER decision.

## 6. Claim boundary

```text
TASK611_V470_AUDIT:                         PASS
TERMINAL LEAVES = CONJUGATES OF 44:         YES, UNDER AUTHENTICATED RECURSION
OPAQUE TRANSITION/OLD LEAF:                 NOT ADMITTED
CURRENT COMPOSE PRESERVES ENDPOINT ONE:     YES, AS REGISTERED ORDERED PRODUCT
LEFT FOX SIDE / CONJUGATOR CANCELLATION:    CORRECT
COEFFICIENT TWO = INVERSE:                  CORRECT
OCCURRENCEWISE TYPING:                      PRESERVED
MAXIMUM BASE ENDPOINT ASSERTIONS:           44 * 11 = 484
CANONICAL GRAPH REPLACED BY LEAF MAP:       NO
LOWER/PRECISION-ONE BEFORE FRESH RHO2:      REQUIRED
ACTUAL SELECTED PAYLOAD / FRESH RHO2:       NOT PRODUCED
GRADE TWO / A0 / COMMON / COFINALITY:       NOT DECIDED
FAKE / IHARA:                               NOT DECLARED
verified:                                    false
```
