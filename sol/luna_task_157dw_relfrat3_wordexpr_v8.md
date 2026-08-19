# Luna task 157dw — full-4096 typed WordExpr/Fox lane v8

## Role and objective

You are Luna. Implement the versioned successor to the frozen, cross-checked
pivot-surgery v7. The v7 run reconstructed the 32,768-translation boundary
basis, inserted 2,277 additional genuine directed D2 columns, and reached an
exact fixed point after 32 rounds. Candidate 1 still failed at acceptance
target 6. This is an honest fixed-candidate INCOMPLETE, not an obstruction.

The next lane must keep that valid saturated basis and scan the complete
pre-registered dictionary of 4,096 corrections in deterministic order. Avoid
the v4 failure in which candidate 2 eagerly flattened `S(T_5)x_5^-1` to more
than 100,000 letters. Compile candidate targets as a typed expression DAG and
compute exact quotient values and left-Fox gradients by the chain rule without
flattening substituted descendants. A PASS is a literal positive certificate.
Exhaustion, a cap, or an unsupported authenticated input is never a negative,
nonmembership, obstruction, B4-A, or B4-B result.

Frozen v7 sources:

```text
search/d972_b345_relfrat3_pivot_surgery_v7.py
  a19c3353c5cfc6da8ad0b7d941ba94bde043c80e69e33c889c5710c897d7a757
search/check_d972_b345_relfrat3_pivot_surgery_v7.py
  fbe033704180a808320c897c52613ca6847305dd85ddcd7a70aa825161e8bfa0
search/d972_b345_relfrat3_pivot_surgery_gha_driver_v7.g
  1be0ec44674108a2f6319057ba18283206756cf2ef73bfe1e1e5896a6f893d8d
```

Cross-checked v7 evidence:

```text
commit                         c40f4f5a0b2fe6a520439d2e921463b3d72d2b6b
canary run                     32219074110 PASS
full run                       32219440063 workflow/checker PASS
artifact                       9353620461 / gap-run-out / 116179 bytes
archive sha256                 0a037f89e9da27eea00fe8a65879f592903c7ef5240c09643b8b38efcb7fbed0
receipt sha256                 e91684ffefa3eab3ef51cee90758b3fcfbc7fa00e79768d499675de327155094
terminal/reason                INCOMPLETE / no_new_exact_directed_translation
rounds/translations/columns    32 / 207 / 2277
v7-prefix total columns/pivots 362725 / 362709
live entries/pool/peak RSS     3090367 / 976408 / 701743104
producer runtime               231.690623611 s
```

The exact deterministic v7 ordered bindings which a fresh v8 reconstruction
must reproduce before the full scan are:

```text
stable_rounds_projection_sha256
  75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d
translations_sha256
  a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f
columns_sha256
  cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343
blocker_history_sha256
  b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53
final blocker sha256
  0cd653ee0966ccc83d270802bbb5d00b61731f28e27eec1918bb5ea282e00903
```

The stable rounds projection is the ordered list of all v7 public round rows
with exactly `elapsed_seconds` and `RSS_bytes` removed from every row before
canonical JSON hashing. The original receipt's full rounds SHA
`e1c11cd5a436229c8730d5174b9a6981a508901a6e44d5362219e03d74557391`
contains those two volatile measurements and is provenance only; a fresh run
must not be forced to reproduce it or copy its values. All listed stable values
are post-reconstruction drift canaries only. Do not import the v7 receipt,
basis, pool, DAG, or blocker as a checkpoint or mathematical input.

## Authorized files

Create only:

```text
search/d972_b345_relfrat3_wordexpr_v8.py
search/check_d972_b345_relfrat3_wordexpr_v8.py
search/d972_b345_relfrat3_wordexpr_gha_driver_v8.g
sol/luna_reply_157dw_relfrat3_wordexpr_v8.md
```

Do not edit v1--v7, q3 sources, workflows, receipts, dialogue, claims, or any
other file. Temporary diagnostics belong outside the repository. Do not run
the full producer locally, production GAP, Git, GHA, or edit a workflow.

