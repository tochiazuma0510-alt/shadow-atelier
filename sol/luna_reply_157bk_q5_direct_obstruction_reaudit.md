# Luna reply 157bk — q5 direct profinite-obstruction re-audit

## Verdict

The proposed one-direction argument is mathematically sound under its stated
typing hypotheses.  The earlier 157bi audit required more than is needed: an
isolated finite-index PB4 source object, its reduction fiber, and the raw 158
presentation are not necessary for this obstruction.  A finite homomorphism
of PB4 already gives a valid contrapositive test for an exact profinite
pentagon.

Consequently, after the exact roof map and the literal A.18/Burau maps are
bound to the frozen model, one q5 receipt with a zero identity-defect count
and an independent checker PASS is enough to exclude one target from the
global image.  With the theorem-level premises

```text
X = GT^heart(M), |X| = 972,
A <= I = im(widehat GT -> X) <= X,
|A| = 324, and I a subgroup,
```

that single exclusion forces `I=A`.  No advance outside label or explicit
324-row arithmetic list is needed for the index-3 step.

## 1. The finite-group argument

Let `Psi=(r,b_1,...,b_5): F -> R x GL_4(F_q)^5` and let
`H=im(Psi)`.  Since `Psi` is onto its image,

```text
Psi(F') = [Psi(F),Psi(F)] = [H,H] = H'.
```

This is an equality, not a density approximation: every commutator in `H`
has lifts in `F`, and products of lifted commutators lift its whole derived
subgroup.  The projection `pi:H' -> R'` therefore has, for every
`fbar in R'`, the exact fiber

```text
pi^(-1)(fbar) = h0 * K_H,
K_H = ker(pi),
```

for any one `h0` above `fbar`.

Because `H` is finite, `Psi` extends uniquely to a continuous map from the
profinite completion.  The image of the closure of `F'` is still exactly
`H'`, since it already contains the finite subgroup `Psi(F')=H'`.  A genuine
profinite GT element has `fhat` in the closed commutator subgroup (for the
original profinite GT this is also a standard consequence of the GT
relations).  Thus a hypothetical lift above `fbar` has finite tuple image in
the same complete coset `h0*K_H`.

Let `D_q` be the five-block image of the literal B4 pentagon defect.  The
five A.18 maps and the Burau representation are homomorphisms, so the exact
profinite pentagon gives

```text
D_q(Psi_hat(fhat)) = identity.
```

If every element of `h0*K_H` has nonidentity `D_q`, no such `fhat` exists.
This is the direct finite-quotient obstruction.  It uses only the forward
implication “global pentagon lift implies finite defect identity”; it does
not need a converse, cofinality, isolatedness, or a source-fiber theorem.

## 2. Audit of the proposed steps

### `Psi(F')=H'`

PASS.  This is the standard image-of-derived-subgroup identity for a
surjection onto `H`.

### Profinite finite-image passage

PASS.  A homomorphism from the free group to a finite group extends to the
profinite completion, and the finite image of the closed commutator subgroup
is `H'`.

### Right-coset fiber

PASS.  The producer's `h0*K_H` is exactly the preimage of one roof element in
`H'`; it is not a sample and does not depend on a word bound.  The right/left
choice is fixed by the code's tuple multiplication and is checked by the
receipt digest.

### Five common `F2` maps

PASS at the free-group level.  The current v4 code uses one common pair of
free generators and the five literal pairs

```text
123       : (x12,              x23)
234       : (x23,              x34)
12,3,4    : (x13*x23,          x34)
1,23,4    : (x12*x13,          x24*x34)
1,2,34    : (x12,              x23*x24).
```

Each assignment extends to a homomorphism from the same `F2`; no independent
source words are being mixed.  The six pure generators are formed from the
three Burau braid generators in the standard conjugate/square pattern, and
the checker replays the braid and commuting relations.

### Defect orientation

PASS for the current literal-A.18 route.  If the five tuple blocks are
`(b_1(f),...,b_5(f))` in the order above, `v4_defect` evaluates, in the
code's documented paper-product convention,

```text
(b5(f)*b3(f))^(-1) * b2(f) * b4(f) * b1(f).
```

