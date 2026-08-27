# R07 cyclic saturation and cofinal Hensel selector v129

Author: Sol / 2026-08-27

Status: paper theorem.  It identifies the fixed-context saturation gate of
v128 and the context-changing transverse gate of v126 as the same intrinsic
kernel, gives the exact augmented one-class solve, and proves that successive
solutions along one fixed cofinal ladder are automatically compatible.  The
R07 augmented systems have not yet been computed.  No cofinal lift, fake, or
Ihara witness is declared.

## 1. One saturation kernel

Let \(\Lambda\) be a ring, let \(J\) be a two-sided nilpotent ideal, and let

\[
 B:A\longrightarrow Z
\tag{1.1}
\]

be a homomorphism of left \(\Lambda\)-modules.  Fix \(z\in Z\) and put

\[
 M_z=B(A)+\Lambda z\subseteq Z.
\tag{1.2}
\]

The inclusion \(M_z\subseteq Z\) induces

\[
 \iota_J:M_z/JM_z\longrightarrow Z/JZ.
\tag{1.3}
\]

Its kernel is exactly

\[
 \boxed{
 \ker\iota_J=\frac{M_z\cap JZ}{JM_z}.}
\tag{1.4}
\]

Moreover, linearity of \(B\) and two-sidedness of \(J\) give

\[
 \boxed{JM_z=B(JA)+Jz.}
\tag{1.5}
\]

Thus the ambient-to-intrinsic gap in v128 is not a second orbit problem.  It
is the kernel of the single map (1.3).  We call (1.4) the **cyclic saturation
kernel** of \((B,z)\) at \(J\).

### Lemma 1.1 (strictness criterion)

The following are equivalent:

1. \(\iota_J\) is injective;
2. \(M_z\cap JZ=JM_z\);
3. every \(e\in M_z\cap JZ\) admits coordinates

   \[
   e=Bd+\rho z,
   \qquad d\in JA,\quad \rho\in J.
   \tag{1.6}
   \]

#### Proof

Formula (1.4) proves the equivalence of 1 and 2, and (1.5) proves the
equivalence of 2 and 3. \(\square\)

Full injectivity is stronger than the R07 actual-class requirement.  For one
specified error \(e\), it is enough that the class of \(e\) in (1.4) vanish.
This distinction prevents an unnecessary classification of the whole
ambient field-outer module.

## 2. The augmented actual-class solve

Suppose \(J^L=0\).  Let \(a_0\in A\) satisfy

\[
 e:=Ba_0-z\in JZ.
\tag{2.1}
\]

Since \(e\in M_z\) automatically, (2.1) places \(e\) in the numerator of
(1.4).  Its saturation class vanishes precisely when the single augmented
system

\[
 \boxed{
 [\,B|_{JA}\ \ L_z\,](d,\rho)=e,
 \qquad L_z(\rho)=\rho z}
\tag{2.2}
\]

has a solution \((d,\rho)\in JA\oplus J\).

### Theorem 2.1 (CYCLIC SATURATION HENSEL)

If (2.2) has a solution, then

\[
 \boxed{
 a=(1+\rho)^{-1}(a_0-d)
   =\left(\sum_{m=0}^{L-1}(-\rho)^m\right)(a_0-d)}
\tag{2.3}
\]

satisfies \(Ba=z\).  If \(\iota_J\) is injective, every \(a_0\) satisfying
(2.1) has such an exact correction.

#### Proof

Equation (2.2) says

\[
 Ba_0-z=Bd+\rho z,
\]

and hence

\[
 B(a_0-d)=(1+\rho)z.
\tag{2.4}
\]

Nilpotence gives the two-sided finite inverse displayed in (2.3).  Applying
\(B\) to (2.3) and using (2.4) gives \(Ba=z\).  The last assertion follows
from Lemma 1.1. \(\square\)

The certificate for (2.2) consists only of \((a_0,d,\rho)\) and a direct
replay of the displayed equality.  A full right inverse on \(M_z\), an
annihilator-compatible splitter on \(\Lambda z\), and a generator-sized
error matrix are not prerequisites.