## A. Pre-registered universe, order, and claim boundary

Reconstruct the frozen 4,096-word correction dictionary exactly:

```text
identity first;
then BFS first-seen products by the authenticated H3 commutator seeds
and their inverses, with the frozen signed-seed and reduction order.
```

The candidate universe and scan order are exactly:

```text
candidate i = reduce(FIXED_WORD + correction[i])
i = 1,2,...,4096
m=0, lambda=1
the same frozen row37/exponent2 outside roof
```

Run the complete source-tuple preflight in section C before building the heavy
32,768-translation basis, so a nonuniform fixed-inverse contract fails fast.
Then build the complete basis and saturated v7 directed prefix fresh in the
same job. Reproduce candidate 1 and its final target-6 failure as a drift
canary. Scan candidates 1 through 4,096 once, in this order, against the fixed
saturated basis. Candidate 1 may be replayed rather than trusted. There is no
checkpoint-major retry schedule after saturation.

This is the complete **registered dictionary**, not the complete H3 fibre and
not a negative-complete universe. Record:

```text
registered_corrections=4096
registered_dictionary_complete=true
full_H3_fibre_complete=false
full_universe_claimed=false
earliest_global_candidate_claimed=false
negative_completeness_claimed=false
```

If a PASS occurs, the operational choice is the first passing registered
index. The theorem uses only existence; do not claim mathematical minimality.
If all 4,096 fail in the fixed basis, the result is only registered-search
INCOMPLETE.

## B. Freeze the corrected Def. 2.9 predicate before execution

Retain exactly the T-52/v7 IF-FIRST predicate. The 33 acceptance targets, in
this exact order, are:

```text
5 charming-error cofaces
10 hexagon cofaces
1 ordered A.18 pentagon
11 S-relation residuals
6 S(T_i) x_i^-1 generator-recovery residuals
```

The 17 diagnostics are:

```text
11 T-relation residuals
6 T(S_i) x_i^-1 residuals
```

Diagnostics must have exact expressions and quotient values and remain outside
acceptance, `all_pass`, Fox proof roots, and terminal selection. A false
diagnostic is allowed on a PASS. If a diagnostic quotient value is identity,
optional Fox membership may be recorded, but its result remains diagnostic.

Record and checker-gate:

```text
acceptance_target_count=33
diagnostic_target_count=17
T_canaries_required_for_acceptance=false
corrected_Def2_9_IF_FIRST_frozen_pre_run=true
```

Every candidate word must have exact F2 exponent sums `(0,0)`. Use the standard
free-group fact `ker(F2 -> Z^2)=[F2,F2]` and choose the charming witness
`g=f` itself. Thus `f*g^-1=1`, and the five charming-error targets have exact
zero gradients. Record the reduced candidate word, its exponent sums, and the
identity charming error. Do not construct the old quadratic commutator-bubble
word. This changes only the witness representation, not the predicate.

Keep the five correction-coface J_H identity gates, friendly/marking gates,
hexagons, ordered pentagon, S relations, S(T_i) recovery, and outside roof as
load-bearing direct gates.

## C. Complete all-candidate source-tuple/inverse preflight

The pinned normalized exponent-seven, complete 27-fibre certificate supplies
one exact tuple `T_1,...,T_6` inverse to the frozen six E4 source images. It may
be reused for a candidate only after exact equality of that candidate's ordered
six E4 source-image tuple with the frozen tuple.

Before sparse candidate scanning:

1. Rebuild the exact 4,096 dictionary parent/signed-edge records.
2. Extend the authenticated fixed-context DP with every context needed for all
   six source images.
3. Compute all 4,096 ordered source tuples without constructing substituted
   long words, and require every tuple to equal the frozen base tuple.
4. Bind the complete tuple ledger/count/digest and every candidate exponent
   sum to the receipt.
5. When a candidate enters the sparse scan, reconstruct its six typed source
   expression roots and evaluate those roots directly in E4, independently of
   the DP recurrence. Require equality both with its DP tuple and the frozen
   tuple before using T. A flat source word may be used as an additional canary
   only when its reduced length is at most 100,000; it is never required.

