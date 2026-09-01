# Luna Task443 — A4 delta tracker pre-loop repair v21

## Status

PASS for the bounded implementation scope.  No GAP, real 6,441-row replay,
production, GHA, commit, push, or dispatch was run.

The v20 arithmetic, 6,441-row authority, evaluator, oracle, rank logic,
K/queue rules, word ancestry, limits, and terminal meanings are byte-frozen.
The generated v21 changes only delta transport plus the placement of its
pre-loop snapshot.

## Canonical-base pin correction

Task443 line 22 repeats the already-rejected hash containing
`...d871d4dc...`.  Task414 explicitly adjudicated that value as erroneous;
the canonical 25,581-byte run-33263899806 base ends in
`...d871c4dc...`.  This is also the value in the exact generated v20
producer, generated v26 checker, embedded v30 seed, and v38 empty HEAD.
Following the parent ruling, v21/v27/v39 retain the canonical identity

```text
bytes   = 25581
sha256  = 595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445
next_row = 25
```

The erroneous `...d871d4dc...` value occurs zero times in both generated
v21 and generated v27.

## Outputs and pins

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v21.py` | 13268 | `23d90839025ae7dafdfef1a358666c640a32844544b4460aecec72644c6e0236` |
| generated v21 producer | 256315 | `e1005be315d97b5045965921ba93a72ea2a8c5024e3abf1dbda5459a09c99f76` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v27.py` | 21489 | `79f42e751684f12814ac25dc7bd17ee5a6fa21b8ab9b8bdfc07c14bd37e4af2a` |
| generated v27 checker | 281781 | `5e0604a1c8560f79aed917f583162a896c788fd894ff192a7201c282c1276911` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v39.g` | 6005 | `3494d194115d7cb2f52ac1c1f8cedb43719f8ea4088ecc604b6aaa6fff9a5d4f` |
| statically reconstructed v39 inner driver | 76466 | `d0b822a9414071427e94fa293a8e62970322c58afa1934a12a9fbdd1b881ffb7` |
| v39 sealed empty producer HEAD | 544 | `d324f9b7708802165c05b1581c3f75afedd6f7e43cdbe8a87dbfd270150ec1e5` |

Exact frozen owners:

- v21 wrapper owner: v20, 2,239 bytes,
  `c45d48ac27f462cf342912e17e619be02ca68322c62a21897fcdc3d524e07a6f`;
- v20 generated owner: 251,799 bytes,
  `b41728b707a21e9fd6487ce015fe4df2dfd6c0040f0d098a399143a55600b2ee`;
- v27 wrapper owner: v26, 2,216 bytes,
  `b447bfc371090262a881db4b76261c534a8ef7a2b884edd65729aba1ea5fb2f4`;
- v26 generated owner: 272,663 bytes,
  `ffd53a2df28252feaf84fa5d96a3bc2bec8bf8d6e5ca31424be55ba8c24fb1dd`;
- v39 semantic driver owner: v38, 5,283 bytes,
  `0aa69186576111e5931cd4428c56967432c148cef823d079cf1977ce588465ff`;
- v39 reconstruction base: v30, 76,229 bytes,
  `bacea39ac0615e0051d5cb59356f45f7fd8b8cd6867bad7b2bc2ec286949575c`.

The empty HEAD has `segment_count=0`, `last_sequence=0`, `last_row=24`,
`next_row=25`, zero rolling chain, canonical base identity, and self seal
`170b4de9d4b3cc10242503f9a0630da4de9fcbd4b49c4823f10cae638fd4c4ea`.

## Repair implemented

The producer has ten exact-cardinality generated-source patches:

1. `_a4_delta_tracker` now records the restored matrix as well as restored
   oracle, word DAG, queue, actions, action-event chain, counters, and prior
   delta metadata.
2. Lazy post-row tracker creation was removed.  A delta writer without the
   pre-loop tracker fails closed.
3. After restored counters are installed and before the row loop, the tracker
   is created exactly once and receives `last_row=resume_row-1` and
   `last_next_row=resume_row`.
4. While the cursor is at a row, a write requires exactly one new row digest,
   exactly one new bridge digest, and exactly one corresponding terminal
   `R:<ordinal>` record/event pair.  Ordinal and next-row continuity are
   required.  K/insertion/queue appends may be empty.
5. The final row is still typed as a row even though its next cursor is
   `ROWS+1`; later writes at that cursor are queue segments.
6. Producer reference and restore paths reject empty/skipped/forged row
   segments, replay record/event indices and epoch, apply the delta, and check
   the reconstructed row/bridge cursor advance.
7. Segment append precedes atomic HEAD replacement; the tracker advances only
   after HEAD.  Immutable base, previous segment seal, and rolling chain are
   unchanged.

Thus run 33303302455's zero-row first segment is rejected before a HEAD can be
advanced and is never migrated.

The independent v27 checker has six exact-cardinality generated-source
patches.  It pins the exact v21 wrapper, loads the byte-pinned canonical base,
independently reconstructs every segment, checks sequence/previous/chain,
ordinal/next-row, record/event/epoch, row and bridge deltas, queue/action
transport, and binds the reconstructed cursor to HEAD and the producer
terminal reference.

The v39 driver retains exact v38 RESUME semantics.  It seeds the producer only
from the canonical next-row-25 base and a valid empty v39 HEAD.  The inherited
`D386InstallSeed` first authenticates any existing target; a nonempty or
corrupt existing HEAD is rejected rather than overwritten.  A later nonempty
continuation therefore requires a new versioned driver.

## Bounded checks

- Python wrapper and generated-source compilation: PASS.
- Frozen owner/generated hashes and unique replacement cardinalities: PASS
  (`producer=10`, `checker=6`; driver has seven unique source replacements
  plus one unique HEAD-path and one unique HEAD-seal rewrite).
- Generated-source diff confinement: PASS.  Producer changes are confined to
  the delta transport block and the pre-loop tracker placement; checker
  changes are confined to its delta validator and producer pin.
- Canonical base pin: PASS (`producer occurrences=2`, `checker occurrences=1`,
  erroneous occurrences=0).
- Pre-loop order: PASS (restored counters installed, tracker snapshot, row
  loop).
- Atomic order: PASS (segment append, atomic HEAD, tracker update).
- Tiny next-row-25 base plus row 25 and row 26 synthetic chain: PASS;
  reconstructed cursor is 27.
- Eight required mutations: all REJECT — empty first-row segment, skipped row
  25, forged `next_row=27`, row-digest deletion, bridge deletion, terminal
  event deletion, reordered segment, and HEAD ahead of segment.
- Empty v39 HEAD physical hash and self seal: PASS.
- Driver source/command reconstruction: PASS; v21/v27 pins, producer base and
  HEAD seeds, RESUME ancestry, checkpoint paths, and absence of a v39 SELFTEST
  mode were all found.
- `git diff --check` on the four authorized outputs: PASS.

No arithmetic source changed.

## Parent dispatch contract

No dispatch was performed.  If the parent authorizes it after audit, the
generic `gap-run.yml` inputs are exactly:

```text
script=search/d972_r07_word_independent_successor_kernel_gha_driver_v39.g
preamble=D386Mode:="RESUME";;
out_dir=ci/out
timeout_min=250
with_pquot_packages=true
```

As a JSON string, the preamble value is
`"D386Mode:=\"RESUME\";;"`.

`TASK443_R07_A4_DELTA_TRACKER_PRELOOP_V21_PASS`

## Parent dispatch record (2026-09-01)

- committed and pushed source SHA:
  `0f3902147257c769de3035fadfeac6b365a160ca`;
- workflow: `gap-run.yml` on `sol/r07-explicit-lift-20260825`;
- run id: `33501365999`;
- inputs: v39 driver, `D386Mode:="RESUME";;`, `ci/out`, 250 minutes,
  pquot packages enabled;
- dispatched at `2026-09-01T20:13:32+09:00`; result pending.

The first dispatch failed before computation because Windows native-argument
quoting removed the quotes around `RESUME`; GAP received
`D386Mode:=RESUME;;`. Run `33501365999`, job `99835240865`, stopped at the
driver preamble with `Variable: 'RESUME' must have a value` and produced no
mathematical result. After checking the actual native argv, the unchanged
source commit was redispatched with escaped literal quotes:

- corrected run id: `33501732575`;
- corrected preamble received from the broker:
  `D386Mode:=\"RESUME\";;` (GAP source `D386Mode:="RESUME";;`);
- source SHA remains `0f3902147257c769de3035fadfeac6b365a160ca`;
- result pending.
