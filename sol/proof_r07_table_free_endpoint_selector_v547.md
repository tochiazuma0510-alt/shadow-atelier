# R07: a table-free endpoint selector with exact exponent normalization (v547)

Author: root / 2026-09-05

Status: new paper strengthening of v545, using the literal pre-normalizers
already constructed in v459. No group-coordinate table, numerical physical
preimage, or actual new pivot is supplied here. `verified=false`.

## 1. Fixed premises and the two already literal words

Use F=F(x,y), Omega=ker(F->Delta), N0=ker(F->Q0),
Gamma0=N0/Omega, and the marked Q2 quotient of Q0. The retained finite facts
used in v545/v546 are

```text
|Gamma0|=243, |Gamma0'|=3, |Phi(Gamma0)|=27, Exp(Gamma0)=9,
epsilon(N0)=2 Z^2, epsilon(Omega)=18 Z^2.                 (1.1)
```

The exponent lattices are the actual marked ones, not an inference from an
unmarked abelian group type: see Fable's v2 addendum section5.1. The two
explicit words from v459(2.1), in the pinned nineteen-word Q0 presentation,
are

```text
r_x=q1 q6^(-2) q7^4 q9,      epsilon(r_x)=(2,0),
r_y=q8^(-1) q4^(-1),        epsilon(r_y)=(0,2).           (1.2)
```

Both are in N0. Their exact roster and canonical hashes remain those of
v459; no new generator choice or s3/s5 coordinate matching is required.
Set a=Theta(r_x), b=Theta(r_y). Throughout,

```text
[u,v]=u^(-1) v^(-1) u v.                                (1.3)
```

The first marked E3 projection of Delta has second coordinates
x->u1, y->u3, with u3^u1=u3 u4 and u4 central of order3. Its subgroup
H=<u1,u3> is the exponent-three Heisenberg group of order27, as in v546(2.1).
This projection alone is NOT faithful on the order27 Phi(Gamma0).

## 2. The abelian part is read by ordinary integer exponent sums

The map

```text
e: Gamma0 -> (Z/9)^2,
e(Theta(n)) = epsilon(n)/2 mod9, n in N0,                (2.1)
```

is well-defined: two such representatives differ by Omega, whose exponent
vectors are in18 Z^2. It is onto by (1.2). Since its codomain has order81
and |Gamma0/Gamma0'|=243/3=81, it induces an isomorphism

```text
Gamma0_ab = (Z/9)^2,             e(a)=(1,0), e(b)=(0,1). (2.2)
```

In particular a,b form a basis modulo Phi and generate Gamma0 by the finite
p-group maximal-subgroup argument. The proof of v545 section3 applies to
these actual a,b too: Gamma0' is central (its automorphism group has order2),
the cubes are central of order3, and

```text
Phi(Gamma0)=<a^3> x <b^3> x <[a,b]> = C3^3.             (2.3)
```

There is no new enumeration in (2.2)--(2.3). For h in Phi represented by w
in N0, its first two coordinates in (2.3) are exactly

```text
alpha(h)=epsilon_x(w)/6 mod3,
beta(h)=epsilon_y(w)/6 mod3.                             (2.4)
```

Indeed the exponent images of a^3,b^3 are6e_x,6e_y, while a commutator has
zero integer exponent. The divisions in (2.4) are in the integers, not
division by zero in F3. The condition h in Phi implies epsilon(w) in6 Z^2
by (2.2); changing w by Omega changes these quotients by multiples of3.

## 3. The missing central coordinate is one second-order word coefficient

For a literal signed-letter word w define

```text
A(w)=epsilon_x(w), B(w)=epsilon_y(w),
omega(w)= sum over x^sigma letters of
          sigma * B(prefix before that letter) mod3.   (3.1)
```

This uses ordinary prefix exponent sums. It is a signed-word invariant:
free cancellation of x x^-1 contributes B-B=0, and cancellation of y y^-1
restores B without contributing. Its product and inverse rules are

```text
omega(uv)=omega(u)+omega(v)+B(u) A(v) mod3,
omega(u^-1)=-omega(u)+A(u) B(u) mod3.                   (3.2)
```

These follow by separating the letters of the two factors in (3.1).
Thus they apply directly to a product/inverse SLP without expanding its
word. More generally

```text
omega(u^m)=m omega(u)+binom(m,2) B(u) A(u) mod3          (3.3)
```

for every integer m; for negative m use (3.2), or the integer polynomial
identity. Exact exponent sums are retained for the later normalization.

In H use normal form u1^A u3^B u4^C. The marked PC relation gives

```text
(A,B,C)*(A',B',C')=(A+A',B+B',C+C'+B A') in F3^3.       (3.4)
```

Equations (3.1)--(3.2) therefore compute the actual E3 coordinate:

```text
Theta_E3(w)|H = u1^(A(w)) u3^(B(w)) u4^(omega(w)).       (3.5)
```

The sign is fixed by (1.3): omega([x,y])=-1=2. For any u,v,

```text
omega([u,v])=B(u) A(v)-B(v) A(u) mod3.                 (3.6)
```

Consequently (1.2) gives

