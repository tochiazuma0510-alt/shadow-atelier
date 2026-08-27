# R07 cyclic successor-kernel Hensel theorem v182

Author: Sol / 2026-08-28

Status: paper theorem and all-rung promotion target.  It gives an exact
condition under which one successful roof correction automatically remains
in the same cyclic actual-defect module at every refinement, with compatible
coefficients.  The required R07 successor-kernel equality has not been proved.
No compatible lift, fake certificate, or Ihara witness is declared.

## 1. Compatible cyclic data

Let

\[
 \Lambda_{n+1}\twoheadrightarrow\Lambda_n,
 \qquad I_n=\ker(\Lambda_{n+1}\to\Lambda_n)
\tag{1.1}
\]

be an inverse system of finite, possibly noncommutative rings.  Let

\[
 r_n:D_{n+1}\twoheadrightarrow D_n
\tag{1.2}
\]

be compatible surjections of finite left modules, and let
\(d=(d_n)\in\varprojlim D_n\) be the distinguished signed original target.
All coefficients below act on the left.

Assume

\[
 \boxed{D_0=\Lambda_0d_0}
\tag{1.3}
\]

and, at every successor, the exact kernel identity

\[
 \boxed{
 \ker r_n=I_nd_{n+1}.}
\tag{1.4}
\]

The inclusion from right to left is automatic by compatibility.  The reverse
inclusion is the load-bearing assertion: every genuinely new actual-defect
direction must be obtained by applying a new coefficient to the same target.

## 2. Cyclicity propagates through every successor

### Theorem 2.1 (CYCLIC SUCCESSOR-KERNEL PROMOTION)

Under (1.3)--(1.4),

\[
 \boxed{D_n=\Lambda_nd_n\quad\text{for every }n.}
\tag{2.1}
\]

#### Proof

Proceed by induction.  The roof case is (1.3).  Suppose
\(D_n=\Lambda_nd_n\) and take \(z\in D_{n+1}\).  Its reduction has the
form

\[
 r_n(z)=\lambda_nd_n
\tag{2.2}
\]

for some \(\lambda_n\in\Lambda_n\).  Choose a lift
\(\widetilde\lambda\in\Lambda_{n+1}\).  Then

\[
 r_n(z-\widetilde\lambda d_{n+1})=0.
\tag{2.3}
\]

By (1.4), there is \(\kappa\in I_n\) such that

\[
 z-\widetilde\lambda d_{n+1}=\kappa d_{n+1}.
\tag{2.4}
\]

Thus \(z=(\widetilde\lambda+\kappa)d_{n+1}\), proving the induction step.
No coefficient was commuted past another. \(\square\)

This theorem does not require \(d_n\) to have zero annihilator.  It asserts
existence of coefficients, not their uniqueness.

## 3. Every coefficient solution lifts

Let \(e=(e_n)\in\varprojlim D_n\) be a compatible corrected residual and
put

\[
 S_n(e)=\{\mu\in\Lambda_n:\mu d_n=e_n\}.
\tag{3.1}
\]

### Theorem 3.1 (SURJECTIVE SOLUTION FIBRES)

Under (1.3)--(1.4), every reduction map

\[
 S_{n+1}(e)\longrightarrow S_n(e)
\tag{3.2}
\]

is surjective.

#### Proof

Take \(\mu_n\in S_n(e)\) and choose a lift
\(\widetilde\mu\in\Lambda_{n+1}\).  Compatibility gives

\[
 r_n(e_{n+1}-\widetilde\mu d_{n+1})
 =e_n-\mu_nd_n=0.
\tag{3.3}
\]

By (1.4), choose \(\kappa\in I_n\) with

\[
 e_{n+1}-\widetilde\mu d_{n+1}=\kappa d_{n+1}.
\tag{3.4}
\]

Then \(\mu_{n+1}=\widetilde\mu+\kappa\) lies in \(S_{n+1}(e)\) and reduces
to \(\mu_n\). \(\square\)

Because the rings and fibres are finite, one may either choose recursively or
apply compactness to obtain

