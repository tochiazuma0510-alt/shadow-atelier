# R07 actual singleton coarse-inverse selector v142

Date: 2026-08-27
Role: Sol mathematical proof / finite actual-class selector

## 1. Scope and authenticated premise

This note concerns only the frozen task176 finite quotient.  It does not
claim a cofinal theorem.

Write (Q_0) for the canonical positive shortlex section group, with

\[
 |Q_0|=1,469,664,
\]

and write

\[
 \sigma_i:Q_0\longrightarrow E_i,\qquad 0\leq i<10,
\]

for the ten section-coordinate homomorphisms reconstructed in task176.  Here
(E_i=E_3) for (i<5) and (E_i=E_4) for (i\geq5).  Let
(kappa_i(q)) be the packed permutation (the coarse part) of
(sigma_i(q)).

The cross-checked task176 production receipt from run `33044121344`, receipt
SHA-256
`715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41`,
records for every (i=0,\ldots,9):

```text
q0_state_count       = 1,469,664
distinct_coarse_keys = 1,469,664
bucket_size_min      = 1
bucket_size_max      = 1
```

Thus each (kappa_i) is injective on the actual (Q_0) roster.  This is a
finite cross-checked premise, not a Lean-verified statement.

For each coordinate put

\[
 A_i=\pi_i(\Gamma)\leq E_i.
\]

Task176 gives a lossless table of (A_i), in first-Gamma-state order, and
literal source words for the corresponding Gamma states.

## 2. The selector

For a packed target (t\in E_i), perform the following finite operation.

1. For every distinct (a\in A_i), in its authenticated Gamma-state order,
   form
   \[
   s_a=a^{-1}t.
   \]
2. Look up the coarse key of (s_a) in the injective table
   \(kappa_i(Q_0)\).  If it is absent, discard (a).  If it is present,
   let (q_a) be its unique preimage.
3. Retain ((q_a,a)) only when the complete packed equality
   \[
   a\,\sigma_i(q_a)=t
   \]
   holds.  The full check includes the PC component and is not inferred from
   coarse equality.
4. If no pair remains, return `EMPTY`.  Otherwise choose the least pair
   ((\operatorname{id}(q_a),\operatorname{id}_\Gamma(a))) lexicographically
   and return the literal word
   \[
   u_{i,t}=u_\Gamma(a)\,u_{Q_0}(q_a).
   \]

The lexicographic convention agrees with the old exhaustive selector:
"first Q0 state, then first Gamma state".

## 3. Correctness theorem

**Theorem 3.1 (actual singleton selector).**  For every coordinate (i) and
every packed (t\in E_i), the algorithm in Section 2 returns `EMPTY` exactly
when the singleton fibre

\[
 \{\delta\in \Gamma Q_0:\pi_i(\delta)=t\}
\]

is empty.  On success its literal word evaluates to the returned ten-tuple
and its (i)-th coordinate is exactly (t).

**Proof.**  Every element of the linked section roster has the form
(a\sigma(q)), with (a\in\Gamma) and (q\in Q_0).  In coordinate (i),

\[
 a_i\sigma_i(q)=t
 \quad\Longleftrightarrow\quad
 \sigma_i(q)=a_i^{-1}t.
\]

If a solution exists, the corresponding (a_i\in A_i) is visited.  Its
right-hand side has coarse key (kappa_i(q)); injectivity of (kappa_i)
therefore returns that unique (q), and the complete packed equality accepts
it.  Conversely, every accepted pair satisfies the displayed equality, so
the concatenated Gamma and Q0 section words give a genuine linked preimage.
The final literal ten-coordinate replay proves the asserted word statement.
The least-pair rule makes the answer deterministic.  ∎

## 4. Certified implementation form

The inverse coarse table need not be a Python dictionary and need not be
trusted.  A bounded open-addressed table may store only `qid+1`:

```text
slot = hash(coarse_key) & mask
while slot occupied:
    compare the exact coarse bytes at the stored qid
    if equal: return that qid
    slot = (slot + 1) & mask
```

For (N=1,469,664), the fixed table length (2^{22}=4,194,304) has load
less than (0.351).  One unsigned 32-bit `qid+1` table therefore costs
exactly 16,777,216 bytes per coordinate, or 167,772,160 bytes for all ten.
Hash collisions cannot change an answer because every apparent hit is
resolved by exact coarse-byte comparison, followed by the full packed group
equality and the literal ten-coordinate word replay.  The hash seed affects
only slot layout, not the selected `(qid,gid)`.

Construction must insert all (N) qids in increasing order and reject any
second qid with the same exact coarse key.  Hence the live run independently
replays the task176 singleton premise while building the index.

## 5. Consequence for the common-word dovetail

Task179's canonical support-fibre step may replace one full (Q_0) scan per
target by:

\[
 O(|Q_0|)\text{ once per used coordinate}
 \quad+\quad O(|A_i|)\text{ exact lookups per target},
\]

where (|A_i|\leq243).  This preserves the v139/v140 positive schedule and
changes no admissible column.  It supplies a uniform actual-class singleton
selector; it does not by itself solve simultaneous multi-coordinate fibres,
the augmented (d+\rho z) saturation, cofinal compatibility, fake, or the
Ihara witness.

`R07_ACTUAL_SINGLETON_COARSE_INVERSE_SELECTOR_V142_PAPER_GRADE`
