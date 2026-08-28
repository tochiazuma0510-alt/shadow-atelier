# Sol reply 347 - task342 A0/v7 code, soundness, and performance audit

## Decision

**REJECT / UNEXECUTED.**  I ran no Python, Node, GAP, GHA/workflow, git, or
network operation.  The candidate was inspected statically; bytes and SHA-256
were recomputed read-only, including a streaming read of the sole ZIP member.
No SELFTEST or PRODUCTION run is authorized.

There is an important first-stop distinction.

- **Frozen-input forced exception before search: none found.**  The current
  candidate, all literal transitive pins, ZIP member, old schema/digests, and
  fresh owned-path preconditions agree.  Static inspection therefore does not
  justify inventing a pin, schema, or runtime exception.
- **First authorization/contract stop:** producer line 2303 unconditionally
  calls `run_real_owner_selftest` on every `PRODUCTION` path, before constructing
  the production `Search` and before its first real boundary pair.  This is not
  a runtime exception.  It is the earliest mandatory production owner which
  violates the commissioned performance and physical-mutation contract.
- On the advertised **resume** route the earlier structural stop is the driver
  itself: lines 122--125 have no `--resume` argument or resume-path branch at
  all.  A v7 checkpoint is consequently not consumable by the commissioned
  driver.

The candidate was reported durably committed and pushed unchanged as
`2c58e837` on `origin/sol/r07-explicit-lift-20260825`.  No workflow or run was
dispatched.

## 1. Frozen identities and input provenance

All five commissioned identities are exact:

| object | bytes | read-only SHA-256 |
|---|---:|---|
| `search/d972_r07_history_free_positive_fast_resume_v7.py` | 122,132 | `cddef2abe41aaad9b2c0dd81d6fcc67b603bbf70359888fdfd34bf1d9f069ef9` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v7.py` | 96,334 | `8afcf5653eefedfb1639ea9a0d30e6d7ba5fc3f337406295b4522c31ae61423c` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v7.g` | 10,156 | `232f67106d5d21c87e01b5889112c48c687186ddd6b3539f0664973b50e4d558` |
| v7 fixture | 2,783 | `5f6628d8413ebcc78a87196fa999b4f73122d4bca2c22efc0a9f637e59f483c6` |
| Luna reply 342 | 16,542 | `6403d8c1d182ddb476ef0f16dbd891d4d1935b392aeb7ea38c356729e5464249` |

The producer's 21 source pins, the checker's same 21 pins plus its producer
pin, and the driver's 24-pin roster have zero current byte/digest mismatches.
This includes task175/task176, q3, the joint receipt, old arithmetic, joint,
v172, g760, PB4, all prerequisite papers, manifest, and fixture.  The q3 input
has 27 correction-fibre records, 26 nonempty words, and the two marked Q0
permutations.  The joint receipt has terminal
`B345_JOINT_KERNEL_QSTAR_CLOSED`, Gamma order 243, and the pinned complete-Q0
presentation ledger.

The staged manifest and member also agree exactly:

```text
source run / head       33149728601 / 7dd85c94c01e35e090917f9d11f9a7252a260523
artifact id / digest    9681838782 / sha256:66ed561b0c19c22dd56ce6aaa1626159d8267788fa282d3f2cb72f33c36e6917
ZIP bytes / SHA-256     5,001,811 / f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566
sole member             d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json
raw bytes / SHA-256     86,368,039 / c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab
old schema              d972-r07-normalized-exact-cached-colgen/v3
old self digest         29bb74f3bd8048913a0365bc4c599f3731d32ba56967f3a238c7468b7fcfd123
rank / columns          2,896 / 2,896
phase / pairs           positive_boundary_correlation / 3,145,088
manifest counter        3,145,728 (the documented 640 frame/counter difference)
candidate words         0
all mathematical claims false
```

Thus identity is not the rejection reason.  These are authenticated candidate
bytes, not an execution, independent cross-check, or Lean verification.

## 2. Literal route and hypothetical continuation

