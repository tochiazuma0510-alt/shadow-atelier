# Task 576 — adversarial audit of packed GF(3) stream worker v3

Role: Sol(max), independent code/protocol auditor.  This is a bounded audit,
not an implementation task.  Do not edit the candidate.  Write only
`sol/sol_reply_576_audit_r07_packed_gf3_stream_worker_v3.md`.

Audit these frozen files:

- `search/d972_packed_gf3_stream_worker_v3.c`
- `search/d972_packed_gf3_stream_worker_v3.py`
- `search/check_d972_packed_gf3_stream_worker_v3.py`
- `sol/luna_reply_574_r07_packed_gf3_stream_worker_v3.md`
- requirements in `sol/luna_task_574_r07_packed_gf3_stream_worker_v3.md`
- prior failure contract in `sol/sol_reply_573_audit_r07_packed_gf3_stream_worker_v2.md`

The only release question is whether this exact implementation can safely be
used for the real grade-two bounded envelope.  A single load-bearing failure
is enough for FAIL; do not spend time polishing nonblocking style issues.

At minimum inspect and reproduce or refute these root static findings:

1. The C service opens append files but appears not to load any manifest,
   basis, lead map, transcript, offsets, or companion state on resume.
2. It appears to write two offset entries per offer instead of a single
   initial zero followed by one EOF per offer.
3. On an accepted companion row it appears to append the companion to both
   `basis.bin` and `companion.bin`; it also appends a companion remainder for
   every offer rather than accepted pivots only.
4. `checkpoint` appears only to return a status response: no flush/fsync,
   atomic manifest, authenticated committed lengths/digests, or generation.
5. State-file open failures appear unchecked, and the compiled fixture does
   not create its `service` directory, so a two-row algebra test may pass
   entirely in memory while persistence is absent.
6. `offer_cap` and `byte_cap` appear parsed but unenforced; progress is printed
   per offer rather than at bounded cadence; `ftell` is used rather than a
   large-file-safe offset.
7. Do **not** flag `byte <= 80` merely for accepting byte 3: the candidate
   uses canonical base-3 packing of four trits, so every byte 0..80 is valid.
   Check the encoding against that actual convention.
8. The checker appears not to compile-test a genuine checkpoint/kill/resume,
   companion resume, corrupt committed prefix, offer/byte cap, or actual
   state-file lengths/digests.  Its 13 mutation count may be synthetic rather
   than mutations of the candidate protocol.

Also check rank-cap dependent-row behavior, stderr deadlock behavior, strict
integer parsing, transcript coefficient/pivot semantics, and wrapper response
binding.  Run only seconds-scale local fixtures if useful; no GHA, workflow,
or production integration.

Return exactly one verdict:

- `PACKED_GF3_STREAM_WORKER_V3_PASS`, or
- `PACKED_GF3_STREAM_WORKER_V3_AUDIT_FAIL`.

For FAIL, list the minimum release blockers with file/line evidence and state
whether any candidate result can be promoted (normally no).  Record SHA-256
for all four frozen inputs and for the reply.
