# R07: a five-coefficient tree-potential oracle for the current separator (v543)

Author: root / 2026-09-05

Status: paper alternative to the scalar-orbit search, not an implementation
or actual membership result. It uses the complete constrained source from
v457/v458 and the existing Conn to account for the physical lower fibre.
It does not use a common actor on the aggregated physical target. It retains
the v541 corrected actual root batch as the current production route.
`verified=false`.

## 1. Fixed finite source and complete lower fibre

At the order-54,432 quotient Q2, use the single two-generator cycle space

```text
C1 = F3^(2*54432),
Z = ker(partial:C1 -> C0),        dim Z = 54433,
tau: Z -> F3^5,                  tau onto,
K = ker tau.                                            (1.1)
```

These are the actual marked objects in v457/v458, not eleven independently
chosen occurrence cycles. The two words c_x,c_y of v459 have J_Q2=0 and
normalized exponent vectors e_x,e_y. Hence the full augmented legal source
is exactly

```text
D = image(J_Q2,nu) = K x F3^2.                           (1.2)
```

The product in (1.2) is an equality of linear images, not a nonabelian
splitting: v542 materializes a z in K and c_x,c_y adjust nu arbitrarily.

Assume the actual same-owner Fox/occurrence/truncation map is authenticated:

```text
Psi: D -> W2,         onto,
pi: W2 -> W1,         onto,
ell = ell1 pi: W2 -> L,
G: W2 -> P.                                              (1.3)
```

Here W2 is the complete precision-two legal occurrence image, W1 is its
P1 truncation, and (ell,G) are the lower-physical/top-physical maps in v530.
For current data `dim W1=8059`, `L=F3^32260`, `P=F3^48384`. Crucially, Psi
is evaluated with the full filtered maps, not with homogeneous maps on
vectors that still have nonzero lower terms (v541).

The signed target under test is the retained rho2 in P. Its full correction
image at this grade is

```text
M2 = G(ker ell) = span(Conn) + G(ker pi).                  (1.4)
```

For the second equality, use the canonical lifts of the P1 basis to split
any u in ker ell into its lifted P1 part and an element of ker pi. The first
part has an ell-zero coefficient relation and its G value is in Conn;
conversely both displayed summands come from ker ell. This is the same image
as v535, independently of the choice of origin roster for ker pi.

## 2. Recover the lower multiplier from the existing Conn

Let btilde_i (i=0,...,8058) be the canonical lifts, with pairs

```text
(ell_i,g_i) = (ell(btilde_i),G(btilde_i)).
```

The existing Conn spans the images of ALL relations among these ell_i.
Let the current separator satisfy

```text
lambda(Conn)=0,            lambda(rho2)=1.                (2.1)
```

When a current enlarged echelon S_current is in use, retain in addition
`Conn <= S_current` and `lambda(S_current)=0`, as the actual separator
contract requires. These are the premises for the rank-rise statement in
Section 4; they are not needed for the abstract equivalence (2.4).

There is then a linear functional mu on L with

```text
mu(ell_i) = lambda(g_i) for every i.                      (2.2)
```

Proof: prescribe mu on `span{ell_i}` by (2.2). Two expressions for the same
lower row differ by a relation whose g-image is in Conn, so (2.1) makes the
prescription well-defined. Extend linearly to L. QED.

It is enough to use the existing lower-first pivot pairs (rank 6705) and
back substitution. No new lower closure is required. The concrete adapter
must retain or read those pairs and verify (2.2); the existence proof alone
is not an exported mu receipt. Its extension outside span{ell_i} is irrelevant
because pi is onto and these ell_i span ell(W2).

Define

```text
F_lambda(z,eta) = lambda G Psi(z,eta) - mu ell Psi(z,eta).
                                                               (2.3)
```

### Theorem 2.1 (complete current-separator test)

```text
lambda(M2)=0  iff  F_lambda(D)=0.                         (2.4)
```