The fresh driver route is coherent through its initial prefix: it pins its
inputs, stale-rejects its own v7 paths, extracts and hashes the unique raw
member, invokes the producer with `--seconds 10800` and W=2 or W=4, then would
invoke one checker, compare one exact terminal from each, apply the
terminal-specific sidecar rule, and make `printf` the last successful shell
operation.  The old v6 final-sentinel defect is repaired.

The producer then authenticates its registry, opens the raw source with
no-follow/link-count/fd-identity checks, reads/hashes/parses it once, builds the
light owner without Q0, checks the old envelope, constructs all P rows, and
derives the fresh target and dual.  No frozen-input exception is forced in
this prefix.  The first contract stop is the unconditional production
selftest at line 2303.  Under the hypothetical repair “remove that call from
PRODUCTION and accept a separate SELFTEST artifact,” the real persistent
owner is reached and its mathematical control flow is:

```text
nonzero remainder -> fresh exact dual -> complete boundary epoch
  ACTIVE -> direct translated row -> rank insertion -> repeat
  zero   -> Q0-LATE build -> correction oracle
             ACTIVE -> direct correction row -> rank insertion -> repeat
             complete no-ACTIVE -> typed resource stop, never NONMEMBER
zero target remainder -> finite COMMON candidate -> independent checker
```

The boundary zero branch is only a transition.  No line promotes it to a
separator, exhaustion theorem, or negative claim.  Hard `ProtocolStop` and
unexpected exceptions produce no acceptable terminal; typed input/resource
paths keep all forbidden claims false.

Independent route failures remain after removing line 2303:

1. producer and checker final JSON owners use direct `path.open("xb")`, write,
   flush, and fsync (producer 2146--2154; checker 1426--1434), not a same-directory
   temporary plus atomic replace.  Cancellation can leave a partial, stale,
   owned receipt/verdict.  The ZIP extractor has the analogous kill window;
2. the producer has no wall/RSS gate during registry authentication, the
   86 MB read/decode/parse, `build_light`, or the complete 2,896-row P build.
   Its first such gate is line 2302;
3. a `ResourceStop` before `build_triangular` returns enters lines 2315--2320,
   whose recovery itself requires non-null reducer, P rows, and triangular
   certificate.  The `formal_entries` cap can take precisely this hard route;
   OOM, cancellation, and raw-read errors likewise have no safe checkpoint;
4. the driver has no resume command.  Even manual `--resume` reconstructs the
   entire registry/raw/light/P/selftest prefix before restore;
5. the COMMON checker does not independently reconstruct the selected
   Q0/Gamma fibre/schedule owner, and the nonpositive checker is not cheap;
6. no hard checker budget or upload reserve exists.  Producer-near-three-hours
   plus checker-near-three-hours consumes the entire six-hour job before an
   artifact upload can be guaranteed.

There is also a terminal-grammar defect on hypothetical pin drift:
`InputStop("pin:" + relative_path)` contains `/`, while both checker
`safe_terminal` and the driver UNKNOWN_INPUT regex forbid `/`.  The frozen
pins match, so this is not the first current-input stop, but it breaks the
advertised typed-input route.

## 3. Mathematical positive path

### Sound pieces

The v276 triangular core is substantially correct.  It checks the old seal,
fixed schema/digests, exact column and pivot inventories, exact record keys,
typed boundary provenance, canonical sparse rows, increasing ancestry indices,
nonzero diagonal, registered pivot, coefficient one, least live key, and the
independent equations

```text
P_j = sum_i a_ji C_i.
```

The frozen arithmetic is:

| quantity | exact value |
|---|---:|
| raw support total / maximum | 20,354 / 12 |
| ancestry entries total / maximum | 137,926 / 258 |
| A*C weighted contributions | 1,011,460 |
| P support total / maximum | 289,774 / 522 |
| first fresh dual support | 1,188 |

Each P is injected directly; historical `Echelon.add(C_j)` is not called.
The target is rebuilt from the pinned light mathematical owners and compared
with the old target bytes.  The first dual is freshly derived and only then
compared with the pinned digest.  Initial old ancestry, new ACTIVE expressions,
correction expressions, zero reduction, and the selected formal support are
carried algebraically.

