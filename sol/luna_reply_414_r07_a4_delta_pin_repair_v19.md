# Luna task 414 — R07 A4 delta-checkpoint canonical pin repair v19

## Status

PASS (v34 supersedes the defective v33 wrapper).  The task410 v18/v24 append-only delta transport is frozen as the
  producer/checker owner.  Only the legacy-base hash and checkpoint schema pins
were advanced; arithmetic, row order, reducer, oracle, cap, and transport
  semantics are unchanged.  The v34 driver installs the canonical seed at both
the producer HEAD and delta-chain base paths before Python starts, preserving
the base for ancestry.

## Versioned outputs

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v19.py` | 2388 | `c7add6648f53e4ec85eb40620e3469008349e5676ac7d9602a6699a52cb4c6c1` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v25.py` | 2540 | `4c04fd31fe4a27c96841ddc5931961cc6d2e4162f98f239df3577ee367a57317` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v33.g` | 4299 | `348732f85a0c7d96ac38692464bf92af1dd47901f61a42f3d569504f5888034f` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v34.g` | 4372 | `a7d333b3120740db35f52969685f4029fcdffc0e5132a3ef4e9ac9a614df66b2` |

Generated-source pins:

- producer: 251746 bytes / `223dd0b759780ed90b8d259311646a41425f40bf00b161e187a98cde73d7c796`;
- checker: 272663 bytes / `344168094ed6dd597b4a5d15bda87d2c348d4fa233e9de7ba1eb7426ef201493`;

## Bounded gates

- Both wrappers compile; both generated Python sources parse as AST.
- The embedded v30 seed decodes to 25581 bytes, SHA-256
  `595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445`,
  schema `d972-r07-word-independent-successor-kernel/v6/checkpoint/v1`,
  `next_row=25`, and code SHA-256
  `964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7`.
- A two-segment synthetic delta chain round-tripped (`last_sequence=2`,
  `last_row=26`, `next_row=27`); a mutated segment was rejected.
- Generated producer has zero `...d871d4dc...` strings and two canonical
  legacy-base identity gates.  The checker has zero erroneous strings and one
  canonical base gate.  Completed-row call sites use `write_checkpoint`; the
  persistent counter charges `len(encoded) + len(head_encoded)` only.
- GAP parsing reaches the intentional `D386Mode` guard.  The transformed v34
  inner driver retains literal `RESUME`, has no `SELFTEST`, installs the
  canonical seed at both producer HEAD and base (preserving base ancestry),
  under `*.producer.base.checkpoint.json`; its native RESUME producer command
  includes `--resume` on the transformed producer HEAD checkpoint path.
- The v33 failure was isolated to `D410Pairs[1]`: after the global version
  rewrite its parsed escaped needle had cardinality zero.  v34 corrects the
  escaped needle/value representation for pairs 1--5; construction exits 0,
  and the generated inner driver parses with GAP.

Exact bounded local checks:

```text
temporary predriver: D386Mode:="RESUME";;
temporary v34 construction: replace final Read(D410Inner);; with QUIT_GAP(0);;
CONSTRUCT_EXIT=0
GAP parse: ReadAsFunction(v34);; ReadAsFunction(ci/out/a4_task410_inner.g);;
PARSE_EXIT=0 (1150 expected unbound-global warning lines)
```

## Generic `gap-run.yml` dispatch inputs

No dispatch was performed.  The exact bounded production inputs are:

```text
script=search/d972_r07_word_independent_successor_kernel_gha_driver_v34.g
preamble=D386Mode:="RESUME";;
out_dir=ci/out
timeout_min=250
with_pquot_packages=true
```

`TASK414_R07_A4_DELTA_PIN_REPAIR_V19`