## 3. Fixed Jennings depth nine

Take

\[
 \Lambda=\mathbf F_3[\Pi_4[3]],
 \qquad I^{29}=0,
 \qquad J=I^9.
\tag{3.1}
\]

Then \(J^4=I^{36}=0\), so (2.3) becomes

\[
 \boxed{
 a=(1-\rho+\rho^2-\rho^3)(a_0-d).}
\tag{3.2}
\]

For the frozen convention \(z=-\beta\), \(B=D\), the exact positive
certificate after the all-seven raw bridge is therefore

\[
 Da_0-z=Dd+\rho z,
 \qquad d\in I^9A,quad \rho\in I^9.
\tag{3.3}
\]

An ambient leading solve provides \(Da_0-z\in I^9Z\).  The only remaining
fixed-context membership question is whether its class in

\[
 \boxed{
 \ker\bigl(M_z/I^9M_z\longrightarrow Z/I^9Z\bigr)}
\tag{3.4}
\]

vanishes.  This is exactly v128's intrinsic saturation gate, now presented
as one augmented linear system.  Once (3.3) is returned, no separate depth
10, 11, or 12 search is needed in this fixed ring.

## 4. A context-changing edge is the same problem

Let

\[
 \pi:\Lambda'\twoheadrightarrow\Lambda,
 \qquad J=\ker\pi,
 \qquad J^L=0
\tag{4.1}
\]

and suppose compatible reductions give

\[
 A'\twoheadrightarrow A,
 \qquad Z'\twoheadrightarrow Z,
 \qquad B':A'\to Z',
 \qquad z'\mapsto z.
\tag{4.2}
\]

Assume

