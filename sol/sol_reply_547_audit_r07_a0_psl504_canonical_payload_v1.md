# Task 547 — independent audit of the canonical PSL504 payload

## 1. Inputs, pins, and claim boundary

I read the prescribed Task545 commission/reply, the complete Task543 audit,
both v2/v3 certificates, both v3 programs, and the complete pinned word file.
The final bytes I audited are:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `sol/sol_task_547_audit_r07_a0_psl504_canonical_payload_v1.md` | 2,607 | `7e3814055e76438e16291c1fb248152374823d11caca258fd7e8af4288c33c15` |
| `sol/luna_task_545_r07_a0_psl504_payload_canonical_repair_v1.md` | 4,745 | `ca71a747fd95a09ee9b7fd355f6526cf8973ed98e1e054752714fd13bf8cef01` |
| `sol/luna_reply_545_r07_a0_psl504_payload_canonical_repair_v1.md` | 3,379 | `8e38008973a1f30df422aaa6a17ed0c862c48fafde112064e7d322a7720154e0` |
| `sol/sol_reply_543_audit_r07_a0_psl504_payload_lift_v1.md` | 12,520 | `680771157c6e0f4ec06f5f111c213c9d4ac11603268f70205df442501c6cf1b9` |
| `search/d972_r07_a0_psl504_member_payload_lift_v3.py` | 12,557 | `6d6f8851c45fdcedb4a4caaf18af3d7aa67d345e315960f81fdd26aab93e0bb4` |
| `search/check_d972_r07_a0_psl504_member_payload_lift_v3.py` | 13,799 | `d9d6a33885dbac620130e7e36b30a8d1810adec13d43ee9fd19b1a7833532289` |
| `search/certs/d972_r07_a0_psl504_member_payload_lift_v3.json` | 7,544 | `a97b3081dfc4b23464f367effe60eda6535f745e823af8d21782ab49b5c4b37d` |
| `search/certs/d972_r07_a0_psl504_member_payload_lift_v2.json` | 9,701 | `29efa11882ba76798ab0e9ca39c86476429d7066c4b203200e40d182af0c15f2` |
| `scratchpad/a0_v2_words.json` | 106,133 | `fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612` |

The capture transitively pinned by these artifacts is present at 3,799,820
bytes with SHA-256
`0f5dba1c51e5a39c46fa8a4382e6ee084fc8d629666114fb40000c54c5c91bb2`.
The producer regenerated the v3 certificate byte-identically; the pre-run
and post-run v3 receipt above is unchanged.

The claim audited here is only the canonical PSL504 literal correction over
F3, conditional on the already pinned PSL504-floor premise.  I do not promote
the full-Q0 residual, order 2016 or 54,432, A0, COMMON, a compatible lift,
fake, Ihara, or Lean verification.

## 2. Independent mathematical replay

### F1. Free reduction and F3 collection — PASS

My temporary auditor imported no repository program or helper.  It read the
pinned v2 terms and obtained:

```text
raw terms                                      553
raw compact-JSON SHA-256                       1b21f56f2309793719a9b004df1b1a7b157bac413ede22edb5adc39b6b2ba142
raw paths containing a free cancellation       163
distinct (seed,reduced word) keys               408
keys zero after F3 collection                    20
surviving canonical terms                       388
canonical compact-JSON SHA-256                  a795b9e00c464af4339835d456439a483a4c908bb9411be0829d92a9f8696148
```

The resulting 388 triples agree entry-for-entry, including order and
coefficient, with the v3 certificate.  Independently forming the sparse F3
map `(seed, freely-reduced conjugator) -> coefficient` from both sides gives
literal equality.  Direct replay of the 553 raw terms and the 388 canonical
terms also gives the same PSL504 row and the same degree-36 row.  Thus this is
not merely equality of two stored digests: free reduction and collection do
not change the represented literal correction.

### F2. Markings, identities, and actions — PASS

I checked that both marked Q0 generators are genuine degree-36 permutations,
that their first nine points form an invariant block, and that

