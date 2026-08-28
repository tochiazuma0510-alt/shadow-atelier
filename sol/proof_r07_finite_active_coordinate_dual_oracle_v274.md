# R07 finite active-coordinate dual oracle v274

Author: Sol / 2026-08-29

Status: feasibility lemma for the exact lazy full-boundary algorithm v272 and
the discrepancy refinement v273.  It proves that neither construction of the
separating dual nor its complete translated-boundary test requires allocation
of the full E3/E4 group-algebra coordinate universe.  No actual A4 terminal or
witness is declared.  `verified=false`.

## 1. Finite-support ambient module

Let \(k=\mathbf F_3\) and let

\[
 V=k^{(\Omega)}
\tag{1.1}
\]

be the finite-support vector space on the typed coordinate set \(\Omega\).
For A4, a coordinate is the complete tuple `(context, component, group
element)`.  The underlying marked E4 factor may be enormous; this does not
change the fact that every Fox row used by the algorithm has finite support.

Let \(U=\langle u_1,\ldots,u_m\rangle\) be the current discovered `B+K`
space and let \(v\) be one target.  Define the active coordinate set

\[
 S=\operatorname{supp}(v)\cup
   \bigcup_{a=1}^{m}\operatorname{supp}(u_a).
\tag{1.2}
\]

Then \(S\) is finite and every vector in \(U+kv\) belongs to the embedded
finite space \(k^S\).

### Lemma 1.1 (ACTIVE-COORDINATE MEMBERSHIP)

\[
 v\in U\text{ in }V
 \quad\Longleftrightarrow\quad
 v\in\langle u_1,\ldots,u_m\rangle\text{ in }k^S.
\tag{1.3}
\]

If \(v\notin U\), there is a functional \(\lambda\in V^*\), supported on
\(S\), such that

\[
 \lambda(U)=0,
 \qquad \lambda(v)\ne0.
\tag{1.4}
\]

#### Proof

The inclusion \(k^S\hookrightarrow V\) is injective, so a coefficient
identity among vectors supported in \(S\) is the same identity in either
space.  This proves (1.3).  If the membership fails, finite-dimensional
linear algebra in \(k^S\) separates the class of \(v\) from \(U\).  Extend
the resulting functional by zero on \(\Omega\setminus S\); (1.4) is
unchanged. \(\square\)

Thus a sparse echelon may discover coordinate keys on demand.  It never needs
the order of E3/E4, a group-element roster, or a dense vector whose length is
the ambient group order.

## 2. Constructive dual from a reduction projection

Fix a deterministic sparse row-reduction map

\[
 N_U:k^S\longrightarrow k^S
\tag{2.1}
\]

which subtracts the ordered normalized pivot rows and satisfies

\[
 \ker N_U=U,
 \qquad N_U^2=N_U.
\tag{2.2}
\]

If \(r=N_U(v)\ne0\), choose the registered leading nonzero coordinate
\(p\in S\) and put

\[
 \lambda(w)=[N_U(w)]_p.
\tag{2.3}
\]

Then \(\lambda\) satisfies (1.4).  Its coefficient row is obtained by the
same finite back-substitution that formed \(N_U\), or independently by a
nullspace solve on the \(m\)-by-\(|S|\) active matrix.  Producer and checker
may use these two different constructions.

Equation (2.3) is important operationally: choosing the `p`-th raw coordinate
of \(w\) without applying \(N_U\) need not annihilate U.  An artificial target
coordinate is also unnecessary and invalid.

## 3. Complete full-D test still uses only active support

Let the 65 tagged base boundary rows be

\[
 d_{i,j}=\sum_{c,h}a_{i,j,c,h}[i,c,h].
\tag{3.1}
\]

For a dual from Lemma 1.1, write its finite support as

\[
 \lambda=\sum_{i,c,g}\lambda_{i,c,g}[i,c,g]^*.
\tag{3.2}
\]

The pairing with a full translated column is

\[
 \langle\lambda,t d_{i,j}\rangle
 =\sum_{c,h}a_{i,j,c,h}\lambda_{i,c,th}.
\tag{3.3}
\]

