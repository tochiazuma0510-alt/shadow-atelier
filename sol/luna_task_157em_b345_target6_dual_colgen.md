# Luna task 157em — bounded full-D2 dual column generation for target 6

## 0. Role, scope, and authorized files

Implement one versioned, exact, positive-or-obstruction column-generation
lane after the cross-checked B1 result of run `32401947156`.  Luna may create
or edit only these four implementation/report files:

1. `search/d972_b345_target6_dual_colgen_v1.py`
2. `search/check_d972_b345_target6_dual_colgen_v1.py`
3. `search/d972_b345_target6_dual_colgen_gha_driver_v1.g`
4. `sol/luna_reply_157em_b345_target6_dual_colgen.md`

This Sol-authored task file is the implementation contract.  Do not edit it,
any frozen predecessor, q3 bundle, workflow, claim ledger, dialogue book, or
other repository file.  Temporary self-test output belongs outside the
repository.  Do not run a full production job, GAP, GHA, Git commit, or push;
the parent session owns those actions.

The lane is deliberately bounded but adaptive.  It reconstructs the frozen
prefix B0 and the already cross-checked first complete block B1, repeatedly
solves the same registered 108-variable target-6 affine problem, lifts an
inconsistency dual to the actual sparse group-ring complex, computes the
complete 76-occurrence/full-11-relator correlation, and—only when that
correlation is ACTIVE—adds a canonical batch of complete 11-relator
translation blocks.  It stops on a target-6 solution, a genuine full-D2
separator, an authenticated input failure, or an honest bounded-resource
terminal.  It does not inspect targets 7--33 and must not claim a typed lift,
full H3, B4-A, or B4-B.

## A. Exact frozen inputs and run evidence

Authenticate path, SHA-256, and byte count before self-test or production.
At minimum pin these immediate inputs exactly:

```text
search/d972_b345_lexfirst_block_target6_v2.py
  ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a / 148824
search/check_d972_b345_lexfirst_block_target6_v4.py
  f15a2beeaf1925c1ea4894ef5fae02de6973c36047a91915b7efd12f6d424533 / 21594
search/d972_b345_lexfirst_block_target6_gha_driver_v4.g
  fa288727c77dcbdd8061b066d4863babeaf160dbac8ca4f87ba602a6c7a58836 / 14899
sol/luna_task_157el_b345_lexfirst_block_checker_accounting_v4.md
  755861e724fbd66f88b59b9ad9808703f26e2c8016394cb49c0c9cb09ce1f88a / 16945
sol/luna_reply_157el_b345_lexfirst_block_checker_accounting_v4.md
  af8b33dccc44881fae7533d633922899774738b7dd1c310afbfaeda967417cb6 / 16035

search/d972_b345_full_d2_dual_correlation_v2.py
  6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f / 42449
search/check_d972_b345_full_d2_dual_correlation_v2.py
  881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060 / 21933
search/d972_b345_full_d2_dual_correlation_gha_driver_v2.g
  5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde / 13253
sol/luna_task_157eh_b345_full_d2_monitor_scope_repair.md
  5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e / 15015
sol/luna_reply_157eh_b345_full_d2_monitor_scope_repair.md
  0b595d82e7fa84ce4ee59256e03ca813b55f36a5c0f90d012ad141554fc23bfa / 10817

search/d972_b345_seedspan_triple4_v1.py
  fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29 / 535219
search/check_d972_b345_seedspan_triple4_v1.py
  ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981 / 574347
search/d972_b345_seedspan_triple4_gha_driver_v1.g
  a9c88540c1abdb21dc214d4d4e6461c1431dc407f93542c49e0e65a14788fca4 / 9041
sol/luna_task_157ec_b345_seedspan_triple4.md
  1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2 / 14751

search/d972_b345_q3_chief_v1.g
  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755 / 76867
search/check_d972_b345_q3_finite_v1.py
  ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73 / 89082
search/d972_b345_q3_gha_driver_v1.g
  c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831 / 5488
```

If the actual q3 filenames in the frozen v2 import table differ, preserve the
frozen paths and the three hashes above; do not silently substitute or repin.
Retain every transitive pin authenticated by the frozen chain.  The new
producer and checker must authenticate this final 157em task by its reported
SHA and byte count.  The driver must pin the final producer, checker, task,
and every immediate predecessor used at runtime; it must not pin the mutable
final reply.

Run `32401947156`, exact head
`2808c3fb61962d7180a192947fed375c754a25ce`, is cross-checked evidence.  Its
canonical receipt is 1,314,365 bytes with SHA-256
`746ca938a962f4d918c07ee270d4e03c3e4f75e40689f3a0507c8daff9d57053`.
It must not be imported as a basis, affine system, pool, or proof object.  A
fresh same-job construction must reproduce the stable values below before
continuing:

```text
B0: columns=362725, pivots=362709, dependent=16,
    live_sparse_entries=3090367
B1: columns=362736, pivots=362720, dependent=16,
    live_sparse_entries=3090463
B1 first block: translation ordinal 32976, 11 ordered relators,
    old-qstar scalars [0,0,0,0,0,0,0,0,1,0,0], rank gain 11
B1 target6: variables=108, equations=33687, rank=54, nullity=54,
    consistent=false, complete=true
```