```text
source map:       x -> q_a, y -> q_c
PB3 triple:       (a,b,c) = (q_a, (q_c q_a)^-1, q_c)
                  a b c = 1
```

In particular source `y` was never replaced by PB3 `b`.  A FIFO enumeration
using the deliberately different neighbour order
`c^-1,a,c,a^-1` has 504 elements; its roster digest is
`82eb8711c87bf049f42c2630a2959cada8859f1db7ad5e75d20ddfdd3dfea0f5`.
All PSL replay coordinates in this independent audit were keyed directly by
the nine-point permutation tuple, not by either program's element number.

The identity totals, checked in both the nine-point and degree-36 actions,
are:

```text
44 compact seeds x 6 occurrences               264 / 264
388 canonical conjugates x 6 occurrences     2,328 / 2,328
```

I represented the coarse augmentation by a single state-free scalar
coordinate.  Left action fixes that scalar, while every non-scalar Q0 state
was asserted to be a 36-tuple.  The only nine-point slicing occurred when
constructing the PSL quotient or the final projection.  This directly checks
the other two previously defective conventions: there are not 36 coarse
augmentation coordinates, and no degree-9 permutation acts on a degree-36
row.

For actor equivariance I compared a freshly differentiated conjugate with
left transport of the compact seed row.  All four one-letter actors passed
for all 44 seeds (176 six-occurrence row identities) in each action.  The
actual 388 canonical conjugators then passed the same comparison (388
six-occurrence row identities, or 2,328 occurrence identities) in each
action.  Algebraically this is the exact identity

\[
J(drd^{-1})=q(d)J(r)
\]

because every occurrence image of `r` is the identity; the direct comparisons
also fix the left-versus-right convention non-vacuously.

### F3. Exponent and PSL504 target — PASS

Every one of the 388 selected base-relator occurrences has both integral
exponents divisible by 18 before reduction.  Summing coefficient times the
integer quotients gives `(-702,-378)`, hence exactly `(0,0)` modulo 3.  No
division was performed after reducing modulo 3.

The complete six-occurrence aggregate of the canonical correction equals the
direct PSL504 target.  The same tuple-key replay with all 553 raw terms gives
the identical target, independently confirming that canonicalization did not
change the correction.

### F4. Actual PB3 Fox/Tietze gate — PASS

The two rows differentiated were exactly

```text
a^-1 b a b c b^-1 c^-1 b^-1
a^-1 c a b c^-1 b^-1
```

using the three distinct degree-36 generator images `(a,b,c)`.  Each endpoint
is the identity.  For each full Fox row `(v_a,v_b,v_c)`, the exact map

\[
(v_a,v_b,v_c)\longmapsto
(v_b-v_a a,\;v_c-v_a\,a b,\;\operatorname{aug}(v_a))
\]

is zero, with the last entry accumulated into one scalar coordinate.
Moreover `C(L_tD)=L_tC(D)` was checked for the four marked source generators
and both relations (8 generator canaries).  Since multiplication acts
bijectively on the two group-ring coordinates and fixes augmentation, this
identity proves zero for every left translate, not just for the canaries.

### F5. Degree-36 residual — PASS as a materialised problem

The raw and canonical corrections give the identical degree-36 replay.  For
`T_Q0 - A_g^Q0(z)` I independently obtained:

```text
support                                      82,965
coefficient 1                               40,794
coefficient 2                               42,171
SHA-256  922995928c0616177a0c6dff45b1b7366b07258c4f202409e3e97f5080cd60fa
scalar residual support                           0
literal first-nine-point projection support       0
```

This confirms the receipt and zero PSL504 projection.  It does not say that
the Q0 residual vanishes or is solvable.

## 3. Checker independence and negative controls

The v3 checker does not import the producer or a new common helper.  It reads
the frozen v2/word/capture/Task543 inputs, reconstructs the canonical list,
marked actions, identities, target, exponent, PB3 rows, residual and
projection, and passes an arbitrary in-memory certificate through one
`validate` path.  The cryptographic fields used by the promoted claim are
anchored to actual file bytes or to independently reconstructed data; the
residual digest is not accepted merely because it equals a copied certificate
constant.

