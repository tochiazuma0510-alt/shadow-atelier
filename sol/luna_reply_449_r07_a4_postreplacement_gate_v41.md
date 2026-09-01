# Luna Task449 - A4 v40 post-replacement gate v41

## Status

PASS for the bounded driver-only repair.  No production, GHA, GAP, git,
commit, push, or dispatch was run.

## Output

| object | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v41.g` | 2674 | `002dcea0d78bb14252e975ff69311f596aac742392658a9b7fb7022cf5c17bbd` |

v41 exact-pins its v40 owner at 16,871 bytes /
`0c87000b7b3b26012b2d68f40e0029e591722aa79f2d6fda37f115fd027b6457`.
It makes one unique source replacement and pins the resulting patched v40 at
16,973 bytes /
`d03eec3d4d954929774516979467f15244a76cd7099e85ce60755c746bb5f7ce`.
The patched source is written, read back byte-for-byte, and then read as GAP
source.

## Exact repair

The only patched v40 source is the redundant post-replacement gate.  Static
reconstruction gives these old/new substring counts after all seven
replacements:

```text
P1=0/1  P2=0/1  P3=0/1  P4=0/1  P5=0/1  P6=0/1  P7=1/1
```

Pairs 1--6 therefore retain `old=0,new=1`.  Pair 7 now requires
`old=1,new=1`, because the inserted delta/HEAD seed prefix deliberately ends
with its unchanged old checker-seed suffix.  The pre-replacement uniqueness
check remains in `D446ReplaceOnce`.

No version string, execution path, artifact path, seed byte, resource,
checkpoint cadence, producer, checker, or arithmetic source changed.

## Static reconstruction

The repaired gate passes and reconstructs the unchanged v40 inner driver:

```text
bytes  = 76586
sha256 = f407a306d25a0ace6bd347615195d94c2f4bc73625dbe9ac055fd02d5ea3961f
```

Seed order remains canonical base, accepted delta 00000001, nonempty HEAD,
then checker base.  The embedded HEAD remains `last_row=25`, `next_row=26`,
`segment_count=1`, `last_sequence=1`; row 26 is still the next row to compute.
No new SELFTEST or fixture was added.

Fail-closed gates cover v40 owner drift, unique patch cardinality, patched
source bytes/SHA, write/readback identity, and the exact post-replacement
counts above.

`TASK449_R07_A4_POSTREPLACEMENT_GATE_V41_PASS`