The process correlation also has the right positive mathematics: all 104
typed descriptors are built, support is type-filtered, the workers compute
`t=g*h^-1`, check `t*h=g`, accumulate in F3, cover disjoint complete intervals,
and commit only after all worker frames pass.  The parent selects the
lexicographically least nonzero accumulator, independently reconstructs the
translated boundary row, scalar, and full contributor list.  Failed epochs
are discarded.

Finally, both producer and checker reconstruct each *selected* boundary or
correction row, use coefficient two as an inverse word, check the selected
joint-kernel factors and exponent pair, recompute the eleven-occurrence/direct
H1/H2/P equality, rebuild the complete sparse sum, and require zero final
residual.  Therefore a false or unreplayed **unselected** old row can change
discovery, timing, or which proposal is found, but cannot by itself make an
invalid selected equality pass.  The set iterated in the final equality is
forced to be exactly the formal-solution support.

### Failed premises

The full commissioned mathematical route nevertheless fails.  For a selected
correction, checker lines 818--890 independently recompute the literal word,
joint-kernel/direct row, formula, coordinates, and scalar, but they do not
construct Q0, Gamma, a fibre, a kernel state, or the claimed section word from
the claimed IDs.  The K=0 branch merely checks target equality and integer
ranges; the K!=0 branch merely checks `qid=cursor//243+1` and
`gid=cursor%243+1`.  `heavy_input_sha256` is accepted as a 64-character shape
at lines 1150--1158.  Hence fabricated fibre IDs, kernel cursor, global
schedule provenance, or heavy digest can be resealed around an otherwise
valid direct row and be accepted.  This violates the explicit
schedule/fibre/Q0 and frozen-side-gate requirement even though the final
finite linear identity itself is a useful sound sub-result.

The checker also does not bind an `o:NNNN` selected record to the corresponding
record bytes in the authenticated raw checkpoint: it hashes the raw object but
does not parse that selected source record.  It derives a valid boundary row
from the receipt provenance, which is sufficient for the explicit positive
identity, but not for the claimed selected-checkpoint-support provenance.

Accordingly the narrow v278 identity argument is preserved, but the literal
commissioned mathematical positive path is **REJECT**, not a finite A0
acceptance route.

## 4. Checker independence and physical transport

The import graph has a good narrow separation:

```text
producer compiles: live, task176, old, joint, v172, g760, PB4
checker compiles:          task176, old, joint, v172, g760, PB4
checker authenticates producer bytes but never compiles/imports them
```

The six shared modules are immutable public group/arithmetic/codec owners.
The checker has its own sparse codec, target constructor, boundary descriptor
and accumulator implementation, all-seven model, and final residual logic; it
does not import the producer, live-v1 helper, or an old full checker.  This
preserves helper non-sharing for the explicit selected equality.

Overall checker independence/transport is still REJECT because the Q0/heavy
provenance above is shape-only and UNKNOWN is far beyond a cheap envelope
check.  On every UNKNOWN the checker authenticates all 22 pinned byte objects,
rehashes the 86,368,039-byte raw source, and may parse a checkpoint of up to
4,000,000,000 bytes.  A resource mutation run opens/parses that checkpoint a
second time and serializes a full temporary copy.  This invokes no positive
mathematics or Q0, but “bounded by 4 GB” is not the required bounded cheap
transport.

The no-follow, regular-file, link-count-one, fd-before/after, and pathname
recheck logic is otherwise sound on Linux.  Device/inode are used only as a
same-job physical-object canary alongside bytes/SHA, not as the sole portable
artifact identity.  Checkpoint sibling naming and COMMON/no-sidecar rules are
exact.  Atomic final output and cheap nonpositive transport are the failed
physical pieces.

## 5. Checkpoint and resume truth

Checkpoint serialization is atomic at the pathname level, but the resume ABI
does not meet its claims.

- `actual_rank_increase`, `last_safe_light_before_heavy`, and
  `correction_row_complete` checkpoints are written while the persistent owner
  is live, so their recorded cleanup has `complete=false` and live PIDs.
  Restore lines 1805--1814 require completed cleanup and no live PID.  Those
  advertised interruption checkpoints are therefore unrestorable.
