# R07 relative defect one-cocycle and the correct full-pair degree v103

Author: Sol / 2026-08-26

Status: paper proof of an abstract composition-typed successor theorem and
its index-three/return consequences.  Applying it to R07 requires the actual
complete common-word residual quotient and its composition receipt at each
diagram-chief edge.  It does not construct the missing correction, a
compatible cofinal lift, or an Ihara witness.  `verified=false`.

## 1. Why an individual lift first gives a one-cocycle

Let \(P\) be a group of coarse relation-complete shadows at one fixed
matched diagram-chief edge.  Let

\[
 \pi:\mathcal E_{\rm raw}\twoheadrightarrow P
\tag{1.1}
\]

be a group of typed raw lifts, defined before the new fine relation values
are required to vanish.  Let \(C\) be its abelian common-word correction
kernel, let \(R_{\rm cl}\) be the actual closed residual module, and let

\[
 D:C\longrightarrow R_{\rm cl}
\tag{1.2}
\]

be the exact affine Jacobian of v99.  Put

\[
 M:=R_{\rm cl}/D(C).
\tag{1.3}
\]

The word ``actual'' in (1.2)--(1.3) includes the two hexagons, printed-order
A.18, all authenticated syzygies, the common-word/relative domain, and every
side condition which is linear at this edge.  An over-approximation is not
substituted for \(C\).

Say that the edge is `DEFECT-1-TYPED` if the normalized residual map

\[
 \Omega:\mathcal E_{\rm raw}\longrightarrow R_{\rm cl}
\tag{1.4}
\]

satisfies, for \(a,b\in\mathcal E_{\rm raw}\) and \(c\in C\),

\[
\begin{aligned}
 [\Omega(ac)]&=[\Omega(a)] &&\text{in }M,\\
 [\Omega(ab)]&=[\Omega(a)]+\pi(a)[\Omega(b)] &&\text{in }M,
\end{aligned}
\tag{1.5}
\]

and \(a\) has an admissible fine correction if and only if
\([\Omega(a)]=0\) in \(M\).  The \(P\)-action on \(M\) in (1.5) is the
coarse prefix action on the complete residual quotient.

The first line of (1.5) is exact affine correction invariance modulo the
actual image.  The second is the linearized closure of the complete GT/PaB
relation roster under the Ihara composition law.  It must be authenticated
on the complete roster; it is not a consequence of dimension agreement.

### Theorem 1.1 (RELATIVE DEFECT ONE-COCYCLE)

At a `DEFECT-1-TYPED` edge, the rule

\[
 o(p):=[\Omega(a)]\quad(\pi(a)=p)
\tag{1.6}
\]

is well-defined and is a crossed homomorphism

\[
 \boxed{o(pq)=o(p)+p\,o(q).}
\tag{1.7}
\]

Moreover, a fixed coarse point \(p\) has an admissible fine successor if
and only if

