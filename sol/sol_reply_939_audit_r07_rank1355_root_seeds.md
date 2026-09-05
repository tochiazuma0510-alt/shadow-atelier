# Task939 — rank1355 root-seed release review

Verdict: **PASS for the planned GHA run on the frozen sources.**
Necessary fixes: none found. This is static review; runtime canaries and
actual producer/checker agreement have not been executed by this auditor.

I read full tasks936/937/939, replies936/937/938 and both complete new
programs. Read-only SHA-256 inspection matches the task freeze:

| File | Bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_rank1355_root_seed_scalars_v1.py` | 31578 | `973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb` |
| `search/check_d972_r07_rank1355_root_seed_scalars_v1.py` | 36236 | `f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62` |

P/C below denote those producer/checker files; line numbers refer to this
freeze. Workflow review is root's separate responsibility.

## F1. New separator authority and all1355 final-lambda dots — PASS

P:184 / C:161 authenticate the pinned successful seed30 delta, source and
checker receipts, rolling append, generation8060/rank1355, new head
`36feb776...71342` and lambda `f83bbaa5...60565`. The immutable rank1354
state is joined as a parent, not rebuilt.

P:223,243 / C:215 directly pair the **final saved new lambda** with each
of the 1354 authenticated old physical rows and the added normalized pivot.
All 1355 dots must be zero. The saved new target-remainder dot must be one.
This explicitly implements ruling2105 F1; it does not rely on intermediate
reverse-substitution equations. The accepted target-reduction identity and
these complete orthogonality checks justify using the saved remainder
instead of a new rho2 solve.

## F2. Fresh roots, contractions and complete seed subtraction — PASS

P:266,280 / C:285,395 derive all four B-adjoint roots from the new lambda
and bind every RawDual to its new generation/head/lambda. No old-q value,
fixed active-character pattern or old-head fallback is used.

P:292 / C:309 make one buffered P1 cache pass for the four fresh
8059-entry contraction vectors, with correct character byte offsets.
Instruction bytes are hash-streamed once. Zero-root skipping on the
producer side occurs only after actual root derivation; the checker
independently produces the same zero contraction vector.

P:438 / C:342 use their respective raw-seed evaluator with
`actual_pin=False`, so no old seed2 scalar assertion remains. P:326 /
C:364 subtract all four prepare-old source expressions and all four
source expressions in each new target block, with the correct global
offsets. Term multiplicity/order is retained in each seed's event chain.
Thus the scalar is raw seed minus the **complete** P1 subtraction, not a
projected-direct-side shortcut. No actor-origin scalar or orbit scan is
called.

## F3. Scope, independent comparison and resources — PASS

P:374,463 / C:417,433 emit exactly 176 character-major seed0–43 records.
The first nonzero gives `ROOT_SEED_VIOLATION`; all zero gives only
`ROOT_SEEDS_ZERO`. New-word materialization and grade2/full-A0 terminals
remain explicitly unperformed/undecided.

C:449,531 reconstruct all 20 expected payloads, nested receipts, stream
and manifest and compare their exact bytes. It uses the disclosed pinned
checker lineage, not the new producer arithmetic. This does not upgrade
the accepted parent derivations or claim a third arithmetic lineage.

No major reachable resource trap was found: physical and P1 reads are
buffered, contraction chunks are bounded, and the five Task554 bodies are
processed singly. P:354,362 and C:390 release the body references before
the next load. No old Conn/state/target reconstruction, parent-state copy
or all8059 dense-lift array is introduced.

No new tests, actor expansion or framework is required by this review.
Only this reply was written; no local execution, network, git or historical
re-audit was performed.

```text
FROZEN RANK1355 ROOT-SEED RELEASE:    STATIC PASS
FINAL-LAMBDA ALL1355-ROW GATE:       PRESENT ON BOTH ACTUAL PATHS
FRESH FOUR ROOTS / COMPLETE SEEDS:   CORRECT STATIC CONTRACT
NECESSARY FIXES / NEW PREREQUISITES: NONE FOUND
ACTUAL NEW SCALARS:                 NOT RUN BY THIS AUDIT
GRADE2 / A0 / FAKE / COFINAL:        NOT PROMOTED
verified=false
```
