# Sol(max) Reply 566: audit of the grade-one to grade-two split handoff

Author: Sol / 2026-09-03

## 0. Verdict

The algebraic handoff is sound, but v450 needs a local serialization and
preflight repair before it is safe as a production contract.  In particular,
the proof must distinguish the four full filtered word-sums from the four
idempotents on the associated grade, give the global reconstruction formulas
for the 44 seeds and old-row transitions, and import the complete v441/v443
arithmetic/boundary gates into the grade-two preflight.  These are
specification repairs; they do not require recomputing any completed
grade-one block and they do not require merge-only data.

Final verdict: `GRADE1_TO_GRADE2_HANDOFF_PASS_AFTER_REPAIR`.

## 1. Inputs and audit boundary

The designated v450 receipt matches exactly:

```text
bytes   7649
sha256  48acc55a73aba140aa73098791d73f936f1b46fc5316d6f56e668be242fdc630
```

The comparison receipts used were:

| input | bytes | SHA-256 |
|---|---:|---|
| v441 | 11,696 | `5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb` |
| v444 | 9,953 | `705afdc595f21f64356b70469a8444708b8a8c8e6306c218e942863a560ef645` |
| v446 | 9,262 | `389ceee1250b892ec4845753af23f4455e619e2d72782931645d8b8176764756` |
| v447 | 4,415 | `3e4bb3e498beb2c44cf3e1f0786ad83c7691312674967877b766e3e61bb496c2` |
| v448 | 5,881 | `168e3fc5ab38520faf8ed5d107013f1f8b53f22d2907032519b86b6e0f01182d` |
| v449 | 1,408 | `0237572f8ee949cdac8129cb9a9dae8c833b00baee2647c0deed194449577ff9` |
| Task 553 audit | 16,864 | `9e06ae4022e6267846561b13fed2f64a73909ba0d3b68436173763cf6bdba1df` |
| Task 558 audit | 22,080 | `b61962bf557c4790fc1d36dde49805527e245933300348c76970c5e7fc49cf6f` |
| Task 560 audit | 10,225 | `5ba42f2aadcf216a75df298d05657ce3fff27bbfd5c40226e6fcf2e7cee4ed64` |
| Task 563 audit | 10,772 | `753437f782bc02196bccdf44dd6e8e346945ca3d8d39444d17542649b9fe86a9` |

I also checked the relevant v3/v4 producer/checker schema at receipts
`bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff`,
`67f56ee92aea7e17ce88303657ca519ee9539269eef44e6e5550da63d6a4a012`,
`1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4`
and `ffd78b41fc9f7a1f59925eb8f07db7278b704c3580bb7e8fa3a586e85db9fe06`.
This was a static mathematical/schema audit, not an audit of the live GHA
artifacts.  I ran no GAP, Python computation, production phase, merge, GHA or
git command.  The counterexamples below are hand calculations.

## 2. Required checks, in order

### F1. The eight basis pieces do give a direct basis, with one notation repair

Let

\[
 C=((0,0),(0,1),(1,0),(1,1)),\qquad
 P_\chi=\sum_{a\in C}\chi(a)L_{w_a}^{\leq1},
\]

where `w_a` is the exact v447/`PURE_Q1_WORDS` word and
\(w_{(0,0)}\) is empty.  The operators \(P_\chi\) are the operators actually
used to form the precision-one projected seeds.  They reduce to the legal
degree-zero character projectors, but v447 proves idempotence only for their
restrictions \(e_\lambda\) to a pure associated grade.  No idempotence of
\(P_\chi\) on the full filtered module is needed or may be inferred.

The old lifted rows are independent modulo the pure grade: if
\(\sum c_{\chi i}\widetilde b_{\chi i}\in\ker r_0\), reduction gives
\(\sum c_{\chi i}b_{\chi i}=0\), and the union of the four \(B_{0,\chi}\)
is a basis, so every coefficient is zero.  V444 gives spanning by the old
lifts plus the defect closure.  Inside the kernel, the genuine associated-
grade idempotents of v447 give
\(H_1=\bigoplus_\lambda H_{1,\lambda}\).  Therefore the roster (2.1) is a
direct basis of \(U_1\).

