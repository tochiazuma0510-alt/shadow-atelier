# Frattini-invisible stability of the R07 onto gate v94

Author: Sol / 2026-08-26

Status: paper proof.  Section 3 proves the required Frattini typing on the
cofinal marked \(3\)-group refinement category above \(\Pi_4[3]\).
Other primes, mixed nonnilpotent refinements, and nonabelian chief factors
remain outside this theorem.  verified=false; no cofinal lift or Ihara
witness is declared.

## 1. One finite direct-product gate

Let \(Q\) be finite, let \(P\) be a finite \(p\)-group, and assume

\[
p\nmid |Q^{\rm ab}|.
\tag{1.1}
\]

For a tuple

\[
s=(s_1,\ldots,s_d)\in(Q\times P)^d,
\tag{1.2}
\]

write \(s_Q\) and \(s_P\) for its coordinate projections.

### Theorem 1.1 (ONTO-FRATTINI-GOURSAT)

If

\[
\langle s_Q\rangle=Q,\qquad
\langle \bar s_P\rangle=P/\Phi(P),
\tag{1.3}
\]

then

\[
\boxed{\langle s_1,\ldots,s_d\rangle=Q\times P.}
\tag{1.4}
\]

Moreover (1.4) remains true after replacing \(s_i\) by any \(t_i\) having
the same \(Q\)-coordinate and the same image in \(P/\Phi(P)\).

#### Proof

Burnside's basis theorem turns the second condition in (1.3) into
\(\langle s_P\rangle=P\).  Hence \(H=\langle s\rangle\) is a subdirect
product of \(Q\times P\).  If \(H\) is proper, Goursat's lemma supplies
a nontrivial common quotient of \(Q\) and \(P\).  It is a nontrivial
\(p\)-group, hence has a quotient \(C_p\).  This would give a \(C_p\)
quotient of \(Q^{\rm ab}\), contradicting (1.1).  This proves (1.4).
The two hypotheses (1.3) are unchanged by the stated replacement, proving
the last assertion. \(\square\)

Thus a transition-kernel correction which is invisible in \(Q\) and modulo
\(\Phi(P)\) cannot destroy onto.  No GT-shaped inverse word is needed.

## 2. Propagation through a Frattini tower

Let

\[
P_{n+1}\twoheadrightarrow P_n
\tag{2.1}
\]

be an epimorphism of finite \(p\)-groups with kernel contained in
\(\Phi(P_{n+1})\).  Then the induced map

\[
P_{n+1}/\Phi(P_{n+1})
 \xrightarrow{\sim}
P_n/\Phi(P_n)
\tag{2.2}
\]

is an isomorphism.  Indeed, a subset of \(P_{n+1}\) generates if and only
if its image generates \(P_n\): failure upstairs lies in a maximal subgroup,
while every maximal subgroup contains \(\Phi(P_{n+1})\) and therefore the
kernel; conversely generation upstairs plainly implies generation downstairs.
Burnside's basis theorem gives (2.2).

### Theorem 2.1 (ONTO-STABILITY-THROUGH-FRATTINI-COVERS)

Fix \(Q\) satisfying (1.1), and let \(P_n\) be an inverse tower whose every
transition has kernel in the finer Frattini subgroup.  Suppose a tuple at
level zero generates \(Q\times P_0\).  Then every compatible tuple of lifts
at every level \(n\) generates \(Q\times P_n\).

#### Proof

The \(Q\)-projection is unchanged.  Iterating (2.2), the images of any lifted
\(P_n\)-tuple span \(P_n/\Phi(P_n)\) because their level-zero images do.
Apply Theorem 1.1 at every level. \(\square\)

This is stronger than checking onto after each correction: on a genuine
Frattini tower it is a property of the coarse source tuple and the type of
the transition maps.

## 3. R07 use and exact boundary

At the frozen \(p=3\) E4 target,

\[
E_4=Q_4\times\Pi_4[3],\qquad |Q_4^{\rm ab}|=32.
\tag{3.1}
\]

