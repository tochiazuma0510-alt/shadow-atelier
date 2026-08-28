# R07 class-two compiler for the first nonlinear remainder v266

Author: Sol / 2026-08-28

Status: paper theorem after v99, v173, v251--v252, v260, and v263.  It gives
an exact finite formula for the first nonlinear remainder `q2` and proves
that no quotient deeper than the first two Zassenhaus layers is needed to
compute it.  It also isolates a later-rung simplification: from depth two
onward, terms containing two occurrences of the newly applied correction
skip the immediately following layer.  The actual A5/A6 correction ancestry
has not yet been produced, so no numerical R07 `q2`, cyclic membership,
compatible lift, fake, or Ihara witness is declared.  `verified=false`.

## 1. The exact two-layer object

Retain the relative pro-3 correction group \(P\) and its Zassenhaus
filtration \(P_{(r)}\) from v263.  Put

\[
 \mathfrak p_1=P_{(1)}/P_{(2)},\qquad
 \mathfrak p_2=P_{(2)}/P_{(3)}.
\tag{1.1}
\]

The quotient

\[
 \overline P_2=P/P_{(3)}
\tag{1.2}
\]

has nilpotency class at most two and exponent three.  Since the class is
strictly smaller than \(3\), the truncated Lazard logarithm identifies its
multiplication with the class-two Campbell--Hausdorff law

\[
 (u,U)\star(v,V)
 =\left(u+v,\ U+V+\frac12[u,v]\right),
 \qquad \frac12=2\in\mathbf F_3,
\tag{1.3}
\]

where \(u,v\in\mathfrak p_1\) and \(U,V\in\mathfrak p_2\).  Formula (1.3)
may equivalently be taken as the deterministic Hall-collection algorithm;
no choice of a rational logarithm is used beyond this finite exponent-three
quotient.

The seven literal relation contexts consist of the two printed hexagons and
the five A.18 cofaces in their frozen order.  For one of the three residual
blocks \(R\), write the exact ratio after right correction as

\[
 R(Fc)R(F)^{-1}=d_1(c)d_2(c)\cdots d_{m_R}(c),
\tag{1.4}
\]

where every \(d_i(c)\) is the corresponding context substitution of \(c\)
or \(c^{-1}\), transported by the exact fixed prefix.  This factorization is
obtained by literal collection of the printed word, so inverse signs,
right-correction convention, and coface order are part of the data.

For a fixed ordered materialization \(c=\operatorname{Mat}(v)\), collect in
\(\overline P_2\)

\[
 \log d_i(c)=\ell_i(v)+\tau_i(v),
 \qquad \ell_i(v)\in\mathfrak p_1,quad
 \tau_i(v)\in\mathfrak p_2.
\tag{1.5}
\]

The term \(\tau_i\) includes the exact class-two part of the chosen ordered
source word and its fixed-prefix transport.  It is not discarded or replaced
by an ambient additive representative.

## 2. Closed formula for `q2`

### Theorem 2.1 (PRINTED-ORDER CLASS-TWO FORMULA)

For every residual block \(R\), the degree-one Jacobian value and the
degree-two nonlinear remainder of (1.4) are

\[
 B_{1,R}(v)=\sum_{i=1}^{m_R}\ell_i(v),
\tag{2.1}
\]

and

\[
 \boxed{
 Q^{(2)}_{F,R}(v)=
 \sum_{i=1}^{m_R}\tau_i(v)
 +\frac12\sum_{1\le i<j\le m_R}
       [\ell_i(v),\ell_j(v)].}
\tag{2.2}
\]

The order \(i<j\) is the literal order in the hexagon or printed A.18 word.
For the v263 first correction \(c_1=\operatorname{Mat}(-a)\), the complete
first nonlinear obstruction is exactly the three tagged values

\[
 \boxed{
 q_2=\bigl(
 Q^{(2)}_{F,H1}(-a),
 Q^{(2)}_{F,H2}(-a),
 Q^{(2)}_{F,A.18}(-a)
 \bigr).}
\tag{2.3}
\]

#### Proof

Apply (1.3) successively to the ordered product (1.4).  Its degree-one part
is the sum of the \(\ell_i\), which is precisely the occurrencewise Fox
Jacobian of v99.  Its degree-two part is the sum of the individual degree-two
pieces plus one bracket for every earlier/later pair, with coefficient
\(1/2\).  No bracket of length three survives modulo \(P_{(3)}\).  This gives
(2.1)--(2.2).

V263 defines \(q_2\) as the degree-two part of the exact word-product error
after the degree-one correction has been separated.  Equation (2.2) is
exactly that discarded word-product part, computed separately in the three
tagged blocks.  Substituting the registered correction \(-a\) gives (2.3).
\(\square\)

In particular, (2.2) retains both sources of the error which a raw additive
Fox chain loses: the class-two part of each materialized occurrence and the
crossed-prefix brackets between different occurrences.

### Corollary 2.2 (TWO-LAYER SUFFICIENCY)

The actual `q2` depends only on:

1. the images of the fixed prefixes and context substitutions in their
   class-two quotients;
2. the ordered word-bearing ancestry of \(a\) modulo \(P_{(3)}\); and
3. the frozen occurrence order and signs.

No third or deeper successor layer and no all-rung lift is needed to compute
`q2`.

#### Proof

Every term in (2.2) lies in \(\mathfrak p_2\), and every term omitted from the
class-two collection has Zassenhaus depth at least three.  \(\square\)