Bind the following stable digests after fresh reconstruction:

```text
B1 raw columns       01ee4f1c1d833b82cedc4728b2b642237e503bac72faab8b28133f29e1075d0f
B1 reducer ledger    171e40b114dc23b4a4656e8cdfd904beef766f3349c0decc317dca924bbc166e
B1 anchor semantic   8ef207454deb76ae49daabe3241b4ca5c70e873fdb5be59010fb35e63f04c74a
B1 target row space  5dd0bd3411afae0a9adafca4254b6fda739774a8b970b59e661d67e686f549be
B1 fresh remainders  9cfd9adc23c9b4dff3d9415f06ce0d0df5fe53b0bf5394aaa8ef667f1b55d407
B1 typed split       96e906aaee06d8748dd5c48c9fb3e9d009a185abdee91d8b66f14d545541f545
B1 direct bindings   32d0b157b4ddbc212ac595543c38f3de5467800cb50bef8361f2c0fbf62ff214
B1 dual support/equations projection
                     f8b1cb6325b158f0984ca945dac2c0e915e0386e1f13ddb911acf0e4e2d9dcad
B1 dual whole canonical public object
                     005d0ad3f9e9c3aa8182108ab13ceed9108594aedec68d3913c5b752646bcc93
B1 dual annihilation 400f67f74b1250e538c395aa8bf647f6f7432ec07fe2582aaff06e5a47fe7ed5
prefix source        d41123a8c4803f6ac67387ac9bbf1a32f797b90d6233605a5511713f215244be
prefix dependents    77ba0632b468c1cb543e1f3eded6c63d52c806686a48e8fa8248de334cebadee
```

The B1 public normalized dual happens to have support count one.  That label
is an affine quotient coordinate.  It is not the old 157eh raw `qstar`, and
neither its blob nor its pool ID may be substituted into the old support-one
oracle.  This distinction is load-bearing.

For performance calibration only, the older B0 run `32374248796` had complete
correlation counts 886 attempted support/occurrence pairs, 724 noncombined
candidates, 156 cancellations, and 568 ACTIVE `(translation,relator)` rows.
Its receipt SHA is
`7c9de4d4aa5dc0facf94cec9c4b2b71d81c1b8cc590e84aa574cace18c1cb7d5`.
Those numbers are not assumed at B1 or later.

## B. Fixed mathematical universe and notation

Work only in the same pinned E4 and sparse group-ring/Fox complex as
157ec/157eh/157el.  Let B0 be the fresh 362,725-column prefix, and let B1 be
B0 plus the fixed cross-checked complete 11-relator block.  Every later Bk is
obtained only by adding exact left translations of the same eleven base D2
relator columns.  Consequently

```text
B0 <= B1 <= ... <= D2_full.
```

The correction universe remains exactly the ordered 108 registered seeds and
coefficients in `F3^108`; no seed, target, roof, quotient, coface, relator, or
candidate order may be added or removed.  Rebuild and hard-gate the same six
pinned source roots, the exact target-plus-six value-root closure, all source
tuples, target-6 base raw gradient, 108 delta gradients, formula/direct
equality, and typed direct canaries.  The 109 raw gradients may be retained as
semantic sparse rows for this job, but no predecessor remainder or dual is an
input.

Build a compact, authenticated raw-Fox parent table while constructing those
109 gradients.  Every initial nonzero semantic term must point to its exact
`(source_word_ordinal, signed_letter_offset)` Fox occurrence and the canonical
prefix-section root at that occurrence.  Repeated occurrences use the
lexicographically earliest exact parent tuple; hashes are not equality.
Seed the same recovery table with all 76 occurrences of the eleven base D2
columns, with their exact relator/word/offset and prefix-section roots; the
frozen 76-occurrence digest remains load-bearing.  The target-gradient parents
alone do not justify recovering a tail coordinate introduced from a D2 row.
Instrument the actual fresh-prefix `add_column` path: for every translated
column in B0 (all BFS and directed-surgery columns), the fixed B1 block, and
every new batch, extend a separate recovery map by the canonical relation

```text
new_group_element = registered_translation_u * parent_group_element_g.
```

The edge records the semantic blobs, the exact registered section root for u,
the parent root for g, relator/term ordinals, and the resulting expression
root.  Edges are acyclic and chosen by one frozen raw-byte lexicographic rule.
The instrumentation is observational: it may not alter translation order,
column bytes, reducer calls/outcomes, pool interning, or the frozen B0/B1
anchors, and an exact state-neutrality ledger must prove this.
Thus every group element occurring in a current pivot/tail row, and hence
every nonzero raw-lambda support element, has a reproducible source section.
After authenticated construction, failure to recover such an element is an
invariant violation and a hard FAIL—not UNKNOWN_INPUT, a zero scalar, or a
reason to skip that contributor.  Physical node/edge/materialization caps may
still yield honest UNKNOWN_RESOURCE before a false receipt is emitted.

Use semantic group-ring coordinates throughout public data:

```text
(component one-based 1..6, exact canonical E4 blob of 154 bytes)
```

Pool IDs are private implementation indices.  They may be used only inside a
single authenticated pool lifetime and never in a stable digest, cache key,
dual label, cross-iteration equality, or producer/checker comparison.