A small trap shows why the distinction matters.  On a filtered space
\(L\oplus G\), let \(E_0,E_1\) select the two character coordinates in both
\(L\) and \(G\), and let \(N:L\to G\) send the first lower coordinate to the
first grade coordinate.  Then
\(P_0=E_0+N\), \(P_1=E_1-N\) reduce to the right quotient projectors and
sum to the identity, but neither need be idempotent (the lower-to-grade block
of \(P_0^2\) is \(2N\), not \(N\)).  V450's directness proof survives because
it uses reduction and the pure-grade \(e_\lambda\), not full filtered
idempotence.

### F2. The records determine the 44 original seeds

Character orthogonality gives an exact identity on the full filtered module,
even though the \(P_\chi\) need not be projectors:

\[
 \sum_\chi P_\chi
 =\sum_{a\in C}\left(\sum_\chi\chi(a)\right)L_{w_a}^{\leq1}
 =4L_{w_{(0,0)}}^{\leq1}=1
 \quad\text{in }\mathbf F_3.                         \tag{R1}
\]

Thus summing the four exact projected relations reconstructs each one of the
44 original seeds.  The state does not merely provide 176 unrelated seed
relations.  V450 should replace its use of \(\sum e_\chi=1\) at this point by
(R1); \(e_\chi\) is reserved for the pure-grade operator.

Without (R1), four arbitrary lifts of quotient projections could sum to
\(1+N\), and the 176 relations would not recover the original 44.  The empty
word and the four-character sum rule exclude exactly that counterexample.

### F3. Old-row transitions, signs, words and global indices

Use the serialized orders

```text
characters: ((0,0),(0,1),(1,0),(1,1))
actors:     (1,-1,2,-2)
```

and write \(r_\chi=|B_{0,\chi}|\),
\(n_\lambda=|H_{1,\lambda}|\), and

\[
 R=\sum_\chi r_\chi,\quad
 O_\chi=\sum_{\kappa<\chi}r_\kappa,\quad
 N_\lambda=R+\sum_{\mu<\lambda}n_\mu,\quad
 D_\chi=\sum_{\kappa<\chi}(44+4r_\kappa).           \tag{R2}
\]

Indices \(i,j,t\) below are zero-based and seed labels \(a\) are one-based.
The prepare origin indices are exactly

\[
 o_s(\chi,a)=D_\chi+a-1,
 \qquad
 o_t(\chi,i,t)=D_\chi+44+4i+t.                      \tag{R3}
\]

Let \(q^s_{\chi,a,i}\) be `seed_reductions[a-1]`, let
\(q^A_{\chi,i,t,j}\) be `actor_transitions[i][t]`, and let
\(R_{\lambda,o,j}\) be block \(\lambda\)'s
`origin_reductions[o]`.  With the global basis indices of (R2), the complete
relations are

\[
 s_a^{(1)}=
 \sum_{\chi,i}q^s_{\chi,a,i}B_1[O_\chi+i]
 +\sum_{\chi,\lambda,j}R_{\lambda,o_s(\chi,a),j}
                            B_1[N_\lambda+j],        \tag{R4}
\]

\[
 A_t\widetilde b_{\chi,i}=
 \sum_jq^A_{\chi,i,t,j}B_1[O_\chi+j]
 +\sum_{\lambda,j}R_{\lambda,o_t(\chi,i,t),j}
                            B_1[N_\lambda+j].        \tag{R5}
\]

Both defect terms have a **plus** sign in (R4)--(R5), because the packet row
is defined as the lifted left side minus its old reduction.  The minus signs
occur inside the literal expansion of that packet.  The inner full filtered
word-sum uses `PURE_Q1_WORDS`; the outer packet split uses the restriction of
the same words to the pure grade.  All four \(\lambda\) reductions must be
summed.  A one-dimensional relation
\(A\widetilde b=q\widetilde b+\delta\) is already a counterexample to either
dropping a block or changing the displayed plus sign.

### F4. New-row transitions and literal DAGs

For a new row the relation is simply

\[
 A_t h_{\lambda,i}
   =\sum_jp_{\lambda,i,t,j}B_1[N_\lambda+j],         \tag{R6}
\]

where \(p\) is `actor_transitions[i][t]` in that block.  The audited schema
requires four entries for every retained row and binds their direct replay.

The old and block bases are insertion-ordered.  Every actor parent and every
reduction edge of an accepted node points to an earlier pivot.  If candidate
\(z\) has earlier reduction coefficients \(c_p\), its stored scale means

