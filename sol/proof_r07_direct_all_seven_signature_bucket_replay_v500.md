# R07 direct all-seven replay after signature coalescence v500

Author: Sol / 2026-09-04

## 0. Purpose and boundary

This is an exact optional acceleration of the Task640 direct all-seven canary.
It does not change the selected graph, the exact leaf table, any coefficient,
the complete eleven-coordinate signature, the precision-two replay, or the
fresh residual.  It may be used only if the current per-key direct replay is a
measured bottleneck.  The already prepared v7 release need not wait for it.

Let `L` be the canonical nonzero exact keys `(s,P)` and let `G` be the nonzero
signature buckets `(s,tau)` of v471.  The current producer and checker call the
direct H1/H2/P replay once for each of the `L` keys.  The claim below permits
one call for each of the `G` buckets, using the representative path already
stored in the canonical bucket receipt.

## 1. Conjugate derivative depends only on the endpoint

For a registered occurrence `j`, write `q_j=eta_j theta_j`.  Every reached
seed satisfies `q_j(r_s)=1`.  In the left Fox convention,

\[
D_j(P r_s P^{-1})=q_j(P)D_j(r_s).                 \tag{1.1}
\]

This is v470 Lemma 3.1.  Consequently, if two paths have the same complete
signature,

\[
\Sigma_{11}(P)=\Sigma_{11}(P'),                    \tag{1.2}
\]

then their conjugate derivative is equal in each of the eleven registered
occurrences.

For each of H1, H2 and the five-factor pentagon, the direct row is obtained by
inserting the endpoint-one conjugate into the fixed word `g`, applying the
registered substitutions, and subtracting the base relation row.  The Fox
product rule cancels the derivative of the conjugating path as in (1.1); all
remaining multipliers are precisely the fixed occurrence prefixes and signs.
Thus its blockwise difference is

\[
\mathcal D_j(s,P)
 =\epsilon_j L_{U_j}L_{q_j(P)}D_j(r_s),             \tag{1.3}
\]

the occurrence row of v477 (4.1).  No term of (1.3) depends on the spelling of
`P` after `q_j(P)` is fixed.

### Theorem 1.1 (direct-row signature invariance)

If (1.2) holds, then the complete serialized H1/H2/P direct rows agree:

\[
\mathcal D(s,P)=\mathcal D(s,P').                   \tag{1.4}
\]

#### Proof

Equation (1.2) gives `q_j(P)=q_j(P')` for every registered occurrence, with
the repeated coordinate retained in its two typed slots.  Substitute these
equalities in (1.3).  The seed derivative, fixed prefix, sign, block type and
serialization order are the same.  Hence all eleven occurrence rows and their
three serialized block sums are equal.  The exponent rows also agree because
the reached relators have exponent pair zero and conjugation preserves it.
This proves (1.4).  \(\square\)

## 2. Exact bucket-level direct gate

After authenticating all exact keys and computing every exact path signature,
form the canonical mod-three buckets

\[
\bar\mu_{s,\tau}=\sum_{P:\Sigma(P)=\tau}\mu_{s,P}.
\]

Delete only buckets with zero coefficient, exactly as v471 already does.  For
each remaining bucket choose its existing deterministic representative path
(the lexicographically fixed retained path in the bucket receipt) and perform
one complete `direct_column(P,r_s)` versus occurrence-column equality.  By
Theorem 1.1, this equality is the equality for every exact key in that bucket.

This changes the direct replay count from `L` to `G<=L`.  It does not justify
discarding source graph edges or exact leaf keys; those remain authenticated
before grouping.  It also does not permit grouping by only six hexagon slots:
the full eleven-slot signature is required for the all-seven canary.

## 3. Independent checker requirements

A versioned checker using this acceleration must independently:

1. reconstruct all exact keys from the accepted graph and leaf stream;
2. check every reached seed in all eleven endpoints;
3. compute every exact path signature independently and compare the full
   path-signature receipt;
4. reconstruct the canonical nonzero `(s,tau)` buckets and their representative
   paths;
5. perform the direct-versus-occurrence equality once for every nonzero bucket;
6. independently recompute the final precision-two aggregate and rho2 bytes.

Fixtures must split two equal-signature paths by mutating one E4 slot, reject a
wrong representative, reverse one pentagon factor, reverse one prefix action,
and show that a zero coefficient bucket makes no direct call.  A run stopping
before all `G` gates is `UNKNOWN_RESOURCE`, never acceptance.

## 4. Claim boundary

```text
SAME FULL SIGNATURE -> SAME DIRECT ALL-SEVEN ROW: PAPER-CLOSED
EXACT-KEY AUTHENTICATION RETAINED: yes
DIRECT REPLAY COUNT: G <= L
VERSIONED PRODUCER/CHECKER: NOT IMPLEMENTED
MEASURED NEED TO DEPLOY: NOT YET ESTABLISHED
FRESH_RHO2/GRADE2/A0/COMMON/COFINAL/FAKE/IHARA: NOT DECLARED
verified=false
```