\[
 \boxed{
 \mu=(\mu_n)\in\varprojlim S_n(e),
 \qquad e=\mu d.}
\tag{3.5}

With fixed ordered bases, choosing the lexicographically first lift and the
first canonical solution of (3.4) makes this a deterministic selector.

## 4. Relative-depth version

Let \(\mathfrak j_n\triangleleft\Lambda_n\) be compatible relative
augmentation ideals such that

\[
 \mathfrak j_{n+1}\twoheadrightarrow\mathfrak j_n,
 \qquad I_n\subseteq\mathfrak j_{n+1}.
\tag{4.1}
\]

Suppose the successful roof correction gives

\[
 e_0=0.
\tag{4.2}
\]

Start with \(\mu_0=0\).  In Theorem 3.1 choose
\(\widetilde\mu\in\mathfrak j_{n+1}\); the correcting
\(\kappa\in I_n\) also lies in \(\mathfrak j_{n+1}\).  Induction therefore
gives

\[
 \boxed{
 \mu_n\in\mathfrak j_n,
 \qquad e_n=\mu_nd_n
 \quad\text{for all }n.}
\tag{4.3}

Passing to the inverse limit yields

\[
 \mu\in\mathfrak j,
 \qquad e=\mu d.
\tag{4.4}

If \(a\) is the literal first correction and the word-bearing/nonlinear gates
of v174 hold, the pointed Neumann formula now gives the single all-rung
correction

\[
 \boxed{
 c_\infty=-\sum_{q\ge0}\mu^qa.}
\tag{4.5}

Thus (1.4), not a fresh unrelated solve at every rung, is a sufficient
structural bridge from the first exact correction to the completed relative
pro-3 correction.

## 5. Necessity relative to the whole actual subsystem

Suppose already that \(D_n=\Lambda_nd_n\) and
\(D_{n+1}=\Lambda_{n+1}d_{n+1}\).  Then

\[
 \ker r_n
 =\{\lambda d_{n+1}:\overline\lambda d_n=0\}.
\tag{5.1}
\]

This can be larger than \(I_nd_{n+1}\) when a new lift of a downstairs
annihilator acts nontrivially upstairs.  Hence (1.4) contains two assertions:

1. no transverse new actual-defect direction appears; and
2. no downstairs relation of \(d_n\) opens into an extra successor direction.

Equivalently, the natural map of cyclic modules

\[
 \Lambda_{n+1}d_{n+1}/I_nd_{n+1}
 \longrightarrow\Lambda_nd_n
\tag{5.2}

must be an isomorphism and the whole actual subsystem must equal the cyclic
source.  A dimension match without a direct map replay is insufficient.

## 6. Exact finite certificate

At one successor, a complete certificate for (1.4) consists of:

1. the genuine diagonal rings \(\Lambda_{n+1}\to\Lambda_n\) and a basis of
   \(I_n\);
2. the complete actual-defect subsystem \(D_{n+1}\), its reduction matrix,
   and a basis of \(\ker r_n\);
3. all columns \(\kappa d_{n+1}\) for a generating basis of \(I_n\), reduced
   through the complete boundary quotient;
4. equality of the two spans, with literal coefficient ancestry in both
   directions; and
5. an independent direct-action replay.

If the spans differ, a dual separating a vector of \(\ker r_n\) from
\(I_nd_{n+1}\) is a complete finite failure of (1.4) for that successor.
A resource stop is `UNKNOWN`.

Task193 supplies the first genuine successor residual and boundary template;
task194 supplies the exact complete correlation machinery needed for item 3.
The first computation is a canary.  To invoke Theorem 2.1 on all rungs, the
same equality must be proved structurally from the universal seven-context
Fox presentation, or certified at every cofinal successor.

## 7. Relation to the trace route

V178--v181 construct compatible equivariant functionals and use them to
detect or recover a multiplier.  The present theorem instead proves cyclicity
directly from exact successor kernels.  Either route can close the multiplier
gate:

\[
 \begin{array}{c}
 \text{trace/Tate route: functional + injectivity},\\
 \text{kernel-Hensel route: }\ker r_n=I_nd_{n+1}.
 \end{array}
\tag{7.1}

The second route is stronger as a module statement but avoids choosing duals.
It is especially attractive if the task193/task194 matrices show that the
actual subsystem is visibly rank-one under the diagonal action.

## 8. Fixed frontier

```text
CYCLIC SUCCESSOR-KERNEL PROMOTION:              PAPER_PROOF
SURJECTIVE COMPATIBLE COEFFICIENT FIBRES:        PAPER_PROOF
RELATIVE-DEPTH ALL-RUNG MULTIPLIER:              PAPER_PROOF
R07 FIRST SUCCESSOR KERNEL EQUALITY:             NOT COMPUTED
R07 UNIVERSAL ALL-RUNG KERNEL EQUALITY:           NOT PROVED
TASK193 ACTUAL SUCCESSOR COMPILER SELFTEST:       CROSS_CHECKED
TASK194 COMPLETE CORRELATION SHARDING:            IMPLEMENTATION IN PROGRESS
WORD/NONLINEAR/FORMATION GATES:                   OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA:           NOT DECLARED
```

`R07_CYCLIC_SUCCESSOR_KERNEL_HENSEL_V182_PAPER_GRADE`
