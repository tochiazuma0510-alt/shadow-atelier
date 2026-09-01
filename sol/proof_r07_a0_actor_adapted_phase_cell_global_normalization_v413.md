# R07 A0 actor-adapted phase-cell global normalization (v413)

Author: Sol / 2026-09-01

Status: paper implementation theorem strengthening v409--v412.  It gives an
exact finite successor for every post-rank-rise dual, including nonzero
`tau`, context coordinates 3--9, and nonzero exponent constants.  It also
records the necessary coordinate-rebase rule: the current least-transversal
PB3 dual must not simply be reinterpreted in actor-adapted coordinates.  No
actual A0 terminal, common word, compatible lift, fake, or Ihara witness is
asserted.  `verified=false`.

## 1. Actor-adapted PB3 coordinates require a replay, not a relabeling

Let

\[
 N_3^{\rm old}:C_3\longrightarrow Y_3^{\rm old}
\tag{1.1}
\]

be v12's present PB3 normal map, whose central-orbit representative is the
least serialized element.  Let

\[
 \kappa_3=\text{the }A_{13}\text{ PC coordinate},\qquad
 H_{3,0}=\ker\kappa_3,
\tag{1.2}
\]

and let \(N_3^{\rm ad}\) be the same triangular contraction with the unique
split representative

\[
 h=h_0z_3^{\kappa_3(h)},\qquad h_0\in H_{3,0}.
\tag{1.3}
\]

V411's finite PC gates give that \(\kappa_3\) is additive,
\(\kappa_3(z_3)=1\), and (1.3) reconstructs every input.  The proof of v401's
normal-map theorem uses one representative in each central orbit but not the
least-serialization order.  Consequently

\[
 \ker N_3^{\rm old}=D_3=\ker N_3^{\rm ad}.
\tag{1.4}
\]

### Lemma 1.1 (SAFE ACTOR-ADAPTED REBASE)

There is a unique linear isomorphism

\[
 C_3:\operatorname{im}N_3^{\rm old}
       \stackrel{\sim}{\longrightarrow}
       \operatorname{im}N_3^{\rm ad},\qquad
 C_3(N_3^{\rm old}v)=N_3^{\rm ad}v.
\tag{1.5}
\]

After adjoining the unchanged second PB3 block, PB4 block, and normalized
exponent pair, the resulting isomorphism \(C\) carries every old physical
column and the old target to its actor-adapted counterpart.  Hence it
preserves ranks and the A0 span-membership question.

#### Proof

Equality of kernels in (1.4) makes (1.5) well-defined and injective; it is
surjective by its definition on the image.  Direct sums with unchanged
blocks remain isomorphisms.  Applying one isomorphism to a target and every
column preserves all linear dependences and target membership. \(\square\)

This lemma is not permission to keep an old sparse dual byte string.  A
change of representative cyclically changes the local `u0/u1` coordinates;
an old global `tau` functional can therefore acquire many localized terms.
The safe implementation boundary is:

1. construct a versioned actor-adapted quotient owner;
2. rebuild the target and the 44 identity compact rows from the frozen raw
   owner;
3. replay every retained correction from `(seed_index,delta_word)` and every
   retained action from its family/translation source; and
4. recompute pivots, remainder, and dual in the new coordinates.

The word-bearing ladder checkpoint makes this a finite replay.  Old row
digests, pivots, and dual bytes are not copied into the new checkpoint.

## 2. The full formula on an exponent cell

Keep v402's already actor-adapted PB4 split.  In the PB3 split (1.3), every
PB3 actor has central phase zero.  In PB4, v411's literal five-context table
shows that every actor phase is either zero or

\[
 \epsilon(\delta)=\operatorname{exp}_x(u_\delta)\pmod 3.
\tag{2.1}
\]

For an arbitrary current physical dual, v410 supplies the localized adjoint
from its finite radius-one reverse neighbourhood.  V411 supplies the global
`tau` contribution by the three central translates.  Thus every compact seed
has the exact formula

\[
 F_i(\delta)=K_{i,\epsilon(\delta)}+
 \sum_{(j,t)\in R_i}c^{(i)}_{j,t}
      {\bf1}_{\pi_j(\delta)=t}.
\tag{2.2}
\]

All eleven occurrences are merged before zero deletion.  Contexts 0--9 are
allowed.  The three constants include normalized exponents and all three
`tau` coefficients.  As in v409, every nonzero formula value is accepted only
after a fresh literal conjugate, ten linked coordinates, eleven raw Fox
occurrences, actor-adapted physical transform, and direct dual pairing agree.

Put

\[
 C_e=\{\delta\in\Delta:\epsilon(\delta)=e\},\qquad
 |C_e|=|\Delta|/3=119{,}042{,}784.
\tag{2.3}
\]

For a fixed formula define its exact support union in the cell

\[
 U_{i,e}=\{\delta\in C_e:\pi_j(\delta)=t
       \text{ for some }(j,t)\in R_i\}.
\tag{2.4}
\]

V142's canonical singleton section and the authenticated kernel rosters of
orders \((9,9,9,9,9,1,1,1,3,3)\) enumerate every fibre in (2.4).  Filter by
\(\epsilon=e\) and deduplicate by the full ten-coordinate tuple.  This gives
the exact finite set \(U_{i,e}\), not only a union bound.

