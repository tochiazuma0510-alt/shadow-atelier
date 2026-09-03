# Task 575 audit — associated-grade Cayley--Fox caps in v454

## Verdict

The cap theorem is correct for the actual coupled-monomial transition-defect
blocks. One local completion-gate repair is required. Saturation certifies the
generated row space, but the three checks listed in v454 Section 3 do not by
themselves prove that arbitrary six-tag rows lie in the correlated occurrence
image. Also, an early saturation stop does not automatically provide the full
origin/actor reduction presentation required by v444 for the next grade. This
repair changes no cap, offer bound, or byte product.

## F1. Pure-grade right Fox boundary — PASS

For a literal relation \(w\), the left-prefix convention gives

\[
 J_x(w)(x-1)+J_y(w)(y-1)=w-1.
\]

Every registered compact relation, and every registered occurrence
substitution of it, has endpoint \(1\). The negative-letter branch of
affine_fox first multiplies the prefix by the inverse and then subtracts that
new prefix (v3 lines 210--225), so there is no negative-letter sign exception.
The crossed factors in v443 (3.2) belong to the exact filtered occurrence map
and do not alter the source endpoint identity.

A v444 seed defect or old-basis actor-transition defect is a linear
combination of reevaluated literal cycle rows. Left translation commutes with
the right boundary, and subtracting the stored lower reduction preserves the
cycle identity. Zero stored lower coordinates imply zero raw lower Fox
coordinates because the identity-tag PB3 map is filtered and invertible on
its two regular components (F5). Hence the first nonzero raw pair is pure
degree \(d\). In degree \(d\), every positive-degree factor coming from a
marked lift or an \(E(c)\) crossed term raises filtration. Only the \(Q_1\)
endpoints of \(x,y\) remain, proving v454 (1.3), including for old-basis lift
defects.

Here \(z\) in v454 (1.2)--(1.3) is necessarily the raw source Fox pair before
PB3 normalization and before the six occurrence maps. The stored tuple is its
correlated occurrence image.

## F2. Right-boundary coefficient character — PASS

Let \(u^\alpha\) have sign character
\(\eta(\alpha)=\eta_1^{\alpha_1}\eta_2^{\alpha_2}\eta_3^{\alpha_3}\).
On the left source-\(\lambda\) summand, associated-grade right multiplication
by a marked generator with \(A\)-part \(a\) has scalar

\[
 \lambda(a)^{-1}\eta(\alpha)(a)
 =\lambda(a)\eta(\alpha)(a),
\]

because every character of \(C_2^2\) has order two. Thus the summand indexed
by \(u^\alpha\) has one-dimensional cokernel exactly when
\(\eta(\alpha)=\lambda\); otherwise its twisted Cayley coinvariants vanish.
This uses no semisimplicity of \(k[P]\): the marked pair generates
\(P\times A\), so a nontrivial twist has a pure-\(A\) loop with nontrivial
holonomy, while the trivial twist has the one-dimensional \(H_0\) of the
connected \(P\)-Cayley graph.

The cokernel dimension is therefore exactly \(m_{d,\lambda}\), and

\[
 \dim\ker\partial_{d,\lambda}
 =2(504h_d)-(504h_d-m_{d,\lambda})
 =504h_d+m_{d,\lambda}.
\]

It is neither \(h_d\) nor zero. A conventionally placed inverse on \(\lambda\)
cannot alter the answer here; F4 also checks the live convention.

## F3. Independent monomial enumeration — PASS

Write the nontrivial characters as
\(\eta_1,\eta_2,\eta_3=\eta_1\eta_2\). Direct enumeration gives:

| \(d\) | monomial types | \((m_{d,1};m_{d,\eta_1},m_{d,\eta_2},m_{d,\eta_3})\) |
|---:|---|---:|
| 1 | permutations of \((1,0,0)\) | \((0;1,1,1)\) |
| 2 | three \((2,0,0)\), three \((1,1,0)\) | \((3;1,1,1)\) |
| 3 | \((1,1,1)\), six \((2,1,0)\) | \((1;2,2,2)\) |
| 4 | complement of degree 2 | \((3;1,1,1)\) |
| 5 | complement of degree 1 | \((0;1,1,1)\) |
| 6 | \((2,2,2)\) | \((1;0,0,0)\) |

The complement map
\(\alpha\mapsto(2,2,2)-\alpha\) sends \(d\) to \(6-d\) and preserves the
character because all added exponents are even. The row sums are
\((3,6,7,6,3,1)=h_d\).

## F4. Live Fourier-array label — PASS

In evaluate_occurrence_pair, the outer Fourier loop is over source_label.
transport[tag][source_label] is used only to evaluate the Fourier weight in
that occurrence; the result is written to the source_index slice of lower and
grade (v3 lines 394--404). The projector then rejects leakage outside the
selected source index (lines 468--494). Thus the persistent array axis is the
left source character, not the transported target character. Task540
(F2.2)--(F2.4) accounts for the inverse in occurrence transport. All
characters have order two, and the three nontrivial multiplicities are equal,
so inversion cannot change the cap table.

