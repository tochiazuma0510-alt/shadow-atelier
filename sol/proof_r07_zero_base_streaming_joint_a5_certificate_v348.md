# R07 zero-base streaming joint A5 certificate

Date: 2026-08-29

Status: paper theorem and implementation refinement of v345.  It changes no
mathematics and does not claim that the actual A4/A0 inputs have passed.

## 1. Setup

Keep v345's pre-`C` complete closure

\[
 \widehat L=
 \{(\theta d_1,\theta\mathbin\odot w):\theta\in I\}
 \subset V\oplus W .
\tag{1.1}
\]

Define the linear map

\[
 T:V\oplus W\longrightarrow V\oplus W_C,
 \qquad T(a,b)=(a,Cb).
\tag{1.2}
\]

For the literal task193 row `e1=e1(c)`, put

\[
 t=(e_1,0).
\tag{1.3}
\]

The action closure must still be computed on the full pre-`C` pairs in
(1.1).  This note does **not** close only their `C`-images.

## 2. Joint-image criterion

**Theorem 2.1 (STREAMING JOINT ZERO-BASE TEST).**

\[
 \boxed{e_1\in Hd_1\quad\Longleftrightarrow\quad
        (e_1,0)\in T(\widehat L).}
\tag{2.1}
\]

**Proof.**  If `e1=theta*d1` for `theta in H`, then `theta in I` and
`Phi(theta)=C(theta odot w)=0`.  Hence

\[
 T(\theta d_1,\theta\mathbin\odot w)=(e_1,0).
\]

Conversely, every element of `T(Lhat)` has the form

\[
 (\theta d_1,C(\theta\mathbin\odot w)),\qquad\theta\in I.
\]

Equality with `(e1,0)` gives `Phi(theta)=0`, hence `theta in H`, and its
first coordinate gives `e1=theta*d1`.  QED.

Thus v345's operation "take the nullspace of the occurrence component and
then project its first coordinate" is algebraically equivalent to one joint
membership query.  No explicit basis of `Hd1` is required.

## 3. Exact streaming algorithm

Maintain two independent echelons.

1. `E_pre` stores full pairs `(a,b)` and owns the marked-action closure
   queue.  A successor is enqueued only when it raises the rank of `E_pre`.
2. Whenever `E_pre` accepts a new row `v_j=(a_j,b_j)`, insert
   `T(v_j)=(a_j,C b_j)` into `E_joint`, retaining the complete ancestry from
   the original A4 word-bearing seed through every marked action.
3. Reduce `t=(e1,0)` against `E_joint` after each accepted pre-`C` row.

There are two sound terminals.

- If the remainder becomes zero, the joint coefficients give immediately

  \[
   (e_1,0)=\sum_j q_jT(v_j)
            =T\!\left(\sum_jq_jv_j\right).
  \tag{3.1}
  \]

  This is an A5 MEMBER certificate.  It is safe to stop before closure queue
  exhaustion: the displayed finite combination already proves
  `e1=theta*d1` and `Phi(theta)=0`.
- If and only if the full `E_pre` action queue is exhausted, a nonzero
  remainder and its independently replayed dual give A5 NONMEMBER.  Before
  exhaustion, a nonzero remainder is only `UNKNOWN`.

The crucial ordering is

```text
full pre-C rank test and action enqueue
    -> apply C to that accepted row
    -> joint target reduction.
```

Applying `C` before the pre-`C` rank/action decision is forbidden because it
can collapse rows whose successors are needed for completeness.

## 4. A6 ancestry is already the membership ancestry

For each accepted pre-`C` row retain its expansion in the original A4 seeds

\[
 v_j=\sum_{i,A}a_{j,i,A}\,
      A\bigl((k_i-1)d_1,(k_i-1)\mathbin\odot w\bigr).
\tag{4.1}
\]

Substituting (4.1) into a positive combination (3.1) gives directly

\[
 \theta=\sum_{j,i,A}q_j a_{j,i,A}\,A(k_i-1).
\tag{4.2}
\]

Each nonzero summand is therefore already in v345's canonical A6 language

```text
(coefficient, prefix_DAG_node, original_A4_kernel_word_index).
```

No nullspace-basis change, anchor term, adapted A4 basis, or local A3
base-pair back-substitution is needed.  Collection modulo 3 may remove equal
factored terms, but their zero-deletion provenance must be retained.

## 5. Independent checker contract

The checker independently reconstructs both echelons from the authenticated
A4 words, task198 actions/occurrences, and literal task193 `e1`.  On MEMBER
it need only replay the finite ancestry (3.1), both coordinates, every
pre-`C` action edge used by that ancestry, and the resulting A6 factored
records.  It need not exhaust unused closure branches to validate a positive
certificate.

On NONMEMBER it must additionally replay queue exhaustion, the complete
`E_joint` span, and the separating dual.  Resource exhaustion before that
point is typed `UNKNOWN_RESOURCE`, never NONMEMBER.

This refinement makes the actual positive route witness-first:

```text
accepted A4 seeds + literal e1
 -> streaming full pre-C action closure
 -> first joint membership hit
 -> theta=mu1 and factored A6 ancestry.
```

`R07_ZERO_BASE_STREAMING_JOINT_A5_CERTIFICATE_V348_PAPER_GRADE`