If any registered tuple differs, do not reject or silently skip that candidate
and do not apply the fixed T. Return `SEARCH_INCOMPLETE` with reason
`fixed_inverse_not_uniform`, `scan_evaluated=0`, the first differing index,
both canonical tuples, and an exact evaluated-prefix digest. This is a bounded
lane limitation, not an external input error and not an obstruction. Do not add
raw endomorphism powering or an unbounded inverse search.

The checker independently rebuilds the context registry, seed images, parent
recurrence, all tuple values/digests, and direct replays. Digests are bindings,
never element equality tests.

## D. Typed WordExpr representation

Flat candidate, correction, source-image, formula-relator, coface-image, and
fixed inverse words remain permitted only when each flat leaf is at most the
unchanged 100,000-letter cap. A substituted descendant is not a flat word and
must never be passed to `word_substitute` or materialized merely to compute a
quotient value or Fox gradient.

Use an exact, hash-consed, candidate-local typed DAG with at least these opcodes:

```text
IDENTITY
FLAT_WORD(registered exact signed-letter word)
PRODUCT(left,right)
INVERSE(parent)
SUBSTITUTE_WORD(registered outer flat word, ordered image roots)
```

Hash-cons by the full opcode payload, child IDs, and exact word bytes/tuples;
never by a digest. Build products in a fixed balanced or otherwise explicitly
registered association order. IDs are local implementation handles only. Every
node carries its free-group rank. `PRODUCT` requires equal ranks and represents
ordinary word concatenation; `INVERSE` represents reverse order with signs
reversed; `SUBSTITUTE_WORD` requires that the outer rank equals the number of
ordered image roots and that every image has the declared target rank. The DAG
must be acyclic and strictly backward-referencing.

Gate the exact semantic bridge to the old literal predicate: recursively
expanding a node gives a (generally nonreduced) free word; its free reduction is
the old literal word. Free reduction does not change its Fox derivative, with
the cancellation identity `D(xx^-1)=0`. Compute the unexpanded letter count by
an exact integer recurrence on the DAG and bind both the expansion-count ledger
and reduced-flat canaries when they fit the old cap. Neither producer nor
checker may treat this bridge as a digest assertion.

Candidate 1 is known to fit the old flat cap. In the production path, build all
of its 33 acceptance and 17 diagnostic words with the frozen v7 literal
constructor, and require exact equality of quotient values and left-Fox
gradients with the new expression evaluator. This is a mandatory bridge canary,
not merely a selftest fixture. The independent checker performs the same
comparison with its own flat evaluator.

For an expression `u`, compute and cache its exact E4 value. Compute its
left-Fox gradient over the six PB4 generators using:

```text
D(uv)       = D(u) + value(u) * D(v)
D(u^-1)     = -value(u)^-1 * D(u)
```

For `SUBSTITUTE_WORD(w; a_1,...,a_r)`, stream the outer letters with prefix
`p=1`:

```text
letter +i:  gradient += p * D(a_i);  p := p * value(a_i)
letter -i:  p := p * value(a_i)^-1; gradient -= p * D(a_i)
```

This negative-letter order and left action are load-bearing. The checker must
reject right translation, updating the negative prefix after the subtraction,
and both reversed product rules.

Evaluate nodes in topological order. Use exact reference counts or another
bounded streaming method to release transient child gradients after their last
use. It is acceptable and useful to retain the six source-image gradients
within one candidate transaction, but retain no candidate expression, value,
gradient, pool suffix, or proof node across candidates. Count every live cached
gradient, including retained source gradients and the current target, against
one candidate-wide cap. Compute intermediate prefix E4 values in a transient
exact canonical-value map; do not intern every prefix into the persistent pool.
Only the final nonzero gradient support is transactionally interned.

Pre-register these additional caps:

```text
wordexpr_nodes_per_candidate              262144
wordexpr_edges_per_candidate             1048576
dictionary_word_records                      4096
wordexpr_flat_leaves_per_candidate          16384
wordexpr_expanded_letter_count_per_target 4194304  # count only; never allocate
candidate_live_gradient_entries_total      1000000
candidate_element_pool_suffix             1000000
candidate_scan_records                       4096
```