\[
 \ker(Z'\to Z)=JZ'.
\tag{4.3}
\]

Put \(M_{z'}=B'(A')+\Lambda'z'\).  Given a coarse solution \(Ba=z\), choose
any lift \(\widehat a\in A'\) and set

\[
 e=B'\widehat a-z'.
\tag{4.4}
\]

Then

\[
 e\in M_{z'}\cap JZ'.
\tag{4.5}
\]

Consequently the transverse actual-class obstruction at this edge is the
class

\[
 \boxed{
 [e]\in
 \ker\bigl(M_{z'}/JM_{z'}\longrightarrow Z'/JZ'\bigr).}
\tag{4.6}
\]

This is the cyclic specialization of the quotient in v126.  If (4.6)
vanishes, solve

\[
 e=B'd+\rho z',
 \qquad d\in JA',\quad\rho\in J,
\tag{4.7}
\]

and set

\[
 \boxed{
 a'=(1+\rho)^{-1}(\widehat a-d).}
\tag{4.8}
\]

Then \(B'a'=z'\), and \(a'\) reduces to \(a\).  In the more general v126
setting with \(K_A=\ker(A'\to A)\) and
\(K_Z=\ker(Z'\to Z)\), the numerator and denominator are respectively

\[
 M_{z'}\cap K_Z,
 \qquad B'(K_A)+Jz'.
\tag{4.9}
\]

Thus the full ambient equality
\(K_Z=B'(K_A)+Jz'\) is unnecessary.  Only the actual error class in the
intrinsic quotient (4.9) must vanish.

### Corollary 4.1 (intrinsic cartesian edge)

If

\[
 M_{z'}\cap JZ'=JM_{z'},
\tag{4.10}
\]

then every coarse solution lifts through this edge by (4.8).  Equivalently,
it is enough that the degree-zero map

\[
 M_{z'}/JM_{z'}\longrightarrow Z'/JZ'
\tag{4.11}
\]

be injective.

This is the useful relative-dihedral generalization: the dihedral
antisymmetrizer may prove (4.7) on the return-odd part, while a separate
field-outer homotopy proves it on the actual return-even class.  Neither
piece has to split the whole ambient target.

## 5. Successive lifting on one cofinal ladder

Let

\[
 \cdots\twoheadrightarrow\Lambda_{n+1}
 \twoheadrightarrow\Lambda_n\twoheadrightarrow\cdots
\tag{5.1}
\]

be a fixed cofinal sequence, with compatible modules, maps \(B_n\), and
targets \(z_n\).  Write \(J_n=\ker(\Lambda_{n+1}\to\Lambda_n)\), and assume
each \(J_n\) is nilpotent.  Suppose \(a_0\) satisfies \(B_0a_0=z_0\).

### Theorem 5.1 (COFINAL CYCLIC HENSEL SELECTOR)

Assume that at every edge, for the error made by lifting the already chosen
\(a_n\), the class (4.6), or its general form (4.9), vanishes.  Choose and
retain one word-bearing solution \((d_n,\rho_n)\) of (4.7), and define

\[
 a_{n+1}=(1+\rho_n)^{-1}(\widehat a_n-d_n).
\tag{5.2}
\]

Then

\[
 B_na_n=z_n,
 \qquad a_{n+1}\longmapsto a_n
\tag{5.3}
\]

for every \(n\).  Hence \((a_n)\) is a compatible family.  If the systems
are complete and separated, it defines a continuous inverse-limit solution
\(a_\infty\) with \(B_\infty a_\infty=z_\infty\).

If every edge is intrinsically cartesian as in (4.10), the lifting step can
never fail.  A deterministic finite solver for (4.7), together with a
deterministic word lift \(\widehat a_n\), is then a uniform explicit
selector on the chosen cofinal ladder.

#### Proof

Theorem 2.1 applied at edge \(n\) gives the first equality in (5.3), while
\(d_n\) and \(\rho_n\) reduce to zero and therefore give the second.  The
claim follows by induction.  The inverse-limit assertion is coordinatewise
and uses completeness and separatedness. \(\square\)

For one chosen cofinal sequence, no extra compatibility problem remains
after (5.2): each new solution is constructed as a lift of the preceding
one.  Naturality of independently defined selectors, as in v127, is needed
only if one wants a path-independent formula over several refinement routes
or constructs all levels separately.  It is not an additional obstruction
for the sequential cofinal construction used here.

## 6. Exact R07 work order

The shortest remaining explicit-witness route is now:

1. task175 authenticates the one common all-seven column module and all
   eleven literal occurrence slots;
2. solve the leading all-seven equation only modulo \(I^9Z\), retaining the
   actual word-bearing \(a_0\);
3. solve the single augmented saturation system (3.3), retaining
   \((d,\rho)\);
4. materialize (3.2) and replay the same correction word in H1, H2, and the
   printed-order pentagon;
5. at each later abelian refinement solve only the actual cyclic system
   (4.7), split into dihedral-odd and field-outer-even blocks when useful;
6. at a nonabelian chief edge retain the finite accepted-set witness and use
   it as the next based lift; and
7. iterate (5.2) along the preregistered cofinal ladder.

If this produces a compatible family above a finite shadow already proved
nonarithmetic, then the nonarithmetic projection persists and supplies the
required profinite fake candidate.  The present theorem proves the lifting
logic; it does not establish the missing all-seven solve, the saturation
equalities, the nonabelian accepted-set nonemptiness, or the final Ihara
identification.

```text
CYCLIC SATURATION KERNEL IDENTITY:           PAPER_PROOF
ONE AUGMENTED ACTUAL-CLASS SOLVE SUFFICES:   PAPER_PROOF
FIXED DEPTH-9 FOUR-TERM CORRECTION:          PAPER_PROOF (v128--v129)
CONTEXT TRANSVERSE GATE = SAME KERNEL:       PAPER_PROOF
SEQUENTIAL COFINAL LIFTS ARE COMPATIBLE:     PAPER_PROOF
TASK175 ALL-SEVEN RAW BRIDGE:                PENDING
R07 LEADING ALL-SEVEN SOLVE:                 NOT COMPUTED
R07 AUGMENTED (d,rho) SATURATION SOLVE:      NOT COMPUTED
R07 INTRINSIC CARTESIAN EDGES:               NOT PROVED
NONABELIAN ACCEPTED SETS:                    OPEN
COMPATIBLE COFINAL R07 LIFT:                 NOT CONSTRUCTED
FAKE / IHARA WITNESS:                        NOT DECLARED
```