Proof: if F_lambda vanishes, its value on any ker ell preimage is lambda G,
so lambda kills M2. Conversely, for u in W2 write its lower-source value as
`pi(u)=sum_i a_i pi(btilde_i)`. Then
`v=u-sum_i a_i btilde_i` is in ker pi, hence ker ell. If lambda kills M2,
it kills G(v); equation (2.2) kills F_lambda on the remaining lifted part.
Thus F_lambda vanishes on every u, and surjectivity of Psi gives (2.4). QED.

This subtraction is essential. Testing just `lambda G Psi` on all legal
cycles would test a larger source than the lower-zero fibre and could again
produce a false physical violation.

## 3. A tree potential and five scalar coefficients

Extend the known linear evaluation in (2.3) from cycles to raw chains by
the same Fox substitution and coordinate maps. Its adjoint is a cochain
and a two-coordinate auxiliary functional:

```text
F_lambda(z,eta) = f(z) + b(eta),
f in C1*,                    b in (F3^2)*.               (3.1)
```

Only the restrictions to cycles and the actual two normalized directions
matter. The eight stored auxiliary coordinates in a P1 row must not be
misread as eight independent source-normalization directions.

First check b(e_x),b(e_y). These are the evaluations on the two explicit
words c_x,c_y. Their Q2-Fox parts are zero, so they can be nontrivial tests
of the lower multiplier even though their top Fox parts vanish.

Next fix a rooted spanning tree of the oriented Cayley graph. Write an edge
as e:tail(e)->head(e), with graph boundary head-tail. Define p(1)=0 and
extend the potential p along the tree so that

```text
f(e) = p(head(e))-p(tail(e)) on each tree edge.           (3.2)
```

For a non-tree edge e let z_e be its fundamental cycle (tree path to tail,
then e, minus the tree path to head). Define

```text
r_e = f(e)-p(head(e))+p(tail(e)) = f(z_e),
t_e = tau(z_e) in F3^5.                                  (3.3)
```

The exact conversion from the implementation's Fox handedness to oriented
edge coordinates is part of the same-owner input. Formula (3.3) cannot be
combined with an unconverted opposite convention.

Because tau is onto and the z_e form a basis of Z, choose five non-tree
edges e_1,...,e_5 whose t_e are independent. Solve the five-equation system

```text
r_(e_i) = a(t_(e_i)),  i=1,...,5,
a in (F3^5)*.                                            (3.4)
```

### Theorem 3.1 (tree-potential annihilator)

```text
F_lambda(D)=0
iff b=0 and r_e=a(t_e) for EVERY non-tree edge e.         (3.5)
```

Proof: D=ker tau x F3^2 gives the auxiliary condition b=0. A functional on
Z vanishes on ker tau if and only if it factors through the surjective map
tau. The five selected cycles force that factor to be the unique a in
(3.4). The remaining fundamental cycles test the factorization on a basis
of Z. Tree edges merely fix the potential and add no further unknowns. QED.

Equivalently, let the extension tilde_tau be zero on tree edges and have
value t_e on each non-tree edge. The annihilator certificate is the one
cochain identity

```text
f = partial* p + a tilde_tau,          b=0.               (3.6)
```

Thus the prospective replacement for the entire current lambda-orbit scan
is two auxiliary evaluations, one tree integration, a 5-by-5 solve, and
54,433 fundamental-cycle scalar comparisons. Constructing f and the marked
t_e remains necessary. These numbers are not a runtime estimate for those
adapters, and are not an A0 completion bound.

## 4. A failed equality supplies a sparse legal cycle, not only a verdict

Suppose b=0 and some e fails (3.5). Express its five-coordinate endpoint

```text
t_e = sum_(i=1)^5 d_i t_(e_i),
z = z_e - sum_(i=1)^5 d_i z_(e_i).                       (4.1)
```

Then tau(z)=0 and