## C. Preregistered bounded adaptive algorithm

Freeze these values before any result is observed:

```text
MAX_BATCHES                    = 8
MAX_TRANSLATIONS_PER_BATCH     = 1024
MAX_TOTAL_NEW_TRANSLATION_BLOCKS = 4096
RELATORS_PER_BLOCK             = 11
MAX_TOTAL_NEW_RELATOR_COLUMNS  = 45056
```

`MAX_TOTAL_NEW_RELATOR_COLUMNS` equals 11 times the total block cap.  B1's
already frozen first block is not counted among the 4,096 new blocks.  The
implementation may use smaller physical caps only if this task is amended and
refrozen before production; it must not adapt a cap after seeing a run.

At basis Bk, starting with k=1:

1. reduce the target-6 base and all 108 delta rows and solve the complete
   transposed affine system in the fixed variable order;
2. if consistent, perform the selected literal/direct/proof replay and stop;
3. if inconsistent, normalize its dual, lift it to an exact raw functional
   lambda_k, and compute the complete full-D2 correlation;
4. if every correlation scalar is zero, stop with the full-D2 obstruction;
5. otherwise group nonzero rows by semantic translation blob, sort blobs by
   raw canonical bytes, and select the first

   ```text
   min(active distinct translations,
       MAX_TRANSLATIONS_PER_BATCH,
       remaining total block budget)
   ```

   translations.  If all ACTIVE translations fit, this is an all-ACTIVE
   batch.  If not, it is the exact canonical prefix; record the truncation and
   total counts.  Never select by pool ID, hash iteration order, relator, or
   section-recovery convenience;
6. before persistent mutation, stage every selected section and all eleven
   raw/typed/scalar columns and pass the full preflight in D.4; then, in
   selected-blob order, register/reuse the exact section and add the complete
   relator block `j=1..11`.  Do not add only ACTIVE relators.  Dependencies are
   valid outcomes and remain in the packed ledger;
7. incrementally reduce the same 109 semantic raw gradients through only the
   newly introduced normalized pivot rows, rebuild the target-major affine
   system, and continue.

After the eighth completed batch, B9 must still be solved and, if
inconsistent, correlated.  A consistent or zero-correlation result at B9 is
mathematical.  If the complete B9 correlation remains ACTIVE, return
UNKNOWN_RESOURCE; the top-level `reason` must equal the exact `cap_key`, while
the human-readable algorithmic explanation belongs in a separate `detail`
field.  Resolve simultaneous stopping conditions in this fixed order:

1. if `remaining total block budget == 0`, use
   `reason == cap_key == "total_new_translation_blocks"` and
   `detail == "total_translation_block_budget_exhausted"`, with
   `limit=4096`, `observed=4097`, `comparison="gt"` for the first forbidden
   next block;
2. otherwise, if eight batches are complete, use
   `reason == cap_key == "column_generation_batches"` and
   `detail == "column_generation_batch_limit"`, with `limit=8`,
   `observed=9`, `comparison="gt"` for the forbidden next batch.

The derived relator-column cap is exactly eleven times the block cap and does
not compete as a second reason at the same boundary.  Gate that arithmetic;
use the block cap as the canonical reason.  Do not call ACTIVE,
nonconvergence, or either cap a negative mathematical result.

This bounded all-ACTIVE/canonical-prefix batching is preferred to a one-block
run because the expensive 109-row reduction was about 332 seconds per side in
the predecessor.  It is preferred to an unbounded all-ACTIVE batch because a
new multi-support raw dual can have far more than the observed 568 B0 rows.
The caps above preserve a finite, preregistered universe and an honest UNKNOWN
boundary.

## D. Load-bearing exact lemmas and gates

### D.1 General reverse-pivot raw lift

Let the normalized inconsistent affine system be `A a = b`, where
`b=-z` and z is the reduced target-6 base row.  Its public dual y must satisfy

```text
y A_i = 0 for i=1..108,       y b = 1.
```

The affine public support is a set of nonpivot semantic coordinates.  Lift y
to lambda on all raw semantic coordinates of the current normalized basis as
follows.  Initialize lambda(q)=y(q) on every public support coordinate and
lambda(q)=0 on every other free coordinate.  For each normalized pivot row

```text
r_p = e_p + sum_{q>p} a_q e_q
```

in reverse exact pivot order, set

```text
lambda(p) = - sum_{q>p} a_q lambda(q) mod 3.
```

The implementation must use canonical `(component,blob)` labels, a frozen
pivot-order comparator, and non-interning absent lookups.  It must reject a
cycle, a non-strict tail, duplicate semantic labels, a public support pivot,
or any pool-lifetime mismatch.  Publish only the support count, per-component
counts, canonical packed support digest, pivot-annihilation digest, dependent
event digest, completed-block annihilation digest, and bounded first/last
canaries; do not serialize a multi-megabyte raw support table.

Hard-gate, not merely diagnose:

```text
lambda(r_p)=0 for every current pivot row;
lambda(c)=0 for every B0 dependent raw column and every previously added
  block column;
lambda(delta_i reduced)=y A_i=0 for all 108 i;
lambda(-z reduced)=y b=1;
lambda(z)=2.
```