This does not mean that only the additive class of \(a\) is enough.  Two
word representatives of the same degree-one value can differ in degree two.
The retained ordered `Mat` ancestry fixes that difference and is therefore
load-bearing.

## 3. Direct word-bearing ancestry for the quadratic terms

Suppose the actual A5/A6 output writes

\[
 a=\sum_{j=1}^{s}b_j[g_jr_jg_j^{-1}],
 \qquad b_j\in\mathbf F_3,
\tag{3.1}
\]

in the registered order.  V251 materializes \(-a\) by exponents
\(0,1,-1\).  In \(P/P_{(3)}\), one scan of those factors gives its pair
\((u,U)\) under (1.3).  Applying the ten registered substitutions and seven
defect occurrences gives every \((\ell_i,\tau_i)\) in (1.5).

Each summand of (2.2) consequently has a literal source ancestry:

- \(\tau_i\) is represented by the degree-two component of one substituted
  ordered word; and
- \([\ell_i,\ell_j]\) is represented by the commutator of the two retained
  occurrence words in that order.

Thus a producer need not return only a vector for `q2`.  It can return a
coefficient-bearing list of the underlying substituted words and pairwise
commutators.  A checker can independently collect the same class-two words
and compare the result without importing a producer echelon.

## 4. The actual cyclic-return decision becomes one finite solve

Let

\[
 L_2=[\Xi\beta]_2\subseteq
 \mathcal F^2\mathcal Z/\mathcal F^3\mathcal Z
\tag{4.1}
\]

be the independently reconstructed diagonal orbit of the actual defect.  By
v263 Corollary 4.3, the pointed route requires one explicit coefficient
\(\nu_2\) with

\[
 q_2=[\nu_2\beta]_2.
\tag{4.2}
\]

### Proposition 4.1 (FINITE FIRST-RETURN CERTIFICATE)

After the word-bearing \(a\) is available, (2.2) followed by a linear solve
in (4.1) returns exactly one of:

1. `MEMBER`, with a retained common-source coefficient ancestry \(\nu_2\);
2. `NONMEMBER`, with a complete separating dual on the full orbit span; or
3. `UNKNOWN_RESOURCE`.

On MEMBER, the next pointed coefficient is

\[
 \lambda_2=\mu+\nu_2.
\tag{4.3}
\]

#### Proof

Theorem 2.1 computes one literal vector in the finite second graded layer.
The orbit (4.1) is a finite \(\mathbf F_3\)-span at every registered finite
window.  Exact elimination gives either a coefficient preimage or a dual
annihilating the full span and not `q2`; a cap gives UNKNOWN.  Equation (4.3)
is v263 (4.10).  \(\square\)

A NONMEMBER result rejects only the named pointed cyclic completion
\((F,a,\mu,\operatorname{Mat})\).  It does not reject a larger actual class,
a different first correction, or witness existence.

## 5. Later-rung simplification

### Lemma 5.1 (NEW-CORRECTION QUADRATIC TERMS SKIP A LAYER)

Let \(r\ge2\) and apply one new correction \(c_r\in P_{(r)}\).  Modulo
\(\mathcal F^{r+2}\mathcal Z\), every term containing at least two
occurrences of \(c_r\) vanishes.

#### Proof

V263 Lemma 2.2 puts a term with two new occurrences in filtration at least
\(2r\).  For \(r\ge2\), \(2r\ge r+2\).  \(\square\)

Therefore the immediately following layer after a depth-\(r\) cancellation
has no term quadratic in the **new** correction.  It can still contain a
linear commutator of \(c_r\) with the already accumulated depth-one base and
the pre-existing higher residual tail.  Those terms remain the all-depth
return problem; Lemma 5.1 does not prove NLSAT.  It does show that the
exceptional self-quadratic compiler (2.2) is needed first at depth one, while
later one-layer returns can be organized as transported linear two-layer
operators rather than a fresh quadratic search at every rung.

## 6. Executable certificate contract

After actual A5/A6 ancestry and the A7/A8 endpoint package exist, the first
nonlinear checker should:

1. authenticate the exact ordered ancestry of \(a\);
2. construct only the registered class-two context quotients;
3. collect every substituted occurrence as \((\ell_i,\tau_i)\);
4. compute (2.2) in H1, H2, and printed A.18 order;
5. replay (2.2) independently from literal class-two words;
6. rebuild the complete diagonal orbit (4.1); and
7. emit MEMBER ancestry, a complete separating dual, or UNKNOWN.

No raw group-like test, unrelated PB boundary search, or deeper-rung
enumeration belongs in this first canary.

```text
PRINTED-ORDER CLASS-TWO FORMULA FOR q2:             PAPER PROOF
ONLY TWO ZASSENHAUS LAYERS NEEDED FOR q2:           PAPER PROOF
WORD-BEARING QUADRATIC ANCESTRY:                    PAPER CONSTRUCTION
DEPTH r>=2 NEW-NEW TERMS SKIP r+1:                  PAPER PROOF
ACTUAL A5/A6 WORD a:                                NOT COMPUTED
ACTUAL NUMERICAL q2:                                NOT COMPUTED
ACTUAL q2=nu2 beta MEMBER/NONMEMBER:                OPEN
ALL-DEPTH TRANSPORTED-LINEAR RETURN / NLSAT:        OPEN
COMPATIBLE LIFT / FAKE / IHARA:                     NOT ESTABLISHED
```

`R07_CLASS_TWO_QUADRATIC_REMAINDER_COMPILER_V266_PAPER_GRADE`