- A caught terminal resource stop aborts the owner and overwrites a clean
  `phase=resource_stop` checkpoint.  That is the only generally restorable
  form, and the driver still provides no route to it.
- Restore correctly rebuilds P and pivot order, directly replays all new rows,
  and checks the resulting remainder/formal solution.  It does **not** compare
  the stored `current_dual` with a freshly derived dual or bind
  `correction_progress.dual_sha256` and every cursor to that next state.
- No Q0 states, stores, membership bitsets, A tables, fibre indices, or Gamma
  owner are serialized.  Even a checkpoint marked `heavy_complete=true`
  restores into a `Search` whose `heavy_built` remains false; the next zero
  epoch rebuilds all heavy data and merely compares the new digest.  This is
  correct recomputation, not accelerated heavy resume.
- Every resume first rereads/parses the 86 MB source and rebuilds light, all P,
  the target/dual, and the production selftest.  It rejects the very serial
  history the checkpoint was supposed to avoid.
- The 4 GB cap is checked only *after* the whole checkpoint is canonicalized,
  written, fsynced, and replaced.  If oversized serialization raises
  `ResourceStop`, the resource handler attempts another checkpoint write and
  can raise the same exception from inside the handler, leaving no final
  terminal.

Caps during authentication/raw parse/light/P have no periodic gate and no
phase-complete resumable state.  Caps during child startup/IPC can cleanly
abort and write a terminal checkpoint.  Caps during partial heavy build drop
the partial heavy owner and later recompute it.  Caps during correction can
record cursors, but the cursor/dual binding is insufficient and the heavy
prefix is missing.  Thus checkpoint/resume is **REJECT**.

## 6. Process and physical-mutation audit

The production fork owner is a genuine Linux `fork`/AF_UNIX owner, persistent
across epochs.  Its channels are nonblocking and length-framed with absolute
deadlines; startup, timeout, child death, partial frame, terminate/join/kill,
process close, and survivor checks are real in the W=2/W=4 process selftest.
This process core is worth preserving.

The mutation claim as a whole is not physical:

- the eight triangular cases write a real temporary file before the actual
  six-row subset validator, but they mutate only a six-column sample, not the
  complete production P owner;
- timeout/death/partial and blocked send use real child processes, but the
  `f3_cancellation` case never requires the advertised zero/cancellation
  result;
- producer `phase_gate_selftest` clones a small shaped dictionary and compares
  it with copied expected fields.  `light_resource_checkpoint` and
  `heavy_transition` are ledger rows with no injected owner;
- producer boundary/positive/physical lists are only
  `*_committed_to_checker` names;
- checker boundary mutations alter a synthetic JSON owner map.  In particular
  blocked/dead/partial/survivor are booleans, not process owners;
- checker positive cases clone and reseal the already assembled receipt.
  Some reach real mathematical reconstruction, but others are copied booleans
  or post-hoc document tests.  Symlink, hard-link, TOCTOU, and stale-output
  cases are genuine filesystem mutations.

Resealing these shaped frames does not convert them into upstream physical
fault injection.  The baseline COMMON mutation route is also data-dependent
and may never exist.  Therefore PHYSICAL MUTATIONS is **REJECT**.

## 7. Mandatory unnecessary-work audit

### Input and module work

On a fresh run the 86,368,039-byte source is traversed three times: ZIP
decompression/write/hash, producer read/hash, and checker read/hash.  It is
JSON-decoded/parsed once by the producer.  The producer read first retains all
chunks and then `b"".join`s them, so about two raw-byte copies coexist; decode
and JSON parsing add a full text copy and object graph.  A resume repeats this
entire prefix.  UNKNOWN mutations can cause an additional full raw hash.

The driver hashes 24 pinned files, the producer retains byte snapshots of 21,
and the checker rereads 22.  Producer module compilation is seven modules;
COMMON checker compilation is six.  Registry caching prevents repeated
compilation inside one process, and heavy `load("joint")` is a cache hit.  The
UNKNOWN branch still reads every mathematical source although it compiles
none.

### P, target, and dual