The sign `lambda(z)=2`, not 1, follows from `b=-z`.  The old support-one qstar
oracle/object/hash must never be reused.  A support-one affine y still goes
through this general reverse-pivot lift.

### D.2 Complete 76-occurrence correlation

Rebuild the exact eleven base D2 columns and their private Fox occurrence
rows.  Hard-gate the frozen base occurrence digest
`3eacd6dc77d62c1799a55923d3c8d5313a37ceab8e78b58b07b45925a28f131d`,
exact total occurrence count 76, relator indices 1..11, component widths, and
the per-relator support distribution.  There are 76 occurrences total, not
76 occurrences for each relator.

For a raw-lambda support row `(component c, group element g, coefficient l)`
and a matching-component occurrence `(relator j, element h, coefficient a)`,
the left-translation key and contribution are exactly

```text
t = g * h^-1,          contribution = l*a mod 3.
```

Correlation has exactly two passes.  Pass 1 enumerates every matching pair
once, accumulates only scalars by `(154-byte translation blob,relator)`,
combines modulo 3, deletes exact zeros, and sorts the ACTIVE rows by that
semantic key.  It enumerates exactly
`sum_c |support_c|*|occurrences_c|` pairs, not an invented
`support*76*11` product.  Hashes are bucket accelerators only; equality and
ordering use full canonical blobs.

After scalar combination and bounded batch selection, define for each selected
translation

```text
j*(t) = min { j in 1..11 : scalar(t,j) != 0 }.
```

Pass 2 is one selected-only global pass over the same matching-pair stream.  It
must not rescan once per translation.  It ignores every pair not contributing
to a selected `(t,j*(t))` and chooses that pair's canonical contributor by the
lexicographically least exact 314-byte record

```text
component:u8 | g_blob:154 | lambda_coefficient:u8 |
relator:u8 | occurrence_ordinal:u16-big-endian |
h_blob:154 | occurrence_coefficient:u8
```

with no padding.  Bind both pass ledgers: attempted pair count, selected-filter
count, zero/cancellation counts, ACTIVE and distinct-translation counts,
canonical semantic SHA-256, and visit-cap/noncontact fields.  Pass 2 occurs
exactly once after Pass 1 and selection.  It may not change a scalar, selected
translation, or j*.  Both passes have explicit per-generation and cumulative
visit caps.

Neither pass may intern an absent element, mutate the
pool/basis/DAG/sections, retain full sparse translated columns, or materialize
the full E4 universe.

If the resulting table is empty then lambda annihilates every E4-left
translation of all eleven base columns, hence annihilates the full D2 image.
Together with `lambda(delta_i)=0` and `lambda(z)=2`, this proves that no member
of the registered `F3^108` correction family solves target 6 modulo full D2
for this pinned E4 roof.  It proves nothing about another correction universe,
roof, target, H3, or global B4.

Required direct canaries include identity translation, inverse orientation,
one scalar-1 row, one scalar-2 row, cancellation to zero, a complete direct
translated column, and a small independently brute-forced nonabelian toy.

### D.3 Exact section-prefix provenance for every selected translation

For each selected semantic translation t, use exactly the Pass-2 contributor
for its fixed earliest ACTIVE relator j*(t).  Its support element g and base
occurrence element h satisfy `t=g*h^-1`.  Recover exact typed section roots for
g and h from the authenticated raw-Fox/recovery map and construct the
expression DAG node

```text
MUL(section(g), INVERSE(section(h))).
```

The source word need not be flattened for every selected translation.  Use a
lane-owned recursive materializer.  Its actual `INVERSE` opcode must first
reserve the exact output-letter count through the current `BoundMonitor`, then
invoke the authenticated signed-word inversion operation `old.inv_word` on
the materialized child.  Do not call an unowned or nonexistent
`inverse_word`, allocate before reserve, or bypass the monitor in fixtures.

The expression DAG must replay to the exact 154-byte t blob; its
reachable-node subgraph, opcodes, child order, source leaves, value digest,
and canonical contributor record are load-bearing.  Materialize and directly
replay at least the first and last selected translation of every batch and a
deterministic cadence no weaker than every 64th translation.  The checker
independently replays every expression DAG value and materializes the same
canary schedule.  A production-path fixture must execute a real `INVERSE`
node through this exact owned materializer and reject wrong child order,
missing reserve, and a fake inverse API.

If t already has an exact section binding, reuse only after value and
provenance equality.  Otherwise register it exactly once before its block.
Never skip an earlier canonical t because a later one is easier to recover.
A cap hit during recovery is UNKNOWN_RESOURCE with the exact cap key and
partial canonical prefix.  Once the input and recovery instrumentation have
authenticated, a missing leaf/edge, a nonrecoverable g or h, or a wrong
materialized value is an invariant breach and hard FAIL, never UNKNOWN_INPUT.
It is never silently treated as a zero correlation or dependency.

### D.4 Complete 11-column batch insertion

Before the first persistent mutation of a batch, stage every selected t and
all eleven relators.  For each of these rows precompute:

- the direct semantic raw left-translated column;
- the typed section/DAG Fox column;
- their exact equality and canonical raw-column SHA-256;
- quotient identity and D1/D2-zero gates;
- `lambda_k(column)` and equality with the completed Pass-1 scalar table.

