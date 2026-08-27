# R07 universal word-polynomial multiplier promotion v175

Author: Sol / 2026-08-28

Status: paper theorem and post-task193 certificate contract.  It gives a
sound way to promote a finite second-rung multiplier discovered from the
actual class to one multiplier on every matched relative pro-3 quotient.
No such multiplier or universal boundary certificate has yet been found.
No compatible R07 lift, fake certificate, or Ihara witness is declared.

## 1. Why a finite multiplier is only a hint

Use the diagonal seven-context action of v173.  Let \(\Gamma\) be the image
of the common source group \(F_2\) in the product of the fixed presented
arity-three/four context groups before a finite relative quotient is chosen.
On the registered tower every finite context group is a quotient of its
fixed presented context group.  Consequently the common word maps give
compatible homomorphisms

\[
 \mathbf F_3[\Gamma]\longrightarrow
  \Lambda_n=\mathbf F_3[\Delta_n].
\tag{1.1}
\]

They also give a homomorphism \(\Gamma\to\Delta_\infty\), hence a continuous
algebra map \(\mathbf F_3[\Gamma]\to\Xi\).  No assertion below is made for a
finite quotient which does not factor through these fixed presentations and
the registered matched maps.

Let \(N_0\) be the kernel of the fixed roof-level diagonal map.  Denote by

\[
 J_0=\mathbf F_3[\Gamma]
      \langle u-1:u\in N_0\rangle
\tag{1.2}
\]

the relative augmentation ideal.  Its image in the completed diagonal
algebra \(\Xi\) lies in the ideal \(\mathfrak j\) of v173.

A task193 successor calculation can suggest an equality

\[
 e_1=\mu_1d_1
\tag{1.3}
\]

in one finite quotient.  Equation (1.3) alone does not determine an element
of \(\Xi\) and does not imply the same equality at a finer quotient.  The
promotion datum must retain a literal preimage of \(\mu_1\) and prove one
identity before all finite reductions.

## 2. The universal seven-context Fox module

Keep the two PB3 relators, eleven PB4 relators, two printed hexagon words,
five ordered pentagon substitutions, and all prefix transports fixed.  Let
\(\widetilde C_1\) be the direct sum of the seven typed free Fox one-chain
modules over the fixed presented context groups.  Let

\[
 \widetilde D_2:\widetilde C_2\longrightarrow\widetilde C_1
\tag{2.1}
\]

be the direct sum of the complete presentation-boundary maps, followed by
the fixed printed-order combination map.

### Lemma 2.1 (UNIVERSAL DIAGONAL ACTION AND BASE CHANGE)

Restriction along the seven context maps makes both modules left
\(\mathbf F_3[\Gamma]\)-modules, and \(\widetilde D_2\) is equivariant.  For
every registered matched quotient, coefficient base change along (1.1)
takes (2.1) to the block-tagged boundary map \(D_{2,n}\) used in
v168--v173.

#### Proof

On context \(i\), a source word \(u\) acts by left translation through its
fixed image \(\rho_i(u)\).  The tuple of these seven actions depends only on
the image of \(u\) in \(\Gamma\).  The Fox boundary of a conjugated relator
is the correspondingly translated Fox boundary after passage to the
abelian chief layer.  Thus every presentation-boundary summand is
equivariant.  The printed-order combination merely adds separately tagged
equivariant summands, so it is equivariant as well.  Fox derivation, word
substitution, and prefix transport are natural under a quotient of the
presented context group; applying the seven matched quotient maps therefore
gives exactly \(D_{2,n}\). \(\square\)

This is the presentation-level object whose finite reductions give the
block-tagged boundary quotients.  In particular, it is not obtained by
letting one PB3 or PB4 component act on all the other components.

For the fixed base word and its task186 correction, regenerate literal
representatives

\[
 \widetilde d,\widetilde e\in\widetilde C_1
\tag{2.2}
\]

of the signed original target and the corrected residual.  Hashes, ranks,
or equality in one finite quotient cannot replace these literal Fox rows.

## 3. Finite-support promotion theorem

### Theorem 3.1 (UNIVERSAL WORD-POLYNOMIAL PROMOTION)

Suppose there are finitely many literal common-source words
\(u_1,\ldots,u_t\in N_0\), coefficients
\(\alpha_i\in\mathbf F_3\), and one finite-support universal boundary chain
\(q\in\widetilde C_2\) such that, with the ordered noncommutative polynomial

\[
 \boxed{M=\sum_{i=1}^t\alpha_i(u_i-1)\in J_0,}
\tag{3.1}
\]

one has the literal equality

\[
 \boxed{
 \widetilde e-M\widetilde d=\widetilde D_2q
 \quad\text{in }\widetilde C_1.}
\tag{3.2}
\]

Then the image \(\mu\) of \(M\) in \(\Xi\) belongs to \(\mathfrak j\), and
at every matched relative pro-3 quotient

