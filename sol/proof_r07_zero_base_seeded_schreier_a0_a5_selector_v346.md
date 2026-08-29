# R07 zero-base seeded Schreier A0/A5 selector (v346)

Author: Sol / 2026-08-29

Status: paper specialization and finite algorithm.  It composes the
cross-checked zero A3 seed of v343/v345 with the complete two-rung state of
v308.  Its new point is operational: after one accepted A0 word, the fallback
joint search needs neither another A0 column search nor enumeration of every
element of the full normal-closure image.  A Schreier kernel roster followed
by its complete `Q1` projection is sufficient.  No actual A0 word, A5
terminal, compatible lift, fake certificate, or Ihara witness is asserted.
`verified=false`.

## 1. Accepted zero-base data

Use v308's finite state group and invariant normal-closure image

\[
 \mathfrak G=U_0^+\times Q_1\times E_{\exp}^+,
 \qquad \mathcal C=\widehat\Psi(\Omega),
\tag{1.1}
\]

together with its homomorphism

\[
 \pi_0:\mathcal C\longrightarrow (Z_0/D_0)\oplus E_{\exp},
 \qquad \tau_0=(-T+D_0,0).
\tag{1.2}
\]

Condition on an independently accepted A0 word \(c_0\).  Literal replay in
the complete two-rung state gives

\[
 h_0=\widehat\Psi(c_0)=(v_0,q_0,0)\in\mathcal C,
 \qquad \pi_0(h_0)=\tau_0.
\tag{1.3}
\]

The cross-checked A3 result is the zero seed.  Thus v345 gives

\[
 \kappa_0=0,
 \qquad \mathcal S=(\ker\Phi)d_1,
\tag{1.4}
\]

where an accepted A4 word-bearing closure constructs \(\mathcal S\) without
an anchor, adapted basis, or local A3 base-pair roster.

Put

\[
 \mathcal K_0=\ker(\pi_0|_{\mathcal C}),
 \qquad P=\operatorname{pr}_{Q_1}(\mathcal K_0)\le Q_1.
\tag{1.5}
\]

## 2. Schreier generation of the A0 kernel

Let \(S_{\mathcal C}\) be a finite symmetric generating roster for the final
invariant subgroup \(\mathcal C\), with a literal v308 ancestry DAG for every
generator.  It is enough to retain subgroup generators and the four action
closure checks; no list of all elements of \(\mathcal C\) is assumed.

Let

\[
 A_0^{\rm im}=\pi_0(\mathcal C).
\tag{2.1}
\]

Run a frozen-order Cayley BFS only in the finite image \(A_0^{\rm im}\).  For
each \(a\in A_0^{\rm im}\), retain one word lift
\(t_a\in\mathcal C\), with \(t_1=1\) and \(\pi_0(t_a)=a\).  For
\(s\in S_{\mathcal C}\), define

\[
 r(a,s)=t_a s t_{a\pi_0(s)}^{-1}.
\tag{2.2}
\]

### Theorem 2.1 (ANCESTRY-BEARING SCHREIER KERNEL)

The finite roster

\[
 \mathcal R_0=\{r(a,s):a\in A_0^{\rm im},\ s\in S_{\mathcal C}\}
\tag{2.3}
\]

generates \(\mathcal K_0\).  Every member of \(\mathcal R_0\) has a literal
normal-closure ancestry obtained by concatenating the retained ancestries of
\(t_a,s,t_{a\pi_0(s)}^{-1}\).

#### Proof

Every element in (2.2) maps to one, so the generated subgroup lies in
\(\mathcal K_0\).  Conversely, write a kernel word as
\(s_1\cdots s_m\), with \(s_i\in S_{\mathcal C}\), and put
\(a_i=\pi_0(s_1\cdots s_i)\).  Since \(a_0=a_m=1\), the usual telescoping
rewriting gives

\[
 s_1\cdots s_m
 =\prod_{i=1}^m t_{a_{i-1}}s_i t_{a_i}^{-1}.
\tag{2.4}
\]

Every factor is in (2.3).  Expanding the stored word lifts proves the ancestry
statement. \(\square\)

Projection to the middle direct-product factor is a homomorphism.  Hence

\[
 \boxed{
 P=\left\langle
   \operatorname{pr}_{Q_1}(r):r\in\mathcal R_0
 \right\rangle.}
\tag{2.5}
\]

Thus constructing \(P\) requires the finite image transversal and a subgroup
closure in \(Q_1\), not enumeration of \(\mathcal C\).

## 3. Exact projected A0 fibre

### Theorem 3.1 (ALL A0 SUCCESSOR STATES FORM ONE `Q1` COSET)

The set of complete next-rung affine occurrence states of all registered A0
corrections is exactly

\[
 \boxed{
 \operatorname{pr}_{Q_1}\bigl(\pi_0^{-1}(\tau_0)\bigr)
 =q_0P.}
\tag{3.1}
\]

Moreover, a frozen-order enumeration of \(P\) can retain one literal A0 word
for every state in \(q_0P\).

#### Proof

