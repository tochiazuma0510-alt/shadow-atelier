# Luna task 422 - repair the v3 A0 terminal without changing architecture

## Verdict, role and allowed outputs

You are Luna, the implementation/calculation owner.  Task421 v3 is **NO-GO
before GHA dispatch**.  Keep its v405/v406 two-echelon architecture, but do
not patch or dispatch v3.  Make only the concrete v4 repairs below.

Allowed new outputs only:

1. `search/d972_r07_a0_pb34_direct_quotient_owner_v4.py`;
2. `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v4.py`;
3. `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v4.g`;
4. `sol/luna_reply_422_r07_a0_pb34_direct_quotient_owner_v4_terminal_repair.md`.

Read task421 and v406 completely first.  Do not modify old files, workflows,
proofs, v220, or checkpoints.  Do not run full A0 locally, commit, push, or
dispatch GHA.  This is a minimal correctness repair, not a redesign or a
profiling/framework task.

## A. Repair the occurrence quotient

1. In the PB3 least-serialization transversal, if the selected representative
   is `r=h*z^j_shift`, return the exponent `j=(-j_shift) mod 3`, and assert
   `r*z^j == h`.  The v3 code returns `j_shift`, which is wrong for two of the
   three orbit positions.  PB4 continues to use only the authenticated
   `kappa` split.
2. Preserve the physical block from the occurrence spec.  H1 occurrences
   must carry block 1 and H2 occurrences block 2.  Remove v3's
   `block=1 if spec["block"]<3 else 3`, which collapses both PB3 blocks.
3. Give `tau` the same parseable key schema as every other normal coordinate,
   for example `qkey(block,"tau",b"")`.  `normal_section` must round-trip it.
   The v3 special key `b"Q"+block+b"tau"` cannot be parsed by `parse()`.
4. Add bounded gates for every coordinate kind in both quotients:
   `normal -> sparse section -> normal` is identity; PB3 representatives at
   all three central positions satisfy the reconstruction assertion; H1 and
   H2 remain distinct after tag removal; and acting after choosing another
   representative gives the same normal row.

The sparse section lives in the **new Tietze coordinates**.  Its component
indices for direct contraction are PB3 `b=0,c=1,central=2` and PB4
`b=0,c=1,p=2,q=3,r=4,central=5`.  After lifting and left-moving all normal
terms of one occurrence, call the new-coordinate `contract(block,entries)`
once.  Do not serialize them as old coordinates and call `transform()`
again.  V3 does that at its actor lines 229--230, so it misreads PB3 central
component 2 as old `c` and PB4 central component 5 as old `r`.  Grouping one
contraction per occurrence also avoids repeating the triangular elimination
for every sparse coordinate.

The exact actor remains

```text
Q_o L_(P_o s_o(letter) P_o^-1) iota_o.
```

Keep aggregation from `occ.rows[pivot]`, not from an incoming candidate.

## B. Repair positive ancestry and selected actions

The task413 reduction convention returns coefficients indexed by **original
physical sources**, satisfying

```text
target + sum(coefficient * original_source_row) = 0.
```

For source index `i`, the source row is
`phys.originals[phys.order[i]]`; it is not `phys.rows[phys.order[i]]` unless
that equality is independently true.  Split selected sources as follows.

### Correction source

For a `PHYSICAL` source, authenticate its occurrence pivot and require its
stored original row to equal the fresh aggregation of `occ.rows[pivot]`.
Expand its occurrence expression DAG.  When a `CONJUGATE(letter,parent)` is
expanded recursively, **prepend** the new letter:

```text
new_prefix = (letter,) + parent_prefix.
```

V3 appends it and reverses nested conjugators.  Coefficient two means inverse.
Assemble the finite literal correction word from the resulting compact seed
atoms.

### Action source

For an `action` source, retain and serialize `family_index`, canonical
`translation_blob`, and coefficient.  Reconstruct its exact row from the
explicit six-row `[5:11]` roster and that translation.  Require it to equal
the stored original source row.  Sum these rows separately from the
correction rows.  A positive terminal must accept selected action sources;
v3 rejects every one.

### Strict terminal

Pass all required objects explicitly to the terminal routine; there must be
no free/undefined `quotient` variable.  Then:

1. perform v399 exactification from the registered `r3,r9,r12` words and
   require exact integer exponent pair `(0,0)`;
