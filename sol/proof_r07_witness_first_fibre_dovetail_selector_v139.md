# R07 witness-first fibre-dovetail selector v139

Author: Sol / 2026-08-27

Status: paper proof and positive-certificate execution design.  This note
combines v118's support-fibre theorem with the word-bearing extension section
of v137.  It gives a deterministic way to seek an actual ACTIVE correction
before paying for a complete cubic-moment audit.  It does not turn a bounded
unsuccessful search into a separator.  No common correction word, cofinal
lift, fake, or Ihara witness is declared here.

## 1. Current dual and weighted fibres

Fix one column-generation stage.  Let \(W\) be the authenticated current
column span, let \(T\notin W\), and choose an exact separating row
\(\lambda\) with

\[
 \lambda(W)=0,\qquad \lambda(T)\ne0.
\tag{1.1}
\]

For a registered normal-generator row \(r\), v132 gives

\[
 F_r(\delta)=\lambda(V_r(\delta))
 =K_r+\sum_{i=1}^{10}\sum_{t\in T_{r,i}}
 c_{r,i}(t){\bf1}_{\pi_i(\delta)=t},
 \qquad \delta\in\Delta.
\tag{1.2}
\]

Equal targets have already been merged in \(\mathbf F_3\), and zero weights
have been deleted.  Define the support-fibre union

\[
 U_r=\bigcup_{i=1}^{10}\bigcup_{t\in T_{r,i}}
 \pi_i^{-1}(t).
\tag{1.3}
\]

By v118 Theorem 2.1,

\[
 \delta\notin U_r\quad\Longrightarrow\quad F_r(\delta)=K_r.
\tag{1.4}
\]

No character sum is needed to validate a single candidate: direct replay of
all eleven typed occurrences in (1.2) gives \(F_r(\delta)\).

## 2. Word-bearing traversal of one fibre

Use the authenticated source extension

\[
 1\longrightarrow\Gamma\longrightarrow G
 \xrightarrow{\rho}Q_0\longrightarrow1,
 \qquad |\Gamma|=243,
\tag{2.1}
\]

and let \(\Phi_i:G\to E_i\) induce \(\pi_i:\Delta\to E_i\).  Put

\[
 \Gamma_i^0=\ker(\Phi_i|_\Gamma).
\tag{2.2}
\]

For the identity target, v137 constructs

\[
 L_i=\{q\in Q_0:\Phi_i(s(q))^{-1}\in\Phi_i(\Gamma)\}.
\tag{2.3}
\]

For each \(q\in L_i\), choose the first authenticated \(\gamma_q\in\Gamma\)
with

\[
 \Phi_i(\gamma_q)=\Phi_i(s(q))^{-1}.
\tag{2.4}
\]

Then the source kernel has the complete word-bearing roster

\[
 \boxed{
 \ker\Phi_i=
 \{\eta\gamma_qs(q):q\in L_i,\ \eta\in\Gamma_i^0\}.}
\tag{2.5}
\]

Every element occurs exactly once when the section, the first adjustments,
and \(\Gamma_i^0\) are fixed as above.

#### Proof

Every displayed element maps to one by (2.2)--(2.4).  Conversely, write
\(g=\gamma s(q)\in\ker\Phi_i\).  Its quotient state belongs to \(L_i\), and
\(\Phi_i(\gamma\gamma_q^{-1})=1\), so
\(\eta=\gamma\gamma_q^{-1}\in\Gamma_i^0\) and
\(g=\eta\gamma_qs(q)\).  Uniqueness follows first from the quotient state
\(q=\rho(g)\), then from the fixed \(\gamma_q\). \(\square\)

If v137 returns a word-bearing \(g_t\) with \(\Phi_i(g_t)=t\), then

\[
 \boxed{
 \Phi_i^{-1}(t)=\{k g_t:k\in\ker\Phi_i\}.}
\tag{2.6}
\]

Thus (2.5)--(2.6) enumerate the complete target fibre using actual source
words

\[
 u_\eta u_{\gamma_q}u_{s(q)}u_{g_t}.
\tag{2.7}
\]

Projecting (2.7) to all ten contexts supplies the linked \(\delta\); the ten
coordinates must never be filled using different Gamma states.

## 3. Immediate ACTIVE certificate

### Theorem 3.1 (WITNESS-FIRST FIBRE SELECTOR)

Traverse the finite triples

\[
 (r,i,t),\qquad t\in T_{r,i},
\tag{3.1}
\]

in frozen order.  Discard a target only after v137 proves that its singleton
fibre is empty.  For a nonempty target, traverse (2.5)--(2.7) in frozen
\((q,\eta)\) order and directly evaluate (1.2).  At the first value with

\[
 F_r(\delta)\ne0,
\tag{3.2}
\]

the word

\[
 u_\delta r u_\delta^{-1}
\tag{3.3}
\]

is an authenticated correction column outside \(W\).