The useful A*C work is exactly 1,011,460 sparse contributions.  It is followed
by avoidable quadratic scans:

```text
pivot in pivots                         4,191,960 prior-byte comparisons
explicit earlier-pivot zero gate        4,191,960 dictionary probes
FormalReducer.inject earlier gate       4,191,960 dictionary probes
explicit pivots[:ordinal-1] slices       4,191,960 copied list references
```

Thus the code does scan every earlier pivot for every P twice, contrary to the
commission, and also performs a linear duplicate search.  A pivot set plus a
scan of the computed P support (289,774 entries total), followed by one trusted
direct insertion, removes all three quadratic owners.

Before the first real boundary pair, the same target/dual is derived in
`build_triangular`, again in `run_real_owner_selftest`, and again in
`Search.run`; `Search.run` also performs a separate reduction immediately
before its `exact_dual`.  These are four 2,896-pivot target sweeps and three
dual builds.  Each dual build traverses 286,878 nonpivot P entries in reverse
and then checks a 1,188-entry functional against all 2,896 rows, i.e.
3,440,448 dictionary probes.  The three redundant annihilator checks alone
therefore make 10,321,344 probes before the first production pair.

### Boundary owner and unconditional selftest

The first real dual has 1,188 `(block,component)=(1,1)` entries and four
matching descriptors, hence exactly 4,752 pairs.  Its support-list JSON alone
is 108,109 bytes per worker (1,188 canonical 90-byte entries plus separators),
before a small frame envelope.  W=4 therefore sends four copies, over 432 kB
of support payload, and each child decodes/unpacks all 1,188 entries although
it computes only its interval.  The combined accumulator has at most 4,752
keys.  On ACTIVE, the parent makes a second complete 4,752-pair translation
pass to materialize contributors.  The real roster is persistent, so there is
no per-epoch pool construction and no per-pair hash; those are good properties.

`run_real_owner_selftest` does not belong on every PRODUCTION.  Before the
first real pair it creates eight process rosters (normal plus three faults at
each of W=2/W=4), 24 roster children, and one blocked-send child: **25 forked
children**.  Its full and scaled-full epochs perform exactly
`2 * 4,752 * 2 = 19,008` full pair products, apart from probes and fault work.
It also busy-waits in timeout/blocked-send children.  The COMMON checker then
serially recomputes this selftest, including another 19,008 full pair products.
This belongs in one separately accepted SELFTEST artifact, not production or
every COMMON check.

The checker boundary mutation suite constructs a 4,752-pair baseline, reruns
it for baseline validation, and reruns the full epoch for six document
mutations (missing/overlapping interval, accumulator, winner, scalar, epoch):
at least **38,016** pair evaluations, plus the malformed-support attempt.

### Q0, ancestry, and document copying

Q0 is correctly delayed until the first complete zero boundary epoch.  Once
triggered, however, it eagerly builds all 1,469,664 states, a 52,907,904-byte
raw Q0 permutation roster, ten coordinate stores totalling 1,425,574,080 raw
bytes, eleven membership bitsets totalling 2,020,788 bytes, and large Python
lists/dictionaries.  Membership alone performs 16,166,304 family probes.  It
then builds and retains all ten coarse indices, scanning 14,696,640
state-coordinate rows and retaining up to that many state-id references,
before the correction formula identifies which coordinates are needed.  The
indices should be lazy per actually queried coordinate and checkpointed or
discarded honestly.

Formal ancestry is not a DAG: every reduction merges flat symbol dictionaries
and `inject` copies the whole result.  It can grow quadratically until the
2,000,000-entry cap.  Every checkpoint flattens/publicizes all P rows and old
ancestry again.  `seal` canonicalizes the whole checkpoint, `atomic_json`
canonicalizes it again, and the size gate occurs after writing.  The final
receipt is also canonicalized for its seal and again for output.

COMMON is validated once, then whole-document cloned/resealed for mutations.
At least `copied_sparse_equality_boolean` and `changed_boundary_preimage`
repeat the complete selected positive replay, so the selected mathematics can
run three full times including baseline.  `open_physical` additionally holds
a bytearray, an immutable bytes copy, decoded text, and the parsed object.  A
receipt has no producer-side byte cap (the checker later caps it at
536,870,912); a checkpoint may reach 4,000,000,000 bytes before rejection.
Those live-copy patterns are not compatible with the 5.7 GB RSS promise.