The entire selected batch must pass this preflight within its declared sparse
entry, expression, inverse-letter, and RSS reserves before any section,
pool, DAG, basis, or remainder state is committed.  A staging registry may be
used, but it must have a transaction checkpoint and exact value replay; it is
not the persistent prefix until the whole preflight succeeds.  This prevents
an early block from changing the interpretation or resource availability of a
later selected row.

After preflight, commit in translation order and relator order 1..11.  Record
independent/dependent outcome and semantic pivot projection for every column.
Do not serialize the per-column ledger as JSON dictionaries: at the maximum
universe that representation was estimated above 292 MB and can itself exceed
the receipt budget.  Use these exact packed public tables:

```text
translation table:
  selected translations in generation/translation order, each exact 154-byte
  blob; no padding

column outcome record (exactly 225 bytes, no padding):
  generation:u8 |
  translation_ordinal_within_generation:u16-little-endian |
  relator:u8 | flags:u8 | lambda_scalar:u8 |
  pivot_component:u8 | pivot_blob:154 |
  raw_column_sha256:32 | typed_column_sha256:32
```

`flags` has the frozen allocation bit0=`independent`,
bit1=`direct_equals_typed`, bit2=`quotient_identity`, bit3=`D1_D2_zero`, and
bits4..7 exactly zero.  For a dependent column, `pivot_component=0` and
`pivot_blob` is exactly 154 zero bytes; for an independent column the
component is 1..6 and the blob is the semantic pivot.
The record order is generation, selected translation, relator.  Publish exact
encoding name/version, endianness, record count, decoded byte length,
base64 length, decoded SHA-256, base64 SHA-256, and canonical translation-table
SHA-256.  Reserve decoded storage and base64/JSON expansion through the
monitor before allocation.  The checker decodes the fixed layout, checks
length/no-padding/unused bits, independently rebuilds every raw and typed
column, and compares every record.  No Python tuple/object serialization or
pool ID is a public substitute.

For the first selected translation t0, hard-gate from the staged scalar vector
that every relator `< j*(t0)` has scalar zero and relator `j*(t0)` has scalar
1 or 2.  Because lambda annihilates Bk, the zero-scalar earlier relators leave
lambda well defined on the enlarged span, and the `j*(t0)` column must produce
an immediate pivot increment of exactly one when absorbed.  Gate that exact
event, not merely total batch rank gain.  Later relators/selected blocks may
be dependent after preceding additions; do not require per-block rank gain.
An ACTIVE translation cannot already have a complete eleven-column block in
Bk; gate this fact, while allowing some individual relator columns or a
partial block to be dependent.

Every committed column is an actual full-D2 column, so batching only enlarges
the known subspace and cannot create a false positive.  It does not itself
prove membership or termination.

### D.5 Incremental normal-form theorem

Retain the 109 B1 semantic remainders in memory.  When a batch adds normalized
new pivot rows whose pivot coordinates were free in Bk, update each remainder
by reducing it through the new pivots in exact pivot order.  The required
identity is

```text
NF_{B(k+1)}(v) = NF_{new pivots}(NF_{Bk}(v)).
```

This is valid only if every new normalized row has zero at every old pivot,
has leading coefficient one, and has a strictly later canonical tail.  Gate
all three conditions.  Do not reuse a remainder after pool rollback, pool-ID
renumbering, changed comparator, or incomplete block transaction.

At every generation compare incremental and fresh-direct reductions for the
base and seeds 1, 54, and 108.  The production self-test must also compare all
109 rows on a small nontrivial fixture.  The independent checker implements
the update separately and repeats the direct cadence; it must not trust a
producer `incremental_equal` boolean.  If a consistent solution is selected,
freshly rebuild and directly reduce its actual typed target gradient through
the entire current basis and construct the proof DAG before accepting.

Incremental update has an exact RESOURCE transaction.  Progress records the
generation, completed new-pivot ordinal, completed remainder ordinal in
`0..108`, pre-update remainder digest, last fully updated row digest, current
new-pivot-prefix digest, live entry count, and whether the persistent batch
anchor has committed.  On a mid-row or mid-pivot cap hit, either rollback all
109 remainders to the pre-update snapshot or publish only this exact
nonmathematical partial state.  It may not publish a mixture as B(k+1), reuse
partly updated rows on resume, or retain a completed affine/dual/terminal
field.  The checker independently reconstructs the same completed prefix and
requires the remaining rows to be explicitly null, not copied from Bk or
filled with empty dictionaries.

## E. Exact terminal meanings and claim boundary

Use exactly four terminals (final spelling may add a version suffix only if
producer/checker/driver/task agree exactly):

```text
B345_E4_D2_COLGEN_TARGET6_CONSISTENT
B345_E4_D2_COLGEN_TARGET6_FULL_D2_OBSTRUCTION
B345_E4_D2_COLGEN_TARGET6_UNKNOWN_RESOURCE
B345_E4_D2_COLGEN_TARGET6_UNKNOWN_INPUT
```

### CONSISTENT

Accept only after a complete 108-variable solve at some Bk, canonical
coefficient extraction, direct literal target-6 replay, exact affine/direct
gradient equality, fresh full-basis reduction to zero, and an independently
replayable D2 proof DAG.  Exact claim:

