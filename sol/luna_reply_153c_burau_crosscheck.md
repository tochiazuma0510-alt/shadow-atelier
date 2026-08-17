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