Keep v7 sparse/pool/pivot/DAG/section/RSS caps unchanged. Reduce the producer
soft wall to 7,200 seconds so that an independently replayable bounded prefix
leaves time for the checker inside the unchanged 330-minute job. Give the
checker its own 7,200-second soft replay bound. A cap hit is a fail-closed
`UNKNOWN_RESOURCE`, never a candidate rejection. The 100,000 flat-word cap is
not raised.

## E. Candidate construction and transactional scan

After the saturated v7 basis is frozen, process one candidate at a time:

1. Snapshot the element pool and proof DAG before any candidate-specific
   intern. Keep the sparse basis and all v7 section/provenance data immutable.
2. Rebuild `f`, its six typed source roots, and the exact source-tuple direct
   expression replay. Do not require flattened source descendants.
3. Construct the 33 acceptance roots and 17 diagnostic roots in the frozen
   order without flattening substituted descendants.
4. Evaluate exact quotient values first. Any failed load-bearing direct gate is
   an exact registered-candidate failure. Diagnostic false values are recorded
   only.
5. For each acceptance root in order, stream its Fox gradient, require quotient
   identity, bind the canonical gradient, and run a membership-only reduction
   against the one fixed saturated basis in canonical pivot order. This first
   pass must not allocate provenance-DAG combination nodes. Stop at the first
   missing pivot.
6. On failure, record the target ordinal/name/kind, blocker component and exact
   canonical E4 binding, gradient entry count, expression accounting, elapsed
   time, and then roll back the candidate pool/DAG/expression suffix and clear
   all pool-ID LRUs before ID reuse.
7. If all 33 membership-only reductions succeed, regenerate that candidate and
   all expressions from its index, require exact expression/value/gradient
   bindings, and only then rerun the 33 solves with provenance enabled. Require
   the proof-producing reductions to agree with the membership-only pass, then
   commit only that selected transaction and serialize it.

The basis does not grow during this scan, so there is no blocker watch/retry
table. Candidate 1 must reproduce the cross-checked v7 target-6 failure and
final blocker digest as a drift canary. Then continue to candidate 2 without
stopping. Failed candidates must leave the persistent proof DAG byte-for-byte
unchanged; proof provenance is paid only for a selected positive candidate.

Pack the scan prefix in bounded arrays. For each evaluated candidate retain an
outcome code, first failed target ordinal, blocker component, and fixed-width
canonical blocker value when applicable. Bind the exact evaluated-index order,
failure distribution, array lengths, and SHA-256. A partial resource stop must
name the current candidate/target and preserve the exact completed prefix.

## F. Positive certificate and terminals

On PASS, serialize:

- the selected correction/candidate/fixed-inverse flat leaves and their exact
  hashes, plus all six source expression roots (not flattened descendants);
- the reachable selected WordExpr DAG with full typed payloads and roots;
- exact quotient values and canonical gradient bindings for all 33 targets;
- the reachable packed boundary proof DAG, including v7 directed leaves and
  their independently replayable section-expression provenance;
- the 17 diagnostic expressions and values, explicitly outside acceptance.

The checker rebuilds the selected candidate and WordExpr table from the
dictionary index; it must not trust serialized opcodes, IDs, values, or hashes.

Allowed terminals are exactly:

```text
B345_RELFRAT3_WORDEXPR_PASS
B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE
B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE
B345_RELFRAT3_WORDEXPR_UNKNOWN_INPUT
```

`SEARCH_INCOMPLETE` has exactly two registered reasons: (i) all 4,096
candidates were evaluated with no resource/input skip and no PASS, or (ii) the
complete preflight found a nonuniform source tuple, so the one fixed inverse
certificate did not cover the registered dictionary and sparse scan evaluation
remained zero. Both state only a bounded positive-lane limitation. Every
non-PASS receipt must contain:

```text
claim_classification=unknown_not_obstruction
claim_scope=registered_4096_wordexpr_positive_search_only
no_mathematical_obstruction_claimed=true
full_universe_claimed=false
negative_claimed=false
```