```text
one registered-108 correction solves target6 modulo the current generated
full-D2 subspace Bk for the pinned E4 roof; targets 7..33 are not checked.
```

This is not yet a typed lift or B4 conclusion.

### FULL_D2_OBSTRUCTION

Accept only after an inconsistent complete affine solve, exact general raw
dual lift, and a complete zero full-D2 correlation.  Exact claim:

```text
no coefficient vector in the registered F3^108 correction family solves
target6 modulo full D2 for the pinned E4 roof.
```

This is family- and roof-relative, not global nonexistence.

### UNKNOWN_RESOURCE

Use for a declared cap/deadline/RSS/serialization hit, section-oracle resource
hit, exhausted batch count, or exhausted total block budget while the last
complete correlation is ACTIVE.  Always require top-level
`reason == resource.cap_key`; a phrase such as
`column_generation_batch_limit` appears only in `resource.detail`.  Apply the
total-block-before-batch precedence in section C.  Claim `none`.  Publish only
a stage-aware, exact partial prefix and no provisional solution, separator, or
ACTIVE mathematical conclusion.

### UNKNOWN_INPUT

Use only for authentication, pinned schema/API, quotient/source, canonical
encoding, or required exact-provenance failure external to the mathematical
search.  Claim `none`.  Mathematical drift after authenticated construction
is a hard failure, not a convenient UNKNOWN_INPUT.

## F. Receipt, transactions, caps, and stable binding

Use a new exact schema, for example
`d972-b345-target6-dual-colgen/v1`, with exact stage-aware top and nested key
sets.  At minimum bind:

- all authenticated pins and the same-job q3 receipt SHA;
- fresh B0 and B1 stable anchors/digests from section A;
- fixed algorithm constants and closed cap/reason registries;
- the exact 108-seed/source/target raw-gradient manifest and compact initial
  `(word,offset)` raw-Fox parent/recovery-map roots;
- an ordered generation ledger for B1 through the terminal basis;
- per generation: pre/post basis accounting, target rank/nullity/equation
  count/digest, normalized affine-dual whole/support-projection digests,
  dynamic raw-lambda support/reverse-edge counts and annihilation digests,
  exact correlation Pass-1/Pass-2 visit/cancellation/ACTIVE ledgers and
  semantic digests, selected/truncated translation counts, contributor and
  section-recovery DAG digests, packed complete-block table metadata/digests,
  rank gain, new pivot digest, incremental-remainder/partial digest, and phase
  timing outside stable hashes;
- terminal-specific selected proof or full-D2 separator proof;
- exact performance/resource/partial records.

The generation ledger order is basis order, then translation blob order, then
relator 1..11.  Stable projections exclude elapsed time, RSS, Python object
IDs, pool IDs, allocation counts not semantically pinned, temporary paths,
and hash-table iteration order.

Batch insertion is transactional at the public boundary.  On RESOURCE during
a staged precompute, no persistent state may have changed.  On RESOURCE during
a committed block, either rollback the whole unfinished block to its exact
checkpoint, or publish a non-mathematical partial receipt containing only the
completed canonical block prefix and enough packed accounting for checker
replay.  Never call an 11-column block complete after fewer than eleven
attempted columns.  A completed batch anchor must bind the actual live basis,
pool, DAG, section registry, raw-coordinate recovery map, packed block ledger,
and 109 remainder state.  Preserve the 157el distinction between the
checker-private six-field semantic replay ledger and the producer-public
eleven-field accounting ledger.

The closed local cap registry must include at least:

```text
column_generation_batches             8
translations_per_batch              1024
total_new_translation_blocks        4096
total_new_relator_columns          45056
affine_variables                     108
affine_rows                      1000000
target_live_remainders           2000000
dual_public_provenance_entries       128
raw_lambda_support_entries        2000000
raw_lambda_reverse_edge_visits    8388608
raw_coordinate_parent_entries     2000000
raw_coordinate_recovery_nodes     2000000
raw_coordinate_recovery_edges     4194304
inverse_materialized_letters      4194304
correlation_pass1_pairs_per_generation 8388608
correlation_pass2_pairs_per_generation 8388608
correlation_pass1_pairs_total    75497472
correlation_pass2_pairs_total    67108864
distinct_correlation_candidates   2000000
packed_active_rows                2000000
batch_staged_sparse_entries        262144
packed_translation_table_bytes    1048576
packed_translation_table_base64_bytes 1398104
packed_block_ledger_decoded_bytes 16777216
packed_block_ledger_base64_bytes  22369624
common_math_soft_deadline_seconds   18000
producer_soft_rss_bytes          4831838208
packed_receipt_bytes              268435456
```

Every dynamic lift/recovery/correlation counter is monotone and published per
generation and cumulatively.  Check/reserve before the operation that would
cross a cap; `observed` is the attempted post-operation value and comparison
is fixed (`gt` for count capacities, `ge` for wall/RSS as inherited).  Pass-1
totals cover at most nine correlations B1..B9; Pass-2 totals cover at most the
eight batches that can actually be selected.  A zero-correlation or final B9
ACTIVE classification does not manufacture a Pass-2 visit.  Cap aliases,
counter resets per generation, or reclassifying a lift cap as an input error
are forbidden.

