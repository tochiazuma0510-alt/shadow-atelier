# Sol(max) Reply 573: adversarial audit of packed GF(3) stream worker v2

Author: Sol / 2026-09-03

## 1. Scope, frozen inputs and bounded execution

The packed arithmetic kernel is recognizably the v4 kernel, and the command
line limits no longer impose Task567's 512-MiB static-input ceiling.  The
candidate is nevertheless not an exact persistent transducer.  The C service
does not install a newly accepted row into its live basis or lead map, its
offset file is malformed after two offers, and companion resume cannot use a
committed pivot.  Prefix authentication, cap handling, Linux paths, Windows
binary input, 64-bit file positions, response framing and the Python client
also have independent load-bearing failures.  The claimed resume fixture
never starts, interrupts or resumes the C service.

I audited these exact objects:

| object | bytes | SHA-256 |
|---|---:|---|
| Task572 instruction | 7,414 | `d0fa112ea40ae2195a83a739a2c06dc6067011df3ddd6b7223d91ac6345dadb0` |
| C service | 18,820 | `782f740a56027f2cf9d05456664df610164e1ea2c74c1fe77b2d8d1cd5f4fc25` |
| Python wrapper | 8,827 | `864f0105e9ce44d5ad59969f203686c7fd7daa8af2d0cefd183058377e3de551` |
| independent checker | 12,468 | `55a53e792793ca73967ac0f475409a6cb9c01b47296b07f9060919a197ccc28c` |
| Task572 reply | 4,293 | `6441ef878affe1bd26e764a4e029b5babffbf245578bd27ca48666c9e5e0a15a` |

No local compiler was found under `clang`, `clang-cl`, `gcc`, `cc`, `cl`,
`zig` or `tcc`, the standard LLVM/MSVC/MSYS2/MinGW locations, or an installed
WSL distribution.  I therefore did not invent a compiled execution or
timing.  Static defects below already prove that a real compiled resume cannot
meet the contract.

The bounded serial commands gave:

```text
python -B -m py_compile search/d972_packed_gf3_stream_worker_v2.py \
  search/check_d972_packed_gf3_stream_worker_v2.py
exit 0; wall 0.234988 s

python -B -u search/check_d972_packed_gf3_stream_worker_v2.py
exit 0; wall 0.471698 s; reported reference_seconds 0.179495
compiled_service=NOT_RUN_NO_COMPILER
```

An audit-local one-record call to the wrapper's `iter_transcript` returned

```text
NameError:name 'status' is not defined
```

Two independently rehashed semantic mutations were then passed through the
official checker's actual `validate_state`.  It accepted both:

```text
rehashed_transcript_row_id_mutation=ACCEPTED
manifest_offer_count_mutation=ACCEPTED
```

All probe files and bytecode were outside the repository.  No production
state, Task565 integration or certificate was created.

## 2. Packed algebra: local kernel PASS, live service FAIL

The local byte operations at C lines 40--45 are correct for four little-endian
base-three trits.  `axpy(a,c,b)` computes `a-c*b`; `reduce` revisits a packed
byte after eliminating its first live trit; `normalize` records leading
coefficient two and scales by two; the map is indexed by lead while the pivot
number is intended to be acceptance order.  If supplied a valid populated
basis, the ordered reduction coefficients have v452/v4's positive expression
meaning

```text
dependent: input = sum(q_i * basis_i)
accepted:  input = sum(q_i * basis_i) + scale * new_basis.
```

The v1 aliased `memcpy` is gone.  These facts do not rescue the service:

1. `basis` and `map` are populated only from a pre-existing checkpoint at C
   line 104.  After a fresh accepted offer, line 106 appends the normalized row
   and lead to disk but never assigns `basis[accepted].row`, its lead/ID, or
   `map[new_lead]`.  The counter is merely incremented.  With width four,
   offer `[1,0,0,0]` and then the identical row.  The correct second result is
   dependent with `q=[[0,1]]`; this service sees an empty map again and accepts
   a second pivot with the same lead.  It therefore fails the most basic
   dynamic accepted-response-to-later-offer contract.
2. If a reduction list is nonempty, `json_pairs` at line 86 uses
   `"[" PRIu64` rather than `"[%" PRIu64`.  It prints literal conversion
   suffixes instead of numbers, so the Python client's `json.loads` rejects
   the response.  This is reached immediately by reducing a row against a
   resumed primary pivot.
3. The response exposes the one-based committed offer count, not the opaque
   `o.id`.  Although the binary transcript contains the ID, the live response
   cannot be independently matched as required.  It also returns no dependent
   companion bytes or authenticated location, and the wrapper supplies no
   companion-handoff accessor.
4. The manifest contains `fifo_head` and `fifo_tail`, but no frame or wrapper
   API ever changes them.  They remain zero and do not checkpoint the caller's
   dynamic closure cursor.

