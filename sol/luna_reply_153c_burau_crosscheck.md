# Luna reply 153c — independent Burau-fiber cross-check

## Scope and implementation

Replaced only `search/check_d972_b4_burau_fiber_v1.py`.  The checker is
helper-independent: it does not import GAP or the producer.  It independently
reconstructs:

- `MakeDn(9)`/`MakeGn(9)`, GF(8) arithmetic, the PSL(2,8) projective action,
  and the compact 36-point roof;
- all 972 signed representative words and their exact stored keys;
- explicit unreduced Burau matrices over GF(3) and GF(4), all six pure
  generators, the five literal A.18 pairs, and the opposite-convention raw
  defect;
- `H`, `H'`, and the faithful roof kernel using SymPy 1.14's
  `PermutationGroup`, `derived_subgroup`, and successive point stabilizers.

The checker consumes the producer's full one-line `fiber_representative` and
reconstructs each exact `h0*K` coset.  It does not trust producer kernel dumps
or declared fiber digests; optional digests are independently compared when
present.  Every nonempty coset element is replayed through all five finite
components.  A candidate producer status
`CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER` is promoted to
`B4_A_BURAU_FINITE_ZERO_FIBER_CROSSCHECKED` only after these checks.  A
producer self-label of `...CROSSCHECKED` is rejected.  Empty or incomplete
fibers fail closed; all-pass remains `UNKNOWN_BURAU_SPECIALIZATION_ALLPASS`.

## Checks run

`python search/check_d972_b4_burau_fiber_v1.py --self-test` passed, including
real negative mutations for reversed `PaperProd`, reversed `x13`, swapped
leading A.18 factors on a common two-letter word, deletion of a kernel
element, and corrupt roof word/key.  The independent roof replay matched all
972 artifact rows.  Python compilation passed.

For `(q,a)=(3,-1)`, the independently built combined generators have degree
441 and SymPy reports:

| object | order |
|---|---:|
| `H` | 105,815,808 |
| `H'` | 2,939,328 |
| `ker(pi\|H')` | 8 |

The kernel was enumerated by the 36 successive point stabilizers.  No producer
receipt was available during this cross-check, so no terminal A/UNKNOWN
classification was issued from a finite fiber scan.

Checker SHA-256:
`819519e93a95e0fbff7b7d4d51f5af633da029e033f33038f100db968e53169e`.

The independent roof gates also give `|P|=1,469,664` and
`|P'|=367,416`; receipt checking compares the independently projected `H'`
image against the latter order and the recorded projection order.

## Interoperability contract

The checker expects the candidate receipt schema to provide `h_generators`,
`fiber_representative`, `fiber_size`,
`identity_image_defect_count`, and
`nonidentity_image_defect_count`; `fiber_digest` and full kernel dumps are
optional.  A supplied `first_defect_witness` must be an actual nonidentity
defect one-line permutation from that exact coset.

## Sequential GHA receipt execution evidence (2026-08-18)

I ran the existing v1 checker sequentially, without GAP, on the downloaded
receipts from runs `32040067382` (q=3) and `32040069470` (q=4).

### q=3 — run 32040067382

The receipt SHA-256 matched the supplied value:

```text
2AADB563AF127B0E35B534AA24144A4F005A4C00CDB677785F7B9D78C0828998
```

Checker stdout ended with:

```text
ValueError: fiber representative roof target drift at 1
```

Process exit: `1`; checker verdict: `FAIL/CHECKER_BLOCKED`.

### q=4 — run 32040069470

The receipt SHA-256 matched the supplied value:

```text
9DE5C5B503765DF6E7063CCCFF71AB0288399C47BB0ED1CB006F195705E739DE
```

Checker stdout ended with:

```text
ValueError: fiber representative roof target drift at 1
```

Process exit: `1`; checker verdict: `FAIL/CHECKER_BLOCKED`.

The failure is an existing v1-checker defect, not a producer receipt verdict:
`_roof_images_for_key` concatenates three local D9 one-line permutations without
adding block offsets, producing repeated `1..9` values instead of a 27-point
direct sum.  For q=3 row 1, the receipt representative's first 36 points are
the identity and the target key is the identity, confirming this exact false
negative.  No A/B conclusion is authorized from these blocked checker runs.

## Repaired sequential rerun evidence (2026-08-18)

I repaired both independent checkers by reconstructing the key image as a
direct sum with D9 offsets `0,9,18` and PSL offsets `27`; both now include an
all-972 stored-key/direct-word image regression gate.  Lightweight compile and
self-tests passed for both checkers.

The same receipts were then checked sequentially, q3 followed by q4, without
GAP.

### q=3 — run 32040067382

Receipt SHA-256:

```text
2AADB563AF127B0E35B534AA24144A4F005A4C00CDB677785F7B9D78C0828998
```

Exact checker stdout:

```text
D972_B4_BURAU_FIBER_CHECK_PASS {"kernel_order": 8, "rows": 972, "status": "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS", "zero_fibers": 0}
```

Process exit: `0`.

### q=4 — run 32040069470

Receipt SHA-256:

```text
9DE5C5B503765DF6E7063CCCFF71AB0288399C47BB0ED1CB006F195705E739DE
```

Exact checker stdout:

```text
D972_B4_BURAU_FIBER_CHECK_PASS {"kernel_order": 8, "rows": 972, "status": "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS", "zero_fibers": 0}
```

Process exit: `0`.

Updated checker SHA-256 values (before the Artin-relation audit gate):

```text
v1 fed97a1fcceb663449c6ba8de71b25bdf9b7894547e0ff15dbe4441ddef19a8a
v2 7fdf0a347abeb1c011374911437b733eb55a40653fc4b20857c51399884255c3
```

These are finite all-pass UNKNOWN results, not A/B evidence.

## Artin-relation audit and sequential rerun (2026-08-18)

The v1 receipt path and lightweight selftest now check all three B4 Artin
relations independently: the `(s1,s2)` and `(s2,s3)` braid relations and the
`(s1,s3)` commuting relation.  Compilation and selftest passed after this
gate was added.  The two existing receipts were rerun sequentially (q=3,
then q=4), with unchanged source SHA values and exact stdout:

```text
q=3 run=32040067382 receipt_sha256=2AADB563AF127B0E35B534AA24144A4F005A4C00CDB677785F7B9D78C0828998
D972_B4_BURAU_FIBER_CHECK_PASS {"kernel_order": 8, "rows": 972, "status": "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS", "zero_fibers": 0}
q=4 run=32040069470 receipt_sha256=9DE5C5B503765DF6E7063CCCFF71AB0288399C47BB0ED1CB006F195705E739DE
D972_B4_BURAU_FIBER_CHECK_PASS {"kernel_order": 8, "rows": 972, "status": "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS", "zero_fibers": 0}
```

Both processes exited `0`.  The repaired v1 checker SHA-256 is
`651420D4D04C17465C32772222BD531261290566444A0C0C03843BEB3FB299FB`.
These remain finite all-pass UNKNOWN results; no A/B verdict is authorized.