#### Proof

Equations (2.5)--(2.7) prove that the candidate is an actual source word and
that all its linked context values come from the same source element.  Direct
Fox replay proves that its column is \(V_r(\delta)\).  By (1.1) and (3.2),
\(\lambda(V_r(\delta))\ne0\) while \(\lambda(W)=0\), so
\(V_r(\delta)\notin W\). \(\square\)

Adding (3.3) therefore raises the current rank.  No statement about the
unscanned part of a fibre is required for this positive conclusion.

## 4. Dovetail and completeness boundary

The cheap first pass uses only the v137 canonical section representative
\(g_t\) for every nonempty target.  If all such representatives cancel, scan
successively larger prefixes of every kernel roster (2.5), for example

\[
 1,2,4,8,\ldots
\tag{4.1}
\]

states per nonempty fibre, round-robin over the 6,441 rows.  This prevents one
large kernel from starving the other rows.  Since every roster is finite, the
dovetail eventually visits every element of \(U_r\).

If \(K_r=0\), (1.4) says that a complete traversal of the support fibres is a
complete correlation test for row \(r\), even if duplicate linked elements
are visited.  If \(K_r\ne0\), the complement may itself contain the first
ACTIVE element.  In that case dovetail the canonical complete source roster

\[
 G=\{\gamma s(q):q\in Q_0,\ \gamma\in\Gamma\}
\tag{4.2}
\]

with the fibre scans.  Equation (4.2) is finite and word-bearing, so it
eventually reaches every linked value in \(\Delta\).

Consequently a complete traversal decides whether the current dual is active
on the whole registered correction family.  The operational distinction is:

```text
first direct nonzero value:  ACTIVE WORD / safe early stop
registered prefix exhausted: UNKNOWN_RESOURCE / continue dovetail
all finite rosters exhausted: exact zero correlation for this family
```

A timeout, shard gap, unscanned kernel suffix, or unscanned complement is
never a zero-correlation certificate.

## 5. Witness-oriented column generation

Repeat the following loop:

1. reduce the all-seven target against the current authenticated span;
2. if the remainder is zero, recover every coefficient and multiply the
   retained word-bearing correction columns and boundary chains;
3. otherwise form an exact separating dual \(\lambda\);
4. test the complete PB3/PB4 boundary families, then run the section probes
   and fibre dovetail of Theorem 3.1;
5. add the canonical first ACTIVE block and repeat.

Each successful iteration strictly raises rank in the fixed finite residual
module.  Hence only finitely many ACTIVE additions can occur.  This is the
same finite-dimensional termination argument as v132, but its positive path
does not wait for all moment terms.  If the target is in the registered full
span, an ACTIVE column exists at every nonzero-remainder stage, and the
complete dovetail eventually finds one.  If it is not in the span, only a
complete negative traversal or v134's exact moment may promote the surviving
dual to a separator.

## 6. Production contract

The first R07 run should retain, for every added column:

1. current basis/target/dual hashes and \(\lambda(T)\);
2. row, coordinate, merged target, \(q\)-state, Gamma-state, and kernel-state
   IDs;
3. the complete source word (2.7) and conjugate word (3.3);
4. all ten direct context values from that one word;
5. every one of the eleven Fox contributions to (1.2), including merged
   cancellations;
6. the final nonzero \(F_r(\delta)\); and
7. the new pivot and rank increase.

The checker must rebuild the dual, target fibres, source word, all context
values, all Fox terms, and the rank increase without importing producer
helpers.  Required mutations include a different Gamma state in one context,
wrong kernel-adjustment side, skipped same-target cancellation, nonzero value
from one occurrence instead of the full sum, wrong conjugation side, and a
column already in the old span.

The task175 raw bridge and a positive task176 extension-section receipt are
prerequisites.  Until both are pinned, production is `UNKNOWN_INPUT`.  A
bounded unsuccessful witness scan is `UNKNOWN_RESOURCE`; it does not invoke
the withdrawn v136 cap.

```text
WORD-BEARING SINGLE-FIBRE ROSTER:              PAPER_PROOF
FIRST ACTIVE COLUMN IS OUTSIDE CURRENT SPAN:   PAPER_PROOF
FAIR FINITE FIBRE/GLOBAL DOVETAIL:             PAPER_PROOF
POSITIVE PATH NEEDS NO COMPLETE MOMENT:         PAPER_PROOF
TASK175 POSITIVE RAW BRIDGE RECEIPT:            GHA RUNNING
TASK176 POSITIVE SECTION/CENSUS RECEIPT:        PIN REPAIR / RERUN PENDING
ACTUAL WITNESS-FIRST COLUMN GENERATION:         NOT YET EXECUTED
COMMON ALL-SEVEN CORRECTION WORD:               NOT CONSTRUCTED
COFINAL LIFT / FAKE / IHARA WITNESS:            NOT DECLARED
```
