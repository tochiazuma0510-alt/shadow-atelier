# Luna task 162: R07 760-letter commutator base and fresh affine RHS v3

Date: 2026-08-26

Role: Luna implementation / finite computation.  This task supersedes only
the **choice of affine base** in v2; all v2 independence, completeness and
GHA rules remain in force.

Requested reply:
`sol/luna_reply_162_r07_760_commutator_affine_rhs_v3.md`

## 1. Frozen base change

Keep the 616-letter parent

\[
f=w_2(w_3^{-1}w_2)^8,\qquad
\operatorname{SHA256}(f)=
3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90.
\]

The primary next-chief base is now

\[
r=x^{108}y^{-36},\qquad
g=f r^{-1}=f y^{36}x^{-108}.
\]

Pin and independently reconstruct:

```text
length(g)       = 760
SHA256(g)       = 518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d
exp(g)          = [0,0]
base_kind       = r07_760_commutator
parent_616_sha  = 3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90
```

If any pin differs, stop with an input terminal.

## 2. Complete settled-map identity certificate for r

Build the literal joint map from every currently frozen constituent map,
not merely one coordinate per target.  Directly prove \(r=1\) in:

1. G36 and PSL(2,8);
2. p2 source and all five p2 cofaces;
3. p3 source and all five p3 cofaces;
4. the complete E3 source value;
5. all five complete E4 coface values;
6. every further immutable finite side map actually consumed downstream.

Then replay \(g=f r^{-1}\), \(\operatorname{exp}(g)=(0,0)\), equality of every settled value
of \(f\) and \(g\), the two hexagons, ordered A.18, the R07 mark, and the
already established E4 source automorphism.  Include one mutation of \(r\)
or one target coordinate in the independent checker.

This is a literal joint identity certificate, so diagonal subdirect-product
correlations do not remain.  The governing paper proof is
`sol/proof_r07_joint_derived_commutator_rebase_v92.md`.

## 3. No transport across the new chief edge

The equality of 616 and 760 at the settled targets does not identify their
values at a finer quotient.  Therefore do **not** transport any 616 or old
20-letter Fox/A.18 datum to the 760 base.

Regenerate from \(g\):

- the six source words and an exact inverse/onto certificate;
- all two-hexagon and ordered five-coface target words;
- the complete base residual and every raw derivative used by the registered
  affine problem;
- B0, the eleven-relator D2 block, parents, sections and recovery data;
- all 109 base/direction rows for the registered 108-seed family;
- every dependent digest, multiplication-side and order canary.

Keep the left-Fox membership complex distinct from the literal arity/coface
A.18 differential.  If the literal normalized Brunnian class cannot yet be
typed, print `UNBUILT` rather than equating the two.

## 4. First successor solve

If the fresh 760 system is complete, solve target 6
`hexagon_1_coface_0`, component 4, using complete-D2 column generation in
the registered 108-dimensional family.  A positive result must materialize
the correction word and directly replay targets 1--6 plus every settled
gate.  A separator excludes only that registered family.  Resource exhaustion
is `UNKNOWN`; neither negative outcome is a full \(J_H/J_\Phi\) obstruction.

Do not proceed silently to targets 7--33.  Serialize the next target ordinal
if target 6 passes.

## 5. Independence and execution

Use a producer and an independent checker sharing no producer helper.  Local
execution is restricted to serial syntax/selftest/preflight.  Every full
dictionary rebuild, affine solve or large Python computation must be one
GHA process dispatched by the parent Sol session.

Exclusive terminals:

```text
R07_760_COMMUTATOR_BASE_READY
R07_760_AFFINE_RHS_READY
R07_760_TARGET6_REGISTERED_CORRECTION_PASS
R07_760_TARGET6_REGISTERED_FULL_D2_SEPARATOR
R07_760_AFFINE_UNKNOWN_RESOURCE
R07_760_AFFINE_INPUT_STOP
```

Every terminal must state

```text
full_JH_over_JPhi_complete=false
cofinal_lift=false
ihara_witness=false
```

unless a genuinely new complete proof establishes one of them.
