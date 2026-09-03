# Task 593 independent audit -- grade-one decision-first factorization

## Verdict

`PASS_AFTER_REPAIR`

The decision-first factorization is mathematically exact: after all 8,059
logical inputs have been routed lower-first, reducing the fixed residual by
the resulting physical grade echelon fixes MEMBER versus NONMEMBER.  The
dual, serialized ancestry, literal expansion, and degree-two replay are
post-decision objects.

Two local resource statements require repair.  The rank 5,044 was observed
only after logical position 7,936 and is not a ceiling for the final
checkpoint basis.  Also, 48,740,832 is a safe ceiling for the grade-owner
roster-scan cursor advances, not for all lower-first cursor advances in v4.
Neither repair changes the predicate, roster, or branch factorization.

`verified=false` (independent static audit; no Lean certificate and no real
calculation).

## 1. Frozen receipts and scope

I read every commissioned input completely.  The byte images audited were:

| input | bytes | SHA-256 |
|---|---:|---|
| `sol/sol_task_593_audit_r07_grade1_decision_first_factorization_v1.md` | 1,570 | `fa6511d26dd740efdb9a7c357b8ab5a2b7d22881b46bdb9e4d04ecbb7f3ac474` |
| `sol/proof_r07_grade1_decision_first_terminal_factorization_v463.md` | 4,844 | `effd84a07176f90de6ebb006e71ea307c1e0cc9d1db76f2593f07fd584998b60` |
| `search/d972_r07_a0_first_rung_grade1_v3.py` | 138,202 | `bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff` |
| `search/d972_r07_a0_first_rung_grade1_v4.py` | 144,552 | `1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4` |
| `sol/proof_r07_grade1_finite_roster_external_owner_cap_v462.md` | 6,669 | `cc51a9c25676565b31d63b691c77c50112501450eb2dfbf36104c79fb01fa5a5` |
| `sol/sol_reply_590_audit_r07_grade1_finite_roster_external_owner_cap_v1.md` | 9,715 | `2d3738fd79516d03053e112cc6c84ae1646fe493a5ddafa7cad6af1b00010bc7` |

The Task590 reply itself pins an earlier 5,904-byte v462 image with SHA-256
`eb295df10a88e759b33f60c5e09970ee13c2317211cbeb0934df26e7ae0d6d8f`.
The current commissioned v462 image is therefore not covered by that older
receipt.  I audited it directly; it now contains the required global-cursor
repair and the per-owner formulas.

No producer, proof, worker, workflow, v220, production state, git operation,
GHA run, or real phase was invoked or changed.

## 2. The decision point is exact

Both v3 and v4 first traverse the 2,014 old rows.  Each is reduced by the
physical lower owner, the same reductions are applied to its grade companion,
and only a lower-dependent old row is offered to the grade owner.  They then
offer the 6,045 block pivots directly to the grade owner.  Thus the common
logical cursor is

\[
 2,014+6,045=8,059.
\]

Only after these loops do the programs load the fixed residual \(\rho\) and
compute `grade_owner.reduce_packed(pack_trits(residual))`.  The Boolean
`member` is exactly the zero test on that remainder.  On the NONMEMBER branch,
the separating dual and its full-basis annihilation check follow this test.
Basis/roster/DAG/presentation serialization follows them.  MEMBER literal
expansion, lower and precision-one replay, and degree-two replay occur later
in `finalize_real_terminal`.  Consequently

\[
 \rho\in\operatorname{span}_{\mathbf F_3}(E)
 \quad\Longleftrightarrow\quad
 \operatorname{rem}_E(\rho)=0
\]

is already fixed at the proposed decision seal.  These later objects certify
or elaborate the selected branch; they cannot change the finite predicate.
This does not say that the current v3/v4 programs already seal at that point:
the early seal and resume boundary remain a producer proposal.

## 3. The v3 progress log does not locate the stall

In the merge loop, the relevant progress record is emitted only after an
attempt and only when `attempts % 256 == 0`.  Hence the 7,936 record proves
that logical positions through 7,936 completed and that the grade rank there
was 5,044.  It supplies no observation for the remaining

\[
 8,059-7,936=123
\]