\[
 h_j=\sigma_j\left(z-\sum_{p<j}c_ph_p\right),
 \qquad \sigma_j\in\{1,2\}.                         \tag{R7}
\]

Old roots expand to projected seeds.  Block roots expand to a specified seed
or transition defect; the latter expands using (1.2), with its old reduction
subtracted.  Actor nodes prepend the recorded actor, and character nodes
prepend the exact v447 word with its character coefficient.  Therefore the
DAGs are well founded and literal-bearing.  Authentication of a DAG digest
alone is not enough: the grade-two consumer must replay (R4)--(R7) against
the referenced basis/lift blobs, as v450 Corollary 2.2 already requires.

### F5. No merge-only datum is needed

Prepare plus all four complete blocks determine \(B_1\), all 44 seed
relations, every generator transition and every literal lift.  V444 then
constructs the precision-two seed and transition defects and their exhausted
closure \(H^{[2]}\).  Reprocessing **all** lifted \(B_1\) rows together with
all \(H^{[2]}\) rows through the lower-first physical echelon determines the
fibre.  The merge target, target solution, stored physical residual and
merge-only pivot cache are not mathematical inputs to any of these steps.

The word "all" is load-bearing.  For a hand counterexample, take two old
source rows whose lower physical images both equal \(\ell\), while their new
grade images are \(g_1\) and \(g_2\), and take \(H^{[2]}=0\).  Lower-first
elimination produces the fibre row \(g_2-g_1\).  Keeping only an old physical
pivot or only \(H^{[2]}\) loses it.  V450 step 3.5 includes both old lifted
rows, so it passes; no merge cache has to be imported.

Likewise, a span generated by \(r\otimes(m_1+m_2)\) need not contain either
\(r\otimes m_1\) or \(r\otimes m_2\).  V450 correctly keeps the six
degree-two monomials coupled rather than making an illegal monomial split.

### F6. The canonical grade-two fibre is target-independent

For the fixed source module and fixed arithmetic/boundary map,
\(E_d=\operatorname{im}C_d\) and
\(K_d=\ker(E_{d+1}\to E_d)\) do not mention a target or a chosen lower
solution.  Equivalently, v441 identifies
\(K_d\cong D_d/D_{d+1}\).  The affine residual class of a checked \(c_1\)
is result-dependent, but the linear fibre against which it is reduced is
not.  V450's target-independent prebuild claim is therefore correct, subject
to the arithmetic and boundary bindings in F8.

### F7. Dimension audit

The four requested counts are exact:

\[
 6\text{ tags}\cdot2\text{ Fox components}\cdot504
 \cdot6\text{ degree-two monomials}=36,288
\]

per source character, hence \(4\cdot36,288=145,152\) source coordinates.
The joint new physical width is
\(4\cdot2016\cdot6=48,384\).  The lower block is

\[
 8,064+24,192+4=32,260,
\]

where the last four coordinates are the two physical PB3 augmentations and
two normalized exponents.  Four base-3 trits per byte gives exactly
\(48,384/4=12,096\) bytes.  These are coordinate widths only, not ranks,
memory peaks or runtime bounds.

### F8. Independent \(\rho_2\) and missing preflight gates

Equation (4.1) has the right dependency, but "from the literal word" is not
yet a complete fail-closed contract.  On a checked MEMBER artifact, the
grade-two consumer must independently evaluate the complete precision-
through-degree-two difference

\[
 \Delta_{\le2}=T_{\le2}-A_{\le2}(c_1),              \tag{R8}
\]

first assert that all 32,260 lower/auxiliary coordinates vanish, and only
then define \(\rho_2=\operatorname{gr}_2(\Delta_{\le2})\), pack it, and
recompute its packed digest, sparse digest and support.  Extracting a stored
top block before that zero-lower assertion is not independent replay.

Both the module prebuild and (R8) must bind and replay the v441/v443 data:

1. the split first-rung product, with its multiplication-section cocycle
   explicitly asserted to be zero for the chosen section;
2. the exact signed kernel action, including
   \(u_i\mapsto2u_{\sigma(i)}+u_{\sigma(i)}^2\) for a negative column;