Inherit the exact structural pool/DAG/section/resource caps reachable through
the frozen builders.  Keep local versus upstream cap sources separate, require
`reason == cap_key`, and map every reachable monitor phase explicitly.  One
closed outer phase set must cover at least `authenticated_input`, `fresh_B0`,
`fixed_B1`, `initial_target`, `dual_lift`, `correlation_pass1`,
`correlation_pass2`, `batch_precompute`, `section_recovery`, `block_commit`,
`incremental_reduction`, `target_resolve`, `selected_proof`,
`receipt_serialization`, and `complete`; generation is a field, not a way to
invent dynamic phase names.  Map every reachable inherited inner monitor
name to exactly one of those outer phases and reject an unknown name.  One
absolute deadline begins before authenticated input and is passed through all
producer phases; do not reset it per generation or in the checker.  Detach a
temporary monitor from basis/DAG in `finally` and hard-gate identity before
and `None` after every phase.  Receipt serialization overflow must go through
the production checked-write fallback, exact readback, and a cross-checkable
RESOURCE receipt.

## G. Independent checker contract

The checker may authenticate and import frozen constructors, but must not
import the new producer or share its raw-lambda, correlation, batch-selection,
incremental-reduction, terminal, receipt-finalizer, or proof helper.  It must:

1. independently authenticate q3 and all frozen pins;
2. rebuild B0 and B1 fresh and verify every stable anchor;
3. independently reconstruct all 109 raw gradients, compact `(word,offset)`
   parents, recovery-map edges, and typed/direct gates;
4. for every generation, independently solve the affine system, derive and
   normalize y, lift the general raw lambda, enumerate both complete
   correlation passes with the same raw-byte contributor rule, select the same
   canonical bounded batch, recover every selected section expression through
   the owned monitored materializer, precompute every selected raw/typed/
   scalar row before mutation, decode/rebuild the packed ledger, replay all
   eleven columns, absorb them, and update/recheck remainders;
5. independently derive the terminal and exact claim;
6. replay a selected proof or full-D2 annihilation certificate rather than
   trusting producer booleans/digests;
7. require exact schema/key sets, cap/reason/phase consistency, stable digest,
   checked-write bytes, and exactly one terminal.

Producer and checker pool schedules need not have equal private IDs.  They
must compare the same semantic `(component,154-byte blob)` projections.  A
checker that simply calls the producer's `run`, `validate_receipt`,
`RawLambda`, correlation, or batch core is not independent.

## H. Mandatory production-path self-tests and mutations

Run the real production validators/cores on bounded fixtures, not parallel
schema-only toys.  Require exact call counters/markers proving each shared
production branch ran.  Include at least:

1. a sealed bounded B0-to-B1 provider passed through the same production
   anchor/block validator; it carries small fixture counts/digests and must
   never claim the real 362,725-column prefix;
2. a nontrivial multi-support reverse-pivot example with direct dot-product
   comparison, plus wrong sign, wrong reverse order, pivot-in-support, cycle,
   non-strict tail, duplicate blob, absent-key interning, stale pool-ID, and
   old-qstar-substitution, dynamic-count reset, and every lift-cap boundary;
3. a tiny nonabelian group brute-force correlation equal to the optimized
   semantic recurrence, plus inverse-orientation, component, coefficient,
   cancellation, omitted occurrence, duplicated occurrence, wrong relator,
   unsorted blob, 76-versus-`76*11`, Pass-2-before-scalar, repeated Pass 2,
   per-selected rescan, contributor raw-byte order, and visit-cap mutations;
4. ACTIVE rows sharing one translation, multiple ACTIVE relators, more than
   the per-batch cap, deterministic canonical truncation, duplicate
   translation, and all-ACTIVE-below-cap fixtures;
5. initial `(word,offset)` parent and translated `u*g` recovery, section
   recovery through `g*h^-1`, inverse-child swap, missing contributor, stale
   expression root, wrong blob, already-registered exact reuse, and
   materialization cadence mutations; the fixture must execute the actual
   production `INVERSE -> reserve -> old.inv_word` branch;
6. all-selected/all-11 precompute before mutation, exact scalar equality,
   first t's zero-before-j* and immediate j* pivot theorem, later dependent
   blocks, partial preexisting block, relator reorder, packed 225-byte
   encode/decode/endian/no-padding/flags/hash/base64 tests, JSON-ledger reject,
   6-key checker replay versus 11-key public accounting separation, and
   incomplete transaction RESOURCE;
7. an interleaved-pivot incremental-normal-form fixture comparing all rows to
   fresh reduction, plus old-pivot leakage, leading coefficient 2, tail-order
   reversal, rollback reuse, skipped-new-pivot, and exact mid-incremental
   partial/remaining-null mutations;
8. exact target-plus-six value-root closure and source omission mutation;
9. consistent, zero-correlation obstruction, ACTIVE-at-final-batch RESOURCE,
   mid-correlation RESOURCE, mid-section RESOURCE, mid-block RESOURCE,
   target-reduction RESOURCE, serialization RESOURCE, INPUT, stale terminal,
   extra/missing nested key, wrong reason/cap source/phase, simultaneous B9
   and total-block precedence, reason/detail swap, and competing terminal
   fixtures;
