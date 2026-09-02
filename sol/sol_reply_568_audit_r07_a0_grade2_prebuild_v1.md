# GRADE2_PREBUILD_V1_AUDIT_PASS_AFTER_REPAIR

Author: Sol / 2026-09-03

## 1. Scope, receipts and bounded execution

The grade-two algebra in the candidate is sound: the split-state data suffice
to reconstruct the complete `T1`, the `44 + 4*rank(B1)` construction is
target-independent, and the lower-first physical calculation correctly keeps
both direct `H^[2]` images and connections induced by dependent lifted-old
rows.  Release is nevertheless blocked by finite checker/authentication holes
and by concrete Python-object and repeated-dense-work paths which can exceed the
declared six-hour/eight-GiB envelope without reaching a mathematical result.

I recorded the three objects before running any check:

| object | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_first_rung_grade2_prebuild_v1.py` | 145,917 | `acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8` |
| `search/check_d972_r07_a0_first_rung_grade2_prebuild_v1.py` | 80,693 | `fc6f9976b4e3164d4dff31c05256750ddb4758856f39ac5b1fceb43249fbdecf` |
| `sol/luna_reply_565_r07_a0_first_rung_grade2_prebuild_v1.md` | 5,283 | `4e410bbd3fbc489f43012079511fb9d9c8eb03736cb62b112a4dcf0e532bda3e` |

Task565 (5,986 bytes,
`0c0c32831a5fbd055ba158b8f6b1c429aa51a4cdfe1d781e912a2eba016ebef3`),
mandatory v451 (8,050 bytes,
`3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4`),
v450 and the complete Task566 reply also matched their pinned receipts.

The prescribed commands were run serially, with `PYTHONPYCACHEPREFIX` under
`%TEMP%` and with `-B` for both fixtures:

| check | result | measured wall time |
|---|---|---:|
| `python -m py_compile` on producer and checker | exit 0 | 0.366 s |
| producer `--fixture` | `fixture=PASS` | 5.321 s (4.915 s reported) |
| checker `--fixture` | `fixture=PASS` | 1.189 s (0.945 s reported) |

I additionally ran two bounded serial probes.  A deterministic sparse
full-width row gave agreement in 15 producer/checker calculations: four
actors, aggregation, four full word sums, four pure-grade word sums and two
literal seeds (1.666 s).  This probe is useful but is not an independence
certificate because both sides ultimately use the same floor module.  A
focused checker mutation is reported in F3.  No real prepare, block, module,
join or membership phase was run; no production state or certificate was
created.

## 2. The eight required mathematical checks, in order

### F1. Full filtered word sum versus pure-grade idempotent — PASS

The producer implements the two operators separately.  The full filtered
operator is `project_full_by_words` (lines 762--773), used for the 44 lifted
seeds and their resolution check (1725--1744) and for lifted `H^[1]`
defect leaves (1793--1817).  `origin_full_lift` first asserts that every such
origin has zero lower part (1682--1711).  Only then is the restriction to the
pure grade legitimate.  The outer grade-two split instead uses
`project_pure_degree2_by_words` (744--759, 1874--1884).  The checker likewise
has separate `full_project` (582--588) and `pure_project` (457--466)
implementations.  Neither path assumes idempotence of the full filtered word
sum.

### F2. Global order, offsets and signs — PASS

`global_offsets` (producer 1440--1452) and `assemble_b1_relations`
(1470--1566) implement, in the serialized character order,

\[
 R=\sum_\chi r_\chi,
 \quad O_\chi=\sum_{\kappa<\chi}r_\kappa,
 \quad N_\lambda=R+\sum_{\mu<\lambda}n_\mu,
 \quad D_\chi=\sum_{\kappa<\chi}(44+4r_\kappa).
\]

Thus the old rows are all first and the new `H^[1]` rows are all second,
with seed origin `D_chi+a-1` and transition origin
`D_chi+44+4i+t`.  Every old seed/actor coefficient is placed at
`O_chi+i`, and the reduction of the corresponding defect is added at
`N_lambda+j` for all four lambda.  The sign is correctly **plus**:
the packet was defined as direct lift minus old reduction.  The checker's
`expected_relations` (702--743) reconstructs the same offsets and compares
the complete objects at 823--825.

### F3. All seeds/transitions and compact ancestry — REPAIR, load-bearing

The producer does perform the required complete work: direct precision-one
replay of the 44 seeds and all four actors of every `B1` row is at
1627--1670; every old and new lift DAG is replayed at 1714--1847; all 32,280
seed/transition defects are emitted at 1850--1907.  The real checker loops
over all 44 seeds and all actors (835--845), every old/new DAG node
(853--904), every defect and all four packets (907--928), and every block
origin, actor and DAG identity (1068--1084).  This is not sampling.

The checker does not, however, establish that a source block really is the
claimed insertion-ordered basis.  `verify_blocks` checks only the length of
`pivot_leads`; it never compares a declared lead with the first nonzero
coordinate, rejects a zero/dependent row, or requires a DAG reduction/actor
parent to precede the current pivot (1036--1084).  The grade-one authentication
has the same structural omission (644--699, 853--904).  The physical bases do
receive a `FinalReducer` echelon check (1089--1125, 1164--1168), but their DAG
edges likewise are not required to be earlier (1195--1224).

The smallest combined bounded witness for the first two omissions used a
rank-two, width-36,288 synthetic block with zero packet rows and two all-zero
declared basis rows, `pivot_leads=[0,1]`, and a pivot-0 DAG reduction
`[[1,1]]`, a forward edge.  All origin and actor expressions were zero.
`verify_blocks` returned normally.  A rank-one zero row alone witnesses the
false-rank acceptance; rank two is needed to witness a strict forward edge as
well.  This is load-bearing: a cyclic DAG is no longer a literal derivation
from the registered defects and can hide an extra invariant submodule, while
zero/dependent rows falsify the recorded rank.

### F4. Precision-two affine arithmetic — PASS, with checker isolation in R5

The producer's truncated polynomial multiplication (538--577),
`e_polynomial` (580--596), affine action (647--710), occurrence crossed data
and laws (1278--1335), and literal seed evaluation (776--815) implement the
semidirect multiplication rather than an additive-cochain shortcut.  In
particular a negative signed column uses
`(1+u)^-1 = 1+2u+u^2 mod ((u)^3,3)`.  The checker independently codes the
grade-two polynomial/affine layer (213--250, 326--377, 414--514), and the
15-case differential probe agreed.

The single canary `e_polynomial((2,0,0))` (producer 1331--1335; checker
1323--1324) is not itself a binding of every negative occurrence-matrix
column.  Static tracing shows that the real substitution loop applies the
correct polynomial to every column, so this is not a mathematical failure.
R5 below makes the checker independence and fixture claim fail-closed without
requesting a new affine design.

### F5. Complete lower-grade gate and physical fibre — PASS

`replay_extension_and_boundary_preflight` (1278--1437) binds the aggregate
table, all 12 affine images, all 96 crossed-law cases, the zero multiplication
section cocycle, the PB3 source and its six translates, both PB4 words/blocks,
all 44 integral-exponent tests, and the four actor plus aggregation filtration
tests.  The genuine degree-one `qnorm` is used; the physical aggregation is
implemented at 918--988.  The checker reconstructs the same arithmetic and
boundary data locally (539--579, 1292--1393).

The six degree-two monomials are one coupled row block throughout actor action,
source closure and aggregation; there is no coordinate-wise closure shortcut.
More importantly, `run_merge_core` implements both kinds of fibre generator
(2453--2604): when a lower row becomes a pivot it stores the correspondingly
scaled grade-two companion; when a later lifted `B1` row reduces to zero
below, it applies those same reductions to the companion and inserts the
remaining positive-grade connection; it then inserts every direct
`H^[2]` image.  The checker's DAG replay plus complete containment loops
(1195--1241) check both induced old connections and direct new rows.

### F6. Defect roster, closure and target independence — PASS

The roster is exactly `44 + 4*presentation["rank"]` (1859--1907), hence
32,280 at the production rank 8,059.  Each source-character phase ingests all
origins and then all four actors of every accepted row; its success condition
is `attempts = origins + 4*rank`, the queue is exhausted, and the ceiling is
checked (2232--2352).  The module consumes every lifted `B1` row first and
every row from all four completed `H^[2]` blocks second (2474--2546).

Prepare and the four source closures use only authenticated grade-one split
prepare/blocks.  The explicit forbidden-key gate rejects target, residual,
MEMBER/NONMEMBER and grade-one merge fields (2227--2229).  The phase named
`--merge` only combines the four grade-two source blocks into the canonical
linear physical fibre; it imports neither a grade-one merge nor target
coefficients.  No grade-two membership is performed.

### F7. Inactive MEMBER join — REPAIR, first-run formula sound

On a fresh first run the producer does the right mathematics.  It authenticates
the grade-one MEMBER merge/certificate (2814--2856), rebuilds literal `c1`
from the canonical solution and update terms (2878--2890), independently
evaluates target and complete precision-two replay (2891--2900), asserts all
32,260 lower/auxiliary coordinates zero before reading the stored residual
(2901--2929), and recomputes all 48,384 top coordinates, 12,096 packed bytes,
support, packed digest and sparse digest (2905--2937).  It stops before
grade-two membership.

Two release bindings are missing.  First, the accepted certificate is bound to
an allowed **producer** hash, not to an independent grade-one checker receipt,
and the grade-two checker has no join mode at all (`parser`, checker
1636--1655).  Its six-coordinate fixture arithmetic (1592--1605) is not the
join path.  Second, resume calls only `validate_join_state` (producer
2974--3011): that validator does not validate the stored grade-one state chain
or literal-term digest, does not equate the residual blob receipt SHA with
`packed_sha256`, and does not recompute support or sparse digest.  A canonical
join body and blob can therefore be altered and rehashed, then accepted on
resume without replay.  The missing independent parent and residual checks are
load-bearing for any future use of the result-dependent residual.

### F8. Parent/blob/phase authentication and v3/v4 compatibility — REPAIR

The canonical HEAD/body and parent chain (producer 231--253), blob shape,
length, SHA and before/after-stat checks (279--334), origin rosters, exact
character/actor orders, queue-exhaustion fields and phase ancestry are otherwise
fail-closed.  The producer authenticates the grade-one split at 1172--1226 and
1985--2032; the checker independently reads canonical states/blobs and binds
the grade-one parents (114--173, 1396--1450).  Both grade-one v3 and v4 use the
same `d972.r07.a0.first-rung-grade1.v3.state` schema, and both allowed producer
receipts are explicitly accepted, so the schema handoff is compatible.

F3's unvalidated basis/DAG structure and F7's resumable join are exceptions to
the otherwise strong authentication.  They must be repaired before these
digests can serve as semantic receipts.

## 3. Independent checker and fixture audit

The checker does not import the Task565 producer and its outer grade-two
affine, projector, aggregation and state implementations are distinct.  It is
not fully helper-independent, however: the producer obtains `floor` through
the grade-one v4 module (producer lines 32--36), while the checker imports the
same `d972_r07_a0_c2fourier_joint_floor_v1` module directly (checker line 23)
and uses its group multiplication/inverse, permutation evaluation,
substitution and exponent helpers.  Consequently the differential probe above
cannot detect a common error in that layer.  This is a narrow checker-contract
failure, not a request to reopen row 36 or the 648-label audit.

The real module checker is complete over seeds, transitions, closures and old
physical connections, subject to F3.  It has no future-residual checker, subject
to F7.  Its file-backed basis access is sensible, but its `combine_store` and
DAG/containment loops repeatedly unpack a complete dense row for each sparse
coefficient (765--781, 1068--1084, 1195--1241), so the checker also needs the
packed/streamed repair below to be a viable independent production consumer.

Every advertised fixture branch is reachable, but the reported coverage is
too strong.  In the producer, five of the seven “semantic mutations” merely
alter a small dictionary consumed by `fixture_mutation_validator`
(3297--3307, 3362--3383), one mutates a toy residual array and only the blob
case reaches a real receipt validator.  The seven “resume” cases write the same
tiny sealed body twice (3399--3424), not a phase resume path.  The checker has
the analogous dictionary comparator (1572--1591), toy residual
(1592--1605), and canonical-hash round trip (1606--1615).  The producer's
“old and new four actor transitions” checks one fabricated old transition
coefficient and otherwise only four-entry lengths; the old physical-connection
case supplies an arbitrary nonzero grade vector rather than executing the
module core.  Neither fixture executes the real join validator/checker.  Thus
fixture success does not cure F3 or F7 and does not make the candidate
cross-checked.

## 4. Performance and memory classification

### (a) Correctness blockers

The exact correctness blockers are F3 (basis and well-founded literal DAG),
F7 (independent MEMBER/join and resume binding), and the shared-helper portion
of the checker contract.  The affine, boundary, direct/induced physical and
target-independence mathematics do not need redesign.

### (b) Likely production memory/time blockers

1. **Unbounded Python coefficient metadata.**  `run_block_core` retains
   `origin_reductions`, four `actor_transitions` per pivot and every DAG node as
   nested JSON lists (2257--2344): already 177,432 expressions per character
   before the DAG reductions themselves.  On this CPython, an empty list is
   56 bytes and a two-int pair list is 72 bytes plus an approximately 8-byte
   outer pointer.  At only 100 pairs/expression this is at least
   1,429,392,192 bytes; at 500 it is 7,107,216,192 bytes for that expression
   roster alone, excluding integer objects, DAGs, row owners and canonical JSON
   serialization.  There is no coefficient-count ceiling; the formal maximum
   is 6,438,652,416 pairs, over 515 GB at that deliberately conservative
   80-byte lower bound.  Physical lower/grade DAG reductions and prepare's
   `B1` relations have the same representation.  Moreover `phase_merge`
   reads all four block bodies into a list (3122--3134), so all four unbounded
   metadata objects coexist even though packed basis stores are opened one at
   a time.  The current design therefore is not safe under its 8-GiB cap.

2. **A repeated projector hot loop.**  `emit` applies all four legal-word
   pure-grade projectors to each of 32,280 defects (1874--1884).  Three bounded
   timings of the actual four-projector call on one full-width defect were
   0.33952, 0.33278 and 0.33102 seconds.  The median extrapolates to 10,743
   seconds, or 2.984 hours, just for this split, before building lifts,
   32,236 transition defects, four closures or the physical fibre.  This is an
   avoidable use of roughly half the entire 21,600-second phase limit.  On the
   pure Fourier grade, after the fixed word products and character table are
   authenticated once, `e_lambda` is exactly the corresponding character
   slice; all packets can be written and checked directly without replaying
   four long words per defect.

3. **Dense decode/cast inside coefficient loops.**  Old/new lift reductions
   call `full_row_from_stores` for every coefficient (1704--1708,
   1765--1769, 1824--1828), repeatedly unpacking the 96,776-coordinate
   precision-one part and the 145,152-coordinate degree-two part even after
   the lower equality has been established.  Defect reductions repeat the
   same pattern (1888--1898).  In the physical pass every lower coefficient
   decodes a 48,384-trit companion and `_add_mod3` makes whole-row integer
   casts (2481--2494).  One million prepare edges alone read at least 242 GB of
   trits before cast temporaries; one million physical edges add at least
   48 GB.  The checker repeats these paths.  Packed base-three AXPY/chunked
   accumulation is required; decode one candidate only at an action or
   aggregation boundary.

The scale of the unavoidable file-backed data makes those overheads decisive:
one defect packet is 292,844,160 bytes, a maximum block basis 329,204,736
bytes, the `B1` precision-one and degree-two lift blobs 194,979,446 and
292,444,992 bytes, and the maximal physical lower basis/companion/grade basis
64,995,835, 97,481,664 and 585,252,864 bytes respectively.  Those blobs are
plausible when streamed; the nested Python transcripts and repeated dense
passes are not.

### (c) Optional/local optimization after the blockers

`validate_blob_receipt(read=True)` retains one-MiB chunks and then joins them
(317--334), temporarily duplicating a 292,844,160-byte packet before the
matrix view is made.  Prepare/module validation also rehashes some already
authenticated blobs when a row-store constructor is opened.  A phase-local
authenticated-path cache and a read-only mapped view of the same stable file
identity, hashed once at the consumption boundary, remove these copies/scans
without opening a post-hash replacement window.  This is a small local
addition to the mandatory streaming repair, not a new framework.

The implementation already has deterministic progress every 128/256 items,
explicit time/RSS ceilings that seal `UNKNOWN_RESOURCE`, atomic canonical
states, phase-level resume, independent character blocks, and no recomputation
of completed grade-one closures or dependency on grade-one merge.  I do not
require a new generalized checkpoint engine or a mid-block checkpoint as part
of this verdict.

## 5. Finite release repairs

The following edits are sufficient and do not change the mathematics.

1. **Stream coefficient transcripts.**  Replace nested JSON coefficient lists
   for `B1` seed/actor relations, each block's origin/actor/DAG reductions,
   and the physical lower/grade DAG reductions by authenticated file-backed
   packed/streamed transcripts.  Each receipt must bind phase parent, exact
   roster/order, row count, rank/offset, total nonzeros, byte length and SHA-256;
   keep only these receipts in canonical JSON.  Producer and checker process
   and release one character body at a time.

2. **Remove the per-defect word-projector loop.**  Once per run, independently
   establish from the pinned four words and character table that the four
   pure-grade projectors are the four Fourier slice selectors.  Thereafter
   write `defect[2][character]` directly for every defect and have the checker
   compare every reconstructed defect slice directly.  Retain one bounded
   legal-word/Walsh canary on each character; do not replace complete packet
   checking by sampling.

3. **Keep reductions packed.**  Add base-three packed/chunked AXPY for the
   streamed coefficients and physical companions.  After a lower identity is
   checked, update only its degree-two packed component; unpack once per row at
   an actor/aggregation boundary, in both producer and checker.

4. **Close the structural and join checker holes.**  For every grade-one,
   grade-two and physical basis, independently check nonzero normalized rows,
   actual strictly increasing unique leads and rank.  Validate exact DAG node
   schemas and require every reduction index and actor parent to be in range
   and strictly earlier than the current pivot.  Add a checker join mode which
   requires and binds an independent grade-one MEMBER-check receipt, rebuilds
   literal `c1`, recomputes target/replay, all 32,260 lower zeros and all
   48,384 residual coordinates/digests, and rejects grade-two membership.
   Make join resume bind the grade-one state chain and literal digest and
   recompute or independently attest support, sparse SHA and equality between
   the blob SHA and `packed_sha256`.

5. **Remove the common mathematical helper from the independent path.**  Give
   the checker local minimal implementations (or comparisons against pinned
   canonical tables) for the floor group operations it currently shares
   transitively with the producer.  Add a loop over the actual signed
   occurrence columns which asserts every negative column maps
   `u_i -> 2u_j+u_j^2`.  This is helper isolation only; it does not reopen
   row 36, the 648 labels, or any prior classification.

6. **Make fixtures exercise their claims.**  Rehash bounded mutated canonical
   artifacts and pass them through the actual state/blob/DAG/join validators.
   Add the zero/dependent-basis and forward-edge canaries from F3, one real
   independently checked join-residual mutation, and a bounded invocation of
   each existing phase-resume branch.  Relabel or remove the toy dictionary,
   arbitrary connection and hash-round-trip claims.  Production-scale data and
   a real phase are not required for these fixtures.

These are finite serialization, hot-loop and checker edits.  They require no
new mathematical construction, no new closure universe, no re-audit of
row 36/648, and no completed grade-one recomputation.

## 6. Claim boundary

The bounded checks establish neither a production artifact nor a membership
result.  Fixture agreement is not cross-checking, and nothing here is a Lean
proof.

```text
GRADE ONE: terminal still external
GRADE TWO MODULE: audited executable candidate, not a real result
GRADE TWO MEMBER/NONMEMBER: not run
A0 / COMMON / COFINAL LIFT / FAKE / IHARA: not declared
verified=false
```
