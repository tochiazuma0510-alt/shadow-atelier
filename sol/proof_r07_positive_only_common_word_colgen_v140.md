# R07 positive-only common-word column generation v140

Author: Sol / 2026-08-27

Status: paper proof and production contract.  This note specializes the
v139 fibre selector to the certificate actually needed for the R07 explicit
witness.  It separates discovery from verification: the producer may use a
bounded heuristic/dovetail to find rank-increasing columns, while a positive
receipt is checked by replaying only the retained columns and the final
linear identity.  Exhaustive moment or cell enumeration is unnecessary on a
successful branch.  No common word, cofinal lift, fake, or Ihara witness is
declared here.

## 1. The raw defect map on the joint kernel

Let \(F=\langle x,y\rangle\), let \(g=g_{760}\), and let \(\Omega\) be the
registered joint kernel generated normally by the 6,441 word-bearing rows
\(r\in\mathcal R_\Omega\).  Put

\[
 Z=Z_{H_1}\oplus Z_{H_2}\oplus Z_P\oplus\mathbf F_3^2
\tag{1.1}
\]

with the three block tags and two exponent coordinates retained literally.
Let

\[
 D=D_{H_1}\oplus D_{H_2}\oplus D_P\oplus0\oplus0\subseteq Z
\tag{1.2}
\]

be the complete translated PB3/PB4 boundary image.  Task175's direct Fox
replay defines the raw defect map

\[
 \mathscr V:\Omega\longrightarrow Z.
\tag{1.3}
\]

This map is additive on \(\Omega\).  Indeed, the Fox product rule in any one
of the ten contexts has the form

\[
 \partial(ab)=\partial a+a\,\partial b.
\tag{1.4}
\]

Every registered correction factor evaluates to the identity in that
context, so the second term in (1.4) is untranslated.  The same argument
holds in all seven defect occurrences, and exponent sums are additive.
Consequently

\[
 \mathscr V(ab)=\mathscr V(a)+\mathscr V(b),\qquad
 \mathscr V(a^{-1})=-\mathscr V(a)
 \quad(a,b\in\Omega).
\tag{1.5}
\]

Let \(T\in Z\) be the independently reconstructed raw base defect of \(g\),
not task175's canary change row.  The finite B4 common-correction problem is

\[
 \boxed{-T\in D+\mathscr V(\Omega).}
\tag{1.6}
\]

## 2. A positive linear certificate is already an explicit word

For a linked source word \(u_j\) and a normal generator \(r_j\), write

\[
 w_j=u_jr_ju_j^{-1}\in\Omega,qquad V_j=\mathscr V(w_j).
\tag{2.1}
\]

Suppose sparse elimination returns an exact equality over \(\mathbf F_3\)

\[
 -T=d+\sum_{j=1}^m a_jV_j,
 \qquad d\in D,quad a_j\in\{0,1,2\}.
\tag{2.2}
\]

Define \(\epsilon(0)=0\), \(\epsilon(1)=1\), and
\(\epsilon(2)=-1\), and use the retained column order to form

\[
 \boxed{c=\prod_{j=1}^m w_j^{\epsilon(a_j)}.}
\tag{2.3}
\]

### Theorem 2.1 (POSITIVE CERTIFICATE TO COMMON WORD)

The word (2.3) lies in the registered joint kernel, has both exponent sums
zero modulo three, and satisfies

\[
 T+\mathscr V(c)=-d\in D.
\tag{2.4}
\]

Thus \(gc\), with the registered right-correction convention, solves both
hexagons and the printed-order pentagon modulo the exact PB3/PB4 boundaries.
The boundary chain \(d\) is part of the certificate but is not multiplied
into the source correction word.

#### Proof

Normal conjugates of rows in \(\Omega\), their inverses, and their products
remain in \(\Omega\).  Every row has the registered zero exponent vector,
so the same is true of (2.3).  By (1.5),

\[
 \mathscr V(c)=\sum_j\epsilon(a_j)V_j
              =\sum_ja_jV_j
\quad\text{in characteristic three}.
\tag{2.5}
\]

Equation (2.4) is now (2.2).  Membership in the three separately typed
boundary images is precisely the PB3/PB4 form of the two hexagons and A.18
pentagon used by task175. \(\square\)

The theorem is deliberately one-way operationally: it validates a printed
word without proving that a failed search found every possible word.

## 3. Positive-only lazy column generation

Let \(W_k\) be the span of the boundary and correction columns retained after
iteration \(k\).  If \(-T\notin W_k\), exact sparse elimination supplies a
dual row \(\lambda_k\) such that

\[
 \lambda_k(W_k)=0,
 \qquad \lambda_k(-T)\ne0.
\tag{3.1}
\]

There are two independent positive oracles.

1. The boundary oracle correlates \(\lambda_k\) with the complete translated
   two-relator PB3 and eleven-relator PB4 families.  It may reuse the
   support-times-occurrence correlation and word-bearing translation section
   of the authenticated full-D2 engine.  The first nonzero correlation is a
   genuine boundary column outside \(W_k\).
2. The correction oracle uses task175's full eleven-occurrence formula and
   task176's word-bearing section.  It runs the canonical-section probes and
   the fair fibre/global dovetail of v139.  At the first direct value
   \(\lambda_k(V_r(\delta))\ne0\), it emits the actual word
   \(u_\delta r u_\delta^{-1}\) and its complete column.