Every nonzero summand in (3.3) has \(g=th\) in the already known support
(3.2), hence \(t=gh^{-1}\).  Therefore v272's support-inversion correlation
over matching pairs of (3.1) and (3.2) is not a heuristic restriction to S:
it computes the pairing with **every** translation in the full marked group.
Translations with no matching active coordinate pair automatically have zero
pairing because the extended functional is zero outside S.

### Theorem 3.1 (ON-DEMAND COMPLETE FULL-BOUNDARY ORACLE)

The v272 lazy query can be implemented using only:

1. the current finite supports of B, K, and the target;
2. a finite dual supported on their union;
3. the finite occurrence indexes of the 65 base rows; and
4. multiplication/inversion for only the group elements occurring in the
   support-inversion pairs.

It returns the same MEMBER/NONMEMBER result as a dense calculation in the
complete ambient module \(V/D\).

#### Proof

Lemma 1.1 makes reduction and dual separation exact in the full V.  Equation
(3.3) and support inversion test the dual on all generators of D.  A nonzero
pairing yields one actual full-D column outside the current B+K span; a zero
correlation proves annihilation of all D.  These are precisely the two steps
of v272 Theorem 2.1. \(\square\)

When an active translated column is added, its finite support may contain new
coordinates outside S.  Add those keys to the active registry and recompute
the next reduction/dual there.  No correctness claim requires S to have been
fixed in advance.

## 4. Honest finite work bounds

Let \(s_q\) be the number of active coordinates in one query round, \(m_q\)
the live B+K rank, and \(\ell_q=|\operatorname{supp}\lambda_q|\).  Let
\(o_{i,c}\) be the number of occurrences with tag/component `(i,c)` among
the 65 base rows.  Then:

- the dense comparison bound for one dual solve is polynomial in
  \((m_q,s_q)\), for example \(O(m_q^2s_q)\) field operations under ordinary
  elimination;
- a sparse implementation charges its actual pivot/support operations;
- the exact boundary correlation work is

  \[
  P_q=\sum_{(i,c,g)\in\operatorname{supp}\lambda_q}o_{i,c};
  \tag{4.1}
  \]

- one active round adds at most the support size of one translated base row
  to the registry; and
- there are exactly p active-boundary rank raises globally and at most one
  zero-correlation round per quotient query, as in v272.

No factor \(|E_i|\) occurs in (4.1).  This is a correctness-preserving removal
of ambient enumeration, not an assertion that \(s_q\), \(m_q\), or p will be
small on the actual data.  If their measured values exceed a registered cap,
the only honest terminal is `UNKNOWN_RESOURCE`.

## 5. Certificate and mutation boundary

A positive query record must bind the active-key registry, live basis rows,
remainder, chosen pivot, dual coefficients, all-row annihilation, target
pairing, base-occurrence index digest, correlation pair count, and either the
selected translated column or complete zero accumulator.  The independent
checker reconstructs S from literal supports; it does not trust a declared
ambient dimension or `finite_support=true` Boolean.

Required negative controls include deleting an active coordinate, adding a
nonzero dual coefficient outside the registered support without updating the
registry, using the raw pivot coordinate instead of (2.3), omitting a matching
base occurrence, accepting a translation absent from the complete key, and
declaring zero correlation before all \(P_q\) pairs are processed.

## 6. Fixed frontier

```text
FINITE ACTIVE-COORDINATE REDUCTION:            PAPER PROOF
FINITE-SUPPORT SEPARATING DUAL:                PAPER PROOF
SUPPORT-INVERSION TEST OF ALL FULL-D COLUMNS:  PAPER PROOF / v272+v274
FULL E3/E4 ENUMERATION FOR A4:                  PROVED UNNECESSARY
ACTUAL ACTIVE SIZES / RANKS / RESOURCE FIT:     NOT COMPUTED
ACTUAL A4 / LIFT / FAKE / IHARA:               NONE
```

`R07_FINITE_ACTIVE_COORDINATE_DUAL_ORACLE_V274_PAPER_GRADE`
