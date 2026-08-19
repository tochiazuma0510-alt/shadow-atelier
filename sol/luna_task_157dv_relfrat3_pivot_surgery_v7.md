# Luna task 157dv — pivot-directed relator surgery v7

## Role and objective

You are Luna.  Implement a versioned, positive-only successor to the frozen
fixed-candidate v6.  The cross-checked v6 run built the full registered
32,768-translation basis, but correction index 1 still reduced first at target
6 to a missing pivot.  Do not double the blind BFS bound.  Add only exact
left-translated PB4 relator columns which are directed at the current missing
pivot, then retry the same candidate.  A PASS is a literal relative-Frattini
certificate.  Every non-PASS remains fixed-candidate-only and has no
nonmembership, obstruction, B4-A, or B4-B meaning.

Frozen v6 sources and run evidence:

```text
search/d972_b345_relfrat3_fixed_candidate_v6.py
  178c7e63dafba0b9deb8b4e363552ff87a0b7d1c2a120457f593845d56d9d493
search/check_d972_b345_relfrat3_fixed_candidate_v6.py
  12c5475c984aa2855c502930169a01cc656ec67507a6aa56d098cd314db011fd
search/d972_b345_relfrat3_fixed_candidate_gha_driver_v6.g
  2b36db96d440316292d271c22e662da507dc6afeba20aa0222c8388bab6f4ada

commit 4cade81aa37f7df056b97015ca86bf025ec27536
canary run 32214206738: PASS
full run 32214317453: producer/checker/driver PASS
artifact 9351964059 / gap-run-out / 50897 bytes
archive sha256 4c4dde33c752004bb1450ac4c7bac3aac55803e053ea23fdac9a03e5fb18e9ef
receipt sha256 cd7cf742ad3304bd87ae54e74a0ab83e18aa85c531b76f2df71949e597640018
terminal B345_RELFRAT3_FIXED_CANDIDATE_INCOMPLETE
translations/columns/pivots 32768 / 360448 / 360432
live sparse entries 3072055
element pool 969407
DAG nodes/edges 669309 / 492108
peak RSS 692957184 bytes
producer runtime 240.388214752 s
```

The recomputed blocker was target 6, `hexagon_1_coface_0`, component 4,
and its pivot was absent at every registered checkpoint through 32,768.  This
is motivation and a post-reconstruction drift canary, not an input blocker
blob and not a nonmembership result.

## Authorized files

Create only:

```text
search/d972_b345_relfrat3_pivot_surgery_v7.py
search/check_d972_b345_relfrat3_pivot_surgery_v7.py
search/d972_b345_relfrat3_pivot_surgery_gha_driver_v7.g
sol/luna_reply_157dv_relfrat3_pivot_surgery_v7.md
```

Do not edit v1--v6, q3 sources, workflows, receipts, dialogue, claims, or any
other file.  Temporary diagnostics belong outside the repository.  Do not use
the v6 artifact as a basis checkpoint: q3, the 32,768-translation basis, the
candidate, and the blocker must all be reconstructed fresh in the same job.

## A. Frozen candidate and pre-registered acceptance predicate

Retain exactly:

```text
kind=fixed_positive_candidate
correction_indices=[1]
correction_word=[]
m=0, lambda=1
frozen row37/exponent2 outside roof
full_4096_universe_claimed=false
earliest_global_candidate_claimed=false
negative_completeness_claimed=false
```

Freeze the corrected Def. 2.9 lane **before execution**.  There are 33
acceptance targets in this exact order, obtained from the v6 order after
removing the T-only canaries:

```text
5 charming-error cofaces
10 hexagon cofaces
1 ordered A.18 pentagon
11 S-relation residuals
6 S(T_i) x_i^-1 generator-recovery residuals
```

The 11 T-relation residuals and 6 T(S_i) x_i^-1 residuals are retained as
lossless diagnostics only.  They must be evaluated and recorded but must not
feed candidate acceptance, `all_pass`, target membership roots, or terminal
selection.  A false diagnostic is allowed on a PASS.  Conversely, any failed
S relation or S(T_i) recovery is an acceptance failure.  Record:

```text
acceptance_target_count=33
diagnostic_target_count=17
T_canaries_required_for_acceptance=false
corrected_Def2_9_IF_FIRST_frozen_pre_run=true
```

Do not relax or strengthen this predicate after seeing a run.  The v6 target-6
blocker belongs to both the old and corrected lists, so its reconstruction is
unchanged.

## B. Exact directed-column theorem and order

Use the existing left-Fox convention.  A base D2 column term has key
`(component,h)`, and left translation by `t` sends it to
`(component,t*h)`.  For the fully reduced candidate blocker
`b=(component,g)`, enumerate every nonzero occurrence `(relator,component,h)`
in the eleven canonical base PB4 relator gradients and set

```text
t = g * h^-1.
```

Thus the translated column contains `b`.  This orientation is load-bearing;
the checker must reject `h^-1*g`, `g^-1*h`, and right translation.

For each round:

1. Reconstruct the fixed candidate and reduce its 33 acceptance targets in
   order against the persistent basis.  Stop at the first unsolved target and
   its canonical least blocker.
2. Traverse matching base support occurrences in fixed order
   `(relator index, component, canonical h bytes)`.  Compute exact `t`,
   deduplicate by canonical E4 bytes (never pool ID or digest), and discard only
   translations whose complete eleven-column block was already inserted.
3. For each first-seen `t`, insert the complete block
   `t*D2_1,...,t*D2_11` in relator order into the same persistent sparse basis.
   Candidate target transactions roll back; directed basis columns never do.
4. Retry immediately after the whole directed batch.  If a later acceptance
   target fails, repeat from its new blocker.

All inserted columns are genuine F3[E4]-left translates of D2.  A proof root
using them is sound.  However, a translated column containing `b` may expose a
smaller missing pivot.  Therefore same-blocker, no-new-translation, or bounded
round exhaustion is only `INCOMPLETE_DIRECTED_SURGERY`, never nonmembership.

Pre-register these additional caps:

```text
directed_surgery_rounds       256
directed_unique_translations  32768
directed_columns              360448
```

Keep every v6 cap unchanged, including sparse entries 4,194,304, element pool
2,000,000, pivot rows 1,000,000, DAG 2m/4m, 100,000 flat word/section, 4.5 GiB
RSS, and 300-minute producer wall.  A cap hit is `UNKNOWN_RESOURCE` with an
exact prefix.  Do not raise a cap preemptively.

## C. Exact section oracle and provenance

Directed translations lie outside the BFS section table.  Every pool element
which may become a residual blocker must have an exact section witness.
Implement a compact, append-only-or-transactional section-expression oracle
bound to canonical E4 equality:

```text
identity
signed marked generator
product(left,right)
inverse(parent)
registered flat word (only with direct quotient replay)
```

Prefer one first-seen expression root per exact pool value.  New multiplication
and inverse values must record their parents.  Any raw `intern(value)` without
a section witness is forbidden on the active route.  Pool suffix rollback and
ID reuse must also roll back or safely detach the corresponding section roots;
no stale numeric-ID reference is allowed.

For blocker section `w_g` and a base-prefix section `w_h`, the directed
translation section is the ordinary composition

```text
w_t = reduce(w_g + inverse(w_h)),
```

not paper-product reversal.  A later blocker may come from target support or
from an inserted raw-column support.  The oracle must reconstruct it in both
cases.  Missing section provenance is a hard invariant failure or an honest
UNKNOWN_INPUT, never a guessed word.

On PASS, serialize only the section-expression roots reachable from proof-DAG
leaves, with exact canonical-value bindings, typed arrays or another compact
lossless format, lengths, and SHA-256.  The checker independently evaluates
every expression, reconstructs each `t=g*h^-1`, rebuilds every base D2 column,
left-translates it, and replays the packed proof DAG.  Digests are bindings,
never equality oracles.

## D. Transaction and receipt contract

Keep candidate work and directed basis growth separate:

- candidate target pool/DAG suffixes roll back after the first failed target;
- export/detach the exact blocker value and section before rollback;
- reconstruct it persistently from its section expression;
- commit directed translations, columns, pool values, and provenance;
- retry the candidate from acceptance target 1.

