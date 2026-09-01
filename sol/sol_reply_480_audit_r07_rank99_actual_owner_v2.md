# Sol reply 480 - R07 rank-99 actual-owner v2 adversarial audit

## Verdict

**STOP.  Do not dispatch Task472 v2 as-is.**

The submitted producer is no longer the Task468 zero-work stub: its default
path really attempts the Task451 construction, frozen physical replay,
selector, delayed-retain loop, batch closure, and COMMON replay.  Nevertheless
it is deterministically non-executable at the first frozen rank-51 correction.
Both producer and checker call a one-argument frozen arithmetic function with
three arguments.  In addition, the checker does not bind the top-level result
rows to the durable rows that it actually replays, so a self-sealed semantic
mutation of the result can be accepted.

The later v427 soft-deadline flush is confirmed absent.  Its absence alone is
an operational durability defect rather than an invalidation of a successfully
closed batch, but production should wait for it: this implementation already
requires a versioned correctness repair, and folding in the narrow v427 repair
avoids knowingly discarding up to 15 expensive certified rises.

## Exact audited pins

The live Task472 reply is synchronized with the live three outputs; I found no
stale pin mismatch in the bytes audited here.

| object | bytes | SHA-256 |
|---|---:|---|
| `sol/luna_task_472_r07_rank99_actual_owner_v2.md` | 4470 | `3162f60b191e48a8d8b055834b37a763092c70e804f2437f018acbf258a62ec7` |
| `sol/luna_reply_472_r07_rank99_actual_owner_v2.md` | 3058 | `4cab8a454b72a2ccc00b3e615476b90a8d605ecea645a58ca60eb36c2806a744` |
| `sol/proof_r07_rank99_actual_owner_transform_v424.md` | 7009 | `f2e2103f214e6d7c15f5d1c2bc84cd100cd37a69634c381793a42a20e8bad2d9` |
| producer v2 | 64344 | `24eededdb4f8d2718c9dc33eb090b1f2c8cbf6dfdf5c40c32e140cb61eae07f9` |
| checker v2 | 47201 | `542a4d6cda7503d27e5247742cc3f44418cf3449235eb5073e61600f369d5418` |
| driver v2 | 5320 | `8f776180c0f948d8fc909c4a01c4196654970a720ecdbb8466b8c55e26dcf5e2` |

Frozen lineage also reproduced exactly:

| object | bytes | SHA-256 |
|---|---:|---|
| C99 | 173082 | `bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358` |
| rank-51 checkpoint | 10934 | `a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4` |
| Task451 producer | 13834 | `ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b` |
| Task451 recovered checker | 14442 | `1d1080cd3e130d987316feefd820215f495cd6320aa5eca764fd2f8997f0c424` |
| Task451 rank-ladder v3 | 12215 | `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37` |
| its bound rank-ladder v2 | 18191 | `cd27d69b06538e77dac1963d147f4966d8f63b9bf0d9e54860f2dae69149369b` |

Independent lightweight JSON replay confirmed both canonical inner seals,
the exact first-eight equality, batch lengths `16,16,16`, flattened 48-row
equality, ranks `51 -> 67 -> 83 -> 99`, accepted count 56, and round 12.

## Load-bearing findings

### F1 - Fatal frozen-API mismatch: neither semantic replay can start

`build_physical` takes `v3 = owner.v3` (producer line 437).  In the pinned
Task451 v3, line 13 binds `b` to the pinned rank-ladder v2.  That v2 defines

```python
def tau_free_adjoint(P):
```

at line 57.  But the producer calls
`bmod.tau_free_adjoint(P, m, args)` at lines 558 and 610, with `bmod=v3.b`.
The checker repeats the same mismatch at lines 488 and 536 as
`v3.b.tau_free_adjoint(P, m, args)`.

A bounded AST signature/call audit reproduced the arities exactly: v2 has
arity 1, v3 has the intended arity-3 wrapper, and all four replay call sites
select v2 while passing three arguments.  The resulting `TypeError` occurs on
the first correction in the exact eight-record prefix.  Thus the producer
cannot reach physical rank 51, READY, the selector, a closed appended batch,
or COMMON; the checker likewise cannot perform its advertised semantic
replay.  The producer's outer main labels this non-resource failure `UNKNOWN`,
after which the checker rejects it.  A production dispatch is therefore
guaranteed to waste construction time and fail pre-semantically.