## 3. Three-to-one normalization of the existing global roster

Let \(\bar x\in\Delta\) be the image of \(x\), so
\(\epsilon(\bar x)=1\).  Define

\[
 \nu(\delta)=\bar x^{-\epsilon(\delta)}\delta\in\ker\epsilon.
\tag{3.1}
\]

### Lemma 3.1 (THREE-TO-ONE GLOBAL NORMALIZER)

Every fibre of \(\nu\) has at most three elements.  Consequently, from any
\(3N\) distinct entries of the authenticated global \(\Delta\)-roster one can
construct at least \(N\) distinct literal states in every cell \(C_e\).

#### Proof

If \(\nu(\delta)=h\), then

\[
 \delta=\bar x^{\epsilon(\delta)}h.
\tag{3.2}
\]

There are only the three possible values of \(\epsilon(\delta)\), so a fibre
has size at most three.  Pigeonhole gives at least \(N\) distinct normalized
states from \(3N\) distinct roster entries.  Left multiplication by
\(\bar x^e\) is injective and carries them into \(C_e\).  If a roster entry
has literal section word \(w\), the literal word

\[
 x^e x^{-\epsilon(w)}w
\tag{3.3}
\]

realizes the constructed state, and its ten-coordinate tuple is checked
directly. \(\square\)

No new BFS is needed.  When \(N\leq |C_e|\), the bound \(3N\leq|\Delta|\)
fits inside the already authenticated global roster.

## 4. Complete phase-cell selector

### Theorem 4.1 (EXACT SUPPORT-UNION PHASE SELECTOR)

For every compact seed \(i\) and phase \(e\), complete enumeration of
\(U_{i,e}\), followed when necessary by Lemma 3.1, decides whether
\(F_i\) is nonzero on \(C_e\):

1. Evaluate every state of the exact set \(U_{i,e}\).  If any value is
   nonzero, return its literal word.
2. If all those values are zero and \(K_{i,e}=0\), then \(F_i\) is zero on
   the whole cell.
3. If all are zero, \(K_{i,e}\ne0\), and
   \(|U_{i,e}|<|C_e|\), use the first
   \(3(|U_{i,e}|+1)\) global-roster entries in Lemma 3.1.  Among the resulting
   \(|U_{i,e}|+1\) distinct cell states, one lies outside \(U_{i,e}\), where
   the formula equals the nonzero constant \(K_{i,e}\).
4. If \(|U_{i,e}|=|C_e|\), step 1 was already a complete cell evaluation.

#### Proof

By definition (2.4), every indicator in (2.2) vanishes outside
\(U_{i,e}\), so the formula is the constant \(K_{i,e}\) there.  This proves
steps 1, 2, and 4.  In step 3, Lemma 3.1 supplies more distinct cell states
than the cardinality of the support union; at least one is outside it and has
value \(K_{i,e}\ne0\). \(\square\)

The practical global-prefix cap is

\[
 3(|U_{i,e}|+1)\leq 3(W_{i,e}+1),
\tag{4.1}
\]

where the right side is the old fibre-order union bound.  Unlike a heuristic
prefix, the factor-three bound is a proof of sufficient distinctness.

## 5. Consequence for the rank ladder

At a nonzero remainder, run the unchanged complete six-action oracle.  If it
is empty, compile (2.2), apply Theorem 4.1 to all at-most-44 seeds and three
cells, and insert the first directly replayed nonzero column.  Such a column
pairs nontrivially with the current separating dual, hence raises physical
rank.  If every seed is zero in every cell, the same dual annihilates the
entire compact correction space and, together with the empty six-action
oracle, is an exact separator.  Finite physical dimension therefore gives a
complete decision after finitely many strict rises.

This removes the mathematical need for the present implementation stops

```text
NONZERO_TAU_PHASE_SELECTOR
SELECTOR_COORDINATES:S3...S9
NONZERO_CONSTANT_SELECTOR
SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION
```

but it does not retrospectively change a terminal returned by the current
tau-free v3 producer.  Promotion still requires a versioned actor-adapted
producer and an independent checker that separately rebuilds the rebase,
support unions, factor-three cell prefixes, literal rows, and positive or
separator terminal.

```text
CURRENT TAU-FREE LADDER:              UNCHANGED / ACTUAL RUN PENDING
ACTOR-ADAPTED PB3 REBASE:             FINITE WORD-BEARING REPLAY
LOCALIZED ADJOINT:                    v410 RADIUS-ONE
GLOBAL TAU:                           v411 THREE CENTRAL PHASES
CONTEXT COORDINATES:                  ALL 0--9
NONZERO CELL CONSTANT:                <= 3*(|U_e|+1) GLOBAL PREFIX
FULL COMPACT ORACLE:                  FINITE ON EVERY DUAL ROUND
ACTUAL A0 MEMBER/NONMEMBER:           NOT YET COMPUTED
COMMON / FAKE / IHARA WITNESS:        NONE
```

`R07_A0_ACTOR_ADAPTED_PHASE_CELL_GLOBAL_NORMALIZATION_V413_PAPER_GRADE`
