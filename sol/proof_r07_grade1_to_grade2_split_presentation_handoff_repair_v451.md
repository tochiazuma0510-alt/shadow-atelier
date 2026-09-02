# R07 A0: audited repair of the grade1-to-grade2 split handoff (v451)

Author: Sol / 2026-09-03

This is the versioned repair of v450 required by independent Task566 verdict
`GRADE1_TO_GRADE2_HANDOFF_PASS_AFTER_REPAIR`.  V450 is used only with the
replacements below.  The underlying direct-sum and target-independence
theorems are unchanged.  No finite grade membership, A0, COMMON, cofinal
lift, fake or Ihara conclusion is asserted. `verified=false`.

## 1. Full filtered word-sums are not associated-grade projectors

Let

\[
 C=((0,0),(0,1),(1,0),(1,1))
\]

in the serialized order, let \(w_a\) be the four exact v447 pure-Q1 source
words, with \(w_{(0,0)}\) empty, and define on precision one

\[
 P_\chi=\sum_{a\in C}\chi(a)L_{w_a}^{\leq1}.         \tag{1.1}
\]

The precision-one projected seed stored by the prepare phase is
\(P_\chi s_b^{(1)}\).  Reduction to degree zero turns \(P_\chi\) into the
usual character projector.  On the full filtered module, however,
\(P_\chi\) is **not** assumed idempotent: the upstairs kernel coordinates of
the words may add lower-to-grade terms.

Reserve \(e_\lambda\) for the genuine v447 idempotent on the pure associated
grade.  It is the \(e_\lambda\) that gives

\[
 H_1=\bigoplus_{\lambda\in C}H_{1,\lambda}.          \tag{1.2}
\]

The reconstruction of an original seed instead uses the exact word identity

\[
 \sum_{\chi\in C}P_\chi
 =\sum_{a\in C}\left(\sum_\chi\chi(a)\right)
       L_{w_a}^{\leq1}
 =4L_{w_{(0,0)}}^{\leq1}=1                          \tag{1.3}
\]

in \(\mathbf F_3\).  Thus the four stored projected relations sum to the
original one even though the individual full filtered operators need not be
projectors.  V450 Theorem 2.1 uses reduction for independence of the lifted
old rows and (1.2) for independence of the new rows; it never needs
idempotence of (1.1).

## 2. Exact global reconstruction formulas

Use actor order

```text
(1,-1,2,-2) = (x,x^-1,y,y^-1)
```

and the character order \(C\) above.  Let

\[
 r_\chi=|B_{0,\chi}|,\qquad n_\lambda=|H_{1,\lambda}|,
 \qquad R=\sum_\chi r_\chi,
\]

and define zero-based global offsets

\[
 O_\chi=\sum_{\kappa<\chi}r_\kappa,
 \qquad
 N_\lambda=R+\sum_{\mu<\lambda}n_\mu,
 \qquad
 D_\chi=\sum_{\kappa<\chi}(44+4r_\kappa).           \tag{2.1}
\]

For a one-based seed label \(a\), a zero-based old pivot \(i\), and a
zero-based actor position \(t\), the prepare origin indices are

\[
 o_s(\chi,a)=D_\chi+a-1,
 \qquad
 o_t(\chi,i,t)=D_\chi+44+4i+t.                      \tag{2.2}
\]

Write \(q^s_{\chi,a,i}\) for the coefficient in the stored old
`seed_reductions[a-1]`, \(q^A_{\chi,i,t,j}\) for the coefficient in
`actor_transitions[i][t]`, and \(R_{\lambda,o,j}\) for the coefficient in
block \(\lambda\)'s `origin_reductions[o]`.  In the deterministic global
basis

\[
 B_1=(\widetilde b_{\chi,i})_{\chi,i}\ \Vert\
     (h_{\lambda,j})_{\lambda,j},                   \tag{2.3}
\]

the 44 seed relations are exactly

\[
 s_a^{(1)}=
 \sum_{\chi,i}q^s_{\chi,a,i}B_1[O_\chi+i]
 +\sum_{\chi,\lambda,j}R_{\lambda,o_s(\chi,a),j}
                            B_1[N_\lambda+j],        \tag{2.4}
\]

and every old-row actor relation is

\[
 A_t\widetilde b_{\chi,i}=
 \sum_jq^A_{\chi,i,t,j}B_1[O_\chi+j]
 +\sum_{\lambda,j}R_{\lambda,o_t(\chi,i,t),j}
                            B_1[N_\lambda+j].        \tag{2.5}
\]

Both displayed defect sums have a plus sign: a packet is the lifted left
side minus its old reduction.  The subtractions are already inside that
packet's literal expansion.  Every one of the four \(\lambda\)-block
reductions must be included.