Equation (1.3) and the homomorphism property give
\(\pi_0^{-1}(\tau_0)=h_0\mathcal K_0\).  Applying the middle-factor
projection gives

\[
 \operatorname{pr}_{Q_1}(h_0\mathcal K_0)
 =q_0\operatorname{pr}_{Q_1}(\mathcal K_0)=q_0P.
\tag{3.2}
\]

The generators (2.3) carry literal ancestry.  During the subgroup closure of
their projections, retain the same product/inverse edges.  Multiplying the
resulting kernel word by \(c_0\) supplies the claimed literal lift. \(\square\)

Keeping the full `Q1` tuple is load-bearing.  No merge by the coarse A0
column, by \(L_g(v)\), or by an already block-summed endpoint is used.

## 4. Zero-base joint selector

Let v308's deterministic literal relation map be

\[
 \mathscr B(q)=\operatorname{Rel}_g(q)-\operatorname{Rel}_g(1).
\tag{4.1}
\]

Because \(\kappa_0=0\), its joint criterion specializes to

\[
 \boxed{d_1-\mathscr B(q)\in\mathcal S.}
\tag{4.2}
\]

### Theorem 4.1 (SEEDED COMPLETE ZERO-BASE A0/A5 DECISION)

There is a registered literal A0 correction with an endpoint-compatible
pointed multiplier if and only if some

\[
 q\in q_0P
\tag{4.3}
\]

satisfies (4.2).  If the accepted slice ancestry gives

\[
 d_1-\mathscr B(q)=\theta d_1,
 \qquad \theta\in\ker\Phi,
\tag{4.4}
\]

then the multiplier is

\[
 \boxed{\mu_1=\theta.}
\tag{4.5}
\]

#### Proof

Theorem 3.1 says that (4.3) is exactly the complete set of successor states
of A0 words, with no missing or extraneous state.  V308 proves that
\(\mathscr B(q)\) reconstructs the literal task193 direct-change row and
that its predicate depends only on this full affine occurrence tuple.  V345
identifies the actual A5 slice with \(\mathcal S\) and removes the base-point
summand.  Substitution gives (4.2)--(4.5). \(\square\)

The map \(q\mapsto\mathscr B(q)+\mathcal S\) is not asserted to be a group
homomorphism.  Consequently the final test is a complete finite evaluation
over the distinct states in \(q_0P\), not an unsound linear-kernel shortcut.
One retained literal lift per `Q1` state is sufficient.

## 5. Witness-first execution and certificates

The exact order is:

1. test the accepted A0 word \(c_0\) immediately by evaluating (4.2) at
   \(q_0\);
2. only if it fails, authenticate the final invariant generator roster
   \(S_{\mathcal C}\);
3. compute the image transversal, the Schreier roster (2.3), and the
   projected subgroup \(P\);
4. enumerate each previously unseen state of \(q_0P\), reconstruct
   \(\mathscr B(q)\), and test (4.2); and
5. stop on the first MEMBER, retaining its literal A0 ancestry and slice
   ancestry for the v345 A6 factored-pair compiler.

A positive checker needs only the selected ancestry, the A0 boundary and
exponent replay, the complete `Q1` occurrence tuple, the task193 row, and the
A4 slice equality.  It need not reproduce the producer's enumeration order.

A complete negative must additionally certify the v308 invariant generator
closure, the image transversal, every Schreier generator, both containments
in (2.5), exhaustion of the finite coset \(q_0P\), and failure of (4.2) for
every distinct state.  Any unfinished closure or cap is `UNKNOWN_RESOURCE`.

If \(m=|A_0^{\rm im}|\) and \(s=|S_{\mathcal C}|\), the raw Schreier roster
has at most \(ms\) entries before subgroup reduction.  The fallback then
enumerates \(|P|\) complete successor states, rather than all
\(|\mathcal C|\) states, and never reruns the A0 column search.

## 6. Fixed frontier

```text
ZERO A3 BASE kappa0=0:                         CROSS-CHECKED
A4 SLICE S=(ker Phi)d1 WITHOUT ANCHOR:         PAPER PROOF / ACTUAL A4 PENDING
ONE ACCEPTED A0 WORD -> SEEDED A5 TEST:         PAPER PROOF / ACTUAL A0 PENDING
A0 KERNEL BY ANCESTRY-BEARING SCHREIER ROSTER: PAPER PROOF
ALL RELEVANT SUCCESSOR STATES = q0*P:           PAPER PROOF
FULL-C STATE ENUMERATION:                       REMOVED
SECOND A0 COLUMN SEARCH AFTER FIRST FAILURE:    REMOVED
ACTUAL q0 / P / TASK193 ROW / A5 TERMINAL:      NOT COMPUTED
A6 / EXACT PB ENDPOINTS / COFINAL LIFT:         NOT COMPUTED
FAKE / IHARA WITNESS:                           NOT CONSTRUCTED
```

`R07_ZERO_BASE_SEEDED_SCHREIER_A0_A5_SELECTOR_V346_PAPER_GRADE`