3. every occurrence map's matrices and crossed cochain \(c_j\), not an
   ordinary additive surrogate, together with all six tags, signs, fixed
   prefixes and left/right conventions;
4. the pinned PB3 normal map and every translated PB3 boundary row, the PB4
   boundary/block quotient, and commutation with filtration, occurrence
   transport and aggregation; and
5. integral normalized-exponent divisibility before reduction mod 3, its
   fixed actor action, and its presence in the lower block.

The zero multiplication cocycle of the split first rung must not be confused
with the generally nonzero occurrence crossed cochains.  These are
target-independent compatibility gates and can be sealed once in the module
state; they are not a request for a new mathematical design or an additional
target-dependent solve.  The result join additionally binds the checked
grade-one terminal and literal \(c_1\) as parents.

### F9. NONMEMBER branch

A checked grade-one NONMEMBER means that no \(c_1\) exists on the registered
lower solution locus.  A degree-two correction reduces to zero at the lower
precision, so it cannot repair that failure.  The result-dependent join and
any grade-two residual/membership assertion are therefore forbidden.  The
already sealed source module, \(\mathcal T_1\), \(H^{[2]}\) and canonical
linear fibre remain valid target-independent objects.  V450's branch logic
is correct.

### F10. Claim boundary

The mathematical theorem is paper-closed after the repairs below.  This
static audit did not authenticate or independently replay the live completed
split artifacts, so it does not promote their producer status to
cross-checked.  A concrete \(\mathcal T_1\) becomes cross-checked only when an
independent consumer authenticates the actual prepare/four-block parents and
directly replays (R1)--(R7).  A concrete grade-two module is merely authorized
here; it becomes cross-checked only after its independent arithmetic,
boundary, closure and lower-first replay.  None of these statements is a
Lean proof.  The existing-checker sentence in v450 section 4 must be read
conditionally ("on a checked MEMBER artifact"), not as a report that the
still-live terminal has already returned MEMBER.

## 3. Exact minimal replacement text for v450

The following four insertions/replacements are sufficient; no production
state or merge rework is requested.

1. In sections 1--2, reserve \(e_\lambda\) for the pure associated grade,
   define the full filtered word-sums \(P_\chi\) above, and replace the seed
   sentence by:

   > The precision-one projected seed is \(P_\chi s_a^{(1)}\).  The
   > \(P_\chi\) are not assumed idempotent.  Nevertheless their exact word
   > formula and \(w_{(0,0)}=1\) give \(\sum_\chi P_\chi=1\) by character
   > orthogonality in \(\mathbf F_3\).  Hence summing the four relations
   > reconstructs the original seed.  Directness of the new blocks uses only
   > the genuine associated-grade idempotents \(e_\lambda\).

2. After Theorem 2.1, insert (R2)--(R7), with the serialized character and
   actor orders displayed.  State explicitly that defect coordinates enter
   (R4)--(R5) with plus sign, that `origin_reductions` is summed over all four
   blocks, and that a consumer directly replays every equality and literal
   expansion.

3. Replace the first paragraph of section 4 by (R8), the 32,260-coordinate
   zero-lower/auxiliary assertion, and gates F8.1--F8.5.  Then recompute and
   bind packed/sparse/support receipts and both the module-state and checked
   grade-one parents.  Phrase the existing first-grade checker sentence
   conditionally on an actual checked MEMBER artifact.

4. Replace section 5 by:

```text
GRADE-ONE SOURCE CLOSURES: production-state claim external to this paper audit
AUTHENTICATED SPLIT STATES -> COMPLETE T1: paper-closed; actual direct replay required for cross-check
TARGET-INDEPENDENT GRADE-TWO MODULE: construction authorized; arithmetic/boundary/closure replay required
GRADE-TWO RESIDUAL / MEMBERSHIP: forbidden without a checked grade-one MEMBER and independently evaluated c1
ORDER-54,432 / FULL-Q0 / A0 / COMMON / COFINAL LIFT: not declared
FAKE / IHARA: not declared
LEAN VERIFIED: false
```

## 4. Final claim boundary

This audit establishes no grade membership.  It establishes no A0, COMMON,
cofinal lift, fake or Ihara conclusion.  It does not convert a candidate or
cross-checked artifact into a Lean-verified theorem.

`GRADE1_TO_GRADE2_HANDOFF_PASS_AFTER_REPAIR`