Thus the service is not merely missing a resume optimization; it computes the
wrong row space in one uninterrupted two-offer process.

## 3. Transcript, offsets and real resume

The required offset sequence for record starts `s_i` and EOF `E` is

```text
[E]                                      for zero offers,
[s0,E]                                   for one offer,
[s0,s1,E]                                for two offers.
```

The C implementation creates an empty file at zero offers and appends both
`start` and `end` for every offer (line 106).  It consequently writes

```text
[]                                       for zero offers,
[s0,E]                                   for one offer,
[s0,s1,s1,E]                             for two offers,
```

because the first end equals the second start.  One offer works only by
accident.  `validate_transcript` consumes one offset per record and then one
EOF; at two offers it reads the duplicated `s1` as EOF and rejects it against
the real `E`.  At zero offers it cannot read the mandatory EOF at all.  Many
offers inherit the same failure.

Resume has further independent defects:

- append streams are opened with `ab+` but never positioned at end before
  `ftell`.  On a resumed update stream its read position may be zero even
  though writes are forced to EOF, so the next recorded start is not the
  committed transcript length;
- primary basis rows are loaded, but `companion.bin` is never used to rebuild
  `cbasis`.  A resumed companion offer which reduces by any old pivot reaches
  `if (!cb[piv].row) return 0` at line 88 and is reported `REJECTED`;
- `companion.bin` contains one companion per **offer**, including dependent
  offers, while a resumed companion basis needs only the accepted companions
  selected by transcript chronology.  No such selection is implemented;
- accepted transcript metadata is not cross-bound to the same pivot's
  `leads.bin` lead and opaque ID, and transcript coefficients are checked only
  by their low byte rather than as complete little-endian uint64 values; and
- manifest structural equalities such as
  `basis_len=accepted*(width/4)`, `leads_len=16*accepted`, counts within caps,
  and the companion/offset length laws are not checked.  A rehashed manifest
  with `accepted>rank_cap` makes line 104 write beyond the allocated `Basis`
  array.

There is therefore no valid compiled checkpoint after multiple offers, no
companion resume, and no evidence of byte-identical continuation without
replaying committed offers.

## 4. Prefix authentication and file/portable-C safety

All parent-identified attack surfaces are real.

### 4.1 Committed prefix versus uncommitted suffix

`check_lengths` hashes the entire current file.  If `got==want`, it compares
that digest with the manifest.  If `got>want`, however, the digest comparison
is disabled and the file is simply truncated.  A minimal attack is a
committed two-byte file with a one-byte committed prefix: change that first
byte, retain or append a second suffix byte, and resume.  `got>want` causes
the mismatched full digest to be ignored; truncation leaves the corrupted
first byte as the allegedly authenticated prefix.  Choosing a non-leading
basis coordinate lets the later row-invariant check pass.

The implementation must hash exactly the first `want` bytes and compare that
digest before truncating the suffix.  It must then durably truncate.  Hashing
the prefix plus suffix and ignoring the result authenticates neither.

Also, `load_manifest` returns the same false value for “absent” and “present
but corrupt/truncated/wrong schema”.  Main then calls `fresh_state`, which
opens the data files with `wb` and destroys the old state.  Flipping the
manifest version is thus treated as authorization to reset rather than a
fail-closed rejection.

### 4.2 Paths, positions and C11 behavior

- `path_join` inserts `\\` unless the directory already ends in `/`.  On
  Linux, a normal `/tmp/session` argument therefore produces a sibling name
  such as `/tmp/session\\basis.bin`, not a file inside the session directory.
  The wrapper uses `Path(directory)/"basis.bin"`, so the two sides do not even
  name the same object.  On Windows, stdin remains in CRT text mode; arbitrary
  packed bytes can undergo text translation or Ctrl-Z EOF handling because
  `_setmode(...,_O_BINARY)` is never called.
- `ftell` is a `long` interface and is used for transcript positions.  It is
  not a valid 64-bit Windows file-position contract.  `_ftelli64` on Windows
  and a checked 64-bit POSIX interface are required.
- `manifest_encode`/`manifest_decode` form a pointer to the scalar member
  `session` and index it as though the next fourteen struct members formed one
  uint64 array.  Those members are not an array object; this pointer arithmetic
  is not defined portable C11 serialization.  Each named field, or an actual
  array member, must be encoded explicitly.
- several write results are ignored: the status byte and padding, and a failed
  pair write only break the inner loop.  Protocol truncation/read errors can
  fall out of the service with exit status zero; close ignores checkpoint
  failure.  `strtoull` conversion tails are not rejected.  These paths do not
  propagate a typed, durable failure.
- the temp manifest is flushed and fsynced before rename, which is the right
  core order, but POSIX publication does not fsync the containing directory.
  More importantly, the wrong path join and corrupt-manifest reset prevent the
  existing routine from serving as a fail-closed atomic state boundary.

