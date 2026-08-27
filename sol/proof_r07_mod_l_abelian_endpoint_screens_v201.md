# R07 mod-l abelian endpoint screens v201

Author: Sol / 2026-08-28

Status: explicit finite-screen specialization of v200.  The mod-2 and mod-3
abelianizations of PB3/PB4 give two very small, independently runnable,
complete projected orbit selectors for the same-successor endpoint repair.
A screen NO is an exact PB obstruction; a screen YES remains only a seed for
the exact Artin/Garside replay.  The actual first multiplier and endpoint are
not yet available, so no numerical screen result, lift, fake certificate, or
Ihara witness is declared.

## 1. Canonical finite PB quotients

For a prime \(\ell\), let

\[
 A_{n,\ell}=H_1(PB_n,\mathbf Z/\ell)
 \cong (C_\ell)^{\binom n2}.
\tag{1.1}
\]

The standard pure generators \(A_{ij}\), \(1\le i<j\le n\), map to the
standard basis.  The quotient

\[
 \tau_{n,\ell}:PB_n\twoheadrightarrow A_{n,\ell}
\tag{1.2}
\]

is therefore authenticated by exponent-summing a retained pure-generator
word modulo \(\ell\).  It does not rely on a sampled permutation action or a
word hash.

Use separately tagged copies for the two hexagons and the pentagon:

\[
 E_\ell=
 \mathbf F_3[A_{3,\ell}]_{H1}
 \oplus
 \mathbf F_3[A_{3,\ell}]_{H2}
 \oplus
 \mathbf F_3[A_{4,\ell}]_P.
\tag{1.3}
\]

Its dimension is

\[
 \boxed{\dim_{\mathbf F_3}E_\ell=2\ell^3+\ell^6.}
\tag{1.4}
\]

The occurrence signs and prefixes are first evaluated in PB and then sent
through (1.2).  H1 and H2 remain distinct summands even though their quotient
groups are isomorphic.

## 2. The eleven-occurrence joint source image is tiny

For the eleven substitutions \(\rho_o:F(x,y)\to PB_{3/4}\), define

\[
 D_\ell=\operatorname{im}\!\left(
 F(x,y)\longrightarrow
 \prod_{o=1}^{11}A_{B(o),\ell}
 \right).
\tag{2.1}
\]

### Lemma 2.1 (TWO-GENERATOR ABELIAN ORBIT CAP)

\[
 \boxed{|D_\ell|\le \ell^2.}
\tag{2.2}
\]

More precisely, \(|D_\ell|\in\{1,\ell,\ell^2\}\).  If the two marked joint
exponent vectors have rank \(r_\ell\) over \(\mathbf F_\ell\), then
\(|D_\ell|=\ell^{r_\ell}\).

#### Proof

Every target factor in (2.1) is abelian of exponent \(\ell\).  Hence the
joint map factors through

\[
 F(x,y)\twoheadrightarrow
 H_1(F(x,y),\mathbf Z/\ell)\cong(C_\ell)^2.
\tag{2.3}
\]

Its image has dimension zero, one, or two over \(\mathbf F_\ell\), which
gives (2.2). \(\square\)

The exact rank must be recomputed from the task198 occurrence ledger.  It is
not inferred from the repeated label C21, and the E3 and E4 C21 coordinates
remain different coordinates of (2.1).

## 3. Complete two-sided work bounds

Let \(S=\{s_1,\ldots,s_t\}\) be a complete finite normal-relator roster for
the actual first successor, as in v195.  V200 Theorem 4.1 says that the whole
projected repair space is spanned by

\[
 \bar{\mathcal E}_{d,\ell}
 \bigl(A(s_i-1)B\bigr),
 \qquad
 \bar A,\bar B\in D_\ell,
 \quad 1\le i\le t.
\tag{3.1}
\]

### Theorem 3.1 (EXPLICIT MOD-l SCREEN BOUNDS)

The complete projected selector needs at most

\[
 \boxed{\ell^4t}
\tag{3.2}
\]

candidate columns in the vector space of dimension \(2\ell^3+\ell^6\).
It returns either a projected coefficient seed or a complete dual
obstruction.  A dual obstruction proves that no exact finite-support
representative of the named \(\mu_1\) has zero H1/H2/P endpoint.

#### Proof

There are at most \(|D_\ell|^2t\le\ell^4t\) triples in (3.1), by Lemma 2.1.
V200 Theorem 4.1 proves that they span the entire projected repair space, not
a word-radius prefix.  Gaussian elimination in (1.3) is finite.  V200
Theorem 5.1 pulls a projected nonmembership dual back to an exact PB dual.
\(\square\)

Repeated columns should be normalized and deduplicated before echelon
insertion, but the completion terminal binds the full roster cardinality and
the disposition of every triple in (3.1).

## 4. The two immediate screens

### 4.1 Modulo two

For \(\ell=2\),