```text
F_lambda(z,0) = r_e - a(t_e) != 0.                       (4.2)
```

Only six fundamental cycles are needed in (4.1). A coefficient may be zero;
the bound is on the number of cycle terms, not on their expanded edge/word
length. If an auxiliary test fails first, use instead `(z,eta)=(0,e_i)`
with its known literal word c_i.

V542 materializes (4.1) as one actual-kernel word with chosen nu=0 using
the small endpoint repair and normalization. More generally it materializes
any `(z,eta)` in D. Let u=Psi(z,eta). Expand its full P1 truncation in the
existing basis and set

```text
pi(u) = sum_i a_i pi(btilde_i),
v = u - sum_i a_i btilde_i.                              (4.3)
```

Now pi(v)=0 in the complete P1 source, not merely in the physical lower
part. Equations (2.2) and (2.3) give

```text
lambda G(v) = F_lambda(z,eta) != 0.                      (4.4)
```

Thus G(v) is a genuine rank-raising physical correction for the current
separator. Literal products/inverses of the cycle word and canonical P1
DAGs implement the same subtraction, because they all lie in Omega and
Fox/nu are additive there. This does require a finite P1 reduction for the
selected candidate. It does NOT require solving for that candidate in the
complete 44-seed actor closure.

If (3.5) holds everywhere, (2.4) instead gives the complete grade-two
negative separator lambda(M2)=0, lambda(rho2)=1. That is a fail-closed
decision for this registered grade, not evidence toward the desired MEMBER.
No actual sign/outcome is predicted here.

## 5. Concrete new gates, retained work, and paper-closure boundary

The new finite data needed to use this theorem are:

1. the current lower multiplier mu and all 8059 equalities (2.2), using the
   existing Conn/P1 parent, not reconstructed closures;
2. the actual same-owner adjoint producing f,b, with nonzero mixed lower/top
   checks against full filtered evaluation;
3. one marked Q2 tree and complete five-coordinate t_e roster, including
   five independent selected columns; and
4. for a violation only, the v542 marked endpoint table and the selected
   P1 subtraction/materialization in (4.3).

At Q2 the edge cochain has `2*54432=108864` scalar entries, and the five-row
fundamental-cycle roster has `5*54433=272165` entries. There is no dense
54,428-by-physical-target matrix in (3.1)--(3.6), and no 504-fold repeat of
the 32,280-origin scalar evaluator. This is an algebraic work reduction;
without the new adapters and measurements it is not a speedup claim for
already running code. The complete t_e data are not asserted to have been
exported by the older five-row dimension proof.

V542 closes the constructive source-readout step. This note closes the
equivalence of a prospective small-coefficient cochain test and the current
full grade-two separation test, conditional on the explicit finite maps.
Neither note constructs the target preimage, decides the current lambda,
completes the remaining H grades, or supplies the PB4 block of finite A0.
There is no inference from this finite argument to the cofinal T2 lift.

The actual v541 root scan remains the immediate production priority. This
paper route is meant to avoid a later expensive orbit sweep if its bounded
same-owner adapters prove inexpensive, not to restart the accepted parents
or delay the corrected scan.

Task925 independently audits the equivalences and the six-cycle readout
PASS. Its clarification about lambda(S_current)=0 has been incorporated
above. The concrete input gates in this section remain unexecuted.

```text
CONN -> WELL-DEFINED LOWER MULTIPLIER:       PAPER PROOF
COMPLETE SEPARATOR -> TREE + 5 COEFFICIENTS: PAPER PROOF, MAP PREMISES
FAILED CHORD TEST -> <=6-CYCLE LEGAL SOURCE: PAPER CONSTRUCTION
ACTUAL mu / f / t_e RECEIPT:                NOT EXPORTED
ACTUAL NEW PHYSICAL PIVOT:                  NONE FROM THIS NOTE
GRADE2 / FULL A0 / COFINAL / FAKE / IHARA:   NOT DECLARED
verified=false
```