## 5. Caps, memory and production-time feasibility

The argument limits do admit the requested numeric shapes: widths 36,288,
48,384 and 32,260 are below `MAX_WIDTH`, ranks 36,288 and 48,384 are below the
hard 50,000 limit, and there is no v1-style static input matrix.  The intended
C memory inventory is also basically appropriate: accepted primary and
accepted companion bases, the lead map, one offered pair and the current
reduction list.  No historical reduction list is retained in C memory.

The cap semantics are nevertheless wrong:

- line 105 rejects every offer whenever `accepted>=rank_cap`, before reduction.
  At full rank, a zero row or an existing basis row must still be accepted as
  a dependent offer.  Width four, rank cap one, one accepted row followed by a
  zero row is the minimal counterexample: the service returns
  `UNKNOWN_RESOURCE` instead of `DEPENDENT`;
- transcript and offset caps are tested against the old manifest lengths only
  after the new bytes and counts have been appended.  A one-byte cap therefore
  permits the first record and checkpoint to exceed the cap.  A later failure
  advances in-memory counts and leaves an uncommitted suffix before returning
  `UNKNOWN_RESOURCE`;
- current-reduction allocation exhaustion becomes `REJECTED`, not typed
  `UNKNOWN_RESOURCE`; malformed packed input is conversely mislabeled as a
  resource result; and
- no predicted record-size check prevents writing past `byte_cap` before
  committing.

Runtime is a separate decisive failure.  Every accepted or dependent offer
fsyncs all open files and `checkpoint` reopens and SHA-256 hashes every complete
file from byte zero.  This is quadratic I/O.  Even keeping the accepted rank
one below its cap so that the present precheck continues to admit dependent
offers, reaching rank 36,287 early makes basis hashing alone read

\[
 9072\left(\frac{36287\cdot36288}{2}
       +(177432-36287)36287\right)
 =52{,}437{,}248{,}122{,}896\ \text{bytes},
\]

or 52.44 decimal TB.  In physical companion mode the current design appends a
12,096-byte companion for every one of 153,211 offers; repeatedly hashing just
that file reads

\[
 12096\frac{153211\cdot153212}{2}
 =141{,}969{,}323{,}051{,}136\ \text{bytes},
\]

or 141.97 decimal TB, before basis, transcript and offset scans.  It also
issues hundreds of thousands of fsyncs.  This cannot be treated as an optional
micro-optimization under the six-hour envelope.

`reduce` additionally calls `invariant` on the entire prefix before the lead
for every coefficient use.  Normalized pivot invariants should be checked once
when a row is accepted or loaded; repeating that scalar scan for every edge is
unnecessary potentially quadratic work.  Companion acceptance also scans the
whole lead map to rediscover the next pivot instead of using the accepted
counter.

Incremental hashing between explicit checkpoint boundaries, a bounded
checkpoint cadence, and one-time pivot validation are mandatory.  Compression,
SIMD and alternate batching remain optional only after those repairs.

## 6. Wrapper and independent-checker audit

### 6.1 Wrapper

The wrapper has two positive properties: it accepts byte-oriented views and
imposes no production timeout or silent Python fallback.  It is not a viable
production client:

1. `StreamService` launches the service with `stderr=PIPE` but never drains
   that pipe.  C writes and flushes one progress line per offer.  Once the pipe
   fills, C blocks after a stdout response; a later caller write/read then
   deadlocks.  stderr must be inherited, redirected to a drained file, or
   consumed concurrently.
2. `iter_transcript` refers to an undefined variable `status` at lines 76 and
   81.  The audit-local one-record probe reached the `NameError` above.  It
   also reads the entire transcript with `read_bytes`, as do state
   authentication and the checker, contradicting the advertised streamed,
   one-record and bounded-memory interface.
3. It neither validates the returned opaque ID nor exposes the dependent
   companion.  `close` can wait indefinitely, does not validate the close
   response or exit status, and cannot recover from the unread-stderr block.
4. The test-only `reference_reduce` stores companions by offer position but
   indexes them later by accepted-pivot number.  Once a dependent offer occurs
   before a later accepted pivot, subsequent companion reductions use the
   wrong row.  The returned object omits companion rows entirely, so even the
   reference API cannot expose the required dependent handoff.

### 6.2 Checker and fixture truthfulness

The dense `reference` routine itself is genuinely dense GF(3) and imports
neither wrapper nor C; that narrow independence property passes.  Its fixture
does not test the candidate it reports about:

- even when `cc`, `gcc` or `clang` is found, lines 177--178 merely print
  `AVAILABLE_FOR_AUDIT`; there is no compile or service invocation anywhere.
  Windows compilers are not searched.  `subprocess` is unused;