The 616-letter source tuple has an explicit two-sided E4 inverse, and the
760-letter commutator rebase has the same six E4 source values.  Therefore
the 760 tuple generates \(E_4\) at the current level.  Since
\(3\nmid32\), there is no nontrivial common quotient of \(Q_4\) and a finite
\(3\)-group.

Put \(P_0=\Pi_4[3]\).  The authenticated marked presentation has six standard
PB4 generators and

\[
P_0/\Phi(P_0)\simeq\mathbf F_3^6.
\tag{3.2}
\]

### Theorem 3.1 (COFINAL-3-FRATTINI-TYPING)

Let \(P\) be any finite marked \(3\)-group quotient of PB4 which maps onto
\(P_0\).  Then

\[
\ker(P\twoheadrightarrow P_0)\leq\Phi(P).
\tag{3.3}
\]

More generally, every transition \(P'\twoheadrightarrow P\) between two such
quotients satisfies

\[
\ker(P'\twoheadrightarrow P)\leq\Phi(P').
\tag{3.4}
\]

The category of finite marked \(3\)-group quotients mapping onto \(P_0\) is
cofinal among all finite marked \(3\)-group quotients of PB4.

#### Proof

The six standard PB4 generators generate \(P\), so

\[
\dim_{\mathbf F_3}P/\Phi(P)\leq6.
\]

The surjection to \(P_0\) induces a surjection on Frattini quotients.  By
(3.2), its target has dimension six.  Hence the source also has dimension
six and the induced map is an isomorphism.  Its kernel is
\(\ker(P\to P_0)\Phi(P)/\Phi(P)\), proving (3.3).

Apply the same dimension argument to \(P'\twoheadrightarrow P\): both
Frattini quotients have dimension six, so their induced map is an
isomorphism and (3.4) follows.

For cofinality, given any finite marked \(3\)-group quotient \(R\) of PB4,
take the quotient by the intersection of the kernels defining \(R\) and
\(P_0\).  It is still a finite \(3\)-group quotient and maps onto both
\(R\) and \(P_0\). \(\square\)

For every \(P\) in Theorem 3.1, the matched quotient obtained by intersecting
the \(Q_4\)-kernel and the \(P\)-kernel is

\[
E(P)=Q_4\times P.
\tag{3.5}
\]

Indeed its image is the corresponding fibre product; a proper fibre product
would give a nontrivial common quotient of \(Q_4\) and \(P\), necessarily a
nontrivial \(3\)-group quotient of \(Q_4\), contradicting
\(3\nmid|Q_4^{\rm ab}|\).

Theorems 2.1 and 3.1 now give

\[
\boxed{\text{the 760 source tuple is onto at every compatible finite
marked \(3\)-group refinement above \(P_0\).}}
\tag{3.6}
\]

Thus no per-stage onto replay is needed on this cofinal \(3\)-primary
subcategory.

The same argument applies prime by prime with the corresponding
\(p\nmid|Q^{\rm ab}|\) gate.  It does not cover a transition which introduces
a new non-\(p\) coarse factor, a non-Frattini \(p\)-extension, or a nonabelian
chief factor changing \(Q\); those steps retain their own onto check.

Combined with the explicit raw commutator rebase, this removes two recurring
parts of HT4 on the cofinal \(3\)-primary lane:

    RAW CHARMING AT THE 760 BASE:                 EXPLICIT WORD CANDIDATE
    CHARMING UNDER COMMUTATOR CORRECTIONS:         PAPER CONSEQUENCE
    CURRENT E4 ONTO:                              CROSS_CHECKED
    COFINAL 3-FRATTINI TYPING:                     PAPER_PROOF
    ONTO THROUGH COFINAL 3-GROUP REFINEMENTS:      PAPER_PROOF
    LITERAL A18 CORRECTION / ACTUAL BETA:          OPEN
    NON-FRATTINI AND NONABELIAN ONTO GATES:         OPEN
    COFINAL COMPATIBLE LIFT:                       NOT YET CONSTRUCTED
    IHARA WITNESS:                                 NOT DECLARED
