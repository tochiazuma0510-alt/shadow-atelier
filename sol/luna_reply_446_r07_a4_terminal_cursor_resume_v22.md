# Luna Task446 - A4 terminal-cursor continuation v22

## Status

PASS for the bounded implementation scope.  The accepted row-25 segment from
run `33501732575` is retained, and the new continuation resumes at row 26.
No GAP, production, real 6,441-row computation, GHA, git commit, push, or
dispatch was run.

## Diagnosis fixed

Run `33501732575` did write row 25 durably.  Its authenticated HEAD has
`last_row=25`, `next_row=26`, and `segment_count=1`; delta 00000001 has one
row digest, one bridge digest, and one `R:25` record/event pair in both the
ordinary and initial-terminal fields.  The row-25 segment is therefore not a
row-25/26 merge.

The failure was in the second writer call.  Generated v21 initialized the two
terminal cursors at 24 but omitted them from the successful post-HEAD tracker
update.  Thus row 26 had an ordinary delta containing only `R:26` but an
initial-terminal slice containing `R:25,R:26`, and the pre-append gate rejected
it with `delta:one_row_terminal_pair`.  Since validation precedes segment append
and HEAD replacement, row 26 was never durable and is recomputed by v40.

Generated v22 changes only the successful tracker update:

```text
segment append                 generated line 154
atomic HEAD replacement        generated line 160
tracker update begins          generated line 162
initial_records cursor advance generated line 165
initial_events cursor advance  generated line 166
```

Each terminal cursor advances by the exact length already present in the
accepted segment body.  There is no scan, matrix copy, cadence change, or
arithmetic/gate/evaluator/queue change.  A rejected segment still cannot
advance any cursor.

## Outputs and exact pins

