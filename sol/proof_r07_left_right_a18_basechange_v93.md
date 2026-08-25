# Exact left/right base change for the literal A.18 Jacobian v93

Author: Sol / 2026-08-26

Status: paper proof.  This identifies the two multiplication-side
linearizations at one fixed coarse base.  It does not transport data between
the 616- and 760-letter bases at a finer quotient.  verified=false; no
cofinal lift or Ihara witness is declared.

## 1. Fixed extension and coface order

Let

\[
1\longrightarrow V\longrightarrow \widetilde Q
 \longrightarrow Q\longrightarrow1
\tag{1.1}
\]

be a group extension with \(V\) abelian.  Write the action of \(q\in Q\)
on \(V\) multiplicatively as \(qv\), while writing the group law of \(V\)
additively.

Fix a coarse common-word value \(q\) at arity three.  In the printed A.18
order put

\[
b_i=\phi_i(f_0),\qquad q_i=\phi_i(q)\quad(1\leq i\leq5),
\tag{1.2}
\]

and

\[
W=b_1b_2b_3b_5^{-1}b_4^{-1}.
\tag{1.3}
\]

The coarse relation says

\[
q_1q_2q_3q_5^{-1}q_4^{-1}=1.
\tag{1.4}
\]

Let \(\lambda_i:V_3\to V_4\) be the five descended coface maps.  Their
equivariance is

\[
\lambda_i(qv)=q_i\lambda_i(v).
\tag{1.5}
\]

## 2. The two exact derivatives

For the left correction \(f_0\mapsto vf_0\), v71 gives

\[
\begin{aligned}
D_L(v)={}&\lambda_1(v)+q_1\lambda_2(v)
q_1q_2\lambda_3(v)\\
&-q_1q_2q_3q_5^{-1}\lambda_5(v)-\lambda_4(v).
\end{aligned}
\tag{2.1}
\]

### Theorem 2.1 (RIGHT-A18-JACOBIAN)

For the right correction \(f_0\mapsto f_0v\), the exact literal A.18
derivative is

\[
\boxed{
\begin{aligned}
D_R(v)={}&q_1\lambda_1(v)+q_1q_2\lambda_2(v)
q_1q_2q_3\lambda_3(v)\\
&-q_1q_2q_3\lambda_5(v)-q_4\lambda_4(v).
\end{aligned}}
\tag{2.2}
\]

Moreover

\[
\boxed{D_R=D_L\circ A_q,}
\qquad A_q(v)=qv.
\tag{2.3}
\]

#### Proof

Under right correction the five lifted factors are
\(b_i\lambda_i(v)\).  Collecting the kernel entries to the left of the
coarse product gives the three positive contributions

\[
q_1\lambda_1(v),\quad
q_1q_2\lambda_2(v),\quad
q_1q_2q_3\lambda_3(v).
\]

The inverse \((b_5\lambda_5(v))^{-1}\) contributes
\(-q_1q_2q_3\lambda_5(v)\).  The final inverse contributes
\(-q_1q_2q_3q_5^{-1}\lambda_4(v)\), which is
\(-q_4\lambda_4(v)\) by (1.4).  This proves (2.2).

Alternatively, in the source extension,

\[
f_0v=(qv)f_0.
\tag{2.4}
\]

Substitute \(qv\) into (2.1) and use (1.5).  The fifth term becomes
\(-q_1q_2q_3\lambda_5(v)\), and the last becomes
\(-q_4\lambda_4(v)\), proving (2.3).  The collection takes place in the
abelian chief kernel, so these are exact affine identities, not truncated
first-order formulas. \(\square\)

## 3. Joint hexagon/pentagon system

The same argument works for every literal relation word: right correction
at \(f_0\) is left correction by \(A_qv\).  Therefore, if

\[
L_L=(E_L,\mathscr P_L),\qquad
L_R=(E_R,\mathscr P_R)
\tag{3.1}
\]

are the complete two-hexagon plus ordered-A.18 maps at the same base, then

\[
\boxed{L_R=L_LA_q.}
\tag{3.2}
\]

Since \(A_q\) is an automorphism of the chief module, it gives a bijection
between the two affine solution sets.  In particular,

\[
\ker E_R=A_q^{-1}(\ker E_L),\qquad
\mathscr P_R(\ker E_R)=\mathscr P_L(\ker E_L).
\tag{3.3}
\]

Thus the normalized Brunnian obstruction is independent of whether the
same fixed-base problem is encoded on the left or on the right, after the
coordinate change \(A_q\) is recorded.

This theorem does not compare two different base words which agree only in
a coarser quotient.  Such a comparison still requires both identities of
v86:

\[
L_1T=SL_0,\qquad b_1=Sb_0.
\tag{3.4}
\]

Accordingly, the 760-letter RHS and gradients must be rebuilt from the
760-letter word; (3.2) can then serve as a multiplication-side canary inside
that rebuilt problem.

## 4. Required finite certificate

At the first 760-letter chief edge, record:

1. the five \(q_i\), the action matrix \(A_q\), and all five \(\lambda_i\);
2. matrices built independently from (2.1) and (2.2);
3. the exact equality \(D_R=D_LA_q\);
4. the analogous equality for both hexagon rows;
5. a mutation of one inverse, prefix, or coface order which breaks the
   equality.

The certificate concerns the literal arity/coface complex.  A left-Fox
presentation membership matrix is not accepted as either side of (2.3)
without a separate chain map.

    GENERAL LEFT/RIGHT A18 BASE CHANGE:          PAPER_PROOF
    SAME-BASE SOLUTION-SET BIJECTION:            PAPER_PROOF
    616-TO-760 FINE-EDGE TRANSPORT:              NOT CLAIMED
    760 ACTUAL A18 MATRIX/RHS:                   PENDING
    COFINAL COMPATIBLE LIFT:                     NOT YET CONSTRUCTED
    IHARA WITNESS:                               NOT DECLARED
