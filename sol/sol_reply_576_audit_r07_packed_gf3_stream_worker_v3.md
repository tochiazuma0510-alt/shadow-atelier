# Task 576 — Sol(max) adversarial audit of packed GF(3) stream worker v3

## 0. Release verdict

`PACKED_GF3_STREAM_WORKER_V3_AUDIT_FAIL`

This exact implementation is not safe for the real grade-two bounded envelope.
The live C service has no resumable authenticated state or durable checkpoint,
its physical companion/offset layout is wrong, and its configured offer/byte
caps are not enforced.  The checker does not exercise those paths and reports
synthetic PASS telemetry.  No candidate result may be promoted.

## 1. Frozen scope and bounded receipt

I read the four frozen candidate inputs, the complete Task 574 requirements,
and the complete Task 573 v2 failure contract.  Exact candidate receipts are:

| frozen input | bytes | SHA-256 |
|---|---:|---|
| `search/d972_packed_gf3_stream_worker_v3.c` | 7,208 | `a19f0dccb44985403716f3446e795e5d901adc52c91e3acafc8035db7d6ed892` |
| `search/d972_packed_gf3_stream_worker_v3.py` | 6,934 | `bb449830d1d4b919592144484a7b69859d9a57e7bd722a8639e6c1f09ec97b09` |
| `search/check_d972_packed_gf3_stream_worker_v3.py` | 5,857 | `e4aa7dbf90b1d5421f39b664a0b5f7c773bdd3b727e275bef8ced24a349f1185` |
| `sol/luna_reply_574_r07_packed_gf3_stream_worker_v3.md` | 2,972 | `a847bb3f9684f1fb774c82581b0ad1b7c46d6dbf431582b809c3ddcfa6bef8ad` |

For reference, the requirements file is 10,340 bytes with SHA-256
`56e7be1728f3414b09dd86b3aca1e9db5da4d35899281bc86b93dea057e0c2e4`,
and the prior audit is 20,499 bytes with SHA-256
`6ab3c30d40f11ebdf7c9fe5ad88f49ff40fe43f9ee72cc115b2649fc177f4401`.

The only executions were seconds-scale local checks:

```powershell
$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'task576-pycache'
python -B -m py_compile search/d972_packed_gf3_stream_worker_v3.py search/check_d972_packed_gf3_stream_worker_v3.py
# exit 0; wall 0.2067969 s

python -B -u search/check_d972_packed_gf3_stream_worker_v3.py
# exit 0; wall 0.2720132 s
```

The checker printed `compiled_service = "NOT_RUN_NO_COMPILER"`, six frozen
cases, 40 purported random rows, and 13 purported rejected mutations.  No C
compiler was found among `clang`, `clang-cl`, `gcc`, `cc`, `cl`, `zig`, and
`tcc`; consequently no compiled-service or RSS claim was measured.  The
static failures below are direct and decisive without compiled execution.
No GHA, workflow, production, Task 565 integration, or candidate repair was
performed.

The exact physical byte count and SHA-256 of this reply can only be measured
after its final byte is written.  I report that immutable receipt in the
parent handoff rather than inserting a self-changing digest here.

## 2. Minimum release blockers

### F1. There is no resume or durable/authenticated checkpoint

This alone is release-blocking.

- C lines 28–31 allocate an empty basis/map, initialize every map entry to
  `-1`, and open data files with `"ab+"`.  There is no read of a manifest,
  basis, leads, transcript, offsets, or companion state anywhere.  Lines
  32–35 expressly say that the C candidate requires a fresh directory; a
  Python emulation cannot supply persistence to the production C process.
- The `CHECKPOINT` branch at C line 36 merely emits
  `response(5,0,count,0,0,0,...)`.  It does not flush or fsync data, maintain
  or finalize hashes, atomically publish a manifest, fsync the directory, or
  return a real generation/committed-count/manifest-digest tuple.
- Wrapper lines 87–93 neither authenticate nor load a directory before
  launching the service.  The manifest parser at lines 38–61 is therefore
  disconnected from the service.  Even called directly, it does not bind a
  caller's session/caps, require `companion_len=accepted*cp`, check the final
  offset against `transcript_len`, replay/count transcript records, cross-bind
  accepted pivot/lead/ID/scale/basis records, or authenticate a committed
  prefix before truncating a provisional suffix.
- Wrapper lines 113–118 reinterpret the C offer count in the response's
  `pivot` field as `generation`, report the always-zero `lead` as `offers`,
  and turn the always-zero `scale` into an eight-byte fake digest.