### Six-hour boundary

There is no measured-runtime claim here.  The current allocation can spend
three hours in the producer and nearly three more in an uncapped COMMON
checker/mutation suite, leaving zero guaranteed upload time.  A conservative
hard decomposition is:

```text
producer, including serialization       10,800 s
checker, including final verdict          7,200 s
upload/finalization reserve               3,600 s
total                                    21,600 s
```

The producer's internal mathematical deadline must be earlier than its outer
10,800-second slot so terminal/checkpoint serialization fits inside it.  The
checker needs an enforced outer deadline and must not run the mutation suite
in production.  Upload needs the explicit final hour; two independent
three-hour allowances are unsound.

## 8. Bounded v8 successor and v220 mapping

One bounded v8 should preserve the authenticated light owner, independent
A*C equations, direct reducer injection, persistent boundary roster, Q0-LATE
transition, selected-support direct equality, and false forbidden claims.  It
must make these minimal changes:

1. move all process/mutation work to a separately accepted SELFTEST artifact;
   delete `run_real_owner_selftest` and mutation replay from PRODUCTION/COMMON;
2. replace whole-file registry/raw reads with metered streaming where possible,
   add early and periodic wall/RSS gates through authentication, parse,
   light-roster work, and P construction, and give every phase a typed safe
   state rather than requiring a completed reducer after an early cap;
3. replace the three O(P^2) pivot owners with a pivot set and product-support
   intersection, and use one prevalidated injection; represent formal ancestry
   as structural DAG nodes and expand only final selected support;
4. retain one production persistent fork roster, but send each worker only its
   support/descriptor slice and remove the unconditional duplicate dual builds;
5. keep Q0 late, build coarse indices only on demand, and define a real
   versioned checkpoint ABI containing or losslessly reconstructing P/new DAG,
   exact next dual, clean owner state, heavy objects/digest, and bound
   correction cursors.  The driver must accept an authenticated `--resume`
   sidecar with fresh output paths;
6. make the COMMON checker reconstruct the selected Q0/Gamma/fibre/schedule
   proof and selected raw source record, rather than accepting IDs/digests by
   shape.  Make UNKNOWN a fixed-size false-claim/envelope check plus one
   streaming sidecar digest, with no raw-source rehash, module compilation,
   checkpoint DOM, or mutation suite;
7. write raw, receipt, verdict, and checkpoint through same-directory exclusive
   temporary files, flush/fsync, atomic replace, and directory fsync; clean
   failed temporaries and retain stale-destination rejection; and
8. enforce the 10,800/7,200/3,600-second producer/checker/upload decomposition
   with outer process deadlines and a serialization reserve.

Static audit cannot change v220.  There is no actual producer COMMON plus
independent checker acceptance, so A0 remains `0/1`.  No separator,
nonmembership, lift, fake, cofinal, or Ihara statement is obtained.

AUDIT VERDICT:                         REJECT / UNEXECUTED
FIRST LITERAL STOP:                    producer line 2303 run_real_owner_selftest on PRODUCTION (authorization/contract stop; no earlier frozen-input forced exception found)
MATHEMATICAL POSITIVE PATH:            REJECT
CHECKER INDEPENDENCE:                  REJECT
CHECKPOINT / RESUME:                   REJECT
PHYSICAL MUTATIONS:                    REJECT
UNNECESSARY SLOW WORK:                 production selftest; O(P^2) pivot scans; repeated duals; eager ten-index Q0; flat ancestry/checkpoint clones; repeated COMMON/UNKNOWN checker work
SELFTEST / PRODUCTION AUTHORIZATION:   NO
ACTUAL A0 COMMON + CHECKER:            0/1
SEPARATOR / NEGATIVE CLAIM:            FORBIDDEN
LIFT / FAKE / IHARA:                   NONE

TASK347_R07_TASK342_A0_V7_CODE_PERFORMANCE_AUDIT