```text
Theta_E3(a^3)=Theta_E3(b^3)=1,
omega([r_x,r_y])=0*0-2*2=-4=2 mod3.                   (3.7)
```

Here the first line means the H projection; their Q0 components are already
identity. Since [a,b] generates Gamma0' of order3, (3.7) proves that this
projection is faithful on Gamma0'. It does not assert faithfulness on all
of Phi. The two exponent coordinates in (2.4) supply its missing order9
kernel. Altogether the three-coordinate readout is

```text
h=(a^3)^alpha (b^3)^beta [a,b]^gamma,
alpha=epsilon_x(w)/6 mod3,
beta=epsilon_y(w)/6 mod3,
gamma=2 omega(w) mod3.                                 (3.8)
```

This is a proved closed readout of all27 elements, with no marked27-product
lookup, Delta enumeration, or BFS. The factor2 in gamma inverts the value2
in (3.7). For h^-1 the commutator coordinate is instead omega(w).

## 4. One formula repairs the endpoint AND the exact exponent pair

Let w be an actual word such that

```text
w in N0,             epsilon(w) in6 Z^2.                (4.1)
```

Let g be the signed representative in {0,1,-1} of omega(w) in F3. Define

```text
R(w)=w (r_x^3)^(-epsilon_x(w)/6)
       (r_y^3)^(-epsilon_y(w)/6) [r_x,r_y]^g.            (4.2)
```

The two displayed quotients are exact INTEGERS, not reduced residues.
Equivalently, the powers of r_x,r_y are -epsilon_x(w)/2 and
-epsilon_y(w)/2, which are multiples of3. The order of the three appended
factors in (4.2) is fixed as written; no literal factor reordering is used.

### Theorem4.1 (table-free normalized endpoint selector)

For every w satisfying (4.1),

```text
R(w) in Omega intersect [F,F],
J_Q(R(w))=J_Q(w) for EVERY quotient Q of Q0.             (4.3)
```

Proof. By (2.2), h=Theta(w) lies in Phi(Gamma0). Formula (2.4) shows that
the first two factors after w cancel its two cube coordinates, since their
integer exponents give the required residues modulo3. The remaining H
central coordinate is omega(w)+2g=0 by (3.7). Faithfulness on Gamma0', or
the full coordinate formula (3.8), now gives Theta(R(w))=1.

Ordinary exponent sums in (4.2) are exactly

```text
epsilon(w)-6(epsilon_x(w)/6)e_x
          -6(epsilon_y(w)/6)e_y+(0,0)=(0,0).             (4.4)
```

Thus the result lies in [F,F], not merely a mod-three normalized kernel.
Finally every appended factor is in Phi(N0)=N0^3[N0,N0]. Its mod-three
Fox row vanishes at Q0, and hence at each quotient Q of Q0. Every factor,
including w, evaluates to identity in such Q, so Fox additivity proves
the second part of (4.3). QED.

Using residues instead of the exact integer exponents in (4.2) would only
normalize modulo18. The exact powers automatically absorb the old ninth-
power normalizers c_x=r_x^9,c_y=r_y^9. There is no second normalization step.
The three-factor count means powers of three fixed words; it is not a
constant bound on expanded word length.

## 5. Application to the legal-cycle readout and precise novelty

For z in the Q2 cycle space with tau2(z)=0, take the fixed-order Schreier
word w(z) of v542. The carry formula in v546 says its Q0 rotation is zero
and its ordinary exponent sums are zero modulo3. Since it is already in
N2, the zero rotation makes it lie in N0; the parity condition of N0 then
makes both exponents divisible by6. Thus (4.1) holds and

```text
C(z)=R(w(z)) in Omega intersect [F,F],
J_Q2(C(z))=z.                                          (5.1)
```

Alternatively use v545's equality of the actual Frattini subgroups to
deduce (4.1). Neither route needs an actual Gamma0 endpoint lookup for each
w(z). One reads exact exponents and omega by the scalar SLP rules (3.2),
then uses the fixed literal formula (4.2).

Relative to v545, this removes the remaining marked27-coordinate table
interface and combines endpoint repair with exact normalization. Relative
to v543, a failed chord test's legal source word can be read out with this
formula without a new finite-group arithmetic adapter. The actual cochain
and lower-multiplier adapters for that physical oracle are still absent.

This is not a solution of the physical equation G(v)=rho2, nor a proof of
PB4 preservation, completion of the other finite H floors, or full A0.
Compatibility in (4.3) concerns the SAME literal w and quotients of the
fixed Q0; it is not a coherent choice of words through cofinal refinements
beyond Q0. The word-valued R is not asserted to be a group homomorphism.
Seed30 production proceeds independently and does not consume this paper.

```text
ENDPOINT READOUT:                  TWO EXACT EXPONENTS + ONE WORD COEFFICIENT
NEW27-ELEMENT TABLE / BFS:         NOT REQUIRED BY FORMULA
EXACT INTEGER NORMALIZATION:      INCLUDED IN THE SAME THREE-FACTOR REPAIR
Q0 AND ITS QUOTIENT FOX ROWS:      PRESERVED
ACTUAL PHYSICAL TARGET / A0:       NOT DECIDED
COFINAL / FAKE / IHARA:            NOT DECLARED
verified=false
```