The receipt-bearing serial runs were:

```text
python -B -u search/d972_r07_a0_psl504_member_payload_lift_v3.py
    exit 0, 28.007 s
python -B -u search/check_d972_r07_a0_psl504_member_payload_lift_v3.py
    exit 0, 41.678 s
python -B -u %TEMP%/task547_independent_payload_audit.py
    exit 0, 39.652 s outer wall (39.436 s internal)
```

I checked the process table immediately before each run.  Guards deferred the
first attempt while the higher-priority Task542 producer/checker or its
follow-up was active; no Task547 Python overlapped another Python process.  A
first checker invocation also completed alone, but its yielded PTY receipt was
not retained, so the 41.678-second run above was made once more to obtain the
complete immutable output.  The temporary auditor is outside the repository
(19,623 bytes, SHA-256
`60d2fd100ae1d1b958eb608b00d7b90e00bd1b9647dde4df4f0d1aeb5cdc6a2f`).

The six required mutations were submitted to `validate` and rejected at the
following semantic gates:

| mutation | rejection gate |
|---|---|
| first literal coefficient `1 -> 2` | `canonical_terms` |
| first conjugator `[] -> [1]` | `canonical_terms` |
| capture hash | `capture_sha256` |
| residual digest | `q0_residual_digest` |
| top-level terminal | `terminal` |
| `flags.A0=false -> true` | `downstream_flags` |

The coefficient and word changes are distinct mutations of distinct fields;
neither is a duplicated difference canary.  The residual mutation reaches its
gate only after an actual residual reconstruction.

There are three concrete checker limitations, none of which changes the
audited payload bytes:

1. The producer and checker use the same LIFO enumeration and generator order
   `(a,c,a^-1,c^-1)`.  Thus there is no genuine alternate checker enumeration.
   No pivot convention is relevant in v3 because it performs no solve or
   echelon construction.  The independent FIFO/direct-permutation replay above
   supplies the missing enumeration diversity for this audit.
2. Although names and control flow differ, many word/Fox/aggregation routines
   remain close translations of the producer.  The checker is data-flow
   independent, but not a strongly diverse third implementation.
3. `validate` does not compare several non-load-bearing telemetry fields,
   notably certificate `q0_residual.support_count`, `pb3_relation_count`, the
   explanatory `pb3_equivariance`/`recipe` strings, and the copied `core`
   object.  It also compares the residual distribution to a pinned constant
   rather than deriving that dictionary explicitly.  The independent replay
   above recomputed all numerical facts used here, but a future generic schema
   validator should close these stale-telemetry openings.  In addition, the
   repository aggregation helpers encode the scalar as `0` and would try to
   act on it as a group state if a nonzero scalar reached aggregation; that
   branch is vacuous for this exact null-exponent payload and was checked with
   a correctly fixed scalar in the independent replay.

## 4. Verdict and handoff

`PSL504_CANONICAL_PAYLOAD_PASS`

The current v3 payload may replace v2 as the pinned **trivial-sector PSL504
literal input** to Task542: its 388 terms are exactly the freely reduced and
F3-collected form of the pinned 553-term correction, and both forms replay to
the same target.  A consumer must pin the v3 certificate SHA-256
`a97b3081dfc4b23464f367effe60eda6535f745e823af8d21782ab49b5c4b37d`
and canonical literal digest
`a795b9e00c464af4339835d456439a483a4c908bb9411be0829d92a9f8696148`.
This replacement does not retroactively alter a Task542 run pinned to v2 and
does not promote any nontrivial-character or higher-quotient result.

The maximal promoted statement is: conditional on the already audited
PSL504-floor premise, the canonical 388-term literal correction is a
cross-checked PSL504 solution.  Full Q0 remains only a materialised residual;
order 2016, order 54,432, A0, COMMON, compatible lift, fake and Ihara remain
undecided/not declared.  No commit, push, GHA dispatch, es7ops call, or Lean
certificate was used.  This reply is the only worktree content change
introduced by this audit.

verified=false