\[
 \boxed{o(p)=0.}
\tag{1.8}

#### Proof

Two raw lifts of \(p\) differ by a kernel correction.  The first identity
in (1.5) therefore makes (1.6) independent of the lift.  Choose raw lifts
\(a,b\) of \(p,q\).  Their product is a raw lift of \(pq\), and the second
identity in (1.5) gives (1.7).  The last clause of
`DEFECT-1-TYPED` gives (1.8). \(\square\)

Thus an individual successor problem is not initially an extension-splitting
problem in \(H^2(P,V)\).  Its normalized obstruction over all coarse points
is a specific element of \(Z^1(P,M)\), and the desired point is decided by
evaluation of that cocycle.

## 2. Pointwise arithmetic lifting is enough

Let \(H\lhd P\).  Assume that every \(h\in H\) has at least one admissible
fine arithmetic lift.  No homomorphic choice of those lifts is assumed.

### Corollary 2.1 (NO ARITHMETIC SECTION IS NEEDED)

Under the hypotheses of Theorem 1.1,

\[
 \boxed{o|_H=0.}
\tag{2.1}

#### Proof

For each \(h\), evaluate (1.6) on any admissible arithmetic lift.  Its
residual class is zero by (1.8), and (1.6) is independent of the chosen raw
lift. \(\square\)

This is strictly weaker than A2 of v101.  Pointwise arithmetic survival does
not generally split a group extension over \(H\), but it does null the
individual-lift obstruction cocycle on \(H\).

## 3. Exact index-three descent

Let \(H\lhd P\), let \(Q=P/H\), and let \(M^H\) be the \(H\)-fixed
submodule.  Denote by

\[
 Z^1(P,H;M)=\{z\in Z^1(P,M):z|_H=0\}.
\tag{3.1}
\]

### Theorem 3.1 (RELATIVE Z1 DESCENT)

Inflation gives a natural isomorphism

\[
 \boxed{Z^1(Q,M^H)\xrightarrow{\sim}Z^1(P,H;M).}
\tag{3.2}

This is an isomorphism of cocycle spaces, not merely of cohomology groups.

#### Proof

Let \(z\in Z^1(P,H;M)\), \(p\in P\), and \(h\in H\).  First

\[
 z(ph)=z(p)+p z(h)=z(p),
\tag{3.3}
\]

so \(z\) is constant on right \(H\)-cosets.  Since \(H\) is normal, write
\(hp=p(p^{-1}hp)\).  Then

\[
 h z(p)=z(hp)=z\bigl(p(p^{-1}hp)\bigr)=z(p).
\tag{3.4}
\]

Thus \(z(p)\in M^H\), and (3.3) makes \(z\) descend to \(Q\).  Equation
(1.7) descends with it.  Conversely, inflation of a cocycle on \(Q\) with
values in \(M^H\) is a cocycle on \(P\) vanishing on \(H\).  The two
constructions are inverse. \(\square\)

Now assume \(Q=\langle q\rangle\cong C_3\), and choose \(g\in P\) above
\(q\).  A cocycle on \(Q\) is determined by \(b=z(q)\), and the relation
\(q^3=1\) gives

\[
 (1+q+q^2)b=0.
\tag{3.5}

Conversely every vector satisfying (3.5) defines a unique cocycle.  Hence

\[
 \boxed{
 \operatorname{ev}_g Z^1(P,H;M)
 =\ker(1+q+q^2:M^H\to M^H).}
\tag{3.6}

In characteristic three, \(1+q+q^2=(q-1)^2\).

Equation (3.6) is the correct full-pair evaluation space for an individual
successor.  It is not the cyclic \(H^2(C_9,V)\) quotient

\[
 (\ker(g-1)\cap(g-1)^6V)/(g-1)^8V
\tag{3.7}

from v70--v83.  A separate actual chain comparison would be required to
relate (3.6) and (3.7).

## 4. Why vanishing of cohomology is still insufficient

The fixed pointed lift asks for \(o(g)=0\), not merely for the cohomology
class \([o]\) to vanish.  This distinction is load-bearing.

### Proposition 4.1 (H1-ZERO DOES NOT KILL EVALUATION)

There are \(C_3\)-modules \(M\) with

\[
 H^1(C_3,M)=0
\tag{4.1}

but with nonzero cocycles and nonzero values at the generator.

#### Proof

Take the free module \(M=\mathbf F_3[C_3]\).  It is projective, so (4.1)
holds.  For any \(a\in M\) not fixed by \(q\),

\[
 z(q)=(q-1)a\ne0
\tag{4.2}

defines the nonzero coboundary \(z(p)=pa-a\).  Thus \(Z^1(C_3,M)\ne0\)
although \(H^1(C_3,M)=0\). \(\square\)

A change by a coboundary is a change of global gauge.  It may be useful only
when that gauge is itself materialized by one allowed common-word correction
which preserves the fixed roof point and side gates.  It cannot be discarded
in the fixed fibre by a cohomology-dimension statement alone.

Consequently neither the repaired v4 full-pair \(H^2\)-restriction-zero
calculation nor a hypothetical vanishing of relative \(H^1\) proves the
explicit R07 successor without the actual evaluation/materialization map.

## 5. Return and the surviving even lane

Let \(\mathfrak R:P\to P\) be the return anti-involution

\[
 \mathfrak R(p)=c_\infty p^{-1}c_\infty^{-1},
\tag{5.1}

and let \(S\) be the registered involution on the complete residual quotient
\(M\), including the relator-order reversal.  Suppose the actual composition
receipt also gives

\[
 o(\mathfrak R(p))=S o(p).
\tag{5.2}

For R07, v77 proves \(\mathfrak R(g)=g\).  Therefore

\[
 \boxed{o(g)\in M^S.}
\tag{5.3}

Combining (2.1), (3.5), and (5.3) gives the exact location

\[
 \boxed{
 o(g)\in
 M^H\cap\ker(1+q+q^2)\cap M^S.}
\tag{5.4}

V77's midpoint formula kills the \((-1)\)-part of the joint residual.  It
does not kill (5.4), which is precisely the return-even lane.  Thus return
symmetry and relative full-pair descent fit together without implying a
false automatic vanishing theorem.

### Corollary 5.1 (UNIFORM RELATIVE-DIHEDRAL SUFFICIENT CONDITION)

At a `DEFECT-1-TYPED` edge, if

\[
 M^H\cap\ker(1+q+q^2)\cap M^S=0,
\tag{5.5}

then every return-fixed coarse point outside \(H\), in particular the
selected R07 point, has zero normalized relation obstruction.  The actual
preimage supplied by (1.8), followed by v98, materializes a compatible
ordinary commutator-word correction.

#### Proof

Equation (5.4) and (5.5) give \(o(g)=0\).  Apply Theorem 1.1 and the actual
materialization clause of `DEFECT-1-TYPED`; v98 removes compatibility of word
spellings as a separate issue. \(\square\)

Condition (5.5) is sufficient, not necessary.  If the intersection is
nonzero, the class-specific route is to compute the actual vector \(o(g)\)
and prove that it is zero; the dimension of the ambient intersection alone
does not decide the branch.

## 6. A finite presentation receipt is enough

Let

\[
 P=\langle x_1,\ldots,x_d\mid r_1,\ldots,r_e\rangle
\tag{6.1}
\]

be a fixed presentation and let \(M\) be a displayed \(P\)-module.  Given
vectors \(b_i\in M\), there is a unique derivation on the free group with

\[
 z(x_i)=b_i.
\tag{6.2}
\]

Its value on a signed word is the exact Fox formula

\[
 z(w)=\sum_i
 \left(\frac{\partial w}{\partial x_i}\right)_{P}b_i.
\tag{6.3}

### Proposition 6.1 (GENERATOR-RELATOR Z1 RECEIPT)

The derivation (6.2) descends to \(P\) if and only if

\[
 z(r_j)=0\qquad(1\leq j\leq e).
\tag{6.4}

If \(H\) is generated by displayed words \(h_1,\ldots,h_t\), then the
descended cocycle lies in \(Z^1(P,H;M)\) if and only if

\[
 z(h_k)=0\qquad(1\leq k\leq t).
\tag{6.5}

#### Proof

Equation (6.3) is the crossed-homomorphism product rule, so it gives the
unique cocycle on the free group with (6.2).  It factors through the
presented quotient exactly when it kills the normal closure of the relators.
Killing every \(r_j\) is sufficient because a cocycle which kills a word
also kills all its conjugates once that word represents the identity in the
coarse action, and it kills products of such words.  The same product rule
shows that vanishing on generators of \(H\) is equivalent to vanishing on
all of \(H\). \(\square\)

Thus the actual full-pair receipt need not contain a \(|P|^2\) cocycle table.
For the frozen roof group it is enough to serialize:

1. the three pinned \(P_0\) generator actions on the actual quotient \(M\);
2. the actual residual classes \(b_i\) of raw lifts of those generators;
3. all presentation-relator replays (6.4);
4. an arithmetic generating roster for \(H\) and the null replays (6.5);
5. the exact row36 word and its Fox evaluation (6.3);
6. the return action and equality (5.2).

This is the smallest non-circular finite target for the corrected full-pair
route.  It binds the actual PaB residual quotient directly and never equates
the roof \(C_9\) power with the five-coface rho word.

## 7. Inverse-limit form

For a nested matched diagram-chief ladder, word evaluation and Ihara
composition commute with refinement.  Hence authenticated
`DEFECT-1-TYPED` records give compatible maps

\[
 M_{n+1}\longrightarrow M_n,
 \qquad o_{n+1}\longmapsto o_n.
\tag{7.1}

The backtracking-free all-abelian theorem now has the following precise
form.

1. At every active edge, construct the actual quotient \(M_n\) and the
   composition/return receipt (1.5), (5.2).
2. Prove (5.5), or prove directly that the particular
   \(o_n(g_n)\) is zero.
3. Materialize one actual correction value.  V98 chooses an ordinary word in
   the accumulated kernel and the infinite product converges.

One does not need a homomorphic arithmetic section, compatible word
spellings, or a full \(P\times P\) two-cocycle table.  One still needs the
actual correction image and the actual residual quotient at every edge.
Nonabelian accepted-set nonemptiness remains separate.

## 8. Fixed ledger

```text
RELATIVE DEFECT Z1 THEOREM:                    PAPER_PROOF
POINTWISE ARITHMETIC H NULLING:                PAPER_PROOF
INDEX-THREE Z1 DESCENT / EVALUATION:           PAPER_PROOF
H1-ZERO INSUFFICIENCY:                         PAPER_PROOF
RETURN-EVEN LOCATION (UNDER TYPING):           PAPER_PROOF
GENERATOR-RELATOR Z1 RECEIPT:                  PAPER_PROOF
ACTUAL DEFECT-1-TYPED R07 OCCURRENCE:          OPEN
ACTUAL COMPLETE RESIDUAL QUOTIENT M_n:         OPEN
UNIFORM INTERSECTION VANISHING (5.5):          OPEN
CLASS-SPECIFIC ACTUAL o_n(g_n)=0:              OPEN
NONABELIAN ACCEPTED-SET NONEMPTINESS:          OPEN
COMPATIBLE COFINAL R07 LIFT:                   NOT CONSTRUCTED
FAKE CERTIFICATE / IHARA WITNESS:              NOT DECLARED
```

No finite computation, external source, or Lean proof is used in this note.