Every returned column raises rank, by (3.1).  No zero claim is made when a
bounded boundary scan, fibre prefix, kernel suffix, or global-roster suffix
remains unvisited.

### Theorem 3.1 (POSITIVE-ONLY TERMINATION)

Assume (1.6), exact boundary/correction replay, and fair finite enumeration
inside both positive oracles.  Repeatedly add any returned nonzero-correlation
column.  Then after finitely many additions, \(-T\) reduces to zero and
Theorem 2.1 returns a common correction word.

#### Proof

If \(-T\notin W_k\), choose \(\lambda_k\) as in (3.1).  Were
\(\lambda_k\) zero on every complete boundary and correction family, it
would vanish on the right side of (1.6), contradicting
\(\lambda_k(-T)\ne0\).  Hence at least one positive oracle has an ACTIVE
column.  Fairness eventually visits it, and adding it strictly raises
\(\dim W_k\).  The ambient space (1.1) is finite-dimensional, so this can
happen only finitely often.  The only remaining possibility is
\(-T\in W_k\), when coefficient recovery and Theorem 2.1 finish the
construction. \(\square\)

This theorem explains the exact role of v134/v138.  A complete cubic moment
is needed only to certify a negative correlation efficiently.  It is not a
prerequisite for a successful witness-first run.  If (1.6) is false, or a
registered runtime cap is reached before the ACTIVE column, the positive-only
engine returns `UNKNOWN_RESOURCE`; it never prints a separator.

## 4. Positive receipts need not certify search completeness

The producer's discovery strategy is not part of the mathematical trusted
base.  A helper-nonshared checker for a positive receipt needs to rebuild
only the following finite chain.

For each retained iteration:

1. authenticate the preceding basis digest, target remainder, dual row, and
   nonzero \(\lambda_k(-T)\);
2. reconstruct the chosen PB3/PB4 translation or the single linked source
   word from its task176 \((q,\gamma,\eta)\) data;
3. replay the full raw column, including all eleven correction occurrences
   when the column is of correction type;
4. check the recorded nonzero correlation and that the new pivot was absent
   from the old basis; and
5. rebuild the new basis/remainder digest.

At the terminal iteration it then:

6. replays the sparse equality (2.2), with block tags and exponent rows;
7. forms (2.3), directly re-evaluates the whole correction word in every
   linked context, and checks the joint-kernel/exponent conditions; and
8. verifies both hexagons and the frozen five-factor pentagon against the
   independently reconstructed boundary chains.

Neither the checker nor the positive receipt has to prove that the producer
used the lexicographically first ACTIVE column, scanned every earlier fibre,
or computed a complete moment.  Those properties affect reproducibility and
negative claims, not the soundness of the exhibited word.

Required positive-certificate mutations include: a context value coming from
a different Gamma state, a changed conjugation side, one omitted Fox
occurrence, one same-target cancellation before the full sum, an already
dependent added column, a coefficient \(1\leftrightarrow2\) change, inserting
a boundary chain into the source word, and one pentagon factor-order change.

## 5. Concrete production order after tasks175--176

The first actual R07 witness run should use this frozen order.

1. Pin one positive task175 `READY` receipt and one positive task176
   `COMPLETE` receipt, including run ids, head SHAs, receipt hashes, checker
   verdict hashes, and exact producer/checker identities.
2. Reconstruct \(T\) from `raw_base_targets`, negate it, and append the two
   zero exponent coordinates.  Never substitute `stacked_target`.
3. Seed \(W_0\) with only authenticated independent PB3/PB4 and correction
   columns; a prefix is sufficient because both full families remain behind
   positive dual oracles.
4. At each nonzero remainder, probe complete boundary correlations first,
   then task176 canonical singleton sections, then dovetail the support-fibre
   kernel prefixes \(1,2,4,8,\ldots\), with the global source roster
   interleaved whenever \(K_r\ne0\).
5. Stop immediately on membership and emit the positive certificate of
   Section 4.  Continue to v129's intrinsic augmented \((d,\rho)\) solve only
   after this finite B4 word is independently accepted.

The run should checkpoint after every rank increase.  A restart authenticates
the complete prefix and resumes at the next dual; it must not recompute and
silently choose a different earlier column.  Large scans and checkpoints run
on GHA.  Local execution is not required.

```text
RAW-DEFECT ADDITIVITY ON THE JOINT KERNEL:     PAPER_PROOF
POSITIVE LINEAR CERTIFICATE -> COMMON WORD:    PAPER_PROOF
POSITIVE-ONLY FAIR COLUMN GENERATION:          PAPER_PROOF
POSITIVE CHECKER NEEDS NO EXHAUSTION CLAIM:    PAPER_PROOF
TASK175 REPAIRED SELFTEST:                     CROSS-CHECKED RUN 33042352557
TASK175 POSITIVE PRODUCTION RECEIPT:            GHA RUNNING 33042556905
TASK176 POSITIVE SECTION/CENSUS RECEIPT:        IMPLEMENTATION REPAIR PENDING
TASK178 FINITE MOMENT SELFTEST:                 CROSS-CHECKED RUN 33042527047
ACTUAL POSITIVE-ONLY R07 COLUMN GENERATION:     NOT YET EXECUTED
COMMON B4 CORRECTION WORD:                     NOT CONSTRUCTED
INTRINSIC (d,rho) / COFINAL LIFT:               NOT COMPUTED
FAKE / IHARA WITNESS:                          NOT DECLARED
```
