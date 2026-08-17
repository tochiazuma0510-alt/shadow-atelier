# Luna reply 156a — exact low-memory Burau mathematics

## Verdict

The proposed full permutation-to-matrix replacement is mathematically sound:
use the full (36)-dimensional permutation module over (mathbf F_q), not a
reduced or projective module, and take a block diagonal sum with the five
(4\times4) Burau blocks.  This gives an exact representation of the same
tuple map.  It removes the degree-(36+5q^4) permutation action, although a
standard-runner memory bound is an engineering property that still requires a
runtime gate; a matrix-group resource stop remains `UNKNOWN_RESOURCE`.

## Faithful representation and projection

For (p\in P\), let (R_q(p)) be its full (36\times36) permutation matrix
over (mathbf F_q), with the multiplication convention checked on the two
roof generators.  The map (p\mapsto R_q(p)) is faithful in every
characteristic: if (R_q(p)=I), every standard basis vector is fixed, hence
(p=1).  This remains true when (qmid |P|); non-semisimplicity is not a
kernel.  Do not replace this block by the augmentation quotient or a
projective/scalar quotient.

For a tuple (t=(p,M_1,\ldots,M_5)), define

\[
  \Phi_q(t)=\operatorname{diag}(R_q(p),M_1,M_2,M_3,M_4,M_5)
  \in GL(56,q).
\]

Each (M_i\) is the original (4\times4) matrix, not its (q^4)-point
permutation action.  Block-diagonal multiplication is componentwise, so
(Phi_q) is a homomorphism.  The first block recovers (p) and the five
remaining blocks recover the (M_i), hence (Phi_q) is injective.  Therefore,
for (X=E(x),Y=E(y)),

\[
 \widetilde H=\langle\Phi_q(X),\Phi_q(Y)\rangle=\Phi_q(H),
 \qquad
 \widetilde H'=\Phi_q(H').
\]

The equality for derived groups follows from preservation of commutators by an
injective homomorphism.  Decode the first block of every matrix-group element
back to a permutation and define

\[
 \widetilde\pi(\Phi_q(p,M_1,\ldots,M_5))=p.
\]

This is exactly the original (pi:H'\to P), and
(ker(\widetilde\pi|_{\widetilde H'})=Phi_q(K)).  The decoder must check
that the first block is a (0/1) permutation matrix and that decoding
respects multiplication; relying only on a guessed `GroupHomomorphismByImages`
is not a completeness proof.  The five lower blocks must remain separate;
mixing them or quotienting by scalars would change (E).

## Complete finite algorithm

1. Construct the two exact (56\times56) matrices over the same field as the
   five Burau blocks.  Gate all three Artin relations, determinants, and the
   full 972 word-to-roof-key replays before group computation.

2. Form (widetilde H) as a matrix group and compute its derived subgroup by
   an exact finite matrix-group algorithm.  Record independent order gates
   (|H|=105815808) and (|H'|=2939328), rather than treating either order as
   an input.  If a custom tuple implementation is used instead of GAP's exact
   matrix-group backend, compute the normal closure of
   (c=[X,Y]) by iteration: start with (L=\langle c\rangle), adjoin
   (s^{X^{\pm1}},s^{Y^{\pm1}}) for every current generator (s), and
   recompute the exact subgroup until all such conjugates lie in (L).  At
   stabilization (L) is normal in (H=\langle X,Y\rangle), contains (c),
   and every adjoined element is a conjugate of (c); hence
   (L=\langle\!\langle c\rangle\!\rangle_H=H').  This is a terminating finite
   algorithm, but only if subgroup membership/closure is exact.

3. Restrict the decoded first-block map to (widetilde H').  Compute its
   image (Q=\pi(H')) and kernel (K) exactly.  Independently require
   (|Q|=367416), (|K|=8), and
   (|H'|=|Q|\,|K|=367416\cdot8=2939328).  Enumerate (K), require
   `Length(Elements(K))=Size(K)`, distinct elements, and identity roof block
   for every element.  This is the point at which matrix-only kernel elements
   cannot be lost.

4. Enumerate all of (Q) to exhaustion (a Cayley BFS on decoded roof
   permutations is sufficient), retaining a parent-pointer word/section for
   every element.  Do not use only the 972 requested roofs or only the order
   expected from a receipt.  For every frozen row roof (r), require
   (r\in Q), obtain an exact (h_r\in H') with (pi(h_r)=r), and scan

   \[
     \pi^{-1}(r)=h_rK=\{h_rk:k\in K\}.
   \]

   Kernel normality makes this a complete right coset; the order and distinct
   element gates make it impossible for a partial (K) to masquerade as a
   fiber.

5. Extract the five (4\times4) blocks from every (h_rk) and evaluate the
   exact v2 paper-convention defect (including the reverse-list `PaperProd` and
   literal A.18 ordering).  Require exactly 972 unique target keys, every fiber
   size 8, and one identity defect per row (with the corresponding seven
   nonidentity defects).  A candidate status may be emitted only after these
   gates; all-pass is still UNKNOWN.

The direct-sum construction itself introduces no mathematical loss.  `Size`,
`DerivedSubgroup`, `Kernel`, and `Elements` must nevertheless be allowed to
finish; an API failure, cap, timeout, or incomplete enumeration is not a
negative result.

## Calibration and false shortcuts

Run the same representation at the frozen (q=3) and (q=4) calibration
parameters before admitting a (q=5) receipt.  Check the supplied exact
orders (|H|=105815808), (|H'|=2939328), projected order (367416), kernel
order (8), and the 972 complete size-8 fibers with one identity defect per
row.  These are independent calibration identities, not assumptions for the
q=5 run; if the frozen q=3/q=4 manifests use parameter-specific values, those
values must be compared separately rather than copied from q=5.

The following tempting shortcuts are only semidecisions:

- The family ({c^{x^iy^j}}) is not generally closed under conjugation by
  (x) or (y); exact orders of (x,y) do not prove it generates (H').
- A few roof lifts, or relator evaluations from a projected presentation,
  can generate only a proper subgroup and silently miss matrix-only elements
  of (K).  They are safe only after the normal-closure/derived-group equality
  above is proved or checked by an exact order equality.
- `|K|=8` used as a stopping condition, a capped Cayley search, a bounded word
  list, random samples, or 972 representatives alone cannot prove completeness.
- One `PreImagesRepresentative` per row proves neither surjectivity onto all
  (Q) nor completeness of its fiber without the exhaustive (Q), exact
  kernel, and coset gates.
- Passing braid/matrix relation selftests or observing the expected order in a
  quotient does not prove that the chosen projection or A.18 defect convention
  is the original (E) map.