This is the unconditional B4 pentagon defect (the paper's `D-tilde` form),
not the old reverse-rho norm.  No condition-(I) identification with a rho
norm is being used.  The earlier warning about rho blocks and raw 158 rows
does not invalidate this direct literal-coface calculation.

Thus there is no algebraic failure in the proposed direct implication.

## 3. What the actual v4 producer/checker computes

For q5 the producer uses the two tuple generators

```text
H <= Sym(36) x GL_4(F5)^5,
H'=[H,H],
pi:H' -> R',
K_H=ker(pi).
```

The equivalent action on five copies of `F5^4` would have degree
`36+5*625=3161`; retaining matrices is only the low-memory representation
of the same finite tuple image.  The producer starts with the commutator of
the two tuple generators, closes its conjugates by both generators and their
inverses, traverses the complete projected derived section of order
`367416`, and enumerates the matrix-only Schreier kernel exactly.

For every frozen row it replays the word only to bind the roof key.  It then
selects the exact section element `h0` in `H'` over that roof permutation and
scans `h0*K_H`.  Not requiring the literal frozen word to lie in `H'` is
correct here: the direct argument concerns all commutator representatives
over the same roof value, and the complete finite image of those
representatives is precisely this coset.

The independent v4 checker reconstructs the Burau matrices, the five A.18
pairs, `H'`, the projected section, `K_H`, every row coset, and every defect.
It checks the q3/q4 calibration receipts and all q5 row digests.  Therefore
the current finite scan is the proposed `h0*K_H` scan, not a different 158
normal closure or a random correction sample.

The candidate status means that at least one row has
`identity_image_defect_count=0`; hence all elements of that row's finite
coset have nonidentity defect.  “Zero fiber” here means zero identity
defects, not an empty coset.

## 4. What is and is not logically needed

For this one-direction obstruction, none of the following is necessary:

* a subgroup `N in NFI_PB4(B4)`;
* B4-normality or isolatedness of the tuple kernel;
* a PB4 quotient/kernel packaged as the paper's source object;
* the 158 raw presentation or its rho normal closure;
* enumeration of every `GT^heart(K)` source lift;
* checking the hexagons for all elements of the superset fiber.

The last item is important: scanning a superset can create false positives,
but cannot create a false exclusion.  Any hypothetical global lift is in
that superset and must satisfy the pentagon, so an all-nonidentity superset
is already an obstruction.

What must be bound is smaller and different:

1. the `build_roof()` generators must be the exact marked map
   `r:F2 -> PB3/M`, and the frozen `(m,key,word)` row must be bound to the
   corresponding element of `X`;
2. the displayed five A.18 substitutions and Burau generator convention must
   be pinned as the maps used by both producer and checker, including the
   displayed defect orientation;
3. the accepted theorem-level ledger must bind `X=GT^heart(M)`, its order,
   the arithmetic subgroup order, and `A <= I <= X` with `I` a subgroup.

The current `semantic_premises` JSON is a digest-bound declaration, not a
proof of item 1 or item 3.  If those premises are not already accepted
outside this workflow, a short roof/X semantic certificate and the theorem
ledger must be attached to the terminal seal.  This is a typing/provenance
gate, not a PB4 isolated-source computation.

For clarity, without item 2 a finite tuple receipt would not suffice.  A
concrete model is obtained by taking any arbitrary finite tuple maps `b_j`
with an all-nonidentity defect coset while taking the actual PB4
representation to be trivial.  A genuine pentagon then has identity image
under the actual representation, but the unrelated arbitrary tuple reports
nonidentity.  This model violates the claimed “literal A.18 followed by
Burau” premise; it shows only why that premise must be bound, not a failure
of the direct theorem once it is bound.

## 5. Index-3 promotion

Assume the theorem-level premises requested in the task.  A q5 zero row gives
an element `t in X` with `t notin I`.  Since `A <= I <= X`, Lagrange gives

```text
|I| is a multiple of 324 and divides 972,
```

so `|I|` is either `324` or `972`.  The zero row rules out `I=X`; hence
`|I|=324`, and `A<=I` with equal order gives `I=A`.

No explicit 324-row arithmetic list is needed.  No advance outside label is
needed either: the obstructed row is automatically outside `A`, because
`A<=I` and it is not in `I`.  Normality of `A` is unnecessary for the order
dichotomy; it is needed only if one additionally wants to name `X/A` as the
group `C3` rather than use the index-three coset action.

This conclusion is conditional on the accepted `X/A/I` theorem premises.  A
q5 all-pass receipt gives no such exclusion and therefore does not decide A.

## 6. Exact terminal seal contract

The direct-A terminal seal should require all of the following, with no
resource or timeout substitution:

```text
Q5_DIRECT_OBSTRUCTION_SOURCE_SHA_BOUND
Q5_DIRECT_OBSTRUCTION_ROOF_X_BINDING_PASS
Q5_DIRECT_OBSTRUCTION_A18_BURAU_FORMULA_PASS
Q5_DIRECT_OBSTRUCTION_Q3_Q4_CALIBRATIONS_PASS
Q5_DIRECT_OBSTRUCTION_Q5_RECEIPT_PASS (q=5, a=2 or 4)
Q5_DIRECT_OBSTRUCTION_CHECKER_PASS (all 972 rows and complete K_H fibers)
Q5_DIRECT_OBSTRUCTION_ZERO_ROW_BOUND (explicit row/key/digest, count=0)
Q5_DIRECT_OBSTRUCTION_INDEX3_PREMISES_BOUND
Q5_DIRECT_OBSTRUCTION_TERMINAL_A
```

The q5 receipt must retain the full row ledger, exact kernel elements and
kernel generators, source/target/tuple digests, q3/q4 receipt hashes, and an
immutable workflow run/artifact identity.  The semantic gates bind only the
three logical premises listed in Section 4; they do not require a new heavy
q5 run if the current receipt already passes.

Under that contract, one zero row is a proof that `I != X`, then the index-3
dichotomy proves `I=A`, and the remaining `648` elements of `X` are all
non-arithmetic/fake.  This is a terminal A result, not a B4-B result and not
a claim that the finite tuple kernel is an isolated PB4 refinement.

No GAP, Git, GHA, or implementation change was made in this audit.

Q5_DIRECT_OBSTRUCTION_TERMINAL_A_IF_ZERO