10. module lifecycle collisions for every fixed dynamic import, wrong
    path/SHA/bytes/API/schema canaries, three-key prefix projection, monitor
    attach/detach identity, and checked-write exact readback.

The mutation table must report every named mutation and exact rejection count.
No exception-message substring alone counts as a semantic self-test.

The bounded B0-to-B1 provider is sealed test data, not a shortcut into main.
It must expose the same production interface and invoke the same production
validator/core, while carrying an explicit `sealed_bounded_fixture=true` gate.
The self-test must install a trap proving the full prefix builder/main entry is
unreachable, and must reject any fixture receipt that says
`fresh_immutable_prefix`, uses the 362,725/362,709 production counts, imports a
production stable digest, or claims a full-prefix/B1 mathematical result.
Conversely production must reject the sealed provider.  Self-test markers may
claim only bounded production-path validation, never construction or checking
of the real 362k prefix.

## I. Thin driver and same-job gates

The new GAP driver is orchestration only.  It must:

- authenticate exact producer/checker/task/upstream paths, SHA-256, and byte
  counts before launching Python; do not pin the mutable final reply;
- preserve the proven quoted `Exec` convention, shell exit/sentinel handling,
  stale-output deletion, run-log markers, and exactly-one-marker gates;
- build and independently check the exact q3 artifact in the same job before
  the new producer; never accept a stale local q3 receipt;
- pass one common remaining deadline to producer and checker without reset;
- require producer PASS, checker PASS, driver PASS, matching receipt SHA, and
  exactly one of the four terminals before artifact promotion;
- accept no old 157el producer candidate or runner-local receipt as the new
  result;
- keep live phase progress visible and fail closed on missing/truncated output.

Self-test mode must execute producer and checker production-path self-tests and
all marker/pin/terminal fixtures without running the full 362k-column job.

## J. Recurrence-prevention table

The reply must explicitly confirm each item:

| Previous failure mode | Required prevention here |
|---|---|
| old support-one qstar reused | general semantic reverse-pivot lift; old oracle reject canary |
| support label had no source section | initial `(word,offset)` parents plus canonical translated `u*g` recovery edges |
| inverse materializer typo/unbounded allocation | owned `INVERSE`, monitored reserve, authenticated `old.inv_word` |
| target root evaluated without six source roots | exact target-first union and omission reject |
| pool-ID schedule compared cross-language | public semantic blobs only |
| direction `h*g^-1` substituted | exact `g*h^-1` theorem and mutation |
| ACTIVE relator alone added | complete ordered 11-relator block per selected t |
| unbounded all-ACTIVE expansion | 1024 per batch, 4096 total, max 8 batches |
| contributor chosen before cancellation | scalar Pass 1, then one selected-only Pass 2 and fixed j* |
| early block mutation changed later inputs | all selected 11 raw/typed/scalar rows precomputed before commit |
| JSON block ledger exceeded receipt cap | fixed 225-byte packed records, base64 bounds and exact decoder |
| one block per expensive solve | canonical batched insertion, one solve per completed batch |
| stale remainder reused | incremental-NF hypotheses plus fresh direct cadence |
| 6-field/11-field ledger conflated | separate checker-semantic and producer-public validators |
| prefix projection omitted a key | exact `directed_base_support`, `directed_surgery`, `prefix` projection |
| monitor phase/identity leak | closed registry and attach/detach `finally` gates |
| dynamic module collision | exact key/path/SHA/bytes/schema/API reuse or fresh-load gate |
| RESOURCE promoted partial math | exact stage partial, claim none, no provisional terminal |
| RESOURCE reason differed from cap key | `reason==cap_key`; detail separate; total-block precedence fixed |
| fixture pretended to build full B0 | sealed bounded provider through production validator; main trapped |
| volatile values in stable SHA | stable projection excludes elapsed/RSS/object IDs |
| checker copied producer result | independent dual/correlation/block/reduction replay |

## K. Runtime and final report

The measured predecessor took about 707.5 seconds producer-side and a similar
checker time, with peak producer RSS 787,005,440 bytes.  B1's 109 remainder
rows had 225,579 live entries.  In the worst case that all 568 B0 ACTIVE rows
had distinct translation blobs, an all-ACTIVE batch would add at most 6,248
columns, only about 1.7 percent of the 362,725-column prefix; this is
calibration, not a B1 prediction.

Expected full-job bands after incremental reuse:

```text
normal, stop within 1--2 batches:      30--70 minutes
pessimistic, several bounded batches:  90--180 minutes
hard outer allowance:                  300 minutes
```

If profiling contradicts those bands, return an honest self-test/design STOP
before dispatch rather than weakening a predicate or silently lowering the
universe.  The reply must report final producer/checker/driver hashes/bytes,
exact diff scope, self-test commands/markers, mutation totals, cap registry
digest, import/pin table, measured self-test runtime/RSS, expected production
bands, and any residual risk.  Its own final reply SHA/byte count must be
reported out-of-band after freeze and must not be embedded in the reply.  Use
`cross-checked` only after a full producer/independent-checker run; reserve
`verified` for Lean.
