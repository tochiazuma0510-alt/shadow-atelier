# R07 A0: exact split-presentation handoff from grade one to grade two (v450)

Author: Sol / 2026-09-03

Status: candidate algebraic handoff theorem.  It specializes the audited
v441/v444/v446--v449 induction to the state emitted by the first-grade v3/v4
engine.  It proves that the completed prepare and four character-block states
already determine the target-independent grade-two module computation.  It
does not decide grade-one membership, and it does not declare order 54,432,
full Q0, A0, COMMON, a cofinal lift, fake, or Ihara. `verified=false`.

## 1. Frozen split data

Work over \(k=\mathbf F_3\).  Let \(U_0\) be the complete order-2,016
occurrence-source image and let

\[
 r_0:U_1\longrightarrow U_0
\]

be reduction from precision one to precision zero in the first
\(C_3^3\)-rung.  The four legal character projectors of v447 split the
degree-zero presentation into bases

\[
 B_{0,\chi}=(b_{\chi,1},\ldots,b_{\chi,r_\chi}),
 \qquad \chi\in\widehat {C_2^2}.
\]

The prepare state retains, for every projected seed and every registered
actor \(A\in\{x,x^{-1},y,y^{-1}\}\), the exact relations

\[
 s_{a,\chi}^{(0)}=\sum_iq_{a,\chi i}b_{\chi,i},
 \qquad
 Ab_{\chi,i}=\sum_jq_{A,\chi ij}b_{\chi,j}.          \tag{1.1}
\]

It also retains literal instruction ancestry and canonical precision-one
lifts \(\widetilde b_{\chi,i}\).  Lifting (1.1) produces the complete seed
and transition defects

\[
 \epsilon_{a,\chi}=s_{a,\chi}^{(1)}-
       \sum_iq_{a,\chi i}\widetilde b_{\chi,i},
 \qquad
 \delta_{A,\chi,i}=A\widetilde b_{\chi,i}-
       \sum_jq_{A,\chi ij}\widetilde b_{\chi,j}.     \tag{1.2}
\]

Every vector in (1.2) lies in \(\ker r_0\).  The four completed block states
retain the reduction of every projected vector
\(e_\lambda\epsilon_{a,\chi}\) and
\(e_\lambda\delta_{A,\chi,i}\) against an exhausted basis
\(H_{1,\lambda}\), together with all four actor transitions and a literal
DAG for that basis.  Put

\[
 H_1=\bigoplus_\lambda H_{1,\lambda}.                \tag{1.3}
\]

No physical merge or target coefficient occurs in this data.

## 2. Deterministic assembly theorem

### Theorem 2.1

Order first by old character and pivot, then by new character and pivot.  The
ordered roster

\[
 \boxed{
 B_1=(\widetilde b_{\chi,i})_{\chi,i}\ \Vert\
             (h_{\lambda,j})_{\lambda,j}}
                                                               \tag{2.1}
\]

is a basis of the complete precision-one legal occurrence image \(U_1\).
The prepare and four block states determine exact reductions of all 44
original seeds and all four actor images of every row of (2.1).  They also
determine literal instruction ancestry for every row.  Consequently they
determine the complete transition presentation \(\mathcal T_1\), without
rediscovering any historical actor path.

#### Proof

V444 gives

\[
 U_1=\operatorname{span}(\widetilde B_0)\oplus H_1. \tag{2.2}
\]

The sum is direct because a combination of lifted old rows that lies in
\(\ker r_0\) reduces to a zero combination of the basis \(B_0\).  The four
summands in (1.3) are direct by the legal character idempotents on the pure
grade.  Thus (2.1) is a basis.

For an old lifted row, (1.2) gives its actor image as the recorded old
transition plus a transition defect.  The four block `origin_reductions`
give the coordinates of that defect in the second part of (2.1).  For a new
row, its block `actor_transitions` give the coordinates directly.  These are
all actor relations.