`UNKNOWN_INPUT` is reserved for a missing or mismatched external pin, schema,
or authenticated q3/v1--v7 input. A computed candidate value, source-tuple
nonuniformity, expression cap, or internal invariant may not use it.

No non-PASS receipt may contain a boundary proof root or affirmative
nonmembership/obstruction language. Internal invariant, orientation, output
schema, rollback, or expression-replay drift is a nonzero hard FAIL, not
UNKNOWN.

## G. Independent checker and real-path tests

The checker must not import producer helpers. Independently rebuild:

- q3, the v1--v7 pins, all presentations/cofaces, E3/E4 collectors, and the
  normalized 27-fibre inverse;
- the 4,096 dictionary, complete source-tuple DP, and every direct tuple replay;
- the 32,768 basis and exact saturated v7 32-round prefix;
- the typed expression table, quotient evaluator, and streaming left-Fox chain
  rule with a separately written implementation;
- candidate order, membership-only pivot reductions, all completed scan
  outcomes/blockers, rollback/accounting, the no-provenance-on-failure
  invariant, and all terminal/claim schemas;
- on PASS, all 33 selected gradients, every proof root/leaf/section expression,
  and the packed proof DAG.

Run at most one lightweight combined differential selftest after the complete
implementation. It must exercise the same production `validate_receipt` path,
not a structurally separate fixture-only validator, and include:

1. exact product/inverse/substitution gradients versus direct flattened toy
   words below the cap;
2. a long nested substitution which exceeds the flat cap but passes value and
   chain-rule gradient replay without materialization;
3. negative-letter prefix, product-order, right-action, opcode, child, and flat
   leaf mutations rejected;
4. all-source-tuple equality and first-difference
   `SEARCH_INCOMPLETE(fixed_inverse_not_uniform)` fixtures;
5. candidate rollback, pool-ID reuse, and fixed-basis immutability mutations;
6. a sealed production-path PASS receipt, then field/expression/gradient/proof
   mutations rejected through the actual validator;
7. diagnostic T/TS false with all 33 acceptance targets true still PASS;
8. S relation or S(T_i) mutation rejects;
9. complete 4,096-style toy exhaustion accepted only as non-obstruction, and a
   forged negative/global claim rejected;
10. PASS, both SEARCH_INCOMPLETE reasons, UNKNOWN_RESOURCE, external-pin
    UNKNOWN_INPUT, and hard-fail terminal fixtures.

Do not claim a negative result in this lane. The nonpositive positive-control
is only a checker/schema canary required by T-52 discipline.

If the sole combined test exposes only a fixture error, report it and request
one corrective rerun. Do not silently rerun.

## H. Driver, estimate, and reply

Version the v7 driver. Pin v1--v7. Run q3 in a separate checked GAP child,
require `with_pquot_packages=true`, purge stale v8 outputs, retain
`python3 -u`, `pipefail|tee`, exact sentinels and marker counts, artifact SHA,
and a 330-minute workflow limit. The parent broker alone dispatches GHA.

Emit live progress at most every 30 seconds and at every 256 candidates. Include
candidate index, target ordinal, evaluated/pass/failure counts, pool suffix,
transient gradient peak, expression nodes/edges, persistent basis/pool/DAG,
elapsed time, and RSS.

Measured v7 basis+saturation was about 232 seconds and 702 MB. Source-only v8
estimate is 1--3 minutes for dictionary/source-tuple preflight plus an unknown
candidate scan. A positive or complete scan may plausibly take 10--60 minutes
per producer and checker; keep the 120-minute per-process soft bounds and the
330-minute job limit. These estimates are not proof claims.

In `sol/luna_reply_157dw_relfrat3_wordexpr_v8.md`, report exact hashes, the
single combined selftest, source-tuple result contract, WordExpr/chain-rule
orientation, transaction/caps, checker independence, terminal boundary,
static audit, and proposed canary/full inputs.

End with exactly:

```text
B345_RELFRAT3_WORDEXPR_V8_READY_FOR_GHA
```
