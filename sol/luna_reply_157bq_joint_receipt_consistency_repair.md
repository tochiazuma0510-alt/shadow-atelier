# Luna reply 157bq — joint receipt consistency repair

## Verdict

The producer/checker receipt contract is repaired and hardened.  The
full-GT witness prefix now has identical semantics in both implementations:
an element is serialized in `full_GT_m_witnesses_prefix` only when

```text
pentagon_ok AND h10_ok AND h11_ok
```

The zero-fiber criterion is unchanged: a candidate still requires
`full_GT_identity_count == 0` for at least one row.  No local GAP, Git, push,
GHA, or heavy joint computation was run.

## Exact changes

Producer `search/d972_b4_burau_joint_v1.py`:

- Added shared contract constants `SOURCE_MAP`, `HEXAGON_CONVENTION`, and
  `M_RESIDUE_GATE` at lines 37–39.
- Added `append_full_gt_witness_prefix` at lines 670–679.  The row loop now
  calls it at lines 851–852, so hexagon-only elements cannot enter the prefix.
- Receipt serialization now uses the source/convention constants at lines
  891 and 916–917.
- Selftest lines 996–1004 explicitly reject hexagon-only and partial-hexagon
  witness insertion and accept the full conjunction.

Independent checker `search/check_d972_b4_burau_joint_v1.py`:

- Duplicated the witness-prefix contract independently at lines 657–665 and
  uses it at line 798.
- Added exact checks for producer `source_map`, `algorithm`,
  `hexagon_convention`, and `m_residue_gate` fields (lines 689–690 and
  749–750).
- Added checks for `normal_closure_rounds`, `hprime_generator_count`, and the
  exact Schreier edge count at lines 753–758.
- Added the same adversarial witness mutation cases at lines 852–861.

The workflow required no binding change: its terminal markers already match
the producer, it runs the independent checker for every complete receipt, and
its artifact upload is `always()`.  Its SHA therefore remains unchanged.

## Adversarial consistency audit

I compared the producer's serialized top-level and row fields against every
checker consumer.  All fields are now either checked or intentionally
recomputed: configuration/field/block order, source and semantic bindings,
generator and algorithm metadata, complete joint H′/kernel evidence, right
fiber and both fiber digests, CRT residue/gcd data, all H10/H11/pentagon
counts, first-failure vector, and full-GT witness prefix.  The checker still
rebuilds the four transforms, uses one synchronized source image, and
intersects one common CRT m-residue across specializations.

The slicing audit found no additional producer/checker disagreement: base
pentagon blocks remain the transform-0 five-block slice, while H10/H11 use
the independent transform-1/2/3 slices.  Product orientation and source
hash/terminal-marker bindings remain unchanged.

## Tests

Executed:

```text
python -B -m py_compile search/d972_b4_burau_joint_v1.py search/check_d972_b4_burau_joint_v1.py
python -B search/d972_b4_burau_joint_v1.py --self-test
python -B search/check_d972_b4_burau_joint_v1.py --self-test
```

Observed producer/checker selftest markers:

```text
D972_B4_BURAU_JOINT_V1_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS row=2 exponent=(-4,-8) nonzero=956
D972_B4_BURAU_JOINT_V1_NEGATIVE_FIXTURES_PASS
D972_B4_BURAU_JOINT_V1_SELFTEST_PASS
D972_B4_BURAU_JOINT_V1_CHECKER_NEGATIVE_FIXTURES_PASS
D972_B4_BURAU_JOINT_V1_CHECKER_SELFTEST_PASS
D972_B4_BURAU_JOINT_V1_CHECKER_FINAL_MARKER status=PASS
```

Workflow parse/static checks:

```text
JOINT_YAML_PARSE_AND_STATIC_PASS
JOINT_PRODUCER_CHECKER_CONTRACT_STATIC_PASS
AUTHORIZED_WHITESPACE_STATIC_PASS
```

`git diff --check` was not run because this task explicitly prohibits local
Git operations; the equivalent authorized-file trailing-whitespace audit
passed.  The parent broker can run the requested Git check.

## SHA-256

```text
search/d972_b4_burau_joint_v1.py          AE87EA25C6CEA8DA7F0145F433E94B4FCB1E17709C3A5C1F7F2B449358FAEE15
search/check_d972_b4_burau_joint_v1.py    AD31D32AF1B67298B4AD1A3DCEDF8770568EC2C5B48A3DF73B454C2B93989CF7
.github/workflows/d972-burau-joint-v1.yml 751DABDF330BF4E37B4DA2281E91E2991B10D8D9F74B60F79D5FACB72D1E7192
```

JOINT_RECEIPT_CONSISTENCY_REPAIR_READY