Likewise, (1.2) expresses every projected seed as its old recorded reduction
plus its seed defect.  Summing the four legal character projections gives
each original seed, since \(\sum_\chi e_\chi=1\).  Hence all 44 seed
reductions are determined.  Finally, every old row has the prepare DAG, and
every new row has a block DAG whose leaves are recorded defects; recursively
substituting (1.2) terminates in literal compact-seed conjugates.  This gives
the required instruction ancestry. \(\square\)

### Corollary 2.2

The compact `transition_presentation` object in the merge certificate is a
digest-bearing summary, not a standalone serialization of \(\mathcal T_1\).
Theorem 2.1 requires the authenticated prepare state, all four block states
and their referenced basis/lift blobs.  A grade-two consumer must reconstruct
the global ordering (2.1) and directly replay the assembled seed and actor
relations; matching only the summary digest is insufficient.

## 3. Work that is independent of the grade-one terminal

The module \(U_1\), its presentation \(\mathcal T_1\), and the next canonical
image fibre depend only on the seeds, actors, occurrence maps, filtration and
boundary quotient.  They do not depend on a chosen target solution.  Thus,
after the prepare and all four block states are authenticated, one may safely
perform the following before the grade-one MEMBER/NONMEMBER terminal exists:

1. assemble and replay \(\mathcal T_1\) by Theorem 2.1;
2. lift its basis, 44 seed reductions and four actor-transition reductions
   to precision two;
3. form every v444 seed and transition defect \(H^{[2]}\);
4. exhaust its four v447 character closures, retaining all six degree-two
   monomials coupled in each block; and
5. combine the lifted \(B_1\) rows and exhausted \(H^{[2]}\) rows in the
   complete lower-first grade-two physical fibre.

These steps may be sealed only as a **target-independent module state**.
They may not be called a complete \(\mathcal T_1\) terminal, a grade-two
residual, or a membership result until the checked grade-one terminal is
bound as their parent.

The exact new-grade widths are

\[
 4\times36,288=145,152\quad\hbox{(source)},
 \qquad48,384\quad\hbox{(joint physical)}.           \tag{3.1}
\]

The lower-first physical block has

\[
 8,064+24,192+4=32,260                               \tag{3.2}
\]

coordinates: degree zero, degree one, and the four PB3/exponent auxiliary
coordinates.  A four-trits-per-byte degree-two residual occupies exactly
12,096 bytes.  These are dimensions, not rank or runtime estimates.

## 4. The result-dependent join

If the independently checked grade-one terminal is MEMBER, it supplies the
literal solution \(c_1\).  The grade-two consumer must independently compute

\[
 \rho_2=T^{(2)}-A^{(2)}(c_1)                         \tag{4.1}
\]

from the literal word, not merely trust the stored residual blob.  It must
recompute the packed digest, sparse digest and support, then bind them and the
entire authenticated split state as parents of the grade-two run.  Only then
may it reduce \(\rho_2\) against the precomputed complete fibre.

If the grade-one terminal is NONMEMBER, there is no \(c_1\) on this
registered lower solution locus and the grade-two join is forbidden.  The
target-independent module state remains a valid computation of the source
module, but it has no witness consequence for this branch.

The existing first-grade checker establishes a positive precision-one target
replay.  Its mere reading of the degree-two blob is not the independent
calculation required by (4.1); that calculation is a mandatory grade-two
preflight gate and does not weaken the grade-one conclusion.

## 5. Claim boundary

```text
GRADE-ONE SOURCE CLOSURES: completed production states; terminal still live
SPLIT STATES -> COMPLETE T1: paper-closed by Theorem 2.1; direct replay required
TARGET-INDEPENDENT GRADE-TWO MODULE: may be built before grade-one terminal
GRADE-TWO RESIDUAL / MEMBERSHIP: requires checked grade-one MEMBER
ORDER-54,432 / FULL-Q0 / A0 / COMMON / COFINAL LIFT: not declared
FAKE / IHARA: not declared
verified=false
```

`R07_GRADE1_TO_GRADE2_SPLIT_PRESENTATION_HANDOFF_V450_CANDIDATE`
