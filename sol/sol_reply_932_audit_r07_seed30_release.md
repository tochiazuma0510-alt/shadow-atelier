# Task932 — bounded seed30 release audit

Verdict: **PASS for the planned GHA release under the frozen sources.**
No necessary code fix or additional release prerequisite was found. This is
a static audit, not a claim that canaries or actual arithmetic have run.

I read the complete Task932, Task927 including section 5, Task928, completed
replies929/930, and both complete new programs. Read-only SHA-256 inspection
matches the freeze:

| File | Bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_actual_seed30_materializer_v1.py` | 79651 | `3ce9293e05f06bf343bd2a54af0ab84ae67f4b922a428cd3c73e38944d6de55c` |
| `search/check_d972_r07_actual_seed30_materializer_v1.py` | 62048 | `f4f8ba2d342cb60e2c70b708b8847768a78ebde40dd0a52879f460cb558eab36` |

Line numbers below refer to those frozen files; P means producer, C checker.

## F1. Raw source and local P1 ABI — PASS

- P:499 / C:282 retain prepare-old source order, then new target/source order
  and every raw term ordinal before F3 collection. Cancelled numerical terms
  keep their literal P1 roots. Both require final support 902.
- P:666 correctly interprets P1 reduction indices locally: the containing
  old/new block base is added when reading the preceding row digest. Stored
  reduction order is not sorted away, and nullable literal metadata is
  accepted. P:714 and C:322 bind the fixed instruction/cache bytes and roots.
- P:810 / C:363 evaluate the raw seed, subtract the complete selected full
  P1 lifts, and require all 96,776 lower coordinates to vanish before the
  full filtered projector. They check its char0 top against the plain slice
  and require the other projected characters to vanish. No old per-character
  seed projection or actor path has slipped back in.

## F2. Physical delta and target step — PASS

- P:889,1315 / C:509 use the pinned B forward table and independently form
  its transpose pullback. They require the fixed q, `q(d)=1`, and
  `lambda(G)=1`.
- P:1106 / C:535 sweep old pivots in insertion order, not sorted lead order.
  They retain reduction coefficients, require every old pivot coordinate
  zero, reject a dependent new row, and retain the normalizing scale. The
  raw/remainder pairings stay 1; the normalized pairing is the scale.
- P:1370 / C:838 construct the single rolling-head append from the fixed
  old head. Logical parent offsets and the zero-offset delta payload remain
  distinct; the normalized word references accepted old instruction roots.
- P:1007,1151,1390 / C:659,567,850 decode and authenticate the saved Task904
  remainder and apply exactly one new normalized-pivot update. The 884 old
  target reductions are references, not recomputed or copied.
- P:1168,1393 / C:668,855 handle a nonzero remainder by reverse substitution
  on the insertion-triangular basis, using the accepted old triangularity
  and the checked new earlier-pivot zeros. Zero produces only
  `ConnectionMemberCandidate`. Neither branch asserts grade-wide MEMBER or
  NONMEMBER, eleven-slot replay, normalized exponent replay or full A0.

## F3. Checker agreement, resources and scope — PASS

C:755 and C:782 reconstruct the entire new result, instruction, binary rows
and manifest, then compare exact canonical bytes. Candidate self-seals are
not sufficient authority. The checker imports its pinned checker lineage,
not the new producer or its new arithmetic.

No reachable avoidable major memory/performance trap was found in the narrow
path: Task554 bodies are processed singly, producer retains only selected
packed P1 rows, checker uses positioned selected reads, and neither builds
an array of all 8059 dense full lifts or reconstructs old Conn. The bounded
synthetic canaries are proportionate; no extra historical test is requested.

Independence is limited to the new delta arithmetic with the disclosed
accepted source lineages and common fixed parents. Workshop2096's limited
cross-checked scalar-parent scope is retained, not upgraded. Runtime syntax,
the existing finite canaries and actual producer/checker agreement remain
for the already planned GHA run. Workflow review belongs to root.

No execution, Python/GAP, network, git or historical mathematical re-audit
was performed. Only this reply file was written.

```text
FROZEN SEED30 RELEASE CODE:          STATIC PASS
NECESSARY FIXES:                    NONE FOUND
ACTUAL RANK1354 -> RANK1355:         NOT RUN BY THIS AUDIT
GRADE2 / FULL A0:                   NOT DECIDED HERE
NEW RELEASE PREREQUISITES:          NONE
verified=false
```