Thus a restarted process silently appends while believing rank and offer count
are zero.  It cannot continue the same transducer state, detect a wrong session,
or establish a durable boundary as required by Task 574 §§4–5.

### F2. The persistent layout is structurally corrupt

All of the following occur in C line 36:

- `offsets.bin` receives the current transcript position before **and** after
  every offer.  It receives no initial zero when the fresh service has zero
  offers.  After two records the shape is `[0,E1,E1,E2]`, not the required
  `[0,E1,E2]`; in general it has `2n` entries rather than `n+1`.
- On an accepted companion offer, the code writes primary `w` and companion
  `g` consecutively to `basis.bin`.  That contradicts the required
  primary-only row size and makes `accepted*p` reconstruction impossible.
- It writes `g` to `companion.bin` on every companion-mode offer, including
  dependent offers.  The resume basis needs exactly one normalized companion
  per accepted pivot, not one remainder per offer.
- None of `put64`, `fwrite`, `fputc`, or these state transitions is checked or
  rolled back.  The in-memory row/map is installed before unchecked writes,
  so an acknowledged result need not match durable bytes.

This violates the exact `basis`, `companion`, transcript, and `n+1` offset laws
in Task 574 lines 108–138, independently of the missing manifest.

### F3. Resource caps, file safety, and numeric/portable-C contracts fail

- C line 28 explicitly discards `byte_cap` with `(void)bytes`; `offer_cap` is
  used only as a nonzero startup test at line 30.  Line 36 never predicts or
  enforces offer, transcript, offset, basis, lead, or companion consumption.
  It can therefore cross both caller-supplied caps while mutating live state.
- Allocation failure is returned as status `FATAL` and the loop continues
  (line 36), rather than transactional `UNKNOWN_RESOURCE`; partial allocation
  and all partial writes lack the required rollback-or-fatal-exit behavior.
- Every `fopen` result at C line 31 is unchecked.  If the directory is absent,
  the service can still accept and reduce rows entirely in memory.  If only
  some opens fail, `ftell(tf)` can even be reached through a non-null offsets
  stream with a null transcript stream.
- Transcript positions are an unchecked `ftell`/`long` cast at line 36, not a
  checked 64-bit file-position interface.  Binary mode is not established for
  Windows stdin/stdout (the state streams themselves do use `ab+`).  Close
  errors at line 37 and response writes at line 26 are ignored.
- CLI conversions at line 29 use `strtoull(..., NULL, 10)` without checking
  `errno` or an end pointer, so values such as `8junk` are accepted.  The
  session is then explicitly unused and never binds a state directory.
- Progress is printed and flushed once per offer at line 36, rather than at
  the required bounded cadence of at least 256 offers or 15 seconds by
  default.

These are correctness failures for the bounded production envelope, not mere
performance/style observations.

### F4. The live protocol and wrapper are only partially bound

- Python line 14 declares `REQ`, but `offer()` at line 97 sends only an op byte,
  ID, and implicit-width payload.  C line 36 consumes that ad-hoc stream.  No
  request magic, version, flags, or checked payload length is present, contrary
  to the fixed checked header requirement.
- Wrapper lines 98–111 do correctly require response magic, a typed offer
  status, and the echoed opaque ID.  They do **not** validate response flags or
  padding, bound `n`/`clen`, validate reduction coefficients/pivot ancestry,
  enforce status-specific zero/payload fields, validate accepted lead/lc/scale,
  or bind companion length to mode and status.  A corrupt length can drive an
  unbounded blocking read.
- Wrapper construction (lines 87–93) does not create the state directory and
  does not strictly validate or bind session, rank/offer/byte caps, or the
  manifest generation/counts.
- `close()` at lines 119–123 ignores the content and length of the close
  response, closes stdout immediately, and waits with no protocol EOF/exit
  bound.  It can hang rather than report the required fatal protocol error.

The narrow opaque-ID echo check passes; the complete response/state binding
contract does not.

### F5. The checker does not test the candidate paths it labels PASS

- Checker lines 71–75 apply thirteen lambdas that merely return integers and
  then deliberately raise/catch `ValueError`.  They mutate no candidate file,
  manifest, protocol message, digest, session, cap, or semantic record.
  Consequently `mutations_rejected = 13` is synthetic telemetry.
- Line 88 hard-codes `offset_eof`, `checkpoint_resume`, `dynamic_closure`,
  `expression_replay`, `member_nonmember`, and other fields to `"PASS"`.
  There is no checkpoint request, process kill/restart, manifest creation,
  corrupt prefix/suffix, cap test, or actual state-file inspection anywhere in
  the checker.  Lines 66–68 test only a dense in-memory member target; no
  primary nonmember candidate path supports `member_nonmember`.