\[
 \boxed{e_n=\mu_nd_n.}
\tag{3.3}
\]

In particular, if \(d=\beta\) and \(e=\beta-Ba\) in the notation of v174,
then v174 Theorem 2.1 gives the single compatible correction

\[
 \boxed{
 c_\infty=-\sum_{r\geq0}\mu^ra.}
\tag{3.4}
\]

subject to the word-bearing and nonlinear side gates stated there.

#### Proof

Every \(u_i\) maps into the relative pro-3 kernel because it is trivial at
the fixed diagonal roof.  Therefore the image of \(u_i-1\) belongs to
\(\mathfrak j\), and so does the image \(\mu\) of (3.1).

By Lemma 2.1, word evaluation, the left Fox derivation, the seven structural
substitutions, prefix transport, and the complete presentation boundary map
all commute with a matched quotient.  Reducing (3.2) at level \(n\) gives

\[
 \widetilde e_n-\mu_n\widetilde d_n=D_{2,n}q_n.
\tag{3.5}
\]

Passing to the boundary quotient kills the right-hand side and proves
(3.3).  The finite-support polynomial (3.1) has compatible images at every
level, hence defines the named element \(\mu\in\Xi\).  Formula (3.4) is now
v174 Theorem 2.1. \(\square\)

### Corollary 3.2 (NO ALL-RUNG ENUMERATION AFTER A UNIVERSAL CERTIFICATE)

Once (3.1)--(3.2) and the v174 side gates are proved, no later Frattini rung
requires a new membership solve.  The reductions of the same \(M,q\) are the
coefficients and boundary witnesses at every rung.

This conclusion is unavailable from (1.3) alone.  The load-bearing addition
is the universal literal boundary equality (3.2).

## 4. Exact post-task193 search contract

The efficient route has two sharply separated phases.

### Phase A: finite discovery

At the first genuine successor built by task193:

1. regenerate both \(e_1\) and the original target shadow \(d_1\) in the
   same canonical affine label universe;
2. enumerate the diagonal images of a preregistered finite set of short
   source-kernel words \(u\), forming the columns
   \((u-1)d_1\);
3. solve (1.3) with a literal coefficient vector, or return a complete dual
   for that registered column universe, or `UNKNOWN_RESOURCE`;
4. retain the exact support words, their seven context images, every column,
   the boundary coefficients, and a direct replay of the resulting equality.

A positive Phase A result is a candidate for \(M\), not an all-rung proof.

### Phase B: universal promotion

For the exact support found in Phase A:

1. authenticate that every \(u_i\) is in the roof diagonal kernel;
2. reconstruct \(M\widetilde d\) by the full noncommutative seven-context
   action;
3. solve for a finite \(q\) in (3.2) using the complete two/eleven PB
   presentation boundaries, retaining a literal ancestry;
4. independently replay every group word, Fox sign, prefix transport,
   context tag, pentagon order, and boundary coefficient;
5. mutate at least one support word, one factor order, one left transport,
   one block tag, and one boundary coefficient and require rejection.

Failure to find \(q\) within a bounded search is `UNKNOWN`, not a proof that
no universal certificate exists.  A complete dual in a precisely registered
finite universal coefficient universe only excludes that universe.

## 5. Interaction with the relative-dihedral split

On the return-odd summand, the already typed relative-dihedral operator may
provide a separate universal polynomial identity.  Theorem 3.1 is especially
useful for the return-even actual class, where \(1-\theta\) vanishes and a
field-outer/relative-kernel word polynomial must be found.  The two
certificates may be added only after their summands and diagonal actions are
shown stable under the same matched maps.

The theorem closes only the relative pro-3 abelian correction once its
hypotheses hold.  Formation purification, prime-to-three refinements, and
new nonabelian perfect-core accepted sets remain separate witness gates.

## 6. Fixed frontier

```text
FINITE-SUPPORT UNIVERSAL PROMOTION THEOREM:       PAPER_PROOF
POST-task193 TWO-PHASE CERTIFICATE CONTRACT:       SPECIFIED
TASK186 EXACT FIRST CORRECTION:                    GHA IN PROGRESS
TASK193 SECOND-RUNG AFFINE COMPILER / RESIDUAL:    IMPLEMENTATION AUDIT
FINITE ACTUAL MULTIPLIER mu_1:                     NOT COMPUTED
UNIVERSAL WORD-POLYNOMIAL M:                       NOT FOUND
UNIVERSAL BOUNDARY CHAIN q:                        NOT FOUND
RELATIVE PRO-3 COMPATIBLE R07 LIFT:                NOT YET CONSTRUCTED
PRIME-TO-3 / NEW NONABELIAN COFINAL GATES:         OPEN
FAKE / IHARA WITNESS:                              NOT DECLARED
```

`R07_UNIVERSAL_WORD_POLYNOMIAL_MULTIPLIER_PROMOTION_V175_PAPER_GRADE`