- “dynamic closure” runs a one-row dense reference, then starts a second dense
  reference from scratch with two rows.  It does not use a service response to
  generate an offer;
- no code interrupts or resumes any process, injects an uncommitted suffix, or
  checks byte-identical resumed output.  `checkpoint_resume="PASS"` is a
  constant in the final JSON;
- the only offset state has 40 offers.  The required zero-, one-, two- and
  many-offer boundaries are not exercised against C;
- companion testing calls only the dense reference.  The emulated companion
  layout interleaves primary and accepted companion rows inside `basis.bin`,
  whereas C writes only primary rows there and puts one companion per offer in
  `companion.bin`.  `validate_state` would reject a real C companion basis by
  its own length formula, and main never applies it to a companion state;
- the 13 file mutations are written without recomputing the manifest hashes,
  so they test almost entirely the outer digest gate.  They do not establish
  semantic reconstruction.  After correctly updating the transcript digest,
  I changed the first transcript opaque ID while leaving the accepted ID in
  `leads.bin`; `validate_state` accepted it.  It likewise accepted a manifest
  offer count changed from one to 999;
- accepted transcript leads are checked only for membership in the set of
  basis leads, not against the row at that pivot, and transcript IDs are not
  cross-bound to accepted IDs.  The checker does not compare `len(records)`
  with the manifest offer count, replay each expression against supplied
  offered rows, enforce the byte cap, or validate companion contents; and
- no compiled RSS, file-size, progress, restart or speed measurement exists.

The checker correctly labels the unavailable compiler, but the other PASS
fields and Task572's claimed fixture coverage are not supported even as a
complete protocol-emulator test.

## 7. Disposition of the specified attack surfaces

| surface | finding |
|---|---|
| `path_join` separator | CONFIRMED: ordinary Linux paths escape the intended directory |
| two offsets per offer | CONFIRMED: zero and two-or-more offer checkpoints fail structure |
| whole-file checkpoint per offer | CONFIRMED: quadratic hashing plus per-offer fsync is production-blocking |
| authentication when `got>want` | CONFIRMED: corrupted committed prefix is accepted and retained |
| companion reconstruction on resume | CONFIRMED absent; first old-pivot use is rejected |
| stale byte-cap lengths | CONFIRMED: current offer is committed over cap |
| rank-cap handling | CONFIRMED: valid dependent offers are blocked at full rank |
| piped unread stderr | CONFIRMED deterministic finite-buffer deadlock risk |
| live accepted-row installation | ADDITIONAL CRITICAL FAILURE: absent |
| response JSON with reductions | ADDITIONAL CRITICAL FAILURE: missing `%` format markers |
| corrupt manifest handling | ADDITIONAL CRITICAL FAILURE: silently resets/truncates state |
| wrapper transcript iterator | ADDITIONAL CRITICAL FAILURE: one-record `NameError` |

## 8. Minimal repair list and claim boundary

A finite v3 repair can retain the same mathematics and files, but it must at
least:

1. install every accepted primary row, lead, opaque ID and map entry in memory
   before acknowledging it; maintain a separate accepted companion basis,
   rebuild it from committed offer statuses on resume, and expose the exact
   dependent companion and input opaque ID;
2. initialize offsets with zero and append exactly one new EOF per committed
   record, seek append readers to the committed end, and validate all count,
   length, pivot/lead/ID/scale and companion cross-bindings;
3. distinguish absent from invalid manifest, hash and compare exactly each
   committed prefix before truncating a suffix, then durably truncate it;
4. predict cap consumption before writes, allow dependent reductions at full
   rank, roll back every uncommitted mutation, and use typed resource versus
   malformed/protocol failures;
5. replace whole-file per-offer hashing/fsync by incremental digests and
   explicit bounded checkpoints; validate each pivot invariant once;
6. fix POSIX/Windows joining, Windows binary stdin, checked 64-bit file
   positions, explicit manifest serialization, all write/error paths and
   durable atomic publication;
7. drain progress output, make authentication/transcript parsing streaming,
   fix the wrapper iterator and companion API, and preserve the no-timeout,
   no-fallback policy; and
8. make the independent checker compile and run the actual service, kill it
   after several committed and uncommitted offers, resume primary and
   companion modes without replay, cover zero/one/two/many offsets, and apply
   rehashed semantic mutations while replaying every supplied offer densely.

These are primitive/protocol repairs, not a change to v452, v4, the Task565
closure universe or the mathematics.

```text
TASK565 INTEGRATION: not performed
CURRENT GRADE-ONE RUNS: unchanged
GRADE-TWO PRODUCTION: not launched
GRADE MEMBERSHIP / A0 / COMMON / COFINAL LIFT / FAKE / IHARA: not declared
MATHEMATICAL TERMINAL: none
verified=false
```

PACKED_GF3_STREAM_WORKER_V2_AUDIT_FAIL