\[
 |A_{3,2}|=8,
 \qquad
 |A_{4,2}|=64,
 \qquad
 \dim E_2=2\cdot8+64=80,
\tag{4.1}
\]

and

\[
 \boxed{|D_2|\le4,\qquad
        \#\text{two-sided columns}\le16t.}
\tag{4.2}
\]

Because the coefficient field is \(\mathbf F_3\), the order of every finite
group in this screen is coprime to the characteristic.  This may make the
screen sparse and well conditioned, but semisimplicity is not used in the
soundness proof.

### 4.2 Modulo three

For \(\ell=3\),

\[
 |A_{3,3}|=27,
 \qquad
 |A_{4,3}|=729,
 \qquad
 \dim E_3=2\cdot27+729=783,
\tag{4.3}
\]

and

\[
 \boxed{|D_3|\le9,\qquad
        \#\text{two-sided columns}\le81t.}
\tag{4.4}
\]

This screen retains characteristic-three augmentation depth that the mod-2
screen cannot see.  It is still a finite quotient screen: a projected zero
or projected membership is not an exact PB identity.

Running (4.2) and (4.4) separately is preferable to forming their direct
product.  Either independently authenticated NO is already terminal, while
the separate matrices have dimensions 80 and 783.

## 5. Exact column formula in exponent coordinates

Write an element of \(A_{n,\ell}\) additively as an exponent vector.  For a
literal occurrence \(o\), retain

\[
 p_o,\quad a_o(A),\quad a_o(s_i),\quad a_o(B),\quad x_o
 \in A_{B(o),\ell},
\tag{5.1}
\]

where \(p_o\) is the projected prefix and \(x_o\) ranges over the one or two
projected buckets in the fixed endpoint \(\xi_o\).  The projected group-ring
term contributed by \(A(s_i-1)B\) is obtained from

\[
 \sigma_o\,[p_o+a_o(A)]
 \bigl([a_o(s_i)]-[0]\bigr)
 [a_o(B)]\,\bar\xi_o.
\tag{5.2}
\]

All additions inside brackets are in the finite abelian group; coefficients
and signs are reduced in \(\mathbf F_3\).  Formula (5.2) is only the
abelian-screen image of v198's noncommutative factor order.  The producer
must derive it by applying \(\tau_{n,\ell}\) to the retained exact formula,
not by commuting factors before projection.

Each block is collected independently in its tagged array.  The two copies
of the repeated E3 substitution are evaluated at their two literal prefixes
before H1/H2 collection.

## 6. Production and independent-checker contract

Once task198 and v188/v191 provide the exact occurrence ledger, complete
first-successor normal relators, and \(M_0\):

1. compute the exact v198 endpoint first; skip the screens if it is zero;
2. independently exponent-sum every retained PB word modulo 2 and modulo 3;
3. compute the two marked joint ranks and enumerate exactly \(D_2,D_3\);
4. stream all \((\bar A,s_i,\bar B)\) triples, deduplicate exact array
   columns, and maintain a sparse echelon;
5. on nonmembership emit the full dual and pair it with the target and every
   registered column; and
6. on membership recover coefficients, choose retained source sections for
   \(\bar A,\bar B\), form a candidate repair, and replay it in exact PB
   normal form before drawing any positive conclusion.

The checker separately reconstructs pure-generator exponent vectors from
the Artin words, the two joint ranks, all normal relators, every endpoint
bucket, the complete orbit counts, echelon membership, and dual pairings.
It rejects a mutation of one occurrence type, duplicate E3 position, C21
type, prefix, sign, inverse slot, generator exponent, relator, orbit element,
coefficient, target bucket, or completion count.

The two screens are independent and naturally parallel.  Their execution is
deferred until the actual \(M_0\) and the complete first-successor relator
roster exist; running them on roof-only or guessed successor relations would
not decide (1.5).

~~~text
PB3/PB4 MOD-2 ABELIAN SCREEN:                    PAPER-SPECIFIED / NOT RUN
PB3/PB4 MOD-3 ABELIAN SCREEN:                    PAPER-SPECIFIED / NOT RUN
JOINT A-ORBIT CAPS 4 AND 9:                      PAPER_PROOF
ROW DIMENSIONS 80 AND 783:                       PAPER_PROOF
TWO-SIDED COLUMN CAPS 16t AND 81t:               PAPER_PROOF
SCREEN NO IMPLIES EXACT SAME-mu1 NO:             PAPER_PROOF VIA v200
SCREEN YES IMPLIES EXACT REPAIR:                 FALSE / FORBIDDEN
ACTUAL M0 / NORMAL RELATORS / SCREEN RESULT:     NOT AVAILABLE
COMPATIBLE RELATIVE PRO-3 LIFT:                  NOT CONSTRUCTED
FAKE / IHARA WITNESS:                            NOT DECLARED
~~~

R07_MOD_L_ABELIAN_ENDPOINT_SCREENS_V201_PAPER_GRADE