positions.  They may have been partly processed, all processed without a
further multiple-of-256 record, or not entered.  Because v3 has no marker
between the last roster row, target reduction, dual construction, and later
serialization, the log also cannot identify any post-row subphase.  V463 is
therefore correct to reject the inference that the dual was the stall.

## 4. V4 cursor accounting: one required scope repair

V3 finds the next nonzero packed byte with a NumPy suffix mask.  V4 instead
executes a Python `while cursor < packed_width` loop and advances `cursor` one
zero byte at a time.  For one grade-owner reduction there are at most 6,048
such cursor advances, apart from iterations which perform pivot elimination.

Let \(\ell\) be the final lower-owner rank.  The exact owner call counts before
target reduction are

\[
 \#\text{lower calls}=2,014,
 \qquad
 \#\text{grade roster calls}=8,059-\ell.
\]

Thus v463 (3.1),

\[
 8,059\cdot6,048=48,740,832,
\]

is a valid conservative ceiling for **grade-owner roster-scan cursor
advances**.  It is not a ceiling for all v4 lower-first roster scans: the old
rows also traverse a 2,017-byte lower owner.  The corresponding all-owner
roster ceiling is

\[
 2,014\cdot2,017+(8,059-\ell)\cdot6,048
 \le 52,803,070,
\]

again apart from pivot-elimination iterations.  Including the one target
grade reduction gives the decision-path ceiling 52,809,118.

The minimal repair is to replace `A physical row` by `A physical-grade row`
and label (3.1) explicitly as the grade-owner roster-scan component.  No
larger formula is needed for v463's conclusion.  The note correctly treats
this only as a performance diagnosis, rejects an unmeasured speedup claim,
and derives no semantic or wall-time result from it.

## 5. Compact checkpoint and both later branches

The proposed checkpoint is sufficient under the blob semantics stated in
v463:

- the five state hashes bind the prepare/four-block inputs and their order;
- 8,059 is the completed **global logical-roster cursor**, not an offer count
  for either owner;
- \(r\), the authenticated packed basis blob bound by \(H_E\), and \(L_E\)
  determine the normalized insertion-ordered echelon;
- the sealed residual and its remainder hash/payload determine the zero test;
  and
- on the zero branch, \(C\) records the ordered pivot coefficients returned
  by the same deterministic reduction.

An independent replay must regenerate the lower-first routing and compare the
actual basis bytes, rank, leads, residual, remainder, and \(C\), rather than
accept hashes as unexplained assertions.  On NONMEMBER, the basis and residual
are enough to construct and check a dual later.  On MEMBER, \(C\) identifies
the selected grade pivot IDs; the same deterministic roster replay reconstructs
the lower and grade DAG nodes needed to expand those roots.  Thus \(C\) is not
standalone literal ancestry, but no ancestry field is required in the compact
decision checkpoint.  This also explains exactly why later branch work may
reuse sealed source blocks while remaining independent of the decision.

## 6. Final-basis ceiling: one required numerical type repair

The multiplication in v463 (2.2) is arithmetically correct:

\[
 5,044\cdot6,048=30,506,112.
\]

Its use as the cost ceiling of the post-8,059 checkpoint basis is not.  Rank
5,044 is only the observed prefix rank, and v463 correctly refuses to infer
the behavior of the last 123 rows.  Each remaining row may add one pivot, so
the narrow prefix-conditioned terminal cap is

\[
 r\le5,044+123=5,167,
 \qquad
 |E|\le5,167\cdot6,048=31,250,016\ {\rm bytes}.
\]

The minimal repair is to replace (2.2) by this bound.  If the prefix receipt
is not used, v462's unconditional roster cap 48,740,832 bytes is also safe but
less sharp.  The malformed unit split in the current (2.2) should be replaced
by `\({\rm bytes}\)` in the same edit.

Current v462 correctly distinguishes

\[
 \mathit{global\_roster\_cursor}=8,059,
 \quad \mathit{lower\_owner\_offers}=2,014,
 \quad \mathit{grade\_owner\_offers}=8,059-\ell.
\]

V463 uses 8,059 correctly in the checkpoint as the global cursor.  It makes
no MEMBER/NONMEMBER, A0, COMMON, COFINAL, or IHARA declaration.  After the two
local repairs above, all commissioned mathematical, replay, typing, and claim
boundaries pass.

PASS_AFTER_REPAIR
