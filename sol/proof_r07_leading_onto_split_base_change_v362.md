# R07 leading-onto split base-change criterion (v362)

Author: Sol / 2026-08-30

Status: paper theorem refining v319 and v361.  Over a complete ring whose
chosen ideal lies in the Jacobson radical, surjectivity of a module map on
the leading quotient already gives an explicit continuous section whenever
the codomain is finite free (and, more generally, gives a split epimorphism
when the codomain is finite projective).  Thus the two base-change defects
of v361 vanish together.  Application to the actual R07 source and target
still requires physical finite-free/projective codomains and leading-rank
certificates.  No compatible lift, fake certificate or Ihara witness is
declared.  `verified=false`.

## 1. Leading surjectivity constructs a section

Let \(\Lambda\) be a unital ring, let \(J\triangleleft\Lambda\) be a
two-sided ideal, and let

\[
 f:M\longrightarrow N
\tag{1.1}
\]

be a homomorphism of left \(\Lambda\)-modules.  Write

\[
 \bar f:M/JM\longrightarrow N/JN
\tag{1.2}
\]

for its leading reduction.

### Theorem 1.1 (LEADING-ONTO FREE-TARGET SPLITTER)

Assume that \(N\cong\Lambda^q\) is finite free and that \(\bar f\) is
surjective.  Suppose either

1. \(J^d=0\) for some \(d\); or
2. \(\Lambda\) and \(N\) are complete and separated for the \(J\)-adic
   topology and all maps below are continuous.

Then \(f\) has an explicit \(\Lambda\)-linear section.  In particular,

\[
 \boxed{M=\ker(f)\oplus s(N).}
\tag{1.3}
\]

#### Proof

Let \(e_1,\ldots,e_q\) be the standard basis of \(N\).  Surjectivity of
(1.2) lets us choose \(m_i\in M\) with

\[
 f(m_i)\equiv e_i\pmod{JN}.
\tag{1.4}
\]

Define \(s_0:N\to M\) by \(s_0(e_i)=m_i\), and put

\[
 E=fs_0-1_N.
\tag{1.5}
\]

Then \(E(N)\subseteq JN\).  Since \(E\) is \(\Lambda\)-linear and \(J\)
is two-sided,

\[
 E(J^rN)\subseteq J^rE(N)\subseteq J^{r+1}N,
 \qquad E^r(N)\subseteq J^rN.
\tag{1.6}
\]

In the nilpotent case the finite sum, and in the complete case the
convergent sum,

\[
 U=\sum_{r\geq0}(-E)^r
\tag{1.7}
\]

is a two-sided inverse of \(1_N+E\).  Hence

\[
 \boxed{s=s_0U,\qquad fs=(1_N+E)U=1_N.}
\tag{1.8}
\]

The section gives (1.3).  \(\square\)

The construction is based rather than existential: a receipt need only
retain the leading preimages \(m_i\), the error matrix \(E\), and the
finite or truncated Neumann sum (1.7).

### Corollary 1.2 (FINITE PROJECTIVE TARGET)

Assume \(J\subseteq\operatorname{Jac}(\Lambda)\), \(N\) is finitely
generated projective, and \(\bar f\) is surjective.  Then \(f\) is a split
epimorphism.

#### Proof

The cokernel \(C=\operatorname{coker}f\) is finitely generated and (1.2)
gives \(C/JC=0\).  Nakayama's lemma gives \(C=0\), so \(f\) is
surjective.  Projectivity of \(N\) supplies a section.  \(\square\)

At a finite relative \(p\)-group edge, \(\Lambda=\mathbf F_p[P]\) and its
augmentation ideal are local/nilpotent, so Theorem 1.1 applies directly to
finite-free codomains.  At a completed pro-\(p\) edge, its second branch is
the corresponding continuous Neumann construction.

## 2. The v361 defects vanish at every depth

Put \(L=\ker f\).  If the hypotheses of Theorem 1.1 or Corollary 1.2 hold,
then v361 Corollary 2.2 applies and gives, for every \(r\geq1\),

