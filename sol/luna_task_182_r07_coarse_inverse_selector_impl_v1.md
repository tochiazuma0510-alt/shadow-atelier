# Luna task 182 — task179 coarse-inverse singleton selector implementation v1

Commissioner: Sol / 2026-08-27

Role: Luna bounded mechanical implementation and static audit.  Do not alter
the mathematics.  Do not run Python, Node, GAP, git, or GHA locally.

## 1. Governing theorem

Implement exactly
`sol/proof_r07_actual_singleton_coarse_inverse_selector_v142.md`.

The old task179 `FibreOracle.canonical` performs one complete 1,469,664-state
Q0 scan for every new `(coordinate,target)`.  Replace that lookup only.  Do
not change the eleven-occurrence formula, target, boundary oracle, Gaussian
logic, word convention, terminals, or checker independence.

## 2. Required index

For each coordinate lazily build an open-addressed inverse of the coarse
section map.

- Fixed state count: 1,469,664.
- Fixed table length: (2^{22}=4,194,304).
- Store only unsigned 32-bit `qid+1`; zero is empty.  Use a compact standard
  library buffer such as `array('I')`, and hard-check that its item size is 4.
- Insert qids in increasing order.
- Probe by a process-local hash of the exact coarse bytes.  On every occupied
  slot compare the exact coarse bytes read from the existing coordinate
  store at the stored qid.  Hash equality alone is never evidence.
- If the same exact coarse key is encountered at a different qid, hard STOP;
  this independently replays task176 coarse injectivity.
- The randomized hash seed may change slots but must not change the selected
  qid or any receipt field.
- Build lazily and retain at most one table per coordinate.  Ten tables cost
  exactly 167,772,160 payload bytes.  Do not duplicate the 1.42 GB coordinate
  stores.
- Charge the one-time qid insertions to the existing `fibre_scans` counter;
  wall and RSS gates remain active.  Record public index count/table length,
  injectivity, and payload bytes in checkpoint/input metadata without
  serializing the tables.

## 3. Exact canonical selector

For target `t` in coordinate `i`:

1. Iterate distinct singleton `A_maps["S{i}"]` values in first Gamma-state
   order.
2. Compute the complete packed `section_target = a^-1 * t`.
3. Look up `section_target`'s coarse bytes in the new index.
4. Compare the complete stored section blob with `section_target`; coarse
   equality alone is insufficient.
5. Verify `a * section == t`, rebuild all ten coordinate blobs and the
   literal `Gamma-word + Q0-word`, and replay the word exactly as before.
6. Select the least `(qid,gid)` so the result is byte-for-byte the old
   "first Q0, then first Gamma" selector.

Cache successes and empty fibres exactly as before.  The positive/global/
kernel schedule remains unchanged.

## 4. Two bounded repairs permitted in the same files

1. Replace whole-file pin reads and avoidable `bytes(store)` /
   `b"".join(qstates)` digest copies by chunked or buffer-streamed hashing,
   without changing any digest value.
2. Replace global-roster exhaustion's generic `RuntimeError` with an honest
   registered positive-only `UNKNOWN_RESOURCE` path.  Exhaustion must never
   become a separator or negative claim.

## 5. Checker and SELFTEST

Extend the noncommutative SELFTEST with a small collision-forced coarse
inverse table (use an injectable deliberately poor hash only in SELFTEST).
It must prove:

- exact-key collision resolution;
- duplicate coarse-key rejection;
- least `(qid,gid)` selection;
- full packed mismatch rejection after a coarse hit; and
- unchanged fifteen existing semantic mutation rejections.

The helper-nonshared checker must validate the public selector provenance on
a COMMON_WORD receipt by reconstructing the chosen section directly; it must
not import or trust the producer's index helper.  UNKNOWN remains claim-free.

## 6. Pin cascade boundary

The parent is currently finalizing task175 and the task175/task176 pins.
Implement against the live files, but leave a clearly marked one-time parent
pin cascade if their identities are not yet frozen.  Cascade in this order:

1. task179 producer pins;
2. checker producer pin and shared predecessor pins;
3. driver producer/checker pins and all predecessor pins;
4. reply identities.

Do not edit task175, task176, any proof, any workflow, or any file outside:

- `search/d972_r07_positive_common_word_colgen_v1.py`
- `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py`
- `search/d972_r07_positive_common_word_colgen_gha_driver_v1.g`
- `search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json`
- `sol/luna_reply_182_r07_coarse_inverse_selector_impl_v1.md`

Return static verdict, exact bytes/SHA-256, memory accounting, and any
remaining execution blocker in the reply.