| object | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v22.py` | 4055 | `0186a8711ae356d1d01d7ccbd4e618ec5d19fa36442812a5dcfa8c452837d2c2` |
| generated v22 producer | 256509 | `20fdeb66f70f428152e06f5e7a92b455dd211bd0e72d665c10d24d2ad0491e94` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v28.py` | 11048 | `c2c1629dc225ebea085b72d1900d7684f4c4184f8e064da8ec4057dc921d2bfa` |
| generated v28 checker | 281780 | `444ee68e79715657707c77778fcb597f83d289147699e7ce5295414b956edeae` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v40.g` | 16871 | `0c87000b7b3b26012b2d68f40e0029e591722aa79f2d6fda37f115fd027b6457` |
| statically reconstructed v40 inner driver | 76586 | `f407a306d25a0ace6bd347615195d94c2f4bc73625dbe9ac055fd02d5ea3961f` |

Frozen owners:

- v22 owns exact v21: 13,268 bytes,
  `23d90839025ae7dafdfef1a358666c640a32844544b4460aecec72644c6e0236`;
  generated owner: 256,315 bytes,
  `e1005be315d97b5045965921ba93a72ea2a8c5024e3abf1dbda5459a09c99f76`.
- v28 owns exact v27: 21,489 bytes,
  `79f42e751684f12814ac25dc7bd17ee5a6fa21b8ab9b8bdfc07c14bd37e4af2a`;
  generated owner: 281,781 bytes,
  `5e0604a1c8560f79aed917f583162a896c788fd894ff192a7201c282c1276911`.
- v40 pins exact v39: 6,005 bytes,
  `3494d194115d7cb2f52ac1c1f8cedb43719f8ea4088ecc604b6aaa6fff9a5d4f`,
  and exact v30 reconstruction base: 76,229 bytes,
  `bacea39ac0615e0051d5cb59356f45f7fd8b8cd6867bad7b2bc2ec286949575c`.

## Embedded continuation chain

The immutable canonical base embedded in the pinned v30 ancestry was decoded
and compared byte-for-byte with the downloaded run artifact:

| object | bytes | SHA-256 |
|---|---:|---|
| canonical base | 25581 | `595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445` |
| exact run source delta 00000001 | 3551 | `1d9818a7f9b867ebdefb751b7309aca22db5d6dccac917fddeb494bc18dbe1b5` |
| exact run source nonempty HEAD | 700 | `297c91e13dce929925246b19fa9735a57b2656d9875d35b347773c918f65b1c0` |
| v40-path rebound delta 00000001 | 3551 | `d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19` |
| v40-path rebound nonempty HEAD | 700 | `a8181cb36651403b7a20386a4b8d63ea301ccdda09ce5d7d8f202e3799a24d08` |

v40 authenticates the exact source delta and HEAD before changing only their
equal-length v39 path strings and dependent chain/seal fields.  The rebound
chain is
`2fea1d5275a3bf03170fe25bfff70218601a41996cc20416220a56fbb7017ee0`;
the delta self seal is
`dcdbf2da88ef7ec4f809e12c716cbb694077a626b2238d48f79735e9806a357d`;
the HEAD self seal is
`bc70c9582bc9abd2085ea07f487bc0d92c7130d46cecbc3728b023b1ece8ef8f`.

Static reconstruction confirmed seed order:

1. canonical v40 base;
2. accepted v40 delta 00000001;
3. authenticated nonempty v40 HEAD (`last_row=25`, `next_row=26`);
4. checker base.

The inherited installer accepts an existing target only when its bytes and
SHA are identical.  Missing files are written and read back under the same
pins; any nonidentical base, delta, HEAD, or checker checkpoint stops.  The
rejected row-26 result and terminal envelope are not embedded or consumed.

## Bounded checks

- Wrapper syntax and generated-source compilation: PASS.
- Frozen owner/generated hashes and unique patch cardinality: PASS
  (`producer=1`, `checker production pin=1`).
- Generated-source diff confinement: PASS.  v21 -> v22 adds only the two
  terminal cursor updates; v27 -> v28 changes only the exact producer path,
  byte count, and SHA pin.
- v22 two-row cursor fixture: PASS; after accepting row 25, both terminal
  cursors are 25 and the next slices contain only `R:26`.
- Independent v28 two-row fixture: PASS.  Row 26 alone occurs in its row
  digest, bridge digest, ordinary record/event, and initial-terminal
  record/event fields.
- Ten independent mutations: all REJECT, including separate stale terminal
  record-cursor and stale terminal event-cursor mutations, in addition to the
  eight v27 segment/HEAD mutations.
- Exact source artifact decoding and v40 re-sealing: PASS; delta/HEAD
  cardinalities, `ordinal=25`, `next_row=26`, sequence/previous/chain, all six
  one-item row fields, file hashes, and self seals agree.
- Static v40 reconstruction: PASS; exact v22/v28 pins occur once, inner bytes
  and SHA match the table, seed order is base < delta1 < HEAD < checker, and
  no `SELFTEST` or `PRODUCTION` route occurs in v40.
- ASCII/final-newline/trailing-whitespace and `git diff --no-index --check`
  checks on the three code outputs: PASS.

No arithmetic source changed.  No production SELFTEST, full reconstruction,
or new heavy calculation was added.

The later parent dispatch contract remains `D386Mode:="RESUME";;` with the
v40 driver.  No dispatch was performed here.

`TASK446_R07_A4_TERMINAL_CURSOR_RESUME_V22_PASS`

## Parent bounded audit

Parent replay and a separate Sol read-only audit both returned **GO**.  The
generated v21-to-v22 diff contains only the two terminal cursor advances, the
v28 two-row fixture rejects all ten registered mutations, and the exact
run-33501732575 delta/HEAD pins agree byte-for-byte with the downloaded
artifact.  Static reconstruction gives the reported 76,586-byte inner driver
with seed order canonical base, accepted delta 00000001, nonempty HEAD, then
checker checkpoint.  Its authenticated HEAD resumes at row 26.  No arithmetic,
cadence, queue/evaluator, or production resource contract changed.