- The offset assertion at line 67 constructs each expected record from the
  record being compared and never creates or reads `offsets.bin`; it cannot
  detect the C `2n` layout.
- The optional compiled fixture does not create its `service` directory
  (lines 78–82), so unchecked `fopen` failures would permit an in-memory pass.
  Moreover, for `width=4`, each offer should contain one packed row byte, but
  lines 83 and 85 append three surplus zero bytes.  After the first offer C
  reads the first surplus byte as opcode zero, emits `MALFORMED`, and exits;
  therefore this is not even a correctly framed two-offer service fixture.
- Companion testing at lines 69–70 and all resume-like labels exercise only
  the dense Python reference.  The reference's accepted-pivot companion index
  is repaired, but it supplies no evidence about the C files or resume path.

The checker's honest compiler status is useful, and its dense algebra gives
limited local evidence.  Its printed PASS labels cannot promote a persistent
worker candidate.

## 3. Disposition of Task 576's eight root findings

| item | disposition |
|---:|---|
| 1 | **CONFIRMED.** No manifest/state load or reconstruction exists; C starts with an empty map and appends. |
| 2 | **CONFIRMED.** Zero offers has no offset; each offer writes a start and EOF, producing `2n` entries instead of `n+1`. |
| 3 | **CONFIRMED.** Accepted companion bytes are also appended to `basis.bin`, and `companion.bin` receives every offer remainder. |
| 4 | **CONFIRMED.** `CHECKPOINT` is a status response only; no durability, atomic manifest, hashes, or genuine generation exists. |
| 5 | **CONFIRMED.** State opens are unchecked, while the optional compiled fixture omits the state directory and inspects no files. |
| 6 | **CONFIRMED.** Offer/byte caps are unenforced, progress is per-offer, and transcript positions use unchecked `ftell`. |
| 7 | **REFUTED as a defect, as required by the corrected task.** `pb` uses weights `1,3,9,27`; four trits range bijectively over bytes 0–80.  Decimal byte 3 is canonical `(0,1,0,0)`, so the `byte <= 80` check is sufficient for this format. |
| 8 | **CONFIRMED.** The named checkpoint/resume/corruption/cap/state-length paths are absent, and all thirteen “mutations” are synthetic lambdas. |

## 4. Required secondary checks and v2 comparison

| surface | result |
|---|---|
| Rank-cap dependent row | **Narrow PASS.** C line 36 reduces before testing `accepted>=rank`; a row reducing to zero remains `DEPENDENT` at full rank, while a genuinely new pivot returns `UNKNOWN_RESOURCE`. |
| Live accepted-row installation | **Narrow PASS versus v2.** Primary row, normalized companion, lead/ID, and lead-map entry are installed before the response.  This does not repair durability or transactional I/O. |
| stderr deadlock | **Narrow PASS versus v2.** Wrapper line 91 inherits stderr or redirects it to a file; it creates no unread stderr pipe.  Per-offer output still violates the cadence contract. |
| Strict integer parsing | **FAIL.** C accepts numeric prefixes with ignored tails; wrapper leaves most launch parameters unvalidated. |
| Transcript coefficient convention | **Algebraic core PASS only.** Reduction performs `w -= c*b`, records positive `c`, and normalizes with `scale=lc` (valid because `2^{-1}=2` in GF(3)), yielding `input = sum(q_i*basis_i) + scale*new_basis`. |
| Transcript pivot semantics | **Persistent contract FAIL.** Uninterrupted pivot indices are ordered, but no resume reconstruction or record-count/offset/lead/ID/scale/basis cross-binding exists. |
| Wrapper response binding | **Opaque-ID PASS; full binding FAIL.** ID/magic/status are checked, but the response lengths, pairs, flags/padding, status payload, companion mode, checkpoint fields, session/caps/generation/counts are not. |
| v2 wrapper iterator/reference defects | **Locally repaired.** `iter_transcript` no longer uses the undefined v2 `status`, streams the record file, and the dense helper indexes companion rows by accepted pivot.  These local repairs do not reach the C persistence defects. |

## 5. Claim boundary

The only executable result is a Python syntax check plus a dense reference
fixture whose compiled path was not run.  Its output is candidate telemetry,
not a cross-check of the production service and not a Lean verification.
Neither a grade-two result nor A0/COMMON/cofinal-lift/fake/Ihara evidence was
produced.  No result from this candidate can be promoted; the release gate
remains closed.