Record per round:

```text
round
failed target ordinal/name/kind
blocker component and canonical-value SHA/binding
matching base occurrences
new/duplicate directed translations
columns attempted/independent/dependent
pivots before/after
live sparse entries, pool, DAG, section-expression nodes, RSS, elapsed
candidate rollback count
```

Also record exact ordered digests for directed translations, columns, blocker
history, and the final bounded prefix.  Live progress is required at every
round and at most every 30 seconds.

Allowed terminals are exactly:

```text
B345_RELFRAT3_PIVOT_SURGERY_PASS
B345_RELFRAT3_PIVOT_SURGERY_INCOMPLETE
B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_RESOURCE
B345_RELFRAT3_PIVOT_SURGERY_UNKNOWN_INPUT
```

`INCOMPLETE` requires either no new exact directed translation/column or all
256 rounds without a PASS.  `UNKNOWN_RESOURCE` must name a closed registered
resource reason.  Invariant/schema/orientation drift is a nonzero hard FAIL,
not UNKNOWN.  Every non-PASS receipt must contain exactly:

```text
claim_classification=unknown_not_obstruction
claim_scope=fixed_candidate_pivot_surgery_only
no_mathematical_obstruction_claimed=true
full_universe_claimed=false
negative_claimed=false
```

No non-PASS receipt may contain a boundary proof root or affirmative
nonmembership/obstruction language.

## E. Independent checker and tests

The checker must not import producer helpers.  It must independently rebuild:

- q3 and all frozen v6 arithmetic/Fox/presentation data;
- the 32,768-translation v6 basis and candidate-1 blocker;
- the exact 33/17 acceptance/diagnostic split;
- every base support occurrence and `t=g*h^-1`;
- every section expression and canonical E4 value;
- directed-column order, deduplication, elimination, blockers, and rounds;
- on PASS, all 33 acceptance gradients and the compact proof DAG;
- all terminal/claim/resource schemas.

Run at most one lightweight combined differential selftest after the complete
implementation.  It must include:

1. a toy left-translation example where `t=g*h^-1` creates the blocker key;
2. rejection of the three wrong orientations and of a forged section;
3. duplicate translation/column neutrality and canonical-key deduplication;
4. candidate rollback versus persistent directed-basis commit;
5. a new-smaller-pivot case proving that no progress remains INCOMPLETE rather
   than obstruction;
6. section-oracle product/inverse/rollback/ID-reuse mutations;
7. PASS, INCOMPLETE, UNKNOWN_RESOURCE, UNKNOWN_INPUT, and hard-fail fixtures;
8. diagnostic T/TS false with all 33 acceptance targets true still PASS;
9. S-relation or S(T_i) mutation rejects;
10. packed proof-DAG and directed-leaf provenance mutations reject.

Do not run the full producer locally.  Do not run production GAP, Git, GHA, or
edit workflows.  If the sole test exposes only a fixture error, report it and
request one corrective rerun.

## F. Driver, estimate, and reply

Version the v6 driver.  Pin v1--v6, run q3 in a separate checked child, require
`with_pquot_packages=true`, purge stale v7 outputs, retain `python3 -u`,
`pipefail|tee`, sentinels, exact marker counts, artifact SHA, and a 330-minute
workflow limit.  The parent broker alone dispatches GHA.

Source-only estimate: q3 plus the measured v6 basis is about 4--7 minutes.  A
short directed closure is expected to add seconds to a few minutes; allow
8--20 minutes normally and retain the full wall/RSS guards.  These are
estimates, not proof claims.

In `sol/luna_reply_157dv_relfrat3_pivot_surgery_v7.md`, report exact hashes,
selftest result, directed theorem/orientation, section/provenance design,
terminal boundary, static audit, runtime estimate, and proposed canary/full
inputs.  State explicitly that the lane is candidate-1-only, positive-only,
and not a substitute for the future full-4,096 expression/Fox lane.

End with exactly:

```text
B345_RELFRAT3_PIVOT_SURGERY_V7_READY_FOR_GHA
```