\[
 \boxed{
 S_r(f)=\frac{L\cap J^rM}{J^rL}=0,
 \qquad
 T_r(f)=\frac{\operatorname{im}f\cap J^rN}{f(J^rM)}=0.}
\tag{2.1}
\]

Consequently the natural map is an isomorphism

\[
 \boxed{L/J^rL\;\xrightarrow{\sim}\;\ker(\bar f_r).}
\tag{2.2}
\]

For completeness, the two equalities can also be read directly from the
section.  The decomposition \(M=L\oplus s(N)\) gives
\(L\cap J^rM=J^rL\), while surjectivity and \(\Lambda\)-linearity give
\(f(J^rM)=J^rN\).

This is stronger than separately finding zero-dimensional defect spaces at
one depth: the same section kills both discrepancies at all depths and is
compatible with the Neumann recursion when its data commute with the tower.

## 3. Exact R07 use

For v361's source map

\[
 G:\widetilde A\longrightarrow Y,
 \qquad A_{\rm legal}=\ker G,
\tag{3.1}
\]

the following physical certificate is sufficient:

1. identify \(Y\) as a finite free module over the actual relative
   group/action ring (or as a finite projective module);
2. serialize the literal matrix of \(G\) and the same \(J\) used by the
   Newton filtration;
3. prove that \(\bar G\) has full target rank; and
4. replay (1.4)--(1.8), including the exact section identity.

Under those gates,

\[
 \boxed{S_1(G)=T_1(G)=0,\qquad
 A_{\rm legal}/JA_{\rm legal}\cong\ker\bar G.}
\tag{3.2}
\]

The same statement applies to v361's packaged target map

\[
 H:Z\longrightarrow Q,
 \qquad L_{\rm loc}=\ker H,
\tag{3.3}
\]

provided the *actual* codomain \(Q\), rather than a convenient larger raw
coordinate space, is finite free/projective and \(\bar H\) is onto.  Then

\[
 \boxed{S_1(H)=T_1(H)=0,\qquad
 L_{\rm loc}/JL_{\rm loc}\cong\ker\bar H.}
\tag{3.4}

This condition must not be inferred merely because the underlying
\(\mathbf F_3\)-matrix has a vector-space complement.  Freeness/projectivity,
linearity over the actual action ring, and leading surjectivity are all
load-bearing.  In particular, an unsplit normalized \(d_0\) sequence or a
nonprojective formation target still falls back to v361's explicit defect
calculation.

## 4. Reduced post-A4 decision tree

After a positive A4 action owner and task382's extraction of
\([\widetilde S,K]\), the base-change branch is now:

\[
 \boxed{
 \begin{array}{c}
 \text{authenticate actual }G,H,J\text{ and codomain module types};\\
 \bar G,\bar H\text{ onto and codomains finite free/projective}
   \Longrightarrow S_1(G)=T_1(G)=S_1(H)=T_1(H)=0;\\
 \text{otherwise compute exactly only the unresolved v361 defects.}
 \end{array}}
\tag{4.1}
\]

Thus four unconditional quotient computations are no longer the first
choice.  Two leading-rank tests plus two module-type certificates may close
the entire base-change gate.  They do not replace the subsequent actual
leading Jacobian onto calculation.

```text
LEADING ONTO + FINITE-FREE TARGET => EXPLICIT SPLIT: PAPER PROOF
SPLIT => ALL S_r,T_r VANISH:                         PAPER PROOF / v361
ACTUAL SOURCE CODOMAIN Y FREE/PROJECTIVE:            NOT AUTHENTICATED
ACTUAL TARGET CODOMAIN Q FREE/PROJECTIVE:             NOT AUTHENTICATED
ACTUAL bar-G / bar-H LEADING ONTO:                    NOT COMPUTED
ACTUAL LEADING COMMON-WORD JACOBIAN:                  NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:               NOT CONSTRUCTED
```

`R07_LEADING_ONTO_SPLIT_BASE_CHANGE_V362_PAPER_GRADE`
