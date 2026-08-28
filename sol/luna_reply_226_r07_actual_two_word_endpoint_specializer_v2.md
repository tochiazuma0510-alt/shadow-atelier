# Luna reply 254 — task226 mod-9 bracket normalization repair

Status: **UNEXECUTED**. No Python, GAP, git, GHA, or network command was run.
Only the five authorized task226 files were edited.

## Static repair

The producer and independent checker now normalize every public PB3/PB4
bracket lookup to canonical residues in `0..8` for both `(i,j)` orientations.
The literal PB3/PB4 tables retain their actual mathematical signs, and the
class-2 multiplication, commutator convention, direct roster checks, and
bracket assertions remain intact.

Both independent SELFTEST paths now assert non-vacuously that the negative
PB3 bracket `(0,2)` is `(8,)` and the negative PB4 bracket `(0,3)` is
`(8,0,0,0)`. The existing exhaustive direct-roster checks therefore exercise
the canonicalized values; no mutation roster extension was needed.

The driver continues comparing lowercase `sha256sum` output and was repinned
to the repaired producer/checker. Conclusion flags remain false pending parent
execution and audit.

## Final identities

```text
producer  40014  967be8bca0723feadcb3318cf77fc2e6ea81e85b11bea6c0b5e7a81a66134fc4
checker   33996  5c3b3d8f4c3736db5b85ff9c86b1c70f0115dd390763b9d279b03e733347966e
driver     5167  db7dc638de31f2e9f06bb7b378b107ca4e603bdff48a75d527c11cc18f6c7160
fixture     1187  91c62b70b3275e9e3bee9689bd677049adc172cb0519a2ccf2808d17d6cabef3
reply     pending final byte/SHA calculation (self-referential digest avoided)
```

```text
A2 PAPER CONTRACT:                 1/3
A2 IMPLEMENTATION SELFTEST:        0/1 UNEXECUTED
A2 ACTUAL SPECIALIZATION:          0/1 AWAITING A0/A1
COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```

`TASK254_TASK226_MOD9_BRACKET_NORMALIZATION_UNEXECUTED`