**Smallest repair:** pass the pinned v3 wrapper into `replay_prefix` and
`replay_batch_rows` and call `v3.tau_free_adjoint(P,m,args)`.  In the checker,
change the two sites to that wrapper, or preferably use the recovered
Task451-checker-owned `I2.adjoint`/`IC.update`/`I2.pair` lineage.  Do not alter
the frozen v2 file.

### F2 - Concrete checker false acceptance: result rows are not the replayed rows

The checker loads and structurally validates the durable checkpoint at lines
636 and 361--375.  It separately makes the top-level result internally
self-consistent at lines 637--643.  The only result-to-durable equations at
lines 644--647 compare C99 identity, segments, and current profile.  They do
**not** compare `appended_batches`, `batches`, `accepted_sources`, counts,
round, or physical rank to the durable state.  Lines 683--688 then replay the
durable state, not the top-level lists.

Consequently, starting from any valid appended result, one can replace a
top-level appended row by an arbitrary dictionary, rebuild top-level
`batches` and `accepted_sources` with the same row count, retain the real
durable metadata/segments/profile, and recompute `self_digest_sha256`.
The present checker reaches PASS because it replays the untouched durable
rows.  This is precisely the commissioned "structurally sealed but
semantically altered row" mutant.  The self-test does not expose it: lines
774--787 use an unrelated four-field toy gate and never call `check`.

**Smallest repair:** before any physical construction require literal equality
between every duplicated result field and the durable state, including all
base/appended batches and records, accepted sources/count, batch count, round,
physical rank, profile, and segments.  Then replay that one bound sequence.
Add a real outer-result mutation test which keeps the durable checkpoint fixed
and must reject before the expensive replay.

### F3 - Segment seals are honest on output, but do not authenticate the current prefix and are not flat O(n)

For an honest producer, the segment input identity and READY predecessor seal
are formed in the right place (producer lines 706--723), and segment counts
sum the actual closed row counts.  The validator, however, checks an historical
input state only against `segments[:index]` and the four start counters
(producer lines 344--373; checker lines 329--358).  It never requires the
current state's appended-batch/accepted-row prefix to equal that input state's
rows.  Two different row prefixes with the same segment ledger and counts can
therefore satisfy the recorded READY seal relation.  Round accounting is also
underconstrained: validators do not tie each new batch's `round` or a segment's
round increment to its batch span.

The traversal is non-recursive because inner validation uses
`check_chain=False`, but it is quadratic, not flat.  For every segment it
hashes/reads the progressively larger historical checkpoint (twice through
`verify_identity` plus `read_*`), validates all of its accumulated batches,
constructs `segments[:index]`, and compares the growing prefix.  Summed over
`n` segments this is Theta(n^2) bytes/work and forces every historical copied
checkpoint to remain present.  The checker performs another such chain walk
for the input and again for the durable output.

**Smallest repair:** authenticate the immediate input checkpoint once, require
literal equality with the complete corresponding current prefix, and validate
the final rows/segments in one chronological pass.  Older segment identities
can be checked as sealed ledger fields or by a stored rolling prefix digest;
do not reopen and revalidate every cumulative ancestor.  Bind batch/segment
round increments in that same pass.  Add a two-segment mutant whose prior file
has different row content but identical counts, plus an instrumented linear
read-count gate.

### F4 - The v424 loop is real, but the reported bounded gates do not exercise it

Conditional on repairing F1, the live correction loop at producer lines
881--903 has the correct core v424 order: one `replay_atom`/aggregate, a
nonmutating unpacked `reduce`, dependent skip before conjugate/`seed_v12`/
exponent/receipt, then the unchanged literal/scalar gates and one `add` whose
pivot must equal `min(remainder)`.  The action path retains direct-row,
nonzero-scalar, reduce, and actual-pivot gates.  `close_batch` performs one
post-batch arithmetic update, and the generated per-invocation rise count
cannot exceed 64.  No miss is promoted to NONMEMBER.

Those positive code facts are not what the fixtures test.  The standalone
`delayed_retain` helper is called only by `fixture`; production duplicates its
logic instead of calling it.  The producer's alleged own-schema resume test
constructs an object in memory and calls the structural validator; only C99 is
passed through `load_resume`.  No symlink is created/tested.  The checker
self-test hard-codes `old_three_batch_replay=true` and
`structural_seal_semantic_row_rejected=true`; it calls neither `arithmetic`,
`replay_all`, nor `check`.  This is why both advertised fixture suites pass
while F1 and F2 remain.

