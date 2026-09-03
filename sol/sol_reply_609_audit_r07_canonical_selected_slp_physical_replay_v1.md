# Task 609 - audit of canonical selected-SLP physical replay v469

## Verdict

`PASS`

V469 exactly closes the two load-bearing defects identified in Task607.
It replaces the ill-typed mixed-node source-grade argument by a
current-quotient physical replay, and it makes the canonical transcript
authoritative only after local records have been compared with the
deterministic routes or sealed source records.  The signs, two distinct
normalization scales, and all relevant product orders are correct.

There is no load-bearing repair.  This is a conditional paper verdict:
no selected payload has been produced or replayed, no fresh grade-two
residual has been computed, and `verified=false`.

## 1. Inputs read in full

| input | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_609_audit_r07_canonical_selected_slp_physical_replay_v1.md` | 1,327 | 25 | `0d70f075287641554865a7b5d6fef11a1b1f521cabd1fd0e05a1eb942020a4ba` |
| `sol/sol_reply_607_audit_r07_canonical_selected_dependency_slp_v1.md` | 13,098 | 274 | `2a7165dcde06a7fc0ef7df064185a128a7c7596c3a0571f1a4b21079e8960008` |
| `sol/proof_r07_selected_ancestry_slp_lift_v465.md` | 9,801 | 253 | `b779fca02449a1e4465bf0a29f7da8388f4c2e32c28a6f959e8c50189f2c7693` |
| `sol/proof_r07_reverse_selected_physical_slp_extraction_v466.md` | 6,810 | 153 | `0a7f1cf9d4f2d494379d39ea62ad20c0c27bb9935f29e9a9af4874493e0de308` |
| `sol/proof_r07_selected_slp_adjoint_fox_replay_v467.md` | 8,481 | 201 | `f80a63b2db0efe56777a48d1ddaab61518df9a802884549834e63e517e9a8dc5` |
| `sol/proof_r07_canonical_selected_dependency_slp_v468.md` | 12,016 | 284 | `b1e0f09ae0c6f136804e37bc8db8cba85bccede0880ed5f26afed880d28829a6` |
| `sol/proof_r07_canonical_selected_dependency_slp_physical_replay_v469.md` | 8,865 | 234 | `bae6864e6f00f65bfd3ff18a4c5676d5afe190ad0f2c6ffaf83cd9683d3f26f6` |

The audited current v469 is therefore bound to SHA-256
`bae6864e6f00f65bfd3ff18a4c5676d5afe190ad0f2c6ffaf83cd9683d3f26f6`.

## 2. Repair 1: the physical statements are correctly typed

V469 preserves the pure theorem only with its missing premise made explicit:
if a node is already known to lie in \(F^1\), v465 Theorem 2.1 gives its
class in \(F^1/F^2\).  It expressly refuses to assign that class to an
old/lower-derived node from physical lower-zero.  All mixed conclusions are
instead equations in
\(\mathcal E^{\rm phys}_{<1}\) and
\(\mathcal E^{\rm phys}_{1}\) at the current marked quotient.

This split is load-bearing and is now complete:

- a selected lower pivot \(L_k\) replays to its generally nonzero normalized
  lower row \(\ell_k\), together with the equally normalized grade companion
  \(g_k\);
- the lower-killed old origin \(Z_j\), not the lower pivot, replays to lower
  zero and the unnormalized offered grade companion \(z_j\);
- a physical-grade pivot \(W_j\) replays to lower zero and its normalized
  grade row \(b_j\); and
- the selected root \(C_T\) replays to lower zero and the authenticated
  MEMBER linear combination.

Thus v469 does not confuse the nonzero lower-pivot equation with the
lower-zero fibre equation.  Its executable endpoint-one premise is imposed
before Fox additivity and is occurrencewise at the current quotient.  It is
not inferred from a node label or carried to a refinement.

No equation in Sections 2--3 promotes physical zero to membership in
\(F^1\), \(F^1/F^2\), or a source relative kernel.  Sections 1, 3.1, 3.2 and
5 each preserve that prohibition.

## 3. Scale, sign, and order

The lower replay applies one lower node's normalization to the complete pair
\((\ell,g)\), not just to its lower component.  Hence a lower scale of two is
the fixed literal inverse convention \([2]=-1\), and gives the same
multiplication by two in the registered \(\mathbf F_3\) rows for both the
lower pivot and its grade companion.  The induction uses the accepted lower
order and every reduction factor in recorded order.

For an old connection, v469 uses

\[
 Z_j=O_j\prod_k^{\longrightarrow}L_k^{[-c_k]} .
\]

The minus sign is the reducer sign.  The \(L_k\) already contain their own
lower normalizations, and no grade-pivot scale is prematurely applied to
\(Z_j\).  Consequently its two physical images are

\[
 E_{<1}(O_j)-\sum_k c_k\ell_k=0,\qquad
 E_1(O_j)-\sum_k c_k g_k=z_j,
\]

in the exact lower-reducer order.  Calling \(z_j\) the unnormalized offered
companion is therefore correct.

The physical-grade word then appends its own ordered grade reductions and
only afterward applies its own outer scale:

\[
 W_j=\left(Z_j\prod_{(p,q)\in E_j}^{\longrightarrow}
                 W_p^{[-q]}\right)^{[\sigma_j]} .
\]

The lower image remains zero, while the grade image is exactly
\(\sigma_j(z_j-\sum q b_p)=b_j\).  The lower scale and grade scale are neither
omitted nor conflated, and coefficient two has the correct inverse/sign
semantics.  No commutation or coefficient coalescence is used in any of
these word identities.

## 4. Selected and complete roots

V469 retains all 3,317 root occurrences in the authenticated Task595 order:

\[
 C_T=\prod_{i=1}^{3317}W_{j_i}^{[a_i]} .
\]

After endpoint-one and the per-node replays, additivity gives lower image
zero and grade image \(\sum_i a_i b_{j_i}\).  Binding that sum to the
registered residual, replaying the authenticated prior root, and composing

\[
 C_1=\operatorname{Compose}(C_{<1},C_T)
\]

in the registered order gives the complete precision-one equality.  This
uses the current target/residual and prior-root premises; it is not a
statement about \(C_T\) alone.

Corollary 3.2 places the fresh-residual gate after both the endpoint checks
and that complete equality, and computes it from the exact complete root
\(C_1\).  The quotient-specific adjoint pass may evaluate that root without
flattening it, but may not replace or mutate its noncommutative syntax.

## 5. Repair 2: canonical local authority

Section 4 now supplies the missing authority before accepting terminal basis
or MEMBER equality.  For every reached node it requires:

1. reconstruction of the physical source origin from authenticated inputs;
2. comparison of lower origin, scale, coefficient values and the complete
   ordered edge interval with the deterministic lower route, followed by
   replay of both \(\ell_k\) and \(g_k\);
3. the analogous grade-route comparison, including the old connection's
   ordered lower interval, the lower-zero/offered-companion check, the
   grade recurrence, and byte equality with the authenticated pivot row;
4. comparison of every reached block/old/non-DAG origin, scale, ordered
   reduction, character sign and referenced sealed expression; and
5. only then, reconstruction of the exact 3,317-term equation and zero
   remainder.

The option to replay selected recurrences from authenticated earlier rows is
sound because the reducer and its order are frozen and each exported local
record is still compared with the independently reconstructed recurrence.
It does not authorize treating the candidate transcript as its own
authority.  Every nonzero child of a selected record is graph-reachable and
therefore retained; transient unselected records may be discarded only after
they have served the deterministic route.

These checks bind the local noncommutative order even when a permutation
would leave the abelian packed row unchanged.  A flat source word is
unnecessary because recursive interpretation of the authenticated acyclic
graph defines it exactly.  Exporting every unselected source node is likewise
unnecessary because complete child intervals plus the reached non-DAG
expressions give the full dependency closure.  The coalesced adjoint leaf map
is explicitly excluded as evidence for this authentication.

## 6. Claim boundary

```text
TASK609_V469_AUDIT:                         PASS
TASK607_SOURCE_PHYSICAL_TYPE_REPAIR:        CLOSED
TASK607_CANONICAL_TRANSCRIPT_REPAIR:        CLOSED
LOWER_PIVOT_AND_GRADE_COMPANION_SCALE:      CORRECT
OLD_CONNECTION_SIGN_AND_ORDER:              CORRECT
PHYSICAL_GRADE_SCALE_SIGN_ORDER:            CORRECT
COMPLETE_CURRENT ROOT:                       CONDITIONAL PAPER-CLOSED
PHYSICAL ZERO -> SOURCE F1/KERNEL:           FORBIDDEN; NOT INFERRED
FLAT WORD / ALL UNSELECTED SOURCE NODES:     NOT REQUIRED
ACTUAL SELECTED PAYLOAD / FRESH RHO2:        NOT PRODUCED
SOURCE-KERNEL SURJECTIVITY / COFINAL LIFT:   NOT PROVED
A0 / COMMON / FAKE / IHARA:                 NOT DECLARED
verified:                                    false
```