2. require the exact word to be identity in every joint state;
3. freshly evaluate its eleven unquotiented Fox occurrences and apply the
   three normal maps;
4. require that result to equal the selected **correction** source sum;
5. freshly reconstruct every selected six-action translate and require it to
   equal the selected **action** source sum; and
6. require

   ```text
   target + correction_sum + action_sum == 0
   ```

   across both PB3 blocks, every PB4 noncentral/survivor coordinate, and the
   normalized exponent pair.

Only after all six gates may the producer emit `COMMON_WORD`,
`A0_membership=true`, `common_word=true`, the literal word, correction atoms,
and nonempty action ancestry when actions were selected.  Fake, Ihara,
compatible-lift and verified remain false.  An empty exact negative oracle
may still return `UNKNOWN_RESOURCE`; do not build a new negative framework.

## C. Make resume/progress production-safe without adding overhead

1. Stream checkpoint verification on read: first parse/hash/size-check in
   chunks, then reopen, skip the header, and `marshal.load` through gzip.
   Do not `read()` the full compressed checkpoint into a `BytesIO`.
2. Persist and validate an actual phase in
   `{seeds, occurrence_queue, six_action}` together with seed cursor, deque,
   actor/action cursor, both echelon rows/orders/expressions/sources/originals,
   and the full pin/map binding.  Validate pivot normalization, index/source
   ranges, queue references and phase on restore.  Persist occurrence
   originals too if the Echelon owns them.
3. Print an immediate preflight line, a post-bootstrap line, and progress
   whenever 60 seconds pass or 32 occurrence pivots are added.  Do not write
   the full checkpoint on every pivot/rank rise, including every six-action
   rank batch as v3 does.  Use only phase boundaries, resource stops and a
   coarse time-based interval.  Resource-stop and phase boundaries must
   atomically save it.
4. On every `UNKNOWN_RESOURCE`, the artifact must record the current
   checkpoint byte count and SHA-256.  The driver/checker require that exact
   checkpoint.  Resume an existing authenticated checkpoint; never delete it.
5. In the hot Echelon insertion/reduction loops, update sparse work and
   ancestry dictionaries in place.  Do not call a helper which starts with
   `dict(work)` for every pivot elimination as v3 does: that creates a full
   row copy at every rank and is an avoidable closure-scale time/RSS
   regression.  This is a local axpy repair, not a new optimization project.
6. Remove v3's duplicate direct load of `OLD`/the compact owner when the same
   byte-pinned source is already loaded through task413 `BASE`; the returned
   `mod` is unused.  Keep its tuple in the binding if desired, but do not
   compile the same 68 KB module twice without a consumer.

## D. Replace the symbolic checker and shallow fixtures

The v3 checker is not independent replay: dictionary self-equalities,
`1+1+1`, hard-coded strings, and receipt booleans are not gates.  V4 must not
import the producer and must implement the actual positive replay path with
independent helper code.  On `COMMON_WORD` it must reconstruct and check:

- the 44 literal roster and emitted correction word;
- all joint values and exact exponent pair;
- all eleven old Fox occurrences and H1/H2 separation;
- PB3 least-serialized contraction, PB4 `kappa` contraction and `tau`;
- the explicit six action relations, translations and source coefficients;
- correction/action source sums and the final zero equality.

On `UNKNOWN_RESOURCE`, it must compare the artifact's checkpoint bytes/SHA
with the supplied checkpoint and reject any positive claim.  It may accept a
plain fail-closed `UNKNOWN` only after checking the envelope.

The bounded self-test must exercise real helper paths and reject mutations to
at least: PB3 exponent sign, H1/H2 block, tau key/value, one occurrence actor,
nested conjugator order, normalized-pivot source, one action family,
translation, coefficient, literal word, survivor value, exponent value, and
checkpoint seal.  Include split-run toy fixtures interrupted during seeds and
actors; they must reproduce uninterrupted rank, remainder, and source
coefficients.  Do not call these Lean verification.

The v4 GAP driver pins **both byte count and SHA-256** of producer and checker,
passes `--resume` for an existing checkpoint, streams logs, invokes the
checker with both artifact and checkpoint, and fails unless an
`UNKNOWN_RESOURCE` checkpoint matches the artifact.  A producer/checker
marker alone is insufficient.

Run only `py_compile`, help, and seconds-scale fixtures locally.  Report the
exact commands, outputs, byte counts and SHA-256 values.

`TASK422_R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V4_TERMINAL_REPAIR`