**Smallest repair:** factor the actual production retained-candidate step so
the producer fixture calls that exact function, and make checker mutants enter
the real envelope/check path with bounded injected arithmetic.  Exercise an
actual own-file resume and an actual symlink escape outside the repository.

The checker does not import the new producer's resume/seal/fixture helpers,
which is good.  However `TASK451_C` is only hashed; `arithmetic()` loads the
search-side Task451 v3 and uses its `v3.b` update/pair/profile/adjoint helpers.
After F1, either narrow and document those calls as the permitted pinned
arithmetic primitives or restore the already frozen checker-owned IC/I2/IP
primitives so the claimed independent lineage is substantive.

### F5 - Atomic fallback is present, but the RSS supervisor can beat it

The checkpoint write uses temporary file, flush, `fsync`, and `os.replace`;
BOOTSTRAP precedes physical construction; READY follows full replay; and an
open batch is omitted from the reported `last_closed`.  These are genuine
improvements over Task468.

The driver nevertheless sets

```text
ulimit -v 4687500
--rss-bytes 4800000000
```

and `4687500 * 1024 = 4800000000` exactly (driver lines 60--63).  The shell
hard limit is virtual memory while the internal gate observes RSS.  Since
virtual memory is normally larger than RSS, allocation failure or the hard
limit can occur before the internal RSS threshold is observable.  `MemoryError`
is not an allowlisted resource reason, so this path yields `UNKNOWN` rather
than a typed closed fallback.  There is no serialization/close reserve.

**Smallest repair:** choose a measured internal RSS soft threshold strictly
below a separately larger hard VM supervisor, leaving reserve for update and
canonical atomic serialization.  Likewise keep a measured wall reserve, not
just nominally adjacent limits.

The remaining driver envelope is good: `PositionSublist` rejects repeated
dots, the exact `.json` one-component allowlist excludes shell metacharacters,
the producer and checker repeat canonical/symlink checks, outputs are fresh,
`set -euo pipefail` is present, there is exactly one producer and one checker,
and exact markers gate COMPLETE.  Bounded GAP loading stopped at the required
external-preamble guard.

### F6 - v427 is absent; wait for it

There is no `SOFT_FLUSH` or inner soft-deadline catch.  A boundary exception at
producer line 875 escapes directly to the outer handler at lines 932--937;
`close_batch` at line 923 is reached only by the normal loop exit.  Any already
added `rows` are therefore discarded from the artifact and the previous
closed checkpoint is returned, exactly as the Luna reply's later note admits.

V427 proves that any nonempty certified prefix of length 1--16 is a valid
batch and specifies the required search/hard/external ordering plus
close-failure rollback.  Because F1--F5 already require a successor, production
should wait and include v427 now.  This is especially warranted by the v426/
v427 timing evidence: candidate scans dominate, while the current driver also
pays a complete checker after every resource segment.  For repeated discovery,
use v426's candidate-chain policy and reserve full prefix replay for COMMON or
chosen audit intervals; this is a performance repair, not permission to weaken
the final checker.

## Bounded audit record

- Producer `--mode FIXTURE`: PASS to a temporary file outside the repository.
- Checker `--self-test` and `--pin-check`: PASS.
- Independent AST parse/signature audit: PASS and exposed F1.
- Independent canonical C99/rank-51 seal/flattening audit: PASS.
- GAP driver parse: reached `task472 external run preamble required` before any
  external action.
- No production owner run, GHA/workflow dispatch, git operation, or authority
  computation was performed.

## Re-audit gate

A smallest dispatchable successor must simultaneously provide:

1. the correct pinned v3 adjoint call in producer and checker, exercised by a
   real bounded frozen-prefix replay entry;
2. exact result-to-durable equality before replay;
3. content-binding, flat O(n) segment-prefix validation with round equations;
4. real production/checker-entry mutation fixtures, including own resume and
   symlink escape;
5. a genuine soft RSS/hard VM reserve; and
6. v427 one-row/fifteen-row flush plus forced-close-failure rollback fixtures.

Task467 PASS remains an external parent dispatch premise and is not replaced
by any result in this audit.  Even if that premise is satisfied, Task472 v2 is
not safe to dispatch.

**STOP / SAFE TO DISPATCH AS-IS: NO / WAIT FOR V427: YES**