## F5. Identity occurrence and PB3 normalization — PASS

The first registered pair in floor.OO is \(([1],[2])\), so a retained fxy slot
is the identity substitution. The live code sets \(b=(yx)^{-1}\), checks
\(xby=1\), and maps a raw pair to

\[
 (v_x,v_y)\longmapsto
 (-v_xx,\ v_y-v_xxb,\ \operatorname{aug}(v_x)).
\]

This is v454 (2.3), with its \(a=x\). The first regular component recovers
\(v_x=-({\rm first})x^{-1}\), after which the second recovers \(v_y\).
Therefore the PB3 map, and hence the complete six-tag map containing it, is
injective. The six PB3 augmentations and two normalized exponents are still
retained by the live evaluator; a v444 pure defect must have them zero. The
argument licenses no quotient of the identity slot, omission of a regular
component, or tagwise-independent occurrence space.

## F6. Numerical caps and grade-one consistency — PASS

Substitution in \(504h_d+m_{d,\lambda}\) gives:

| grade | trivial | each nontrivial |
|---:|---:|---:|
| 1 | 1,512 | 1,513 |
| 2 | 3,027 | 3,025 |
| 3 | 3,529 | 3,530 |
| 4 | 3,027 | 3,025 |
| 5 | 1,512 | 1,513 |
| 6 | 505 | 504 |

The measured grade-one ranks \((1509,1512,1512,1512)\) lie below these caps,
with codimensions \((3,1,1,1)\). This is only a consistency check; it is not
used to prove the cap.

## F7. Saturation and queue bounds — LOCAL REPAIR

For the legal occurrence image, saturation is sound. If its retained rank
equals \(\dim\ker\partial_{d,\lambda}\), then

\[
 H_{d,\lambda}\subseteq
 \Phi(\ker\partial_{d,\lambda})
\]

and injectivity of \(\Phi\) force equality. Every later legal origin and actor
image is dependent. Rank coincidence alone is insufficient, however: checking
only the identity-slot boundary, the character label, and identity-slot
injectivity does not prove that arbitrary coordinates in the other five tags
are the correlated image of the recovered raw pair.

Saturation also completes only the row space. It does not manufacture the
reductions required by v444 (2.2)--(2.3). If a saturated block is to serve as a
next-grade transition presentation, every registered origin and all four
actor images of every retained pivot still need replayable reductions, or an
independently replayable equivalent presentation.

Replace the completion proviso in v454 Section 3, and qualify the last sentence
of Section 4, by:

> For closure-span completeness the gate is
> queue_exhausted OR cayley_fox_ambient_saturated, provided the checker
> replays that every accepted row is the full correlated six-tag occurrence
> image, with the registered auxiliary conditions and ancestry, of a
> source-character raw pair satisfying (1.3). Identity-tag injectivity
> identifies that raw pair but does not by itself certify the other five
> tags. Saturation may stop discovery of the row space. It may not be called
> a complete v444/v451 transition presentation until all registered origin
> reductions and all four actor reductions for every retained pivot have
> also been recorded and replayed.

Without saturation, the actual origins-first, accepted-pivot FIFO,
four-actor discipline of v452 gives exactly

\[
 \#\mathrm{offers}=n_2+4r,\qquad
 n_2=44+4(8059)=32280.
\]

Therefore

\[
 32280+4(3027)=44388,\qquad
 32280+4(3025)=44380.
\]

If a saturated artifact also fills the complete next-grade presentation, the
same reductions may still have to be processed. The early stop is then a
row-discovery saving, not permission to omit those records.

## F8. Packed live-basis resources — PASS

At four trits per byte, the largest width-36,288 source basis is

\[
 3027(36288/4)=27,460,944\ \text{bytes}.
\]

The synchronized width-48,384 companion on the same pivots is

\[
 3027(48384/4)=36,614,592\ \text{bytes}.
\]

These are packed live-row products only. V454 explicitly says streamed
reduction transcripts may be much larger and gives them no byte bound. It
also does not claim that the physical lower-first rank is bounded by 3,027;
that physical echelon has a different ambient and input family.

## F9. Direct cycle basis versus seed ancestry — PASS

Section 5 correctly separates \(Z_Q=\ker\partial_Q\), the five-row kernel
\(K_Q=\ker\tau_Q\), and a replayable compact-seed/actor presentation. A
spanning-tree chord, or a vector obtained as a kernel of the five functionals,
does not thereby carry coefficients in the 44 compact seed orbits. V454 calls
the direct construction exact only in principle and explicitly requires a
compact-seed/actor DAG, or a literal closure proved to attain the exact rank,
before use in a MEMBER word or a later grade. It makes no direct-replacement
or ancestry overclaim.

No grade membership, A0, COMMON, compatible cofinal lift, fake, or Ihara claim
is promoted by this audit. verified=false.

ASSOCIATED_GRADE_CAYLEY_FOX_CAP_V454_AUDIT_PASS_AFTER_REPAIR