For a new row the relation is

\[
 A_t h_{\lambda,i}
 =\sum_jp_{\lambda,i,t,j}B_1[N_\lambda+j],          \tag{2.6}
\]

where \(p\) is the block's stored transition.  If an accepted DAG node is
obtained from a candidate \(z\), prior reductions \(c_p\), and stored
normalizing scale \(\sigma_j\in\{1,2\}\), its literal identity is

\[
 h_j=\sigma_j\left(z-\sum_{p<j}c_ph_p\right).       \tag{2.7}
\]

Old roots are full filtered word-sums (1.1); pure packet splitting uses
\(e_\lambda\); actor nodes prepend the stored actor.  The pivot order makes
this recursion well founded.  A grade-two consumer must reconstruct the
global offsets, directly replay (1.3) and (2.4)--(2.7), and replay every
literal expansion against the referenced basis/lift blobs.  A digest of the
compact merge summary alone is insufficient.

## 3. Exact target-independent preflight

Prepare plus the four complete character blocks, with their referenced
blobs, determine (2.3)--(2.7).  No grade-one physical merge row, target
coefficient, residual or pivot cache is needed.  Hence v444 constructs
\(H^{[2]}\), and v441 constructs the canonical grade-two fibre by
lower-first processing **every** lifted \(B_1\) row together with every
exhausted \(H^{[2]}\) row.

Before sealing this as a target-independent module state, the producer and
independent checker must bind and replay:

1. the split first-rung product and the zero multiplication cocycle of its
   chosen section;
2. the exact signed kernel action, retaining
   \(u_i\mapsto2u_{\sigma(i)}+u_{\sigma(i)}^2\) for every negative column;
3. all six occurrence matrices and their generally nonzero crossed cochains
   \(c_j\), with the crossed law rather than ordinary addition, all tag
   signs, fixed prefixes, and left/right conventions;
4. the pinned PB3 normal map, every translated PB3 boundary row, the PB4
   boundary/block quotient, and commutation with filtration, occurrence
   transport and physical aggregation; and
5. integral normalized-exponent divisibility before reduction modulo three,
   its actor action, and its presence in the lower block.

The zero multiplication cocycle in item 1 does not make the occurrence
crossed cochains in item 3 vanish.

The exact widths remain

\[
 36,288\ \text{per source character},\quad
 145,152\ \text{total source},\quad
 48,384\ \text{new physical},\quad
 32,260\ \text{lower/auxiliary}.                    \tag{3.1}
\]

All six degree-two monomials stay coupled inside each source character.  The
48,384-trit residual occupies 12,096 bytes in the registered packing.

## 4. Result-dependent join

Only an independently checked `FIRST_RUNG_GRADE1_MEMBER` supplies a legal
literal \(c_1\).  The consumer must independently evaluate the complete
difference through degree two,

\[
 \Delta_{\leq2}=T_{\leq2}-A_{\leq2}(c_1).           \tag{4.1}
\]

It first asserts that all 32,260 lower and auxiliary coordinates vanish.
Only then may it define

\[
 \rho_2=\operatorname{gr}_2(\Delta_{\leq2}),        \tag{4.2}
\]

and independently recompute its packed SHA-256, sparse digest and support.
It must bind the complete module-state ancestry and the checked grade-one
state/certificate as parents.  Reading the stored `next_degree2_residual`
blob or extracting its top block before the zero-lower assertion is not an
independent replay.

On a checked grade-one NONMEMBER, the result-dependent join is forbidden: a
degree-two correction reduces to zero below and cannot repair that failure.
The target-independent module state remains mathematically valid but has no
witness consequence for this branch.

## 5. Audited status

Task566 found no counterexample to the direct basis, 44-seed reconstruction,
old/new transition reconstruction, target independence or branch logic after
the repairs above.  Its reply is 15,828 bytes with SHA-256
`b8c04819a27906cfaa88534627c147307e1fb7b9429e1f1246fc518b72f2297a`.

```text
GRADE-ONE SOURCE CLOSURES: production-state claim external to this paper audit
AUTHENTICATED SPLIT STATES -> COMPLETE T1: paper-closed; actual direct replay required for cross-check
TARGET-INDEPENDENT GRADE-TWO MODULE: construction authorized; arithmetic/boundary/closure replay required
GRADE-TWO RESIDUAL / MEMBERSHIP: forbidden without a checked grade-one MEMBER and independently evaluated c1
ORDER-54,432 / FULL-Q0 / A0 / COMMON / COFINAL LIFT: not declared
FAKE / IHARA: not declared
LEAN VERIFIED: false
```

`R07_GRADE1_TO_GRADE2_SPLIT_PRESENTATION_HANDOFF_V451_PAPER`
